# leak check, task446

**Verdict: REVIEW.** 17 files read, 33 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: cohort, cohorts, screen, decisive, window, asserted, closed, standard, forecast, measured, arrival, forecasting, history, estimand, reading, sample, facility, carries, reaching, validated, sentence, clause, property, measures, stated

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: \bthe model\b x1: ...have not changed since. A change would be a new release, approved by the Model Risk Committee before use. 1.3 Dates and times in this standard are U...

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: carries 13 of 13 distinctive words of the committed call: 'Put a 2027 caseload of 133 groups to the committee: 133 of the 913 obligor groups in the monitored book at 30 September '

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: 11 of 25 stump-paragraph terms appear (cohort, cohorts, closed, standard, forecast, measured); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `facility_obligor_extract_20260930.csv`: 3021 ISO dates after 2026-10-11, e.g. 2026-10-19, 2026-10-22, 2026-10-23, 2026-10-29, 2026-10-30

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
