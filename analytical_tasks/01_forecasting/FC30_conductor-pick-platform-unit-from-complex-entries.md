# FC30 — How many weekday-morning conductor shifts the spring pick funds, when the standard posts conductors per platform and every count is kept per station complex

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · public transit service planning |
| Mirrors | Staffing posts at the level where crowding happens rather than where it is counted (Apple Store floor zones against store door counts, fulfilment-centre dock doors against building volume, airport security lanes against terminal entries, campus shuttle stops against building badge-ins) |
| Decision shape | One figure committed at a date: the weekly conductor-shift count filed in the spring pick notice |
| Committed call | The number of weekday-morning platform conductor shifts per week for the spring pick (2 March – 26 June), as a whole number |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S1 (the unit the decision funds is not the unit the pack records), with the population a flag suggests (measured #5) at rung 2 |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #5 takes the population a flag or filter suggests · #3 stops at a close but inexact match |
| Calibration form | Gold-standard verification subsample: 60 platform-mornings counted by hand last autumn, each the peak 15-minute accumulation on one platform |
| Driving force | The crowding standard posts a conductor to a platform; the fare data counts entries at fare devices and the dashboard sums them per station complex. A platform's load is the entries of the fare arrays that feed it, through the station engineering map, plus the in-system transfers arriving from other lines, which no fare device records. At the twelve multi-line complexes the load piles onto one or two platforms, so platforms cross the threshold at complexes whose average never does, and even the best complex-level count misses a fifth of the shifts the pick needs. |

## 1. Situation

A city transit agency posts platform conductors on weekday mornings where crowding is forecast. Its crowding standard posts one to a
platform on each weekday morning when that platform's forecast peak 15-minute accumulation exceeds 85% of its rated capacity, and the
spring roster pick, which closes on 20 January, needs the weekly shift count. The pack holds fare-device entries by hour since 2022, the
complex-level ridership dashboard, the platform capacity register, the station engineering map of fare arrays to stairways and
platforms, last autumn's transfer census, the service-change register, and last autumn's hand counts. Hybrid work has left Mondays and
Fridays lighter than mid-week mornings.

## 2. Gate G: why this is legal

* **Litmus.** Every figure in the pack is correct: device entries, dashboard totals, capacities, the engineering map, the transfer
  census and the hand counts. No stakeholder's reading of their own numbers is overturned; the dashboard sums its complexes exactly.
  The difficulty is that the post the standard funds is a platform, and no file stores a platform's load.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and every voice. Device entries still aggregate most naturally to the complex, and the complex
  count still misses the platforms that carry the crowd.
* **Instrument repair.** Clean-data test. One file is suspect: the station register still flags Ferrier Street's two downtown platforms in
  service, superseded by the service-change register's closure for the whole pick. Repaired, with Ferrier Street's riders moved to Hollins
  Road and Marsh Gate, rung 0 returns 34 and rung 1 returns 47 (rung 2's figure), neither 58. Fare-device entries, the engineering map and
  the transfer census are complete and record entries and links, not platform loads, which no population file claims to hold; the hand
  counts are complete for the 60 mornings they cover and serve as the check. The platform build is still needed.
* **Lens swap.** The naive read and the answer count different populations: complexes whose averaged load crosses the line, against
  platforms whose own load does, which include platforms at complexes that never cross it.

## 3. The driving force

A strong solver forecasts each complex's weekday-morning peak by day type from recent eligible weeks, converts the peak hour to the peak
15 minutes, compares it with the complex's summed platform capacity, removes the platforms the service-change register closes, and
counts shifts. Every step is correct. But a conductor stands on a platform, and the load on a platform is not the complex's load shared
out. Each fare array feeds particular stairways, and the engineering map says which platform each serves; on top of the array entries
come riders changing lines inside the station, who pass no fare device and appear only in the transfer census. At the multi-line
complexes the morning load concentrates on the downtown platforms of one or two lines. Built per platform, 23 platforms need a conductor
on some weekday mornings, four of them at complexes whose own average stays under the threshold.

## 4. The ladder

| Rung | Construction | Lands on (shifts per week) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Complex peak from the dashboard's pooled weekday average, against summed platform capacity, over the platforms the station register flags in service | 30 (−48%) | The audited dashboard and the standard's threshold, applied station by station | The hand counts: Tuesday–Thursday mornings run 14% above the pooled weekday, Mondays and Fridays 19% below |
| 1 | Complex peak by day type (Monday, Tuesday–Thursday, Friday) | 41 (−29%) | Hybrid-aware and confirmed by the hand counts' day-type levels at single-platform stations | The service-change register closes Ferrier Street's two downtown platforms from 1 March to 30 June and routes their riders to Hollins Road and Marsh Gate, though the station register still flags them in service |
| 2 | Day-typed complex peaks over the platforms the register puts in service, with Ferrier Street's riders diverted | 47 (−19%) | The population is the one the register puts in service on the pick's dates, not the one the flag suggests | The hand counts at multi-line complexes: complex loads shared out reproduce only 29 of 60 counted platform-mornings |
| 3 | **Decisive:** platform loads built from array entries through the engineering map plus in-system transfers from the census, day-typed and over the platforms in service | **58** | — | — |

* **Figure shape.** Every wrong construction under-counts: complex grain misses platforms that carry a complex's load, pooling
  weekdays dilutes mid-week peaks, the flag misses the platforms Ferrier Street's diverted riders push over, and every rival platform
  split omits the transfers that land on downtown platforms. The answer is the maximum cell of the grid, and rungs 0–2 sit 48%, 29% and
  19% below it.
* **Partial correction priced (L3).** Splitting each complex's load evenly across its platforms lands at 44 (−24%), below rung 2. The
  array map without the transfers reproduces 46 of 60 hand counts, every miss low, and lands at 50 (−13.8%); splitting by each platform's
  share of train departures reproduces 38 of 60 and lands at 51 (−12.1%).
* **Grid.** Unit (complex, even split, departure share, array map, array map with transfers) × day types (pooled, typed) × population
  (flag, register) = 20 cells, every toggle pushing the count down, so errors stack rather than cancel. Every wrong cell sits at least
  12% below 58. The nearest is the departure-share split with everything else right (51, −12.1%), which needs a split that ignores the
  engineering map and the census together.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard names the platform as the post and says nothing about how a platform's load is built; no document
   joins the engineering map to the fare data or mentions transfers in relation to crowding.
2. **Reproduction (Pattern B).** The array map with transfers reproduces 60 of 60 hand counts within 3%; the best rival, the array map
   alone, 46 of 60, every miss low; the departure-share split 38 of 60; complex loads shared out 29 of 60. The rule is a construction, not
   a menu: it needs a device → array → stairway → platform chain and the census's line-pair flows, and no column anywhere carries a
   platform's load.
3. **No arithmetic symptom.** Device entries sum to the dashboard, platform capacities sum to the complex capacities, and the census
   reconciles to the agency's published transfer totals on every rung.
4. **Not a row predicate.** A platform's load is a sum over the arrays the map assigns it plus the transfers arriving on its lines, so it
   needs two joins and a group to the platform before any threshold applies.
5. **The enumeration is arithmetic.** Which platforms need conductors is computed; no file flags a platform as crowded.
6. **No cutover date in the decisive cause.** The Ferrier Street closure is dated and sits at rung 2. Platform concentration is a
   standing property of how each complex is built.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Last autumn's verification subsample: 60 platform-mornings (Monday to Friday) counted by hand, each the peak 15-minute
  accumulation on one platform, 44 of them at single-platform stations and 16 at multi-line complexes.
* **What it certifies.** The day-type levels, and the hour-to-15-minute peaking factor (0.31 at every platform), on the 44 single-platform
  stations, where complex and platform coincide.
* **What it pins.** The platform build: 60 of 60 under the array map with transfers, against 46, 38 and 29 for the rivals above.
* **Twin pair.** Ostrava Avenue and Wexley Junction are two-platform complexes identical on device entries by hour and day type, on
  capacity and on departures. Their busier platform's counted peak accumulation is 1,180 against 590 (2.0×): Wexley's arrays split
  evenly between its platforms and it carries few transfers, while Ostrava's main arrays feed the downtown stairways and 410 riders change
  onto that platform each peak quarter-hour.
* **Resemblance points at the decoy.** 44 of the 60 counts sit at single-platform stations, where the complex construction reproduces
  every one exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The crowding standard: a conductor is posted to a platform on each weekday morning when that platform's forecast peak
  15-minute accumulation exceeds 85% of its rated capacity. The capacity register gives each platform's rated capacity. The service-change
  register gives effective dates for closures. The pick runs from 2 March to 26 June.
* **Empirical pins.** The peaking factor and the platform build, from the hand counts. Day-type levels, from eligible autumn weeks.
* **Voices.** The planning analyst: "Complex entries are the only numbers we audit; platform splits are guesswork." The station
  operations chief: "Crowding lives at the downtown hubs; we know those stations." The union representative: "Conductors should go where
  the dashboard shows red."
* **Licensed wrong basis.** The standard's appendix records that the city's transit oversight committee monitors crowding at complex
  level from the published dashboard and will compare the pick against it.

## 8. Determinism by construction

* **Forecast window.** Every complex's day-typed autumn mornings are flat across the last 12 eligible weeks, so 8- and 12-week bases
  agree, and same-weeks-last-year growth is 1.00–1.04 everywhere under either window.
* **Threshold distance.** No platform's forecast peak sits within 3% of 85% of its capacity on any day type.
* **Transfers.** The census's line-pair flows scale with the arriving lines' entries under every reasonable scaling, because no platform's
  transfer share moves across the day types.
* **Closures.** Ferrier Street's closure spans the whole pick, so no part-season convention arises.
* **Holidays.** The standard excludes public holidays and the Christmas week from eligible weeks, and none falls inside the pick.

## 9. Prompt sketch and deliverables

> The spring pick closes on the 20th and I need one number for it: how many weekday-morning conductor shifts per week we fund at the
> stations. The analysts tell me the complex dashboard is the only count we audit. Give me the weekly shift count as a whole number, in a
> line I can put on the pick notice, and send `spring_pick.xlsx` with the build and the sheets below, a chart `platform_loads.png`, and a
> one-page `pick_note.pdf`.

* `spring_pick.xlsx` — the platform-level build and shift count, the fare-cap sheet (ask A) and the lift-outage sheet (ask B).
* `platform_loads.png` — for the twelve multi-line complexes, each platform's forecast Tuesday–Thursday peak quarter-hour as a share of its
  capacity, split into array entries and transfers, with the 85% line, the complex average marked on each group, and the four platforms
  that cross the line at under-threshold complexes annotated.
* `pick_note.pdf` — the committed count and how it differs from the dashboard view.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve busiest complexes and each autumn month, the share of weekday-morning
  entries that rode free under the weekly fare cap. *Device:* capped rides and free bus-to-rail transfers both post at zero fare, with
  different tap types, as the fare data guide documents; counting zero-fare taps conflates them at every complex. Entries count the same
  either way, so no platform load moves.
* **Ask B (device-carried).** For each of the twelve complexes, lift outage hours in each autumn month. *Device:* an outage ticket
  reopened after a failed repair keeps its ticket number with a new segment, as the maintenance guide documents; summing ticket spans
  double-counts the overlap at five complexes.
* **Ask C (validity).** The weekly shift count under each of the four rung constructions, and how many of the 60 hand counts each
  reproduces within 3%.
* **Decoupling.** Clearing the platform build changes no figure in asks A or B.

## 11. Rubric arithmetic

12 complexes × 3 months (ask A) + 12 × 3 (ask B) + 4 constructions × 2 (ask C) + the committed count, the platforms needing conductors
and the four platforms at under-threshold complexes + 5 named chart parts + 3 files ≈ 91 criteria.

## 12. World-building constraints

* 40 complexes in the study area, twelve of them multi-line. Shift counts: 30 / 41 / 47 / 58 across rungs 0–3; even split 44, array map
  without transfers 50, departure share 51, full build over the flagged population 49, full build on pooled weekdays 46.
* 23 platforms need conductors on some weekday mornings; four sit at complexes whose day-typed average stays under 85%.
* Hand counts: 60 platform-mornings, 44 at single-platform stations; reproduction 60 / 46 / 38 / 29 as above.
* With the station register repaired and Ferrier Street's riders moved, rung 0 gives 34 and rung 1 gives 47.
* Ferrier Street's two downtown platforms close from 1 March to 30 June; the station register's flag still reads in service. They sit
  below the threshold even when open, and their diverted riders push three platforms at Hollins Road and Marsh Gate over it on Tuesday to
  Thursday mornings.
* The twin complexes are identical on every device, capacity and departure column.
* Fare caps, zero-fare transfers and lift outages touch no entry count or platform load.
