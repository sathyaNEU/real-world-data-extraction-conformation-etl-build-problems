# DS21 — Picking seed hybrids from yield trials: the top of a noisy table is partly luck

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Selecting the "best" option from noisy multi-site evaluations (ML models across benchmarks, store formats across pilot sites, vendors across regions) |
| Domain | Agriculture / seed procurement |
| Task shape | 01 · Ranked list under a cap (5 hybrids purchased for next season from ~120 tested, ranked by predicted performance) |
| Core method | Linear mixed model on plot yields: yield = location + hybrid + hybrid × location + error, with hybrid and interaction as random effects; best linear unbiased predictions (BLUPs) of hybrid effects (shrunk by number of locations and reps); rank by BLUP; compare with ranking by raw mean yield across the locations each hybrid was tested in |
| Analytical stump | Ranking by raw means rewards hybrids tested in few, high-yield locations and those with lucky plots; unbalanced testing makes raw means incomparable. BLUPs adjust for location effects and shrink noisy estimates, changing the top five |
| Primary sources | University corn performance test results (e.g., Iowa State University Crop Performance Testing, plot/entry-level yield by location) |

## 1. The real-world situation

A cooperative chooses **5** corn hybrids to stock for members next season. The agronomist ranked all entries by average yield across the trial
locations where they were tested and picked the top five; two of them had been tested in only three high-yield locations.

## 2. The decision (one deterministic recommendation)

**The 5 hybrids purchased, ranked by BLUP of hybrid effect from the mixed model, and the 6th.**

Rules (agronomy memo):

* Data: performance test results for the maturity zone and two seasons in memo; entry × location × replicate yields (bu/acre, adjusted to 15.5%
  moisture as reported).
* Eligibility: hybrids tested in ≥ 4 locations in at least one season.
* Model: yield_ijk = μ + season-location_j (fixed) + hybrid_i (random) + hybrid × season-location_ij (random) + e_ijk; REML estimation.
* BLUP_i for hybrid; rank; top 5; report #6.
* Contrast: raw mean across tested locations.

## 3. Why capable analysts get it wrong

* Average yield tables are what trial reports print.
* Unbalanced designs confound hybrid and location.
* Noise across plots and locations inflates extremes.
* G×E interaction must be modelled to avoid over-crediting specific locations.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `corn_performance_test_<season>_plots.csv` (2 seasons) | CSV | ~20k plots each | University crop performance testing programme (public results) | Public (cite programme) | Plot yields |
| 2 | `corn_performance_test_<season>_report.pdf` | PDF | — | Same | Public | Published tables |
| 3 | `location_metadata.csv` | CSV | ~20 | Same | Public | Locations, management |
| 4 | `agronomy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `agronomist_raw_ranking.xlsx` | XLSX | ~120 | Task author | — | Naive ranking |
| 6 | `mixed_model_reference.pdf` | PDF | — | Cite (Piepho; Smith et al.) | Cite | BLUP in variety trials |
| 7 | `reml_check_values.json` | JSON | — | Task author | — | Variance components check |

## 5. Deterministic solution path

1. Assemble plots; filter maturity zone and eligibility.
2. Fit the mixed model; variance components; BLUPs.
3. Rank; top 5 + #6; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — raw means.** Location and noise effects.

**B — hybrid as fixed effect without shrinkage.** No regression to the mean.

**C — ignoring G×E.** Overstates differences.

**D — including hybrids tested in 1–2 locations.** Noise dominates.

## 7. Why the stump is analytical, not semantic

Model and eligibility are specified. The trap is selection on noisy, unbalanced means.

## 8. Draft task prompt (prose)

> Which five hybrids should we stock? Fit the mixed model in the agronomy memo to the trial plots and rank by BLUP. Provide `hybrid_blups.csv`
> (hybrid: locations, raw mean, BLUP, rank), `raw_vs_blup.png`, and a one-page `hybrid_selection.pdf`.

## 9. Deliverables

* `hybrid_blups.csv`, `raw_vs_blup.png`, `hybrid_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 hybrids + #6; variance components; BLUPs for 10 hybrids; contrast; eligibility exclusions.

## 11. Golden-output checklist

* Filters; model specification; REML; BLUP ranking; contrast.

## 12. Build notes (scope tuning)

* Confirm at least two of the raw top five drop out.
