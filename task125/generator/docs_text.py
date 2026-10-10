"""The pack's documents: the audit methodology and statements, the exchequer's run book, the Shared Lives
rate schedule, the closure notice, the scheme note, Fernhollow's terms, order, variation and service
report, the call-off correspondence, the working papers index and the internal audit plan."""
import datetime as dt

import params as PR
import writers as WR
from world import DEPTS, DEPT_ORDER

COUNCIL = "Wealdmoor County Council"
FH = "Fernhollow Assurance Ltd"
PP = PR.PEOPLE


def methodology(path, when):
    blocks = [
        ("h", "1. Purpose"),
        ("p", "Internal Audit runs a first-two-digit test over the council's outgoing payments once each financial "
              "year has closed. The test is a selection tool. It tells the exchequer where in each department's "
              "payments the frequency of leading digits departs most from the Benford distribution, so that "
              "post-payment examination can be pointed at those payments. A flagged cell is not a finding."),
        ("h", "2. The test"),
        ("p", "The test is applied to payments as made, by department and financial year, over complete decades "
              "only, so that every two-digit cell from 10 to 99 can be reached equally. Each payment is placed in "
              "the cell given by the first two digits of its amount."),
        ("p", "The expected count for a cell is the Benford proportion for that cell, log10(1 + 1/d), multiplied "
              "by the number of the department's payments tested in the year."),
        ("p", "The mean absolute deviation (MAD) is the average, over the 90 cells, of the absolute difference "
              "between the observed proportion of payments in the cell and its Benford proportion."),
        ("h", "3. Flagged cells"),
        ("p", "A cell is flagged when its count exceeds the expected count by more than half and by at least 30 "
              "payments."),
        ("h", "4. Statement and reproduction"),
        ("p", "For each year Internal Audit publishes a digit-conformity statement giving, for each department, the "
              "payments tested and the MAD, and the MAD for the council's payments taken together. MADs are "
              "published to five decimal places. The statement is published in July of the following year. "
              "Flagged cells are notified to the head of exchequer services and are not published."),
        ("p", "A screen used to set flagged cells must reproduce every figure in the published statement for the "
              "year it is run on."),
        ("h", "5. Use in a plan year"),
        ("p", "In a plan year the filter routes every payment of 1,000 pounds or more in a cell its department "
              "exceeded on the screen of the latest year whose statement is published when the call-off is "
              "placed."),
        ("h", "6. Departments"),
        ("p", "The test covers the ten directorates that make payments through the council's creditor and "
              "client payment systems: %s." % ", ".join(DEPTS[d][0] for d in DEPT_ORDER)),
        ("h", "7. Review"),
        ("p", "This methodology was approved by the Audit and Governance Committee on 19 March 2023 and is "
              "reviewed every three years. Queries to %s, Head of Internal Audit." % PP["audit"]),
    ]
    WR.write_pdf(path, "Payment digit screen: methodology (version 3.1)", "Internal Audit, %s" % COUNCIL,
                 "Approved March 2023. Owner: %s" % PP["audit"], blocks, PP["audit"], when, COUNCIL)


def statements(path, st, when):
    blocks = []
    pub = {"2023/24": "12 July 2024", "2024/25": "11 July 2025", "2025/26": "10 July 2026"}
    for fy in PR.SCREEN_YEARS:
        blocks.append(("h", "Digit-conformity statement %s (published %s)" % (fy, pub[fy])))
        blocks.append(("p", "Payments made between 1 April %s and 31 March %s, tested under the payment digit "
                            "screen methodology (version 3.1)." % (fy[:4], int(fy[:4]) + 1)))
        rows = [["Department", "Payments tested", "MAD"]]
        for d in DEPT_ORDER:
            rows.append([DEPTS[d][0], "{:,}".format(st[(fy, d, "tested")]), st[(fy, d, "mad")]])
        rows.append(["Council (all departments)", "", st[(fy, "ALL", "mad")]])
        blocks.append(("table", {"rows": rows, "widths": [200, 110, 80]}))
    blocks.append(("small", "Flagged cells are notified to the head of exchequer services and are not published. "
                            "Statements are as published; none has been revised."))
    WR.write_pdf(path, "Digit-conformity statements, 2023/24 to 2025/26", "Internal Audit, %s" % COUNCIL,
                 "Head of Internal Audit: %s" % PP["audit"], blocks, PP["audit"], when, COUNCIL)


