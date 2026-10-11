"""Simulates the borough's homelessness cases (with the members of each household), the move-on queue
and the temporary-accommodation placements from 2012 to the extract cut. Returns plain DataFrames
holding the full truth; extracts.py censors them at the cut and writes the shipped files.

Bedroom need is not drawn: it is the bedroom standard (allocations scheme Part 3) applied to the
household's members on the day, so it moves when a child is born or reaches ten or sixteen."""
import functools

import numpy as np
import pandas as pd

import world as W

FAR = pd.Timestamp("2099-12-31")


def _days(rng, lo, hi, n=None):
    return pd.to_timedelta(rng.integers(lo, hi + 1, n), unit="D")


# ---------------------------------------------------------------- the bedroom standard

@functools.lru_cache(maxsize=None)
def _pairs(kids):
    """largest number of shared rooms among children under 16: two can share if both are under ten,
    or if they are of the same sex"""
    if len(kids) < 2:
        return 0
    (a, s), rest = kids[0], kids[1:]
    best = _pairs(rest)
    for j, (b, t) in enumerate(rest):
        if (a < 10 and b < 10) or s == t:
            best = max(best, 1 + _pairs(rest[:j] + rest[j + 1:]))
    return best


def rooms(members, day):
    """bedrooms the household needs on `day`: one for the applicant (and partner), one for each other
    person aged 16 or over, and the children under 16 paired as far as the standard allows"""
    n, kids = 1, []
    for rel, sex, dob in members:
        if dob > day:
            continue
        if rel in ("Applicant", "Partner"):
            continue
        age = day.year - dob.year - ((day.month, day.day) < (dob.month, dob.day))
        if age >= 16:
            n += 1
        else:
            kids.append((age, sex))
    kids = tuple(sorted(kids))
    return n + len(kids) - _pairs(kids)


def _members(rng, app, typ):
    """the household on the day it applies"""
    def dob(age_years):
        return app - pd.Timedelta(days=int(age_years * 365.25 + rng.integers(0, 365)))
    lead_age = int(rng.integers(18, 56))
    female = rng.random() < (0.86 if typ == "Single parent with children" else 0.5)
    m = [("Applicant", "F" if female else "M", dob(lead_age))]
    if typ.startswith("Couple"):
        m.append(("Partner", "M" if female else "F", dob(max(18, lead_age + int(rng.integers(-5, 6))))))
    if typ in ("Single parent with children", "Couple with children"):
        k = int(rng.choice(list(W.N_CHILDREN), p=list(W.N_CHILDREN.values())))
        span = max(1, min(lead_age - 16, 17))
        ages = sorted(int(rng.integers(0, span + 1)) for _ in range(k))
        for a in ages:
            m.append(("Child", "F" if rng.random() < 0.49 else "M", dob(a)))
        if rng.random() < W.OTHER_ADULT:
            m.append(("Other adult", "F" if rng.random() < 0.5 else "M", dob(int(rng.integers(16, 26)))))
    return m, lead_age


def _births(rng, app, lead_age, typ):
    """births after the application while an adult in the household is under 42"""
    if typ == "Single person" or lead_age >= 42:
        return []
    years = 42 - lead_age
    out, t = [], 0.0
    while True:
        t += rng.exponential(1 / W.BIRTH_RATE)
        if t > years:
            return out
        out.append(app + pd.Timedelta(days=int(t * 365.25)))


def _birthday(dob, age):
    try:
        return pd.Timestamp(year=dob.year + age, month=dob.month, day=dob.day)
    except ValueError:                                   # 29 February in a common year
        return pd.Timestamp(year=dob.year + age, month=3, day=1)


def _changes(members, app):
    """the household's need from the application on, as (date, need) at every change"""
    days = {app}
    for rel, sex, d in members:
        if d > app:
            days.add(d)                                  # a birth
        if rel == "Child":
            for age in (10, 16):
                b = _birthday(d, age)
                if b > app:
                    days.add(b)
    out, last = [], None
    for day in sorted(days):
        n = rooms(members, day)
        if n != last:
            out.append((day, n))
            last = n
    return out


