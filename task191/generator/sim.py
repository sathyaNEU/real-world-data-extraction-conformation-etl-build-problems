"""How the panel's minute values come to exist, and what an evening's shortfall is.

Nothing in this build is congested. Every path's evening delivered bitrate sits below its daytime
bitrate because evening demand is higher everywhere, and the spread of that shortfall across paths,
evenings and windows is the measurement's own. A quarter's worst cell is therefore a maximum over
seven paths, ninety evenings and three windows, and that is what its reference has to be.
"""
import datetime as dt
import math
import random

import world as W

SEASON = {1: 1.14, 2: 1.11, 3: 1.02, 4: 0.93, 5: 0.86, 6: 0.82,
          7: 0.80, 8: 0.84, 9: 0.92, 10: 1.01, 11: 1.09, 12: 1.16}
WINDOW_LIFT = {19: 0.88, 20: 1.00, 21: 0.95}
BASE = 96.0                  # kbps, the shortfall an average path shows on an average evening
SPREAD = 84.0                # kbps, the evening to evening spread of that shortfall


def quarters():
    """every quarter the pack covers, oldest first, as (label, first day, last day)"""
    out = []
    d = W.PRIOR_FROM
    while d <= W.Q_TO:
        q = (d.month - 1) // 3 + 1
        lo = dt.date(d.year, 3 * q - 2, 1)
        hi = dt.date(d.year + (1 if q == 4 else 0), 1 if q == 4 else 3 * q + 1, 1) - dt.timedelta(days=1)
        out.append(("%dQ%d" % (d.year, q), lo, hi))
        d = hi + dt.timedelta(days=1)
    return out


def evenings(lo, hi):
    d = lo
    while d <= hi:
        yield d
        d += dt.timedelta(days=1)


TAIL_P = 0.022               # the share of windows the measurement spreads a little wider on
TAIL_SCALE = 1.45


def in_maintenance(code, day):
    return code == W.MAINTENANCE[0] and W.MAINTENANCE[1] <= day <= W.MAINTENANCE[2]


def shortfall(rng, path, day, hour, qspread, label=None):
    """one window's shortfall in kbps: the path's level, the quarter's, the season's and the noise.

    The noise is heavy tailed, as a minute-sampled quality measure is: most windows sit close to the
    path's own level and a few per cent sit far out, which is why a quarter's worst window is a long
    way above its own mean and why the worst window of one quarter is a long way from the next.
    """
    code, peer, kind, cap, load, spread = path
    mu = BASE * load * SEASON[day.month] * WINDOW_LIFT[hour] * W.LOAD_TREND.get(label, 1.0)
    sd = SPREAD * spread * qspread * (TAIL_SCALE if rng.random() < TAIL_P else 1.0)
    v = mu + rng.gauss(0.0, sd)
    if in_maintenance(code, day):
        v *= W.MAINTENANCE_LIFT         # the port is running on one card
    return v


def cells(qspread_by_quarter, seed_shift=0):
    """every (quarter, path, evening, window) shortfall the pack's own record implies"""
    out = {}
    for label, lo, hi in quarters():
        rows = []
        for path in W.PATHS:
            rng = random.Random(W.SEED * 97 + seed_shift + sum(ord(c) for c in path[0] + label))
            for day in evenings(lo, hi):
                for _, hour in W.WINDOWS:
                    rows.append((path[0], day, hour,
                                 shortfall(rng, path, day, hour, qspread_by_quarter[label], label)))
        out[label] = rows
    return out


def calibrate(targets, rounds=46):
    """nudge each quarter's measurement spread until its worst window lands on that quarter's target

    The level is demand and is left alone: it moves with the season and with each path's own load.
    What a quarter's worst window turns on is how widely the measurement spread that quarter, which
    is what this solves for.
    """
    qspread = {}
    for label, lo, hi in quarters():
        lo_s, hi_s = 0.45, 2.40
        for _ in range(rounds):
            mid = (lo_s + hi_s) / 2.0
            worst = 0.0
            for path in W.PATHS:
                rng = random.Random(W.SEED * 97 + sum(ord(c) for c in path[0] + label))
                for day in evenings(lo, hi):
                    for _, hour in W.WINDOWS:
                        if in_maintenance(path[0], day):
                            shortfall(rng, path, day, hour, mid, label)
                            continue      # the target is the record the framework leaves standing
                        v = shortfall(rng, path, day, hour, mid, label)
                        if v > worst:
                            worst = v
            if worst < targets[label]:
                lo_s = mid
            else:
                hi_s = mid
        qspread[label] = (lo_s + hi_s) / 2.0
    return qspread
