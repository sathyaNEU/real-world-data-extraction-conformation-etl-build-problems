# determinism-check report, task255 (loop 1), 2026-10-14

## Verdict
NOT_DETERMINISTIC (no SOLUTION_WRONG on the main call)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection (statistical_rigor, truncated and censored MLE), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) saw only the fresh unzip at /tmp/determinism-check-task255-loop1/target/ and the inlined blocks; its verdict is /tmp/determinism-check-task255-loop1/verdict.md. The main call is forced: literal execution of the policy gives 1.25 at $3.0M and 0.74 at $4.0M, so $4.0M, and the open-suit second layer is licensed by policy 4.1/4.2 ("all of the members' liability occurrences", "the pool's claims record"). The failure is in the asks. The vehicle count behind all seven premiums (ask 2) and the vehicles per class (ask 3) rests on a rule no shipped file states: count a vehicle once, under the latest unit number added for it, if that unit is active at 30 Sep 2026. The broker says only "the units on the members' vehicle schedules at September 30, 2026" and the extract notes say only "one row for each add, delete or change of a unit". Nothing mentions the FMC- renumbering. Literal readings reach 5,649, 6,212, 6,387 or 8,233, so the premiums move by roughly $18k to $82k at $4.0M. Label: underspecified_objective, in the asks. The main recommendation is unaffected.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Record / at retention | 820 / 108 (67 at $250k, 41 at $500k); 800 closed, 20 open | same | yes |
| Log mean, log SD | 10.18, 1.71 | 10.1769, 1.7102 | yes |
| Expected counts $1.0M to $5.0M | 7.46 4.03 2.53 1.73 1.25 0.74 0.48 | same to two decimals | yes |
| Closed-only fit above $3.0M | 0.70 | 0.70 ($3.0M call) | yes |
| Total operating expenditure, 60 members | $5,668,433,420 | same; class sums as golden | yes |
| Vehicles at 30 Sep 2026 | 5,649 | 5,649 only under the unfiled latest-unit rule; 6,212 / 6,387 / 8,233 under other literal readings | no (convention unfiled) |
| Premiums, all seven ($4.0M: 735,429) | as golden | $4.0M: 753,304 / 758,861 / 817,471 under the competing counts | no |

## Competing answers that survived
- Vehicle identity (asks 2 and 3). Golden: a vehicle counts only if its latest-added unit number, FMC- re-adds included, is active (5,649; $735,429 at $4.0M). Competing: last transaction across all of the VIN's unit numbers is not a DELETE (6,212; $753,304); any unit active (6,387; $758,861); raw active unit numbers with no VIN dedupe (8,233; $817,471). The fork sits in 2,584 VINs carried under a legacy and an FMC- unit; in 738 the FMC- unit is deleted while the legacy unit is still active, and in 563 of those the legacy unit keeps taking CHANGE rows. The golden drops all 738, the least natural reading from the log. Shipped rule closing it: none.
- Main call: none survived. Naive fit $2.0M, censoring only $2.5M, truncation only $2.0M, closed files only $3.0M, each ruled out by a stated memorandum mechanism or policy 4.1/4.2.
- Minor: a cost of $249,984.39 is not censored under "at or above the retention"; no effect to two decimals.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (pdf, xlsx, csv, md) | yes |
| Large file | 25,000 rows or more | vehicle log 43,855 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | member_deductible_history.csv, liability_triangles_2026-09-30.csv | yes |
| Distractor quality | unused, weighable, ruled out by a shipped fact | judge saw no file ranking the attachments; not independently recomputed by me | not verified |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 attachments x (count, premium), 7 classes x (expenditure, vehicles); stated in the prompt | yes on form; the vehicle and premium figures are not determinate |
| Prompt shape, rubric | shape identifiable, 25 or more criteria | shape 04; design note counts 39 | yes |
| Reads as real | no LLM tells | system-output mess, no disclosure found | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection (statistical_rigor), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, strategy maturity_censoring (retention censoring, deductible truncation, open files as censored), Gate G method_or_model_selection, declared distractors the deductible history and the triangles. Match. The thread did not name either distractor as carrying the task, and no shipped file ranks the attachments. The note's default-path ladder ($2.0M, $2.5M, $3.0M, golden $4.0M) matches the thread's competing fits. The design note has no fork row for vehicle identity (SF1 to SF15 cover the claims side; the vehicle convention appears only in its ask rows A and B as D1 and D7), and the shipped files do not file the latest-unit rule the note's golden uses. Gate G: pass. Gate H: pass.

Gate H line: domain: pass, layers: pass, decisive_step: analytical.

## Stump power (Gate F)
Strong on the main call: every easy route ends on $2.0M, $2.5M or $3.0M, and the open-suit layer needs a censored likelihood over every file of the window. The vehicle ask adds unfiled-convention noise, a defect rather than a stump.

## Findings, ranked
1. SEND_BACK, asks 2 and 3: the vehicle-identity convention is unfiled. All seven premiums and the seven class vehicle counts depend on it.
2. The golden rule is the least natural of four literal readings (it drops vehicles whose legacy unit is still being changed).
3. Minor: the rounded class expenditures sum to 5,668,434 thousand against a total of 5,668,433; the submission already notes the total is rounded from the exact figure.

## Next action for the author
File the WHAT in the extract notes or the prompt: a vehicle is one VIN (serial where the VIN is NONE, SEE SERIAL, UNKNOWN or blank), counted once, and on the schedule at 30 Sep 2026 if it has an ADD or CHANGE effective on or before that day and no later DELETE, stating how the FMC- re-adds relate to the legacy unit numbers. Then rederive premiums and class vehicle counts from that rule, add an SF row to the fork table and assert it in checks.py. Leave the main call, the expected counts and the stump frozen, and re-judge once.
