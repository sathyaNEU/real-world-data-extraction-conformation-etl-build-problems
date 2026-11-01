"""task157 architecture 3: the pack's documents. The franchise agreement's performance regime (Schedule 7, the
estimand and the relief rule), the council's traffic management plan for the Thornsby Bridge closure, and the
authority's close-out note on the 2025 Marsh Lane closure."""
from __future__ import annotations

import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import cm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import params as P   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1b222b"), colors.HexColor("#5b6570"), colors.HexColor("#bcc3cb")
CA_PURPLE = colors.HexColor("#4b2a6b")
COUNCIL_GREEN = colors.HexColor("#1f5a43")


def styles(face, accent):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.0, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.5, leading=18.5, textColor=accent, spaceAfter=3),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.2, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10.0, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=30, firstLineIndent=-30))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(2.2 * cm, A4[1] - 1.35 * cm, left)
        canvas.drawRightString(A4[0] - 2.2 * cm, A4[1] - 1.35 * cm, right)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.1 * cm,
                             bottomMargin=1.9 * cm, title=title, author=author, subject=subject,
                             creator="Microsoft Word for Microsoft 365", producer="Microsoft Word for Microsoft 365")


# ---------------------------------------------------------------------------- Schedule 7
SCHEDULE7_7_2 = ("A Departure is On Time if it is made no more than one minute before, and no more than five minutes "
                 "fifty-nine seconds after, the time shown for it in the Registered Timetable for that day. The "
                 "Punctuality of a Route over a period is the number of its Departures made On Time divided by the "
                 "number of its Departures the AVL System records in that period, expressed as a percentage. A "
                 "Departure the AVL System does not record is left out of both numbers.")


def write_schedule7(path):
    S = styles("Serif", CA_PURPLE)
    doc = _doc(path, "Bus Franchise Agreement Lot 2, Schedule 7: Performance Regime", P.AUTHORITY, "Schedule 7")
    fr = _frame(P.AUTHORITY + " - Bus Franchise Agreement, Lot 2 (Saltmeadow)", "Schedule 7, Performance Regime (v1.4)")
    s = []
    s.append(Paragraph("Schedule 7: Performance Regime", S["h1"]))
    s.append(Paragraph("Bus Franchise Agreement, Lot 2 (Saltmeadow), between %s and %s Limited. Consolidated version "
                       "1.4 incorporating Variation 3 (in force 31 August 2026). Extract: clauses 7.1 to 7.9."
                       % (P.AUTHORITY, P.OPERATOR), S["meta"]))
    s.append(Paragraph("7.1 Definitions", S["h2"]))
    defs = [
        ("AVL System", "the Authority's automatic vehicle location system, which records the time each Lot 2 vehicle "
                       "leaves or reaches each Timing Point."),
        ("Departure", "a scheduled departure of a journey on a Route from one of its Timing Points, other than the last "
                      "Timing Point of the journey, which is an arrival."),
        ("Disruption", "a closure, diversion or restriction of the highway, or other event outside the Operator's "
                       "control, which the Authority expects to affect one or more Routes for 14 days or more."),
        ("Excused Event", "an event listed in clause 7.5."),
        ("Period", "each of the thirteen four-week periods of the Authority's financial year."),
        ("Registered Timetable", "the timetable for a Route registered for the day concerned, as published in the "
                                 "Authority's TransXChange data."),
        ("Route", "each Lot 2 service identified by its service number."),
        ("Timing Point", "a stop shown as a principal timing point in the Registered Timetable."),
    ]
    for k, v in defs:
        s.append(Paragraph("<b>%s</b> means %s" % (k, v), S["clause"]))
    s.append(Paragraph("7.2 Punctuality", S["h2"]))
    s.append(_clause(S, "7.2.1", SCHEDULE7_7_2))
    s.append(_clause(S, "7.2.2", "Times are compared to the second, in local time. Punctuality is reported to one "
                     "decimal place."))
    s.append(Paragraph("7.3 Punctuality Floor and Deduction", S["h2"]))
    s.append(_clause(S, "7.3.1", "The Punctuality Floor is 80 per cent for every Route."))
    s.append(_clause(S, "7.3.2", "For each Period in which a Route's Punctuality is below the Punctuality Floor, the "
                     "Authority deducts from the Service Payment GBP 4,250 for each whole percentage point, or part of "
                     "one, by which it is below."))
    s.append(Paragraph("7.4 Reliability", S["h2"]))
    s.append(_clause(S, "7.4.1", "Scheduled Kilometres are the kilometres of the Route Links of every journey in the "
                     "Registered Timetable. Lost Kilometres are the Scheduled Kilometres of the journeys, or of the "
                     "parts of journeys, not operated; a journey that ends before its last stop, or starts after its "
                     "first, loses the Route Links it does not run."))
    s.append(_clause(S, "7.4.2", "Reliability for a Route over a period is its Scheduled Kilometres less its Lost "
                     "Kilometres other than those lost to an Excused Event, divided by its Scheduled Kilometres, "
                     "expressed as a percentage. Reliability is reported to two decimal places."))
    s.append(Paragraph("7.5 Excused Events", S["h2"]))
    s.append(_clause(S, "7.5.1", "The Excused Events are: (a) a road closed or obstructed by the police or the "
                     "emergency services; (b) works or a closure by a highway authority or a statutory undertaker of "
                     "which the Operator had less than seven days' notice; (c) severe weather, including flooding; "
                     "(d) an obstruction caused by another vehicle's breakdown or collision; (e) a civil emergency."))
    s.append(_clause(S, "7.5.2", "For the avoidance of doubt, a vehicle defect, a shortage or illness of staff, a "
                     "ticket machine or AVL fault, traffic congestion, and a decision to turn a journey short to "
                     "restore the timetable are not Excused Events."))
    s.append(Paragraph("7.6 Disruption Notices", S["h2"]))
    s.append(_clause(S, "7.6.1", "Where the Authority knows of a Disruption, it may issue a Disruption Notice to the "
                     "Operator. The notice states the Disruption's first and last days and, for each Route, the "
                     "Authority's forecast of that Route's Punctuality over the whole Disruption, every day of it, "
                     "on the Registered Timetable for those days. It also states each Route's Reliability over the "
                     "record the forecast rests on, against which Reliability during the Disruption is reported, and "
                     "the boardings at any stops the Disruption leaves unserved, which the Operator's passenger "
                     "information for the Disruption must cover."))
    s.append(_clause(S, "7.6.2", "During the Disruption the Punctuality Deduction does not apply to a Route whose "
                     "forecast in the notice is below the Punctuality Floor. Every other Route remains subject to "
                     "clause 7.3."))
    s.append(_clause(S, "7.6.3", "A Disruption Notice has effect only if the Authority issues it at least 21 days "
                     "before the first day of the Disruption. A Route not named in a notice that has effect cannot be "
                     "added to it once the Disruption has begun."))
    s.append(_clause(S, "7.6.4", "Reliability continues to be measured on every Route during a Disruption."))
    s.append(Paragraph("7.7 Reporting", S["h2"]))
    s.append(_clause(S, "7.7.1", "The Authority publishes each Route's Punctuality for each calendar month, "
                     "provisionally in the following month and finally once late AVL data has been loaded."))
    s.append(Paragraph("7.8 Records", S["h2"]))
    s.append(_clause(S, "7.8.1", "The Operator keeps, and on request supplies, its duty schedules, daily returns "
                     "of uncovered work, ticket machine data and vehicle records for each Period."))
    s.append(Paragraph("7.9 Review", S["h2"]))
    s.append(_clause(S, "7.9.1", "The Authority and the Operator review this Schedule at each timetable change."))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------- the traffic management plan
