# AD02 — How many payments next year's digit filter will route to audit, when the year's largest flagged cell is a cohort that has almost finished being paid

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · local government internal audit |
| Mirrors | Sizing next year's review queue from this year's alert volume when part of the alert stream is a fixed-term cohort running off (fraud-alert queues at payment platforms, trust-and-safety review queues at Meta, invoice-exception desks in large accounts-payable operations at Amazon-scale retailers) |
| Decision shape | One figure committed at a date: the payments the digit filter will route for examination in the 2027/28 plan year, filed in the audit plan on 25 March 2027 |
| Committed call | Routed payments in April 2027 to March 2028, to the nearest hundred |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (past exceedance against forward yield), with Pattern B in the control set for the shallow rungs (finer controls separate the screen constructions) |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #12 stops at the first control that passes · #21 adds exclusions the rules do not ask for |
| Calibration form | Published control set with a reproduction clause: the three published digit-conformity statements, 63 figures any screen must reproduce |
| Driving force | The screen is right about 2025/26, and Housing Support's flagged cell is the year's largest. That cell is a fixed-term instalment cohort: each household is paid exactly 30 monthly instalments, a term written nowhere and recoverable only from the 2021 intake, which has already run off. The cohort's stream has been flat for the last 13 months of the extract, and by the plan year more than half of it has stopped. |

## 1. Situation

A county council's internal audit team runs a continuous-audit filter on payments: in the plan year it routes for examination every
payment of £1,000 or more that falls in a first-two-digit cell its department exceeded on the latest closed-year Benford screen. The
2027/28 plan goes to the audit committee on 25 March 2027 and must commit the number of payments the filter will route, which sets the
team's examination days. The screen for 2025/26 is on file, labelled as a description of that year's payments. Payments since April 2021,
the payee records and the three published conformity statements ship with it.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published statements, the screen, the payment files and the payee records. The screen is
  labelled as describing 2025/26 and makes no claim about the plan year. Nothing reported is overturned and no stakeholder read is
  corrected; the difficulty is that the plan year's flagged-cell payments are not the closed year's for one department.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the external auditor's view and the screen file. The statements still certify the closed-year construction,
  every department's recent series is still flat, and carrying the closed year forward still looks like the careful forecast.
* **Instrument repair.** Suspect file: the published payment files, whose rows are invoice lines wherever a remittance has several. Repaired
  to one row per payment, rung 0 sheds the 4,200 line rows and returns 34,700 (+238%), and rung 1 lands on rung 2's 12,800 (+24.5%); the
  £500 floor removes no row the filter or any rung uses. The payee records are complete for what they hold, a household and an amount, and
  writing the 30-instalment term or each household's last instalment date onto every record leaves all three rungs where they are, because
  each carries the closed year forward. Instalments not yet paid are a forward population no payment row records, so the per-household count
  into 2027/28 is still needed for 10,280.
* **Lens swap.** The naive figure counts payments made in 2025/26. The answer counts payments in 2027/28, which for Housing Support is a
  different population: the households of one cohort with instalments still to come.

## 3. The driving force

A strong solver rebuilds the screen until it reproduces every published statement, applies the filter's rule, checks that each
department's monthly flagged-cell series is flat, and carries the closed year into the plan year. Each step is competent. Housing Support's
flagged cell (first digits 14) holds a household support scheme's instalments of £1,420 to £1,490. Households were approved monthly from
October 2024 to September 2025 and each is paid exactly 30 instalments, but nothing in the pack states the term. It shows only in the 2021
intake, whose 512 households each received 30 instalments and stopped between September 2023 and August 2024. To see the plan year, a
solver must group the cell's payments by payee, count each household's instalments paid, recover the term from the completed intake, and
count what falls between April 2027 and March 2028. Adult Social Care's flagged cell, identical on every statement figure, is a standing
care-fee stream and carries forward whole.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Benford screen on every published payment (£500 and up), filter rule applied, closed-year flagged-cell count carried forward | 38,900, +278% | The publication is the population the filter sees, and the rule is applied as written | The reproduction clause: the full published range reproduces none of the 60 departmental statement figures, because the £500 floor cuts the first decade |
| 1 | Complete decades (£1,000 to £999,999.99) at the publication's row grain, carried forward | 17,000, +65% | It reproduces the council-wide statement figure exactly in all three years, the control everyone checks first | The finer controls: line grain reproduces only 34 of the 60 departmental figures, because a multi-line remittance is published one row per invoice line under one transaction reference |
| 2 | Hygiene: payments collapsed to transaction reference, credit notes excluded; every statement figure reproduced; closed-year count carried forward | 12,800, +24.5% | All 63 published figures reproduce exactly, every flagged series has been flat for 13 months, and the closed year is the natural forecast | The 2021 intake's payment history: each of its 512 households was paid exactly 30 instalments, and the 2024–25 intake's households reach their 30th before or during the plan year |
| 3 | **Decisive:** ongoing streams carried at their flat level; Housing Support's cell rebuilt per household, with instalments paid counted, the 30-instalment term from the completed intake, and only instalments falling in 2027/28 counted | **10,280** | — | — |

