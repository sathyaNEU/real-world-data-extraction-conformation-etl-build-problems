#!/usr/bin/env python3
"""task464: every file the bundle ships, written in the form the producing system would export it.

No file under target/ describes the pack: each carries its own conventions the way its own system writes
them, and what the plan itself defines sits in the network agreement's capacity terms.
"""
import collections
import csv
import datetime as dt
import json
import os
import re
import zlib
import sqlite3

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import sim
import world

ASOF = world.ASOF
EXTRACT_PULL = dt.date(2027, 1, 5)
RUNOUT_PULL = dt.date(2027, 2, 16)
ROSTER_FROM = dt.date(2026, 10, 1)
FILING_SUBMITTED = dt.date(2026, 3, 31)
FILING_POSITION = dt.date(2026, 1, 1)
PROJECTION_PUBLISHED = dt.date(2027, 1, 15)
AGREEMENT_APPROVED = dt.date(2026, 12, 10)
CYCLES = [(2024, dt.date(2024, 11, 14)), (2025, dt.date(2025, 11, 12)), (2026, dt.date(2026, 11, 18))]
MOVED_ADDRESS = 3           # sites that changed address and kept their plan identifier

ORG = "Wrenlow Community Health Plan"
STAMP = dt.datetime(2027, 2, 16, 10, 30, 0)


