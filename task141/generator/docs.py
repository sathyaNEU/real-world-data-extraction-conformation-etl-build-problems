"""The pack's documents: the draft revision of the local bail policy (the presumptive tier), the 2024 local bail policy,
the Pretrial Assessment Scale's scoring guide, the extracts note, the jail and court code lists, the clerk's offence
code crosswalk, the magistrate roster, Halsey County's board bills, and two papers from the county's Criminal Justice
Advisory Council (the 2025 jail population report and the reported-crime series)."""
from __future__ import annotations

import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import catalog as C   # noqa: E402
import common as K    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf"),
               ("LiberationSerif", "liberation/LiberationSerif-Regular.ttf"),
               ("LiberationSerif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("LiberationSerif-Italic", "liberation/LiberationSerif-Italic.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
SERIF, SERIF_B, SERIF_I = "LiberationSerif", "LiberationSerif-Bold", "LiberationSerif-Italic"
INK = colors.HexColor("#1b1f27")
GREY = colors.HexColor("#555b66")
RULE = colors.HexColor("#9aa3ad")
PALE = colors.HexColor("#eceff3")

BODY = ParagraphStyle("body", fontName=SERIF, fontSize=10.6, leading=14.0, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=28, firstLineIndent=-28)
H1 = ParagraphStyle("h1", fontName=SERIF_B, fontSize=13.5, leading=17, textColor=INK, spaceAfter=2, alignment=1)
H1S = ParagraphStyle("h1s", fontName=SERIF, fontSize=10.2, leading=13, textColor=INK, spaceAfter=10, alignment=1)
H2 = ParagraphStyle("h2", fontName=SERIF_B, fontSize=11, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
NOTE = ParagraphStyle("note", fontName=SERIF_I, fontSize=9, leading=11.5, textColor=GREY, spaceBefore=4)
SB = ParagraphStyle("sb", fontName=SANS, fontSize=10.2, leading=13.2, textColor=INK, spaceAfter=5)
SH1 = ParagraphStyle("sh1", fontName=SANS_B, fontSize=15, leading=18.5, textColor=colors.HexColor("#22405f"), spaceAfter=2)
SH1S = ParagraphStyle("sh1s", fontName=SANS, fontSize=9.6, leading=12.4, textColor=GREY, spaceAfter=9)
SH2 = ParagraphStyle("sh2", fontName=SANS_B, fontSize=11.2, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.8, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName=SANS_B, fontSize=8.8, leading=10.8, textColor=INK)


def n0(x):
    return "{:,}".format(int(round(x)))


def _footer(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "%s  |  page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.85 * inch,
                             bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths, head=True):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), PALE))
    t.setStyle(TableStyle(st))
    return t


# ---------------------------------------------------------------------------------------------------- the 2024 policy

