"""Writers for the bundle's data files, each in the layout and idiom of the system that exports it."""
import csv
import datetime as dt

import numpy as np

import world as W

D = dt.date
FILES = {
    "register": "open_payments_general_2021-2025_jan2027_extract.csv",
    "register_june": "open_payments_general_py2025_jun2026_extract.csv",
    "profiles": "open_payments_covered_recipient_profiles.csv",
    "research": "open_payments_research_2021-2025_extract.csv",
    "roster": "clinical_faculty_appointments.csv",
    "depts": "department_codes.csv",
    "entities": "coi_entity_list.csv",
    "export": "coi_disclosures_2021-2026_export.xlsx",
    "history": "coi_submission_history.csv",
    "nih": "nih_awards_marrowfield_fy2025.csv",
    "policy": "coi_policy_2024.pdf",
    "guide": "coi_disclosure_form_guide_2026.pdf",
    "dict": "oricoi_field_definitions.xlsx",
    "manifest": "oricoi_export_contents_2027-01-21.csv",
}

OP_COLUMNS = [
    "Change_Type", "Covered_Recipient_Type", "Teaching_Hospital_CCN", "Teaching_Hospital_ID", "Teaching_Hospital_Name",
    "Covered_Recipient_Profile_ID", "Covered_Recipient_NPI", "Covered_Recipient_First_Name",
    "Covered_Recipient_Middle_Name", "Covered_Recipient_Last_Name", "Covered_Recipient_Name_Suffix",
    "Recipient_Primary_Business_Street_Address_Line1", "Recipient_City", "Recipient_State", "Recipient_Zip_Code",
    "Recipient_Country", "Covered_Recipient_Primary_Type_1", "Covered_Recipient_Specialty_1",
    "Covered_Recipient_License_State_code1", "Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name",
    "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID",
    "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name",
    "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_State",
    "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Country", "Total_Amount_of_Payment_USDollars",
    "Date_of_Payment", "Number_of_Payments_Included_in_Total_Amount", "Form_of_Payment_or_Transfer_of_Value",
    "Nature_of_Payment_or_Transfer_of_Value", "City_of_Travel", "State_of_Travel", "Country_of_Travel",
    "Physician_Ownership_Indicator", "Third_Party_Payment_Recipient_Indicator",
    "Name_of_Third_Party_Entity_Receiving_Payment_or_Transfer_of_Value", "Charity_Indicator",
    "Third_Party_Equals_Covered_Recipient_Indicator", "Contextual_Information", "Delay_in_Publication_Indicator",
    "Record_ID", "Dispute_Status_for_Publication", "Related_Product_Indicator", "Covered_or_Noncovered_Indicator_1",
    "Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_1", "Product_Category_or_Therapeutic_Area_1",
    "Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1", "Program_Year", "Payment_Publication_Date",
    "ORICOI_Matched_Emp_ID",
]
NS_CITIES = [("Toledo", "OH"), ("Dayton", "OH"), ("Akron", "OH"), ("Youngstown", "OH"), ("Canton", "OH"), ("Erie", "PA"),
             ("Wheeling", "WV"), ("Fort Wayne", "IN"), ("Lansing", "MI"), ("Evansville", "IN"), ("Peoria", "IL"),
             ("Duluth", "MN"), ("Spokane", "WA"), ("Tulsa", "OK"), ("Reno", "NV")]
TRAVEL = [("Chicago", "IL"), ("Orlando", "FL"), ("Boston", "MA"), ("San Diego", "CA"), ("New Orleans", "LA"),
          ("Philadelphia", "PA"), ("Nashville", "TN"), ("Denver", "CO"), ("Atlanta", "GA"), ("Las Vegas", "NV")]
AREAS = {"CARD": "Cardiology", "ORTH": "Orthopedics", "HEON": "Oncology", "NEUR": "Neurology", "PSYC": "Psychiatry",
         "GAST": "Gastroenterology", "DERM": "Dermatology", "OPHT": "Ophthalmology", "UROL": "Urology",
         "IMED": "Endocrinology", "OBGY": "Women's Health", "ANES": "Anesthesiology", "RADI": "Radiology",
         "SURG": "General Surgery", "PEDS": "Immunology", "EMED": "Critical Care"}


