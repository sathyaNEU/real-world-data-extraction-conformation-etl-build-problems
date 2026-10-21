"""The records each system writes from the world: Kerbline's detections and defect numbers (renumbered at the
17 March platform migration), the district's review of the pothole reports, the units' platform sessions, the MMS
cold patch work orders, the telematics provider's re-processed block, and the two files nobody needs for the call
(the 2026 pavement condition survey and the winter operations log)."""
import datetime as dt
import json
import math
import os

import numpy as np

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def everything():
    """The whole world and its records, built once."""
    segs, seg25, sec_pos = W.network()
    veh = W.fleet(segs)
    trav, ign = W.driving(segs, veh)
    looks = W.looks_of(veh, trav)
    tune = {int(k): v for k, v in json.load(open(os.path.join(HERE, "tune.json"))).items()}
    pots = []
    for no in W.ORDER:
        pots += W.section_potholes(no, segs, looks, tune[no], veh_group={v["unit"]: v["group"] for v in veh})
    # two potholes never share a route milepost to the thousandth: the later one moves along a few feet
    S = {s["seg"]: s for s in segs}
    taken = set()
    for d in sorted(pots, key=lambda d: (S[d["seg"]]["route"], d["mp"], d["seg"])):
        key = (S[d["seg"]]["route"], round(d["mp"], 3))
        while key in taken:
            d["mp"] = round(d["mp"] + 0.002, 3)
            key = (S[d["seg"]]["route"], d["mp"])
        assert d["mp"] < S[d["seg"]]["emp"] - 0.004
        taken.add(key)
    others = W.other_defects(segs, looks)
    e = dict(segs=segs, seg25=seg25, veh=veh, trav=trav, ign=ign, looks=looks, pots=pots, others=others,
             S={s["seg"]: s for s in segs}, unit_veh={v["unit"]: v for v in veh},
             veh_by={v["veh"]: v for v in veh})
    kerbline(e)
    covers(e)
    sessions(e)
    work_orders(e)
    loops(e)
    replay(e)
    distractors(e)
    return e


# ------------------------------------------------------------------------------------------------ Kerbline
OFF_ROADS = ["Hollis Ave", "Granger St", "Mill Race Rd", "County Rd 31", "Quarry Ln", "Depot St", "Wharton Ave",
             "County Rd 18", "Fairview Ter", "Lockhart St", "Bell Hill Rd", "Union St"]


def _seg25_of(e, s, mp):
    """The 2025 segment holding a milepost on a 2026 segment."""
    for x in e["seg25_by_child"][s["seg"]]:
        lo, hi = x[1], x[2]
        if lo - 1e-9 <= mp <= hi + 1e-9:
            return x[0]
    raise AssertionError((s["seg"], mp))


def _route_seg(e, route, mp):
    """The 2026 state segment of a route holding a milepost, or None between sections' pieces of the route."""
    for x in e["by_route"].get(route, []):
        if x["bmp"] - 1e-9 <= mp <= x["emp"] + 1e-9:
            return x
    return None


