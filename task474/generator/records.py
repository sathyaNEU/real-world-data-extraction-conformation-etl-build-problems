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


MOVES = ("DROP EXPORT", "PICK IMPORT", "DROP EMPTY", "PICK EMPTY")
LANES = {"B20": (6, 4), "B30": (8, 5), "B40": (5, 3)}


def gates(rng, g):
    """Gate transaction rows, one per container transaction, as each terminal's gate system writes them: Berth 20's
    in-gate kiosks on standard time all year; Pacific Gateway keeping a transaction keyed to the wrong truck and voided
    beside the re-keyed one; Berth 40 writing a truck's run to the on-dock rail ramp as two legs through the ramp
    gate."""
    tags = sorted({v["tag"] for v in g["visits"]})
    rows = []
    tid = 4400000
    for v in sorted(g["visits"], key=lambda v: (v["tin"], v["tag"])):
        ni, no = LANES[v["term"]]
        il, ol = "IG%02d" % int(rng.integers(1, ni + 1)), "OG%02d" % int(rng.integers(1, no + 1))
        tin, out = v["tin"], v["tout"]
        if v["term"] == "B20" and us_eastern_dst(tin.date()):
            tin = tin - dt.timedelta(hours=1)
        cont = lambda: "%s%07d" % (("MSKU", "TGHU", "CMAU", "OOLU", "HLXU", "MEDU", "TCNU", "BEAU")[int(rng.integers(0, 8))],
                                   int(rng.integers(0, 9999999)))
        if v["ramp"]:
            a, b = v["ramp"]
            tid += int(rng.integers(1, 9))
            rows.append((tid, v["term"], v["tag"], il, tin, "RG1", a, "PICK IMPORT", cont()))
            tid += int(rng.integers(1, 9))
            rows.append((tid, v["term"], v["tag"], "RG1", b, ol, out, "DROP EMPTY", cont()))
            continue
        n = 2 if v["dual"] else 1
        for j in range(n):
            mv = MOVES[int(rng.choice(4, p=[.33, .37, .14, .16]))] if n == 1 else \
                (("DROP EXPORT", "PICK IMPORT")[j] if rng.random() < .7 else MOVES[int(rng.integers(0, 4))])
            c = cont()
            if v["term"] == "B30" and j == 0 and rng.random() < .032:
                # keyed first to another truck's tag and voided a few minutes later
                tid += int(rng.integers(1, 5))
                wrong = tags[int(rng.integers(0, len(tags)))]
                rows.append((tid, v["term"], wrong, il, tin, ol, tin + dt.timedelta(seconds=int(rng.integers(90, 560))),
                             mv, c))
            tid += int(rng.integers(1, 9))
            rows.append((tid, v["term"], v["tag"], il, tin, ol, out, mv, c))
            tin = tin + dt.timedelta(seconds=int(rng.integers(20, 95)))
    return rows
