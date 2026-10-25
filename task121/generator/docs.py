"""The pack's documents: the agency's technical note and topline report for the spring 2026 wave, the Western Rail
Partnership's letter requiring the recovery plan, the contract's Schedule 7 (service quality measures and
drivers), and the fleet register workbook."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1b2430"), colors.HexColor("#56616c"), colors.HexColor("#b8c0c8")
TEAL = colors.HexColor("#0f5c63")
PLUM = colors.HexColor("#4b2a55")
SLATE = colors.HexColor("#2e3f50")


def styles(face="Sans", accent=TEAL):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.0, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.5, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.8, leading=14, textColor=INK, spaceBefore=8, spaceAfter=2,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.2, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.9, leading=10.1, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28),
        sub=ParagraphStyle("s", parent=body, leftIndent=44, firstLineIndent=-16))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(20 * mm, A4[1] - 13 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 13 * mm, right)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=(), head_bg=colors.HexColor("#e8eef0")):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
          ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    for c in right:
        st.append(("ALIGN", (c, 1), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author, subject, left, right):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                             producer=author), _frame(left, right)


def write_technote(path, stats):
    S = styles("Sans", TEAL)
    doc, fr = _doc(path, "Customer Satisfaction Tracker: technical note, spring 2026", K.AGENCY,
                   "Technical note", K.AGENCY + " for " + K.OPERATOR, "CST technical note, spring 2026")
    P = lambda t, s="body": Paragraph(t, S[s])
    f = [P("Customer Satisfaction Tracker", "h1"),
         P("Technical note for the spring 2025 and spring 2026 waves. Prepared for %s by %s. Version 1.1, "
           "11 May 2026. Contact: %s, Associate Director." % (K.OPERATOR, K.AGENCY, K.PEOPLE["agency"]), "meta"),
         P("1. What the tracker measures", "h2"),
         P("The tracker asks passengers about the journey they are making on the day they are given a "
           "questionnaire. It has run in a spring wave and an autumn wave each year since 2021; this note covers "
           "the two spring waves the operator compares year on year."),
         P("2. Sample design", "h2"),
         P("Trains are sampled from the operator's working timetable for the fieldwork weeks, in strata defined by "
           "service group (Marlvale Main Line, Hollin Vale, Coastway, Pellow Branch, Corrington Link) and time band "
           "(weekday morning peak, inter-peak, evening peak and evening, and weekends). A fieldworker boards the "
           "sampled train at one of its stations, rides it to a later station and hands a questionnaire to every "
           "passenger aboard in the unit or units covered (on a train of two units the fieldworker usually covers "
           "one). Trains due at their last station after 23:45 are not sampled. The fieldwork log records each "
           "batch: the train, the stations between which the fieldworker rode, the units covered and the "
           "questionnaires handed out."),
         P("Passengers return the questionnaire by freepost or complete it online with the serial printed on it. "
           "Questionnaires received up to 28 days after the end of fieldwork are included. Spring 2025 fieldwork "
           "ran from %s to %s, spring 2026 from %s to %s." % (
               K.WAVES[2025][0].strftime("%-d %B %Y"), K.WAVES[2025][1].strftime("%-d %B %Y"),
               K.WAVES[2026][0].strftime("%-d %B %Y"), K.WAVES[2026][1].strftime("%-d %B %Y"))),
         _table(S, [["Wave", "Batches", "Questionnaires handed out", "Returned", "Return rate"]] + [
             [w, "{:,}".format(stats["batches"][w]), "{:,}".format(stats["issued"][w]),
              "{:,}".format(stats["returned"][w]), "%.1f%%" % (100.0 * stats["returned"][w] / stats["issued"][w])]
             for w in (2025, 2026)], [32 * mm, 22 * mm, 46 * mm, 26 * mm, 26 * mm], right=(1, 2, 3, 4)),
         P("Source: %s fieldwork records." % K.AGENCY, "note"),
         P("3. Questionnaire", "h2"),
         P("Q1 asks how satisfied the passenger was with this journey overall, on a five-point scale (very "
           "satisfied, fairly satisfied, neither satisfied nor dissatisfied, fairly dissatisfied, very "
           "dissatisfied). Q5 asks the passenger to rate ten aspects of the journey on the same scale, with a "
           "no-opinion box; the spring 2026 questionnaire added an eleventh aspect, the Wi-Fi on the train, and "
           "moved the Q5 block from page 1 to page 2 so the journey questions come first. No wording changed. The "
           "passenger also writes in the stations they joined and left the train, and gives their ticket type, "
           "journey purpose, how often they travel and their age band."),
         _table(S, [["Item", "Aspect rated"]] + [[q.upper(), a] for q, a in K.ITEMS] + [[K.ITEM_2026[0].upper(), K.ITEM_2026[1] + " (spring 2026 only)"]],
                [22 * mm, 128 * mm]),
         P("4. Data file conventions", "h2"),
         P("Ratings are coded 1 (very dissatisfied) to 5 (very satisfied); 9 is the no-opinion box and a blank is "
           "a question left unanswered. Written-in stations are given as written and, where the coding frame "
           "recognised them, with their three-letter station code; the remainder are left uncoded. The "
           "batch identifier links each questionnaire to the fieldwork log."),
         P("5. Weighting", "h2"),
         P("Within each wave, returned questionnaires are weighted so that each service group and time band "
           "carries its share of the passenger journeys made on the operator's trains in the fieldwork weeks, "
           "from the operator's journey estimates. The weights sum to the number of questionnaires returned in the "
           "wave. All results the agency reports are weighted."),
         P("6. Reporting", "h2"),
         P("A passenger is satisfied when they answer very or fairly satisfied (codes 4 and 5). Percentages are "
           "of those who answered the question: the no-opinion box and blanks are left out of the base for that "
           "question. Changes between waves are in percentage points."),
         P("The tracker is a sample: changes of less than about two points in the overall result, or of less "
           "than about four points for a single service group, are within the range sampling alone produces "
           "between waves.", "note")]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_topline(path, stats):
    S = styles("Sans", TEAL)
    doc, fr = _doc(path, "Customer Satisfaction Tracker: spring 2026 topline", K.AGENCY, "Topline report",
                   K.AGENCY + " for " + K.OPERATOR, "CST spring 2026 topline")
    P = lambda t, s="body": Paragraph(t, S[s])
    s25, s26 = stats["overall"][2025], stats["overall"][2026]
    f = [P("Customer Satisfaction Tracker: spring 2026 topline", "h1"),
         P("%s for %s. Issued 11 May 2026. Weighted results; the base for each aspect is passengers who "
           "rated it." % (K.AGENCY, K.OPERATOR), "meta"),
         P("Overall satisfaction with the journey fell from %.0f%% in spring 2025 to %.0f%% in spring 2026, the "
           "lowest spring result since the tracker began. Every aspect the questionnaire asks about was rated "
           "lower than a year earlier. The new Wi-Fi question is reported for the first time." % (s25, s26)),
         _table(S, [["", "Spring 2025", "Spring 2026", "Change (points)"]] + [
             ["Satisfied with the journey overall", "%.0f%%" % s25, "%.0f%%" % s26, "%+.0f" % (round(s26) - round(s25))]] + [
             [a[0].upper() + a[1:], "%.0f%%" % stats["items"][q][2025], "%.0f%%" % stats["items"][q][2026],
              "%+.0f" % (round(stats["items"][q][2026]) - round(stats["items"][q][2025]))]
             for q, a in K.ITEMS] + [[K.ITEM_2026[1][0].upper() + K.ITEM_2026[1][1:], "-",
                                      "%.0f%%" % stats["items"]["q5k"][2026], "-"]],
                [76 * mm, 26 * mm, 26 * mm, 28 * mm], right=(1, 2, 3)),
         P("Percentage very or fairly satisfied. Source: %s, Customer Satisfaction Tracker, spring waves." % K.AGENCY, "note"),
         P("Returns", "h2"),
         P("Spring 2026: {:,} questionnaires returned from {:,} handed out on {:,} sampled trains; spring 2025: "
           "{:,} from {:,} on {:,}.".format(stats["returned"][2026], stats["issued"][2026], stats["batches"][2026],
                                            stats["returned"][2025], stats["issued"][2025], stats["batches"][2025]))]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_requirement(path, stats):
    S = styles("Serif", PLUM)
    doc, fr = _doc(path, "Customer satisfaction recovery plan: requirement", K.AUTHORITY, "Recovery plan requirement",
                   K.AUTHORITY, "Contract Management, ref WRP/CM/2026/118")
    P = lambda t, s="body": Paragraph(t, S[s])
    s25, s26 = stats["overall"][2025], stats["overall"][2026]
    f = [P(K.AUTHORITY, "h1"),
         P("Contract Management. Ref WRP/CM/2026/118. 2 October 2026.", "meta"),
         P("To: %s, Contract Performance Manager, %s<br/>From: %s, Contract Manager, %s" % (
             K.PEOPLE["contract"], K.OPERATOR_LTD, K.PEOPLE["authority"], K.AUTHORITY)),
         P("Subject: Customer satisfaction recovery plan (Schedule 7, paragraph 9)", "h2"),
         P("The spring 2026 wave of your Customer Satisfaction Tracker reports %.0f%% of passengers satisfied with "
           "their journey overall, against %.0f%% in spring 2025. Under Schedule 7, paragraph 9, a fall of three "
           "points or more between spring waves requires a recovery plan. Please submit it by %s." % (
               s26, s25, K.PLAN_DUE.strftime("%-d %B %Y"))),
         P("The plan must:"),
         P("(a)&nbsp;&nbsp;state which of the four service drivers in Part 3 of Schedule 7 (crowding, punctuality, "
           "on-board staffing and fares) accounts for most of the fall in the share of passengers satisfied overall "
           "between the spring 2025 and spring 2026 waves, and how many points of the fall it accounts for: the "
           "points by which the share satisfied would have fallen less had passengers' journeys met that driver as "
           "they did in spring 2025, the other three as they were;", "clause"),
         P("(b)&nbsp;&nbsp;fund the remedy for that driver from the Customer Experience Fund for 2027; and", "clause"),
         P("(c)&nbsp;&nbsp;report the Part 2 measures for each service group for the four weeks ending 19 September "
           "2026 as the plan's baseline.", "clause"),
         P("The share satisfied is as the tracker reports it (the agency's technical note). The Partnership will "
           "review the plan with your Customer Experience Committee before the Fund is drawn."),
         P("%s<br/>Contract Manager" % K.PEOPLE["authority"])]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_schedule(path):
    S = styles("Serif", SLATE)
    doc, fr = _doc(path, "Schedule 7: Service Quality", K.AUTHORITY + " and " + K.OPERATOR_LTD, "Contract schedule",
                   "Marlvale Network Contract", "Schedule 7: Service Quality (consolidated, April 2026)")
    P = lambda t, s="body": Paragraph(t, S[s])
    f = [P("Schedule 7: Service Quality", "h1"),
         P("Marlvale Network Contract between the %s and %s. Consolidated text incorporating variations to "
           "1 April 2026." % (K.AUTHORITY, K.OPERATOR_LTD), "meta"),
         P("Part 1. General", "h2"),
         P("1.1&nbsp;&nbsp;Times are those of the working timetable in force on the day, in local time. A train is "
           "identified by its train identity and the date it runs.", "clause"),
         P("1.2&nbsp;&nbsp;A service group is the group named in Annex A for the train's route.", "clause"),
         P("Part 2. Measures", "h2"),
         P("2.1&nbsp;&nbsp;<b>Punctuality.</b> A train is on time when it arrives at the final destination in the "
           "working timetable less than five minutes after the time shown there. A train that does not run, or "
           "does not reach that destination, is not on time. The measure is trains on time as a percentage of "
           "trains in the working timetable for the day.", "clause"),
         P("2.2&nbsp;&nbsp;<b>On-board staffing.</b> A train runs with on-board staff when a conductor, a host or a "
           "member of staff covering their turn works it. The measure is trains that ran with on-board staff as a "
           "percentage of trains that ran; a train that did not run at all is left out.", "clause"),
         P("2.3&nbsp;&nbsp;<b>Standing on arrival.</b> For each train in the working timetable to arrive at "
           "Marlvale Central between 07:00 and 09:59 on a weekday, the passengers on board on arrival less the "
           "standard-class seats of the train as formed that day, where that is more than nothing; the measure is "
           "the sum. Passengers on board on arrival are those recorded by the units' load-weigh equipment on "
           "departure from the station before Marlvale Central.", "clause"),
         P("Part 3. Service drivers", "h2"),
         P("3.1&nbsp;&nbsp;The service drivers the Operator reports against are, for a passenger's journey:", "clause"),
         P("(a)&nbsp;&nbsp;<b>crowding</b>: the train carried more passengers than standard-class seats between any two "
           "consecutive stations of the passenger's journey;", "sub"),
         P("(b)&nbsp;&nbsp;<b>punctuality</b>: the train arrived at the passenger's station five minutes or more "
           "after the working timetable;", "sub"),
         P("(c)&nbsp;&nbsp;<b>on-board staffing</b>: the train ran without on-board staff (2.2); and", "sub"),
         P("(d)&nbsp;&nbsp;<b>fares</b>: the change, in per cent, in the price of the passenger's ticket at the "
           "annual fares change of 4 January 2026.", "sub"),
         P("Part 4. Customer satisfaction", "h2"),
         P("9.&nbsp;&nbsp;Where the share of passengers satisfied with their journey overall in the Customer "
           "Satisfaction Tracker falls by three percentage points or more between spring waves, the Operator shall "
           "submit a recovery plan within such period as the Partnership notifies.", "clause"),
         P("Annex A. Service groups: Marlvale Main Line (Marlvale Central to Tregarrow), Hollin Vale (Marlvale "
           "Central to Hollinford), Coastway (Marlvale Central to Trevose Quay), Pellow Branch (Sennow to Pellow), "
           "Corrington Link (Marlvale Central to Corrington).", "note")]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_fleet(path, w):
    """The fleet register as the fleet engineer keeps it: the units, and the modifications log."""
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Units"
    head = ["Unit", "Class", "Vehicles", "Standard seats", "On lease from", "Off lease", "Depot", "Notes"]
    ws.append(head)
    for u in w.fleet:
        cls = u["cls"]
        veh, seats = K.CLASSES[cls]
        on = u["on"].isoformat() if u["on"] else "2019-12-15"
        off = u["off"].isoformat() if u["off"] else None
        note = None
        if cls == "166" and u["off"]:
            note = "Released to the lessor at the October 2025 cascade"
        if cls == "150/2" and u["on"]:
            note = "Cascaded in October 2025"
        ws.append([u["unit"], "Class " + cls, veh, seats, on, off, "Marlvale TMD", note])
    ws2 = wb.create_sheet("Modifications")
    ws2.append(["Unit", "Modification", "Out of service", "Returned to traffic", "Standard seats after"])
    for u in w.fleet:
        if u["refurb"]:
            a, b = u["refurb"]
            ws2.append([u["unit"], "Interior refresh: cycle area and wheelchair space (C4 exam)", a.isoformat(),
                        b.isoformat(), K.CLASSES["158/9"][1]])
    for s in (ws, ws2):
        for c in s[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DCE6E8")
        s.freeze_panes = "A2"
    for col, wd in zip("ABCDEFGH", (10, 12, 9, 15, 14, 12, 14, 48)):
        ws.column_dimensions[col].width = wd
    for col, wd in zip("ABCDE", (10, 58, 15, 19, 21)):
        ws2.column_dimensions[col].width = wd
    wb.properties.creator = K.PEOPLE["fleet"]
    wb.save(path)


def write_dictionary(path):
    """Field notes for the operating extracts, as the performance team keeps them beside the exports."""
    F = K.FILES
    txt = """MARLVALE TRAINS - OPERATING EXTRACTS: FIELD NOTES
