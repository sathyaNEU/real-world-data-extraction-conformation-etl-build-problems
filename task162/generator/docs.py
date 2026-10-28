"""task162 documents: Lynmere's leakage assessment method LW-LA-04 (with Table C2 and the zone balance in section 8),
the outcome contract's Schedule 4 for Phase 3, the planning note for the 2027-28 delivery plan, Coldbeck's Phase 3 valve
schedule and the Thornholme outlet meter's calibration certificate. Their text is data here so checks.py and verify.py
can quote and execute it."""
from __future__ import annotations

import datetime as dt
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5a6470")
ACCENT = colors.HexColor("#1f5a7a")
RULE = colors.HexColor("#b8c1c9")
HEAD = colors.HexColor("#e5edf2")

F_METHOD = "LW-LA-04_DMA_leakage_assessment_method.pdf"
F_SCHEDULE = "outcome_contract_schedule_4_phase3.pdf"
F_NOTE = "2027-28_planning_assumptions.eml"
F_VALVES = "phase3_prv_schedule_rev_C.xlsx"
F_CERT = "TH-OUT-0417_calibration_certificate.pdf"


# ------------------------------------------------------------------------------------------------- LW-LA-04
METHOD_TITLE = "District metered area leakage assessment method"
METHOD_REF = "LW-LA-04 issue 6"
METHOD = [
    ("1 Scope", [
        "This method sets how Lynmere Water assesses the leakage of each district metered area (district) from its "
        "inlet meters and pressure loggers, month by month and for the year (1 April to 31 March). It is the "
        "measure the leakage outcome contracts are paid on. Section 8 sets the top-down balance for a supply zone."]),
    ("2 Records", [
        "The assessment reads the hourly means the zone's loggers return to the telemetry archive. Times are "
        "Greenwich Mean Time throughout the year, the loggers' own clock; each hourly mean is stamped with the start "
        "of its hour. A district's inflow in an hour is the sum of its inlet meters' flows in that hour. Its inlet "
        "pressure is the pressure at its principal inlet and its average zone pressure the pressure at its average "
        "zone point, each in metres head.",
        "Logger makes report pressure in their own unit; the logger register gives each serial's make, unit and "
        "dates in service. A pressure of 1 bar is 10.197 metres head."]),
    ("3 The night hour", [
        "The night hour is 03:00 to 04:00 GMT, the hourly mean stamped 03:00. The minimum night flow is the "
        "district's inflow in the night hour and the average zone night pressure (AZNP) its average zone pressure in "
        "the night hour."]),
    ("4 Night use allowance", [
        "Legitimate night use is allowed at 1.7 litres an hour for each dwelling connected to the district that day "
        "and 8.0 litres an hour for each non-household property connected to the district that day. The net night flow "
        "is the minimum night flow less the allowance, in litres a second."]),
    ("5 Valid days", [
        "A day counts when the district's inlet and average zone point loggers each return all 24 hourly means and "
        "the district was closed all day, every boundary valve shut so that its inlet meters carried its whole "
        "supply. Other days are left out of the month."]),
    ("6 The day's leakage, the month and the year", [
        "The night-day factor of a day is the sum over its 24 hourly means of the average zone pressure divided by "
        "that day's AZNP, each ratio raised to the district's N1 (Table C2); it is in hours. The day's leakage is "
        "the net night flow times 3.6 times the night-day factor, in cubic metres a day, reported in megalitres a "
        "day.",
        "A month's leakage is the mean of its valid days. The year's leakage is the mean of its twelve months. A "
        "group of districts is the sum of its districts."]),
    ("7 N1", [
        "N1 is the district's leakage exponent from Lynmere's 2023 step tests, in Table C2. It applies to the night-"
        "day factor and to any change in a district's leakage with its pressure."]),
    ("8 The zone's balance (top-down)", [
        "The system input of a zone is the volume through its reservoir outlet meter, corrected by the meter's "
        "calibration certificates for the readings before each calibration. Billed metered and billed unmetered "
        "consumption are the volumes billed to the zone's customers, each bill apportioned to the year by days. The "
        "zone's customers are the properties in its districts and the trunk main's direct supplies (code NZ-TM in "
        "the property system).",
        "Unbilled authorised use is 0.4 per cent of system input. Apparent losses are customer meter "
        "under-registration at 2.5 per cent of billed metered consumption and unauthorised use at 0.3 per cent of "
        "system input. Real losses are the system input less billed metered and billed unmetered consumption, "
        "unbilled authorised use and apparent losses. Each component is reported in megalitres a day over the "
        "year's days."]),
]


