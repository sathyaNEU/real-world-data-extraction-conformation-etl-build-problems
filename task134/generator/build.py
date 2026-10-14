"""Build task134's evidence pack into <out>/ (default: task134/target), then target.zip and metadata.json.

    python3 task134/generator/build.py [--out DIR] [--zip PATH] [--no-zip]
"""
import argparse
import csv
import datetime as dt
import json
import os
import shutil
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D
import observe as OB
import projects as PR
import sim as S
import world as W

TASK = os.path.dirname(HERE)
FILES = {
    "roll_old": "roll_extract_2014-2018.csv",
    "roll_new": "roll_extract_2019-2026.csv",
    "permits": "building_permits_2014-2026.csv",
    "buildings": "permit_buildings.csv",
    "occupancy": "occupancy_permits_2018-2026.csv",
    "folios": "folio_history_2014-2026.csv",
    "zoning": "zoning_schedule_2014-2026.csv",
    "notes": "extract_notes_2027-01-12.txt",
    "schedule": "tod_order_schedule_a.xlsx",
    "order": "tod_area_order_ridgemont_2026.pdf",
    "method": "housing_target_methodology_2026.pdf",
    "tables": "housing_reference_tables_2026.xlsx",
    "projections": "population_projections_2026-2036.csv",
    "rental": "rental_market_survey_oct2026.xlsx",
    "index": "folder_index_2027-01-15.txt",
}
DISTRACTORS = ["projections", "rental"]
MTIMES = {"roll_old": (2027, 1, 8, 15, 42), "roll_new": (2027, 1, 8, 15, 49), "permits": (2027, 1, 11, 9, 26),
          "buildings": (2027, 1, 11, 9, 27), "occupancy": (2027, 1, 11, 9, 31), "folios": (2027, 1, 11, 9, 35),
          "zoning": (2026, 12, 15, 11, 8), "notes": (2027, 1, 12, 14, 3), "schedule": (2026, 6, 30, 14, 58),
          "order": (2026, 6, 30, 15, 31), "method": (2026, 3, 24, 16, 15), "tables": (2026, 11, 20, 14, 37),
          "projections": (2026, 9, 17, 10, 44), "rental": (2026, 12, 14, 10, 2), "index": (2027, 1, 15, 16, 52)}

OLD_USE = {"house": "000 SINGLE FAMILY DWELLING", "house_suite": "032 RESIDENTIAL DWELLING WITH SUITE",
           "house_laneway": "034 SINGLE FAMILY DWELLING WITH LANEWAY HOUSE", "rental": "285 MULTI-FAMILY (APARTMENT BLOCK)",
           "rental_new": "285 MULTI-FAMILY (APARTMENT BLOCK)", "plan_summary": "299 STRATA PLAN SUMMARY"}
NEW_USE = {"house": "Detached house", "house_suite": "Detached house with suite or laneway house",
           "house_laneway": "Detached house with suite or laneway house", "comm": "Commercial",
           "rental": "Purpose-built rental", "rental_new": "Purpose-built rental", "strata": "Strata residential",
           "plan_summary": "Strata plan summary", "vacant": "Vacant or under construction"}


def truth():
    """the world and its records, in the neutral schema"""
    lots = S.make_lots()
    panel, rebuild, alive = S.simulate(lots)
    reg = PR.registry()
    projects = PR.build_projects(lots, rebuild, reg)
    others = PR.other_permits(lots, rebuild, projects)
    old_plans = PR.existing_strata(reg)
    rows, sidx = OB.roll(lots, projects, old_plans, W.value)
    permits = OB.permits(lots, projects, others)
    active_no = {p["project"]: p["permit_no"] for p in permits if p["role"] == "active"}
    occ = OB.occupancies(lots, projects, active_no)
    fh = OB.folio_history(lots, projects, sidx)
    sched = OB.schedule_a(lots, projects, old_plans, sidx)
    return dict(lots=lots, panel=panel, rebuild=rebuild, alive=alive, projects=projects, others=others,
                old_plans=old_plans, roll=rows, sidx=sidx, permits=permits, active_no=active_no, occ=occ, folios=fh,
                schedule=sched)


