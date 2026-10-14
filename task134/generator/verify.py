"""Independent verifier: reads only the shipped bundle (target/ or a target.zip) and recomputes the call, its
components, the default path and both asks on its own code path (csv and openpyxl, no pandas, no generator
module), then compares them with generator/figures.json.

    python3 task134/generator/verify.py [--zip task134/target.zip]
Exit 0 when every figure reproduces, 1 otherwise.
"""
import csv
import io
import json
import math
import os
import sys
import zipfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


class Bundle:
    def __init__(self, zpath=None):
        self.z = zipfile.ZipFile(zpath) if zpath else None

    def open(self, name):
        if self.z:
            return io.BytesIO(self.z.read("target/" + name))
        return open(os.path.join(TASK, "target", name), "rb")

    def rows(self, name):
        with self.open(name) as f:
            return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8")))

    def book(self, name):
        with self.open(name) as f:
            return openpyxl.load_workbook(io.BytesIO(f.read()), read_only=True, data_only=True)


NB = {"ELLERY": "Ellery", "WESTERLY": "Westerly", "HALDANE": "Haldane", "PELL ROAD": "Pell Road",
      "CALDERBROOK CENTRE": "Calderbrook Centre", "NORTH CALDER": "North Calder", "RAVENSDALE": "Ravensdale",
      "FERNLEA": "Fernlea"}


def kind_old(code):
    c = code[:3]
    if c in ("000", "032", "034"):
        return "house"
    if c in ("210", "214", "220", "230", "260"):
        return "comm"
    if c == "285":
        return "rental"
    return None


def kind_new(use):
    return {"Detached house": "house", "Detached house with suite or laneway house": "house", "Commercial": "comm",
            "Purpose-built rental": "rental"}.get(use)


def num(s):
    s = (s or "").strip()
    return float(s) if s else None


def load(B):
    roll = {}
    for r in B.rows("roll_extract_2014-2018.csv"):
        a = num(r["LAND_AREA"])
        if a is not None and r["AREA_UNIT"] == "AC":
            a *= 43560.0
        code = r["ACTUAL_USE"][:3]
        units = 2 if code in ("032", "034") else (1 if code == "000" else None)
        roll[(r["FOLIO"], int(r["ROLL_YEAR"]))] = dict(
            kind=kind_old(r["ACTUAL_USE"]), zone=r["ZONE"], area=NB[r["NEIGHBOURHOOD"]], sqft=a,
            land=num(r["LAND_VALUE"]), imp=num(r["IMPROVEMENT_VALUE"]), units=units, use=r["ACTUAL_USE"], unit_no="",
            floor=num(r["FINISHED_AREA"]))
    for r in B.rows("roll_extract_2019-2026.csv"):
        a = num(r["lot_area"])
        if a is not None and r["area_unit"] == "AC":
            a *= 43560.0
        roll[(r["folio"], int(r["roll_year"]))] = dict(
            kind=kind_new(r["use_group"]), zone=r["zone_code"], area=r["neighbourhood"], sqft=a,
            land=num(r["assessed_land"]), imp=num(r["assessed_improvements"]), units=num(r["dwelling_units"]),
            use=r["use_group"], unit_no=r["unit_no"], floor=num(r["floor_area_sqft"]))
    zones = {}
    for r in B.rows("zoning_schedule_2014-2026.csv"):
        u = r["residential_use"]
        form = ("house" if u.startswith("Single detached") else "town" if u.startswith("Townhouses") else
                "none" if u == "Not permitted" else "tower" if "no height limit" in u else
                "low" if "to 4 storeys" in u else "mid")
        zones[r["zone_code"]] = (form, float(r["max_floor_area_ratio"] or 0))
    wb = B.book("housing_reference_tables_2026.xlsx")
    types = {}
    for row in wb["Building types"].iter_rows(min_row=4, max_row=7, values_only=True):
        types[row[0]] = (float(row[5]), float(row[6]))
    values = {}
    for row in wb["Sale values"].iter_rows(min_row=4, values_only=True):
        if row[0]:
            values[(int(row[0]), row[1])] = {"town": row[2], "wood": row[3], "conc": row[4]}
    costs = {}
    for row in wb["Construction costs"].iter_rows(min_row=4, values_only=True):
        if row[0]:
            costs[int(row[0])] = {"TH3": row[1], "LR4": row[2], "MR6": row[3], "HR": row[4]}
    sched = []
    for row in B.book("tod_order_schedule_a.xlsx")["Schedule A"].iter_rows(min_row=4, values_only=True):
        if row[0]:
            sched.append((row[0], row[1], row[2], row[3]))
    permits = B.rows("building_permits_2014-2026.csv")
    folios = B.rows("folio_history_2014-2026.csv")
    occ = B.rows("occupancy_permits_2018-2026.csv")
    blds = B.rows("permit_buildings.csv")
    return roll, zones, types, values, costs, sched, permits, folios, occ, blds


