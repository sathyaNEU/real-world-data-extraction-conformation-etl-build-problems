# determinism-check report, task245, pass 2, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (fresh unzip at /tmp/determinism-check-task245-pass2r2/target/, blocks inlined, judge system prompt verbatim) executed the prompt and procedure AQ-QP-04 s5.1 to 5.2 literally. The estimand (days in 2027 with a daily mean above 50, every day counting, note where valid-day count is 35 or fewer and whole-year count above 35) is filed; the rebuild method is open but separated by the data (lost days at TBT1, TH3, TBT4 are wind-biased: 103 of 229 lost days against 72 of 866 valid days in the stockyard sector). Every committed answer reproduced from the bundle. Blind fills (scaling by capture, median of others, interpolation) file a wrong set of notes, and every wind-conditioned rebuild puts the three at 41 or more.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Valid-day exceedances TBT1 / TH3 / TBT4 | 22 / 17 / 19 | 22 / 17 / 19 | yes |
| Lost days (3 stations) | 229 | 80+71+78 = 229 | yes |
| Stockyard-wind days, lost / valid | 103 / 72 of 229 / 866 | 103 / 72 | yes |
| Valid-day mean on those days vs others' median | 53.9, 82.1, 63.0 vs 19.9, 22.2, 21.0 | same | yes |
| Whole-year counts, 12 stations | 57,14,51,51,16,14,30,30,24,15,11,2 | all 12 exact | yes |
| Accepted ranges | TBT1 39-61, TH3 45-58, TBT4 44-56, TH5 23-33, TH6 26-34 | variants span 41-60, 45-55, 45-57, 24-32, 27-33, all inside | yes |
| NO2 annual means TH3/TH5/TH6/TH1/TH2/TH4 | 19.0/29.0/26.3/19.4/15.5/23.7 | same; boundary shifts of up to 2 h change nothing at 1 dp | yes |
| Deposition TBT1/2/4/3/5 | 69/61/60/59/46 | 68.8/60.8/59.8/59.3/46.3; exact 227 mm area gives same integers | yes |

## Competing answers that survived
- Valid-day count only, or scaling by capture: wrong set (none noted, or TH5 and TH6 noted); refuted by the wind-biased missingness. Not a surviving fork.
- Residual fork, flagged not a defect: Market Street (TH5) under a ratio-of-means rebuild from Town Hall alone gives 36 (35 with local ratio), from Grangefield alone 40. The data close it: that method over-predicts TH5's observed valid-day exceedances (35 against 24 on matched days) while the linear/additive methods predict about 31. TH6 stays at or under 34 under every sensible variant. A validated rebuild lands on no note at TH5; an unvalidated ratio route could land on a note. The thread judged this a risk, not an open fork. I record it as the single thin margin (30 against the 35 line) worth the author knowing.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, xlsx, pdf, eml, md | yes |
| Large file | 25,000 rows or more | 166,776 rows (council hourly csv) | yes |
| Distractors named, none labelled in file names | 2 or more | metadata.json: asr2027_table_a3_no2_2026.pdf, background_maps_2027_thornmouth_extract.csv; file names do not say distractor | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | 2026 NO2 table and background map count no 2027 PM10 days; thread also found the NOx channel and the plan's 200 mg/m2 action level as weighable and ruled out by shipped facts | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12 stations x count and note, 6 NO2 stations, 5 gauges; days whole, NO2 1 dp, deposition mg/m2 per day whole | yes |
| Prompt shape and 25+ criteria | shape identifiable, 25+ | shape 10 (scorecard); about 12 + 12 + 6 + 5 graded figures plus the call and chart, design note counts well over 25 | yes |
| Reads as real, not LLM generated | yes | thread found no authoring disclosure in README/DATA_DICTIONARY; dates coherent; one minor wrinkle (plan dated May 2027 lists a 7 Jun gauge fitting) resolved by the service log, no effect on the answer | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g `decomposition_attribution`, stump_strategy `population_selection`, gap `population`, official_decoy false, decisive_rule_filed false. Design note: the stump is estimating the lost days of a station whose analysers stop on plume days, from background plus the station's own wind response. These agree in substance (estimation of unobserved, informative-missing days; population = the whole year). The label wording differs (the card's attribution/population-selection against the thread's method selection) but names the same decisive step; not a mismatch of mechanism. The thread did not name either declared distractor as the surface read carrying the task, so the distractors are not too load-bearing.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (domain test: wind-sector conditional rebuild of lost hours near a point source; Layer 1 clocks, re-sent week, logger factor, gauge area; Layer 2 estimation_fit; No decoy and Not semantics/Not rule application lines present). The card carries stump_class analytical, with analyst_test (scaling, 90.4th percentile, interpolation or network-only fill file the wrong set) and domain_test (whole-year count with lost days rebuilt from wind against the station's pollution rose); the thread's reading agrees with both.

## Stump power (Gate F)
Strong. The default routes (valid-day count, scaling by capture, 90.4th percentile, interpolation, network-only fill) each file a wrong set of notes; scaling wrongly notes Market Street and Westholme Avenue and misses the three terminal-affected stations. Second-tier devices (sequential clock conversion, logger factor, gauge area change, void period, re-sent week) carry the asks. TH5 sits nearest the line.

## Findings, ranked
1. Market Street (TH5) margin is thin (30 against 35); an unvalidated ratio-to-one-station rebuild can reach 36 to 40. Closed by back-testing against the data; not an open fork. No change required.
2. Minor: plan dated May 2027 describes a gauge fitted 7 Jun 2027. Service log resolves it; cosmetic.
3. Leak reader REVIEW lines (procedure PDF vocabulary overlap, the s5.2 note rule announcing the outcome type) are the leak reader's matter, not determinism.

## Next action for the author
Proceed to ship (stage 5). Optionally, if a one-line tidy is wanted, date the monitoring plan after the 7 Jun gauge change; this needs no rebuild for determinism.
