# determinism-check report, task448, 2026-10-12

## Verdict
NOT_DETERMINISTIC (scoped to supplementary answer 3, county counts for 2024 and 2025; the main recommendation and asks 1, 2, 4, 5 are forced and reproduce)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: yes (borderline)

## Why
Ask 3's golden (Saline 1,360; McPherson 580; Dickinson 360; Marion 270; other four 440) spreads each HMDA reporter's total over the counties of its Venridge recordings. The dictionary defines HMDA county_code as the property's county, and guideline 2.2 says a home is in the county where it stands. The Venridge county is only the recording county. No shipped text says the HMDA county is mislocated. The dictionary-literal reading (HMDA county for the seven reporters, rows over group capture for the rest) gives 1,410 / 590 / 350 / 250 / 410, total 3,010. Every cell differs from the golden by 10 to 40, so rounding does not absorb it. The data favour the golden: a subset (Venridge) exceeds its superset (HMDA) in Marion, Rice, Ottawa and Lincoln for same-day reporters, and HMDA shares follow postal city. That is an inference the solver must make, not a filing. Competing_defensible_answer (Gate C).

Note: the design note's SF4 row states the golden reading as "HMDA county code for the reporters' totals", but submission step 7 and ask 3 use the recorder-county spread. The golden and the fork table disagree, and the "asserted" claim in SF4 does not cover county cells.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Venridge stacked rows | n/a | 3,770 | yes |
| Capture, same-day / after-deed | 1,673 of 1,731 (97%) / 236 of 395 (60%) | 96.6% / 59.7% | yes |
| Weyrauch, Mennwell rows | 154, 121 | 154, 121 | yes |
| Weyrauch, Mennwell estimates | 260, 200 | 257.7, 202.5 | yes |
| Reporters Corvane, Halverd, Arkhaven, Shunga, Tessaline, Saltfork, Ninnescah | 311, 228, 182, 151, 141, 138, 133 | same | yes |
| Ranking, five and sixth | 310/260/230/200/180, 150 | same | yes |
| Program year by county, total | 710/310/190/150/240, 1,610 | 710.9/311.1/191.8/151.9/241.9, 1,607.6 | yes |
| County 2024-25 (golden spread) | 1,360/580/360/270/440 | 1,359.1/577.5/361.9/269.5/441.8 | yes, under golden's spread only |
| County 2024-25 (HMDA county_code for reporters) | not claimed | 1,410/590/350/250/410 | competing answer |

## Competing answers that survived
- Ask 3, county of a reporter's loans: HMDA county_code (dictionary-literal) gives 1,410/590/350/250/410. The golden uses the recorder-county spread, 1,360/580/360/270/440. No shipped rule closes it.
- Closed by the data, not surviving: raw rows (Mennwell sixth), pooled 90% capture (Shunga fifth), lender-based capture for the program year (1,740, refuted by the April 2026 recording switch), counting trust quitclaims (Heidebrecht 200, still outside the five and excluded by 7.3 and 7.4).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, txt, pdf, xlsx) | yes |
| Large file | 25,000 or more rows | 62,167 (HMDA LAR) | yes |
| Distractors named in metadata.json, none in a file name | 2 or more | 2 (hmda_2023_county_summary_ks.csv, homebuyer_education_completions_2024_2026.csv); neither label is in a file name | yes |
| Distractor unused yet weighable, ruled out by a shipped fact | yes | judge found both unused by the solution; neither judged to answer a graded quantity | yes (weighing not independently tested) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt states "Round every count to the nearest 10"; asks are multi-cell | yes |
| Prompt shape and 25 or more rubric criteria | yes | shape 01 identified; rubric count not verified here | open |
| Not LLM-reading, goldens realistic | yes | judge found no authoring language; manifest labels the synthetic HMDA file as the FFIEC Data Browser, which overstates its provenance | note |

## Gate G reconciliation
The judge's mechanism (method_or_model_selection, coverage calibration stratified by recording timing) matches the design note's Gate G label and the dual-system-estimate stump. The surface read carrying the task is the row count or the pooled 90% capture, not either declared distractor, so there is no too-load-bearing-distractor finding. sole_data_defect is borderline: the Venridge undercount is a coverage gap, but the difficulty is choosing and validating the estimator on honest rows. The design note already records that the Gate G label repeats seven older builds. Mismatch finding: SF4 and golden ask 3 disagree on the county source (see Why).
Gate H line: domain: pass, layers: pass, decisive_step: analytical.

## Stump power (Gate F)
Plausibly stumping. Raw counts or a pooled 90% capture both miss Mennwell and misorder Weyrauch. The stratifier is not a column, and nothing shipped hints at capture. Weakness: a careful model that cross-checks Venridge against HMDA and tests a split by recording timing will find it.

## Findings, ranked
1. Ask 3 county cells are not forced: HMDA county_code versus the recorder-county spread, no shipped pin. Fix now.
2. The design note's SF4 reading ("HMDA county code") contradicts the golden's actual method. Reconcile.
3. The program-year total 1,610 is the rounded exact total, while the rounded cells sum to 1,600. State "total rounded separately".
4. export_manifest.csv overstates the synthetic HMDA file's provenance.
5. MTG_INSTR_DATE as the closing date is not named in guideline 7.5. Low risk.

## Next action for the author
Pin the county source in field_dictionary.xlsx with one line. For example: HMDA county_code follows the postal city of the reported address, so for reporters the home's county is taken from the recorder, per guideline 2.2. Then correct SF4 to match, keep the golden, and note the 1,610 total as rounded separately. Run /fix-determinism for this; the main call, the stump and every main-call figure stay frozen.
