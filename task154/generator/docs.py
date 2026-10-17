"""The pack's documents: the Statistics Office's user guide to the quarterly national accounts and its notice of 24
July, and TBS's June bulletin of merchandise trade and business stocks (with its tables). The text is held here as
data so checks.py can quote it and execute every filed sentence."""
from __future__ import annotations

import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import partners as PT       # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5e656e")
SO = colors.HexColor("#14506e")         # the Statistics Office's blue
TBS = colors.HexColor("#6b3b16")        # TBS's brown
RULE = colors.HexColor("#a6adb6")
HEAD = colors.HexColor("#e6eaef")


def styles(font, bold, accent, size=9.6):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.34, textColor=INK, spaceAfter=4),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.6, leading=13.6, textColor=accent, spaceBefore=6,
                          spaceAfter=2),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=7.9, leading=9.6, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=7.9, leading=9.6, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=7.9, leading=9.6, textColor=INK),
        cellbr=ParagraphStyle("cbr" + font, fontName=bold, fontSize=7.9, leading=9.6, textColor=INK, alignment=2),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.8, leading=10.0, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                             bottomMargin=16 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 9 * mm, left)
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("$", "&#36;")


def grid(rows, widths, st, right_from=1, bold_rows=()):
    data = []
    for k, row in enumerate(rows):
        cells = []
        for j, c in enumerate(row):
            if k == 0:
                sty = st["cellbr"] if j >= right_from else st["cellb"]
            elif k in bold_rows:
                sty = st["cellbr"] if j >= right_from else st["cellb"]
            else:
                sty = st["cellr"] if j >= right_from else st["cell"]
            cells.append(Paragraph(esc(str(c)), sty))
        data.append(cells)
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z(])", p)]


def n1(x):
    return "{:,.1f}".format(x)


def n0(x):
    return "{:,.0f}".format(x)


# ---------------------------------------------------------------------------------------------------- the user guide
GUIDE = [
    ("The quarterly estimates", [
        "The Office publishes three estimates of each quarter's gross domestic product (GDP): the advance estimate "
        "about 30 days after the end of the quarter, the second estimate about 60 days after and the third about 90 "
        "days after. Each is released at 10:45 on its publication day.",
        "GDP is measured from the expenditure side, as household and government final consumption, gross fixed "
        "capital formation and changes in inventories, plus exports less imports. The accounts follow the System of "
        "National Accounts 2008."]),
    ("The headline", [
        "The headline is the percentage change in the volume of GDP from the previous quarter, seasonally adjusted. "
        "It is also published at a compound annual rate, ((1 + q/100) to the fourth power, less 1) times 100 for a "
        "quarterly change of q per cent.",
        "Releases give the headline to one decimal place, from the unrounded estimates."]),
    ("Volumes and prices", [
        "Volumes are chain volume measures at the average prices of the previous calendar year, linked from year to "
        "year. The quarters of 2026 are at 2025 prices. The reference year moves on with each year's March quarter "
        "advance estimate, when the whole series is re-expressed at the new year's prices.",
        "In the quarters of the reference year and after, the components add to GDP.",
        "Estimates are seasonally adjusted. The seasonal factors are re-estimated with each annual update."]),
    ("Contributions to growth", [
        "A component's contribution to growth is its change in volume from the previous quarter as a share of the "
        "previous quarter's GDP, in percentage points. Imports enter with a negative sign. The contributions add to "
        "the quarterly change in GDP."]),
    ("Revisions", [
        "The advance estimate revises no earlier quarter, though each March quarter's advance estimate re-expresses "
        "the whole series at the new reference year's prices. The second estimate revises its own quarter and the one "
        "before; the third estimate its own quarter and the two before.",
        "Each July the annual national accounts revise the quarterly series of the three most recent years to the "
        "annual estimates and re-estimate the seasonal factors.",
        "The Office's real-time database holds every release's estimates of every quarter since 2018, in chain volume "
        "measures at that release's reference-year prices and at current prices. It is updated after each release.",
        "Revisions are measured between growth rates calculated from the unrounded estimates, not between the rounded "
        "headlines."]),
    ("Changes in inventories", [
        "Changes in inventories are the change over the quarter in the volume of goods held by businesses: materials "
        "and supplies, work in progress, finished goods and goods held for resale. For the quarters of 2026 they are "
        "valued at 2025 prices.",
        "Non-farm business inventories are compiled industry by industry from Trade and Business Statistics' monthly "
        "survey of business stocks, with the Office's estimate for businesses outside the survey. Farm and other "
        "inventories come from livestock and crop statistics and the stocks of public trading enterprises."]),
]
SOURCES = [
    ("Household final consumption expenditure", "monthly household spending indicator; retail and services surveys",
     "consumer price index components"),
    ("General government final consumption", "Treasury monthly statements; local government returns",
     "wage and input price indexes"),
    ("Dwellings", "building activity survey", "construction cost index"),
    ("Machinery and equipment", "capital expenditure survey; capital goods imports", "import and producer price indexes"),
    ("Non-dwelling construction", "construction work done survey", "construction cost index"),
    ("Intellectual property products", "software and research and development surveys", "wage and price indexes"),
    ("General government investment", "Treasury monthly statements", "construction and producer price indexes"),
    ("Changes in inventories: non-farm business", "TBS monthly survey of business stocks, by industry",
     "producer price indexes, inputs to each industry"),
    ("Changes in inventories: farm and other", "livestock and crop statistics; public trading enterprises",
     "farm and producer price indexes"),
    ("Exports and imports of goods", "TBS merchandise trade, by SITC section",
     "export and import price indexes, by SITC section"),
    ("Exports and imports of services", "services trade survey; visitor arrivals and departures",
     "services trade price indexes"),
]
CALENDAR = [("December quarter 2025", "29 January 2026", "26 February 2026", "26 March 2026"),
            ("March quarter 2026", "30 April 2026", "28 May 2026", "25 June 2026"),
            ("June quarter 2026", "30 July 2026", "27 August 2026", "24 September 2026")]


