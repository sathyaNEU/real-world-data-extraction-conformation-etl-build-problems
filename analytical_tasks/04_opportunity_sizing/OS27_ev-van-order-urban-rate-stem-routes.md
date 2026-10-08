# OS27 — How many electric vans go into the second order, when the consumption rate that predicted every first-tranche route was measured on town streets

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · last-mile delivery fleet electrification |
| Mirrors | Feasibility sizing validated on a first deployment cohort and applied to a cohort that differs on one axis (delivery-van electrification at parcel carriers and marketplaces, data-centre power-per-rack models validated on one rack type and applied to another, warehouse-robot throughput validated on single-zone aisles) |
| Decision shape | One figure committed at a date: the tranche-2 van order, filed on the manufacturer's allocation form by the 20th |
| Committed call | The number of electric vans in the tranche-2 order, out of the 410 diesel vans coming off lease |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · E17 (a consumption rate validated on the first tranche's town routes, applied to forward routes that run long stems at speed), with E25 below it (the manufacturer's suppressed cold-weather cell, bounded by its published combined and warm figures) |
| Gate G mechanism | method_or_model_selection, with forecasting |
| Measured traps engaged | #13 validates on one population, applies to another · #24 treats an unpublished figure as unknown · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the signed tranche-1 close-out, route by route, for the 120 electric vans deployed last April |
| Driving force | Tranche 1's measured 0.40 kWh a mile predicts the worst day of all 120 closed routes within 2%, because every tranche-1 depot sits inside its delivery zone and its vans almost never leave town streets. The forward depots sit outside their zones, and 38% of their miles are stem miles at 50 mph or more, which segment telemetry prices at 0.64 kWh. A day-level fit cannot see speed, because tranche-1 days never vary in it. |

## 1. Situation

A parcel carrier's northern region has 410 diesel vans at six depots coming off lease next year. Last April it put 120 electric vans on the
routes of three town-centre depots, and the fleet board signed the tranche-1 close-out in November. The manufacturer needs the tranche-2
order on its allocation form by the 20th. The fleet policy says an electric van must complete its route's 95th-percentile day at
end-of-lease battery capacity, keeping a 15% reserve. The sustainability team expects most of the 410 to qualify.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the manufacturer's certified figures, the tranche-1 telemetry, the close-out's route-by-route
  predictions and the route master. The close-out's 0.40 is a true measurement of tranche 1. Nothing is overturned. The difficulty is that
  the forward routes are a different population on the one axis tranche 1 never varied.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the sustainability team's expectation and every voice. The close-out still certifies a rate with a 120-of-120
  record, and nothing in the pack says that rate depends on speed.
* **Instrument repair.** Give tranche 1 perfect telemetry for a full year. Its routes still contain 2–4% stem miles, so any day-level
  instrument still returns one rate that fits them all.
* **Lens swap.** Tranche-1 routes last year and the forward depots' routes next year are different populations at different moments. The
  answer rests on the forward routes' own speed profiles.

## 3. The driving force

