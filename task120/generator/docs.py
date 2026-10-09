"""The pack's documents and workbooks. Every figure written here is computed upstream from the
records; nothing is typed by hand."""
import datetime as dt

import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from constructions import CLASS_LABELS
import world as Wm

AUTHOR_DOR = "Research and Statistics Section"
AUTHOR_REC = "Revenue Estimating Conference"
AUTHOR_ORR = "Office of Revenue Research"

TABLE_DATES = {2022: dt.datetime(2023, 11, 14, 10, 12), 2023: dt.datetime(2024, 11, 13, 9, 41),
               2024: dt.datetime(2025, 11, 12, 11, 5)}


def _wb(path, author, created):
    wb = xlsxwriter.Workbook(path)
    wb.set_properties({"author": author, "created": created, "company": ""})
    return wb


# ------------------------------------------------------------------ published tables

def household_table(path, year, cells, appendix):
    wb = _wb(path, AUTHOR_REC, TABLE_DATES[year])
    b = wb.add_format({"bold": True})
    t = wb.add_format({"bold": True, "font_size": 12})
    h = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True, "valign": "bottom"})
    n0 = wb.add_format({"num_format": "#,##0"})
    small = wb.add_format({"italic": True, "font_size": 9})
    ws = wb.add_worksheet("Table 1")
    ws.set_column(0, 0, 34)
    ws.set_column(1, 2, 17)
    ws.write(0, 0, "Revenue Estimating Conference", b)
    ws.write(1, 0, f"Household Income Tables, Tax Year {year}", t)
    ws.write(2, 0, "Table 1. Full-year resident household units with federal AGI of $100,000 or more, by AGI class")
    ws.write(4, 0, "Federal AGI class", h)
    ws.write(4, 1, "Household units", h)
    ws.write(4, 2, "Federal AGI ($ thousands)", h)
    row = 5
    for lab in CLASS_LABELS:
        ws.write(row, 0, lab)
        ws.write_number(row, 1, cells[("units", lab)], n0)
        ws.write_number(row, 2, cells[("agi_k", lab)], n0)
        row += 1
    row += 1
    ws.write(row, 0, "All full-year resident household units, total federal AGI ($ thousands)")
    ws.write_number(row, 2, cells[("total_agi_k", "all")], n0)
    row += 2
    notes = [
        "Federal AGI is adjusted gross income as reported on state individual income tax returns, processed returns as of record.",
        "Units are whole counts; AGI is rounded to the nearest $1,000.",
        f"Compiled for the Conference by the State University Fiscal Research Center from Department of Revenue data. Released {TABLE_DATES[year]:%d %B %Y}.",
    ]
    if year == 2024:
        notes.insert(2, "Appendix A gives household units at the top of the distribution for the twelve largest counties.")
    for s in notes:
        ws.write(row, 0, s, small)
        row += 1
    if year == 2024:
        wa = wb.add_worksheet("Appendix A")
        wa.set_column(0, 0, 20)
        wa.set_column(1, 2, 16)
        wa.write(0, 0, f"Household Income Tables, Tax Year {year}", t)
        wa.write(1, 0, "Appendix A. Full-year resident household units with federal AGI of $500,000 or more, twelve largest counties")
        wa.write(3, 0, "County", h)
        wa.write(3, 1, "County code", h)
        wa.write(3, 2, "Household units", h)
        r = 4
        for name, code in appendix:
            wa.write(r, 0, name)
            wa.write_string(r, 1, code)
            wa.write_number(r, 2, cells[("county_units_500k", code)], n0)
            r += 1
        wa.write(r + 1, 0, "Counties ranked by full-year resident returns processed for the tax year.", small)
    wb.close()


DEPT_CLASSES = [("Zero or less", None, 1), ("$1 under $10,000", 1, 10_000), ("$10,000 under $25,000", 10_000, 25_000),
                ("$25,000 under $50,000", 25_000, 50_000), ("$50,000 under $75,000", 50_000, 75_000),
                ("$75,000 under $100,000", 75_000, 100_000), ("$100,000 under $200,000", 100_000, 200_000),
                ("$200,000 under $500,000", 200_000, 500_000), ("$500,000 under $1,000,000", 500_000, 1_000_000),
                ("$1,000,000 or more", 1_000_000, None)]


