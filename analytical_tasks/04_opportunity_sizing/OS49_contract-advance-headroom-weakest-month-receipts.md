# OS49 — Where £30M of contract-advance headroom goes, when the funder lends against each customer's weakest month of cash

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · SME lending and receivables finance |
| Mirrors | Commitments sized on the weakest period of cash rather than the average (marketplace seller cash advances sized on the weakest month of settlements, cloud committed-use discounts sized on the lowest hour of usage, advertising platforms' annual spend commitments sized on the weakest quarter) |
| Decision shape | An allocation under a cap: £30M of warehouse headroom for contract advances, split across eight industry segments |
| Committed call | Headroom per segment, to the nearest £0.1M, and the annual net margin the split earns, to the nearest £10,000 |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E30 (a contract clears only for its weakest month: the funder lends 40% of twelve times the lowest calendar month of cash the customer paid, so one month without a receipt clears nothing), with E07 below it (net yield averaged over advances against net margin per pound of headroom, where tiny advances carry the minimum fee) |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #7 uses the ready-made measure · #13 validates on one population, applies to another · #3 stops at a close but inexact match |
| Calibration form | Settled-transaction ledger: last year's pilot, 600 contract-advance applications with the funder's approved amounts and every advance's monthly sweeps, fees, funding charges and losses, all settled |
| Driving force | The funder approves a contract advance at 40% of twelve times the weakest calendar month of cash the customer paid in the year before. No document states the rule, and all 600 pilot decisions reproduce it. IT and haulage contracts invoice large amounts every month. But seven in ten IT customers settle per-seat invoices quarterly, and haulage receipts swing with loads and payment runs, so their weakest months hold a quarter to a sixth of average invoicing. Cleaning customers pay like clockwork. The pilot's approval rates hide this, because pilot clients brought their steadiest contracts. The weakest month is a minimum over twelve monthly sums of receipts, joined to each contract's customer through the payer accounts. |

## 1. Situation

A lender that offers invoice finance inside a small-business accounting platform is launching contract advances: cash against a firm's
recurring monthly invoices to one customer, repaid from that customer's payments over a year. Its warehouse funder will give £30M of
headroom next year, and the lender must split it across eight industry segments (IT managed services, haulage, temporary staffing,
security, contract cleaning, equipment hire, waste collection, and catering) before it pre-approves offers on the platform. The funder
approves every advance itself. Last year's pilot sent it 600 applications, and every advance has settled. The head of sales is sure
haulage firms will take every pound the lender offers.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the platform's invoices and bank receipts, the payer links, the pilot ledger and the portfolio
  report. The pilot's approval rates are what the funder approved. Nothing reported is overturned. The difficulty is how much the funder
  will approve for the market's contracts, a rule no document states.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of sales and every voice. The request limit and the pilot approval rates still send the money to IT,
  haulage and staffing, and no document says how the funder sizes an advance.
* **Instrument repair.** Suspect file: the portfolio report, whose net yield is an average over advances, a narrower meaning than margin
  per pound of headroom. Repaired to margin per pound from the ledger, rung 0 returns the rung-1 plan (Haulage 17.0, IT 13.0, £2.14M),
  rung 1 is unchanged and rung 2 still gives IT 12.5 (£2.09M). The invoices, the receipts feed, the payer links and the ledger are complete
  for every contract and month. The funder's rule is recovered from complete records, so the weakest month is still needed for Cleaning's
  13.4.
* **Lens swap.** The answer counts different pounds, each market contract's weakest month of cash, and a different population, the
  market's contracts rather than the ones pilot clients chose.

## 3. The driving force

A strong solver sizes each segment's pipeline at the product sheet's request limit, 40% of twelve months' invoicing, and fills the £30M in
order of net margin. It notices that the portfolio report averages yields over advances, so Waste's tiny advances, which pay the £250
minimum fee, look rich, and it recomputes margin per pound from the ledger. It then sees that the funder approved well under the requests
and scales each segment by its pilot approval rate. Each step is right, and the money goes to IT, haulage and staffing. But the funder's
approvals follow a rule written nowhere: 40% of twelve times the weakest calendar month of cash the customer paid in the year before. A
month without a receipt clears nothing. IT firms invoice flat per-seat amounts every month, but seven in ten IT customers on the platform
settle quarterly, so two months in three bring no cash. Haulage and staffing receipts swing with loads, hours and customers' payment runs.
Contract cleaning is paid like clockwork. The pilot's rates hide all of this, because pilot clients brought their steadiest contracts. The
weakest month comes from the receipts feed, joined to each contract's customer through the payer accounts and summed by calendar month.

## 4. The ladder

| Rung | Construction (capacity per segment; fill £30M in order of margin, each segment up to its capacity) | Allocation (largest block) and annual net margin | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Capacity = the request limit, 40% of twelve months' invoicing to customers invoiced every month; order by the portfolio report's net yield | A, Waste 18.0 (IT 12.0, 1.50×); £2.50M, +39.6% | The lender's own limit and its own yield report | The warehouse allocates and charges headroom per pound approved, and the report averages over advances: most of Waste's pilot advances are under £2,000 and pay the £250 minimum fee |
| 1 | The same capacity, ordered by net margin per pound from the ledger (E07) | B, Haulage 17.0 (IT 13.0, 1.31×); £2.14M, +19.4% | The right grain for a pound of headroom | The ledger: the funder approved 63% of the pounds requested, and 40% in haulage |
| 2 | Capacity × each segment's pilot approval rate | C, IT 12.5 (Haulage 10.0, 1.25×; Staffing 7.5); £2.09M, +16.7% | Calibrated on the funder's own decisions | The ledger: every approval is 4.8 times the weakest calendar month of receipts in the year before (600 of 600), so a segment's rate belongs to the contracts its pilot clients chose |
| 3 | **Decisive:** capacity = 4.8 × each market contract's weakest calendar month of receipts, summed by segment, ordered by margin per pound | **E, Cleaning 13.4** (Security 5.4, Haulage 4.1, Staffing 3.9, IT 3.2; 2.47×); **£1.79M** | — | — |

* **The answer.** IT 3.2, Haulage 4.1, Staffing 3.9, Security 5.4 and Cleaning 13.4 (£M), earning £1,788,140 a year, committed as
  £1,790,000. Cleaning gets nothing on rungs 0 to 2.
* **Figure shape.** Every correction walks the margin down (−14.5%, −2.2%, −14.3%), and the answer is the minimum cell of the grid.
* **Discriminator dominance.** The four segments ahead of Cleaning in margin order carry £38.9M of capacity into rung 3, 1.30 times the
  cap. The weakest month keeps 43% of their capacity and 98% of Cleaning's, an edge of 2.29×, which leaves them £16.6M and Cleaning £13.4M,
  2.47 times the next block.
* **The deciding comparison.** The rung-2 plan's headroom as the funder would approve it is £11.2M, earning £0.76M, because the funder
  approves IT, haulage and staffing contracts at their weakest months. The note has to set that against £1.79M.
* **Partial correction priced (L3).** Every half-built floor hands the largest block to a wrong segment and gives Cleaning nothing. The
  weakest month of invoicing, not receipts, gives IT 11.2 against Haulage 7.5 (1.49×) and £2.04M (+13.9%). The weakest quarter of receipts
  divided by three gives IT 11.7 against Haulage 10.0 (1.17×) and £2.08M (+16.2%). Dropping contracts with a month without a receipt and
  keeping 40% of twelve months' receipts gives Haulage 19.0 against Staffing 7.2 (2.63×) and £2.05M (+14.4%).
* **Grid.** Margin grain (per advance, per pound) × capacity law (request limit, pilot approval rate, weakest month of receipts) = 6
  cells. Every non-answer cell puts the largest block on Waste, Haulage or IT. The nearest is the pilot approval rate at margin per pound
  (rung 2), £2.09M (+16.7%). The weakest month ordered by per-advance yield gives Waste 14.8 and £2.34M (+31.1%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The funder's term sheet says only that advances are approved case by case against evidence of recurring receipts.
   No document gives an amount, and the product sheet's 40% of invoicing reads like the answer.
2. **The corpus pins the law by reproduction (Pattern B).** 4.8 times the weakest calendar month of receipts reproduces all 600 pilot
   decisions. The weakest month of invoicing reproduces 468 and 40% of twelve months' receipts 84, and every miss overstates, so both
   rivals also miss the pilot's approved total. Scaling twelve months' receipts by any constant fits no more than 15% of decisions. The law
   is a construction behind a join (receipts linked to each contract's customer through the payer accounts, summed by calendar month, the
   minimum over twelve), not a setting a sweep reaches.
3. **No arithmetic symptom.** Receipts reconcile to invoices less credit notes and to the bank feed, and every capacity ties to its
   contracts under every law.
4. **Not a row predicate.** A contract's capacity is a minimum over twelve monthly sums. Dropping contracts with an empty month, the nearest
   row-level rule, still puts the largest block on Haulage.
5. **The enumeration is arithmetic.** No column holds a weakest month. It is computed for 38,000 market contracts from 4.6 million
   receipts.
6. **No cutover date.** The funder's rule held for every application across the pilot year, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot's settled-transaction ledger: 600 applications from 410 client firms, each with the requested amount and the
  funder's approved amount, and for every advance its monthly sweeps, fees, funding charges and losses, all settled. Each contract's
  invoices and receipts for the year before its application sit in the platform feed.
* **What it certifies.** Net margin per pound by segment (the rung-1 grain), the product sheet's request rule (every request is 40% of
  twelve months' invoicing) and the approval rates by segment (63% overall, 40% in haulage, 96% in IT). A solver who back-tests rungs 1 and
  2 is confirmed.
* **The absolute split (O2).** The 71 contracts with a calendar month without a receipt were all declined. Every other contract was
  approved at exactly 4.8 times its weakest month, and no decision falls in between.
* **Twin pair.** Two pilot security contracts, each invoicing £9,000 on the first of every month to a customer in the same size band on
  30-day terms, are identical on every invoice column and on twelve months' receipts (£108,000 each). The funder approved £43,200 for one and £21,600 for the other, 2.0× apart, because
  the second customer, a managing agent, holds back half an invoice for sign-off twice a year and pays it with the next.
* **Resemblance points at the decoy.** IT's market contracts match the pilot's IT contracts on every invoice column (flat per-seat amounts
  every month, customer size and terms), so transferring the pilot's 96% rate by resemblance lands on IT. The pilot's IT clients brought
  their monthly payers.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The warehouse gives £30M of headroom for contract advances next year and allocates and charges it per pound approved.
  The product sheet lets a client request up to 40% of the last twelve months' invoicing to a customer invoiced in each of those months.
  The funder approves every advance case by case against evidence of recurring receipts. The plan funds segments in order of the net
  margin they earn on the headroom they use.
* **Empirical pins.** Net margin per pound by segment, from the ledger's settled fees, funding charges and losses over approved pounds; the
  funder's rule, from the ledger's reproduction.
* **Voices.** The head of sales: "Haulage firms are desperate for cash; they'll take every pound we offer." The finance director: "The
  pilot's approval rates are the best evidence we have of what the funder will do."
* **Licensed wrong basis.** The warehouse funder's quarterly review sizes each segment's pipeline at 40% of twelve months' invoicing, and
  will see that basis.

## 8. Determinism by construction

* **Months.** Receipts are dated by the bank's value date, and the weakest month is taken over the twelve complete calendar months before
  the application (pilot) or before the plan date (market).
* **Payer links.** Every receipt's paying account resolves to exactly one customer, and no receipt is split across customers.
* **Approvals.** Every approval is exactly 4.8 times a weakest month in whole pounds, so the law reproduces at zero tolerance.
* **Fill order.** Margins per pound differ by at least 0.4 points between every pair of segments, so no tie decides the order, and the last
  funded segment takes the remainder.
* **Rounding.** Allocations round to £0.1M and sum to £30.0M. The margin rounds to £1,790,000 from the exact capacities (£1,788,140) and
  from the rounded allocations (£1,788,800) alike.
* **Maturity.** Every pilot advance has settled, so margins and losses are final.

## 9. Prompt sketch and deliverables

> Our warehouse funder is giving us £30M of headroom for contract advances next year, and our head of sales is sure haulage firms will
> take every pound we offer. Tell me how much of the £30M goes to each of the eight segments, to the nearest £0.1M, and the annual net
> margin it earns, to the nearest £10,000, in a form I can put to the credit committee. Send `headroom_plan.xlsx`, a chart
> `segment_floors.png`, and a one-page `credit_committee_note.pdf`.

* `headroom_plan.xlsx`: allocations and margins under the four rung bases, the reproduction sheet, the insolvency sheet (ask A) and the
  payroll sheet (ask B).
* `segment_floors.png`: for each segment, the request-limit, pilot-rate and weakest-month capacities as three horizontal bars, segments
  ordered by margin per pound, the point where £30M runs out marked, and the allocation printed beside each segment.
* `credit_committee_note.pdf`: the committed split, the margin, and the rung-2 plan's approvable headroom and margin beside it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each segment, last year's count of platform clients that entered a formal insolvency
  procedure, and that count as a share of the segment's clients. *Device:* the Gazette publishes a notice for each step of a procedure
  (administrators appointed, then a move to creditors' voluntary liquidation), and its notice-code guide counts a company once, at its
  first step. Counting notices overstates insolvencies by about a third in haulage and staffing, where administrations often convert.
* **Ask B (device-carried).** For each segment, the median headcount of client firms, from the payroll submissions the platform files.
  *Device:* a payroll submission goes to the tax authority for each pay run, so a firm paying weekly and monthly staff files two schedules
  a month, and the payroll guide counts distinct employees per month. Counting employee rows per submission overstates headcount by about
  40% in staffing and security, which run both pay frequencies.
* **Ask C (validity).** The allocation and margin under each of the four rung bases; the ledger reproduction under the weakest month of
  receipts (600 of 600), the weakest month of invoicing (468) and 40% of twelve months' receipts (84); and the rung-2 plan's approvable
  headroom (£11.2M) and margin (£0.76M).
* **Decoupling.** Clearing the weakest-month construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 segments × 2 (ask A) + 8 (ask B) + 4 bases × 2 + 3 reproduction counts + 2 rung-2 figures (ask C) + 8 allocations and the margin + 4
named chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Segments (request-limit capacity £M / net margin per pound / per-advance net yield / pilot approval rate / weakest-month capacity £M):
  IT 13.0 / 7.4% / 7.9% / 0.96 / 3.16; Haulage 25.0 / 6.9% / 7.2% / 0.40 / 4.08; Staffing 20.0 / 6.3% / 6.8% / 0.45 / 3.94; Security 12.0
  / 5.8% / 6.5% / 0.62 / 5.42; Cleaning 24.0 / 5.3% / 6.0% / 0.82 / 19.20; Equipment hire 15.0 / 4.9% / 5.3% / 0.75 / 10.50; Waste 18.0 /
  4.6% / 8.6% / 0.85 / 14.76; Catering 10.0 / 4.2% / 5.0% / 0.40 / 1.50.
* Partial capacities (£M): weakest month of invoicing IT 11.18, Haulage 7.5, Staffing 7.0, Security 7.2; weakest quarter ÷ 3 IT 11.7,
  Haulage 10.0, Staffing 9.6; empty-month drop at 40% of receipts IT 3.77, Haulage 19.0, Staffing 14.0. Seven in ten IT market customers
  settle quarterly.
* Rung largest blocks Waste 18.0, Haulage 17.0, IT 12.5 and Cleaning 13.4, with margins £2.50M, £2.14M, £2.09M and £1.79M; Cleaning
  unfunded on rungs 0 to 2 and in every partial.
* Pilot: 600 applications from 410 firms (IT 70, Haulage 85, Staffing 80, Security 75, Cleaning 90, Equipment hire 60, Waste 85,
  Catering 55), £9.6M requested and £6.08M approved; 71 declined for an empty month; reproduction 600, 468 and 84. The two security
  contracts are identical on every invoice column at £43,200 and £21,600.
* Gazette notices and payroll submissions never touch invoices, receipts, payer links or the ledger.