def kerbline(e):
    """Kerbline's detections: one per unit per defect per local day (the platform keeps the first), each placed where
    the unit's GPS fix put it, and the defect numbers the platform keeps for itself."""
    r = W.rng(30)
    by_child = {}
    for x in e["seg25"]:
        for ch, lo, hi in x["children"]:
            by_child.setdefault(ch, []).append((x["seg25"], lo, hi))
    e["seg25_by_child"] = by_child
    by_route = {}
    for x in e["segs"]:
        by_route.setdefault(x["route"], []).append(x)
    e["by_route"] = by_route
    defects = []
    for d in e["pots"] + e["others"]:
        if not W.detected(d):
            continue
        defects.append(dict(src=d, seg=d["seg"], sec=d["sec"], mp=d["mp"], cls=d["cls"], k_cls=d["cls"], real=d["real"],
                            seen=d["seen"], off=False, route=e["S"][d["seg"]]["route"]))
    # potholes and other defects the sweepers and crew trucks recorded on city streets and county roads
    ign_by = {}
    for s in e["ign"]:
        ign_by.setdefault(s["veh"], []).append(s)
    off_units = [v for v in e["veh"] if v["group"] in ("SWEEPER", "CREW")]
    for j in range(64):
        v = off_units[int(r.integers(len(off_units)))]
        sess = [s for s in ign_by[v["veh"]] if W.installed_at(v, s["start"]) and W.local(s["start"]).month == 3
                and W.local(s["end"]).month == 3]
        s = sess[int(r.integers(len(sess)))]
        span = (s["end"] - s["start"]).total_seconds()
        t = s["start"] + dt.timedelta(seconds=round(float(r.uniform(0.15, 0.85)) * span))
        cls = "pothole" if r.random() < 0.7 else str(r.choice(["utility_cover", "alligator_cracking"]))
        defects.append(dict(src=None, seg=None, sec=None, mp=None, cls=cls, k_cls=cls,
                            real=cls == "pothole", off=True, route=OFF_ROADS[j % len(OFF_ROADS)],
                            seen={v["unit"]: [dict(veh=v["veh"], enter=t, exit=t + dt.timedelta(seconds=9), seg=None,
                                                   dir=None, fwd=True)]},
                            lat=round(W.CENTER[0] + float(r.uniform(-0.3, 0.3)), 6),
                            lon=round(W.CENTER[1] + float(r.uniform(-0.4, 0.4)), 6)))
    order = sorted(defects, key=lambda d: (min(p["enter"] for u in d["seen"] for p in d["seen"][u]), str(d["route"]),
                                           d["mp"] or 0))
    taken = set()
    for d in order:
        d["first"] = min(p["enter"] for u in d["seen"] for p in d["seen"][u])
        while True:
            n = int(r.integers(27310000, 27989999))
            if n not in taken:
                taken.add(n)
                d["id"] = n
                break
    e["defects"] = order
    rows = []
    det_id = 4100238117
    for d in order:
        s = e["S"].get(d["seg"]) if d["seg"] else None
        for u in sorted(d["seen"]):
            sig = W.SIGMA["SWEEPER" if e["unit_veh"][u]["group"] == "SWEEPER" else "OTHER"]
            days = set()
            for p in sorted(d["seen"][u], key=lambda p: p["enter"]):
                if s is not None:
                    frac = (d["mp"] - s["bmp"]) / s["length"]
                    f = frac if p["fwd"] else 1 - frac
                    t = p["enter"] + (p["exit"] - p["enter"]) * max(0.0, min(1.0, f - 0.008))
                else:
                    t = p["enter"]
                loc = W.local(t)
                if loc.date() in days or loc.month != 3:
                    continue
                days.add(loc.date())
                det_id += int(r.integers(3, 470))
                if s is not None:
                    fix = d["mp"] + float(r.normal(0, sig))
                    on = _route_seg(e, s["route"], fix) or s
                    fix = min(max(fix, on["bmp"] + 0.0005), on["emp"] - 0.0005)
                    lat, lon = W.latlon(on, fix)
                    road_mp = round(fix, 4)
                    road_ref = _seg25_of(e, on, road_mp)
                    lat, lon = lat + float(r.normal(0, 0.000025)), lon + float(r.normal(0, 0.00003))
                else:
                    lat, lon, road_mp, road_ref = d["lat"], d["lon"], None, None
                rows.append(dict(det=det_id, defect=d["id"], unit=u, t=t, lat=round(lat, 6), lon=round(lon, 6),
                                 road_ref=road_ref, road_mp=road_mp, route=d["route"], cls=d["k_cls"],
                                 conf=round(float(r.uniform(0.52, 0.98)), 2),
                                 sev=(d["src"]["severity"] if d["real"] and d["src"] is not None else int(r.choice([1, 2])))
                                 if d["k_cls"] == "pothole" else None))
    rows.sort(key=lambda x: (x["t"], x["det"]))
    e["detections"] = rows
    e["det_by"] = {}
    for x in rows:
        e["det_by"].setdefault(x["defect"], []).append(x)