def method_sentences():
    return [s for _, paras in METHOD for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ------------------------------------------------------------------------------------------------- Schedule 4
SCHEDULE_TITLE = "Schedule 4: Performance, Phase 3 (Northern zone pressure management)"
SCHEDULE = [
    ("4.1 Districts", [
        "Phase 3 covers the 22 district metered areas listed in Table 4.1, at the Brackenby end of the Thornholme to "
        "Brackenby trunk main, each fitted with a pressure reducing valve at its inlet by 31 March 2027."]),
    ("4.2 Measure", [
        "The Phase 3 reduction is the Phase 3 districts' leakage in the 2025-26 assessment year less their leakage "
        "in the 2027-28 assessment year (1 April 2027 to 31 March 2028), each assessed by method LW-LA-04 issue 6 "
        "and each the sum of the districts' annual figures. The 2025-26 figures are those in Lynmere's assessment "
        "export of 14 May 2026."]),
    ("4.3 Target", [
        "The Phase 3 target reduction is 0.48 Ml/d."]),
    ("4.4 Shortfall", [
        "Where the Partner's delivery plan forecasts a Phase 3 reduction under the target, the plan instructs "
        "find-and-fix in the Phase 3 districts for 2027-28 to make up the shortfall, at 0.05 Ml/d of sustained "
        "reduction for each find-and-fix gang-year, rounded up to whole gang-years. The 2027-28 delivery plan is "
        "due to Lynmere by 30 November 2026."]),
]


def schedule_sentences():
    return [s for _, paras in SCHEDULE for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ------------------------------------------------------------------------------------------------- the planning note
NOTE_SUBJECT = "2027-28 delivery plan: planning assumptions"
NOTE_DATE = dt.datetime(2026, 10, 19, 14, 6)
NOTE_BODY = [
    "Emily,",
    "For the 2027-28 delivery plan please take each Phase 3 district's demand and pressures in each month of "
    "2027-28 as they were recorded in the same month of 2025-26, the year of the assessment export, with no growth. "
    "The valves are in service for the whole of 2027-28 at the settings in Annette's Phase 3 schedule (rev C).",
    "Louis has sent the 2025-26 telemetry extract for the whole zone and the assessment export for the Phase 3 "
    "districts. The property and billing extracts are the North region's as at 2 November.",
    "Thanks,",
    "",
    "Clive Heath",
    "Contract Manager, Leakage Outcome Contracts",
    "Lynmere Water",
]


def note_sentences():
    return [s for p in NOTE_BODY for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ------------------------------------------------------------------------------------------------- the valve schedule
VALVE_BASIS = ("Fixed-outlet pressure reducing valves at each district's principal inlet. Settings hold 20 m at the "
               "district's critical point at its design peak hour (the 2025-26 peak hour flow grown to the 2035 "
               "demand, with an 8 l/s fire flow drawn at the critical point). Settings are metres head at the valve "
               "outlet, the point the district's inlet logger reads. Each valve is sized to pass its district's peak "
               "hour flow with under 0.1 m head loss.")
VALVE_COLS = ["District", "Name", "Valve", "Type", "Outlet setting (m)", "AZNP 2025-26 (m)",
              "AZNP after commissioning (m)", "Commissioning week"]

CERT_TEXT = [
    "Instrument: electromagnetic flow meter TH-OUT-0417, DN600, Thornholme service reservoir outlet.",
    "Calibration date: 12 November 2025. Method: in-situ verification against a clamp-on reference over 72 hours.",
    "As found: reading 1.4 per cent low across the flow range. As left: within 0.5 per cent after re-zeroing and "
    "coil re-calibration.",
    "Readings from the last calibration (9 October 2024) to this one should be corrected for the as-found error.",
]


# ------------------------------------------------------------------------------------------------- PDF writing
def _styles():
    return dict(
        title=ParagraphStyle("t", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4),
        sub=ParagraphStyle("s", fontName="LibSans", fontSize=9, leading=12, textColor=GREY, spaceAfter=10),
        h=ParagraphStyle("h", fontName="LibSans-Bold", fontSize=10.5, leading=14, textColor=ACCENT, spaceBefore=8,
                         spaceAfter=3),
        p=ParagraphStyle("p", fontName="LibSans", fontSize=9.5, leading=13.2, textColor=INK, spaceAfter=5),
        cell=ParagraphStyle("c", fontName="LibSans", fontSize=8.5, leading=10.5, textColor=INK),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("LibSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(2 * cm, 1.2 * cm, text)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths):
    st = _styles()
    data = [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def write_method(path, n1_rows):
    st = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, title=METHOD_TITLE, author=K.PEOPLE["leakage"],
                            subject="", creator="", producer="")
    flow = [Paragraph("Lynmere Water", st["sub"]), Paragraph(METHOD_TITLE, st["title"]),
            Paragraph("%s, effective 1 April 2025. Owner: %s, Leakage Analysis." % (METHOD_REF, K.PEOPLE["leakage"]),
                      st["sub"])]
    for head, paras in METHOD:
        flow.append(Paragraph(head, st["h"]))
        for p in paras:
            flow.append(Paragraph(p, st["p"]))
        if head.startswith("7"):
            flow.append(Spacer(1, 4))
            flow.append(Paragraph("Table C2. N1 by district", st["cell"]))
            rows = [["District", "Name", "N1", "District", "Name", "N1"]]
            half = (len(n1_rows) + 1) // 2
            for i in range(half):
                a = n1_rows[i]
                b = n1_rows[i + half] if i + half < len(n1_rows) else ["", "", ""]
                rows.append([a[0], a[1], "%.2f" % a[2], b[0], b[1], ("%.2f" % b[2]) if b[0] else ""])
            flow.append(_table(rows, [1.6 * cm, 3.9 * cm, 1.2 * cm, 1.6 * cm, 3.9 * cm, 1.2 * cm]))
    doc.build(flow, onFirstPage=_footer("%s  |  Uncontrolled when printed" % METHOD_REF),
              onLaterPages=_footer("%s  |  Uncontrolled when printed" % METHOD_REF))


def write_schedule(path, districts):
    st = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, title=SCHEDULE_TITLE, author=K.PEOPLE["contract"],
                            subject="", creator="", producer="")
    flow = [Paragraph("Leakage Outcome Contract LW/LOC/2024/07 between Lynmere Water and Coldbeck Network Partners Ltd",
                      st["sub"]), Paragraph(SCHEDULE_TITLE, st["title"]),
            Paragraph("Variation 3, signed 2 September 2026", st["sub"])]
    for head, paras in SCHEDULE:
        flow.append(Paragraph(head, st["h"]))
        for p in paras:
            flow.append(Paragraph(p, st["p"]))
        if head.startswith("4.1"):
            rows = [["District", "Name", "District", "Name"]]
            half = (len(districts) + 1) // 2
            for i in range(half):
                b = districts[i + half] if i + half < len(districts) else ("", "")
                rows.append([districts[i][0], districts[i][1], b[0], b[1]])
            flow.append(Paragraph("Table 4.1. Phase 3 districts", st["cell"]))
            flow.append(_table(rows, [1.8 * cm, 5.2 * cm, 1.8 * cm, 5.2 * cm]))
    doc.build(flow, onFirstPage=_footer("LW/LOC/2024/07 Schedule 4 (Variation 3)"),
              onLaterPages=_footer("LW/LOC/2024/07 Schedule 4 (Variation 3)"))


def write_certificate(path):
    st = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm, title="Calibration certificate TH-OUT-0417", author="Fenwold Flow Services",
                            subject="", creator="", producer="")
    flow = [Paragraph("Fenwold Flow Services Ltd", st["sub"]), Paragraph("Certificate of verification FFS-25-1182",
                                                                         st["title"]),
            Paragraph("Customer: Lynmere Water, Northern zone operations", st["sub"])]
    for line in CERT_TEXT:
        flow.append(Paragraph(line, st["p"]))
    flow.append(Spacer(1, 8))
    flow.append(_table([["Test point", "Reference (l/s)", "Meter (l/s)", "Error"],
                        ["Low", "112.40", "110.82", "-1.41%"], ["Mid", "236.90", "233.58", "-1.40%"],
                        ["High", "389.10", "383.69", "-1.39%"]], [3.5 * cm, 3.5 * cm, 3.5 * cm, 3 * cm]))
    doc.build(flow, onFirstPage=_footer("FFS-25-1182"), onLaterPages=_footer("FFS-25-1182"))


def write_note(path):
    frm = "%s <%s>" % (K.PEOPLE["contract"], K.addr(K.PEOPLE["contract"]))
    to = "%s <%s>" % (K.PEOPLE["delivery"], K.addr(K.PEOPLE["delivery"], K.CB_DOMAIN))
    cc = "%s <%s>" % (K.PEOPLE["leakage"], K.addr(K.PEOPLE["leakage"]))
    body = "\r\n".join(NOTE_BODY) + "\r\n"
    hdr = ["Message-ID: <%s.%s@%s>" % (K.token("note", n=12), K.token("note2", n=6), K.LW_DOMAIN),
           "Date: Mon, 19 Oct 2026 14:06:41 +0100",
           "From: %s" % frm, "To: %s" % to, "Cc: %s" % cc, "Subject: %s" % NOTE_SUBJECT,
           "MIME-Version: 1.0", "Content-Type: text/plain; charset=\"utf-8\"", "Content-Transfer-Encoding: 8bit", ""]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(hdr) + "\r\n" + body)
