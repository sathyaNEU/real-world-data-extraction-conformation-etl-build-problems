"""The pack's documents: the society's standard OM-07, Schedule 3 of the turbine supply agreement (the warranted
power curve) and the asset manager's extract notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W      # noqa: E402

STANDARD = "OM-07_blade_campaigns_and_lost_production.pdf"
SCHEDULE = "TSA_schedule_3_warranted_power_curve.pdf"
NOTES = "extract_notes_2026-10-09.txt"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY = colors.HexColor("#1d2a24"), colors.HexColor("#5a6660")

BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("c", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=14, leading=18, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=8, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.2, leading=10.6, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.4, leading=10.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
SBODY = ParagraphStyle("sb", fontName="Serif", fontSize=10.0, leading=13.4, textColor=INK, spaceAfter=5)
SH1 = ParagraphStyle("sh1", fontName="Serif-B", fontSize=13, leading=17, textColor=INK, spaceAfter=3)
SMETA = ParagraphStyle("smeta", fontName="Serif", fontSize=8.6, leading=11, textColor=GREY, spaceAfter=8)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                             bottomMargin=19 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot, font="Sans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.8)
        canvas.drawString(22 * mm, A4[1] - 11 * mm, top_left)
        canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 11 * mm, top_right)
        canvas.setFont(font, 7.2)
        canvas.drawString(22 * mm, 10 * mm, foot)
        canvas.drawRightString(A4[0] - 22 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


STANDARD_CLAUSES = [
    ("1  Purpose and scope", [
        ("1.1", "This standard sets how the society chooses the turbine for its yearly leading-edge repair campaign, and "
                "how the asset manager accounts to the board for the farm's lost production."),
        ("1.2", "It applies to the ten Hallvard H93-2.3 turbines of Cairnhollow Community Wind Farm, CH01 to CH10."),
    ]),
    ("2  The yearly leading-edge campaign", [
        ("2.1", "The society runs one leading-edge repair campaign each summer: its rope-access contractor repairs the "
                "leading edges of the three blades of one turbine in the June to August weather window."),
        ("2.2", "The board books the campaign at its November meeting, on a paper from the asset manager naming the "
                "turbine and the energy the repair is expected to recover over the twelve months after the work."),
        ("2.3", "The campaign goes to the turbine whose repaired blades would add the most energy."),
        ("2.4", "A campaign is valued on the turbine's last twelve months of normal operation: the energy the turbine "
                "would have produced in those intervals, in the same winds, had its blades been as new, less the "
                "energy it produced."),
        ("2.5", "Where the blade set now on a turbine went up within those twelve months, the value is taken on that "
                "blade set's own months on the turbine."),
        ("2.6", "The last twelve months are the twelve calendar months to the end of the September before the "
                "board's November meeting."),
    ]),
    ("3  Normal operation", [
        ("3.1", "A ten-minute interval is in normal operation when the turbine's controller state for the interval is "
                "10 (running) or 20 (ready, wind below cut-in)."),
    ]),
    ("4  Lost production", [
        ("4.1", "Each November the asset manager reports to the board each turbine's lost production over the same "
                "twelve months to downtime and to grid curtailment."),
        ("4.2", "Downtime is time a turbine is stopped by a fault, for repair, or for planned service."),
        ("4.3", "Grid curtailment is time in which an instruction of the network operator under the farm's active "
                "network management (ANM) agreement is in force: an export limit or a trip."),
        ("4.4", "An interval of downtime counts as downtime whatever else applied in it. An interval in which the "
                "turbine was stopped for ice, for high wind or by a loss of the grid is neither downtime nor grid "
                "curtailment. Any other interval in which an ANM instruction was in force is grid curtailment."),
        ("4.5", "The lost production in an interval of downtime or grid curtailment is the turbine's potential power "
                "less its mean power in the interval, over the interval's ten minutes, and is taken as zero where that "
                "difference is negative."),
        ("4.6", "The potential power is the warranted power of Schedule 3 to the turbine supply agreement at the met "
                "mast's 80 m wind speed for the interval, corrected to standard air density as v x (rho / 1.225)^(1/3), "
                "with rho = p / (287.05 T) from the mast's pressure p in pascals and temperature T in kelvin. The "
                "warranted power is interpolated linearly between the listed wind speeds and is zero below 3.0 m/s and "
                "above 25.0 m/s."),
        ("4.7", "Losses are reported by turbine in MWh."),
    ]),
    ("5  Records", [
        ("5.1", "The asset manager works from the SCADA's ten-minute records, the met mast's record, the network "
                "operator's ANM log, the service contractor's work orders and the turbines' energy meters, and keeps "
                "them for six years."),
    ]),
]


def write_standard(path):
    who, role = W.PEOPLE["secretary"]
    title = "Blade leading-edge campaigns and lost production"
    doc = _doc(path, title, who)
    s = [Paragraph(W.SOCIETY.upper() + " · OPERATIONS AND MAINTENANCE STANDARDS", META),
         Paragraph("OM-07  " + title, H1),
         Paragraph("Revision 3, approved by the Board on 14 May 2026. Owner: %s. Issued by %s, %s." % (
             W.PEOPLE["asset_manager"][1], who, role), META)]
    for head, items in STANDARD_CLAUSES:
        s.append(Paragraph(head, H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), CLAUSE))
    s.append(Spacer(1, 8))
    rows = [[Paragraph(x, CELLB) for x in ("Revision", "Approved", "Change")],
            [Paragraph(x, CELL) for x in ("1", "14 September 2017", "First issue")],
            [Paragraph(x, CELL) for x in ("2", "9 May 2023", "Lost production potential power taken from the met mast")],
            [Paragraph(x, CELL) for x in ("3", "14 May 2026", "Lost production by cause rewritten; campaign valuation "
                                                               "clarified")]]
    t = Table(rows, colWidths=[22 * mm, 34 * mm, 104 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    s.append(t)
    foot = W.SOCIETY + " | OM-07 | revision 3"
    doc.build(s, onFirstPage=_frame(W.FARM, "OM-07 rev. 3", foot), onLaterPages=_frame(W.FARM, "OM-07 rev. 3", foot))


def write_schedule(path, curve):
    speeds, kw, cp = curve
    title = "Schedule 3: Warranted power curve"
    doc = _doc(path, title, "")
    head = [Paragraph(x, CELLB) for x in ("Wind speed (m/s)", "Electrical power (kW)", "Power coefficient Cp")]
    body = [[Paragraph("%.1f" % v, CELLR), Paragraph("%d" % p, CELLR), Paragraph("%.3f" % c, CELLR)]
            for v, p, c in zip(speeds, kw, cp)]
    half = (len(body) + 1) // 2
    left, right = body[:half], body[half:] + [[Paragraph("", CELL)] * 3] * (half - len(body[half:]))
    rows = [head + head] + [a + b for a, b in zip(left, right)]
    t = Table(rows, colWidths=[24 * mm, 28 * mm, 28 * mm] * 2, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEAFTER", (2, 0), (2, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]))
    s = [Paragraph("TURBINE SUPPLY AGREEMENT · CAIRNHOLLOW COMMUNITY WIND FARM · HALLVARD H93-2.3", SMETA),
         Paragraph(title, SH1),
         Paragraph("Between Cairnhollow Community Energy and Hallvard Wind Systems UK Ltd, dated 3 March 2014.", SMETA),
         Paragraph("1&nbsp;&nbsp;&nbsp;The warranted power curve below gives the turbine's electrical power at its low-voltage "
                   "terminals against the ten-minute mean wind speed at hub height (80 m), at the standard air density "
                   "of 1.225 kg/m<super>3</super>, for the Hallvard H93-2.3 with the HB45.2 blade.", SBODY),
         Paragraph("2&nbsp;&nbsp;&nbsp;It is the curve against which the power performance warranty of Schedule 7 is "
                   "assessed. Cut-in wind speed 3.0 m/s; cut-out 25.0 m/s; restart below 20.0 m/s.", SBODY),
         Spacer(1, 6), t, Spacer(1, 8),
         Paragraph("Cp is the electrical power over the power in the wind through the rotor (93.0 m diameter) at 1.225 "
                   "kg/m<super>3</super>.", SMETA)]
    foot = "Turbine Supply Agreement | Schedule 3"
    doc.build(s, onFirstPage=_frame("Hallvard H93-2.3", "Schedule 3", foot, "Serif"),
              onLaterPages=_frame("Hallvard H93-2.3", "Schedule 3", foot, "Serif"))


NOTES_TEXT = """Cairnhollow Community Wind Farm: data for the 2027 campaign paper and the 2025-26 lost production report
Extracted 9 October 2026 by {am} (asset manager).

