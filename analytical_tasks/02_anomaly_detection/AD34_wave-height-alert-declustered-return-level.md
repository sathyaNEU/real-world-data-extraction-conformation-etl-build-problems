# AD34 — "Once-a-year" sea states: hourly percentiles count one storm forty times

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Offshore wind and oil & gas marine operations setting weather-alert levels; insurers defining parametric triggers; any alert meant to fire "about once a year" on autocorrelated data |
| Domain | Marine operations / metocean |
| Task shape | 04 · Setting one dial (the significant-wave-height alert level at each of 4 buoys equal to the 1-year return level) |
| Core method | Peaks-over-threshold with runs declustering (independent storm peaks), generalized Pareto fit by maximum likelihood, return level for a 1-year return period using the peak rate; comparison with the empirical 99.99th percentile of hourly data |
| Analytical stump | An alert "exceeded once a year on average" is a statement about storm events, not hours. Hourly observations within a storm are highly dependent; percentile-of-hours thresholds are exceeded in clumps and fire several storms per year, and extrapolation from all hours misstates tail shape |
| Primary sources | NOAA National Data Buoy Center (NDBC) standard meteorological historical data |

## 1. The real-world situation

An offshore-wind construction contractor wants a "severe sea state" alert at four buoys that fires, on average, once per year, to trigger
vessel recall. A planner set each alert at the 99.99th percentile of hourly significant wave height (WVHT); in the first season, alerts fired
four to six distinct storms per buoy.

## 2. The decision (one deterministic recommendation)

**The alert level (m, one decimal) at each of the four buoys equal to the 1-year return level of declustered storm peaks.**

Rules (metocean memo):

* Data: NDBC standard meteorological files, 2008–2022, for the four stations in `stations.json`; hourly WVHT (values 99.00 = missing).
* Threshold u per station: the 98th percentile of valid hourly WVHT.
* Declustering: exceedances separated by ≥ 48 hours below u form separate clusters; keep the cluster maximum.
* GPD fit to (peak − u) by maximum likelihood; λ = peaks per year of valid record (years weighted by data completeness per memo).
* 1-year return level z = u + (σ/ξ)[(λ·1)^ξ − 1] (ξ ≠ 0).
* Validation: count distinct storms per year exceeding z in the record; report alongside the planner's percentile level and its storm count.

## 3. Why capable analysts get it wrong

* Percentiles are a natural way to state rarity, but per-hour rarity is not per-event rarity.
* Dependence within storms means exceedances arrive in clusters.
* The return-period formula needs the rate of independent peaks per year, not the number of exceeding hours.
* Missing data (buoy outages, often in storms) must enter the rate through the effective record length.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `<station>h2008.txt.gz` … `<station>h2022.txt.gz` (4 stations × 15 years) | Whitespace text | ~8.7k per file | NOAA NDBC historical data | U.S. Gov public domain | Hourly observations |
| 5 | `ndbc_measurement_descriptions.html` | HTML | — | NDBC | Public domain | Field definitions, missing codes |
| 6 | `stations.json` | JSON | 4 | Task author | — | Stations in scope |
| 7 | `station_metadata.csv` | CSV | 4 | NDBC station pages | Public domain | Depth, location |
| 8 | `metocean_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `planner_percentile_levels.xlsx` | XLSX | 4 | Task author | — | Current alert levels |
| 10 | `coles_2001_citation.pdf` | PDF | — | Cite | Cite | POT/GPD methods |
| 11 | `wvht_hourly_clean.parquet` | Parquet | ~520k | Derived | Public domain | Cleaned series |

## 5. Deterministic solution path

1. Parse files; clean missing codes; compute completeness per year.
2. Threshold u; decluster; peaks.
3. Fit GPD; λ; return level.
4. Validate storm counts; compare with percentile levels.

## 6. Wrong paths (method errors, not misreadings)

**A — hourly percentile.** Too many storms per year.

**B — GPD on all exceedance hours.** Dependence violates the model; rate wrong.

**C — λ from calendar years ignoring gaps.** Biased return level.

**D — annual maxima with 15 points.** Not the memo's method; unstable.

## 7. Why the stump is analytical, not semantic

Data, threshold, declustering and formula are specified. The trap is temporal dependence in extreme-value analysis.

## 8. Draft task prompt (prose)

> Set our once-a-year sea-state alert at each of the four buoys using the declustered peaks-over-threshold method in the metocean memo.
> Provide `return_levels.csv` (station: u, peaks, λ, σ, ξ, return level, storms per year above it, planner level and its storms per year),
> `peaks_over_threshold.png` (time series of peaks with u and the alert level), and a one-page `alert_levels.pdf`.

## 9. Deliverables

* `return_levels.csv`, `peaks_over_threshold.png`, `alert_levels.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 stations × (u, peaks, λ, σ, ξ, z, storm count) = 28; planner contrast; completeness handling.

## 11. Golden-output checklist

* Missing codes; threshold; 48-h declustering; MLE; rate with completeness; return level formula.

## 12. Build notes (scope tuning)

* Choose stations with ≥ 12 years of good data and at least one long storm-season outage.
* Confirm percentile levels yield ≥ 3 storms per year.
