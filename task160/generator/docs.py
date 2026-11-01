"""The governing documents and Quillfield's planning and register workbooks, in each organisation's own voice."""
import datetime as dt

import docx
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import io_util as IO
import params as P

BOLD = Font(bold=True)


def _save_xlsx(wb, path, title, creator, company, created, modified):
    wb.properties.creator = creator
    wb.save(path)
    IO.repack_ooxml(path, creator, creator, created, modified, title, company)


def write_plan(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly plan"
    ws.append(["Week beginning", "Department", "Planned admissions", "Planned patient days"])
    for c in ws[1]:
        c.font = BOLD
    for wk, code, pa, pd in rows:
        ws.append([wk, code, pa, pd])
        ws.cell(row=ws.max_row, column=1).number_format = "yyyy-mm-dd"
    ws.column_dimensions["A"].width = 15
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 19
    ws.column_dimensions["D"].width = 21
    ws.freeze_panes = "A2"
    b = wb.create_sheet("Basis")
    for line in ["Quillfield Regional Medical Center, FY2027 inpatient volume plan (1 July 2026 to 30 June 2027)",
                 "Prepared by Finance, Decision Support, 12 June 2026",
                 "Adult inpatient units, planned admissions and patient days by planning week (weeks begin Monday).",
                 "Basis: FY2026 admissions by department with the seasonal profile of FY2025 and FY2026; no service "
                 "openings or closures assumed.",
                 "Planned patient days are planned admissions times each department's FY2026 average length of stay."]:
        b.append([line])
    b.column_dimensions["A"].width = 110
    _save_xlsx(wb, path, "FY2027 inpatient volume plan", "Decision Support", "Quillfield Regional Medical Center",
               "2026-06-12T14:05:00Z", "2026-06-12T16:41:00Z")
    return len(rows)


def write_interventions(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Interventions"
    ws.append(["Date", "Department", "Intervention", "Medication", "Outcome", "Minutes", "Pharmacist"])
    for c in ws[1]:
        c.font = BOLD
    for r in rows:
        ws.append(r)
        ws.cell(row=ws.max_row, column=1).number_format = "mm/dd/yyyy"
    for col, wdt in zip("ABCDEFG", (12, 12, 34, 42, 14, 9, 11)):
        ws.column_dimensions[col].width = wdt
    _save_xlsx(wb, path, "Pharmacist interventions Q3 2026", "Pharmacy Clinical Services",
               "Quillfield Regional Medical Center", "2026-10-05T13:12:00Z", "2026-10-05T13:30:00Z")
    return len(rows)


REGISTER = [
    ("DDI_SEVERE", "Drug-drug interaction, severe", "High",
     "An order is signed for a drug with a severe interaction with an order active for the patient; one alert for "
     "each interacting active order", "Live", "All adult inpatient units", "2019-05-20", "Yes, when overridden"),
    ("DRUG_ALLERGY", "Drug allergy or cross-sensitivity", "High",
     "An order is signed for a drug the patient is recorded as allergic or cross-sensitive to", "Live",
     "All adult inpatient units", "2019-05-20", "Yes, when overridden"),
    ("MAX_DOSE", "Maximum dose exceeded", "High",
     "An order is signed above the maximum single or daily dose for the drug", "Live", "All adult inpatient units",
     "2019-05-20", "Yes, when overridden"),
    ("DDI_MODERATE", "Drug-drug interaction, moderate", "Moderate",
     "An order is signed for a drug with a moderate interaction with an order active for the patient", "Live",
     "All adult inpatient units", "2019-05-20", "No"),
    ("MSP26_DUP_OPIOID_PRN", "Duplicate PRN opioid therapy", "Moderate",
     "A PRN opioid order is signed while another PRN opioid order is active for the patient", "Live",
     "7W, 5E, 8N", "2024-09-09", "No"),
    ("MSP26_DUP_OPIOID_PRN", "Duplicate PRN opioid therapy", "Moderate",
     "A PRN opioid order is signed while another PRN opioid order is active for the patient", "Background",
     "All other adult inpatient units", "2026-07-06", "No"),
    ("MSP26_QT_COMBO", "QT-prolonging drug combination", "High",
     "An order for a drug on the package's QT list is signed while another order for a drug on that list is active "
     "for the patient; one alert for each such active order", "Live", "7W, 5E, 8N", "2024-09-09",
     "Yes, when overridden"),
    ("MSP26_QT_COMBO", "QT-prolonging drug combination", "High",
     "An order for a drug on the package's QT list is signed while another order for a drug on that list is active "
     "for the patient; one alert for each such active order", "Background", "All other adult inpatient units",
     "2026-07-06", "Not displayed in background mode"),
]


def write_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rules"
    ws.append(["Rule ID", "Rule name", "Severity", "Fires when", "Status", "Units", "Since",
               "Sent to override review desk"])
    for c in ws[1]:
        c.font = BOLD
    for r in REGISTER:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2):
        row[3].alignment = Alignment(wrap_text=True, vertical="top")
    for col, wdt in zip("ABCDEFGH", (24, 32, 10, 70, 12, 30, 12, 30)):
        ws.column_dimensions[col].width = wdt
    ws.append([])
    ws.append(["Planned change: CR-2291, both MSP26 rules live on all adult inpatient units from 07:00 on "
               "Monday 4 January 2027."])
    ws.append(["All rules evaluate when an order is signed, against the orders active for the patient at that "
               "moment."])
    u = wb.create_sheet("Units")
    u.append(["Department", "Unit name", "Department name before 9 November 2025"])
    for c in u[1]:
        c.font = BOLD
    for code, name, *_ in P.UNITS:
        u.append([code, name, "QRMC " + name.upper()])
    for col, wdt in zip("ABC", (12, 40, 48)):
        u.column_dimensions[col].width = wdt
    _save_xlsx(wb, path, "Medication alert rule register", "Pharmacy Informatics",
               "Quillfield Regional Medical Center", "2023-02-14T15:20:00Z", "2026-10-26T13:47:00Z")
    return len(REGISTER)


def write_release(path):
    blocks = [
        ("t", "Medication Safety Package MSP26, content release 2026.2"),
        ("s", "Client bulletin for pharmacy informatics teams. Halverson Clinical Content, March 2026."),
        ("h", "1. What the package adds"),
        ("p", "MSP26 adds two rules to the client's medication alert engine. Both are interruptive when live. The "
              "client sets each rule's status by unit: off, background or live."),
        ("table", [["Rule ID", "Rule", "Severity", "Fires when", "Prescriber options"],
                   ["MSP26_DUP_OPIOID_PRN", "Duplicate PRN opioid therapy", "Moderate",
                    "A PRN opioid order is signed while another PRN opioid order is active for the patient.",
                    "Remove the new order; keep both orders (acknowledge)."],
                   ["MSP26_QT_COMBO", "QT-prolonging drug combination", "High",
                    "An order for a drug on the QT list is signed while another order for a drug on the list is "
                    "active for the patient; one alert for each such active order.",
                    "Remove the new order; override with a reason."]]),
        ("h", "2. Drugs in scope"),
        ("p", "PRN opioids: oxycodone, hydromorphone, morphine and hydrocodone combination products, PRN orders "
              "only. QT list, this release: ondansetron, haloperidol, levofloxacin, azithromycin and quetiapine, "
              "with further agents the client's formulary does not stock."),
        ("h", "3. Evaluation"),
        ("p", "MSP26 rules evaluate like every rule in the engine: when an order is signed, against the orders "
              "active for the patient at that moment."),
        ("h", "4. Background mode"),
        ("p", "A rule in background mode evaluates exactly as it would live, and each alert it would have shown "
              "is written to the background log with the order, the interacting order and the evaluation time "
              "(UTC) instead of being displayed. Nothing is shown to the prescriber."),
        ("h", "5. Upgrade notes"),
        ("p", "Release 2026.2 replaces 2025.4. Rule logic for both rules is unchanged; the QT list adds two agents "
              "outside most US formularies."),
    ]
    IO.write_pdf(path, "MSP26 content release 2026.2", "Halverson Clinical Content", "Halverson Content Publisher",
                 blocks, "Halverson Clinical Content, MSP26 release 2026.2 client bulletin", "D:20260316100000-04'00'",
                 "D:20260316100000-04'00'",
                 widths={5: [112, 80, 52, 150, 102]})


def write_schedule(path):
    blocks = [
        ("t", "Schedule B: Override review service (revision 3)"),
        ("s", "To the Remote Pharmacy Services Agreement between Corvane Remote Pharmacy, LLC and Quillfield "
              "Regional Medical Center. Effective 1 July 2026; replaces revision 2."),
        ("h", "1. Scope"),
        ("p", "Corvane's override review desk reviews medication alert overrides for Quillfield's adult inpatient "
              "units, as listed in Quillfield's medication alert rule register. The Emergency Department, "
              "perioperative areas, Labor and Delivery and the Observation Unit are outside this schedule."),
        ("h", "2. Reviews"),
        ("p", "2.1 Every high-severity medication alert that a Quillfield prescriber overrides on an adult inpatient "
              "unit is sent to the desk and reviewed by a Corvane pharmacist. One overridden alert is one review."),
        ("p", "2.2 Alerts answered by removing or modifying the order, and alerts of moderate severity, are not "
              "reviewed."),
        ("p", "2.3 Quillfield's interface opens one queue task for each order on which a prescriber overrides "
              "high-severity alerts at a signing. The task carries every high-severity alert overridden on that "
              "order at that signing, and signing the task off signs off the review of each of them."),
        ("h", "3. Desk hours, time and reporting"),
        ("p", "3.1 The desk works three shifts, Eastern time: day 07:00 to 15:00, evening 15:00 to 23:00 and night "
              "23:00 to 07:00. A review counts in the month and the shift in which a pharmacist signs it off."),
        ("p", "3.2 Desk time is the time a pharmacist has a review open, from claiming it to signing it off or "
              "returning it to the queue. Corvane reports reviews and desk time by the Quillfield department in "
              "which the alert fired."),
        ("h", "4. Volume basis, staffing and fees"),
        ("p", "4.1 Corvane staffs the desk each quarter on a forecast of reviews built on Quillfield's inpatient "
              "volume plan for that quarter."),
        ("p", "4.2 Fees: USD 6.40 for each review; desk time is not billed separately."),
        ("p", "4.3 Content changes. When Quillfield takes a change to its medication alert content, Corvane "
              "re-forecasts the reviews for the first thirteen weeks the change is live on every unit it reaches: "
              "the reviews those units will send with the change live, prescribers answering its alerts as they "
              "have on any unit where it already runs, against the reviews the same units would send over the "
              "same weeks without it. The change order prices the difference at the fee in 4.2."),
        ("h", "5. Service level"),
        ("p", "Each month, 90 per cent of reviews are signed off within 60 minutes of reaching the desk."),
        ("h", "Signed"),
        ("table", [["For Corvane Remote Pharmacy, LLC", "For Quillfield Regional Medical Center"],
                   ["Chris Hernandez, Director of Pharmacy Operations, 18 June 2026",
                    "Andrew Harvey, Chief Pharmacy Officer, 18 June 2026"]]),
    ]
    IO.write_pdf(path, "Schedule B override review service rev 3", "Corvane Remote Pharmacy",
                 "Corvane Contracts", blocks, "Corvane Remote Pharmacy and Quillfield Regional Medical Center, "
                 "Schedule B revision 3", "D:20260618151000-04'00'", "D:20260618151000-04'00'",
                 widths={2: [240, 230]})


def write_cr(path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("Change Request CR-2291", level=1)
    t = d.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in [("Title", "MSP26 medication safety package, hospital-wide go-live"),
                 ("Requested by", "Shawn Whitaker, Pharmacy Informatics Manager, Quillfield Regional Medical Center"),
                 ("Date", "26 October 2026"),
                 ("To", "Corvane Remote Pharmacy, LLC (Chris Hernandez, Director of Pharmacy Operations)"),
                 ("Approved", "Andrew Harvey, Chief Pharmacy Officer, 26 October 2026")]:
        c = t.add_row().cells
        c[0].text, c[1].text = k, v
    d.add_heading("Change", level=2)
    d.add_paragraph("Both MSP26 rules (MSP26_DUP_OPIOID_PRN, duplicate PRN opioid therapy, and MSP26_QT_COMBO, "
                    "QT-prolonging drug combination) go live on every adult inpatient unit at 07:00 on Monday "
                    "4 January 2027. The rules have run live on 7W, 5E and 8N since 9 September 2024 and in "
                    "background mode on the other adult inpatient units since 6 July 2026.")
    d.add_heading("Request to Corvane", level=2)
    d.add_paragraph("Under Schedule B section 4.3, a re-forecast of override reviews for the thirteen weeks from "
                    "Monday 4 January 2027 to Sunday 4 April 2027, and a change order, by 13 November 2026.")
    d.add_heading("Attached", level=2)
    for line in ["Medication alert history, 1 January 2025 to 25 October 2026 (Clarity extract, pulled by quarter)",
                 "MSP26 background log, 6 July to 25 October 2026",
                 "Unit census by day, 1 January 2025 to 25 October 2026",
                 "FY2027 inpatient volume plan (Finance, Decision Support)",
                 "Medication alert rule register as of 26 October 2026"]:
        d.add_paragraph(line, style="List Bullet")
    d.core_properties.author = "Shawn Whitaker"
    d.save(path)
    IO.repack_ooxml(path, "Shawn Whitaker", "Shawn Whitaker", "2026-10-26T13:02:00Z", "2026-10-26T14:15:00Z",
                    "CR-2291 MSP26 hospital-wide go-live", "Quillfield Regional Medical Center")
