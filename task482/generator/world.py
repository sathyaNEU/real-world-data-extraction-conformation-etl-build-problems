"""The Wellhaven Bike Share fleet, 24 September 2026 to 10 January 2027: the truth task482's pack is cut from.

Minute steps on the absolute clock (UTC), every routine keyed to local time (Eastern, the clocks going back on
1 November 2026). Each minute: renters arrive at each station (Poisson by station type, hour, day type,
month and weather), take a bike in working order of the type they want (or of the other type), ride, and dock at
the end of the ride (a full station sends them to the nearest free dock). A bike breaks on a ride with a small
probability; its rider docks it, and some riders report it, after which the operator takes it out of rental. A renter
who finds only broken bikes listed sometimes reports one too. The vans fill the stations each morning, answer the
feed's empty and full alerts, and the mechanics check every station on a cycle and take broken bikes to the depot,
where they are repaired. December nights take bikes off the street for the winter.

The status feed counts a docked bike as available until the operator has taken it out of rental, so a broken bike no
one reported stays listed, and a station whose only listed bikes are broken raises no empty alert.
"""
import collections
import datetime as dt
import math

import numpy as np

SEED = 1076
UTC = dt.timezone.utc
FALLBACK_UTC = dt.datetime(2026, 11, 1, 6, 0, tzinfo=UTC)     # 2:00 EDT becomes 1:00 EST
START = dt.datetime(2026, 9, 24, 0, 0, tzinfo=UTC)           # 20:00 on 23 September, Eastern daylight time
NMIN = 157020
END = START + dt.timedelta(minutes=NMIN)                      # 20:00 on 10 January, the City's extract


def offset_hours(utc):
    return -4 if utc < FALLBACK_UTC else -5


def to_local(utc):
    """local wall-clock time (naive) of an absolute instant"""
    return (utc + dt.timedelta(hours=offset_hours(utc))).replace(tzinfo=None)


def utc_of_local(t):
    """the absolute instant of a local wall-clock time; in the repeated hour the first one"""
    first = (t - dt.timedelta(hours=-4)).replace(tzinfo=UTC)
    if first < FALLBACK_UTC:
        return first
    return (t - dt.timedelta(hours=-5)).replace(tzinfo=UTC)