def cases(rng):
    rows = []
    months = pd.date_range(W.SIM_START, W.ASOF, freq="MS")
    for i, m in enumerate(months):
        lam = 92 + 34 * i / len(months)
        if pd.Timestamp("2023-08-01") <= m <= pd.Timestamp("2024-01-01"):
            lam *= 1.35                                  # the autumn 2023 rise in approaches
        n_ta = rng.poisson(lam)
        n_home = rng.poisson(7.5)
        dim = m.days_in_month
        for _ in range(n_ta):
            rows.append(dict(app=m + pd.Timedelta(days=int(rng.integers(0, dim))), placed=True))
        for _ in range(n_home):
            rows.append(dict(app=m + pd.Timedelta(days=int(rng.integers(0, dim))), placed=False))
    df = pd.DataFrame(rows).sort_values("app", kind="mergesort").reset_index(drop=True)
    n = len(df)
    types = list(W.HH_TYPES)
    df["hh_type"] = rng.choice(types, n, p=list(W.HH_TYPES.values()))
    mem, chg = [], []
    for app, typ in zip(df["app"], df["hh_type"]):
        m, lead_age = _members(rng, app, typ)
        for b in _births(rng, app, lead_age, typ):
            m.append(("Child", "F" if rng.random() < 0.49 else "M", b))
        mem.append(m)
        chg.append(_changes(m, app))
    df["members"] = mem
    df["changes"] = chg
    df["need"] = [c[0][1] for c in chg]                   # at application
    df["ta_start"] = df["app"].where(df["placed"])
    lag = rng.integers(21, 76, n)
    slow = rng.random(n) < 0.22                          # inquiries, reviews and late evidence
    lag = np.where(slow, rng.integers(110, 330, n), lag)
    lag_home = rng.integers(30, 71, n)
    df["decision"] = df["app"] + pd.to_timedelta(np.where(df["placed"], lag, lag_home), unit="D")
    df["main"] = np.where(df["placed"], rng.random(n) < 0.52, True)
    df["exit"] = pd.NaT
    df["exit_reason"] = None
    nm = ~df["main"]
    df.loc[nm, "exit"] = df.loc[nm, "decision"] + _days(rng, 0, 14, nm.sum())
    df.loc[nm, "exit_reason"] = rng.choice(
        ["Relief duty ended: accommodation secured", "Main duty not owed", "Contact lost"],
        nm.sum(), p=[0.55, 0.35, 0.10])
    df["duty"] = df["decision"].where(df["main"])
    # early other exits, inside the first 120 days of the main duty only
    oth = df["main"] & (rng.random(n) < 0.12)
    df.loc[oth, "exit"] = df.loc[oth, "duty"] + _days(rng, 5, 120, oth.sum())
    df.loc[oth, "exit_reason"] = rng.choice(
        ["Own arrangements", "Moved out of the area", "Contact lost"], oth.sum(), p=[0.5, 0.3, 0.2])
    df["case_ref"] = [
        "HPR/%02d/%05d" % (a.year % 100, k + 1)
        for k, a in zip(df.groupby(df["app"].dt.year).cumcount(), df["app"])
    ]
    df["hh"] = ["H%06d" % (100000 + i * 7 % 900000) for i in range(n)]
    _pack_changes(df)
    return df


CHECKED = ("Private sector lease", "Nightly-paid self-contained", "Tenter House")


