"""task231 architecture 2: the pack's documents. The District's data quality standard, the vendor's QC configuration,
Schedule B of the service agreement and the review request. Every table cell wraps inside the page; each PDF carries
its own issue stamps."""
import datetime as dt
import os
from email.message import EmailMessage
from email.utils import format_datetime

import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess as PP

reportlab.rl_config.invariant = 1
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.6, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.5,
                    spaceBefore=7, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.9, leading=10.2, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.2, leading=10.2, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(rows, widths):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.0),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#bbbbbb"))]))
    return t


def _pdf(path, title, author, story, footer, created, modified, tz):
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.8 * inch, 0.5 * inch, footer)
        canvas.drawRightString(letter[0] - 0.8 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch, title=title, author=author,
                            creator=author, producer=author)
    doc.build(story, onFirstPage=page, onLaterPages=page)
    PP.normalize_pdf(path, ("D:%s%s" % (created.strftime("%Y%m%d%H%M%S"), tz)).encode(),
                     ("D:%s%s" % (modified.strftime("%Y%m%d%H%M%S"), tz)).encode())


def standard(path):
    s = [Paragraph("Road Weather Information System Data Quality Standard", H1),
         Paragraph("%s, Maintenance Division, Intelligent Transportation Systems. Revision 2, effective "
                   "1 September 2026; supersedes Revision 1 of August 2021." % P.ORG, SMALL), Spacer(1, 6),
         Paragraph("1. Scope", H2),
         Paragraph("This standard applies to the District's environmental sensor stations (ESS) on the state "
                   "routes the District maintains, and to the observations the District's road weather vendor "
                   "passes to the maintenance decision support system (MDSS) and to the 511 traveler information "
                   "service.", BODY),
         Paragraph("2. Terms", H2),
         Paragraph("<b>Winter.</b> The period from 1 October 00:00 to 1 May 00:00, Mountain time.", BODY),
         Paragraph("<b>Winter hour.</b> A clock hour of the winter. A station's observation for an hour is the "
                   "observation stamped at the end of that hour.", BODY),
         Paragraph("<b>Withheld.</b> An observation an automated quality-control test kept out of the MDSS and "
                   "511 feeds.", BODY),
         Paragraph("<b>False rejection.</b> A winter hour on which an automated quality-control test withheld a "
                   "station's air temperature observation that was right. An air temperature observation is "
                   "right when it is within the sensor's stated accuracy of the air temperature at the station "
                   "in that hour. The District's air temperature probes are stated accurate to 0.3 C.", BODY),
         Paragraph("3. Winter review of the quality-control tests", H2),
         Paragraph("After each winter the ITS engineer reviews each automated air temperature test station by "
                   "station. A station's false-rejection share for a test is the number of winter hours with a "
                   "false rejection by that test at that station, as a percentage of the hours of the winter.", BODY),
         Paragraph("Where a station's false-rejection share for a test is above 2 per cent, the District asks the "
                   "vendor to re-tune that test at that station before the next winter begins. The District sends "
                   "the vendor its list of stations by 1 June. A test is not re-tuned at a station whose share is "
                   "2 per cent or less.", BODY),
         Paragraph("4. MDSS pavement indicators", H2),
         Paragraph("Each winter the District reports for each station:", BODY),
         _table([["Indicator", "Definition"],
                 ["Freezing hours", "Winter hours in which the station's travel-lane pavement sensor reported a "
                                    "surface temperature at or below 32.0 F (0.0 C)."],
                 ["Ice hours", "Winter hours in which the station's travel-lane pavement sensor reported a surface "
                               "status of ice warning or ice watch."]], [1.5, 5.3]),
         Spacer(1, 4),
         Paragraph("A pavement sensor replaced during the winter counts for the hours each sensor reported. A "
                   "bridge-deck sensor is not a travel-lane sensor.", BODY),
         Paragraph("5. Vendor service levels", H2),
         Paragraph("The vendor's data availability is measured under Schedule B of the operations and data "
                   "services agreement.", BODY),
         Paragraph("6. Revision history", H2),
         _table([["Revision", "Date", "Change"],
                 ["1", "16 August 2021", "First issue."],
                 ["2", "28 August 2026", "The winter review is made per test and per station; the MDSS pavement "
                                         "indicators added."]], [0.9, 1.4, 4.5])]
    _pdf(path, "RWIS Data Quality Standard, Revision 2", P.PEOPLE["engineer"][0], s,
         "%s  |  RWIS Data Quality Standard  |  Revision 2" % P.ORG, dt.datetime(2026, 8, 24, 10, 12, 0),
         dt.datetime(2026, 8, 28, 15, 41, 0), "-06'00'")


