"""Each hospital-day's true state (full or not) over the season, and what each feed flags on it.

A region's strain follows the respiratory season (light in November, rising through December, highest in the
first half of January); each hospital sits a little above or below its region; a full day tends to follow a full
day. Each feed then flags each hospital-day with its own chance given the day's state alone, the same everywhere:
the feeds never see one another and nothing else about the day moves them.
"""
import datetime as dt

import numpy as np

import world as W

TRUTH_SEED = 5081


def days(a=W.SEASON_START, b=W.SEASON_END):
    return [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]


def season_shape(d):
    """the season's strain relative to the 28-day window's mean (1.0)"""
    t = (d - W.WINDOW_START).days
    if t < -35:
        return 0.30
    if t < 0:
        return 0.30 + 0.62 * (t + 35) / 35
    return 1.0 + 0.10 * np.sin(np.pi * t / 27.0)


def states(hosp, seed=TRUTH_SEED):
    """the true state of every hospital-day of the season: {(licence, date): 0 or 1}"""
    rng = np.random.default_rng(seed)
    target = {r[0]: r[4] for r in W.REGIONS}
    D = days()
    Z = {}
    for h in hosp:
        eff = rng.normal(0.0, 0.05)
        prev = 0
        for d in D:
            p = float(np.clip(target[h["region"]] * season_shape(d) / 1.033 + eff, 0.01, 0.97))
            z = prev if rng.random() < 0.45 else int(rng.random() < p)
            Z[(h["licence"], d)] = z
            prev = z
    return Z


def flags(hosp, Z, seed=TRUTH_SEED + 1):
    """what each feed flags on each hospital-day: {(licence, date): (A, B, C)}; A is None where the census
    survey has no report (the two holidays, for about half the hospitals)"""
    rng = np.random.default_rng(seed)
    s, f = np.array(W.FEED_S), np.array(W.FEED_F)
    skip = {h["licence"]: rng.random() < 0.5 for h in hosp}
    out = {}
    for h in hosp:
        for d in days():
            z = Z[(h["licence"], d)]
            y = (rng.random(3) < (s if z else f)).astype(int)
            a = None if (d in W.HOLIDAYS and skip[h["licence"]]) else int(y[0])
            out[(h["licence"], d)] = (a, int(y[1]), int(y[2]))
    return out
