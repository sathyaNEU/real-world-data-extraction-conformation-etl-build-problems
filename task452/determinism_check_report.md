# determinism-check report, task452, 2026-10-14

## Pass 1 (2026-10-14), architecture 2

One isolated judge thread (Sonnet, medium) on a fresh unzip at /tmp/determinism-check-task452-161350/target/, with the prompt, the submission's graded blocks and the judge system prompt verbatim. It did not see the design note, the generator or the metadata. This file replaces architecture 1's report (tributary phosphorus, retired; recoverable from git commit 28f07dd).

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE (one author-side finding below: the design note is stale against the shipped bundle; fix the note, not the bundle)
**Stumping type:** mechanism: method_or_model_selection (design-based against map-based area estimation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The agreement (arts. 1-6), monitoring plan (s3, s4.5), sampling design (s2 strata table) and the reference points pin every graded figure. 122,900 ha reproduces under the design-weight estimator and under a correctly weighted post-stratified estimator (122,934, same rounding). The estimator choice is therefore not a fork. Only the textbook error matrix with the final map's class areas diverges (171,582 ha, no reductions offered), an analytical error rather than a licensed reading. The adjudication log changes no class (a no-op, not a fork).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Deforestation points (rule-classed, = change=loss) | 224 | 224 (201 S1, 23 S2, 0 S3) | yes, reference_points_main_campaign_2026.csv |
| Stratum weights | 329 / 2,469 / 4,785 | 328.81 / 2,469.19 / 4,785.35 | yes, sampling design s2 |
| Area of deforestation | 122,900 (122,882.7) | 122,882.7 | yes |
| 90% interval | 100,000 to 140,000 | 102,756 to 143,009 (post-strat 103,554 to 142,314) | yes after rounding |
| Reference level emissions | 71,965,600 t | 72,400 x 2 x 497 | yes |
| Monitored emissions | 61,081,300 t | 122,900 x 497 | yes |
| Emission reductions | 10,884,300 t | same | yes |
| Offered / payment | 8,925,126 t / USD 44,625,630 | x0.82 exact; x5 | yes |
| 12 district areas | 7,600 ... 5,100 (sum 122,900) | identical, also under post-strat | yes |
| Patches (all / under 1 ha / 5 ha or more) | 30,548 / 12,206 / 3,221, 12 districts | identical, no patch at exactly 1.0 or 5.0 | yes |
| xlsx class counts | 224/2,491/1,285; 216/2,516/1,268 | identical | yes |
| Final-map deforestation | 73,225 ha, 59.6% | same; would offer about 29.2 Mt | yes |

## Competing answers that survived
None. Tested and rejected: final-map area (plan s4.1 requires a sample-based estimate), unweighted per-final-class points (171,582 ha), buffer skipped or ordered differently (art. 5 explicit). Loose wording, not decisive: the chart-title share (59.6%) has no stated decimals; xlsx column names and class labels are not pinned.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 5 (pdf, csv, xlsx, json, parquet) | yes |
| Large file | 25,000 rows or more | polygons 48,947 (also NFI 39,122) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | nfi_tree_measurements_2018-2022.csv, fire_hotspots_2024-2025.csv; names carry no label | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | tree and fire data relevant to forest loss, no deforestation estimate | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both present | yes |
| Asks | multi-dimensional, unit and rounding stated | stated once in the prompt for all asks | yes |
| Prompt | one paragraph, under 1,000 characters | 903 characters | yes |
| Rubric 25 or more criteria | 25 or more | not countable here; 12 districts x 3 patch counts, 12 areas, 5 headline figures and the per-point sheet give ample grain | assumed yes |
| Reads as real work product | yes | judge found no authoring disclosures; Spanish QC json and dd/mm/yyyy dates are realistic Layer 1 | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no, Gate G pass. The design note declares the same trap (error matrix on the final map's classes against the sampling strata), a stump_class analytical architecture, and two distractors (NFI, fire hotspots) that the thread did not name as the surface read. Mechanism and family match. The final map's statistics workbook (73,225 ha) is a true map-area figure and is not a declared wrong-basis distractor; the thread found it ranks nothing on the call.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Borderline note from the thread: the correct route is largely stated in the design pdf's strata table, so the H3 check passes but is not strongly protective.

## Stump power (Gate F)
Moderate to uncertain. A strong model that reads the design pdf first and weights by stratum area over points drawn reaches the answer directly, so there is real too-easy risk. The error-matrix route, final-map area and mixing 2025 with 2019 districts catch weaker runs. No determinism repair is required; hardening would mean stating the strata less plainly, at the cost of a rerun.

## Findings, ranked
1. Stale design note (author-side, does not change the verdict). DESIGN_NOTE.md still carries the earlier reference level (89,950 ha a year, 179,900 for two years) and the earlier figures (stump sentence: 3,382,582 t at USD 16,912,910 on the default path, 23,229,780 t and USD 116,148,900 for the golden). The bundle, submission, goldens and judge recomputation use 72,400 ha a year, 144,800 for two years, 8,925,126 t and USD 44,625,630. On the shipped bundle the error-matrix route (171,600 ha) exceeds the reference level and offers nothing, so the note's analyst-test, R3a/R3b assertions and fork text name wrong-answer amounts that no longer match. Re-sync the note (stump sentence, Three rules, analyst test, fork table) to the shipped figures, and confirm checks.py and figures_check assert the shipped default-path result.
2. Chart-title share has no stated decimals (59.6%); low risk, graded leniently.
3. xlsx column names and class labels are not pinned by the prompt; low risk.
4. Stump power is moderate because the design pdf states the strata plainly (Gate F, optional).

## Next action for the author
Re-sync DESIGN_NOTE.md to the shipped figures (finding 1), then proceed with the leak reader's result; no bundle change and no re-judge is needed.
