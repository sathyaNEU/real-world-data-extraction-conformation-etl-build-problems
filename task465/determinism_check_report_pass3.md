# determinism-check report, task465, 2026-10-17 (pass 3: architecture 2, round 2, the one re-judge)

Earlier passes (`determinism_check_report.md`, `determinism_check_report_pass2.md`) are not overwritten.
Judge thread output: /tmp/determinism-check-task465-r2a2/verdict.md (one thread, sonnet, medium, fresh unzip of the rebuilt target.zip).

## Verdict
DETERMINISTIC (SOLUTION_WRONG does not apply)
**Disposition:** APPROVE (one residual fork recorded below, closed by plan section 5 on the literal reading)
**Stumping type:** mechanism: method_or_model_selection (joint estimation under dependence), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The plan files each cell as the demographer's households times the energy survey's burden share and the health survey's equipment share in each division and band. That fixes both marginals, not the joint. Only the pilot observed both traits on one household; it rejects independence (odds ratios 3.49 and 3.47). Independence staffs 26; every way of putting the measured association into the cell lands on the same hundred in all 18 cells and on 38 caseworkers. Asks 2 to 4 reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot latest complete screens | n/a | 3,164 addresses (1,259 under $25k, 1,905 $25k to $49.9k); 3,117 with Yes/No | yes |
| Equipment rate, high burden vs rest, under $25k | 10.7 vs 3.3 | 59/549 vs 23/689 | yes |
| Same, $25k to $49.9k | 11.7 vs 3.7 | 39/333 vs 57/1,546 | yes |
| Odds ratios | 3.49, 3.47 | 3.487, 3.465 | yes |
| 18 division-band cells (nearest 100) | 500/200, 600/300, 900/500, 1,000/300, 1,000/500, 600/300, 1,700/800, 1,300/1,000, 1,200/600 | unrounded 493/192, 607/292, 906/492, 1,007/292, 991/497, 607/308, 1,705/807, 1,295/995, 1,193/593 | yes, all 18 |
| Division eligible | 700, 900, 1,400, 1,300, 1,500, 900, 2,500, 2,300, 1,800 | 686, 899, 1,398, 1,300, 1,488, 915, 2,512, 2,290, 1,786 | yes |
| Caseworkers | 2,3,4,4,4,3,7,6,5 = 38 | same, from unrounded and rounded counts | yes |
| Independence staffing | 26 | 26 | yes |
| Baseline households open 31 Oct 2026 | 933, 821, 1,506, 1,359, 1,313, 1,181, 3,500, 3,320, 3,391 | identical (17,324 households from 17,374 spells) | yes |
| Battery households, Jan 1 to Oct 31 2026, Central Time | 202, 161, 283, 255, 237, 219, 603, 641, 635 | identical (3,236 households from 3,497 orders) | yes |

## Competing answers that survived
Round 1 forks:
- **North Metro $25k to $49.9k (1,000 against 900): closed.** Own-division odds ratios, Mantel-Haenszel, pooled-over-bands, rate-ratio, "don't know" as No, no dedup and first-screen variants all keep the same 18 hundreds and 38.
- **Kestrelmere DIVISION label: closed in substance.** The dictionary now reads "Service division recorded on the account when it was set up" for the enrolment file, so the stale column is described. The judge states the premise county through the register governs (stale in 1,437 rows). The recorded-DIVISION shortcut gives other numbers (Central 1,938) but has one literal reading to reject.

Residual, from the judge and the main session's recomputation: fusing at county-by-band level and summing to divisions (13 to 22 interviews in the thinnest cells) keeps all nine divisions' caseworkers and the total of 38, but moves two graded hundreds (Central 1,432 against 1,500; Southwest under $25,000 1,618 against 1,700). Plan section 5 files the shares "in each division and band", so the division-level fusion is the literal reading, and the design note carries it as a fork-table row closed by that sentence (I did not find it by keyword in the note; the main session reports the row). It survives as an alternative a reviewer could argue, so it is a residual risk on the CSV and the xlsx eligible figures, not on the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 or more rows | medical_baseline_enrolment_2026.csv, 38,848 rows | yes |
| Distractors named, no file name labels one | 2 or more | heat_vulnerability_index_county_2025.csv and energy_assistance_applications_2025.csv in metadata.json | yes |
| Distractors unused yet weighable | yes | both unused by the solution, neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | nine divisions or eighteen cells each; nearest hundred stated for eligible figures; asks 2 and 3 are exact counts | yes |
| Prompt shape, 25 or more rubric criteria | yes | shape 07 in metadata; the generated rubric is not in the folder, so the count is not verified here | not verified |
| Not LLM generated; goldens real | yes | no authoring language seen; file register and dictionary tidy but plausible | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and note: stump_class analytical, default path the product of shares (26), decisive step the pilot's within-band association carried into cells that keep both shares (38). They match, and neither declared distractor carries the task. The card's `analyst_test` now agrees with the rebuilt pack (26 caseworkers, 8,200 eligible households), so the round 1 staleness is cleared.
Gate H: domain pass, layers pass, decisive_step analytical; matches the note's Three rules.

## Stump power (Gate F)
Moderate to good. The plan's wording invites multiplying the two shares, which files 26 and undercounts every division; the pilot supplies the dependence but nothing in the prompt announces it. The estimate is forced inside an odds-ratio window of about 3.2 to 3.9 (OR 3 gives 37, OR 4 gives 39) although the pilot's interval is wide (about 2.1 to 5.7): thin but clean, not contested. Smallest margin: Southwest 2,512 against 2,400.

## Findings, ranked
1. Residual county-by-band fusion fork moves two graded hundreds (Central, Southwest under $25,000), not the call; closed by plan section 5 on the literal reading only.
2. Rubric criterion count of 25 or more is not verifiable from the folder.
3. Minor: file_register.csv and data_dictionary.csv read as tidy folder indexes.

## Next action for the author
Ship. Optionally, to take finding 1 off the table, add three words to the ask's or the plan's wording stating that the shares and the fusion are taken at division and band level; otherwise confirm the generated rubric reaches 25 criteria at the ship step.