def guide_sentences():
    return sentences([p for _, ps in GUIDE for p in ps])


def write_guide(path):
    st = styles("LibSans", "LibSans-Bold", SO, 9.3)
    s = [Paragraph("Statistics Office", st["sub"]),
         Paragraph("Quarterly national accounts: user guide", st["h1"]),
         Paragraph("2026 edition, published with the advance estimate for the March quarter 2026 (30 April 2026)",
                   st["sub"])]
    for title, paras in GUIDE:
        block = [Paragraph(title, st["h2"])] + [Paragraph(esc(p), st["body"]) for p in paras]
        s.append(KeepTogether(block))
    s.append(Paragraph("Sources and price measures", st["h2"]))
    s.append(grid([("Component", "Main sources", "Prices")] + [list(r) for r in SOURCES], [58, 62, 54], st,
                  right_from=9))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Release calendar", st["h2"]))
    s.append(grid([("Quarter", "Advance", "Second", "Third")] + [list(r) for r in CALENDAR], [52, 40, 40, 40], st,
                  right_from=9))
    s.append(Paragraph(esc("The annual national accounts for 2025 are scheduled for Tuesday 21 July 2026."),
                       st["body"]))
    s.append(Spacer(1, 6))
    s.append(Paragraph(esc("Enquiries: national accounts, Statistics Office. This guide replaces the 2025 edition."),
                       st["small"]))
    doc = _doc(path, "Quarterly national accounts: user guide (2026 edition)", "Statistics Office")
    doc.build(s, onFirstPage=_footer("Statistics Office | Quarterly national accounts: user guide, 2026", "LibSans"),
              onLaterPages=_footer("Statistics Office | Quarterly national accounts: user guide, 2026", "LibSans"))
    PP.normalize_pdf(path, b"D:20260429161204+12'00'", b"D:20260429161204+12'00'")


# ---------------------------------------------------------------------------------------------------- the notice
NOTICE = [
    "STATISTICS OFFICE",
    "Notice: gross domestic product, June quarter 2026 (advance estimate)",
    "Friday 24 July 2026",
    "",
    "The advance estimate of gross domestic product for the June quarter 2026 will be published as scheduled, at "
    "10:45 on Thursday 30 July 2026.",
    "",
    "Trade and Business Statistics has told the Office that its June 2026 bulletin of merchandise trade and business "
    "stocks, delayed by the failure of its processing system on 13 July, will be published on Tuesday 28 July. The "
    "advance estimate will incorporate the June results.",
    "",
    "The second estimate for the June quarter remains scheduled for Thursday 27 August 2026.",
    "",
    "Media enquiries: Yvonne Mitchell, national accounts releases.",
]


