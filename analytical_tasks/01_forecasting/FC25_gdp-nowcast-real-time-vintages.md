# FC25 — Nowcasting the GDP print the market will see: train on what was known, target what is released

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Trading and economics desks forecasting first releases of revised statistics (and any business metric that is later restated) |
| Domain | Macroeconomics / markets research |
| Task shape | 10 · Scorecard against thresholds (bridge-equation variants × real-time tests → adopt / hold) |
| Core method | Real-time data vintages (ALFRED): indicators as available on each nowcast date, target = advance GDP estimate; bridge equations re-estimated on vintage data |
| Analytical stump | Backtesting with today's revised data uses information that did not exist and targets the final number rather than the advance print; the model looks far more accurate than it can be in real time, and its ranking versus simpler models flips |
| Primary sources | Federal Reserve Bank of St. Louis ALFRED (archival vintages of GDP, payrolls, industrial production, retail sales) |

## 1. The real-world situation

A bank's research desk publishes a nowcast of the **advance** quarterly real GDP growth estimate two weeks before its release.
A new hire built a bridge-equation model on the latest FRED data and showed a backtest RMSE of 0.6 percentage points (annualized),
half the desk's current model. The head of research asked whether the backtest was done in real time.

## 2. The decision (one deterministic recommendation)

**Adopt the new model or keep the current one, based on real-time performance against advance estimates for 2012Q1–2024Q4.**

Rules (research memo):

* Target: advance estimate of real GDP growth (q/q, annualized) for each quarter, from ALFRED vintages.
* Nowcast date: 14 days before each advance release. Indicators: nonfarm payrolls, industrial production, real retail sales —
  each taken from the latest vintage available on the nowcast date; quarterly averages of available months (missing third month
  filled by the average of the two available months).
* Current model C: GDP growth = a + b × payroll growth (quarterly average, annualized). New model N: GDP growth = a + b₁ payroll
  growth + b₂ IP growth + b₃ retail-sales growth.
* Real-time evaluation: for each quarter, estimate the model on all earlier quarters using, for each of them, the advance GDP and
  the indicator values as they stood at that quarter's nowcast date; nowcast; compare with the advance release.
* Adopt N if its real-time RMSE is ≥ 10% lower than C's; otherwise keep C.

## 3. Why capable analysts get it wrong

* FRED's default series are the latest vintage; ALFRED's vintages must be requested explicitly.
* Revised indicators correlate better with revised GDP — revisions share information.
* The target the market prices is the advance print; final GDP is a different (and later) number.
* Ragged edges (missing latest months) exist in real time but not in revised data.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `alfred_GDPC1_all_vintages.csv` | CSV | ~100k (vintage × date) | FRB St. Louis ALFRED (BEA data) | BEA data public domain; ALFRED terms | GDP vintages |
| 2 | `alfred_PAYEMS_all_vintages.csv` | CSV | ~300k | ALFRED (BLS data) | Public domain data | Payroll vintages |
| 3 | `alfred_INDPRO_all_vintages.csv` | CSV | ~300k | ALFRED (Federal Reserve Board data) | Public data | IP vintages |
| 4 | `alfred_RRSFS_all_vintages.csv` | CSV | ~100k | ALFRED (Census data) | Public domain data | Retail sales vintages |
| 5 | `fred_latest_GDPC1_PAYEMS_INDPRO_RRSFS.json` | JSON | ~3k | FRED API | Same | Latest vintage (the trap) |
| 6 | `bea_release_schedule_2012_2025.csv` | CSV | ~160 | BEA | Public domain | Advance release dates |
| 7 | `alfred_user_guide.pdf` | PDF | — | FRB St. Louis | Cite | Vintage concepts |
| 8 | `croushore_stark_real_time_citation.pdf` | PDF | — | Cite | Cite | Real-time data background |
| 9 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `new_hire_backtest.xlsx` | XLSX | ~60 | Task author | — | Revised-data backtest |

## 5. Deterministic solution path

1. Build, for each target quarter, the real-time dataset (advance GDP history and indicator values as of the nowcast date).
2. Estimate C and N recursively; nowcast; compare with advance releases; RMSEs.
3. Apply the adoption rule; also report revised-data RMSEs for contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — latest-vintage backtest.** N's RMSE looks half of C's; adopted.

**B — target = latest GDP.** Different benchmark; ranking may flip.

**C — complete quarters assumed.** Ignores the ragged edge.

**D — full-sample estimation.** Look-ahead in coefficients.

## 7. Why the stump is analytical, not semantic

All series and timing rules are defined; the trap is the backtest design — information sets and targets over time.

## 8. Draft task prompt (prose)

> Before we switch nowcast models, test both the way they would really have run: with the data available two weeks before each
> advance GDP release from 2012 to 2024, scored against the advance print, per the research memo. Provide `realtime_scorecard.csv`
> (model: real-time RMSE, revised-data RMSE, improvement, decision), `nowcast_errors.png` comparing real-time errors of both models
> by quarter, and a one-page `model_decision.pdf` with the decision and why the new hire's backtest overstated the gain.

## 9. Deliverables

* `realtime_scorecard.csv`, `nowcast_errors.png`, `model_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 2 models × (real-time RMSE, revised RMSE, bias) = 6; quarterly nowcasts for a sample of 12 quarters; decision; improvement figure;
  ragged-edge handling.

## 11. Golden-output checklist

* Vintage selection by date; advance target; recursive estimation; ragged edge; adoption rule.

## 12. Build notes (scope tuning)

* Exclude or separately treat 2020Q2–2020Q4 (state the rule) and confirm the decision differs between real-time and revised
  backtests.
* Record the ALFRED download date.
