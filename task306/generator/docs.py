"""The pack's documents: the investment committee's allocation policy, the dealing desk's TCA standard and the
chief investment officer's request. Each carries its own save history; table cells wrap inside the page."""
import datetime as dt
import re
from email.message import EmailMessage
from email.utils import format_datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

INK = colors.HexColor("#1d2b36")
RULE = colors.HexColor("#8a9aa6")


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13.2, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4f5f6b")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                                spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("cell", parent=base, fontSize=8.8, leading=11.2, spaceAfter=0),
            "head": ParagraphStyle("head", parent=base, fontName="Helvetica-Bold", fontSize=8.8, leading=11.2,
                                   spaceAfter=0)}


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, author, blocks, footer, created, modified):
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#5b6b77"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    width = A4[0] - 40 * mm
    for kind, val in blocks:
        if kind == "table":
            ncol = max(len(r) for r in val)
            widths = [44 * mm, width - 44 * mm] if ncol == 2 else [width / ncol] * ncol
            data = [[Paragraph(_esc(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(val)]
            t = Table(data, colWidths=widths, hAlign="LEFT")
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            story += [t, Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    open(path, "wb").write(data)


def policy(path):
    blocks = [
        ("t", "Investment Committee: allocation of new capital to systematic strategies"),
        ("s", "Wealdmoor Investment Management. Policy IC-07, approved by the Investment Committee on 14 April 2026. "
              "Owner: Howard Simpson, Chief Investment Officer."),
        ("h", "1. Scope"),
        ("p", "This policy governs how the Committee places new client capital with a systematic equity strategy "
              "that has not yet run money, when the Research team puts candidate strategies forward with their "
              "backtests."),
        ("h", "2. The comparison"),
        ("p", "New capital goes to the candidate expected to add the most alpha a year at the size allocated. A "
              "candidate's expected alpha at a size is its expected gross alpha less the expected cost a year of "
              "trading its rebalances at that size."),
        ("p", "Expected gross alpha is the annualised gross alpha of the candidate's backtest from 2015 to 2026, as "
              "the Research team's backtest workbook reports it."),
        ("p", "The expected cost of trading is the implementation shortfall, as the dealing desk's TCA standard "
              "defines it, that the candidate's rebalances in the twelve months to 30 November 2026 would have "
              "paid, each rebalance's trades scaled to the capital allocated and traded in full on the rebalance "
              "day. Expected costs are estimated from the desk's own executions. Commissions are paid from the "
              "research budget and are not part of the comparison, and one-off trading to build a portfolio at "
              "launch is outside it."),
        ("h", "3. Paper to the Committee"),
        ("p", "The head of systematic equities puts the comparison to the Committee with the candidate recommended, "
              "the runner-up and the difference between them, alongside the dealing desk's report on the year's "
              "trading of the live strategies."),
        ("table", [["Item", "Owner"],
                   ["Backtests and the rebalance trade log", "Quantitative Research"],
                   ["Implementation shortfall and the desk's executions", "Dealing (Sarah Ford, Head of Trading)"],
                   ["The paper and the recommendation", "Carole Shaw, Head of Systematic Equities"]]),
    ]
    _pdf(path, "IC-07 Allocation of new capital", "Wealdmoor Investment Committee", blocks,
         "Wealdmoor Investment Management  |  IC-07  |  Investment Committee policy",
         "D:20260409113000+01'00'", "D:20260414162000+01'00'")


def tca(path):
    blocks = [
        ("t", "Transaction cost analysis standard"),
        ("s", "Wealdmoor Investment Management, Dealing. Revision 4, effective 1 January 2026. Owner: Sarah Ford, "
              "Head of Trading."),
        ("h", "1. Orders and fills"),
        ("p", "An order is one instruction from a portfolio to buy or sell one stock. The order management system "
              "records each order with its arrival mid, the mid price when the order reached the desk, and each "
              "fill a broker returns against it. An execution id identifies one fill. Fill prices are in pence "
              "unless the fill's price unit says pounds."),
        ("p", "An order the backup order system re-created after a failover of the order management system is the "
              "original order: its fills before and after the failover count together, from the original order's "
              "arrival mid. A block order the desk places for several portfolios at once belongs to them in the "
              "quantities its post-trade allocation gives each, at the block's arrival mid and average fill price."),
        ("h", "2. Implementation shortfall"),
        ("p", "An order's implementation shortfall is the difference between the average price of its fills and its "
              "arrival mid, as a share of the arrival mid, in basis points, signed so that a cost is positive: a buy "
              "that paid more than its arrival mid, or a sell that received less, has a positive shortfall. An "
              "order's value is its filled quantity at its arrival mid. Orders cancelled before they were complete "
              "count for the quantity they filled."),
        ("p", "A portfolio's shortfall for a period is the value-weighted mean of the shortfalls of its orders traded "
              "in the period, an order belonging to the London trade date on which it reached the desk."),
        ("h", "3. Size"),
        ("p", "An order's participation is its value as a share of the stock's average daily traded value, close "
              "times volume, over the 20 sessions before its trade date. A stock's daily volatility is the standard "
              "deviation of its daily log returns over the 60 sessions before."),
        ("h", "4. Reporting"),
        ("p", "Dealing reports each live portfolio's shortfall each quarter and the value it traded, its filled "
              "quantity at the average fill price, each half year. A portfolio's orders are those of the account "
              "codes the trading account register gives it on the trade date."),
        ("table", [["Term", "Meaning"],
                   ["Arrival mid", "The mid price when the order reached the desk"],
                   ["Shortfall", "Average fill price against arrival mid, basis points, cost positive"],
                   ["Participation", "Order value over the 20-session average daily traded value"],
                   ["Trade date", "The London date the order reached the desk"]]),
    ]
    _pdf(path, "TCA standard, revision 4", "Wealdmoor Dealing", blocks,
         "Wealdmoor Investment Management  |  Dealing  |  TCA standard rev. 4",
         "D:20251208094500+00'00'", "D:20251219151000+00'00'")


def request(path):
    m = EmailMessage()
    m["From"] = "Howard Simpson <howard.simpson@wealdmoor-im.co.uk>"
    m["To"] = "Carole Shaw <carole.shaw@wealdmoor-im.co.uk>"
    m["Cc"] = "Sarah Ford <sarah.ford@wealdmoor-im.co.uk>"
    m["Subject"] = "The new GBP 400m mandate: which strategy launches it"
    m["Date"] = format_datetime(dt.datetime(2026, 12, 1, 8, 4, 0, tzinfo=dt.timezone.utc))
    m["Message-ID"] = "<20261201080400.4471@wealdmoor-im.co.uk>"
    m.set_content(
        "Carole,\n\n"
        "The Severnvale money has landed and the GBP 400 million goes live on 4 January. The Committee meets on the "
        "15th and wants one of the three candidates Research put forward to take it, compared the way IC-07 sets "
        "out. Research's workbook and the rebalance trade log are in the folder, with the security master, the "
        "market data, and Sarah's OMS extract of the desk's orders and fills for 2025 and 2026.\n\n"
        "Sarah also needs the year's TCA numbers for the live books in the same pack, so please put them in the "
        "workbook rather than a separate note.\n\n"
        "Thanks,\nHoward\n")
    data = m.as_bytes(policy=m.policy.clone(linesep="\n"))
    open(path, "wb").write(data)
