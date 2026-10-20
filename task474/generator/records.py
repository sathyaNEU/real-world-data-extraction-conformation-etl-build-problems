"""The records cut from the truth: hourly station volumes, each link's 48-hour classification count in its count
programme's own layout, and the terminals' gate transactions (the asks)."""
import datetime as dt

import numpy as np

import sources as S
import world as W

# share of a class's daily traffic in each hour (hour 0 = midnight to 1 a.m.)
PROFILE = {
    "P": np.array([.8, .5, .4, .4, .7, 1.8, 4.1, 6.6, 6.9, 5.4, 4.9, 5.2, 5.5, 5.6, 6.0, 6.8, 7.6, 7.9, 6.4, 4.9, 3.9,
                   3.2, 2.4, 1.5]),
    "SU": np.array([.6, .4, .4, .6, 1.4, 3.3, 5.8, 7.4, 8.0, 8.3, 8.4, 8.2, 7.8, 7.6, 7.2, 6.4, 5.3, 3.9, 2.6, 1.8,
                    1.3, 1.1, .9, .7]),
    "CU": np.array([1.4, 1.1, 1.0, 1.3, 2.2, 3.6, 5.1, 6.2, 6.9, 7.3, 7.5, 7.4, 7.2, 7.0, 6.7, 6.1, 5.2, 4.2, 3.2, 2.5,
                    2.1, 1.9, 1.7, 1.5])}
for _k in PROFILE:
    PROFILE[_k] = PROFILE[_k] / PROFILE[_k].sum()


def us_eastern_dst(d):
    """True on dates daylight time is in force (second Sunday of March to first Sunday of November)."""
    y = d.year
    mar = dt.date(y, 3, 8) + dt.timedelta((6 - dt.date(y, 3, 8).weekday()) % 7)
    nov = dt.date(y, 11, 1) + dt.timedelta((6 - dt.date(y, 11, 1).weekday()) % 7)
    return mar <= d < nov


def hourly(rng, day_volume, c, split):
    """24 x 2 integer hourly volumes (direction 1 and 2) for one day's class volume."""
    p = PROFILE[c] * rng.lognormal(0, .06, 24)
    p = p / p.sum()
    v = day_volume * p
    a = rng.binomial(np.maximum(np.round(v).astype(int), 0), split)
    return a, np.maximum(np.round(v).astype(int), 0) - a


def stations(rng, x):
    """[(station, date, hour_ending, direction, class, volume)] in local standard time, with each station's detector
    outages (whole days absent)."""
    rows = []
    for s, (route, rt, aadt, su, cu, cls) in W.STATIONS.items():
        out = set()
        for _ in range(int(rng.integers(0, 4))):
            a = int(rng.integers(0, 350))
            out |= set(range(a, a + int(rng.integers(1, 9))))
        split = float(rng.uniform(.47, .53))
        for i, d in enumerate(W.DAYS):
            if i in out:
                continue
            per = {c: hourly(rng, x["stations"][s][c][i], c, split) for c in W.CLASSES}
            for h in range(24):
                for di, dname in ((0, "1"), (1, "5")):
                    if cls:
                        for c, code in zip(W.CLASSES, ("1-3", "4-7", "8-13")):
                            rows.append((s, d, h + 1, dname, code, int(per[c][di][h])))
                    else:
                        rows.append((s, d, h + 1, dname, "ALL", int(sum(per[c][di][h] for c in W.CLASSES))))
    return rows


def counts(rng, x):
    """{link: {class: [48 hourly volumes per direction pair]}} for the two count days, local time."""
    out = {}
    for k in W.LINKS:
        i = W.DAYS.index(W.COUNT_DAY[k])
        split = float(rng.uniform(.44, .56))
        out[k] = {}
        for c in W.CLASSES:
            a1, b1 = hourly(rng, x["links"][k][c][i], c, split)
            a2, b2 = hourly(rng, x["links"][k][c][i + 1], c, split)
            out[k][c] = (np.concatenate([a1, a2]), np.concatenate([b1, b2]))
    return out


def gate_report(rng, g):
    """The terminals' daily gate reports: trucks in and out each day (a truck in the yard at midnight goes out the next
    day), and the container moves."""
    rows = []
    for t in W.TERMINALS:
        carry = 0
        for i, d in enumerate(W.DAYS):
            v = int(g[t][i])
            late = int(rng.binomial(v, .006))
            out = v - late + carry
            carry = late
            moves = int(round(v * float(rng.uniform(1.22, 1.34))))
            rows.append((d, t, v, out, moves))
    return rows
