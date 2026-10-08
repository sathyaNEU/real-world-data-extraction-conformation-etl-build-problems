# DS37 — Whether the resurfacing books a nightly lane closure this season, when the detour can only take the traffic that may use it

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · highway work-zone operations |
| Mirrors | Scheduling capacity-reducing maintenance when the mitigation serves only part of the traffic (database maintenance with failover only for read traffic, warehouse line stoppages rerouted only for standard parcels, cloud-region maintenance where only stateless traffic can shift) |
| Decision shape | Hold, forced by a blocking quantity: book one of six nightly closure windows for eight weeks, or push the works to next season's weekend programme |
| Committed call | Book one named window or push the works, with the deciding figure: the best window's expected queue delay per night, in vehicle-hours |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern C, the detour serves only through traffic under the weight posting (a share set by re-identification and weigh-in-motion records), with a mixed heavy-vehicle class split through a join (E29) at rung 2 |
| Gate G mechanism | binding_constraint, with signal_vs_noise_or_hold |
| Measured traps engaged | #7 uses the ready-made measure · #6 treats a mixed segment all one way · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: six weeks in which the loop-detector station and a new radar counter both recorded the segment, including three nights of single-lane maintenance closures |
| Driving force | A signed detour removes only the traffic that can take it: trips that pass the whole segment, in vehicles under the arterial bridge's 26-tonne posting. At night, re-identification and weigh-in-motion records put that pool at 9% of demand, against the 20% the work-zone manual assumes. With the real pool, every allowed window queues past the policy's 600 vehicle-hours. |

## 1. Situation

A state DOT must resurface a three-lane urban freeway segment, which needs eight weeks of nightly closures of one lane. Its work-zone
mobility policy books a window only where expected queue delay, with the approved detour signed, stays at or under 600 vehicle-hours a
night; otherwise the works move to next season's weekend full-closure programme. Six start times on Sunday to Thursday nights are allowed.
The traffic-management plan signs a detour along a parallel arterial whose river bridge is posted at 26 tonnes. The planner favours the
quietest hour on the counter. The booking is due on Friday.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the loop station's three years of hourly counts, the radar overlap, the weigh-in-motion records,
  the re-identification reads and the work-zone manual's default diversion. No stakeholder read is overturned: the planner's hour is the
  quietest, and 20% is the manual's statewide figure. The difficulty is what share of this segment's night traffic the detour can serve.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the planner's preference and the manual's default. A queue model with any diversion a solver might assume
  still books a window; the pool still has to be built from two files to see that none qualifies.
* **Instrument repair.** Count every vehicle perfectly by class and speed. The pool is a property of trips and weights, not of counts, and
  the detour has never been signed at night here, so no better counter reveals how much traffic it would take.
* **Lens swap.** The naive read and the answer differ in population: all traffic times a statewide diversion rate, against the through
  trips under 26 tonnes that can actually leave the segment.

## 3. The driving force

A strong solver discards the average-volume shortcut, runs a deterministic queue over every historical night for each window, converts
heavy vehicles to passenger-car equivalents as the manual's capacity requires, and subtracts the manual's 20% diversion for a signed detour.
Sunday 21:00 comes in at 540 vehicle-hours and is booked. Every step is the manual's. But a detour serves only trips that pass the whole
segment, because traffic entering or leaving at the two interchanges inside it has nowhere to go, and only in vehicles the arterial bridge
can carry. The re-identification readers at the segment's ends give the through share by hour, 22% in the Sunday 21:00 window. The weigh-in-motion
station gives the share of those through vehicles under 26 tonnes, 41% then, when long-haul trucks dominate. The pool is 9%, the
traffic-management plan signs the detour as mandatory for exactly that pool, and with 9% removed instead of 20% the best window's expected
delay is 790 vehicle-hours.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Window with the lowest average hourly volume on the counter | Sunday 23:00 (980 vehicles an hour against 1,210 for the next) | The planner's measure, and the quietest hour by a clear margin | The mobility policy: windows are judged on expected queue delay per night, which a queue run over every night gives |
| 1 | Deterministic queue over every historical night in vehicles, with the manual's 20% diversion | Monday 22:00 (410 vehicle-hours, against 505 for the next) | The policy's measure on the full distribution of nights, under the cap | The work-zone manual: capacity is in passenger-car equivalents, with the counter's heavy class split by axle configuration into 1.5 and 2.5 |
| 2 | Hygiene of class: heavy vehicles split through the weigh-in-motion axle records and converted; 20% diversion | Sunday 21:00 (540, against 660 for the next) | Capacity measured the way the manual defines it, and a window still within the cap | The traffic-management plan's detour takes only through traffic under 26 tonnes; re-identification and weigh-in-motion put that pool at 9% at night |
| 3 | **Decisive:** diversion limited to the pool, hour by hour, from the through share and the weight split | **Push the works: the best window, Sunday 21:00, at 790 vehicle-hours** | — | — |

