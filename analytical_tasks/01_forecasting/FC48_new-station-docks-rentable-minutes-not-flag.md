# FC48 — How many docks to add at this winter's thirty new bike-share stations, when the feed says every station was in service all winter and half the waterfront mornings had no bike to rent

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · micromobility network expansion |
| Mirrors | Sizing capacity at new sites whose first weeks of demand were capped by supply (bike-share stations, parcel lockers and chargers, new stores and dark stores whose shelves were empty at launch), where the "in service" flag records the hardware rather than whether a customer could be served |
| Decision shape | One figure committed at a date: the July dock order placed with the manufacturer |
| Committed call | Docks to add across the thirty winter-opened stations before July, as a whole number |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · the population a flag suggests (measured #5: peak hours the feed flags in service, not peak hours a bike could be rented), with finer controls separating constructions (measured #12) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #12 stops at the first control that passes · #13 validates on one population, applies to another |
| Calibration form | Published control set: the city's July station census for 2025 and 2026, weekday 08:00–08:59 departures at every station, the figures the city permits dock expansions against |
| Driving force | A station's demand is its departures per peak hour in which a bike could be rented. The feed's is_renting flag says whether the dock hardware is up. For every earlier cohort the two agreed, because new stations joined the rebalancing routes in their first week. This winter's twelve waterfront and park stations sat outside the depots' route areas until March, and the five-minute status snapshots show them empty at 08:00 on 45% of weekdays while the flag showed them renting. Their winter level, the base every forecast multiplies by the summer index, is understated by almost half, and they are the stations with the steepest summer rise. |

## 1. Situation

A city bike-share operator opened thirty stations between December and January, each with 15 docks: eighteen near transit stops and
twelve along the waterfront and in parks. The expansion standard gives a station enough docks that its forecast July average weekday
08:00–08:59 departures are at most 80% of its docks, and the dock modules must be ordered by 15 March. The pack holds two years of trips,
the station feed with its is_renting flag, the five-minute status snapshots, the rebalancing route register, the zone groups, the federal
holiday calendar and the city's July station census for the last two years.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: trips, the feed, the snapshots, the route register and the census. No stakeholder's reading of their
  own numbers is overturned; the waterfront stations really did record few winter departures and the flag really did read renting. The
  difficulty is which peak hours count as hours a station could serve, which the flag does not record.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the expansion lead's view and every voice. Recorded departures per flagged weekday are still the natural
  winter level, and seasonally scaled they still leave the waterfront stations needing three docks or none.
* **Instrument repair.** Imagine a feed whose flag tracked bikes on the dock. The empty mornings would be visible, but July demand is still
  a forecast: a winter level scaled by the summer rise of the right peers, which no better record of winter supplies.
* **Lens swap.** The naive read and the answer average over different populations: weekdays the hardware was up, against peak hours in
  which a rider could actually take a bike.

## 3. The driving force

A strong solver borrows seasonality from mature stations, measures each new station's level from its first eight weeks deseasonalized,
and scales it to July. It finds that the city census reproduces last year's cohort total under a citywide index but misses every station
inside it, so it takes peers by demand type: stations where most departures fall on weekends follow a leisure curve that rises 4.5 times
from January to July, transit stations one that rises 1.4 times. It drops the three federal holidays the census does not count. It
orders 114 docks. Every step is correct. But each level was measured over the weekdays the feed flagged as renting, and for the twelve
waterfront and park stations that is not the same thing as weekdays a bike could be rented: they were off the rebalancing routes until
March, and the five-minute snapshots show their last bike gone by 07:40 on 45% of weekdays. Measured over the peak hours they could
serve, their winter level is 6.3 departures, not 3.5, and on the leisure curve each needs 21 more docks. The order is 306.

## 4. The ladder

| Rung | Construction | Lands on (docks) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Level per flagged weekday over eight weeks, deseasonalized and scaled by a citywide index from mature stations | 144 (−53%) | The standard cold-start method, and it reproduces last year's cohort total in the census within 3% | The census's station rows: under the citywide index last year's waterfront and park stations ran 40% above forecast and its transit stations 15% below |
| 1 | Index by demand type (leisure where most departures fall on weekends, transit otherwise), each new station scaled by its own type | 84 (−73%) | Passes the census at station level as well as in total | The holiday calendar: three of the forty weekdays were Christmas, New Year's Day and Martin Luther King Jr. Day, which the census does not count as weekdays |
| 2 | Hygiene: holidays removed from the eight weeks | 114 (−63%) | Right peers, right days, every count reconciled to the trips | The status snapshots: the twelve waterfront and park stations had no bike at 08:00 on 45% of weekdays while the feed flagged them renting |
| 3 | **Decisive:** each station's level measured over the peak hours a bike could be rented, from the snapshots, then scaled by its type's index | **306** | — | — |

* **Figure shape.** The answer is the extreme cell: every other construction orders fewer docks, the nearest 14% fewer, so a solver who
  stops anywhere short leaves the waterfront stations full by mid-morning in July.
* **Partial correction priced (L3).** A solver who measures over rentable hours but keeps the citywide index lands at 162 (−47%): on the
  citywide curve even the corrected waterfront level stays under 15 docks' worth. One who measures over rentable hours but leaves the
  holidays in lands at 264 (−13.7%).
* **Grid.** Index (citywide, by type) × holidays (in, out) × exposure (flagged weekdays, rentable peak hours) = 8 cells: 144, 144, 162,
  162; 84, 264, 114, 306. The nearest wrong cell is 264, 13.7% short.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard speaks of forecast departures; the feed's guide defines is_renting as the dock hardware accepting
   rentals. No document says a station without bikes was not serving, or that the new stations were off the routes.
2. **Corpus blind to the gap.** *In every earlier cohort the new stations joined the rebalancing routes in their first week, because every
   earlier expansion sat inside the depots' route areas; so the flagged weekdays were the weekdays a bike could be rented, and the
   flag-based level reproduced every new station's July census count within 5%.*
3. **No arithmetic symptom.** Departures reconcile to trips, the flag to the feed's history, the census to the trips; every rung's order
   is internally consistent.
4. **Not a row predicate.** Rentable exposure comes from the snapshots, minute by minute, aggregated to each station's peak hours and used
   as the denominator of its level; departures alone carry no trace of the minutes they could not happen.
5. **The enumeration is arithmetic.** No column marks an empty morning; it is computed from bikes available in the snapshots.
6. **No cutover date.** The route register dates the stations' joining in March, after the eight weeks; nothing steps inside the window
   the level is measured on.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The city's July census for 2025 and 2026: weekday 08:00–08:59 departures at every station, with last year's winter cohort
  inside it.
* **What it certifies.** The demand-type index (it reproduces every station of last year's cohort within 5%, where the citywide index
  reproduces only the total) and the holiday rule.
* **What it is blind to.** Rentable exposure: every earlier new station was on a route from its first week.
* **Twin pair.** Harbor Steps and Pier Gardens, two mature leisure stations with 15 docks each, recorded the same 12 weekday peak
  departures a day through the March 2025 depot outage, under the same flag. In April they ran 13 and 26 (2.0× apart), because Pier
  Gardens had no bike at 08:00 on half the outage weekdays and Harbor Steps on none. Departures per flagged day predict them equal; only
  departures per rentable hour reproduce both.
* **Resemblance points at the decoy.** By winter departures and docks, the waterfront stations most resemble last winter's quiet new
  stations, none of which needed docks in July.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The expansion standard: a station gets enough docks that its forecast July average weekday 08:00–08:59 departures are
  at most 80% of its docks. The census counts working weekdays only. Mature stations are those open for 24 months or more.
* **Empirical pins.** The leisure and transit indices, from mature stations' last two years. Rentable exposure, from the snapshots.
* **Voices.** The expansion lead: "The waterfront stations barely moved all winter; they won't need anything." The operations manager:
  "Every new station was renting from the day it opened; the feed shows it." The network planner: "Seasonality is seasonality; one index
  for the city is plenty."
* **Licensed wrong basis.** The standard records that the city's permit office checks dock requests against recorded departures per
  in-service day and will review the order on that basis.

## 8. Determinism by construction

* **Exposure.** A waterfront station was either stocked through the whole peak hour or empty from 07:40, so rentable minutes and rentable
  weekdays give the same exposure within 1%.
* **Demand type.** Transit stations draw at most 35% of departures at weekends, leisure stations at least 60%, in the new stations' eight
  weeks and in every mature station, so the split has one reading.
* **Index.** January and July indices from mature stations' last two years: leisure 0.40 and 1.80, transit 0.80 and 1.10, citywide 0.70
  and 1.30; one-year and two-year averages agree within 2%.
* **Rounding.** Every station's docks needed sits at least 0.35 from a whole number under every construction (transit 17.4, waterfront
  35.4 on the answer).
