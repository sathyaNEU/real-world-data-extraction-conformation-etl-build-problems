"""Writers for every shipped file."""
import calendar
import csv
import datetime as dt
import io
import json
import os
from zoneinfo import ZoneInfo

import numpy as np
import params as P
import records as RC

LON, UTC = ZoneInfo("Europe/London"), ZoneInfo("UTC")
FILES = {
    "legacy": "walkin_tickets_legacy_2023-04_to_2024-11.csv",
    "events": "phlebotomy_queue_events_2024-11-18_to_2026-09-30.csv",
    "log": "reception_turned_away_log.xlsx",
    "roster": "eroster_phlebotomy_2023-04_to_2026-09.csv",
    "kiosk": "kiosk_ticket_allocations_2023-04_to_2026-09.csv",
    "practices": "gp_practices_catchment.csv",
    "clinics": "outpatient_clinic_codes.csv",
    "report": "phlebotomy_annual_report_2025-26.pdf",
    "icb": "icb_pathology_planning_assumptions_2026-27.pdf",
    "bh": "bank_holidays_england.json",
    "survey": "phlebotomy_patient_survey_2025.csv",
    "hub": "community_hub_session_plan_2027.xlsx",
    "dict": "data_dictionary.csv",
}
PACK = list(FILES)
DISTRACTORS = ["survey", "hub"]
CONTEXT = ["report", "icb"]


