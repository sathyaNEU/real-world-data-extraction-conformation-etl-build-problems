"""The authority's own documents: the audit plan, the audit manual, the testing schedule."""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=5)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=7,
                    spaceAfter=3)
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12.5, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica-Oblique", fontSize=8, leading=10.5, spaceAfter=3)
TBL = TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5),
                  ("FONT", (0, 1), (-1, -1), "Helvetica", 7.5),
                  ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                  ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                  ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.grey),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.3),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 1.3)])


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author=W.AUTHORITY,
                             leftMargin=20 * mm, rightMargin=20 * mm,
                             topMargin=18 * mm, bottomMargin=18 * mm)


def plan(target):
    path = os.path.join(target, "audit_plan_2026.pdf")
    d = _doc(path, "Internal audit plan 2026, section 4")
    f = [Paragraph(W.AUTHORITY, H1),
         Paragraph("Internal audit plan for the year to 31 December 2026: section 4, substantive "
                   "testing", H2),
         Paragraph("Approved by the audit and risk committee on 4 February 2026. Owner: head of "
                   "internal audit. Sections 1 to 3 and 5 to 8 are held separately.", SMALL),
         Spacer(1, 5),
         Paragraph("4.1 Populations", H2),
         Paragraph("Substantive testing covers the capital programme payments population, the "
                   "revenue expenditure population and the payroll population. Each population is "
                   "tested separately and concluded on separately. This section sets the basis for "
                   "the capital programme payments population; the other two are at 4.4 and 4.5 "
                   "and are not reproduced here.", BODY),
         Paragraph("4.2 Capital programme payments", H2),
         Paragraph("Tolerable misstatement for the capital programme payments population is set at "
                   "1,160,000 euro for the year to 31 December 2026, being 2.0 per cent of "
                   "budgeted capital expenditure, and the population is tested to a confidence of "
                   "95 per cent.", BODY),
         Paragraph("4.3 Conclusion on a tested population", H2),
         Paragraph("A population is accepted only where the testing shows, to the confidence at "
                   "4.2, that the population's misstatement does not exceed tolerable "
                   "misstatement. Where the testing does not show that, the population is referred "
                   "for extended testing before the financial statements are certified.", BODY),
         Paragraph("4.6 Reporting", H2),
         Paragraph("The head of internal audit reports the conclusion on each population to the "
                   "audit and risk committee, with the misstatement the testing indicates for the "
                   "population and for each work programme within it, before the statements are "
                   "certified on 30 June 2027.", BODY)]
    d.build(f)
    return path


def manual(target):
    path = os.path.join(target, "audit_manual_part9.pdf")
    d = _doc(path, "Internal audit manual, part 9")
    f = [Paragraph(W.AUTHORITY, H1),
         Paragraph("Internal audit manual: part 9, reporting a tested population", H2),
         Paragraph("Version 6.1, approved 18 November 2025. Owner: head of internal audit. Review "
                   "due November 2028.", SMALL),
         Spacer(1, 5),
         Paragraph("9.1 What a tested population's misstatement means", H2),
         Paragraph("The misstatement of a tested population is the amount by which the "
                   "population's recorded value exceeds the amount properly payable, taken over "
                   "every payment line in the population and over the year in which the line was "
                   "paid. It is an amount of euro and not a count of lines or of invoices. It is "
                   "stated for each work programme and for the authority, each to the nearest "
                   "fifty thousand euro, the authority's figure being the sum of the programme "
                   "figures as stated.", BODY),
         Paragraph("9.2 Records", H2),
         Paragraph("No feed, schedule or register the authority keeps records a population's "
                   "misstatement, and none can: the payment records carry what was paid, not what "
                   "was properly payable, and the testing establishes the difference only for the "
                   "lines tested. The head of internal audit is satisfied each year that the figure "
                   "reported rests on the year's own payment records and the testing performed on "
                   "them.", BODY),
         Paragraph("9.4 Work programmes", H2),
         Paragraph("A population is reported by the work programmes the capital programme register "
                   "carries. Programme codes were last reissued in April 2024 and the register "
                   "carries the codes in force.", BODY),
         Paragraph("9.7 Retention", H2),
         Paragraph("Working papers, the testing schedule and the extracts taken for a population "
                   "are kept for seven years from the end of the year they cover. Extracts are "
                   "pulled once, after the year closes, and are not re-pulled.", BODY)]
    d.build(f)
    return path


def schedule(target, tested):
    """The testing schedule: a table inside a PDF, one row per tested line."""
    path = os.path.join(target, "internal_audit_testing_schedule_2026.pdf")
    d = _doc(path, "Internal audit testing schedule 2026")
    f = [Paragraph(W.AUTHORITY, H1),
         Paragraph("Capital programme payments: testing schedule for the year to 31 December 2026",
                   H2),
         Paragraph("Testing completed %s by %s and reviewed by %s. One row per line tested. "
                   "amount_properly_payable is the amount the testing established was properly "
                   "payable and equals the recorded amount where the testing found nothing."
                   % (W.TESTING_DONE, W.SENIOR_AUDITOR, W.HEAD_OF_AUDIT), SMALL),
         Spacer(1, 4)]
    head = ["schedule_ref", "programme_code", "paid_date", "amount_recorded",
            "amount_properly_payable", "finding"]
    rows = [head]
    for t in tested:
        rows.append([t["schedule_ref"], t["code"], t["day"].isoformat(),
                     "%0.2f" % t["amount"], "%0.2f" % t["payable"], t["finding"]])
    per = 42
    for i in range(0, len(rows) - 1, per):
        chunk = [head] + rows[1 + i:1 + i + per]
        f.append(Table(chunk, colWidths=[38 * mm, 18 * mm, 20 * mm, 25 * mm, 30 * mm, 36 * mm],
                       style=TBL))
        f.append(Spacer(1, 3))
    d.build(f)
    return path
