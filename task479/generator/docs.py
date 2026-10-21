"""The pack's documents: the Executive Director's contribution review memo to the Board of Trustees, the benefit
designs by district for plan years 2025 and 2026, the 2026 contribution rates workbook, the data dictionary and the
extract manifest."""
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

import numpy as np    # noqa: E402

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
GREEN = colors.HexColor("#2c5a3f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.4, leading=10.6, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)

MEMO = [
    ("1. Purpose", [
        "At its meeting on 4 November 2026 the Board decides which member districts' contributions rise from "
        "1 January 2027. Under the funding policy a district whose contribution does not cover the claims its plan is "
        "running pays an increase from the next 1 January; the size of each increase is set at the December meeting "
        "with the 2027 rates. This memo fixes the basis of the November review."]),
    ("2. The test", [
        "A district's contribution rises from 1 January 2027 when its expected plan-paid claims per member per month "
        "for plan year 2026, January to December 2026, exceed the claims component of its 2026 contribution rate.",
        "Plan-paid claims are the medical and pharmacy claims the plan pays after the member's deductible, "
        "coinsurance and copays, gross of specific stop-loss reimbursements and before pharmacy rebates, which are "
        "credited to the cooperative's reserve and not to a district. Per member per month is over the district's "
        "member months, a member month being a member enrolled in the district's plan in the month."]),
    ("3. The evidence", [
        "The review rests on the claims each district has incurred from January to June 2026 and Tollard has paid "
        "through 30 September 2026, with the district's January to June 2026 member months, and on the cooperative's "
        "experience in plan year 2025, incurred in 2025 and paid through 31 March 2026, all from Tollard's claims lag "
        "reports and eligibility file. Tollard pays nearly all of a month's claims within three months of it, so both "
        "periods are complete. The claims components are in the 2026 contribution rates workbook; the Board set them "
        "in October 2025 on each district's 2026 benefit design."]),
    ("4. Alongside the review", [
        "The Board will also see each district's July to September 2026 member months, on which Tollard bills the "
        "third-quarter contributions, and the members Granfield Specialty Insurance Company has on specific advisory "
        "for 2026, with their incurred claims to date as Granfield last reported them, so that trustees can see where "
        "a district's year rests on a few large claims."]),
]


def _frame(foot):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return frame


def _masthead(title):
    return [Paragraph(P.COMPANY.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4,
                                                        textColor=GREEN, leading=11)),
            Paragraph(title, ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18,
                                            textColor=INK, spaceAfter=6))]


def write_memo(path):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="Contribution review for 1 January 2027",
                          author="James Hernandez", subject="", creator="", producer="")
    head = [["To", "Board of Trustees"], ["From", "James Hernandez, Executive Director"],
            ["Date", "2 October 2026"], ["Subject", "Contribution review for 1 January 2027"]]
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead("Memorandum") + [t, Spacer(1, 8)]
    for h, paras in MEMO:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    foot = "%s. Contribution review for 1 January 2027, 2 October 2026." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


PLANS = [("MVA", "$500 / $1,000", "20%", "$2,500 / $5,000", "$25", "$10 / $35 / $70"),
         ("MVB", "$1,500 / $3,000", "20%", "$4,000 / $8,000", "$30", "$10 / $35 / $70"),
         ("MVC", "$3,000 / $6,000", "20%", "$6,000 / $12,000", "20% after deductible", "$10 / $35 / $70")]


