# determinism-check report, task255, 2026-10-13

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (deductible truncation and retention censoring in a severity fit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) saw only the fresh unzip at /tmp/determinism-check-task255-1791853130/target/ and the inlined blocks. The prompt, policy 4.2/4.3/5.1, the coverage memorandum (2.3, 3.1, 3.2) and the broker letter pin the estimand: trended lognormal MLE on the 820-occurrence 2014-2021 record, counts scaled from 228.7 above $25,000, retention = lowest quoted attachment with at most one expected occurrence. Literal execution gives 1.25 at $3.0M and 0.74 at $4.0M, so $4.0M. Every graded figure reproduced. Verdict file: /tmp/determinism-check-task255-1791853130/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Record / stopped at retention | 820 / 108 (67 at $250k, 41 at $500k) | same | yes |
| Log mean, log SD | 10.18, 1.71 | 10.1769, 1.7102 | yes |
| Expected counts $1.0M to $5.0M | 7.46 4.03 2.53 1.73 1.25 0.74 0.48 | 7.4575 4.0328 2.5281 1.7289 1.2528 0.7378 0.4805 | yes |
| Premiums, same order | 1,678,252 ... 536,691 | same | yes |
| Total operating expenditure | $5,351,537 thousand, 60 members | 5,351,537,064 | yes |
| Class expenditure (7 classes) | 4,694,899 / 113,908 / 125,382 / 149,725 / 202,850 / 48,527 / 16,247 | same | yes |
| Units at 2026-09-30 | 5,629 (4,199 / 301 / 242 / 202 / 515 / 139 / 31) | same | yes |

## Competing answers that survived
None on the main call. Tested and closed: no truncation ($2.5M), no censoring ($2.0M), neither ($2.0M), untrended deductible/retention (mixed fit still $4.0M), each contradicting a stated memorandum mechanism. One ask-only fork: vehicle identity by entered_date gives 5,602 units ($4.0M premium 662,116) against the golden 5,629; the file's effective_date definition and the letter's "on the schedules at September 30, 2026" close it. It does not move the retention. Cosmetic: class rows rounded individually sum to 5,351,538 against the stated 5,351,537 total.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (pdf, xlsx, csv, md) | yes |
| Large file | 25,000 rows or more | vehicle_schedule_log 39,109 rows | yes |
| Distractors named | 2 or more in metadata.json, none labelled by file name | member_deductible_history.csv, liability_triangles_2026-09-30.csv | yes (names label nothing) |
| Distractor quality | unused by solution, weighable, ruled out by shipped fact if it answers a quantity | not independently recomputed by me; judge saw no file rank or rate the candidates | not verified (see findings) |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 attachments x (count, premium), 7 classes x (expenditure, vehicles); units and rounding in the prompt | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 04 (setting one dial); design note counts 39 | yes |
| Reads as real | no LLM tells | 4 PDFs and extract notes read as in-fiction documents; golden is an xlsx and a chart; no generator disclosure found | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump class analytical, strategy maturity_censoring (limit censoring plus deductible truncation), Layer 2 estimation_fit, Gate G method_or_model_selection, declared distractors the deductible history and the triangles. Match. The thread did not name either declared distractor as the surface read carrying the task, and no shipped file ranks the attachments. The note's default path ends on $2.0M and the thread's competing answers ($2.0M / $2.5M) match its ladder rungs R0 to R2. Gate G: pass.

## Stump power (Gate F)
Good. The thread says an analyst fitting paid or ground-up costs by plain lognormal MLE lands on $2.0M or $2.5M, and only the truncated and censored likelihood at trended thresholds reaches $4.0M. Wrong fits move the call by one to three steps, not by a coin flip. Thread's caution: the memorandum and policy describe the mechanism fairly directly, so the risk of the task being too easy is in discovery, not computation.

## Findings, ranked
1. Gate H line: domain pass, layers pass, decisive_step analytical. This matches the card (`stump_class` analytical) and the note's `## Three rules`. The thread's H3 test agrees: a clean-data analyst reading every field still lands on $2.0M or $2.5M.
2. Residual risk (low): the design note's "Not semantics" claims no sentence names the truncation, but the thread found the memorandum 2.3/3.2 states the mechanism in prose. A reviewer could read the decisive step as following from a stated mechanism. The thread judged it still analytical because no rule files the likelihood.
3. Distractor quality was not independently verified by me, and the thread did not test whether the triangles or the deductible history reproduce a graded quantity.
4. Cosmetic: the class rows of the expenditure ask foot to 5,351,538 against the stated 5,351,537. Optional note that the total is computed from exact values.

## Next action for the author
None required; proceed to ship. Optionally, ask the leak reader to confirm that the memorandum's wording does not file the likelihood.
