# AD23 — Earthquake-rate alarms: the network got better at hearing, and one sequence shouts for months

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Regulators and insurers monitoring induced seismicity near wastewater injection; any metric whose detection coverage expanded over time (more sensors or logging → more recorded events) |
| Domain | Geophysics / energy regulation / catastrophe risk |
| Task shape | 07 · Grid of cells (6 regulatory areas × 3 periods → declustered rate above completeness; areas that meet the "significant increase" rule receive injection-volume directives) |
| Core method | Magnitude of completeness (Mc) by period via maximum curvature + 0.2; a common Mc across periods; Gardner–Knopoff declustering; Poisson rate-ratio test on mainshocks above the common Mc |
| Analytical stump | Network densification lowers Mc, so counts of all recorded events jump even where nothing changed underground; one large sequence's aftershocks dominate an area's count. Raw counts flag the wrong areas and overstate increases |
| Primary sources | USGS ANSS Comprehensive Catalog (ComCat); Oklahoma Geological Survey earthquake catalog; Oklahoma Corporation Commission UIC injection volume reports |

## 1. The real-world situation

A state regulator divided north-central Oklahoma into six areas of interest. Areas with a statistically significant increase in seismicity
receive a directive to reduce disposal volumes in the deepest formation. A staff analyst compared counts of all catalogued events per year
and flagged five of six areas. Operators objected that the state's seismic network had added dozens of stations over the period and that
one area's count was dominated by the aftershocks of a single M5 event.

## 2. The decision (one deterministic recommendation)

**The set of areas that receive volume-reduction directives under the regulator's rate rule.**

Rules (seismicity memo):

* Catalog: ComCat events inside the six polygons, 2009-01-01 to 2016-12-31, depth ≤ 15 km; magnitude preference per the memo (ML
  where available).
* Periods: P0 = 2009–2011, P1 = 2012–2013, P2 = 2014–2016.
* Mc per period: maximum curvature of the non-cumulative magnitude histogram (0.1 bins) + 0.2, computed over all six areas pooled.
  Common Mc = the largest of the three period Mc values.
* Declustering: Gardner–Knopoff space–time windows (table in the memo); keep mainshocks only.
* Rate test per area: declustered mainshocks with M ≥ common Mc per year, P2 versus P0; one-sided conditional binomial test of the
  P2 share given the total and the period lengths; significant if p < 0.01 and the rate ratio ≥ 2.
* Directive: areas meeting the test.

## 3. Why capable analysts get it wrong

* "More earthquakes in the catalog" is read as "more earthquakes"; detection capability is invisible in a count.
* Aftershocks are not independent events; a Poisson test on clustered events is wildly anti-conservative.
* Area-specific Mc estimates on small samples are unstable; the memo pools them by period.
* Using the cumulative instead of the non-cumulative histogram for maximum curvature mislocates Mc.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `comcat_oklahoma_2009_2016.csv` | CSV | ~25k events | USGS ComCat (FDSN event service) | U.S. Gov public domain | Events |
| 2 | `comcat_oklahoma_2009_2016.geojson` | GeoJSON | ~25k | USGS | Public domain | Same with magnitude types |
| 3 | `ogs_catalog_2009_2016.csv` | CSV | ~30k | Oklahoma Geological Survey | Public (state data; cite) | Cross-check, station counts |
| 4 | `ogs_station_history.csv` | CSV | ~150 | OGS / IRIS station metadata | Public | Network densification evidence |
| 5 | `areas_of_interest.geojson` | GeoJSON | 6 | Task author (from published regulatory maps) | — | Polygons |
| 6 | `occ_uic_injection_volumes.xlsx` | XLSX | ~40k well-months | Oklahoma Corporation Commission | Public | Context: disposal volumes |
| 7 | `gardner_knopoff_windows.json` | JSON | ~10 | From Gardner & Knopoff (1974) table | Cite | Declustering windows |
| 8 | `seismicity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `staff_count_comparison.xlsx` | XLSX | 6 | Task author | — | Raw-count flags |
| 10 | `wiemer_wyss_mc_citation.pdf` | PDF | — | Cite | Cite | Completeness methods |

## 5. Deterministic solution path

1. Clip events to polygons and depth; build per-period magnitude histograms; compute Mc and the common Mc.
2. Decluster with the Gardner–Knopoff windows (largest-first order).
3. Count mainshocks ≥ common Mc per area and period; rates per year.
4. Binomial test and rate ratio per area; directive set.
5. Contrast with the staff raw-count flags.

## 6. Wrong paths (method errors, not misreadings)

**A — raw counts.** Detection improvements look like rate increases.

**B — per-period Mc without a common threshold.** Periods are not comparable.

**C — no declustering.** Aftershock-heavy area flagged on one sequence.

**D — Poisson test on clustered events.** Every area "significant".

## 7. Why the stump is analytical, not semantic

The catalog, polygons, windows and test are specified. The traps are detection-capability change and dependence between events —
measurement and statistical-model errors.

## 8. Draft task prompt (prose)

> Under our seismicity rule, which of the six areas get a disposal-volume directive? Use the 2009–2016 catalog, put all periods on a
> common completeness magnitude, decluster, and run the rate test in the memo. Provide `area_period_grid.csv` (area × period: events, Mc,
> mainshocks ≥ Mc, rate), `magnitude_frequency.png` (histograms by period with Mc marked) and a one-page `directive_memo.pdf` listing the
> areas, their rate ratios and p-values, and how the result differs from the staff's raw-count comparison.

## 9. Deliverables

* `area_period_grid.csv`, `magnitude_frequency.png`, `directive_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 period Mc values and the common Mc; 6 areas × 3 periods mainshock counts = 18; 6 rate ratios and test results; directive set; staff
  contrast.

## 11. Golden-output checklist

* Correct polygon clipping; Mc by maximum curvature + 0.2; common Mc; declustering order; binomial test with period lengths; directive.

## 12. Build notes (scope tuning)

* Draw polygons so one area contains a large aftershock sequence and one area's raw-count increase is mostly sub-Mc events.
* Confirm the directive set differs from the raw-count flags by at least two areas.
