"""Tamsett District's March 2027 pothole detection pilot, before any file is written: the road network and its 2025
to 2026 renumbering, the pilot fleet and its Kerbline units, every vehicle's March driving, the potholes and other
defects on the roadway, what each unit saw, the district's review of the pothole reports, the units' platform
sessions and the cold patch work orders.

One generating process, fixed seeds, one RNG stream per component, so two builds are identical."""
import datetime as dt
import math

import numpy as np
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
SEED = 4782027

# The capture process: a unit either can or cannot see a given defect from where its phone sits on its vehicle
# (fixed for the installation); a unit that can see it records it on a pass with probability R_PASS.
Q_SEE = 0.56
R_PASS = 0.95
LINE = 6.0

MARCH = [dt.date(2027, 3, d) for d in range(1, 32)]
DST_DAY = dt.date(2027, 3, 14)
MIGRATION_UTC = dt.datetime(2027, 3, 17, 9, 0, tzinfo=UTC)          # Kerbline's platform migration
TURNBACK = dt.date(2027, 3, 15)                                      # route turnback to the City of Tamsett
STORM_NIGHTS = [dt.date(2027, 3, 5), dt.date(2027, 3, 26)]          # Friday nights of the two snow events
REPLAY_FROM = dt.datetime(2027, 3, 12, 0, 0, tzinfo=UTC)            # telematics re-processed block
REPLAY_TO = dt.datetime(2027, 3, 13, 6, 0, tzinfo=UTC)
EXPORT_FROM = dt.datetime(2027, 2, 28, 0, 0, tzinfo=UTC)
EXPORT_TO = dt.datetime(2027, 4, 2, 0, 0, tzinfo=UTC)

DISTRICT = "Tamsett District"
DOT = "State Department of Transportation"
CITY = "City of Tamsett"
VENDOR = "Kerbline Vision"
PEOPLE = {"engineer": "Nancy Hansen", "analyst": "Andrew Greene"}
DAY_RATE = 10.85

# no, name, kind (U metro, S suburban, R rural), mean potholes per ten lane-miles, crew-truck reach, tuning centre
SECTIONS = [
    (403, "Carrow Point", "U", 8.0, 0.0, 8),
    (407, "Elmscourt", "U", 9.0, 0.0, 9),
    (411, "Rushmead", "U", 5.0, 0.0, 5),
    (402, "Fenwick Gap", "S", 7.0, 0.40, 7),
    (409, "Thistlebank", "S", 8.0, 0.30, 8),
    (405, "Marlpit", "S", 4.0, 0.55, 4),
    (412, "Stonebeck", "S", 3.0, 0.45, 3),
    (414, "Pyke Hill", "S", 2.0, 0.50, 2),
    (401, "Holloway Run", "R", 8.0, 0.18, 8),
    (406, "Kestrelton", "R", 7.0, 0.32, 7),
    (413, "Norvelle", "R", 8.0, 0.24, 8),
    (404, "Grisholt", "R", 4.0, 0.28, 4),
    (408, "Halverton", "R", 3.0, 0.27, 3),
    (410, "Oxbrae", "R", 4.0, 0.25, 4),
]
SEC = {s[0]: dict(no=s[0], name=s[1], kind=s[2], target=s[3], reach=s[4], whole=s[5]) for s in SECTIONS}
ORDER = [s[0] for s in SECTIONS]

