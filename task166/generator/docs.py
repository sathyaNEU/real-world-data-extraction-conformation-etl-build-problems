"""task166 workbooks and documents: the credit administration maturity log, ALCO's planning cycle workbook, the
treasury system's swap register, the deposit study, the hedging policy, the third-quarter ALM report and the extract
notes. Their text is kept here as data so checks.py and verify.py can quote and execute it."""
from __future__ import annotations

import datetime as dt
import os
import re

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import records as R         # noqa: E402
import swaps as SW          # noqa: E402
import world as WD          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d232a")
GREY = colors.HexColor("#5a626b")
ACCENT = colors.HexColor("#1f4e5f")
RULE = colors.HexColor("#b9c1c8")
HEAD = colors.HexColor("#e5ebef")

F_LOG = "cre_maturity_log.xlsx"
F_PLAN = "planning_cycle_2027_base_case.xlsx"
F_REGISTER = "swap_register_20261130.xlsx"
F_NMD = "deposit_decay_study_2026.xlsx"
F_POLICY = "balance_sheet_hedging_policy.pdf"
F_ALM = "alm_report_2026_q3.pdf"
F_NOTES = "extract_notes.txt"

BOLD = Font(name="Calibri", size=11, bold=True)
BODY = Font(name="Calibri", size=11)
FILL = PatternFill("solid", fgColor="DDE5EA")


def _sheet(ws, header, rows, widths=None, fmt=None):
    ws.append(header)
    for c in ws[1]:
        c.font = BOLD
        c.fill = FILL
    for r in rows:
        ws.append(r)
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
    if fmt:
        for col, f in fmt.items():
            for cell in ws[col][1:]:
                cell.number_format = f
    ws.freeze_panes = "A2"


# ------------------------------------------------------------------------------------------------- maturity log
LOG_A = ["Obligation", "Property", "Prop Type", "Orig Amt", "Rate", "Maturity", "Balance", "Disposition", "New Maturity"]
LOG_B = ["Obligation No.", "Property No.", "Property Type", "Original Principal", "Note Rate", "Maturity Date",
         "Principal at Maturity", "Outcome", "Extended To"]
PT_A = {"MF": "MF", "OFF": "OFF", "RET": "RTL", "IND": "IND", "MIX": "MXD", "HOT": "HTL"}
OUT_B = {"PO": "Paid at maturity", "EXT": "Extended", "EXT-S": "Extended, sale pending",
         "PO-EXT": "Paid at extended maturity", "SA": "Transferred to special assets"}


def write_log(path, W):
    log = R.maturity_log(W)
    wb = Workbook()
    wb.remove(wb.active)
    for y in sorted(log):
        ws = wb.create_sheet(str(y))
        rows = []
        if y < 2020:
            for r in log[y]:
                L = r["L"]
                rows.append([r["ob"], "%d" % r["prop"], PT_A[L["ptype"]], round(L["b0"], 0), L["r0"], r["date"],
                             round(r["bal"], 2), r["out"], r["new"]])
            _sheet(ws, LOG_A, rows, widths=[13, 10, 10, 13, 8, 12, 15, 12, 13],
                   fmt={"D": "#,##0", "E": "0.00", "F": "mm/dd/yyyy", "G": "#,##0.00", "I": "mm/dd/yyyy"})
        else:
            for r in log[y]:
                L = r["L"]
                rows.append([r["ob"], "%d" % r["prop"], R.PT_NAME[L["ptype"]], round(L["b0"], 2), L["r0"], r["date"],
                             round(r["bal"], 2), OUT_B[r["out"]], r["new"]])
            _sheet(ws, LOG_B, rows, widths=[15, 13, 14, 18, 10, 14, 20, 26, 13],
                   fmt={"D": "#,##0.00", "E": "0.000", "F": "yyyy-mm-dd", "G": "#,##0.00", "I": "yyyy-mm-dd"})
    wb.save(path)
    return sum(len(v) for v in log.values())


