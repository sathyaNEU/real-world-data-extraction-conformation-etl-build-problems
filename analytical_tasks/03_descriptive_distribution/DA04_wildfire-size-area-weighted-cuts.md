# DA04 — Planning bands for wildfire response: most fires are small, most burned area is not

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Domain | Wildland fire management / emergency resource planning / catastrophe insurance |
| Task shape | 14 · Cuts of a distribution (area-weighted size thresholds at 50% / 80% / 95% coverage across four regions) |
| Core method | Weighted (area-weighted) quantiles of a heavy-tailed size distribution; cumulative coverage curves from the largest fire downward; consistent rounding |
| Analytical stump | Count-based percentiles describe the typical fire; resource planning needs the distribution of burned area, which is dominated by a tiny share of very large fires. Using count percentiles, means or size-class midpoints puts the band boundaries orders of magnitude too low |
| Primary sources | USDA Forest Service FPA-FOD national wildfire occurrence database (1992–2020) |

## 1. The real-world situation

A multi-state wildfire coordination group sets **planning bands** for aviation and extended-attack resources: the fire-size
thresholds above which fires account for 50%, 80% and 95% of all area burned in each region. The analyst used the 50th,
80th and 95th percentiles of fire size — producing thresholds of a fraction of an acre to a few hundred acres. Incident
commanders pointed out that their extended-attack fires are thousands of acres.

## 2. The decision (one deterministic recommendation)

**The three band boundaries for each of the four regions (12 thresholds), and the share of fires that lie above each.**

Rules (coordination group method):

* Fires 2001–2020 in the FPA-FOD database, assigned to regions by the geographic-area coordination center field (four regions
  in the folder); size = `FIRE_SIZE` (acres).
* For coverage c ∈ {50%, 80%, 95%}, the boundary S_c is the largest fire size S such that fires with size ≥ S together account
  for at least c of the region's total burned area (sort fires by size descending, accumulate area).
* Round each boundary down to the nearest 10 acres (nearest 1 acre if below 10 acres).
* Also report, for each boundary, the percentage of fires (by count) with size ≥ S_c.

## 3. Why capable analysts get it wrong

* "Percentile" by default means by count; the planning question is about area.
* Fire sizes span eight orders of magnitude; the mean is dominated by a handful of megafires and the median is tiny.
* Size classes A–G are coarse; using class midpoints loses the tail detail.
* The direction of accumulation (from largest down) matters for the "at least c" definition.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `FPA_FOD_20221014.sqlite` (Fires table) | SQLite | ~2.3M fires | USDA Forest Service Research Data Archive (RDS-2013-0009.6) | U.S. Gov (FS research data; free use with citation) | Fire records |
| 2 | `fpa_fod_2001_2020_regions.csv` | CSV | ~1.6M | Derived | Same | Working extract |
| 3 | `FPA_FOD_metadata.pdf` | PDF | — | USDA FS RDS | Same | Field definitions |
| 4 | `gacc_boundaries.geojson` | GeoJSON | ~10 | NIFC Open Data | Public domain | Region boundaries |
| 5 | `nifc_annual_fire_statistics.xlsx` | XLSX | ~30 | National Interagency Fire Center | Public domain | Annual totals cross-check |
| 6 | `nwcg_fire_size_classes.pdf` | PDF | — | NWCG glossary | Public domain | A–G class bounds |
| 7 | `mtbs_burned_area_boundaries_summary.csv` | CSV | ~30k | MTBS (USGS/USFS) | Public domain | Large-fire cross-check |
| 8 | `regions_in_scope.json` | JSON | 4 | Task author | — | Scope |
| 9 | `coordination_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_count_percentiles.xlsx` | XLSX | 12 | Task author | — | Count-based thresholds |

## 5. Deterministic solution path

1. Extract 2001–2020 fires with region and size; drop records with missing size.
2. For each region: sort by size descending; cumulative area share; find boundaries for 50/80/95%.
3. Round; compute count shares above each boundary.
4. Compare with count percentiles and class-midpoint estimates.

## 6. Wrong paths (method errors, not misreadings)

**A — count percentiles.** Boundaries far too low.

**B — size-class midpoints.** Coarse and biased in the tail.

**C — accumulating from the smallest fire.** Boundary off by the definition (gives the complement threshold).

**D — mean fire size as a band.** Meaningless for planning; dominated by outliers.

## 7. Why the stump is analytical, not semantic

The boundary is defined precisely in the method. The traps come from the habit of count-based percentiles and from
summarizing heavy-tailed data with location statistics — analytical, not definitional, errors.

## 8. Draft task prompt (prose)

> Set our three planning-band boundaries for each of the four regions: the fire sizes above which fires account for 50%,
> 80% and 95% of area burned from 2001 to 2020, using the FPA-FOD data and the coordination method in the folder. Provide
> `planning_bands.csv` (region × coverage: boundary in acres, fires above it, percentage of fires above it), and
> `area_coverage_curves.png` showing, for each region, the share of area burned by fires at or above each size on a log size
> axis with the three boundaries marked. Add a one-page `bands_memo.pdf` contrasting the area-based boundaries with the
> count-based percentiles.

## 9. Deliverables

* `planning_bands.csv`, `area_coverage_curves.png`, `bands_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 regions × 3 boundaries = 12; 12 count shares; count-percentile contrast; chart elements.

## 11. Golden-output checklist

* Area-weighted cumulative from largest; correct boundary definition; rounding rule; count shares.

## 12. Build notes (scope tuning)

* Verify region assignment fields in the FPA-FOD edition you ship; record the edition (6th, 2022).
* The answer is deterministic; check ties at boundaries (identical sizes) and state the tie rule in the method.