def write_benefits(path):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="Benefit designs by member district, plan years 2025 and 2026",
                          author="Brady Cooper", subject="", creator="", producer="")
    story = _masthead("Benefit designs by member district, plan years 2025 and 2026")
    story.append(Paragraph(
        "Each member district chooses one of the cooperative's three plans for each plan year, which runs from "
        "1 January to 31 December. The plans share Tollard's network, the Granfield specific stop-loss policy and the "
        "pharmacy formulary, and differ only in the member's cost sharing. Pharmacy is at copays for every plan.", BODY))
    hdr = ["Plan", "Calendar-year deductible (individual / family)", "Coinsurance", "Out-of-pocket maximum "
           "(individual / family)", "Office visit", "Pharmacy copays (generic / brand / specialty)"]
    rows = [[Paragraph(h, CELLB) for h in hdr]] + [[Paragraph(c, CELL) for c in r] for r in PLANS]
    t = Table(rows, colWidths=[0.55 * inch, 1.45 * inch, 0.9 * inch, 1.45 * inch, 1.0 * inch, 1.6 * inch])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [Spacer(1, 4), t, Spacer(1, 10)]
    story.append(Paragraph("Plan by district", H2))
    hdr = ["District", "Plan year", "Plan", "Individual deductible", "District name"]
    rows = [[Paragraph(h, CELLB) for h in hdr]]
    for did, name, d25, d26, *_ in W.DISTRICTS:
        for y, dz in ((2025, d25), (2026, d26)):
            rows.append([Paragraph(c, CELL) for c in (did, str(y), P.PLAN[dz], "${:,}".format(dz), name)])
    t = Table(rows, colWidths=[0.7 * inch, 0.75 * inch, 0.6 * inch, 1.2 * inch, 3.0 * inch], repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, 2), (-1, -1), 0.25, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [t, Spacer(1, 8)]
    story.append(Paragraph(
        "Brantmoor Public Schools, Farrowdale Consolidated Schools, Isenbrook Unified Schools and Northam Vale "
        "School District moved from plan MVA to plan MVC on 1 January 2026, with the cooperative's health savings "
        "account option opened to their employees from the same date. No other district changed plan.", SMALL))
    foot = "%s. Benefit designs, plan years 2025 and 2026; issued 14 November 2025." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_rates(path, x):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2026 rates"
    ws["A1"] = "%s: 2026 contribution rates per member per month" % P.COMPANY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Adopted by the Board of Trustees on 21 October 2025 for plan year 2026."
    ws.append([])
    ws.append(["District", "District name", "2026 plan", "Claims component", "Administration", "Specific stop-loss",
               "Reserve", "2026 contribution"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C5A3F")
    rng = np.random.default_rng(W.SEED + 9)
    for did, name, d25, d26, *_ in W.DISTRICTS:
        claims = x["rates"][did]
        admin = round(float(rng.uniform(34, 41)), 2)
        sl = round(float(rng.uniform(42, 58)), 2)
        res = round(claims * 0.03, 2)
        ws.append([did, name, P.PLAN[d26], claims, admin, sl, res, round(claims + admin + sl + res, 2)])
    for row in ws.iter_rows(min_row=5):
        for c in row[3:8]:
            c.number_format = "#,##0.00"
    for col, w in zip("ABCDEFGH", (9, 32, 9, 15, 14, 16, 10, 17)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["enroll"], "member_id", "Tollard's id for the member"),
        (f["enroll"], "subscriber_id", "Tollard's id for the employee whose coverage the member is on"),
        (f["enroll"], "relationship", "EE employee, SP spouse, CH child"),
        (f["enroll"], "birth_date", "the member's date of birth"),
        (f["enroll"], "district_id", "the member district"),
        (f["enroll"], "plan_code", "the district's plan in the month (benefit designs PDF)"),
        (f["enroll"], "coverage_month", "a month the member is enrolled, YYYY-MM"),
        (f["enroll"], "coverage_tier", "the subscriber's tier: EE, ES, EC or FAM"),
        (f["lag_old"], "IncurredMonth", "the month of service, MM/YYYY"),
        (f["lag_old"], "PaidMonth", "the month the claims were paid, MM/YYYY"),
        (f["lag_old"], "Category", "Medical or Pharmacy"),
        (f["lag_old"], "PaidAmount", "claims paid by the plan, dollars, net of reversals in the month"),
        (f["lag_new"], "incurred_period", "the month of service, YYYY-MM"),
        (f["lag_new"], "paid_period", "the month the claims were paid, YYYY-MM"),
        (f["lag_new"], "benefit_type", "MED medical, RX pharmacy"),
        (f["lag_new"], "plan_paid_cents", "claims paid by the plan, cents, net of reversals in the month"),
        (f["adv"], "advisory_date", "the date Granfield issued the advisory"),
        (f["adv"], "member_ref", "Tollard's member_id as Granfield holds it"),
        (f["adv"], "incurred_to_date", "the claimant's claims incurred in the 2026 contract year to date, dollars"),
        (f["adv"], "advisory_type", "initial (first advisory on the claimant file) or update"),
        (f["policy"], "contract_basis", "12/15: claims incurred in the contract year and paid within 15 months"),
        (f["policy"], "specific_deductible", "the claims of one member in a contract year above which Granfield "
                                             "reimburses, dollars"),
        (f["policy"], "aggregate_corridor_pct", "the aggregate attachment as a share of expected claims"),
        (f["rebates"], "rebate_amount", "pharmacy rebates credited to the cooperative's reserve, dollars"),
        (f["receipts"], "fiscal_year", "the districts' fiscal year, July to June"),
        (f["receipts"], "contribution_billed", "the district's contribution billed for the month, dollars"),
        (f["survey"], "median_total_pmpm_2025", "the survey's median 2025 total claims cost per member per month"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["enroll"], "member months by district", "Tollard eligibility", "2026-10-06", "2025-01 to 2026-09",
         n["enroll"]),
        (f["lag_old"], "claims lag report, legacy platform", "Tollard claims", "2026-06-02", "paid 2025-01 to 2026-05",
         n["lag_old"]),
        (f["lag_new"], "claims lag report, current platform", "Tollard claims", "2026-10-06",
         "paid 2026-05 to 2026-09", n["lag_new"]),
        (f["adv"], "2026 specific advisories", P.CARRIER, "2026-10-01", "2026 contract year to date", n["adv"]),
        (f["policy"], "specific stop-loss policy schedule", P.CARRIER, "2026-09-30", "2025 to 2027", n["policy"]),
        (f["rates"], "2026 contribution rates", P.COMPANY, "2025-10-21", "plan year 2026", 16),
        (f["memo"], "contribution review memo", P.COMPANY, "2026-10-02", "", ""),
        (f["benefits"], "benefit designs by district", P.COMPANY, "2025-11-14", "plan years 2025 and 2026", ""),
        (f["rebates"], "2025 pharmacy rebate statement", "Tollard pharmacy benefits", "2026-05-12", "2025",
         n["rebates"]),
        (f["receipts"], "district contribution receipts", P.COMPANY + " finance", "2026-07-15", "FY2026",
         n["receipts"]),
        (f["survey"], "state survey of school employee health plans", "State School Boards Benefits Council",
         "2026-04-30", "2025", n["survey"]),
        (f["dictionary"], "field descriptions", P.COMPANY, "2026-10-06", "", n["dictionary"]),
    ]
