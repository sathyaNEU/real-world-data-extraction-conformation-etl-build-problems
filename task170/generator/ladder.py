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

FAMILY = ["golden", "plain", "thr2995", "win36", "win24", "q1", "sig_rms", "sig_mad", "sig_diff", "sig_near", "own_sd",
          "pv", "pv_win36", "pv_win24", "eb_plug", "eb_plug_win36", "eb_plug_win24", "eb_pred", "eb_pred_win36",
          "eb_pred_win24", "eb_joint", "mc_joint", "monte_carlo", "hazard24", "hazard_pooled", "seasonal"]
# the choice each member varies from the golden; a pair of members from two dimensions is a solver's compound choice
DIMENSION = {"plain": "held back", "thr2995": "threshold", "win36": "window", "win24": "window", "q1": "weighed",
             "sig_rms": "scatter", "sig_mad": "scatter", "sig_diff": "scatter", "sig_near": "scatter",
             "own_sd": "scatter", "pv": "line error", "pv_win36": "line error", "pv_win24": "line error",
             "eb_plug": "line error", "eb_plug_win36": "line error", "eb_plug_win24": "line error",
             "eb_pred": "line error", "eb_pred_win36": "line error", "eb_pred_win24": "line error",
             "eb_joint": "line error", "mc_joint": "line error", "monte_carlo": "computation", "hazard24": "exits",
             "hazard_pooled": "exits", "seasonal": "season"}
ALSO = []
# the decisive step taken with each child's slope pooled toward a group's: the register measures the between-child
# spread of slopes, and pooling removes it
SHRUNK = ["pooled_candidates", "pooled_paediatric", "pooled_everyone", "pooled_global"]


def family(kids, visits, fr=K.MAIN):
    c = K.context(kids, visits, fr)
    out = {}
    T = lambda P: K.total(c, P)[0]
    out["golden"] = T(K.P_noisy(c)[0])
    out["plain"] = T(K.P_noisy(c, lag=0.0)[0])
    out["thr2995"] = T(K.P_noisy(c, thr=c.thr - 0.05)[0])
    out["win36"] = T(K.P_noisy(c, window=36)[0])
    out["win24"] = T(K.P_noisy(c, window=24)[0])
    out["q1"] = T(K.P_noisy(c, q=1.0)[0])
    for kind in ("rms", "mad", "diff", "near"):
        out["sig_" + kind] = T(K.P_noisy(c, sig=K.scatter(c, kind))[0])
    out["own_sd"] = T(K.P_own_sd(c))
    out["pv"] = T(K.P_pv(c))
    out["pv_win36"] = T(K.P_pv(c, 36))
    out["pv_win24"] = T(K.P_pv(c, 24))
    out["eb_plug"] = T(K.P_shrunk(c))
    out["eb_plug_win36"] = T(K.P_shrunk(c, 36))
    out["eb_plug_win24"] = T(K.P_shrunk(c, 24))
    out["eb_pred"] = T(K.P_shrunk(c, None, True))
    out["eb_pred_win36"] = T(K.P_shrunk(c, 36, True))
    out["eb_pred_win24"] = T(K.P_shrunk(c, 24, True))
    out["eb_joint"] = T(K.P_joint(c, shrink=True))
    out["mc_joint"] = T(K.P_joint(c))
    out["monte_carlo"] = T(K.P_monte_carlo(c))
    c24 = K.context(kids, visits, fr, hz_months=24)
    out["hazard24"] = K.total(c24, K.P_noisy(c24)[0])[0]
    cp = K.context(kids, visits, fr, by_age=False)
    out["hazard_pooled"] = K.total(cp, K.P_noisy(cp)[0])[0]
    out["seasonal"] = T(K.P_seasonal(c))
    return out, c


CHOICE = {"plain": dict(lag=0.0), "thr2995": dict(thr=-0.05), "win36": dict(window=36), "win24": dict(window=24),
          "q1": dict(q=1.0), "sig_rms": dict(sig="rms"), "sig_mad": dict(sig="mad"), "sig_diff": dict(sig="diff"),
          "sig_near": dict(sig="near"), "hazard24": dict(hz="24"), "hazard_pooled": dict(hz="pooled")}


