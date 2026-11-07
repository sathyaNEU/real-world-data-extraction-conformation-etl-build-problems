## Tags

**Domain:** Quantitative Finance (portfolio construction and risk: a systematic equity desk placing new capital with one of its backtested strategies, each sized by the alpha it keeps at that capital).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Give the GBP 400 million to UK Mid Cap Value, which keeps GBP 8 million of alpha a year at that size, GBP 2 million more than UK Large Cap Quality, the runner-up.** Each strategy's gross alpha is netted of the shortfall its twelve months of rebalances would pay at GBP 400 million, priced on the desk's own orders at each trade's share of the stock's daily traded value. Not UK Smaller Companies Momentum: its GBP 20 million of gross alpha is the largest, but at GBP 400 million its month-end trades take a large share of each small cap's day, and it keeps GBP 5 million.

## 2. Critical Components

1. The desk's 2025 and 2026 orders cost more the larger their share of the stock's 20-session daily traded value: shortfall rises with the square root of participation, times the stock's daily volatility.
2. At GBP 400 million the rebalances of December 2025 to November 2026 trade GBP 1211 million (UK Smaller Companies Momentum), GBP 524 million (UK Mid Cap Value) and GBP 485 million (UK Large Cap Quality).
3. Alpha kept a year at GBP 400 million: UK Smaller Companies Momentum **GBP 5 million** of 20 gross; UK Mid Cap Value **GBP 8 million** of 12 gross; UK Large Cap Quality **GBP 6 million** of 7 gross.

## 3. Step-by-Step Solution

1. Conformed the desk's orders: kept each execution id once from oms_fills_2025-2026.csv, read pounds fills as pence times 100, merged each BACKUP-RECOVERY order into the terminated original it continues (same account, stock, side and London date, the original's unfilled quantity), and measured each order's shortfall from its arrival mid, cost positive (TCA standard sections 1 and 2).
2. Gave each order its participation, value at arrival over the 20-session average of close times volume in lse_daily_market_data_2025-2026.parquet, and the 60-session daily volatility, skipping each consolidation day in wealdmoor_security_master_2026-11-30.csv (TCA standard section 3).
3. Fitted, band by band, shortfall on daily volatility times the square root of participation by least squares over the band's orders (IC-07 section 2: the desk's executions in the candidate's index band).
4. Took each candidate's rebalances from 1 December 2025 to 30 November 2026 in backtest_rebalance_trades_2025-2026.csv, joined ISIN to SEDOL, scaled each traded weight to GBP 400 million and priced it on the fitted curve at its participation on the rebalance date (IC-07 section 2).
5. Took each strategy's annualised gross alpha 2015 to 2026 from research_backtests_2027_candidates.xlsx times GBP 400 million and subtracted the cost.
6. Recommended UK Mid Cap Value, GBP 2 million ahead of UK Large Cap Quality.
7. For the workbook, gave each live strategy its orders through the dated trading account register (WM-DYN-01 is UK Dynamic to 30 June 2026 and the Severnvale transition from 17 August; WM-DYN-02 UK Dynamic from 1 July), then the value-weighted shortfall by quarter of 2026 and the value traded, filled quantity at the average fill price, by half year.

## 4. Deliverable Answers

### capital_allocation_2027.pptx

1. Recommendation: give the GBP 400 million to UK Mid Cap Value.
2. Runner-up: UK Large Cap Quality.
3. Difference between them: GBP 2 million a year.
4. Alpha each strategy keeps a year at GBP 400 million, whole GBP million:
   - UK Smaller Companies Momentum: 5
   - UK Mid Cap Value: 8
   - UK Large Cap Quality: 6
5. Gross alpha a year at GBP 400 million, whole GBP million:
   - UK Smaller Companies Momentum: 20
   - UK Mid Cap Value: 12
   - UK Large Cap Quality: 7
6. Chart on slide 1: each strategy's gross alpha beside the alpha it keeps, both in GBP million, UK Mid Cap Value's kept alpha the tallest.

### strategy_capacity_2027.xlsx

1. Implementation shortfall by quarter of 2026, basis points to one decimal:
   - UK Equity Income: Q1 29.3, Q2 35.1, Q3 19.2, Q4 15.1
   - UK Mid Cap Growth: Q1 30.0, Q2 31.0, Q3 31.3, Q4 32.5
   - UK Smaller Companies: Q1 59.0, Q2 61.4, Q3 59.8, Q4 59.7
   - UK Dynamic: Q1 38.8, Q2 35.4, Q3 32.1, Q4 32.7
2. Value traded by half of 2026, whole GBP million:
   - UK Equity Income: H1 815, H2 463
   - UK Mid Cap Growth: H1 171, H2 147
   - UK Smaller Companies: H1 69, H2 62
   - UK Dynamic: H1 620, H2 514
