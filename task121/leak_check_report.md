# leak check, task121

**Verdict: REVIEW.** 14 files read, 41 golden figures and 9 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: pupils, school, secondary, primary, sessions, architecture, primaries, accounts, address, second, member, orders, borough, cross-classified, secondaries, household, identity, published, golden, device, harden, schools, family, decisive, schema

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `ks4_measures_summary_2026.pdf`: golden figure 1.5 appears: ...istinction* 3 Level 1 Distinction 2 Level 1 Merit 1.5 Level 1 Pass 1.25 Unclassified 0 Where two qualif...
- **REVIEW** `trustees_paper6_halwick_progress8_2026.pdf`: golden figure -0.14 appears: ...emy -0.17 -0.39 -0.32 Coldwell Academy -0.05 0.01 -0.14 Mossgate Academy 0.05 -0.14 0.03 Saltmoor Academy...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `brantholme_transfer_file_guide_2026.pdf`: 7 of 25 stump-paragraph terms appear (pupils, school, secondary, sessions, second, borough); read whether the document names the move
- **REVIEW** `larkhollow_attendance_reporting_2025_26.pdf`: 3 of 25 stump-paragraph terms appear (pupils, school, sessions); read whether the document names the move
- **REVIEW** `trustees_paper6_halwick_progress8_2026.pdf`: 8 of 25 stump-paragraph terms appear (pupils, school, secondary, sessions, second, borough); read whether the document names the move

## 6 ranking artifacts (REVIEW 7, INFO 3)
- **REVIEW** `brantholme_ks2_ks4_transfer_2022_2024.csv`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `brantholme_school_funding_2025_26.xlsx`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `brantholme_school_workforce_nov2025.xlsx`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `ks4_performance_tables_brantholme_2022_2024.csv`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `larkhollow_attendance_2025_26.csv`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `larkhollow_in_year_movements_2025_26.csv`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `trustees_paper6_halwick_progress8_2026.pdf`: names 9 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `brantholme_establishments_2026.csv`: names 8 of 9 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `larkhollow_exam_results_summer2025.csv`: names 8 of 9 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `larkhollow_exam_results_summer2026.csv`: names 8 of 9 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Stage 4 scored readers (architecture 5, 2026-10-25)

Two isolated readers (general-purpose, sonnet, medium), each on a fresh copy of the cut pack and `prompt.txt` only,
scored with `score_reader.py task121 <reader.json> --call-key call.largest --call-key walk.own`.

**Reader A: exit 1, Gate F failed.** Call figures 1 of 3 (call.verdict "no" hit; call.largest "own" and walk.own
-0.2 missed), ask figures 20 of 38. It fitted P8 on absence, disadvantage and secondary effects over all 14 schools
and read the walk as Paper 6 states it (own -0.245 largest, remainder nil), then grouped Halwick's pupils by
`ks2_urn` on its first exploration pass, found the seven feeders' pupils near -0.5 wherever they went, added key
stage 2 school effects (own -0.245 to -0.023) and answered "no" with the feeder legacy behind the gap. Q1: no
sentence announces the step; the nearest is Paper 6 3(c), "the same pupils, with the same attendance". Q6: the
verdict is an analytical choice; nothing planted. Annex A 15 of 16 (current academy repaired from the movements log,
the 2025/26 year group read off the UPN's year digits); Annex B 16 cells on the January-census cohort with 38
leavers at nil.

**Reader B: exit 0 on the call.** Call figures 0 of 3: "yes, the own effect, about two thirds of the gap", the walk
on secondaries only (own -0.245, remainder nil); what lies behind it read as a whole-school shortfall across
cohorts, elements and prior-attainment bands. Annex A 16 of 16 by the same two repairs; Annex B the same 16 cells
as reader A.

**Annex B.** Both readers executed the measures summary's cohort sentence (year 11 on the roll at the January 2026
census, 1,514 pupils, 38 who left after the census at nil) and agree with each other in all 16 cells; the golden
took its cohort from the summer 2026 results file (1,476) and so did not execute its own filed sentence. The
cracker shared the golden's cohort and could not see it. The judge thread found the same fork (SEND_BACK).
