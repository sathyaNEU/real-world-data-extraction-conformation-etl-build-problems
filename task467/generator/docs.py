"""The pack's documents: the Office's data dictionary, the Authority's fees by-law and finance policy, its temporary
rank notice, Velmont Transit's Airport Line bulletin, the 2027 program budget workbook, the airport's passenger
statistics and its 2023 ground access survey (the last two distractors), and the folder's contents list."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import numpy as np    # noqa: E402

import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
NAVY = colors.HexColor("#17365d")
TEAL = colors.HexColor("#0f5c63")
GREEN = colors.HexColor("#2f5d34")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SCELL = ParagraphStyle("scell", fontName="LiberationSerif", fontSize=9, leading=11.2, textColor=INK)
SCELLB = ParagraphStyle("scellb", parent=SCELL, fontName="LiberationSerif-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.3, leading=10.8, textColor=GREY)


def styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.3, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3)
    return h1, h1s, h2


def _doc(path, title, author, footer, layout="left"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        if layout == "left":
            canvas.setFont("LiberationSans", 7.5)
            canvas.drawString(0.9 * inch, 0.6 * inch, footer)
            canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        elif layout == "centre":
            canvas.setFont("LiberationSerif", 8.5)
            canvas.drawCentredString(letter[0] / 2, 0.6 * inch, "%s  -  %d" % (footer, doc.page))
        else:
            canvas.setFont("LiberationSans", 8)
            canvas.drawString(0.9 * inch, letter[1] - 0.55 * inch, footer)
            canvas.setStrokeColor(GREY)
            canvas.setLineWidth(0.5)
            canvas.line(0.9 * inch, letter[1] - 0.6 * inch, letter[0] - 0.9 * inch, letter[1] - 0.6 * inch)
            canvas.drawCentredString(letter[0] / 2, 0.55 * inch, str(doc.page))
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e6eef0", serif=False):
    c, cb = (SCELL, SCELLB) if serif else (CELL, CELLB)
    data = [[Paragraph(str(v), cb if i == 0 else c) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def long_date(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def ca_date(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return str(d.day) + d.strftime(" %B %Y")


# ---------------------------------------------------------------- the Office's data dictionary
V3_FIELDS = [
    ("record_id", "integer", "The Office's record number, given to each record when it is received."),
    ("vendor_id", "integer", "Taximeter vendor: 1 Orlan Metering, 2 Corvane Systems."),
    ("vehicle_id", "text", "Taxi licence (plate) number."),
    ("brokerage_id", "integer", "The vehicle's licensed brokerage (see the brokerage register)."),
    ("meter_on", "timestamp", "Date and time the taximeter was engaged."),
    ("meter_off", "timestamp", "Date and time the taximeter was disengaged."),
    ("pu_zone", "integer", "Taxi zone where the meter was engaged (zone map 2019, see the zone list)."),
    ("do_zone", "integer", "Taxi zone where the meter was disengaged."),
    ("passengers", "integer", "Number of passengers, entered by the driver."),
    ("distance_km", "decimal", "Metered distance in kilometres."),
    ("fare", "decimal", "Metered fare (flag, distance and waiting time), dollars."),
    ("airport_fee", "decimal", "Airport pickup fee charged on the meter, dollars."),
    ("tip", "decimal", "Tip paid by card, dollars. Cash tips are not recorded."),
    ("total", "decimal", "Total charged: fare, airport pickup fee and tip, dollars."),
    ("payment_type", "integer", "1 card, 2 cash, 3 account."),
    ("sf_flag", "text", "Y when the meter held the record in memory and sent it later; N otherwise."),
]
V2_NAMES = ["record_id", "vendor_id", "vehicle_id", "brokerage_id", "pickup_datetime", "dropoff_datetime",
            "pickup_zone", "dropoff_zone", "passenger_count", "trip_distance_km", "fare_amount", "airport_fee",
            "tip_amount", "total_amount", "payment_type", "store_and_fwd_flag"]


def write_dictionary(path):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Taxi trip records: data dictionary", W.OFFICE, W.OFFICE + "  |  Taxi trip records, version 3.1")
    s = [Paragraph("Taxi trip records: data dictionary", h1),
         Paragraph("Version 3.1, February 2026. %s" % W.OFFICE, h1s),
         Paragraph("About the records", h2),
         Paragraph("Every licensed taxi's taximeter sends a record of each trip to the Office. The Office publishes the "
                   "records monthly as Parquet, about five weeks after a month ends; each monthly file holds the "
                   "records the Office received that month. After a year closes the Office builds an annual file of "
                   "the year's trips, which replaces the year's monthly files. Records of a closed year that arrive "
                   "after its last monthly file are added to its annual file, not to the next year's monthly files.",
                   BODY),
         Paragraph("The Velmont Airport Authority receives an extract of the trips with a pickup or a drop-off in "
                   "zone 1 (Velmont International Airport) under data sharing agreement DSA-2019-04. Records "
                   "before 2024 are kept as a daily origin-destination archive (trips by date, pickup zone and "
                   "drop-off zone; voided trips not counted).", BODY),
         Paragraph("When a driver voids a trip, the meter sends the trip and later a reversal record carrying "
                   "the same vehicle, times and zones with every amount negated.", BODY),
         Paragraph("Fields (version 3)", h2),
         _table([["Field", "Type", "Description"]] + [list(r) for r in V3_FIELDS], [1.25 * inch, 0.8 * inch, 4.6 * inch]),
         Spacer(1, 8),
         Paragraph("Version 2 field names (annual files to 2024)", h2),
         _table([["Version 2", "Version 3"]] + [[a, b] for a, b in zip(V2_NAMES, [f[0] for f in V3_FIELDS])],
                [2.2 * inch, 2.2 * inch]),
         Paragraph("Changes", h2),
         _table([["Version", "Date", "Change"],
                 ["3.1", "February 2026", "Annual file 2025, in version 3 field names and local time. Voided trips "
                  "and their reversals are no longer included in annual files."],
                 ["3.0", "January 2026", "Taximeter firmware 8.1: fields renamed (above); meter_on and meter_off are "
                  "recorded in Coordinated Universal Time and written with the time zone. Earlier files carry local "
                  "time (Eastern)."],
                 ["2.4", "January 2025", "Rate order 2025-01: flag $4.25, $2.02 a kilometre, waiting time $0.64 a "
                  "minute."],
                 ["2.3", "March 2023", "Airport extract under DSA-2019-04 moved from monthly CSV to Parquet."]],
                [0.7 * inch, 1.1 * inch, 4.85 * inch]),
         Spacer(1, 10),
         Paragraph("Questions to %s, Open Data Coordinator, Vehicle-for-Hire Office." % W.PEOPLE["opendata"], SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
    return len(V3_FIELDS)


# ---------------------------------------------------------------- the Authority's by-law and policy
def write_bylaw(path):
    h1, h1s, h2 = styles(NAVY, serif=True)
    d, frame = _doc(path, W.BYLAW, W.AUTHORITY, W.AUTHORITY + "  |  " + W.BYLAW + ", consolidated 1 January 2026",
                    layout="centre")
    fees = [["Year", "Fee per fee-liable pickup"]] + [[str(y), "$%.2f" % f] for y, f in sorted(W.FEES.items())] + [
        ["2027", "To be set by the Board under section 4"]]
    s = [Paragraph(W.BYLAW.replace(" GT-3", ""), h1),
         Paragraph("By-law GT-3 of the Velmont Airport Authority. Consolidated to 1 January 2026.", h1s),
         Paragraph("1. Short title", h2),
         Paragraph("This By-law may be cited as the Ground Transportation Fees By-law.", BODY),
         Paragraph("2. Definitions", h2),
         Paragraph("In this By-law, <i>airport</i> means the lands of Velmont International Airport, which the City of "
                   "Velmont's taxi zone map shows as zone 1; <i>brokerage</i> means a taxi brokerage licensed by the "
                   "City; <i>fee-liable pickup</i> means a trip a licensed taxi begins at the airport; a trip the "
                   "taximeter records as voided is not a trip for this By-law; <i>Ground Transportation Program</i> "
                   "means the Authority's taxi rank, taxi holding lot, marshalling and dispatch; <i>year</i> means a "
                   "calendar year. Days, months and years are reckoned in Velmont local time.", BODY),
         Paragraph("3. Fee", h2),
         Paragraph("(1) A taxi pickup fee is payable for each fee-liable pickup at the fee Schedule A sets for the year "
                   "in which the trip begins.", BODY),
         Paragraph("(2) The Authority bills each month's fee-liable pickups to the brokerage with which the taxi is "
                   "affiliated when the trip begins, counting each trip once.", BODY),
         Paragraph("(3) A brokerage shall have its taxis' meters charge the fee in force within 21 days of the fee "
                   "changing. The fee billed is the fee in force, whatever a meter charged.", BODY),
         Paragraph("4. Setting the fee", h2),
         Paragraph("(1) Before 1 December each year the Board sets the next year's fee as the lowest multiple of $0.25 "
                   "at which the year's budgeted fee-liable pickups, multiplied by the fee, are not less than the "
                   "amount the year's Ground Transportation Program budget assigns to the taxi pickup fee.", BODY),
         Paragraph("(2) Budgeted fee-liable pickups are determined under Finance Policy FP-07.", BODY),
         Paragraph("5. Review", h2),
         Paragraph("The Board reviews this By-law at least every five years.", BODY),
         Paragraph("Schedule A: Taxi pickup fee", h2),
         _table(fees, [1.2 * inch, 3.2 * inch], serif=True),
         Spacer(1, 10),
         Paragraph("Enacted 12 March 2019. Amended 9 December 2019, 7 December 2020, 6 December 2021, 5 December 2022, "
                   "4 December 2023, 2 December 2024 and 1 December 2025 (Schedule A).", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_policy(path):
    h1, h1s, h2 = styles(GREEN)
    d, frame = _doc(path, W.POLICY, W.AUTHORITY, W.AUTHORITY + "  |  " + W.POLICY + ": Budgeting user-fee revenue")
    s = [Paragraph("Finance Policy FP-07: Budgeting user-fee revenue", h1),
         Paragraph("Approved by the Finance and Audit Committee, 18 May 2021; revised 14 June 2023.", h1s),
         Paragraph("1. Purpose and application", h2),
         Paragraph("1.1 This policy sets how the Authority budgets the revenue of its fee-funded programs.", BODY),
         Paragraph("1.2 It applies to the taxi pickup fee, limousine and sedan permit fees and shuttle permit fees. "
                   "Parking revenue is budgeted under FP-04.", BODY),
         Paragraph("1.3 The Authority's fiscal year is the calendar year.", BODY),
         Paragraph("2. Program budgets", h2),
         Paragraph("2.1 Each fee-funded program's budget states its costs, its other revenues and the amount it "
                   "assigns to its fee.", BODY),
         Paragraph("2.2 Costs are budgeted at the contract prices and wage rates in force for the budget year.", BODY),
         Paragraph("3. Permit fees", h2),
         Paragraph("3.1 Limousine, sedan and shuttle permit revenue is budgeted on the permits issued for the current "
                   "year at the budget year's permit fees.", BODY),
         Paragraph("4. Taxi pickup fee", h2),
         Paragraph("4.1 The taxi pickup fee is set under section 4 of the Ground Transportation Fees By-law on the "
                   "budgeted fee-liable pickups this section defines.", BODY),
         Paragraph("4.2 Budgeted fee-liable pickups for a year are the fee-liable pickups of the most recent complete "
                   "fiscal year (the base year), restated for any change in taxi loading arrangements between the "
                   "base year and the budget year. A taxi loading arrangement is the location and operation of the "
                   "taxi rank and the taxi holding lot. No traffic growth is assumed.", BODY),
         Paragraph("4.3 Where an arrangement that applied in the base year will not apply in the budget year, the "
                   "base year's pickups are restated to those the base year would have had under the budget year's "
                   "arrangement.", BODY),
         Paragraph("4.4 Base-year pickups are read from the Vehicle-for-Hire Office's final annual file for the base "
                   "year.", BODY),
         Paragraph("5. Reporting", h2),
         Paragraph("5.1 The budget package states each fee's budgeted volume and the fee proposed.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_notice(path):
    h1, h1s, h2 = styles(NAVY)
    d, frame = _doc(path, W.NOTICE, W.AUTHORITY, W.AUTHORITY + "  |  Ground Transportation", layout="header")
    s = [Paragraph("Ground Transportation Notice GT-2024-11", h1),
         Paragraph("Temporary taxi rank during the arrivals forecourt reconstruction. Issued 7 October 2024; "
                   "revision 2, 14 August 2026.", h1s),
         Paragraph("To: taxi brokerages, licensed drivers, terminal operations, customer service", SANS),
         Paragraph("What changes", h2),
         Paragraph("From 05:00 on Monday 4 November 2024 the terminal's arrivals forecourt closes for reconstruction. "
                   "Taxis load passengers at the temporary rank on the Level 2 road of Parkade P2, reached from the "
                   "arrivals hall by the covered walkway at door 6 or by the courtesy shuttle from door 2, every six "
                   "minutes from 06:00 to 01:00. The taxi holding lot (P7), the dispatch procedure and the order of "
                   "loading do not change. Departures drop-off on the upper roadway is not affected.", SANS),
         Paragraph("Signage and staff", h2),
         Paragraph("Marshals at doors 2 and 6 direct passengers to the rank. Customer service will hand out the rank "
                   "map at the arrivals information desk.", SANS),
         Paragraph("Revision 2, 14 August 2026", h2),
         Paragraph("The forecourt works remain on schedule. The taxi rank returns to its former position on the arrivals "
                   "forecourt on Friday 1 January 2027, and the temporary rank on P2 closes at 05:00 that day. The "
                   "courtesy shuttle ends with it.", SANS),
         Spacer(1, 12),
         Paragraph("%s<br/>%s" % (W.PEOPLE["director"], W.TITLES["director"]), SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_bulletin(path):
    h1, h1s, h2 = styles(colors.HexColor("#6b2d5c"))
    d, frame = _doc(path, "Service Bulletin 2024-19", W.TRANSIT, W.TRANSIT + "  |  Service Bulletin 2024-19")
    s = [Paragraph("Service Bulletin 2024-19: the Airport Line opens Monday, November 4", h1),
         Paragraph("%s. Issued October 21, 2024." % W.TRANSIT, h1s),
         Paragraph("The Airport Line begins service with the first train from Central at 4:40 a.m. on Monday, "
                   "November 4, 2024. Trains run between Central and Airport stations, calling at Midtown, University "
                   "and Commerce Park.", SANS),
         Paragraph("Service", h2),
         _table([["", "Weekdays", "Saturdays", "Sundays and holidays"],
                 ["First train from Central", "4:40 a.m.", "5:10 a.m.", "5:40 a.m."],
                 ["First train from Airport", "5:05 a.m.", "5:35 a.m.", "6:05 a.m."],
                 ["Last train from Airport", "1:10 a.m.", "1:10 a.m.", "12:40 a.m."],
                 ["Every", "8 min. (6 a.m. to 9 p.m.), 15 min. other times", "10 min. / 15 min.", "12 min. / 15 min."]],
                [1.7 * inch, 1.9 * inch, 1.3 * inch, 1.7 * inch]),
         Spacer(1, 6),
         Paragraph("Running times from Airport: Commerce Park 5 minutes, University 14, Midtown 21, Central 27.", SANS),
         Paragraph("Fares", h2),
         Paragraph("Regular fares apply between Central and Commerce Park. Trips to or from Airport station pay a $4.50 "
                   "airport station charge in addition to the regular fare; transfers to buses are free for 90 minutes.",
                   SANS),
         Paragraph("Bus changes", h2),
         Paragraph("Route 97 Airport Express ends on Sunday, November 3. Routes 11, 26 and 58 are rerouted to serve "
                   "Commerce Park and University stations.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the 2027 program budget workbook
BUDGET_LINES = [
    ("Rank operations contract (Corran Ground Services, year 3 of 5)", 284600.00),
    ("Marshalling, 3.2 full-time equivalents", 196450.00),
    ("Dispatch system licence and support", 38920.00),
    ("Holding lot P7 lease (Authority real estate)", 61200.00),
    ("Forecourt rank: cleaning and maintenance", 22840.00),
    ("Signage, wayfinding and customer information", 9310.00),
]
OVERHEAD = 0.065
OTHER_REVENUE = [("Limousine and sedan permit fees", 74350.00), ("Shuttle and hotel courtesy vehicle permits", 31480.00),
                 ("Ground transportation advertising", 12328.80)]


def budget_figures():
    direct = sum(v for _, v in BUDGET_LINES)
    over = round(direct * OVERHEAD, 2)
    total = round(direct + over, 2)
    amount = round(total - sum(v for _, v in OTHER_REVENUE), 2)
    return direct, over, total, amount


def write_budget(path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    direct, over, total, amount = budget_figures()
    assert abs(amount - W.AMOUNT_2027) < 0.005, amount
    wb = Workbook()
    ws = wb.active
    ws.title = "Program budget 2027"
    bold = Font(name="Calibri", bold=True, size=11)
    head = PatternFill("solid", fgColor="DCE6F1")
    ws.append(["Velmont Airport Authority: Ground Transportation Program, budget 2027"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append(["Draft for the Finance and Audit Committee, 4 November 2026. Dollars."])
    ws.append([])
    ws.append(["Line", "Item", "Budget 2027"])
    for c in ws[4]:
        c.font = bold
        c.fill = head
    rows = [[i, item, v] for i, (item, v) in enumerate(BUDGET_LINES, start=1)]
    rows.append([7, "Allocated corporate overhead, 6.5% of lines 1 to 6", over])
    rows.append([8, "Total program cost", total])
    for j, (item, v) in enumerate(OTHER_REVENUE, start=9):
        rows.append([j, "Less: " + item.lower(), -v])
    rows.append([12, "Amount assigned to the taxi pickup fee", amount])
    for r in rows:
        ws.append(r)
    for r in ws.iter_rows(min_row=5, max_row=ws.max_row):
        r[2].number_format = '#,##0.00;(#,##0.00)'
        r[0].alignment = Alignment(horizontal="center")
    for c in ws[ws.max_row]:
        c.font = bold
    ws.append([])
    ws.append([None, "The amount assigned to the fee is the program's cost less its other revenues (FP-07 2.1)."])
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["B"].width = 58
    ws.column_dimensions["C"].width = 15
    ws.freeze_panes = "A5"
    wb.save(path)
    return amount


# ---------------------------------------------------------------- distractors: passenger statistics and the survey
def passenger_rows():
    rng = np.random.default_rng([W.SEED, 91])
    out = []
    for (y, m) in W.months():
        g = (1 + W.GROWTH) ** (((y - 2024) * 12 + m - 7) / 12)
        s = W.SEAS[m - 1] / (sum(W.SEAS) / 12)
        days = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
        base = 5480 * g * s * days
        enp = int(round(base * np.exp(rng.normal(0, 0.012))))
        dep = int(round(base * np.exp(rng.normal(0, 0.012)) * (1.004 if m in (1, 8, 9) else 0.996)))
        mov = int(round(base / 92.0 * np.exp(rng.normal(0, 0.01))))
        out.append(["%d-%02d" % (y, m), enp, dep, enp + dep, mov])
    return out


def write_passengers(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Monthly traffic"
    ws.append(["Velmont International Airport: passengers and aircraft movements"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append(["Source: airline traffic returns; aircraft movements from the airfield operations log."])
    ws.append([])
    ws.append(["Month", "Enplaned passengers", "Deplaned passengers", "Total passengers", "Aircraft movements"])
    for c in ws[4]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="E2EFDA")
    for r in passenger_rows():
        ws.append(r)
    for r in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in r[1:]:
            c.number_format = "#,##0"
    for col, w in zip("ABCDE", (10, 20, 20, 18, 19)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)


def write_survey(path):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Ground access survey 2023", W.AUTHORITY, W.AUTHORITY + "  |  Ground access survey, October 2023")
    shares = [["Mode", "Arriving passengers", "Departing passengers"],
              ["Private vehicle, picked up or dropped off", "31.4%", "36.2%"],
              ["Private vehicle, parked", "22.7%", "24.1%"],
              ["Taxi", "11.8%", "8.9%"],
              ["App-based vehicle", "14.6%", "13.1%"],
              ["Rental car", "9.3%", "7.6%"],
              ["Bus (Route 97 Airport Express and others)", "6.1%", "6.0%"],
              ["Hotel courtesy shuttle", "3.6%", "3.4%"],
              ["Other", "0.5%", "0.7%"]]
    purpose = [["Trip purpose", "Share of passengers", "Taxi share within purpose"],
               ["Business", "27.3%", "16.4%"], ["Leisure", "51.8%", "8.1%"], ["Visiting friends or relatives", "20.9%", "9.7%"]]
    s = [Paragraph("Ground access survey 2023", h1),
         Paragraph("Intercept survey of 4,212 passengers in the terminal, 10 to 23 October 2023. Weighted to the "
                   "month's enplaned and deplaned passengers.", h1s),
         Paragraph("How passengers reach and leave the airport", h2),
         _table(shares, [3.2 * inch, 1.5 * inch, 1.5 * inch]),
         Spacer(1, 8),
         Paragraph("By trip purpose (both directions)", h2),
         _table(purpose, [2.6 * inch, 1.6 * inch, 1.9 * inch]),
         Spacer(1, 8),
         Paragraph("Notes", h2),
         Paragraph("Shares are of passengers, not of vehicles. App-based vehicles have been licensed in Velmont since "
                   "2018. The survey will be repeated after the forecourt reconstruction.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the folder's contents
INDEX = [
    ("trips2024", "City of Velmont Vehicle-for-Hire Office", "2025-02-03",
     "Annual file 2024, airport extract (trips with a pickup or drop-off in zone 1)."),
    ("trips2025", "City of Velmont Vehicle-for-Hire Office", "2026-02-06",
     "Annual file 2025, airport extract."),
] + [("drop%02d" % m, "City of Velmont Vehicle-for-Hire Office", d,
      "Monthly file %s, airport extract." % dt.date(2026, m, 1).strftime("%B %Y"))
     for m, d in zip(range(1, 9), ("2026-03-06", "2026-04-07", "2026-05-08", "2026-06-05", "2026-07-07",
                                   "2026-08-06", "2026-09-04", "2026-10-02"))] + [
    ("archive", "City of Velmont Vehicle-for-Hire Office", "2024-03-15",
     "Daily origin-destination archive 2023 for trips with a pickup or drop-off in zone 1."),
    ("zones", "City of Velmont Vehicle-for-Hire Office", "2019-06-01", "Taxi zone list (zone map 2019)."),
    ("brokerages", "City of Velmont Vehicle-for-Hire Office", "2026-10-09", "Licensed taxi brokerages."),
    ("affiliations", "City of Velmont Vehicle-for-Hire Office", "2026-10-09",
     "Taxi licences and the brokerage each was affiliated with, by effective date."),
    ("dictionary", "City of Velmont Vehicle-for-Hire Office", "2026-02-09", "Taxi trip records: data dictionary, v3.1."),
    ("bylaw", "Velmont Airport Authority", "2026-01-02", "Ground Transportation Fees By-law GT-3, consolidated."),
    ("policy", "Velmont Airport Authority", "2023-06-14", "Finance Policy FP-07: Budgeting user-fee revenue."),
    ("budget", "Velmont Airport Authority", "2026-10-14", "Ground Transportation Program budget 2027, draft."),
    ("notice", "Velmont Airport Authority", "2026-08-14", "Ground Transportation Notice GT-2024-11, revision 2."),
    ("bulletin", "Velmont Transit", "2024-10-21", "Service Bulletin 2024-19: the Airport Line."),
    ("passengers", "Velmont Airport Authority", "2026-09-22", "Passengers and aircraft movements, monthly."),
    ("survey", "Velmont Airport Authority", "2024-02-26", "Ground access survey, October 2023."),
]


def write_index(path, counts):
    import pack as P
    rows = []
    for k, src, asof, desc in INDEX:
        n = counts.get(k, "")
        rows.append([W.FILES[k], src, asof, desc, n])
    return P.write_csv(path, ["file_name", "source", "as_of", "description", "rows"], rows)
