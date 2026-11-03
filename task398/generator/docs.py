"""The pack's documents: the prospectus extract, the board's review terms, the sub-advisers' reports and two
documents the work does not need."""
import os

import numpy as np

import postprocess as PP
import world as W
from world import D, DAYS, IDX

MONTHS = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3), (2026, 4), (2026, 5), (2026, 6),
          (2026, 7), (2026, 8), (2026, 9)]
MNAME = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _pdf(path, title, author, blocks, created, modified):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    st = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.2, leading=13.5, spaceBefore=6, spaceAfter=4)
    sm = ParagraphStyle("s", fontName="Helvetica", fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator="")
    flow = []
    for kind, val in blocks:
        if kind == "h1":
            flow.append(Paragraph(val, h1))
        elif kind == "h2":
            flow.append(Paragraph(val, h2))
        elif kind == "p":
            flow.append(Paragraph(val, st))
        elif kind == "small":
            flow.append(Paragraph(val, sm))
        elif kind == "sp":
            flow.append(Spacer(1, val))
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.2),
                                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9a9a9a")),
                                   ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            flow.append(t)

    def _meta(c, d):
        c.setProducer("Microsoft\xae Word for Microsoft 365")
        c.setCreator("Microsoft\xae Word for Microsoft 365")
    doc.build(flow, onFirstPage=_meta, onLaterPages=_meta)
    PP.normalize_pdf(path, created, modified)


# ------------------------------------------------------------------------------------------------ prospectus
def prospectus(out):
    blocks = [
        ("small", "Thornbury Fund Managers Limited  |  Authorised and regulated by the Financial Conduct Authority  |  "
                  "Prospectus dated 1 April 2026 (extract)"),
        ("h1", "Thornbury Managed Risk UK Equity Fund"),
        ("p", "A sub-fund of Thornbury Investment Funds ICVC, an investment company with variable capital and a UK UCITS "
              "scheme. Authorised fund manager: Thornbury Fund Managers Limited. Depositary: Holloway Trustee Services "
              "Limited to 31 March 2026; Northcote Depositary Limited from 1 April 2026, which also holds the fund's "
              "assets in safekeeping from that date."),
        ("h2", "1. Investment objective and policy"),
        ("p", "1.1 The fund aims to provide capital growth and income over any five year period by investing in the "
              "shares of companies listed or traded in the United Kingdom, while limiting the fall in the value of its "
              "shares through the overlay described in section 4."),
        ("p", "1.2 The fund's performance is compared with the Larkspur UK All-Share Index (total return), measured at "
              "the fund's valuation point."),
        ("h2", "2. Valuation and pricing"),
        ("p", "2.1 The fund is valued at 12:00 UK time on each dealing day. Shares are single priced and dealt at the "
              "price calculated at the next valuation point after an instruction is received."),
        ("p", "2.2 Investments are valued at mid-market prices at the valuation point. A security whose trading is "
              "suspended is valued at the authorised fund manager's fair value."),
        ("h2", "3. Sleeves and sub-advisers"),
        ("p", "3.1 The fund's equity investments are held in two sleeves: a value sleeve managed by Ashcombe Investment "
              "Partners LLP and a growth sleeve managed by Fennick Capital Limited. A liquidity sleeve is invested in "
              "the Thornbury Sterling Liquidity Fund."),
        ("p", "3.2 The authorised fund manager allocates 47 per cent of the fund's net asset value to the value sleeve, "
              "47 per cent to the growth sleeve and 6 per cent to the liquidity sleeve, and restores those proportions "
              "at the last valuation point of each calendar quarter, after that valuation, by moving cash between the "
              "sleeves."),
        ("p", "3.3 Subscriptions and redemptions, the fund's charges, distributions to income shareholders and the "
              "margin on the overlay's futures are settled through the liquidity sleeve."),
        ("h2", "4. The drawdown overlay"),
        ("p", "4.1 Merrow Overlay Services LLP manages the overlay. It uses Larkspur 100 index futures only, in whole "
              "contracts, with a contract value of GBP 10 per index point, traded at the fund's valuation point."),
        ("p", "4.2 Equity exposure means the value of the value sleeve and the growth sleeve plus the notional value of "
              "the fund's index futures (contracts held, multiplied by the futures price and by GBP 10), as a proportion "
              "of the fund's net asset value."),
        ("p", "4.3 At each valuation point the overlay manager compares the price of a B Accumulation share with the "
              "highest price of a B Accumulation share at any of the 63 valuation points ending with that one. Where the "
              "price is more than 8 per cent below that highest price and equity exposure is not already reduced, the "
              "overlay manager sells futures at the valuation point of the next dealing day so that equity exposure is as "
              "near as possible to 40 per cent of net asset value, and resets the position at each later valuation point "
              "while the reduction lasts."),
        ("p", "4.4 Where, during a reduction, the price of a B Accumulation share at a valuation point is within 4 per "
              "cent of the highest price measured as in 4.3, the overlay manager closes the futures position at the "
              "valuation point of the next dealing day."),
        ("p", "4.5 The overlay manager holds the contract with the nearest expiry until five dealing days before its last "
              "trading day, when it moves the position to the next contract."),
        ("h2", "5. Share classes, charges and distributions"),
        ("table", [["Class", "Annual management charge", "Distribution"],
                   ["B Accumulation", "0.85%", "Accumulated"], ["B Income", "0.85%", "Paid"],
                   ["C Accumulation", "0.60%", "Accumulated"], ["C Income", "0.60%", "Paid"]]),
        ("sp", 6),
        ("p", "5.1 The annual management charge accrues at each valuation point on each class's net asset value at the "
              "previous valuation point, for the calendar days between them, and is taken from the price of that class. "
              "The authorised fund manager pays the sub-advisers, the overlay manager, the depositary and the custodian "
              "from its charge. Dealing commission, stamp duty reserve tax and futures commission are paid by the fund."),
        ("p", "5.2 The fund's accounting year ends on 30 September and its interim period on 31 March. Income shares go "
              "ex-distribution on 1 April and 1 October and distributions are paid by the last business day of May and "
              "November."),
    ]
    _pdf(os.path.join(out, "thornbury_mruke_prospectus_extract_2026.pdf"), "Thornbury Managed Risk UK Equity Fund",
         "Thornbury Fund Managers Limited", blocks, b"D:20260318094100+00'00'", b"D:20260401080500+01'00'")


