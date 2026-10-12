# determinism-check report, task254, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium, readable paths limited to the brief and the fresh unzip) recomputed every load-bearing figure from the bundle with pandas. The literal trip build (4-minute lot leg, each of the 16 TMC segments at the passenger travel time of the five-minute epoch in which the shuttle enters it, 3-minute leg) gives 238 on-time days at 7:05 and 190 at 7:10 against a bar of 227 (90% of 252). The nearest single-day boundary at 7:05 is 19.75 s from 8:00, so no rounding or <= vs < choice moves the call. No gate failed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Working weekdays, Oct 2025 to Sep 2026 | 252 | 252 (261 weekdays less 9 holidays, hr_holiday_calendars.xlsx) | yes |
| Bar (90%) | 227 | ceil(226.8) = 227 | yes |
| Segment coverage | complete | 17,520 epochs x 16 TMCs, 0 NaN, 0 duplicates | yes |
| On-time days at 7:05 | 238 | 238 | yes |
| On-time days at 7:10 | 190 | 190 | yes |
| Riders | 410 | 370 + 87 - 34 overlap - 13 opt-outs in the 8:00 set | yes |
| Vehicles / empty seats | 15 / 10 | ceil(410/28) = 15; 420 - 410 = 10 | yes |
| Deadhead miles | 10.96 | 0.8 + 2.1 + 8.06 (release 2025.2) | yes |
| Service days 2027 | 252 | 252 | yes |
| Vehicle charge | $953,920.80 | 15 x 252 x (214 + 3.5 x 10.96) | yes |
| Late arrivals 6:50 to 7:20 | 410, 410, 1,230, 5,740, 25,420, 47,560, 66,830 | 410 x (252 - on-time days), same | yes |
| Cost 6:50 to 7:20 | 969,501 / 969,501 / 1,000,661 / 1,172,041 / 1,919,881 / 2,761,201 / 3,493,461 | x.8 unrounded values, round to the golden | yes |
| Rival: departure-epoch sum | wrong path 7:15 | 252/252/252/251/250/241/181 for 6:50 to 7:20; 241 >= 227 so files 7:15 | yes (the wrong path reproduces) |

## Competing answers that survived
- Trip timing (standard 2.4 says only "along the route ... with the fixed legs"): departure-epoch summing gives 7:15, the dynamic build gives 7:05. The readme defines each value as the epoch average of the vehicles, so the only trip a vehicle makes enters each segment in its own epoch. Residual fork: low to moderate (a solver could say the standard did not state segment timing). This is the intended analytical step, not a reading difference the files leave open; optional pin is one clause in 2.4, but it would name the decisive step.
- Deadhead release (cost answers only, not the call): 2026.1 lengths give 10.27 mi and costs $9,128.7 lower at every departure. The deadhead file's "Set up ... October 2025" date and the description mismatch for 121N04637 force release 2025.2. Residual fork: low.
- Opt-outs, population, window, holidays, rounding, exact-boundary arrival: all closed by shipped text or data; no fork.
Net: no fork that changes the call or any graded figure under the shipped text.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | >= 10 | 25 | yes |
| Formats | >= 3 | 5 (csv 14, xlsx 5, docx 2, pdf 2, txt 1) | yes |
| Largest file | >= 25,000 rows | 52,080 rows (trelvane_tmc_export_2026-05.csv) | yes |
| Distractors | >= 2 in metadata.json, none labelled in file names | 2 named: staff_commute_survey_2026.csv, route_40x_southwest_express_timetable.pdf; neither name nor file marks them; unused by the solution, same world; judge found them non-answering | yes |
| Deliverables | 1 to 3 | 2 (xlsx, html); both present under golden/ | yes |
| Multi-dimensional asks | yes | per-departure seven-setting grids, riders/vehicles/seats, chart | yes |
| Units and rounding stated | yes | whole numbers and whole dollars in the prompt | yes |
| Prompt | one paragraph, under 1,000 chars | 850 chars | yes |
| Prompt shape and 25-criteria floor | shape identifiable, >= 25 | shape 04; design note counts about 26 (3 + 14 + 3 + 4 + 2); close to the floor | yes, thin margin |
| Realism | no LLM tells | judge found none; golden-realism run separately | yes |
Licence provenance in metadata.json: constructed, CC BY 4.0, source and date recorded; the judge could not check it (outside its tree).

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and pipeline.json: strategy time_semantics, Gate G method_or_model_selection, stump_class analytical, with the same wrong path (7:15 at 241 days) and the same golden (7:05 at 238, 7:10 at 190). The design note says no shipped artifact ranks the candidates wrongly; the judge found the data honest. Metadata declares the two distractors; the judge named neither as the surface read carrying the task. Match: no mismatch to predict a send-back.

## Stump power (Gate F)
Good. A capable solver summing segment times at the departure epoch (or using the whole route at one epoch) files 7:15; only taking each segment at the epoch the shuttle reaches it gives 7:05. Ask 2 (190 at 7:10) and every cost and late-arrival cell need the same dynamic build, so the difficulty reaches the asks. No too-easy signals named.

## Gate H line
domain: pass | layers: pass | decisive_step: analytical. Layer 1 is probe exports in local time, TMC release changes, payroll IDs vs employee numbers and merged overlapping lists; Layer 2 is a time-dependent path travel-time build against a percentile-of-days standard. The headcount and deadhead-release steps are data-semantics steps and are not decisive. Matches the card's analytical stump_class and the design note's analyst test (the departure-period sum files 7:15; the reflexes file 7:10, 7:00 or 7:15).

## Findings, ranked
1. Low: the trip-timing fork in standard 2.4 (staff_shuttle_service_standard.docx) is unstated by design; this is the decisive step, so a pin would hand over the answer. Leave as is.
2. Low: the deadhead file does not state its release (ridgeline_deadhead_route_brook_st_yard.xlsx); it is resolved by the setup date and the description mismatch, and affects cost cells only. An optional one-line pin would need a rebuild.
3. Minor: the opt-out list runs "to 16 October 2026" and the late requests "to 14 October 2026", both after the 12 October budget note and the 5 October export. Not stump-affecting.
4. Minor: the rubric estimate is about 26 criteria, close to the 25 floor.

## Next action for the author
Proceed to ship; no repair is required and no re-judge is needed.
