## Tags

**Domain:** Banking, credit and financial risk (collections and recovery).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Place the Financial Support Team on the First-time buyer 2019-21 book in 2027: it avoids about 10 possessions there, against fewer than 5 in High LTV 2022-24, the next best.**
The first-time buyer book's 2021 borrowers who took a longer term at their 2026 rate switch are almost all up to date now, but the 2024 term increases fell behind mostly after their first eight months, so the book's 2027 arrears cases outnumber every other book's. Not High LTV 2022-24, which leads on current arrears and on a forecast that reads the extended accounts' small payment rise as low risk. Not Shared ownership or Buy to let, at fewer than 5 each.

## 2. Critical Components

1. **7,129** of the **16,455** first-time buyer accounts on the book at 30 September 2026 had their remaining term raised at their 2026 rate switch, a median **10** years, holding their payment rise to a median **10 per cent** against **26 per cent** for the switchers on the book who kept their term.
2. Of the **347** accounts whose term was raised in 2024, **4** were two payments or more in arrears at one of the eight month ends after the month of the increase and **81** at a month end after it up to 30 September 2026.
3. Possessions avoided in 2027 (nearest ten): First-time buyer 2019-21 **10**; High LTV 2022-24, Shared ownership and Buy to let **fewer than 5** each, at the planning rates of **4.5**, **7.4**, **1.9** and **10.7 per cent** and the plan's **15 per cent** cut.

## 3. Step-by-Step Solution

1. Rebuilt payments in arrears at each month end from mortgage_payment_history_2019-01_to_2026-09.parquet (the arrears balance over the contractual payment, rounded down, arrears_and_possessions_policy_2026.pdf section 2), with the re-sent month rows dropped.
2. Marked each rate switch (a new product_code, read with the dashes taken out) and each month the remaining_term_months rose: 7,129 first-time buyer accounts on the book had their term raised at the 2026 switch, and 81 of the 347 raised in 2024 had been two payments behind at a month end after the month of the increase up to September 2026, 4 of them at one of the eight month ends after it.
3. Fitted the monthly chance of each move between nought, one and two or more payments behind on the January 2024 to August 2026 history, by book, the payment rise at the last switch (under 5, 5 to 20, 20 to 40, 40 per cent or more) and the months since a term increase (none, under 8, 8 to 15, 16 or more), leaving out the month an account closes, each cell smoothed towards its book's rate with a weight of 20 account-months.
4. Carried every account on mortgage_book_2026-09-30.parquet with recovery_stage None from its September 2026 arrears through 2027, month by month, with no allowance for accounts that close, counting each account's first entry from January to December 2027 once and taking it out of the chain there (financial_support_team_2027_plan_paper.pdf section 2).
5. Took 15 per cent of each book's expected 2027 entries times its planning rate (financial_support_team_2027_plan_paper.pdf section 3): First-time buyer 2019-21 about 10 possessions avoided, High LTV 2022-24 fewer than 5, Shared ownership and Buy to let fewer than 5 each; the same chain without the term-increase state puts High LTV 2022-24 first.
6. From litigation_open_claims_2023-01_to_2026-09.csv (one line per claim and action, the second defendant's lines dropped) counted the possession orders made or varied at hearings dated 1 October 2025 to 30 September 2026, an order line repeating the claim's previous order with no hearing between being the same order sent again, and took each claim as open at 30 September 2026 unless withdrawn, discharged, evicted or, since Ridley Varga's reports end at the warrant, recorded in possession_register_2019-01_to_2026-09.csv as taken into possession after it was issued.
7. Took the latest statement of each sale reference in possession_sales_completed_2019-2026.csv completed from 1 October 2025 to 30 September 2026, matched receivers' sales to the account through lpa_receiver_appointments_2019-2026.csv, counted one possession sold per account and completion date (the Society issues a statement for each loan part), took the debt as the sum of the account's rows in possession_register_2019-01_to_2026-09.csv (one per loan part) and each account's book from mortgage_payment_history_2019-01_to_2026-09.parquet (the register's rows before April 2026 carry its earlier first-time buyer book), and set each loss to the debt less the sale price net of selling costs, nil where the sale covers it (policy section 8).
8. Recommended the First-time buyer 2019-21 book, about 10 possessions avoided against fewer than 5 in High LTV 2022-24.

## 4. Deliverable Answers

### support_team_2027_placement_paper.pdf

1. The book to work in 2027: First-time buyer 2019-21, about 10 possessions avoided.
2. The next best book: High LTV 2022-24, fewer than 5 possessions avoided.
3. Chart of possessions avoided in 2027 by book (section 3 of the paper), with and without the term increases carried, the First-time buyer 2019-21 book the largest with them.

### support_team_2027_workbook.xlsx

1. Possession orders made or varied at hearings from October 2025 to September 2026, of those suspended on terms, and possession claims open at 30 September 2026:
   - First-time buyer 2019-21: 34, 27, 17
   - High LTV 2022-24: 71, 56, 43
   - Shared ownership: 9, 9, 2
2. Possessions sold with completion from October 2025 to September 2026 (sold, sold at a loss, average loss per possession sold):
   - First-time buyer 2019-21: 20, 7, £4,500
   - High LTV 2022-24: 24, 24, £33,300
   - Shared ownership: 4, 2, £3,300
