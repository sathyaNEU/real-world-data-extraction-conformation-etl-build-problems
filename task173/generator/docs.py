"""The pack's documents: the watermaster's 2027 order, Halvern's forecast instructions and its rate schedule
excerpt, the county crop report excerpt (a background file), the data dictionary and the export manifest.

PDFs are written with reportlab's invariant mode so two builds give the same bytes."""
from __future__ import annotations

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

import common as C

BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="Times-Roman", fontSize=8.5, leading=10.5, spaceAfter=4)
HEAD = ParagraphStyle("head", fontName="Times-Bold", fontSize=12, leading=15, spaceAfter=8)
SUB = ParagraphStyle("sub", fontName="Times-Bold", fontSize=10.5, leading=13.6, spaceBefore=6, spaceAfter=4)


def _scrub(path, stamp):
    """Equal-length byte substitution: the writer's comment lines blanked and the document dates set to the
    document's own issue date, so the xref offsets stand."""
    b = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        b = b.replace(sig, b" " * len(sig))
    b = b.replace(b"D:20000101000000", ("D:" + stamp).encode())
    assert b.count(b"ReportLab") == 0 and b.count(b"reportlab") == 0
    open(path, "wb").write(b)


def _pdf(path, title, author, story, footer, stamp="20261016152000"):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.drawString(0.9 * inch, 0.55 * inch, footer)
        canvas.drawRightString(7.6 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.85 * inch, title=title, author=author,
                            creator=author, producer=author, subject=title, invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    _scrub(path, stamp)


def order(path):
    s = []
    s.append(Paragraph("VARNER RIVER WATERMASTER", HEAD))
    s.append(Paragraph("Superior Court Case No. 4417, <i>In re the Determination of the Rights of the Various Claimants "
                       "to the Waters of the Varner River and its Tributaries</i> (Decree of 19 March 1934)", BODY))
    s.append(Paragraph("ORDER NO. 2026-14: SURFACE WATER SUPPLY FOR THE 2027 IRRIGATION SEASON", SUB))
    s.append(Paragraph("Issued 28 September 2026", BODY))
    s.append(Paragraph("1. Authority. This order is issued under Paragraph 22 of the Decree and the Court's Interim Order "
                       "of 2 July 2026 adopting the interim instream flow schedule for the reach below Hatch Road. The "
                       "interim schedule fixes the 2027 season's supply without regard to the season's runoff forecast, "
                       "so this order is not revised in February as in other years.", BODY))
    s.append(Paragraph("2. Season. The 2027 irrigation season runs from 1 April 2027 to 30 September 2027. No diversion "
                       "under the Decree is made outside the season.", BODY))
    s.append(Paragraph("3. Post-1914 appropriative rights. Diversion under every post-1914 appropriative right in the "
                       "schedule of allotments, including Right D-0007 of the Lone Bench Irrigation District at POD LBD-1, "
                       "is suspended for the whole of the 2027 season.", BODY))
    s.append(Paragraph("4. Riparian and pre-1914 appropriative rights. Diversion under each riparian and each pre-1914 "
                       "appropriative right in the schedule of allotments is limited, for the 2027 season, to 25 per cent "
                       "of the season allotment shown for that right in the schedule, measured at the right's point of "
                       "diversion and counted cumulatively from 1 April. A holder who reaches the limit stops diverting "
                       "for the rest of the season.", BODY))
    s.append(Paragraph("5. Measurement and statements. Holders continue to report monthly diversions at each point of "
                       "diversion by the tenth day of the following month. Where a point of diversion is pumped and "
                       "metered by electric service, the statement names the service.", BODY))
    s.append(Paragraph("6. Scope. This order governs diversion of surface water under the Decree. Extraction of "
                       "groundwater within the Varner Subbasin is administered by the Varner Subbasin Groundwater "
                       "Agency under its own rules and is not addressed here.", BODY))
    s.append(Paragraph("7. Enforcement. The deputy watermasters will read every metered point of diversion at the start "
                       "of the season and monthly thereafter. Diversion beyond the limit in Paragraph 4 is a violation of "
                       "the Decree and will be reported to the Court.", BODY))
    s.append(Spacer(1, 18))
    s.append(Paragraph("Kimberly Ball<br/>Varner River Watermaster", BODY))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Distribution: holders of record on the schedule of allotments; Lone Bench Irrigation District; "
                       "Varner Subbasin Groundwater Agency; Varner Valley Public Utility District (pumped points of "
                       "diversion).", SMALL))
    _pdf(path, "Order No. 2026-14", "Varner River Watermaster", s, "Varner River Watermaster  |  Order No. 2026-14",
         stamp="20260928141500")


