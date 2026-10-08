# DA29 — When did the corrosion start? Failures seen only at annual tests are interval-censored

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Reliability analysis where failures are detected only at check-ins (IoT heartbeats, periodic inspections, annual device health checks) |
| Domain | Automotive reliability |
| Task shape | 14 · Cuts of a distribution (age at which 10%, 25% and 50% of vehicles have developed a structural-corrosion failure, for 4 model families; the family enrolled in an extended corrosion warranty review) |
| Core method | Turnbull non-parametric maximum likelihood estimator for interval-censored data: each vehicle's first corrosion failure lies between its last passing test and its first failing test; right-censored if never failed; quantiles read from the NPMLE |
| Analytical stump | Treating the test date of the first failure as the failure age biases ages upward (by up to a year); treating the midpoint as exact understates uncertainty and is biased when intervals are long. Vehicles with gaps in testing have wide intervals. The interval-censored estimator uses exactly what is known |
| Primary sources | UK DVSA anonymised MOT test results and failure items |

## 1. The real-world situation

A manufacturer's reliability team reviews corrosion durability by model family using public MOT (annual roadworthiness) data. The first
analysis used the age at the failing test as the failure age and concluded that corrosion failures start late enough to fall outside the
warranty for all families. A reliability engineer noted that the true onset lies somewhere in the year before the failing test.

## 2. The decision (one deterministic recommendation)

**The model family enrolled in the extended corrosion warranty review: the family whose estimated age at 10% cumulative corrosion failure is
below 8.0 years, choosing the lowest if several qualify; with the 10%, 25% and 50% ages for all four families.**

Rules (reliability memo):

* Data: MOT test results and failure-item files for test years 2010–2023; vehicles first registered 2005–2009 in the four model families
  (make/model strings mapped by the memo).
* Corrosion failure: a failure item in the memo's list of structural corrosion reasons (RfR IDs).
* Age: years from first-use date to test date.
* Interval for each vehicle: (age at last test without corrosion failure, age at first test with corrosion failure]; right-censored at the
  last test if never failed; vehicles whose first test is a corrosion failure: (0, age].
* Estimator: Turnbull NPMLE (self-consistency algorithm to convergence 1e-8); quantiles: smallest age at which F ≥ p (using the memo's
  convention for flat regions).
* Report also the "age at failing test" empirical quantiles for contrast.

## 3. Why capable analysts get it wrong

* The failing test date is the only recorded date; using it as the event time is natural.
* Failures happen between inspections; ignoring this shifts the distribution.
* Missed tests (vehicles off-road) create long intervals.
* Right-censoring for vehicles never failing must be retained.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–14 | `test_result_<yyyy>.csv` (2010–2023) | CSV | ~35–40M each | DVSA anonymised MOT data | Open Government Licence v3 | Tests: vehicle ID, date, result, make, model, first-use date |
| 15–28 | `test_item_<yyyy>.csv` | CSV | ~40–60M each | DVSA | OGL v3 | Failure items (RfR) |
| 29 | `item_detail.csv`, `item_group.csv` | CSV | ~3k | DVSA | OGL v3 | RfR descriptions |
| 30 | `mot_data_user_guide.pdf` | PDF | — | DVSA | OGL v3 | Field definitions |
| 31 | `model_family_map.json` | JSON | ~60 | Task author | — | Make/model → family |
| 32 | `corrosion_rfr_list.json` | JSON | ~40 | Task author | — | Corrosion reasons |
| 33 | `reliability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 34 | `first_analysis_failing_test_ages.xlsx` | XLSX | 4 | Task author | — | Naive quantiles |
| 35 | `vehicle_intervals.parquet` | Parquet | ~1.2M | Derived | OGL v3 | Interval per vehicle |
| 36 | `turnbull_check.json` | JSON | — | Task author | — | Small worked example |

## 5. Deterministic solution path

1. Select vehicles by family and registration years; order tests per vehicle.
2. Identify first corrosion failure; construct intervals and censoring.
3. Turnbull NPMLE per family; quantiles.
4. Choose the family; contrast with naive quantiles.

## 6. Wrong paths (method errors, not misreadings)

**A — failing-test age as exact.** Ages overstated.

**B — midpoint imputation then KM.** Biased and overconfident.

**C — dropping never-failed vehicles.** Distribution conditioned on failure.

**D — ignoring retests within the same month.** Duplicate failures; the memo uses the first test of each annual cycle.

## 7. Why the stump is analytical, not semantic

Intervals and the estimator are specified. The trap is the censoring structure of inspection data.

## 8. Draft task prompt (prose)

> Which model family needs a corrosion warranty review? Estimate the age distribution of first structural-corrosion failures from MOT data
> treating them as interval-censored, as the reliability memo specifies. Provide `corrosion_quantiles.csv` (family: vehicles, failures, ages at
> 10/25/50% — Turnbull and naive), `cumulative_failure.png`, and a one-page `warranty_review.pdf`.

## 9. Deliverables

* `corrosion_quantiles.csv`, `cumulative_failure.png`, `warranty_review.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 families × 3 quantiles × 2 methods = 24; counts; choice; toy check.

## 11. Golden-output checklist

* Cohort selection; corrosion RfRs; interval construction; NPMLE convergence; quantile convention; choice.

## 12. Build notes (scope tuning)

* Confirm the naive method places all families above 8 years while the Turnbull estimate puts one below.