* **Position table.** Rung leaders are Sunday 23:00, Monday 22:00, Sunday 21:00, then the hold; no leader repeats. Margins: 1.23× on
  volume (1,210 against 980), 1.23× on delay (505 against 410) and 1.22× (660 against 540).
* **Blocking quantity.** With the pool as the diversion, the best window's expected delay is 790 vehicle-hours a night, 1.32× the cap;
  every other window is at 905 or more. The hold is falsifiable: had the night pool reached 15%, Sunday 21:00 would have come in at 590
  and been booked.
* **Discriminator dominance.** Sunday 21:00 carries a 1.11× clearance into rung 3 (600 against 540). Cutting diversion from 20% to 9%
  multiplies its delay by 1.46× (790 against 540), more than the 1.11 clearance times the 1.20 floor (1.33), so it lands 1.32× over.
* **Partial correction priced (L3).** Limiting diversion to the through share alone, forgetting the weight posting, gives 22% and books
  Sunday 21:00 at 525. Limiting it to vehicles under 26 tonnes alone gives 41% and books it at 470. Applying the 9% pool to cars and the
  counter's heavy class without the axle split finds Sunday 21:00 at 700, a hold on a figure 11.4% low. Half the construction books a
  window.
* **Grid.** Measure (average volume, queue) × capacity unit (vehicles, PCE by axle class) × diversion (20%, through only, weight only,
  pool) = 16 cells. Twelve book a window; the hold appears only with the queue and the pool, at 700 without the axle split and 790 with
  it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan signs the detour and the bridge carries a posting; the manual gives a default diversion. No document says
   the default does not apply here, or how large the eligible pool is.
2. **Corpus blind for a computable reason.** *On all three overlap nights with a lane closed, no detour was signed, so diversion is zero
   in every closure the overlap holds, and every diversion assumption reproduces it identically.* The overlap certifies the queue model
   with PCE demand: measured delay on those nights matches it within 3%, and the vehicle-count model misses by 21%.
3. **No arithmetic symptom.** Loop and radar volumes agree, PCE demand reconciles to class counts, and every window's delay is positive and
   plausible under every diversion.
4. **Not a row predicate.** The pool needs re-identification matches across the segment's two ends, by hour, crossed with the weight
   distribution of matched through vehicles, then fed through a queue run for every historical night.
5. **The enumeration is arithmetic.** No column marks a trip as through or a vehicle as eligible; both come from matching and weights.
6. **No cutover date.** The answer rests on trip structure and weights, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without the manual's default, any assumed diversion still books a window.

## 6. The calibration corpus

* **Form.** Six spring weeks in which the loop station and a new radar counter both recorded the segment by hour and class, including
  three nights with one lane closed for maintenance, with radar speeds giving measured delay.
* **What it certifies.** Volumes (the two sources agree within 1% on every hour), and the queue model with PCE demand by axle class (within
  3% on all three closure nights).
* **What it is blind to.** Diversion (above).
* **Twin pair.** Monday 22:00 and Wednesday 22:00 are identical on every counter column: volume, heavy share, PCE demand and unmitigated
  expected delay. Their delay with the pool as diversion is 905 and 1,810 vehicle-hours (2.0×): Monday's late traffic still carries
  commuters passing through in cars, Wednesday's is mostly deliveries to the riverside depots inside the segment, pools of 6% and 2%.
  Only the re-identification join separates them.
