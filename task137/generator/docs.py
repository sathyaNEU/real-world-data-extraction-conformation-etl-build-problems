"""The pack's documents: the statement of work with its schedules, the eight quarterly campaign briefs, the retention
procedure, the block-order thread, the extract notes, and the two background files (the treasury funding outlook and
Harbourline's 2027 staffing proposal)."""
from __future__ import annotations

import datetime as dt
import email.utils
from email.message import EmailMessage
from email.policy import SMTP

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Mm
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf"),
               ("LiberationSans", "liberation/LiberationSans-Regular.ttf"),
               ("LiberationSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
ARIAL, ARIAL_B = "LiberationSans", "LiberationSans-Bold"
INK = colors.HexColor("#1f2428")
GREY = colors.HexColor("#5b6670")
NAVY = colors.HexColor("#173a5e")
GREEN = colors.HexColor("#2f6b3a")
RULE = colors.HexColor("#a7b0b8")

BODY = ParagraphStyle("body", fontName=SANS, fontSize=10, leading=13.2, textColor=INK, spaceAfter=4.5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=24, firstLineIndent=-24)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15, leading=19, textColor=NAVY, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName=SANS, fontSize=10, leading=13, textColor=GREY, spaceAfter=9)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=11, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
NOTE = ParagraphStyle("note", fontName=SANS_I, fontSize=8.6, leading=11, textColor=GREY, spaceBefore=3)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=9, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)
# Harbourline's house style (its own documents)
HB_BODY = ParagraphStyle("hbody", fontName=ARIAL, fontSize=9.4, leading=12.6, textColor=INK, spaceAfter=4.5)
HB_CL = ParagraphStyle("hcl", parent=HB_BODY, leftIndent=26, firstLineIndent=-26)
HB_H1 = ParagraphStyle("hh1", fontName=ARIAL_B, fontSize=14, leading=18, textColor=GREEN, spaceAfter=2)
HB_H1S = ParagraphStyle("hh1s", fontName=ARIAL, fontSize=9.4, leading=12.4, textColor=GREY, spaceAfter=9)
HB_H2 = ParagraphStyle("hh2", fontName=ARIAL_B, fontSize=10.4, leading=13.4, textColor=INK, spaceBefore=7,
                       spaceAfter=3)
HB_CELL = ParagraphStyle("hcell", fontName=ARIAL, fontSize=8.6, leading=10.6, textColor=INK)
HB_CELLB = ParagraphStyle("hcellb", parent=HB_CELL, fontName=ARIAL_B)


def _footer(left, right, font=SANS):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths, head=1, hb=False):
    c, cb = (HB_CELL, HB_CELLB) if hb else (CELL, CELLB)
    data = [[Paragraph(str(x), cb if i < head else c) for x in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=head, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, head - 1), (-1, head - 1), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.8), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3)]))
    return t