def save_xlsx(wb, path, when=dt.datetime(2026, 10, 2, 9, 12), author=None):
    """Save a workbook with fixed document properties and fixed zip entry times, so a rebuild is byte-identical."""
    import zipfile
    wb.properties.created = when
    wb.properties.modified = when
    if author:
        wb.properties.creator = author
        wb.properties.lastModifiedBy = author
    tmp = path + ".tmp"
    wb.save(tmp)
    with zipfile.ZipFile(tmp) as zin, zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            zi = zipfile.ZipInfo(info.filename, date_time=(when.year, when.month, when.day, when.hour, when.minute, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            data = zin.read(info.filename)
            if info.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.'
                        b'openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats'
                        b'.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel</Application><DocSecurity>0'
                        b'</DocSecurity><ScaleCrop>false</ScaleCrop><Company>' + P.HOSPITAL.encode() + b'</Company>'
                        b'<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false'
                        b'</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            if info.filename == "docProps/core.xml":
                import re
                stamp = when.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data)
            zout.writestr(zi, data)
    os.remove(tmp)


def hms(m):
    s = int(round(m * 60))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def utc(d, m):
    x = dt.datetime(d.year, d.month, d.day, tzinfo=LON) + dt.timedelta(minutes=float(m))
    return x.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def legacy(target, V, rng):
    rows = []
    by_day = {}
    for v in V:
        if v[0] <= P.OLD_SYSTEM_OFF:
            by_day.setdefault(v[0], []).append(v)
    for d in sorted(by_day):
        a = f = 0
        lst = sorted(by_day[d], key=lambda v: v[6])
        for v in lst:
            dd, g, sp, prac, org, issued, m, called, recall, done, bay, fasting = v
            if fasting:
                f += 1
                tk = "F%03d" % f
            else:
                a += 1
                tk = "A%03d" % a
            key = m + (rng.uniform(0.2, 2.8) if dd >= P.NEW_SYSTEM_LIVE else 0.0)
            shown_call = recall if recall is not None else called
            desk = str(bay) if not str(bay).startswith("B") else "B"
            rows.append(["HGH Outpatients", d.strftime("%d/%m/%Y"), tk, hms(key), hms(max(shown_call, key + 0.1)), desk,
                         "Hospital form" if g == "H" else "GP form", "Fasting blood test" if fasting else "Blood test", "Seen"])
        if rng.random() < 0.025:
            rows.append(["HGH Outpatients", d.strftime("%d/%m/%Y"), "Z001", "07:01:12", "07:01:40", "1", "", "Test", "Test ticket"])
    write_csv(os.path.join(target, FILES["legacy"]),
              ["Site", "Date", "Ticket", "Issued", "Called", "Desk", "Request", "Service", "Outcome"], rows)
    return len(rows)


def events(target, V, rng):
    rows, eid, vid = [], 50200000, 1048000
    for v in V:
        dd, g, sp, prac, org, issued, m, called, recall, done, bay, fasting = v
        if dd < P.NEW_SYSTEM_LIVE:
            continue
        vid += 1
        ref = "PV%08d" % vid
        blank = (g != "H") and rng.random() < 0.006
        rtype = "HOSP" if g == "H" else "GP"
        eid += 1
        rows.append([eid, ref, "CHECKED_IN", utc(dd, m), "", rtype, "" if blank else org,
                     "" if blank else issued.isoformat(), "WALK_IN_FASTING" if fasting else "WALK_IN"])
        eid += 1
        bayname = "Bay %s" % bay
        rows.append([eid, ref, "CALLED", utc(dd, called), bayname, "", "", "", ""])
        if recall is not None:
            eid += 1
            rows.append([eid, ref, "CALLED", utc(dd, recall), bayname, "", "", "", ""])
        eid += 1
        rows.append([eid, ref, "COMPLETED", utc(dd, done), bayname, "", "", "", ""])
    write_csv(os.path.join(target, FILES["events"]),
              ["event_id", "visit_ref", "event_type", "event_utc", "bay", "request_type", "request_org", "request_date",
               "pathway"], rows)
    return len(rows)


def gone_text(m, style):
    h, mi = int(m // 60), int(m % 60)
    if style == 0:
        return "%02d:%02d" % (h, mi)
    if style == 1:
        return "%d.%02d" % (h, mi)
    return "%d:%02d%s" % (h if h <= 12 else h - 12, mi, "am" if h < 12 else "pm")


def reception_log(target, W, V, AW, rng):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    gone = {}
    for v in V:
        gone[v[0]] = max(gone.get(v[0], 0), v[6])
    turned = {}
    for d, g, m in AW:
        key = "H" if g == "H" else "G"
        half = "AM" if m < 750 else "PM"
        turned.setdefault(d, {"G": {"AM": 0, "PM": 0}, "H": {"AM": 0, "PM": 0}})[key][half] += 1
    wb = Workbook()
    wb.remove(wb.active)
    days = [d for d in W["days"] if d <= P.REC_END]
    for fy in (2023, 2024, 2025, 2026):
        ws = wb.create_sheet("%d-%s" % (fy, str(fy + 1)[2:]))
        ws.append(["Phlebotomy reception: patients turned away after the day's tickets had gone (PALS monthly return)"])
        ws["A1"].font = Font(bold=True)
        fdays = [d for d in days if (d.year - (d.month < 4)) == fy]
        if fy <= 2024:
            ws.append(["One line per clinic day. Leave the boxes blank if nobody was turned away. AM is the morning "
                       "receptionist's shift (to 12:30). Totals to %s by the 3rd." % P.PEOPLE["reception"]])
            ws.append([])
            ws.append(["Date", "Day", "Tickets gone at", "GP form AM", "GP form PM", "Hospital form AM",
                       "Hospital form PM", "Comments"])
            cur, tot = None, [0, 0, 0, 0]
            for d in fdays:
                if cur is not None and d.month != cur.month:
                    ws.append(["Total %s" % cur.strftime("%B %Y"), None, None] + [x or None for x in tot] + [None])
                    ws.append([])
                    tot = [0, 0, 0, 0]
                cur = d
                if d in turned:
                    t = turned[d]
                    vals = [t["G"]["AM"], t["G"]["PM"], t["H"]["AM"], t["H"]["PM"]]
                    com = None
                    if (vals[1] or vals[3]) and rng.random() < 0.18:
                        vals = [vals[0] + vals[1], 0, vals[2] + vals[3], 0]
                        com = "inc PM"
                    tot = [a + b for a, b in zip(tot, vals)]
                    ws.append([d, d.strftime("%a"), gone_text(gone[d], int(rng.choice([0, 0, 1, 2])))] +
                              [x if x else None for x in vals] + [com])
                else:
                    ws.append([d, d.strftime("%a"), None, None, None, None, None, None])
            if cur is not None:
                ws.append(["Total %s" % cur.strftime("%B %Y"), None, None] + [x or None for x in tot] + [None])
        else:
            ws.append(["From April 2025 log only the days the tickets ran out, one line per day."])
            ws.append([])
            ws.append(["Date", "Tickets gone", "GP forms turned away", "Hospital forms turned away", "Initials"])
            for d in fdays:
                if d in turned:
                    t = turned[d]
                    dv = d if rng.random() > 0.03 else d.strftime("%d/%m/%Y")
                    ws.append([dv, gone_text(gone[d], int(rng.choice([0, 0, 0, 1]))), t["G"]["AM"] + t["G"]["PM"],
                               t["H"]["AM"] + t["H"]["PM"], str(rng.choice(["RR", "CD", "RW", "RR", "CD"]))])
        for row in ws.iter_rows(min_row=1):
            for cell in row:
                if isinstance(cell.value, dt.date):
                    cell.number_format = "DD/MM/YYYY"
    path = os.path.join(target, FILES["log"])
    save_xlsx(wb, path, dt.datetime(2026, 10, 1, 16, 48), P.PEOPLE["reception"])
    return turned


EMP = ["20441735", "20495208", "20611843", "20730512", "20884271", "21006734", "21139068"]
GRADES = ["Senior Phlebotomist Band 3"] + ["Phlebotomist Band 2"] * 6
BANKPOOL = ["B-38812", "B-40157", "B-41930", "B-42288"]


def eroster(target, W, rng):
    rows = []
    days = W["days"]
    n = sum(1 for d in days if d <= P.REC_END)
    st = W["status"]
    # once a holder's sickness passes five clinic days the e-roster unassigns the line until the holder returns
    unassigned = np.zeros((n, P.POSTS), bool)
    for p in range(P.POSTS):
        i = 0
        while i < n:
            if st[i, p] == "SICK":
                j = i
                while j < n and st[j, p] == "SICK":
                    j += 1
                if j - i > P.UNASSIGN_AFTER:
                    unassigned[i + P.UNASSIGN_AFTER:j, p] = True
                i = j
            else:
                i += 1
    for i in range(n):
        d = days[i]
        for p in range(P.POSTS):
            s = st[i, p]
            if s == "VAC" or unassigned[i, p]:
                rows.append([d.isoformat(), "", GRADES[p], "CLIN 07:30-15:30", "", "Y", "7.50"])
                continue
            emp = P.VACANCY_SUCCESSOR if (p == P.POSTS - 1 and d > P.VACANCY[1]) else EMP[p]
            absn = {"CLIN": "", "SICK": "Sickness", "AL": "Annual leave"}[s]
            rows.append([d.isoformat(), emp, GRADES[p], "CLIN 07:30-15:30", absn, "N", "7.50"])
        for k in range(int(W["bank"][i])):
            rows.append([d.isoformat(), BANKPOOL[(i + k) % len(BANKPOOL)] if rng.random() < 0.9 else str(rng.choice(BANKPOOL)),
                         "Bank Phlebotomist", "BANK 07:30-15:30", "", "N", "7.50"])
    write_csv(os.path.join(target, FILES["roster"]),
              ["Roster date", "Employee no", "Assignment", "Shift", "Absence", "Vacant line", "Hours"], rows)
    return len(rows)


def kiosk(target, W, rng):
    rows = []
    for i, d in enumerate(W["days"]):
        if d > P.REC_END:
            break
        rows.append([d.strftime("%d/%m/%Y"), "07:%02d" % int(rng.integers(2, 14)), int(W["alloc"][i]),
                     str(rng.choice(["RD", "RD", "RD", "JP", "SM"]))])
    write_csv(os.path.join(target, FILES["kiosk"]), ["Date", "Set at", "Tickets", "Set by"], rows)


def practices(target):
    rows = []
    for code, name, size, g, own in P.PRACTICES:
        sizes = [round(size * (1 + g) ** k) for k in range(4)]
        note = ""
        if code == P.MERGED_FROM:
            note = "Merged into Fellside Health Centre (K91031) on 1 October 2025; list closed at the merger"
            sizes[3] = ""
        if code == P.MERGED_INTO:
            cv = [x for x in P.PRACTICES if x[0] == P.MERGED_FROM][0]
            sizes[3] = sizes[3] + round(cv[2] * (1 + cv[3]) ** 3)
            note = "Includes Castle View Medical Centre's patients from 1 October 2025"
        rows.append([code, name] + sizes + ["Y" if own else "N", note])
    write_csv(os.path.join(target, FILES["practices"]),
              ["practice_code", "practice_name", "list_size_2023-04", "list_size_2024-04", "list_size_2025-04",
               "list_size_2026-04", "phlebotomy_les_2025-26", "notes"], rows)


DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def clinics(target):
    rows = []
    loc = {"Cardiology": "Outpatients block C", "Diabetes and endocrinology": "Diabetes Centre",
           "Gastroenterology": "Outpatients block C", "General medicine": "Outpatients block A",
           "Haematology": "Haematology Day Unit", "Renal medicine": "Renal Unit", "Rheumatology": "Outpatients block B"}
    for name, (code, wds) in sorted(P.NEW_CLINIC.items(), key=lambda kv: kv[1][0]):
        rows.append([code, "%s outpatient clinic" % name, name, ", ".join(DAYN[x] for x in wds), loc[name]])
    write_csv(os.path.join(target, FILES["clinics"]),
              ["clinic_code", "clinic_name", "specialty", "clinic_days", "location"], rows)


def bank_holidays(target):
    titles = {(1, 1): "New Year's Day", (12, 25): "Christmas Day", (12, 26): "Boxing Day"}
    ev = []
    for y, m, d in P.BANK_HOLIDAYS:
        x = dt.date(y, m, d)
        if (m, d) in titles:
            t = titles[(m, d)]
        elif m == 12 or (m == 1):
            t = "Substitute day" if m == 12 else "New Year's Day"
        elif m in (3, 4) and x.weekday() == 4:
            t = "Good Friday"
        elif m in (3, 4) and x.weekday() == 0:
            t = "Easter Monday"
        elif m == 5 and x.day <= 7:
            t = "Early May bank holiday"
        elif m == 5 and x.day == 8:
            t = "Bank holiday for the coronation of King Charles III"
        elif m == 5:
            t = "Spring bank holiday"
        else:
            t = "Summer bank holiday"
        ev.append({"title": t, "date": x.isoformat(), "notes": "Substitute day" if t == "Substitute day" else "",
                   "bunting": True})
    doc = {"england-and-wales": {"division": "england-and-wales", "events": ev}}
    with open(os.path.join(target, FILES["bh"]), "w") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")


def survey(target, rng):
    rows = []
    bands = ["Under 15 minutes", "15 to 30 minutes", "30 to 45 minutes", "45 to 60 minutes", "Over an hour"]
    for k in range(412):
        rows.append([3100 + k, "2025-06", str(rng.choice(["GP request", "Hospital clinic request"], p=[0.74, 0.26])),
                     bands[int(rng.choice(5, p=[0.12, 0.22, 0.25, 0.23, 0.18]))],
                     int(rng.choice([1, 2, 3, 4, 5], p=[0.04, 0.07, 0.11, 0.38, 0.40])),
                     str(rng.choice(["Yes", "No", "Not sure"], p=[0.71, 0.12, 0.17]))])
    write_csv(os.path.join(target, FILES["survey"]),
              ["response_id", "survey_month", "request_type", "time_waited", "rating_1_to_5", "would_recommend"], rows)


def hub_plan(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Sessions"
    ws.append(["Kingsmead Health Village community phlebotomy hub: draft session plan from April 2027 (Outpatients "
               "business office)"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Day", "Opens", "Closes", "Chairs", "Booked slots per chair", "Walk-in tickets per chair",
               "Phlebotomists rostered"])
    for d, o, c, ch, b, w, ph in [("Monday", "07:30", "16:00", 10, 16, 26, 10), ("Tuesday", "07:30", "16:00", 9, 16, 24, 9),
                                   ("Wednesday", "07:30", "16:00", 9, 16, 24, 9), ("Thursday", "07:30", "18:30", 9, 20, 24, 10),
                                   ("Friday", "07:30", "15:00", 8, 14, 22, 8)]:
        ws.append([d, o, c, ch, b, w, ph])
    ws.append([])
    ws.append(["Walk-in tickets are not capped: the senior phlebotomist adds bank chairs on the day."])
    ws2 = wb.create_sheet("Staffing")
    ws2.append(["Role", "Band", "WTE", "Funding"])
    for r in [("Hub lead phlebotomist", 4, 1.0, "Recurrent"), ("Senior phlebotomist", 3, 2.0, "Recurrent"),
              ("Phlebotomist", 2, 9.6, "Recurrent"), ("Receptionist", 2, 2.0, "Recurrent"),
              ("Bank phlebotomist", 2, 1.5, "Non-recurrent")]:
        ws2.append(list(r))
    save_xlsx(wb, os.path.join(target, FILES["hub"]), dt.datetime(2026, 9, 24, 11, 3), P.PEOPLE["outpatients"])


def dictionary(target):
    rows = [
        (FILES["legacy"], "Date", "Clinic day the ticket was issued (dd/mm/yyyy, UK local time)"),
        (FILES["legacy"], "Ticket", "Ticket number shown to the patient; numbering restarts each day, A for blood tests and F for fasting blood tests"),
        (FILES["legacy"], "Issued", "Time the kiosk issued the ticket (UK local time)"),
        (FILES["legacy"], "Called", "Time of the last call of the ticket to a desk (UK local time)"),
        (FILES["legacy"], "Desk", "Desk number; B is the bank phlebotomist's desk"),
        (FILES["legacy"], "Request", "Request form the patient brought, as chosen at the kiosk"),
        (FILES["legacy"], "Outcome", "Seen, or Test ticket for kiosk tests by the IT team"),
        (FILES["events"], "event_utc", "Time of the event in UTC"),
        (FILES["events"], "event_type", "CHECKED_IN when the patient takes a ticket; CALLED each time the ticket is called to a bay; COMPLETED when the bay closes the visit"),
        (FILES["events"], "visit_ref", "One reference per ticket"),
        (FILES["events"], "request_type", "GP or HOSP, the request form the patient brought, as chosen at the kiosk"),
        (FILES["events"], "request_org", "Code of the organisation that issued the request, read from the form's barcode: the practice's ODS code or the outpatient clinic code; blank where the form has no barcode"),
        (FILES["events"], "request_date", "Date the request was issued, read from the form's barcode"),
        (FILES["events"], "pathway", "WALK_IN or WALK_IN_FASTING"),
        (FILES["roster"], "Hours", "Rostered hours for the line on the roster date"),
        (FILES["roster"], "Absence", "Blank when worked; Annual leave; Sickness"),
        (FILES["roster"], "Vacant line", "Y where no substantive post holder was assigned to the line on the roster date"),
        (FILES["kiosk"], "Tickets", "Walk-in tickets the senior phlebotomist set the kiosk to issue that day"),
        (FILES["practices"], "phlebotomy_les_2025-26", "Y where the practice holds the 2025-26 phlebotomy local enhanced service"),
        (FILES["clinics"], "clinic_code", "Outpatient clinic code on the trust's patient administration system"),
        (FILES["clinics"], "clinic_days", "Weekdays the clinic runs"),
        (FILES["survey"], "time_waited", "Patient's own estimate of the wait after taking a ticket"),
    ]
    write_csv(os.path.join(target, FILES["dict"]), ["file", "column", "description"], rows)
