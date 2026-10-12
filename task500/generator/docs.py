"""The documents in task500's pack: the office's standing variance procedure, the two certified statements, the
committee's request thread, the extract field guide and the extract notes. Short and functional."""
from pathlib import Path

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack
import world as W

rl_config.invariant = 1

F_METHOD = "revenue_variance_procedure_rev2023.pdf"
F_STATEMENTS = "certified_variance_statements_fy2024_fy2025.pdf"
F_THREAD = "variance_statement_thread_2026-07.txt"
F_GUIDE = "lodging_extract_field_guide.md"
F_NOTES = "extract_notes.txt"

BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=13.8, spaceAfter=5)
SMALL = ParagraphStyle("small", parent=BODY, fontName="Helvetica", fontSize=7.8, leading=9.8,
                       textColor=colors.HexColor("#444444"))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=7, spaceAfter=3)
HEAD = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=8.6, leading=11, textColor=colors.HexColor("#2F4858"))
P = W.PEOPLE


def pdf(path, story, footer):
    def on_page(cv, doc):
        cv.saveState()
        cv.setFont("Helvetica", 7)
        cv.setFillColor(colors.HexColor("#666666"))
        cv.drawString(0.9 * inch, 0.55 * inch, footer)
        cv.drawRightString(7.6 * inch, 0.55 * inch, "Page %d" % doc.page)
        cv.restoreState()
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.85 * inch)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


def p(t, st=BODY):
    return Paragraph(t, st)


# ---------------------------------------------------------------------------------------------- standing procedure
def procedure(T):
    s = [p("OFFICE OF REVENUE ANALYSIS", HEAD),
         p("Lodging Tax Revenue Variance Statement: Standing Procedure", H1),
         p("Revision of March 2023. Applies to the year-end variance statement the office files with the Joint "
           "Committee on Finance for the state lodging tax and the county option collected with it.", SMALL),
         p("1. The variance", H2),
         p("The variance for a fiscal year is the tax due on the returns filed for the year's twelve monthly periods, "
           "less the adopted forecast for those periods. Returns are taken as originally filed; amended returns post "
           "to the treasury ledger and are reconciled separately."),
         p("2. What the statement names", H2),
         p("Every change in law, rate or administration that took effect in the fiscal year is measured. The "
           "statement names the change that accounts for the largest part of the variance and gives each change's "
           "effect. The part no change accounts for is reported as one line."),
         p("3. Measuring a change", H2),
         p("3.1 Each filer the change touched is compared with a reference group of comparable filers that no change "
           "of the year touched. Reference filers come from outside the touched filer's own region and must have "
           "filed continuously. No reference filer serves more than two touched filers in one statement."),
         p("3.2 For each month from the change's effective month through June, the touched filer's reference "
           "receipts are its taxable receipts in the same month a year earlier, carried forward at its reference "
           "group's growth over the year for that month."),
         p("3.3 The change's effect is the tax on the difference between the touched filers' actual and reference "
           "receipts, at each filer's rate for the month, summed over the touched filers."),
         p("3.4 A change in the tax rate is measured on actual taxable receipts at the old rate and the new rate."),
         p("3.5 Where a change moves receipts from one set of filers to another, as when a marketplace facilitator "
           "begins to collect for its hosts, both sets are measured together as one group, against the hosts' "
           "receipts a year earlier grown at the median month growth of all filers eligible to serve as reference "
           "filers that year."),
         p("4. Reproduction", H2),
         p("Before the procedure is applied to a new year, the office reproduces the reference figures in Appendix B "
           "of the two most recent certified statements. The procedure is not used for a statement unless it "
           "reproduces every Appendix B figure to the dollar."),
         p("5. Presentation", H2),
         p("Figures are computed unrounded. The statement shows effects, the variance and the line no change accounts "
           "for in thousands of dollars, each rounded once."),
         Spacer(1, 8),
         p("Approved by the Director, Office of Revenue Analysis, March 14, 2023.", SMALL)]
    pdf(T / F_METHOD, s, "Office of Revenue Analysis  |  Lodging tax variance statement: standing procedure, rev. 2023")