def run_book(path, when):
    blocks = [
        ("meta", "Exchequer Services. Owner: %s. Approved by %s, Head of Exchequer Services. Version 2.4, "
                 "June 2024." % (PP["analyst"], PP["requester"])),
        ("h", "1. What the filter does"),
        ("p", "The digit filter screens outgoing BACS payments against the flagged cells Internal Audit notifies "
              "for the call-off year and routes the payments that fall in them to the framework provider for "
              "post-payment examination. The cells applied change only when a new call-off is placed."),
        ("h", "2. Monthly runs"),
        ("p", "Each monthly run screens the BACS files submitted in the month. The scheduled run is started "
              "after the 16:00 submission deadline on the last working day of the month and is logged on "
              "completion with the payments screened in range and routed, by department and cell."),
        ("p", "Each run sends one batch per department to the provider through the secure transfer folder, with "
              "the batch reference WCC-<run>-<department>. The provider acknowledges batches on the next working "
              "day."),
        ("h", "3. Re-runs"),
        ("p", "If a file screened in a run is corrected and resubmitted, the run is repeated. The repeat replaces "
              "the run: its batches go to the provider in place of the earlier batches, which are withdrawn "
              "before examination."),
        ("h", "4. Supplementary runs"),
        ("p", "A file accepted by the bureau after the scheduled run has started is screened in a supplementary "
              "run, logged against the month in which the file was submitted. Its routings are added to that "
              "month's."),
        ("h", "5. Checks after each run"),
        ("p", "Tie the payments screened in range to the BACS file totals for the month before the batches are "
              "released. Any difference is investigated before release and noted on the run sheet. Keep the run "
              "sheet with the month's BACS reports for six years."),
        ("h", "6. Contacts"),
        ("p", "Exchequer Services: %s (filter runs), %s (head of service). Provider: %s service desk, "
              "examinations@fernhollow-assurance.co.uk." % (PP["analyst"], PP["requester"], FH)),
    ]
    WR.write_docx(path, "Digit filter run book", blocks, PP["analyst"], when, COUNCIL)


def rate_schedule(path, when):
    rows = [["Placement type", "Weekly rate (GBP)"]]
    for k in ("B1", "B2", "B3", "SDs", "SDe", "SDc"):
        rows.append([PR.RATE_LABEL[k], "%d.00" % PR.RATES[k]])
    sb = [["Short breaks", "Nightly rate (GBP)"], ["Short break, band A", "68.50"], ["Short break, band B", "74.00"],
          ["Short break, band C", "88.50"]]
    blocks = [
        ("p", "These rates are paid to approved Shared Lives carers under the five-year carer rates settlement "
              "agreed with the Wealdmoor Shared Lives Carers' Forum in March 2023. They apply from 1 April 2023 "
              "and are held at these levels to 31 March 2028."),
        ("table", {"rows": rows, "widths": [250, 120]}),
        ("p", "Carer payments are made four-weekly in arrears by BACS. Each run pays the four weeks ending on its "
              "payment date."),
        ("table", {"rows": sb, "widths": [250, 120]}),
        ("p", "Short-break claims are paid on the next creditor run after the claim is approved."),
        ("small", "Adult Social Care, Shared Lives scheme. Scheme manager: %s. Issued 31 March 2023." %
         PP["sl_manager"]),
    ]
    WR.write_pdf(path, "Shared Lives carer rates 2023/24 to 2027/28", "Adult Social Care, %s" % COUNCIL, "",
                 blocks, PP["sl_manager"], when, COUNCIL)


def _eml(headers, body):
    out = []
    for k, v in headers:
        out.append("%s: %s" % (k, v))
    out.append("MIME-Version: 1.0")
    out.append('Content-Type: text/plain; charset="utf-8"')
    out.append("Content-Transfer-Encoding: 8bit")
    out.append("")
    out.append(body.rstrip("\n"))
    return "\n".join(out) + "\n"


