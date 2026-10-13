"""The pack's documents: the trustees' risk financing policy, the pool's liability coverage memorandum, selected
exhibits of the actuary's 2026 study, the broker's 2027 excess liability indications, and the finance office's
extract notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import LETTER                                         # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W      # noqa: E402

POLICY = "risk_financing_policy_2026.pdf"
MEMO = "liability_coverage_memorandum_2026.pdf"
STUDY = "actuarial_study_2026_selected_exhibits.pdf"
QUOTES = "excess_liability_indications_2027.pdf"
NOTES = "extract_notes_2027_retention_review.md"
BROKER = "Kestrelline Insurance Brokers"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY = colors.HexColor("#1f2329"), colors.HexColor("#5d646c")
PAGE = LETTER

M_BODY = ParagraphStyle("mb", fontName="Serif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=5)
M_CL = ParagraphStyle("mc", parent=M_BODY, leftIndent=24, firstLineIndent=-24)
M_H1 = ParagraphStyle("mh1", fontName="Serif-B", fontSize=15, leading=19, textColor=INK, spaceAfter=3)
M_H2 = ParagraphStyle("mh2", fontName="Serif-B", fontSize=11, leading=14, textColor=INK, spaceBefore=9, spaceAfter=3)
M_META = ParagraphStyle("mm", fontName="Serif", fontSize=9, leading=11.8, textColor=GREY, spaceAfter=8)
S_BODY = ParagraphStyle("sb", fontName="Sans", fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle("sh1", fontName="Sans-B", fontSize=13.5, leading=17, textColor=INK, spaceAfter=2)
S_H2 = ParagraphStyle("sh2", fontName="Sans-B", fontSize=10, leading=13, textColor=INK, spaceBefore=8, spaceAfter=3)
S_META = ParagraphStyle("sm", fontName="Sans", fontSize=8.1, leading=10.4, textColor=GREY, spaceAfter=7)
S_CELL = ParagraphStyle("sc", fontName="Sans", fontSize=8.8, leading=11.4, textColor=INK)
S_CELLR = ParagraphStyle("scr", parent=S_CELL, alignment=2)
S_CELLB = ParagraphStyle("scb", parent=S_CELL, fontName="Sans-B")
S_CELLBR = ParagraphStyle("scbr", parent=S_CELLB, alignment=2)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=PAGE, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=22 * mm,
                             bottomMargin=21 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot, font="Serif"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 8)
        canvas.drawString(24 * mm, PAGE[1] - 12 * mm, top_left)
        canvas.drawRightString(PAGE[0] - 24 * mm, PAGE[1] - 12 * mm, top_right)
        canvas.setFont(font, 7.4)
        canvas.drawString(24 * mm, 11 * mm, foot)
        canvas.drawRightString(PAGE[0] - 24 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def dollars(x):
    return "${:,.0f}".format(x)


# ---------------------------------------------------------------- the trustees' policy
POLICY_CLAUSES = [
    ("1  Purpose", [
        ("1.1", "This policy sets how the pool decides, each year, how much of each liability occurrence it keeps and "
                "above what amount it buys excess insurance."),
    ]),
    ("2  Terms", [
        ("2.1", "An occurrence is an accident, event or wrongful act, or a series of them from one cause, that gives "
                "rise to liability claims against a member. However many claimants or coverage parts it involves, "
                "it is one occurrence."),
        ("2.2", "The cost of an occurrence is what it costs from its first dollar, damages and defense costs together, "
                "whoever pays them: the member within its deductible, the pool, or an excess insurer."),
        ("2.3", "An attachment is the cost of an occurrence, from its first dollar and inclusive of the member's "
                "deductible, above which an excess insurer pays. The retention is the attachment in force for the "
                "pool in a coverage year."),
        ("2.4", "A coverage year is a calendar year. An occurrence's accident year is the calendar year in which it "
                "happens."),
    ]),
    ("3  Inputs", [
        ("3.1", "The actuary's latest study supplies the liability claim cost index by accident year and the expected "
                "number of the coverage year's occurrences costing more than $25,000."),
        ("3.2", "The broker gathers excess insurers' indications at the attachments the trustees ask for."),
    ]),
    ("4  The severity curve", [
        ("4.1", "The pool's ground-up severity curve for a coverage year is the distribution of the cost of an "
                "occurrence, at the coverage year's cost level, over all of the members' liability occurrences."),
        ("4.2", "The curve is lognormal. It is estimated by maximum likelihood from the pool's record of the "
                "occurrences of the latest eight accident years in which every occurrence has closed (for the 2027 "
                "coverage year, the accident years 2014 to 2021), with the record brought to the coverage year's cost "
                "level by the ratio of the coverage year's claim cost index to the accident year's."),
        ("4.3", "The expected number of the coverage year's occurrences costing more than an amount is the actuary's "
                "expected number costing more than $25,000, times the curve's probability that an occurrence costs "
                "more than the amount, divided by the curve's probability that an occurrence costs more than $25,000."),
    ]),
    ("5  The retention", [
        ("5.1", "The pool keeps every layer of cost that it expects its occurrences to reach more than once in a "
                "coverage year, and insures above it. The retention for a coverage year is the lowest attachment "
                "quoted for that year at which the expected number of the year's occurrences costing more than the "
                "attachment is one or fewer."),
        ("5.2", "If no quoted attachment meets 5.1, the retention is the highest attachment quoted."),
        ("5.3", "The retention does not change any member's deductible."),
    ]),
    ("6  Review", [
        ("6.1", "Each autumn the finance director brings the curve, the expected numbers at each quoted attachment and "
                "the indications to the trustees, who set the next year's retention at their November meeting."),
    ]),
]


def write_policy(path):
    title = "Risk Financing Policy"
    doc = _doc(path, title, W.POOL)
    s = [Paragraph(W.POOL.upper(), M_META), Paragraph(title, M_H1),
         Paragraph("Adopted by the Board of Trustees, Resolution 2026-07, 17 June 2026. Replaces the policy adopted "
                   "9 March 2011.", M_META)]
    for head, items in POLICY_CLAUSES:
        s.append(Paragraph(head, M_H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), M_CL))
    foot = "%s | Risk Financing Policy | Resolution 2026-07" % W.POOL
    doc.build(s, onFirstPage=_frame("Board of Trustees", "Resolution 2026-07", foot),
              onLaterPages=_frame("Board of Trustees", "Resolution 2026-07", foot))


# ---------------------------------------------------------------- the coverage memorandum
def memo_sections():
    return [
        ("1  Coverage", [
            "The pool covers its members' liability on an occurrence basis under five parts: general liability, "
            "automobile liability, law enforcement liability, public officials' errors and omissions, and employment "
            "practices liability. An occurrence is covered under the terms in force in the year it happens.",
            "One occurrence is one occurrence however many claimants or coverage parts it involves; the deductible and "
            "the retention apply to it once.",
        ]),
        ("2  Member deductibles", [
            "Each member elects a per-occurrence deductible of $10,000, $25,000, $50,000 or $100,000 for each calendar "
            "year, effective 1 January. The deductible in force on the date of an occurrence applies to it.",
            "The deductible applies to damages and defense costs together.",
            "A member administers and pays an occurrence within its deductible itself and tenders the occurrence to "
            "the pool when its payments on it reach the deductible. From then the pool's administrator adjusts the "
            "occurrence and the pool pays its cost above the deductible.",
        ]),
        ("3  Retention and excess insurance", [
            "The pool pays the cost of an occurrence above the member's deductible up to the pool's retention, which "
            "includes the deductible: $250,000 for occurrences in 2014 to 2017 and $500,000 for occurrences from "
            "1 January 2018.",
            "Above the retention the excess insurer of the occurrence's year pays the cost directly, up to $10,000,000 "
            "for each occurrence. The excess insurer's payments are not entered in the pool's claims system; once the "
            "pool's share is paid, the pool's administrator closes the pool's file on the occurrence.",
        ]),
        ("4  Administration and records", [
            "%s administered the pool's claims from 1 January 2014 to 30 June 2020, and %s from 1 July 2020, when "
            "the claims then open were converted to its system under new numbers." % (W.LEGACY_ADMIN, W.CURRENT_ADMIN),
            "The pool's record of an occurrence is its date, member, coverage part, the member's deductible and the "
            "pool's payments and reserves, as its administrators keep them.",
        ]),
    ]


def write_memo(path):
    who, role = W.PEOPLE["claims"]
    title = "Liability Coverage Memorandum, 2026"
    doc = _doc(path, title, who)
    s = [Paragraph("%s · LIABILITY PROGRAM" % W.POOL.upper(), S_META), Paragraph(title, S_H1),
         Paragraph("A summary for members and trustees of the liability coverage the pool provides and of its program "
                   "history; the memorandum of coverage governs. Issued 5 January 2026 by %s, %s." % (who, role),
                   S_META)]
    for head, paras in memo_sections():
        s.append(Paragraph(head, S_H2))
        for k, t in enumerate(paras, 1):
            s.append(Paragraph("%s.%d&nbsp;&nbsp;&nbsp;%s" % (head.split()[0], k, t),
                               ParagraphStyle("x", parent=S_BODY, leftIndent=22, firstLineIndent=-22)))
    foot = "%s | Liability Coverage Memorandum 2026" % W.POOL
    doc.build(s, onFirstPage=_frame("Liability program", "2026", foot, "Sans"),
              onLaterPages=_frame("Liability program", "2026", foot, "Sans"))


# ---------------------------------------------------------------- the actuary's exhibits
def write_study(path, payroll):
    who, _ = W.PEOPLE["actuary"]
    title = "Actuarial Study of Liability Losses as of September 30, 2026: Selected Exhibits"
    doc = _doc(path, title, who)
    rate = round(W.COUNT_25K / (payroll / 1e6), 5)
    assert round(rate * payroll / 1e6, 1) == W.COUNT_25K
    s = [Paragraph(W.POOL.upper(), S_META), Paragraph(title, S_H1),
         Paragraph("Prepared by %s, FCAS, MAAA, consulting actuary to the pool. October 9, 2026. These pages carry "
                   "Exhibits 3 and 6 of the study; the full study is on file with the finance director." % who, S_META),
         Paragraph("Exhibit 3. Liability claim cost index", S_H2),
         Paragraph("Average cost level of the pool's liability occurrences by accident year, 2014 = 100.0. Accident "
                   "years 2014 to 2026 are measured; 2027 is projected at the selected trend of 6.1 per cent.", S_BODY)]
    rows = [[Paragraph(h, S_CELLB if i == 0 else S_CELLBR) for i, h in enumerate(("Accident year", "Index",
                                                                                   "Change"))]]
    prev = None
    for y in range(W.FIT_YEARS[0], W.COVER_YEAR + 1):
        v = W.INDEX[y]
        ch = "" if prev is None else "%+.1f%%" % (100 * (v / prev - 1))
        rows.append([Paragraph("%d%s" % (y, " (projected)" if y == W.COVER_YEAR else ""), S_CELL),
                     Paragraph("%.1f" % v, S_CELLR), Paragraph(ch, S_CELLR)])
        prev = v
    t = Table(rows, colWidths=[42 * mm, 26 * mm, 24 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    s += [t, Spacer(1, 6),
          Paragraph("Exhibit 6. Projected 2027 frequency", S_H2),
          Paragraph("Occurrences are counted by their cost from the first dollar, damages and defense together, at "
                    "2027 cost.", S_BODY)]
    rows = [[Paragraph("2027 payroll exposure, as declared by the members", S_CELL),
             Paragraph(dollars(payroll), S_CELLR)],
            [Paragraph("Selected occurrences costing more than $25,000, per $1 million of payroll", S_CELL),
             Paragraph("%.5f" % rate, S_CELLR)],
            [Paragraph("Expected 2027 liability occurrences costing more than $25,000", S_CELLB),
             Paragraph("%.1f" % W.COUNT_25K, S_CELLBR)]]
    t = Table(rows, colWidths=[118 * mm, 38 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.3, GREY), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s += [t, Spacer(1, 6),
          Paragraph("The selected frequency is developed in Exhibit 5 of the study.", S_META)]
    foot = "%s | Actuarial study as of 9/30/2026 | Exhibits 3 and 6" % W.POOL
    doc.build(s, onFirstPage=_frame("Actuarial study 2026", "Selected exhibits", foot, "Sans"),
              onLaterPages=_frame("Actuarial study 2026", "Selected exhibits", foot, "Sans"))
    return rate


# ---------------------------------------------------------------- the broker's indications
def write_quotes(path):
    who, role = W.PEOPLE["broker"]
    to = W.PEOPLE["director"]
    title = "Excess Liability Indications for January 1, 2027"
    doc = _doc(path, title, who)
    s = [Paragraph("%s · PUBLIC ENTITY PRACTICE" % BROKER.upper(), S_META), Paragraph(title, S_H1),
         Paragraph("October 2, 2026. To %s, %s, %s. From %s, %s." % (to[0], to[1], W.POOL, who, role), S_META),
         Paragraph("We approached the excess liability market for the pool's 2027 program at the attachments the "
                   "trustees asked for. The lead market's indications are below; following markets have indicated "
                   "support on the same terms. Each option provides $10,000,000 for each occurrence above its "
                   "attachment, on an occurrence basis, for the pool's five liability coverage parts.", S_BODY),
         Spacer(1, 4)]
    rows = [[Paragraph(h, S_CELLB if i == 0 else S_CELLBR) for i, h in enumerate(
        ("Attachment per occurrence", "Limit per occurrence", "Rate per $1,000 of 2027 operating expenditures",
         "Rate per scheduled unit"))]]
    for a in W.OPTIONS:
        gl, al = W.QUOTES[a]
        rows.append([Paragraph(dollars(a), S_CELL), Paragraph("$10,000,000", S_CELLR), Paragraph("$%.4f" % gl, S_CELLR),
                     Paragraph("$%.2f" % al, S_CELLR)])
    t = Table(rows, colWidths=[38 * mm, 34 * mm, 48 * mm, 34 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.3, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s += [t, Spacer(1, 6), Paragraph("Basis of the indications", S_H2),
          Paragraph("Attachments are stated per occurrence, from the first dollar of the occurrence and inclusive of "
                    "the member's deductible.", S_BODY),
          Paragraph("The indicated premium for an option is its operating expenditure rate applied to the members' "
                    "2027 total operating expenditures as declared for the renewal, plus its unit rate applied to the "
                    "units on the members' vehicle schedules at September 30, 2026. Premiums are annual and exclude "
                    "the Washington surplus lines tax and stamping fee.", S_BODY),
          Paragraph("Subjectivities", S_H2),
          Paragraph("The indications are subject to the pool's final 2027 exposure declarations and vehicle "
                    "schedules, to no material change in the pool's loss experience before binding, and to the "
                    "lead market's review of the pool's claims handling. They are valid for binding until "
                    "December 15, 2026.", S_BODY)]
    foot = "%s | %s | Indications, not a binder" % (BROKER, W.POOL)
    doc.build(s, onFirstPage=_frame(BROKER, "2027 excess liability", foot, "Sans"),
              onLaterPages=_frame(BROKER, "2027 excess liability", foot, "Sans"))


# ---------------------------------------------------------------- the extract notes
NOTES_TEXT = """# Extract notes: 2027 retention review

