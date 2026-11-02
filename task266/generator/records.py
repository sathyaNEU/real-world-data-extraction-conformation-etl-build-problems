"""The pack's data files, each in its producing system's own layout."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import world as W

LEG_EXPO = {"Occupational": "OCC", "Domestic": "DOM", "Environmental": "ENV", "No exposure identified": "NIL"}


def _d(x):
    return W.day(x)


def _iso(x):
    return "" if x is None else _d(x).isoformat()


def _csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        for r in rows:
            w.writerow(r)
    return len(rows)


def _head(ws, row, values, widths=None, fill="1F3B57"):
    for j, v in enumerate(values, 1):
        c = ws.cell(row=row, column=j, value=None if v == "" else v)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for j, wd in enumerate(widths, 1):
            ws.column_dimensions[ws.cell(row=row, column=j).column_letter].width = wd


# ------------------------------------------------------------------------------------------ the register
def write_register(path, T):
    rows = []
    for c in T["register"]:
        if _d(c["notified"]) <= K.LEGACY_END:
            continue
        rows.append([c["ref"], c["notif_no"], _iso(c["notified"]), c["sex"], _iso(c["dob"]), _iso(c["D"]), c["site"],
                     c["histology"], c["basis"], c["hospital"], c["category"], _iso(c["interview"]),
                     "Deceased" if c["death"] is not None else "Living", _iso(c["death"]), c["claim"]])
    return _csv(path, ["fund_ref", "notification_no", "notified", "sex", "date_of_birth", "date_of_diagnosis",
                       "primary_site", "histology", "basis_of_diagnosis", "diagnosing_hospital", "exposure_category",
                       "interview_date", "vital_status_2026_09_30", "date_of_death", "claim_status"], rows)


def write_legacy(path, T):
    wb = Workbook()
    ws = wb.active
    ws.title = "Register"
    ws["A1"] = "%s - mesothelioma register (case system 1)" % K.FUND
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Cases notified 1 July 2004 to 31 December 2012. Export of 15 February 2013, when case system 1 was closed."
    head = ["Ref", "Notif No", "Notified", "Sex", "DOB", "Date diagnosed", "Site", "Histology", "Basis", "Hospital",
            "Exposure", "Interviewed", "Died", "Claim"]
    _head(ws, 4, head, [13, 11, 12, 5, 12, 13, 12, 22, 20, 28, 9, 12, 12, 15])
    r = 5
    n = 0
    for c in T["register"]:
        if _d(c["notified"]) > K.LEGACY_END:
            continue
        died = K.fmt_legacy(_d(c["death"])) if c["death"] is not None and _d(c["death"]) <= dt.date(2013, 2, 15) else ""
        vals = [c["ref"], c["notif_no"], K.fmt_legacy(_d(c["notified"])), c["sex"][0], K.fmt_legacy(_d(c["dob"])),
                K.fmt_legacy(_d(c["D"])), c["site"], c["histology"], c["basis"], c["hospital"],
                LEG_EXPO[c["category"]], K.fmt_legacy(_d(c["interview"])), died, c["claim"]]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=None if v == "" else v)
        r += 1
        n += 1
    ws.freeze_panes = "A5"
    wb.save(path)
    return n


def write_histories(path, T):
    """Every register case's occupational history as its interview recorded it. Interviews on the first system
    (cases notified to 2012) were migrated in January 2013 with their workplace and occupation as written."""
    rows = []
    for c in T["register"]:
        legacy = _d(c["notified"]) <= K.LEGACY_END
        order = list(c["spells"])
        for k, s in enumerate(order, 1):
            end = "" if s["end"] >= c["D"] - 30 else (K.fmt_legacy(_d(s["end"])) if legacy else _iso(s["end"]))
            start = K.fmt_legacy(_d(s["start"])) if legacy else _iso(s["start"])
            rows.append([c["hist_ref"], k, s["employer"], s["workplace"] if legacy else "",
                         "" if legacy else s["wp_code"], s["occ"][1], "" if legacy else s["occ"][0], start, end,
                         ("Yes" if s["exposed"] else "No") if legacy else ("Y" if s["exposed"] else "N"),
                         "Interview 2004-2012" if legacy else "Exposure assessment",
                         K.fmt_legacy(_d(c["interview"])) if legacy else _iso(c["interview"])])
    return _csv(path, ["case_ref", "job_no", "employer", "workplace", "workplace_code", "occupation", "anzsco_code",
                       "started", "ended", "asbestos_exposure", "source", "interview_date"], rows)


WP_KINDS = [("%s Power Station", "Power generation"), ("%s District Hospital (boiler house)", "Health services"),
            ("%s High School", "Education buildings"), ("%s Railway Depot", "Rail transport"),
            ("%s Council Works Depot", "Local government"), ("%s Butter Factory", "Food manufacturing"),
            ("%s Brickworks", "Building products"), ("%s Sawmill", "Timber"), ("%s Woolstore", "Storage"),
            ("%s Water Treatment Plant", "Water and sewerage"), ("%s Telephone Exchange", "Communications"),
            ("%s Courthouse", "Public buildings"), ("%s Showground grandstand", "Public buildings"),
            ("%s Abattoir", "Meat processing"), ("%s Gasworks", "Gas supply"), ("%s Post Office", "Public buildings")]
WP_FIRMS = ["Hadley & Sons Engineering", "Meredith Insulation Co.", "Tasker Building Supplies", "Corlett Bros. Plumbing",
            "Westgate Asbestos Products", "Southern Boiler Co.", "R. J. Penhall & Co.", "Ironside Fabrications",
            "Lomax Brake Services", "Pacific Lagging Contractors", "Crossley Electrical", "Dunmore Constructions",
            "Highfield Roofing", "Albion Pipe & Fittings", "Kingsway Motors (workshop)", "Garnet Ship Repairs"]


def write_workplaces(path, T):
    """The Fund's register of workplaces where asbestos was used or suspected (a distractor: no answer reads it)."""
    rng = np.random.default_rng([K.SEED, 9])
    used = set(T["workplace_codes"].values())
    rows = []
    for name, code in T["workplace_codes"].items():
        exposed = name in W.EMPLOYERS_EXPOSED
        ind = ("Power generation" if "Power" in name else "Asbestos cement manufacture" if "Cement" in name or "Fibro" in name
               else "Shipbuilding and repair" if "Ship" in name or "dockyard" in name else "Construction and trades"
               if exposed else "Not an asbestos workplace")
        rows.append([code, name, ind, int(rng.integers(1938, 1966)) if exposed else "",
                     int(rng.integers(1978, 1990)) if exposed else "", "Confirmed" if exposed else "Not listed"])
    places = list(K.CITIES) + list(K.CIRCUIT) + list(K.WAYPOINTS)
    seen = {r[1] for r in rows}
    while len(rows) < 412:
        if rng.random() < 0.8:
            fmt, ind = WP_KINDS[int(rng.integers(len(WP_KINDS)))]
            name = fmt % places[int(rng.integers(len(places)))]
        else:
            name = "%s, %s" % (WP_FIRMS[int(rng.integers(len(WP_FIRMS)))], places[int(rng.integers(len(places)))])
            ind = "Construction and trades"
        if name in seen:
            continue
        seen.add(name)
        while True:
            code = "WP%04d" % int(rng.integers(1000, 9999))
            if code not in used:
                used.add(code)
                break
        status = str(rng.choice(["Confirmed", "Probable", "Suspected", "Not confirmed"], p=[0.46, 0.27, 0.17, 0.10]))
        y0 = int(rng.integers(1930, 1972))
        y1 = min(int(y0 + rng.integers(6, 45)), 2003)
        rows.append([code, name, ind, y0 if status != "Not confirmed" else "", y1 if status != "Not confirmed" else "",
                     status])
    rows.sort(key=lambda r: r[0])
    return _csv(path, ["workplace_code", "workplace_name", "industry", "asbestos_use_from", "asbestos_use_to",
                       "listing"], rows)