def closure_notice(path):
    body = """Colleagues,

As trailed at the January commissioning board, the Home First Step-Down service will close on 31 March 2027,
when the hospital discharge funding that pays for it ends. The ICB has confirmed there is no successor
allocation for 2027/28.

What this means in practice:

- No new step-down placements will be made from 1 March 2027.
- Every guest currently in a step-down placement will have moved on by 31 March 2027, either home with a
  package of care or into residential or extra-care provision. The Shared Lives team is working through each
  guest's plan with the discharge hub.
- Long-term Shared Lives placements are not affected.

The step-down budget lines will be closed in the 2027/28 budget build. Please pass this on to anyone in your
teams who needs it.

Thanks

Adam White
Commissioning Manager, Adult Social Care
Wealdmoor County Council
County Hall, Wealdmoor
"""
    hdr = [("Message-ID", "<20270114101532.4471.adam.white@wealdmoor.gov.uk>"),
           ("Date", "Thu, 14 Jan 2027 10:15:32 +0000"),
           ("From", "Adam White <adam.white@wealdmoor.gov.uk>"),
           ("To", "ASC Finance Business Partners <asc.finance@wealdmoor.gov.uk>"),
           ("Cc", "Exchequer Services <exchequer.services@wealdmoor.gov.uk>, Bethan Carpenter "
                  "<bethan.carpenter@wealdmoor.gov.uk>"),
           ("Subject", "Home First Step-Down: service closes 31 March 2027")]
    WR.write_text(path, _eml(hdr, body))


def scheme_note(path, when):
    blocks = [
        ("meta", "Housing Support. Prepared by %s, Finance Manager, for the exchequer's records. "
                 "September 2025." % PP["hs"]),
        ("h", "What the scheme pays"),
        ("p", "Tenancy Sustainment Payments help households moving on from supported housing into a tenancy of "
              "their own with rent, service charges and set-up costs while the tenancy beds in. Each household is "
              "awarded a fixed monthly amount, set at award from the household's rent and circumstances, and paid "
              "to the tenant by BACS on the 15th of each month (or the working day before). The first payment is "
              "made in the month the award is approved."),
        ("h", "Rounds"),
        ("p", "The scheme has run in two rounds. The 2021 round took applications from July 2021 to June 2022. "
              "The 2024-25 round opened in July 2024 and closed to new applications on 30 June 2025. No further "
              "round is provided for in the medium-term financial strategy 2026 to 2030."),
        ("h", "Controls"),
        ("p", "Awards are approved by the Housing Support panel and every award is reviewed by Internal Audit in "
              "its annual sample. Payments are made from the client payments system and appear in the spending "
              "file under Housing Support, Tenancy Sustainment, with the recipient's name redacted."),
        ("h", "Records"),
        ("p", "The case system holds one row per payment, keyed by case reference, with the date the award was "
              "approved. An extract is supplied to Exchequer Services on request."),
    ]
    WR.write_docx(path, "Tenancy Sustainment Payments: scheme note", blocks, PP["hs"], when, COUNCIL)


def framework_terms(path, when):
    c = [
        ("h", "4. Call-off orders"),
        ("p", "4.1 The customer places one call-off order for each financial year, stating the number of routed "
              "payments it orders for examination. The quarterly allocation is one quarter of the order."),
        ("p", "4.2 The provider's indicative volume for a call-off is the customer's routed count for its latest "
              "closed year, as recorded in the customer's filter run log."),
        ("p", "4.3 A call-off may be varied by written variation signed by both parties. The call-off as varied "
              "is the order of record from the date the variation takes effect."),
        ("h", "5. Batches"),
        ("p", "5.1 Routed payments are delivered in batches through the secure transfer folder. The provider "
              "acknowledges each batch, examines each payment received and returns unexamined any payment for "
              "which remittance evidence is not supplied within ten working days."),
        ("p", "5.2 Each batch is charged per payment examined, with a minimum charge of 25 examinations per batch."),
        ("p", "5.3 A batch withdrawn by the customer before examination, and a payment returned unexamined, are "
              "not charged."),
        ("h", "6. Charges"),
        ("p", "6.1 Examinations are reckoned against the quarter of the run month in which the payments were "
              "routed."),
        ("p", "6.2 Examinations charged in a quarter beyond the quarter's allocation are charged at the premium "
              "rate."),
        ("p", "6.3 Allocation not used in a quarter is charged as unused volume at 40 per cent of the base rate in "
              "force in that quarter."),
        ("p", "6.4 Rates are those of the rate card in force on the date a batch is received."),
        ("h", "7. Invoicing"),
        ("p", "7.1 The provider invoices monthly in arrears, at the base rate, for batches whose examination was "
              "completed in the month. The premium element and any unused-volume charge are settled by a "
              "quarterly reconciliation invoice."),
        ("p", "7.2 Credit notes reference the invoice they credit; a replacement invoice references the invoice it "
              "replaces."),
        ("h", "8. Service reporting"),
        ("p", "8.1 The provider issues a quarterly service report within six weeks of the quarter end."),
    ]
    WR.write_pdf(path, "Payment Assurance Services Framework, Lot 2: call-off terms (extract, clauses 4 to 8)",
                 "Framework reference PASF-2023-L2. Customer: %s. Provider: %s" % (COUNCIL, FH),
                 "Terms dated 1 April 2023", c, PP["provider"], when, FH)