def compound(kids, visits, keys, fr=K.MAIN):
    """The children's line under the golden construction with the choices of several family members at once."""
    kw = {}
    for k in keys:
        kw.update(CHOICE[k])
    hz = kw.pop("hz", None)
    c = K.context(kids, visits, fr, hz_months=24) if hz == "24" else (
        K.context(kids, visits, fr, by_age=False) if hz == "pooled" else K.context(kids, visits, fr))
    sig = kw.pop("sig", None)
    if sig is not None:
        kw["sig"] = K.scatter(c, sig)
    if "thr" in kw:
        kw["thr"] = c.thr + kw["thr"]
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
    """The decisive step with each child's slope pooled (by sex and year of age over the candidates, over every child
    on a paediatric regimen or over every child) or replaced by the candidates' one mean slope."""
    out = {}
    out["pooled_candidates"] = K.total(c, K.P_pooled_velocity(c, None, "cand"))[0]
    out["pooled_paediatric"] = K.total(c, K.P_pooled_velocity(c, None, "paed"))[0]
    out["pooled_everyone"] = K.total(c, K.P_pooled_velocity(c, None, "everyone"))[0]
    out["pooled_global"] = K.total(c, K.P_eb(c))[0]
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
    put("exp_noisy_24", K.P_noisy(c, window=24, form="exp")[0])
    put("exp_noisy_12", K.P_noisy(c, window=12, form="exp")[0])
    put("noisy_12", K.P_noisy(c, window=12)[0])
    put("noisy_monthly", K.P_noisy(c, monthly=True)[0])
    r["no_exits"] = K.total_no_exits(c, K.P_noisy(c)[0])
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
    for k in LEADS:
        put("lead_%d" % k, K.P_line_shift(c, months=k))
    for m in MARGINS:
        put("margin_%.2f" % m, K.P_line_shift(c, margin=m))
    return r, dict(cross=cross, lead=L, median_age=K.median_switch_age(c))


LEADS = (3, 4, 5, 6, 7, 8)
MARGINS = (0.5, 0.75, 1.0, 1.25, 1.5)


# rivals the checks assert outside line 2's pallet (the habitual routes and the register-history routes), and the
# routes reported where they land (the decisive step taken with a variation the family does not hold, or a knob)
MISS = ["carried", "smooth_all", "smooth_36", "smooth_24", "smooth_12", "exp_smooth_24", "mean_curve", "band_0.5",
        "band_1.0", "chain_24", "recent_3", "recent_6", "recent_12", "trend", "lead_shift", "age_median_window",
        "crossing_age_window", "last_weight_27", "last_weight_29", "age_10_backlog", "age_11_backlog", "ten_and_over",
        "lead_7", "lead_8", "margin_0.50", "margin_1.50"]


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


BACKTESTS = [(D(2024, 8, 31), 12), (D(2025, 2, 28), 12), (D(2025, 8, 31), 6)]


def backtests(kids, visits):
    """Each route stood at a closed origin under the rule then in force (TLD from 35 kg until the 2026 guidelines):
    bottle-months its candidates were forecast to take on TLD over the window against what the register shows they
    took. Every window closes before the 2026 guidelines took effect."""
    out = []
    for origin, H in BACKTESTS:
        fr = K.Frame(origin, H, 0)
        c = K.context(kids, visits, fr)
        base = K.total(c, np.zeros((len(c.cand), c.nm)))[0]
        act = actual_T(kids, visits, c)
        row = dict(origin=origin, months=H, candidates=len(c.cand), actual=act, threshold=c.thr)

        def f(P):
            return K.total(c, P)[0] - base
        row["golden"] = f(K.P_noisy(c)[0])
        row["plain"] = f(K.P_noisy(c, lag=0.0)[0])
        row["thr2995"] = f(K.P_noisy(c, thr=c.thr - 0.05)[0])
        row["win36"] = f(K.P_noisy(c, window=36)[0])
        row["win24"] = f(K.P_noisy(c, window=24)[0])
        row["q1"] = f(K.P_noisy(c, q=1.0)[0])
        for kind in ("rms", "mad", "diff", "near"):
            row["sig_" + kind] = f(K.P_noisy(c, sig=K.scatter(c, kind))[0])
        row["own_sd"] = f(K.P_own_sd(c))
        row["pv"] = f(K.P_pv(c))
        row["pv_win24"] = f(K.P_pv(c, 24))
        row["eb_plug"] = f(K.P_shrunk(c))
        row["eb_pred"] = f(K.P_shrunk(c, None, True))
        row["noisy_12"] = f(K.P_noisy(c, window=12)[0])
        row["noisy_monthly"] = f(K.P_noisy(c, monthly=True)[0])
        row["smooth_all"] = f(K.P_smooth(c))
        row["smooth_12"] = f(K.P_smooth(c, window=12))
        row["band_0.5"] = f(K.P_band_hazard(c, 0.5))
        row["recent_3"] = K.need_recent(c, 3) - base
        row["recent_12"] = K.need_recent(c, 12) - base
        row["trend"] = K.need_trend(c) - base
        for k, v in shrunk(c).items():
            row[k] = v - base
        out.append(row)
    return out
