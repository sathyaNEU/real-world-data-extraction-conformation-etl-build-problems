"""The bundle's documents, each in its issuer's own genre: the network's operating procedure, the councils'
service agreement schedule, the check-source calibration certificates, the network's 2025 annual report and the
radiochemistry service's filter gamma spectrometry. None says how an increase's origin is established."""
import datetime as dt
import io
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

import world as W

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=12.6, alignment=TA_LEFT, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=6, textColor=colors.HexColor("#1F3B57"))
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3,
                    textColor=colors.HexColor("#1F3B57"))
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=10.5)
SMALLB = ParagraphStyle("smallb", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5)
GRID = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]
HEADFILL = colors.HexColor("#E8EEF4")


def cells(rows, bold_cols=(), bold_row0=False):
    return [[Paragraph(str(v), SMALLB if (j in bold_cols or (bold_row0 and i == 0)) else SMALL)
             for j, v in enumerate(r)] for i, r in enumerate(rows)]


def table(rows, widths, head=True, bold_cols=()):
    t = Table(cells(rows, bold_cols=bold_cols, bold_row0=head), colWidths=[w * mm for w in widths])
    style = list(GRID)
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEADFILL))
    for c in bold_cols:
        style.append(("BACKGROUND", (c, 0), (c, -1), HEADFILL))
    t.setStyle(TableStyle(style))
    return t


class Doc:
    """A document with a letterhead band and a footer carrying its reference, revision and page of pages."""

    def __init__(self, path, title, author, subject, band, right, footer):
        self.path, self.title, self.author, self.subject = path, title, author, subject
        self.band, self.right, self.footer = band, right, footer
        self.pages = 1

    def _frame(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(colors.HexColor("#1F3B57"))
        canvas.rect(0, h - 17 * mm, w, 17 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(18 * mm, h - 10.8 * mm, self.band)
        canvas.setFont("Helvetica", 8.2)
        canvas.drawRightString(w - 18 * mm, h - 10.8 * mm, self.right)
        canvas.setFillColor(colors.black)
        canvas.setFont("Helvetica", 7.4)
        canvas.drawString(18 * mm, 11 * mm, self.footer)
        canvas.drawRightString(w - 18 * mm, 11 * mm, "Page %d of %d" % (doc.page, self.pages))
        canvas.restoreState()

    def _build(self, target, story):
        doc = BaseDocTemplate(target, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=25 * mm,
                              bottomMargin=20 * mm, title=self.title, author=self.author, subject=self.subject,
                              creator="", producer="", invariant=1)
        fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
        doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=self._frame)])
        doc.build(story)
        return doc.page

    def build(self, make_story):
        self.pages = self._build(io.BytesIO(), make_story())
        self._build(self.path, make_story())


# ------------------------------------------------------------------ the operating procedure

