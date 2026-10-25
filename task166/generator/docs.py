"""task166's documents and office files: the lending policy section that files the forecast, the third-quarter ALM report,
the planning cycle's rate workbook, the data dictionary and the export manifest. Their text is kept here as data so
checks.py and verify.py can quote and execute it."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A           # noqa: E402
import common as K          # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d232a")
GREY = colors.HexColor("#5a626b")
ACCENT = colors.HexColor("#24515e")
RULE = colors.HexColor("#b9c1c8")
HEAD = colors.HexColor("#e5ebef")

F_POLICY = "lending_policy_7-4_he_payoff_forecast.pdf"
F_ALM = "alm_report_2026_q3.pdf"
F_PLAN = "planning_cycle_2027_rates.xlsx"
F_DICT = "data_dictionary.txt"
F_MANIFEST = "export_manifest.csv"

BOLD = Font(name="Calibri", size=11, bold=True)
FILL = PatternFill("solid", fgColor="DDE5EA")

# ------------------------------------------------------------------------------------------------- the policy section
POLICY = [
    ("7.4.1 Purpose", [
        "In 2027 the credit union will test whether a dedicated mortgage loan officer who contacts home equity members "
        "before they pay a loan off keeps more of those members' borrowing with the credit union. The pilot runs in one "
        "regional lending center from Monday 4 January 2027 to Friday 31 December 2027, and the Management Lending "
        "Committee chooses the region at its December 2026 meeting.",
    ]),
    ("7.4.2 Choosing the pilot region", [
        "The pilot opens in the regional lending center whose members are forecast to pay off the most fixed-rate home "
        "equity principal in calendar 2027. The forecast is the one defined in 7.4.3; no other measure decides the "
        "region.",
    ]),
    ("7.4.3 The 2027 home equity payoff forecast", [
        "Population: the fixed-rate closed-end home equity loans on the books at the close of business on 30 November "
        "2026. Loans funded after that date are not in the forecast; home equity lines of credit are a separate product "
        "and are not in it.",
        "Outcome: principal paid ahead of schedule, which is the principal retired when a loan is paid in full before "
        "its maturity date and any principal paid in a month above that month's scheduled principal. Scheduled "
        "principal, including the final scheduled payment of a loan that reaches maturity, is not paid ahead of "
        "schedule, and a balance charged off is not principal paid. A loan the credit union refinances itself is paid "
        "in full.",
        "Window: payments posted from 1 January 2027 to 31 December 2027.",
        "Region: the regional lending center of the county where the collateral property sits, as the county map "
        "assigns it.",
        "Rates: the planning cycle's base case, which states the credit union's posted rates as monthly averages for "
        "each month from December 2026 to December 2027.",
        "Unit: dollars of principal, reported in millions.",
    ]),
    ("7.4.4 Records", [
        "The forecast is prepared from the credit union's own records: the legacy core's home equity loan master from "
        "January 2019 to the conversion on 1 September 2024, the new core's monthly trial balance since the "
        "conversion, the lending system's funded-loan file, and the posted rate sheet archive. Loan numbers changed at "
        "the conversion and the conversion cross-reference links them.",
    ]),
    ("7.4.5 Responsibilities", [
        "The lending analytics manager prepares the forecast and presents it to the Management Lending Committee, "
        "which records the pilot region in its minutes. The ALM and finance manager owns the planning cycle's rates.",
    ]),
]


def sentences(paras):
    import re
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


def policy_text():
    return [p for _, ps in POLICY for p in ps]


def _styles():
    return dict(
        h1=ParagraphStyle("h1", fontName="LibSans-Bold", fontSize=14.5, leading=18.5, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("sub", fontName="LibSans", fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2", fontName="LibSans-Bold", fontSize=10.4, leading=14, textColor=INK, spaceBefore=6,
                          spaceAfter=3),
        body=ParagraphStyle("b", fontName="LibSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5),
        cell=ParagraphStyle("c", fontName="LibSans", fontSize=8.4, leading=10.6, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="LibSans-Bold", fontSize=8.4, leading=10.6, textColor=INK),
        small=ParagraphStyle("sm", fontName="LibSans", fontSize=7.8, leading=10, textColor=GREY, spaceAfter=4))


def _footer(text):
    def foot(canvas, doc):
        canvas.saveState()
        canvas.setFont("LibSans", 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.55 * inch, text)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return foot


def _table(data, widths, head=True):
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def write_policy(path):
    st = _styles()
    s = [Paragraph("Lending Policy, Section 7.4: Home Equity Payoff Forecast and the 2027 Payoff-Retention Pilot", st["h1"]),
         Paragraph("%s. Owner: %s, Chief Lending Officer. Adopted by the Management Lending Committee on 21 October 2026; "
                   "version 1.0." % (K.CU, K.PEOPLE["clo"]), st["sub"])]
    for head, paras in POLICY:
        s.append(Paragraph(head, st["h2"]))
        for p in paras:
            s.append(Paragraph(p, st["body"]))
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.85 * inch,
                            title="Lending Policy 7.4: Home Equity Payoff Forecast", author=K.PEOPLE["clo"],
                            subject="", creator="", producer="")
    foot = _footer("%s  |  Lending Policy  |  Section 7.4  |  v1.0" % K.CU)
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


# ------------------------------------------------------------------------------------------------- the Q3 ALM report
def alm_figures(W):
    """the third-quarter book the ALM report states, from the clean truth at 30 September 2026"""
    t = K.mo(2026, 9)
    bal = [W.bal.get((i, t)) for i in range(W.n)]
    live = [b for b in bal if b]
    he = sum(live)
    rates = [(W.bal.get((i, t)), W.r2[i]) for i in range(W.n) if W.bal.get((i, t))]
    wac = sum(b * r for b, r in rates) / he
    return dict(he=he, wac=wac, count=len(live))


ALM_BALANCE = [("Cash and short-term investments", 0.312), ("Investment securities", 0.684),
               ("First mortgage loans", 1.418), ("Fixed-rate home equity loans", None),
               ("Home equity lines of credit", 0.094), ("Auto loans", 0.731), ("Credit card and other consumer", 0.188),
               ("Commercial and member business loans", 0.246), ("Allowance for credit losses", -0.031),
               ("Premises, NCUSIF deposit and other assets", 0.122)]
ALM_NEV = [("-200", 2.6, 12.1), ("-100", 1.6, 11.8), ("Base", 0.0, 11.4), ("+100", -4.1, 10.6), ("+200", -8.9, 9.7),
           ("+300", -13.8, 8.8)]
ALM_NII = [("-200 ramp", -2.9), ("-100 ramp", -1.3), ("+100 ramp", 0.8), ("+200 ramp", 1.4)]


def write_alm(path, W):
    st = _styles()
    f = alm_figures(W)
    he_b = f["he"] / 1e9
    total = sum(v for _, v in ALM_BALANCE if v is not None) + he_b
    s = [Paragraph("Asset/Liability Management Report, Third Quarter 2026", st["h1"]),
         Paragraph("%s. Prepared by %s, ALM and Finance Manager, for the Asset/Liability Committee meeting of 20 October "
                   "2026. Positions at 30 September 2026." % (K.CU, K.PEOPLE["alm"]), st["sub"])]
    s.append(Paragraph("1. Balance sheet", st["h2"]))
    s.append(Paragraph("Total assets were $%.2f billion at 30 September 2026. Fixed-rate home equity loans stood at "
                       "$%.1f million across %s loans at a weighted average note rate of %.2f per cent." %
                       (total, f["he"] / 1e6, "{:,}".format(f["count"]), f["wac"]),
                       st["body"]))
    data = [[Paragraph("Assets ($ billions)", st["cellb"]), Paragraph("30 Sep 2026", st["cellb"])]]
    for a, v in ALM_BALANCE:
        v = he_b if v is None else v
        data.append([Paragraph(a, st["cell"]), Paragraph("%.3f" % v, st["cell"])])
    data.append([Paragraph("Total assets", st["cellb"]), Paragraph("%.3f" % total, st["cellb"])])
    s.append(_table(data, [3.6 * inch, 1.3 * inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("2. Net economic value and net interest income", st["h2"]))
    s.append(Paragraph("Instantaneous parallel shocks to the posted rate curves; ramp scenarios over twelve months. All "
                       "results are within the limits in the ALM Policy (net economic value ratio not below 7.0 per "
                       "cent in any shock).", st["body"]))
    data = [[Paragraph(h, st["cellb"]) for h in ("Shock (bp)", "NEV change (%)", "NEV ratio (%)")]]
    for a, b, c in ALM_NEV:
        data.append([Paragraph(a, st["cell"]), Paragraph("%.1f" % b, st["cell"]), Paragraph("%.1f" % c, st["cell"])])
    s.append(_table(data, [1.4 * inch, 1.4 * inch, 1.4 * inch]))
    s.append(Spacer(1, 6))
    data = [[Paragraph(h, st["cellb"]) for h in ("Scenario", "Net interest income, next 12 months (%)")]]
    for a, b in ALM_NII:
        data.append([Paragraph(a, st["cell"]), Paragraph("%.1f" % b, st["cell"])])
    s.append(_table(data, [1.4 * inch, 3.0 * inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("3. Liquidity and the planning cycle", st["h2"]))
    s.append(Paragraph("Liquid assets were 11.9 per cent of shares and deposits. The 2027 planning cycle's rates were "
                       "approved by ALCO on 22 September 2026; the base case and two alternatives are in the planning "
                       "workbook.", st["body"]))
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.85 * inch, title="ALM Report Q3 2026",
                            author=K.PEOPLE["alm"], subject="", creator="", producer="")
    foot = _footer("%s  |  ALM Report  |  Q3 2026" % K.CU)
    doc.build(s, onFirstPage=foot, onLaterPages=foot)
    return f


# ------------------------------------------------------------------------------------------------- the planning workbook
def plan_rows(shift=0.0):
    rows = []
    for k, o in enumerate(K.FORE):
        y, m = K.ym(o)
        r30 = WD.PLAN_30[k] + shift
        rows.append([dt.date(y, m, 1), round(r30, 2), round(r30 - WD.M15_SPREAD, 2), round(r30 + WD.HE_SPREAD[120], 2),
                     round(r30 + WD.HE_SPREAD[180], 2), round(r30 + WD.HE_SPREAD[240], 2),
                     round(PRIME[k] + shift, 2)])
    return rows


PRIME = [7.00, 7.00, 6.75, 6.75, 6.50, 6.50, 6.50, 6.25, 6.25, 6.25, 6.25, 6.25, 6.25]
PLAN_HEAD = ["Month", "30-year fixed mortgage", "15-year fixed mortgage", "Home equity fixed 10-year",
             "Home equity fixed 15-year", "Home equity fixed 20-year", "Prime rate"]


def write_plan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Base case"
    for title, shift in (("Base case", 0.0), ("Rates up 100", 1.0), ("Rates down 100", -1.0)):
        if title != "Base case":
            ws = wb.create_sheet(title)
        ws.append(PLAN_HEAD)
        for c in ws[1]:
            c.font = BOLD
            c.fill = FILL
        for r in plan_rows(shift):
            ws.append(r)
        for row in ws.iter_rows(min_row=2):
            row[0].number_format = "mmm yyyy"
            for c in row[1:]:
                c.number_format = "0.00"
        ws.column_dimensions["A"].width = 11
        for col in "BCDEFG":
            ws.column_dimensions[col].width = 15
    ws = wb.create_sheet("About")
    for line in ["2027 planning cycle: rate scenarios",
                 "Approved by ALCO on 22 September 2026. Owner: %s, ALM and Finance Manager." % K.PEOPLE["alm"],
                 "Each rate is the monthly average of the credit union's posted rate for the product, in per cent.",
                 "The base case is the plan; the alternatives are parallel shifts used for the net interest income "
                 "ramps."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 110
    wb.save(path)


# ------------------------------------------------------------------------------------------------- the dictionary and manifest
DICT = [
    (R.F_LEGACY, "Legacy core system, home equity loan master as archived at the conversion. One row per fixed-rate "
     "home equity loan on the books at any month-end from 31 December 2018 to 31 August 2024.", [
        ("LOAN_NO", "Legacy loan number: the legacy member number and a two-digit loan suffix."),
        ("MBR_NO", "Legacy member number."),
        ("PROD_CD", "HEF10, HEF15 or HEF20: fixed-rate home equity, term in years."),
        ("OPEN_DT", "Date funded (MM/DD/YYYY)."),
        ("ORIG_AMT", "Amount funded, dollars."),
        ("NOTE_RT", "Note rate, per cent."),
        ("TERM_MOS", "Term in months."),
        ("PMT_AMT", "Monthly principal and interest payment, dollars."),
        ("MAT_DT", "Maturity date."),
        ("BAL_12_31_2018", "Principal balance at 31 December 2018; blank for loans funded after that date."),
        ("STATUS", "CLOSED: the loan closed before the conversion. CNV: open at the conversion and moved to the new core."),
        ("CLOSE_DT", "Date the loan closed."),
        ("CLOSE_CD", "PIF paid in full by the member; MAT final scheduled payment at maturity; CO charged off."),
        ("PRIN_AT_CLOSE", "Principal retired or charged off when the loan closed, dollars."),
        ("BAL_AT_CONV", "Principal balance at 31 August 2024 for loans moved to the new core."),
    ]),
    (R.F_CORE, "New core system, monthly trial balance of fixed-rate home equity loans. One row per loan per month-end "
     "from 30 September 2024 to 30 November 2026, including the month a loan closed.", [
        ("LoanNumber", "Loan number in the new core."),
        ("MemberNumber", "Member number in the new core."),
        ("ProductCode", "FHE120, FHE180 or FHE240: fixed-rate home equity, term in months."),
        ("AsOfDate", "Month-end date of the row."),
        ("OpenDate", "Date funded."),
        ("OriginalAmount", "Amount funded, dollars."),
        ("InterestRate", "Note rate as a decimal fraction."),
        ("TermMonths", "Term in months."),
        ("PaymentAmount", "Monthly principal and interest payment, dollars."),
        ("PrincipalBalance", "Principal balance at the month-end, dollars."),
        ("ScheduledPrincipal", "Principal due in the month under the loan's payment schedule, dollars."),
        ("PrincipalPaid", "Principal posted in the month, dollars."),
        ("InterestPaid", "Interest posted in the month, dollars."),
        ("LoanStatus", "ACTIVE; PIF paid in full by the member; MAT final scheduled payment at maturity; CHGOFF charged off."),
        ("CloseDate", "Date the loan closed, on the row of the month it closed."),
        ("DaysPastDue", "Days the oldest unpaid installment was past due at the month-end."),
    ]),
    (R.F_XREF, "Conversion cross-reference. One row per loan moved from the legacy core to the new core on 1 September "
     "2024.", [
        ("legacy_loan_no", "Legacy loan number."), ("loan_number", "New core loan number."),
        ("legacy_member_no", "Legacy member number."), ("member_number", "New core member number."),
        ("converted_on", "Conversion date."),
    ]),
    (R.F_LOS, "Lending system, funded fixed-rate home equity loans since January 2009. One row per funded loan, as "
     "underwritten. The senior lien fields are the first mortgage tradeline on the applicant's credit report at "
     "application.", [
        ("application_id", "Application identifier."), ("funded_date", "Date funded."),
        ("loan_number", "Core loan number assigned at funding (the legacy number for loans funded before September 2024)."),
        ("member_number", "Member number at funding."),
        ("property_street", "Collateral property street address."), ("property_city", "Collateral property city."),
        ("property_county", "Collateral property county."), ("property_state", "Collateral property state."),
        ("property_zip", "Collateral property ZIP code."),
        ("appraised_value", "Appraised or automated value of the property at application, dollars."),
        ("cltv_pct", "Combined loan-to-value at funding, per cent."),
        ("credit_score", "Credit score at application."),
        ("dti_pct", "Debt-to-income ratio at application, per cent."),
        ("loan_amount", "Amount funded, dollars."), ("note_rate_pct", "Note rate, per cent."),
        ("term_months", "Term in months."),
        ("senior_lien_creditor", "Creditor name on the first mortgage tradeline."),
        ("senior_lien_opened", "Month the first mortgage was opened (MMYYYY)."),
        ("senior_lien_original_amount", "Original amount of the first mortgage, dollars."),
        ("senior_lien_term_months", "Term of the first mortgage in months, where the tradeline reported it."),
        ("senior_lien_balance", "Balance of the first mortgage as last reported, dollars."),
        ("senior_lien_balance_as_of", "Month of that balance (MMYYYY)."),
        ("senior_lien_monthly_payment", "Monthly payment on the first mortgage as the tradeline reported it, dollars."),
        ("senior_lien_note_rate_pct", "Note rate of the first mortgage, per cent, for a loan funded with the purchase of "
         "the property, where the first mortgage's terms came from the purchase file; blank otherwise."),
    ]),
    (R.F_SERV, "Mortgage servicing system, the credit union's first mortgages: those active at 30 November 2026 and those "
     "paid in full since 1 January 2025.", [
        ("mortgage_loan_number", "Mortgage loan number."), ("member_number", "Member number in the new core."),
        ("property_street", "Property street address."), ("property_city", "Property city."),
        ("property_zip", "Property ZIP code."), ("note_date", "Note date."),
        ("original_amount", "Original principal, dollars."), ("note_rate_pct", "Note rate, per cent."),
        ("term_months", "Term in months."), ("maturity_date", "Maturity date."),
        ("status", "ACTIVE or PAID IN FULL."), ("paid_in_full_date", "Date paid in full."),
        ("principal_paid_at_payoff", "Principal retired at the payoff, dollars."),
        ("principal_balance_2026_11_30", "Principal balance at 30 November 2026, dollars."),
    ]),
    (R.F_MAP, "County map of the regional lending centers.", [
        ("county", "County."), ("state", "State."), ("regional_lending_center", "Regional lending center."),
        ("effective_date", "Date the assignment took effect."),
    ]),
    (R.F_RATES, "Posted rate sheet archive. One row per product per rate sheet; a sheet takes effect on its date and "
     "stays in effect until the next sheet.", [
        ("effective_date", "Date the sheet took effect."), ("product", "Product."),
        ("rate_pct", "Posted rate, per cent."), ("apr_pct", "Annual percentage rate as posted, per cent."),
    ]),
    (R.F_HELOC, "Home equity lines of credit at 30 November 2026.", [
        ("line_number", "Line number."), ("member_number", "Member number."), ("open_date", "Date opened."),
        ("credit_limit", "Credit limit, dollars."), ("balance_2026_11_30", "Balance at 30 November 2026, dollars."),
        ("index", "Rate index."), ("margin_pct", "Margin over the index, per cent."),
        ("rate_pct", "Rate at 30 November 2026, per cent."), ("draw_period_end", "End of the draw period."),
        ("line_status", "OPEN or FROZEN."), ("property_county", "Collateral property county."),
        ("property_zip", "Collateral property ZIP code."),
    ]),
    (R.F_HPI, "Quarterly all-transactions house price index by county, 1995 Q1 = 100.", [
        ("county", "County."), ("state", "State."), ("quarter", "Quarter."), ("index_1995q1_100", "Index level."),
    ]),
    (A.F_LOG, "Payoff statement system. One row per payoff statement request: issued statements, updated statements "
     "for a later good-through date, and requests voided before a statement was issued. The system was out of service "
     "from 9 to 20 March 2026 for its upgrade.", [
        ("statement_id", "Statement identifier."), ("issued_utc", "Time the statement was issued or the request voided, UTC."),
        ("channel", "PORTAL, FAX or EMAIL."), ("requested_by", "Who asked for the statement."),
        ("account_reference", "The account the request named."),
        ("product_on_file", "HE home equity (loans and lines); MTG first mortgage."),
        ("good_through_date", "Date the quoted amount is good through."),
        ("statement_amount", "Amount needed to pay in full on the good-through date, dollars."),
        ("statement_status", "ISSUED, UPDATED or VOID."), ("prepared_by", "Initials of the payoff desk staff member."),
    ]),
    (A.F_MANUAL, "Payoff desk, statements prepared by hand from 9 to 20 March 2026. One row per statement prepared.", [
        ("Date received", "Date the request arrived."), ("Requested by", "Who asked for the statement."),
        ("Borrower", "Borrower's last name."), ("Property", "Property address."),
        ("Liens", "The liens the statement quoted."), ("Amount quoted", "Amount quoted, dollars."),
        ("Good through", "Date the amount is good through."), ("Prepared by", "Initials."),
    ]),
    (F_PLAN, "2027 planning cycle rates: the base case and two alternatives, monthly averages of posted rates, per cent.",
     []),
]


def write_dictionary(path):
    lines = ["%s data dictionary" % K.CU, "Files pulled on 3 December 2026 for the 2027 home equity payoff forecast.", ""]
    for f, desc, fields in DICT:
        lines.append(f)
        lines.append("  " + desc)
        for a, b in fields:
            lines.append("    %-30s %s" % (a, b))
        lines.append("")
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines))


MANIFEST = [
    (R.F_LEGACY, "Legacy core (archived)", "2026-12-03", "Loans on the books at any month-end, Dec 2018 to Aug 2024"),
    (R.F_CORE, "New core", "2026-12-03", "Month-ends Sep 2024 to Nov 2026"),
    (R.F_XREF, "Conversion project", "2024-09-03", "Loans moved on 1 Sep 2024"),
    (R.F_LOS, "Lending system", "2026-12-03", "Fixed-rate home equity loans funded Jan 2009 to Nov 2026"),
    (R.F_SERV, "Mortgage servicing system", "2026-12-03", "First mortgages active at 30 Nov 2026 or paid since 1 Jan 2025"),
    (R.F_MAP, "Lending administration", "2026-12-03", "Counties served"),
    (R.F_RATES, "Pricing desk", "2026-12-03", "Rate sheets 3 Dec 2018 to 30 Nov 2026"),
    (R.F_HELOC, "New core", "2026-12-03", "Lines open at 30 Nov 2026"),
    (R.F_HPI, "ALM (market data)", "2026-11-12", "2019 Q1 to 2026 Q3"),
    (A.F_LOG, "Payoff statement system", "2026-12-03", "Requests 1 Oct 2025 to 30 Nov 2026"),
    (A.F_MANUAL, "Payoff desk", "2026-03-23", "Statements prepared by hand 9 to 20 Mar 2026"),
    (F_PLAN, "ALM", "2026-09-22", "Planning cycle 2027"),
    (F_POLICY, "Lending administration", "2026-10-21", "Lending Policy section 7.4, version 1.0"),
    (F_ALM, "ALM", "2026-10-16", "Positions at 30 Sep 2026"),
    (F_DICT, "Lending analytics", "2026-12-03", "Fields of the data files"),
]


def write_manifest(path, n):
    rows = []
    for f, sysname, pulled, cov in MANIFEST:
        rows.append([f, sysname, pulled, cov, n.get(f, "")])
    rows.append([F_MANIFEST, "Lending analytics", "2026-12-03", "This list", ""])
    return K.write_csv(path, ["file", "source_system", "pulled_or_issued", "coverage", "rows"], rows)


def write_all(out, W, n):
    write_policy(os.path.join(out, F_POLICY))
    alm = write_alm(os.path.join(out, F_ALM), W)
    write_plan(os.path.join(out, F_PLAN))
    write_dictionary(os.path.join(out, F_DICT))
    n[F_MANIFEST] = write_manifest(os.path.join(out, F_MANIFEST), n)
    return alm
