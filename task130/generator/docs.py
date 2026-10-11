"""The pack's documents, each in its own organisation's voice: the services agreement excerpt (recitals and
Schedule C), the consulting actuary's renewal letter, the stop-loss policy schedule, Northcourt's three
stratification exports, Quarrystone's rebate statement and the analyst's field dictionary."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

import containers as C
import world as W

# ------------------------------------------------------------------ shared pdf styles
BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=10.5, spaceAfter=3)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Times-Bold", fontSize=12.5, leading=15, alignment=TA_CENTER, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Times-Bold", fontSize=10.5, leading=13.5, spaceBefore=6, spaceAfter=4)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=18, firstLineIndent=-18)
SUB = ParagraphStyle("sub", parent=BODY, leftIndent=36, firstLineIndent=-18)

SANS = ParagraphStyle("sans", fontName="Helvetica", fontSize=9.6, leading=12.6, spaceAfter=6)
SANS_SM = ParagraphStyle("sans_sm", parent=SANS, fontSize=8, leading=10, spaceAfter=2)
SANS_B = ParagraphStyle("sans_b", parent=SANS, fontName="Helvetica-Bold")
SANS_R = ParagraphStyle("sans_r", parent=SANS, alignment=TA_RIGHT)


def money(x, cents=False):
    return ("$%s" % format(x, ",.2f")) if cents else ("$%s" % format(int(round(x)), ","))


def build_pdf(path, story, title, author, creator, producer, when, onpage=None, margins=(0.9, 0.9, 0.85, 0.8)):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=margins[0] * inch, rightMargin=margins[1] * inch,
                            topMargin=margins[2] * inch, bottomMargin=margins[3] * inch, title=title, author=author,
                            subject="", creator=creator, producer=producer, invariant=1)
    if onpage:
        doc.build(story, onFirstPage=onpage, onLaterPages=onpage)
    else:
        doc.build(story)
    C.pdf_stamp(path, when)


def grid(data, widths, header=True, align_right_from=1, font="Helvetica", size=8.6, zebra=False):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("FONT", (0, 0), (-1, -1), font, size), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("ALIGN", (align_right_from, 0), (-1, -1), "RIGHT")]
    if header:
        st.append(("FONT", (0, 0), (-1, 0), font + "-Bold" if font == "Helvetica" else "Times-Bold", size))
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F2F2F2")))
    t.setStyle(TableStyle(st))
    return t


# ------------------------------------------------------------------ the agreement excerpt
def agreement_pdf(path):
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8.5)
        canvas.drawString(0.9 * inch, 0.5 * inch, "Agreement No. RCV-2027-014")
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()

    s = []
    s.append(Paragraph("CARE MANAGEMENT SERVICES AGREEMENT", H1))
    s.append(Paragraph("between Independent School District No. 2817 (Red Cedar Valley Schools), Minnesota,<br/>"
                       "and Northcourt Care Partners, LLC", CENTER))
    s.append(Paragraph("Agreement No. RCV-2027-014", CENTER))
    s.append(Spacer(1, 6))
    s.append(Paragraph("<i>Excerpt for the District's benefits file: Recitals and Schedule C. The body of the Agreement and "
                       "Schedules A (Services), B (Administrative Fees), D (Data Exchange) and E (Business Associate "
                       "Agreement) are held by the Business Office.</i>", SMALL))
    s.append(Spacer(1, 8))
    s.append(Paragraph("RECITALS", H2))
    rec = [
        ("A.", "The District sponsors the Red Cedar Valley Schools Employee Health Plan (the \"Plan\"), a self-insured "
               "group health plan for eligible employees, early retirees under age 65 and their dependents. Ellery Benefit "
               "Administrators administers medical claims under the Plan and Quarrystone Rx administers pharmacy claims."),
        ("B.", "On 13 January 2025 the District issued Request for Proposals 2025-07 for high-cost care management "
               "services for a programme year beginning 1 April 2025. Northcourt submitted a proposal on 28 February 2025 "
               "and on 18 March 2025 the School Board approved a recommendation to award the contract to Northcourt, "
               "subject to an agreement."),
        ("C.", "On 8 April 2025, before any agreement was signed, the School Board suspended the award under the "
               "District's budget freeze for the 2025-26 fiscal year. No agreement was executed under RFP 2025-07 and "
               "Northcourt provided no services to Plan members before the Effective Date."),
        ("D.", "On 9 February 2027 the School Board authorised the Superintendent to enter into this Agreement with "
               "Northcourt for the Programme Year on the terms set out below."),
    ]
    for k, t in rec:
        s.append(Paragraph("%s&nbsp;&nbsp;%s" % (k, t), CLAUSE))
    s.append(Paragraph("NOW, THEREFORE, in consideration of the mutual promises in this Agreement, the District and "
                       "Northcourt agree as follows.", BODY))
    s.append(Spacer(1, 4))
    s.append(Paragraph("<i>[Sections 1 to 14 of the Agreement not reproduced.]</i>", SMALL))
    s.append(PageBreak())
    s.append(Paragraph("SCHEDULE C", H1))
    s.append(Paragraph("BASELINE AND SAVINGS", H1))
    s.append(Spacer(1, 6))
    s.append(Paragraph("C.1&nbsp;&nbsp;<b>Definitions.</b> In this Schedule:", CLAUSE))
    defs = [
        ("(a)", "\"Allowed Claims\" means the allowed amount of medical and pharmacy claims for covered services to a "
                "member, including the member's deductible, copayment and coinsurance. Pharmacy claims are taken before "
                "manufacturer rebates. Claims are taken net of replacement claims, voided claims and pharmacy reversals. "
                "No deduction is made for reimbursements under the District's stop-loss insurance. A medical claim is "
                "incurred on its first date of service and a pharmacy claim on its date of fill."),
        ("(b)", "\"Member Month\" means a calendar month in which a member is enrolled in the Plan on the first day of "
                "the month."),
        ("(c)", "\"Data Cut-Off Date\" means 28 February 2027."),
        ("(d)", "\"Final Enrolment List\" means the list of members delivered by Northcourt under Section 3.2 on claims "
                "paid through the Data Cut-Off Date. \"Enrolled Members\" means the members on the Final Enrolment List, "
                "and a member's \"Risk Tier\" is the tier assigned to the member on that list."),
        ("(e)", "\"Programme\" means the Services described in Schedule A, and \"Programme Year\" means the twelve "
                "months from 1 April 2027 to 31 March 2028."),
        ("(f)", "\"Trend Factor\" means the annual medical and pharmacy trend rates adopted in the District's most "
                "recent renewal of Plan funding rates."),
        ("(g)", "\"Baseline PMPM\" means, for each Risk Tier and separately for medical and for pharmacy Allowed Claims, "
                "the Allowed Claims per Member Month that the Enrolled Members in that Risk Tier would be expected to "
                "incur in the Programme Year in the absence of the Programme. Experience from an earlier period that is "
                "used to determine a Baseline PMPM is projected by multiplying it by one plus the Trend Factor, raised to "
                "the power of the number of months from the midpoint of that period to the midpoint of the Programme "
                "Year divided by twelve."),
        ("(h)", "\"Programme Baseline\" means the Baseline PMPMs averaged across the Risk Tiers, weighted by the number "
                "of Enrolled Members in each Risk Tier, for medical, for pharmacy and in total."),
        ("(i)", "\"Actual PMPM\" means, for each Risk Tier and separately for medical and for pharmacy, the Enrolled "
                "Members' Allowed Claims incurred in the Programme Year and paid by 30 June 2028, divided by their "
                "Member Months in the Programme Year."),
    ]
    for k, t in defs:
        s.append(Paragraph("%s&nbsp;&nbsp;%s" % (k, t), SUB))
    s.append(Paragraph("C.2&nbsp;&nbsp;<b>Certification.</b> Before the start of the Programme Year the District will "
                       "certify to Northcourt in writing, following approval by the School Board, the Baseline PMPM for "
                       "each Risk Tier and benefit and the Programme Baseline. The certification will also show, for each "
                       "Risk Tier, the number of Enrolled Members and their Allowed Claims per Member Month for calendar "
                       "year 2026 as paid through the Data Cut-Off Date, without completion. Amounts are stated in whole "
                       "dollars and no amount is rounded before the final figure.", CLAUSE))
    s.append(Paragraph("C.3&nbsp;&nbsp;<b>Savings.</b> For each Risk Tier and benefit, Savings equal the Baseline PMPM "
                       "less the Actual PMPM, multiplied by the Enrolled Members' Member Months in the Programme Year in "
                       "that Risk Tier. Programme Savings are the sum of Savings across Risk Tiers and benefits; a negative "
                       "result for one Risk Tier or benefit reduces the total.", CLAUSE))
    s.append(Paragraph("C.4&nbsp;&nbsp;<b>Shared Savings Fee.</b> Northcourt is entitled to 40 per cent of Programme "
                       "Savings, if positive, up to a maximum of $900,000 for the Programme Year. The Shared Savings Fee "
                       "is in addition to the administrative fee in Schedule B and is payable within 45 days after the "
                       "reconciliation becomes final.", CLAUSE))
    s.append(Paragraph("C.5&nbsp;&nbsp;<b>Reconciliation.</b> The District will deliver to Northcourt a reconciliation of "
                       "Programme Savings by 31 August 2028, on claims paid through 30 June 2028, with the member-level "
                       "detail Northcourt reasonably needs to check it.", CLAUSE))
    s.append(Paragraph("C.6&nbsp;&nbsp;<b>Disputes.</b> Either party may dispute the certification under C.2 or the "
                       "reconciliation under C.5 by written notice within 30 days of receiving it. A dispute the parties "
                       "do not settle within a further 30 days will be referred to an independent actuary who is a Fellow "
                       "of the Society of Actuaries and a Member of the American Academy of Actuaries, appointed jointly "
                       "by the parties. The actuary's determination is final and binding, and the parties share the "
                       "actuary's fees equally.", CLAUSE))
    s.append(Paragraph("C.7&nbsp;&nbsp;<b>Plan changes.</b> If the District changes Plan benefits during the Programme "
                       "Year, the parties will adjust the affected Baseline PMPMs in good faith to reflect the change.", CLAUSE))
    s.append(Spacer(1, 14))
    sig = [["INDEPENDENT SCHOOL DISTRICT NO. 2817", "NORTHCOURT CARE PARTNERS, LLC"],
           ["", ""],
           ["By: Sandra Lopez", "By: Phillip Alvarado"],
           ["Superintendent", "Chief Operating Officer"],
           ["Date: 16 February 2027", "Date: 16 February 2027"]]
    t = Table(sig, colWidths=[3.3 * inch, 3.3 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Times-Roman", 10), ("FONT", (0, 0), (-1, 0), "Times-Bold", 10),
                           ("LINEABOVE", (0, 2), (0, 2), 0.5, colors.black), ("LINEABOVE", (1, 2), (1, 2), 0.5, colors.black),
                           ("TOPPADDING", (0, 1), (-1, 1), 14)]))
    s.append(KeepTogether([t]))
    build_pdf(path, s, "Care Management Services Agreement RCV-2027-014 (excerpt)", "Business Office",
              "Microsoft\xae Word for Microsoft 365", "Microsoft\xae Word for Microsoft 365",
              dt.datetime(2027, 2, 17, 10, 42, 18), onpage=page)


# ------------------------------------------------------------------ the renewal letter
def renewal_pdf(path, F):
    """F: figures computed from the shipped extracts at the letter's paid-through date (see estimators.letter_figures)"""
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 11)
        canvas.setFillColor(colors.HexColor("#1F3B57"))
        canvas.drawString(0.95 * inch, letter[1] - 0.6 * inch, "LINDQVIST")
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.95 * inch, letter[1] - 0.75 * inch, "Benefits Consulting")
        canvas.drawRightString(letter[0] - 0.95 * inch, letter[1] - 0.6 * inch, "80 South Eighth Street, Suite 2210")
        canvas.drawRightString(letter[0] - 0.95 * inch, letter[1] - 0.73 * inch, "Minneapolis, MN 55402")
        canvas.setFillColor(colors.black)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.95 * inch, 0.5 * inch, "Red Cedar Valley Schools, 2027-28 renewal")
        canvas.drawRightString(letter[0] - 0.95 * inch, 0.5 * inch, "%d" % doc.page)
        canvas.restoreState()

    s = [Spacer(1, 14)]
    s.append(Paragraph("26 February 2027", SANS))
    s.append(Paragraph("Joyce Salinas<br/>Director of Risk Management and Benefits<br/>Red Cedar Valley Schools", SANS))
    s.append(Paragraph("cc: Anthony Olsen, Chief Financial Officer", SANS_SM))
    s.append(Spacer(1, 4))
    s.append(Paragraph("<b>Re: Employee Health Plan, funding rates for the plan year 1 July 2027 to 30 June 2028</b>", SANS))
    s.append(Paragraph("Dear Joyce,", SANS))
    s.append(Paragraph(
        "This letter sets out our recommended funding rates for the 2027-28 plan year. Anthony and I went through the "
        "draft on 23 February; the only change since the draft we sent on 19 February is the stop-loss premium, which "
        "Wyecliff confirmed on 22 February.", SANS))
    s.append(Paragraph("<b>Experience.</b> We used Ellery's medical claims and Quarrystone's pharmacy claims incurred from "
                       "January 2025 to December 2026 and paid through 31 January 2027, with member months from Ellery's "
                       "eligibility. Bramwell's 2024 history is not in the District's warehouse and we did not use it. "
                       "Claims are taken at their allowed amounts, net of replacement and void claims and pharmacy "
                       "reversals; pharmacy is before rebates, which we treat as a separate credit. Exhibit 1 summarises the "
                       "experience. We completed 2026 medical claims with the factors in Exhibit 2, which we derived from "
                       "the plan's own payment pattern on claims incurred in the second half of 2025. Pharmacy claims are "
                       "paid at the point of sale and need no completion.", SANS))
    s.append(Paragraph("<b>Trend.</b> We are holding annual trend at %.1f per cent for medical and %.1f per cent for pharmacy, "
                       "unchanged from last year's renewal. The pharmacy rate reflects GLP-1 and specialty growth on the "
                       "Quarrystone formulary; we will look at it again after the 2026 rebate true-up in June."
                       % (100 * (W.TREND_MED - 1), 100 * (W.TREND_RX - 1)), SANS))
    s.append(Paragraph("<b>Projection.</b> We projected the 2026 completed experience 18 months, from the middle of calendar "
                       "2026 to the middle of the 2027-28 plan year. That gives %s per member per month for medical and %s "
                       "for pharmacy, %s in total, before fixed costs."
                       % (money(F["proj_med"], True), money(F["proj_rx"], True), money(F["proj_med"] + F["proj_rx"], True)), SANS))
    s.append(Paragraph("<b>Fixed costs.</b> Ellery's administrative fee is $38.75 per employee per month from 1 January 2027. "
                       "Wyecliff renewed the specific stop-loss for calendar 2027 at a $300,000 deductible with no individual "
                       "lasers, at $78.20 per employee per month, and the aggregate cover at $4.15. Northcourt's "
                       "administrative fee under the new care management agreement is budgeted outside the funding rates, "
                       "as is any shared savings payment, and we have not taken credit for programme savings in the "
                       "projection. We have kept the 3 per cent margin.", SANS))
    s.append(Paragraph("<b>Recommended rates.</b> On this basis we recommend the monthly funding rates below, an increase of "
                       "%.1f per cent on the current rates on the District's enrolment as of February 2027." % F["rate_incr"], SANS))
    rates = [["Coverage tier", "PPO 2026-27", "PPO 2027-28", "HSA plan 2026-27", "HSA plan 2027-28"]]
    for tier, label in (("EE", "Employee"), ("ES", "Employee + spouse"), ("EC", "Employee + child(ren)"), ("FAM", "Family")):
        rates.append([label, money(F["rates_now"]["PPO"][tier], True), money(F["rates_new"]["PPO"][tier], True),
                      money(F["rates_now"]["HDHP"][tier], True), money(F["rates_new"]["HDHP"][tier], True)])
    s.append(grid(rates, [1.75 * inch, 1.15 * inch, 1.15 * inch, 1.2 * inch, 1.2 * inch]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Please call me with any questions before the Board's 25 March meeting.", SANS))
    s.append(Paragraph("Sincerely,", SANS))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Michael Perry, FSA, MAAA<br/>Principal and Consulting Actuary", SANS))
    s.append(PageBreak())
    s.append(Paragraph("<b>Exhibit 1. Experience, incurred January 2025 to December 2026, paid through 31 January 2027</b>", SANS))
    e = [["", "2025", "2026"],
         ["Member months", format(F["mm"][2025], ","), format(F["mm"][2026], ",")],
         ["Medical allowed, paid", money(F["med_paid"][2025]), money(F["med_paid"][2026])],
         ["Medical allowed, completed", money(F["med_comp"][2025]), money(F["med_comp"][2026])],
         ["Pharmacy allowed, before rebates", money(F["rx"][2025]), money(F["rx"][2026])],
         ["Medical per member per month", money(F["med_comp"][2025] / F["mm"][2025], True), money(F["med_comp"][2026] / F["mm"][2026], True)],
         ["Pharmacy per member per month", money(F["rx"][2025] / F["mm"][2025], True), money(F["rx"][2026] / F["mm"][2026], True)],
         ["Total per member per month", money((F["med_comp"][2025] + F["rx"][2025]) / F["mm"][2025], True),
          money((F["med_comp"][2026] + F["rx"][2026]) / F["mm"][2026], True)]]
    s.append(grid(e, [2.6 * inch, 1.5 * inch, 1.5 * inch]))
    s.append(Paragraph("Member months and claims on the same basis as the 2026-27 renewal. 2025 medical claims are treated as "
                       "complete.", SANS_SM))
    s.append(Spacer(1, 10))
    s.append(Paragraph("<b>Exhibit 2. Medical completion factors, 2026 incurred months, paid through 31 January 2027</b>", SANS))
    cf = [["Incurred month", "Completion factor"]]
    for m in range(1, 13):
        cf.append([dt.date(2026, m, 1).strftime("%B 2026"), "%.3f" % F["cf"][m]])
    s.append(grid(cf, [2.0 * inch, 1.4 * inch]))
    s.append(Paragraph("Completed claims are paid claims divided by the factor. Factors are the share of the final allowed "
                       "amount for claims incurred July to December 2025 that had been paid the same number of months after "
                       "the incurred month.", SANS_SM))
    s.append(Spacer(1, 10))
    s.append(Paragraph("<b>Exhibit 3. Projection to the 2027-28 plan year (per member per month)</b>", SANS))
    pj = [["", "Medical", "Pharmacy"],
          ["2026 completed experience", money(F["med_comp"][2026] / F["mm"][2026], True), money(F["rx"][2026] / F["mm"][2026], True)],
          ["Annual trend", "%.1f%%" % (100 * (W.TREND_MED - 1)), "%.1f%%" % (100 * (W.TREND_RX - 1))],
          ["Months, 1 July 2026 to 1 January 2028", "18", "18"],
          ["Projected 2027-28", money(F["proj_med"], True), money(F["proj_rx"], True)]]
    s.append(grid(pj, [2.6 * inch, 1.5 * inch, 1.5 * inch]))
    build_pdf(path, s, "RCV 2027-28 renewal", "Michael Perry", "Microsoft\xae Word for Microsoft 365",
              "Microsoft\xae Word for Microsoft 365", dt.datetime(2027, 2, 26, 16, 5, 41), onpage=page,
              margins=(0.95, 0.95, 1.0, 0.8))


# ------------------------------------------------------------------ stop-loss policy schedule
def stoploss_pdf(path, census):
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.9 * inch, 0.5 * inch, "WLA-SL-SCH (01/26)    Policy WSL 27 041188")
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d of 3" % doc.page)
        canvas.restoreState()

    s = []
    s.append(Paragraph("<b>WYECLIFF LIFE ASSURANCE COMPANY</b>", ParagraphStyle("x", parent=SANS, fontSize=13, alignment=TA_CENTER)))
    s.append(Paragraph("Employer Medical Stop Loss Insurance", ParagraphStyle("y", parent=SANS, alignment=TA_CENTER)))
    s.append(Paragraph("<b>POLICY SCHEDULE</b>", ParagraphStyle("z", parent=SANS, alignment=TA_CENTER)))
    s.append(Spacer(1, 6))
    rows = [
        ["Policyholder", "Independent School District No. 2817 (Red Cedar Valley Schools), Minnesota"],
        ["Policy number", "WSL 27 041188"],
        ["Policy period", "12:01 a.m. 1 January 2027 to 12:00 midnight 31 December 2027, Central Time"],
        ["Plan", "Red Cedar Valley Schools Employee Health Plan (self-insured)"],
        ["Claims administrator", "Ellery Benefit Administrators (medical); Quarrystone Rx (prescription drugs)"],
        ["Producer of record", "Lindqvist Benefits Consulting, Minneapolis"],
        ["Covered benefits", "Medical and prescription drug"],
    ]
    s.append(grid(rows, [1.7 * inch, 4.9 * inch], header=False, align_right_from=9, size=9))
    s.append(Paragraph("<b>Part 1. Specific stop loss</b>", SANS))
    rows = [
        ["Specific deductible", "$300,000 per Covered Person per Policy Period"],
        ["Contract basis", "Claims incurred 1 January 2026 to 31 December 2027 and paid 1 January 2027 to 31 December 2027 (24/12)"],
        ["Reimbursement", "100 per cent of Eligible Expenses in excess of the specific deductible"],
        ["Maximum benefit", "Unlimited per Covered Person"],
        ["Individual deductibles", "None. No Covered Person is subject to a separate specific deductible for this Policy Period."],
        ["Premium", "$78.20 per covered employee per month, composite"],
    ]
    s.append(grid(rows, [1.7 * inch, 4.9 * inch], header=False, align_right_from=9, size=9))
    s.append(Paragraph("<b>Part 2. Aggregate stop loss</b>", SANS))
    rows = [["Coverage tier", "Monthly aggregate factor"], ["Employee", "$812.40"], ["Employee + spouse", "$1,690.10"],
            ["Employee + child(ren)", "$1,452.60"], ["Family", "$2,371.30"]]
    s.append(grid(rows, [2.6 * inch, 1.8 * inch], size=9))
    rows = [
        ["Attachment point", "The sum over the Policy Period of the monthly aggregate factors times the covered employees in "
                             "each tier in that month; not less than the minimum attachment point"],
        ["Minimum attachment point", "95 per cent of the first month's factors times 12"],
        ["Contract basis", "Claims incurred 1 January 2027 to 31 December 2027 and paid 1 January 2027 to 31 March 2028 (12/15)"],
        ["Maximum benefit", "$1,000,000 per Policy Period"],
        ["Premium", "$4.15 per covered employee per month"],
    ]
    s.append(grid(rows, [1.7 * inch, 4.9 * inch], header=False, align_right_from=9, size=9))
    s.append(PageBreak())
    s.append(Paragraph("<b>Part 3. Definitions used in this Schedule</b>", SANS))
    for k, t in [
        ("Eligible Expenses", "Amounts the Plan has paid for covered medical and prescription drug services under the terms "
                              "of the Plan Document in force at the start of the Policy Period, after member deductibles, "
                              "copayments and coinsurance, coordination of benefits, provider discounts and any "
                              "prescription drug rebates, administrative fees and cost-containment fees, and within the "
                              "contract basis above."),
        ("Covered Person", "An employee, early retiree or dependent covered under the Plan on the date a service is received."),
        ("Paid", "A claim is paid on the date the claims administrator releases the payment, provided funds are available "
                 "in the Plan's account when the payment clears."),
        ("Run-in", "Claims incurred in 2026 are eligible under the specific coverage only if paid within the Policy Period."),
    ]:
        s.append(Paragraph("<b>%s.</b> %s" % (k, t), SANS))
    s.append(Paragraph("<b>Part 4. Notification and claims</b>", SANS))
    s.append(Paragraph("The Policyholder or its claims administrator will notify the Company within 30 days after a Covered "
                       "Person's paid claims in the Policy Period reach $150,000, and within 30 days after any of the "
                       "following is first coded on a claim: a malignant neoplasm under active treatment, an organ or bone "
                       "marrow transplant evaluation, end-stage renal disease or dialysis, a neonatal intensive care stay "
                       "over 10 days, a spinal cord or traumatic brain injury, or a specialty drug with an annual cost above "
                       "$100,000. Requests for reimbursement are submitted with an itemised claim history and proof of "
                       "payment; the Company pays within 30 days of a complete request.", SANS))
    s.append(Paragraph("<b>Part 5. Renewal</b>", SANS))
    s.append(Paragraph("The Company will offer renewal terms at least 60 days before the end of the Policy Period. Renewal "
                       "terms may change the deductible, factors, premiums and individual deductibles on the basis of the "
                       "Plan's experience and the disclosure provided with the renewal application.", SANS))
    s.append(PageBreak())
    s.append(Paragraph("<b>Part 6. Premium summary at issue</b>", SANS))
    rows = [["", "Covered employees (January 2027 census)", "Monthly premium"],
            ["Specific", format(census, ","), money(census * 78.20, True)],
            ["Aggregate", format(census, ","), money(census * 4.15, True)],
            ["Total", "", money(census * 78.20 + census * 4.15, True)]]
    s.append(grid(rows, [1.3 * inch, 2.8 * inch, 1.6 * inch], size=9))
    s.append(Spacer(1, 18))
    s.append(Paragraph("Signed for Wyecliff Life Assurance Company on 18 December 2026.", SANS))
    s.append(Spacer(1, 14))
    s.append(Paragraph("Jonathan Hoffman<br/>Vice President, Stop Loss Underwriting", SANS))
    s.append(Paragraph("This Schedule forms part of the Policy and should be read with the Policy form WLA-SL-1 (01/26).", SANS_SM))
    build_pdf(path, s, "Policy Schedule WSL 27 041188", "Wyecliff Life Assurance Company", "PScript5.dll Version 5.2.2",
              "Acrobat Distiller 23.0 (Windows)", dt.datetime(2026, 12, 18, 9, 12, 7), onpage=page)


# ------------------------------------------------------------------ workbooks
THIN = Side(style="thin", color="A6A6A6")
HDR_FILL = PatternFill("solid", fgColor="DCE6F1")


def save_xlsx(wb, path, creator, last_by, created, modified, company):
    wb.properties.creator = creator
    wb.save(path)
    C.repack(path, C.core_props(creator, last_by, created, modified),
             C.app_props_xlsx([ws.title for ws in wb.worksheets], company))


def stratification_xlsx(path, kind, rows, people):
    """kind: bid, draft or final. rows: (rank, pid, ident, score, tier)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Cover"
    tiers = "Tier 1: %.1f and above; Tier 2: %.1f to %.1f; Tier 3: %.1f to %.1f; Tier 4: below %.1f" % (
        W.TIERS[0][1], W.TIERS[1][1], W.TIERS[0][1] - 0.1, W.TIERS[2][1], W.TIERS[1][1] - 0.1, W.TIERS[2][1])
    if kind == "bid":
        meta = [
            ("Northcourt Care Partners", "Clinical Analytics"),
            ("Document", "RFP 2025-07 response, Attachment C: population stratification"),
            ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817)"),
            ("Prepared by", "Amy Kelley, Clinical Analytics; reviewed by Allison Santiago, Account Lead"),
            ("Date", "21 February 2025"),
            ("Data basis", "RFP 2025-07 data book issued 24 January 2025: medical and pharmacy claims incurred 1 January to "
                           "31 December 2024, paid through 31 December 2024; eligibility as of 1 January 2025"),
            ("Member ID", "Member number as shown in the data book (Bramwell Plan Services)"),
            ("Model", "Northcourt Acuity Model 4.2, run on one calendar year of claims"),
            ("Score", "0 to 100, shown to one decimal; ranks use the unrounded score"),
            ("Selection", "The 140 highest-scoring members enrolled on 1 January 2025 (proposed programme capacity)"),
            ("Risk tiers", tiers),
            ("Proposed programme year", "1 April 2025 to 31 March 2026"),
            ("", ""),
            ("Confidential", "Contains protected health information. For use in the evaluation of RFP 2025-07 only."),
        ]
        when = (dt.datetime(2025, 2, 21, 14, 37, 2), "Amy Kelley")
    elif kind == "draft":
        meta = [
            ("Northcourt Care Partners", "Clinical Analytics"),
            ("Document", "Stratification of 2026 claims: DRAFT for District review"),
            ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817)"),
            ("Prepared by", "Amy Kelley, Clinical Analytics; Allison Santiago, Account Lead"),
            ("Date", "14 January 2027"),
            ("Data basis", "Ellery medical and Quarrystone pharmacy claims incurred 1 January to 31 December 2026, paid "
                           "through 31 December 2026; members enrolled on 1 January 2027"),
            ("Member ID", "Ellery member ID"),
            ("Model", "Northcourt Acuity Model 4.2, run on one calendar year of claims"),
            ("Score", "0 to 100, shown to one decimal; ranks use the unrounded score"),
            ("Selection", "The 140 highest-scoring members enrolled on 1 January 2027"),
            ("Risk tiers", tiers),
            ("Status", "Draft. The enrolment list will be rerun on February paid claims."),
            ("", ""),
            ("Confidential", "Contains protected health information."),
        ]
        when = (dt.datetime(2027, 1, 14, 11, 20, 45), "Amy Kelley")
    else:
        meta = [
            ("Northcourt Care Partners", "Clinical Analytics"),
            ("Document", "Final Enrolment List, Care Management Services Agreement RCV-2027-014, Section 3.2"),
            ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817)"),
            ("Prepared by", "Amy Kelley, Clinical Analytics; Allison Santiago, Account Lead"),
            ("Delivered", "5 March 2027"),
            ("Data basis", "Ellery medical and Quarrystone pharmacy claims incurred 1 January to 31 December 2026, paid "
                           "through 28 February 2027; members enrolled on 1 March 2027"),
            ("Member ID", "Ellery member ID"),
            ("Model", "Northcourt Acuity Model 4.2, run on one calendar year of claims"),
            ("Score", "0 to 100, shown to one decimal; ranks use the unrounded score"),
            ("Selection", "The 140 highest-scoring members enrolled on 1 March 2027"),
            ("Risk tiers", tiers),
            ("Programme Year", "1 April 2027 to 31 March 2028"),
            ("Supersedes", "Draft stratification of 14 January 2027"),
            ("", ""),
            ("Confidential", "Contains protected health information."),
        ]
        when = (dt.datetime(2027, 3, 5, 9, 48, 30), "Allison Santiago")
    for i, (k, v) in enumerate(meta, 1):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True, name="Calibri", size=11 if i > 1 else 13)
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=i, column=1).alignment = Alignment(vertical="top")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 96
    lst = wb.create_sheet("Members")
    hdr = ["Rank", "Member ID", "Relationship", "Date of birth", "Sex", "Acuity score", "Risk tier"]
    if kind == "final":
        hdr += ["Care team", "Enrolment effective"]
    lst.append(hdr)
    rel = {"E": "Subscriber", "R": "Subscriber", "S": "Spouse", "C": "Dependent"}
    for rank, pid, ident, sc, tier in rows:
        p = people[pid]
        row = [rank, ident, rel[p.rel], p.dob, p.sex, sc, tier]
        if kind == "final":
            row += [("RN Team " + "ABC"[(rank - 1) % 3]) if tier <= 2 else ("Health Coach Team " + "12"[(rank - 1) % 2]),
                    dt.date(2027, 4, 1)]
        lst.append(row)
    for j in range(1, len(hdr) + 1):
        c = lst.cell(row=1, column=j)
        c.font = Font(bold=True)
        c.fill = HDR_FILL
        c.border = Border(bottom=THIN)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for r_ in range(2, len(rows) + 2):
        lst.cell(row=r_, column=4).number_format = "mm/dd/yyyy"
        lst.cell(row=r_, column=6).number_format = "0.0"
        if kind == "final":
            lst.cell(row=r_, column=9).number_format = "mm/dd/yyyy"
    widths = [7, 15, 13, 13, 6, 12, 10, 18, 18]
    for j, wdt in enumerate(widths[:len(hdr)], 1):
        lst.column_dimensions[get_column_letter(j)].width = wdt
    lst.freeze_panes = "A2"
    lst.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(hdr)), len(rows) + 1)
    sm = wb.create_sheet("Tier summary")
    sm.append(["Risk tier", "Score range", "Members"])
    for t, floor in W.TIERS:
        hi = {1: None, 2: W.TIERS[0][1], 3: W.TIERS[1][1], 4: W.TIERS[2][1]}[t]
        rng = ("%.1f and above" % floor) if t == 1 else ("below %.1f" % hi if t == 4 else "%.1f to %.1f" % (floor, hi - 0.1))
        sm.append([t, rng, sum(1 for r_ in rows if r_[4] == t)])
    sm.append(["Total", "", len(rows)])
    for j in range(1, 4):
        sm.cell(row=1, column=j).font = Font(bold=True)
        sm.cell(row=1, column=j).fill = HDR_FILL
    sm.cell(row=6, column=1).font = Font(bold=True)
    sm.cell(row=6, column=3).font = Font(bold=True)
    sm.column_dimensions["A"].width = 11
    sm.column_dimensions["B"].width = 18
    sm.column_dimensions["C"].width = 10
    created = when[0] - dt.timedelta(hours=3, minutes=12)
    save_xlsx(wb, path, "Amy Kelley", when[1], created.replace(tzinfo=C.CENTRAL), when[0].replace(tzinfo=C.CENTRAL),
              "Northcourt Care Partners, LLC")


def rebate_xlsx(path, R):
    """R: per quarter and drug counts of net brand claims in 2026 (estimators.rebate_figures)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    top = [("Quarrystone Rx", ""), ("Client rebate statement, calendar year 2026", ""),
           ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817), group RCV01"),
           ("Prepared", "19 February 2027 by Client Services (Michelle Peterson, Client Account Executive)"),
           ("Contract", "Pharmacy Benefit Services Agreement, Exhibit 4: minimum rebate guarantees per paid brand claim"), ("", "")]
    for k, v in top:
        ws.append([k, v])
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"].font = Font(bold=True)
    hdr = ["Quarter", "Brand claims, retail and mail", "Guarantee per claim", "Specialty claims", "Guarantee per claim",
           "Rebates earned", "Invoiced to manufacturers", "Received from Quarrystone", "Status"]
    ws.append(hdr)
    hr = ws.max_row
    for j in range(1, len(hdr) + 1):
        c = ws.cell(row=hr, column=j)
        c.font = Font(bold=True)
        c.fill = HDR_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    status = {1: ("05/14/2026", "08/21/2026", "Paid"), 2: ("08/13/2026", "11/20/2026", "Paid"),
              3: ("11/12/2026", "02/18/2027", "Paid"), 4: ("02/11/2027", "", "Invoiced; payment expected by 06/30/2027")}
    tot = [0, 0, 0.0]
    for q in (1, 2, 3, 4):
        b, sp = R["brand"][q], R["spec"][q]
        earned = b * R["g_brand"] + sp * R["g_spec"]
        tot[0] += b
        tot[1] += sp
        tot[2] += earned
        ws.append(["Q%d 2026" % q, b, R["g_brand"], sp, R["g_spec"], earned, status[q][0], status[q][1], status[q][2]])
    ws.append(["Total", tot[0], None, tot[1], None, tot[2], None, None, None])
    last = ws.max_row
    for r_ in range(hr + 1, last + 1):
        for col in (3, 5, 6):
            ws.cell(row=r_, column=col).number_format = '"$"#,##0.00'
        for col in (2, 4):
            ws.cell(row=r_, column=col).number_format = "#,##0"
    for col in range(1, 10):
        ws.cell(row=last, column=col).font = Font(bold=True)
        ws.cell(row=last, column=col).border = Border(top=THIN)
    ws.append([])
    notes = ["Counts are paid brand claims net of reversals, by date of service. Generic claims and compound claims are "
             "not rebatable.",
             "Specialty claims are claims dispensed by Quarrystone Specialty Pharmacy for drugs on the specialty list.",
             "Rebates are remitted to the plan quarterly in arrears and are not shown on claim records or in claim amounts.",
             "Q4 2026 amounts are minimum guarantees; any excess over guarantee is reconciled in the annual true-up in June 2027."]
    for n in notes:
        ws.append([n])
    for j, wdt in enumerate([13, 16, 13, 12, 13, 16, 16, 16, 36], 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.row_dimensions[hr].height = 45
    d = wb.create_sheet("By drug")
    hdr = ["Drug", "NDC", "Specialty", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "Claims 2026", "Rebates earned"]
    d.append(hdr)
    for j in range(1, len(hdr) + 1):
        d.cell(row=1, column=j).font = Font(bold=True)
        d.cell(row=1, column=j).fill = HDR_FILL
    for name, ndc, spec, qs in R["by_drug"]:
        n = sum(qs)
        d.append([name, ndc, "Y" if spec else "N"] + list(qs) + [n, n * (R["g_spec"] if spec else R["g_brand"])])
    for r_ in range(2, d.max_row + 1):
        d.cell(row=r_, column=9).number_format = '"$"#,##0.00'
    for j, wdt in enumerate([36, 15, 10, 9, 9, 9, 9, 12, 15], 1):
        d.column_dimensions[get_column_letter(j)].width = wdt
    d.freeze_panes = "A2"
    save_xlsx(wb, path, "Michelle Peterson", "Michelle Peterson", dt.datetime(2027, 2, 18, 15, 2, 11, tzinfo=C.CENTRAL),
              dt.datetime(2027, 2, 19, 8, 31, 54, tzinfo=C.CENTRAL), "Quarrystone Rx")


# ------------------------------------------------------------------ the analyst's dictionary
DICTIONARY = """CLAIMS WAREHOUSE EXTRACTS - FIELD DICTIONARY
Red Cedar Valley Schools, Risk Management and Benefits
Maintained by Tiffany Barrett, Benefits Analyst
Version of 8 March 2027 (covers the extracts pulled 1 to 3 March 2027)

Four files, all CSV with a header row, UTF-8, comma delimited, amounts in US dollars.

  medical_claim_lines_2025-01_2027-02.csv    Ellery Benefit Administrators, medical claim lines
  pharmacy_claims_2025-01_2027-02.csv        Quarrystone Rx, monthly claims file (PBM layout, unchanged)
  eligibility_spans_2027-02.csv              Ellery Benefit Administrators, eligibility
  tpa_conversion_crosswalk_2025-01-01.csv    Ellery's conversion file from the Bramwell Plan Services records

The warehouse feed started with Ellery's takeover on 1 January 2025. Bramwell's claims history (everything incurred
before 1 January 2025) was never loaded, so neither claims file has dates of service before 1 January 2025.


1. medical_claim_lines_2025-01_2027-02.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per line of an adjudicated claim. Every version of a claim that Ellery has adjudicated (original,
replacement, void) is its own claim number with its own lines. Claims paid or processed 1 January 2025 through
28 February 2027. Pulled 3 March 2027. A claim adjudicated after 28 February 2027 is not in the file.

claim_number            Ellery claim number. YYDDD of the receipt date followed by a sequence.
line_number             Line on the claim, from 1.
claim_type              P professional (CMS-1500 / 837P), I institutional (UB-04 / 837I).
bill_type               Institutional type of bill (UB-04 form locator 4), blank on professional claims. The third
                        digit repeats the claim frequency code.
claim_frequency_code    1 original claim
                        7 replacement of a prior claim
                        8 void / cancel of a prior claim
                        A replacement claim replaces every line of the claim named in original_claim_number; the
                        replaced claim's lines stay in the file as they were first adjudicated. A void claim's lines
                        repeat the voided claim's lines with every amount carrying the opposite sign.
original_claim_number   For frequency 7 and 8 claims, the claim number the claim replaces or voids. Blank otherwise.
member_id               Ellery member ID (RCV + 7 digits). Joins to eligibility_spans_2027-02.csv.
first_date_of_service   Earliest date of service on the claim (statement from date on institutional claims).
last_date_of_service    Latest date of service on the claim (statement through date; discharge date for a stay).
paid_date               Date Ellery released payment; on a fully denied claim, the date it was processed.
place_of_service        CMS place of service code, professional claims only (11 office, 20 urgent care, 21 inpatient
                        hospital, 22 on-campus outpatient hospital, 23 emergency department, 24 ambulatory surgery
                        center, 41 ambulance, 81 independent laboratory, 10 telehealth in the patient's home).
revenue_code            NUBC revenue code, institutional claims only.
procedure_code          CPT or HCPCS code. Blank on revenue lines billed without one (room and board, supplies).
modifier                First procedure modifier, where billed.
diagnosis_code_1        Principal or first-listed ICD-10-CM diagnosis on the claim (shown with the decimal point).
diagnosis_code_2        Second diagnosis on the claim, where there is one.
billing_npi             Billing provider NPI.
units                   Units of service (days for room and board and NICU lines, sessions for dialysis).
billed_amount           Provider's billed charge for the line.
allowed_amount          Ellery's allowed amount for the line under the provider contract or the plan's reasonable
                        and customary schedule. Blank on a denied line.
deductible_amount       Member deductible applied to the line.
copay_amount            Member copayment applied to the line.
coinsurance_amount      Member coinsurance applied to the line.
plan_paid_amount        Amount the plan paid on the line. On every line with an allowed amount,
                        allowed_amount = deductible_amount + copay_amount + coinsurance_amount + plan_paid_amount.
denial_reason_code      Claim adjustment reason code on a denied line; blank on a paid line. A denied line carries no
                        allowed amount and no member cost sharing, and plan_paid_amount is 0.00.
                          16   claim lacks information needed for adjudication (usually resubmitted as a new claim)
                          18   exact duplicate claim or service
                          27   expenses incurred after coverage terminated
                          97   payment included in the allowance for another service
                          204  service not covered under the current benefit plan


2. pharmacy_claims_2025-01_2027-02.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per PBM transaction, claims processed 1 January 2025 through 28 February 2027. Quarrystone's monthly
file, appended month by month with no changes to their layout. Dates are CCYYMMDD.

CLAIM_NBR            Quarrystone transaction number.
TXN_CD               B1 claim billing; B2 reversal of an earlier billing. A B2 carries the RX_NBR, FILL_NBR,
                     DATE_OF_SERVICE and pharmacy of the B1 it reverses and the same quantities, with every amount
                     carrying the opposite sign.
RX_NBR, FILL_NBR     Pharmacy prescription number and fill number (00 for the original fill, 01 onward for refills).
DATE_OF_SERVICE      Fill date.
DATE_PROCESSED       Date Quarrystone adjudicated the transaction.
CARDHOLDER_ID        District employee number of the subscriber, zero-filled to nine characters.
PERSON_CD            Person code: 01 subscriber, 02 spouse, 03 and up dependents. Same codes as Ellery's eligibility.
PATIENT_DOB          Patient date of birth.
PATIENT_GENDER_CD    1 male, 2 female.
RELATIONSHIP_CD      1 cardholder, 2 spouse, 3 child.
PHARMACY_NPI         Dispensing pharmacy NPI.
PHARMACY_NCPDP_ID    Dispensing pharmacy NCPDP provider ID.
NDC                  National Drug Code, 11 digits in 5-4-2 form.
DRUG_NAME            Quarrystone's drug description.
BRAND_GENERIC_CD     B brand, G generic.
DAW_CD               Dispense as written code (0 no product selection indicated, 1 substitution not allowed by
                     prescriber).
QTY_DISPENSED        Metric quantity (tablets, capsules, mL or grams).
DAYS_SUPPLY          Days supply.
INGREDIENT_COST      Ingredient cost paid.
DISPENSING_FEE       Dispensing fee paid.
GROSS_AMT_DUE        INGREDIENT_COST + DISPENSING_FEE: the allowed amount of the claim.
PATIENT_PAY_AMT      Member copayment, coinsurance or deductible.
PLAN_PAY_AMT         GROSS_AMT_DUE - PATIENT_PAY_AMT.
                     All amounts are before manufacturer rebates. Rebates are remitted quarterly in arrears and are
                     reported on Quarrystone's rebate statements, not on claims.


3. eligibility_spans_2027-02.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per member per coverage span with Ellery. A new span starts whenever the plan, the coverage tier or
the employee class changes. Pulled 1 March 2027 from Ellery's eligibility as of 28 February 2027.

member_id           Ellery member ID.
employee_number     District employee number of the subscriber (six digits). Early retirees keep theirs.
person_code         01 subscriber, 02 spouse, 03 and up dependents. Ellery renumbered dependents by date of birth at
                    the conversion; children added later take the next number.
relationship        SUB subscriber (employee or early retiree), SPS spouse, DEP dependent child.
birth_date          Date of birth.
sex                 F or M.
employee_class      TCH licensed teacher, ESP education support professional, ADM administrator, RET early retiree.
coverage_tier       EE employee only, ES employee and spouse, EC employee and child(ren), FAM family.
plan_code           RCV-PPO (PPO plan) or RCV-HSA (high-deductible plan with HSA).
span_start          First day of coverage in the span. Spans start no earlier than 1 January 2025, the day Ellery took
                    over; a member covered before then starts on 1 January 2025.
span_end            Last day of coverage in the span (inclusive). Blank: coverage continuing at the pull.
                    Terminations take effect at month end (31 August for teachers who complete the school year),
                    except deaths, which end coverage on the date of death. Newborns are covered from the date of birth.


4. tpa_conversion_crosswalk_2025-01-01.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per Bramwell member record converted to Ellery on 1 January 2025. Built by Ellery's implementation
team from Bramwell's final eligibility file. Not updated since.

prior_subscriber_number   Bramwell subscriber number (eight digits).
prior_member_suffix       Bramwell member suffix. Bramwell's member number is prior_subscriber_number and
                          prior_member_suffix (shown as NNNNNNNN-SS on Bramwell reports and in the RFP 2025-07 data
                          book). Bramwell gave dependents suffixes in the order it enrolled them, and the suffixes
                          were not carried over: compare person_code.
member_id                 Ellery member ID issued at conversion.
employee_number           District employee number of the subscriber.
person_code               Ellery person code at conversion.
relationship              SUB, SPS or DEP.
birth_date                Date of birth as received from Bramwell (MM/DD/YYYY).
conversion_note           MERGED DUPLICATE PRIOR RECORD where Bramwell held one member under two records; both prior
                          numbers map to the one Ellery member ID.

Questions on these files: Tiffany Barrett, ext. 4417.
"""


def dictionary_txt(path):
    with open(path, "w", newline="\n") as f:
        f.write(DICTIONARY)
