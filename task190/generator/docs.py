"""The bank's governing documents and the contract register."""
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


def wrap(rows):
    return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm)


def framework(target):
    path = os.path.join(target, "financial_crime_framework.pdf")
    d = _doc(path, "Financial crime framework")
    f = [Paragraph("%s: financial crime framework" % W.BANK, H1),
         Paragraph("Approved by the board risk committee, 19 November 2026. Issued under the bank's "
                   "obligations to %s. Parts 1, 3, 4, 5, 7 and 8 and the appendices are not "
                   "reproduced in this extract." % W.SUPERVISOR, SMALL),
         Paragraph("Part 2 Cases", H2),
         Paragraph("2.1 The bank maintains a register of the financial crime cases it has confirmed, "
                   "with the business line the customer was served by, the typology, and the months "
                   "the investigation establishes under the investigation handbook.", BODY),
         Paragraph("2.2 A case is confirmed when the head of financial crime accepts the "
                   "investigation's finding. The register holds every version of a case the bank has "
                   "issued, and the latest version is the case.", BODY),
         Paragraph("2.3 A case is one customer and one typology. Activity by one customer under two "
                   "typologies is two cases; activity by two customers under one typology is two "
                   "cases, whatever the alerts that led to them.", BODY),
         Paragraph("2.4 The business line of a case is the line that serves the customer. Where the "
                   "bank has reorganised its lines, the line structure register carries each line "
                   "the records name and the line it now forms part of, with the dates each was in "
                   "force.", BODY),
         Paragraph("Part 6 The specialist review", H2),
         Paragraph("6.1 The bank engages a specialist review each year under contract ARW/FC/2024. "
                   "The review works in the business lines the committee places it with, for the "
                   "period the contract sets.", BODY),
         Paragraph("6.2 The review is placed with the business lines expected to be carrying the most "
                   "cases that have begun and that no one at the bank has yet seen at the review "
                   "date, counting one case per customer per typology as paragraph 2.3 defines it. A "
                   "case is no longer within this count once anyone at the bank has seen the activity "
                   "it is about, which is the first seen month the investigation handbook defines, "
                   "and not once it is confirmed. A case that has begun and that no one has yet seen "
                   "is within this count whether or not the bank yet holds a record of it, and the "
                   "expectation is taken over the cases the line's own closed record implies.", BODY),
         Paragraph("6.3 A line's closed record is its cases whose activity began between 1 January "
                   "2021 and 31 January 2024. The bank's look-back review of those months is "
                   "complete, and no case that began in them is still to be detected.", BODY),
         Paragraph("6.4 The review covers three business lines. The committee places it on the "
                   "assessment the head of financial crime puts to it.", BODY),
         Paragraph("6.5 The head of financial crime reports to the committee each quarter the cases "
                   "the bank confirmed in the two complete quarters before the report, by business "
                   "line.", BODY),
         Paragraph("Part 9 Records", H2),
         Paragraph("9.1 The bank keeps the alert system's record of every alert and of each stage of "
                   "its adjudication, and the case register, and reconciles the two through the "
                   "customer identifier crosswalk.", BODY),
         Paragraph("9.2 The bank does not maintain a ranking of its business lines for any purpose "
                   "under this framework.", BODY)]
    d.build(f)
    return path


def handbook(target):
    path = os.path.join(target, "investigation_handbook.pdf")
    d = _doc(path, "Investigation handbook")
    f = [Paragraph("%s: investigation handbook, dating a case" % W.BANK, H1),
         Paragraph("Financial crime operations, issue 7. The months every confirmed case carries.", SMALL),
         Paragraph("The onset month", H2),
         Paragraph("The onset month is the month in which the activity the case is about began. The "
                   "investigator establishes it from the account record after the case is opened, and "
                   "it is often well before anything was noticed. It is not the month an alert fired "
                   "and not the month the case was opened.", BODY),
         Paragraph("The first seen month", H2),
         Paragraph("The first seen month is the month in which anyone at the bank first saw the "
                   "activity the case is about, whether through an alert, a customer's dispute, a "
                   "counterparty enquiry, a document review or a report from outside the bank. Where "
                   "several of these happened, it is the earliest.", BODY),
         Paragraph("The confirmed month", H2),
         Paragraph("The confirmed month is the month the head of financial crime accepted the "
                   "finding. It follows the first seen month by the time the investigation took.", BODY),
         Paragraph("Notes", H2),
         Paragraph("All three months are recorded for every confirmed case. An amendment to a case "
                   "may change the amount or the typology and does not change any of the three "
                   "months.", BODY),
         Paragraph("Cases differ widely in how they come to light. A card or payment case is "
                   "ordinarily seen when the customer disputes a transaction. A trade finance or "
                   "correspondent case is seen when a document review, a counterparty enquiry or a "
                   "report from outside the bank reaches it.", BODY)]
    d.build(f)
    return path


