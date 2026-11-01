"""The pack's documents: Brackenmere's survey reporting standard and Kestrava's fielding copy of the 2026
questionnaire."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY, RULE, GREEN = (colors.HexColor("#1f2421"), colors.HexColor("#5d6660"), colors.HexColor("#a9b2ac"),
                          colors.HexColor("#2f5d3a"))
BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
CL = ParagraphStyle("c", parent=BODY, leftIndent=24, firstLineIndent=-24)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=16, leading=20, textColor=GREEN, spaceAfter=2)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.4, leading=11, textColor=GREY, spaceAfter=10)
NOTE = ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10, textColor=GREY, spaceBefore=8)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.6, leading=11.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=22 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(22 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 12 * mm, right)
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def write_standard(path):
    owner, head = K.PEOPLE["analytics"], K.PEOPLE["head"]
    story = [Paragraph("Survey reporting standard", H1),
             Paragraph("Brackenmere Markets, People Analytics. Owner: %s, People Analytics Lead. Version 2025.1, "
                       "approved by %s, Head of Employee Listening, on 17 November 2025. Sections 3.4 and 4.3 and the "
                       "calendar in section 5 were updated on 2 September 2026." % (owner, head), META)]
    sections = [
        ("1. Scope", [
            "1.1 This standard governs how Brackenmere Markets reports its yearly engagement survey, including the "
            "engagement dashboard that store, distribution centre and head office managers use.",
            "1.2 The dashboard reports the yearly engagement survey only. The quarterly pulse survey asks its own "
            "five items and is reported separately.",
            "1.3 The questionnaire fielded in 2026 (30 items and the recommend question) is used unchanged in the "
            "2026 and 2027 surveys."]),
        ("2. Sub-scales", [
            "2.1 A sub-scale reports one distinct dimension of employees' views that the survey's items measure. The "
            "dashboard carries one sub-scale for each such dimension.",
            "2.2 Each item reports under exactly one sub-scale, the dimension it measures most.",
            "2.3 A team's score on a sub-scale is the share of its respondents' scored answers to the sub-scale's "
            "items that are favourable: agree or strongly agree with a statement, disagree or strongly disagree with "
            "a negatively worded statement, and yes to a yes or no question.",
            "2.4 The recommend question is reported on its own and belongs to no sub-scale.",
            "2.5 A team whose score on a sub-scale is below the company's prepares an action plan for that "
            "sub-scale within six weeks of the dashboard's release."]),
        ("3. Respondents", [
            "3.1 A respondent is an employee who answered at least one of the 30 items before the survey closed. "
            "The survey closes at 23:59 local time at the employee's site on the closing day.",
            "3.2 Every respondent counts once, and results are not weighted. Where a personal link was submitted "
            "more than once, its last submission counts.",
            "3.3 A does-not-apply answer is not scored.",
            "3.4 A respondent is reported under the site and the department they were assigned to in the HR system "
            "on the day the survey opened, and a store under its district."]),
        ("4. Showing results", [
            "4.1 A group's results are shown only when it has 10 or more respondents.",
            "4.2 Comments are read by People Analytics and are never shown with a name or a site below district "
            "level.",
            "4.3 A group's response rate is its respondents as a share of the employees assigned to it in the HR "
            "system on the day the survey opened."]),
        ("5. Calendar", [
            "5.1 The 2026 survey opens on 14 September 2026 and closes on 27 September 2026.",
            "5.2 The 2027 survey is planned for September 2027."]),
    ]
    for h, paras in sections:
        story.append(Paragraph(h, H2))
        for t in paras:
            story.append(Paragraph(t, CL))
    story.append(Paragraph("Questions about this standard go to People Analytics.", NOTE))
    doc = _doc(path, "Survey reporting standard", owner)
    f = _frame("Brackenmere Markets  |  People Analytics", "Survey reporting standard, version 2025.1")
    doc.build(story, onFirstPage=f, onLaterPages=f)


def write_questionnaire(path, S):
    """The questionnaire as fielded: Kestrava's fielding copy of BRK-ENG-2026, both language versions, each question
    with the number it carries in its version and the Kestrava library item it was built from, and the answer options
    with the codes Kestrava records."""
    vendor, head = K.PEOPLE["vendor"], K.PEOPLE["head"]
    items = {it["key"]: it for it in S["items"]}
    story = [Paragraph("Engagement Survey 2026: questionnaire", H1),
             Paragraph("Brackenmere Markets, BRK-ENG-2026, fielded by Kestrava Listening from 14 to 27 September 2026 "
                       "by personal link, store kiosk and printed form, in English and French. Fielding copy approved "
                       "by %s, Head of Employee Listening, and %s, Kestrava Listening, on 2 September 2026." %
                       (head, vendor), META)]
    story.append(Paragraph("Answer options", H2))
    opts = [[Paragraph("Question type", CELLB), Paragraph("Options (code)", CELLB)],
            [Paragraph("Statement", CELL), Paragraph("Strongly disagree (1), Disagree (2), Neither agree nor disagree "
                                                     "(3), Agree (4), Strongly agree (5), Does not apply to me (6)", CELL)],
            [Paragraph("Yes or no", CELL), Paragraph("Yes (1), No (2), Does not apply to me (6)", CELL)],
            [Paragraph("Recommend", CELL), Paragraph("0 (not at all likely) to 10 (extremely likely)", CELL)]]
    t = Table(opts, colWidths=[30 * mm, 136 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story += [t, Paragraph("A question may be left blank. The French version shows the same questions in its own "
                           "order.", NOTE)]
    story.append(Paragraph("Questions", H2))
    head_row = [Paragraph(x, CELLB) for x in ("EN no.", "FR no.", "Library", "Type", "Question (English / French)")]
    body = [head_row]
    for key in K.EN_ORDER:
        it = items[key]
        body.append([Paragraph(it["en_code"], CELL), Paragraph(it["fr_code"], CELL), Paragraph(it["library"], CELL),
                     Paragraph("Statement" if it["kind"] == "a5" else "Yes or no", CELL),
                     Paragraph("%s<br/><font color='#5d6660'>%s</font>" % (it["en"], it["fr"]), CELL)])
    body.append([Paragraph("ENPS", CELL), Paragraph("ENPS", CELL), Paragraph("KL-0001", CELL),
                 Paragraph("Recommend", CELL),
                 Paragraph("%s<br/><font color='#5d6660'>%s</font>" % (K.ENPS_EN, K.ENPS_FR), CELL)])
    t = Table(body, colWidths=[15 * mm, 15 * mm, 18 * mm, 23 * mm, 95 * mm], hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(t)
    story.append(Paragraph("Kestrava Listening, client services. Fielding copy for Brackenmere Markets.", NOTE))
    doc = _doc(path, "Engagement Survey 2026: questionnaire", vendor)
    f = _frame("Kestrava Listening  |  Brackenmere Markets", "BRK-ENG-2026 questionnaire")
    doc.build(story, onFirstPage=f, onLaterPages=f)
