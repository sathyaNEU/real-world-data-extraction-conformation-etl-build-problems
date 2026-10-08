# DA45 — How stable is a top-sites list? Set overlap ignores order and treats rank 1 like rank 10,000

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Stability of ranked outputs at search, app-store and recommendation teams (top-chart churn, search-result volatility, model-ranking drift) |
| Domain | Internet measurement / security research |
| Task shape | 07 · Grid of cells (3 list providers × 4 depth cut-offs → daily stability by rank-biased overlap; the provider adopted as the measurement sampling frame) |
| Core method | Rank-biased overlap (RBO, Webber et al.) with persistence p (top-weighted similarity) between consecutive days' lists; comparison with Jaccard similarity of top-k sets; mean and 5th percentile over 30 day-pairs |
| Analytical stump | Jaccard of top-k sets treats a swap between ranks 1 and 1,000 the same as no change and is dominated by churn in the long tail; it also depends heavily on k. RBO weights agreement at the top and supports unequal depth; the provider choice depends on which similarity reflects the use case |
| Primary sources | Tranco research-oriented top-sites ranking (daily lists), plus two other public lists archived by the Tranco project (e.g., Cisco Umbrella, Majestic) |

## 1. The real-world situation

A security-measurement team must pick a top-sites list as the sampling frame for weekly crawls; results must not change merely because the
list reshuffled. The analyst compared providers by Jaccard similarity of the top 100,000 between consecutive days and picked the most "stable"
one. A researcher noted that the crawls weight sites by rank (the top 10,000 drive most findings).

## 2. The decision (one deterministic recommendation)

**The list provider adopted: highest mean RBO (p = 0.999, evaluated to depth 100,000) between consecutive days over the 30-day window, with the
RBO/Jaccard grid for all providers.**

Rules (measurement memo):

* Data: daily lists for 31 consecutive days (dates in memo) from the three providers (as archived by Tranco).
* Normalisation: registrable domain (eTLD+1) via the Public Suffix List snapshot provided; keep first occurrence rank.
* RBO: extrapolated RBO (RBO_ext) per Webber et al. at depth 100,000 with p = 0.999.
* Jaccard: top-k sets for k = 1,000, 10,000, 100,000.
* Statistics per provider: mean and 5th percentile over 30 consecutive-day pairs.
* Adopt the highest mean RBO; ties → higher 5th percentile.

## 3. Why capable analysts get it wrong

* Set overlap is a natural similarity measure.
* Top-weighted similarity reflects what matters when importance decays with rank.
* Jaccard depends strongly on k; long tails churn more.
* Domain normalisation affects matches (subdomains versus registrable domains).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–31 | `tranco_<date>.csv` | CSV | 1M each | Tranco list (tranco-list.eu) | Tranco terms (free for research; cite) | Daily Tranco lists |
| 32–62 | `umbrella_<date>.csv` | CSV | 1M each | Archived via Tranco project (Cisco Umbrella public list) | Provider terms (verify) | Provider B |
| 63–93 | `majestic_<date>.csv` | CSV | 1M each | Majestic Million (CC BY 3.0) | CC BY 3.0 | Provider C |
| 94 | `public_suffix_list.dat` | Text | ~10k | Mozilla Public Suffix List | MPL 2.0 | Normalisation |
| 95 | `measurement_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 96 | `analyst_jaccard_comparison.xlsx` | XLSX | 3 | Task author | — | Naive choice |
| 97 | `webber_2010_rbo_citation.pdf` | PDF | — | Cite | Cite | RBO |
| 98 | `rbo_check_values.json` | JSON | ~5 | Task author | — | Small-list checks |

## 5. Deterministic solution path

1. Load and normalise lists; de-duplicate.
2. Compute RBO_ext and Jaccard for each consecutive pair.
3. Aggregate per provider; adopt by rule.
4. Contrast with the analyst's Jaccard choice.

## 6. Wrong paths (method errors, not misreadings)

**A — Jaccard at k = 100,000.** Long-tail churn dominates.

**B — Spearman correlation on the intersection only.** Ignores entries and exits.

**C — no domain normalisation.** Spurious churn.

**D — RBO without extrapolation at finite depth.** Not the memo's estimator.

## 7. Why the stump is analytical, not semantic

The measures and parameters are specified. The trap is choosing a similarity measure that does not reflect rank importance.

## 8. Draft task prompt (prose)

> Which top-sites list should we use as our crawl frame? Compare daily stability with rank-biased overlap as the measurement memo specifies,
> alongside Jaccard at three depths. Provide `stability_grid.csv` (provider × measure: mean, 5th percentile), `daily_rbo.png`, and a one-page
> `frame_selection.pdf`.

## 9. Deliverables

* `stability_grid.csv`, `daily_rbo.png`, `frame_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 providers × 4 measures × 2 statistics = 24; adoption; checks; contrast.

## 11. Golden-output checklist

* Normalisation; RBO_ext; Jaccard depths; aggregation; adoption rule.

## 12. Build notes (scope tuning)

* Confirm the Jaccard-at-100k leader differs from the RBO leader.