# ---------------------------------------------------------------------------------------------- certified statements
def statements(T, writer):
    hw, sd = writer.certified["HW"], writer.certified["SD"]

    def k(x):
        return "{:,.0f}".format(abs(x) / 1000)
    s = [p("OFFICE OF REVENUE ANALYSIS", HEAD),
         p("Lodging Tax Revenue Variance Statement, Fiscal Year 2024 (certified)", H1),
         p("Filed with the Joint Committee on Finance on September 10, 2024.", SMALL),
         p("One change took effect in fiscal 2024: the reconstruction of Highway 14 through the North Woods region, "
           "from March 2024, which closed lanes and exits used by the corridor's motels and limited-service hotels."),
         p("Measured under the standing procedure, the reconstruction reduced fiscal 2024 lodging tax by $%s "
           "thousand across %d filers on the corridor. Appendix B lists the reference figures by filer."
           % (k(hw[0]), len(hw[1]))),
         Spacer(1, 6),
         p("Certified: Office of Revenue Analysis", SMALL),
         Spacer(1, 22),
         p("OFFICE OF REVENUE ANALYSIS", HEAD),
         p("Lodging Tax Revenue Variance Statement, Fiscal Year 2025 (certified)", H1),
         p("Filed with the Joint Committee on Finance on September 9, 2025.", SMALL),
         p("One change took effect in fiscal 2025: the opening of the stadium district in Capital City North in "
           "September 2024, with its hotels taking event-night demand from the first home game."),
         p("Measured under the standing procedure, the stadium district added $%s thousand to fiscal 2025 lodging tax "
           "across %d filers in the district. Appendix B lists the reference figures by filer." % (k(sd[0]), len(sd[1]))),
         Spacer(1, 6),
         p("Certified: Office of Revenue Analysis", SMALL)]
    pdf(T / F_STATEMENTS, s, "Office of Revenue Analysis  |  Certified variance statements FY2024 and FY2025")


# ---------------------------------------------------------------------------------------------- thread
def thread(T):
    text = """From: %(committee)s
To: %(director)s
Date: Tue, 14 Jul 2026 09:12:44 -0500
Subject: FY2026 lodging tax variance statement

Thomas,

The committee takes the fiscal 2026 lodging tax variance statement at the September 15 hearing. Members will want
the statement in the usual form, the change it names and each change's effect, and the chair asked that the cash
numbers in the treasury's monthly report be reconciled to it this year, since that is what members have been reading
all spring.

Erica

------------------------------------------------------------
From: %(accounting)s
To: %(director)s
Date: Mon, 10 Aug 2026 16:03:12 -0500
Subject: RE: FY2026 lodging tax variance statement

The treasury ledger for lodging tax deposits, July 2024 through July 2026, is in the folder with the returns extract.
The monthly report's collections are deposits booked in the month, net of refunds, with penalty and interest kept out.
Amendments post as their own lines.

Rachel

------------------------------------------------------------
From: %(analyst)s
To: %(director)s
Date: Fri, 14 Aug 2026 15:41:30 -0500
Subject: RE: FY2026 lodging tax variance statement

The returns extract for fiscal 2023 through 2026 is pulled, with the filer register, the change list and Appendix B
of the last two statements. The two facilitators file one return line per county.

Paul
""" % P
    (T / F_THREAD).write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------------------------- field guide
