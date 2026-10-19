# determinism-check report, task270, 2026-10-19 (pass 2, run task270-r3)

## Verdict
NOT_DETERMINISTIC (main recommendation forced and reproduced; supplementary answer 3, the windscreen figures, is not forced)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call reproduces: band C is North West, West Midlands and Yorkshire and the Humber, with South East first below. The call is stable across thresholds from 1,500 to 3,000 and across alternative estimators. The windscreen ask (supplementary 3) holds only under a rule no shipped file states. The basis note (3.2) says only "a replacement and the camera recalibration it needs are one claim". The golden merges an own-repairer claim notified within 15 days after a replacement on the same policy into that replacement, and that rule appears only in SOLUTION_STEPS. A replacement among own-repairer claims is recognisable only by amount (about 300 pounds or more). Read literally, all eight rates differ from the golden (NE 10.97 vs 10.7, NW 13.29 vs 13.0, WM 13.02 vs 12.7, EoE 9.73 vs 9.5, SE 11.92 vs 11.7, SW 10.43 vs 10.2, YH 11.50 vs 11.3, EM 10.84 vs 10.7). Under the data-inferred rule, a pair in the amount overlap zone (264.38 then 209.22 pounds, claims C0459034 and C0459517, North East and Cumbria) flips the NE rate between 10.7 and 10.6. The fix pass did not close this fork. Full evidence is in /tmp/determinism-check-task270-r3/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Vehicle-years 2024 and 2025 | 182,255 | 182,255.02 | yes |
| Accident claims above nil | 19,592 | 19,592 | yes |
| SE / NW reported frequency | 12.5 / 11.8 | 12.50 / 11.76 | yes |
| Share of step 0 and Step Protection claims above 2,500 | 37.8% | 37.85% (1,140 of 3,012) | yes |
| Band C on the counterfactual | NW, WM, YH; SE next | NW 14.18, WM 14.16, YH 13.63, SE 12.29 | yes |
| Theft rate and cost, 8 regions | per golden | all eight to stated rounding | yes |
| Windscreen rate and cost, 8 regions | per golden | only with the unfiled 15-day merge and amount threshold | NO (literal reading: all 8 rates differ) |

## Competing answers that survived
- Windscreen (supplementary 3): own-repairer claims each counted as one claim gives different rates in all 8 regions. The shipped rule meant to close it (note 3.2) does not state the own-repairer recalibration merge.
- Windscreen (supplementary 3): replacement threshold 275 to 325 gives 10.7 for NE, and 225 to 250 gives 10.6. Nothing pins the threshold.
- Main call: none survives. The reported-frequency route (YH, WM, SE) is wrong by the note's own definition.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats | 10 or more files, 3 or more formats | 15 files; csv, pdf, xlsx, txt | yes |
| Large file | 25,000 rows or more | policy_terms_legacy 230,324 | yes |
| Distractors | 2 or more in metadata.json, none named by file name | industry_private_motor_statistics_2025.xlsx, customer_complaints_log_2025.csv; neither is labelled in its file name | yes |
| Distractors unused and weighable | unused by the solution, ruled out by a shipped fact | judge found them unused; no distractor answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | stated in the prompt; ask 3 not determinate (see above) | no on ask 3 |
| Rubric | 25 or more criteria | not checkable at this stage (generated downstream) | not checked |
| Prompt shape, realism | identifiable; reads as real | judge found nothing LLM-generated and system-extract hygiene clean | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note: stump is the incentive-truncated claim record, recovered through the claims above 2,500 and the step 0 / Step Protection size distribution. This matches. The declared distractors are not named as the surface read carrying the task; the surface read is the reported frequency. No mismatch.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. This matches the design note's Three rules.

## Stump power (Gate F)
The reported frequency files the wrong band C (YH, WM, SE). A solver has to model the truncation to get NW into band C. The judge cautions that note section 2.1 ("had every policy already carried step protection") signals a correction is needed. It also found that a cruder estimator, raw frequency on step 0 plus Step Protection policy years only, reaches the golden set, so the decisive step can be passed without the intended model. The main thread should weigh this with the scored readers' result. Ask 3 is over-hard for the wrong reason, an unfiled rule.

## Findings, ranked
1. Windscreen own-repairer recalibration merge (15 days, same policy, amount-recognised replacement) is unfiled, and one pair in the amount overlap flips the NE rate between 10.7 and 10.6. This is the fork the fix pass was meant to close.
2. The stump can be bypassed by a cruder size-free estimator (step 0 plus Step Protection policy years). Not a determinism failure, and a Gate F note.
3. Note 2.1's wording hints that a correction is needed.

## Next action for the author
Run /fix-determinism on ask 3 only. In the basis note section 3.2, file the WHAT: an own-repairer claim notified within 15 days after a replacement on the same policy is that replacement's recalibration and counts with it, and how a replacement is recognised (a type or description field, or a stated amount). Regenerate the own-repairer windscreen claims so no replacement and recalibration amounts overlap. Recheck all eight windscreen rates for rounding margins. The main call, accident claims and theft stay frozen.
