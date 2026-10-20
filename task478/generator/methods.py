"""Everything the call and the asks compute, read from the cut pack: the golden, the default path and the other rungs,
the licensed variants of the completion, and the asks with their natural wrong handlings. checks.py, golden.py and
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
    wb = load_workbook(os.path.join(target, "kerbline_qa_review_2027-03.xlsx"), read_only=True)
    rows = list(wb["Review decisions"].iter_rows(values_only=True))
    p["qa"] = [dict(zip(rows[0], r)) for r in rows[1:]]
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


def looks(p, road, use_utc_day=False, ignore_install=False, sessions_only=False):
    """segment -> set of units that drove it in March while installed on the vehicle."""
    u = units(p)
    by_veh = defaultdict(list)
    for unit, (veh, grp, inst, rem) in u.items():
        by_veh[veh].append((unit, inst, rem))
    open_iv = None
    if sessions_only:
        open_iv = defaultdict(list)
        for x in p["sess"]["units"]:
            for s in x["sessions"]:
                open_iv[x["unit_serial"]].append((_utc(s["start_utc"]), _utc(s["end_utc"])))
    out = defaultdict(set)
    for t in p["trav"]:
        seg = int(t["segment_id"])
        if seg not in road:
            continue
        a = _utc(t["enter_utc"])
        day = a.date() if use_utc_day else a.astimezone(TZ).date()
        if not (day.year == 2027 and day.month == 3):
            continue
        for unit, inst, rem in by_veh.get(t["vehicle_id"], []):
            if not ignore_install and (day < inst or (rem is not None and day >= rem)):
                continue
            if sessions_only and not any(lo <= a <= hi for lo, hi in open_iv[unit]):
                continue
            out[seg].add(unit)
    return out


def potholes(p, road, mapper=None, merge_dups=True):
    """Confirmed potholes on the roadway: defect -> (segment, set of units that detected it)."""
    mapper = mapper or ref_to_2026(p)
    confirmed, dup_of = set(), {}
    for r in p["qa"]:
        if r["Decision"] == "Confirmed":
            confirmed.add(int(r["Defect ID"]))
        elif r["Reason"] and str(r["Reason"]).startswith("Duplicate of "):
            dup_of[int(r["Defect ID"])] = int(str(r["Reason"]).split()[-1])
    segs = defaultdict(list)
    det_units = defaultdict(set)
    for d in p["det"]:
        did = int(d["defect_id"])
        if merge_dups and did in dup_of:
            did = dup_of[did]
        if did not in confirmed:
            continue
        seg = mapper(d["road_ref"], float(d["road_mp"]) if d["road_mp"] else None)
        if seg is None:
            continue
        segs[did].append(seg)
        det_units[did].add(d["unit_serial"])
    out = {}
    for did, ss in segs.items():
        seg = max(set(ss), key=lambda s: (ss.count(s), -s))
        if seg in road:
            out[did] = (seg, det_units[did])
    return out


# ---------------------------------------------------------------------------------------------- the completion
def q_pairs(pots, lk):
    a = b = 0
    for did, (seg, us) in pots.items():
        C = len(lk.get(seg, ()))
        k = len(us & lk.get(seg, set()))
        if C >= 2 and k >= 1:
            a += k * (k - 1)
            b += k * (C - 1)
    return a / b


def q_mle(pots, lk):
    data = [(len(us & lk[seg]), len(lk[seg])) for did, (seg, us) in pots.items()
            if len(lk.get(seg, ())) >= 2 and len(us & lk[seg]) >= 1]
    k = np.array([x[0] for x in data], float)
    c = np.array([x[1] for x in data], float)
    lo, hi = 0.2, 0.9
    for _ in range(80):     # the score is decreasing in q: bisect it
        q = (lo + hi) / 2
        score = np.sum(k / q - (c - k) / (1 - q) - c * (1 - q) ** (c - 1) / (1 - (1 - q) ** c))
        lo, hi = (q, hi) if score > 0 else (lo, q)
    return (lo + hi) / 2


def completed(pots, lk, road, rate, by="segment"):
    """Each section's potholes per ten lane-miles: every confirmed pothole counted as one over the chance that at
    least one of the distinct units that drove its segment found it. rate: a number, or a function of (pothole
    segment, unit) for the per-kind and per-fleet members."""
    lm = lane_miles(None, road)
    tot = defaultdict(float)
    for did, (seg, us) in pots.items():
        drove = lk.get(seg, set())
        if callable(rate):
            miss = float(np.prod([1 - rate(seg, u) for u in drove]))
        else:
            miss = (1 - rate) ** len(drove)
        tot[road[seg]["sec"]] += 1.0 / (1.0 - miss)
    return {sec: tot.get(sec, 0.0) / (lm[sec] / 10.0) for sec in lm}


def found(pots, road):
    lm = lane_miles(None, road)
    n = defaultdict(int)
    for did, (seg, us) in pots.items():
        n[road[seg]["sec"]] += 1
    return {sec: n.get(sec, 0) / (lm[sec] / 10.0) for sec in lm}


def designated(rates):
    return sorted(s for s, v in rates.items() if v >= LINE)


def golden(p):
    road = roadway(p)
    lk = looks(p, road)
    pots = potholes(p, road)
    q = q_pairs(pots, lk)
    est = completed(pots, lk, road, q)
    return dict(road=road, looks=lk, pots=pots, q=q, est=est, set=designated(est), found=found(pots, road),
                lm=lane_miles(p, road))


def family(p, g=None):
    """The completion under each licensed member: one rate by pairs or by maximum likelihood, the pass-level
    refinement, one rate per kind of section, one per fleet."""
    g = g or golden(p)
    road, lk, pots = g["road"], g["looks"], g["pots"]
    out = {"pairs": g["est"], "mle": completed(pots, lk, road, q_mle(pots, lk))}
    kind = {sec: ("U" if any(road[s]["fc"] == "Other Freeway/Expressway" for s in road if road[s]["sec"] == sec)
                  else None) for sec in g["lm"]}
    # the kind of section from the inventory: metro sections carry freeway, rural ones only collectors
    fcs = defaultdict(set)
    for s, v in road.items():
        fcs[v["sec"]].add(v["fc"])
    for sec in kind:
        kind[sec] = "U" if "Other Freeway/Expressway" in fcs[sec] else ("R" if fcs[sec] == {"Major Collector"} else "S")
    rates = {}
    for k in ("U", "S", "R"):
        sub = {d: v for d, v in pots.items() if kind[road[v[0]]["sec"]] == k}
        rates[k] = q_pairs(sub, lk)
    out["kind"] = completed(pots, lk, road, lambda seg, u: rates[kind[road[seg]["sec"]]])
    grp = {u: v[1] for u, v in units(p).items()}
    fr = {}
    for f in FLEETS:
        a = b = 0
        for did, (seg, us) in pots.items():
            drove = lk.get(seg, set())
            for u in drove:
                if grp[u] != f:
                    continue
                if (us & drove) - {u}:
                    b += 1
                    a += 1 if u in us else 0
        fr[f] = a / b
    out["fleet"] = completed(pots, lk, road, lambda seg, u: fr[grp[u]])
    out["_rates"] = dict(pairs=g["q"], mle=q_mle(pots, lk), kind=rates, fleet=fr)
    return out


# ---------------------------------------------------------------------------------------------- the rungs
def per_pass(p, g=None):
    """The default path: every pass an independent chance at the rate a pass finds a pothole already found."""
    g = g or golden(p)
    road, pots = g["road"], g["pots"]
    u = units(p)
    by_veh = defaultdict(list)
    for unit, (veh, grp, inst, rem) in u.items():
        by_veh[veh].append((unit, inst, rem))
    passes = defaultdict(list)     # seg -> [(unit, local date)]
    for t in p["trav"]:
        seg = int(t["segment_id"])
        if seg not in road:
            continue
        day = _utc(t["enter_utc"]).astimezone(TZ).date()
        if day.month != 3:
            continue
        for unit, inst, rem in by_veh.get(t["vehicle_id"], []):
            if day >= inst and (rem is None or day < rem):
                passes[seg].append((unit, day))
    first = {}
    det_days = defaultdict(set)
    for d in p["det"]:
        did = int(d["defect_id"])
        if did in pots:
            day = d["captured_local"][:10]
            det_days[did].add((d["unit_serial"], day))
            first[did] = min(first.get(did, "9999"), day)
    a = b = 0
    for did, (seg, us) in pots.items():
        days = {(un, dd.isoformat()) for un, dd in passes[seg] if dd.isoformat() > first[did]}
        b += len(days)
        a += len(days & det_days[did])
    rate = a / b
    lm = lane_miles(p, road)
    tot = defaultdict(float)
    for did, (seg, us) in pots.items():
        n = len({(un, dd) for un, dd in passes[seg]})
        tot[road[seg]["sec"]] += 1.0 / (1.0 - (1.0 - rate) ** n)
    return {sec: tot.get(sec, 0.0) / (lm[sec] / 10.0) for sec in lm}, rate


def halves(p, g=None):
    """Two-sample recapture, the first half of March against the second, per section."""
    g = g or golden(p)
    road, pots = g["road"], g["pots"]
    when = defaultdict(set)
    for d in p["det"]:
        did = int(d["defect_id"])
        if did in pots:
            when[did].add(1 if d["captured_local"][:10] <= "2027-03-15" else 2)
    lm = lane_miles(p, road)
    out = {}
    for sec in lm:
        ds = [did for did, (seg, us) in pots.items() if road[seg]["sec"] == sec]
        n1 = sum(1 for d in ds if 1 in when[d])
        n2 = sum(1 for d in ds if 2 in when[d])
        m = sum(1 for d in ds if when[d] == {1, 2})
        out[sec] = (n1 * n2 / m if m else len(ds)) / (lm[sec] / 10.0)
    return out


def overlap_only(p, g=None):
    """Two units' recapture where two or more drove a segment; the segments one unit drove taken as found."""
    g = g or golden(p)
    road, lk, pots = g["road"], g["looks"], g["pots"]
    lm = lane_miles(p, road)
    tot = defaultdict(float)
    for did, (seg, us) in pots.items():
        C = len(lk.get(seg, ()))
        tot[road[seg]["sec"]] += 1.0 if C < 2 else 1.0 / (1.0 - (1.0 - g["q"]) ** C)
    return {sec: tot.get(sec, 0.0) / (lm[sec] / 10.0) for sec in lm}


