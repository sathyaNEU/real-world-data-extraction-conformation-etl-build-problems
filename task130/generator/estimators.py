"""The golden reading and every rung of the ladder, computed from the shipped files only."""
import functools
import os

import numpy as np
import pandas as pd
import openpyxl

ASOF = pd.Timestamp("2026-09-30")
UNITS_START = pd.Timestamp("2027-04-01")
SIZES = [1, 2, 3, 4]
MONTH_ENDS = [pd.Timestamp(x) for x in ("2026-10-31", "2026-11-30", "2026-12-31", "2027-01-31",
                                         "2027-02-28", "2027-03-31")]
OCTOBER = pd.Timestamp("2026-10-01")
TENANCY_MONTHS = [pd.Timestamp(x) for x in ("2026-11-01", "2026-12-01", "2027-01-01", "2027-02-01", "2027-03-01")]
F = {
    "cases": "homelessness_cases_2026-09-30.csv",
    "placements": "ta_placements_2018-04_2026-09.csv",
    "reviews": "bedroom_need_reviews.csv",
    "members": "household_members_2026-09-30.csv",
    "lets": "moveon_lets_2018-04_2026-09.csv",
    "plan": "moveon_plan_2026-27.xlsx",
    "prices": "dps_lot2_lot3_price_schedule.xlsx",
}


def load(target):
    p = lambda k: os.path.join(target, F[k])
    c = pd.read_csv(p("cases"), dtype=str, keep_default_na=False)
    pl = pd.read_csv(p("placements"), dtype=str, keep_default_na=False)
    rv = pd.read_csv(p("reviews"), dtype=str, keep_default_na=False)
    mb = pd.read_csv(p("members"), dtype=str, keep_default_na=False)
    lt = pd.read_csv(p("lets"), dtype=str, keep_default_na=False)
    for df, cols in ((c, ["application_date", "decision_date", "closed_date"]),
                     (pl, ["placement_start", "placement_end"]), (rv, ["review_date"]),
                     (lt, ["offer_date", "tenancy_start"]), (mb, ["date_of_birth"])):
        for k in cols:
            df[k] = pd.to_datetime(df[k].replace("", None))
    rv["bedrooms_after"] = rv["bedrooms_after"].astype(int)
    lt["bedrooms"] = lt["bedrooms"].astype(int)
    c["need0"] = pd.to_numeric(c["bedrooms_needed_at_decision"].replace("", None))
    return c, pl, rv, mb, lt


def plan(target, sheet="Revised 14 Sep 2026"):
    """lets by bedrooms in the home (5 meaning five or more) for each month, October to March"""
    ws = openpyxl.load_workbook(os.path.join(target, F["plan"]), data_only=False)[sheet]
    out = {}
    for r in range(5, 10):
        s = ws.cell(row=r, column=1).value
        s = 5 if s == "5 or more" else int(s)
        out[s] = [int(ws.cell(row=r, column=8 + j).value) for j in range(6)]
    return out


def lot3_2728(target):
    ws = openpyxl.load_workbook(os.path.join(target, F["prices"]))["Rates"]
    out = {}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] == "3":
            out[4 if r[3] == "4+" else int(r[3])] = float(r[5])
    return out


# ---------------- Part 3: the bedroom standard ----------------

@functools.lru_cache(maxsize=None)
def _shared(kids):
    """most pairs of children under 16 that can share a room: both under 10, or of the same sex"""
    if len(kids) < 2:
        return 0
    (a, s), rest = kids[0], kids[1:]
    best = _shared(rest)
    for j, (b, t) in enumerate(rest):
        if (a < 10 and b < 10) or s == t:
            best = max(best, 1 + _shared(rest[:j] + rest[j + 1:]))
    return best


def _age(dob, day):
    return day.year - dob.year - ((day.month, day.day) < (dob.month, dob.day))


def rooms(people, day):
    """people: (relationship, sex, date of birth) for everyone on the application"""
    n, kids = 1, []
    for rel, sex, dob in people:
        if rel in ("Applicant", "Partner") or dob > day:
            continue
        a = _age(dob, day)
        if a >= 16:
            n += 1
        else:
            kids.append((a, sex))
    kids = tuple(sorted(kids))
    return n + len(kids) - _shared(kids)


