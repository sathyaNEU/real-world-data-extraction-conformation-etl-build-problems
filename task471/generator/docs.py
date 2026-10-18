"""The pack's documents: the survey contractor's methods report and handout log, the bureau's pitch standard, Kessick
Valley Regional's 2027 nonstop schedule, Brennick's public parking rates and the bureau's 2025 ground access survey."""
import datetime as dt
from collections import defaultdict

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1e21")
GREY = colors.HexColor("#5a5f66")
NAVY = colors.HexColor("#1f3b5c")
TEAL = colors.HexColor("#22545a")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def styles(font="LiberationSans", accent=NAVY, size=9.8):
    bold = font + "-Bold"
    return dict(
        BODY=ParagraphStyle("body", fontName=font, fontSize=size, leading=size * 1.37, textColor=INK, spaceAfter=6),
        CELL=ParagraphStyle("cell", fontName=font, fontSize=8.2, leading=10.2, textColor=INK),
        CELLB=ParagraphStyle("cellb", fontName=bold, fontSize=8.2, leading=10.2, textColor=INK),
        SMALL=ParagraphStyle("small", fontName=font, fontSize=8.0, leading=10.4, textColor=GREY, spaceAfter=4),
        H1=ParagraphStyle("h1", fontName=bold, fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        H1S=ParagraphStyle("h1s", fontName=font, fontSize=9, leading=12, textColor=GREY, spaceAfter=10),
        H2=ParagraphStyle("h2", fontName=bold, fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3))


S = styles()


def _doc(path, title, footer, author, size=letter):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.5)
        canvas.drawString(0.9 * inch, 0.6 * inch, footer)
        canvas.drawRightString(size[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=size, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, st=S, head="#e3e9f1", right=()):
    data = [[Paragraph(str(v), st["CELLB"] if i == 0 else st["CELL"]) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
             ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    t.setStyle(TableStyle(style))
    return t


def _story(title, sub, sections, st=S):
    story = [Paragraph(title, st["H1"]), Paragraph(sub, st["H1S"])]
    for head, paras in sections:
        if head:
            story.append(Paragraph(head, st["H2"]))
        for p in paras:
            story.append(p if not isinstance(p, str) else Paragraph(p, st["BODY"]))
    return story


def _fmt(n):
    return "{:,}".format(int(n))


def _day(d):
    return "%d %s" % (d.day, MONTHS[d.month - 1])


def _wdate(d):
    return "%s %d/%d/%d" % (["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][d.weekday()], d.month, d.day, d.year)


def wave_dates():
    out = []
    for name, q, start in W.WAVES:
        last = start + dt.timedelta(days=W.HAND_DAYS - 1)
        close = start + dt.timedelta(days=W.LAST_COLLECT - 1)
        out.append((name, q, start, last, close))
    return out


# ---------------------------------------------------------------------------------------------- the methods report
def write_methods(path, x):
    st = styles("LiberationSerif", TEAL, 10.0)
    d, frame = _doc(path, "Brennick International long-stay parking survey 2026: methods and delivery",
                    "%s  |  Brennick International long-stay parking survey 2026" % W.CONTRACTOR, W.CONTRACTOR)
    handed = defaultdict(int)
    for w, day, l, a, b, n in x["handout"]:
        handed[w] += n
    keyed = defaultdict(int)
    for c in x["cards"]:
        keyed[c["wave"]] += 1
    t1 = [["Wave", "Handout days", "Last box collection", "Cards handed", "Cards returned and keyed"]]
    for name, q, start, last, close in wave_dates():
        t1.append([name[1], "%s to %s 2026" % (_day(start), _day(last)), "Night of %s 2026" % _day(close),
                   _fmt(handed[name]), _fmt(keyed[name])])
    t1.append(["2026", "", "", _fmt(sum(handed.values())), _fmt(sum(keyed.values()))])
    dict_cards = [["Column", "Contents"],
                  ["card_no", "The number printed on the card: the wave's digit followed by a six-digit serial."],
                  ["wave", "1 to 4."],
                  ["keying_batch", "The wave and the batch the card was keyed in."],
                  ["box_collected", "The date stamped on the night's box run when the card came out of the box, "
                                    "yyyy-mm-dd."],
                  ["home_zip", "Q1 as written."],
                  ["destination_code", "Q2 coded: the airport's three-letter code where the card names an airport, "
                                       "or a city's main airport where it names only the city; CHI, NYC or WAS where "
                                       "it names only Chicago, New York or Washington."],
                  ["nights", "Q3 as written."],
                  ["party", "Q4 coded as a number."],
                  ["purpose", "Q5 coded B (business), L (leisure), V (visiting friends or relatives) or O (other)."]]
    dict_verb = [["Column", "Contents"],
                 ["card_no", "As in the cards file."],
                 ["question", "Q2 or Q4."],
                 ["as_written", "The answer keyed as the traveller wrote it."]]
    secs = [
        ("1. The survey", [
            "1.1 The State %s's %s commissioned %s to survey the cars parked in the three long-stay lots at "
            "%s (Economy C, Economy D and Long-Term) through 2026: where their travellers live, where they flew, "
            "how long they were away and how many of them flew. The short-term garage was not surveyed."
            % (W.STATE_AGENCY, W.BUREAU, W.CONTRACTOR, W.HUB),
            "1.2 The survey ran in four waves, one in each quarter of 2026. Each wave's 28 days of entries stand for "
            "its quarter."]),
        ("2. Handout", [
            "2.1 Each wave ran for 28 consecutive days from a Monday: %s." % ", ".join(
                "%s to %s" % (_day(s), _day(l)) for _, _, s, l, _ in wave_dates()),
            "2.2 At the entry plaza of each lot (Plaza C for Economy C, Plaza D for Economy D and Plaza L for "
            "Long-Term) attendants handed a card to the driver of each car taking a ticket. Cars entering while an "
            "attendant was away from the lane were missed, more of them in the August wave, when the contractor was "
            "short of attendants. The permit lanes were not covered.",
            "2.3 Each card carries a printed seven-digit number, the wave's digit followed by a serial. The "
            "attendants recorded the first and last number handed at each plaza each day; the handout log lists "
            "them with the number of cards handed."]),
        ("3. Returns", [
            "3.1 The card asks the traveller to answer when they get back to the car and to drop the card in the box "
            "at the lot's exit plaza on the way out (Appendix A). The boxes were emptied every night after the last "
            "exits of the day, and each night's cards were stamped with that day's date.",
            "3.2 Each wave's boxes were emptied for the last time on the night of the second day after its last "
            "handout day, and then taken in until the next wave.",
            _table(t1, [0.5 * inch, 1.9 * inch, 1.6 * inch, 1.0 * inch, 1.5 * inch], st, head="#dfecea"),
            Spacer(1, 4),
            Paragraph("Table 1. Cards by wave. Cards returned and keyed are counted once each.", st["SMALL"])]),
        ("4. Keying and coding", [
            "4.1 The cards were keyed in batches as they came out of each night's box, up to 450 a batch, and "
            "delivered in two files. The cards file has one row for each card:",
            _table(dict_cards, [1.3 * inch, 5.2 * inch], st, head="#dfecea"), Spacer(1, 6),
            "4.2 The verbatims file has the answers to Q2 and Q4 as keyed from the card, one row for each card and "
            "question:",
            _table(dict_verb, [1.3 * inch, 5.2 * inch], st, head="#dfecea"), Spacer(1, 6),
            "4.3 The files are the cards as keyed and coded; expansion to the lots' entries is the Bureau's."]),
        ("Appendix A. The card", [
            _table([["%s PARKING SURVEY" % W.HUB_SHORT.upper()],
                    ["Please answer when you get back to your car and drop this card in the box at the exit booth "
                     "as you leave. Thank you for helping us plan air service for the region."],
                    ["Q1  Your home ZIP code"],
                    ["Q2  The final destination of your trip (city or airport)"],
                    ["Q3  How many nights were you away?"],
                    ["Q4  How many people flew in your travel party, including you?"],
                    ["Q5  The main purpose of your trip: business, leisure, visiting friends or relatives, other"]],
                   [6.5 * inch], st, head="#f2f2f2")]),
    ]
    story = _story("Brennick International long-stay parking survey 2026: methods and delivery",
                   "%s for the %s, %s. %s, Project Manager. 15 December 2026." % (
                       W.CONTRACTOR, W.BUREAU, W.STATE_AGENCY, W.PEOPLE["contractor"]), secs, st)
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the handout log
def write_handout(path, x):
    st = styles("LiberationSans", TEAL, 9.4)
    d, frame = _doc(path, "Brennick International parking survey 2026: handout log",
                    "%s  |  Parking survey 2026, handout log" % W.CONTRACTOR, W.CONTRACTOR)
    story = [Paragraph("Brennick International long-stay parking survey 2026: handout log", st["H1"]),
             Paragraph("%s. Compiled from the plaza attendants' sheets; the first and last card number handed at "
                       "each plaza each day and the cards handed." % W.CONTRACTOR, st["H1S"])]
    for i, (name, q, start, last, close) in enumerate(wave_dates()):
        if i:
            story.append(PageBreak())
        story.append(Paragraph("Wave %s: %s to %s 2026" % (name[1], _day(start), _day(last)), st["H2"]))
        rows = [["Date", "Plaza", "First card", "Last card", "Cards handed"]]
        tot = 0
        for w, day, lot, a, b, n in x["handout"]:
            if w != name:
                continue
            rows.append([_wdate(day), W.PLAZA[lot], P.card_no(int(name[1]), a), P.card_no(int(name[1]), b),
                         _fmt(n)])
            tot += n
        rows.append(["Wave %s" % name[1], "", "", "", _fmt(tot)])
        story.append(_table(rows, [1.2 * inch, 0.9 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch], st,
                            head="#dfecea"))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the pitch standard
def shortlist_rows():
    rows = [["Market", "Code", "Airports"]]
    for m in W.SHORTLIST:
        name, aps = W.CITY_MARKETS[m]
        rows.append([name, m, ", ".join(a for a, _ in aps)])
    return rows


def write_standard(path):
    st = styles("LiberationSans", NAVY, 9.8)
    d, frame = _doc(path, "Air Service Pitch Standard, 2027 pitch",
                    "%s, %s  |  Air Service Pitch Standard, 2027 pitch" % (W.STATE_AGENCY, W.BUREAU), W.BUREAU)
    secs = [
        ("1. Purpose", [
            "1.1 Each year the Bureau's air service development office pitches three markets for new nonstop service "
            "from %s to the network planners of the airlines. This standard sets the basis on which the three are "
            "chosen, so that each year's pitch is made the same way." % W.REGIONAL]),
        ("2. The basis", [
            "2.1 The basis is the trips that the Kessick Valley service area makes by car to %s and parks in its "
            "long-stay lots (Economy C, Economy D and Long-Term) to fly. The short-term garage is not part of the "
            "basis." % W.HUB,
            "2.2 A trip is one car's stay in the long-stay lots, from entry to exit, counted once whatever the size "
            "of its party, in the year the car entered. A pitch uses the latest full calendar year: the 2027 pitch "
            "uses the trips that entered in 2026.",
            "2.3 A trip is the service area's when its party's home ZIP code is on the Bureau's Kessick Valley "
            "service area ZIP list.",
            "2.4 The lots' entries are the transient entries counted by Brennick's parking revenue control system. "
            "Permit holders' entries (employees and tenants) are not trips.",
            "2.5 A trip's market is the city market of its final destination under the Bureau's city-market table, "
            "which groups each city's airports and the metropolitan codes used for them.",
            "2.6 Every such trip counts, not only the trips a survey reached.",
            "2.7 The passengers a trip carried are the people in its party who flew, counted in full."]),
        ("3. Candidates", [
            "3.1 The candidates for a pitch are the markets on the shortlist drawn up by the office's market review "
            "(Appendix A) that have no nonstop service from %s in its published schedule for the pitch year. A "
            "market with nonstop service to any of its airports, seasonal service included, is not a candidate."
            % W.REGIONAL_SHORT]),
        ("4. The pitch", [
            "4.1 The office pitches the three candidates with the most trips.",
            "4.2 The pitch file lists every candidate's trips and passengers in the basis year. The pitch brief "
            "names the three, the first candidate left out and the trips that separate it from the third.",
            "4.3 Trips and passengers are reported to the nearest hundred."]),
        ("Appendix A. Shortlist, 2027 pitch", [
            "From the office's market review of July 2026.",
            _table(shortlist_rows(), [1.6 * inch, 0.7 * inch, 2.4 * inch], st)]),
    ]
    story = _story("Air Service Pitch Standard: 2027 pitch",
                   "%s, %s, Air Service Development. Approved by %s, Air Service Development Manager, "
                   "14 September 2026." % (W.STATE_AGENCY, W.BUREAU, W.PEOPLE["asd"]), secs, st)
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- KVR's schedule
def write_schedule(path):
    from reportlab.lib.pagesizes import landscape
    st = styles("LiberationSans", colors.HexColor("#3c4f1e"), 9.6)
    d, frame = _doc(path, "Kessick Valley Regional Airport nonstop schedule, 2027",
                    "%s (%s)  |  Nonstop schedule 2027" % (W.REGIONAL, W.REGIONAL_CODE), W.REGIONAL,
                    size=landscape(letter))
    rows = [["Airline", "Flight", "To", "Days", "Dep.", "Arr.", "Aircraft", "From", "Until"]]
    for car, fl, ap, days, dep, arr, eq, eff, dis in W.KVR_2027:
        rows.append([car, fl, "%s (%s)" % (W.AIRPORT_NAMES[ap], ap), days, dep, arr, eq,
                     dt.date.fromisoformat(eff).strftime("%d %b %Y") if eff else "",
                     dt.date.fromisoformat(dis).strftime("%d %b %Y") if dis else ""])
    secs = [
        (None, ["Nonstop departures from %s for 2027 as filed by the airlines on 20 January 2027. Times are local "
                "(Chicago is on Central time). "
                "Flights without dates operate all year; seasonal flights show their first and last day. Return "
                "flights operate on the same days." % W.REGIONAL_SHORT]),
        (None, [_table(rows, [1.75 * inch, 1.0 * inch, 2.3 * inch, 0.9 * inch, 0.5 * inch, 0.5 * inch,
                              0.7 * inch, 0.8 * inch, 0.8 * inch], st, head="#e6eddc")]),
        (None, [Spacer(1, 6), Paragraph("Kessick Valley Regional Airport is owned and operated by the %s, %s. "
                                        "Schedules change; check with the airline." % (W.BUREAU, W.STATE_AGENCY),
                                        st["SMALL"])]),
    ]
    story = _story("Kessick Valley Regional Airport (KVR): nonstop schedule, 2027", "Published 20 January 2027.",
                   secs, st)
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the parking rates
def write_rates(path):
    st = styles("LiberationSans", colors.HexColor("#5c2d1f"), 9.8)
    d, frame = _doc(path, "Brennick International public parking rates 2026",
                    "%s, Parking Operations  |  Public parking rates 2026" % W.HUB, W.HUB)
    rows = [["Facility", "Code", "Entry", "Rate", "Daily maximum", "Getting to the terminal"],
            ["Garage (short-term)", "GR", "Garage plaza", "$4 each 30 minutes", "$34", "Walk"],
            ["Long-Term", "LT", "Plaza L", "$5 an hour", "$18", "Walk or covered walkway"],
            ["Economy C", "EC", "Plaza C", "$4 an hour", "$13", "Shuttle every 10 minutes"],
            ["Economy D", "ED", "Plaza D", "$4 an hour", "$12", "Shuttle every 12 minutes"]]
    secs = [
        ("Rates", [_table(rows, [1.35 * inch, 0.5 * inch, 0.9 * inch, 1.25 * inch, 0.9 * inch, 1.6 * inch], st,
                          head="#f2e4dc"),
                   Spacer(1, 6),
                   "Take a ticket at the entry plaza and pay at the exit plaza by card, cash or the Brennick Parking "
                   "app. Receipts show the facility code. Rates effective 1 January 2026."]),
        ("Long-stay parking", [
            "Economy C, Economy D and Long-Term are for stays of one night or more as well as the day. Parking in "
            "the public lots is limited to 28 consecutive days; a vehicle parked longer is towed at the owner's "
            "expense (Airport Rules and Regulations, section 7.4).",
            "During peak travel weeks the economy lots can fill; the message signs on the airport parkway show which "
            "lots are open."]),
        ("Permits", [
            "Employees and tenants with an Brennick parking permit use the permit lanes at each plaza. Permits are "
            "issued by Parking Operations."]),
        ("Questions", [
            "%s, Parking Operations Manager, %s." % (W.PEOPLE["parking"], W.HUB)]),
    ]
    story = _story("Public parking at %s: rates and rules, 2026" % W.HUB_SHORT,
                   "%s, Parking Operations. Effective 1 January 2026." % W.HUB, secs, st)
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the 2025 access survey
ACCESS_MODES = ["Drove and parked at Brennick", "Parked off airport", "Dropped off", "Taxi or ride-hailing",
                "Rental car", "Hotel shuttle", "Bus or rail"]
ACCESS = {   # home area: interviews, shares by mode (per cent)
    "Brennick County": (2104, (31.8, 6.2, 34.9, 18.4, 2.3, 2.6, 3.8)),
    "Rest of the Brennick metro": (1196, (44.6, 9.1, 28.7, 9.8, 1.9, 3.2, 2.7)),
    "Kessick Valley service area": (612, (63.1, 7.4, 21.7, 3.1, 1.8, 2.4, 0.5)),
    "Elsewhere in the state": (517, (52.4, 5.8, 23.6, 4.9, 5.1, 7.3, 0.9)),
    "Out of state": (383, (8.1, 0.6, 21.2, 30.3, 26.4, 12.9, 0.5)),
}
ACCESS_PARTY = {"Drove and parked at Brennick": 1.71, "Parked off airport": 1.84, "Dropped off": 1.62,
                "Taxi or ride-hailing": 1.27, "Rental car": 1.58, "Hotel shuttle": 1.66, "Bus or rail": 1.09}


def write_access(path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Mode by home area"
    ws.append(["How departing passengers reached %s, October 2025 (per cent of passengers)" % W.HUB_SHORT])
    ws.append([])
    ws.append(["Home area", "Interviews"] + ACCESS_MODES)
    for c in ws[3]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for area, (n, shares) in ACCESS.items():
        ws.append([area, n] + list(shares))
    ws.append(["All passengers", sum(v[0] for v in ACCESS.values())] + [
        round(sum(v[0] * v[1][i] for v in ACCESS.values()) / sum(v[0] for v in ACCESS.values()), 1)
        for i in range(len(ACCESS_MODES))])
    for c in ws[ws.max_row]:
        c.font = Font(name="Calibri", bold=True)
    for row in ws.iter_rows(min_row=4, min_col=3):
        for c in row:
            c.number_format = "0.0"
    for row in ws.iter_rows(min_row=4, min_col=2, max_col=2):
        for c in row:
            c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 11
    for col in "CDEFGHI":
        ws.column_dimensions[col].width = 14
    ws.row_dimensions[3].height = 32
    ws.freeze_panes = "B4"
    ws2 = wb.create_sheet("Party size")
    ws2.append(["Mode", "Mean party flying (interviewed passenger and those with them)"])
    for c in ws2[1]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for m, v in ACCESS_PARTY.items():
        ws2.append([m, v])
    for row in ws2.iter_rows(min_row=2, min_col=2):
        for c in row:
            c.number_format = "0.00"
    ws2.column_dimensions["A"].width = 30
    ws2.column_dimensions["B"].width = 58
    ws3 = wb.create_sheet("About")
    for line in ["%s, %s: departing passenger ground access survey, 2025" % (W.STATE_AGENCY, W.BUREAU),
                 "Interviews with departing passengers past the security checkpoint at %s, 6 to 26 October 2025, "
                 "at all hours the checkpoint was open; 4,812 interviews." % W.HUB_SHORT,
                 "Home areas from the passenger's home ZIP code. Shares are of passengers, weighted to the "
                 "checkpoint's hourly throughput.",
                 "Parked off airport: the private lots on the airport parkway.",
                 "Released 9 January 2026."]:
        ws3.append([line])
    ws3["A1"].font = Font(name="Calibri", bold=True)
    ws3.column_dimensions["A"].width = 110
    wb.save(path)
