"""Everything the call and the asks compute, read from the cut pack: the golden, the default path and the other rungs,
the licensed variants of the linkage, and the asks with their natural wrong handlings. checks.py, golden.py and
ceiling.py read the pack through this module; verify.py has its own code."""
import csv
import datetime as dt
import json
import os
import re
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np

TZ = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
LINE = 6.0
DAY_RATE = 10.85
FLEETS = ["Section patrol", "Freeway service patrol", "Street sweeper", "District crew"]


def _csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def _local(s, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.datetime.strptime(s, fmt).replace(tzinfo=TZ)


def turnback_segments(target):
    import pdfplumber
    out = []
    with pdfplumber.open(os.path.join(target, "route_turnback_notice_2027-03.pdf")) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    for m in re.finditer(r"^SR \d+ (\d{7}) \d+\.\d{3} \d+\.\d{3}", text, re.M):
        out.append(int(m.group(1)))
    return out, text


def load(target):
    """The pack, parsed once."""
    from openpyxl import load_workbook
    p = {}
    p["inv"] = {int(r["segment_id"]): dict(sec=int(r["section"]), route=r["route"], bmp=float(r["begin_mp"]),
                                           emp=float(r["end_mp"]), length=float(r["length_mi"]),
                                           lanes=int(r["through_lanes"]), fc=r["functional_class"])
                for r in _csv(target, "road_inventory_2026.csv")}
    p["xw"] = _csv(target, "road_inventory_crosswalk_2025_2026.csv")
    p["turnback"], p["turnback_text"] = turnback_segments(target)
    p["det"] = _csv(target, "kerbline_detections_2027-03.csv")
    p["trav"] = _csv(target, "fleet_camera_traversals_2027-03.csv")
    p["wo"] = _csv(target, "mms_cold_patch_orders_2027-03.csv")
    p["covers"] = _csv(target, "utility_cover_inventory_2026.csv")
    wb = load_workbook(os.path.join(target, "kerbline_unit_register.xlsx"), read_only=True)
    rows = list(wb["Units"].iter_rows(values_only=True))
    p["reg"] = [dict(zip(rows[0], r)) for r in rows[1:]]
    p["sess"] = json.load(open(os.path.join(target, "kerbline_unit_sessions_2027-03.json")))
    return p


# ---------------------------------------------------------------------------------------------- shared pieces
def roadway(p, keep_turnback=False):
    """The program's roadway: the inventory's state segments in each section as at 31 March 2027."""
    tb = set() if keep_turnback else set(p["turnback"])
    return {s: v for s, v in p["inv"].items() if s not in tb}


def lane_miles(p, road):
    out = defaultdict(float)
    for s, v in road.items():
        out[v["sec"]] += v["length"] * v["lanes"]
    return dict(out)


def ref_to_2026(p, drop_unlisted=False, first_child=False):
    """road_ref (2025) and road_mp to the 2026 segment."""
    xw = defaultdict(list)
    for r in p["xw"]:
        xw[int(r["segment_id_2025"])].append((int(r["segment_id_2026"]), float(r["begin_mp_2026"]), float(r["end_mp_2026"])))

    def f(ref, mp):
        if ref == "":
            return None
        ref = int(ref)
        if ref in xw:
            if drop_unlisted:
                return None
            if first_child:
                return xw[ref][0][0]
            for seg, lo, hi in xw[ref]:
                if lo <= mp <= hi:
                    return seg
            return xw[ref][0][0]
        return ref if ref in p["inv"] else None
    return f


def units(p):
    """unit -> (vehicle, fleet group, installed date, removed date or None)."""
    out = {}
    for r in p["reg"]:
        inst = r["Installed"].date() if hasattr(r["Installed"], "date") else r["Installed"]
        rem = r["Removed"].date() if hasattr(r["Removed"], "date") and r["Removed"] is not None else r["Removed"]
        out[r["Unit serial"]] = (r["Vehicle"], r["Fleet group"], inst, rem)
    return out


def route_segment(p, keep_turnback=False):
    """(route, milepost) -> the 2026 segment holding it."""
    by_route = defaultdict(list)
    for seg, v in p["inv"].items():
        by_route[v["route"]].append((v["bmp"], v["emp"], seg))
    for k in by_route:
        by_route[k].sort()

    def f(route, mp):
        for lo, hi, seg in by_route.get(route, ()):
            if lo - 1e-9 <= mp <= hi + 1e-9:
                return seg
        return None
    return f


def sigma(p, by="unit", robust=False):
    """Each unit's milepost error: its utility cover detections against the inventory's surveyed covers on the same
    route (the nearest within a tenth of a mile). by='fleet' pools a fleet group's units."""
    u = units(p)
    cov = defaultdict(list)
    for c in p["covers"]:
        cov[c["route"]].append(float(c["milepost"]))
    res = defaultdict(list)
    for d in p["det"]:
        if d["defect_class"] != "utility_cover" or not d["road_mp"]:
            continue
        mp = float(d["road_mp"])
        near = min(cov.get(d["route"], [1e9]), key=lambda c: abs(c - mp))
        if abs(near - mp) > 0.1:
            continue
        key = d["unit_serial"] if by == "unit" else u[d["unit_serial"]][1]
        res[key].append(mp - near)
    out = {}
    for k, v in res.items():
        v = np.array(v)
        out[k] = float(1.4826 * np.median(np.abs(v - np.median(v)))) if robust else float(np.sqrt(np.mean(v ** 2)))
    if by == "fleet":
        return {unit: out[g] for unit, (veh, g, a, b) in u.items()}
    return out


def pothole_detections(p, utc=False):
    """Kerbline's pothole-class detections on the state routes in March (district local time)."""
    out = []
    for d in p["det"]:
        if d["defect_class"] != "pothole" or not d["road_mp"]:
            continue
        t = _local(d["captured_local"])
        if utc:
            t = t.replace(tzinfo=UTC)
        if (t.year, t.month) != (2027, 3):
            continue
        out.append(d)
    return out


def link(p, tol, road, dets=None, place="route", mapper=None):
    """Potholes per section: the detections on each route sorted by milepost, a detection joining the run before it
    when the gap is within tol(a, b); a run is one pothole, placed on the 2026 segment holding its median milepost."""
    dets = pothole_detections(p) if dets is None else dets
    seg_of = route_segment(p)
    mapper = mapper or ref_to_2026(p)
    by_route = defaultdict(list)
    for d in dets:
        by_route[d["route"]].append(d)
    out = defaultdict(int)
    for rt, xs in by_route.items():
        xs = sorted(xs, key=lambda d: (float(d["road_mp"]), d["detection_id"]))
        runs = [[xs[0]]]
        for a, b in zip(xs, xs[1:]):
            if float(b["road_mp"]) - float(a["road_mp"]) > tol(a, b):
                runs.append([b])
            else:
                runs[-1].append(b)
        for run in runs:
            mps = sorted(float(d["road_mp"]) for d in run)
            mid = mps[(len(mps) - 1) // 2]
            if place == "route":
                seg = seg_of(rt, mid)
            else:
                d0 = min(run, key=lambda d: abs(float(d["road_mp"]) - mid))
                seg = mapper(d0["road_ref"], float(d0["road_mp"]))
            if seg in road:
                out[road[seg]["sec"]] += 1
    return dict(out)


def rates(p, counts, road):
    lm = lane_miles(p, road)
    return {sec: counts.get(sec, 0) / (lm[sec] / 10.0) for sec in lm}


def designated(r):
    return sorted(s for s, v in r.items() if v >= LINE)


def unit_tol(sig, k=3.0):
    return lambda a, b: k * float(np.hypot(sig[a["unit_serial"]], sig[b["unit_serial"]]))


def golden(p):
    road = roadway(p)
    sig = sigma(p)
    cnt = link(p, unit_tol(sig), road)
    est = rates(p, cnt, road)
    return dict(road=road, sig=sig, counts=cnt, est=est, set=designated(est))


def family(p, g=None):
    """Every licensed member: the tolerance at 2.5 to 4 times the pair's combined error, each unit's error or its fleet's,
    by root mean square or by median absolute deviation."""
    g = g or golden(p)
    out = {}
    for by in ("unit", "fleet"):
        for robust in (False, True):
            sig = sigma(p, by=by, robust=robust)
            for k in (2.5, 3.0, 3.5, 4.0):
                out["%s_%s_k%.1f" % (by, "mad" if robust else "rms", k)] = rates(p, link(p, unit_tol(sig, k), g["road"]),
                                                                              g["road"])
    return out


SINGLE = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.010, 0.013, 0.016, 0.020, 0.025, 0.030, 0.040, 0.050,
          0.060, 0.080, 0.100]


def single(p, t, road=None):
    """One tolerance for every unit (the default path at any t)."""
    road = road or roadway(p)
    return rates(p, link(p, lambda a, b: t, road), road)


def per_detection(p, road=None):
    """Every pothole detection a pothole (the rung below)."""
    road = road or roadway(p)
    return rates(p, link(p, lambda a, b: -1.0, road), road)


def mishandled(p):
    """The golden method with each Layer 1 item read the natural wrong way."""
    out = {}
    road = roadway(p)
    sig = sigma(p)
    tol = unit_tol(sig)
    out["utc_window"] = rates(p, link(p, tol, road, dets=pothole_detections(p, utc=True)), road)
    out["placed_by_road_ref"] = rates(p, link(p, tol, road, place="ref"), road)
    out["crosswalk_unused"] = rates(p, link(p, tol, road, place="ref", mapper=ref_to_2026(p, drop_unlisted=True)), road)
    out["crosswalk_first_child"] = rates(p, link(p, tol, road, place="ref", mapper=ref_to_2026(p, first_child=True)), road)
    road_tb = roadway(p, keep_turnback=True)
    out["turnback_kept"] = rates(p, link(p, tol, road_tb), road_tb)
    return out


# ---------------------------------------------------------------------------------------------- the asks
def _mms_time(s):
    return dt.datetime.strptime(s, "%m/%d/%Y %H:%M").replace(tzinfo=TZ) if s else None


def ask_pounds(p, pounds="severity"):
    """Ask A: per section, the pounds of cold mix its March cold patches used (COMPLETE orders finished in March).
    pounds: 'severity' takes a figure repeated on every line of an order once where it is more than any single-line
    order used on a pothole of any of its lines' severities, 'per_order' wherever it repeats; 'lines' sums."""
    done = [r for r in p["wo"] if r["status"] == "COMPLETE" and r["finished"] and _mms_time(r["finished"]).month == 3]
    sev = {d["detection_id"]: int(d["severity"]) for d in p["det"] if d["severity"]}
    orders = defaultdict(list)
    for r in done:
        orders[r["wo_number"]].append(r)
    top = defaultdict(int)
    for wo, lines in orders.items():
        if len(lines) == 1:
            s_ = sev[lines[0]["ext_ref"]]
            top[s_] = max(top[s_], int(lines[0]["cold_mix_lb"]))
    TOTALS.clear()
    lb = defaultdict(int)
    for wo, lines in orders.items():
        sec = int(lines[0]["section"])
        vals = [int(l["cold_mix_lb"]) for l in lines]
        repeated = len(lines) > 1 and len(set(vals)) == 1
        if pounds == "severity" and repeated and vals[0] > max(top[sev[l["ext_ref"]]] for l in lines):
            TOTALS.add(wo)
            lb[sec] += vals[0]
        elif pounds == "per_order" and repeated:
            lb[sec] += vals[0]
        else:
            lb[sec] += sum(vals)
    return dict(lb)


TOTALS = set()


def total_orders(p):
    """The orders whose repeated figure ask A's golden takes once."""
    ask_pounds(p)
    return set(TOTALS)


def ask_miles(p, dedupe=True, installed=True, local_window=True, program_road=True, window_s=None, overlap=False):
    """Ask B: per section, the miles the pilot's camera units were driven on the program's roadway in March, each
    pass at the segment's inventory length. dedupe drops a traversal that repeats the same vehicle's traversal of the
    segment, the same way, exactly five hours later (the re-run's clock); window_s instead drops a vehicle's repeat of
    a segment within that many seconds."""
    road = roadway(p) if program_road else p["inv"]
    u = units(p)
    inst = {}
    for unit, (veh, grp, a, b) in u.items():
        inst.setdefault(veh, []).append((a, b))
    rows = sorted(p["trav"], key=lambda t: (t["vehicle_id"], t["segment_id"], t["enter_utc"], int(t["traversal_id"])))
    if dedupe and window_s is None:
        sig = {(t["vehicle_id"], t["segment_id"], t["direction"], _utc(t["enter_utc"]), _utc(t["exit_utc"])) for t in rows}
        five = dt.timedelta(hours=5)
        rows = [t for t in rows if (t["vehicle_id"], t["segment_id"], t["direction"], _utc(t["enter_utc"]) + five,
                                    _utc(t["exit_utc"]) + five) not in sig]
    keep = []
    last = {}
    for t in rows:
        key = (t["vehicle_id"], t["segment_id"])
        a, b = _utc(t["enter_utc"]), _utc(t["exit_utc"])
        if window_s is not None and key in last and (a - last[key][0]).total_seconds() <= window_s \
                and t["direction"] == last[key][2]:
            continue
        if overlap and key in last and a <= last[key][1]:
            continue
        last[key] = (a, b, t["direction"])
        keep.append(t)
    out = defaultdict(float)
    for t in keep:
        seg = int(t["segment_id"])
        if seg not in road:
            continue
        a = _utc(t["enter_utc"])
        day = a.astimezone(TZ).date() if local_window else a.date()
        if not (day.year == 2027 and day.month == 3):
            continue
        if installed and not any(day >= x and (y is None or day < y) for x, y in inst.get(t["vehicle_id"], [])):
            continue
        if not installed and t["vehicle_id"] not in inst:
            continue
        out[road[seg]["sec"]] += road[seg]["length"]
    return dict(out)
