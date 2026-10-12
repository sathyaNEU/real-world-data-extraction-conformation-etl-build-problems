# determinism-check report, task121, pass 2, 2026-10-12

## Verdict
NOT_DETERMINISTIC (every golden figure reproduces; the main call is not forced by the shipped text). SOLUTION_WRONG does not apply.
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The prompt asks which facility is "behind the surge", and no shipped file defines how to attribute events to a source. CP-14 says only that the upwind check "on its own does not show which source did". The golden's hour-matched baseline (expected upwind events from the same clock hour on other days, then excess over it) is in no file, so it is a method the solver must pick, and other licensed baselines give other winners. Gate C and Gate E fail on the main recommendation and on the closest-rival answer. Taxonomy: underspecified_objective.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Season odor events | 499 | 499 (export, boundary point-in-polygon, dedupe, 2-hour household rule) | yes |
| Events in calm / no usable wind | 60 / 2 | 60 / 2 | yes |
| Upwind: Landfill / Ridgeway / WPCP / Kestrel / Sutter | 210 / 69 / 10 / 99 / 43 | 210 / 69 / 10 / 99 / 43 (needs the PDT-to-PST shift; unshifted gives 255 / 35 / 24 / 88 / 46) | yes |
| Hour-matched expectation: Ridgeway / Kestrel / Landfill | 26.4 / 76.5 / 299.1 | 26.4 / 76.7 / 299.1 | yes (Kestrel 0.2 off, minor) |
| Excess: Ridgeway / Kestrel | 42.6 (2.6x) / 22.5 | 42.6 (2.61x) / 22.3 | yes (minor) |
| All-hours baseline: Kestrel / Ridgeway | 2.69x / 0.39x | 2.69x / 0.39x | yes |
| Monthly complaints Jan to Sep | 29 30 28 27 89 90 120 119 100 (632) | same (prefix-truncation dedupe, 38 migrated rows removed, app times converted from UTC) | yes |
| Usable hours May to Sep | 743 669 740 738 717 | same | yes |
| Calm hours May to Sep | 38 35 44 39 46 | same | yes |
| Wind sector counts (437 events) | N82 NNE23 NE179 ENE3 E4 ESE43 S1 SSW4 SW51 WSW17 NNW30, rest 0 | same | yes |
| Facility bearings from station | n/a | Landfill 37.9, Ridgeway 237.9, WPCP 168.0, Kestrel 334.1, Sutter 118.1 | for the chart |

## Competing answers that survived
1. Pre-surge baseline. Each facility's upwind share among January to April events (107 events) applied to the 499 season events gives Kestrel 99 vs 37.3 expected (+61.7, 2.65x) and Ridgeway 69 vs 28.0 (+41.0, 2.46x). Answer: Kestrel, rival Ridgeway, against the golden's Ridgeway, rival Kestrel. No filed fact rules it out (the small baseline of 8 and 6 events and the winter wind regime are the solver's argument). The shipped rule that was supposed to close it: none.
2. All-hours baseline. Kestrel 2.69x against Ridgeway 0.39x. The golden rejects it only by the solver's own clock-hour argument.
3. Raw count of events upwind. The prompt literally asks for this per facility and it gives the Landfill (210). The procedure says it does not identify the source.
4. Time zone: unshifted local hour gives Landfill 255 / Kestrel 88 / Ridgeway 35. The readme settles it, so not counted as open.
5. Monthly complaint dedupe: contact plus noticed gives 91 93 123 123 101; address plus time gives 88 89 119 118 99; truncated-prefix gives the golden 89 90 120 119 100. The prefix rule is the only one consistent with the files ("One person's report" in CP-14) but it is not stated, a minor risk on workbook ask 1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, txt, geojson) | yes |
| Largest file | 25,000 rows or more | 78,624 rows (hfs_met_5min csv) | yes |
| Distractors | 2 or more declared, relevant, unused, not labelled in file names | 3 declared in metadata.json (operator_monthly_reports xlsx, hfs_pm25_hourly csv, kestrel_county_airport_hourly csv); no file name labels one; same world as the decision | yes |
| Distractor does not answer the question | rules out by a shipped fact | CP-14 states the airport observations are not used; operator reports and PM2.5 do not rank facilities | yes |
| Deliverables | 1 to 3 | 3 (docx, xlsx, png) | yes |
| Multi-dimensional asks | yes | monthly series, per-month hours, per-facility counts, 16-sector chart | yes |
| Deliverables present | all named | per metadata.json and the thread's recompute, all present | yes |
| Units and rounding | stated | "Counts are whole numbers" in prompt; hours and counts whole | yes |
| Prompt shape and 25 criteria | shape identifiable, 25 or more | shape 07 (call and rival, per-facility counts, 9 monthly cells, 5 usable and 5 calm hours, 16-sector chart); prompt 922 characters, over 25 criteria by cell count | yes |
| Realism | no LLM tells | the thread found mixed address casing, UTC app stamps, truncated resends, migrated cases, free-text log notes; nothing exclusion-level. The round 1 reader's realism tells (menu, boundary rectangle) are in the design note | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate G passes. Card: stump_class analytical, gate_g decomposition_attribution, stump_strategy causal_design, decisive generator G14 (attribution conditioned on the clock). Design note round 1 recorded statistical_rigor, analytical_non_defect. The class agrees (analytical, no defect, no surface read). The label differs only in wording (decomposition_attribution against method selection of a conditioning basis). Declared distractors are not named as the surface read carrying the task. The real mismatch is not in Gate G but in determinism: the design note's Determinism section says the method is "forced by the design" and every same-hours variant converges, whereas the judge found the pre-surge baseline and the all-hours baseline both licensed by the text and giving Kestrel.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This matches the card's analyst_test (counting upwind events files the Landfill, dividing by all-hours frequency files the rendering plant) and domain_test (conditional probability by direction and its time-stratified form is the air agency's own analysis).

## Stump power (Gate F)
Strong models would most plausibly fail by taking the raw upwind count (Landfill 210) or the all-hours lift (Kestrel 2.69x). The hour-of-day confound is a real analytical trap. Because the baseline is not pinned, some failures would be a coin flip on the baseline and not a provable error. Margin once the hour-matched baseline is adopted (Ridgeway 42.6 against Kestrel 22.5; 2.6x against 1.3x) is clear and robust to the 0.2 difference.

## Findings, ranked
1. Main call not forced (Gate C and E, underspecified_objective). Prompt.txt or the CP-14 procedure must file the attribution basis, for example the wind at the same clock hours on the season's other days with a usable wind. The pre-surge Jan to Apr baseline (Kestrel +61.7) is a licensed rival not ruled out by any shipped fact.
2. Workbook ask 1 duplicate rule ("a report received twice") is not filed; pin the truncated-prefix rule in complaint_export_fields.txt or CP-14. Minor.
3. Pinning the baseline removes part of the trap, so the stump must be re-argued after the change. Golden figures can stay byte-identical.
4. The design note's Determinism claim (every same-hours variant converges, SF11) does not cover baselines outside the clock-hour family; the fork table needs a row for the pre-surge baseline.

## Next action for the author
Add the comparison basis to the filed definition of "behind the surge" (CP-14 or the prompt) so its literal execution is the hour-matched excess, then re-check the stump on paper, since the filed sentence changes what a solver sees.
