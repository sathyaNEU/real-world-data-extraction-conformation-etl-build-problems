# AD06 — Epidemic thresholds for flu-like illness: a baseline fitted to epidemics cannot detect epidemics

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Baselines for operational surveillance contaminated by past events (error-rate baselines fitted through past incidents, demand baselines fitted through past promotions) |
| Domain | Public health surveillance / hospital surge planning |
| Task shape | 08 · Rule replayed on history (ten seasons replayed through the threshold rule → surge weeks to budget) |
| Core method | Serfling-type cyclic regression baseline fitted only on non-epidemic weeks, prediction-interval threshold, season-by-season replay |
| Analytical stump | A baseline regression fitted on all weeks absorbs past epidemic peaks, raising the threshold so that only extreme seasons register. Thresholds must use prediction intervals, not residual SD of contaminated fits |
| Primary sources | CDC ILINet (FluView Interactive) regional weighted ILI, CDC surveillance methods documentation |

## 1. The real-world situation

A hospital network in one HHS region staffs a **surge unit** whenever regional influenza-like illness (ILI) is above the
epidemic threshold. Next year's surge budget is set from how many weeks per season the threshold was exceeded historically.
The analyst fitted a seasonal regression to every week of the last decade and set the threshold at the fit plus two
residual standard deviations; in most seasons, only three or four weeks crossed it — far fewer than the clinicians
remembered working under surge conditions.

## 2. The decision (one deterministic recommendation)

**How many surge weeks should the 2025–26 budget fund = the median number of above-threshold weeks across the ten replay
seasons (2010–11 to 2019–20)?**

Rules (surveillance memo):

* Series: weekly weighted ILI (%) for the HHS region, MMWR weeks, 2005–2020 (seasons start in MMWR week 40).
* For each replay season s, fit the baseline on the **five preceding seasons**, using only **non-influenza weeks** as CDC
  defines them: runs of two or more consecutive weeks in which each week accounted for less than 2% of that season's total
  influenza-positive specimens reported by the region's public health laboratories. Model
  ILI_t = a + b·t + c·sin(2πt/52.18) + d·cos(2πt/52.18) by OLS on those weeks.
* Threshold for each week of season s = the upper bound of the 95% **prediction interval** of the fitted model for that week.
* A week is "above threshold" if observed ILI > threshold. Count per season.
* Budget = median of the ten counts (if even, the average of the middle two, rounded up).

## 3. Why capable analysts get it wrong

* Fitting a seasonal model to all data is the default; the model then "learns" epidemics as normal winter behaviour.
* Residual SD from a contaminated fit is inflated by epidemic weeks, widening the band further.
* Confidence intervals for the mean are narrower than prediction intervals for a new observation; mixing them changes counts.
* Fitting on all years (including the season being evaluated) is look-ahead.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ILINet_regional_1997_2024.csv` | CSV | ~14k (10 regions × weeks) | CDC FluView Interactive | U.S. Gov public domain | Weighted ILI by region |
| 2 | `ILINet_national_1997_2024.csv` | CSV | ~1.4k | CDC | Public domain | Context |
| 3 | `WHO_NREVSS_clinical_labs_regional.csv` | CSV | ~5k | CDC FluView | Public domain | Virologic context |
| 4 | `WHO_NREVSS_public_health_labs_regional.csv` | CSV | ~5k | CDC | Public domain | Context |
| 5 | `mmwr_week_calendar_2005_2025.csv` | CSV | ~1.1k | CDC MMWR week definitions | Public domain | Week alignment |
| 6 | `cdc_flu_surveillance_methods.pdf` | PDF | — | CDC "Overview of Influenza Surveillance" | Public domain | Baseline/threshold concepts |
| 7 | `serfling_1963_reference.pdf` (citation) | PDF | — | Public Health Reports (cite) | Cite | Method background |
| 8 | `surveillance_memo.pdf` | PDF | — | Task author | — | Rules in §2 (quotes CDC's non-influenza-week definition) |
| 9 | `analyst_all_weeks_fit.xlsx` | XLSX | ~600 | Task author | — | Contaminated-baseline results |
| 10 | `hhs_region_states.json` | JSON | 10 | HHS | Public domain | Region definitions |

## 5. Deterministic solution path

1. Assign MMWR weeks and seasons; select the region.
2. For each replay season: build the training window (five prior seasons), classify non-influenza weeks from the public
   health laboratory positives, fit OLS on those weeks only.
3. Compute prediction-interval upper bounds for every week of the replay season; count exceedances.
4. Median across ten seasons; budget weeks.
5. Contrast with the all-weeks/residual-SD approach and with confidence-interval thresholds.

## 6. Wrong paths (method errors, not misreadings)

**A — fit on all weeks.** Threshold too high; few exceedances; budget too small.

**B — residual-SD band.** Different width; counts shift.

**C — confidence interval instead of prediction interval.** Band too narrow; counts too high.

**D — training on all seasons including the one evaluated.** Look-ahead; counts biased.

## 7. Why the stump is analytical, not semantic

The memo defines the series, the model and the exclusion rule. The stump is recognizing that a baseline must be estimated
from non-epidemic periods and out of sample, and using the right interval — statistical method, not interpretation.

## 8. Draft task prompt (prose)

> Our surge budget for next season is the median number of weeks per season that regional ILI exceeded the epidemic
> threshold over the last ten replay seasons, using the method in the surveillance memo. Replay each season with a baseline
> fitted only on the preceding non-epidemic weeks and tell me how many surge weeks to fund. Provide `season_replay.csv`
> (season, training weeks used, fitted coefficients, weeks above threshold, first and last week above), `ili_threshold.png`
> showing ILI against the replayed threshold for all ten seasons with exceedances shaded, and a one-page `surge_budget.pdf`
> with the budget and how many weeks the all-weeks method would have funded.

## 9. Deliverables

* `season_replay.csv` (10 rows), `ili_threshold.png`, `surge_budget.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 seasons × (count, first/last week) = 30; median; budget; contaminated-method contrast.

## 11. Golden-output checklist

* Rolling five-season training, exclusions, OLS cyclic model, 95% prediction intervals, counts, median rule.

## 12. Build notes (scope tuning)

* Quote CDC's non-influenza-week definition verbatim from the methods page you ship, and confirm the contaminated approach
  gives a median at least 3 weeks lower.
* The 2009 pandemic falls in training windows for early replay seasons; check that its weeks are excluded by the
  virologic rule (positives were high), and document how the 2009–10 "season" is bounded.
