"""The ask computed from the register's files as the pack carries them (pandas frames read from the shipped CSVs): the
golden for each option's people the register holds in the region, and of those the people with no valid MMR dose and
with exactly one, and every stop of their ladder. The generator's golden and checks use these; verify.py recomputes
the golden on its own code path."""
import pandas as pd

import world as W

REGION_CODES = set(W.REGION_LHO_NEW)          # LH20-LH26, the same areas under both schemes
OPTION_YEARS = {k: W.OPTIONS[k]["years"] for k in W.OPTION_KEYS}
AS_AT = pd.Timestamp(W.AS_AT)
CUT = pd.Timestamp(W.CUTOVER)
GP_LINE = "GPR-"
# a registration's household as the register holds it: twins registered together from one birth notification share
# every one of these
HOUSEHOLD = ("date_of_birth", "sex", "gp_practice", "registered_on", "lho_code", "lho_recorded", "postcode")
DECADE = 10
REG_WINDOW = (6, 45)            # days from a birth to its registration from the birth notification
FIRST_DOSE_WINDOW = (365, 525)  # days from a birth to the GP's first dose at the schedule's age (12 months, or 15)


def _yob(df):
    return pd.to_datetime(df["date_of_birth"]).dt.year


def outside_state(people):
    """An address with a UK postcode (Northern Ireland): not in the State, so not in the region, whatever area code the
    record carries."""
    return people["postcode"].fillna("").str.upper().str.startswith("BT")


def in_region(people, how="golden"):
    """Who the register holds as living in the region. golden: an address in the State whose local health office,
    read in the scheme in force when it was recorded, is in the region (LH20-LH26 under either scheme, LH27 only where
    it was recorded before 1 July 2024, Monaghan West). Stops: current (the current code list, every address),
    lh27 (LH27 read by its recorded date, every address: the circular cracked), state (the current code list, addresses
    in the State only), old (every LH27 read as Monaghan West, addresses in the State), all (every active registration)."""
    code = people["lho_code"]
    rec = pd.to_datetime(people["lho_recorded"])
    by_code = code.isin(REGION_CODES) | ((code == "LH27") & (rec < CUT))
    here = ~outside_state(people)
    if how == "golden":
        return by_code & here
    if how == "current":
        return code.isin(REGION_CODES)
    if how == "lh27":
        return by_code
    if how == "state":
        return code.isin(REGION_CODES) & here
    if how == "old":
        return code.isin(REGION_CODES | {"LH27"}) & here
    if how == "all":
        return pd.Series(True, index=people.index)
    raise ValueError(how)


def _union(ids, links):
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in links:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return {i: find(i) for i in ids}


LINKS = ("golden", "none", "any_ref", "dob_sex_area", "dob_sex_postcode", "household")


def persons(f, link="golden", merge_how="chain"):
    """Which registrations in the people extract are one person, as a map from registration to person. golden: every
    registration is one child (registrations holding one GP return line once the merges are followed would be one
    child's; none does). Stops: none (every registration a person, the same map); any_ref (any shared source
    reference joins, and a school session's is every pupil's there); dob_sex_area and dob_sex_postcode (a person key
    over the registrations' own fields, the postcode only where one was recorded); household (registrations sharing
    every field of HOUSEHOLD joined as one child: twins merged)."""
    people = f["people"]
    ids = list(people["person_id"])
    if link == "none":
        return {i: i for i in ids}
    links = []
    if link in ("golden", "any_ref"):
        ev = resolve_merges(f["events"], f["merges"], merge_how)
        ev = ev[ev["person_id"].isin(set(ids))]
        if link == "golden":
            ev = ev[ev["source_ref"].str.startswith(GP_LINE)]
        held = ev.groupby("source_ref")["person_id"].nunique()
        shared = ev[ev["source_ref"].isin(set(held[held > 1].index))]
        for _, grp in shared.groupby("source_ref")["person_id"]:
            u = sorted(set(grp))
            links.extend((u[0], x) for x in u[1:])
        return _union(ids, links)
    if link == "dob_sex_area":
        key = people["date_of_birth"] + "|" + people["sex"] + "|" + people["lho_code"].fillna("")
        keep = [True] * len(people)
    elif link == "dob_sex_postcode":
        key = people["date_of_birth"] + "|" + people["sex"] + "|" + people["postcode"].fillna("")
        keep = list(people["postcode"].fillna("") != "")
    elif link == "household":
        key = people[list(HOUSEHOLD)].fillna("").agg("|".join, axis=1)
        keep = [True] * len(people)
    else:
        raise ValueError(link)
    first = {}
    for pid, k, kp in zip(people["person_id"], key, keep):
        if not kp:
            continue
        if k in first:
            links.append((first[k], pid))
        else:
            first[k] = pid
    return _union(ids, links)


def _population(people, how, unlisted):
    m = in_region(people, how)
    if unlisted == "drop":
        m = m & (people["gp_practice"].fillna("") != "")
    return m


def _plus_years(s, n):
    """ISO dates n years on (no date of birth on the register falls on 29 February)."""
    return (s.str[:4].astype(int) + n).astype(str) + s.str[4:]


