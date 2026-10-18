"""The pack's documents: Board Policy 3.12 (Academic Program Review), the registrar's notes on the extracts for the
June 2027 review, and the export manifest."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle      # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2326"), colors.HexColor("#5b646b"), colors.HexColor("#b7bec4")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=7,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.4, leading=10.6, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.4, leading=10.6, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=24, firstLineIndent=-24))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(19 * mm, letter[1] - 11.5 * mm, left)
        canvas.drawRightString(letter[0] - 19 * mm, letter[1] - 11.5 * mm, right)
        canvas.drawRightString(letter[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
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
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


# ---------------------------------------------------------------------------------------------- the policy
def write_policy(path):
    S = styles("Serif", colors.HexColor("#22465f"))
    doc = _doc(path, "Board Policy 3.12: Academic Program Review", K.COLLEGE)
    st = [Paragraph("%s: Board Policy 3.12, Academic Program Review" % K.COLLEGE, S["h1"]),
          Paragraph("Adopted by the Board of Trustees 14 May 2019; revised 10 June 2025. Policy owner: %s, Vice "
                    "President for Academic Affairs. Replaces the program review procedure of 2014." % K.PEOPLE["vpaa"],
                    S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    st.append(Paragraph("1. Purpose", S["h2"]))
    P("The college reviews its associate-degree programs every year so that the Board of Trustees can see whether the "
      "students who start a program finish with a degree, and act when too few do.")
    st.append(Paragraph("2. Scope", S["h2"]))
    P("This policy applies to every associate-degree program (AA, AS and AAS) in the program register. Certificate "
      "programs are reviewed under Policy 3.14. High school dual enrollment and non-degree study are not programs under "
      "this policy.")
    st.append(Paragraph("3. Three-year completion", S["h2"]))
    C("3.1", "A program's three-year completion share is the share of its entering students who earn an associate "
             "degree from the college within three years of entering: by the end of the ninth term, counting the fall "
             "term of entry as the first and summer terms included. A degree in any of the college's associate-degree "
             "programs counts.")
    C("3.2", "A program's entering students are the students in the Office of Institutional Research's fall "
             "entering-student file whose program at entry is the program: degree-seeking students in their first "
             "term at the college, first-time in college or transferring in, as frozen at the fall census. Each "
             "student is followed under the admission recorded at entry and is reported in the program the student "
             "entered; a student who leaves and is later readmitted is not followed under the new admission, and a "
             "degree earned under it does not count for the class. Students who die are removed from the class.")
    C("3.3", "Each June the share is reported for the classes that entered in the second, third and fourth fall terms "
             "before the review, taken together, from the student record as it stands at the end of the spring term "
             "before the review. Students whose ninth term is still to come are counted in full: the share includes an "
             "estimate, made from that record, of how many of them will have earned the degree by the end of their ninth "
             "term. Shares are reported as percentages to one decimal place.")
    C("3.4", "A program whose three-year completion share is below 30 per cent enters review.")
    st.append(Paragraph("4. The review profile", S["h2"]))
    C("4.1", "Beside the completion share, the review profile reports each program's full-time-equivalent enrolment "
             "at the fall census: the credit hours registered at the census by the students whose program of record "
             "at the census is the program, divided by 15.")
    C("4.2", "The profile also reports the number of classes of the program's own courses (the course subjects the "
             "program register assigns to the program) that ran in the fall term with fewer than ten students "
             "registered at the census. A class is a section, or two or more sections scheduled to meet together, "
             "which count as one class with their students added together; laboratory, shop and clinical sections are "
             "classes of their own.")
    C("4.3", "A student is registered at the census in a section when the registration was in place on the term's "
             "census date, whether or not the student later withdrew. The profile uses the fall term before the review.")
    st.append(Paragraph("5. Review and its outcomes", S["h2"]))
    P("A program in review submits an improvement plan to the Vice President for Academic Affairs by 1 October. The "
      "board receives a report on each program in review at its June meeting in each of the next two years and decides "
      "at the second whether to continue the program, continue it under a further plan, or begin its sunset. A program "
      "that recovers to 30 per cent or more leaves review at the next June meeting.")
    st.append(Paragraph("6. Responsibilities", S["h2"]))
    P("The Office of Institutional Research prepares the review from the registrar's extracts and its own "
      "entering-student files and presents it to the board each June. The registrar maintains the student record and "
      "documents each extract. Program coordinators receive their program's figures before the board meeting.")
    doc.build(st, onFirstPage=_frame("Board Policy 3.12", K.COLLEGE, "Serif"),
              onLaterPages=_frame("Board Policy 3.12", K.COLLEGE, "Serif"))


# ---------------------------------------------------------------------------------------------- the registrar's notes
def write_notes(path):
    S = styles("Sans", colors.HexColor("#3b4f2a"))
    F = K.FILES
    doc = _doc(path, "Registrar's extracts for program review, May 2027", "Office of the Registrar")
    st = [Paragraph("Registrar's extracts for program review, June 2027", S["h1"]),
          Paragraph("Office of the Registrar, %s. Prepared by %s, Registrar, 28 May 2027, for the Office of "
                    "Institutional Research. Extracts taken 28 May 2027, after spring 2027 grades and the May "
                    "conferral." % (K.COLLEGE, K.PEOPLE["registrar"]), S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    st.append(Paragraph("1. Student systems and term codes", S["h2"]))
    P("The college moved from its legacy student system to the current one over the summer of 2024; fall 2024 was the "
      "first term run in the current system. Student records were converted with new student numbers (A0 and seven "
      "digits), and %s lists each converted student's legacy number and current number. Current term codes are the "
      "academic year in which the term ends followed by 10 for fall, 20 for spring and 30 for summer, so fall 2023 is "
      "202410 and spring 2027 is 202720; legacy codes were the calendar year and FA, SP or SU. %s gives every term's "
      "codes and dates." % (F["idmap"], F["terms"]))
    st.append(Paragraph("2. Admissions and exits", S["h2"]))
    P("%s has one row for each admission with an admit term from fall 2023 (202410) to spring 2027 (202720), converted "
      "admissions included. Admit types: N new to the college, T transferring in, R readmitted, S admitted to a second "
      "program after a degree, D high school dual enrollment, V visiting or non-degree. program_code is the program "
      "admitted to; later changes of program are in the program-of-record history." % F["admissions"])
    P("An admission closes in the exit term with one of four exit reasons. GR: graduated, the award of the student's "
      "program conferred at the end of the exit term. TO: transferred out, the student was not enrolled in the exit "
      "term and the %s match shows the student enrolled at another institution in that term. WD: withdrawn, the "
      "student was not enrolled in the exit term and had neither graduated nor transferred out. DC: deceased." % K.EXCHANGE)
    P("The registrar closes an admission at the census of the first fall or spring term in which the student is not "
      "enrolled; not enrolling in a summer term does not close an admission. Its reason is WD until the exchange's "
      "quarterly match shows the student enrolled at another institution in that term, when it becomes TO; "
      "exit_recorded_on is the date the current reason was recorded. A student who returns after an admission has "
      "closed applies for readmission and is given a new admission. An admission with no exit term was open at the "
      "end of the spring 2027 term.")
    st.append(Paragraph("3. Associate degree conferrals", S["h2"]))
    P("%s lists every associate degree conferred from December 2023 to May 2027, one row per degree, with the program "
      "in which it was conferred, the conferral date and the term. Degrees are conferred at the end of the fall, spring "
      "and summer terms. Certificates are conferred separately and are not in the file." % F["conferrals"])
    st.append(Paragraph("4. Program-of-record history", S["h2"]))
    P("%s has one row for each period in which a program of record was in effect for a student at any time from fall "
      "2023 to spring 2027. effective_term is the first term of the period and end_term its last, blank while the "
      "period is open; change_reason is ADM admission, RDM readmission, SEC second program or CHG change of program; "
      "entered_on is the date the row was keyed." % F["history"])
    st.append(Paragraph("5. Fall 2026 registrations", S["h2"]))
    P("%s has every registration for fall 2026 (202710), one row per student and section, as it stood when the file "
      "was extracted. reg_status: RE registered, RW registered on the web, WC withdrew from the course after the "
      "census (a W grade), DD dropped before the census, DW dropped on the web before the census; status_date is the "
      "date of that status. credit_hours is the course's credit hours and program_code the student's program of "
      "record." % F["registrations"])
    st.append(Paragraph("6. Fall 2026 section schedule", S["h2"]))
    P("%s has one row per fall 2026 section, exported 28 May 2027. Type is LEC lecture, LAB laboratory, SHP shop or "
      "CLN clinical; Link is the lecture a laboratory, shop or clinical section belongs to. Camp is QNL, TRV, HOL or "
      "ONL for online sections, which have no meeting days or times (TBA) and room ONLINE. Clinical groups meet at "
      "clinical agencies (room OFF CAMPUS). Rooms ending in V are interactive video classrooms. Start Date and End "
      "Date are the section's first and last class days. Cr Hrs is the section's credit hours, Max its enrolment "
      "limit and Enrl the students registered in it when the schedule was exported. Status A is active and X "
      "cancelled before the census." % F["schedule"])
    st.append(Paragraph("7. Program register", S["h2"]))
    P("%s lists each program's current and legacy codes, award, CIP code and campuses. Its Subjects sheet gives the "
      "program that owns each course subject; general education subjects belong to no program." % F["register"])
    doc.build(st, onFirstPage=_frame("Office of the Registrar", "Extract notes, May 2027", "Sans"),
              onLaterPages=_frame("Office of the Registrar", "Extract notes, May 2027", "Sans"))


def write_manifest(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "contents", "prepared_by", "as_of", "size"])
        for r in rows:
            w.writerow(r)