def nzd(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


# ------------------------------------------------------------------------------------------------------------------
# Statement of work
def write_sow(path):
    P = lambda t: Paragraph(t, HB_BODY)
    C = lambda no, t: Paragraph("%s&nbsp;&nbsp;%s" % (no, t), HB_CL)
    s = [Paragraph("Harbourline Contact Services Limited", HB_H1S),
         Paragraph("Statement of Work %s: term deposit maturity calls" % W.SOW_REF, HB_H1),
         Paragraph("Between Kaimai Building Society (the Society) and Harbourline Contact Services Limited "
                   "(Harbourline), under the Master Services Agreement dated 14 October 2024. Signed 22 November 2024.",
                   HB_H1S)]
    s.append(Paragraph("1 Term", HB_H2))
    s.append(C("1.1", "This statement of work runs from 1 December 2024 to 31 December 2027. Its schedules apply to "
                      "every quarterly campaign in that period."))
    s.append(Paragraph("2 Services", HB_H2))
    s.append(C("2.1", "Harbourline calls the holders of the term deposits the Society releases to it, to confirm or "
                      "take their instructions for the deposit's maturity, using the Society's script and the campaign "
                      "brief for the quarter."))
    s.append(C("2.2", "A campaign covers the term deposits on the Society's list for one calendar quarter of maturity "
                      "dates."))
    s.append(Paragraph("3 Cases", HB_H2))
    s.append(C("3.1", "The Society releases each case in its daily release file 21 days before the deposit's maturity "
                      "date, with the holder's callable numbers in the order the Society holds them."))
    s.append(C("3.2", "The Society withdraws a case in its daily withdrawal file when the holder gives instructions "
                      "through another channel. Harbourline stops dialling a withdrawn case from the next dialling day."))
    s.append(C("3.3", "A case closes at the first conversation with the holder, when every callable number is closed "
                      "under schedule 1, when it is withdrawn, or on the maturity date."))
    s.append(Paragraph("4 Reporting", HB_H2))
    s.append(C("4.1", "Harbourline delivers the dial log and the case close-outs for each campaign within 15 business "
                      "days of the end of the campaign's quarter, in the layouts in schedule 4."))
    s.append(Paragraph("Schedule 1: Dialling", HB_H2))
    s.append(C("1.1", "Dialling days are Monday to Friday, except New Zealand public holidays, Wellington Anniversary "
                      "Day and Harbourline's close-down from 24 December to 3 January. Calls are made between 9.00 am "
                      "and 8.00 pm New Zealand time."))
    s.append(C("1.2", "Each callable number is dialled at most once in a dialling day, in the order released."))
    s.append(C("1.3", "A number is closed after six dials that do not reach the holder, or at once if it is "
                      "disconnected or answered by someone other than the holder."))
    s.append(C("1.4", "Agents do not leave voicemail messages."))
    s.append(Paragraph("Schedule 2: Charges", HB_H2))
    s.append(C("2.1", "Agent time is billed per event at the minutes below, totalled for the month and invoiced in "
                      "agent-hours at the block rate."))
    s.append(_table([["Event", "Codes (schedule 3)", "Agent-minutes"],
                     ["A dial that does not reach the holder", ", ".join(W.NOT_REACHED), "1.5"],
                     ["A conversation with the holder", ", ".join(W.CONVERSATION), "8"],
                     ["A conversation in which the holder says they intend to withdraw or move the funds and the "
                      "agent takes them through the retention offer", ", ".join(W.RETENTION), "22"]],
                    [88 * mm, 42 * mm, 30 * mm], hb=True))
    s.append(Spacer(1, 4))
    s.append(C("2.2", "The Society books a block of agent-hours, in multiples of 250, for each quarter's campaign by "
                      "the 20th day of the second month before the quarter. The block is payable in full whether or not "
                      "it is used."))
    s.append(C("2.3", "Hours used beyond the block are invoiced at the block rate plus 35 per cent."))
    s.append(C("2.4", "The block rate is NZ$64.80 an agent-hour, indexed each 1 January to the Consumers Price Index."))
    s.append(Paragraph("Schedule 3: Disposition codes", HB_H2))
    s.append(_table([["Code", "Meaning"]] + [[k, v] for k, v in W.CODES.items()], [18 * mm, 142 * mm], hb=True))
    s.append(Paragraph("Schedule 4: Files", HB_H2))
    s.append(C("4.1", "Release file (from the Society): campaign, account, maturity date, release date, and up to four "
                      "callable numbers with their types."))
    s.append(C("4.2", "Dial log (from Harbourline): one row per dial, with the case reference, the Society's account "
                      "reference, the dial's number within the case, the time dialled (UTC), the number dialled, its "
                      "slot, the disposition code, talk seconds and the agent."))
    s.append(C("4.3", "Case close-out (from Harbourline): one row per released case, with its release and close dates, "
                      "the reason it closed (CONVERSATION, EXHAUSTED or WITHDRAWN), the dials made and the last "
                      "disposition."))
    doc = _doc(path, "SOW %s term deposit maturity calls" % W.SOW_REF, "Harbourline Contact Services")
    f = _footer("Harbourline Contact Services Limited  |  Commercial in confidence", W.SOW_REF, ARIAL)
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ------------------------------------------------------------------------------------------------------------------
# Campaign briefs
def write_brief(path, q, listed, issued, draft=False):
    start, end = W.q_start(q), W.q_end(q)
    first_rel, last_rel = start - dt.timedelta(days=21), end - dt.timedelta(days=21)
    label = W.q_label(q)
    s = [Paragraph("Kaimai Building Society  |  Term Deposits", H1S),
         Paragraph("Campaign brief: term deposits maturing %s%s" % (label, " (draft)" if draft else ""), H1),
         Paragraph("For Harbourline Contact Services. Issued %s. Campaign TDR-%s." % (nzd(issued), q), H1S)]
    s.append(Paragraph("1 The campaign", H2))
    s.append(Paragraph("The list for this campaign was cut on %s and holds %s term deposits maturing from %s to %s. "
                       "Cases will be released daily from %s to %s, each 21 days before its maturity date." % (
                           nzd(W.CUTS[q]), "{:,}".format(listed), nzd(start), nzd(end), nzd(first_rel),
                           nzd(last_rel)), BODY))
    s.append(Paragraph("2 What the agent confirms", H2))
    s.append(Paragraph("After verifying the holder, the agent tells them the deposit's maturity date and that, unless "
                       "they instruct otherwise, it will reinvest for the same term at the Society's posted rate on that "
                       "date (the rates for this quarter are in section 3), and takes any instructions: reinvest as is, "
                       "change the term or amount, or pay out to a nominated account.", BODY))
    s.append(Paragraph("3 Reinvestment rates for deposits maturing this quarter", H2))
    rates = [W.card(q, t) for t in W.TERMS]
    if q < "2026Q1":
        s.append(_table([["Term", "Rate (% p.a.)"]] + [["%d year%s" % (t, "" if t == 1 else "s"), "%.2f" % r]
                                                       for t, r in zip(W.TERMS, rates)], [40 * mm, 30 * mm]))
    else:
        s.append(_table([["Term", "1 yr", "2 yrs", "3 yrs", "4 yrs", "5 yrs"],
                         ["Rate % p.a."] + ["%.2f" % r for r in rates]],
                        [32 * mm] + [22 * mm] * 5))
    s.append(Paragraph("Posted rates as approved by ALCO for %s. Interest is paid as the deposit specifies; the rate "
                       "applies to a reinvestment for the same term." % label, NOTE))
    s.append(Paragraph("4 Retention offer", H2))
    s.append(Paragraph("If the holder says they intend to withdraw or move the funds, the agent takes them through the "
                       "retention offer: up to 0.25 percentage points above the rate in section 3 for a one- or two-year "
                       "reinvestment and up to 0.15 for three to five years. Requests above that go to the Society's "
                       "pricing desk while the holder is on the line.", BODY))
    s.append(Paragraph("5 Contacts", H2))
    s.append(Paragraph("Society: %s, Term Deposits Product Manager. Harbourline: %s, Account Manager." % (
        W.PEOPLE["product"], W.PEOPLE["vendor"]), BODY))
    doc = _doc(path, "Campaign brief TDR-%s" % q, W.PEOPLE["product"])
    f = _footer("Kaimai Building Society  |  Confidential", "TDR-%s brief" % q)
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ------------------------------------------------------------------------------------------------------------------
# Harbourline's 2027 staffing proposal (background)
def write_proposal(path):
    P = lambda t: Paragraph(t, HB_BODY)
    s = [Paragraph("Harbourline Contact Services Limited", HB_H1S),
         Paragraph("Kaimai Building Society: 2027 service and staffing proposal", HB_H1),
         Paragraph("Prepared by %s (Workforce Planning) and %s (Account Manager), 9 October 2026." % (
             W.PEOPLE["wfm"], W.PEOPLE["vendor"]), HB_H1S)]
    s.append(Paragraph("1 Team", HB_H2))
    s.append(P("The Society's maturity calls are worked by a dedicated pod in our Palmerston North centre: a team leader, "
               "a quality coach and a pool of 14 to 24 licensed agents drawn from our retail banking bench, rostered "
               "against the quarter's block. Agents work the society's script and nothing else while rostered."))
    s.append(Paragraph("2 Shifts", HB_H2))
    s.append(_table([["Shift", "Hours (NZ time)", "Used for"],
                     ["Early", "8.30 am to 5.00 pm", "dialling from 9.00 am, case preparation"],
                     ["Late", "11.30 am to 8.00 pm", "evening dialling for working holders"],
                     ["Split", "9.00 am to 1.00 pm, 4.00 pm to 8.00 pm", "peak days in maturity clusters"]],
                    [28 * mm, 58 * mm, 74 * mm], hb=True))
    s.append(Paragraph("3 Capacity and commercial terms for 2027", HB_H2))
    s.append(P("We can staff up to 9,000 agent-hours a quarter on the Society's campaigns with four weeks' notice. The "
               "block rate for 2027 after the January index is NZ$66.10 an agent-hour; the minimum block is 750 "
               "hours. Hours beyond the block remain at the schedule 2.3 premium."))
    s.append(Paragraph("4 Quality", HB_H2))
    s.append(P("We score 2 per cent of recorded conversations each month against the Society's script and share the "
               "results at the monthly service review. We propose adding a second coach from April 2027 and moving the "
               "service review to the second Thursday of each month."))
    doc = _doc(path, "Kaimai 2027 service and staffing proposal", "Harbourline Contact Services")
    f = _footer("Harbourline Contact Services Limited  |  Commercial in confidence", "2027 proposal", ARIAL)
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ------------------------------------------------------------------------------------------------------------------
# The retention procedure (Word)
def write_procedure(path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = d.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)

    def head(t, size=12, color="173A5E"):
        p = d.add_paragraph()
        r = p.add_run(t)
        r.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)

    def clause(no, t):
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Mm(10)
        p.paragraph_format.first_line_indent = Mm(-10)
        p.paragraph_format.space_after = Pt(4)
        p.add_run("%s\t%s" % (no, t))

    t = d.add_paragraph()
    r = t.add_run("Kaimai Building Society")
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor.from_string("5B6670")
    head("Term Deposit Retention Procedure", 16)
    m = d.add_paragraph()
    m.add_run("Version 4, effective 3 August 2026. Owner: Term Deposits Product Manager. Approved: Head of Deposits.") \
        .italic = True
    head("1 Purpose")
    clause("1.1", "This procedure sets how the Society lists maturing term deposits for retention calls, releases them "
                  "to its contact centre, and books the contact centre's hours.")
    head("2 Scope")
    clause("2.1", "It applies to term deposits held by members. Kaimai Investment Certificates are serviced by the "
                  "branches and are not listed.")
    head("3 The list")
    clause("3.1", "The list for a quarter is cut on the first business day of the second month before the quarter and "
                  "is fixed from then. It holds the term deposits maturing in the quarter with a principal of "
                  "NZ$25,000 or more and no maturity instruction on file at the cut.")
    clause("3.2", "The list is cut from the core banking system by the Deposits analytics team and filed with the "
                  "quarter's campaign brief.")
    clause("3.3", "The list carries one deposit per member. Where a member has more than one, the largest is listed "
                  "and the agent covers the others in the same conversation.")
    head("4 Release")
    clause("4.1", "Each listed deposit is released to the contact centre 21 days before its maturity date, with the "
                  "holder's callable numbers.")
    clause("4.2", "A deposit is not released if the holder has given maturity instructions by then.")
    clause("4.3", "A number is callable if it is held for the member and is not on the Society's do-not-call "
                  "register. A deposit with no callable number is not released, and the member receives the maturity "
                  "letter only.")
    head("5 During the campaign")
    clause("5.1", "Every holder receives the maturity letter 28 days before maturity. At maturity a term deposit "
                  "reinvests for the same term at the posted rate in force on its maturity date unless the holder has "
                  "given other instructions (Term Deposit Terms and Conditions, clause 9.2).")
    clause("5.2", "Instructions taken through a branch, online banking or the Society's own phone line are sent to "
                  "the contact centre in the daily withdrawal file.")
    head("6 Booking")
    clause("6.1", "The Deposits team books with the contact centre the agent-hours the quarter's list is forecast to "
                  "need, rounded to the nearest 250 hours, by the date schedule 2 of the statement of work sets. The "
                  "forecast draws on every campaign the contact centre has closed under the statement of work.")
    clause("6.2", "The booking is approved by the Deposits Committee, chaired by the Head of Deposits, before it is "
                  "sent.")
    head("7 Records")
    clause("7.1", "The release log, the contact centre's dial logs and close-outs, and each campaign's brief and list are "
                  "kept for seven years.")
    d.core_properties.title = "Term Deposit Retention Procedure v4"
    d.save(path)