# ------------------------------------------------------------------------------------------- the review queue
REVIEWERS = ["MPK", "MPK", "MPK", "DLW"]


def _business(t_utc, r):
    """The next time the reviewer is at the queue: weekdays 07:30 to 16:30 local."""
    t = W.local(t_utc)
    while True:
        if t.weekday() < 5 and (7, 30) <= (t.hour, t.minute) < (16, 30):
            return t.astimezone(W.UTC)
        nxt = t + dt.timedelta(minutes=30)
        if (nxt.hour, nxt.minute) >= (16, 30) or nxt.weekday() >= 5:
            day = (t + dt.timedelta(days=1)).date()
            t = dt.datetime(day.year, day.month, day.day, 7, 30, tzinfo=W.TZ) + dt.timedelta(minutes=int(r.integers(0, 50)))
        else:
            t = nxt


# ------------------------------------------------------------------------------------------------ sessions
def sessions(e):
    """Kerbline's platform sessions: a unit's session runs while its vehicle's ignition is on; before
    installation the vendor bench-tested every unit."""
    r = W.rng(32)
    out = []
    sid = 880214
    for v in e["veh"]:
        mine = []
        # bench tests at the vendor's shop, the weekend before installation
        bench_day = v["installed"] - dt.timedelta(days=(v["installed"].weekday() - 5) % 7 or 7)
        for k in range(int(r.integers(2, 4))):
            a = W.utc_of(bench_day, 9 + 2 * k, int(r.integers(0, 50)))
            mine.append(dict(start=a, end=a + dt.timedelta(minutes=float(r.uniform(18, 70))), kind="bench"))
        for s in e["ign"]:
            if s["veh"] != v["veh"]:
                continue
            if not W.installed_at(v, s["start"]):
                continue
            mine.append(dict(start=s["start"], end=s["end"], kind="drive"))
        for m in sorted(mine, key=lambda m: m["start"]):
            if not (W.EXPORT_FROM - dt.timedelta(days=12) <= m["start"] < W.EXPORT_TO):
                continue
            sid += int(r.integers(1, 9))
            mins = (m["end"] - m["start"]).total_seconds() / 60.0
            out.append(dict(unit=v["unit"], sid=sid, start=m["start"].replace(microsecond=0),
                            end=m["end"].replace(microsecond=0), kind=m["kind"],
                            frames=int(mins * float(r.uniform(28, 34)) * (0.4 if m["kind"] == "bench" else 1.0)),
                            mb=round(mins * float(r.uniform(5.2, 6.9)) * (0.3 if m["kind"] == "bench" else 1.0), 1)))
    # a phone that lost power mid-shift leaves its session open, and the platform's session export lists only the
    # sessions it closed; the unit's detections from that day still came in
    drive = [x for x in out if x["kind"] == "drive" and x["start"] >= W.utc_of(dt.date(2027, 3, 1), 0)
             and x["end"] < W.utc_of(dt.date(2027, 4, 1), 0)]
    det_days = {(x["unit"], W.local(x["t"]).date()) for x in e["detections"]}
    group = {v["unit"]: v["group"] for v in e["veh"]}
    days_with = {}
    for x in out:
        if x["kind"] != "drive":
            continue
        d = W.local(x["start"]).date()
        while d <= W.local(x["end"]).date():
            days_with.setdefault((x["unit"], d), []).append(x)
            d += dt.timedelta(1)
    unclosed = []
    for g, n in (("PATROL", 5), ("FSP", 3), ("SWEEPER", 2), ("CREW", 3)):
        cands = []
        for x in sorted(drive, key=lambda x: (x["unit"], x["start"])):
            if group[x["unit"]] != g:
                continue
            d, solo = W.local(x["start"]).date(), []
            while d <= W.local(x["end"]).date():
                if len(days_with[(x["unit"], d)]) == 1:
                    solo.append(d)
                d += dt.timedelta(1)
            if solo and all((x["unit"], d) in det_days and d.month == 3 for d in solo):
                cands.append(x)
        for i in sorted(r.choice(len(cands), n, replace=False)):
            unclosed.append(cands[int(i)])
    for x in unclosed:
        x["unclosed"] = True
    e["sessions"] = out


