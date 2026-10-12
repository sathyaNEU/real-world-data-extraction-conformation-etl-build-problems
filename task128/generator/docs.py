"""The pack's documents: the early-stage collections protocol (PDF), the credit policy's collections resourcing
chapter (DOCX), the 2027 collections budget request (XLSX), the extracts' field reference (DOCX) and the manifest."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import LETTER                                 # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import inch                                       # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

PROTOCOL = "Early_Stage_Collections_Protocol_Cards_v7.2.pdf"
POLICY = "Credit_Policy_CP-14_Collections_Resourcing_2026.docx"
BUDGET = "2027_Collections_Budget_Request.xlsx"
FIELDS = "Collections_Extracts_Field_Reference_2026-10.docx"
MANIFEST = "CMI_EXTRACT_REGISTER_20261009.csv"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Italic", FONT_DIR + "LiberationSans-Italic.ttf"))
SANS, SANS_B, SANS_I = "LiberationSans", "LiberationSans-Bold", "LiberationSans-Italic"
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#5a5a5a")
TEAL = colors.HexColor("#0d4f5c")
BODY = ParagraphStyle("body", fontName=SANS, fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=4.5)
PARA = ParagraphStyle("para", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=14, leading=18, textColor=TEAL, spaceAfter=2)
H1b = ParagraphStyle("h1b", fontName=SANS, fontSize=10.5, leading=14, textColor=INK, spaceAfter=8)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=10.6, leading=14, textColor=TEAL, spaceBefore=8, spaceAfter=3)
META = ParagraphStyle("meta", fontName=SANS_I, fontSize=8.6, leading=11, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)


def _frame(canvas, doc):
    canvas.saveState()
    canvas.setFont(SANS, 7.6)
    canvas.setFillColor(GREY)
    canvas.drawString(0.9 * inch, 0.55 * inch, "Ferncliffe Trust Bank  |  Collections Operations  |  Internal")
    canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Early-stage protocol, cards, v7.2  |  page %d" % doc.page)
    canvas.restoreState()


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEABOVE", (0, 0), (-1, 0), 0.8, INK),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.8, INK),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


def write_protocol(path):
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.9 * inch, title="Early-stage collections protocol, cards",
                            author="Collections Operations", subject="", creator="", producer="")
    s = [Paragraph("Early-stage collections protocol: credit cards, 30 days past due", H1),
         Paragraph("Version 7.2. Effective 6 January 2025. Owner: Director, Collections Operations. Replaces version 7.1 "
                   "(April 2024).", H1b)]
    P_ = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), PARA))
    s.append(Paragraph("1. Scope", H2))
    P_("1.1", "This protocol governs the first calls to consumer credit card accounts that reach 30 days past due. "
              "Business cards are worked by Commercial Collections and are outside it.")
    P_("1.2", "Accounts are worked at their servicing centre: Thunder Bay, Sudbury, Kingston, London or Winnipeg. "
              "Each centre has one early-stage team and its own campaign on the dialler.")
    s.append(Paragraph("2. The 30-day list", H2))
    P_("2.1", "Every billing cycle has a collections day, the cycle's business day of the month (cycle 01 on the first "
              "business day, cycle 19 on the nineteenth), on which its accounts that missed the payment due a month "
              "earlier reach 30 days past due. The bank's collections calendar sets the business days.")
    P_("2.2", "The card platform's overnight run writes the cycle's 30-day entries. An entry with a hold (an arrangement "
              "already in force, a dispute, an insolvency or consumer proposal, a deceased customer) stays off the list "
              "and is worked by the team that owns the hold.")
    P_("2.3", "The remaining entries load to the servicing centre's campaign before 07:30 in the platform's extract "
              "order. The order is not changed at the centre.")
    s.append(Paragraph("3. Working the list", H2))
    P_("3.1", "The team works the list from 08:00 to 20:00 local time in load order, with up to three attempts a "
              "record on the list day. Attempts after the first are made later in the day.")
    P_("3.2", "The campaign closes at 20:00. Each record keeps its final result for the day in the list export; a record "
              "the team has not reached when the campaign closes has no result.")
    P_("3.3", "Records are not carried to the next day's list. An account that is still delinquent at its next cycle date "
              "is worked by the 60-day team.")
    s.append(Paragraph("4. The call", H2))
    P_("4.1", "Verify the customer before discussing the account. Where the customer can bring the account current, "
              "take a promise to pay with its amount and date. Where they cannot, offer a payment arrangement of two to "
              "six instalments on the overdue balance and set it up during the call.")
    P_("4.2", "Where the customer asks to be called back, book the callback. A customer who calls back is put through "
              "to the team, and an arrangement agreed on that call is set up by the agent who takes it.")
    P_("4.3", "Record the result of every attempt with the dialler's result codes (Collections extracts field "
              "reference).")
    s.append(Paragraph("5. Letters", H2))
    P_("5.1", "The 30-day letter goes by post the next business day to every listed account the team did not reach "
              "as the right party.")
    s.append(Paragraph("6. Contact rules", H2))
    P_("6.1", "Calls are made between 08:00 and 20:00 in the customer's local time and never on a statutory holiday.")
    P_("6.2", "The dialler applies the bank's do-not-call file and its own number check to every campaign. It does "
              "not dial a record whose account is on the file or that has no diallable number.")
    P_("6.3", "No more than three attempts on an account on one day, across every campaign.")
    s.append(Paragraph("7. Quality and records", H2))
    P_("7.1", "The QA team places test calls to the dialler's test accounts each working day to check routing and "
              "recording. Test calls are logged under the QA campaign.")
    P_("7.2", "The dialler's list export and call detail, the card platform's delinquency history and "
              "the workforce log are kept for seven years.")
    s.append(Spacer(1, 6))
    s.append(Paragraph("Appendix. Teams and campaigns", H2))
    rows = [["Centre", "Code", "Campaign", "Calls in"]]
    for c, n, prov in W.CENTRES:
        rows.append([n, c, "ES30_%s" % c, "Eastern time" if prov == "ON" else "Central time"])
    s.append(_table(rows, [1.4 * inch, 0.7 * inch, 1.2 * inch, 1.6 * inch]))
    doc.build(s, onFirstPage=_frame, onLaterPages=_frame)


def _docx_base():
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: F401
    from docx.shared import Pt, RGBColor
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for name, size in (("Heading 1", 14), ("Heading 2", 11.5)):
        h = d.styles[name]
        h.font.name = "Calibri"
        h.font.size = Pt(size)
        h.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    return d


def write_policy(path):
    from docx.shared import Pt
    d = _docx_base()
    sec = d.sections[0]
    sec.header.paragraphs[0].text = "Ferncliffe Trust Bank  |  Credit Policy  |  CP-14 Collections Resourcing"
    sec.footer.paragraphs[0].text = "Approved by the Credit Risk Committee, 14 May 2026; the 2027 line in 6.5 added 6 October 2026. Next review May 2027."
    d.add_heading("CP-14 Collections Resourcing", level=1)
    p = d.add_paragraph("Chapter of the Credit Policy covering how collections capacity is planned and funded. "
                        "Sections 1 to 5 are summarised; section 6 is reproduced in full.")
    p.runs[0].italic = True
    for t, body in (
            ("1. Purpose", "Collections capacity is a credit cost. This chapter sets how it is planned, funded and "
                           "reviewed, so that capacity follows the losses it prevents."),
            ("2. Annual plan", "Collections Operations files a capacity plan with the annual budget, by team and "
                               "centre, in agent hours and accounts dialled."),
            ("3. Vendors", "Agency and recovery vendor contracts are governed by CP-17."),
            ("4. Tests", "Changes to call strategy are tested before roll-out where a test can be run; test design is "
                         "agreed with Credit Risk Analytics."),
            ("5. Reporting", "Contact rates, promises to pay and arrangements are reported monthly by centre.")):
        d.add_heading(t, level=2)
        d.add_paragraph(body)
    d.add_heading("6. New collections teams", level=2)
    for n, body in (
            ("6.1", "A request for a new collections team is decided by the Executive Committee on the case below, "
                    "filed with the budget."),
            ("6.2", "The case sizes, for each centre that could take the team, the rolls to 90 days past due the new "
                    "team's calls would have prevented on that centre's 30-day lists over the latest year of lists "
                    "whose rolls are known."),
            ("6.3", "A roll is a listed account that is 90 or more days past due on its cycle date two months after "
                    "its list day."),
            ("6.4", "The new team is sized at the accounts dialled a day the budget request rates it for."),
            ("6.5", "A team is funded only where its calls would have prevented at least its yearly cost divided by "
                    "the loss the bank books on a roll. For 2027 that is $1,183,000 over $1,705, rounded up to 694 rolls. Where "
                    "no centre reaches it, the budget line is returned."),
            ("6.6", "One new early-stage team may be funded for 2027.")):
        para = d.add_paragraph()
        r = para.add_run(n + "  ")
        r.bold = True
        para.add_run(body)
        para.paragraph_format.left_indent = Pt(28)
        para.paragraph_format.first_line_indent = Pt(-28)
    d.save(path)


def write_budget(path):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 requests"
    ws.append(["Collections Operations: 2027 budget request (filed 30 September 2026)"])
    ws.append(["Amounts in Canadian dollars, fully loaded"])
    ws.append([])
    ws.append(["Line", "Item", "Detail", "FTE", "Rated accounts dialled a day", "2027 cost", "Status"])
    lines = [
        ("C-01", "Early-stage team (new), centre to be decided", "8 agents and a team leader; CX2 dialler seats", 9, 400,
         1183000, "For decision under CP-14 s.6"),
        ("C-02", "Dialler licences, CX2", "renewal, 5 centres plus QA", None, None, 412600, "Committed"),
        ("C-03", "30-day and 60-day letters", "print and post, volume at 2026 rate", None, None, 286350, "Committed"),
        ("C-04", "Recoveries agency panel", "contingency fees, CP-17 panel", None, None, 1940000, "Committed"),
        ("C-05", "Quality team", "two QA analysts, test line", 2, None, 168900, "Committed"),
        ("C-06", "Workforce management", "scheduling tool licence", None, None, 54800, "Committed"),
    ]
    for ln in lines:
        ws.append(list(ln))
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in ws.iter_rows(min_row=5, max_row=4 + len(lines)):
        row[5].number_format = "#,##0"
        row[4].number_format = "#,##0"
    for i, w in enumerate([6, 38, 34, 6, 14, 12, 26]):
        ws.column_dimensions["ABCDEFG"[i]].width = w
    ws.freeze_panes = "A5"
    n = wb.create_sheet("Notes")
    n.append(["Notes"])
    n.append(["C-01 rating: the accounts a team of eight agents dials in a 08:00 to 20:00 shift at the protocol's three "
              "attempts a record, from Kingston's CX2.1 pacing study in March 2026."])
    n.append(["C-01 cost: eight agents at $104,600, a team leader at $129,700, nine CX2 seats at $8,300 and the "
              "centre's share of supervision and quality at $95,700."])
    n["A1"].font = Font(bold=True)
    n.column_dimensions["A"].width = 120
    wb.save(path)


def write_fields(path):
    from docx.shared import Pt
    d = _docx_base()
    sec = d.sections[0]
    sec.header.paragraphs[0].text = "Ferncliffe Trust Bank  |  Collections MI  |  Field reference"
    d.add_heading("Collections data extracts: field reference", level=1)
    p = d.add_paragraph("Collections MI, October 2026. Covers the extracts pulled on 9 October 2026 for the 2027 "
                        "capacity case.")
    p.runs[0].italic = True

    def table(rows, widths):
        t = d.add_table(rows=0, cols=len(rows[0]))
        t.style = "Table Grid"
        for i, r in enumerate(rows):
            cells = t.add_row().cells
            for j, v in enumerate(r):
                cells[j].text = str(v)
                for para in cells[j].paragraphs:
                    for run in para.runs:
                        run.font.size = Pt(9)
                        run.bold = i == 0
        for row in t.rows:
            for j, w in enumerate(widths):
                row.cells[j].width = Pt(w)
        d.add_paragraph()

    F = P.FILES
    d.add_heading(F["lists"], level=2)
    d.add_paragraph("Dialler list export. One row per account loaded to a centre's 30-day campaign on a list day, in "
                    "load order. An account loaded on two list days is two rows. Collections reporting counts an "
                    "account each day it is dialled.")
    table([["Field", "Description"],
           ["LIST_DT", "List day (the cycle's collections day)"],
           ["CENTRE_CD", "Servicing centre"],
           ["LIST_SEQ", "Position of the record in the day's load"],
           ["ACCT_NO", "Card account number (internal, 11 digits)"],
           ["CYCLE_CD", "Billing cycle, 01 to 19"],
           ["DPD", "Days past due at load"],
           ["BEH_SCORE", "Behaviour score at the cycle date"],
           ["ATTEMPTS", "Dial attempts on the list day"],
           ["RESULT_CD", "Final result of the record for the day (result codes below)"]], [120, 330])
    d.add_heading(F["calls"], level=2)
    d.add_paragraph("Dialler call detail, July 2025 to June 2026. One row per dial attempt, CALL_START in the centre's "
                    "local time. CAMPAIGN_ID is the dialler campaign the attempt was placed from. TALK_SEC is the "
                    "connected time with an agent or a recorded message; AGENT_ID is blank where no agent took the "
                    "call.")
    d.add_heading("Result codes", level=2)
    table([["Code", "Meaning", "Right-party contact"],
           ["RPC", "Right party contacted, no commitment", "Yes"],
           ["PTP", "Promise to pay taken", "Yes"],
           ["ARR", "Payment arrangement agreed", "Yes"],
           ["RTP", "Refused to pay", "Yes"],
           ["CBK", "Customer asked to be called back", "Yes"],
           ["NOA", "No answer", "No"],
           ["AR", "Answering machine, recorded message left", "No"],
           ["BSY", "Busy", "No"],
           ["WRN", "Wrong number or third party", "No"],
           ["DIS", "Number disconnected", "No"],
           ["DNC", "Not dialled: account on the do-not-call file", "No"],
           ["NDN", "Not dialled: no diallable number", "No"],
           ["(blank)", "No result: not reached before the campaign closed", "No"]], [50, 300, 100])
    d.add_heading(F["history"], level=2)
    d.add_paragraph("Card platform delinquency history. One row per account and cycle date on which the account was "
                    "past due, from the cycle date it reached 30 days past due (its 30-day entry, listed or held); no "
                    "row on a cycle date the account was current.")
    table([["Field", "Description"],
           ["PRODUCT_CD", "VCL Visa Classic, VGD Visa Gold, VIF Visa Infinite, VSD Visa Student, VUSD Visa US Dollar"],
           ["CYCLE_DT", "Cycle date (the cycle's collections day that month)"],
           ["DPD", "Days past due on the cycle date"],
           ["BAL_CAD", "Balance, Canadian dollars"],
           ["HOLD_CD", "On a 30-day entry, the hold that kept it off the list: ARR arrangement in force, DSP dispute, "
                       "INS insolvency or consumer proposal, DEC deceased; blank where the entry was listed"],
           ["STATUS_CD", "CO where the account was charged off on the cycle date"]], [120, 330])
    d.add_heading(F["worklog"], level=2)
    d.add_paragraph("Workforce and dialler log. One row per team and working day. LON-A and LON-B are London's two pods "
                    "until they merged on 2 September 2025; the first pod's row carries the records loaded to the "
                    "centre's campaign.")
    table([["Field", "Description"],
           ["DIALLER_VER", "Dialler platform version at the centre that day"],
           ["SEATS_STAFFED, AGENT_HRS", "Agents on the 30-day list and their scheduled hours"],
           ["ES30_RECORDS_LOADED", "Records loaded to the campaign"],
           ["ES30_ACCOUNTS_DIALLED", "Records dialled at least once"]], [120, 330])
    d.add_heading(F["arrangements"], level=2)
    d.add_paragraph("Arrangement system extract. One row per payment arrangement set up by an early-stage team, by "
                    "set-up date.")
    table([["Field", "Description"],
           ["ARR_REF", "Arrangement reference"],
           ["SETUP_DT, SETUP_AGENT", "Day and agent that set it up"],
           ["ARR_BAL", "Balance placed on the arrangement"],
           ["INSTALMENTS, FREQUENCY, FIRST_DUE_DT", "Schedule"],
           ["STATUS", "ACTIVE, COMPLETED or BROKEN at the pull"]], [120, 330])
    d.add_heading(F["rates"], level=2)
    d.add_paragraph("Treasury booking rates. One row per business day: Canadian dollars per US dollar.")
    d.add_heading(F["ls60"], level=2)
    d.add_paragraph("60-day campaign daily summary from the dialler platform. One row per centre and list day: records "
                    "loaded to the centre's 60-day campaign, accounts dialled, right-party contacts and promises to pay "
                    "as the platform counted them that day.")
    d.save(path)


def write_manifest(path, counts):
    F = P.FILES
    rows = [
        (F["lists"], "Collections MI (dialler platform)", "2026-10-09", counts["lists"], "30-day campaign lists, list days 2 Jan 2025 to 28 Sep 2026"),
        (F["calls"], "Collections MI (dialler platform)", "2026-10-09", counts["calls"], "dial attempts, 30-day and QA campaigns, July 2025 to June 2026"),
        (F["history"], "Card platform", "2026-10-09", counts["history"], "delinquency by cycle date for accounts with a 30-day entry January 2025 to September 2026, cycle dates to 8 Oct 2026"),
        (F["worklog"], "Workforce management", "2026-10-09", counts["worklog"], "seats, hours and campaign counts by team and working day"),
        (F["arrangements"], "Arrangement system", "2026-10-09", counts["arrangements"], "arrangements set up by the 30-day teams, January 2025 to September 2026"),
        (F["rates"], "Treasury", "2026-10-09", counts["rates"], "daily booking rates"),
        (F["ls60"], "Collections MI (dialler platform)", "2026-10-09", counts["ls60"], "60-day campaign daily summary"),
        (F["headcount"], "Human Resources", "2026-10-06", counts["headcount"], "collections workforce by centre and quarter"),
        (PROTOCOL, "Collections Operations", "2025-01-06", "", "protocol in force for the review year"),
        (POLICY, "Credit Risk", "2026-10-06", "", "CP-14 as approved May 2026, with the 2027 line in 6.5 added October 2026"),
        (BUDGET, "Collections Operations", "2026-09-30", "", "2027 budget request lines"),
        (FIELDS, "Collections MI", "2026-10-09", "", "field reference for these extracts"),
    ]
    rows.sort(key=lambda r: r[0].lower())
    rows = [(i + 1, r[0], r[1], r[2].replace("-", ""), r[3], r[4]) for i, r in enumerate(rows)]
    P.write_text(path, P._csv(rows, ["SEQ", "OBJECT_NAME", "SOURCE_SYSTEM", "PULL_DT", "RECORD_CT", "SCOPE_NOTE"]))
