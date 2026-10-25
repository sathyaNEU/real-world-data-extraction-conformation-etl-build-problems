## Tags

**Domain:** Banking, credit and financial risk, deposit and liquidity behaviour (home equity prepayment).  
**Analytical objective:** Forecasting and predictive modeling.

## 1. Final Recommendation

**Open the payoff-retention pilot at the Muskegon and the North lending center: its members will pay off about $40 million of fixed-rate home equity principal in 2027, the most of the four centers, and the Lakeshore comes second.**
The forecast reads each loan's payoff off the whole debt on the house, the first mortgage and the home equity loan at their balances: Muskegon and the North's 2024 to 2026 home equity loans are large and sit behind small seasoned first mortgages, so those stacks come into the money as the planning cycle's 30-year rate falls, and the region pays off 39.2 against 23.9 for the Lakeshore. Not Grand Rapids, which a prepayment curve on each loan's own note rate puts first at about $60 million (58.7), when its home equity loans sit behind large first mortgages that keep the debt on the house below the market. Not the Lakeshore, which leads when payoffs are read off the first mortgage's own rate alone because its purchase seconds sit behind high-rate first mortgages; those seconds are small. Not Kalamazoo and Battle Creek, whose trailing payoffs were its 2023 purchase loans, now mostly paid off.

## 2. Critical Components

1. Fixed-rate home equity loans on the books at the close of 30 November 2026: **8,813** loans, **$436.9 million**
2. Muskegon and the North's principal on the books at 30 November 2026: **$132.5 million**
3. Payoffs in full in the record the forecast is fitted on, January 2019 to November 2026: **5,264**

## 3. Step-by-Step Solution

1. Took the loans on the books from core_he_trial_balance_2024-09_2026-11.csv, the 2026-11-30 rows with LoanStatus ACTIVE: 8,813 loans, $436.9 million, per Lending Policy 7.4.3.
2. Built one loan-month history from January 2019 to November 2026 from legacy_he_loans_2019-01_2024-08.csv to August 2024 (each month's balance on the loan's schedule from BAL_12_31_2018 or its funding) and the trial balance after it (the prior month-end balance, the first core month from BAL_AT_CONV), linked through core_conversion_xref.csv, with the region from he_lending_file_2009-2026.csv's property_county and county_region_map.csv: 5,264 payoffs in full (PIF); maturities and charge-offs leave the record without counting.
3. Recovered each first mortgage from the lending file's senior lien: its rate from the amortization identity on senior_lien_original_amount, senior_lien_term_months and senior_lien_balance after the payments from senior_lien_opened to senior_lien_balance_as_of (a blank term is the one of 360 and 180 months whose payment the reported payment carries; a second funded with the purchase carries senior_lien_note_rate_pct as filed), and its balance in every month on its schedule.
4. Took the posted 30 YR FIXED MORTGAGE rate's monthly average from posted_rate_sheets_2018-12_2026-11.csv, each sheet in effect until the next, and the base case's 30-year fixed rate from planning_cycle_2027_rates.xlsx for December 2026 to December 2027.
5. Fitted each loan-month's payoff probability by logistic regression on the stack's refinancing incentive, the blended rate of the first mortgage and the home equity loan at their balances less the posted 30-year rate a month earlier (piecewise linear, knots at -1, 0, 0.5, 1, 1.5 and 2 points), with a sine and cosine of the month and a marker for a first mortgage opened less than 24 months before: deviance 48,888.4, against 49,475.5 on the first mortgage's own rate, 49,294.9 with each lien against its own posted rate, 49,431.4 with the loan's own and the first's rates side by side and 52,394.5 on the loan's own note rate against the posted home equity rate.
6. Took curtailments at the trial balance's rate, PrincipalPaid above ScheduledPrincipal in ACTIVE months over the prior month-end balance: 0.165 per cent of the balance a month.
7. Ran the book from December 2026 through December 2027 on the base case, a payoff at the start-of-month balance and curtailments on the balance that survives the month, and summed 2027 by region: Muskegon and the North 39.2 million (about 40 to the nearest 10), the Lakeshore 23.9, Grand Rapids 18.5, Kalamazoo and Battle Creek 13.5; the pilot opens at Muskegon and the North and the Lakeshore comes second.
8. Counted each center's loans quoted a payoff per quarter from payoff_statement_log_2025-10_2026-11.csv, ISSUED and UPDATED statements by their Eastern issue date, a legacy number through the cross-reference, home equity lines and VOID requests out; added the home equity loan behind each MTG statement whose amount paid it as well as the credit union's first mortgage (the mortgage in first_mortgage_servicing_2026-11.csv, the loan at the same property_street and property_zip in the lending file) and the home equity loans in payoff_statements_manual_2026-03.xlsx matched by property address; paid in full is LoanStatus PIF with a CloseDate on or before 2026-11-30.

## 4. Deliverable Answers

### he_payoff_pilot_2027.xlsx

1. Center to open the payoff-retention pilot on 4 January 2027: **Muskegon and the North**
2. Fixed-rate home equity principal its members will pay off in 2027: **$40 million** (nearest 10)
3. Center second: **The Lakeshore**
4. Fixed-rate home equity loans quoted a payoff, and of those paid in full by 30 November 2026, by center and quarter:
   - Grand Rapids, October to December 2025: **47** quoted, **39** paid in full
   - Grand Rapids, January to March 2026: **59** quoted, **49** paid in full
   - Grand Rapids, April to June 2026: **63** quoted, **57** paid in full
   - Grand Rapids, July to September 2026: **65** quoted, **49** paid in full
   - The Lakeshore, October to December 2025: **76** quoted, **71** paid in full
   - The Lakeshore, January to March 2026: **72** quoted, **61** paid in full
   - The Lakeshore, April to June 2026: **51** quoted, **45** paid in full
   - The Lakeshore, July to September 2026: **78** quoted, **67** paid in full
   - Kalamazoo and Battle Creek, October to December 2025: **140** quoted, **139** paid in full
   - Kalamazoo and Battle Creek, January to March 2026: **109** quoted, **103** paid in full
   - Kalamazoo and Battle Creek, April to June 2026: **92** quoted, **84** paid in full
   - Kalamazoo and Battle Creek, July to September 2026: **101** quoted, **97** paid in full
   - Muskegon and the North, October to December 2025: **48** quoted, **41** paid in full
   - Muskegon and the North, January to March 2026: **46** quoted, **36** paid in full
   - Muskegon and the North, April to June 2026: **48** quoted, **40** paid in full
   - Muskegon and the North, July to September 2026: **55** quoted, **41** paid in full

### payoff_quotes_by_center.png

1. One bar per quarter, October to December 2025 through July to September 2026, split by center, each segment labelled with its count of loans quoted as in answer 4 above.
