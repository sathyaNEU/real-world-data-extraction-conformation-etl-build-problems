# DS07 — Repair or replace a water main: replace when the next break costs more than waiting

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Fleet and hardware replacement decisions (servers, vehicles, network gear) where failure rates rise with age and each failure has a cost |
| Domain | Water utilities / asset management |
| Task shape | 13 · Scenarios and the flip point (pipe cohorts × discount-rate and break-cost scenarios → replace now or defer; the replacement list for next year's capital plan and the break cost at which the plan flips) |
| Core method | Break-rate growth model per cohort (material × installation decade): breaks per km-year growing exponentially with age, fitted by Poisson regression with exposure; economic replacement time (Shamir–Howard): replace when the present value of future breaks avoided equals the replacement cost; segments whose threshold year ≤ next year are replaced |
| Analytical stump | Replacing the mains with the most past breaks (or the oldest) ignores how fast each cohort's break rate grows and the cost trade-off; some frequently broken pipes are cheaper to keep repairing, while some with few breaks so far are past their economic replacement point. The decision requires the break-rate model and discounting |
| Primary sources | City of Toronto Open Data — watermain breaks; Toronto water distribution main asset inventory (material, diameter, install year, length) |

## 1. The real-world situation

A water utility's capital plan replaces 40 km of mains per year. The draft list chose segments with the most breaks over the past decade. The
asset-management engineer argued for an economic replacement rule based on cohort break-rate growth, break costs and replacement costs.

## 2. The decision (one deterministic recommendation)

**Next year's replacement list (segments whose economic replacement year ≤ next year, ranked by net present benefit, capped at 40 km), and the
repair cost per break at which the top-ranked cast-iron cohort flips from "replace" to "defer".**

Rules (asset memo):

* Data: main segments with material, diameter, install year and length; breaks geocoded to segments (within 10 m) 1990–2023.
* Cohorts: material × install decade; break rate N(t) = N(t0) e^{A (t − t0)} per km; fit A and N(t0) by Poisson regression with log(length ×
  years at risk) offset.
* Segment-specific N(t0): cohort rate × (segment's observed breaks + 1) ÷ (cohort-expected breaks + 1) (credibility per memo).
* Economic replacement year t*: N(t*) = ln(1 + r) × C_replace ÷ C_break per km (Shamir–Howard), r = 4%.
* Costs: C_break = $18,000 per break; C_replace per km by diameter (memo table).
* Replace segments with t* ≤ next year; rank by NPV of break costs avoided over 20 years − replacement cost; cap 40 km.
* Flip point for the top cast-iron cohort: C_break at which its t* = next year.

## 3. Why capable analysts get it wrong

* Past break counts are visible and persuasive.
* Break rates grow at cohort-specific speeds; counts lag growth.
* Discounting and costs determine when replacement pays.
* Segment length and exposure years must enter the rates.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `watermain_breaks_1990_2023.csv` | CSV | ~45k | City of Toronto Open Data | Open Government Licence – Toronto | Break dates and locations |
| 2 | `water_distribution_mains.geojson` | GeoJSON | ~60k segments | City of Toronto Open Data | OGL – Toronto | Segment attributes |
| 3 | `replacement_costs_by_diameter.csv` | CSV | ~10 | Task author (from public capital budget documents; cite) | — | Costs |
| 4 | `asset_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `draft_break_count_list.xlsx` | XLSX | ~150 | Task author | — | Draft list |
| 6 | `shamir_howard_1979_citation.pdf` | PDF | — | Cite | Cite | Replacement rule |
| 7 | `breaks_segment_join.parquet` | Parquet | ~45k | Derived | OGL – Toronto | Break-to-segment matches |

## 5. Deterministic solution path

1. Join breaks to segments; compute exposure; cohorts.
2. Fit cohort models; segment adjustments; N(t) projections.
3. Economic replacement years; NPV ranking; 40 km cap.
4. Flip point; contrast with the draft list.

## 6. Wrong paths (method errors, not misreadings)

**A — most past breaks.** Ignores growth and costs.

**B — oldest pipes first.** Ignores material differences.

**C — no exposure offset.** Long segments penalised.

**D — undiscounted comparison.** Replaces too early.

## 7. Why the stump is analytical, not semantic

Models, costs and the rule are specified. The trap is replacing on history instead of forward-looking economics.

## 8. Draft task prompt (prose)

> Which water mains should next year's capital plan replace? Apply the economic replacement rule in the asset memo with cohort break-rate models.
> Provide `replacement_list.csv` (segment: cohort, length, breaks, N(t), t*, NPV, rank), `break_rate_curves.png`, and a one-page
> `capital_plan_mains.pdf` with the flip point.

## 9. Deliverables

* `replacement_list.csv`, `break_rate_curves.png`, `capital_plan_mains.pdf`.

## 10. Where 25+ rubric criteria come from

* Cohort A values (6); top-15 segments; km total; flip point; overlap with the draft list.

## 11. Golden-output checklist

* Join tolerance; exposure; Poisson fit; credibility adjustment; t*; NPV; cap; flip point.

## 12. Build notes (scope tuning)

* Confirm fewer than half the draft list's km appear in the economic list.
