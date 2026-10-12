"""The documents: the investment policy, finance procedure 7, the budget workbook, Kestwick's key facts, price history
and factsheets, Fernside's quarterly report and Brackenfold's export notes."""
import datetime as dt
import os
import shutil
import tempfile

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import officex as OX
import world as W

P = lambda t: ("p", t)


# ------------------------------------------------------------------------------------------------ the policy

POLICY = [
    ("h1", "1. Purpose and scope"),
    P("1.1 The trust invests its permanent and expendable endowments as one portfolio under this policy."),
    P("1.2 The investment objective is to preserve the real value of the permanent endowment over the long term while "
      "producing a reliable income for the trust's grant-making, and to keep the expendable endowment available to "
      "meet grant commitments when income falls short."),
    P("1.3 The trustees have delegated the oversight of this policy to the investment committee. The finance director "
      "reports on the portfolio to each meeting of the committee and of the trustees."),
    ("h1", "2. Asset allocation"),
    P("2.1 Growth assets are the segregated UK equity portfolio managed by Fernside Partners (the mandate) and the "
      "Kestwick North American, European and Japan Equity Funds for Charities; defensive assets are the Kestwick Gilt "
      "Fund for Charities and the Kestwick Sterling Corporate Bond Fund for Charities."),
    P("2.2 Within growth assets the weights are 40 per cent the mandate, 30 per cent North American, 15 per cent European "
      "and 15 per cent Japan; within defensive assets, 55 per cent gilts and 45 per cent corporate bonds."),
    P("2.3 The mandate includes the cash its manager holds in it."),
    P("2.4 All holdings are held through Brackenfold Custody in the names of the two endowment designations."),
    ("h1", "3. The growth share and the volatility cap"),
    P("3.1 The trustees set the growth share in ten-point steps from 20 to 100 per cent."),
    P("3.2 At their December meeting the trustees set the growth share for the following calendar year."),
    P("3.3 The portfolio is rebalanced to the policy weights at each quarter end."),
    P("3.4 The portfolio's expected volatility at the growth share set must be not more than 10 per cent."),
    ("h1", "4. Expected volatility"),
    P("4.1 Expected volatility is the standard deviation of the portfolio's total return over twelve months."),
    P("4.2 It is estimated from the time-weighted total returns of the policy's holdings, each measured from the "
      "holding's own prices and the income it pays, over the two years to the last month-end valuation before the "
      "review, combined in every period at the policy weights for the growth share under review."),
    P("4.3 The two years are divided into return periods of equal length, at least 100 of them, and every period is "
      "weighted equally."),
    P("4.4 The estimate is compared with the cap before any rounding."),
    ("h1", "5. Costs"),
    P("5.1 Investment management and custody fees are charged to the capital of the endowments."),
    ("h1", "6. Use of capital"),
    P("6.1 The trustees may release capital from the expendable endowment to meet grant payments and running costs "
      "that income does not cover."),
    P("6.2 Capital is not released from the permanent endowment."),
    ("h1", "7. Responsible investment"),
    P("7.1 The trust does not hold directly any company deriving more than 10 per cent of its revenue from tobacco, "
      "thermal coal or controversial weapons. The Kestwick funds apply Kestwick's own charity exclusions, which the "
      "committee reviews each year."),
    ("h1", "8. Review"),
    P("8.1 This policy is reviewed by the investment committee each year and approved by the trustees."),
    ("h1", "Annex"),
    P("The growth share for 2026 is 80 per cent."),
]


def policy_pdf(path):
    blocks = [("title", "The Wrexford Trust: Investment Policy"),
              ("small", "Approved by the trustees on 9 December 2025 on the recommendation of the investment committee"),
              ("table", [["Owner", "Investment committee (chair: Lawrence Barnes)"],
                         ["Approved", "9 December 2025"], ["Next review", "December 2026"],
                         ["Registered charity", "1048735"]], [2600, 6400], 19)] + POLICY
    blocks.append(("small", "Signed for the trustees: Lawrence Barnes, chair of the investment committee"))
    props = dict(title="The Wrexford Trust: Investment Policy", creator="Lawrence Barnes", modified_by="Harriet Clarke",
                 created=dt.datetime(2019, 11, 14, 10, 2), modified=dt.datetime(2025, 12, 10, 9, 41), revision=23,
                 total_time=412, company="The Wrexford Trust")
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "policy.docx")
    OX.docx(src, blocks, ("The Wrexford Trust", "Investment Policy"),
            ("Approved 9 December 2025", "Page {PAGE} of {NUMPAGES}"), props, font="Arial", seed=2512, sessions=7,
            margins=(1418, 1418, 1247, 1247))
    OX.pdf_from_docx(src, path)
    shutil.rmtree(tmp)