# ------------------------------------------------------------------------------------------------ review terms
TERMS = [
    ("h", "1. What the board decides"),
    ("p", "1.1 In its assessment of value for the accounting year to 30 September 2026 the board will make one change to "
          "the fund for 2026-27, chosen from the list at section 3. Each change on the list is priced on the accounting "
          "year just ended, the only year for which the fund's records exist under its present structure."),
    ("h", "2. How a change is priced"),
    ("p", "2.1 A change is priced as the part of the accounting year's shortfall against the benchmark that it would "
          "have removed: the return of the fund's B Accumulation shares over the accounting year had the change been in "
          "force from the 12:00 valuation point on 30 September 2025, less the return of those shares over the "
          "accounting year as it ran, in basis points."),
    ("p", "2.2 The accounting year runs from the 12:00 valuation point on 30 September 2025 to the 12:00 valuation "
          "point on 30 September 2026. The benchmark is the Larkspur UK All-Share Index (total return) taken at the "
          "fund's valuation point."),
    ("p", "2.3 The market and dealing in the fund's shares are taken as they were, a sleeve the change leaves with its "
          "sub-adviser keeps that sub-adviser's holdings, and the fund is otherwise run as its prospectus requires. A "
          "change is taken to be in force from the start of the year without transition costs."),
    ("h", "3. The changes before the board"),
    ("p", "Value sleeve to a tracker. Ashcombe's mandate ends and the value sleeve is run as a tracker of the benchmark, "
          "taken to earn the benchmark's total return between valuation points."),
    ("p", "Growth sleeve to a tracker. Fennick's mandate ends and the growth sleeve is run as a tracker of the "
          "benchmark, taken to earn the benchmark's total return between valuation points."),
    ("p", "Higher trigger. The overlay reduces equity exposure only when the B Accumulation price is more than 12 per "
          "cent below its highest price, in place of 8 per cent."),
    ("p", "Earlier restoration. The overlay closes a reduction when the B Accumulation price is within 6 per cent of its "
          "highest price, in place of 4 per cent."),
    ("p", "Equitised liquidity sleeve. While equity exposure is not reduced, the overlay manager holds Larkspur 100 "
          "index futures in whole contracts with a notional value as near as possible to the liquidity sleeve's value, "
          "set at each valuation point; at the last valuation point of a calendar quarter the liquidity sleeve's value "
          "is taken after the cash moved between the sleeves at that valuation point."),
    ("h", "4. Timetable"),
    ("p", "4.1 Investment oversight prepares the pricing for the board meeting of 19 November 2026. The authorised fund "
          "manager publishes the assessment of value with the annual report by 31 January 2027."),
]