def service_days(e, start_only=False, utc=False, bench=False, listed_only=False):
    """Billable unit-days by fleet: local calendar days in March on which an installed unit had a session."""
    out = {}
    for v in e["veh"]:
        days = set()
        for s in e["sessions"]:
            if s["unit"] != v["unit"]:
                continue
            if s["kind"] == "bench" and not bench:
                continue
            if s.get("unclosed") and listed_only:
                continue
            a, b = (s["start"], s["end"]) if utc else (W.local(s["start"]), W.local(s["end"]))
            d = a.date()
            last = a.date() if start_only else b.date()
            while d <= last:
                if d.month == 3 and d.year == 2027 and (bench or (d >= v["installed"] and (v["removed"] is None or d < v["removed"]))):
                    days.add(d)
                d += dt.timedelta(1)
        out[v["group"]] = out.get(v["group"], 0) + len(days)
    return out


# ------------------------------------------------------------------------------------------------ work orders
BAND = {1: 40, 2: 66, 3: 112}


def work_orders(e):
    """MMS cold patch work orders raised from the review queue in March. Office orders carry each line's own
    pounds and hours; the crews' mobile app writes the order's total pounds on every line."""
    r = W.rng(33)
    rq = W.rng(38)
    for d in e["defects"]:
        # the crews work from Kerbline's map: a pothole shows there the business day after its first detection
        d["reviewed"] = _business(d["first"] + dt.timedelta(hours=float(rq.uniform(14, 40))), rq)
    conf = [d for d in e["defects"] if d["real"] and not d["off"] and not e["S"][d["seg"]]["turnback"]]
    p_cls = {"FWY": 0.46, "ART": 0.34, "SUB": 0.27, "RUR": 0.24}
    picks = []
    for d in conf:
        s = e["S"][d["seg"]]
        if d["reviewed"] >= W.utc_of(dt.date(2027, 3, 31), 12):
            continue
        if r.random() < p_cls[s["cls"]]:
            picks.append(d)
    # crews: two per section
    jobs = []
    for d in picks:
        s = e["S"][d["seg"]]
        raised = d["reviewed"] + dt.timedelta(minutes=float(r.uniform(6, 95)))
        jobs.append(dict(d=d, sec=s["sec"], route=s["route"], raised=raised, attempt=1))
    # failed cold patches come back: a second order a few days after the first was finished
    out = []
    wo = 27004210

    def finish_after(t, hours):
        x = W.local(t + dt.timedelta(hours=hours))
        while x.weekday() >= 5 or not (7 <= x.hour < 15):
            x = x + dt.timedelta(minutes=37)
            if x.weekday() >= 5:
                x = dt.datetime(x.year, x.month, x.day, 7, 20, tzinfo=W.TZ) + dt.timedelta(days=7 - x.weekday())
        return x.astimezone(W.UTC)
    by_sec_day = {}
    for j in sorted(jobs, key=lambda j: (j["raised"], j["d"]["id"])):
        by_sec_day.setdefault((j["sec"], W.local(j["raised"]).date()), []).append(j)
    orders = []
    for key in sorted(by_sec_day):
        group = list(by_sec_day[key])
        mobile_day = r.random() < 0.6
        while group:
            head = group.pop(0)
            if mobile_day:
                k = int(r.integers(1, 5))
                mates = [g for g in group if g["route"] == head["route"]][:k - 1]
            else:
                mates = group[:1] if group and r.random() < 0.3 else []
            for g in mates:
                group.remove(g)
            orders.append(dict(lines=[head] + mates, mobile=mobile_day, sec=key[0]))
    # finish times, crews and the second attempt
    second = []
    for o in orders:
        raised = max(l["raised"] for l in o["lines"])
        o["raised"] = raised
        o["finish"] = finish_after(raised, float(r.uniform(3.0, 70.0)))
        o["crew"] = "%d-%s" % (o["sec"], "AB"[int(r.integers(2))])
        o["crew_size"] = int(r.choice([2, 3], p=[0.55, 0.45]))
        for l in o["lines"]:
            sev = l["d"]["src"]["severity"]
            l["lb"] = int(5 * round(float(r.uniform(*{1: (18, 40), 2: (32, 66), 3: (58, 112)}[sev])) / 5))
            if r.random() < 0.16 and o["finish"] < W.utc_of(dt.date(2027, 3, 26), 12):
                again = o["finish"] + dt.timedelta(hours=float(r.uniform(60, 260)))
                second.append(dict(d=l["d"], sec=o["sec"], route=l["route"], raised=again, attempt=2))
    for x in sorted(second, key=lambda x: (x["raised"], x["d"]["id"])):
        x["raised"] = _business(x["raised"], r)
        o = dict(lines=[x], mobile=r.random() < 0.5, sec=x["sec"], raised=x["raised"])
        o["finish"] = finish_after(x["raised"], float(r.uniform(3.0, 50.0)))
        o["crew"] = "%d-%s" % (x["sec"], "AB"[int(r.integers(2))])
        o["crew_size"] = int(r.choice([2, 3], p=[0.55, 0.45]))
        sev = x["d"]["src"]["severity"]
        x["lb"] = int(5 * round(float(r.uniform(*{1: (18, 40), 2: (32, 66), 3: (58, 112)}[sev])) / 5))
        orders.append(o)
    # every section has a multi-line mobile order: where none came of the day's queue, the crew took the
    # section's next two first-attempt potholes on one order
    for no in W.ORDER:
        if any(o["sec"] == no and o["mobile"] and len(o["lines"]) >= 2 for o in orders):
            continue
        multi = [o for o in orders if o["sec"] == no and len(o["lines"]) >= 2]
        if multi:
            multi[0]["mobile"] = True
            continue
        singles = sorted([o for o in orders if o["sec"] == no and len(o["lines"]) == 1
                          and o["lines"][0]["attempt"] == 1], key=lambda o: o["raised"])
        while len(singles) < 2:
            # a confirmed pothole of the section with no order yet gets one
            pool = sorted([d for d in conf if e["S"][d["seg"]]["sec"] == no
                           and d["reviewed"] < W.utc_of(dt.date(2027, 3, 26), 12)
                           and not any(l["d"] is d for o_ in orders for l in o_["lines"])],
                          key=lambda d: (d["reviewed"], d["id"]))
            d = pool[0]
            line = dict(d=d, sec=no, route=e["S"][d["seg"]]["route"], attempt=1,
                        raised=d["reviewed"] + dt.timedelta(minutes=float(r.uniform(6, 95))))
            sev = d["src"]["severity"]
            line["lb"] = int(5 * round(float(r.uniform(*{1: (18, 40), 2: (32, 66), 3: (58, 112)}[sev])) / 5))
            o = dict(lines=[line], mobile=True, sec=no, raised=line["raised"])
            o["finish"] = finish_after(line["raised"], float(r.uniform(3.0, 30.0)))
            o["crew"] = "%d-%s" % (no, "AB"[int(r.integers(2))])
            o["crew_size"] = int(r.choice([2, 3], p=[0.55, 0.45]))
            orders.append(o)
            singles = sorted([o for o in orders if o["sec"] == no and len(o["lines"]) == 1
                              and o["lines"][0]["attempt"] == 1], key=lambda o: o["raised"])
        a, b = singles[0], singles[1]
        a["lines"] = a["lines"] + b["lines"]
        a["mobile"] = True
        a["raised"] = max(a["raised"], b["raised"])
        a["finish"] = max(a["finish"], b["finish"])
        orders.remove(b)
    # crews often enter one figure for like potholes on an office order; the mobile app's repeated total is more
    # than any one pothole of its lines' severities takes
    sev_of = lambda l: l["d"]["src"]["severity"]
    for o in orders:
        if len(o["lines"]) < 2:
            continue
        if o["mobile"]:
            top = max(BAND[sev_of(l)] for l in o["lines"])
            while sum(l["lb"] for l in o["lines"]) <= top:
                room = [l for l in o["lines"] if l["lb"] + 5 <= BAND[sev_of(l)]]
                if not room:
                    break
                min(room, key=lambda l: (l["lb"] - BAND[sev_of(l)], l["d"]["id"]))["lb"] += 5
            if sum(l["lb"] for l in o["lines"]) <= top:
                o["mobile"] = False
        if not o["mobile"] and len({sev_of(l) for l in o["lines"]}) == 1 and r.random() < 0.7:
            v = min(l["lb"] for l in o["lines"])
            for l in o["lines"]:
                l["lb"] = v
    # every section has an office order carrying one figure on like potholes
    for no in W.ORDER:
        def like(o):
            return (not o["mobile"] and len(o["lines"]) >= 2 and len({l["lb"] for l in o["lines"]}) == 1
                    and o["finish"] < W.utc_of(dt.date(2027, 3, 31), 12))
        if any(o["sec"] == no and like(o) for o in orders):
            continue
        multi = [o for o in orders if o["sec"] == no and not o["mobile"] and len(o["lines"]) >= 2
                 and len({sev_of(l) for l in o["lines"]}) == 1 and o["finish"] < W.utc_of(dt.date(2027, 3, 31), 12)]
        if multi:
            v = min(l["lb"] for l in multi[0]["lines"])
            for l in multi[0]["lines"]:
                l["lb"] = v
            continue
        singles = sorted([o for o in orders if o["sec"] == no and len(o["lines"]) == 1
                          and o["lines"][0]["attempt"] == 1 and o["finish"] < W.utc_of(dt.date(2027, 3, 29), 12)
                          and not any(x["d"] is o["lines"][0]["d"] for x in second)],
                         key=lambda o: (o["raised"], o["lines"][0]["d"]["id"]))
        pair = None
        for i, a in enumerate(singles):
            for b in singles[i + 1:]:
                if (sev_of(a["lines"][0]) == sev_of(b["lines"][0])
                        and (b["raised"] - a["raised"]) < dt.timedelta(days=6)):
                    pair = (a, b)
                    break
            if pair:
                break
        if not pair:
            # two like potholes of the section with no order yet go on one office order
            pool = sorted([d for d in conf if e["S"][d["seg"]]["sec"] == no
                           and d["reviewed"] < W.utc_of(dt.date(2027, 3, 24), 12)
                           and not any(l["d"] is d for o_ in orders for l in o_["lines"])],
                          key=lambda d: (d["reviewed"], d["id"]))
            for i, d1 in enumerate(pool):
                d2 = next((d for d in pool[i + 1:] if d["src"]["severity"] == d1["src"]["severity"]), None)
                if d2 is None:
                    continue
                made = []
                for d in (d1, d2):
                    line = dict(d=d, sec=no, route=e["S"][d["seg"]]["route"], attempt=1,
                                raised=d["reviewed"] + dt.timedelta(minutes=float(r.uniform(6, 95))))
                    line["lb"] = int(5 * round(float(r.uniform(*{1: (18, 40), 2: (32, 66), 3: (58, 112)}[sev_of(line)])) / 5))
                    o = dict(lines=[line], mobile=False, sec=no, raised=line["raised"])
                    o["finish"] = finish_after(line["raised"], float(r.uniform(3.0, 30.0)))
                    o["crew"] = "%d-%s" % (no, "AB"[int(r.integers(2))])
                    o["crew_size"] = int(r.choice([2, 3], p=[0.55, 0.45]))
                    orders.append(o)
                    made.append(o)
                pair = tuple(made)
                break
        a, b = pair
        a["lines"] = a["lines"] + b["lines"]
        a["raised"] = max(a["raised"], b["raised"])
        a["finish"] = max(a["finish"], b["finish"])
        a["mobile"] = False
        v = min(l["lb"] for l in a["lines"])
        for l in a["lines"]:
            l["lb"] = v
        orders.remove(b)
    orders.sort(key=lambda o: (o["raised"], o["lines"][0]["d"]["id"]))
    rows = []
    for o in orders:
        wo += int(r.integers(1, 23))
        o["wo"] = wo
        total = sum(l["lb"] for l in o["lines"])
        still_open = o["finish"] >= W.utc_of(dt.date(2027, 4, 1), 0)
        for n, l in enumerate(o["lines"], 1):
            d = l["d"]
            dets = [x for x in e["det_by"][d["id"]] if x["t"] <= o["raised"]] or e["det_by"][d["id"]]
            ref = min(dets, key=lambda x: x["t"])["det"]
            rows.append(dict(wo=wo, line=n, sec=o["sec"], route=l["route"], mp=d["mp"], ref=ref, raised=o["raised"],
                             finish=None if still_open else o["finish"], crew=o["crew"], crew_size=o["crew_size"],
                             lb=None if still_open else (total if o["mobile"] else l["lb"]),
                             status="OPEN" if still_open else "COMPLETE", defect=d, mobile=o["mobile"],
                             true_lb=l["lb"], attempt=l["attempt"]))
    e["orders"] = orders
    e["wo_rows"] = rows


