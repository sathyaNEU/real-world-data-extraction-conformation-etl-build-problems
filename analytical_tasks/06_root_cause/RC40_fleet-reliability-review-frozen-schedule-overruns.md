# RC40 — How much of the fleet's capacity-factor fall is reliability, when the worst of it sits inside refuelling outages that overran their frozen schedules

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · power-fleet maintenance and availability |
| Mirrors | Availability accounting for fleets with planned maintenance windows (data-centre maintenance at AWS and Google, heavy checks at Delta TechOps and Lufthansa Technik, refinery turnarounds), where the maintenance record files a whole outage as planned although the days past the frozen plan, and the days a failure forced it early, are unplanned |
| Decision shape | One figure committed at a date (a component): the reliability part of the year-on-year capacity-factor fall, which decides whether the risk committee commissions an independent review |
| Committed call | Commission the reliability review: losses attributable to reliability rose by 1.80 capacity-factor points between the two years, against the committee's 1.5-point line |
| Gap · Pattern | Gap 4 (rule) at the decisive rung, Gap 2 (population) at rung 2 · Pattern B (the parallel run's certified cells reproduce only when each refuelling run is split at its own frozen schedule), with the latent marker of measured #17 at rung 2 (derates matched to the grid operator's instructions) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #3 stops at a close but inexact match · #17 guesses an attribution the data can settle · #1 reports a failed back-test, ships anyway |
| Calibration form | Parallel-run overlap: the four quarters of the first year in which the plants' manual indicator classification, certified by their licensing engineers, ran beside the new automated loss accounting (72 certified cells) |
| Driving force | Every number is correct: the historian's generation, the event log, the grid operator's instructions, the outage register and the certified cells. The capacity factor fell six points mostly because four refuelling outages fell in the second year against three. Derates that match the grid operator's instructions to the minute and the megawatt take out another 1.40 points, and reliability looks up only 0.90, under the line. But the certified indicator splits every refuelling run at the schedule frozen 28 days before it: hours after the frozen end are overruns, and hours before the frozen start are a failure that forced the outage early. Only that split reproduces all 72 certified cells. The second year's outages overran by 2.09 points, the first year's 21-day forced early start now counts against the first year, and reliability losses rose 1.80. |

## 1. Situation

Penhallow Generation runs six nuclear units at three stations: Ravensholt R1 and R2 (1,150 MW each), Hawkcliffe H1 and H2 (1,250 MW) and
Westray W1 and W2 (900 MW). The fleet capacity factor fell from 93.0% to 87.0% between two years. The risk committee proposes an
independent reliability review costing several million, and its terms commission the review if unplanned capability loss rose by 1.5
points or more. The fleet is moving from the plants' manual indicator classification to automated loss accounting, and the two ran in
parallel for the four quarters of the first year. The reporting policy lets a classification be used only if it reproduces every
certified cell of that parallel run.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the historian's hourly generation, the event log's outage codes, the grid operator's
  instruction log, the outage register's schedules and the certified cells. The performance director is right that refuelling timing
  explains most of the fall, and the reliability part is quantified. No one's figures are overturned. The difficulty is which hours inside
  a refuelling outage were planned.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the committee's view and every voice. The parallel run still certifies the event-log rule on 56 of 72 cells and
  the grid marker on 68, and only the frozen-schedule split reaches 72.
* **Instrument repair.** Suspect: the plant's derate records leave the cause blank when the grid operator instructed the derate. Repair:
  fill the cause on every derate. Rung 0 still returns +5.99, and rung 1 falls to +0.90, the figure rung 2 reaches by matching instructions;
  none reaches +1.80. The event log is not suspect: it types every event correctly as a refuelling outage, forced outage or derate, a
  different attribute from planned capability loss, and the outage register's frozen schedules are complete. The split at the frozen
  schedule is a rule recovered by reproduction, which no row records, so it is still needed.
* **Lens swap.** The naive figure compares annual capacity factors. The answer counts a different set of lost hours: the overrun and
  forced-early hours inside runs the event log files as planned.

## 3. The driving force

A strong solver sets the headline aside, because the second year carried four refuelling outages against three, and it classifies losses
with the event log's codes. That leaves reliability up 2.30 points. It then sees that many second-year derates start in the same minute as
a set-point instruction in the grid operator's log and fall by exactly the instructed megawatts. Those are outside the plant's control, and
taking them out leaves reliability up 0.90, under the 1.5 line. The performance director looks vindicated. The parallel run disagrees in
four cells. Ravensholt R1's first-year outage was frozen at 22 days and ran 24, and the certified cells count the two extra days as
unplanned. Hawkcliffe H2 tripped 21 days before its frozen start and rolled straight into refuelling, and the certified cells count those
21 days as unplanned too. The event log files both as single refuelling events. Split at the frozen schedules, every second-year outage
overran, by 9 to 12.6 days, while the first year's forced early start, which the naive comparison filed as planned, now counts against the
first year and has no second-year counterpart. Reliability losses rose 1.80 points.

