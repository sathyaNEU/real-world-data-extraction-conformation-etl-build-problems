"""The pack's documents: SOP 2.10 (call answering and answer-time reporting) and the FY2028 recommended budget's
communications floor page (PDF), the README with its field notes. Their text is kept here as data so checks.py can
quote and execute it."""
from __future__ import annotations

import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"),
               ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d232b")
GREY = colors.HexColor("#5d6672")
RED = colors.HexColor("#8a1c1c")       # the agency's maroon
BLUE = colors.HexColor("#22436b")      # the county budget office's blue

BODY = ParagraphStyle("body", fontName="Carlito", fontSize=10.5, leading=14.0, textColor=INK, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Carlito-Bold", fontSize=15.0, leading=19, textColor=RED, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName="Carlito", fontSize=9.2, leading=12.0, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="Carlito-Bold", fontSize=11.2, leading=14.5, textColor=RED, spaceBefore=8, spaceAfter=3)
B_BODY = ParagraphStyle("bb", fontName="LibSans", fontSize=9.6, leading=12.8, textColor=INK, spaceAfter=5)
B_H1 = ParagraphStyle("bh1", fontName="LibSans-Bold", fontSize=13.0, leading=16.5, textColor=BLUE, spaceAfter=2)
B_H1S = ParagraphStyle("bh1s", fontName="LibSans", fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=9)
B_H2 = ParagraphStyle("bh2", fontName="LibSans-Bold", fontSize=10.2, leading=13.0, textColor=BLUE, spaceBefore=7,
                      spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LibSans", fontSize=8.6, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LibSans-Bold", fontSize=8.6, leading=10.6, textColor=INK)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                             topMargin=0.85 * inch, bottomMargin=0.85 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(left, right, font="Carlito"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.5 * inch, left)
        canvas.drawRightString(letter[0] - 1.0 * inch, 0.5 * inch, "%s%s" % (right, doc.page))
        canvas.restoreState()
    return draw


# ---------------------------------------------------------------------------------------------------- SOP 2.10
F_SOP = "sop_2-10_call_handling_standard_and_reporting.pdf"
SOP = [
    ("1", "Purpose and scope", "scope", [
        "1.1 This procedure sets the agency's 911 call-answering standard and how answer-time compliance is measured, "
        "reported and planned for. It applies to every call-taking position on the 911 floor.",
        "1.2 The agency's fiscal year runs from 1 July to 30 June; fiscal 2026 is the year from 1 July 2025 to "
        "30 June 2026, its quarters starting on 1 July, 1 October, 1 January and 1 April. The days, months, quarters "
        "and years the agency reports are local (Central) calendar dates."]),
    ("2", "The standard", "standard", [
        "2.1 Ninety per cent of 911 calls presented to the agency are answered within 15 seconds.",
        "2.2 The standard covers every 911 call presented to the agency's 911 queue, calls transferred in from other "
        "PSAPs included. Calls on the administrative lines are not 911 calls; neither are test calls."]),
    ("3", "Measurement", "measure", [
        "3.1 A call is presented when it reaches the agency's 911 queue: the i3 queue entry on NG911, or the trunk "
        "seizure on the CAMA trunks before the cutover. It is answered when it is connected to a call-taker's "
        "position.",
        "3.2 A call abandoned within 5 seconds of presentation is treated as a misdial and left out of the measure.",
        "3.3 Answer-time compliance for a period is the number of 911 calls answered within 15 seconds of "
        "presentation divided by the number of 911 calls presented in the period, less the calls abandoned within "
        "5 seconds of presentation."]),
    ("4", "Positions", "positions", [
        "4.1 Call-taking positions run on auto-answer: a call is delivered to a call-taker in Ready and connected with "
        "a tone, and the caller is on the line at once.",
        "4.2 A position takes no new call until the call-taker sets Ready again after the call's after-call work and "
        "CAD entry.",
        "4.3 The floor supervisor and the callback desk do not take calls from the 911 queue."]),
    ("5", "Staffing", "staffing", [
        "5.1 Minimum floor staffing for each block of each fiscal year is planned against the Tri-County Regional 911 "
        "Board's published hourly volume forecast for the agency for that year.",
        "5.2 Floor blocks start at 02:00, 06:00, 10:00, 14:00, 18:00 and 22:00. A block that runs past midnight "
        "belongs to the day it starts."]),
    ("6", "Reporting", "reporting", [
        "6.1 Quality assurance reports compliance monthly, for the floor and for each block. A shift's calls are "
        "reported in the month the shift starts."]),
    ("7", "Abandoned calls", "abandoned", [
        "7.1 Every abandoned 911 call is called back by the callback desk, however briefly the caller held on. The "
        "desk aims to dial each one within two minutes of the hang-up."]),
]


def sop_sentences(key=None):
    out = []
    for _, _, k, paras in SOP:
        if key is None or k == key:
            out += [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9])", p)]
    return out


