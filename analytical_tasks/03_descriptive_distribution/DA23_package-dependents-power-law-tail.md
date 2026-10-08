# DA23 — How heavy is the tail of open-source dependencies? A straight line on a log-log plot is not an estimate

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Software-supply-chain security teams sizing the "blast radius" of popular packages; app-store and creator-economy teams describing long-tail download distributions |
| Domain | Software ecosystems / security |
| Task shape | 14 · Cuts of a distribution (tail exponent, xmin and the share of all dependency links captured by the top 0.1%, 1% and 5% of packages in 3 ecosystems; the ecosystem prioritised for a funding programme) |
| Core method | Clauset–Shalizi–Newman: discrete power-law MLE for α above xmin, xmin chosen by minimising the Kolmogorov–Smirnov distance; likelihood-ratio (Vuong) comparison with a lognormal tail; empirical concentration shares computed directly |
| Analytical stump | Least-squares lines on log-log histograms or rank plots give biased exponents and invite "power law" claims that lognormals fit equally well. Funding priorities depend on concentration at the top, which should be read empirically, while the tail model must be estimated by MLE with a principled xmin |
| Primary sources | Libraries.io open data (projects and dependencies) |

## 1. The real-world situation

An open-source security foundation funds maintainers of critical packages in one ecosystem this year — the ecosystem where dependency
links are most concentrated in a few packages. A draft report fitted straight lines to log-log histograms of dependents counts, claimed a
power-law exponent near 2 for all three ecosystems, and inferred equal concentration.

## 2. The decision (one deterministic recommendation)

**The ecosystem prioritised (highest share of dependency links pointing to its top 1% of packages), with α, xmin and the lognormal
comparison for each ecosystem.**

Rules (research memo):

* Data: Libraries.io dependencies snapshot; ecosystems npm, PyPI and Maven; runtime dependencies on the latest version of each project.
* Dependents count per package = number of distinct dependent projects (latest versions) referencing it.
* Concentration: sort packages by dependents; share of all links captured by the top 0.1%, 1%, 5% of packages (with dependents ≥ 1).
* Tail model: discrete power law fitted by MLE for each candidate xmin among unique values up to the 99.9th percentile; choose xmin
  minimising KS distance; report α and n_tail.
* Comparison: normalised log-likelihood ratio R and p-value versus a discrete lognormal on the same tail (Vuong test); "power law favoured"
  only if R > 0 and p < 0.1.
* Priority: highest top-1% link share.

## 3. Why capable analysts get it wrong

* Log-log regression is common and visually convincing.
* Binning and the choice of where the tail starts drive the slope.
* Heavy-tailed alternatives are hard to distinguish; formal comparisons are needed.
* The decision rests on concentration, which needs no model.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `projects-<version>.csv` | CSV | ~4–5M | Libraries.io open data | CC BY-SA 4.0 | Projects, platforms |
| 2 | `dependencies-<version>.csv` | CSV | ~200M (3-ecosystem extract ~60M) | Libraries.io open data | CC BY-SA 4.0 | Dependency links |
| 3 | `versions-<version>.csv` | CSV | ~20M | Libraries.io | CC BY-SA 4.0 | Latest versions |
| 4 | `librariesio_data_readme.html` | HTML | — | Libraries.io | CC BY-SA 4.0 | Schema |
| 5 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `draft_report_loglog_fits.xlsx` | XLSX | 3 | Task author | — | Draft results |
| 7 | `clauset_2009_citation.pdf` | PDF | — | Clauset, Shalizi & Newman, SIAM Review 2009 (cite) | Cite | Method |
| 8 | `dependents_counts.parquet` | Parquet | ~3M | Derived | CC BY-SA 4.0 | Counts per package |
| 9 | `powerlaw_check_values.json` | JSON | ~6 | Task author | — | Checks on a known sample |
| 10 | `dependency_kind_rules.json` | JSON | — | Task author | — | Runtime filter |

## 5. Deterministic solution path

1. Filter ecosystems, latest versions and runtime kinds; count dependents.
2. Concentration shares.
3. xmin search, α MLE, KS; lognormal comparison.
4. Priority; contrast with the draft.

## 6. Wrong paths (method errors, not misreadings)

**A — log-log OLS.** Biased α.

**B — fixed xmin = 1.** Body contaminates the tail fit.

**C — no alternative comparison.** Overclaims power law.

**D — counting all versions' dependencies.** Inflated links.

## 7. Why the stump is analytical, not semantic

Counts and methods are specified. The trap is estimating heavy tails by regression on plots and deciding on model fit rather than the
descriptive quantity that matters.

## 8. Draft task prompt (prose)

> Which ecosystem's critical packages should we fund first? Measure concentration of dependency links and fit tail models properly as the
> research memo specifies. Provide `ecosystem_tails.csv` (ecosystem: packages, links, top-0.1/1/5% shares, xmin, α, R, p), `ccdf_plots.png`
> (empirical CCDFs with fitted tails), and a one-page `funding_priority.pdf`.

## 9. Deliverables

* `ecosystem_tails.csv`, `ccdf_plots.png`, `funding_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 ecosystems × (3 shares + xmin + α + n_tail + R + p) = 24; priority; contrast with the draft.

## 11. Golden-output checklist

* Filters; counts; shares; xmin search; MLE; Vuong; priority.

## 12. Build notes (scope tuning)

* Record the snapshot version; confirm the draft's equal-exponent claim is contradicted by α estimates or the lognormal comparison.
