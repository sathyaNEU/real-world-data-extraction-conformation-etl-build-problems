# leak check, task446

**Verdict: REVIEW.** 18 files read, 21 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: cohorts, standard, decisive, back-test, device, architecture, cohort, entity, signals, register, forecast, screen, asserted, projection, consolidation, closed, performance, measure, agenda, sentence, golden, measures, reference, seasonal, ladder

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: \bthe model\b x1: ...have not changed since. A change would be a new release, approved by the Model Risk Committee before use. 2 Obligor groups 2.1 An obligor group is t...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: golden figure 5.1 appears: ...s not reaching it. 5 Watch-list caseload forecast 5.1 Each October credit risk monitoring forecasts how...
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: carries 13 of 13 distinctive words of the committed call: 'Put a 2027 caseload of 134 groups to the committee: 134 of the 913 obligor groups in the monitored book at 30 September '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `credit_data_field_reference.md`: 5 of 25 stump-paragraph terms appear (entity, register, consolidation, closed, reference); read whether the document names the move
- **REVIEW** `early_warning_and_watch_list_standard.pdf`: 13 of 25 stump-paragraph terms appear (cohorts, standard, cohort, entity, signals, register); read whether the document names the move
- **REVIEW** `exec_risk_committee_agenda_2026-11-04.docx`: 3 of 25 stump-paragraph terms appear (standard, performance, agenda); read whether the document names the move

## 9 dates after the setting (REVIEW 3)
- **REVIEW** `facility_extract_hbdac_20260930.csv`: 110 ISO dates after 2026-10-11, e.g. 2026-12-15, 2027-01-03, 2027-01-27, 2027-02-19, 2027-02-22
- **REVIEW** `facility_extract_hbplc_20260930.csv`: 2587 ISO dates after 2026-10-11, e.g. 2026-10-21, 2026-10-28, 2026-10-30, 2026-11-01, 2026-11-05
- **REVIEW** `facility_extract_hbplc_20260930_rerun.csv`: 2587 ISO dates after 2026-10-11, e.g. 2026-10-21, 2026-10-28, 2026-10-30, 2026-11-01, 2026-11-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt form (clean)

## Solver's-eye read (architecture 2)

One isolated reader (Sonnet), 2026-10-11, on a fresh scratch copy of prompt.md and target.zip.

- **Q1 (decisive step named):** no sentence names it, but `early_warning_and_watch_list_standard.pdf` carries the procedure: 4.3 (hit, capture and false-alarm rates "on the last four closed cohorts taken together"), 5.2 ("a probability of reaching the watch list that depends only on its flag status at the cohort date ... set from the performance measures in 4.3"), 1.2 (models unchanged), 4.1, 4.2, 5.1 (book, outcome, later joiners excluded).
- **Q2:** none states the asked figures (nearest: the rating master scale's PD grades, far from the answer).
- **Q3:** `credit_data_field_reference.md`, then the extract log's "the rerun is the record for 30/09"; neither touches the decisive step.
- **Q4:** none.
- **Forks:** (1) MAIN CALL: pooled hit rates (38% flagged, 1.4% unflagged) give about 74; backing the probabilities out of capture (79%) and false-alarm (7.7%) on the September flag share (165 of 913) gives about 134; the reader says the text allows both and only the data separates them. (2) Inside the inversion: pooled 134.1, mean of cohort rates 133.9, three cohorts 133 or 136, latest alone 129. (3) Asks: 6.1 states only the maturity rule, so CANCELLED and CLOSED rows with future maturity move 18 groups between bands.
- **Realism tells:** python-docx default template and openpyxl stub app.xml with identical created and modified stamps across four authors; the standard's 2.3 lists exactly the pack's edge cases; RED counts jump only each 30 September; the 25 ACTIVE facilities maturing 30/09/2026 are the last 25 rows.
- **REVIEW lines:** all harmless (clause numbers, topic words, contract maturity dates).

Main-thread disposition: fork (1) is a main-call fork and the same defect the portal's judge failed task445 on (a filed basis whose literal reading gives the easy answer); it is closed before any solver round, in a designer pass (the standard states the estimand and the criterion that selects the basis, never a basis that yields the easy answer). Fork (3) is pinned in the same pass; the realism tells are repaired in the same rebuild.
