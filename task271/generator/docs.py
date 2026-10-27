"""task271 documents: the group's order execution policy, Fenmarsh Wealth's dealing plan for 2027, the desk's 2026
router configuration, and the desk's 2025 venue report (unused by the solution). No file describes the data: every
export names its own columns. Their text is kept here as data so checks.py can quote and execute it."""
from __future__ import annotations

import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2229")
GREY = colors.HexColor("#5d6570")
FIM = colors.HexColor("#1f3d5c")
WEALTH = colors.HexColor("#4a2f5c")
DESK = colors.HexColor("#2f4f3f")
RULE = colors.HexColor("#a5adb6")
HEAD = colors.HexColor("#e8ecf0")


def styles(font, bold, accent, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=6),
        h1=ParagraphStyle("h1" + font + str(size), fontName=bold, fontSize=14.5, leading=18.5, textColor=accent,
                          spaceAfter=3),
        sub=ParagraphStyle("s" + font + str(size), fontName=font, fontSize=8.9, leading=11.8, textColor=GREY,
                           spaceAfter=9),
        h2=ParagraphStyle("h2" + font + str(size), fontName=bold, fontSize=10.6, leading=14.0, textColor=accent,
                          spaceBefore=7, spaceAfter=3),
        cell=ParagraphStyle("c" + font + str(size), fontName=font, fontSize=8.7, leading=10.9, textColor=INK),
        cellb=ParagraphStyle("cb" + font + str(size), fontName=bold, fontSize=8.7, leading=10.9, textColor=INK),
        small=ParagraphStyle("sm" + font + str(size), fontName=font, fontSize=8.2, leading=10.6, textColor=GREY,
                             spaceAfter=4))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm, topMargin=2.0 * cm,
                             bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="Carlito"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(2.1 * cm, 1.2 * cm, left)
        canvas.drawRightString(A4[0] - 2.1 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid(rows, widths, st, head=True):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if (head and k == 0) else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------------- the policy
F_POLICY = "order_execution_policy_2025.pdf"
POLICY = [
    ("1. Scope", [
        "This policy governs how the central dealing desk of Fenmarsh Investment Management executes orders in UK "
        "shares for the funds it manages and for any client flow of the Fenmarsh group the desk deals for. A client "
        "flow is the orders that reach the desk from one source: the funds' portfolio managers, or a platform of the "
        "group that passes its clients' orders to the desk.",
    ]),
    ("2. Execution factors", [
        "The desk takes all sufficient steps to obtain the best possible result for the client, weighing price, costs, "
        "speed, likelihood of execution and settlement, size and the nature of the order. For orders that are small "
        "against the market, price and costs weigh most.",
    ]),
    ("3. How orders are executed", [
        "The desk works an order itself through direct market access, or passes it to an algorithm of one of its two "
        "approved brokers, Ashlowe Securities and Pemberwick & Co, which executes it on the desk's venues in child "
        "orders. Every execution is captured by the desk's order management system and, through the brokers' drop "
        "copies, by the desk's transaction cost provider, Hessenby Analytics.",
    ]),
    ("4. Execution venues", [
        "4.1 The desk executes on the venues listed in Annex A and on no other.",
        "4.2 Each client flow has its own venue list, which the board responsible for the flow approves before the "
        "desk starts dealing for it and reviews each year. The router sends a flow's orders only to venues on its list.",
        "4.3 The adverse-move test. The adverse move of a fill is the change in the mid price from the moment of the "
        "fill to 60 seconds after it, in basis points of the mid at the fill, counted positive when the mid has moved "
        "against the order: down after a buy, up after a sell. A venue's adverse move for a client flow is the average "
        "adverse move of the fills that flow's orders would receive there, in continuous trading. A venue whose "
        "adverse move for a client flow is above 1.5 basis points is kept off that flow's venue list.",
        "4.4 The test is read from the desk's own executions, as the transaction cost provider records them, over the "
        "most recent twelve months or, where a list is first set during a year, over that year to date. The mid is "
        "the mid of the best bid and offer across the consolidated UK market. Executions a broker later busted are "
        "left out.",
        "4.5 A venue on a client flow's list must accept the flow's orders as the flow sends them, in their order "
        "types and sizes.",
    ]),
    ("5. Monitoring", [
        "The desk reports each month the implementation shortfall of its orders: the difference between the average "
        "price of an order's executions and the mid when the desk released the order, in basis points of that mid, "
        "positive when it cost the client. Brokers' algorithms are compared on it each quarter.",
    ]),
    ("6. Governance", [
        "The Best Execution Committee owns this policy and reviews it each year. The head of dealing proposes each "
        "client flow's venue list to the board responsible for the flow, with the evidence the test in 4.3 rests on.",
    ]),
]


def write_policy(path):
    st = styles("LibSerif", "LibSerif-Bold", FIM, 10.2)
    s = [Paragraph("Fenmarsh Investment Management", st["h1"]),
         Paragraph("Order Execution Policy, UK equities. Version 2025.2, approved by the Best Execution Committee on "
                   "15 September 2025. Owner: Head of Dealing", st["sub"])]
    for head, paras in POLICY:
        s.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph(esc("Annex A. Execution venues"), st["h2"]))
    rows = [("Venue", "Operator", "Type", "MIC")]
    for v in K.VENUES:
        info = K.VENUE[v]
        rows.append((info["name"], info["operator"], info["kind"], v))
    s.append(grid(rows, [5.2, 4.6, 3.6, 1.6], st))
    s.append(Spacer(1, 6))
    s.append(Paragraph(esc("The closing auction is held on the Wexcombe Stock Exchange's order book."), st["small"]))
    doc = _doc(path, "Order Execution Policy 2025.2", K.PEOPLE["dealing"])
    doc.build(s, onFirstPage=_footer("Fenmarsh Investment Management  |  Order Execution Policy 2025.2", "LibSerif"),
              onLaterPages=_footer("Fenmarsh Investment Management  |  Order Execution Policy 2025.2", "LibSerif"))


