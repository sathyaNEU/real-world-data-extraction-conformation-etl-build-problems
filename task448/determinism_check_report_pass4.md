# determinism-check report, task448, 2026-10-13 (pass 4)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) saw only a fresh unzip of target.zip and the extracted blocks. The five lenders and the sixth are forced by the shipped files. HMDA does not cover Weyrauch, Mennwell, Heidebrecht, Kessinger or Eisenbrandt, so their counts come from the Venridge stack, scaled by the feed's capture within each recording mode, measured on the HMDA reporters (97% same-day, 60% after the deed). The pooled 90% capture or raw rows swap Mennwell for Shunga Valley. The county fork that the portal's second return found (HMDA county_code against the recorder's county) is closed by guidelines 2.2 ("the county in which the property is recorded") and the field dictionary; the HMDA-code reading gives 1,410 / 590 / 350 / 250 / 410, which the filed text excludes. Every graded figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| HMDA counts (7 reporters) | 311 / 228 / 182 / 151 / 141 / 138 / 133 | same | yes |
| Venridge rows after drops | Weyrauch 154, Mennwell 121, Heidebrecht 82, Kessinger 80, Eisenbrandt 47 | same | yes |
| Capture by mode | 1,673/1,731 (97%), 236/395 (60%) | same | yes |
| Non-reporter estimates | 260 / 200 / 140 / 80 / 80 | 257.8 / 202.5 / 137.2 / 82.8 / 78.7 | yes |
| Ask 3 | 1,360 / 580 / 360 / 270 / 440 | 1,359.1 / 577.5 / 361.9 / 269.5 / 441.8 | yes |
| Ask 4 | 710 / 310 / 190 / 150 / 240; total 1,610 | 710.9 / 311.1 / 191.8 / 151.9 / 241.9; 1,607.6 | yes |
| Ask 5 (twelve) | 310 ... 80 | matches | yes |

## Competing answers that survived
- Ask 3 and 4 county by HMDA county_code: closed by guidelines 2.2; not a surviving fork.
- Estimator variant for the county split (Venridge rows over group capture): rounds to the same values.
- Closing date versus recording date: same top five, order and sixth.
- Advisory (not a verdict change): ask 4 weights each mortgage by the capture of how it was recorded. After-deed lenders record with the deed from 6 April 2026 (lag 0 in 75 of 75 rows), a switch visible only in the data. Assigning the lender's 2024-25 mode instead would give 760 / 320 / 210 / 180 / 260, total 1,740. The judge treats this as analysis (a solver who sees the switch has no basis for applying 59.7% to a mortgage recorded with its deed). Optional closure: one sentence in venridge_pmm_layout_guide_v4.pdf that matching follows the recording sequence of the mortgage and conveyance (would need a rerun, not required).
- Closest rounding margins: McPherson 577.5 (575), Mennwell 202.5 (205), Heidebrecht 137.2 (135); stable across variants.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / rows | 10+ / 3+ / 25,000+ | 15 / 4 (csv, txt, pdf, xlsx) / 62,167 | yes |
| Distractors in metadata.json, none named in a file | 2+ | hmda_2023_county_summary_ks.csv, homebuyer_education_completions_2024_2026.csv; no file name labels one | yes |
| Distractors unused yet weighable, not answering a graded quantity | yes | unused, deletion moves nothing (design note); neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pptx, both in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | county by period, program year; "round every count to the nearest 10, each from its own unrounded figure" | yes |
| Prompt shape and 25+ criteria | 25+ | shape 01 (ranked list under a cap); design note plans about 26 criteria (not independently counted) | yes (by design note) |
| Not LLM generated, goldens realistic | yes | judge found no authoring disclosures; Venridge mess reads realistic; golden realism not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical, stump a stratified capture estimate by recording mode; analyst_test predicts the pooled capture leaves Mennwell at about 135 below Shunga Valley's 151, which the judge reproduced (134.8 pooled). Match. No declared distractor was named as the surface read carrying the task. The raw-count surface read is a Venridge rows path, which the design note itself calls the default path and the layout guide flags as incomplete; the judge flags this as borderline but not a Gate G breach.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the design note's `## Three rules` and the card's domain_test.

## Stump power (Gate F)
Good. Raw counting or pooled capture both file the wrong fifth; ten or more separately gradable figures in the asks. The design note's planned pair ceiling is 32.5.

## Findings, ranked
1. Advisory only: ask 4 mode switch of 6 April 2026 is documented nowhere in the files.
2. Note: the HMDA LEIs are fictitious 549300... strings; consistent with the fiction, not a finding.

## Next action for the author
None required; ship. Optionally add the one layout-guide sentence on the recording sequence if ask 4 is to be pinned, which forces a rebuild and no further re-judge licensed here.
