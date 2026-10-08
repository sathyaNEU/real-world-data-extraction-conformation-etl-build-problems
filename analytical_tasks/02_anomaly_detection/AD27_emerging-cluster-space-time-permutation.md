# AD27 — Emerging hotspots: the map of high counts shows where it always happens, not what just started

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Security and trust-and-safety operations hunting emerging clusters (fraud rings by area, outage clusters for telcos and utilities, syndromic surveillance) |
| Domain | Public safety / spatial surveillance |
| Task shape | 04 · Setting one dial (the signalling threshold on the scan statistic's log-likelihood ratio, then the week's alert) |
| Core method | Prospective space–time permutation scan: expected counts from the product of spatial and temporal margins; cylinders over centroids, radii and recent windows; maximum log-likelihood ratio (LLR); threshold calibrated on historical weeks |
| Analytical stump | Hotspot maps and week-over-week counts by beat show persistent high-crime areas and city-wide surges (weather, holidays). An emerging cluster is a space–time *interaction*: an area that is high now relative to its own history *and* relative to the city's current week. Only the permutation model conditions on both margins |
| Primary sources | City of Chicago "Crimes – 2001 to Present" (Chicago Data Portal); police beat boundaries |

## 1. The real-world situation

A city's analysis unit sends one "emerging cluster" alert per week to district commanders. The current method ranks police beats by
the increase in robberies versus the prior four weeks; it alerts on the same high-volume beats after every warm weekend and missed a
cluster that spanned three small beats on a district boundary.

## 2. The decision (one deterministic recommendation)

**The LLR threshold that would have produced at most one false alert per eight weeks over the 2022 calibration period, and whether the
target week (in the memo) signals — with the cluster's centre, radius and days.**

Rules (analysis memo):

* Events: robberies (primary type ROBBERY), 2021-01-01 onward, geocoded; snap to beat centroids.
* Study window for each evaluation date: the previous 365 days; candidate clusters: circles centred on beat centroids with radius ≤ 1.5 km
  (containing ≤ 10% of events), time windows ending on the evaluation date of 3–14 days.
* Expected count in a cylinder = (events in its area over the study window) × (events in its time window over all areas) ÷ total events.
* LLR (Poisson approximation as in the memo) for cylinders with observed > expected; scan statistic = maximum LLR.
* Calibration: compute the weekly maximum LLR on 52 evaluation dates in 2022; label alerts using `known_clusters_2022.json`; choose the
  smallest threshold (grid 5.0–15.0 step 0.1) with ≤ 6 alerts on weeks with no known cluster.
* Apply to the target week; report the most likely cluster and whether it exceeds the threshold.

## 3. Why capable analysts get it wrong

* Counts per area mirror population and land use; "most robberies" is not "emerging".
* Week-over-week increases pick up city-wide swings that the temporal margin explains.
* Fixed administrative areas split clusters that cross boundaries; circles over centroids do not.
* Many cylinders are tested; the maximum statistic must be calibrated, not judged by a nominal p-value per cylinder.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Crimes_-_2001_to_Present.csv` (2021–2023 extract) | CSV | ~700k | Chicago Data Portal | City of Chicago data terms (open) | Incidents with type, date, beat, coordinates |
| 2 | `police_beats.geojson` | GeoJSON | ~275 | Chicago Data Portal | Open | Beat polygons |
| 3 | `beat_centroids.csv` | CSV | ~275 | Derived | Open | Centroids |
| 4 | `beat_distance_matrix.parquet` | Parquet | ~75k | Derived | Open | Pairwise distances |
| 5 | `known_clusters_2022.json` | JSON | ~10 | Task author (from department press releases and incident series) | — | Calibration labels |
| 6 | `analysis_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `current_beat_increase_alerts.xlsx` | XLSX | 52 | Task author | — | Current method's alerts |
| 8 | `kulldorff_2005_citation.pdf` | PDF | — | Kulldorff et al., PLoS Med 2005 (cite) | Cite | Space–time permutation scan |
| 9 | `iucr_codes.csv` | CSV | ~400 | Chicago Data Portal | Open | Offense codes |
| 10 | `target_week.json` | JSON | 1 | Task author | — | Evaluation date |

## 5. Deterministic solution path

1. Filter robberies; assign beats; daily counts by beat.
2. For each evaluation date, compute expected counts and LLR for all cylinders; record the maximum.
3. Calibrate the threshold with the false-alert constraint.
4. Apply to the target week; report the cluster.

## 6. Wrong paths (method errors, not misreadings)

**A — counts or increases by beat.** Persistent hotspots and city-wide swings.

**B — Poisson scan with population denominators.** Not the memo's model; flags dense areas.

**C — thresholding per-cylinder p-values.** Multiple testing ignored.

**D — beat boundaries only.** Cross-boundary clusters split.

## 7. Why the stump is analytical, not semantic

Events, model and calibration are specified. The trap is level-versus-interaction thinking in spatial surveillance.

## 8. Draft task prompt (prose)

> Calibrate our emerging-cluster alert using the space–time permutation scan in the analysis memo, then tell me whether this week signals and
> where. Provide `calibration_weeks.csv` (week: max LLR, cluster, known-cluster label), `cluster_map.png` (the target week's most likely
> cluster over beats), and a one-page `alert_decision.pdf` with the threshold, the alert, and how it compares with the beat-increase method.

## 9. Deliverables

* `calibration_weeks.csv`, `cluster_map.png`, `alert_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Threshold; 52 weekly maxima (sampled checks); target cluster centre, radius, days, observed, expected, LLR; alert call; contrast with
  current alerts.

## 11. Golden-output checklist

* Expected-count formula; cylinder constraints; LLR; calibration rule; target result.

## 12. Build notes (scope tuning)

* Choose a target week with a cross-boundary cluster that the beat method misses.
* Publish cylinder enumeration counts for grader verification.
