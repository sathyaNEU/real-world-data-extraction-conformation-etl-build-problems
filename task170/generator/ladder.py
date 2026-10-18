"""The main call's ladder: the children's need under every route, the family that must agree with the golden, the
rivals that must not, and the same routes stood at closed origins for the out-of-sample record. Shared by checks.py,
deliver.py and the design note's figures."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import calc as K
import common as C

D = dt.date

FAMILY = ["golden", "thr2995", "win36", "win24", "q1", "sig_rms", "sig_diff", "sig_near", "pooled_everyone",
          "monte_carlo", "hazard24", "hazard_pooled"]
# the choice each member varies from the golden; a pair of members from two dimensions is a solver's compound choice
DIMENSION = {"thr2995": "threshold", "win36": "window", "win24": "window", "q1": "weighed", "sig_rms": "scatter",
             "sig_diff": "scatter", "sig_near": "scatter", "pooled_everyone": "slope", "monte_carlo": "computation",
             "hazard24": "exits", "hazard_pooled": "exits"}
# the scatter from the median absolute deviation over every candidate: reported beside the family (the infants'
# smaller scatter pulls it below the near-band children's), asserted in the step
ALSO = ["sig_mad"]
# the decisive step taken with each child's slope pooled or shrunk toward a group's: the register measures the
# between-child spread of slopes, and every one of these under-forecasts every closed window
SHRUNK = ["pooled_candidates", "pooled_paediatric", "pooled_global", "eb_dl", "eb_dl_group"]


def family(kids, visits):
    c = K.context(kids, visits)
    out = {}
    out["golden"] = K.total(c, K.P_noisy(c, thr=30.0)[0])[0]
    out["thr2995"] = K.total(c, K.P_noisy(c, thr=29.95)[0])[0]
    out["win36"] = K.total(c, K.P_noisy(c, window=36, thr=30.0)[0])[0]
    out["win24"] = K.total(c, K.P_noisy(c, window=24, thr=30.0)[0])[0]
    out["q1"] = K.total(c, K.P_noisy(c, q=1.0, thr=30.0)[0])[0]
    for kind in ("rms", "mad", "diff", "near"):
        out["sig_" + kind] = K.total(c, K.P_noisy(c, thr=30.0, sig=K.scatter(c, kind))[0])[0]
    out["pooled_everyone"] = K.total(c, K.P_pooled_velocity(c, 30.0, "everyone"))[0]
    out["monte_carlo"] = K.total(c, K.P_monte_carlo(c, thr=30.0))[0]
    c24 = K.context(kids, visits, hz_months=24)
    out["hazard24"] = K.total(c24, K.P_noisy(c24, thr=30.0)[0])[0]
    cp = K.context(kids, visits, by_age=False)
    out["hazard_pooled"] = K.total(cp, K.P_noisy(cp, thr=30.0)[0])[0]
    return out, c


CHOICE = {"thr2995": dict(thr=29.95), "win36": dict(window=36), "win24": dict(window=24), "q1": dict(q=1.0),
          "sig_rms": dict(sig="rms"), "sig_diff": dict(sig="diff"), "sig_near": dict(sig="near"),
          "hazard24": dict(hz="24"), "hazard_pooled": dict(hz="pooled")}


def compound(kids, visits, keys):
    """The children's need under the golden construction with the choices of several family members at once."""
    kw = {}
    for k in keys:
        kw.update(CHOICE[k])
    hz = kw.pop("hz", None)
    c = K.context(kids, visits, hz_months=24) if hz == "24" else (
        K.context(kids, visits, by_age=False) if hz == "pooled" else K.context(kids, visits))
    sig = kw.pop("sig", None)
    if sig is not None:
        kw["sig"] = K.scatter(c, sig)
    kw.setdefault("thr", 30.0)
    return K.total(c, K.P_noisy(c, **kw)[0])[0]


def extreme_pairs(fam):
    """The two members from different dimensions whose choices push the need furthest up, and furthest down."""
    d = {k: fam[k] - fam["golden"] for k in FAMILY if k in CHOICE}
    best = {}
    keys = sorted(d)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if DIMENSION[a] != DIMENSION[b]:
                best[(a, b)] = d[a] + d[b]
    hi = max(best, key=best.get)
    lo = min(best, key=best.get)
    return lo, hi


def shrunk(c):
    """The decisive step with each child's slope pooled (by sex and year of age over the candidates or over every
    child on a paediatric regimen, or the candidates' one mean slope) or shrunk by random effects."""
    out = {}
    out["pooled_candidates"] = K.total(c, K.P_pooled_velocity(c, 30.0, "cand"))[0]
    out["pooled_paediatric"] = K.total(c, K.P_pooled_velocity(c, 30.0, "paed"))[0]
    out["pooled_global"] = K.total(c, K.P_eb(c, 30.0))[0]
    out["eb_dl"] = K.total(c, K.P_eb_dl(c, 30.0))[0]
    out["eb_dl_group"] = K.total(c, K.P_eb_dl(c, 30.0, by_group=True))[0]
    return out