def households(mb):
    return {ref: list(zip(g["relationship"], g["sex"], g["date_of_birth"]))
            for ref, g in mb.groupby("case_ref", sort=False)}


def part3(hh, refs, day):
    """need under Part 3 on `day` of each case in `refs`, from the people on its application"""
    refs = list(refs)
    return pd.Series([rooms(hh[r], day) for r in refs], index=refs)


def recorded(c, rv, t):
    """need as the case records it on day t: the decision, then the latest review on or before t"""
    n = c.set_index("case_ref")["need0"].copy()
    r = rv[rv["review_date"] <= t].sort_values(["review_date"], kind="mergesort")
    last = r.groupby("case_ref")["bedrooms_after"].last()
    n.loc[last.index] = last.values
    return n


# ---------------- the lists ----------------

def open_main(c, t):
    """cases owed the main duty on day t: accepted on or before t and not closed by t"""
    m = (c["decision"] == "Main duty accepted") & (c["decision_date"] <= t)
    m &= c["closed_date"].isna() | (c["closed_date"] > t)
    return c[m]


def tenter_house(pl, t=ASOF):
    live = (pl["accommodation_type"] == "Tenter House") & (pl["placement_start"] <= t)
    live &= pl["placement_end"].isna() | (pl["placement_end"] > t)
    return set(pl.loc[live, "case_ref"])


def in_ta(pl, t=ASOF):
    live = (pl["placement_start"] <= t) & (pl["placement_end"].isna() | (pl["placement_end"] > t))
    return set(pl.loc[live, "case_ref"])


def round_date(month):
    """the offer round for tenancies starting in `month`: the third Monday of the month before"""
    prev = (month - pd.DateOffset(months=1)).replace(day=1)
    first_monday = prev + pd.Timedelta(days=(7 - prev.weekday()) % 7)
    return first_monday + pd.Timedelta(days=14)


def accepted_october(lt):
    return set(lt.loc[lt["let_status"] == "Accepted, tenancy to start", "case_ref"])


def runoff(c, pl, lt, P, list_need, unit_need, order="duty", members="all", lump=False, october="log"):
    """Month-end households still in Tenter House, October to March, by replacement unit size.

    list_need(day, refs) gives each listed case's bedrooms on a round day; unit_need (a Series by case)
    is the unit size each Tenter House household is counted under. The October lets were offered in the
    September round and are in the lets log ("log"); "plan" runs the September round from the plan's
    October column instead, and "twice" does both."""
    q = open_main(c, ASOF).copy()
    if members == "ta":
        q = q[q["case_ref"].isin(in_ta(pl))]
    if order == "ta_start":
        first = pl.groupby("case_ref")["placement_start"].min()
        q["key"] = q["case_ref"].map(first).fillna(q["application_date"])
    elif order == "application":
        q["key"] = q["application_date"]
    else:
        q["key"] = q["decision_date"]
    q = q.sort_values(["key", "case_ref"], kind="mergesort")
    refs = q["case_ref"].tolist()
    th = tenter_house(pl)
    is_th = np.array([r in th for r in refs])
    unit = np.minimum(unit_need.reindex(refs).fillna(0).astype(int).values, 4)
    gone = np.zeros(len(refs), bool)
    if october in ("log", "twice"):
        acc = accepted_october(lt)
        gone |= np.array([r in acc for r in refs])
    steps = [(m, {s: P[s][k + 1] for s in P}) for k, m in enumerate(TENANCY_MONTHS)]
    if october in ("plan", "twice"):
        steps = [(OCTOBER, {s: P[s][0] for s in P})] + steps
    out = {s: [] for s in SIZES}

    def take(m, pk):
        nd = np.asarray(list_need(round_date(m), refs), dtype=int)
        if lump:
            nd = np.minimum(nd, 4)
        for s, n in pk.items():
            if n > 0:
                idx = np.flatnonzero((nd == s) & ~gone)[:n]
                gone[idx] = True

    def count():
        for s in SIZES:
            out[s].append(int(((unit == s) & is_th & ~gone).sum()))
    if steps[0][0] == OCTOBER:
        take(*steps.pop(0))
    count()                                   # 31 October
    for m, pk in steps:
        take(m, pk)
        count()
    return out


