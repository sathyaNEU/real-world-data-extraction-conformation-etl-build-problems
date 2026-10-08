# DS50 — Shifting compute to "green" hours: average carbon intensity is not what your extra load emits

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Carbon-aware computing at cloud providers (shifting flexible batch jobs in time), EV smart charging and demand flexibility programmes |
| Domain | Electricity / sustainability operations |
| Task shape | 07 · Grid of cells (season × hour of day → average and marginal emission factors; the daily scheduling window adopted for flexible batch compute) |
| Core method | Average emission factor (AEF) = total CO₂ ÷ consumption per hour from the grid operator's data; marginal emission factor (MEF) estimated by regressing hour-to-hour changes in total emissions on changes in consumption (Siler-Evans/Hawkes method) by season × hour-of-day bins; schedule 4 flexible hours per day in the hours with the lowest MEF; compare emissions avoided with an AEF-based schedule |
| Analytical stump | The hours with the cleanest average mix (e.g., nuclear and hydro dominant at night) are not necessarily the hours where an extra MWh is met by low-carbon sources; marginal response may come from gas or interconnector imports. Scheduling by average intensity can save little or even increase emissions; marginal factors drive the decision |
| Primary sources | RTE eCO2mix (French grid real-time and consolidated data: consumption, generation by source, CO₂ emissions and intensity) |

## 1. The real-world situation

A cloud provider's sustainability team schedules 4 hours per day of flexible batch compute in France to minimise emissions. The first policy used
the published average carbon intensity and picked the overnight hours. An energy analyst argued that the marginal generator differs from the average
mix and that savings should be computed on marginal emissions.

## 2. The decision (one deterministic recommendation)

**The 4-hour daily window by season (from contiguous windows) minimising expected marginal emissions of the batch load, and the annual tCO₂ difference
versus the AEF-based window for 20 MW of flexible load.**

Rules (sustainability memo):

* Data: eCO2mix consolidated data 2021–2023 (30-minute or hourly; aggregated to hourly): consumption, generation by source, exchanges, CO₂ emissions
  (as published by RTE, domestic generation basis).
* AEF_t = emissions ÷ consumption (published intensity as provided).
* MEF: for each season (DJF, MAM, JJA, SON) × hour bin, OLS of ΔE_t on ΔD_t (hour-to-hour changes); slope = MEF; bins with R² < 0.2 flagged.
* Windows: contiguous 4-hour windows starting on the hour; choose the minimum Σ MEF per season.
* Emissions for 20 MW over the year = Σ_days Σ_window hours 20 × MEF (and × AEF for contrast).
* Report AEF-chosen windows and their marginal emissions.

## 3. Why capable analysts get it wrong

* Average intensity is the published, intuitive metric.
* Decisions about incremental load change marginal, not average, emissions.
* Imports and exports affect the marginal response; the memo uses domestic emissions per RTE convention (documented limitation).
* Seasonal and hourly heterogeneity matter.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `eCO2mix_RTE_Annuel-Definitif_<yyyy>.zip` (2021–2023) | XLS/CSV inside ZIP | ~17.5k records per year | RTE eCO2mix | Licence Ouverte / Etalab 2.0 | Consumption, generation, CO₂ |
| 2 | `eco2mix_documentation.pdf` | PDF | — | RTE | Licence Ouverte | Definitions, emission factors |
| 3 | `sustainability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 4 | `aef_schedule.xlsx` | XLSX | 4 seasons | Task author | — | Current policy |
| 5 | `siler_evans_2012_citation.pdf` | PDF | — | Siler-Evans, Azevedo & Morgan, ES&T 2012 (cite) | Cite | MEF method |
| 6 | `hourly_series.parquet` | Parquet | ~26k | Derived | Licence Ouverte | Cleaned hourly data |

## 5. Deterministic solution path

1. Aggregate to hourly; handle DST; compute AEF.
2. MEF regressions by season × hour; flags.
3. Window selection by MEF and by AEF; annual emissions; difference.

## 6. Wrong paths (method errors, not misreadings)

**A — AEF-based scheduling.** Wrong objective.

**B — MEF from levels instead of changes.** Confounded by baseload.

**C — one MEF for all hours.** Ignores timing differences.

**D — ignoring DST.** Hour bins misaligned.

## 7. Why the stump is analytical, not semantic

Data and estimators are specified. The trap is using an average factor for a marginal decision.

## 8. Draft task prompt (prose)

> When should our flexible batch compute run in France to cut emissions? Estimate marginal emission factors by season and hour and choose windows as
> the sustainability memo specifies, comparing with the average-intensity schedule. Provide `emission_factors.csv` (season × hour: AEF, MEF, R²),
> `aef_vs_mef.png`, and a one-page `scheduling_policy.pdf`.

## 9. Deliverables

* `emission_factors.csv`, `aef_vs_mef.png`, `scheduling_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 seasons' windows (MEF and AEF); MEF values for 24 hours in one season; annual emissions; difference; flags.

## 11. Golden-output checklist

* Aggregation; DST; Δ regressions; bins; window search; emissions.

## 12. Build notes (scope tuning)

* Confirm AEF and MEF windows differ in at least two seasons.