# ------------------------------------------------------------------------------------------------ telematics
def loops(e):
    """Patrol and service-patrol trucks working an interchange come round its loop and drive a short segment a second
    time, the same way, a minute or three after leaving it."""
    r = W.rng(37)
    S = e["S"]
    by_veh = {}
    for t in e["trav"]:
        by_veh.setdefault(t["veh"], []).append(t["enter"])
    for v in by_veh:
        by_veh[v].sort()
    added = []
    for no in W.ORDER:
        cands = []
        for t in e["trav"]:
            s = S[t["seg"]]
            dur = (t["exit"] - t["enter"]).total_seconds()
            if (s["sec"] != no or s["turnback"] or s["length"] > 1.3 or dur > 150
                    or not W.installed_at(e["veh_by"][t["veh"]], t["enter"])
                    or W.local(t["enter"]).month != 3 or W.local(t["enter"]).day in (1, 31)
                    or W.REPLAY_FROM - dt.timedelta(hours=2) <= t["enter"] < W.REPLAY_TO + dt.timedelta(hours=2)):
                continue
            nxt = [x for x in by_veh[t["veh"]] if t["enter"] < x <= t["exit"] + dt.timedelta(minutes=8)]
            if nxt:
                continue
            cands.append(t)
        cands.sort(key=lambda t: (t["enter"], t["veh"], t["seg"]))
        picks = [cands[int(i)] for i in r.permutation(len(cands))]
        miles, n = 0.0, 0
        for t in picks:
            if miles >= 1.6 and n >= 3:
                break
            dur = (t["exit"] - t["enter"]).total_seconds()
            gap = float(r.uniform(60, max(61.0, 270 - dur)))
            a = t["exit"] + dt.timedelta(seconds=round(gap, 1))
            b = a + dt.timedelta(seconds=round(dur * float(r.uniform(0.9, 1.12)), 1))
            if (a - t["enter"]).total_seconds() >= 290:
                continue
            added.append(dict(veh=t["veh"], seg=t["seg"], enter=a, exit=b, dir=t["dir"], fwd=t.get("fwd"), loop=True))
            by_veh[t["veh"]].append(a)
            by_veh[t["veh"]].sort()
            miles += S[t["seg"]]["length"]
            n += 1
        assert miles >= 1.0 and n >= 2, (no, miles, n)
    e["trav"] = sorted(e["trav"] + added, key=lambda t: (t["enter"], t["veh"], t["seg"]))
    e["loops"] = added


