"""Simulate Tullan's tea category scan feed, store by week by item, from the world's laws.

Units are drawn as Poisson counts by inverse CDF from one fixed uniform per store, item and week
(common random numbers), so a change to a mean moves only the counts it touches."""
import datetime as dt

import numpy as np
from scipy.stats import poisson

import world as W
from stores import scan_ids

# units a week at store size 1, by price file
LEVEL = {
    "211401": {"P": 8.5, "C": 9.0, "V": 9.5}, "211402": {"P": 20.0, "C": 23.0, "V": 26.0},
    "211403": {"P": 6.5, "C": 7.0, "V": 7.5}, "211404": {"P": 5.5, "C": 5.0, "V": 4.0},
    "208115": {"P": 24.0, "C": 26.0, "V": 29.0}, "208116": {"P": 25.0, "C": 27.0, "V": 30.0},
    "208117": {"P": 42.0, "C": 46.0, "V": 50.0}, "208118": {"P": 13.0, "C": 14.0, "V": 15.0},
    "209331": {"P": 14.0, "C": 15.0, "V": 17.0}, "209332": {"P": 27.0, "C": 29.0, "V": 33.0},
    "214770": {"P": 28.0, "C": 25.0, "V": 22.0}, "214771": {"P": 3.5, "C": 3.0, "V": 2.5},
    "300812": {"P": 30.0, "C": 34.0, "V": 40.0}, "300814": {"P": 15.0, "C": 17.0, "V": 20.0},
    "216050": {"P": 16.0, "C": 15.0, "V": 14.0}, "216051": {"P": 16.0, "C": 15.0, "V": 14.0},
    "216052": {"P": 14.0, "C": 13.0, "V": 12.0},
}
# own-label 160s is set against Delahunt 160s in the same store, by price file
OL160_RATIO = {"P": 3.93, "C": 3.05, "V": 3.85}
GAPS = {("0203", dt.date(2026, 8, 10)), ("0203", dt.date(2026, 8, 17))}      # files not received
NOT_IN = {("0256", "BD26-04")}      # traded through its refit but could not run the leaflet cycle
# per-region multipliers on Delahunt 160s (D) and on own-label 160s in Premium (P) and Core (C) stores,
# solved so every graded figure sits off-centre inside its rounding bin (tune.py, solve3 and the fine pass)
DEFAULT_TUNE = {
    "P": {"DNE": 1.0286072284895091, "S": 0.8538788815783048, "WNW": 1.1611578383995536, "MSE": 1.5730218708851291},
    "C": {"DNE": 0.7658016678368719, "S": 1.0997552013505274, "WNW": 1.0464739407432353, "MSE": 0.6376457901844931},
    "D": {"DNE": 0.9986136945337483, "S": 1.00965275350298, "WNW": 1.1113493265071899, "MSE": 1.1186792054205512},
}


def ranged(store, item):
    return W.LINE[item]["express"] or store["format"] != "Express"


def store_means(stores, seed, tune):
    rng = np.random.default_rng(seed * 11 + 3)
    means = {}
    for s in stores:
        key = (s["no"], s["town"])
        reg = s["reg_event"]
        for item in W.LINE:
            if not ranged(s, item):
                continue
            aff = float(rng.lognormal(0, 0.15))
            if item == W.OL160:
                continue
            means[(key, item)] = LEVEL[item][s["pfile"]] * s["size"] * aff
        means[(key, W.DEL160)] *= tune["D"].get(reg, 1.0)
        d = means[(key, W.DEL160)]
        k = tune["P"].get(reg, 1.0) if s["pfile"] == "P" else tune["C"].get(reg, 1.0) if s["pfile"] == "C" else 1.0
        means[(key, W.OL160)] = d * OL160_RATIO[s["pfile"]] * float(rng.lognormal(0, 0.10)) * k
    return means


def event_map():
    out = {}
    for code, start, item, kind, val, label in W.EVENTS:
        for k in range(3):
            out[(start + dt.timedelta(days=7 * k), item)] = (code, kind, val, label)
    return out


def uniforms(stores, seed):
    rng = np.random.default_rng(seed * 101 + 7)
    return rng.random((len(stores), len(W.LINE), len(W.WEEKS)))


def simulate(stores, seed, tune=None):
    tune = tune or DEFAULT_TUNE
    means = store_means(stores, seed, tune)
    U = uniforms(stores, seed)
    ev = event_map()
    items = list(W.LINE)
    widx = {w: k for k, w in enumerate(W.WEEKS)}
    meta, lam, uu = [], [], []
    truth = []
    for w in W.WEEKS:
        xm = W.XMAS.get(w, 1.0)
        for si, s in enumerate(stores):
            sid = scan_ids(s, w)
            if sid is None or (sid, w) in GAPS:
                continue
            key = (s["no"], s["town"])
            mu = {i: means[(key, i)] * xm for i in items if (key, i) in means}
            reg = {i: W.price(i, s["pfile"], w) for i in mu}
            dprice, dref = {}, {}
            for i in list(mu):
                e = ev.get((w, i))
                if not e:
                    continue
                code, kind, val, label = e
                if (s["no"], code) in NOT_IN:
                    continue
                dp = W.deal_price(reg[i], kind, val)
                dprice[i], dref[i] = dp, code
                base_i = mu[i]
                mu[i] = base_i * (1 + W.lift(W.depth(reg[i], kind, val)))
                pair = W.OWN.get(W.LINE[i]["bags"])
                if pair and pair in mu and dp <= reg[pair]:
                    ol = mu[pair]
                    mu[pair] = ol * (1 - W.SWITCH_LOSS)
                    mu[i] += W.SWITCH_GAIN * ol
                    truth.append((w, key, i, "cross"))
            for ii, i in enumerate(items):
                if i not in mu:
                    continue
                meta.append((w, sid, i, reg[i], dprice.get(i), dref.get(i)))
                lam.append(mu[i])
                uu.append(U[si, ii, widx[w]])
    units = poisson.ppf(np.array(uu), np.array(lam)).astype(int)
    rows = [(m[0], m[1], m[2], int(u), m[3], m[4], m[5]) for m, u in zip(meta, units)]
    return rows, means, truth
