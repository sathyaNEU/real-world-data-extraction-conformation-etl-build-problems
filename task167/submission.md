## Tags

**Domain:** General Statistics & Data Science (regression, classification and model diagnostics: a grant-making foundation's 2027 call reserve for its private fund commitments, each fund's call schedule read from the funds whose first year was financed like its own and validated on the funds that have passed their second year).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The Foundation should hold a call reserve of $450 million for 2027.** The funds committed before 1 January are expected to call $425 million in 2027, most of it the 2026 programme in its second year: twelve of its fourteen funds called less than 8 per cent of commitment in 2026, fees and a first investment, as 36 of the 172 earlier funds did in their first year before calling more than twice the others' share of commitment in their second. Not $350 million, the reserve from Takahashi-Alexander rates on the undrawn balance pooled over every earlier fund ($300 million from shares of commitment pooled the same way), which puts those funds' second-year calls low in every vintage left out of the fit. Not 2026's calls carried forward, which take the programme's first year as its pace.

## 2. Critical Components

1. Funds that called less than 8 per cent of commitment in their first year: **36 of the 172** earlier funds and **12 of the 14** programme funds.
2. Capital calls expected in 2027: **$425 million** (to the nearest $25 million).
3. By strategy: buyout **$175 million**, growth equity **$100 million**, venture capital **$75 million**, private credit **$75 million**.

## 3. Step-by-Step Solution

1. Joined investor_capital_activity_2016-04_2026-12.csv and legacy_administrator_notices_2006-2016.xlsx to fund_commitments_register.xlsx (the legacy file before 1 April 2016, settled notices only), and built each fund's calls gross of distributions (policy 2.3) by month of age from its first close (policy 2.4).
2. Split the funds on their first twelve months from first close: 36 earlier funds and 12 programme funds called less than 8 per cent of commitment, fees and a first investment, and no fund called between 8 and 11 per cent.
3. Left out one vintage at a time, the schedule pooled over every earlier fund put the light-first-year funds' second-year calls low in all 12 vintages, and their own schedule came within 1 per cent of those calls in total.
4. Fitted each class's schedule by month of age on the earlier funds, the light-first-year funds calling more than twice the others' share of commitment in their second year.
5. Applied each fund's class schedule to its 2027 ages, capped at its undrawn commitment, euro funds at 1.1326 (policy 2.5): $425 million expected.
6. Rounded up to the next $50 million (policy 2.2): a call reserve of $450 million.

## 4. Deliverable Answers

### call_reserve_2027.xlsx

1. Call reserve for 2027: $450 million.
2. Capital calls expected in 2027, $ million to the nearest 25: all funds 425; buyout 175; growth equity 100; venture capital 75; private credit 75.
3. Private-markets net asset value at 31 December 2026, $ million:
   - Buyout: 617.8
   - Growth equity: 242.2
   - Venture capital: 508.1
   - Private credit: 43.1
   - Euro funds: 185.7
   - Dollar funds: 1225.6
   - Vintages 2015 to 2018: 326.4
   - Vintages 2019 to 2022: 960.2
   - Total: 1411.2
4. Reserve account at 31 December 2026, $ million:
   - Qualifying assets: 161.0
   - Treasury bills among them: 88.6
   - Face value maturing January to March 2027: 32.0
   - Face value maturing April to June 2027: 15.0
   - Face value maturing July to September 2027: 25.0
   - Face value maturing October to December 2027: 18.0

### call_reserve_memo_2027.pdf

1. States the call reserve of $450 million.
2. Chart of the capital calls expected in 2027 by strategy, stacked to the $425 million total, with the $450 million reserve drawn across as a line.