def order_and_variation(path, when):
    blocks = [
        ("h", "Call-off order WCC/FA/2025-26"),
        ("table", {"rows": [["Field", "Entry"], ["Customer", COUNCIL], ["Provider", FH],
                            ["Framework", "PASF-2023-L2, Lot 2 post-payment examination"],
                            ["Period", "1 April 2025 to 31 March 2026"],
                            ["Order quantity", "{:,} routed payments".format(PR.ORDER_2526)],
                            ["Quarterly allocation", "{:,} routed payments".format(PR.ALLOC_ORIG)],
                            ["Placed by", "%s, Head of Exchequer Services" % PP["requester"]],
                            ["Date", "14 March 2025"]], "widths": [140, 300]}),
        ("p", "Placed under clause 4.1 of the call-off terms. Rates per the 2025/26 rate card."),
        ("h", "Variation No. 1 to call-off WCC/FA/2025-26"),
        ("p", "Following the mid-year review meeting on 9 September 2025 the parties agree that the quarterly "
              "allocation for the quarters beginning 1 October 2025 and 1 January 2026 is increased to "
              "{:,} routed payments per quarter, with effect from 1 October 2025. All other terms of the "
              "call-off are unchanged.".format(PR.ALLOC_VARIED)),
        ("table", {"rows": [["Signed for", "Name", "Date"],
                            [COUNCIL, "%s, Category Manager, Procurement" % PP["procurement"], "19 September 2025"],
                            [FH, "%s, Service Delivery Manager" % PP["fh_service"], "22 September 2025"]],
                   "widths": [150, 200, 100]}),
    ]
    WR.write_pdf(path, "Call-off order 2025/26 and Variation No. 1", "Exchequer Services, %s" % COUNCIL, "",
                 blocks, PP["requester"], when, COUNCIL)


def service_report_q2(path, q2, when):
    rows = [["Measure", "July to September 2025 routings"],
            ["Batches received", str(q2["batches"])],
            ["Payments received", "{:,}".format(q2["received"])],
            ["Returned unexamined (evidence not supplied)", str(q2["returned"])],
            ["Payments examined", "{:,}".format(q2["examined"])],
            ["Examinations charged", "{:,}".format(q2["charged"])],
            ["Median working days, acknowledgement to completion", str(q2["median_days"])]]
    blocks = [
        ("p", "Quarterly service report under clause 8.1 for %s. Figures are for the batches routed in the "
              "customer's July, August and September 2025 runs." % COUNCIL),
        ("table", {"rows": rows, "widths": [280, 160]}),
        ("p", "Exceptions raised in the quarter: none. Payments returned unexamined were notified to Exchequer "
              "Services at the time of return."),
        ("small", "Prepared by %s, Service Delivery Manager, %s. Issued 6 November 2025." %
         (PP["fh_service"], FH)),
    ]
    WR.write_pdf(path, "Service report, quarter 2 2025/26", FH, "", blocks, PP["fh_service"], when, FH)


