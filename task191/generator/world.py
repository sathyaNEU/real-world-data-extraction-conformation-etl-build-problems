"""The world: Lorvega's depots, its two networks (Red 2025 to 13 December 2025, Red 2026 from 14 December 2025),
the stops and their coordinates, the routes' stop sequences with their validity, the timetable, the calendar, the
fleet and the places where the forward camera fires.

Everything here is generator truth. Nothing in this module is shipped as it stands; build.py writes the files."""
import datetime as dt
import math

from common import NETWORK_2026, rng

DEPOTS = [
    ("SLZ", "San Lázaro"),
    ("HOR", "Hornacho"),
    ("VDO", "Valdeolmos"),
    ("QUI", "El Quiñón"),
    ("TEN", "Las Tenerías"),
    ("RIB", "La Ribera"),
    ("SCL", "Santa Clara"),
]
DEPOT_NAME = dict(DEPOTS)
SECTOR = {"SLZ": 92, "HOR": 140, "VDO": 196, "QUI": 248, "TEN": 296, "RIB": 344, "SCL": 40}

ROUTES = {
    "SLZ": ["1", "3", "7", "9"],
    "HOR": ["12", "14", "27", "33"],
    "VDO": ["40", "41", "44", "46"],
    "QUI": ["5", "16", "21", "25"],
    "TEN": ["2", "8", "19", "23"],
    "RIB": ["4", "10", "17", "29"],
    "SCL": ["6", "11", "31", "35"],
}
NIGHT = {"N1": "SLZ", "N2": "HOR", "N3": "VDO", "N4": "QUI", "N5": "TEN", "N6": "RIB", "N7": "SCL"}   # Fri and Sat nights
MOVED_ROUTE = ("25", "QUI", "TEN")          # route 25 runs from Las Tenerías from Red 2026
LOW_FREQ = {"27", "33"}

BUSWAY_OPEN = dt.date(2026, 6, 1)
SCULPTURE_FROM = dt.date(2026, 4, 15)
SHARED_SPACE_FROM = dt.date(2026, 3, 2)

DIRS = ("IDA", "VUELTA")                    # IDA: terminus towards the centre; VUELTA: centre towards the terminus

HOLIDAYS = {
    dt.date(2025, 10, 12), dt.date(2025, 11, 1), dt.date(2025, 12, 6), dt.date(2025, 12, 8), dt.date(2025, 12, 25),
    dt.date(2026, 1, 1), dt.date(2026, 1, 6), dt.date(2026, 2, 28), dt.date(2026, 4, 2), dt.date(2026, 4, 3),
    dt.date(2026, 5, 1), dt.date(2026, 8, 15), dt.date(2026, 9, 8), dt.date(2026, 10, 12), dt.date(2026, 11, 1),
}
SCHOOL_TERMS = [
    (dt.date(2025, 9, 8), dt.date(2025, 12, 22)), (dt.date(2026, 1, 8), dt.date(2026, 3, 27)),
    (dt.date(2026, 4, 6), dt.date(2026, 6, 19)), (dt.date(2026, 9, 9), dt.date(2026, 11, 1)),
]


def day_type(d):
    if d in HOLIDAYS or d.weekday() == 6:
        return "D"          # Sunday and holiday service
    if d.weekday() == 5:
        return "S"
    return "L"              # weekday (laborable)


def school_day(d):
    return d.weekday() < 5 and d not in HOLIDAYS and any(a <= d <= b for a, b in SCHOOL_TERMS)


def route_depot(route, d):
    if route in NIGHT:
        return NIGHT[route]
    if route == MOVED_ROUTE[0]:
        return MOVED_ROUTE[2] if d >= NETWORK_2026 else MOVED_ROUTE[1]
    for dep, rs in ROUTES.items():
        if route in rs:
            return dep
    raise KeyError(route)


# ---------------------------------------------------------------- geometry
LAT0, LON0 = 37.6185, -5.0421
M_PER_DEG_LAT = 111_320.0
M_PER_DEG_LON = 111_320.0 * math.cos(math.radians(LAT0))


