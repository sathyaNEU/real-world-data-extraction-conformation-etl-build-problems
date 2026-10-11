"""Writers for the task181 workbooks and documents."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

import world as W

ORG = W.ORG


def _sheet(ws, title_lines, header, rows, widths, date_cols=(), text_cols=(), money_cols=(), freeze=True):
    for i, line in enumerate(title_lines, start=1):
        c = ws.cell(row=i, column=1, value=line)
        if i == 1:
            c.font = Font(bold=True, size=12)
    hr = len(title_lines) + 2
    for j, h in enumerate(header, 1):
        c = ws.cell(row=hr, column=j, value=h)
        c.font = Font(bold=True)
    for i, row in enumerate(rows, start=hr + 1):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=i, column=j, value=v)
            if j in date_cols and v is not None:
                c.number_format = "yyyy-mm-dd"
            elif j in text_cols:
                c.number_format = "@"
            elif j in money_cols:
                c.number_format = "#,##0.00"
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    if freeze:
        ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    return hr


def write_card_history(path, cards, rep, mem):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cards"
    _sheet(ws, [ORG + " | Card services | card history",
                "As at Monday 5 October 2026, 06:00. Every card number issued to a member that was in use at any time "
                "since 1 June 2026. Status is as at the extract."],
           ["card_token", "member_id", "card_type", "product", "issued_on", "expiry", "status", "status_date"],
           cards.itertuples(index=False), [20, 11, 10, 30, 12, 8, 10, 12], date_cols=(5, 8), text_cols=(1, 2, 6))
    ws2 = wb.create_sheet("Replacements")
    _sheet(ws2, ["Card number replacements, 1 June to 4 October 2026",
                 "The old number stops on replaced_on and the new number carries the card from then on."],
           ["old_card_token", "new_card_token", "replaced_on", "reason"], rep.itertuples(index=False),
           [20, 20, 12, 10], date_cols=(3,), text_cols=(1, 2))
    ws3 = wb.create_sheet("Members")
    _sheet(ws3, ["Members holding the cards above", "home_branch is the branch the membership is held at."],
           ["member_id", "home_branch", "member_since", "membership"], mem.itertuples(index=False),
           [11, 16, 13, 12], date_cols=(3,), text_cols=(1,))
    wb.save(path)


def write_cases_workbook(path, wb_rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Disputed transactions"
    rows = []
    for r in wb_rows.itertuples(index=False):
        rows.append([r.case_number, r.card_token, r.member_id, r.fraud_type, r.txn_date, r.merchant_as_on_statement,
                     r.amount, r.retrieval_ref, r.case_opened, r.refunded_on, r.status])
    _sheet(ws, [ORG + " | Fraud desk | disputed card transactions",
                "Cases opened 1 August to 4 October 2026. One row per transaction a member disputes. Kept by "
                "N. Rodriguez."],
           ["case_number", "card_token", "member_id", "fraud_type", "txn_date", "merchant_as_on_statement", "amount",
            "retrieval_ref", "case_opened", "refunded_on", "status"],
           rows, [12, 20, 11, 17, 12, 46, 11, 15, 22, 12, 10], date_cols=(5, 10), text_cols=(2, 3, 8),
           money_cols=(7,))
    ws.auto_filter.ref = "A4:K%d" % (4 + len(rows))
    wb.save(path)


def write_atm_cash(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Replenishment"
    _sheet(ws, [ORG + " | Cash operations | branch ATM replenishment, July to September 2026",
                "Prepared by D. Keller. Loads and returns in dollars by cassette; minutes out of service on the visit."],
           ["visit_date", "branch", "terminal_id", "position", "loaded_20s", "loaded_50s", "returned_20s",
            "returned_50s", "minutes_out_of_service", "route"],
           rows, [12, 16, 11, 15, 11, 11, 13, 13, 12, 9], date_cols=(1,), text_cols=(3,))
    wb.save(path)


# ------------------------------------------------------------------------------------------------
def _pdf(path, title, story_fn, author="Larchmere Credit Union"):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate
    ss = getSampleStyleSheet()
    st = {
        "body": ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.6,
                               spaceAfter=4),
        "h": ParagraphStyle("h", parent=ss["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8,
                            spaceAfter=3),
        "t": ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14.5, alignment=0,
                            spaceAfter=4),
        "small": ParagraphStyle("s", parent=ss["BodyText"], fontName="Helvetica", fontSize=8, leading=10,
                                textColor="#555555"),
    }

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColorRGB(0.35, 0.35, 0.35)
        canvas.drawString(54, 36, title)
        canvas.drawRightString(558, 36, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54,
                            title=title, author=author, creator=author, producer=author, subject=title)
    doc.build(story_fn(st), onFirstPage=footer, onLaterPages=footer)


def _table(data, widths, header=True):
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    t = Table(data, colWidths=widths)
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
             ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9aa1ab")),
             ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if header:
        style += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9ecf0"))]
    t.setStyle(TableStyle(style))
    return t


def write_cp14(path):
    from reportlab.platypus import Paragraph, Spacer

    def story(st):
        P = lambda x, s="body": Paragraph(x, st[s])
        out = [P("CP-14 Card compromise and reissue", "t"),
               P("Larchmere Credit Union card policy. Version 3, approved by the Board Risk Committee on "
                 "11 March 2026. Owner: Fraud and Risk (L. Townsend). Replaces version 2 of June 2024.", "small"),
               Spacer(1, 6)]
        secs = [
            ("1. Purpose and scope",
             "This policy sets how the credit union decides that a card acceptance terminal has been compromised "
             "and which member cards are reissued as a result. It applies to every debit and credit card the credit "
             "union issues. Authorisation times are held in UTC; dates and days in this policy are Eastern time."),
            ("2. Unit",
             "The unit of reissue is the card number. A member who holds several cards is assessed card by card, and "
             "a card is reissued once however many compromised terminals read it."),
            ("3. Exposure",
             "A terminal exposes a card when it reads the card by contact: a chip read (POS entry mode 05), a chip "
             "read that falls back to the magnetic stripe (80) or a magnetic stripe read (90). Contactless reads (07 "
             "and 91), keyed transactions (01) and electronic commerce (81) do not expose a card to a skimming device. "
             "Every message from the terminal for the card is a read, whatever its response code."),
            ("4. Finding a compromised terminal",
             "When members' cards are used in counterfeit fraud, the fraud desk runs the common-point screen as the "
             "first pass. A card's first counterfeit use is the date of the earliest counterfeit transaction its "
             "holder disputes, and its lookback is the 60 days before that date. For each terminal, the share of the "
             "counterfeit cards it read by contact in their lookbacks is set against the member base rate: the share "
             "of the credit union's other cards with at least one authorisation over the same calendar span (from the "
             "first day of the earliest lookback to the last day of the latest) that the terminal read by contact in "
             "that span. A terminal that read a far larger share of the counterfeit cards than of other cards is a "
             "common point, and the investigation starts there."),
            ("5. Exposure window",
             "Once a terminal is found to have been compromised, its exposure window runs from the first to the last "
             "read, at that terminal, of a card later used in counterfeit fraud."),
            ("6. Reissue",
             "Every card read by contact at a compromised terminal within its exposure window is reissued, unless "
             "it has been replaced since or closed. Card status is taken from the card history as at the day the "
             "request is prepared; a card already replaced for renewal, loss, theft, damage or fraud is not reissued "
             "again."),
            ("7. Losses",
             "Counterfeit losses are reported in Canadian dollars at the amount posted to the member's account, by "
             "card type. Each disputed transaction is counted once. Recovered is the chargeback money received, net of "
             "any amount later taken back; net loss is gross less recovered."),
            ("8. Approval",
             "A reissue of more than 100 cards goes to the Board Risk Committee. The request states the number of "
             "cards, each compromised terminal with its exposure window, the counterfeit losses to date and the "
             "member refund record under MS-3."),
        ]
        for h, body in secs:
            out.append(P(h, "h"))
            out.append(P(body))
        out.append(Spacer(1, 8))
        out.append(_table([["Version", "Approved", "Change"],
                           ["1", "April 2021", "First issue (ATM skimming only)"],
                           ["2", "June 2024", "Exposure defined by POS entry mode; all terminal types"],
                           ["3", "March 2026", "Member base rate taken over active cards in the screen's span"]],
                          [50, 70, 330]))
        out.append(Spacer(1, 8))
        out.append(P("Internal. Not for distribution outside the credit union.", "small"))
        return out
    _pdf(path, "CP-14 Card compromise and reissue", story)


def write_codebook(path):
    from reportlab.platypus import Paragraph, Spacer

    def story(st):
        P = lambda x, s="body": Paragraph(x, st[s])
        out = [P("Authorisation extract code lists", "t"),
               P("Card processor interface guide, issuer edition 7.2, excerpt for the authorisation host extract. "
                 "Codes are carried as two- to six-character text.", "small"), Spacer(1, 6),
               P("POS entry mode (pos_entry_mode)", "h"),
               _table([["Code", "How the terminal captured the card data"],
                       ["01", "Manual key entry of the card number"],
                       ["05", "Integrated circuit card (chip) read by contact"],
                       ["07", "Contactless read of the chip"],
                       ["80", "Chip card read by magnetic stripe after the chip could not be read (fallback)"],
                       ["81", "Electronic commerce, card number entered by the cardholder"],
                       ["90", "Magnetic stripe read, full track data"],
                       ["91", "Contactless read, magnetic stripe data"]], [40, 410]),
               P("Message type (message_type)", "h"),
               _table([["Code", "Message"],
                       ["0100", "Authorisation request (includes pre-authorisations and balance enquiries)"],
                       ["0200", "Financial transaction request"],
                       ["0220", "Financial transaction advice: completion of an earlier pre-authorisation, same "
                                "retrieval reference"],
                       ["0420", "Reversal advice: reverses all or part of an earlier message, same retrieval reference"]],
                      [40, 410]),
               P("Processing code (processing_code)", "h"),
               P("Positions 1 and 2 give the transaction type: 00 goods and services, 01 cash withdrawal or cash advance, "
                 "20 return, 30 balance enquiry. Positions 3 and 4 give the account debited: 00 default, 10 savings, "
                 "20 chequing, 30 credit card account. Positions 5 and 6 give the account credited, on the same codes."),
               P("Response code (response_code)", "h"),
               _table([["Code", "Meaning"], ["00", "Approved"], ["05", "Do not honour"], ["51", "Insufficient funds"],
                       ["54", "Expired card"], ["55", "Incorrect PIN"], ["61", "Exceeds withdrawal amount limit"],
                       ["62", "Restricted card"], ["91", "Issuer or switch inoperative"]], [40, 410]),
               P("Currency (currency_txn)", "h"),
               _table([["Code", "Currency"], ["124", "Canadian dollar"], ["840", "US dollar"]], [40, 410]),
               Spacer(1, 6),
               P("Advices (0220, 0420) carry the response code 00 when the host accepts them.", "small")]
        return out
    _pdf(path, "Authorisation extract code lists", story)


def write_closeout(path):
    from reportlab.platypus import Paragraph, Spacer

    def story(st):
        P = lambda x, s="body": Paragraph(x, st[s])
        out = [P("Close-out: Brockville branch ATM skimmer, February to March 2025", "t"),
               P("Fraud and Risk, prepared by L. Townsend for the Board Risk Committee meeting of 15 May 2025. "
                 "Branch input from E. Snyder (Brockville).", "small"), Spacer(1, 6),
               P("What happened", "h"),
               P("A card-reading overlay and a pinhole camera were fitted to the lobby ATM at the Brockville branch. "
                 "Members' cards were then copied to magnetic stripe cards and used for cash withdrawals in Toronto and "
                 "Buffalo. The device was found by branch staff on 4 March 2025 and handed to Brockville police."),
               P("Timeline", "h"),
               _table([["Date (2025)", "Event"],
                       ["24 February", "First members call about withdrawals they did not make"],
                       ["3 March", "Fraud desk names the Brockville lobby ATM as the common point"],
                       ["4 March", "Device found and removed; ATM out of service until 6 March"],
                       ["5 to 12 March", "Cards read at the ATM in its exposure window reissued in two mailings"],
                       ["31 March", "Last chargeback decision received"]], [90, 360]),
               P("Cost", "h"),
               _table([["Item", "Amount"],
                       ["Cards reissued", "1,184"],
                       ["Card stock, mailing and activation support", "$11,129.60"],
                       ["Counterfeit losses, gross", "$61,738.50"],
                       ["Recovered from the acquirer", "$0.00 (our own ATM)"],
                       ["Net counterfeit loss", "$61,738.50"],
                       ["Members refunded within ten business days (MS-3)", "52 of 57"]], [270, 180]),
               Spacer(1, 6),
               P("The lobby ATM's card reader was replaced with an anti-skimming model on 6 March 2025, and the other "
                 "branch ATMs were fitted with the same reader by June 2025.")]
        return out
    _pdf(path, "Close-out: Brockville branch ATM skimmer 2025", story)


def write_ms3(path):
    from docx import Document
    from docx.shared import Pt
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("MS-3 Member service standard: unauthorised card transactions", level=1)
    d.add_paragraph("Larchmere Credit Union. Owner: E. Jenkins, Member Experience. Effective 1 January 2026, "
                    "approved by the Board Risk Committee.")
    paras = [
        "1. This standard covers members who report a debit or credit card transaction they did not make or allow.",
        "2. We refund an unauthorised transaction within ten business days of the member's report.",
        "3. Business days are Monday to Friday, other than the holidays in the appendix. The count runs from the day "
        "the member reports, in the member's local time: that day is day 0, and the refund is on time if it is posted "
        "to the member's account on or before the tenth business day after day 0. A report made on a Saturday, a "
        "Sunday or a holiday is treated as made on the next business day.",
        "4. A claim that is closed and later re-opened under a new case number is the same claim, and its ten "
        "business days run from the member's first report.",
        "5. The refund is posted as a provisional credit when the member's signed declaration is received.",
        "6. The fraud desk reports against this standard by card type: the claims refunded within the ten business "
        "days, and the longest any refunded member waited.",
    ]
    for p in paras:
        d.add_paragraph(p)
    d.add_heading("Appendix: holidays observed in 2026", level=2)
    t = d.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Date", "Holiday"
    for day, name in W.HOLIDAYS_2026:
        row = t.add_row().cells
        row[0].text = day.strftime("%a %d %b %Y")
        row[1].text = name
    d.add_paragraph("")
    d.add_paragraph("Branches and the contact centre are closed on these days; no refunds post.")
    d.save(path)


def write_notes(path, F):
    txt = f"""# Fraud desk extracts: field notes

