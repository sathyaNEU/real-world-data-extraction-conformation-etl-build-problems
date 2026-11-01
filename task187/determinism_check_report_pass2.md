# determinism-check report, task187, 2026-11-01 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (final). First thread: DETERMINISTIC, SOLUTION_WRONG, FIX_NOW on step 5. The author restated step 5 in full; the one permitted re-judge (scratch /tmp/determinism-check-task187-1793554859/, verdict.md) returned DETERMINISTIC, APPROVE with step 5 reproducing as written.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Re-judge result: CH04 88.2 (88.9 at Cp 0.470 exactly), CH02 64.5 (65.3), the other eight turbines between -1.1 and +0.4 MWh, fleet-cell cross-check CH04 83.9, CH02 58.1. Fit and reference-turbulence variants (window, mean or median, ratio form) all give 100 MWh; only an unmotivated flat 0.12 reference gives 150. CH04 first in every variant. Its two optional wording notes (step 2's platform-change date is not observable in any file; step 7 should say the ten-minute record fills the part-windows) are applied in submission.md with no figure moved.

## Why
Read literally, OM-07 2.3 to 2.6 (last twelve months, states 10 and 20, as-new energy in the same winds less energy produced, CH09 on its pool rotor only) makes CH04 the largest blade loss, 76 to 89 MWh under every principled method, so 100 MWh at the 50 MWh rounding. CH04 leads CH02 by 20 to 25 MWh under all methods. The easy route (Schedule 3 shortfall at the same mean wind) books CH07 (235, so 250), and ignoring the rotor swap puts CH09 first. Both ask outputs (per-turbine metered generation, ten values; farm export by local month, ten values) reproduce. The defect was in the written method only: step 5 (Cp 0.470, Gaussian averaging over each record's own TI) gave CH04 76.2 and CH02 56.0, with healthy turbines negative, not 89 and 65. No committed answer is affected.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Shortfall vs Schedule 3, 0.5 m/s bins (CH07, CH01, CH05, CH04, CH02) | 235, 115, 114, 93, 71 | 235, 115, 114, 93, 71 (interpolated: 228, 113, 111, 89, 68) | yes |
| Blade loss CH04 / CH02, step 5 as originally written | 89 / 65 | 76.2 / 56.0, CH07 -70, CH01 -47 | no (first thread) |
| Blade loss CH04 / CH02, step 5 as restated | 89 / 65, others within 1 MWh | 88.2 to 88.9 / 64.5 to 65.3, others -1.1 to +0.4; fleet cells 83.9 | yes (re-judge) |
| Blade loss CH04 / CH02, healthy-fleet turbulence-binned reference | 89 / 65 (cross-check 83) | CH04 85.0 (80.5 to 86.9), CH02 55.6 to 65.6; regression 85.8 / 66.4 | yes, within method spread; 100 MWh under every licensed variant |
| CH09 from 25 Apr 2026 | pool rotor | WO-25925 back 25 Apr 14:20; crane log P08 = CH09; pool-rotor loss about 0 to 2 MWh | yes |
| Metered generation, ten turbines, MWh | 6708, 6770, 6554, 6327, 6404, 5966, 6394, 6398, 5938, 6394 | 6708.1, 6769.8, 6553.9, 6327.0, 6404.0, 5966.0, 6394.4, 6398.3, 5937.7, 6393.9 | yes |
| Farm export by local month, MWh | 6960, 9765, 5121, 6819, 8310, 5868, 2513, 3267, 5634, 6334 | 6960.3, 9764.7, 5120.7, 6818.7, 8310.3, 5867.7, 2513.1, 3267.3, 5633.6, 6334.4 | yes |
| SCADA clock (interval end, UK local then UTC) | stated in step 2 | recovered by correlation with the mast only; not documented in the pack | yes, with note |

## Competing answers that survived
- F1, rounding edge: licensed estimates 76 (first-principles), 81 (leave-one-out), 85 to 87 (healthy reference), 89 (golden) all give 100. Only a self-contaminated reference (67 to 72, an analyst error) gives 50. The first-principles route sits about 1 MWh above the 75 edge. Thin, not contested by a licensed method.
- F2, wind source in OM-07 2.4 ("the same winds"): turbine's own nacelle wind gives CH04; mast winds give CH07. No sentence names the source. Closed by sense, not by text. Residual.
- F3, "as new" as Schedule 3 at mean wind (CH07, 250) against as new at the record's own turbulence (CH04, 100). No filed sentence says turbulence matters; the data separate them (healthy turbines deviate from Schedule 3 monotonically in sd/mean, CH07 tracks TI and is flat in time, CH04 and CH02 carry a TI-independent offset). Analytical discovery, not a withheld rule.
- F4, window-end timezone for per-turbine generation: at most 1 MWh on CH05, CH07, CH08; covered by "site local time".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | SCADA parquet 522,159 rows (also export 17,520, mast 10-minute csv) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | anm_instructions_glenrigg csv, lost_production_2024_25.xlsx; neither labelled by name | yes |
| Distractors weigh yet unused | relevant, ruled out by a shipped fact | ANM overlaps only 147 state-10 intervals (about 0.02 MWh); lost_production is the superseded rev-2 method, board of 13 Nov 2025; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 10 turbines and 10 months, MWh to nearest MWh; recovered energy to nearest 50 MWh | yes |
| Prompt shape / rubric | identifiable shape, 25 or more criteria | shape 14 (cuts of a distribution by segment); graded items count about 25 (call, energy, chart, 10 + 10 figures); rubric is portal-generated, not verifiable here | yes, argued |
| LLM-looking | none | none found (varied work-order time formats, gaps around outages, fall-back duplicate hour) | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, decisive step comparing each turbine with an as-new turbine at its own ten-minute turbulence instead of matched mean wind; Layer 2 estimand identification; Layer 1 clock, mast stamps, state codes, rotor swap. No mismatch. The surface read that carries the task is the Schedule 3 shortfall by bins (CH07), which is the easy route and not a declared distractor; the declared distractors (ANM log, lost_production 2024-25) are not load-bearing. Gate G: no shipped artifact ranks the candidates wrongly on the decision question. Pass.
Gate H: domain pass (turbulence normalisation of a capped cubic ten-minute power curve, fails the swap test); layers pass; decisive_step analytical. Matches design note and card. The note's analyst_test (cleaned shortfall vs warranted curve books the plantation-edge turbine) is borne out by CH07 235 MWh.

## Stump power (Gate F)
Good. Two plausible wrong landings: CH07 via Schedule 3 at mean wind or mast winds, and CH09 if the rotor swap is missed. Turbulence normalisation is IEC 61400-12-1 Annex M, a textbook route for a strong wind analyst, so a capable solver can land it; the main ladder reasoning stays with the design note. The 100 MWh bin is thin on the first-principles route (about 1 MWh over the 75 edge), so energy may split even among solvers who land CH04.

## Findings, ranked
1. Step 5 as originally written did not reproduce (76/56 vs 89/65). Closed: restated step 5 reproduces in the re-judge.
2. Rounding edge: 100 MWh sits 14 over the edge for the best method and about 1 over for first-principles. Optional hardening (deepen CH04's loss about 10 MWh in the generator) would be SEND_BACK cost and moves graded figures.
3. F2: OM-07 2.4 does not name the wind source. Optional single sentence naming the turbine's own wind, without filing the turbulence method.
4. The SCADA timestamp convention (interval end, local then UTC) is documented nowhere in the pack and is recovered only by correlation; effect confined to October 2025.
5. IEC 61400-12-1 Annex M is cited in step 5 but not shipped (acceptable as field knowledge).

## Next action for the author
None required for determinism. Optional: the rounding-edge and OM-07 2.4 wind-source hardening in findings 2 and 3, both at send-back cost or a prompt-side change.
