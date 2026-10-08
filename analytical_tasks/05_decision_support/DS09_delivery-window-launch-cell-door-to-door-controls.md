# DS09 — Which corridor gets the 30-minute delivery window, when the pilot's headline is matched by four constructions and its cells by one

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · last-mile delivery operations |
| Mirrors | Promise-time products whose reliability standard is held cell by cell and door to door (Amazon and Instacart delivery windows, Uber Eats and DoorDash arrival promises, Google Maps fleet ETAs) |
| Decision shape | Which of N gets one scarce thing: the single corridor launch of the 30-minute delivery window next quarter |
| Committed call | The corridor that gets the launch, and the van-minutes per delivery needed to hold the promise, to the nearest minute |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · measured #12's architecture (finer controls separate constructions that all pass the headline), with two grains of travel time (day against trip) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #12 stops at the first control that passes · #14 coarsens the segment it was asked about · #18 joins only on the visible key · #15 follows the requester's hunch over the rule |
| Calibration form | Pilot log: last quarter's pilot of the window in two corridors, with the pilot report's headline on-time rate and its twelve published cell rates |
| Driving force | The dispatch standard holds 95% on time in every weekday-group × departure-bucket cell, and a promise is kept at the customer's door, not at the depot gate. The pilot's headline (95.3%) is reproduced by all four trip-level planning-time constructions, and they name three different corridors. Its twelve cells are reproduced only by per-cell 95th percentiles of road time plus the depot's own gate dwell, reached through the gate log. Docklands, the cheapest corridor on road time, queues 25 minutes at its gate on Monday mornings. Hillcrest has a dedicated gate and flat cells. |

## 1. Situation

A grocery delivery company can launch its 30-minute delivery window in one corridor next quarter. The launch goes where holding the promise
costs the fewest van-minutes per delivery, because a van must leave early enough to arrive inside the window. Six corridors compete. The
company has a year of trip-level probe travel times, the traffic agency's daily corridor index, every depot's gate log, and the dispatch
standard. Last quarter it piloted the window in Docklands and Riverside. The pilot report gives a headline on-time rate and a rate for each
corridor × weekday group × departure bucket. The operations director wants the launch where the pilot ran, since it is known to work there.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the probe times, the daily index, the gate
  log and both pilot figures. The pilot did work in Docklands. The difficulty is that the planning-time rule behind the pilot is written
  nowhere, four rules match its headline, and they name different corridors.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. A trip-level 95th percentile per corridor still makes Docklands cheapest, and its pilot
  replay still matches the 95.3% headline.
* **Instrument repair.** Give every van perfect telemetry from gate to door. Docklands' Monday gate queue is still 25 minutes. A cheaper
  plan still fails the standard's cells, and a rule that matches only the headline still names the wrong corridor.
* **Lens swap.** The naive rule plans for each corridor's pooled road trips. The answer plans for each weekday × bucket cell's door-to-door
  trips, a different population of departures that includes the gate.

## 3. The driving force

A strong solver drops the mean-plus-ten-minutes rule and moves from the agency's daily index to trip-level probe times, because the standard
says a promise is kept or broken delivery by delivery. It takes each corridor's 95th percentile and replays the pilot quarter. The replay
returns 95.3%, the published headline, and Docklands is cheapest at 55 minutes. Each step is competent, and the headline check passes. But
the pilot report also prints twelve cell rates, and the pooled rule misses eight of them. Docklands' Monday 07:00 cell lands at 88.1%,
because its depot gate queues 25 minutes on Monday mornings and probe road time never sees the gate. Only a planning time built per cell,
from road time plus the gate dwell joined from the gate log by vehicle and timestamp, reproduces all twelve. Under that rule Docklands costs
75 minutes, and Hillcrest, whose depot has its own gate and whose cells are flat, costs 60.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Mean travel time + 10 minutes, the current dispatch rule | A, Ring Road North (38 min) | The rule dispatch already uses | The standard: 95% on time, and the mean-plus-ten rule replays the pilot at 81% |
| 1 | 95th percentile of the agency's daily corridor index | B, Motorway West (45 min) | A reliability percentile from an official series | The standard: a promise is kept or broken delivery by delivery, and Motorway West's trips vary within the day in ways its daily means hide |
| 2 | 95th percentile of trip-level probe times per corridor; the pilot replay matches the 95.3% headline | C, Docklands (55 min) | The right grain, and the pilot's own figure reproduced | The pilot report's twelve cells: this rule reproduces 4 of 12, with Docklands' Monday 07:00 at 88.1% against the published 95.4% |
| 3 | **Decisive:** per weekday-group × bucket cell, the 95th percentile of road time plus that depot's gate dwell from the gate log; van-minutes as the delivery-weighted mean | **E, Hillcrest (60 min)** (4th of 6 on rung 0) | — | — |

