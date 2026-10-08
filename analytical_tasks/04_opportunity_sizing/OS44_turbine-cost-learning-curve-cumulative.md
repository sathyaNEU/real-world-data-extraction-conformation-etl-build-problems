# OS44 — Cost-down from scale: learning curves run on cumulative volume, not on calendar years

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Manufacturing cost-down forecasts (consumer electronics, batteries, solar) where unit cost falls with cumulative production (Wright's law) |
| Domain | Wind energy manufacturing |
| Task shape | 13 · Scenarios and the flip point (deployment scenarios × learning rate uncertainty → turbine price in 2030; the contract price floor accepted and the deployment level at which it breaks) |
| Core method | Fit log(real turbine price) = a + b log(cumulative installed capacity) on historical data (excluding the memo's commodity-shock years or including a commodity index control); learning rate LR = 1 − 2^b; project price at cumulative capacity under scenarios; compare with a time-trend fit |
| Analytical stump | Fitting price against time extrapolates a rate of decline that depends on how fast deployment grew historically; if deployment slows, cost declines slow too. Price data also include commodity and supply-chain shocks (2021–2022) that are not learning. The cumulative-volume model with controls gives scenario-consistent forecasts |
| Primary sources | LBNL Land-Based Wind Market Report data (turbine transaction prices, installed capacity); U.S. BLS producer price index for steel (control) |

## 1. The real-world situation

A component supplier negotiates a long-term contract with a turbine maker that includes a price floor for 2030. The supplier's analyst
extrapolated a time trend of turbine prices (−3% per year) to 2030 and accepted a floor near that level. A strategist argued that U.S. deployment
is expected to slow, which would slow learning.

## 2. The decision (one deterministic recommendation)

**Accept or reject the proposed 2030 price floor ($/kW) under the central deployment scenario, and the cumulative capacity at which the forecast
price equals the floor.**

Rules (strategy memo):

* Data: LBNL turbine price index ($/kW, real) by year 2000–2023; cumulative U.S. (or global per memo) installed wind capacity by year.
* Model: OLS log(price) = a + b log(cumulative capacity) + c log(steel PPI real); fit 2000–2023.
* Learning rate LR = 1 − 2^b.
* Scenarios: cumulative capacity 2030 under low/central/high deployment (`deployment_scenarios.json`); steel PPI at its 2010–2023 average.
* Forecast price 2030 per scenario; accept the floor if forecast (central) ≥ floor + 5% margin.
* Flip point: cumulative capacity where forecast = floor.
* Report the time-trend extrapolation for contrast.

## 3. Why capable analysts get it wrong

* Time trends are easy to fit and communicate.
* Learning depends on cumulative experience, not elapsed time.
* Commodity shocks move prices independently of learning.
* Scenario consistency requires linking forecasts to deployment.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `land_based_wind_market_report_data_<year>.xlsx` | XLSX | ~30 sheets | LBNL (DOE) | Public (DOE/LBNL data; cite) | Turbine prices, capacity |
| 2 | `global_wind_capacity.csv` | CSV | ~25 | Task author (from public IRENA statistics; cite) | CC BY 4.0 (IRENA terms; verify) | Cumulative capacity |
| 3 | `ppi_steel_mill_products.csv` | CSV | ~300 months | BLS PPI | Public domain | Commodity control |
| 4 | `deployment_scenarios.json` | JSON | 3 | Task author | — | Scenarios |
| 5 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `analyst_time_trend.xlsx` | XLSX | — | Task author | — | Naive forecast |
| 7 | `contract_terms.json` | JSON | — | Task author | — | Proposed floor |
| 8 | `wright_learning_curve_citation.pdf` | PDF | — | Cite | Cite | Method |

## 5. Deterministic solution path

1. Assemble price, cumulative capacity and PPI series; deflate.
2. Fit the log-log model with control; LR.
3. Scenario forecasts; accept/reject; flip point.
4. Contrast with the time trend.

## 6. Wrong paths (method errors, not misreadings)

**A — time trend.** Ignores deployment pace.

**B — no commodity control.** Shock years distort b.

**C — annual (not cumulative) capacity.** Wrong learning variable.

**D — nominal prices.** Inflation confounds.

## 7. Why the stump is analytical, not semantic

The model and scenarios are specified. The trap is the learning variable and confounding shocks.

## 8. Draft task prompt (prose)

> Should we accept the 2030 price floor in the contract? Forecast turbine prices with the learning-curve model in the strategy memo under the
> deployment scenarios. Provide `learning_forecast.csv` (scenario: cumulative capacity, forecast price; LR), `learning_curve.png`, and a one-page
> `price_floor_decision.pdf`.

## 9. Deliverables

* `learning_forecast.csv`, `learning_curve.png`, `price_floor_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Coefficients a, b, c; LR; 3 scenario forecasts; flip point; time-trend contrast; fitted values for 10 years.

## 11. Golden-output checklist

* Deflation; cumulative capacity; control; fit; scenarios; decision; flip point.

## 12. Build notes (scope tuning)

* Choose the floor so the time-trend method accepts and the learning-curve method rejects under the central scenario.
