"""task131 generator: weather at Murrandi Aero, 1 October 2025 to 31 March 2026.

Daily maxima follow the season; one heatwave (19 to 25 January) and a second hot spell (10 and 11 February) carry
the summer's hottest workdays, and no other workday reaches 40 degrees. The half-hourly trace is built from each
day's minimum and maximum with an evening that stays warm in proportion to the day's heat."""
from datetime import date, timedelta

import numpy as np

import params as P

W0, W1 = date(2025, 10, 1), date(2026, 3, 31)
WDAYS = [W0 + timedelta(i) for i in range((W1 - W0).days + 1)]

# the hot spells, set by hand (workday maxima average the design day's 44.6)
FIXED = {
    date(2026, 1, 16): 39.4, date(2026, 1, 17): 41.8, date(2026, 1, 18): 43.0,
    date(2026, 1, 19): 44.2, date(2026, 1, 20): 44.9, date(2026, 1, 21): 45.3, date(2026, 1, 22): 44.6,
    date(2026, 1, 23): 43.7, date(2026, 1, 24): 44.1, date(2026, 1, 25): 42.6, date(2026, 1, 26): 39.6,
    date(2026, 1, 27): 36.1,
    date(2026, 2, 8): 38.4, date(2026, 2, 9): 39.7, date(2026, 2, 10): 44.5, date(2026, 2, 11): 45.0,
    date(2026, 2, 12): 38.2,
}
HOT_WORKDAYS = [date(2026, 1, 19), date(2026, 1, 20), date(2026, 1, 21), date(2026, 1, 22), date(2026, 1, 23),
                date(2026, 2, 10), date(2026, 2, 11)]
MEAN_MAX = {10: 30.2, 11: 33.1, 12: 35.0, 1: 35.9, 2: 35.4, 3: 33.0}


def daily(seed=P.SEED):
    rng = np.random.default_rng(seed * 7 + 1)
    tmax, tmin = {}, {}
    prev = 32.0
    for d in WDAYS:
        if d in FIXED:
            x = FIXED[d]
        else:
            m = MEAN_MAX[d.month]
            x = 0.45 * prev + 0.55 * m + rng.normal(0, 2.6)
            if P.workday(d) and x >= 39.95 and d.month in (11, 12, 1, 2):
                x = 39.95 - abs(rng.normal(0.9, 0.7))
            x = min(x, 42.4) if d.month in (10, 3) else x
            x = max(x, 24.5)
        x = round(x, 1)
        tmax[d] = x
        prev = x
        gap = 12.8 + rng.normal(0, 1.6) - (1.6 if x >= 43 else 0)
        tmin[d] = round(x - gap, 1)
    return tmax, tmin


def s_heat(t):
    """0 at 33 degrees, 1 from 42: how far the day's heat drives the trial response"""
    return float(np.clip((t - 33.0) / 9.0, 0.0, 1.0))


def trace(tmax, tmin, prev_tmax):
    """half-hourly air temperature for one day from its minimum (about 05:30) and maximum (about 15:00)"""
    h = (np.arange(48) + 0.5) / 2.0
    out = np.empty(48)
    warm = 0.28 + 0.012 * max(0.0, tmax - 30.0)          # how warm the evening stays
    for i, x in enumerate(h):
        if x < 5.5:
            y = (prev_tmax - tmin) * (0.32 - 0.32 * x / 5.5) * 0.9 + tmin
        elif x <= 15.0:
            f = 0.5 - 0.5 * np.cos(np.pi * (x - 5.5) / 9.5)
            y = tmin + (tmax - tmin) * f
        else:
            f = np.exp(-(x - 15.0) / (6.5 + 10 * warm))
            y = tmin + (tmax - tmin) * (warm + (1 - warm) * f)
        out[i] = y
    return out
