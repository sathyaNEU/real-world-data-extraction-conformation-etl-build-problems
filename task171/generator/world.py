"""The clean truth of task171: Sablewood Electric Cooperative's residential services, their billed use by
load-research period and billing month, the evening-peak rate R-TOU (offered from March 2024) and the members'
take-up of it, and the expected take-up of the overnight rate R-ON from January 2027.

Members take an optional rate by what it would save them on their own use in the year before it is offered
(monthly hazard, logit in the dollar saving, decaying with months since the offer). Members on R-TOU move part
of their 4 p.m. to 9 p.m. use into other hours after joining."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as C

NPREM = 25_600
ARCH = np.array([[0.22, 0.33, 0.33, 0.12],   # evening family
                 [0.22, 0.45, 0.24, 0.09],   # home through the day
                 [0.45, 0.28, 0.18, 0.09],   # overnight timer loads (storage water heating, thermal storage)
                 [0.26, 0.30, 0.27, 0.17]])  # late evening
DALPHA = {"Sedge Flats": [2.2, 1.0, 0.45, 0.9], "Brisco Bend": [1.6, 1.6, 0.40, 0.8], "Kessel Mill": [1.4, 1.0, 1.10, 0.7],
          "Pike Ridge": [2.6, 0.9, 0.35, 1.2], "Tamsey": [1.5, 1.3, 0.80, 0.8]}
DSHARE = [0.24, 0.22, 0.18, 0.20, 0.16]
DEFF = {"Sedge Flats": 0.05, "Brisco Bend": 0.10, "Kessel Mill": -0.05, "Pike Ridge": 0.0, "Tamsey": -0.10}
TYPES = ["single-family", "manufactured", "multi-unit"]
TEFF = {"single-family": 0.0, "manufactured": -0.10, "multi-unit": -0.40}

# take-up: monthly logit hazard AK[k] + B_SAV * saving + effects + u, k months since the offer (FORM hazard)
A0, B_SAV, U_SD = -2.55, 0.020, 0.55
TIMING = np.exp(-np.arange(12) / 3.2); TIMING = TIMING / TIMING.sum()
FORM = "hazard"
AK = -4.66 - np.arange(12) / 4.0
JOIN_TAIL = 0.0009     # monthly, members of the offer cohort after the first year
LEAVE = 0.0045          # monthly hazard of going back to R-1 after twelve months on R-TOU
JOIN_LATE = 0.0022      # monthly hazard of joining R-TOU for services opened after the offer
MOVE = 0.0071           # monthly move-out hazard
SHIFT_MU, SHIFT_SD = 0.15, 0.05


def season(m, heat):
    """monthly use factor (mean 1 over the year)"""
    w = np.cos((m - 1) / 12 * 2 * np.pi)          # winter +1, summer -1
    s = np.cos((m - 7.5) / 12 * 2 * np.pi)        # summer peak
    f = 1 + np.where(heat, 0.38, 0.10) * np.maximum(w, 0) + 0.22 * np.maximum(s, 0)
    return f


def build(seed=C.SEED):
    rng = np.random.default_rng(seed)
    nm = len(C.MONTHS)
    # premises
    dist = rng.choice(len(C.DISTRICTS), NPREM, p=DSHARE)
    ptype = rng.choice(3, NPREM, p=[0.66, 0.21, 0.13])
    heat = rng.random(NPREM) < np.where(ptype == 2, 0.30, 0.47)
    cycle = rng.integers(1, 5, NPREM)
    prem = pd.DataFrame(dict(prem=np.arange(NPREM), district=[C.DISTRICTS[d] for d in dist],
                             ptype=[TYPES[t] for t in ptype], heat=heat, cycle=cycle))
    # services: occupants over the window (open index -1 means opened before March 2023)
    rows = []
    for p in range(NPREM):
        start = -1
        close = rng.geometric(MOVE) - 1                 # last billing month of the occupant at the window's start
        while True:
            rows.append((p, start, close if close < nm else None))
            if close >= nm:
                break
            start = close + 1 + int(rng.random() < 0.18)  # a vacant month now and then
            if start >= nm:
                break
            close = start + rng.geometric(MOVE) - 1
    svc = pd.DataFrame(rows, columns=["prem", "open_i", "close_i"])
    svc = svc.merge(prem, on="prem", how="left")
    ns = len(svc)
    svc["sid"] = np.arange(ns)
    # profiles and use
    w = np.vstack([rng.dirichlet(DALPHA[d]) for d in svc.district])
    svc[["w0", "w1", "w2", "w3"]] = w
    tbase = np.array([11800, 9900, 6400])[svc.ptype.map({t: i for i, t in enumerate(TYPES)}).values]
    svc["kwh_yr"] = tbase * np.where(svc.heat, 1.30, 1.0) * rng.lognormal(0, 0.33, ns) * (1 + 0.25 * w[:, 0])
    svc["u"] = rng.normal(0, U_SD, ns)
    svc["shift"] = np.clip(rng.normal(SHIFT_MU, SHIFT_SD, ns), 0.02, 0.35)
    ev = rng.random(ns) < 0.075
    svc["ev_i"] = np.where(ev, rng.integers(-6, nm + 4, ns), 10_000)
    svc["ev_kwh"] = np.where(ev, rng.normal(255, 60, ns).clip(120, 420), 0.0)
    # use by month, before any rate effect: (ns, nm, 4)
    mm = np.array([m for _, m in C.MONTHS])
    fac = season(mm[None, :], svc.heat.values[:, None])
    tot = svc.kwh_yr.values[:, None] / 12 * fac * rng.lognormal(0, 0.075, (ns, nm))
    sh = (w @ ARCH)[:, None, :] * np.ones((1, nm, 1))
    summer = np.maximum(np.cos((mm - 7.5) / 12 * 2 * np.pi), 0)[None, :, None]
    winter = np.maximum(np.cos((mm - 1) / 12 * 2 * np.pi), 0)[None, :, None]
    tilt = np.array([0.0, -0.01, 0.025, -0.015])[None, None, :] * summer + np.array([0.02, 0.0, -0.01, -0.01])[None, None, :] * winter
    sh = np.clip(sh + tilt + rng.normal(0, 0.008, (ns, nm, 4)), 0.02, None)
    sh /= sh.sum(2, keepdims=True)
    use = tot[:, :, None] * sh
    evm = (np.arange(nm)[None, :] >= svc.ev_i.values[:, None]) * svc.ev_kwh.values[:, None]
    use[:, :, 0] += evm * 0.93
    use[:, :, 1] += evm * 0.07
    cl = svc.close_i.fillna(nm).values.astype(int)
    active = (np.arange(nm)[None, :] >= np.maximum(svc.open_i.values, 0)[:, None]) & (np.arange(nm)[None, :] <= cl[:, None])
    use = use * active[:, :, None]

    # R-TOU: offered to services on R-1 and open at 1 March 2024
    pre = use[:, C.PRE_A, :].sum(1)                        # pre-offer billed use by period
    npre = active[:, C.PRE_A].sum(1)
    savA = npre * (C.R1_2024["cc"] - C.RTOU_2024["cc"]) + pre.sum(1) * C.R1_2024["e"] \
        - (pre[:, 2] * C.RTOU_2024["peak"] + (pre.sum(1) - pre[:, 2]) * C.RTOU_2024["other"])
    svc["savA"] = savA
    lin = A0 + B_SAV * savA + svc.district.map(DEFF).values + svc.ptype.map(TEFF).values + svc.u.values
    base = 1 / (1 + np.exp(-lin))
    close = svc.close_i.fillna(10_000).values
    cohort = (svc.open_i.values < C.OFFER_A) & (close >= C.OFFER_A)
    svc["cohortA"] = cohort
    tou_start = np.full(ns, -1)
    tou_end = np.full(ns, -1)
    # a member of the offer cohort decides once, in the rate's first year, with probability logistic(lin); the
    # month its rate change takes effect follows the launch campaign's response curve, whatever its saving
    if FORM == "once":
        takes = cohort & (rng.random(ns) < base)
        k = rng.choice(12, ns, p=TIMING)
        eff = C.OFFER_A + k
        ok = takes & (close >= eff)
        tou_start[ok] = eff[ok]
    else:
        # monthly discrete-time hazard, logit in the saving with a month-since-offer effect
        lin0 = lin - A0
        for kk in range(12):
            t = C.OFFER_A + kk
            at = cohort & (tou_start < 0) & (close >= t)
            hz = 1 / (1 + np.exp(-(AK[kk] + lin0)))
            j = at & (rng.random(ns) < hz)
            tou_start[j] = t
    # services opened after the offer join at a low steady rate; members who passed in the first year rarely do later
    for t in range(C.OFFER_A + 1, nm):
        at = (tou_start < 0) & (close >= t) & (svc.open_i.values <= t)
        hz = np.where(svc.open_i.values >= C.OFFER_A, JOIN_LATE, np.where(cohort & (t >= C.OFFER_A + 12), JOIN_TAIL, 0.0))
        j = at & (rng.random(ns) < hz)
        tou_start[j] = t
    # leaving R-TOU after twelve months
    for t in range(C.OFFER_A + 12, nm):
        on = (tou_start >= 0) & (tou_end < 0) & (t - tou_start >= 13) & (close >= t)
        lv = on & (rng.random(ns) < LEAVE)
        tou_end[lv] = t                                     # first month back on R-1
    svc["tou_start"] = tou_start
    svc["tou_end"] = tou_end
    # behaviour on R-TOU: part of the 4-9 p.m. use moves to other hours from the first month on the rate
    on_tou = np.zeros((ns, nm), bool)
    for i in np.where(tou_start >= 0)[0]:
        e = tou_end[i] if tou_end[i] >= 0 else nm
        on_tou[i, tou_start[i] + 1:e] = True        # the rate takes effect at the read that closes billing month tou_start
    moved = use[:, :, 2] * svc["shift"].values[:, None] * on_tou
    use[:, :, 2] -= moved
    use[:, :, 0] += moved * 0.42
    use[:, :, 1] += moved * 0.33
    use[:, :, 3] += moved * 0.25
    svc["on_tou_asof"] = (tou_start >= 0) & (tou_end < 0) & svc.close_i.isna()
    return dict(prem=prem, svc=svc, use=use, active=active, on_tou=on_tou)


def truth_B(W):
    """expected moves to R-ON by quarter end among the R-1 services open at 31 October 2026 (no closures), and the
    shortfall at test-year use on the 2027 schedules"""
    svc, use, active = W["svc"], W["use"], W["active"]
    ty = use[:, C.TEST, :]
    nty = active[:, C.TEST].sum(1)
    pop = svc.close_i.isna().values & ~svc.on_tou_asof.values & (nty == 12)
    kwh = ty.sum(1)
    savB = nty * (C.R1_2027["cc"] - C.RON_2027["cc"]) + kwh.sum(1) * C.R1_2027["e"] \
        - (kwh[:, 0] * C.RON_2027["off"] + (kwh.sum(1) - kwh[:, 0]) * C.RON_2027["other"])
    lin = A0 + B_SAV * savB + svc.district.map(DEFF).values + svc.ptype.map(TEFF).values + svc.u.values
    base = 1 / (1 + np.exp(-lin))
    if FORM == "once":
        cum = np.cumsum(TIMING)
        P = {q: base * cum[3 * q - 1] for q in (1, 2, 3, 4)}
    else:
        lin0 = lin - A0
        surv = np.ones(len(svc)); P = {}
        for kk in range(12):
            surv = surv * (1 - 1 / (1 + np.exp(-(AK[kk] + lin0))))
            if kk % 3 == 2:
                P[kk // 3 + 1] = 1 - surv
    out = {q: dict(n=float(P[q][pop].sum()), short=float((P[q] * savB)[pop].sum())) for q in P}
    return out, savB, pop
