# determinism-check report, task210, pass 3, 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pack judged: target.zip sha256 ce1842d66373e7efafe941e03367d49fb310e43f45b7b5a962c92170f723a0da, fresh unzip at /tmp/determinism-check-task210-145501/target/. One thread (sonnet, medium), no retry. Verdict file: /tmp/determinism-check-task210-145501/verdict.md; derivation: /tmp/determinism-check-task210-145501/derivation.md.

## Order and the one re-judge
The graded blocks sat in their own file (graded_blocks.md), not in the brief. The thread wrote derivation.md (main call, all 14 return lines, all 168 chart cells, every reading) before opening graded_blocks.md, and states in verdict.md that it kept this order. Its derivation matched the submission on the main call and on every return-line figure it could compare. The order was kept, so this pass is the architecture's one valid re-judge after the pass-2 FIX_NOW.

## Why
Permit condition 2.3.1 is a measured-flow test ("is passing forward ... not less than N l/s"). The shipped wet-well levels, pump events, register geometry and three rising-main meters force one measurement: delivered rate = drawdown rate plus inflow, validated on the three metered stations (cycles 117.8, 83.7, 66.7 against meters 116-118, 83-85, 66-68). It flags Gallowfen alone (47.9 against 72). Spill counts, hours and monitored percentages follow from procedure sections 3 to 5 and reproduced for all 14 overflows.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gallowfen permit / delivered | 72 / 48 l/s | 72 / 47.9 (telemetry sqlite + register wet well + consents csv) | yes |
| Gallowfen rated duty | 85.3 l/s | 85.3 (register, 307.1 m3/h) | yes |
| Closest other station | Sallowholme 57 against 50 | 56.9 against 50 | yes |
| 14 pass-forward flows, Yes/No | per submission | all 14 whole-l/s values and flags identical | yes |
| 12/24 spills (14) | 15,12,30,57,15,13,11,14,13,17,9,20,9,11 | same | yes |
| Hours (14) | 28.9 ... 12.3, 20.9 | same (union of monitors) | yes |
| Monitored % (14) | 100.0 ... 99.8 | same (daily max over 8,760 h) | yes |
| Monitor serial mapping (14 serials) | via OVERFLOW OPERATING alarms | every one of 499 log rows matches within 3 min | yes |
| Monthly chart cells | not listed in submission | thread's 168 cells, see below | yes against golden svg |

## Chart cells against the golden svg
The submission does not list the cells, so the thread could not compare. I read the golden svg's 120 cell labels (the nonzero cells, written as comments, in row order alphabetical by overflow then January to December). The thread's derivation.md, parsed into 14 rows by 12 months, gives 120 nonzero cells. The sorted label sets are identical and the in-order sequence is identical to the svg. The 48 zero cells are unlabelled in the svg by design. The chart is confirmed.

## Competing answers that survived
Main call: none. Reading 1 (rated duty) files "none"; reading 2 (drawdown over on-time) files three overflows (median), or two (night-only, 90th percentile), which the one-overflow rule of procedure section 7 excludes, and is contradicted by the meters (103/76/62 against 118/84/67); reading 3 is the golden. Reading 1 is the designed default path: no shipped sentence forbids the nameplate, it is closed by the permit's measured "is passing forward", the meters and the 56 per cent running ratio. The thread rates that closure weak. See Stump power.