def instructions(path):
    s = []
    s.append(Paragraph("HALVERN POWER AUTHORITY", HEAD))
    s.append(Paragraph("Member Load Forecast, 2027 Planning Year: Instructions to Members", SUB))
    s.append(Paragraph("Load Forecasting and Member Services  |  Revision of 4 August 2026", BODY))
    s.append(Paragraph("1. Purpose. Halvern schedules its 2027 purchases and sets each member's 2027 energy blocks "
                       "from the members' forecasts. Each member files one workbook for its whole system by 1 December "
                       "2026. Members with an irrigation class file the class separately under section 3.", BODY))
    s.append(Paragraph("2. Classes. Residential, commercial and large power classes are forecast for the calendar year "
                       "2027 as in previous years (Form MLF-1).", BODY))
    s.append(Paragraph("3. Irrigation class (Form MLF-3).", SUB))
    s.append(Paragraph("3.1 The irrigation class is every service on the member's irrigation pumping rate schedule that "
                       "is in service on 30 September 2026. Services connected later are not forecast in this filing.", BODY))
    s.append(Paragraph("3.2 The forecast is the class's energy at the retail meter, in MWh, from 1 April 2027 to 30 "
                       "September 2027, under the surface water supply ordered for that season.", BODY))
    s.append(Paragraph("3.3 Weather is a normal season: the mean of the April to September reference "
                       "evapotranspiration totals of the 20 seasons 2007 to 2026 at the weather station the member names "
                       "on the form.", BODY))
    s.append(Paragraph("3.4 The forecast holds each service to its 2026 acreage and cropping. Land that the season's "
                       "water supply cannot reach is not irrigated.", BODY))
    s.append(Paragraph("3.5 The member's method is its own. Halvern will compare the forecast with the metered "
                       "deliveries after the season.", BODY))
    s.append(Paragraph("4. Base-year tables (Form MLF-4). Each member reports for 2026:", SUB))
    s.append(Paragraph("(a) the energy Halvern metered at each of the member's delivery points in each billing month "
                       "from April to September (billing months as in Rate Schedule W-2);", BODY))
    s.append(Paragraph("(b) the member's demand at each delivery point in the hour of each of Halvern's monthly system "
                       "peaks from April to September, as posted by Halvern and as Rate Schedule W-2 defines it;", BODY))
    s.append(Paragraph("(c) for each delivery point, the irrigation services it supplied through the 2026 season and the "
                       "energy billed to them from April to September.", BODY))
    s.append(Paragraph("5. Data. Halvern's delivery-point interval data and its monthly system peak postings are "
                       "available to each member through the member portal.", BODY))
    s.append(Spacer(1, 14))
    s.append(Paragraph("Questions: Tammy Gibson, Load Forecasting.", BODY))
    _pdf(path, "Member Load Forecast 2027: Instructions", "Halvern Power Authority", s,
         "Halvern Power Authority  |  MLF instructions, 2027 planning year", stamp="20260804093000")


def rate_excerpt(path):
    s = []
    s.append(Paragraph("HALVERN POWER AUTHORITY", HEAD))
    s.append(Paragraph("Rate Schedule W-2: Wholesale Power Service to Members (excerpt: sections 1, 2 and 6)", SUB))
    s.append(Paragraph("Effective 1 January 2025", BODY))
    s.append(Paragraph("1. Availability. To each member taking all-requirements service at one or more delivery points.", BODY))
    s.append(Paragraph("2. Definitions.", SUB))
    s.append(Paragraph("2.1 Times. All times in this schedule are Pacific prevailing time.", BODY))
    s.append(Paragraph("2.2 Billing month. A calendar month, beginning at 00:00 on its first day.", BODY))
    s.append(Paragraph("2.3 Delivery point energy. The energy registered in the billing month by Halvern's revenue "
                       "meter at the delivery point.", BODY))
    s.append(Paragraph("2.4 Monthly system peak. The clock hour of the billing month in which Halvern's total system "
                       "load was highest, posted by Halvern by the fifth working day of the following month as the hour "
                       "ending.", BODY))
    s.append(Paragraph("2.5 Coincident demand. A member's demand at a delivery point in the monthly system peak: the "
                       "energy registered by the revenue meter at that delivery point in that clock hour, in kWh, read as "
                       "kW.", BODY))
    s.append(Paragraph("6. Metering. Halvern owns, reads and maintains the revenue meter at each delivery point and any "
                       "other meter it installs there. Interval data are retained for five years.", BODY))
    t = Table([["Charge", "Rate"], ["Coincident demand charge", "USD 13.85 per kW-month"],
               ["Energy charge, June to September", "USD 0.0518 per kWh"],
               ["Energy charge, October to May", "USD 0.0447 per kWh"]], colWidths=[3.2 * inch, 2.2 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 9.5), ("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("3. Monthly charges (section 3 in full is not reproduced; the charges are):", BODY))
    s.append(t)
    _pdf(path, "Rate Schedule W-2 (excerpt)", "Halvern Power Authority", s,
         "Halvern Power Authority  |  Rate Schedule W-2  |  excerpt", stamp="20241203110000")


def crop_report(path, rows):
    s = []
    s.append(Paragraph("KESTREL COUNTY AGRICULTURAL COMMISSIONER", HEAD))
    s.append(Paragraph("2025 Crop and Livestock Report (excerpt: field, fruit and nut crops)", SUB))
    s.append(Paragraph("Harvested acreage and gross value, all of Kestrel County. Values are at the first point of "
                       "sale and do not reflect production costs.", BODY))
    data = [["Crop", "Harvested acres", "Yield per acre", "Gross value (USD)"]] + rows
    t = Table(data, colWidths=[2.0 * inch, 1.3 * inch, 1.3 * inch, 1.6 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 9.5), ("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black)]))
    s.append(t)
    s.append(Spacer(1, 8))
    s.append(Paragraph("Yields: almonds, walnuts, pistachios and prunes in dry tons; tomatoes in tons; alfalfa in tons of "
                       "hay; pasture is not harvested and carries no yield.", SMALL))
    _pdf(path, "2025 Crop Report (excerpt)", "Kestrel County Agricultural Commissioner", s,
         "Kestrel County 2025 Crop and Livestock Report  |  excerpt", stamp="20260630100000")
