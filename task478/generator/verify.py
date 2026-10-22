"""verify.py: recompute every graded figure from the shipped bundle alone, on its own code path (no generator module),
and compare with generator/figures.json and the golden CSV. Reads every format the pack ships, each through one
extractor with a positive control.

    python3 task478/generator/verify.py [target]
"""
import bisect
import csv
import datetime as dt
import json
import os
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ET = ZoneInfo("America/New_York")
Z = dt.timezone.utc
OK = []


def ok(name, cond):
    OK.append((name, bool(cond)))
    print("%s  %s" % ("PASS" if cond else "FAIL", name))


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sheet(path, name):
    """A worksheet's rows through the workbook's XML: shared strings and inline values, no spreadsheet library."""
    import re
    import xml.etree.ElementTree as ET_
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        wb = ET_.fromstring(z.read("xl/workbook.xml"))
        names = [s.get("name") for s in wb.find("m:sheets", ns)]
        idx = names.index(name) + 1
        sst = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET_.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                sst.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        data = ET_.fromstring(z.read("xl/worksheets/sheet%d.xml" % idx))
    out = []
    for r in data.find("m:sheetData", ns):
        vals = {}
        for c in r.findall("m:c", ns):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find("m:v", ns)
            if v is None:
                continue
            vals[col] = sst[int(v.text)] if c.get("t") == "s" else v.text
        out.append(vals)
    head = out[0]
    cols = sorted(head, key=lambda c: (len(c), c))
    return [{head[c]: r.get(c) for c in cols} for r in out[1:]]


def excel_time(v):
    return dt.datetime(1899, 12, 30) + dt.timedelta(days=float(v))


