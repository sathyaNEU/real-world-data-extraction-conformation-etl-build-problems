"""The pack's documents: the plan's programme criteria for its 2027 Pancreatic Surgery Centres, the consortium's guide
to its hepatobiliary and pancreatic research files, and the pack's contents."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
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
INK, GREY, RULE = colors.HexColor("#1f2428"), colors.HexColor("#5d646a"), colors.HexColor("#b8bfc4")
PLUM = colors.HexColor("#5b2a6e")
LAKE = colors.HexColor("#1d4f73")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(.8 * inch, letter[1] - .5 * inch, left)
        canvas.drawRightString(letter[0] - .8 * inch, letter[1] - .5 * inch, right)
        canvas.drawRightString(letter[0] - .8 * inch, .45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=.85 * inch, rightMargin=.85 * inch,
                             topMargin=.8 * inch, bottomMargin=.75 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


CITY = {"A": "Madison", "B": "Milwaukee", "C": "Green Bay", "D": "La Crosse", "E": "Wausau", "F": "Eau Claire",
        "G": "Appleton", "H": "Kenosha"}


# ---------------------------------------------------------------------------------------------- the criteria
def write_criteria(path):
    S = styles("Sans", PLUM)
    doc = _doc(path, "%s: 2027 programme criteria" % K.PROGRAMME, K.PLAN)
    hosp = [["Hospital", "City", "ULHDC hospital ID"]]
    for c in K.ELIGIBLE:
        hosp.append([K.NAME[c], CITY[c], K.NEW_NO[c]])
    appx = [["ICD-10-PCS", "Description"]] + [[c, d] for c, d in K.RESECTION.items()]
    s = [Paragraph("%s: 2027 programme criteria" % K.PROGRAMME, S["h1"]),
         Paragraph("%s, Network Strategy. Version 2, 30 September 2026, for the Board of Directors' meeting of "
                   "17 November 2026. Prepared by %s, Director of Network Strategy." % (K.PLAN, K.PEOPLE["requester"]),
                   S["meta"]),
         Paragraph("1. The programme", S["h2"]),
         Paragraph("From 1 January 2027, a member who has a pancreatic resection at one of the cooperative's "
                   "Pancreatic Surgery Centres pays no deductible, copayment or coinsurance for the stay, and the "
                   "cooperative pays travel and lodging for the operation and the follow-up visits. The benefit applies "
                   "in every line of business. The board names three centres for 2027 and reviews the choice each "
                   "year.", S["body"]),
         Paragraph("2. Eligible hospitals", S["h2"]),
         Paragraph("A hospital is eligible if it performed 20 or more pancreatic resections in each of 2023, 2024 and "
                   "2025 by the %s's research files. Eight Wisconsin hospitals are eligible:" % K.CONSORTIUM,
                   S["body"]),
         _table(S, hosp, [3.1, 1.4, 1.5]),
         Spacer(1, 4),
         Paragraph("3. How the board compares the eligible hospitals", S["h2"]),
         _clause(S, "3.1", "The board compares the eight hospitals on how often patients died after a pancreatic "
                           "resection there, against how often those same patients would have died given their "
                           "condition before surgery."),
         _clause(S, K.CLAUSE["population"], "Operations: every pancreatic resection (Appendix A) performed at the hospital on a "
                           "patient aged 18 or over, with an operation date from 1 January 2023 to 31 December 2025, "
                           "in the consortium's hepatobiliary and pancreatic research files. Each operation counts, so "
                           "a patient operated on twice in the period counts twice."),
         _clause(S, K.CLAUSE["deaths"], "Deaths: a death from any cause within 90 days of the operation date, in or out of "
                           "hospital, from the consortium's death linkage. A death after a transfer counts for the "
                           "hospital that operated."),
         _clause(S, K.CLAUSE["expected"], "Expected deaths: the deaths the same patients' condition before surgery would have "
                           "produced at the eight hospitals together, over the same three years. A hospital's ratio is "
                           "its deaths divided by its expected deaths."),
         _clause(S, K.CLAUSE["comparison"], "The three hospitals with the lowest ratios become the 2027 centres. The board compares "
                           "the ratios unrounded and reports them to one decimal."),
         Paragraph("4. Contracting", S["h2"]),
         Paragraph("Network Strategy contracts the three centres for 2027 at case rates. For each eligible hospital the "
                   "board also sees its record of pancreatic resections since 2016, its resections in 2026 so far and what "
                   "the cooperative allowed for its own members' resection stays there.", S["body"]),
         Paragraph("Appendix A. Pancreatic resection", S["h2"]),
         Paragraph("A discharge record carrying any of these procedure codes is a pancreatic resection; the operation "
                   "date is the date recorded for that code.", S["body"]),
         _table(S, appx, [1.3, 4.6])]
    doc.build(s, onFirstPage=_frame(K.PLAN, "Pancreatic Surgery Centres 2027, v2", "Sans"),
              onLaterPages=_frame(K.PLAN, "Pancreatic Surgery Centres 2027, v2", "Sans"))


# ---------------------------------------------------------------------------------------------- the file guide
FW_A = [("1-10", "Record number"), ("11-14", "Hospital number"), ("15-30", "Person key"), ("31", "Sex"),
        ("32-34", "Age (years)"), ("35-42", "Admission date (YYYYMMDD)"), ("43-50", "Discharge date (YYYYMMDD)"),
        ("51", "Admission type"), ("52", "Admission source"), ("53-54", "Discharge status"), ("55", "Payer category"),
        ("56-127", "Diagnoses 1 to 9: code (7, no decimal point) then present-on-admission indicator (1)"),
        ("128-169", "Procedures 1 to 6 (7 each)"), ("170-177", "Date of procedure 1 (YYYYMMDD)")]


def write_guide(path):
    S = styles("Serif", LAKE)
    doc = _doc(path, "Hepatobiliary and pancreatic research files: file guide", K.CONSORTIUM)
    fw = [["Columns", "Field"]] + [[a, b] for a, b in FW_A]
    codes = [["Field", "Values"],
             ["Admission type", "1 emergency, 2 urgent, 3 elective, 9 unknown"],
             ["Admission source", "1 non-health care point of origin, 2 clinic or physician referral, 4 transfer from a "
                                  "hospital, 5 transfer from a skilled nursing facility, 7 emergency department"],
             ["Discharge status", "01 home or self-care, 02 short-term general hospital, 03 skilled nursing facility, "
                                  "06 home health care, 07 left against medical advice, 20 expired, 30 still a "
                                  "patient, 50 hospice (home), 51 hospice (facility), 62 inpatient rehabilitation"],
             ["Payer category", "1 Medicare, 2 Medicare Advantage, 3 Medicaid or BadgerCare, 5 commercial, 9 self-pay"],
             ["Present on admission", "Y present at the time of the inpatient admission, N not present, U documentation "
                                      "insufficient, W clinically undetermined, 1 or blank exempt from reporting"]]
    s = [Paragraph("Hepatobiliary and pancreatic research files: file guide", S["h1"]),
         Paragraph("%s, Data Services. 2026 edition, 22 September 2026. Contact: %s." % (K.CONSORTIUM, K.PEOPLE["analyst"]),
                   S["meta"]),
         Paragraph("1. What the files hold", S["h2"]),
         Paragraph("One record for each inpatient discharge from a member hospital that carries at least one ICD-10-PCS "
                   "procedure in body system F (hepatobiliary system and pancreas). Records are filed by discharge "
                   "date: the 2016 file holds the discharges from 1 January to 31 December 2016, and so on. The "
                   "diagnoses and procedures are as the hospital coded and submitted them.", S["body"]),
         Paragraph("2. Files and layouts", S["h2"]),
         _clause(S, "2016-2018", "One fixed-width text file a year, one record a line. The 2018 file inserts the "
                                 "patient's county code (2 characters) after the payer category, so every later field "
                                 "moves two columns to the right. The 2016 and 2017 layout:"),
         _table(S, fw, [1.0, 4.9]),
         Spacer(1, 4),
         _clause(S, "2019-2022", "One comma-separated file for the four years. Twenty-five diagnosis slots, each with "
                                 "its present-on-admission indicator, and twenty-five procedure slots, each with the date "
                                 "the procedure was performed. Codes are written without the decimal point; dates as "
                                 "MM/DD/YYYY."),
         _clause(S, "2023-2025", "One comma-separated file for the three years, with the six-digit hospital IDs "
                                 "introduced on 1 January 2023, renamed columns, codes written with the decimal point "
                                 "and ISO dates."),
         _clause(S, "2026", "A preliminary release of the first quarter's discharges (15 May 2026) and a revised "
                            "release of the first and second quarters' (18 September 2026), which takes the place of the "
                            "preliminary release, both in the 2023-2025 layout. Record numbers are assigned when a "
                            "release is cut."),
         Paragraph("3. Fields and codes", S["h2"]),
         Paragraph("The person key is the consortium's encrypted linkage key, built from the name, date of birth and "
                   "sex the hospital submits. It is the same on every discharge of the same person at any member "
                   "hospital in any year. It is blank where a hospital did not submit the identifiers, which happened "
                   "for about one record in a hundred before 2019. Age is in completed years at admission.", S["body"]),
         _table(S, codes, [1.4, 4.5]),
         Spacer(1, 4),
         Paragraph("Before 2019 only the first procedure carries a date. Procedure classes for every procedure code "
                   "that appears in the files are in ulhdc_procedure_classes.csv, and hospital numbers and IDs, with "
                   "the changes to them, in ulhdc_hospital_directory.xlsx.", S["body"]),
         Paragraph("4. Death linkage", S["h2"]),
         Paragraph("Each year the consortium links every person key in the research files to the state death index. "
                   "The 2026 run (31 August 2026) covers deaths in Wisconsin from 1 January 2016 to 31 August 2026; "
                   "deaths outside Wisconsin are not captured. Where a death record gives the month but not the day, "
                   "the day is set to the 15th and the record flagged.", S["body"]),
         Paragraph("5. Using the files", S["h2"]),
         Paragraph("Research files are released to member hospitals and to payers that hold a data use agreement with "
                   "the consortium. Counts under 11 may not be published.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.CONSORTIUM, "Research file guide 2026", "Serif"),
              onLaterPages=_frame(K.CONSORTIUM, "Research file guide 2026", "Serif"))


def write_contents(path, items):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("Pancreatic Surgery Centres 2027: board pack evidence files\n")
        f.write("Corrisbrook Health Cooperative, Network Strategy, assembled 9 October 2026\n\n")
        for name, desc in items:
            f.write("%s\n    %s\n" % (name, desc))
