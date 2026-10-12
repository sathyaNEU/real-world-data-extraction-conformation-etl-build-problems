# task135: The Wrexford Trust, the 2027 growth share under the investment policy's volatility cap

## Tags

**Domain:** Quantitative Finance (volatility and derivatives pricing: a charity endowment's expected volatility at each growth share).
**Analytical objective:** Forecasting & Predictive Modeling (the portfolio's expected twelve-month volatility for 2027 at each step, against the policy's cap).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Set the 2027 growth share at 60 per cent: it is the largest of the policy's steps whose expected volatility stays inside the 10% cap.**

Measured where the holdings' prices are struck together, expected volatility is 9.0% to 9.7% at 60 per cent and 10.3% to 11.1% at 70 per cent. Not 70 per cent from a daily covariance scaled by the square root of 252 (9.4% at 70 per cent), which treats the Kestwick funds' noon prices as struck at the London close and misses the co-movement that lands a day apart. Not 80 per cent from an exponentially weighted daily estimate, which weights the calm last months against policy 4.3's equally weighted periods.

## 2. Critical Components

1. Expected volatility at 60 per cent growth, on weekly returns or on daily covariances with the one-day lead and lag: **9.0% to 9.7%**, inside the cap.
2. Expected volatility at 70 per cent growth on the same estimates: **10.3% to 11.1%**, over the cap.

## 3. Step-by-Step Solution

1. Built the mandate's daily time-weighted total return from `brackenfold_valuation_lots_2024-11_2026-11.csv` (both designations' lots, cash and accrued income), stripping the contributions and withdrawals in `brackenfold_capital_movements_2024-12_2026-11.csv` and carrying the demerger in `brackenfold_corporate_events_2024-12_2026-11.csv`, and each Kestwick fund's from its income-unit prices and distributions in `kestwick_charity_funds_prices_2024-11_2026-11.xlsx`: 505 daily returns per holding to the 30 November 2026 valuation (investment policy 4.2).
2. Read the pricing points in `kestwick_charity_funds_key_facts_2026.pdf` and `brackenfold_export_notes_2026-12-02.txt`: the funds are dealt at 12 noon from each market's latest prices, so the North American fund carries the previous New York close while the mandate is priced at the London close; the mandate's daily return correlates 0.20 with the North American fund's on the same day and 0.49 with its next-day return.
3. Combined the holdings at each step's policy weights (investment policy 2.2) and measured co-movement where the prices line up: weekly returns, Friday to Friday at 52 a year, give 9.0% at 60 per cent and 10.3% at 70 per cent; daily covariances with the one-day lead and lag added, at 252 a year, give 9.6% and 11.0%.
4. Compared each estimate with the cap before rounding (investment policy 3.4 and 4.4): 60 per cent is the largest step inside it; the daily covariance alone gives 9.4% at 70 per cent and wrongly clears it.
5. Estimated 2027 income under finance procedure 7.2 and 7.3: the mandate's dividends with ex-dividend dates in the twelve months to 30 November 2026 in `brackenfold_income_entitlements_by_lot_2025-11_2026-11.csv`, one amount per designation, security and event although the report repeats it on every tax lot, over the mandate's market value without accrued income (3.70%), and each fund's distributions per income unit over its 30 November price, at each step's weights of the portfolio's £32,908,401.
6. Took the open instalments in `wrexford_grant_instalments_2026-11-30.csv` of grants not withdrawn in `wrexford_grants_register_2026-11-30.csv` (procedure 7.4 and 7.5), paying core grants and first instalments on their due dates and later project instalments 35 to 70 days after, as every payment in `wrexford_grant_payments_2023-01_2026-11.csv` shows, euro at 1.1460: 2027 grant payments of £1,260,000.
7. Added the running costs total in `wrexford_budget_2027_draft_2026-11-24.xlsx`, £328,949 (fees are charged to capital under investment policy 5.1), and took off each step's income: the release runs from £147,000 at 20 per cent to £735,000 at 100 per cent, and income covers the grant payments up to 40 per cent.
8. Recommendation: set the 2027 growth share at 60 per cent.

## 4. Deliverable Answers

### growth_share_2027.xlsx

1. Largest growth share inside the 10% volatility cap: 60 per cent.
2. 2027 grant payments: £1,260,000.
3. 2027 investment income and capital release at each growth share, pounds to the nearest thousand:
   - 20 per cent: income £1,442,000, release £147,000
   - 30 per cent: income £1,368,000, release £221,000
   - 40 per cent: income £1,295,000, release £294,000
   - 50 per cent: income £1,221,000, release £368,000
   - 60 per cent: income £1,148,000, release £441,000
   - 70 per cent: income £1,074,000, release £515,000
   - 80 per cent: income £1,001,000, release £588,000
   - 90 per cent: income £927,000, release £662,000
   - 100 per cent: income £854,000, release £735,000

### income_cost_by_step_2027.svg

1. One bar per growth share from 20 to 100 per cent at its 2027 investment income, the figures above.
2. A line at the 2027 grant payments, £1,260,000.
3. A line at the grant payments plus running costs, £1,589,000.
4. Title naming 40 per cent: "2027 income covers the grant payments up to 40% growth".
