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
| Calibration form | Pilot log: last quarter's pilot of the window in two corridors, with every delivery's on-time flag and door wait, and the pilot report's headline and twelve published cells |
| Driving force | The dispatch standard holds 95% on time in every weekday-group × departure-bucket cell, at the customer's door rather than the depot gate. Four trip-level planning rules match the pilot's 95.3% headline. Per-cell road-time percentiles also match its twelve cell on-time rates, but only per-cell door-to-door percentiles, with each trip's gate dwell joined from the gate log, also reproduce the cells' door waits. Docklands, cheapest on road time, sits inside the port estate and queues about 40 minutes at the port gate every morning. Hillcrest's pooled percentile is set by one Friday school-run cell; planned per cell, through its own gate, it is the cheapest corridor. |

## 1. Situation

A grocery delivery company can launch its 30-minute delivery window in one corridor next quarter. The launch goes where holding the promise
costs the fewest van-minutes per delivery, because a van must leave early enough to arrive inside the window. Six corridors compete. The
company has a year of trip-level probe travel times, the traffic agency's daily corridor index, every depot's gate log, and the dispatch
standard. Last quarter it piloted the window in Ring Road North and Riverside. The pilot report gives a headline on-time rate and, for each
corridor × weekday group × departure bucket, an on-time rate and the mean minutes vans waited at the door for the window to open. The
operations director wants the launch where the pilot ran, since it is known to work there.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the probe times, the daily index, the gate
  log and every pilot figure. The pilot did work in both corridors. The difficulty is that the planning rule behind the pilot is written
  nowhere, four rules match its headline, two match its cell on-time rates, and they name different corridors.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. A trip-level 95th percentile per corridor still makes Docklands cheapest, its replay still
  matches the 95.3% headline, and the per-cell version still matches all twelve cell on-time rates.
* **Instrument repair.** Give every van perfect telemetry from gate to door. Docklands' port-gate queue is still 40 minutes, Hillcrest's
  Friday 07:00 cell still carries the school run, and a rule that matches only the headline or the on-time rates still names the wrong
  corridor.
* **Lens swap.** The naive rule plans for each corridor's pooled road trips. The answer plans for each weekday × bucket cell's door-to-door
  trips, a different population of departures that includes the gate.

## 3. The driving force

A strong solver drops the mean-plus-ten-minutes rule and moves from the agency's daily index to trip-level probe times, because the standard
says a promise is kept or broken delivery by delivery. It takes each corridor's 95th percentile and replays the pilot quarter. The replay
returns 95.3%, the published headline, and Docklands is cheapest at 55 minutes. The pilot's twelve cell on-time rates then fail the pooled
rule in eight cells, so the solver plans per cell, and the cell rates all match. Docklands is still cheapest, at 48 minutes. Each step is
competent and each control passes. But the pilot report also prints each cell's door wait, and per-cell road time misses six of the twelve.
Riverside's Friday 07:00 vans wait twice as long as its Tuesday–Thursday 07:00 vans on identical road times, because the Friday plan carries
an allowance for the parcel hub's queue at the shared gate. Only a planning time built per cell from road time plus the gate dwell, joined
from the gate log by vehicle and timestamp, reproduces all twelve cells. Under it Docklands, whose depot sits inside the port estate, costs
92 minutes. Hillcrest, whose pooled percentile was set by its Friday school-run cell and whose depot has its own gate, costs 58.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Mean travel time + 10 minutes, the current dispatch rule | A, Ring Road North (38 min) | The rule dispatch already uses, on a pilot corridor | The standard: 95% on time, and the mean-plus-ten rule replays the pilot at 81% |
| 1 | 95th percentile of the agency's daily corridor index | B, Motorway West (45 min) | A reliability percentile from an official series | The standard: a promise is kept or broken delivery by delivery, and Motorway West's trips vary within the day in ways its daily means hide |
| 2 | 95th percentile of trip-level probe times per corridor; the pilot replay matches the 95.3% headline | C, Docklands (55 min) | The right grain, and the pilot's own headline reproduced | The pilot report's twelve cells: pooled road time reproduces 4 of 12, with Riverside's Friday 07:00 replaying at 88.6% against the published 95.2% |
| 3 | **Decisive:** per weekday-group × bucket cell, the 95th percentile of road time plus that depot's gate dwell from the gate log; van-minutes as the delivery-weighted mean | **E, Hillcrest (58 min)** (4th of 6 on rung 0) | — | — |

* **Position table.** Hillcrest is 4th on rung 0 (52 min), 5th on rung 1 (62) and last on rung 2 (80). It leads only rung 3, 1.21× cheaper
  than Riverside (70). Rung margins: 1.24, 1.20, 1.20, 1.21.
* **Discriminator dominance.** Docklands carries a 1.45× cost advantage into rung 3 (55 against 80). The decisive construction moves
  Hillcrest by ×0.73 (its Friday tail no longer charged to every cell, and no gate) and Docklands by ×1.67 (the port gate), a relative swing
  of 2.31. Product: 2.31 / 1.45 = 1.59, Hillcrest's final advantage (58 against 92). The swing is 1.32× the 1.75 it needs (1.2 × the carried
  1.45).
