"""The pack's documents: Attachment C of the pharmacy benefit administration contract (the SMAC program), the survey
contractor's AAC methodology, and the Department's request naming the 2027 candidate classes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as PK   # noqa: E402
import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
pdfmetrics.registerFontFamily("LiberationSerif", normal="LiberationSerif", bold="LiberationSerif-Bold",
                              italic="LiberationSerif-Italic", boldItalic="LiberationSerif-Bold")
INK = colors.HexColor("#1d1f21")
GREY = colors.HexColor("#5a5f66")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=7)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17, textColor=INK, spaceAfter=3, alignment=1)
CAP = ParagraphStyle("cap", fontName="LiberationSerif", fontSize=10, leading=13, textColor=GREY, spaceAfter=14, alignment=1)
H2 = ParagraphStyle("h2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=6, spaceAfter=4)
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=10, leading=14, textColor=INK, spaceAfter=8)
SANSB = ParagraphStyle("sansb", parent=SANS, fontName="LiberationSans-Bold", fontSize=12.5, leading=16, spaceAfter=4)
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=9, leading=11.5, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")


def _doc(path, title, author, footer, style="contract"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        if style == "contract":
            canvas.setFont("LiberationSans", 7.5)
            canvas.drawString(1.0 * inch, 0.6 * inch, footer)
            canvas.drawRightString(LETTER[0] - 1.0 * inch, 0.6 * inch, "Page %d" % doc.page)
        elif style == "report":
            # the survey contractor's report style: a running head over a rule, the page number centred below
            canvas.setFont("LiberationSerif-Italic", 8.5)
            canvas.drawString(1.0 * inch, LETTER[1] - 0.55 * inch, footer)
            canvas.setStrokeColor(GREY)
            canvas.setLineWidth(0.4)
            canvas.line(1.0 * inch, LETTER[1] - 0.6 * inch, LETTER[0] - 1.0 * inch, LETTER[1] - 0.6 * inch)
            canvas.setFont("LiberationSerif", 9)
            canvas.drawCentredString(LETTER[0] / 2.0, 0.55 * inch, "%d" % doc.page)
        else:
            # the Department's letterhead: the address line centred at the foot, no page number on a one-page letter
            canvas.setFont("LiberationSans", 7)
            canvas.drawCentredString(LETTER[0] / 2.0, 0.5 * inch, footer)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                          bottomMargin=0.95 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def write_terms(path):
    title = "Attachment C: State Maximum Allowable Cost Program"
    doc, frame = _doc(path, title, W.DEPARTMENT,
                      "Pharmacy Benefit Administration Contract  |  Attachment C  |  as amended effective 1 July 2026")
    s = [Paragraph("PHARMACY BENEFIT ADMINISTRATION CONTRACT", H1),
         Paragraph("between the %s and %s<br/>Attachment C: State Maximum Allowable Cost Program, as amended effective "
                   "1 July 2026" % (W.DEPARTMENT, W.ADMIN), CAP)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("The list and its rates", H2))
    N("C.1", "The State Maximum Allowable Cost (SMAC) list caps the ingredient cost the Program pays for the generic "
             "products on it. The Administrator keeps the list and sets each listed product's rate per unit.")
    N("C.2", "A SMAC rate applies to every NDC of a listed product, whatever its labeler or package. For a claim the "
             "Program pays the ingredient at the lesser of the pharmacy's usual and customary charge, the State actual "
             "acquisition cost (AAC) rate in effect for the NDC on the fill date, the SMAC rate where the product is "
             "listed and, where no AAC rate is in effect for the NDC, the wholesale acquisition cost (WAC). The "
             "professional dispensing fee is paid separately.")
    s.append(Paragraph("The annual update", H2))
    N("C.3", "Each year the Department names, by 15 March, the drug classes that are candidates for the list. The "
             "Administrator proposes one of them by the first business day of May, and the class proposed and approved "
             "is added on 1 July.")
    N("C.4", "The Administrator proposes the candidate class with the largest ingredient spread over the twelve months of "
             "fills ending with the last calendar quarter closed before the proposal. The comparison is made on "
             "unrounded figures.")
    N("C.5", "The ingredient spread of a class is the ingredient cost the Program paid on the class's fee-for-service "
             "claims, net of reversals, less the acquisition cost of the units those claims dispensed: what the "
             "dispensing pharmacies paid their suppliers for them.")
    N("C.6", "The proposal sets out each candidate class's ingredient spread and, for the Department's budget, the "
             "class's claims, units dispensed and ingredient cost paid over the twelve months of fills before those.")
    s.append(Paragraph("Rates in force and appeals", H2))
    N("C.7", "The Administrator reviews listed rates each month against the State AAC rates and the market and hears "
             "pharmacy appeals within ten business days. A rate changed on appeal applies from the date of the appeal.")
    s.append(Spacer(1, 10))
    s.append(Paragraph("Amendment 3, approved by the Department and the Administrator, effective 1 July 2026.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_method(path):
    title = "State Actual Acquisition Cost: Survey and Rate-Setting Methodology"
    doc, frame = _doc(path, title, W.SURVEY, "%s: State AAC survey and rate-setting methodology, January 2026" % W.SURVEY,
                      style="report")
    s = [Paragraph(title.upper(), H1),
         Paragraph("Prepared for the %s, Pharmacy Program, by %s. Revised January 2026." % (W.DEPARTMENT, W.SURVEY), CAP)]
    P = lambda t: s.append(Paragraph(t, BODY))
    s.append(Paragraph("1. What a rate is", H2))
    P("A State AAC rate is the average price per unit that community pharmacies pay their suppliers for an NDC, net of "
      "the discounts shown on the invoice. Rates are per pricing unit: each for tablets and capsules, millilitre for "
      "liquids.")
    s.append(Paragraph("2. The survey", H2))
    P("Each month a random sample of about one in five of the community pharmacies enrolled with the Program submits "
      "its purchase invoices for the month. Invoices from wholesalers and direct purchases from manufacturers are both "
      "used; credits and returns are netted against the purchases they reverse.")
    s.append(Paragraph("3. Setting the rates", H2))
    P("For each NDC whose invoices in the month carry at least 30 purchase lines from at least five pharmacies, the "
      "contractor computes the average invoice price per unit. A new rate is published when that average differs from "
      "the rate in effect by more than 2 per cent; otherwise the rate in effect continues. Rates take effect on the "
      "first day of a month.")
    P("Not every NDC has a rate. An NDC whose month's invoices fall below the purchase count carries no rate for that "
      "month, and an NDC that drops below it after being priced loses its rate from the first day of the month. The "
      "Program pays claims for NDCs without a rate on its other bases.")
    s.append(Paragraph("4. Publication", H2))
    P("The contractor publishes the rate file to the Department and the Program's claims processor on the first business "
      "day of each month. Each row carries the NDC, the rate, the pricing unit and the dates the rate is in effect.")
    s.append(Spacer(1, 12))
    s.append(Paragraph("%s<br/>Project manager, %s" % (W.PEOPLE["survey"], W.SURVEY), SANS))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_request(path):
    title = "Candidate classes for the 1 July 2027 SMAC update"
    doc, frame = _doc(path, title, W.DEPARTMENT, "%s, Pharmacy Program  |  1400 Capitol Avenue, Suite 600" % W.DEPARTMENT,
                      style="letter")
    s = [Paragraph(W.DEPARTMENT.upper(), SANSB), Paragraph("Pharmacy Program", SANS), Spacer(1, 6),
         Paragraph("8 March 2027", SANS),
         Paragraph("%s<br/>Account director, %s" % (W.PEOPLE["account"], W.ADMIN), SANS),
         Paragraph("<b>Re: %s</b>" % title, SANS)]
    P = lambda t: s.append(Paragraph(t, SANS))
    P("Under Attachment C, section C.3, the Department names the following twelve drug classes as the candidates for "
      "the 1 July 2027 update of the State Maximum Allowable Cost list. Please send the Administrator's proposal by "
      "3 May 2027.")
    rows = [[Paragraph("Class code", CELLB), Paragraph("Class", CELLB)]]
    for nm in W.SHORTLIST_NAMES:
        rows.append([Paragraph(PK.class_code(nm), CELL), Paragraph(nm, CELL)])
    t = Table(rows, colWidths=[1.1 * inch, 3.6 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaed")),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    s += [t, Spacer(1, 10)]
    P("The classes are those of the drug class list in force from 1 January 2027, which the Department sent with this "
      "letter.")
    s += [Spacer(1, 8), Paragraph("%s<br/>Pharmacy Director" % W.PEOPLE["director"], SANS)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
