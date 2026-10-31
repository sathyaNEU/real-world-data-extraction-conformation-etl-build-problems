"""task118 documents: the resource adequacy plan's accreditation chapter, System Operations' OP-7 and the Home
Battery Network agreement's schedule 2, each a short operational PDF in its issuer's voice."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18,
                        spaceAfter=3, textColor=colors.HexColor("#173B57"))
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#4A4A4A"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(19 * mm, 10 * mm, text)
        canvas.drawRightString(letter[0] - 19 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.8):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.4)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E9EF")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, author, flow, footer):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=17 * mm,
                            bottomMargin=19 * mm, title=title, author=author, creator=author, producer=author,
                            subject="", invariant=1)
    doc.build(flow, onFirstPage=_footer(footer), onLaterPages=_footer(footer))


PLAN_PIN = ("A demand-side programme is accredited at its expected load reduction in the system peak hour of the "
            "design year, with the programme operated as the procedures in force for 2027 operate it. The reduction "
            "is measured against the load the same enrolled units would have drawn had the programme not been "
            "called. An enrolled unit added for 2027 is credited at the programme's expected reduction per enrolled "
            "unit, under the contract terms in force for 2027.")
PLAN_DESIGN = ("Appendix B (appendix_b_design_year_2027.csv) is the design year: the hourly dry-bulb temperature at "
               "Cholla Basin International and the forecast system load from 1 June to 30 September 2027, built on "
               "the one-in-ten summer of the 1996 to 2025 record. The design year is planned as forecast, so each "
               "day's highest temperature is the day-ahead forecast high the procedures act on. Hours are hour "
               "beginning, Mountain Standard Time; the utility does not observe daylight saving time. The system "
               "peak hour is the hour of the highest forecast system load in Appendix B.")
OP7_DAYS = ("Each programme is called on every weekday whose day-ahead forecast high at Cholla Basin International "
            "(CBX) is 110F or above, except Independence Day and Labor Day as the City observes them. The forecast "
            "is the National Weather Service point forecast issued at 13:00 for the following day.")
HBN_SETTING = ("Each enrolled battery discharges at 3.0 kW through the event window. Until 31 December 2024 the "
               "dispatch setting was 2.0 kW.")
HBN_EARN = ("For each event in which any of a premise's enrolled batteries discharged at its dispatch setting for at "
            "least three hours in all during the event window, the premise earns USD 15.")
HBN_CAP = "A premise earns at most USD 255 in a season."
HBN_MONTH = "An incentive belongs to the calendar month of the event."


def plan(path):
    body, h1, h2, small = _styles()
    units = [["Resource", "Type", "Summer net capability (MW)", "Accredited for 2027 (MW)"],
             ["Basin Springs 1", "combined cycle", "318", "289"],
             ["Basin Springs 2", "combined cycle", "306", "277"],
             ["Sotol peakers 1 to 4", "combustion turbines", "4 x 47", "171"],
             ["Gila Canal solar", "single-axis solar", "80", "19"],
             ["Desert Southwest firm purchase", "contract import", "400", "400"]]
    s = [Paragraph("Resource Adequacy Plan 2027, Chapter 4: Capacity accreditation", h1),
         Paragraph("%s, Resource Planning. Draft for the 2027 budget, issued 12 October 2026. Prepared by Corey Cox, "
                   "Resource Planning Manager." % P.UTILITY, small),
         Spacer(1, 4),
         Paragraph("4.1 Purpose", h2),
         Paragraph("This chapter sets how each resource counts toward the 2027 summer, so that the plan the City "
                   "Council adopts with the 2027 budget compares like with like. Every resource is accredited in one "
                   "hour of one design year.", body),
         Paragraph("4.2 The design year", h2),
         Paragraph(PLAN_DESIGN, body),
         Paragraph("4.3 Demand-side programmes", h2),
         Paragraph(PLAN_PIN, body),
         Paragraph("4.4 Generating units and purchases", h2),
         Paragraph("A generating unit is accredited at its net capability at the dry-bulb temperature of the system "
                   "peak hour, less its summer forced-outage rate over the last five seasons; solar at its expected "
                   "output in that hour. A firm purchase counts at its contract quantity.", body),
         _table(units, [52, 40, 42, 40]),
         Spacer(1, 6),
         Paragraph("4.5 Review", h2),
         Paragraph("Resource Planning reviews this chapter each year before the budget round. Comments to the "
                   "Resource Planning Manager by 6 November 2026.", body)]
    _doc(path, "Resource Adequacy Plan 2027, Chapter 4", "CBMU Resource Planning", s,
         "%s  |  Resource Adequacy Plan 2027  |  Chapter 4  |  Draft 12 October 2026" % P.UTILITY)


def op7(path):
    body, h1, h2, small = _styles()
    progs = [["Programme", "Provider", "What is called"],
             ["Cool Credit", "Halvern Controls", "Enrolled smart thermostats: pre-cooling from 14:00, a 4F setback "
              "through the window"],
             ["Peak Time Rewards", "CBMU Customer Programs", "Enrolled residential customers: a day-ahead alert and a "
              "rebate on the energy they save in the window"],
             ["Business Demand Partners", "Arroyo Demand Services", "Enrolled commercial sites: cooling and "
              "ventilation curtailment through the window"],
             ["Home Battery Network", "Brightwell Storage", "Enrolled customer batteries: discharge at the "
              "contracted dispatch setting through the window"]]
    s = [Paragraph("Operating Procedure OP-7: Demand response dispatch", h1),
         Paragraph("%s, System Operations. Revision 3, effective 1 May 2024. Owner: Nina Franklin, System "
                   "Operations Manager." % P.UTILITY, small),
         Spacer(1, 4),
         Paragraph("1. Scope", h2),
         Paragraph("This procedure covers how System Operations calls the utility's four demand response "
                   "programmes.", body),
         _table(progs, [40, 42, 92]),
         Paragraph("2. Event window", h2),
         Paragraph("An event runs from 16:00 to 20:00 Mountain Standard Time for every programme.", body),
         Paragraph("3. Event days", h2),
         Paragraph(OP7_DAYS, body),
         Paragraph("4. Notices", h2),
         Paragraph("By 15:00 on the day before an event, the shift supervisor opens an event ticket for each "
                   "programme and sends the notice to Halvern Controls, to Peak Time Rewards customers by text and "
                   "email, to Arroyo Demand Services and to Brightwell Storage. A notice is not withdrawn once sent.",
                   body),
         Paragraph("5. Records", h2),
         Paragraph("System Operations keeps the event log of tickets. Each provider keeps its own records of the "
                   "event and delivers them under its agreement; Ridgeway Analytics receives them for measurement and "
                   "verification.", body),
         Paragraph("6. Readiness", h2),
         Paragraph("System Operations records each programme's readiness for every event. A Cool Credit premise is "
                   "ready when it is enrolled on the event day and a thermostat installed at it is registered with "
                   "Halvern Controls, not retired, and online at 16:00, which is when the last status Halvern "
                   "reported for the thermostat at or before 16:00 is ONLINE, or is IDLE reported under Halvern's "
                   "firmware 6.0. Firmware 6.0 reached every registered thermostat on 6 July 2026; under earlier "
                   "firmware a thermostat reported IDLE when its radio slept, and it could not take a command.",
                   body),
         Paragraph("The readiness of Business Demand Partners for a month is the kilowatts Arroyo Demand Services "
                   "nominated for that month on the utility's commercial meters.", body)]
    _doc(path, "OP-7 Demand response dispatch", "CBMU System Operations", s,
         "%s  |  OP-7 Demand response dispatch  |  Revision 3" % P.UTILITY)


def hbn(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Home Battery Network Participation Agreement, Schedule 2: Dispatch setting and incentives", h1),
         Paragraph("Between %s and Brightwell Storage LLC. Schedule 2 as amended by Amendment 1, signed 14 March 2025."
                   % P.UTILITY, small),
         Spacer(1, 4),
         Paragraph("2.1 Dispatch setting", h2),
         Paragraph(HBN_SETTING, body),
         Paragraph("2.2 Event incentive", h2),
         Paragraph(HBN_EARN, body),
         Paragraph("2.3 Season cap", h2),
         Paragraph(HBN_CAP + " A season runs from 1 June to 30 September.", body),
         Paragraph("2.4 Timing", h2),
         Paragraph(HBN_MONTH + " CBMU credits the incentives for a month on the customer's second bill after it.",
                   body),
         Paragraph("2.5 Records", h2),
         Paragraph("Brightwell settles each event from its dispatch records and delivers the records to CBMU each "
                   "week of the season.", body)]
    _doc(path, "HBN Participation Agreement Schedule 2", "Brightwell Storage LLC", s,
         "Home Battery Network Participation Agreement  |  Schedule 2  |  Amendment 1")
