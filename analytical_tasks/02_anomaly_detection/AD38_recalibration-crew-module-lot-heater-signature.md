# AD38 — Which region gets the quarter's recalibration crew, when the fast-drifting sensor lot went in as unrecorded field swaps

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · industrial sensor field service |
| Mirrors | Fleet service targeting where the part that drives failure was swapped in the field and never recorded (battery-lot campaigns after repairs at Apple and Samsung, line-card swaps in installed Cisco routers, battery-module replacements in EV fleets), recovered from a signal the part itself emits |
| Decision shape | Which of N gets one scarce thing: the single recalibration crew for next quarter goes to one of five service regions |
| Committed call | The region the crew works, and the device-months outside drift tolerance it prevents before each device's next regular service |
| Gap · Pattern | Gap 2 (population: which devices carry the fast-drifting lot) over Gap 1 (time: today's drift against the coming exceedance) · a latent attribution marker (each module's boot heater resistance identifies its lot), with an implicit join (distributor manifests re-home warehouse-registered devices) below it |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #17 guesses an attribution the data can settle · #18 joins only on the visible key · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: the 1,800 devices measured against reference gas at service visits in the last 18 months, with their measured drift |
| Driving force | How fast a gas detector drifts is a property of its sensor module's lot, and 38% of devices carry a replacement module whose lot the swap log leaves blank. Every module reports its heater resistance at boot, and each lot's heater resistance sits in its own narrow band, so the lot of every swapped module is recoverable exactly from telemetry. Lot L7 drifts three times as fast as the rest, and field swaps concentrated L7 modules in region E, whose devices look healthiest today. |

## 1. Situation

A maker of fixed gas detectors has 21,000 units in service at 140 industrial sites in five service regions. Each unit's 16-sensor array
drifts; once drift passes the certified tolerance, the unit's classifier misreads gases and the customer's site must treat it as faulty. One
recalibration crew (reference gases and a technician team) can work one region next quarter, about 1,500 units. The service plan sends it
where it prevents the most device-months outside tolerance before each unit's next regular service. The company holds daily telemetry
(including boot diagnostics), the asset register, the build records, the field swap log, distributors' shipment manifests, the service
schedule and the measured drift from every service visit. The product manager points at region A's red dashboard.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the dashboard's per-feature tests, each unit's drift score, the register, the swap log (whose blank
  lot is honest: field kits are not lot-labelled) and the measured drifts. Nobody's numbers are overturned; the difficulty is an attribution
  no field records and the data can settle.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the product manager's view and the dashboard. Current drift scores, re-homed through the manifests, still name
  C.
* **Instrument repair.** Suspect files: the swap log's lot field, blank for every field-kit module (38% of units), and the asset register's
  region for distributor stock, which records the warehouse rather than the working site (24% of units). Give the swap log every module's
  lot and register every unit where it works: rung 0 still names A, which has the most units at work, rung 1 becomes rung 2 and names C,
  rung 2 names C, and none of rungs 0–2 reads a lot. Confirmed: the recorded lot makes the heater-signature recovery unnecessary, but the
  forward projection (each lot's drift rate run to each unit's next service) is still needed, because on drift already accumulated E is
  second.
* **Lens swap.** The naive population is units with high drift today; the answer's is units that will cross tolerance before their next
  service, which depends on lot. A different set of units at a different moment.

## 3. The driving force