# ------------------------------------------------------------------------------------------------------------------
# The block-order thread (the context artifact)
def write_thread(path):
    msg = EmailMessage(policy=SMTP)
    msg["From"] = "%s <hazel.johnstone@kaimai.co.nz>" % W.PEOPLE["product"]
    msg["To"] = "%s <s.wallis@harbourline.co.nz>" % W.PEOPLE["vendor"]
    msg["Cc"] = "%s <stuart.waller@kaimai.co.nz>" % W.PEOPLE["head"]
    msg["Subject"] = "RE: January to March 2027 block order"
    msg["Date"] = "Wed, 04 Nov 2026 09:12:44 +1300"
    msg["Message-ID"] = "<KBS-20261104-091244-4471@kaimai.co.nz>"
    msg["In-Reply-To"] = "<HCS.2026-10-28.7c1e@harbourline.co.nz>"
    body = (
        "Thanks Suzanne.\n\n"
        "The January to March list was cut on Monday: 18,400 deposits. The Deposits Committee signs off the block on "
        "Tuesday 17 November and I'll send it to you by Friday 20 November, as schedule 2.2 has it, with the hours by "
        "month so Ashton can shape the roster.\n\n"
        "Regards,\n"
        "Hazel Johnstone\n"
        "Term Deposits Product Manager | Kaimai Building Society\n"
        "DDI 07 571 6620 | 51 Devonport Road, Tauranga\n\n"
        "-----Original Message-----\n"
        "From: Suzanne Wallis <s.wallis@harbourline.co.nz>\n"
        "Sent: Wednesday, 28 October 2026 3:41 pm\n"
        "To: Hazel Johnstone <hazel.johnstone@kaimai.co.nz>\n"
        "Subject: January to March 2027 block order\n\n"
        "Hi Hazel,\n\n"
        "Our rostering for January to March closes on 20 November, so we need the Society's block for the January to "
        "March campaign by then. If you can give us the hours by maturity month as well, Ashton will build the "
        "team around it; January is always the hardest month to roster with the close-down.\n\n"
        "The 2027 rate after the January index will be NZ$66.10 an hour. Our 2027 proposal went to Stuart on the "
        "9th.\n\n"
        "Kind regards,\n"
        "Suzanne Wallis\n"
        "Account Manager | Harbourline Contact Services\n"
        "Level 2, 33 The Square, Palmerston North 4410\n")
    msg.set_content(body)
    with open(path, "wb") as f:
        f.write(msg.as_bytes())