* **Resemblance points at the decoy.** Sunday 21:00 most resembles last year's Sunday closure on the adjacent segment, which stayed within
  the cap with a signed detour; that segment's night through share was 58%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The mobility policy: a window is booked only where expected queue delay with the detour signed stays at or under 600
  vehicle-hours a night; otherwise the works move to next season's weekend programme. The work-zone manual: work-zone capacity 2,900
  passenger-car equivalents an hour with one lane closed; equivalents of 1.5 and 2.5 by axle class. The traffic-management plan: the detour
  is signed as mandatory for through traffic within the bridge posting. The bridge posting: 26 tonnes.
* **Empirical pins.** The through share and weight split by hour, from the readers and the weigh-in-motion station.
* **Voices.** The planner: "The quietest hour on the counter is the safest bet." The traffic-management engineer: "A signed detour always
  takes a fifth of the traffic." The contractor: "We can be in and out by 05:00 any night you give us."
* **Licensed wrong basis.** The policy records that the regional operations centre reviews bookings on average hourly volume and will see
  that table.

## 8. Determinism by construction

* **Queue.** Deterministic, starting at the window's start and clearing at full capacity afterwards, per the manual; every historical
  night is run, holidays excluded as the manual lists them.
* **Re-identification.** A through trip is a read at both ends within 15 minutes; every matched trip falls within 4 to 9 minutes, so match
  windows from 10 to 20 minutes give the same share.
* **Weights.** No through vehicle's weigh-in-motion gross weight sits within 0.5 tonnes of 26, so the posting splits them unambiguously.
* **Margins.** Every window's pool-limited delay is at least 31% over 600, so no capacity or equivalence convention within the manual's
  range books one.

## 9. Prompt sketch and deliverables

> The resurfacing needs eight weeks of nightly lane closures, and I have to book a window with the state by Friday or tell them we're
> pushing the job to next season's weekend programme. The planner favours the quietest hour on the counter. Give me the window, or tell
> me to push it, in one sentence for the booking form, with the expected delay that decides it in vehicle-hours a night. Send
> `closure_windows.xlsx`, a chart `night_delay_by_window.png`, and a one-page `booking_decision.pdf`.

* `closure_windows.xlsx` — the six windows under each rung basis (ask C), the crash sheet (ask A) and the speed sheet (ask B).
* `night_delay_by_window.png` — expected delay for the six windows under the manual's 20% and under the pool, as paired bars, with the
  600 line labelled, the 790 annotated, and each window's pool share printed on its bar.
* `booking_decision.pdf` — the committed call, the blocking quantity and what would have made a window bookable.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of the last year, crashes on the segment and the share at night. *Device:* the
  state re-referenced its mileposts after the interchange rebuild, and the reference crosswalk maps old posts to new. Filtering crashes by
  the new milepost range drops the first five months' crashes recorded on the old posts and picks up some from the next segment.
* **Ask B (device-carried).** For each month, the share of evening-peak hours with average speed under 45 mph. *Device:* the station
  leaves speed blank for intervals with fewer than ten vehicles, as its guide documents; reading blanks as zeros puts slow hours in
  quiet nights that never had them.
* **Ask C (validity).** Each of the six windows' expected delay under each of the four rung bases, and the night pool share by start hour.
* **Decoupling.** Clearing the pool changes no figure in asks A or B. Crash records and speed blanks touch no volume, class, read or
  weight record.

## 11. Rubric arithmetic

12 months × 2 (ask A) + 12 months (ask B) + 6 windows × 4 bases + 6 pool shares (ask C) + the hold, the blocking quantity, its distance
from the cap and the falsifier + 5 named chart parts + 3 files ≈ 78 criteria.

## 12. World-building constraints

* Rung leaders: Sunday 23:00 (980 vehicles an hour), Monday 22:00 (410 vehicle-hours), Sunday 21:00 (540), then the hold at 790. Every
  other window under the pool is at 905 or more.
* In the Sunday 21:00 window the through share is 22% and the under-26-tonne share among through vehicles 41%: pool 9%. Monday and
  Wednesday 22:00 match on every counter column, with pools of 6% and 2%.
* The overlap holds three closure nights, none with a detour signed. The adjacent segment's through share was 58%.
* Milepost re-referencing and speed blanks are independent of every main-call record.
