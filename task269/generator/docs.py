"""The pack's documents: the School's assessment policy (version 7), the 2027 final OSCE delivery plan, the board of
examiners' minutes of 14 May 2026, the case bank's migration report, the 2026 candidate feedback summary and the
pack's contents list."""
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
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1c2428"), colors.HexColor("#5a646b"), colors.HexColor("#b4bdc3")
GREEN = colors.HexColor("#1f5a44")
SLATE = colors.HexColor("#2f4a63")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=10, leading=13.8, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.8, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.6, leading=11.6, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.4, leading=10.6, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.4, leading=10.6, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.6)
        canvas.drawString(19 * mm, A4[1] - 11.5 * mm, left)
        canvas.drawRightString(A4[0] - 19 * mm, A4[1] - 11.5 * mm, right)
        canvas.drawRightString(A4[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
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
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _long(d):
    return d.strftime("%d %B %Y").lstrip("0")


# ---------------------------------------------------------------------------------------------- the policy
def write_policy(path):
    S = styles("Serif", GREEN)
    P = lambda t: Paragraph(t, S["body"])
    C = lambda n, t: KeepTogether([Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), S["clause"])])
    H = lambda t: Paragraph(t, S["h2"])
    st = [Paragraph("Assessment policy", S["h1"]),
          Paragraph("%s. Version 7, approved by the Faculty Board on 23 September 2026; in force from the 2026-27 "
                    "session. Owner: Head of Assessment." % K.SCHOOL, S["meta"]),
          H("1. Scope"),
          C("1.1", "This policy governs the assessments of the medical degree (MB BCh BAO) and of the graduate-entry "
                   "medicine programme taught at %s. Where it refers to the final OSCE it means the final "
                   "objective structured clinical examination both programmes' final-year students sit." % K.FENNABEG),
          H("2. Principles"),
          C("2.1", "An assessment measures what the programme's outcomes say a graduate can do, in the setting a "
                   "graduate will do it."),
          C("2.2", "Every candidate sits the same assessment under the same conditions, and every decision about a "
                   "candidate rests on marks the board of examiners has confirmed."),
          H("3. Clinical examinations"),
          C("3.1", "An OSCE is a circuit of stations. At each station a candidate has eight minutes with a simulated "
                   "patient, a manikin or a task, and two minutes to move on. Each station has a checklist and a "
                   "global grade."),
          C("3.2", "Each checklist item is marked 0 (not done), 1 (partly done) or 2 (done well), or not applicable "
                   "where the item depends on a cue the simulated patient gives and the cue was not given. A "
                   "station's mark is the points the candidate scored over the points its available items carry, an "
                   "item marked not applicable not being available, expressed out of 20. A candidate's total mark is "
                   "the sum of their station marks."),
          C("3.3", "Each station is marked by the examiner or examiners the examinations office allocates. Where two "
                   "examiners mark a candidate at a station, each marks independently and the candidate's station "
                   "mark is the mean of their two marks."),
          C("3.4", "The board of examiners may withdraw a checklist item it finds unsound. The item is then removed "
                   "from every candidate's mark and the station is marked out of its remaining items."),
          C("3.5", "Each station's pass mark is set after the examination by borderline regression on its examiners' "
                   "marks and global grades."),
          H("4. The final OSCE"),
          C("4.1", "The final OSCE's total mark decides whether a candidate passes the clinical component of the "
                   "final examination and places the candidates who pass in their order of merit, which the "
                   "national intern matching uses."),
          C("4.2", "Its stations are drawn each year from the School's case bank, the same number from each of the "
                   "four blueprint domains: history taking, physical examination, communication and procedural "
                   "skills. Where the number of stations is not a multiple of four, the remaining stations are drawn "
                   "from the domains in that order."),
          C("4.3", "The final OSCE's total mark must rank candidates with a reliability of at least 0.80: the share of "
                   "the variance among candidates' total marks that reflects differences in their clinical "
                   "performance, the stations being drawn from the case bank each year and the examiners from the "
                   "faculty's examiner register."),
          C("4.4", "A case may be set at the final OSCE only if (a) its status in the case bank is Active (an Active "
                   "case with edits pending may be set as it stands); (b) the OSCE assessment group has reviewed it "
                   "in the three years before the sitting; and (c) it was not set at a final OSCE sitting, main or "
                   "supplemental, in either of the two previous years. A case keeps its sittings when its record is "
                   "revised."),
          H("5. Examiners"),
          C("5.1", "The examinations office keeps the faculty's examiner register: every clinician who has completed "
                   "the School's examiner training, with their grade, base and training dates."),
          C("5.2", "The examinations office allocates the final OSCE's examiners in December from the examiners "
                   "eligible at allocation: those active on the register, at lecturer, senior lecturer, associate "
                   "professor, professor or consultant grade or a GP trainer, who have completed the examiner "
                   "training or an examiner refresher in the three years before the allocation."),
          C("5.3", "An allocated examiner examines at one site, for the sessions they offered."),
          C("5.4", "Examiners attend the briefing at the start of their session and mark each candidate on the "
                   "station's checklist and global grade without conferring."),
          H("6. Review"),
          C("6.1", "The Head of Assessment reviews this policy each year and brings changes to the Faculty Board.")]
    doc = _doc(path, "Assessment policy, version 7", K.SCHOOL)
    fr = _frame(K.SCHOOL, "Assessment policy v7", "Serif")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- the minutes
