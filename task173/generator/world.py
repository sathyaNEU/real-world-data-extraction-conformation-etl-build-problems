"""The clean truth of the Varner Valley world: farms, pumps, rights, weather and every season's water and energy,
drawn before any record is written or any mess applied.

Juniors (the Lone Bench lands): Lone Bench Irrigation District landowners whose canal water is the district's
post-1914 right; each farm pumps the rest of its need from a deep bench well.
Seniors (the bottomlands): riparian and pre-1914 holders under the Varner River decree who lift their diversion out
of the river with an electric river pump; most also run a shallow well at the same plant on the same service.
"""
from __future__ import annotations

import datetime as dt
import numpy as np

import common as C

ETO_MONTH = {1: 1.05, 2: 1.75, 3: 2.95, 4: 4.40, 5: 6.15, 6: 7.30, 7: 7.95, 8: 7.05, 9: 5.25,
             10: 3.45, 11: 1.60, 12: 0.95}            # station 247 monthly mean reference ET, inches
DELIV_SHARE = {4: 0.10, 5: 0.16, 6: 0.19, 7: 0.20, 8: 0.19, 9: 0.16}   # LBID canal delivery pattern
DRY = {2015, 2021, 2022, 2025, 2026}


def rng(tag):
    """One stream per component, keyed by a stable digest of its tag."""
    return np.random.default_rng([C.SEED, sum(ord(c) * (i + 1) for i, c in enumerate(tag))])


class World:
    pass


