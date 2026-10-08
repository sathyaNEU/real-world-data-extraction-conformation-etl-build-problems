# FC34 — From business applications to new employers: conversion happens over two years, not in the same quarter

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Small-business platforms (payroll, payments, banking) forecasting new-customer formation from leading application data |
| Domain | Fintech / B2B go-to-market planning |
| Task shape | 03 · Bridge between two totals (naive "applications × conversion" forecast → lag-convolution forecast for the next four quarters) |
| Core method | Distributed-lag conversion: formations in quarter q = Σ_k applications(q − k) × c_k, with lag weights from historical cohorts' 4- and 8-quarter formation rates, by application type |
| Analytical stump | Multiplying the latest quarter's applications by an average conversion rate puts all formations in the wrong quarters and ignores that the mix of high- vs low-propensity applications shifts; surges of low-propensity filings barely become employers |
| Primary sources | U.S. Census Bureau Business Formation Statistics (BFS) |

## 1. The real-world situation

A payroll software company sizes its small-business sales team on how many **new employer businesses** will start payroll in each of
the next four quarters in its states. The analyst multiplied the latest quarter's business applications by the long-run share that
become employers. Applications had surged — mostly low-propensity filings — and the hiring plan overshot.

## 2. The decision (one deterministic recommendation)

**Forecast new employer business formations for each of the next four quarters (sum over the company's states) and the committed
annual total.**

Rules (go-to-market memo):

* BFS quarterly series by state: high-propensity applications (HBA), other applications (BA − HBA), and formation rates for
  application cohorts: share forming within 4 quarters and within 8 quarters (from the BF4Q/BF8Q series ÷ applications), by type,
  averaged over application cohorts 2012Q1–2018Q4.
* Lag weights: quarters 1–4 share the 4-quarter rate equally; quarters 5–8 share (8-quarter rate − 4-quarter rate) equally.
* Forecast formations in future quarter q = Σ over k = 1…8 Σ types applications_type(q − k) × weight_type(k), using actual
  applications through the latest quarter (future applications for k beyond observed are not needed for the next 4 quarters except
  where q − k is in the future — use the latest four quarters' average for those).
* Report the bridge: naive (latest-quarter applications × 8-quarter rate × 4) → timing correction → mix correction → forecast.

## 3. Why capable analysts get it wrong

* Conversion rates are published as cumulative shares, which invites "applications × rate" in a single period.
* The application mix matters: high-propensity applications convert many times more often.
* Formations from today's applications arrive over two years; formations next quarter come mostly from applications made
  quarters ago.
* Surges in low-propensity applications (e.g. online sellers) dominate headline application counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `bfs_quarterly_state.csv` | CSV | ~50k | U.S. Census BFS | Public domain | Applications and formations by state |
| 2 | `bfs_monthly_state.csv` | CSV | ~150k | U.S. Census BFS | Public domain | Monthly applications |
| 3 | `bfs_quarterly_naics_sector.csv` | CSV | ~30k | U.S. Census BFS | Public domain | Sector context |
| 4 | `bfs_methodology.pdf` | PDF | — | U.S. Census | Public domain | Definitions of HBA, BF4Q/BF8Q |
| 5 | `bfs_api_response_sample.json` | JSON | ~1k | Census API | Public domain | Field format |
| 6 | `company_states.json` | JSON | ~12 | Task author | — | Scope |
| 7 | `go_to_market_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `analyst_naive_forecast.xlsx` | XLSX | ~10 | Task author | — | Naive plan |
| 9 | `qcew_new_establishments_context.csv` | CSV | ~1k | BLS Business Employment Dynamics | Public domain | Cross-check |
| 10 | `bfs_release_calendar.csv` | CSV | ~50 | Census | Public domain | Data availability |

## 5. Deterministic solution path

1. Compute type-specific 4- and 8-quarter rates from the 2012–2018 cohorts; build lag weights.
2. Convolve historical applications to forecast the next four quarters; sum over states.
3. Build the bridge from the naive forecast; annual total.
4. Back-test the method on a historical origin (e.g. 2019Q4) for credibility.

## 6. Wrong paths (method errors, not misreadings)

**A — applications × rate, same quarter.** Timing and mix wrong; overshoots after surges.

**B — single conversion rate for all types.** Mix shift ignored.

**C — using recent cohorts whose 8-quarter outcomes are incomplete.** Biased rates.

**D — monthly seasonal noise treated as trend.** Over-reacts.

## 7. Why the stump is analytical, not semantic

Definitions are published by the Census Bureau and restated in the memo. The trap is temporal and compositional modelling of a
conversion process.

## 8. Draft task prompt (prose)

> Size next year's small-business sales hiring from a forecast of new employer businesses in our states, quarter by quarter, using
> the BFS data and the conversion method in the go-to-market memo. Provide `formation_forecast.csv` (quarter × state: contributions
> by lag and type, total), `formation_bridge.png` walking from the naive estimate to our forecast, and a one-page `hiring_basis.pdf`
> with the four quarterly forecasts and the annual total.

## 9. Deliverables

* `formation_forecast.csv`, `formation_bridge.png`, `hiring_basis.pdf`.

## 10. Where 25+ rubric criteria come from

* Type-specific rates (4); 8 lag weights per type; 4 quarterly totals; annual total; bridge bars; back-test error.

## 11. Golden-output checklist

* Cohort window; lag weights; convolution; mix separation; bridge reconciles.

## 12. Build notes (scope tuning)

* Choose states and an origin after an application surge (e.g. 2021) so the naive forecast overshoots by > 20%.
* Verify the BFS formation series' cohort definitions (application quarter basis) in the methodology.
