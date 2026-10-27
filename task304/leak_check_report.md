# leak check, task304

**Verdict: REVIEW.** 13 files read, 3 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: arrears, account, payment, months, accounts, planning, window, payments, extension, switch, asserted, family, first-time, section, concession, policy, decisive, carries, history, golden, forecast, extended, chance, extensions, member

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `financial_support_team_2027_plan_paper.pdf`: carries 11 of 14 distinctive words of the committed call: 'Place the Financial Support Team on the First-time buyer 2019-21 book in 2027: it avoids about 10 possessions there, aga'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `arrears_and_possessions_policy_2026.pdf`: 9 of 25 stump-paragraph terms appear (arrears, account, payment, months, payments, extension); read whether the document names the move
- **REVIEW** `board_risk_appetite_statement_2026.pdf`: 6 of 25 stump-paragraph terms appear (arrears, account, payment, accounts, payments, first-time); read whether the document names the move
- **REVIEW** `financial_support_team_2027_plan_paper.pdf`: 12 of 25 stump-paragraph terms appear (arrears, account, payment, months, accounts, planning); read whether the document names the move
- **REVIEW** `financial_support_team_pilot_2024_report.pdf`: 10 of 25 stump-paragraph terms appear (arrears, account, payment, months, accounts, planning); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `mortgage_book_2026-09-30.parquet`: 54897 ISO dates after 2026-09-30, e.g. 2026-10-31, 2026-11-30, 2026-12-31, 2027-01-31, 2027-02-28

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

One isolated leak reader (sonnet, medium), on fresh copies of prompt.txt and target/ from target.zip 57a875af, read for leaks and solved nothing.

1. Decisive step: none. "No sentence announces it. Closest are the plan paper's section 3 method sentences ... These fix the method rather than flag a pitfall."
2. Ranking: the plan paper's planning-rate table (4.5, 7.4, 1.9, 10.7 per cent) with "the book with the most possessions avoided is the one to choose"; the reader calls the rates "an easy route to a placement" and names Buy to let, the highest rate, the obvious pick.
3. Analyst-only file: none. "No file looks analyst-only."
4. Answer figure: none. "Nothing reads as the answer"; the rates and the 15 per cent cut read as inputs and no book is named.
5. Literal sentences: plan sections 2 and 3 fix the 2027 population (first crossings to two payments in arrears in calendar 2027, the 30 September 2026 book with no closures, litigation and receiver accounts left out), the arrears measure (policy section 2), the rate window and outcome, and the figure as 0.15 times each book's expected 2027 borrowers taken on times its planning rate.
6. What decides: "Mostly an analytical choice"; read as a stated procedure only if the analyst takes the 2027 flow as given rather than estimating it.

Sweep lines: sweep 3 harmless (the paper is the Committee's own brief, it must use the team's and the books' names, and it carries no avoided count); sweep 9 harmless (every future date is product_end_date, fixed-rate expiries to 2031; completion_date ends 2026-08-28).

Realism: selling costs to the penny; the litigation file's 2022 claims inside a 2023-01 to 2026-09 name; claim numbers as letter and digit strings; the rate card's creator "Mortgage Pricing"; the distractors; the PDFs' saved times and producer; the plan's neat capacity figure; mixed date formats.

### Rulings (main thread)

- Q1, Q3, Q4: nothing quoted. Harmless.
- Q2: harmless. The rate table holds a filed input of the estimand, not a ranking on the decision question: possessions avoided need each book's 2027 entries, and the rate alone names Buy to let, which is neither the call nor the default path's wrong book (Gate G passes on the judge's pass 1). It stays.
- Q5: each quoted sentence is the WHAT the golden executes (population, window, unit, comparison, the 15 per cent cut); the 2027 entries are the forecast the plan leaves to the analyst. Executes to the golden; not a fork.
- Q6: analytical. The plan files the arithmetic around the forecast, and the forecast of each book's 2027 entries is the step (the concessions' delayed re-entry), which no file states.
- Realism: selling costs to the penny are fees on a sale price plus fixed charges, as real completion statements carry them; the litigation file holds every claim open at any time from January 2023, so claims issued in 2022 belong in it, and the name now says so; claim numbers follow the county court format; "Mortgage Pricing" is the owning team, as a shared workbook's author field often reads; the rate card's two sheets are "Product transfers" and "Terms" (the reader joined each title to its visibility state); the PDFs now carry working-day save times on the UK offset (fixed after the first read). No change.
