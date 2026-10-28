# determinism-check report, task464, 2026-10-28 (pass 7)

Thread run by the main session on the brief from pass 6, against the final target.zip (md5 491993a850683ec6a7096285dc1d16a9; only pcn_practice_profiles_2026.xlsx document properties differ from the copy the thread read). Raw verdict: /tmp/determinism-check-task464-1793180641/verdict.md.

## Verdict
NOT_DETERMINISTIC (the call is forced; the top practice's figure and ranks 4 to 7 are not). Failure type: margin_or_boundary_fragility / underspecified_objective on the xlsx figure and ranks 4 to 7.
**Disposition:** SEND_BACK (bundle may stay; prompt and golden change).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
No shipped file fixes the model behind the "expected number". The call (Marrick first, Cobbet second) held under every variant. The 170 did not reproduce: base reconstructions 153 to 160, variants 97 to 195 (12% lapse rate the main lever); step-3 hazards came out near 1.1/0.9 or 1.4/0.7 against 0.93/0.20 depending on the definition of "new start". Ranks 4 to 7 differ by 3 to 8 patients and tie when recent exhausted repeats are treated as re-authorised or when rounded to 10.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Population | 8,648; Marrick 1,648 | 8,648; 1017/829/877/1961/1648/1192/1124 | yes |
| CC1 lapse | 12% | 12.0% (13,590 repeats); bimodal, 12.0 to 13.6% for 30 vs 60 days | yes |
| Marrick figure | 170 | 153 to 160 base, 97 to 195 across variants | NO |
| Order | Marrick, Cobbet, Fennbridge, Wyndhollow, Thistlecombe, Larkspur, Pellow Green | top 3 stable; Wyndhollow 58-63, Thistlecombe 43-53, Larkspur 38-49, Pellow 35-43, ties in one variant | top 3 yes, 4 to 7 NO |
| Stop hazards | 0.93% / 0.20% | about 1.1/0.9 or 1.4/0.7 | NO |
| R1 | 81.0, 80.3, 81.9, 77.8, 79.9, 75.8, 92.9 | same (694, 523, 587, 1432, 1123, 669, 750 denominators) | yes, all 7 |
| R2 | 82, 83, 83, 71, 84, 58, 55 | same (strict ">" the anniversary; ">=" gives Fennbridge 78.6, Cobbet 66.7) | yes, all 7 |

## Competing answers that survived
- Figure: 150 to 190 for Marrick depending on rate, interval, lapse treatment, hazards; acute-only patients (96, 22 at Marrick) uncounted in the brief.
- Ranks 4 to 7: tie or reorder under recent-exhaustion treatment and rounding to 10.
- Call: none (prior-year rate gives Cobbet 147, largest list gives Fennbridge: wrong routes).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / csv, jsonl, pdf, xlsx | yes |
| Large file | 25,000 rows | 300k-row issues A | yes |
| Distractors | 2+ in metadata, unlabelled in names | qof_cvd_achievement, dispensed_items_cvd named; unused, weighed | yes |
| Deliverables | 1 to 3, all in golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding | figure ask ties and sub-tolerance at ranks 4 to 7 (judge) | no on the figure; R1/R2 yes |
| Prompt shape / 25 criteria | identifiable, 25+ | shape 01; rubric not checkable here | not verified |
| Realism | no LLM tells | judge: none | yes |

## Gate G reconciliation
Judge: forecasting / analytical_non_defect / no / no, Gate G passes. Card and design note: method_or_model_selection, stump_class analytical, decisive step the clock a forward estimate runs on. Same mechanism, no mismatch. The prior-year-rate lure (Cobbet 147) matches ladder rung 1; it is not a declared distractor, and the declared distractors (QOF, dispensed items) are not carrying the task.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules.

## Stump power (Gate F)
Good per the judge: both easy routes miss. Risk: a run-out count of authorisations before March also reaches Marrick, so the call may be landable by a strong solver (stumping 1.3); main thread to weigh against the ladder.

## Findings, ranked
1. Figure and ranks 4 to 7 not forced by the filed text (Gate C), the only blocking finding.
2. Stop-hazard definition (new start) not reproduced from step 3 as written.
3. Acute-only patients and recently exhausted repeats unspecified.

## Next action for the author
Drop the figure and the full ranking from the asks (done in the repaired prompt: placement, runner-up, populations) and re-judge once as pass 8 on the unchanged bundle.
