"""The pack's documents: the quality board paper on the 2027 register re-validation, the re-validation cost estimates
workbook, the data dictionary and the extract manifest."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import numpy as np    # noqa: E402

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5b6470")
GREEN = colors.HexColor("#2c5a3f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.4, leading=10.6, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)

MEMO = [
    ("1. Purpose", [
        "At its meeting on 18 November 2026 the quality board decides which regional business registers go to the 2027 "
        "re-validation exercise, in which every record of a region is checked against its source documents and "
        "corrected. The exercise is costed region by region in the estimates workbook; this paper fixes the basis on "
        "which regions are chosen."]),
    ("2. The test", [
        "A regional register goes to re-validation when the share of its records in error exceeds 4 per cent.",
        "A record is in error when one of the fields the register certifies (legal name, legal form, registered "
        "address, status and activity code) is wrong against the business's source documents. The share is over the "
        "region's records on the register on 30 April 2026, when the summer audit was drawn, active and since "
        "dissolved alike; records registered after 30 April are not part of it."]),
    ("3. The evidence", [
        "The summer 2026 quality audit checked a sample of the 30 April register against source documents between "
        "May and August, and each audited record's outcome is in the audit file. The audit's outcome codes changed on "
        "1 July with the new audit form. No other check of the register's accuracy is used."]),
    ("4. Alongside the decision", [
        "For each region the board will also see its new registrations in the third quarter of 2026, by the register's "
        "own quarter, which keeps Ardmuir local time, and the companies struck off and dissolved in the quarter that "
        "were still dissolved at its end, from the gazette's company notices."]),
]


def _frame(foot):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return frame


def _masthead(title):
    return [Paragraph(P.COMPANY.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4,
                                                        textColor=GREEN, leading=11)),
            Paragraph(title, ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18,
                                            textColor=INK, spaceAfter=6))]


def write_memo(path):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="Register re-validation 2027: basis of the choice",
                          author="Sally Phillips", subject="", creator="", producer="")
    head = [["To", "Quality board"], ["From", "Sally Phillips, Head of Register Quality"],
            ["Date", "7 October 2026"], ["Subject", "Business register re-validation 2027: which regions"]]
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead("Quality board paper") + [t, Spacer(1, 8)]
    for h, paras in MEMO:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    foot = "%s. Quality board paper QB/26/41, 7 October 2026." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_costs(path, x):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Re-validation costs"
    ws["A1"] = "%s: 2027 register re-validation, cost estimates by region" % P.COMPANY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Prepared for the quality board, September 2026. Unit costs from the 2023 Northmuir pilot."
    ws.append([])
    ws.append(["Region", "Region name", "Records to check", "Cost per record (GBP)", "Estimated cost (GBP)",
               "Weeks of fieldwork"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C5A3F")
    rng = np.random.default_rng(W.SEED + 9)
    for code, name, *_ in W.REGIONS:
        n = sum(1 for r in x["recs"] if r["region"] == code and r["frame"])
        unit = round(float(rng.uniform(3.1, 4.4)), 2)
        ws.append([code, name, n, unit, round(n * unit, -2), int(n / 900) + 2])
    for row in ws.iter_rows(min_row=5):
        row[2].number_format = "#,##0"
        row[4].number_format = "#,##0"
    for col, w in zip("ABCDEF", (8, 18, 15, 18, 18, 16)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["register"], "record_id", "the register's record number"),
        (f["register"], "region", "the regional register holding the record (codes from April 2025)"),
        (f["register"], "status", "active or dissolved at the extract"),
        (f["register"], "created_at_utc", "when the record was created, UTC"),
        (f["register"], "last_updated", "the date of the record's last change"),
        (f["screen"], "risk_score", "the screen's score, 0 to 1"),
        (f["screen"], "referred", "Y: referred to the regional team (score 0.70 or more)"),
        (f["audit"], "region_old", "the region under the codes before April 2025, which the audit system still uses"),
        (f["audit"], "outcome", "PASS or FAIL until 30 June 2026; from 1 July 0 no error, 1 legal name, 2 legal form, "
                                "3 registered address, 4 status or activity code"),
        (f["codes"], "region_old", "the code before 1 April 2025"),
        (f["gazette"], "notice_type", "first notice (proposal to strike off), struck off and dissolved, or restored to "
                                      "the register"),
        (f["gazette"], "gazette_date", "the date of publication, which is the date the notice takes effect"),
        (f["survey"], "mean_satisfaction", "mean rating, 1 to 5"),
        (f["returns"], "late_pct", "share of annual returns filed late, per cent"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["register"], "business register extract", "register operations", "2026-09-30", "all records", n["register"]),
        (f["screen"], "risk screen referral list", "register operations", "2026-05-04", "screen run of 4 May 2026",
         n["screen"]),
        (f["audit"], "summer quality audit outcomes", "register quality", "2026-09-05", "May to August 2026",
         n["audit"]),
        (f["codes"], "regional code crosswalk", "register operations", "2025-04-01", "", n["codes"]),
        (f["gazette"], "company notices", "Ardmuir Gazette", "2026-10-02", "July to September 2026", n["gazette"]),
        (f["paper"], "quality board paper", P.COMPANY, "2026-10-07", "", ""),
        (f["costs"], "re-validation cost estimates", "register quality", "2026-09-22", "2027", 14),
        (f["survey"], "register user survey", P.COMPANY, "2025-12-12", "2025", n["survey"]),
        (f["returns"], "annual return compliance", "register operations", "2026-03-31", "2025", n["returns"]),
        (f["dictionary"], "field descriptions", P.COMPANY, "2026-10-08", "", n["dictionary"]),
    ]
