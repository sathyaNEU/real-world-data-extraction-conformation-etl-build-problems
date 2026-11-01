"""The pack's documents: SOP 2.10 (call answering and answer-time reporting) and the FY2028 recommended budget's
communications floor page (PDF). Their text is kept here as data so checks.py can quote and execute it, and checks.py
reads each one back from the shipped PDF through the verifier's extractor. No file in the pack describes the data
(dataset-generation section 3): provenance lives in metadata.json."""
from __future__ import annotations

import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"),
               ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d232b")
GREY = colors.HexColor("#5d6672")
RED = colors.HexColor("#8a1c1c")       # the agency's maroon
BLUE = colors.HexColor("#22436b")      # the county budget office's blue

BODY = ParagraphStyle("body", fontName="Carlito", fontSize=10.5, leading=14.0, textColor=INK, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Carlito-Bold", fontSize=15.0, leading=19, textColor=RED, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName="Carlito", fontSize=9.2, leading=12.0, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="Carlito-Bold", fontSize=11.2, leading=14.5, textColor=RED, spaceBefore=8, spaceAfter=3)
B_BODY = ParagraphStyle("bb", fontName="LibSans", fontSize=9.6, leading=12.8, textColor=INK, spaceAfter=5)
B_H1 = ParagraphStyle("bh1", fontName="LibSans-Bold", fontSize=13.0, leading=16.5, textColor=BLUE, spaceAfter=2)
B_H1S = ParagraphStyle("bh1s", fontName="LibSans", fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=9)
B_H2 = ParagraphStyle("bh2", fontName="LibSans-Bold", fontSize=10.2, leading=13.0, textColor=BLUE, spaceBefore=7,
                      spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LibSans", fontSize=8.6, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LibSans-Bold", fontSize=8.6, leading=10.6, textColor=INK)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                             topMargin=0.85 * inch, bottomMargin=0.85 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(left, right, font="Carlito"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.5 * inch, left)
        canvas.drawRightString(letter[0] - 1.0 * inch, 0.5 * inch, "%s%s" % (right, doc.page))
        canvas.restoreState()
    return draw


# ---------------------------------------------------------------------------------------------------- SOP 2.10
F_SOP = "sop_2-10_call_handling_standard_and_reporting.pdf"
SOP = [
    ("1", "Purpose and scope", "scope", [
        "1.1 This procedure sets the agency's 911 call-answering standard and how answer-time compliance is measured, "
        "reported and planned for. It applies to every call-taking position on the 911 floor.",
        "1.2 The agency's fiscal year runs from 1 July to 30 June; fiscal 2026 is the year from 1 July 2025 to "
        "30 June 2026, its quarters starting on 1 July, 1 October, 1 January and 1 April. The days, months, quarters "
        "and years the agency reports are local (Central) calendar dates."]),
    ("2", "The standard", "standard", [
        "2.1 Ninety per cent of 911 calls presented to the agency are answered within 15 seconds.",
        "2.2 The standard covers every 911 call presented to the agency's 911 queue, calls transferred in from other "
        "PSAPs included. Calls on the administrative lines are not 911 calls; neither are test calls."]),
    ("3", "Measurement", "measure", [
        "3.1 A call is presented when it reaches the agency's 911 queue: the i3 queue entry on NG911, or the trunk "
        "seizure on the CAMA trunks before the cutover. It is answered when it is connected to a call-taker's "
        "position.",
        "3.2 A call abandoned within 5 seconds of presentation is treated as a misdial and left out of the measure.",
        "3.3 Answer-time compliance for a period is the number of 911 calls answered within 15 seconds of "
        "presentation divided by the number of 911 calls presented in the period, less the calls abandoned within "
        "5 seconds of presentation."]),
    ("4", "Positions", "positions", [
        "4.1 Call-taking positions run on auto-answer: a call is delivered to a call-taker in Ready and connected with "
        "a tone, and the caller is on the line at once.",
        "4.2 A position takes no new call until the call-taker sets Ready again after the call's after-call work and "
        "CAD entry.",
        "4.3 The floor supervisor and the callback desk do not take calls from the 911 queue."]),
    ("5", "Staffing", "staffing", [
        "5.1 Minimum floor staffing for each block of each fiscal year is planned against the Tri-County Regional 911 "
        "Board's published hourly volume forecast for the agency for that year.",
        "5.2 Floor blocks start at 02:00, 06:00, 10:00, 14:00, 18:00 and 22:00. A block that runs past midnight "
        "belongs to the day it starts."]),
    ("6", "Reporting", "reporting", [
        "6.1 Quality assurance reports compliance monthly, for the floor and for each block. A shift's calls are "
        "reported in the month the shift starts.",
        "6.2 Calls are reported by where they were placed from, a wireless call by the last handset location "
        "received for it."]),
    ("7", "Abandoned calls", "abandoned", [
        "7.1 Every abandoned 911 call is called back by the callback desk, however briefly the caller held on. The "
        "desk aims to dial each one within two minutes of the hang-up."]),
]


def sop_sentences(key=None):
    out = []
    for _, _, k, paras in SOP:
        if key is None or k == key:
            out += [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9])", p)]
    return out