# ---------------------------------------------------------------------------------------------- Layer 1, mishandled
def mishandled(p):
    """The golden method with each Layer 1 item read the natural wrong way."""
    out = {}
    road = roadway(p)
    lk = looks(p, road)
    pots = potholes(p, road)

    def run(road_=road, lk_=lk, pots_=pots):
        return completed(pots_, lk_, road_, q_pairs(pots_, lk_))
    out["utc_window"] = run(lk_=looks(p, road, use_utc_day=True))
    out["install_dates_ignored"] = run(lk_=looks(p, road, ignore_install=True))
    out["crosswalk_unused"] = run(pots_=potholes(p, road, mapper=ref_to_2026(p, drop_unlisted=True)))
    out["crosswalk_no_milepost"] = run(pots_=potholes(p, road, mapper=ref_to_2026(p, first_child=True)))
    road_tb = roadway(p, keep_turnback=True)
    out["turnback_kept"] = completed(potholes(p, road_tb), looks(p, road_tb), road_tb,
                                     q_pairs(potholes(p, road_tb), looks(p, road_tb)))
    out["duplicates_unmerged"] = run(pots_=potholes(p, road, merge_dups=False))
    out["sessions_gate_passes"] = run(lk_=looks(p, road, sessions_only=True))
    return out


