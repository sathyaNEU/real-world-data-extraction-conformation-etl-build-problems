# leak check, task170

**Verdict: REVIEW.** 15 files read, 6 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: driver, starts, report, asserted, conventions, probability, window, register, start-up, first-year, practice, recorder, operator, forward, rollout, category, counted, earlier, planned, reports, diagrams, decisive, default, family, roster

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `etcs_rollout_plan_2024-2027.pdf`: golden figure 461 appears: ...7 on the dates in Table 1. Their units, the Class 461 fleet, are fitted in the Phase 4 fitment programm...
- **REVIEW** `fleet_etcs_acceptance_note.pdf`: golden figure 461 appears: ...Class 461 ETCS Fitment: Acceptance for Service Page 1 Class...
- **REVIEW** `phase4_safety_case_conventions.pdf`: golden figure 250 appears: ...xpected number of errors, reported to the nearest 250. 3. Drivers and turns A driver is counted at the...
- **REVIEW** `phase4_safety_case_conventions.pdf`: carries 18 of 19 distinctive words of the committed call: 'Plan the Phase 4 safety case and its debriefing for about 1,250 train data entry errors recorded against the six Phase 4'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `etcs_rollout_plan_2024-2027.pdf`: 3 of 25 stump-paragraph terms appear (driver, rollout, diagrams); read whether the document names the move
- **REVIEW** `phase4_safety_case_conventions.pdf`: 8 of 25 stump-paragraph terms appear (driver, report, conventions, rollout, category, counted); read whether the document names the move
- **REVIEW** `safety_desk_reporting_guidance.pdf`: 6 of 25 stump-paragraph terms appear (driver, report, register, recorder, category, reports); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'The Phase 4 safety case carries that forecast, so put it in phase4_data_entry_forecast.xlsx with how many drivers it covers and their ETCS start-ups over those twelve months; also give me, for each Phase 4 depot, how man'

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `etcs_rollout_plan_2024-2027.pdf`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `punctuality_by_depot_2024-2026.xlsx`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `staff_number_crosswalk.csv`: names 3 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `etcs_fitment_works_records.xlsx`: 89 ISO dates after 2026-11-09, e.g. 2026-11-12, 2026-11-15, 2026-11-16, 2026-11-25, 2026-11-29
- **REVIEW** `fleet_allocation_2027.csv`: 51 ISO dates after 2026-11-09, e.g. 2026-12-13, 2027-01-07, 2027-01-16, 2027-01-26, 2027-01-29

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Read 1 (2026-11-01, Sonnet at medium, fresh copy of prompt.txt and target.zip 60c3b11b, nothing else readable)

1. Decisive step: none. No sentence names it; the conventions define the count and the exposure and say nothing about the error rate per start or how it changes.
2. Ranking or scoring file: none. Nothing computes the forecast; the punctuality workbook holds no errors, the register lists raw reports, the works records give per-vehicle dates.
3. Helper files: none of the dictionary, readme, manifest or how-to-read kind. The conventions, the reporting guidance, the acceptance note and the rollout plan read as the operator's own governing and procedural documents; the crosswalk and renumbering register as key-bridging tables.
4. Figure or name reading as the answer: none.
5. Filed sentences fixing the computation: the conventions' count sentence (population, window, outcome, linked and withdrawn reports), their rounding sentence (the expected number, to the nearest 250), their turns sentence (each driver's average monthly cab activations on worked, latest-issue duties, one Start of Mission each), the acceptance note's pin and the rollout plan's go-live table. Together they fix population, window, unit and de-duplication and leave the error rate per start and its shape open.
6. What decides: an analytical choice (how the Phase 1 to 3 error rate per start is carried to the Phase 4 exposure); the cleaning is Layer 1, the exposure rule and the fleet ask are rule application on the asks, nothing looks planted.

REVIEW rulings: the rollout plan's and the acceptance note's figure (the class number) harmless; the conventions' figure and call vocabulary harmless (the governing estimand document, no rate, method or forecast); the punctuality workbook harmless (PPM by depot, no errors, no ranking); the works records' and the allocation's later dates harmless (planned acceptance dates and a scheduled allocation date).

Realism tells reported and handled in the generator (data only, every graded figure frozen, `figures.json` unchanged): one shared allocation date and alphabetical ordering (dates drawn per unit from the timetable changes, rows in fleet order); `Trains Planned` jumping month to month (now timetable-driven: a daily rate per depot moved at each December and May change, times the month's days less engineering possessions); a fleet-wide Start of Mission reference sequence (now each unit's recorder numbering its own starts). Kept as real: vehicle numbers 51nnn and 52nnn by unit, a renumbering of plus 100 on a sub-class change, sequential register report numbers by year, a roster in depot and staff number order, the whole fleet in the fitment programme, four-weekly Phase 4 go-lives on possession weekends.

The stage 4 judge (DETERMINISTIC, APPROVE) found two supplementary-ask readings, closed in the same pass: ask C's depot attribution, now asked as what the safety desk recorded against each depot (SF16), and ask A's unit source, now filed in the acceptance note as a unit's two driving vehicles in its formation (SF17).

### Read 2 (2026-11-01, Sonnet at medium, fresh copy of prompt.txt and target.zip 0d6e2973 after the stage 4 fixes)

1 none (the conventions fix what is counted and the exposure basis, never how the rate is got); 2 none; 3 none of the describing kind (four governing or context PDFs and two key-mapping tables, ordinary records); 4 none; 5 the conventions' count, roster and turns sentences, the acceptance pin and the guidance's category and linking sentences, which fix population, window, outcome, exposure and de-duplication; 6 an analytical choice (the reader's own guess at the route was the rate per start by months since go-live, the default path). Ask A: one reading (the allocation's units, both driving vehicles by go-live, the formation list settling a unit's vehicles); the allocation dates are all before the depots' go-lives (asserted SF17), so they never decide. Ask C: one reading at the register's depot, the reader asking for a filed sentence for transferred drivers, now in the guidance (each report logged with the depot the driver worked from that day, SF16). Realism: the rollout plan's inline revision note rewritten as a revision history line; the renumbering of plus 100 per sub-class change and the 51nnn and 52nnn vehicle numbers kept as rail practice.

### Read 3 (2026-11-01, Sonnet at medium, fresh copy of prompt.txt and the final cut, target.zip 21761154)

1 none (the conventions' sections 2 and 3 fix what is counted and the exposure, never a rate, a curve or the drivers' practice); 2 none; 3 no readme, dictionary or manifest, the four PDFs read as organisational documents and the two CSVs as key maps; 4 none; 5 the conventions' count, roster and turns sentences, the go-live table, the acceptance pin and the guidance's categories and linking (population, window, outcome, exposure, de-duplication); 6 an analytical choice, the reader's own guess at the route being a rate falling over a depot's first months (the default path). Ask A: one reading, the formation list settling a unit's vehicles; the inclusive or exclusive reading of "by go-live" converges (no vehicle is dated on a go-live day, asserted SF18). Ask C: one reading at the register's depot (the prompt's "recorded against it" and the guidance's "the depot the driver worked from that day"); the guidance's linking and withdrawal sentences are general to every category; the local or UTC reading of the window converges (no report within three hours of either edge, asserted SF19). Realism: short one-page governing documents and a named author on the register kept; nothing reported reads as a plant.
