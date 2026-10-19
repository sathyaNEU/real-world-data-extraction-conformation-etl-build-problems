"""The pack's documents: the Civil Service Commission's rules for the police officer entry examination (2023 edition),
the validation trial plan, the academy's recruit handbook, the 2022 job analysis and the working pack's contents."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2226"), colors.HexColor("#5b6268"), colors.HexColor("#b9c0c5")
NAVY = colors.HexColor("#1f3554")
GREEN = colors.HexColor("#2c5a3f")
BROWN = colors.HexColor("#5a4128")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=10, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14.5, leading=18.5, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.6, leading=11.6, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.4, leading=10.6, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.4, leading=10.6, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.6)
        canvas.drawString(0.8 * inch, letter[1] - 0.48 * inch, left)
        canvas.drawRightString(letter[0] - 0.8 * inch, letter[1] - 0.48 * inch, right)
        canvas.drawRightString(letter[0] - 0.8 * inch, 0.42 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                             topMargin=0.85 * inch, bottomMargin=0.7 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ---------------------------------------------------------------------------------------------- the rules
def write_rules(path):
    S = styles("Serif", NAVY)
    doc = _doc(path, "Rules for the Entry Examination for Police Officer", K.PEOPLE["secretary"])
    s = [Paragraph("Rules for the Entry Examination for Police Officer", S["h1"]),
         Paragraph("%s. 2023 edition, adopted by the Commission on 14 November 2023 and effective with the spring 2024 "
                   "examination. Replaces the 2019 edition." % K.COMMISSION, S["meta"]),
         Paragraph("Rule 1. Scope", S["h2"]),
         Paragraph("These rules govern original appointment to the classification of Police Officer in the %s. An "
                   "examination is held each spring and each autumn; each produces an eligibility list for the "
                   "academy classes named in its announcement." % K.DIVISION, S["body"]),
         Paragraph("Rule 2. Applications", S["h2"]),
         _clause(S, "2.1", "The Commission announces each examination with its application period, its test dates and "
                           "the academy classes its list is expected to fill. Applications are made through the "
                           "City's online application system and must be submitted by 11:59 p.m. Eastern time on the "
                           "closing date. A form started and not submitted is not an application."),
         _clause(S, "2.2", "An applicant must be 21 years of age by the start of the academy class, hold a high school "
                           "diploma or equivalent and a valid driver's license, and meet the Ohio Peace Officer "
                           "Training Commission's standards for admission to a basic training academy."),
         _clause(S, "2.3", "Officers employed full time by an Ohio law enforcement agency may apply for lateral entry "
                           "under Rule 8. A lateral entry application is not an application for this examination."),
         Paragraph("Rule 3. The components", S["h2"]),
         _clause(S, "3.1", "<i>Written test.</i> Halvorsen Selection Systems' Police Officer Entry Test, given in two "
                           "equated forms. A candidate's written test score is the scaled score (0 to 100) Halvorsen "
                           "reports, which places both forms on one scale."),
         _clause(S, "3.2", "<i>Oral board.</i> A structured interview before a panel of three: two sworn officers of the "
                           "rank of sergeant or above and a community panelist appointed by the Commission. Each "
                           "member rates the candidate from 1 to 5 on six dimensions: oral communication, problem "
                           "solving, integrity, interpersonal skills, community orientation and composure. The oral "
                           "board score is the mean of the ratings given, multiplied by 20. A member who knows a "
                           "candidate personally stands down for that candidate, and the mean is taken over the "
                           "other members' ratings."),
         _clause(S, "3.3", "<i>Physical ability test.</i> The Division's obstacle course. A candidate who does not finish "
                           "the course in 240 seconds or less may run it a second time the same day, and the faster "
                           "time counts. A candidate passes with a time of 240 seconds or less. The course is also "
                           "scored in points: 100 points at 160 seconds or less, less 0.62 points for each second over "
                           "160, rounded to the nearest point and never below zero."),
         _clause(S, "3.4", "<i>Trial components.</i> In the 2024 and 2025 examinations candidates also take, online in "
                           "the two weeks after the written test, Pellwyn Assessment Partners' situational judgement "
                           "test and Halvorsen's work style inventory, under the validation trial plan approved with "
                           "these rules. Their scores are recorded and take no part in the final score or the list."),
         Paragraph("Rule 4. The final score", S["h2"]),
         Paragraph("A candidate who completes the oral board and passes the physical ability test receives a final "
                   "score: 60 per cent of the written test score and 40 per cent of the oral board score, plus %d "
                   "points for an honorably discharged veteran who claims the credit with the application. Final "
                   "scores are carried to two decimals." % K.VETERAN_POINTS, S["body"]),
         Paragraph("Rule 5. The eligibility list", S["h2"]),
         _clause(S, "5.1", "Candidates with a final score are listed in order of final score, highest first. A tie is "
                           "broken by the higher written test score, and then by the earlier application."),
         _clause(S, "5.2", "The Commission certifies the list to the Chief of Police, who appoints from it in list order "
                           "to the academy classes named in the announcement. A candidate who does not pass the "
                           "background investigation, the psychological evaluation or the medical examination, or who "
                           "declines an offer, is passed over and the next candidate is offered the place."),
         _clause(S, "5.3", "A list expires when the next examination's list is certified. Candidates not reached by "
                           "then may apply to a later examination."),
         Paragraph("Rule 6. Changing the examination", S["h2"]),
         Paragraph("The Commission adds, removes or reweights a component only on evidence that the components it keeps "
                   "predict success in the %s for the candidates the examination ranks. The validation trial plan "
                   "sets out how that evidence is gathered for the 2027 examination." % K.ACADEMY, S["body"]),
         Paragraph("Rule 7. Records", S["h2"]),
         Paragraph("Halvorsen, Pellwyn, the panels and the course officers return scores to the Commission, which "
                   "keeps each candidate's record under the candidate number it assigns at registration for four "
                   "years. Halvorsen and Pellwyn use their own candidate identifiers; the Commission keeps the "
                   "crosswalk.", S["body"]),
         Paragraph("Rule 8. Lateral entry", S["h2"]),
         Paragraph("An officer employed full time by an Ohio law enforcement agency for two years or more may be "
                   "appointed on lateral entry after an oral board, a background investigation and the medical "
                   "examination. Lateral entry officers attend an abbreviated transition course, not the basic "
                   "academy.", S["body"]),
         Spacer(1, 8),
         Paragraph("%s, Executive Secretary. City Hall, Room 310." % K.PEOPLE["secretary"], S["meta"])]
    doc.build(s, onFirstPage=_frame(K.COMMISSION, "Police Officer entry examination rules, 2023", "Serif"),
              onLaterPages=_frame(K.COMMISSION, "Police Officer entry examination rules, 2023", "Serif"))


# ---------------------------------------------------------------------------------------------- the trial plan
def write_plan(path):
    S = styles("Sans", GREEN)
    doc = _doc(path, "Entry examination validation trial: plan", K.PEOPLE["analyst"])
    mins = [["Component", "Cost center", "Minutes a candidate"]]
    for c in K.COMPONENTS:
        mins.append([K.LABEL[c], K.CC_OF[c], K.MINUTES[c]])
    s = [Paragraph("Entry examination validation trial, 2024 and 2025: plan", S["h1"]),
         Paragraph("%s, Personnel Research. Prepared by %s, personnel research analyst; approved by the %s with the "
                   "2023 examination rules on 14 November 2023." % (K.DIVISION, K.PEOPLE["analyst"], K.COMMISSION),
                   S["meta"]),
         Paragraph("1. Purpose", S["h2"]),
         Paragraph("From 2027 the entry examination keeps two scored components. The trial gathers the evidence the "
                   "Commission needs under Rule 6 to choose them, and the cost and attendance record each component "
                   "carries.", S["body"]),
         Paragraph("2. The trial", S["h2"]),
         Paragraph("In the four examinations of spring and autumn 2024 and spring and autumn 2025 every candidate is "
                   "offered all five components: the written test, the oral board, the physical ability test, the "
                   "situational judgement test and the work style inventory. The lists are made and appointments are "
                   "made from them under the 2023 rules throughout the trial.", S["body"]),
         Paragraph("3. The candidate pool", S["h2"]),
         Paragraph("The evidence is judged for the people the examination ranks: every candidate who sat all five "
                   "components in the four examinations, whether or not they were appointed. A candidate who missed a "
                   "component is not in the pool.", S["body"]),
         Paragraph("4. The criterion", S["h2"]),
         Paragraph("A candidate's criterion is the final average the %s records at graduation, under the recruit "
                   "handbook. For a recruit who separates before graduating it is the average the academy recorded "
                   "at separation. Only candidates appointed to an academy class have a criterion." % K.ACADEMY,
                   S["body"]),
         Paragraph("5. The scores", S["h2"]),
         Paragraph("Written test: the scaled score. Oral board: the oral board score. Physical ability test: the points "
                   "for the faster run. Situational judgement test: Pellwyn's scaled score. Work style inventory: the "
                   "Dependability scale, a T score.", S["body"]),
         Paragraph("6. The decision", S["h2"]),
         Paragraph("A component's validity is the correlation between its score and the criterion across the candidate "
                   "pool. The 2027 examination keeps the two components with the highest validities, and the trial "
                   "report gives the order of all five.", S["body"]),
         Paragraph("7. Cost", S["h2"]),
         Paragraph("A component's cost per candidate is what its work in the four examinations cost the City, divided "
                   "by the candidates who sat it in those examinations. Each component's work is charged to its own "
                   "cost center: the vendors' invoices, the officers' overtime and the other charges for it. Running "
                   "each examination (proctors, notices) is charged to cost center 4410, and what that cost is "
                   "shared among the five components in proportion to the minutes each takes a candidate:", S["body"]),
         _table(S, mins, [2.6, 1.2, 1.5], right=(2,)),
         Spacer(1, 6),
         Paragraph("8. Attendance", S["h2"]),
         Paragraph("A component's completion rate is the share of the people who applied that sat it, the four "
                   "examinations taken together. A person who applied is one who submitted an application for the "
                   "entry examination by the closing date of its application period, counted once in each "
                   "examination however many applications they submitted. Lateral entry applicants are not counted.",
                   S["body"]),
         Paragraph("9. Report", S["h2"]),
         Paragraph("Personnel Research reports to the Commission once the last trial class has finished the academy, "
                   "in time for the 2027 examination's announcement.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.DIVISION + ", Personnel Research", "Validation trial plan", "Sans"),
              onLaterPages=_frame(K.DIVISION + ", Personnel Research", "Validation trial plan", "Sans"))


# ---------------------------------------------------------------------------------------------- the handbook
def write_handbook(path):
    S = styles("Serif", BROWN)
    doc = _doc(path, "Recruit Handbook 2024", K.ACADEMY)
    blocks = [["Block", "Weight", "Graded work", "Ends"],
              ["Firearms", "15%", "Qualification courses (handgun, patrol rifle), judgement range", "Week 8"],
              ["Defensive tactics", "15%", "Control and arrest techniques, scenario assessments", "Week 14"],
              ["Report writing", "15%", "Six graded reports, the field notes portfolio", "Week 18"],
              ["Physical conditioning", "15%", "Three fitness assessments, the final run", "Week 24"],
              ["Academics", "40%", "Twelve written examinations on law, procedure and patrol", "Week 26"]]
    s = [Paragraph("Recruit Handbook 2024", S["h1"]),
         Paragraph("%s, Basic Training Academy. Issued to recruits of classes 24-1 onward." % K.ACADEMY, S["meta"]),
         Paragraph("1. The academy", S["h2"]),
         Paragraph("The basic academy runs %d weeks and meets the Ohio Peace Officer Training Commission's basic "
                   "training curriculum. Recruits are full-time employees of the City from the first day of the "
                   "class." % K.ACADEMY_WEEKS, S["body"]),
         Paragraph("2. Grading", S["h2"]),
         Paragraph("Recruits are graded in five blocks:", S["body"]),
         _table(S, blocks, [1.5, 0.6, 3.4, 0.7], right=(1,)),
         Spacer(1, 6),
         Paragraph("A block score is the average of its graded work, to one decimal. The final average is the weighted "
                   "average of the five block scores, to one decimal. A recruit must score 70 or more in every block "
                   "to graduate, with one retest a block.", S["body"]),
         Paragraph("3. Separation", S["h2"]),
         Paragraph("A recruit who resigns, or is dismissed on academic or medical grounds, separates on the day the "
                   "Academy Commander signs the separation. The gradebook records the recruit's average of the graded "
                   "work completed to that day as the average at separation.", S["body"]),
         Paragraph("4. Conduct", S["h2"]),
         Paragraph("Recruits follow the Division's general orders and the academy's rules of conduct. A recruit's "
                   "class sergeant is the first point of contact for leave, illness and grade questions.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.ACADEMY, "Recruit Handbook 2024", "Serif"),
              onLaterPages=_frame(K.ACADEMY, "Recruit Handbook 2024", "Serif"))


# ---------------------------------------------------------------------------------------------- the job analysis
def write_job_analysis(path):
    S = styles("Sans", NAVY)
    doc = _doc(path, "Police Officer Job Analysis 2022", "Halvorsen Selection Systems")
    tasks = [["Rank", "Task statement", "Officers rating it critical"],
             ["1", "Writes incident and arrest reports that stand up in court", "92%"],
             ["2", "De-escalates disputes and persons in crisis", "90%"],
             ["3", "Decides whether there is probable cause to arrest", "88%"],
             ["4", "Drives a patrol vehicle in emergency response", "84%"],
             ["5", "Interviews victims, witnesses and suspects", "83%"],
             ["6", "Restrains a resisting person", "79%"],
             ["7", "Applies city ordinances and the Ohio Revised Code in the field", "77%"],
             ["8", "Pursues a fleeing person on foot", "71%"],
             ["9", "Testifies in court and at administrative hearings", "68%"],
             ["10", "Works with residents and businesses on neighborhood problems", "64%"]]
    ksa = [["Knowledge, skill or ability", "Assessed in 2022 by"],
           ["Reading comprehension; written expression", "Written test"],
           ["Reasoning and judgement under rules", "Written test, oral board"],
           ["Oral communication; interpersonal skill", "Oral board"],
           ["Integrity", "Oral board, background investigation"],
           ["Cardiovascular endurance; agility; strength", "Physical ability test"],
           ["Composure under stress", "Oral board"]]
    s = [Paragraph("Police Officer Job Analysis 2022", S["h1"]),
         Paragraph("Halvorsen Selection Systems for the %s, March 2022. Survey of 214 sworn officers and five subject "
                   "matter expert panels, October 2021 to January 2022." % K.COMMISSION, S["meta"]),
         Paragraph("1. Method", S["h2"]),
         Paragraph("Officers of every patrol district rated 168 task statements for frequency and criticality. Subject "
                   "matter expert panels of sergeants and field training officers reviewed the ratings, wrote the "
                   "knowledge, skill and ability statements and linked them to the tasks.", S["body"]),
         Paragraph("2. The most critical tasks", S["h2"]),
         _table(S, tasks, [0.5, 4.3, 1.4], right=(2,)),
         Spacer(1, 6),
         Paragraph("3. Knowledge, skills and abilities", S["h2"]),
         Paragraph("The panels judged these needed on the first day of the academy and not learned there:", S["body"]),
         _table(S, ksa, [3.6, 2.6]),
         Spacer(1, 6),
         Paragraph("4. Use", S["h2"]),
         Paragraph("The analysis supports the content of the written test and the oral board's dimensions. It is to be "
                   "reviewed within five years or when the job changes materially.", S["body"])]
    doc.build(s, onFirstPage=_frame("Halvorsen Selection Systems", "Police Officer Job Analysis 2022", "Sans"),
              onLaterPages=_frame("Halvorsen Selection Systems", "Police Officer Job Analysis 2022", "Sans"))


def write_contents(path, rows):
    lines = ["Entry examination 2027: working pack",
             "Personnel Research, %s. Assembled 6 October 2026 for the Commission's November meeting." % K.DIVISION, ""]
    for name, desc in rows:
        lines.append(name)
        lines.append("    " + desc)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
