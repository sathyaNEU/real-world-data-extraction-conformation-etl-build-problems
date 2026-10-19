"""task249's documents: the integrity standard, the technical manual's chapter 4 extract, the equivalence study
report, the 2029 client plans workbook, the registers and the data dictionary."""
import datetime as dt
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import params as P
import postprocess

VAS, ABH, RAC, NAC, ISH = (P.PEOPLE[k] for k in ("head", "psychometrician", "client", "ops", "data"))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.5,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.2, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.9, leading=9.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EAF0"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _sections(s, sec, body, h2):
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))


# ------------------------------------------------------------------ the integrity standard
def standard(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "MAL-IS-04 Assessment integrity standard", VAS, "Assessment integrity standard, issue 4")
    s = [Paragraph("Medhavi Assessment Labs: Assessment integrity standard (MAL-IS-04)", h1),
         Paragraph("Issue 4, approved 24 April 2029, in force from the 2029 campus season. Owner: %s, Head of "
                   "Assessment Integrity. Supersedes issue 3 (May 2027)." % VAS, small), Spacer(1, 4)]
    sec = [
        ("1. Scope", [
            "This standard governs how Medhavi keeps the results it shares with client employers fit to use: who may "
            "sit MAT-R, how sittings are logged, how an item is kept from over-use, and, from the 2029 season, how a "
            "shortlisted candidate's online result is verified under proctoring before the client relies on it."]),
        ("2. Terms", [
            "<b>Candidate</b>: a person in the season's candidate register. <b>Booking</b>: a candidate's one MAT-R "
            "booking for the season; a candidate sits MAT-R once a season and the result is shared with every client "
            "account the candidate applies to. <b>Attempt</b>: one run of the test under a booking. <b>Genuine "
            "candidate</b>: a candidate who sat their own MAT-R. <b>Shortlisted</b>: invited by a client account to its "
            "selection day on the account's ranking of the results shared with it.",
            "Platform records (attempts, item administrations) carry UTC; client-facing exports carry IST. Estimates "
            "and standard errors are held in logits to three decimals; the scale score shown to clients is 50 plus 10 "
            "per logit, rounded to a whole number (technical manual, chapter 4)."]),
        ("3. Verification of shortlisted candidates (from the 2029 season)", [
            "<b>3.1 Verification.</b> Every candidate a client account shortlists sits MAT-V, the 12-item proctored "
            "adaptive test drawn from "
            "the secure bank, at the start of the account's selection day. The platform compares the candidate's "
            "MAT-R estimate with the MAT-V estimate.",
            "<b>3.2 Referral.</b> A candidate is referred to the integrity desk when the MAT-R estimate lies above the "
            "upper limit of the 95 per cent band around the MAT-V estimate, that is, above the MAT-V estimate plus "
            "1.96 times the MAT-V standard error, both in logits as the platform holds them. A referral is not a "
            "finding: the desk reviews the case and decides it.",
            "<b>3.3 Referral cap.</b> Over a season, the check at a client account may refer no more than 15 per cent "
            "of the genuine candidates the account shortlists. Before each season the desk takes each account's plan "
            "for the season, with an applicant pool like the account's previous season, and sets the account on MAT-V "
            "Extended (24 items) for the season where the share of its genuine shortlisted candidates the check would "
            "refer exceeds 15 per cent.",
            "<b>3.4</b> The cap protects candidates and clients from referrals that a genuine candidate cannot "
            "answer; it is not a target for the number of impersonations found."]),
        ("4. Item exposure", [
            "An item's weekly exposure is the share of the candidates who sat MAT-R in the test week who were shown "
            "the item. An item "
            "whose exposure exceeds 12 per cent in any test week of a season is rested for the next season and its "
            "replacement drawn from the pretest pool. Test weeks run Monday to Sunday, IST."]),
        ("5. Impersonation", [
            "A sitting found to have been taken by someone other than the registered candidate is an impersonation. "
            "Selection-day staff check photo identity against the booking; a suspected case is opened by the account's "
            "selection-day lead and decided by the integrity desk. A candidate may appeal a decision within 30 days. "
            "A confirmed impersonation voids the sitting's result for every account it was shared with."]),
        ("6. Interrupted attempts", [
            "An attempt interrupted by a connection or device failure may be restarted once within the test week. The "
            "restart is a new attempt under the same booking and starts its item selection afresh."]),
    ]
    _sections(s, sec, body, h2)
    doc.build(s, onFirstPage=_footer("MAL-IS-04, issue 4"), onLaterPages=_footer("MAL-IS-04, issue 4"))
    postprocess.scrub(path, P.PRODUCER, "2029-04-24T10:15:00")


