"""The three governing documents, written as the organisations that issue them would write them."""
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import world as WD

rl_config.invariant = 1

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Normal"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=SS["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=6,
                    spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.2, leading=10.5, textColor=colors.HexColor("#333333"))


def _doc(path, title, author, story):
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                          bottomMargin=18 * mm, title=title, author=author, subject="", creator=author,
                          producer=author)
    d.build(story)


def _table(rows, widths, head=True):
    t = Table(rows, colWidths=widths)
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8"))]
    t.setStyle(TableStyle(st))
    return t


def fund_terms(path):
    s = []
    s.append(Paragraph("ARDMUIR UNIVERSITY", SMALL))
    s.append(Paragraph("University Court", SMALL))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Course Texts Fund 2027: terms", H1))
    s.append(Paragraph("Paper UC/26/114. Approved by the Court on 15 October 2026. Owner: University Librarian. "
                       "Next review: October 2027.", SMALL))
    s.append(Paragraph("1. Background", H2))
    s.append(Paragraph("On 15 October 2026 the Court upheld complaint SA/C/2026/07 from the Students' Association "
                       "about how long students waited for course e-textbooks lent on Shelfmark Lend in the spring "
                       "2026 semester, and established the Course Texts Fund 2027 of &pound;180,000 for additional "
                       "licences of course e-textbooks in the 2027 calendar year.", BODY))
    s.append(Paragraph("2. Division among faculties", H2))
    s.append(Paragraph("2.1 The Fund is divided among the faculties of the University as they stand from 1 August "
                       "2026 (Schedule 1).", BODY))
    s.append(Paragraph("2.2 Each faculty's share of the Fund is its share of the hold-weeks of the spring 2026 "
                       "semester.", BODY))
    s.append(Paragraph("2.3 Each faculty's amount is credited to its 2026-27 course texts fund code (Schedule 2).",
                       BODY))
    s.append(Paragraph("3. Hold-weeks", H2))
    s.append(Paragraph("3.1 A hold counts if a student placed it on a course e-textbook on Shelfmark Lend between "
                       "Monday 12 January and Sunday 26 April 2026, by UK time. Holds placed by members of staff do "
                       "not count.", BODY))
    s.append(Paragraph("3.2 A hold counts for the faculty of the school the student belonged to when the hold was "
                       "placed, each school being taken in the faculty it belongs to from 1 August 2026.", BODY))
    s.append(Paragraph("3.3 A hold's hold-weeks are the weeks beyond the second that it waited for a copy: the time "
                       "from the moment the hold was placed to the moment Shelfmark Lend offered it a copy or, for a "
                       "hold that was cancelled, to the moment a copy would have been offered to it had it not been "
                       "cancelled, less fourteen days, and never more than ten weeks. A hold that waited fourteen "
                       "days or less has no hold-weeks.", BODY))
    s.append(Paragraph("3.4 A faculty's hold-weeks are the sum of the hold-weeks of its holds.", BODY))
    s.append(Paragraph("4. Review and reporting", H2))
    s.append(Paragraph("Internal Audit reviews the division before the Fund opens on 4 January 2027. The University "
                       "Librarian reports each faculty's amount, holds and hold-weeks to the Court at its December "
                       "2026 meeting.", BODY))
    s.append(Paragraph("Schedule 1. Faculties from 1 August 2026", H2))
    rows = [["Faculty", "Schools"]]
    names = {c: n for c, n, olds in P.FACULTIES}
    for code, name, olds in P.FACULTIES:
        schools = ["%s (%s)" % (sn, sc) for sc, sn, old, n in WD.SCHOOLS if old in olds]
        txt = ", ".join(schools)
        if code == "SAE":
            txt += ". Formed on 1 August 2026 from the Faculty of Engineering and the Faculty of Physical Sciences."
        rows.append([Paragraph(names[code], SMALL), Paragraph(txt, SMALL)])
    s.append(_table(rows, [42 * mm, 128 * mm]))
    s.append(Paragraph("Schedule 2. Course texts fund codes", H2))
    old_names = {"AH": "Arts and Humanities", "SS": "Social Sciences", "BS": "Ardmuir Business School", "LW": "Law",
                 "EN": "Engineering", "PS": "Physical Sciences", "LS": "Life Sciences", "MD": "Medicine and Dentistry",
                 "NH": "Nursing and Health Sciences"}
    rows = [["Fund code", "Faculty", "In use", "Faculty from 1 August 2026"]]
    for o in ["AH", "SS", "BS", "LW", "EN", "PS", "LS", "MD", "NH"]:
        rows.append(["CT-" + o, old_names[o], "to 31 July 2026", names[WD.new_faculty(o)]])
    for code, name, olds in P.FACULTIES:
        rows.append(["CT-" + code, name, "from 1 August 2026", name])
    rows.append(["CT-CORE", Paragraph("Course texts bought centrally (publisher packages)", SMALL), "throughout", ""])
    s.append(_table(rows, [22 * mm, 64 * mm, 34 * mm, 50 * mm]))
    _doc(path, "Course Texts Fund 2027: terms", "Ardmuir University Court", s)


