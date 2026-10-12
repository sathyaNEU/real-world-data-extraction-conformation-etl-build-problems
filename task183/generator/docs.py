"""The pack's documents: the reliability reporting standard (TVE-RS-04), the underground cable section of the 2025
annual reliability report, and the extract notes (field definitions and where each file came from)."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import LETTER                                 # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import inch                                       # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

STANDARD = "TVE-RS-04_reliability_reporting_standard_rev6.pdf"
REPORT = "2025_annual_reliability_report_sec6_ug_cable.pdf"
NOTES = "asset_analytics_extract_notes_2026-10.md"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
SERIF, SERIF_B, SANS, SANS_B = "LiberationSerif", "LiberationSerif-Bold", "LiberationSans", "LiberationSans-Bold"
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#5b6470")
BODY = ParagraphStyle("body", fontName=SERIF, fontSize=10.2, leading=13.4, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=14, leading=18, textColor=INK, spaceAfter=2)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=10.5, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
META = ParagraphStyle("meta", fontName=SANS, fontSize=8.2, leading=10.5, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.3, leading=10, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(0.85 * inch, 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.85 * inch, 0.55 * inch, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.85 * inch, title=title, author=author,
                             subject="", creator="", producer="")


STANDARD_CLAUSES = [
    ("1", "Scope", [
        ("1.1", "This standard sets how %s computes the reliability indices it reports for the Tamsin Valley "
                "district and files with the Commission. It adopts the definitions and methods of IEEE Std "
                "1366-2022 except where a clause below says otherwise." % W.COMPANY),
        ("1.2", "The Tamsin Valley district (Harrow Road, Mill Lane, Quarry Hill and Sutter Park substations and "
                "their eight 13.2 kV feeders) reports as one system."),
    ]),
    ("2", "Reporting period and time", [
        ("2.1", "The reliability year runs from 1 October to 30 September and is named for the year in which it "
                "ends. Reliability years, days and every period in this standard are in local prevailing time "
                "(Eastern)."),
        ("2.2", "An interruption belongs to the day, and to the period, in which the outage that caused it began."),
    ]),
    ("3", "Customers and interruptions", [
        ("3.1", "A customer is a metered service point."),
        ("3.2", "Customers served, for a feeder or for the system, are the metered points connected to it in the "
                "network connectivity model on the last day of the period."),
        ("3.3", "A sustained interruption is a loss of supply to a customer lasting more than five minutes, timed "
                "for that customer from the start of the outage to the restoration of that customer's supply. An "
                "interruption of five minutes or less is momentary and is left out of SAIFI, SAIDI and CEMI."),
    ]),
    ("4", "Indices", [
        ("4.1", "SAIFI is the number of customer sustained interruptions divided by customers served. SAIDI is the "
                "customer minutes of sustained interruption divided by customers served."),
        ("4.2", "A feeder's customer interruptions and customer minutes are those of the outages on its own "
                "devices; for an outage of a substation transformer bank, those of the bank's customers on that "
                "feeder."),
    ]),
    ("5", "Major event days", [
        ("5.1", "Major event days are identified by the 2.5 beta method. The daily SAIDI of each day of the five "
                "reliability years before the reporting year is the customer minutes of sustained interruptions "
                "beginning that day divided by the customers served on the last day of that reliability year. Days "
                "with no customer minutes are left out. Alpha is the mean and beta the standard deviation of the "
                "natural logarithms of the remaining daily values, and the threshold is exp(alpha + 2.5 beta)."),
        ("5.2", "A day of the reporting year whose daily SAIDI, on the reporting year's customers served, exceeds "
                "the threshold is a major event day. Indices reported with major event days excluded leave out the "
                "interruptions that began on them."),
    ]),
    ("6", "Customers experiencing multiple interruptions", [
        ("6.1", "CEMIn counts the customers with n or more sustained interruptions in the period, major event days "
                "included. The count is taken for each metered point over every outage that interrupted it in the "
                "period, and the point is reported under the feeder it is connected to on the last day of the "
                "period."),
    ]),
    ("7", "Records", [
        ("7.1", "Interruptions are taken from the outage management records: the legacy outage management system "
                "to 17 March 2026 and the advanced distribution management system (ADMS) from that date."),
        ("7.2", "Reliability Engineering holds the published major event day list for each reliability year."),
    ]),
]


def write_standard(path):
    doc = _doc(path, "TVE-RS-04 Reliability Reporting Standard", W.PEOPLE["reliability"])
    story = [Paragraph("Reliability Reporting Standard", H1),
             Paragraph("TVE-RS-04, revision 6. Effective 1 January 2024. Owner: Reliability Engineering (%s). "
                       "Supersedes revision 5 (2019)." % W.PEOPLE["reliability"], META)]
    for no, head, clauses in STANDARD_CLAUSES:
        story.append(Paragraph("%s  %s" % (no, head), H2))
        for cno, text in clauses:
            story.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (cno, text), CLAUSE))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Revision 6 moves the reliability year to October through September to match the "
                           "Commission's filing calendar and adds clause 6.", META))
    frame = _frame("%s  |  TVE-RS-04 rev 6" % W.COMPANY, "Controlled copy on the standards library")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


def _grid(rows, widths, bold_last=False):
    data = [[Paragraph(str(c), CELLB if (i == 0 or (bold_last and i == len(rows) - 1)) else CELL) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.5, GREY),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def write_report(path, failures, miles, customers):
    """failures: {feeder: {year: n}}; miles: {feeder: {year: miles}}; customers: {feeder: {year: n}}."""
    doc = _doc(path, "2025 Annual Reliability Report, Section 6", W.PEOPLE["reliability"])
    years = [2021, 2022, 2023, 2024, 2025]
    story = [Paragraph("Section 6. Underground cable, Tamsin Valley district", H1),
             Paragraph("2025 Annual Reliability Report to the Commission (calendar year 2025). Filed 30 April 2026. "
                       "Prepared by Reliability Engineering.", META),
             Paragraph("6.1&nbsp;&nbsp;This section reports the district's underground primary cable failures by "
                       "feeder and calendar year: the failures of the cable itself (insulation, splice and "
                       "termination failures; damage by others is reported in section 7) repaired in the year on the "
                       "cable in service on the feeder at the time.", BODY)]
    rows = [["Feeder"] + [str(y) for y in years] + ["2021-2025"]]
    for f in W.FEEDERS:
        rows.append([W.NAME[f]] + [str(failures[f][y]) for y in years] + [str(sum(failures[f][y] for y in years))])
    rows.append(["District"] + [str(sum(failures[f][y] for f in W.FEEDERS)) for y in years] +
                [str(sum(failures[f][y] for f in W.FEEDERS for y in years))])
    story += [Paragraph("Table 6.1  Underground primary cable failures by feeder", H2),
              _grid(rows, [1.45 * inch] + [0.7 * inch] * 5 + [0.85 * inch], bold_last=True)]
    rows = [["Feeder"] + ["%d" % y for y in years]]
    for f in W.FEEDERS:
        rows.append([W.NAME[f]] + ["%.1f" % miles[f][y] for y in years])
    story += [Paragraph("Table 6.2  Underground primary cable in service at 31 December, circuit miles", H2),
              _grid(rows, [1.45 * inch] + [0.7 * inch] * 5),
              Paragraph("2021 and 2022 as filed, on the plat lengths; from 2023 on the GIS lengths after the 2023 "
                        "re-measurement of the network.", META)]
    rows = [["Feeder"] + ["%d" % y for y in years]]
    for f in W.FEEDERS:
        rows.append([W.NAME[f]] + ["{:,}".format(customers[f][y]) for y in years])
    story += [Paragraph("Table 6.3  Customers served at 31 December", H2),
              _grid(rows, [1.45 * inch] + [0.7 * inch] * 5),
              Spacer(1, 6),
              Paragraph("6.2&nbsp;&nbsp;Harrow Road 12's paper-insulated lead-covered cable was replaced between April "
                        "and November 2025 under the PILC replacement program; its 2025 count includes the failures "
                        "on that cable before it was retired.", BODY)]
    frame = _frame("%s  |  2025 Annual Reliability Report" % W.COMPANY, "Section 6")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


NOTES_TEXT = """# Extract for the 2027 UG cable program review