# ------------------------------------------------------------------------------------------ the program
def write_members(path, T):
    rows = []
    for m in T["members"]:
        rows.append([m["no"], m["sex"], _d(m["dob"]).year, _iso(m["E"]), m["town"], _iso(m["enrolled"]), m["status"],
                     _iso(m["status_date"])])
    return _csv(path, ["member_no", "sex", "year_of_birth", "first_exposure", "home_locality", "enrolled",
                       "status", "status_date"], rows)


def write_appointments(path, T):
    rows = []
    for r in T["bookings"]:
        rows.append([r["id"], r["member"], r["site"], r["date"].isoformat(), r["time"], r["review"],
                     r["booked"].isoformat(), r["status"]])
    return _csv(path, ["booking_id", "member_no", "site", "appointment_date", "appointment_time", "review",
                       "booked_on", "attendance"], rows)


def write_card(path, T):
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws["A1"] = "Fleet card statement - Mobile Review Unit (vehicle MRU-1)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Card ending 4417. Statement period 1 July 2025 to 30 June 2026."
    _head(ws, 4, ["Date", "Time", "Merchant", "Location", "Category", "Litres", "Odometer", "Amount (AUD)"],
          [12, 7, 34, 18, 14, 9, 10, 13])
    r = 5
    for c in T["card"]:
        vals = [c["t"].date().isoformat(), c["t"].strftime("%H:%M"), c["merchant"], c["location"], c["category"],
                c["litres"], c["odo"], c["amount"]]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=None if v == "" else v)
        r += 1
    ws.freeze_panes = "A5"
    wb.save(path)
    return len(T["card"])