A strong solver applies the policy's 95th-percentile day, bounds the winter penalty that the manufacturer will not publish, and replaces
the certified test-cycle consumption with the carrier's own measured rate. That rate is validated on 120 closed routes and is the best
evidence in the pack. But it was measured where nothing varied: every tranche-1 depot is a town-centre unit whose vans reach their first
drop within two miles. The six forward depots are edge-of-town sheds, and their vans run 8 to 19 miles of trunk road before the first drop.
The tranche-1 segment telemetry splits each day by speed, and it prices a town mile at 0.38 kWh and a stem mile (50 mph or more) at 0.64.
Daily totals hide this, because the day-level stem share never left 2–4%. The forward order needs each route's own stem share from the
route geometry, priced at the segment rates.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Policy design day (each route's 95th-percentile day) at the manufacturer's certified combined consumption, 0.47 kWh a mile | 312 vans, +57.6% | The policy test at the certified figure, which is the industry's standard suitability screen | The manufacturer's suppressed cold cell is bounded at 0.59–0.63 by its published combined and warm figures, and January design days need it |
| 1 | Warm days at 0.43, cold days at the bounded 0.59–0.63; the bound decides every van identically | 236 vans, +19.2% | Winter is handled with a defensible bound instead of a guess, and both ends of the bound give the same order | The close-out: 120 tranche-1 routes reproduce at 0.40 kWh a mile on warm days, not at the certified 0.43 |
| 2 | The close-out's measured 0.40 on warm days, scaled by the bounded cold ratio (1.37–1.47) | 281 vans, +41.9% | The carrier's own consumption, validated route by route on 120 closed routes | Segment telemetry prices a stem mile at 0.64 kWh against 0.38 in town, and the route master puts 38% of forward miles on stems |
| 3 | **Decisive:** each forward route's design day priced segment by segment (town at 0.38, stem at 0.64, cold ratio as at rung 2), from the route's own geometry | **198 vans** | — | — |

* **Figure shape.** The answer is the minimum cell of the grid, so every partial or missing correction over-orders vans that would need
  a mid-shift charge. The per-rung moves are −24.4%, +19.1% and −29.5%.
* **Partial correction priced (L3).** A solver who prices speed but applies each depot's average stem share to all of its routes lands at
  118 vans (−40.4%), as far below the answer as rung 2 is above it. The four edge-of-town depots run 96 short local loops whose own stem
  share is under 0.05, and the depot average condemns them with the stem routes. A solver who fits speed at day grain on tranche-1 days
  recovers no usable slope and stays at rung 2.
* **Grid.** Consumption basis (certified, tranche-1 day rate, segment rates) × winter (ignored, bounded) = 6 cells: 312, 236, 352, 281, 268
  and 198. The nearest wrong cell is rung 1 at +19.2%. Reaching it means keeping the certified test cycle against the carrier's own
  measured record. Segment rates without winter give 268 (+35.4%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The close-out reports one validated rate. No document says consumption depends on speed or that the forward depots
   sit outside their zones; the route geometry is a mapping file.
2. **Corpus blind for a computable reason.** *In every tranche-1 route the stem share is between 2% and 4%, because all three tranche-1
   depots sit inside their delivery zones.* The day rate and the segment rates predict every closed route's worst day within 1.5% of each
   other, so the close-out's 120-of-120 holds under both.
3. **No arithmetic symptom.** Daily energy, miles, charging sessions and the close-out's predictions reconcile under every rung, and the
   day-level fit has an R² of 0.99.
4. **Not a row predicate.** Each forward route's design-day energy is built from segment-level rates fitted on another fleet's telemetry
   and the route's own geometry (depot-to-zone stem plus in-zone loop) before the policy test applies.
5. **The enumeration is arithmetic.** No column says "stem route". Stem share is computed per route from the geometry file's segment speeds.
6. **No cutover date.** Depot location is geography; nothing steps in any series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The tranche-1 close-out: for each of the 120 routes, the predicted and observed worst-day energy, days operated and any
  mid-shift charge, signed by the fleet board in November. It answers whether tranche 1 worked, a labelled question about the past.
* **What it certifies.** The 95th-percentile design day, the 15% reserve and the warm-day rate of 0.40 kWh a mile: 120 of 120 routes within
  2%. A solver who back-tests rung 2 is confirmed.
* **What it is blind to.** Speed (above). No tranche-1 van has yet run a day below 0°C, so it is silent on cold as well, which is why the
  bound in rung 1 is needed.
* **Twin pair.** Forward depots Hartley Lane and Ousebridge are identical on every route-master column: 64 routes each, the same
  95th-percentile miles by route, stops, parcels and payload. Hartley Lane sits inside its zone (stem share 0.06) and Ousebridge 14 miles
  outside its own (0.45). They qualify 52 and 25 vans, 2.1× apart, and no depot-level rate reproduces both.
* **Resemblance points at the decoy.** The forward depots match the tranche-1 depots on stops per route, payload and 95th-percentile miles,
  so a solver who transfers the validated rate by resemblance files rung 2's 281.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fleet policy fixes the design day (the route's 95th-percentile day over the last two years), end-of-lease usable
  capacity at the manufacturer's warranted 88%, and the 15% reserve. The manufacturer's data sheet publishes combined (0.47) and warm (0.43)
  consumption, states that its annual test cycle is 20–25% cold-condition driving, and leaves the cold cell blank.
* **Empirical pins.** The town and stem rates come from tranche-1 segment telemetry. Each route's stem share comes from the geometry file.
* **Voices.** The sustainability lead: "Most of these routes are nowhere near the van's range; we're being timid." The tranche-1 programme
  manager: "Our model called every tranche-1 route to within two per cent." That is true.
* **Licensed wrong basis.** The fleet policy records that the lessor's residual-value team screens electric suitability on the
  manufacturer's certified consumption and will review the order on that basis.

## 8. Determinism by construction

* **The cold bound decides.** No van's design-day energy falls between the thresholds implied by 0.59 and 0.63 (or by cold ratios of 1.37
  and 1.47) under rungs 1, 2 or 3, so the order is exact without the suppressed value.
