"""The pack's documents: the foundation's criteria for the FY2027 Decision Coaching Grants, the collaborative's data
guide to the 2025 extracts, and the pack's contents."""
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
                            "sits with the hospital's counsellors as they work their queues, monthly case reviews, and "
                            "a refresher on the hospital's own financial-assistance policy." % K.COLLAB),
          _clause(S, "1.2", "The board approves the number of grants with the FY2027 budget on 12 March 2027. Each "
                            "grant is $%s for twelve months, whatever the hospital's size." % format(GRANT, ",")),
          _clause(S, "1.3", "The program team applies these criteria to the collaborative's 2025 extracts."),
          Paragraph("2. Which hospitals qualify", S["h2"]),
          _clause(S, "2.1", "A hospital qualifies when its financial-assistance counsellors are at least six "
                            "percentage points less likely to approve an application right after approving the "
                            "application before it than right after denying it."),
          _clause(S, "2.2", "This is measured on the hospital's 2025 determinations: every approval and every denial a "
                            "counsellor recorded at the hospital from 1 January to 31 December 2025 (the hospital's "
                            "local date), first determinations and determinations on reconsideration alike. A pend or "
                            "a withdrawal is not a determination. The nightly presumptive screening is not a "
                            "counsellor, and its approvals are not counted."),
          _clause(S, "2.3", "A determination is compared by the determination the same counsellor recorded just "
                            "before it on the same working day, in the order the counsellor recorded them. A "
                            "counsellor's first determination of a working day follows none."),
          _clause(S, "2.4", "Likely refers to the counsellor's chance of approving the application in hand. That "
                            "chance moves with the applications a working day brings, from a day of presumptive "
                            "Medicaid referrals to a day of mailed balances, so the comparison is between the chance "
                            "right after an approval and right after a denial among the same working day's "
                            "applications; the difference between one day's applications and another's is not part "
                            "of it."),
          _clause(S, "2.5", "An approval is a determination that reduces what the patient owes under the hospital's "
                            "financial-assistance policy, in full or in part; a denial reduces nothing."),
          _clause(S, "2.6", "Each hospital is measured in percentage points and compared with six unrounded."),
          Paragraph("3. Terms", S["h2"])]
    rows = [["Term", "Meaning"],
            ["Counsellor", "A member of the hospital's financial-assistance team who records determinations under "
                           "the counsellor's own user ID."],
            ["Determination", "An approval or a denial of an application for financial assistance."],
            ["Reconsideration", "A further determination on an application, made once the applicant supplies what "
                                "was missing."],
            ["Working day", "A day on which the counsellor recorded at least one determination, by the hospital's "
                            "local date."],
            ["Chance of approving", "The probability that the counsellor approves an application of the kind the "
                                    "working day brings."],
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
def write_guide(path, counts):
    S = styles("Serif", SLATE)
    title = "%s: data guide to the 2025 extracts" % K.COLLAB
    doc = _doc(path, title, K.COLLAB)
    F = K.FILES
    st = [Paragraph(title, S["h1"]),
          Paragraph("Prepared by the foundation's data team for the program staff &nbsp;|&nbsp; 14 April 2026", S["meta"]),
          Paragraph("1. Where the extracts come from", S["h2"]),
          Paragraph("Each member hospital's billing system sends its financial-assistance log to one of three regional "
                    "hubs, and each hub's consolidation tool writes one extract for its hospitals: the Puget hub (%s), "
                    "the Willamette hub (%s) and the Columbia hub (%s). Lundgren Regional Hospital (H23) moved from the "
                    "Columbia hub to the Puget hub when its billing converted on 2 June 2025: its rows to 30 May 2025 "
                    "are in the Columbia extract and its rows from 2 June 2025 in the Puget extract. Its counsellors "
                    "kept working under new user IDs (%s); open applications kept their numbers. The adjustments and "
                    "the patient accounts come from the collaborative's warehouse for all 31 hospitals."
                    % (F["puget"], F["willamette"], F["columbia"], F["crosswalk"]), S["body"]),
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
                         ["denial_reason", "For a denial, the reason code (section 5)."]], [1.9, 4.8]))
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
                         ["DENY_RSN", "For a denial, the reason code (section 5)."]], [1.9, 4.8]))
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
                         ["reason", "For a denial, the reason code (section 5)."]], [1.9, 4.8]))
    st.append(Paragraph("5. Denial reason codes", S["h2"]))
    st.append(Paragraph("All three hubs use the collaborative's common list:", S["body"]))
    st.append(_table(S, [["Code", "Reason"], ["1", "Documents not received"], ["2", "Income above the policy limit"],
                         ["3", "Other coverage available"], ["4", "Outside the service area"]], [0.8, 5.9]))
    st.append(Paragraph("6. The presumptive screening", S["h2"]))
    st.append(Paragraph("Each hub runs a presumptive screening at about 02:00 on weekday mornings against accounts with "
                        "a self-pay balance, using public-program enrolment. An account that matches is approved and "
                        "its balance written off in full, with no application from the patient; the approval is "
                        "recorded under the hub's system user.", S["body"]))
    st.append(Paragraph("7. Assistance adjustments (%s)" % F["ledger"], S["h2"]))
    st.append(Paragraph("Every financial-assistance adjustment posted through 31 March 2026 on an application "
                        "determined in 2025.", S["body"]))
    st.append(_table(S, [["Column", "Contents"],
                         ["adjustment_id", "The warehouse's number for the adjustment line."],
                         ["hospital_code, application_id, account_number", "The hospital, the application and the "
                                                                           "patient account the line posts to."],
                         ["posted_date", "The date the adjustment posted."],
                         ["adjustment_code", "FAWO a financial-assistance write-off; FAWR a reversal of a "
                                             "financial-assistance write-off, for example when Medicaid later pays "
                                             "the account."],
                         ["amount", "Amount in US dollars."]], [2.4, 4.3]))
    st.append(Paragraph("8. Patient accounts (%s)" % F["accounts"], S["h2"]))
    st.append(Paragraph("Every account the adjustments post to: account_number, hospital_code, guarantor_id, "
                        "service_date (the first service date on the account) and patient_balance (what the patient "
                        "owed on the account when the application was determined, US dollars).", S["body"]))
    st.append(Paragraph("9. Other files", S["h2"]))
    st.append(Paragraph("%s lists the member hospitals with their hubs and policy limits. %s is the collaborative's "
                        "2025 patient-experience survey by payer group. %s is each hospital's charity care as filed "
                        "with its state for its own fiscal year 2025, at full charges."
                        % (F["hospitals"], F["survey"], F["state"]), S["body"]))
    st.append(Paragraph("10. Rows", S["h2"]))
    st.append(_table(S, [["File", "Rows"]] + [[F[k], format(counts[k], ",")] for k in
                                               ("puget", "willamette", "columbia", "ledger", "accounts")],
                     [4.6, 1.0], right=(1,)))
    fr = _frame(K.COLLAB, "Data guide, 2025 extracts", "Serif")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


def write_contents(path, items):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("%s: Decision Coaching Grants FY2027, files for the program team\n\n" % K.FOUNDATION)
        for name, desc in items:
            f.write("%s\n    %s\n" % (name, desc))
