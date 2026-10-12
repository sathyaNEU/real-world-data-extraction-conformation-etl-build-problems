# leak check, task183

**Verdict: REVIEW.** 14 files read, 23 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: failure, section, decisive, quarry, second, forecast, window, in-service, population, forward, states, sutter, hospital, method, outage, history, applied, default, carries, replaced, report, recurrence, behind, hazard, asserted

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: \bthe model\b x1: ...eder, parent device and in-service dates (blank when in service since the model's go-live). **cis_service_accounts_20260930.csv**: one row per activ...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `2025_annual_reliability_report_sec6_ug_cable.pdf`: carries 7 of 7 distinctive words of the committed call: 'Quarry Hill 21 will have the most failures of the cable itself in 2027, so it is the feeder for the 2027 cable program.'
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: carries 6 of 7 distinctive words of the committed call: 'Quarry Hill 21 will have the most failures of the cable itself in 2027, so it is the feeder for the 2027 cable program.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `2025_annual_reliability_report_sec6_ug_cable.pdf`: 6 of 25 stump-paragraph terms appear (failure, section, quarry, sutter, replaced, report); read whether the document names the move
- **REVIEW** `TVE-RS-04_reliability_reporting_standard_rev6.pdf`: 5 of 25 stump-paragraph terms appear (quarry, sutter, method, outage, report); read whether the document names the move
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: 7 of 25 stump-paragraph terms appear (section, quarry, in-service, sutter, outage, replaced); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Which of the eight feeders on our underground network will have the most failures of the cable itself in 2027, counting insulation, splice and termination failures on the sections in service at the end of September 2026 '

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `2025_annual_reliability_report_sec6_ug_cable.pdf`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `TVE-RS-04_reliability_reporting_standard_rev6.pdf`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `feeder_device_list.json`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 8 column names (REVIEW 3)
- **REVIEW** `feeder_device_list.json`: columns a generator names and an organisation does not: device_id, device_type, parent_device_id, device_id, device_type, parent_device_id, device_id, device_type
- **REVIEW** `oms_outage_export_2020-10_2026-09.csv`: columns a generator names and an organisation does not: device_id, device_type
- **REVIEW** `oms_restoration_steps_2020-10_2026-09.csv`: columns a generator names and an organisation does not: device_id, restoring_device_id

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)
