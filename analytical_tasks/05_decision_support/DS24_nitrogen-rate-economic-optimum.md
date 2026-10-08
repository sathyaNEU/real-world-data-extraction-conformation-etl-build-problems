# DS24 — How much nitrogen to apply: the rate that maximises yield is not the rate that maximises profit

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Spend decisions on saturating response curves (advertising budgets, compute for model training, sales headcount) where marginal return must equal marginal cost |
| Domain | Agronomy / farm management |
| Task shape | 13 · Scenarios and the flip point (nitrogen price × corn price scenarios → economic optimum N rate; the recommended rate and the price ratio at which it moves by 20 lb/acre) |
| Core method | Fit quadratic-plateau yield response per site from N-rate trials; pooled economic optimum via the Maximum Return to N approach: for each rate, average across sites of net return (yield × corn price − N × N price) relative to zero-N; choose the rate maximising mean net return; profitable range within $1/acre of the maximum |
| Analytical stump | Choosing the rate at which yield plateaus (agronomic maximum) ignores the cost of the last pounds of N; per-site optima averaged arithmetically differ from the rate maximising average net return across sites. Price ratios shift the optimum |
| Primary sources | Corn nitrogen rate trial data compiled for the regional Corn N Rate Calculator (Maximum Return to Nitrogen database; trial yields by N rate and site) |

## 1. The real-world situation

A farm co-operative recommends nitrogen rates to members for corn following soybean. Its agronomist recommended 190 lb N/acre — the average
rate at which trial yields stopped increasing. With nitrogen prices high, the board asked for the profit-maximising rate.

## 2. The decision (one deterministic recommendation)

**The recommended N rate (lb/acre, nearest 5) at current prices ($0.70/lb N, $4.50/bu corn), the profitable range, and the price ratio at which the
recommendation changes by 20 lb.**

Rules (agronomy memo):

* Data: trial site yields by N rate (0–240 lb in steps per site) for corn following soybean in the state in memo.
* Per site: fit quadratic-plateau yield(N) = a + bN + cN² for N < N_p, plateau thereafter (least squares).
* Net return for rate R at site s: yield_s(R) × P_corn − R × P_N − yield_s(0) × P_corn.
* Mean net return across sites for R = 0–240 (1 lb steps); choose the maximum (MRTN); profitable range: rates within $1/acre of the maximum.
* Scenarios: P_N/P_corn ratios 0.05–0.25; find the ratio where the MRTN rate shifts by 20 lb from current.
* Contrast: average of site agronomic maxima (N_p).

## 3. Why capable analysts get it wrong

* Yield maximisation is intuitive.
* Diminishing returns mean the last increments cost more than they return.
* Averaging site optima ≠ optimising average returns when responses differ.
* Price ratios, not absolute prices, drive the optimum.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `mrtn_trial_yields_<state>.csv` | CSV | ~5–10k site × rate yields | Corn N Rate Calculator / regional MRTN database (public summaries) | Public (cite; verify terms) | Trial yields |
| 2 | `site_metadata.csv` | CSV | ~300 sites | Same | Public | Previous crop, year, soil |
| 3 | `mrtn_methodology.pdf` | PDF | — | Sawyer et al., Iowa State Extension (cite) | Public | Method |
| 4 | `agronomy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `agronomist_plateau_average.xlsx` | XLSX | — | Task author | — | Naive recommendation |
| 6 | `price_scenarios.json` | JSON | — | Task author | — | Prices |
| 7 | `qp_fit_check.json` | JSON | — | Task author | — | Fit checks for 3 sites |

## 5. Deterministic solution path

1. Filter sites (previous crop, state); fit quadratic-plateau per site.
2. Net returns by rate averaged across sites; MRTN; profitable range.
3. Scenario sweep; flip ratio; contrast with agronomic average.

## 6. Wrong paths (method errors, not misreadings)

**A — average plateau rate.** Over-applies N.

**B — average of per-site economic optima.** Not the memo's pooled method.

**C — linear-plateau without curvature.** Different optimum.

**D — absolute prices without ratio sensitivity.** Misses flip.

## 7. Why the stump is analytical, not semantic

The model and economic rule are specified. The trap is maximising output instead of return.

## 8. Draft task prompt (prose)

> What nitrogen rate should we recommend for corn after soybean at today's prices? Fit the trial responses and compute the maximum return to N as the
> agronomy memo specifies. Provide `net_return_curve.csv` (rate: mean net return), `response_and_return.png`, and a one-page `n_rate_recommendation.pdf`
> with the price-ratio flip point.

## 9. Deliverables

* `net_return_curve.csv`, `response_and_return.png`, `n_rate_recommendation.pdf`.

## 10. Where 25+ rubric criteria come from

* MRTN rate; range bounds; net returns at 10 rates; scenario rates at 5 ratios; flip ratio; contrast; fit checks.

## 11. Golden-output checklist

* Site filter; QP fits; net-return formula; pooling; range; scenarios.

## 12. Build notes (scope tuning)

* Confirm the agronomic average exceeds the MRTN rate by ≥ 30 lb at current prices.
