# P13 — Regional surge trigger from weekly hospital capacity: averages of ratios, suppressed sentinels, and the wrong ICU

| Field | Value |
|---|---|
| Domain | Hospital operations / regional emergency preparedness |
| Objective family | Descriptive & Distribution Analysis (scorecard) with feed conformance |
| Task shape | 10 · Scorecard against thresholds |
| Core technique | Ratio-of-sums aggregation over facility rows with partial reporting coverage; sentinel-value handling per documentation; field selection by written definition (staffed adult ICU vs all ICU) |
| Trap family (honest data) | Mean of hospital percentages; -999999 treated as a number or as a dropped row; total ICU beds (incl. NICU/PICU) used for an adult metric |
| Primary sources | HHS "COVID-19 Reported Patient Impact and Hospital Capacity by Facility" (weekly), CDC/NCHS Health Service Area crosswalk |

## 1. The real-world project

A state hospital association runs a **regional surge compact**: when a Health Service Area (HSA) is under sustained
strain, member hospitals activate transfer agreements and travel-staff contracts. The trigger is computed from the
public HHS facility-level weekly capacity file. The association's first automated run activated the compact in a rural
HSA whose largest hospital had a quiet week — and missed an urban HSA whose ICUs were full.

## 2. The business decision (one deterministic recommendation)

**Go / no-go: does the compact activate for the target HSA for the two collection weeks in scope?**

Rules (compact trigger protocol):

* Hospitals: `hospital_subtype` in {Short Term, Critical Access Hospitals}; assigned to HSAs through county FIPS.
* Metrics per HSA-week, each a **ratio of sums of 7-day averages** across hospitals:
  M1 adult inpatient occupancy = Σ `all_adult_hospital_inpatient_bed_occupied_7_day_avg` ÷ Σ
  `all_adult_hospital_inpatient_beds_7_day_avg`;
  M2 staffed adult ICU occupancy = Σ `staffed_adult_icu_bed_occupancy_7_day_avg` ÷ Σ
  `total_staffed_adult_icu_beds_7_day_avg`;
  M3 COVID share of staffed adult ICU = Σ `staffed_icu_adult_patients_confirmed_covid_7_day_avg` ÷ Σ
  `total_staffed_adult_icu_beds_7_day_avg`.
* A hospital enters a metric only if both its numerator and denominator have `_7_day_coverage` ≥ 4.
* Suppressed values (`-999999`, documented as a 7-day sum of 1–3) are replaced by a sum of 2, i.e. average =
  2 ÷ coverage.
* Thresholds: M1 ≥ 85%, M2 ≥ 90%, M3 ≥ 20%. An HSA-week is "strained" if at least two metrics meet threshold.
* Go if the target HSA is strained in **both** weeks.

## 3. Why this gets overlooked in real projects

* Facility files invite `groupby(hsa).mean()` on a pre-computed percentage column — the mean of ratios lets a 25-bed
  hospital outvote a 600-bed hospital.
* `-999999` is a number; arithmetic proceeds silently and produces negative or absurd sums. Dropping the whole row
  instead removes that hospital's beds from the denominator.
* There are several ICU fields; `total_icu_beds_7_day_avg` includes pediatric and neonatal beds, so it dilutes adult
  occupancy.
* Coverage fields are easy to ignore because most rows have 7.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `covid_hospital_capacity_by_facility.csv` (state, full history) | CSV | 50k–300k | HealthData.gov (HHS) | U.S. Gov public domain | Facility-week metrics |
| 2 | `covid_hospital_capacity_by_facility_week.parquet` (target weeks, all states) | Parquet | ~5k per week | HealthData.gov | Public domain | Same, columnar |
| 3 | `facility_dataset_dictionary.pdf` | PDF | — | HHS Protect / HealthData.gov FAQ | Public domain | Field definitions, -999999 rule, Friday week start |
| 4 | `hsa_county_crosswalk.xlsx` | XLSX | ~3.1k | CDC/NCHS Health Service Areas | Public domain | County → HSA |
| 5 | `county_fips_reference.csv` | CSV | ~3.2k | Census | Public domain | FIPS validation |
| 6 | `hospital_general_information.json` | JSON | ~5k | CMS Provider Data Catalog | Public domain | Subtype cross-check |
| 7 | `compact_trigger_protocol.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `member_hospitals.csv` | CSV | ~100 | Task author (from public CCNs) | — | Target HSA, member list |
| 9 | `state_daily_hospital_capacity.json` | JSON | ~1k | HealthData.gov (state timeseries) | Public domain | Reconciliation check |
| 10 | `collection_weeks.csv` | CSV | 2 | Task author | — | Weeks in scope |

## 5. Deterministic solution path

1. Filter subtypes and weeks; map hospitals to HSA.
2. Replace `-999999` per protocol; compute averages; apply coverage gating per metric.
3. Aggregate ratio-of-sums per HSA-week for M1–M3; compare to thresholds; mark strained.
4. Decide for the target HSA; report all HSAs in the state as context.
5. Show the mean-of-ratios and total-ICU variants.

## 6. The traps

**Trap A — mean of ratios.** Small hospitals with high occupancy push a rural HSA over the line.

**Trap B — sentinel as number.** Negative sums depress M3; the target HSA misses "strained".

**Trap C — dropping suppressed rows.** Removes beds from denominators; occupancy rises artificially.

**Trap D — total ICU beds.** Pediatric/neonatal capacity dilutes M2 below 90% for the target HSA.

**Trap E — ISO weeks.** Re-bucketing Friday-start collection weeks merges partial weeks.

## 7. Why the data is honest

The HHS file reports exactly what hospitals submitted, with documented suppression and coverage semantics. Nothing is
planted; the protocol defines how to aggregate.

## 8. Draft task prompt (prose)

> The compact activates for an HSA only if it is strained in both collection weeks in scope, under the trigger protocol in
> the folder. Using the HHS facility file and the HSA crosswalk, compute the three trigger metrics for every HSA in the
> state for both weeks and tell me whether the compact activates for our target HSA. Produce `trigger_scorecard.xlsx`
> with HSA × week rows showing each metric, its threshold result, hospitals included and excluded by coverage, and the
> strained flag; and `trigger_grid.png`, a grid of HSAs against metric-week cells coloured by pass/fail with values
> printed. In a short note on the first sheet, give the decision, the binding metric for the target HSA, and how far it
> sits from its threshold.

## 9. Deliverables

* `trigger_scorecard.xlsx`, `trigger_grid.png`.

## 10. Where 25+ rubric criteria come from

* HSAs × 3 metrics × 2 weeks threshold checks (≥ 24 for 4+ HSAs); strained flags; decision; binding metric and distance.

## 11. Golden-output checklist

* Ratio of sums of averages; sentinel replacement; coverage gating; adult staffed ICU fields; decision stated.

## 12. Build notes (scope tuning)

* Choose two consecutive weeks (e.g. winter 2021–22 or 2022–23) and a target HSA where the correct method gives the
  opposite decision from Trap A or Trap D.
* The dataset's field names changed over time; freeze the downloaded schema and quote exact names in the protocol.
