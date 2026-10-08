# AD19 — Which leak-alarm rule the train fleet adopts, when every candidate passes the repair log's headline test and only one matches the measured leaks

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · rail fleet maintenance |
| Mirrors | Adopting a fleet anomaly rule when several feature constructions pass the headline back-test and only one matches the repair measurements (predictive maintenance in airline fleets, delivery-van telematics in Amazon-scale fleets, cooling-plant compressors in data centres) |
| Decision shape | A structure the body adopts: the leak-alarm rule (feature, normalisation, which compressor-off periods count, threshold), judged by the engineering standard on reproducing the leaks measured at repair and kept within the depots' repair slots |
| Committed call | The rule the maintenance engineering board adopts on 12 November 2026, and its threshold in litres per minute of leak flow |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · finer controls separate constructions that a salient control cannot (E16), with a binding repair-slot limit applied in the threshold at the lower rung (E14) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #12 stops at the first control that passes · #10 notes a binding limit as a risk · #3 stops at a close but inexact match |
| Calibration form | Change-log natural experiments: 23 logged leak repairs, each with the ultrasonic leak flow measured before repair and the compressor record either side |
| Driving force | A leak shows as faster pressure decay while the compressor is off, and every candidate feature drops after every logged repair, the control everyone checks. But decay depends on the reservoir a leak drains, and while the compressor is off on a stopping service the doors also draw air. The ultrasonic flows recorded at repair are reproduced only by decay measured over off-periods with no door event, scaled by each unit's reservoir volume, and that rule alarms a different third of the fleet. |

## 1. Situation

A metro operator's 48 trains, 2-car and 3-car units across four lines, each carry an air-production unit whose compressor cycles on and
off. A leak shows as faster reservoir decay while the compressor is off. The maintenance engineering board adopts a fleet leak-alarm
rule on 12 November. The engineering standard says an alarm rule is adopted when it reproduces the leak flows measured at repair, and that
it must not raise more alarms than the depots can repair: three leak repairs a night, 21 a week. The pack carries the compressor and
pressure signals, the formation register with reservoir volumes, the door controller log, the depot plan, and the change log of repairs.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the pressure signals, the compressor states, the volumes, every door event and every ultrasonic
  measurement. The fleet engineer's decay rate is a true decay rate. Nothing reported is overturned; the difficulty is which construction
  of a leak from the signals reproduces the leaks the depots measured.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. Volume-normalised decay over every off-period still passes the headline control, matches 15 of 23
  measured flows, and alarms seven trains the answer does not.
* **Instrument repair.** Sample pressure ten times faster; the decay is already measured exactly. A better pressure instrument still mixes
  door draw into a stopping train's off-period.
* **Lens swap.** The naive feature uses every off-period; the answer uses only off-periods with no door event, a different population of
  segments, and scales them by a property of a different entity, the unit's reservoir.

## 3. The driving force

A strong solver segments the duty cycle, measures decay over off-periods, runs a CUSUM, sees the first week would raise 38 alarms against
21 slots and raises the threshold to fit, then notices 2-car units drain a smaller reservoir, converts decay to leak flow through each
unit's volume, and back-tests against the change log: every one of the 23 repairs shows its leak signal fall afterwards. Each step is
competent, and the salient control is passed. It is passed by every construction, because every one of them falls when a leak is fixed.
The finer controls in the same log are the ultrasonic flows measured before each repair and the residual after it. Volume-normalised decay
over every off-period reproduces 15 of the 23 flows: on the two stopping-service lines, off-periods span station stops, and opening doors
draws air that reads as leak. Excluding off-periods that contain any door event, which needs the door controller's log joined in time to
the segments, reproduces all 23 and leaves no residual after repair. With the threshold set to fill the 21 slots, that rule alarms seven
trains the volume rule does not.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | CUSUM on decay rate (bar/min) over every off-period, one fleet baseline, every exceedance alarmed | Fleet decay rule, 38 alarms in week one | The textbook duty-cycle feature and a robust baseline, the slots noted as a risk | The depot plan: three leak repairs a night, and the standard says alarms must not exceed the slots |
| 1 | The same feature, threshold raised until week one's alarms fill the 21 slots | Fleet decay rule at 0.031 bar/min (9 of its 21 alarms shared with the answer) | The limit applied in the rule, not merely noted | The formation register: 2-car units drain 400-litre reservoirs and 3-car units 600, so equal leaks decay 1.5× faster on 2-car units |
| 2 | Decay scaled by reservoir volume to leak flow, every off-period, threshold filling the slots | Volume rule at 7.9 L/min (14 of 21 shared) | Physical units, fair across formations, every repair's signal falls after it | The change log's ultrasonic flows: this rule reproduces 15 of 23, missing every repair on the two stopping-service lines |
| 3 | **Decisive:** leak flow over off-periods with no door event (door log joined in time), volume-scaled, threshold filling the slots | **Door-free volume rule at 6.4 L/min** | — | — |