def write_policy24(path):
    s = [Paragraph("STATE OF NORTH CAROLINA, DORRANCE COUNTY", H1S),
         Paragraph("In the General Court of Justice", H1S),
         Paragraph("LOCAL BAIL POLICY FOR PRETRIAL RELEASE", H1),
         Paragraph("Issued under G.S. 15A-535 by the Senior Resident Superior Court Judge after consultation with the "
                   "Chief District Court Judge. Effective 1 July 2024; replaces the policy of 1 March 2019.", H1S)]

    def part(title, clauses):
        s.append(Paragraph(title, H2))
        for n, t in clauses:
            s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), CLAUSE))

    part("Part 1. Definitions", [
        ("1.1", "Judicial official: a magistrate, district court judge or superior court judge setting conditions of "
                "pretrial release."),
        ("1.2", "Initial appearance: the defendant's first appearance before a judicial official after an arrest on new "
                "charges, at which the conditions of pretrial release are set."),
        ("1.3", "Conditions of pretrial release: a written promise to appear; an unsecured appearance bond; release to "
                "the custody of a designated person or organization; a secured appearance bond; and, added to any of "
                "these, house arrest with electronic monitoring or pretrial supervision by Pretrial Services."),
        ("1.4", "Failure to appear: a scheduled court date at which the defendant did not appear and for which the "
                "court issued an order for arrest."),
        ("1.5", "Pretrial Assessment Scale: the records-based screen Dorrance County Pretrial Services completes at "
                "intake (version 2 from 1 July 2021), giving a new-criminal-activity score and a failure-to-appear "
                "score, each from 1 to 6."),
    ])
    part("Part 2. Initial appearance", [
        ("2.1", "An arrested person shall be taken before a judicial official without unnecessary delay. At the "
                "detention center the initial appearance is ordinarily held within six hours of booking."),
        ("2.2", "Pretrial Services gives the magistrate the defendant's screen before the initial appearance where the "
                "screen has been completed. The screen informs the conditions and does not decide them."),
        ("2.3", "Initial appearances at the detention center are heard by the magistrate on duty. The Chief "
                "Magistrate assigns magistrates to the twelve-hour duty shifts by rota."),
        ("2.4", "The magistrate records the conditions set and the first court date on the release order."),
    ])
    part("Part 3. Conditions", [
        ("3.1", "The judicial official shall impose a written promise to appear, an unsecured bond or custody release "
                "unless the official determines that such a release will not reasonably assure the defendant's "
                "appearance, will pose a danger of injury to any person or is likely to result in the destruction of "
                "evidence, the subornation of perjury or the intimidation of witnesses (G.S. 15A-534(b))."),
        ("3.2", "Where a secured bond is required, the amounts below are guidelines for the most serious charge. The "
                "official may depart from them and shall state the reason on the release order."),
    ])
    rows = [["Most serious charge", "Guideline secured bond"],
            ["Misdemeanor, Class 3", "$500"], ["Misdemeanor, Class 2", "$1,000"], ["Misdemeanor, Class 1", "$1,500"],
            ["Misdemeanor, Class A1", "$2,500"], ["Felony, Class I", "$5,000"], ["Felony, Class H", "$7,500"],
            ["Felony, Class G or F", "$15,000 to $25,000"], ["Felony, Class E or higher", "$50,000 or more"]]
    s.append(_table(rows, [2.6 * inch, 2.0 * inch]))
    s.append(Spacer(1, 6))
    part("Part 4. Monitoring and supervision", [
        ("4.1", "House arrest with electronic monitoring may be added as a condition where the official finds it "
                "necessary. Monitoring is provided under the county's contract with the monitoring vendor and ends at "
                "the disposition of the charges or on the court's order."),
        ("4.2", "Pretrial supervision may be added for a defendant released on a written promise or an unsecured bond."),
    ])
    part("Part 5. Review", [
        ("5.1", "A defendant who remains in custody after the initial appearance shall be brought before a district "
                "court judge at the next session of court for a review of the conditions set."),
    ])
    s.append(Paragraph("Zachary Henson, Senior Resident Superior Court Judge. Kristen Thompson, Chief District Court "
                       "Judge.", NOTE))
    doc = _doc(path, "Local Bail Policy, Dorrance County, 1 July 2024", K.PEOPLE["srj"])
    doc.build(s, onFirstPage=_footer("Dorrance County local bail policy, 1 July 2024", "Superior Court"),
              onLaterPages=_footer("Dorrance County local bail policy, 1 July 2024", "Superior Court"))


# ---------------------------------------------------------------------------------------------------- the draft

