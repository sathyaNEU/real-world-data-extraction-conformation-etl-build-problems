"""The simulation: the operated service, every collision warning the cameras raised (October 2025 to October 2026),
October 2026's ticket-machine log-ons, the incident register and the insurer's claims, the diversions and the
service return. Generator truth only; build.py writes the files and estim.py reads them back."""
import datetime as dt
import math

import numpy as np

from common import EXTRACT_FROM, LAST_DAY, NETWORK_2026, days, local_to_utc, rng
from world import (DEPOTS, DIRS, NIGHT, ROUTES, Fleet, Network, day_type, departures, night_trips, route_depot,
                   school_day, trips_per_day, HOLIDAYS)

SPEED_MPS = 5.2                 # mean running speed along a route, for the time a trip reaches each link
NOBRAKE = {"SLZ": 0.170, "HOR": 0.160, "VDO": 0.164, "QUI": 0.158, "TEN": 0.168, "RIB": 0.262, "SCL": 0.166}
P_LINK_MEAN = 0.0050
EXCLUSION_M = 30.0              # no warning off a false-trigger place falls this close to its point


def all_routes():
    out = []
    for dep, _ in DEPOTS:
        out.extend(ROUTES[dep])
    return out + sorted(NIGHT)


class World:
    def __init__(self):
        self.net = Network()
        self.fleet = Fleet()
        self.days = days(EXTRACT_FROM, LAST_DAY)
        r = rng("links")
        self.p_link = {}
        for (route, d), periods in sorted(self.net.seq.items()):
            for a, b, seq in periods:
                for i in range(len(seq) - 1):
                    ln = (seq[i], seq[i + 1])
                    if ln not in self.p_link:
                        self.p_link[ln] = float(P_LINK_MEAN * math.exp(r.normal(-0.18, 0.6)))
        # The bus-only underpass, link road and busway, and the quiet street past the sculpture, see no other road
        # users: no warning there has anything in the path.
        for pl in self.net.places:
            if pl["kind"] == "false":
                a, b = pl["link"]
                for ln in ((a, b), (b, a)):
                    if ln in self.p_link:
                        self.p_link[ln] = 0.0
        # The shared space is driven at walking pace: few warnings there besides the pedestrians'.
        for pl in self.net.places:
            if pl["kind"] == "pinch" and pl["link"] in self.p_link:
                self.p_link[pl["link"]] *= 0.25
        self.pcw_share = {ln: float(r.uniform(0.25, 0.7)) for ln in sorted(self.p_link)}
        self._service()
        self._warnings()

    # ------------------------------------------------------------ operated service
    def _service(self):
        """Every route-direction-day: scheduled and operated trips with their departures, and the bus on each."""
        r = rng("service")
        self.trips = {}             # (day, route, dir) -> list of (dep_seconds, fleet_no)
        self.scheduled = {}         # (day, route, dir) -> n
        for day in self.days:
            dtype = day_type(day)
            # Buses per depot that day, shuffled once.
            pool = {}
            for dep, _ in DEPOTS:
                bs = self.fleet.buses_of(dep, day)
                pool[dep] = [bs[int(i)] for i in r.permutation(len(bs))]
            used = {dep: 0 for dep, _ in DEPOTS}
            for route in all_routes():
                dep = route_depot(route, day)
                if route in NIGHT:
                    n = night_trips(day)
                else:
                    n = trips_per_day(route, dtype)
                for d in DIRS:
                    self.scheduled[(day, route, d)] = n
                if n == 0:
                    continue
                nb = 3 if route in NIGHT else (5 if route in ("27", "33") else 9)
                buses = []
                for _ in range(nb):
                    buses.append(pool[dep][used[dep] % len(pool[dep])])
                    used[dep] += 1
                for d in DIRS:
                    deps_ = departures(route, dtype, n)
                    keep = []
                    for k, t in enumerate(deps_):
                        if r.random() < 0.0045:
                            continue            # a trip lost to a breakdown or a missing driver
                        keep.append((t + (1800 if d == "VUELTA" else 0), buses[k % nb]))
                    self.trips[(day, route, d)] = keep

    # ------------------------------------------------------------ warnings
    def _point(self, link, frac, jitter, r):
        a, b = self.net.stops[link[0]], self.net.stops[link[1]]
        ux, uy = b.x - a.x, b.y - a.y
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        along = frac * L + r.normal(0, jitter)
        off = r.normal(0, jitter * 0.6)
        return a.x + ux * along - uy * off, a.y + uy * along + ux * off

    def _link_offsets(self, links):
        """Seconds from a trip's departure to the start of each link."""
        out, t = [], 0.0
        for ln in links:
            out.append(t)
            t += self.net.link_len(ln) / SPEED_MPS
        return out

    def _warnings(self):
        r = rng("warnings")
        rb = rng("brake")
        self.events = []            # dicts: the generator's truth for each warning
        places_by_rd = {}
        for pl in self.net.places:
            for rd in pl["routes"]:
                places_by_rd.setdefault(rd, []).append(pl)
        false_points = {}
        for pl in self.net.places:
            if pl["kind"] == "false":
                a, b = self.net.stops[pl["link"][0]], self.net.stops[pl["link"][1]]
                L = math.hypot(b.x - a.x, b.y - a.y)
                false_points.setdefault(pl["link"], []).append(pl["frac"] * L)
        for day in self.days:
            dtype = day_type(day)
            for route in all_routes():
                dep = route_depot(route, day)
                for d in DIRS:
                    trips = self.trips.get((day, route, d), [])
                    if not trips:
                        continue
                    links = self.net.links_on(route, d, day)
                    offs = self._link_offsets(links)
                    n = len(trips)
                    # Ordinary warnings, link by link.
                    lam = np.array([self.p_link[ln] for ln in links]) * n * (0.85 if dtype == "D" else 1.0)
                    counts = r.poisson(lam)
                    for li, c in enumerate(counts):
                        if c == 0:
                            continue
                        ln = links[li]
                        L = self.net.link_len(ln) / 1.18
                        fps = false_points.get(ln, [])
                        for _ in range(int(c)):
                            k = int(r.integers(0, n))
                            t0, bus = trips[k]
                            while True:
                                frac = float(r.uniform(0.04, 0.96))
                                if all(abs(frac * L - p) > EXCLUSION_M for p in fps):
                                    break
                            t = t0 + offs[li] + frac * self.net.link_len(ln) / SPEED_MPS
                            wtype = "PCW" if r.random() < self.pcw_share[ln] else "FCW"
                            x, y = self._point(ln, frac, 0.0, r)
                            spd = float(r.uniform(11, 26)) if wtype == "PCW" else float(r.uniform(16, 47))
                            self.events.append(dict(day=day, secs=t, bus=bus, route=route, dir=d, link=ln, x=x, y=y,
                                                    wtype=wtype, speed=spd, kind="ordinary", place=None, dep=dep))
                    # Places on this route-direction.
                    for pl in places_by_rd.get((route, d), []):
                        if day < pl["start"] or pl["link"] not in links:
                            continue
                        if pl["kind"] == "pinch" and (day.weekday() == 6 or day in HOLIDAYS):
                            continue
                        if pl["kind"] == "school" and not school_day(day):
                            continue
                        li = links.index(pl["link"])
                        for t0, bus in trips:
                            t = t0 + offs[li] + pl["frac"] * self.net.link_len(pl["link"]) / SPEED_MPS
                            tod = t % 86400
                            if "hours" in pl and not (pl["hours"][0] <= tod < pl["hours"][1]):
                                continue
                            if "windows" in pl and not any(a <= tod < b for a, b in pl["windows"]):
                                continue
                            if r.random() >= pl["q"]:
                                continue
                            jit = 2.5 if pl["kind"] == "false" else (4.0 if pl["kind"] == "pinch" else 6.0)
                            x, y = self._point(pl["link"], pl["frac"], jit, r)
                            lo, hi = pl["speed"]
                            self.events.append(dict(day=day, secs=t, bus=bus, route=route, dir=d, link=pl["link"],
                                                    x=x, y=y, wtype=pl["wtype"], speed=float(r.uniform(lo, hi)),
                                                    kind=pl["kind"], place=pl["name"], dep=dep))
        # Brake responses, in a separate stream.
        for e in self.events:
            if e["kind"] == "false":
                pl = [p for p in self.net.places if p["name"] == e["place"]][0]
                pnb = pl["nobrake"]
            elif e["kind"] == "pinch":
                pnb = 0.975 if e["dep"] == "SLZ" else NOBRAKE[e["dep"]]
            else:
                pnb = NOBRAKE[e["dep"]]
            e["braked"] = bool(rb.random() >= pnb)
            e["react_ms"] = int(rb.integers(340, 1960)) if e["braked"] else (
                int(rb.integers(2060, 2990)) if rb.random() < 0.25 else None)
        # Lane-departure and headway warnings, which the programme does not read.
        ro = rng("other_warnings")
        extra = []
        for e in self.events:
            if e["kind"] == "ordinary" and ro.random() < 0.17:
                f = dict(e)
                f["wtype"] = "LDW" if ro.random() < 0.55 else "HMW"
                f["secs"] = e["secs"] + float(ro.uniform(-900, 900))
                f["kind"] = "other"
                f["place"] = None
                f["braked"] = bool(ro.random() < 0.3)
                f["react_ms"] = int(ro.integers(400, 1900)) if f["braked"] else None
                extra.append(f)
        self.events.extend(extra)
        for e in self.events:
            e["utc"] = local_to_utc(e["day"], e["secs"])
        self.events.sort(key=lambda e: (e["utc"], e["bus"], e["x"]))


def summary(w):
    """Quick truth summary used while tuning (never shipped)."""
    from collections import Counter
    c = Counter()
    for e in w.events:
        if dt.date(2026, 1, 1) <= e["day"] <= dt.date(2026, 10, 31) and e["kind"] != "other":
            c[(e["dep"], e["kind"])] += 1
    return c
