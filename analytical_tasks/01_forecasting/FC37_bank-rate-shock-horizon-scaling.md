# FC37 — How bad can a year of rate moves get for a bond book? Daily volatility × √252 is not a one-year shock

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Bank balance-sheet interest-rate risk (the 2023 regional-bank failures driven by long-duration securities losses) |
| Domain | Banking treasury / asset-liability management |
| Task shape | 13 · Scenarios and the flip point (shock-estimation method × portfolio duration grid; flip duration for the hedge decision) |
| Core method | Empirical distribution of overlapping 12-month changes in Treasury yields (historical simulation) versus square-root-of-time scaling of daily changes; duration-based portfolio loss |
| Analytical stump | Scaling daily yield-change volatility by √252 assumes independent daily changes; rates trend and mean-revert, so 12-month changes have fatter, regime-dependent tails. The square-root rule understated the 2022 one-year rise by a wide margin. Overlapping windows are needed to use the history, and their dependence must not be mistaken for more data |
| Primary sources | U.S. Treasury daily par yield curve rates |

## 1. The real-world situation

A regional bank holds a large securities portfolio funded by deposits. The ALCO policy says: **hedge (or shorten duration) if the
99th-percentile one-year mark-to-market loss exceeds 25% of Tier 1 capital**. The risk team estimated the one-year shock as the
99th percentile of daily 5-year yield changes × √252 and concluded no hedge was needed — a conclusion that history since 2022
contradicts.

## 2. The decision (one deterministic recommendation)

**Hedge or not, the one-year 99th-percentile loss, and the portfolio duration at which the decision flips.**

Rules (ALM memo):

* Yields: daily 5-year par Treasury yield, 1990-01-02 to the as-of date.
* Shock (historical simulation): all overlapping 252-business-day changes in the 5-year yield; 99th percentile of increases
  (inclusive linear interpolation).
* Comparator (√T rule): 99th percentile of daily changes × √252.
* Portfolio: market value and effective duration in `portfolio.json`; loss = MV × duration × shock (first-order).
* Hedge if loss > 25% of Tier 1 capital (in the file).
* Scenario grid: shock method {historical 1990–as-of, historical 2000–as-of, √T} × duration {3, 5, 7 years}; flip duration = the
  duration (one decimal) at which the historical 1990–as-of loss equals 25% of Tier 1.

## 3. Why capable analysts get it wrong

* Square-root-of-time is a standard regulatory shortcut for VaR horizons and looks principled.
* Daily rate changes are nearly uncorrelated, but monetary-policy cycles make multi-month changes persistent.
* Historical windows matter: post-1990 history contains several tightening cycles; short windows (e.g. 2010–2021) miss them.
* Overlapping 12-month windows are highly dependent; they describe the distribution but do not multiply the information.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–35 | `daily-treasury-rates_par-yield-curve_YYYY.csv` (1990–2024) | CSV | ~250 each | U.S. Department of the Treasury | Public domain | Daily par yields |
| 36 | `par_yield_curve_all.parquet` | Parquet | ~8.8k days | Derived | Public domain | Combined |
| 37 | `treasury_yield_curve_methodology.pdf` | PDF | — | U.S. Treasury | Public domain | Methodology notes |
| 38 | `fdic_call_report_securities_extract.csv` | CSV | ~5k | FFIEC CDR bulk Call Reports (Schedule RC-B) | Public domain | Peer portfolio context |
| 39 | `portfolio.json` | JSON | — | Task author (illustrative bank built from public call-report averages) | — | MV, duration, Tier 1 |
| 40 | `alm_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 41 | `risk_team_sqrt_t_estimate.xlsx` | XLSX | ~10 | Task author | — | √T estimate |
| 42 | `fomc_tightening_cycles.json` | JSON | ~8 | Federal Reserve (public dates) | Public domain | Context |

## 5. Deterministic solution path

1. Build the daily 5-year series; compute all overlapping 252-day changes; 99th percentile.
2. Compute the √T comparator.
3. Loss for the portfolio; decide; fill the 3 × 3 grid; solve the flip duration.

## 6. Wrong paths (method errors, not misreadings)

**A — √T scaling.** Shock far too small; no hedge.

**B — short history window.** Misses tightening cycles.

**C — calendar-year changes only.** Few observations; percentile unstable.

**D — non-overlapping windows with interpolation across gaps.** Inconsistent counting.

## 7. Why the stump is analytical, not semantic

Series, horizon, percentile and loss formula are explicit. The trap is a statistical assumption about time aggregation of risk.

## 8. Draft task prompt (prose)

> ALCO needs a hedge decision under the policy in the ALM memo: hedge if the 99th-percentile one-year loss exceeds 25% of Tier 1.
> Estimate the one-year rate shock from the Treasury history, compute the loss for our portfolio, fill the scenario grid and tell me
> the duration at which the decision flips. Provide `shock_grid.csv` (method × duration: shock in bp, loss, % of Tier 1, hedge flag),
> `twelve_month_changes.png` (distribution of 12-month changes vs the √T-implied distribution) and a one-page `alco_decision.pdf`.

## 9. Deliverables

* `shock_grid.csv`, `twelve_month_changes.png`, `alco_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 shocks; 9 grid cells × (loss, flag); flip duration; decision; percentile ladder of 12-month changes.

## 11. Golden-output checklist

* Overlapping 252-day changes; inclusive percentile; correct loss; grid; flip.

## 12. Build notes (scope tuning)

* Calibrate `portfolio.json` from public call-report averages for banks of a given size; keep the hedge threshold fixed.
* Confirm √T and historical methods give opposite decisions at the base duration.
