# leak check, task472

**Verdict: REVIEW.** 19 files read, 20 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, millrace, saltworks, counterfactual, decisive, silent, nothing, sailing, record, readiness, objective, decision, quantity, closed, halyard, reader, architecture, domain, operating, sailings, binding, directions, windows, missed, second

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `salt_point_tide_predictions_2025_2026.txt`: golden figure 257 appears: ...t 04:37 AM -3.2 -99 L 2025/06/14 Sat 10:54 AM 8.4 257 H 2025/06/14 Sat 05:05 PM -2.8 -85 L 2025/06/14 S...
- **REVIEW** `crane_replacement_program_rules.pdf`: carries 4 of 5 distinctive words of the committed call: 'Ternmouth should place the six 2027 replacement cranes at Millrace.'
- **REVIEW** `data_dictionary.txt`: carries 3 of 5 distinctive words of the committed call: 'Ternmouth should place the six 2027 replacement cranes at Millrace.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `crane_replacement_program_rules.pdf`: 5 of 25 stump-paragraph terms appear (millrace, saltworks, record, closed, halyard); read whether the document names the move
- **REVIEW** `data_dictionary.txt`: 10 of 25 stump-paragraph terms appear (window, millrace, saltworks, sailing, record, closed); read whether the document names the move
- **REVIEW** `harbor_masters_general_directions_2025.pdf`: 5 of 25 stump-paragraph terms appear (millrace, saltworks, sailing, sailings, directions); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `crane_maker_service_timesheets_fy2026.xlsx`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `crane_replacement_program_rules.pdf`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `data_dictionary.txt`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `berth_windows_fy2027.csv`: 7 ISO dates after 2026-10-06, e.g. 2027-01-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Four isolated readers (general-purpose, medium), each on a fresh copy of prompt.txt and target.zip, in two rounds;
each scored with score_reader.py before its verdict was read.

| Round | Reader | Call | Ask and component figures kept | score_reader |
|---|---|---|---|---|
| 1 | 1 | Saltworks 991, Pine Neck 804 (the default path) | 13 of 21: all twelve ask figures and the call count | exit 1 (asks re-sited) |
| 1 | 2 | Saltworks 991, Pine Neck 804 | 1 of 21 (the call count) | exit 0 |
| 2 | 1 | Saltworks 991, Pine Neck 804 | 1 of 21; found the second breakdown orders and the report-total keying, placed every stop at the register's terminal | exit 0 |
| 2 | 2 | Saltworks 991, Pine Neck 804 | 1 of 21 | exit 0 |

1. Decisive step announced: none, all four. Each quoted rules 3.4 to 3.7 as the definition and took the saving as a
   fifth of the cargo work.
2. A file ranking the terminals: none, all four.
3. Files only for the analyst: the data dictionary and the export manifest (registers every port keeps).
4. A figure or name reading as the answer: none.
5. Literal sentence: rules 3.5 to 3.7, executed as a fifth of each call's cargo work, giving Saltworks 990.62. That is
   the easy route on the same estimand, not another reading: rule 3.6 files the berth hours by which the call, all
   fast to let go (3.1), would have been shorter, and the directions file when a ship may sail; the judge's thread
   recomputed the golden from the same sentences and found every actual sailing equal to the first permitted time.
6. What decided the main answer: following the stated rules and conforming the data (all four). None met the
   sailing windows; the step none performed is the analytical one, recognising that the sailing the port's access
   rules allocate, not the last container move, ends a gated call's stay.
7. Realism: round 1 named three PROJECT outages of exactly 200.0 hours and about 250 repeated person, order and day
   ledger rows; round 2 named repeated description suffixes and three second breakdown orders at every terminal. All
   four were fixed in the generator (the move crew's booking times, staff assigned once per order and day, the
   descriptions drawn per order, the second orders two to four per terminal), a data-only repair checked by leak.py.

REVIEW lines, each harmless: 257 is a tide height in centimetres in the predictions table; the rules and the
dictionary carry the call's words and the stump's place names because they define the program and name the
terminals; the timesheets and the rules' document control name terminals beside hours and revision numbers, never
ranked on berth hours saved; the 2027 dates are the berth windows' effective dates, a declared distractor.
