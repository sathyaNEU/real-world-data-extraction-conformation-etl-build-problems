"""The pack's documents: the Foundation's grant terms, the hospital's hand hygiene program summary and its hospital-onset
bloodstream infection surveillance definitions (PDF); the workforce team's extract notes and the pack's contents (TXT);
the data dictionary (CSV); the ward and area reference workbook (XLSX)."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import cm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402
import records as R  # noqa: E402
import side as SD    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1b2430"), colors.HexColor("#56616c"), colors.HexColor("#b8c0c8")
PLUM = colors.HexColor("#5a2a52")
TEAL = colors.HexColor("#1d5a57")
NAVY = colors.HexColor("#173b5c")


def styles(face="Sans", accent=NAVY):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.5, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=2,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.4, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=7.9, leading=9.9, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=7.9, leading=9.9, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28),
        bullet=ParagraphStyle("u", parent=body, leftIndent=14, firstLineIndent=-9, spaceAfter=3))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.4)
        canvas.drawString(2.0 * cm, A4[1] - 1.25 * cm, left)
        canvas.drawRightString(A4[0] - 2.0 * cm, A4[1] - 1.25 * cm, right)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.1 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject, left, right):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=2.0 * cm,
                             bottomMargin=1.9 * cm, title=title, author=author, subject=subject, creator=author,
                             producer=author), _frame(left, right)


# ------------------------------------------------------------------------------------------------ the grant's terms
def write_terms(path):
    S = styles("Serif", PLUM)
    doc, fr = _doc(path, "%s: terms" % K.GRANT, K.FOUNDATION, "Grant terms", K.FOUNDATION, "%s: terms" % K.GRANT)
    st = [Paragraph(K.GRANT, S["h1"]),
          Paragraph("Terms adopted by the board of the %s on 22 September 2026. Grants manager: %s." %
                    (K.FOUNDATION, K.PEOPLE["grants"]), S["meta"]),
          Paragraph("1. Purpose", S["h2"]),
          _clause(S, "1.1", "The Foundation funds a hand hygiene coaching nurse, one full-time position for twelve "
                            "months, on each ward of %s where staff performed hand hygiene least reliably. The "
                            "coach works on the ward's day shifts beside its nurses, doctors and other staff, "
                            "coaching hand hygiene at the bedside." % K.HOSPITAL),
          _clause(S, "1.2", "Coaching nurses start on 1 February 2027. The positions are additional to the ward's "
                            "nursing establishment and are not counted in its nursing hours."),
          Paragraph("2. The wards funded", S["h2"]),
          _clause(S, "2.1", "A ward is funded when its staff performed hand hygiene at fewer than 80 per cent of the "
                            "hand hygiene moments that arose on its AM and PM shifts in the 2025-26 audit year, 1 July "
                            "2025 to 30 June 2026. The 80 per cent line is the national benchmark for hand hygiene "
                            "compliance."),
          _clause(S, "2.2", "The moments are the five moments for hand hygiene, as the national program defines "
                            "them, on every AM and PM shift of the year. A ward's moments on a shift are taken in "
                            "proportion to the care hours its patients required on that shift, as the hospital's "
                            "patient acuity system assessed them."),
          _clause(S, "2.3", "Hand hygiene was performed at a moment when it was done by hand rub or hand wash. The "
                            "hospital's gold-auditor sessions are the record of the moments observed."),
          _clause(S, "2.4", "The Foundation funds at most six coaching nurses in 2027, one on each funded ward."),
          Paragraph("3. Evaluation", S["h2"]),
          _clause(S, "3.1", "The Foundation evaluates the grant on three outcome measures for every ward, funded or "
                            "not: hospital-onset bloodstream infections per 10,000 occupied bed days, as the "
                            "hospital's infection prevention and control service defines them, and alcohol-based hand "
                            "rub and liquid hand soap used per 1,000 occupied bed days, as the hospital's hand hygiene "
                            "program measures them."),
          _clause(S, "3.2", "The application gives the three measures for every ward for the 2025-26 audit year, the "
                            "grant's baseline."),
          Paragraph("4. Timetable", S["h2"]),
          _clause(S, "4.1", "The Foundation's board approves its 2027 grants budget on 8 December 2026."),
          _clause(S, "4.2", "Funded wards report their coaching activity to the grants manager each quarter.")]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ the program
def write_program(path):
    S = styles("Sans", TEAL)
    doc, fr = _doc(path, "Hand Hygiene Program 2025-26", K.PEOPLE["ipc"], "Infection prevention and control",
                   "%s, Infection Prevention and Control" % K.HOSPITAL, "Hand Hygiene Program 2025-26")
    moments = ["Moment 1, before touching a patient", "Moment 2, before a procedure",
               "Moment 3, after a procedure or body fluid exposure risk", "Moment 4, after touching a patient",
               "Moment 5, after touching a patient's surroundings"]
    st = [Paragraph("Hand Hygiene Program 2025-26", S["h1"]),
          Paragraph("%s, Infection Prevention and Control Service. Program summary for the 2025-26 audit year, "
                    "issued 14 July 2026 by %s, Clinical Nurse Consultant." % (K.HOSPITAL, K.PEOPLE["ipc"]), S["meta"]),
          Paragraph("1. The program", S["h2"]),
          Paragraph("The hospital takes part in the national hand hygiene program. Compliance is measured by direct "
                    "observation against the five moments for hand hygiene, by gold auditors trained and validated "
                    "under the national program, and reported against the national benchmark of 80 per cent. The "
                    "audit year runs from 1 July to 30 June.", S["body"]),
          Paragraph("2. The five moments", S["h2"])]
    st += [Paragraph("&bull;&nbsp;&nbsp;" + m, S["bullet"]) for m in moments]
    st += [Paragraph("3. Gold auditors and sessions", S["h2"]),
           Paragraph("Each ward and department has its own gold auditors, nurses and other clinicians from its staff "
                     "who have completed gold auditor training and annual validation. In a session the auditor "
                     "observes the moments that arise in view for about twenty minutes and records each one: which "
                     "moment it was, the health care worker group of the person it belonged to, and whether hand "
                     "hygiene was performed by hand rub or by hand wash or was missed. Each ward aims to audit at "
                     "least 100 moments a month.", S["body"]),
           Paragraph("Sessions are entered in the hand hygiene audit application on a tablet at the end of the "
                     "session. The application was unavailable from 9 to 20 March 2026; sessions in those days were "
                     "recorded on the paper form and entered by their auditors when it returned.", S["body"]),
           Paragraph("4. Health care worker groups", S["h2"]),
           _table(S, [["National group", "Includes"],
                      ["Nurse/Midwife", "Registered and enrolled nurses and midwives"],
                      ["Medical", "Medical officers of every grade"],
                      ["Allied health", "Physiotherapists, occupational therapists, dietitians, pharmacists, "
                                        "radiographers and other allied health staff"],
                      ["Personal care staff", "Assistants in nursing and patient care assistants"],
                      ["Support services", "Ward support, cleaning, catering and transport staff"],
                      ["Student", "Nursing, medical and allied health students on placement"]], [4.0, 12.8]),
           Paragraph("5. Hand rub and hand soap use", S["h2"]),
           Paragraph("Alcohol-based hand rub use is reported to the program's quarterly review as the litres of hand "
                     "rub put out on a ward per 1,000 occupied bed days. The litres are those of the bottles the "
                     "store issues to the ward's cost centre (500 mL pump bottles and cartons of 24 personal 100 mL "
                     "bottles), less bottles returned to the store, and of the 1 litre refills the cleaning "
                     "contractor fits to the ward's wall dispensers on its dispenser rounds. Liquid hand soap use is "
                     "reported the same way: the litres of the 500 mL soap pump bottles the store issues to the "
                     "ward's cost centre, less returns, and of the 800 mL cartridges the contractor fits to the soap "
                     "dispensers at the ward's sinks. Occupied bed days are the midnight census's occupied beds "
                     "summed over the days of the period.", S["body"]),
           Paragraph("6. Reporting", S["h2"]),
           Paragraph("Ward results are reported each quarter to the ward's nurse unit manager and to the hospital's "
                     "infection prevention committee, and the hospital's results to the national program three "
                     "times a year.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ surveillance definitions
def write_definitions(path):
    S = styles("Sans", NAVY)
    doc, fr = _doc(path, "Hospital-onset bloodstream infection surveillance: definitions", K.PEOPLE["ipc"],
                   "Infection prevention and control", "%s, Infection Prevention and Control" % K.HOSPITAL,
                   "HOBSI surveillance definitions, version 3")
    st = [Paragraph("Hospital-onset bloodstream infection surveillance: definitions", S["h1"]),
          Paragraph("Version 3, effective 1 July 2025. Infection Prevention and Control Service, %s. Replaces "
                    "version 2 (2022)." % K.HOSPITAL, S["meta"]),
          _clause(S, "1", "Scope. Inpatients of the hospital's wards. Patients seen in the emergency department, "
                          "clinics, day units and the renal dialysis unit who are not admitted are outside "
                          "surveillance."),
          _clause(S, "2", "Positive blood culture. A recognised pathogen grown from at least one blood culture set; "
                          "or a common commensal grown from two or more blood culture sets collected within 48 hours "
                          "of each other. A common commensal grown from a single set is a contaminant and is not an "
                          "infection."),
          _clause(S, "3", "Hospital onset. An episode is hospital onset when its first positive blood culture was "
                          "collected more than 48 hours after the patient was admitted to the hospital. A culture "
                          "collected before admission or within 48 hours of it is community onset."),
          _clause(S, "4", "Episodes. A further positive blood culture with the same organism collected less than 14 "
                          "days after the episode's first positive culture belongs to that episode. The same "
                          "organism 14 days or more after it begins a new episode."),
          _clause(S, "5", "Attribution. An episode is attributed to the ward the patient was on when its first "
                          "positive blood culture was collected."),
          _clause(S, "6", "Rate. Hospital-onset bloodstream infections per 10,000 occupied bed days, the occupied bed "
                          "days from the patient administration system's midnight census."),
          Paragraph("Common commensals", S["h2"]),
          Paragraph("Coagulase-negative staphylococci (including <i>Staphylococcus epidermidis</i> and "
                    "<i>Staphylococcus hominis</i>), <i>Micrococcus</i> species, <i>Corynebacterium</i> species "
                    "(diphtheroids), <i>Cutibacterium</i> species, <i>Bacillus</i> species other than <i>B. "
                    "anthracis</i>, and viridans group streptococci.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ extract notes
def write_notes(path, counts):
    out = ["WORKFORCE INFORMATION: EXTRACT NOTES",
           "Request WI-26-0418, acuity and roster actuals 2025-26 (requested by %s, Infection Prevention and"
           % K.PEOPLE["ipc"],
           "Control, for the %s application)" % K.GRANT,
           "Extracted by %s, 3 November 2026" % K.PEOPLE["workforce"],
           "Files: acuity_patient_shifts_2025_26.csv (%s rows), nursing_roster_actuals_2025_26.csv (%s rows)"
           % ("{:,}".format(counts["acuity"]), "{:,}".format(counts["roster"])),
           "",
           "1. acuity_patient_shifts_2025_26.csv",
           "One row per patient per AM or PM shift on each inpatient ward, 1 July 2025 to 30 June 2026, from the",
           "patient acuity system. required_care_hours is the direct nursing care the patient was assessed to need",
           "over the shift, entered by the nurse in charge at the start of the shift and updated if the patient's",
           "condition changed. Patients in escalation spaces (corridor and chair spaces opened when a ward is over",
           "its beds) are rated like any other patient; their bed codes end ESC1, ESC2 and so on.",
           "",
           "2. nursing_roster_actuals_2025_26.csv",
           "One row per nurse per shift worked on each ward, from the rostering system after timesheet approval.",
           "Shifts are AM 07:00 to 15:30, PM 13:00 to 21:30 and night 21:00 to 07:30, each with a 30 minute unpaid",
           "meal break; part shifts are 4 hours. worked_hours are the paid hours. The two night shifts over the",
           "daylight saving changes (4 October 2025 and 4 April 2026) were 9 and 11 hours.",
           "Shifts worked by the hospital's casual pool nurses carry their employee numbers like any other.",
           "Rows whose shift_category begins Supernumerary are orientation, clinical education and student",
           "placement shifts. They are not counted in a ward's nursing hours.",
           "",
           "3. Ward 6A",
           "Ward 6A (Orthopaedics) moved to the new surgical block on 2 February 2026 and carries the code S1A in",
           "both systems from that date. Its beds and staff moved with it.",
           ""]
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(out))


# ------------------------------------------------------------------------------------------------ dictionary
DICTIONARY = [
    ("audits", "session_id", "The audit application's session number, given when the session is saved."),
    ("audits", "session_date", "Date of the session (day/month/year)."),
    ("audits", "session_start", "Time the session began (24-hour clock, local time)."),
    ("audits", "department", "The ward or department audited, as the audit application names it."),
    ("audits", "auditor", "The gold auditor's code in the audit application."),
    ("audits", "moment_seq", "Order of the moment within the session."),
    ("audits", "moment", "Which of the five moments for hand hygiene."),
    ("audits", "hcw_category", "Health care worker group of the person the moment belonged to, as the application "
                               "lists it."),
    ("audits", "action", "Hand rub, Hand wash or Missed."),
    ("acuity", "ward", "Ward code."),
    ("acuity", "shift_date", "Date of the shift (year-month-day)."),
    ("acuity", "shift", "AM or PM."),
    ("acuity", "bed", "Bed or escalation space."),
    ("acuity", "encounter", "The patient's encounter number in the acuity system."),
    ("acuity", "required_care_hours", "Direct nursing care hours the patient was assessed to need over the shift."),
    ("roster", "roster_date", "Date the shift began (day/month/year)."),
    ("roster", "ward", "Ward code."),
    ("roster", "shift_code", "AM, PM or ND (night)."),
    ("roster", "staff_key", "Employee number; for a student on placement, the university's student number."),
    ("roster", "staff_type", "Employee or Placement."),
    ("roster", "designation", "RN registered nurse, EN enrolled nurse, AIN assistant in nursing, Student."),
    ("roster", "shift_start", "Rostered start time."),
    ("roster", "shift_end", "Rostered end time."),
    ("roster", "worked_hours", "Paid hours of the shift."),
    ("roster", "shift_category", "Rostered, or the kind of supernumerary shift."),
    ("isolates", "lab_number", "Laboratory accession number of the blood culture set."),
    ("isolates", "mrn", "The patient's medical record number on the request."),
    ("isolates", "date_of_birth", "Patient's date of birth (day/month/year)."),
    ("isolates", "sex", "Patient's sex."),
    ("isolates", "collected", "Date and time the blood culture set was collected."),
    ("isolates", "received", "Date and time the laboratory received it."),
    ("isolates", "location", "The ward or department on the request."),
    ("isolates", "specimen", "Specimen type."),
    ("isolates", "organism", "Organism grown."),
    ("admissions", "admission_no", "Admission number."),
    ("admissions", "mrn", "The patient's medical record number."),
    ("admissions", "date_of_birth", "Patient's date of birth (day/month/year)."),
    ("admissions", "sex", "Patient's sex."),
    ("admissions", "admitted", "Date and time the admission began."),
    ("admissions", "admitting_ward", "Ward of the patient at the start of the admission."),
    ("admissions", "separated", "Date and time the admission ended."),
    ("admissions", "separation_ward", "Ward of the patient at the end of the admission."),
    ("transfers", "admission_no", "Admission number."),
    ("transfers", "transfer_seq", "Order of the transfer within the admission."),
    ("transfers", "from_ward", "Ward the patient moved from."),
    ("transfers", "to_ward", "Ward the patient moved to."),
    ("transfers", "transferred", "Date and time the patient moved."),
    ("census", "census_date", "Date of the census (year-month-day)."),
    ("census", "ward", "Ward code."),
    ("census", "occupied_beds", "Inpatients in a bed or escalation space on the ward at midnight at the end of "
                                "census_date."),
    ("issues", "issue_no", "Store transaction number."),
    ("issues", "issue_date", "Date of the transaction (day/month/year)."),
    ("issues", "transaction", "ISSUE, or RETURN for stock returned to the store."),
    ("issues", "cost_centre", "Cost centre charged."),
    ("issues", "cost_centre_name", "Cost centre name."),
    ("issues", "item_code", "Store item code."),
    ("issues", "item_description", "Store item description."),
    ("issues", "unit_of_issue", "EA each, CTN carton."),
    ("issues", "quantity", "Quantity in units of issue; negative for a return."),
    ("rounds", "record_id", "The contractor's record number, given when the handheld synchronises."),
    ("rounds", "handheld", "The handheld that recorded the refill."),
    ("rounds", "job_no", "Work order of a job raised outside the scheduled rounds (terminal cleans); blank on a scheduled round."),
    ("rounds", "dispenser_id", "The dispenser's asset number."),
    ("rounds", "fitted", "Date and time of the refill, as the handheld recorded it."),
    ("rounds", "product", "Refill or cartridge fitted."),
    ("rounds", "quantity", "Quantity, as the handheld recorded it."),
    ("rounds", "cleaner", "The cleaner's code."),
    ("survey", "ward", "Ward code."),
    ("survey", "survey_month", "Month of discharge."),
    ("survey", "responses", "Patients who answered the hand hygiene question."),
    ("survey", "hand_hygiene_yes", "Answered yes to: did staff clean their hands before touching you?"),
    ("survey", "hand_hygiene_no", "Answered no."),
    ("survey", "hand_hygiene_dont_know", "Answered don't know."),
    ("flu", "employee_no", "Employee number."),
    ("flu", "home_ward", "The employee's home ward."),
    ("flu", "vaccinated_on", "Date of the 2025 influenza vaccination; blank if not vaccinated in the program."),
]


def write_dictionary(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["file_name", "field_name", "source_system", "data_type", "description"])
        for k, fld, desc in DICTIONARY:
            w.writerow([K.FILES[k], fld, SYSTEM[k], _dtype(k, fld), desc])
        for sheet, desc in (("Wards", "One row per inpatient ward code: name, specialty, beds, floor, cost centre, "
                                      "audit application department, laboratory location."),
                            ("Areas", "One row per other audited area."),
                            ("Dispensers", "One row per wall dispenser: the ward or area it serves, floor, "
                                           "hand rub or hand soap, installed and removed dates.")):
            w.writerow([K.FILES["wards"], "sheet " + sheet, "Reference workbook", "sheet", desc])


SYSTEM = {"audits": "Hand hygiene audit application", "acuity": "Patient acuity system", "roster": "Rostering system",
          "isolates": "Laboratory information system", "admissions": "Patient administration system",
          "transfers": "Patient administration system", "census": "Patient administration system",
          "issues": "Store inventory system", "rounds": "Contractor handheld system",
          "survey": "Patient experience survey", "flu": "Staff health"}
NUMERIC = {("audits", "moment_seq"): "integer", ("acuity", "required_care_hours"): "decimal(4,1)",
           ("roster", "worked_hours"): "decimal(5,2)", ("admissions", "admission_no"): "char(9)",
           ("transfers", "transfer_seq"): "integer", ("census", "occupied_beds"): "integer",
           ("issues", "quantity"): "integer", ("rounds", "quantity"): "integer", ("survey", "responses"): "integer",
           ("survey", "hand_hygiene_yes"): "integer", ("survey", "hand_hygiene_no"): "integer",
           ("survey", "hand_hygiene_dont_know"): "integer"}


def _dtype(k, fld):
    if (k, fld) in NUMERIC:
        return NUMERIC[(k, fld)]
    if fld in ("collected", "received", "admitted", "separated", "transferred", "fitted"):
        return "datetime"
    if fld.endswith("_date") or fld in ("date_of_birth", "vaccinated_on", "survey_month"):
        return "date"
    if fld in ("session_start", "shift_start", "shift_end"):
        return "time"
    return "text"


# ------------------------------------------------------------------------------------------------ reference workbook
def _style_sheet(sh, widths=None, fill="1D5A57"):
    from openpyxl.styles import Alignment, Font, PatternFill
    for cell in sh[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    sh.freeze_panes = "B2"
    for col in sh.columns:
        letter_ = col[0].column_letter
        if widths and letter_ in widths:
            sh.column_dimensions[letter_].width = widths[letter_]
        else:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col[:200])
            sh.column_dimensions[letter_].width = min(46, max(8, width + 2))


def write_wards(path, side):
    import openpyxl
    floor_of = {u: fl for fl, units in SD.FLOORS.items() for u in units}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Wards"
    ws.append(["code", "ward", "specialty", "beds", "floor", "cost_centre", "audit_application_department",
               "laboratory_location", "notes"])
    for code, name, spec, beds, *_ in K.WARDS:
        note = None
        if code == K.MOVED[0]:
            note = "Moved to the surgical block on 2 February 2026; code S1A from that date."
        ws.append([code, name, spec, beds, "Level " + floor_of[code] if floor_of[code] != "G" else "Ground",
                   R.COST_CENTRE[code][0], R.APP_DEPT[code], R.LAB_LOC[code], note])
        if code == K.MOVED[0]:
            ws.append([K.MOVED[1], "Ward S1A", spec, beds, "Surgical Block Level 1", R.COST_CENTRE[code][0],
                       R.APP_DEPT[K.MOVED[1]], R.LAB_LOC[K.MOVED[1]], "Ward 6A from 2 February 2026."])
    _style_sheet(ws, {"I": 60})
    wa = wb.create_sheet("Areas")
    wa.append(["code", "area", "floor", "audit_application_department", "laboratory_location"])
    for code, name in K.AREAS:
        fl = floor_of[code]
        wa.append([code, name, {"G": "Ground", "S1": "Surgical Block Level 1"}.get(fl, "Level " + fl),
                   R.APP_DEPT[code], R.LAB_LOC[code]])
    _style_sheet(wa)
    wd = wb.create_sheet("Dispensers")
    wd.append(["dispenser_id", "ward_or_area", "floor", "type", "installed", "removed"])
    for did, u, fl, f, t in side.dispensers:
        wd.append([did, u, {"G": "Ground", "S1": "Surgical Block Level 1"}.get(fl, "Level " + fl),
                   side.disp_type[did], f.strftime("%d/%m/%Y"), t.strftime("%d/%m/%Y") if t else None])
    _style_sheet(wd)
    wb.save(path)


def write_contents(path, items):
    out = ["%s: %s, application pack" % (K.HOSPITAL, K.GRANT),
           "Assembled %s by %s, Infection Prevention and Control, for the %s." %
           (K.ASSEMBLED.strftime("%d %B %Y").lstrip("0"), K.PEOPLE["ipc"], K.FOUNDATION), ""]
    for name, desc in items:
        out.append(name)
        out.append("    " + desc)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(out) + "\n")
