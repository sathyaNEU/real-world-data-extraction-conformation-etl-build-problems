# determinism-check report, task474, 2026-10-20 (pass 2, architecture 6 re-judge; overwrites pass 1 as instructed)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (annualisation basis pinned by the data's structure), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope note: the isolated thread (sonnet, medium, one pass) judged the bundle unzipped at /tmp/determinism-check-task474-g/target/ (zip sha prefix 40335d5414269e1c). The coordinator then rebuilt target.zip (now sha prefix 2025e51b8d57c653) with one text change, rule 3.1 reading "under the motor carrier of its latest registration in force on that day". I confirmed the PDF in the current zip carries that sentence and that the file list is unchanged (14 files). The graded figures are stated byte-unchanged by the coordinator; the thread did not see this wording, but it is the pin the thread itself named as optional, and it closes the minor fork recorded below in the direction of the golden.

## Why
Every committed answer reproduced from the shipped files alone: the designation (L03, L05, L14), the four quarter-end fleet counts and the eight per-carrier counts. The pass-1 registry fork is closed by data_notes.txt ("registered_to is the last day in force"); treating it as exclusive gives the same totals anyway. The designation turns on carrying the combination trucks of the three terminal access roads to the year by the terminal's gate record, which the data forces (count-day CU totals are 0.94 to 0.97 of the terminal's same-day trucks in plus out) but no shipped text states. That is the one place the literal text is silent; the thread rated it analytical (the data selects the method), and rule 2.2 files the estimand (vehicle-miles in the twelve months), so the annualisation is estimation, not a withheld rule.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| L03 NOx per mile (t) | >= 5.00 | 6.18 | yes |
| L05 | >= 5.00 | 5.46 | yes |
| L14 | >= 5.00 | 5.40 | yes |
| L09 / L01 / L06 (nearest below the line) | < 5.00 | 4.56 / 4.55 / 4.45 | yes |
| Designated count | 3 of 14 | 3 of 14 | yes |
| Trucks 31 Dec 2025 / 2009 or older | 2,290 / 379 | 2,290 / 379 | yes |
| 31 Mar 2026 | 2,333 / 385 | 2,333 / 385 | yes |
| 30 Jun 2026 | 2,369 / 392 | 2,369 / 392 | yes |
| 30 Sep 2026 | 2,423 / 405 | 2,423 / 405 | yes |
| Carriers 30 Sep (Atlantic, Bay, Coastal, Harborline, Northpoint, Rivera, Seaboard, Tri-County) | 229/39, 259/49, 304/42, 413/74, 275/48, 237/45, 323/54, 383/54 | identical, all eight | yes |
Sources: dot_short_counts_fy2026.csv, county_traffic_counts_2025_2026.xlsx, terminal_access_counts_2026.csv, ccs_hourly_volumes_oct2025_sep2026.csv, count_station_register_2026.xlsx, onroad_nox_emission_rates_2026.csv, terminal_daily_gate_report_fy2026.csv, drayage_truck_registry_2026.csv (registered_from, registered_to, vin, engine_family), heavy_duty_engine_certifications.xlsx. Sensitivities that keep the set: trucks_out for trucks_in, pooled-sum factors, weekday-only factors.

## Competing answers that survived
- Gate ratio taken against the same-month, same-weekday gate mean instead of the count day gives L01, L03, L05, L14. The thread judged it unlicensed (the count-day gate volume is the quantity the CU count tracks, ratio 0.97). Weak fork, the one place a reader could land on a different set.
- Latest registration overall (not in force on the day) gives 2,600 / 438 on 30 Sep. Now closed by the rule 3.1 wording added after the thread returned.
- No O/I VIN read gives 2,478 / 412; the 55 pairs match exactly on carrier-change date and engine family, and the submission files the read.
- Unfiled element: that terminal-road combination trucks follow the gate record. Not a fork on the answer (the alternatives are wrong or unsupported) but a strict rule-based reader could call it a hidden rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000 rows or more | ccs hourly, 347,376 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | no2_monitor_hourly_2026.csv, truck_complaints_311_2025_2026.csv; names carry no label | yes |
| Distractors unused yet weighable, none answering a graded quantity | yes | ambient NO2 and 311 complaints by street, ruled out by rule 2.2 (NOx emitted by traffic) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | quarter x age cut, carrier x age cut, link set with chart; "whole trucks", 5.00 line | yes |
| Prompt shape and rubric 25 or more | yes | shape 07 grid per design note (14 link verdicts, 8 quarter-end cells, 16 carrier cells, count, chart); rubric file not in the folder, not recounted | yes, per note |
| LLM-read and golden realism | none | thread found no authoring language; mixed date formats, header blocks, typo VINs present | yes |
| Prompt | one paragraph, under 1,000 characters | 702 characters | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and note: analytical, estimation_fit; stump sentence is the class-factor expansion on every link (L01, L03, L05, L06) against the gate-record expansion on the three access roads (L03, L05, L14). These agree. The declared distractors (NO2 monitors, 311 complaints) were not named as the surface read carrying the task, so they are not too load-bearing. Gate G: no shipped artifact ranks the links wrongly; the wrong set only arises from the analyst's own expansion.

## Gate H line
Thread: domain pass, layers pass, decisive_step analytical. The note's Three rules agree (domain: emissions inventory expansion; Layer 1: three count programmes, UTC offsets, outage days, VIN typos; Layer 2: choose the annualisation basis per vehicle population). Caveat recorded by both: the terminal treatment is an inference from the data (0.97 tie), not a filed sentence.

## Stump power (Gate F)
The thread expects a strong model to miss the designation (factor expansion on every class is the textbook step, giving L01, L03, L05, L06, wrong on three links) and plausibly one fleet cell (O/I merge, in-force latest registration, engine year from the certification list not the registry column). Margins are about 0.4 t either side of the line. This is the standard-method-versus-data-structure kind of call; whether the blind readers find the CU-to-gate check is for the scored readers to weigh, and the thread flagged that the discovery step is real and unprompted.

## Findings, ranked
1. Unfiled terminal-follows-gate treatment, the sole text silence (risk: a strict reader calls it a hidden rule; judged analytical).
2. Same-month gate-mean ratio reading gives L01, L03, L05, L14 (weak, judged unlicensed).
3. Latest-registration wording fork, closed after the thread by the rule 3.1 pin.
4. Optional, not required: data_notes.txt could say the gate report counts every truck through the terminal gates; weigh against stump cost, likely decline.

## Next action for the author
Ship as is. The post-thread rule 3.1 wording (sha 2025e51b8d57c653 zip) was not seen by the thread; if any further text in target.zip changes, no re-judge is needed unless a graded figure moves.