# ---------------------------------------------------------------------------------------------- the asks
def _mms_time(s):
    return dt.datetime.strptime(s, "%m/%d/%Y %H:%M").replace(tzinfo=TZ) if s else None


def ask_patches(p, legacy="location", pounds="per_order"):
    """Ask A: per section, the potholes cold patched in March (a pothole patched twice counts once) and the pounds of
    cold mix their orders used. legacy: 'location' maps an ext_ref Kerbline no longer carries to the defect at the
    same route and milepost; 'as_is' counts refs as written. pounds: 'per_order' takes a figure repeated on every
    line of an order once; 'lines' sums the lines."""
    qa_loc = {}
    known = set()
    for r in p["qa"]:
        known.add(int(r["Defect ID"]))
        if r["Decision"] == "Confirmed" and r["Milepost"] is not None:
            qa_loc[(r["Route"], round(float(r["Milepost"]), 3))] = int(r["Defect ID"])
    done = [r for r in p["wo"] if r["status"] == "COMPLETE" and r["finished"]
            and _mms_time(r["finished"]).month == 3]
    pots = defaultdict(set)
    for r in done:
        ref = int(r["ext_ref"])
        if legacy == "location" and ref not in known:
            ref = qa_loc[(r["route"], round(float(r["milepost"]), 3))]
        pots[int(r["section"])].add(ref)
    orders = defaultdict(list)
    for r in done:
        orders[r["wo_number"]].append(r)
    lb = defaultdict(int)
    for wo, lines in orders.items():
        sec = int(lines[0]["section"])
        vals = [int(l["cold_mix_lb"]) for l in lines]
        if pounds == "per_order" and len(lines) > 1 and len(set(vals)) == 1:
            lb[sec] += vals[0]
        else:
            lb[sec] += sum(vals)
    return {sec: len(v) for sec, v in pots.items()}, dict(lb)


