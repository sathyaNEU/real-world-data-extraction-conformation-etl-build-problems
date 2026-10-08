# RC09 — Which air-handler repair programme the estates budget buys this winter, or none, when closed repairs come back where no screen looks

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · university estates and facilities management |
| Mirrors | Fix-programme sizing for fleets of connected equipment (data-centre cooling units, fulfilment-centre conveyors, Apple and Cisco field-repair programmes), where repairs closed in the ticketing system recur silently inside an alert-suppression window |
| Decision shape | Hold, forced by a blocking quantity: fund one repair programme across the estate, or none this winter |
| Committed call | No programme this winter, with the blocking figure: the only programme that clears the saving floor pays back in 4.4 years against the policy's three |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S2 (a residual population between two correct records: repairs closed in the order system whose faults are back, suppressed from the alarm stream), with E15 (the quiet second trap) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #9 picks from the offered options when none passes · #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: the estate's 212 closed air-handler repairs over three winters, each with its measured saving |
| Driving force | The fault-detection system suppresses alarms on a unit for 90 days after a work order closes, and the order system shows the repair done. Units whose fault came back inside that window sit in neither stream. Among this winter's variable-speed-drive repairs, 9 of 17 came back. That shows only when the detection rules are rerun on the raw trends of suppressed units, and it cuts the drive programme's durable saving by more than half. |

## 1. Situation

A university's estates department runs 40 air-handling units across 12 buildings, and heating and ventilation energy rose sharply this winter. The
maintenance contractor blames economiser dampers, which alarm every week on the fault-detection screen. The estates director has one repair-programme
budget: dampers (A), sensors (B), heating valves (C), cooling valves (D) or fan variable-speed drives (E), each repaired on every unit that needs it.
The capital policy funds the programme with the largest expected saving among those that save at least 50,000 kWh a year and pay back within three
years, or none. The estate's book of closed repairs records what each past repair saved.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the alarms under the documented suppression rule, the work orders, the raw trends, the trend
  configuration log and the book's measured savings. The contractor's dampers do alarm, and past drive repairs did save what the book says in
  their first month. Nothing reported is overturned; the decision turns on a population no record lists.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the contractor, the energy manager's view and the licensed basis. The alarms, orders and book still size a drive
  programme that passes both tests.
* **Instrument repair.** A perfect detection system running the same alarm-management rule still suppresses a recurring fault for 90 days, and
  a perfect order system still shows the order closed. The population exists between two correct records by the design of the process.
* **Lens swap.** The naive programme counts units with alarms or open orders and prices them at first-month savings; the answer counts units
  the record shows as fixed and prices the repair at what survives: a different population over a different horizon.

## 3. The driving force

