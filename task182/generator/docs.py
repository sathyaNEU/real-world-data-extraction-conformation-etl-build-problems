"""The pack's documents: MG-02 (the company's procedure for landholder bore assessments and make good) and the
environment team's notes on the network extract."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

MG02 = "MG-02_bore_assessment_and_make_good.pdf"
NOTES = "monitoring_network_notes.md"

INK = colors.HexColor("#1f2a24")
RULE = colors.HexColor("#7f8c84")
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=4.5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#4d5852"))
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")


def _frame(title, ref, issued):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(colors.HexColor("#4d5852"))
        canvas.drawString(18 * mm, A4[1] - 12 * mm, "%s  |  %s" % (W.COMPANY, W.MINE))
        canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 12 * mm, ref)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, A4[1] - 13.6 * mm, A4[0] - 18 * mm, A4[1] - 13.6 * mm)
        canvas.drawString(18 * mm, 11 * mm, "%s  |  %s  |  Uncontrolled when printed" % (title, issued))
        canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("LEFTPADDING", (0, 0), (-1, -1), 3)]))
    return t


MG02_TEXT = [
    ("1", "Purpose and scope", [
        ("1.1", "This procedure sets how %s assesses landholder bores around the mine and makes good a bore whose "
                "capacity has been impaired by the mine's take of associated water." % W.MINE),
        ("1.2", "It applies to the landholder bores in the %s landholder bore register. The other bores in the "
                "monitoring network, the state reference bores and the mine's own monitoring bores, are outside its "
                "scope." % W.MINE),
    ]),
    ("2", "Water levels", [
        ("2.1", "A static level is a water level read with the bore's pump off for at least 12 hours. A reading taken "
                "with the pump running is a pumped level and is not used under this procedure."),
        ("2.2", "A reduced level (m AHD) is the elevation of the measuring point in force on the reading date, less "
                "the depth to water below it."),
        ("2.3", "A logged bore's daily level is the mean of the day's logger readings, each compensated for air "
                "pressure, over the day in Queensland time."),
        ("2.4", "A bore's assessment level is the mean of its static levels in the assessment month: its daily "
                "levels where the bore has a logger, its manual dips otherwise."),
    ]),
    ("3", "Trigger thresholds", [
        ("3.1", "The trigger threshold for a bore is set by the class of the aquifer it draws from: 2 m for an "
                "unconsolidated aquifer and 5 m for a consolidated aquifer."),
    ]),
    ("4", "Impaired capacity", [
        ("4.1", "A bore has impaired capacity when the decline in its water level caused by the mine's take of "
                "associated water, at its assessment level, exceeds the trigger threshold for its aquifer. A decline "
                "with another cause is not the mine's."),
        ("4.2", "The assessment month for a bore under a complaint is the last complete month before the "
                "assessment."),
        ("4.3", "The principal hydrogeologist assesses each bore and recommends offers to the executive team, which "
                "approves them."),
    ]),
    ("5", "Baseline assessments", [
        ("5.1", "Before the take began, each bore in the register received a baseline assessment recording its "
                "construction, static level, yield and water quality."),
    ]),
    ("6", "Make good", [
        ("6.1", "Where a bore has impaired capacity, the mine offers its owner a make-good agreement. There is one "
                "agreement per owner, covering every bore of the owner's that has impaired capacity."),
        ("6.2", "A make-good agreement may provide for deepening or replacing the bore, lowering the pump, or "
                "supplying water while the bore is restored."),
    ]),
    ("7", "Complaints", [
        ("7.1", "A landholder who believes a bore has been affected by the mine may complain by phone, email, letter "
                "or in person. The complaint is recorded in the register and the bore is assessed under section 4."),
    ]),
]


def write_mg02(path):
    title = "MG-02 Landholder bore assessment and make good"
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=W.COMPANY, subject="Procedure MG-02, revision 3",
                            creator="Tarrabool Resources document control", producer="Tarrabool Resources document control")
    s = [Paragraph(title, H1),
         Paragraph("%s, %s" % (W.COMPANY, W.MINE), SMALL), Spacer(1, 5),
         _table([["Revision", "Effective", "Owner", "Approved", "Next review"],
                 ["3", "01/03/2026", "Principal hydrogeologist", "General manager, %s" % W.MINE, "March 2028"]],
                [18 * mm, 21 * mm, 44 * mm, 54 * mm, 24 * mm]),
         Spacer(1, 8)]
    for num, head, clauses in MG02_TEXT:
        block = [Paragraph("%s  %s" % (num, head), H2)]
        for cl, text in clauses:
            block.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (cl, text), CLAUSE))
        s.append(KeepTogether(block))
    s += [Spacer(1, 8), Paragraph("Revision history", H2),
          _table([["Revision", "Date", "Change"],
                  ["3", "01/03/2026", "One agreement per owner (6.1); make-good measures (6.2)"],
                  ["2", "14/03/2023", "Logged bores' daily levels (2.3) and assessment levels (2.4)"],
                  ["1", "07/03/2022", "First issue, for the baseline assessments before the take of associated water"]],
                 [18 * mm, 21 * mm, 122 * mm]),
          Spacer(1, 6),
          Paragraph("Distribution: environment; mining; general manager's office. The current revision is on the "
                    "site document register.", SMALL)]
    doc.build(s, onFirstPage=_frame(title, "MG-02 rev 3", "Effective 01/03/2026"),
              onLaterPages=_frame(title, "MG-02 rev 3", "Effective 01/03/2026"))
    PP.normalize_pdf(path, b"D:20260301083000+10'00'")


def write_notes(path):
    text = """# Kelvale groundwater monitoring network: notes on the October 2026 extract