def ask_miles(p, dedupe=True, installed=True, local_window=True, program_road=True):
    """Ask B: per section, the miles the pilot's camera units were driven on the program's roadway in March, each
    pass at the segment's inventory length. dedupe drops a vehicle's traversal of a segment that overlaps an
    earlier-numbered traversal of the same segment."""
    road = roadway(p) if program_road else p["inv"]
    u = units(p)
    inst = {}
    for unit, (veh, grp, a, b) in u.items():
        inst.setdefault(veh, []).append((a, b))
    rows = sorted(p["trav"], key=lambda t: (t["vehicle_id"], t["segment_id"], t["enter_utc"], int(t["traversal_id"])))
    keep = []
    last = {}
    for t in rows:
        key = (t["vehicle_id"], t["segment_id"])
        a, b = _utc(t["enter_utc"]), _utc(t["exit_utc"])
        if dedupe and key in last and a <= last[key][1]:
            continue
        last[key] = (a, b)
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


def ask_service_days(p, detections=True, any_part=True, local_days=True, bench=False):
    """Ask C: per fleet, the March service days Kerbline may bill: local calendar days during any part of which an
    installed unit had a session open. detections adds the days a unit captured detections, which only an open
    session can carry."""
    u = units(p)
    days = defaultdict(set)
    for x in p["sess"]["units"]:
        unit = x["unit_serial"]
        veh, grp, inst, rem = u[unit]
        for s in x["sessions"]:
            a, b = _utc(s["start_utc"]), _utc(s["end_utc"])
            if local_days:
                a, b = a.astimezone(TZ), b.astimezone(TZ)
            d, last = a.date(), (b.date() if any_part else a.date())
            while d <= last:
                if d.year == 2027 and d.month == 3 and (bench or (d >= inst and (rem is None or d < rem))):
                    days[unit].add(d)
                d += dt.timedelta(1)
    if detections:
        for d in p["det"]:
            unit = d["unit_serial"]
            day = dt.date.fromisoformat(d["captured_local"][:10])
            veh, grp, inst, rem = u[unit]
            if day.month == 3 and day >= inst and (rem is None or day < rem):
                days[unit].add(day)
    out = defaultdict(int)
    for unit, ds in days.items():
        out[u[unit][1]] += len(ds)
    total = sum(out.values())
    return dict(out), int(round(total * DAY_RATE + 1e-9))
