# determinism-check report, task465, 2026-10-17 (pass 2: architecture 2, round 1)

(The earlier `determinism_check_report.md` is the architecture 1 pass and is not overwritten.)
Judge thread output: /tmp/determinism-check-task465-r1a2/verdict.md (one pass, one thread, sonnet, medium).

## Verdict
DETERMINISTIC (SOLUTION_WRONG does not apply)
**Disposition:** FIX_NOW (one graded cell family has a surviving rounding fork; the recommendation, every caseworker figure and asks 2 and 3 are unaffected)
**Stumping type:** mechanism: method_or_model_selection (joint estimation under dependence), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The plan fixes only each division's two marginal shares per band; eligibility is their conjunction, so the joint has to come from the pilot, the one file that observed both traits. Independence staffs 26; the pilot rejects it (odds ratios 3.07 and 3.15) and raking each band's pilot table to the survey shares staffs 37. 37 holds under every pilot-based joint tried (Mantel-Haenszel 3.11, pooled 3.04, rate-ratio form, by-division odds ratios, dedup variants, "don't know" as No). The one defect: the solution's claim that a by-division odds ratio "puts every cell on the same hundred" is false for North Metro, $25,000 to $49,999.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot latest complete screens | n/a | 3,309 addresses under $50k with Yes/No | yes |
| Equipment rate, high burden vs rest, under $25k | 10.3 vs 3.6 | 10.31 vs 3.61 | yes |
| Same, $25k to $49.9k | 11.3 vs 3.9 | 11.26 vs 3.88 | yes |
| Odds ratios | 3.07, 3.15 | 3.069, 3.148 | yes |
| Eligible by division (nearest 100) | 700/900/1,400/1,300/1,500/1,100/2,500/2,200/1,500 | 685/900/1,398/1,292/1,497/1,088/2,502/2,200/1,510, same hundreds | yes |
| 18 division-band cells | CSV | all 18 match | yes |
| Caseworkers | 2/3/4/4/4/3/7/6/4 = 37 | same, from unrounded and rounded counts | yes |
| Independence staffing | 26 | 26 | yes |
| Baseline households open 31 Oct 2026 | 960/754/1,494/1,422/1,272/1,156/3,518/3,303/3,414 | identical (17,293 households) | yes |
| Battery households, Jan 1 to Oct 31 2026, Central Time | 212/124/303/259/234/184/623/640/600 | identical (3,179 households) | yes |

## Competing answers that survived
1. **North Metro joint (graded cell).** The pilot covers North and South Metro, so division-specific odds ratios exist (North Metro 3.47 and 3.63, South Metro 2.75 and 2.95). Using them North Metro $25,000 to $49,999 is 967.7 households, which rounds to 1,000 against the golden 900, and North Metro total is 2,300 against 2,200. South Metro cells and all 37 caseworkers are unchanged. The gap between divisions is not significant (log OR gap 0.23, SE about 0.47), so pooling is better justified, but nothing shipped files the pooled estimand. Affects the CSV North Metro $25k to $49.9k row and the xlsx North Metro total (ask 1), not the call.
2. **Division for asks 2 and 3 (minor).** The enrolment file's DIVISION column labels 1,422 Kestrelmere rows "Central" and 44 later rows "Southwest"; the register puts Kestrelmere in Southwest. Column reading: Central 1,876, Southwest 2,914. Register reading (golden): Central 1,272, Southwest 3,518. The register is the plan's stated authority and the better-forced reading, but the data dictionary only says "Service division of the account", so a literal reader could split.
Closed forks: first vs latest screen, "don't know" as No, rate-ratio joint, Mantel-Haenszel (same hundreds); UTC without conversion (closed by the dictionary line on Central Time); orders vs accounts vs households (closed by "households" and PRIOR_ACCOUNT_NO).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 or more rows | medical_baseline_enrolment_2026.csv, 38,827 rows | yes |
| Distractors named, no file name labels one | 2 or more | heat_vulnerability_index_county_2025.csv, energy_assistance_applications_2025.csv in metadata.json; names are neutral | yes |
| Distractors unused, weighable, ruled out by a shipped fact | yes | judge found both unused and relevant-looking; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | nine divisions or eighteen cells each; households to the nearest hundred stated for the eligible figures. Asks 2 and 3 are exact household counts with no rounding sentence, which reads as exact | yes (note) |
| Prompt shape and 25 or more rubric criteria | identifiable, 25+ | shape 07 in metadata; the note plans a rubric of about 20 ask criteria plus the main block. The generated rubric is not in the folder, so the count of 25 is not verified here | not verified |
| Not LLM generated; goldens real | yes | judge saw no authoring language; prompt is 735 characters, one paragraph | yes (hygiene); golden realism not judged by this pass |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; the default path is the product of the two shares (26); the decisive step is the pilot's within-band association carried into cells that keep both surveys' shares (37). These match. Neither declared distractor was named as carrying the task. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical. Matches the note's `## Three rules` (statistical matching with auxiliary information).
One reconciliation finding: the card's `analyst_test` text is stale against the built pack. It says the product counts "about half" the households and staffs about 14, and that the right method staffs 25. The built pack, the note and the judge say 26 and 37. Update the card.

## Stump power (Gate F)
Plausible and real. The plan's wording invites multiplying the two shares, which files 26 and understates eligibility in every division. Only a solver who tests independence with the pilot (never mentioned in the plan, and covering just the two metro divisions) reaches 37. Residual risk is a solver who reaches the pilot by habit; the margins are fair (closest threshold Southwest 2,502 against 2,400). Odds ratios from 2.75 to 3.6 all give 37.

## Findings, ranked
1. North Metro $25k to $49.9k cell (and the North Metro total) differs under division-specific odds ratios: 1,000 and 2,300 against 900 and 2,200. The design note's and solution's claim that by-division ratios land on the same hundreds is false. FIX_NOW.
2. Kestrelmere DIVISION-column mislabel in the enrolment extract affects asks 2 and 3 (Central and Southwest). Minor; the register is the stated authority, but the dictionary does not say the column is stale.
3. Card `analyst_test` carries the earlier architecture's numbers (14 and 25).
4. Rubric criterion count of 25 or more is not verifiable from the folder.

## Next action for the author
In the generator, file the pilot's odds ratio as pooled across the pilot's divisions within each income band (a WHAT: estimand) in the prompt or methods text, or make the North Metro $25k to $49.9k cell robust; correct the "by-division odds ratio gives the same hundreds" claim in `submission.md` step 5 and the design note. Optionally add one line saying the DIVISION label for Kestrelmere changed in July 2026 and that divisions follow the register. Refresh the card's `analyst_test`. Then run the one re-judge.
