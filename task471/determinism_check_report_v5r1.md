# determinism-check report, task471 (v5r1), 2026-10-20

## Verdict
NOT_DETERMINISTIC (narrow, supplementary ask 1 only; the main recommendation and the PNG are forced and reproduce). No SOLUTION_WRONG: every golden figure reproduces.
**Disposition:** FIX_NOW. File the time basis of PROCESSED in roll_extract_data_dictionary.xlsx and/or roll_platform_migration_notes.pdf; data, prompt and goldens stay byte-identical, so no rerun for the pin.
**Stumping type:** mechanism: method_or_model_selection / etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The NEW_ELECTORS (167,285) and REMOVED_DIED (33,225) columns need the new platform's PROCESSED stamps (non-R25- TXN_IDs, from 3 Aug 2025 12:32) converted from UTC to the country's time at +12 h, +13 h in daylight saving. I checked the shipped text myself: roll_platform_migration_notes.pdf and the dictionary never say UTC or give an offset or a daylight-saving period; the only filed sentence is the specification's "Dates and times are the country's time". Read literally the stamps are already the country's time and the answer is 167,605 / 33,626 (+320 and +401 across regions; 1,109 accepted rows sit in UTC 12:00 to 23:59 on 30 June). The convention is inferable (first new-platform stamp is Sunday 3 Aug against "Monday 4 August"; PRV transfers at 06:xx old, 18:xx or 17:xx new; shift on 27 Sep and 4 Apr) but is not filed. Taxonomy: external_dependency (Gates B, C, E on ask 1). The 16 organiser counts are unaffected.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Residential electors | 3,329,031 | 3,329,031 (roll + electorates_and_regions; overseas 106,280 out) | yes |
| Adults by DSE in cells | 3,593,178 | 3,593,178 | yes |
| Men per woman DSE 18-24/25-34/35-49 | 1.01/0.99/0.97 | 1.006/0.991/0.973 | yes |
| Men per woman DA | 1.04/1.03/1.02 | 1.043/1.031/1.021 | yes |
| DSE men short of DA | about 4% | 3.6/4.0/4.5%; women -0.1/-0.2/+0.2% | yes |
| Adults after correction | about 3.63m | 3,633,824 | yes |
| 16 organisers | 27 20 25 26 29 5 11 12 7 5 4 8 6 3 8 4 | identical (also under DA unrounded or 2 dp; floor of two not binding) | yes |
| DSE as is / census counts | 8 / 14 regions differ | 8 / 14 | yes |
| NEW_ELECTORS total | 167,285 | 167,285 per region, only with UTC to local conversion | yes, conditional |
| REMOVED_DIED total | 33,225 | 33,225 per region (33,359 before 134 REI reversals) | yes, conditional |
| PNG | bars of organisers | matches counts | yes |

## Competing answers that survived
1. Time basis (verdict-driving): stamps as stored, 167,605 / 33,626 against golden 167,285 / 33,225, per-region columns differ. Closing rule meant: specification 2 "country's time", which does not say the stored new-platform stamps are not already that. Survives. A flat +12 h gives the golden, so DST instants do not matter.
2. Age range of the sex-ratio correction (not the verdict basis): the thread's run read 50-64 as DSE 0.988 against DA 0.997, and extending the correction there gave Glenwhite 28 and Rowanlea 4. Reconciliation: this reproduced only because the thread built demographic analysis without deaths_by_year_of_birth_1925_1990.xlsx (50-64 DA 0.9967, men -1.76%, women -0.92%). With the workbook read, the 50-64 ratios agree within 0.1 per cent and every age-range reading files the golden. So it is the thread's own data handling, not a fork in the package, and it does not change the verdict. Design-note row SF14 ("the 50 to 64 and 65 and over ratios agree") stands.

Rejected as errors rather than forks: imputed records in the numerator, W or D read as correct. Reason 01 (deceased on the old platform, own request on the new) is documented in the notes and dictionary, not a fork. DEL05 and NEW moves, first-transaction logic, rejected rows and overseas rows are consistent with specification 3.2.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows or more | roll_transactions 321,192 rows (also 145,252 and 151,041) | yes |
| Distractors | 2 or more in metadata.json, none named by file name | subnational_population_estimates_jun2024.csv (wrong-basis) and census_2025_field_operations_summary.pdf; the thread also found pes_2025_sampled_meshblocks.csv unused. No name labels one | yes |
| Distractor relevance | unused, weighs, ruled out by a shipped fact | 2018-base estimates at 30 Jun 2024 ruled out by plan 2.1 (census day population); the thread did not find it carrying the call | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, png), both present | yes |
| Asks | multi-dimensional, unit and rounding stated | 16 regions by organisers, added, died; "whole number" | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 05 (allocation to a fixed total); 16 x 3 figures plus components exceeds 25 | yes |
| Not LLM-generated, golden realistic | read | thread found the files read as system output; no authoring language | yes (thread's read) |

## Gate G reconciliation
Thread: method_or_model_selection / etl_conformance, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: field_method, analytical, decisive step measuring DSE correlation bias against the demographic-analysis sex ratio. They match. The declared distractor (the June 2024 estimates) is not named by the thread as the surface read; the surface read the thread names is the DSE as it stands (8 regions off) and the census counts (14), which are the declared default path, so the distractor is not too load-bearing. Gate H: thread says domain pass, layers pass, decisive_step analytical. Design note Three rules agree. One mismatch to record: SF16 in the fork table is marked closed by specification 2 "country's time", but that sentence does not close the UTC basis of the stored stamps. The note also says the roll log's UTC stamps sit on the asks' path only; the asks are free of Rule 3 and they carry this as a data-semantics device, which is legal, but the fork has to be filed.

## Stump power (Gate F)
Good. A strong analyst who cleans everything and reads every rule can still file the DSE as it stands (8 regions wrong) or the census counts (14 wrong). Reaching the golden needs demographic analysis rebuilt from births, deaths (both layouts) and movements, and the judgment that the shortfall is confined to men 18 to 49. The dual-system plus sex-ratio correction is the field's standard route for correlation bias, so the main thread should weigh it with the scored readers' result (library methods are textbook routes a strong solver takes, stumping 1.3). It is not applying a stated rule: nothing shipped names a dual-system estimator, dependence or sex ratio. The asks add the time-basis, reason-code and reversal devices.

## Findings, ranked
1. Unfiled time basis of PROCESSED (UTC after 3 Aug 2025, offset and DST) moves ask 1 columns in all regions. FIX_NOW, input_files, documentation only.
2. SF16 fork row is closed by a sentence that does not close it; update the note and assert it in checks.py.
3. Residual: age-range cut for the correction (see fork 2); the package supports the golden once the deaths workbook is read. No action required.
4. Hygiene passes, nothing exclusion-level. Cross-batch check not run (isolation).

## Next action for the author
Add one filed sentence to the PROCESSED row of roll_extract_data_dictionary.xlsx (and the migration notes) saying the old platform stamps in the country's time and the new platform in UTC, with the country's standard offset and daylight-saving period. File the WHAT (time basis and offset), not the conversion procedure. Rebuild with the golden unchanged, update the SF16 row, then re-judge once.