def dept_table_rows(r25):
    agi = r25.federal_agi.to_numpy()
    rows = []
    for lab, lo, hi in DEPT_CLASSES:
        m = ((agi >= lo) if lo is not None else True) & ((agi < hi) if hi is not None else True)
        rows.append((lab, int(m.sum()), int(agi[m].sum())))
    rows.append(("All returns", int(len(agi)), int(agi.sum())))
    return rows


def dept_table(path, rows):
    wb = _wb(path, AUTHOR_DOR, dt.datetime(2026, 10, 22, 16, 40))
    b = wb.add_format({"bold": True})
    t = wb.add_format({"bold": True, "font_size": 12})
    h = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True, "valign": "bottom"})
    n0 = wb.add_format({"num_format": "#,##0"})
    tot = wb.add_format({"num_format": "#,##0", "top": 1, "bold": True})
    totl = wb.add_format({"top": 1, "bold": True})
    small = wb.add_format({"italic": True, "font_size": 9})
    ws = wb.add_worksheet("AGI class")
    ws.set_column(0, 0, 28)
    ws.set_column(1, 2, 20)
    ws.write(0, 0, "Department of Revenue, Individual Income Tax", b)
    ws.write(1, 0, "Returns Processed by AGI Class, Tax Year 2025", t)
    ws.write(2, 0, "Returns processed, all filers (full-year residents, part-year residents and nonresidents)")
    ws.write(4, 0, "Federal AGI class", h)
    ws.write(4, 1, "Returns", h)
    ws.write(4, 2, "Federal AGI (dollars)", h)
    r = 5
    for lab, c, a in rows:
        last = lab == "All returns"
        ws.write(r, 0, lab, totl if last else None)
        ws.write_number(r, 1, c, tot if last else n0)
        ws.write_number(r, 2, a, tot if last else n0)
        r += 1
    ws.write(r + 1, 0, "Processed through 22 October 2026. Counts are returns; a joint return is one return.", small)
    ws.write(r + 2, 0, "Federal AGI as reported on the state return.", small)
    wb.close()


def recon_table(path, rows_distinct):
    rows, distinct = rows_distinct
    wb = _wb(path, AUTHOR_DOR, dt.datetime(2026, 10, 22, 15, 55))
    t = wb.add_format({"bold": True, "font_size": 12})
    h = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True, "valign": "bottom"})
    n0 = wb.add_format({"num_format": "#,##0"})
    tot = wb.add_format({"num_format": "#,##0", "top": 1, "bold": True})
    totl = wb.add_format({"top": 1, "bold": True})
    small = wb.add_format({"italic": True, "font_size": 9})
    ws = wb.add_worksheet("By channel")
    ws.set_column(0, 0, 26)
    ws.set_column(1, 4, 18)
    ws.write(0, 0, "Employer annual withholding reconciliations, tax year 2025", t)
    ws.write(1, 0, "Statewide totals of the wage statements filed with reconciliations, by filing channel")
    for j, lab in enumerate(["Filing channel", "Employers", "Wage statements", "State wages ($)", "State income tax withheld ($)"]):
        ws.write(3, j, lab, h)
    r = 4
    for lab, e, s, w, wh in rows:
        ws.write(r, 0, lab)
        for j, v in enumerate((e, s, w, wh), start=1):
            ws.write_number(r, j, v, n0)
        r += 1
    ws.write(r, 0, "All channels", totl)
    ws.write_number(r, 1, distinct, tot)
    ws.write_number(r, 2, sum(x[2] for x in rows), tot)
    ws.write_number(r, 3, sum(x[3] for x in rows), tot)
    ws.write_number(r, 4, sum(x[4] for x in rows), tot)
    ws.write(r + 2, 0, "An employer filing on both channels is counted in each channel and once in all channels. Status at 22 October 2026.", small)
    wb.close()


