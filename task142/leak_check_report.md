# leak check, task142

**Verdict: REVIEW.** 20 files read, 34 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: admissions, spread, history, percentile, stream, capacity, window, alliance, pathway, decisive, course, inside, poisson, episodes, margin, northgate, counted, forecasting, unbooked, family, schedule, clause, expected, allocation, independent

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `bellbird_agreement_schedule2_2027q1_block.pdf`: carries 13 of 14 distinctive words of the committed call: "Book Northgate 300 visits, Riverbend 250, Westmere 225 and Kingsdale 75 from Bellbird's January to March 2027 block, and"
- **REVIEW** `bellbird_service_report_2025-26.pdf`: carries 10 of 14 distinctive words of the committed call: "Book Northgate 300 visits, Riverbend 250, Westmere 225 and Kingsdale 75 from Bellbird's January to March 2027 block, and"
- **REVIEW** `bji_at_home_pathway_northgate_westmere_2026.docx`: carries 9 of 14 distinctive words of the committed call: "Book Northgate 300 visits, Riverbend 250, Westmere 225 and Kingsdale 75 from Bellbird's January to March 2027 block, and"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `bellbird_agreement_schedule2_2027q1_block.pdf`: 8 of 25 stump-paragraph terms appear (percentile, capacity, alliance, inside, northgate, schedule); read whether the document names the move
- **REVIEW** `bellbird_agreement_schedules3-4_fees_and_service_levels.pdf`: 4 of 25 stump-paragraph terms appear (stream, alliance, schedule, clause); read whether the document names the move
- **REVIEW** `bji_at_home_pathway_northgate_westmere_2026.docx`: 7 of 25 stump-paragraph terms appear (admissions, stream, alliance, pathway, course, northgate); read whether the document names the move
- **REVIEW** `hith_program_streams_and_visit_schedule_2025-07.pdf`: 6 of 25 stump-paragraph terms appear (admissions, stream, alliance, course, episodes, schedule); read whether the document names the move

## 6 ranking artifacts (REVIEW 7, INFO 2)
- **REVIEW** `bellbird_agreement_schedule2_2027q1_block.pdf`: names 4 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `bellbird_intake_register_2026.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `bellbird_service_report_2025-26.pdf`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `data_dictionary.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `hith_inhouse_capacity_return_2027q1.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `hith_operating_plans_2026-27_rev_oct2026.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `hith_patient_experience_survey_2025-26.xlsx`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `alliance_member_campuses.csv`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `bellbird_client_accounts.csv`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `alliance_finance_calendar_2026-27.csv`: 473 ISO dates after 2026-11-03, e.g. 2026-11-04, 2026-11-05, 2026-11-06, 2026-11-07, 2026-11-08
- **REVIEW** `export_manifest.csv`: 5 ISO dates after 2026-11-03, e.g. 2027-01-01, 2027-03-31, 2027-06-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Q1 to Q4: none (Schedule 2 clause 2.4 files the estimand, the 90th percentile of the quarter's visits taken together; 2.5 gives the plan's mean only; no file ranks the members or states a percentile or booking; the stream crosswalk and the at-home pathway document have real reasons to exist; the 850 block and the booking order are context and rules). Q5: clauses 2.3, 2.6 and 2.7; no spread filed, so no literal figure (the open method by design); the allocation is executable once the percentiles are known. Q6: analytical (the spread of the quarter's total visits, with the new H04 stream at Northgate and Westmere drawn from the members already running it); the reader did not name the stays-as-home-days structure. REVIEW lines: all harmless (member names and dates, generic domain words, the booking order as a rule, forward calendar and coverage dates). Realism: plausible throughout; the H04 plan rows' October ramp then steady level mildly designed; the manifest lists two files without row counts. Readings: the referral share's denominator (accepted within two hours over referrals made, against responded within two hours per clause 4.2); the chart's weeks (the finance calendar's Monday to Sunday weeks, and weeks straddling the quarter's ends); payable visits as a count; time bases and status labels (documented Layer 1).

Rulings (stage 4 fix pass, after the rebuild): every REVIEW line harmless, as read. The three readings are closed: the referral share's basis by Schedule 4 clause 4.5 (each quarter, for each Member, the share of the referrals it made that Bellbird accepted within two hours, and the share of its accepted referrals first visited within 24 hours), the response reading of clause 4.2 asserted another figure for every Member; the chart's weeks by the prompt's "pay week" and the dictionary's week_commencing row (Monday to Sunday, the year's first pay week commencing 29 June 2026), the part weeks holding only the quarter's days because the export holds nothing else (asserted); payable visits as a count by the prompt's "the number of", attempted visits payable under clause 3.4 (completed visits alone asserted another count). Realism: the manifest now gives rows or pages for every file; the H04 plan rows are kept (October to March feed the call, so no figure-neutral change exists).

## Solver's-eye read (round 2)

Targeted re-read after the stage 4 fix pass (Schedules 3 and 4 clause 4.5, the dictionary's week_commencing row, the manifest and the prompt's chart sentence): clean.

- Q1: no sentence quoted that announces the decisive step.
- Q2: no file ranks the members on the booking.
- Q4: no figure or name reads as the answer.
- Q6: the main call is decided by an analytical choice.
- Telephoned referrals count as referrals under Schedule 4 clause 4.1: closed in the pack.
- The straddling pay weeks hold only the quarter's days: closed in the pack.
- Every accepted portal referral has a Bellbird visit after acceptance (checked: 0 missing): closed in the pack.