Performance and Planning, issued with the extracts of 23 October 2026. Times are local (UK) unless a field says
otherwise. A train is its train identity (headcode) on its run date; train_uid identifies a schedule within one
working timetable.

{tt}
  timetable            Dec24 (in force to 13 December 2025) or Dec25 (from 14 December 2025).
  train_uid            The schedule's identifier in that timetable.
  headcode             Train identity. Headcodes are reissued at each timetable change.
  service_group        Code of the service group (Annex A of Schedule 7): MAIN, VALE, COAST, BRANCH, LINK.
  days_run             MO-FR, SAT or SUN. Bank holidays run the SUN schedules.
  call_seq, station    Calling order and station code; arr and dep are the public times (blank at the ends).

{mv}
  One row per recorded arrival or departure. wtt_time is the working timetable time; recorded_time is the time
  the train describer recorded, to the minute. A train cancelled in full has no rows; a train cancelled part way has
  rows up to the station where it terminated.

{lw}
  Passengers on board estimated from each unit's suspension load on departure from a station. Class 166 units
  report each vehicle (vehicle = unit-number and position); other classes report the unit. Recorder downloads
  were not recovered for a few units on some days.

{fm}
  The units that formed each train, from the fleet allocation system as worked. position 1 is the leading unit.

{fl}
  Units: one row per unit with its class, vehicles and standard seats. Modifications: works that changed a unit's
  layout, with the date it returned to traffic and its standard seats afterwards.

{cw}
  One row per train worked by a member of on-board staff (conductor or host), from the as-worked archive
  (to 30 April 2026). The archive was closed when the new rostering platform went live on 17 May 2026.

{cr}
  The new rostering platform: one row per on-board turn and day. status is Rostered (worked by the member of
  staff shown), Sick (the member of staff shown was off sick) or Vacant (the turn was not filled). workings lists
  the trains in the diagram the turn covers.

{ca}
  A spare member of staff put on a turn, as the crew controller logged it: amend_date and logged are the date and
  time of the log entry; original_staff_ref is the member of staff the turn was rostered to (blank for a vacancy).

{fa}
  Fares by flow and ticket type before and after the annual fares change of 4 January 2026, in pence.

{st}
  Station codes and names, with the service groups calling there.
""".format(tt=F["timetable"], mv=F["movements"], lw=F["loadweigh"], fm=F["formations"], fl=F["fleet"],
           cw=F["crew_worked"], cr=F["crew_roster"], ca=F["crew_amend"], fa=F["fares"], st=F["stations"])
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(txt)
