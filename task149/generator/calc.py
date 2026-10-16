"""Everything the golden and the ladder compute, read from the shipped pack only (the first solver). Returns a dict of
results; `deliver.py` writes the goldens and figures.json from it, `checks.py` asserts on it."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import warnings
import zoneinfo

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

FUNCS = ["RCV", "PUT", "SEL", "LOD"]
DIRECT = set(FUNCS)
CATS = ["AMB", "CHL", "FRZ", "HVB"]
OLD = {"DRYG": "AMB", "PERI": "CHL", "FROZ": "FRZ", "BULK": "HVB"}
ZONES = {"OH": "America/New_York", "IN": "America/Indiana/Indianapolis", "MI": "America/Detroit",
         "PA": "America/New_York", "KY": "America/New_York", "GA": "America/New_York", "NC": "America/New_York",
         "IL": "America/Chicago", "TN": "America/Chicago", "TX": "America/Chicago", "WI": "America/Chicago"}
FY_START = {2021: dt.date(2020, 12, 27), 2022: dt.date(2021, 12, 26), 2023: dt.date(2023, 1, 1),
            2024: dt.date(2023, 12, 31), 2025: dt.date(2024, 12, 29), 2026: dt.date(2025, 12, 28),
            2027: dt.date(2026, 12, 27), 2028: dt.date(2027, 12, 26)}
PERIOD_END = [4, 8, 13, 17, 21, 26, 30, 34, 39, 43, 47, 52]


def fiscal(d):
    for fy in range(2021, 2028):
        if FY_START[fy] <= d < FY_START[fy + 1]:
            wk = (d - FY_START[fy]).days // 7 + 1
            return fy, wk
    return None, None


def period(wk):
    for i, e in enumerate(PERIOD_END):
        if wk <= e:
            return i + 1
    return 12


# ---------------------------------------------------------------------------------------------------- loading
def load(T):
    reg = pd.read_csv(os.path.join(T, "site_register_2026-11-02.csv"), dtype=str)
    num2dc, loc2dc, est2dc, state, prog = {}, {}, {}, {}, []
    for r in reg.itertuples():
        nums = [int(x) for x in str(r.DC_NO).split(";")]
        locs = [x.strip() for x in str(r.WMS_LOC).split(";")]
        dc = nums[0]
        for n in nums:
            num2dc[n] = dc
        for l_ in locs:
            loc2dc[l_] = dc
        est2dc[r.EHS_ESTABLISHMENT] = dc
        state[dc] = r.STATE
        if r.ERGO_PROGRAM_FY27 == "Y":
            prog.append(dc)
    D = dict(reg=reg, num2dc=num2dc, loc2dc=loc2dc, est2dc=est2dc, state=state, prog=sorted(prog))
    # cases
    leg = pd.read_csv(os.path.join(T, "ehs_legacy_case_export_fy21_2024-06-30.csv"), dtype=str, keep_default_na=False)
    with open(os.path.join(T, "ehs_platform_cases_2024-07-01_2026-11-02.json"), encoding="utf-8") as f:
        plat = json.load(f)["cases"]
    migrated = {c["legacy_case_ref"] for c in plat if c["legacy_case_ref"]}
    rows = []
    for r in leg.itertuples():
        d = dt.datetime.strptime(r.INCIDENT_DATE, "%m/%d/%Y").date()
        rows.append(dict(src="legacy", case=r.CASE_NO, dc=est2dc[r.ESTABLISHMENT], date=d,
                         cls=r.CLASSIFICATION, status=r.CASE_STATUS, type=r.OSHA_CASE_TYPE, dept=r.DEPT,
                         ill=r.INJURY_ILLNESS, utc_date=d, migrated_copy=r.CASE_NO in migrated))
    zones = {dc: zoneinfo.ZoneInfo(ZONES[st]) for dc, st in state.items()}
    for c in plat:
        dc = num2dc[int(c["site"]["site_code"][2:])]
        u = dt.datetime.strptime(c["occurred_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        d = u.astimezone(zones[dc]).date()
        cls = "RECORDABLE" if c["classification"]["category"] == "Recordable" else "FIRST AID"
        st = {"Open": "OPEN", "Closed": "CLOSED", "Removed - not work-related": "NOT WORK RELATED"}[c["status"]]
        rows.append(dict(src="platform", case=c["case_id"], dc=dc, date=d, cls=cls, status=st,
                         type=c["classification"]["osha_case_type"] or "", dept=c["person"]["department"],
                         ill=c["classification"]["injury_illness_type"] or "", utc_date=u.date(), migrated_copy=False))
    ALL = pd.DataFrame(rows)
    D["cases_all"] = ALL
    D["cases"] = case_frame(ALL)
    D["plat"] = plat
    D["migrated"] = migrated
    # hours
    H = pd.read_csv(os.path.join(T, "wfm_hours_by_dept_week_fy21_fy26.csv"))
    H["dc"] = H.DC_NO.map(num2dc)
    H["hrs"] = H.REG_HRS + H.OT_HRS + H.AGY_HRS
    H["dir"] = np.where(H.DEPT.isin(DIRECT), H.hrs, 0.0)
    D["wfm"] = H
    # throughput
    M = pq.read_table(os.path.join(T, "wms_cases_shipped_by_category_week.parquet")).to_pandas()
    M["dc"] = M.loc_code.map(loc2dc)
    M["cat"] = M.category_code.map(lambda x: OLD.get(x, x))
    D["wms"] = M
    # standards
    mins = pd.read_excel(os.path.join(T, "ie_engineered_labor_standards.xlsx"), sheet_name="Minutes per case", header=3)
    mins = mins[mins.Function.isin(FUNCS)].set_index("Function")[CATS].astype(float)
    fac = pd.read_excel(os.path.join(T, "ie_engineered_labor_standards.xlsx"), sheet_name="Site factors")
    fac["dc"] = fac.DC_NO.map(num2dc)
    fac["from"] = pd.to_datetime(fac.EFFECTIVE_FROM).dt.date
    fac["to"] = pd.to_datetime(fac.EFFECTIVE_TO).dt.date
    D["mins"], D["fac"] = mins, fac
    # plan
    pv = pd.read_excel(os.path.join(T, "fy2027_operating_plan_v3.xlsx"), sheet_name="Volume")
    ph = pd.read_excel(os.path.join(T, "fy2027_operating_plan_v3.xlsx"), sheet_name="Labor hours")
    pv["dc"] = pv.DC_NO.map(num2dc)
    ph["dc"] = ph.DC_NO.map(num2dc)
    D["plan_vol"], D["plan_hrs"] = pv, ph
    return D


_FAC = {}


def case_frame(ALL, date_col="date", keep_migrated_copies=False, keep_removed=False):
    """The case list the history reads: each migrated case once (the platform's copy), fiscal year and week of the date
    of injury, recordable flag (first aid out, removed cases out)."""
    CS = ALL if keep_migrated_copies else ALL[~ALL.migrated_copy]
    CS = CS.copy()
    CS["date"] = CS[date_col]
    fw = [fiscal(d) for d in CS.date]
    CS["fy"] = [a for a, b in fw]
    CS["wk"] = [b for a, b in fw]
    CS["rec"] = (CS.cls == "RECORDABLE") & ((CS.status != "NOT WORK RELATED") | keep_removed)
    return CS.reset_index(drop=True)




def factor_at(fac, dc, func, d):
    """The site factor in force for a DC and function on a date (the standards' effective dates)."""
    key = (id(fac), len(fac), float(fac.FACTOR.sum()))
    if key not in _FAC:
        tab = {}
        for dc_, fn, a, b, f in zip(fac.dc, fac.FUNCTION, fac["from"], fac["to"], fac.FACTOR):
            tab.setdefault((dc_, fn), []).append((a, None if pd.isna(b) else b, float(f)))
        _FAC.clear()
        _FAC[key] = tab
    hits = [f for a, b, f in _FAC[key][(dc, func)] if a <= d and (b is None or b >= d)]
    return hits[0]


def weekly(D):
    """DC x fiscal week: recordables, hours, direct hours, cases by category, standard hours."""
    CS = D["cases"]
    rec = CS[CS.rec].groupby(["dc", "fy", "wk"]).size().rename("inj")
    H = D["wfm"].groupby(["dc", "FISCAL_YEAR", "FISCAL_WEEK"]).agg(hours=("hrs", "sum"), direct=("dir", "sum"))
    H.index.names = ["dc", "fy", "wk"]
    M = D["wms"].pivot_table(index=["dc", "fiscal_year", "fiscal_week"], columns="cat", values="cases_shipped",
                             aggfunc="sum").fillna(0)
    M.index.names = ["dc", "fy", "wk"]
    X = H.join(M).join(rec).fillna({"inj": 0})
    X = X.reset_index()
    mins, fac = D["mins"], D["fac"]
    earned = np.zeros(len(X))
    cache = {}
    for i, r in enumerate(X.itertuples()):
        d = FY_START[r.fy] + dt.timedelta(days=7 * (r.wk - 1))
        key = (r.dc, d)
        fp = factor_at(fac, r.dc, "PUT", d)
        fs = factor_at(fac, r.dc, "SEL", d)
        e = 0.0
        for c in CATS:
            n = getattr(r, c)
            e += n * (mins.loc["RCV", c] + mins.loc["LOD", c] + mins.loc["PUT", c] * fp + mins.loc["SEL", c] * fs)
        earned[i] = e / 60.0
    X["earned"] = earned
    X["cases"] = X[CATS].sum(axis=1)
    X["per"] = X.wk.map(period)
    X["pace"] = X.earned / X.direct
    return X


def plan_frame(D):
    pv, ph, mins, fac = D["plan_vol"], D["plan_hrs"], D["mins"], D["fac"]
    V = pv.pivot_table(index=["dc", "PERIOD"], columns="CATEGORY", values="CASES", aggfunc="sum")
    P = ph.groupby(["dc", "PERIOD"]).agg(direct=("DIRECT_HOURS", "sum"), indirect=("INDIRECT_HOURS", "sum")).join(V)
    P = P.reset_index().rename(columns={"PERIOD": "per"})
    d0 = FY_START[2027]
    earned = []
    for r in P.itertuples():
        fp = factor_at(fac, r.dc, "PUT", d0)
        fs = factor_at(fac, r.dc, "SEL", d0)
        e = sum(getattr(r, c) * (mins.loc["RCV", c] + mins.loc["LOD", c] + mins.loc["PUT", c] * fp + mins.loc["SEL", c] * fs)
                for c in CATS)
        earned.append(e / 60.0)
    P["earned"] = earned
    P["hours"] = P.direct + P.indirect
    P["cases"] = P[CATS].sum(axis=1)
    P["pace"] = P.earned / P.direct
    P["weeks"] = [4 if p % 3 else 5 for p in P.per]
    return P


def period_frame(X):
    G = X.groupby(["dc", "fy", "per"], as_index=False).agg(inj=("inj", "sum"), hours=("hours", "sum"),
                                                          direct=("direct", "sum"), earned=("earned", "sum"),
                                                          cases=("cases", "sum"), HVB=("HVB", "sum"))
    G["pace"] = G.earned / G.direct
    return G


def golden_of(D, X=None, P=None):
    """The golden's construction on a (possibly modified) set of loaded inputs: Poisson on DC-periods with a DC effect,
    log pace against standard, offset log hours; summed over the programme DCs' FY2027 plan periods."""
    X = weekly(D) if X is None else X
    P = plan_frame(D) if P is None else P
    PP = P[P.dc.isin(D["prog"])]
    G = period_frame(X[X.direct > 0])
    G = G[(G.earned > 0) & (G.hours > 0)].copy()
    G["lpace"] = np.log(G.pace)
    new = pd.DataFrame({"dc": PP.dc.values, "lpace": np.log(PP.pace.values), "hours": PP.hours.values})
    m = fit("inj ~ C(dc) + lpace", G, "hours")
    return float(np.sum(m.predict(new, offset=np.log(new.hours))))


def fit(formula, data, off=None, fam=None):
    return smf.glm(formula, data=data, family=fam or sm.families.Poisson(),
                   offset=(np.log(data[off]) if off else None)).fit()


def run(T):
    D = load(T)
    X = weekly(D)
    P = plan_frame(D)
    prog = D["prog"]
    PP = P[P.dc.isin(prog)].copy()
    R = {"prog": prog}
    # period level history (the plan's grain)
    G = period_frame(X)
    for Z in (X, G):
        Z["lpace"] = np.log(Z.pace)
        Z["luph"] = np.log(Z.cases / Z.direct)
        Z["lh"] = np.log(Z.hours)
        Z["lc"] = np.log(Z.cases)
        Z["le"] = np.log(Z.earned)
        Z["hshare"] = Z.HVB / Z.cases
    new = PP[["dc", "per"]].copy()
    new["lpace"] = np.log(PP.pace.values)
    new["luph"] = np.log((PP.cases / PP.direct).values)
    new["lh"] = np.log(PP.hours.values)
    new["lc"] = np.log(PP.cases.values)
    new["le"] = np.log(PP.earned.values)
    new["hshare"] = (PP.HVB / PP.cases).values
    new["pace_lin"] = PP.pace.values
    new["hours"], new["direct"] = PP.hours.values, PP.direct.values
    nwk = PP.weeks.values
    newW = new.copy()
    for c in ("lh", "lc", "le"):
        newW[c] = new[c] - np.log(nwk)
    newW["hours"] = new.hours / nwk
    newW["direct"] = new.direct / nwk

    def pred(m, nd, offc=None):
        return float(np.sum(m.predict(nd, offset=(np.log(nd[offc]) if offc else None))))

    # the golden: Poisson on DC-periods, a DC effect, log pace, offset log hours, every DC, FY2021 to FY2026 wk 44
    mg = fit("inj ~ C(dc) + lpace", G, "hours")
    R["golden"] = pred(mg, new, "hours")
    R["gamma"], R["gamma_se"] = float(mg.params["lpace"]), float(mg.bse["lpace"])
    gold_by = mg.predict(new, offset=np.log(new.hours))
    R["golden_by_dc"] = {int(k): float(v) for k, v in pd.Series(gold_by.values, index=new.dc.values).groupby(level=0).sum().items()}
    # variants
    V = {}
    V["weekly fit"] = float(np.sum(fit("inj ~ C(dc) + lpace", X[X.hours > 0], "hours").predict(newW, offset=np.log(newW.hours)) * nwk))
    V["negative binomial"] = pred(fit("inj ~ C(dc) + lpace", G, "hours", sm.families.NegativeBinomial(alpha=0.02)), new, "hours")
    V["direct-hours offset"] = pred(fit("inj ~ C(dc) + lpace", G, "direct"), new, "direct")
    V["fiscal-period effects"] = pred(fit("inj ~ C(dc) + C(per) + lpace", G, "hours"), new, "hours")
    ny = new.copy()
    ny["fy"] = 2026
    V["fiscal-year effects at FY2026"] = pred(fit("inj ~ C(dc) + C(fy) + lpace", G, "hours"), ny, "hours")
    V["free log hours and log standard hours"] = pred(fit("inj ~ C(dc) + lh + le", G), new)
    G["pace_lin"] = G.pace
    V["exponential in pace"] = pred(fit("inj ~ C(dc) + pace_lin", G, "hours"), new, "hours")
    for y0 in (2022, 2023, 2024):
        V["from FY%d" % y0] = pred(fit("inj ~ C(dc) + lpace", G[G.fy >= y0], "hours"), new, "hours")
    V["programme DCs only"] = pred(fit("inj ~ C(dc) + lpace", G[G.dc.isin(prog)], "hours"), new, "hours")
    l12 = X[((X.fy == 2025) & (X.wk >= 45)) | (X.fy == 2026)]
    g12 = l12.groupby("dc")
    rate_h = g12.inj.sum() / g12.hours.sum()
    pace12 = g12.earned.sum() / g12.direct.sum()
    pplan = PP.groupby("dc").earned.sum() / PP.groupby("dc").direct.sum()
    V["latest twelve months' rate x fitted pace uplift"] = float(sum(
        r.hours * rate_h[r.dc] * (r.pace / pace12[r.dc]) ** R["gamma"] for r in PP.itertuples()))
    R["variants"] = V
    # rungs
    L = {}
    L["R0 latest twelve months' rate per hour x planned hours"] = float(np.sum(PP.hours.values * rate_h.loc[PP.dc].values))
    ga = X.groupby("dc")
    L["R0a every year's rate per hour"] = float(np.sum(PP.hours.values * (ga.inj.sum() / ga.hours.sum()).loc[PP.dc].values))
    sp = X.groupby(["dc", "per"]).apply(lambda z: z.inj.sum() / z.hours.sum())
    L["R0s each fiscal period's rate"] = float(sum(r.hours * sp.loc[(r.dc, r.per)] for r in PP.itertuples()))
    L["R1c rate per case shipped"] = float(np.sum(PP.cases.values * (g12.inj.sum() / g12.cases.sum()).loc[PP.dc].values))
    L["R1e rate per standard hour"] = float(np.sum(PP.earned.values * (g12.inj.sum() / g12.earned.sum()).loc[PP.dc].values))
    L["R2h hours elasticity"] = pred(fit("inj ~ C(dc) + lh", G), new)
    mu = fit("inj ~ C(dc) + luph", G, "hours")
    L["R2u cases per hour within DCs"] = pred(mu, new, "hours")
    L["R2c free log hours and log cases"] = pred(fit("inj ~ C(dc) + lh + lc", G), new)
    mp = fit("inj ~ lpace", G, "hours")
    L["R2p pace pooled across DCs"] = pred(mp, new, "hours")
    L["R2s heavy-freight share within DCs"] = pred(fit("inj ~ C(dc) + hshare", G, "hours"), new, "hours")
    tr_ = X[X.fy <= 2025]
    R["rungs"] = L
    R["gamma_pooled"] = float(mp.params["lpace"])
    R["uph_coef"] = float(mu.params["luph"])
    # the plan's pace and the latest twelve months' at the programme DCs
    lp = l12[l12.dc.isin(prog)]
    R["pace_plan"] = float(PP.earned.sum() / PP.direct.sum())
    R["pace_l12"] = float(lp.earned.sum() / lp.direct.sum())
    R["pace_ratio_by_dc"] = {int(d): float(pplan[d] / pace12[d]) for d in prog}
    R["hours_ratio"] = float(PP.hours.sum() / lp.hours.sum())
    R["cases_ratio"] = float(PP.cases.sum() / lp.cases.sum())
    R["earned_ratio"] = float(PP.earned.sum() / lp.earned.sum())
    R["uph_ratio"] = float((PP.cases.sum() / PP.direct.sum()) / (lp.cases.sum() / lp.direct.sum()))
    R["l12_recordables_prog"] = int(lp.inj.sum())
    R["l12_rate_prog"] = float(lp.inj.sum() * 200000 / lp.hours.sum())
    R["rate_uplift"] = float((R["pace_plan"] / R["pace_l12"]) ** R["gamma"])
    # the golden's standard error: parametric draws of the DC effects and the response
    rng = np.random.default_rng(149)
    draws = rng.multivariate_normal(mg.params.values, mg.cov_params().values, 400)
    names = list(mg.params.index)
    Xn = np.zeros((len(new), len(names)))
    for i, r in enumerate(new.itertuples()):
        Xn[i, names.index("Intercept")] = 1
        k = "C(dc)[T.%d]" % r.dc
        if k in names:
            Xn[i, names.index(k)] = 1
        Xn[i, names.index("lpace")] = r.lpace
    vals = np.exp(draws @ Xn.T + np.log(new.hours.values)).sum(axis=1)
    R["golden_sigma"] = float(vals.std())
    # back-test: fit on FY2021 to FY2024, predict FY2025 and FY2026 to week 44 at each DC's actual hours
    tr = G[G.fy <= 2024]
    te = G[G.fy >= 2025].copy()
    mb = fit("inj ~ C(dc) + lpace", tr, "hours")
    te["p_pace"] = mb.predict(te, offset=np.log(te.hours))
    x24 = X[X.fy == 2024].groupby("dc")
    te["p_rate"] = te.hours * (x24.inj.sum() / x24.hours.sum()).loc[te.dc].values
    xa = X[X.fy <= 2024].groupby("dc")
    te["p_rate_all"] = te.hours * (xa.inj.sum() / xa.hours.sum()).loc[te.dc].values
    te["p_earn"] = te.earned * (x24.inj.sum() / x24.earned.sum()).loc[te.dc].values
    te["p_uph"] = fit("inj ~ C(dc) + luph", tr, "hours").predict(te, offset=np.log(te.hours))
    te["p_hours_el"] = fit("inj ~ C(dc) + lh", tr).predict(te)
    te["p_hours_cases"] = fit("inj ~ C(dc) + lh + lc", tr).predict(te)
    te["p_pooled"] = fit("inj ~ lpace", tr, "hours").predict(te, offset=np.log(te.hours))
    te["p_hshare"] = fit("inj ~ C(dc) + hshare", tr, "hours").predict(te, offset=np.log(te.hours))
    te["p_case"] = te.cases * (x24.inj.sum() / x24.cases.sum()).loc[te.dc].values
    sp24 = X[X.fy <= 2024].groupby(["dc", "per"]).apply(lambda z: z.inj.sum() / z.hours.sum())
    te["p_seasonal"] = [h_ * sp24.loc[(d_, p_)] for h_, d_, p_ in zip(te.hours, te.dc, te.per)]
    cols = ["p_pace", "p_rate", "p_rate_all", "p_seasonal", "p_case", "p_earn", "p_hours_el", "p_uph", "p_hours_cases",
            "p_pooled", "p_hshare"]
    bt = te.groupby("dc")[["inj"] + cols].sum()
    p24 = x24.earned.sum() / x24.direct.sum()
    x2526 = X[X.fy >= 2025].groupby("dc")
    bt["dpace"] = (x2526.earned.sum() / x2526.direct.sum() / p24).loc[bt.index]
    bt["dwork"] = ((x2526.earned.sum() / x2526.cases.sum()) / (x24.earned.sum() / x24.cases.sum())).loc[bt.index]
    big = (bt.dpace - 1).abs() > 0.04
    mixed = (bt.dwork - 1).abs() > 0.03
    B = {}
    for c in cols:
        err = (bt[c] - bt.inj) / bt.inj
        B[c] = dict(mape=float(100 * err.abs().mean()), bias=float(100 * err.mean()), n_big=int(big.sum()),
                    mape_big=float(100 * err[big].abs().mean()), corr=float(np.corrcoef(err, bt.dpace)[0, 1]),
                    n_mixed=int(mixed.sum()), mape_mixed=float(100 * err[mixed].abs().mean()))
    R["backtest"] = B
    R["backtest_dcs"] = bt
    # separation of pace from the other measures of how hard an hour is worked, in sample (DC-periods, every DC)
    S = {}
    for nm, f, o in [("pace", "inj ~ C(dc) + lpace", "hours"), ("uph", "inj ~ C(dc) + luph", "hours"),
                     ("pace_uph", "inj ~ C(dc) + lpace + luph", "hours"), ("hshare", "inj ~ C(dc) + hshare", "hours"),
                     ("pace_hshare", "inj ~ C(dc) + lpace + hshare", "hours"), ("dc_only", "inj ~ C(dc)", "hours"),
                     ("hours_el", "inj ~ C(dc) + lh", None), ("hours_cases", "inj ~ C(dc) + lh + lc", None),
                     ("hours_earned", "inj ~ C(dc) + lh + le", None)]:
        m = fit(f, G, o)
        S[nm] = dict(dev=float(m.deviance), aic=float(m.aic),
                     params={k: (float(m.params[k]), float(m.bse[k])) for k in m.params.index
                             if not k.startswith("C(") and k != "Intercept"})
    R["separation"] = S
    # chart: the programme DCs' recordable cases by fiscal year
    R["chart"] = {int(fy): int(X[(X.dc.isin(prog)) & (X.fy == fy)].inj.sum()) for fy in range(2021, 2026)}
    R["askA"] = ask_a(T, D)
    R["askB"] = ask_b(T, D)
    R["X"], R["G"], R["PP"], R["D"] = X, G, PP, D
    return R


# ---------------------------------------------------------------------------------------------------- Ask A
EXTRACT = dt.date(2026, 10, 31)
OPENS = ("AWAY", "RESTRICTED", "TRANSFER")
ORDER = {"TRANSFER OUT": 0, "AWAY": 1, "RESTRICTED": 2, "TRANSFER": 3, "FULL DUTY": 4, "SEPARATED": 5}


def spell_days(tl, first_day, upto=EXTRACT, cap=180):
    """Calendar days away and restricted or transferred on a status timeline [(date, status)], from `first_day`
    through `upto`; each opening status runs to the day before the next status; the total capped."""
    away = restr = 0
    for i, (d, st) in enumerate(tl):
        if st not in OPENS:
            continue
        nxt = tl[i + 1][0] if i + 1 < len(tl) else upto + dt.timedelta(days=1)
        a, b = max(d, first_day), min(nxt - dt.timedelta(days=1), upto)
        n = (b - a).days + 1
        if n <= 0:
            continue
        if st == "AWAY":
            away += n
        else:
            restr += n
    if cap and away + restr > cap:
        away, restr = (cap, 0) if away >= cap else (away, cap - away)
    return away, restr


def _tl(rows):
    return sorted(((r.eff, r.STATUS) for r in rows.itertuples()), key=lambda x: (x[0], ORDER[x[1]]))


def ask_a(T, D):
    log = pd.read_csv(os.path.join(T, "rtw_work_status_log_fy2026.csv"), dtype=str, keep_default_na=False)
    log["eff"] = [dt.date.fromisoformat(x) for x in log.EFFECTIVE_DATE]
    num2dc, prog = D["num2dc"], D["prog"]
    CS = D["cases"]
    pc = CS[(CS.src == "platform") & (CS.cls == "RECORDABLE")].set_index("case")
    plat = {c["case_id"]: c for c in D["plat"]}
    # fiscal 2026 recordable cases to 31 October at the programme DCs (removed cases are off the log)
    fy = pc[(pc.fy == 2026) & (pc.date <= EXTRACT) & (pc.status != "NOT WORK RELATED") & pc.dc.isin(prog)]
    by_case = {k: g for k, g in log[log.EHS_CASE_NO != ""].groupby("EHS_CASE_NO")}
    conts = log[log.EHS_CASE_NO == ""]
    cont_by = {(r.ASSOCIATE_NO, r.eff): r.RTW_CASE_ID for r in conts.itertuples() if r.STATUS == "RESTRICTED"}
    cont_files = {k: g for k, g in conts.groupby("RTW_CASE_ID")}
    gold = {d: 0 for d in prog}
    stop_case = {d: 0 for d in prog}
    stop_plat = {d: 0 for d in prog}
    over = {d: 0 for d in prog}
    nocap = {d: 0 for d in prog}
    sep_ignored = {d: 0 for d in prog}
    detail = []
    n_cont = {d: 0 for d in prog}
    for cid, c in fy.iterrows():
        dc = c.dc
        o = plat[cid]["osha_log"] or {}
        stop_plat[dc] += int(o.get("days_away_from_work") or 0) + int(o.get("days_job_transfer_restriction") or 0)
        if cid not in by_case:
            detail.append((cid, dc, 0, 0))
            continue
        g = by_case[cid]
        first = c.date + dt.timedelta(days=1)
        tl0 = _tl(g)
        tl = list(tl0)
        cont_part, to = [], None
        for d_, st in tl0:
            if st == "TRANSFER OUT":
                rid2 = cont_by.get((g.ASSOCIATE_NO.iloc[0], d_))
                if rid2:
                    cont_part = _tl(cont_files[rid2])
                    tl = [x for x in tl0 if x[0] <= d_] + cont_part
                    to = num2dc[int(cont_files[rid2].HOME_DC.iloc[0])]
                    n_cont[dc] += 1
        a, b = spell_days(tl, first)
        gold[dc] += a + b
        detail.append((cid, dc, a, b))
        a0, b0 = spell_days(tl0, first)
        stop_case[dc] += a0 + b0
        a1, b1 = spell_days(tl, first, cap=None)
        nocap[dc] += a1 + b1
        a2, b2 = spell_days([x for x in tl if x[1] != "SEPARATED"], first)
        sep_ignored[dc] += a2 + b2
        over[dc] += a0 + b0       # the continuation credited to the receiving DC instead
        if cont_part and to in over:
            over[to] += (a + b) - (a0 + b0)
    # the log summed by its own home DC: every file, removed cases included, each file from its own first status
    home = {d: 0 for d in prog}
    for rid, g in log.groupby("RTW_CASE_ID"):
        dc = num2dc[int(g.HOME_DC.iloc[0])]
        tl = _tl(g)
        a, b = spell_days(tl, tl[0][0])
        if dc in home:
            home[dc] += a + b
    # removed cases' spells left in (joined by case number, the platform's status not read)
    rem = {d: 0 for d in prog}
    rm = pc[(pc.fy == 2026) & (pc.date <= EXTRACT) & (pc.status == "NOT WORK RELATED") & pc.dc.isin(prog)]
    for cid, c in rm.iterrows():
        if cid in by_case:
            a, b = spell_days(_tl(by_case[cid]), c.date + dt.timedelta(days=1))
            rem[c.dc] += a + b
    with_removed = {d: gold[d] + rem[d] for d in prog}
    return dict(golden=gold, stop_platform=stop_plat, stop_by_case_no=stop_case, stop_home_dc=home,
                stop_over=over, stop_no_cap=nocap, stop_sep_ignored=sep_ignored, stop_with_removed=with_removed,
                n_continuations=n_cont, n_cases={d: int((fy.dc == d).sum()) for d in prog}, detail=detail)


# ---------------------------------------------------------------------------------------------------- Ask B
KG = 2.20462


def period_dates(p):
    first = PERIOD_END[p - 2] + 1 if p > 1 else 1
    last = min(PERIOD_END[p - 1], 44)
    return FY_START[2026] + dt.timedelta(days=7 * (first - 1)), FY_START[2026] + dt.timedelta(days=7 * last - 1)


def ask_b(T, D):
    loc2dc, prog = D["loc2dc"], D["prog"]
    pk = pq.read_table(os.path.join(T, "wms_sku_picks_fy2026_p01_p11.parquet")).to_pandas()
    pk["dc"] = pk.loc_code.map(loc2dc)
    cur = pd.read_csv(os.path.join(T, "wms_item_master_2026-11-01.csv"), dtype={"SKU": int})
    hist = pd.read_csv(os.path.join(T, "wms_item_master_history.csv"), dtype={"SKU": int}, keep_default_na=False)
    hist["f"] = [dt.date.fromisoformat(x) for x in hist.EFFECTIVE_FROM]
    hist["t"] = [dt.date.fromisoformat(x) if x else None for x in hist.EFFECTIVE_TO]

    def lb(w, src):
        return w * KG if src == "PORTAL" else w

    hv = {}
    for r in hist.itertuples():
        hv.setdefault(r.SKU, []).append((r.f, r.t, float(r.CASE_WEIGHT), r.WEIGHT_SOURCE, int(r.ITEM_VERSION)))
    pdates = {p: period_dates(p) for p in range(1, 12)}

    def in_force(sku, p):
        a, b = pdates[p]
        vs = {(v[4], v[2], v[3]) for v in hv.get(sku, []) if v[0] <= b and (v[1] is None or v[1] >= a)}
        return vs

    curw = {r.SKU: (float(r.CASE_WEIGHT), r.WEIGHT_SOURCE, dt.date.fromisoformat(r.SETUP_DATE)) for r in cur.itertuples()}
    out = {k: {d: 0 for d in prog} for k in ("golden", "stop_pounds", "stop_current", "stop_cracker", "stop_over",
                                             "stop_at_50")}
    amb = 0
    for r in pk.itertuples():
        vs = in_force(r.sku, r.fiscal_period)
        if len(vs) != 1:
            amb += 1
        ver, w, src = sorted(vs)[0]
        n = int(r.cases_picked)
        if lb(w, src) > 50:
            out["golden"][r.dc] += n
        if w > 50:
            out["stop_pounds"][r.dc] += n
        if lb(w, src) >= 50:
            out["stop_at_50"][r.dc] += n
        if r.sku in curw:
            cw, cs, csu = curw[r.sku]
            if lb(cw, cs) > 50:
                out["stop_current"][r.dc] += n
            if cw > 50:
                out["stop_cracker"][r.dc] += n
            if (cw * KG if csu >= dt.date(2025, 3, 3) else cw) > 50:
                out["stop_over"][r.dc] += n
    out["ambiguous_rows"] = amb
    out["unmatched_rows"] = int((~pk.sku.isin(set(curw))).sum())
    out["rows"] = len(pk)
    return out