A strong solver distrusts the alarm counts, reruns the detection rules by operating mode on the raw trends, and finds most damper alarms are
start-up transients. It then sees heating-valve "leaks" everywhere, until it reads the trend configuration log: a November controller upgrade
logged valve commands only on 5% changes, so small openings record as zero and look like leaks. Corrected, the drive programme is the clear
winner: 14 units, 86,800 kWh a year, a 2.1-year payback. That build prices each repair at the book's measured saving, taken in the 30 days after
each closed repair, which is inside the 90 days during which a recurring fault cannot alarm. This winter's drive repairs were done by a new
contractor team whose parameter resets do not survive a controller power cycle. Rerunning the rules on the suppressed units' raw trends shows 9
of the 17 drive repairs closed in the last 90 days have the fault back. Those 9 units need the repair again, and a repair that comes back half the
time saves 47% of what the book records. At 23 units and 67,106 kWh a year, the drive programme clears the saving floor and pays back in 4.4 years.
No other programme reaches the floor.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Units with active alarms or open orders per class, priced at the book's saving per repair | A, dampers (115,200 kWh, 2.1-year payback) | The detection screen and the order system are the estate's own records, priced on its own actuals | The raw trends: 26 of the 32 damper alarms fall within 30 minutes of a mode change |
| 1 | Units re-diagnosed by mode on raw trends, transients excluded | C, heating valves (115,200 kWh, 2.7 years) | The textbook diagnosis, rerun from the trends rather than the screen | The trend configuration log: valve commands since November record only 5% steps, and 19 of the 24 "leaks" vanish at the logged resolution |
| 2 | The same, with valve commands read at their logged deadband | E, fan drives (86,800 kWh, 2.1 years) | Both traps beaten, every count reconciled, every price from the book | Rerunning the rules on suppressed units: 9 of 17 drive repairs closed in the last 90 days have the fault back |
| 3 | **Decisive:** the recurring units added to the count and each repair priced at its durable saving (the book's saving × 8/17) | **Hold: no programme passes** | — | — |

* **Why every candidate fails.** On the rung-3 basis the drives save 67,106 kWh but pay back in 4.39 years (limit 3.0); dampers save 19,440,
  heating valves 24,000, cooling valves 11,040 and sensors 7,695 kWh, all under the 50,000 floor. One standard, the policy's two tests on durable
  savings, refuses all five.
* **Blocking quantity and its distance.** The drive programme's durable payback, 4.39 years, 46% over the limit. It would pass if the
  recurrence share were 31% or less (98,133 kWh a year needed).
* **Position table.** Rungs 0–2 commit to A, C and E, each leading its runner-up by 1.33×, 1.33× and 3.62×; no rung leaves the field
  inconclusive.
* **Partial correction priced (L3).** Adding the 9 recurring units to the count but keeping the book's first-month price makes the drive
  programme look larger (142,600 kWh, 2.06 years) and further from a hold than rung 2. Halving the price without adding the units gives 40,880
  kWh, under the floor, and names nothing for the wrong reason: the drives would fail the saving test rather than the payback test, which the
  memo has to state.
* **Grid.** Diagnosis (alarms, modes) × valve resolution (raw, logged) × recurrence (none, count only, price only, both) gives twelve
  builds: three commit to A, three to C and four to E. Two hold: the full build, on the drives' payback, and the price-only build at logged
  resolution, on the drives' 40,880 kWh falling under the saving floor, a different blocking figure.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The alarm-management standard states the 90-day suppression as a rule for operators; the capital policy states the two
   tests; the book states how savings were measured. No document connects suppression to the book's prices or mentions recurrence.
2. **Corpus blind for a computable reason.** *Every saving in the book was measured in the 30 days after its repair closed, inside the 90-day
   window in which a recurring fault cannot alarm, so no closed case can record a recurrence.* The book certifies first-month savings and the
   mode-and-deadband diagnosis exactly.
3. **No arithmetic symptom.** Alarms, orders and units reconcile; every suppressed unit carries a closed order, and the book's savings
   reproduce from its own records.
4. **Not a row predicate.** A recurrence is a closed order on one record followed by the fault's rule pattern on another, inside a window keyed
   to the order date, found only by running the rules on units the alarm stream excludes.
5. **The enumeration is arithmetic.** No column marks a recurrence; the 9 units are a residual between the order system and the trends.
6. **No cutover date.** Recurrences are scattered across the winter as controllers power-cycle; the dated event (the November controller
   upgrade) is the quiet trap's, and it moves the valves, not the drives.
7. **Survives deletion.** With every voice gone, rung 2's drive programme still passes both tests on the book's prices.

## 6. The calibration corpus

* **Form.** The book: 212 closed repairs over three winters, each with the unit, fault class, the rule-attributed saving before repair, and the
  saving measured over the 30 days after closure.
* **What it certifies.** The mode-and-deadband diagnosis: rule-attributed savings match measured ones within 6% for 204 of 212 repairs once
  valve commands are read at their logged resolution, and for 173 on raw trends, every miss an overstated valve repair.
* **What it is blind to.** Recurrence (above).
* **Twin pair.** AHU-14 and AHU-31 are the same model in the same building type, with drive repairs closed the same week, no active alarm and
  no open order. Their January fan energy differs 2.1×. Only rerunning the rules on their raw trends after the closure separates them:
  AHU-14's fault is back.
* **Resemblance points at the decoy.** This winter's drive repairs resemble last winter's on unit type, fault signature and first-month saving,
  and last winter's are the book's best-paying class.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital policy: fund the programme with the largest expected annual saving among those that save at least 50,000 kWh a
  year and pay back within three years, or none; a programme repairs every unit that needs it. The alarm-management standard: alarms are
  suppressed for 90 days after a work order on the unit closes.
* **Empirical pins.** Diagnosis by mode at logged resolution, from the book; recurrence from the raw trends of suppressed units.
* **Voices.** The contractor's account manager: "Your dampers are the problem; the screen tells you so every week." The energy manager: "The
  drive repairs paid for themselves inside a month last winter. Do all of them."
* **Licensed wrong basis.** The policy records that the contractor sizes repair programmes from active alarms and will present that at the
  estates committee.

## 8. Determinism by construction

* **Recurrence.** A unit has recurred when the repaired fault's rule pattern holds for at least 20 steady occupied hours after closure; every
  unit is either well above or at zero, so the cut is immaterial.
* **Durable saving.** The book's saving × the share of last-90-day repairs in the class that did not recur; for classes with no recurrence
  data the book price stands, and none of them nears the floor either way.
* **Prices.** One electricity-equivalent rate (£0.20 per kWh) for every class, from the policy; unit costs from the framework contract.
* **Window.** Last 90 days ending at the extract; every drive repair in the window has at least 30 days of trends after closure.
* **Rounding.** Paybacks to two decimals; no programme sits within 0.2 years of the limit or 5,000 kWh of the floor.

## 9. Prompt sketch and deliverables

> I have one repair-programme budget for the estate's air handlers this winter, and the sustainability committee is convinced the heating
> valves are leaking everywhere. Tell me which programme we fund under the capital policy, or tell me we fund none this winter, with the one
> figure that decides it, in a sentence for the estates committee. Send `repair_programme_case.xlsx`, a chart `programme_payback.png` and a
> one-page `estates_note.pdf`.

* `repair_programme_case.xlsx` — the five programmes under each construction, the buildings sheet (ask A), the spares sheet (ask B) and the
  book back-test (ask C).
* `programme_payback.png` — a scatter of annual saving against payback for the five programmes under each construction, joined by arrows from
  rung 0 to rung 3, with the 50,000 kWh floor and the three-year limit as reference lines, the passing region shaded and the drive programme's
  final point labelled.
* `estates_note.pdf` — the decision, the blocking figure, and what would change it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 buildings, weather-normalised heating gas for this winter and last, in kWh.
  *Device:* the gas meters read in cubic metres and the conversion uses the monthly published calorific value, as the billing guide documents;
  a fixed value misstates every building by up to 3% and reorders the two closest.
* **Ask B (device-carried).** For each of the five component classes, parts in stock and the supplier lead time. *Device:* the stores system
  carries superseded part numbers chained to their replacements, as its catalogue notes document; counting stock under current numbers only
  misses the valve and drive parts held under old numbers.
* **Ask C (validity).** Each programme's unit count, annual saving and payback under each of the four constructions; and the book back-test
  (repairs matched within 6%) on raw and logged valve resolution.
* **Decoupling.** Clearing the recurrence construction changes no figure in asks A or B.

## 11. Rubric arithmetic

12 buildings × 2 winters (ask A) + 5 classes × 2 figures (ask B) + 5 programmes × 4 constructions × 3 figures + 2 back-test counts (ask C) + the
hold, the blocking payback, the recurrence threshold and the runner-up's failure reason + 5 named chart parts + 3 files ≈ 110 criteria.

## 12. World-building constraints

* Book savings per repair (kWh a year): A 3,600, B 900, C 4,800, D 3,000, E 6,200; unit costs £1,500 / £300 / £2,600 / £2,400 / £2,560.
* Counts by rung (A / B / C / D / E): alarms 32 / 9 / 11 / 4 / 14; modes on raw trends 6 / 9 / 24 / 4 / 14; logged resolution 6 / 9 / 5 / 4 /
  14; rung 3 adds 9 recurring drive units.
* Recurrence in the last 90 days: drives 9 of 17; dampers 10%, sensors 5%, heating valves none, cooling valves 8%.
* AHU-14 and AHU-31 identical on every unit, order and alarm column.
* Calorific values and superseded part numbers touch no unit, trend or order in the programme build.