def _int(v):
    return "" if v is None else str(int(round(v)))


def write_roll(rows, lots, path_old, path_new):
    comm_use = {lot["lot_id"]: OB.comm_use(lot) for lot in lots if lot["kind"] == "comm"}
    old = sorted((r for r in rows if r["roll_year"] <= 2018), key=lambda r: (r["roll_year"], r["folio"]))
    new = sorted((r for r in rows if r["roll_year"] >= 2019), key=lambda r: (r["roll_year"], r["folio"]))
    n_old = n_new = 0
    with open(path_old, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ROLL_YEAR", "FOLIO", "CIVIC_ADDRESS", "NEIGHBOURHOOD", "ZONE", "ACTUAL_USE", "LAND_AREA", "AREA_UNIT",
                    "LAND_VALUE", "IMPROVEMENT_VALUE", "YEAR_BUILT", "STRATA_PLAN", "FINISHED_AREA"])
        for r in old:
            use = r["use"]
            if use == "comm":
                code = " ".join(comm_use[r["lot_id"]])
            elif use == "strata":
                code = ("054 STRATA-LOT ROWHOUSE" if r.get("townhouse") else "050 STRATA-LOT RESIDENCE (CONDOMINIUM)") \
                    if r.get("home", True) else "052 STRATA-LOT PARKING (RESIDENTIAL)"
            elif use == "vacant":
                g = r["group"]
                code = "201 VACANT COMMERCIAL" if g in ("TOD_C", "CORR_C", "CC_C") else "001 VACANT RESIDENTIAL LESS THAN 2 ACRES"
            else:
                code = OLD_USE[use]
            addr = ("%s-%d %s" % (r["unit_no"], r["civic"], r["street"]) if r["unit_no"] else "%d %s" % (r["civic"], r["street"])).upper()
            la, au = OB.lot_area_cols(r["area"]) if r["area"] else ("", "")
            w.writerow([r["roll_year"], r["folio"], addr, r["neighbourhood"], r["zone"], code, la, au, _int(r["land"]),
                        _int(r["imp"]), r["built"] or "", r["plan"], _int(r["floor"])])
            n_old += 1
    with open(path_new, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["roll_year", "folio", "civic_number", "street_name", "unit_no", "neighbourhood", "zone_code", "use_group",
                    "lot_area", "area_unit", "assessed_land", "assessed_improvements", "dwelling_units", "strata_lot_count",
                    "floor_area_sqft", "year_built", "strata_plan"])
        for r in new:
            la, au = OB.lot_area_cols(r["area"]) if r["area"] else ("", "")
            units = r["units"] if r["use"] in ("house", "house_suite", "house_laneway", "rental", "rental_new") else None
            w.writerow([r["roll_year"], r["folio"], r["civic"], r["street"], r["unit_no"], r["neighbourhood"].title(),
                        r["zone"], NEW_USE[r["use"]], la, au, _int(r["land"]), _int(r["imp"]), _int(units),
                        _int(r.get("strata_lots")), _int(r["floor"]), r["built"] or "", r["plan"]])
            n_new += 1
    return n_old, n_new


TYPE_LABEL = {"NEW": "New Construction", "DEMOLITION": "Demolition", "SUITE": "Secondary Suite", "LANEWAY": "Laneway House",
              "ALTERATION": "Alteration/Repair"}


