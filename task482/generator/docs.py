"""The pack's documents: the City's notes on its station status archive, the operating agreement's Schedules A, C
and D as consolidated to Amendment 2, and Northlane's quarterly report for Q4 2026 (all PDF)."""
import datetime as dt
from collections import Counter

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)
GRID = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                   ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#777777")),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4), ("TOPPADDING", (0, 0), (-1, -1), 2.0),
                   ("VALIGN", (0, 0), (-1, -1), "TOP")])
CITY = "City of Wellhaven, Transportation Services"
NORTHLANE = "Northlane Mobility Inc."


def _doc(path, title, org):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.85 * inch, title=title, author=org, creator=org, producer=org, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, "%s  |  %s" % (org, title))
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def _p(items):
    return [Paragraph(x, BODY) for x in items]


def _t(rows, widths):
    t = Table(rows, colWidths=[w * inch for w in widths], hAlign="LEFT")
    t.setStyle(GRID)
    return t


def write_notes(path, gaps):
    title = "Bike share station status archive: collection notes"
    d, frame = _doc(path, title, CITY)
    s = [Paragraph("Bike Share Station Status Archive", TITLE),
         Paragraph("City of Wellhaven, Transportation Services, Data and Systems. Notes for the archive file "
                   "wellhaven_station_status_archive_2026q4.csv, 23 September 2026 to 10 January 2027. "
                   "Issued 12 January 2027.", SUB),
         Paragraph("What the archive holds", HEAD)]
    s += _p(["The City's poller requests Northlane Mobility's public station status feed for Wellhaven Bike Share "
             "(GBFS 2.3, station_status.json) once a minute, at the top of the minute. A row is written for a station "
             "whenever a poll finds any of its fields different from the last row written for that station, so a "
             "station's status at any time is the last row written for it at or before that time. The first poll, and "
             "the first poll after each spell in which the poller was down, writes a row for every station in the "
             "feed.",
             "The archive starts at the poll at 20:01 on 23 September 2026 (Eastern time), the minute after the "
             "third-quarter extract, and ends with the poll before 20:00 on 10 January 2027, when the City took the "
             "extract for the fourth-quarter review."])
    s += [Paragraph("Fields", HEAD)]
    rows = [["Field", "Meaning"],
            ["polled_at", "Time of the poll, UTC, in seconds since 1 January 1970"],
            ["station_id", "Northlane's feed station ID (the City's station numbers are in the station list)"],
            ["num_bikes_available", "Bikes docked at the station and available for rental"],
            ["num_bikes_disabled", "Bikes docked at the station that Northlane has marked out of service"],
            ["num_docks_available", "Empty docks able to take a bike"],
            ["num_docks_disabled", "Docks out of service"],
            ["is_installed, is_renting, is_returning", "Station flags as published (1 yes, 0 no)"],
            ["last_reported", "The feed's own time of the station's last status report, UTC, seconds since 1 January 1970"]]
    s.append(_t([[a, Paragraph(b, ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=9.6))] for a, b in rows],
                (1.9, 4.6)))
    s += [Spacer(1, 6), Paragraph("Spells the poller was down", HEAD)]
    s += _p(["The poller was down in the spells below (Eastern time). No row was written in a spell; the first poll after "
             "it wrote every station."])
    rows = [["From", "To", "Minutes"]]
    for start, mins in gaps:
        end = start + dt.timedelta(minutes=mins)
        rows.append([start.strftime("%Y-%m-%d %H:%M"), end.strftime("%Y-%m-%d %H:%M"), str(mins)])
    s.append(_t(rows, (1.6, 1.6, 0.8)))
    s += [Spacer(1, 6), Paragraph("Stations", HEAD)]
    s += _p(["Linden Avenue (W-17) moved across the street on the evening of 8 November 2026 and has published under "
             "feed ID 125 since then; feed ID 117 stopped publishing at the move. Birch Hill (W-16) and Willow Crescent (W-19) each gained "
             "four docks in November. The station list gives each station's feed IDs and dates."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_agreement(path):
    title = "Bike Share Operating Agreement, Schedules A, C and D"
    d, frame = _doc(path, title, CITY)
    s = [Paragraph("Bike Share Operating Agreement", TITLE),
         Paragraph("Between the City of Wellhaven and Northlane Mobility Inc., dated 2 April 2024. Schedules A, C and D "
                   "as consolidated to Amendment 2 (effective 1 May 2026). Schedule B (fees and revenue) and Schedule E "
                   "(insurance) are not reproduced here.", SUB),
         Paragraph("Schedule A. Stations", HEAD)]
    s += _p(["A.1 The stations are the numbered stations W-01 to W-24 in the City's station list, which also gives the "
             "feed station ID the Operator publishes each station under. A station the City moves within its block keeps "
             "its number and remains the same station.",
             "A.2 Each station has a pay station at which a customer can buy a single ride or a day pass by card.",
             "A.3 Times and dates in these Schedules are Eastern time, daylight or standard as in force."])
    s += [Paragraph("Schedule C. Station Availability", HEAD)]
    s += _p(["C.1 In this Schedule, <i>service hours</i> are 6:00 a.m. to midnight, Eastern time, every day; a bike is "
             "<i>in working order</i> when a customer can unlock it and ride it away; and a minute of service hours is an "
             "<i>available minute</i> at a station when at least one bike in working order is docked at the station at "
             "the start of the minute.",
             "C.2 A station's availability for a calendar month is its available minutes as a percentage of the minutes "
             "of service hours in that month.",
             "C.3 Every station whose availability is under 90 per cent in any calendar month of a quarter is a priority "
             "station for the following quarter. The City names the priority stations by notice to the Operator by the "
             "15th day of the following quarter.",
             "C.4 For each priority station the Operator keeps a rebalancing crew within ten minutes' drive of the "
             "station from 7:00 to 10:00 a.m. and 4:00 to 7:00 p.m. on weekdays from 1 February to 30 April of the "
             "following quarter, or for the whole of a quarter that does not include those months.",
             "C.5 Each month the Operator gives the City its trip records, its fleet moves log (each bike its vans or "
             "staff take from or leave at a station) and the fault reports customers make in the app. The City keeps an "
             "archive of the Operator's public station status feed. The City determines availability from these "
             "records."])
    s += [Paragraph("Schedule D. Fleet Maintenance", HEAD)]
    s += _p(["D.1 A customer can report a fault on a bike in the app. The Operator marks a reported bike out of service "
             "within two hours of the report and collects it on the next van or mechanic's visit to its station.",
             "D.2 The Operator's mechanics inspect each station on the cycle in Table D-1 and take any bike with a fault "
             "to the depot for repair. A bike returns to service when the depot has repaired it.",
             "D.3 The Operator's vans fill each station before service hours begin, answer the empty-station and "
             "full-station alerts its dispatch system raises in service hours, and move bikes between stations and the "
             "depot as the fleet needs.",
             "D.4 From 1 December the Operator may take bikes off the street for the winter, leaving at least 45 per cent "
             "of each station's docks filled after each storage run."])
    rows = [["Stations", "Inspection", "Window"],
            ["Downtown, campus and transit hub stations (W-01 to W-11)", "Every day", "10:00 a.m. to 3:00 p.m."],
            ["Neighbourhood and park stations (W-12 to W-24)", "Every third or fourth day, on the rota the Operator "
             "files with the City each quarter", "1:00 to 5:00 p.m."]]
    s += [Paragraph("Table D-1. Station inspection cycle", HEAD),
          _t([[a, Paragraph(b, ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=9.6)), c] for a, b, c in rows],
             (3.0, 2.2, 1.3))]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_report(path, E):
    f = E["f"]
    title = "Wellhaven Bike Share quarterly report, Q4 2026"
    d, frame = _doc(path, title, NORTHLANE)
    trips = Counter()
    casual = Counter()
    moves = Counter()
    reports = Counter()
    for t in f.trips:
        if t["user"] == "staff":
            continue
        mo = W.to_local(W.START + dt.timedelta(minutes=t["start_minute"])).month
        trips[mo] += 1
        if E["rtype"][t["trip"]] == "casual":
            casual[mo] += 1
    for mv in f.moves:
        moves[W.to_local(W.START + dt.timedelta(minutes=mv["minute"])).month] += 1
    for r in f.reports:
        reports[W.to_local(W.START + dt.timedelta(minutes=r["minute"])).month] += 1
    s = [Paragraph("Wellhaven Bike Share: Quarterly Report", TITLE),
         Paragraph("Northlane Mobility Inc. to the City of Wellhaven, Transportation Services. Fourth quarter 2026. "
                   "Submitted 14 January 2027.", SUB),
         Paragraph("Ridership", HEAD)]
    s += _p(["Ridership followed the season down from October, with the usual drop after the first snowfall in late "
             "November and the December storage runs. Casual riders took a larger share of weekend trips at the "
             "waterfront and park stations."])
    rows = [["", "October", "November", "December", "Quarter"]]
    for lab, c in (("Trips", trips), ("Trips by casual riders", casual), ("Fleet moves (vans and staff)", moves),
                   ("Fault reports from customers", reports)):
        rows.append([lab] + ["{:,}".format(c[m]) for m in (10, 11, 12)] + ["{:,}".format(c[10] + c[11] + c[12])])
    s.append(_t(rows, (2.4, 0.9, 0.9, 0.9, 0.9)))
    s += [Paragraph("Operations", HEAD)]
    s += _p(["Linden Avenue moved to the north side of the street on the evening of 8 November for the City's "
             "sidewalk widening, and "
             "Birch Hill and Willow Crescent each gained four docks. The pay-station vendor's terminal refurbishment "
             "program ran from 26 October to 27 November, one pay station each working day. Storage runs on 1, 8 and 15 "
             "December took bikes to the depot for the winter.",
             "Customer contacts were steady at about 40 a week, most of them about memberships and day-pass refunds. The "
             "fall rider survey (412 responses) rated the service 3.9 out of 5."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)
