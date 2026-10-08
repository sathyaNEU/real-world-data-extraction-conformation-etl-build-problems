# FC20 — Which sites will have the most injuries next year? Last year's worst sites are partly just unlucky

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Warehouse and fulfilment-network safety programmes targeting high-injury sites (large e-commerce and logistics operators) |
| Domain | Occupational safety / operations |
| Task shape | 01 · Ranked list under a cap (20 sites receive an ergonomics intervention) |
| Core method | Empirical-Bayes (Poisson–gamma) forecasts of next-year injury rates per site, shrinking each site's observed rate toward its industry mean by its exposure (hours); backtest of selection rules on prior years |
| Analytical stump | Selecting on one year's extreme observed rates picks many small sites whose rates regress toward the mean next year; forecasts must weigh each site's evidence by its exposure |
| Primary sources | OSHA Injury Tracking Application (ITA) Form 300A establishment data |

## 1. The real-world situation

A logistics operator benchmarks its network against public injury data and funds an **ergonomics intervention at 20 sites**
expected to have the highest injury rates next year. The safety analyst picked the 20 sites with the highest total recordable
case rate (TRCR) last year. In the following year, most of those sites' rates fell back sharply without any intervention, while
several large sites with persistently high rates were never selected.

## 2. The decision (one deterministic recommendation)

**Which 20 establishments are forecast to have the highest 2023 TRCR, and which is 21st?**

Rules (safety analytics memo):

* Establishments in NAICS 493 (warehousing and storage) and 4921/4922 (couriers) in the ITA 300A data with filings for 2021 and
  2022 and annual hours worked ≥ 50,000 in both years.
* TRCR = total recordable cases × 200,000 ÷ hours worked.
* Model: cases_i ~ Poisson(hours_i × λ_i ÷ 200,000), λ_i ~ Gamma with mean μ_g and variance τ²_g per NAICS group g, estimated by
  the method of moments on 2021–2022 pooled data (formula in memo).
* Forecast 2023 rate = posterior mean of λ_i given the site's 2021–2022 cases and hours.
* Rank by forecast; top 20 + 21st. Backtest: apply the same procedure with 2019–2020 → 2021 and report the realized 2021 TRCR of the
  chosen 20 vs the 20 chosen by raw 2020 TRCR.

## 3. Why capable analysts get it wrong

* "Worst last year" lists are intuitive and look objective.
* Small sites have volatile rates; extremes are disproportionately noise.
* Two years of data help only if combined with the right weights (exposure), not averaged as rates.
* Without a backtest, regression to the mean is invisible.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ITA_300A_Summary_Data_2019.csv` | CSV | ~300k | OSHA Injury Tracking Application | U.S. Gov public domain | 2019 establishment summaries |
| 2 | `ITA_300A_Summary_Data_2020.csv` | CSV | ~300k | OSHA | Public domain | 2020 |
| 3 | `ITA_300A_Summary_Data_2021.csv` | CSV | ~350k | OSHA | Public domain | 2021 |
| 4 | `ITA_300A_Summary_Data_2022.csv` | CSV | ~370k | OSHA | Public domain | 2022 |
| 5 | `ITA_300A_Summary_Data_2023.csv` | CSV | ~380k | OSHA | Public domain | Validation |
| 6 | `ita_data_dictionary.pdf` | PDF | — | OSHA | Public domain | Fields |
| 7 | `bls_soii_rates_naics_2022.xlsx` | XLSX | ~2k | BLS Survey of Occupational Injuries and Illnesses | Public domain | Industry benchmarks |
| 8 | `establishment_linkage_2019_2023.parquet` | Parquet | ~400k | Derived (EIN + address matching rule in memo) | Public domain | Site IDs across years |
| 9 | `empirical_bayes_poisson_gamma_reference.pdf` (citation) | PDF | — | Cite | Cite | Method |
| 10 | `safety_analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `last_years_raw_list.xlsx` | XLSX | 20 | Task author | — | Raw-rate selection |

## 5. Deterministic solution path

1. Link establishments across years; filter industry and hours.
2. Estimate μ_g, τ²_g by method of moments; compute posterior means for 2023 from 2021–2022 data.
3. Rank; top 20 + 21st.
4. Backtest both selection rules on 2019–2020 → 2021; report realized rates.

## 6. Wrong paths (method errors, not misreadings)

**A — raw last-year TRCR.** Small noisy sites dominate; realized next-year rates disappoint.

**B — average of two yearly rates.** Ignores exposure weighting.

**C — global shrinkage target.** Ignores industry differences.

**D — no backtest.** No evidence for either rule.

## 7. Why the stump is analytical, not semantic

The rate definition, eligibility and model are explicit. The error is selection on noisy extremes — regression to the mean — and
the cure is a statistical forecasting model.

## 8. Draft task prompt (prose)

> We fund an ergonomics intervention at the 20 sites expected to have the highest injury rates next year. Using the OSHA ITA files
> and the safety analytics memo in the folder, forecast each eligible site's 2023 rate with the shrinkage model and give me the 20
> sites and the 21st. Provide `injury_forecasts.csv` (site, NAICS group, hours and cases 2021–2022, raw rates, forecast, rank),
> `shrinkage_plot.png` showing raw 2022 rate against forecast with point size by hours, and a one-page `selection_memo.pdf` with the
> list and the backtest comparing both selection rules.

## 9. Deliverables

* `injury_forecasts.csv`, `shrinkage_plot.png`, `selection_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 sites + 21st; μ and τ² per group; forecasts for 5 named sites; backtest realized rates for both rules; overlap with the raw list.

## 11. Golden-output checklist

* Linkage; filters; moment estimates; posterior means; ranking; backtest.

## 12. Build notes (scope tuning)

* Document the establishment linkage rule (EIN + normalized address) and its match rate.
* Confirm the raw-rate list's realized next-year mean is clearly below the EB list's in the backtest.