ROUTES = {
    403: [("SR 9", "FWY"), ("SR 30", "FWY"), ("SR 11", "ART"), ("SR 24", "ART")],
    407: [("SR 9", "FWY"), ("SR 52", "ART"), ("SR 11", "ART"), ("SR 63", "ART")],
    411: [("SR 30", "FWY"), ("SR 24", "ART"), ("SR 63", "ART"), ("SR 71", "ART")],
    402: [("SR 104", "SUB"), ("SR 117", "SUB"), ("SR 52", "SUB"), ("SR 129", "SUB")],
    409: [("SR 136", "SUB"), ("SR 141", "SUB"), ("SR 104", "SUB")],
    405: [("SR 158", "SUB"), ("SR 117", "SUB"), ("SR 163", "SUB"), ("SR 71", "SUB")],
    412: [("SR 129", "SUB"), ("SR 172", "SUB"), ("SR 136", "SUB")],
    414: [("SR 158", "SUB"), ("SR 181", "SUB"), ("SR 141", "SUB"), ("SR 63", "SUB")],
    401: [("SR 207", "RUR"), ("SR 214", "RUR"), ("SR 172", "RUR")],
    406: [("SR 226", "RUR"), ("SR 233", "RUR"), ("SR 181", "RUR"), ("SR 214", "RUR")],
    413: [("SR 248", "RUR"), ("SR 259", "RUR"), ("SR 207", "RUR")],
    404: [("SR 271", "RUR"), ("SR 286", "RUR"), ("SR 226", "RUR")],
    408: [("SR 292", "RUR"), ("SR 248", "RUR"), ("SR 233", "RUR"), ("SR 305", "RUR")],
    410: [("SR 311", "RUR"), ("SR 286", "RUR"), ("SR 259", "RUR")],
}
LANE_MILES = {"U": 262.0, "S": 171.0, "R": 131.0}
SPEED = {"FWY": 52.0, "ART": 24.0, "SUB": 36.0, "RUR": 44.0}
CENTER = (41.214, -77.062)


def rng(*keys):
    return np.random.default_rng([SEED] + [int(k) for k in keys])


def local(t):
    return t.astimezone(TZ)


def utc_of(day, hour, minute=0, second=0):
    """A local wall-clock time on a day as a UTC datetime."""
    return dt.datetime(day.year, day.month, day.day, int(hour), int(minute), int(second), tzinfo=TZ).astimezone(UTC)