def write_draft(path):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(11.5)
    for t, b in (("STATE OF NORTH CAROLINA, DORRANCE COUNTY", False), ("In the General Court of Justice", False),
                 ("LOCAL BAIL POLICY FOR PRETRIAL RELEASE: REVISION FOR 2027", True),
                 ("Draft for consultation, 6 October 2026", False)):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(t)
        r.bold = b
    d.add_paragraph("Circulated to the Chief District Court Judge, the District Attorney, the Public Defender, the Chief "
                    "Magistrate, the Sheriff and the Director of Pretrial Services. Comments to the Senior Resident "
                    "Superior Court Judge's office by 6 November 2026. The revision is to be issued and filed with the "
                    "Clerk of Superior Court by 1 December 2026.")

    def clause(n, text):
        p = d.add_paragraph()
        r = p.add_run(n + "  ")
        r.bold = True
        p.add_run(text)

    def head(t):
        p = d.add_paragraph()
        r = p.add_run(t)
        r.bold = True
    head("1. Purpose")
    clause("1.1", "This revision amends the local bail policy of 1 July 2024 from 1 January 2027 by adding a presumptive "
                  "release tier for defendants charged only with eligible misdemeanors. Parts 1, 2, 3, 4 and 5 of the "
                  "2024 policy continue for every other defendant, and their definitions apply to this revision.")
    head("2. Presumptive release tier")
    clause("2.1", "Eligible defendant. A defendant is eligible when each charge at the initial appearance is a "
                  "misdemeanor, none of the charges is an offense listed in Appendix B, and no other jurisdiction has "
                  "lodged a hold or detainer for the defendant at intake.")
    clause("2.2", "The tier. Every eligible defendant whose Pretrial Assessment Scale screen shows a new-criminal-activity "
                  "score at or below the tier's top score shall be released on a written promise to appear at the "
                  "initial appearance. The magistrate sets the first court date and adds no other condition.")
    clause("2.3", "Safety floor. A score is in the tier only if at least 85 percent of the eligible defendants the tier "
                  "releases at that score are expected to complete the pretrial period without a new-offense arrest.")
    clause("2.4", "New-offense arrest. An arrest anywhere in North Carolina for an offense committed after the day of "
                  "release and within 365 days of release, or before the last of the defendant's charges from the "
                  "initial appearance is disposed, whichever comes first. An arrest on an order for arrest, on a warrant "
                  "for an offense committed before release, or for a probation violation is not a new-offense arrest.")
    clause("2.5", "The tier's top score. The highest score at which that score and every lower score meet the safety "
                  "floor.")
    clause("2.6", "Setting the top score. Pretrial Services will propose the top score for the filed revision from the "
                  "county's records of eligible defendants' initial appearances.")
    head("3. Defendants above the tier")
    clause("3.1", "For a defendant who is not eligible, or whose score is above the tier's top score, the magistrate sets "
                  "conditions under Part 3 of the 2024 policy.")
    head("4. Review")
    clause("4.1", "The Chief District Court Judge and the Director of Pretrial Services will review the tier after its "
                  "first twelve months in operation.")
    head("5. Effective date")
    clause("5.1", "This revision takes effect on 1 January 2027.")
    head("Appendix B. Offenses that take a defendant out of the tier")
    t = d.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "G.S."
    t.rows[0].cells[1].text = "Offense"
    for stt, desc, _ in C.APPENDIX_B:
        row = t.add_row().cells
        row[0].text = stt
        row[1].text = desc
    d.add_paragraph("")
    d.add_paragraph("Zachary Henson, Senior Resident Superior Court Judge")
    d.core_properties.author = K.PEOPLE["srj"]
    d.core_properties.title = "Local bail policy revision for 2027, draft"
    d.save(path)


# ---------------------------------------------------------------------------------------------------- the scoring guide

def write_guide(path):
    s = [Paragraph("Dorrance County Pretrial Services", SH1S), Paragraph("Pretrial Assessment Scale: scoring guide",
                                                                          SH1),
         Paragraph("Version 2, in use from 1 July 2021. Revised July 2021; reissued March 2024 with the clerk's new "
                   "system's field names. Owner: Director of Pretrial Services.", SH1S),
         Paragraph("What the screen is", SH2),
         Paragraph("The Pretrial Assessment Scale is a records-based screen. A screener completes it at intake from the "
                   "statewide criminal record and the court's records, before the initial appearance; there is no "
                   "interview. One screen is completed for each booking on new charges. A screen completed on paper "
                   "during a system outage is entered afterwards and carries no booking number.", SB),
         Paragraph("The screen gives two scores, each from 1 to 6: a new-criminal-activity score and a failure-to-appear "
                   "score. Points are added for each item and the total is converted to the score with the tables below.",
                   SB),
         Paragraph("New-criminal-activity items", SH2)]
    rows = [["Item", "Points"]]
    for _, label, pts in C.NCA_ITEMS:
        rows.append([label, ", ".join("%s" % v for k, v in sorted(pts.items()) if k > 0)])
    s.append(_table(rows, [4.6 * inch, 1.2 * inch]))
    s.append(Spacer(1, 6))
    rows = [["Points", "New-criminal-activity score"]] + [["%d" % lo if lo == hi else "%d to %d" % (lo, hi), str(sc)]
                                                          for lo, hi, sc in C.NCA_BANDS]
    s.append(_table(rows, [1.4 * inch, 2.4 * inch]))
    s.append(Paragraph("Failure-to-appear items", SH2))
    rows = [["Item", "Points"]]
    for _, label, pts in C.FTA_ITEMS:
        rows.append([label, ", ".join("%s" % v for k, v in sorted(pts.items()) if k > 0)])
    s.append(_table(rows, [4.6 * inch, 1.2 * inch]))
    s.append(Spacer(1, 6))
    rows = [["Points", "Failure-to-appear score"]] + [["%d" % lo if lo == hi else "%d to %d" % (lo, hi), str(sc)]
                                                      for lo, hi, sc in C.FTA_BANDS]
    s.append(_table(rows, [1.4 * inch, 2.4 * inch]))
    s.append(Paragraph("Definitions", SH2))
    for t in ("Pending charge: a charge pending in any North Carolina court on the day of the current arrest.",
              "Prior conviction: a conviction entered before the day of the current arrest, in any court.",
              "Violent conviction: a conviction for an offense the scale's offense list marks violent (assaults, robbery, "
              "and offenses with a weapon).",
              "Failure to appear: a court date for which an order for arrest for failure to appear was issued; the "
              "two-year count runs back from the day of the current arrest."):
        s.append(Paragraph(t, SB))
    doc = _doc(path, "Pretrial Assessment Scale scoring guide, version 2", K.PEOPLE["director"])
    doc.build(s, onFirstPage=_footer("Pretrial Assessment Scale v2 scoring guide", "Pretrial Services"),
              onLaterPages=_footer("Pretrial Assessment Scale v2 scoring guide", "Pretrial Services"))


