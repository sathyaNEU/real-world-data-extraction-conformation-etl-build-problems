"""The business improvement district's four pedestrian sensors: the hourly counts as the feed delivers them (in UTC,
every hour of the season), the fault log the supplier publishes beside them, the sensor register and the quarter's
trading hours.

A sensor head counts in both directions. When one direction fails, or the unit is retrying its connection, the feed
still publishes a count for every hour; the count is simply a part of the footfall that passed. The supplier's fault
log is the only record of which hours those were.
"""
import datetime as dt

import numpy as np

import world as W

COUNTS = "harbourgate_footfall_hourly.csv"
AVAIL = "footfall_sensor_availability.csv"
SENSREG = "footfall_sensor_register.csv"
TRADING = "harbourgate_trading_hours.csv"

BASE = {"FG-01": 1242.24, "FG-02": 809.43, "FG-04": 561.82, "FG-07": 450.49}
HOUR_SHAPE = [0.10, 0.06, 0.04, 0.05, 0.22, 0.40, 0.55, 0.80, 1.00, 1.05, 1.10, 1.20,
              1.45, 1.35, 1.25, 1.20, 1.30, 1.50, 1.40, 1.15, 1.05, 0.95, 0.70, 0.35]
# each sensor's faults: (season index, first day offset, days, the share of footfall the head still counted, reason)
FAULTS = {
    "FG-01": [(0, 44, 12, 0.46, "west head not counting, awaiting replacement"),
              (1, 102, 9, 0.52, "power supply fault, unit resetting")],
    "FG-02": [(0, 12, 14, 0.38, "connection retries"),
              (1, 61, 17, 0.44, "colonnade resurfacing, one head obstructed")],
    "FG-04": [(0, 96, 11, 0.49, "one direction only after a strike on the housing"),
              (1, 23, 21, 0.33, "lane works, head realigned part way through")],
    "FG-07": [(0, 130, 16, 0.57, "firmware rollback, one direction only"),
              (1, 7, 10, 0.41, "connection retries")],
}


def rng(k):
    return np.random.default_rng([W.SEED, 7, k, W.NUDGE])


def trading_open(day, hour):
    """Is the quarter trading at this local hour of this weekday? TRADING holds the opening hour and the closing
    hour counted past midnight, so Saturday runs 04:00 to 05:00 the next morning."""
    o, c = W.TRADING[day]
    if o <= hour < min(c, 24):
        return True
    prev = (day - 1) % 7
    po, pc = W.TRADING[prev]
    return pc > 24 and hour < pc - 24


def fault_hours(sid):
    """Every local hour the supplier's fault log covers, with the share of footfall the head still counted."""
    out = {}
    for si, off, days, share, _why in FAULTS[sid]:
        d0 = W.SEASONS[si][0] + dt.timedelta(days=off)
        for i in range(days):
            d = d0 + dt.timedelta(days=i)
            for h in range(24):
                out[(d, h)] = share
    return out


def availability_rows():
    rows = [("sensor_id", "fault_from", "fault_to", "fault")]
    for sid in W.SENSORS:
        for si, off, days, _share, why in FAULTS[sid]:
            d0 = W.SEASONS[si][0] + dt.timedelta(days=off)
            d1 = d0 + dt.timedelta(days=days)
            rows.append([sid, d0.isoformat() + "T00:00", d1.isoformat() + "T00:00", why])
    return rows


def register_rows():
    installed = {"FG-01": "2023-03-14", "FG-02": "2023-03-14", "FG-04": "2024-02-27", "FG-07": "2023-11-06"}
    rows = [("sensor_id", "location_name", "position", "installed_on", "feed_timezone")]
    for sid, (loc, pos) in W.SENSORS.items():
        rows.append([sid, loc, pos, installed[sid], "UTC"])
    return rows


def trading_rows():
    """The quarter's trading day. A day that trades past midnight closes on the following day, which the schedule
    names, because the fish market opens at four and the licensed premises keep their terminal hours."""
    rows = [("day_of_week", "opens_local", "closes_local", "closes_on")]
    for d in range(7):
        o, c = W.TRADING[d]
        rows.append([W.DAYS[d], "%02d:00" % o, "%02d:00" % (c % 24), W.DAYS[(d + 1) % 7] if c >= 24 else W.DAYS[d]])
    return rows


def counts():
    """The hourly feed. One row per sensor and hour of the season, stamped in UTC; local time runs an hour ahead
    through both seasons. An hour the quarter was closed carries a genuine count, usually zero or near it. An hour
    the fault log covers carries the part of the footfall the head was still counting."""
    out = []
    for k, sid in enumerate(sorted(W.SENSORS)):
        g = rng(k + 1)
        faults = fault_hours(sid)
        for si in range(len(W.SEASONS)):
            trend = 1.0 + 0.045 * si
            for d in W.season_days(si):
                dow = d.weekday()
                wk = 1.22 if dow >= 4 else (0.95 if dow <= 2 else 1.0)
                for h in range(24):
                    if trading_open(dow, h):
                        mu = BASE[sid] * HOUR_SHAPE[h] * wk * trend
                        n = int(round(g.gamma(mu / 26.0, 26.0)))
                    else:
                        n = int(g.poisson(2.4))
                    share = faults.get((d, h))
                    if share is not None:
                        n = int(round(n * share))
                    local = dt.datetime.combine(d, dt.time(hour=h))
                    out.append((sid, (local - dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), n))
    out.sort(key=lambda r: (r[1], r[0]))
    return out


def count_rows(rows):
    return [("sensor_id", "count_hour_utc", "pedestrians")] + [list(r) for r in rows]


def per_trading_hour(rows):
    """The ask: each sensor's pedestrians per trading hour, by season. The hours the fault log covers are out of the
    count and out of the hours, because what the head reported for them is a part of the footfall that passed. The
    feed's stamps are UTC and the trading hours are local."""
    tot = {}
    faults = {sid: fault_hours(sid) for sid in W.SENSORS}
    for sid, stamp, n in rows:
        local = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=1)
        if not trading_open(local.weekday(), local.hour):
            continue
        if (local.date(), local.hour) in faults[sid]:
            continue
        si = 0 if local.date() <= W.SEASONS[0][1] else 1
        tot.setdefault((sid, si), [0, 0])[0] += n
    for sid in sorted(W.SENSORS):
        for si in range(len(W.SEASONS)):
            hrs = sum(1 for d in W.season_days(si) for h in range(24)
                      if trading_open(d.weekday(), h) and (d, h) not in faults[sid])
            tot.setdefault((sid, si), [0, 0])[1] = hrs
    return {k: v[0] / v[1] for k, v in tot.items()}
