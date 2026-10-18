# determinism-check report (pass 2), task243, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the rebuilt bundle. The five offices below 80 per cent are the City of Santa Cruz, San Isidro, Libertad, San Luis and Del Carmen. With net movement from the 2020 residence-five-years-ago tabulation in the balance, the other seven sit at 89 to 90 per cent. The one real fork is the closed balance against the balance carrying movement. The closed balance gives Esperanza 72, Magsaysay 76 and Mabini 74 and files eight offices. The shipped files decide it: the tabulation and its cover note are in the folder, the request email lists the tabulation, the ToR allows "any other census output the review needs", and the three offices show large net out-migration of older residents. The pass-1 findings are closed: the accepted ranges now cover the judge's whole robustness grid (no reading crosses 80 in either direction), and B1 and C1 reproduce exactly for all 12 offices.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| D1 five flagged (SC, SI, Lib, SL, DC) | 63, 63, 56, 64, 52 | 63.3, 63.2, 55.6, 63.9, 51.7 | yes |
| D1 other seven | 89, 89, 89, 89, 90, 89, 90 | 89.3, 89.2, 89.1, 88.8, 89.8, 88.9, 89.8 | yes |
| D1 closed balance (easy route) | eight offices | Esperanza 72, Magsaysay 76, Mabini 74; eight in | yes |
| Robustness grid, movement kept | no reading crosses 80 | five: 0.50 to 0.66; seven: 0.82 to 0.97 | yes (nearest approach about 2 points) |
| B1, 12 offices | 88.0 ... 83.3 | identical, e.g. 88.0, 61.0, 73.6, 81.5 | yes |
| C1, 12 offices | 77.2 ... 75.9 | identical, e.g. 59.2, 39.8, 37.8, 77.2, 84.6 | yes |
| FHSIS ratio | n/a | 0.78 to 1.55, not a completeness denominator | n/a |

## Competing answers that survived
None on the call. The closed balance is a method rung, not a reading fork, and the shipped tabulation overturns it. Residual risk, as the judge states: the prompt does not name the migration adjustment, which is method discovery and not a semantic gap. An optional line in the prompt or ToR saying the denominator is estimated from the two censuses would file the WHAT, but it is not required.

## Spec gates
Checked against /tmp/determinism-check-task243-r2/target/ (14 files) and metadata.json.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, eml, md) | yes |
| Large file | 25,000 rows or more | death extract 56,866 rows | yes |
| Distractors | 2 or more, named in metadata.json, none labelled in a file name | fhsis_m2_mortality_reports_2015_2022.csv, lcro_capacity_survey_jul2023.xlsx; not labelled | yes |
| Distractor weighs, unused, ruled out | yes | FHSIS includes infants and gives 0.78 to 1.55, not a completeness denominator; capacity survey unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx) | yes |
| Asks | multi-dimensional, unit and rounding stated | 12-row grids, whole per cent and one decimal in the prompt | yes |
| Prompt shape and 25 or more criteria | identifiable | shape 07 grid; criteria count from the design note (12 + 12 + 24 + set + chart parts) | yes |
| Reads as real, not LLM-generated | yes | judge found no authoring leakage and no temporal incoherence | yes |

## Gate G reconciliation
The judge returned mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no. The design note declares decomposition_attribution with the migration term in the growth balance, and the closed-balance route giving eight offices. The two agree in substance. No shipped artifact ranks the offices, and the declared distractors are not the surface read carrying the task. Gate G: PASS.
Gate H: domain pass, layers pass, decisive_step analytical. This matches the card and the design note's `## Three rules`.
One slip in the judge's evidence: it names the tabulation `cph2020_special_tabulation_pdpfp_kalinawan.csv`. The shipped file is `cph2020_residence_5yrs_ago_kalinawan_special_tab.csv`. This does not change the verdict.

## Stump power (Gate F)
Strong and analytical. The closed growth balance is the textbook shortcut and files eight instead of five. A solver who cleans the data and reads the ToR literally still lands on the wrong eight. Recognising that the tabulation's movement belongs in the balance is the stump, and the data separate the two routes.

## Findings, ranked
1. None blocking.
2. Optional: one prompt or ToR line stating that the denominator is estimated from the two censuses (files the WHAT, not the HOW). It needs no rerun.

## Next action for the author
Proceed to ship (stage 5). Nothing further from the determinism check.

Author's check (main session, after the report): the shipped target.zip holds `cph2020_special_tabulation_pdpfp_kalinawan.csv` (unzip -l, and byte-identical to target/); the judge thread named the shipped file correctly, and the "slip" above came from the pass-1 scratch copy, made before the rename.
