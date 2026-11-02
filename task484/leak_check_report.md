# leak check, task484

**Verdict: REVIEW.** 13 files read, 51 golden figures and 34 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, propane, survey, appliance, counters, heating, golden, record, season, register, factor, comparison, detector, reflex, window, factors, decisive, station, exports, burned, degree, vehicle, sentence, records, member

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `traffic_estimate_terms_2025.pdf`: golden figure 3.5 appears: ...les. Heavy goods vehicles are goods vehicles over 3.5 tonnes gross vehicle weight, rigid or articulated...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `network_operations_log_2025.docx`: 3 of 25 stump-paragraph terms appear (survey, counters, detector); read whether the document names the move
- **REVIEW** `traffic_estimate_terms_2025.pdf`: 4 of 25 stump-paragraph terms appear (counters, record, register, vehicle); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "For the noise model's other inputs, traffic_network_2025.xlsx should hold each permanent counter's average daily heavy goods vehicles in 2025 and the vehicles the detectors recorded in 2025 on each approach to the Wester"

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `count_points_2025.xlsx`: names 31 of 34 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `expansion_factor_review_2025.xlsx`: names 13 of 34 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `network_operations_log_2025.docx`: names 15 of 34 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `streetworks_permits_2025.csv`: names 24 of 34 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `utc_asset_register_2025.xlsx`: names 16 of 34 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `atc_sites_2025.csv`: names 13 of 34 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (Leak reader, architecture 4 round 1 (2026-11-02, isolated, Sonnet at medium effort, on target.zip ec5ec5c1))

1. Decisive step: none stated; the nearest is the terms' section 4 definition of a section's annual traffic (every motor vehicle passing along it, both directions, on all the days of the calendar year), a definition, not a method.
2. Nothing ranks the sections on annual traffic (manual counts are one-day 07:00 to 19:00 hourly counts; the counter file is daily totals).
3. Nothing exists only to help the analyst; the closest is the expansion factor review, scoped to the permanent counters only ("the review does not test count point sections"), a method-validation record that fixes no count-point figure.
4. Nothing reads as the answer (no section carries an annual figure).
5. Terms sections 2 and 4 and the noise-mapping scope's section 3 read literally: each counted section's motor vehicles, both directions, over every day of 2025, for the sections counted in 2025; no sentence says how to estimate it from a one-day count.
6. An analytical choice: estimating annual traffic from the 12-hour counts; nothing states which expansion source to use.
Sweep flags: the terms and the operations log are harmless (definitions and dated operational entries); the count-point register and the factor review give no section traffic; the UTC asset register lists detectors by junction and approach with inconsistent naming and maps none to a counted section.
Realism: none generated; minor: every counter shows the same 98 weekdays tested in the factor review.
