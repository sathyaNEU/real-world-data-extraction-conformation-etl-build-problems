"""Write target/ from the clean truth: the registration extract, the two medical examiner offices' logs, the postcode
lookup, the registration districts, the three context files and (through docs.py) the fund's terms and the data
notes. Every file is written the way its source system exports it."""
import csv
import datetime as dt
import io
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import docs
import postprocess as PP
import world as W

REG = "ellesmoor_death_registrations_2021-2026.csv"
NORTH = "north_ellesmoor_me_office_log.xlsx"
SOUTH = "south_ellesmoor_me_office_cases.json"
LOOKUP = "postcode_to_place_lookup.csv"
DISTRICTS = "registration_districts.csv"
POPULATION = "population_estimates_mid-2025.csv"
TEMPERATURE = "daily_max_temperature_2026.csv"
ALERTS = "heat_health_alerts_summer_2026.csv"
TERMS = "heat_resilience_fund_2027_terms.pdf"
CARE = "care_home_locations_2026-10.xlsx"
DISTRACTORS = [POPULATION, TEMPERATURE, ALERTS, CARE]

CARE_NAMES = ["Beech Lodge", "The Laurels", "Holly Bank", "Ashgrove House", "Moorside Court", "Elm Tree Lodge",
              "Rowan House", "Fernlea", "Oak Lodge", "The Willows", "Heathview", "Millbrook House", "Larch Court",
              "Brookfield", "Highcroft", "Meadowbank", "Cedar House", "Woodlands", "Thornfield House", "Valley View",
              "Birch Court", "Rose Lodge", "Greenacres", "Hillside", "Linden House", "Spring Bank", "Hawthorn Lodge",
              "Westfield", "Prospect House", "Moorlands", "Kingfisher Court", "Orchard House", "Bramley Lodge",
              "Sycamore House", "Riverside", "Hazelwood", "Primrose Court", "St Anne's", "Lilac House", "Abbeyfield",
              "Glebe House", "Fairview", "Clough Bank", "Mill View", "The Grange", "Ivy Court", "Southlands",
              "Copper Beeches", "Holme Lea", "Wharf House"]
OLD_CODE = {"Hollinsgate": "HOL", "Ashwold and Thornley": "ASH", "Calderholt": "CAL", "Brinmoor and Moorbridge": "BRM",
            "Kexley": "KEX"}
NEW_CODE = {"Hollinsgate": "E30000801", "Ashwold and Thornley": "E30000802", "Calderholt": "E30000803",
            "Brinmoor and Moorbridge": "E30000804", "Kexley": "E30000917"}


def fmt_reg_date(d, old):
    return d.strftime("%d/%m/%Y") if old else d.isoformat()


def write_csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def care_home_name(T, pc):
    keys = sorted({x["pod_pc"] for x in T.deaths if x["pod"] == "Care home"})
    return {k: CARE_NAMES[i % len(CARE_NAMES)] for i, k in enumerate(keys)}


def registrations(T, path):
    names = care_home_name(T, None)
    rows = []
    for r in T.rows:
        x = r["death"]
        old = r["date"] < W.SYSTEM_CHANGE
        dist = x["district"]
        if x["pod"] == "Care home":
            pod = names[x["pod_pc"]]
        else:
            pod = x["pod_name"]
        rows.append([dist, OLD_CODE[dist] if old else NEW_CODE[dist], r["entry"], 1 if r["kind"] == "Registration" else 2,
                     fmt_reg_date(r["date"], old), fmt_reg_date(x["dod"], old), x["surname"].upper(), x["forenames"],
                     fmt_reg_date(x["dob"], old), x["sex"], x["age"], r["marital"], r["occupation"], r["usual_pc"],
                     W.CODE[r["place"]], x["pod"], pod, x["pod_pc"], r["cert"]])
    header = ["registration_district", "district_code", "entry_number", "version", "date_of_registration",
              "date_of_death", "deceased_surname", "deceased_forenames", "date_of_birth", "sex", "age_at_death",
              "marital_status", "occupation", "usual_address_postcode", "usual_residence_code",
              "place_of_death_type", "place_of_death", "place_of_death_postcode", "certification"]
    write_csv(path, header, rows)
    return len(rows)


DEC_N = {"100A": "Form 100A (no post-mortem)", "Post-mortem": "Post-mortem ordered", "Inquest opened": "Inquest opened",
         "Awaiting decision": "Awaiting decision", "Advice only": "Advice only"}
DEC_S = {"100A": "100A", "Post-mortem": "post_mortem", "Inquest opened": "inquest_opened",
         "Awaiting decision": "awaiting", "Advice only": "advice_only"}
POD_S = {"Hospital": "hospital", "Hospice": "hospice", "Home": "home", "Care home": "care_home", "Other": "other"}