def replay(e):
    """The telematics provider re-ran its map matching over 12 March 00:00 to 13 March 06:00 UTC after a fix and
    appended the re-run's traversals beside the originals; the re-run wrote the district's clock time where the export
    carries UTC, so each re-run traversal sits five hours before the pass it repeats."""
    out = []
    for t in e["trav"]:
        if W.REPLAY_FROM <= t["enter"] < W.REPLAY_TO:
            out.append(dict(veh=t["veh"], seg=t["seg"], enter=t["enter"] - dt.timedelta(hours=5),
                            exit=t["exit"] - dt.timedelta(hours=5), dir=t["dir"], replay=True))
    e["replays"] = out


# ------------------------------------------------------------------------------------------------ asset inventory
def covers(e):
    """The district's utility cover inventory: every cover in the state roadway, located by its 2026 rover survey."""
    r = W.rng(39)
    owners = [("Tamsett Water Authority", "Water valve"), ("Tamsett Water Authority", "Manhole"),
              ("Tamsett County Sewer District", "Manhole"), ("Keystone Gas", "Gas valve"),
              ("Northline Telecom", "Handhole"), ("State DOT", "Drainage inlet")]
    out = []
    aid = 61000412
    for d in sorted([d for d in e["others"] if d["cls"] == "utility_cover"], key=lambda d: (d["seg"], d["mp"])):
        s = e["S"][d["seg"]]
        aid += int(r.integers(3, 29))
        own, typ = owners[int(r.integers(len(owners)))]
        lat, lon = W.latlon(s, d["mp"])
        out.append(dict(asset="UC-%d" % aid, route=s["route"], mp=d["mp"], lat=lat, lon=lon, seg=s["seg"], owner=own,
                        type=typ, surveyed=dt.date(2026, 5, 4) + dt.timedelta(int(r.integers(0, 150)))))
    e["covers"] = out


