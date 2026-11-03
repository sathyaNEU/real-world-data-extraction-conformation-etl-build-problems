"""The governing documents, each in its organisation's own genre: the Ministry's Budget 2027 regional bid
instructions (the measure the bid is assessed on, the shortlist with scope and cost, the cost bases), the Department
of Corrections' EM bail address assessment service standard, and the bail support contract's schedule of service
measures. None of them describes a file, a field or how a figure is computed beyond the quantity it defines."""
import os

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP

rl_config.invariant = 1

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13.2, alignment=TA_LEFT, spaceAfter=5)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.4, leading=11)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=10.6, leading=14, spaceBefore=7,
                    spaceAfter=3)
META = ParagraphStyle("meta", parent=BODY, fontSize=8.6, leading=11.5, textColor=colors.HexColor("#444444"))


def _pdf(path, story, title, author, created, modified):
    PP.word_pdf_info()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=PP.WORD_PDF,
                            producer=PP.WORD_PDF)
    doc.build(story)
    PP.normalize_pdf(path, created, modified)


def _table(rows, widths):
    t = Table([[Paragraph(str(c), SMALL) for c in r] for r in rows], colWidths=[w * mm for w in widths],
              repeatRows=1)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8ecef")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa4ab")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def bid_instructions(path):
    s = [Paragraph("Budget 2027: regional bid instructions", H1),
         Paragraph("Criminal court operations, Halsey Coast region", H2),
         Paragraph("Ministry of Justice, Regional Operations. Issued 12 October 2026. Bids close 20 November 2026.",
                   META), Spacer(1, 4),
         Paragraph("1. Purpose", H2),
         Paragraph("Each region puts forward one initiative from the shortlist in section 4 for the Minister's "
                   "Budget 2027 justice package. The region's bid names the initiative, the case for it on the "
                   "measure in section 3, and the cost bases in section 5. A bid that puts forward more than one "
                   "initiative is returned.", BODY),
         Paragraph("2. Timetable", H2),
         Paragraph("Bids close on 20 November 2026. Regional managers present their bids to the Deputy Secretary on "
                   "2 December 2026, and the Minister's package is settled in February 2027. Funded initiatives "
                   "start on 1 July 2027.", BODY),
         Paragraph("3. The measure", H2),
         Paragraph("Each bid is assessed on one measure: the gap in custody remands at first appearance. For each "
                   "year to 30 September, take every first appearance from police custody heard at the region's four "
                   "District Courts (Kestrel Bay, Dunmore, Ashgrove and Thornmere), each counted once, on its New "
                   "Zealand date. All of them are decided on the day they are heard. The share remanded in custody "
                   "is the share of those first appearances that end with the defendant remanded in custody, "
                   "whatever else the court ordered; a first appearance that ends in a sentence or any other outcome "
                   "stays in the count and is not a remand in custody. The gap is that share for defendants with no "
                   "lawyer of record at that appearance minus the share for defendants with a lawyer of record at "
                   "that appearance, in percentage points.", BODY),
         Paragraph("The region's bid compares the year to 30 September 2026 with the year to 30 September 2025 and "
                   "puts forward the initiative that removes the change in the gap between them.", BODY),
         Paragraph("4. The shortlist", H2),
         _table([["Initiative", "Owner", "Scope", "Annual cost (NZD)"],
                 ["EM bail assessment capacity", "Department of Corrections, EM Bail Unit",
                  "Two additional address assessors for the region's courts", "240,000"],
                 ["A judge on the Kestrel Bay custody list", "Ministry of Justice, District Court operations",
                  "A District Court judge presiding over the Kestrel Bay custody list on every sitting day",
                  "620,000"],
                 ["Duty lawyer roster", "Ministry of Justice, Legal Aid Services",
                  "A second rostered duty lawyer at Kestrel Bay District Court on every sitting day", "210,000"],
                 ["Supported bail accommodation", "Coastline Bail Support Trust (contracted)",
                  "Four further beds across the two bail houses", "330,000"],
                 ["Court-date text reminders", "Ministry of Justice, Courts Digital",
                  "Reminders for every bailed defendant with a mobile number on file", "90,000"]],
                [52, 46, 52, 20]),
         Spacer(1, 4),
         Paragraph("5. Cost bases", H2),
         Paragraph("Each shortlist line is costed from its own operating record for the year to 30 September 2026: "
                   "the judge line from the sitting hours in the court sitting calendar; the duty lawyer line from "
                   "the duty lawyer returns; the EM line from the EM Bail Unit's assessments of the District Courts' "
                   "orders, at the turnaround the Department's service standard defines, month by month; the bail "
                   "house line from occupied nights "
                   "as the support contract's schedule defines them, month by month; the reminder line from the "
                   "reminder service log.", BODY),
         Paragraph("6. Contacts", H2),
         Paragraph("Regional Operations, Halsey Coast: Freya Herd, Regional Manager, Criminal Court Operations.",
                   BODY)]
    _pdf(path, s, "Budget 2027 regional bid instructions, Halsey Coast", "Ministry of Justice",
         b"D:20261012091500+13'00'", b"D:20261012091500+13'00'")


