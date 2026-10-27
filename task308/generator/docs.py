"""task308 documents: the resource adequacy standard (pdf), the request for offers summary (pdf), the wholesale
billing procedures (pdf), and the cause code reference (csv). Every sentence here is a filed one: a literal reader
executes it."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P

ORG = "Prairie Hollow Power Cooperative"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Times-Roman", fontSize=10.2, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.5, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.5,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontName="Helvetica", fontSize=7.8, leading=10.2,
                           textColor=colors.HexColor("#3A3A3A"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(19 * mm, 11 * mm, text)
        canvas.drawRightString(letter[0] - 19 * mm, 11 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.4):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.3)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8C8C8C")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8E2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _pdf(path, title, subject, author, story, foot):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=17 * mm,
                            bottomMargin=19 * mm, title=title, author=author, creator="Microsoft Word",
                            subject=subject, invariant=1)
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))


def standard(path):
    body, h1, h2, small = _styles()
    s = [Paragraph(ORG, small), Paragraph("Resource Adequacy Planning Standard RA-3", h1),
         Paragraph("Revision 4. Approved by the Board of Directors on 24 February 2026; effective 1 March 2026. "
                   "Owner: Resource Planning.", small), Spacer(1, 6)]
    secs = [
        ("1. Purpose",
         ["This standard sets how the cooperative measures the adequacy of the resources it holds for a planning "
          "year, and how it values a resource offered for that year. Adequacy is measured by expected unserved "
          "energy (EUE)."]),
        ("2. Weather years",
         ["The planning year is tested against the ten recorded calendar years 2016 to 2025 at the Hollow Junction "
          "hub (the weather years). Each weather year counts equally."]),
        ("3. Load, wind and solar",
         ["Load is the planning load table prepared by Load Forecasting: the planning year's load in each hour of "
          "each weather year, by hour ending in local prevailing time. The output of the wind and solar resources "
          "under contract for the planning year is taken from the same table for the same hour."]),
        ("4. Generating units",
         ["Each generating unit in the planning-year fleet (the fleet list) is replayed in each weather year with "
          "the forced outages and forced derates it had in that year, as recorded in the outage event log, whatever "
          "their cause. Where an event was reported more than once, its latest revision is the record. Planned and "
          "maintenance outages are not replayed: the planning-year maintenance schedule keeps them out of the "
          "winter and summer peak months.",
          "A unit counts at its net winter capability, less the capability an event takes away while the event "
          "lasts; a derate leaves the unit its net available capability. An event that covers part of an hour "
          "counts for the part of the hour it covers, and where a unit's events overlap, the one leaving it the "
          "least capability governs."]),
        ("5. Imports",
         ["Firm imports count at their contract quantity in every hour the Red Willow tie is in service. A tie "
          "outage, forced or planned, removes the imports for the time it covers."]),
        ("6. Unserved energy",
         ["The unserved energy in an hour is the load less wind, solar, the available capability of the generating "
          "units and the imports, where that is positive. A weather year's unserved energy is the sum over its "
          "hours. EUE is the average of the ten weather years' unserved energy, in MWh a year."]),
        ("7. Resources offered for the planning year",
         ["A resource offered for the planning year has no record of its own in the weather years. It is counted in "
          "each replayed hour at its expected available capacity in that hour, judged from the evidence the record "
          "holds; a wind or solar resource counts at its modelled output for that hour.",
          "The EUE reduction an offer makes is the planning year's EUE without it less the EUE with it, each offer "
          "taken alone against the planning-year fleet."]),
        ("8. Value of lost load",
         ["Unserved energy is valued at USD 20,000 per MWh in planning-year evaluations."]),
    ]
    for head, paras in secs:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Paragraph("Revision history", h2))
    s.append(_table([["Revision", "Date", "Change"],
                     ["2", "March 2019", "Expected unserved energy replaces the reserve margin target."],
                     ["3", "June 2023", "Value of lost load raised from USD 12,000 to USD 20,000 per MWh."],
                     ["4", "February 2026", "Weather years moved to 2016 to 2025."]], [22, 30, 118]))
    _pdf(path, "RA-3 Resource Adequacy Planning Standard, Rev. 4", "Resource adequacy", "J. Graham", s,
         "RA-3 Rev. 4  |  Prairie Hollow Power Cooperative  |  Internal")


def _price(o):
    unit, v = P.PRICE[o]
    return "USD %s %s" % (("%.2f" % v) if v < 100 else ("%d" % v), unit[4:])


def offers(path):
    body, h1, h2, small = _styles()
    s = [Paragraph(ORG + "  |  Resource Planning", small),
         Paragraph("2027 Capacity Request for Offers: offers received", h1),
         Paragraph("Prepared for the Resource Planning Committee, 30 October 2026. Offers are firm until the "
                   "committee's award meeting on 19 November 2026; the award is one contract for delivery from "
                   "1 January 2027.", small), Spacer(1, 6),
         Paragraph("Offers received", h2)]
    rows = [["Offer", "Counterparty", "Resource", "Capacity", "Capacity price, 2027"],
            ["Ketchum Ridge", "Halvard Energy Partners LLC",
             "Two 150 MW simple-cycle combustion turbines, natural gas delivered on Northgate Interstate Gas "
             "Transmission under interruptible transportation (IT) service. Manufacturer's EFORd 4.5%.",
             "300 MW", _price("Ketchum Ridge")],
            ["Red Willow import", "Red Willow Hydro Authority",
             "Firm system sale delivered at Hollow Junction 345 kV over the existing Red Willow tie; curtailable "
             "only while the tie is out of service.", "300 MW", _price("Red Willow import")],
            ["Sandhill Draw", "Sandhill Draw Wind LLC",
             "150 turbines of 3.0 MW. Hourly modelled output per MW of capacity for 2016 to 2025 from the "
             "developer's resource assessment (offer profiles file, hours beginning in UTC).", "450 MW",
             _price("Sandhill Draw")],
            ["Coulee Flats", "Coulee Flats Solar LLC",
             "Single-axis tracking PV, 500 MW AC. Hourly modelled output per MW for 2016 to 2025 (offer profiles "
             "file, hours beginning in UTC).", "500 MW", _price("Coulee Flats")]]
    s.append(_table(rows, [24, 30, 70, 17, 27], size=8.0))
    s.append(Paragraph("Evaluation basis", h2))
    s.append(Paragraph("The committee ranks the offers by the value of the EUE reduction each makes in planning year "
                       "2027 under RA-3, at the standard's value of lost load, less the offer's 2027 capacity "
                       "payment. Energy is settled at market under every offer and is not part of the comparison. The "
                       "award goes to the offer with the highest value, provided it is positive.", body))
    s.append(Paragraph("Planning year 2027", h2))
    s.append(Paragraph("The 2027 fleet is the fleet list; Sandoval Unit 1 retires on 31 December 2026. The 2027 "
                       "load, contracted wind and contracted solar are in the planning load table, and the 200 MW "
                       "firm import already contracted from Red Willow continues through 2027.", body))
    _pdf(path, "2027 Capacity RFO - offers received", "Capacity procurement", "J. Graham", s,
         "2027 Capacity RFO  |  Resource Planning Committee  |  Confidential")


def billing(path):
    body, h1, h2, small = _styles()
    s = [Paragraph(ORG + "  |  Member Services and Settlements", small),
         Paragraph("Wholesale Billing Procedures: metering, energy and coincident peak", h1),
         Paragraph("Procedure MS-12, revision 7, January 2025.", small), Spacer(1, 6)]
    secs = [
        ("1. Delivery points",
         ["Each member is billed for the energy delivered at its delivery points. The delivery point register lists "
          "each point and its member; a point that moves between members carries an assignment history, and an "
          "interval belongs to the member the point was assigned to at the start of the interval."]),
        ("2. The meter data export",
         ["The meter data management system (MDM) exports one row per delivery point per hour. Each row carries "
          "the interval's start in local prevailing time with its UTC offset, the version and quality of the "
          "reading, the multiplier the MDM applied, and the delivered and received energy in kWh after the "
          "multiplier.",
          "Readings that fail validation are estimated and carry quality E. When a reading is loaded again for the "
          "same interval, the export keeps both rows and the highest version is the reading of record."]),
        ("3. Net energy",
         ["Where a delivery point has member-owned generation behind it, the meter records energy delivered to the "
          "member and energy received from it on separate channels. A member's net energy in an interval is "
          "delivered less received."]),
        ("4. Coincident peak",
         ["The cooperative's coincident peak for a calendar month is the hour, beginning in local prevailing time, "
          "in which the net energy of all delivery points together was highest. A member's contribution to it is "
          "its net energy in that hour, in kWh, which is its average demand in kW over the hour. The 12-CP "
          "average is the average of a member's twelve monthly contributions. Demand-related costs are allocated "
          "to members on the 12-CP average of the prior calendar year."]),
    ]
    for head, paras in secs:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    _pdf(path, "MS-12 Wholesale Billing Procedures", "Member settlements", "L. Ramos", s,
         "MS-12 Rev. 7  |  Prairie Hollow Power Cooperative")


CAUSE_TEXT = {
    1000: "Boiler: waterwall (furnace wall) tube leaks", 1005: "Boiler: first reheater tube leaks",
    1060: "Boiler: economizer tube leaks", 1455: "Boiler: fuel feeders and pulverizer problems",
    1795: "Boiler: other boiler problems", 1999: "Boiler: planned overhaul",
    3110: "Reactor: control rod drive problems", 3410: "Feedwater pump problems",
    3620: "Main transformer problems", 4260: "Turbine: control valves", 4290: "Turbine: other turbine problems",
    4400: "Engine: fuel injection problems", 4410: "Engine: cooling system", 4420: "Engine: lube oil system",
    4800: "Generator: stator windings", 4990: "Turbine: planned overhaul", 5000: "Gas turbine: compressor problems",
    5040: "Gas turbine: combustor problems", 5099: "Gas turbine: planned inspection",
    5110: "Gas turbine: fuel nozzles", 5250: "Gas turbine: controls and instrumentation",
    5300: "Gas turbine: starting system", 6500: "Heat recovery steam generator: tube leaks",
    7040: "Hydro: turbine runner", 7110: "Hydro: wicket gates", 7300: "Hydro: penstock and intake",
    7400: "Hydro: generator", 7999: "Hydro: planned maintenance",
    9130: "Lack of fuel (interruptible supply of fuel part of fuel contract)",
    9131: "Lack of fuel (not under operator control)", 9300: "Transmission system problems (external)",
}
