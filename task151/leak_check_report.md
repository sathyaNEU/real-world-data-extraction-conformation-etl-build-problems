# leak check, task151

**Verdict: REVIEW.** 21 files read, 25 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: season, regulars, starts, look-back, appearances, projection, planned, vendor, catchers, decisive, population, starting, non-catcher, contract, distribution, asserted, regular, readable, batting, sheets, scores, lineup, golden, window, forecasting

## 1 file names (REVIEW 2)
- **REVIEW** `lsf_batting_2021_2024.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `lsf_feed_notes.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 7)
- **REVIEW** `CF-14.4_look-back_working_paper.pdf`: golden figure 4.4 appears: ...ses Standing paper under Accounting Policy FIN-14 4.4. Prepared by Harry Barnes, Controller, November 1...
- **REVIEW** `FIN-14_player_compensation_accounting_policy.pdf`: golden figure 4.4 appears: ...ys less than planned, is part of the probability. 4.4 The Controller chooses the basis for the probabil...
- **REVIEW** `ral_player_contract_register_2023_2026.xlsx`: golden figure 225,000 appears: ...Juan E1096965 3B 12/12/2024 2025 7250000 500000 $225,000 each for 375, 475 and 575 plate appearances Assig...
- **REVIEW** `ral_player_contract_register_2023_2026.xlsx`: golden figure 140,000 appears: ...1B 12/14/2022 2023-2024 9500000 9500000 1000000 $140,000 each for 500, 550, 600 and 650 plate appearances...
- **REVIEW** `ral_player_contract_register_2023_2026.xlsx`: golden figure 55,000 appears: ...01661 P 12/20/2022 2023 5500000 Innings pitched: $55,000 each for 140 and 160 Expired Blair, Johnny E10658...
- **REVIEW** `ral_player_contract_register_2023_2026.xlsx`: golden figure 60,000 appears: ...24 2025-2026 2400000 2400000 Relief appearances: $60,000 each for 55 and 65 $50,000 for All-Star selection...
- **REVIEW** `term_sheets_2027_free_agent_hitters.pdf`: carries 7 of 10 distinctive words of the committed call: "Accrue $4,250,000 at signing for the plate-appearance bonuses in the five free-agent hitters' 2027 contracts."

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `CF-14.4_look-back_working_paper.pdf`: 7 of 25 stump-paragraph terms appear (season, look-back, appearances, starting, contract, scores); read whether the document names the move
- **REVIEW** `FIN-14_player_compensation_accounting_policy.pdf`: 6 of 25 stump-paragraph terms appear (season, look-back, appearances, planned, contract, scores); read whether the document names the move
- **REVIEW** `lsf_feed_notes.txt`: 5 of 25 stump-paragraph terms appear (season, appearances, catchers, batting, lineup); read whether the document names the move
- **REVIEW** `term_sheets_2027_free_agent_hitters.pdf`: 3 of 25 stump-paragraph terms appear (season, appearances, contract); read whether the document names the move

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
(sha256 44480c2b, the hardening's first cut) and prompt.txt only, briefed with the six questions and the REVIEW lines
minus the stump-vocabulary lines and minus every figure. Verdict: CLEAN, nothing hands over the answer or a step.

- Q1: for the call it quotes FIN-14 4.4 (the look-back that chooses the basis), the filed selection criterion that names
  no basis; for the supplementary table, no sentence names a step (a compilation from the register and the payroll).
- Q2: no file ranks or scores the five.
- Q3: lsf_feed_notes.txt (the League's field notes) and the close-file index, which it reads as the close-file record
  FIN-14 6 calls for; both frozen main-call files carried since e93c6561.
- Q4: nothing reads as the answer; every dollar figure is a raw input (terms, salaries, a projection, a past payment).
- Q5: FIN-14 4.2 and 4.3 fix the call's estimand at signing with health inside the probability, leaving the basis to
  4.4; for the table no filed sentence fixes the computation and nothing states how to attribute a payment to a class.
- Q6: an analytical choice (the basis chosen by the back-test).
- REVIEW lines: the batting file is the League's record; the four flagged documents read as context; no file ranks the
  five; the calendar and the 2027 schedule are forward by nature.
- Realism: nothing planted; the October 2025 void, reversal and reissue read as an ordinary correction; the payroll,
  the register, the HRIS map and the code table read as one club's records across a migration. It did not surface the
  deferred salary in the contract-end lines.

The shipped pack (3ded6ddd) differs from the read pack only in five deferral amounts and the salary lines carrying them,
a record file and no document, so the read stands (`leak-check`: the reader re-runs only when a document or the prompt
changes). Ruling on the REVIEW lines: every one harmless (the design note's Build record).
