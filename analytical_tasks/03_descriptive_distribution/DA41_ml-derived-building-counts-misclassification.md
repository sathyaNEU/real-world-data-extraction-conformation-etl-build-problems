# DA41 — Counting from a machine-learning layer: predicted positives are not the count

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Prevalence measurement from classifiers (content-moderation prevalence in transparency reports, spam rates, defect counts from vision inspection) |
| Domain | Geospatial analytics / infrastructure planning |
| Task shape | 10 · Scorecard against thresholds (8 districts × confidence thresholds → adjusted building counts; which districts exceed the electrification programme's 5,000-building floor) |
| Core method | Prevalence correction for classifier error: adjusted count = (predicted positives × precision) ÷ recall at the chosen confidence threshold, using precision and recall from the provider's regional evaluation; check stability across thresholds |
| Analytical stump | Counting footprints above a confidence threshold mixes false positives (counted) and false negatives (missed). Different thresholds give different raw counts; the corrected estimate should be roughly threshold-invariant if the evaluation applies. Districts near the floor flip depending on the method |
| Primary sources | Google Open Buildings v3 polygons (with confidence scores) and published precision/recall evaluation by region |

## 1. The real-world situation

A rural electrification programme funds districts with at least 5,000 buildings lacking grid access. The planning team counted footprints in
Google Open Buildings with confidence ≥ 0.70 and found six eligible districts. A data scientist noted that the provider publishes precision
and recall at thresholds by region and that recall at 0.70 is well below 1.

## 2. The decision (one deterministic recommendation)

**The districts eligible for the programme (adjusted building count ≥ 5,000 outside grid buffers), with adjusted counts at thresholds 0.65,
0.70 and 0.75 for all 8 districts.**

Rules (planning memo):

* Data: Open Buildings v3 polygons intersecting the 8 districts (country and districts in memo); confidence field; grid-line buffer (2 km) from
  the provided grid map.
* Buildings counted: polygon centroids inside the district and outside the buffer.
* Precision and recall at each threshold: from `open_buildings_eval_<region>.csv` (provider's regional evaluation).
* Adjusted count at threshold t = N_t × precision_t ÷ recall_t.
* Final estimate = mean of the three adjusted counts; eligible if ≥ 5,000.
* Report raw counts at 0.70 for contrast.

## 3. Why capable analysts get it wrong

* Thresholded counts look like measured counts.
* False negatives (missed small buildings, thatched roofs) are common in rural areas.
* Thresholds trade precision for recall; uncorrected counts depend on the arbitrary choice.
* The correction requires evaluation data from a comparable region.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `open_buildings_v3_polygons_<tiles>.csv.gz` | CSV (WKT) | ~5–10M | Google Open Buildings | CC BY 4.0 or ODbL (dual licence per provider) | Footprints, confidence |
| 2 | `open_buildings_eval_<region>.csv` | CSV | ~20 | Google Open Buildings documentation | CC BY 4.0 | Precision/recall by threshold |
| 3 | `districts.geojson` | GeoJSON | 8 | Task author (national admin boundaries, open licence) | Open | Districts |
| 4 | `grid_lines.geojson` | GeoJSON | ~5k | Open grid map (e.g., gridfinder; CC BY 4.0) | CC BY 4.0 | Grid access buffer |
| 5 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `team_thresholded_counts.xlsx` | XLSX | 8 | Task author | — | Raw counts |
| 7 | `open_buildings_paper_citation.pdf` | PDF | — | Sirko et al. 2021 (cite) | Cite | Model and evaluation |
| 8 | `centroids_in_scope.parquet` | Parquet | ~1M | Derived | CC BY 4.0 | Centroids with flags |

## 5. Deterministic solution path

1. Compute centroids; assign districts; apply grid buffer.
2. Raw counts at three thresholds.
3. Adjust with precision/recall; average; eligibility.
4. Contrast with the team's counts.

## 6. Wrong paths (method errors, not misreadings)

**A — raw count at 0.70.** Recall loss ignored.

**B — adjusting by precision only.** False negatives ignored.

**C — counting polygons intersecting the boundary.** Double counting across districts.

**D — evaluation from another continent.** Not the memo's region.

## 7. Why the stump is analytical, not semantic

The thresholds, metrics and formula are specified. The trap is treating classifier outputs as ground-truth counts.

## 8. Draft task prompt (prose)

> Which districts qualify for the electrification programme? Correct the Open Buildings counts for classifier error as the planning memo
> specifies. Provide `district_counts.csv` (district: raw counts at three thresholds, adjusted counts, final estimate, eligible),
> `threshold_stability.png`, and a one-page `eligibility_list.pdf`.

## 9. Deliverables

* `district_counts.csv`, `threshold_stability.png`, `eligibility_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 districts × (3 raw, 3 adjusted) = 48 values (sampled); eligibility list; contrast.

## 11. Golden-output checklist

* Centroid assignment; buffer; thresholds; correction formula; averaging; eligibility.

## 12. Build notes (scope tuning)

* Choose districts so that two near the floor flip between raw and adjusted counts.
