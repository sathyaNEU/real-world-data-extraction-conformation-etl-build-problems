# determinism-check report, task156, 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one card text fix recommended, no rebuild)
**Stumping type:** mechanism: method_or_model_selection (forecast extrapolation across a regime change), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet pass, scratch /tmp/determinism-check-task156-200811/, verdict at verdict.md. target.zip sha256 200b0014d310ee60e8a5fb9b86bb8eec3ea9b5845bbfc7ed7f5e4c3daf9f91e3. Architecture 2; the earlier report belongs to a dead architecture and was ignored.

## Why
The groundwater-conditioned replay of 2004 to 2023 puts PS03 at about 3 overflows a year with the subdivision against condition 6's limit of 2, so condition 8 bars the connection until the upgrade (about 0.75 to 1 a year after). The easy routes (one rain response fitted on 2024 to 2026, or the station's own 2-in-2-years record) give about 0.65 a year and "connect"; the held-out June 2025 high-river weeks refute them. Gates A to E pass for the main call and asks 1 to 4.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Water use per dwelling, 11 quarters | 448 ... 313 | identical, all 11 (CCC dwelling dating is load-bearing: without it 440, 375, 334) | Yes |
| Other stations, 10 overflow/spill-hour pairs | as filed | identical | Yes |
| Emergency overflows 2024, 2025 | 3, 3 | 3, 3 | Yes |
| Infiltration per km below water table | 4.2 L/s | 4.206 | Yes |
| Fast / slow response | 30 / 6.0 | 30.2 / 5.93 | Yes |
| Median km below water table, 2024-26 / 2004-23 | 0.2 / 2.1 | 0.24 / 2.14 | Yes |
| Max km | about 21 | 21.4 / 21.0 | Yes |
| Replay events in 20 yr (now / with / with+upgrade) | 58 / 64 / 15 | 53 / 63 / 15 | Whole numbers yes (3 / 3 / 1) |
| Naive single-response replay | about 0.70 a year | 0.65 a year (13/13/0) | Yes |
| Held-out errors 43 and 0.2 L/s | as filed | not recomputed to the decimal; coefficients support | Partial |

## Competing answers that survived
- Ask 1 whole numbers under pump staging: if the replay lets the duty pump alone (61.8 L/s) run below about 8 m3, counts are 78 / 84 / 18, i.e. 4, 4, 1 a year. The SCADA (about 2 pumps at the 1.10 m level, 56 L/s each) argues for 112 L/s, but no filed sentence closes it. Main call unchanged; only ask 1 "without" and "with" cells move.
- Ask 1 "without" margin: judge's 2.65 a year sits near the 2.5 rounding line (golden 2.9). Rounds to 3 in every well-fitting variant run.
- "the catchment's residential water use": no file maps rating units to the PS03 catchment; the golden uses the whole residential metered roll, the only population available. Wording looseness, figures unchanged.
- Table 5.2 "New Zealand time" (NZST vs NZDT) moves counts by one or two events at most.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 | Yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, docx) | Yes |
| Large file | 25,000 rows or more | SCADA 99,360; hourly rain 192,864; meter reads 44,846 | Yes |
| Distractors in metadata.json, none named by file name | 2 or more | 2 (wwtp inlet, work orders); neither file name labels it | Yes |
| Distractor unused yet weighable, ruled out by a shipped fact | yes | WWTP inlet shows the June 2025 rise town-wide on both readings alike; per design note and judge, does not answer a graded quantity | Yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, docx, png), all present in golden/ | Yes |
| Asks multi-dimensional, unit and rounding stated | yes | 3 asks across 11 quarters, 10 station-years, 3 scenarios; units and rounding in the prompt's last sentence | Yes |
| Prompt shape, rubric 25 or more | yes | shape identifiable; rubric is generated at portal, not checkable here (about 27 separately gradable cells plus call and components) | Likely yes |
| Reads as real, not LLM generated | yes | judge found coherent in-fiction authors and dates, no generator text; no em dashes in prompt.txt or submission.md | Yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read no, sole_data_defect no. Design note and card: stump_class analytical, decisive step is conditioning infiltration on km of sewer below the water table and replaying each day with its own water table; Layer 2 is forecast_uncertainty (model chosen on held-out hours). These match. The declared distractors (WWTP inlet, work orders) were not named by the thread as the surface read carrying the task. Thread's naive route (0.65) agrees with the note's (0.70). No shipped artifact ranks the candidates wrongly.
Gate H (thread): domain pass, layers pass, decisive_step analytical. Matches the card's analyst_test and domain_test and the note's Three rules. The thread did not class the step analytical merely because the method is standard: it had to be reached through the held-out check and the bore/invert construction, with no filed rule. Note for the main thread: the hold call is reachable by a strong solver who thinks of groundwater infiltration, so stump power rests on that recognition; the thread judged it good.

## Stump power (Gate F)
Good. A single-response fit and the station record both file "connect". Reaching "hold" needs the datum conversion, km below the water table from the mains' inverts, a dry-hour infiltration fit, a km-scaled slow response and the out-of-sample check, with Layer 1 mess (UTC/NZST/NZDT, hour-ending stamps, serial swaps, ICP changes) also costing on the asks. No document hands over the mechanism and the prompt does not name groundwater.

## Findings, ranked
1. Card text is stale: card task156.json analyst_test says the consent replay is "2006 to 2025"; the prompt, golden and note use 2004 to 2023. Fix the card text only.
2. Ask 1 whole numbers can move to 4, 4, 1 under the duty-pump-alone reading; no filed sentence closes it (the call holds either way). Optional: have the data sheet or consent state that the station pumps at its full rated flow whenever the replay needs it, in the generator, then rebuild and re-verify (a rebuild reopens the gates).
3. Ask 1 "without" is near the 2.5 rounding line in the judge's reconstruction (2.65 vs golden 2.9); no change required.
4. "the catchment" in ask 2 is loose; optional wording only.

## Next action for the author
Correct the 2006 to 2025 wording in the card's analyst_test to 2004 to 2023, then proceed to ship; no re-judge needed. Take finding 2 only if you accept a rebuild.
