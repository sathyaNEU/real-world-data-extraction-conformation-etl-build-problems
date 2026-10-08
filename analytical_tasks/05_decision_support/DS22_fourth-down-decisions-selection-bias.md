# DS22 — Go for it on fourth down? Observed conversion rates come from the situations coaches chose

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Decision rules estimated from observational outcomes where actions were chosen selectively (sales reps' discretionary discounts, clinicians' treatment choices, support escalations) |
| Domain | Sports analytics |
| Task shape | 07 · Grid of cells (yards to go × field position → recommended action: go, punt, or field goal; the decision chart adopted by the coaching staff) |
| Core method | Win-probability model (from play-by-play) for the states after each action; conversion probability estimated from *all* 3rd-and-short and 4th-down attempts with a model including yards to go, field position and offense/defense strength (to reduce selection), punt net distance and field-goal make probability by distance; choose the action with the highest expected win probability per cell |
| Analytical stump | Raw 4th-down conversion rates are biased: teams go for it when they expect to convert (short yardage, strong offence, weak defence). Using them (or punting because "it usually works") gives the wrong chart. Conversion must be modelled with situational covariates and borrowing from comparable 3rd-down plays |
| Primary sources | nflverse play-by-play data (nflfastR) |

## 1. The real-world situation

A team's analytics staff builds a fourth-down decision chart for the coach. The first version used observed conversion rates by yards to go and
punt outcomes; it recommended going for it from 4th-and-6 in midfield, because observed conversions there were high. Staff noticed only a few
teams attempted those, mostly late in games and with elite offences.

## 2. The decision (one deterministic recommendation)

**The decision chart (go/punt/FG) for yards to go 1–10 × field position bands (own 20 to opponent 5 in 5-yard bands), for a neutral game state
(score tied, 2nd quarter), and the cells that differ from the observed-rate chart.**

Rules (analytics memo):

* Data: nflverse play-by-play 2016–2023 regular seasons.
* Conversion model: logistic regression of success (first down or TD) on yards to go (splines), field position, down (3rd vs 4th indicator),
  offensive and defensive EPA/play (season-to-date), fitted on 3rd- and 4th-down runs/passes; predict for 4th down with league-average team
  strengths.
* Punt: mean net yards by field position band; touchback rules; FG: make probability by kick distance (logistic), with miss at spot.
* Win probability: nflverse WP model values for resulting states (or the memo's WP lookup table).
* Choose action maximising expected WP; ties → conventional action (punt/FG).
* Contrast chart: observed 4th-down conversion rates by yards to go and field position.

## 3. Why capable analysts get it wrong

* Observed rates seem like empirical truth.
* Attempts are selected; conditions differ from the average situation.
* Third-down plays provide comparable information with less selection.
* Decisions require win probability, not yards or points alone.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–8 | `play_by_play_<yyyy>.parquet` (2016–2023) | Parquet | ~50k plays each | nflverse-data releases | CC BY 4.0 (nflverse data licence; verify) | Plays with EPA, WP |
| 9 | `nflverse_pbp_field_descriptions.csv` | CSV | ~370 | nflverse | Same | Fields |
| 10 | `analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `observed_rate_chart.xlsx` | XLSX | 10 × 15 | Task author | — | Naive chart |
| 12 | `wp_lookup_table.parquet` | Parquet | ~100k states | Derived from nflverse WP | Same | Win probability |
| 13 | `fourth_down_research_citation.pdf` | PDF | — | Cite (Romer 2006; Burke) | Cite | Context |

## 5. Deterministic solution path

1. Filter plays; fit conversion, punt and FG models.
2. For each cell, compute expected WP for go, punt, FG.
3. Choose actions; chart; contrast with the observed-rate chart.

## 6. Wrong paths (method errors, not misreadings)

**A — observed 4th-down rates.** Selection bias.

**B — expected points instead of win probability.** Not the memo's objective (close in neutral states, but differs near the end zone).

**C — no team-strength adjustment.** Strong offences over-represented.

**D — ignoring missed-FG field position.** FG overvalued.

## 7. Why the stump is analytical, not semantic

The models and objective are specified. The trap is learning decision values from selectively chosen actions.

## 8. Draft task prompt (prose)

> Build the fourth-down chart for a neutral game state. Use the conversion, punt and kick models in the analytics memo with win probability, and show
> where it differs from the observed-rate chart. Provide `decision_chart.csv` (cell: WP go, punt, FG, action), `decision_chart.png`, and a one-page
> `fourth_down_policy.pdf`.

## 9. Deliverables

* `decision_chart.csv`, `decision_chart.png`, `fourth_down_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 150 cells (sampled 30 checks); model coefficients; differing cells; FG make curve.

## 11. Golden-output checklist

* Filters; conversion model with selection controls; punt/FG models; WP evaluation; ties.

## 12. Build notes (scope tuning)

* Publish the WP lookup to make grading deterministic; confirm ≥ 10 cells differ from the observed-rate chart.
