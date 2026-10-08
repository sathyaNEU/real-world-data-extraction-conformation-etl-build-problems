# RC27 — A health plan lost its 4.5-star rating and its bonus: did the plan get worse, or did everyone else get better?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Relative grading systems (app-store ranking percentiles, seller ratings banded against peers, performance reviews on a curve) where the threshold moves with the field |
| Domain | Health insurance / Medicare Advantage quality |
| Task shape | 03 · Bridge between two totals (overall summary rating before rounding, last year → this year, bridged by own-performance changes and cut-point shifts per measure, reward factor and the categorical adjustment, then rounding) |
| Core method | For each measure, star change split into own-performance (this year's score on last year's cut points minus last year's star) and cut-point shift (this year's star minus this year's score on last year's cut points); weighted average using measure weights; reward-factor and CAI changes as separate lines; show the half-star rounding threshold crossed |
| Analytical stump | Measure scores moved little, so executives search for which measures "dropped", but stars are assigned against cut points that are recalculated every year from all contracts' scores (with clustering, outlier trimming and guardrails). Small cut-point increases across many measures, plus a summary score sitting just above a half-star rounding threshold, explain the loss. Attributing each star change to own performance misallocates almost all of it |
| Primary sources | CMS Medicare Part C and D Star Ratings data tables (measure scores, measure stars, cut points, summary ratings, reward factor and CAI tables) |

## 1. The real-world situation

A Medicare Advantage contract's overall rating fell from 4.5 to 4.0 stars, costing it the quality bonus on its benchmark and rebate share. The
quality team was told to find which measures "fell" and fix them. The CFO asked whether the plan actually got worse or the cut points moved, because
the answer changes where next year's improvement money goes.

## 2. The decision (one deterministic recommendation)

**The primary cause of the rating loss — cut-point shifts or own-performance changes — by weighted contribution to the change in the unrounded
summary score, and the three measures with the largest weighted own-performance losses.**

Rules (quality memo):

* Data: CMS Star Ratings data tables for the two rating years for the memo's contract: measure scores, measure stars and cut points (Part C and D,
  MA-PD contract), measure weights, reward factor and CAI values.
* Measures: those rated for the contract in both years with the same specification (memo lists measures excluded for specification changes).
* Star on given cut points: the highest star whose cut-point threshold the score meets (direction per measure: higher-is-better or
  lower-is-better).
* Own-performance effect_m = star(score_cur, cuts_ref) − star_ref; cut-point effect_m = star_cur − star(score_cur, cuts_ref).
* Weighted contribution = weight_m × effect_m ÷ Σ weights (over measures rated in the current year).
* Bridge: unrounded summary_ref → + Σ own-performance + Σ cut-point + Δ(measure set and weights) + Δ reward factor + Δ CAI → unrounded summary_cur;
  closure residual reported.
* Primary cause: the larger of Σ own-performance and Σ cut-point contributions in absolute terms (when the drop is negative, the more negative).
* Rounding: report both unrounded summaries and the half-star threshold crossed.

## 3. Why capable analysts get it wrong

* Stars look like absolute grades.
* Measure-score changes are small and diffuse; star changes are discrete and dramatic.
* Cut points move every year by method, not by fiat.
* Rounding thresholds turn small changes into a full half-star.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `<year>_star_ratings_data_table_measure_data.csv` (2 years) | CSV | ~35k each (contract × measure) | CMS Star Ratings data tables | U.S. Government work (public domain) | Measure scores |
| 2 | `<year>_star_ratings_data_table_measure_stars.csv` | CSV | ~35k each | CMS | Public domain | Measure stars |
| 3 | `<year>_star_ratings_cut_points.csv` | CSV | ~80 each | CMS | Public domain | Cut points by measure |
| 4 | `<year>_star_ratings_summary_ratings.csv` | CSV | ~800 each | CMS | Public domain | Summary ratings |
| 5 | `<year>_reward_factor_cai.xlsx` | XLSX | ~1k each | CMS technical notes tables | Public domain | Reward factor and CAI |
| 6 | `star_ratings_technical_notes_<year>.pdf` | PDF | — | CMS | Public domain | Weights and methodology |
| 7 | `quality_memo.pdf` | PDF | — | Task author | — | Rules in §2, contract ID |
| 8 | `quality_team_measure_list.xlsx` | XLSX | — | Task author | — | The "measures that dropped" list |

## 5. Deterministic solution path

1. Extract the contract's scores and stars, cut points and weights for both years; align measures.
2. Recompute stars from scores and cut points (validate against published stars).
3. Own-performance and cut-point effects per measure; weighted contributions.
4. Reward factor, CAI and measure-set changes; closure; rounding threshold.
5. Primary cause; top 3 own-performance measures; contrast with the quality team's list.

## 6. Wrong paths (method errors, not misreadings)

**A — star changes attributed to own performance.** Every lost star is read as the plan getting worse.

**B — score changes ranked without cut points.** Ranks by raw score movement, which does not map to stars.

**C — unweighted measure counts.** Ignores triple-weighted outcome measures and improvement measures' weights.

**D — rounded summaries compared.** A 0.5-star change is analysed when the unrounded change is small.

## 7. Why the stump is analytical, not semantic

All inputs are published numeric tables; the decomposition is fully specified. The trap is relative grading and discrete thresholds.

## 8. Draft task prompt (prose)

> We lost our 4.5-star rating and the bonus with it. Use the quality memo's method to tell me how much of the drop was our own performance and how
> much was cut points moving, and which measures to prioritise. Provide `star_bridge.csv` (measure: own effect, cut-point effect, weighted
> contributions), `summary_rating_bridge.png`, and a one-page `star_rating_rca.pdf`.

## 9. Deliverables

* `star_bridge.csv` — per-measure effects and contributions, plus the summary bridge lines.
* `summary_rating_bridge.png` — waterfall of the unrounded summary with the 4.25 rounding threshold marked.
* `star_rating_rca.pdf` — primary cause, top 3 measures, and why the quality team's list misleads.

## 10. Where 25+ rubric criteria come from

* Measure alignment and exclusions: 2.
* Star recomputation validated: 2.
* Effects for the 10 highest-weight measures: 10.
* Weighted sums, reward factor, CAI, closure: 6.
* Rounding threshold: 1.
* Primary cause and top 3 measures: 4.
* Contrast: 2.

## 11. Golden-output checklist

* Direction of each measure; star on cut points rule.
* Effects defined in the given order; weights from the current year.
* Bridge closes to the unrounded current summary.

## 12. Build notes (scope tuning)

* Choose a contract whose unrounded summary fell across a half-star threshold with mostly stable scores; confirm that cut-point contributions exceed
  own-performance contributions.
