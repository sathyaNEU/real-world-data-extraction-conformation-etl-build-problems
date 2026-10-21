"""The pack's documents: Marlowe's 2027 renewal assumptions memo, the employers' 2027 funding elections workbook, the
data dictionary and the extract manifest."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5b6470")
NAVY = colors.HexColor("#22395c")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.4, leading=10.6, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)

MEMO = [
    ("1. Purpose", [
        "This memo sets the assumptions Client Finance uses for each self-funded group's 2027 expected claims and for "
        "the funding true-up notices that go to employers on 2 November 2026. It does not change any group's plan "
        "design, stop-loss contract or administrative fee."]),
    ("2. Experience period", [
        "Each group's experience is its claims incurred from 1 January to 31 December 2025 and paid through "
        "31 March 2026, medical and pharmacy, as the claims lag report records them, and its 2025 member months from "
        "the enrollment file. A member month is a member enrolled in the group in the month. Claims paid after "
        "31 March 2026 are not part of the experience; the run-out factor for them is carried in the administrative "
        "load, not in the claims projection."]),
    ("3. Trend", [
        "Medical and pharmacy claims trend at 7.5 per cent a year, 2025 to 2027, two years, for every group. The "
        "assumption follows the 2027 renewal survey of the regional stop-loss market and Marlowe's own book; it is "
        "not adjusted by group."]),
    ("4. Retained claims", [
        "A group's retained claims are the claims the plan itself pays: its incurred claims less the specific "
        "stop-loss reimbursements due from Arbor Ridge Specialty Insurance Company. Each group's specific policy "
        "reimburses a member's claims incurred in the contract year above the specific deductible, which Arbor Ridge's "
        "2027 renewals keep at $250,000 for every group. Pharmacy rebates are credited to the employer's funding "
        "account when received and are not netted from claims. No group carries an aggregate stop-loss recovery in "
        "its experience."]),
    ("5. The true-up notice", [
        "Each employer elected its 2027 funding rate in September, of which the claims component is shown in the "
        "funding elections workbook. A group receives a true-up notice when its expected 2027 retained claims per "
        "member per month, on its 2025 experience and the trend in section 3, exceed the claims component of its "
        "2027 funding rate. The notice gives the employer until 1 December 2026 to raise its rate before the "
        "contribution schedules close."]),
]


def write_memo(path):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, "%s, Client Finance. 2027 renewal assumptions, issued 9 September "
                                                     "2026." % P.COMPANY)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="2027 renewal assumptions", author="Claire Grant", subject="",
                          creator="", producer="")
    head = [["To", "Account managers, Client Finance"], ["From", "Claire Grant, Director of Client Finance"],
            ["Date", "9 September 2026"], ["Subject", "2027 renewal assumptions for self-funded groups"]]
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = [Paragraph(P.COMPANY.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4,
                                                         textColor=NAVY, leading=11)),
             Paragraph("Memorandum", ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18,
                                                    textColor=INK, spaceAfter=6)), t, Spacer(1, 8)]
    for h, paras in MEMO:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_rates(path, x):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 elections"
    ws.append(["Group", "Employer", "Elected 2027 funding rate PMPM", "Claims component PMPM", "Administration PMPM",
               "Specific stop-loss premium PMPM", "Elected on", "Signed by"])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="22395C")
    import numpy as np
    rng = np.random.default_rng(W.SEED + 9)
    for gno, emp, *_ in W.GROUPS:
        claims = x["rates"][gno]
        admin = round(float(rng.uniform(38, 52)), 2)
        prem = round(float(rng.uniform(61, 96)), 2)
        day = int(rng.integers(8, 27))
        ws.append([gno, emp, round(claims + admin + prem, 2), claims, admin, prem, dt.date(2026, 9, day),
                   "Benefits committee"])
    for row in ws.iter_rows(min_row=2):
        for c in row[2:6]:
            c.number_format = "#,##0.00"
        row[6].number_format = "yyyy-mm-dd"
    for col, w in zip("ABCDEFGH", (9, 32, 16, 14, 13, 16, 12, 18)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["enroll"], "member_id", "Marlowe's id for the member"),
        (f["enroll"], "subscriber_id", "Marlowe's id for the employee whose coverage the member is on"),
        (f["enroll"], "relationship", "EE employee, SP spouse, CH child"),
        (f["enroll"], "birth_date", "the member's date of birth"),
        (f["enroll"], "coverage_month", "a month the member is enrolled, YYYY-MM"),
        (f["enroll"], "coverage_tier", "the subscriber's tier: EE, ES, EC or FAM"),
        (f["lag_old"], "IncurredMonth", "the month the service was provided, MM/YYYY"),
        (f["lag_old"], "PaidMonth", "the month the claims were paid, MM/YYYY"),
        (f["lag_old"], "Category", "Medical or Pharmacy"),
        (f["lag_old"], "PaidAmount", "claims paid by the plan, dollars, net of reversals in the month"),
        (f["lag_new"], "incurred_period", "the month the service was provided, YYYY-MM"),
        (f["lag_new"], "paid_period", "the month the claims were paid, YYYY-MM"),
        (f["lag_new"], "benefit_type", "MED medical, RX pharmacy"),
        (f["lag_new"], "paid_cents", "claims paid by the plan, cents, net of reversals in the month"),
        (f["lcr"], "member_ref", "Marlowe's member_id as Arbor Ridge holds it"),
        (f["lcr"], "total_incurred", "the member's claims incurred in 2025 and paid through 31 March 2026, dollars"),
        (f["lcr"], "specific_deductible", "the policy's specific deductible, dollars"),
        (f["lcr"], "eligible_excess", "total_incurred above the specific deductible, dollars"),
        (f["lcr"], "reimbursed_to_date", "what Arbor Ridge has reimbursed on the claimant, dollars"),
        (f["adv"], "advisory_date", "the date Arbor Ridge issued the advisory"),
        (f["adv"], "incurred_to_date", "the claimant's claims incurred in the 2026 contract year to date, dollars"),
        (f["adv"], "advisory_type", "initial (first advisory) or update"),
        (f["policy"], "contract_basis", "12/15: claims incurred in the contract year and paid within 15 months"),
        (f["policy"], "aggregate_corridor_pct", "the aggregate attachment as a share of expected claims (no group "
                                                "has an aggregate claim)"),
        (f["rebates"], "rebate_amount", "pharmacy rebates credited to the group's funding account, dollars"),
        (f["bench"], "median_pmpm_2025", "the survey's median 2025 total claims cost per member per month"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["enroll"], "member months by group", "Marlowe eligibility", "2026-10-05", "2025-01 to 2026-08", n["enroll"]),
        (f["lag_old"], "claims lag report, legacy platform", "Marlowe claims", "2026-06-03", "paid 2025-01 to 2026-05",
         n["lag_old"]),
        (f["lag_new"], "claims lag report, current platform", "Marlowe claims", "2026-10-05",
         "paid 2026-06 to 2026-09", n["lag_new"]),
        (f["lcr"], "2025 large claimant report", P.CARRIER, "2026-05-20", "claimants of $100,000 or more", n["lcr"]),
        (f["adv"], "2026 specific advisories", P.CARRIER, "2026-10-01", "2026 contract year to date", n["adv"]),
        (f["policy"], "specific stop-loss policy schedule", P.CARRIER, "2026-09-30", "2025 to 2027", n["policy"]),
        (f["roster"], "group roster", "Marlowe account management", "2026-10-01", "", n["roster"]),
        (f["rates"], "employers' 2027 funding elections", "Marlowe Client Finance", "2026-09-30", "2027", 16),
        (f["memo"], "2027 renewal assumptions", "Marlowe Client Finance", "2026-09-09", "", ""),
        (f["rebates"], "2025 pharmacy rebate statement", "Marlowe pharmacy benefits", "2026-05-14", "2025",
         n["rebates"]),
        (f["bench"], "regional employer health cost survey", "Lakeshore Employers Health Coalition", "2026-04-30",
         "2025", n["bench"]),
        (f["dictionary"], "field descriptions", "Marlowe Client Finance", "2026-10-05", "", n["dictionary"]),
    ]
