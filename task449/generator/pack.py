"""Writes the main-call files of the target/ pack from the world truth (board snapshots, activity logs, employer
services cases, employer accounts, jobseeker counts, concordance). Documents and survey tables: docs.py.
Ask files: asks_world.py.
"""
import datetime as dt
import math
import os

import numpy as np

import common as C
import params as P
import world as W

TITLES = {
    "31301": ["Registered Nurse", "RN - Medicine", "Registered Nurse (Casual)", "RN, Long-Term Care", "Registered Psychiatric Nurse"],
    "32101": ["Licensed Practical Nurse", "LPN", "Licensed Practical Nurse - Days", "LPN (Part-time)"],
    "33102": ["Health Care Aide", "Nurse Aide", "Personal Care Aide", "Patient Care Attendant", "HCA - Nights"],
    "44101": ["Home Support Worker", "Caregiver", "Personal Support Worker", "Home Care Aide", "Respite Worker"],
    "42202": ["Early Childhood Educator", "ECE Assistant", "Early Childhood Educator Level II", "Child Care Worker"],
    "62200": ["Chef", "Sous Chef", "Chef de Partie", "Executive Chef", "Kitchen Manager / Chef"],
    "63200": ["Cook", "Line Cook", "Prep Cook", "Breakfast Cook", "Cook II"],
    "65201": ["Kitchen Helper", "Dishwasher", "Food Counter Attendant", "Prep / Dish", "Kitchen Porter"],
    "65200": ["Server", "Food and Beverage Server", "Banquet Server", "Bartender / Server"],
    "62020": ["Food Service Supervisor", "Shift Supervisor - Restaurant", "Cafeteria Supervisor"],
    "72200": ["Electrician", "Journeyperson Electrician", "Construction Electrician", "Electrician (Residential)"],
    "72310": ["Carpenter", "Framer", "Finish Carpenter", "Journeyperson Carpenter"],
    "72300": ["Plumber", "Journeyperson Plumber", "Service Plumber"],
    "75110": ["Construction Labourer", "General Labourer - Construction", "Site Labourer", "Labourer"],
    "73400": ["Heavy Equipment Operator", "Excavator Operator", "Loader Operator", "Grader Operator"],
    "64100": ["Retail Sales Associate", "Sales Associate", "Retail Associate", "Visual Merchandiser"],
    "65100": ["Cashier", "Front End Cashier", "Cashier (Part-time)"],
    "65102": ["Stock Clerk", "Order Picker", "Shelf Stocker", "Grocery Clerk - Night Crew"],
    "73300": ["Class 1 Driver", "Truck Driver (AZ)", "Long Haul Driver", "Class 3 Driver", "Transport Driver"],
    "75101": ["Warehouse Worker", "Material Handler", "Shipper / Receiver Helper", "Forklift Operator"],
    "94141": ["Meat Cutter", "Industrial Butcher", "Poultry Processor", "Deboner"],
    "95106": ["Production Worker", "Food Processing Labourer", "Packaging Line Worker", "Plant Labourer"],
    "72400": ["Millwright", "Industrial Mechanic", "Maintenance Millwright", "Industrial Mechanic (Millwright)"],
    "72106": ["Welder", "MIG Welder", "Welder / Fabricator", "Welder - B Pressure"],
    "21232": ["Software Developer", "Programmer Analyst", "Full Stack Developer", "Software Developer II"],
    "13110": ["Administrative Assistant", "Office Administrator", "Executive Assistant", "Administrative Assistant - Clinic"],
    "65310": ["Cleaner", "Housekeeper", "Room Attendant", "Light Duty Cleaner"],
    "41221": ["Elementary Teacher", "Kindergarten Teacher", "Teacher - Grade 3", "French Immersion Teacher"],
    "85101": ["Harvest Worker", "Farm Labourer - Harvest", "Fruit Picker", "Vegetable Harvester"],
    "72410": ["Automotive Service Technician", "Heavy Duty Mechanic", "Auto Technician", "Truck and Coach Technician"],
}


def title_for(code, rng):
    t = TITLES.get(code)
    if t is None:
        return None
    return t[int(rng.integers(len(t)))]


