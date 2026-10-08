# FC42 — How many ambulances the city needs on duty at the evening peak while St. Columba's is shut, when every crew's time at hospital is set by one receiving desk's pace

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · municipal emergency medical services administration |
| Mirrors | Capacity planning where a shared downstream server sets every upstream line's cycle time (Amazon linehaul trucks queued at a sort-centre dock, container trucks at a congested port gate, cloud jobs waiting on a shared database), where the server's speed was only ever measured below its capacity |
| Decision shape | One figure committed at a date: the evening deployment order for January to March |
| Committed call | Ambulances on duty at the evening peak on weekdays next quarter, as a whole number |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · a mixture, not a constant (one hospital desk sets the time at hospital of every post that drives there), with a field validated on one population and applied to another (measured #13) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #3 stops at a close but inexact match |
| Calibration form | Settled-transaction ledger: the county's paid ambulance-transport claims for the last two years, each carrying the receiving hospital's signed arrival and transfer-of-care times |
| Driving force | A crew's time at hospital is set by the receiving desk, not by its post or its patient. Riverside General hands over one ambulance every 12 minutes, first come first served, so its time at hospital is a queue fed by every post that drives there. At last year's 4.2 evening arrivals an hour the queue always cleared, and Riverside looked like the county's fastest desk at 14 minutes; with St. Columba's shut, 7.0 an hour arrive against a pace of 5, and the queue grows all evening. The pace shows only as exact 12-minute spacing between transfer-of-care times in the settled claims. |

## 1. Situation

A city EMS agency runs ambulances from nine posts into four emergency departments: Ashgrove Medical, Riverside General, St. Columba's
and Dunmore. St. Columba's department closes for a refit from January to March, and the county's destination rule sends each patient
to the nearest open department by the county routing matrix. The deployment standard sets the evening order at the 90th-percentile
weekday of the most ambulances busy at once in the evening's busiest hour, and the forecasting convention replays last year's same
quarter. The pack holds the dispatch system's incident and unit-status tables, the county's settled transport claims, the routing matrix,
the county's offload report by hospital and the destination rule. The deployment order is signed on 1 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: incident and status times, the settled claims, the drive times and the offload report, which
  really does rank Riverside fastest. No stakeholder's reading of their own numbers is overturned. The difficulty is what Riverside's desk
  does at a load it has never carried, which no record of the past shows directly.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operations chief's view and every voice. Replaying last year with each hospital's hourly mean time at
  hospital is still the natural build, it still reproduces every closed quarter within a unit, and it still lands at 28.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: the status table
  records every attachment (a unit re-assigned mid-call stays attached to both incidents, as the guide documents), the claims every
  transfer of care, the routing matrix every drive time. The deepest repair available, a status table with one row per unit and minute,
  makes rung 0 return 31 and rung 1 28 (rung 2's figure), neither 40, and the desk queue is still needed, because Riverside has never
  received seven ambulances an hour.
* **Lens swap.** The naive read and the answer describe different moments of the same desk: Riverside below its pace, where time at
  hospital is a stable 14 minutes, against Riverside above it, where time at hospital grows with every arrival since the afternoon.

## 3. The driving force

A strong solver replays last January to March from the unit-status table, re-drives St. Columba's transports to their new departments by
the routing matrix, gives each diverted transport the receiving hospital's hourly mean time at hospital rather than its own, counts
distinct units rather than unit-incident pairs, and reads the busiest evening hour's 90th-percentile weekday: 28 ambulances. It
back-tests the method on the previous year and lands within a unit. Every step is correct. But a crew's time at Riverside is not a
property of Riverside's average evening: the desk takes one handover every 12 minutes in arrival order, so each crew waits for every
crew ahead of it, whichever post sent them. Last year Riverside's evening arrivals averaged 4.2 an hour against a pace of 5, so queues
formed only in bursts and cleared within the hour. Next quarter the diverted transports bring 7.0 an hour from four in the afternoon, the
queue grows by two crews an hour, and on the 90th-percentile weekday eleven crews are at Riverside at once by half past seven. Built as a
first-come queue at the 12-minute pace the claims reveal, the evening needs 40 ambulances.

## 4. The ladder

| Rung | Construction | Lands on (ambulances) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last year's quarter replayed as recorded, St. Columba's transports re-driven by the routing matrix, each keeping its recorded time at hospital | 36 (−10%) | The forecasting convention applied to the letter, with the closure modelled | The county's offload report: time at hospital belongs to the receiving desk, and St. Columba's 38-minute mean is the county's slowest |
| 1 | Diverted transports take the receiving hospital's hourly mean time at hospital | 33 (−17.5%) | Calibrated by receiving desk, the subgroup the forward rows differ on | The dispatch data guide: a unit re-assigned mid-call stays attached to both incidents, so counting open unit-incident pairs counts it twice |
| 2 | Hygiene: distinct units busy each minute | 28 (−30%) | Clean, desk-calibrated, and the back-test on the previous year lands within a unit | The settled claims: at Riverside every transfer of care that follows a waiting crew comes exactly 12 minutes after the one before |
| 3 | **Decisive:** each department's desk built as a first-come queue at the pace its claims reveal (Riverside 12 minutes), fed by the replayed arrivals from every post | **40** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the order down (−10%, −17.5%, −30%) and the decisive rung reverses past rung 0, so a solver who
  stops anywhere short leaves the evening under-covered.
* **Partial correction priced (L3).** A solver who suspects congestion but scales Riverside's mean time at hospital by the load ratio
  (7.0 / 4.2) lands at 29 (−27.5%). One who sees the 5-an-hour pace but uses a steady-state queue, finds it undefined above the pace and
  caps each wait at the longest wait in the claims (52 minutes) lands at 33 (−17.5%).
* **Grid.** Diverted time at hospital (own recorded, receiving hourly mean, receiving desk as a queue) × count (unit-incident pairs,
  distinct units) = 6 cells: 36, 31; 33, 28; 45, 40. The nearest wrong cells are 36 (−10%) and the queue with unit-incident pairs at 45
  (+12.5%); reaching either takes dropping one whole correction.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The offload report gives each hospital's mean time at hospital; the hospitals' handover agreement sets a 30-minute
   target. No document says a desk hands over at a fixed pace, in arrival order, or that a mean belongs to a load.
2. **Reproduction (Pattern B).** A first-come queue at 12 minutes reproduces all 1,940 Riverside transfer-of-care times in the claims to
   the minute; an 11- or 13-minute pace misses all 212 queued handovers; hourly means reproduce none of the queued handovers and miss them
   by up to 40 minutes. The rule is a construction, not a menu: a recursion over each department's arrivals from every post, joined from the
   status table's at-hospital stamps to the claims' transfer-of-care times, and no sweep over constants reaches it.
3. **No arithmetic symptom.** Claims reconcile to transports, status stamps to incidents, drive times to the matrix, and every rung's
   replay reproduces the previous year within a unit.
4. **Not a row predicate.** A crew's wait depends on every crew that reached the same desk before it, so it needs an ordered recursion per
   department, not a filter or a group mean.
5. **The enumeration is arithmetic.** No column marks a handover as queued; queues are computed from arrival order and pace.
6. **No cutover date.** The closure lies in the future and steps nothing in the pack; Riverside's pace has been 12 minutes in every claim.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The county's settled transport claims for two years: every paid transport, its receiving hospital, and the hospital-signed
  arrival and transfer-of-care times the county requires before paying.
* **What it certifies.** Rungs 1 and 2: each hospital's hourly mean time at hospital, the 10-minute restock after every transfer of care,
  and a replay that reproduces each closed quarter's evening 90th percentile within a unit.
* **What it is blind to, and what it pins.** *In every closed evening Riverside's arrivals averaged under five an hour, so its queue
  cleared within the hour and its hourly mean described every evening;* the pace itself, 12 minutes in arrival order, is pinned by the
  212 queued handovers.
* **Twin pair.** Two weekday evenings at Riverside last February each brought six crews between 19:00 and 20:00, from the same posts with
  the same acuity mix. Their crews spent 147 and 297 ambulance-minutes at the hospital (2.0× apart), because one evening's six arrived
  eleven minutes apart and the other's within five minutes. Hourly means predict them equal; only the 12-minute queue reproduces both.
* **Resemblance points at the decoy.** The offload report ranks Riverside the county's fastest desk, and by drive time and acuity the
  diverted patients most resemble Riverside's own.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The deployment standard: the evening order covers the 90th-percentile weekday of the most ambulances busy at once in the
  evening's busiest hour. The forecasting convention: replay last year's same quarter with the quarter's known changes. The destination
  rule: each patient goes to the nearest open department by the county routing matrix.
* **Empirical pins.** Each department's handover pace and order, and the restock time, from the settled claims.
* **Voices.** The operations chief: "Riverside turns crews round faster than anyone; St. Columba's patients will clear quicker there than
  they ever did at home." The deployment planner: "We've staffed evenings on last year's busy units for six years and never been more than
  a unit out." The finance director: "Call volume is flat, so I don't see why the evening needs more."
* **Licensed wrong basis.** The county's EMS agreement records that the city's minimum evening deployment is reviewed against last year's
  90th-percentile busy units, and the county auditor will check the order on that basis.

## 8. Determinism by construction

* **Replay.** The convention fixes last year's January to March weekdays (63 evenings) and the county's call forecast is flat, so no
  volume scaling arises.
* **Routing.** No post's incidents sit within two minutes of a tie between two open departments in the matrix, so every diverted transport
  has one destination.
* **Pace and order.** Every queued handover at every department fits its integer pace in arrival order; restock is 10 minutes in every
  claim.
* **Peak hour.** 19:00–20:00 is the busiest weekday hour in all six grid cells.
* **Percentile.** The ordered evening maxima are flat around the 90th percentile (the 55th to 59th of 63 are all 40), so inclusive and
  exclusive definitions agree.

## 9. Prompt sketch and deliverables

> St. Columba's emergency department shuts for its refit from January to March, and its ambulance patients will go elsewhere. Our
> operations chief expects Riverside to absorb them without trouble. Tell me how many ambulances we need on duty at the evening peak next
> quarter, as a whole number, in one sentence for the deployment order, and send `evening_build.xlsx` with the build and the sheets below,
> a chart `riverside_evening.png`, and a one-page `deployment_note.html`.

* `evening_build.xlsx` — the replay under each construction, the response sheet (ask A) and the call-type sheet (ask B).
* `riverside_evening.png` — crews at Riverside minute by minute from 15:00 to 23:00 on the 90th-percentile weekday under hourly means and
  under the 12-minute queue, with arrivals as ticks along the axis, the 5-an-hour pace as a reference slope, and the peak hour shaded.
* `deployment_note.html` — the committed figure, what Riverside's desk does above its pace, and why last year's busy units understate it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine post districts and each month of last quarter, the share of priority-1
  calls reached within eight minutes. *Device:* the response standard counts the first medical unit on scene, and fire engines with
  paramedics log their arrival in the fire dispatch apparatus table, linked by incident number, as the EMS data guide documents; timing
  from the ambulance's on-scene stamp understates compliance in six districts. Response times enter no part of the busy-unit build.
* **Ask B (device-carried).** For each of the eight call types, last quarter's mean time on scene. *Device:* a call upgraded or
  downgraded after dispatch keeps its dispatch type in the incident table, with the final type in the call-type history table, as the
  dispatch data guide documents; grouping by the incident table misplaces 11% of calls. Call types enter no part of the busy-unit build.
* **Ask C (validity).** The evening requirement under each of the four rung constructions, and how many of the 212 queued Riverside
  handovers each construction reproduces to the minute.
* **Decoupling.** Clearing the desk queue changes no figure in asks A or B.

## 11. Rubric arithmetic

9 districts × 3 months (ask A) + 8 call types (ask B) + 4 constructions × 2 (ask C) + the committed figure and Riverside's forecast evening
arrival rate + 5 named chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Last year's weekday evenings (16:00–22:00): Riverside 4.2 arrivals an hour, never more than six in an hour; St. Columba's 3.1, of which
  the routing matrix sends 2.8 to Riverside and 0.3 to Dunmore. Next quarter Riverside receives 7.0 an hour against a 5-an-hour pace.
* Mean arrival to transfer of care: St. Columba's 38 minutes, Riverside 14; restock 10 minutes after every transfer of care.
* Requirement by rung: 36 / 33 / 28 / 40. Grid: own time with distinct units 31; queue with unit-incident pairs 45. Partials: scaled mean
  29, capped steady-state wait 33. Unit-incident pairs add five ambulances at the 90th-percentile peak hour under every construction.
* Claims: 1,940 Riverside transfers of care, 212 of them queued, each exactly 12 minutes after the previous one.
* The twin evenings are identical in hourly arrivals, posts and acuity; 147 and 297 ambulance-minutes at hospital.
* Fire apparatus times and call-type history touch no busy interval, claim or arrival used in the forecast.
