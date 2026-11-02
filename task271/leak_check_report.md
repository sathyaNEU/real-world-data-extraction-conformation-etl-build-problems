# leak check, task271

**Verdict: LEAK.** 13 files read, 33 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: survey, architecture, anglers, dropped, reflex, reader, record, readers, candidate, golden, nothing, family, health, hospital, effort, member, screens, estimate, design, selection, decisive, spread, pooled, profile, scored

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `catchable_allocation_policy_2026.pdf`: golden figure 500 appears: ...er for a stocking year when anglers fished it for 500 or more angler-hours per hectare of its surface a...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `catchable_allocation_policy_2026.pdf`: 3 of 25 stump-paragraph terms appear (survey, anglers, estimate); read whether the document names the move
- **REVIEW** `creel_survey_protocol_2026.pdf`: 3 of 25 stump-paragraph terms appear (survey, anglers, record); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `lake_temperature_loggers_2026.csv`: columns a generator names and an organisation does not: temp_c
- **REVIEW** `quillet_creek_drop_tallies_2026.json`: columns a generator names and an organisation does not: water_temp_c, water_temp_c, water_temp_c, water_temp_c, water_temp_c, water_temp_c, water_temp_c, water_temp_c

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `creel_survey_protocol_2026.pdf`: names 14 column(s) of the data files verbatim (Access, Lake, access, boats, clerk, date): confirm it is the organisation's own record and not a note written for the analyst

## 13 task metadata (LEAK 1)
- **LEAK** `metadata.json`: prompt_shape carries a figure from the submission's graded blocks (500)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)