def write_sop(path):
    s = [Paragraph("%s &middot; Standard Operating Procedure 2.10 &middot; Revision 4" % K.AGENCY, H1S),
         Paragraph("Call answering and answer-time reporting", H1),
         Paragraph("Effective 1 July 2025; supersedes Revision 3 (1 August 2022). Owner: %s, Operations Manager. "
                   "Reviewed each year with the budget." % K.PEOPLE["ops"], H1S)]
    for num, head, _, paras in SOP:
        s.append(Paragraph("%s&nbsp;&nbsp;%s" % (num, head), H2))
        for p in paras:
            s.append(Paragraph(p.replace("&", "&amp;"), BODY))
    doc = _doc(path, "SOP 2.10 Call answering and answer-time reporting", K.PEOPLE["ops"])
    f = _footer("%s  |  SOP 2.10 Rev. 4  |  Internal" % K.AGENCY_SHORT, "Page ")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the budget page
F_BUDGET = "fy2028_recommended_budget_communications_floor.pdf"
BUDGET_ROWS = [
    ("02:00 to 06:00", "3", "3", ""),
    ("06:00 to 10:00", "4", "4", ""),
    ("10:00 to 14:00", "6", "6", ""),
    ("14:00 to 18:00", "6", "6", ""),
    ("18:00 to 22:00", "5", "5", ""),
    ("22:00 to 02:00, nights starting Sunday to Thursday", "4", "4", ""),
    ("22:00 to 02:00, nights starting Friday and Saturday", "5", "4",
     "The fifth call-taker is paid by the state 911 surcharge staffing grant, which ends on 30 June 2027."),
]
BUDGET_TEXT = [
    "The recommended budget holds the communications floor at its fiscal 2027 staffing in every block except the "
    "Friday and Saturday late shift, where the grant-funded fifth call-taker ends with the grant. Halvorsen Township's "
    "911 calls come to the agency on 1 July 2027 under the township's new service agreement, which pays the agency "
    "$412,800 a year for call-taking and dispatch.",
    "The board asked for the months of fiscal 2028, if any, in which a seasonal fifth call-taker should cover the "
    "Friday and Saturday late shift. A seasonal call-taker on overtime costs $468 a night, four hours at the "
    "overtime rate with benefits; the operations manager brings the request with the final budget in May 2027.",
]


