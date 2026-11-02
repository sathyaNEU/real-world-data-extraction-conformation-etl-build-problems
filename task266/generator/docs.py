"""The pack's three documents: the Program's 2027-2031 terms, the Fund's 2025-26 annual report and the Mobile Review
Unit's published 2025-26 visit schedule."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1b2227"), colors.HexColor("#59636a"), colors.HexColor("#b5bcc2")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.2, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=22, firstLineIndent=-22))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(18 * mm, A4[1] - 11.5 * mm, left)
        canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 11.5 * mm, right)
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


TERMS_HORIZON = ("The horizon is the shortest step within which at least nine in ten of the mesotheliomas of the "
                 "Program's workforce are diagnosed. The mesotheliomas counted are every mesothelioma (pleural, "
                 "peritoneal or pericardial) among the Program's workforce, whenever it is diagnosed.")
TERMS_YEARS = ("A mesothelioma's years after first exposure run from the day of first exposure to the day of "
               "diagnosis, at 365.25 days to a year, and a step covers the mesotheliomas diagnosed no later than its "
               "number of years after first exposure.")
TERMS_SHAPE = "The share within each step is read from the Fund's mesothelioma register without assuming a shape for the latency curve."
TERMS_FIRST = ("A member's first exposure is the first day of the earliest period of work that the Fund's exposure "
               "assessment records as exposed to asbestos.")
TERMS_INVITE = ("A member is invited to a review in a program year if, on 1 July of that year, at least 20 years and "
                "fewer than the horizon have passed since their first exposure, at 365.25 days to a year.")
REPORT_REGISTER = ("The State Cancer Registry has notified the Fund of every mesothelioma diagnosed in the State since "
                   "the Fund began on 1 July 2004. The register for 2025-26 closed on 30 September 2026 and holds every "
                   "mesothelioma diagnosed to 30 June 2026.")


def write_terms(path):
    S = styles("Serif", colors.HexColor("#25425c"))
    doc = _doc(path, "Former Asbestos Workers Review Program: program terms 2027-2031", K.FUND)
    p = [Paragraph("Former Asbestos Workers Review Program", S["h1"]),
         Paragraph("Program terms for the term 1 July 2027 to 30 June 2031. Approved by the Board of the %s on "
                   "27 November 2026 (resolution 2026/41); they replace the 2023-2027 terms from 1 July 2027." % K.FUND,
                   S["meta"]),
         Paragraph("1. Purpose", S["h2"]),
         Paragraph("1.1 The Program offers former workers who were exposed to asbestos at work in the State a yearly "
                   "review of the chest and lungs, help with a claim to the Fund where a dust disease is found, and one "
                   "point of contact with the Fund.", S["clause"]),
         Paragraph("2. Membership", S["h2"]),
         Paragraph("2.1 A person may join the Program if they were first exposed to asbestos at work in the State "
                   "before 1 January 1986 (the Program's workforce).", S["clause"]),
         Paragraph("2.2 " + TERMS_FIRST, S["clause"]),
         Paragraph("2.3 Membership ends when the member asks, dies or no longer lives in the State.", S["clause"]),
         Paragraph("3. Invitations", S["h2"]),
         Paragraph("3.1 A program year runs from 1 July to 30 June.", S["clause"]),
         Paragraph("3.2 " + TERMS_INVITE, S["clause"]),
         Paragraph("3.3 A member is reviewed at the fixed clinic or the Mobile Review Unit visit nearest their home. "
                   "Fixed clinics run at Port Ellery, Hawksmere, Carrowby, Lindenvale and Murrell Heads; the Mobile "
                   "Review Unit runs a yearly circuit of the State's other towns from its base at Hawksmere.", S["clause"]),
         Paragraph("4. The horizon", S["h2"]),
         Paragraph("4.1 For each term the Board sets the horizon in years after first exposure, in five-year steps "
                   "from 40 to 70 years.", S["clause"]),
         Paragraph("4.2 " + TERMS_HORIZON, S["clause"]),
         Paragraph("4.3 " + TERMS_YEARS, S["clause"]),
         Paragraph("4.4 " + TERMS_SHAPE, S["clause"]),
         Paragraph("5. Reviews", S["h2"]),
         Paragraph("5.1 A review is a chest X-ray (posterior-anterior and lateral views), or a low-dose CT where the "
                   "review nurse decides, with spirometry and a talk with the review nurse. The Program's radiologists "
                   "report every image within ten working days.", S["clause"]),
         Paragraph("5.2 A member with a new finding is referred to a respiratory physician and offered help with a "
                   "claim.", S["clause"]),
         Paragraph("5.3 The Fund pays a member's reasonable travel to a review at the rates in the Fund's travel "
                   "policy.", S["clause"]),
         Paragraph("6. Review of these terms", S["h2"]),
         Paragraph("6.1 The Board will review these terms before 1 July 2031.", S["clause"])]
    doc.build(p, onFirstPage=_frame(K.FUND, "Program terms 2027-2031", "Serif"),
              onLaterPages=_frame(K.FUND, "Program terms 2027-2031", "Serif"))


def write_report(path, figs):
    S = styles("Sans", colors.HexColor("#0f5a64"))
    doc = _doc(path, "Dust Diseases Compensation Fund: Annual Report 2025-26", K.FUND)
    p = [Paragraph("Annual Report 2025-26", S["h1"]),
         Paragraph("%s. Tabled 22 October 2026 under section 58 of the %s." % (K.FUND, K.ACT), S["meta"]),
         Paragraph("The Fund", S["h2"]),
         Paragraph("The Fund was set up by the %s and began on 1 July 2004. It pays compensation to people with "
                   "dust diseases caused by work in the State, recovers its costs from employers' insurers, keeps the "
                   "State's register of mesothelioma and runs the Former Asbestos Workers Review Program." % K.ACT,
                   S["body"]),
         Paragraph("The mesothelioma register", S["h2"]),
         Paragraph(REPORT_REGISTER + " Each case is held with the occupational history taken at its interview, "
                   "with the person or, after a death, with the family, and the Fund's assessment of each period of "
                   "work. On 1 January 2013 the register moved to the Fund's current case system; the cases notified "
                   "before then stayed on the first system, and their interviews were moved across.", S["body"]),
         Paragraph("Compensation", S["h2"]),
         _table(S, [["", "2024-25", "2025-26"],
                    ["Claims lodged (all dust diseases)", figs["lodged"][0], figs["lodged"][1]],
                    ["Claims accepted", figs["accepted"][0], figs["accepted"][1]],
                    ["Lump sums paid ($m)", figs["lump"][0], figs["lump"][1]],
                    ["Medical and care costs paid ($m)", figs["care"][0], figs["care"][1]],
                    ["Recoveries from insurers ($m)", figs["recov"][0], figs["recov"][1]]], [80, 30, 30], right=(1, 2)),
         Spacer(1, 6),
         Paragraph("The Review Program", S["h2"]),
         Paragraph("At 30 June 2026 the Program had %s members. Reviews run at the five fixed clinics and on the "
                   "Mobile Review Unit, which in 2025-26 made %s visits to fourteen towns on its circuit. The Program's "
                   "terms for 2027-2031, which set the horizon of the invitations for the term from 1 July 2027, go "
                   "to the Board in November 2026." % (figs["members"], figs["visits"]), S["body"]),
         Paragraph("Finances", S["h2"]),
         Paragraph("The Fund's levy income was $%sm and its investment income $%sm. Its outstanding claims "
                   "liability, assessed by the Fund's actuary at 30 June 2026, was $%sm." % (figs["levy"], figs["invest"],
                                                                                          figs["liab"]), S["body"])]
    doc.build(p, onFirstPage=_frame(K.FUND, "Annual Report 2025-26", "Sans"),
              onLaterPages=_frame(K.FUND, "Annual Report 2025-26", "Sans"))


def write_schedule(path, unit):
    S = styles("Sans", colors.HexColor("#7a3b12"))
    doc = _doc(path, "Mobile Review Unit: visit schedule 2025-26", K.PROGRAM)
    rows = [["Dates", "Town", "Venue"]]
    for v in sorted(unit, key=lambda x: x["first"]):
        d0, d1 = v["days"][0], v["days"][-1]
        if d0.month == d1.month:
            span = "%d-%d %s" % (d0.day, d1.day, d1.strftime("%B %Y"))
        else:
            span = "%d %s - %d %s" % (d0.day, d0.strftime("%B"), d1.day, d1.strftime("%B %Y"))
        rows.append([span, v["town"], v["venue"]])
    p = [Paragraph("Mobile Review Unit: visit schedule 2025-26", S["h1"]),
         Paragraph("%s. Published 16 June 2025. Reviews 8.30 am to 4.30 pm on each day of a visit; bookings "
                   "through the Program line." % K.PROGRAM, S["meta"]),
         _table(S, rows, [52, 34, 70])]
    doc.build(p, onFirstPage=_frame(K.PROGRAM, "Visit schedule 2025-26", "Sans"),
              onLaterPages=_frame(K.PROGRAM, "Visit schedule 2025-26", "Sans"))
