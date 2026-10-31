"""The pack's documents: the partner agreement's Schedule B with Exhibit 1 (each partner's 2026 target), Keswold's
extract dictionary, the Fund's data notes, Corvane's claims file layout and the Fund's stop-loss policy summary."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d1f21")
GREY = colors.HexColor("#5a5f66")

BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=7)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=28, firstLineIndent=-28)
SUBNUM = ParagraphStyle("subnum", parent=BODY, leftIndent=46, firstLineIndent=-18)
H1 = ParagraphStyle("h1", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17, textColor=INK, spaceAfter=4,
                    alignment=1)
SUB = ParagraphStyle("sub", fontName="LiberationSerif", fontSize=10, leading=13, textColor=GREY, spaceAfter=14, alignment=1)
H2 = ParagraphStyle("h2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.6 * inch, footer)
        canvas.drawRightString(LETTER[0] - 1.0 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                          bottomMargin=0.95 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head=True):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaed") if head else colors.white),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


# ------------------------------------------------------------------------------------------------- Schedule B
def write_schedule_b(path, targets, group_npi):
    title = "Accountable Care Partner Agreement, Schedule B: Annual Reconciliation"
    doc, frame = _doc(path, title, W.FUND, "%s  |  Accountable Care Partner Agreement  |  Schedule B (2026 edition)" % W.FUND)
    s = [Paragraph("ACCOUNTABLE CARE PARTNER AGREEMENT", H1),
         Paragraph("Schedule B: Annual Reconciliation (2026 edition)<br/>Common to the Fund's agreements with each partner "
                   "group listed in Exhibit 1. Adopted by the Board of Trustees on 18 November 2025.", SUB)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;&nbsp;%s" % (n, t), NUM))
    M = lambda n, t: s.append(Paragraph("(%s)&nbsp;&nbsp;%s" % (n, t), SUBNUM))
    s.append(Paragraph("B.1 Definitions", H2))
    N("B.1.1", "<i>Performance Year</i> means a calendar year. This edition applies to the Performance Year 2026.")
    N("B.1.2", "<i>Member</i> means a participant or dependent eligible for medical benefits under the Fund's Plan of "
               "Benefits in the month concerned.")
    N("B.1.3", "<i>Attributed Member Month</i> means a month in which a Member is eligible for the Fund's medical benefits "
               "and appears on the Fund's attribution roster for the Partner for that month. The roster is run on the "
               "first day of each month and attributes each Member to the partner group of the Member's primary care "
               "provider of record on that day.")
    N("B.1.4", "<i>Total Cost of Care</i> means the Fund's paid amount for covered medical services (professional services "
               "and outpatient and inpatient facility services) with a first date of service in the Performance Year, for "
               "Members attributed to the Partner in the month of that first date of service, whenever the claims are paid. "
               "Outpatient prescription drugs dispensed by retail, mail-order and specialty pharmacies are excluded.")
    N("B.1.5", "Where a Member's amount under B.1.4 for the Performance Year exceeds $200,000, the amount above $200,000 is "
               "excluded. For a Member attributed to more than one partner group during the year, the excluded amount is "
               "shared in proportion to the Member's amounts with each.")
    N("B.1.6", "<i>TCOC PMPM</i> means the Partner's Total Cost of Care for the Performance Year, after B.1.5, divided by "
               "its Attributed Member Months for the year.")
    s.append(Paragraph("B.2 Shared savings and shared losses", H2))
    N("B.2.1", "If the Partner's TCOC PMPM exceeds its Target PMPM in Exhibit 1 by more than 2.0 per cent, the Partner pays "
               "the Fund a shared-loss payment of 40 per cent of the amount by which its TCOC PMPM exceeds its Target PMPM, "
               "multiplied by its Attributed Member Months, but not more than 4 per cent of its Target PMPM multiplied by "
               "its Attributed Member Months.")
    N("B.2.2", "If the Partner's TCOC PMPM is below its Target PMPM by more than 2.0 per cent and its quality score for the "
               "Performance Year is 70 points or more, the Fund pays the Partner a shared-savings payment of 40 per cent "
               "of the amount by which its TCOC PMPM is below its Target PMPM, multiplied by its Attributed Member Months, "
               "on the same limit.")
    N("B.2.3", "The comparisons in B.2.1 and B.2.2 are made on unrounded figures.")
    s.append(Paragraph("B.3 Reconciliation", H2))
    N("B.3.1", "Within 60 days after the end of the Performance Year the Fund issues each Partner a reconciliation from "
               "the claims its claims administrator has paid through the last business day of January following the "
               "year. The Fund estimates the claims incurred in the Performance Year and not yet paid from its claims data.")
    N("B.3.2", "A shared-loss or shared-savings payment under B.2 is due within 45 days after the reconciliation is issued.")
    N("B.3.3", "When twelve months of claims after the Performance Year have been paid, the Fund issues a final "
               "reconciliation on the claims then paid, and any difference from the payment under B.3.2 is settled.")
    s.append(Paragraph("B.4 The reconciliation report", H2))
    N("B.4.1", "For information, the reconciliation also reports for each Partner:")
    M("a", "the Fund's pharmacy spending for its Members: the Fund's net payments to its pharmacy benefit manager for "
           "prescriptions filled in the Performance Year in the Members' Attributed Member Months with the Partner, "
           "reversals included whenever processed; and")
    M("b", "the share of the Fund's paid amount for the professional services in its Total Cost of Care, before B.1.5 "
           "and as paid through the reconciliation date, that was for services rendered by clinicians who were not with "
           "the Partner group when the service was given.")
    s.append(Spacer(1, 6))
    s.append(Paragraph("Exhibit 1: Partner groups and Target PMPM, Performance Year 2026", H2))
    rows = [["Partner group", "Partner code", "Group NPI", "Target PMPM (USD)"]]
    for code in W.CODES:
        rows.append([W.NAME[code], code, group_npi[code], "{:,.2f}".format(targets[code])])
    s.append(_table(rows, [2.6 * inch, 0.9 * inch, 1.2 * inch, 1.4 * inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Target PMPM: as set for 2026 in Schedule A of each Partner's agreement. Group NPI: the "
                       "Partner group's organisational NPI.", SMALL))
    s.append(Spacer(1, 14))
    s.append(Paragraph("For the Board of Trustees: %s, %s." % W.PEOPLE["chair"], BODY))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------- Keswold dictionary
# ----------------------------------------------------------------------------------------- the Fund's data notes
# --------------------------------------------------------------------------------------------- Corvane layout
# --------------------------------------------------------------------------------------------- stop-loss summary
def write_stop_loss(path):
    title = "Specific stop-loss policy summary, 2026"
    doc, frame = _doc(path, title, W.FUND, "%s  |  Stop-loss policy summary 2026" % W.FUND)
    s = [Paragraph("SPECIFIC STOP-LOSS INSURANCE: POLICY SUMMARY", H1),
         Paragraph("Policy year 1 January to 31 December 2026. Carrier: %s. Policyholder: %s." % (W.STOP_LOSS_CARRIER, W.FUND), SUB)]
    rows = [["Term", "Provision"],
            ["Specific deductible", "$175,000 per covered person per policy year"],
            ["Contract basis", "12/15: claims incurred in the policy year and paid from 1 January 2026 to 31 March 2027"],
            ["Covered expenses", "medical claims and outpatient prescription drugs paid by the Plan"],
            ["Reimbursement", "100 per cent of covered expenses above the specific deductible, on submission of proof "
                              "of payment"],
            ["Aggregate coverage", "none"]]
    s.append(_table(rows, [1.8 * inch, 4.7 * inch]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Reimbursements are credited to the Plan's claims account when received. This summary does not "
                       "change the policy's terms.", BODY))
    s.append(Paragraph("Prepared by %s, %s, December 2025." % W.PEOPLE["controller"], BODY))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- code values
CODE_VALUES = [   # the Fund Office's reference list of the codes in its claims, pharmacy and eligibility feeds
    ("Keswold medical claims", "claim_form", "CMS1500", "Professional claim"),
    ("Keswold medical claims", "claim_form", "UB04", "Facility claim"),
    ("Keswold medical claims", "claim_frequency_code", "1", "Original (Tallis)"),
    ("Keswold medical claims", "claim_frequency_code", "7", "Replacement (Tallis)"),
    ("Keswold medical claims", "claim_frequency_code", "8", "Void (Tallis)"),
    ("Keswold medical claims", "claim_frequency_code", "O", "Original (legacy system)"),
    ("Keswold medical claims", "claim_frequency_code", "A", "Adjustment, a replacement (legacy system)"),
    ("Keswold medical claims", "claim_frequency_code", "V", "Void (legacy system)"),
    ("Keswold medical claims", "claim_status", "P", "Paid"),
    ("Keswold medical claims", "claim_status", "D", "Denied"),
    ("Keswold medical claims", "claim_status", "V", "Voided"),
    ("Corvane pharmacy claims", "transaction_code", "B1", "Claim"),
    ("Corvane pharmacy claims", "transaction_code", "B2", "Reversal: carries the amounts of the claim it reverses"),
    ("Corvane pharmacy claims", "transaction_code", "B3", "Rebill: replaces a reversed claim"),
    ("Corvane pharmacy claims", "relationship_code", "1", "Cardholder"),
    ("Corvane pharmacy claims", "relationship_code", "2", "Spouse"),
    ("Corvane pharmacy claims", "relationship_code", "3", "Dependent"),
    ("Corvane pharmacy claims", "person_code", "01", "Cardholder"),
    ("Corvane pharmacy claims", "person_code", "02", "Spouse"),
    ("Corvane pharmacy claims", "person_code", "03 and up", "Dependents in order of date of birth, eldest first"),
    ("Fund eligibility", "relationship_code", "P", "Participant"),
    ("Fund eligibility", "relationship_code", "S", "Spouse"),
    ("Fund eligibility", "relationship_code", "D", "Dependent child"),
    ("Fund eligibility", "change_reason", "NE", "New enrollee"),
    ("Fund eligibility", "change_reason", "HB", "Hour bank"),
    ("Fund eligibility", "change_reason", "RI", "Reinstated after late contributions"),
    ("Fund eligibility", "change_reason", "RT", "Retroactive termination"),
]


def write_code_values(path):
    import csv
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["source", "field", "code", "meaning"])
        w.writerows(CODE_VALUES)


def write_tallis_notice(path):
    title = "Client notice CN-2026-14: moving your claims to Tallis"
    name, role = W.PEOPLE["tpa"]
    doc, frame = _doc(path, title, W.TPA, "%s  |  Client notice CN-2026-14" % W.TPA)
    s = [Paragraph("CLIENT NOTICE CN-2026-14", H1),
         Paragraph("%s, 15 September 2026. To: %s (group 4417)." % (W.TPA, W.FUND), SUB),
         Paragraph("Moving your claims to Tallis", H2),
         Paragraph("From Monday 5 October 2026 we adjudicate the Fund's medical claims on our Tallis platform in place of "
                   "our legacy claims system. Claims received before 5 October and not yet paid will be adjudicated on "
                   "Tallis from that date. Claim numbers are unchanged, and your monthly client extract keeps its layout "
                   "and its run date.", BODY),
         Paragraph("What changes in your extract", H2),
         Paragraph("Claim versions processed on Tallis carry the standard claim frequency codes (1 original, 7 "
                   "replacement, 8 void) in place of the legacy system's codes (O original, A adjustment, V void). Versions "
                   "processed before 5 October keep their legacy codes. Nothing else changes: as before, a claim keeps its "
                   "claim number through every version, a replacement carries the claim's full corrected amounts and a "
                   "void carries zero amounts, so a claim's value is the paid amount of its latest version.", BODY),
         Paragraph("Questions to %s, %s." % (name, role), BODY)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