def rivals(c):
    """Every rival route's children's need (bottles over the window, with the maximum stock level)."""
    r = {}

    def put(k, P):
        r[k] = K.total(c, P)[0]
    r["carried"] = K.total(c, np.zeros((len(c.cand), c.nm)))[0]
    put("smooth_all", K.P_smooth(c))
    put("smooth_36", K.P_smooth(c, window=36))
    put("smooth_24", K.P_smooth(c, window=24))
    put("smooth_12", K.P_smooth(c, window=12))
    put("exp_smooth_all", K.P_smooth(c, form="exp"))
    put("exp_smooth_24", K.P_smooth(c, window=24, form="exp"))
    put("exp_smooth_12", K.P_smooth(c, window=12, form="exp"))
    put("exp_noisy_24", K.P_noisy(c, window=24, form="exp", thr=30.0)[0])
    put("exp_noisy_12", K.P_noisy(c, window=12, form="exp", thr=30.0)[0])
    put("noisy_12", K.P_noisy(c, window=12, thr=30.0)[0])
    put("noisy_monthly", K.P_noisy(c, monthly=True, thr=30.0)[0])
    put("band_0.5", K.P_band_hazard(c, 0.5))
    put("band_1.0", K.P_band_hazard(c, 1.0))
    r["chain_12"] = K.need_band_chain(c, 12)
    r["chain_24"] = K.need_band_chain(c, 24)
    for L in (3, 6, 12):
        r["recent_%d" % L] = K.need_recent(c, L)
    r["trend"] = K.need_trend(c)
    put("age_median_backlog", K.P_age(c, None, True))
    put("age_median_window", K.P_age(c, None, False))
    for A in (10, 11, 12):
        put("age_%d_backlog" % A, K.P_age(c, A, True))
    put("ten_and_over", K.P_now_if(c, lambda u: (c.fr.origin - c.dob[u]).days / 365.25 >= 10))
    Pm, cross = K.P_mean_curve(c)
    put("crossing_age_window", Pm)
    put("mean_curve", K.P_centile_tracking(c))
    for th in (27, 28, 29):
        put("last_weight_%d" % th, K.P_now_if(c, lambda u, th=th: c.lastw.get(u, 0) >= th))
    Pl, L = K.P_lead_shift(c)
    put("lead_shift", Pl)
    return r, dict(cross=cross, lead=L, median_age=K.median_switch_age(c))


AGE_RULE = [dict(look=lk, bw=bw, interp=ip, backlog=bl) for lk in (12, 24) for bw in (0.25, 0.5, 1.0)
            for ip in (False, True) for bl in (False, True)]


def age_rule(c):
    """The crossing-age rule under each binning a solver might take: each child switched on reaching the age at
    which the register's median weight for age reaches 30 kg. Returns {label: (children's need, crossing ages)}."""
    out = {}
    for kw in AGE_RULE:
        bl = kw["backlog"]
        P, cross = K.P_crossing_age(c, backlog=bl, look=kw["look"], bw=kw["bw"], interp=kw["interp"])
        lab = "%d months, %.2f-year bins, %s, %s" % (kw["look"], kw["bw"], "interpolated" if kw["interp"] else "bin label",
                                                     "backlog" if bl else "window")
        out[lab] = (K.total(c, P)[0], cross)
    return out


def actual_T(kids, visits, c):
    """Bottles the origin's candidates actually took on TLD over the window (switched and no outcome by each month's
    end), from the register's later rows."""
    sw = visits[visits.regimen == C.REG_TLD].groupby("uid").date.min()
    od = kids.set_index("uid").outcome_date
    tot = 0
    for u in c.cand:
        s = sw.get(u, None)
        if s is None or s <= c.fr.origin:
            continue
        o = od.get(u, None)
        for e in c.fr.ends:
            if s <= e and (o is None or pd.isna(o) or o > e):
                tot += 1
    return tot


BACKTESTS = [(D(2025, 8, 31), 12), (D(2025, 12, 31), 6), (D(2026, 2, 28), 6)]


def backtests(kids, visits):
    """Each route stood at a closed origin: bottle-months its candidates were forecast to take on TLD over the
    window against what the register shows they took."""
    out = []
    for origin, H in BACKTESTS:
        fr = K.Frame(origin, H, 0)
        c = K.context(kids, visits, fr)
        base = K.total(c, np.zeros((len(c.cand), c.nm)))[0]
        act = actual_T(kids, visits, c)
        row = dict(origin=origin, months=H, candidates=len(c.cand), actual=act)

        def f(P):
            return K.total(c, P)[0] - base
        row["golden"] = f(K.P_noisy(c, thr=30.0)[0])
        row["win24"] = f(K.P_noisy(c, window=24, thr=30.0)[0])
        row["pooled_everyone"] = f(K.P_pooled_velocity(c, 30.0, "everyone"))
        row["noisy_12"] = f(K.P_noisy(c, window=12, thr=30.0)[0])
        row["noisy_monthly"] = f(K.P_noisy(c, monthly=True, thr=30.0)[0])
        row["smooth_all"] = f(K.P_smooth(c))
        row["smooth_12"] = f(K.P_smooth(c, window=12))
        row["exp_smooth_all"] = f(K.P_smooth(c, form="exp"))
        row["band_0.5"] = f(K.P_band_hazard(c, 0.5))
        row["chain_12"] = K.need_band_chain(c, 12) - base
        row["recent_3"] = K.need_recent(c, 3) - base
        row["trend"] = K.need_trend(c) - base
        row["thr2995"] = f(K.P_noisy(c, thr=29.95)[0])
        row["q1"] = f(K.P_noisy(c, q=1.0, thr=30.0)[0])
        for kind in ("rms", "mad", "diff", "near"):
            row["sig_" + kind] = f(K.P_noisy(c, thr=30.0, sig=K.scatter(c, kind))[0])
        row["pooled_candidates"] = f(K.P_pooled_velocity(c, 30.0, "cand"))
        row["pooled_paediatric"] = f(K.P_pooled_velocity(c, 30.0, "paed"))
        row["pooled_global"] = f(K.P_eb(c, 30.0))
        row["eb_dl"] = f(K.P_eb_dl(c, 30.0))
        row["eb_dl_group"] = f(K.P_eb_dl(c, 30.0, by_group=True))
        Pm, _ = K.P_mean_curve(c)
        row["crossing_age_window"] = f(Pm)
        row["mean_curve"] = f(K.P_centile_tracking(c))
        out.append(row)
    return out