def procedure(path):
    ref, rev, issued = "MVGN-OP-04", "6", "02/06/2025"
    d = Doc(path, "Network operating procedure", W.PEOPLE["manager"], ref, W.LAB_SHORT + " " + W.NETWORK_SHORT,
            W.NETWORK, "%s  Rev %s  Issued %s  Controlled copy on the laboratory SharePoint; uncontrolled when printed"
            % (ref, rev, issued))

    def story():
        s = [Paragraph("%s: network operating procedure" % W.NETWORK, H1)]
        s.append(table([["Document", ref, "Revision", rev],
                        ["Owner", "%s, Network Manager" % W.PEOPLE["manager"], "Issued", issued],
                        ["Applies to", "All stations and air samplers of the %s" % W.NETWORK, "Next review", "06/2027"]],
                       [24, 92, 22, 34], head=False, bold_cols=(0, 2)))
        s.append(Spacer(1, 6))
        s.append(Paragraph("1. Purpose", H2))
        s.append(Paragraph(
            "This procedure sets out how the %s operates the %s for the %s: how the stations' records are held and "
            "reviewed, how probes are checked, and how air filters are reported. Notification of increases to the "
            "Committee and the %s is made under Schedule 2 of the service agreement." % (W.LAB, W.NETWORK, W.COMMITTEE,
                                                                                       W.REGULATOR), BODY))
        s.append(Paragraph("2. Station records", H2))
        s.append(Paragraph(
            "Each station's probe measures the ambient dose equivalent rate, H*(10), and its outstation reports a "
            "value for every ten minutes. The platform stores each value against the start of its ten-minute "
            "interval in UTC. A value recorded while a station is in test mode carries the status T and is not "
            "monitoring data. When a probe reports a fault the outstation still sends a record for the interval, "
            "with the status F and no dose rate. Every other value carries the status V.", BODY))
        s.append(Paragraph("3. Reference levels and review", H2))
        s.append(Paragraph(
            "Each station's reference level for a quarter is entered on the platform's alarm configuration on the "
            "first day of the quarter. A ten-minute value 30 nSv/h or more above the reference level is an "
            "investigation-level value, and the duty radiation scientist reviews every period of investigation-level "
            "values within one working day of the platform raising it. At the end of each quarter the duty radiation "
            "scientist reviews the quarter's record for every station and prepares the notification and the "
            "quarterly report.", BODY))
        s.append(Paragraph("4. Source checks", H2))
        s.append(Paragraph(
            "Each probe is checked once a quarter with a sealed check source held in a field kit. The engineer puts "
            "the station into test mode, records the probe's reading without the source (the background) and then "
            "with the source seated in the kit's jig; the check reading is the reading with the source less the "
            "background. The expected reading is the reading on the source's calibration certificate for the jig "
            "used, corrected for the source's decay from the certificate's reference date to the date of the check. "
            "A certificate applies from its date of issue. A probe passes when its check reading is within 10 per "
            "cent of the expected reading. Where a check is repeated at the same visit, the repeat is the check.",
            BODY))
        s.append(Paragraph("5. Air sampling", H2))
        s.append(Paragraph(
            "The network's air samplers draw air through a glass-fibre filter, changed weekly. Each filter is sent "
            "to %s for gross beta counting, and its result is reported in the quarter in which the filter is taken "
            "off. A filter's gross beta activity concentration is its gross beta activity divided by the volume of "
            "air drawn through it." % W.LAB_GB, BODY))
        s.append(Paragraph("6. Probe exchanges", H2))
        s.append(Paragraph(
            "A probe that fails its check, or develops a fault, is exchanged for a calibrated probe from the "
            "laboratory's pool. The engineer records the exchange on the visit sheet and the laboratory enters the "
            "new probe's calibration factor on the platform.", BODY))
        s.append(Paragraph("7. Responsibilities", H2))
        s.append(table([["Role", "Responsibility"],
                        ["Network Manager", "Owns this procedure; signs the quarterly report"],
                        ["Duty Radiation Scientist", "Reviews investigation-level periods and the quarter's record; "
                         "prepares the notification and the quarterly report"],
                        ["Field Engineers", "Quarterly station visits, source checks, filter changes, probe exchanges"],
                        ["Radiochemistry Services", "Gross beta counting and gamma spectrometry of air filters"]],
                       [52, 120]))
        tail = [Paragraph("8. Revision history", H2),
                table([["Rev", "Date", "Change", "Approved"],
                       ["3", "11/02/2019", "Air sampling added", "Rosemary Wood"],
                       ["4", "27/09/2021", "Investigation level set at reference level plus 30 nSv/h", "Rosemary Wood"],
                       ["5", "08/01/2024", "Field kits and jigs; source check repeats", W.PEOPLE["manager"]],
                       ["6", issued, "Platform migration: interval start in UTC, test and fault status, platform codes",
                        W.PEOPLE["manager"]]], [12, 22, 108, 30]),
                Spacer(1, 10),
                table([["Prepared", "%s, Duty Radiation Scientist" % W.PEOPLE["duty"], "30/05/2025"],
                       ["Approved", "%s, Network Manager" % W.PEOPLE["manager"], "02/06/2025"]],
                      [24, 118, 30], head=False, bold_cols=(0,))]
        s.append(KeepTogether(tail))
        return s
    d.build(story)


# ------------------------------------------------------------------ the service agreement schedule