# ------------------------------------------------------------------------------------------------ procedure 7

PROCEDURE = [
    ("h1", "7. The annual budget"),
    P("7.1 The budget year is the calendar year."),
    P("7.2 Investment income for the budget year is estimated from the last month-end valuation before the trustees' "
      "December meeting. For the Fernside mandate, it is the mandate's dividends and distributions with an ex-dividend "
      "date in the twelve months to the valuation date, as a share of the mandate's market value at that date. For each "
      "Kestwick fund, it is the distributions per unit with an ex-dividend date in those twelve months, as a share of "
      "the fund's price at that date. Each share is applied to the value that the policy weights for the growth share "
      "under review place in the holding, the portfolio taken at its market value at the valuation date."),
    P("7.3 Market value excludes income accrued but not yet received."),
    P("7.4 Grant payments for the budget year are the instalments of grants awarded by the date of the budget that the "
      "trust expects to pay in the year; grants awarded during the year are budgeted under the new awards line."),
    P("7.5 Grant payments in euro are budgeted at 1.1460 euro to the pound."),
    P("7.6 Running costs are the budget workbook's running costs total; investment management and custody fees are "
      "charged to capital (investment policy 5.1) and are not running costs."),
    P("7.7 The new awards line is set by the trustees at the December meeting from the grants committee's proposals."),
    P("7.8 The draft budget goes to the finance and audit committee in November and to the trustees in December, with "
      "the investment income, grant payments and new awards lines completed after the trustees have set the growth "
      "share."),
    ("h1", "8. Month-end close"),
    P("8.1 The finance team reconciles the custodian's month-end valuation to the general ledger within ten working "
      "days of the month end, and the grant payment ledger to the grants system each month."),
    P("8.2 Differences over 500 pounds are explained to the finance director in writing."),
]


def procedure_docx(path):
    blocks = [("title", "Finance procedures, section 7: the annual budget"),
              ("small", "The Wrexford Trust  |  Revised October 2026  |  Owner: Harriet Clarke, finance director")] + PROCEDURE
    props = dict(title="Finance procedures 7: the annual budget", creator="Harriet Clarke", modified_by="Harriet Clarke",
                 created=dt.datetime(2021, 9, 6, 14, 12), modified=dt.datetime(2026, 10, 19, 16, 37), revision=17,
                 total_time=288, company="The Wrexford Trust")
    OX.docx(path, blocks, ("The Wrexford Trust", "Finance procedures"),
            ("Section 7, revised October 2026", "Page {PAGE} of {NUMPAGES}"), props, seed=2610, sessions=6)


# ------------------------------------------------------------------------------------------------ budget workbook

