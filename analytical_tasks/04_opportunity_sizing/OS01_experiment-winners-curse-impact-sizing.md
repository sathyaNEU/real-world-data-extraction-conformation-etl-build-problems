# OS01 — Summing the lifts of winning experiments: the winners' curse inflates the programme's impact

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Experimentation-programme reporting at large online companies (annual "impact" of shipped A/B winners), growth-team roadmaps sized from past test results |
| Domain | Digital media / experimentation |
| Task shape | 03 · Bridge between two totals (naively summed lift of shipped winners → shrinkage-adjusted expected lift; the programme budget decision) |
| Core method | Empirical-Bayes shrinkage of per-test lift estimates toward the prior distribution of true effects (normal prior fitted by method of moments across all tests, accounting for sampling variance); expected true lift of the selected winners; bridge items: selection, noise, multiple arms |
| Analytical stump | Choosing the best-performing variant in each test and then reporting its observed lift selects on noise; the expected true lift of a winner is much smaller. Summing observed winner lifts across hundreds of tests overstates impact, sometimes several-fold, and the programme's sized value flips the funding call |
| Primary sources | The Upworthy Research Archive (headline A/B tests with impressions and clicks per package) |

## 1. The real-world situation

A media company's growth team asks for a larger experimentation budget, sizing the value of its headline-testing programme as the sum of the
observed click-through lifts of each test's winning headline over the control-equivalent average. Finance asked for an estimate that
accounts for the fact that winners are selected because they did well in noisy data.

## 2. The decision (one deterministic recommendation)

**The expected annual incremental clicks from shipping winners (shrinkage-adjusted), and whether it clears the budget threshold of 25 million
clicks in the memo.**

Rules (finance memo):

* Data: Upworthy Research Archive exploratory and confirmatory test packages; tests with ≥ 2 packages and ≥ 1,000 impressions per package.
* Per test: winner = package with highest CTR; baseline = impressions-weighted mean CTR of the other packages; observed lift = CTR_winner −
  baseline (absolute).
* Sampling variance of the lift: binomial variance of the winner's CTR plus that of the baseline (per memo).
* Prior: true lifts of a *random* package versus its test mean ~ N(0, τ²) with τ² = var(package deviations) − mean sampling variance, using all
  packages (not just winners).
* Shrunken winner lift = observed × τ² ÷ (τ² + v_winner).
* Annual incremental clicks = Σ over tests of shrunken lift × the test's post-test impressions (from `post_test_impressions.csv`, memo
  convention: 1 year of traffic at the test's impressions rate × 50).
* Fund if ≥ 25 million.

## 3. Why capable analysts get it wrong

* Winner lift is the natural "result" of a test.
* Selection of the maximum of several noisy estimates biases upward; more arms → more bias.
* The prior must be estimated from all packages, not from winners.
* Small tests carry the largest noise and the largest apparent lifts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `upworthy-archive-exploratory-packages-03.12.2020.csv` | CSV | ~22.7k packages | Upworthy Research Archive (Matias et al.) | CC BY 4.0 | Exploratory tests |
| 2 | `upworthy-archive-confirmatory-packages-03.12.2020.csv` | CSV | ~105k packages | Same | CC BY 4.0 | Confirmatory tests |
| 3 | `upworthy-archive-holdout-packages-03.12.2020.csv` | CSV | ~28k | Same | CC BY 4.0 | Holdout (context) |
| 4 | `upworthy_archive_datasheet.pdf` | PDF | — | Matias et al., Scientific Data 2021 (cite) | CC BY 4.0 | Data description |
| 5 | `post_test_impressions.csv` | CSV | ~30k tests | Task author (memo convention) | — | Traffic assumption |
| 6 | `finance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `growth_team_sizing.xlsx` | XLSX | ~30k | Task author | — | Naive sum |
| 8 | `eb_shrinkage_reference.pdf` | PDF | — | Cite (Efron & Morris; experimentation literature) | Cite | Method |
| 9 | `test_level_summary.parquet` | Parquet | ~30k | Derived | CC BY 4.0 | Convenience |

## 5. Deterministic solution path

1. Filter tests and packages; compute CTRs, winners, baselines, observed lifts and variances.
2. Estimate τ² from all package deviations.
3. Shrink winner lifts; compute annual clicks; compare with the naive sum.
4. Bridge: naive → shrunken, decomposed by test size bands.

## 6. Wrong paths (method errors, not misreadings)

**A — sum of observed winner lifts.** Overstated impact.

**B — prior estimated from winners.** Prior too wide; little shrinkage.

**C — relative lifts on tiny baselines.** Explodes for low-CTR tests.

**D — ignoring the number of arms.** Bias differs by test.

## 7. Why the stump is analytical, not semantic

Selection and shrinkage rules are specified. The trap is selection bias from picking maxima of noisy estimates.

## 8. Draft task prompt (prose)

> What is our headline-testing programme really worth per year, and does it clear the funding bar? Apply the shrinkage method in the finance
> memo to the Upworthy tests and bridge from the growth team's figure. Provide `impact_bridge.csv` (step: clicks), `observed_vs_shrunken.png`
> (winner lifts before and after shrinkage by test size), and a one-page `programme_funding.pdf`.

## 9. Deliverables

* `impact_bridge.csv`, `observed_vs_shrunken.png`, `programme_funding.pdf`.

## 10. Where 25+ rubric criteria come from

* τ²; naive and shrunken totals; bridge by 5 size bands × 2 = 10; 8 example tests; decision.

## 11. Golden-output checklist

* Filters; winner/baseline definitions; variance; prior from all packages; shrinkage; traffic convention; decision.

## 12. Build notes (scope tuning)

* Set the threshold between the naive and shrunken totals; confirm the ratio naive ÷ shrunken ≥ 2.