# ------------------------------------------------------------------ methodology (PDF)

METHODOLOGY = [
    ("h", "1. Purpose"),
    ("p", "The personal income tax forecast that the Revenue Estimating Conference certifies carries the top of the income "
          "distribution in three tiers, because realised capital gains, estimated payments and withholding move differently in "
          "each. This note sets out how the tiers are drawn and re-based, what the tier base holds and how a re-based schedule "
          "is adopted. The Office of Revenue Research maintains it and staffs the Conference."),
    ("h", "2. Tiers"),
    ("p", "The tiers are re-based each autumn on the latest processed tax year. "
          "Tiers are drawn on full-year resident household units at the 10, 5 and 1 per cent marks of household AGI; every such "
          "unit counts in the base whatever its AGI, and each floor is stated to the nearest $1,000. "
          "Tier 1 runs from the 1 per cent floor up, tier 2 from the 5 per cent floor up to the 1 per cent floor, and tier 3 from "
          "the 10 per cent floor up to the 5 per cent floor; each unit sits in the tier its AGI falls in under the adopted floors."),
    ("h", "3. Adoption"),
    ("p", "A tier schedule is adopted only on a construction that reproduces every published cell of the three most recent "
          "Household Income Tables. The finance secretary adopts the schedule on the Office's recommendation, and the Conference "
          "certifies its income tax estimate on the adopted tiers. "
          "The Legislative Fiscal Office draws its household tiers on federal filing units and will put its own schedule beside "
          "the Office's at the certification."),
    ("h", "4. Tier base"),
    ("p", "For each tier the forecast carries, from the re-based year, the estimated-tax receipts at each of the four "
          "instalments, withholding, and net capital gain with its share of the tier's AGI."),
    ("b", "Estimated-tax receipts are cash received toward the tax year; an overpayment credited from a prior year's return is "
          "not a receipt of the year it is credited to. A receipt counts at the first instalment whose due date it arrives by, "
          "and the fourth instalment also takes receipts that arrive after its due date."),
    ("b", "Withholding is measured on employers' wage statements."),
    ("b", "Capital gain is the amount entering AGI."),
    ("h", "5. Sources"),
    ("p", "Processed returns, dependents schedules and the payment and information-return extracts come from the Department of "
          "Revenue's research extracts, whose record layouts define every field. Published tables are the Conference's own."),
]

REVISIONS = [
    ("Sep 2026", "TY2025 is the first year the Office compiles the Household Income Tables and the tier schedule itself; the "
                 "TY2022 to TY2024 tables were compiled for the Conference by the State University Fiscal Research Center "
                 "under the interagency data agreement that ended with the TY2024 tables."),
    ("Sep 2024", "County appendix added to the Household Income Tables."),
    ("Oct 2022", "Withholding added to the tier base."),
    ("Sep 2021", "Note first issued."),
]


def methodology_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                            topMargin=0.9 * inch, bottomMargin=0.9 * inch, invariant=1,
                            title="Income tax tiers: methodology", author=AUTHOR_ORR, subject="", creator=AUTHOR_ORR)
    base = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=14, alignment=TA_LEFT, spaceAfter=6)
    head = ParagraphStyle("h", parent=base, fontName="Times-Bold", fontSize=11, spaceBefore=8, spaceAfter=3)
    bullet = ParagraphStyle("u", parent=base, leftIndent=14, bulletIndent=2)
    title = ParagraphStyle("t", parent=base, fontName="Times-Bold", fontSize=14, leading=18, spaceAfter=2)
    sub = ParagraphStyle("s", parent=base, fontSize=10, textColor=colors.HexColor("#333333"))
    story = [Paragraph("REVENUE ESTIMATING CONFERENCE", sub), Paragraph("Income tax tiers: methodology", title),
             Paragraph("Office of Revenue Research &middot; revised 18 September 2026", sub), Spacer(1, 10)]
    for kind, text in METHODOLOGY:
        if kind == "h":
            story.append(Paragraph(text, head))
        elif kind == "b":
            story.append(Paragraph(text, bullet, bulletText="•"))
        else:
            story.append(Paragraph(text, base))
    story.append(Paragraph("Revision history", head))
    data = [[Paragraph("<b>Date</b>", base), Paragraph("<b>Change</b>", base)]] + \
           [[Paragraph(d, base), Paragraph(c, base)] for d, c in REVISIONS]
    tb = Table(data, colWidths=[0.9 * inch, 5.5 * inch])
    tb.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(tb)
    doc.build(story)