def write_sop(path):
    s = [Paragraph("%s &middot; Standard Operating Procedure 2.10 &middot; Revision 4" % K.AGENCY, H1S),
         Paragraph("Call answering and answer-time reporting", H1),
         Paragraph("Effective 1 July 2025; supersedes Revision 3 (1 August 2022). Owner: %s, Operations Manager. "
                   "Reviewed each year with the budget." % K.PEOPLE["ops"], H1S)]
    for num, head, _, paras in SOP:
        s.append(Paragraph("%s&nbsp;&nbsp;%s" % (num, head), H2))
        for p in paras:
            s.append(Paragraph(p.replace("&", "&amp;"), BODY))
    doc = _doc(path, "SOP 2.10 Call answering and answer-time reporting", K.PEOPLE["ops"])
    f = _footer("%s  |  SOP 2.10 Rev. 4  |  Internal" % K.AGENCY_SHORT, "Page ")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the budget page
F_BUDGET = "fy2028_recommended_budget_communications_floor.pdf"
BUDGET_ROWS = [
    ("02:00 to 06:00", "3", "3", ""),
    ("06:00 to 10:00", "4", "4", ""),
    ("10:00 to 14:00", "6", "6", ""),
    ("14:00 to 18:00", "6", "6", ""),
    ("18:00 to 22:00", "5", "5", ""),
    ("22:00 to 02:00, nights starting Sunday to Thursday", "4", "4", ""),
    ("22:00 to 02:00, nights starting Friday and Saturday", "5", "4",
     "The fifth call-taker is paid by the state 911 surcharge staffing grant, which ends on 30 June 2027."),
]
BUDGET_TEXT = [
    "The recommended budget holds the communications floor at its fiscal 2027 staffing in every block except the "
    "Friday and Saturday late shift, where the grant-funded fifth call-taker ends with the grant. Halvorsen Township's "
    "911 calls come to the agency on 1 July 2027 under the township's new service agreement, which pays the agency "
    "$412,800 a year for call-taking and dispatch.",
    "The board asked for the months of fiscal 2028, if any, in which a seasonal fifth call-taker should cover the "
    "Friday and Saturday late shift. A seasonal call-taker on overtime costs $468 a night, four hours at the "
    "overtime rate with benefits; the operations manager brings the request with the final budget in May 2027.",
]


def write_budget(path):
    s = [Paragraph("Tavish County &middot; FY2028 Recommended Budget &middot; Public Safety", B_H1S),
         Paragraph("%s: communications floor staffing" % K.AGENCY, B_H1),
         Paragraph("Budget office draft for the agency board's work session, 2 October 2026. Prepared by %s, "
                   "Finance Director." % K.PEOPLE["finance"], B_H1S),
         Paragraph("Call-takers on the 911 floor, by block", B_H2)]
    data = [[Paragraph("Block", CELLB), Paragraph("FY2027 adopted", CELLB), Paragraph("FY2028 recommended", CELLB),
             Paragraph("Note", CELLB)]]
    for blk, a, b, note in BUDGET_ROWS:
        data.append([Paragraph(blk, CELL), Paragraph(a, CELL), Paragraph(b, CELL), Paragraph(note, CELL)])
    t = Table(data, colWidths=[2.15 * inch, 0.85 * inch, 1.0 * inch, 2.5 * inch])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa4b0")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6ebf2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    s.append(Spacer(1, 8))
    for p in BUDGET_TEXT:
        s.append(Paragraph(p.replace("&", "&amp;").replace("$", "&#36;"), B_BODY))
    doc = _doc(path, "FY2028 Recommended Budget: communications floor staffing", K.PEOPLE["finance"])
    f = _footer("Tavish County Budget Office  |  FY2028 recommended  |  Draft", "Page ", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)
