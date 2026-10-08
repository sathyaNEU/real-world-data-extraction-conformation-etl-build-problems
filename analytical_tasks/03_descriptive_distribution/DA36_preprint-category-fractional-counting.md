# DA36 — Which research area is growing fastest? Cross-listed papers are counted once, not three times

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Multi-label content analytics (posts with several tags, products in several categories, tickets routed to several teams) where category totals exceed the overall total |
| Domain | Research analytics / publishing |
| Task shape | 03 · Bridge between two totals (sum of whole-counted category submissions → total unique submissions; growth ranking by fractional counts and the category that gets a new moderator) |
| Core method | Fractional counting: each paper contributes 1/k to each of its k categories (primary + cross-lists); category growth 2019→2023 on fractional counts; bridge showing double counting; comparison with whole counting and primary-only counting |
| Analytical stump | Whole counting assigns each cross-listed paper fully to every category, so interdisciplinary areas with heavy cross-listing appear to grow fastest and category totals sum to more than all papers. Fractional counting conserves the total and gives growth in actual moderation load per the memo's definition |
| Primary sources | arXiv metadata (OAI-PMH bulk metadata / Kaggle-hosted arXiv metadata snapshot) |

## 1. The real-world situation

A preprint server adds one volunteer moderator to the category whose submission load grew the most from 2019 to 2023. A report counted
every paper in every category it was listed in and named a machine-learning–adjacent category as the fastest growing. Moderators pointed
out that most of its "growth" was cross-lists from another category, whose moderators handle those papers first.

## 2. The decision (one deterministic recommendation)

**The category receiving the new moderator: highest absolute growth in fractional load 2019→2023 among the 20 largest categories, with the
bridge from whole-counted totals to unique submissions.**

Rules (operations memo):

* Data: arXiv metadata snapshot (date in memo); new submissions (version v1 date) in 2019 and 2023.
* Categories: the `categories` field (space-separated); primary = first listed (per arXiv convention).
* Load definition: fractional count — primary category weight 0.5, remaining 0.5 split equally among cross-lists (memo); a paper with no
  cross-lists gives 1.0 to its primary.
* Growth = load(2023) − load(2019); choose among the 20 categories with highest 2023 load.
* Bridge: Σ whole counts → minus duplicate counting from cross-lists → equals unique papers; report whole, primary-only and fractional growth
  for the top 20.

## 3. Why capable analysts get it wrong

* Category listing pages show all papers listed, including cross-lists.
* Whole counting inflates categories with many cross-lists.
* The memo's load definition reflects moderation responsibility, which sits mostly with the primary.
* Version dates must be the first version to measure new submissions.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `arxiv-metadata-oai-snapshot.json` | JSON lines | ~2.4M | arXiv metadata (OAI-PMH; Kaggle mirror) | CC0 1.0 (metadata) | Papers, categories, versions |
| 2 | `arxiv_category_taxonomy.csv` | CSV | ~155 | arXiv category taxonomy page | arXiv terms (public) | Category names |
| 3 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 4 | `growth_report_whole_counts.xlsx` | XLSX | 20 | Task author | — | Earlier report |
| 5 | `fractional_counting_reference.pdf` | PDF | — | Cite (bibliometrics fractional counting) | Cite | Method |
| 6 | `submissions_2019_2023.parquet` | Parquet | ~400k | Derived | CC0 | Filtered papers |
| 7 | `arxiv_monthly_submission_stats.csv` | CSV | ~400 | arXiv stats page | Public | Validation of totals |
| 8 | `category_check_cases.json` | JSON | ~10 | Task author | — | Hand-checked papers |

## 5. Deterministic solution path

1. Parse snapshot; v1 dates; filter years.
2. Parse categories; primary; cross-lists; compute weights.
3. Load per category-year under three methods; top 20; growth; choice.
4. Bridge totals; validate unique counts against arXiv stats.

## 6. Wrong paths (method errors, not misreadings)

**A — whole counting.** Cross-list-heavy categories win.

**B — equal 1/k weights when the memo specifies primary 0.5.** Different load.

**C — latest version date.** Mixes revisions into new submissions.

**D — percentage growth.** Small categories win.

## 7. Why the stump is analytical, not semantic

The weights and definitions are specified. The trap is multi-membership counting that breaks additivity.

## 8. Draft task prompt (prose)

> Which category gets the new moderator? Measure 2019→2023 growth in moderation load with the fractional counting rule in the operations memo
> and reconcile category totals to unique submissions. Provide `category_load.csv` (category: whole, primary-only and fractional load by year,
> growth), `count_bridge.png`, and a one-page `moderator_allocation.pdf`.

## 9. Deliverables

* `category_load.csv`, `count_bridge.png`, `moderator_allocation.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 categories' fractional growth (sampled 12); bridge items; chosen category; contrasts; validation.

## 11. Golden-output checklist

* v1 dates; primary rule; weights; top-20 selection; growth; bridge.

## 12. Build notes (scope tuning)

* Confirm whole counting and fractional counting choose different categories.
