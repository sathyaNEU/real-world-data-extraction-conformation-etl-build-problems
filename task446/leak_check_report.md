# leak check, task446

**Verdict: REVIEW.** 17 files read, 33 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: history, cohort, cohorts, decisive, closed, facility, window, arrival, architecture, standard, reaching, register, extract, entity, status, signals, together, measured, projection, consolidation, nearest, forecast, property, asserted, pooled

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: \bthe model\b x1: ...have not changed since. A change would be a new release, approved by the Model Risk Committee before use. 1.3 Dates and times in this standard are U...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: golden figure 5.2 appears: ...after the cohort date are outside the forecast. 5.2 The forecast is the number of groups in the monit...
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: carries 13 of 13 distinctive words of the committed call: 'Put a 2027 caseload of 133 groups to the committee: 133 of the 913 obligor groups in the monitored book at 30 September '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `credit_data_field_reference.md`: 6 of 25 stump-paragraph terms appear (closed, facility, register, extract, entity, consolidation); read whether the document names the move
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: 18 of 25 stump-paragraph terms appear (history, cohort, cohorts, closed, facility, arrival); read whether the document names the move
- **REVIEW** `reference_data_extract_log_20261008.txt`: 3 of 25 stump-paragraph terms appear (history, facility, extract); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `facility_obligor_extract_20260930.csv`: 3021 ISO dates after 2026-10-11, e.g. 2026-10-19, 2026-10-22, 2026-10-23, 2026-10-29, 2026-10-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt form (clean)

## Solver's-eye read (architecture 2, loop 1)

One isolated reader (Sonnet, medium), 2026-10-11, on a fresh copy of prompt.md and target.zip (cut d1696c6).

- **Q1:** none. Closest: the standard's 5.2 basis test ("on whichever basis predicts those cohorts best ... on the basis set from the other three taken together"), read as a test, not the step.
- **Q2:** none. **Q3:** none clearly (the field reference and extract log read as ordinary reference-data documents). **Q4:** none.
- **Q5:** 4.1 (book), 4.2 (outcome, counted once), 2.2 (membership through the credit system and GLEIF consolidation in force at the date), 3.2 (flag: any member AMBER or RED), 5.2 (one probability per flag status, the same across the book; the basis chosen by the leave-one-out test, error the largest share miss, smallest error wins), 6.1 and 6.2 (exposure, bands), 5.3 (rounding). Literal execution: rebuild each cohort's book, membership and flags, compute outcomes, run the leave-one-out test over candidate bases, apply the winner to the 2026 book. Open choice named: the candidate list is not enumerated.
- **Realism tells (deferred to 6b):** a tidy extract log; standard 1.2's "models, triggers and bands have not changed since" reads convenient; the analyst-capacity fact appears in both the prompt and the agenda.
- **Forks sized:** the candidate set (largest); flag status for CRN-keyed members (a few flags); exposure at end of date against UTC stamps (band figures).
- **REVIEW lines:** all harmless.

Main-thread disposition: no Q1 to Q3 finding. Q5's open candidate list is closed by convergence, asserted in the generator: the winning basis (capture and false-alarm, worst miss 1.57 per cent) and the next four bases (2.00 to 2.03 per cent) all give 133; the only bases giving other numbers (147 at 7.97 per cent, 73 at 40.6 per cent) lose the filed test by a wide margin. The CRN-key fork moves ask figures only (separation zero-counts asserted). Realism tells deferred to stage 6b.
