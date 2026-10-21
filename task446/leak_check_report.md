# leak check, task446

**Verdict: REVIEW.** 17 files read, 29 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: member, cohorts, cohort, decisive, asserted, closed, architecture, window, customer, pooled, parent, estimand, credit, raised, nothing, facility, ultimate, driver, history, forecasting, customers, booked, standard, segmentation, sentence

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: \bthe model\b x1: ...have not changed since. A change would be a new release, approved by the Model Risk Committee before use. 1.3 Dates and times in this standard are U...

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: golden figure 5.1 appears: ...s not reaching it. 5 Watch-list caseload forecast 5.1 In the close of each monitoring year, which ends...
- **REVIEW** `credit_data_field_reference.md`: carries 9 of 14 distinctive words of the committed call: 'Set the 2027 watch-list caseload at 78 groups: 78 of the 913 obligor groups in the monitored book at 30 September 2026 a'
- **REVIEW** `crm_year_end_close_timetable_2026.docx`: carries 10 of 14 distinctive words of the committed call: 'Set the 2027 watch-list caseload at 78 groups: 78 of the 913 obligor groups in the monitored book at 30 September 2026 a'
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: carries 14 of 14 distinctive words of the committed call: 'Set the 2027 watch-list caseload at 78 groups: 78 of the 913 obligor groups in the monitored book at 30 September 2026 a'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `credit_data_field_reference.md`: 8 of 25 stump-paragraph terms appear (closed, customer, parent, credit, facility, ultimate); read whether the document names the move
- **REVIEW** `crm_year_end_close_timetable_2026.docx`: 5 of 25 stump-paragraph terms appear (cohort, closed, credit, history, standard); read whether the document names the move
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: 12 of 25 stump-paragraph terms appear (member, cohorts, cohort, closed, customer, parent); read whether the document names the move
- **REVIEW** `reference_data_extract_log_20261008.txt`: 3 of 25 stump-paragraph terms appear (credit, facility, history); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `facility_obligor_extract_20260930.csv`: 3047 ISO dates after 2026-10-08, e.g. 2026-10-10, 2026-10-17, 2026-10-26, 2026-10-29, 2026-10-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (prompt.txt and a fresh unzip of target.zip only), 2026-10-15, after the 10/10 repair.

1. Decisive step: none. CRM-07 5.2 defines the quantity and says nothing of how to forecast it; 4.3 gives the committee's performance vocabulary, not an instruction for the forecast.
2. File ranking or forecasting the caseload: none. The rating sheet gives a grade per group, an input to weigh, not a ranking of the answer.
3. Files only to help: none; the field reference, trigger codes and rates are ordinary companions.
4. Figure or name reading as the answer: none.
5. 4.1, 4.2, 5.1 and 5.3 fix the population, outcome, window, exclusions, rounding and the band split; no sentence fixes the forecasting method, its fitting window or a rule for choosing between methods.
6. What decides: an analytical choice, how to estimate expected arrivals for the open cohort from what the closed cohorts show.

REVIEW lines: "the model" (the Model Risk Committee in 1.2), harmless; the call's nouns in the standard, harmless (it defines the quantity); stump-paragraph terms, harmless (the document never names the move); dates after the setting, harmless (final maturity dates of live facilities).

Realism tells (minor, all present in the shipped version, no figure touched): the 01:15 extract run after start of day reads as deliberate (it is the ask layer's limit clock); a tidy reconciliation line in the log; the grade 7 PD midpoint at exactly 0.03. Kept: the extract timing is the ask device's real cause, and the others are cosmetic.