def minute_of(t):
    """minute index of a local wall-clock time (or of an aware instant)"""
    u = t if t.tzinfo is not None else utc_of_local(t)
    return int((u - START).total_seconds() // 60)


QSTART = dt.datetime(2026, 10, 1)
QEND = dt.datetime(2027, 1, 1)
# The fleet's own clock: the local minute of the day and the local day (days since 24 September) at each minute. It
# keeps Eastern time from the window's start and turns back an hour four hours early, at 22:00 on 31 October, which
# moves nothing the pack records; the first four hours (the evening of 23 September) run on day -1.
_fb = 54840
_idx = np.arange(NMIN)
_local_min = _idx - 4 * 60
_local_min[_fb:] -= 60
LOCAL_MOD = (_local_min % 1440).astype(np.int32)
LOCAL_DAY = (_local_min // 1440).astype(np.int32)           # days since 24 September 2026 local
# Eastern time itself at each minute, for the Schedule C minutes and anything the pack states
_fb_true = int((FALLBACK_UTC - START).total_seconds() // 60)
_true_min = _idx - 4 * 60
_true_min[_fb_true:] -= 60
TRUE_MOD = (_true_min % 1440).astype(np.int32)
TRUE_DAY = (_true_min // 1440).astype(np.int32)
DAY0 = dt.date(2026, 9, 24)
SERVICE = (6 * 60, 24 * 60)
MONTHS = (10, 11, 12)

P = dict(p_break=0.0080, break_per_km=0.0026, p_report=0.35, p_report_seen=0.012, flag_lo=20, flag_hi=150,
         p_find_alert=0.5, p_find_morning=0.0, alert_lo=15, alert_hi=50, queue_step=25, check_lo=10 * 60,
         check_hi=15 * 60, repair_lo=1, repair_hi=3, prefer_e=0.45, take_other=0.85, fill_target=0.68,
         alert_fill=0.55, full_trim=0.7, p_staff=0.01,
         res_cycle={112: 3, 113: 4, 114: 4, 115: 4, 116: 3, 117: 4, 118: 4, 119: 3, 120: 4, 121: 4, 122: 4, 123: 4,
                    124: 4},
         check_lo_res=13 * 60, check_hi_res=17 * 60)
MONTH_SCALE = {9: 1.0, 10: 0.88, 11: 0.62, 12: 0.34, 1: 0.30}
DAILY = {"core": 46, "campus": 38, "hub": 58, "res": 30, "park": 16}
MULT = {112: 1.55, 116: 1.6, 113: 1.25, 117: 1.3, 119: 1.35, 121: 1.3, 114: 1.1, 118: 1.0, 115: 0.9, 120: 0.85}
STORAGE_NIGHTS = (dt.date(2026, 12, 1), dt.date(2026, 12, 8), dt.date(2026, 12, 15))

# id, name, kind, x km, y km, docks
STATIONS = [
    (101, "Market Square", "core", 0.0, 0.0, 27),
    (102, "Queen and Albert", "core", 0.4, 0.2, 23),
    (103, "City Hall", "core", -0.3, 0.3, 19),
    (104, "Wharf Street", "core", 0.2, -0.4, 23),
    (105, "Courthouse", "core", 0.7, -0.1, 19),
    (106, "Library Plaza", "core", -0.6, -0.2, 19),
    (107, "General Hospital", "core", 0.1, 0.7, 15),
    (108, "University Commons", "campus", 2.4, 1.1, 23),
    (109, "Science Quad", "campus", 2.8, 0.6, 15),
    (110, "Central Station", "hub", -1.1, 0.5, 27),
    (111, "Eastgate Terminal", "hub", 1.3, -0.9, 23),
    (112, "Maple Grove", "res", 2.29, 0.71, 11),
    (113, "Elmwood Park", "res", 2.06, 2.36, 15),
    (114, "Riverbend", "res", 0.71, 3.23, 13),
    (115, "Cedar Heights", "res", -0.71, 2.29, 19),
    (116, "Birch Hill", "res", -2.36, 2.06, 11),
    (117, "Linden Avenue", "res", -3.23, 0.71, 15),
    (118, "Orchard Lane", "res", -2.29, -0.71, 13),
    (119, "Willow Crescent", "res", -2.06, -2.36, 11),
    (120, "Ashdale", "res", -0.71, -3.23, 15),
    (121, "Fernwood", "res", 0.71, -2.29, 13),
    (122, "Waterfront Trail", "park", -0.8, -1.6, 15),
    (123, "Pier Park", "park", 0.6, -1.7, 19),
    (124, "Lighthouse Point", "park", 1.9, -1.5, 11),
]
# Linden Avenue moves across the street on 9 November under a new id; Birch Hill and Willow Crescent gain four docks
RELOCATION = dict(old=117, new=125, when=dt.datetime(2026, 11, 8, 23, 0), dx=0.05, dy=0.02)
EXPANSIONS = {116: (dt.datetime(2026, 11, 1, 23, 0), 15), 119: (dt.datetime(2026, 11, 22, 23, 0), 15)}


def profile(kind, weekend):
    h = np.zeros(24)
    if weekend:
        base = {"core": 0.5, "campus": 0.4, "hub": 0.7, "res": 0.7, "park": 1.4}[kind]
        for t in range(24):
            h[t] = base * max(0.0, math.sin(math.pi * (t - 8) / 14)) if 8 <= t <= 22 else 0.02
        return h
    peaks = {
        "res": {7: 2.6, 8: 3.0, 9: 1.4, 12: 0.4, 17: 0.6, 18: 0.7, 19: 0.6, 20: 0.4},
        "core": {8: 0.3, 9: 0.3, 12: 1.0, 13: 0.8, 16: 1.6, 17: 2.8, 18: 1.8, 19: 0.6, 21: 0.3},
        "hub": {7: 1.6, 8: 2.0, 9: 0.8, 12: 0.5, 16: 1.0, 17: 1.8, 18: 1.2, 19: 0.4},
        "campus": {9: 0.8, 10: 1.2, 11: 1.2, 12: 1.4, 13: 1.2, 14: 1.0, 15: 1.0, 16: 1.2, 17: 0.9, 20: 0.4},
        "park": {11: 0.4, 12: 0.6, 14: 0.6, 16: 0.7, 17: 0.8, 18: 0.6},
    }[kind]
    for t in range(24):
        h[t] = peaks.get(t, 0.08 if 6 <= t <= 22 else 0.01)
    return h


def dest_weights(kind_from, hour, weekend):
    if weekend:
        return {"core": 1.0, "campus": 0.3, "hub": 0.8, "res": 1.0, "park": 1.6}
    if hour < 11:
        if kind_from in ("res", "hub"):
            return {"core": 3.0, "campus": 1.6, "hub": 1.4, "res": 0.3, "park": 0.2}
        return {"core": 1.0, "campus": 1.0, "hub": 1.0, "res": 0.6, "park": 0.3}
    if hour < 15:
        return {"core": 1.4, "campus": 0.8, "hub": 0.8, "res": 0.6, "park": 0.6}
    if kind_from in ("core", "campus", "hub"):
        return {"core": 0.5, "campus": 0.4, "hub": 1.0, "res": 3.2, "park": 0.4}
    return {"core": 1.0, "campus": 0.4, "hub": 0.8, "res": 1.0, "park": 0.6}


def weather(seed):
    """daily demand factor from the season's weather (rain and snow days ride less)"""
    rng = np.random.default_rng([seed, 7])
    out = {}
    d = DAY0
    while d < dt.date(2027, 1, 12):
        f = 1.0
        r = rng.random()
        if d.month >= 11 and r < 0.18:
            f = 0.45          # snow or freezing rain
        elif r < 0.22:
            f = 0.65          # rain
        out[d] = f
        d += dt.timedelta(days=1)
    return out


class Fleet:
    def __init__(self, seed=SEED, params=None, mult=None):
        self.seed = seed
        self.P = dict(P, **(params or {}))
        self.mult = dict(MULT)
        self.mult.update(mult or {})
        self.rng = np.random.default_rng(seed)
        self.st = {s[0]: dict(id=s[0], name=s[1], kind=s[2], x=s[3], y=s[4], cap=s[5]) for s in STATIONS}
        self.public = [s[0] for s in STATIONS]
        self.wx = weather(seed)
        self.btype = {}
        for k in range(310):
            self.btype[1000 + k] = "classic"
        bikes = list(self.btype)
        self.rng.shuffle(bikes)
        self.docked = {s: [] for s in self.public}
        it = iter(bikes)
        for s in self.public:
            for _ in range(int(0.55 * self.st[s]["cap"])):
                self.docked[s].append(next(it))
        self.depot = list(it)
        self.broken = set()
        self.flagged = set()
        self.flag_due = {}
        self.repair_due = {}
        self.in_ride = {}
        self.trips = []
        self.moves = []
        self.pending = {}
        self.checks_today = []
        self.trip_id = 0
        self.flags = []
        self.reports = []
        self.breaks = []          # dicts: bike, station, docked minute, reported, removed minute
        self.open_break = {}      # bike -> index into breaks
        self.lost = collections.Counter()
        self.listed = {s: np.zeros(NMIN, dtype=np.int16) for s in self.public}
        self.work = {s: np.zeros(NMIN, dtype=np.int16) for s in self.public}
        self.disabled = {s: np.zeros(NMIN, dtype=np.int16) for s in self.public}
        self.docks = {s: np.zeros(NMIN, dtype=np.int16) for s in self.public}
        self.active = {s: np.zeros(NMIN, dtype=bool) for s in self.public}
        self.relocated = False
        self.rs = {}
        self.seq = 0
        self.dock_min = {}
        self.last_rent = {}

    def r(self, *key):
        """an independent random stream per purpose and station, so one station's dials move little else"""
        if key not in self.rs:
            self.rs[key] = np.random.default_rng([self.seed] + [int(k) for k in key])
        return self.rs[key]

    # ----------------------------------------------------------------------------------------------------------
    def cap(self, s):
        return self.st[s]["cap"]

    def listed_n(self, s):
        return sum(1 for b in self.docked[s] if b not in self.flagged)

    def working(self, s, kind=None):
        return [b for b in self.docked[s] if b not in self.broken and (kind is None or self.btype[b] == kind)]

    def station_ids(self):
        return [s for s in self.public if self.st[s].get("open", True)]

    def to_depot(self, b, m, repair):
        self.depot.append(b)
        if b in self.open_break:
            self.breaks[self.open_break.pop(b)]["removed"] = m
        if repair:
            rb = self.r(5, b)
            days = int(rb.integers(self.P["repair_lo"], self.P["repair_hi"] + 1))
            self.repair_due[b] = m + days * 1440 + int(rb.integers(-180, 180))

    def depot_ready(self):
        return [b for b in self.depot if b not in self.broken]

    def finish_repairs(self, m):
        for b in [b for b, d in self.repair_due.items() if d <= m]:
            self.broken.discard(b)
            self.flagged.discard(b)
            del self.repair_due[b]

    def tick(self):
        self.seq += 1
        return self.seq

    def log_move(self, m, van, station, action, bikes):
        for b in bikes:
            self.moves.append(dict(minute=m, van=van, station=station, action=action, bike=b, seq=self.tick()))

    def van_visit(self, m, s, van, target, p_find):
        rf = self.r(4, s)
        found = [b for b in self.docked[s] if b in self.broken and (b in self.flagged or (self.idle(s, b) and rf.random() < p_find))]
        for b in found:
            self.docked[s].remove(b)
            self.to_depot(b, m, True)
        self.log_move(m, van, s, "pickup", found)
        n = len(self.docked[s])
        if n < target:
            ready = self.depot_ready()
            take = ready[: max(0, min(target - n, len(ready)))]
            for b in take:
                self.depot.remove(b)
                self.docked[s].append(b)
                self.dock_min[b] = m
            self.log_move(m, van, s, "drop", take)
        elif n > target:
            # the crew pulls the bikes nearest the van, the ones docked last
            extra = [b for b in reversed(self.docked[s]) if b not in self.broken][: n - target]
            for b in extra:
                self.docked[s].remove(b)
                self.to_depot(b, m, False)
            self.log_move(m, van, s, "pickup", extra)

    def idle(self, s, b):
        """on the operator's idle-bike list: a renter took another bike at its station after it was docked"""
        return self.last_rent.get(s, -1) > self.dock_min.get(b, 10 ** 9)

    def check_visit(self, m, s):
        found = [b for b in self.docked[s] if b in self.broken and (b in self.flagged or self.idle(s, b))]
        for b in found:
            self.docked[s].remove(b)
            self.to_depot(b, m, True)
        self.log_move(m, "V%d" % (1 + (s + m // 1440) % 3), s, "pickup", found)

    def nearest_free(self, s):
        a = self.st[s]
        for x in sorted(self.station_ids(), key=lambda x: (self.st[x]["x"] - a["x"]) ** 2 + (self.st[x]["y"] - a["y"]) ** 2):
            if len(self.docked[x]) < self.cap(x):
                return x
        return s

    # ----------------------------------------------------------------------------------------------------------
    def relocate(self, m):
        """Linden Avenue's bikes are moved by van to its new site across the street, under a new station id"""
        old, new = RELOCATION["old"], RELOCATION["new"]
        a = self.st[old]
        self.st[new] = dict(id=new, name=a["name"], kind=a["kind"], x=a["x"] + RELOCATION["dx"],
                            y=a["y"] + RELOCATION["dy"], cap=a["cap"])
        self.public.append(new)
        self.docked[new] = []
        for arr in (self.listed, self.work, self.disabled, self.docks):
            arr[new] = np.zeros(NMIN, dtype=np.int16)
        self.active[new] = np.zeros(NMIN, dtype=bool)
        moving = list(self.docked[old])
        self.docked[old] = []
        self.log_move(m, "V1", old, "pickup", moving)
        self.in_van = (m + 25, new, moving)
        self.st[old]["open"] = False
        self.mult[new] = self.mult.get(old, 1.0)
        self.relocated = True

    def run(self):
        rng = self.rng
        P = self.P
        lam_cache = {}
        day0 = DAY0
        rel_m = minute_of(RELOCATION["when"])
        exp_m = {minute_of(t): (s, c) for s, (t, c) in EXPANSIONS.items()}
        days = [DAY0 + dt.timedelta(days=int(k)) for k in range(int(LOCAL_DAY[-1]) + 1)]
        seen_midnight = set()
        for m in range(NMIN):
            mod = int(LOCAL_MOD[m])
            day = days[int(LOCAL_DAY[m])]
            weekend = day.weekday() >= 5
            if m == rel_m:
                self.relocate(m)
            if getattr(self, "in_van", None) and self.in_van[0] == m:
                _, new, moving = self.in_van
                self.docked[new].extend(moving)
                for b in moving:
                    self.dock_min[b] = m
                self.log_move(m, "V1", new, "drop", moving)
                self.in_van = None
            if m in exp_m:
                s, c = exp_m[m]
                self.st[s]["cap"] = c
            if mod == 0 and day not in seen_midnight:
                seen_midnight.add(day)
                self.finish_repairs(m)
                self.checks_today = []
                for s in self.station_ids():
                    inner = self.st[s]["kind"] in ("core", "hub", "campus")
                    every = 1 if inner else self.P["res_cycle"].get(s, 3)
                    lo, hi = (P["check_lo"], P["check_hi"]) if inner else (P["check_lo_res"], P["check_hi_res"])
                    if (day - day0).days % every == (s % every):
                        self.checks_today.append((int(self.r(3, s).integers(lo, hi)), s))
            for b in [b for b, d in self.flag_due.items() if d <= m]:
                if b in self.broken:
                    self.flagged.add(b)
                    where = next((s for s in self.public if b in self.docked[s]), None)
                    if where is not None:
                        self.flags.append(dict(minute=m, seq=self.tick(), bike=b, station=where))
                    if b in self.open_break and self.breaks[self.open_break[b]].get("flagged") is None:
                        self.breaks[self.open_break[b]]["flagged"] = m
                del self.flag_due[b]
            if mod == 4 * 60 + 30:
                for s in self.station_ids():
                    if self.st[s]["kind"] in ("res", "hub", "park", "campus"):
                        self.van_visit(m, s, "V1", int(P["fill_target"] * self.cap(s)), P["p_find_morning"])
                    elif len(self.docked[s]) > 0.8 * self.cap(s):
                        self.van_visit(m, s, "V2", int(0.6 * self.cap(s)), P["p_find_morning"])
            if day in STORAGE_NIGHTS and mod == 60:
                for s in self.station_ids():
                    keep = int(0.45 * self.cap(s))
                    if len(self.docked[s]) > keep:
                        self.van_visit(m, s, "V2", keep, 0.0)
            for (cm, s) in self.checks_today:
                if cm == mod and self.st[s].get("open", True):
                    self.check_visit(m, s)
            # trips ending
            for tid in [tid for tid, v in self.in_ride.items() if v[2] <= m]:
                b, dest, end, broke, rec, rep, fdelay = self.in_ride.pop(tid)
                if not self.st[dest].get("open", True):
                    dest = RELOCATION["new"]
                s = dest
                if len(self.docked[s]) >= self.cap(s) and not rec.get("diverted"):
                    # a full station: the rider rides on to the nearest free dock, four minutes on
                    s = self.nearest_free(s)
                    rec["end_minute"] = m + 4
                    rec["end_station"] = s
                    rec["diverted"] = True
                    self.in_ride[tid] = (b, s, m + 4, broke, rec, rep, fdelay)
                    continue
                if len(self.docked[s]) >= self.cap(s):
                    s = self.nearest_free(s)
                    rec["end_minute"] = m
                self.docked[s].append(b)
                self.dock_min[b] = m
                rec["end_station"] = s
                rec["end_seq"] = self.tick()
                if broke:
                    self.broken.add(b)
                    if rep:
                        self.flag_due[b] = m + fdelay
                        self.reports.append(dict(minute=rec["end_minute"], bike=b, station=s, how="ride"))
                    self.open_break[b] = len(self.breaks)
                    self.breaks.append(dict(bike=b, station=s, docked=rec["end_minute"], reported=rep, removed=None,
                                            flagged=None))
            # alerts on the feed's counts
            if SERVICE[0] <= mod < SERVICE[1] - 30:
                for s in self.station_ids():
                    if s in self.pending:
                        kind, due = self.pending[s]
                        if due <= m:
                            del self.pending[s]
                            tgt = P["alert_fill"] if kind == "empty" else P["full_trim"]
                            self.van_visit(m, s, "V3", int(tgt * self.cap(s)), P["p_find_alert"])
                        continue
                    delay = int(self.r(6, s).integers(P["alert_lo"], P["alert_hi"])) + P["queue_step"] * max(0, len(self.pending) - 1)
                    if self.listed_n(s) == 0:
                        self.pending[s] = ("empty", m + delay)
                    elif len(self.docked[s]) >= self.cap(s):
                        self.pending[s] = ("full", m + delay)
            # renters arrive
            hour = mod // 60
            key = (hour, weekend, day.month, self.wx[day], self.relocated)
            ids = self.station_ids()
            if key not in lam_cache:
                lam_cache[key] = np.array([DAILY[self.st[s]["kind"]] * self.mult.get(s, 1.0)
                                           * profile(self.st[s]["kind"], weekend)[hour]
                                           / profile(self.st[s]["kind"], weekend).sum() / 60.0
                                           * MONTH_SCALE[day.month] * self.wx[day] for s in ids])
            lam = lam_cache[key]
            for i, s in enumerate(ids):
                k_arr = int(self.r(1, s).poisson(lam[i]))
                rr = self.r(2, s)
                for _ in range(k_arr):
                    want = "e" if rr.random() < P["prefer_e"] else "classic"
                    pool = self.working(s, want)
                    if not pool:
                        other = "classic" if want == "e" else "e"
                        pool = self.working(s, other) if rr.random() < P["take_other"] else []
                    if not pool:
                        self.lost[(s, day)] += 1
                        seen = [b for b in self.docked[s] if b in self.broken and b not in self.flagged
                                and b not in self.flag_due]
                        if seen and rr.random() < P["p_report_seen"]:
                            self.flag_due[seen[0]] = m + int(rr.integers(P["flag_lo"], P["flag_hi"]))
                            self.reports.append(dict(minute=m, bike=seen[0], station=s, how="seen"))
                        continue
                    b = pool[int(rr.integers(len(pool)))]
                    self.docked[s].remove(b)
                    self.last_rent[s] = m
                    w = dest_weights(self.st[s]["kind"], hour, weekend)
                    cands = [x for x in ids if x != s]
                    wt = np.array([w[self.st[x]["kind"]] for x in cands], dtype=float)
                    dest = cands[int(rr.choice(len(cands), p=wt / wt.sum()))]
                    a, c = self.st[s], self.st[dest]
                    km = 1.25 * math.hypot(a["x"] - c["x"], a["y"] - c["y"]) + 0.2
                    speed = 17.0 if self.btype[b] == "e" else 12.0
                    dur = max(2, int(round(km / speed * 60 * rr.lognormal(0, 0.18))))
                    broke = rr.random() < (P["break_per_km"] * km if P.get("break_per_km") else P["p_break"])
                    rep = rr.random() < P["p_report"]
                    fdelay = int(rr.integers(P["flag_lo"], P["flag_hi"]))
                    self.trip_id += 1
                    rec = dict(trip=self.trip_id, bike=b, btype=self.btype[b], start_station=s, start_minute=m,
                               end_station=dest, end_minute=m + dur,
                               user="staff" if rr.random() < P["p_staff"] else "rider", start_seq=self.tick())
                    self.trips.append(rec)
                    self.in_ride[self.trip_id] = (b, dest, m + dur, broke, rec, rep, fdelay)
            for s in self.station_ids():
                d = self.docked[s]
                nl = nw = nd = 0
                for b in d:
                    if b in self.flagged:
                        nd += 1
                    else:
                        nl += 1
                    if b not in self.broken:
                        nw += 1
                self.listed[s][m] = nl
                self.work[s][m] = nw
                self.disabled[s][m] = nd
                self.docks[s][m] = self.cap(s) - len(d)
                self.active[s][m] = True
        return self


# ---------------------------------------------------------------------------------------------------------------
def month_minutes(mo):
    """the minutes of a month's service hours (6:00 to midnight local); minute m holds the state at the start of
    the minute that follows it, so the service minute starting at 6:00 is the state recorded at 5:59"""
    a = minute_of(dt.datetime(2026, mo, 1))
    b = minute_of(dt.datetime(2026, mo + 1, 1)) if mo < 12 else minute_of(QEND)
    idx = np.arange(a, b)
    mod = TRUE_MOD[idx]
    return idx[(mod >= SERVICE[0]) & (mod < SERVICE[1])] - 1


PEAKS = ((7 * 60, 10 * 60), (16 * 60, 19 * 60))


def peak_minutes(mo):
    """the weekday peak minutes of a month (7:00 to 10:00 and 16:00 to 19:00 local)"""
    a = minute_of(dt.datetime(2026, mo, 1))
    b = minute_of(dt.datetime(2026, mo + 1, 1)) if mo < 12 else minute_of(QEND)
    idx = np.arange(a, b)
    mod = TRUE_MOD[idx]
    wdm = np.array([(DAY0 + dt.timedelta(days=int(k))).weekday() < 5 for k in TRUE_DAY[idx]])
    inpk = np.zeros(len(idx), dtype=bool)
    for lo, hi in PEAKS:
        inpk |= (mod >= lo) & (mod < hi)
    return idx[inpk & wdm]


def station_series(f, arr, name):
    """a public station's series across a relocation (the old id until it closed, the new one after)"""
    ids = [s for s in f.public if f.st[s]["name"] == name]
    out = np.zeros(NMIN, dtype=np.int32)
    for s in ids:
        out += np.where(f.active[s], arr[s], 0)
    return out


def availability(f, arr, months=MONTHS, peak=False):
    out = {}
    pick = peak_minutes if peak else month_minutes
    names = []
    for s in f.public:
        if f.st[s]["name"] not in names:
            names.append(f.st[s]["name"])
    for name in names:
        ser = station_series(f, arr, name)
        out[name] = {mo: 100.0 * float((ser[pick(mo)] >= 1).mean()) for mo in months}
    return out


def designated(av, line=90.0):
    return sorted(n for n, d in av.items() if min(d.values()) < line)


_FLEET = {}


def fleet(seed=SEED):
    """the fleet run once per process (a run takes about half a minute)"""
    if seed not in _FLEET:
        _FLEET[seed] = Fleet(seed).run()
    return _FLEET[seed]


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    f = Fleet(int(sys.argv[1]) if len(sys.argv) > 1 else SEED).run()
    print("ran in %.1fs: trips %d, breaks %d (reported %d), moves %d" % (
        time.time() - t0, len(f.trips), len(f.breaks), sum(1 for b in f.breaks if b["reported"]), len(f.moves)))
    d = availability(f, f.listed)
    g = availability(f, f.work)
    for n in d:
        print("%-20s" % n, " ".join("%5.1f/%5.1f" % (d[n][mo], g[n][mo]) for mo in MONTHS))
    print("default", designated(d))
    print("golden ", designated(g))