# ---------------------------------------------------------------------------------------------------- dealing plan
F_PLAN = "wealth_dealing_plan_2027.pdf"
PLAN = [
    ("1. Why the change", [
        "Since 2022 Gresmere Stockbrokers has executed the platform's orders in UK shares under an execution-only "
        "agreement that ends on 31 December 2026. From Monday 4 January 2027 the central dealing desk of Fenmarsh "
        "Investment Management deals for the platform, under the group's order execution policy.",
    ]),
    ("2. Dealing points", [
        "The platform deals three times on each UK business day, at 09:30, 12:00 and 14:30 London time, as it does "
        "today. An order joins the next dealing point whose cut-off, 15 minutes before the point, it was placed "
        "before. An order placed after the 14:15 cut-off, at a weekend or on a bank holiday joins the 09:30 point of "
        "the next business day.",
    ]),
    ("3. From client orders to market orders", [
        "At each dealing point the platform adds up its clients' orders in each share, across every account and "
        "wrapper. Buys and sells in the same share cross with each other at the market order's price, and only the "
        "difference goes to market, as one market order. An order to invest a sum of money is converted to shares at "
        "the dealing point. Gresmere did not cross: it sent the buys and the sells in a share as two market orders.",
    ]),
    ("4. Execution", [
        "The desk sends each market order whole to one venue on the platform's venue list, the venue showing the "
        "best price for its full size at that moment. Platform market orders are small against the market, and each "
        "is filled in one execution.",
    ]),
    ("5. The venue list", [
        "The board approves the platform's venue list at its meeting on 9 December 2026 under section 4.3 of the "
        "order execution policy. The head of dealing proposes the list in November with the evidence the policy asks "
        "for.",
    ]),
]


def write_plan(path):
    st = styles("Carlito", "Carlito-Bold", WEALTH, 10.6)
    s = [Paragraph("Fenmarsh Wealth", st["h1"]),
         Paragraph("Client dealing from 4 January 2027. Paper for the board of Fenmarsh Wealth Limited, 12 October "
                   "2026. Oliver Hamilton, Chief Operating Officer", st["sub"])]
    rows = [("Dealing point", "Cut-off", "Orders placed")]
    rows += [("09:30", "09:15", "after 14:15 on the previous business day, or before 09:15"),
             ("12:00", "11:45", "from 09:15 to before 11:45"),
             ("14:30", "14:15", "from 11:45 to before 14:15")]
    for head, paras in PLAN:
        s.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
        if head.startswith("2."):                # the cut-off table sits with the dealing points it sets out
            s.append(grid(rows, [3.2, 2.2, 9.0], st))
    doc = _doc(path, "Client dealing from 4 January 2027", K.PEOPLE["coo"])
    doc.build(s, onFirstPage=_footer("Fenmarsh Wealth  |  Board paper FW-2026-41"),
              onLaterPages=_footer("Fenmarsh Wealth  |  Board paper FW-2026-41"))


