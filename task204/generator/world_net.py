"""Carvale light rail: stations, the GTFS timetable for three service periods, vehicle blocks.

Times are seconds after midnight of the service day (GTFS convention, may exceed 86400).
"""
import datetime as dt
import math

import numpy as np

import params as P

LINE_STOPS = {
    "EL": [s[0] for s in P.EAST],
    "NL": [s[0] for s in P.NORTH],
}
STN = {}
for code, name, x, y in P.EAST + P.NORTH:
    STN[code] = {"code": code, "name": name, "x": x, "y": y}

# Run time (seconds) from each stop to the next, outbound order; inbound uses the reverse with small asymmetry.
RUN = {
    ("EL", "WG", "CS"): 276, ("EL", "CS", "UY"): 168, ("EL", "UY", "MB"): 174, ("EL", "MB", "FG"): 102,
    ("EL", "FG", "CB"): 108, ("EL", "MB", "CB"): 192, ("EL", "CB", "AR"): 180, ("EL", "AR", "RV"): 186,
    ("EL", "RV", "PG"): 180,
    ("NL", "CS", "SH"): 156, ("NL", "SH", "KP"): 144, ("NL", "KP", "HL"): 156, ("NL", "HL", "LM"): 162,
}
DWELL = 30
LAYOVER = 300

# Headway tables: list of (start_sec, end_sec, headway_sec) for departures from each origin terminus.
def _hw(rows):
    out = []
    for a, b, h in rows:
        ha, ma = a
        hb, mb = b
        out.append((ha * 3600 + ma * 60, hb * 3600 + mb * 60, h * 60))
    return out

HEADWAYS = {
    ("W", "WKD"): _hw([((5, 32), (6, 30), 15), ((6, 30), (9, 0), 8), ((9, 0), (15, 0), 12),
                      ((15, 0), (18, 30), 8), ((18, 30), (21, 0), 12), ((21, 0), (24, 50), 15)]),
    ("S", "WKD"): _hw([((5, 32), (6, 30), 15), ((6, 30), (9, 0), 8), ((9, 0), (15, 0), 10),
                      ((15, 0), (18, 30), 8), ((18, 30), (21, 0), 12), ((21, 0), (24, 50), 15)]),
    ("W", "SAT"): _hw([((6, 15), (8, 0), 15), ((8, 0), (21, 0), 12), ((21, 0), (24, 50), 15)]),
    ("S", "SAT"): _hw([((6, 15), (8, 0), 15), ((8, 0), (21, 0), 12), ((21, 0), (24, 50), 15)]),
    ("W", "SUN"): _hw([((7, 10), (24, 20), 15)]),
    ("S", "SUN"): _hw([((7, 10), (24, 20), 15)]),
}
# The two termini of each line start at slightly different minutes.
ORIGIN_OFFSET = {("EL", 0): 0, ("EL", 1): 240, ("NL", 0): 120, ("NL", 1): 360}


def stops_for(line, period):
    seq = list(LINE_STOPS[line])
    if line == "EL" and period != "S26":
        seq.remove("FG")
    return seq


def run_time(line, a, b, inbound):
    key = (line, a, b) if (line, a, b) in RUN else (line, b, a)
    t = RUN[key]
    return t + (6 if inbound else 0)


def build_timetable(rng):
    """Every trip of every service: dict with trip_id, line, period, daytype, direction, stops [(code, arr, dep)]."""
    trips = []
    used_ids = set()
    for period in ("W25", "W26", "S26"):
        tab = "S" if period == "S26" else "W"
        for daytype in ("WKD", "SAT", "SUN"):
            for line in ("EL", "NL"):
                seq_out = stops_for(line, period)
                for direction in (0, 1):            # 0 outbound (away from Centre Square for NL; east for EL), 1 inbound
                    seq = seq_out if direction == 0 else list(reversed(seq_out))
                    if line == "EL" and direction == 0:
                        seq = seq_out                # WG -> PG is outbound (east)
                    off = ORIGIN_OFFSET[(line, direction)]
                    day_trips = []
                    for (a, b, h) in HEADWAYS[(tab, daytype)]:
                        t = a + off
                        k_band = 0
                        peak = daytype == "WKD" and h <= 8 * 60
                        while t < b + off:
                            stimes = []
                            cur = t
                            for i, s in enumerate(seq):
                                if i == 0:
                                    stimes.append((s, cur, cur))
                                else:
                                    cur += run_time(line, seq[i - 1], s, direction == 1)
                                    stimes.append((s, cur, cur + DWELL))
                                    cur = cur + DWELL
                            # peak short turns on the Eastline: every other eastbound trip turns at Cobb Street; every
                            # other westbound trip starts at Ashford Road in the morning peak, at Cobb Street in the evening
                            if line == "EL" and peak and k_band % 2 == 1:
                                codes = [x[0] for x in stimes]
                                if direction == 0:
                                    stimes = stimes[:codes.index("CB") + 1]
                                else:
                                    turn = "AR" if a < 12 * 3600 else "CB"
                                    stimes = stimes[codes.index(turn):]
                            k_band += 1
                            day_trips.append(stimes)
                            t += h
                    # depot pull-outs and pull-ins: the first and last trips of the day start or end at the depot
                    depot = {"EL": "UY", "NL": "KP"}[line]
                    n_out, n_in = {("EL", 0): (3, 2), ("EL", 1): (2, 3), ("NL", 0): (2, 1), ("NL", 1): (1, 2)}[(line, direction)]
                    for k, stimes in enumerate(day_trips):
                        codes = [x[0] for x in stimes]
                        if depot in codes:
                            di = codes.index(depot)
                            if k < n_out and di > 0:
                                stimes = stimes[di:]
                            elif k >= len(day_trips) - n_in and di < len(stimes) - 1:
                                stimes = stimes[:di + 1]
                        last = stimes[-1]
                        stimes = stimes[:-1] + [(last[0], last[1], last[1])]
                        first = stimes[0]
                        stimes = [(first[0], first[2], first[2])] + stimes[1:]
                        while True:
                            tid = str(int(rng.integers(30000000, 39999999)))
                            if tid not in used_ids:
                                used_ids.add(tid)
                                break
                        trips.append({"trip_id": tid, "line": line, "period": period, "daytype": daytype,
                                      "direction": direction, "stops": stimes})
    _assign_blocks(trips, rng)
    return trips