def budget_xlsx(path, running, capital):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    bold = Font(bold=True)
    ws.append(["The Wrexford Trust: budget 2027 (draft for the finance and audit committee, 24 November 2026)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["", "2027 draft (GBP)", "Note"])
    for c in ("A3", "B3", "C3"):
        ws[c].font = bold
    ws.append(["Investment income", None, "To complete after the trustees set the 2027 growth share (procedure 7.2)"])
    ws.append(["Grant payments", None, "To complete (procedure 7.4)"])
    ws.append(["New awards", None, "Set by the trustees in December (procedure 7.7)"])
    ws.append(["Running costs", "='Running costs'!B17", "Running costs sheet"])
    ws.append(["Capital release from the expendable endowment", None, "To complete"])
    for r in range(4, 9):
        ws.cell(row=r, column=2).number_format = "#,##0"
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 70
    rc = wb.create_sheet("Running costs")
    rc.append(["Running costs 2027", "GBP"])
    rc["A1"].font = bold
    rc["B1"].font = bold
    for nm, v in running:
        rc.append([nm, v])
    rc.append([])
    n = len(running)
    assert n + 3 == 16, n
    rc.append(["Total running costs", "=SUM(B2:B%d)" % (n + 1)])
    rc["A17"].font = bold
    rc["B17"].font = bold
    rc.append([])
    rc.append(["Charged to capital (investment policy 5.1)", "GBP"])
    rc["A19"].font = bold
    for nm, v in capital:
        rc.append([nm, v])
    rc.append(["Total charged to capital", "=SUM(B20:B%d)" % (19 + len(capital))])
    rc.cell(row=20 + len(capital), column=1).font = bold
    for r in range(2, 25):
        rc.cell(row=r, column=2).number_format = "#,##0"
    rc.column_dimensions["A"].width = 48
    rc.column_dimensions["B"].width = 14
    total = sum(v for _, v in running)
    OX.xlsx_from_openpyxl(wb, path, "Harriet Clarke", "Harriet Clarke", dt.datetime(2026, 10, 27, 10, 4),
                          dt.datetime(2026, 11, 24, 17, 12), company="The Wrexford Trust", seed=2711)
    return total


# ------------------------------------------------------------------------------------------------ Kestwick history

def kestwick_xlsx(path, hist):
    wb = openpyxl.Workbook()
    first = True
    for f in W.FUNDS:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = W.FUNDS[f]["short"][:31]
        ws.append([W.FUNDS[f]["name"]])
        ws["A1"].font = Font(bold=True)
        ws.append(["Income units ISIN %s   Accumulation units ISIN %s" % (W.FUNDS[f]["isin_inc"], W.FUNDS[f]["isin_acc"])])
        ws.append(["Prices at the valuation point, GBP. Source: Kestwick Investment Management, price history export 2 December 2026"])
        ws.append([])
        df = hist[f]
        ws.append(list(df.columns))
        for c in ws[5]:
            c.font = Font(bold=True)
        for row in df.itertuples(index=False):
            d, pi, pa, xd, dist = row
            ws.append([d, float(pi), float(pa), xd or None, None if dist is None or dist != dist else float(dist)])
        for r in range(6, ws.max_row + 1):
            ws.cell(row=r, column=1).number_format = "dd/mm/yyyy"
            ws.cell(row=r, column=2).number_format = "0.0000"
            ws.cell(row=r, column=3).number_format = "0.0000"
            ws.cell(row=r, column=5).number_format = "0.0000"
        for col, w in zip("ABCDE", [12, 20, 26, 12, 34]):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = "A6"
    OX.xlsx_from_openpyxl(wb, path, "KIM Web Services", "KIM Web Services", dt.datetime(2026, 12, 2, 8, 15),
                          dt.datetime(2026, 12, 2, 8, 15), company="Kestwick Investment Management", seed=3301)


# ------------------------------------------------------------------------------------------------ PDFs (reportlab)

def _rl():
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                    TableStyle)
    return locals()


def key_facts_pdf(path):
    R = _rl()
    ss = R["getSampleStyleSheet"]()
    body = R["ParagraphStyle"]("b", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, leading=11)
    head = R["ParagraphStyle"]("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
                               textColor=R["colors"].HexColor("#0B4F6C"), spaceBefore=6, spaceAfter=4)
    sub = R["ParagraphStyle"]("s", parent=body, fontName="Helvetica-Bold", fontSize=8.8, spaceBefore=4)
    objective = {
        "NAEF": "To provide long-term capital growth with some income from a portfolio of shares in companies listed in "
                "the United States and Canada.",
        "EUEF": "To provide long-term capital growth and income from a portfolio of shares in companies listed in "
                "continental Europe.",
        "JPEF": "To provide long-term capital growth from a portfolio of shares in companies listed in Japan.",
        "GILT": "To provide income with the preservation of capital from a portfolio of UK government bonds.",
        "CORP": "To provide income from a portfolio of sterling investment-grade corporate bonds.",
    }
    ocf = {"NAEF": "0.42%", "EUEF": "0.48%", "JPEF": "0.51%", "GILT": "0.22%", "CORP": "0.29%"}
    dist = {"NAEF": "half-yearly; ex-dividend on the first Monday of March and September",
            "EUEF": "half-yearly; ex-dividend on the first Monday of April and October",
            "JPEF": "half-yearly; ex-dividend on the first Monday of May and November",
            "GILT": "quarterly; ex-dividend on the first Monday of February, May, August and November",
            "CORP": "quarterly; ex-dividend on the first Monday of February, May, August and November"}
    story = [R["Paragraph"]("Kestwick Charity Funds: key facts", head),
             R["Paragraph"]("Kestwick Investment Management Limited is authorised and regulated by the Financial Conduct "
                            "Authority. The funds are common investment funds for charities established under the "
                            "Charities Act 2011. This document summarises each fund; the scheme particulars are "
                            "available on request.", body), R["Spacer"](1, 6)]
    for f, v in W.FUNDS.items():
        rows = [["Fund", v["name"]], ["Objective", R["Paragraph"](objective[f], body)],
                ["Units", "Income units %s; accumulation units %s" % (v["isin_inc"], v["isin_acc"])],
                ["Ongoing charges", ocf[f] + " a year, taken from capital"],
                ["Distributions", dist[f]],
                ["Dealing", R["Paragraph"]("Dealing: daily at 12 noon UK time, the fund's valuation point. Investments are "
                                           "valued at their latest available prices at the valuation point.", body)],
                ["Eligibility", "Charities in England and Wales, Scotland and Northern Ireland"]]
        t = R["Table"](rows, colWidths=[32 * R["mm"], 140 * R["mm"]])
        t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.4),
                                    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.25, R["colors"].HexColor("#B8C7CE")),
                                    ("BACKGROUND", (0, 0), (-1, 0), R["colors"].HexColor("#E3EEF2"))]))
        story += [R["KeepTogether"]([R["Paragraph"](v["name"], sub), t]), R["Spacer"](1, 8)]
    story.append(R["Paragraph"]("Past performance is not a guide to future returns. The value of units and the income "
                                "from them can fall as well as rise. Issued September 2026.", body))
    doc = R["SimpleDocTemplate"](path, pagesize=R["A4"], leftMargin=18 * R["mm"], rightMargin=18 * R["mm"],
                                 topMargin=16 * R["mm"], bottomMargin=16 * R["mm"], title="Kestwick Charity Funds key facts",
                                 author="Kestwick Investment Management", subject="", creator="", producer="")
    doc.build(story)


