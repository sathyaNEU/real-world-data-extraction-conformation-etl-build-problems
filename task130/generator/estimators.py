"""The golden reading and every rung of the ladder, computed from the shipped files only."""
import os

import numpy as np
import pandas as pd
import openpyxl

ASOF = pd.Timestamp("2026-09-30")
VACANT = pd.Timestamp("2027-03-31")
SIZES = [1, 2, 3, 4]
MONTH_ENDS = [pd.Timestamp(x) for x in ("2026-10-31", "2026-11-30", "2026-12-31", "2027-01-31",
                                         "2027-02-28", "2027-03-31")]
F = {
    "cases": "homelessness_cases_2026-09-30.csv",
    "placements": "ta_placements_2018-04_2026-09.csv",
    "reviews": "bedroom_need_reviews.csv",
    "lets": "moveon_lets_2018-04_2026-09.csv",
    "plan": "moveon_plan_2026-27.xlsx",
    "prices": "dps_lot2_lot3_price_schedule.xlsx",
}


def load(target):
    p = lambda k: os.path.join(target, F[k])
    c = pd.read_csv(p("cases"), dtype=str, keep_default_na=False)
    pl = pd.read_csv(p("placements"), dtype=str, keep_default_na=False)
    rv = pd.read_csv(p("reviews"), dtype=str, keep_default_na=False)
    lt = pd.read_csv(p("lets"), dtype=str, keep_default_na=False)
    for df, cols in ((c, ["application_date", "decision_date", "closed_date"]),
                     (pl, ["placement_start", "placement_end"]), (rv, ["review_date"]),
                     (lt, ["offer_date", "tenancy_start"])):
        for k in cols:
            df[k] = pd.to_datetime(df[k].replace("", None))
    rv["bedrooms_after"] = rv["bedrooms_after"].astype(int)
    lt["bedrooms"] = lt["bedrooms"].astype(int)
    c["need0"] = pd.to_numeric(c["bedrooms_needed_at_decision"].replace("", None))
    return c, pl, rv, lt


def plan(target, sheet="Revised 14 Sep 2026"):
    ws = openpyxl.load_workbook(os.path.join(target, F["plan"]), data_only=False)[sheet]
    out = {}
    for r in range(5, 9):
        s = ws.cell(row=r, column=1).value
        s = 4 if s == "4+" else int(s)
        out[s] = [int(ws.cell(row=r, column=8 + j).value) for j in range(6)]
    return out


def lot3_2728(target):
    ws = openpyxl.load_workbook(os.path.join(target, F["prices"]))["Rates"]
    out = {}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] == "3":
            out[4 if r[3] == "4+" else int(r[3])] = float(r[5])
    return out


def need_at(c, rv, t):
    """bedroom need of every case on day t: the latest review on or before t, else the decision"""
    n = c.set_index("case_ref")["need0"].copy()
    r = rv[rv["review_date"] <= t].sort_values(["review_date"], kind="mergesort")
    last = r.groupby("case_ref")["bedrooms_after"].last()
    n.loc[last.index] = last.values
    return n


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


def queue_runoff(c, rv, pl, pl_plan, order="decision_date", need="current", members="all", pending_twice=None):
    """month-end households still in Tenter House by bedroom size, the lists ordered by `order`"""
    q = open_main(c, ASOF).copy()
    if members == "ta":
        q = q[q["case_ref"].isin(in_ta(pl))]
    q["need"] = need_at(c, rv, ASOF).loc[q["case_ref"]].values if need == "current" else q["need0"].values
    if order == "ta_start":
        first = pl.groupby("case_ref")["placement_start"].min()
        q["key"] = q["case_ref"].map(first).fillna(q["application_date"])
    elif order == "application":
        q["key"] = q["application_date"]
    else:
        q["key"] = q["decision_date"]
    th = tenter_house(pl)
    out = {}
    for s in SIZES:
        qs = q[q["need"] == s].sort_values(["key", "case_ref"], kind="mergesort")
        if pending_twice is not None:
            gone = set(pending_twice.loc[pending_twice["bedrooms"] == s, "case_ref"])
            qs = qs[~qs["case_ref"].isin(gone)]
        rank = np.arange(1, len(qs) + 1)
        is_th = qs["case_ref"].isin(th).values
        cum = np.cumsum(pl_plan[s])
        out[s] = [int((is_th & (rank > k)).sum()) for k in cum]
    return out


def th_by_need(c, rv, pl):
    n = need_at(c, rv, ASOF)
    th = sorted(tenter_house(pl))
    return {s: int((n.loc[th] == s).sum()) for s in SIZES}


def golden(target):
    c, pl, rv, lt = load(target)
    return queue_runoff(c, rv, pl, plan(target))


def callout(run):
    return {s: run[s][-1] for s in SIZES}


def weekly_cost(units, rates):
    return sum(units[s] * rates[s] for s in SIZES)


# ---------------- the wrong rungs ----------------

def rung_none(c, rv, pl):
    n = th_by_need(c, rv, pl)
    return {s: [n[s]] * 6 for s in SIZES}


