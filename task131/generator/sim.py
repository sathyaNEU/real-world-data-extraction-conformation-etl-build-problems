"""task131 generator: half-hourly loads for every trial premise, 1 November 2025 to 28 February 2026.

The noise is drawn first, from streams that do not depend on the response parameters, and the response is added
deterministically, so a tuned parameter moves the measured response and nothing else. Each premise carries a
general-supply channel (E1), a controlled-load hot-water channel (E2) where fitted, and an export channel (B1)
where rooftop PV is connected. Values are average kW over the half-hour."""
from datetime import timedelta

import numpy as np

import params as P
import knobs as K
import weather as WX

H = (np.arange(48) + 0.5) / 2.0      # half-hour mid-points, hours after midnight


def base_shape(weekend):
    s = 0.36 + 0.18 * np.exp(-0.5 * ((H - 7.6) / 1.1) ** 2) + 0.12 * np.exp(-0.5 * ((H - 13.0) / 3.0) ** 2) \
        + 0.42 * np.exp(-0.5 * ((H - 19.2) / 1.9) ** 2)
    if weekend:
        s = s + 0.10 * np.exp(-0.5 * ((H - 11.5) / 3.0) ** 2)
    return s


def solar(clear):
    x = np.clip(np.sin(np.pi * (H - 5.6) / (19.25 - 5.6)), 0, None)
    x[(H < 5.6) | (H > 19.25)] = 0.0
    return 0.80 * clear * x ** 1.25


def duty(temp, weekday):
    lag = np.roll(temp, 3) * 0.55 + np.roll(temp, 2) * 0.25 + temp * 0.20
    d = np.clip((lag - 24.5) / 15.5, 0, 1) ** 1.25
    occ = np.ones(48)
    if weekday:
        occ[(H > 9) & (H < 15)] = 0.72
    occ[H < 6] = 0.85
    return d * occ


def response(design, s, eff=None):
    """per-household response at heat index s, kW by half-hour, before dilution (see knobs.EFF)"""
    e = K.EFF if eff is None else eff
    g = 0.45 + 0.55 * s
    sn = s ** e["ex"]
    r = np.zeros(48)
    hh = np.arange(48)
    if design == "A":
        r[(hh >= 30) & (hh < 42)] = -e["cA"] * g * (1.0 + 0.04 * np.cos(np.pi * (hh[(hh >= 30) & (hh < 42)] - 36) / 6))
        r[(hh >= 28) & (hh < 30)] = e["pre"] * g
        for k, f in enumerate([1.0, 0.58, 0.26, 0.10]):
            r[42 + k] += e["sA"] * f * sn + (e["tm"] if k == 0 else 0.0)
    elif design == "B":
        r[(hh >= 32) & (hh < 40)] = -e["cB"] * g * (1.0 + 0.04 * np.cos(np.pi * (hh[(hh >= 32) & (hh < 40)] - 36) / 4))
        r[(hh >= 30) & (hh < 32)] = e["pre"] * g
        for k, f in enumerate([1.0, 0.58, 0.26, 0.10]):
            r[40 + k] += e["sB"] * f * sn + (e["tm"] if k == 0 else 0.0)
    elif design == "C":
        r[(hh >= 32) & (hh < 40)] = -e["cC"] * g * (1.0 + 0.04 * np.cos(np.pi * (hh[(hh >= 32) & (hh < 40)] - 36) / 4))
        sh = ((hh >= 28) & (hh < 32)) | ((hh >= 40) & (hh < 44))
        r[sh] = -e["cS"] * g
        r[(hh >= 26) & (hh < 28)] = 0.4 * e["pre"] * g
        for k, f in enumerate([1.0, 0.5]):
            r[40 + k] += e["sC1"] * f * sn
        for k, f in enumerate([1.0, 0.58, 0.26, 0.10]):
            r[44 + k] += e["sC2"] * f * sn + (e["tm"] if k == 0 else 0.0)
    return r


class Premise:
    """one meter point's occupant(s) and loads: attributes of the people living there and of the house"""

    def __init__(self, size, ac, pvkw, e2, seed):
        self.size, self.ac, self.pvkw, self.e2 = size, ac, pvkw, e2
        self.rng = np.random.default_rng(seed)


