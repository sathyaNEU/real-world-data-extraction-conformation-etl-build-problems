# determinism-check report, task253, 2026-10-12 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (method_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The place count is the number of schools whose underlying Year 5 mean is below 480, unobserved, so under the filed LT-AS-04 s3.1 to 3.5 model it is the sum of the 264 schools' chances (41.95, mean, median and mode all 42). The rivals (56 raw means, 28 shrunk means below 480, 69 on 2026 only) are each refuted by the filed text or are plug-in thresholds far outside the model's own count spread (sd 4.45). All supplementary answers reproduced. Judge thread: isolated, brief at /tmp/determinism-check-task253-1791774195/judge_brief.md, verdict at verdict.md in the same folder.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Participating Year 5 results (2024 legacy + 2025 portal + 2026 csv) | 30,956 | 30,956 (10,232 / 10,400 / 10,324) | yes |
| REML mean / school SD / year-group SD / student SD | 496.5 / 16.5 / 9.3 / 69.9 | 496.48 / 16.47 / 9.28 / 69.86 | yes |
| Places (sum of P(underlying < 480)) | 42 (41.95) | 41.947 | yes |
| Region shares % N, S, Northern, W, Southern, Coastal | 15.5, 25.6, 12.2, 16.7, 14.1, 15.9 | 15.52, 25.58, 12.18, 16.68, 14.13, 15.91 (none within 0.02 of a rounding edge) | yes |
| 2027 Year 3 to 6 students, total | 7,072 | 7,072.2 | yes |
| Students by region | 1,578 / 3,530 / 356 / 768 / 431 / 409 | identical | yes |
| Hub students / fortnightly km: Brinrigg | 3,068 / 813 | identical | yes |
| Carnbrae | 2,243 / 1,957 | identical | yes |
| Kirkanby | 725 / 1,826 | identical | yes |
| Tullgate | 671 / 1,593 | identical | yes |
| Haskwick South | 365 / 2,138 | identical | yes |
| Hub totals | 7,072 / 8,327 | 7,072 / 8,326.8 | yes |
| Chart order (Haskwick South longest) | as golden | consistent | yes |

## Competing answers that survived
None closed by anything but a shipped text or date. Judge notes two minor forks, both resolved by files:
- Region shares over rounded regional places sum to 43, incoherent with the 42 total; shares over 41.95 are the reading.
- Hub source: facilities directory (Feb 2026, 45 schools differ, predates July 2026 Haskwick South) against the 6 Nov 2026 hub plan; the plan "takes effect" in 2027.
Soft spot (Gate C, minor): the prompt never says "expected" for places, students and km. Judge's optional suggestion (a clause naming the count as the expected number of partner schools) is declined by the main session: such a sentence would name the decisive step (design note readability screen; leak reader question 1). Disposition of the suggestion: declined, recorded here. The estimand stays forced by the prompt's "underlying average" definition and the guidelines' unobserved-membership logic (s2, s3, s5).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, docx, txt) | yes |
| Largest file | 25,000 rows or more | 110,515 (naplan_results_2026.csv), 107,995 (2024 extract) | yes |
| Distractors | 2 or more in metadata, none labelled in a file name | 2 named (literacy_specialist_rates_2027.xlsx, literacy_PL_register_2026.csv); no file name labels one | yes |
| Distractor relevance / ruled out | same world, unused, ruled out by shipped fact, none answers a graded quantity | rates and PL register are in the programme's world and feed no graded figure; judge also counted the Feb 2026 directory as a lure, ruled out by dates | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png) | yes |
| Goldens present | all named | both present in golden/ | yes |
| Multi-dimensional asks | yes | region cuts, per-hub students and km, chart | yes |
| Units and rounding stated | each ask | whole numbers and one-decimal per cent in the prompt | yes |
| Prompt shape and 25-criteria floor | shape identifiable, 25 or more | shape 14; design note counts about 32 | yes |
| Prompt | one paragraph, under 1,000 chars | 820 chars | yes |
| Realism | no LLM tells | judge saw none; notes file somewhat tidy but reads as a data team handover | yes |

## Gate G reconciliation
Judge: statistical_rigor / analytical_non_defect, no surface-read dependency, no sole data defect; decisive step analytical. Card: stump_class analytical, gate_g method_or_model_selection, analyst_test (28 by model-then-count, 56 by raw means, miss the 42), which matches the judge's two traps and 42 exactly. The card carries no mechanism/stumping_family keys, so no field-level conflict. Judge named no declared distractor as carrying the task. No mismatch.

## Stump power (Gate F)
Good. Strong models are expected to fit the model correctly and split between 28 and 42; every ask figure carries the chance weighting, so a point-count response misses the supplementary tables as well. Lower rungs: the early roll-forward of 64 F-6 primaries (7,130 against 7,072) and the hub plan against the directory. No too-easy signals named.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test.

## Findings, ranked
1. None blocking. Minor: the prompt does not say "expected" (suggestion declined, above).

## Next action for the author
Proceed to stage 5 ship; no repair and no re-judge needed.