def agreement(path):
    ref = "MVJC/SA/2024/03"
    d = Doc(path, "Service agreement, Schedule 2", W.PEOPLE["clerk"], ref, W.COMMITTEE, "Service agreement %s" % ref,
            "%s  Schedule 2: service levels and reporting  Version 2, 1 April 2024" % ref)

    def story():
        s = [Paragraph("Schedule 2: service levels and reporting", H1)]
        s.append(Paragraph(
            "This Schedule forms part of the agreement dated 1 April 2024 between the %s (the Committee), acting for "
            "%s, %s and %s, and %s (the Contractor) for the operation of the %s." % (
                W.COMMITTEE, W.COUNCILS[0], W.COUNCILS[1], W.COUNCILS[2], W.UNIVERSITY, W.NETWORK), BODY))
        s.append(Paragraph("2.1 The monitoring service", H2))
        s.append(Paragraph(
            "The Contractor operates the network's gamma dose-rate stations and air samplers continuously, maintains "
            "and checks them under its operating procedure, and keeps their records for at least ten years.", BODY))
        s.append(Paragraph("2.2 Notifications", H2))
        s.append(Paragraph(
            "The Contractor notifies the Committee and the %s of every increase in the ambient dose equivalent rate "
            "recorded at a network station that is of artificial origin, giving the station, the date of the "
            "increase and the highest ten-minute value recorded during it. Increases of natural origin, and the "
            "Contractor's own source checks, are not notified. Notifications for a quarter are made with that "
            "quarter's report." % W.REGULATOR, BODY))
        s.append(Paragraph("2.3 Timeliness", H2))
        s.append(Paragraph(
            "Timeliness for a station is the percentage of the quarter's ten-minute intervals for which the "
            "platform received the station's value by telemetry within sixty minutes of the end of the interval.",
            BODY))
        s.append(Paragraph("2.4 Quarterly report", H2))
        s.append(Paragraph(
            "Within fifteen working days of the end of each quarter the Contractor sends the Committee its quarterly "
            "report, giving the quarter's notifications, each station's timeliness, each station's source check "
            "and its result, and the gross beta results of the quarter's air filters.", BODY))
        s.append(Paragraph("2.5 Service credits", H2))
        s.append(table([["Measure", "Level", "Credit"],
                        ["Timeliness, any station", "below 95 per cent in a quarter", "2 per cent of the quarter's fee per station"],
                        ["Quarterly report", "later than fifteen working days", "5 per cent of the quarter's fee"],
                        ["Source checks", "a station not checked in the quarter", "1 per cent of the quarter's fee per station"]],
                       [52, 58, 62]))
        s.append(Spacer(1, 8))
        s.append(Paragraph("2.6 Fees", H2))
        s.append(Paragraph(
            "The quarterly fee is set in Schedule 3 and is invoiced in arrears with the quarterly report.", BODY))
        s.append(Spacer(1, 10))
        s.append(KeepTogether([table([["For the Committee", "%s, Clerk to the Joint Committee" % W.PEOPLE["clerk"], "21/03/2024"],
                                      ["For the Contractor", "Director of Research Services, %s" % W.UNIVERSITY, "25/03/2024"]],
                                     [32, 110, 30], head=False, bold_cols=(0,))]))
        return s
    d.build(story)


# ------------------------------------------------------------------ calibration certificates

def received(serial, ref):
    if serial == "CS-0583" and ref.year == 2026:
        return W.RMU_RECEIVED
    return ref - dt.timedelta(days={"CS-0417": 6, "CS-0583": 8, "CS-0729": 5}[serial])


def certificates(path):
    d = Doc(path, "Calibration certificates, check sources", "Radiation Metrology Unit", "HCX-CAL",
            W.UNIVERSITY + " Radiation Metrology Unit", "Calibration laboratory 4217",
            "Calibration certificates for sealed check sources  Issued by the Radiation Metrology Unit")

    def story():
        s = []
        allc = []
        for serial, certs in W.SOURCES.items():
            for c in certs:
                allc.append((c[2], serial, c))
        allc.sort()
        for k, (_, serial, (no, ref, issued, vals)) in enumerate(allc):
            if k:
                s.append(PageBreak())
            s.append(Paragraph("Certificate of calibration %s" % no, H1))
            s.append(table([["Customer", W.LAB],
                            ["Item", "Sealed check source, caesium-137, serial %s, in its field kit holder" % serial],
                            ["Nuclide data", "Caesium-137, half-life 30.05 years"],
                            ["Date received", received(serial, ref).strftime("%d/%m/%Y")],
                            ["Reference date", ref.strftime("%d %B %Y")],
                            ["Method", "Ambient dose equivalent rate H*(10) at the reference point of a GTP-6 probe, "
                             "measured with the laboratory's transfer standard in each jig"]],
                           [34, 138], head=False, bold_cols=(0,)))
            s.append(Spacer(1, 8))
            s.append(Paragraph("Results at the reference date", H2))
            s.append(table([["Jig", "Ambient dose equivalent rate (nSv/h)", "Expanded uncertainty (k = 2)"],
                            ["J1 clamp", "%.0f" % vals["J1"], "3.5 per cent"],
                            ["J2 sleeve", "%.0f" % vals["J2"], "3.5 per cent"]], [40, 70, 62]))
            s.append(Spacer(1, 8))
            s.append(Paragraph(
                "The results relate only to the item calibrated, at the reference date. The background at the "
                "reference point has been subtracted. This certificate supersedes any earlier certificate for the "
                "same item from its date of issue.", BODY))
            s.append(Spacer(1, 14))
            s.append(table([["Date of issue", issued.strftime("%d/%m/%Y")],
                            ["Calibrated by", "Kim Simpson"], ["Checked and approved", "Brian Smith, Technical Manager"]],
                           [44, 128], head=False, bold_cols=(0,)))
        return s
    d.build(story)