def write_tm_plan(path):
    S = styles("Sans", COUNCIL_GREEN)
    doc = _doc(path, "Thornsby Bridge closure: Traffic Management Plan", P.COUNCIL, "TMP-2026-117 v2")
    fr = _frame(P.COUNCIL + " - Highways and Transportation", "Thornsby Bridge closure TMP, ref. TMP-2026-117, v2")
    s = []
    s.append(Paragraph("Thornsby Bridge (A6046) bearing replacement: full closure", S["h1"]))
    s.append(Paragraph("Traffic Management Plan, reference TMP-2026-117, version 2, 27 November 2026. Prepared by "
                       "%s, Bridges and Structures Manager. Supersedes version 1 (20 November 2026)." %
                       P.PEOPLE["council"], S["meta"]))
    s.append(Paragraph("1. The works", S["h2"]))
    s.append(Paragraph(
        "The principal inspection of Thornsby Bridge on 2 November 2026 found section loss to the bearings at the "
        "south abutment. The bearings will be replaced with the deck jacked, which needs the bridge closed to all "
        "vehicles. The closure runs from 06:00 on Monday 11 January 2027 to 23:59 on Sunday 28 March 2027. The east "
        "footway stays open to pedestrians and cyclists except on four weekends, which will be notified separately.",
        S["body"]))
    s.append(Paragraph("2. Diversion for general traffic", S["h2"]))
    s.append(Paragraph(
        "Traffic is diverted in both directions via Tenter Street, the Ring Road crossing (Junction 4 to Junction 5) "
        "and Ravensholme Road. Signal timings at Junction 4 and at the Saltmeadow Lane junction will be revised for "
        "the duration.", S["body"]))
    s.append(Paragraph("3. Bus services", S["h2"]))
    s.append(Paragraph(
        "Service 41 is the only bus service that crosses Thornsby Bridge. It is diverted in both directions between "
        "Tenter Street and Ravensholme Road by the general traffic diversion. The stops at Thornsby Road, Bridge End "
        "and Thornsby Quay are not served in either direction, and no temporary stops are provided on the diversion. "
        "Agreed with the Combined Authority and Pellbridge Buses at the bus liaison meeting on 25 November 2026: "
        "service 41 runs to its registered timetable on the diversion, and closure notices go up at the three stops "
        "from 4 January 2027.", S["body"]))
    s.append(Paragraph("The council's journey time model gives the following for buses on the diversion, per "
                       "journey in each direction:", S["body"]))
    s.append(_table(S, [["", "Weekday morning peak, 07:30 to 09:30", "Weekday evening peak, 16:00 to 18:30",
                         "All other times"],
                        ["Additional running time, Tenter Street to Ravensholme Road", "13 minutes", "13 minutes",
                         "10 minutes"],
                        ["Additional distance, northbound (towards Ravensholme)", "3.6 km", "3.6 km", "3.6 km"],
                        ["Additional distance, southbound (towards the city)", "3.4 km", "3.4 km", "3.4 km"]],
                    [6.2, 3.6, 3.6, 3.2]))
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        "Traffic on the Ring Road crossing between Junction 4 and the Junction 5 and Saltmeadow Lane slips is "
        "expected to take about 2 minutes longer in the weekday peaks with the diverted traffic added. No change is "
        "expected there at other times.", S["body"]))
    s.append(Paragraph("4. Other measures", S["h2"]))
    s.append(Paragraph(
        "Parking suspensions on Ravensholme Road (east side) during the peaks; enforcement cameras at Junction 4; "
        "advance signing from 14 December 2026; variable message signs on the A6046 and the Ring Road; a weekly "
        "progress note to the Combined Authority and the emergency services.", S["body"]))
    s.append(Paragraph("5. Monitoring", S["h2"]))
    s.append(Paragraph(
        "Journey time surveys on the diversion in weeks 1 and 2, with signal timings adjusted where queues exceed "
        "the modelled lengths. The council will not change the diversion route without seven days' notice to the "
        "Combined Authority.", S["body"]))
    s.append(Paragraph("Contact: Bridges and Structures, Grainford City Council, Civic Centre, Grainford.", S["note"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------- the 2025 close-out
def write_closeout(path, rows):
    """rows: (band, plan minutes, realised minutes) for route 14 outbound, and the punctuality figures."""
    S = styles("Serif", CA_PURPLE)
    doc = _doc(path, "Marsh Lane outbound closure 2025: close-out note", P.AUTHORITY, "Network performance note 25/07")
    fr = _frame(P.AUTHORITY + " - Bus Network Performance", "Close-out note NP 25/07, 30 May 2025")
    s = []
    s.append(Paragraph("Marsh Lane outbound closure, 3 March to 13 April 2025: close-out note", S["h1"]))
    s.append(Paragraph("Network performance note NP 25/07, 30 May 2025. Author: %s, Head of Bus Network Performance."
                       % P.PEOPLE["authority"], S["meta"]))
    s.append(Paragraph("1. The closure", S["h2"]))
    s.append(Paragraph(
        "Northern Gas Networks closed Marsh Lane to traffic leaving the city between Mill Bank and the Oxenstall "
        "turn for a mains replacement. Traffic towards the city was not affected. Route 14's outbound journeys used "
        "the signed diversion via Dyke Road; its inbound journeys ran normally.", S["body"]))
    s.append(Paragraph("2. Running time", S["h2"]))
    s.append(Paragraph("The council's traffic management plan estimated the added outbound running time. The AVL "
                       "record for the closure gives the following against the four weeks before it:", S["body"]))
    s.append(_table(S, [["Route 14 outbound, Mill Bank to Oxenstall", "Plan estimate", "AVL, mean added time"]] +
                    [[r[0], r[1], r[2]] for r in rows["running"]], [7.6, 3.6, 4.4], right=(1, 2)))
    s.append(Spacer(1, 5))
    s.append(Paragraph("3. Disruption Notice", S["h2"]))
    s.append(Paragraph(
        "The Authority issued a Disruption Notice on 7 February 2025 under clause 7.6 of Schedule 7. Route 14's "
        "forecast punctuality for the closure was %s per cent, below the floor, and the punctuality deduction was "
        "not applied to it for the closure. Route 14's recorded punctuality over the closure was %s per cent." %
        (rows["forecast"], rows["realised"]), S["body"]))
    s.append(Paragraph("4. Points for future closures", S["h2"]))
    s.append(Paragraph(
        "The plan's running time estimates were within half a minute of the AVL record in both bands. Notices should "
        "continue to be issued as early as the council's programme allows; this one was issued 24 days before the "
        "closure. The council's journey time model will be used again for the Thornsby Bridge inspection programme.",
        S["body"]))
    doc.build(s, onFirstPage=fr, onLaterPages=fr)
