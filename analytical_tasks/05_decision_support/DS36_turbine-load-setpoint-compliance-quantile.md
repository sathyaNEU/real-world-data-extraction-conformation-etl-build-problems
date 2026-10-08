# DS36 — How hard to run the gas turbine: keep the 95th-percentile NOx under the permit, not the average

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Operating as close as possible to a constraint that must hold with high probability (SLA latency at peak throughput, error budgets at maximum batch size) |
| Domain | Power generation / environmental compliance |
| Task shape | 04 · Setting one dial (the maximum turbine energy yield setpoint by ambient-temperature band that keeps hourly NOx ≤ 70 mg/m³ with 95% probability) |
| Core method | Quantile regression of NOx on turbine energy yield (TEY) with ambient covariates (temperature, humidity, pressure) by temperature band; the setpoint is the largest TEY where the conditional 95th percentile is ≤ the limit; evaluate exceedance rates on the held-out year; compare with mean-regression-based setpoints |
| Analytical stump | Setting the operating point where *predicted mean* NOx equals the limit produces exceedances about half the time at that point. Compliance requires a conditional quantile; ambient conditions shift both mean and spread, so a single global setpoint is too loose in some conditions and too tight in others |
| Primary sources | UCI "Gas Turbine CO and NOx Emission Data Set" (Kaya et al., 2015 data from a combined-cycle plant in Turkey) |

## 1. The real-world situation

A combined-cycle plant wants to maximise output while complying with an hourly NOx limit. The operations engineer fitted a linear regression of NOx
on load and ambient variables and set the maximum load where predicted NOx equals the limit. The plant logged frequent exceedance warnings the
following year.

## 2. The decision (one deterministic recommendation)

**The TEY setpoint (MWh, to 0.5) for each of 4 ambient-temperature bands that keeps the conditional 95th percentile of NOx ≤ 70 mg/m³, and the
exceedance rate in the held-out year versus the mean-based setpoints.**

Rules (operations memo):

* Data: UCI gas turbine data 2011–2015 (hourly averages); training 2011–2014; evaluation 2015.
* Bands: ambient temperature < 10, 10–17, 17–24, ≥ 24 °C.
* Model per band: linear quantile regression NOx ~ TEY + AH + AP (τ = 0.95) on training data.
* Setpoint: largest TEY on a 0.5 MWh grid within the band's observed TEY range where the predicted 95th percentile at band-median AH and AP ≤ 70.
* Evaluation: in 2015, hours at or below the setpoint in each band; exceedance rate = share with NOx > 70.
* Contrast: OLS-based setpoints (predicted mean = 70).

## 3. Why capable analysts get it wrong

* Regression on means is the default.
* Constraints on outcomes need tail predictions.
* Heteroscedasticity: spread varies with ambient conditions and load.
* Out-of-time validation reveals drift (compressor fouling, tuning).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–5 | `gt_2011.csv` … `gt_2015.csv` | CSV | ~7.2k each (36,733 total) | UCI ML Repository (id 551) | CC BY 4.0 | Hourly sensor and emissions data |
| 6 | `gas_turbine_description.html` | HTML | — | UCI | CC BY 4.0 | Variables |
| 7 | `kaya_2019_citation.pdf` | PDF | — | Kaya, Tüfekci & Uzun, Turkish J. EE&CS 2019 (cite) | Cite | Dataset paper |
| 8 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `engineer_ols_setpoints.xlsx` | XLSX | 4 | Task author | — | Mean-based setpoints |
| 10 | `quantile_regression_reference.pdf` | PDF | — | Koenker (cite) | Cite | Method |

## 5. Deterministic solution path

1. Split by year; assign bands.
2. Fit quantile regressions; compute setpoints.
3. Evaluate on 2015; exceedance rates; contrast with OLS setpoints.

## 6. Wrong paths (method errors, not misreadings)

**A — mean-based setpoint.** ~50% exceedance at the operating point.

**B — single global setpoint.** Mis-sized by band.

**C — evaluating on training years.** Optimistic.

**D — quantile of unconditional NOx.** Ignores load dependence.

## 7. Why the stump is analytical, not semantic

Model, bands and grid are specified. The trap is enforcing a probabilistic constraint with a mean model.

## 8. Draft task prompt (prose)

> What maximum turbine output should we allow in each ambient band while staying within the NOx limit 95% of the time? Fit the quantile models in the
> operations memo and evaluate them on 2015. Provide `setpoints.csv` (band: quantile setpoint, OLS setpoint, 2015 exceedance for each),
> `nox_vs_tey.png`, and a one-page `operating_limits.pdf`.

## 9. Deliverables

* `setpoints.csv`, `nox_vs_tey.png`, `operating_limits.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 bands × (quantile setpoint, OLS setpoint, 2 exceedance rates) = 16; coefficients; overall rates; decision.

## 11. Golden-output checklist

* Year split; bands; τ = 0.95; grid search; evaluation.

## 12. Build notes (scope tuning)

* Confirm OLS setpoints yield ≥ 20% exceedance in at least two bands in 2015.