def occ_maps():
    t21, c16, prof = {}, {}, {}
    for o in P.OCCUPATIONS:
        t21[o[0]] = o[1]
        c16[o[0]] = o[2]
        prof[o[0]] = o[7]
    for o in P.OTHER_OCCUPATIONS:
        t21[o[0]] = o[1]
        c16[o[0]] = o[2]
        prof[o[0]] = o[7]
    return t21, c16, prof


def build_postings(emps, vac, rng):
    """Posting records for every posted vacancy: numbers on each platform, times of each event."""
    mig = W.d2i(P.MIGRATION)
    ext = W.d2i(P.EXTRACT)
    t21, c16, _ = occ_maps()
    posts = []
    used_old, used_new = set(), set()
    order = sorted((i for i, v in enumerate(vac) if v["posted"]), key=lambda i: (vac[i]["start"], i))
    for i in order:
        v = vac[i]
        if v["start"] > ext:
            continue
        p = dict(v)
        p["vid"] = i
        p["employer_no"] = emps[v["emp"]]["employer_no"]
        p["noc16"] = c16[v["occ"]]
        p["title"] = title_for(v["occ"], rng) or t21[v["occ"]].split(",")[0].split(" (")[0]
        p["pub_minute"] = int(rng.integers(7 * 60 + 30, 18 * 60))
        p["end_minute"] = 5 if p["end_kind"] == "EXPIRED" else int(rng.integers(8 * 60, 19 * 60))
        p["ren_minutes"] = [int(rng.integers(8 * 60, 21 * 60)) for _ in p["renewals"]]
        p["ren_lead"] = [int(rng.integers(0, 3)) for _ in p["renewals"]]
        if v["start"] < mig:
            while True:
                n = "WS%02d%05d" % (W.i2d(v["start"]).year % 100, int(rng.integers(0, 100000)))
                if n not in used_old:
                    used_old.add(n)
                    break
            p["old_no"] = n
        else:
            p["old_no"] = None
        # migrated: live at the end of the day before go-live (still on the board when the old platform closed)
        p["migrated"] = bool(v["start"] <= mig - 1 < p["listing_end"])
        if v["start"] >= mig or p["migrated"]:
            while True:
                n = "J-%07d" % int(rng.integers(1000000, 9999999))
                if n not in used_new:
                    used_new.add(n)
                    break
            p["new_id"] = n
        else:
            p["new_id"] = None
        posts.append(p)
    return posts


