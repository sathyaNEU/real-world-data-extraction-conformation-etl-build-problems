# determinism-check report (pass 2, re-judge after FIX_NOW), task240, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduces from the fresh unzip of the rebuilt target.zip. QS-7 2.1 and 3.2 tie the SE to the estimate as published with the final weights as the weighting note describes; the note states post-stratification to 96 region x age x sex cells, so z = w(y - p_cell) and the warned set is 9. It is robust to dropping n/(n-1) and to a re-post-stratified delete-one-PSU jackknife. The pass-1 step 7 wording defect is closed. No gate A to E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Adults / households / PSUs / strata | 7,238 / 3,764 / 707 / 24 | same; weights sum to SSB cell populations | yes |
| 48 CVs | Ask 1 | all match at 1 dp; warned min 27.6, unwarned max 18.4 | yes |
| Warned count | 9 | 9 | yes |
| Fixed-weight variant | 15 | 15 | yes |
| Response rates (12) | 59.6 ... 54.4 | all match, e = 0.91697 | yes |
| Calls (12) | 96 ... 425 | all match, 769 exact duplicates removed | yes |
| Step 7 (107 late households, 94 absent addresses) | revised wording | consistent with files (107 earlier statuses, 94 letters only) | yes |

## Competing answers that survived
None. Extract-only outcomes, raw region_code, dropping the 94 absent addresses and last-issue-only calls each shift answers (up to about 2 points) and are each excluded by shipped text (QS-7 4.2, 4.3, data dictionary "final outcome 110", QS-7 2.2).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / csv, xlsx, docx, pdf, md | yes |
| Large file | 25,000+ rows | call records 35,849 | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | interviewers.csv, ssb_population_estimates (plain names) | yes |
| Distractors unused, weighable, none answers a graded quantity | yes | no precision figure in either | yes |
| Deliverables | 1 to 3, in golden | 2, both in golden/ | yes |
| Asks multi-dimensional, unit and rounding | yes | yes | yes |
| Prompt shape, rubric 25+ | yes | shape 07 grid; rubric not in folder, 48+24+note items far exceed 25 | yes (not counted) |
| Not LLM-sounding | yes | no authoring disclosure found | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read no, sole_data_defect no. Design note: method_or_model_selection, estimation_fit. Match. The thread names the closeout memo, interviewer hours and CARD records as weighable unused material, and the population estimates as weight-building input rather than as a distractor; neither declared distractor carries the task. Gate G: pass.

## Gate H
domain: pass; layers: pass; decisive_step: analytical (variance of a post-stratified estimator against default fixed-weight linearisation). Matches the design note.

## Stump power (Gate F)
Moderate to good. Fixed-weight default wrongly warns 6 more; the asks stack independent traps (region repair, 107 late interviews, 94 absent addresses, duplicate calls) that hold scores down.

## Findings, ranked
1. LOW, optional: add a data-dictionary line that region_code is the master-sample region and the households file carries the current one (no change to solver work).
2. LOW, residual: the duplicate-call rule is inferred from identical key fields, unambiguous in the data.
3. LOW, caveat: QS-7 3.2 "as published" could be read as rule application by a strict reviewer (carried from pass 1).
4. INFO: rubric criterion count not verifiable in the folder.

## Next action for the author
Proceed to ship; no re-judge.
