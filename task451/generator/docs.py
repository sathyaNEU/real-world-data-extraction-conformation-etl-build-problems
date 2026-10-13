"""The pack's two documents: the secretariat's methodology note for its member funds statistics, and the council paper
that sets the decision on the country coordination offices."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import cm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer        # noqa: E402

import world as W   # noqa: E402

METHOD = "member_funds_methodology_2026.pdf"
PAPER = "council_paper_C-26-14.pdf"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#202326")
GREY = colors.HexColor("#5f6368")
TEAL = colors.HexColor("#0f5257")

BODY = ParagraphStyle("body", fontName="LiberationSans", fontSize=10, leading=14, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=24, firstLineIndent=-24)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=15, leading=19, textColor=TEAL, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=12)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=11, leading=15, textColor=TEAL, spaceBefore=8, spaceAfter=3)


def _frame(title):
    def f(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(2.2 * cm, 1.3 * cm, "%s  |  %s" % (W.COLLAB_SHORT, title))
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.3 * cm, "%d" % doc.page)
        canvas.restoreState()
    return f


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.0 * cm,
                             bottomMargin=2.2 * cm, title=title, author=W.SECRETARIAT, subject="", creator="", producer="")


def write_method(path):
    title = "Member funds statistics: methodology note"
    doc = _doc(path, title)
    s = [Paragraph("Member funds statistics: methodology note", H1),
         Paragraph("%s. Version 2, March 2026. Contact: %s, %s." % (W.SECRETARIAT, W.PEOPLE["data"][0], W.PEOPLE["data"][1]), SUB)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. What the statistics are", H2))
    N("1.1", "The secretariat compiles statistics of the members' funding for maternal and newborn health in the "
             "countries where they fund work, from the IATI publications of the members, the pooled funds they give "
             "through and the organisations they and the funds pay. The council uses them to plan the Collaborative's "
             "work in each country.")
    N("1.2", "The members are the organisations on the secretariat's member register.")
    s.append(Paragraph("2. The members' money spent in a country", H2))
    N("2.1", "The members' money spent in a country in a year is the expenditure in that country in that year, by the "
             "organisations that spent it, of money that came from the members, whether the members paid it to those "
             "organisations directly or through one or more pooled funds.")
    N("2.2", "Spending is what the organisation that spent the money reports as expenditure. A payment from one "
             "organisation to another is not spending.")
    s.append(Paragraph("3. Dates, currencies and countries", H2))
    N("3.1", "A transaction belongs to the year of its transaction date.")
    N("3.2", "Amounts are converted to US dollars at the secretariat's exchange table rate for the transaction's value "
             "date, or for its transaction date where it carries none. A transaction that names no currency is in its "
             "activity's default currency.")
    N("3.3", "A transaction is placed in the recipient country it names, and otherwise in its activity's recipient "
             "countries in proportion to their percentages.")
    N("3.4", "Each transaction is converted on its own; totals are summed from the unrounded US dollar amounts and "
             "reported in millions of US dollars to one decimal place.")
    s.append(Paragraph("4. Sources", H2))
    N("4.1", "The IATI Datastore, queried for the countries and sectors the Collaborative works in, and the pooled funds' "
             "own activity files, which carry the activities that name no country.")
    N("4.2", "The members and both pooled funds require every organisation they fund to publish its spending to IATI.")
    N("4.3", "The exchange table gives units of each currency per US dollar for every calendar day, and is kept by the "
             "secretariat's finance team.")
    doc.build(s, onFirstPage=_frame("Methodology note, version 2"), onLaterPages=_frame("Methodology note, version 2"))


def write_paper(path):
    title = "Country coordination offices"
    doc = _doc(path, title)
    s = [Paragraph("Paper C/26/14: Country coordination offices", H1),
         Paragraph("Members' Council, 9 December 2026. From %s, %s. For decision." % (W.PEOPLE["director"][0],
                                                                                    W.PEOPLE["director"][1]), SUB)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    N("1", "The council is asked to choose the three countries in which the Collaborative opens country coordination "
           "offices in 2027.")
    N("2", "At its meeting of 17 June 2026 the council agreed to open three offices, each with three posts, to "
           "coordinate the work the members fund in a country with the government and with each other, and to place "
           "them where the most of the members' money was spent in the latest complete year, 2025, as the "
           "secretariat's member funds statistics measure it. The members' grant plans for 2027 are not yet final, so "
           "the council chose the latest complete year as the basis.")
    N("3", "The secretariat's head of data and learning will present, with this paper, the members' money spent in "
           "2025 in each of the 13 countries where the members fund work, with two further figures for each country "
           "the council asked for in June: the money the members have committed to activities there and not yet "
           "paid, at 30 June 2026, and the number of organisations the members pay directly for work there.")
    N("4", "Once the council has chosen, the secretariat will negotiate host-country agreements and office leases, to be "
           "signed in the first quarter of 2027, within the running costs the secretariat has estimated for each "
           "capital.")
    s.append(Spacer(1, 8))
    s.append(Paragraph("Recommendation: that the council choose three countries on the basis set out in paragraph 2.", BODY))
    doc.build(s, onFirstPage=_frame("Paper C/26/14"), onLaterPages=_frame("Paper C/26/14"))
