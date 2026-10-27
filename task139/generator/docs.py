"""The pack's documents: the Drive Plus rate manual, the contract terms, the Fareline channel agreement summary and
Tarrant Mutual's contractual liability policy summary."""
from __future__ import annotations



from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
INK = colors.HexColor("#1d2330")
GREY = colors.HexColor("#5a6270")
RULE = colors.HexColor("#a3abb6")
PALE = colors.HexColor("#edf0f4")
TEAL = colors.HexColor("#7a4b1e")

BODY = ParagraphStyle("body", fontName=SANS, fontSize=10.4, leading=13.8, textColor=INK, spaceAfter=6)
CL = ParagraphStyle("cl", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15, leading=19, textColor=TEAL, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName=SANS, fontSize=9.6, leading=12.4, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=11.2, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
NOTE = ParagraphStyle("note", fontName=SANS_I, fontSize=9, leading=11.6, textColor=GREY, spaceBefore=6)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=9, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName=SANS_B, fontSize=9, leading=11, textColor=INK)


def _footer(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "%s  |  page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.85 * inch,
                             bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("BACKGROUND", (0, 0), (-1, 0), PALE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def _write(path, title, sub, items, footer, author, closing=None):
    s = [Paragraph(title, H1), Paragraph(sub, H1S)]
    for item in items:
        if isinstance(item, tuple) and item[0] == "TABLE":
            s.append(_table(item[1], item[2]))
            s.append(Spacer(1, 6))
        else:
            n, h, t = item
            s.append(Paragraph("%s %s" % (n, h), H2))
            s.append(Paragraph(t, BODY))
    if closing:
        s.append(Paragraph(closing, NOTE))
    d = _doc(path, title, author)
    d.build(s, onFirstPage=_footer(footer, "Copperline Vehicle Protection"),
            onLaterPages=_footer(footer, "Copperline Vehicle Protection"))


def write_rate_manual(path):
    rows = [["Vehicle class", "Odometer at sale under 50,000", "50,000 to 99,999", "100,000 to 125,000"]]
    for c in K.CLASSES:
        rows.append([c] + ["%s" % format(int(K.base_price(c, lo)), ",") for lo, hi, f in K.ODO_BANDS])
    items = [
        ("1.", "Scope", "This manual sets the price of Copperline Drive Plus, sold through approved dealers and through "
         "channel agreements, for contracts written from 1 January 2026. Vehicle classes follow the class table in "
         "the dealer portal by make, model and engine."),
        ("2.", "Contract price", "The contract price is the base price for the vehicle class and the odometer at sale "
         "below. A channel agreement may add a loading for the use its vehicles see."),
        ("TABLE", rows, [100, 110, 100, 100]),
        ("3.", "High-use surcharge", "For a channel whose vehicles are driven for hire, Copperline may apply a high-use "
         "surcharge of up to 40 per cent of the contract price (the price with any channel loading), the maximum the manual allows."),
        ("4.", "Claims cost", "Claims cost is the payments Copperline makes on covered repairs, net of the deductible "
         "and of reversed lines. Goodwill payments are not claims cost."),
        ("5.", "Channel review", "Before a channel agreement renews, Copperline forecasts the lifetime loss ratio of the "
         "contracts the channel will sell in its next agreement year: the claims cost Copperline will pay over each "
         "contract's cover, at current repair costs and with no trend, over the contract price, for contracts like "
         "those the channel has sold in its current year (the same vehicles, odometers at sale and driving). The "
         "channel renews at current rates if that forecast is 70 per cent or less. Otherwise it renews with the high-use "
         "surcharge at its maximum if the forecast at the surcharged price is 70 per cent or less. Otherwise the channel "
         "lapses at its renewal date."),
        ("6.", "Dealer remittance", "Dealers remit the contract price of each contract they sell on their monthly "
         "bordereau, by ACH, by the end of the month after the sale.")]
    _write(path, "Copperline Drive Plus rate manual", "Effective 1 January 2026. Pricing and Product, Copperline Vehicle "
           "Protection, Fort Worth, Texas. Supersedes the 2025 edition.", items, "Drive Plus rate manual 2026",
           "Copperline Vehicle Protection")


def write_terms(path):
    items = [
        ("1.", "What is covered", "Repairs to the covered components of the engine, transmission, drive axle, cooling "
         "and fuel systems, electrical, steering and air conditioning, by a licensed repair facility, after the "
         "repair order is authorised by Copperline."),
        ("2.", "Term", "This contract runs for 60 months or 75,000 miles from the sale date and the odometer reading at "
         "sale shown on the contract, whichever comes first."),
        ("3.", "Deductible", "You pay 100 dollars for each repair visit."),
        ("4.", "Sale of the vehicle", "This contract does not transfer to a new owner. When the vehicle is sold or "
         "traded, the contract may be cancelled by you, by the selling dealer or by the lienholder shown on the "
         "contract."),
        ("5.", "Cancellation and refund", "A contract is cancelled as of the date Copperline receives the first request "
         "to cancel it. If that date is within 30 days of the sale date and no claim has been made under the "
         "contract by then (a repair order dated on or before it), the full contract price is refunded. Otherwise the refund is the contract price times one less the greater of the share of "
         "1,826 days and the share of 75,000 miles used by the cancellation date, less a cancellation fee of 50 "
         "dollars, and not less than zero. Miles used are the odometer stated on the request that cancels the "
         "contract, less the odometer at sale; where that request states no odometer, the latest odometer on "
         "Copperline's records on or before the cancellation date. If the contract shows a lienholder, the refund is "
         "paid to the lienholder."),
        ("6.", "Your records", "Keep proof of the maintenance the manufacturer recommends. You may upload receipts in "
         "the Copperline app, which records the odometer on each. Your selling dealer fits a CarLink reporter at sale; "
         "it sends Copperline the odometer at each month end while this contract is in force and a closing reading on "
         "the day it ends, and it is removed if the contract is cancelled.")]
    _write(path, "Copperline Drive Plus vehicle service contract: terms and conditions", "Form DP-T 4.2, in use from "
           "August 2023. Obligor: Copperline Vehicle Protection, Fort Worth, Texas.", items, "Form DP-T 4.2",
           "Copperline Vehicle Protection")


def write_agreement(path):
    items = [
        ("1.", "Parties and term", "Copperline Vehicle Protection and Fareline, Inc. (a rideshare platform operating in "
         "Texas and Oklahoma), signed 12 March 2026. The first agreement year runs from 1 April 2026 to 31 December "
         "2026; the agreement renews each 1 January."),
        ("2.", "What Fareline drivers buy", "Copperline Drive Plus on the standard terms (form DP-T 4.2), at the rate "
         "manual's contract price with a commercial-use loading of 20 per cent, paid by the driver in full at sale."),
        ("3.", "Data", "Fareline sends Copperline a weekly mileage feed with the odometer of each car carrying a Drive "
         "Plus contract, by VIN."),
        ("4.", "Renewal election", "By 1 December each year Copperline elects, by written notice, to renew at the "
         "current price, to renew with the rate manual's high-use surcharge, or to let the agreement lapse on 1 "
         "January.")]
    _write(path, "Fareline channel agreement: summary of terms", "Prepared by Commercial, Copperline Vehicle "
           "Protection, for the product committee. The signed agreement governs.", items, "Fareline agreement summary",
           "Copperline Vehicle Protection")


def write_clip(path):
    items = [
        ("1.", "Policy", "Contractual liability insurance policy TMC-CL-2025-118 issued by Tarrant Mutual Casualty "
         "Company to Copperline Vehicle Protection, period 1 July 2025 to 30 June 2026, renewed to 30 June 2027."),
        ("2.", "What it insures", "Copperline's obligations to contract holders under Drive Plus contracts written "
         "during the policy period, should Copperline fail to perform them."),
        ("3.", "Reporting", "Copperline reports contracts written and cancelled each quarter, with the reserve it holds "
         "for them, within 45 days of the quarter's end."),
        ("4.", "Premium", "A rate per contract written by vehicle class, adjusted each year on Copperline's reported "
         "reserves.")]
    _write(path, "Contractual liability insurance: policy summary", "Tarrant Mutual Casualty Company, programme "
           "underwriting. Summary for the insured; the policy wording governs.", items, "TMC-CL-2025-118 summary",
           "Tarrant Mutual Casualty Company")