def record_assessments(df, pl, lt):
    """The need as the case records it. It is assessed under the bedroom standard at the decision, again
    when the household reports a birth (a few weeks after it), when the TA team checks the household
    before moving it into self-contained accommodation, and when the lettings team checks it before an
    offer. Nobody reports a birthday, so a child reaching ten or sixteen reaches the record only at the
    next assessment."""
    lag = np.random.default_rng(W.SEED + 7).integers(7, 61, (len(df), 8))
    moves = pl[pl["type"].isin(CHECKED)].groupby("row")["start"].apply(list).to_dict()
    offers = dict(zip(lt["row"], lt["offer_date"]))
    out = []
    for i, (m, d) in enumerate(zip(df["members"], df["decision"])):
        ev = [(d, "Decision")]
        for k, b in enumerate(sorted(x for rel, sex, x in m if x > d)):
            ev.append((b + pd.Timedelta(days=int(lag[i, k % 8])), "Birth reported"))
        for s in moves.get(i, []):
            if s > d:
                ev.append((s, "Household checked before a move in TA"))
        if i in offers:
            ev.append((offers[i], "Household checked before an offer"))
        ev.sort(key=lambda e: e[0])
        out.append([(t, rooms(m, t), why) for t, why in ev])
    df = df.copy()
    df["assess"] = out
    _pack_assess(df)
    return df


def _pack_changes(df):
    k = max(len(c) for c in df["changes"])
    dates = np.full((len(df), k), np.datetime64("2262-01-01"), dtype="datetime64[D]")
    needs = np.zeros((len(df), k), int)
    for i, c in enumerate(df["changes"]):
        for j, (d, nd) in enumerate(c):
            dates[i, j] = np.datetime64(d.date())
            needs[i, j] = nd
        needs[i, len(c):] = c[-1][1]
    df.attrs["cp_dates"] = dates
    df.attrs["cp_needs"] = needs


def _pack_assess(df):
    k = max(len(a) for a in df["assess"])
    dates = np.full((len(df), k), np.datetime64("2262-01-01"), dtype="datetime64[D]")
    needs = np.zeros((len(df), k), int)
    for i, a in enumerate(df["assess"]):
        for j, (d, nd, why) in enumerate(a):
            dates[i, j] = np.datetime64(d.date())
            needs[i, j] = nd
        needs[i, len(a):] = a[-1][1]
    df.attrs["as_dates"] = dates
    df.attrs["as_needs"] = needs


def recorded_at(df, t, rows=None):
    """bedroom need as the case recorded it on day t (the latest assessment on or before t)"""
    dates, needs = df.attrs["as_dates"], df.attrs["as_needs"]
    if rows is not None:
        dates, needs = dates[rows], needs[rows]
    t = np.datetime64(pd.Timestamp(t).date())
    j = np.maximum((dates <= t).sum(axis=1) - 1, 0)
    return needs[np.arange(len(needs)), j]


def need_at(df, t, rows=None):
    """bedroom need of every case (or of `rows`) on day t"""
    dates, needs = df.attrs["cp_dates"], df.attrs["cp_needs"]
    if rows is not None:
        dates, needs = dates[rows], needs[rows]
    t = np.datetime64(pd.Timestamp(t).date())
    j = np.maximum((dates <= t).sum(axis=1) - 1, 0)
    return needs[np.arange(len(needs)), j]


def need_on(df, rows, days):
    """bedroom need of each of `rows` on its own day"""
    dates, needs = df.attrs["cp_dates"][rows], df.attrs["cp_needs"][rows]
    t = np.asarray(pd.to_datetime(days).values.astype("datetime64[D]"))[:, None]
    j = np.maximum((dates <= t).sum(axis=1) - 1, 0)
    return needs[np.arange(len(needs)), j]


def round_date(month):
    """the offer round for tenancies starting in `month`: the third Monday of the month before"""
    prev = (month - pd.DateOffset(months=1)).replace(day=1)
    first_monday = prev + pd.Timedelta(days=(7 - prev.weekday()) % 7)
    return first_monday + pd.Timedelta(days=14)


