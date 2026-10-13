"""The pack's documents: the Regional Rapid Response Program Regulation (consolidated) and the Provincial Revenue
Agency's release note on placing payroll jobs at the workplace from the January 2026 reference month."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

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
NUM = ParagraphStyle("num", parent=BODY, leftIndent=26, firstLineIndent=-26)
SUB = ParagraphStyle("sub", parent=BODY, leftIndent=44, firstLineIndent=-18)
DEF = ParagraphStyle("def", parent=BODY, leftIndent=44, firstLineIndent=0)
H1 = ParagraphStyle("h1", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17, textColor=INK, spaceAfter=3, alignment=1)
CAP = ParagraphStyle("cap", fontName="LiberationSerif", fontSize=10, leading=13, textColor=GREY, spaceAfter=14, alignment=1)
H2 = ParagraphStyle("h2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=6, spaceAfter=4)
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=10, leading=14, textColor=INK, spaceAfter=8)
SANSB = ParagraphStyle("sansb", parent=SANS, fontName="LiberationSans-Bold", fontSize=13, leading=17, spaceAfter=4)
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=9, leading=11.5, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.6 * inch, footer)
        canvas.drawRightString(LETTER[0] - 1.0 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                          bottomMargin=0.95 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def write_regulation(path):
    doc, frame = _doc(path, W.REGULATION, "Office of the Legislative Counsel",
                      "%s  |  Consolidated to 1 July 2026" % W.REGULATION)
    s = [Paragraph(W.REGULATION.upper(), H1),
         Paragraph("made under the Labour Market Adjustment Act. Consolidated to 1 July 2026; this consolidation is "
                   "not an official version.", CAP)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    M = lambda n, t: s.append(Paragraph("(%s)&nbsp;&nbsp;%s" % (n, t), SUB))
    D = lambda t: s.append(Paragraph(t, DEF))
    s.append(Paragraph("Interpretation", H2))
    N("1", "(1) In this regulation,")
    D("<i>Agency</i> means the %s;" % W.AGENCY)
    D("<i>bureau</i> means the %s;" % W.BUREAU)
    D("<i>economic region</i> means a region set out in the Schedule, made up of the municipalities that the bureau's "
      "municipal concordance places in it;")
    D("<i>Minister</i> means the Minister of Labour and Economic Development;")
    D("<i>payroll jobs</i> of an economic region for a month means the jobs on the monthly returns that employers file "
      "with the Agency for the month at workplaces in the region's municipalities;")
    D("<i>quarter</i> means the three months beginning on 1 January, 1 April, 1 July or 1 October;")
    D("<i>workplace</i> means a place in the province at which an employer's employees work.")
    M("2", "An economic region's payroll jobs for a quarter are the average of its payroll jobs for the three months of "
           "the quarter, and its payroll jobs for a calendar year are the average of its payroll jobs for the twelve "
           "months of the year.")
    s.append(Paragraph("Designation", H2))
    N("2", "(1) An economic region is designated for a quarter if its seasonally adjusted payroll jobs for the quarter "
           "are more than 1.0 per cent below its payroll jobs for the preceding calendar year.")
    M("2", "The comparison in subsection (1) is made on unrounded figures.")
    s.append(Paragraph("Certification", H2))
    N("3", "(1) Within 45 days after the end of each quarter, the bureau shall certify to the Minister the economic "
           "regions designated for the quarter.")
    M("2", "The certification is made on the returns, and the revisions to them, that the Agency has supplied to the "
           "bureau by the date of certification.")
    M("3", "For each designated region the certification sets out its seasonally adjusted payroll jobs for the quarter "
           "and its payroll jobs for the preceding calendar year.")
    s.append(Paragraph("Response in designated regions", H2))
    N("4", "(1) For an economic region designated for a quarter, the Minister may fund, for the two quarters that "
           "follow the certification,")
    M("a", "workforce adjustment services for workers whose jobs at the region's workplaces have ended or been cut; and")
    M("b", "outreach to the employers with workplaces in the region.")
    M("2", "Funding under subsection (1) is set by the Minister and is not limited by the bureau's certification.")
    s.append(Paragraph("Schedule: Economic regions", H2))
    rows = [[Paragraph("Code", CELLB), Paragraph("Economic region", CELLB)]] + \
        [[Paragraph(c, CELL), Paragraph(n, CELL)] for c, n, *_ in W.REGIONS]
    t = Table(rows, colWidths=[0.9 * inch, 2.6 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaed")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_release_note(path):
    nm, title = W.PEOPLE["liaison"]
    doc, frame = _doc(path, "Payroll jobs by place of work", W.AGENCY,
                      "%s  |  Employer return statistics  |  Release note, 16 February 2026" % W.AGENCY)
    s = [Paragraph(W.AGENCY.upper(), SMALL), Spacer(1, 4),
         Paragraph("Employer return statistics: payroll jobs by place of work from the January 2026 reference month", SANSB),
         Paragraph("Release note, 16 February 2026", SMALL), Spacer(1, 10)]
    P = lambda t: s.append(Paragraph(t, SANS))
    P("From the January 2026 reference month, the monthly employer return carries a workplace schedule. Employers "
      "report the payroll jobs at each of their workplaces in the province, with the workplace's address and activity.")
    P("The Agency's statistics now place payroll jobs in the municipality of the workplace. For reference months to "
      "December 2025, the statistics placed all of an employer's payroll jobs in the municipality of its account address. "
      "For most employers the two are the same place. For employers with workplaces in more than one municipality, the "
      "account address is usually the head office.")
    P("The change moves payroll jobs between municipalities and between economic regions. It does not change the "
      "province's total.")
    P("Statistics for reference months before January 2026 have not been revised. The Agency does not hold workplace "
      "information for those months.")
    s.append(Spacer(1, 8))
    P("%s<br/>%s<br/>%s" % (nm, title, W.AGENCY))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
