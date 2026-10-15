"""The pack's documents: Brackenmere's survey reporting standard and Kestrava's notes on the 2026 export."""
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
                       "approved by %s, Head of Employee Listening, on 17 November 2025. The calendar in section 5 "
                       "was updated on 2 September 2026." % (owner, head), META)]
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
            "3.2 Every respondent counts once, and results are not weighted.",
            "3.3 A does-not-apply answer is not scored.",
            "3.4 A respondent is reported under the site they were assigned to in the HR system on the day the "
            "survey opened, and a store under its district."]),
        ("4. Showing results", [
            "4.1 A group's results are shown only when it has 10 or more respondents.",
            "4.2 Comments are read by People Analytics and are never shown with a name or a site below district "
            "level."]),
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


def write_export_notes(path, names, counts):
    vendor = K.PEOPLE["vendor"]
    story = [Paragraph("Export notes", H1),
             Paragraph("Kestrava Listening for Brackenmere Markets: Engagement Survey 2026 (BRK-ENG-2026). Export run "
                       "on 19 October 2026 by %s, account manager. These notes describe the files of this export and "
                       "their columns." % vendor, META)]
    story.append(Paragraph("Files", H2))
    rows = [[Paragraph("File", CELLB), Paragraph("Rows", CELLB), Paragraph("Holds", CELLB)],
            [Paragraph(names["responses"], CELL), Paragraph("{:,}".format(counts["responses"]), CELL),
             Paragraph("one row per answer; three lines of export information precede the header", CELL)],
            [Paragraph(names["submissions"], CELL), Paragraph("{:,}".format(counts["submissions"]), CELL),
             Paragraph("one row per submission", CELL)],
            [Paragraph(names["invitations"], CELL), Paragraph("{:,}".format(counts["invitations"]), CELL),
             Paragraph("the distribution list as loaded", CELL)],
            [Paragraph(names["codebook"], CELL), Paragraph("", CELL),
             Paragraph("items, French codes and response codes", CELL)]]
    t = Table(rows, colWidths=[66 * mm, 18 * mm, 82 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story += [t, Spacer(1, 6)]
    blocks = [
        ("Answers", [
            "token: the token the answer was given under.",
            "submission: 1 for the first submission under a token, 2 for the next. A token can be submitted again "
            "while the survey is open; every submission is exported, and Kestrava reports the last submission under "
            "each token.",
            "item: Q01 to Q30 are the items in the order of the English questionnaire and F01 to F30 in the order of "
            "the French questionnaire; the codebook gives each French code's item. ENPS is the recommend question.",
            "answer: the response code (codebook, Response codes). An item left blank has no row.",
            "answered_at: the time Kestrava recorded the answer, in UTC."]),
        ("Submissions", [
            "channel: web (a personal link sent by email or text message), kiosk (a session at a site's kiosk; the "
            "kiosk opens a new token for each session) or paper (a printed form returned by the store).",
            "language: the questionnaire the submission was answered in.",
            "status: submitted; saved (the answers given are kept, the submission was not completed); test (Kestrava's "
            "pre-launch tests of 11 and 12 September, not respondents).",
            "first_answered_at and last_answered_at: the first and last answered_at in the submission, in UTC.",
            "items_answered: how many of the 30 items the submission holds an answer to (the recommend question is "
            "not counted)."]),
        ("Distribution list", [
            "The list Kestrava loaded on 2 September 2026 from Brackenmere's HR extract of 31 August 2026: the token "
            "issued to each employee invited by email, by text message or by printed form, with the employee's site "
            "and language as they stood in the extract. Employees at a site with a kiosk who had no email address or "
            "mobile number on file were invited to use the kiosk and have no row.",
            "Kiosk sessions are signed in with the employee number; Brackenmere IT keeps the kiosk app's session "
            "log."]),
        ("Collection", [
            "Personal links opened at 06:00 local time on 14 September 2026 and stopped accepting answers at 06:00 UTC "
            "on 28 September 2026, a setting Kestrava uses for every client.",
            "Reminders went by email and text message on 21 and 25 September."]),
    ]
    for h, paras in blocks:
        story.append(Paragraph(h, H2))
        for t in paras:
            story.append(Paragraph(t, CL))
    story.append(Paragraph("Kestrava Listening, client services. This export is confidential to Brackenmere Markets.",
                           NOTE))
    doc = _doc(path, "Export notes: Engagement Survey 2026", vendor)
    f = _frame("Kestrava Listening", "BRK-ENG-2026 export notes")
    doc.build(story, onFirstPage=f, onLaterPages=f)
