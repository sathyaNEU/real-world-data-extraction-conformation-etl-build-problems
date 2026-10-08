# AD46 — Restaurant hygiene outliers: re-inspections and complaint visits find what they were sent to find

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Food-delivery and marketplace quality teams auditing merchants; any audit programme where follow-up audits target known problems and inflate observed failure rates |
| Domain | Food safety / marketplace quality |
| Task shape | 10 · Scorecard against thresholds (cuisine × neighbourhood segments × metrics → which segments enter a targeted education campaign) |
| Core method | Restrict to initial cycle inspections (routine, unannounced) to estimate segment violation rates; one inspection per restaurant per cycle; critical-violation rate with Wilson intervals; segment flagged when the lower bound exceeds the citywide rate by the memo's margin |
| Analytical stump | Re-inspections occur only after a failing initial inspection, and complaint-driven visits target suspected problems; both have higher violation rates. Segments with many re-inspections (because they failed before) look systematically worse on all-inspection rates. Selection into inspection type must be removed before comparing segments |
| Primary sources | NYC Department of Health and Mental Hygiene (DOHMH) restaurant inspection results (NYC Open Data) |

## 1. The real-world situation

A city health department funds a hygiene-education campaign for restaurant segments (cuisine × neighbourhood tabulation area) with
unusually high critical-violation rates. The pilot analysis used every inspection row and flagged 40 segments; owners in those segments
pointed out that their numbers were swollen by follow-up visits after an initial failure and by complaint-driven inspections.

## 2. The decision (one deterministic recommendation)

**The list of segments entering the campaign under the memo's scorecard, and the number of restaurants it reaches.**

Rules (campaign memo):

* Data: DOHMH inspection results, inspection dates 2022-01-01 to 2023-12-31.
* Inspection unit: CAMIS × inspection date × inspection type (rows are violations; collapse).
* Initial cycle inspections only: inspection type "Cycle Inspection / Initial Inspection".
* One per restaurant: the earliest initial cycle inspection in the window.
* Critical violation: at least one violation with `CRITICAL FLAG` = "Critical".
* Segment: cuisine description × NTA (from coordinates); eligible segments with ≥ 40 restaurants.
* Metrics per segment: critical rate with Wilson 95% interval; citywide rate on the same basis.
* Flag: Wilson lower bound > citywide rate + 5 percentage points.
* Campaign: flagged segments; reach = restaurants in them.

## 3. Why capable analysts get it wrong

* All rows feel like the full picture; the file mixes inspection purposes.
* Violation rows must be collapsed to inspections; counting rows inflates rates for messy inspections.
* Repeated inspections of the same restaurant are not independent observations.
* Small segments need interval-based rules.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `DOHMH_New_York_City_Restaurant_Inspection_Results.csv` | CSV | ~250k violation rows | NYC Open Data | NYC Open Data terms (open) | Inspections and violations |
| 2 | `restaurant_inspection_data_dictionary.xlsx` | XLSX | — | NYC Open Data | Open | Field definitions, inspection types |
| 3 | `nta_2020.geojson` | GeoJSON | ~260 | NYC Department of City Planning | Open | Neighbourhood tabulation areas |
| 4 | `cuisine_groups.json` | JSON | ~85 | Task author | — | Cuisine harmonisation |
| 5 | `campaign_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `pilot_all_rows_flags.xlsx` | XLSX | 40 | Task author | — | Pilot flags |
| 7 | `inspection_type_counts.csv` | CSV | ~40 | Derived | Open | Context |
| 8 | `wilson_interval_reference.pdf` | PDF | — | Cite | Cite | Interval |
| 9 | `restaurants_geocoded.parquet` | Parquet | ~30k | Derived | Open | CAMIS → coordinates, NTA |
| 10 | `dohmh_grading_rules_citation.pdf` | PDF | — | NYC DOHMH (cite) | Public | Inspection process |

## 5. Deterministic solution path

1. Collapse to inspections; filter dates and initial cycle type; first per restaurant.
2. Critical indicator; segments; eligibility.
3. Rates, Wilson bounds, citywide rate; flags; reach.
4. Contrast with the pilot flags.

## 6. Wrong paths (method errors, not misreadings)

**A — all inspection types.** Re-inspection selection inflates rates.

**B — counting violation rows.** Rates exceed 100% in effect.

**C — multiple inspections per restaurant.** Non-independence and weighting by failures.

**D — point-estimate flags.** Small segments flagged by chance.

## 7. Why the stump is analytical, not semantic

The inspection types and rules are specified. The trap is selection bias from follow-up targeting and the unit of analysis.

## 8. Draft task prompt (prose)

> Which restaurant segments go into the hygiene campaign? Follow the campaign memo using initial cycle inspections only, one per restaurant, and
> the interval-based flag. Provide `segment_scorecard.csv` (segment: restaurants, critical rate, interval, flag), `segment_rates.png` (rates with
> intervals for flagged and pilot segments against the citywide line), and a one-page `campaign_segments.pdf` with reach.

## 9. Deliverables

* `segment_scorecard.csv`, `segment_rates.png`, `campaign_segments.pdf`.

## 10. Where 25+ rubric criteria come from

* Citywide rate; each flagged segment's rate and bound; reach; pilot segments that drop out; collapse counts.

## 11. Golden-output checklist

* Collapse; inspection-type filter; first per restaurant; Wilson; threshold; reach.

## 12. Build notes (scope tuning)

* Freeze the download date (the dataset is a rolling window of active restaurants).
* Confirm fewer than half of the pilot segments are flagged.
