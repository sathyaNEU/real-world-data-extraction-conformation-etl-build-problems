"""The pack's documents and workbooks: the measure specification, the Office of Vital Records' methods note, the claims
extract notes, Carrisford's encounter file layout, the risk scores workbook, and the two distractors (the quality
dashboard's readmissions and the network hospital profiles)."""
import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
TEAL = colors.HexColor("#0f5c63")
NAVY = colors.HexColor("#1f3a5f")
OXBLOOD = colors.HexColor("#6b2230")
SLATE = colors.HexColor("#3d4a57")
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.3, leading=10.8, textColor=GREY)


def styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.3, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    return h1, h1s, h2


def _doc(path, title, author, footer, layout="left"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        if layout == "left":
            canvas.setFont("LiberationSans", 7.5)
            canvas.drawString(0.9 * inch, 0.6 * inch, footer)
            canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        elif layout == "centre":
            canvas.setFont("LiberationSerif", 8.5)
            canvas.drawCentredString(letter[0] / 2, 0.6 * inch, "%s, page %d" % (footer, doc.page))
        else:
            canvas.setFont("LiberationSans", 8)
            canvas.drawString(0.9 * inch, letter[1] - 0.55 * inch, footer)
            canvas.setStrokeColor(GREY)
            canvas.setLineWidth(0.5)
            canvas.line(0.9 * inch, letter[1] - 0.6 * inch, letter[0] - 0.9 * inch, letter[1] - 0.6 * inch)
            canvas.drawCentredString(letter[0] / 2, 0.55 * inch, str(doc.page))
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e6eef0", font=None):
    data = [[Paragraph(str(v), CELLB if i == 0 else (font or CELL)) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


# ---------------------------------------------------------------------------------------- the measure specification
def write_spec(path):
    h1, h1s, h2 = styles(NAVY)
    d, frame = _doc(path, "Hospital Quality Bonus, contract year 2027: measure specification", W.PLAN,
                    W.PLAN + "  |  Provider Contracting and Payment  |  HQB 2027 measure specification v1.0")
    hosp = [["", "Network hospital"]] + [[str(i + 1), h[0]] for i, h in enumerate(W.HOSPITALS)]
    s = [Paragraph("Hospital Quality Bonus, contract year 2027", h1),
         Paragraph("Measure specification: 30-day mortality after admission, measurement year fiscal 2026 (July 1, "
                   "2025 to June 30, 2026). Version 1.0, approved May 12, 2025 by %s, %s." % (
                       W.PEOPLE["vp"], W.TITLES["vp"]), h1s),
         Paragraph("1. The bonus", h2),
         Paragraph("1.1 Each network hospital's services agreement with Halbrook Community Health Plan provides for a "
                   "Hospital Quality Bonus in contract year 2027 (January 1 to December 31, 2027): 2 per cent added to "
                   "the inpatient payments Halbrook makes to the hospital, unless the hospital's mortality ratio for "
                   "the measurement year, as this specification defines it, exceeds 1.15.", SANS),
         Paragraph("1.2 The measurement year is Halbrook's fiscal 2026, July 1, 2025 to June 30, 2026. The determination "
                   "is filed with the state as part of Halbrook's value-based payment arrangements for 2027, due "
                   "November 1, 2026.", SANS),
         Paragraph("2. Index admissions", h2),
         Paragraph("2.1 An index admission is an inpatient admission of a Halbrook member to one of the network "
                   "hospitals in Exhibit A with an admission date from July 1, 2025 to June 30, 2026, whether the stay "
                   "was paid by Halbrook or by a delegated medical group and reported to Halbrook as an encounter. A "
                   "stay is taken as last corrected; a bill or encounter that was voided or deleted is not a stay.",
                   SANS),
         Paragraph("2.2 These admissions are not index admissions: (a) an admission of a member younger than 18 on the "
                   "admission date; (b) an admission for an obstetric delivery (MS-DRGs 768, 783 to 788, 796 to 798 "
                   "and 805 to 807); (c) an admission ending in a discharge against medical advice (patient status "
                   "07).", SANS),
         Paragraph("2.3 A member has at most one index admission: the member's first admission in the measurement year "
                   "that 2.1 and 2.2 allow. The member's later admissions are not index admissions.", SANS),
         Paragraph("2.4 When a member is discharged from a network hospital to another acute-care hospital (patient "
                   "status 02) and admitted there on the day of discharge or the next day, the two stays are one index "
                   "admission. It belongs to the hospital that first admitted the member, and its admission date is "
                   "that hospital's admission date.", SANS),
         Paragraph("3. Deaths", h2),
         Paragraph("3.1 An index admission ends in death when the member died, from any cause, on or before the 30th "
                   "day after the admission date (the admission date is day 0), in hospital or after discharge.", SANS),
         Paragraph("3.2 A hospital's deaths are the number of its index admissions that end in death. The last index "
                   "admissions' 30 days run to July 30, 2026.", SANS),
         Paragraph("3.3 Halbrook learns of deaths from the hospitals' bills and the delegated group's encounters "
                   "(patient status 20) and from the state Office of Vital Records, which links Halbrook members to the "
                   "state's death records each year for this measure.", SANS),
         Paragraph("4. Expected deaths", h2),
         Paragraph("4.1 An index admission's expected probability of death is the score that the Halbrook Inpatient "
                   "Mortality Model, version 3.2 (HIMM 3.2), gives the admission in Halbrook Analytics' scores file for "
                   "fiscal 2026 admissions.", SANS),
         Paragraph("4.2 A hospital's expected deaths are the sum of its index admissions' scores.", SANS),
         Paragraph("5. The ratio and the determination", h2),
         Paragraph("5.1 A hospital's mortality ratio is its deaths divided by its expected deaths.", SANS),
         Paragraph("5.2 A network hospital whose mortality ratio exceeds 1.15 does not receive the 2027 Hospital "
                   "Quality Bonus. Every other network hospital receives it.", SANS),
         Paragraph("5.3 Halbrook states each hospital's bonus at stake in its notice to the hospital and in the 2027 "
                   "budget as 2 per cent of the payments Halbrook made to the hospital for inpatient stays discharged "
                   "in the measurement year. Stays of members whose care is delegated to a medical group are paid by "
                   "the group under its own agreement and are not payments Halbrook made.", SANS),
         Paragraph("Exhibit A. Network hospitals", h2),
         _table(hosp, [0.4 * inch, 4.6 * inch]),
         Spacer(1, 6),
         Paragraph("Questions on this specification go to Quality Measurement, Provider Contracting and Payment.",
                   SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------- the linkage methods note
def write_linknote(path, n_sent, n_linked):
    h1, h1s, h2 = styles(SLATE, serif=True)
    d, frame = _doc(path, "Death record linkage for Halbrook Community Health Plan, fiscal 2026 admissions",
                    "Office of Vital Records", "Office of Vital Records, Linkage Unit", layout="centre")
    s = [Paragraph("Office of Vital Records, Linkage Unit", h1s),
         Paragraph("Death record linkage for Halbrook Community Health Plan: inpatient admissions, July 1, 2025 to "
                   "June 30, 2026", h1),
         Paragraph("Methods note to accompany the return file of October 7, 2026. %s, %s." % (
             W.PEOPLE["linkage"], W.TITLES["linkage"].replace(", State Office of Vital Records", "")), h1s),
         Paragraph("What we received", h2),
         Paragraph("On October 1, 2026 Halbrook sent %s records under its data use agreement with the Office: one "
                   "record for each inpatient admission of a member aged 18 or older at one of its network hospitals "
                   "with an admission date from July 1, 2025 to June 30, 2026, giving the member's Halbrook identifier, "
                   "name, date of birth and sex, the member's Social Security number where Halbrook holds one, and "
                   "the admission date." % "{:,}".format(n_sent), SERIF),
         Paragraph("How we searched", h2),
         Paragraph("Each record was searched against the deaths that occurred in the state from its admission date "
                   "through the 30th day after it, as registered with the Office by September 30, 2026.", SERIF),
         Paragraph("Pass 1 matched records that carry a Social Security number to death records on the number, date "
                   "of birth and sex. Pass 2 took every record not linked in pass 1, including every record without a "
                   "number, and compared it with the death records on first name, last name, date of birth and sex, "
                   "scoring each candidate pair with the Unit's standard probabilistic weights; a pair scoring above "
                   "the Unit's threshold is linked. Where more than one death record scored above the threshold, the "
                   "highest-scoring pair was kept.", SERIF),
         Paragraph("What the return contains", h2),
         Paragraph("The return file lists the %s records we linked, one row each: Halbrook's member identifier and the "
                   "admission date as Halbrook sent them, the state file number of the death certificate, the date of "
                   "death and the pass that made the link. A death is listed against each of a member's records whose "
                   "30 days it falls in. Records not listed were searched and not linked." % "{:,}".format(n_linked),
                   SERIF),
         Paragraph("As with any linkage that relies on names and dates of birth, some deaths of plan members are not "
                   "found and some members are linked to a death that is not theirs.", SERIF),
         Paragraph("Use of the return", h2),
         Paragraph("State file numbers are confidential and may be used only to measure outcomes under the data use "
                   "agreement. Copies of death certificates are not released under the agreement.", SERIF)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------------- the claims notes
def write_claimnotes(path):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Inpatient claims extract IP_CLM: notes", W.PLAN,
                    "Halbrook Enterprise Data Warehouse  |  IP_CLM extract notes  |  extract of October 5, 2026",
                    layout="top")
    cols = [["Column", "Contents"],
            ["claim_number", "Halbrook's claim number for the bill"],
            ["type_of_bill", "UB-04 type of bill: 0111 admit through discharge, 0117 replacement of a prior claim, "
                             "0118 void or cancel of a prior claim"],
            ["original_claim_number", "On a 0117 or 0118 bill, the claim it replaces or cancels; blank otherwise"],
            ["member_id", "Halbrook member identifier (nine digits)"],
            ["billing_npi", "The hospital's billing NPI on the bill"],
            ["admission_date", "Date of admission"],
            ["statement_from_date, statement_thru_date", "The period the bill covers; on a bill closing the stay the "
                                                         "through date is the discharge date"],
            ["admission_type", "1 emergency, 2 urgent, 3 elective, 4 newborn"],
            ["patient_status", "UB-04 patient discharge status: 01 home or self care, 02 short-term general "
                               "hospital, 03 skilled nursing facility, 06 home health, 07 left against medical "
                               "advice, 20 expired"],
            ["drg", "MS-DRG as grouped by Halbrook (version 42)"],
            ["principal_dx", "Principal diagnosis, ICD-10-CM, without the decimal point"],
            ["paid_date", "Date the bill was adjudicated and paid"],
            ["paid_amount", "Amount Halbrook paid on the bill, in dollars"]]
    s = [Paragraph("Inpatient claims extract IP_CLM", h1),
         Paragraph("Halbrook Community Health Plan, Enterprise Data Warehouse. Extract of October 5, 2026, prepared for "
                   "Quality Measurement.", h1s),
         Paragraph("Scope", h2),
         Paragraph("Every inpatient bill (type of bill 011x) that Halbrook paid to one of its fourteen network "
                   "hospitals for a stay with a statement-through date from July 1, 2025, paid through September 30, "
                   "2026, one row per bill. Members of every age and stays of every kind are included. Stays of members "
                   "delegated to Carrisford Medical Group are paid by Carrisford and are not in this extract; "
                   "Carrisford submits them to Halbrook as encounters.", SANS),
         Paragraph("Columns", h2),
         _table(cols, [1.9 * inch, 4.8 * inch]),
         Paragraph("Claims platform", h2),
         Paragraph("On January 1, 2026 Halbrook moved claims adjudication from its former system (CPS) to its new "
                   "platform. Bills adjudicated before that date were converted into the warehouse with their CPS claim "
                   "numbers (13 digits); bills adjudicated from that date carry platform numbers (HC followed by ten "
                   "digits). A bill keeps the number it was adjudicated under, so a replacement or void adjudicated in "
                   "2026 can point to a CPS claim.", SANS),
         Paragraph("The two systems record a replacement and a void differently, and paid_amount keeps what the system "
                   "that adjudicated the bill recorded. A replacement (0117) with a CPS number carries the change CPS "
                   "made to the payment, negative where the payment went down; one with a platform number carries the "
                   "stay's full payment. A void (0118) carries the payment it reverses, as a positive amount on a CPS "
                   "void and a negative amount on a platform void.", SANS),
         Paragraph("Other notes", h2),
         Paragraph("Mercy Valley Medical Center bills under a new NPI from January 1, 2026; the network hospital list "
                   "gives both. Dates are written YYYY-MM-DD. The extract has a header row and no trailer.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------- Carrisford's file layout
def write_layout(path):
    h1, h1s, h2 = styles(OXBLOOD)
    d, frame = _doc(path, "Inpatient encounter submission file, layout version 4", W.GROUP,
                    W.GROUP + "  |  Encounter Operations  |  IP encounter layout v4")
    rec = [["#", "Field", "Contents"],
           ["1", "REC_TYPE", "D"],
           ["2", "ENC_ID", "Carrisford's encounter identifier"],
           ["3", "FREQ", "1 original, 7 replacement of a prior encounter, 8 deletion of a prior encounter"],
           ["4", "ORIG_ENC_ID", "On a 7 or 8 record, the encounter it replaces or deletes; empty otherwise"],
           ["5", "CMG_MBR_NO", "Carrisford member number"],
           ["6", "FAC_NPI", "Facility NPI"],
           ["7", "ADMIT_DT", "Admission date, MM/DD/YY"],
           ["8", "DISCH_DT", "Discharge date, MM/DD/YY"],
           ["9", "DISCH_STAT", "UB-04 patient discharge status"],
           ["10", "DRG", "MS-DRG"],
           ["11", "DX1", "Principal diagnosis, ICD-10-CM without the decimal point"],
           ["12", "SUBMIT_DT", "Date Carrisford submitted the record, MM/DD/YY"],
           ["13", "CMG_PAID", "Amount Carrisford paid the facility for the stay, in dollars"]]
    s = [Paragraph(W.GROUP, h1s),
         Paragraph("Inpatient encounter submission file: layout version 4", h1),
         Paragraph("Effective for submissions from January 1, 2025. Prepared by Encounter Operations for Halbrook "
                   "Community Health Plan under the delegation agreement.", h1s),
         Paragraph("File", h2),
         Paragraph("Pipe-delimited text, one record per line, no column names. The first record is a header (H): "
                   "sender, receiver, file type, the submission period's first and last dates and the creation date. "
                   "Each encounter is a detail record (D). The last record is a trailer (T) giving the number of detail "
                   "records and the sum of CMG_PAID over them.", SANS),
         Paragraph("Detail record", h2),
         _table(rec, [0.35 * inch, 1.3 * inch, 5.0 * inch]),
         Paragraph("Members", h2),
         Paragraph("Members are identified by Carrisford member number. Halbrook's enrollment file carries the "
                   "Carrisford number of every member assigned to Carrisford.", SANS),
         Paragraph("Corrections", h2),
         Paragraph("A corrected encounter is sent as a replacement (FREQ 7) naming the encounter it corrects; an "
                   "encounter sent in error is deleted (FREQ 8). Each record's CMG_PAID is its own amount.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the risk scores
HEAD_FILL = PatternFill("solid", fgColor="DCE6EC")
THIN = Side(style="thin", color="A9B4BC")


def write_scores(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Scores"
    head = ["member_id", "admission_date", "facility_npi", "model_version", "p_death_30d"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
    for r in rows:
        ws.append([r[0], dt.date.fromisoformat(r[1]), r[2], r[3], r[4]])
    for c, w in zip("ABCDE", (13, 15, 14, 14, 13)):
        ws.column_dimensions[c].width = w
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    for row in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.0000"
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:E%d" % (len(rows) + 1)
    ab = wb.create_sheet("About")
    lines = [
        ("Halbrook Inpatient Mortality Model (HIMM), version 3.2", True),
        ("Halbrook Analytics, scores run of October 2, 2026", False),
        ("", False),
        ("Scores every inpatient admission of a member aged 18 or older at a network hospital with an admission date "
         "from July 1, 2025 to June 30, 2026, as the claims and encounters stood on September 30, 2026.", False),
        ("p_death_30d is the model's probability that the member dies, from any cause, within 30 days of the "
         "admission date.", False),
        ("Inputs: age, sex, admission type, principal diagnosis group, Elixhauser comorbidities from 12 months of "
         "claims and encounters before admission, dialysis dependence, prior admissions in 12 months, and nursing "
         "facility residence.", False),
        ("Fitted on fiscal 2023 and 2024 admissions; calibration checked on fiscal 2025 admissions (observed over "
         "expected 1.01).", False),
        ("Admissions are keyed by member, admission date and the facility NPI on the bill or encounter.", False),
    ]
    for i, (t, b) in enumerate(lines, 1):
        c = ab.cell(row=i, column=1, value=t or None)
        c.font = Font(bold=b, size=12 if b else 10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ab.column_dimensions["A"].width = 110
    wb.save(path)


# --------------------------------------------------------------------------------------- Provider Disputes' log
def write_disputes(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Log"
    import pack as P
    ws.append(P.DISPUTE_COLS)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for r in rows:
        ws.append(r)
    fmt = {2: "mm/dd/yyyy", 7: "mm/dd/yyyy", 8: "mm/dd/yyyy", 10: "#,##0.00", 12: "mm/dd/yyyy", 13: "#,##0.00",
           14: "mm/dd/yyyy"}
    for row in ws.iter_rows(min_row=2):
        for c in row:
            if c.column in fmt and c.value is not None:
                c.number_format = fmt[c.column]
    widths = (13, 11, 30, 12, 16, 11, 11, 11, 17, 12, 20, 13, 12, 11)
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:N%d" % (len(rows) + 1)
    nt = wb.create_sheet("Notes")
    lines = [
        ("Provider Dispute Resolution log: inpatient", True),
        ("Halbrook Community Health Plan, Provider Disputes. Disputes of inpatient payments received from network "
         "hospitals January 1, 2025 to September 30, 2026. Log run October 1, 2026.", False),
        ("", False),
        ("Claim No.: the bill the hospital disputed, as Halbrook numbered it.", False),
        ("Determination: Overturned, decided for the hospital; Partially overturned, decided for the hospital in "
         "part; Upheld, Halbrook's payment stands; Withdrawn by the hospital; Pending, not yet decided.", False),
        ("Additional Payment: what the determination found Halbrook owed the hospital on the bill beyond what it had "
         "paid.", False),
        ("Payment Date: the day the additional payment was made; blank until it is made.", False),
        ("Amounts in dollars. Dates of admission and discharge as on the disputed bill.", False),
    ]
    for i, (t, b) in enumerate(lines, 1):
        c = nt.cell(row=i, column=1, value=t or None)
        c.font = Font(bold=b, size=12 if b else 10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 110
    wb.save(path)


# -------------------------------------------------------------------------------------------- the distractors
def write_readmissions(path, rows):
    """The quality dashboard's 30-day readmission measure by hospital (a different measure on different stays)."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Readmissions FY2026"
    ws["A1"] = "Halbrook Quality Dashboard: 30-day all-cause readmissions, fiscal 2026 (preliminary, run of Aug 31, 2026)"
    ws["A1"].font = Font(bold=True, size=12)
    head = ["Hospital", "Eligible discharges", "Readmitted within 30 days", "Observed rate", "Expected rate",
            "O/E", "Plan median O/E"]
    for j, h in enumerate(head, 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = Border(bottom=THIN)
    for i, r in enumerate(rows, 4):
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i, column=j, value=v)
            if j in (2, 3):
                c.number_format = "#,##0"
            elif j in (4, 5):
                c.number_format = "0.0%"
            elif j in (6, 7):
                c.number_format = "0.00"
    ws.cell(row=len(rows) + 5, column=1,
            value="Eligible discharges: adult discharges alive, excluding obstetric deliveries, transfers out and "
                  "discharges against medical advice. Readmission: any inpatient admission at any hospital within 30 "
                  "days of discharge, planned readmissions excluded. Preliminary: claims through July 31, 2026.")
    ws.column_dimensions["A"].width = 32
    for c in "BCDEFG":
        ws.column_dimensions[c].width = 14
    ws.row_dimensions[3].height = 32
    ws.freeze_panes = "B4"
    wb.save(path)


def write_profiles(path, rows):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Network hospital profiles, 2026", W.PLAN,
                    W.PLAN + "  |  Provider Network Management  |  Network hospital profiles 2026")
    tab = [["Hospital", "County", "Licensed beds", "ICU beds", "Services", "Ownership"]] + rows
    s = [Paragraph("Network hospital profiles, 2026", h1),
         Paragraph("Provider Network Management, January 2026. From the hospitals' 2025 annual licensing reports and "
                   "contracting files.", h1s),
         _table(tab, [1.55 * inch, 0.68 * inch, 0.72 * inch, 0.5 * inch, 2.05 * inch, 1.2 * inch]),
         Spacer(1, 6),
         Paragraph("Services list the units each hospital reports; NICU levels as designated by the state. X", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
