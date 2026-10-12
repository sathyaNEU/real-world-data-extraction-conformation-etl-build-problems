"""Documents of the task501 pack: the liquidity directive, the term sheet, the board minutes extract, the mail thread,
the field notes, the export manifest and the H2 2025 semi-annual report (context artifact). Figures that appear in a
document are computed from the pack by solve.py at build time, never typed."""
import json
import os
from datetime import date, datetime

import docx
from docx.shared import Pt, Cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

import sim
import solve

T = solve.T
P = sim.PEOPLE


def _para_style():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    head = ParagraphStyle("head", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, spaceAfter=4)
    title = ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14, alignment=0, spaceAfter=6)
    return body, small, head, title


# ------------------------------------------------------------------ the directive (governing standard)
def write_directive():
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
    d.add_paragraph("Pensionskasse Werdinsel").runs[0].bold = True
    d.add_paragraph("Richtlinie Liquiditätsplanung Privatmarktanlagen (RL-PM-04)")
    d.add_paragraph("Working translation, version 4. Approved by the Stiftungsrat on 20 November 2024, in force from 1 January 2025. "
                    "The German text is binding. Owner: Treasury & Liquidity. Review: annual, next due Q4 2026.")
    d.add_heading("1  Purpose and scope", level=2)
    d.add_paragraph("This directive sets how the liquidity need of the private-markets programme is planned and funded. It applies to every fund "
                    "commitment held in the programme register, in all strategies, and to the standing reserve and any standby credit facility held "
                    "against the programme. The programme is managed by Portfolio Management; the plan under section 5 is prepared by Treasury & "
                    "Liquidity and approved by the Stiftungsrat together with the facility amount.")
    d.add_heading("2  Definitions", level=2)
    d.add_paragraph("Commitment: the amount the Pensionskasse has subscribed to a fund, in the fund's currency, as recorded in the programme register.")
    d.add_paragraph("Capital call: a notice from the manager requesting payment against the commitment, for investments, management fees or partnership expenses. "
                    "Distribution: a notice from the manager returning capital, realised gain or income, in cash or in specie.")
    d.add_paragraph("Fund age: the number of calendar months from the month of the fund's first capital call notice to the month in question, both months counted. "
                    "A fund that has not yet issued a first capital call is aged from the month after the plan date, as if its first call fell in that month.")
    d.add_paragraph("Age bands: months 1 to 12, 13 to 24, 25 to 36, 37 to 54, 55 to 78, and 79 and later. Estimation window: the record from January 2019 to the "
                    "last day of a stated month, which for a plan is the plan date.")
    d.add_paragraph("Strategy: one of Buyout, Growth, Private credit and Infrastructure, as recorded in the register (sheet Strategien).")
    d.add_paragraph("Plan date: the last day of the quarter preceding the plan.")
    d.add_heading("3  Programme liquidity reserve", level=2)
    d.add_paragraph("The programme holds a standing reserve of CHF 75 million in the programme cash account, replenished to that level on the first "
                    "business day of each year from the general portfolio. The reserve is the first source for calls; the standby facility is the second.")
    d.add_heading("4  Standby facility", level=2)
    d.add_paragraph("The facility amount for a facility year is the smallest amount offered by the lender that is at least the plan's peak cumulative net outflow "
                    "for that year, plus the plan buffer of section 5.6, less the reserve, where the peak is taken over the month ends of the facility year and the "
                    "cumulative net outflow is counted from the first day of the facility year. Expected distributions enter the net outflow at one quarter of "
                    "their forecast amount. Amounts are translated to Swiss francs at the custodian reference rate of the plan date.")
    d.add_heading("5  The forward schedule", level=2)
    d.add_paragraph("5.1  The schedule runs month by month from the month after the plan date to the end of the facility year, for every fund in the register. "
                    "The expected call of a fund in a month is its rate under the selected basis applied to its commitment, and not more than the fund's unfunded "
                    "commitment at the start of that month; the unfunded commitment is reduced by the expected call before the next month is scheduled. "
                    "Cancelled notices are excluded throughout; rates are carried unrounded.")
    d.add_paragraph("5.2  Three candidate bases are maintained. Under the band basis a fund's rate is the pooled monthly call rate of its age band: the sum of capital "
                    "calls over the sum of commitments across all fund-months in that band from January 2019 to the end of the estimation window, each fund-month "
                    "counting from the month of the fund's first call. Under the strategy basis the pooling is by strategy and age band. Under the manager basis a "
                    "fund's rate in an age band is its own calls over its own commitment averaged over its fund-months in that band within the estimation window; "
                    "for a band the fund has not yet reached it carries its rate in the latest band it has reached, and a fund with no fund-months carries the "
                    "strategy basis rate. Sums across funds are translated at the reference rate of the window's last day.")
    d.add_paragraph("5.3  The basis used for a plan is selected by the walk-forward test. The test origins are the twelve quarter ends from 31 December 2022 to "
                    "30 September 2025. At each origin every candidate is estimated on the record up to and including the origin month and nothing later, and "
                    "applied to the funds in the register at that origin, with their unfunded commitments at that origin, over the twelve months following the "
                    "origin; the forecast and the realised calls of those funds over the same twelve months are both translated at the reference rate of the origin "
                    "date. A candidate's error at an origin is the absolute difference between forecast and realised programme calls as a share of the realised "
                    "calls, and its test error is the mean over the twelve origins. The candidate with the lowest test error is selected; on an equal test error "
                    "the basis with fewer parameters is selected.")
    d.add_paragraph("5.4  Distributions. The expected distribution of a fund in a month is the pooled distribution rate of its strategy and age band applied to the "
                    "fund's net asset value at the last audited year-end before the plan date, as reported in the audited capital account; a fund without an audited "
                    "net asset value at that date carries no expected distribution. The pooled distribution rate of a strategy and age band is the sum of "
                    "distributions, in cash and in specie at notice value, over the sum of the funds' audited net asset values at the year-end preceding each "
                    "fund-month, across all fund-months of that strategy and band from January 2022 to the plan date for which such an audited value exists, both "
                    "sums translated at the plan-date rate.")
    d.add_paragraph("5.5  The plan states, for each month of the facility year, the expected calls, the expected distributions, the credited distributions, the "
                    "net outflow and the cumulative net outflow, in thousands of Swiss francs, the test result for every candidate at every origin, and the plan buffer.")
    d.add_paragraph("5.6  Plan buffer. The plan buffer is the largest amount by which the realised calls of the test ran ahead of the selected basis's forecast at "
                    "any point in a horizon, translated at the rate of that origin's date, or nil where they never did.")
    d.add_heading("6  Basis of unfunded commitments", level=2)
    d.add_paragraph("6.1  The unfunded commitment of each fund at any date is carried from the programme's own notice ledger: the commitment, less capital calls "
                    "issued to that date, plus the return-of-capital proceeds of investments realised within the fund's recycling period stated in the register, "
                    "measured from the date of the fund's first investment in the company, where the distribution is dated during the fund's investment period. "
                    "It is not taken from a manager's quarterly statement, which may be outstanding or unreconciled.")
    d.add_paragraph("6.2  The ledger basis is agreed to the audited capital account of every fund at every audited year-end on file before a plan is submitted.")
    d.add_heading("7  Semi-annual programme report", level=2)
    d.add_paragraph("7.1  The programme report to the Stiftungsrat bridges the net asset value from the opening to the closing period end by strategy: opening "
                    "value, capital called, distributions, valuation and currency movement, closing value, in thousands of Swiss francs.")
    d.add_paragraph("7.2  Net asset values are translated at the custodian reference rate of the period end to which they relate. Capital called and distributions "
                    "are attributed to the period of their value date and translated at the reference rate of that value date. Distributions in specie are not "
                    "cash and do not enter the report's distribution line.")
    d.add_paragraph("7.3  Where a manager's statement for the closing period end has not been received by the reporting date, the fund's closing value is its "
                    "latest received statement value adjusted for capital called and distributions, in the fund's currency, with a value date after that "
                    "statement's period end and on or before the closing period end.")
    d.add_paragraph("7.4  The valuation and currency movement is the balancing item of the bridge.")
    d.add_heading("8  Roles", level=2)
    d.add_paragraph("Treasury & Liquidity prepares the plan and the facility proposal. Rechnungswesen maintains the notice ledger, the register, the NAV register and "
                    "the audited capital accounts. Portfolio Management confirms the register before each plan. The Stiftungsrat approves the facility amount.")
    d.add_paragraph("")
    d.add_paragraph("Distribution: Stiftungsrat, Geschäftsleitung, Treasury & Liquidity, Portfolio Management, Rechnungswesen. Internal. Not to be forwarded outside the Pensionskasse.").runs[0].italic = True
    d.save(os.path.join(T, "richtlinie_liquiditaet_privatmarkt_RL-PM-04.docx"))
    import pack
    pack.fix_zip_times(os.path.join(T, "richtlinie_liquiditaet_privatmarkt_RL-PM-04.docx"))


