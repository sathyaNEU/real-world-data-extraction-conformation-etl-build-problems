# AD28 — Building energy alarms: a cold month is not a faulty chiller

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Campus and data-centre facilities analytics at large tech companies and universities; energy-service companies doing measurement and verification |
| Domain | Facilities / building energy |
| Task shape | 17 · Periods around a change point (weeks after a suspected controls fault checked against a weather-normalised baseline; go/no-go on a recommissioning ticket and the savings it unlocks) |
| Core method | Change-point regression (3-parameter heating or cooling, 5-parameter) of daily energy on outdoor temperature, selected by the memo's rule; baseline fitted on a clean year; ASHRAE Guideline 14 CV(RMSE) and NMBE acceptance; weekly cumulative excess (CUSUM of residuals) |
| Analytical stump | Year-over-year or month-over-month comparisons fire whenever the weather differs; a baseline that includes the faulty months absorbs the fault. The anomaly is the residual against a weather-normalised model fitted on a clean period, and the run of positive residuals after the change |
| Primary sources | Building Data Genome Project 2 (BDG2) meter and weather data |

## 1. The real-world situation

A university energy office opens recommissioning tickets for buildings whose consumption runs persistently above expectation. Its current
alert compares each month with the same month last year; it fires on every cold snap and missed a building whose simultaneous heating and
cooling started in late spring. The office has budget for **one** ticket this cycle among five flagged buildings.

## 2. The decision (one deterministic recommendation)

**The building that receives the recommissioning ticket, the week its excess run began, and the annualised excess energy (kWh) that the
ticket would recover.**

Rules (energy office memo):

* Meters: electricity and chilled water (kWh-equivalent per memo conversion) for the five buildings in `flagged_buildings.csv`, site
  weather from BDG2.
* Daily totals; days with > 2 hours of missing meter data excluded.
* Baseline: calendar year 2016. Fit 2P, 3PC, 3PH and 5P change-point models to daily energy versus mean daily temperature; choose the
  model with the lowest CV(RMSE) among those whose parameters are physically signed (heating slope ≤ 0, cooling slope ≥ 0).
* Acceptance: CV(RMSE) ≤ 25% and |NMBE| ≤ 0.5% on daily data; buildings failing acceptance are ineligible.
* Monitoring 2017: residual r = actual − predicted; weekly sums; a run starts at the first week of ≥ 6 consecutive weeks with positive
  weekly residual exceeding 2 × the baseline weekly residual SD.
* Ticket: the eligible building with the largest annualised excess = mean daily residual in the run × 365.

## 3. Why capable analysts get it wrong

* Calendar comparisons confound weather; degree days or temperature regressions remove it.
* Fitting the model on the period being judged hides the fault.
* Linear models without change points misfit the flat base load and bias residuals at shoulder temperatures.
* Without acceptance criteria, poorly modelled buildings produce spurious residual runs.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `electricity_cleaned.csv` | CSV | ~17.5k hours × 1.5k meters | BDG2 (GitHub/Kaggle mirror) | CC BY 4.0 | Hourly electricity |
| 2 | `chilledwater_cleaned.csv` | CSV | ~17.5k × ~500 | BDG2 | CC BY 4.0 | Chilled water |
| 3 | `steam_cleaned.csv` | CSV | ~17.5k × ~370 | BDG2 | CC BY 4.0 | Steam (context) |
| 4 | `weather.csv` | CSV | ~330k | BDG2 | CC BY 4.0 | Site weather |
| 5 | `metadata.csv` | CSV | ~1.6k | BDG2 | CC BY 4.0 | Building attributes |
| 6 | `flagged_buildings.csv` | CSV | 5 | Task author | — | Candidates |
| 7 | `ashrae_guideline14_excerpt_citation.pdf` | PDF | — | Cite | Cite | Acceptance metrics |
| 8 | `energy_office_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `current_yoy_alerts.xlsx` | XLSX | ~60 | Task author | — | Existing alerts |
| 10 | `unit_conversions.json` | JSON | ~5 | Task author | — | Chilled water to kWh-equivalent |

## 5. Deterministic solution path

1. Aggregate to daily, apply missing-data rule, convert units.
2. Fit candidate change-point models on 2016 per building; choose; check acceptance.
3. Compute 2017 residuals; weekly sums; detect runs.
4. Annualised excess for eligible buildings; choose the ticket.

## 6. Wrong paths (method errors, not misreadings)

**A — year-over-year monthly comparison.** Weather-driven alerts.

**B — baseline including 2017.** Fault absorbed.

**C — linear regression without change points.** Biased residuals.

**D — skipping acceptance.** A poorly modelled building wins.

## 7. Why the stump is analytical, not semantic

Models, acceptance and run rules are explicit. The trap is weather confounding and baseline contamination.

## 8. Draft task prompt (prose)

> Which of the five flagged buildings gets this cycle's recommissioning ticket? Build the weather-normalised baselines in the energy office
> memo, check their accuracy, and find each building's run of excess use in 2017. Provide `building_models.csv` (building: model, parameters,
> CV(RMSE), NMBE, run start, annualised excess), `residual_runs.png` (weekly residuals per building with run marks), and a one-page
> `ticket_decision.pdf`.

## 9. Deliverables

* `building_models.csv`, `residual_runs.png`, `ticket_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 buildings × (model, CV(RMSE), NMBE, run start, excess) = 25; selection; contrast with year-over-year alerts.

## 11. Golden-output checklist

* Daily aggregation and exclusions; model selection rule; acceptance; residual runs; annualisation.

## 12. Build notes (scope tuning)

* Choose five meters including one with a mid-2017 shift and one with weather-driven year-over-year differences only.
* Confirm the year-over-year method would pick a different building.