# ------------------------------------------------------------------ distractors

def annual_report(path, rows):
    ref = "MVGN-AR-2025"
    d = Doc(path, "Annual report 2025", W.PEOPLE["manager"], ref, W.LAB_SHORT + " " + W.NETWORK_SHORT, "Annual report 2025",
            "%s  Report to the %s, March 2026" % (ref, W.COMMITTEE))

    def story():
        s = [Paragraph("%s: annual report 2025" % W.NETWORK, H1)]
        s.append(Paragraph(
            "This report gives the network's annual results for 1 January to 31 December 2025. The network's "
            "outstations moved to the new platform on 14 May 2025; the platform codes are used throughout. There "
            "were no notifications under Schedule 2 in 2025.", BODY))
        s.append(Paragraph("Annual mean ambient dose equivalent rate and data capture, 2025", H2))
        body = [["Station", "Site", "Annual mean (nSv/h)", "Data capture (per cent)"]]
        body += [[a, b, "%.1f" % c, "%.1f" % e] for a, b, c, e in rows]
        s.append(table(body, [22, 62, 40, 48]))
        s.append(Spacer(1, 6))
        s.append(Paragraph(
            "Annual means are taken over every valid ten-minute value in the year. Data capture is the share of the "
            "year's ten-minute intervals for which the platform holds a valid value.", BODY))
        s.append(Paragraph("Air sampling", H2))
        s.append(Paragraph(
            "Gross beta activity concentrations at the three samplers ranged from 0.21 to 1.07 mBq/m3 over the year, "
            "in line with earlier years. Monthly gamma spectrometry found no artificial radionuclide above its "
            "minimum detectable activity.", BODY))
        s.append(Spacer(1, 10))
        s.append(table([["Prepared", "%s, Duty Radiation Scientist" % W.PEOPLE["duty"], "11/03/2026"],
                        ["Approved", "%s, Network Manager" % W.PEOPLE["manager"], "16/03/2026"]],
                       [24, 118, 30], head=False, bold_cols=(0,)))
        return s
    d.build(story)


def gamma_spec(path, rows):
    d = Doc(path, "Gamma spectrometry of air filter composites", W.PEOPLE["chem"], "RCS-26-Q3-GS",
            W.LAB_GB, "Report RCS-26-Q3-GS", "RCS-26-Q3-GS  Gamma spectrometry of monthly air filter composites, Q3 2026")

    def story():
        s = [Paragraph("Gamma spectrometry of monthly air filter composites, July to September 2026", H1)]
        s.append(Paragraph(
            "Each month's filters from each sampler were combined after gross beta counting and counted for 80,000 s "
            "on the laboratory's HPGe detector. Activity concentrations are referred to the middle of each month. "
            "Results below the minimum detectable activity are shown as less than that activity.", BODY))
        body = [["Sampler", "Month", "Be-7 (mBq/m3)", "Pb-210 (mBq/m3)", "K-40 (mBq/m3)", "Cs-137 (mBq/m3)", "I-131 (mBq/m3)"]]
        body += [list(r) for r in rows]
        s.append(table(body, [16, 20, 26, 28, 26, 28, 28]))
        s.append(Spacer(1, 10))
        s.append(table([["Analyst", W.PEOPLE["chem"], "06/10/2026"], ["Checked", "Gerard Buckley", "07/10/2026"]],
                       [24, 118, 30], head=False, bold_cols=(0,)))
        return s
    d.build(story)


def build(tgt, FILES, extras):
    procedure(os.path.join(tgt, FILES["procedure"]))
    agreement(os.path.join(tgt, FILES["agreement"]))
    certificates(os.path.join(tgt, FILES["certs"]))
    annual_report(os.path.join(tgt, FILES["national"]), extras["annual"])
    gamma_spec(os.path.join(tgt, FILES["gammaspec"]), extras["gammaspec"])
