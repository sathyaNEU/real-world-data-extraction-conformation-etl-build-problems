# DS38 — Shutting down coastal facilities before a hurricane: "inside the cone" is not a decision rule

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Spatial risk decisions from forecast uncertainty (pre-positioning crews, shutting data centres or plants, rerouting shipments) where a graphic's boundary is mistaken for a probability threshold |
| Domain | Energy operations / emergency management |
| Task shape | 10 · Scorecard against thresholds (facilities × forecast lead times → probability of tropical-storm-force winds; shutdown decisions under the memo's cost–loss threshold) |
| Core method | Empirical track-error distributions by lead time (along- and cross-track) from historical official forecast errors; simulate track realisations around the forecast; wind-radius model for tropical-storm-force winds (34 kt) from forecast radii; probability that each facility experiences 34-kt winds; shut down if probability ≥ C/L |
| Analytical stump | The forecast cone contains the storm centre about two-thirds of the time and says nothing about wind extent; facilities outside the cone can face damaging winds, and those inside may have low probability at long lead times. Treating cone membership as the decision rule produces both unnecessary and missed shutdowns |
| Primary sources | NOAA NHC HURDAT2 best tracks; NHC official forecast archives (track and wind radii) and verification error statistics |

## 1. The real-world situation

An energy company with 12 coastal facilities shuts down a facility when it falls inside the NHC forecast cone 72 hours before landfall. After a
season with several unnecessary shutdowns and one facility outside the cone hit by tropical-storm winds, the risk team proposed a probabilistic
rule with cost–loss threshold C/L = 0.15.

## 2. The decision (one deterministic recommendation)

**For a historical storm advisory in the memo, which facilities to shut down at the 72-hour and 48-hour advisories under the probabilistic rule, and
how the decisions differ from the cone rule.**

Rules (risk memo):

* Track errors: along- and cross-track error distributions by lead time (24, 48, 72 h) from NHC official forecasts for Atlantic storms 2014–2023
  (computed from forecast archives versus HURDAT2 positions).
* Simulation: 10,000 tracks per advisory: forecast positions + bivariate errors (independent along/cross, empirical sampling with seed 99);
  intensity and 34-kt radii from the forecast advisory (quadrant radii; memo uses the maximum radius for simplicity).
* Facility hit: any simulated position within the 34-kt radius of the facility during the forecast period.
* Probability = share of simulated tracks hitting; shut down if ≥ 0.15.
* Cone rule: facility inside the official cone polygon at that advisory.

## 3. Why capable analysts get it wrong

* The cone is the most recognised hurricane graphic.
* It represents centre-track uncertainty, not wind extent.
* Cost–loss decisions need probabilities, not boundaries.
* Uncertainty grows with lead time; decisions should differ by lead time.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `hurdat2-1851-2023.txt` | Text | ~55k track points | NOAA NHC HURDAT2 | U.S. Gov public domain | Best tracks |
| 2 | `nhc_forecast_advisories_2014_2023.csv` | CSV | ~40k forecast points | NHC forecast/advisory archive (parsed) | Public domain | Forecast positions, radii |
| 3 | `nhc_cone_polygons_<storm>.zip` | Shapefile | ~20 advisories | NHC GIS archive | Public domain | Cones for the case storm |
| 4 | `facilities.csv` | CSV | 12 | Task author | — | Facility coordinates |
| 5 | `risk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `cone_rule_decisions.xlsx` | XLSX | 24 | Task author | — | Cone-rule decisions |
| 7 | `nhc_verification_report_citation.pdf` | PDF | — | NHC forecast verification reports (cite) | Public domain | Error context |

## 5. Deterministic solution path

1. Match forecasts to best tracks; compute along/cross errors by lead time.
2. For the case advisories, simulate tracks; compute hit probabilities.
3. Apply thresholds; compare with cone membership.

## 6. Wrong paths (method errors, not misreadings)

**A — cone membership.** Wrong concept.

**B — centre-track probability only (no wind radius).** Underestimates exposure.

**C — same error distribution for all lead times.** Miscalibrated.

**D — Gaussian errors fitted by mean/SD with outliers.** Memo specifies empirical sampling.

## 7. Why the stump is analytical, not semantic

The error model, simulation and rule are specified. The trap is misreading an uncertainty graphic as a decision rule.

## 8. Draft task prompt (prose)

> Which facilities should shut down at the 72- and 48-hour advisories for the case storm? Compute wind-exposure probabilities from track-error
> simulations as the risk memo specifies and compare with the cone rule. Provide `facility_scorecard.csv` (facility × advisory: probability, shut down,
> cone rule), `exposure_map.png`, and a one-page `shutdown_decisions.pdf`.

## 9. Deliverables

* `facility_scorecard.csv`, `exposure_map.png`, `shutdown_decisions.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 facilities × 2 advisories probabilities and decisions = 24+; error statistics by lead time; differences from cone rule.

## 11. Golden-output checklist

* Error computation; simulation; radius; threshold; cone comparison.

## 12. Build notes (scope tuning)

* Choose a storm where at least one facility outside the cone exceeds 15% and one inside is below.
