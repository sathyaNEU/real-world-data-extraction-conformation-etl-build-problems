"""The folder's three documents: Schedule 3 of the logistics services agreement (the service levels), Siersma's
packaging change notification for the Daily range, and the site's December 2026 service close-out."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import postprocess as PP  # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#202124")
GREY = colors.HexColor("#5f6368")
NAVY = colors.HexColor("#1f3b5c")
TEAL = colors.HexColor("#2e6f6a")
BODY = ParagraphStyle("body", fontName="LiberationSans", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=13.5, leading=17, textColor=NAVY, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9, leading=12, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10, leading=13.5, textColor=INK, spaceBefore=6, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8, leading=10.5, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.2)
        canvas.setFillColor(GREY)
        canvas.drawString(2.0 * cm, 1.2 * cm, footer)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "%d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.8 * cm,
                          bottomMargin=1.9 * cm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, right_from=1):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a5abb3")),
             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6ecf2")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
             ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    t.setStyle(TableStyle(style))
    return t


def _stamp(d, hh="10", mm="00"):
    return ("D:%s%s%s00+01'00'" % (d.strftime("%Y%m%d"), hh, mm)).encode()


def write_schedule(path):
    d, frame = _doc(path, "Schedule 3 Service Levels", "Kroonvaart Fulfilment B.V.",
                    "Logistics Services Agreement Siersma Care B.V. / Kroonvaart Fulfilment B.V., Schedule 3, version 2.0")
    s = [Paragraph("Schedule 3: Service Levels", H1),
         Paragraph("Logistics Services Agreement between Siersma Care B.V. and Kroonvaart Fulfilment B.V. "
                   "for the Venlo site. Version 2.0, effective 1 January 2026, replacing version 1.3.", SUB),
         Paragraph("3.1 Scope", H2),
         Paragraph("This Schedule sets the service levels for the warehousing and fulfilment services Kroonvaart performs at "
                   "Venlo for Siersma's retail orders (orders for stores of Siersma's trade customers) and e-commerce orders "
                   "(orders from Siersma's webshop and marketplace shops). Terms not defined here have the meaning given in "
                   "the Agreement.", BODY),
         Paragraph("3.2 Pick accuracy", H2),
         Paragraph("Pick accuracy for a calendar month is the share of order lines picked in that month, by the Europe/Amsterdam "
                   "date of the pick, that pass pack-out verification. An order line is a line of an order as Siersma transmits "
                   "it, however many picks it takes; a line confirmed with a quantity of zero is not picked.", BODY),
         Paragraph("A line fails pack-out verification when the verification finds it short, over or carrying a wrong article. "
                   "Damage and labelling findings are reported under 3.5 and do not count against pick accuracy.", BODY),
         Paragraph("Target: 99.80 per cent in each calendar month, retail and e-commerce lines together.", BODY),
         Paragraph("3.3 Dispatch on time", H2),
         Paragraph("A retail order is dispatched on time when it leaves the site by 23:00 on the day it is picked. Target: 99.0 per "
                   "cent of retail orders in each calendar month. E-commerce orders released by 21:00 leave the site the same day.", BODY),
         Paragraph("3.4 Inventory record accuracy", H2),
         Paragraph("The share of pick faces counted in a calendar month whose counted quantity equals the system quantity. "
                   "Target: 99.5 per cent.", BODY),
         Paragraph("3.5 Store claims and findings", H2),
         Paragraph("Siersma's customer service registers the claims stores make on retail deliveries and passes those for "
                   "short, over or wrong articles to Kroonvaart, which investigates each within five "
                   "working days. Damage and labelling findings at pack-out are reported monthly with the claims.", BODY),
         Paragraph("3.6 Reporting and review", H2),
         Paragraph("Kroonvaart reports the service levels monthly in a service close-out. At each quarterly business review "
                   "Kroonvaart presents its forecast of pick accuracy for the coming months, built on the site's records kept "
                   "under this Schedule.", BODY),
         Paragraph("3.7 Service credits", H2),
         Paragraph("Where pick accuracy falls below target in a calendar month, Kroonvaart credits 1.5 per cent of that month's "
                   "handling fee for each 0.05 percentage point, or part of it, below target, up to 10 per cent of the month's "
                   "handling fee. Service credits are Siersma's sole financial remedy for a missed service level.", BODY),
         Spacer(1, 8),
         Paragraph("Signed for Siersma Care B.V. and for Kroonvaart Fulfilment B.V., Venlo, 18 December 2025.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
    PP.normalize_pdf(path, _stamp(dt.date(2025, 12, 18), "16", "12"), _stamp(dt.date(2025, 12, 18), "16", "12"))


def write_pcn(path):
    d, frame = _doc(path, "PCN-2026-11 Daily range", "Siersma Care B.V.", "Siersma Care B.V., Packaging Development, PCN-2026-11")
    rows = [["Item", "Range", "Change", "Effective"],
            ["1", "Daily (all articles)", "Inner pack from 6 to 4 units for the new shelf-ready tray. The shipping case stays at 24 "
             "units (now 6 inners of 4). Consumer unit EANs unchanged; each inner carries a new inner GTIN.", "Production week 50"],
            ["2", "Hair, 250 ml shampoo and conditioner", "Shipping case from 24 to 36 units for the larger pallet layer. Inner pack "
             "unchanged.", "Applied from 7 September 2026 receipts"],
            ["3", "Sun, all articles", "New artwork for the 2027 season. Pack sizes unchanged.", "First 2027 receipts"]]
    s = [Paragraph("Packaging Change Notification PCN-2026-11", H1),
         Paragraph("Siersma Care B.V., Packaging Development. Issued 17 November 2026 to Kroonvaart Fulfilment, Venlo site.", SUB),
         _table(rows, [1.1 * cm, 4.0 * cm, 8.4 * cm, 3.5 * cm]),
         Spacer(1, 10),
         Paragraph("Logistics", H2),
         Paragraph("The item master update with the new inner GTINs and configurations is sent to the Venlo site on 1 December "
                   "2026, dated from the first receipt. First deliveries of the Daily range in the new pack reach Venlo in week 2 of "
                   "2027 (11 January). Stock in the old pack is sold through by 31 January 2027; from 1 February 2027 Venlo holds "
                   "the Daily range in the new pack only.", BODY),
         Spacer(1, 6),
         Paragraph("Questions to packaging.development@siersmacare.nl.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
    PP.normalize_pdf(path, _stamp(dt.date(2026, 11, 17), "11", "40"), _stamp(dt.date(2026, 11, 17), "11", "40"))


def write_closeout(path, table, notes):
    d, frame = _doc(path, "Service close-out December 2026", "Romy Friehus",
                    "Kroonvaart Fulfilment B.V., Venlo, service close-out for Siersma Care, December 2026")
    hdr = ["Month 2026", "Order lines picked", "Pick accuracy", "Dispatch on time", "Inventory record accuracy", "Store claims received"]
    rows = [hdr] + table
    s = [Paragraph("Service close-out, December 2026", H1),
         Paragraph("Venlo site for Siersma Care. Prepared 4 January 2027 by site operations planning.", SUB),
         Paragraph("Service levels under Schedule 3, January to December 2026", H2),
         _table(rows, [2.4 * cm, 2.9 * cm, 2.4 * cm, 2.6 * cm, 3.4 * cm, 3.2 * cm]),
         Spacer(1, 8),
         Paragraph("December", H2)] + [Paragraph(n, BODY) for n in notes] + [
         Spacer(1, 4),
         Paragraph("Pick accuracy, dispatch and inventory figures as defined in Schedule 3, sections 3.2 to 3.4. Store claims "
                   "received: entries in Siersma's claims register in the month, all reasons.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
    PP.normalize_pdf(path, _stamp(dt.date(2027, 1, 4), "09", "26"), _stamp(dt.date(2027, 1, 4), "09", "26"))
