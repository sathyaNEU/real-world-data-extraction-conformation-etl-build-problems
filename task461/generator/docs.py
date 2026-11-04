"""The pack's documents: Schedule 9 (sustainability KPIs) of the Corvane Bank facility agreement and the
building's 2024 energy performance certificate."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6066")
TEAL = colors.HexColor("#0f4c5c")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.2, leading=13.8, textColor=INK, spaceAfter=5)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=TEAL, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.6, leading=12.5, textColor=GREY, spaceAfter=9)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                    spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.6, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.2, leading=10.5, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6ecee")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


# ------------------------------------------------------------------------------------------------- the licence
def write_schedule(path):
    doc, frame = _doc(path, "Schedule 9: Sustainability Performance", W.BANK,
                      "Facility agreement dated 14 March 2025 between %s and %s  |  Schedule 9" % (W.ORG, W.BANK))
    s = [Paragraph("Schedule 9: Sustainability Performance Targets and KPI Reporting", H1),
         Paragraph("Revolving credit facility agreement dated 14 March 2025 between %s (the Borrower) and %s (the "
                   "Agent). This Schedule applies to the Building for each Measurement Period from 2025." % (W.ORG, W.BANK),
                   SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("Part 1. Definitions", H2))
    p("1.1", "<b>Building</b> means %s." % W.ADDRESS)
    p("1.2", "<b>Measurement Period</b> means a calendar year, 1 January to 31 December, in the local time of the "
             "Building; a quarter is three calendar months of a Measurement Period.")
    p("1.3", "<b>Tenancy</b> means each part of the Building let or licensed to an occupier, including any licence of "
             "the roof.")
    p("1.4", "<b>Base Building Electricity</b> means the electricity imported to the Building through the revenue "
             "meter (MPAN %s) in the Measurement Period, less the electricity supplied in that period to the Tenancies "
             "as metered at each Tenancy's supply." % W.MPAN)
    p("1.5", "<b>Net Lettable Area</b> means %s square metres." % "{:,}".format(W.NLA_M2))
    s.append(Paragraph("Part 2. Key Performance Indicator", H2))
    p("2.1", "<b>Base Building Scope 2 Emissions</b> means Base Building Electricity multiplied by %s kg CO2e per kWh."
             % W.FACTOR_KG_PER_KWH)
    p("2.2", "<b>KPI</b> means Base Building Scope 2 Emissions divided by Net Lettable Area, in kg CO2e per square "
             "metre.")
    s.append(Paragraph("Part 3. Sustainability Performance Targets", H2))
    s.append(_table([["Measurement Period", "Target (kg CO2e per m2, not more than)"],
                     ["2025", "18.4"], ["2026", "%.1f" % W.TARGET_KG_M2], ["2027", "16.8"], ["2028", "16.0"]],
                    [50 * mm, 80 * mm]))
    s.append(Spacer(1, 5))
    p("3.1", "Where the KPI for a Measurement Period exceeds its Target, the Margin increases by 2.5 basis points for "
             "the following year; where it is at or below the Target, the Margin decreases by 2.5 basis points.")
    s.append(Paragraph("Part 4. Reporting", H2))
    p("4.1", "By 31 January after each Measurement Period the Borrower delivers a KPI report giving the KPI against "
             "its Target, verified by an external reviewer, with the Building's Scope 1 lines.")
    p("4.2", "<b>Gas oil:</b> the litres burned by the Building's standby generator in each quarter, at %s kg CO2e per "
             "litre." % W.DIESEL_KG_PER_L)
    p("4.3", "<b>Refrigerant:</b> the refrigerant released from each chiller in the Measurement Period, at a global "
             "warming potential of %s for R-134a." % "{:,}".format(W.GWP_R134A))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Executed as part of the Agreement.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_epc(path):
    doc, frame = _doc(path, "Energy Performance Certificate", "Halden Energy Assessors",
                      "Non-domestic EPC  |  certificate 0624-7713-4402-9187-3051  |  valid until 17 October 2034")
    s = [Paragraph("Energy Performance Certificate: Non-Domestic Building", H1),
         Paragraph("%s. Certificate 0624-7713-4402-9187-3051, issued 18 October 2024, valid until 17 October 2034. "
                   "Assessor: Halden Energy Assessors." % W.ADDRESS, SUB)]
    s.append(_table([["Asset rating", "Band", "Building emission rate (kg CO2/m2 per year)", "Main heating fuel",
                      "Total useful floor area (m2)"],
                     ["63", "C", "38.21", "Natural gas", "27,940"]],
                    [22 * mm, 14 * mm, 52 * mm, 30 * mm, 42 * mm]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("The asset rating compares the building's modelled performance, under standard occupancy and "
                       "standard operating conditions, with a reference building of the same type. It is a rating of "
                       "the building fabric and services as designed, not of the energy the building uses in operation.",
                       BODY))
    s.append(Paragraph("Recommendations: replace the remaining T8 fluorescent lighting in the car park with LED; "
                       "variable speed drives on the condenser water pumps; review the chiller sequencing set points.",
                       BODY))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
