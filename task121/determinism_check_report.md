# determinism-check report, task121, 2026-10-25

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: decomposition_attribution (with statistical_rigor / selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, brief at /tmp/determinism-check-task121-1792947066/judge_brief.md, verdict at /tmp/determinism-check-task121-1792947066/verdict.md. The main recommendation, the walk and Annex A are forced and reproduce. Supplementary answer 5 (Annex B) is not forced.

## Why
The measures summary defines the 2026 cohort as "its pupils at the end of key stage 4: those in year 11 on its roll at the January 2026 census", and the average as the total of its pupils' Attainment 8 over "the number of pupils in its cohort". 38 year 11 pupils (3 to 6 per academy) were on the January roll and left on 2026-02-23 or 2026-04-13 (movements log), so they have no 2026 results. The golden silently drops them from the denominator (1,476 of 1,514). The literal text keeps them (no result scores 0, not entered), and that changes every Annex B cell. Neither reading is closed by a shipped sentence. Label: competing_defensible_answer (underspecified cohort denominator). The design note's own fork SF16 names the January-roll cohort but never closes the leaver case.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pupils with a Progress 8 score | 9,573 | 9,573 (9,842 rows less 269 without KS2) | yes |
| Halwick / trust mean P8, gap | -0.52 / -0.14 / -0.378 | -0.523 / -0.145 / -0.378 | yes |
| Attendance item | -0.063 (-0.1) | -0.063 | yes |
| Disadvantage item | -0.068 (-0.1) | -0.068 | yes |
| Own effect | -0.023 (0.0) | -0.023 (equal-weighted -0.025) | yes |
| Remainder | -0.224 (-0.2) | -0.224 | yes |
| Seven primaries: share, P8 at Halwick, elsewhere, Halwick others | 89%, -0.57, -0.50, -0.10 | 89.4%, -0.572, -0.502, -0.104 | yes |
| Annex A, 16 figures (Halwick 30.2 / 1.2 etc.) | per submission | all 16 | yes |
| Annex B, 16 figures, golden denominator | per submission | all 16 | yes, only under the golden's denominator |
| Annex B, 16 figures, literal denominator | n/a | Halwick 35.7 / 43.3, Brantholme Park 48.1 / 30.2, Coldwell 41.5 / 36.2, Fernlea 40.6 / 39.4, Mossgate 39.3 / 38.6, Ridley Hey 46.6 / 36.6, Saltmoor 39.4 / 34.5, Wrayfield 42.1 / 34.0 | differs from golden in every cell |

## Competing answers that survived
1. Annex B cohort denominator. Golden: pupils with 2026 results (Halwick 37.0 / 44.8). Literal: all pupils on the January roll (Halwick 35.7 / 43.3). Closing rule: none shipped; the measures summary is silent on January-roll leavers.
2. Main call method (judge rates this a legitimate analytical step, not an unforced fork, with residual risk). Secondary-only effects give own effect -0.245 and remainder 0.0, which reads "yes". Adding KS2-school effects gives own 0.0 and remainder -0.2. The text supports the second only through "the same pupils", "all the borough's pupils", the ks2_urn / predecessor-URN note and the four-item walk. The data separates them (feeder pupils -0.50 elsewhere against -0.57 at Halwick). Restricting the fit to trust pupils gives own -0.085 (-0.1); "all the borough's pupils" pins this out.
3. Annex A, sensitivity not a fork: the year_group offset (extract's year less one for on_roll = Y) is documented in no shipped file. Labelling by the extract's current academy shifts Halwick to 29.9, and not offsetting year_group to 29.6. A moderate Gate B/E risk.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 3 (csv x7, pdf x4, xlsx x3) | yes |
| Large file | 25,000 rows or more | attendance 43,134 rows | yes |
| Distractors named in metadata.json, none labelled in a file name | 2 or more | 2 (school workforce, school funding); neither name labels it | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | workforce and funding rank nothing on the call (design note); the judge also treated the KS4 tables and national estimates as unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 16 + 16 cells across eight academies; "one decimal place", Progress 8 points | yes |
| Prompt shape; rubric 25 or more criteria | yes | shape is a decomposition walk plus two annexes; the criteria count is generated downstream and was not checked here | not verified |
| Nothing reads LLM generated; goldens real work products | yes | judge saw no authoring or provenance leakage and coherent dates; golden realism not re-judged here | yes (judge) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The thread names feeder-primary confounding as the work, with the within-secondary model or Progress 8 itself as the easy route. The design note and card declare the same: the second classification (primary school) that the value-added baseline leaves out, no decoy, no planted defect. They match. The declared distractors (workforce, funding) are not named as the surface read, so they are not too load-bearing. Gate G: no shipped artifact ranks the candidates wrongly; the published table is the gap itself. No Gate G finding.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. This matches the design note's `## Three rules`. The thread reached the golden by recognising a comparison group (the same primaries' pupils at other secondaries), not by executing a filed method.

## Stump power (Gate F)
Plausible, not certain. The within-secondary route gives own effect -0.2 and "yes", which a strong analyst files, so the trap is real. The placebo evidence is in the data. Some strong solvers will add KS2-school effects because of "the same pupils" and the remainder item. This is a standard multilevel cross-classification, a textbook route a strong solver can take; the main thread should weigh it with the scored readers' result.

## Findings, ranked
1. (Blocking) Annex B denominator unclosed: 38 January-roll leavers with no results; every one of 16 cells differs between the two readings.
2. (Moderate) The main call's cross-classified method is not named in the text. The judge accepts it as analytical, with residual risk that a literal executor stops at secondary effects. Filing it would be rule application, so do not file the HOW.
3. (Moderate) Annex A depends on an undocumented year_group offset. It is inferable, but one line in the attendance note would cover it.
4. (Minor) The establishment register gives Okeley Vale CE Academy and Brantholme Park the same predecessor URN (105802); an orphan with no effect on the analysis.

## Next action for the author
Pin the Annex B cohort in `ks4_measures_summary_2026.pdf` with one sentence stating whether a pupil on the January roll who left before sitting any exam stays in the denominator. File the WHAT (population) only. Then either keep the golden's reading ("a pupil with no 2026 results is not in the cohort") or re-key Annex B to the literal table above. Add one line to the attendance note that year_group is as at the extract date if you want Annex A hardened. Rebuild twice for byte-identical output and re-run. This edits a shipped input, so earlier runs are invalidated. The main recommendation, walk and Annex A stay frozen.
