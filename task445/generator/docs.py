"""task445 architecture 3: the board's code of practice and the awarding minute (PDF), and the request (email)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP
import world as W

ORG = "Arafura Examinations Board"
DOMAIN = "arafura-exams.edu.au"
RESULTS = ("Christopher Turner", "c.turner")
STANDARDS = ("Mary Deleon", "m.deleon")
DATA = ("Melissa Chen", "m.chen")


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=ORG, creator=ORG, producer=ORG, subject=subject, invariant=1)


def code_of_practice(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Code of practice for examining and awarding, 2026", "Code of practice")
    s = [Paragraph(ORG, small), Paragraph("Code of practice for examining and awarding", h1),
         Paragraph("2026 edition, approved by the Board on 18 March 2026 and in force for the 2026 Arafura Senior "
                   "Certificate examinations. Owner: the Head of Research and Standards.", small), Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "This code governs how the board marks its written papers, how optional questions are treated, how "
            "grades are awarded and how the board handles centres' requests for post-results reviews. It applies to "
            "every component of the Arafura Senior Certificate."]),
        ("2. Entries and centres", [
            "2.1 A candidate's centre for a paper is the centre that entered the candidate for it. A centre's "
            "region is the region the centres register gives it, under its current code or under the code it held "
            "before a merger.",
            "2.2 A candidate who is re-entered at another centre after entry keeps one entry and one result, under "
            "the number and the centre of the later entry; the earlier entry is withdrawn.",
            "2.3 A candidate present for a paper has sat it, whatever the candidate wrote; a candidate who was "
            "absent has not."]),
        ("3. Marking and crediting", [
            "3.1 Every answer a candidate writes is marked. Where a senior examiner re-marks an answer, the senior "
            "examiner's mark stands.",
            "3.2 Where a candidate answers more optional questions than the paper's instructions ask for, every answer is "
            "marked and the candidate is credited with the best answers the instructions allow."]),
        ("4. Optional questions", [
            "4.1 Optional questions on a paper are set to be equally demanding. After marking, Research and Standards "
            "reports to the executive on each optional question of every paper that offers a choice, before the "
            "paper's results are certified.",
            "4.2 An optional question is more demanding than the paper's other optional questions when the paper's "
            "candidates would have earned fewer marks on it than on the others taken together. The difference is "
            "measured in marks.",
            "4.3 Where an optional question is more demanding by a mark and a half or more, every candidate's mark on "
            "it is raised by that difference, to the nearest whole mark and no higher than the question's maximum, "
            "before the best answers are credited under 3.2 and before the grade boundaries are applied. No optional "
            "question's marks are lowered."]),
        ("5. Grades", [
            "5.1 A candidate's paper total is the candidate's Section A total and the marks of the credited answers; "
            "a candidate who wrote no essay is credited with none.",
            "5.2 A candidate's grade for the paper is the highest grade whose boundary the paper total reaches. A "
            "total below the boundary for grade E is ungraded (U). The boundaries are those the Awarding Committee "
            "sets for the paper; they are not moved after an optional question is scaled."]),
        ("6. Post-results reviews", [
            "6.1 After results are issued a centre may request a review of any component of a candidate's result. "
            "One request may cover several components; each component is reviewed and reported separately.",
            "6.2 A request is counted in the month in which the centre made it, in the centre's local time. A request "
            "the centre withdraws before its review begins is not counted.",
            "6.3 A review changes a grade when its outcome changes the component's grade."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Paragraph("7. Outcome codes in the review log", h2))
    t = Table([[Paragraph(x, cell) for x in r] for r in [
        ["Code", "Meaning"], ["NC", "Reviewed, no change to the mark"], ["MC", "Mark changed, grade unchanged"],
        ["GC", "Mark changed and grade changed"], ["WD", "Withdrawn by the centre before the review began"]]],
        colWidths=[22 * mm, 148 * mm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    s.append(t)
    s.append(Spacer(1, 6))
    s.append(Paragraph("Approved by the Board, 18 March 2026.", small))
    doc.build(s, onFirstPage=_footer("Code of practice 2026  |  " + ORG),
              onLaterPages=_footer("Code of practice 2026  |  " + ORG))
    PP.normalize_pdf(path, b"D:20260318041500+09'30'", b"D:20260319233000+09'30'")


def awarding_minute(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "History Awarding Committee minute, 24 November 2026", "Minute")
    s = [Paragraph(ORG, small), Paragraph("History Awarding Committee", h1),
         Paragraph("Minute of the meeting held in Darwin on 24 November 2026.", small), Spacer(1, 4),
         Paragraph("1. Paper 1 boundaries", h2),
         Paragraph("The committee set the Paper 1 boundaries recorded in the Paper 1 minute.", body),
         Paragraph("2. Paper 2 boundaries", h2),
         Paragraph("The committee set the following boundaries for Paper 2, out of 90 marks (Section A 40, Section B "
                   "two essays of 25):", body)]
    t = Table([[Paragraph(x, cell) for x in r] for r in [["Grade"] + [g for g, _ in W.BOUNDS],
                                                          ["Boundary (marks)"] + [str(b) for _, b in W.BOUNDS]]],
              colWidths=[40 * mm] + [26 * mm] * len(W.BOUNDS))
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    s += [t, Spacer(1, 4),
          Paragraph("3. Optional questions", h2),
          Paragraph("Section B offered Questions 4, 5 and 6, of which candidates answer two. Research and Standards will "
                    "report on the optional questions under sections 4.1 to 4.3 of the code of practice before the "
                    "results are certified.", body),
          Paragraph("4. Next meeting", h2),
          Paragraph("The committee will meet again in March 2027 to review the 2026 examining year.", body)]
    doc.build(s, onFirstPage=_footer("History Awarding Committee  |  " + ORG),
              onLaterPages=_footer("History Awarding Committee  |  " + ORG))
    PP.normalize_pdf(path, b"D:20261124063000+09'30'", b"D:20261125010500+09'30'")


def _mail(who):
    return "%s <%s@%s>" % (who[0], who[1], DOMAIN)


def request(path):
    text = """From: %s
To: %s
Cc: %s
Date: Tue, 01 Dec 2026 09:18:40 +0930
Subject: History Paper 2: certification on 14 December
Message-ID: <20261201091840.2210.cturner@%s>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Hi Mary,

Marking of History Paper 2 closed on Friday, and the executive certifies the
History results to the admissions centres on Monday 14 December, so I need
your section 4 report on the paper's optional questions this week.

Melissa has put the marking export, the Section A scan, the entries register
and the centres register in the usual folder, with last year's review log for
the annual report. The executive will want the results file for the
certification run and the entries figures by region.

Thanks,
Chris

--
%s
Executive Officer, Results
%s
""" % (_mail(RESULTS), _mail(STANDARDS), _mail(DATA), DOMAIN, RESULTS[0], ORG)
    open(path, "w", encoding="utf-8").write(text)
