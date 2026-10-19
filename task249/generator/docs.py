"""task249's documents: the request thread, the quality plan, the station sheet, the maintenance log, the firmware
note, the head datasheet, the March visit sheets, the dictionary and the folder contents."""
import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import params as P
import nodes as N
import postprocess

AADAN = ("Adán Ruano", "aruano")
MATILDE = ("Matilde Criado", "mcriado")
EDEL = ("Edelmira Urrutia", "eurrutia")
PAULINO = ("Paulino Cardona", "pcardona")


def _addr(who, domain):
    return "%s <%s@%s>" % (who[0], who[1], domain)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.5,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.2, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.9, leading=9.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAF0"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _build(doc, s, foot):
    doc.build(s, onFirstPage=_footer(foot), onLaterPages=_footer(foot))


def _sections(s, sec, body, h2):
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))


# ------------------------------------------------------------------ the request thread (eml)
def request(path):
    text = f"""From: {_addr(MATILDE, P.DOMAIN)}
To: Datos red de ozono <datos.ozono@{P.DOMAIN}>
Cc: {_addr(PAULINO, P.DOMAIN)}
Date: Thu, 01 Jun 2028 09:12:44 +0200
Subject: Fwd: June round - pull list
Message-ID: <20280601091244.3301@{P.DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Hola,

Adán needs the pull list for the June round by tomorrow (his note below). It is
the last round before the ozone season, so the list follows the quality plan as
it stands: every node whose span over the eight weeks to 31 May is outside the
band goes to the bench. The node export runs to 31 May (23:00 UTC) and the
regional network's provisional release to the same hour.

One more thing for the same workbook: the foundation's quarterly report wants
each node's data capture for its first full winter quarter, November to January.

Gracias,
Matilde

-------- Forwarded message --------
From: {_addr(AADAN, P.CONTRACTOR_DOMAIN)}
To: {_addr(MATILDE, P.DOMAIN)}
Date: Tue, 30 May 2028 17:40:02 +0200
Subject: June round - pull list

Matilde,

We start the June round on Monday 12 June. Please send me the list of nodes
that come down for the bench by Friday 2 June so that I can book the bench at
Parque de la Dehesa and take spare units for those sites. The others get the
usual inlet cleaning on the same visit.

OZ14 and OZ30 are on their new roofs since March, as in my visit sheets.

Un saludo,
Adán Ruano
{P.CONTRACTOR}
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# ------------------------------------------------------------------ the quality plan (pdf)
def plan(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Quality assurance plan for the low-cost ozone network", h1),
         Paragraph("%s, version 3, January 2028. Prepared by %s (sensor scientist); approved by %s (network "
                   "coordinator). Replaces version 2 of September 2027." % (P.CENTRE, PAULINO[0], MATILDE[0]), small),
         Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "The centre runs 36 low-cost ozone nodes across the comarca. Each node carries one gas-sensitive "
            "semiconductor head (tungsten oxide) and reports over the mobile network. Two models are in service: "
            "OZN-A and OZN-B. Nodes are sited at background locations, on the roofs of schools and municipal "
            "buildings at least 50 m from any road carrying more than 2,000 vehicles a day."]),
        ("2. Records", [
            "A node reports its ozone in parts per billion (ppb), stamped with the start of the record's interval in "
            "UTC. Each record carries a status code (listed in the data dictionary) and the time it reached the "
            "centre. A record the node sends again after a break in its link carries a later received time."]),
        ("3. Setting a head", [
            "Before installation each node spent a week on the bench beside the reference analyser at Alcorna - "
            "Parque de la Dehesa (regional network station ES4101A) and was set so that its span was 1.00 and its "
            "zero 0 ppb against the analyser. A node set again at a round is set the same way."]),
        ("4. Span and the pull list", [
            "A node's span is the change in its reading for a unit change in the true ozone concentration at its "
            "inlet, as a week on the bench measures it. At each round the coordinator lists for recalibration every "
            "node whose span over the eight weeks before the list is set lies outside 0.85 to 1.15. A node on the "
            "list is taken to the bench, measured and set again; the others are cleaned where they stand.",
            "A node's zero drifts as well. It is re-set from the node's own night-time readings at every round and "
            "is not a reason to take a node down."]),
        ("5. The reference between rounds", [
            "Between rounds no node sits beside an analyser. The regional network's four ozone analysers in the "
            "comarca are the network's reference. Their hourly values come from the regional network's validated "
            "release for past years and its provisional release for the current year."]),
        ("6. Data capture", [
            "A node's data capture over a period is the number of hours, in local time, in which it reported at least "
            "one accepted reading."]),
        ("7. Rounds", [
            "Three rounds a year: March (cleaning), June (before the summer ozone season) and October. The June and "
            "October rounds take down the nodes on the pull list; every visit cleans the inlet."]),
    ]
    _sections(s, sec, body, h2)
    d = _doc(path, "Quality assurance plan, low-cost ozone network, v3", P.CENTRE, "Network QA plan")
    _build(d, s, "%s - QA plan v3 - January 2028" % P.CENTRE_SHORT)
    postprocess.scrub(path, P.CENTRE, "2028-01-22")


# ------------------------------------------------------------------ the regional network's station sheet (pdf)
def stations(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Ozone analysers in the comarca of Alcorna", h1),
         Paragraph("%s. Station sheet prepared by %s, data officer, for the users of the network's ozone data. "
                   "Issued 15 April 2028 with the validated release for 2026 and 2027." % (P.NETWORK, EDEL[0]), small),
         Spacer(1, 4)]
    lat = lambda y: P.LAT0 + y / 111.0
    import math
    lon = lambda x: P.LON0 + x / (111.0 * math.cos(math.radians(P.LAT0)))
    kind = {"ES4101A": "suburban background", "ES4102A": "suburban background", "ES4103A": "rural background",
            "ES4104A": "rural background"}
    model = {"ES4101A": "Thermo 49i", "ES4102A": "Thermo 49i", "ES4103A": "Thermo 49i", "ES4104A": "Teledyne T400"}
    elev = {"ES4101A": 712, "ES4102A": 719, "ES4103A": 694, "ES4104A": 738}
    rows = [["Code", "Station", "Type", "Latitude", "Longitude", "Elevation (m)", "Analyser"]]
    for code, name, x, y in P.ANALYSERS:
        rows.append([code, name.replace("Mencia", "Mencía"), kind[code], "%.4f" % lat(y), "%.4f" % lon(x), elev[code], model[code]])
    s.append(_grid(rows, [17 * mm, 44 * mm, 28 * mm, 17 * mm, 18 * mm, 18 * mm, 24 * mm], cell))
    sec = [
        ("Method and units", [
            "Ozone is measured by ultraviolet photometry (EN 14625). Values are hourly means in micrograms per cubic "
            "metre (µg/m³) at 20 °C and 101.3 kPa."]),
        ("Times", [
            "All times are UTC+1 throughout the year. The column hora runs from 1 to 24 and gives the hour ending at "
            "that time on the date in fecha: hora 1 is 00:00 to 01:00 and hora 24 is 23:00 to 24:00."]),
        ("Flags", [
            "V validated, P provisional, N not valid. The validated release keeps the recorded value of an hour flagged "
            "N; the provisional release leaves it blank. Each analyser runs a span check at 11:00 on Tuesdays "
            "while the station is visited, and that hour is flagged N. On 21 September 2027 the analyser at "
            "Villarejo de Menc\u00eda (ES4104A) read high from 11:00 to 17:00 with a failing lamp; those hours are flagged N."]),
        ("Torralba del Campo (ES4103A)", [
            "The analyser was replaced on 4 July 2027. From the hour ending 11:00 that day the station's values are the "
            "new analyser's (serial TE49i-1342). The old analyser (TE49i-0921) ran beside it until 17 July for "
            "comparison, and its values for those days are in the validated release under its own serial."]),
        ("Releases", [
            "The validated release for 2026 and 2027 replaces every earlier release for those years. The provisional "
            "release is refreshed daily from 1 December of the previous year; values in it may change at validation.",
            "For the target value for the protection of human health, the network takes the maximum daily 8-hour mean "
            "from the 8-hour running means of the hourly values, each assigned to the day on which it ends, an 8-hour "
            "mean counting when at least six of its hours are valid and a day counting when at least 18 of its 8-hour "
            "means do."]),
    ]
    _sections(s, sec, body, h2)
    d = _doc(path, "Ozone analysers in the comarca of Alcorna", P.NETWORK, "Station sheet")
    _build(d, s, "%s - station sheet, ozone - 15 April 2028" % P.NETWORK)
    postprocess.scrub(path, "RRVCA Calidad del Aire", "2028-04-15")


# ------------------------------------------------------------------ the maintenance log (pdf)
def maintenance(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Maintenance log, low-cost ozone network, September 2027 to May 2028", h1),
         Paragraph("%s. Kept by %s with the contractor's visit reports (%s). Last entry 18 May 2028." %
                   (P.CENTRE, PAULINO[0], P.CONTRACTOR), small), Spacer(1, 4),
         Paragraph("Installation", h2),
         Paragraph("Each node spent its bench week at Alcorna - Parque de la Dehesa before it went up, and every "
                   "head was set to span 1.00 and zero 0 ppb against analyser ES4101A.", body)]
    rows = [["Node", "Municipality", "Bench week from", "Installed", "Model"]]
    for i, (code, town, _, _) in enumerate(N.NODES):
        inst = N.install_date(i)
        rows.append([code, town.replace("Mencia", "Mencía"), (inst - dt.timedelta(days=8)).strftime("%d %b %Y"),
                     inst.strftime("%d %b %Y"), "OZN-B" if code in N.MODEL_B else "OZN-A"])
    s.append(_grid(rows, [16 * mm, 46 * mm, 32 * mm, 28 * mm, 18 * mm], cell))
    s.append(Paragraph("Events", h2))
    ev = [["Date (local)", "Event"],
          ["27 Nov 2027", "Storm. Power cut 14:00 to 19:00 in Villarejo de Mencía, Campillo de Mencía and "
                          "Peñalba de Alcorna; the nodes there restarted when power came back."],
          ["12 to 14 Dec 2027", "The mobile operator moved the comarca to its new network. Links down from 08:00 on 12 "
                                "December to 02:00 on 14 December. On reconnecting each node sent its buffer again (OZN-A "
                                "keeps 24 hours, OZN-B 48 hours)."],
          ["6 Jan 2028", "OZ19: head fault at 14:00; unit taken down on 8 January."],
          ["9 Jan 2028", "OZ19: spare unit (OZN-A, head H41950, firmware 4.2, set on the bench in December) up at "
                         "11:00. It reported as OZ19B until the register entry was moved on 25 January at 10:00."],
          ["10 to 19 Jan 2028", "Firmware 4.2 sent to every node (dates below)."],
          ["15 to 16 Mar 2028", "Cleaning round. OZ14 and OZ30 moved to new roofs in their municipalities (the "
                                "register gives the new sites); both were down 08:00 to 11:00 for the move."]]
    s.append(_grid(ev, [32 * mm, 138 * mm], cell))
    s.append(Paragraph("Firmware 4.2", h2))
    fw = [["Node", "Firmware 4.2 from (local, 10:00)"] * 3]
    codes = list(N.CODES)
    for k in range(0, 36, 3):
        r = []
        for c in codes[k:k + 3]:
            r += [c, "on 4.2 (the spare)" if c == N.REPLACED[0] else N.FW_DATES[c].strftime("%d %b %Y")]
        fw.append(r)
    s.append(_grid(fw, [16 * mm, 40 * mm] * 3, cell))
    d = _doc(path, "Maintenance log, low-cost ozone network", P.CENTRE, "Maintenance log")
    _build(d, s, "%s - maintenance log - 18 May 2028" % P.CENTRE_SHORT)
    postprocess.scrub(path, P.CENTRE, "2028-05-18")


# ------------------------------------------------------------------ the vendor's firmware note (pdf)
def firmware(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("OZN firmware 4.2 release note", h1),
         Paragraph("%s, December 2027. For OZN-A and OZN-B nodes on firmware 3.7." % P.VENDOR, small), Spacer(1, 4)]
    sec = [("What changes", [
        "4.2 adds humidity compensation for the tungsten oxide head. When the relative humidity at the head is above "
        "85 per cent the node corrects its reading for the head's humidity response and sends the record as "
        "humidity-compensated.",
        "Records carry these status codes:"])]
    _sections(s, sec, body, h2)
    rows = [["Status", "Meaning"],
            ["0", "accepted"],
            ["1", "accepted, humidity-compensated"],
            ["2", "warm-up: the first two hours after a restart, while the head heats; the reading is low"],
            ["3", "head fault: no reading"]]
    s.append(_grid(rows, [16 * mm, 144 * mm], cell))
    _sections(s, [("Installing", [
        "The node downloads 4.2 over the mobile network and installs it at once. It then restarts, so its first two "
        "hours on 4.2 are warm-up."]),
        ("Unchanged", [
            "The weekly restart at 03:00 local time on Sundays, the record intervals (OZN-A one hour, OZN-B 30 "
            "minutes), the units (ppb) and the time stamps (start of the interval, UTC)."])], body, h2)
    d = _doc(path, "OZN firmware 4.2 release note", P.VENDOR, "Release note")
    _build(d, s, "%s - OZN firmware 4.2" % P.VENDOR)
    postprocess.scrub(path, P.VENDOR, "2027-12-14")


# ------------------------------------------------------------------ the head datasheet (pdf, distractor)
def datasheet(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("OZN-A and OZN-B ozone nodes: datasheet", h1),
         Paragraph("%s, revision C, 2027." % P.VENDOR, small), Spacer(1, 4)]
    rows = [["", "OZN-A", "OZN-B"],
            ["Head", "tungsten oxide, heated", "tungsten oxide, heated"],
            ["Range", "0 to 250 ppb", "0 to 250 ppb"],
            ["Resolution", "0.1 ppb", "0.1 ppb"],
            ["Noise (1 hour, zero air)", "below 3 ppb", "below 3 ppb"],
            ["Response time (t90)", "90 s", "60 s"],
            ["Temperature range", "-10 to 45 °C", "-10 to 45 °C"],
            ["Relative humidity effect (uncompensated)", "up to 6 per cent of reading above 80 per cent", "up to 6 per cent of reading above 80 per cent"],
            ["Record interval", "60 min", "30 min"],
            ["Buffer when the link is down", "24 hours", "48 hours"],
            ["Power", "mains, 4 W", "mains, 5 W"]]
    s.append(_grid(rows, [62 * mm, 54 * mm, 54 * mm], cell))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Heads age in service and their response changes with use; the maker recommends a reference "
                       "check at least twice a year.", body))
    d = _doc(path, "OZN datasheet", P.VENDOR, "Datasheet")
    _build(d, s, "%s - OZN datasheet rev C" % P.VENDOR)
    postprocess.scrub(path, P.VENDOR, "2027-06-02")


# ------------------------------------------------------------------ the contractor's March visit sheets (xlsx)
def visits(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Visitas marzo 2028"
    head = ["Node", "Date", "Arrived (local)", "Left (local)", "Work done", "Technician"]
    ws.append(head)
    for c in head:
        pass
    for i, (code, town, _, _) in enumerate(N.NODES):
        day = dt.date(2028, 3, 13) + dt.timedelta(days=i // 9)
        if code in N.MOVES:
            day = N.MOVES[code][2]
        rv = __import__("numpy").random.default_rng(700 + i)
        a = dt.datetime.combine(day, dt.time(8, 0)) + dt.timedelta(minutes=int(52 * (i % 9) + rv.integers(-9, 14)))
        work = "inlet cleaned; filter changed"
        if code in N.MOVES:
            a = dt.datetime.combine(day, dt.time(8, 0))
            work = "moved to new roof (see register); inlet cleaned; filter changed"
            b = dt.datetime.combine(day, dt.time(11, 0))
        else:
            b = a + dt.timedelta(minutes=int(rv.integers(22, 48)))
        ws.append([code, day.strftime("%d/%m/%Y"), a.strftime("%H:%M"), b.strftime("%H:%M"), work,
                   "A. Ruano" if i % 2 == 0 else "J. Pedraza"])
    for k, w in enumerate([9, 12, 15, 13, 58, 13]):
        ws.column_dimensions[get_column_letter(k + 1)].width = w
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"
    wb.save(path)
    postprocess.scrub(path, P.CONTRACTOR, "2028-03-20")
    postprocess.finish_office(path, "2028-03-17T15:02:00Z", "2028-03-20T08:41:00Z", P.CONTRACTOR)


# ------------------------------------------------------------------ the dictionary and the folder contents (md)
def dictionary(F):
    return f"""# Data dictionary

