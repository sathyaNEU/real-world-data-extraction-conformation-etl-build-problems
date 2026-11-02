# determinism-check report, task501 pass 4, 2026-11-02

## Verdict
NOT_DETERMINISTIC (confined to the register asks 3 and 4 of winter_measles_2027.xlsx; the call and all six reproduction numbers are forced)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read word for word, asks 3 and 4 (people per option, no valid dose, exactly one) have no single answer. The golden needs two inferences no shipped file states: (i) 104 registrations whose date_of_birth is ten years early are moved +10 years (registered 6 to 45 days after DOB+10y, first GP dose 12 to 17 months after it); (ii) the second of two same-day GP lines on 228 registrations is given to an unmerged twin registration. Guidelines ch.12, circular 03/2024, the merges file, the GP query log and the register columns file neither. A literal solver gets different people counts and dose counts in at least four of five options. Gates C and E fail on asks 3 and 4 (underspecified_objective). The call, ask 2 and the deck pass.
The design note's fork rows SF30 and SF31 close these by "C1 in the data ... nothing filed", i.e. by convergence inside the data, which a literal reader cannot be expected to find. That is a hidden rule on the asks.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Susceptible share 15-19 on 1 Jan 2028 | 11.2% | 11.2% (3,992 of 35,572), profile joined to projection | yes |
| Region susceptible share | 4.8% | 4.83% | yes |
| R no catch-up | 1.3 | 1.299 | yes |
| R A / B / C / D / E | 1.3 / 0.9 / 1.3 / 1.3 / 1.3 | 1.288 / 0.892 / 1.292 / 1.292 / 1.289 | yes |
| People A / B / C / D / E | 35,840 / 33,665 / 29,810 / 31,016 / 58,570 | same, only under both inferences | yes, golden reading only |
| No valid dose A to E | 3,576 / 4,354 / 2,897 / 5,029 / 8,597 | same, golden reading only | yes, golden reading only |
| Exactly one A to E | 4,795 / 6,155 / 4,005 / 7,414 / 11,964 | same, golden reading only | yes, golden reading only |

## Competing answers that survived
- DOB as filed (no decade correction): people A 35,798 / B 33,629 / C 29,826 / D 31,042 / E 58,632; B one-dose 6,149. Shipped rule meant to close it: none.
- 12.5.2 read literally, second same-day line simply invalid (no twin reassignment): none A 3,581 / B 4,362 / C 2,901 / D 5,047 / E 8,620; one A 4,842 / B 6,184 / C 4,041 / D 7,421 / E 12,000. Shipped rule meant to close it: none.
- Closed forks (no finding): merges documented in the merges file; LH27 scheme by lho_recorded date per circular 03/2024; "by that date" is date_given (13 late-loaded doses, immaterial).
- On the call: holiday-only or pooled diaries give R 0.8 to 0.9 and "no catch-up needed". That is the intended wrong route, not an open fork; no option other than B reaches one on any reading (B 0.892 against others 1.288 to 1.292).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 rows or more | events file 283,131 rows (also 23 MB) | yes |
| Distractors | 2 or more named in metadata, none labelled in a file name | national_mmr_uptake_report_2027q1.pdf, mmr_stock_return_2027-06-30.csv; neither named as a distractor | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | judge: unused by the solution; the NSCS population xlsx is only a symmetrisation weight and moves nothing beyond 0.001 | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt states one decimal for R and whole numbers for people | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape 07 (grid of cells) per metadata; the criterion count was not computed in this pass | shape yes, count unverified |
| Reads as real, not LLM generated | yes | judge found no authoring disclosures; register reads as system output | yes |
Note (Gate B, low grade): no shipped file states that a December to February winter is school term; one filed sentence (a school-term note) would remove the dependency on general knowledge.

## Gate G reconciliation
Judge: mechanism method_or_model_selection (which contact diaries represent the winter), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The pooled-diary route is the easy wrong read, and the difficulty survives clean data. This matches the design note's stump (term-time against holiday diaries, every reading a fork row landing on B). The declared distractors are not the surface read carrying the task. No mismatch on the main call.
Gate H line: domain: pass; layers: pass (Layer 1 LH scheme revisions, merged registrations, GP query log, PDF tables; Layer 2 age-structured next-generation-matrix R from seasonal contacts); decisive_step: analytical. The register devices (decade-keyed DOB, twin lines) are planted defects and rule application, but sit on the asks, which are free of rule 3; their fault is determinism, not stump class.

## Stump power (Gate F)
Good on the main call: pooling all 7,560 diaries or using the larger holiday set gives R 0.9 and the opposite call, and a strong analyst can plausibly take it. The register asks will also break many answers, but two layers are unfiled, so they fail for the wrong reason.

## Findings, ranked
1. SEND_BACK: ask 3 and 4 depend on two unfiled inferences (decade-keyed DOB, 228 twin-held same-day lines). Underspecified_objective.
2. Low: no filed statement that winter is school term (Gate B).
3. Note: criterion count for the 25 criteria not verified in this pass.

## Next action for the author
Reopen only asks 3 and 4 (R side, call and deck frozen) and either (a) ship a file that makes each inference recoverable by a literal reader (a register correction log or export note covering the decade-keyed dates of birth and the twin-held same-day lines), or (b) restate the asks and golden on the documented reading, DOB as filed and 12.5.2 applied literally, which recomputes to the second-reading figures above and needs no new file. Add one school-term sentence if the pack is reopened.