def dictionary(target):
    path = os.path.join(target, "extract_dictionary.pdf")
    d = _doc(path, "Extract dictionary")
    rows = [["Field", "Meaning"],
            ["case_id", "the register's identifier for a case"],
            ["customer_ref", "the customer as the case system codes them; the crosswalk carries the "
                             "alert system's own reference for the same customer"],
            ["line_code", "the business line code the record carried when it was written; the line "
                          "structure register carries the line it now forms part of"],
            ["typology", "the financial crime typology the case was confirmed under"],
            ["onset_month, first_seen_month, confirmed_month", "the three months the investigation "
                                                               "handbook defines"],
            ["disposition", "confirmed for a case the head of financial crime has accepted"],
            ["record_version", "the version of the case record; a later version supersedes an earlier"],
            ["amount", "the amount at issue, in the currency of the currency field"],
            ["alert_id, queue, stage, stage_at", "an alert, the queue it was raised in, the "
                                                 "adjudication stage and the date that stage was reached"],
            ["outcome", "closed or escalated at triage; with investigations once escalated"],
            ["batch_id", "the load batch the alert rows arrived in"],
            ["alerts_awaiting_review", "alerts in the queue that no analyst has yet opened, at the "
                                       "week ending date"]]
    f = [Paragraph("%s: extract dictionary" % W.BANK, H1),
         Paragraph("The fields of the case register, the alert extract and the weekly backlog, as the "
                   "data office maintains them.", SMALL)]
    t = Table(wrap(rows), colWidths=[52 * mm, 122 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("Notes", H2))
    f.append(Paragraph("A case row is one version of one case. An alert row is one stage of one "
                       "alert, so an alert that was escalated has three rows.", BODY))
    f.append(Paragraph("The card disputes queue was called chargebacks before April 2026. The queue "
                       "field carries the name in use when the alert was raised.", BODY))
    f.append(Paragraph("A load batch that was re-sent carries the original batch identifier with an R "
                       "suffix. Both loads are in the extract.", BODY))
    d.build(f)
    return path


def contract(target):
    path = os.path.join(target, "contract_register.pdf")
    d = _doc(path, "Contract register")
    f = [Paragraph("%s: contract register, ARW/FC/2024" % W.BANK, H1),
         Paragraph("The specialist review contract with %s, as varied. Held by procurement." % W.CONTRACTOR,
                   SMALL),
         Paragraph("Hours allowed", H2)]
    rows = [["Quarter", "Hours allowed", "Varied by"],
            ["2026-Q1", "420.0", "original schedule"],
            ["2026-Q2", "420.0", "original schedule"],
            ["2026-Q3", "480.0", "variation 2 of 14 June 2026"],
            ["2026-Q4", "480.0", "variation 2 of 14 June 2026"]]
    t = Table(wrap(rows), colWidths=[34 * mm, 34 * mm, 72 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("Rate card", H2))
    rows = [["Work type", "Rate an hour", "In force from"],
            ["review", "285.00", "1 January 2024"],
            ["expert testimony", "410.00", "1 January 2024"],
            ["credit note", "285.00", "1 January 2024"]]
    t = Table(wrap(rows), colWidths=[42 * mm, 34 * mm, 64 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("Notes", H2))
    f.append(Paragraph("A ticket billed at a rate other than the rate card's review rate is outside "
                       "the rate card and is listed separately in the quarterly reconciliation.", BODY))
    f.append(Paragraph("A credit note reverses hours already billed. Where the contractor has "
                       "reissued a credit note under the credit note reference series, the ledger "
                       "holds the ticket under both references and the hours are owed once.", BODY))
    d.build(f)
    return path