# ---------------------------------------------------------------------------------------------------- router 2026
F_ROUTER = "router_configuration_2026.pdf"
ROUTER = [
    ("Order types and venue lists for 2026", [
        "Direct market access orders below 0.1 per cent of a share's average daily volume go to the lit order books "
        "and the systematic internalisers: Wexcombe, Ardenwick lit, Delvenne lit, Brindock SI and Quintrell SI. The "
        "desk's direct access screens are not connected to the midpoint books in 2026.",
        "Orders passed to a broker's algorithm may use all eight venues in Annex A of the order execution policy, as "
        "the algorithm routes them. The desk sets no venue exclusions for the algorithms in 2026.",
        "Closing auction participation goes to Wexcombe through the algorithms that target the close.",
    ]),
    ("Venue changes notified", [
        "Thursgate Trading moves its midpoint book to a new matching platform on 1 June 2026, under the segment code "
        "THGM; the segment code THGD is withdrawn after the close on 29 May. The router's venue tables and the "
        "brokers' venue mappings are updated for 1 June.",
    ]),
    ("Brokers' algorithms", [
        "Ashlowe Securities: Arrival (implementation shortfall), Volume (participation to a volume schedule), Close "
        "(works to the closing auction). Pemberwick & Co: Shortfall (implementation shortfall), VWAP, Inline "
        "(participation to a target rate).",
    ]),
]


def write_router(path):
    st = styles("LibSans", "LibSans-Bold", DESK, 9.8)
    s = [Paragraph("Central dealing desk", st["h1"]),
         Paragraph("Smart order router configuration, 2026. Issued 5 January 2026 by Owen Porter, Head of Dealing",
                   st["sub"])]
    for head, paras in ROUTER:
        s.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    doc = _doc(path, "Router configuration 2026", K.PEOPLE["dealing"])
    doc.build(s, onFirstPage=_footer("Fenmarsh Investment Management  |  Central dealing desk", "LibSans"),
              onLaterPages=_footer("Fenmarsh Investment Management  |  Central dealing desk", "LibSans"))


# ---------------------------------------------------------------------------------------------------- 2025 report
F_REPORT = "venue_volume_report_2025.pdf"
REPORT_ROWS = [("Venue", "Share of volume traded", "Share of orders executed", "Passive", "Aggressive"),
               ("Wexcombe Stock Exchange (XWEX)", "27.4%", "24.9%", "21.0%", "79.0%"),
               ("Ardenwick MTF lit book (AWKL)", "17.2%", "16.8%", "33.5%", "66.5%"),
               ("Delvenne MTF lit book (DLVL)", "15.9%", "15.1%", "30.2%", "69.8%"),
               ("Quintrell Markets SI (QTSI)", "11.8%", "13.6%", "0.0%", "100.0%"),
               ("Brindock Securities SI (BDSI)", "9.6%", "11.2%", "0.0%", "100.0%")]


def write_report(path):
    st = styles("LibSans", "LibSans-Bold", FIM, 9.8)
    s = [Paragraph("Fenmarsh Investment Management", st["h1"]),
         Paragraph("Top five execution venues for 2025: shares and depositary receipts, liquidity bands 5 and 6. "
                   "Published 28 April 2026", st["sub"]),
         Paragraph(esc("Class of instrument: equities, shares and depositary receipts, tick size liquidity bands 5 and "
                       "6. Notification if fewer than one average trade per business day in the previous year: no."),
                   st["body"]),
         grid(REPORT_ROWS, [5.0, 3.2, 3.2, 1.8, 2.4], st),
         Spacer(1, 8),
         Paragraph(esc("Shares of volume and of orders are of the desk's executions in 2025 on all venues, the "
                       "closing auction included in Wexcombe's figures. The midpoint books took 18.1 per cent of "
                       "volume between them."), st["body"])]
    doc = _doc(path, "Top five execution venues 2025", K.PEOPLE["dealing"])
    doc.build(s, onFirstPage=_footer("Fenmarsh Investment Management  |  Venue report 2025", "LibSans"),
              onLaterPages=_footer("Fenmarsh Investment Management  |  Venue report 2025", "LibSans"))


def write_all(out):
    p = lambda f: os.path.join(out, f)
    write_policy(p(F_POLICY))
    write_plan(p(F_PLAN))
    write_router(p(F_ROUTER))
    write_report(p(F_REPORT))
    stamps = {F_POLICY: (b"D:20250915162000+01'00'", b"D:20250915162000+01'00'"),
              F_PLAN: (b"D:20261012113500+01'00'", b"D:20261012113500+01'00'"),
              F_ROUTER: (b"D:20260105083000+00'00'", b"D:20260105083000+00'00'"),
              F_REPORT: (b"D:20260428150500+01'00'", b"D:20260428150500+01'00'")}
    for f, (c, m) in stamps.items():
        PP.normalize_pdf(p(f), c, m)
