# FC48 — How many docks to add at this winter's thirty new bike-share stations, when the summer curve they borrow must come from stations of like demand and the maintenance zones only mostly match it

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · micromobility network expansion |
| Mirrors | Cold-start capacity for new sites that borrow seasonality from peers (bike-share stations, parcel lockers and chargers, new stores and dark stores), where the operations grouping everyone plans by only mostly matches the demand the new site will see |
| Decision shape | One figure committed at a date: the July dock order placed with the manufacturer |
| Committed call | Docks to add across the thirty winter-opened stations before July, as a whole number |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · the population a field suggests (measured #5: peers by maintenance zone, where the standard's "like demand" is set by catchment land use through the parcel register), with finer controls separating constructions (measured #12) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #12 stops at the first control that passes · #14 coarsens the segment it was asked about |
| Calibration form | Published control set: the city's July station census for 2025 and 2026, weekday 08:00–08:59 departures at every station, the figures the city permits dock expansions against |
| Driving force | A new station borrows its summer rise from mature stations of like demand. The dashboard's seasonal indices, and every plan the depots make, group stations by maintenance zone, and the zone index reproduces the census zone by zone. But demand follows what lies around a station: where parkland, beaches and waterfront make up most of its 400-metre catchment, July runs 4.5 times January; where offices and transit dominate, 1.4 times. Five of this winter's stations sit in parks inside the Downtown zone, whose mature peers are mostly commuter stations, and the zone index gives them no summer at all. The class is reached only by intersecting each catchment with the city's parcel register. |

## 1. Situation

A city bike-share operator opened thirty stations between December and January, each with 15 docks: ten along the waterfront and twenty
in the Downtown maintenance zone, five of them in parks. The expansion standard gives a station enough docks that its forecast July average
weekday 08:00–08:59 departures are at most 80% of its docks, with seasonality borrowed from mature stations of like demand. The dock
modules must be ordered by 15 March. The pack holds two years of trips, the station feed with each station's maintenance zone, the
dashboard's seasonal indices by zone, the city's land-use parcel register, the planning manual, the federal holiday calendar and the city's
July station census for the last two years.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: trips, the feed, the zone indices, the parcel register and the census. No stakeholder's reading of
  their own numbers is overturned; the zone indices really do reproduce the census zone by zone. The difficulty is which mature stations a
  new station is like, which the zone does not say.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the expansion lead's view and every voice. The dashboard's zone indices are still the natural peers, they
  still pass the census zone by zone, and they still give the park stations no summer.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: the trip table holds
  every departure, the census every station's July count, the parcel register every parcel's land use, and the maintenance zone records
  which depot services a station, a different attribute from demand, so using it as a peer group is an ordinary wrong rung. With nothing
  to repair, rung 0 returns 90 docks, rung 1 95 and rung 2 120, and the catchment classing is still needed, because no file records a
  station's demand class.
* **Lens swap.** The naive read and the answer borrow from different populations: the mature stations a depot maintains, against the
  mature stations whose surroundings draw the same riders.

## 3. The driving force

A strong solver borrows seasonality from mature stations, measures each new station's level from its first eight weeks deseasonalized,
and scales it to July. It finds that a citywide index reproduces last year's cohort total in the census but misses every zone inside it,
so it moves to the dashboard's zone indices, which pass the census zone by zone. It drops the three federal holidays the census does not
count. It orders 120 docks. Every step is correct. But the standard borrows from stations of like demand, and the planning manual classes
demand by what a station's 400-metre catchment holds: leisure where parkland, beaches and waterfront exceed 40% of it, commuter otherwise.
The Downtown zone is mostly commuter stations, so its index rises a sixth from January to July; the five park stations opened there this
winter follow the leisure curve, which rises four and a half times, and on it each needs 7 more docks. On the leisure curve the waterfront
stations need 8 each rather than 3, and on the commuter curve the Downtown commuter stations need 2 rather than 6. The order is 145.

## 4. The ladder

| Rung | Construction | Lands on (docks) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Level per weekday over eight weeks, deseasonalized and scaled by a citywide index from mature stations | 90 (−37.9%) | The standard cold-start method, and it reproduces last year's cohort total in the census within 3% | The census's zone totals: under the citywide index last year's Waterfront cohort ran 45% above forecast and its Downtown cohort 12% below |
| 1 | The dashboard's zone indices, each new station scaled by its own maintenance zone's | 95 (−34.5%) | Passes the census in total and zone by zone | The holiday calendar: three of the forty weekdays were Christmas, New Year's Day and Martin Luther King Jr. Day, which the census does not count as weekdays |
| 2 | Hygiene: holidays removed from the eight weeks | 120 (−17.2%) | Right days, zone-level peers that pass every zone control, every count reconciled to the trips | The census's station rows: inside the Downtown zone, last year's new stations whose catchments are mostly parkland ran 2.1 times the zone index's forecast, and those mostly offices and transit 0.9 times |
| 3 | **Decisive:** every mature and new station classed by catchment land use through the parcel register, each new station scaled by its class's index | **145** | — | — |

* **Figure shape.** Every correction walks the order up (90, 95, 120) and the decisive rung is the last step up, so the answer is the
  maximum cell and a solver who stops anywhere short leaves the park stations full by mid-morning in July.
* **Partial correction priced (L3).** A solver who builds leisure and commuter indices but takes each new station's class from its
  maintenance zone (waterfront leisure, Downtown commuter) lands at 110 (−24.1%): the park stations stay on the commuter curve. One who
  classes by catchment but leaves the holidays in lands at 115 (−20.7%).
* **Grid.** Peers (citywide, maintenance zone, class from the zone, class from the catchment) × holidays (in, out) = 8 cells: 90, 105;
  95, 120; 85, 110; 115, 145. The nearest wrong cells are 120 (−17.2%) and 115 (−20.7%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "mature stations of like demand"; the planning manual defines demand classes for the network
   plan, not for seasonality; no document says the zone indices are the wrong peers.
2. **Reproduction (Pattern B).** Catchment-class peers reproduce the July census count of all 24 of last year's new stations within 5%;
   zone peers 19, every miss a park or ferry-side station; the citywide index 11. The rule is a construction, not a menu: each station's
   400-metre catchment intersected with the parcel register, land-use shares computed, the class drawn at 40%, and an index built for each
   class from its mature stations.
3. **No arithmetic symptom.** Departures reconcile to trips, zone indices to the dashboard, the census to the trips; every rung's order
   is internally consistent.
4. **Not a row predicate.** A station's class needs a spatial intersection with thousands of parcels and an area share before any peer
   group exists, and the order then runs through each class's index.
5. **The enumeration is arithmetic.** No column holds a demand class; it is computed from geometry and land use.
6. **No cutover date.** Nothing steps; the park stations were simply opened inside a zone drawn for depots.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The city's July census for 2025 and 2026: weekday 08:00–08:59 departures at every station, with last year's 24 new stations
  inside it.
* **What it certifies.** The zone indices at zone level (they reproduce each zone's total) and the holiday rule.
* **What it pins.** The peer rule: only catchment classes reproduce every one of last year's new stations.
* **Twin pair.** Mill Green and Carver Street, two of last year's new stations in the Downtown zone, had 15 docks each and identical
  winter departures. Their July census counts were 26 and 13 (2.0× apart), because Mill Green's catchment is 70% parkland and Carver
  Street's 5%. Zone, docks and winter departures predict them equal; only the catchment class reproduces both.
* **Resemblance points at the decoy.** By zone, docks and winter departures, the park stations most resemble last winter's quiet Downtown
  stations, none of which needed docks in July.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The expansion standard: a station gets enough docks that its forecast July average weekday 08:00–08:59 departures are
  at most 80% of its docks, with seasonality from mature stations of like demand. The census counts working weekdays only. Mature
  stations are those open for 24 months or more. The planning manual's demand classes.
* **Empirical pins.** The class indices (leisure January 0.40, July 1.80; commuter 0.80 and 1.10), from mature stations' last two years.
  Each station's class, from the parcel register.
* **Voices.** The expansion lead: "The waterfront stations barely moved all winter; they won't need anything." The depot manager: "We plan
  everything by zone; the zones are how this network works." The network planner: "Seasonality is seasonality; one index for the city is
  plenty."
* **Licensed wrong basis.** The standard records that the city's permit office reviews dock requests against the dashboard's zone indices
  and will check the order on that basis.

## 8. Determinism by construction

* **Class line.** No station's catchment holds between 30% and 50% parkland, beach and waterfront, so any line in that range classes
  every station the same way.
* **Catchment.** 300-, 400- and 500-metre catchments give the same classes.
* **Indices.** One-year and two-year averages agree within 2%: citywide January 0.72 and July 1.30, Waterfront zone 0.46 and 1.60,
  Downtown zone 0.70 and 1.20.
* **Rounding.** Every station's docks needed sits at least 0.36 from a whole number under every construction (waterfront 22.5, park 21.6,
  Downtown commuter 16.5 on the answer).
* **Maturity.** The eight weeks are closed and every trip is in the pack.

## 9. Prompt sketch and deliverables

> Thirty bike-share stations opened this winter, and the dock order for July goes to the manufacturer by 15 March. Our expansion lead says
> the waterfront stations barely moved all winter and won't need anything. Tell me how many docks to add across the new stations, as a
> whole number, in one sentence for the purchase order, and send `dock_order.xlsx` with the build and the sheets below, a chart
> `new_station_curves.svg`, and a one-page `order_note.html`.

* `dock_order.xlsx` — each new station's level, class, July forecast and docks under each construction, the parking sheet (ask A) and the
  faults sheet (ask B).
* `new_station_curves.svg` — the citywide, zone and class indices by week as lines, the five park stations' winter weeks plotted against
  them, the July forecast against 80% of 15 docks as a reference line, and the docks added labelled for each group of stations.
* `order_note.html` — the committed order, the five park stations behind it, and why the zone indices understated them.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the thirty new stations, the share of e-bike trips in its first eight weeks that
  ended away from a dock. *Device:* a trip ending within 50 metres of a station is snapped to that station in the trip table, with the true
  end point in the GPS-end table, as the data guide documents; reading the station ID counts lock-to parking as docked returns at
  nineteen stations. Trip ends enter no part of the dock forecast, which counts departures.
* **Ask B (device-carried).** For each of the network's six maintenance zones, the dock faults reported last quarter. *Device:* a fault
  reported by several riders is one work order with several reports, linked in the work-order table, as the maintenance guide documents;
  counting reports overstates faults in every zone. Faults enter no part of the dock forecast.
* **Ask C (validity).** The order under each of the four rung constructions, and how many of last year's 24 new stations each set of peers
  reproduces within 5%.
* **Decoupling.** Clearing the catchment classing changes no figure in asks A or B.

## 11. Rubric arithmetic

30 new stations (ask A) + 6 zones (ask B) + 4 constructions × 2 (ask C) + the committed order and the docks per waterfront, park and
Downtown commuter station + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* New stations: 10 waterfront (leisure), 5 park stations in the Downtown zone (leisure), 15 Downtown commuter, 15 docks each. Weekday peak
  departures per weekday with holidays in: waterfront 3.80, park 3.65, commuter 9.10; holidays remove 5.2% of the base.
* Orders by rung: 90 / 95 / 120 / 145 docks (waterfront 8 each, park 7, commuter 2 on the answer). Grid: citywide with holidays out 105;
  class from the zone 85 and 110; catchment class with holidays in 115.
* Census: last year's 24 new stations; catchment peers reproduce 24, zone peers 19, citywide 11, all within 5%.
* The twin stations are identical on zone, docks and winter departures; July 26 and 13.
* Snapped trip ends and work-order reports touch no departure, class or dock in the forecast.
