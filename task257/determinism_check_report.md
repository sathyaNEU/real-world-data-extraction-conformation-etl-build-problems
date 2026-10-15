# determinism-check report, task257, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (optional hygiene tidy of the benchmark workbook, no rerun)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (general-purpose, sonnet, medium) recomputed everything from the fresh unzip. All figures reproduced. Latent (tetrachoric and polychoric) eigenvalues are 9.76, 6.00, 2.21 and 0.78 against a parallel-analysis 95th percentile of 1.07 at the fourth, so the answer is three. Pearson correlations give five, by splitting off the lopsided tools (93.8 to 95.0 per cent yes) and growth (4.5 to 6.7 per cent yes) items. The respondent and all-30 counts follow from the filed standard, export notes, site time zones and paper sealed dates. The thread's residual note: the correlation type is not filed, so choosing polychoric over Pearson is expert method selection, separated by the data (endorsement rates), not a coin flip.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Respondents | 13,717 | 13,717 | yes |
| Store-district respondents / all 30 | 12,245 / 10,055 | 12,245 / 10,055; all 12 district rows match | yes |
| Latent eigenvalues | 9.76, 6.00, 2.21, 0.78 | 9.76, 6.00, 2.21, 0.78 (5th 0.76) | yes |
| Parallel 95th percentile | 1.07 (4th) | 1.067 (4th), 1.059 (5th) | yes |
| Pearson eigenvalues 4th, 5th | 1.49, 1.34 | same; five retained | yes |
| Velicer MAP (polychoric) | 3 | 3 | yes |
| Item placement 11/11/8 | PAF, promax, 3 factors | identical lists; primary loadings 0.48 to 0.91, cross-loadings at most 0.06 | yes |

## Competing answers that survived
- Five (Pearson) is the intended default-path wrong answer. It rests on difficulty-factor splitting, and the latent loadings of tools and growth items are 0.86 to 0.91 on their own factors. It does not survive as a defensible alternative.
- Six (questionnaire areas by wording) has no support in the data. Four is rejected by every test.
- Ask-2 forks, all closed or low risk and confined to the xlsx table:
  - Kiosk "sessions taken together" (union gives 10,055; best single token gives 9,761) is not filed verbatim but follows from the employee-level respondent definition.
  - The paper sealed-date rule lives in the paper_returns workbook, not the standard. Keyed time would give 13,147 / 11,675 / 9,634.
  - Local 23:59 close against the vendor's 06:00 UTC cutoff differs by 10 employees. The filed rule governs.
  - A does-not-apply answer counting as an answer is closed by the export notes (items_answered verified). The scored-only reading, 7,949 all-30, is contradicted by the files.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 4 (csv, xlsx, pdf, jsonl) | yes |
| Large file | 25,000+ rows | 417,224 (responses.csv) | yes |
| Distractors in metadata.json, none named in a file name | 2+ | 2 (pulse_survey_2026_q2_site_results.csv, kestrava_retail_benchmark_2026.xlsx); names neutral | yes |
| Distractors relevant, unused, ruled out by a shipped fact | yes | Judge found neither carries the call; I did not separately test whether either reproduces a graded quantity | yes, not independently confirmed |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, png, md), all present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 30-item grid, 12 districts x 2 counts; counts of employees | yes |
| Prompt shape and 25+ criteria | yes | shape 07 grid; 30 placements + 24 district figures + call/components, well over 25 | yes |
| Not LLM-generated; goldens realistic | yes | Judge found no authoring disclosure. Nit: the benchmark workbook has 75th percentiles above 100 per cent (101.8, 103.5) and negative 25th percentiles, and item KL-2266 names the Brackenmere Leaders programme while benchmarked across 14 other clients. | yes, with nit |

## Gate G reconciliation
The thread says mechanism is method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The data are honest and the difficulty survives clean data. This matches the card (`stump_class: analytical`, driver = Pearson against latent correlations on lopsided items, `layer2_family: estimation_fit`) and the design note's stump sentence. The declared distractors are not named as the surface read. No mismatch. Gate G passes.

## Stump power (Gate F)
Good. A solver who cleans everything and runs Pearson EFA with parallel analysis files five with a plausible story. Only noticing the 5 per cent and 94 per cent endorsement rates leads to three. Ask 2 stacks heavy ETL, so it should separate strong responses. The only soft spot is a grader defending "Pearson five".

## Findings, ranked
1. (Low) The correlation estimator is not filed. This is by design (the HOW stays open), and the data separate the candidates.
2. (Low) Ask 2 residual forks: kiosk union wording and the paper sealed-date rule are unfiled in the standard. They are confined to the xlsx table.
3. (Hygiene) The benchmark workbook has impossible percentiles, and the library item KL-2266 is named for the Brackenmere programme.

## Next action for the author
Optional: clamp or replace the benchmark percentile columns and neutralise the Brackenmere-named library item in the generator, then rebuild. Otherwise proceed to ship.
