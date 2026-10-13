"""The analysis on the pack as shipped: match Tallyband's respondents to Tarnwick's Data Engineer levels, carry each
report to the benchmark date, read the band points; and every rung and alternative the checks compare."""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import common as K

LEVELS = K.LEVELS


def norm_employer(s):
    s = str(s).casefold().replace(",", " ").replace(".", " ")
    s = re.sub(r"\s+inc\s*$", "", s.strip())
    return re.sub(r"[^a-z0-9]", "", s)


def age_years(d, how="days"):
    if how == "months":
        return np.array([((K.BENCHMARK.year - x.year) * 12 + K.BENCHMARK.month - x.month) / 12.0 for x in d])
    return np.array([(K.BENCHMARK - x).days / 365.25 for x in d])


def map_levels(df, cw, code_col="employer_level", date_col="filed_on", current=False):
    """Each report's employer level code to Tarnwick's level through the crosswalk row in effect on the report's
    date (or, with current, the row in effect today for every report)."""
    c = cw.copy()
    c["key"] = c.employer.map(norm_employer)
    out = pd.Series([None] * len(df), index=df.index, dtype=object)
    keys = df.employer.map(norm_employer)
    by = {}
    for r in c.itertuples():
        by.setdefault((r.key, r.level_code), []).append((r.effective_from, r.effective_to, r.tarnwick_level))
    for i, k, code, d in zip(df.index, keys, df[code_col], df[date_col]):
        if d is None or code is None or (isinstance(code, float) and np.isnan(code)):
            continue
        on = K.BENCHMARK if current else d
        for f, t, lv in by.get((k, code), ()):
            if f <= on and (t is None or on <= t):
                out[i] = lv
    return out


def matched(ex, pr, cw, fam, focus, current=False, us_ft=True, exact_names=False):
    df = ex.merge(pr[["respondent_id", "primary_focus"]], on="respondent_id", how="left")
    if exact_names:
        df = df[df.employer.isin(set(cw.employer))]
    df = df.copy()
    df["level"] = map_levels(df, cw, current=current)
    m = (df.job_family == fam) & (df.primary_focus == focus) & df.level.isin(LEVELS)
    if us_ft:
        m &= (df.country == "US") & (df.employment_type == "full_time")
    return df[m].copy()


def _demean(v, keys, iters=200):
    """v net of every group's mean, for each key array in turn, alternated until it settles (two-way fixed
    effects by alternating projections)."""
    v = np.asarray(v, float).copy()
    for _ in range(iters if len(keys) > 1 else 1):
        for k in keys:
            v = v - pd.Series(v).groupby(k).transform("mean").to_numpy()
    return v


def employer_key(df, typed=False):
    return df.employer.astype(str).to_numpy() if typed else df.employer.map(norm_employer).to_numpy()


def movement(df, how="fe"):
    """The market's movement at a fixed level, a year: the slope of log base pay on filing date. "fe" reads it within
    employers (an intercept for each employer and each level); the cross-section forms read it across every report,
    whoever filed it."""
    y = np.log(df.base_salary_usd.to_numpy(float))
    t = -age_years(df.filed_on)
    lev = df.level.to_numpy()
    if how in ("fe", "fe_typed"):
        emp = employer_key(df, typed=how == "fe_typed")
        yy, tt = _demean(y, [emp, lev]), _demean(t, [emp, lev])
        return float(tt @ yy / (tt @ tt))
    if how == "fe_employer_level":
        el = np.array(["%s|%s" % (a, b) for a, b in zip(employer_key(df), lev)])
        yy, tt = _demean(y, [el]), _demean(t, [el])
        return float(tt @ yy / (tt @ tt))
    if how == "fe_per_level":
        emp = employer_key(df)
        out = {}
        for lv in LEVELS:
            k = lev == lv
            yy, tt = _demean(y[k], [emp[k]]), _demean(t[k], [emp[k]])
            out[lv] = float(tt @ yy / (tt @ tt))
        return out
    if how in ("panel_first_year", "panel_every_year"):
        emp = employer_key(df)
        yr = np.floor(-t).astype(int)                      # 0: the last twelve months ... 2: the first
        seen = pd.DataFrame({"e": emp, "yr": yr}).groupby("e").yr.agg(set)
        keep = {e for e, s_ in seen.items() if (2 in s_ if how == "panel_first_year" else s_ >= {0, 1, 2})}
        k = np.array([e in keep for e in emp])
        X = np.c_[pd.get_dummies(lev[k]).to_numpy(float), t[k]]
        return float(np.linalg.lstsq(X, y[k], rcond=None)[0][-1])
    if how == "pooled":
        X = np.c_[pd.get_dummies(df.level).to_numpy(float), t]
        return float(np.linalg.lstsq(X, y, rcond=None)[0][-1])
    if how == "no_level":
        return float(np.polyfit(t, y, 1)[0])
    if how == "fe_no_level":
        emp = employer_key(df)
        yy, tt = _demean(y, [emp]), _demean(t, [emp])
        return float(tt @ yy / (tt @ tt))
    if how == "per_level":
        return {lv: float(np.polyfit(t[lev == lv], y[lev == lv], 1)[0]) for lv in LEVELS}
    if how == "quarterly_medians":
        q = np.floor(-t * 4).astype(int)
        out = {}
        for lv in LEVELS:
            m = lev == lv
            g = pd.DataFrame({"q": q[m], "y": y[m]}).groupby("q").y.median()
            out[lv] = float(-np.polyfit(g.index.to_numpy(float) / 4.0 + 0.125, g.to_numpy(), 1)[0])
        return out
    if how == "annual_medians":
        yr = np.floor(-t).astype(int)
        out = {}
        for lv in LEVELS:
            m = lev == lv
            g = pd.DataFrame({"yr": yr[m], "y": y[m]}).groupby("yr").y.median()
            out[lv] = float((g.loc[0] - g.loc[2]) / 2.0)
        return out
    if how == "median_regression":
        import statsmodels.api as sm
        X = np.c_[pd.get_dummies(df.level).to_numpy(float), t]
        return float(sm.QuantReg(y, X).fit(q=0.5).params[-1])
    raise ValueError(how)


