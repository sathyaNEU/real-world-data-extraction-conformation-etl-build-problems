# leak check, task151

**Verdict: REVIEW.** 21 files read, 24 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: season, regulars, starts, look-back, appearances, projection, planned, vendor, catchers, decisive, population, starting, non-catcher, distribution, asserted, regular, readable, batting, sheets, scores, record, lineup, golden, window, forecasting

## 1 file names (REVIEW 2)
- **REVIEW** `lsf_batting_2021_2024.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `lsf_feed_notes.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `CF-14.4_look-back_working_paper.pdf`: golden figure 4.4 appears: ...ses Standing paper under Accounting Policy FIN-14 4.4. Prepared by Harry Barnes, Controller, November 1...
- **REVIEW** `FIN-14_player_compensation_accounting_policy.pdf`: golden figure 4.4 appears: ...ys less than planned, is part of the probability. 4.4 The Controller chooses the basis for the probabil...
- **REVIEW** `ral_player_contract_register_2023_2026.xlsx`: golden figure 140,000 appears: ...1B 12/14/2022 2023-2024 9500000 9500000 1000000 $140,000 each for 500, 550, 600 and 650 plate appearances...
- **REVIEW** `ral_player_contract_register_2023_2026.xlsx`: golden figure 60,000 appears: ...24 2025-2026 2400000 2400000 Relief appearances: $60,000 each for 55 and 65 $50,000 for All-Star selection...
- **REVIEW** `term_sheets_2027_free_agent_hitters.pdf`: carries 7 of 10 distinctive words of the committed call: "Accrue $4,250,000 at signing for the plate-appearance bonuses in the five free-agent hitters' 2027 contracts."

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `CF-14.4_look-back_working_paper.pdf`: 6 of 25 stump-paragraph terms appear (season, look-back, appearances, starting, scores, lineup); read whether the document names the move
- **REVIEW** `FIN-14_player_compensation_accounting_policy.pdf`: 6 of 25 stump-paragraph terms appear (season, look-back, appearances, planned, scores, record); read whether the document names the move
- **REVIEW** `lsf_feed_notes.txt`: 5 of 25 stump-paragraph terms appear (season, appearances, catchers, batting, lineup); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 1)
- **REVIEW** `hvbd_hitter_projections_2022_2027.csv`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `hvbd_winter_depth_charts_2021_2026.xlsx`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lsf_transactions_2024_2026.json`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `term_sheets_2027_free_agent_hitters.pdf`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `ral_depth_chart_2027.xlsx`: names 9 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `league_calendar_2021_2027.csv`: 5 ISO dates after 2026-12-11, e.g. 2027-03-25, 2027-07-12, 2027-07-15, 2027-09-26, 2027-09-29
- **REVIEW** `league_schedule_2027.csv`: 2430 ISO dates after 2026-12-11, e.g. 2027-03-25, 2027-03-26, 2027-03-27, 2027-03-28, 2027-03-29

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader: one isolated general-purpose agent (sonnet, medium effort), 2026-10-28, on a fresh unzip of target.zip
(sha256 f4bcf386) and prompt.txt only. Verdict: CLEAN, nothing hands over the answer or the decisive step.

- Q1: the call's step is not named: FIN-14 4.4 and CF-14.4 file the look-back's population, score and selection rule
  and name no basis. For the supplementary table no sentence names a step; the register's two bonus columns and FIN-14
  4.1's list separate the classes.
- Q2: no file ranks or scores the candidates.
- Q3: lsf_feed_notes.txt (the League's own field notes, layout only) and the close-file index (the close binder's
  index); neither names the task, a bonus or the look-back. Both shipped at e93c6561 and are unchanged.
- Q4: nothing reads as the answer; CF-14.4's 450 to 650 scoring ladder overlaps contract thresholds by design.
- Q5: the call: FIN-14 4.2 and 4.3 literally fix an expected amount at signing over the five term sheets. The reader
  notes the vendor's 2027 preliminary projection is dated December 1, after two signings; the golden basis does not
  read it (main side frozen, three judge rounds and the 10-28 pass found no fork). The table: the reader names pay
  year against season earned as two readings of "paid for each of the seasons"; the 10-28 judge recomputed and found
  no competing answer (FIN-14 4.5 and the word "for"; every January payment precedes that year's Opening Day). It
  observes, unprompted, that a pitcher's season-end and January payments pair across two codes and that the code alone
  cannot separate the classes.
- Q6: the call is decided by an analytical choice (a basis chosen by an out-of-sample back-test).
- Realism: nothing reads as generated or planted; the two Andres Rivas are realistic collision noise; the five's
  signing order equalling their lineup order is a mild tell in two frozen main-call files.

Ruling on the REVIEW lines: every one harmless (the reader's verdicts match the design note's Build record).