def to_latlon(x, y):
    return LAT0 + y / M_PER_DEG_LAT, LON0 + x / M_PER_DEG_LON


def to_xy(lat, lon):
    return (lon - LON0) * M_PER_DEG_LON, (lat - LAT0) * M_PER_DEG_LAT


STREETS = ["Calle Real", "Avenida de Andalucía", "Calle San Pablo", "Ronda Norte", "Calle Ancha", "Calle Alfarería",
           "Avenida del Río", "Calle Mayor", "Calle Granada", "Avenida de la Paz", "Calle Jardines", "Calle Hornos",
           "Avenida de Córdoba", "Calle Santiago", "Calle Pozo", "Calle Nueva", "Avenida de Sevilla", "Calle Tinte",
           "Calle Laurel", "Avenida de la Estación", "Calle Victoria", "Calle Molino", "Calle Toledo", "Calle Ermita",
           "Avenida de Europa", "Calle Arenal", "Calle Cádiz", "Calle Huerta", "Calle Ciprés", "Avenida del Parque"]
SUFFIX = ["", " Norte", " Sur", " Alta", " Baja", " (Mercado)", " (Ambulatorio)", " (Colegio)", " (Iglesia)",
          " (Instituto)", " (Polideportivo)", " (Plaza)"]


class Stop:
    __slots__ = ("key", "name", "x", "y", "code25", "code26")

    def __init__(self, key, name, x, y):
        self.key, self.name, self.x, self.y = key, name, x, y
        self.code25 = None
        self.code26 = None


