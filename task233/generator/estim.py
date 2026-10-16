"""task233 estimators, run on the shipped files only: the golden flags (the follow-up's departure carried nonrespondent
by nonrespondent on the odds scale), every rung and estimator variant the checks compare it with, and the two asks."""
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import brentq
from scipy.special import expit, logit
from scipy.stats import norm

FIELD = {"F01": "HE", "F02": "FE", "F03": "APP", "F04": "APP", "F05": "EMP", "F06": "NEET", "F07": "NEET"}
BANDS = ["AB1", "AB2", "AB3", "AB4"]
CUT = [(480, "AB1"), (360, "AB2"), (240, "AB3"), (-1, "AB4")]
STATS = {"neet": "NEET", "he": "HE"}
CAUTION, SUPPRESS = 1.0, 3.0
EDITION_2025_BUILD = "7."


def flag(x):
    a = abs(x)
    return "Suppressed" if a >= SUPPRESS else ("Caution" if a >= CAUTION else "Standard")


def margin(x):
    a = abs(x)
    return min(abs(a - CAUTION), abs(a - SUPPRESS))


def CL(p):
    return np.clip(p, 1e-9, 1 - 1e-9)


def load(target):
    f = lambda n: os.path.join(target, n)
    T = dict(
        f26=pd.read_csv(f("leaver_destinations_frame_2026.csv"), dtype=str, keep_default_na=False),
        f25=pd.read_csv(f("leaver_destinations_final_2025.csv"), dtype=str, keep_default_na=False),
        fu=pd.read_csv(f("nonresponse_followup_2025_outcomes.csv"), dtype=str, keep_default_na=False),
        xw=pd.read_csv(f("followup_case_crosswalk_2025.csv"), dtype=str, keep_default_na=False),
        codes=pd.read_csv(f("activity_codes.csv"), dtype=str, keep_default_na=False),
        pts=pd.read_csv(f("state_exam_points_2026.csv"), dtype=str, keep_default_na=False),
        reg=pd.read_excel(f("school_register.xlsx"), sheet_name="Schools", dtype=str),
        dist=pd.read_excel(f("school_register.xlsx"), sheet_name="Districts", dtype=str),
    )
    for k in ("f26", "f25"):
        for c in [c for c in T[k].columns if c.startswith("alloc_")]:
            T[k][c] = pd.to_numeric(T[k][c].replace("", np.nan))
    T["name"] = dict(zip(T["dist"]["district_code"], T["dist"]["district"]))
    return T


def conform(T, map26="district_2026", map25="district_2025"):
    """the 2026 frame by district, the 2025 final file by district, and the follow-up's comparable cases"""
    reg = T["reg"]
    f26 = T["f26"].copy(); f26["district"] = f26["school_code"].map(dict(zip(reg["school_code"], reg[map26])))
    f25 = T["f25"].copy(); f25["district"] = f25["school_code"].map(dict(zip(reg["school_code"], reg[map25])))
    f26["nonresp"] = f26["return_form"] == ""
    f25["nonresp"] = f25["return_form"] == ""
    xw = T["xw"].copy(); xw["leaver_ref"] = "L" + xw["leaver_ref"]
    fu = T["fu"][T["fu"]["outcome_code"] != "F99"].drop_duplicates("case_no")
    cal = fu.merge(xw, on="case_no", how="inner").merge(f25, on="leaver_ref", how="inner")
    cal = cal[cal["nonresp"]].copy()
    cal["found"] = cal["outcome_code"].map(FIELD)
    return f26, f25, cal


# ------------------------------------------------------------------ the departure, by estimator
def _offset(p, a, f=logit, g=expit):
    li = f(CL(p)); return brentq(lambda x: g(li + x).sum() - a.sum(), -10, 10)