# ------------------------------------------------------------------ record layouts (text)

def record_layouts():
    L = []
    w = L.append
    w("DEPARTMENT OF REVENUE")
    w("Research and Statistics Section")
    w("Individual income tax research extracts: record layouts")
    w("Revision 2026-10, issued with the TY2025 delivery")
    w("")
    w("Amounts are whole dollars. TINs are nine-digit numbers without separators. Dates are YYYY-MM-DD.")
    w("")

    def table(rows):
        for name, typ, desc in rows:
            w(f"  {name:<28}{typ:<9}{desc}")
        w("")
    w("1. Processed returns  (returns_processed_tyYYYY.parquet, one file per tax year)")
    w("   One record per processed state individual income tax return, as of record: an accepted amended return")
    w("   replaces the figures of the return it amends.")
    table([
        ("return_id", "int", "Return document number; the first two digits are the tax year."),
        ("tax_year", "int", "Tax year of the return."),
        ("filer_tin", "num(9)", "TIN of the filer of this return."),
        ("spouse_tin", "num(9)", "TIN of the spouse on a joint return; blank otherwise."),
        ("federal_primary_tin", "num(9)", "TIN of the primary taxpayer on the federal return the state return was prepared"),
        ("", "", "from; equal to filer_tin except on a spouse's separate state return."),
        ("filing_status", "int", "1 single; 2 married filing jointly; 3 married filing a separate state return;"),
        ("", "", "4 head of household; 5 qualifying surviving spouse."),
        ("residency_code", "int", "1 full-year resident; 2 part-year resident; 3 nonresident."),
        ("county_code", "char(3)", "County of residence at filing, state county code; 000 for an address outside the state."),
        ("federal_agi", "int", "Federal adjusted gross income as reported on the state return. The only AGI field the"),
        ("", "", "extract carries."),
        ("state_taxable_income", "int", "State taxable income."),
        ("overpayment_credit_elect", "int", "Overpayment the filer elected to credit to the following year's estimated tax."),
        ("processed_date", "date", "Date the return completed processing."),
    ])
    w("2. Dependents schedule  (dependents_schedule_tyYYYY.parquet, one file per tax year)")
    w("   One record per dependent claimed for the exemption credit on a processed return. The Department accepts")
    w("   one claim for a dependent TIN in a tax year.")
    table([
        ("claimant_return_id", "int", "return_id of the return claiming the dependent."),
        ("dependent_tin", "num(9)", "TIN of the dependent."),
        ("relationship_code", "char(2)", "01 son or daughter; 02 stepchild; 03 foster child; 04 grandchild; 05 parent;"),
        ("", "", "06 brother or sister; 07 other relative; 08 other member of the claimant's home."),
        ("dependent_birth_year", "int", "Year of birth."),
    ])
    w("3. Estimated payments  (estimated_payments_ledger_2025.parquet)")
    w("   Estimated-tax account activity for tax years 2024 and 2025 posted 1 January 2025 to 31 January 2026,")
    w("   from the payments platform. Payments are recorded as received.")
    table([
        ("txn_id", "int", "Transaction number."),
        ("account_tin", "num(9)", "TIN the payment was made under, as reported by the payer."),
        ("tax_year", "int", "Tax year the transaction is posted to."),
        ("txn_type", "char(3)", "ES estimated payment; TRF transfer."),
        ("amount", "int", "A transfer out of a tax year is negative."),
        ("txn_utc", "char(20)", "Timestamp in UTC: for a payment, when the platform received it; for a transfer, when"),
        ("", "", "it posted."),
        ("source_ref", "char", "For a transfer, the return_id or txn_id the amount came from; blank otherwise."),
        ("channel", "char", "EPAY_ACH_DEBIT, CARD or ACH_CREDIT; blank for a transfer."),
    ])
    w("   Estimated-tax instalments for a tax year are due on 15 April, 15 June and 15 September of the tax year")
    w("   and on 15 January of the following year, at 11:59:59 pm Central time. A due date that falls on a Saturday,")
    w("   Sunday or state holiday moves to the next business day.")
    w("")
    w("4. Returned items  (returned_items_2025.csv)")
    w("   Payments returned unpaid by the payer's bank or card issuer in 2025 and January 2026, with any")
    w("   re-presentment of the item.")
    table([
        ("item_id", "int", "Returned item number."),
        ("txn_id", "int", "The payment returned (ledger txn_id)."),
        ("return_reason", "char(3)", "ACH return reason code (R01, R02, R03, R08, R16, R29) or CB for a card chargeback."),
        ("returned_date", "date", "Date the item came back."),
        ("represented_date", "date", "Date the item was presented again; blank if it was not."),
        ("represented_result", "char", "PAID or RETURNED; blank if the item was not presented again."),
    ])
    w("5. TIN match cases  (tin_match_cases.csv)")
    w("   One case for each TIN reported on a payment or a wage statement that matched no filer. A resolved case")
    w("   carries the TIN of the filer the reported number belongs to; an open case carries none.")
    table([
        ("case_id", "int", "Case number."),
        ("reported_tin", "num(9)", "The TIN as reported."),
        ("reported_on", "char", "PAYMENT or WAGE_STATEMENT."),
        ("opened_date", "date", ""),
        ("case_status", "char", "RESOLVED or OPEN."),
        ("resolved_tin", "num(9)", "TIN of the filer; blank for an open case."),
        ("closed_date", "date", "Blank for an open case."),
    ])
    w("6. Schedule D  (schedule_d_extract_ty2025.csv)")
    w("   One record per TY2025 return with a capital gains schedule: the latest version of the schedule received.")
    table([
        ("return_id", "int", ""),
        ("tax_year", "int", ""),
        ("amendment_seq", "int", "0 for the original return, 1 for the first amended return and so on."),
        ("received_date", "date", "Date this version was received."),
        ("net_gain_loss", "int", "Net capital gain or loss on the schedule."),
        ("amount_in_agi", "int", "Capital gain or loss carried to federal AGI."),
    ])
    w("7. Amended returns  (amended_returns_log_ty2025.csv)")
    w("   Every version of each TY2025 return amended to date, the original included, with its disposition. A return's")
    w("   version of record is its latest accepted version.")
    table([
        ("return_id", "int", ""),
        ("amendment_seq", "int", "As in the Schedule D extract."),
        ("received_date", "date", ""),
        ("disposition", "char", "ACCEPTED, REJECTED or PENDING."),
        ("disposition_date", "date", "Blank while pending."),
        ("federal_agi", "int", "Federal AGI on this version."),
        ("net_gain_loss", "int", "Schedule D figures on this version; blank where the return carries no schedule."),
        ("amount_in_agi", "int", ""),
    ])
    w("8. Wage statements")
    w("   Wage statements reach the Department through two channels: electronic submissions on the platform, and")
    w("   paper statements keyed by the capture vendor and delivered in the vendor's layout.")
    w("")
    w("   8a. Electronic  (wage_statements_efile_ty2025.parquet)")
    table([
        ("statement_id", "int", ""),
        ("submission_id", "int", "The employer's submission the statement arrived in."),
        ("employer_ein", "num(9)", ""),
        ("employee_tin", "num(9)", "As reported by the employer."),
        ("tax_year", "int", ""),
        ("state_wages", "int", ""),
        ("state_tax_withheld", "int", "State income tax withheld."),
        ("received_date", "date", ""),
    ])
    w("   8b. Paper, capture vendor layout  (w2_paper_keyed_ty2025.txt), fixed width, one statement a line")
    table([
        ("positions 1-6", "num", "Batch."),
        ("positions 7-10", "num", "Sequence within the batch."),
        ("positions 11-19", "num", "Employer EIN."),
        ("positions 20-28", "num", "Employee TIN as keyed."),
        ("positions 29-32", "num", "Tax year."),
        ("positions 33-43", "num", "State wages, zero filled."),
        ("positions 44-53", "num", "State income tax withheld, zero filled."),
        ("positions 54-61", "num", "Date keyed, YYYYMMDD."),
        ("positions 62-63", "char", "Keyer."),
    ])
    w("9. Employer reconciliations  (employer_reconciliations_ty2025.xlsx)")
    w("   Statewide totals of the annual withholding reconciliations employers file, by filing channel.")
    w("")
    w("10. Withholding deposits  (withholding_deposits_2025.csv)")
    w("   Employer withholding deposits received in calendar 2025.")
    table([
        ("deposit_id", "int", ""),
        ("employer_ein", "num(9)", ""),
        ("deposit_schedule", "char", "SEMIWEEKLY, MONTHLY or QUARTERLY."),
        ("period_end", "date", "End of the payroll period the deposit covers."),
        ("received_date", "date", "Date the deposit was received."),
        ("amount", "int", ""),
    ])
    w("Questions on these layouts: Research and Statistics Section, Department of Revenue.")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ thread