def options(form, far):
    o = []
    if form in ("town", "low", "mid", "tower") and far >= 0.7:
        o.append(("TH3", min(1.2, far), "town"))
    if form in ("low", "mid", "tower") and far >= 1.5:
        o.append(("LR4", min(2.0, far), "wood"))
    if form in ("mid", "tower") and far >= 3.0:
        o.append(("MR6", 3.0, "wood"))
    if form == "tower" and far > 3.0:
        o.append(("HR", far, "conc"))
    return o


def best(types, values, costs, sqft, area, form, far, y):
    top = (None, 0.0, -math.inf)
    for t, f, prod in options(form, far):
        eff = types[t][0]
        v = sqft * f * (eff * values[(y, area)][prod] - costs[y][t])
        if v > top[2]:
            top = (t, f, v)
    return top


def main(argv):
    zpath = argv[argv.index("--zip") + 1] if "--zip" in argv else None
    B = Bundle(zpath)
    roll, zones, types, values, costs, sched, permits, folios, occ, blds = load(B)
    fails = []

    def check(label, got, want, tol=0.0):
        good = (abs(got - want) <= tol) if isinstance(want, (int, float)) else got == want
        print("%-4s %-58s %s%s" % ("ok" if good else "FAIL", label, got, "" if good else "  (figures.json: %s)" % (want,)))
        if not good:
            fails.append(label)

    # counted permits for new construction: first issue year per folio; a revision counted once (methodology 2.3)
    first = {}
    for p in permits:
        if p["permit_type"] == "New Construction" and p["status"] in ("Issued", "Completed", "Superseded"):
            y = int(p["issued_date"][:4])
            first[p["folio"]] = min(y, first.get(p["folio"], 9999))
    # the record: feasible lot-years and rebuilds by kind
    n = {"house": 0, "comm": 0, "rental": 0}
    e = dict(n)
    for (folio, y), r in roll.items():
        k = r["kind"]
        if not k or (folio in first and y > first[folio]):
            continue
        form, far = zones[r["zone"]]
        t, f, v = best(types, values, costs, r["sqft"], r["area"], form, far, y)
        if t and v / (r["land"] + r["imp"]) > 1.0:
            n[k] += 1
            e[k] += 1 if first.get(folio) == y else 0
    rate = {k: e[k] / n[k] for k in n}
    # Schedule A carried forward through the folio history
    nxt = {}
    for r in folios:
        nxt.setdefault(r["retired_folio"], []).append(r["new_folio"])
    band_far = {"Within 200 m": 5.0, "200 m to 400 m": 4.0, "400 m to 800 m": 3.0}
    cur = {}
    for folio, addr, station, band in sched:
        stack = [folio]
        while stack:
            f = stack.pop()
            if f in nxt:
                stack.extend(nxt[f])
            else:
                cur.setdefault(f, (station, band))
    standing = []
    for f, (station, band) in cur.items():
        r = roll.get((f, 2026))
        if not r or not r["kind"] or f in first:
            continue
        far = max(band_far[band], zones[r["zone"]][1])
        t, fb, v = best(types, values, costs, r["sqft"], r["area"], "tower", far, 2026)
        eff, nsf = types[t]
        homes = math.floor(r["sqft"] * fb * eff / nsf + 1e-9)
        units = 0 if r["kind"] == "comm" else int(r["units"])
        standing.append((r["kind"], v / (r["land"] + r["imp"]), homes - units, t))
    yearly = []
    for j in range(5):
        yearly.append(sum(rate[k] * (1 - rate[k]) ** j * net for k, R, net, t in standing if R > 1.0))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    for y, v in zip(range(2027, 2032), yearly):
        check("net new homes %d (to the nearest 100)" % y, int(round(v / 100.0) * 100), fig["call"]["yearly"][str(y)])
        check("net new homes %d unrounded" % y, round(v, 1), fig["unrounded"]["yearly"][str(y)], 0.05)
    check("net new homes 2027 to 2031 (to the nearest 500)", int(round(sum(yearly) / 500.0) * 500), fig["call"]["total"])
    c = fig["components"]
    check("standing lots", len(standing), c["standing_lots"])
    for k in ("house", "comm", "rental"):
        check("rebuild rate, %s (per cent, one decimal)" % k, round(100 * rate[k], 1), c["rates_pct"][k])
        check("rebuilds, %s" % k, e[k], c["rebuilds"][k])
        check("feasible lot-years, %s" % k, n[k], c["feasible_lot_years"][k])
    check("net homes once every standing lot is rebuilt", sum(net for _, _, net, _ in standing), c["net_homes_once_rebuilt"])
    check("best-paying building on every standing lot", sorted(set(t for *_, t in standing)), ["MR6"])
    check("every standing lot feasible", all(R > 1.0 for _, R, _, _ in standing), True)
    # the default path: zoned capacity at the corridors' take-up since their 2013 rezoning
    cap_c = 0.0
    corridor = set()
    for (folio, y), r in roll.items():
        if y == 2014 and r["zone"] == "CR-3" and r["sqft"]:
            corridor.add(folio)
            cap_c += max(0.0, math.floor(r["sqft"] * 3.0 * 0.85 / 820 + 1e-9) - (r["units"] or 0))
    created = {}
    for p in sorted(permits, key=lambda p: p["issued_date"]):
        if p["permit_type"] == "New Construction" and p["status"] in ("Issued", "Completed", "Superseded") \
                and p["folio"] in corridor:
            if p["status"] != "Superseded" or p["folio"] not in created:
                created[p["folio"]] = int(p["dwelling_units_created"]) - int(p["dwelling_units_demolished"])
    tk = sum(created.values()) / cap_c / 13.0
    cap = 0.0
    for f, (station, band) in cur.items():
        r = roll.get((f, 2026))
        if not r or not r["sqft"]:
            continue
        far = max(band_far[band], zones[r["zone"]][1])
        cap += max(0.0, math.floor(r["sqft"] * far * 0.85 / 820 + 1e-9) - (r["units"] or 0))
    check("default path: net new homes a year at the take-up", int(round(cap * tk)), fig["default"]["yearly"], 1)
    # Ask A: homes completed, by station area and year of each building's first occupancy
    prev = {}
    for r in folios:
        prev.setdefault(r["new_folio"], []).append(r["retired_folio"])
    station_of = {}
    for folio, addr, station, band in sched:
        for start, graph in ((folio, prev), (folio, nxt)):
            stack = [start]
            while stack:
                f = stack.pop()
                station_of.setdefault(f, (station, band))
                stack.extend(g for g in graph.get(f, []) if g not in station_of)
    pfolio = {p["permit_no"]: p["folio"] for p in permits}
    bunits = {(b["permit_no"], b["building_no"]): int(b["dwelling_units"]) for b in blds}
    firsts = {}
    for o in occ:
        key = (o["permit_no"], o["building_no"])
        if key not in firsts or o["issued_date"] < firsts[key]:
            firsts[key] = o["issued_date"]
    grid_a = {}
    for key, d in firsts.items():
        y = int(d[:4])
        st = station_of.get(pfolio[key[0]])
        if st and 2022 <= y <= 2026:
            grid_a[(st[0], y)] = grid_a.get((st[0], y), 0) + bunits[key]
    for s, row in fig["ask_a"].items():
        for y, v in row.items():
            check("Ask A %s %s" % (s, y), grid_a.get((s, int(y)), 0), v)
    # Ask B: homes standing at the 2026 roll on the order's lots, by station area and band
    grid_b = {}
    for (f, y), r in roll.items():
        if y != 2026 or f not in station_of:
            continue
        s, band = station_of[f]
        if r["use"] in ("Detached house", "Detached house with suite or laneway house", "Purpose-built rental"):
            h = int(r["units"])
        elif r["use"] == "Strata residential":
            h = 1 if (r["unit_no"] or r["floor"] is not None) else 0
        else:
            h = 0
        grid_b[(s, band)] = grid_b.get((s, band), 0) + h
    for s, row in fig["ask_b"].items():
        for band, v in row.items():
            check("Ask B %s %s" % (s, band), grid_b.get((s, band), 0), v)
    print("VERIFY %s: %d failures" % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
