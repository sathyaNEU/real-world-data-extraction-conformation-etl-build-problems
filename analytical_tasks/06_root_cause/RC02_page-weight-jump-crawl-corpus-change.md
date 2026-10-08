# RC02 — Did web pages suddenly get heavier? The crawl list changed underneath the metric

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Metric breaks caused by changes in the measured population (new users added to a panel, a new data source in a dashboard, sampling changes) |
| Domain | Web performance |
| Task shape | 03 · Bridge between two totals (median page weight before → after the jump, bridged by corpus change, device mix and like-for-like growth on pages present in both crawls) |
| Core method | Split the change in median bytes per page into: (1) like-for-like change on URLs crawled in both months, (2) entry/exit of URLs due to the corpus switch, (3) device-client mix; use quantile-preserving decomposition per memo (compute medians on matched panel and on full samples) |
| Analytical stump | Treating a month-over-month jump in the published median as real growth ignores that the crawl corpus changed (e.g., switching seed lists) — new pages differ systematically. A matched-panel (same URLs) comparison reveals the like-for-like change, which is far smaller |
| Primary sources | HTTP Archive (BigQuery public dataset `httparchive`, summary_pages/pages tables) |

## 1. The real-world situation

A performance team's quarterly report highlighted a sharp jump in median mobile page weight in one month and launched an initiative against
bloated third-party scripts. An engineer noted that the HTTP Archive changed its URL corpus that month (moving to a list derived from the Chrome UX
Report), roughly quadrupling the number of pages.

## 2. The decision (one deterministic recommendation)

**The like-for-like change in median mobile page weight across the corpus-change month, and the share of the published jump explained by the corpus
change.**

Rules (performance memo):

* Data: HTTP Archive summary pages for the month before and the month of the corpus change (dates in memo), mobile and desktop clients.
* Metric: median bytesTotal per page (client = mobile unless stated).
* Matched panel: URLs present in both months (normalised origin + path).
* Bridge: published median before → like-for-like change (median on matched URLs, after − before) → composition effect (difference between full
  after median and matched after median) → published median after. Device mix reported separately (desktop/mobile not mixed in the mobile metric).
* Report shares of the jump explained by composition versus like-for-like.

## 3. Why capable analysts get it wrong

* Published medians look like stable time series.
* Corpus changes alter which sites are measured.
* Medians are not additive; the bridge must be built from computed medians on defined sets.
* URL normalisation affects matching.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `summary_pages_<month_before>_mobile.parquet` | Parquet | ~5M | HTTP Archive BigQuery | HTTP Archive data (Apache 2.0 / open; verify) | Page-level summaries |
| 2 | `summary_pages_<month_change>_mobile.parquet` | Parquet | ~7–8M | Same | Same | Same |
| 3 | `summary_pages_<months>_desktop.parquet` | Parquet | ~12M | Same | Same | Desktop (context) |
| 4 | `httparchive_methodology.html` | HTML | — | HTTP Archive | Open | Corpus and crawl notes |
| 5 | `performance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `quarterly_report_chart.xlsx` | XLSX | — | Task author | — | Original claim |
| 7 | `url_normalisation_rules.json` | JSON | — | Task author | — | Matching |
| 8 | `extraction_queries.sql` | SQL | — | Task author | — | Reproducible extraction |

## 5. Deterministic solution path

1. Extract page-level bytes for both months; normalise URLs.
2. Medians: full before, full after, matched before, matched after.
3. Bridge components and shares.

## 6. Wrong paths (method errors, not misreadings)

**A — published median change as real growth.** Composition ignored.

**B — mean bytes instead of median.** Different metric; outlier-driven.

**C — mixing desktop and mobile.** Device composition confounds.

**D — no URL normalisation.** Matched panel too small.

## 7. Why the stump is analytical, not semantic

The sets, metric and bridge are specified. The trap is a population change disguised as a trend.

## 8. Draft task prompt (prose)

> Was the page-weight jump real? Bridge the published median across the corpus change using a matched panel as the performance memo specifies.
> Provide `page_weight_bridge.csv` (step: value), `matched_vs_full.png`, and a one-page `page_weight_rca.pdf`.

## 9. Deliverables

* `page_weight_bridge.csv`, `matched_vs_full.png`, `page_weight_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 medians; bridge components; shares; matched URL counts; resource-type breakdown for matched pages (6 types × 2 months).

## 11. Golden-output checklist

* Month selection; normalisation; matched set; medians; bridge.

## 12. Build notes (scope tuning)

* Confirm composition explains > 70% of the published jump.
