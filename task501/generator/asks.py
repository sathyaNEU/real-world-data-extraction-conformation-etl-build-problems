"""The asks computed from the ask files as the pack carries them (pandas frames read from the shipped CSVs): the
golden for each and every stop of its ladder. The generator's golden and checks use these; verify.py recomputes the
golden on its own code path."""
import datetime as dt
import re

import pandas as pd

import world as W

REGION_CODES = set(W.REGION_LHO_NEW)          # LH20-LH26, the same areas under both schemes
OPTION_YEARS = {k: W.OPTIONS[k]["years"] for k in W.OPTION_KEYS}
AS_AT = pd.Timestamp(W.AS_AT)
CUT = pd.Timestamp(W.CUTOVER)


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


def ask1(people, how="golden"):
    y = _yob(people)
    m = in_region(people, how)
    return {k: int(((y >= a) & (y <= b) & m).sum()) for k, (a, b) in OPTION_YEARS.items()}


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


def ask2(people, events, log, merges=None, pop="golden", ev_how="golden", merge_how="chain"):
    p = people[in_region(people, pop)]
    y = _yob(p)
    ev = resolve_merges(events, merges, merge_how)
    counts = valid_counts(p, clean_events(ev, log, ev_how))
    n = p["person_id"].map(counts).fillna(0).astype(int)
    out = {}
    for k, (a, b) in OPTION_YEARS.items():
        sel = (y >= a) & (y <= b)
        out[k] = {"none": int(((n == 0) & sel).sum()), "one": int(((n == 1) & sel).sum())}
    return out


LEGACY_IN_COMMENT = re.compile(r"Legacy no\.\s*(MZ\d{2}/\d{4})")


def _components(rows, links):
    """Union of records into one illness per person: links is a list of (i, j) index pairs."""
    parent = {i: i for i in rows}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, j in links:
        a, b = find(i), find(j)
        if a != b:
            parent[max(a, b)] = min(a, b)
    return {i: find(i) for i in rows}


def dedup_cases(cases, how="golden", lab=None):
    """Confirmed cases with rash onset in the window, one per person and illness.
    golden: a back-entered record whose comments name a legacy number held by a migrated record is that record again,
    and records with the same date of birth, sex and onset are one illness notified twice; every record joined by
    either is one case. Stops: none (every row a case); legacy (the comments only); key (date of birth, sex and onset
    only); dob_sex (one per date of birth and sex); window14 (date of birth and sex with onsets within 14 days); lab
    (confirmed cases with a positive result in the laboratory file)."""
    c = cases[(cases["classification"] == "Confirmed")].copy()
    c["onset"] = pd.to_datetime(c["onset_date"])
    c = c[(c["onset"] >= pd.Timestamp(W.WINDOW[0])) & (c["onset"] <= pd.Timestamp(W.WINDOW[1]))]
    if how in ("golden", "legacy", "key"):
        links = []
        if how in ("golden", "legacy"):
            by_legacy = {r: i for i, r in c["legacy_ref"].items() if r}
            ref = c["comments"].fillna("").str.extract(LEGACY_IN_COMMENT)[0]
            links += [(i, by_legacy[r]) for i, r in ref.items() if isinstance(r, str) and r in by_legacy]
        if how in ("golden", "key"):
            first = {}
            for i, r in c.iterrows():
                k = (r["date_of_birth"], r["sex"], r["onset_date"])
                if k in first:
                    links.append((i, first[k]))
                else:
                    first[k] = i
        comp = _components(list(c.index), links)
        keep = sorted({v for v in comp.values()})
        return c.loc[keep]
    if how == "none":
        return c
    if how == "dob_sex":
        return c.drop_duplicates(["date_of_birth", "sex"])
    if how == "window14":
        c = c.sort_values(["date_of_birth", "sex", "onset"])
        keep, last = [], {}
        for i, r in c.iterrows():
            k = (r["date_of_birth"], r["sex"])
            if k in last and (r["onset"] - last[k]).days <= 14:
                continue
            last[k] = r["onset"]
            keep.append(i)
        return c.loc[keep]
    if how == "lab":
        pos = set(lab.loc[lab["result"] == "Positive", "case_id"])
        return c[c["case_id"].isin(pos)]
    raise ValueError(how)


def ask3(cases, how="golden", lab=None):
    c = dedup_cases(cases, how, lab)
    y = _yob(c)
    out = {}
    for k, (a, b) in OPTION_YEARS.items():
        sel = (y >= a) & (y <= b)
        out[k] = {"confirmed": int(sel.sum()), "imported": int((sel & (c["importation"] == "Imported")).sum())}
    return out
