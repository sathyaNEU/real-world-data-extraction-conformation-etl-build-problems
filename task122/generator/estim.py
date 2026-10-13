"""task122: the eGFR estimators every route uses, on a long table of central eGFR at scheduled visits.

Input columns: SUBJID, ARM, VISIT, WEEK (nominal), DAY (actual study day), EGFR, SET_ASIDE (True for values after a
patient stopped study drug for good). Baseline is the mean of the screening and day-1 values."""
import numpy as np
import pandas as pd

NOMINAL = {"DAY 1": 0, "WEEK 2": 2, "WEEK 4": 4, "WEEK 8": 8, "WEEK 12": 12, "WEEK 16": 16, "WEEK 20": 20,
           "WEEK 24": 24, "WEEK 32": 32, "WEEK 40": 40, "WEEK 52": 52}
DOSES = ["VMK-4410 5 mg", "VMK-4410 10 mg", "VMK-4410 20 mg", "VMK-4410 40 mg"]
PBO = "Placebo"


def changes(df, keep_set_aside=False):
    """each patient's change from baseline at each on-treatment scheduled visit"""
    base = df[df["VISIT"].isin(["SCREENING", "DAY 1"])].groupby("SUBJID")["EGFR"].mean()
    on = df[df["VISIT"].isin(list(NOMINAL))].copy()
    if not keep_set_aside:
        on = on[~on["SET_ASIDE"]]
    on["BASE"] = on["SUBJID"].map(base)
    on = on[on["BASE"].notna()]
    on["CHG"] = on["EGFR"] - on["BASE"]
    on["W"] = on["VISIT"].map(NOMINAL)
    return on


def arm_visit(chg, by="W"):
    return chg.groupby(["ARM", by])["CHG"].mean().unstack(0)


def diffs(av):
    return {a: av[a] - av[PBO] for a in DOSES}


def line_at(series, start, end=52, at=156, xs=None):
    """the straight line through a difference series over nominal weeks start..end, read at week `at`"""
    s = series[(series.index >= start) & (series.index <= end)].dropna()
    x = np.array(s.index, float) if xs is None else np.array([xs[i] for i in s.index], float)
    b, a = np.polyfit(x / 52.0, s.to_numpy(float), 1)
    return a + b * at / 52.0, b


def routes(df, keep_set_aside=False):
    """every route's 36-month (week-156) difference from placebo by dose"""
    chg = changes(df, keep_set_aside)
    av = arm_visit(chg)
    d = diffs(av)
    out = {}
    for a in DOSES:
        s = d[a]
        r = {"w52": float(s.loc[52])}
        for k in (0, 4, 12, 16, 20, 24, 32):
            r["k%d" % k], r["s%d" % k] = (float(x) for x in line_at(s, k))
        out[a] = r
    return out


def golden(df):
    return {a: v["k24"] for a, v in routes(df).items()}


def pooled_actual(df, start=24, at_days=1092, keep_set_aside=False):
    """each arm's pooled least-squares line of change on actual study time over visits from `start`, read at
    study day `at_days` + 1, as a difference from placebo"""
    chg = changes(df, keep_set_aside)
    chg = chg[chg["W"] >= start]
    out = {}
    for a, g in chg.groupby("ARM"):
        x = (g["DAY"].to_numpy(float) - 1) / 365.25
        b, c = np.polyfit(x, g["CHG"].to_numpy(float), 1)
        out[a] = c + b * at_days / 365.25
    return {a: float(out[a] - out[PBO]) for a in DOSES}


def per_patient(df, start=24, at=156, keep_set_aside=False, min_n=3):
    """each patient's own line over visits from `start`, read at week `at`, averaged by arm, against placebo"""
    chg = changes(df, keep_set_aside)
    chg = chg[chg["W"] >= start]
    vals = {}
    for (a, s), g in chg.groupby(["ARM", "SUBJID"]):
        if len(g) < min_n:
            continue
        b, c = np.polyfit(g["W"].to_numpy(float) / 52.0, g["CHG"].to_numpy(float), 1)
        vals.setdefault(a, []).append(c + b * at / 52.0)
    m = {a: float(np.mean(v)) for a, v in vals.items()}
    return {a: m[a] - m[PBO] for a in DOSES}