# ------------------------------------------------------------------ technical manual, chapter 4 extract
def manual(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "MAT-R and MAT-V technical manual, chapter 4", ABH, "Scoring and precision")
    s = [Paragraph("MAT-R and MAT-V technical manual: chapter 4, scoring and precision (extract)", h1),
         Paragraph("Edition 2028.2, September 2028. Psychometrics team: %s." % ABH, small), Spacer(1, 4)]
    sec = [
        ("4.1 Banks and selection", [
            "MAT-R draws 16 items from an operational bank of 340 two-parameter logistic items in three content "
            "areas (numerical, verbal, abstract), taken in rotation. The first item is chosen at the typical level of "
            "the candidate's college tier; each later item is drawn at random from the five unused items of the due "
            "area that carry the most information at the running estimate. MAT-V draws 12 items, and MAT-V Extended "
            "24, from a separate secure bank of 228 items under the same rules; MAT-V is delivered only under "
            "proctoring.",
            "Both banks are dense between about -2 and +1 logit and hold fewer items above that."]),
        ("4.2 Estimates", [
            "The final estimate is the weighted likelihood estimate on the bank's logit scale, which stays finite for "
            "a candidate who answers every item correctly. The standard error reported with it is the inverse square "
            "root of the test information at the estimate. The client scale score is 50 plus 10 per logit, rounded to "
            "a whole number; the standard error in scale points is ten times the logit value."]),
        ("4.3 Conditional standard error", [
            "Table 4.3 gives the standard error at each ability, from the design simulations (20,000 simulees per "
            "point) that set the test lengths. Between the tabled points the standard error may be interpolated."]),
    ]
    _sections(s, sec, body, h2)
    grid = np.round(np.arange(-3.0, 3.01, 0.25), 2)
    rows = [["Ability (logit)", "MAT-R, 16 items", "MAT-V, 12 items", "MAT-V Extended, 24 items"]]
    for t in grid:
        rows.append(["%+.2f" % t, "%.3f" % P.se_online(t), "%.3f" % P.se_verify(t), "%.3f" % (P.se_verify(t) / np.sqrt(2.0))])
    s.append(_grid(rows, [34 * mm, 38 * mm, 38 * mm, 44 * mm], cell))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Standard errors in logits. Source: design simulations, September 2028.", small))
    doc.build(s, onFirstPage=_footer("MAT technical manual, chapter 4"), onLaterPages=_footer("MAT technical manual, chapter 4"))
    postprocess.scrub(path, P.PRODUCER, "2028-09-22T16:40:00")


# ------------------------------------------------------------------ the equivalence study report
def study_report(path, tab_gain, tab_ref, n_vol, n_att, r_corr):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "MAT-V equivalence study 2028", ABH, "Equivalence study report")
    s = [Paragraph("MAT-V equivalence study, October to December 2028", h1),
         Paragraph("Report EQ-2028-03, 19 January 2029. %s, psychometrics. For the integrity desk." % ABH, small),
         Spacer(1, 4)]
    sec = [
        ("Purpose", [
            "Before MAT-V is used at the 2029 selection days, the study checks that MAT-V and MAT-R report on one "
            "scale and measures the gain a second sitting brings, so that the integrity desk can read a difference "
            "between the two tests."]),
        ("Design", [
            "%s volunteers, final-year students at 14 partner colleges recruited through the colleges' placement "
            "cells after the 2028 season, sat MAT-R under supervision in their college laboratory between 16 and 27 "
            "October 2028 and MAT-V at a Medhavi centre after an interval fixed in advance (1, 2, 3, 7, 14, 21, 28, "
            "42, 56, 70 or 84 days). %s sat both tests; the others did not attend MAT-V. Both sittings were "
            "supervised, so every pair is a genuine candidate's." % (f"{n_vol:,}", f"{n_att:,}")]),
        ("Results", [
            "The two tests correlate at %.2f over the pairs. Table 1 gives the mean of MAT-V minus MAT-R by interval: "
            "the second sitting runs higher, most within the first days and fading over the following weeks." % r_corr]),
    ]
    _sections(s, sec, body, h2)
    rows = [["Interval (days)", "Pairs", "Mean MAT-V minus MAT-R (logit)"]] + tab_gain
    s.append(_grid(rows, [40 * mm, 30 * mm, 60 * mm], cell))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Table 2 applies the referral rule of MAL-IS-04 section 3.2 to the pairs, by interval band.", body))
    rows = [["Interval band", "Pairs", "Referred", "Share referred"]] + tab_ref
    s.append(_grid(rows, [40 * mm, 30 * mm, 30 * mm, 40 * mm], cell))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Source: equivalence study pairs (file mat_v_equivalence_study_2028.csv).", small))
    doc.build(s, onFirstPage=_footer("EQ-2028-03"), onLaterPages=_footer("EQ-2028-03"))
    postprocess.scrub(path, P.PRODUCER, "2029-01-19T11:05:00")