def ts_local(day, minute):
    d = W.i2d(day)
    return "%s %02d:%02d" % (d.isoformat(), minute // 60, minute % 60)


def utc_offset_hours(d):
    """Laurentide keeps Eastern time: UTC-4 from the second Sunday of March to the first Sunday of November."""
    y = d.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return 4 if mar <= d < nov else 5


def ts_utc(day, minute):
    d = W.i2d(day)
    off = utc_offset_hours(d)
    t = dt.datetime(d.year, d.month, d.day, minute // 60, minute % 60) + dt.timedelta(hours=off)
    return t.strftime("%Y-%m-%dT%H:%M:00Z")


def write_snapshots(posts, emps, tgt):
    mig = W.d2i(P.MIGRATION)
    old_rows, new_rows = [], []
    for sd in P.SNAP_DATES:
        d = W.d2i(sd)
        live = [p for p in posts if p["start"] <= d < p["listing_end"]]
        live.sort(key=lambda p: (p["start"], p["old_no"] or "", p["new_id"] or ""))
        for p in live:
            if p["channel"] == "S":
                k = (d - p["start"]) // P.TERM_DAYS
                term_last = p["start"] + P.TERM_DAYS * (k + 1) - 1
            else:
                term_last = None
            if d < mig:
                old_rows.append([sd.isoformat(), p["old_no"], p["employer_no"], p["noc16"], p["title"], p["positions"],
                                 W.i2d(p["start"]).strftime("%d/%m/%Y"), "SS" if p["channel"] == "S" else "ES",
                                 W.i2d(term_last).strftime("%d/%m/%Y") if term_last is not None else ""])
            else:
                new_rows.append([sd.isoformat(), p["new_id"], p["old_no"] if p["migrated"] else "", p["employer_no"],
                                 p["occ"], p["title"], p["positions"], W.i2d(p["start"]).isoformat(),
                                 "Self-service" if p["channel"] == "S" else "Employer Services",
                                 W.i2d(term_last).isoformat() if term_last is not None else ""])
    C.write_csv(os.path.join(tgt, "workshore_live_postings_2025-07_2026-01.csv"),
                ["snapshot_date", "posting_no", "employer_no", "noc_2016", "job_title", "positions", "date_posted",
                 "channel", "expiry_date"], old_rows)
    C.write_csv(os.path.join(tgt, "workshore_live_postings_2026-02_2026-09.csv"),
                ["extract_date", "job_id", "legacy_ref", "employer_number", "noc_2021", "title", "openings",
                 "posted_on", "source", "term_end"], new_rows, crlf=False)
    return len(old_rows), len(new_rows)


def write_activity(posts, tgt):
    mig = W.d2i(P.MIGRATION)
    a0 = W.d2i(P.ACTIVITY_FROM)
    ext = W.d2i(P.EXTRACT)
    old_ev, new_ev = [], []
    for p in posts:
        evs = []
        evs.append((p["start"], p["pub_minute"], "PUBLISHED"))
        for r, m, u in zip(p["renewals"], p["ren_minutes"], p["ren_lead"]):
            evs.append((r - 1 - u, m, "RENEWED"))      # renewed in the term's last days; the new term starts at r
        if p["listing_end"] <= ext:
            kind = {"REMOVED": "REMOVED", "EXPIRED": "EXPIRED", "CLOSED": "CLOSED_ES"}[p["end_kind"]]
            evs.append((p["listing_end"], p["end_minute"], kind))
        for day, minute, kind in evs:
            if day < a0 or day > ext:
                continue
            if day < mig:
                old_ev.append((day, minute, p["old_no"], kind, p["employer_no"],
                               p["noc16"] if kind == "PUBLISHED" else "", ("SS" if p["channel"] == "S" else "ES") if kind == "PUBLISHED" else "",
                               p["positions"] if kind == "PUBLISHED" else ""))
            else:
                if p["new_id"] is None:
                    continue
                new_ev.append((day, minute, p["new_id"], kind, p["employer_no"], p["old_no"] if p["migrated"] else None, p))
        if p["migrated"]:
            new_ev.append((mig, 2, p["new_id"], "MIGRATED", p["employer_no"], p["old_no"], p))
    old_ev.sort(key=lambda e: (e[0], e[1], e[2]))
    new_ev.sort(key=lambda e: (e[0], e[1], e[2], e[3]))
    old_code = {"PUBLISHED": "PUBLISHED", "RENEWED": "RENEWED", "REMOVED": "REMOVED_BY_EMPLOYER",
                "EXPIRED": "EXPIRED", "CLOSED_ES": "CLOSED_ES"}
    C.write_csv(os.path.join(tgt, "workshore_board_events_2025-10-01_2026-02-01.csv"),
                ["event_time", "posting_no", "event", "employer_no", "noc_2016", "channel", "positions"],
                [[ts_local(d, m), n, old_code[k], e, noc, ch, ps] for d, m, n, k, e, noc, ch, ps in old_ev])
    new_code = {"PUBLISHED": "posted", "RENEWED": "renewed", "REMOVED": "taken_down_by_employer",
                "EXPIRED": "expired", "CLOSED_ES": "closed_by_employer_services", "MIGRATED": "migrated"}
    recs = []
    for d, m, n, k, e, leg, p in new_ev:
        r = {"ts": ts_utc(d, m), "job_id": n, "type": new_code[k], "employer": e}
        if k in ("PUBLISHED", "MIGRATED"):
            r["noc"] = p["occ"]
            r["openings"] = p["positions"]
            r["source"] = "self_service" if p["channel"] == "S" else "employer_services"
        if k == "MIGRATED":
            r["legacy_ref"] = leg
        recs.append(r)
    C.write_jsonl(os.path.join(tgt, "workshore_board_events_2026-02-02_2026-11-14.jsonl"), recs)
    return len(old_ev), len(recs)


def write_cases(posts, emps, rng, tgt):
    """Employer Services' own case workbook: every managed vacancy open at any time from 1 April 2025."""
    import openpyxl
    from openpyxl.styles import Font
    lo = W.d2i(dt.date(2025, 4, 1))
    ext = W.d2i(P.EXTRACT)
    mig = W.d2i(P.MIGRATION)
    rows = []
    used = set()
    for p in posts:
        if p["channel"] != "E":
            continue
        if p["listing_end"] < lo or p["start"] > ext:
            continue
        opened = p["start"] - (1 if rng.random() < 0.15 else 0)
        while True:
            cn = "ES-%06d" % int(rng.integers(100000, 999999))
            if cn not in used:
                used.add(cn)
                break
        ref = p["old_no"] if p["start"] < mig else p["new_id"]
        if p["listing_end"] <= ext:
            if p["withdrawn"]:
                outcome = "Withdrawn by employer"
            else:
                outcome = "Filled - Workshore referral" if rng.random() < 0.31 else "Filled - other source"
            odate = W.i2d(p["listing_end"])
        else:
            outcome, odate = "Open", None
        rows.append((opened, cn, ref, p["employer_no"], p["occ"], p["positions"], outcome, odate, p))
    rows.sort(key=lambda r: (r[0], r[1]))
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    fy = {"FY 2025-26": (dt.date(2025, 4, 1), dt.date(2026, 3, 31)), "FY 2026-27": (dt.date(2026, 4, 1), dt.date(2027, 3, 31))}
    for sheet, (a, b) in fy.items():
        ws = wb.create_sheet(sheet)
        ws.append(["Workshore Employer Services - vacancy cases opened %s" % sheet.replace("FY ", "in fiscal year ")])
        ws["A1"].font = Font(bold=True)
        ws.append(["Run %s, case management system" % P.EXTRACT.strftime("%d %b %Y")])
        ws.append([])
        ws.append(["Case no.", "Job ref.", "Employer no.", "NOC", "Openings", "Case opened", "Outcome", "Outcome date"])
        for c in ws[4]:
            c.font = Font(bold=True)
        rix = 4
        for opened, cn, ref, en, occ, npos, outc, od, p in rows:
            od_open = W.i2d(opened)
            if not (a <= od_open <= b):
                continue
            ws.append([cn, ref, en, occ, npos, od_open, outc, od])
            rix += 1
            ws.cell(row=rix, column=6).number_format = "yyyy-mm-dd"
            if od is not None:
                ws.cell(row=rix, column=8).number_format = "yyyy-mm-dd"
        ws.column_dimensions["A"].width = 12
        ws.column_dimensions["B"].width = 12
        ws.column_dimensions["G"].width = 28
    # cases opened before 1 April 2025 that were still open then go on the first sheet's foot as carried cases
    C.save_workbook(wb, os.path.join(tgt, "employer_services_vacancy_cases.xlsx"),
                    dt.datetime(2026, 11, 14, 8, 0), "Workshore Employer Services")
    return len(rows)


def write_employers(emps, rng, tgt):
    rows = []
    for e in sorted(emps, key=lambda e: e["employer_no"]):
        opened = W.i2d(int(rng.integers(-3000, W.d2i(dt.date(2025, 6, 1)))))
        status = "Active"
        rows.append([e["employer_no"], e["legal_name"], e["operating_name"], e["naics"], e["bn9"],
                     opened.isoformat(), status])
    C.write_csv(os.path.join(tgt, "workshore_employer_accounts.csv"),
                ["employer_number", "legal_name", "operating_name", "naics_2017", "business_number", "account_opened",
                 "status"], rows)
    return len(rows)


def jobseeker_counts(rng):
    """Registered jobseekers by primary sought occupation at each snapshot month-end (Schedule A)."""
    out = {}
    for o in P.OCCUPATIONS:
        code, prof, base = o[0], o[7], o[8]
        for sd in P.SNAP_DATES:
            f = P.JS_SEASONAL[prof][sd.month - 1]
            out[(code, sd)] = int(round(base * P.SCALE * f * (1.0 + rng.normal(0.0, 0.018))))
    return out


def write_jobseekers(js, rng, tgt):
    t21, _, _ = occ_maps()
    rows = []
    revised_month = dt.date(2026, 6, 30)
    for sd in P.SNAP_DATES:
        for o in P.OCCUPATIONS:
            code = o[0]
            n = js[(code, sd)]
            if sd == revised_month:
                # the June extract was first run before the month's last check-ins were posted, then re-issued
                first = int(round(n * (1.0 + rng.uniform(0.012, 0.035))))
                rows.append([sd.isoformat(), code, t21[code], first, "2026-07-03"])
                rows.append([sd.isoformat(), code, t21[code], n, "2026-07-21"])
            else:
                rows.append([sd.isoformat(), code, t21[code], n, (sd + dt.timedelta(days=3)).isoformat()])
    C.write_csv(os.path.join(tgt, "workshore_registered_jobseekers_schedule_a.csv"),
                ["month_end", "noc_2021", "occupation", "registered_jobseekers", "run_date"], rows)
    return len(rows)


def write_concordance(tgt):
    t21, c16, _ = occ_maps()
    titles16 = {
        "3012": "Registered nurses and registered psychiatric nurses", "3233": "Licensed practical nurses",
        "3413": "Nurse aides, orderlies and patient service associates", "4412": "Home support workers, housekeepers and related occupations",
        "4214": "Early childhood educators and assistants", "6321": "Chefs", "6322": "Cooks",
        "6711": "Food counter attendants, kitchen helpers and related support occupations", "6513": "Food and beverage servers",
        "6311": "Food service supervisors", "7241": "Electricians (except industrial and power system)", "7271": "Carpenters",
        "7251": "Plumbers", "7611": "Construction trades helpers and labourers", "7521": "Heavy equipment operators (except crane)",
        "6421": "Retail salespersons", "6611": "Cashiers", "6622": "Store shelf stockers, clerks and order fillers",
        "7511": "Transport truck drivers", "7452": "Material handlers",
        "9462": "Industrial butchers and meat cutters, poultry preparers and related workers",
        "9617": "Labourers in food and beverage processing", "7311": "Construction millwrights and industrial mechanics",
        "7237": "Welders and related machine operators", "2174": "Computer programmers and interactive media developers",
        "1241": "Administrative assistants", "6731": "Light duty cleaners", "4032": "Elementary school and kindergarten teachers",
        "8611": "Harvesting labourers", "7321": "Automotive service technicians, truck and bus mechanics and mechanical repairers",
        "1311": "Accounting technicians and bookkeepers", "1411": "General office support workers",
        "6552": "Other customer and information services representatives", "1121": "Human resources professionals",
        "6733": "Janitors, caretakers and building superintendents", "4216": "Other instructors",
        "4011": "University professors and lecturers", "3414": "Other assisting occupations in support of health services",
        "3211": "Medical laboratory technologists", "3112": "General practitioners and family physicians",
        "4411": "Home child care providers", "6721": "Support occupations in accommodation, travel and facilities set-up services",
        "6525": "Hotel front desk clerks", "7612": "Other trades helpers and labourers",
        "7313": "Refrigeration and air conditioning mechanics", "9411": "Machine operators, mineral and metal processing",
        "9463": "Fish and seafood plant workers", "6411": "Sales and account representatives - wholesale trade (non-technical)",
        "7514": "Delivery and courier service drivers", "8431": "General farm workers",
        "8252": "Agricultural service contractors, farm supervisors and specialized livestock workers", "6332": "Bakers",
        "4311": "Police officers (except commissioned)", "1521": "Shippers and receivers", "1221": "Administrative officers",
    }
    rows = []
    for code21 in sorted(c16, key=lambda c: c16[c]):
        rows.append([c16[code21], titles16[c16[code21]], code21, t21[code21]])
    C.write_csv(os.path.join(tgt, "noc_2016_v1.3_to_noc_2021_v1.0.csv"),
                ["noc_2016", "noc_2016_title", "noc_2021", "noc_2021_title"], rows)
    return len(rows)


def write_main(emps, vac, tgt, rng):
    posts = build_postings(emps, vac, rng)
    n_old, n_new = write_snapshots(posts, emps, tgt)
    write_activity(posts, tgt)
    write_cases(posts, emps, rng, tgt)
    write_employers(emps, rng, tgt)
    write_concordance(tgt)
    return posts