def qc_config(path):
    s = [Paragraph("Air temperature quality control: configuration 4.3", H1),
         Paragraph("%s for the %s ESS network. Contract SDHD-2023-114. Document QRWS-QC-0457, issue 3." % (
             P.VENDOR, P.ORG), SMALL), Spacer(1, 6),
         Paragraph("1. Tests", H2),
         Paragraph("Each air temperature observation the District's central server receives is checked by the "
                   "tests below at the next QC run. The QC runs at 20 minutes past each hour on every observation "
                   "received since the previous run. An observation that fails any test is withheld from the MDSS "
                   "and 511 feeds and written to the QC withheld log, one row per test it failed.", BODY),
         _table([["Test", "Withheld when"],
                 ["Range", "the reading is below -45.0 C or above 50.0 C."],
                 ["Step", "the reading differs by more than 10.0 C from the station's reading for the previous "
                          "hour."],
                 ["Persistence", "the reading has not changed for 6 hours or more."],
                 ["Spatial", "the reading differs by more than 6.0 C from the spatial estimate (section 2)."]],
                [1.3, 5.5]),
         Paragraph("2. Spatial estimate", H2),
         Paragraph("The spatial estimate for a station is taken from the other District stations within 45 km "
                   "whose readings for the same hour the server holds at the QC run. Each neighbour's reading is "
                   "carried to the station's elevation at a lapse rate of 6.5 C per km and weighted by the inverse "
                   "square of its distance from the station. The spatial test is not applied when fewer than two "
                   "neighbours are available.", BODY),
         Paragraph("3. Acceptance", H2),
         Paragraph("Configuration 4.3 was accepted by the District on 18 July 2025 on the summer 2024 archive "
                   "(1 June to 31 August 2024). Faults were injected at random stations and hours: spikes, stuck "
                   "readings and slow drifts of 5 C or more.", BODY),
         _table([["Acceptance measure", "Result", "Required"],
                 ["Injected faults withheld", "100.0 per cent", "95 per cent or more"],
                 ["Uninjected observations withheld", "0.3 per cent", "1 per cent or less"]], [3.0, 1.6, 2.2]),
         Paragraph("4. Releases", H2),
         _table([["Release", "In service", "Change"],
                 ["4.3.0", "30 September 2025", "Configuration 4.3 as accepted."],
                 ["4.3.2", "12 January 2027", "Dew point range test corrected; the air temperature tests are "
                                              "unchanged."]], [0.9, 1.5, 4.4])]
    _pdf(path, "Air temperature QC configuration 4.3", P.PEOPLE["vendor"][0], s,
         "%s  |  QRWS-QC-0457 issue 3  |  configuration 4.3" % P.VENDOR, dt.datetime(2025, 9, 22, 14, 3, 0),
         dt.datetime(2027, 1, 13, 9, 26, 0), "-07'00'")


def schedule_b(path):
    s = [Paragraph("Schedule B: Service levels", H1),
         Paragraph("Operations and Data Services Agreement SDHD-2023-114 between the %s and %s. Schedule B, "
                   "as amended by Amendment 2 (1 July 2025)." % (P.ORG, P.VENDOR), SMALL), Spacer(1, 6),
         Paragraph("B1. Service period", H2),
         Paragraph("The winter service period runs from 1 October 00:00 to 1 May 00:00, Mountain time.", BODY),
         Paragraph("B2. Data availability", H2),
         Paragraph("An hour of the service period is available at a station when that station's observation for "
                   "the hour was received at the District's central server no later than 20 minutes after the "
                   "end of the hour. An hour that lies wholly within a planned outage the District was notified of "
                   "at least 48 hours in advance is excluded. Every other hour of the service period is an "
                   "unavailable hour.", BODY),
         Paragraph("Availability is measured from the central server's message log.", BODY),
         Paragraph("B3. Service level and credits", H2),
         _table([["Measure", "Service level", "Credit"],
                 ["Station availability over the service period", "97.5 per cent of the hours not excluded",
                  "0.5 per cent of the annual station fee for each full 10 unavailable hours beyond the service "
                  "level, capped at 25 per cent"],
                 ["Network availability over the service period", "98.5 per cent of the station-hours not "
                                                                  "excluded", "As agreed at the annual review"]],
                [2.2, 2.0, 2.6]),
         Paragraph("B4. Reporting", H2),
         Paragraph("The vendor reports availability by station within 30 days of the end of the service period. "
                   "The District's own measurement from the message log prevails.", BODY)]
    _pdf(path, "SDHD-2023-114 Schedule B", P.PEOPLE["vendor"][0], s,
         "SDHD-2023-114  |  Schedule B  |  Amendment 2", dt.datetime(2025, 6, 12, 11, 20, 0),
         dt.datetime(2025, 6, 27, 16, 2, 0), "-06'00'")


def email(path):
    m = EmailMessage()
    m["From"] = "%s <%s@%s>" % (P.PEOPLE["manager"][0], P.PEOPLE["manager"][1], P.DOMAIN)
    m["To"] = "%s <%s@%s>" % (P.PEOPLE["engineer"][0], P.PEOPLE["engineer"][1], P.DOMAIN)
    m["Subject"] = "Winter 2026/27 RWIS review"
    m["Date"] = format_datetime(dt.datetime(2027, 5, 18, 8, 42, 0, tzinfo=dt.timezone(dt.timedelta(hours=-6))))
    m["Message-ID"] = "<rwis-review-2027.20270518084200.mhayden@%s>" % P.DOMAIN
    body = ("Lynn,\n\nRobyn Reeves at Quillan needs our spatial test list by 1 June so their engineers can book the "
            "re-tune work before October. Can you run the winter review under the standard (Rev 2) and bring the "
            "list to the operations meeting on 27 May? I also need each station's Schedule B hours for the "
            "contract file, and the freezing and ice hours for the section supervisors' winter reports.\n\n"
            "Everything we have from the winter is in the review folder: the ESS export, Quillan's withheld log, "
            "the central server's message log, the modem and site registers, the outage notices, the pavement "
            "export and the pre-season checks from last fall. The HRRR point forecasts Dispatch pulls and the ATR "
            "counts are in there as well.\n\nThanks,\nMelissa\n\nMelissa Hayden\nITS Program Manager\n%s\n" % P.ORG)
    m.set_content(body)
    with open(path, "wb") as f:
        f.write(bytes(m))


def write_all(target):
    f = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    standard(f["standard"])
    qc_config(f["qcconfig"])
    schedule_b(f["sla"])
    email(f["email"])
