"""The telemetry the platform's own client SDK reports, minute by minute.

The shortfall the standard defines is a difference of two medians, so the minute values are drawn
around a window median that the calibration has already fixed. The medians the goldens use are then
read back off the cut rows, never from the calibration.
"""
import datetime as dt
import random

import sim
import world as W

DAY_BASE = {"cable": 6150, "fibre": 7400, "fixed wireless": 4850}   # kbps on the reference band
MINUTE_SPREAD = {"cable": 196.0, "fibre": 138.0, "fixed wireless": 274.0}
ZONE_WINTER = 1                     # hours ahead of UTC before the last Sunday in March
ZONE_SUMMER = 2


def offset(day):
    """the hours local time runs ahead of UTC on a given local date"""
    return ZONE_SUMMER if day >= W.DST_SPRING else ZONE_WINTER


def utc_stamp(day, local_hour, minute):
    """the UTC instant of a local wall-clock minute"""
    naive = dt.datetime(day.year, day.month, day.day, local_hour, minute)
    return naive - dt.timedelta(hours=offset(day))


def minute_values(rng, median, n, spread):
    """n minute medians whose own median sits on the figure given, within a kbps or two"""
    half = n // 2
    out = []
    for i in range(half):
        d = abs(rng.gauss(0.0, spread)) + 1.0
        out.append(median - d)
        out.append(median + d * (0.86 + 0.3 * rng.random()))
    while len(out) < n:
        out.append(median + rng.gauss(0.0, spread * 0.4))
    vals = [int(round(v)) for v in out]
    # the band median is a whole kbps: with an even count the two middle values have to sum even,
    # so one of them moves by a single kbps, which is below the measurement's own resolution
    srt = sorted(range(len(vals)), key=lambda i: vals[i])
    a, b = srt[len(vals) // 2 - 1], srt[len(vals) // 2]
    if (vals[a] + vals[b]) % 2:
        vals[b] += 1 if vals[b] + 1 <= vals[srt[min(len(vals) - 1, len(vals) // 2 + 1)]] else -1
    rng.shuffle(vals)
    return vals


def median_of(vals):
    """the median the standard asks for: the middle of the sorted minute values"""
    v = sorted(vals)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def day_level(rng, path, day):
    """the path's own reference band median for the day, which is throughput, not shortfall"""
    code, peer, kind, cap, load, spread = path
    base = DAY_BASE[kind]
    season = 1.0 + 0.011 * (day.month - 2) / 2.0
    weekday = 1.0 - 0.006 * (1 if day.weekday() >= 5 else 0)
    return base * season * weekday * (1.0 + 0.004 * (day.toordinal() % 29 - 14) / 14.0) \
        * (0.981 + 0.038 * rng.random())


def detie(shorts):
    """nudge a window's shortfall down a kilobit where two evenings of one port and window tie

    A tie at the top of a cell would make the evening the cell reports a matter of convention. The
    measurement's own resolution is well above a kilobit, so moving one of them by that much is
    below anything the record could distinguish.
    """
    cells = {}
    for (code, day, hour), v in shorts.items():
        cells.setdefault((code, hour), []).append((day, v))
    for key, rows in cells.items():
        rows.sort(key=lambda r: (-r[1], r[0]))
        seen = {}
        for day, v in rows:
            while round(v) in seen:
                v -= 1.0
            seen[round(v)] = day
            shorts[(key[0], day, key[1])] = v
    return shorts


def build(qspread):
    """every minute row of the decision quarter, and every window median of all nine quarters"""
    rollup = []                     # (label, code, local day, hour, evening median, day median)
    minutes = []                    # (utc stamp, code, sessions, median kbps, p10, rebuffers)
    decided = {}
    for label, lo, hi in sim.quarters():
        if label != "2027Q1":
            continue
        for path in W.PATHS:
            rng = random.Random(W.SEED * 97 + sum(ord(c) for c in path[0] + label))
            for day in sim.evenings(lo, hi):
                for _, hour in W.WINDOWS:
                    decided[(path[0], day, hour)] = sim.shortfall(
                        rng, path, day, hour, qspread[label], label)
    decided = detie(decided)
    for label, lo, hi in sim.quarters():
        for path in W.PATHS:
            code = path[0]
            rng = random.Random(W.SEED * 97 + sum(ord(c) for c in code + label))
            lvl = random.Random(W.SEED * 13 + sum(ord(c) for c in code + label))
            for day in sim.evenings(lo, hi):
                dayband = day_level(lvl, path, day)
                shorts = {}
                for _, hour in W.WINDOWS:
                    v = sim.shortfall(rng, path, day, hour, qspread[label], label)
                    shorts[hour] = decided.get((code, day, hour), v) if label == "2027Q1" else v
                sessions_day = int(2100 * path[4] * (0.9 + 0.2 * lvl.random()))
                if label != "2027Q1":
                    for _, hour in W.WINDOWS:
                        rollup.append((label, code, day, hour,
                                       dayband - shorts[hour], dayband, sessions_day))
                    continue
                # the quarter the decision is about ships minute by minute; the pipeline's daily
                # rollup for it is read back off those same minutes once the collector's losses
                # have been taken out, in pack.rollup_from_panel
                for band, hours in (("day", range(W.DAY_BAND[0], W.DAY_BAND[1])),
                                    ("evening", range(W.EVENING_BAND[0], W.EVENING_BAND[1]))):
                    for h in hours:
                        tgt = dayband if band == "day" else dayband - shorts[h]
                        vals = minute_values(lvl, tgt, 60,
                                             MINUTE_SPREAD[path[2]] * (0.93 + 0.14 * lvl.random()))
                        for m, v in enumerate(vals):
                            minutes.append((utc_stamp(day, h, m), code,
                                            int(sessions_day * (0.55 if band == "day" else 1.0)
                                                * (0.9 + 0.2 * lvl.random())),
                                            v, int(v * (0.62 + 0.06 * lvl.random())),
                                            int(max(0, lvl.gauss(3.0 if band == "evening" else 1.2,
                                                                 1.6))), sessions_day))
    return minutes, rollup
