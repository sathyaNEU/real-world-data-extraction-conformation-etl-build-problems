"""The pack's documents: the foundation's criteria for the FY2027 Decision Coaching Grants, the collaborative's data
guide to the 2024 and 2025 extracts, and the pack's contents."""
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
INK, GREY, RULE = colors.HexColor("#1f2428"), colors.HexColor("#5d646a"), colors.HexColor("#b8bfc4")
TEAL = colors.HexColor("#1d5c63")
SLATE = colors.HexColor("#33475b")
GRANT = 64000


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(.8 * inch, letter[1] - .5 * inch, left)
        canvas.drawRightString(letter[0] - .8 * inch, letter[1] - .5 * inch, right)
        canvas.drawRightString(letter[0] - .8 * inch, .45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=.85 * inch, rightMargin=.85 * inch,
                             topMargin=.8 * inch, bottomMargin=.75 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ------------------------------------------------------------------------------------------- the criteria
FPL25 = (15650, 5500)


def write_criteria(path):
    S = styles("Sans", TEAL)
    title = "Decision Coaching Grants, FY2027: criteria"
    doc = _doc(path, title, K.FOUNDATION)
    st = [Paragraph(title, S["h1"]),
          Paragraph("%s &nbsp;|&nbsp; Program Committee &nbsp;|&nbsp; Approved 8 December 2026 &nbsp;|&nbsp; "
                    "Program: %s" % (K.FOUNDATION, K.COLLAB), S["meta"]),
          Paragraph("1. The grants", S["h2"]),
          _clause(S, "1.1", "From 1 July 2027 the foundation funds a year of decision coaching for the "
                            "financial-assistance team of each %s member hospital these criteria select: a coach who "
                            "works with the hospital's counsellors on assessing applications under the collaborative's "
                            "income standard, monthly case reviews, and a refresher on the hospital's own "
                            "financial-assistance policy." % K.COLLAB),
          _clause(S, "1.2", "The board approves the number of grants with the FY2027 budget on 12 March 2027. Each "
                            "grant is $%s for twelve months, whatever the hospital's size." % format(GRANT, ",")),
          _clause(S, "1.3", "The program team applies these criteria to the collaborative's 2024 and 2025 extracts."),
          Paragraph("2. Which hospitals qualify", S["h2"]),
          _clause(S, "2.1", "A hospital qualifies when at least six percent of the applications its counsellors "
                            "decided in 2025 from households within the free-care limit left the household owing more "
                            "than half of its balance."),
          _clause(S, "2.2", "The applications are those a counsellor decided on first review from 1 January to "
                            "31 December 2025, by the hospital's local date: each application's first approval or "
                            "denial. A reconsideration, a pend or a withdrawal is not a first review, and the nightly "
                            "presumptive screening is not a counsellor. A household that applied more than once counts "
                            "once for each application."),
          _clause(S, "2.3", "A household is within the free-care limit when its income over the twelve full calendar "
                            "months before the month in which it applied was no more than 200 percent of the 2025 "
                            "federal poverty guideline for its size (section 3). This is the household's income as the "
                            "collaborative's income standard counts it from 1 January 2026."),
          _clause(S, "2.4", "A decision leaves the household owing more than half of its balance when it denies the "
                            "application, for any reason, or approves it at a 25 percent discount."),
          _clause(S, "2.5", "Each hospital's share is measured in percent of its applications from households within "
                            "the limit and compared with six unrounded."),
          Paragraph("3. The free-care limit", S["h2"])]
    rows = [["Household size", "2025 federal poverty guideline", "Free-care limit (200 percent)"]]
    for n in range(1, 9):
        g = FPL25[0] + FPL25[1] * (n - 1)
        rows.append([str(n), "$" + format(g, ","), "$" + format(2 * g, ",")])
    st.append(_table(S, rows, [1.5, 2.4, 2.4], right=(1, 2)))
    st.append(Spacer(1, 4))
    st.append(Paragraph("For each person over eight, add $5,500 to the guideline and $11,000 to the limit.", S["body"]))
    st.append(Paragraph("4. Terms", S["h2"]))
    rows = [["Term", "Meaning"],
            ["Counsellor", "A member of the hospital's financial-assistance team who decides applications under the "
                           "counsellor's own user ID."],
            ["Household", "The applicant and the people the application counts in the household."],
            ["Income", "The household's gross income from work, self-employment, benefits and other sources, before "
                       "deductions."],
            ["Balance", "What the patient owed on the accounts the application covers when it was decided."],
            ["Presumptive screening", "The nightly check of patient accounts against public-program enrolment, which "
                                      "approves assistance without an application."]]
    st.append(_table(S, rows, [1.6, 5.1]))
    st.append(Spacer(1, 8))
    st.append(Paragraph("Questions on these criteria go to %s, %s, %s." % (K.PEOPLE["requester"],
                                                                         K.PEOPLE["requester_title"], K.FOUNDATION),
                        S["meta"]))
    fr = _frame(K.FOUNDATION + " | Program Committee", "Decision Coaching Grants FY2027", "Sans")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------- the data guide
APPL = ("received_date", "household_size", "income_3mo", "work_type")


def write_guide(path, counts):
    S = styles("Serif", SLATE)
    title = "%s: data guide to the 2024 and 2025 extracts" % K.COLLAB
    doc = _doc(path, title, K.COLLAB)
    F = K.FILES
    st = [Paragraph(title, S["h1"]),
          Paragraph("Prepared by the foundation's data team for the program staff &nbsp;|&nbsp; 14 April 2026", S["meta"]),
          Paragraph("1. Where the extracts come from", S["h2"]),
          Paragraph("Each member hospital's billing system sends its financial-assistance log to one of three regional "
                    "hubs, and each hub's consolidation tool writes one extract for its hospitals: the Puget hub (%s), "
                    "the Willamette hub (%s) and the Columbia hub (%s). Each holds every row the hub recorded in 2024 "
                    "and 2025. Lundgren Regional Hospital (H23) moved from the Columbia hub to the Puget hub when its "
                    "billing converted on 2 June 2025: its rows to 30 May 2025 are in the Columbia extract and its rows "
                    "from 2 June 2025 in the Puget extract. Its counsellors kept working under new user IDs and its "
                    "guarantors were given Puget numbers (%s); applications and accounts kept their numbers. The "
                    "adjustments and the patient accounts come from the collaborative's warehouse for all 31 "
                    "hospitals." % (F["puget"], F["willamette"], F["columbia"], F["crosswalk"]), S["body"]),
          Paragraph("Every row about an application carries what the application recorded: the date the hospital "
                    "received it, the household's size, the main earner's work and the household's income as the "
                    "2025 policy assessed it. The policy counted the household's gross income in the three full "
                    "calendar months before the month the application was received, times four, as its yearly "
                    "income, and set the discount from it against the federal poverty guideline for the year the "
                    "application was received: the whole balance written off to 200 percent of the guideline, 75 "
                    "percent of it to 250 percent, 50 percent to 300 percent and 25 percent to 400 percent; above 400 "
                    "percent the application was denied for income. Each hub's system records the income in its own "
                    "way (sections 2 to 4).", S["body"]),
          Paragraph("2. The Puget hub extract (%s)" % F["puget"], S["h2"])]
    st.append(_table(S, [["Column", "Contents"],
                         ["hospital_code", "The collaborative's hospital code (H01 to H31)."],
                         ["determination_id", "The hub's number for the row."],
                         ["application_id, guarantor_id", "The application, and the guarantor whose accounts it covers."],
                         ["user_id", "The counsellor's user ID; FA_PRESUMPTIVE for the presumptive screening."],
                         ["determined_at", "Date and time the row was recorded, local time at the hospital."],
                         ["determination_type", "INITIAL, RECONSIDERATION or PRESUMPTIVE."],
                         ["outcome", "APPROVED, DENIED, PENDED (waiting for documents) or WITHDRAWN."],
                         ["discount_pct", "For an approval, the percent of the patient's balance written off (100, 75, "
                                          "50 or 25)."],
                         ["denial_reason", "For a denial, the reason code (section 5)."],
                         ["received_date", "The date the hospital received the application."],
                         ["household_size", "The number of people the application counts in the household."],
                         ["income_3mo", "The household's gross income in the three full calendar months before the "
                                        "month the application was received, US dollars."],
                         ["work_type", "The main earner's work (section 6)."]], [1.9, 4.8]))
    st.append(Paragraph("3. The Willamette hub extract (%s)" % F["willamette"], S["h2"]))
    st.append(_table(S, [["Column", "Contents"],
                         ["HOSP_ID", "The collaborative's hospital code."],
                         ["DET_NO", "The hub's number for the row, in order within each hospital."],
                         ["APPL_NO, GUAR_NO", "The application and the guarantor."],
                         ["USER_ID", "The counsellor's user ID; BATCHPE for the presumptive screening."],
                         ["DET_DATE, DET_TIME", "Date (MM/DD/YYYY) and time the row was recorded, local time."],
                         ["RECON", "Y for a determination on reconsideration, otherwise N."],
                         ["RESULT", "A approved, D denied, P pended, X withdrawn."],
                         ["ADJ_PCT", "For an approval, the percent of the patient's balance written off."],
                         ["DENY_RSN", "For a denial, the reason code (section 5)."],
                         ["RCVD_DATE", "The date the hospital received the application (MM/DD/YYYY)."],
                         ["HH_SIZE", "The number of people in the household."],
                         ["ANN_INC", "The household's yearly income as the 2025 policy counted it (the three full "
                                     "calendar months before the month received, times four), whole US dollars."],
                         ["WORK_CD", "The main earner's work, by number (section 6)."]], [1.9, 4.8]))
    st.append(Paragraph("4. The Columbia hub extract (%s)" % F["columbia"], S["h2"]))
    st.append(_table(S, [["Column", "Contents"],
                         ["facility", "The collaborative's hospital code."],
                         ["app_ref, guarantor", "The application and the guarantor."],
                         ["seq", "The hub's number for the row."],
                         ["staff_key", "The counsellor's staff key; PE-AUTOSCREEN for the presumptive screening."],
                         ["ts_utc", "Date and time the row was recorded, in UTC (ISO 8601)."],
                         ["kind", "new, recheck (reconsideration) or screen (presumptive screening)."],
                         ["decision", "1 approved in full, 2 approved in part, 3 denied, 8 withdrawn, 9 pending "
                                      "documents."],
                         ["pct", "For an approval, the percent of the patient's balance written off."],
                         ["reason", "For a denial, the reason code (section 5)."],
                         ["rcvd", "The date the hospital received the application."],
                         ["hh", "The number of people in the household."],
                         ["inc_mo", "The household's average monthly gross income over the three full calendar months "
                                    "before the month received, US dollars."],
                         ["work", "The main earner's work, by short code (section 6)."]], [1.9, 4.8]))
    st.append(Paragraph("5. Denial reason codes", S["h2"]))
    st.append(Paragraph("All three hubs use the collaborative's common list:", S["body"]))
    st.append(_table(S, [["Code", "Reason"], ["1", "Documents not received"], ["2", "Income above the policy limit"],
                         ["3", "Other coverage available"], ["4", "Outside the service area"]], [0.8, 5.9]))
    st.append(Paragraph("6. The main earner's work", S["h2"]))
    st.append(Paragraph("Question 7 of the common application asks what kind of work the household's main earner "
                        "does; the applicant ticks one box.", S["body"]))
    st.append(_table(S, [["WORK_CD", "work", "work_type"]] + [[str(n), s, lbl] for _, n, s, lbl in K.WORK],
                     [1.0, 1.0, 4.7]))
    st.append(Paragraph("7. The presumptive screening", S["h2"]))
    st.append(Paragraph("Each hub runs a presumptive screening at about 02:00 on weekday mornings against accounts with "
                        "a self-pay balance, using public-program enrolment. An account that matches is approved and "
                        "its balance written off in full, with no application from the patient; the approval is "
                        "recorded under the hub's system user and carries no application fields.", S["body"]))
    st.append(Paragraph("8. Assistance adjustments (%s)" % F["ledger"], S["h2"]))
    st.append(Paragraph("Every financial-assistance adjustment the warehouse posted from 1 January 2025 through "
                        "31 March 2026.", S["body"]))
    st.append(_table(S, [["Column", "Contents"],
                         ["adjustment_id", "The warehouse's number for the adjustment line."],
                         ["hospital_code, application_id, account_number", "The hospital, the application the line "
                                                                           "posted under and the patient account."],
                         ["posted_date", "The date the adjustment posted."],
                         ["adjustment_code", "FAWO a financial-assistance write-off; FAWR a reversal of a "
                                             "financial-assistance write-off, for example when Medicaid later pays "
                                             "the account."],
                         ["amount", "Amount in US dollars."]], [2.4, 4.3]))
    st.append(Paragraph("9. Patient accounts (%s)" % F["accounts"], S["h2"]))
    st.append(Paragraph("Every account the adjustments post to: account_number, hospital_code, guarantor_id, "
                        "service_date (the first service date on the account) and patient_balance (what the patient "
                        "owed on the account before any financial-assistance write-off, US dollars).", S["body"]))
    st.append(Paragraph("10. Other files", S["h2"]))
    st.append(Paragraph("%s lists the member hospitals with their regions and hubs. %s is the collaborative's 2025 "
                        "patient-experience survey by payer group. %s is each hospital's charity care as filed with "
                        "its state for its own fiscal year 2025, at full charges."
                        % (F["hospitals"], F["survey"], F["state"]), S["body"]))
    st.append(Paragraph("11. Rows", S["h2"]))
    st.append(_table(S, [["File", "Rows"]] + [[F[k], format(counts[k], ",")] for k in
                                               ("puget", "willamette", "columbia", "ledger", "accounts")],
                     [4.6, 1.0], right=(1,)))
    fr = _frame(K.COLLAB, "Data guide, 2024 and 2025 extracts", "Serif")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


def write_contents(path, items):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("%s: Decision Coaching Grants FY2027, files for the program team\n\n" % K.FOUNDATION)
        for name, desc in items:
            f.write("%s\n    %s\n" % (name, desc))