def carry(df, rate, form="exp", how="days"):
    """Each report carried to the benchmark date at a rate, or at each level's own rate."""
    if not isinstance(rate, dict):
        return aged(df, rate, form, how)
    pay = np.empty(len(df))
    for lv in LEVELS:
        m = (df.level == lv).to_numpy()
        pay[m] = aged(df[m], rate[lv], form, how)
    return pay


def paired_growth(df, cw, same_level=True):
    """The re-reporters' own growth: log change between their previous and current reports, a year."""
    p = df[df.previous_filed_on.notna()].copy()
    p["prev_level"] = map_levels(p, cw, code_col="previous_employer_level", date_col="previous_filed_on")
    if same_level:
        p = p[p.prev_level == p.level]
    gap = np.array([(a - b).days / 365.25 for a, b in zip(p.filed_on, p.previous_filed_on)])
    g = np.log(p.base_salary_usd.to_numpy(float) / p.previous_base_salary_usd.to_numpy(float)) / gap
    return float(np.mean(g)), len(p)


def aged(df, rate, form="exp", how="days"):
    a = age_years(df.filed_on, how)
    b = df.base_salary_usd.to_numpy(float)
    if form == "exp":
        return b * np.exp(rate * a)
    if form == "compound":
        return b * (1.0 + rate) ** a
    if form == "linear":
        return b * (1.0 + rate * a)
    raise ValueError(form)


def points(df, pay, method="linear"):
    out = {}
    for lv in LEVELS:
        v = np.sort(pay[(df.level == lv).to_numpy()])
        out[lv] = {p: float(np.percentile(v, p, method=method)) for p in (25, 50, 75)}
    return out


def to_k(x):
    return int(np.floor(x / 1000.0 + 0.5) * 1000)


def golden(ex, pr, cw, fam, focus):
    df = matched(ex, pr, cw, fam, focus)
    g = movement(df, "fe")
    pts = points(df, aged(df, g))
    return dict(df=df, g=g, points=pts, filed={lv: {p: to_k(v) for p, v in d.items()} for lv, d in pts.items()},
                n={lv: int((df.level == lv).sum()) for lv in LEVELS})


def rungs(ex, pr, cw, fam, focus):
    df = matched(ex, pr, cw, fam, focus)
    g = movement(df, "fe")
    gx = movement(df, "pooled")
    gn = movement(df, "no_level")
    gp, npairs = paired_growth(df, cw, True)
    ga, nall = paired_growth(df, cw, False)
    r0 = ex[(ex.job_family == fam) & (ex.country == "US") & (ex.employment_type == "full_time")]
    r0_mid = {lv: float(np.percentile(r0[r0.tallyband_level == tl].base_salary_usd, 50))
              for lv, tl in zip(LEVELS, ("L2", "L3", "L4", "L5"))}
    return dict(g=g, g_pooled=gx, g_no_level=gn, g_pair=gp, n_pair=npairs, g_all=ga, n_all=nall,
                R0=r0_mid, R1=points(df, df.base_salary_usd.to_numpy(float)),
                R2=points(df, aged(df, gp)), R2_all=points(df, aged(df, ga)), R3=points(df, aged(df, gx)),
                R3_no_level=points(df, aged(df, gn)), R4=points(df, aged(df, g)))