def monthly_rate(c, rv, months=12):
    """share of main-duty households leaving each month over the last `months` months, by need"""
    rate = {}
    starts = pd.date_range(ASOF - pd.DateOffset(months=months) + pd.Timedelta(days=1), ASOF, freq="MS")
    tot = {s: [0, 0] for s in SIZES}
    for m in starts:
        me = m + pd.offsets.MonthEnd(0)
        o = open_main(c, m - pd.Timedelta(days=1))
        nd = need_at(c, rv, m).loc[o["case_ref"]].values
        left = (o["closed_date"] <= me).values
        for s in SIZES:
            tot[s][0] += int(((nd == s) & left).sum())
            tot[s][1] += int((nd == s).sum())
    for s in SIZES:
        rate[s] = tot[s][0] / tot[s][1]
    return rate


def rung_rate(c, rv, pl):
    n = th_by_need(c, rv, pl)
    r = monthly_rate(c, rv)
    return {s: [n[s] * (1 - r[s]) ** (k + 1) for k in range(6)] for s in SIZES}


def rung_share(c, rv, pl, pl_plan):
    n = th_by_need(c, rv, pl)
    q = open_main(c, ASOF)
    nd = need_at(c, rv, ASOF).loc[q["case_ref"]]
    out = {}
    for s in SIZES:
        L = (nd == s).sum()
        cum = np.cumsum(pl_plan[s])
        out[s] = [n[s] * (1 - k / L) for k in cum]
    return out


def rung_survival(c, rv, pl):
    """Kaplan-Meier on time since the main duty was accepted, cases accepted from 1 April 2018,
    by bedroom need at the end of the spell, read at each Tenter House household's elapsed time"""
    acc = c[(c["decision"] == "Main duty accepted") & c["decision_date"].notna()
            & (c["decision_date"] >= pd.Timestamp("2018-04-01"))].copy()
    end = acc["closed_date"].where(acc["closed_date"].notna() & (acc["closed_date"] <= ASOF), ASOF)
    acc["dur"] = (end - acc["decision_date"]).dt.days.values
    acc["ev"] = (acc["closed_date"].notna() & (acc["closed_date"] <= ASOF)).values
    nd = need_at(c, rv, ASOF)
    acc["need"] = nd.loc[acc["case_ref"]].values
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


def replay_lets(c, rv, lt, order="decision_date", members="all", need="current", pl=None):
    """Re-run every let since April 2018 against a list rule: the lets of one size starting on one
    day go to the first households of that size's list on that day. Returns (reproduced, total)."""
    started = lt[lt["let_status"] == "Tenancy started"]
    acc = c[c["decision"] == "Main duty accepted"].copy()
    if order == "ta_start":
        first = pl.groupby("case_ref")["placement_start"].min()
        acc["key"] = acc["case_ref"].map(first).fillna(acc["application_date"])
    else:
        acc["key"] = acc[order]
    acc = acc.sort_values(["key", "case_ref"], kind="mergesort").reset_index(drop=True)
    far = np.datetime64("2100-01-01")
    dec = acc["decision_date"].values.astype("datetime64[D]")
    clo = acc["closed_date"].values.astype("datetime64[D]")
    clo = np.where(np.isnat(clo), far, clo)
    need0 = acc["need0"].fillna(0).astype(int).values
    refs = acc["case_ref"].values
    pos = {r: k for k, r in enumerate(refs)}
    rvs = rv[rv["case_ref"].isin(pos)].sort_values("review_date", kind="mergesort")
    r_idx = np.array([pos[x] for x in rvs["case_ref"]], int)
    r_day = rvs["review_date"].values.astype("datetime64[D]")
    r_new = rvs["bedrooms_after"].values.astype(int)
    if members == "ta":
        p_idx = np.array([pos.get(x, -1) for x in pl["case_ref"]])
        p_st = pl["placement_start"].values.astype("datetime64[D]")
        p_en = pl["placement_end"].values.astype("datetime64[D]")
        p_en = np.where(np.isnat(p_en), far, p_en)
        keep = p_idx >= 0
        p_idx, p_st, p_en = p_idx[keep], p_st[keep], p_en[keep]
    taken = np.zeros(len(acc), bool)
    hits = 0
    for (t, s), grp in started.groupby(["tenancy_start", "bedrooms"], sort=True):
        td = np.datetime64(t.date())
        ok = (dec <= td) & (clo >= td) & ~taken
        if members == "ta":
            live = np.zeros(len(acc), bool)
            live[p_idx[(p_st <= td) & (p_en >= td)]] = True
            ok &= live
        nd = need0.copy()
        if need == "current":
            m = r_day <= td
            nd[r_idx[m]] = r_new[m]          # reviews sorted by date, so the last one wins
        cand = np.flatnonzero(ok & (nd == s))[:len(grp)]
        hits += len(set(refs[cand]) & set(grp["case_ref"]))
        for x in grp["case_ref"]:
            if x in pos:
                taken[pos[x]] = True
    return hits, len(started)
