# RC16 — Eleven bad-air days after the new plant opened: the plant, or wildfire smoke?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Separating an external, region-wide shock from a local, internal cause (a sitewide latency spike from an upstream provider vs one service; a sales drop from a market-wide event vs one store) |
| Domain | Air quality regulation |
| Task shape | 18 · Hypotheses versus evidence (exceedance days × evidence lines: smoke overhead, regional uniformity, upwind–downwind gradient, co-pollutant ratios, upwind fire activity; each day classified, then the referral decision) |
| Core method | Day-by-day evidence for each exceedance day: satellite smoke polygons over the metro area; spread of PM2.5 across monitors (regional vs local); downwind-minus-other monitor difference using resultant wind relative to the facility bearing; PM2.5/NO2 ratio against each monitor's 90-day median; fire radiative power upwind in the prior 72 hours; deterministic classification rule; count local-signature days |
| Analytical stump | Comparing the season's mean PM2.5 before and after the facility opened, or correlating daily PM2.5 with the facility's operating days, confounds the comparison with an exceptional smoke season. The nearest monitor being the highest is not evidence when every monitor is high. A local source leaves a wind-dependent spatial gradient and a combustion co-pollutant signature; smoke leaves a uniform regional rise with PM enhanced relative to NO2 |
| Primary sources | U.S. EPA Air Quality System (AQS) pre-generated daily and hourly files; NOAA Hazard Mapping System (HMS) smoke polygons; NASA FIRMS VIIRS active fire detections; NOAA ISD hourly winds |

## 1. The real-world situation

A county recorded eleven days above the 24-hour PM2.5 standard in the summer after a large aggregate-processing facility opened nearby, compared
with two the summer before. Residents petitioned the air district to cite the facility. The facility pointed to wildfire smoke that summer. The
district must decide whether to refer the facility for an enforcement inspection.

## 2. The decision (one deterministic recommendation)

**Whether the facility is referred for enforcement (referral if ≥ 3 exceedance days carry a local signature), with every exceedance day classified as
smoke, local, mixed or unclassified.**

Rules (air district memo):

* Monitors: all AQS PM2.5 FRM/FEM monitors within 50 km of the facility (daily means); NO2 and CO hourly monitors in the same area.
* Exceedance day: any of those monitors with a daily mean > 35 µg/m³.
* Evidence per exceedance day:
  * E1 smoke overhead: an HMS smoke polygon of medium or heavy density covers the facility location.
  * E2 regional uniformity: (max − min) ÷ mean of daily PM2.5 across monitors < 0.35.
  * E3 local gradient: monitors whose bearing from the facility is within ±45° of the daily vector-mean wind direction (downwind) minus all other
    monitors ≥ 10 µg/m³.
  * E4 co-pollutant: daily PM2.5 ÷ NO2 (µg/m³ per ppb) at collocated sites ≥ 2 × that site's 90-day median.
  * E5 fire activity: Σ FIRMS VIIRS fire radiative power within 600 km in the upwind 90° sector over the prior 72 hours ≥ 5,000 MW.
* Classification: smoke if E1 and E2 and (E4 or E5); local if E3 and not E1; mixed if E3 and E1; otherwise unclassified.
* Referral: local days ≥ 3 (mixed days do not count).

## 3. Why capable analysts get it wrong

* Before/after averages are natural for "did the facility make it worse?".
* Smoke seasons vary hugely year to year.
* Spatial gradients need wind direction and geometry, not just the nearest monitor.
* Co-pollutant ratios separate combustion and dust sources from transported smoke but need a local baseline.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `daily_88101_<year>.csv` | CSV | ~800k (national) | EPA AQS pre-generated data files | U.S. Government work (public domain) | Daily PM2.5 |
| 2 | `hourly_42602_<year>.csv` | CSV | ~4M | EPA AQS | Public domain | Hourly NO2 |
| 3 | `hourly_42101_<year>.csv` | CSV | ~3M | EPA AQS | Public domain | Hourly CO |
| 4 | `hms_smoke_<yyyymmdd>.shp` (daily) | Shapefile | ~120 days | NOAA NESDIS Hazard Mapping System | Public domain | Smoke polygons |
| 5 | `firms_viirs_<region>_<season>.csv` | CSV | ~500k detections | NASA FIRMS | NASA open data (cite) | Fire detections and FRP |
| 6 | `isd_<station>_<year>.csv` | CSV | ~9k | NOAA ISD | NOAA open data | Hourly wind |
| 7 | `frs_facility.json` | JSON | 1 | EPA Facility Registry Service | Public domain | Facility coordinates and start-up date |
| 8 | `air_district_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `resident_petition_summary.xlsx` | XLSX | — | Task author | — | Before/after comparison in the petition |

## 5. Deterministic solution path

1. Select monitors within 50 km; flag exceedance days.
2. Compute vector-mean daily wind; facility-to-monitor bearings; downwind sets.
3. Evaluate E1–E5 per day (spatial joins for HMS and FIRMS; rolling medians for ratios).
4. Classify days; count; decide referral.
5. Contrast with the petition's before/after averages.

## 6. Wrong paths (method errors, not misreadings)

**A — before/after seasonal means.** Attributes a smoke season to the facility.

**B — correlation with operating days.** The facility runs on most days, including smoke days; correlation reflects season.

**C — nearest-monitor reasoning.** Ignores wind and the regional rise.

**D — PM2.5 alone.** Without co-pollutants and fire data, smoke and local days cannot be separated.

## 7. Why the stump is analytical, not semantic

All thresholds and evidence lines are numeric and specified. The trap is aggregating away the day-level spatial and chemical signatures that
distinguish a regional shock from a local source.

## 8. Draft task prompt (prose)

> Residents want the new facility cited for this summer's bad-air days. Classify each exceedance day using the air district memo's evidence rules and
> tell me whether the facility should be referred. Provide `exceedance_day_evidence.csv` (day: E1–E5, class), `exceedance_map_timeline.png`, and a
> one-page `referral_decision.pdf`.

## 9. Deliverables

* `exceedance_day_evidence.csv` — one row per exceedance day with evidence values and class.
* `exceedance_map_timeline.png` — timeline of PM2.5 with day classes, plus a map panel of the gradient on local days.
* `referral_decision.pdf` — decision, day counts by class, and why the petition's comparison is misleading.

## 10. Where 25+ rubric criteria come from

* Monitor selection and exceedance-day count: 3.
* Per-day evidence values for the 11 days (sampled 5 days × 5 lines): 25 cells, scored in groups.
* Class counts: 4.
* Referral decision: 1.
* Petition contrast: 2+.

## 11. Golden-output checklist

* 50 km monitor set; daily means; > 35 µg/m³.
* Vector-mean wind (not scalar mean direction); ±45° downwind sector.
* HMS density filter; FRP sector and window; 90-day median ratios.
* Classification precedence; mixed days excluded from the referral count.

## 12. Build notes (scope tuning)

* Choose a county and season with a known smoke episode and a new facility; confirm that the before/after comparison suggests the facility while the
  day-level rules classify no more than 2 days as local.
