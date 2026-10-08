# DA34 — Sizing a feeder: the sum of each home's peak is not the peak of the homes

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Capacity planning in clouds and CDNs (sum of per-tenant peaks versus peak of aggregate demand), and utility distribution planning |
| Domain | Electricity distribution |
| Task shape | 05 · Allocation to a fixed total (allocate a transformer's 300 kVA rating across customer groups by coincident-peak contribution so allocations sum exactly to 300) |
| Core method | Coincident peak (maximum of the group's aggregate 30-minute load) versus sum of individual maxima; diversity factor = Σ individual peaks ÷ coincident peak as a function of group size; allocation by each group's contribution to the aggregate at the coincident peak interval |
| Analytical stump | Allocating capacity by each customer's own peak over-allocates because peaks rarely coincide; the diversity factor grows with group size. Rooftop solar shifts the timing of net peaks. Allocation must use contributions at the moment of the coincident peak |
| Primary sources | Ausgrid "Solar home electricity data" (300 homes, half-hourly general consumption, controlled load and gross generation) |

## 1. The real-world situation

A distribution network operator plans a new 300 kVA transformer to serve three customer groups in a new estate, using measured loads from
comparable homes. The first plan sized each group by the sum of its customers' individual annual peaks; the total exceeded 600 kVA, implying
two transformers. A planner suggested using coincident peaks.

## 2. The decision (one deterministic recommendation)

**The allocation of the 300 kVA rating across the three groups (kVA, one decimal, summing exactly to 300.0), based on each group's contribution
at the combined coincident peak, and the diversity factor for each group.**

Rules (planning memo):

* Data: Ausgrid solar home data for the year in the memo; 300 homes; half-hourly kWh for general consumption (GC), controlled load (CL) and gross
  generation (GG).
* Net load per home per interval (kW) = (GC + CL − GG) × 2; power factor 0.95 for kVA (memo).
* Groups: A = homes without controlled load; B = homes with controlled load; C = homes with generator capacity ≥ 3 kWp (assignment order in the
  memo resolves overlaps).
* Coincident peak: maximum over intervals of Σ net load across all 300 homes, scaled to the estate's home counts per group (scale factors in
  the memo).
* Group contribution = group's scaled net load at that interval; allocation = 300 × contribution ÷ total, rounded with largest remainder.
* Diversity factor per group = Σ individual annual peaks ÷ group coincident peak.

## 3. Why capable analysts get it wrong

* Individual peaks are easy to compute and feel conservative.
* Load diversity means the aggregate peak is much lower than the sum of peaks.
* Solar generation moves net peaks to evening; daytime peaks of homes with solar may be negative.
* Allocations must be computed at a single interval to add up.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `<year> Solar home electricity data.csv` | CSV | ~300 homes × 3 channels × 365 days (wide, 48 intervals) | Ausgrid | Ausgrid terms (free use with attribution; verify) | Half-hourly data |
| 2 | `solar_home_data_notes.pdf` | PDF | — | Ausgrid | Same | Data notes, cleaned subset |
| 3 | `home_attributes.csv` | CSV | 300 | Derived (postcode, generator capacity) | Same | Group assignment |
| 4 | `estate_home_counts.json` | JSON | 3 | Task author | — | Scaling |
| 5 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `first_plan_sum_of_peaks.xlsx` | XLSX | 3 | Task author | — | First plan |
| 7 | `net_load_long.parquet` | Parquet | ~5.3M | Derived | Same | Long format |
| 8 | `diversity_factor_reference.pdf` | PDF | — | Cite (distribution planning texts) | Cite | Concept |

## 5. Deterministic solution path

1. Reshape to long; compute net kW and kVA per home-interval.
2. Assign groups; individual peaks; group coincident peaks; diversity factors.
3. Scaled aggregate; coincident peak interval; contributions; allocation with rounding.
4. Contrast with sum-of-peaks plan.

## 6. Wrong paths (method errors, not misreadings)

**A — sum of individual peaks.** Over-sizing.

**B — gross consumption ignoring generation.** Peak timing wrong.

**C — allocations from group-specific peaks at different times.** Do not sum to the coincident total.

**D — controlled load omitted.** Underestimates night peaks.

## 7. Why the stump is analytical, not semantic

Channels, groups and allocation are specified. The trap is non-additivity of maxima and timing of peaks.

## 8. Draft task prompt (prose)

> How should the new transformer's 300 kVA be allocated across the three customer groups? Use measured home loads and the coincident-peak
> method in the planning memo. Provide `group_allocation.csv` (group: homes, sum of peaks, coincident peak, diversity factor, contribution,
> allocation), `aggregate_peak_day.png`, and a one-page `transformer_sizing.pdf`.

## 9. Deliverables

* `group_allocation.csv`, `aggregate_peak_day.png`, `transformer_sizing.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 groups × 6 values = 18; peak interval; totals; rounding; contrast; diversity curve points.

## 11. Golden-output checklist

* Net load sign; kVA conversion; group assignment order; scaling; peak interval; rounding.

## 12. Build notes (scope tuning)

* Confirm the sum of scaled individual peaks exceeds 2× the coincident peak.
