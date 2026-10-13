# determinism-check report, task450, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The deciding quantity is the 2026 form's passing raw score. Linking through the 25 shared items puts it at 25 under chained equipercentile, frequency estimation, Tucker, Levine and Rasch true-score linking. Tucker is the thinnest, at 26.72 against the 26.5 cut, and the pass or fail verdict is unchanged. At cut 25 the shipped rules give the golden's 15 campuses and every ask figure. The judge thread (isolated, fresh unzip, blocks only) recomputed every load-bearing value from the bundle. Its verdict was produced by a separate thread; I did not judge in my own thread.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Passing raw score | 25 | 25 under all five methods | yes |
| Rated FAY tested / met / share | 5,727 / 2,769 / 48.3 | same | yes |
| Tobar plus Delgadillo | 63 of 176, 35.8 | same | yes |
| Designated campuses | 15 | 15, same set and counts | yes |
| 2025 tests / 2026 tests | 6,564 / 6,341 | same | yes |
| Anchor means | 12.10 / 12.58 | same | yes |
| Default-path rejections | 30 (2025 conversion), 21 (distribution matching) | same | yes |
| Ask 4 by community | 1,431 / 56.8 ... 1,359 / 49.3 | same | yes |
| Ask 5 no 2026 result | 18, 25, 18, 19, 18, district 98 | same | yes |

## Competing answers that survived
None on the main call. Three forks were examined and none survives:
- **Linking method.** Not named in the files, but every method gives raw 25.
- **2025 campus identity for ask 4.** SCHOOL_CODE contradicts SCHOOL_NAME in 6,440 rows. The data decide it: counts by name correlate 0.99 with SIS campus size, by code 0.10. The code reading would give different community figures (North 1,427 / 40.2). This is detectable Layer 1 mess, not a fork.
- **Ask 3 population.** Minor and non-blocking. The prompt's "every rated campus's tested and meeting counts" most naturally reads as the rule-4 full-academic-year counts, but it does not say so. An optional clause in the prompt would remove the all-student alternative reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | CSV, XLSX, PDF | yes |
| Large file | 25,000 or more rows | 317,050 rows (2026 responses) | yes |
| Distractors | 2 or more, in metadata.json, none labelled in a file name | `grade5_enrollment_projection_2026-27.csv` and `math_professional_learning_hours_2025-26.csv`; neither is named as a distractor in any file name | yes |
| Distractors unused and weighable | unused by solution; one that answers a graded quantity is ruled out by a shipped fact | Unused by the solution per the judge and the design note. The judge did not report that either answers a graded quantity. | yes |
| Deliverables | 1 to 3, all in the golden | 2 (docx, xlsx), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | the prompt states one-decimal percentages and whole-number counts | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | metadata shape 14 (cuts of a distribution); the design note counts about 50 candidate criteria before the generated rubric selects | yes (not independently verified) |
| Realism | nothing reads as LLM generated | the judge's hygiene review found nothing; I did not independently review the goldens | yes |

## Gate G reconciliation
Judge: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The judge's Gate G reads as passing, with no wrong-ranking artifact.

Card and design note: `stump_class: analytical`. The analyst test names matching the raw-score distribution (21 campuses, raw 26). The default path (2025 conversion, 30 campuses) is the same stump the judge identified. Both agree on the mechanism and on the two wrong routes.

The judge did not name either declared distractor as the surface read, so neither is too load-bearing. No mismatch.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This matches the card's `domain_test` and the design note's `## Three rules`. The decisive step is common-item linking under non-equivalent cohorts.

## Stump power (Gate F)
Moderate to good. The easy routes give 30 campuses or 21; only anchor linking gives 15. Nothing in the files names the linking method. The asks add independent Layer 1 mess (old-system codes, id merges, closure mapping, unrated Vereda).

## Findings, ranked
1. Optional: add a clause to the prompt saying ask 3 counts are the full-academic-year counts, to close the minor ask 3 reading. It is not needed for determinism.
2. Non-blocking: 2025 campus identity for ask 4 relies on the solver noticing that SCHOOL_CODE contradicts SCHOOL_NAME. The data resolve it. If a SEND_BACK ever cites this, a one-line filing of the code's meaning in `data_dictionary.xlsx` is the fix.

## Next action for the author
None required. Proceed with the stage-4 card and pre-ship check.
