"""The pack's documents: the Plan Administrator's 2027 renewal review memo to the Board of Trustees, the plan
summary, the 2027 contribution elections workbook, the data dictionary and the extract manifest."""
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
        "At their meeting on 12 November 2026 the trustees decide which member employers pay a claims surcharge on "
        "their 2027 contributions. Each employer elected its 2027 contribution in September; the trust's funding "
        "policy adds a surcharge from 1 January 2027 for an employer whose contribution does not cover the claims its "
        "members are expected to cost, the surcharge itself set at the December meeting. This memo fixes the basis of "
        "the November review."]),
    ("2. The test", [
        "An employer is surcharged when its expected 2027 retained claims per member per month exceed the claims "
        "component of the 2027 contribution it elected.",
        "Retained claims are the medical and pharmacy claims the plan pays for the employer's members, less Westerby "
        "Specialty Insurance Company's specific stop-loss reimbursements, and before pharmacy rebates, which are "
        "credited to the trust's reserve. Per member per month is over member months, a member month being a member "
        "enrolled through the employer in the month. The 2027 plan, the specific deductible of $150,000 and the "
        "administrative and stop-loss charges are unchanged from 2026, and no employer is leaving the trust."]),
    ("3. The evidence", [
        "The review rests on the trust's experience in plan years 2023, 2024 and 2025: for every member employer, the "
        "claims incurred in the year and paid through 31 March of the next, from Hallam's claims lag reports, the "
        "member months from Hallam's eligibility file, and Westerby's reimbursements for the contract year. Each year's "
        "retained claims are trended at 7 per cent a year to 2027, the trust's trend for every employer. Claims for "
        "2026 are not yet complete and are not part of the review."]),
    ("4. Alongside the review", [
        "The trustees will also see each employer's July to September 2026 member months, on which Hallam bills the "
        "third-quarter contributions, and the members on Hallam's 2026 high-cost claimant report with their claims "
        "paid to date as last reported, so that trustees can see which employers carry large claims into 2027."]),
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
                          bottomMargin=0.9 * inch, title="2027 renewal review",
                          author="Michelle Patrick", subject="", creator="", producer="")
    head = [["To", "Board of Trustees"], ["From", "Michelle Patrick, Plan Administrator"],
            ["Date", "6 October 2026"], ["Subject", "2027 renewal review of member employers' contributions"]]
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead("Memorandum") + [t, Spacer(1, 8)]
    for h, paras in MEMO:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    foot = "%s. 2027 renewal review, 6 October 2026." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_plan(path):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="Plan summary, plan years 2023 to 2027",
                          author="Michelle Patrick", subject="", creator="", producer="")
    story = _masthead("Plan summary, plan years 2023 to 2027")
    story.append(Paragraph(
        "Every member employer offers its employees the trust's one medical and pharmacy plan, administered by Hallam "
        "Benefit Administrators on the plan year 1 January to 31 December. The plan design has not changed since 2023 "
        "and is renewed unchanged for 2027.", BODY))
    rows = [["Feature", "In network"], ["Calendar-year deductible (individual / family)", "$1,000 / $2,000"],
            ["Coinsurance", "20%"], ["Out-of-pocket maximum (individual / family)", "$4,500 / $9,000"],
            ["Office visit", "$30 copay"], ["Pharmacy (generic / brand / specialty)", "$10 / $40 / 25% to $250"],
            ["Specific stop-loss (Westerby Specialty Insurance Company)", "$150,000 a member a contract year, 12/15"]]
    t = Table([[Paragraph(c, CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)],
              colWidths=[3.6 * inch, 3.0 * inch])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [Spacer(1, 4), t, Spacer(1, 10)]
    story.append(Paragraph(
        "Contributions are elected by each member employer each September for the next plan year, as a rate per "
        "member per month made up of a claims component, Hallam's administration fee, the specific stop-loss premium "
        "and the trust's reserve load. Employers join the trust on 1 January and may leave at a renewal.", SMALL))
    foot = "%s. Plan summary, plan years 2023 to 2027; issued 30 September 2026." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_rates(path, x):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 elections"
    ws["A1"] = "%s: 2027 contribution elections per member per month" % P.COMPANY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Elected by each member employer in September 2026 for plan year 2027."
    ws.append([])
    ws.append(["Employer", "Employer name", "Elected on", "Claims component", "Administration", "Specific stop-loss",
               "Reserve load", "2027 contribution"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C5A3F")
    rng = np.random.default_rng(W.SEED + 9)
    for eid, name, ind, n in W.EMPLOYERS:
        claims = x["rates"][eid]
        admin = 38.50
        sl = 61.20
        res = round(claims * 0.025, 2)
        day = dt.date(2026, 9, int(rng.integers(4, 29)))
        ws.append([eid, name, day, claims, admin, sl, res, round(claims + admin + sl + res, 2)])
    for row in ws.iter_rows(min_row=5):
        row[2].number_format = "yyyy-mm-dd"
        for c in row[3:8]:
            c.number_format = "#,##0.00"
    for col, w in zip("ABCDEFGH", (9, 34, 12, 15, 14, 16, 12, 17)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["enroll"], "member_id", "Hallam's id for the member"),
        (f["enroll"], "subscriber_id", "Hallam's id for the employee whose coverage the member is on"),
        (f["enroll"], "relationship", "EE employee, SP spouse, CH child"),
        (f["enroll"], "birth_date", "the member's date of birth"),
        (f["enroll"], "employer_id", "the member employer"),
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
        (f["reimb"], "member_ref", "Hallam's member_id as Westerby holds it"),
        (f["reimb"], "paid_in_contract_year", "the member's claims incurred in the contract year and paid within 15 "
                                              "months, dollars"),
        (f["reimb"], "reimbursed", "what Westerby reimbursed, dollars"),
        (f["hcc"], "report_month", "the month of the report, YYYY-MM"),
        (f["hcc"], "paid_ytd", "the member's 2026 claims paid to the end of the report month, dollars"),
        (f["policy"], "contract_basis", "12/15: claims incurred in the contract year and paid within 15 months"),
        (f["rebates"], "rebate_amount", "pharmacy rebates credited to the trust's reserve, dollars"),
        (f["survey"], "median_claims_pmpm_2025", "the survey's median 2025 claims cost per member per month"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["enroll"], "member months by employer", "Hallam eligibility", "2026-10-07", "2023-01 to 2026-09",
         n["enroll"]),
        (f["lag_old"], "claims lag report, legacy platform", "Hallam claims", "2026-06-03", "paid 2023-01 to 2026-05",
         n["lag_old"]),
        (f["lag_new"], "claims lag report, current platform", "Hallam claims", "2026-10-07",
         "paid 2026-05 to 2026-09", n["lag_new"]),
        (f["reimb"], "specific reimbursements", P.CARRIER, "2026-07-31", "contract years 2023 to 2025", n["reimb"]),
        (f["hcc"], "high-cost claimant report", "Hallam claims", "2026-10-07", "2026-01 to 2026-09", n["hcc"]),
        (f["policy"], "specific stop-loss policy schedule", P.CARRIER, "2026-09-30", "2023 to 2027", n["policy"]),
        (f["rates"], "2027 contribution elections", P.COMPANY, "2026-09-30", "plan year 2027", 18),
        (f["memo"], "2027 renewal review memo", P.COMPANY, "2026-10-06", "", ""),
        (f["plan"], "plan summary", P.COMPANY, "2026-09-30", "plan years 2023 to 2027", ""),
        (f["rebates"], "2025 pharmacy rebate statement", "Hallam pharmacy benefits", "2026-05-12", "2025",
         n["rebates"]),
        (f["roster"], "member employer roster", P.COMPANY, "2026-10-01", "", n["roster"]),
        (f["survey"], "small-group plan survey", "Ridgeline Benefits Brokers Association", "2026-04-15", "2025",
         n["survey"]),
        (f["dictionary"], "field descriptions", P.COMPANY, "2026-10-07", "", n["dictionary"]),
    ]