Pulled 6 Oct 2026 for {asset} (Distribution Asset Management). Tamsin Valley district only, the eight feeders out of
Harrow Road, Mill Lane, Quarry Hill and Sutter Park. Everything runs through 30 Sep 2026 unless it says otherwise.
GIS and work order questions to {gis}, outage and reliability questions to {rel}.

Files:
- {wo}: SAP PM cable fault orders (order type ZUGF). Orders before 2012 were not converted.
- {reg}: GIS UG primary sections layer, nightly export of 30 Sep, in service and retired.
- {codes}: cause, repair and GIS status codes.
- {oms}, {steps}: one export view over legacy OMS (to 17 Mar 2026) and ADMS (from 17 Mar 2026), outages from 1 Oct 2020.
- {conn}, {devices}: network model, meter to transformer to protective device, and the device hierarchy.
- {cis}: CIS active accounts at 30 Sep.
- {med}: Reliability Engineering's published MED list, RY2021 to RY2025.
- {standard}, {report}: from the standards library and the 2025 filing.
- {vaults}, {loading}: inspections database and SCADA monthly peaks, as asked.

Things to know:
- When a section is replaced the old one is retired in GIS (status RET, retired_date filled) and the new cable goes in as
  a new section with predecessor_section_id pointing at the old one. A retired section keeps the feeder it was on when
  it was retired.
- feeder_id on a work order is the feeder when the order was raised. On a REPL order completed_date is the day the new
  cable was energised.
- OMS export is one row per outage per feeder affected; restore_ts is when the last customer came back. Legacy OMS
  times are Eastern local, ADMS times are UTC, and the step table uses the same clock as its outage.
- Connectivity rows: eff_to is the first day the row no longer applies, blank while current. A new row is opened when
  the point's device, feeder or meter changes.
- Device list in-service dates are blank for devices in service since the model went live (Nov 2014).
"""


def write_notes(path, counts):
    import records as R
    text = NOTES_TEXT.format(asset=W.PEOPLE["asset"], gis=W.PEOPLE["gis"], rel=W.PEOPLE["reliability"], wo=R.WO, reg=R.REGISTER,
                             codes=R.CODES, oms=R.OMS, steps=R.STEPS, conn=R.CONN, devices=R.DEVICES, cis=R.CIS,
                             med=R.MED, standard=STANDARD, report=REPORT, vaults=R.VAULTS, loading=R.LOADING)
    with open(path, "w", newline="\n") as fh:
        fh.write(text)
