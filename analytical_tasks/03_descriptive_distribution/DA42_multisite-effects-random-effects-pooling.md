# DA42 — Pooling an effect measured at many sites: simple averages hide heterogeneity

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Pooling A/B-test results across markets or surfaces (experimentation platforms at large tech companies), multi-store pilots, multi-centre trials |
| Domain | Behavioural research / experimentation |
| Task shape | 07 · Grid of cells (6 effects × 4 statistics → pooled estimate, τ, I², prediction interval; the effect "productised" because its prediction interval excludes zero) |
| Core method | Per-site standardised effects and variances; DerSimonian–Laird random-effects pooling; between-site heterogeneity τ² and I²; 95% prediction interval for a new site; comparison with unweighted averages and fixed-effect pooling |
| Analytical stump | Averaging site effects ignores precision; fixed-effect pooling assumes one true effect and produces narrow intervals even when sites disagree. A product decision about deploying in a *new* market needs the prediction interval, which can include zero even when the pooled mean is clearly positive |
| Primary sources | Many Labs 2 replication project data (site-level effects; Open Science Framework) |

## 1. The real-world situation

A behavioural-design team considers productising nudges whose effects were replicated across many labs worldwide. The team's rule is to
productise only effects that will very likely work in a new market. An analyst averaged site effects and reported six effects as reliably
positive. The experimentation lead asked for random-effects pooling and prediction intervals.

## 2. The decision (one deterministic recommendation)

**The effects productised: those whose 95% prediction interval for a new site lies entirely above zero, with pooled estimates and
heterogeneity statistics for all six candidates.**

Rules (experimentation memo):

* Data: Many Labs 2 site-level summary data for the 6 effects listed in the memo (standardised effect sizes and sampling variances per site).
* Pooling: DerSimonian–Laird τ²; random-effects weights 1 ÷ (v_i + τ²); pooled mean and SE.
* I² = max(0, (Q − df) ÷ Q).
* Prediction interval: pooled mean ± t_{k−2, 0.975} × √(SE² + τ²) (Higgins et al.).
* Productise if the lower bound > 0.
* Report unweighted mean and fixed-effect estimate for contrast.

## 3. Why capable analysts get it wrong

* Averages of site effects are simple and intuitive.
* Precision differs across sites; weighting matters.
* Heterogeneity is the key quantity for generalisation; confidence intervals of the mean do not describe a new site.
* The t-distribution with k−2 df widens intervals with few sites.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ML2_site_level_effects.csv` | CSV | ~3k (effect × site) | Many Labs 2 (OSF) | CC0 / CC BY 4.0 (per OSF project; verify) | Site effects and variances |
| 2 | `ML2_raw_data_slate1.csv`, `ML2_raw_data_slate2.csv` | CSV | ~15k participants each | Many Labs 2 (OSF) | Same | Participant data (for recomputation) |
| 3 | `ML2_codebook.pdf` | PDF | — | OSF | Same | Variables |
| 4 | `klein_2018_many_labs_2_citation.pdf` | PDF | — | Klein et al., AMPPS 2018 (cite) | Cite | Design |
| 5 | `effects_in_scope.json` | JSON | 6 | Task author | — | Candidate effects |
| 6 | `experimentation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `analyst_average_effects.xlsx` | XLSX | 6 | Task author | — | Naive results |
| 8 | `higgins_prediction_interval_citation.pdf` | PDF | — | Cite | Cite | Method |
| 9 | `dl_check_values.json` | JSON | ~5 | Task author | — | Toy meta-analysis |

## 5. Deterministic solution path

1. Load site effects and variances for the six effects.
2. Q, τ², I², random-effects pooled mean and SE.
3. Prediction intervals; productisation list.
4. Contrast with unweighted and fixed-effect results.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted average with SD across sites.** Precision ignored.

**B — fixed-effect pooling.** Overconfident.

**C — confidence interval instead of prediction interval.** Answers a different question.

**D — normal quantile instead of t_{k−2}.** Intervals too narrow.

## 7. Why the stump is analytical, not semantic

The data and formulas are specified. The trap is generalisation under between-site heterogeneity.

## 8. Draft task prompt (prose)

> Which of the six replicated effects should we productise? Pool the site results with random effects and use prediction intervals as the
> experimentation memo specifies. Provide `pooled_effects.csv` (effect: sites, pooled mean, SE, τ, I², PI, fixed-effect, unweighted),
> `forest_summaries.png`, and a one-page `productisation_decision.pdf`.

## 9. Deliverables

* `pooled_effects.csv`, `forest_summaries.png`, `productisation_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 effects × (mean, τ, I², PI bounds) = 30; list; contrasts; toy check.

## 11. Golden-output checklist

* DL estimator; weights; I²; PI formula with t; decision.

## 12. Build notes (scope tuning)

* Choose effects including one with a clearly positive pooled mean but large τ so its PI includes zero.