A strong solver ignores the dashboard's red cells (128 tests per unit guarantee some), scores each unit's drift against its training
baseline, maps units to regions, notices that a quarter of units are still registered to distributors' warehouses and re-homes them through
the shipment manifests. Every step is correct, and each ranks regions by drift already accumulated. The decision buys the coming quarters,
and drift speed is set by the module's lot. The build record gives every unit's original lot, and 38% of units have since had a module
swapped from an unlabelled field kit. The book of measured drifts refuses both the build lot and any blanket rate for swapped units. Each
module's heater resistance at boot sits in a band unique to its lot (learned from the 13,000 modules whose lot is known), so every swapped
module's lot is recoverable, and L7, which drifts at three times the rate of the others, went out mostly in region E's swap kits.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Units with any per-feature drift test failing on the dashboard, by registered region: A 1,900, B 1,600, C 1,450, D 1,300, E 1,150 | A | The monitoring team's own dashboard | The telemetry: with 128 unadjusted tests per unit, 96% of units in every region fail at least one, and A simply has the most units |
| 1 | Units whose drift score is past 70% of tolerance, by registered region: B 1,240, A 1,010, C 960, E 820, D 700 | B | A joint drift score per unit, against its own baseline | The distribution agreement: units sold through distributors stay registered to the distributor's warehouse until activation, and 24% never activate |
| 2 | The same, with warehouse-registered units re-homed through the shipment manifests (serial to order to end-customer site): C 1,320, E 1,080, B 930, A 760, D 690 | C | Every unit placed where it actually works | The swap log: 38% of units carry a replacement module whose lot is blank, and drift speed differs by lot |
| 3 | **Decisive:** each unit's lot from its boot heater resistance, its lot's drift rate from the book, and the device-months it will spend outside tolerance before its next service: E 4,900, C 3,100, D 2,700, B 2,300, A 1,800 | **E** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.22×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.19×, 1.23×, 1.22× and 1.58×.
* **Discriminator dominance.** C carries a 1.22× advantage in at-risk units into rung 3, so the required edge is 1.2 × 1.22 = 1.46×. E's
  forward device-months per at-risk unit are 4.54 against C's 2.35 (1.93×), because 46% of E's at-risk units carry L7 against 9% of C's: an
  edge 1.32× the requirement, and a net of 1.93 / 1.22 = 1.58×.
* **Partial correction priced (L3).** A solver who sees the swaps but gives every swapped module the fleet-average drift rate names D, whose
  swaps are slow lots that the average overstates, while the average hides E's L7: D 3,400 against C's 2,850 (1.19×), E at 2,500. A solver
  who reads the heater signature but leaves warehouse-registered units where they are registered names B, which is credited with 260 of E's
  field units still registered to its distributor's warehouse: B 4,000 against E's 3,200 (1.25×).
* **Grid.** Region link (registered or re-homed) × lot (build record, fleet average for swaps, heater signature) × horizon (today's drift or
  forward exceedance) = 12 cells. Today's-drift cells name B (registered) or C (re-homed); registered forward cells name B; re-homed
  forward cells name C with the build lot, D with the fleet average, and E only with the heater-signature lot.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** Boot diagnostics are documented as a power-on self-test. No document connects heater resistance to lots, and the
   swap log's blank lot column is explained only as "kit not lot-labelled".
2. **The corpus pins a construction, not a menu (Pattern B).** Drift rates by heater-signature lot reproduce all 1,800 measured drifts
   within 0.05 of tolerance. The build-record lot reproduces 1,116, and a fleet-average rate for swapped units 1,340; both under-predict
   every L7 swap, so both miss the book's total. The assignment is a band map learned from known-lot modules and applied to swapped ones,
   not a parameter on a list.
3. **No arithmetic symptom.** Every unit has a build lot, every swap has a serial, register counts tie to manifests, and the build-lot drift
   rates reproduce every unswapped unit exactly.
4. **Not a row predicate.** It needs a lot map learned across 13,000 modules, applied to 8,000 swapped ones, then a per-unit drift
   projection to its own next service date.
5. **The enumeration is arithmetic.** Which units carry L7 is computed; no column holds it for swapped units.
6. **No cutover date.** Swap kits went out over three years; no regional series steps.
7. **Survives deletion.** Remove both voices and the dashboard, and the re-homed drift ranking is still the natural build.

## 6. The calibration corpus

* **Form.** The book of 1,800 service visits in the last 18 months: each unit's serial, months in service, module history and drift measured
  against reference gas.
* **What it pins.** Lot-specific linear drift rates, L7 at 3.1× the others, reproduce every measurement once swapped modules carry their
  heater-signature lot.
* **The absolute split (O2).** Nine lots, nine heater-resistance bands with gaps of at least 4 ohms between them, and all 13,000 known-lot
  modules inside their own band.
