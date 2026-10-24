# determinism-check report, task482, 2026-10-24 (pass 2; pass 1 was DETERMINISTIC / APPROVE on the round 1 pack, /tmp/determinism-check-task482-030123/verdict.md)

## Verdict
NOT_DETERMINISTIC (margin_or_boundary_fragility, with competing_defensible_answer on the Fallowmere figure and an unreproduced Ask 2 rule)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (USD 0.3M, Fallowmere only) needs a Fallowmere count of about 177.6 to 180.5 beneficiaries; break-even is 187.68. Policy FIN-14 s2.3 to 2.4 files only "the days expected after that date ... read from the experience since 1 October 2016 ... of the provider number ... in the beneficiary's group". It files no survival method, no limit on later elections, no tail rule. Literal readings give 0.2, 0.3 and 0.4. Gates C and E fail for the main recommendation and the summary figures. The other seven provider numbers are nil under every variant (at least 20 beneficiaries clear). The unreproduced Ask 2 inpatient day counts are a second, separate finding.
The thread's 0.248 (stays starting on or after 1 Oct 2016) and 0.277 (pre-Oct-2016 elections kept) sit either side of the 0.25 edge. The design note's own SF10 reads "experience since October 2016" as every election under the provider number; the filed words do not say which. This is a reading the note must close in the policy text, not in the note.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fallowmere payments before sequestration (remittance CLP, adj_carc_253 added back, reversals netted, PLB left out) | USD 6,636,768 | 6,636,768.30 | yes |
| Rows / beneficiaries | 3,572 / 3,540 | 3,572 / 3,540 | yes |
| Fallowmere beneficiaries and close states | 304; 62 on service, 44 live-discharged, 198 died | same | yes |
| Fallowmere days of care; inpatient share | 28,193; 1.4% | 28,193; 1.4% with 399 days | yes |
| Fallowmere repayment | USD 0.3M | 0.248 to 0.447 across variants (0.2, 0.3, 0.4) | no (method-dependent) |
| Other seven repayments | nil | nil under all variants | yes |
| Ask 2 Fallowmere GIP / respite days | 327 / 72 | 388 / 76 on paid, unreversed units (repricing rule not shipped) | no |
| Ask 2 other provider numbers | per submission | not reproduced | unverified |

## Competing answers that survived
- Pool start: stays starting on or after 1 Oct 2016 gives 180.53 (0.248, prints 0.2); pre-Oct-2016 elections kept gives 179.70 (0.277, prints 0.3). Shipped rule: "since 1 October 2016" (policy 2.4), which does not say which.
- Group pooled across diagnosis groups: 178.70, 0.311, 0.3 (policy 2.4 names the group, so this is a weak fork).
- Number of later elections counted: one (golden) against several; the 1.5 times and 2 times sensitivity runs give 0.360 and 0.447, printing 0.4. No shipped sentence limits it.
- Kaplan-Meier tail (restricted mean or extrapolated) and "last provider number" when the open stay is at an X-keyed hospice (35 beneficiaries): unfiled.
- Ask 2: "days Medicare paid for" against a repricing rule ("last days paid at the routine rate, the count that closes the gap to the cent") that appears only in the solution steps. Counting units on paid, unreversed claims gives 464 days and 1.6% against the golden's 327 plus 72 and 1.4%. The design note says the payment closes on that count (SF15, SF19, AD1), but the judge did not recover it from the bundle.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 6 (pdf, csv, xlsx, txt, json, docx) | yes |
| Large file | 25,000 rows or more | 66,364-row fixed-width extract; 28,635-line EMR export | yes |
| Distractors in metadata | 2 or more, none named in a file name | hospice_quality_measures_2026.xlsx, fy2027_operating_budget.xlsx (named in metadata.json; file names do not label them) | yes |
| Distractor unused yet weighable | yes; any answering a graded quantity reproduces arithmetically and is ruled out by a shipped fact | quality scores and a 2027 plan enter neither cap; judge found no artifact answering a graded quantity. The census report's average lengths of stay is a context artifact (see Gate G) | yes |
| Deliverables | 1 to 3, all in golden | 1 (fy2026_hospice_cap_accrual.xlsx), present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | summary and cap schedule, inpatient days and shares per provider number; units and rounding stated in the prompt | yes |
| Prompt shape identifiable; rubric 25 or more criteria | yes | shape 07; per-provider repayments, 8 x 3 inpatient cells and the schedule give well over 25 | yes (not formally generated) |
| Reads as real, not LLM generated | yes | judge found no provenance or LLM-generation problem | yes |
| Gate C and E (determinism) | literal reading gives one answer | forks above | NO |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_strategy maturity_censoring, gate_g method_or_model_selection, stump_class analytical, no official decoy, no validated decoy. Design note: nothing planted; the census report's average lengths of stay "rank nothing on the decision" (R1 reads it and lands at nil). These agree. The thread did not name the declared distractors (quality measures, 2027 budget) as the surface read. The census report is not a metadata distractor; the thread found no Gate G failure from it. No mismatch on Gate G.

Gate H: thread says domain pass, layers pass, decisive_step analytical. Design note and card (analyst_test, domain_test, layer2_family field_method) say the same: projecting live discharges' later hospice days. No mismatch. Reconciliation holds; the fault is determinism margin, not classification.

Design-note vs thread margins. The note claims a standing family of twelve constructions spanning USD 0.279 to 0.314M, each at least 0.029M from its edge, and that SF10 (since 1 March 2025 only) is the only reading giving 0.4. The thread found readings on both sides of the 0.25 edge (0.248) and at 0.360 and above. The note's "standing family" does not include the pool-start variants. The set of constructions the note tested is incomplete.

## Stump power (Gate F)
Real: treating live discharges as finished gives 0.0 (count 194.9 against 187.7), and a survival-based solver lands near the line. But the line is a window of about 3 beneficiaries set by unfiled estimation choices, so a correct method can still miss. Note for the main thread: Kaplan-Meier and Aalen-Johansen are the field's standard method. The thread reached the golden's neighbourhood by applying them with no data-settled judgment, so the blind readers' scored result may show this landable; weigh it with that result.

## Findings, ranked
1. Main call fragile at the 0.25 rounding edge under unfiled pool start (0.248 against 0.277). Fix by filing the pool's population in the policy (which elections enter) and widening the margin to at least 3 beneficiaries clear of 0.25 and 0.35 under every variant.
2. Number of later elections counted, tail rule and last-provider-number choice are unfiled. File the WHAT (one or all later elections, horizon), not the HOW (CLAUDE.md rule on determinism repairs).
3. Ask 2 inpatient day counts are not recoverable from shipped text. The paid-at-routine-rate rule exists only in the solution steps. Either state in the asking sentence or policy what "days Medicare paid for" means, or re-key to a countable quantity. Judge got 388/76 for Fallowmere against 327/72.
4. Minor: BP_DAYS excludes the discharge day for live discharges but counts the death day; 21 rows deviate by a day. Layer 1, not decisive.

## Next action for the author
Run `/fix-determinism task482` with the pool-start and number-of-later-elections findings: file the estimand's population in the policy, re-measure the margin across the pool-start, group and later-election variants (including 0.248 and 0.36), and state the Ask 2 "paid for" rule; rebuild and re-judge once.
