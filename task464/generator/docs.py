"""task464 architecture 8: the governing documents.

Three PDFs. Between them they file WHAT the review has to produce and HOW the moderation sample is drawn, and
neither of those is HOW the composition is to be computed:

  coding_manual_2025.pdf           what each of the six categories means. No hit rate appears anywhere.
  quality_assurance_procedure.pdf  how the moderation sample is drawn (a fixed number per CODED category) and
                                   that the moderating coder's category is the authoritative one. It does not
                                   say what to do with the sample.
  withdrawal_review_terms_of_reference.pdf
                                   the estimand: the share of withdrawals that HAPPENED for each reason, over
                                   all four terms, to one decimal place, and the one reason the 2027 retention
                                   budget will carry.

No document states a corrected share, a per-category hit rate, or any ranking of the reasons.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import world as W

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
S = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=S["Heading1"], fontSize=13, spaceAfter=7)
H2 = ParagraphStyle("h2", parent=S["Heading2"], fontSize=10.5, spaceBefore=9, spaceAfter=4)
BODY = ParagraphStyle("body", parent=S["BodyText"], fontSize=9, leading=12.5, spaceAfter=5)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.8, textColor=colors.HexColor("#555555"))


def _doc(name, title, flow):
    d = SimpleDocTemplate(os.path.join(OUT, name), pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=18 * mm,
                          title=title, author=W.SERVICE, subject="", creator="")
    d.build(flow)
    return name


def _table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, 1), (-1, -2), 0.2, colors.HexColor("#bbbbbb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


MEANING = {
    "CR": ("Use this code where the learner gives looking after another person as the reason they stopped "
           "attending. It covers children, an adult relative, a partner and a neighbour, and it covers both a "
           "standing arrangement and one that broke down."),
    "WH": ("Use this code where the learner gives their paid working hours as the reason, including a change of "
           "shift, a change of rota, extra hours taken on, and an employer declining to move a shift."),
    "TR": ("Use this code where the learner gives getting to or from the centre as the reason, including a "
           "service withdrawn, the cost of the journey, a lift that fell through and parking."),
    "CD": ("Use this code where the learner gives the demand of the course itself as the reason, including the "
           "level, the pace, the assignments and being placed on the wrong course."),
    "HL": ("Use this code where the learner gives their own physical or mental health as the reason, including a "
           "period signed off, a waiting list and a change of medication."),
    "OT": ("Use this code where the learner gives no reason, gives one the five codes above do not cover, or "
           "gives only that the course was not for them."),
}


def coding_manual():
    f = [Paragraph("%s" % W.MANUAL, H1),
         Paragraph("Version 4.2, in force from 1 September 2025. Supersedes version 4.1.", SMALL),
         Paragraph("Purpose", H2),
         Paragraph("Every withdrawal recorded on the student record carries the learner's exit comment in their "
                   "own words. A coder reads the comment and records one reason code against the withdrawal. "
                   "One code is recorded for each withdrawal, and only one.", BODY),
         Paragraph("Choosing between codes", H2),
         Paragraph("Comments often touch on more than one thing. Where a comment carries more than one reason, "
                   "record the code for the reason the learner puts first. Where a comment is short or general, "
                   "record OT rather than inferring a reason the learner has not given.", BODY),
         Paragraph("The codes", H2)]
    data = [["Code", "Reason", "When to use it"]]
    for c in W.CODES:
        data.append([c, Paragraph(W.LABEL[c], BODY), Paragraph(MEANING[c], BODY)])
    f.append(_table(data, [16 * mm, 32 * mm, 118 * mm]))
    f += [Paragraph("Changes in version 4.2", H2),
          Paragraph("Version 4.1 carried a seventh code, FN, for financial reasons. FN is withdrawn. Comments "
                    "that would have carried FN are now coded under the reason the learner gives for the cost "
                    "mattering, most often TR where the cost is the journey, and otherwise OT. Withdrawals coded "
                    "before 1 September 2025 keep the code they were given.", BODY)]
    return _doc("coding_manual_2025.pdf", W.MANUAL, f)


def qa_procedure():
    f = [Paragraph("Exit comment coding: quality assurance procedure", H1),
         Paragraph("%s. Issued by the quality team, September 2025." % W.SERVICE, SMALL),
         Paragraph("Why we moderate", H2),
         Paragraph("Coding an exit comment is a judgement. Two coders reading the same comment do not always "
                   "place it in the same category, and the service needs to know how its coding stands up "
                   "before the figures are used. The quality team therefore moderates a sample of coded "
                   "withdrawals every term.", BODY),
         Paragraph("How the sample is drawn", H2),
         Paragraph("The sample is drawn <b>by reason code</b>. For each of the six codes in the manual, the "
                   "quality team draws %d withdrawals across the year that carry that code, spread across the "
                   "four terms. The sample is therefore the same size for every code and is not in proportion "
                   "to how often each code is recorded. It is not a sample of withdrawals in general and it "
                   "must not be read as one."
                   % W.MODERATED_PER_CODE, BODY),
         Paragraph("What the moderating coder records", H2),
         Paragraph("A senior coder re-reads the learner's comment without seeing the code already recorded "
                   "against it, and records the category the comment belongs in under the manual. Where the two "
                   "differ, the moderating coder's category stands as the service's view of that comment. The "
                   "original code is left on the student record so that the two can be compared.", BODY),
         Paragraph("What is published", H2),
         Paragraph("The moderation file is released with the withdrawal extracts each year. The quality team "
                   "reports the number of comments moderated and does not publish any figure derived from "
                   "them.", BODY)]
    return _doc("quality_assurance_procedure.pdf", "Coding quality assurance procedure", f)


def terms_of_reference():
    f = [Paragraph("%s withdrawal review %s: terms of reference" % (W.SERVICE, W.YEAR), H1),
         Paragraph("Agreed by the head of service, %s. Lead: %s, retention lead."
                   % (W.ASOF, W.PEOPLE["retention_lead"]), SMALL),
         Paragraph("What the review is for", H2),
         Paragraph("The service carries one retention budget line in %s and it funds work against a single "
                   "reason for withdrawal. The review decides which reason that is." % W.DECISION_YEAR, BODY),
         Paragraph("What the review has to produce", H2),
         Paragraph("For each of the six reasons in the %s, the share of the service's %s withdrawals that "
                   "<b>happened for that reason</b>, as a percentage of all withdrawals recorded across the "
                   "four terms of %s, to one decimal place. The six shares are of one total and together they "
                   "account for every withdrawal in the year."
                   % (W.MANUAL, W.YEAR, W.YEAR), BODY),
         Paragraph("Scope", H2),
         Paragraph("All withdrawals recorded across the four terms of %s at the service's five centres, on every "
                   "curriculum area. Learners who completed and learners still enrolled are out of scope. "
                   "Withdrawals from earlier years are out of scope." % W.YEAR, BODY),
         Paragraph("The call", H2),
         Paragraph("The review names one reason, with the runner-up and the gap between them, and the budget "
                   "line follows it. The review does not reopen the coding manual and does not recode any "
                   "withdrawal.", BODY)]
    return _doc("withdrawal_review_terms_of_reference.pdf",
                "Withdrawal review terms of reference", f)


def main():
    for fn in (coding_manual, qa_procedure, terms_of_reference):
        print("  %s" % fn())


if __name__ == "__main__":
    main()
