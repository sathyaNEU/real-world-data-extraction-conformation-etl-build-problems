"""The agency's own signal detection standard and the assessment desk's capacity report."""
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


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=22 * mm, rightMargin=22 * mm,
                             topMargin=20 * mm, bottomMargin=18 * mm)


def _table(head, rows, widths):
    data = [[Paragraph(h, CELLB) for h in head]]
    for r in rows:
        data.append([Paragraph(str(c), CELL) for c in r])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TBL)
    return t


def standard(tgt):
    p = os.path.join(tgt, "signal_standard.pdf")
    d = _doc(p, "Standard for signal detection and assessment")
    s = []
    s.append(Paragraph("Standard for signal detection and assessment", H1))
    s.append(Paragraph("Pharmacovigilance division, edition 7, in force from 1 January 2026. "
                       "Parts 1, 5 and 6 and the annexes are not reproduced in this extract.", SMALL))

    s.append(Paragraph("2. The quarterly run", H2))
    s.append(Paragraph("2.1 A run covers the reports the agency received in the quarter. A report is "
                       "in the quarter when the date the agency received it falls on or between the "
                       "first and the last day of the quarter, both days included. The date the "
                       "reporter wrote the report, and the date the case was coded, do not bear on "
                       "which quarter a report belongs to.", BODY))
    s.append(Paragraph("2.2 A report is one case. Where a case reaches the agency through more than "
                       "one channel, the submissions are one report and are counted once, and the "
                       "case number is what joins them. A reaction reported more than once on one "
                       "case is one reaction on that case.", BODY))
    s.append(Paragraph("2.3 A reaction is the preferred term the case was coded to, at the version of "
                       "the reaction dictionary in force when the case was coded. The dictionary "
                       "records every term it has carried and the version each mapping belongs to.", BODY))
    s.append(Paragraph("2.4 A product is the product the register holds under one code. Where a "
                       "product has been renamed, the register carries the former name and the day "
                       "the name changed, and the reports stand under the one code throughout.", BODY))

    s.append(Paragraph("3. What the run takes forward", H2))
    s.append(Paragraph("3.1 A signal of disproportionate reporting is a product and reaction pair "
                       "whose reporting in the quarter is disproportionate, measured by the "
                       "proportional reporting ratio and the chi-square of the same table.", BODY))
    s.append(Paragraph("3.2 A pair is taken forward where the ratio is %.1f or more, the chi-square "
                       "is %.0f or more, and the pair is named on %d or more of the quarter's "
                       "reports. A pair failing any of the three is not taken forward."
                       % (W.PRR_MIN, W.CHI_MIN, W.N_MIN), BODY))
    s.append(Paragraph("3.3 A pair the product information already describes is not a signal and is "
                       "not taken forward. The register of what each product's information describes "
                       "is kept by the division and is current at the run.", BODY))
    s.append(Paragraph("3.4 A pair the desk has assessed and closed is not taken forward again in the "
                       "twelve months after it closed, unless the reporting has changed in kind.", BODY))

    s.append(Paragraph("4. The assessment desk", H2))
    s.append(Paragraph("4.1 The pairs a run takes forward go to the assessment desk at the triage "
                       "that follows the run. The desk's capacity for a quarter is set out in the "
                       "capacity report the division publishes before the quarter begins.", BODY))
    s.append(Paragraph("4.2 Where a run takes forward more pairs than the desk's capacity allows, the "
                       "desk works them in order of the number of reports naming the pair, the "
                       "largest first, and the pairs it cannot reach are carried to the next quarter.", BODY))
    s.append(Paragraph("4.3 The coordinator reports to the division the pairs taken forward, the "
                       "pairs carried, and the capacity used.", BODY))

    s.append(Paragraph("7. What this standard does not define", H2))
    s.append(Paragraph("The standard reduces the quarter's reports to pairs and sets the criteria a "
                       "pair meets to be taken forward. It does not set out how the division's "
                       "epidemiologists are to construct the measure in 3.1, which is their own work "
                       "and is recorded with each run.", BODY))
    d.build(s)
    return p


def capacity(tgt, worked_last):
    p = os.path.join(tgt, "assessment_capacity_report.pdf")
    d = _doc(p, "Assessment desk capacity report")
    s = []
    s.append(Paragraph("Assessment desk capacity report", H1))
    s.append(Paragraph("Pharmacovigilance division, published 18 September 2026 for the quarter "
                       "beginning 1 October 2026.", SMALL))
    s.append(Paragraph("1. Capacity", H2))
    s.append(Paragraph("The desk is staffed by four assessors at four fifths of full time and one "
                       "senior assessor. A signal assessment takes a mean of 7.5 assessor days from "
                       "triage to a closing note, and the desk holds 124 assessor days in the "
                       "quarter after leave and the division's other standing work. The desk can "
                       "therefore take <b>%d</b> assessments in the quarter beginning 1 October." % W.CAPACITY,
                       BODY))
    s.append(Paragraph("2. The quarter now closing", H2))
    s.append(Paragraph("The desk worked %d assessments in the quarter to 30 September and carried "
                       "none. Assessor days are charged to the division at 4,850 kroner a day."
                       % worked_last, BODY))
    s.append(Spacer(1, 4))
    s.append(_table(["Quarter", "Assessments taken", "Assessor days held", "Assessments carried in"],
                    [["2026 Q1", "13", "118", "0"], ["2026 Q2", "15", "121", "0"],
                     ["2026 Q3", str(worked_last), "119", "0"], ["2026 Q4", "capacity %d" % W.CAPACITY,
                                                                 "124", "0"]],
                    [28, 34, 34, 36]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("3. Note", H2))
    s.append(Paragraph("Capacity is the number of assessments the desk can close in the quarter. It "
                       "is not a limit on what a run may take forward, and it carries no measure of "
                       "how strong a pair's reporting is.", BODY))
    d.build(s)
    return p