def review_terms(out):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("Thornbury Managed Risk UK Equity Fund", level=1)
    doc.add_paragraph("Assessment of value 2025-26: terms for pricing the changes before the board")
    doc.add_paragraph("Owner: Carol Rowe, Head of Investment Oversight. Approved by the board of Thornbury Fund Managers "
                      "Limited on 7 October 2026.")
    for kind, text in TERMS:
        if kind == "h":
            doc.add_heading(text, level=2)
        else:
            doc.add_paragraph(text)
    p = os.path.join(out, "aov_2025-26_review_terms.docx")
    doc.save(p)
    PP.normalize_ooxml(p, "Carol Rowe", "Carol Rowe", "2026-09-29T08:12:00Z", "2026-10-07T15:48:00Z",
                       title="Assessment of value 2025-26: review terms", company="Thornbury Fund Managers Limited")
    PP.scrub_docx(p, total_time=47, title="Assessment of value 2025-26: review terms",
                  company="Thornbury Fund Managers Limited")


# ------------------------------------------------------------------------------------------------ sub-advisers
def sleeve_close_returns(S, tag):
    """the sub-adviser's own monthly returns: the sleeve at the custodian's close prices, chain-linked by day"""
    world, act = S["world"], S["act"]
    rec = act["rec"]
    hold = {}
    for (i, t, sid, q) in act["holdings"]:
        if t == tag:
            hold.setdefault(i, []).append((sid, q))
    pen = act["pen"]
    n = len(DAYS)
    k = np.ones(n)
    for i in range(n):
        noon = clo = 0.0
        for sid, q in hold.get(i, []):
            pn = world["prices"][sid][i]
            pc = world["closes"][sid][i]
            if sid == pen and DAYS[i] >= W.PENROSE_SUSPENDED:
                pn = pc = 0.0
            noon += q * pn
            clo += q * pc
        k[i] = clo / noon if noon else 1.0
    V = rec["V"] if tag == "V" else rec["G"]
    T = rec["TV"] if tag == "V" else rec["TG"]
    vc = V * k
    r = np.zeros(n)
    for i in range(1, n):
        r[i] = vc[i] / (vc[i - 1] + T[i - 1] * k[i - 1]) - 1
    out = {}
    for y, m in MONTHS:
        idx = [i for i, d in enumerate(DAYS) if (d.year, d.month) == (y, m)]
        out[(y, m)] = float(np.prod(1 + r[idx]) - 1)
    return out


def index_month(S, key):
    ix = S["world"]["ix"][key]
    out = {}
    for y, m in MONTHS:
        idx = [i for i, d in enumerate(DAYS) if (d.year, d.month) == (y, m)]
        out[(y, m)] = float(ix[idx[-1]] / ix[idx[0] - 1] - 1)
    return out


def ashcombe(out, S):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    sl = sleeve_close_returns(S, "V")
    bm = index_month(S, "val_close")
    wb = Workbook()
    ws = wb.active
    ws.title = "Performance"
    ws["A1"] = "Ashcombe Investment Partners LLP"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Client: Thornbury Managed Risk UK Equity Fund, value sleeve"
    ws["A3"] = "Mandate benchmark: Larkspur UK Value Index (total return)"
    ws["A4"] = "Report date: 9 October 2026. Returns gross of fees, in sterling, valued at close of business."
    ws.append([])
    ws.append(["Month", "Sleeve return (%)", "Benchmark return (%)", "Relative (%)"])
    for c in ws[6]:
        c.font = Font(bold=True)
    cs = cb = 1.0
    for y, m in MONTHS:
        a, b = sl[(y, m)], bm[(y, m)]
        cs *= 1 + a
        cb *= 1 + b
        ws.append(["%s %d" % (MNAME[m - 1], y), round(a * 100, 2), round(b * 100, 2), round((a - b) * 100, 2)])
    ws.append(["12 months to Sep 2026", round((cs - 1) * 100, 2), round((cb - 1) * 100, 2),
               round((cs - cb) * 100, 2)])
    ws.column_dimensions["A"].width = 24
    for col in "BCD":
        ws.column_dimensions[col].width = 18
    p = os.path.join(out, "ashcombe_mandate_report_sep2026.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Ashcombe Reporting", "Ashcombe Reporting", "2026-10-08T16:02:00Z", "2026-10-09T08:30:00Z",
                       excel=True, company="Ashcombe Investment Partners LLP")


