# DS08 — Choosing crop-insurance coverage: the best expected return is not the best protection

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Risk-constrained procurement and hedging (insurance limits, cloud reserved capacity, supply contracts) where the objective includes a downside constraint |
| Domain | Agriculture / insurance |
| Task shape | 13 · Scenarios and the flip point (coverage level × plan type → expected net cost and 5% CVaR of farm revenue; the coverage chosen under the lender's CVaR floor and the premium subsidy at which the choice flips) |
| Core method | Build a historical loss distribution from county-level indemnity and liability by year (loss cost ratios) for the crop; simulate farm revenue per year with and without insurance at each coverage level; expected net cost = premium − expected indemnity; CVaR_5% of revenue; choose the cheapest coverage meeting the CVaR floor |
| Analytical stump | Choosing the coverage with the best expected net return (often low coverage, since premiums exceed expected indemnities after subsidy) ignores that the farm needs protection in bad years; the lender's covenant is on downside revenue. Ranking by loss ratio or average indemnity misses the tail |
| Primary sources | USDA Risk Management Agency (RMA) Summary of Business and Cause of Loss data (county × crop × year) |

## 1. The real-world situation

A grain farm's lender requires that, in the worst 5% of years, farm revenue stays above $600,000 (CVaR covenant). The farm's adviser recommended
70% coverage because it had the best expected net return over the past 20 years. The lender asked which coverage level meets the covenant at least
cost.

## 2. The decision (one deterministic recommendation)

**The coverage level (50–85% in 5-point steps, revenue protection) that meets the CVaR floor at the lowest expected net cost, and the premium subsidy
rate at which the next-lower coverage would also meet the floor.**

Rules (risk memo):

* Data: RMA Summary of Business by county/crop/coverage level and Cause of Loss for the county and crop in memo, 2004–2023.
* Farm: 2,000 acres, APH yield and projected price per memo; revenue = yield × harvest price (county loss history used to scale yield shocks).
* Loss scenarios: each historical year's county loss cost ratio at each coverage level (indemnity ÷ liability) applied to the farm's liability;
  revenue shortfall scaled consistently (memo's mapping).
* Premium: county average premium rate per coverage level × liability × (1 − subsidy rate by coverage level, current schedule).
* For each coverage: expected net cost = mean(premium − indemnity); CVaR_5% = mean of the worst 5% (one year of 20) of revenue + indemnity −
  premium.
* Choose the lowest expected net cost among coverages with CVaR_5% ≥ $600,000; flip point on subsidy.

## 3. Why capable analysts get it wrong

* Expected return is the default comparison.
* Insurance exists for the tail; subsidised premiums still exceed expected indemnity at high coverage.
* Loss ratios at county level must be mapped to the farm's liability.
* CVaR with 20 years uses the single worst year (memo convention); that year drives the decision.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `sobcov_<yyyy>.txt` (2004–2023) | Pipe-delimited | ~100k–200k each | USDA RMA Summary of Business | U.S. Gov public domain | Liability, premium, indemnity by coverage level |
| 2 | `colsom_<yyyy>.txt` (2004–2023) | Pipe-delimited | ~100k each | USDA RMA Cause of Loss | Public domain | Indemnities by cause |
| 3 | `rma_file_layouts.pdf` | PDF | — | USDA RMA | Public domain | Layouts |
| 4 | `subsidy_schedule.json` | JSON | ~8 | Task author (from RMA subsidy rates) | Public domain | Subsidies |
| 5 | `farm_profile.json` | JSON | — | Task author | — | Farm inputs |
| 6 | `risk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `adviser_expected_return.xlsx` | XLSX | 8 | Task author | — | Naive choice |

## 5. Deterministic solution path

1. Extract county/crop records; compute loss cost ratios and premium rates by coverage and year.
2. Map to farm liability; revenue scenarios with and without insurance.
3. Expected net cost and CVaR per coverage; choose; flip point.
4. Contrast with the adviser's recommendation.

## 6. Wrong paths (method errors, not misreadings)

**A — maximise expected return.** Fails the covenant.

**B — use average loss ratio across coverages.** Ignores coverage-specific losses.

**C — ignoring subsidies.** Wrong costs.

**D — VaR instead of CVaR.** Different statistic than the covenant.

## 7. Why the stump is analytical, not semantic

The data mapping and risk measure are specified. The trap is optimising the mean when the decision is constrained by the tail.

## 8. Draft task prompt (prose)

> Which coverage level should the farm buy to satisfy the lender's downside covenant at least cost? Build the historical scenario analysis in the
> risk memo. Provide `coverage_grid.csv` (coverage: premium, expected indemnity, expected net cost, CVaR), `risk_return_plot.png`, and a one-page
> `coverage_choice.pdf` with the subsidy flip point.

## 9. Deliverables

* `coverage_grid.csv`, `risk_return_plot.png`, `coverage_choice.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 coverage levels × (expected net cost, CVaR) = 16; worst-year identification; choice; flip point; adviser contrast.

## 11. Golden-output checklist

* Record filters; loss ratios; liability mapping; premiums after subsidy; CVaR; choice.

## 12. Build notes (scope tuning)

* Choose county and crop with at least one severe loss year; confirm the expected-return choice fails the covenant.
