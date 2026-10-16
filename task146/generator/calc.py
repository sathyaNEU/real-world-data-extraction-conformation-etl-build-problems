"""Every figure of the main call and the asks, computed from the shipped files (or, for the analyst test, from the
clean truth through the same code): the golden and its constructions, the default path and every rival, the
precision of the golden, the leave-one-out and panel rejection margins, the twin pairs; then Ask A and Ask B from
their rows.

A view holds, for each region, the weekly initial claims by the claims week's Sunday (revised, and first reported),
the latest week at its advance count, and the monetarily ineligible determinations by quarter (the program
statistics' claims-week months summed)."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

import common as K
import industry as I
import notices as N
import records as R

warnings.filterwarnings("ignore")
REG = K.REGIONS
Q3 = (2026, 3)


class View:
    pass


# ---------------------------------------------------------------------------------------------------- loading
def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def from_pack(target):
    """Read the weekly series (both layouts), the program statistics' determinations (both layouts) and the regions
    file, as a solver would."""
    p = lambda f: os.path.join(target, f)
    code = {r["region_code"]: r["region"] for r in read_csv(p(R.F_REGIONS))}
    V = View()
    V.rev = {r: {} for r in REG}
    V.adv = {r: {} for r in REG}
    V.new = {r: {} for r in REG}
    for row in read_csv(p(R.F_LEGACY)):
        d = dt.datetime.strptime(row["WEEK_COMMENCING"], "%d/%m/%Y").date()
        r = code[row["REGION_CD"]]
        V.rev[r][d] = int(row["INITIAL_CLAIMS"])
        V.new[r][d] = int(row["NEW_CLAIMS"])
    status = {}
    for row in read_csv(p(R.F_CURRENT)):
        d = dt.date.fromisoformat(row["claims_week_start"])
        r = row["region"]
        V.rev[r][d] = int(row["initial_claims"])
        V.adv[r][d] = int(row["first_reported_initial_claims"])
        V.new[r][d] = int(row["new_claims"])
        status[d] = row["count_status"]
    V.latest = max(status)
    assert status[V.latest] == "Advance" and all(v == "Revised" for d, v in status.items() if d != V.latest)
    V.inelig_m, V.new_m = program_months(p(R.F_PROGRAM), code)
    finish(V)
    return V


def program_months(path, code):
    """Monetarily ineligible determinations and new claims by claims-week month and region, from every fiscal-year
    sheet in either layout."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    inel, new = {}, {}
    for ws in wb.worksheets:
        if not ws.title.startswith("FY"):
            continue
        rows = list(ws.iter_rows(values_only=True))
        if rows[0][0] == "UNEMPLOYMENT INSURANCE BOARD":
            block = None
            for i, r in enumerate(rows):
                if r[0] in ("INSUFFICIENT", "NEW CLAIMS"):
                    block = r[0]
                    hdr = rows[i + 1]
                    months = []
                    for h in hdr[1:13]:
                        mon, yy = h.split("-")
                        months.append((2000 + int(yy), [m.upper() for m in
                                                        ("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())].index(mon) + 1))
                    for rr in rows[i + 2:i + 10]:
                        reg = code[rr[0]]
                        for (ym, v) in zip(months, rr[1:13]):
                            if v is not None:
                                (inel if block == "INSUFFICIENT" else new)[(ym, reg)] = int(v)
        else:
            hdr = rows[2]
            ci, cn = hdr.index("Monetarily ineligible"), hdr.index("New claims")
            for r in rows[3:]:
                if isinstance(r[0], dt.datetime) and r[1] in REG:
                    ym = (r[0].year, r[0].month)
                    inel[(ym, r[1])] = int(r[ci])
                    new[(ym, r[1])] = int(r[cn])
    return inel, new


def from_truth(T):
    """The same view from the clean truth: every week revised but the latest, the determinations of the weeks."""
    V = View()
    V.rev = {r: {} for r in REG}
    V.adv = {r: {} for r in REG}
    V.new = {r: {} for r in REG}
    li = T.idx[K.ASOF_LAST_SUNDAY]
    for i in R.ship_index(T):
        s = T.sundays[i]
        for r in REG:
            n, a, ic = R.week_counts(T, r, i)
            V.rev[r][s] = ic
            V.new[r][s] = n
            if s >= K.CURRENT_FIRST_SUNDAY:
                V.adv[r][s] = int(T.advance[r][i])
    V.latest = K.ASOF_LAST_SUNDAY
    V.inelig_m, V.new_m = {}, {}
    for key, idx in R.months_of(T).items():
        for r in REG:
            V.inelig_m[(key, r)] = sum(int(T.adv_inelig[r][i]) if i == li else int(T.inelig[r][i]) for i in idx)
            V.new_m[(key, r)] = sum(R.week_counts(T, r, i)[0] for i in idx)
    finish(V)
    return V


def finish(V):
    V.weeks = sorted(V.rev[REG[0]])
    for r in REG:
        assert sorted(V.rev[r]) == V.weeks
    V.nat = {d: sum(V.rev[r][d] for r in REG) for d in V.weeks}
    V.pool = {}
    for (ym, r), v in V.inelig_m.items():
        q = (ym[0], (ym[1] - 1) // 3 + 1)
        V.pool[(r, q)] = V.pool.get((r, q), 0) + v
    for q in {q for _, q in V.pool}:
        V.pool[("NAT", q)] = sum(V.pool[(r, q)] for r in REG)
    V.months_in_q = {}
    for (ym, r) in V.inelig_m:
        if r == REG[0]:
            q = (ym[0], (ym[1] - 1) // 3 + 1)
            V.months_in_q[q] = V.months_in_q.get(q, 0) + 1
    V.qclaims = {}
    for d in V.weeks:
        q = K.quarter_of(d)
        for r in REG:
            V.qclaims[(r, q)] = V.qclaims.get((r, q), 0) + V.rev[r][d]
            V.qclaims[("NAT", q)] = V.qclaims.get(("NAT", q), 0) + V.rev[r][d]


# ---------------------------------------------------------------------------------------------------- the turns
def turns(V, series="rev"):
    """Every first claims week of a quarter with the closing quarter's determinations complete (three months)."""
    rows = []
    W = V.weeks
    for k in range(3, len(W)):
        d = W[k]
        q = K.quarter_of(d)
        if K.quarter_of(W[k - 1]) == q:
            continue
        pq = K.prev_quarter(q)
        if V.months_in_q.get(pq) != 3:
            continue
        row = dict(sun=d, q=q, qq=q[1], y=q[0])
        for r in REG + ["NAT"]:
            ser = (lambda dd: V.nat[dd]) if r == "NAT" else (lambda dd, r=r: V.rev[r][dd])
            row["nq_" + r] = ser(d)
            if series == "adv":
                if r == "NAT":
                    row["nqa_" + r] = sum(V.adv[x].get(d, V.rev[x][d]) for x in REG)
                else:
                    row["nqa_" + r] = V.adv[r].get(d, V.rev[r][d])
            row["p1_" + r] = ser(W[k - 1])
            row["p2_" + r] = ser(W[k - 2])
            row["p3_" + r] = ser(W[k - 3])
            row["pool_" + r] = V.pool[(r if r != "NAT" else "NAT", pq)]
            row["pqc_" + r] = V.qclaims[(r, pq)]
        rows.append(row)
    return pd.DataFrame(rows)


def dums(df):
    return pd.get_dummies(df["qq"].astype(str), prefix="q", dtype=float)


def fit_region(df, r, kind="diff", robust=False, base="p1"):
    X = dums(df)
    if kind == "ratio":
        y = df["nq_" + r] / df["p1_" + r] - 1
        X["pool"] = df["pool_" + r] / df["p1_" + r]
    else:
        if kind == "adv":
            y = df["nqa_" + r] - df["p1_" + r]
        elif base == "mean3":
            y = df["nq_" + r] - (df["p1_" + r] + df["p2_" + r] + df["p3_" + r]) / 3
        else:
            y = df["nq_" + r] - df["p1_" + r]
        X["pool"] = df["pool_" + r]
    if "q_4" not in X:
        X = sm.add_constant(X, has_constant="add")
    return sm.RLM(y, X, M=sm.robust.norms.HuberT()).fit() if robust else sm.OLS(y, X).fit()


def base_of(V, r, base="p1"):
    ser = (lambda d: V.nat[d]) if r == "NAT" else (lambda d: V.rev[r][d])
    W = V.weeks
    if base == "mean3":
        return (ser(W[-1]) + ser(W[-2]) + ser(W[-3])) / 3.0
    return float(ser(W[-1]))


def predict(V, m, r, kind="diff", base="p1"):
    icpt = m.params["q_4"] if "q_4" in m.params else m.params["const"]
    pool = V.pool[(r, Q3)]
    if kind == "ratio":
        return base_of(V, r) * (1 + icpt) + m.params["pool"] * pool
    return base_of(V, r, base) + icpt + m.params["pool"] * pool


def regional(V, df, **kw):
    fk = {k: v for k, v in kw.items() if k in ("kind", "robust", "base")}
    pk = {k: v for k, v in kw.items() if k in ("kind", "base")}
    return sum(predict(V, fit_region(df, r, **fk), r, **pk) for r in REG)


def national(V, df, **kw):
    fk = {k: v for k, v in kw.items() if k in ("kind", "robust", "base")}
    pk = {k: v for k, v in kw.items() if k in ("kind", "base")}
    return predict(V, fit_region(df, "NAT", **fk), "NAT", **pk)


# ---------------------------------------------------------------------------------------------------- the ladder
def golden_parts(V, D):
    """The golden by region: the base week, the fourth-quarter intercept (the week's movement net of the refiling),
    the refiling (slope times the region's third-quarter determinations), with the delta-method variance of each."""
    out = {}
    for r in REG:
        m = fit_region(D, r)
        P = V.pool[(r, Q3)]
        C = m.cov_params().loc[["q_4", "pool"], ["q_4", "pool"]].values
        v = np.array([1.0, P])
        out[r] = dict(base=base_of(V, r), icpt=float(m.params["q_4"]), slope=float(m.params["pool"]),
                      slope_se=float(m.bse["pool"]), icpt_se=float(m.bse["q_4"]), pool=P,
                      refile=float(m.params["pool"]) * P, var_call=float(v @ C @ v),
                      var_refile=float(m.bse["pool"] ** 2 * P ** 2), var_icpt=float(m.bse["q_4"] ** 2))
    return out


def ladder(V):
    D = turns(V, series="adv")
    out = {}
    q4 = D[D.qq == 4]
    G = {}
    G["all turns"] = regional(V, D)
    G["fourth-quarter turns only"] = regional(V, q4)
    G["third and fourth-quarter turns"] = regional(V, D[D.qq >= 3])
    G["without 2020 and 2021"] = regional(V, D[~D.y.isin([2020, 2021])])
    G["since 2019"] = regional(V, D[D.y >= 2019])
    G["since 2017"] = regional(V, D[D.y >= 2017])
    G["without January turns"] = regional(V, D[D.qq != 1])
    G["the current system's turns"] = regional(V, D[D.sun >= dt.date(2021, 7, 1)])
    G["Huber"] = regional(V, D, robust=True)
    G["ratio form"] = regional(V, D, kind="ratio")
    G["mean of the last three weeks as base"] = regional(V, D, base="mean3")
    cur = D[D.sun >= dt.date(2021, 7, 1)]
    G["advance count as the target (current system)"] = regional(V, cur, kind="adv")
    G["each region through the origin"] = sum(
        base_of(V, r) + float(sm.OLS(D["nq_" + r] - D["p1_" + r], D[["pool_" + r]]).fit().params.iloc[0]) *
        V.pool[(r, Q3)] for r in REG)
    G["each region with one intercept"] = sum(
        predict(V, sm.OLS(D["nq_" + r] - D["p1_" + r], sm.add_constant(pd.DataFrame({"pool": D["pool_" + r]}))).fit(), r)
        for r in REG)
    # holiday-touched turns dropped: Easter Monday or Good Friday in the turn week or the week before
    hol = set(d for y in range(2014, 2028) for d, n in K.holidays(y))

    def touched(s):
        return any((s + dt.timedelta(days=k)) in hol for k in range(-7, 7))
    G["holiday-touched turns dropped"] = regional(V, D[[not touched(s) for s in D.sun]])
    out["golden"] = G
    gold = G["all turns"]
    # one equation for the national step on the eight regional pools (the regional steps discarded)
    X = dums(D)
    for r in REG:
        X["pool_" + r] = D["pool_" + r]
    m = sm.OLS(D["nq_NAT"] - D["p1_NAT"], X).fit()
    Pv = np.array([V.pool[(r, Q3)] for r in REG])
    cols = ["pool_" + r for r in REG]
    out["nat_on_regional_pools"] = (base_of(V, "NAT") + m.params["q_4"] + float(m.params[cols].values @ Pv),
                                    math.sqrt(float(np.r_[1.0, Pv] @ m.cov_params().loc[["q_4"] + cols, ["q_4"] + cols].values
                                                    @ np.r_[1.0, Pv])))
    # rivals
    Rv = {}
    Rv["R0 seasonal factors of the quarter's first claims week on the level of the last four weeks (default)"] = default_path(V)
    Rv["R0b ISO-week seasonal factors on the level of the last four weeks"] = iso_factor(V)
    Rv["R1 last year's week times the last eight weeks' growth on the year"] = yoy(V)
    m = sm.OLS(D["nq_NAT"] - D["p1_NAT"], dums(D)).fit()
    Rv["R2 the step from the week before, one intercept per quarter of the year"] = base_of(V, "NAT") + m.params["q_4"]
    X = dums(D)
    X["pqc"] = D["pqc_NAT"]
    m = sm.OLS(D["nq_NAT"] - D["p1_NAT"], X).fit()
    Rv["R3 the step scaled on the closing quarter's claims"] = base_of(V, "NAT") + m.params["q_4"] + \
        m.params["pqc"] * V.qclaims[("NAT", Q3)]
    tot = 0.0
    for r in REG:
        X = dums(D)
        X["pqc"] = D["pqc_" + r]
        m = sm.OLS(D["nq_" + r] - D["p1_" + r], X).fit()
        tot += base_of(V, r) + m.params["q_4"] + m.params["pqc"] * V.qclaims[(r, Q3)]
    Rv["R3r the step scaled on the closing quarter's claims, region by region"] = tot
    m = sm.OLS(D["nq_NAT"] / D["p1_NAT"] - 1, dums(D)).fit()
    Rv["R2r a quarter-start ratio"] = base_of(V, "NAT") * (1 + m.params["q_4"])
    tot = 0.0
    for r in REG:
        m = sm.OLS(D["nq_" + r] - D["p1_" + r], dums(D)).fit()
        tot += base_of(V, r) + m.params["q_4"]
    Rv["R2g quarter-start terms region by region"] = tot
    N4 = {}
    N4["all turns"] = national(V, D)
    N4["fourth-quarter turns only"] = national(V, q4)
    N4["without 2020 and 2021"] = national(V, D[~D.y.isin([2020, 2021])])
    N4["Huber"] = national(V, D, robust=True)
    N4["ratio form"] = national(V, D, kind="ratio")
    N4["since 2019"] = national(V, D[D.y >= 2019])
    N4["since 2022"] = national(V, D[D.y >= 2022])
    N4["the current system's turns"] = national(V, cur)
    N4["mean of the last three weeks as base"] = national(V, D, base="mean3")
    m = sm.OLS(D["nq_NAT"] - D["p1_NAT"], sm.add_constant(pd.DataFrame({"pool": D["pool_NAT"]}))).fit()
    N4["one intercept"] = base_of(V, "NAT") + m.params["const"] + m.params["pool"] * V.pool[("NAT", Q3)]
    m = sm.OLS(D["nq_NAT"] - D["p1_NAT"], D[["pool_NAT"]]).fit()
    N4["through the origin"] = base_of(V, "NAT") + m.params["pool_NAT"] * V.pool[("NAT", Q3)]
    X = dums(D)
    X["pool"] = D["pool_NAT"]
    X["pqc"] = D["pqc_NAT"]
    m = sm.OLS(D["nq_NAT"] - D["p1_NAT"], X).fit()
    N4["with the closing quarter's claims"] = base_of(V, "NAT") + m.params["q_4"] + m.params["pool"] * \
        V.pool[("NAT", Q3)] + m.params["pqc"] * V.qclaims[("NAT", Q3)]
    # one common share for every region, region intercepts (the panel's pooled slope), summed
    N4["one share for every region, each region's own intercepts"] = common_share(V, D)
    out["national"] = N4
    L = {}
    L4 = D.tail(4)
    L["the last four turns' step per refused claim"] = base_of(V, "NAT") + \
        float((L4["nq_NAT"] - L4["p1_NAT"]).sum() / L4["pool_NAT"].sum()) * V.pool[("NAT", Q3)]
    L1 = D.tail(1)
    L["the last turn's step per refused claim"] = base_of(V, "NAT") + \
        float((L1["nq_NAT"] - L1["p1_NAT"]).iloc[0] / L1["pool_NAT"].iloc[0]) * V.pool[("NAT", Q3)]
    ly = D[(D.y == 2025) & (D.qq == 4)]
    L["last October's step per refused claim"] = base_of(V, "NAT") + \
        float((ly["nq_NAT"] - ly["p1_NAT"]).iloc[0] / ly["pool_NAT"].iloc[0]) * V.pool[("NAT", Q3)]
    out["latest"] = L
    out["rivals"] = Rv
    out["gold"] = gold
    out["parts"] = golden_parts(V, D)
    out["D"] = D
    return out


def common_share(V, D):
    """Stacked regions: region-by-quarter intercepts and one slope on the regions' own pools."""
    rows = []
    for _, t in D.iterrows():
        for r in REG:
            rows.append(dict(r=r, qq=t.qq, y=t["nq_" + r] - t["p1_" + r], pool=t["pool_" + r]))
    P = pd.DataFrame(rows)
    X = pd.get_dummies(P.r + "_" + P.qq.astype(str), dtype=float)
    X["pool"] = P.pool
    m = sm.OLS(P.y, X).fit()
    return sum(base_of(V, r) + m.params["%s_4" % r] + m.params["pool"] * V.pool[(r, Q3)] for r in REG)


def factor_frame(V):
    w = pd.DataFrame({"sun": V.weeks, "ic": [V.nat[d] for d in V.weeks]})
    w["q"] = [K.quarter_of(s) for s in w.sun]
    kq = []
    for i in range(len(w)):
        kq.append(0 if i == 0 or w.q[i] != w.q[i - 1] else kq[-1] + 1)
    w["kq"] = kq
    w["ma"] = w.ic.rolling(52, center=True).mean()
    w["ratio"] = w.ic / w.ma
    return w


def default_path(V):
    """Default path steps 2 to 4: factors of each claims week of the quarter, 2022 to 2025, on the level of the last
    four weeks, times the factor of the first claims week of the fourth quarter."""
    w = factor_frame(V)
    w2 = w[(w.sun >= dt.date(2022, 1, 2)) & (w.sun <= dt.date(2025, 12, 28))]
    fac = w2.groupby(["kq", w2.q.map(lambda x: x[1])]).ratio.mean()
    last = w.tail(4)
    lvl = np.mean([row.ic / fac[(row.kq, row.q[1])] for row in last.itertuples()])
    return float(lvl * fac[(0, 4)])


def iso_factor(V):
    w = factor_frame(V)
    w["iso"] = [(s + dt.timedelta(days=6)).isocalendar()[1] for s in w.sun]
    w2 = w[(w.sun >= dt.date(2022, 1, 2)) & (w.sun <= dt.date(2025, 12, 28))]
    fac = w2.groupby("iso").ratio.mean()
    last = w.tail(4)
    lvl = np.mean([row.ic / fac[row.iso] for row in last.itertuples()])
    return float(lvl * fac[(K.TARGET_SUNDAY + dt.timedelta(days=6)).isocalendar()[1]])


def yoy(V):
    W = V.weeks
    ly = dt.date(2025, 10, 5)
    k = W.index(ly)
    g8 = sum(V.nat[d] for d in W[-8:]) / sum(V.nat[d] for d in W[k - 8:k])
    return float(V.nat[ly] * g8)


# ---------------------------------------------------------------------------------------------------- precision
def precision(V, L):
    parts = L["parts"]
    se_call = math.sqrt(sum(p["var_call"] for p in parts.values()))
    se_refile = math.sqrt(sum(p["var_refile"] for p in parts.values()))
    se_icpt = math.sqrt(sum(p["var_icpt"] for p in parts.values()))
    m = fit_region(L["D"], "NAT")
    P = V.pool[("NAT", Q3)]
    se_nat = math.sqrt(float(np.array([1.0, P]) @ m.cov_params().loc[["q_4", "pool"], ["q_4", "pool"]].values @
                             np.array([1.0, P])))
    return dict(se_call=se_call, se_refile=se_refile, se_icpt=se_icpt, se_nat=se_nat)


def components(V, L):
    parts = L["parts"]
    refile = sum(p["refile"] for p in parts.values())
    wci = sum(parts[r]["refile"] for r in ("Western", "Coastal", "Island"))
    without = sum(p["base"] + p["icpt"] for p in parts.values())
    pool = V.pool[("NAT", Q3)]
    pool_wci = sum(V.pool[(r, Q3)] for r in ("Western", "Coastal", "Island"))
    shares = {r: parts[r]["slope"] for r in REG}
    nat_slope = float(fit_region(L["D"], "NAT").params["pool"])
    return dict(call=L["gold"], refile=refile, refile_wci_share=wci / refile, without=without, pool=pool,
                pool_wci=pool_wci, pool_wci_share=pool_wci / pool, shares=shares, nat_slope=nat_slope,
                nat_refile=nat_slope * pool, base=base_of(V, "NAT"))


def usual_mix(V, L):
    D = L["D"]
    hi = (D["pool_Western"] + D["pool_Coastal"] + D["pool_Island"]) / D["pool_NAT"]
    pools = D["pool_NAT"]
    return dict(median_share=float(hi.median()), mean_share=float(hi.mean()), max_share=float(hi.max()),
                median_pool=float(pools.median()), mean_pool=float(pools.mean()), hi=hi)


def loo(V, D):
    """Leave-one-out errors of the national step at each turn: the regional build summed, the national pool, the
    closing quarter's claims, a quarter-start term alone."""
    errs = {k: [] for k in ("regional", "pool", "claims", "term")}
    for k in range(len(D)):
        tr = D.drop(index=D.index[k])
        te = D.iloc[[k]]
        qq = int(te.qq.iloc[0])
        y = float(te["nq_NAT"].iloc[0] - te["p1_NAT"].iloc[0])
        p = 0.0
        for r in REG:
            m = fit_region(tr, r)
            p += m.params["q_%d" % qq] + m.params["pool"] * float(te["pool_" + r].iloc[0])
        errs["regional"].append(y - p)
        for name, col in (("pool", "pool_NAT"), ("claims", "pqc_NAT"), ("term", None)):
            X = dums(tr)
            if col:
                X["v"] = tr[col]
            m = sm.OLS(tr["nq_NAT"] - tr["p1_NAT"], X).fit()
            p = m.params["q_%d" % qq] + (m.params["v"] * float(te[col].iloc[0]) if col else 0.0)
            errs[name].append(y - p)
    return {k: np.array(v) for k, v in errs.items()}


def panel(V, D):
    """Each region's step at each turn: region-by-quarter intercepts with one slope against a slope per region; the
    F test and the leave-one-turn-out root mean square error per region and turn."""
    rows = []
    for k, (_, t) in enumerate(D.iterrows()):
        for r in REG:
            rows.append(dict(turn=k, r=r, qq=t.qq, y=t["nq_" + r] - t["p1_" + r], pool=t["pool_" + r]))
    P = pd.DataFrame(rows)

    def design(df, common):
        X = pd.get_dummies(df.r + "_" + df.qq.astype(str), dtype=float)
        if common:
            X["pool"] = df.pool
        else:
            for r in REG:
                X["pool_" + r] = df.pool * (df.r == r)
        return X
    out = {}
    for common in (True, False):
        e = []
        for tid in P.turn.unique():
            tr, te = P[P.turn != tid], P[P.turn == tid]
            Xtr = design(tr, common)
            Xte = design(te, common).reindex(columns=Xtr.columns, fill_value=0.0)
            e.extend(list(te.y - sm.OLS(tr.y, Xtr).fit().predict(Xte)))
        out["rmse_common" if common else "rmse_regional"] = float(np.sqrt(np.mean(np.square(e))))
    mc, mr = sm.OLS(P.y, design(P, True)).fit(), sm.OLS(P.y, design(P, False)).fit()
    out["F"] = float(((mc.ssr - mr.ssr) / 7) / (mr.ssr / mr.df_resid))
    out["df"] = (7, int(mr.df_resid))
    return out


def twins(V, D):
    """Pairs of turns whose national pools are within 5 per cent while the share of the pool in Western, Coastal and
    Island differs by 0.12 or more, outside 2020 and 2021."""
    D = D.reset_index(drop=True).copy()
    D["step"] = D.nq_NAT - D.p1_NAT
    D["hi"] = (D.pool_Western + D.pool_Coastal + D.pool_Island) / D.pool_NAT
    out = []
    for a in range(len(D)):
        for b in range(a + 1, len(D)):
            A, B = D.loc[a], D.loc[b]
            if A.y in (2020, 2021) or B.y in (2020, 2021):
                continue
            if abs(A.pool_NAT / B.pool_NAT - 1) < 0.05 and abs(A.hi - B.hi) >= 0.12:
                out.append(dict(a=A.sun, b=B.sun, pool_a=A.pool_NAT, pool_b=B.pool_NAT, hi_a=A.hi, hi_b=B.hi,
                                step_a=A.step, step_b=B.step))
    out.sort(key=lambda x: -abs(x["hi_a"] - x["hi_b"]))
    return out


# ---------------------------------------------------------------------------------------------------- the asks
def ask_a_rows(target):
    import openpyxl
    p = lambda f: os.path.join(target, f)
    portal = read_csv(p(R.F_PORTAL))
    wb = openpyxl.load_workbook(p(R.F_REGISTER), data_only=True)
    ws = wb["Notices"]
    rows = list(ws.iter_rows(values_only=True))
    hi = [i for i, r in enumerate(rows) if r and r[0] == "ES ref"][0]
    hdr = rows[hi]
    register = [dict(zip(hdr, r)) for r in rows[hi + 1:] if r and r[0]]
    notes = read_csv(p(R.F_CASES))
    regions = read_csv(p(R.F_REGIONS))
    town_region = {r["locality"]: r["region"] for r in regions}
    code_region = {r["region_code"]: r["region"] for r in regions}
    return portal, register, notes, town_region, code_region


def ask_a(target, **kw):
    portal, register, notes, town_region, code_region = ask_a_rows(target)
    return N.ask_a(portal, register, notes, town_region, code_region, **kw)


def ask_b(target, **kw):
    rows = read_csv(os.path.join(target, R.F_CUBE))
    return I.ask_b(rows, **kw)


# ---------------------------------------------------------------------------------------------------- the rivals
# built on the two series the call never reads
def ads_rival(V, target):
    """The step at each turn since the job advertisements index begins, regressed on the closing quarter's change in
    the national index (the mean of the quarter's weeks over the mean of the quarter before) with one intercept per
    quarter of the year, carried to the fourth-quarter turn of 2026 on the third quarter's change."""
    import json
    with open(os.path.join(target, R.F_ADS), encoding="utf-8") as fh:
        obs = json.load(fh)["observations"]
    nat = {}
    for o in obs:
        d = dt.date.fromisoformat(o["week_ending"])
        nat.setdefault(d, []).append(o["index"])
    q_mean = {}
    for d, v in nat.items():
        q_mean.setdefault(K.quarter_of(d), []).append(float(np.mean(v)))
    q_mean = {q: float(np.mean(v)) for q, v in q_mean.items()}
    D = turns(V)
    rows = []
    for _, t in D.iterrows():
        pq = K.prev_quarter(t.q)
        ppq = K.prev_quarter(pq)
        if pq in q_mean and ppq in q_mean:
            rows.append(dict(qq=t.qq, y=t.nq_NAT - t.p1_NAT, x=q_mean[pq] / q_mean[ppq] - 1))
    P = pd.DataFrame(rows)
    X = dums(P)
    X["x"] = P.x
    m = sm.OLS(P.y, X).fit()
    x26 = q_mean[Q3] / q_mean[(2026, 2)] - 1
    return base_of(V, "NAT") + m.params["q_4"] + m.params["x"] * x26, len(P), x26