Finance office, {pool}. Files pulled for the trustees' November 2026 meeting; questions on the claims files to
{claims}, on the declarations and schedules to the finance office. The documents beside them are as issued:
{policy}, {memo}, {study} and {quotes}.

## {legacy}

{legacy_short}'s final run of the liability claims it closed, one sheet per accident year and a summary sheet, run
on 2 July 2020 at the end of its administration. Claims open on 30 June 2020 were converted to {current_short}'s
system and are in the current loss run. Member is the member code (member_roster.csv). Coverage: GL general
liability, AL automobile liability, LEL law enforcement liability, POL public officials' errors and omissions, EPL
employment practices liability. Dates are month/day/year. Amounts are dollars: Member Deductible is the member's
deductible for the occurrence; Indemnity Paid, Defense Paid and Total Paid are the pool's payments.

## {current}

{current_short}'s loss run of every liability occurrence it has handled since 1 July 2020, open and closed, at
30 September 2026. prior_claim_no is the {legacy_short} number of a claim converted on 1 July 2020. coverage: GENL,
AUTO, LAWE, PUBO and EMPL are the same five parts as {legacy_short}'s GL, AL, LEL, POL and EPL. deductible is the
member's deductible for the occurrence; the paid_ and reserve_ columns are the pool's payments and case reserves to
date, indemnity and defense, in dollars.

