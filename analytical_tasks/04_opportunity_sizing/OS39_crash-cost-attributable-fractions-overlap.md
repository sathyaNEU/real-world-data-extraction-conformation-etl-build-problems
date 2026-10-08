# OS39 — Crash costs attributable to speeding, alcohol and distraction: the shares add to more than 100%

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Attributing a problem to overlapping causes (churn due to price, bugs and support; defects due to several process faults) when sizing the value of fixing each one |
| Domain | Road safety / insurance telematics |
| Task shape | 03 · Bridge between two totals (sum of single-factor attributable costs → joint attributable cost for the three factors; the telematics feature prioritised) |
| Core method | Weighted crash-level data with factor flags; single-factor "involved" costs; joint attribution via the set of crashes with any factor and Shapley allocation of each crash's cost among the factors present (equal split among present factors per memo); bridge from naive sum to joint total |
| Analytical stump | Counting each crash fully under every factor present (speeding and alcohol and distraction) double or triple counts costs; summing factor totals exceeds the cost of all factor-involved crashes. Prioritising a feature by its "involved" total overweights factors that co-occur with others |
| Primary sources | NHTSA Crash Report Sampling System (CRSS) — accident, vehicle, person files with sampling weights |

## 1. The real-world situation

An insurer's telematics team must pick one feature to build next: speeding alerts, impaired-driving detection or phone-distraction blocking. The
business case sized each feature's addressable crash cost as the weighted cost of all crashes involving that factor, and the three numbers
summed to more than the cost of all factor-involved crashes.

## 2. The decision (one deterministic recommendation)

**The feature prioritised (largest Shapley-allocated weighted crash cost), with single-factor, Shapley and joint totals.**

Rules (product memo):

* Data: CRSS for the year in memo; weights (`WEIGHT` on accident file); crash severity by maximum injury severity (KABCO).
* Factor flags per crash: speeding-related (vehicle file speeding indicator), alcohol-involved (any driver with alcohol involvement per memo
  rule), distraction (driver distraction codes indicating phone use per memo).
* Cost per crash by maximum severity (memo's unit costs).
* Single-factor total for factor f = Σ weight × cost over crashes with f.
* Shapley allocation (equal split among factors present) = Σ weight × cost × (1 ÷ number of factors present) over crashes with f.
* Joint total = Σ weight × cost over crashes with any factor.
* Bridge: Σ single-factor totals → minus overlaps → joint total.
* Priority: largest Shapley total.

## 3. Why capable analysts get it wrong

* "Crashes involving X" is the standard safety statistic.
* Multiple factors co-occur; involvement totals overlap.
* Attribution shares must sum to the joint total.
* Weights must be applied (CRSS is a probability sample).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ACCIDENT.csv` | CSV | ~55k | NHTSA CRSS | U.S. Gov public domain | Crashes, weights, severity |
| 2 | `VEHICLE.csv` | CSV | ~95k | NHTSA CRSS | Public domain | Speeding indicators |
| 3 | `PERSON.csv` | CSV | ~140k | NHTSA CRSS | Public domain | Driver alcohol involvement |
| 4 | `DISTRACT.csv` | CSV | ~95k | NHTSA CRSS | Public domain | Distraction codes |
| 5 | `crss_analytical_users_manual.pdf` | PDF | — | NHTSA | Public domain | Codes, weights |
| 6 | `unit_costs_by_severity.json` | JSON | 5 | Task author (from NHTSA economic cost study; cite) | Public domain | Costs |
| 7 | `product_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `business_case_involvement.xlsx` | XLSX | 3 | Task author | — | Naive sizing |
| 9 | `factor_flag_rules.json` | JSON | — | Task author | — | Code mapping |

## 5. Deterministic solution path

1. Build crash-level factor flags from vehicle, person and distraction files.
2. Attach weights and costs; single-factor totals; Shapley totals; joint total.
3. Bridge; priority.
4. Contrast with the business case.

## 6. Wrong paths (method errors, not misreadings)

**A — involvement totals as addressable.** Double counting.

**B — unweighted counts.** Not national estimates.

**C — vehicle-level costs.** Multi-vehicle crashes counted repeatedly.

**D — priority by single-factor totals.** Overlap-driven choice.

## 7. Why the stump is analytical, not semantic

Flags, costs and attribution are specified. The trap is non-additive overlapping attributions.

## 8. Draft task prompt (prose)

> Which telematics feature should we build next? Attribute weighted crash costs across speeding, alcohol and distraction without double counting,
> as the product memo specifies. Provide `attribution_bridge.csv` (factor: involved, Shapley; joint total), `factor_overlap_venn.png`, and a
> one-page `feature_priority.pdf`.

## 9. Deliverables

* `attribution_bridge.csv`, `factor_overlap_venn.png`, `feature_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 involved totals; 3 Shapley totals; joint; 7 overlap-region totals; priority; severity breakdown (5).

## 11. Golden-output checklist

* Flag rules; crash-level aggregation; weights; Shapley; joint; bridge.

## 12. Build notes (scope tuning)

* Confirm the involvement ranking differs from the Shapley ranking.
