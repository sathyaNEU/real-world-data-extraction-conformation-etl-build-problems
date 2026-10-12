"""Documents of the task501 pack: the liquidity directive, the lender's term sheet, the Stiftungsrat minutes extract,
the mail thread, the field notes, the export manifest and the H1 2025 programme report (the context artifact).
Every figure a document states is computed from the written files at build time, never typed."""
import json
import os
from datetime import date, timedelta

import docx
from docx.shared import Pt, Cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

import world as W
import pack as PK

T = PK.T
P = W.PEOPLE
DIRECTIVE = "richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx"
TERMSHEET = "term_sheet_lindenhof_standby_2027.pdf"
MINUTES = "stiftungsrat_protokoll_auszug_2026-09-24.pdf"
MAIL = "mail_standby_fazilitaet_2027.txt"
NOTES = "feldbeschrieb_privatmarkt_extrakt.md"
MANIFEST = "extraktprotokoll_PKW-PM-2026-12-31.json"
REPORT = "halbjahresbericht_privatmarkt_2025-H1.pdf"

# the directive's text, sentence for sentence; checks.py asserts every quoted sentence of the fork table is here
DIRECTIVE_TEXT = [
    ("h", "1  Purpose and scope"),
    ("p", "This directive sets how the cash needs of the private-markets programme are planned and funded. It applies to every fund "
          "commitment in the programme register, to the programme account and its reserve, and to any standby credit facility held for "
          "the programme. Portfolio Management manages the commitments; Treasury & Liquidität plans and funds the calls."),
    ("h", "2  Definitions"),
    ("p", "2.1  Commitment: the amount the Pensionskasse has subscribed to a fund, in the fund's currency, as recorded in the programme register."),
    ("p", "2.2  Capital call: an amount a manager calls against the commitment, for investments, management fees or partnership expenses, "
          "payable on the value date the notice states."),
    ("p", "2.3  Distribution: an amount a manager returns as return of capital, realised gain or income, in cash or in specie."),
    ("p", "2.4  Unfunded commitment: the commitment less the capital calls with a value date on or before that day."),
    ("p", "2.5  Plan date: 31 December of the year before the facility year."),
    ("p", "2.6  Facility year: the calendar year for which the facility is elected."),
    ("p", "2.7  Reference rate: the custodian's 16:00 reference rate for the currency on the day; for a day without a rate, the rate of the "
          "preceding business day."),
    ("h", "3  Programme reserve"),
    ("p", "The programme account holds a reserve of CHF 150 million, restored at the start of each month from the general portfolio. The "
          "reserve is the first source for calls and the standby facility the second."),
    ("h", "4  Standby facility"),
    ("p", "The Pensionskasse elects the smallest facility amount offered by the lender that, together with the reserve, is at least the "
          "expected capital calls of the facility year plus one tenth of them. Amounts in other currencies are translated at the reference "
          "rate of the plan date. Distributions are credited to the programme account and swept to the general portfolio on the day they "
          "arrive; they are not credited against calls."),
    ("h", "5  The plan"),
    ("p", "5.1  The plan states the expected capital calls of the facility year on every commitment in the programme register at the plan "
          "date. A call is in the facility year when its value date is, whenever it was noticed. Commitments signed after the plan date are "
          "funded from the commitment budget and are not in the plan."),
    ("p", "5.2  Treasury & Liquidität prepares the plan from the programme's own records as they stand at the plan date."),
    ("p", "5.3  The Stiftungsrat delegates the election to its president together with the head of Treasury & Liquidität, who elect the "
          "facility on the basis of the plan and report it at the next sitting."),
    ("h", "6  Annual liquidity report"),
    ("p", "Each January Treasury & Liquidität reports to the Stiftungsrat the cash the programme paid and received in the year past, with "
          "the facility elected for the year ahead."),
    ("h", "7  Roles"),
    ("p", "Rechnungswesen maintains the notice ledger, the programme register, the NAV register and the audited capital accounts and receives "
          "the custodian's statements. Portfolio Management confirms the register before each plan. Treasury & Liquidität prepares the plan "
          "and the report."),
]


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    head = ParagraphStyle("head", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceAfter=4)
    title = ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=13.5, alignment=0, spaceAfter=6)
    return body, small, head, title


