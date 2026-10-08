# OS05 — How to place ten funded positions across the permit centre's four stages, when none of the director's four options keeps every stage under its limit

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · municipal permitting operations |
| Mirrors | Deploying a fixed headcount increment across pipeline stages when rework loops multiply one stage's real load and the proposals on the table were drawn from the wrong load (code review → CI → deploy pipelines at Meta and Google where failed checks re-enter review, trust-and-safety queues with appeals, Amazon fulfilment lines with re-picks) |
| Decision shape | An allocation under a cap: ten funded positions divided among intake, plan review, corrections and issuance |
| Committed call | The number of new positions in each stage, and the permits a year the plan lets the centre issue, to the nearest hundred |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · the admissible option off the slate (#9), evaluated on a workload built from the applicants' receipts, with a quiet second trap (#11) beneath it |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #9 picks from the offered options when none passes · #11 beats the headline trap, misses the quiet one · #10 notes a binding limit as a risk |
| Calibration form | Counterparty acknowledgement file: the applicant portal's receipts for every correction notice acknowledged and every resubmission lodged, for jobs filed over twelve closed months |
| Driving force | Plan review's workload is reviews, and the applicants' receipts show each filing coming back for 0.8 further reviews, so the stage needs 32 examiners, not 18, and the corrections desk takes 120 resubmissions a week, not the 100 it manages to clear. Under that load none of the director's four options keeps every stage at or under 95% within budget. The policy admits any whole division of the ten, and exactly one division passes: one intake clerk, six examiners, two corrections technicians and one issuance clerk. |

## 1. Situation

A city council has funded ten new positions for its permit centre, which takes 150 filings a week through intake, plan review, a
corrections desk for resubmissions, and issuance. The director has sent four options: (a) all ten in plan review, (b) five in plan
review and five on the corrections desk, (c) six in plan review, two on corrections and two in issuance, (d) three each in intake and
corrections and four in issuance. She favours (a), because plan review has the longest median wait. The operations policy requires
every stage to run at or under 95% of capacity and the new positions to cost no more than $1.0M a year, and funded positions are not
held vacant. The workload standard gives each stage's weekly capacity per person.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the median waits, the workload standard, the staffing roster, the weekly completions and the
  applicants' receipts. The director's reading of her own waits is right. The difficulty is the workload each stage really carries,
  and that the answer lies outside the options on the table.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's preference and her four options. A throughput model on filings still finds intake,
  corrections and issuance short and plan review comfortable, and still lands on a division that leaves plan review at 115%.
* **Instrument repair.** No file is suspect: the receipts hold every closed job's notices and resubmissions, and the waits, roster and
  completions are complete; completions are a correct count of a different thing, used as load at rung 1. Rung 0 returns option (a), rung 1
  option (d) and rung 2 option (c), and the search over divisions is still needed.
* **Lens swap.** The naive read counts filings. The answer counts reviews and resubmissions, a different population of work items, and
  searches a different set of plans.

## 3. The driving force

A strong solver beats the loud decoy at once: plan review's long wait is a queue, not a capacity measure. It builds a throughput model,
takes 150 filings a week through each stage, and finds intake, corrections and issuance short while plan review has 234 reviews of
capacity for 150 filings. Option (d) fixes exactly those three stages within budget, and the solver signs it. But every filing that
plan review returns comes back as a resubmission and is reviewed again. The applicants' receipts show 0.8 further reviews per filing,
so plan review carries 270 reviews a week, and the corrections desk receives 120 resubmissions while clearing only the 100 its four
staff can manage. Under that load (d) runs plan review at 115%, every option fails, and the policy does not limit the plan to the four
options. One division of the ten clears every stage.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Staff the stage with the longest median wait | Option (a), all ten in plan review | The director's reading, and the wait figures are correct | The workload standard and roster: intake (3 × 45), corrections (4 × 25) and issuance (2 × 60) each clear fewer than 150 a week |
| 1 | Throughput model on filings: each stage's load is 150 a week, corrections' load its weekly completions | Option (d), the only option that passes | A proper bottleneck analysis that clears the policy on the director's own slate | The receipts: 0.8 resubmissions per filing, so plan review carries 270 reviews and corrections 120 resubmissions a week |
| 2 | The same model on reviews and resubmissions, options only | Option (c), one condition from passing (intake at 111%); 7,020 permits a year | Every option fails; (c) is the closest and issues the most | The policy's terms: positions are assigned in whole positions to any stage, and none is held vacant |
| 3 | **Decisive:** search every whole division of the ten under the receipt-built load | **Intake +1, plan review +6, corrections +2, issuance +1; 7,800 permits a year** | — | — |

* **Shape.** The graded object is the division; each rung names a different one. Under the certified load the options issue 6,240,
  6,240, 7,020 and 6,760 permits a year, and only the committed division issues all 7,800 filed.
* **Partial correction priced (L3).** A solver who corrects plan review's load but keeps corrections at its completions (100 a week)
  finds three divisions passing and cannot single one out. One who searches the divisions on filings finds 119 passing, (d) among them,
  and keeps the director's option.
* **Grid.** Load (filings, receipt-built) × plan space (options, all divisions) gives 4 cells: (d), 119 divisions, (c), and the answer.
  The answer is the only cell with one admissible division. The nearest wrong division, (c), differs by one position and issues 10% fewer
  permits, and reaching it costs keeping the plan to the options.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the conditions and the whole-position rule. No document says the options are incomplete, and
   the workload standard counts reviews without saying a filing may need more than one.
2. **Corpus blind for a computable reason.** *In every week of the receipt file the centre ran its current roster, so the file scores
   the load each stage carries and never a division of new positions.* No division of the ten appears anywhere in the record.
3. **No arithmetic symptom.** Filings reconcile to intake completions, issued permits to the permit register, and every option's
   utilisation is computed without error under either load.
4. **Not a row predicate.** The load needs each job's chain of correction notices and resubmissions followed to approval in the receipts,
   counted per job, and averaged over closed jobs, then a search over 286 divisions against three conditions.
5. **The enumeration is arithmetic.** No column gives reviews per filing, and the corrections desk's arrivals exceed its completions only
   in the receipts.
6. **No cutover date.** The roster and the rework rate are stable across the twelve months, and no series steps.
7. **Survives deletion.** Removing the director's preference leaves a throughput model on filings certifying option (d).

## 6. The calibration corpus

* **Form.** The applicant portal's receipt file: every correction notice acknowledged and every resubmission lodged, for 7,800 jobs filed
  in the twelve months ending 150 days before the extract.
* **What it certifies.** 1.80 reviews and 0.80 resubmissions per filing; resubmission arrivals of 120 a week at the corrections desk
  against 100 completions.
* **What it is blind to.** Any division of the new positions (above).
* **Twin pair.** Residential additions and tenant fit-outs are identical on filings a week, valuation band, intake fields and a 45%
  first-review return rate. Additions never return twice and carry 0.45 resubmissions per filing; fit-outs return 55% of the time at every
  later review and carry 1.00, 2.2× more. Only chaining each job's receipts to approval separates them.
* **Resemblance points at the decoy.** The 2023 hiring round, which added four examiners and cut the median plan-review wait by a fifth,
  most resembles option (a).

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The operations policy: no stage may run above 95% of its capacity; the new positions' annual cost may not exceed $1.0M;
  positions are assigned to stages in whole positions; funded positions are not held vacant. The workload standard: weekly capacity per
  person is 45 filings at intake, 9 reviews in plan review, 25 resubmissions on the corrections desk and 60 permits at issuance. The
  filing forecast: 150 a week next year at this year's mix.
* **Empirical pins.** Reviews and resubmissions per filing, from the receipts.
* **Voices.** The director: "Plan review has the longest wait, so that's where the ten go." The permit centre manager: "Intake is the
  front door. If intake flows, everything flows."
* **Licensed wrong basis.** The policy records that the council's budget committee ranks staffing requests by median days saved per
  position and will review the plan on that basis.

## 8. Determinism by construction

* **Maturity.** Every job in the receipt window is closed; the longest took 140 days and the window ends 150 days before the extract, so
  no open chain is cut short.
* **Mix.** The forecast keeps this year's job-type mix, so reviews per filing carries forward at 1.80 without a convention.
* **Costs.** Intake $70k, plan review $115k, corrections $80k, issuance $68k a year; the answer costs $988k.
* **Threshold.** No division lands within half a percentage point of 95% at any stage under the receipt-built load, so rounding a
  utilisation cannot change which divisions pass.

## 9. Prompt sketch and deliverables

> Council has funded ten new permit-centre positions and the director has sent me four ways to deploy them; she would put all ten in plan
> review, where the wait is longest. Tell me how many go to intake, plan review, corrections and issuance, and how many permits a year
> that lets us issue, to the nearest hundred, as the line I sign. Send `position_split.xlsx`, a chart `stage_utilisation.png`, and a
> one-page `position_memo.pdf`.

* `position_split.xlsx` — each stage's load and utilisation for the four options and the committed division under both loads, the
  inspection sheet (ask A) and the refund sheet (ask B).
* `stage_utilisation.png` — a script-rendered small-multiple bar chart: one panel per plan (four options and the committed division),
  four bars per panel for the stages' utilisation, the 95% line drawn, failing bars marked, and plan review's filings-based utilisation
  shown as a ghost bar beside its true one.
* `position_memo.pdf` — the committed division, the permits figure, and why each option fails.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve inspection districts, last year's inspections per inspector-day and the
  share failed. *Device:* a re-inspection after a failure keeps the original inspection number with a suffix (-R1, -R2), as the
  inspection manual documents. Counting suffixed rows as new inspections inflates productivity in the districts with the most failures.
* **Ask B (device-carried).** For each of the six permit types, last year's fee refunds and the median days from cancellation to refund.
  *Device:* a refund posts as a negative fee line dated on the refund, carrying the original receipt number. Netting by receipt date
  instead of matching the refund to its receipt misplaces a third of refunds into the wrong quarter and halves the median.
* **Ask C (validity).** Pass or fail on each condition for the four options and the committed division under both loads, and reviews per
  filing for the three job types.
* **Decoupling.** Replacing the receipt-built load with filings changes no figure in asks A or B. Inspections and refunds are post-issue
  records that touch neither the receipts nor the roster.

## 11. Rubric arithmetic

12 districts × 2 (ask A) + 6 permit types × 2 (ask B) + 5 plans × 2 loads and 3 job-type rates (ask C) + the division (4), the permits
figure, its cost and plan review's utilisation + 5 named chart parts + 3 files ≈ 64 criteria.

## 12. World-building constraints

* Roster today: intake 3, plan review 26, corrections 4, issuance 2. Filings 150 a week; 1.80 reviews and 0.80 resubmissions per filing.
* Under filings: only option (d) passes; 119 of 286 divisions pass. Under the receipt-built load: no option passes; exactly one division
  passes (+1, +6, +2, +1) at 83%, 94%, 80% and 83% utilisation.
* True permits a year: (a) 6,240, (b) 6,240, (c) 7,020, (d) 6,760, committed 7,800.
* Additions and fit-outs match on every intake-visible column and on first-review returns.
* Inspection and refund records never touch receipts, roster or filings.