* **Maturity.** The eight weeks are closed and every snapshot is in the pack.

## 9. Prompt sketch and deliverables

> Thirty bike-share stations opened this winter, and the dock order for July goes to the manufacturer by 15 March. Our expansion lead says
> the waterfront stations barely moved all winter and won't need anything. Tell me how many docks to add across the new stations, as a
> whole number, in one sentence for the purchase order, and send `dock_order.xlsx` with the build and the sheets below, a chart
> `new_station_levels.svg`, and a one-page `order_note.html`.

* `dock_order.xlsx` — each new station's level, July forecast and docks under each construction, the parking sheet (ask A) and the faults
  sheet (ask B).
* `new_station_levels.svg` — one row per new station: flagged weekdays and rentable peak hours as paired bars, the winter level under each
  as dots, the July forecast against 80% of 15 docks as a reference line, and the docks added labelled at the end of each row.
* `order_note.html` — the committed order, the twelve stations that drive it, and why the feed's flag understated them.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six zone groups and each month of last quarter, the share of e-bike trips that
  ended away from a dock. *Device:* a trip ending within 50 metres of a station is snapped to that station in the trip table, with the true
  end point in the GPS-end table, as the data guide documents; reading the station ID counts lock-to parking as docked returns. Trip ends
  enter no part of the dock forecast.