def write_minutes(path, n_pass, n_fail):
    S = styles("Sans", SLATE)
    P = lambda t: Paragraph(t, S["body"])
    H = lambda t: Paragraph(t, S["h2"])
    st = [Paragraph("Board of examiners: final OSCE", S["h1"]),
          Paragraph("Minutes of the meeting of 14 May 2026, Clinical Skills Centre. Chair: Meghan Daniel (Head of "
                    "Assessment). Present: Cillian Garland (Director of Clinical Skills), the twelve lead examiners, "
                    "the examinations officer.", S["meta"]),
          H("1. Conduct of the examination"),
          P("The final OSCE ran on 12 and 13 May 2026 as one circuit of twelve stations at the Clinical Skills Centre: "
            "four rounds on the first day and three on the second, twelve candidates a round, 84 candidates in all. "
            "Each station had the same two examiners throughout both days, the lead examiner and a second examiner, "
            "each marking every candidate independently as policy 3.3 provides."),
          H("2. Station 7, item 14"),
          P("Examiners at station 7 (consent for a lumbar puncture) reported on the evening of day 1 that item 14 "
            "(\"states the risk of headache after the procedure in figures\") had been read two ways. The board "
            "withdraws the item under policy 3.4: it is removed from every candidate's mark and station 7 is marked "
            "out of its remaining fifteen items. The item was taken off the station 7 forms before day 2."),
          H("3. The examination system"),
          P("The OSCE system's scheduled update ran overnight between the two days as planned. The examinations "
            "officer confirmed that no marks were lost and that both days' marks are in the system's export."),
          H("4. Items not applicable"),
          P("At stations 1, 5 and 9 an item depends on a cue the simulated patient gives; where the cue was not "
            "given both examiners marked the item not applicable (policy 3.2)."),
          H("5. Results"),
          P("The board confirmed the station marks and the pass marks set by borderline regression. %d candidates "
            "passed the clinical component and %d did not; those who did not are offered the supplemental sitting "
            "in August. The order of merit goes to the registry with the written papers' marks." % (n_pass, n_fail)),
          H("6. 2027"),
          P("Fennabeg's first graduate-entry cohort sits the final OSCE in 2027. The Director of Clinical Skills will "
            "bring a delivery plan for three sites; the Head of Assessment will set the number of stations against "
            "policy 4.3, and the School will notify the %s of the 2027 blueprint as a material change to the final "
            "examination." % K.BOARD)]
    doc = _doc(path, "Board of examiners, final OSCE: minutes of 14 May 2026", "Examinations Office")
    fr = _frame(K.SCHOOL + ": Examinations Office", "Board of examiners, 14 May 2026", "Sans")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- migration report
def write_migration(path, b):
    S = styles("Sans", colors.HexColor("#3b3b6d"))
    P = lambda t: Paragraph(t, S["body"])
    H = lambda t: Paragraph(t, S["h2"])
    st = [Paragraph("OSCE case bank migration", S["h1"]),
          Paragraph("Cut-over report for the move of the School's OSCE case bank to the Assessment Item Bank, "
                    "14 November 2025. Prepared by the Assessment Technology team for the Examinations Office.",
                    S["meta"]),
          H("1. What moved"),
          P("The cut-over ran on 14 November 2025. Every case record in the old bank was carried across with its "
            "code, title, blueprint domain, specialty, resources, version, status and last review date. Review dates "
            "typed into the old bank came across as the text they were typed in; dates entered in the Assessment "
            "Item Bank are stored as dates. Cases written in the Assessment Item Bank take codes beginning CV- and "
            "the year."),
          H("2. Revisions in progress"),
          P("The Assessment Item Bank cannot carry a revision that is part-way through. A case whose revision was "
            "pending at the cut-over was re-created as a new record under a new code, and its old record was "
            "retired; the OSCE assessment group signs each of those revisions off on the new record. Cases the "
            "group had already decided to retire were retired at the cut-over."),
          H("3. After the cut-over"),
          P("The old bank was closed to edits on 7 November 2025 and switched off on 28 November 2025, once the "
            "Examinations Office had checked the carried-across records against it. Requests for changes to case "
            "records go to the Assessment Technology service desk.")]
    st[1] = Paragraph("Cut-over report for the move of the School's OSCE case bank to the Assessment Item Bank on "
                      "14 November 2025. Prepared by the Assessment Technology team for the Examinations Office, "
                      "2 December 2025.", S["meta"])
    doc = _doc(path, "OSCE case bank migration: cut-over report", "Assessment Technology")
    fr = _frame(K.UNIVERSITY + ": Assessment Technology", "Case bank migration, November 2025", "Sans")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- feedback (distractor)
