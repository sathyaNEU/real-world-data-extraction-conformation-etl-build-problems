"""The pack's documents: the State Tax Commission's Rule 18-7 and the County Administrator's memo (PDF), the
data dictionary (TXT), and two workbooks: the retired appraisal system's 2025 roll export and the FY2026 levy sheet."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import LETTER                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1b2430"), colors.HexColor("#56616c"), colors.HexColor("#b8c0c8")
GREEN = colors.HexColor("#22433a")
SLATE = colors.HexColor("#2c3e57")


def styles(face="Sans", accent=SLATE):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.2, leading=13.9, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.2, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.8, leading=14, textColor=INK, spaceBefore=8, spaceAfter=2,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.4, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.4, leading=10.4, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.9, leading=10.1, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=30, firstLineIndent=-30),
        sub=ParagraphStyle("s", parent=body, leftIndent=48, firstLineIndent=-18))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(0.9 * inch, LETTER[1] - 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, LETTER[1] - 0.55 * inch, right)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text, key="clause"):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S[key])


def _doc(path, title, author, subject, left, right):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                             topMargin=0.85 * inch, bottomMargin=0.8 * inch, title=title, author=author,
                             subject=subject, creator=author, producer=author), _frame(left, right)


# ------------------------------------------------------------------------------------------------ Rule 18-7
RULE_LEVEL = ("The level of a class is the median, over every parcel of the class on the county's certified roll, "
              "sold or not, of the parcel's assessed value on that roll divided by its market value on the "
              "assessment date.")
RULE_COD = ("The uniformity of a class is its coefficient of dispersion (COD): the average, over the same parcels, "
            "of the absolute difference between a parcel's ratio and the class's level, divided by the level and "
            "expressed as a percentage.")
RULE_EVIDENCE = ("A parcel's market value on the assessment date is evidenced by its arm's-length sale recorded in "
                 "the calendar year before the assessment date (validation code Q in the county recorder's "
                 "extract). The price is carried to the assessment date by the county's monthly residential price "
                 "index, multiplied by the index for the month of the assessment date and divided by the index for "
                 "the month of the deed.")
RULE_SETASIDE = ("A sale is set aside where the parcel's boundaries or improvements changed between the date of the "
                 "deed and the assessment date. Ratios are not otherwise trimmed.")
RULE_PRD = ("The price-related differential (PRD) of a class is the mean of its parcels' ratios divided by its "
            "aggregate ratio, the total of their assessed values divided by the total of their market values.")


def write_rule(path):
    S = styles("Serif", GREEN)
    doc, fr = _doc(path, "Rule 18-7. Residential ratio studies", K.STATE_BODY, "Rule 18-7",
                   "%s, %s" % (K.STATE_BODY, K.DIVISION), "Rule 18-7")
    st = [Paragraph("Rule 18-7. Residential ratio studies", S["h1"]),
          Paragraph("%s. Adopted 11 March 2021; applies to every county's roll from the assessment date of 1 "
                    "January 2022. Administered by the %s." % (K.STATE_BODY, K.DIVISION), S["meta"]),
          Paragraph("1. Scope", S["h2"]),
          _clause(S, "1.1", "Each year the Division studies every county's roll for the two residential classes: "
                            "single-family residential (class R1) and residential condominium (class R2). Vacant "
                            "residential land is outside this rule."),
          _clause(S, "1.2", "The study measures the roll the county assessor certified for the assessment date, "
                            "1 January of the roll year."),
          Paragraph("2. Statistics", S["h2"]),
          _clause(S, "2.1", RULE_LEVEL),
          _clause(S, "2.2", RULE_COD),
          _clause(S, "2.3", RULE_PRD + " The PRD is reported with each class's study; it is not a test under 4."),
          Paragraph("3. Evidence of market value", S["h2"]),
          _clause(S, "3.1", RULE_EVIDENCE),
          _clause(S, "3.2", RULE_SETASIDE),
          Paragraph("4. Standards", S["h2"]),
          _clause(S, "4.1", "A class meets this rule when its level is from %.3f to %.3f and its COD is %.1f or "
                            "less." % (K.STANDARD["level_lo"], K.STANDARD["level_hi"], K.STANDARD["cod_max"])),
          _clause(S, "4.2", "The PRD of a class is expected to fall from %.2f to %.2f." % (K.STANDARD["prd_lo"],
                                                                                        K.STANDARD["prd_hi"])),
          Paragraph("5. Orders", S["h2"]),
          _clause(S, "5.1", "Where a class fails either standard in 4.1, the Commission orders the county to "
                            "reappraise every parcel of that class for the roll of the second assessment date after "
                            "the study, at the county's cost, and to submit the vendor contract or work plan by 31 "
                            "January of the year the reappraisal is carried out."),
          _clause(S, "5.2", "The Division sends each county its study by 30 November of the roll year."),
          Spacer(1, 8),
          Paragraph("Questions on this rule go to the Property Tax Division, Equalization Section.", S["note"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ the memo
def write_memo(path):
    S = styles("Sans", SLATE)
    doc, fr = _doc(path, "The single-family reappraisal offer", K.PEOPLE["administrator"], "Reappraisal offer",
                   "%s, Office of the County Administrator" % K.COUNTY, "Reappraisal offer")
    head = _table(S, [["", ""],
                      ["To", "Budget and Policy Analysis"],
                      ["From", "%s, County Administrator" % K.PEOPLE["administrator"]],
                      ["Copy", "%s, Chair, Board of Commissioners; %s, County Assessor"
                       % (K.PEOPLE["board_chair"], K.PEOPLE["assessor"])],
                      ["Date", "14 September 2026"],
                      ["Subject", "The single-family reappraisal offer and Rule 18-7"]],
                  [0.9, 5.6])
    st = [Paragraph("Memorandum", S["h1"]), head, Spacer(1, 10),
          Paragraph("The %s's Property Tax Division studies our certified 2026 roll under Rule 18-7 this autumn and "
                    "sends its study by 30 November. If a residential class fails the rule, the Commission orders "
                    "a county-wide reappraisal of that class for the 1 January 2028 roll, at our cost, with the "
                    "vendor contract due by 31 January 2027." % K.STATE_BODY, S["body"]),
          Paragraph("The appraisal vendor that carried out our last reappraisal has offered to reappraise the "
                    "single-family class for the 1 January 2028 roll for about USD 1.6 million over two years. Its "
                    "offer holds until 30 October 2026. After that its field crews are committed to other counties "
                    "until the 2030 roll, and the Assessor does not expect another vendor to take the work on two "
                    "months' notice, so the Board has to accept or decline the offer before the Division's study "
                    "arrives.", S["body"]),
          Paragraph("Please bring the Board's 6 October work session a recommendation: does the 2026 single-family "
                    "roll meet Rule 18-7, or do we accept the vendor's offer? The Chair has also asked to see where "
                    "the condominium class stands on the same rule, and what the Board of Review took off the 2025 "
                    "roll in each market area, since the hearings have been the Board's main complaint about the "
                    "roll.", S["body"]),
          Paragraph("The Assessor's office has sent the certified 2026 roll from the new appraisal system, the 2025 "
                    "roll exported from the old system before it was retired in January, and its parcel change log. "
                    "The Recorder has sent the 2025 deed extract with the clerks' validation codes, and Building "
                    "Services the 2025 permits. The Board of Review's clerk has sent the hearings held in 2025. The "
                    "price index is the one the Division publishes for Tillford County.", S["body"]),
          Paragraph("The homestead credit file and the FY2026 levy sheet came with the roll for the Treasurer's levy "
                    "estimate; they are not part of this question.", S["body"]),
          Spacer(1, 10),
          Paragraph("DG/lm", S["note"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ dictionary
DICTIONARY = [
    (K.FILES["roll26"], "One row per parcel on the 2026 roll as certified on 1 June 2026 (assessment date 1 January "
                        "2026), exported from the county's appraisal system.",
     [("parcel_id", "parcel identifier: book, page, parcel and a suffix digit (0 unless the parcel was split)"),
      ("class_code", "R1 single-family residential; R2 residential condominium; R0 vacant residential land"),
      ("nbhd_code", "appraisal neighbourhood (see the crosswalk)"),
      ("situs_address", "property address; a condominium unit's address carries its unit label"),
      ("year_built", "year the main structure was built (blank for land)"),
      ("living_area_sf", "finished living area, square feet"),
      ("land_value", "assessed value of the land, USD"),
      ("improvement_value", "assessed value of the improvements, USD"),
      ("total_assessed_value", "land_value plus improvement_value, USD")]),
    (K.FILES["roll25"], "One row per parcel on the 2025 roll as certified on 2 June 2025 (assessment date 1 January "
                        "2025), exported from the appraisal system the county retired in January 2026.",
     [("Parcel No.", "book-page-parcel"),
      ("Class", "the old system's class description"),
      ("Neighborhood", "appraisal neighbourhood by name"),
      ("Land, Improvements, Total Assessed", "assessed values, USD")]),
    (K.FILES["crosswalk"], "One row per appraisal neighbourhood.",
     [("nbhd_code, nbhd_name", "the new system's code and the old system's name for the same neighbourhood"),
      ("market_area, market_area_name", "the market area the neighbourhood belongs to")]),
    (K.FILES["changes"], "One row per old parcel number and new parcel identifier joined by a change the Assessor "
                         "recorded in 2025.",
     [("effective_date", "date the change took effect"),
      ("change_type", "SPLIT, COMBINE or RENUMBER"),
      ("old_parcel_no", "the parcel number before the change, book-page-parcel"),
      ("new_parcel_id", "the parcel identifier after the change, as on the 2026 roll"),
      ("reference_doc", "the plat, combination request or declaration recorded for the change")]),
    (K.FILES["deeds"], "One row per parcel conveyed by a deed recorded from 1 January to 31 December 2025; a deed "
                       "conveying several parcels has a row for each.",
     [("instrument_no", "the Recorder's instrument number"),
      ("recorded_date", "date the deed was recorded"),
      ("deed_date", "date the deed was signed"),
      ("parcel_no", "parcel number as written on the deed, book-page-parcel"),
      ("deed_type", "form of deed"),
      ("consideration", "price stated on the transfer declaration, USD"),
      ("validation_code", "Q arm's-length sale; U1 related parties; U2 foreclosure or sheriff's sale; U3 estate or "
                          "probate; U4 partial interest; U5 several parcels on one deed; U6 corrective deed")]),
    (K.FILES["index"], "One row per month: the Division's residential price index for Tillford County.",
     [("period", "year and month"), ("index_jan2025_100", "index, January 2025 = 100.0")]),
    (K.FILES["permits"], "One row per building permit issued in 2025.",
     [("parcel_no", "parcel number, book-page-parcel"),
      ("issued_date, final_inspection_date", "permit issued; final inspection passed (blank while open)"),
      ("status", "FINALED, OPEN or EXPIRED"),
      ("declared_valuation", "cost of the work declared on the application, USD")]),
    (K.FILES["bor"], "One row per hearing decision the Board of Review entered in 2025; a case heard a second time "
                     "has a row for each hearing.",
     [("case_no", "the Board's case number"),
      ("parcel_no", "parcel number, book-page-parcel"),
      ("property_class", "SFR single-family; CONDO condominium"),
      ("hearing_date", "date of the hearing (blank for a petition withdrawn before it was heard)"),
      ("decision", "REDUCED, SUSTAINED or WITHDRAWN"),
      ("value_before, value_after", "assessed value appealed from and value set by the decision, USD")]),
]


def write_dictionary(path):
    out = ["%s: files gathered for the single-family reappraisal offer" % K.COUNTY,
           "Office of the County Administrator, Budget and Policy Analysis, 18 September 2026", ""]
    for name, grain, cols in DICTIONARY:
        out.append(name)
        out.append("  " + grain)
        for c, m in cols:
            out.append("    %-36s %s" % (c, m))
        out.append("")
    out += ["Documents", "  " + K.FILES["rule"] + "  State Tax Commission Rule 18-7",
            "  " + K.FILES["memo"] + "  the County Administrator's memo of 14 September 2026",
            "  " + K.FILES["homestead"] + "  2026 homestead credits by parcel (Treasurer)",
            "  " + K.FILES["levy"] + "  FY2026 levies and rates by taxing district (Auditor)", ""]
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(out))


# ------------------------------------------------------------------------------------------------ workbooks
def write_roll25(path, head, rows):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ROLL2025"
    ws.append(["TILLFORD COUNTY ASSESSOR"])
    ws.append(["2025 CERTIFIED ROLL, RESIDENTIAL CLASSES (certified June 2, 2025)"])
    ws.append(["Run 01/08/2026 16:42  CAMA-LEGACY RPT 114"])
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    for k, v in {"A": 13, "B": 26, "C": 18, "D": 30, "E": 8, "F": 8, "G": 11, "H": 13, "I": 14}.items():
        ws.column_dimensions[k].width = v
    wb.save(path)


LEVY = [("Tillford County", "General fund", 24318650), ("Tillford County", "Roads and bridges", 6102480),
        ("Tillford County", "Health department", 1875300),
        ("Tillford Unified School District 41", "Operating", 38410920),
        ("Tillford Unified School District 41", "Debt service", 7934100),
        ("North Lakes School District 12", "Operating", 11208770),
        ("City of Tillford", "General fund", 9786410), ("Village of Grebe Lake", "General fund", 1219860),
        ("Tillford Fire Protection District", "Operating", 3402150),
        ("Tillford Library District", "Operating", 1388040)]


def write_levy(path, taxable):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Levy FY2026"
    ws.append(["Tillford County Auditor: FY2026 levies and rates by taxing district"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Taxable value from the 2025 roll after homestead credits. Rates per USD 1,000 of taxable value."])
    ws.append([])
    ws.append(["Taxing district", "Fund", "Levy (USD)", "Taxable value (USD)", "Rate per 1,000"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for name, fund, levy in LEVY:
        tv = taxable[name]
        ws.append([name, fund, levy, tv, round(1000.0 * levy / tv, 4)])
        ws.cell(ws.max_row, 3).number_format = "#,##0"
        ws.cell(ws.max_row, 4).number_format = "#,##0"
        ws.cell(ws.max_row, 5).number_format = "0.0000"
    for k, v in {"A": 38, "B": 20, "C": 14, "D": 18, "E": 13}.items():
        ws.column_dimensions[k].width = v
    wb.save(path)