Files
{scada}
  The SCADA's ten-minute records for CH01 to CH10, October 2025 to September 2026. One row per turbine and interval,
  timestamped at the end of the interval. The SCADA moved from the site server to the provider's hosted platform on
  3 February 2026; this file joins the server archive to the platform's export.
  wind_speed_mean: nacelle anemometer, ten-minute mean, m/s (nacelle transfer function applied by the controller)
  wind_speed_sd: standard deviation of the nacelle anemometer's one-second readings over the interval, m/s
  nacelle_position: degrees from north
  active_power_mean: kW at the turbine's low-voltage terminals
  ambient_temperature: nacelle sensor, deg C
  state: controller state (see {states})
{mast}
  Met mast M1 logger. TIMESTAMP_UTC is the start of the ten-minute interval. Cup anemometer at 80 m (m/s), vane at
  78 m (degrees from north), temperature (deg C), pressure (hPa) and relative humidity (%) at 76 m.
{anm}
  Morvenside Networks' log of ANM instructions to our connection (Glenrigg zone). Times UTC; an instruction is in
  force from start_utc to end_utc; export_limit_mw is the limit at our connection, 0 for a trip.
{states}
  Hallvard's controller state codes.
{lifts}
  Brackwater Cranes' lift log for the site in 2026. Pads as on the site layout.
{layout}
  Pads, turbines and the met mast on the site grid (metres east and north of the site datum).
{register}
  Turbine register.
{counters}
  Each turbine's energy meter, read at local midnight on the first of each month.
{orders}
  Hallvard Service UK's work orders for the twelve months. Times are local (UK) clock times.
{standard}
  Our O&M standard (revision 3).
{schedule}
  The warranted power curve from the turbine supply agreement.
{meter}
  Export meter at the 33 kV connection, half-hourly settlement data (kWh, UTC periods), from the supplier's portal.
{prior}
  Last year's lost production report to the board.
"""


def write_notes(path, names):
    open(path, "w").write(NOTES_TEXT.format(am=W.PEOPLE["asset_manager"][0], standard=STANDARD, schedule=SCHEDULE,
                                            **names))
