# determinism-check report, task255 (loop 1, pass 2), 2026-10-14

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: fine_numbers_method, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) saw only the fresh unzip of the rebuilt target.zip at /tmp/determinism-check-task255-loop1-pass2/target/ and the inlined blocks; verdict at /tmp/determinism-check-task255-loop1-pass2/verdict.md. Literal execution of the policy (4.2, 4.3, 5.1), the memorandum (2.3, 3.1, 3.2) and the actuary's exhibits gives $4.0M at 0.74 expected occurrences, with $3.0M at 1.25, a wide margin on both sides of the one-a-year line. The pass 1 finding is closed: the extract notes now file the vehicle identity (VIN, or serial without a VIN; the 4 March 2024 consortium load under FMC- numbers; earlier numbers left on the schedule and still revalued; later consortium adds, changes and deletes under FMC- numbers). With that text the thread reproduced 5,649 vehicles and the class split, and notes that the naive last-transaction count (6,212) contradicts the filed note.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Record, open, at retention | 820, 20, 108 (67 at $250k, 41 at $500k) | same | yes |
| Log mean, log SD | 10.18, 1.71 | 10.177, 1.710 | yes |
| Expected counts $1.0M to $5.0M | 7.46 4.03 2.53 1.73 1.25 0.74 0.48 | 7.458 4.033 2.528 1.729 1.253 0.738 0.481 | yes |
| Premiums, same order | 1,770,565 1,414,020 1,180,073 1,017,817 881,870 735,429 641,333 | same to the dollar | yes |
| Exhibit 6 anchor | 228.7 | 0.11683 x 1,957.566 = 228.7 | yes |
| Total operating expenditure | $5,668,433,420, 60 members | same | yes |
| Class expenditure (thousands) | 4,992,928 / 121,458 / 126,705 / 141,394 / 218,248 / 50,231 / 17,470 | same | yes |
| Vehicles, total and by class | 5,649; 4,207 / 301 / 241 / 189 / 541 / 143 / 27 | same | yes |

## Competing answers that survived
None on the main call. Closed files only $3.0M, no truncation or censoring $2.0M, censoring only $2.5M, no trend $2.5M, open suits uncensored $3.0M: each contradicts a stated policy or memorandum text. Untrended thresholds give the same call. Supplementary only, one residual fork: the schedule "at September 30" on an entered-date basis gives 5,623 against 5,649 (18 entries keyed after 30 Sep and backdated); effective_date is defined in the notes as the coverage date and SF16 files the effective-date reading, so it is closed, and the effect is about $825 on each premium. The "All members" expenditure row (5,668,433) is rounded from the exact total and not asked for.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (pdf, xlsx, csv, md) | yes |
| Large file | 25,000 rows or more | vehicle log 43,855 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | member_deductible_history.csv, liability_triangles_2026-09-30.csv | yes |
| Distractor quality | unused, weighable, ruled out by a shipped fact | neither answers a graded quantity; the thread found no file ranking the attachments | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 attachments x (count, premium), 7 classes x (expenditure, vehicles); stated in the prompt | yes |
| Prompt shape, rubric | shape identifiable, 25 or more criteria | shape 04; design note counts 39 | yes |
| Reads as real | no LLM tells | system-output mess, no disclosure found | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family fine_numbers_method, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, strategy maturity_censoring, Gate G method_or_model_selection, Layer 2 estimation_fit (truncated and censored likelihood over the whole window), declared distractors the deductible history and the triangles. Substantive match: both describe a truncated and censored severity fit, with no defect and no surface read, and the thread did not name either distractor as carrying the task. The mechanism and family labels differ in vocabulary (pass 1 of this loop returned method_or_model_selection and analytical_non_defect for the same build); this is a labelling difference, not a mismatch in what carries the task. The note's ladder ($2.0M, $2.5M, $3.0M, then $4.0M) matches the thread's competing fits. Gate G: pass.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the note's Three rules.

## Stump power (Gate F)
Strong. Every easy route ends on $2.0M, $2.5M or $3.0M, and the open-suit layer needs a censored and truncated likelihood over every file of the window at 2027 cost. The asks add independent hurdles (member totals counted once, FMC- chain, identifier cleaning).

## Findings, ranked
1. None blocking. The pass 1 SEND_BACK (unfiled vehicle identity) is closed by the extract notes and SF16.
2. Optional: say once that the schedule is read as effective at 30 Sep 2026 (the entered-date basis gives 5,623); the notes' definition of effective_date already closes it.
3. Optional: the design note's SF16 alternatives list 6,387 and 8,233 but not the entered-date basis; the earlier note records that fork as closed.

## Next action for the author
Proceed to ship: stage 5 with this APPROVE and the leak reader's result.
