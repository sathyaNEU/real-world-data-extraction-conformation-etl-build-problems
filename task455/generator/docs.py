"""The pack's document: the Department of Commerce's designation guideline for the Formation Counties Program."""

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5a636b")
NAVY = colors.HexColor("#1f3a5c")
BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=10, leading=13.8, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("n", parent=BODY, leftIndent=28, firstLineIndent=-28)
TITLE = ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=NAVY, spaceAfter=2)
SUB = ParagraphStyle("s", fontName="LiberationSans", fontSize=10, leading=13.5, textColor=GREY, spaceAfter=12)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.8, leading=14, textColor=NAVY, spaceBefore=7,
                    spaceAfter=3)
CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=9.4, leading=12.2, textColor=INK)
REF = "FC-G-2027-01"


def write_guideline(path):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(22 * mm, 12 * mm, "Formation Counties Program, Designation Guideline %s" % REF)
        canvas.drawRightString(letter[0] - 22 * mm, 12 * mm, "Page %d of 2" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                          bottomMargin=20 * mm, title="Formation Counties Program Designation Guideline %s" % REF,
                          author=W.ORG_COMMERCE, subject="", creator="", producer="")
    P = lambda t: Paragraph(t, NUM)
    s = [Paragraph("Department of Commerce &nbsp;|&nbsp; Office of Business Development", SUB),
         Paragraph("Formation Counties Program", TITLE),
         Paragraph("Designation Guideline for the 2027 to 2029 Grant Period (%s), issued 2 February 2027" % REF, SUB)]
    s.append(Paragraph("1. Purpose", H2))
    s.append(P("1.1&nbsp;&nbsp;The Formation Counties Program helps the counties where new businesses start to keep "
               "them: it funds county development authorities' small business advisers, microloan funds and "
               "incubator space."))
    s.append(P("1.2&nbsp;&nbsp;This guideline sets how the Secretary of Commerce designates the Formation Counties of the "
               "Lornock Valley Development Region for the grant period 1 July 2027 to 30 June 2029, under the "
               "appropriation the legislature made for the program in its 2027 session."))
    s.append(Paragraph("2. Designation", H2))
    s.append(P("2.1&nbsp;&nbsp;The Secretary designates three of the region's seven counties (Brennock, Caldmere, "
               "Dunrath, Eskwell, Fennamore, Quarrin and Tolbeck): the three with the highest establishment birth "
               "rates in calendar year 2026, each county's rate measured from its own establishments."))
    s.append(P("2.2&nbsp;&nbsp;The designation is made by 30 June 2027. Each designated county's development authority "
               "receives a grant of $1,250,000 for the grant period."))
    s.append(P("2.3&nbsp;&nbsp;If a designated county's authority declines the grant or cannot meet its conditions by 1 "
               "September 2027, the county with the next highest rate is designated in its place."))
    s.append(Paragraph("3. Definitions", H2))
    s.append(P("3.1&nbsp;&nbsp;<b>Establishment.</b> A single worksite at which a private employer has employment "
               "covered by the state's unemployment insurance law."))
    s.append(P("3.2&nbsp;&nbsp;<b>County.</b> An establishment is counted in the county in which its worksite lies."))
    s.append(P("3.3&nbsp;&nbsp;<b>Birth.</b> An establishment that first reported employment in 2026 and whose business "
               "did not operate before under another employer account. A business that is sold, reorganised or "
               "changes its legal form and goes on under a new employer account continues; it is not a birth. An "
               "establishment's first reported employment is the first it ever reported under its account, not the "
               "first in the year being measured."))
    s.append(P("3.4&nbsp;&nbsp;<b>Birth rate.</b> A county's births per 100 of its private establishments that reported "
               "employment in at least one month of the fourth quarter of 2025."))
    s.append(Paragraph("4. Rates", H2))
    s.append(P("4.1&nbsp;&nbsp;Rates are computed from the unemployment insurance program's records as the Department "
               "of Workforce Services' Labor Market Information Bureau holds them after the reports for the fourth "
               "quarter of 2026 are due on 30 April 2027."))
    s.append(P("4.2&nbsp;&nbsp;Rates are compared unrounded. The designation memorandum shows them to one decimal."))
    s.append(Paragraph("5. Data and confidentiality", H2))
    s.append(P("5.1&nbsp;&nbsp;The Labor Market Information Bureau prepares the rates under the data sharing agreement "
               "between the Department of Commerce and the Department of Workforce Services (DWS-DOC-2023-07). Records "
               "that identify an employer or a person stay with the bureau; the memorandum to the Secretary reports "
               "county figures."))
    s.append(P("5.2&nbsp;&nbsp;Grant conditions, reporting and payment schedules are set in the grant agreements and are "
               "not part of this guideline."))
    s.append(Spacer(1, 10))
    sig = Table([[Paragraph("Issued for the Secretary of Commerce<br/><br/>%s, Program Director<br/>Office of Business "
                            "Development<br/>2 February 2027" % W.PEOPLE["director"], CELL)]], colWidths=[90 * mm],
                hAlign="LEFT")
    sig.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.5, GREY), ("TOPPADDING", (0, 0), (-1, -1), 6),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(sig)
    s.append(Paragraph("Annex A. Timetable for the 2027 to 2029 grant period", H2))
    rows = [("2 February 2027", "Guideline issued"),
            ("30 April 2027", "Reports for the fourth quarter of 2026 due from employers"),
            ("May 2027", "Labor Market Information Bureau computes the 2026 rates"),
            ("by 30 June 2027", "Secretary designates the Formation Counties"),
            ("1 July 2027", "Grant period begins"),
            ("1 September 2027", "Grant agreements signed; a county that declines is replaced under 2.3"),
            ("30 June 2029", "Grant period ends")]
    tt = Table([[Paragraph("<b>Date</b>", CELL), Paragraph("<b>Step</b>", CELL)]] +
               [[Paragraph(a, CELL), Paragraph(b, CELL)] for a, b in rows], colWidths=[38 * mm, 120 * mm],
               hAlign="LEFT")
    tt.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.5, NAVY), ("TOPPADDING", (0, 0), (-1, -1), 2),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(tt)
    s.append(Paragraph("Annex B. County development authorities eligible to receive a grant", H2))
    auth = [("Brennock", "Brennock County Economic Development Authority"),
            ("Caldmere", "Caldmere County Development Commission"),
            ("Dunrath", "Dunrath Area Economic Development Council"),
            ("Eskwell", "Eskwell Area Development Partnership"),
            ("Fennamore", "Fennamore County Development Corporation"),
            ("Quarrin", "Quarrin County Economic Development Authority"),
            ("Tolbeck", "Tolbeck County Industrial Development Authority")]
    ta = Table([[Paragraph("<b>County</b>", CELL), Paragraph("<b>Authority</b>", CELL)]] +
               [[Paragraph(a, CELL), Paragraph(b, CELL)] for a, b in auth], colWidths=[38 * mm, 120 * mm],
               hAlign="LEFT")
    ta.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.5, NAVY), ("TOPPADDING", (0, 0), (-1, -1), 2),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    s.append(ta)
    d.build(s, onFirstPage=frame, onLaterPages=frame)

