# determinism-check report, task307, 2026-10-27 (pass 1)

Note: this report records pass 1 on the pack as cut at stage 4. The build was repaired afterwards (F1 to F3 fixed, the probe-index ask dropped); a pass-2 re-judge runs separately. Findings below describe the pass-1 pack, not the repaired one.

## Verdict
DETERMINISTIC (main call and ask 1); not SOLUTION_WRONG. Supplementary families (workbook asks 3 and 4, brief ask 3) held only under conventions no shipped file stated.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Re-assigning the 2028 AM and PM tables to user equilibrium on the no-build and each build network reproduces every golden figure, none near a rounding boundary. Guidance 3.1 (largest annual benefit) names TIP-28-009. The fixed-volume easy route names Route 9 (196,483), the wrong project. Three conventions were unfiled (F1 to F3 below); none moves the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Center Street annual benefit / per USD 1M | 323,000 / 8,300 | 322,911 / 8,301 | yes |
| Route 9 | 159,000 / 3,400 | 159,166 / 3,401 | yes |
| Southport | 126,000 / 4,900 | 125,963 / 4,901 | yes |
| Ferry Street | 37,000 / 2,100 | 37,203 / 2,102 | yes |
| AADT (8), K (8) | block 4 | exact (AADT diff at most 0.3 veh) | yes, only under the golden's valid-hour rule (F2) |
| Validation (12 cells) | block 4 | exact | yes, same condition |
| Planning time index (8 cells) | block 4 | exact | yes, only under end-of-interval stamps (F3) |
| No-build link volumes vs loaded network file | n/a | within 0.05 veh | consistent |

## Competing answers that survived
- F1, Route 9 link 2 FTYPE after widening: recoding to FTYPE 1 gives Route 9 229,560 / 4,905 instead of 159,000 / 3,400. Call and ranking unchanged; only the Route 9 pair in ask 1. Closed by guidance 4 (the coding sheet is the record), but it needs a fork-table row.
- F2, carry-over after a multi-day outage: manual 3.2 never says counters carry missed hours. Dropping the first poll after any NR moves AADT by up to 49 vehicles (S-0101 74,488 vs 74,514; S-0104 57,641 vs 57,690; S-0103 19,384 vs 19,390) and validation cells (S-0101 WB AM -1.2 vs -1.3; EB PM -9.2 vs -9.3). K unchanged at three decimals.
- F3, probe stamp convention: the CMP memo did not say start or end of interval. Start-stamp gives CS 2.57/2.29, HA 1.41/1.43, R9 1.88/1.75, SP 2.03/1.88, so all eight indexes change. UTC to local conversion is data-forced.

## Spec gates (pass-1 pack)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 16 / 4 (csv, xlsx, pdf, parquet) / ATR 140,160 rows, probe 900,091 | yes |
| metadata.json distractors, none named by file name | 2+ | 5 named (crash xlsx, MRTA csv, probe parquet, CMP reference csv, CMP memo pdf); no file name labels one | yes on the declaration |
| Distractors unused by solution, relevant, ruled out by a shipped fact | each | the probe parquet, reference csv and CMP memo were used by the pass-1 solution (planning time index ask), so three of five were not distractors | no at pass 1; resolved only if the dropped ask leaves them unused (pass 2 to confirm) |
| Deliverables 1 to 3, all in golden | 1 to 3 | 2 (xlsx, pptx), both in golden | yes |
| Asks multi-dimensional with unit and rounding | each | yes (prompt states unit and rounding for each) | yes |
| Prompt shape identifiable, rubric 25+ criteria | 25+ | prompt shape clear; no rubric artifact in the folder, count not verifiable here | not verified |
| Reads as real work product, not LLM generated | yes | judge found no authoring language; realism good | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: analytical stump (re-assign trips to equilibrium versus re-time project links at no-build volumes), no decoy, no planted defect. Match. The declared distractors (probe files, crash, ridership) were not the surface read carrying the task; the loaded network file is undeclared and the judge calls it a consistent check, not a trap, which agrees with the note's "No decoy" line. Gate H: thread says domain pass, layers pass, decisive_step analytical, borderline toward rule_application because documentation 6.1 files user equilibrium. Card stump_class analytical, analyst_test and domain_test agree on the content; the note's Not-rule-application line argues the borderline, so the risk is the one the leak reader's question 6 also raised. No mismatch on the label, but the borderline reading is the finding most likely to be sent back.

## Stump power (Gate F)
Moderate. A solver who writes a correct UE solver lands the call and ask 1; only solvers who shortcut the assignment miss. Most graded weight sits in the ATR and probe asks, where F2 and F3 cost careful solvers credit as data semantics, not a valid stump. The decisive step is a textbook method (equilibrium assignment, filed in 6.1) that a strong solver takes: the main thread should weigh this against the note's ladder (two solvers both landing the call puts the pair near the 60 ceiling).

## Findings, ranked
1. F3 probe stamp unfiled, plus the probe family used by the solution while declared a distractor (resolved in the repair by dropping the ask; confirm in pass 2).
2. F2 carry-over after multi-day outage unfiled (repair: filed in manual 3.2).
3. F1 Route 9 FTYPE after widening needs a fork-table row (repair: sponsor description now says the weaving remains; SF16 asserted).
4. Decisive step borderline toward rule application (documentation 6.1 files the method); argue it in the ladder.
5. Rubric criterion count not verifiable from the folder.

## Next action for the author
Wait for the pass-2 re-judge on the repaired pack; confirm there that the probe files are truly unused by every remaining ask and graded figure, and that the dropped ask leaves the asks still at 25 or more rubric criteria.
