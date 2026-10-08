# DA08 — Portfolio web performance: you cannot average 75th percentiles

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Web-performance teams reporting Core Web Vitals across many sites or apps (publishers, retailers, platform companies) and any SLO reported over a portfolio of services |
| Domain | Web performance / product analytics |
| Task shape | 14 · Cuts of a distribution (portfolio p75 of LCP, INP and CLS by device; pass/fail against "good" thresholds; the device × metric cell that gets the engineering quarter) |
| Core method | Merge per-origin histograms weighted by each origin's traffic share (the memo's popularity proxy), then read the 75th percentile from the merged distribution with within-bin interpolation; compare with the mean (or traffic-weighted mean) of per-origin p75s |
| Analytical stump | Percentiles are not additive: the mean of origin p75s is not the portfolio p75, and the unweighted mean treats a tiny origin like the flagship. The portfolio's user experience is the traffic-weighted mixture of histograms; reading p75 from it can flip pass/fail against the threshold |
| Primary sources | Chrome UX Report (CrUX) BigQuery dataset — monthly origin-level histograms by device |

## 1. The real-world situation

A media group with 40 web properties reports Core Web Vitals to its board. The analyst averaged each property's published p75 Largest
Contentful Paint (LCP) and declared the portfolio "good" on mobile. The engineering lead asked which device–metric combination actually
fails for the group's users and deserves the next quarter of performance work.

## 2. The decision (one deterministic recommendation)

**The device × metric cell (mobile/desktop × LCP/INP/CLS) that receives the engineering quarter: the cell whose portfolio p75 exceeds its
"good" threshold by the largest relative margin.**

Rules (performance memo):

* Data: CrUX monthly table for the month in the memo; origins in `portfolio_origins.csv`; device form factors phone and desktop.
* Histograms: CrUX bin densities per origin, device and metric.
* Weights: each origin's share of portfolio page loads from `origin_traffic_shares.csv` (internal analytics, provided), split by device per
  the CrUX form-factor density.
* Portfolio distribution = Σ weight × origin density per bin; p75 read with linear interpolation within the bin.
* "Good" thresholds: LCP 2.5 s, INP 200 ms, CLS 0.1.
* Relative margin = (p75 − threshold) ÷ threshold; the cell with the largest positive margin wins; if none positive, report "all good".

## 3. Why capable analysts get it wrong

* Published per-origin p75s are convenient; averaging them is a reflex.
* Percentiles of a mixture depend on the full shape of each component.
* Equal weighting ignores where users actually are.
* Within-bin interpolation matters when p75 falls in a wide bin.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `crux_<yyyymm>_portfolio_histograms.parquet` | Parquet | ~200k bins | CrUX BigQuery (chrome-ux-report.all.<yyyymm>) | CC BY 4.0 | Origin × device × metric histograms |
| 2 | `crux_<yyyymm>_p75_summary.csv` | CSV | ~240 | CrUX materialized summary tables | CC BY 4.0 | Published p75s |
| 3 | `crux_methodology.html` | HTML | — | Chrome developers documentation | CC BY 4.0 | Bin definitions |
| 4 | `portfolio_origins.csv` | CSV | 40 | Task author | — | Origins |
| 5 | `origin_traffic_shares.csv` | CSV | 40 | Task author (fixed shares) | — | Weights |
| 6 | `web_vitals_thresholds.json` | JSON | 3 | web.dev (cite) | CC BY 4.0 | Thresholds |
| 7 | `performance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `analyst_average_p75.xlsx` | XLSX | 6 | Task author | — | Averaged p75s |
| 9 | `merge_check_values.json` | JSON | ~6 | Task author | — | Two-origin test merges |
| 10 | `form_factor_densities.csv` | CSV | ~120 | CrUX | CC BY 4.0 | Device splits |

## 5. Deterministic solution path

1. Load histograms; normalize densities; apply device splits to weights.
2. Merge histograms per device × metric; interpolate p75.
3. Margins against thresholds; choose the cell.
4. Contrast with averaged p75s.

## 6. Wrong paths (method errors, not misreadings)

**A — mean of origin p75s.** Not a percentile of anything.

**B — unweighted histogram merge.** Small origins overweighted.

**C — weights ignoring device split.** Phone/desktop mixtures wrong.

**D — bin upper bound as p75.** Overstated values.

## 7. Why the stump is analytical, not semantic

Data, weights and thresholds are specified. The trap is aggregating quantiles instead of distributions.

## 8. Draft task prompt (prose)

> Which device and metric should get our next performance quarter? Merge the CrUX histograms across our 40 origins by traffic share as the
> performance memo describes, read the portfolio p75s, and compare with the "good" thresholds. Provide `portfolio_vitals.csv` (cell: merged
> p75, averaged p75, threshold, margin), `merged_distributions.png` (cumulative curves with thresholds), and a one-page `performance_priority.pdf`.

## 9. Deliverables

* `portfolio_vitals.csv`, `merged_distributions.png`, `performance_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 cells × (merged p75, averaged p75, margin, pass) = 24; chosen cell; check merges; weights.

## 11. Golden-output checklist

* Density normalization; device split; merge; interpolation; thresholds; choice.

## 12. Build notes (scope tuning)

* Choose origins so that the averaged-p75 view passes mobile LCP while the merged view fails.