# ---------------------------------------------------------------------------------------------------- code lists

JAIL_CODES = [
    ("booking_type", "NEW", "Booked on an arrest on new charges"),
    ("booking_type", "TRF", "Moved in from another housing site of the detention center"),
    ("booking_type", "BI", "Returned from a contract facility"),
    ("booking_type", "OFA", "Booked on an order for arrest"),
    ("release_type", "WPA", "Released on a written promise to appear"),
    ("release_type", "UNSEC", "Released on an unsecured bond"),
    ("release_type", "CUST", "Released to the custody of a designated person"),
    ("release_type", "BOND", "Released on a secured bond posted"),
    ("release_type", "TS", "Released, time served or sentence complete"),
    ("release_type", "DISM", "Released, charges dismissed"),
    ("release_type", "CRTO", "Released on a court order"),
    ("release_type", "XFER", "Released to another agency on its hold or detainer"),
    ("release_type", "TRF", "Moved to another housing site of the detention center"),
    ("release_type", "BO", "Boarded out to a contract facility"),
    ("facility", "DCDC", "Dorrance County Detention Center, 410 Court Street, Garrison"),
    ("facility", "DCDC-ANNEX", "Detention Center annex, Mill Street, Garrison"),
]

COURT_CODES = [
    ("court", "DISTRICT", "District Court"),
    ("court", "SUPERIOR", "Superior Court"),
    ("condition_legacy", "WPA", "Written promise to appear"),
    ("condition_legacy", "UNSEC", "Unsecured bond"),
    ("condition_legacy", "CUST", "Custody release"),
    ("condition_legacy", "SEC", "Secured bond"),
    ("release_condition", "WRITTEN_PROMISE", "Written promise to appear"),
    ("release_condition", "UNSECURED_BOND", "Unsecured bond"),
    ("release_condition", "CUSTODY_RELEASE", "Custody release"),
    ("release_condition", "SECURED_BOND", "Secured bond"),
    ("disposition_code", "GP", "Guilty plea"),
    ("disposition_code", "GT", "Guilty at trial"),
    ("disposition_code", "VD", "Voluntary dismissal by the State"),
    ("disposition_code", "DD", "Dismissed after deferred prosecution"),
    ("disposition_code", "NG", "Not guilty"),
    ("disposition_code", "IND", "Indictment returned in superior court"),
    ("event_code", "SET", "Court date held or continued"),
    ("event_code", "FTA", "Called and failed; order for arrest issued"),
    ("event_code", "OFAR", "Order for arrest recalled"),
    ("event_code", "OFARI", "Order for arrest reissued"),
    ("event_code", "OFAS", "Order for arrest served"),
    ("event_code", "DISP", "Disposition entered"),
]


def write_code_lists(jail_path, court_path):
    K.write_csv(jail_path, ["field", "code", "description"], [list(x) for x in JAIL_CODES], crlf=True)
    K.write_csv(court_path, ["field", "code", "description"], [list(x) for x in COURT_CODES], crlf=True)


# ---------------------------------------------------------------------------------------------------- workbooks

def _title_rows(ws, title, sub, note=None):
    ws.append([title])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append([sub])
    ws["A2"].font = Font(name="Calibri", italic=True, size=10, color="595959")
    if note:
        ws.append([note])
        ws.cell(row=ws.max_row, column=1).font = Font(name="Calibri", size=9, color="595959")
    ws.append([])


def _head(ws, cols, widths=None, fill="DCE6F0"):
    ws.append(cols)
    row = ws.max_row
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name="Calibri", bold=True)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return row