# ----------------------------------------------------------------------------------------------- the network
def network():
    """Segments of the 2026 road inventory (state routes in the fourteen sections), the 2025 inventory they were
    renumbered from, and the route turnback segments."""
    r = rng(1)
    segs = []
    sec_pos = {}
    k = 0
    ring = {"U": 0.07, "S": 0.22, "R": 0.45}
    counts = {"U": 0, "S": 0, "R": 0}
    for no in ORDER:
        kind = SEC[no]["kind"]
        ang = 2 * math.pi * counts[kind] / {"U": 3, "S": 5, "R": 6}[kind] + {"U": 0.4, "S": 0.9, "R": 0.2}[kind]
        counts[kind] += 1
        sec_pos[no] = (CENTER[0] + ring[kind] * math.sin(ang), CENTER[1] + 1.32 * ring[kind] * math.cos(ang))
    next_id = 2210437
    route_end = {}
    for no in ORDER:
        kind = SEC[no]["kind"]
        target = LANE_MILES[kind] * r.uniform(0.93, 1.07)
        routes = ROUTES[no]
        lm = 0.0
        per_route = {rt: [] for rt, _ in routes}
        start_mp = {}
        for rt, _ in routes:
            base = route_end.get(rt)
            start_mp[rt] = round(float(r.uniform(0.6, 9.0)) if base is None else base + float(r.uniform(1.5, 7.0)), 3)
        heading = {rt: float(r.uniform(0, 2 * math.pi)) for rt, _ in routes}
        i = 0
        while lm < target:
            rt, cls = routes[i % len(routes)] if r.random() < 0.8 else routes[int(r.integers(len(routes)))]
            i += 1
            if cls == "FWY":
                length, lanes = r.uniform(0.25, 1.1), int(r.choice([6, 8], p=[0.6, 0.4]))
            elif cls == "ART":
                length, lanes = r.uniform(0.18, 0.85), int(r.choice([4, 5, 3], p=[0.6, 0.25, 0.15]))
            elif cls == "SUB":
                length, lanes = r.uniform(0.3, 1.45), int(r.choice([2, 3, 4], p=[0.62, 0.13, 0.25]))
            else:
                length, lanes = r.uniform(0.55, 2.4), int(r.choice([2, 3], p=[0.94, 0.06]))
            length = round(float(length), 3)
            prev = per_route[rt][-1]["emp"] if per_route[rt] else start_mp[rt]
            seg = dict(seg=next_id, sec=no, route=rt, route_num=int(rt.split()[1]), cls=cls, bmp=round(prev, 3),
                       emp=round(prev + length, 3), length=length, lanes=lanes, juris="STATE", turnback=False, k=k)
            next_id += int(r.integers(3, 41))
            k += 1
            per_route[rt].append(seg)
            segs.append(seg)
            lm += length * lanes
        for rt, _ in routes:
            if per_route[rt]:
                route_end[rt] = per_route[rt][-1]["emp"]
            for j, s in enumerate(per_route[rt]):
                s["route_seq"] = j
                s["heading"] = heading[rt]
                s["origin"] = (sec_pos[no][0] + float(r.uniform(-0.02, 0.02)), sec_pos[no][1] + float(r.uniform(-0.025, 0.025)))
                s["route_start"] = start_mp[rt]
    # route turnback: arterial segments in Rushmead and Elmscourt handed to the City on 15 March
    arts = [s for s in segs if s["cls"] == "ART" and s["sec"] in (411, 407)]
    for s in sorted(arts, key=lambda s: (s["sec"], s["route"], s["bmp"]))[3:8]:
        s["turnback"] = True
    # the 2025 inventory: most segments kept their ids; some 2026 segments were split out of one 2025 segment, and
    # a few 2025 pairs were merged into one 2026 segment
    r2 = rng(2)
    seg25 = []
    by_route = {}
    for s in segs:
        by_route.setdefault((s["sec"], s["route"]), []).append(s)
    nid = 1874210
    used = set()
    for key in sorted(by_route):
        run = sorted(by_route[key], key=lambda s: s["bmp"])
        j = 0
        while j < len(run):
            s = run[j]
            u = r2.random()
            if u < 0.016 and j + 1 < len(run):
                # one 2025 segment split into these two 2026 segments
                a, b = run[j], run[j + 1]
                pid = nid
                nid += int(r2.integers(5, 60))
                seg25.append(dict(seg25=pid, route=s["route"], sec=s["sec"], bmp=a["bmp"], emp=b["emp"],
                                  children=[(a["seg"], a["bmp"], a["emp"]), (b["seg"], b["bmp"], b["emp"])], kind="SPLIT"))
                a["seg25"] = pid
                b["seg25"] = pid
                j += 2
            elif u < 0.025:
                # two 2025 segments merged into this 2026 segment
                cut = round(s["bmp"] + s["length"] * float(r2.uniform(0.3, 0.7)), 3)
                p1, p2 = nid, nid + int(r2.integers(2, 9))
                nid = p2 + int(r2.integers(5, 60))
                seg25.append(dict(seg25=p1, route=s["route"], sec=s["sec"], bmp=s["bmp"], emp=cut,
                                  children=[(s["seg"], s["bmp"], cut)], kind="MERGE"))
                seg25.append(dict(seg25=p2, route=s["route"], sec=s["sec"], bmp=cut, emp=s["emp"],
                                  children=[(s["seg"], cut, s["emp"])], kind="MERGE"))
                s["seg25"] = None
                s["merged_from"] = (p1, p2, cut)
                j += 1
            else:
                seg25.append(dict(seg25=s["seg"], route=s["route"], sec=s["sec"], bmp=s["bmp"], emp=s["emp"],
                                  children=[(s["seg"], s["bmp"], s["emp"])], kind="SAME"))
                s["seg25"] = s["seg"]
                j += 1
    for x in seg25:
        assert x["seg25"] not in used
        used.add(x["seg25"])
    return segs, seg25, sec_pos