## 4. The ladder

| Rung | Construction | Lands on (change in reliability losses, capacity-factor points) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The capacity-factor fall read as reliability | +5.99 (+233%) | The committee's own metric and question | The outage register: four refuelling outages started in the second year against three in the first |
| 1 | Event-log codes: refuelling runs planned, forced outages and all derates unplanned | +2.30 (+28%) | The plants' own classification, applied to every hour | The grid operator's instruction log: 1.66 points of second-year derates begin in the minute of an instructed set-point and fall by its megawatts |
| 2 | The same, with derates matched to the grid operator's instructions moved outside management control | +0.90 (−50%) | Reproduces 68 of 72 certified cells and the fleet's outside-control total exactly | The parallel run: the four cells it misses are R1's and H2's outage quarters, and the certified figures put R1's two days past its frozen end and H2's 21 days before its frozen start in unplanned loss |
| 3 | **Decisive:** every refuelling run split at its schedule frozen 28 days before the start (hours before the frozen start and after the frozen end unplanned), with the grid marker kept | **+1.80** | — | — |

* **Figure shape.** The corrections walk the figure down from +5.99 to +0.90, and the decisive move reverses them to +1.80. Offsets from the
  answer are +4.19, +0.50 and −0.90. The reversal is the sum of two opposite parts: overruns up 1.99 points and forced early starts down
  1.09.
* **Partial correction priced (L3).** Rung 2 sits 0.90 from the answer. A solver who splits only at the frozen end lands at +2.89, 1.09 away,
  because the first year's early start stays planned. One who splits only at the frozen start lands at −0.19, 1.99 away. One who splits at
  the latest schedule revision finds that every revision moved the dates to the actual ones and lands back on +0.90. The best fixed rule, a
  cut that calls the last 24 days of each run planned, reproduces 70 of 72 cells and lands at +3.60, because every second-year outage was
  frozen longer than 24 days.
* **Grid.** Run split (none, end only, start only, frozen schedule) × grid marker (off, on) gives 8 cells. The nearest wrong cells are +2.30
  (27% away) and the start-only split without the marker at +1.21 (33% away). Every other cell is at least 50% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The outage procedure says each schedule is frozen 28 days before its planned start and that work added after the
   freeze is emergent. The certified cells carry figures and no method. No document says overrun or forced-early hours are unplanned loss.
2. **Reproduction numbers.** The frozen-schedule split reproduces 72 of 72 certified cells. The best rival, a last-24-days cut with the grid
   marker, reproduces 70, the grid marker alone 68 and the event-log rule 56. The split is a construction, not a menu: each outage's planned
   window comes from its own frozen version in the outage register, a join, and no fixed cut or offset reproduces both R1's two-day overrun
   and H2's 21-day early start.
3. **No arithmetic symptom.** Generation, event log, instructions and register reconcile on every rung, and each year's total loss is the
   same under every construction. Only its classification moves.
4. **Not a row predicate.** The event log holds each refuelling outage as one event. Its hours are classified by their position against a
   schedule version frozen on a date that differs for every outage.
5. **The enumeration is arithmetic.** No field marks an hour as an overrun. The split is computed from two timestamps per outage.
6. **No cutover date.** The overruns sit in four outages in different quarters, each measured against its own frozen dates.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The parallel run: for each of the six units in each quarter of the first year, the certified planned, unplanned and
  outside-control losses in megawatt-hours, 72 cells, beside the automated system's hourly classification.
* **What it certifies, and what it pins.** The grid marker (twelve cells in six instructed reactor-quarters move only when matched
  instructions go outside control) and the frozen-schedule split (four cells in two outage quarters).
* **The numbers.** 56, 68, 70 and 72 of 72 for the event-log rule, the grid marker, the best fixed cut and the split.
* **Twin pair.** R1's first quarter and R2's fourth quarter are identical on every column the event log and historian show: a 24-day run
  coded refuelling on a 1,150 MW unit, one two-day forced outage and no grid instructions. Their certified unplanned losses are 110.4 and
  55.2 GWh (2.0×), because R1's schedule was frozen at 22 days and R2's at 24.
* **Resemblance points at the decoy.** The second year's four outages look most like R2's first-year outage, one event coded refuelling and
  no instructions, which every construction reproduces to the megawatt-hour.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The reporting policy: "A loss classification may be used for indicator reporting, and for any decision taken on those
  indicators, only if it reproduces every certified cell of the parallel run." The committee's terms: "The independent reliability review
  is commissioned if unplanned capability loss rose by 1.5 points of capacity factor or more year on year." The outage procedure: "The
  schedule of record is frozen 28 days before the planned start; work added after the freeze is emergent."