def golden(target):
    c, pl, rv, mb, lt = load(target)
    hh = households(mb)
    P = plan(target)
    th = sorted(tenter_house(pl))
    unit = part3(hh, th, UNITS_START)
    return runoff(c, pl, lt, P, lambda day, refs: part3(hh, refs, day).values, unit)


def start_counts(pl, hh):
    th = sorted(tenter_house(pl))
    u = np.minimum(part3(hh, th, UNITS_START).values, 4)
    return {s: int((u == s).sum()) for s in SIZES}


def callout(run):
    return {s: run[s][-1] for s in SIZES}


def weekly_cost(units, rates):
    return sum(units[s] * rates[s] for s in SIZES)


# ---------------- the wrong rungs ----------------

def rung_recorded(c, rv, pl, lt, P, hh, unit="recorded", lump=True):
    """the queue on the need the case records on 30 September (the stump), lumped at four by default"""
    rec = recorded(c, rv, ASOF)
    th = sorted(tenter_house(pl))
    u = rec.reindex(th) if unit == "recorded" else part3(hh, th, UNITS_START)
    return runoff(c, pl, lt, P, lambda day, refs: rec.reindex(refs).values, u, lump=lump)


def rung_frozen(c, pl, lt, P, hh, day=ASOF, unit_day=UNITS_START, lump=False):
    """Part 3 need from the application, but worked out once (on `day`) for every round"""
    q = open_main(c, ASOF)
    fixed = part3(hh, q["case_ref"], day)
    th = sorted(tenter_house(pl))
    return runoff(c, pl, lt, P, lambda d, refs: fixed.reindex(refs).values, part3(hh, th, unit_day), lump=lump)


def rung_dynamic(c, pl, lt, P, hh, unit_day=UNITS_START, lump=False, members="all", order="duty", october="log"):
    """Part 3 need on each round day (the answer's list rule) with one other choice changed"""
    th = sorted(tenter_house(pl))
    return runoff(c, pl, lt, P, lambda d, refs: part3(hh, refs, d).values, part3(hh, th, unit_day),
                  lump=lump, members=members, order=order, october=october)


def rung_none(pl, unit):
    th = sorted(tenter_house(pl))
    u = np.minimum(unit.reindex(th).values, 4)
    return {s: [int((u == s).sum())] * 6 for s in SIZES}


def monthly_rate(c, rv, months=12):
    """share of main-duty households leaving each month over the last `months` months, by recorded need"""
    starts = pd.date_range(ASOF - pd.DateOffset(months=months) + pd.Timedelta(days=1), ASOF, freq="MS")
    tot = {s: [0, 0] for s in SIZES}
    for m in starts:
        me = m + pd.offsets.MonthEnd(0)
        o = open_main(c, m - pd.Timedelta(days=1))
        nd = np.minimum(recorded(c, rv, m).reindex(o["case_ref"]).values, 4)
        left = (o["closed_date"] <= me).values
        for s in SIZES:
            tot[s][0] += int(((nd == s) & left).sum())
            tot[s][1] += int((nd == s).sum())
    return {s: tot[s][0] / tot[s][1] for s in SIZES}


def rung_rate(c, rv, pl):
    th = sorted(tenter_house(pl))
    u = np.minimum(recorded(c, rv, ASOF).reindex(th).values, 4)
    n = {s: int((u == s).sum()) for s in SIZES}
    r = monthly_rate(c, rv)
    return {s: [n[s] * (1 - r[s]) ** (k + 1) for k in range(6)] for s in SIZES}


def rung_share(c, rv, pl, P):
    rec = recorded(c, rv, ASOF)
    th = sorted(tenter_house(pl))
    u = np.minimum(rec.reindex(th).values, 4)
    n = {s: int((u == s).sum()) for s in SIZES}
    q = open_main(c, ASOF)
    nd = np.minimum(rec.reindex(q["case_ref"]).values, 4)
    out = {}
    for s in SIZES:
        L = (nd == s).sum()
        lets = [P[s][k] + (P[5][k] if s == 4 else 0) for k in range(6)]
        out[s] = [n[s] * (1 - k / L) for k in np.cumsum(lets)]
    return out