def calloff_thread(path):
    body = """Thanks both. Short answers are fine.
Tina

________________________________
From: Wendy Lyons <wendy.lyons@wealdmoor.gov.uk>
Sent: 01 March 2027 14:06
To: Tina Rogers <tina.rogers@wealdmoor.gov.uk>
Cc: Pauline Pollard <pauline.pollard@wealdmoor.gov.uk>
Subject: RE: FW: Wealdmoor 2027/28 call-off

Tina, from the filter side: Shared Lives has paid the same carers the same amounts for three years, so
nothing has moved there that I can see in the runs. I'll have the 2025/26 log tidied by Wednesday if you
want it for the order note.
Wendy

________________________________
From: Pauline Pollard <pauline.pollard@wealdmoor.gov.uk>
Sent: 01 March 2027 11:41
To: Tina Rogers <tina.rogers@wealdmoor.gov.uk>
Cc: Wendy Lyons <wendy.lyons@wealdmoor.gov.uk>
Subject: RE: FW: Wealdmoor 2027/28 call-off

Hi Tina,

Our scheme payments are approved and audited every year, there's nothing in them for your filter. I've
said this before! Happy to send the case extract again if it helps.
Pauline

________________________________
From: Tina Rogers <tina.rogers@wealdmoor.gov.uk>
Sent: 01 March 2027 09:12
To: Wendy Lyons <wendy.lyons@wealdmoor.gov.uk>; Pauline Pollard <pauline.pollard@wealdmoor.gov.uk>
Subject: FW: Wealdmoor 2027/28 call-off

Morning both. Douglas's note below. The order goes to Fernhollow on Friday 12th and the quantity is mine to
set. Before I do, is anything changing in your areas that I should know about?
Tina

________________________________
From: Douglas Harris <douglas.harris@fernhollow-assurance.co.uk>
Sent: 26 February 2027 16:48
To: Tina Rogers <tina.rogers@wealdmoor.gov.uk>
Subject: Wealdmoor 2027/28 call-off

Dear Tina,

Ahead of the call-off for 2027/28, a reminder that we'd like the order by Friday 12 March so we can book
examiner time for April. As usual we would size on your routed count for your latest closed year, which is
how the framework sets the indicative volume. In our experience volumes don't move much year to year, and
ordering on last year's number keeps everyone out of the premium band.

Happy to talk it through on a call if useful.

Kind regards,

Douglas Harris
Account Director, Local Government
Fernhollow Assurance Ltd
"""
    hdr = [("Message-ID", "<20270301142233.9921.tina.rogers@wealdmoor.gov.uk>"),
           ("In-Reply-To", "<20270301140611.3310.wendy.lyons@wealdmoor.gov.uk>"),
           ("Date", "Mon, 01 Mar 2027 14:22:33 +0000"),
           ("From", "Tina Rogers <tina.rogers@wealdmoor.gov.uk>"),
           ("To", "Wendy Lyons <wendy.lyons@wealdmoor.gov.uk>, Pauline Pollard <pauline.pollard@wealdmoor.gov.uk>"),
           ("Subject", "RE: FW: Wealdmoor 2027/28 call-off")]
    WR.write_text(path, _eml(hdr, body))


def audit_plan(path, when):
    rows = [["Ref", "Audit", "Directorate", "Quarter", "Days"],
            ["26-01", "Payment digit screen 2025/26: statement and notification of cells", "Corporate Resources",
             "Q1-Q2", "12"],
            ["26-02", "Creditor payments: duplicate payment review", "Corporate Resources", "Q2", "15"],
            ["26-03", "Shared Lives: carer approval and annual review compliance", "Adult Social Care", "Q3", "10"],
            ["26-04", "Direct payments: audit of recipient accounts", "Adult Social Care", "Q2", "18"],
            ["26-05", "Highways term contract: valuation and certification", "Highways & Transport", "Q3", "20"],
            ["26-06", "Waste disposal contract: performance deductions", "Waste & Environment", "Q4", "12"],
            ["26-07", "Schools' financial value standard returns", "Education & Skills", "Q1", "8"],
            ["26-08", "Fire & Rescue: fleet and equipment procurement", "Fire & Rescue", "Q4", "10"],
            ["26-09", "Tenancy Sustainment Payments: annual award sample", "Housing Support", "Q3", "6"],
            ["26-10", "Payroll: starters, leavers and variations", "Corporate Resources", "Q1", "14"],
            ["26-11", "Cyber security: backup and recovery testing", "Corporate Resources", "Q4", "15"],
            ["26-12", "Follow-up of agreed actions", "All", "Q1-Q4", "25"]]
    blocks = [
        ("meta", "Internal Audit. Prepared by %s, Audit Manager, for the Audit and Governance Committee of 23 March "
                 "2026. Head of Internal Audit: %s." % (PP["audit_mgr"], PP["audit"])),
        ("p", "The plan below sets out the assurance work for 2026/27 against the risk register and the "
              "committee's priorities. Days are audit days; contingency of 20 days is held separately."),
        ("table", rows),
        ("p", "Changes during the year are reported to the committee at each meeting."),
    ]
    WR.write_docx(path, "Internal Audit plan 2026/27", blocks, PP["audit_mgr"], when, COUNCIL)