The ozone network's data folder, {P.CENTRE} ({P.CENTRE_SHORT}).

## {F['nodes']}

The centre's export of every record its 36 nodes sent, from each node's installation to 31 May 2028. One row per record
received.

| Column | Meaning |
|---|---|
| node_id | the node, as the node reported itself |
| reading_start_utc | start of the record's interval, UTC (OZN-A records cover an hour, OZN-B records 30 minutes) |
| o3_ppb | ozone, parts per billion, as the node reported it; blank when the node sent no reading |
| status | the node's status code for the record (below) |
| received_utc | when the record reached the centre, UTC |

Status codes: 0 accepted; 1 accepted, humidity-compensated; 2 warm-up after a restart; 3 head fault.

## {F['register']}

One row per node in service on 31 May 2028: its municipality, site code, mounting, position (WGS84), installation
date, model and head serial. A node moved to another roof carries its current site.

## {F['validated']} and {F['provisional']}

The regional network's hourly ozone for its four analysers in the comarca ({P.NETWORK}). The validated release covers
2026 and 2027; the provisional release runs from 1 December 2027 to 31 May 2028. One row per station, analyser and
hour.

| Column | Meaning |
|---|---|
| fecha | date, dd/mm/yyyy |
| hora | hour ending, 1 to 24, UTC+1 |
| estacion | station code |
| o3_ugm3 | ozone, micrograms per cubic metre at 20 degrees C |
| validacion | V validated, P provisional, N not valid |
| analizador | the analyser's serial |

