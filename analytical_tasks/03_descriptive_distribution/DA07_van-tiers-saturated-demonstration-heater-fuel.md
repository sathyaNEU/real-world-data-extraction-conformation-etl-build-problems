# DA07 — The replacement tiers a parcel fleet adopts for its nine van models, when seven tie at full demonstration on the telematics everyone trusts

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · last-mile delivery fleet procurement |
| Mirrors | Choosing a preferred hardware SKU when many tie at full compliance on the telemetry everyone trusts (server SKUs all meeting a power-efficiency bar on BMC readings until reconciled with metered rack draw at cloud providers, EV and van models on telematics against charging or fuel invoices at large delivery networks) |
| Decision shape | A structure the body adopts: the three-tier list for the 2027 replacement round (one Tier 1 model, Tier 2 at 75% demonstrated or more, Tier 3 below) |
| Committed call | The Tier 1 model and each of the nine models' tiers |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · E21, a saturated tie at full demonstration broken only by the framework's lowest-consistent rule, with E22 (total fuel against total distance) below it and a parallel run blind to winter heater draw (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #20 leaves the deciding comparison unstated · #13 validates on one population, applies to another · #12 stops at the first control that passes |
| Calibration form | Parallel-run overlap: April to September 2026, when the fuel bureau's card-based accounting and the telematics fuel-flow system both measured every van |
| Driving force | On telematics, seven of nine models demonstrate their duty-cycle economy on every unit, and the framework's distance tie-break hands Tier 1 to the biggest. The framework scores a unit on the lowest economy consistent with every file of record, and the fuel-card ledger is one. Fuel-fired cab heaters, a build option on most vans in the northern depots, draw from the main tank below 5°C, and the engine's fuel-flow signal counts only injector flow. In winter the cards carry litres the telematics never sees. The parallel run that certified telematics van for van ran April to September, when no heater fires. |

## 1. Situation

A parcel carrier runs 2,640 vans of nine models from 14 depots. Its procurement framework sets the tiers for the 2027 replacement round.
Tier 1 goes to the model whose every unit in service demonstrated its duty-cycle fuel-economy target over the assessment year (October
2025 to September 2026), ties broken by distance driven. Tier 2 takes models with at least 75% of units demonstrated, and Tier 3 the
rest. The pack holds the telematics feed (distance and fuel-flow litres per van per day), the fuel bureau's card ledger, the
effective-dated card-to-van assignments, the build specifications with option codes, the depot transfer log and the parallel-run report.
The procurement board adopts the tiers on 3 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: telematics distance and fuel flow, the card ledger, the assignments, the build specs and the
  parallel-run report. Telematics measures engine fuel exactly, and nobody's reading of their own numbers is overturned. The difficulty
  is which units actually demonstrate their target under the framework's own scoring.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the fleet engineering lead's view and the leasing partner's licensed basis. The telematics feed still gives a
  clean economy for every van, and seven models still tie at 100%.
* **Instrument repair.** Make the fuel-flow sensor perfect: it already reads the injectors exactly. A fuel-fired heater burns tank fuel
  outside the engine, so a perfect engine instrument still never sees it. The card ledger is a second instrument of record, not a
  correction to the first.
* **Lens swap.** The two reads cover different fuel: engine fuel against all fuel drawn from the tank. They differ only in the winter
  months and only on 1,060 heater-equipped vans, so they put different units below target.

## 3. The driving force

A strong solver computes each van's economy as total distance over total fuel, not the average of monthly rates. It removes the distance
the transfer log shows was reported on two gateways after depot moves, checks telematics against the parallel run (every van agreeing within 0.5%),
and finds four models still at 100%. The framework's tie-break then gives Tier 1 to Aldo, the one driven furthest. But the framework
scores a unit on "the lowest economy consistent with every file of record", and the parallel run's agreement belongs to summer. A
fuel-fired cab heater runs off the main tank whenever the cab is below 5°C. The engine's fuel-flow signal counts injector flow only, so
from November to March the cards record litres that telematics cannot. Building each van's card litres takes the card ledger through
the effective-dated card assignments, and the build-spec option code H2 marks the fuel-fired heater. On the lower of the two economies,
only Vela, whose heater option is electric, keeps every unit at target.

## 4. The ladder

| Rung | Construction | Names (Tier 1) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each van's economy as the mean of its twelve monthly telematics economies; seven models at 100%, distance tie-break | A, Torvan (9.8M km, 1.32× Kestrel) | The framework's test and tie-break applied as written | The duty-cycle target is an economy over the year, and total distance over total fuel puts Torvan and Brenta units below it |
| 1 | Total distance over total fuel per van (E22); five models at 100% | B, Kestrel (7.4M km, 1.21× Aldo) | The deciding comparison done properly, matching the parallel run's per-van totals | The transfer log: after each depot move a van reports on both gateways until the old one is closed, two to six weeks for Kestrel's relief vans |
| 2 | Post-transfer distance counted once (hygiene); four models at 100% | C, Aldo (6.1M km, 1.22× Vela) | Every van now reconciles to the parallel run within 0.5% | The card ledger through the card assignments: from November to March, heater-equipped vans drew fuel the telematics never saw |
| 3 | **Decisive:** each van scored on the lower of its telematics and card-ledger economies; only Vela stays at 100% | **D, Vela (1.00 against Kestrel's 0.82, 1.22×)** (4th of the seven tied on rung 0) | — | — |

* **Position table.** Vela is 4th of the tied seven on rung 0 (ranked by the tie-break), 3rd on rung 1 and 2nd on rung 2 (1.22× behind
  Aldo on distance), and leads only rung 3. Each rung's leader beats its runner-up by at least 1.21×.
* **Discriminator dominance.** Aldo carries 1.22× on distance, the tie-break axis, into rung 3. On the decisive axis, demonstrated share,
  Vela holds 1.00 against Aldo's 0.50, an edge of 2.00×. That is 1.37 times the required 1.2 × 1.22 = 1.46, even though the framework
  ranks share before any tie-break.
* **Partial correction priced (L3).** Every half-applied construction names a wrong outcome. Reconciling card litres at fleet level finds
  the 1.9% gap inside the bureau's tolerance and keeps Aldo (1.22× Vela on distance). Checking card litres only in the parallel-run months
  finds nothing and keeps Aldo too. Averaging the two economies instead of taking the lower halves the heater penalty and leaves Aldo,
  Corso and Vela at 100%, so the tie-break again gives Aldo Tier 1 (1.22×). In April, 41 Aldo vans and 41 Vela vans swapped depots and
  their depot fuel cards changed hands. Allocating fills by each card's current van, not its van on the fill date, moves the Aldo vans'
  winter heater litres onto those Vela vans. Vela falls to 0.97, no model is fully demonstrated, and the board would adopt no Tier 1 at all.
* **Grid.** Averaging (monthly mean or total) × post-transfer distance (twice or once) × files (telematics or lowest consistent) gives 8
  cells. Every non-answer cell names Torvan, Kestrel or Aldo. Kestrel carries no fuel-fired heaters, so without the transfer fix its
  doubled distance keeps it level with Vela at 100% under the lowest-consistent rule, and the tie-break hands it Tier 1.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The framework states the lowest-consistent rule but not that the files disagree. The build-spec codebook lists
   H2 as "auxiliary cab heater, fuel-fired", and no document says where its fuel is drawn or metered.
2. **Corpus blind for a computable reason.** *In every van-month of the parallel run, telematics and card litres agree within 0.5%,
   because the run covered April to September and fuel-fired heaters only run below 5°C.* The run certifies telematics, and the transfer
   fix, van for van.
3. **No arithmetic symptom.** Over the year the fleet's card litres exceed telematics by 1.9%, inside the bureau's documented 2.5%
   tank-timing tolerance. Distance, card counts and assignments all reconcile.
4. **Not a row predicate.** A van's card litres are fills allocated through effective-dated card assignments, summed by month and set
   against the same van's telematics. Its score is the lower of two annual economies. No row carries it.
5. **The enumeration is arithmetic.** 1,060 heater vans, of which 526 fall below target, are found only by the allocation and the
   comparison.
6. **No cutover date.** Heaters fire with the weather every winter, and the card gap rises and falls smoothly with temperature. No series
   steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, seven models still tie at 100% on the feed.

## 6. The calibration corpus

* **Form.** The parallel-run report and its data: for April to September 2026, each van's monthly litres from the card ledger and from
  telematics, and the bureau's odometer readings.
* **What it certifies.** Telematics as an instrument (every van within 0.5% of its cards), total-over-total economy, and the transfer fix
  (all 212 moves in the run show the dual-gateway distance the fix removes against the bureau's odometer readings).
* **What it is blind to.** Winter heater draw (above).
* **Twin pair.** Depots North-7 and South-3 are identical on every telematics column: vans, model mix, distance, telematics litres and
  monthly economies. Their unmetered fuel for the year (card litres less telematics) is 38,400 and 19,200 litres (2.0×). North-7's Corsos
  carry the fuel-fired heater (H2), and South-3's carry the electric one (H1). Only the card-ledger allocation separates them.
* **Resemblance points at the decoy.** Vela's telematics profile (route types, distance per van, monthly economies) most resembles
  Aldo's, the model the distance tie-break favours.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The framework: "A unit demonstrates when its fuel economy over the assessment year meets its duty-cycle target; a unit's
  economy is the lowest consistent with every file of record." The framework: "Tier 1 is the model with every unit in service
  demonstrated, ties broken by distance driven; Tier 2 needs 75% demonstrated." The duty-cycle schedule gives the targets (urban 8.6, mixed
  9.4, rural 10.2 km per litre). The transfer log's notes describe the dual-gateway report after a depot move.
* **Empirical pins.** The economy construction and the transfer fix, from the parallel run.
* **Voices.** The fleet engineering lead: "Telematics settles it; the parallel run matched the bureau van for van." The northern region
  manager: "Our vans do the hardest miles in the fleet and still hit target. Aldo has earned Tier 1."
* **Licensed wrong basis.** The framework records that the leasing partner scores models on telematics economy alone and will present its
  own tier list to the board.

## 8. Determinism by construction

* **Population.** Only vans in service for the whole year are scored. No van changed model or build options during the year.
* **Card allocation.** No card served two vans on one day, and every fill falls inside one assignment interval, so allocating by fill
  date and by posting date gives the same litres.
* **Thresholds.** No van's lower economy lies within 0.5% of its target. No model's demonstrated share lies within five points of 75%.
* **Tie-break.** Distances are distinct to the kilometre, so no tie survives the tie-break under any construction.

## 9. Prompt sketch and deliverables

> The procurement board fixes the 2027 replacement tiers on 3 December: which van model takes Tier 1 and where the other eight sit. Our
> fleet engineering lead believes the telematics data settles it. Name the Tier 1 model and each model's tier, as the table the board
> adopts, and send `tier_case.xlsx` with the sheets below, plus `demonstration_chart.png`.

* `tier_case.xlsx` — the per-van build, each model's demonstrated share under the four rung constructions with each one's total distance
  against total fuel (ask C), the workshop sheet (ask A) and the tyre sheet (ask B).
* `demonstration_chart.png` — each model's demonstrated share under telematics alone and under the lowest-consistent rule as paired
  bars, the 100% and 75% tier lines labelled, monthly card-minus-telematics litres for heater and non-heater vans as an inset, and the
  North-7 and South-3 twins annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Van-days lost to unplanned repairs at each of the 14 depots in each half of the assessment year.
  *Device:* a job re-opened after a failed road test is logged as a new job carrying its parent's number, as the workshop guide
  documents. Counting it separately double-counts the overlap days, overstating 19 of the 28 cells by 4% to 15%.
* **Ask B (device-carried).** Tyres replaced per 100,000 km for each of the nine models. *Device:* the tyre contract logs a pair fitted
  on one axle as one job line with quantity 2. Counting lines understates every model, and the error varies with each model's pair share,
  so it reorders five models.
* **Ask C (validity).** Each model's demonstrated share and its total distance against total fuel under each of the four rung
  constructions.
* **Decoupling.** The workshop system and the tyre contract share no row with the telematics feed or the card ledger. Clearing the
  lowest-consistent rule changes no figure in asks A or B.

## 11. Rubric arithmetic

14 depots × 2 halves (ask A) + 9 models (ask B) + 9 models × 4 constructions (ask C) + the Tier 1 model and the nine tiers + 4 named chart
parts + 2 files ≈ 89 criteria.

## 12. World-building constraints

* Distances (millions of km): Torvan 9.8, Kestrel 7.4, Aldo 6.1, Vela 5.0, Corso 4.2, Brenta 3.4, Ferro 2.9, Lumo 2.6, Sabre 2.2.
* Tier 1 by rung: Torvan, Kestrel, Aldo, Vela. Shares at rung 3: Vela 1.00, Kestrel 0.82, Ferro 0.80, Brenta 0.79, Corso 0.78, Lumo
  0.77, Torvan 0.69, Sabre 0.67, Aldo 0.50, giving Tier 2 to five models and Tier 3 to three. Van counts follow distance at about
  16,500 km a van (Torvan 594, Kestrel 448, Aldo 370, Vela 303, Corso 255, Brenta 206, Ferro 176, Lumo 158, Sabre 133).
* 1,060 vans carry H2. Every one of their card-minus-telematics litres falls between November and March. The fleet's annual gap is 1.9%,
  and the parallel run shows no gap above 0.5%.
* Kestrel runs only from southern depots and carries no fuel-fired heaters. Its relief vans' dual-gateway reporting holds 18% of its
  units above target until the post-transfer distance is counted once, under either file.
* North-7 and South-3 are identical on every telematics column, and their heater options differ.
* The workshop system and the tyre contract touch no fuel or distance record.