* **Figure shape.** Every correction walks the figure down, and the decisive move continues down: the answer is the minimum of every cell that
  applies the filter's rule to every flagged department. Per-rung offsets are +278%, +65.4% and +24.5%.
* **Partial correction priced (L3).** A solver who suspects the scheme and fits an exponential decay to Housing Support's monthly series
  finds no decay, because the series has been flat since September 2025, and lands back on 12,800. A solver who sees the scheme and drops
  Housing Support's cell as legitimate payments lands at 7,550, 26.6% low, because the filter's rule routes every payment in a flagged
  cell. Taking the current run-rate (5,850 for Housing Support) instead of the closed year lands at 13,400, +30.4%.
* **Grid.** Range (full or complete decades) × grain (line or payment) × forward (carry or cohort) × coverage (every flagged department or
  Housing Support dropped) gives 16 cells. The nearest wrong cell is line grain with Housing Support dropped, at 11,750 (+14.3%), and it
  needs two filed rules broken at once: the reproduction clause and the filter's coverage. Every single-error cell sits at least 24.5%
  away; every full-range cell sits more than 200% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The scheme's award letters are not in the pack, the payee records carry a household ID and an amount, and no
   document gives a term or an end date. The audit methodology defines flagged cells and the reproduction clause, nothing about a plan
   year.
2. **Corpus blind for a computable reason.** *In each of the three statements the carry-forward reading and the cohort reading return
   identical figures, because a statement reports only payments already made.* The statements certify the screen and are arithmetically
   incapable of pricing a plan year.
3. **No arithmetic symptom.** Payments tie to the published files, every statement figure reproduces, flagged-cell counts reconcile to the
   payee records, and the Housing Support series shows no break, trend or gap in the extract.
4. **Not a row predicate.** It needs a group-by on payee, a count of instalments per household, a constant recovered from another cohort's
   completed histories, and a projection per household into the plan year.
5. **The enumeration is arithmetic.** Which households still pay in 2027/28, and how many times, is computed; no column carries an
   instalment number or a remaining count.
6. **No cutover date.** Approvals ran monthly for a year, so the cohort's end is spread over twelve months; no closed series steps, and the
   2021 intake's run-off was equally gradual.
7. **Survives deletion.** With every voice and the screen file removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The published conformity statements for 2023/24, 2024/25 and 2025/26: each year's council-wide first-two-digit MAD and, for each
  of the ten tested departments, the payments in range and the MAD. The audit methodology makes exact reproduction of every published
  figure the condition of using a screen.
* **What it certifies (rungs 0–2).** Payment grain, complete decades and positive amounts reproduce all 63 figures exactly. Line grain
  reproduces the 3 council-wide figures and 34 of the 60 departmental ones; counting credit notes as absolute values breaks Facilities' MAD
  in all three years; the full published range reproduces 0 of 60.
* **What it is blind to.** The plan year (above). The statements are equally satisfied by any forward model.
* **Twin pair.** Housing Support and Adult Social Care are identical on the 2025/26 statement: payments in range, MAD, flagged cell 14, and
  5,250 payments in it. Their plan-year routed counts are 2,730 and 5,250 (1.92×), separated only by the cohort construction.
* **Free training instance.** The 2021 intake's run-off sits inside the 2023/24 and 2024/25 statements, visible and harmless: it is
  history, and no plan year rests on it.
* **Resemblance points at the decoy.** On every statement column Housing Support's 2025/26 profile is closest to Adult Social Care's, a
  stream that carries forward whole.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The audit methodology's reproduction clause: a screen used to set flagged cells reproduces every figure in the published
  conformity statements. The filter's rule: in the plan year it routes every payment of £1,000 or more in a first-two-digit cell its
  department exceeded, on the latest closed-year screen at the plan's approval, by more than half the expected count and by at least 30
  payments. The plan commits routed payments for April to March.
