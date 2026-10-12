"""The procedure's arithmetic, shared by the generator's clearances and its analysis: hourly winds from the
station's 5-minute records, odor events from complaint rows, the upwind check, and the comparisons the rungs make."""
import datetime as dt
import math
import re

import core

FKEYS = core.FKEYS


def hour_wind(recs, held=None, method="vector"):
    """recs: [(minute, ws, wd, sigma, qc)] for one PST clock hour. held: a set of minutes the vane was held (excluded
    from a usable wind, as the golden reads the maintenance log); returns (speed, dir, n_used) or None when fewer
    than nine usable records remain."""
    use = [r for r in recs if r[4] == "V" and (held is None or r[0] not in held)]
    if len(use) < core.MIN_RECORDS:
        return None
    if method == "vector":
        u = sum(-r[1] * math.sin(math.radians(r[2])) for r in use) / len(use)
        v = sum(-r[1] * math.cos(math.radians(r[2])) for r in use) / len(use)
        sp = math.hypot(u, v)
        dr = (math.degrees(math.atan2(-u, -v)) + 360.0) % 360.0
        return sp, dr, len(use)
    sp = sum(r[1] for r in use) / len(use)
    dr = sum(r[2] for r in use) / len(use)
    return sp, dr, len(use)


def norm_address(a):
    a = a.upper().strip()
    a = re.sub(r"\s+", " ", a)
    a = re.sub(r"\b(APT|UNIT)\s*", "#", a)
    a = a.replace("# ", "#")
    for long, short in ((" STREET", " ST"), (" AVENUE", " AVE"), (" DRIVE", " DR"), (" ROAD", " RD")):
        a = re.sub(long + r"\b", short, a)
    a = re.sub(r"\s*#", " #", a)
    return a


def events(rows):
    """rows: dicts with household, noticed (local), lat, lon. The procedure: a household's complaints whose noticed
    time falls within two hours of the household's first complaint in the event are one event."""
    out = []
    by_h = {}
    for r in sorted(rows, key=lambda r: (r["household"], r["noticed"])):
        by_h.setdefault(r["household"], []).append(r)
    for hh, rr in by_h.items():
        first = None
        for r in rr:
            if first is None or r["noticed"] - first["noticed"] > core.EVENT_WINDOW:
                first = r
                out.append(dict(household=hh, noticed=r["noticed"], lat=r["lat"], lon=r["lon"], n=1))
            else:
                out[-1]["n"] += 1
    out.sort(key=lambda e: (e["noticed"], e["household"]))
    return out


def is_upwind(f, lat, lon, w, bearing=core.bearing_deg, deg=core.UPWIND_DEG):
    if w is None or w[0] < core.CALM_MS:
        return False
    b = bearing(lat, lon, core.FAC[f]["lat"], core.FAC[f]["lon"])
    return core.angdiff(w[1], b) <= deg


def event_hour(e, convert=True):
    t = core.local_to_pst(e["noticed"]) if convert else e["noticed"]
    return t.date(), t.hour


def station_hour(d, h, convert=True):
    """The station's hour key for local clock hour h on local date d (h may run past the day)."""
    t = dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=h)
    if convert:
        t = core.local_to_pst(t)
    return t.date(), t.hour


def compare(evs, hourly, mode="same", days=None, convert=True, bearing=core.bearing_deg, center=False, deg=core.UPWIND_DEG):
    """Per facility: O (events it lay upwind of) and E (the expected count under the comparison). The pools are local
    clock hours on the season's local days, each read at the station's matching standard-time hour.
    mode: 'count' (no base), 'all' (each household's share of all season hours), 'same' (the event's clock hour on
    the season's other days with a usable wind), 'month' (same hour, same calendar month), 'pm1' (the hour and the
    hours either side), 'incl' (the season's days including the event's own)."""
    days = days or core.SEASON_DAYS
    O = {f: 0 for f in FKEYS}
    E = {f: 0.0 for f in FKEYS}
    cache = {}
    for e in evs:
        lat, lon = (core.STATION if center else (e["lat"], e["lon"]))
        d0, h0 = event_hour(e, convert)
        ld, lh = e["noticed"].date(), e["noticed"].hour
        w = hourly.get((d0, h0))
        for f in FKEYS:
            O[f] += is_upwind(f, lat, lon, w, bearing, deg)
            if mode == "count":
                continue
            key = (f, round(lat, 6), round(lon, 6), mode, lh if mode != "all" else -1, ld.month if mode == "month" else 0,
                   ld if mode in ("same", "month", "pm1") else None)
            if key in cache:
                E[f] += cache[key]
                continue
            if mode == "all":
                pool = [station_hour(d, h, convert) for d in days for h in range(24)]
            elif mode == "same":
                pool = [station_hour(d, lh, convert) for d in days if d != ld]
            elif mode == "incl":
                pool = [station_hour(d, lh, convert) for d in days]
            elif mode == "month":
                pool = [station_hour(d, lh, convert) for d in days if d != ld and d.month == ld.month]
            elif mode == "pm1":
                pool = [station_hour(d, lh + k, convert) for d in days if d != ld for k in (-1, 0, 1)]
            vals = [is_upwind(f, lat, lon, hourly.get(p), bearing, deg) for p in pool if hourly.get(p) is not None]
            v = sum(vals) / len(vals)
            cache[key] = v
            E[f] += v
    return O, E


def pick(O, E, metric="excess"):
    if metric == "count":
        sc = {f: O[f] for f in FKEYS}
    elif metric == "ratio":
        sc = {f: O[f] / E[f] if E[f] else 0.0 for f in FKEYS}
    else:
        sc = {f: O[f] - E[f] for f in FKEYS}
    order = sorted(FKEYS, key=lambda f: -sc[f])
    return order, sc