def field_guide(T):
    text = """# Lodging extract field guide

Office of Revenue Analysis. Describes the returns extract, the filer register, the treasury ledger and the forecast
file used for the year-end variance statement. Amounts are in dollars.

## %(register)s

One row per filer holding a lodging license at any time since July 2022.

| Field | Meaning |
|---|---|
| filer_id | lodging tax account |
| class | FS full-service hotel, LS limited-service hotel, ES extended-stay hotel, MO motel, BB bed and breakfast or inn, CG campground or RV park, STR short-term rental host, PF marketplace facilitator |
| rooms_or_units | rooms, sites or rental units on the license; blank for facilitators |
| region | tourism region |
| county | county of the property; Statewide for facilitators |
| license_from, license_to | license period; license_to blank while the license is open |

## %(returns)s

One row per filer, monthly period and county, as originally filed. A filer with no row for a month filed no return
for it. Facilitators file one line per county for the receipts they collected for their hosts.

| Field | Meaning |
|---|---|
| period | the month the receipts were earned |
| taxable_receipts | receipts subject to tax |
| tax_rate | state rate plus the county option for the county |
| tax_due | tax_rate times taxable_receipts |
| filed_date | date the return was received |

## %(ledger)s

One row per deposit or adjustment booked by the treasury, July 2024 through July 2026.

| Field | Meaning |
|---|---|
| deposit_date | date the treasury booked the line |
| period | the return period the line belongs to |
| type | TAX payment of tax due; PEN_INT penalty and interest on a late return; REFUND refund of an overpayment (negative); AMEND adjustment from an amended return |
| amendment_seq | A1, A2 for a return's first and second amendment |

An amended return restates the whole difference from the return as originally filed, so a second amendment replaces
the first rather than adding to it.

## %(report)s

The adopted fiscal 2026 forecast of tax due by monthly period (December 2024 consensus).

## %(changes)s

The changes the variance statements measured in fiscal 2024 and fiscal 2025, and the changes that took effect in
fiscal 2026.

## %(appendix)s

Appendix B of the certified fiscal 2024 and fiscal 2025 statements: the touched filers, their actual and reference
taxable receipts over each statement's window, and the tax effect.
""" % dict(register=pack.F_REGISTER, returns=pack.F_RETURNS, ledger=pack.F_LEDGER, report=pack.F_REPORT,
           changes=pack.F_CHANGES, appendix=pack.F_APPENDIX)
    (T / F_GUIDE).write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------------------------- extract notes
def notes(T):
    import csv
    def n(f):
        with open(T / f, newline="") as fh:
            return "{:,}".format(sum(1 for _ in fh) - 1)
    files = [(pack.F_REGISTER, "Department of Revenue licensing system", "2026-08-14", n(pack.F_REGISTER)),
             (pack.F_RETURNS, "Department of Revenue returns processing", "2026-08-14", n(pack.F_RETURNS)),
             (pack.F_LEDGER, "State treasury, revenue accounting", "2026-08-10", n(pack.F_LEDGER)),
             (pack.F_REPORT, "Office of Revenue Analysis, December 2024 consensus forecast", "2024-12-16",
              n(pack.F_REPORT)),
             (pack.F_CHANGES, "Office of Revenue Analysis", "2026-08-14", n(pack.F_CHANGES)),
             (pack.F_APPENDIX, "Certified statements, Appendix B", "2025-09-09", "2 sheets"),
             (F_METHOD, "Office of Revenue Analysis", "2023-03-14", "2 pages"),
             (F_STATEMENTS, "Joint Committee on Finance filings", "2025-09-09", "2 statements"),
             (F_THREAD, "Email, director's mailbox", "2026-08-14", "3 messages"),
             (F_GUIDE, "Office of Revenue Analysis", "2026-08-14", "")]
    lines = ["Fiscal 2026 lodging tax variance statement: working folder",
             "Compiled by %s, Office of Revenue Analysis, 14 August 2026" % P["analyst"], "",
             "File | Source | As of | Rows", "-" * 72]
    lines += ["%s | %s | %s | %s" % f for f in files]
    lines += ["", "Returns and ledger lines are confidential taxpayer information held under the state tax code and "
                  "are shared here for the statement only. Filer identifiers are account numbers, not names."]
    (T / F_NOTES).write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(T, m=None, writer=None):
    T = Path(T)
    procedure(T)
    statements(T, writer)
    thread(T)
    field_guide(T)
    notes(T)