# ------------------------------------------------------------------------------------------------ distractors
def distractors(e):
    r = W.rng(35)
    pci = []
    for s in e["segs"]:
        iri = float(r.uniform(68, 190)) if s["cls"] != "FWY" else float(r.uniform(55, 120))
        crack = float(r.uniform(0.5, 18.0))
        pci.append(dict(seg=s["seg"], route=s["route"], bmp=s["bmp"], emp=s["emp"],
                        date=dt.date(2026, 6, 1) + dt.timedelta(int(r.integers(0, 92))),
                        iri=int(round(iri)), rut=round(float(r.uniform(0.05, 0.42)), 2), crack=round(crack, 1),
                        pci=int(max(31, min(98, round(100 - 0.18 * iri - 1.4 * crack + float(r.normal(18, 6))))))))
    e["pci"] = pci
    winter = []
    for no in W.ORDER:
        for ev, (a, b) in enumerate([(dt.date(2027, 3, 5), dt.date(2027, 3, 6)), (dt.date(2027, 3, 26), dt.date(2027, 3, 27))]):
            hrs = float(r.uniform(18, 46)) * (1.3 if W.SEC[no]["kind"] == "U" else 1.0)
            winter.append(dict(sec=no, event="2027-W%02d" % (7 + ev), start=a, end=b, plow_hrs=round(hrs, 1),
                               salt_t=round(hrs * float(r.uniform(2.1, 3.4)), 1),
                               brine_gal=int(round(hrs * float(r.uniform(140, 260)), -1)),
                               ft_cycles=int(r.integers(3, 9))))
    e["winter"] = winter
