# determinism-check report, task471 (v5r2, the one re-judge after the v5r1 FIX_NOW), 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (statistical_rigor), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged on target.zip sha256 prefix 5402dd6ec2786aea, from a fresh unzip at /tmp/determinism-check-task471-v5r2/target/ (19 files). The thread's verdict is /tmp/determinism-check-task471-v5r2/verdict.md. The brief was re-extracted from the corrected submission.md (step 3 file names fixed), and the thread was not shown any earlier report.

## Why
Every committed figure reproduced from the bundle: the 16 organiser counts, both supplementary counts for all 16 regions, and every critical component. The main call is forced by the data. The cell-wise dual-system estimate agrees with demographic analysis for children, women and men 50 and over, and is short only for men 18 to 49 (3.6, 4.0 and 4.8 per cent). Raising those men to demographic analysis's sex ratio is the only correction the files support. The 16 counts are the same under absolute male counts, a single 18-to-49 factor, and either age-mapping convention. The largest-remainders cut has margin (last award 0.598, first miss 0.381), and no share falls under 2.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Electors with residential address | 3,329,031 | 3,329,031 | yes |
| Adults, cell-wise DSE | 3,593,178 | 3,593,178.2 | yes |
| DSE men per woman 18-24 / 25-34 / 35-49 | 1.01 / 0.99 / 0.97 | 1.006 / 0.991 / 0.973 | yes |
| DA men per woman, same groups | 1.04 / 1.03 / 1.02 | 1.043 / 1.031 / 1.020 | yes |
| Men short against DA | about 4 per cent | 3.6 / 4.0 / 4.8 per cent | yes |
| Adults after correction | about 3.63 million | 3,633,254 | yes |
| 16 organiser counts | as filed | identical | yes |
| DSE as it stands | 8 regions change | identical 8 | yes |
| Census counts | 14 regions change | 14 | yes |
| New electors, 16 regions (total 166,644) | as filed | identical | yes |
| Removed because died, 16 regions (total 32,758) | as filed | identical | yes |

## Competing answers that survived
None on the main call or the counts. Forks tested, each closed by a shipped rule or fact:
- Imputed people added back or not subtracted: 9 regions change. Closed by pes_2025_methods_report.pdf sections 3.2 and 3.3 (MATCH N is "no census record" and imputed records are excluded from the checked file, so adding them back double counts).
- D or W counted as correct: 3 to 5 regions change. Closed by the methods report, where only C is "counted correctly".
- Region-level DSE instead of cells: equals the plain DSE.
- DA ratio applied region by region: not available, DA is national only.
- New-platform UTC read as country time: about 300 NEW and 402 DEL rows land on the wrong side of 30 June 2026. Closed by roll_extract_data_dictionary.xlsx.
- Old-platform (R25-) electorate numbers read as current: 32,311 new electors and 6,476 died removals land in the wrong region. Residual risk, below.

Residual risk (supplementary counts only, not the organisers): no document states that old-platform electorate numbers are the pre-2024-review numbers. The files settle it three ways. The NUMBER_BEFORE_2024_REVIEW column exists. All 70 reinstatements of old-platform removals return to the same region only under those numbers (100 per cent, against 44 per cent under current numbers). Old-platform enrolments per electorate correlate with roll size at 0.87 under them, against 0.31 as read. The judge counts this as a documented Layer-1 discovery, not a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, rows | 10+ files, 3+ formats, one file 25,000+ rows | 19 files, 4 formats (csv, xlsx, pdf, docx), roll_transactions_2025_2026.csv 319,994 rows | yes |
| Distractors | two or more in metadata.json, none labelled in a file name | metadata.json names subnational_population_estimates_jun2024.csv and census_2025_field_operations_summary.pdf, no file name labels one; the judge also found pes_2025_sampled_meshblocks.csv unused | yes |
| Distractor weighs but is ruled out | reproduces arithmetically, ruled out by a shipped fact | the wrong-basis distractor is ruled out by plan section 2.1 (adults usually resident on census day) | yes |
| Deliverables | 1 to 3, all in the golden | 2 (CSV and PNG), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 16 regions by 3 figures; prompt states whole numbers | yes |
| Prompt shape and rubric | shape identifiable, 25+ criteria | shape 05 (allocation to a fixed total); 16 x 3 figures plus components exceed 25. The rubric is not generated yet, so this passes by shape. | yes (by shape) |
| Reads as real | no LLM tells, goldens read as work products | judge: system-export look, no authoring disclosure; no contradicting finding | yes |

Hygiene notes from the judge, none decisive: one backward timestamp near the 28 September 2025 clock change (touches neither window edge), and pes_2025_methods_report.pdf (September 2025) cites a census workbook released 18 November 2025. I did not review the golden files for realism. This pass relied on the thread's hygiene read.

## Gate G reconciliation
Thread: method_or_model_selection / analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card has `stump_class: analytical`. Its `analyst_test` names the cell-wise DSE as the strong analyst's route and the 8 wrong regions (Ardenmere 26, Westerby 26, Larchfield 28, Glenwhite 31, Hawksridge 4, Corran Valley 6, Drumlea 4, Nethermoor 3). The thread's list is identical. The card's stumping_family and mechanism fields are None, so only the stump class and the analyst test could be compared, and they match. The declared wrong-basis distractor (subnational_population_estimates_jun2024.csv) is not the surface read carrying the task: the thread names the cell-wise DSE as the easy route, so the distractor is not too load-bearing.

**Gate H:** domain pass, layers pass, decisive_step analytical.
- The card's `domain_test` (census net coverage error by dual-system estimation, corrected for correlation bias with demographic-analysis sex ratios) matches the thread's domain pass.
- Layer 1: platform migration with two time bases, renumbered electorates, REF_TXN person chains, imputed-record convention.
- Layer 2: correlation-bias correction against demographic analysis.

## Stump power (Gate F)
Good. A strong solver who stops at a correct DSE files 8 wrong regions. One who uses census counts files 14 wrong. Reaching the golden needs building demographic analysis from births, deaths and movements, which nothing in the prompt or plan points at. The thread did not class the decisive step analytical merely because the golden is the field's standard method. It reasoned that the correction is not a stated rule: the data's own structure (the men-only shortfall) forces it. The supplementary counts add an independent layer: UTC and daylight saving, platform numbering, REF_TXN joins and reversals. The design note's ceiling.py figures (pair ceiling 33.5) are the author's own measure, not re-run here. The main thread should weigh them with the blind readers' result.

## Findings, ranked
1. No blocking finding.
2. Optional, FIX_NOW-grade, no rerun: one sentence in roll_platform_migration_notes.pdf saying old-platform transactions carry the electorate numbers in force before the 2024 review would close the one unstated convention behind the supplementary counts. It would also reduce a documented Layer-1 discovery that the design note counts toward the ask difficulty, so it is the author's call.
3. Minor: the backward timestamp and the methods-report date wrinkle above.

## Next action for the author
Ship. If you take finding 2, rebuild and re-check the byte-identical rebuild and ceiling.py before the zip changes.
