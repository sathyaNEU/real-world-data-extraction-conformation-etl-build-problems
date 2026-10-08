# RC09 — Which air-handler repair programme the estates budget buys this winter, or none, when the book's best repair was only ever made where fans could slow

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · university estates and facilities management |
| Mirrors | Fix-programme sizing for fleets of connected equipment (data-centre cooling units, fulfilment-centre conveyors, Apple and Cisco field-repair programmes), where the book of past repairs prices a fix on units whose operating regime let it pay, and this year's faulty units run a regime in which it cannot |
| Decision shape | Hold, forced by a blocking quantity: fund one repair programme across the estate, or none this winter |
| Committed call | No programme this winter, with the blocking figure: the largest programme, the fan drives, saves 37,800 kWh a year at the hours its units' fans can slow, under the policy's 50,000 floor, and would pay back in 4.7 years against three |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · L1 with S4 (the book certifies the shallow rungs and is blind to the decisive one: every drive repair it holds served demand-controlled spaces, whose fans slow for about 80% of occupied hours, while this winter's faulty drives mostly serve lecture theatres ventilated to the timetable), with E15 (the quiet second trap) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #9 picks from the offered options when none passes · #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: the estate's 212 closed air-handler repairs over three winters, each with its measured saving |
| Driving force | A variable-speed drive repair saves energy only in the hours the fan can run below its design airflow. Every drive repair in the estate's book served demand-controlled offices and libraries, whose fans slow for about 80% of occupied hours, so the book's price per repair is right for them and reproduces every closed case. Ten of this winter's fourteen faulty drives serve lecture theatres ventilated at design airflow throughout the timetable, where the fans slow for 17% of occupied hours. Priced at the hours each unit's ventilation control lets its fan slow, the drive programme falls under the policy's saving floor, and no programme passes. |

## 1. Situation

A university's estates department runs 40 air-handling units across 12 buildings, and heating and ventilation energy rose sharply this winter. The
maintenance contractor blames economiser dampers, which alarm every week on the fault-detection screen. The estates director has one repair-programme
budget: dampers (A), sensors (B), heating valves (C), cooling valves (D) or fan variable-speed drives (E), each repaired on every unit that needs it.
The capital policy funds the programme with the largest expected saving among those that save at least 50,000 kWh a year and pay back within three
years, or none. The estate's book of closed repairs records what each past repair saved.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the alarms, the work orders, the raw trends, the trend configuration log, the building management
  system's zone schedules and the book's measured savings. The contractor's dampers do alarm, and past drive repairs did save what the book says.
  Nothing reported is overturned; the decision turns on what a repair can save on units unlike any the book holds.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the contractor, the energy manager's view and the licensed basis. The alarms, orders and book still size a drive
  programme that passes both tests.
* **Instrument repair.** Suspect file: the trend log, which since November records valve commands only on 5% changes. Repaired to full
  resolution, rung 1 drops the phantom leaks and names E, the drive programme at 86,800 kWh and 2.1 years, as rung 2 does; rung 0 still names A.
  The alarms, orders, zone schedules and book are complete, and the book's savings are correct for the repairs it holds. No rung holds. The
  answer still needs each unit's repair priced at the hours its ventilation control lets the fan slow: no record of past repairs, however
  complete, measures a drive repair on a fan held at design airflow.
* **Lens swap.** The naive programme prices this winter's drive units at the book's repairs; the answer prices them at what their own ventilation
  control lets a repair save: a different population of units under a different operating regime.

## 3. The driving force

A strong solver distrusts the alarm counts, reruns the detection rules by operating mode on the raw trends, and finds most damper alarms are
start-up transients. It then sees heating-valve "leaks" everywhere, until it reads the trend configuration log: a November controller upgrade
logged valve commands only on 5% changes, so small openings record as zero and look like leaks. Corrected, the drive programme is the clear
winner: 14 units, 86,800 kWh a year, a 2.1-year payback at the book's 6,200 kWh per repair. A drive repair restores variable speed, and it saves
energy only in the hours the fan can run below its design airflow. Every drive repair in the book served demand-controlled offices and
libraries, whose fans slow for about 80% of occupied hours as rooms empty. Ten of this winter's fourteen faulty drives serve lecture theatres
ventilated at design airflow for the whole timetable, where the fans slow for 17% of occupied hours. Priced at the hours each unit's ventilation
control lets its fan slow, the drive programme saves 37,800 kWh a year and pays back in 4.74 years: under the saving floor and over the payback
limit. No other programme reaches the floor.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Units with active alarms or open orders per class, priced at the book's saving per repair | A, dampers (115,200 kWh, 2.1-year payback) | The detection screen and the order system are the estate's own records, priced on its own actuals | The raw trends: 26 of the 32 damper alarms fall within 30 minutes of a mode change |
| 1 | Units re-diagnosed by mode on raw trends, transients excluded | C, heating valves (115,200 kWh, 2.7 years) | The textbook diagnosis, rerun from the trends rather than the screen | The trend configuration log: valve commands since November record only 5% steps, and 19 of the 24 "leaks" vanish at the logged resolution |
| 2 | The same, with valve commands read at their logged deadband | E, fan drives (86,800 kWh, 2.1 years) | Both traps beaten, every count reconciled, every price from the book | The zone schedules: 10 of the 14 drive units serve lecture theatres ventilated at design airflow through the timetable, and every drive repair in the book served demand-controlled spaces |
| 3 | **Decisive:** each repair priced at the book's saving per hour below design airflow × the hours its unit's ventilation control lets the fan slow | **Hold: no programme passes** | — | — |

* **Why every candidate fails.** On the rung-3 basis the drives save 37,800 kWh and pay back in 4.74 years (limit 3.0); dampers save 21,600,
  heating valves 24,000, cooling valves 12,000 and sensors 8,100 kWh, all under the 50,000 floor. One standard, the policy's two tests on the
  savings each unit's ventilation allows, refuses all five.
* **Blocking quantity and its distance.** The drive programme's saving, 37,800 kWh a year, 24% under the floor, with a payback 58% over the
  limit. It would pass both tests only if its lecture-theatre fans could slow for 45% of occupied hours; they slow for 17%.
* **Position table.** Rungs 0–2 commit to A, C and E, each leading its runner-up by 1.33×, 1.33× and 3.62×; no rung leaves the field
  inconclusive.
* **Partial correction priced (L3).** Each half of the pricing funds the drives. Scaling each drive repair by the share of hours its building is
  occupied, rather than the hours its fan can slow, makes the lecture theatres look like the book's offices, since both are occupied all day:
  86,100 kWh and 2.08 years. Reading each unit's reduced-speed hours from the commissioning file's design schedules, which specified demand
  control the building management system never enabled in the lecture theatres, gives 66,000 kWh and 2.72 years.
* **Grid.** Diagnosis (alarms, modes) × valve resolution (raw, logged) × drive pricing (book, occupied hours, design schedules, operating
  schedules) gives sixteen builds: eight commit to A, four to C, three to E, and only the full build holds.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The capital policy states the two tests; the book states how savings were measured; the building management system
   holds each zone's ventilation schedule. No document says a drive repair saves only in the hours a fan can slow, or that every drive repair in
   the book served a demand-controlled space.
2. **Corpus blind for a computable reason.** *Every drive repair in the book served demand-controlled spaces, whose fans run below design
   airflow for about 80% of occupied hours, so in every closed case the reduced-speed share was the same and the book's flat price reproduces
   every drive saving.* The book certifies the mode-and-deadband diagnosis and its own prices exactly.
3. **No arithmetic symptom.** Alarms, orders and units reconcile, and the book's savings reproduce from its own records under every
   construction.
4. **Not a row predicate.** A unit's saving depends on the hours its ventilation control lets the fan slow, computed from the hourly schedules of
   the zones it serves, a join across the unit, its zones and their schedules.
5. **The enumeration is arithmetic.** No column carries a unit's reduced-speed hours; fourteen are computed from the zone schedules.
6. **No cutover date.** The lecture theatres have run on timetable ventilation since they opened; the dated event (the November controller
   upgrade) belongs to the valve trap.
7. **Survives deletion.** With every voice gone, rung 2's drive programme still passes both tests on the book's prices.

## 6. The calibration corpus

* **Form.** The book: 212 closed repairs over three winters, each with the unit, the fault class, the zones it serves, the rule-attributed
  saving before repair, and the saving measured over the following winter.
* **What it certifies.** The mode-and-deadband diagnosis: rule-attributed savings match measured ones within 6% for 204 of 212 repairs once
  valve commands are read at their logged resolution, and for 173 on raw trends, every miss an overstated valve repair.
* **What it is blind to.** Ventilation control (above).
* **Twin pair.** AHU-14 and AHU-31, repaired in October and monitored since, are the same model with the same drive fault, the same pre-repair
  fan energy and the same occupied hours. Their fan savings since the repair differ 2.0×: AHU-14's office floor is demand-controlled and its fan
  slows for 80% of occupied hours, AHU-31's seminar rooms run to the timetable and its fan slows for 40%. Only the zone schedules separate them.
* **Resemblance points at the decoy.** This winter's drive faults resemble last winter's on unit type, fault signature and pre-repair fan
  energy, and last winter's are the book's best-paying class.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital policy: fund the programme with the largest expected annual saving among those that save at least 50,000 kWh a
  year and pay back within three years, or none; a programme repairs every unit that needs it. The framework contract: the unit cost of each
  repair class.
* **Empirical pins.** Diagnosis by mode at logged resolution, from the book; each unit's reduced-speed hours from its zone schedules.
* **Voices.** The contractor's account manager: "Your dampers are the problem; the screen tells you so every week." The energy manager: "The
  drive repairs paid for themselves inside a month last winter. Do all of them."
* **Licensed wrong basis.** The policy records that the contractor sizes repair programmes from active alarms and will present that at the
  estates committee.

## 8. Determinism by construction

* **Reduced-speed hours.** A fan runs below design airflow in an hour when its zones' airflow setpoint is under 90% of design; occupied hours
  follow the timetable and opening hours; the share is taken over last winter's occupied hours.
* **Pricing.** The book's drive saving (6,200 kWh a repair) belongs to an 80% share; a unit's saving is the book's × its share ÷ 80%. The other
  classes' savings do not depend on airflow and keep the book price.
* **Prices.** One electricity-equivalent rate (£0.20 per kWh) for every class, from the policy; unit costs from the framework contract.
* **Counts.** This winter's diagnoses at the extract; every unit's zone schedules cover last winter.
* **Rounding.** Paybacks to two decimals; no programme sits within 0.2 years of the limit or 5,000 kWh of the floor.

## 9. Prompt sketch and deliverables

> I have one repair-programme budget for the estate's air handlers this winter, and the sustainability committee is convinced the heating
> valves are leaking everywhere. Tell me which programme we fund under the capital policy, or tell me we fund none this winter, with the one
> figure that decides it, in a sentence for the estates committee. Send `repair_programme_case.xlsx`, a chart `programme_payback.png` and a
> one-page `estates_note.pdf`.

* `repair_programme_case.xlsx` — the five programmes under each construction, the buildings sheet (ask A), the spares sheet (ask B) and the
  book back-test (ask C).
* `programme_payback.png` — a scatter of annual saving against payback for the five programmes under each construction, joined by arrows from
  rung 0 to rung 3, with the 50,000 kWh floor and the three-year limit as reference lines, the passing region shaded, and the drive programme's
  final point labelled with its units' reduced-speed share.
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
* **Decoupling.** Clearing the reduced-speed pricing changes no figure in asks A or B.

## 11. Rubric arithmetic

12 buildings × 2 winters (ask A) + 5 classes × 2 figures (ask B) + 5 programmes × 4 constructions × 3 figures + 2 back-test counts (ask C) + the
hold, the blocking saving, the payback and the threshold share + 5 named chart parts + 3 files ≈ 110 criteria.

## 12. World-building constraints

* Book savings per repair (kWh a year): A 3,600, B 900, C 4,800, D 3,000, E 6,200 at an 80% reduced-speed share; unit costs £1,500 / £300 /
  £2,600 / £2,400 / £2,560.
* Counts by rung (A / B / C / D / E): alarms 32 / 9 / 11 / 4 / 14; modes on raw trends 6 / 9 / 24 / 4 / 14; logged resolution 6 / 9 / 5 / 4 /
  14.
* Drive units: 4 demand-controlled at 80%, 10 lecture theatres on timetable ventilation at 17%; 37,800 kWh, 4.74 years. Partials: occupied-hours
  scaling 86,100 kWh and 2.08 years; design schedules 66,000 kWh and 2.72 years.
* Every drive repair in the book served demand-controlled spaces.
* AHU-14 and AHU-31 identical on every unit, fault, order and occupancy column.
* Calorific values and superseded part numbers touch no unit, trend, schedule or order in the programme build.