* **Position table.** Hillcrest is 4th on rung 0 (52 min), 4th on rung 1 (59) and 2nd on rung 2 (67, 1.22× Docklands' 55). It leads only rung
  3, 1.22× cheaper than Riverside (73). Rung margins: 1.24, 1.20, 1.22, 1.22.
* **Discriminator dominance.** Docklands carries a 1.22× cost advantage into rung 3 (55 against 67). The decisive construction moves
  Hillcrest by ×0.90 (flat cells, no queue) and Docklands by ×1.36 (Monday queue), a relative swing of 1.52. Product: 1.52 / 1.22 = 1.25,
  Hillcrest's final advantage (60 against 75).
* **Partial correction priced (L3).** Per-cell percentiles on road time alone keep Docklands cheapest (53 against 57) and reproduce 7 of 12
  cells. Door-to-door times pooled per corridor name Riverside (64 against 69). Each half of the construction lands on a different wrong
  corridor.
* **Grid.** Grain (day, trip) × stratification (pooled, per cell) × time (road, door to door) gives 6 feasible cells, since the daily index
  carries no gate. They name B, C, C, D, B and E. The nearest wrong cell is per-cell road time (Docklands, 1.08× clear), and it costs one
  omission: the gate log.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "95% on time in every cell" and "at the customer's door". It does not say the gate counts toward
   travel time, and no document describes the pilot's planning rule.
2. **The reproducing rule is a construction, not a menu.** Per-cell door-to-door percentiles reproduce 12 of 12 cells and the headline. The
   best rival, per-cell road time, reproduces 7 of 12. Pooled road time and pooled door-to-door reproduce the headline and 4 or 5 cells. The
   winning rule needs each calibration trip's gate dwell, joined from the gate log by vehicle and timestamp, before any percentile is taken.
   No parameter scan reaches it.
3. **No arithmetic symptom.** Trips, deliveries and the headline reconcile under every rule. The misses appear only in cells that nothing
   invites a solver to replay.
4. **Not a row predicate.** It needs a trip-to-gate join, a percentile inside each corridor × weekday × bucket group, and a
   delivery-weighted mean across cells.
5. **The enumeration is arithmetic.** No column carries a planning time, and the pilot log does not keep dispatch times.
6. **No cutover date.** The Monday queue recurs every week, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: every pilot delivery in Docklands and Riverside with its window, weekday group, bucket and on-time flag, plus the
  report's headline (95.3%) and its twelve cell rates (95.0–95.9%). Dispatch times were set by the dispatch system and are not kept.
* **What it pins.** The per-cell door-to-door rule, through replay against the probe times and gate log. The headline alone is matched by
  all four trip-grain rules.
* **Twin pair.** Docklands' Tuesday–Thursday 07:00 cell and Riverside's Monday 07:00 cell are identical on every visible column: 412
  deliveries each, the same probe road-time median (31 min) and 95th percentile (41 min). Their late deliveries are 20 and 10 (2.0×). Only
  Docklands' gate dwell separates them, so any road-time rule predicts the same lateness for both.
* **Every rule exercised.** Riverside's depot shares a gate with a parcel hub, queuing only on Fridays, which tests the cell grain. One
  Docklands cell has no queue, which tests that the dwell is joined and not added flat.
* **Resemblance points at the decoy.** Docklands is a pilot corridor with every cell at or above 95%, the profile a lookup would carry
  forward.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The launch brief: the window goes to the corridor where holding it costs the fewest van-minutes per delivery. The dispatch
  standard: 95% on time in every weekday-group × departure-bucket cell, and a promise is kept or broken at the customer's door, delivery by
  delivery. The calibration window is the last full year. One sentence each.
* **Empirical pins.** The per-cell door-to-door rule, from the pilot cells.
* **Voices.** The operations director: "Launch where the pilot ran; we know it works there." The dispatch lead: "Mean plus ten has served us
  for years." The marketing lead: "Motorway West is the corridor customers ask about."
* **Licensed wrong basis.** The launch brief records that the regional board reads corridor cases on the agency's daily reliability index and
  will see that basis.

## 8. Determinism by construction

* **Percentiles.** Every cell holds at least 1,500 calibration trips, so interpolation conventions move a cell's percentile by under 0.2
  minutes.
* **Gate dwell.** The gate log stamps queue entry and exit per vehicle, and every trip joins to exactly one gate passage.
* **Cells.** Weekday groups (Monday, Tuesday–Thursday, Friday) and buckets (06:30, 07:00) are defined in the standard.
* **Rounding.** Van-minutes are filed to the nearest minute, and the final margin (60 against 73) exceeds any rounding.

## 9. Prompt sketch and deliverables

> Marketing can launch the 30-minute delivery window in one corridor next quarter. The ops director wants it where the pilot ran, since we
> know it works there. Tell me which corridor gets the launch and how many van-minutes per delivery it will take to keep the promise, to the
> nearest minute, in a sentence for the launch plan. Send `window_launch.xlsx`, a chart `planning_time.png`, and a one-page
> `launch_note.pdf`.

* `window_launch.xlsx` — the six corridors under each construction, the proof-of-delivery sheet (ask A), the reattempt sheet (ask B) and the
  replay sheet (ask C).
* `planning_time.png` — a heatmap of planning minutes by corridor × cell under the final rule, a strip of each corridor's delivery-weighted
  mean with the chosen corridor marked, and Docklands' Monday 07:00 gate queue annotated.
* `launch_note.pdf` — the committed corridor, its minutes, and why the pilot corridor is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each corridor, last quarter's share of deliveries signed for in person. *Device:* when the
  driver app syncs offline, it back-fills the signature field on photo-only drops and marks the record `offline_sync`, as the
  proof-of-delivery dictionary documents. Counting those as signed inflates three corridors by 5–8 points.
* **Ask B (device-carried).** For each corridor and weekday group, failed first attempts per 1,000 orders. *Device:* a reattempt is logged
  as a new delivery row carrying the original order ID. Counting rows instead of orders double-counts every failure.
* **Ask C (validity).** The twelve pilot cells and the headline under each of the four trip-grain rules (hits of twelve), and the six
  corridors' van-minutes under each rung.
* **Decoupling.** Clearing the gate join and the cell grain changes no figure in asks A or B. Signatures and reattempts never enter a
  planning time.

## 11. Rubric arithmetic

6 corridors (ask A) + 6 × 3 weekday groups (ask B) + 4 rules × 2 (cell hits, headline) + 6 × 4 rung values (ask C) + the committed
corridor, its minutes and the runner-up + 6 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* Van-minutes per delivery (rungs 0–3): Ring Road North 38 / 58 / 70 / 74; Motorway West 47 / 45 / 68 / 77; Docklands 48 / 54 / 55 / 75;
  Riverside 55 / 60 / 68 / 73; Hillcrest 52 / 59 / 67 / 60; Airport Spur 60 / 66 / 78 / 84. Each corridor's day-grain percentile is at or
  below its trip-grain one.
* Docklands' gate queues 25 minutes in Monday 07:00 departures and 12 in Tuesday–Thursday 07:00. Hillcrest has a dedicated gate. Per-cell
  road time gives Docklands 53 and Hillcrest 57, and pooled door-to-door gives Riverside 64 and Hillcrest 69.
* The pilot replay: 12 of 12 for the winning rule, 7, 5 and 4 for the rivals; all four match the 95.3% headline. The twin cells are
  identical on every visible column.
* Signature syncs and reattempt rows never touch trips, gate passages or pilot flags.