# ------------------------------------------------------------------------------------------------------------------
# The extract notes (the society's data dictionary for these extracts)
NOTES = """KAIMAI BUILDING SOCIETY  -  DEPOSITS ANALYTICS
Notes on the extracts for the January to March 2027 term deposit retention campaign
Prepared 3 November 2026

kbs_td_retention_lists_2025.csv
  The retention lists as cut for the four 2025 campaigns, from the core banking report used until January 2026.
  Campaign, Account No (bank-branch-account-suffix), Customer No, Product, Term (mths), Rate % (per cent a year),
  Principal (NZ$), Opened, Maturity (DD/MM/YYYY), Interest (payment frequency), Branch (member's home branch).

kbs_td_retention_lists_2026.csv, kbs_td_retention_list_2027Q1.csv
  The retention lists as cut for the 2026 campaigns and for January to March 2027, from the current core (upgraded
  12 January 2026). account (16 digits), customer_no, product_code, term_months, int_rate (decimal, a year),
  principal (NZ$), start_date, maturity_date, interest_freq (MAT at maturity, QTR, ANN, MTH), branch_code.

kbs_case_release_log_2025q1-2026q3.csv
  One row per listed deposit for each closed campaign. status RELEASED or NOT RELEASED; reason for a deposit not
  released. callable_1 to callable_4 and type_1 to type_4: the numbers released with the case, in the order sent,
  and their type (MOBILE, HOME, WORK).

kbs_contact_points_2026-11-02.csv
  Numbers held at the cut for the members on the January to March 2027 list. priority: the order the Society holds
  them in. number: as recorded (branch, online and legacy formats). recorded: date the number was recorded.

kbs_do_not_call_register_2026-11-02.csv
  Numbers members have asked the Society not to call. number (E.164). recorded: date the request was recorded.
  withdrawn: date the member withdrew the request, blank if it stands. source: where the request was taken.

kbs_td_account_events_2025-01_2026-10.csv
  Events from 1 January 2025 to 31 October 2026 on the term deposit accounts listed in those campaigns, and on term
  deposit accounts their holders opened in that period. customer_no: the account's first-named holder. event_type:
  OPEN, MATURE, REINVEST, PAYOUT, BREAK (withdrawal before maturity), CLOSE. For OPEN and REINVEST: term_months, rate
  (decimal) and maturity_date of the deposit as opened or reinvested.

kbs_member_transfers_2025-01_2026-10.csv
  Transfers of principal into and out of the accounts in the events extract, with the payment of their maturity
  proceeds, 1 January 2025 to 31 October 2026 (interest payments are not included). Society accounts are 16 digits;
  accounts at other banks are in their bank's format. narrative: as the payments system records it.

kbs_term_holdings_2026-11-02.csv
  Term deposits and investment certificates held in the core at the cut and maturing from 1 January to 30 June 2027.
  product: TD term deposit, KIC Kaimai Investment Certificate. principal (NZ$), int_rate (decimal), start_date,
  maturity_date.

kip_certificate_register_2026-06-30.csv
  Kaimai Investment Platform certificate register at close of business 30 June 2026. principal (NZ$), rate (per
  cent a year).

kip_migration_batches_2026.csv
  Investment platform to core migration, July to October 2026: batch, batch date, certificate, core account, status
  (MIGRATED, DEFERRED).
"""