N. Rodriguez, fraud desk. Pulled Monday 5 October 2026 for the card reissue request.

## {F['auth']}
One row per message the authorisation host received for a Larchmere card, from 1 June 2026 00:00 UTC up to
5 October 2026 00:00 UTC. `txn_datetime_utc` is UTC. `amount_txn` is in `currency_txn`; `amount_billing_cad` is
the Canadian dollar amount posted to, or held on, the member's account for that message. A pre-authorisation and
its completion advice share a `retrieval_ref`, and so do a message and its reversal. `terminal_id` is the
acquirer's terminal identifier; a replaced terminal gets a new one. Codes are in `{F['codebook']}`.

## {F['merchants']}
One row per merchant ID. A site with several businesses has a merchant ID for each.

## {F['cards']}
Cards: one row per card number, with its status as at the extract (Open, Replaced or Closed).
Replacements: old and new card number, the date the new number took over and the reason.
Members: home branch of each member.

## {F['cases']}
One row per disputed transaction, under its case number. `amount` is the transaction amount the member entered on
the dispute form. `retrieval_ref` is the authorisation's. `case_opened` is when the case was created in the case
system, in UTC. `refunded_on` is the day the provisional credit posted. Status: Open (no refund yet), Refunded,
Closed (closed without a refund).