def lending_terms(path):
    s = []
    s.append(Paragraph("Shelfmark Lend", SMALL))
    s.append(Paragraph("Lending and licence terms for institutional customers", H1))
    s.append(Paragraph("Version 2025.2, effective 1 August 2025. Shelfmark Lend Ltd, Edinburgh.", SMALL))
    s.append(Paragraph("1. Loans", H2))
    s.append(Paragraph("1.1 A borrower chooses a loan of 1, 3 or 7 days. A borrower may return a title early; "
                       "otherwise the loan ends when its loan period ends.", BODY))
    s.append(Paragraph("1.2 A borrower may hold one loan, one offer or one hold of a title at a time.", BODY))
    s.append(Paragraph("2. Holds", H2))
    s.append(Paragraph("2.1 When every copy a customer licenses for a title is on loan or under offer, a borrower may "
                       "place a hold.", BODY))
    s.append(Paragraph("2.2 When a copy becomes free it is offered to the earliest-placed hold still waiting on the "
                       "title, and the borrower is notified. The borrower has 48 hours to borrow the offered copy; an "
                       "offer that is not taken up lapses and the copy is offered to the next hold.", BODY))
    s.append(Paragraph("2.3 A borrower may cancel a hold at any time. The holds of a borrower whose institutional "
                       "account is closed are cancelled when the account closes.", BODY))
    s.append(Paragraph("3. Licence models", H2))
    rows = [["Model", "Terms"],
            ["1 user, perpetual", Paragraph("One borrower at a time. No expiry.", SMALL)],
            ["3 users, perpetual", Paragraph("Three borrowers at a time. No expiry.", SMALL)],
            ["1 user, 40 loans", Paragraph("One borrower at a time. The licence lapses when its fortieth loan ends.", SMALL)],
            ["Publisher package", Paragraph("Each title in a package the customer subscribes to may be borrowed by "
                                           "three borrowers at a time for the subscription period.", SMALL)]]
    s.append(_table(rows, [40 * mm, 130 * mm]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("3.2 Where a customer holds more than one 40-loan licence for a title, each loan is counted "
                       "against the earliest-purchased of those licences that has loans left.", BODY))
    s.append(Paragraph("3.3 Where automatic re-licensing is enabled, a 40-loan licence that lapses is replaced when it "
                       "lapses by a new 40-loan licence for the title, invoiced at the current price on the following "
                       "monthly invoice.", BODY))
    s.append(Paragraph("4. Invoicing", H2))
    s.append(Paragraph("4.1 Title licences and re-licences are invoiced monthly in arrears, by Shelfmark Lend or, for "
                       "a publisher that sells through an appointed agent, by the agent in the agent's currency. "
                       "Publisher packages are invoiced annually in advance.", BODY))
    _doc(path, "Lending and licence terms for institutional customers", "Shelfmark Lend Ltd", s)


def procedures(path):
    s = []
    s.append(Paragraph("ARDMUIR UNIVERSITY LIBRARY", SMALL))
    s.append(Paragraph("Collections procedures: course texts (extract)", H1))
    s.append(Paragraph("Collections and Content. Version 3, 24 August 2026. Owner: Head of Collections and Content.",
                       SMALL))
    s.append(Paragraph("C3.1 Reading lists", H2))
    s.append(Paragraph("A reading list belongs to the faculty of the school that teaches the course, each school "
                       "being taken in the faculty it belongs to from 1 August 2026 (Court paper UC/26/114, Schedule 1). "
                       "Items are marked Essential, Recommended or Background by the course leader.", BODY))
    s.append(Paragraph("C3.2 Course text spend", H2))
    s.append(Paragraph("A faculty's course text spend for a period is the net amount, in pounds, of the invoice lines "
                       "dated in the period that are charged to its course texts fund (Court paper UC/26/114, "
                       "Schedule 2), together with its share of each publisher package invoiced in the period. Lines "
                       "in euros or US dollars are converted at the Finance Office's rate for the month of the invoice "
                       "date. A package is charged to CT-CORE; its net amount is shared among the faculties in "
                       "proportion to the number of the package's titles on each faculty's essential reading lists for "
                       "the academic year in which it is invoiced.", BODY))
    s.append(Paragraph("C3.4 Coverage", H2))
    s.append(Paragraph("An essential item on a reading list is covered on a date if on that date the Library could "
                       "lend, as an e-book on Shelfmark Lend, the edition the list cites or a later edition of the same "
                       "work, whether licensed title by title or through a publisher package.", BODY))
    s.append(Paragraph("C3.6 Metered licences", H2))
    s.append(Paragraph("Automatic re-licensing is enabled for all 40-loan licences (Shelfmark terms 3.3). A licence "
                       "and each re-licence of it are charged to the course texts fund of the faculty whose school "
                       "ordered the title, under the fund code in use on the date of the order or re-licence.", BODY))
    _doc(path, "Collections procedures: course texts", "Ardmuir University Library", s)
