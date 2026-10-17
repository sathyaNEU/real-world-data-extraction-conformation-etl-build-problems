## Tags

**Domain:** Economics & Econometrics (forecasting and forecast evaluation: a statistical office's first estimate of quarterly GDP growth).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The Statistics Office's advance estimate will show real GDP growth of 2.8% at an annualised rate in the June quarter of 2026.**
Quarterly growth is 0.69%, with business inventories, each industry's book-value stocks revalued over its own stockholding period at both quarter ends, taking 0.43 percentage points off. Not each industry's book value over its month-end price index, which reads the rise in import prices inside the stockholding period as a fall in the volume of stocks bought before it; not the quarter's average index, which reads it the other way; not a two-month stockholding period for every industry, which ignores each industry's own stock-to-sales ratio.

## 2. Critical Components

1. The change in business inventories at 2025 prices in the June quarter is **-19 million dollars**, after the March quarter's published **534 million**: a contribution of **-0.43** percentage points.
2. Goods exports contribute **+0.67** and goods imports **+0.39** percentage points.
3. GDP grows **0.69%** on the March quarter.

## 3. Step-by-Step Solution

1. Took the June-quarter estimates of the ten lines TBS's bulletin does not feed, with their contributions, and the March-quarter base from tarbert_gdp_tracker_2026q2.xlsx: March-quarter GDP is 129,210 million dollars.
2. Rebased the export and import price indexes in so_price_indexes_2026-06.xlsx from 2019 to their 2025 average and divided the seasonally adjusted April to June values by SITC section in tbs_merchandise_trade_business_stocks_2026-06.pdf by them (user guide, sources and price measures): goods exports 30,881.1 and imports 27,116.3 million dollars at 2025 prices, against the March quarter's 30,021 and 27,618.
3. For each of the bulletin's eight industries, divided the end-March and end-June book value by the average of the industry's input price index, rebased to 2025, over the months its stock-to-sales ratio covers at that date, counted back from the month end: the change in business inventories is -19 million dollars at 2025 prices.
4. Rebuilt every quarter from 2019Q2 to 2026Q1 the same way from tbs_portal_monthly_2019-01_2026-05.csv: it comes within 9.9 million dollars root mean square of the Office's latest estimates of non-farm business inventories, the 25 June release in so_realtime_gdp_database.csv.
5. Took each line's change over March-quarter GDP (user guide, contributions to growth), summed the thirteen contributions to 0.69% and compounded to an annual rate (user guide, the headline): 2.8%.

## 4. Deliverable Answers

### gdp_preview_2026q2.pdf

1. The call, in the headline and the first sentence: real GDP growth of 2.8% at an annualised rate, 0.69% on the March quarter, in the June quarter of 2026.
2. A chart of each quarter's growth from the June quarter 2023 to the March quarter 2026 in its advance estimate and in the latest estimates, and the thirteen contributions.

### gdp_preview_2026q2_tables.xlsx

1. The revision from the advance estimate to the latest estimate of annualised growth, percentage points:
   - September quarter 2025: +0.5
   - December quarter 2025: +0.6
   - March quarter 2026: +1.2
2. Over the twelve quarters from June 2023 to March 2026: mean revision +0.34, mean absolute revision 0.58.
3. The change in the value of coal and of LNG shipped in the June quarter of 2026 on the June quarter of 2025, millions of dollars:
   - Japan: coal +174.5, LNG +680.7
   - China: coal +116.9, LNG +262.8
   - Korea: coal -23.5, LNG +91.2
   - India: coal +72.9, LNG +166.8
   - Taiwan: coal -15.3, LNG +265.3
   - The five markets: coal +325.5, LNG +1,466.8
