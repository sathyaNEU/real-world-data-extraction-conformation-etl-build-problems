# DS11 — How much to mark up a highway bid: you win most often exactly when you underestimated the cost

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Bidding in procurement and auctions (contractor bids, ad auctions, cloud capacity tenders) where winning is correlated with optimistic estimates |
| Domain | Construction / public procurement |
| Task shape | 04 · Setting one dial (the bid markup over the firm's cost estimate that maximises expected profit for a class of resurfacing lettings) |
| Core method | Model the lowest competing bid relative to the engineer's estimate from historical bid tabulations (empirical distribution by project type, size band and number of bidders); expected profit(m) = P(win | m) × (bid − true cost), with our estimate = true cost × u (estimation error), so that winning is conditioned on low u (winner's curse) |
| Analytical stump | Choosing the markup that maximises "win rate × markup" using the firm's estimate as true cost ignores that, conditional on winning, the firm's estimate was more likely too low. Using all bids rather than the lowest competitor bid, or pooling projects with different numbers of bidders, misestimates win probability |
| Primary sources | Texas Department of Transportation (TxDOT) bid tabulations (letting results with all bids and engineer's estimates) |

## 1. The real-world situation

A paving contractor bids on TxDOT resurfacing lettings. Its estimator sets markup at 12% and wins 1 in 5. Management wants the markup that
maximises expected profit for next year's lettings with 3–5 bidders. The finance team noted that projects the company wins tend to overrun its
internal estimate.

## 2. The decision (one deterministic recommendation)

**The markup (percent of own estimate, 0.5% steps from 0% to 20%) that maximises expected profit per letting for the target class, accounting for
the winner's curse, and the expected win rate at that markup.**

Rules (bidding memo):

* Data: TxDOT bid tabulations 2018–2023 for resurfacing project types (memo's work-type codes), engineer's estimate $1–10M, 3–5 bidders.
* Competitor bid ratio R = lowest bid among other bidders ÷ engineer's estimate (computed for each letting excluding a randomly chosen bidder as
  "us", per memo's leave-one-out construction).
* True cost of a letting = engineer's estimate × T, T ~ lognormal(0, 0.06); our cost estimate = true cost × u, u ~ lognormal(0, 0.08)
  (estimation error), independent of competitors' bids (memo convention).
* Win if our bid = our estimate × (1 + m) < competitor low bid (R × engineer's estimate, R drawn from the empirical distribution).
* Expected profit(m) = E[1{win} × (bid − true cost)] by Monte Carlo (100,000 draws, seed 2024); because low u makes winning more likely,
  wins are concentrated where our estimate was too low (winner's curse).
* Naive contrast: the same calculation with u = 1 (our estimate treated as true cost).
* Choose m maximising expected profit; report win rate and expected profit; contrast with the naive optimum (u = 1).

## 3. Why capable analysts get it wrong

* Naive models treat the own estimate as true cost.
* Winning selects cases where the estimate was low (adverse selection).
* The relevant competitor statistic is the lowest other bid.
* Bidder count strongly shifts the distribution.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `txdot_bid_tabulations_2018_2023.csv` | CSV | ~120k bid lines | TxDOT letting results / bid tabulations | Texas public information (public) | Bids by letting and bidder |
| 2 | `txdot_lettings_2018_2023.csv` | CSV | ~6k lettings | TxDOT | Public | Engineer's estimates, work types |
| 3 | `work_type_codes.json` | JSON | ~30 | Task author | — | Resurfacing filter |
| 4 | `bidding_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `estimator_naive_markup.xlsx` | XLSX | — | Task author | — | Current approach |
| 6 | `winners_curse_reference.pdf` | PDF | — | Capen, Clapp & Campbell 1971 (cite) | Cite | Concept |
| 7 | `letting_class_summary.parquet` | Parquet | ~1k | Derived | Public | Filtered lettings |

## 5. Deterministic solution path

1. Filter lettings and bids; compute competitor low-bid ratios by leave-one-out.
2. Simulate win and profit for each markup with the estimation error u.
3. Choose markup; report win rate and profit; naive contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — profit ignoring estimation error (u = 1).** Overly low markup.

**B — using the winning bid distribution.** Wrong competitor statistic.

**C — pooling all bidder counts.** Misestimated win probabilities.

**D — maximising win rate.** Wrong objective.

## 7. Why the stump is analytical, not semantic

The filters, distributions and simulation are specified. The trap is adverse selection in competitive bidding.

## 8. Draft task prompt (prose)

> What markup should we bid on next year's TxDOT resurfacing lettings? Model competitor low bids from the tabulations and include the winner's
> curse as the bidding memo specifies. Provide `markup_sweep.csv` (markup: win rate, expected profit naive and adjusted), `profit_curve.png`, and a
> one-page `bidding_policy.pdf`.

## 9. Deliverables

* `markup_sweep.csv`, `profit_curve.png`, `bidding_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* Optimal markup; win rate; expected profit; sweep at 10 markups (adjusted and naive); competitor distribution quantiles.

## 11. Golden-output checklist

* Filters; leave-one-out; estimation-error model; simulation seed; optimisation; contrast.

## 12. Build notes (scope tuning)

* Confirm the adjusted optimum markup exceeds the naive optimum by ≥ 2 percentage points.
