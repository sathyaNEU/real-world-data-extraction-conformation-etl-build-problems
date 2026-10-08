# FC38 — Where will the endowment be in ten years? Average returns don't compound, and spending makes order matter

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Endowment, pension and treasury cash projections (e.g. assumed-return controversies at large public pensions; corporate cash-pile planning) |
| Domain | Institutional investing / nonprofit finance |
| Task shape | 14 · Cuts of a distribution (P10 / P50 / P90 of real value after ten years, for two spending rules) |
| Core method | Historical simulation over all overlapping 120-month windows since 1926: monthly portfolio returns with monthly spending withdrawals, deflated by CPI; empirical percentiles |
| Analytical stump | Compounding the arithmetic average return overstates the typical (median) outcome by the volatility drag; ignoring withdrawals during drawdowns hides sequence risk; mixing nominal returns with real spending targets misstates purchasing power |
| Primary sources | Kenneth R. French Data Library (market and risk-free returns), BLS CPI-U |

## 1. The real-world situation

A university board wants to know how much of a capital campaign the endowment can support. The CFO projected ten years forward at
the historical **average** annual return minus the 5% spending rate and showed steady real growth. The investment committee chair
asked what the endowment looked like after ten bad years — and whether the median path really grows.

## 2. The decision (one deterministic recommendation)

**The board commits to a campaign draw only if the 10th-percentile real endowment value after ten years is at least 85% of today's
value under the adopted spending rule. Report P10/P50/P90 for two spending rules and the go/no-go.**

Rules (finance committee memo):

* Portfolio: 70% U.S. market (Mkt-RF + RF), 30% one-month T-bills (RF), rebalanced monthly, from the French data library; returns
  monthly, July 1926 – December 2024.
* Windows: every overlapping 120-month window starting from July 1926 through January 2015.
* Spending rule S1: each month withdraw (5% ÷ 12) of the start-of-month value. Rule S2: each month withdraw (5% ÷ 12) of the
  average of the 36 most recent month-end values (window start pre-filled at the initial value).
* Real value: deflate by CPI-U (not seasonally adjusted; months before 1913 not needed).
* Percentiles over windows (inclusive interpolation) of real end value ÷ initial value. Adopted rule: S2. Go if P10 ≥ 0.85.

## 3. Why capable analysts get it wrong

* Arithmetic average returns are higher than geometric (compound) returns by roughly half the variance.
* Spending withdrawn after losses cannot recover; deterministic projections ignore path dependence.
* Nominal projections look healthier; spending policies are about purchasing power.
* Using non-overlapping decades leaves only ~9 observations; overlapping windows use the full history (with dependence noted).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `F-F_Research_Data_Factors.csv` (monthly) | CSV | ~1.2k months | Kenneth R. French Data Library | Free use (data library terms; cite) | Market and RF returns |
| 2 | `F-F_Research_Data_Factors_daily.csv` | CSV | ~25k days | Same | Same | Context |
| 3 | `Portfolios_Formed_on_ME.csv` | CSV | ~1.2k × 20 | Same | Same | Context |
| 4 | `CUUR0000SA0.txt` (CPI-U) | TSV | ~1.3k | BLS | Public domain | Deflator |
| 5 | `french_data_library_notes.pdf` | PDF | — | Same | Same | Construction notes |
| 6 | `nacubo_spending_policy_summary.pdf` (public summary) | PDF | — | Cite | Cite | Spending-rule context |
| 7 | `finance_committee_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `cfo_projection.xlsx` | XLSX | ~15 | Task author | — | Arithmetic-mean projection |
| 9 | `window_results_template.csv` | CSV | — | Task author | — | Output layout |
| 10 | `endowment_profile.json` | JSON | — | Task author | — | Initial value |

## 5. Deterministic solution path

1. Build monthly 70/30 returns and CPI index.
2. For each 120-month window and rule, simulate value with withdrawals; deflate; ratio to initial.
3. Percentiles; decision; compare with the CFO's arithmetic projection.

## 6. Wrong paths (method errors, not misreadings)

**A — arithmetic-mean compounding.** P50 overstated; no tails.

**B — no withdrawals path (net return).** Sequence risk ignored.

**C — nominal values.** Purchasing power overstated.

**D — non-overlapping windows only.** Unstable percentiles.

## 7. Why the stump is analytical, not semantic

Returns, rules and percentiles are specified. The traps are compounding and path dependence — analytical properties of returns.

## 8. Draft task prompt (prose)

> The board will commit to a campaign draw only if, under our smoothed spending rule, the endowment's real value after ten years is
> at least 85% of today's in the bad (10th-percentile) case. Replay every ten-year window since 1926 as the finance committee memo
> specifies and give me the answer. Provide `window_outcomes.csv` (window start, end real ratio for both rules), `outcome_fan.png`
> showing P10/P50/P90 paths for both rules against the CFO's line, and a one-page `campaign_decision.pdf`.

## 9. Deliverables

* `window_outcomes.csv`, `outcome_fan.png`, `campaign_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 2 rules × 3 percentiles = 6; worst five windows (dates, ratios); decision; arithmetic vs geometric annual returns; CFO contrast.

## 11. Golden-output checklist

* Monthly rebalanced mix; correct withdrawal timing; CPI deflation; all windows; percentiles; decision.

## 12. Build notes (scope tuning)

* Confirm P10 under S2 sits within ±5 points of the 85% bar (adjust the bar before freezing if needed and document it).
* Cite the French library and record the download date (series are occasionally revised).