def write_crosswalk(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Offense codes"
    _title_rows(ws, "Offense code crosswalk, legacy system to the new case management system",
                "Office of the Clerk of Superior Court, Dorrance County. Prepared for the conversion of 4 March 2024.",
                "One row per legacy code. Charges entered from 4 March 2024 carry the new code only.")
    hr = _head(ws, ["Legacy code", "New code", "G.S.", "Description", "Class"], [12, 11, 14, 42, 8])
    for o in sorted(C.OFFENCES, key=lambda o: o[1][0]):
        for lc in o[1]:
            ws.append([lc, o[0], o[2], o[3], o[4]])
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    wb.save(path)


def write_roster(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Magistrates"
    _title_rows(ws, "Dorrance County magistrates, 2021 to 2026", "Office of the Chief Magistrate. Updated 28 September "
                "2026.", "Initials are the magistrate's key in the clerk's legacy system; the employee number is the key "
                "in the new system from 4 March 2024.")
    hr = _head(ws, ["Magistrate", "Initials (legacy)", "Employee no.", "Sworn in", "Left office"], [28, 15, 13, 12, 12])
    for m in sorted(W.mags, key=lambda m: (m["last"], m["first"])):
        ws.append(["%s, %s %s." % (m["last"], m["first"], m["middle"]), m["initials"], m["empno"], m["start"],
                   m["end"] if m["end"] else None])
        ws.cell(row=ws.max_row, column=4).number_format = "mm/dd/yyyy"
        if m["end"]:
            ws.cell(row=ws.max_row, column=5).number_format = "mm/dd/yyyy"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    ws2 = wb.create_sheet("Duty shifts")
    _title_rows(ws2, "Detention center duty shifts", "Office of the Chief Magistrate.")
    for t in ("Day shift 07:00 to 19:00, night shift 19:00 to 07:00, every day of the year.",
              "Four magistrates on duty at the detention center on each shift.",
              "Shift assignments are posted each quarter; each magistrate works day, night and weekend shifts.",
              "Initial appearances are taken in turn by the magistrates on duty."):
        ws2.append([t])
    ws2.column_dimensions["A"].width = 96
    wb.save(path)


def write_halsey(path, W, stays):
    """One sheet a month: every Dorrance defendant held at Halsey in the month, the stay's own dates in and out (out
    left blank while the stay runs on), and the days billed in the month, each day or part of a day."""
    wb = openpyxl.Workbook()
    months = []
    m = dt.date(2025, 11, 1)
    while m <= K.EXTRACT_END:
        months.append(m)
        m = dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
    P = W.persons
    end_t = K.d2dt(K.EXTRACT_END + dt.timedelta(days=1))
    for i, m in enumerate(months):
        m_end = dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1) - dt.timedelta(days=1)
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = m.strftime("%b %Y")
        _title_rows(ws, "Halsey County Sheriff's Office, Detention Division", "Inmate housing invoice to Dorrance County "
                    "Sheriff's Office for %s. Rate $68.00 per inmate per day or part of a day." % m.strftime("%B %Y"))
        hr = _head(ws, ["Halsey booking", "Inmate", "DOB", "Agency ref.", "Date in", "Date out", "Days", "Amount"],
                   [15, 30, 12, 14, 12, 12, 8, 11])
        tot_d, tot_a = 0, 0.0
        for h in stays:
            s, e = h["s"], h["e"]
            din = s["start"].date()
            out = s["end"].date() if s["end"] < end_t else None
            last = out if out else K.EXTRACT_END
            if din > m_end or last < m:
                continue
            a, b = max(din, m), min(last, m_end)
            days = (b - a).days + 1
            p = P[e["pid"]]
            ws.append([h["hbk"], "%s, %s" % (p.last.upper(), p.first.upper()), p.dob,
                       None if h["ref_blank"] else e["booking_no"], din, out if (out and out <= m_end) else None, days,
                       round(days * 68.0, 2)])
            for c, f in ((3, "mm/dd/yyyy"), (5, "mm/dd/yyyy"), (6, "mm/dd/yyyy"), (8, "#,##0.00")):
                ws.cell(row=ws.max_row, column=c).number_format = f
            tot_d += days
            tot_a += days * 68.0
        ws.append([])
        ws.append(["Total", None, None, None, None, None, tot_d, round(tot_a, 2)])
        ws.cell(row=ws.max_row, column=1).font = Font(name="Calibri", bold=True)
        ws.cell(row=ws.max_row, column=8).number_format = "#,##0.00"
        ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- the README

def write_readme(path, files):
    lines = ["Dorrance County Pretrial Services: extracts for the 2027 bail policy revision",
             "Pulled 2 October 2026 by Pretrial Services from the systems named below. Every extract runs to the end of",
             "30 September 2026.", ""]
    for f, desc, src in files:
        lines.append(f)
        lines.append("    " + desc)
        lines.append("    Source: " + src)
        lines.append("")
    lines += [
        "Notes",
        "- Times: the court exports and the screens are Eastern local time. The jail export is UTC (ISO 8601, ending Z).",
        "  The state arrest extract has dates only.",
        "- The clerk's legacy system ran to 3 March 2024 and the new case management system from 4 March 2024. The legacy",
        "  export writes case numbers with a space (21CR 004512), booking numbers without the B and the hyphen, the",
        "  magistrate's initials and the legacy offense codes; the new export writes the new codes on its charge rows.",
        "  The offense code crosswalk maps one to the other. The case index lists every case in the new system's format.",
        "- A first appearance is the defendant's initial appearance before a magistrate after an arrest on new charges.",
        "  Appearances on orders for arrest are not in the first-appearance exports.",
        "- Detention: a stay runs from booking to release. The jail's population count is taken at midnight and dated",
        "  with the day it begins; one bed-day is counted for each midnight count at which the person is held.",
        "- Release at first appearance, as Pretrial Services reports it: leaving the detention center within 24 hours of",
        "  the first appearance on the conditions set at it, a secured bond posted in that time included. A defendant",
        "  still in custody 24 hours after the appearance is held after it.",
        "- The state arrest extract lists every arrest in North Carolina of anyone with a first appearance in either",
        "  export, from 1 October 2021, one row for each charge of an arrest.",
        "- Sentry Point bills each enrollment by the month, each day or part of a day the enrollment is active.",
        "- Code lists: jail_code_list.csv and court_code_list.csv.",
    ]
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------------------------------- distractors

def write_cjac_jail(path, W, monthly):
    """The Criminal Justice Advisory Council's 2025 jail population report: average daily population, bookings and
    releases by month for calendar 2025, from the jail system (computed from the shipped export)."""
    s = [Paragraph("Dorrance County Criminal Justice Advisory Council", SH1S),
         Paragraph("Jail population report, 2025", SH1),
         Paragraph("Prepared by the Sheriff's Office for the Council's February 2026 meeting. Calendar 2025, from the jail "
                   "management system. Average daily population is the mean of the midnight counts in the month, every "
                   "housing site of the detention center, contract beds not included.", SH1S)]
    rows = [["Month", "Bookings", "Releases", "Average daily population", "Highest count"]]
    for mth, b, r_, adp, hi in monthly:
        rows.append([mth, n0(b), n0(r_), "%.1f" % adp, n0(hi)])
    s.append(_table(rows, [1.4 * inch, 1.0 * inch, 1.0 * inch, 1.8 * inch, 1.2 * inch]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("The detention center's rated capacity is 1,020 beds across the main building and the Mill Street "
                       "annex. The Council asked for the 2026 report to add length of stay by charge level.", SB))
    doc = _doc(path, "Jail population report 2025", K.PEOPLE["jail"])
    doc.build(s, onFirstPage=_footer("CJAC jail population report 2025", "Dorrance County Sheriff's Office"),
              onLaterPages=_footer("CJAC jail population report 2025", "Dorrance County Sheriff's Office"))


def write_crime(path):
    r = K.rng("crime")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reported offenses"
    _title_rows(ws, "Reported offenses, Dorrance County law enforcement agencies, 2019 to 2025",
                "Compiled for the Criminal Justice Advisory Council from the agencies' annual submissions. Counts of "
                "offenses known to law enforcement.")
    years = list(range(2019, 2026))
    _head(ws, ["Offense"] + [str(y) for y in years], [34] + [9] * len(years))
    base = [("Murder and nonnegligent manslaughter", 31), ("Rape", 212), ("Robbery", 655), ("Aggravated assault", 2410),
            ("Burglary", 3870), ("Larceny-theft", 17950), ("Motor vehicle theft", 2240), ("Simple assault", 7640),
            ("Vandalism", 4310), ("Drug and narcotic violations", 5120), ("Driving while impaired", 2985),
            ("Trespass of real property", 1870)]
    trend = [1.0, 0.93, 0.98, 1.03, 1.01, 0.97, 0.95]
    for name, b in base:
        vals = [int(round(b * trend[i] * (1 + 0.035 * r.standard_normal()))) for i in range(len(years))]
        ws.append([name] + vals)
    wb.save(path)