* **Percentile convention.** No route's 95th-percentile day lies within one mile of its threshold, so nearest-rank and interpolated
  percentiles return the same set.
* **Stem cut.** Segment speeds are bimodal: town segments run under 30 mph and stem segments over 55. Cuts at 45, 50 and 55 mph return the
  same stem shares to within one point.
* **Battery ageing.** End-of-lease capacity is pinned at 88% by the policy and the warranty, so no ageing curve is chosen.
* **Maturity and censoring.** Two full years of route history exist for every forward route, and the close-out window is closed. No
  forward route was added or re-cut in the last 90 days.

## 9. Prompt sketch and deliverables

> The van maker needs our tranche-2 order on its allocation form by the 20th, and the sustainability team would like it to be most of the
> 410 vans coming off lease. Tell me how many electric vans we order, as one whole number I can sign. Send `tranche2_order.xlsx`, a chart
> `route_energy.png`, and a one-page `order_note.pdf`.

* `tranche2_order.xlsx`: the route-by-route suitability test and the order by depot, the fuel sheet (ask A) and the shift sheet (ask B).
* `route_energy.png`: design-day energy against usable energy for all 410 routes as a scatter by depot, with the reserve line, the stem
  share as point colour, the two twin depots outlined, and the order count in the title.
* `order_note.pdf`: the committed order and the readings a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six forward depots, last year's diesel litres per 100 van-miles and fuel cost per
  van-mile. *Device:* depot pumps also fill yard tractors on the same fuel card, and the asset register's equipment code identifies them.
  Reversed transactions post as negative rows that carry the original transaction number. A naive per-depot total overstates van fuel by
  9–17% at the two depots with yard tractors and double-counts 41 reversals.
* **Ask B (device-carried).** For each depot, the share of routes whose 95th-percentile shift exceeds the 10-hour driving limit, and the
  median shift. *Device:* shifts that cross midnight are split into two timesheet rows by calendar date, as the payroll guide documents.
  Summing by date halves the longest shifts at the three depots with early starts.
* **Ask C (validity).** The order under each of the four rung bases, and the close-out's reproduction count under the day rate and under
  the segment rates (120 of 120 for both).
* **Decoupling.** Clearing the segment pricing changes no figure in asks A or B.

## 11. Rubric arithmetic

6 depots × 2 (ask A) + 6 depots × 2 (ask B) + 4 bases + 2 reproduction counts (ask C) + the committed order, its split by depot (6) and the
count lost to stems + 5 named chart parts + 3 files ≈ 46 criteria.

## 12. World-building constraints

* Tranche 1: 120 routes, stem share 2–4%, worst-day energy predicted by 0.40 kWh a mile within 2% on every route. No tranche-1 day below 0°C.
* Segment telemetry: town 0.38 kWh a mile and stem 0.64, identifiable from at least 9,000 tranche-1 stem miles. Forward region: 38% of
  miles on stems. Four edge-of-town depots, each with 20–28 local loops (stem share under 0.05).
* Rung counts are 312 / 236 / 281 / 198. Grid cells are 352 and 268. The depot-average partial lands at 118. No cell is within 19% of the
  answer.
* Hartley Lane and Ousebridge are identical on every route-master column and differ only in depot location.
* Fuel-card yard fills, reversals and midnight-split shifts never touch route geometry, telemetry or the close-out.
