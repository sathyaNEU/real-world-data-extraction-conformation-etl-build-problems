"""The pack's document: Statistics Kellesay's plan for introducing supermarket transaction data into the RPI."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
TEAL = colors.HexColor("#0f4c5c")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14.5, leading=18, textColor=TEAL, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=9.5, leading=12.5, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(2.2 * cm, 1.4 * cm, footer)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.4 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.0 * cm,
                          bottomMargin=2.2 * cm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6eef0")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def write_plan(path):
    doc, frame = _doc(path, "RPI transaction data: introduction plan", W.ORG,
                      "%s  |  Retail Prices Index: introducing supermarket transaction data  |  Version 2, 24 June 2026"
                      % W.ORG)
    s = [Paragraph("Retail Prices Index: Introducing Supermarket Transaction Data", H1),
         Paragraph("%s. Introduction plan, version 2, approved by the Chief Statistician on 24 June 2026. Owner: %s, %s."
                   % (W.ORG, W.PEOPLE["prices"], W.TITLE["prices"]), H1S)]
    P_ = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Purpose", H2))
    P_("1.1", "From the January 2027 index the office intends to price the RPI's packaged grocery and household items "
              "from the sales records of the island's three supermarket groups, Wrenfold Stores, Gorsedale Co-operative "
              "and Calderby's, in place of the monthly field collection, item by item. This plan sets out the items, the "
              "parallel year on which each is assessed, the definitions used to put the supermarkets' records on one "
              "footing, and the test an item must pass before it moves.")
    s.append(Paragraph("2. Items and records", H2))
    P_("2.1", "The sixteen items in Table 1. Every other RPI item stays on its present sources in 2027.")
    s.append(_table([["Item code", "Item", "Item code", "Item"]] +
                    [[W.ITEMS[i][0], W.ITEMS[i][1], W.ITEMS[i + 8][0], W.ITEMS[i + 8][1]] for i in range(8)],
                    [2.0 * cm, 5.6 * cm, 2.0 * cm, 5.6 * cm]))
    s.append(Paragraph("Table 1. Items assessed for transaction data.", SMALL))
    P_("2.2", "Under the data supply agreements signed in 2025 each supermarket sends its full sales records: Wrenfold "
              "Stores weekly, Gorsedale Co-operative by fiscal period, Calderby's monthly as an extract of its "
              "point-of-sale database. Records for September 2025 to September 2026 form the parallel year, over which "
              "the field collection continued unchanged.")
    P_("2.3", "The agreements fix what each supermarket sends. Wrenfold Stores sends each week's sales by product, its "
              "weeks running Sunday to Saturday and dated by the Saturday that ends them. Gorsedale Co-operative sends its "
              "sales by fiscal week, its weeks running Monday to Sunday, with its fiscal calendar. Calderby's sends each "
              "month an extract of its point-of-sale database, one row for each store, day and product, a return being a "
              "row of negative units. Wrenfold's and Gorsedale's sales values include GST and Calderby's are net of it; "
              "GST is charged at 5 per cent on every item in Table 1.")
    s.append(Paragraph("3. Definitions", H2))
    P_("3.1", "<b>Product line.</b> A GTIN sold by one supermarket; the same GTIN at two supermarkets is two lines. A line "
              "belongs to the RPI item the office's product classification gives it.")
    P_("3.2", "<b>Month.</b> A day belongs to its calendar month. A supermarket's week belongs to the month in which the "
              "week ends; Gorsedale Co-operative's fiscal calendar gives the dates of its weeks.")
    P_("3.3", "<b>Monthly price.</b> A line's price in a month is its sales value including GST divided by its units sold "
              "in the month, returns netted.")
    P_("3.4", "<b>Lines compared.</b> The assessment of the parallel year covers the lines each supermarket sold in every "
              "month from September 2025 to September 2026.")
    P_("3.5", "<b>Index.</b> Each item's index from transaction data is compiled monthly over the lines compared, "
              "September 2025 = 100; a line counts in its item's price change by its share of the item's spending, as in "
              "a Törnqvist index.")
    P_("3.6", "<b>12-month rate.</b> An item's 12-month rate from transaction data is the percentage change in its index "
              "from September 2025 to September 2026, the change in the item's prices over the year.")
    P_("3.7", "<b>Field collection.</b> A collector who finds a sampled product unavailable on the day carries its last "
              "collected price, and the quote is marked T.")
    s.append(Paragraph("4. The test", H2))
    P_("4.1", "An item moves to transaction data from the January 2027 index when its 12-month rate from transaction data "
              "is within 1.5 percentage points of its published 12-month rate to September 2026, either way. An item "
              "further apart stays on the field collection for 2027 while the office examines the difference.")
    P_("4.2", "The notice of the January 2027 changes is published on 13 November 2026, two months before the index is "
              "compiled, as the Statistics Code requires.")
    s.append(Spacer(1, 10))
    s.append(Paragraph("Supersedes version 1 (3 February 2026), which proposed a six-month parallel run.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