def repack(path, stamp=None, company=None):
    """Rewrite a workbook's own archive with one fixed entry date, members in the order the writer put
    them, so two builds of the same pack are byte-identical (reduce-house-fixes H1 and H7)."""
    import zipfile
    stamp = stamp or STAMP
    iso = stamp.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    with zipfile.ZipFile(path) as z:
        members = []
        for i in z.infolist():
            data = z.read(i.filename)
            if i.filename == "docProps/core.xml":
                # the writer stamps its own clock into the modified date; the fiction's date ships
                data = re.sub(rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", iso, data)
            if i.filename == "docProps/app.xml":
                # and its own name and version into the application; a spreadsheet's own pair ships
                data = re.sub(rb"<Application>[^<]*</Application>",
                              b"<Application>Microsoft Excel</Application>", data)
                if b"<AppVersion>" in data:
                    data = re.sub(rb"<AppVersion>[^<]*</AppVersion>",
                                  b"<AppVersion>16.0300</AppVersion>", data)
                else:
                    data = data.replace(b"</Properties>",
                                        b"<AppVersion>16.0300</AppVersion></Properties>")
                if company and b"<Company>" not in data:
                    data = data.replace(b"</Properties>",
                                        b"<Company>" + company.encode("utf-8") +
                                        b"</Company></Properties>")
            members.append((i, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for info, data in members:
            zi = zipfile.ZipInfo(info.filename, date_time=(stamp.year, stamp.month, stamp.day,
                                                           stamp.hour, stamp.minute, stamp.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            z.writestr(zi, data)
    return path


def save_book(wb, path, creator=None, title=None):
    finalise(wb, creator, title)
    wb.save(path)
    return repack(path, company=creator or ORG)


def finalise(wb, creator=None, title=None):
    """One stamp for every workbook: the producer and the dates are the fiction's, so two builds of the
    same pack are byte-identical and no writer name ships (reduce-house-fixes H1)."""
    p = wb.properties
    p.creator = creator or ORG
    p.lastModifiedBy = creator or ORG
    p.created = STAMP
    p.modified = STAMP
    p.title = title
    p.subject = None
    p.description = None
    p.keywords = None
    p.category = None
    p.lastPrinted = None
    p.revision = None
    p.version = None
    return wb

GROUP_PRACTICE = 3          # sites billing under one tax identifier


def _w(path, rows, header):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)


def _dst(d):
    """United States central time: standard from the first Sunday of November, daylight from the second
    Sunday of March."""
    y = d.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return "-05:00" if mar <= d < nov else "-06:00"


def _hhmm(minutes):
    return "%02d:%02d" % (minutes // 60, minutes % 60)


# ------------------------------------------------------------------- 1 the provider directory
def directory(target, sites, extra, rnd):
    rows = []
    taxes = {}
    group = sorted(sites, key=lambda s: s["seq"])[:GROUP_PRACTICE]
    group_tax = "47-2210388"
    for s in sites:
        taxes[s["site"]] = group_tax if s in group else "%02d-%07d" % (20 + s["seq"] % 60,
                                                                       1100000 + s["seq"] * 1511)
    movers = sorted(sites, key=lambda s: -s["seq"])[:MOVED_ADDRESS]
    for cycle, attested_on in CYCLES:
        for s in sites:
            stations = s["attested"]
            if cycle < 2026 and s["gap"] and s["seq"] % 4 == 0:
                stations = s["attested"] - 1          # a chair added since the earlier cycle
            addr = s["address"]
            if s in movers and cycle < 2026:
                addr = addr.replace(addr.split(",")[0], str(int(addr.split(" ")[0]) + 118) + " " +
                                    " ".join(addr.split(",")[0].split(" ")[1:]))
            rows.append([cycle, attested_on.isoformat(), s["site"], s["name"], s["operator"], addr,
                         s["locality"], s["area"], world.AREA[s["area"]]["name"],
                         "in-centre haemodialysis" if s["modality"] == "dialysis" else "ambulatory infusion",
                         stations, taxes[s["site"]],
                         "contract" if cycle == 2026 else ""])
        for e in extra:
            if e["kind"] != "dropped":
                continue
            rows.append([cycle, attested_on.isoformat(), e["site"], e["name"], e["operator"], e["address"],
                         e["locality"], e["area"], world.AREA[e["area"]]["name"],
                         "in-centre haemodialysis" if e["modality"] == "dialysis" else "ambulatory infusion",
                         e["licensed"], "%02d-%07d" % (20 + e["seq"] % 60, 1100000 + e["seq"] * 1511),
                         "none" if cycle == 2026 else ""])
    _w(os.path.join(target, "provider_directory_2027.csv"), rows,
       ["attestation_cycle", "attested_on", "plan_site_id", "site_name", "operator", "service_address",
        "locality", "service_area_code", "service_area_name", "service_category", "attested_stations",
        "tax_id", "contract_intent_2027"])
    return rows, taxes


# ------------------------------------------------------------------- 2 the state licence register
def licence_register(target, sites, extra, rnd):
    oprnd = __import__("random").Random(5519)     # the operator market, off every other stream
    facilities, amendments, reissues = [], [], []
    def num(seq, mod):
        return "%s-%05d" % ("ESRD" if mod == "dialysis" else "AIT", 21000 + seq * 23)
    for s in sites:
        s["licence_no"] = num(s["seq"], s["modality"])
    for e in extra:
        e["licence_no"] = num(e["seq"], e["modality"])
    allf = [(s, s["licensed"], s["modality"], s["area"], s["address"], s["locality"], s["operator"],
             s["licence_no"]) for s in sites]
    allf += [(e, e["licensed"], e["modality"], e["area"], e["address"], e["locality"], e["operator"],
              e["licence_no"]) for e in extra]
    rows = []
    for i, (obj, st, mod, area, addr, loc, op, lic) in enumerate(allf):
        cat = "in-centre haemodialysis" if mod == "dialysis" else "ambulatory infusion"
        eff = dt.date(2015 + (i % 9), 1 + (i * 5) % 12, 1 + (i * 7) % 27)
        # a superseded amendment row for about a third of the facilities: the station count before a change
        if i % 3 == 0:
            amend_to = dt.date(2024, 1 + (i * 3) % 11, 2 + (i * 11) % 26)
            rows.append([lic, op, "facility", addr, loc, area, cat, max(2, st - 2),
                         eff.isoformat(), amend_to.isoformat(), "amended"])
            eff = amend_to
            amendments.append(lic)
        rows.append([lic, op, "facility", addr, loc, area, cat, st, eff.isoformat(), "", "active"])
    # three licences of sites the plan is not contracting lapse during 2026 and the number is reissued
    # to a new facility later in the year, so the row covering an earlier position date is not the row
    # covering the as-of date
    lapsed = [o for o in allf if o[0].get("kind") == "dropped"][:3]
    for i, (obj, st, mod, area, addr, loc, op, lic) in enumerate(lapsed):
        new_op = world.draw_operator("dialysis" if i % 2 == 0 else "infusion", oprnd)
        new_loc = world.LOCALITIES[world.CODES[(i * 4 + 1) % 12]][0]
        new_addr = "%d %s, %s" % (300 + i * 23, world.STREETS[(i * 9) % len(world.STREETS)], new_loc)
        for r in rows:
            if r[0] == lic and r[10] == "active":
                r[9] = dt.date(2026, 5 + i, 27 + i).isoformat()
                r[10] = "lapsed"
        rows.append([lic, new_op, "facility", new_addr, new_loc, world.CODES[(i * 4 + 1) % 12],
                     "in-centre haemodialysis" if i % 2 == 0 else "ambulatory infusion",
                     5 + i * 2, dt.date(2026, 8 + i, 14).isoformat(), "", "active"])
        reissues.append(lic)
        obj["licence_reissued"] = True
    # five licence numbers reissued to another operator at another address after a lapse
    for i, (obj, st, mod, area, addr, loc, op, lic) in enumerate(allf):
        if obj.get("kind") == "off_plan" and len(reissues) < 8:
            old_op = world.draw_operator(mod, oprnd)
            old_addr = "%d %s, %s" % (200 + i * 17, world.STREETS[(i * 13) % len(world.STREETS)], loc)
            rows.append([lic, old_op, "facility", old_addr, loc, area,
                         "in-centre haemodialysis" if mod == "dialysis" else "ambulatory infusion",
                         max(2, st - 3), dt.date(2012 + i % 5, 3, 14).isoformat(),
                         dt.date(2019 + i % 4, 6, 30).isoformat(), "lapsed"])
            reissues.append(lic)
    # the corporate umbrella rows: one per chain operator per area, carrying the sum of its facilities
    byop = collections.defaultdict(lambda: collections.defaultdict(int))
    for obj, st, mod, area, addr, loc, op, lic in allf:
        if world.OPERATOR_KIND.get(op) == "chain":
            byop[op][area] += st
    for op in sorted(byop):
        for area in sorted(byop[op]):
            rows.append(["CORP-%05d" % (9000 + zlib.crc32((op + area).encode()) % 900), op, "corporate umbrella", "",
                         "", area, "multi-category", byop[op][area],
                         dt.date(2016, 4, 1).isoformat(), "", "active"])
    # eight facilities licensed outside the plan's twelve service areas
    for i in range(8):
        rows.append(["ESRD-%05d" % (31000 + i * 19), world.draw_operator("dialysis", oprnd),
                     "facility", "%d Marchford Road, Tarnsby" % (40 + i * 13), "Tarnsby", "OUT-OF-AREA",
                     "in-centre haemodialysis", 6 + i % 7, dt.date(2018 + i % 6, 2, 9).isoformat(), "",
                     "active"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Licences"
    head = ["licence_no", "licence_holder", "holder_type", "service_address", "locality", "county_or_area",
            "service_category", "licensed_stations", "effective_from", "effective_to", "licence_status"]
    ws.append(head)
    for r in rows:
        ws.append(r)
    ws.freeze_panes = "A2"
    for i, h in enumerate(head, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, min(34, len(h) + 6))
        ws.cell(row=1, column=i).font = Font(bold=True)
    s2 = wb.create_sheet("Register Summary")
    s2.append(["Outpatient Facility Licensing Register", ""])
    s2.append(["position as at", ASOF.isoformat()])
    s2.append([])
    s2.append(["service_category", "licence_numbers_on_register"])
    cnt = collections.Counter(r[6] for r in rows)
    for k in sorted(cnt):
        s2.append([k, cnt[k]])
    s2.append(["all categories", len(set(r[0] for r in rows))])
    for i, w in enumerate((34, 26), start=1):
        s2.column_dimensions[get_column_letter(i)].width = w
    save_book(wb, os.path.join(target, "state_licence_register.xlsx"),
              "State licensing authority", "Outpatient Facility Licensing Register")
    return rows, reissues, amendments


# ------------------------------------------------------------------- 3 the staffing roster
def roster(target, sites):
    rows = []
    for s in sites:
        rows.append([ROSTER_FROM.isoformat(), s["site"], s["name"], s["days"], s["shifts"],
                     s["sessions"], int(round(s["sessions"] * 4.33 * (6.5 if s["modality"] == "dialysis"
                                                                       else 5.0)))])
    _w(os.path.join(target, "staffing_roster_2026q4.csv"), rows,
       ["effective_from", "plan_site_id", "site_name", "days_open_week", "shifts_per_day",
        "treatment_sessions_week", "clinical_hours_month"])
    return rows


# ------------------------------------------------------------------- 4 the timed encounter extract
def encounters_db(target, sites, rows, cancels):
    path = os.path.join(target, "treatment_encounters.db")
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("PRAGMA page_size=4096")
    cur.execute("""CREATE TABLE encounters_2023_2024 (
        encounter_id TEXT, service_facility_id TEXT, member_id TEXT, service_date TEXT,
        service_start TEXT, service_stop TEXT, encounter_status TEXT, service_category TEXT)""")
    cur.execute("""CREATE TABLE encounters_2025_2026 (
        encounter_id TEXT, service_facility_id TEXT, member_id TEXT, service_date TEXT,
        service_start TEXT, service_minutes INTEGER, encounter_status TEXT, service_category TEXT)""")
    cat = {s["site"]: ("HD" if s["modality"] == "dialysis" else "AIT") for s in sites}
    a, b, n = [], [], 0
    allrows = sorted(rows + cancels, key=lambda r: (r["date"], r["site"], r["start"]))
    for r in allrows:
        n += 1
        eid = "E%d%08d" % (r["date"].year, n)
        st = r.get("status", sim.STATUS_COMPLETED)
        if r["date"].year <= 2024:
            start = "%s %s" % (r["date"].isoformat(), _hhmm(r["start"] % 1440))
            if r["dur"] is None:
                stop = ""
            else:
                end = r["start"] + r["dur"]
                stop = "%s %s" % ((r["date"] + dt.timedelta(days=end // 1440)).isoformat(),
                                  _hhmm(end % 1440))
            a.append((eid, r["site"], r["member"], r["date"].isoformat(), start, stop, st, cat[r["site"]]))
        else:
            start = "%sT%s:00%s" % (r["date"].isoformat(), _hhmm(r["start"] % 1440), _dst(r["date"]))
            b.append((eid, r["site"], r["member"], r["date"].isoformat(), start, r["dur"], st,
                      cat[r["site"]]))
    cur.executemany("INSERT INTO encounters_2023_2024 VALUES (?,?,?,?,?,?,?,?)", a)
    cur.executemany("INSERT INTO encounters_2025_2026 VALUES (?,?,?,?,?,?,?,?)", b)
    con.commit()
    cur.execute("VACUUM")
    con.commit()
    con.close()
    return len(a), len(b)


# ------------------------------------------------------------------- 5 the enrolment projection
def projection(target, by_area):
    rows = []
    for c in world.CODES:
        a = world.AREA[c]
        base = 1800 + (int(a["growth"] * 1000) % 7) * 310 + len(by_area[c]) * 540
        rows.append([PROJECTION_PUBLISHED.isoformat(), c, a["name"], base,
                     int(round(base * a["growth"])), "%.3f" % a["growth"]])
    _w(os.path.join(target, "enrolment_projection_2027.csv"), rows,
       ["published_on", "service_area_code", "service_area_name", "members_2026",
        "projected_members_2027", "projected_growth_factor"])
    return rows


# ------------------------------------------------------------------- 7 the 2026 state filing
def filing(target, sites, extra, rnd):
    rows = []
    for s in sites:
        if not s["in_2026_filing"]:
            continue
        rows.append([s["licence_no"], s["name"], s["address"], s["locality"], s["area_2026"],
                     world.AREA[s["area_2026"]]["name"],
                     "in-centre haemodialysis" if s["modality"] == "dialysis" else "ambulatory infusion",
                     s["licensed"], "contracted"])
    for e in extra:
        if e["kind"] != "dropped":
            continue
        rows.append([e["licence_no"], e["name"], e["address"], e["locality"], e["area_2026"],
                     world.AREA[e["area_2026"]]["name"],
                     "in-centre haemodialysis" if e["modality"] == "dialysis" else "ambulatory infusion",
                     e["licensed"], "contracted"])
    dup = [e for e in extra if e["kind"] == "dropped"][4:9]
    for e in dup:
        rows.append(["CORP-%05d" % (9000 + zlib.crc32((e["operator"] + e["area"]).encode()) % 900), e["name"],
                     e["address"], e["locality"], e["area_2026"], world.AREA[e["area_2026"]]["name"],
                     "in-centre haemodialysis" if e["modality"] == "dialysis" else "ambulatory infusion",
                     e["licensed"], "contracted"])
        e["filed_twice"] = True
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contracted Sites"
    head = ["licence_no", "site_name", "service_address", "locality", "service_area_code",
            "service_area_name", "service_category", "licensed_stations", "network_status"]
    ws.append(head)
    for r in rows:
        ws.append(r)
    ws.freeze_panes = "A2"
    for i, h in enumerate(head, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, min(36, len(h) + 8))
        ws.cell(row=1, column=i).font = Font(bold=True)
    s2 = wb.create_sheet("Area Summary")
    s2.append(["Annual Network Adequacy Filing, 2026 network year"])
    s2.append(["position as at", FILING_POSITION.isoformat()])
    s2.append(["submitted", FILING_SUBMITTED.isoformat()])
    s2.append([])
    s2.append(["service_area_code", "service_area_name", "contracted_sites", "licensed_stations",
               "treatments_delivered_2025"])
    agg = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        agg[r[4]][0] += 1
        agg[r[4]][1] += r[7]
    for c in world.CODES:
        v = agg.get(c, [0, 0])
        s2.append([c, world.AREA[c]["name"], v[0], v[1],
                   int(round(v[1] * 46.0 * (1.0 + (ord(c[-1]) % 7) / 40.0)))])
    for i, w in enumerate((22, 24, 18, 20, 26), start=1):
        s2.column_dimensions[get_column_letter(i)].width = w
    save_book(wb, os.path.join(target, "state_adequacy_filing_2026.xlsx"), None,
              "Annual Network Adequacy Filing, 2026 network year")
    return rows


# ------------------------------------- 8, 9, 10 the out-of-network register, its run-out and its control
def out_of_network(target, sites, extra, rows_in, rnd):
    dropped = [e for e in extra if e["kind"] == "dropped"]
    areas = world.CODES
    main, runout, n = [], [], 0
    for e in dropped:
        weekly = max(5, e["weekly"] // 7)
        start = dt.date(2025, 10, 6)
        while start <= dt.date(2026, 12, 28):
            for k in range(weekly):
                n += 1
                sd = start + dt.timedelta(days=(k * 3) % 6)
                if sd > dt.date(2026, 12, 31):
                    continue
                lag = 24 + (n * 7) % 48
                adj = sd + dt.timedelta(days=lag)
                mem = "M%09d" % (500000000 + (n * 3571) % 900000)
                # the register carries the member's own residence area, not the area of the site treated
                res = areas[(n * 5) % 12] if n % 8 == 0 else e["area"]
                amt = 268.0 + (n % 37) * 4.5
                cid = "C%d%07d" % (sd.year, n)
                rows_for_claim = [[cid, 1, mem, sd.isoformat(), e["name"], e["address"],
                                   e["licence_no"], res, "%.2f" % amt, adj.isoformat(),
                                   "%d-Q%d" % (adj.year, (adj.month - 1) // 3 + 1), 1]]
                if n % 6 == 0:
                    rows_for_claim.insert(0, [cid, 0, mem, sd.isoformat(), e["name"], e["address"],
                                              e["licence_no"], res, "%.2f" % amt, adj.isoformat(),
                                              "%d-Q%d" % (adj.year, (adj.month - 1) // 3 + 1), 1])
                for row in rows_for_claim:
                    if adj.year == 2026:
                        main.append(row)
                    elif adj.year == 2027 and adj <= RUNOUT_PULL:
                        runout.append(row)
            start += dt.timedelta(days=7)
    head = ["claim_id", "line_no", "member_id", "service_date", "service_facility_name",
            "service_facility_address", "licence_no", "member_residence_area", "paid_amount",
            "adjudicated_date", "adjudication_quarter", "treatment_units"]
    _w(os.path.join(target, "out_of_network_payments_2026.csv"), main, head)
    _w(os.path.join(target, "out_of_network_payments_runout_2027q1.csv"), runout, head)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Adjudicated Quarters"
    ws.append(["Out-of-network outpatient dialysis and infusion payments"])
    ws.append(["extract pulled", dt.date(2027, 1, 9).isoformat()])
    ws.append([])
    ws.append(["adjudication_quarter", "claim_lines", "treatment_units", "paid_amount"])
    agg = collections.defaultdict(lambda: [0, 0, 0.0])
    for r in main:
        q = agg[r[10]]
        q[0] += 1
        q[1] += r[11]
        q[2] += float(r[8])
    for q in sorted(agg):
        ws.append([q, agg[q][0], agg[q][1], round(agg[q][2], 2)])
    ws.append(["total", sum(v[0] for v in agg.values()), sum(v[1] for v in agg.values()),
               round(sum(v[2] for v in agg.values()), 2)])
    for i, w in enumerate((24, 14, 16, 16), start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for r in ws.iter_rows(min_row=4, max_row=4):
        for c in r:
            c.font = Font(bold=True)
    save_book(wb, os.path.join(target, "out_of_network_payments_reconciliation_2026.xlsx"), None,
              "Out-of-network outpatient dialysis and infusion payments, adjudicated quarters")
    return main, runout


# ------------------------------------------------------------------- 11 the extract transmittal
def transmittal(target, na, nb, rows, cancels):
    q = collections.Counter()
    for r in rows + cancels:
        q["%d-Q%d" % (r["date"].year, (r["date"].month - 1) // 3 + 1)] += 1
    doc = {
        "extract": "outpatient treatment encounters",
        "pulled_on": EXTRACT_PULL.isoformat(),
        "covers": {"from": world.REC_START.isoformat(), "to": "2026-12-31"},
        "tables": {"encounters_2023_2024": na, "encounters_2025_2026": nb},
        "rows_by_service_quarter": {k: q[k] for k in sorted(q)},
        "timestamp_convention": {
            "encounters_2023_2024": "service_start and service_stop in site local clock",
            "encounters_2025_2026": "service_start with offset from coordinated universal time"},
    }
    with open(os.path.join(target, "encounter_extract_transmittal.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, sort_keys=False)
        f.write("\n")
    return doc


# ------------------------------------------------------------------- 12 the transport file (distractor)
def nemt(target, by_area, rnd):
    rows = []
    modes = ["ambulatory", "wheelchair", "stretcher"]
    for c in world.CODES:
        for m in range(1, 13):
            for i, mode in enumerate(modes):
                base = 140 + (ord(c[-1]) * 17 + m * 11 + i * 29) % 260
                rows.append([c, world.AREA[c]["name"], "2026-%02d" % m, mode, base,
                             "%.2f" % (base * (21.4 + i * 9.3))])
    _w(os.path.join(target, "nemt_trips_2026.csv"), rows,
       ["service_area_code", "service_area_name", "service_month", "trip_mode", "trips", "paid_amount"])
    return rows