## {F['weather']}

Weather at Alcorna - Parque de la Dehesa (ES4101A), October 2027 to May 2028: fecha and hora as above, air temperature
(temperatura, degrees C), relative humidity (humedad, per cent), wind speed (vel_viento, m/s) and direction (dir_viento,
degrees).

## Documents

{F['plan']}: the network's quality assurance plan, version 3. {F['stations']}: the regional network's station sheet for its
ozone analysers. {F['log']}: the maintenance log. {F['firmware']}: the vendor's note for firmware 4.2.
{F['datasheet']}: the vendor's datasheet for the two node models. {F['visits']}: the contractor's visit sheets for the
March 2028 round (local times). {F['request']}: the request for the June round's list.
"""


def contents(F):
    rows = [
        (F["request"], "the coordinator's request, forwarding the contractor's note", "1 June 2028"),
        (F["plan"], "quality assurance plan for the low-cost ozone network, v3", "January 2028"),
        (F["nodes"], "the centre's export of every node record received", "to 31 May 2028 23:00 UTC"),
        (F["register"], "the node register", "31 May 2028"),
        (F["log"], "maintenance log, September 2027 to May 2028", "18 May 2028"),
        (F["firmware"], "the vendor's release note for firmware 4.2", "December 2027"),
        (F["datasheet"], "the vendor's datasheet for OZN-A and OZN-B", "2027"),
        (F["visits"], "the contractor's visit sheets for the March 2028 round", "20 March 2028"),
        (F["stations"], "the regional network's station sheet for its ozone analysers", "15 April 2028"),
        (F["validated"], "the regional network's validated hourly ozone, 2026 and 2027", "15 April 2028"),
        (F["provisional"], "the regional network's provisional hourly ozone, December 2027 to May 2028", "31 May 2028"),
        (F["weather"], "weather at Alcorna - Parque de la Dehesa", "31 May 2028"),
        (F["dict"], "this folder's data dictionary", "1 June 2028"),
    ]
    out = ["# Folder contents", "", "The June 2028 round. Every file is the centre's, its contractor's, the vendor's or the "
           "regional network's own; the regional network's data are published under CC BY 4.0, the rest are internal.",
           "", "| File | What it is | As of |", "|---|---|---|"]
    out += ["| %s | %s | %s |" % r for r in rows]
    return "\n".join(out) + "\n"