def factsheets_pdf(path, figs):
    """figs[f]: size_m, perf (three discrete years), cum3, vol3, sectors [(name, pct)], launch"""
    R = _rl()
    ss = R["getSampleStyleSheet"]()
    body = R["ParagraphStyle"]("b", parent=ss["Normal"], fontName="Helvetica", fontSize=8.4, leading=10.5)
    head = R["ParagraphStyle"]("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14,
                               textColor=R["colors"].HexColor("#0B4F6C"), spaceAfter=2)
    sub = R["ParagraphStyle"]("s", parent=body, fontName="Helvetica-Bold", fontSize=9, spaceBefore=6, spaceAfter=2)
    story = []
    for n, (f, v) in enumerate(W.FUNDS.items()):
        g = figs[f]
        story.append(R["Paragraph"](v["name"], head))
        story.append(R["Paragraph"]("Factsheet, 30 September 2026  |  Income units %s" % v["isin_inc"], body))
        story.append(R["Spacer"](1, 6))
        facts = [["Fund size", "GBP %.1fm" % g["size_m"]], ["Launch date", g["launch"]], ["Benchmark", g["bench"]],
                 ["Number of holdings", str(g["n"])]]
        t = R["Table"](facts, colWidths=[40 * R["mm"], 60 * R["mm"]])
        t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.4),
                                    ("LINEBELOW", (0, 0), (-1, -1), 0.25, R["colors"].HexColor("#B8C7CE"))]))
        story += [t, R["Paragraph"]("Discrete performance to 30 September (total return, income units, %)", sub)]
        perf = [["", "2024", "2025", "2026", "3 years cumulative"],
                ["Fund"] + ["%.1f" % x for x in g["perf"]] + ["%.1f" % g["cum3"]]]
        t = R["Table"](perf, colWidths=[30 * R["mm"]] + [22 * R["mm"]] * 3 + [34 * R["mm"]])
        t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                                    ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("BACKGROUND", (0, 0), (-1, 0), R["colors"].HexColor("#E3EEF2"))]))
        story += [t, R["Paragraph"]("Risk", sub),
                  R["Paragraph"]("Volatility, three years to 30 September 2026, from monthly returns: %.1f%%" % g["vol3"], body),
                  R["Paragraph"](g["label"], sub)]
        t = R["Table"]([[a, "%.1f" % b] for a, b in g["sectors"]], colWidths=[60 * R["mm"], 20 * R["mm"]])
        t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                    ("LINEBELOW", (0, 0), (-1, -1), 0.25, R["colors"].HexColor("#DDE6EA"))]))
        story += [t, R["Spacer"](1, 8),
                  R["Paragraph"]("Past performance is not a guide to future returns. Source: Kestwick Investment Management.", body)]
        if n < len(W.FUNDS) - 1:
            story.append(R["PageBreak"]())
    doc = R["SimpleDocTemplate"](path, pagesize=R["A4"], leftMargin=18 * R["mm"], rightMargin=18 * R["mm"],
                                 topMargin=16 * R["mm"], bottomMargin=16 * R["mm"], title="Kestwick Charity Funds factsheets",
                                 author="Kestwick Investment Management", subject="", creator="", producer="")
    doc.build(story)


