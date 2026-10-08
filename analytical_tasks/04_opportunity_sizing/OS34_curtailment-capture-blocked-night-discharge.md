# OS34 — The year-one energy a storage programme delivers from curtailed solar, when the line that curtails the plants also blocks the batteries at night

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · electricity storage and grid congestion |
| Mirrors | Sizing what a buffer can absorb when the bottleneck that creates the surplus also blocks its release (CDN caches behind a saturated egress link, overflow storage served by the same congested dock doors, cloud burst capacity sharing a choked link with the workload it absorbs) |
| Decision shape | One figure committed at a date: year-one delivered energy from captured curtailment, filed in the lenders' base case at financial close on the 30th |
| Committed call | GWh delivered in year one by the programme's batteries from curtailed solar, to one decimal |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · Pattern C (serviceable share behind a join: a battery behind the congested path that curtails its plant cannot empty overnight), with E33 below it (the hybrid status flag against the amendments' effective dates) |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #10 notes a binding limit as a risk · #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another |
| Calibration form | Retry or revision log: the pilot battery's dispatch revision log, two years of daily charge and discharge schedules with every revision and its reason code |
| Driving force | The plants curtailed most are curtailed because the Kettle Pass line is full at midday, and on windy spring nights the same line is full all night. A battery behind it charges from curtailment, cannot discharge, starts the next day full and captures nothing. The pilot battery sits on an unconstrained line, so its log never shows a blocked night. Capture is a day-by-day state-of-charge recursion over the path's constraint log, reached through plant → path. |

## 1. Situation

A solar developer is adding a 100 MW / 400 MWh battery at each of its plants whose hybrid amendment is in force, to store curtailed
output and sell it later. The lenders' base case needs one figure at financial close on the 30th: year-one energy delivered from captured
curtailment. The company's pilot battery at another plant has two years of dispatch records. The CEO's view is that every curtailed
megawatt-hour is one the batteries can store.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the ISO's curtailment data, the plant register, the amendment file, the path constraint log and the
  pilot's revision log. The pilot battery really does hit its capture model. Nothing is overturned. The difficulty is a limit on emptying
  the battery that the pilot site never faced.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CEO's view and every voice. The pilot log still certifies a daily cycle that empties overnight, and nothing
  says a forward battery cannot.
* **Instrument repair.** Suspect file: the plant register's hybrid flag, which marks approval rather than an amendment in force. Repaired to
  effective dates, rung 0 becomes rung 1 (258.0 GWh), and rung 2 stays at 110.1. The constraint log and the pilot's revision log are
  complete, and the pilot's nights are unconstrained however well they are metered, so the blocked-night recursion is still needed for 63.7
  GWh.
* **Lens swap.** The answer runs on different days, the curtailment days that follow a blocked night at plants behind Kettle Pass, a
  population the pilot never contained.

## 3. The driving force

A strong solver scopes the programme to the plants whose amendments are in force in year one and simulates each battery against the
5-minute curtailment: charge from curtailment up to 100 MW until 400 MWh, discharge overnight, repeat. That is the textbook capture model,
it reproduces the pilot to 1% on 730 of 730 days, and it lands at 110 GWh. But three of the four batteries sit behind Kettle Pass, whose
midday congestion is why those plants are curtailed at all. The ISO's constraint log shows the same path binding from 21:00 to 05:00 on 58%
of their spring curtailment days, when wind fills it. On those nights a battery behind the path cannot export, so the next day it is still
full and captures nothing. Capture becomes a recursion in which today's room depends on last night's discharge, through a plant → path join
to a log no capture model opens.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last year's curtailment at all six plants × 86% round trip | 361.2 GWh, +467% | The register lists all six as approved hybrids, and curtailment is the opportunity | The amendment file: Corona Flats and Ewan Ridge take effect in month 13 |
| 1 | The four plants whose amendments are in force in year one, × 86% | 258.0 GWh, +305% | The right plants, on the governing dates | The batteries are 100 MW and 400 MWh, and spring curtailment runs to 1,100 MWh a day |
| 2 | Daily simulation: charge at up to 100 MW to 400 MWh, empty overnight, × 86% | 110.1 GWh, +72.8% | Reproduces the pilot to 1% on 730 of 730 days | The constraint log: Kettle Pass binds from 21:00 to 05:00 on 58% of those plants' curtailment days |
| 3 | **Decisive:** state of charge carried day to day, with no discharge on nights the plant's path binds | **63.7 GWh** | — | — |