* **Twin pair.** Units 4471-0932 and 4471-1208 are identical on every register column (model, build lot, install month, site type, region,
  last drift score). Their measured drifts at service were 0.31 and 0.64 of tolerance, 2.1× apart, because 1208's swapped module reads in
  L7's heater band.
* **Resemblance points at the decoy.** On every register column E's units resemble the serviced units with the slowest measured drift
  (recent installs of the best build lot).

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The service plan: the crew goes where it prevents the most device-months outside certified tolerance before each unit's
  next regular service. The service schedule's next-visit dates. The distribution agreement's registration practice. One sentence each.
* **Empirical pins.** Lot drift rates, from the book; the heater-band map, from known-lot modules.
* **Voices.** The product manager: "Region A's dashboard has been red since spring; that is where the drift is." The service director:
  "Drift is drift; send the crew where today's scores are worst."
* **Licensed wrong basis.** The service plan records that the certification body's surveillance auditor counts units outside tolerance at
  the last telemetry read, by registered site, and will review the plan on that basis.

## 8. Determinism by construction

* **Lot bands.** Disjoint bands with 4-ohm gaps make nearest-band, interval and classifier assignments identical for every swapped module.
* **Drift form.** Linear and quadratic drift in months of service give the same set of units crossing tolerance before their next service,
  because no unit's projected crossing falls within two weeks of its service date.
* **Re-homing.** Every warehouse-registered serial appears in exactly one shipment manifest, with one end-customer site.
* **Crew capacity.** E's units outside tolerance before service number 1,380, inside the crew's 1,500, so the capacity does not cut the
  answer; the committed figure is rounded to the nearest 100 device-months.

## 9. Prompt sketch and deliverables

> Next quarter's recalibration crew can work one region, and the monitoring team has had region A's dashboard on red since spring. Tell me
> which region gets the crew and how many device-months outside tolerance it saves us before those units' next service, to the nearest
> hundred, in a line for the service plan. Send `crew_case.xlsx`, a chart `drift_by_lot.png`, and a one-page `crew_memo.pdf`.

* `crew_case.xlsx` — the five regions under each rung's basis (ask C), the response-time sheet (ask A) and the factory sheet (ask B).
* `drift_by_lot.png` — measured drift against months in service for the 1,800 serviced units, coloured by heater-signature lot with L7's
  steeper line labelled, the tolerance line drawn, and a second panel of each region's forward device-months.
* `crew_memo.pdf` — the committed region and figure, and why each other region falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each region, median and 90th-percentile days from a service request to technician arrival last
  year. *Device:* the CRM logs requests in the site's local time and arrivals in UTC, as the CRM guide says, and four regions span time
  zones; subtracting raw stamps misplaces a fifth of same-day arrivals. The crew decision never uses CRM records.
* **Ask B (device-carried).** For each of the nine module lots, factory sensitivity at final test and the share of modules inside
  specification. *Device:* the test specification was revised after lot 5, and lots 6–9 record sensitivity as a ratio to a reference module
  rather than in millivolts, as the revision note says; comparing raw values fails every module of lots 6–9.
* **Ask C (validity).** Each region's figure under each of the four rung bases.
* **Decoupling.** Clearing the heater-signature lots and the re-homing changes no figure in asks A or B.

## 11. Rubric arithmetic

5 regions × 2 (ask A) + 9 lots × 2 (ask B) + 5 regions × 4 bases (ask C) + the committed region, its device-months, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.22× behind C) and 1st.
* 38% of units carry a swapped module; 46% of E's at-risk units and 9% of C's carry L7. L7 drifts at 3.1× the other lots.
* 24% of units are registered to distributor warehouses; each appears in one manifest. 260 at-risk units working at E's customers are
  registered to B's distributor and carry 1,700 of E's 4,900 forward device-months. Under the fleet-average rate: D 3,400, C 2,850, E 2,500.
* Twins 4471-0932 and 4471-1208 are identical on every register column.
* CRM records and factory test records never touch telemetry, the swap log, manifests or the service book.
* Re-homed through the manifests, A still has the most units at work.