* **Empirical pins.** The split and the grid marker come from the parallel run's 72 of 72. Every grid instruction matches a set-point change
  to the minute and the megawatt.
* **Voices.** Risk committee chair: "Six points is a reliability problem until someone shows me otherwise." Performance director: "This is
  just more refuelling outages landing in one year." Outage manager: "Every outage this year finished inside its window." Grid desk lead:
  "Half our derates this year were the grid operator's calls."
* **Licensed wrong basis.** The committee's terms record that it reads reliability on the event log's outage codes and will see this year's
  figure on that basis.

## 8. Determinism by construction

* **Energy.** Net generation is hourly from the historian, and reference energy is net capacity of record × hours. No unit changed capacity
  in either year.
* **Frozen schedules.** The register holds exactly one version per outage stamped 28 days before its planned start, and splits are exact to
  the hour. Power ascension finished inside the frozen window for every on-time outage and is counted with the overrun otherwise.
* **Grid marker.** Every instruction matches a set-point change in the same minute and megawatt, and no equipment derate begins in an
  instructed minute.
* **Years.** No outage straddles a year end, and no grid instruction falls inside an outage.
* **Maturity.** The second year is complete, every event closed before the extract, and the certified cells are final.

## 9. Prompt sketch and deliverables

> Our fleet capacity factor fell from 93.0% to 87.0%, and the risk committee wants an independent reliability review that will cost several
> million. Our performance director says it is just more refuelling outages landing in one year. Tell me in one sentence whether the review
> goes ahead, and give me the change in losses you attribute to reliability between the two years, in capacity-factor points to two
> decimals. Send `reliability_bridge.xlsx`, a chart `loss_bridge.png`, and a one-page `review_call.pdf`.

* `reliability_bridge.xlsx` — both years' losses by unit and category under every construction, the scram-rate sheet (ask A), the
  discharge sheet (ask B) and the parallel-run back-test (ask C).
* `loss_bridge.png` — a bridge from the first year's capacity factor to the second's with one bar per loss category, unplanned and
  outside-control categories in distinct colours, the overrun and early-start bars labelled with their outages, the 1.5-point review line
  on an inset of the unplanned change, and a title that states the call.
* `review_call.pdf` — the call, the reliability figure and its four parts.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Unplanned automatic scrams per 7,000 critical hours, for each unit in each year. *Device:* the
  indicator's denominator is hours critical, which the reactor-physics log records from criticality to shutdown, not hours on grid. Using
  grid hours overstates the rate by 4% to 9% at the units with long low-power physics testing after refuelling. Scram counts and critical
  hours never enter the loss classification.
* **Ask B (device-carried).** Fuel assemblies discharged at each of the seven refuelling outages. *Device:* the fuel-handling log records
  every move to the pool, and assemblies parked for one cycle and reinserted are not discharges as the fuel accountancy ledger defines them.
  Counting pool moves overstates discharges by about 15% at the two units that reinsert.
* **Ask C (validity).** For each of the 24 parallel-run reactor-quarters, your unplanned loss beside the certified figure.
* **Decoupling.** Clearing the frozen-schedule split or the grid marker changes no figure in asks A or B.

## 11. Rubric arithmetic

6 units × 2 years (ask A) + 7 outages (ask B) + 24 reactor-quarters (ask C) + the figure, the call, each year's unplanned loss and its four
parts (overruns, early starts, forced outages, equipment derates) + 5 named chart parts + 3 files ≈ 59 criteria.

## 12. World-building constraints

* Fleet net capacity is 6,600 MW. First-year losses are planned 3.44, early starts 1.09, overruns 0.10, forced outages 1.25, equipment
  derates 0.86 and instructed derates 0.26 points (93.0%). Second-year losses are 6.23, 0.00, 2.09, 1.85, 1.16 and 1.66 (87.0%).
* First-year outages: R1 frozen at 22 days, ran 24; H2 forced off 21 days before a 24-day frozen window; R2 frozen at 24, ran 24.
  Second-year outages: H1 frozen 34, overran 12; W1 30 and 9; R1 32 and 10; H2 35 and 12.6.
* Reliability losses are 3.30 and 5.10 points, a rise of 1.80. Every other grid cell sits at least 0.50 away.
* The parallel run holds grid instructions in six reactor-quarters and schedule departures only in R1's and H2's outage quarters. R1's first
  quarter and R2's fourth are identical on every event-log and historian column.
* Every revision after a freeze moved the schedule to the actual dates.
* Critical hours and fuel moves never touch generation, events, instructions or schedules.