Asks:
- **Reading 5 (any part against start-only):** closed by section 3, "A block contains discharge when any part of a discharge falls within it".
- **Reading 7 (UTC against local):** moves no graded figure.
- **Reading 8 (rounding lines):** nothing within a minute (closest: Cressfleet hours 24.132, 1.1 min from 24.15; about 20 cells at 1.13 min).
- **Reading 6 (daily maximum against average), the softest fork:**
  - It is open on a supplementary ask only. It moves the monitored-percentage column (ask A3) and nothing else: no main-call figure, spill count, hours figure or chart cell. The 11 replaced-monitor overflows differ at one decimal place (Scarrow Leas 100.0/99.9, Cressfleet 97.4/97.3, Sallowholme 99.8/99.7, Northwade 98.5/98.4, Brackenings 99.4/99.3, Thornmarsh 98.8/98.6, Kettlewade 99.9/99.8, Saltwade 100.0/99.9, Reedhaven 99.4/99.3, Sedgefleet 99.7/99.5, Swathe Drove 99.8/99.7). The 3 never-replaced overflows are unaffected. That is 11 of the 14 A3 cells (the design note's SF13 counts the same eleven overflows).
  - Section 5 does not say how overlapping monitors combine. It does define the quantity as "the hours in the reporting year during which its discharges were being monitored", which a changeover day with one monitor at 24 h answers as 24 monitored hours; a per-day mean across monitors measures something else (18.5 h on 3 March at Scarrow Leas). The words close it for a careful reader, but no sentence names the combination. I record it as a residual, ask-level, mostly closed fork, not an open one on the main call.
  - Nothing in the procedure states an ask device in plain words. Section 5 files the estimand (hours monitored over the year's hours, a day with no data counts as no monitoring), not the monitor-replacement device, the retired-serial mapping or the handover-week duplication. The design note's SF13 closure quotes that same section 5 sentence and adds the "monitored, not half monitored" reasoning in the note only. No closure was found that spells out the device, so the pass-1 finding does not recur here.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, sqlite) | yes |
| Large file | 25,000 rows or large db | pump_event 324,394 rows; radar rainfall 175,201 lines; meter csv 105,121 lines | yes |
| Distractors | 2 or more named, no file name labels one | 4 in metadata.json (rainfall, groundwater, improvement plan, work orders); file names carry no label | yes |
| Distractor behaviour | unused, weighs, ruled out by a shipped fact | The dry-day screen (rainfall + groundwater) reaches Hagworth Wold arithmetically; section 7 ties a breach to the permit's pass-forward condition and Hagworth delivers 36 against 31 | yes |
| Deliverables | 1 to 3, all in golden, no family required | 3 (docx, csv, svg), all present in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 14-overflow return lines x 6 columns plus a 14 x 12 chart; whole l/s, one decimal place stated in the prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 10 (scorecard); about 98 ask figures plus the call; prompt 940 characters, no em dash | yes |
| Reads as real work product | no LLM tells | the thread saw no authoring disclosure; the docx is a dated letter to the Environment Agency with a numbered discharge table; return csv carries the permit reference, station code and overflow name | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_strategy binding_constraint (Gate G), layer2_family field_method, stump_class analytical, no decoy, no certified replay. The labels differ in vocabulary but describe the same thing: estimate the delivered rate from the unit's own storage cycles instead of reading the rating. No mismatch. The thread names the rated duty as the surface read; that is the designed default path (the register's true datasheet figure), not the declared distractor, and it classes the dependency as "no". The declared distractors (rainfall, groundwater, improvement plan, work orders) are not named as the surface read carrying the task; the dry-day screen to Hagworth is the secondary wrong route. Not a finding.

Gate G line: PASS, no mismatch with the card (binding_constraint / field_method); surface read is the designed default path, not a declared distractor; sole_data_defect no.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card domain_test and the design note's Three rules agree (the deciding quantity is the delivered pump rate from wet-well fill and draw between control levels; it fails the swap test; Layer 1 is UTC against local, duplicates, units, mAOD levels, monitor outages; Layer 2 is the delivered-rate measurement). No mismatch. The note's `No decoy:`, `Not semantics:` and `Not rule application:` lines are present and each is substantive.

Gate H line: domain pass, layers pass, decisive_step analytical; matches the card and the design note.

## Stump power (Gate F)
The thread rates it moderate to good. The call is landable. It classes the decisive step analytical and reached the golden itself in its first derivation, because the permit's own words ("is passing forward") make the measured flow the quantity and the three meters let a solver validate it. The method is the field's standard wet-well pump test, a textbook route a strong solver takes (`stumping` 1.3). Note too that the meters match the nameplate at all three metered stations, so they validate the cycle estimator, not the rated-duty route. A response that reads the rated duty files "none"; draw-only files two or three overflows. The main thread should weigh this against the design note's ladder: pair ceiling 55.4 (cracker 75.3 on the call, mirror 35.6 off it), mirror leakage 42.9 per cent, and the ask side carrying 55 per cent of the weight (the monitor-replacement mapping, the handover-week union, the 12/24 count). The ask device is hard for a response that lands the call: the design note's cracker keeps 3 of 14 on each of the four device asks. I record the landable call as a finding for the main thread's ladder check, not as a determinism defect.

## Findings, ranked
1. Landable main call. The thread derived Gallowfen cold and cleanly; the stump rests on the rated-duty route being the easy one, with no shipped sentence forbidding the nameplate. Weigh against the ladder and the ask weight.
2. Reading 6 (daily maximum against mean): ask-level only, 11 of 14 A3 cells at one decimal place, closed by section 5's estimand wording but not by a combination rule. No device is spelled out. Optional to leave.
3. Sensitivity of three chart cells to monitor-overlap handling (Brackenings March 8.409 to 8.3 if the new monitor alone is preferred; Kettlewade March 3.078 to 3.0; Cressfleet September 2.969 to 2.9). Closed by "any period of discharge counted once" in section 4.
4. About 21 short alarms (under 4.5 minutes, mostly Hagworth) in the alarm table are absent from the EDM log; the return is built from the log, which section 3 to 5 cover. Not a fork.
5. Closest rounding margins: Cressfleet hours 24.132 (1.1 min from the line) and about 20 chart cells at 1.13 min. Nothing within a minute.

## Next action for the author
Ship this pack as judged (APPROVE, no repair). If a change is made later it needs its own judge; there is no further re-judge on this architecture.
