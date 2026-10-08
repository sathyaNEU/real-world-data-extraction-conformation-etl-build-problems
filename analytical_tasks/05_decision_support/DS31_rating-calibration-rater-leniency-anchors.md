# DS31 — Ranking items by average rating: who rated them matters as much as how good they are

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Rating calibration on two-sided platforms (adjusting driver or host ratings for rider/guest harshness) and performance-review calibration across managers |
| Domain | Content platforms / ratings |
| Task shape | 01 · Ranked list under a cap (20 items featured in a "best of" collection, ranked by leniency-adjusted rating) |
| Core method | Estimate each rater's leniency from a common anchor set that every rater scored (the gauge items): leniency_r = rater's mean on anchors − overall anchor mean; adjust each non-anchor rating by subtracting leniency; item score = mean adjusted rating with Bayesian shrinkage to the global mean (prior weight per memo); rank |
| Analytical stump | Raw item means depend on which raters chose to rate each item: items rated mostly by enthusiastic (lenient) raters look better. Without calibration, the featured list over-represents items favoured by lenient rater segments; anchor items make leniency estimable |
| Primary sources | Jester online joke recommender datasets (UC Berkeley; continuous ratings −10 to +10 with a gauge set rated by all users) |

## 1. The real-world situation

A content platform will feature **20** items in a "best of" collection. The draft ranked items by average rating. The ratings team noticed that
heavy raters of niche items are systematically more generous, and that every user rated the same small onboarding set, which could serve as an
anchor for calibration.

## 2. The decision (one deterministic recommendation)

**The 20 featured items (by leniency-adjusted, shrunk mean rating), the 21st, and the items whose inclusion differs from the raw-mean list.**

Rules (ratings memo):

* Data: Jester dataset (version in memo); ratings −10 to +10; the gauge set (items listed in the dataset documentation) rated by all users.
* Raters: users with all gauge items rated and ≥ 5 non-gauge ratings.
* Leniency_r = mean(rater's gauge ratings) − mean over all raters of gauge means.
* Adjusted rating = rating − leniency_r.
* Item score = (Σ adjusted + m × μ) ÷ (n + m), μ = global mean adjusted rating, m = 30 (memo).
* Candidates: non-gauge items with ≥ 200 ratings; rank; top 20; report #21.
* Raw contrast: mean raw rating with the same eligibility.

## 3. Why capable analysts get it wrong

* Average ratings are the default ranking.
* Rater populations differ by item; leniency is confounded with quality.
* Anchors provide a common reference that removes rater effects.
* Shrinkage stabilises items with fewer ratings.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `jester_ratings.csv` (dataset version in memo) | CSV | ~1.7M ratings | Jester datasets (UC Berkeley, Goldberg et al.) | Free for research use (cite; verify terms) | User × item ratings |
| 2 | `jester_items.csv` | CSV | ~150 | Same | Same | Item texts, gauge flags |
| 3 | `jester_readme.txt` | Text | — | Same | Same | Gauge set, rating scale |
| 4 | `goldberg_2001_citation.pdf` | PDF | — | Goldberg et al., Information Retrieval 2001 (cite) | Cite | Dataset description |
| 5 | `ratings_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `raw_mean_list.xlsx` | XLSX | ~140 | Task author | — | Raw ranking |
| 7 | `calibration_check.json` | JSON | — | Task author | — | Check values for 5 raters |

## 5. Deterministic solution path

1. Filter raters; compute gauge leniency.
2. Adjust non-gauge ratings; shrunk item scores.
3. Rank; top 20 + #21; differences from the raw list.

## 6. Wrong paths (method errors, not misreadings)

**A — raw means.** Rater mix confounds.

**B — z-scoring each rater on all their ratings.** Mixes item choice with leniency.

**C — no shrinkage.** Small-n items at extremes.

**D — including gauge items as candidates.** Not the memo's scope.

## 7. Why the stump is analytical, not semantic

The anchor set and formulas are specified. The trap is unadjusted aggregation across heterogeneous raters.

## 8. Draft task prompt (prose)

> Which 20 items should we feature? Calibrate ratings for rater leniency using the anchor set and rank with shrinkage as the ratings memo specifies.
> Provide `calibrated_items.csv` (item: n, raw mean, adjusted shrunk score, rank), `leniency_distribution.png`, and a one-page `featured_list.pdf`.

## 9. Deliverables

* `calibrated_items.csv`, `leniency_distribution.png`, `featured_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 items + #21; scores for 8 boundary items; leniency checks; differences from raw list.

## 11. Golden-output checklist

* Rater filter; leniency; adjustment; shrinkage; eligibility; ranking.

## 12. Build notes (scope tuning)

* Confirm at least four items differ between raw and calibrated top-20 lists.
