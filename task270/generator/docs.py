"""task270 document: the network's program guidelines for the 2028 to 2030 late-life frailty program. Its text is data
here so checks.py and verify.py can quote and execute it."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2a30")
GREY = colors.HexColor("#5d6870")
ACCENT = colors.HexColor("#0f5c6e")
RULE = colors.HexColor("#b9c6cc")
HEAD = colors.HexColor("#e3eef1")

TITLE = "Late-life frailty program 2028 to 2030: program guidelines"
REF = "Version 1.0, 2 September 2027"
AREAS_TEXT = ", ".join(sorted(K.AREA_NAMES)[:-1]) + " and " + sorted(K.AREA_NAMES)[-1]

GUIDE = [
    ("1 Purpose", [
        "The late-life frailty program commissions three services for residents aged 85 and over from 1 January 2028 "
        "to 31 December 2030: frailty screening and care planning in general practice, a falls prevention service "
        "delivered at home and in residential aged care, and after-hours palliative support. It is funded under the "
        "Commonwealth's schedule for the network's primary care programs for 2028 to 2030, and the network's executive "
        "approves the areas it goes to before the activity work plan is lodged with the Department."]),
    ("2 Areas", [
        "The network covers twelve local government areas on their boundaries of 1 July 2023: %s. The program goes to "
        "the whole of each area it names." % AREAS_TEXT]),
    ("3 Which areas the program goes to", [
        "3.1 The program goes to each area whose residents reaching 85 could expect to live fewer than seven more "
        "years under the area's death rates of 2024 to 2026.",
        "3.2 An area's life expectancy at 85 is the average number of further years a person reaching 85 would live "
        "if the area's 2024 to 2026 death rate at each age held for the rest of their life. The rates run by single "
        "year of age from 85 to 94, with 95 and over as the last group. A death rate is deaths per year lived at that "
        "age: a person who dies at an age has lived half of that year of age, and the years lived at 95 and over are "
        "the survivors to 95 divided by that group's death rate.",
        "3.3 The death rate at an age is the number of the area's usual residents who died at that age (in completed "
        "years at the date of death) in 2024, 2025 or 2026, wherever the death was registered, divided by the sum of "
        "the area's estimated resident population of that age at 30 June 2024, 30 June 2025 and 30 June 2026.",
        "3.4 An area is named on its unrounded life expectancy at 85. The guidelines report it in years to one decimal "
        "place."]),
    ("4 Data", [
        "Deaths are the registrations of the deaths of the network's usual residents that the NSW Registry of Births, "
        "Deaths and Marriages releases to the network under data release agreement DRA-2025-117, with the deaths of "
        "the network's residents registered in other states and territories, which the Australian Bureau of Statistics "
        "supplies. Populations are the Australian Bureau of Statistics' estimated resident population. A resident's "
        "area is the 2023 local government area of their usual residence's 2021 SA2, as the ABS correspondence "
        "assigns it."]),
    ("5 After-hours palliative support", [
        "Since 2019 the network has commissioned %s to make after-hours home visits across the region, at private "
        "residences and in residential aged care, on weekday evenings and nights, at weekends and on public holidays. "
        "From 2028 the program funds the service's palliative visits to residents aged 85 and over in the areas it "
        "names and adds a second clinician on call for them. A resident is aged 85 and over for a visit when they are "
        "85 or older on the day of the visit, and belongs to the area of the residence the service attends." %
        K.AH_SERVICE]),
    ("6 Approval", [
        "The executive approves the program's areas at its October 2027 meeting. The areas are not reviewed during "
        "2028 to 2030, and an area added or removed after that meeting waits for the 2031 program."]),
]

CONTROL = [("Owner", "%s, Executive Manager, Commissioning" % K.PEOPLE["commissioning"]),
           ("Contact", "%s, Manager, Population Health Planning" % K.PEOPLE["planning"]),
           ("Prepared by", "%s, Senior Data Analyst" % K.PEOPLE["analyst"]),
           ("Version", REF)]


def text_of_sections(secs):
    return " ".join(" ".join(ps) for _h, ps in secs)


def _styles():
    return dict(
        title=ParagraphStyle("t", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4),
        sub=ParagraphStyle("s", fontName="LibSans", fontSize=9, leading=12, textColor=GREY, spaceAfter=10),
        h=ParagraphStyle("h", fontName="LibSans-Bold", fontSize=10.5, leading=14, textColor=ACCENT, spaceBefore=8,
                         spaceAfter=3),
        p=ParagraphStyle("p", fontName="LibSans", fontSize=9.5, leading=13.2, textColor=INK, spaceAfter=5),
        cell=ParagraphStyle("c", fontName="LibSans", fontSize=8.5, leading=10.5, textColor=INK),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("LibSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(2 * cm, 1.2 * cm, text)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths):
    st = _styles()
    data = [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.25, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (0, -1), HEAD),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def write_guidelines(path):
    st = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, title=TITLE, author=K.PHN, subject="", creator="", producer="")
    flow = [Paragraph(K.PHN, st["sub"]), Paragraph(TITLE, st["title"]), Paragraph(REF, st["sub"])]
    for head, paras in GUIDE:
        flow.append(Paragraph(head, st["h"]))
        for p in paras:
            flow.append(Paragraph(p, st["p"]))
    flow.append(Spacer(1, 10))
    flow.append(_table([list(r) for r in CONTROL], [3.2 * cm, 13.8 * cm]))
    foot = "%s  |  Late-life frailty program guidelines  |  %s" % (K.PHN_SHORT, REF)
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
