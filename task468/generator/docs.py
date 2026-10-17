"""The pack's documents: the State Department of Transportation's program guidance, the ITS administrator's notes on
the Quinnell cutover and its export, Service Quality's trip-matching review memo, the department's ridership report,
its farebox workbook and its 2025 Title VI monitoring report (the last two distractors), and each file's date."""
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
NAVY = colors.HexColor("#1d3557")
TEAL = colors.HexColor("#0f5c63")
PLUM = colors.HexColor("#5a2a4f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.3, leading=10.8, textColor=GREY)


def styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.3, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
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


def _table(rows, widths, head="#e6eef0"):
    data = [[Paragraph(str(v), CELLB if i == 0 else CELL) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def us_date(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


# ---------------------------------------------------------------- the state's program guidance
def write_guidance(path):
    h1, h1s, h2 = styles(NAVY, serif=True)
    d, frame = _doc(path, "Frequent Transit Corridors Program: FY2027 guidance", W.STATE_DOT,
                    W.STATE_DOT + "  |  Office of Public Transportation  |  FTC Program guidance, FY2027", layout="centre")
    s = [Paragraph("Frequent Transit Corridors Program", h1),
         Paragraph("Guidance for the FY2027 round. Office of Public Transportation, %s. Issued July 15, 2026."
                   % W.STATE_DOT, h1s),
         Paragraph("1. About the program", h2),
         Paragraph("1.1 The Frequent Transit Corridors Program funds stop, shelter, real-time sign and transit signal "
                   "priority work on bus routes that have delivered frequent service. Awards are made to transit "
                   "agencies for the routes they nominate.", BODY),
         Paragraph("1.2 This guidance applies to nominations for state fiscal year 2027. Applications close on "
                   "December 1, 2026.", BODY),
         Paragraph("1.3 A transit agency may apply if it operates fixed-route bus service in the state and reports to "
                   "the National Transit Database.", BODY),
         Paragraph("1.4 Times and dates in this guidance are Central time.", BODY),
         Paragraph("2. Candidate routes and designated stops", h2),
         Paragraph("2.1 An agency names its candidate routes and, for each, a designated stop: one stop that every "
                   "trip of the route serves in one direction. A stop may be the designated stop of more than one "
                   "route.", BODY),
         Paragraph("3. The service standard", h2),
         Paragraph("3.1 A route qualifies if it meets the service standard in section 3.3 over the qualifying period, "
                   "January 1 to June 30, 2026.", BODY),
         Paragraph("3.2 A departure is a bus of the route in revenue service leaving the route's designated stop. It is "
                   "counted in the clock hour in which the bus left the stop.", BODY),
         Paragraph("3.3 A route meets the service standard if, in each of the thirteen clock hours beginning 6:00 a.m. "
                   "through 6:00 p.m., the total of its departures in that hour on the counting days, divided by the "
                   "number of counting days, is at least four.", BODY),
         Paragraph("3.4 The counting days are the weekdays of the qualifying period except the state holidays New "
                   "Year's Day (January 1), Martin Luther King Jr. Day (January 19), Presidents' Day (February 16) and "
                   "Memorial Day (May 25). Departures are counted from the agency's automatic vehicle location (AVL) "
                   "records for the counting days. A departure counts whether or not the agency's records tie it to "
                   "the route; where the records do not show the route of every departure, the agency reports its "
                   "estimate of each route's departures and keeps its working for audit.", BODY),
         Paragraph("4. The application", h2),
         Paragraph("4.1 The application is made by the agency and accompanied by a resolution of its governing body "
                   "authorizing the nominations and by the GTFS feeds of its published timetable for the qualifying "
                   "period.", BODY),
         Paragraph("4.2 For each nominated route the application gives the designated stop; the lowest of its thirteen "
                   "hourly averages under section 3.3; its average weekday boardings over the qualifying period; its "
                   "on-time performance (of the route's departures from 6:00 a.m. to 7:00 p.m. on the counting days "
                   "that the agency's AVL records tie to a trip, the share that left the designated stop no more than "
                   "one minute before and no more than five minutes after the trip's scheduled departure in the "
                   "published timetable); and "
                   "the average scheduled wait at the designated stop (the average time a rider arriving at a random "
                   "moment between 6:00 a.m. and 7:00 p.m. on a weekday of the agency's current service would wait "
                   "for the route's next scheduled departure).", BODY),
         Paragraph("5. Nominations", h2),
         Paragraph("5.1 An agency may nominate at most five routes, each of which meets the service standard. Where more "
                   "than five of its candidate routes meet the standard, it nominates the five with the highest average "
                   "weekday boardings over the qualifying period as reported in its ridership report.", BODY),
         Paragraph("5.2 The Office may audit an agency's AVL records and its estimate of any route's departures.", BODY),
         Paragraph("6. Awards", h2),
         Paragraph("6.1 Awards are made in March 2027 for work completed by June 30, 2029. The program funds 80 per "
                   "cent of eligible costs; the agency provides the remaining 20 per cent.", BODY),
         Spacer(1, 10),
         Paragraph("Questions to the Office of Public Transportation, (515) 555-0182.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the ITS administrator's cutover notes
def write_change_note(path):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Quinnell cutover: AVL export notes", W.PEOPLE["its"],
                    W.DEPARTMENT + "  |  ITS  |  Quinnell cutover: AVL export notes", layout="header")
    q_cols = [["Field", "Meaning"],
              ["EventID", "Quinnell's number for the row."],
              ["VehicleID", "Quinnell asset tag of the unit on the bus; the fleet roster gives the fleet number."],
              ["StopCode", "Public stop code (the code on the stop sign and in the feeds' stops.txt)."],
              ["ActualDepartureUTC", "When the bus left the stop, Coordinated Universal Time."],
              ["ScheduledDeparture", "The trip's scheduled departure from the stop in the GTFS feed in effect that "
               "day, service-day time (times past 24:00:00 run after midnight). Blank when no trip."],
              ["TripID, Route", "The trip in the feed in effect that day, and its route. Blank when no trip."],
              ["MatchStatus", "MATCHED, or NO TRIP when the matcher could not tie the event to a trip."],
              ["DeviationSec", "Quinnell's schedule adherence: the departure against ScheduledDeparture, seconds, "
               "late positive. Blank when no trip."]]
    a_cols = [["Field", "Meaning"],
              ["event_id", "Arbor's event number."],
              ["svc_date", "The service day the event belongs to."],
              ["veh_no", "Fleet number."],
              ["stop_id", "Stop id in the January feed's stops.txt."],
              ["arr_time, dep_time", "When the bus reached and left the stop, local time."],
              ["route, trip_id, sched_dep", "The matched trip, its route and Arbor's schedule time for the trip at "
               "the stop. Blank when unmatched."],
              ["adherence_min", "Arbor's schedule adherence: dep_time against sched_dep, minutes to one decimal, late "
               "positive."]]
    s = [Paragraph("Quinnell cutover: AVL export notes", h1),
         Paragraph("%s, %s. Updated July 8, 2026." % (W.PEOPLE["its"], W.TITLES["its"]), h1s),
         Paragraph("Cutover", h2),
         Paragraph("Quinnell Transit Systems' CAD/AVL replaced Arbor Fleetware's at 7:00 p.m. on March 31, 2026 (00:00 "
                   "UTC on April 1). The Arbor units stayed powered until the buses pulled in that night, so Arbor's "
                   "export runs to the end of service on March 31 and Quinnell's begins at 7:00 p.m. that evening.", SANS),
         Paragraph("Trip matching", h2),
         Paragraph("Both systems tie a stop event to a scheduled trip when the bus is within seven minutes of the "
                   "trip's scheduled time at the stop. Quinnell's window was set to seven minutes at the cutover to "
                   "match Arbor's. An event the matcher cannot tie to a trip keeps its bus, stop and time and carries "
                   "no trip. Service Quality reviews a sample of these each month.", SANS),
         Paragraph("The exports for the program", h2),
         Paragraph("Both exports hold the stop events at the five transfer points that are the candidate routes' "
                   "designated stops, every hour and every day of the qualifying period. Quinnell delivers its export "
                   "as daily files; the second-quarter file is the daily files joined in order.", SANS),
         Paragraph("Quinnell export (avl_stop_events_2026q2_quinnell.csv)", h2),
         _table(q_cols, [1.45 * inch, 5.2 * inch]),
         Spacer(1, 6),
         Paragraph("Arbor export (avl_stop_events_2026q1_arbor.csv)", h2),
         _table(a_cols, [1.45 * inch, 5.2 * inch]),
         Paragraph("Stops and timetables", h2),
         Paragraph("The spring timetable began on April 5 with a new GTFS feed in which every stop id was renumbered; "
                   "stop codes did not change. Arbor's export uses the January feed's stop ids; Quinnell's uses stop "
                   "codes throughout.", SANS),
         Paragraph("Fleet", h2),
         Paragraph("The fleet roster lists each bus with the asset tag of the Quinnell unit fitted to it.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- Service Quality's review memo
def write_review_memo(path, frame_rows, findings):
    h1, h1s, h2 = styles(PLUM)
    d, frame = _doc(path, "Trip-matching review, January to June 2026", W.PEOPLE["quality"],
                    W.DEPARTMENT + "  |  Service Quality  |  Trip-matching review")
    tally = [["Month", "Bus-days listed", "Bus-days drawn", "Events reviewed", "Late beyond window", "Logon fault",
              "Out of service"]]
    for (m, listed, drawn), f in zip(frame_rows, findings):
        tally.append([dt.date(2026, m, 1).strftime("%B"), "{:,}".format(listed), drawn, drawn, f[0], f[1], f[2]])
    s = [Paragraph("Trip-matching review, January to June 2026", h1),
         Paragraph("%s, %s. To %s, %s. July 31, 2026." % (W.PEOPLE["quality"], W.TITLES["quality"], W.PEOPLE["its"],
                                                         W.TITLES["its"]), h1s),
         Paragraph("What the review is for", h2),
         Paragraph("Each month Service Quality checks why the AVL system's trip matcher leaves stop events at the five "
                   "transfer points without a trip: a bus running more than seven minutes from its timetable, an "
                   "operator logon fault, or a bus passing through out of service. The findings go to ITS for the "
                   "matcher's configuration and to Operations for schedule adherence.", SANS),
         Paragraph("How the sample is drawn", h2),
         Paragraph("When a month's service is complete we list its bus-days (a bus and a service day) on which the "
                   "AVL system left at least one stop event at the five transfer points without a trip. We "
                   "draw 250 bus-days from the list at random. For each bus-day drawn we draw one of its events "
                   "without a trip at random, retrieve the bus's CCTV for that moment, and record the route the bus "
                   "was operating, or that it was not in service, and why the matcher missed it. CCTV is kept for 30 "
                   "days, so the review runs monthly; pulling one recording per bus-day keeps it to a day's work a "
                   "week.", SANS),
         Paragraph("The log (trip_matching_review_2026h1.csv) gives each reviewed event, its bus, service date, stop, "
                   "time and source event number, the route operated and the finding.", SANS),
         Paragraph("Tally", h2),
         _table(tally, [0.85 * inch, 0.95 * inch, 0.85 * inch, 0.85 * inch, 0.95 * inch, 0.8 * inch, 0.85 * inch],
                head="#efe4ec"),
         Paragraph("Notes", h2),
         Paragraph("From April the events are Quinnell's; its window is seven minutes, like Arbor's, and the findings "
                   "run much as before. Logon faults fell after the cutover, as Quinnell's units take the run from "
                   "the dispatch system.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- distractor: Title VI service monitoring 2025
def write_equity(path):
    h1, h1s, h2 = styles(NAVY)
    d, frame = _doc(path, "Title VI service monitoring 2025", W.DEPARTMENT,
                    W.DEPARTMENT + "  |  Title VI program  |  Service monitoring 2025")
    r = np.random.default_rng([W.SEED, 51])
    rows = [["Route", "Name", "Minority route", "Peak load factor", "Vehicle age (years)", "Stops with shelter"]]
    for rt in sorted(W.ROUTE_NAMES, key=int):
        rows.append([rt, W.ROUTE_NAMES[rt], "Yes" if rt in ("2", "6", "9", "14", "22", "51") else "No",
                     "%.2f" % (0.55 + r.random() * 0.6), "%.1f" % (4 + r.random() * 6),
                     "%d%%" % int(18 + r.random() * 40)])
    s = [Paragraph("Title VI service monitoring 2025", h1),
         Paragraph("%s. Adopted by the Transit Advisory Board, March 2026." % W.DEPARTMENT, h1s),
         Paragraph("Purpose", h2),
         Paragraph("Under FTA Circular 4702.1B the department monitors its service standards and policies every three "
                   "years for minority and non-minority routes. A minority route is one where at least a third of the "
                   "route's revenue miles lie in census block groups with a minority share above the service area's.",
                   SANS),
         Paragraph("Route classification and indicators, 2025", h2),
         _table(rows, [0.55 * inch, 1.6 * inch, 0.95 * inch, 1.05 * inch, 1.1 * inch, 1.1 * inch]),
         Paragraph("Findings", h2),
         Paragraph("No disparate impact was found for vehicle load, vehicle assignment or stop amenities. Shelter "
                   "coverage on minority routes is within the board's 20 per cent band of non-minority routes.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the ridership report and the farebox workbook
def write_ridership(path, table):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekday average"
    ws.append(["Larkhaven Transit: average weekday boardings by route, January to June 2026"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append(["Automatic passenger counters, expanded to all trips under the department's NTD sampling plan. "
               "Weekdays less state holidays."])
    ws.append([])
    ws.append(["Route", "Name", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jan to Jun"])
    for c in ws[4]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
        c.alignment = Alignment(horizontal="center")
    for rt, nm, months, avg, sat, sun in table:
        ws.append([int(rt), nm] + months + [avg])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in row[2:]:
            c.number_format = "#,##0"
        row[0].alignment = Alignment(horizontal="center")
    for col, w in zip("ABCDEFGHI", (7, 22, 8, 8, 8, 8, 8, 8, 11)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C5"
    w2 = wb.create_sheet("Weekend average")
    w2.append(["Average Saturday and Sunday boardings by route, January to June 2026"])
    w2["A1"].font = Font(name="Calibri", bold=True, size=12)
    w2.append([])
    w2.append(["Route", "Name", "Saturday", "Sunday"])
    for c in w2[3]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for rt, nm, months, avg, sat, sun in table:
        w2.append([int(rt), nm, sat, sun])
    for row in w2.iter_rows(min_row=4, max_row=w2.max_row):
        for c in row[2:]:
            c.number_format = "#,##0"
    for col, w in zip("ABCD", (7, 22, 10, 10)):
        w2.column_dimensions[col].width = w
    wb.save(path)


def write_farebox(path, table):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Farebox revenue"
    ws.append(["Larkhaven Transit: farebox revenue by route, January to June 2026 (dollars)"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append([])
    ws.append(["Route", "Name", "Jan", "Feb", "Mar", "Apr", "May", "Jun"])
    for c in ws[3]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="FCE4D6")
    for rt, nm, vals in table:
        ws.append([int(rt), nm] + vals)
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row):
        for c in row[2:]:
            c.number_format = "#,##0.00"
    for col, w in zip("ABCDEFGH", (7, 22, 11, 11, 11, 11, 11, 11)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C4"
    wb.save(path)


# ---------------------------------------------------------------- each file's date in the folder
INDEX = [
    ("avl_q1", "Larkhaven Transit (Arbor Fleetware CAD/AVL export)", "2026-04-02",
     "AVL stop events at the five transfer points, January 1 to March 31, 2026."),
    ("avl_q2", "Larkhaven Transit (Quinnell Transit Systems CAD/AVL export)", "2026-07-06",
     "AVL stop events at the five transfer points from the Quinnell cutover to June 30, 2026."),
    ("review", "Larkhaven Transit, Service Quality", "2026-07-31", "Trip-matching review log, January to June 2026."),
    ("review_memo", "Larkhaven Transit, Service Quality", "2026-07-31", "Trip-matching review memo, January to June 2026."),
    ("gtfs_jan", "Larkhaven Transit", "2025-12-12", "GTFS feed, winter timetable from January 1, 2026."),
    ("gtfs_apr", "Larkhaven Transit", "2026-03-13", "GTFS feed, spring timetable from April 5, 2026."),
    ("ridership", "Larkhaven Transit, Planning", "2026-07-22", "Ridership report: average weekday boardings by route."),
    ("guidance", "State Department of Transportation", "2026-07-15", "Frequent Transit Corridors Program, FY2027 guidance."),
    ("change_note", "Larkhaven Transit, ITS", "2026-07-08", "Quinnell cutover: AVL export notes."),
    ("fleet", "Larkhaven Transit, Fleet", "2026-06-30", "Fleet roster with Quinnell asset tags."),
    ("equity", "Larkhaven Transit", "2026-03-11", "Title VI service monitoring 2025."),
    ("farebox", "Larkhaven Transit, Finance", "2026-07-16", "Farebox revenue by route, January to June 2026."),
    ("candidates", "Larkhaven Transit, Planning", "2026-07-24",
     "Candidate routes for the FY2027 nominations, with the designated stop each would name."),
]