# ------------------------------------------------------------------ term sheet
def write_term_sheet():
    body, small, head, title = _para_style()
    doc = SimpleDocTemplate(os.path.join(T, "term_sheet_lindenhof_standby_2027.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm, invariant=1,
                            title="Indicative term sheet, standby facility 2027", author=sim.BANK)
    el = [Paragraph(sim.BANK, head), Paragraph("Indicative term sheet: committed standby facility, facility year 2027", title),
          Paragraph("Private and confidential. Indicative only, subject to credit approval and documentation. Dated 6 October 2026.", small), Spacer(1, 8)]
    rows = [
        ["Borrower", "Pensionskasse Werdinsel, Zürich"],
        ["Lender", sim.BANK],
        ["Purpose", "Bridging of capital calls under the Borrower's private-markets programme"],
        ["Facility amount", "One of CHF 50, 75, 100, 125, 150, 175, 200, 225, 250, 275 or 300 million, elected by the Borrower in writing by 15 December 2026"],
        ["Availability period", "1 January 2027 to 31 December 2027"],
        ["Drawings", "Minimum CHF 5 million, multiples of CHF 1 million, two business days' notice"],
        ["Commitment fee", "0.30 per cent per annum on the facility amount, payable quarterly in arrears"],
        ["Arrangement fee", "0.15 per cent flat on the facility amount, payable on signing"],
        ["Interest on drawings", "Compounded SARON plus 1.10 per cent per annum, payable monthly"],
        ["Repayment", "Each drawing repaid within 90 days; final maturity 31 March 2028"],
        ["Security", "Unsecured; negative pledge over the programme fund interests"],
        ["Covenants", "Programme net asset value at least CHF 1,000 million; facility amount not exceeding 25 per cent of programme net asset value"],
        ["Governing law", "Swiss law, courts of Zürich"],
        ["Contact", f"{P['bank']}, Institutional Clients, {sim.BANK}"],
    ]
    t = Table([[Paragraph(a, body), Paragraph(b, body)] for a, b in rows], colWidths=[4.2 * cm, 12.6 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eeeeee"))]))
    el += [t, Spacer(1, 10), Paragraph("This term sheet does not constitute a commitment to lend. Fees and margin are indicative for a facility elected before 15 December 2026.", small)]
    doc.build(el)


# ------------------------------------------------------------------ board minutes extract
def write_minutes():
    body, small, head, title = _para_style()
    doc = SimpleDocTemplate(os.path.join(T, "stiftungsrat_protokoll_auszug_2026-09-24.pdf"), pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm, invariant=1,
                            title="Protokollauszug Stiftungsrat 24.09.2026", author="Pensionskasse Werdinsel")
    el = [Paragraph("Pensionskasse Werdinsel", head), Paragraph("Stiftungsrat, Sitzung vom 24. September 2026, Auszug (Traktandum 6)", title),
          Paragraph("Working translation of the extract circulated to Treasury & Liquidity. Present: the full Stiftungsrat, the Geschäftsleitung, "
                    f"{P['treasury']} (Treasury & Liquidity, for item 6), {P['pm']} (Portfolio Management, for item 6). Chair: {P['president']}.", small), Spacer(1, 8),
          Paragraph("6  Liquidity event of September and funding of the private-markets programme", head),
          Paragraph("6.1  The chair reported that in the second week of September the programme cash account fell below the reserve floor of the directive "
                    "when several capital calls fell due in the same week and two expected distributions were paid later than their notices indicated. "
                    "Treasury & Liquidity met the calls by selling a block of the domestic bond ladder at short notice. The realised loss on that sale will be "
                    "shown in the third-quarter report. No call was paid late.", body), Spacer(1, 4),
          Paragraph(f"6.2  {P['cio']} said that in his view the event was one of timing rather than of size. Every manager has its own rhythm, the programme has "
                    "ten years of each fund's own record, and a plan built fund by fund on what each manager has actually done, using everything on file, would have "
                    "carried the September week with a modest line. He asked that the facility be kept as small as the directive allows.", body), Spacer(1, 4),
          Paragraph(f"6.3  {P['pm']} noted that the private-credit funds of the 2023 and 2024 vintages are, on the register, close to fully drawn, and that in his "
                    "experience a credit manager at that stage calls little beyond fees. He expected 2027 calls to come from the buyout and infrastructure "
                    "commitments of 2024 to 2026.", body), Spacer(1, 4),
          Paragraph(f"6.4  {P['president']} recalled that under RL-PM-04 the facility amount is set by the plan and not by judgement, and that the Stiftungsrat "
                    "would decide the amount at its sitting of 19 November 2026 on the basis of the plan prepared by Treasury & Liquidity. "
                    f"{sim.BANK} has offered a committed standby facility for 2027 in fixed amounts; the term sheet is to be circulated with the plan.", body), Spacer(1, 4),
          Paragraph(f"Resolution 2026-41: Treasury & Liquidity ({P['treasury']}) prepares the 2027 liquidity plan under RL-PM-04 from the 30 September 2026 "
                    "extract and proposes the facility amount to be elected. Deadline: papers to the secretariat by 10 November 2026.", body), Spacer(1, 10),
          Paragraph("Secretariat of the Stiftungsrat. This extract is for internal use.", small)]
    doc.build(el)


# ------------------------------------------------------------------ mail thread
def write_thread():
    txt = f"""From: {P['treasury']} <treasury@pk-werdinsel.ch>
To: {P['accounting']} <rechnungswesen@pk-werdinsel.ch>; {P['pm']} <portfolio@pk-werdinsel.ch>
Cc: {P['cio']}
Date: Thu, 1 Oct 2026 08:12 +0200
Subject: 2027 standby line: extract and inputs

Noelia, Othmar,

The board wants the facility number on 19 November. I am working from the 30 September extract (manifest PKW-PM-2026-09-30). What I need from you:

- Noelia: confirmation that the notice ledger is complete to 30 September, and the status of the manager statements.
- Othmar: confirmation of the register (any side letters or commitment changes I would not see).

I will run the plan under RL-PM-04 section 5 and bring the term sheet from Lindenhof with it.

Serena

-----Original Message-----
From: {P['accounting']} <rechnungswesen@pk-werdinsel.ch>
To: {P['treasury']}; {P['pm']}
Cc: {P['cio']}
Date: Thu, 1 Oct 2026 11:47 +0200
Subject: RE: 2027 standby line: extract and inputs

Serena,

Ledger is complete to 30.09. Every notice received by then is in, including the three that the managers withdrew and reissued this year (you will see them with status CANCELLED and the reissue under its own number).

Statements: the audited FY2025 capital accounts are all on file and reconciled (sheet Kapitalkonten, 180 rows). The quarterly statements are another matter. We have all Q1 2026 statements. Q2 2026 is still outstanding for three managers (Rosenthal II, Ebersol IV and Juno II), and the Q2 capital account reconciliation has not been done for anyone yet because of the audit and the September week.

The FX in the NAV register is the custodian rate on the booking date, as always. Period-end rates are in the daily file.

Noelia

-----Original Message-----
From: {P['pm']} <portfolio@pk-werdinsel.ch>
To: {P['treasury']}
Cc: {P['cio']}; {P['accounting']}
Date: Fri, 2 Oct 2026 09:30 +0200
Subject: RE: 2027 standby line: extract and inputs

Serena,

Register confirmed, no changes since the June sitting apart from Halvorsen III, which closed in September and will call for the first time in Q4.

For what it is worth: the credit managers have had a very good year of repayments, the 2023-24 vintages are nearly drawn and I would not plan on much from them next year beyond fees. The money will go to Aldringen V, Brantwood IV, Corvisart VIII, Marignane V and the Dunmore and Juno infrastructure funds. If the plan says otherwise I would like to see why before it goes to the board.

Othmar

-----Original Message-----
From: {P['cio']}
To: {P['treasury']}
Date: Fri, 2 Oct 2026 17:05 +0200
Subject: RE: 2027 standby line: extract and inputs

Serena, two things before you go too far.

One, we pay 30 basis points on the whole line whether we draw or not, so every tranche above what we need costs real money. Two, I still think the honest base is each fund's own record. We have every notice since 2015; fit each manager on what it has actually done, all of it, and you will see the pooled rates are a planning fiction. If you land somewhere else, walk me through it first.

L.

--
Pensionskasse Werdinsel, Werdstrasse 21, 8004 Zürich. Diese Nachricht ist vertraulich.
"""
    with open(os.path.join(T, "mail_standby_line_2027.txt"), "w") as fh:
        fh.write(txt)


# ------------------------------------------------------------------ field notes (data dictionary)
def write_field_notes(counts):
    md = f"""# Feldbeschrieb Privatmarkt-Extrakt PKW-PM-2026-09-30

Rechnungswesen, Pensionskasse Werdinsel. Extract of the private-markets ledgers as at 30 September 2026 (close of business).
Prepared for Treasury & Liquidity. Amounts are in the currency stated on each row; no file carries Swiss-franc
translations except where a column says so.

## kapitalabrufe_ausschuettungen_2015-2026.csv ({counts['spine']} rows)

One row per line of a manager notice. A notice has one or more lines.

| column | meaning |
|---|---|
| notice_id | manager's notice number as recorded by us: fund code, CN (capital call) or DN (distribution), sequence. A reissued notice carries the suffix R. |
| fund_id, fund_code | our fund identifier and the short code (register) |
| notice_type | CAPITAL_CALL or DISTRIBUTION |
| notice_date | date on the notice |
| value_date | for a call, the due date for payment; for a distribution, the date the cash was credited to our account |
| status | ISSUED, or CANCELLED where the manager withdrew the notice. A cancelled notice has no cash effect; the manager reissues under a new number. |
| line_no, line_type | line sequence within the notice and its kind: INVESTMENT, MANAGEMENT_FEE, PARTNERSHIP_EXPENSES on calls; RETURN_OF_CAPITAL, REALISED_GAIN, INCOME, IN_KIND on distributions |
| investment_ref | the manager's investment reference the line relates to (register of investments); blank for fees and expenses |
| description | text as entered by the clerk |
| currency | fund currency (ISO 4217); the clerks are not consistent about case |
| amount | amount of the line, positive, two decimals |
| entered_at | when the line was entered in the ledger |
| remarks | free text; used for withdrawals and reissues |

IN_KIND lines are distributions of listed shares at the value stated on the manager's notice; they settle in securities, not cash.

## fondsregister_2026-09-30.xlsx

Sheet Fonds: one row per fund commitment. commitment is in the fund currency. first_close is the fund's first closing; admission_date the closing at which we were admitted; investment_period_end and term_end as per the limited partnership agreement; recycling_months and recycling_basis the recycling clause of the agreement as summarised by Rechnungswesen; lei is the fund's legal entity identifier. status: active (has issued at least one call) or committed. Sheet Strategien: strategy codes. The register carries contractual data only.

## beteiligungsverzeichnis_2026-09-30.csv ({counts['inv']} rows)

One row per investment of a fund, compiled from the managers' quarterly reports. initial_investment_date is the date of the fund's first investment in the company (later tranches do not change it); cost_to_date is the total cost including later tranches; status is HELD, REALISED or REALISED_IN_KIND; realisation_date is the closing date of the sale or repayment.

## kapitalkonten_revidiert_2021-2025.xlsx ({counts['cells']} rows)

Sheet Kapitalkonten: our capital account in each fund as stated in the fund's audited financial statements, one row per fund and financial year-end 31 December 2021 to 2025, in the fund currency: commitment, contributions since inception, distributions since inception, net asset value at the year-end, unfunded commitment, auditor and opinion date. Sheet Erfassung: compilation notes.

## nav_register_quartal.csv ({counts['nav']} rows)

Our NAV register: one row per manager statement received, from the first quarter of 2019. period_end is the statement's period end; statement_type is quarterly report or annual audited; nav_fund_ccy the net asset value in the fund currency; received_date when the statement arrived; booking_date the date Rechnungswesen booked it; fx_rate_booked the custodian reference rate of the booking date; nav_chf_booked the Swiss-franc value booked to the balance sheet at that rate. A statement not yet received has no row.

## fx_referenzkurse_tagesende.csv ({counts['fx']} rows)

Custodian reference rates, business days 2015 to 30 September 2026: Swiss francs per one US dollar (USDCHF) and per one euro (EURCHF). For a date with no row the rate of the preceding business day applies.

## Documents

richtlinie_liquiditaet_privatmarkt_RL-PM-04.docx (the directive, working translation) · term_sheet_lindenhof_standby_2027.pdf · stiftungsrat_protokoll_auszug_2026-09-24.pdf · halbjahresbericht_privatmarkt_2025-H1.pdf (the last semi-annual programme report on file; the H2 2025 report is with the Stiftungsrat secretariat) · mail_standby_line_2027.txt · export_manifest_2026-09-30.json
"""
    with open(os.path.join(T, "feldbeschrieb_privatmarkt_extrakt.md"), "w") as fh:
        fh.write(md)


def write_manifest(counts):
    files = sorted(os.listdir(T))
    man = {
        "extract_id": "PKW-PM-2026-09-30",
        "organisation": "Pensionskasse Werdinsel, Rechnungswesen",
        "as_of": "2026-09-30T18:00:00+02:00",
        "produced": "2026-10-01T07:40:00+02:00",
        "produced_by": P["accounting"],
        "system": "PM-Ledger 4.2 (custodian feed CF-PM), register and NAV register maintained in Rechnungswesen",
        "files": [{"file": f, "size_bytes": os.path.getsize(os.path.join(T, f))} for f in files if not f.startswith(".")],
        "row_counts": {"kapitalabrufe_ausschuettungen_2015-2026.csv": counts["spine"], "beteiligungsverzeichnis_2026-09-30.csv": counts["inv"],
                       "nav_register_quartal.csv": counts["nav"], "fx_referenzkurse_tagesende.csv": counts["fx"], "kapitalkonten_revidiert_2021-2025.xlsx": counts["cells"]},
        "notes": "Ledger complete to 30.09.2026. Quarterly statements Q2 2026 outstanding for three managers at extract date. FY2025 audited capital accounts complete.",
    }
    with open(os.path.join(T, "export_manifest_2026-09-30.json"), "w") as fh:
        json.dump(man, fh, indent=2, ensure_ascii=False)


# ------------------------------------------------------------------ the H2 2025 semi-annual report (context artifact)
def write_semi_annual(pack):
    body, small, head, title = _para_style()
    br = pack.nav_bridge(start=date(2024, 12, 31), end=date(2025, 6, 30))
    doc = SimpleDocTemplate(os.path.join(T, "halbjahresbericht_privatmarkt_2025-H1.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm, invariant=1,
                            title="Halbjahresbericht Privatmarktprogramm 2025 H1", author="Pensionskasse Werdinsel")
    el = [Paragraph("Pensionskasse Werdinsel, Treasury & Liquidity", head), Paragraph("Privatmarktprogramm: Halbjahresbericht 1. Januar bis 30. Juni 2025", title),
          Paragraph("Report to the Stiftungsrat under RL-PM-04 section 7. Figures in thousands of Swiss francs. Presented at the sitting of 25 September 2025.", small), Spacer(1, 8)]
    hdr = ["Strategy", "NAV 31.12.2024", "Capital called", "Distributions", "Valuation and currency", "NAV 30.06.2025"]
    labels = {"BO": "Buyout", "GR": "Growth", "PC": "Private credit", "IN": "Infrastructure", "TOTAL": "Programme"}
    data = [hdr]
    for s in ["BO", "GR", "PC", "IN", "TOTAL"]:
        b = br[s]
        data.append([labels[s]] + [f"{round(b[k] / 1000):,}" for k in ("opening", "calls", "dists", "valuation_fx", "closing")])
    t = Table(data, colWidths=[3.4 * cm, 2.6 * cm, 2.6 * cm, 2.6 * cm, 3.0 * cm, 2.6 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 8.5)]))
    el += [t, Spacer(1, 10),
           Paragraph("The first half of 2025 saw the private-credit funds of the 2023 and 2024 vintages close to the end of their deployment, with the "
                     "first repayments of loans written in 2024 arriving in the second quarter. Distributions ran ahead of calls across the programme for the "
                     "third consecutive half-year. The reserve was not drawn below its floor in the period.", body), Spacer(1, 6),
           Paragraph("Prepared by Treasury & Liquidity from the NAV register, the notice ledger and the custodian rate file. Rounded to the nearest thousand after translation.", small)]
    doc.build(el)
    return br


def write_all(counts, pack):
    write_directive()
    write_term_sheet()
    write_minutes()
    write_thread()
    write_field_notes(counts)
    br = write_semi_annual(pack)
    write_manifest(counts)
    return br