def departure(cal, f25):
    E = {}
    for s, dest in STATS.items():
        p = cal["alloc_" + s].to_numpy(float); a = (cal["found"] == dest).to_numpy(float)
        band = cal["attainment_band"].to_numpy(); dd = cal["district"].to_numpy()
        e = dict(gap=a.mean() - p.mean(), rr=a.sum() / p.sum(), delta=_offset(p, a), probit=_offset(p, a, norm.ppf, norm.cdf), n=len(p))
        e["gap_b"] = {b: a[band == b].mean() - p[band == b].mean() for b in BANDS}
        e["rr_b"] = {b: a[band == b].sum() / p[band == b].sum() for b in BANDS}
        e["delta_b"] = {b: _offset(p[band == b], a[band == b]) for b in BANDS}
        e["delta_own"] = {d: _offset(p[dd == d], a[dd == d]) for d in sorted(set(dd))}
        e["gap_db"] = {(d, b): a[(dd == d) & (band == b)].mean() - p[(dd == d) & (band == b)].mean()
                       for d in sorted(set(dd)) for b in BANDS if ((dd == d) & (band == b)).any()}
        lp = logit(CL(p))
        e["cal"] = sm.GLM(a, sm.add_constant(lp), family=sm.families.Binomial()).fit().params
        e["slope"] = float(e["cal"][1])
        e["lin"] = sm.OLS(a - p, sm.add_constant(p)).fit().params
        e["quad"] = sm.OLS(a - p, np.column_stack([np.ones_like(p), p, p * p])).fit().params

        def dev(q):
            q = np.clip(q, 1e-4, 1 - 1e-4); return float(-2 * (a * np.log(q) + (1 - a) * np.log(1 - q)).sum())

        def ll(q):
            q = np.clip(q, 1e-6, 1 - 1e-6); return float((a * np.log(q) + (1 - a) * np.log(1 - q)).sum())
        qg, qr, qo = np.zeros_like(p), np.zeros_like(p), np.zeros_like(p)
        for b in BANDS:
            m = band == b
            qg[m] = p[m] + (a[m].mean() - p[m].mean()); qr[m] = p[m] * a[m].sum() / p[m].sum()
            qo[m] = expit(lp[m] + _offset(p[m], a[m]))
        e["ll"] = {"odds ratio, pooled (1 parameter)": ll(expit(lp + e["delta"])),
                   "points gap, pooled (1)": ll(p + e["gap"]), "ratio of rates, pooled (1)": ll(p * e["rr"]),
                   "points gap, by band (4)": ll(qg), "ratio of rates, by band (4)": ll(qr), "odds ratio, by band (4)": ll(qo)}
        e["dev"] = dict(points=dev(p + e["gap"]), ratio=dev(p * e["rr"]), odds=dev(expit(lp + e["delta"])),
                        linear=dev(p + e["lin"][0] + e["lin"][1] * p),
                        quadratic=dev(p + e["quad"][0] + e["quad"][1] * p + e["quad"][2] * p * p),
                        calibration=dev(expit(e["cal"][0] + e["cal"][1] * lp)))
        # cells: district by band, the odds ratio, the points gap and the ratio of rates each cell shows
        cells = []
        for (d, b), g in e["gap_db"].items():
            m = (dd == d) & (band == b)
            if m.sum() >= 25 and 0 < a[m].sum() < m.sum():
                cells.append(dict(district=d, band=b, n=int(m.sum()), alloc=p[m].mean(), found=a[m].mean(),
                                  gap=g, ratio=a[m].sum() / p[m].sum(), odds_ratio=float(np.exp(_offset(p[m], a[m])))))
        e["cells"] = cells
        # fixed-effects logistic: respondents and comparable followed-up nonrespondents in the followed-up districts
        dists = sorted(set(dd))
        resp = f25[(~f25["nonresp"]) & f25["district"].isin(dists)]
        y = np.concatenate([(resp["destination"] == dest).to_numpy(float), a])
        D = np.concatenate([resp["district"].to_numpy(), dd]); Bn = np.concatenate([resp["attainment_band"].to_numpy(), band])
        U = np.concatenate([np.zeros(len(resp)), np.ones(len(a))])
        X = np.column_stack([*(D == d for d in dists[1:]), *(Bn == b for b in BANDS[1:]), U]).astype(float)
        e["delta_fe"] = sm.GLM(y, sm.add_constant(X), family=sm.families.Binomial()).fit().params[-1]
        num = den = 0.0
        for d in dists:
            for b in BANDS:
                r = (D == d) & (Bn == b)
                A1 = ((U == 1) & r & (y == 1)).sum(); B1 = ((U == 1) & r & (y == 0)).sum()
                C1 = ((U == 0) & r & (y == 1)).sum(); D1 = ((U == 0) & r & (y == 0)).sum(); n = A1 + B1 + C1 + D1
                if n:
                    num += A1 * D1 / n; den += B1 * C1 / n
        e["delta_mh"] = np.log(num / den)
        e["known_rate"] = {d: (resp[resp["district"] == d]["destination"] == dest).mean() for d in dists}
        allresp = f25[~f25["nonresp"]]
        e["known_rate_all"] = (allresp["destination"] == dest).groupby(allresp["district"]).mean().to_dict()
        E[s] = e
    return E


