"""task183 documents: the Bank's Business Cash Review Standard BCR-3 (PDF). The ask documents are written by
asks.py with the same helpers."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Italic", FONT_DIR + "LiberationSans-Italic.ttf"))
SANS, SANS_B, SANS_I = "LiberationSans", "LiberationSans-Bold", "LiberationSans-Italic"
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5d6570")
BRAND = colors.HexColor("#123f6b")
BODY = ParagraphStyle("body", fontName=SANS, fontSize=9.6, leading=13.0, textColor=INK, spaceAfter=4.5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=10 * mm, firstLineIndent=-10 * mm)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15, leading=19, textColor=BRAND, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
META = ParagraphStyle("meta", fontName=SANS, fontSize=8.2, leading=10.8, textColor=GREY, spaceAfter=9)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.6, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)


def frame(left, right, org=W.BANK):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(BRAND)
        canvas.setLineWidth(1.2)
        canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
        canvas.setFont(SANS_B, 7.6)
        canvas.setFillColor(BRAND)
        canvas.drawString(18 * mm, A4[1] - 12 * mm, org.upper())
        canvas.setFont(SANS, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 11 * mm, left)
        canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")


def table(rows, widths, head=1, align_right=()):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(str(x), CELLB if i < head else CELL) for x in r])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=head)
    style = [("LINEBELOW", (0, 0), (-1, head - 1), 0.8, BRAND), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LINEBELOW", (0, head), (-1, -1), 0.25, colors.HexColor("#d4d8de")),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    for c in align_right:
        style.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t


def c(no, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (no, text), CLAUSE)


def write_bcr3(path):
    s = []
    s.append(Paragraph("Business Cash Review Standard", H1))
    s.append(Paragraph("BCR-3, issue 3. Owner: %s, Money Laundering Reporting Officer. Approved by the Financial "
                       "Crime Risk Committee on 18 June 2025; effective for review years from 1 October 2025."
                       % W.PEOPLE["mlro"], META))
    s.append(Paragraph("1. Purpose", H2))
    s.append(c("1.1", "Each year the Bank reviews the business customers whose trade is mostly taken in cash for cash "
                      "put through their accounts that their own trading did not take, and refers those customers to "
                      "Financial Crime Investigations. This standard sets the population, the year, the quantity "
                      "reviewed and the line for referral. It supersedes BCR-2."))
    s.append(Paragraph("2. Population and review year", H2))
    s.append(c("2.1", "The population is every customer on the cash-intensive segment's review list for the year. "
                      "Financial Crime Operations draws the list at the start of October from the trades in "
                      "Schedule A."))
    s.append(c("2.2", "The review year runs from 1 October to 30 September. The review year 2025-26 runs from "
                      "1 October 2025 to 30 September 2026."))
    s.append(Paragraph("3. Lodgements", H2))
    s.append(c("3.1", "A lodgement is cash, in notes or coin, handed in for credit to a customer's account at a "
                      "branch counter of the Bank or at a post office counter under the Bank's agency arrangement "
                      "with An Post."))
    s.append(c("3.2", "A lodgement is dated by the day the cash was handed in at the counter. The cash a customer "
                      "lodged in the review year is the total of its lodgements dated in that year, to all of its "
                      "accounts with the Bank."))
    s.append(Paragraph("4. Unexplained cash and referral", H2))
    s.append(c("4.1", "A customer's unexplained cash for the review year is the cash it lodged in the review year "
                      "beyond what its own trading took."))
    s.append(c("4.2", "Where a customer runs the Bank's till service throughout the review year, what its own "
                      "trading took is the cash sales its till recorded in the review year."))
    s.append(c("4.3", "Every customer whose unexplained cash for the review year is more than EUR 40,000 is "
                      "referred to Financial Crime Investigations at the Financial Crime Risk Committee's January "
                      "meeting. A referral restricts the customer's accounts until Financial Crime Investigations "
                      "closes the case."))
    s.append(c("4.4", "A referral is not a finding of wrongdoing, and no customer is contacted about the review "
                      "before the committee meets."))
    s.append(Paragraph("5. Timetable and records", H2))
    s.append(c("5.1", "The review is carried out on the Bank's own records, pulled after the review year closes. "
                      "Financial Crime Operations presents its referral paper to the committee in January."))
    s.append(c("5.2", "The referral paper and the review's working files are kept for six years from the "
                      "committee's decision."))
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph("Schedule A. Trades in the cash-intensive segment", H2))
    rows = [["Trade", "Typical business"]]
    for tkey, tlabel, _, _, _ in W.TRADES:
        rows.append([tlabel, {"cafe": "cafes, coffee shops and tea rooms", "takeaway": "chippers, takeaways, pizza "
                              "and kebab shops", "barber": "barbers and hairdressers", "nails": "nail bars and "
                              "beauty salons", "carwash": "hand car washes and valeting centres", "convenience":
                              "convenience stores and newsagents", "launderette": "launderettes and dry cleaners"}[tkey]])
    s.append(table(rows, [62, 108]))
    d = doc(path, "Business Cash Review Standard BCR-3", W.PEOPLE["mlro"])
    d.build(s, onFirstPage=frame("BCR-3 Business Cash Review Standard, issue 3", "Financial Crime"),
            onLaterPages=frame("BCR-3 Business Cash Review Standard, issue 3", "Financial Crime"))


def write_apfee(path):
    """Schedule 2 (fees) of the agency services agreement between An Post and the Bank."""
    s = []
    s.append(Paragraph("Agency Services Agreement: Schedule 2, Fees", H1))
    s.append(Paragraph("Between An Post and %s. Agreement dated 4 March 2024; this schedule as varied with effect "
                       "from 1 July 2025." % W.BANK, META))
    s.append(Paragraph("1. Business lodgements", H2))
    s.append(c("1.1", "For each business lodgement that a post office counter takes for a customer of the Bank, the "
                      "Bank pays An Post a transaction fee of EUR 1.15 and a cash handling fee of 0.065 per cent of "
                      "the cash lodged, notes and coin together."))
    s.append(c("1.2", "The fees are worked out lodgement by lodgement, and the fees for each lodgement are rounded "
                      "to the nearest cent, a half cent rounding up."))
    s.append(c("1.3", "A lodgement falls in the calendar month in which the counter took it."))
    s.append(Paragraph("2. Invoicing and payment", H2))
    s.append(c("2.1", "An Post invoices the Bank monthly in arrears for the lodgements of the month. The Bank pays "
                      "within 30 days of the invoice."))
    s.append(c("2.2", "No VAT is chargeable on the fees in this schedule."))
    s.append(c("2.3", "Either party may ask for a lodgement-level reconciliation of an invoice within six months of "
                      "its date. Differences found are settled on the next invoice."))
    s.append(Paragraph("3. Other services", H2))
    s.append(c("3.1", "Personal lodgements, bill payments and cash withdrawals under the agreement are priced in "
                      "Schedule 3 and are not covered by this schedule."))
    d = doc(path, "Agency Services Agreement Schedule 2", "An Post Agency Services")
    d.build(s, onFirstPage=frame("Agency Services Agreement, Schedule 2", "Commercial in confidence", org="An Post"),
            onLaterPages=frame("Agency Services Agreement, Schedule 2", "Commercial in confidence", org="An Post"))