* **What the structures change.** The decisive rule's threshold is 6.4 L/min, the volume rule's 7.9 (+23%); the decay rules are in bar per
  minute and share 9 of the answer's 21 week-one alarms; the volume rule shares 14.
* **Partial correction priced (L3).** A solver who excludes only off-periods that start at a station stop, not every period containing a door
  event, reproduces 19 of 23 and sets 7.1 L/min (+11%). A solver who keeps a separate threshold per formation instead of scaling by volume
  passes the headline control and reproduces 8 of 23.
* **Grid.** Feature (decay or flow) × off-periods (all, stop-start excluded, door-free) × threshold (unconstrained or slot-filling) gives
  twelve rules: every unconstrained rule breaches the slots; slot-filling flow rules set 7.9, 7.1 and 6.4 L/min. Only the door-free flow
  rule reproduces all 23 flows, and the nearest wrong rule (7.1) needs door events inside an off-period ignored.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard names the measured flows as the test; no document says doors draw air during an off-period, and the
   door log is a fault-diagnosis record.
2. **The corpus pins a construction, not a menu.** Door-free flow reproduces 23 of 23 measured flows within 5% and leaves a residual under
   0.3 L/min after every repair; the volume rule reproduces 15, overstating every stopping-service leak, and the decay rules 6 and 8. The
   rule is a construction: segments built from compressor states, intersected in time with a second log's events, scaled by a third file's
   volumes, and no column holds a leak flow.
3. **No arithmetic symptom.** Every candidate's signal falls after every repair; segments tie to compressor cycles and volumes to the
   register.
4. **Not a row predicate.** It needs off-period segments built from a state signal, a time-interval join to door events, a per-segment decay
   scaled by a unit property, and a per-train robust median over the week.
5. **The enumeration is arithmetic.** Which trains alarm is the slot-filling cut of a computed flow; no field marks a leak.
6. **No cutover date.** Leaks open at scattered dates on every line; no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The change log: 23 leak repairs over two years, each with the train, the repair date, the ultrasonic leak flow measured at 7 bar
  before repair, and the compressor and pressure record for the four weeks either side.
* **What it pins.** The salient control (signal falls after repair) is met by every rule. The finer controls are met only by door-free flow:
  23 of 23 flows within 5% and a post-repair residual under 0.3 L/min, against residuals of 1.6–2.4 L/min for rules that keep door draw.
* **Twin pair.** Repairs R-07 and R-16 sit on 3-car units with the same pre-repair decay (0.041 bar/min), compressor duty, mileage and
  formation. The depot measured 9.8 and 4.6 L/min (2.1×): R-16's train runs the stopping service, and door draw made up half its decay.
* **Every rule exercised.** Four repairs are on 2-car units, so volume scaling is tested; one unit was re-formed from 2-car to 3-car between
  two of its repairs, so the dated formation is tested.