def write_directive():
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
    d.add_paragraph(W.ORG).runs[0].bold = True
    d.add_paragraph("Richtlinie Liquiditätsplanung Privatmarktanlagen (RL-PM-05)")
    d.add_paragraph("Working translation of version 5, approved by the Stiftungsrat on 24 September 2026 and in force from 1 October 2026; "
                    "it replaces RL-PM-04. The German text is binding. Owner: Treasury & Liquidität. Review: annual.")
    for kind, text in DIRECTIVE_TEXT:
        if kind == "h":
            d.add_heading(text, level=2)
        else:
            d.add_paragraph(text)
    d.add_paragraph("")
    d.add_paragraph("Verteiler: Stiftungsrat, Geschäftsleitung, Treasury & Liquidität, Portfolio Management, Rechnungswesen. Intern.").runs[0].italic = True
    d.save(os.path.join(T, DIRECTIVE))
    PK.fix_zip_times(os.path.join(T, DIRECTIVE))


def write_term_sheet():
    body, small, head, title = _styles()
    doc = SimpleDocTemplate(os.path.join(T, TERMSHEET), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm, invariant=1, title="Indicative term sheet, standby facility 2027", author=W.BANK, subject="Standby facility 2027",
                            creator="Institutional Clients")
    menu = ", ".join(str(a) for a in W.MENU[:-1]) + " or " + str(W.MENU[-1])
    el = [Paragraph(W.BANK, head), Paragraph("Indicative term sheet: committed standby facility, facility year 2027", title),
          Paragraph("Private and confidential. Indicative, subject to credit approval and documentation. Zurich, 9 December 2026.", small),
          Spacer(1, 8)]
    rows = [
        ["Borrower", f"{W.ORG}, Zurich"],
        ["Lender", W.BANK],
        ["Purpose", "Bridging of capital calls under the Borrower's private-markets programme"],
        ["Facility amount", f"One of CHF {menu} million, elected by the Borrower in writing by 15 January 2027 and available in that "
                            "amount for the whole availability period"],
        ["Availability period", "1 January 2027 to 31 December 2027"],
        ["Drawings", "Minimum CHF 5 million, multiples of CHF 1 million, one business day's notice before 11:00"],
        ["Commitment fee", "0.30 per cent of the facility amount for the availability period, drawn or undrawn, payable in four equal "
                           "quarterly instalments in arrears"],
        ["Arrangement fee", "0.15 per cent flat on the facility amount, payable on election"],
        ["Interest on drawings", "Compounded SARON plus 1.10 per cent per annum, payable monthly"],
        ["Repayment", "Each drawing repaid within 60 days; final maturity 31 March 2028"],
        ["Security", "Unsecured; negative pledge over the programme's fund interests"],
        ["Covenants", "Programme net asset value at least CHF 900 million; facility amount not above 25 per cent of programme net asset value"],
        ["Governing law", "Swiss law, courts of Zurich"],
        ["Contact", f"{P['bank']}, Institutional Clients"],
    ]
    t = Table([[Paragraph(a, body), Paragraph(b, body)] for a, b in rows], colWidths=[4.2 * cm, 12.6 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eeeeee"))]))
    el += [t, Spacer(1, 10), Paragraph("This term sheet is not a commitment to lend. Fees and margin are indicative for an election made by 15 January 2027.", small)]
    doc.build(el)


def write_minutes(sept):
    body, small, head, title = _styles()
    doc = SimpleDocTemplate(os.path.join(T, MINUTES), pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            invariant=1, title="Protokollauszug Stiftungsrat 24.09.2026", author=W.ORG, subject="Traktandum 6",
                            creator="Sekretariat des Stiftungsrats")
    drawn = f"{sept['drawn'] / 1e6:.0f}"
    el = [Paragraph(W.ORG, head), Paragraph("Stiftungsrat, Sitzung vom 24. September 2026, Auszug (Traktandum 6)", title),
          Paragraph(f"Working translation of the extract circulated to Treasury & Liquidität. Present: the full Stiftungsrat and the Geschäftsleitung; "
                    f"{P['treasury']} (Treasury & Liquidität) and {P['pm']} (Portfolio Management) for item 6. Chair: {P['president']}.", small),
          Spacer(1, 8),
          Paragraph("6  Programme liquidity: the September event and the revised directive", head),
          Paragraph(f"6.1  {P['treasury']} reported that in the week of {sept['first'].day} September capital calls of CHF {sept['calls'] / 1e6:.1f} million "
                    "fell due on the programme account while the month's transfer from the general portfolio was held back by the settlement of a bond "
                    f"sale. The standby facility was drawn for CHF {drawn} million on {sept['date'].day} September and repaid on {sept['repaid'].day} October. "
                    "No call was paid late. The interest and fees are in the third-quarter accounts.", body), Spacer(1, 4),
          Paragraph("6.2  The Stiftungsrat approved version 5 of the liquidity directive (RL-PM-05), in force from 1 October 2026. It raises the "
                    "programme reserve from CHF 35 million to CHF 150 million and sizes the standby facility on the plan's expected capital calls "
                    "for the facility year, with a margin of one tenth, instead of the buffer of version 4.", body), Spacer(1, 4),
          Paragraph(f"6.3  {W.BANK} has indicated that it will offer the 2027 facility in fixed amounts; the term sheet will follow in December.", body),
          Spacer(1, 4),
          Paragraph(f"Resolution 2026-41: Treasury & Liquidität prepares the plan for 2027 under RL-PM-05 from the year-end extract. The election of "
                    f"the facility amount is delegated under section 5.3 to the president ({P['president']}) together with the head of Treasury & "
                    "Liquidität and is reported at the sitting of 18 March 2027.", body), Spacer(1, 10),
          Paragraph("Sekretariat des Stiftungsrats. Dieser Auszug ist für den internen Gebrauch bestimmt.", small)]
    doc.build(el)


def write_mail(info):
    txt = f"""From: {P['bank']} <lazar.marti@lindenhof.ch>
Sent: Wednesday, 6 January 2027 14:30
To: {P['treasury']} <treasury@pk-werdinsel.ch>
Subject: RE: Standby facility 2027

Domenica, noted. The terms stand as indicated; the 2026 facility runs to 31 December as agreed.

Best regards,
Lazar Marti
Privatbank Lindenhof AG, Institutional Clients

________________________________________
From: {P['treasury']} <treasury@pk-werdinsel.ch>
Sent: Wednesday, 6 January 2027 09:12
To: {P['bank']} <lazar.marti@lindenhof.ch>
Subject: Standby facility 2027

Lazar,

Thank you for the term sheet of 9 December. We will confirm the amount in writing by 15 January, as agreed.

Domenica

________________________________________
From: {P['pm']} <portfolio@pk-werdinsel.ch>
Sent: Tuesday, 5 January 2027 10:41
To: {P['treasury']} <treasury@pk-werdinsel.ch>
Cc: {P['accounting']} <rechnungswesen@pk-werdinsel.ch>
Subject: RE: Jahresendextrakt Privatmarkt PKW-PM-2026-12-31

Register confirmed as at 31 December: {info['n_funds']} commitments, the most recent the Halvorsen III close in September.
The two commitments the investment committee approved in December (Marignane VI and Ebersol V) close in February and
March and are not in the register.

Torsten

________________________________________
From: {P['accounting']} <rechnungswesen@pk-werdinsel.ch>
Sent: Tuesday, 5 January 2027 08:05
To: {P['treasury']} <treasury@pk-werdinsel.ch>
Cc: {P['pm']} <portfolio@pk-werdinsel.ch>
Subject: Jahresendextrakt Privatmarkt PKW-PM-2026-12-31

Domenica,

The year-end extract is on the share (Extraktprotokoll PKW-PM-2026-12-31): the notice ledger to 31 December, the register as at
31 December, the NAV register, the audited capital accounts to FY2025, the look-through holdings to the third quarter, the
custodian's statement of the programme account for 2025 and 2026, and the reference rates. Field notes attached.

Statements: the third-quarter reports of {info['q3_missing']} funds had not arrived by the close; everything else to Q3 is in.

Noémie

--
Pensionskasse Werdinsel, Werdstrasse 21, 8004 Zürich. Diese Nachricht ist vertraulich.
"""
    with open(os.path.join(T, MAIL), "w", encoding="utf-8") as fh:
        fh.write(txt)


def write_field_notes(counts):
    md = f"""# Feldbeschrieb Privatmarkt-Extrakt PKW-PM-2026-12-31

Rechnungswesen, Pensionskasse Werdinsel. Extract of the private-markets records as at 31 December 2026 (close of business),
produced on 5 January 2027 for Treasury & Liquidität. Amounts are in the currency stated on each row; a file carries Swiss
francs only where a column says so.

## {PK.LEDGER} ({counts['ledger']} rows)

One row per line of a notice recorded in the private-markets ledger. A notice has one or more lines.

| column | meaning |
|---|---|
| notice_id | the reference under which the notice was recorded |
| fund_id, fund_code | our fund identifier and the fund's short code (register) |
| notice_type | CAPITAL_CALL or DISTRIBUTION |
| notice_date | date of the notice |
| value_date | for a call, the due date on the notice; for a distribution, the payment date |
| status | ISSUED, or CANCELLED where the manager withdrew the notice. A withdrawn notice has no cash effect; the manager reissues it under a new number. |
| line_no, line_type | line sequence within the notice and its kind: INVESTMENT, MANAGEMENT_FEE, PARTNERSHIP_EXPENSES on calls; RETURN_OF_CAPITAL, REALISED_GAIN, INCOME, IN_KIND on distributions |
| investment_ref | the manager's reference of the investment the line relates to, where there is one |
| description | text of the line |
| currency | fund currency (ISO 4217); the clerks are not consistent about case |
| amount | amount of the line, positive, two decimals |
| entered_at | when the line was entered in the ledger |
| remarks | free text, used for withdrawals and reissues |

IN_KIND lines are distributions of listed shares at the value stated on the notice; they settle in securities, not cash.

## {PK.REGISTER}

Sheet Fonds: one row per fund commitment, in the fund currency, with the contractual dates and the management fee during
the investment period. Sheet Strategien: strategy codes. Sheet Hinweise: notes on the contract terms.

## {PK.CUSTODY} ({counts['custody']} rows)

The custodian's statement of the programme account (CHF), 1 January 2025 to 31 December 2026, semicolon-separated, as
exported from the custodian's portal: Buchungsdatum (the day the custodian booked the posting), Valuta (the value date, the
day the amount was credited to or debited from the account), Buchungstext (posting text),
Gegenpartei (counterparty), Referenz (the payment reference as received or as given on our order), Transaktionsreferenz
(the custodian's reference), Betrag CHF (amount, credits positive) and Saldo CHF (the balance after the posting). Receipts
and payments in other currencies are converted into Swiss francs by the custodian on the value date at its dealing rate.

## {PK.AUDITED} ({counts['audited']} rows)

Sheet Kapitalkonten: our capital account in each fund as stated in the fund's audited financial statements, one row per
fund and financial year-end 31 December 2021 to 2025, in the fund currency. Sheet Erfassung: compilation notes.

## {PK.NAVREG} ({counts['nav']} rows)

Our NAV register: one row per manager statement received, from the first quarter of 2019. period_end is the statement's
period end; received_date when it arrived; booking_date when Rechnungswesen booked it; fx_rate_booked the reference rate of
the booking date; nav_chf_booked the Swiss-franc value booked at that rate. A statement not yet received has no row.

## {PK.HOLDINGS} ({counts['holdings']} rows)

The managers' quarterly schedules of investments as loaded into the look-through system, from the first quarter of 2016 to
the third quarter of 2026: one row per instrument of each investment held at the report date (a shareholder loan is a row of
its own), with the cost to date and the fair value the manager reports, in the fund currency, and the sector (NACE Rev. 2
section) as the manager reports it.

## {PK.FXFILE} ({counts['fx']} rows)

The custodian's 16:00 reference rates against the Swiss franc on business days, 5 January 2015 to 31 December 2026, one
row per currency and day, for every currency the custodian quotes: rate_chf is the price in Swiss francs of unit units of
the currency (1 for USD, EUR, GBP, CAD, AUD and SGD; 100 for JPY, SEK, NOK, DKK and HKD). For a date with no row the rate
of the preceding business day applies.

## Documents

{DIRECTIVE} (the directive, working translation) · {TERMSHEET} · {MINUTES} · {REPORT} (the last
semi-annual programme report on file; the H2 2025 and H1 2026 reports are with the secretariat) · {MAIL} · {MANIFEST}
"""
    with open(os.path.join(T, NOTES), "w", encoding="utf-8") as fh:
        fh.write(md)


def write_manifest(counts, info):
    files = sorted(f for f in os.listdir(T) if not f.startswith("."))
    man = {
        "extract_id": "PKW-PM-2026-12-31",
        "organisation": f"{W.ORG}, Rechnungswesen",
        "as_of": "2026-12-31T18:00:00+01:00",
        "produced": "2027-01-05T07:40:00+01:00",
        "produced_by": P["accounting"],
        "system": "PM-Ledger 4.3 with the custodian's CF-PM advices; register, NAV register and capital accounts maintained in Rechnungswesen",
        "files": [{"file": f, "size_bytes": os.path.getsize(os.path.join(T, f))} for f in files if f != MANIFEST],
        "row_counts": {PK.LEDGER: counts["ledger"], PK.CUSTODY: counts["custody"], PK.NAVREG: counts["nav"], PK.HOLDINGS: counts["holdings"],
                       PK.FXFILE: counts["fx"], PK.AUDITED: counts["audited"]},
        "coverage": {PK.LEDGER: "notices dated 2015-01-01 to 2026-12-31", PK.CUSTODY: "postings 2025-01-01 to 2026-12-31",
                     PK.NAVREG: "statements received by 2027-01-04", PK.HOLDINGS: "report dates 2016-03-31 to 2026-09-30",
                     PK.AUDITED: "financial years 2021 to 2025"},
        "notes": f"Ledger complete to 31.12.2026. Third-quarter 2026 statements outstanding for {info['q3_missing']} funds at the extract date.",
    }
    with open(os.path.join(T, MANIFEST), "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2, ensure_ascii=False)


ORDINAL = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth"}


def write_report(bridge, streak):
    """The H1 2025 semi-annual programme report: a closed half-year's NAV bridge by strategy (the context artifact)."""
    body, small, head, title = _styles()
    doc = SimpleDocTemplate(os.path.join(T, REPORT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            invariant=1, title="Halbjahresbericht Privatmarktprogramm 2025 H1", author=W.ORG, subject="Privatmarktprogramm",
                            creator="Treasury & Liquiditaet")
    el = [Paragraph(f"{W.ORG}, Treasury & Liquidität", head), Paragraph("Privatmarktprogramm: Halbjahresbericht 1. Januar bis 30. Juni 2025", title),
          Paragraph("Report to the Stiftungsrat. Figures in thousands of Swiss francs. Net asset values at the reference rate of the period end; "
                    "calls and distributions at the reference rate of their value date. Presented at the sitting of 25 September 2025.", small), Spacer(1, 8)]
    hdr = ["Strategy", "NAV 31.12.2024", "Capital called", "Distributions", "Valuation and currency", "NAV 30.06.2025"]
    data = [hdr]
    for s in ("BO", "GR", "PC", "IN", "TOTAL"):
        b = bridge[s]
        data.append([W.STRATEGIES.get(s, "Programme")] + [f"{round(b[k] / 1000):,}" for k in ("opening", "calls", "dists", "valuation", "closing")])
    t = Table(data, colWidths=[3.4 * cm, 2.6 * cm, 2.6 * cm, 2.6 * cm, 3.0 * cm, 2.6 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 8.5)]))
    el += [t, Spacer(1, 10)]
    lead = sorted(("BO", "GR", "PC", "IN"), key=lambda s: -bridge[s]["dists"])[:2]
    el += [Paragraph(f"Distributions exceeded calls in the first half for the {ORDINAL[streak]} half-year running, led by "
                     f"{W.STRATEGIES[lead[0]].lower()} and {W.STRATEGIES[lead[1]].lower()}. The programme account was restored to the "
                     "reserve at the start of each month; the standby facility was not drawn.", body),
           Spacer(1, 6), Paragraph("Prepared by Treasury & Liquidität from the NAV register, the notice ledger and the reference-rate file. "
                                   "Rows and totals are rounded separately.", small)]
    doc.build(el)
