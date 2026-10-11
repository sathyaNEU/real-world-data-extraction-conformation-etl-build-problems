"""The decision analysis over cleaned readings: each bore's September 2026 assessment level (MG-02 2.4), the naive
rungs, and the answer grid (five model families x calibration start x time step x data). golden.py loads the
shipped files into the per-bore structure this module reads; the tuning scratch builds the same structure from
the simulation. Nothing here reads a file.

obs[code] = dict(unit, cls, kind, dips=(days, levels), logger=(days, levels) or None, baseline=level or None)
with days counted from 1 January 1990 and levels in m AHD."""
import datetime as dt

import numpy as np

import models as M

TRIGGER = {"unconsolidated": 2.0, "consolidated": 5.0}
SEP = (dt.date(2026, 9, 1), dt.date(2026, 9, 30))
JUNE22 = (dt.date(2022, 6, 1), dt.date(2022, 6, 30))
REF_PERIOD = (dt.date(2022, 4, 1), dt.date(2022, 6, 30))
PRE_END = dt.date(2022, 6, 30)
CAL_END = dt.date(2022, 7, 3)
TREND_STARTS = {"2017": dt.date(2017, 1, 1), "2012": dt.date(2012, 1, 1)}
TREND_AT = dt.date(2026, 9, 15)
FAMILIES = ("gamma", "exp", "crd", "ma", "full")
CALS = ("first", "may2015")
STEPS = ("daily", "monthly")
DATAS = ("dips", "logger")
dn = M.dnum


def in_window(days, lo, hi):
    return (days >= dn(lo)) & (days <= dn(hi))


def series(o, data):
    """The bore's level readings for a fit: static dips, or logger daily means from the logger's first day with the
    dips before it."""
    d_days, d_lev = o["dips"]
    if data == "dips" or o.get("logger") is None:
        return d_days, d_lev
    l_days, l_lev = o["logger"]
    first = l_days.min()
    keep = d_days < first
    days = np.concatenate([d_days[keep], l_days])
    lev = np.concatenate([d_lev[keep], l_lev])
    order = np.argsort(days, kind="stable")
    return days[order], lev[order]


def assessment_level(o, rule="mean"):
    """MG-02 2.4: the mean of the bore's static levels in September 2026, daily means for a logged bore. rule='last'
    takes the last static reading in the month instead (a variant)."""
    if o.get("logger") is not None:
        days, lev = o["logger"]
    else:
        days, lev = o["dips"]
    sel = in_window(days, *SEP)
    if rule == "last":
        return float(lev[sel][np.argmax(days[sel])])
    return float(lev[sel].mean())


def window_mean(o, lo, hi, data="logger"):
    days, lev = series(o, data)
    sel = in_window(days, lo, hi)
    return float(lev[sel].mean())


def monthly(o, data="logger", until=PRE_END):
    days, lev = series(o, data)
    sel = days <= dn(until)
    mi = np.array([M.month_index(M.D0 + dt.timedelta(days=int(x))) for x in days[sel]])
    u, inv = np.unique(mi, return_inverse=True)
    return u, np.bincount(inv, lev[sel]) / np.bincount(inv)


def month_mid_day(mi):
    y, m = 1990 + mi // 12, mi % 12 + 1
    return dn(dt.date(y, m, 15))


