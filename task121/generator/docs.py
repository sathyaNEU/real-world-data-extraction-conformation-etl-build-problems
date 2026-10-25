"""The pack's documents: the director of education's paper to the trustees, the council's guide to the transfer file,
the trust's summary of the 2026 key stage 4 measures and its attendance reporting note."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
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
INK, GREY, RULE = colors.HexColor("#1b2430"), colors.HexColor("#56616c"), colors.HexColor("#b8c0c8")
GREEN = colors.HexColor("#1f5e4a")
NAVY = colors.HexColor("#22355a")
RUST = colors.HexColor("#7a3b1d")

NAMES = {s[0]: s[1] for s in K.SECONDARIES}


def styles(face="Sans", accent=GREEN):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.0, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.5, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.8, leading=14, textColor=INK, spaceBefore=8, spaceAfter=2,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.2, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.9, leading=10.1, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28),
        sub=ParagraphStyle("s", parent=body, leftIndent=44, firstLineIndent=-16))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.6)
        canvas.drawString(20 * mm, A4[1] - 13 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 13 * mm, right)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=(), head_bg=colors.HexColor("#e6ede9")):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
          ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    for c in right:
        st.append(("ALIGN", (c, 1), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author, subject, left, right):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                             producer=author), _frame(left, right)


def write_paper(path, tables):
    S = styles("Serif", GREEN)
    doc, fr = _doc(path, "Paper 6: Halwick Academy, the Progress 8 gap", K.PEOPLE["director"], "Board of Trustees",
                   K.TRUST + ", Board of Trustees, 9 December 2026", "Paper 6 (draft for the chair's briefing)")
    P = lambda t, s="body": Paragraph(t, S[s])
    by = {}
    for r in tables:
        by.setdefault(r[0], {})[r[2]] = r[5]
    urn = {v: k for k, v in K.SEC_URN.items()}
    rows = [["Academy", "2021/22", "2022/23", "2023/24"]]
    for k in K.TRUST_KEYS:
        rows.append([NAMES[k]] + [by[K.SEC_URN[k]][y] for y in ("2021/22", "2022/23", "2023/24")])
    f = [P(K.TRUST, "h1"),
         P("Board of Trustees, 9 December 2026. Paper 6, for decision. From %s, Director of Education. Draft of 23 "
           "October 2026 for the chair's briefing." % K.PEOPLE["director"], "meta"),
         P("Halwick Academy: the Progress 8 gap and the 2027 school improvement plan", "h2"),
         P("1. Purpose", "h2"),
         P("At its meeting on 24 September the board asked how much of Halwick Academy's gap to the rest of the trust "
           "on Progress 8 is the academy's own doing, before it votes the 2027 school improvement plan in December. "
           "This paper sets out what the board asked for, so that the analysis answers that question as the board "
           "put it. The figures follow in the analysis workbook, with the two annexes the board asked for."),
         P("2. Where Halwick stands", "h2"),
         P("Progress 8 as published for the trust's academies (the Department's revised figures):"),
         _table(S, rows, [62 * mm, 30 * mm, 30 * mm, 30 * mm], right=(1, 2, 3)),
         P("Source: Department for Education, key stage 4 performance tables (revised), 2021/22 to 2023/24.", "note"),
         P("Halwick's Progress 8 has been the lowest in the trust in each of the last three published years. There is "
           "no Progress 8 for 2024/25 or 2025/26: the key stage 2 tests those cohorts would have sat in 2020 and 2021 "
           "were cancelled, so these three cohorts are the last the measure covers."),
         P("3. What the board asked for", "h2"),
         P("The board asked for Halwick's gap to the trust average to be walked in four items that add up to the "
           "gap:"),
         P("<b>The gap.</b> Halwick's average Progress 8 less the trust's average, over the pupils who finished key "
           "stage 4 at the trust's eight academies in 2022, 2023 and 2024 and have a Progress 8 score, the three "
           "cohorts pooled so that each pupil counts once.", "clause"),
         P("(a)&nbsp;&nbsp;<b>Attendance:</b> the effect of a pupil's year 11 absence rate (sessions missed in the "
           "autumn and spring terms as a percentage of sessions possible) on their Progress 8, times Halwick's average "
           "absence rate less the trust's.", "clause"),
         P("(b)&nbsp;&nbsp;<b>Disadvantage:</b> the effect of being disadvantaged on a pupil's Progress 8, times "
           "Halwick's share of disadvantaged pupils less the trust's.", "clause"),
         P("(c)&nbsp;&nbsp;<b>The academy's own effect:</b> how far the Progress 8 of Halwick's pupils differs from "
           "what the same pupils, with the same attendance, would have made at the trust's average academy, that is "
           "with the eight academies' own effects averaged over the trust's pupils.", "clause"),
         P("(d)&nbsp;&nbsp;<b>The remainder:</b> the gap less the other three items.", "clause"),
         P("Every effect is measured on all the borough's pupils in the three cohorts, in the council's transfer file, "
           "and is read as it stands, without shrinking it toward the average, the way Progress 8 itself reports a "
           "school. The walk is given in Progress 8 points to one decimal place: the board has been clear that it "
           "wants the size of each item, not a precision the cohorts cannot support."),
         P("4. What the board will decide", "h2"),
         P("The trust's school improvement budget for 2027 is GBP 640,000. If the academy's own effect is the largest "
           "item in the walk, the plan puts it into a Halwick improvement programme (curriculum leadership, teaching "
           "and the academy's leadership capacity). If it is not, the plan follows the largest item instead. The "
           "analysis should therefore say which item is largest and what lies behind it."),
         P("5. Annexes the board asked for", "h2"),
         P("<b>Annex A, attendance in 2025/26.</b> For each academy, the persistent absence rate (the share of its "
           "pupils missing 10 per cent or more of their possible sessions) and the severe absence rate (50 per cent "
           "or more), counted as the trust's attendance reporting note sets out.", "clause"),
         P("<b>Annex B, results in 2026.</b> For each academy, the average Attainment 8 and the EBacc entry rate of "
           "its 2026 cohort (its pupils in year 11 in 2025/26), as the trust's summary of the 2026 key stage 4 "
           "measures defines them.", "clause"),
         P("6. Data", "h2"),
         P("The council's key stage 2 to key stage 4 transfer file for the borough's fourteen secondary schools "
           "(2022 to 2024), shared under the data sharing agreement of March 2026; the Department's performance tables "
           "and Progress 8 estimates; the trust warehouse's attendance extract and movements log for 2025/26; and the "
           "summer 2025 and summer 2026 results from the trust's examination centres."),
         P("%s<br/>Director of Education" % K.PEOPLE["director"])]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_guide(path):
    S = styles("Sans", NAVY)
    doc, fr = _doc(path, "KS2 to KS4 transfer file: guide for data sharing partners", K.PEOPLE["la"], "Data guide",
                   K.COUNCIL, "School Performance and Data Team, September 2026")
    P = lambda t, s="body": Paragraph(t, S[s])
    rows = [["Field", "What it holds"],
            ["pupil_ref", "The council's pseudonymised reference for the pupil; one row per pupil"],
            ["ks4_year", "Academic year the pupil finished key stage 4 (2021/22, 2022/23 or 2023/24)"],
            ["ks4_urn, ks4_laestab, ks4_school", "The secondary school the pupil is counted at: the school they were "
                                                 "on roll at in the January census of year 11"],
            ["gender, sen_provision, eal", "From the January census of year 11. sen_provision: N none, K SEN support, "
                                          "E education, health and care plan"],
            ["disadvantaged", "Y if the pupil was eligible for free school meals at any census in the last six years, "
                              "looked after, or previously looked after, as at the January census of year 11"],
            ["ks2_year, ks2_la, ks2_urn", "The year the pupil sat the key stage 2 tests, and the local authority number "
                                         "and URN of the school they sat them at (397 is Brantholme)"],
            ["ks2_read_scaled, ks2_mat_scaled", "Key stage 2 reading and mathematics scaled scores (80 to 120)"],
            ["ks2_prior_attainment", "The average of the two scaled scores, the prior attainment Progress 8 uses"],
            ["y11_sessions_possible, y11_sessions_auth_absence, y11_sessions_unauth_absence",
             "Sessions possible and sessions missed (authorised and unauthorised) in the autumn and spring terms of "
             "year 11, from the termly censuses"],
            ["att8, att8_english, att8_maths, att8_ebacc, att8_open", "Attainment 8 and its four elements"],
            ["p8_score", "Progress 8 as the Department calculated it for the pupil; blank where the pupil has no key "
                         "stage 2 result"]]
    f = [P(K.COUNCIL, "h1"),
         P("%s. Key stage 2 to key stage 4 transfer file, 2021/22 to 2023/24: guide for data sharing partners. "
           "September 2026. Contact: %s, School Performance and Data Manager." % (K.LA_TEAM, K.PEOPLE["la"]),
           "meta"),
         P("What the file holds", "h2"),
         P("One row for every pupil who finished key stage 4 at one of the borough's fourteen state-funded mainstream "
           "secondary schools in 2021/22, 2022/23 or 2023/24, with their key stage 2 results, their school census "
           "record and their key stage 4 results. Special schools and the pupil referral unit are not in the file. The "
           "key stage 4 results and Progress 8 scores are the Department's revised (final) data for each year."),
         _table(S, rows, [58 * mm, 112 * mm]),
         P("Notes", "h2"),
         P("Pupils who arrived in England after key stage 2, or whose results were not recorded, have no Progress 8 "
           "score; their Attainment 8 is in the file. Pupils who sat key stage 2 outside the borough carry the local "
           "authority number and URN of the school where they sat it."),
         P("A school's URN changes when it converts to an academy. The file keeps the URN the school had when the "
           "pupil sat the tests; the borough's establishment register lists each academy's predecessor URN."),
         P("Absence covers the autumn and spring terms of year 11 only: the summer term census is not collected for "
           "pupils in year 11."),
         P("Data sharing", "h2"),
         P("Shared with %s under the data sharing agreement of March 2026 for school improvement planning across the "
           "trust's academies. Do not publish figures for groups of fewer than six pupils." % K.TRUST)]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_measures(path):
    S = styles("Sans", RUST)
    doc, fr = _doc(path, "Key stage 4 measures 2026: a summary for the trust", K.PEOPLE["data"], "KS4 measures",
                   K.TRUST, "Data and Assessment, September 2026")
    P = lambda t, s="body": Paragraph(t, S[s])
    pts = [["Technical award grade", "Points"], ["Level 2 Distinction*", "8.5"], ["Level 2 Distinction", "7"],
           ["Level 2 Merit", "5.5"], ["Level 2 Pass", "4"], ["Level 1 Distinction*", "3"], ["Level 1 Distinction", "2"],
           ["Level 1 Merit", "1.5"], ["Level 1 Pass", "1.25"], ["Unclassified", "0"]]
    f = [P("Key stage 4 measures 2026", "h1"),
         P("%s, Data and Assessment. A summary of the Department's key stage 4 performance measures guidance for the "
           "2026 results, for academies' data leads. %s, Head of Data and Assessment, September 2026." % (
             K.TRUST, K.PEOPLE["data"]), "meta"),
         P("Who is counted", "h2"),
         P("An academy's 2026 cohort is its pupils at the end of key stage 4: those in year 11 on its roll at the "
           "January 2026 census. Results a pupil achieved in any examination series during key stage 4, in year 10 or "
           "year 11, count toward the cohort's measures."),
         P("Attainment 8", "h2"),
         P("Attainment 8 adds a pupil's points in eight subjects, in three elements:"),
         P("(a)&nbsp;&nbsp;English: the higher of English language and English literature, double weighted only if the "
           "pupil took both; the other can count in the open element.", "clause"),
         P("(b)&nbsp;&nbsp;Mathematics, double weighted.", "clause"),
         P("(c)&nbsp;&nbsp;The EBacc element: the three highest-scoring of the sciences (biology, chemistry, physics, "
           "combined science, computer science), history, geography and languages. Combined science counts as two "
           "qualifications, each scored at the mean of its two grades.", "clause"),
         P("(d)&nbsp;&nbsp;The open element: the three highest-scoring of the remaining qualifications, including the "
           "second English, any EBacc subject not used in (c), other GCSEs and approved technical awards.", "clause"),
         P("A GCSE graded 9 to 1 scores its grade; U scores nothing. Technical awards score as follows:"),
         _table(S, pts, [60 * mm, 25 * mm], right=(1,)),
         P("Where two qualifications share a discount code only one counts. For English, mathematics and the EBacc "
           "subjects it is the pupil's first entry (the earliest series), whatever a later entry achieved; otherwise "
           "it is the higher-scoring. An academy's average Attainment 8 is the total of its pupils' Attainment 8 over "
           "the number of pupils in its cohort."),
         P("EBacc entry", "h2"),
         P("A pupil is entered for the EBacc if they took English language and English literature, mathematics, "
           "combined science or two of biology, chemistry, physics and computer science, history or geography, and a "
           "language. The entry rate is the share of the cohort entered.")]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)


def write_attnote(path):
    S = styles("Sans", NAVY)
    doc, fr = _doc(path, "Attendance reporting 2025/26", K.PEOPLE["data"], "Attendance reporting", K.TRUST,
                   "Data and Assessment, attendance reporting note 2025/26")
    P = lambda t, s="body": Paragraph(t, S[s])
    f = [P("Attendance reporting, 2025/26", "h1"),
         P("%s, Data and Assessment. How the trust counts attendance for its board, following the Department's "
           "methodology for school absence statistics. %s, September 2026." % (K.TRUST, K.PEOPLE["data"]), "meta"),
         P("Measures", "h2"),
         P("A pupil is persistently absent if they missed 10 per cent or more of their possible sessions, and severely "
           "absent if they missed 50 per cent or more. Sessions missed are authorised and unauthorised absence; "
           "approved educational activity counts as attendance. Sessions coded as not possible (pupils not required to "
           "attend, unable to attend in exceptional circumstances, not yet on roll, or planned closures) are not in "
           "sessions possible."),
         P("Who is counted, and where", "h2"),
         P("Each academy counts its own pupils' sessions while they are on its roll. A pupil who moved between "
           "academies during the year counts at each academy for the sessions they spent on its roll, their absence "
           "there judged against their possible sessions there. A rate is the number of the academy's pupils "
           "persistently (or severely) absent over the number of pupils it counts."),
         P("Pupils in year 11 count for the autumn and spring terms only, as in the Department's full-year measure: "
           "most have left by the summer half-term and the remainder are on study leave."),
         P("Source", "h2"),
         P("The trust's data warehouse, which takes each academy's registers nightly. The board's figures are taken "
           "from the extract of 18 September 2026, which holds every half-term of 2025/26 for every pupil on any "
           "academy's roll during the year.")]
    doc.build(f, onFirstPage=fr, onLaterPages=fr)