Environment, Kelvale Mine. Erika Martin, 9 October 2026.

These notes go with the network extract taken on Friday 9 October 2026 for the MG-02 assessments. Water levels run
to 30 September 2026; the loggers were downloaded between 1 and 6 October.

## The network

27 bores: the 18 landholder bores in the register, three state reference bores outside the EIS predicted drawdown
(read by our field team under an arrangement with the department) and six mine monitoring bores on the pit
perimeter. The consultant read the network for the EIS baseline every quarter from March 2012 to June 2014. The field
team has read it monthly since July 2014, and the landholder bores every fortnight since 10 August 2026. Ten bores
have had pressure loggers since May 2015.

Pit dewatering began on 4 July 2022 from the pit sumps; the advance dewatering bores AD01 to AD04 came on from March
2023.

## Bores and their names

Every bore has the company's code (KV-LB for landholder bores, KV-RF for the reference bores, KV-MB for the mine's
bores) and its state registered number. The field sheets use the code; the consultant's EIS sheets used the
registered number. Landholders use their own names for their bores. The register (`%(reg)s`) holds all three, with
each bore's aquifer, construction and baseline assessment, the measuring point history and the other network bores.

## Manual dips (`%(dips)s`)

One row per entry keyed from the field sheets, in the order keyed.

| Field | Meaning |
|---|---|
| `entry_no` | Database entry number. |
| `reading_date`, `reading_time` | Date and time of the reading, Queensland time (AEST, no daylight saving). |
| `site` | The bore as written on the field sheet. |
| `dtw` | Depth to water below the measuring point. |
| `units` | `m`; `ft` for the consultant's EIS rounds (March 2012 to June 2014), which were read in feet. |
| `remarks` | The officer's notes from the field sheet (access, headworks, pump, weather), as written. |
| `officer` | Initials of the officer who read the bore (IVH is the EIS consultant). |

A dip is measured from the measuring point in force on the day. Two bores have had their headworks rebuilt since the
baseline assessments and the new measuring point surveyed; the register's measuring point sheet has the dates.

## Loggers

`%(logs)s` holds the hourly records of every logger: `logger_serial`, `timestamp_utc` (UTC), `pressure_kpa` (absolute
pressure at the sensor, kPa) and `temperature_c`. The loggers are unvented, so each reading includes air pressure.
`%(baro)s` is the site barometric logger, hourly, also in UTC. `%(inst)s` gives each logger's bore, the times it went
in and came out (Queensland time) and its sensor depth below the measuring point.

The water column above the sensor is the logger pressure less the barometric pressure for the same hour, divided by
9.80665 kPa per metre of water. The level (m AHD) is the measuring point elevation less the sensor depth plus the
water column. Each logger is checked against a manual dip when it is downloaded; the check dips are in the dips file.

## Other files

- `%(clim)s`: gridded climate data for the point nearest the pit: daily rainfall (24 hours to 9 am on the date) and
  Morton's areal potential evapotranspiration (mm), with maximum and minimum temperature, from 1 January 1990 to 30
  September 2026.
- `%(take)s`: the daily metered volume from each dewatering source (ML).
- `%(qual)s`: field and laboratory water quality results by sampling round.
- `%(cont)s`: the environment team's log of contacts with neighbours in 2026.
""" % dict(reg=R.REGISTER, dips=R.DIPS, logs=R.LOGGERS, baro=R.BARO, inst=R.INSTALLS, clim=R.CLIMATE, take=R.TAKE,
           qual=R.QUALITY, cont=R.CONTACTS)
    with open(path, "w", newline="\n") as fh:
        fh.write(text)