def latlon(s, mp):
    d = mp - s["route_start"]
    lat = s["origin"][0] + d / 69.0 * math.sin(s["heading"])
    lon = s["origin"][1] + d / 52.2 * math.cos(s["heading"])
    return round(lat, 6), round(lon, 6)


# ------------------------------------------------------------------------------------------------- the fleet
def fleet(segs):
    """Vehicles with Kerbline units and their install periods."""
    r = rng(3)
    vehicles = []
    fleet_no = iter(sorted(set(int(x) for x in r.integers(21040, 29890, 80)))[:60])
    serials = iter(sorted(set(int(x) for x in r.integers(30410, 30990, 70)))[:50])
    for no in sorted(ORDER):
        vehicles.append(dict(veh="4-%d" % next(fleet_no), group="PATROL", desc="Ford F-250 crew cab, section patrol",
                             home=no))
    urban = [n for n in ORDER if SEC[n]["kind"] == "U"]
    for j in range(6):
        vehicles.append(dict(veh="4-%d" % next(fleet_no), group="FSP", desc="Freightliner M2 service patrol",
                             home=urban[j % 3]))
    for j in range(6):
        vehicles.append(dict(veh="4-%d" % next(fleet_no), group="SWEEPER", desc="Elgin Pelican street sweeper",
                             home=urban[j // 2]))
    crews = ["Sign crew", "Sign crew", "Guide rail crew", "Guide rail crew", "Bridge crew", "Bridge crew",
             "Drainage crew", "Drainage crew"]
    for j in range(8):
        vehicles.append(dict(veh="4-%d" % next(fleet_no), group="CREW", desc="International CV, %s" % crews[j].lower(),
                             home=None))
    late = {vehicles[k]["veh"] for k in (27, 29, 31, 33)}
    for v in vehicles:
        v["unit"] = "KV-%d" % next(serials)
        if v["veh"] in late:
            v["installed"] = dt.date(2027, 3, 9)
        else:
            v["installed"] = dt.date(2027, 2, 22) + dt.timedelta(int(r.integers(0, 4)))
        v["removed"] = None
    # the six sweepers' units: two came off on 25 March, when those sweepers went in for their spring overhaul
    sw = [v for v in vehicles if v["group"] == "SWEEPER"]
    sw[1]["removed"] = dt.date(2027, 3, 25)
    sw[4]["removed"] = dt.date(2027, 3, 25)
    return vehicles


def installed_at(v, t_utc):
    d = local(t_utc).date()
    if d < v["installed"]:
        return False
    if v["removed"] is not None and d >= v["removed"]:
        return False
    return True


# -------------------------------------------------------------------------------------------- the driving
def _dir(s, forward):
    """The traversal's direction as the route's own cardinal pair: increasing milepost runs north or east."""
    h = s["heading"] % (2 * math.pi)
    ns = abs(math.sin(h)) >= abs(math.cos(h))
    up = ("NB" if math.sin(h) >= 0 else "SB") if ns else ("EB" if math.cos(h) >= 0 else "WB")
    flip = {"NB": "SB", "SB": "NB", "EB": "WB", "WB": "EB"}
    return up if forward else flip[up]


def _trip(path, start_utc, speeds, r, out, veh):
    """Traverse a list of segments in order from start_utc, appending traversals; returns the end time."""
    forward = len(path) < 2 or path[0]["bmp"] <= path[-1]["bmp"]
    t = start_utc
    for s in path:
        mph = speeds[s["cls"]] * float(r.uniform(0.82, 1.12))
        t2 = t + dt.timedelta(seconds=round(s["length"] / mph * 3600.0, 1))
        out.append(dict(veh=veh, seg=s["seg"], enter=t, exit=t2, dir=_dir(s, forward), fwd=forward))
        t = t2 + dt.timedelta(seconds=round(float(r.uniform(4, 40)), 1))
    return t


def workday(d):
    return d.weekday() < 5


def driving(segs, vehicles):
    """Every traversal of a state segment by a pilot vehicle from 27 February to 1 April (local), with UTC enter
    and exit times, and each vehicle's ignition-on periods (the units power with the vehicle)."""
    by_route = {}
    for s in segs:
        by_route.setdefault((s["sec"], s["route"]), []).append(s)
    for key in by_route:
        by_route[key].sort(key=lambda s: s["bmp"])
    days = [dt.date(2027, 2, 27) + dt.timedelta(k) for k in range(34)]
    trav, ign = [], []
    urban = [n for n in ORDER if SEC[n]["kind"] == "U"]

    def drive(v, paths, start, r, speeds=SPEED, gap=(3, 25)):
        t = start
        n0 = len(trav)
        for path in paths:
            t = _trip(path, t, speeds, r, trav, v["veh"])
            t = t + dt.timedelta(seconds=round(float(r.uniform(gap[0], gap[1])) * 60, 1))
        return trav[n0]["enter"], trav[-1]["exit"]

    def on(v, a, b, r, pre=(6, 22), post=(8, 30)):
        ign.append(dict(veh=v["veh"], start=a - dt.timedelta(seconds=round(float(r.uniform(*pre)) * 60)),
                        end=b + dt.timedelta(seconds=round(float(r.uniform(*post)) * 60))))

    for vi, v in enumerate(vehicles):
        r = rng(10, vi)
        g = v["group"]
        if g == "PATROL":
            no = v["home"]
            routes = sorted({rt for (sec, rt) in by_route if sec == no})
            share = {"U": 0.5, "S": 0.4, "R": 0.32}[SEC[no]["kind"]]
            done = set()
            for d in days:
                if workday(d):
                    wk = d.isocalendar()[1]
                    todays = [rt for rt in routes if r.random() < share or (wk, rt) not in done]
                    todays = todays or [routes[int(r.integers(len(routes)))]]
                    paths = []
                    for rt in todays:
                        run_ = by_route[(no, rt)]
                        if (wk, rt) not in done:
                            seg_run = run_
                            done.add((wk, rt))
                        else:
                            a = int(r.integers(0, max(1, len(run_) // 3)))
                            b = len(run_) - int(r.integers(0, max(1, len(run_) // 4)))
                            seg_run = run_[a:b] if b > a else run_
                        paths += [seg_run, list(reversed(seg_run))]
                    f, e = drive(v, paths, utc_of(d, 7, int(r.integers(5, 50))), r)
                    on(v, f, e, r)
                if d in STORM_NIGHTS:
                    paths = []
                    for rt in routes:
                        run_ = by_route[(no, rt)]
                        paths += [run_, list(reversed(run_))]
                    f, e = drive(v, paths, utc_of(d, 19, int(r.integers(0, 40))), r)
                    while local(e).date() == d or local(e).hour < 1:
                        _, e = drive(v, paths[:2], e + dt.timedelta(minutes=20), r)
                    on(v, f, e, r, pre=(10, 14), post=(10, 25))
        elif g == "FSP":
            beat_secs = [v["home"]] + ([urban[(urban.index(v["home"]) + 1) % 3]] if r.random() < 0.5 else [])
            beat = [run_ for (sec, rt), run_ in sorted(by_route.items()) if sec in beat_secs and run_[0]["cls"] == "FWY"]
            for d in days:
                if not workday(d):
                    continue
                paths = []
                for run_ in beat:
                    paths += [run_, list(reversed(run_))]
                for (h0, h1) in ((6, 9), (15, 18)):
                    f, e = drive(v, paths, utc_of(d, h0, int(r.integers(0, 30))), r, gap=(10, 40))
                    while local(e).hour < h1:
                        _, e = drive(v, paths, e + dt.timedelta(minutes=float(r.uniform(10, 40))), r, gap=(10, 40))
                    on(v, f, e, r, pre=(5, 15), post=(5, 20))
                if d.weekday() == 4 and r.random() < 0.55:
                    # Friday night lane-closure cover, past midnight
                    p2 = [beat[0], list(reversed(beat[0]))]
                    f, e = drive(v, p2, utc_of(d, 22, int(r.integers(5, 40))), r, gap=(15, 45))
                    while local(e).date() == d or local(e).hour < 1:
                        _, e = drive(v, p2, e + dt.timedelta(minutes=float(r.uniform(15, 45))), r, gap=(15, 45))
                    on(v, f, e, r, pre=(8, 12), post=(5, 15))
        elif g == "SWEEPER":
            no = v["home"]
            arts = [run_ for (sec, rt), run_ in sorted(by_route.items()) if sec == no and run_[0]["cls"] == "ART"]
            sp = {"ART": 7.0, "FWY": 30.0, "SUB": 20.0, "RUR": 25.0}
            for d in days:
                if d.weekday() not in (6, 0, 1, 2, 3):
                    continue
                if v["removed"] is not None and d >= v["removed"] - dt.timedelta(1):
                    continue
                if d in (dt.date(2027, 2, 28), dt.date(2027, 3, 31)):
                    continue     # the spring sweeping schedule ran Monday 1 March to Tuesday 30 March nights
                paths = []
                for run_ in arts:
                    if r.random() < 0.5:
                        a = int(r.integers(0, len(run_)))
                        seg_run = run_[a:a + int(r.integers(3, 8))] or run_[-2:]
                        paths += [seg_run, list(reversed(seg_run))]
                if not paths:
                    paths = [arts[0][:3], list(reversed(arts[0][:3]))]
                f, e = drive(v, paths, utc_of(d, 22, int(r.integers(0, 35))), r, speeds=sp, gap=(5, 30))
                # the rest of the night is on city streets, outside the state export
                end = max(e, utc_of(d + dt.timedelta(1), 4, int(r.integers(30, 59))))
                on(v, f, end, r, pre=(12, 18), post=(4, 12))
        else:  # CREW
            pool = [n for n in ORDER if SEC[n]["kind"] != "U"]
            w = np.array([SEC[n]["reach"] for n in pool])
            jobs = []
            d0 = 0
            work = [d for d in days if workday(d)]
            visit = [pool[(vi * 3 + j) % len(pool)] for j in range(len(pool))]
            while d0 < len(work):
                dest = visit.pop(0) if visit and r.random() < 0.55 else int(r.choice(pool, p=w / w.sum()))
                routes = sorted({rt for (sec, rt) in by_route if sec == dest})
                rt = routes[int(r.integers(len(routes)))]
                run_ = by_route[(dest, rt)]
                end_at = int(r.integers(1, max(2, int(len(run_) * SEC[dest]["reach"] * 1.6) + 1)))
                length = int(r.integers(2, 6))
                jobs.append((work[d0:d0 + length], run_[:end_at]))
                d0 += length
            for jdays, seg_run in jobs:
                for d in jdays:
                    if d == v["installed"]:
                        continue     # the unit went on in the yard that day; the truck stayed in
                    f, e = drive(v, [seg_run], utc_of(d, 7, int(r.integers(10, 55))), r)
                    on(v, f, e, r, pre=(8, 25), post=(3, 9))
                    back = e + dt.timedelta(seconds=round(float(r.uniform(2.5, 5.5)) * 3600))
                    f2, e2 = drive(v, [list(reversed(seg_run))], back, r)
                    on(v, f2, e2, r, pre=(4, 12), post=(8, 25))
            for d in days:
                if d in STORM_NIGHTS and vi % 2 == 0:
                    # a call-out on the storm night: a knocked-down sign, out after 23:00
                    dest = int(r.choice([n for n in ORDER if SEC[n]["kind"] == "S"]))
                    routes = sorted({rt for (sec, rt) in by_route if sec == dest})
                    run_ = by_route[(dest, routes[int(r.integers(len(routes)))])][:2]
                    f, e = drive(v, [run_], utc_of(d, 23, int(r.integers(5, 40))), r)
                    back = e + dt.timedelta(seconds=round(float(r.uniform(40, 80)) * 60))
                    _, e2 = drive(v, [list(reversed(run_))], back, r)
                    on(v, f, e2, r, pre=(12, 16), post=(10, 20))
    trav = [t for t in trav if EXPORT_FROM <= t["enter"] < EXPORT_TO]
    trav.sort(key=lambda t: (t["enter"], t["veh"], t["seg"]))
    ign.sort(key=lambda s: (s["veh"], s["start"]))
    return trav, ign


# ------------------------------------------------------------------------------------- defects and capture
CLASSES = ["pothole", "alligator_cracking", "longitudinal_crack", "utility_cover", "patch", "edge_break", "debris"]


def looks_of(vehicles, trav):
    """seg -> unit -> the unit's passes over the segment in March (local) while installed."""
    looks = {}
    veh_unit = {v["veh"]: v for v in vehicles}
    for t in trav:
        v = veh_unit[t["veh"]]
        if not installed_at(v, t["enter"]) or local(t["enter"]).date().month != 3:
            continue
        looks.setdefault(t["seg"], {}).setdefault(v["unit"], []).append(t)
    return looks


def section_potholes(no, segs, looks, offset):
    """The potholes on one section's segments and what each unit recorded of them; offset picks the stream."""
    out = []
    for s in segs:
        if s["sec"] != no:
            continue
        r = rng(20, s["k"], offset)
        lam = SEC[no]["target"] / 10.0 * s["length"] * s["lanes"] * float(r.gamma(9.0, 1 / 9.0))
        n = int(r.poisson(lam))
        units = looks.get(s["seg"], {})
        for i in range(n):
            mp = round(float(r.uniform(s["bmp"] + 0.012, s["emp"] - 0.012)), 3)
            seen = {}
            for u in sorted(units):
                vis = r.random() < Q_SEE
                seen[u] = [p for p in units[u] if vis and r.random() < R_PASS]
            out.append(dict(seg=s["seg"], sec=no, mp=mp, cls="pothole", real=True, seen=seen,
                            severity=int(r.choice([1, 2, 3], p=[0.38, 0.44, 0.18]))))
    return out


def other_defects(segs, looks):
    """Cracking, utility covers, old patches, edge breaks and debris: what the units also record."""
    out = []
    for s in segs:
        other = {"alligator_cracking": 0.9, "longitudinal_crack": 1.1,
                 "utility_cover": 0.9 if s["cls"] in ("ART", "SUB") else 0.15, "patch": 0.8,
                 "edge_break": 0.6 if s["cls"] == "RUR" else 0.1, "debris": 0.25}
        r2 = rng(21, s["k"])
        units = looks.get(s["seg"], {})
        for c, rate in other.items():
            m = int(r2.poisson(rate / 10.0 * s["length"] * s["lanes"]))
            for i in range(m):
                mp = round(float(r2.uniform(s["bmp"] + 0.012, s["emp"] - 0.012)), 3)
                seen = {}
                for u in sorted(units):
                    vis = r2.random() < (0.62 if c != "debris" else 0.5)
                    hits = [p for p in units[u] if vis and r2.random() < 0.93]
                    seen[u] = hits[:1] if c == "debris" else hits
                out.append(dict(seg=s["seg"], sec=s["sec"], mp=mp, cls=c, real=False, seen=seen, severity=1))
    return out


def detected(d):
    return any(d["seen"][u] for u in d["seen"])