* **Resemblance points at the decoy.** By decay profile, the fleet's highest-decay stopping-service trains most resemble R-07, the largest
  measured leak.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The engineering standard: an alarm rule is adopted when it reproduces the leak flows measured at repair, and it must not
  raise more alarms than the depots can repair. The depot plan: three leak repairs a night. The formation register's reservoir volumes.
* **Empirical pins.** The door-free segment definition and the volume scaling, from the change log.
* **Voices.** The fleet engineer: "Decay is decay; a leak is a leak on any unit." The maintenance planner: "Two-car units always look worse;
  give them their own threshold and be done."
* **Licensed wrong basis.** The standard records that the compressor maker's field engineer evaluates leak alarms on decay in bar per minute
  with one fleet threshold and will present that rule at the board.

## 8. Determinism by construction

* **Segments.** Every train has at least 40 door-free off-periods a day, so the weekly median is stable; medians over 30 to 60 periods agree
  within 0.1 L/min.
* **Slots.** The slot-filling threshold is the 21st-highest train's flow in week one; no two trains sit within 0.2 L/min of it.
* **Volume.** No unit was re-formed in the live window; the dated register settles the one re-formation in the change log.
* **Measurement.** Ultrasonic flows are all at 7 bar, the reservoir's working pressure, so no pressure correction is needed.

## 9. Prompt sketch and deliverables

> The fleet's leak-alarm rule goes to the maintenance engineering board on 12 November, and the depots can repair three leaks a night. Our
> fleet engineer thinks a leak is a leak on any unit. Tell me the rule we adopt and its threshold, in two sentences for the board, with
> `leak_rule.xlsx` holding the sheets below, the chart `decay_segments.png`, and `board_paper.docx`.

* `leak_rule.xlsx` — the rule build for all 48 trains, the wear sheet (ask A), the filter sheet (ask B) and the change-log back-test (ask C).
* `decay_segments.png` — one stopping-service train's day of pressure with off-periods shaded and door events marked, beside measured
  against predicted flows for the 23 repairs under the volume and door-free rules, the twin repairs labelled and the 6.4 L/min threshold
  drawn.
* `board_paper.docx` — the adopted rule, its threshold, and why the fleet decay rule and the volume rule are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight line-and-formation groups, brake-pad wear per 10,000 km over the last six
  months. *Device:* a wear reading that fails the gauge's validation is re-measured and both rows are kept, the second flagged as a
  re-measure, per the depot measurement guide. Averaging both rows misstates wear in the three groups with the most re-measures. The leak
  rule never reads brake wear.
* **Ask B (device-carried).** For each of the two depots, HVAC filter changes in each of the last six months. *Device:* a filter change done
  during a heavy-maintenance exam is logged under the exam's work order, not as a filter task, as the work-order guide documents. Counting
  filter tasks alone misses every exam month's changes.
* **Ask C (validity).** For each of the four rung rules, the measured flows it reproduces within 5% out of 23, and how many of its week-one
  alarms it shares with the answer.
* **Decoupling.** Clearing the door-free segmentation changes no figure in asks A or B.

## 11. Rubric arithmetic

8 groups × 2 halves of the period (ask A) + 2 depots × 6 months (ask B) + 4 rules × 2 (ask C) + the rule's feature, segments and scaling, its
threshold and its week-one alarms on 3-car units + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Week one at the slot-filling cut: fleet decay rule 0.031 bar/min (9 shared alarms), volume rule 7.9 L/min (14 shared), door-free rule 6.4
  L/min; unconstrained, the decay rule raises 38 alarms.
* Door draw adds 1.6–2.4 L/min of apparent leak on stopping-service trains; express-line trains rarely open doors in an off-period.
* Reservoirs: 2-car 400 litres, 3-car 600 litres; one re-formation in the change log, none in the live window.
* The change log holds 23 repairs; R-07 and R-16 are identical on every pre-repair signal column.
* Brake re-measures and exam-logged filter changes never touch the pressure signals, the door log or the change log.