def write_notes(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(NOTES.replace("\n", "\r\n"))


# ------------------------------------------------------------------------------------------------------------------
# Treasury funding outlook (background)
def write_outlook(path, td_balances):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "TD outlook"
    ws["A1"] = "Kaimai Building Society  -  Treasury"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Funding outlook FY2027 (April 2026 to March 2027): term funding, member term deposits and investment "
                "certificates with wholesale term deposits. Prepared for ALCO, 27 October 2026.")
    ws["A3"] = "Actuals to September 2026; forecast from October. NZ$ millions."
    hdr = ["Month", "Opening balance", "New money", "Maturities", "Reinvested", "Closing balance", "Basis"]
    for k, h in enumerate(hdr):
        c = ws.cell(row=5, column=k + 1, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F0")
    row = 6
    for m, (op, new, mat, rein, cl, basis) in td_balances:
        for k, v in enumerate([m, op, new, mat, rein, cl, basis]):
            c = ws.cell(row=row, column=k + 1, value=v)
            if 1 <= k <= 5:
                c.number_format = "#,##0.0"
        row += 1
    ws.cell(row=row + 1, column=1, value="Forecast months assume 82 per cent of maturing balances reinvest, the "
                                         "rate ALCO adopted in April 2026 for the liquidity plan.")
    ws.column_dimensions["A"].width = 12
    for col in "BCDEF":
        ws.column_dimensions[col].width = 15
    ws.column_dimensions["G"].width = 10
    ws.freeze_panes = "A6"
    wb.save(path)