* **Figure shape.** Every correction walks the figure down (−28.6%, −57.3%, −42.1%), and the answer is the minimum cell of the grid.
* **The deciding comparison.** The three Kettle Pass batteries charge 34, 33 and 31 GWh under rung 2 and 15.32, 14.88 and 13.87 under
  rung 3. Dry Lake, on an unconstrained line, stays at 30.00.
* **Partial correction priced (L3).** A solver who sees the congestion but applies the path's annual binding share (23% of hours) as a
  haircut lands at 90.7 GWh (+42%). Discharging in whatever night hours stay free changes nothing, because blocked nights bind for all of
  21:00 to 05:00, so that reading converges on the answer.
* **Grid.** Plants (six, four) × battery limits (none, power and energy) × nights (always empty, blocked by the path) = 8 cells. The
  nearest wrong cell is rung 2 at +72.8%. Even all six plants with the blocked-night rule give 115.3 GWh (+81%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The amendment file, the plant register and the battery specification say nothing about discharge. The constraint
   log is an ISO publication about transmission, and no document connects it to storage.
2. **Corpus blind for a computable reason.** *In every one of the pilot log's 730 days no discharge was revised for congestion, because the
   pilot plant exports on an unconstrained 500 kV path.* The daily-cycle model and the recursion return identical capture for every pilot
   day.
3. **No arithmetic symptom.** Curtailment, charging, discharge and losses balance every day under every rung, and state of charge never
   leaves 0–400 MWh.
4. **Not a row predicate.** Each day's room is the previous night's discharge, so capture is a recursion within each plant. Whether a night
   blocks comes from a different entity, the path, through a join.
5. **The enumeration is arithmetic.** No column marks a blocked night or a full battery. Both come out of the recursion over the constraint
   log.
6. **No cutover date.** The pattern is seasonal and repeats each spring; no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot's revision log: for each of 730 days, the scheduled charge and discharge, every revision, and the reason code
  (state-of-charge limit, telemetry fault, curtailment ended early).
* **What it certifies.** The 100 MW and 400 MWh limits, the 86% round trip, 97% availability, and charging from curtailment only. The
  rung-2 model reproduces 730 of 730 days within 1%.
* **What it is blind to.** Blocked nights (above).
* **The absolute split (O2).** On the forward plants' curtailment days, Kettle Pass either binds for all of 21:00 to 05:00 or for none of
  it. There is no partially blocked night.
* **Twin pair.** Weeks 15 and 17 at Kettle North are identical on every column of the curtailment report: daily curtailment within 1%,
  the same curtailed hours and the same irradiance. The battery captures 2,800 MWh in week 15 and 1,200 MWh in week 17, 2.3× apart, because
  four of week 17's nights were blocked. No rate per curtailed megawatt-hour reproduces both.
* **Resemblance points at the decoy.** The forward plants match the pilot on curtailment profile and battery size, so transferring the
  pilot's capture ratio by resemblance files rung 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The term sheet defines the base case as year-one energy delivered from curtailment captured by batteries at plants whose
  hybrid amendment is in force, on last year's 5-minute curtailment pattern. The battery specification fixes 100 MW and 400 MWh.
* **Empirical pins.** The round trip, availability and charging rule come from the pilot log. Blocked nights come from the ISO constraint
  log joined to each plant's path.
* **Voices.** The CEO: "Every curtailed megawatt-hour is one we can store." The pilot asset manager: "Our battery has hit its capture model
  every month for two years." That is true.
* **Licensed wrong basis.** The term sheet records that the lenders' independent engineer models capture on a daily cycle that empties
  overnight, and will review the base case on that basis.

## 8. Determinism by construction

* **Discharge window.** Blocked nights bind for all of 21:00 to 05:00 and open nights for none of it, so any discharge window inside
  18:00–08:00 gives the same blocked days.
* **Starting state.** There is no curtailment in January, so starting the year full or empty gives the same total.
* **Curtailment basis.** The term sheet pins last year's settlement-final 5-minute curtailment, so no forecast is chosen.
* **Simultaneous charge and congestion.** Charging behind the constraint reduces exports, so it is never blocked. Only discharge is.
* **Rounding.** Charged energy is 74.07 GWh (15.32, 14.88, 13.87 and 30.00), so the answer is 63.70 GWh, 0.05 from either one-decimal
  boundary, at the pilot's 86.0% round trip.

## 9. Prompt sketch and deliverables

> Financial close on the storage programme is on the 30th, and the lenders need one number: the energy our batteries deliver in year one
> from curtailed solar, in GWh to one decimal. Our CEO believes every curtailed megawatt-hour is one we can store. Send
> `capture_base_case.xlsx`, a chart `daily_capture.png`, and a one-page `lender_note.pdf`.

* `capture_base_case.xlsx`: the daily recursion per plant, the figure under the four rung bases, the availability sheet (ask A) and the
  instruction sheet (ask B).
* `daily_capture.png`: for one spring month at Kettle North and Dry Lake, daily curtailment, energy captured and end-of-night state of
  charge as paired panels, with blocked nights shaded and the 400 MWh line drawn.
* `lender_note.pdf`: the committed figure, the plant split, and the basis the independent engineer will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six plants, availability in each quarter of last year. *Device:* the outage log
  records full outages and partial derates as separate rows that can overlap. The outage guide converts overlapping rows to equivalent
  unavailable hours. Summing rows double-counts 140 hours at the two plants with inverter campaigns.
* **Ask B (device-carried).** For each plant, the number of curtailment instructions last year and their median duration. *Device:* the ISO
  revises an instruction by reissuing it under the same number with a higher revision, and cancels one by reissuing it at zero MW. Counting
  rows as instructions inflates the count by 37% and shortens durations at the Kettle Pass plants.
* **Ask C (validity).** The figure under each of the four rung bases, and the pilot reproduction under the daily cycle and the recursion
  (730 of 730 days for both).
* **Decoupling.** Clearing the blocked-night rule changes no figure in asks A or B.

## 11. Rubric arithmetic

6 plants × 4 quarters (ask A) + 6 × 2 (ask B) + 4 bases + 2 reproduction counts (ask C) + the committed figure, the four plants' charged
energy and the blocked-day counts for the three Kettle plants + 5 named chart parts + 3 files ≈ 58 criteria.

## 12. World-building constraints

* Last year's curtailment (GWh): Kettle North 96, Kettle South 88, Kettle West 81 (behind Kettle Pass), Dry Lake 35, Corona Flats 64 and
  Ewan Ridge 56 (amendments in force from month 13), 420 in total.
* Rung-2 charged energy: Kettle North 34, Kettle South 33, Kettle West 31, Dry Lake 30. Rung 3: 15.32, 14.88, 13.87 and 30.00. Corona Flats and
  Ewan Ridge would charge 31 and 29 on unconstrained lines.
* Rung figures are 361.2 / 258.0 / 110.1 / 63.7 GWh, and no other grid cell is within 70% of the answer.
* Kettle Pass binds all of 21:00–05:00 on 58% of the Kettle plants' curtailment days and on none of the pilot's. Kettle North's weeks
  15 and 17 are identical on every curtailment-report column.
* Derate overlaps and instruction revisions never touch curtailment, the constraint log or the pilot log.