def allocate(df, rng, last_start_month):
    """Move-on lets in monthly offer rounds: each month's lets of each size go, in the round held the
    month before, to the first households of that size's list on the day of the round (main duty
    accepted and still owed, need on the day equal to the home's bedrooms, earliest duty date, then case
    reference). Tenancies start through the month."""
    lets = []
    duty = df["duty"].values.astype("datetime64[D]")
    ref = df["case_ref"].values
    order_key = np.lexsort((ref, duty))
    rank = np.empty(len(df), int)
    rank[order_key] = np.arange(len(df))
    exit_ = df["exit"].values.astype("datetime64[D]")
    has_exit = ~pd.isna(df["exit"]).values
    main = df["main"].values
    taken = np.zeros(len(df), bool)
    for m in pd.date_range(W.SIM_START + pd.DateOffset(months=1), last_start_month, freq="MS"):
        r = round_date(m)
        t = np.datetime64(r.date())
        nd = need_at(df, r)
        for s in W.SIZES_LET:
            k = rng.poisson(W.supply(m, s) if s <= 4 else W.supply5(m))
            if k == 0:
                continue
            ok = main & (duty <= t) & ~taken & (nd == s) & (~has_exit | (exit_ > t))
            idx = np.flatnonzero(ok)
            if not len(idx):
                continue
            pick = idx[np.argsort(rank[idx])][:k]
            starts = sorted(m + pd.Timedelta(days=int(x)) for x in rng.integers(0, m.days_in_month, len(pick)))
            for j, st in zip(pick, starts):
                taken[j] = True
                exit_[j] = np.datetime64(st.date())
                has_exit[j] = True
                lets.append((st, s, j, r))
    lt = pd.DataFrame(lets, columns=["tenancy_start", "size", "row", "offer_date"])
    df = df.copy()
    df.loc[lt["row"].values, "exit"] = lt["tenancy_start"].values
    kind = np.where(rng.random(len(lt)) < 0.76, "Settled: social housing let", "Settled: private let (Larkmoor Lettings)")
    df.loc[lt["row"].values, "exit_reason"] = kind
    lt["kind"] = kind
    return df, lt


def hash_pick(uid, f):
    import zlib
    return zlib.crc32(("%s|%s" % (uid, f.date())).encode())


def _tenter_house(df, rows, far):
    """Tenter House flats are let, from the day the block opened until the owner's notice, to the
    household that has been in a nightly-paid flat longest under the main duty (earliest duty date,
    then case reference) among those whose bedroom need matches the flat (four-bedroom flats house
    households needing four or more); the move takes place a week after the flat falls vacant."""
    import heapq
    units = [(W.TH_OPEN + pd.Timedelta(days=int(k * 56 / sum(W.TH_UNITS.values()))), s, "TH-%d%02d" % (s, q + 1))
             for k, (s, q) in enumerate((s, q) for s in W.SIZES for q in range(W.TH_UNITS[s]))]
    heapq.heapify(units)
    np_idx = [j for j, r in enumerate(rows) if r[1] == "Nightly-paid self-contained"]
    hh = np.array([rows[j][0] for j in np_idx])
    st = np.array([rows[j][3] for j in np_idx], dtype="datetime64[ns]")
    en = np.array([rows[j][4] for j in np_idx], dtype="datetime64[ns]")
    duty = df["duty"].values.astype("datetime64[ns]")[hh]
    order = np.lexsort((df["case_ref"].values[hh], duty))
    rank = np.empty(len(hh), int)
    rank[order] = np.arange(len(hh))
    avail = np.ones(len(hh), bool)
    while units:
        f, s, uid = heapq.heappop(units)
        if f + pd.Timedelta(days=7) >= W.NOTICE:
            continue
        t = np.datetime64(f)
        nd = np.minimum(need_at(df, f, hh), 4)
        ok = avail & (st < t) & (en > t + np.timedelta64(45, "D")) & (nd == s)
        if not ok.any():
            heapq.heappush(units, (f + pd.Timedelta(days=14), s, uid))
            continue
        cand = np.flatnonzero(ok)
        if f >= W.TH_RULE:
            c = cand[np.argmin(rank[cand])]
        else:
            # before the rule, flats went by school and support ties: no order by waiting time
            c = cand[(hash_pick(uid, f) % len(cand))]
        j = np_idx[c]
        avail[hh == hh[c]] = False
        i_, typ, unit, st_, en_, kind = rows[j]
        mv = f + pd.Timedelta(days=7)
        rows[j] = (i_, typ, unit, st_, mv, "move")
        rows.append((i_, "Tenter House", uid, mv, en_, kind))
        if en_ < far:
            heapq.heappush(units, (en_ + pd.Timedelta(days=4), s, uid))