def describe(p, lots, projects):
    lot = lots[p["lot_id"]]
    if p["type"] == "NEW":
        pj = projects[p["project"]]
        b = W.BTYPES[pj["btype"]]
        nb = len(pj["split"])
        bld = "building" if nb == 1 else "%d buildings" % nb
        tenure = "rental apartment" if pj["tenure"] == "rental" else "strata apartment"
        return "New %d-storey %s %s %s, %d dwelling units" % (pj["storeys"], b["cons"].lower(), tenure, bld, p["units"])
    if p["type"] == "DEMOLITION":
        what = {"house": "single family dwelling", "comm": "commercial building", "rental": "apartment building"}[lot["kind"]]
        return "Demolish %s" % what
    if p["type"] == "SUITE":
        return "Secondary suite in existing dwelling"
    if p["type"] == "LANEWAY":
        return "Laneway house, one dwelling unit"
    r = S.rng_for("alt", p["lot_id"], p["issue"].isoformat())
    return ["Interior renovation", "Re-roof", "Deck and stairs", "Tenant improvement", "Foundation repair",
            "Window replacement", "Kitchen and bath renovation", "Fire damage repair"][int(r.integers(0, 8))]


def write_permits(permits, lots, projects, path, path_b):
    n = nb = 0
    with open(path, "w", newline="", encoding="utf-8") as f, open(path_b, "w", newline="", encoding="utf-8") as fb:
        w = csv.writer(f, lineterminator="\n")
        wb = csv.writer(fb, lineterminator="\n")
        w.writerow(["permit_no", "permit_type", "status", "issued_date", "folio", "civic_address", "work_description",
                    "dwelling_units_created", "dwelling_units_demolished", "floor_area", "floor_area_unit",
                    "construction_value", "buildings", "revises_permit"])
        wb.writerow(["permit_no", "building_no", "storeys", "construction", "dwelling_units", "gross_floor_area"])
        for p in permits:
            metric = p["issue"] >= dt.date(2020, 1, 1)
            fa = p["gfa"]
            fa_out = "" if not fa else (round(fa * 0.092903) if metric else int(round(fa)))
            unit = "" if not fa else ("SQ M" if metric else "SQ FT")
            w.writerow([p["permit_no"], TYPE_LABEL[p["type"]], p["status"], p["issue"].isoformat(), p["folio"], p["address"],
                        describe(p, lots, projects), p["units"], p["units_demolished"], fa_out, unit,
                        int(round(p["value"])), p["buildings"] if p["type"] == "NEW" else 1, p.get("revises_no", "")])
            n += 1
            if p["type"] == "NEW":
                pj = projects[p["project"]]
                tot = sum(pj["split"])
                units = p["units"]
                split = list(pj["split"])
                if units != tot:
                    split = [int(round(u * units / tot)) for u in split[:-1]]
                    split.append(units - sum(split))
                for k, u in enumerate(split):
                    g = fa * u / units if units else 0
                    wb.writerow([p["permit_no"], k + 1, pj["storeys"], W.BTYPES[pj["btype"]]["cons"], u,
                                 round(g * 0.092903) if metric else int(round(g))])
                    nb += 1
    return n, nb


def write_occupancy(occ, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["occupancy_no", "permit_no", "building_no", "occupancy_type", "issued_date", "civic_address",
                    "dwelling_units"])
        for o in occ:
            w.writerow([o["occupancy_no"], o["permit_no"], o["building_no"], o["type"], o["issued"].isoformat(),
                        o["address"], o["units"]])
    return len(occ)


def write_folios(fh, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["event_date", "event", "retired_folio", "new_folio", "plan"])
        for r in fh:
            w.writerow([r["date"].isoformat(), r["event"], r["old"], r["new"], r["plan"]])
    return len(fh)


def projections_rows():
    r = S.rng_for("projections")
    base = {"ELL": 14650, "WES": 13820, "HAL": 12940, "PEL": 12210, "CC": 31480, "NC": 28760, "RAV": 26630,
            "FER": 24110, "REST": 167900}
    growth = {"ELL": .061, "WES": .058, "HAL": .056, "PEL": .052, "CC": .034, "NC": .012, "RAV": .011, "FER": .010,
              "REST": .008}
    pph0 = {"ELL": 2.31, "WES": 2.36, "HAL": 2.41, "PEL": 2.44, "CC": 1.92, "NC": 2.78, "RAV": 2.83, "FER": 2.86,
            "REST": 2.91}
    out = []
    for a in base:
        name = W.AREA_NAME.get(a, "Rest of city")
        if a in W.STATIONS:
            name += " station area"
        pop = base[a]
        for y in range(2026, 2037):
            if y > 2026:
                pop = pop * (1 + growth[a] * (1 - 0.035 * (y - 2027)) + float(r.uniform(-0.002, 0.002)))
            pph = pph0[a] - 0.006 * (y - 2026)
            out.append([name, y, int(round(pop, -1)), int(round(pop / pph)), "%.2f" % pph])
    return out


