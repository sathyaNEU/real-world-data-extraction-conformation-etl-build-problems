"""Independent verifier: recomputes every graded figure from target/ alone, reading each file the way a solver would,
and compares them with golden/ and generator/figures.json.

    python3 task484/generator/verify.py
"""
import collections
import csv
import json
import os
import re

import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
FAIL = []


def ok(tag, cond, msg):
    print("%-5s %s %s" % (tag, "ok  " if cond else "FAIL", msg))
    if not cond:
        FAIL.append(tag)


def rows(name):
    with open(os.path.join(T, name), newline="") as f:
        return list(csv.DictReader(f))


def pdf(name):
    return " ".join(p.extract_text() for p in PdfReader(os.path.join(T, name)).pages).replace("\n", " ")


def r1(x):
    return round(x + 1e-9, 1)


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    prov = pdf("contingency_provisions_rwc.pdf")
    commit = {m.group(1): int(m.group(3)) for m in re.finditer(r"(Brannock|Ivelton|Quarrow|Saddeny|Wethermoor|Ellick) "
                                                              r"(Selwick|Corrin|Tamsey) (\d+)", prov)}
    ok("V0", len(commit) == 6, "six commitments read from Table 4-1")
    scc = {x["registry_appliance_code"]: x["scc"] for x in rows("scc_crosswalk_rwc.csv")}
    lab = {x["survey_appliance"]: x["scc"] for x in rows("scc_crosswalk_rwc.csv")}
    app = {x["application_appliance"]: x["scc"] for x in rows("scc_crosswalk_rwc.csv") if x["application_appliance"]}
    ef = {x["scc"]: float(x["factor"]) for x in rows("emission_factors_rwc_2023.csv") if x["pollutant"] == "PM2.5"}
    pellet = [s for s, l in lab.items() if s.startswith("Pellet")][0]
    pel = lab[pellet]
    area20 = {x["parcel_number"]: x["area_2020_boundary"] for x in rows("parcel_area_crosswalk.csv")}
    reg = rows("wood_device_registry_2026-06-30.csv")
    # the 2025-26 appliances: in place in the season, the 2020 boundary, each device once
    n26 = collections.Counter()
    for x in reg:
        if x["status"] == "A" and int(x["year_installed"]) <= 2025 and area20.get(x["parcel_number"]):
            n26[area20[x["parcel_number"]], scc[x["appliance_code"]]] += 1
    # the survey: wood burned per appliance by area and class (cords, or tons of pellets)
    conv = {"cords": 1.0, "face cords": 1 / 3.0, "pickup loads": 0.5, "tons": 1.0, "bags": 40 / 2000.0}
    sv = collections.defaultdict(list)
    for x in rows("household_wood_survey_2024_25.csv"):
        yr = x["year_installed"]
        yr = int(yr) if not yr.startswith("'") else (1900 + int(yr[1:]) if int(yr[1:]) > 30 else 2000 + int(yr[1:]))
        sv[x["maintenance_area"], lab[x["appliance"]]].append((float(x["amount_burned_2024_25"]) * conv[x["amount_unit"]],
                                                               x["wood_main_heat"] == "Yes", yr, float(x["weight"])))
    mean = lambda v: sum(u * w for u, s, y, w in v) / sum(w for u, s, y, w in v)
    # the changeouts: completed applications, by area (parcel or address), class and heat status
    by_addr = {}
    for x in reg:
        by_addr.setdefault((x["site_address"], x["county"]), x["parcel_number"])
    co = collections.Counter()
    for x in rows("changeout_applications_2015_2025.csv"):
        if x["status"] != "Completed":
            continue
        p = x["parcel_number"] or by_addr[x["site_address"], x["county"]]
        a = area20.get(p) or [y["area_2014_boundary"] for y in rows_cache(p)][0]
        prim = x["heat"] in ("P", "main heat source")
        co[a, app[x["existing_appliance"]], prim] += 1
    ws = openpyxl.load_workbook(os.path.join(T, "maintenance_plan_rwc_base_year_2014.xlsx"), read_only=True)["RWC base year 2014"]
    it = ws.iter_rows(values_only=True)
    next(it)
    n14 = {(r[0], r[2]): r[4] for r in it if r[0]}
    tpc = 1.163
    res = {}
    for a in commit:
        e26 = b14 = 0.0
        for s in ef:
            v = sv[a, s]
            m = mean(v)
            f = (1.0 if s == pel else tpc) * ef[s] / 2000
            e26 += n26[a, s] * m * f
            ncp, ncs = co[a, s, True], co[a, s, False]
            if ncp + ncs:
                mp = mean([z for z in v if z[1]])
                ms = mean([z for z in v if not z[1]])
                b14 += ((n14[a, s] - ncp - ncs) * m + ncp * mp + ncs * ms) * f
            else:
                old = [z for z in v if z[2] <= 2014]
                b14 += n14[a, s] * mean(old) * f
        red = 100 * (b14 - e26) / b14
        res[a] = (b14, e26, red, red < commit[a])
    if os.environ.get("VDEBUG"):
        for a in res:
            x = figs["areas"][a]
            print(a, "pm14 %.3f/%.1f pm26 %.3f/%.1f red %.3f/%.1f" % (res[a][0], x["pm14"], res[a][1], x["pm26"], res[a][2], x["reduction"]))
    trig = sorted(a for a in res if res[a][3])
    ok("V1", trig == figs["call"]["triggered"], "areas triggered: %s" % ", ".join(trig))
    ok("V2", all(abs(r1(res[a][2]) - figs["areas"][a]["reduction"]) < 1e-9 and abs(r1(res[a][0]) - figs["areas"][a]["pm14"]) < 1e-9
                 and abs(r1(res[a][1]) - figs["areas"][a]["pm26"]) < 1e-9 for a in res),
       "every area's base year, 2025-26 tons and reduction")
    ok("V3", min(abs(res[a][2] - commit[a]) for a in res) > 4.0,
       "every area more than 4 points from its commitment (min %.2f)" % min(abs(res[a][2] - commit[a]) for a in res))
    with open(os.path.join(GD, "contingency_determinations_2026_27.csv"), newline="") as f:
        det = {x["maintenance_area"]: x for x in csv.DictReader(f)}
    ok("V4", all(det[a]["determination"] == ("TRIGGERED" if res[a][3] else "NOT TRIGGERED") for a in res),
       "the determinations file agrees")
    # ask A: the registry's appliances in place in the 2014 season on the 2020 boundaries, each appliance once: a record
    # closed on a day another record of the same kind and install year is registered at the same address is the same
    # appliance registered again; records registered together at one address are two appliances
    reg_on = collections.defaultdict(list)
    for x in reg:
        reg_on[x["site_address"], x["county"], x["appliance_code"], x["year_installed"], x["registered_on"]].append(x)
    again = set()
    for x in reg:
        if x["status"] == "C" and x["status_reason"] == "Record closed":
            for y in reg_on.get((x["site_address"], x["county"], x["appliance_code"], x["year_installed"], x["status_date"]), []):
                if y["device_no"] != x["device_no"]:
                    again.add(y["device_no"])
    na = collections.Counter()
    for x in reg:
        if x["device_no"] in again or x["replaces_device_no"] or int(x["year_installed"]) > 2014:
            continue
        a = area20.get(x["parcel_number"])
        if a:
            na[a, scc[x["appliance_code"]]] += 1
    ok("V5", all(na[tuple(k.split("."))] == v["registry"] for k, v in figs["ask_a"].items()),
       "ask A: the registry's 2014-season appliances, 36 cells (%d re-registrations paired)" % len(again))
    print("\n%s" % ("all checks passed" if not FAIL else "FAILED: " + ", ".join(FAIL)))
    return 1 if FAIL else 0


_rows = {}


def rows_cache(p):
    if not _rows:
        for x in rows("parcel_area_crosswalk.csv"):
            _rows.setdefault(x["parcel_number"], []).append(x)
    return _rows.get(p, [])


if __name__ == "__main__":
    raise SystemExit(main())
