# FC26 — Monthly retail budgets: some months simply have more Saturdays (and Easter moves)

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Store-network monthly budgeting and comps (grocery and general-merchandise chains, flagship retail staffing) |
| Domain | Retail finance / workforce planning |
| Task shape | 02 · Forecast across many periods (12 monthly turnover forecasts → one committed peak-month staffing level) |
| Core method | Regression with month effects, day-of-week counts per month (trading-day regressors), a moving-Easter regressor and trend, estimated on original (unadjusted) data and projected on the known future calendar |
| Analytical stump | "Same month last year × growth" ignores that the composition of weekdays and the date of Easter change every year; for a weekend-heavy category a month with five Saturdays can be several percent bigger. Seasonally adjusted series already remove trading-day effects, so mixing them with original data double counts or misses them |
| Primary sources | Australian Bureau of Statistics Retail Trade (monthly turnover by state and industry) |

## 1. The real-world situation

A grocery chain in one Australian state sets monthly store labour budgets from a turnover forecast. Finance used last year's same
month × 4% growth. In months where the calendar shifted (an extra weekend day, Easter moving between March and April), the budget
was several percent off — and the peak-month roster was set for the wrong month.

## 2. The decision (one deterministic recommendation)

**The committed peak-month staffing level = the largest of the 12 monthly turnover forecasts for the next fiscal year (July–June),
and which month it is.**

Rules (finance memo):

* Series: original (not seasonally adjusted) monthly turnover, the state's "Food retailing" industry, from the ABS Retail Trade
  release in the folder.
* Estimation window: July 2012 – June 2024, excluding March 2020 – December 2021.
* Model: ln(turnover_t) = month-of-year effects + Σ_{d=Mon..Sat} β_d × (count of weekday d in month t − count of Sundays) + η × Easter
  share (fraction of the 8 days before Easter Sunday falling in month t) + linear trend; OLS.
* Forecast July 2025 – June 2026 with the known calendar; exponentiate with the smearing factor (mean of exp residuals).
* Committed level = max monthly forecast (A$ million, one decimal) and its month.

## 3. Why capable analysts get it wrong

* Seasonal-naive budgeting is standard and works when calendars repeat — they do not.
* The weekday mix matters most for categories with strong weekend shopping; the effect is invisible in annual totals.
* Easter's date moves the pre-Easter shopping peak between March and April.
* ABS seasonally adjusted series are already trading-day adjusted; fitting trading-day terms on them, or combining them with
  original-series growth, mixes concepts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `850101.xlsx` (Table 1: turnover by state, original/SA/trend) | XLSX | ~500 months × series | ABS Retail Trade, Australia | CC BY 4.0 | National and state turnover |
| 2 | `850111.xlsx` (Table 11: by state and industry, original) | XLSX | ~500 × ~200 series | ABS | CC BY 4.0 | Food retailing by state |
| 3 | `850112.xlsx` (Table 12: SA by state and industry) | XLSX | same | ABS | CC BY 4.0 | SA series (decoy) |
| 4 | `abs_retail_series_long.parquet` | Parquet | ~100k | Derived | CC BY 4.0 | Long format |
| 5 | `abs_retail_trade_explanatory_notes.pdf` | PDF | — | ABS | CC BY 4.0 | Trading-day and Easter treatment |
| 6 | `calendar_2012_2026.csv` | CSV | ~5.5k days | Derived | — | Weekday counts |
| 7 | `easter_dates.json` | JSON | 15 | Public calendar | Public | Easter dates |
| 8 | `state_public_holidays_2012_2026.json` | JSON | ~200 | State government (public) | CC BY | Context |
| 9 | `finance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `finance_seasonal_naive_budget.xlsx` | XLSX | 12 | Task author | — | Current method |

## 5. Deterministic solution path

1. Extract the original series; build trading-day and Easter regressors; exclude the pandemic months.
2. Fit OLS; compute smearing factor.
3. Forecast the 12 months; identify the maximum; report.
4. Contrast with seasonal-naive × growth; quantify per-month differences explained by the calendar.

## 6. Wrong paths (method errors, not misreadings)

**A — seasonal naive.** Misses calendar shifts; wrong peak month or level.

**B — SA series with trading-day regressors.** Double-adjusts.

**C — no Easter regressor.** March/April misallocated.

**D — pandemic months kept.** Distorted seasonal and trend estimates.

## 7. Why the stump is analytical, not semantic

The series and model are specified. The trap is temporal composition — calendar effects that change between years — which a naive
seasonal method structurally cannot capture.

## 8. Draft task prompt (prose)

> Budget next fiscal year's store labour for our state's food retailing from the ABS turnover data, using the calendar-aware model
> in the finance memo. Give me the twelve monthly forecasts and the committed peak-month level. Provide `turnover_forecast.csv`
> (month: weekday counts, Easter share, forecast, seasonal-naive value, difference), `calendar_effects.png` showing each month's
> calendar contribution, and a one-page `staffing_memo.pdf` with the peak month and level and where the old method went wrong.

## 9. Deliverables

* `turnover_forecast.csv`, `calendar_effects.png`, `staffing_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 trading-day coefficients, Easter coefficient, 12 monthly forecasts, peak month and level, seasonal-naive contrasts.

## 11. Golden-output checklist

* Original series; correct regressors; exclusion window; smearing; max and month.

## 12. Build notes (scope tuning)

* Choose a state/industry with a visible weekend effect and a forecast year in which Easter or weekday counts shift the peak; confirm
  seasonal naive picks a different peak month or a level > 3% off.
* Cite the ABS release month used; ABS revises original series.