* **Empirical pins.** The 30-instalment term, from the 2021 intake's 512 completed households.
* **Voices.** The head of internal audit: "Digit screens find behaviour, and behaviour doesn't change in a year." Housing Support's finance
  manager: "Our scheme payments are approved and audited every year; there's nothing in them for your filter."
* **Licensed wrong basis.** The methodology records that the external auditor sizes continuous-audit workloads on the latest closed year's
  routed count and will review the plan on that basis.

## 8. Determinism by construction

* **Ongoing streams.** Every other flagged stream is flat across 30 months with no seasonality, so trailing-year, run-rate and
  seasonal-naive forecasts agree to the payment.
* **Term.** All 512 households of the 2021 intake received exactly 30 monthly instalments with no gap or early exit, and the 480 households
  of the 2024–25 intake show no gap or exit in the extract. Instalments are paid on the 15th, so no payment sits on a year boundary.
* **Counting from payments.** The payee file carries no approval date, so remaining instalments are counted from payments made and no
  approval-date convention exists.
* **Flagged cells.** No cell sits within 10% of either limb of the filter's rule, so rounding of expected counts never changes the flagged
  set.
* **Rounding.** 10,280 rounds to 10,300; the nearest cell rounds to 11,800.

## 9. Prompt sketch and deliverables

> The 2027/28 audit plan goes to committee on 25 March and has to state how many payments our digit filter will route to the team over the
> plan year, to the nearest hundred. Our external auditor would rather we planned for too many than too few. Give me the number as a
> sentence for the plan, with `filter_workload.xlsx` holding the sheets below, a chart `routed_payments.svg`, and a one-page `plan_note.pdf`.

* `filter_workload.xlsx` — the routed-payment build by department, the grants sheet (ask A), the supplier set-up sheet (ask B) and the
  reproduction table (ask C).
* `routed_payments.svg` — monthly flagged-cell payments from April 2021 to March 2028 as stacked areas by department, the plan year under the
  carry-forward and the cohort readings as two lines, Housing Support's run-off shaded, and the 2021 intake's completed run-off annotated.
* `plan_note.pdf` — the committed figure, Housing Support's share of it, and the readings a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the ten departments, the voluntary-sector grant awards live at 31 March 2026 and their
  total annual value. *Device:* the grants register records an amendment as a variation row restating the full award, as its guidance
  notes say. Summing award rows double-counts every amended award and overstates three departments. The filter never reads the grants
  register.
* **Ask B (device-carried).** For each department, new suppliers set up in 2025/26 and the share set up without a verified bank-detail
  check. *Device:* the supplier master's change log records a bank-detail change as a new record linked to its predecessor, per the master
  data guide. Counting records as new suppliers overstates set-ups in two departments and flatters their verified share.
* **Ask C (validity).** For each statement year, the published figures each of the three screen constructions reproduces (3 × 3), and the
  plan-year routed count under each of the four rung bases.
* **Decoupling.** Clearing the cohort construction and the screen changes no figure in asks A or B.

## 11. Rubric arithmetic

10 departments × 2 (ask A) + 10 departments × 2 (ask B) + 9 reproduction counts and 4 bases (ask C) + the committed figure, Housing
Support's plan-year count and the gap to the carry-forward figure + 5 named chart parts + 3 files ≈ 64 criteria.

## 12. World-building constraints

* Rung figures are 38,900 / 17,000 / 12,800 / 10,280, and the full range at payment grain returns 34,700. Every single-error cell sits
  at least 24.5% from the answer, and the only cell inside 20% (11,750) needs two filed rules broken.
* Housing Support: 480 households approved 40 a month from October 2024 to September 2025, 30 instalments each; 5,160 instalments in
  2025/26, 5,760 in 2026/27 and 2,640 in 2027/28, plus 90 ordinary payments a year in the cell. The 2021 intake: 512 households, 30 each,
  run off between September 2023 and August 2024.
* Adult Social Care's 2025/26 statement figures equal Housing Support's exactly; its cell holds a flat 5,250 a year. Highways (cells 49
  and 99, 1,400 a year) and Facilities (cell 12, 900 a year) are flat.
* Multi-line remittances sit in Children's Services and Waste and add 4,200 routed rows at line grain; Facilities holds the credit notes.
* Grant variations and supplier bank-detail changes never touch the payment files or the screen.