def fennick(out, S):
    sl = sleeve_close_returns(S, "G")
    bm = index_month(S, "gro_close")
    rows = [["Month", "Portfolio (%)", "Larkspur UK Growth TR (%)", "Difference (%)"]]
    cs = cb = 1.0
    for y, m in MONTHS:
        a, b = sl[(y, m)], bm[(y, m)]
        cs *= 1 + a
        cb *= 1 + b
        rows.append(["%s %d" % (MNAME[m - 1], y), "%.2f" % (a * 100), "%.2f" % (b * 100), "%.2f" % ((a - b) * 100)])
    rows.append(["Twelve months", "%.2f" % ((cs - 1) * 100), "%.2f" % ((cb - 1) * 100), "%.2f" % ((cs - cb) * 100)])
    blocks = [
        ("small", "Fennick Capital Limited  |  Quarterly review for Thornbury Fund Managers Limited  |  October 2026"),
        ("h1", "Thornbury Managed Risk UK Equity Fund: growth sleeve"),
        ("p", "Performance to 30 September 2026 against the mandate benchmark, the Larkspur UK Growth Index (total "
              "return). Returns are time-weighted, in sterling, before fees, from close-of-business valuations."),
        ("table", rows),
        ("sp", 8),
        ("small", "Past performance is not a guide to future returns. Prepared for the client named above."),
    ]
    _pdf(os.path.join(out, "fennick_quarterly_review_q3_2026.pdf"), "Quarterly review Q3 2026", "Fennick Capital Limited",
         blocks, b"D:20261012113000+01'00'", b"D:20261012114400+01'00'")


# ------------------------------------------------------------------------------------------------ not needed
def aov_prior(out):
    blocks = [
        ("small", "Thornbury Fund Managers Limited  |  Assessment of value for the year to 30 September 2025  |  "
                  "published 28 January 2026 (extract)"),
        ("h1", "Thornbury Managed Risk UK Equity Fund"),
        ("p", "The board assessed the fund against the seven considerations the FCA's rules require. Its conclusions "
              "for each share class are set out below."),
        ("table", [["Consideration", "B Acc", "B Inc", "C Acc", "C Inc"],
                   ["Quality of service", "Good", "Good", "Good", "Good"],
                   ["Performance", "Fair", "Fair", "Good", "Good"],
                   ["Authorised fund manager costs", "Fair", "Fair", "Good", "Good"],
                   ["Economies of scale", "Good", "Good", "Good", "Good"],
                   ["Comparable market rates", "Fair", "Fair", "Good", "Good"],
                   ["Comparable services", "Good", "Good", "Good", "Good"],
                   ["Classes of units", "Fair", "Fair", "Good", "Good"]]),
        ("sp", 6),
        ("p", "Performance. Over five years to 30 September 2025 the B Accumulation shares returned 31.6 per cent "
              "against 38.9 per cent for the Larkspur UK All-Share Index. The overlay did not reduce equity exposure "
              "during the year."),
        ("p", "Classes of units. Investors holding B shares who qualify for C shares will be offered a conversion "
              "free of charge during 2026. The board will report on take-up next year."),
        ("p", "Ongoing charges figures: B classes 0.85 per cent, C classes 0.60 per cent."),
    ]
    _pdf(os.path.join(out, "aov_2024-25_published_extract.pdf"), "Assessment of value 2024-25",
         "Thornbury Fund Managers Limited", blocks, b"D:20260126140200+00'00'", b"D:20260128091500+00'00'")


def l100_factsheet(out, S):
    world = S["world"]
    ix = world["ix"]
    i1 = IDX[D(2026, 9, 30)]
    i0 = IDX[D(2025, 9, 30)]
    r = W.rng("factsheet")
    big = [s for s in world["secs"] if s["market"] == "Main Market" and s["name"] != "Penrose Bank plc"]
    picks = [big[int(k)] for k in r.choice(len(big), size=10, replace=False)]
    w = np.sort(r.uniform(1.6, 7.4, 10))[::-1]
    rows = [["Constituent", "Industry", "Weight (%)"]] + [[s["name"], s["industry"], "%.2f" % x] for s, x in zip(picks, w)]
    blocks = [
        ("small", "Larkspur Indices Limited  |  Index factsheet  |  data as at 30 September 2026"),
        ("h1", "Larkspur 100 Index"),
        ("p", "The Larkspur 100 Index measures the 100 largest companies by full market capitalisation listed on the "
              "Main Market. It is reviewed quarterly. Futures on the index are listed with quarterly expiries on the "
              "third Friday of March, June, September and December, contract value GBP 10 per index point."),
        ("p", "Index level at close, 30 September 2026: %.1f. Price return over twelve months: %.2f per cent."
         % (ix["l100_close"][i1], (ix["l100_close"][i1] / ix["l100_close"][i0] - 1) * 100)),
        ("h2", "Ten largest constituents"),
        ("table", rows),
        ("sp", 6),
        ("small", "Larkspur Indices accepts no liability for errors in the index or for the use of this factsheet."),
    ]
    _pdf(os.path.join(out, "larkspur_100_factsheet_sep2026.pdf"), "Larkspur 100 Index factsheet", "Larkspur Indices Limited",
         blocks, b"D:20261005070000+01'00'", b"D:20261005070000+01'00'")


def write_all(out, S):
    prospectus(out)
    review_terms(out)
    ashcombe(out, S)
    fennick(out, S)
    aov_prior(out)
    l100_factsheet(out, S)