* **Ask B (device-carried).** For each zone group, the dock faults reported last quarter. *Device:* a fault reported by several riders is
  one work order with several reports, linked in the work-order table, as the maintenance guide documents; counting reports overstates
  faults in every zone. Faults enter no part of the dock forecast.
* **Ask C (validity).** The order under each of the four rung constructions, and how many of last year's cohort's census counts each index
  reproduces within 5%.
* **Decoupling.** Clearing the rentable exposure changes no figure in asks A or B.

## 11. Rubric arithmetic

6 zone groups × 3 months (ask A) + 6 zone groups (ask B) + 4 constructions × 2 (ask C) + the committed order and the docks per transit and
per waterfront station + 5 named chart parts + 3 files ≈ 43 criteria.

## 12. World-building constraints

* New stations: 18 transit, 12 waterfront and park, 15 docks each. Weekday peak departures per flagged weekday: transit 9.64, waterfront
  3.29 (with holidays); holidays removed: 10.14 and 3.46. Waterfront stations empty at 08:00 on 45% of weekdays; rentable level 6.29.
* Orders by rung: 144 / 84 / 114 / 306 docks (transit 3 each, waterfront 21 each on the answer). Partials: citywide index with rentable
  exposure 162; rentable exposure with holidays in 264.
* Census: last year's cohort total within 3% under the citywide index; waterfront and park stations 40% above it, transit 15% below.
* The twin stations are identical on every feed and trip column through the outage; April departures 13 and 26.
* Snapped trip ends and work-order reports touch no departure, snapshot or dock in the forecast.
