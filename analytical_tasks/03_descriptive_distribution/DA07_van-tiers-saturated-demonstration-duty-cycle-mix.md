# DA07 — The replacement tiers a parcel fleet adopts for its nine van models, when three tie at full demonstration and the tie-break rewards the vans with the easiest routes

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · last-mile delivery fleet procurement |
| Mirrors | Choosing a preferred hardware SKU when many tie at full compliance with a duty-cycle target, and some pass only because they ran lighter work than the cycle they are rated for (server SKUs passing power-efficiency bars on lightly loaded racks at cloud providers, EV and van models judged on telematics at large delivery networks, warehouse robots rated on aisles they were spared) |
| Decision shape | A structure the body adopts: the three-tier list for the 2027 replacement round (one Tier 1 model, Tier 2 at 75% demonstrated or more, Tier 3 below) |
| Committed call | The Tier 1 model and each of the nine models' tiers |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · E21, a saturated tie at full demonstration that only each van's duty-cycle economy (its fuel by road class re-weighted to its cycle's mix) breaks, pinned by Pattern B on the parallel run's certified interim results, with E22 (total fuel against total distance) and the card ledger's winter heater draw below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #20 leaves the deciding comparison unstated · #3 stops at a close but inexact match · #12 stops at the first control that passes |
| Calibration form | Parallel-run overlap: April to September 2026, when the fuel bureau's card accounting and the telematics fuel-flow system both measured every van, and the bureau certified each van's interim demonstration |
| Driving force | A van demonstrates when its economy meets its duty-cycle target, and a duty cycle is a mix of urban, suburban and rural kilometres. Telematics records every van's distance and fuel by road class. Aldo is the fleet's relief model: its vans are assigned to urban depots and spend much of the year on suburban and rural relief runs, where any van does better, so every Aldo unit beats the urban target on its raw economy. Re-weighted to the urban cycle's mix, half of them fall short. The bureau's certified interim results reproduce only on that re-weighting, and with it only Vela, whose vans run the cycles they are rated for, keeps every unit at target. |

## 1. Situation

A parcel carrier runs 2,640 vans of nine models from 14 depots. Its procurement framework sets the tiers for the 2027 replacement round.
Tier 1 goes to the model whose every unit in service demonstrated its duty-cycle fuel-economy target over the assessment year (October
2025 to September 2026), ties broken by distance driven. Tier 2 takes models with at least 75% of units demonstrated, and Tier 3 the
rest. The pack holds the telematics feed (distance and fuel-flow litres per van per day, by road class), the fuel bureau's card ledger,
the effective-dated card-to-van assignments, the build specifications, the duty-cycle schedule and the parallel-run report with the
bureau's interim certifications. The procurement board adopts the tiers on 3 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: telematics distance and fuel, the card ledger, the assignments, the build specs and the
  certifications. Aldo's vans really do beat the urban target on the routes they drove, and nobody's reading of their own numbers is
  overturned. The difficulty is what demonstrating a duty-cycle target means.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the fleet engineering lead's view, the region manager's view and the leasing partner's basis. Three models
  still tie at 100% on the lowest-consistent economy, and the distance tie-break still names Aldo.
* **Instrument repair.** Clean-data test. The suspect file is the telematics feed, whose fuel-flow signal counts injector flow only and
  misses the fuel-fired cab heaters' winter draw. Repair it (meter all tank fuel): rung 1 becomes rung 2's construction and names Aldo,
  rung 0 still names Torvan, the answer is unchanged, and re-weighting each van to its duty cycle is still needed. No other file is
  suspect: road-class distances and fuel are complete for every van, and the card ledger and assignments reconcile.
* **Lens swap.** The two reads judge different journeys: each van's own year of driving, against the duty cycle it is rated for. On
  Aldo's 370 vans the two differ by up to 9% in economy.

## 3. The driving force

A strong solver computes each van's economy as total distance over total fuel, not the average of monthly rates, and applies the
framework's rule that a unit's economy is the lowest consistent with every file of record. The card ledger, allocated through the card
assignments, shows winter litres that telematics misses on heater-equipped vans, and Kestrel's northern vans drop below target. Three
models still have every unit at target, and the distance tie-break gives Aldo Tier 1. But the target is a duty-cycle target, and the
schedule defines each cycle by its mix of urban, suburban and rural kilometres. Aldo is the fleet's relief model: assigned to urban
depots, its vans spend much of the year covering suburban and rural rounds, where fuel economy is easier. Telematics records each van's
fuel by road class, so each van's economy on its cycle's mix can be built exactly. The bureau's interim certifications reproduce only
that way. Re-weighted, 185 of Aldo's 370 vans miss the urban target, and only Vela keeps every unit.

## 4. The ladder

| Rung | Construction | Names (Tier 1) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each van's economy as the mean of its twelve monthly telematics economies; seven models at 100%, distance tie-break | A, Torvan (9.8M km, 1.32× Kestrel) | The framework's test and tie-break applied as written | The duty-cycle target is an economy over the year, and total distance over total fuel puts Torvan units below it |
| 1 | Total distance over total fuel per van (E22); five models at 100% | B, Kestrel (7.4M km, 1.21× Aldo) | The deciding comparison done properly, matching the parallel run's per-van totals | The card ledger through the card assignments: from November to March, heater-equipped vans drew fuel telematics never saw |
| 2 | Each van on the lower of its telematics and card economies (the framework's lowest-consistent rule); three models at 100% | C, Aldo (6.1M km, 1.22× Vela) | The framework's own rule applied to both files of record | The parallel run's certifications: raw economy reproduces 2,301 of 2,640 interim results, every miss a van passed that the bureau failed |
| 3 | **Decisive:** each van's lowest-consistent economy re-weighted by road class to its duty cycle's mix; only Vela at 100% | **D, Vela (1.00 against Aldo's 0.50)** (4th of the seven tied on rung 0) | — | — |

* **Position table.** Vela is 4th of the tied seven on rung 0, 3rd on rung 1 and 2nd on rung 2 (1.22× behind Aldo on distance), and
  leads only rung 3. Each rung's leader beats its runner-up by at least 1.21×.
* **Discriminator dominance.** Aldo carries 1.22× on distance, the tie-break axis, into rung 3. On the decisive axis, demonstrated share,
  Vela holds 1.00 against Aldo's 0.50, an edge of 2.00×. That is 1.37 times the required 1.2 × 1.22 = 1.46, though the framework ranks
  share before any tie-break.
* **Partial correction priced (L3).** Every half-applied construction names a wrong outcome. Re-weighting without the card ledger keeps
  Kestrel at 100% and names it (1.48× Vela on distance). Re-weighting by each depot's average route mix instead of each van's own leaves
  Aldo's relief runs averaged away and names Aldo (1.22×). Re-weighting monthly-mean economies keeps Torvan at 100% and names Torvan.
* **Grid.** Averaging (monthly mean or total) × files (telematics or lowest consistent) × economy (as driven or on the duty cycle) gives
  8 cells. Every non-answer cell names Torvan, Kestrel or Aldo, and only total economy, both files and the duty-cycle mix name Vela.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The framework says "its duty-cycle target"; the schedule gives each cycle's target and kilometre mix. No document
   says a van is judged on its cycle's mix rather than the routes it drove, or names the relief runs.
2. **Reproduction, and why it is a construction.** Duty-cycle economy on total fuel reproduces all 2,640 interim certifications. Raw
   economy reproduces 2,301, and every one of its 339 misses passes a van the bureau failed, so it cannot reconcile on any model's pass
   count. The reproducing quantity re-weights each van's own fuel per kilometre by road class to its cycle's mix. No threshold or menu
   reaches it.
3. **No arithmetic symptom.** Road-class distances sum to each van's distance, fuel sums to its total, cards reconcile to assignments,
   and every raw economy is correct.
4. **Not a row predicate.** A van's duty-cycle economy is a weighted combination of its own per-class economies, built from its whole
   year of road-class records.
5. **The enumeration is arithmetic.** 2,640 vans are re-weighted; 185 of Aldo's 370 and 22 of Corso's 255 fall below target.
6. **No cutover date.** Relief work runs all year and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, three models still tie at 100% on raw economy.

## 6. The calibration corpus

* **Form.** The parallel-run report and its data: for April to September 2026, each van's monthly litres from the card ledger and from
  telematics, the bureau's odometer readings, and the bureau's interim certification of each van against its duty-cycle target.
* **What it certifies.** Telematics as an instrument in summer (every van within 0.5% of its cards), total-over-total economy, and the
  duty-cycle re-weighting (2,640 of 2,640, above).
* **What it is blind to.** Winter heater draw: *in every van-month of the run, cards and telematics agree within 0.5%, because the run
  covered April to September and fuel-fired heaters only fire below 5°C.* The card ledger's winter months find it.
* **Twin pair.** Depots East-2 and West-5 are identical on every telematics column: 40 Aldo vans each, the same distance, litres and raw
  economies, both rated on the urban cycle. East-2's vans ran their urban rounds; West-5's covered rural relief. Re-weighted to the urban
  cycle, 37 and 18 of their vans demonstrate (2.1×). Every raw-economy rule passes all 80.
* **Resemblance points at the decoy.** Vela's telematics profile most resembles Aldo's, the model the distance tie-break favours.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The framework: "A unit demonstrates when its fuel economy over the assessment year meets its duty-cycle target; a unit's
  economy is the lowest consistent with every file of record. Tier 1 is the model with every unit in service demonstrated, ties broken by
  distance driven; Tier 2 needs 75% demonstrated." The duty-cycle schedule: urban 8.6 km per litre on 70% urban, 25% suburban and 5%
  rural kilometres; mixed 9.4; rural 10.2, each with its mix.
* **Empirical pins.** Total economy and the duty-cycle re-weighting, from the parallel run's certifications.
* **Voices.** The fleet engineering lead: "Telematics settles it, and the parallel run matched the bureau van for van." The southern
  region manager: "Our Aldos cover every gap in the network and still hit target. They've earned Tier 1."
* **Licensed wrong basis.** The framework records that the leasing partner scores models on raw telematics economy and will present its
  own tier list to the board.

## 8. Determinism by construction

* **Population.** Only vans in service for the whole year are scored, and each van's duty cycle is its depot's, fixed for the year.
* **Road classes.** Telematics assigns every kilometre to one of three classes from the national road register, and fuel follows the
  kilometres it was burned on.
* **Card allocation.** No card served two vans on one day, and every fill falls inside one assignment interval.
* **Thresholds.** No van's duty-cycle economy lies within 0.5% of its target, and no model's share lies within five points of 75%.
* **Tie-break.** Distances are distinct to the kilometre, so no tie survives under any construction.

## 9. Prompt sketch and deliverables

> The procurement board fixes the 2027 replacement tiers on 3 December: which van model takes Tier 1 and where the other eight sit. Our
> fleet engineering lead believes the telematics data settles it. Name the Tier 1 model and each model's tier, as the table the board
> adopts, and send `tier_case.xlsx` with the sheets below, plus `demonstration_chart.png`.

* `tier_case.xlsx` — the per-van build, each model's demonstrated share under the four rung constructions (ask C), the workshop sheet
  (ask A) and the tyre sheet (ask B).
* `demonstration_chart.png` — each model's demonstrated share on raw and on duty-cycle economy as paired bars, the 100% and 75% tier
  lines labelled, Aldo's road-class mix against the urban cycle's as an inset, and the East-2 and West-5 twins annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Van-days lost to unplanned repairs at each of the 14 depots in each half of the assessment year.
  *Device:* a job re-opened after a failed road test is logged as a new job carrying its parent's number, as the workshop guide
  documents. Counting it separately double-counts the overlap days, overstating 19 of the 28 cells by 4% to 15%.
* **Ask B (device-carried).** Tyres replaced per 100,000 km for each of the nine models. *Device:* the tyre contract logs a pair fitted
  on one axle as one job line with quantity 2. Counting lines understates every model, and the error varies with each model's pair share,
  so it reorders five models.
* **Ask C (validity).** Each model's demonstrated share under each of the four rung constructions, and each construction's reproduction
  count on the interim certifications.
* **Decoupling.** The workshop system and the tyre contract share no row with the telematics feed or the card ledger. Clearing the
  duty-cycle re-weighting changes no figure in asks A or B.

## 11. Rubric arithmetic

14 depots × 2 halves (ask A) + 9 models (ask B) + 9 models × 4 constructions and 4 reproduction counts (ask C) + the Tier 1 model and the
nine tiers + 4 named chart parts + 2 files ≈ 93 criteria.

## 12. World-building constraints

* Distances (millions of km): Torvan 9.8, Kestrel 7.4, Aldo 6.1, Vela 5.0, Corso 4.2, Brenta 3.4, Ferro 2.9, Lumo 2.6, Sabre 2.2. Van
  counts: Torvan 594, Kestrel 448, Aldo 370, Vela 303, Corso 255, Brenta 206, Ferro 176, Lumo 158, Sabre 133.
* Tier 1 by rung: Torvan, Kestrel, Aldo, Vela. Shares at rung 3: Vela 1.00, Corso 0.91, Kestrel 0.80, Ferro 0.80, Brenta 0.79, Lumo 0.77,
  Torvan 0.69, Sabre 0.67, Aldo 0.50, giving Tier 2 to five models and Tier 3 to three.
* Aldo's vans run 41% of their kilometres off their urban cycle's mix; Vela's run within two points of their cycles' mixes.
* Kestrel's northern vans carry fuel-fired heaters; every card-minus-telematics litre falls between November and March, and none in the
  parallel run.
* The interim certifications reproduce 2,640 of 2,640 on duty-cycle economy and 2,301 on raw economy. East-2 and West-5 are identical on
  every telematics column.
* The workshop system and the tyre contract touch no fuel or distance record.
