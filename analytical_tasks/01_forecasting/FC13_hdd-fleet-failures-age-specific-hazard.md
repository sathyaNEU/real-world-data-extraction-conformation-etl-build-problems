# FC13 — Spare drives for next quarter: the fleet is ageing into the steep part of the bathtub

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Data-centre hardware reliability and spares provisioning (hyperscalers, storage providers; the well-known 3 TB drive failure wave) |
| Domain | Infrastructure operations / reliability engineering |
| Task shape | 02 · Forecast across many periods (13 weekly failure forecasts → one committed spares level) |
| Core method | Age-specific failure hazards per drive model from drive-days of exposure, projected onto next quarter's age distribution (ageing cohorts + planned deployments, minus planned retirements); Poisson quantile for the committed level |
| Analytical stump | A single annualized failure rate times today's drive count ignores that hazard depends on age; a large cohort crossing into wear-out (or a large new deployment in infant mortality) changes failures far more than headcount does. Exposure must be drive-days by age, and retirements are censoring, not failures |
| Primary sources | Backblaze Drive Stats daily data (quarterly archives) |

## 1. The real-world situation

A storage provider orders spare drives quarterly. Ops forecast next quarter's failures as last year's annualized failure rate
(AFR) per model × current drive count ÷ 4, and ordered spares at that level plus 10%. Two quarters in a row they ran out:
a large purchase of one model from three years earlier was entering the age at which that model's failures climb.

## 2. The decision (one deterministic recommendation)

**The committed spare-drive level for Q1 2025: the 90th percentile of total fleet failures in the quarter.**

Rules (reliability memo):

* Data: daily drive records for 2024-01-01 … 2024-12-31 (one row per drive-day; `failure = 1` on a drive's failure day).
* Drive age = days since the drive's first appearance in the data (drives present on 2024-01-01 use the first appearance in the
  2013–2023 archives supplied).
* Hazard per model × age band (bands of 6 months): failures ÷ drive-days in that band during 2024. Bands with < 50,000 drive-days
  pool with the adjacent older band.
* Q1 2025 exposure: every drive alive on 2024-12-31 ages day by day through the quarter (no retirements unless listed in
  `planned_retirements.csv`); planned deployments in `planned_deployments.csv` enter at age 0 on their dates.
* Expected failures per week = Σ (drive-days by model × age band in that week × hazard). Total quarterly mean λ = Σ weeks.
* Committed level = smallest k with Poisson(λ) CDF ≥ 0.90.

## 3. Why capable analysts get it wrong

* AFR is a single published number per model, so it is used as if hazard were constant over life.
* Dividing failures by drive count (not drive-days) mis-states exposure when drives enter or leave mid-year.
* Retired drives disappear from the data; treating disappearance as failure, or ignoring it in exposure, biases hazards.
* Ageing is deterministic and known — the forecast should use it.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `data_Q1_2024.zip` … `data_Q4_2024.zip` (daily CSVs) | CSV (zipped) | ~22–25M rows per quarter | Backblaze Drive Stats | Free use with attribution (Backblaze terms; may not be sold) | Drive-days, failures, model |
| 5 | `drive_first_seen_2013_2023.parquet` | Parquet | ~400k drives | Derived from Backblaze archives | Same | Age anchors |
| 6 | `drive_stats_2024_daily_model_summary.parquet` | Parquet | ~50k | Derived | Same | Model × day counts |
| 7 | `backblaze_drive_stats_methodology.pdf` | PDF | — | Backblaze blog/reports | Same | AFR formula, retirement notes |
| 8 | `planned_deployments.csv` | CSV | ~20 | Task author | — | New drives by model and date |
| 9 | `planned_retirements.csv` | CSV | ~10 | Task author | — | Retirements |
| 10 | `reliability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `ops_afr_forecast.xlsx` | XLSX | ~30 | Task author | — | The flat-AFR forecast |
| 12 | `smart_attribute_reference.json` | JSON | ~50 | Public SMART references | Public | Context |

## 5. Deterministic solution path

1. Build drive-level age; compute drive-days and failures per model × age band in 2024; pool sparse bands.
2. Project each surviving drive's daily age through Q1 2025; add deployments, remove retirements.
3. Weekly expected failures; quarterly λ; Poisson 90th percentile.
4. Compare with the flat-AFR forecast; attribute the difference by model.

## 6. Wrong paths (method errors, not misreadings)

**A — flat AFR × drive count.** Misses wear-out of the ageing cohort; spares short.

**B — failures ÷ drive count.** Exposure wrong for models with mid-year deployments.

**C — retirements as failures.** Inflated hazards; spares over-ordered.

**D — mean instead of P90.** Stock-outs in half of quarters.

## 7. Why the stump is analytical, not semantic

Failures, ages and plans are explicit. The error is a constant-hazard model applied to an age-structured population — a
reliability-modelling mistake.

## 8. Draft task prompt (prose)

> We need the committed spare-drive level for Q1 2025: enough to cover total fleet failures in nine quarters out of ten, using
> the 2024 drive data and the reliability memo in the folder. Provide `weekly_failure_forecast.csv` (13 weeks × model: drive-days by
> age band, expected failures), `hazard_by_age.png` showing failure rate against age for the five largest models with the fleet's
> Q1 age distribution overlaid, and a one-page `spares_memo.pdf` with the committed level, the mean, and the shortfall the flat-AFR
> method would have produced.

## 9. Deliverables

* `weekly_failure_forecast.csv`, `hazard_by_age.png`, `spares_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 13 weekly totals; λ; committed level; hazards for 2–3 model × age cells; model attribution of the difference; flat-AFR contrast.

## 11. Golden-output checklist

* Drive-day exposure; age bands with pooling; daily ageing; deployments/retirements; Poisson P90.

## 12. Build notes (scope tuning)

* Choose the deployments/retirements so they are realistic (based on Backblaze's published fleet changes) and confirm the flat-AFR
  forecast is short by ≥ 15%.
* Document how "first seen" is computed when a drive's history starts before the earliest archive.