def fernside_pdf(path, rep):
    """rep: q, ytd, y1 (mandate and index), vol12 (mandate, index), top [(name, pct)], trades text"""
    R = _rl()
    ss = R["getSampleStyleSheet"]()
    body = R["ParagraphStyle"]("b", parent=ss["Normal"], fontName="Times-Roman", fontSize=10, leading=13, spaceAfter=5)
    head = R["ParagraphStyle"]("h", parent=ss["Heading1"], fontName="Times-Bold", fontSize=15, spaceAfter=4)
    sub = R["ParagraphStyle"]("s", parent=body, fontName="Times-Bold", fontSize=11, spaceBefore=6)
    story = [R["Paragraph"]("Fernside Partners", head),
             R["Paragraph"]("The Wrexford Trust: segregated UK equity portfolio. Quarterly report to 30 September 2026", sub),
             R["Paragraph"]("Dear Trustees,", body)]
    for para in rep["letter"]:
        story.append(R["Paragraph"](para, body))
    story.append(R["Paragraph"]("Performance (time-weighted total return after fees, %)", sub))
    t = R["Table"]([["", "Quarter", "Year to date", "One year"],
                    ["Portfolio"] + ["%.1f" % x for x in rep["port"]],
                    ["FTSE All-Share"] + ["%.1f" % x for x in rep["index"]]],
                   colWidths=[40 * R["mm"], 28 * R["mm"], 28 * R["mm"], 28 * R["mm"]])
    t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Times-Roman", 9.5), ("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5),
                                ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.5, R["colors"].black)]))
    story += [t, R["Paragraph"]("Risk, twelve months to 30 September 2026", sub)]
    t = R["Table"]([["", "Volatility (%)", "Beta", "Tracking error (%)"],
                    ["Portfolio", "%.1f" % rep["vol"][0], "%.2f" % rep["beta"], "%.1f" % rep["te"]],
                    ["FTSE All-Share", "%.1f" % rep["vol"][1], "1.00", ""]],
                   colWidths=[40 * R["mm"], 28 * R["mm"], 28 * R["mm"], 34 * R["mm"]])
    t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Times-Roman", 9.5), ("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5),
                                ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.5, R["colors"].black)]))
    story += [t, R["Paragraph"]("Risk statistics are calculated from the portfolio's daily returns over the twelve months "
                                "to the quarter end.", body),
              R["Paragraph"]("Ten largest holdings at 30 September 2026 (% of portfolio)", sub)]
    t = R["Table"]([[a, "%.1f" % b] for a, b in rep["top"]], colWidths=[80 * R["mm"], 20 * R["mm"]])
    t.setStyle(R["TableStyle"]([("FONT", (0, 0), (-1, -1), "Times-Roman", 9.5), ("ALIGN", (1, 0), (1, -1), "RIGHT")]))
    story += [t, R["Spacer"](1, 8), R["Paragraph"]("Yours faithfully,", body),
              R["Paragraph"]("Connor Wells<br/>Portfolio Manager, Fernside Partners LLP", body),
              R["Paragraph"]("Fernside Partners LLP is authorised and regulated by the Financial Conduct Authority. This "
                             "report is for the trustees of The Wrexford Trust.", body)]
    doc = R["SimpleDocTemplate"](path, pagesize=R["A4"], leftMargin=22 * R["mm"], rightMargin=22 * R["mm"],
                                 topMargin=20 * R["mm"], bottomMargin=18 * R["mm"],
                                 title="The Wrexford Trust quarterly report Q3 2026", author="Connor Wells",
                                 subject="", creator="", producer="")
    doc.build(story)