## {F['chargebacks']}
One row per chargeback event. `amount_cad` is the money the event moved in Canadian dollars: credits to us are
positive, amounts taken back are negative, and a filing moves nothing.
"""
    with open(path, "w") as fh:
        fh.write(txt)


def write_log(path, F, counts, msg):
    first = msg.txn_datetime_utc.min().strftime("%Y-%m-%dT%H:%M:%SZ")
    last = msg.txn_datetime_utc.max().strftime("%Y-%m-%dT%H:%M:%SZ")
    txt = f"""card data pull 2026-10-05 06:12:41 EDT  job: fraud_weekly  user: nrodriguez
source                     file                                                  rows
auth_host.messages         {F['auth']:<53} {counts['messages']}
acquirer.merchant_dir      {F['merchants']:<53} {counts['merchants']}
cards.history (Cards)      {F['cards']:<53} {counts['cards']}
cards.history (Repl.)      {F['cards']:<53} {counts['replacements']}
cards.history (Members)    {F['cards']:<53} {counts['members']}
fraud_desk.disputed_txns   {F['cases']:<53} {counts['case_rows']}
chargebacks.events         {F['chargebacks']:<53} {counts['chargebacks']}
online_banking.sessions    {F['logins']:<53} {counts['logins']}
atm_ops.replenishment      {F['atmcash']:<53} {counts['atm_cash']}
auth window 2026-06-01T00:00:00Z <= txn_datetime_utc < 2026-10-05T00:00:00Z; first {first}, last {last}
case window: case_opened 2026-08-01 to 2026-10-04 (Eastern)
documents copied: {F['cp14']}, {F['ms3']}, {F['codebook']}, {F['closeout']}, {F['notes']}
"""
    with open(path, "w") as fh:
        fh.write(txt)
