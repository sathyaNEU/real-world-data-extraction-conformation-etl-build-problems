# FC14 — The warranty reserve for a new cell lot's laptop packs, when a pack dies with its weakest cell and its cells share a tray

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · battery supply quality and warranty |
| Mirrors | Reserving for failures of an assembled product whose components fail by the weakest link and are matched at assembly (Apple and Samsung battery-pack warranty reserves, EV module qualification at Tesla, SSD and DIMM array qualification at hyperscalers) |
| Decision shape | One figure committed at a date: the warranty reserve booked at lot release |
| Committed call | Model K packs built from lot 18-04 expected to fall below 80% capacity within the 600-cycle warranty, to the nearest 10 packs |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S1, the unit the reserve funds (a three-cell pack of tray-mates) is not the unit the test file stores (a cell), with a coarsened segment below it |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #14 coarsens the segment it was asked about · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: three engineering changes to pack build in earlier lots, each logged with pack warranty returns before and after |
| Driving force | The reserve counts packs, and a three-cell series pack is returned when its weakest cell reaches 80%. The assembly standard builds each pack from tray-mates, positions 1–3 or 4–6 of one formation tray, and cells from a bad tray fail together. So pack failures are neither the cell failure share nor the independent weakest-link figure. They are the share of actual tray-mate triples with any failing cell. The test file stores cells, and its trays and positions sit in the formation log. |

## 1. Situation

A laptop maker qualifies each cell lot on 100 cycles of an accelerated test and books a warranty reserve at release. The qualification
memo files the early-prediction model, fitted on earlier batches, that turns each test cell's first 100 cycles into a predicted cycle
life. Lot 18-04 supplies Model K, which takes 7,200 three-cell packs from its A-grade trays, and Model J, which takes the B-grade trays.
The test sample is 20 whole formation trays, 120 cells. Model K's warranty covers 600 cycles, and finance books the Model K reserve on
release day.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the test cycling data, the model's predictions, the qualification summary, the formation log and
  the change log. No one's claim about their own numbers is overturned. The difficulty is the unit the reserve counts, which no test row
  is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The filed model still predicts a cell failure share, and a cell share
  still reads as a pack share.
* **Instrument repair.** No file is suspect: the test file holds every cell's cycling, the formation log every cell's tray and position,
  and the change log every pack-build change. Cycling every cell to end of life returns the same rungs (420, 500, 1,400), because the
  reserve counts packs of tray-mates, a unit no file stores.
* **Lens swap.** The naive read and the answer are different populations: test cells against the packs those cells' tray-mates will
  form.

## 3. The driving force

A strong solver runs the filed model on every test cell, keeps to Model K's A-grade trays and sees that a series pack fails with its
weakest cell. It applies 1 − (1 − p)³ to the A-grade cell share, which treats a pack as three independent draws, and books 1,400
packs. The assembly standard does not draw independently. A pack is positions 1–3 or 4–6 of one formation tray, and cells from one tray
share an electrolyte fill and a formation channel. The test file shows the consequence. Of the five failing A-grade cells, three sit in
tray A3 and two in tray A9. They fall in three of the 24 tray-mate packs the sample forms, 12.5%, against the 19.4% independence
predicts and the 6.9% the cells show. Tray and position are not in the test file. They sit in the formation log, reached by the cell
serial.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The qualification summary's lot-wide predicted cell failure share (7 of 120) × Model K's 7,200 packs | 420 packs, −53% | The filed model, the lot's own summary, the build plan's pack count | **E18 (the segment coarsened):** the build allocation sends only A-grade trays to Model K, and the summary is pooled over both grades |
| 1 | The A-grade cells' failure share (5 of 72) × 7,200 | 500 packs, −44% | The right segment at the right grain, every cell's prediction from the filed model | The warranty policy: a pack is returned when its capacity falls below 80%, and a series pack's capacity is its weakest cell's |
| 2 | Weakest-link with independent cells: 1 − (1 − 5/72)³ × 7,200 | 1,400 packs, +55% | Pack physics applied correctly to the right cells | The change log: when a sorter outage built packs from random cells, returns rose by half; tray-mate packs fail far less often than independence predicts |
| 3 | **Decisive:** test cells grouped into their actual tray-mate triples (formation log, positions 1–3 and 4–6), share of A-grade triples with any predicted failure × 7,200 | **900 packs** | — | — |

* **Figure shape.** Two corrections walk the figure up (−53%, −44%), the independence reading overshoots (+55%), and the decisive rung
  brings it back. A solver who stops anywhere is out by at least 44%.
* **Partial correction priced (L3).** A solver who knows packs fail on the weakest cell but bootstraps random triples from the A-grade
  cells reproduces independence (+55%). Tray-mate triples over all 20 trays, Model J's included, give 720 packs (−20%). Neither is nearer
  than the answer's own construction allows.
* **Grid.** Segment (lot, A-grade) × unit (cell, independent triple, tray-mate triple) gives 6 cells: 420, 500, 1,190, 1,400, 720 and the
  answer. The nearest wrong cell is tray-mates without the grade restriction, 20% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The assembly standard says which positions form a pack. The warranty policy says packs are returned at 80%. No
   document says tray-mates' lives are correlated or how to turn cell predictions into pack failures.