# ------------------------------------------------------------------ the 2029 client plans workbook
def plans(path, w):
    wb = Workbook()
    ws = wb.active
    ws.title = "2029 plans"
    ws["A1"] = "Client plans for the 2029 campus season"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Compiled by client services (%s) from the accounts' returns due 30 April 2029. Shortlist is the number of " \
               "candidates the account will invite to its selection day, ranked on MAT-R." % RAC
    ws.merge_cells("A2:I2")
    ws["A4"] = "Account"; ws.merge_cells("A4:C4")
    ws["D4"] = "2029 plan"; ws.merge_cells("D4:I4")
    hdr = ["Code", "Client", "Sector", "Selection format", "Campuses", "Expected applicants", "Shortlist",
           "Selection days", "Notes"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=5, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E6EAF0")
    fmt_txt = {"D1": "Day-one campus drive", "S": "First-company campus drive", "L": "Later campus drive",
               "C": "Assessment centre"}
    days = {"D1": "Day 3 of each campus's test week", "S": "Day 3 of each campus's test week",
            "L": None, "C": None}
    r = np.random.default_rng(P.SEED + 3)
    row = 6
    for code, name, sector, grp, mix, f28, f29, q29 in P.ACCOUNTS:
        a = w.acc[code]
        pl = w.plan[code]
        ncamp = sum(len(v) for v in a["cover"].values())
        if f29 == "L":
            d0 = dt.date(2029, 9, 3) + dt.timedelta(days=int(r.integers(0, 8)))
            sd = "%s to %s" % (d0.strftime("%d %B %Y").lstrip("0"), (d0 + dt.timedelta(days=int(r.integers(10, 18)))).strftime("%d %B %Y").lstrip("0"))
        elif f29 == "C":
            d0 = dt.date(2029, 10, 8) + dt.timedelta(days=int(r.integers(0, 15)))
            sd = "%s to %s (Bengaluru, Pune, Hyderabad)" % (d0.strftime("%d %B %Y").lstrip("0"), (d0 + dt.timedelta(days=int(r.integers(14, 30)))).strftime("%d %B %Y").lstrip("0"))
        else:
            sd = days[f29]
        note = ""
        if code == "NVK":
            note = "Includes the former Paisaghar Lending campus list (PGL in 2028)."
        if code == "VRD":
            note = "Moves from assessment centres to day-one campus drives in 2029."
        vals = [code, name, sector, fmt_txt[f29], ncamp, pl["expected"], pl["shortlist"], sd, note]
        for j, v in enumerate(vals, 1):
            ws.cell(row=row, column=j, value=v)
        row += 1
    widths = [8, 32, 24, 26, 10, 18, 11, 44, 52]
    for j, wdt in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.freeze_panes = "A6"
    cal = wb.create_sheet("Calendar")
    cal["A1"] = "2029 campus season calendar"
    cal["A1"].font = Font(bold=True, size=12)
    lines = [
        "MAT-R test weeks run in July 2029: each college's week begins on Monday 2, 9, 16 or 23 July, as in 2028 "
        "(college register). Candidates sit MAT-R once, on day 1 or day 2 of their college's week; a candidate who has "
        "applied to a day-one or first-company drive sits it in the campus lab on day 1.",
        "Day-one and first-company campus drives hold the selection day on day 3 of the campus's test week.",
        "Later campus drives and assessment centres hold their selection days on the dates in the plans sheet.",
        "MAT-V is sat at the start of the selection day, under proctoring (MAL-IS-04, section 3).",
    ]
    for k, t in enumerate(lines, 3):
        cal.cell(row=k, column=1, value=t)
        cal.cell(row=k, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    cal.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.scrub(path, P.FIRM, "2029-05-06T18:20:00")
    postprocess.finish_office(path, "2029-04-30T09:00:00Z", "2029-05-06T18:20:00Z", P.FIRM)
