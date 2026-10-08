# OS27 — Which delivery vans can go electric? A van that averages 60 miles still has 140-mile days

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Feasibility sizing on averages versus tails (capacity for peak days, SLAs on worst-case latency, battery range for worst days) in fleet and infrastructure planning |
| Domain | Commercial fleets / electrification |
| Task shape | 14 · Cuts of a distribution (per-vehicle daily-distance percentiles by vocation; the share of vehicles suitable for a 150-mile-range EV at the 95th-percentile day; the replacement order size) |
| Core method | Per-vehicle distribution of daily distance and energy-relevant metrics from drive-cycle logs; suitability if the vehicle's 95th percentile daily distance × winter derate ≤ usable range; fleet share by vocation; comparison with average-based suitability |
| Analytical stump | Average daily miles make most vehicles look suitable; operations fail on the long days. Range must also be derated for cold weather and battery ageing. Sizing the EV order on averages commits vehicles that will strand on their worst days |
| Primary sources | NREL Fleet DNA commercial vehicle drive-cycle data (vocational vehicles) |

## 1. The real-world situation

A logistics company plans to replace part of its delivery fleet with electric vans with 150 miles of rated range. The sustainability team
counted vehicles whose average daily distance is below 150 miles and proposed replacing 85% of the fleet. Operations noted that routes vary
widely by day and season.

## 2. The decision (one deterministic recommendation)

**The number of vans in the replacement order: vehicles in the in-scope vocations whose 95th-percentile daily distance ≤ usable range, scaled
to the company's fleet by vocation shares.**

Rules (fleet memo):

* Data: Fleet DNA vehicle-day summaries for vocations in scope (parcel delivery, linen delivery, beverage delivery per memo); vehicles with ≥ 20
  operating days.
* Usable range on a day = 150 × 0.8 (battery reserve and ageing) = 120 miles, further × 0.75 = 90 miles on days in December–February
  (winter derate).
* Daily ratio = daily distance ÷ that day's usable range; a vehicle is suitable if the 95th percentile of its daily ratios is ≤ 1.
* Fleet scaling: suitable share by vocation × company vehicles by vocation (`company_fleet.json`).
* Order size = Σ suitable vehicles (rounded down).
* Report the average-based count for contrast.

## 3. Why capable analysts get it wrong

* Average daily distance is the most common summary.
* Daily distances are right-skewed; peaks matter for operations.
* Range depends on season and battery health.
* Per-vehicle evaluation is required; fleet-level percentiles mix vehicles.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `fleet_dna_vehicle_day_summaries.csv` | CSV | ~30k vehicle-days | NREL Fleet DNA | Public (NREL data terms; verify) | Daily distance, speed, stops, vocation |
| 2 | `fleet_dna_documentation.pdf` | PDF | — | NREL | Public | Field definitions |
| 3 | `company_fleet.json` | JSON | — | Task author | — | Vehicles by vocation |
| 4 | `fleet_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `sustainability_average_count.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 6 | `range_derate_assumptions.json` | JSON | — | Task author (from public EV range studies; cite) | — | Derates |
| 7 | `vehicle_percentiles.parquet` | Parquet | ~500 | Derived | Public | Per-vehicle stats |

## 5. Deterministic solution path

1. Filter vocations and vehicles with enough days.
2. Daily usable range by season; ratio; per-vehicle 95th percentile.
3. Suitable shares by vocation; scale to company fleet; order size.
4. Contrast with average-based count.

## 6. Wrong paths (method errors, not misreadings)

**A — average daily miles.** Overstated suitability.

**B — fleet-wide percentile.** Mixes vehicles.

**C — no derates.** Overstated range.

**D — percentile of distance rather than of ratio to that day's range.** Ignores winter coincidence.

## 7. Why the stump is analytical, not semantic

The thresholds and derates are specified. The trap is feasibility on averages versus tails.

## 8. Draft task prompt (prose)

> How many delivery vans should our first EV order include? Evaluate each vehicle's worst-day needs from Fleet DNA as the fleet memo specifies.
> Provide `vehicle_suitability.csv` (vehicle: days, mean, P95 ratio, suitable), `distance_distributions.png`, and a one-page `ev_order_size.pdf`.

## 9. Deliverables

* `vehicle_suitability.csv`, `distance_distributions.png`, `ev_order_size.pdf`.

## 10. Where 25+ rubric criteria come from

* Suitable shares for 3 vocations; P95 ratios for 10 vehicles; order size; contrast; derate handling.

## 11. Golden-output checklist

* Filters; seasonal derate; ratio; per-vehicle percentile; scaling; rounding.

## 12. Build notes (scope tuning)

* Confirm average-based suitability exceeds the tail-based share by ≥ 25 points.
