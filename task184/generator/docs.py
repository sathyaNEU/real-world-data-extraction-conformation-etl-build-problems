"""task184 documents: the company's avian influenza surveillance protocol FP-AI-03, the prevention zone notice, and
the farm register workbook."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W  # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
SANS, SANS_B = "LiberationSans", "LiberationSans-Bold"
INK = colors.HexColor("#1f2421")
GREY = colors.HexColor("#5f665f")
GREEN = colors.HexColor("#2f5d3a")
BODY = ParagraphStyle("body", fontName=SANS, fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=9 * mm, firstLineIndent=-9 * mm)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=14.5, leading=18, textColor=GREEN, spaceAfter=2)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=10.4, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
META = ParagraphStyle("meta", fontName=SANS, fontSize=8.0, leading=10.6, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)

PROTOCOL_TEXT = {
    "title": "FP-AI-03  Avian influenza surveillance on contract farms",
    "meta": "Fosdyke Poultry Ltd, Flock Health. Issue 4, effective 2 November 2026 for the 2026-27 season. "
            "Owner: Annette Begum, Head of Flock Health. Supersedes issue 3 (October 2025).",
    "clauses": [
        ("1", "Purpose", [
            ("1.1", "This protocol sets how Flock Health decides, each week of the season, which contract farms it "
                    "visits to swab for avian influenza, so that an infection on a farm is found while it is still "
                    "small. It sits alongside, and does not replace, every keeper's legal duty to report suspicion of "
                    "avian influenza to APHA at once."),
        ]),
        ("2", "The week's measure", [
            ("2.1", "Every contract farm with birds on site on the Sunday is in the week's review."),
            ("2.2", "For each farm the measure is the number of birds avian influenza killed on the farm, across all "
                    "its houses, in the five recording days Wednesday to Sunday, read from the growers' daily "
                    "returns."),
            ("2.3", "A return belongs to the recording day the grower enters it for, whenever it is submitted. Birds "
                    "the grower records as found dead count; birds the grower culls do not."),
            ("2.4", "Ordinary deaths are what the company's own crops cleared in 2025 and 2026 show of the deaths a "
                    "crop has when it is not infected."),
        ]),
        ("3", "Swabbing", [
            ("3.1", "On Monday's round the team swabs every farm where avian influenza killed more than 150 birds "
                    "in the five days. A farm at 150 or fewer is not swabbed that week."),
            ("3.2", "Each swabbed farm gives one pooled oropharyngeal and cloacal sample of up to five fresh dead "
                    "birds per house. A positive or inconclusive result is reported to APHA the same day and the "
                    "farm's movements stop until APHA has visited."),
            ("3.3", "The list, with the birds the infection killed on each farm and in each of its houses, goes to "
                    "the Agriculture Director by 08:00 on Monday."),
        ]),
    ],
}


def frame(org_line, left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(1.1)
        canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
        canvas.setFont(SANS_B, 7.6)
        canvas.setFillColor(GREEN)
        canvas.drawString(18 * mm, A4[1] - 12 * mm, org_line)
        canvas.setFont(SANS, 7.3)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 11 * mm, left)
        canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")


def write_protocol(path):
    T = PROTOCOL_TEXT
    story = [Paragraph(T["title"], H1), Paragraph(T["meta"], META)]
    for num, head, cl in T["clauses"]:
        story.append(Paragraph("%s  %s" % (num, head), H2))
        for n, text in cl:
            story.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (n, text), CLAUSE))
    story.append(Spacer(1, 6 * mm))
    story.append(Table([[Paragraph("Issue", CELLB), Paragraph("Date", CELLB), Paragraph("Change", CELLB)],
                        [Paragraph("3", CELL), Paragraph("20 October 2025", CELL),
                         Paragraph("Annual review; the measure and the line unchanged.", CELL)],
                        [Paragraph("4", CELL), Paragraph("2 November 2026", CELL),
                         Paragraph("Recording days set as Wednesday to Sunday; swabs taken on Monday's round.", CELL)]],
                       colWidths=[18 * mm, 34 * mm, 118 * mm],
                       style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, GREY),
                                         ("VALIGN", (0, 0), (-1, -1), "TOP")])))
    d = _doc(path, "FP-AI-03 Avian influenza surveillance on contract farms", "Annette Begum")
    fr = frame("FOSDYKE POULTRY LTD  |  FLOCK HEALTH", "FP-AI-03 issue 4", "Controlled when printed from the QMS")
    d.build(story, onFirstPage=fr, onLaterPages=fr)


AIPZ_TEXT = [
    ("Declaration", "An Avian Influenza Prevention Zone (AIPZ) is declared across England under the Avian "
     "Influenza and Influenza of Avian Origin in Mammals (England) (No. 2) Order 2006, from 12:00 on Tuesday 3 "
     "November 2026, until it is withdrawn."),
    ("Housing measures", "From 00:01 on Monday 30 November 2026 every keeper of poultry in England must house their "
     "birds or, where housing is not practicable, keep them separate from wild birds. The housing measures apply "
     "whatever the size of the flock."),
    ("Biosecurity", "Keepers of more than 500 birds must restrict access to non-essential people, change clothing "
     "and footwear before entering bird enclosures, cleanse and disinfect vehicles entering and leaving the premises, "
     "and keep records of every person and vehicle entering any part of the premises where birds are kept."),
    ("Vehicles and catching teams", "Vehicles, crates, modules and equipment used for catching and transporting "
     "birds must be cleansed and disinfected before arrival at the premises and before leaving it. Catching teams "
     "must change protective clothing between premises."),
    ("Wild birds", "Keepers must not let wild birds reach feed, water or bedding, and must cover feed and bedding "
     "stores. Dead wild birds found on the premises should be reported to the Defra helpline and must not be "
     "handled."),
]


def write_aipz(path):
    story = [Paragraph("Avian Influenza Prevention Zone: mandatory housing measures", H1),
             Paragraph("Declaration by the Chief Veterinary Officer for the United Kingdom, as it applies to keepers "
                       "in England. Issued 26 November 2026.", META)]
    for head, text in AIPZ_TEXT:
        story.append(Paragraph(head, H2))
        story.append(Paragraph(text, BODY))
    d = _doc(path, "Avian Influenza Prevention Zone: mandatory housing measures", "Animal and Plant Health Agency")
    fr = frame("ANIMAL AND PLANT HEALTH AGENCY", "AIPZ declaration, England", "26 November 2026")
    d.build(story, onFirstPage=fr, onLaterPages=fr)


def write_farm_register(path, header, rows):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Farms and houses"
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    widths = [10, 30, 28, 18, 13, 14, 12, 30, 7, 22, 13]
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"
    wb.save(path)