def placements(df, rng):
    """Every temporary-accommodation placement, start and end. A household starts in bed and
    breakfast or a hostel; once the main duty is accepted it moves to self-contained accommodation:
    a private sector lease or a nightly-paid flat, and since April 2021 Tenter House when a flat of
    its need falls vacant."""
    rows = []
    far = FAR
    placed = df[df["placed"]]
    fl = rng.integers(14, 71, len(placed))
    ft = rng.choice(["Bed and breakfast", "Hostel"], len(placed), p=[0.6, 0.4])
    wait = rng.integers(3, 31, len(placed))
    u_away = rng.random(len(placed))
    u_away_t = rng.random(len(placed))
    u_np = rng.random(len(placed))
    u_np_move = rng.random(len(placed))
    u_np_t = rng.random(len(placed))
    seq = []
    for k, (i, r) in enumerate(placed.iterrows()):
        end = r["exit"] if pd.notna(r["exit"]) else far
        if not r["main"]:
            rows.append((i, ft[k], None, r["ta_start"], end, "left"))
            continue
        d2 = max(r["ta_start"] + pd.Timedelta(days=int(fl[k])), r["duty"] + pd.Timedelta(days=int(wait[k])))
        if end <= d2:
            rows.append((i, ft[k], None, r["ta_start"], end, "left"))
            continue
        rows.append((i, ft[k], None, r["ta_start"], d2, "move"))
        seq.append((d2, i, k, end))
    seq.sort(key=lambda x: (x[0], x[1]))
    for d2, i, k, end in seq:
        span = (min(end, W.ASOF + pd.Timedelta(days=400)) - d2).days
        away = None
        if u_away[k] < 0.05 and span > 150:
            away = d2 + pd.Timedelta(days=int(60 + u_away_t[k] * (span - 90)))
        stop = away if away is not None else end
        last = "away" if away is not None else "left"
        t2 = "Private sector lease" if u_np[k] < 0.45 else "Nightly-paid self-contained"
        if t2 == "Nightly-paid self-contained" and u_np_move[k] < 0.25 and (stop - d2).days > 240:
            d3 = d2 + pd.Timedelta(days=int(90 + u_np_t[k] * ((min(stop, far) - d2).days - 150)))
            rows.append((i, t2, None, d2, d3, "move"))
            rows.append((i, "Private sector lease", None, d3, stop, last))
        else:
            rows.append((i, t2, None, d2, stop, last))
    _tenter_house(df, rows, far)
    out = []
    split_u = rng.random(len(rows))
    split_t = rng.random(len(rows))
    for k, r in enumerate(rows):
        i, typ, unit, st, en, kind = r
        span = (min(en, W.ASOF + pd.Timedelta(days=60)) - st).days
        if typ in ("Bed and breakfast", "Hostel") and split_u[k] < 0.55 and span >= 12:
            mid = st + pd.Timedelta(days=int(4 + split_t[k] * (span - 8)))
            other = "Hostel" if (typ == "Bed and breakfast" and split_t[k] < 0.5) else "Bed and breakfast"
            out.append((i, typ, None, st, mid, "move"))
            out.append((i, other, None, mid, en, kind))
        else:
            out.append(r)
    pl = pd.DataFrame(out, columns=["row", "type", "unit", "start", "end", "end_kind"])
    pl = pl.sort_values(["start", "row"], kind="mergesort").reset_index(drop=True)
    return pl
