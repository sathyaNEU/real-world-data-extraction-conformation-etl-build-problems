# leak check, task230

**Verdict: REVIEW.** 26 files read, 24 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: method, closed, repeat, detection, forecast, design, operations, driver, nothing, quarter, architecture, selection, decisive, back-test, segment, default, shift-day, registered, window, inside, population, monthly, decision, quality, monitoring

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `client_quality_schedules_2026.pdf`: golden figure 5.2 appears: ...9.80% 6% of the stream's monthly invoice KBA-PROF 5.2 99.48% 6% of the stream's monthly invoice Measure...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `QCP-04_first_pass_quality_control.docx`: 8 of 25 stump-paragraph terms appear (method, closed, forecast, operations, quarter, shift-day); read whether the document names the move
- **REVIEW** `capture_mis_extract_notes.md`: 6 of 25 stump-paragraph terms appear (closed, forecast, design, nothing, shift-day, quality); read whether the document names the move
- **REVIEW** `client_quality_schedules_2026.pdf`: 4 of 25 stump-paragraph terms appear (quarter, monthly, decision, quality); read whether the document names the move
- **REVIEW** `hollings_pryce_pilot_report.docx`: 5 of 25 stump-paragraph terms appear (forecast, operations, shift-day, inside, quality); read whether the document names the move

## 9 dates after the setting (REVIEW 5)
- **REVIEW** `form_specifications.xlsx`: 4 ISO dates after 2026-10-28, e.g. 2026-11-09, 2026-11-16, 2026-11-23
- **REVIEW** `hollings_pryce_forecast_nov26.json`: 10 ISO dates after 2026-10-28, e.g. 2026-11-02, 2026-11-09, 2026-11-16, 2026-11-23, 2026-11-30
- **REVIEW** `november_operating_plan.xlsx`: 30 ISO dates after 2026-10-28, e.g. 2026-11-01, 2026-11-02, 2026-11-03, 2026-11-04, 2026-11-05
- **REVIEW** `stream_register.csv`: 3 ISO dates after 2026-10-28, e.g. 2026-10-31, 2026-11-01
- **REVIEW** `wattlebird_coolabah_forecasts_fy27.xlsx`: 19 ISO dates after 2026-10-28, e.g. 2026-11-01, 2026-11-02, 2026-11-08, 2026-11-09, 2026-11-15

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

Two reads at medium effort, each on a fresh copy of `prompt.txt` and `target/` and nothing else.

**Read 1 (the first cut of the rebuilt asks).** Question 1: none (nearest QCP-04 4.3, one method for every stream, not
which). Question 2: none. Question 3: none clearly (nearest the MIS notes; the labour note read as tailored for its
change line). Question 4: none (the pilot's 0.69 against 0.77 is context). Question 5: QCP-04 4.1 fixes the
population (the stream's own documents the November plan routes), the window, the unit; no method. REVIEW lines all
harmless; the labour note's change line "mildly leaky". Realism tells: badge and employee numbers in fixed steps,
forecast revisions in uniform steps, the schedules' repeated credit sentence, the plan's even daily spread. Fixed in
the generator (irregular numbers by date of joining, week-by-week re-forecasts, each client's credit clause in its
own words, the change line removed); the plan's spread is its documented rule and stays.

**Read 2 (after the repair).** Question 1: none (QCP-04 4.3 gives the method in outline only). Question 2: none.
Question 3: none clearly. Question 4: none (the pilot's 0.69 and the October list are context). Question 5: QCP-04
4.1, the quantity without a method (the design forces it). REVIEW lines all harmless; the pilot report's "Second-pass
verification ran on the pilot's documents throughout" read as weakly suggestive, a process fact the typed family's
second-pass minutes need, harmless. Remaining notes are tidiness impressions (engineered variety across clients,
tidy notes and version history), none a gate finding.