def rungs(obs, landholders, refs, cl, level_rule="mean"):
    """Every naive rung's quantity per landholder bore (a positive figure is a fall, m)."""
    L = {k: assessment_level(o, level_rule) for k, o in obs.items()}
    out = {}
    out["R1 decline from the baseline assessment"] = {k: obs[k]["baseline"] - L[k] for k in landholders}
    out["R1b decline from the June 2022 level"] = {k: window_mean(obs[k], *JUNE22) - L[k] for k in landholders}
    mean_pre = {}
    for k in landholders:
        u, v = monthly(obs[k])
        mean_pre[k] = float(v.mean())
    out["R1b decline from the 2012 to 2022 mean"] = {k: mean_pre[k] - L[k] for k in landholders}
    ref_change = {k: window_mean(obs[k], *REF_PERIOD) - L[k] for k in refs}
    pooled = float(np.mean(list(ref_change.values())))
    alluv = [k for k in refs if obs[k]["unit"] == "alluvium"]
    basalt = [k for k in refs if obs[k]["unit"] == "basalt"]
    matched = {"alluvium": float(np.mean([ref_change[k] for k in alluv])),
               "basalt": float(np.mean([ref_change[k] for k in basalt]))}
    matched["coal"] = matched["basalt"]
    r1 = out["R1 decline from the baseline assessment"]
    out["R2 less the reference bores' change, pooled"] = {k: r1[k] - pooled for k in landholders}
    out["R2 less the reference bores' change, matched by unit"] = {k: r1[k] - matched[obs[k]["unit"]] for k in landholders}
    for name, start in TREND_STARTS.items():
        vals = {}
        for k in landholders:
            u, v = monthly(obs[k])
            t = np.array([month_mid_day(x) for x in u])
            sel = t >= dn(start)
            A = np.vstack([np.ones(sel.sum()), t[sel] / 365.25]).T
            coef, *_ = np.linalg.lstsq(A, v[sel], rcond=None)
            vals[k] = float(coef[0] + coef[1] * dn(TREND_AT) / 365.25) - L[k]
        out["R2b pre-July 2022 trend extrapolated, from %s" % name] = vals
    for w in (1, 3):
        vals = {}
        for k in landholders:
            days, lev = series(obs[k], "logger")
            pre = days <= dn(CAL_END)
            model, info = M.fit_crd_fixed(cl, "monthly", days[pre], lev[pre], dn(CAL_END), w)
            vals[k] = M.sep_value(cl, model, "monthly") - L[k]
        out["R3 one rainfall-departure window for every bore, %d %s" % (w * 12 if w == 1 else w, "months" if w == 1 else "years")] = vals
    return out, dict(levels=L, ref_change=ref_change, pooled=pooled, matched=matched, mean_pre=mean_pre)


def cell(obs, k, cl, family, cal, step, data, level_rule="mean"):
    """The mine's drawdown at one bore in one grid cell: the fitted level for September 2026 less the assessment
    level, or the full-record model's take term."""
    o = obs[k]
    days, lev = series(o, data)
    lo = days.min() if cal == "first" else dn(M.MAY15)
    L = assessment_level(o, level_rule)
    if family == "full":
        sel = (days >= lo) & (days <= dn(SEP[1]))
        clim, take_term, info = M.fit_full(cl, step, days[sel], lev[sel])
        return M.sep_value(cl, take_term, step), info
    sel = (days >= lo) & (days <= dn(CAL_END))
    if family in ("gamma", "exp"):
        model, info = M.fit_response(cl, family, step, days[sel], lev[sel])
    elif family == "crd":
        model, info = M.fit_crd(cl, step, days[sel], lev[sel], dn(CAL_END))
    else:
        model, info = M.fit_ma(cl, step, days[sel], lev[sel])
    return M.sep_value(cl, model, step) - L, info


def grid(obs, landholders, cl, families=FAMILIES, cals=CALS, steps=STEPS, datas=DATAS, level_rule="mean"):
    """{(family, cal, step, data): {bore: drawdown}}; the data axis matters only at logged bores."""
    out = {}
    for fam in families:
        for cal in cals:
            for step in steps:
                for data in datas:
                    vals = {}
                    for k in landholders:
                        if data == "logger" and obs[k].get("logger") is None:
                            vals[k] = out[(fam, cal, step, "dips")][k] if (fam, cal, step, "dips") in out else \
                                cell(obs, k, cl, fam, cal, step, "dips", level_rule)[0]
                        else:
                            vals[k] = cell(obs, k, cl, fam, cal, step, data, level_rule)[0]
                    out[(fam, cal, step, data)] = vals
    return out


def designate(vals, obs):
    return sorted(k for k, v in vals.items() if v > TRIGGER[obs[k]["cls"]])


def margin_ok(vals, obs, frac=0.25):
    """Every bore at least frac of its trigger away from it."""
    bad = {}
    for k, v in vals.items():
        t = TRIGGER[obs[k]["cls"]]
        if (1 - frac) * t < v < (1 + frac) * t:
            bad[k] = round(v, 3)
    return bad
