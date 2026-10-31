# determinism-check report, task471, 2026-10-31 (pass v5r4)

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG on one critical component (component 2 only; no graded figure moves).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Plan 2.1 to 3.1 forces the 200 organisers: adults whether or not the census counted them, less residential electors, largest remainders. The one defensible route builds the dual-system estimate in the PES cells with the formula (census less imputed) x correct-enumeration x P/M, sees its men aged 18 to 49 about 4 per cent under demographic analysis while its women agree, and corrects the men to the DA sex ratio. All sensible correction variants give the golden 27/20/25/26/29/5/11/12/7/5/4/8/6/3/8/4. The supplementary figures reproduce under a literal reading of the specification. The isolated thread (sonnet, medium, scratch prefix only) wrote verdict.md at /tmp/determinism-check-task471-v5r4/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Residential electors (roll_at_close, ADDRESS_TYPE R) | 3,329,031 | 3,329,031 (regions too) | yes |
| DSE adults | 3,593,178 | 3,593,109 | NO (69 people, 0.002%); no allocation depends on it |
| DA men per woman 18-24 / 25-34 / 35-49 | 1.04 / 1.03 / 1.02 | 1.044 / 1.031 / 1.021 | yes (robust to age-from-birth-year convention) |
| DSE men per woman | 1.01 / 0.99 / 0.97 | 1.006 / 0.991 / 0.973 | yes |
| Corrected adults | about 3.63M | 3,633,890 | yes |
| Organisers | golden | golden exactly | yes |
| Raw-DSE alternative | 26/20/26/28/31/4/11/12/6/4/4/8/6/3/8/3 | same | yes |
| Census-count alternative | changes 14 regions | same | yes |
| NEW_ELECTORS | 166,710 | 166,710, all regions | yes |
| REMOVED_DIED | 33,188 | 33,188, all regions | yes |

## Competing answers that survived
No answer survived as a competing golden. Forks tried and closed:
- Raw DSE (8 regions differ): the easy route, undefendable once the sex-ratio contradiction with DA is seen; the vital notes state the series are complete.
- Census counts: contradict plan 2.1 "whether or not the census counted them".
- Imputed records kept as correct enumerations: gives 25/19/24/26/28/6/12/13/7/6/5/8/6/4/7/4. Nearest reading fork. Closed by the methods report ("name no one to check") and the flagged imputed column; the standard formula excludes them.
- Men set to own women x national DA ratio: 30/22/27/27/30/5/12/13/2/5/5/4/6/4/4/4; erases real regional structure.
- Scaling variants (men only, 18-64, flat 4 per cent) give the golden; crude raking flipped two regions only through a crude birth-year mapping.
- Sixth largest remainder Nethermoor 0.60 against Rowanlea 0.39, held across all variants.
- Time zone (naive UTC gives 167,048): closed by specification note 2.
- Old-platform R25- electorate numbering (shifts 3,896 people): not stated in any document; settled by data (105 of 105 cross-platform records agree under the 2023 mapping, 40 of 105 under the naive one). A data-discoverable key mismatch, so Layer 1.
- 34 death removals reversed only after 30 June 2026: literal text counts them reversed (golden); a period-limited reading gives 33,222. Judge treated as closed by the literal text. Watch item.
- 203 CORRECTS_TXN references outside the extract: treated as additions, consistent with the golden.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows | roll_transactions_2025_2026.csv 362,786 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | 2 (subnational_population_estimates_jun2024.csv declared wrong-basis, census_2025_field_operations_summary.pdf); no file name labels one | yes |
| Distractor unused and relevant | ruled out by a shipped fact | the 2018-base estimates ruled out by plan 2.1 (date and base; age groups do not isolate adults) | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 16 regions x 3 figures, whole numbers stated | yes |
| Prompt shape and 25+ criteria | shape identifiable, rubric 25+ | shape 05 named in metadata; rubric is generated at the portal and cannot be counted here | shape yes, count unverified |
| Not LLM-generated, golden realistic | yes | no authoring text found by the thread; golden is a plain 16-row CSV | yes (thread-level) |
| Licence record | source, date, licence | metadata.json: original work, 2026-10-14 | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card (stump_class analytical): stump is the DSE correlation bias measured against DA sex ratios, with the declared wrong-basis distractor (2018-base estimates) ruled out by plan 2.1 and never the stump. Match. The thread did not name the distractor as the surface read carrying the task. Gate G classification: pass (analytical_non_defect, no ranking artifact, distractor not load-bearing). No mismatch.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test and the note's Three rules (No decoy, Not semantics, Not rule application each present).

## Stump power (Gate F)
Moderate to good. The raw DSE is the textbook route and gives 8 wrong regions of 16. The check against DA is not asked for by any shipped sentence, so the open question is whether strong solvers cross-check; the data separate the candidates and the vital notes call the series complete. The thread did not class the decisive step analytical merely because it is standard; it described the correction as needing an observation the data must show. The main thread should weigh, against the ladder, that a strong census-methods solver reaches the DA correction as a textbook organ (stumping 1.3). The heavy ETL (time zone, two platforms, person identity, reversals) adds ask-side difficulty.

## Findings, ranked
1. SOLUTION_WRONG, critical component 2 (FIX_NOW): submission states DSE adults 3,593,178; the shipped method reproduces 3,593,109. Restate as 3,593,109 or "about 3.59 million", then re-check step 2 in the generator so the claimed figure is what checks.py asserts. No allocation, prompt or bundle change.
2. Watch, reading fork on the 34 death removals reversed after 30 June 2026 (33,188 vs 33,222 under a period-limited reading). The literal text settles it for the golden; consider whether the filed sentence should say "in the extract" so no reviewer reads it otherwise. Region-level effect on REMOVED_DIED unconfirmed.
3. Watch, imputed-records reading is the nearest fork on the main call; closed by the methods report and the census workbook flag, not by the plan. Confirm the fork-table row says "same call"/closure.
4. Optional: solution steps could say old-platform electorate codes follow the 2020 review (data-settled, not shipped as a sentence).
5. Cosmetic: CORRECTS_TXN values of the form `R25--006800` (double hyphen) look like a formatting artefact; harmless.
6. Rubric criterion count (25+) not verifiable here.

## Next action for the author
Correct critical component 2 in submission.md (and the generator assertion behind it) to 3,593,109, rebuild identically, and have the one allowed re-judge only if the main session wants it; nothing else moves.
