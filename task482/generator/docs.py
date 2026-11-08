"""task482 architecture 17: the Trust's PDFs, written in Writer and exported (officepdf): the paper specification,
the standard-setting record, the council's minute, the 2026 course review and the make-up roster."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

NZT = P.NZST
NZDT = __import__("datetime").timezone(__import__("datetime").timedelta(hours=13))
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.4, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=7.6, leading=9.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")
AUTHOR = P.TRUST


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(rows, widths):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333"))]))
    return t


def _p(t, st=BODY):
    return Paragraph(_esc(t), st)


def specification(path):
    s = [_p("Year 10 Science Benchmark: paper specification, 2027", H1),
         _p("%s, Assessment Committee. Approved 4 November 2026; replaces the 2026 specification." % P.TRUST, SMALL),
         Spacer(1, 4),
         _p("1. Purpose", H2),
         _p("The Benchmark reports each Year 10 candidate at member schools against the Achieved, Merit and Excellence "
            "standards of the Trust's Year 10 science course. Results are returned to schools for their reports to "
            "families."),
         _p("2. Sitting and form", H2),
         _p("The 2027 Benchmark is sat online in November 2027, on the dates the Council set on 14 October 2026. The "
            "paper has 50 one-mark items, multiple-choice and short-answer, and candidates have 60 minutes."),
         _p("3. Content", H2),
         _p("Items are drawn from the Year 10 science item bank and cover the six core units of the course outline. "
            "The paper holds each strand within these limits:"),
         _table([["Strand", "Items on the paper"], ["Material World", "10 to 14"], ["Living World", "10 to 14"],
                 ["Physical World", "12 to 16"], ["Planet Earth and Beyond", "10 to 14"]], [70, 40]),
         _p("4. Targeting", H2),
         _p("The paper set for 2027 is the submitted draft whose expected mark at the Achieved standard, for a "
            "candidate sitting the 2027 paper, is nearest 25 of its 50 marks. The expected mark is the sum over the "
            "paper's items of the probability, under the Rasch model on the bank scale, that a candidate at the "
            "Achieved standard answers the item correctly. Drafts are compared on their expected marks before rounding."),
         _p("5. Standards", H2),
         _p("The Achieved, Merit and Excellence standards are those of the standard-setting record for the Year 10 "
            "Science Benchmark."),
         _p("6. Review", H2),
         _p("Every item on a submitted draft has passed the Trust's content, language and cultural reviews.")]
    O.build(path, s, "Year 10 Science Benchmark paper specification 2027", AUTHOR,
            "Paper specification for the 2027 Year 10 Science Benchmark", "Year 10 Science Benchmark: paper specification 2027",
            dt.datetime(2026, 11, 4, 15, 12, tzinfo=NZDT), dt.datetime(2026, 11, 4, 16, 40, tzinfo=NZDT))


def standards(path, raw_cuts):
    rows = [["Form (August 2026)", "Items", "Raw mark at the Achieved standard"]]
    for f, c in raw_cuts:
        rows.append(["F%d" % (f + 1), "50", str(c)])
    s = [_p("Year 10 Science Benchmark: standard-setting record", H1),
         _p("%s. Standards set by a Bookmark panel of fourteen teachers, 12 and 13 August 2024; confirmed by the "
            "Assessment Committee on 3 March 2026." % P.TRUST, SMALL), Spacer(1, 4),
         _p("1. The standards", H2),
         _p("Each standard is a point on the Year 10 science bank scale (logits). A candidate is reported at a "
            "standard when their ability estimate on the bank scale reaches it."),
         _table([["Standard", "Bank scale (logits)"], ["Achieved", "%.2f" % P.THETA_ACHIEVED],
                 ["Merit", "%.2f" % P.THETA_MERIT], ["Excellence", "%.2f" % P.THETA_EXCELLENCE]], [60, 50]),
         _p("2. Raw marks on the August 2026 forms", H2),
         _p("For reporting the August 2026 sitting, each form's raw mark at the Achieved standard was read from the "
            "final 2026 calibration:"),
         _table(rows, [45, 20, 60]),
         _p("3. Panel", H2),
         _p("The panel worked from an ordered item booklet of the 2024 forms over three rounds, with impact data "
            "after round two. The committee reviewed the standards against the 2025 and 2026 results in March 2026 "
            "and left them unchanged.")]
    O.build(path, s, "Year 10 Science Benchmark standard-setting record", AUTHOR,
            "Standards for the Year 10 Science Benchmark on the bank scale", "Year 10 Science Benchmark: standard-setting record",
            dt.datetime(2026, 3, 3, 14, 5, tzinfo=NZDT), dt.datetime(2026, 3, 4, 9, 22, tzinfo=NZDT))


def minute(path):
    s = [_p("Minutes of the Council", H1),
         _p("%s. Meeting of 14 October 2026, held at the Trust's offices and by video link." % P.TRUST, SMALL),
         Spacer(1, 4),
         _p("1. Apologies and minutes", H2),
         _p("Apologies were received from two members. The minutes of 12 August 2026 were confirmed."),
         _p("2. Finance", H2),
         _p("The council received the accounts to 30 September 2026 and approved the draft 2027 budget for "
            "consultation with member schools."),
         _p("3. Membership", H2),
         _p("No school joined or left the Trust in the period."),
         _p("4. Platform", H2),
         _p("The delivery platform contract was renewed for 2027 on the same terms."),
         _p("5. Benchmark timing", H2),
         _p("The council resolved that from 2027 the Year 10 Science Benchmark is sat from Monday 1 November to "
            "Friday 12 November, so that results reach families with schools' end-of-year reports. The Assessment "
            "Committee is to set the 2027 paper by the end of the year."),
         _p("6. General business", H2),
         _p("The chair thanked the make-up host schools for the August sitting.")]
    O.build(path, s, "Minutes of the Council 14 October 2026", AUTHOR, "Council minutes, 14 October 2026",
            "Council minutes, 14 October 2026", dt.datetime(2026, 10, 16, 10, 2, tzinfo=NZDT),
            dt.datetime(2026, 10, 16, 11, 48, tzinfo=NZDT))


def course_review(path, sch, seq_rows):
    units = [["Unit", "Strand", "Term", "Weeks suggested"]]
    for code, name, strand, term in P.UNITS:
        units.append(["%s %s" % (code, name), strand, str(term), "9 to 10" if term < 3 else "4 to 6"])
    units.append(["School's own choice (extension and revision)", "", "4", ""])
    s = [_p("Year 10 Science: course review 2026", H1),
         _p("%s, Curriculum Committee. Presented to the Assessment Committee, 9 September 2026." % P.TRUST, SMALL),
         Spacer(1, 4),
         _p("1. The course outline", H2),
         _p("The Year 10 science course has six core units over Terms 1 to 3, with Term 4 left to each school. The "
            "weeks suggested are a guide."),
         _table(units, [70, 45, 15, 30]),
         _p("2. Review", H2),
         _p("Schools again reported that the electricity unit runs long and that practical time in Earth's systems "
            "depends on field trips. The committee proposes no change to the core units for 2027."),
         _p("3. Item bank", H2),
         _p("Bank items are tagged to the six core units (U1 to U6). The strands follow the New Zealand Curriculum."),
         PageBreak(),
         _p("Appendix B. Member schools' Year 10 science sequences, 2026", H2),
         _p("Sequences are as each school returned them. Week numbers are the school's own weeks of the term, counted "
            "from the school's Term 3 start date in the second column.", SMALL),
         _table([["School", "Term 3 began", "Term 1 and 2", "Term 3"]] + seq_rows, [38, 20, 56, 60])]
    O.build(path, s, "Year 10 Science course review 2026", AUTHOR, "Course outline and member schools' sequences, 2026",
            "Year 10 Science: course review 2026", dt.datetime(2026, 9, 8, 16, 30, tzinfo=NZT),
            dt.datetime(2026, 9, 9, 8, 15, tzinfo=NZT))


def roster(path, blocks):
    s = [_p("Year 10 Science Benchmark: make-up sitting, 25 to 27 August 2026", H1),
         _p("Booked candidates by host centre, as typed from the host supervisors' returns. Paper form M26.", SMALL)]
    first = True
    for host_name, host_code, rows in blocks:
        if not first:
            s.append(PageBreak())
        first = False
        s.append(_p("Host centre: %s (%s)" % (host_name, host_code), H2))
        s.append(_table([["Day", "Script", "Entry no", "Candidate", "Home school", "Attended"]] + rows,
                        [22, 24, 22, 50, 24, 20]))
    O.build(path, s, "Make-up sitting roster August 2026", AUTHOR, "Make-up sitting roster by host centre",
            "Make-up sitting, August 2026", dt.datetime(2026, 8, 28, 15, 40, tzinfo=NZT),
            dt.datetime(2026, 8, 31, 9, 5, tzinfo=NZT))