def write_notice(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(NOTICE) + "\n")


# ---------------------------------------------------------------------------------------------------- the bulletin
BULLETIN_NOTES = [
    ("The outage", [
        "TBS's processing system and data portal have been unavailable since 13 July 2026, when a storage migration "
        "failed. This bulletin, due on 22 July, is issued as a PDF; the portal's tables will be updated when it is "
        "restored."]),
    ("Merchandise trade", [
        "Exports are valued free on board and imports at the value for duty, from the export and import entries "
        "lodged with Customs. Values are in millions of dollars. Seasonally adjusted series are re-estimated as each "
        "month is added; the tables by destination are in original terms.",
        "From the January 2026 month the statistics are compiled on TBS's new processing system."]),
    ("Business stocks", [
        "TBS's monthly survey of wholesalers, retailers and manufacturers collects the book value of the goods each "
        "business holds at the end of the month, as recorded in its accounts, and its cost of sales in the month. "
        "Stocks are at cost.",
        "The stock-to-sales ratio is stocks at the end of the month divided by the month's cost of sales, in months.",
        "Stocks, cost of sales and the ratios are seasonally adjusted."]),
    ("Revisions", [
        "April and May are revised in this issue. March and earlier months are unchanged."]),
]


def bulletin_sentences():
    return sentences([p for _, ps in BULLETIN_NOTES for p in ps])