# ------------------------------------------------------------------------------------------------ export notes

def export_notes(path, ri_code_new):
    text = """BRACKENFOLD CUSTODY - CLIENT DATA EXPORT
Client: The Wrexford Trust (client number 40719)
Run: 2 December 2026 06:41 (export job CLX-2207)
Prepared for: Harriet Clarke, finance director

Designations
  WRX-PE01  Permanent endowment
  WRX-EX02  Expendable endowment
Both designations hold shares and cash in the segregated UK equity portfolio managed by Fernside Partners and units
in the Kestwick Charity Funds. WRX-PE01 holds income units and WRX-EX02 accumulation units.

Files in this export
  brackenfold_valuation_lots_2024-11_2026-11.csv
  brackenfold_capital_movements_2024-12_2026-11.csv
  brackenfold_corporate_events_2024-12_2026-11.csv
  brackenfold_income_entitlements_by_lot_2025-11_2026-11.csv
  brackenfold_static_data_2026-12-02.csv

Dates are written YYYY-MM-DD. Amounts are in pounds sterling.

Valuation (brackenfold_valuation_lots_*)
  One line per tax lot per valuation date for shares; one line per designation for cash and for collective
  investment schemes, which are not lot-tracked.
  valuation_date       business day of the valuation
  sub_account          designation
  security_code        Brackenfold security code (see static data)
  lot_id, lot_open_date  tax lot and the date it was opened; for shares received in a corporate action, the
                       open date of the lot they came from
  quantity             shares, units, or for cash the balance
  price                price used for the valuation, GBP
  market_value_gbp     quantity x price
  accrued_income_gbp   income due on the lot that has gone ex-dividend and has not yet been paid
  asset_class          from the static data
Pricing: Listed securities are valued at the official closing price of their primary exchange. Units in collective
investment schemes are valued at the latest dealing price published by the manager.

Capital movements (brackenfold_capital_movements_*)
  Every cash movement on the Fernside designations' cash accounts.
  movement_type
    Contribution            cash paid in to the portfolio by the client
    Withdrawal              cash paid out of the portfolio to the client
    Dividend received       income paid on a holding
    Purchase / Sale         trades by the manager (trade date)
    Rights subscription     payment for rights taken up
    Takeover consideration  cash received for shares under a takeover or scheme
    Cash in lieu            cash for fractions of shares
    Management fee          the manager's fee, debited from the portfolio's cash

Corporate events (brackenfold_corporate_events_*)
  action_type: SPLR consolidation, SOFF demerger, RHTS rights issue, MRGR takeover or scheme of arrangement.
  ex_date is the first day the shares trade without the entitlement; effective_date is the day the new holding,
  or the cash, is booked to the account.

Income entitlements (brackenfold_income_entitlements_by_lot_*)
  Income events with an ex-dividend date from 1 November 2025 to 30 November 2026.
  One line per tax lot. entitlement_gbp: the income entitlement in pounds.
  event_type: Dividend, Property income distribution, Distribution (income units), Accumulation (accumulation
  units, income retained in the unit price).

Static data (brackenfold_static_data_*)
  security_code, ISIN, SEDOL, name, asset class, listing, price currency.

Queries: client.data@brackenfold-custody.co.uk
"""
    with open(path, "w") as f:
        f.write(text)
