"""task305 documents: the property team's spend-share model sheet (pdf) and the GIS analyst's notes on the data
folder (md)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=17, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.4):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E9E4")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def model_sheet(path):
    body, h1, h2, small = _styles()
    s = []
    s.append(Paragraph("Marrable Foodstores: store sales model", h1))
    s.append(Paragraph("Spend-share parameters. Property and Network Planning, recalibrated June 2025 (supersedes the "
                       "parameters of March 2022). Owner: %s." % P.PEOPLE["property"], small))
    s.append(Spacer(1, 4))
    s.append(Paragraph("1. What the model does", h2))
    s.append(Paragraph("The model shares grocery spend among the grocery stores that can win it. Spend starts where people "
                       "are: a household's at its output area, and anyone else's at the place where they are staying. A "
                       "store's share of the spend that starts at a place is its pull times its deterrence from that "
                       "place, divided by the sum of pull times deterrence over every store in the share. A store's sales "
                       "are the sum of its shares of the spend.", body))
    s.append(Paragraph("2. The stores in the share", h2))
    s.append(Paragraph("Every grocery store on the VOA rating list for the planning region whose primary description is "
                       "SUPERMARKET AND PREMISES, SUPERSTORE AND PREMISES or FOOD STORE AND PREMISES and whose summary "
                       "valuation measures 280 m2 or more, our own stores included. A proposed store enters the share at "
                       "its proposed floor area from the site schedule.", body))
    s.append(Paragraph("3. Parameters", h2))
    s.append(_table([["Term", "Value", "Source"],
                     ["Pull", "floor area in m2, to the power 1.0", "summary valuation, main measure"],
                     ["Deterrence", "exp(-0.22 x road km)", "fitted, June 2025"],
                     ["Road km", "1.25 x straight-line km between grid references", "network sample, 2022"],
                     ["Grid reference", "an output area at its population-weighted centroid; a store, a site or any "
                                        "other address at its postcode's grid reference", "ONS centroids; ONSPD"],
                     ["Households", "an output area's households as Census 2021 counted them, not rolled forward",
                      "Census 2021, TS041"],
                     ["In-store share", "88 per cent of households' grocery spend; the rest is bought online and is "
                                        "not shared", "household spend survey, 2025"]],
                    [30, 82, 52]))
    s.append(Paragraph("4. Appraisal of a new store (Finance)", h2))
    s.append(Paragraph("A store's contribution is 26 per cent of its sales less its running costs. A new store adds to the "
                       "chain's contribution 26 per cent of its own sales, less 26 per cent of the sales it takes from "
                       "our existing stores, less its running costs as the site schedule estimates them: a year of "
                       "trading at 2026 prices.", body))
    s.append(Paragraph("5. Calibration", h2))
    s.append(Paragraph("Fitted in June 2025 to our stores' card spend by month and cardholder home sector for FY2024/25. "
                       "The deterrence held at 0.22 and the floor-area power at 1.0, both as in 2022; the road factor was "
                       "not refitted.", body))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Store sales model: spend-share parameters", author=P.ORG,
                            creator=P.ORG, subject="Property and Network Planning", invariant=1)
    doc.build(s, onFirstPage=_footer("Marrable Foodstores, Property and Network Planning. Internal."),
              onLaterPages=_footer("Marrable Foodstores, Property and Network Planning. Internal."))


VOA_FIELDS = ["Entry number", "Billing authority code", "Community code", "Billing authority reference",
              "Primary description code", "Primary description", "Unique address reference number (UARN)",
              "Full property identifier", "Firm's name", "Number or name", "Street", "Town", "Postal district",
              "County", "Postcode", "Effective date", "Composite indicator", "Rateable value",
              "Appeal settlement code", "Assessment reference", "List alteration date", "SCAT code and suffix",
              "Sub-street level 3", "Sub-street level 2", "Sub-street level 1", "Case number", "Current from date",
              "Current to date"]


def voa_spec(path):
    """the VOA's own layout for the compiled list entries file (publisher documentation)"""
    body, h1, h2, small = _styles()
    s = [Paragraph("Valuation Office Agency: compiled list entries, file specification", h1),
         Paragraph("Non-domestic rating, 2026 local rating list. Data download service.", small), Spacer(1, 4),
         Paragraph("Each list entry is one line of text. Fields are separated by an asterisk (*); there is no header "
                   "line, and an empty field is two consecutive asterisks. Dates are written DD-MON-YYYY. The rateable "
                   "value is in whole pounds.", body),
         Paragraph("Field order", h2),
         _table([["Position", "Field"]] + [[str(k + 1), f] for k, f in enumerate(VOA_FIELDS)], [24, 110])]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Compiled list entries: file specification",
                            author="Valuation Office Agency", creator="Valuation Office Agency", invariant=1)
    doc.build(s, onFirstPage=_footer("Valuation Office Agency. Open Government Licence v3.0."),
              onLaterPages=_footer("Valuation Office Agency. Open Government Licence v3.0."))


def dc_procedure(path):
    """the distribution centre's store deliveries procedure (governing document for the DC's records)"""
    body, h1, h2, small = _styles()
    s = [Paragraph("Loderwell Gate distribution centre: store deliveries", h1),
         Paragraph("Transport procedure TP-04, issue 3, September 2025. Owner: transport manager.", small), Spacer(1, 4),
         Paragraph("1. Planning", h2),
         Paragraph("Each night's trips are planned on the transport management system from the stores' orders. A trip's "
                   "load plan gives the cases and cages for each stop; the system keeps every time in UTC.", body),
         Paragraph("2. At the store", h2),
         Paragraph("The driver closes each stop on the handset when the trailer leaves the bay. A store may turn a load "
                   "away at the door, for damage, temperature or no room in the backroom; the driver still closes the "
                   "stop as delivered, and the planners send the same load again the next day on a trip of its own.",
                   body),
         Paragraph("3. Collections", h2),
         Paragraph("Empty cages and recyclables come back on the same trip and are closed as collections, with no "
                   "cases.", body)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Store deliveries: transport procedure TP-04", author=P.ORG,
                            creator=P.ORG, invariant=1)
    doc.build(s, onFirstPage=_footer("Marrable Foodstores, Loderwell Gate distribution centre. Internal."),
              onLaterPages=_footer("Marrable Foodstores, Loderwell Gate distribution centre. Internal."))