# ------------------------------------------------------------------------------------------------- planning cycle
PLAN_NOTE = [
    "ALCO planning cycle: 2027 plan, base case",
    "Approved by ALCO on Monday 21 September 2026. Owner: %s, ALM." % K.PEOPLE["alm"],
    "Base-case zero rates are continuously compounded, by tenor in years, read by linear interpolation between "
    "tenors and held flat beyond 30 years.",
    "Product rates are the bank's posted rates assumed for each month of the plan; after December 2027 they are held "
    "at their December 2027 level.",
]
PLAN_MONTHS = [K.mo(2026, 12) + i for i in range(13)]


def write_plan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cycle"
    for i, line in enumerate(PLAN_NOTE):
        ws.cell(row=i + 1, column=1, value=line).font = BOLD if i == 0 else BODY
    ws.column_dimensions["A"].width = 120
    z = wb.create_sheet("Zero curve")
    _sheet(z, ["Tenor (years)", "Zero rate (%)"],
           [[round(t, 6) if t >= 1 else round(t, 6), r] for t, r in zip(K.CURVE_TENORS, K.CURVE_ZEROS)],
           widths=[15, 15], fmt={"A": "0.0000", "B": "0.00"})
    p = wb.create_sheet("Product rates")
    rows = []
    for o in PLAN_MONTHS:
        y, m = K.ym(o)
        rows.append([dt.date(y, m, 1), K.PLAN_MORTGAGE, K.PLAN_MORTGAGE_15, K.PLAN_CRE])
    _sheet(p, ["Month", "Portfolio jumbo 30-year fixed (%)", "Conforming 15-year fixed (%)",
               "Commercial real estate 5-year fixed (%)"], rows, widths=[12, 32, 30, 40],
           fmt={"A": "mmm yyyy", "B": "0.00", "C": "0.00", "D": "0.00"})
    wb.save(path)


# ------------------------------------------------------------------------------------------------- swap register
REG_COLS = ["Trade No.", "Book", "Strategy", "Hedged item", "Counterparty", "Cleared", "Clearing ref", "Bank pays",
            "Notional (USD)", "Fixed rate (%)", "Floating index", "Trade date", "Effective date", "Maturity date",
            "Amortizing", "Status", "Terminated on"]


def register_rows(S):
    rows = []
    for t in S["trades"]:
        cur = t["notional"]
        if t["key"] in S["sched"]:
            cur = [n for a, b, n in S["sched"][t["key"]] if a <= K.AS_OF < b][0]
        rows.append([t["id"], t["book"], t["strategy"], t["item"], t["cpty"], "Y" if t["cleared"] else "N",
                     t["ccp_id"] or "", "FIXED" if t["dir"] == "PAY" else "FLOAT", float(cur), t["rate"],
                     "USD-SOFR-OIS COMPOUND", t["trade"], t["eff"], t["mat"], "Y" if t["amort"] else "N", t["status"],
                     t.get("terminated")])
    rows.sort(key=lambda r: r[0])
    return rows


def write_register(path, S):
    wb = Workbook()
    ws = wb.active
    ws.title = "Trades"
    rows = register_rows(S)
    _sheet(ws, REG_COLS, rows, widths=[11, 10, 17, 52, 26, 8, 12, 10, 17, 13, 24, 12, 13, 13, 11, 12, 14],
           fmt={"I": "#,##0.00", "J": "0.000", "L": "yyyy-mm-dd", "M": "yyyy-mm-dd", "N": "yyyy-mm-dd",
                "Q": "yyyy-mm-dd"})
    wb.save(path)
    return len(rows)


# ------------------------------------------------------------------------------------------------- deposit study
NMD_PRODUCTS = [("Non-interest-bearing demand", 6.9, 0.00, 7.8), ("Interest checking", 4.1, 0.18, 6.2),
                ("Savings", 2.6, 0.22, 5.4), ("Money market", 5.3, 0.46, 3.1), ("Business money market", 3.2, 0.58, 2.4)]