ROMAN_OF = {"1": "I", "2": "II", "3": "III", "4": "IV"}


def zone_on(zones, loc, on):
    for r in zones[zones.work_location == loc].itertuples():
        if r.effective_from <= on and (r.effective_to is None or on <= r.effective_to):
            return int(r.pay_zone)
    return None


def headcount(hr, zones, on=None, zone_from="map", statuses=("active", "leave"), employees_only=True,
              as_of=True):
    """Data Engineers employed on a date: each worker's job record in effect that day (the last record dated on or
    before it), counted once, by level and by the pay zone of their work location that day."""
    on = on or K.BENCHMARK
    h = hr.copy()
    h["_row"] = np.arange(len(h))
    if as_of:
        h = h[[d <= on for d in h.effective_date]]
    cur = h.sort_values(["employee_id", "effective_date", "_row"], kind="mergesort").groupby("employee_id").tail(1)
    cur = cur[cur.job_code.str.startswith("DE") & cur.status.isin(statuses)]
    if employees_only:
        cur = cur[cur.worker_type == "employee"]
    lv = cur.job_code.str[-1].map(ROMAN_OF)
    if zone_from == "map":
        zn = [zone_on(zones, loc, on) for loc in cur.work_location]
    else:
        zn = cur.pay_zone.astype(int).tolist()
    t = pd.DataFrame({"level": lv.to_numpy(), "zone": zn})
    grid = t.groupby(["level", "zone"]).size().unstack(fill_value=0)
    return grid.reindex(index=LEVELS, columns=[1, 2, 3], fill_value=0)


def open_requisitions(req, on=None, end_from="status"):
    """Data Engineer requisitions open on a date: opened on or before it and not yet filled or cancelled, counted once
    per requisition, by level."""
    on = on or K.BENCHMARK
    r = req.drop_duplicates("requisition_id")
    r = r[r.job_code.str.startswith("DE")]
    out = {lv: 0 for lv in LEVELS}
    for x in r.itertuples():
        if x.opened_on > on:
            continue
        if end_from == "status":
            end = x.status_date if x.status in ("filled", "cancelled") else None
        else:                                   # closed_on alone
            end = x.closed_on
        if end is None or end > on:
            out[ROMAN_OF[x.job_code[-1]]] += 1
    return out


DETERMINISM = ("fe_typed", "fe_employer_level", "fe_per_level", "panel_first_year", "panel_every_year",
               "linear_form", "compound_form", "months", "pct_nearest", "pct_lower", "pct_higher", "pct_hazen",
               "pct_weibull", "pct_median_unbiased", "round_first")
LAYER1 = ("names_exact", "keep_nonus_pt", "current_crosswalk", "keep_nonus_only")
CROSS_SECTION = ("pooled", "per_level", "quarterly_medians", "annual_medians", "median_regression", "no_level")


def variants(ex, pr, cw, fam, focus):
    """Every defensible variant of the golden construction (the determinism set), every Layer 1 item mishandled, and
    every cross-section reading of the movement (the rung below), as band points per level."""
    out = {}
    df = matched(ex, pr, cw, fam, focus)
    g = movement(df, "fe")
    out["golden"] = points(df, aged(df, g))
    for how in ("fe_typed", "fe_employer_level", "fe_per_level", "panel_first_year", "panel_every_year"):
        out[how] = points(df, carry(df, movement(df, how)))
    out["linear_form"] = points(df, aged(df, g, form="linear"))
    out["compound_form"] = points(df, aged(df, g, form="compound"))
    out["months"] = points(df, aged(df, g, how="months"))
    for meth in ("nearest", "lower", "higher", "hazen", "weibull", "median_unbiased"):
        out["pct_" + meth] = points(df, aged(df, g), method=meth)
    out["round_first"] = points(df, np.round(aged(df, g)))
    for tag, kw in (("names_exact", dict(exact_names=True)), ("keep_nonus_pt", dict(us_ft=False)),
                    ("current_crosswalk", dict(current=True))):
        d2 = matched(ex, pr, cw, fam, focus, **kw)
        out[tag] = points(d2, aged(d2, movement(d2, "fe")))
    d2 = matched(ex, pr, cw, fam, focus, us_ft=False)
    d2 = d2[d2.employment_type == "full_time"]
    out["keep_nonus_only"] = points(d2, aged(d2, movement(d2, "fe")))
    for how in CROSS_SECTION:
        out["xs_" + how] = points(df, carry(df, movement(df, how)))
    return out