def rung_survival(c, rv, pl):
    """Kaplan-Meier on time since the main duty was accepted, cases accepted from 1 April 2018,
    by recorded need, read at each Tenter House household's elapsed time"""
    acc = c[(c["decision"] == "Main duty accepted") & c["decision_date"].notna()
            & (c["decision_date"] >= pd.Timestamp("2018-04-01"))].copy()
    end = acc["closed_date"].where(acc["closed_date"].notna() & (acc["closed_date"] <= ASOF), ASOF)
    acc["dur"] = (end - acc["decision_date"]).dt.days.values
    acc["ev"] = (acc["closed_date"].notna() & (acc["closed_date"] <= ASOF)).values
    acc["need"] = np.minimum(recorded(c, rv, ASOF).reindex(acc["case_ref"]).values, 4)
    th = tenter_house(pl)
    out = {}
    for s in SIZES:
        sub = acc[acc["need"] == s]
        d = sub["dur"].values
        e = sub["ev"].values
        ts = np.unique(d)
        S, at, Ss = 1.0, len(d), []
        for t in ts:
            m = d == t
            k = (m & e).sum()
            if k:
                S *= 1 - k / at
            at -= m.sum()
            Ss.append(S)
        Ss = np.array(Ss)

        def f(x):
            j = np.searchsorted(ts, x, "right") - 1
            return np.where(j < 0, 1.0, Ss[np.clip(j, 0, None)])
        t0 = acc[acc["case_ref"].isin(th) & (acc["need"] == s)]
        el = (ASOF - t0["decision_date"]).dt.days.values
        base = np.maximum(f(el), 1e-12)
        out[s] = [float((f(el + (me - ASOF).days) / base).sum()) for me in MONTH_ENDS]
    return out


def replay(c, rv, lt, need="recorded", hh=None, since=pd.Timestamp("2018-04-01")):
    """Re-run every round from `since` against the list rule: each round's homes of one size go to the
    first households of that size's list on the day of the round. need="recorded" sorts households by
    the need on the case record, need="part3" by Part 3 on the day from the application (open cases
    only, so only rounds whose candidates are all still open can be replayed that way).
    Returns (reproduced, total)."""
    acc = c[c["decision"] == "Main duty accepted"].sort_values(["decision_date", "case_ref"], kind="mergesort")
    acc = acc.reset_index(drop=True)
    far = np.datetime64("2100-01-01")
    dec = acc["decision_date"].values.astype("datetime64[D]")
    clo = acc["closed_date"].values.astype("datetime64[D]")
    clo = np.where(np.isnat(clo), far, clo)
    refs = acc["case_ref"].values
    pos = {r: k for k, r in enumerate(refs)}
    taken = np.zeros(len(acc), bool)
    for x in lt.loc[lt["offer_date"] < since, "case_ref"]:
        if x in pos:
            taken[pos[x]] = True
    need0 = acc["need0"].fillna(0).astype(int).values
    rvs = rv[rv["case_ref"].isin(pos)].sort_values("review_date", kind="mergesort")
    r_idx = np.array([pos[x] for x in rvs["case_ref"]], int)
    r_day = rvs["review_date"].values.astype("datetime64[D]")
    r_new = rvs["bedrooms_after"].values.astype(int)
    hits = tot = 0
    for r, grp_r in lt[lt["offer_date"] >= since].groupby("offer_date", sort=True):
        td = np.datetime64(r.date())
        ok = (dec <= td) & (clo > td) & ~taken
        if need == "recorded":
            nd = need0.copy()
            m = r_day <= td
            nd[r_idx[m]] = r_new[m]
        else:
            nd = np.full(len(acc), -1)
            for k in np.flatnonzero(ok):
                if refs[k] in hh:
                    nd[k] = rooms(hh[refs[k]], r)
        for s, grp in grp_r.groupby("bedrooms"):
            cand = np.flatnonzero(ok & (nd == s))[:len(grp)]
            hits += len(set(refs[cand]) & set(grp["case_ref"]))
            tot += len(grp)
        for x in grp_r["case_ref"]:
            if x in pos:
                taken[pos[x]] = True
    return hits, tot