def write_budget(path):
    s = [Paragraph("Tavish County &middot; FY2028 Recommended Budget &middot; Public Safety", B_H1S),
         Paragraph("%s: communications floor staffing" % K.AGENCY, B_H1),
         Paragraph("Budget office draft for the agency board's work session, 2 October 2026. Prepared by %s, "
                   "Finance Director." % K.PEOPLE["finance"], B_H1S),
         Paragraph("Call-takers on the 911 floor, by block", B_H2)]
    data = [[Paragraph("Block", CELLB), Paragraph("FY2027 adopted", CELLB), Paragraph("FY2028 recommended", CELLB),
             Paragraph("Note", CELLB)]]
    for blk, a, b, note in BUDGET_ROWS:
        data.append([Paragraph(blk, CELL), Paragraph(a, CELL), Paragraph(b, CELL), Paragraph(note, CELL)])
    t = Table(data, colWidths=[2.15 * inch, 0.85 * inch, 1.0 * inch, 2.5 * inch])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa4b0")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6ebf2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    s.append(Spacer(1, 8))
    for p in BUDGET_TEXT:
        s.append(Paragraph(p.replace("&", "&amp;").replace("$", "&#36;"), B_BODY))
    doc = _doc(path, "FY2028 Recommended Budget: communications floor staffing", K.PEOPLE["finance"])
    f = _footer("Tavish County Budget Office  |  FY2028 recommended  |  Draft", "Page ", font="LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- README
F_README = "README.md"


def readme_text(files):
    L = []
    L.append("# Tavish County Emergency Communications Agency: data for the FY2028 late-shift staffing request")
    L.append("")
    L.append("Compiled by Quality Assurance (%s) on 6 October 2026 for the operations manager. Callback numbers in "
             "every export are replaced by a keyed pseudonym (the same number gives the same pseudonym in every file "
             "of this folder); everything else is as the systems wrote it." % K.PEOPLE["qa"])
    L.append("")
    L.append("## Files")
    L.append("")
    for f, d in files:
        L.append("- `%s`: %s" % (f, d))
    L.append("")
    L.append("## Field notes")
    L.append("")
    L.append("**ACD call detail, legacy layout** (`acd_call_detail_legacy_2025-01-01_2025-05-16.csv`). The CAMA and "
             "ALI-era ACD's call detail, one row per call presented to the 911 queue. Times are local (Central) to the "
             "second, `MM/DD/YYYY HH:MM:SS`. `SEIZE_TIME` is the trunk seizure (presentation), `ANS_TIME` the "
             "connection to a position, `REL_TIME` the end of the conversation, `RDY_TIME` the call-taker's "
             "return to Ready, `DISC_TIME` the caller's disconnect on an abandoned call. `CALL_STATUS` is `ANS` "
             "(answered), `ABN` (abandoned before answer) or `TST` (a trunk test answered by the test position). "
             "`CLASS_OF_SVC` codes: `RESD` residence, `BUSN` business, `PBXB` business PBX, `WPH1` and `WPH2` "
             "wireless (Phase I and Phase II), `VOIP`, `TLMA` telematics, `TEST`. `XFER_IN_FROM` and `XFER_OUT_TO` "
             "are the transfer speed-dial codes: `WEXLEY`, `WEX ALT`, `GARRICK`, `GAR ALT`, `SP D6` (State Patrol "
             "District 6), `HOLLIN CR`.")
    L.append("")
    L.append("**i3 call log** (`i3_call_log_2025-05-13_2026-09-30.jsonl`). The NG911 call-handling system's call "
             "records, one JSON object per line per call presented to the 911 queue. Times are UTC with milliseconds. "
             "`presented` is the queue entry; `answered` the connection to a position; `released` the end of the "
             "conversation; `ready` the call-taker's return to Ready; `ended` the caller's disconnect on an abandoned "
             "call. `disposition` is `answered`, `abandoned` or `test-responder` (an ESInet test call answered by the "
             "test responder, not a call-taker). `serviceType` is `wireless`, `fixed`, `voip`, `mlts`, `telematics` or "
             "`test`. `referredBy` is the URI of the PSAP that transferred the call in; `transferTo` and `transferAt` "
             "the URI a call was transferred out to and when. `callId` is the ESInet's Call Identifier and "
             "`incidentId` its Incident Tracking Identifier.")
    L.append("")
    L.append("**Cutover.** Wireless, VoIP and telematics calls moved to NG911 at 06:00 on 13 May 2025; wireline "
             "calls stayed on the CAMA trunks until 06:00 on 16 May 2025. Calls presented between those times are in "
             "one export or the other, never both.")
    L.append("")
    L.append("**Floor roster** (`floor_roster_2025-01_2026-09.csv`). Call-takers on the 911 floor by block, from "
             "the scheduling system. A block that runs past midnight is dated by the day it starts: the `2200-0200` "
             "block of a Friday runs to 02:00 on Saturday.")
    L.append("")
    L.append("**Location records** (`che_location_records_fy2026_northeast.csv`). Every location record the "
             "agency's call-handling systems, on the floor and at the backup centre, stored for wireless 911 calls "
             "presented from 1 July 2025 to 30 June 2026 with any location inside 39.80 to 39.97 N and 88.21 to 87.97 W "
             "(the north-east of the county and the Wexley County line). `method` is `cell` (the serving cell sector's "
             "location delivered with the call; `cell_sector` names the sector), `device` (a handset location from the "
             "device-based hybrid service) or `gnss` (a handset satellite fix, also returned on a rebid). `radius_m` is "
             "the uncertainty radius at `confidence_pct`. `call_id` ties each record to its call in the i3 log. The "
             "agency places a wireless call by the last handset location received for it (`device` or `gnss`).")
    L.append("")
    L.append("**Township boundary** (`halvorsen_township_boundary.geojson`). Tavish County GIS's boundary of "
             "Halvorsen Township, the layer the ESInet's routing uses for the township from 1 July 2027 (WGS84 "
             "longitude and latitude).")
    L.append("")
    L.append("**PSAP directory** (`esinet_psap_directory.csv`). The ESInet's directory of PSAP URIs and the "
             "agencies that answer on them.")
    L.append("")
    L.append("**Callback desk** (`callback_desk_tasks_2026-01_2026-06.csv`). The callback module's tasks created "
             "from 1 January to 30 June 2026, for abandoned 911 calls and abandoned administrative-line calls. Times "
             "are local (Central), `YYYY-MM-DD HH:MM:SS`. `call_ref` is the call that opened the task (the i3 "
             "`callId`, or the administrative line's `call_id`); `callback_number` is the pseudonym of the number "
             "dialled; `first_dial` is the desk's first dial. The desk works one open task per callback number: an "
             "abandon from a number whose task has not been dialled yet joins that task and opens none of its own. A "
             "task closed as `caller called in` was never dialled: the caller got through on a redial first.")
    L.append("")
    L.append("**Other exports.** The CAD incident export and the administrative line's ACD export are as pulled for "
             "the request; the board's forecast workbook is as published, with its own Read me sheet.")
    L.append("")
    return "\n".join(L)
