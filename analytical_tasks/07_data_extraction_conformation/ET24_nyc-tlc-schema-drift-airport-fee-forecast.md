# ET24 — Forecasting taxi airport-fee revenue from monthly Parquet drops: a column that changed case and a fee that changed price

| Field | Value |
|---|---|
| Domain | Transportation / airport ground-transport revenue / data lake engineering |
| Objective family | Forecasting & Predictive Modeling (with ingestion conformance) |
| Task shape | 02 · Forecast across many periods → one committed annual level |
| Core technique | Schema-drift-tolerant union (case-insensitive column mapping, type coercion) across monthly files; volume × rate decomposition across a tariff change; mandated seasonal forecast |
| Trap family (honest data) | Case-sensitive union nulls a column in some months; revenue forecast without separating the rate change; trips assigned by file month instead of timestamp |
| Primary sources | NYC TLC Trip Record Data (yellow taxi monthly Parquet), TLC data dictionary, taxi zone lookup, TLC fare notices |

## 1. The real-world project

An airport ground-transportation team budgets next year's revenue from the per-trip fee charged on yellow-taxi pickups at
JFK and LaGuardia. The data team ingests TLC's monthly Parquet files into a lake with a schema-on-read union. The
analyst's history showed several months with almost no airport-fee revenue and a strange step in early 2023; the
forecast came in well below what finance expected.

## 2. The business decision (one deterministic recommendation)

**What is the committed 2025 airport-fee revenue budget (sum of 12 monthly forecasts)?**

Rules (budget method):

* History: yellow taxi trips with pickup timestamp in 2022-01-01 … 2024-12-31 (assign by `tpep_pickup_datetime`, not by
  file; discard timestamps outside this range).
* Column conformance: map columns case-insensitively (`airport_fee` / `Airport_fee` are the same field); coerce numeric
  types before union.
* Volume = trips with `PULocationID` ∈ {132 (JFK), 138 (LaGuardia)} and positive `airport_fee`; revenue = Σ `airport_fee`
  over all rows (voids/disputes with negative amounts net out).
* Rate in effect = modal positive `airport_fee` in the latest history month (must agree with the TLC fare notice in the
  folder).
* Forecast trips for each month of 2025 = same month 2024 trips × (trips in last 12 months ÷ trips in the prior 12 months).
* Forecast revenue = forecast trips × rate in effect; budget = Σ 12 months, rounded to the nearest $1,000.

## 3. Why this gets overlooked in real projects

* Monthly files are produced over years by different pipeline versions; column-name case and dtypes drift. Spark/
  DuckDB/pandas unions by name are case-sensitive or type-strict by default — the column silently becomes null for some
  months, or the union fails and someone drops the column "temporarily".
* A tariff change is visible only as a level step in revenue; forecasting revenue directly blends two price regimes.
* Each file contains a few trips with timestamps from other months or years (device clocks); assigning by file name
  shifts trips across months.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–36 | `yellow_tripdata_2022-01.parquet` … `yellow_tripdata_2024-12.parquet` | Parquet | ~2.5–3.5M each | NYC TLC Trip Record Data | NYC Open Data terms (free use) | Trips |
| 37 | `taxi_zone_lookup.csv` | CSV | 265 | NYC TLC | NYC open data terms | Zone IDs (132 JFK, 138 LGA, 1 EWR) |
| 38 | `taxi_zones.zip` (shapefile) | SHP | 263 polygons | NYC TLC | Same | Optional map |
| 39 | `data_dictionary_trip_records_yellow.pdf` | PDF | — | NYC TLC | Same | Field definitions |
| 40 | `tlc_fare_notice_2022.pdf` | PDF | — | NYC TLC | Public | Fee/rate change dates |
| 41 | `tlc_monthly_indicators.csv` (aggregated industry data) | CSV | ~500 | NYC TLC | Same | Reconciliation of monthly trip counts |
| 42 | `budget_method.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Read each Parquet schema; build a case-insensitive column map; cast numerics; union.
2. Assign months from pickup timestamps; drop out-of-range.
3. Monthly airport volume and revenue for 36 months; reconcile trip totals to TLC monthly indicators.
4. Identify the rate in effect; compute the trailing-12 growth ratio; forecast 12 months; sum.
5. Contrast: case-sensitive union history; revenue-direct forecast.

## 6. The traps

**Trap A — case-sensitive union.** Months where the field is `Airport_fee` show zero revenue; trailing growth and seasonal
anchors collapse; budget falls sharply.

**Trap B — revenue forecast across the tariff change.** Mixing old and new fee levels understates the budget.

**Trap C — file-month assignment.** Small shifts, but they move the growth ratio near the boundary months.

**Trap D — using `airport_fee > 0` alone for volume.** Includes non-airport pickups with data errors or misses airport
pickups in months with the case issue.

## 7. Why the data is honest

TLC publishes exactly what the vendors' systems reported; the dictionary documents the fields, and the fare change is a
public, dated decision. Schema drift across years of files is a real ingestion reality.

## 8. Draft task prompt (prose)

> Finance needs a committed 2025 budget for the taxi airport fee, built the way our budget method describes from the TLC
> monthly files in the folder. Conform the files, build the 36-month history of airport pickups and fee revenue,
> forecast each month of 2025 and give me the budget. Deliver `airport_fee_forecast.xlsx` with the monthly history (trips,
> revenue, average fee), the growth ratio, the twelve monthly forecasts and the total, plus `airport_fee_history.png`
> showing monthly trips and revenue for 2022–2024 with the forecast year appended and the tariff change marked. On the
> workbook's first sheet, state the budget, the rate in effect, and what the budget would have been if the history had been
> built with a case-sensitive union.

## 9. Deliverables

* `airport_fee_forecast.xlsx`, `airport_fee_history.png`.

## 10. Where 25+ rubric criteria come from

* 12 monthly forecasts; 36 historical months (spot-check ~8); growth ratio; rate; budget; case-sensitive variant.

## 11. Golden-output checklist

* Case-insensitive union; timestamp months; volume × rate split; mandated forecast; budget stated.

## 12. Build notes (scope tuning)

* Inspect every file's schema (e.g. `pyarrow.parquet.read_schema`) and confirm which months carry `Airport_fee` vs
  `airport_fee`; if the case drift is absent in the chosen window, extend the window to include it.
* Confirm the fee amounts and effective dates from TLC's published notices.