* **Partial correction priced (L3).** Per-cell percentiles on road time alone match all twelve cell on-time rates and keep Docklands
  cheapest (48 against Hillcrest's 58, 1.21×). Door-to-door times pooled per corridor name Riverside (66, 1.21× under Hillcrest's and
  Ring Road North's 80 and 81). Each half of the construction lands on a wrong corridor, never on Hillcrest.
* **Grid.** Grain (day, trip) × stratification (pooled, per cell) × time (road, door to door) gives 6 feasible cells, since the daily index
  carries no gate. Day-grain cells name Motorway West pooled and per weekday group (45 and 47); trip-grain cells name Docklands (pooled
  road), Docklands (per-cell road), Riverside (pooled door to door) and Hillcrest (per-cell door to door). Both one-toggle neighbours of the
  answer are 1.21× clear: per-cell road time costs one omission (the gate log), pooled door-to-door costs the other (the cell grain).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "95% on time in every cell" and "at the customer's door". It does not say the gate counts toward
   travel time, and no document describes the pilot's planning rule.
2. **The reproducing rule is a construction, not a menu.** Per-cell door-to-door percentiles reproduce 12 of 12 cells (on-time rate and
   door wait) and the headline. The best rival, per-cell road time, reproduces 6 of 12; pooled door-to-door 5 and pooled road time 4. All
   four match the headline. The winning rule needs each calibration trip's gate dwell, joined from the gate log by vehicle and timestamp,
   before any percentile is taken, and no percentile or stratification scan on road time reaches it.
3. **No arithmetic symptom.** Trips, deliveries, the headline and every cell on-time rate reconcile under the per-cell road rule. The misses
   appear only in door waits, which nothing invites a solver to replay.
4. **Not a row predicate.** It needs a trip-to-gate join, a percentile inside each corridor × weekday × bucket group, and a
   delivery-weighted mean across cells.
5. **The enumeration is arithmetic.** No column carries a planning time, and the pilot log does not keep dispatch times.
6. **No cutover date.** The port-gate queue, the parcel hub's Friday queue and the school run recur every week, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: every pilot delivery in Ring Road North and Riverside with its window, weekday group, bucket, on-time flag and
  minutes waited at the door, plus the report's headline (95.3%) and its twelve cells (on-time 95.0–95.9%, with mean door waits).
  Dispatch times were set by the dispatch system and are not kept.
* **What it pins.** The per-cell door-to-door rule, through replay against the probe times and the gate log. The headline alone is matched
  by all four trip-grain rules, and the cell on-time rates by both per-cell rules.
* **Twin pair.** Riverside's Friday 07:00 cell and its Tuesday–Thursday 07:00 cell are identical on every visible column: 480 deliveries
  each, probe road-time median 33 and 95th percentile 44 minutes, and 95.2% on time. Their mean door waits are 9.6 and 4.8 minutes (2.0×).
  Only the Friday gate dwell separates them: the Friday plan allows for the parcel hub's queue, and the vans that miss the queue arrive
  early. Any road-time rule predicts the same wait for both.
* **Every rule exercised.** Ring Road North's depot shares an industrial-estate gate that queues on four of its six cells, and its Friday
  06:30 cell has no queue, which tests that the dwell is joined and not added flat. Riverside's gate queues only on Fridays, which tests the
  cell grain.
* **Resemblance points at the decoy.** On probe road times Docklands' cells look like Riverside's Tuesday–Thursday cells, which the pilot
  held at 95% with no gate allowance. Pooled, Hillcrest looks like Airport Spur, the costliest corridor.

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
* **Door waits.** The driver app logs the minutes between arrival and the window opening, and a van arriving inside the window logs zero, so
  the mean wait has one reading.
* **Cells.** Weekday groups (Monday, Tuesday–Thursday, Friday) and buckets (06:30, 07:00) are defined in the standard.
* **Rounding.** Van-minutes are filed to the nearest minute, and the final margin (58 against 70) exceeds any rounding.

## 9. Prompt sketch and deliverables

> Marketing can launch the 30-minute delivery window in one corridor next quarter. The ops director wants it where the pilot ran, since we
> know it works there. Tell me which corridor gets the launch and how many van-minutes per delivery it will take to keep the promise, to the
> nearest minute, in a sentence for the launch plan. Send `window_launch.xlsx`, a chart `planning_time.png`, and a one-page
> `launch_note.pdf`.

* `window_launch.xlsx` — the six corridors under each construction, the proof-of-delivery sheet (ask A), the reattempt sheet (ask B) and the
  replay sheet (ask C).
* `planning_time.png` — a heatmap of planning minutes by corridor × cell under the final rule, a strip of each corridor's delivery-weighted
  mean with the chosen corridor marked, and Docklands' morning port-gate queue and Hillcrest's Friday 07:00 cell annotated.
* `launch_note.pdf` — the committed corridor, its minutes, and why neither pilot corridor is it.

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

* Van-minutes per delivery (rungs 0–3): Ring Road North 38 / 58 / 70 / 77; Motorway West 47 / 45 / 68 / 76; Docklands 48 / 54 / 55 / 92;
  Riverside 55 / 60 / 66 / 70; Hillcrest 52 / 62 / 80 / 58; Airport Spur 60 / 66 / 78 / 84. Each corridor's day-grain percentile is at or
  below its trip-grain one.
* Per-cell road time: 66 / 66 / 48 / 63 / 58 / 75. Pooled door to door: 81 / 82 / 97 / 66 / 80 / 88. Day grain per weekday group:
  60 / 47 / 56 / 62 / 64 / 68.
* Docklands' port gate queues 35–50 minutes in every morning bucket. Hillcrest has a dedicated gate; its Friday 07:00 cell holds a sixth of
  its deliveries at a 98-minute percentile, and its other cells sit near 50. Riverside's Friday cells hold a third of its deliveries and add
  about 21 minutes of gate dwell at the percentile.
* The pilot replay: 12 of 12 for the winning rule, 6, 5 and 4 for the rivals; all four match the 95.3% headline, and both per-cell rules
  match every cell on-time rate. The twin cells are identical on every visible column and their door waits are 2.0× apart.
* Signature syncs and reattempt rows never touch trips, gate passages, door waits or pilot flags.
