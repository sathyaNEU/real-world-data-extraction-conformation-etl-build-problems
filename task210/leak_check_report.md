# leak check, task210

**Verdict: REVIEW.** 12 files read, 28 golden figures and 14 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, delivered, running, decisive, control, gallowfen, permitted, dry-day, condition, capacity, levels, volume, cycles, hagworth, delivers, telemetry, rising, screen, sentence, reflex, alarms, meters, company, inflow, golden

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `procedures/WW-ENV-PR-014_storm_overflow_EDM_reporting.pdf`: carries 9 of 13 distinctive words of the committed call: 'Self-report the Gallowfen PS storm overflow (permit EPRWW4412BK, condition 2.3.1): it discharged in 2026 while its stati'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `procedures/WW-ENV-PR-014_storm_overflow_EDM_reporting.pdf`: 4 of 25 stump-paragraph terms appear (register, dry-day, condition, company); read whether the document names the move

## 6 ranking artifacts (INFO 2)
- **INFO** `planning/storm_overflow_improvement_plan_2025-2030.xlsx`: names 6 of 14 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `registers/wastewater_discharge_consents_2026.csv`: names 14 of 14 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `procedures/WW-ENV-PR-014_storm_overflow_EDM_reporting.pdf`: names 4 column(s) of the data files verbatim (Investigation, Permit, issued, station): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 7cec12239723a24eec754e009cbd2802bbb19d6fcfbcb9f7980e8be34050b0f9). Sweep 4's line was kept out of the brief and ruled in the main thread. Verdict: no leak; the decisive step is read as an analytical reconstruction (each station's pass-forward flow during each discharge); the realism tells below go to the generator.

# Leak read, task210 (no solving)

1. Decisive step stated: none. Closest is the procedure's WW-ENV-PR-014 s7: "Where a storm overflow has discharged in breach of a condition of its permit, the Wastewater Environmental Compliance Manager self-reports the breach ... A self-report names one storm overflow and its permit." and the consents register condition_text "The discharge from the storm overflow shall only occur when the pumping station is passing forward to the rising main a flow of not less than 35 litres per second." (same wording for all 14 permits). These restate the prompt's question; they do not say how to establish pass-forward flow (only 3 stations have a flow meter in flow/rising_main_flow_meters_2026.csv; the other 11 are not metered in the pack).
2. Ranking or scoring file: none.
3. File that exists only to help the analyst: none evident. Every file reads as an operational record. Distractor-like: groundwater OBH daily, improvement plan, work orders.
4. Figure or name reading as the answer: none. Closest is a work-order row "WO4141453,SPS0452,Sedgefleet SPS,2026-04-28,Flow meter verification,Meter verified within tolerance" (and the same for SPS0428, SPS0437); that is context on meter trust, not an answer. The assets workbook "Flow meters" sheet lists only SPS0428, SPS0437 and SPS0452, which flags where measured pass-forward exists, not which overflow breached.
5. Filed sentences that fix computation/population:
 - PR-014 s3: "Spills are counted for each storm overflow by the 12/24 method. Counting begins at the start of the first discharge. Any discharge in the first 12 hours counts as one spill. Any discharge in each following 24-hour block counts as one further spill, block by block ... When a full 24-hour block passes with no discharge, the next discharge begins a new count." Fixes spill count rule.
 - s4: "total duration of discharge ... from the start of each discharge to its end, any period of discharge counted once." Fixes hours (union of overlapping periods).
 - s5: "A day for which no monitoring data reached the company counts as a day with no monitoring." Fixes monitored percentage.
 - s2: "A discharge is reported in the year in which it starts." Fixes year window (UK local time).
 - Consents register condition_text (2.3.1): breach = overflow discharging while the station's forward flow is below the permit's litres per second. Fixes the comparison and the permit's flow per overflow (pass_forward_ls column).
 These are literal, closed rules for the return lines (rule application). Nothing in the pack states how to derive pass-forward flow at unmetered stations or how to line up UTC telemetry/flow with local-time EDM logs.
6. What decides the main answer: from the files alone it looks like an analytical reconstruction of station pass-forward flow during each discharge (telemetry pump events/levels, three flow meters, pump duty flows with mixed l/s and m3/h units in marsh_wolds_wastewater_assets.xlsx "Pumps"), compared to the permit flow. No sentence announces the decisive step. The unit mix and UTC/local differences are visible as mess; the counting rules are stated rules. No sentence calls anything planted.

## Flagged items
a. harmless, because the PDF names no overflow, station, permit or figure to self-report; s7 is generic ("A self-report names one storm overflow and its permit") and carries no flows other than the 12/24, 0.25 mm and 12 h/24 h rules that govern counting.
b. harmless, because it reads as the organisation's own procedure (owner, revision 4, issue 03/11/2025, next review 11/2027, responsibilities table, revision history with named approvers). It uses concepts the data shares (monitor operational time, dry day) but never names a column, table or file.
c. harmless, because the improvement plan (xlsx "Schemes visible": permit, overflow, scheme, driver, target spills, delivery, status) ranks nothing and scores nothing on pass-forward; the consents CSV lists 14 permits each with identical condition wording and only the pass_forward_ls figure differing, with no spill or flow data. Note only: the plan lists 6 of 14 overflows with "Driver" values, which is incidental.

## Realism
Minor tells only, none disqualifying:
- flow/rising_main_flow_meters_2026.csv: quality column is "G" on all 105,120 rows (too uniform for a real meter log, though plausible if only good data is exported). Check whether this is intended.
- operations/sps_work_orders_2026.csv: outcomes are a small set of templated strings (e.g. "Level high on arrival, duty pump running, standby available"), repeated verbatim; mild uniformity.
- PDF: 2 pages, Author "Harriet Kirk", no Creator/Producer, 5.6 KB, plain; letterhead, document control block, revision history, prepared/approved sign-off and "Uncontrolled when printed" footer are all present and appropriate for a procedure. Empty Creator/Producer reads slightly scrubbed but not machine-made. Length fits a short procedure.
- Different systems do read as different systems (telemetry in UTC with ISO times, EDM logs dd/mm/yyyy local, asset register xlsx authored "Maurice Russell", planning xlsx "Wastewater Planning", mixed pump duty units).
- alarm table has 427 "OVERFLOW OPERATING" rows vs 426 rows in edm_discharge_log; plausible system difference.
