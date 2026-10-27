# leak check, task304

**Verdict: LEAK.** 14 files read, 3 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: arrears, account, payment, accounts, months, planning, window, payments, switch, asserted, first-time, section, family, decisive, concession, history, extended, chance, extensions, member, comparison, golden, close-out, register, entries

## 1 file names (LEAK 1, REVIEW 1)
- **LEAK** `data_dictionary.csv`: a file whose name says it describes the data (data_dictionary): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `product_transfer_rate_card_2026-10.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `financial_support_team_2027_plan_paper.pdf`: carries 11 of 14 distinctive words of the committed call: 'Place the Financial Support Team on the First-time buyer 2019-21 book in 2027: it avoids about 10 possessions there, aga'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `arrears_and_possessions_policy_2026.pdf`: 7 of 25 stump-paragraph terms appear (arrears, account, payment, months, payments, switch); read whether the document names the move
- **REVIEW** `board_risk_appetite_statement_2026.pdf`: 6 of 25 stump-paragraph terms appear (arrears, account, payment, accounts, payments, first-time); read whether the document names the move
- **REVIEW** `financial_support_team_2027_plan_paper.pdf`: 12 of 25 stump-paragraph terms appear (arrears, account, payment, accounts, months, planning); read whether the document names the move
- **REVIEW** `financial_support_team_pilot_2024_report.pdf`: 9 of 25 stump-paragraph terms appear (arrears, account, payment, accounts, months, planning); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `data_dictionary.csv`: Python-style nulls or booleans (nan/None/True/False) in the first rows

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `mortgage_book_2026-09-30.parquet`: 54897 ISO dates after 2026-09-30, e.g. 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31, 2027-02-28

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)