def write_qa(path, T):
    wb = Workbook()
    a = wb.active
    a.title = "Jul-Dec 2025"
    a["A1"] = "MRU-1 X-ray unit: daily QA and exposure counter"
    a["A1"].font = Font(bold=True)
    _head(a, 3, ["Date", "Operator", "Counter start", "Counter end", "Constancy exposures", "Remarks"],
          [12, 9, 13, 13, 12, 34])
    b = wb.create_sheet("Jan-Jun 2026")
    b["A1"] = "MRU-1 X-ray QA log (template rev. 2, from January 2026)"
    b["A1"].font = Font(bold=True)
    _head(b, 3, ["Date", "Radiographer", "Exposure count (start)", "Exposure count (end)", "QC exposures", "Comments"],
          [12, 12, 18, 18, 12, 34])
    rng = np.random.default_rng([K.SEED, 6])
    remarks = ["Constancy within limits", "Constancy OK", "Constancy OK, kV and mAs in tolerance", "Detector calibration done",
               "Gain calibration after move", "Warm-up exposures after cold start (tube cold overnight)",
               "Collimator light field checked against marks", "Grid alignment checked", "Lead aprons inspected, one tagged",
               "Exposure index drifting high, rechecked after cal, OK", "Dose meter batteries replaced",
               "Mains at venue, no generator", "Ran on generator all day", "Air-con fault in the morning, room 27 C",
               "Detector cover cleaned", "Spirometer calibration syringe check passed", "Bucky tray sticking, freed",
               "Quarterly physics check due next visit", "Pressure in the cabin door seal low, reported to fleet"]
    ra, rb = 4, 4
    for k, q in enumerate(T["qa"]):
        r = rng.random()
        note = "" if r < 0.34 else remarks[int(rng.integers(len(remarks)))]
        if q["date"] < dt.date(2026, 1, 1):
            ws, row = a, ra
            ra += 1
            vals = [q["date"].strftime("%d/%m/%Y"), q["op"], q["start"], q["end"], q["tests"], note]
        else:
            ws, row = b, rb
            rb += 1
            vals = [q["date"].isoformat(), q["op"], q["start"], q["end"], q["tests"], note]
        for j, v in enumerate(vals, 1):
            ws.cell(row=row, column=j, value=None if v == "" else v)
    wb.save(path)
    return len(T["qa"])


def write_roads(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Road km"
    places = list(K.CITIES) + list(K.CIRCUIT) + list(K.WAYPOINTS) + list(K.LOCALITIES)
    ws["A1"] = "Review sites and localities: road distances (km), from the travel reimbursement table"
    ws["A1"].font = Font(bold=True)
    _head(ws, 3, ["From \\ To"] + places, [18] + [9] * len(places))
    for i, a in enumerate(places):
        ws.cell(row=4 + i, column=1, value=a).font = Font(bold=True)
        for j, b in enumerate(places):
            ws.cell(row=4 + i, column=2 + j, value=K.road_km(a, b))
    s2 = wb.create_sheet("Sites")
    _head(s2, 1, ["Site code", "Site", "Locality"], [10, 40, 18])
    rr = 2
    for code, (town, name) in K.CLINIC_SITES.items():
        for j, v in enumerate([code, name, town], 1):
            s2.cell(row=rr, column=j, value=v)
        rr += 1
    for j, v in enumerate([K.UNIT_SITE, "Mobile Review Unit (circuit as scheduled)", K.UNIT_BASE + " (base)"], 1):
        s2.cell(row=rr, column=j, value=v)
    wb.save(path)
    return len(places)


def write_registry(path):
    """The State Cancer Registry's published counts of mesothelioma by year of diagnosis and sex (a distractor)."""
    rng = np.random.default_rng([K.SEED, 8])
    wb = Workbook()
    ws = wb.active
    ws.title = "Table 7.3"
    ws["A1"] = "Table 7.3 Mesothelioma (ICD-10 C45), new cases by year of diagnosis and sex, 1982-2024"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "%s, Cancer in the State 2024 (published November 2025)" % K.REGISTRY
    _head(ws, 4, ["Year", "Males", "Females", "Persons"], [8, 9, 9, 9])
    for i, y in enumerate(range(1982, 2025)):
        lvl = 60 + 210 / (1 + np.exp(-(y - 1998) / 5.5)) - 0.9 * max(0, y - 2014) ** 1.3
        m = int(round(lvl * 0.86 + rng.normal(0, 7)))
        f = int(round(lvl * 0.14 + rng.normal(0, 3)))
        for j, v in enumerate([y, m, f, m + f], 1):
            ws.cell(row=5 + i, column=j, value=v)
    ws.cell(row=5 + 43 + 1, column=1, value="Counts for 2023 and 2024 are preliminary and may rise as late notifications arrive.")
    wb.save(path)
    return 43