## {log}

The transaction log of the pool's vehicle schedule system from its opening load (dated 1 January 2022), with
every entry keyed through 19 October 2026: one row for each add, delete or change of a unit on a member's schedule. effective_date is when
the change applies to coverage; entered_date is when it was keyed. stated_value is the value carried for physical
damage cover, blank on deletes.

## {decl}

The 2027 renewal exposure declarations as exported from the declarations intake on 5 October 2026, one row for each
department line a member declared. Budget Basis says whether the member's 2027 budget was adopted or still proposed
when it declared.

## member_roster.csv

Every member since 2014: member number, legacy member code, class, the date it joined the pool and, where it has
left, the date it withdrew.

## {dedhist}

Each member's per-occurrence deductible since 2014, one row for each change, effective 1 January.

## {tri}

The actuary's development data for the liability program: the pool's paid and incurred (paid plus case reserves)
by accident year and evaluation date, with the counts of occurrences tendered and closed. Amounts are the pool's,
net of member deductibles.
"""


def write_notes(path, names):
    open(path, "w").write(NOTES_TEXT.format(pool=W.POOL, claims=W.PEOPLE["claims"][0], legacy_admin=W.LEGACY_ADMIN,
                                            current_admin=W.CURRENT_ADMIN, legacy_short=W.LEGACY_ADMIN.split()[0],
                                            current_short=W.CURRENT_ADMIN.split()[0], policy=POLICY, memo=MEMO,
                                            study=STUDY, quotes=QUOTES,
                                            **names))
