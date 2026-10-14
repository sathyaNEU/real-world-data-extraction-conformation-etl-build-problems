# leak check, task255

**Verdict: REVIEW.** 12 files read, 43 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: million, record, closed, likelihood, truncation, censoring, deductible, window, sentence, censored, asserted, memorandum, severity, decisive, fitted, actuary, accident, nothing, distribution, ground-up, observation, thresholds, recorded, archive, current

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `risk_financing_policy_2026.pdf`: carries 10 of 13 distinctive words of the committed call: "Keep the first $4,000,000 of each 2027 liability occurrence: Fallowmere's 2027 retention is the $4.0 million quoted atta"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `actuarial_study_2026_selected_exhibits.pdf`: 3 of 25 stump-paragraph terms appear (million, actuary, accident); read whether the document names the move
- **REVIEW** `extract_notes_2027_retention_review.md`: 5 of 25 stump-paragraph terms appear (closed, deductible, actuary, accident, current); read whether the document names the move
- **REVIEW** `liability_coverage_memorandum_2026.pdf`: 3 of 25 stump-paragraph terms appear (record, deductible, memorandum); read whether the document names the move
- **REVIEW** `risk_financing_policy_2026.pdf`: 8 of 25 stump-paragraph terms appear (record, likelihood, deductible, severity, actuary, accident); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `vehicle_schedule_log_2022-2026.csv`: 7 ISO dates after 2026-11-18, e.g. 2026-11-19, 2026-11-20, 2026-11-21, 2026-11-22, 2026-11-24

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

Three isolated reads on the loop 1 cut (fresh copies of prompt.txt and target/ only).

- Read 1: no decisive-step sentence, no ranking or answer-like figure. Finding: the coverage memorandum said "once the pool's share is paid, the pool's administrator closes the pool's file on the occurrence", which the twenty open suits of 2014 to 2021 contradict. Fixed: the clause is cut. Realism: the notes' "The documents beside them are as issued" read as meta; reworded.
- Read 2 (after the fix): no decisive-step sentence; question 6 an analytical choice (the fit of a record that is truncated and capped); question 7 no contradiction; nothing names the open suits.
- Read 3 (after the vehicle-identity notes): no decisive-step sentence; it asked whether the unit count is by effective or entered date (filed: effective_date is when the change applies to coverage) and whether trailers count (the broker rates on "the units on the members' vehicle schedules"). Realism tells (round totals at the pool's share, open files with nothing reserved, tidy notes) are the record as such a pool keeps it: a capped occurrence's pool share is the retention less the deductible, and an open suit whose layer is paid carries no reserve.

Mechanical REVIEW lines: the policy's call words and the documents' vocabulary are the estimand's own (no move named); the schedule rows effective after the meeting are deletes keyed ahead, allow-listed in metadata.json.