def write_nmd(path):
    g = K.rng(50)
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    rows = []
    for name, bal, beta, life in NMD_PRODUCTS:
        rows.append([name, round(bal * 1000 + float(g.uniform(-40, 40)), 1), round(beta + float(g.normal(0, 0.01)), 3),
                     round(life + float(g.normal(0, 0.15)), 2), round(100 / (life * 12) * 1.9, 3)])
    _sheet(ws, ["Product", "Balance 30 Jun 2026 ($ millions)", "Deposit beta", "Average life (years)",
                "Monthly decay (%)"], rows, widths=[30, 30, 14, 20, 18])
    h = wb.create_sheet("Vintage decay")
    rows = []
    for name, bal, beta, life in NMD_PRODUCTS:
        for yrs in range(1, 11):
            rows.append([name, yrs, round(100 * np.exp(-yrs / life) * float(np.exp(g.normal(0, 0.02))), 1)])
    _sheet(h, ["Product", "Years since account opening", "Balance retained (% of opening cohort)"], rows,
           widths=[30, 28, 38])
    wb.save(path)


# ------------------------------------------------------------------------------------------------- the hedging policy
POLICY = [
    ("1. Purpose", [
        "This policy governs the interest-rate swaps Carrick Valley Bank uses to manage the economic value of its "
        "balance sheet, and how the Asset/Liability Committee (ALCO) designates them.",
    ]),
    ("2. The hedge programme", [
        "The hedge programme is the swaps in the treasury system's ALM book. Overlays are pay-fixed swaps designated "
        "against a fixed-rate asset pool; funding hedges are pay-fixed swaps on the interest the bank pays on its "
        "funding; loan hedges are receive-fixed swaps on the interest it earns on floating-rate loans. Swaps the bank "
        "writes for its customers, and the swaps that offset them, are not part of the programme.",
        "A swap is in effect on a date when its effective date is on or before that date and its maturity date, and the "
        "date it was terminated where it has been terminated early, are after it.",
        "The notional of pay-fixed swaps in effect may not exceed 15 per cent of total assets at any quarter-end.",
    ]),
    ("3. Designating an overlay", [
        "ALCO designates each overlay, before it is traded, against the eligible pool in Schedule A whose loss in "
        "economic value under a parallel rise of 200 basis points, averaged over the month-ends of the overlay's first "
        "twelve months, is largest.",
        "A pool is eligible if its principal outstanding at the close on the as-of date of the designation memo is at "
        "least the overlay's notional. A pool is the positions in it at the close on that date; positions added after "
        "it are not part of it.",
        "The loss in economic value of a pool at a month-end is the present value at that month-end of the pool's "
        "expected cash flows after that month-end, discounted on the base-case zero curve of ALCO's most recent "
        "planning cycle, the same zero rates at every month-end, less their present value on that curve shifted up by "
        "200 basis points. The same expected cash flows are used in both. Time is measured in years from the "
        "month-end, a month counting as a twelfth of a year, and each cash flow is placed at the end of the month in "
        "which it is paid.",
        "Expected cash flows are the principal and interest the bank expects each position to pay under the planning "
        "cycle's base case, before credit losses.",
    ]),
    ("4. Documentation", [
        "The designation memo goes to ALCO's chair before the trade. It names the pool, gives its averaged loss in "
        "millions of dollars, and states the programme's notional in effect at each quarter-end of the overlay's "
        "first year.",
    ]),
]
SCHEDULE_A = [
    ("Treasury ladder", "United States Treasury notes held in the available-for-sale portfolio."),
    ("Agency MBS", "Agency mortgage pass-through securities bought in 2020 and 2021."),
    ("2023-24 residential mortgages", "First-lien residential mortgages held for investment, originated from "
                                      "1 January 2023 to 31 December 2024."),
    ("Indirect auto loans", "Auto loans bought from dealers."),
    ("Fixed-rate commercial real estate", "Commercial real estate term loans with a fixed note rate."),
]


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


def policy_sentences():
    return sentences([p for _, ps in POLICY for p in ps] + [b for _, b in SCHEDULE_A])