def decade_early(f, events=None, rule="both"):
    """Registrations whose date of birth the register holds ten years early. The child was registered from the birth
    notification, 6 to 45 days after the date ten years on, and had the GP's first dose 12 to 17 months after that
    date (its events re-pointed through the merges, less the lines replaced or withdrawn). rule: both (the golden),
    registration (the registration alone), first_dose (the first GP dose alone)."""
    people = f["people"]
    ten = pd.to_datetime(_plus_years(people["date_of_birth"], DECADE))
    off = (pd.to_datetime(people["registered_on"]) - ten).dt.days
    by_reg = set(people.loc[off.between(*REG_WINDOW), "person_id"])
    ev = clean_events(resolve_merges(f["events"] if events is None else events, f["merges"]), f["log"])
    gp = ev[ev["source_ref"].str.startswith(GP_LINE)]
    first = pd.to_datetime(gp.groupby("person_id")["date_given"].min())
    tenmap = dict(zip(people["person_id"], ten))
    lag = {p: (d - tenmap[p]).days for p, d in first.items() if p in tenmap}
    by_dose = {p for p, x in lag.items() if FIRST_DOSE_WINDOW[0] <= x <= FIRST_DOSE_WINDOW[1]}
    if rule == "registration":
        return by_reg
    if rule == "first_dose":
        return by_dose
    if rule == "both":
        return by_reg & by_dose
    raise ValueError(rule)


DOB_HOWS = ("corrected", "held", "registration", "first_dose", "any_birthday")


def people_as_born(f, dob_how="corrected"):
    """The people extract with each date of birth as the child was born. corrected (the golden): a date of birth held
    ten years early read ten years on (decade_early). Stops: held (as the register holds it); registration and
    first_dose (one signature alone, the same registrations); any_birthday (every registration made 6 to 45 days after
    any birthday read as a birth registration: over-cleaning)."""
    people = f["people"]
    if dob_how == "held":
        return people
    p = people.copy()
    if dob_how == "any_birthday":
        reg = pd.to_datetime(p["registered_on"])
        shift = pd.Series(0, index=p.index)
        for n in range(1, 21):
            off = (reg - pd.to_datetime(_plus_years(p["date_of_birth"], n))).dt.days
            shift = shift.where(shift > 0, n * off.between(*REG_WINDOW))
        for n in sorted(set(shift) - {0}):
            m = shift == n
            p.loc[m, "date_of_birth"] = _plus_years(p.loc[m, "date_of_birth"], n)
        return p
    shifted = decade_early(f, rule="both" if dob_how == "corrected" else dob_how)
    m = p["person_id"].isin(shifted)
    p.loc[m, "date_of_birth"] = _plus_years(p.loc[m, "date_of_birth"], DECADE)
    return p


def ask1(f, how="golden", link="golden", unlisted="keep", dob_how="corrected"):
    """Each option's people the register holds as living in the region, one per person, by the year each was born:
    how reads the area code (in_region), link joins the registrations that are one person (persons), dob_how reads
    the date of birth (people_as_born), unlisted="drop" leaves out registrations no practice lists (a stop)."""
    people = people_as_born(f, dob_how)
    sel = people[_population(people, how, unlisted)]
    y = _yob(sel)
    who = sel["person_id"].map(persons(f, link))
    return {k: int(who[(y >= a) & (y <= b)].nunique()) for k, (a, b) in OPTION_YEARS.items()}


def clean_events(events, log, how="golden"):
    """golden: drop events loaded from GP lines the log shows replaced or withdrawn; keep lines confirmed as sent.
    all: keep every loaded event. drop_queried: drop every queried line. drop_unresolved: keep a queried line only
    where the log shows it confirmed as sent and closed by the as-at date (an open query read as not standing; SF17)."""
    ev = events
    if how == "golden":
        bad = set(log.loc[log["outcome"].isin(["Replaced by corrected line", "Withdrawn by practice"]), "line_ref"])
        ev = ev[~ev["source_ref"].isin(bad)]
    elif how == "drop_queried":
        ev = ev[~ev["source_ref"].isin(set(log["line_ref"]))]
    elif how == "drop_unresolved":
        stands = ((log["outcome"] == "Confirmed as sent") & (log["closed_on"] != "")
                  & (log["closed_on"] <= W.AS_AT.isoformat()))
        ev = ev[~ev["source_ref"].isin(set(log.loc[~stands, "line_ref"]))]
    elif how != "all":
        raise ValueError(how)
    return ev