def draw():
    W = World()
    # ---- weather: daily reference ET at station 247, 2007 to 15 October 2026
    r = rng("eto")
    yf = {}
    for y in C.ET_YEARS:
        yf[y] = 1.0 + r.normal(0, 0.022) + (0.028 if y in DRY else 0.0) + (0.012 if y in (2013, 2014) else 0.0)
    days = []
    d = dt.date(2007, 1, 1)
    end = dt.date(2026, 10, 15)
    while d <= end:
        m = d.month
        ndays = (dt.date(d.year + (m == 12), m % 12 + 1, 1) - dt.date(d.year, m, 1)).days
        base = ETO_MONTH[m] / ndays
        f = yf[d.year] if m in C.SEASON else 1.0 + 0.4 * (yf[d.year] - 1.0)
        v = base * f * np.exp(r.normal(0, 0.16))
        days.append((d, max(v, 0.0)))
        d += dt.timedelta(days=1)
    W.eto_daily = days
    mon = {}
    for d, v in days:
        mon[(d.year, d.month)] = mon.get((d.year, d.month), 0.0) + v
    W.eto_month = mon
    W.eto_season = {y: sum(mon[(y, m)] for m in C.SEASON) for y in C.ET_YEARS}
    W.eto_normal = float(np.mean([W.eto_season[y] for y in C.ET_YEARS]))

    # ---- juniors: Lone Bench farms, one deep well each
    r = rng("juniors")
    nJ = 296
    crops = np.array(["ALMOND", "PISTACHIO", "WALNUT", "WINEGRAPE", "CORN SILAGE"])
    kc = {"ALMOND": 0.98, "PISTACHIO": 0.92, "WALNUT": 1.02, "WINEGRAPE": 0.70, "CORN SILAGE": 0.86}
    J = {}
    J["acres"] = np.clip(np.round(r.lognormal(np.log(132), 0.55, nJ) * 0.9923, 1), 18, 960)
    J["crop"] = r.choice(crops, nJ, p=[0.45, 0.25, 0.15, 0.06, 0.09])
    J["kc"] = np.array([kc[c] for c in J["crop"]]) * r.normal(1, 0.035, nJ)
    J["eff"] = r.uniform(0.82, 0.90, nJ)
    J["need_n"] = J["acres"] * J["kc"] * (W.eto_normal / 12.0) / J["eff"]           # AF in a normal season
    J["contract"] = np.round(J["acres"] * r.choice([2.4, 2.5, 2.6, 2.6, 2.6, 2.7, 2.8], nJ), 1)
    J["swl"] = r.uniform(298, 402, nJ)
    J["dd"] = r.uniform(24, 62, nJ)
    J["dis"] = r.uniform(38, 72, nJ)
    J["ope"] = r.uniform(0.50, 0.70, nJ)
    J["k"] = 1.0241 * (J["swl"] + J["dd"] + J["dis"]) / J["ope"]                  # kWh per acre-foot
    J["off_af"] = J["acres"] * r.uniform(0.10, 0.32, nJ)                           # Oct to Mar, pre-irrigation and frost
    J["dp"] = np.where(r.random(nJ) < 0.58, "BENCH", "CORWIN ROAD")
    W.J = J
    W.nJ = nJ

    # ---- seniors: bottomland farms under the decree, a river lift and (mostly) a shallow well on one service
    r = rng("seniors")
    nS = 384
    crops = np.array(["ALFALFA", "IRRIGATED PASTURE", "PROCESSING TOMATO", "WALNUT", "ALMOND", "PRUNE"])
    kcs = {"ALFALFA": 1.06, "IRRIGATED PASTURE": 1.00, "PROCESSING TOMATO": 0.86, "WALNUT": 1.02, "ALMOND": 0.98,
           "PRUNE": 0.95}
    effs = {"ALFALFA": 0.72, "IRRIGATED PASTURE": 0.68, "PROCESSING TOMATO": 0.78, "WALNUT": 0.84, "ALMOND": 0.85,
            "PRUNE": 0.84}
    S = {}
    S["acres"] = np.clip(np.round(r.lognormal(np.log(160), 0.6, nS), 1), 15, 1400)
    S["crop"] = r.choice(crops, nS, p=[0.30, 0.15, 0.20, 0.15, 0.10, 0.10])
    S["kc"] = np.array([kcs[c] for c in S["crop"]]) * r.normal(1, 0.035, nS)
    S["eff"] = np.array([effs[c] for c in S["crop"]]) * r.normal(1, 0.03, nS)
    S["need_n"] = S["acres"] * S["kc"] * (W.eto_normal / 12.0) / S["eff"]
    S["well"] = r.random(nS) < 0.86
    orch = np.isin(S["crop"], ["WALNUT", "ALMOND", "PRUNE"])
    S["wsh0"] = np.where(S["well"], np.where(orch, r.uniform(0.10, 0.28, nS), r.uniform(0.05, 0.16, nS)), 0.0)
    u = np.clip(r.normal(0.66, 0.15, nS), 0.18, 0.98)
    dn_nominal = S["need_n"] * (1 - S["wsh0"])
    S["allot"] = np.round(dn_nominal / u)                                         # decreed season allotment, AF
    S["r_tdh"] = r.uniform(18, 24, nS)
    S["r_ope"] = r.uniform(0.60, 0.68, nS)
    S["kr"] = 1.0241 * S["r_tdh"] / S["r_ope"]
    S["w_swl"] = r.uniform(18, 46, nS)
    S["w_dd"] = r.uniform(12, 30, nS)
    S["w_dis"] = r.uniform(36, 63, nS)
    S["w_ope"] = r.uniform(0.50, 0.66, nS)
    S["kw"] = np.where(S["well"], 1.0241 * (S["w_swl"] + S["w_dd"] + S["w_dis"]) / S["w_ope"], 0.0)
    S["off_w"] = np.where(S["well"] & orch, S["acres"] * r.uniform(0.04, 0.12, nS), 0.0)   # frost protection
    S["dp"] = np.where(r.random(nS) < 0.52, "RIVERSIDE", "MILL SLOUGH")
    W.S = S
    W.nS = nS

    # ---- season by season: water and energy at every plant, by month (the clean truth)
    r = rng("history")
    W.months = [(y, m) for y in C.YEARS for m in range(1, 13) if not (y == 2026 and m > 9)]
    J_af = {}; J_kwh = {}
    S_div = {}; S_wa = {}; S_kwh = {}
    kJy = {}; kRy = {}; kWy = {}
    for y in C.YEARS:
        kJy[y] = J["k"] * r.normal(1, 0.008, nJ)
        kRy[y] = S["kr"] * r.normal(1, 0.008, nS)
        kWy[y] = S["kw"] * r.normal(1, 0.008, nS)
    wsh = {}
    for y in C.YEARS:
        wsh[y] = np.where(S["well"], np.clip(S["wsh0"] * np.exp(r.normal(0, 0.30, nS)), 0.0, 0.55), 0.0)
    for (y, m) in W.months:
        if m in C.SEASON:
            et_ratio = W.eto_month[(y, m)] / W.eto_normal          # this month's ET as a share of a normal season
            need_m_J = J["need_n"] * et_ratio * r.normal(1, 0.025, nJ)
            deliv = C.LBID_ALLOC[y] * J["contract"] * DELIV_SHARE[m]
            pj = np.maximum(need_m_J - deliv, 0.0)
            need_m_S = S["need_n"] * et_ratio * r.normal(1, 0.025, nS)
            d_m = need_m_S * (1 - wsh[y])
            w_m = need_m_S * wsh[y]
        else:
            share = {1: 0.06, 2: 0.14, 3: 0.30, 10: 0.32, 11: 0.12, 12: 0.06}[m]
            pj = J["off_af"] * share * r.normal(1, 0.10, nJ)
            d_m = np.zeros(nS)
            w_m = S["off_w"] * {1: 0.10, 2: 0.30, 3: 0.40, 10: 0.10, 11: 0.05, 12: 0.05}[m] * r.normal(1, 0.10, nS)
        J_af[(y, m)] = pj
        J_kwh[(y, m)] = pj * kJy[y]
        S_div[(y, m)] = d_m
        S_wa[(y, m)] = w_m
        S_kwh[(y, m)] = d_m * kRy[y] + w_m * kWy[y]
    W.J_af, W.J_kwh, W.S_div, W.S_wa, W.S_kwh = J_af, J_kwh, S_div, S_wa, S_kwh

    # ---- the 2027 season under the order, at a normal season (the truth the forecast is scored against)
    W.truth = truth_2027(W)
    return W


def truth_2027(W):
    J, S = W.J, W.S
    j = float((J["need_n"] * J["k"]).sum())
    wshe = W.S["wsh0"] * np.exp(0.30 ** 2 / 2)
    wshe = np.minimum(wshe, 0.55)
    dn = S["need_n"] * (1 - wshe)
    wn = S["need_n"] * wshe
    lim = C.SENIOR_LIMIT_2027 * S["allot"]
    div27 = np.minimum(dn, lim)
    gap = np.maximum(dn - lim, 0.0)
    s = float((div27 * S["kr"]).sum() + ((wn + gap) * S["kw"] * S["well"]).sum())
    return {"juniors_kwh": j, "seniors_kwh": s, "total_kwh": j + s}
