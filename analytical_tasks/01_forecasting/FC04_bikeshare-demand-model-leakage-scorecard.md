# FC04 — Choosing the next-day bike-share demand model: the best backtest used tomorrow's information

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Leakage in production forecasting models (ride-hail and delivery demand forecasts, ads delivery forecasts, supply-chain ML), where backtests use information unavailable at prediction time |
| Domain | Micromobility operations / fleet rebalancing |
| Task shape | 10 · Scorecard against thresholds (candidate model × criterion → adopt / hold) |
| Core method | Forecast-origin discipline (information set at issuance), rolling-origin evaluation with monthly refits, Poisson GLMs with pinned specifications |
| Analytical stump | Three kinds of leakage make infeasible models win: target components as features, same-day weather that is unknown at issuance, lags that are not yet observed; random K-fold CV on autocorrelated hourly data hides all three |
| Primary sources | UCI Bike Sharing Dataset (Capital Bikeshare 2011–2012), Capital Bikeshare trip history, NOAA ISD hourly weather |

## 1. The real-world situation

A bike-share operator schedules overnight rebalancing crews from an hourly demand forecast for the next day, issued at
**12:00 the day before**. The data-science team compared models with 10-fold cross-validation on the hourly file and
proposed one with an R² near 0.99. In production it could not be run: two of its inputs did not exist at noon the day
before.

## 2. The decision (one deterministic recommendation)

**Adopt or hold: which candidate replaces the incumbent seasonal-naive forecast, if any?**

Rules (model governance memo):

* Target: hourly trip count `cnt` for every hour of day D, issued at 12:00 on day D−1. A feature is admissible only if its
  value is known at 12:00 on D−1. No archived weather forecasts exist; weather observed up to 12:00 on D−1 is admissible.
* Candidates (Poisson GLM, log link, MLE unless noted):
  M1 incumbent: cnt(h, D−7). M2: hour×workingday + month + weathersit + temp + hum + windspeed (values for day D).
  M3: M2 + casual + registered. M4: hour×workingday + month + log(1+cnt lag 24) + log(1+cnt lag 168).
  M5: hour×workingday + month + log(1+cnt lag 48) + log(1+cnt lag 168) + temp and weathersit at 11:00 on D−1.
* Evaluation: rolling origin over 2012 — refit at the start of each month on all prior data; forecast every day of that
  month using only admissible information.
* Scorecard thresholds: admissible (pass/fail); MAE ≤ 0.80 × incumbent MAE; mean bias within ±5% of mean demand.
* Adopt the admissible candidate with the lowest MAE that passes every test; hold the incumbent if none passes.

## 3. Why capable analysts get it wrong

* The UCI file presents every column side by side; `casual + registered = cnt` exactly, and including them is target leakage.
* Hourly weather in the file is *observed* weather for that hour — perfectly known in hindsight, unknown at noon the day
  before.
* Lag-24 is natural for hourly data, but for hours after 11:00 on D, the same hour on D−1 has not happened yet at issuance.
* Random K-fold CV places neighbouring hours in train and test, so autocorrelated features look prescient.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `hour.csv` | CSV | 17,379 | UCI Bike Sharing Dataset (id 275) | CC BY 4.0 | Hourly counts + weather |
| 2 | `day.csv` | CSV | 731 | UCI | CC BY 4.0 | Daily aggregates |
| 3 | `Readme.txt` | Text | — | UCI | CC BY 4.0 | Field definitions |
| 4–11 | `2011-Q1-cabi-trip-history-data.csv` … `2012-Q4-…csv` | CSV | 0.2–0.6M each | Capital Bikeshare system data | Capital Bikeshare data licence (verify) | Raw trips for reconciliation |
| 12 | `isd_724050_2011_2012.csv` (Washington Reagan hourly obs) | CSV | ~20k | NOAA NCEI Integrated Surface Database | Public domain | Weather cross-check |
| 13 | `dc_holidays_2011_2012.json` | JSON | ~25 | DC government / OPM | Public | Calendar |
| 14 | `model_governance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 15 | `kfold_results_from_team.xlsx` | XLSX | ~5 | Task author | — | The flawed comparison |

## 5. Deterministic solution path

1. Classify each candidate's features as admissible or not at 12:00 on D−1 (M2, M3 fail; M4 fails for hours ≥ 12; M1, M5 pass).
2. Rolling-origin evaluation for all five (to show the gap), monthly refits, admissible-information forecasts for M1/M5.
3. Compute MAE and bias per model on 2012; apply thresholds; adopt or hold.
4. Contrast with 10-fold CV results.

## 6. Wrong paths (method errors, not misreadings)

**A — random K-fold.** M3 then M2 win with spectacular scores.

**B — admit same-day weather.** M2 adopted; production error far higher than evaluated.

**C — admit lag-24 for all hours.** M4 adopted although half its inputs are unavailable.

**D — in-sample fit.** Overstates every model; the threshold test passes spuriously.

## 7. Why the stump is analytical, not semantic

The memo states the issuance time and the admissibility rule in plain terms, and the README defines every column. The
failure is methodological — evaluating models under an information set they will never have — not a misread field.

## 8. Draft task prompt (prose)

> Rebalancing runs off a next-day hourly forecast issued at noon the day before. Using the bike-share data and the
> governance memo in the folder, evaluate the five candidate models the way they would actually be used and tell me
> whether we adopt one or keep the incumbent. Provide `model_scorecard.csv` with each model's admissibility, rolling-origin
> MAE, MAE relative to the incumbent, bias, each threshold result and the decision, and `rolling_mae_by_month.png` showing
> monthly MAE for every candidate in 2012 with inadmissible models visibly marked. Add a short `adoption_memo.pdf` with the
> decision, the adopted model's MAE improvement, and what the team's K-fold comparison would have chosen.

## 9. Deliverables

* `model_scorecard.csv`, `rolling_mae_by_month.png`, `adoption_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 models × 4 tests = 20 cells; 12 monthly MAEs for the adopted model (sampled); decision; improvement; K-fold contrast.

## 11. Golden-output checklist

* Admissibility judged at the issuance time; rolling-origin monthly refits; thresholds applied; decision stated.

## 12. Build notes (scope tuning)

* Confirm M5 passes the 0.80 × incumbent threshold (adjust the threshold within reason, documented, before freezing) and
  that K-fold ranks M3/M2 first.
* Publish the exact GLM formulas and the R/Python reference implementation output to two decimals.
