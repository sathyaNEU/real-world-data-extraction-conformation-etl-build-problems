"""verify.py: recompute every graded figure from the shipped bundle alone, on its own code path (no generator module),
and compare with generator/figures.json and the golden CSV. Reads every format the pack ships, each through one
extractor with a positive control.

    python3 task478/generator/verify.py [target]
"""
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
    qa = sheet(j("kerbline_qa_review_2027-03.xlsx"), "Review decisions")
    ok("xlsx read back: the review's header (control)", "Reviewed (UTC)" in qa[0])
    conf = {r["Defect ID"] for r in qa if r["Decision"] == "Confirmed"}
    near = defaultdict(list)
    for r in qa:
        if r["Decision"] == "Confirmed":
            near[r["Route"]].append((float(r["Milepost"]), r["Defect ID"]))
    dup = {r["Defect ID"]: min(near[r["Route"]], key=lambda c: (abs(c[0] - float(r["Milepost"])), c[1]))[1]
           for r in qa if r["Reason"] == "Duplicate"}
    det = rows(j("kerbline_detections_2027-03.csv"))
    where = defaultdict(Counter_)
    found_by = defaultdict(set)
    for d in det:
        k = dup.get(d["defect_id"], d["defect_id"])
        if k not in conf:
            continue
        s = seg_of(d["road_ref"], d["road_mp"])
        if s is None:
            continue
        where[k][s] += 1
        found_by[k].add(d["unit_serial"])
    pot = {k: max(c.items(), key=lambda kv: (kv[1], -int(kv[0])))[0] for k, c in where.items()}
    pot = {k: s for k, s in pot.items() if s in road}
    reg = sheet(j("kerbline_unit_register.xlsx"), "Units")
    units = defaultdict(list)
    fleet = {}
    for r in reg:
        a = excel_time(r["Installed"]).date()
        b = excel_time(r["Removed"]).date() if r["Removed"] else None
        units[r["Vehicle"]].append((r["Unit serial"], a, b))
        fleet[r["Unit serial"]] = (r["Fleet group"], a, b)
    drove = defaultdict(set)
    trav = rows(j("fleet_camera_traversals_2027-03.csv"))
    for t in trav:
        if t["segment_id"] not in road:
            continue
        day = dt.datetime.strptime(t["enter_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=Z).astimezone(ET).date()
        if (day.year, day.month) != (2027, 3):
            continue
        for u, a, b in units.get(t["vehicle_id"], []):
            if a <= day and (b is None or day < b):
                drove[t["segment_id"]].add(fleet[u][0])
    ok("every roadway segment has an installed unit's March pass", all(drove[s] for s in road))
    found_by = {k: {fleet[u][0] for u in us} for k, us in found_by.items()}
    num = den = 0
    for k, s in pot.items():
        C, f_ = len(drove[s]), len(found_by[k] & drove[s])
        if C >= 2:
            num += f_ * (f_ - 1)
            den += f_ * (C - 1)
    q = num / den
    est = defaultdict(float)
    for k, s in pot.items():
        est[road[s]["section"]] += 1 / (1 - (1 - q) ** len(drove[s]))
    rate = {sec: est[sec] / (lmi[sec] / 10) for sec in lmi}
    des = sorted(sec for sec, v in rate.items() if v >= 6.0)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    by_no = {str(x["section"]): (n, x) for n, x in figs["sections"].items()}
    ok("the confirmed potholes (%d) and lane-miles (%.1f) match" % (len(pot), sum(lmi.values())),
       len(pot) == figs["components"]["confirmed"] and round(sum(lmi.values()), 1) == figs["components"]["lane_miles"])
    ok("the find rate %.4f matches %.1f per cent" % (q, figs["components"]["find_rate_pct"]),
       round(100 * q, 1) == figs["components"]["find_rate_pct"])
    ok("the designated set matches", sorted(by_no[s][0] for s in des) == sorted(figs["call"]["designated"]))
    ok("every section's whole number matches", all(int(rate[s] + 0.5) == by_no[s][1]["rate"] for s in rate))
    # ask A
    known = {r["Defect ID"] for r in qa}
    loc = {(r["Route"], "%.3f" % float(r["Milepost"])): r["Defect ID"] for r in qa if r["Milepost"]}
    wo = rows(j("mms_cold_patch_orders_2027-03.csv"))
    done = [r for r in wo if r["status"] == "COMPLETE" and r["finished"][:2] == "03"]
    pots, lbs, lines = defaultdict(set), defaultdict(int), defaultdict(list)
    for r in done:
        ref = r["ext_ref"] if r["ext_ref"] in known else loc[(r["route"], r["milepost"])]
        pots[r["section"]].add(dup.get(ref, ref))
        lines[r["wo_number"]].append(r)
    sev = {d["defect_id"]: d["severity"] for d in det if d["severity"]}
    ref_of = lambda r: r["ext_ref"] if r["ext_ref"] in known else loc[(r["route"], r["milepost"])]
    big = defaultdict(int)
    for w, ls in lines.items():
        if len(ls) == 1:
            big[sev[ref_of(ls[0])]] = max(big[sev[ref_of(ls[0])]], int(ls[0]["cold_mix_lb"]))
    for w, ls in lines.items():
        v = [int(x["cold_mix_lb"]) for x in ls]
        total = len(ls) > 1 and len(set(v)) == 1 and v[0] > max(big[sev[ref_of(x)]] for x in ls)
        lbs[ls[0]["section"]] += v[0] if total else sum(v)
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
