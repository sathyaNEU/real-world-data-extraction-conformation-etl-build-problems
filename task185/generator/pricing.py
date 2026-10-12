"""The pricing manual's method, and every rung's construction, on the station record.

Counts: each season's heat days (35.0 C or more) and severe heat days (40.0 C or more) from the daily maxima on the
present instrument's basis. Lines: least squares of each count on the season's first year, 1965/66 to 2026/27.
Projection: each season's count plus the line's slope times the years to 2027/28, floored at zero. Burn: the average
payout per hectare of the projected seasons under the 2027/28 terms. Premium: the burn times 1.32, rounded once to the
whole dollar."""
import collections
import math

import numpy as np

import world as W

SEASONS = list(range(W.FIRST_SEASON, W.LAST_SEASON + 1))


def r_dollar(x):
    return int(math.floor(x + 0.5))


def bin_conversion(pairs):
    """mean probe-minus-glass difference at each glass reading, from (glass, probe) pairs"""
    b = collections.defaultdict(list)
    for g, p in pairs:
        b[g].append(p - g)
    return {g: float(np.mean(v)) for g, v in b.items()}


def converter(table):
    """per-reading conversion: the table's value at the reading, linear between the nearest tabulated readings"""
    xs = np.array(sorted(table))
    ys = np.array([table[x] for x in xs])

    def conv(g):
        return g + float(np.interp(g, xs, ys))
    return conv


def basis_series(mf, conv):
    """the daily maxima on the present instrument's basis: the probe from the change, the glass converted before it"""
    out = {}
    for d, g, p in zip(mf["days"], mf["glass"], mf["probe"]):
        if d >= W.CHANGE:
            out[d] = float(p)
        else:
            out[d] = conv(float(g))
    return out


def counts(series):
    heat, severe = {}, {}
    for s in SEASONS:
        vals = [series[d] for d in W.season_days(s)]
        heat[s] = sum(1 for v in vals if v >= W.HEAT_C - 1e-9)
        severe[s] = sum(1 for v in vals if v >= W.SEVERE_C - 1e-9)
    return heat, severe


def line(cnt):
    x = np.array(SEASONS, float)
    y = np.array([cnt[s] for s in SEASONS], float)
    b, a = np.polyfit(x, y, 1)
    return a, b


def payout(h, sv):
    return min(W.CAP, W.HEAT_RATE * max(0.0, h - W.DEDUCTIBLE_DAYS) + W.SEVERE_RATE * sv)


def price(heat, severe):
    ah, bh = line(heat)
    asv, bsv = line(severe)
    proj = {}
    for s in SEASONS:
        h = max(0.0, heat[s] + bh * (W.PRICED_SEASON - s))
        sv = max(0.0, severe[s] + bsv * (W.PRICED_SEASON - s))
        proj[s] = (h, sv, payout(h, sv))
    burn = float(np.mean([proj[s][2] for s in SEASONS]))
    return {
        "expected_heat": ah + bh * W.PRICED_SEASON,
        "expected_severe": asv + bsv * W.PRICED_SEASON,
        "slope_heat_decade": 10 * bh,
        "slope_severe_decade": 10 * bsv,
        "burn": burn,
        "premium_exact": burn * W.LOADING,
        "premium": r_dollar(burn * W.LOADING),
        "projected": proj,
        "floor_binds": any(heat[s] + bh * (W.PRICED_SEASON - s) < 0 or severe[s] + bsv * (W.PRICED_SEASON - s) < 0
                           for s in SEASONS),
    }


def uniform(u):
    def conv(g):
        return g + u
    return conv


def rung(mf, conv):
    heat, severe = counts(basis_series(mf, conv))
    return heat, severe, price(heat, severe)