def _w(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for row in rows:
            w.writerow(row)
    return len(rows)


def _money(x):
    return "%.2f" % x


def _product(m, r):
    name, kind = m["products"][int(r.integers(len(m["products"])))]
    return "Covered", kind, AREAS[m["primary"]], name


def register_rows(recs, mfrs, namesakes_by_npi):
    """Each record as the refresh publishes it (Record_ID and Change_Type fixed here), in the order the office's
    extract sorts them: program year, then recipient profile, then date. Returns (rows, meta) with meta keyed by
    Record_ID for the June vintage and the checks."""
    r = np.random.default_rng([W.SEED, 31])
    rows, meta = [], {}
    rid = 731000000
    order = sorted(range(len(recs)), key=lambda i: (recs[i]["year"], _profile(recs[i]), recs[i]["date"].toordinal(),
                                                     recs[i]["mfr"]["id"], recs[i]["amount"]))
    for i in order:
        rec = recs[i]
        f = rec["f"]
        m = rec["mfr"]
        rid += int(r.integers(1, 180))
        is_ns = rec.get("namesake", False)
        prof = _profile(rec)
        if is_ns:
            city, st = NS_CITIES[int(f.city)]
            addr = (_ns_street(f.npi), city, st, "%05d" % (40000 + int(f.npi[-5:]) % 9000))
            spec = W.SPECIALTY[f.twin.dept]
            ptype = "Medical Doctor"
            lic = st
        else:
            import register as RG
            addr = RG.address(f, rec["year"], r)
            spec = W.SPECIALTY[f.dept] if f.cred in ("MD", "DO") else W.APP_SPECIALTY[f.cred]
            ptype = {"MD": "Medical Doctor", "DO": "Doctor of Osteopathy", "NP": "Nurse Practitioner",
                     "PA": "Physician Assistant"}[f.cred]
            lic = "OH"
        rtype = ("Covered Recipient Non-Physician Practitioner" if (not is_ns and f.cred in ("NP", "PA"))
                 else "Covered Recipient Physician")
        npi = "" if rec["npi_blank"] else f.npi
        name_m = f.middle if r.random() < 0.6 else ""
        mname = W.former_name(m) if (m["index"] in W.RENAMED and rec["year"] <= 2024) else m["name"]
        if m["name"] in W.NOW_REPORTING_FORMER and rec["year"] <= 2025:
            mname = W.NOW_REPORTING_FORMER[m["name"]]
        nature = rec["nature"]
        travel = ("", "", "")
        if nature == "Travel and Lodging":
            c = TRAVEL[int(r.integers(len(TRAVEL)))]
            travel = (c[0], c[1], "United States")
        third = "No Third Party Payment"
        third_name = ""
        third_eq = ""
        if not rec["personal"]:
            third, third_name, third_eq = "Entity", W.ORG, "No"
        form = "In-kind items and services" if nature in ("Food and Beverage", "Travel and Lodging", "Education") else "Cash or cash equivalent"
        npay = "1"
        if nature == W.NATURES_REMUN[0] and r.random() < 0.08:
            npay = str(int(r.integers(2, 4)))
        cov, kind, area, brand = _product(m, r)
        related = "Yes" if nature not in ("Education",) else "No"
        ctx = ""
        if nature == W.NATURES_REMUN[1] and r.random() < 0.3:
            ctx = "Speaker program, %s" % area.lower()
        dispute = "Yes" if r.random() < 0.002 else "No"
        change = "UNCHANGED"
        if rec["year"] == 2025:
            change = "UNCHANGED"
        row = [change, rtype, "", "", "", prof, npi, f.first.upper() if r.random() < 0.15 else f.first, name_m,
               f.last.upper() if r.random() < 0.15 else f.last, "", addr[0], addr[1], addr[2], addr[3],
               "United States", ptype, spec, lic, mname if r.random() < 0.97 else mname.upper(), m["id"], mname, m["state"],
               "United States", _money(rec["amount"]), rec["date"].strftime("%m/%d/%Y"), npay, form, nature,
               travel[0], travel[1], travel[2], "No", third, third_name, "No" if third == "Entity" else "", third_eq, ctx,
               "No", str(rid), dispute, related, cov if related == "Yes" else "", kind if related == "Yes" else "",
               area if related == "Yes" else "", brand if related == "Yes" else "", str(rec["year"]), "01/15/2027",
               ""]
        rows.append(row)
        meta[str(rid)] = rec
        rec["rid"] = str(rid)
        rec["row"] = row
    return rows, meta


def _profile(rec):
    f = rec["f"]
    if rec.get("namesake"):
        return f.profile
    if rec.get("dup"):
        return f.dup_profile
    return f.profiles[-1] if (len(f.profiles) > 1 and rec["date"].toordinal() % 3 == 0) else f.profiles[0]


def matcher(rows, fac, namesakes):
    """The office's matcher: a record carrying an NPI joins the faculty member holding it; a record without one
    joins the faculty member whose first and last name it carries."""
    by_npi = {f.npi: f.emp_id for f in fac}
    by_name = {(f.first.lower(), f.last.lower()): f.emp_id for f in fac}
    i_npi, i_first, i_last = OP_COLUMNS.index("Covered_Recipient_NPI"), OP_COLUMNS.index("Covered_Recipient_First_Name"), OP_COLUMNS.index("Covered_Recipient_Last_Name")
    for row in rows:
        if row[i_npi]:
            row[-1] = by_npi.get(row[i_npi], "")
        else:
            row[-1] = by_name.get((row[i_first].lower(), row[i_last].lower()), "")
    return rows


def vintages(rows, meta):
    """Mark the refresh's changes to program year 2025 against the June 2026 publication, on records of faculty
    outside the docket region: a few added late (NEW), a few amounts corrected (CHANGED), and a few records the
    June publication carried that the refresh no longer does. Returns the June rows."""
    r = np.random.default_rng([W.SEED, 32])
    ic, ia, iy, ipub = OP_COLUMNS.index("Change_Type"), OP_COLUMNS.index("Total_Amount_of_Payment_USDollars"), OP_COLUMNS.index("Program_Year"), OP_COLUMNS.index("Payment_Publication_Date")
    irid = OP_COLUMNS.index("Record_ID")
    june = []
    for row in rows:
        rec = meta[row[irid]]
        if rec["year"] != 2025:
            if rec["remun"] and r.random() < 0.004 and rec["f"].group == "bg":
                row[ic] = "CHANGED"
            continue
        movable = rec["f"].group == "bg" and not rec.get("namesake")
        u = r.random()
        if movable and u < 0.012:
            row[ic] = "NEW"                       # submitted after the June publication
            continue
        jrow = list(row)
        jrow[ic] = "NEW"
        jrow[ipub] = "06/30/2026"
        if movable and u < 0.03:
            row[ic] = "CHANGED"
            jrow[ia] = _money(max(5.0, float(row[ia]) * float(r.choice([0.5, 0.8, 1.25, 2.0]))))
        june.append(jrow)
        if movable and rec["remun"] and r.random() < 0.006:
            gone = list(jrow)
            gone[irid] = str(int(row[irid]) + 7)
            gone[ia] = _money(float(row[ia]) * 0.5)
            june.append(gone)                     # in June, withdrawn by the manufacturer before the refresh
    return june


def write_register(rows, path):
    return _w(path, OP_COLUMNS, rows)


NS_STREETS = ["Professional Drive", "Medical Park Boulevard", "Corporate Drive", "Physicians Plaza", "Wellness Way",
              "Commerce Parkway", "Executive Court", "Healthplex Drive", "Main Street", "Oak Grove Road"]


def _ns_street(npi):
    """A namesake's practice address in another city."""
    return "%d %s" % (200 + int(npi[-4:]) % 4000, NS_STREETS[int(npi[-7:-4]) % len(NS_STREETS)])


def write_profiles(fac, namesakes, path):
    rows = []
    for f in fac:
        for k, p in enumerate(f.profiles):
            street, zp = W.CAMPUS[f.dept]
            rows.append([p, f.npi, f.first, f.middle, f.last, "", "MEDICAL DOCTOR" if f.cred in ("MD", "DO") else
                         ("NURSE PRACTITIONER" if f.cred == "NP" else "PHYSICIAN ASSISTANT"), street, W.CITY, W.STATE,
                         zp, "OH"])
        if getattr(f, "dup_profile", None):
            street, zp = W.CAMPUS[f.dept]
            rows.append([f.dup_profile, "", f.first, "", f.last, "", "MEDICAL DOCTOR", street, W.CITY, W.STATE, zp, ""])
    for ns in namesakes:
        city, st = NS_CITIES[int(ns.city)]
        rows.append([ns.profile, ns.npi if int(ns.npi[-1]) % 3 else "", ns.first, ns.middle, ns.last, "", "MEDICAL DOCTOR",
                     _ns_street(ns.npi), city, st,
                     "%05d" % (40000 + int(ns.npi[-5:]) % 9000), st])
    rows.sort(key=lambda x: int(x[0]))
    header = ["Covered_Recipient_Profile_ID", "Covered_Recipient_NPI", "Covered_Recipient_Profile_First_Name",
              "Covered_Recipient_Profile_Middle_Name", "Covered_Recipient_Profile_Last_Name",
              "Covered_Recipient_Profile_Suffix", "Covered_Recipient_Profile_Primary_Type",
              "Covered_Recipient_Profile_Address_Line_1", "Covered_Recipient_Profile_City",
              "Covered_Recipient_Profile_State", "Covered_Recipient_Profile_Zipcode",
              "Covered_Recipient_Profile_License_State_Code_1"]
    return _w(path, header, rows)


def roster_terms(f):
    """[(employee number, term)]: a faculty member whose employee number changed holds the terms before the change under
    the old number (the open term ending the day before) and the rest under the new one."""
    day = getattr(f, "rekey_day", None)
    if day is None:
        return [(f.emp_id, t) for t in f.terms]
    out = []
    for t in f.terms:
        if t["start"] < day:
            out.append((f.emp_id, dict(t, end=min(t["end"], day - dt.timedelta(days=1)))))
        if t["end"] >= day:
            out.append((f.new_emp_id, dict(t, start=max(t["start"], day))))
    return out


def write_roster(fac, path):
    rows = []
    for f in fac:
        for emp, t in roster_terms(f):
            rows.append([emp, f.last, f.first, f.middle, f.cred, f.npi, t["dept"], t["division"],
                         "Primary" if t["primary"] else "Secondary", f.rank, t["start"].isoformat(), t["end"].isoformat()])
    rows.sort(key=lambda x: (x[0], x[10], x[8]))
    header = ["emp_id", "last_name", "first_name", "middle_initial", "credential", "npi", "dept_code", "division_code",
              "appointment_type", "rank", "term_start", "term_end"]
    return _w(path, header, rows)


def write_depts(path):
    rows = [[W.MED[0], W.MED[1], "1972-07-01", "2025-06-30", ""]]
    for c, n, _ in W.DEPTS:
        if c in W.SUCCESSOR_OF:
            rows.append([c, n, "2025-07-01", "", "MED/%s" % W.SUCCESSOR_OF[c]])
        else:
            rows.append([c, n, "1972-07-01" if c not in ("EMED", "UROL") else "1989-07-01", "", ""])
    for div, name in W.DIVISION_NAME.items():
        rows.append(["MED/%s" % div, name, "1972-07-01", "2025-06-30", ""])
    rows.sort()
    return _w(path, ["dept_code", "dept_name", "effective_from", "effective_to", "formed_from"], rows)


def write_entities(ents, path):
    rows = [[e["entity_id"], e["name"], e["op_id"], e["type"], e["state"]] for e in ents]
    return _w(path, ["entity_id", "entity_name", "open_payments_id", "entity_type", "state"], rows)


def write_history(events, path):
    rows = [[d, v, ev, t.strftime("%Y-%m-%dT%H:%M:%SZ"), actor] for d, v, ev, t, actor in events]
    return _w(path, ["disclosure_id", "version", "event", "event_time_utc", "actor"], rows)


def write_export(disclosures, items, path):
    """The disclosure system's export: one sheet of disclosures, one of the items of every submitted version."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Disclosures"
    hdr = ["disclosure_id", "emp_id", "disclosure_year", "form_edition", "current_version", "status", "last_submitted_utc"]
    ws.append(hdr)
    for d in sorted(disclosures, key=lambda d: d["disclosure_id"]):
        ws.append([d["disclosure_id"], d["emp_id"], d["year"], d["edition"], d["version"], d["status"],
                   d["last_submitted"].strftime("%Y-%m-%d %H:%M:%S")])
    ws2 = wb.create_sheet("Items")
    ws2.append(["disclosure_id", "version", "item_no", "entity_id", "entity_name", "relationship_type", "amount_usd"])
    for it in sorted(items, key=lambda i: (i["disclosure_id"], i["version"], i["item_no"])):
        ws2.append([it["disclosure_id"], it["version"], it["item_no"], it["entity_id"] or None, it["entity_name"],
                    it["relationship_type"], it["amount"]])
    for s in (ws, ws2):
        for c in s[1]:
            c.font = Font(bold=True)
        s.freeze_panes = "A2"
    widths = {"Disclosures": [16, 10, 15, 13, 15, 22, 20], "Items": [16, 9, 8, 11, 46, 28, 12]}
    for s in (ws, ws2):
        for k, w in enumerate(widths[s.title]):
            s.column_dimensions[chr(65 + k)].width = w
    for row in ws2.iter_rows(min_row=2, min_col=7, max_col=7):
        for c in row:
            c.number_format = "#,##0"
    wb.save(path)
    return len(disclosures), len(items)


def write_research(fac, mfrs, path):
    """Research payments naming faculty as principal investigators (paid to the university): a neighbouring
    Open Payments file the docket does not use."""
    r = np.random.default_rng([W.SEED, 33])
    pis = [f for f in fac if f.cred in ("MD", "DO") and f.dept in ("HEON", "CARD", "NEUR", "GAST", "ORTH", "DERM", "PSYC")]
    rows = []
    rid = 812000000
    for y in W.REGISTER_YEARS:
        for _ in range(170):
            f = pis[int(r.integers(len(pis)))]
            if not (f.holds(D(y, 6, 30)) or f.holds(D(y, 12, 31))):
                continue
            m = mfrs[int(r.integers(len(mfrs)))]
            rid += int(r.integers(1, 400))
            amt = float(np.exp(r.normal(np.log(18000), 1.0)))
            day = D(y, int(r.integers(1, 13)), int(r.integers(1, 29)))
            rows.append(["UNCHANGED", "Covered Recipient Teaching Hospital", W.CCN, W.TEACHING_HOSPITAL_ID, W.HOSPITAL,
                         f.profiles[0], f.npi, f.first, f.last, m["name"], m["id"], _money(amt), day.strftime("%m/%d/%Y"),
                         "Cash or cash equivalent", "Phase %s trial, %s" % (["II", "III", "II", "IV"][int(r.integers(4))], AREAS[f.dept].lower()),
                         "No", str(rid), str(y), "01/15/2027"])
    header = ["Change_Type", "Covered_Recipient_Type", "Teaching_Hospital_CCN", "Teaching_Hospital_ID",
              "Teaching_Hospital_Name", "Principal_Investigator_1_Profile_ID", "Principal_Investigator_1_NPI",
              "Principal_Investigator_1_First_Name", "Principal_Investigator_1_Last_Name",
              "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name",
              "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID", "Total_Amount_of_Payment_USDollars",
              "Date_of_Payment", "Form_of_Payment_or_Transfer_of_Value", "Name_of_Study", "Delay_in_Publication_Indicator",
              "Record_ID", "Program_Year", "Payment_Publication_Date"]
    return _w(path, header, rows)


def write_nih(fac, path):
    """NIH awards with a Marrowfield faculty member as contact PI, fiscal year 2025: a neighbouring file the docket
    does not use."""
    r = np.random.default_rng([W.SEED, 34])
    ics = ["NHLBI", "NCI", "NINDS", "NIDDK", "NIAMS", "NIMH", "NEI", "NIA", "NICHD", "NIAID"]
    pis = [f for f in fac if f.cred in ("MD", "DO") and f.holds(D(2025, 6, 30))]
    rows = []
    for k in range(310):
        f = pis[int(r.integers(len(pis)))]
        ic = ics[int(r.integers(len(ics)))]
        act = str(r.choice(["R01", "R01", "R21", "K23", "K08", "U01", "R34"]))
        num = int(r.integers(100000, 999999))
        amt = int(np.exp(r.normal(np.log(410000), 0.6)))
        rows.append(["%s%s%06d-%02d" % ("1" if r.random() < 0.3 else "5", act, num, int(r.integers(1, 6))), act, ic,
                     "%s, %s" % (f.last.upper(), f.first.upper()), W.ORG.upper(),
                     "MARROWFIELD", "OH", "2025", str(amt)])
    rows.sort(key=lambda x: x[0])
    header = ["project_number", "activity_code", "administering_ic", "contact_pi_name", "organization",
              "org_city", "org_state", "fiscal_year", "total_cost"]
    return _w(path, header, rows)


DICT_FILES = [
    ("open_payments_general_2021-2025_jan2027_extract.csv", "Open Payments general payments for program years 2021 to 2025 as the publication of 15 January 2027 shows them, for the covered recipients the office's extract routine matched to anyone holding a clinical faculty appointment since January 2021. One row per payment record, in the Open Payments layout, with one column the office adds."),
    ("open_payments_general_py2025_jun2026_extract.csv", "The office's extract of program year 2025 as Open Payments first published it on 30 June 2026, pulled on 7 July 2026. Same layout."),
    ("open_payments_covered_recipient_profiles.csv", "Open Payments' covered-recipient profiles for every profile the two extracts carry: one row per profile."),
    ("open_payments_research_2021-2025_extract.csv", "Open Payments research payments naming a clinical faculty member as principal investigator, program years 2021 to 2025 (paid to the university's teaching hospital)."),
    ("clinical_faculty_appointments.csv", "Human resources: every clinical faculty appointment term held since July 2019, one row per term; pulled 20 January 2027."),
    ("department_codes.csv", "The clinical departments and the Department of Medicine's former divisions, with the dates each code was in use."),
    ("coi_entity_list.csv", "The disclosure system's list of companies faculty pick from, with each manufacturer's Open Payments identifier; as of 21 January 2027."),
    ("coi_disclosures_2021-2026_export.xlsx", "The disclosure system's export of every annual disclosure for 2021 to 2026: sheet Disclosures, one row per disclosure; sheet Items, one row per item of every submitted version. Pulled 21 January 2027."),
    ("coi_submission_history.csv", "The disclosure system's submission history: one row per event on a disclosure."),
    ("nih_awards_marrowfield_fy2025.csv", "NIH awards for fiscal year 2025 with a clinical faculty member as contact principal investigator."),
    ("coi_policy_2024.pdf", "Policy RI-14, Conflicts of Interest of the Clinical Faculty (effective 1 July 2024)."),
    ("coi_disclosure_form_guide_2026.pdf", "The office's guide to the 2026 edition of the annual disclosure form."),
    ("oricoi_export_contents_2027-01-21.csv", "The files of this export with their row counts."),
]
DICT_FIELDS = [
    ("open_payments_general_*_extract.csv", "Change_Type", "Whether the record is new, changed or unchanged since the program year's previous publication (NEW, CHANGED, UNCHANGED)."),
    ("open_payments_general_*_extract.csv", "Covered_Recipient_Type", "The kind of covered recipient the record is reported for."),
    ("open_payments_general_*_extract.csv", "Covered_Recipient_Profile_ID", "Open Payments' identifier of the covered recipient the record is reported for; see the profiles file."),
    ("open_payments_general_*_extract.csv", "Covered_Recipient_NPI", "The National Provider Identifier the manufacturer reported for the recipient; blank when it reported none."),
    ("open_payments_general_*_extract.csv", "Covered_Recipient_First_Name / _Middle_Name / _Last_Name", "The recipient's name as the manufacturer reported it."),
    ("open_payments_general_*_extract.csv", "Recipient_Primary_Business_Street_Address_Line1, Recipient_City, Recipient_State, Recipient_Zip_Code", "The recipient's business address as the manufacturer reported it for the payment."),
    ("open_payments_general_*_extract.csv", "Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name", "The company that submitted the record to Open Payments."),
    ("open_payments_general_*_extract.csv", "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID", "Open Payments' identifier of the company making the payment."),
    ("open_payments_general_*_extract.csv", "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name", "The name of the company making the payment, as registered with Open Payments for the program year."),
    ("open_payments_general_*_extract.csv", "Total_Amount_of_Payment_USDollars", "The amount of the payment, in US dollars."),
    ("open_payments_general_*_extract.csv", "Date_of_Payment", "The date of the payment (MM/DD/YYYY); the program year is its calendar year."),
    ("open_payments_general_*_extract.csv", "Number_of_Payments_Included_in_Total_Amount", "How many discrete payments the record's amount combines."),
    ("open_payments_general_*_extract.csv", "Form_of_Payment_or_Transfer_of_Value", "Cash or cash equivalent, in-kind items and services, and the other forms Open Payments lists."),
    ("open_payments_general_*_extract.csv", "Nature_of_Payment_or_Transfer_of_Value", "The nature of the payment as Open Payments categorises it (consulting fee, honoraria, food and beverage, travel and lodging and the others)."),
    ("open_payments_general_*_extract.csv", "Third_Party_Payment_Recipient_Indicator", "Whether the payment was made to a third party at the request of or on behalf of the covered recipient: No Third Party Payment, Entity or Individual."),
    ("open_payments_general_*_extract.csv", "Name_of_Third_Party_Entity_Receiving_Payment_or_Transfer_of_Value", "The entity receiving a third-party payment."),
    ("open_payments_general_*_extract.csv", "Record_ID", "Open Payments' identifier of the record."),
    ("open_payments_general_*_extract.csv", "Program_Year", "The calendar year of the payment."),
    ("open_payments_general_*_extract.csv", "Payment_Publication_Date", "The date of the publication the row comes from."),
    ("open_payments_general_*_extract.csv", "ORICOI_Matched_Emp_ID", "The employee number the office's extract routine attached to the record when it pulled the extract."),
    ("open_payments_covered_recipient_profiles.csv", "Covered_Recipient_Profile_ID", "Open Payments' identifier of the profile."),
    ("open_payments_covered_recipient_profiles.csv", "Covered_Recipient_NPI", "The NPI Open Payments holds for the profile; blank where it holds none."),
    ("clinical_faculty_appointments.csv", "emp_id", "The employee number the term was issued under."),
    ("clinical_faculty_appointments.csv", "npi", "The faculty member's NPI."),
    ("clinical_faculty_appointments.csv", "dept_code, division_code", "The department of the term and, where the department had divisions, the division."),
    ("clinical_faculty_appointments.csv", "appointment_type", "Primary or Secondary; a faculty member holds one primary appointment at a time."),
    ("clinical_faculty_appointments.csv", "term_start, term_end", "The first and last days of the term."),
    ("department_codes.csv", "effective_from, effective_to", "The first and last days the code was in use; blank effective_to: in use."),
    ("department_codes.csv", "formed_from", "The department and division a department was formed from."),
    ("coi_entity_list.csv", "entity_id", "The disclosure system's identifier of the company."),
    ("coi_entity_list.csv", "entity_name", "The company's name on the list today."),
    ("coi_entity_list.csv", "open_payments_id", "The company's Open Payments identifier, as the office recorded it when it added the company to the list; blank where it recorded none."),
    ("coi_entity_list.csv", "entity_type", "Applicable manufacturer or Other company, as the office classed the company when it added it to the list."),
    ("coi_disclosures_2021-2026_export.xlsx: Disclosures", "disclosure_year", "The calendar year the disclosure covers."),
    ("coi_disclosures_2021-2026_export.xlsx: Disclosures", "current_version", "The version in force; each submitted version replaces the items of the one before."),
    ("coi_disclosures_2021-2026_export.xlsx: Disclosures", "status", "The event that put the current version in force: Submitted, Amended or Resubmitted."),
    ("coi_disclosures_2021-2026_export.xlsx: Disclosures", "last_submitted_utc", "When the current version was submitted, in UTC."),
    ("coi_disclosures_2021-2026_export.xlsx: Items", "version", "The version of the disclosure the item belongs to."),
    ("coi_disclosures_2021-2026_export.xlsx: Items", "entity_id", "The company picked from the list; blank when the faculty member typed the name."),
    ("coi_disclosures_2021-2026_export.xlsx: Items", "entity_name", "The company's name as the list showed it when the item was entered, or as typed."),
    ("coi_disclosures_2021-2026_export.xlsx: Items", "relationship_type", "The relationship type of the form edition the disclosure used."),
    ("coi_disclosures_2021-2026_export.xlsx: Items", "amount_usd", "The remuneration received from the company in the calendar year for that kind of service, US dollars."),
    ("coi_submission_history.csv", "event", "Submitted (the first version), Amended, Returned for correction, Resubmitted."),
    ("coi_submission_history.csv", "event_time_utc", "When the event happened, in UTC."),
]


def write_dictionary(path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Files"
    ws.append(["file", "contents"])
    for row in DICT_FILES:
        ws.append(list(row))
    ws2 = wb.create_sheet("Fields")
    ws2.append(["file", "field", "meaning"])
    for row in DICT_FIELDS:
        ws2.append(list(row))
    for s, widths in ((ws, [52, 120]), (ws2, [44, 52, 100])):
        for c in s[1]:
            c.font = Font(bold=True)
        s.freeze_panes = "A2"
        for k, w in enumerate(widths):
            s.column_dimensions[chr(65 + k)].width = w
        for row in s.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    return len(DICT_FIELDS)


def write_manifest(path, n):
    rows = []
    for k, name in FILES.items():
        if k == "manifest":
            continue
        cnt = n.get(k)
        if isinstance(cnt, tuple):
            cnt = "%d disclosures; %d items" % cnt
        rows.append([name, "" if cnt is None else str(cnt), {
            "register": "Open Payments (CMS), publication of 15 January 2027", "register_june": "Open Payments (CMS), publication of 30 June 2026",
            "profiles": "Open Payments (CMS) covered recipient profile supplement", "research": "Open Payments (CMS), publication of 15 January 2027",
            "roster": "Human resources information system", "depts": "Human resources information system", "entities": "COI disclosure system",
            "export": "COI disclosure system", "history": "COI disclosure system", "nih": "NIH RePORTER export",
            "policy": "Board of Trustees", "guide": W.OFFICE, "dict": W.OFFICE}[k],
            {"register": "2027-01-19", "register_june": "2026-07-07", "profiles": "2027-01-19", "research": "2027-01-19",
             "roster": "2027-01-20", "depts": "2027-01-20", "entities": "2027-01-21", "export": "2027-01-21",
             "history": "2027-01-21", "nih": "2026-12-03", "policy": "2024-06-11", "guide": "2026-11-02",
             "dict": "2027-01-21"}[k]])
    return _w(path, ["file", "rows", "source", "pulled_or_issued"], rows)