def _styles():
    return dict(
        h1=ParagraphStyle("h1", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("sub", fontName="LibSans", fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2", fontName="LibSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=6,
                          spaceAfter=3),
        body=ParagraphStyle("b", fontName="LibSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5),
        cell=ParagraphStyle("c", fontName="LibSans", fontSize=8.6, leading=10.8, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="LibSans-Bold", fontSize=8.6, leading=10.8, textColor=INK),
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


def _table(data, widths, st, head=True):
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def write_policy(path):
    st = _styles()
    s = [Paragraph("Balance Sheet Hedging Policy", st["h1"]),
         Paragraph("%s. Owner: %s, Treasurer. Approved by ALCO on 17 March 2026 and by the Board Risk Committee on "
                   "24 March 2026. Version 1.0." % (K.HOLDCO, K.PEOPLE["treasurer"]), st["sub"])]
    for head, paras in POLICY:
        s.append(Paragraph(head, st["h2"]))
        for p in paras:
            s.append(Paragraph(p, st["body"]))
    s.append(Paragraph("Schedule A. Pools for overlay designation", st["h2"]))
    data = [[Paragraph("Pool", st["cellb"]), Paragraph("Positions", st["cellb"])]]
    for a, b in SCHEDULE_A:
        data.append([Paragraph(a, st["cell"]), Paragraph(b, st["cell"])])
    s.append(_table(data, [2.2 * inch, 4.5 * inch], st))
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.85 * inch, title="Balance Sheet Hedging Policy",
                            author=K.PEOPLE["treasurer"], subject="", creator="", producer="")
    doc.build(s, onFirstPage=_footer("%s  |  Treasury  |  Balance Sheet Hedging Policy v1.0" % K.HOLDCO),
              onLaterPages=_footer("%s  |  Treasury  |  Balance Sheet Hedging Policy v1.0" % K.HOLDCO))


# ------------------------------------------------------------------------------------------------- the Q3 ALM report
ALM_EVE = [("-100", 1.9), ("+100", -5.4), ("+200", -11.6), ("+300", -17.9)]
ALM_LIMIT = {"+100": -8.0, "+200": -15.0, "+300": -22.0, "-100": -8.0}
ALM_NII = [("-100 ramp", -1.8), ("+100 ramp", 1.1), ("+200 ramp", 1.9)]
ALM_BALANCE = [("Cash and due from banks", 1.48), ("Securities available for sale", 4.31), ("Loans held for sale", 0.06),
               ("Commercial and industrial loans", 4.62), ("Commercial real estate loans", 6.93),
               ("Residential mortgages", 7.38), ("Home equity and consumer loans", 1.36), ("Indirect auto loans", 1.33),
               ("Other assets", 3.68)]


def cre_book(W):
    """the commercial real estate book at the as-of: principal, and the share graded watch or worse"""
    fx = [(R.cre_balance_asof(L), R.risk_grade(L)) for L in W.cre if R.cre_alive(L)]
    fl = [(F["bal"], F["grade"]) for F in W.cre_float]
    tot = sum(b for b, _ in fx + fl)
    w6 = sum(b for b, g_ in fx + fl if g_ >= 6) / tot
    w7 = sum(b for b, g_ in fx + fl if g_ >= 7) / tot
    return tot, w6, w7


ALM_TOTAL = 38.06          # total assets at 30 September 2026, $ billions


def alm_balance(W):
    """the balance sheet at 30 September: the commercial real estate line is the book, C&I takes up the rest"""
    tot, _, _ = cre_book(W)
    cre = round(tot / 1e9 + 0.04, 2)
    others = sum(v for k, v in ALM_BALANCE if k not in ("Commercial real estate loans", "Commercial and industrial loans"))
    rows = []
    for k, v in ALM_BALANCE:
        if k == "Commercial real estate loans":
            v = cre
        elif k == "Commercial and industrial loans":
            v = round(ALM_TOTAL - others - cre, 2)
        rows.append((k, v))
    return rows


def write_alm(path, W):
    st = _styles()
    bal = alm_balance(W)
    tot = sum(v for _, v in bal)
    _, w6, w7 = cre_book(W)
    s = [Paragraph("ALM Report, Third Quarter 2026", st["h1"]),
         Paragraph("%s. Positions at Wednesday 30 September 2026. Prepared by %s, ALM, for ALCO's meeting of 19 October "
                   "2026." % (K.BANK, K.PEOPLE["alm"]), st["sub"]),
         Paragraph("This report answers where the balance sheet stands against ALCO's interest-rate risk limits at the "
                   "quarter-end.", st["body"]),
         Paragraph("Economic value of equity", st["h2"]),
         Paragraph("Economic value of equity at 30 September was $3.41 billion. Its change under instantaneous parallel "
                   "shifts of the quarter-end market curve:", st["body"])]
    data = [[Paragraph(x, st["cellb"]) for x in ("Shift (basis points)", "Change in EVE (%)", "Limit (%)")]]
    for k, v in ALM_EVE:
        data.append([Paragraph(k, st["cell"]), Paragraph("%.1f" % v, st["cell"]), Paragraph("%.1f" % ALM_LIMIT[k], st["cell"])])
    s.append(_table(data, [1.8 * inch, 1.8 * inch, 1.4 * inch], st))
    s.append(Spacer(1, 6))
    s.append(Paragraph("The +200 basis point change used 77 per cent of its limit, against 71 per cent at 30 June; the "
                       "+300 change used 81 per cent. ALCO's November meeting will consider a pay-fixed overlay.",
                       st["body"]))
    s.append(Paragraph("Net interest income", st["h2"]))
    data = [[Paragraph(x, st["cellb"]) for x in ("Scenario, twelve months", "Change in NII (%)")]]
    for k, v in ALM_NII:
        data.append([Paragraph(k, st["cell"]), Paragraph("%.1f" % v, st["cell"])])
    s.append(_table(data, [2.4 * inch, 1.8 * inch], st))
    s.append(Paragraph("Credit quality", st["h2"]))
    s.append(Paragraph("Commercial real estate loans graded watch or worse (grades 6 to 8) were %.1f per cent of the "
                       "commercial real estate book at 30 September, against %.1f per cent at 30 June; special mention "
                       "and substandard loans (grades 7 and 8) were %.1f per cent." %
                       (100 * w6, 100 * w6 - 0.6, 100 * w7), st["body"]))
    s.append(Paragraph("Balance sheet", st["h2"]))
    data = [[Paragraph(x, st["cellb"]) for x in ("Assets at 30 September 2026", "$ billions")]]
    for k, v in bal:
        data.append([Paragraph(k, st["cell"]), Paragraph("%.2f" % v, st["cell"])])
    data.append([Paragraph("Total assets", st["cellb"]), Paragraph("%.2f" % tot, st["cellb"])])
    s.append(_table(data, [3.4 * inch, 1.4 * inch], st))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Report version 1.2, issued 14 October 2026. Questions to %s." % K.PEOPLE["alm"], st["small"]))
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.85 * inch, title="ALM Report, Third Quarter 2026",
                            author=K.PEOPLE["alm"], subject="", creator="", producer="")
    doc.build(s, onFirstPage=_footer("%s  |  ALM  |  Q3 2026" % K.BANK), onLaterPages=_footer("%s  |  ALM  |  Q3 2026" % K.BANK))


# ------------------------------------------------------------------------------------------------- the extract notes
def notes_text(n):
    P = K.PEOPLE
    L = []
    w = L.append
    w("Overlay designation memo: files pulled Thursday 3 December 2026")
    w("Prepared by %s, ALM. Positions are as of the close on Monday 30 November 2026." % P["analyst"])
    w("")
    w("servicing_monthly_legacy_2023-01_2024-08.csv (%s rows)" % format(n[R.F_LEGACY], ","))
    w("  The legacy servicing platform's monthly extract of the residential loans originated in 2023 and 2024,")
    w("  cycles January 2023 to August 2024. One row per loan per cycle; the platform was retired after the August")
    w("  2024 cycle. The last row is the platform's trailer (record count, total END_PRIN).")
    w("  PORTF: PORT held for investment, HFS held for sale. ORIG_DT and LIQ_DT are MMDDYYYY; NOTE_RT is per cent.")
    w("  BEG_PRIN principal at the start of the cycle; SCHED_PRIN scheduled principal paid; CURTAIL principal paid")
    w("  ahead of schedule on a loan that stays open; PIF_PRIN principal paid off, or delivered on a sale, on the")
    w("  loan's last cycle; END_PRIN principal at the end of the cycle. STAT: C active, P paid in full, S sold.")
    w("")
    w("servicing_monthly_2024-09_2026-11.csv (%s rows)" % format(n[R.F_SERV], ","))
    w("  The servicing platform from the September 2024 cycle: the same population, reporting periods September 2024")
    w("  to November 2026, one row per loan per reporting period. investor_type PORTFOLIO is held for investment.")
    w("  interest_rate is a decimal (0.06875 is 6.875 per cent). unscheduled_principal is all principal paid beyond")
    w("  the scheduled payment, a payoff included. zero_balance_code: 01 paid in full, 15 sold.")
    w("")
    w("servicing_conversion_xref.csv (%s rows)" % format(n[R.F_XREF], ","))
    w("  Every loan converted from the legacy platform: legacy loan number, loan id, principal converted.")
    w("")
    w("rate_sheet_archive.csv (%s rows)" % format(n[R.F_RATES], ","))
    w("  The bank's posted rate sheets as issued: commercial real estate from 2015, conforming from 2019, portfolio")
    w("  jumbo from 2022. Sheets go out on Mondays, with a mid-week re-price when markets move. Rates and points are")
    w("  per cent. The product codes changed with the pricing engine on 1 January 2024: JMB30 is now J30F, JMB15")
    w("  J15F, CNF30 C30F, CNF15 C15F and CRE5 CRE5F.")
    w("")
    w("cre_term_loans_20261130.csv (%s rows)" % format(n[R.F_CRE], ","))
    w("  Every commercial real estate term loan at the close on 30 November 2026, fixed and floating; loans in special")
    w("  assets are not in it. The loan number is 44, the obligor number and the note number. maturity_date is the")
    w("  current maturity and original_maturity_date the maturity at origination; on an extended loan note_rate,")
    w("  monthly_payment and amortization_months are the extension's. interest_basis ACT/360 charges the month's actual")
    w("  days over 360 and 30/360 thirty days over 360; the monthly payment is fixed and principal is what it leaves")
    w("  after interest. interest_only_months is the interest-only period from origination, after which the payment")
    w("  amortizes the loan over amortization_months. On floating loans note_rate is the rate in force (one-month Term")
    w("  SOFR plus rate_spread). risk_grade is the bank's scale of 1 to 9: 6 watch, 7 special mention, 8 substandard.")
    w("")
    w("cre_maturity_log.xlsx (%s rows)" % format(n[F_LOG], ","))
    w("  Credit administration's log of term loans reaching a maturity date, one sheet a year from 2015, one row per")
    w("  loan and maturity date. The sheet layout changed in 2020. Obligation is the obligor and note number;")
    w("  Property is the property number without its P. Disposition (to 2019) and Outcome: PO, paid at maturity;")
    w("  EXT, extended; EXT-S, extended six months on the note's terms for a sale under contract; PO-EXT, paid at")
    w("  the extended maturity; SA, transferred to special assets at the extended maturity. The bank grants a")
    w("  maturing term loan one extension, of 36 months, on a paydown of 10 per cent of the principal due, at the")
    w("  bank's posted five-year fixed rate on the maturity date, the payment amortizing the rest over 25 years. An")
    w("  extended loan is not extended again: at its extended maturity it is paid or goes to special assets. Every")
    w("  extension is granted on the guarantor's reaffirmed support agreement, with an interest reserve funded at the")
    w("  extension; the extended loan's payments are made as scheduled.")
    w("")
    w("cre_operating_statements.csv (%s rows)" % format(n[R.F_STMT], ","))
    w("  Borrowers' annual operating statements as reviewed, one row per property and fiscal year from 2013, with the")
    w("  underwriting row (statement_basis Underwriting: the net operating income the loan was sized on, its year")
    w("  ending the month before the loan closed). Fiscal years end in the borrower's own month. review_completed is")
    w("  the date the review was signed off.")
    w("")
    w("custody_holdings_20261130.csv (%s rows)" % format(n[R.F_CUSTODY], ","))
    w("  The custodian's statement of the available-for-sale account at the close on 30 November 2026. Faces, cost,")
    w("  value and accrued interest are thousands of dollars; factor is the pool factor for November 2026.")
    w("")
    w("agency_pool_factors.csv (%s rows)" % format(n[R.F_FACTORS], ","))
    w("  Monthly factors of the agency pools held, with each pool's weighted average coupon (wac, per cent),")
    w("  remaining term and age (wam, wala, months). A factor is the principal left per dollar of original face")
    w("  after the month's payments; holders receive the month's principal and interest on the 25th of the next month.")
    w("")
    w("indirect_auto_tape_20261130.csv (%s rows)" % format(n[R.F_AUTO], ","))
    w("  Every indirect auto loan at the close on 30 November 2026.")
    w("")
    w("indirect_auto_monthly_roll.csv (%s rows)" % format(n[R.F_ROLL], ","))
    w("  The indirect auto portfolio's roll by month from January 2023: principal at the start of the month, loans")
    w("  bought, scheduled principal, principal prepaid, charge-offs, principal at the month end.")
    w("")
    w("planning_cycle_2027_base_case.xlsx")
    w("  ALCO's September 2026 planning cycle for the 2027 plan, base case.")
    w("")
    w("swap_register_20261130.xlsx (%s rows)" % format(n[F_REGISTER], ","))
    w("  The treasury system's register of the bank's interest-rate swaps at the close on 30 November 2026, both")
    w("  books, one row per trade. Notional is the trade's notional on 30 November (an amortizing swap's current")
    w("  period). Hedged item is what the swap is designated against. Clearing ref is the clearing house's trade id.")
    w("  Terminated on is the date an early termination took effect, on a trade with Status TERMINATED.")
    w("")
    w("swap_amortisation_schedules.csv (%s rows)" % format(n[R.F_SCHED], ","))
    w("  Notional by calculation period of the amortizing swaps.")
    w("")
    w("clearing_statement_20261130.csv (%s rows)" % format(n[R.F_CLEAR], ","))
    w("  The clearing broker's statement of the bank's cleared swaps at the close on 30 November 2026.")
    w("  client_trade_ref is the bank's reference the broker holds for the trade: the treasury system trade number the")
    w("  bank gave the broker when it submitted the trade for clearing. cleared_on is the date the clearing house")
    w("  accepted it; termination_date is the swap's scheduled end; client_pays is the bank's side.")
    w("")
    w("mortgage_lock_pipeline_20261130.csv (%s rows)" % format(n[R.F_LOCKS], ","))
    w("  Rate locks outstanding at the close on 30 November 2026.")
    w("")
    w("deposit_decay_study_2026.xlsx")
    w("  ALM's 2026 study of non-maturity deposits (balances at 30 June 2026).")
    w("")
    w("balance_sheet_hedging_policy.pdf, alm_report_2026_q3.pdf")
    return "\r\n".join(L) + "\r\n"


def write_notes(path, n):
    open(path, "w", encoding="utf-8", newline="").write(notes_text(n))


def write_all(out, W, S, n):
    p = lambda f: os.path.join(out, f)
    n[F_LOG] = write_log(p(F_LOG), W)
    write_plan(p(F_PLAN))
    n[F_REGISTER] = write_register(p(F_REGISTER), S)
    write_nmd(p(F_NMD))
    write_policy(p(F_POLICY))
    write_alm(p(F_ALM), W)
    write_notes(p(F_NOTES), n)
    return n