THREAD = """From: Shepard, Brittany (DOR Research and Statistics)
Sent: Friday, October 23, 2026 8:47 AM
To: Reid, Stephanie (ORR)
Cc: Stevenson, Manuel (ORR)
Subject: TY2025 research extract delivered

Stephanie,

The TY2025 research extract is on your share as of this morning: processed returns, the dependents
schedule, the estimated-payment and wage-statement pulls with the returned items and the TIN match
cases, the Schedule D extract and the amended-returns log. The back years, TY2022 to TY2024, are
there in the same layout. I've also dropped in our Returns Processed by AGI Class table for 2025.
It ties to the processed file to the row and the dollar, so if you ever want a check on what we send
you, that's the one I'd trust.

The record layouts were revised for this delivery and are in the folder.

Brittany

________________________________
From: Stevenson, Manuel (ORR)
Sent: Monday, October 26, 2026 10:05 AM
To: Reid, Stephanie (ORR)
Subject: RE: TY2025 research extract delivered

Thanks Brittany.

Stephanie, my view hasn't moved since we talked last week. Every return is a taxpayer, so the floors
should come straight off this year's returns. It's the one count in the building nobody can argue
with, and it's what the secretary will expect to see.

Manuel

________________________________
From: King, Jeffrey (Legislative Fiscal Office)
Sent: Wednesday, October 28, 2026 3:31 PM
To: Reid, Stephanie (ORR)
Subject: Certification packet

Stephanie,

Heads-up for the packet: we'll tier on the federal return again this year. As far as our model is
concerned the federal return is the tax unit, and that's how we've always carried it. Our schedule
goes in beside yours, same as before.

Jeff

________________________________
From: Reid, Stephanie (ORR)
Sent: Thursday, October 29, 2026 9:18 AM
To: Shepard, Brittany (DOR Research and Statistics)
Subject: RE: TY2025 research extract delivered

Brittany, all received, thank you. Does the payment pull run through the January instalment?

Stephanie

________________________________
From: Shepard, Brittany (DOR Research and Statistics)
Sent: Thursday, October 29, 2026 11:02 AM
To: Reid, Stephanie (ORR)
Subject: RE: TY2025 research extract delivered

It does. Anything posted through the end of January is in it.

B.
"""


def intake_rows(info):
    """The office's log of what arrived on the share for the re-base (file, received, from,
    what it holds, records)."""
    return info
