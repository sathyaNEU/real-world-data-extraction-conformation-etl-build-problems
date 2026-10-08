# DA44 — An annual mean from 8,760 hours is not 8,760 independent observations

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Confidence intervals on dashboard metrics computed from autocorrelated time series (daily KPIs, latency, energy use) where naive standard errors are far too small |
| Domain | Air quality / environmental compliance |
| Task shape | 10 · Scorecard against thresholds (12 monitoring stations → annual mean NO₂ with autocorrelation-robust intervals; certainly above, certainly below or undetermined relative to the 40 µg/m³ limit) |
| Core method | Annual mean of hourly concentrations with data-capture rules; standard error via effective sample size from the lag-1 autocorrelation of daily means (AR(1) approximation) or Newey–West on daily means per memo; classification against the limit |
| Analytical stump | Naive SE = SD ÷ √n with hourly n treats pollution hours as independent; intervals are an order of magnitude too narrow and declare stations "certainly compliant" when they are not. Pollution persists over days; the effective number of independent observations is much smaller |
| Primary sources | European Environment Agency (EEA) air quality e-reporting — validated hourly NO₂ data (E1a) |

## 1. The real-world situation

A city environment department must tell residents whether each monitoring station is above or below the annual NO₂ limit, with uncertainty
reflected. The draft reported 95% intervals of ±0.3 µg/m³ for every station and classified all twelve definitively. A statistician pointed
out that consecutive hours and days are strongly correlated.

## 2. The decision (one deterministic recommendation)

**The classification of each of 12 stations (certainly above, certainly below, undetermined) for the year, with the annual mean and an
autocorrelation-robust 95% interval.**

Rules (environment memo):

* Data: EEA validated hourly NO₂ (E1a) for the 12 stations and year in the memo; validity flag ≥ 1 and verification = verified.
* Data capture: ≥ 90% valid hours for inclusion; otherwise "insufficient data".
* Annual mean = mean of valid hourly values.
* Uncertainty: daily means (days with ≥ 18 valid hours); lag-1 autocorrelation ρ of daily means; n_eff = n_days × (1 − ρ) ÷ (1 + ρ);
  SE = SD(daily means) ÷ √n_eff; interval = mean ± 1.96 SE.
* Classification: lower bound > 40 → certainly above; upper bound < 40 → certainly below; else undetermined.
* Report naive hourly SE for contrast.

## 3. Why capable analysts get it wrong

* Large n invites tiny standard errors.
* Weather regimes create multi-day persistence.
* Hourly autocorrelation is even stronger; using hours with an hourly AR(1) is not the memo's method.
* Data-capture rules affect which stations are reportable.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `<country>_8_<station>_<year>_timeseries.csv` (12 stations) | CSV | ~8.8k each | EEA Air Quality download service (E1a) | CC BY 4.0 (EEA standard reuse) | Hourly NO₂ with validity/verification |
| 2 | `station_metadata.csv` | CSV | 12 | EEA | CC BY 4.0 | Station type, location |
| 3 | `eea_e1a_data_dictionary.pdf` | PDF | — | EEA | CC BY 4.0 | Flags |
| 4 | `aaq_directive_annex_xi_citation.pdf` | PDF | — | Directive 2008/50/EC (cite) | EU reuse | Limit value |
| 5 | `environment_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `draft_station_intervals.xlsx` | XLSX | 12 | Task author | — | Naive intervals |
| 7 | `effective_sample_size_reference.pdf` | PDF | — | Cite (Bayley & Hammersley / Wilks) | Cite | n_eff |
| 8 | `daily_means.parquet` | Parquet | ~4.4k | Derived | CC BY 4.0 | Convenience |

## 5. Deterministic solution path

1. Filter valid, verified hours; data capture per station.
2. Annual means; daily means; ρ, n_eff, SE, intervals.
3. Classification; contrast with naive intervals.

## 6. Wrong paths (method errors, not misreadings)

**A — hourly SE.** Overconfident classifications.

**B — daily SE without autocorrelation.** Still too narrow.

**C — including unverified data.** Different means.

**D — ignoring data capture.** Unreportable stations classified.

## 7. Why the stump is analytical, not semantic

The flags, rules and n_eff formula are specified. The trap is dependence in time series inflating precision.

## 8. Draft task prompt (prose)

> Which stations are above, below or not clearly on either side of the NO₂ limit this year? Compute annual means with the autocorrelation-aware
> intervals in the environment memo. Provide `station_scorecard.csv` (station: capture, mean, ρ, n_eff, interval, naive interval, class),
> `station_intervals.png`, and a one-page `compliance_statement.pdf`.

## 9. Deliverables

* `station_scorecard.csv`, `station_intervals.png`, `compliance_statement.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 stations × (mean, interval, class) = 36; capture exclusions; naive contrast.

## 11. Golden-output checklist

* Flags; capture; daily means; ρ; n_eff; classification.

## 12. Build notes (scope tuning)

* Choose stations with means between 35 and 45 so classification depends on interval width.
