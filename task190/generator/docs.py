"""The bank's own programme handbook, last year's filed report, and the vendor's service report."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)
CELL = ParagraphStyle("c", fontName="Times-Roman", fontSize=8, leading=10)
CELLB = ParagraphStyle("cb", fontName="Times-Bold", fontSize=8, leading=10)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.90, 0.90, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])


def wrap(rows, head=True):
    out = []
    for i, r in enumerate(rows):
        out.append([Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r])
    return out


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author=W.BANK, subject="",
                             creator=W.BANK, leftMargin=20 * mm, rightMargin=20 * mm,
                             topMargin=18 * mm, bottomMargin=18 * mm)


def handbook(target):
    path = os.path.join(target, "aml_programme_handbook.pdf")
    d = _doc(path, "AML and CFT programme handbook")
    f = []
    f.append(Paragraph("%s" % W.BANK, H1))
    f.append(Paragraph("Anti-money laundering and countering financing of terrorism programme: "
                       "handbook, part 7, reporting", H2))
    f.append(Paragraph("Version 9.2, approved 14 May 2026. Owner: money laundering reporting "
                       "officer. Review due May 2028.", SMALL))
    f.append(Spacer(1, 5))

    f.append(Paragraph("1.2 Reporting year", H2))
    f.append(Paragraph("The programme's reporting year runs from 1 July to 30 June. The annual "
                       "report for the year ended 30 June 2027 is due with the supervisor by "
                       "30 September 2027 and is signed by the money laundering reporting officer "
                       "after the board's audit and risk committee has seen it.", BODY))

    f.append(Paragraph("3.1 Prescribed transactions", H2))
    f.append(Paragraph("A domestic physical cash transaction of ten thousand dollars or more "
                       "requires a prescribed transaction report. The reporting engine raises a "
                       "report from the deposit feeds on the day after the transaction and the "
                       "financial crime team releases it within ten working days. Cash means "
                       "notes and coin counted at a counter or by a smart deposit machine; "
                       "cheques and electronic credits are not cash for this purpose.", BODY))
    f.append(Paragraph("3.2 Structuring", H2))
    f.append(Paragraph("Splitting cash so that no single transaction reaches the prescribed "
                       "transaction threshold is an offence under section 142 of the Act, whether "
                       "or not the cash itself is the proceeds of anything. The programme treats "
                       "the practice as a risk in its own right and reports on its extent each "
                       "year.", BODY))

    f.append(Paragraph("7.4 The annual report's structuring figure", H2))
    f.append(Paragraph("The annual report states, for each business segment, the number of "
                       "physical cash deposits of nine thousand dollars or more and below ten "
                       "thousand dollars that the segment's customers paid in during the "
                       "reporting year and that were paid in below the prescribed transaction "
                       "threshold when the amount would otherwise have been at or above it. The "
                       "count is of deposits, one for one, and not of customers or of days; a "
                       "deposit is counted in the reporting year in which it was paid in; every "
                       "customer on the business register at the end of the reporting year is "
                       "within its segment's count.", BODY))
    f.append(Paragraph("7.5 Segments", H2))
    f.append(Paragraph("The report uses the eight business banking segments the customer register "
                       "carries. Segment codes were reissued on 6 April 2027 under the bank's new "
                       "coding standard; the segments themselves were not changed and the register "
                       "carries both codings.", BODY))
    f.append(Paragraph("7.6 What the report also states", H2))
    f.append(Paragraph("Beside the figure at 7.4 the report states, for each segment, the cash "
                       "deposits its customers paid in during the reporting year; for each branch "
                       "and quarter, the cash count sessions recorded, those whose variance "
                       "exceeded the tolerance in force and the net variance; for each customer "
                       "risk band, the ratings raised and lowered during the year; and for each "
                       "month, the availability of the deposit machine estate.", BODY))

    f.append(Paragraph("9.1 Records", H2))
    f.append(Paragraph("The programme keeps the deposit feeds, the registers and the reporting "
                       "extracts for seven years from the end of the reporting year they fall in. "
                       "Extracts are pulled once, after the year closes, and are not re-pulled for "
                       "the report.", BODY))
    f.append(Paragraph("9.3 Branch changes", H2))
    f.append(Paragraph("Where a branch closes, its deposits are taken up at the branch named in "
                       "the estate register from the closing date, and the report treats the two "
                       "as one branch for the whole year.", BODY))
    d.build(f)
    return path


def prior_report(target, ptr_filed, cash_paid_in):
    path = os.path.join(target, "annual_report_extract_2026.pdf")
    d = _doc(path, "Annual report extract, year ended 30 June 2026")
    f = []
    f.append(Paragraph("%s" % W.BANK, H1))
    f.append(Paragraph("Annual AML and CFT report, year ended 30 June 2026: extract", H2))
    f.append(Paragraph("Filed with the supervisor 28 September 2026. Sections 2 and 5 only; the "
                       "full report is held by the financial crime team.", SMALL))
    f.append(Spacer(1, 5))
    f.append(Paragraph("2 Reporting volumes", H2))
    f.append(Paragraph("The bank filed the prescribed transaction reports set out below. The "
                       "engine was re-run twice during the year after configuration changes and "
                       "the figures are taken from the final run.", BODY))
    f.append(Table(wrap([["Report type", "Filed in the year"],
                         ["Prescribed transaction reports, physical cash", "%s" % format(ptr_filed, ",")],
                         ["Prescribed transaction reports, international wire", "4,118"],
                         ["Suspicious activity reports", "212"]]),
                   colWidths=[95 * mm, 45 * mm], style=TBL))
    f.append(Spacer(1, 6))
    f.append(Paragraph("5 Business banking cash", H2))
    f.append(Paragraph("Business banking customers paid in %s of physical cash over the year "
                       "across the counter and the smart deposit machine estate. The programme's "
                       "view is that the cash-intensive segments carry the bank's highest "
                       "residual risk, and the segment risk assessments at appendix C are "
                       "unchanged from the prior year." % cash_paid_in, BODY))
    f.append(Paragraph("The structuring figure required by paragraph 7.4 of the programme "
                       "handbook was first stated for the year ended 30 June 2027 and is not "
                       "given here; paragraph 7.4 was approved in May 2026.", BODY))
    d.build(f)
    return path


def vendor_report(target, monthly):
    """The machine estate vendor's own monthly service report, by site, hours as h:mm."""
    path = os.path.join(target, "vendor_service_report_2027.pdf")
    d = _doc(path, "Deposit machine estate service report 2026/27")
    f = []
    f.append(Paragraph("Kaituna Cash Systems Limited", H1))
    f.append(Paragraph("Smart deposit machine estate: monthly service report for %s" % W.BANK, H2))
    f.append(Paragraph("Contract ACS-4471. Reported by site, to the nearest minute, from the "
                       "vendor's own dispatch records. Issued 9 July 2027.", SMALL))
    f.append(Spacer(1, 5))
    f.append(Paragraph("Out of service time by site", H2))
    rows = [["Site", "Month", "Out of service", "Visits"]]
    for site, month, mins, visits in monthly:
        rows.append([site, month, "%d:%02d" % (mins // 60, mins % 60), str(visits)])
    f.append(Table(wrap(rows), colWidths=[32 * mm, 30 * mm, 38 * mm, 25 * mm], style=TBL,
                   repeatRows=1))
    f.append(Spacer(1, 6))
    f.append(Paragraph("Time is counted from the dispatch call to the engineer's sign off. Where "
                       "a site runs more than one machine the site's time is the total across "
                       "them. Machines withdrawn from service under the estate refresh are not "
                       "reported.", SMALL))
    d.build(f)
    return path