def write_feedback(path, fb):
    S = styles("Sans", SLATE)
    P = lambda t: Paragraph(t, S["body"])
    rows = [["Station", "Case", "Responses", "Clear instructions (1 to 5)", "Realistic (1 to 5)", "Enough time (%)"]]
    rows += [[str(r[0]), r[1], str(r[2]), "%.1f" % r[3], "%.1f" % r[4], "%d" % r[5]] for r in fb]
    st = [Paragraph("Final OSCE 2026: what candidates told us", S["h1"]),
          Paragraph("Summary of the candidate survey after the May 2026 final OSCE. Student Experience Office, "
                    "June 2026.", S["meta"]),
          P("Candidates rated each station on a five-point scale for how clear its instructions were and how "
            "realistic it felt, and said whether eight minutes was enough. Responses came from candidates of both "
            "days."),
          _table(S, rows, [16, 62, 20, 30, 24, 22], right=(2, 3, 4, 5)),
          Spacer(1, 6),
          P("Candidates asked again for the room numbers to be shown on the circuit plan, and for water at the rest "
            "points.")]
    doc = _doc(path, "Final OSCE 2026: candidate feedback", "Student Experience Office")
    fr = _frame(K.SCHOOL, "Candidate feedback, final OSCE 2026", "Sans")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ---------------------------------------------------------------------------------------------- the delivery plan
def write_plan(path):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    stl = d.styles["Normal"]
    stl.font.name = "Calibri"
    stl.font.size = Pt(11)
    d.add_heading("Final OSCE 2027: delivery plan", level=1)
    d.add_paragraph("Cillian Garland, Director of Clinical Skills. Draft for the Head of Assessment, 12 November 2026.")
    d.add_heading("Dates and candidates", level=2)
    d.add_paragraph("The 2027 final OSCE runs on Tuesday 11 and Wednesday 12 May 2027. It is the first sitting with "
                    "Fennabeg Clinical School's graduate-entry students alongside Callowfield's final year, which "
                    "makes it about twice the size of 2026.")
    d.add_heading("Sites and circuits", level=2)
    d.add_paragraph("The examination runs at three sites at once, one circuit at each: the Clinical Skills Centre in "
                    "Callowfield, the Simulation Suite at Callowfield University Hospital, and the Clinical Skills "
                    "Unit at Fennabeg. Each site has eighteen rooms that can hold a station, so a circuit can have "
                    "up to eighteen stations. Every circuit runs the same stations, in the same order.")
    d.add_paragraph("Each day has a morning session (08:30 to 12:45) and an afternoon session (13:30 to 17:45). A "
                    "station takes eight minutes and the move two, so a round with n stations takes 10n minutes "
                    "and examines n candidates.")
    d.add_heading("Examining", level=2)
    d.add_paragraph("With three circuits running at once we cannot staff two examiners at every station as we did in "
                    "2026. Each station will have one examiner in each circuit. The examinations office allocates "
                    "examiners on Monday 7 December from the register (policy 5.2), each to one site and the sessions they "
                    "offered, and a station's examiner stays for the whole session; the afternoon session has its own "
                    "examiners.")
    d.add_paragraph("The availability form for 2027 went to every examiner on the register on 19 October and closes "
                    "on 27 November. Examiners who need to change what they told us submit the form again; their "
                    "latest response stands.")
    d.add_heading("Stations", level=2)
    d.add_paragraph("Stations are drawn from the case bank under policies 4.2 and 4.4, the same number from each "
                    "blueprint domain. The number of stations is for the Head of Assessment to set so that the "
                    "total mark meets policy 4.3, within the eighteen rooms. The bank draw and the examiner "
                    "allocation follow once the number is set.")
    d.add_heading("Simulated patients", level=2)
    d.add_paragraph("Simulated patients come from the agency we used in 2026, booked by the session; manikin and "
                    "task-trainer stations need none.")
    d.save(path)


def write_contents(path, rows):
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    lines = ["Final OSCE 2027 blueprint: working pack",
             "Assembled by the Examinations Office for the Head of Assessment, %s" % _long(K.PACK_DATE), ""]
    for i, r in enumerate(rows):
        lines.append("  ".join(str(c).ljust(widths[j]) for j, c in enumerate(r)).rstrip())
        if i == 0:
            lines.append("  ".join("-" * w for w in widths))
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