def _assign_blocks(trips, rng):
    """A vehicle takes a trip from the terminus it waits at once its layover is done (first in, first out)."""
    groups = {}
    for tr in trips:
        groups.setdefault((tr["line"], tr["period"], tr["daytype"]), []).append(tr)
    for (line, period, daytype), lst in sorted(groups.items()):
        lst.sort(key=lambda r: (r["stops"][0][2], r["direction"]))
        waiting = {}          # terminus -> list of (ready_time, block)
        nblocks = 0
        prefix = {"EL": "E", "NL": "N"}[line]
        for tr in lst:
            origin = tr["stops"][0][0]
            dep = tr["stops"][0][2]
            pool = waiting.setdefault(origin, [])
            pool.sort()
            chosen = None
            for i, (ready, blk) in enumerate(pool):
                if ready <= dep:
                    chosen = pool.pop(i)[1]
                    break
            if chosen is None:
                nblocks += 1
                chosen = "%s%s%02d" % (prefix, {"WKD": "W", "SAT": "A", "SUN": "U"}[daytype], nblocks)
            tr["block_id"] = "%s-%s" % (period, chosen)
            end_stop = tr["stops"][-1][0]
            waiting.setdefault(end_stop, []).append((tr["stops"][-1][1] + LAYOVER, chosen))


def service_dates(period):
    a, b = P.SERVICE[period]
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def daytype_of(d):
    if d in P.HOLIDAYS:
        return "SUN"
    wd = d.weekday()
    return "WKD" if wd < 5 else ("SAT" if wd == 5 else "SUN")


def period_of(d):
    for p, (a, b) in P.SERVICE.items():
        if a <= d <= b:
            return p
    return None


def trips_on(trips_index, d):
    """Trips running on service date d (holiday exceptions applied)."""
    p = period_of(d)
    if p is None:
        return []
    return trips_index.get((p, daytype_of(d)), [])


def index_trips(trips):
    idx = {}
    for tr in trips:
        idx.setdefault((tr["period"], tr["daytype"]), []).append(tr)
    return idx


def gtfs_time(sec):
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return "%02d:%02d:%02d" % (h, m, s)


# --- coordinates -------------------------------------------------------------------------------------
def utm_to_latlon(e, n, zone=12):
    """Inverse transverse Mercator (WGS84), northern hemisphere."""
    a = 6378137.0
    f = 1 / 298.257223563
    k0 = 0.9996
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    x = e - 500000.0
    y = n
    m = y / k0
    mu = m / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + (151 * e1 ** 3 / 96) * math.sin(6 * mu))
    c1 = ep2 * math.cos(phi1) ** 2
    t1 = math.tan(phi1) ** 2
    n1 = a / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    r1 = a * (1 - e2) / (1 - e2 * math.sin(phi1) ** 2) ** 1.5
    d = x / (n1 * k0)
    lat = phi1 - (n1 * math.tan(phi1) / r1) * (d ** 2 / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1 ** 2 - 9 * ep2) * d ** 4 / 24
                                               + (61 + 90 * t1 + 298 * c1 + 45 * t1 ** 2 - 252 * ep2 - 3 * c1 ** 2) * d ** 6 / 720)
    lon0 = math.radians((zone - 1) * 6 - 180 + 3)
    lon = lon0 + (d - (1 + 2 * t1 + c1) * d ** 3 / 6
                  + (5 - 2 * c1 + 28 * t1 - 3 * c1 ** 2 + 8 * ep2 + 24 * t1 ** 2) * d ** 5 / 120) / math.cos(phi1)
    return math.degrees(lat), math.degrees(lon)


def district_of(x, y, layout):
    for d, rects in layout.items():
        for (x0, y0, x1, y1) in rects:
            if x0 <= x < x1 and y0 <= y < y1:
                return d
    return None


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