def em_standard(path):
    s = [Paragraph("Electronically monitored bail: address assessment service standard", H1),
         Paragraph("Department of Corrections, EM Bail Unit, Halsey Coast. Version 4, effective 3 February 2026 (version 3, 1 July 2025, revised for section 4).", META),
         Spacer(1, 4),
         Paragraph("1. Scope", H2),
         Paragraph("This standard applies to every address assessment the District Courts of the Halsey Coast region "
                   "order before deciding an application for electronically monitored bail.", BODY),
         Paragraph("2. Turnaround", H2),
         Paragraph("An assessment's turnaround runs from the day the court orders the assessment to the day the "
                   "assessment report is filed with the court, counted in calendar days. The turnaround runs to the day the first "
                   "assessment report is filed; an amended report is a later document and does not move that day. A "
                   "court order is one assessment, whatever the number of addresses it names. Assessments are reported "
                   "in the month in which the court ordered them.", BODY),
         Paragraph("3. Target", H2),
         Paragraph("The unit files nine in ten assessment reports within ten calendar days of the court's order.",
                   BODY),
         Paragraph("4. Records", H2),
         Paragraph("From 2 February 2026 the unit records its assessments in the EM case system. Assessments open on "
                   "that day were carried into the case system.", BODY),
         Paragraph("5. Review", H2),
         Paragraph("This standard is reviewed each July.", BODY)]
    _pdf(path, s, "EM bail address assessment service standard", "Department of Corrections",
         b"D:20260203101500+13'00'", b"D:20260203101500+13'00'")


def contract_schedule(path):
    s = [Paragraph("Schedule 2: Service measures", H1),
         Paragraph("Supported bail accommodation agreement between the Ministry of Justice and Coastline Bail Support "
                   "Trust, 1 July 2025 to 30 June 2028.", META), Spacer(1, 4),
         Paragraph("1. Houses", H2),
         Paragraph("The provider runs two bail houses, at Kestrel Bay (eight beds) and Dunmore (six beds), for "
                   "defendants the District Courts bail to them.", BODY),
         Paragraph("2. Placements", H2),
         Paragraph("A placement starts on the first night a resident spends at a house and ends on the day the "
                   "resident leaves it.", BODY),
         Paragraph("3. Payment", H2),
         Paragraph("The Ministry pays a fixed monthly fee for each house and a rate for each occupied night above "
                   "the house's base level.", BODY),
         Paragraph("4. Occupied nights", H2),
         Paragraph("An occupied night is a night a resident spends at a bail house. A night is dated by the evening "
                   "it begins and is occupied when the resident is at the house at midnight. Nights a resident spends "
                   "in police custody or in hospital are not occupied nights, although the bed is held for the "
                   "resident, and a night away on approved leave or absent without leave is not a night at the "
                   "house. A placement's first "
                   "night is the night the resident arrives at the house and its last is the night before the "
                   "resident leaves; a booking or register entry made before the resident arrives or after the "
                   "resident leaves neither starts nor extends a placement.", BODY),
         Paragraph("5. Reporting", H2),
         Paragraph("The provider reports occupied nights for each house by calendar month.", BODY)]
    _pdf(path, s, "Supported bail accommodation, Schedule 2", "Ministry of Justice",
         b"D:20250630150000+12'00'", b"D:20250630150000+12'00'")


def build_docs(out):
    bid_instructions(os.path.join(out, "budget2027_bid_instructions_halsey_coast.pdf"))
    em_standard(os.path.join(out, "em_bail_service_standard_v4.pdf"))
    contract_schedule(os.path.join(out, "bail_support_contract_schedule2.pdf"))
