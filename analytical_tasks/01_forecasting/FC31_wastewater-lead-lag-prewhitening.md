# FC31 — How many weeks of warning does wastewater give? Cross-correlations of trending series lie about lags

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Leading-indicator selection for operational forecasts (any "signal X leads outcome Y by k weeks" claim in health systems, supply chains or ad platforms) |
| Domain | Public health / hospital surge planning |
| Task shape | 17 · Periods around a change point (lag identified on training seasons, then each forecast week checked against a committed threshold; go/no-go on early surge activation) |
| Core method | Box–Jenkins prewhitening: fit an AR model to the leading series, filter both series with it, read the lag from the cross-correlation of the prewhitened series; distributed-lag forecast at the identified lead |
| Analytical stump | Raw cross-correlations between two smooth, autocorrelated epidemic curves are broad and biased; their peak often sits at lag 0 or at a spurious lag. Picking the lead from the raw CCF over the whole sample also uses future data |
| Primary sources | CDC National Wastewater Surveillance System (NWSS) state-level data, CDC NHSN Hospital Respiratory Data |

## 1. The real-world situation

A state hospital association wants to activate surge staffing **ahead** of respiratory admissions using wastewater viral levels.
An analyst computed the cross-correlation between weekly wastewater concentration and weekly COVID-19 admissions over 2022–2024 and
reported "wastewater leads admissions by 3 weeks". The plan built on that lead activated surge staffing too early in one season and
too late in the next.

## 2. The decision (one deterministic recommendation)

**The lead (in weeks) to use, and go/no-go: would the resulting rule have activated surge staffing at least 2 weeks before
admissions crossed the surge threshold in the 2024–25 season?**

Rules (surveillance memo):

* Series: weekly state-level SARS-CoV-2 wastewater viral activity level (NWSS) and weekly new COVID-19 hospital admissions (NHSN),
  MMWR weeks.
* Training: 2022-09 through 2024-06; evaluation season: 2024-07 through 2025-06.
* Prewhitening: fit AR(p) to the first differences of the log wastewater series on training data (p chosen by AIC, p ≤ 4); filter
  both differenced log series with the fitted AR polynomial; lead k = the lag (0–6 weeks) maximizing the cross-correlation of the
  filtered series with wastewater leading.
* Rule for evaluation: activate when log wastewater (k weeks earlier) predicts admissions above the surge threshold using the OLS
  model ln(adm_t) = a + b·ln(ww_{t−k}) fitted on training data.
* Go if the first activation week precedes the first week admissions actually exceed the threshold by ≥ 2 weeks.

## 3. Why capable analysts get it wrong

* Cross-correlation of two autocorrelated series spreads correlation across many lags; the peak is not a reliable lead estimate.
* Trends and common seasonality make level correlations high at every lag.
* Selecting the lag on the full sample, then evaluating on part of it, is look-ahead.
* Differencing alone does not remove AR structure; prewhitening uses the input series' own model.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `NWSS_state_level_viral_activity.csv` | CSV | ~20k | CDC NWSS (data.cdc.gov) | U.S. Gov public domain | Weekly wastewater levels |
| 2 | `NWSS_site_level_concentrations.csv` | CSV | ~500k | CDC NWSS | Public domain | Site detail (context) |
| 3 | `NHSN_Hospital_Respiratory_Data_weekly.csv` | CSV | ~30k | CDC NHSN (data.cdc.gov) | Public domain | Weekly COVID admissions by state |
| 4 | `nwss_methodology.pdf` | PDF | — | CDC | Public domain | Normalization and viral activity levels |
| 5 | `nhsn_hrd_data_dictionary.pdf` | PDF | — | CDC | Public domain | Admission definitions |
| 6 | `mmwr_weeks_2022_2025.csv` | CSV | ~180 | CDC | Public domain | Week alignment |
| 7 | `box_jenkins_prewhitening_reference.pdf` (citation) | PDF | — | Cite | Cite | Method |
| 8 | `surge_threshold.json` | JSON | — | Task author | — | Admissions threshold |
| 9 | `surveillance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_ccf_results.xlsx` | XLSX | ~15 | Task author | — | Raw full-sample CCF |

## 5. Deterministic solution path

1. Align series by MMWR week for the state; log-transform and difference.
2. Fit AR(p) on training wastewater differences; filter both series; CCF lags 0–6; choose k.
3. Fit the OLS lag model on training data; run on the evaluation season; find activation and threshold-crossing weeks; decide.
4. Contrast with the raw-CCF lead.

## 6. Wrong paths (method errors, not misreadings)

**A — raw CCF lead.** Wrong k; activation too early or too late.

**B — levels correlation.** Every lag looks strong.

**C — full-sample selection.** Look-ahead; optimistic evaluation.

**D — no differencing before AR fit.** Unit-root behaviour distorts filtering.

## 7. Why the stump is analytical, not semantic

The series and rules are defined. The trap is a time-series identification error — reading leads from autocorrelated series.

## 8. Draft task prompt (prose)

> Before we tie surge staffing to wastewater, establish the lead properly and test it on last season, following the surveillance
> memo. Using the NWSS and NHSN files in the folder, prewhiten, identify the lead, build the lag model on the training period and tell
> me whether it would have activated at least two weeks early in 2024–25. Provide `lead_identification.csv` (AR order and
> coefficients, prewhitened CCF by lag, raw CCF by lag), `ccf_comparison.png`, and a one-page `surge_trigger_decision.pdf` with the
> lead, the activation and crossing weeks, and the go/no-go.

## 9. Deliverables

* `lead_identification.csv`, `ccf_comparison.png`, `surge_trigger_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* AR coefficients; 7 prewhitened and 7 raw CCF values; k; a, b; activation week; crossing week; decision.

## 11. Golden-output checklist

* Log-differencing; AIC-chosen AR on training only; filtering both series; lag choice; out-of-sample evaluation.

## 12. Build notes (scope tuning)

* Pick a state with complete coverage in both systems; confirm raw-CCF and prewhitened leads differ.
* Note the NHSN reporting changes in 2024 (mandatory reporting gaps) and choose the state/season accordingly.