def north_log(T, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Scrutiny log"
    hdr = ["Case ref", "Date of death", "Deceased", "Date of birth", "Usual postcode", "Place of death",
           "Scrutiny completed", "Outcome", "Coroner ref", "Coroner decision", "Decision date"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="005EB8")
        c.alignment = Alignment(vertical="center")
    names = care_home_name(T, None)
    n = 0
    for c in T.cases:
        if c["area"] != "North":
            continue
        x = c["death"]
        pod = names[x["pod_pc"]] if x["pod"] == "Care home" else (
            "Home" if x["pod"] == "Home" else x["pod_name"])
        ws.append([c["ref"], x["dod"], "%s, %s" % (x["surname"].upper(), c["forenames"]), x["dob"], x["usual_pc"], pod,
                   c["completed"], "MCCD issued" if c["outcome"] == "MCCD" else "Referred to coroner",
                   c["cref"] or None, DEC_N[c["decision"]] if c["decision"] else None, c["decision_date"]])
        n += 1
    for row in ws.iter_rows(min_row=2):
        for idx in (1, 3, 6, 10):
            if row[idx].value is not None:
                row[idx].number_format = "dd/mm/yyyy"
    for col, wdt in zip("ABCDEFGHIJK", [12, 12, 34, 12, 11, 30, 13, 20, 12, 26, 12]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    wb.properties.creator = "Medical Examiner Office"
    wb.properties.lastModifiedBy = "Medical Examiner Office"
    wb.properties.created = dt.datetime(2024, 9, 2, 9, 12, 40)
    wb.properties.modified = dt.datetime(2026, 10, 9, 16, 48, 5)
    wb.save(path)
    PP.normalize_zip(path, modified="2026-10-09T16:48:05Z",
                     company="Hollinsgate Teaching Hospitals NHS Foundation Trust")
    return n


def utc(d, minute_of_day):
    """a local time on date d, as the South office's system stores it (UTC)"""
    local = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=minute_of_day)
    bst = dt.date(d.year, 3, 31) - dt.timedelta(days=(dt.date(d.year, 3, 31).weekday() + 1) % 7) <= d < \
        dt.date(d.year, 10, 31) - dt.timedelta(days=(dt.date(d.year, 10, 31).weekday() + 1) % 7)
    return (local - dt.timedelta(hours=1 if bst else 0)).strftime("%Y-%m-%dT%H:%M:%SZ")


def south_cases(T, path):
    rng = np.random.default_rng(W.SEED + 7)
    names = care_home_name(T, None)
    out = []
    for c in T.cases:
        if c["area"] != "South":
            continue
        x = c["death"]
        sur = x["surname"]
        given = c["forenames"]
        pod = names[x["pod_pc"]] if x["pod"] == "Care home" else (
            "Usual address" if x["pod"] == "Home" else x["pod_name"])
        done = int(rng.integers(8 * 60 + 15, 17 * 60 + 50))
        opened = max(8 * 60, done - int(rng.integers(30, 400)))
        rec = {"case_id": c["ref"], "created_at": utc(c["completed"], opened),
               "deceased": {"family_name": sur, "given_names": given, "date_of_birth": x["dob"].isoformat(),
                            "sex": x["sex"]},
               "death": {"date": x["dod"].isoformat(), "place_type": POD_S[x["pod"]], "place": pod,
                         "usual_postcode": x["usual_pc"]},
               "scrutiny": {"completed_at": utc(c["completed"], done),
                            "outcome": "mccd" if c["outcome"] == "MCCD" else "referred"},
               "coroner": None}
        if c["cref"]:
            rec["coroner"] = {"reference": c["cref"], "decision": DEC_S[c["decision"]],
                              "decided_on": c["decision_date"].isoformat() if c["decision_date"] else None}
        out.append(rec)
    doc = {"system": "Pathfinder ME Case Manager", "office": "South Ellesmoor Medical Examiner Office",
           "host": "Calderholt and Moorbridge Hospitals NHS Trust", "extracted_at": "2026-10-09T17:05:12Z",
           "case_count": len(out), "cases": out}
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return len(out)


def lookup(T, path):
    rows = []
    for pc, place, intro, term, repl in T.lookup:
        rows.append([pc, W.CODE[place], place, intro.isoformat(), term.isoformat() if term else "", repl])
    write_csv(path, ["postcode", "place_code", "place_name", "date_introduced", "date_terminated", "replaced_by"], rows)


def districts(path):
    rows = [[n, o, c, a + " Ellesmoor"] for n, o, c, a in W.REG_DISTRICTS]
    rows.append(["Kexley", "KEX", "E30000917", "outside Ellesmoor"])
    write_csv(path, ["registration_district", "code_to_2023-04-02", "code_from_2023-04-03", "coroner_area"], rows)


def population(path):
    shares = {"0-17": 0.205, "18-64": 0.590, "65-74": 0.105, "75-84": 0.070, "85+": 0.030}
    old = {"Ashwold": 1.22, "Thornley Vale": 1.08, "Hollinsgate": 0.86}
    rows = []
    for p in W.NAMES:
        tot = W.POP[p]
        k = old.get(p, 1.0)
        raw = {b: s * (k if b in ("65-74", "75-84", "85+") else 1.0) for b, s in shares.items()}
        z = sum(raw.values())
        vals = {b: int(round(tot * v / z)) for b, v in raw.items()}
        vals["18-64"] += tot - sum(vals.values())
        for b in shares:
            rows.append([W.CODE[p], p, b, vals[b]])
    write_csv(path, ["place_code", "place_name", "age_band", "population_mid_2025"], rows)


def temperature(path):
    rng = np.random.default_rng(W.SEED + 11)
    rows = []
    d = dt.date(2026, 6, 1)
    while d <= dt.date(2026, 9, 30):
        doy = d.timetuple().tm_yday
        base = 19.5 + 2.5 * np.sin((doy - 120) / 365.25 * 2 * np.pi)
        if W.HEAT26[0] <= d <= W.HEAT26[1]:
            k = (d - W.HEAT26[0]).days
            base = 27.5 + 6.0 * np.sin(np.pi * (k + 1) / 12)
        for st, off in (("Hollinsgate Weston Park", 0.6), ("Brinmoor Edge", -1.1)):
            rows.append([d.isoformat(), st, "%.1f" % (base + off + rng.normal(0, 1.4))])
        d += dt.timedelta(days=1)
    write_csv(path, ["date", "station", "max_air_temperature_c"], rows)


def alerts(path):
    rows = [["2026-06-23T11:00", "Yellow", "2026-06-24T09:00", "2026-06-26T17:00", "North of England"],
            ["2026-07-10T11:00", "Yellow", "2026-07-12T09:00", "2026-07-14T09:00", "North of England"],
            ["2026-07-12T10:30", "Amber", "2026-07-14T09:00", "2026-07-20T09:00", "North of England"],
            ["2026-07-17T10:00", "Red", "2026-07-18T09:00", "2026-07-21T09:00", "North of England"],
            ["2026-07-20T11:00", "Amber", "2026-07-21T09:00", "2026-07-25T09:00", "North of England"],
            ["2026-08-11T11:00", "Yellow", "2026-08-12T09:00", "2026-08-14T17:00", "North of England"]]
    write_csv(path, ["issued_at", "level", "valid_from", "valid_to", "region"], rows)


def care_homes(T, path):
    """the board's commissioning list of the care homes in its six places"""
    rng = np.random.default_rng(W.SEED + 13)
    names = care_home_name(T, None)
    pc_place = {pc: pl for pc, pl, _, _, _ in T.lookup}
    wb = Workbook()
    ws = wb.active
    ws.title = "Care homes"
    ws.append(["Care home", "Postcode", "Place", "Service", "Registered beds", "Provider type"])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="005EB8")
    for pc in sorted(names, key=lambda k: (pc_place.get(k, ""), names[k])):
        ws.append([names[pc], pc, pc_place.get(pc, ""), "Nursing" if rng.random() < 0.4 else "Residential",
                   int(rng.integers(22, 96)), "Independent" if rng.random() < 0.85 else "Local authority"])
    for col, wdt in zip("ABCDEF", [24, 11, 14, 12, 15, 15]):
        ws.column_dimensions[col].width = wdt
    wb.properties.creator = "Care Market Team"
    wb.properties.lastModifiedBy = "Care Market Team"
    wb.properties.created = dt.datetime(2025, 4, 7, 10, 3, 51)
    wb.properties.modified = dt.datetime(2026, 10, 2, 14, 22, 9)
    wb.save(path)
    PP.normalize_zip(path, modified="2026-10-02T14:22:09Z")


def write_all(T, target):
    os.makedirs(target, exist_ok=True)
    counts = {}
    counts[REG] = registrations(T, os.path.join(target, REG))
    counts[NORTH] = north_log(T, os.path.join(target, NORTH))
    counts[SOUTH] = south_cases(T, os.path.join(target, SOUTH))
    lookup(T, os.path.join(target, LOOKUP))
    districts(os.path.join(target, DISTRICTS))
    population(os.path.join(target, POPULATION))
    temperature(os.path.join(target, TEMPERATURE))
    alerts(os.path.join(target, ALERTS))
    docs.terms(T, os.path.join(target, TERMS))
    care_homes(T, os.path.join(target, CARE))
    return counts