class Network:
    """Stops and every route-direction's stop sequence by validity period."""

    def __init__(self):
        self.stops = {}                 # key -> Stop
        self.seq = {}                   # (route, dir) -> list of (valid_from, valid_to, [stop keys])
        self.length_km = {}             # (route, dir, valid_from) -> km
        self.places = []                # dicts: kind, name, route-dir list, link (a, b), frac, from, to, ...
        self._build()

    # ---- helpers
    def _stop(self, key, name, x, y):
        if key not in self.stops:
            self.stops[key] = Stop(key, name, x, y)
        return key

    def _path(self, r, x0, y0, x1, y1, spacing, jitter, prefix):
        """Stops from (x0, y0) towards (x1, y1), every `spacing` metres, the first at (x0, y0), the last short of
        (x1, y1)."""
        dist = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(dist // spacing))
        ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
        out = []
        for i in range(n):
            t = i * dist / n
            off = r.normal(0, jitter) if 0 < i else 0.0
            x = x0 + ux * t - uy * off
            y = y0 + uy * t + ux * off
            out.append((x, y))
        return out

    def _build(self):
        r = rng("network")
        names = r.permutation(len(STREETS) * len(SUFFIX))
        name_iter = iter(int(i) for i in names)

        def fresh_name():
            i = next(name_iter)
            return STREETS[i % len(STREETS)] + SUFFIX[i // len(STREETS)]

        # Central hubs and each depot's trunk into the centre.
        hubs = {"CEN": ("Plaza Mayor", 0.0, 0.0), "MER": ("Mercado Central", -320.0, 640.0),
                "EST": ("Estación de Autobuses", 880.0, -420.0)}
        for k, (nm, x, y) in hubs.items():
            self._stop("H-" + k, nm, x, y)
        trunk = {}
        hub_of = {"SLZ": "MER", "HOR": "EST", "VDO": "EST", "QUI": "CEN", "TEN": "CEN", "RIB": "CEN", "SCL": "MER"}
        for dep, ang in SECTOR.items():
            hk = "H-" + hub_of[dep]
            hx, hy = self.stops[hk].x, self.stops[hk].y
            a = math.radians(ang)
            if dep == "SLZ":
                # The old town: Calle Mesones, Plaza de Abastos, Calle Feria, then the Mercado Central.
                pts = [(hx + 1300 * math.cos(a), hy + 1300 * math.sin(a)), (hx + 900 * math.cos(a), hy + 900 * math.sin(a)),
                       (hx + 520 * math.cos(a), hy + 520 * math.sin(a)), (hx + 160 * math.cos(a), hy + 160 * math.sin(a))]
                nm = ["Calle Mesones", "Calle Cuna", "Plaza de Abastos", "Calle Feria"]
            else:
                pts = [(hx + d * math.cos(a), hy + d * math.sin(a)) for d in (1500, 1080, 660)]
                nm = [fresh_name() for _ in pts]
            keys = [self._stop("T-%s-%d" % (dep, i), nm[i], x, y) for i, (x, y) in enumerate(pts)]
            trunk[dep] = keys + [hk]

        # Each daytime route: terminus in the depot's sector, a path to the start of the trunk, then the trunk.
        for dep, routes in ROUTES.items():
            base = math.radians(SECTOR[dep])
            tx0, ty0 = self.stops[trunk[dep][0]].x, self.stops[trunk[dep][0]].y
            for j, route in enumerate(routes):
                ang = base + math.radians((-22, -8, 8, 22)[j])
                rad = 5200 + 400 * j - (900 if route in LOW_FREQ else 0)
                x0, y0 = rad * math.cos(ang), rad * math.sin(ang)
                pts = self._path(r, x0, y0, tx0, ty0, 430, 55, route)
                keys = [self._stop("S-%s-%02d" % (route, i), fresh_name(), x, y) for i, (x, y) in enumerate(pts)]
                ida = keys + trunk[dep]
                self._add(route, ida, dt.date(2000, 1, 1), dt.date(2099, 12, 31))

        # Night routes: each depot's trunk joined across the centre to the next depot's.
        order = [d for d, _ in DEPOTS]
        for route, dep in NIGHT.items():
            other = order[(order.index(dep) + 1) % len(order)]
            ida = list(trunk[dep]) + list(reversed(trunk[other]))[1:]
            self._add(route, ida, dt.date(2000, 1, 1), dt.date(2099, 12, 31))

        self._red2026(r)
        self._number_stops(r)

    def _add(self, route, ida, a, b):
        for d, seq in (("IDA", list(ida)), ("VUELTA", list(reversed(ida)))):
            self.seq.setdefault((route, d), []).append((a, b, seq))

    def _replace(self, route, start, stop_idx_from, stop_idx_to, new_pts, names, prefix, until=None):
        """From `start`, route `route` runs through new stops in place of IDA stops [from, to)."""
        cur = [s for s in self.seq[(route, "IDA")] if s[1] >= start]
        a, b, ida = cur[-1]
        new_keys = [self._stop("%s-%d" % (prefix, i), names[i], x, y) for i, (x, y) in enumerate(new_pts)]
        new_ida = ida[:stop_idx_from] + new_keys + ida[stop_idx_to:]
        for d in DIRS:
            lst = self.seq[(route, d)]
            a0, b0, s0 = lst[-1]
            lst[-1] = (a0, start - dt.timedelta(days=1), s0)
            lst.append((start, b0, list(new_ida) if d == "IDA" else list(reversed(new_ida))))
        return new_keys

    def _red2026(self, r):
        S = self.stops
        # Route 27: the Almadraba branch under the railway (a bus-only underpass), from Red 2026.
        ida = self.seq[("27", "IDA")][-1][2]
        p0, p3 = S[ida[0]], S[ida[3]]
        pts = [(p0.x + 260, p0.y - 380), (p0.x + 170, p0.y - 40), (p3.x - 120, p3.y - 80)]
        self._replace("27", NETWORK_2026, 0, 3, pts, ["Polígono Almadraba Sur", "Polígono Almadraba Norte",
                                                      "Paso Inferior Almadraba"], "A27")
        # Route 33: over the hill by the Ramal de Los Molinos, a bus-only link road with a tight barriered bend.
        ida = self.seq[("33", "IDA")][-1][2]
        p4, p7 = S[ida[4]], S[ida[7]]
        pts = [(p4.x - 300, p4.y + 160), (p4.x - 260, p4.y + 560), (p7.x - 190, p7.y + 120)]
        self._replace("33", NETWORK_2026, 4, 7, pts, ["Los Molinos Alto", "Ramal de Los Molinos",
                                                      "Cuesta de Los Molinos"], "M33")
        # Route 40: the Vía Verde busway with automatic bollard gates, from 1 June 2026.
        ida = self.seq[("40", "IDA")][-1][2]
        p2, p6 = S[ida[2]], S[ida[6]]
        pts = [(p2.x + 210, p2.y - 230), (p2.x + 600, p2.y - 360), (p6.x + 240, p6.y - 210)]
        self._replace("40", BUSWAY_OPEN, 2, 6, pts, ["Vía Verde Norte", "Vía Verde Centro", "Vía Verde Sur"], "V40")
        # Places where the forward camera fires on passes with nothing in the path.
        a27 = self.seq[("27", "VUELTA")][-1][2]
        i = a27.index("A27-2")
        self.places.append(dict(kind="false", name="Paso Inferior Almadraba", routes=[("27", "VUELTA")],
                                link=(a27[i], a27[i + 1]), frac=0.62, start=NETWORK_2026, q=0.50,
                                wtype="FCW", speed=(38, 46), nobrake=0.880))
        m33 = self.seq[("33", "IDA")][-1][2]
        i = m33.index("M33-1")
        for d in DIRS:
            ln = (m33[i], m33[i + 1]) if d == "IDA" else (m33[i + 1], m33[i])
            self.places.append(dict(kind="false", name="Ramal de Los Molinos", routes=[("33", d)],
                                    link=ln, frac=0.47 if d == "IDA" else 0.53, start=NETWORK_2026, q=0.30,
                                    wtype="FCW", speed=(30, 37), nobrake=0.890))
        v40 = self.seq[("40", "IDA")][-1][2]
        i = v40.index("V40-0")
        for d in DIRS:
            ln = (v40[i], v40[i + 1]) if d == "IDA" else (v40[i + 1], v40[i])
            self.places.append(dict(kind="false", name="Vía Verde (bollard gate)", routes=[("40", d)],
                                    link=ln, frac=0.55 if d == "IDA" else 0.45, start=BUSWAY_OPEN, q=0.276,
                                    wtype="PCW", speed=(12, 18), nobrake=0.870))
        # Route 44, inbound to its terminus, passes the Glorieta del Olivo, where a sculpture was installed in April
        # 2026 on a street the route has always used.
        v44 = self.seq[("44", "VUELTA")][-1][2]
        k = len(v44) - 4
        self.places.append(dict(kind="false", name="Glorieta del Olivo", routes=[("44", "VUELTA")],
                                link=(v44[k], v44[k + 1]), frac=0.40, start=SCULPTURE_FROM, q=0.80,
                                wtype="PCW", speed=(22, 29), nobrake=0.860))
        # Genuine hotspots: the market's pinch point in the old town's shared space, schools and the hospital.
        slz = self.seq[("1", "IDA")][-1][2]
        i = slz.index("T-SLZ-2")
        for d in DIRS:
            ln = (slz[i], slz[i + 1]) if d == "IDA" else (slz[i + 1], slz[i])
            self.places.append(dict(kind="pinch", name="Plaza de Abastos", routes=[(rt, d) for rt in ROUTES["SLZ"]],
                                    link=ln, frac=0.42 if d == "IDA" else 0.58, start=SHARED_SPACE_FROM, q=0.084,
                                    wtype="PCW", speed=(9, 17), nobrake=0.975, hours=(8 * 3600, 15 * 3600),
                                    days="MS"))
        for route, frac in (("8", 0.5), ("10", 0.35), ("31", 0.6), ("16", 0.45)):
            seqv = self.seq[(route, "IDA")][-1][2]
            k = len(seqv) // 3
            for d in DIRS:
                ln = (seqv[k], seqv[k + 1]) if d == "IDA" else (seqv[k + 1], seqv[k])
                self.places.append(dict(kind="school", name="school, route %s" % route, routes=[(route, d)],
                                        link=ln, frac=frac if d == "IDA" else 1 - frac, start=dt.date(2000, 1, 1),
                                        q=0.10, wtype="PCW", speed=(14, 28), nobrake=None,
                                        windows=((8 * 3600 + 1800, 9 * 3600 + 1800), (13 * 3600 + 2700, 14 * 3600 + 2700))))
        seqv = self.seq[("4", "IDA")][-1][2]
        k = len(seqv) // 2
        for d in DIRS:
            ln = (seqv[k], seqv[k + 1]) if d == "IDA" else (seqv[k + 1], seqv[k])
            self.places.append(dict(kind="hospital", name="Hospital de la Ribera", routes=[("4", d)], link=ln,
                                    frac=0.5, start=dt.date(2000, 1, 1), q=0.028, wtype="PCW", speed=(12, 30),
                                    nobrake=None, hours=(7 * 3600, 22 * 3600)))

    def _number_stops(self, r):
        keys = sorted(self.stops)
        new_keys = {k for k in keys if k.split("-")[0] in ("A27", "M33", "V40")}
        c25 = r.permutation(len(keys)) + 1001
        c26 = r.permutation(len(keys)) + 26001
        for i, k in enumerate(keys):
            s = self.stops[k]
            s.code26 = "%05d" % c26[i]
            s.code25 = None if k in new_keys else "P%04d" % c25[i]

    # ---- queries
    def seq_on(self, route, d, day):
        for a, b, s in self.seq[(route, d)]:
            if a <= day <= b:
                return s
        raise KeyError((route, d, day))

    def links_on(self, route, d, day):
        s = self.seq_on(route, d, day)
        return [(s[i], s[i + 1]) for i in range(len(s) - 1)]

    def link_len(self, link):
        a, b = self.stops[link[0]], self.stops[link[1]]
        return math.hypot(b.x - a.x, b.y - a.y) * 1.18        # street distance over the straight line

    def route_km(self, route, d, day):
        return sum(self.link_len(ln) for ln in self.links_on(route, d, day)) / 1000.0


# ---------------------------------------------------------------- timetable
def trips_per_day(route, dtype):
    if route in NIGHT:
        return 0
    if route == "33":
        return {"L": 14, "S": 11, "D": 8}[dtype]
    if route in LOW_FREQ:
        return {"L": 32, "S": 24, "D": 18}[dtype]
    return {"L": 52, "S": 38, "D": 28}[dtype]


def night_trips(day):
    """Night routes run on Friday and Saturday nights; the service day is the evening's date."""
    return 7 if day.weekday() in (4, 5) else 0


def departures(route, dtype, n):
    """Departure times (seconds after midnight) of the n trips of a route-direction-day, 06:00 to 23:30, denser in
    the peaks."""
    if n == 0:
        return []
    if route in NIGHT:
        return [int(23.5 * 3600 + i * 50 * 60) for i in range(n)]
    span0, span1 = 6 * 3600, 23 * 3600 + 1800
    if dtype == "L":
        # Peaks 07:00 to 09:30 and 13:30 to 15:30 carry a third of the trips.
        grid = []
        w = []
        for t in range(span0, span1, 300):
            peak = (7 * 3600 <= t < 9 * 3600 + 1800) or (13 * 3600 + 1800 <= t < 15 * 3600 + 1800)
            grid.append(t)
            w.append(1.8 if peak else 1.0)
        cum = [0.0]
        for x in w:
            cum.append(cum[-1] + x)
        tot = cum[-1]
        out = []
        j = 0
        for i in range(n):
            target = (i + 0.5) * tot / n
            while cum[j + 1] < target:
                j += 1
            out.append(grid[j] + int(300 * (target - cum[j]) / (cum[j + 1] - cum[j])))
        return out
    return [int(span0 + (i + 0.5) * (span1 - span0) / n) for i in range(n)]


# ---------------------------------------------------------------- fleet
class Fleet:
    """Buses with fleet numbers, plates (some re-registered), models, the depot each is allocated to by date, and
    each bus's camera firmware version by date."""

    MODELS = [("Irizar ie tram 12", 0.22), ("MAN Lion's City 12 E", 0.30), ("Mercedes-Benz eCitaro", 0.18),
              ("Iveco Urbanway 12 Hybrid", 0.20), ("Solaris Urbino 12", 0.10)]

    def __init__(self):
        r = rng("fleet")
        self.buses = []
        self.alloc = {}             # fleet_no -> list of (from, to, depot)
        self.plates = {}            # fleet_no -> list of (from, to, plate)
        self.model = {}
        self.fw2 = {}               # fleet_no -> date the camera moved to firmware 2.x, or None
        letters = "BCDFGHJKLMNPRSTVWXYZ"
        n = 0
        used = set()

        def plate():
            while True:
                num = int(r.integers(1000, 9999))
                lt = "".join(letters[int(i)] for i in r.integers(0, len(letters), 3))
                p = "%d %s" % (num, lt)
                if p not in used:
                    used.add(p)
                    return p

        for dep, _ in DEPOTS:
            size = 52 if dep not in ("QUI", "TEN") else 48
            for _ in range(size):
                n += 1
                fno = "%d" % (1000 + n)
                self.buses.append(fno)
                ms = [m for m, _ in self.MODELS]
                ps = [p for _, p in self.MODELS]
                self.model[fno] = ms[int(r.choice(len(ms), p=ps))]
                self.alloc[fno] = [(dt.date(2015, 1, 1), dt.date(2099, 12, 31), dep)]
                self.plates[fno] = [(dt.date(2015, 1, 1), dt.date(2099, 12, 31), plate())]
                u = r.random()
                if u < 0.84:
                    self.fw2[fno] = dt.date(2026, 5, 4) + dt.timedelta(days=int(r.integers(0, 75)))
                else:
                    self.fw2[fno] = None
        # Route 25's buses move with it from El Quiñón to Las Tenerías at Red 2026.
        qui = [b for b in self.buses if self.alloc[b][0][2] == "QUI"]
        for b in qui[:9]:
            self.alloc[b] = [(dt.date(2015, 1, 1), NETWORK_2026 - dt.timedelta(days=1), "QUI"),
                             (NETWORK_2026, dt.date(2099, 12, 31), "TEN")]
        # Second-hand buses bought in 2025 kept their previous plates until re-registered on 20 April 2026.
        rr = r.permutation(len(self.buses))[:40]
        for idx in sorted(int(i) for i in rr):
            b = self.buses[idx]
            old = self.plates[b][0][2]
            self.plates[b] = [(dt.date(2015, 1, 1), dt.date(2026, 4, 19), old),
                              (dt.date(2026, 4, 20), dt.date(2099, 12, 31), plate())]
        # Loans: a bus lent to another depot for a few days.
        deps = [d for d, _ in DEPOTS]
        self.loans = []
        for k in range(22):
            b = self.buses[int(r.integers(0, len(self.buses)))]
            if len(self.alloc[b]) > 1 or any(lb == b for lb, *_ in self.loans):
                continue
            home = self.alloc[b][0][2]
            to = deps[int(r.integers(0, len(deps)))]
            if to == home:
                continue
            a = dt.date(2026, 1, 12) + dt.timedelta(days=int(r.integers(0, 270)))
            e = a + dt.timedelta(days=int(r.integers(3, 16)))
            self.alloc[b] = [(dt.date(2015, 1, 1), a - dt.timedelta(days=1), home), (a, e, to),
                             (e + dt.timedelta(days=1), dt.date(2099, 12, 31), home)]
            self.loans.append((b, a, e, home, to))

    def depot_on(self, fno, day):
        for a, b, d in self.alloc[fno]:
            if a <= day <= b:
                return d
        raise KeyError((fno, day))

    def plate_on(self, fno, day):
        for a, b, p in self.plates[fno]:
            if a <= day <= b:
                return p
        raise KeyError((fno, day))

    def buses_of(self, dep, day):
        return [b for b in self.buses if self.depot_on(b, day) == dep]