2. **The reproduction numbers.** On the change log's six before-and-after lot pairs, tray-mate triples reproduce all six pack-return
   rates within 0.1 point. Independent triples miss all six high by 35–55%, and the cell share misses all six low. Building the triples is
   a construction: a join from serial to formation log, then a grouping by tray and position band. No parameter does it.
3. **No arithmetic symptom.** Every prediction ties to the filed model, cells to trays, and trays to the build allocation under every
   rung.
4. **Not a row predicate.** A pack's failure is a minimum over three cells reached through another file's tray and position fields. It is
   a group property, not a cell flag.
5. **The enumeration is arithmetic.** Which synthetic packs fail is computed from the triples. No column marks them.
6. **No cutover date.** The lot is a single production run, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The engineering change log's three pack-build changes, each with pack warranty returns for the lots before and after.
  ECN-1907 moved Model J from two-cell to three-cell packs. ECN-2011 built packs from random cells during a quarter-long sorter outage.
  ECN-2104 restored tray-mate matching.
* **What it pins.** The unit and its construction: returns move with cells per pack and with how packs are matched, exactly as tray-mate
  triples predict.
* **Twin pair.** Lots 20-03 and 20-07 are identical on every column the change log and the qualification summaries carry: predicted cell
  failure share 5.0%, lot size, supplier, test protocol and three-cell packs. Their pack returns were 4.4% and 8.8% (2.0×), because 20-07's
  packs were built during the sorter outage. No cell-level rate reproduces both; tray-mate and random triples do.
* **Resemblance points at the decoy.** Lot 18-04's qualification summary most resembles lots whose packs were two-cell, where cell share
  and pack returns were closest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The qualification memo: the early-prediction model, its fit on the earlier batches, and failure as predicted life below
  the warranty cycles. The warranty policy: Model K covers 600 cycles, and a pack is returned below 80% of rated capacity. The assembly
  standard: packs are built from positions 1–3 and 4–6 of a formation tray. The build allocation: A-grade trays to Model K, 7,200 packs.
* **Empirical pins.** Each test cell's tray and position, from the formation log. The pack construction, from the change log's
  natural experiments.
* **Voices.** The quality engineer: "The qualification number is the lot's failure rate. That's what we've always booked." The pack
  designer: "Three cells in series means three chances to fail."
* **Licensed wrong basis.** The memo records that the cell supplier's warranty recovery is negotiated on the lot's predicted cell failure
  share, and that the supplier will present the lot on that basis.

## 8. Determinism by construction

* **Predictions.** The filed model is fixed, so every test cell's predicted life is a single number. No A-grade cell sits within 15 cycles
  of 600.
* **Grades.** Grades are per tray, recorded in the build allocation, so no cell's segment depends on its own capacity.
* **Triples.** Positions are integers 1–6 in the formation log, every test tray is complete, and the standard's position bands leave no
  choice.
* **Scaling.** The reserve scales the sample's failing-pack share to Model K's 7,200 packs, as the memo scales cell shares. No other
  scaling convention is filed.
* **Rounding.** 3 of 24 packs gives exactly 900.

## 9. Prompt sketch and deliverables

> Finance books the warranty reserve for lot 18-04's Model K packs the day we release it, and I need the number of packs to reserve
> for, to the nearest ten. Our quality engineer would book the lot's failure rate as usual. Send me `lot_reserve_build.xlsx`, a chart
> `tray_failure_map.png`, and a one-page `reserve_note.pdf` that commits to the figure.

* `lot_reserve_build.xlsx` — the reserve build cell by cell and tray by tray, the internal-resistance sheet (ask A) and the returns
  sheet (ask B).
* `tray_failure_map.png` — the 20 test trays as a grid of six positions, each cell coloured by predicted life, pack boundaries drawn,
  failing packs outlined, A-grade trays labelled, and the three reserve readings as an inset bar.
* `reserve_note.pdf` — the committed reserve and the basis the supplier will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 20 test trays, the mean and spread of cells' internal resistance at cycle 100.
  *Device:* the cycler logs a resistance pulse twice when a channel is re-seated mid-test, and the test procedure keeps the second
  reading. Averaging both inflates the spread in six trays. Resistance plays no part in the filed model.
* **Ask B (device-carried).** For each of the last eight lots, Model K warranty returns per thousand packs at 12 months in service.
  *Device:* a pack replaced twice under warranty appears twice in the returns file, the second time with a repeat flag, and the policy
  counts packs, not claims. Counting claims overstates three lots by a fifth.
* **Ask C (validity).** The reserve under each of the four rung constructions, with each one's fit to the change log's six lot pairs.
* **Decoupling.** Replacing tray-mate triples with the cell share changes no figure in asks A or B.

## 11. Rubric arithmetic

20 trays × 2 (ask A) + 8 lots × 1 (ask B) + 4 constructions × 2 (ask C) + the committed reserve, the failing packs in the sample and the
A-grade cell share + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Test sample: 20 trays (12 A-grade), 120 cells; 7 predicted failures, 5 of them A-grade (three in tray A3, two in A9), forming 3
  failing packs of 24 A-grade tray-mate packs.
* Rung figures 420 / 500 / 1,400 / 900 packs. Tray-mates without the grade restriction give 720.
* Change-log pairs reproduce within 0.1 point under tray-mate triples only. Lots 20-03 and 20-07 are identical on every summary column.
* Re-seated channels and repeat warranty claims never touch predicted lives, trays or positions.