def pdf_lines(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return "\n".join(pg.extract_text() or "" for pg in pdf.pages)


def main(target=None):
    T = target or os.path.join(TASK, "target")
    j = lambda n: os.path.join(T, n)
    inv = {r["segment_id"]: r for r in rows(j("road_inventory_2026.csv"))}
    ok("csv read back: the inventory has its first segment (control)", "2210437" in inv)
    tb_text = pdf_lines(j("route_turnback_notice_2027-03.pdf"))
    ok("pdf read back: the turnback notice's effective time (control)", "12:01 a.m. on 15 March 2027" in tb_text.replace("\n", " "))
    turned = {ln.split()[2] for ln in tb_text.splitlines() if ln.startswith("SR ") and len(ln.split()) >= 7}
    ok("five segments turned back", len(turned) == 5 and turned <= set(inv))
    road = {k: v for k, v in inv.items() if k not in turned}
    lmi = defaultdict(float)
    for k, v in road.items():
        lmi[v["section"]] += float(v["length_mi"]) * int(v["through_lanes"])
    prog = pdf_lines(j("spring_patching_program_2027.pdf")).replace("\n", " ")
    ok("pdf read back: the program's line (control)", "6.0 or more potholes per ten lane-miles" in prog)
    # the 2025 to 2026 map
    xw = defaultdict(list)
    for r in rows(j("road_inventory_crosswalk_2025_2026.csv")):
        xw[r["segment_id_2025"]].append((r["segment_id_2026"], float(r["begin_mp_2026"]), float(r["end_mp_2026"])))

    def seg_of(ref, mp):
        if not ref:
            return None
        if ref in xw:
            return next(s for s, lo, hi in xw[ref] if lo <= float(mp) <= hi)
        return ref if ref in inv else None
    reg = sheet(j("kerbline_unit_register.xlsx"), "Units")
    ok("xlsx read back: the register's header (control)", "Unit serial" in reg[0])
    # each detection's pass: its unit's vehicle, its capture time in UTC, the vehicle's traversal at that moment
    veh_of = {r["Unit serial"]: r["Vehicle"] for r in reg}
    trav = defaultdict(list)
    for r in rows(j("fleet_camera_traversals_2027-03.csv")):
        a = dt.datetime.strptime(r["enter_utc"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=Z)
        b = dt.datetime.strptime(r["exit_utc"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=Z)
        trav[r["vehicle_id"]].append((a, b, r["segment_id"], r["direction"]))
    for k in trav:
        trav[k].sort()
    starts = {k: [x[0] for x in v] for k, v in trav.items()}
    det = rows(j("kerbline_detections_2027-03.csv"))
    ok("csv read back: the detections carry a pothole class (control)", any(d["defect_class"] == "pothole" for d in det))
    pas = {}
    for d in det:
        if not d["road_mp"]:
            continue
        t = dt.datetime.strptime(d["captured_local"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=ET).astimezone(Z)
        best = None
        vv = veh_of[d["unit_serial"]]
        hi_ = bisect.bisect_right(starts[vv], t + dt.timedelta(seconds=3))
        for a, b, seg, dirn in trav[vv][max(0, hi_ - 3):hi_]:
            if a - dt.timedelta(seconds=3) <= t <= b + dt.timedelta(seconds=3):
                gap = 0 if a <= t <= b else min(abs((t - a).total_seconds()), abs((t - b).total_seconds()))
                if best is None or gap < best[0]:
                    best = (gap, a, b, seg, dirn)
        if best is not None:
            _, a, b, seg, dirn = best
            pas[d["detection_id"]] = (1 if dirn in ("NB", "EB") else -1,
                                      float(inv[seg]["length_mi"]) / (b - a).total_seconds())
    ok("every detection on the state routes has its pass", len(pas) == sum(1 for d in det if d["road_mp"]))
    # each unit's latency as the median of error along the direction of travel over speed (a code path of its own:
    # methods.py's golden fits through the origin), the covers matched within a tenth of a mile
    covers = defaultdict(list)
    for r in rows(j("utility_cover_inventory_2026.csv")):
        covers[r["route"]].append(float(r["milepost"]))
    ratios = defaultdict(list)
    for d in det:
        if d["defect_class"] == "utility_cover" and d["road_mp"]:
            x = float(d["road_mp"])
            c = min(covers[d["route"]], key=lambda m: abs(m - x))
            if abs(c - x) <= 0.1:
                sg, v = pas[d["detection_id"]]
                ratios[d["unit_serial"]].append((x - c) * sg / v)
    lat = {}
    for k, xs in ratios.items():
        xs = sorted(xs)
        n = len(xs)
        lat[k] = xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])
    ok("every unit's latency fitted on the covers", len(lat) == len(reg))
    seg_by_route = defaultdict(list)
    for k, s in road.items():
        seg_by_route[s["route"]].append((float(s["begin_mp"]), float(s["end_mp"]), k))
    pots = defaultdict(list)
    for d in det:
        if d["defect_class"] == "pothole" and d["road_mp"] and d["captured_local"][:7] == "2027-03":
            sg, v = pas[d["detection_id"]]
            pots[d["route"]].append(float(d["road_mp"]) - sg * lat[d["unit_serial"]] * v)
    count = defaultdict(int)
    for rt, xs in pots.items():
        xs.sort()
        runs = [[xs[0]]]
        for m1, m2 in zip(xs, xs[1:]):
            if (m2 - m1) * 5280 <= 12.0:
                runs[-1].append(m2)
            else:
                runs.append([m2])
        for run in runs:
            mid = run[(len(run) - 1) // 2]
            hit = [k for lo, hi, k in seg_by_route.get(rt, []) if lo - 1e-9 <= mid <= hi + 1e-9]
            if hit:
                count[road[hit[0]]["section"]] += 1
    rate = {sec: count[sec] / (lmi[sec] / 10) for sec in lmi}
    des = sorted(sec for sec, v_ in rate.items() if v_ >= 6.0)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    by_no = {str(x["section"]): (n, x) for n, x in figs["sections"].items()}
    ok("the potholes (%d) and lane-miles (%.1f) match" % (sum(count.values()), sum(lmi.values())),
       sum(count.values()) == figs["components"]["potholes"] and round(sum(lmi.values()), 1) == figs["components"]["lane_miles"])
    ok("the designated set matches", sorted(by_no[s][0] for s in des) == sorted(figs["call"]["designated"]))
    ok("every section's whole number matches", all(int(rate[s] + 0.5) == by_no[s][1]["rate"] for s in rate))
    # ask A
    wo = rows(j("mms_cold_patch_orders_2027-03.csv"))
    done = [r for r in wo if r["status"] == "COMPLETE" and r["finished"][:2] == "03"]
    lbs, lines = defaultdict(int), defaultdict(list)
    for r in done:
        lines[r["wo_number"]].append(r)
    sev = {d["detection_id"]: d["severity"] for d in det if d["severity"]}
    segs = defaultdict(list)
    for r in inv.values():
        segs[r["route"]].append((float(r["begin_mp"]), float(r["end_mp"]), r["section"]))
    sec_at = lambda x: next(s for lo, hi, s in segs[x["route"]] if lo <= float(x["milepost"]) <= hi)
    for w, ls in lines.items():
        vals = [int(x["cold_mix_lb"]) for x in ls]
        if len(ls) > 1 and len(set(vals)) == 1 and len({x["finished"] for x in ls}) == 1:
            lbs[sec_at(ls[0])] += vals[0]
        else:
            for x, v in zip(ls, vals):
                lbs[sec_at(x)] += v
    ok("ask A pounds match", all(lbs[s] == by_no[s][1]["cold_mix_lb"] for s in by_no))
    # the golden CSV carries the same figures
    gc = rows(os.path.join(TASK, "golden", "tamsett_spring_patching_sections_2027.csv"))
    ok("golden CSV agrees with every graded figure", all(
        int(r["potholes_per_10_lane_miles"]) == by_no[r["section"]][1]["rate"] and
        int(r["cold_mix_lb_mar"]) == by_no[r["section"]][1]["cold_mix_lb"] and
        r["dedicated_crew"] == by_no[r["section"]][1]["crew"] for r in gc))
    gp = pdf_lines(os.path.join(TASK, "golden", "tamsett_spring_patching_task_orders_2027.pdf")).replace("\n", " ")
    ok("golden PDF carries every designated section", all(n in gp for n in figs["call"]["designated"]))
    fails = [n for n, c in OK if not c]
    print("%d verifications, %d failed" % (len(OK), len(fails)))
    return 0 if not fails else 1


class Counter_(dict):
    def __missing__(self, key):
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
