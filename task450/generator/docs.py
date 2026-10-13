"""The pack's documents: the 2025 technical report excerpt (the 2025 form, its scoring and its conversion to the
reporting scale), the board's campus designation rules for the 2027 improvement plan, and the assessment office's
key correction notice."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import LETTER                                 # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import inch                                       # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

REPORT = "dma_technical_report_2025_excerpt.pdf"
RULES = "campus_designation_rules_2026-27.pdf"
NOTICE = "dma_key_correction_2026-05-19.pdf"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1c1c")
GREY = colors.HexColor("#5c5c5c")
NAVY = colors.HexColor("#1f3a5f")
MAROON = colors.HexColor("#6b1f2a")

BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.6, leading=14.4, textColor=INK, spaceAfter=5)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=28, firstLineIndent=-28)
H1 = ParagraphStyle("h1", fontName="LiberationSerif-Bold", fontSize=15, leading=18.5, textColor=MAROON, spaceAfter=3)
SUB = ParagraphStyle("sub", fontName="LiberationSerif-Italic", fontSize=10, leading=13, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="LiberationSerif-Bold", fontSize=11.4, leading=15, textColor=MAROON, spaceBefore=8,
                    spaceAfter=3)
T_BODY = ParagraphStyle("tbody", fontName="LiberationSans", fontSize=9.4, leading=12.6, textColor=INK, spaceAfter=4.5)
T_H1 = ParagraphStyle("th1", fontName="LiberationSans-Bold", fontSize=14, leading=17, textColor=NAVY, spaceAfter=2)
T_SUB = ParagraphStyle("tsub", fontName="LiberationSans", fontSize=9.4, leading=12, textColor=GREY, spaceAfter=9)
T_H2 = ParagraphStyle("th2", fontName="LiberationSans-Bold", fontSize=10.6, leading=13.5, textColor=NAVY,
                      spaceBefore=9, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")


def _frame(title):
    def f(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.58 * inch, "%s  |  %s" % (W.DISTRICT, title))
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.58 * inch, "%d" % doc.page)
        canvas.restoreState()
    return f


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                             topMargin=0.85 * inch, bottomMargin=0.95 * inch, title=title, author=W.OFFICE,
                             subject="", creator="", producer="")


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.8, INK),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4)]))
    return t


def write_report(path, strands):
    """strands: [(strand, items on the 2025 form)]."""
    title = "District Mathematics Assessment, Spring 2025: Technical Report (excerpt)"
    doc = _doc(path, title)
    s = [Paragraph("District Mathematics Assessment, Spring 2025", T_H1),
         Paragraph("Technical report, grade 5 mathematics: sections 2 to 4 and Table 4. %s, September 2025."
                   % W.OFFICE, T_SUB)]
    s.append(Paragraph("2. The 2025 grade-5 form", T_H2))
    s.append(Paragraph("The 2025 grade-5 form (%s) has 50 multiple-choice items in two sessions of 25, written to the "
                       "grade-5 mathematics TEKS. The items by strand:" % W.FORM25, T_BODY))
    s.append(_table([["Strand", "Items"]] + [[a, b] for a, b in strands] + [["Total", sum(b for _, b in strands)]],
                    [3.2 * inch, 0.8 * inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("The form was given online from 21 April to 2 May 2025 to every grade-5 student enrolled at an "
                       "elementary campus, apart from students assessed on the state's alternate assessment.", T_BODY))
    s.append(Paragraph("3. Scoring", T_H2))
    s.append(Paragraph("Each item is worth one point. An answer left blank, whether omitted or not reached, and an "
                       "answer with more than one choice marked score zero. A student's raw score is the number of "
                       "points, from 0 to 50.", T_BODY))
    s.append(Paragraph("4. The reporting scale and the proficiency standard", T_H2))
    s.append(Paragraph("4.1 The reporting scale was set on the 2025 grade-5 form. On that form a raw score converts to "
                       "a scale score as 141 + 6 x raw score, reported as a whole number (Table 4). The district chose a "
                       "linear scale so that the standard sits at 300 and each raw point on the 2025 form is worth six "
                       "scale points. The conversion applies to raw scores on the 2025 form only.", T_BODY))
    s.append(Paragraph("4.2 The proficiency standard, recommended by the standard-setting panel that met from 9 to 11 "
                       "June 2025 and adopted by the board of trustees on 23 June 2025, is a scale score of 300. On the "
                       "2025 form it lies at a raw score of 26.5.", T_BODY))
    s.append(Paragraph("Table 4. Raw score to scale score, 2025 grade-5 form", T_H2))
    rows = [["Raw", "Scale", "Raw", "Scale", "Raw", "Scale"]]
    col = [[r, 141 + 6 * r] for r in range(0, 51)]
    for i in range(17):
        row = []
        for j in range(3):
            k = i + 17 * j
            row += col[k] if k < len(col) else ["", ""]
        rows.append(row)
    s.append(_table(rows, [0.55 * inch, 0.65 * inch] * 3))
    doc.build(s, onFirstPage=_frame("Technical report, spring 2025"), onLaterPages=_frame("Technical report, spring 2025"))


def write_rules(path):
    title = "Campus designation rules for the 2027 District Improvement Plan"
    doc = _doc(path, title)
    s = [Paragraph("Campus designation rules for the 2027 District Improvement Plan", H1),
         Paragraph("Approved by the Board of Trustees on 18 August 2026. %s, %s." % (W.PEOPLE["board"][0],
                                                                                     W.PEOPLE["board"][1]), SUB)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    N("1", "Purpose. The 2027 District Improvement Plan names the elementary campuses that receive mathematics "
           "intervention coaching in 2027, from the results of the spring 2026 grade-5 District Mathematics "
           "Assessment.")
    N("2", "Standard. A student meets the mathematics standard when the student's scale score on the District "
           "Mathematics Assessment's reporting scale, which the district set on its 2025 grade-5 form, is 300 or "
           "above. Results from later forms are reported on the same scale.")
    N("3", "Full academic year. A student is full academic year at a campus when the student was enrolled at the "
           "campus on the fall snapshot date, 31 October 2025, and on every day after it through the first day of the "
           "testing window, 20 April 2026, and was enrolled at no other campus in that time.")
    N("4", "Rate. A campus's rate is the number of its full-academic-year students who tested and met the standard, "
           "divided by the number of its full-academic-year students who tested.")
    N("5", "Campuses. Campuses are rated as they are organised for the 2026-27 school year. The students of a campus "
           "that closed at the end of 2025-26 count with the campus that takes in its attendance zone.")
    N("6", "Rated campuses. A campus with fewer than ten full-academic-year students tested is not rated.")
    N("7", "Designation. A rated elementary campus whose rate is under 40 per cent is designated.")
    N("8", "Testing window. The spring 2026 administration ran from 20 April to 1 May 2026.")
    s.append(Spacer(1, 8))
    s.append(Paragraph("The superintendent's cabinet places the coaches at the designated campuses and reports the "
                       "placements to the board with the plan's 2027 amendment.", SUB))
    doc.build(s, onFirstPage=_frame("Campus designation rules, 2026-27"),
              onLaterPages=_frame("Campus designation rules, 2026-27"))


def write_notice(path, item_id, wrong, right):
    title = "Notice of key correction, spring 2026 grade-5 mathematics"
    doc = _doc(path, title)
    s = [Paragraph("Notice of key correction", T_H1),
         Paragraph("District Mathematics Assessment, grade 5 mathematics, spring 2026. %s, 19 May 2026." % W.OFFICE,
                   T_SUB)]
    s.append(Paragraph("Item %s, position %d on the 2026 grade-5 form (%s), was entered in the item bank with key %s. "
                       "The content review of 14 May 2026 found that the correct answer is %s. Score the item with key "
                       "%s for every 2026 test." % (item_id, 38, W.FORM26, wrong, right, right), T_BODY))
    s.append(Paragraph("The item bank's release of 6 April 2026 still shows the key as entered; the summer release "
                       "will carry the correction.", T_BODY))
    s.append(Spacer(1, 10))
    s.append(Paragraph("%s<br/>%s" % W.PEOPLE["director"], T_BODY))
    doc.build(s, onFirstPage=_frame("Key correction notice"), onLaterPages=_frame("Key correction notice"))
