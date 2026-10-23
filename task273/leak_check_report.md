# leak check, task273

**Verdict: REVIEW.** 17 files read, 14 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: driver, exposure, struck, pooled, sample, private, report, architecture, delivery, stratum, shares, records, decisive, recorded, induced, counts, golden, stations, population, method, scaled, driven, family, selection, not-at-fault

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `cfsp_coverage_rule_2026.pdf`: golden figure 1.5 appears: ...sed crashes at a rate per mile driven of at least 1.5 times the rate of private drivers, over 1 Januar...
- **REVIEW** `travel_monitoring_report_2025.pdf`: golden figure 1.7 appears: ...s 1.1% Single-unit trucks 3.5% Combination trucks 1.7%...
- **REVIEW** `travel_monitoring_report_2025.pdf`: golden figure 402 appears: ...cal Urban 1,608.1 2,552.1 Interstate Rural 74.0 3,402.7 Other freeways and expressways Rural 31.0 680.5...
- **REVIEW** `cfsp_coverage_rule_2026.pdf`: carries 10 of 12 distinctive words of the committed call: 'The programme should cover four of the seven uses: taxicabs, ride-hail, parcel delivery and app-based delivery.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `README_pack_contents.txt`: 5 of 25 stump-paragraph terms appear (report, delivery, records, recorded, stations); read whether the document names the move
- **REVIEW** `cfsp_coverage_rule_2026.pdf`: 7 of 25 stump-paragraph terms appear (driver, private, report, delivery, records, recorded); read whether the document names the move
- **REVIEW** `crash_extract_data_dictionary.pdf`: 5 of 25 stump-paragraph terms appear (driver, report, delivery, records, recorded); read whether the document names the move
- **REVIEW** `travel_monitoring_report_2025.pdf`: 3 of 25 stump-paragraph terms appear (report, counts, stations); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 2: five isolated scored readers (sonnet, medium), each on fresh copies of `prompt.txt` and `target/`. Architecture 1's readers are recorded in the design note's Architecture 1 record.

- r273c and r273d on target.zip a0eea6c8 (the rule's section 5 still scheduling a vote, the golden still counting at-fault drivers): each filed airport shuttles and paratransit by the pooled share of the not-at-fault vehicles (1.73 and 1.67; 1.78 and 1.70), parcel delivery the near miss at 1.45 and 1.46. Ask A and Ask B 0 of 14 each: the persons file read row by row, the register's deaths matched on crash, unit, type, age and sex, each crash costed at its most severe row. Q1 none, Q2 none, Q4 none (the 1.5 line read as the threshold), Q6 an analytical choice (induced exposure).
- r273e on 4c8e07aa: the same two (1.74, 1.66), parcel delivery 1.44; asks 0 of 14. Q1 none, Q2 none, Q3 the count-station, weather, work-zone and inventory files read as distractors, Q4 none, Q6 an analytical choice.
- r273f on fdf66198, with the dictionary then saying a later report on a crash numbers its persons on from the earlier ones: the same two (1.78, 1.70), parcel delivery 1.46; it followed that clause to the persons file's later listings and kept every ask figure (14 of 14). The clause was withdrawn.
- r273g on the final cut 73efe129: filed taxicabs, parcel delivery and app-based delivery by taking each use's share of the not-at-fault vehicles within each year, functional system and area, scaled by Table 1's VMT (rung R3a: ride-hail 1.40, paratransit 1.41, the pooled share named as the wrong route); asks 0 of 14 (rows read as they stand, each crash at its most severe row). Q1 none, Q2 none, Q3 the operator register and the legacy-route sheet as help, Q4 none, Q6 an analytical choice (stratifying the exposure by road class).
- `score_reader.py`: every reader's call 0 of 2. Once the golden counted each crash once per use (rule 3.2), every reader's crash counts matched it (critical component 1, which every route shares).
- Verdict on the REVIEW lines: 1.5 in the rule is the coverage line every reader quoted as the threshold; 1.7 and 402 in the travel monitoring report are a vehicle-class share and part of 3,402.7; the rule's table names the seven uses because it licenses them; the vocabulary hits are generic words. No reader read any file as ranking the uses (Q2 and Q4 none for all five).

Gate F held on all five readers. Determinism judge: pass 1 NOT_DETERMINISTIC on the asks only, FIX_NOW; pass 2 DETERMINISTIC, APPROVE (`determinism_check_report.md`, `determinism_check_report_pass2.md`).
