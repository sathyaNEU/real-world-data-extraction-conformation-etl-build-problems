"""The governing standard (PDF) and the extract field reference (Markdown)."""
from reportlab import rl_config
from reportlab.lib.pagesizes import A4

rl_config.invariant = 1
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

STANDARD = [
    ("h", "1  Purpose"),
    ("p", "This standard sets how Metering Data Services measures the read health of each communications "
          "firmware build in the field, and when the read-health alert fires on a build. The alert is the "
          "go/no-go input the rollout desk takes for each wave."),
    ("h", "2  Scope"),
    ("p", "Every communications firmware build (EM3 and PX5 modules) running on meters at installations "
          "where HVM is the metering data provider. Bench and laboratory meters are out of scope."),
    ("h", "3  Definitions"),
    ("p", "3.1  <b>Installation</b>: a metering installation, identified by its NMI."),
    ("p", "3.2  <b>Assessment week</b>: Monday 00:00 to Sunday 24:00 market time (AEST) immediately before "
          "the wave's go/no-go."),
    ("p", "3.3  <b>Expected interval reads</b>: every interval of every data stream metered at the "
          "installation in the assessment week."),
    ("p", "3.4  <b>Delivery cut-off</b>: 06:00 market time on the day after the read date."),
    ("p", "3.5  <b>Read held at cut-off</b>: an interval carrying an actual read in the latest MDM delivery "
          "for its data stream and read date received before the delivery cut-off. Deliveries received "
          "after the cut-off complete the settlement data; they do not change read health."),
    ("p", "3.6  A meter <b>runs</b> a build from its successful activation of that build, or its "
          "commissioning on it, until its next successful activation. A failed activation that is rolled "
          "back does not change the build the meter runs."),
    ("p", "3.7  <b>Assessed installation</b>: an installation whose meter ran the build from the start to "
          "the end of the assessment week. An installation whose meter was changed during the week is not "
          "assessed."),
    ("h", "4  Measure"),
    ("p", "4.1  An installation's read health is its reads held at cut-off as a percentage of its expected "
          "interval reads for the assessment week."),
    ("p", "4.2  A build's read health is the mean of its assessed installations' read health."),
    ("p", "4.3  Only the build's own assessed installations enter its read health and its standard error."),
    ("h", "5  Alert rule"),
    ("p", "5.1  The reference read health is 99.50 per cent."),
    ("p", "5.2  A build's lower limit sits three standard errors of the build's read health below the "
          "reference."),
    ("p", "5.3  The alert fires on a build whose read health is below its lower limit. Otherwise the build "
          "holds."),
    ("h", "6  Routing"),
    ("p", "6.1  <b>Fire</b>: the rollout desk holds every move onto the build in the coming wave; the vendor "
          "desk opens a defect against the build; Settlement Operations are told to expect substitutions on "
          "the build's installations."),
    ("p", "6.2  <b>Hold</b>: the coming wave proceeds on the build as scheduled."),
    ("h", "7  Reporting"),
    ("p", "Read health, standard errors and lower limits are reported in per cent to two decimal places. "
          "Standard deviations are sample standard deviations (divisor one less than the count), and "
          "standard errors are built from them."),
]


def standard_pdf(path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3)
    title = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=17)
    small = ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="MDS-STD-114 Firmware read health", author="Metering Data Services",
                            subject="Controlled document", creator="Microsoft Word", producer="Microsoft Word")
    story = [Paragraph("Halvane Metering Pty Ltd &nbsp;&nbsp;|&nbsp;&nbsp; Metering Data Services", small), Spacer(1, 4),
             Paragraph("MDS-STD-114 &nbsp;Firmware read health", title), Spacer(1, 6)]
    ctl = Table([["Revision", "3", "Effective", "01/07/2026"],
                 ["Owner", "Manager, Metering Data Services", "Approved", "Head of Metering Operations"],
                 ["Supersedes", "Revision 2 (01/02/2025)", "Review due", "30/06/2027"]],
                colWidths=[24 * mm, 56 * mm, 22 * mm, 58 * mm])
    ctl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
                             ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 8.5), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                             ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [ctl, Spacer(1, 8)]
    for kind, text in STANDARD:
        story.append(Paragraph(text, head if kind == "h" else body))
    story += [Spacer(1, 10), Paragraph("Revision history: r3 01/07/2026, cut-off aligned to the MDP service level; "
                                       "r2 01/02/2025, reference raised from 99.20 per cent; r1 14/08/2023, first issue.", small),
              Spacer(1, 4), Paragraph("Uncontrolled when printed. Internal: HVM staff and contracted rollout partners.", small)]
    doc.build(story)


FIELD_REFERENCE = """# MDS extract field reference

Metering Data Services, analytics team. Covers the extracts MDS pulls for the weekly read-health gate.
Last revised 14/09/2026 (T. Phillips).

## MDM interval receipts

`mdm_interval_receipts_<from>_<to>.csv`, one row per data stream, read date and delivery.

| Field | Meaning |
|---|---|
| NMI | National Metering Identifier, 10 characters (the MDM does not store the checksum character) |
| NMI_SUFFIX | data stream: E1 general supply, E2 controlled load, B1 export, Q1 reactive |
| READ_DATE | the market day the intervals belong to, CCYYMMDD, market time (AEST) |
| INTERVAL_LENGTH | minutes per interval for the data stream |
| UOM | unit of the interval values |
| DELIVERY_ID | MDM load batch that carried the row |
| RECEIVED_UTC | time the MDM received the delivery, UTC |
| QTY_A | intervals in the delivery carrying an actual read |
| QTY_S | intervals carrying a substituted value |
| QTY_F | intervals carrying a final substituted value |
| QTY_E | intervals carrying an estimated value from the MDM estimation run |
| DAY_TOTAL | sum of the day's interval values in UOM, every quality |

A delivery carries the whole data stream for the read date; a later delivery for the same NMI, suffix and
read date replaces the earlier one.

## HES firmware history

`hes_meter_firmware_history.json`, one object per meter registered to the head-end.

| Field | Meaning |
|---|---|
| meter_id | `MTR-` followed by the 8-digit meter serial |
| module, model | communications module family and meter model |
| status | IN_SERVICE, REMOVED, or BENCH (laboratory meters, never at an installation) |
| comms_parent | the node that collects the meter's reads: a collector (`EMC-`) on the EM3 mesh, an access point (`PXA-`) on the PX5 mesh; empty for bench meters |
| comms_parent_since | when the meter joined that node, UTC |
| events[].type | COMMISSIONED, FW_IMAGE_STAGED (image downloaded, not running), FW_ACTIVATED, FW_ACTIVATION_FAILED, FW_ROLLBACK_OK, DECOMMISSIONED |
| events[].image | HES image id; the release catalogue gives the release name |
| events[].job | rollout job reference |
| events[].event_id | identifier of the event at the meter |
| events[].ts_utc | time of the event at the meter, UTC |
| events[].ingested_utc | time the HES stored the event, UTC |
| events[].seq | HES storage sequence |

## MP installation register

`mp_installation_register_<date>.xlsx`: sheets Installations, Meters and Data streams. NMIs carry the
11th (checksum) character. Meter serials are 8 digits. Installed and Removed are local time at the
installation. Network is the distributor the installation is connected to.

## Wave schedules

Built by the rollout desk from the HES inventory on the day the wave is cut. Meter No is the meter serial;
NMI is filled in where the depot had it.
"""


def field_reference_md(path):
    with open(path, "w") as fh:
        fh.write(FIELD_REFERENCE)