def rental_rows():
    r = S.rng_for("rental-survey")
    zones = [("Ellery-Westerly", 4120), ("Haldane-Pell Road", 3380), ("City Centre", 6950), ("North Calder", 2210),
             ("Ravensdale-Fernlea", 2590)]
    beds = [("Bachelor", .07, 1390), ("1 Bedroom", .46, 1720), ("2 Bedroom", .38, 2210), ("3 Bedroom +", .09, 2640)]
    out = []
    for y in range(2022, 2027):
        for z, u in zones:
            for b, share, rent in beds:
                units = int(round(u * share * (1 + 0.012 * (y - 2022)) * float(r.uniform(0.97, 1.03))))
                vac = max(0.3, 1.1 + 0.55 * (y - 2022) + float(r.uniform(-0.5, 0.5)))
                rnt = rent * (1.052 ** (y - 2022)) * (1.08 if z == "City Centre" else 1.0) * float(r.uniform(0.97, 1.03))
                out.append([y, z, b, units, round(vac, 1), int(round(rnt, -1))])
    return out


def set_mtime(path, key):
    t = W.posix(dt.datetime(*MTIMES[key]))
    os.utime(path, (t, t))


def build(out, T=None):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    T = T or truth()
    lots, projects = T["lots"], T["projects"]
    p = lambda k: os.path.join(out, FILES[k])
    r_old, r_new = write_roll(T["roll"], lots, p("roll_old"), p("roll_new"))
    n_bp, n_pb = write_permits(T["permits"], lots, projects, p("permits"), p("buildings"))
    n_oc = write_occupancy(T["occ"], p("occupancy"))
    n_fh = write_folios(T["folios"], p("folios"))
    D.zoning_csv(p("zoning"))
    D.notes_txt(p("notes"), dict(r1=format(r_old, ","), r2=format(r_new, ","), bp=format(n_bp, ","), pb=format(n_pb, ","),
                                 oc=format(n_oc, ","), fh=format(n_fh, ",")))
    D.schedule_xlsx(T["schedule"], p("schedule"))
    D.order_pdf(p("order"))
    D.methodology_pdf(p("method"))
    D.reference_xlsx(p("tables"))
    D.projections_csv(p("projections"), projections_rows())
    D.rental_xlsx(p("rental"), rental_rows())
    D.index_txt(p("index"))
    for k in FILES:
        set_mtime(p(k), k)
    return T


def zip_target(src, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(src)):
            fp = os.path.join(src, name)
            st = os.stat(fp)
            zi = zipfile.ZipInfo("target/" + name, date_time=dt.datetime.fromtimestamp(st.st_mtime, W.TZ).timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(fp, "rb") as f:
                z.writestr(zi, f.read())


def write_metadata():
    meta = {"task": "task134", "objective": "Forecasting & Predictive Modeling", "domain": "Urban & Regional Science",
            "task_type": "Land use and spatial development modeling",
            "distractor_files": ["target/" + FILES[k] for k in DISTRACTORS],
            "deliverables": ["tod_housing_target_2027-31.xlsx", "tod_completions_2022-26.png"],
            "as_of": "2026-12-31",
            "sources": {FILES[k]: "constructed in the layout of the issuing organisation's own export; synthetic, "
                                  "released with the task under CC BY 4.0" for k in FILES}}
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    ap.add_argument("--zip", default=os.path.join(TASK, "target.zip"))
    ap.add_argument("--no-zip", action="store_true")
    a = ap.parse_args()
    build(a.out)
    write_metadata()
    if not a.no_zip:
        zip_target(a.out, a.zip)
    print("built", a.out)


if __name__ == "__main__":
    main()