INDEX_ROWS = [
    # key, owner, source, as at, coverage
    ("spine", "Exchequer Services", "Published spending file (Transparency Code), cut from the creditor and client "
     "payment systems", "01/03/2027", "Payments dated 01/04/2023 to 25/02/2027"),
    ("tsp", "Housing Support", "Case system extract supplied by Pauline Pollard", "02/03/2027",
     "Every Tenancy Sustainment payment, July 2021 to February 2027"),
    ("statements", "Internal Audit", "Published statements", "10/07/2026", "2023/24, 2024/25 and 2025/26"),
    ("method", "Internal Audit", "Methodology as approved", "19/03/2023", "Current version"),
    ("runlog", "Exchequer Services", "Filter run log", "07/04/2026", "Runs for April 2025 to March 2026"),
    ("runbook", "Exchequer Services", "Procedure document", "28/06/2024", "Current version"),
    ("calendar", "Exchequer Services", "Payment calendar workbook", "15/01/2027", "2025/26 to 2027/28"),
    ("rates", "Adult Social Care", "Rate schedule as issued", "31/03/2023", "2023/24 to 2027/28"),
    ("closure", "Adult Social Care", "Email as received", "14/01/2027", "Single notice"),
    ("scheme", "Housing Support", "Scheme note", "22/09/2025", "Current"),
    ("terms", "Fernhollow / Procurement", "Framework call-off terms, clauses 4 to 8", "01/04/2023", "Framework term"),
    ("ratecards", "Fernhollow", "Rate cards as supplied", "17/02/2026", "2025/26 and 2026/27"),
    ("order", "Exchequer Services", "Order and variation as signed", "22/09/2025", "2025/26 call-off"),
    ("invoices", "Exchequer Services", "Accounts payable extract, supplier Fernhollow Assurance Ltd, examination "
     "invoices and credit notes", "04/06/2026", "Documents for batches routed in 2025/26 runs"),
    ("acks", "Fernhollow", "Provider portal export", "03/06/2026", "Batches routed in 2025/26 runs"),
    ("q2report", "Fernhollow", "Quarterly service report", "06/11/2025", "Quarter 2 2025/26"),
    ("thread", "Exchequer Services", "Email thread as held", "01/03/2027", "2027/28 call-off"),
    ("auditplan", "Internal Audit", "Committee paper", "23/03/2026", "2026/27"),
    ("hsf", "Housing Support", "Allocation workbook", "12/05/2026", "2026/27"),
]

FIELD_NOTES = """
FIELD NOTES

{spine}
  One row per payment, as published under the Local Government Transparency Code. Payments are published
  where the net amount is 500 pounds or more; credit notes of 500 pounds or more are published as negative
  amounts.
  department, service_area, expense_type: the council's reporting structure at the date of payment.
  supplier_name: the payee; payments to individuals show REDACTED - PERSONAL DATA.
  vendor_no: the council's supplier number. A payee keeps one vendor number throughout the file.
  transaction_ref: the payment document number, unique in the file.
  payment_date: the date the payment is made, dd/mm/yyyy.
  net_amount: the amount excluding VAT, in pounds.
  vat_amount: VAT on the payment, in pounds; 0.00 where none is charged.

{tsp}
  One row per payment from the Housing Support case system.
  case_ref: the award; scheme_round: the round the award was made in; approved_on: the date the award was
  approved; payment_date: yyyy-mm-dd; amount: pounds.

{runlog}
  One row per run, department and applied cell (one row with a blank cell for a department with none).
  payments_in_range: the department's payments screened in range in the run; it repeats on each cell line.
  payments_routed: payments routed from that cell. batch_ref: the batch the department's routings went in.

{invoices}
  One row per document line. quantity: examinations charged on the line (negative on a credit note).
  unit_rate, net_amount, vat_amount: pounds. related_document: for a credit note, the invoice it credits;
  for a replacement invoice, the invoice it replaces.

{acks}
  One record per batch: payments received, returned unexamined and examined, the dates of acknowledgement and
  completion, and the batch status.

{calendar}
  One sheet per financial year: each BACS payment date by payment type, with the date the file is submitted.
"""


def index(path, F):
    lines = ["WEALDMOOR COUNTY COUNCIL, EXCHEQUER SERVICES",
             "2027/28 examination call-off: working papers index",
             "Compiled by %s, 3 March 2027" % PP["analyst"], "",
             "file | owner | source | as at | coverage"]
    for key, owner, src, asat, cov in INDEX_ROWS:
        lines.append("%s | %s | %s | %s | %s" % (F[key], owner, src, asat, cov))
    lines.append("")
    lines.append("All files are copies of the records named; none has been edited for this pack.")
    text = "\n".join(lines) + "\n" + FIELD_NOTES.format(**{k: F[k] for k in ("spine", "tsp", "runlog", "invoices",
                                                                              "acks", "calendar")})
    WR.write_text(path, text)