def write_bulletin(path, T):
    st = styles("Carlito", "Carlito-Bold", TBS, 9.4)
    mo = ["Mar 2026", "Apr 2026 r", "May 2026 r", "Jun 2026"]
    s = [Paragraph("Trade and Business Statistics | Department of Industry", st["sub"]),
         Paragraph("Merchandise trade and business stocks, June 2026", st["h1"]),
         Paragraph("Issued Tuesday 28 July 2026. Contact: Bryan O'Brien, Trade and Business Statistics.", st["sub"])]
    tx = sum(T["exp"][x]["2026-06"] for x in K.SITC_CODES)
    tm = sum(T["imp"][x]["2026-06"] for x in K.SITC_CODES)
    stk = sum(T["stocks"][c]["2026-06"] for c in K.IND_CODES)
    stk3 = sum(T["stocks"][c]["2026-03"] for c in K.IND_CODES)
    s.append(Paragraph(esc(
        "In June, seasonally adjusted exports were $%s million and imports $%s million. Businesses in the survey held "
        "stocks with a book value of $%s million at the end of June, against $%s million at the end of March."
        % (n1(tx), n1(tm), n1(stk), n1(stk3))), st["body"]))
    for name, key in (("Table 1. Exports by SITC section, seasonally adjusted, $ million", "exp"),
                      ("Table 2. Imports by SITC section, seasonally adjusted, $ million", "imp")):
        rows = [["Section"] + mo]
        for sec, title in K.SITC:
            rows.append(["%s %s" % (sec, title)] + [n1(T[key][sec][m]) for m in R.BULLETIN_MONTHS])
        rows.append(["Total"] + [n1(sum(T[key][x][m] for x in K.SITC_CODES)) for m in R.BULLETIN_MONTHS])
        s.append(KeepTogether([Paragraph(name, st["h2"]), grid(rows, [86, 22, 22, 22, 22], st,
                                                                bold_rows=(len(rows) - 1,))]))
    rows = [["Original terms, $ million"] + mo,
            ["Exports"] + [n1(T["orig"]["EXP"][m]) for m in R.BULLETIN_MONTHS],
            ["Imports"] + [n1(T["orig"]["IMP"][m]) for m in R.BULLETIN_MONTHS],
            ["Balance"] + [n1(T["orig"]["EXP"][m] - T["orig"]["IMP"][m]) for m in R.BULLETIN_MONTHS]]
    s.append(KeepTogether([Paragraph("Table 3. Trade totals, original terms", st["h2"]),
                           grid(rows, [86, 22, 22, 22, 22], st)]))
    names = {"JP": "Japan", "CN": "China", "KR": "Korea", "TW": "Taiwan", "IN": "India", "TH": "Thailand",
             "VN": "Viet Nam", "PH": "Philippines"}
    order = ["JP", "CN", "KR", "TW", "IN", "TH", "VN", "PH"]
    rows = [["Destination", "Coal $m", "Coal kt", "LNG $m", "LNG kt"]]
    for c in order:
        e = T["energy"][c]
        rows.append([names[c], n1(e["32"][0]), n1(e["32"][1]) if e["32"][1] else "-",
                     n1(e["34"][0]) if e["34"][0] else "-", n1(e["34"][1]) if e["34"][1] else "-"])
    rows.append(["Total", n1(sum(T["energy"][c]["32"][0] for c in order)), n1(sum(T["energy"][c]["32"][1] for c in order)),
                 n1(sum(T["energy"][c]["34"][0] for c in order)), n1(sum(T["energy"][c]["34"][1] for c in order))])
    s.append(KeepTogether([Paragraph("Table 4. Exports of coal and LNG by destination, June 2026, original terms",
                                     st["h2"]), grid(rows, [50, 24, 24, 24, 24], st, bold_rows=(len(rows) - 1,))]))
    for name, key, fmt in (("Table 5. Business stocks by industry, book value at end of month, seasonally adjusted, "
                            "$ million", "stocks", n1),
                           ("Table 6. Cost of sales by industry, seasonally adjusted, $ million", "sales", n1),
                           ("Table 7. Stock-to-sales ratio by industry, months", "ratio", lambda x: "%.2f" % x)):
        rows = [["Industry"] + mo]
        for c, iname, *_ in K.INDUSTRIES:
            rows.append(["%s %s" % (c, iname)] + [fmt(T[key][c][m]) for m in R.BULLETIN_MONTHS])
        if key != "ratio":
            rows.append(["Total"] + [n1(sum(T[key][x][m] for x in K.IND_CODES)) for m in R.BULLETIN_MONTHS])
        s.append(KeepTogether([Paragraph(name, st["h2"]), grid(rows, [86, 22, 22, 22, 22], st,
                                                                bold_rows=((len(rows) - 1,) if key != "ratio" else ()))]))
    rows = [["$ million", "Apr 2026 previous", "Apr 2026 revised", "May 2026 previous", "May 2026 revised"]]
    for lab, key in (("Exports, seasonally adjusted", "exports"), ("Imports, seasonally adjusted", "imports"),
                     ("Business stocks, end of month", "stocks")):
        a, b = T["revisions"]["2026-04"][key], T["revisions"]["2026-05"][key]
        rows.append([lab, n1(a[0]), n1(a[1]), n1(b[0]), n1(b[1])])
    s.append(KeepTogether([Paragraph("Table 8. Revisions", st["h2"]), grid(rows, [62, 28, 28, 28, 28], st)]))
    s.append(Paragraph("Explanatory notes", st["h2"]))
    for title, paras in BULLETIN_NOTES:
        s.append(Paragraph("<b>%s.</b> %s" % (esc(title), " ".join(esc(p) for p in paras)), st["body"]))
    s.append(Paragraph(esc("Industries: " + "; ".join("%s %s" % (c, n) for c, n, *_ in K.INDUSTRIES) + "."),
                       st["small"]))
    s.append(Paragraph(esc("r revised. Figures may not add to totals because of rounding."), st["small"]))
    doc = _doc(path, "Merchandise trade and business stocks, June 2026", "Trade and Business Statistics")
    doc.build(s, onFirstPage=_footer("TBS | Merchandise trade and business stocks | June 2026", "Carlito"),
              onLaterPages=_footer("TBS | Merchandise trade and business stocks | June 2026", "Carlito"))
    PP.normalize_pdf(path, b"D:20260728105512+12'00'", b"D:20260728105512+12'00'")


def write_all(out, W):
    write_guide(os.path.join(out, R.F_GUIDE))
    write_notice(os.path.join(out, R.F_NOTICE))
    write_bulletin(os.path.join(out, R.F_BULLETIN), W.BULLETIN)