# ------------------------------------------------------------------ shifts, by construction
def shifts(f26, E, s, d, which=None):
    e = E[s]; g = f26[f26["district"] == d]; N = len(g); nr = g[g["nonresp"]]
    p = nr["alloc_" + s].to_numpy(float); band = nr["attainment_band"].to_numpy(); lp = logit(CL(p))
    S = lambda q: (np.clip(q, 0, 1) - p).sum() / N * 100
    out = {}
    out["golden"] = S(expit(lp + e["delta"]))
    out["default"] = len(nr) * e["gap"] / N * 100
    if which == "golden":
        return out
    out["fixed_effects"] = S(expit(lp + e["delta_fe"]))
    out["mantel_haenszel"] = S(expit(lp + e["delta_mh"]))
    out["band_odds"] = S(expit(lp + np.array([e["delta_b"][b] for b in band])))
    out["own_district_odds"] = S(expit(lp + e["delta_own"].get(d, e["delta"])))
    out["calibration"] = S(expit(e["cal"][0] + e["cal"][1] * lp))
    out["band_points"] = sum(e["gap_b"][b] for b in band) / N * 100
    out["clipped_points"] = S(p + e["gap"])
    out["ratio"] = S(p * e["rr"])
    out["band_ratio"] = S(p * np.array([e["rr_b"][b] for b in band]))
    out["linear_points"] = S(p + e["lin"][0] + e["lin"][1] * p)
    out["quadratic_points"] = S(p + e["quad"][0] + e["quad"][1] * p + e["quad"][2] * p * p)
    out["probit"] = S(norm.cdf(norm.ppf(CL(p)) + e["probit"]))
    known = e["known_rate_all"][d]
    an = d if d in e["known_rate"] else min(e["known_rate"], key=lambda t: abs(e["known_rate"][t] - known))
    out["analog"] = sum(e["gap_db"].get((an, b), e["gap_b"][b]) for b in band) / N * 100
    out["analog_district"] = an
    pm = p.mean(); out["district_mean_odds"] = len(nr) * (expit(logit(CL(pm)) + e["delta"]) - pm) / N * 100
    return out


GOLD_VARIANTS = ["golden", "fixed_effects", "mantel_haenszel", "band_odds", "own_district_odds", "calibration"]
WRONG = ["default", "band_points", "analog", "ratio", "linear_points", "clipped_points", "band_ratio", "district_mean_odds"]


# ------------------------------------------------------------------ the forms: activity codes to destinations
def code_maps(T):
    cur = {(r.form, r.activity_code): r.destination for r in T["codes"].itertuples()}
    f25 = T["f25"]; on = f25[(f25["return_form"] == "LDS-2")]
    old = on.groupby("activity_code")["destination"].agg(lambda x: x.mode().iloc[0]).to_dict()
    return cur, {("LDS-2", k): v for k, v in old.items()}


def destinations(g, T, by_build=True):
    cur, old = code_maps(T)
    out = []
    for form, code, build in zip(g["return_form"], g["activity_code"], g["form_build"]):
        if form == "":
            out.append("")
        elif by_build and form == "LDS-2" and build.startswith(EDITION_2025_BUILD):
            out.append(old[(form, code)])
        else:
            out.append(cur[(form, code)])
    return np.array(out)


def released(g, T, by_build=True):
    """the released NEET and HE rates of a group of leavers: returned forms plus allocations, over every leaver"""
    dest = destinations(g, T, by_build)
    N = len(g); nr = g["return_form"] == ""
    return {s: ((dest == STATS[s]).sum() + g.loc[nr, "alloc_" + s].sum()) / N * 100 for s in STATS}


def final_band(T):
    pts = T["pts"].copy(); pts["exam_points"] = pts["exam_points"].astype(int)
    def b(x):
        for lo, lab in CUT:
            if x >= lo:
                return lab
    return dict(zip(pts["leaver_ref"], pts["exam_points"].map(b)))


# ------------------------------------------------------------------ the analysis
def analyse(target):
    T = load(target)
    f26, f25, cal = conform(T)
    E = departure(cal, f25)
    dists = sorted(T["name"])
    cells = []
    for d in dists:
        for s in STATS:
            sh = shifts(f26, E, s, d)
            cells.append(dict(district=d, name=T["name"][d], stat=s, shift=sh["golden"], flag=flag(sh["golden"]),
                              default=sh["default"], default_flag=flag(sh["default"]), all=sh))
    # ask A: each district's released rates
    A = {}
    for d in dists:
        g = f26[f26["district"] == d]
        A[d] = dict(right=released(g, T, True), natural=released(g, T, False), leavers=len(g),
                    nonresp=int(g["nonresp"].sum()))
    # ask B: island-wide by attainment band on the final points
    fb = final_band(T)
    f26["final_band"] = f26["leaver_ref"].map(fb)
    Bq = {}
    for b in BANDS:
        g = f26[f26["final_band"] == b]; g2 = f26[f26["attainment_band"] == b]
        Bq[b] = dict(leavers=len(g), right=released(g, T, True), frame_band=released(g2, T, True),
                     natural=released(g2, T, False), final_natural=released(g, T, False), frame_leavers=len(g2))
    return dict(T=T, f26=f26, f25=f25, cal=cal, E=E, cells=cells, A=A, B=Bq, dists=dists)
