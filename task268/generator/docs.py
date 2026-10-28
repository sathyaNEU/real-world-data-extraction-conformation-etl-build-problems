"""The pack's documents: the chief underwriting officer's terms for the 2027 telematics pilot, the Motor Claims Reserving
Standard (version 4), the telematics supplier's quotation and the planning thread."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, K.FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2327"), colors.HexColor("#5d666c"), colors.HexColor("#b7c0c6")
TEAL, PLUM, SLATE = colors.HexColor("#0f5f66"), colors.HexColor("#5b2a4e"), colors.HexColor("#2f3e4c")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.5, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.3, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.3, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=24, firstLineIndent=-24))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.5)
        canvas.drawString(18 * mm, A4[1] - 11 * mm, left)
        canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 11 * mm, right)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _d(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


# ---------------------------------------------------------------------------------------------- the pilot terms
TERMS = [
    ("1", "Purpose", "The pilot tests whether a telematics policy, priced at each renewal on the driving the device "
     "records, reduces claim frequency on Corriven's private-car book. It runs for twelve months from 1 March 2027 "
     "and its result informs the 2028 rating plan."),
    ("2", "Where the pilot runs", "The pilot runs in the two sales regions whose private-car policies had the highest "
     "claim frequency in accident year 2025."),
    ("3", "Claim frequency", "Claim frequency for accident year 2025 is the number of claims arising from accidents "
     "between 1 January and 31 December 2025 under private-car policies in the region, whether or not they had been "
     "notified to Corriven by the end of 30 September 2026, per 100 car-years earned in the region in 2025. Claims "
     "are counted as the Motor Reserving Standard counts them, including claims closed without payment, and claims "
     "not yet notified are estimated as that Standard provides. Earned car-years are the pricing mart's earned "
     "exposure for private cars."),
    ("4", "Regions", "A claim or a car belongs to the sales region of its risk postcode district, on the 2025 drawing "
     "of the regions. Vans and other light commercial vehicles are outside the pilot."),
    ("5", "Reporting", "Frequencies are reported per 100 car-years to one decimal place."),
    ("6", "The offer", "Policyholders in the pilot regions are offered the device at renewal from 1 March 2027. "
     "COMP, TPFT and TPO policies are each offered their own discount scale, so the supplier's order is placed by "
     "cover."),
    ("7", "Timetable", "The regions are decided on %s. The supplier's order is placed by %s, and fitting "
     "starts in February 2027." % (_d(K.DECISION_DATE), _d(K.ORDER_DATE))),
    ("8", "Evaluation", "The pilot's claim frequency is compared at the end of the pilot with the same regions' "
     "policyholders who declined the device and with the other three regions, adjusted for the rating factors. The "
     "evaluation plan is a separate paper."),
]


def write_terms(path):
    S = styles("Sans", TEAL)
    doc = _doc(path, "Telematics pilot 2027: terms", "Chief Underwriting Officer")
    st = [Paragraph("Telematics pilot 2027", S["h1"]),
          Paragraph("Terms set by %s, Chief Underwriting Officer, %s, after consultation with Pricing, Claims and "
                    "Reserving. Distribution: Motor Pricing, Claims, Reserving, Underwriting Operations." % (K.PEOPLE["cuo"], _d(K.TERMS_DATE)), S["meta"])]
    for num, head, text in TERMS:
        st.append(Paragraph("%s&nbsp;&nbsp;%s" % (num, head), S["h2"]))
        st.append(Paragraph(text, S["body"]))
    doc.build(st, onFirstPage=_frame(K.ORG_LTD, "Underwriting", "Sans"),
              onLaterPages=_frame(K.ORG_LTD, "Underwriting", "Sans"))


# ---------------------------------------------------------------------------------------------- the reserving standard
STANDARD = [
    ("1", "Scope", [
        ("1.1", "This Standard governs the estimation of claim numbers and claim amounts for Corriven's private-car and "
                "light commercial vehicle books, for the quarterly reserving review, the annual actuarial function "
                "report and any pricing or portfolio work that uses claim numbers.")]),
    ("2", "Claims and accident years", [
        ("2.1", "A claim is one claimant's claim under one head of claim (own damage, third-party property damage, "
                "third-party injury, theft, fire or glass) arising from one accident. One accident can give rise to "
                "several claims. Every claim notified counts once, including claims closed without payment."),
        ("2.2", "Claims are grouped by the calendar year of the accident and valued at 30 September each year. The "
                "valuation age of an accident year is counted in months from 1 January of that year, so an accident "
                "year is 21 months old at the first 30 September after it ends."),
        ("2.3", "An accident year is closed three years after its last day, and its claim count is then final.")]),
    ("3", "Claims not yet notified", [
        ("3.1", "The number of claims incurred but not yet notified for an open accident year is estimated by "
                "development. Development factors are measured on the closed accident years of the whole private-car "
                "book, from their counts at the same valuation age to their final counts."),
        ("3.2", "Sales-region estimates apply the whole book's factors to each region's notified claims; regional "
                "triangles are too thin to give stable factors."),
        ("3.3", "Before a development basis is used for an open accident year, it is re-run on the most recent closed "
                "accident year from that year's position at the same valuation age, with only the closed accident "
                "years before it. The basis is used only if its estimate reproduces that year's final count in every "
                "sales region to within two per cent.")]),
    ("4", "Claim amounts", [
        ("4.1", "Case estimates are set by the handler at first contact and reviewed at each material change and at "
                "least every 90 days. Injury estimates follow the Judicial College guidelines and, for claims under "
                "the whiplash tariff, the tariff in force at the date of the accident."),
        ("4.2", "Incurred but not enough reported amounts are projected on paid and incurred triangles by head of "
                "claim. Claims over 250,000 pounds incurred are projected individually by the large loss team and "
                "excluded from the triangles."),
        ("4.3", "Periodical payment orders are valued at the discount rate set in the reserving basis, with the "
                "personal injury discount rate of the date of settlement for lump sums.")]),
    ("5", "Governance", [
        ("5.1", "The Chief Actuary owns this Standard and reviews it each year. Changes are approved by the Reserving "
                "Committee. Version 4 replaces version 3 from 1 December 2025; the change is the back-test in 3.3, "
                "which version 3 required only for the annual report.")]),
]


def write_standard(path):
    S = styles("Serif", PLUM)
    doc = _doc(path, "Motor Claims Reserving Standard, version 4", "Chief Actuary")
    st = [Paragraph("Motor Claims Reserving Standard", S["h1"]),
          Paragraph("Version 4. Approved by the Reserving Committee on %s; effective 1 December 2025. Owner: Chief "
                    "Actuary." % _d(K.STANDARD_DATE), S["meta"])]
    for num, head, clauses in STANDARD:
        st.append(Paragraph("%s&nbsp;&nbsp;%s" % (num, head), S["h2"]))
        for cn, text in clauses:
            st.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (cn, text), S["clause"]))
    doc.build(st, onFirstPage=_frame(K.ORG_LTD, "Reserving Standard v4", "Serif"),
              onLaterPages=_frame(K.ORG_LTD, "Reserving Standard v4", "Serif"))


# ---------------------------------------------------------------------------------------------- the supplier's quote
def write_quote(path):
    S = styles("Sans", SLATE)
    doc = _doc(path, "Quotation Q-26-1184", "Brackwell Telematics Ltd")
    st = [Paragraph("Quotation Q-26-1184: device telematics for private-car policies", S["h1"]),
          Paragraph("Brackwell Telematics Ltd, Unit 4, Brunel Park, Northampton NN4 7BF. For Corriven Insurance "
                    "Limited, attention %s. Issued 22 September 2026; valid to 31 December 2026." % K.PEOPLE["cuo"],
                    S["meta"]),
          Paragraph("Scope", S["h2"]),
          Paragraph("Supply and fitting of the VT-5 self-install device, the driving-score service and the claims "
                    "notification feed for a twelve-month pilot, with an option to extend. Devices are posted to the "
                    "policyholder on renewal and activate on first journey; a fitter visit is offered where the car has "
                    "no accessible OBD port.", S["body"]),
          Paragraph("Charges", S["h2"]),
          _table(S, [["Item", "Unit", "Price (GBP, excl. VAT)"],
                     ["VT-5 device, posted", "per device", "38.50"],
                     ["Fitter visit (where required)", "per visit", "64.00"],
                     ["Driving-score and data service", "per active device per month", "2.15"],
                     ["First-notice crash alert and reconstruction", "per alert", "11.00"],
                     ["Returns handling at lapse", "per device", "6.20"],
                     ["Programme set-up and integration", "once", "18,500.00"]], [92, 44, 38], right=(2,)),
          Spacer(1, 6),
          Paragraph("Volume terms", S["h2"]),
          _table(S, [["Devices ordered", "Device price", "Data service"],
                     ["up to 5,000", "list", "list"],
                     ["5,001 to 20,000", "list less 6 per cent", "list less 4 per cent"],
                     ["over 20,000", "list less 11 per cent", "list less 8 per cent"]], [60, 56, 58]),
          Spacer(1, 6),
          Paragraph("Terms", S["h2"]),
          Paragraph("Prices are fixed for orders placed before 31 December 2026. The volume tier is set by the devices "
                    "on the order. Data is held in the United Kingdom and processed under the data processing "
                    "agreement of 14 May 2025. Expected take-up in comparable pilots has been 18 to 31 per cent of "
                    "renewing policies offered the device.", S["body"])]
    doc.build(st, onFirstPage=_frame("Brackwell Telematics Ltd", "Q-26-1184", "Sans"),
              onLaterPages=_frame("Brackwell Telematics Ltd", "Q-26-1184", "Sans"))


# ---------------------------------------------------------------------------------------------- the planning thread
def thread_text():
    a, c, i = K.PEOPLE["actuary"], K.PEOPLE["cuo"], K.PEOPLE["claims"]
    mail = lambda n: n.lower().replace(" ", ".") + "@corriven.co.uk"
    msgs = [
        (c, [a, i], dt.datetime(2026, 10, 7, 9, 12), "Telematics pilot: paper for 13 November",
         "Carol, Iain,\n\nI signed off the pilot terms yesterday (attached). Brackwell's quote holds to the end of "
         "the year, and I want the order placed by 27 November so fitting can start in February. Could I have the "
         "paper by 13 November? It needs to name the two regions with the 2025 frequencies behind them, "
         "and tell Brackwell how many cars it is ordering for.\n\nDamian"),
        (a, [c, i], dt.datetime(2026, 10, 7, 14, 40), "RE: Telematics pilot: paper for 13 November",
         "Damian,\n\nYes. I'll work from the claims extract Data took on 1 October (everything notified to the end of "
         "30 September) and the pricing mart's exposure, and do the 2025 year on the terms' basis, all five regions so "
         "you see the gap below the two.\n\nFor Brackwell I'll count the private cars on cover at 30 "
         "September, region by region and by cover, since each cover has its own discount scale.\n\nCarol"),
        (i, [a, c], dt.datetime(2026, 10, 8, 8, 55), "RE: Telematics pilot: paper for 13 November",
         "Damian, Carol,\n\nBrackwell's crash alerts will come into my first-notice desk from February, so I need the "
         "two regions settled before the order goes. Happy to help with the claims extract if anything in it looks "
         "odd.\n\nIain"),
        (c, [a, i], dt.datetime(2026, 10, 9, 17, 31), "RE: Telematics pilot: paper for 13 November",
         "Thanks both. A workbook with the figures and a short deck I can decide from, please; four or five slides "
         "is plenty.\n\nDamian"),
    ]
    out = []
    for frm, to, t, subj, body in reversed(msgs):
        out.append("From: %s <%s>\nTo: %s\nDate: %s\nSubject: %s\n\n%s\n" % (
            frm, mail(frm), "; ".join("%s <%s>" % (x, mail(x)) for x in to),
            t.strftime("%a %d %b %Y %H:%M"), subj, body))
    return ("\n" + "-" * 72 + "\n\n").join(out)