def reattribute(people, ev):
    """A child has one MMR dose at a visit. Where one registration holds two GP return lines given on one day, the
    second is its co-twin's: the one other registration of its household (HOUSEHOLD, as the register holds it) with
    no GP line that day. ev: events already re-pointed through the merges and cleaned of replaced and withdrawn
    lines."""
    gp = ev[ev["source_ref"].str.startswith(GP_LINE)]
    n = gp.groupby(["person_id", "date_given"])["source_ref"].transform("nunique")
    dbl = gp[n >= 2].sort_values(["person_id", "date_given", "source_ref"])
    if not len(dbl):
        return ev
    cols = list(HOUSEHOLD)
    pk = people[["person_id"] + cols].fillna("")
    homes = pk[pk["person_id"].isin(set(dbl["person_id"]))][cols].drop_duplicates()
    cand = pk.merge(homes, on=cols)
    mates = {}
    for _, grp in cand.groupby(cols)["person_id"]:
        ms = list(grp)
        for m in ms:
            mates[m] = [x for x in ms if x != m]
    gpc = gp[gp["person_id"].isin(set(cand["person_id"]))]
    days = {p: set(d) for p, d in gpc.groupby("person_id")["date_given"]}
    ev = ev.copy()
    for (pid, day), grp in dbl.groupby(["person_id", "date_given"]):
        cand = [c for c in mates.get(pid, []) if day not in days.get(c, set())]
        if len(cand) == 1:
            for idx in grp.index[1:]:
                ev.at[idx, "person_id"] = cand[0]
    return ev


def valid_counts(people, events):
    """Valid MMR doses per person at 30 June 2027 under the guidelines: on or after the first birthday and at least
    28 days after the previous valid dose. Vectorised over people, one pass per dose position."""
    import numpy as np
    pid = people["person_id"].to_numpy()
    dob = pd.to_datetime(people["date_of_birth"])
    first = pd.to_datetime(pd.DataFrame({"year": dob.dt.year + 1, "month": dob.dt.month, "day": dob.dt.day}))
    idx = {p: i for i, p in enumerate(pid)}
    ev = events[events["person_id"].isin(idx)]
    d = pd.to_datetime(ev["date_given"])
    keep = d <= AS_AT
    ev, d = ev[keep], d[keep]
    pi = ev["person_id"].map(idx).to_numpy()
    day = (d.to_numpy().astype("datetime64[D]").astype(np.int64))
    fb = first.to_numpy().astype("datetime64[D]").astype(np.int64)
    order = np.lexsort((day, pi))
    pi, day = pi[order], day[order]
    rank = np.zeros(len(pi), dtype=int)
    if len(pi):
        new = np.r_[True, pi[1:] != pi[:-1]]
        start = np.maximum.accumulate(np.where(new, np.arange(len(pi)), 0))
        rank = np.arange(len(pi)) - start
    count = np.zeros(len(pid), dtype=int)
    prev = np.full(len(pid), -10 ** 9, dtype=np.int64)
    for r in range(int(rank.max()) + 1 if len(rank) else 0):
        m = rank == r
        p_, d_ = pi[m], day[m]
        ok = (d_ >= fb[p_]) & (d_ - prev[p_] >= 28)
        count[p_] += ok
        prev[p_] = np.where(ok, d_, prev[p_])
    return dict(zip(pid, count))


def resolve_merges(events, merges, how="chain"):
    """Events re-pointed to the registration they now belong to. chain: follow every merge to the surviving record
    (the golden); one_hop: follow one merge only; none: the record each event was loaded to."""
    if how == "none" or merges is None or not len(merges):
        return events
    m = dict(zip(merges["retired_number"], merges["surviving_number"]))

    def final(x):
        seen = 0
        while x in m and seen < 10:
            x = m[x]
            seen += 1
            if how == "one_hop":
                break
        return x
    ev = events.copy()
    ev["person_id"] = ev["person_id"].map(lambda x: final(x) if x in m else x)
    return ev


TWINS = ("reattributed", "loaded")


def ask2(f, pop="golden", ev_how="golden", merge_how="chain", link="golden", events=None, unlisted="keep",
         twins="reattributed", dob_how="corrected"):
    """Of the option's people (pop, link, unlisted and dob_how as in ask1), those with no valid dose and with exactly one
    at 30 June 2027: each person's events re-pointed through the merges (merge_how), less the GP return lines the
    query log shows replaced or withdrawn (ev_how), each line a twin's loader put on its co-twin given back to the
    child it was given to (twins="reattributed"; "loaded" leaves every line where it was loaded), counted under the
    guidelines' 12.5 from the date each person was born; events, when given, replaces the extract's."""
    people = people_as_born(f, dob_how)
    who = persons(f, link, merge_how)
    p = people[_population(people, pop, unlisted)]
    p = p.assign(person_id=p["person_id"].map(who)).drop_duplicates("person_id")
    ev = resolve_merges(f["events"] if events is None else events, f["merges"], merge_how)
    ev = clean_events(ev, f["log"], ev_how)
    if twins == "reattributed":
        ev = reattribute(f["people"], ev)
    elif twins != "loaded":
        raise ValueError(twins)
    ev = ev.assign(person_id=ev["person_id"].map(lambda x: who.get(x, x)))
    counts = valid_counts(p, ev)
    y = _yob(p)
    n = p["person_id"].map(counts).fillna(0).astype(int)
    out = {}
    for k, (a, b) in OPTION_YEARS.items():
        sel = (y >= a) & (y <= b)
        out[k] = {"none": int(((n == 0) & sel).sum()), "one": int(((n == 1) & sel).sum())}
    return out