def simulate(hh, ev, newp, occ, exch, tmax, tmin):
    """returns per premise key a dict of channel -> array (NDAY, 48) of average kW, and per household the arrays it
    needs for the truth (status by day)"""
    n = P.N_HH
    days = P.DAYS
    nd = len(days)
    # status of each household by day: 'D' on its design, 'H' Home Plan, '-' not present at the trial premise
    status = np.full((n, nd), "H", dtype=object)
    at_new = np.zeros((n, nd), dtype=bool)
    for i in range(n):
        a = hh["arm"][i]
        on = a in P.DESIGNS
        st = []
        for j, d in enumerate(days):
            st.append("D" if (on and P.trial_day(d)) else "H")
        for kind, d, _ in ev[i]:
            j0 = (d - P.DATA_FROM).days
            if kind in ("return", "lifesupport"):
                for j in range(j0, nd):
                    if st[j] == "D":
                        st[j] = "H"
            elif kind == "leave":
                for j in range(j0, nd):
                    st[j] = "-"
            elif kind in ("move_keep", "move_home", "return_move"):
                for j in range(j0, nd):
                    at_new[i, j] = True
                    if kind == "move_home":
                        st[j] = "H"
        status[i] = st
    # weather by day
    tr = []
    prev = WX.daily()[0][P.DATA_FROM - timedelta(1)]
    for d in days:
        tr.append(WX.trace(tmax[d], tmin[d], prev))
        prev = tmax[d]
    tr = np.array(tr)
    sday = np.array([WX.s_heat(tmax[d]) for d in days])
    wkd = np.array([P.workday(d) for d in days])
    weekend = np.array([d.weekday() >= 5 for d in days])
    clear = np.clip(1.0 - np.abs(np.random.default_rng(P.SEED + 5).normal(0, 0.07, nd)), 0.72, 1.0)
    resp_scale = {a: response(a, 1.0) for a in P.DESIGNS}   # noqa: F841 (kept for inspection)
    # what every household in the town shares on a given day and half-hour (cloud, wind, what is on television)
    rc = np.random.default_rng(P.SEED + 6)
    cday = rc.normal(0, K.COMMON["day"], nd)
    cbase = rc.normal(0, K.COMMON["base"], (nd, 48))
    cac = rc.normal(0, K.COMMON["ac"], (nd, 48))

    loads = {}
    meta = {}

    def run(key, prem, active_fn, pv_from=None):
        e1 = np.zeros((nd, 48))
        e2 = np.zeros((nd, 48)) if prem.e2 else None
        b1 = np.zeros((nd, 48)) if (prem.pvkw > 0 or pv_from is not None) else None
        r = prem.rng
        dayf = np.exp(cday + r.normal(0, K.NOISE["day"], nd))
        nb = np.exp(cbase + r.normal(0, K.NOISE["base"], (nd, 48)))
        na = np.exp(cac + r.normal(0, K.NOISE["ac"], (nd, 48)))
        hw = r.uniform(1.9, 3.6, nd)
        for j in range(nd):
            base = prem.size * base_shape(weekend[j]) * dayf[j] * nb[j] * 0.95
            ac = prem.ac * duty(tr[j], not weekend[j]) * na[j] * 0.62
            eff = active_fn(j)
            pvk = prem.pvkw if (pv_from is None or j >= pv_from) else 0.0
            pv = pvk * solar(clear[j])
            net = base + ac + eff - pv
            e1[j] = np.maximum(net, 0.0)
            if b1 is not None:
                b1[j] = np.maximum(-net, 0.0)
            if e2 is not None:
                on = np.zeros(48)
                k0, k1 = 46, 46 + int(round(hw[j] * 2))
                on[k0:min(k1, 48)] = 1.8
                if k1 > 48 and j + 1 < nd:
                    pass
                e2[j] += on
                if k1 > 48 and j + 1 < nd:
                    e2[j + 1, :k1 - 48] += 1.8
        loads[key] = {"E1": e1, "E2": e2, "B1": b1}

    for i in range(n):
        a = hh["arm"][i]
        pv_from = None
        if i in exch and exch[i]["why"] == "PV":
            pv_from = (exch[i]["date"] - P.DATA_FROM).days
        prem = Premise(hh["size"][i], hh["ac"][i], hh["pvkw"][i] if hh["pv0"][i] else (5.0 if pv_from is not None else 0.0),
                       hh["e2"][i], P.SEED * 1000 + i)

        def act(j, i=i, a=a):
            if a not in P.DESIGNS or status[i, j] != "D" or at_new[i, j] or not wkd[j]:
                return np.zeros(48)
            return hh["resp"][i] * hh["w"][i] / K.RESP_SHARE * response(a, sday[j])
        run(("nmi", hh["nmi"][i]), prem, act, pv_from=pv_from)
        meta[("nmi", hh["nmi"][i])] = {"hh": i, "role": "trial"}
    # new premises of in-town movers
    for i, rec in newp.items():
        a = hh["arm"][i]
        j0 = (rec["date"] - P.DATA_FROM).days
        prem = Premise(hh["size"][i], float(np.clip(hh["ac"][i] * 1.08, 2.4, 7.8)), 0.0, hh["e2"][i], P.SEED * 2000 + i)

        def act2(j, i=i, a=a, j0=j0):
            if j < j0 or a not in P.DESIGNS or status[i, j] != "D" or not wkd[j]:
                return np.zeros(48)
            return hh["resp"][i] * hh["w"][i] / K.RESP_SHARE * response(a, sday[j])
        run(("nmi", rec["nmi"]), prem, act2)
        meta[("nmi", rec["nmi"])] = {"hh": i, "role": "new_premise", "from": j0}
    # new occupants at vacated trial premises
    rng = np.random.default_rng(P.SEED + 77)
    for i, rec in occ.items():
        j0 = (rec["date"] - P.DATA_FROM).days
        prem = Premise(float(np.exp(rng.normal(0, 0.28))), float(np.clip(rng.normal(4.4, 1.0), 2.4, 7.8)),
                       hh["pvkw"][i] if hh["pv0"][i] else 0.0, hh["e2"][i], P.SEED * 3000 + i)
        run(("occ", hh["nmi"][i]), prem, lambda j: np.zeros(48))
        meta[("occ", hh["nmi"][i])] = {"hh": i, "role": "occupant", "from": j0}
    return loads, meta, status, at_new, sday, wkd
