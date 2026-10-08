# OS31 — Which liner string gets the one methanol dual-fuel newbuild, when the ship only runs clean until its methanol tank is spent

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · liner shipping and carbon compliance |
| Mirrors | Placing a scarce clean asset where it will actually run clean (electric trucks at depots without fast chargers, a carbon-free data-centre region whose workloads still fail over to a fossil region, a sustainable-aviation-fuel allocation at an airport only some rotations refuel at) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the newbuild joins one of five strings, replacing its oldest ship |
| Committed call | The string the newbuild joins, and the EU allowances a year it avoids from 2026 |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E22 (the deciding comparison: the replaced ship's in-scope emissions against what the newbuild still burns in scope on the same rotation), with E18 below it (the trading scheme's class list against the monitoring report's coarse voyage split) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #14 coarsens the segment it was asked about · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: nine months in which the first methanol dual-fuel ship and its fuel-oil sisters sailed string TA3's rotation in alternate weeks, with fuel by type for every leg |
| Driving force | A dual-fuel ship avoids allowances only on the legs where it actually burns green methanol. It can bunker methanol only at the two ports in the supply contract, burns it until 90% of the tank is used, then runs on fuel oil at 0.78 of the old ship's burn. On the Asia and transatlantic loops the tank is spent before the long in-scope legs; on the Med–North Europe shuttle both ends are supply ports. The allowances avoided are a net of two rotation-level quantities that no column holds. |

## 1. Situation

A container line takes delivery of one methanol dual-fuel ship in the spring. It will join one of five strings, replacing that string's
oldest ship. The company has a green-methanol supply contract at Rotterdam and Valencia. From 2026 every tonne of in-scope CO2 costs one
EU allowance. The sustainability director wants the ship on the Asia–North Europe loop, AE2, the company's biggest emitter.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the monitoring reports, the scheme's class list, the voyage records, the supply contract and the
  overlap's fuel logs. Nothing reported is overturned. The difficulty is a net of two counterfactual rotations that the pack never states
  as a quantity.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and every voice. The replaced ships' in-scope emissions still rank AE2 and TA3 first,
  and nothing says the newbuild will burn fuel oil.
* **Instrument repair.** Give every ship perfect fuel meters. The overlap already has them. What the newbuild will burn on a rotation it has
  never sailed is a construction, not a measurement.
* **Lens swap.** The answer needs the newbuild's own future fuel by leg on each candidate rotation, a different population of voyages from
  the replaced ship's past ones.

## 3. The driving force

A strong solver reads the trading scheme's class list instead of the monitoring report's coarse split, rebuilds each replaced ship's full
year on its own string from voyage records, and counts the replaced ship's in-scope CO2 as what the newbuild avoids. That makes TA3 the
answer, the transatlantic string whose old ship burns hardest in scope. But the newbuild is not a zero-emission ship. In the overlap it
bunkered at Rotterdam, burned methanol until 90% of its tank was used, part-way across the Atlantic, and finished the rotation on fuel oil
at 0.78 of its sisters' burn. What a placement avoids is the replaced ship's in-scope CO2 minus the newbuild's in-scope fuel-oil CO2 on
the same rotation. That needs a leg-by-leg sequence: supply ports, tank drawdown and each leg's scope class. On TA3 the newbuild keeps 66%
of the old ship's in-scope burn on fuel oil. On MN4, which calls at both supply ports, it keeps 4%.

## 4. The ladder

| Rung | Construction (replaced ship's in-scope CO2, kt a year) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Monitoring-report split (between EU ports 100%, to or from 50%, at berth 100%) on the replaced ship's ship-year; newbuild assumed clean | A, AE2, 62.0 (1.19× CF1) | The certified public report and the scheme's headline percentages | The scheme's class list: calls at listed neighbouring transshipment ports do not end a voyage, and outermost-region voyages are exempt to 2030 |
| 1 | The scheme's fine classes, voyage by voyage | B, AM1, 79.0 (1.23× AE2) | The authoritative class list, not the report's convenience split | Voyage records: three replaced ships spent four to five months of the year on other strings |
| 2 | Hygiene: each replaced ship's full year rebuilt on its own string's rotation | C, TA3, 75.0 (1.21× AM1) | The right classes, on the right rotation, for a whole year | The overlap: the newbuild ran on fuel oil for 85% of TA3's in-scope miles once its methanol tank was spent |
| 3 | **Decisive:** net of the newbuild's in-scope fuel-oil CO2, from a leg sequence of supply-port bunkering, tank drawdown to 90% and scope class | **E, MN4, 44.2 (1.33× AE2)** (5th of 5 on rung 0) | — | — |

* **The answer.** MN4, avoiding 44,206 allowances a year from 2026, committed as 44,000.
* **Position table.** MN4 ranks 5th on rung 0, 4th on rungs 1 and 2, and leads only rung 3. It is never 2nd.
* **Discriminator dominance.** TA3 carries a 1.63× lead into rung 3 (75.0 against 46.0). TA3 keeps 0.337 of its value as net avoidance
  and MN4 keeps 0.961, an edge of 2.85×, above 1.2 × 1.63 = 1.96.
* **The deciding comparison (#20).** For MN4, 46.0 kt replaced against 1.8 kt still burned. For AE2, 58.0 against 24.9. For TA3, 75.0
  against 49.7. The note has to state these. Replaced-ship emissions alone never decide.
* **Partial correction priced (L3).** A solver who takes the overlap's own ratio (the newbuild emitted 0.337 of its sisters' in-scope CO2
  on TA3) and applies it to every string still names TA3. A solver who gives the newbuild clean running on any string that calls at a
  supply port also names TA3.
* **Grid.** Voyage classes (report split, scheme list) × build (ship-year, string rotation) × newbuild fuel (clean, overlap ratio, leg
  sequence) = 12 cells. Every non-answer cell names AE2, AM1, TA3 or CF1. The nearest is the scheme list with the leg sequence but no
  rotation rebuild, led by AE2 at 1.15× over MN4.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The supply contract names two ports and the ship's specification gives its tank volume. No document says when the
   newbuild switches fuel or connects either fact to allowances.
2. **Corpus blind for a computable reason.** *In every overlap voyage the rotation was TA3's, so the overlap's ratio (0.337) and the leg
   sequence return identical in-scope totals for all 39 voyages.* The corpus pins the burn rule and cannot tell its pooled form from its
   sequence.
3. **No arithmetic symptom.** Fuel, distance, voyages and the certified reports reconcile on every rung, and the overlap ties to its bunker
   delivery notes.
4. **Not a row predicate.** Each candidate rotation needs an ordered leg sequence: bunkering calls, cumulative methanol drawn against 90%
   of tank volume, the fuel switch, then each remaining leg's scope class.
5. **The enumeration is arithmetic.** No column holds the newbuild's fuel on another string, and no column says where its tank runs dry.
6. **No cutover date.** Nothing steps; the overlap is one closed nine-month window on one rotation.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The overlap: 39 newbuild voyages and 117 sister-ship voyages on TA3's rotation, with fuel by type, leg and day, and the
  bunker delivery notes.
* **What it pins (Pattern B).** The newbuild burns methanol from each supply-port bunkering until 90% of the tank is used, then fuel oil,
  reproducing 39 of 39 voyages' fuel splits to the tonne. Rival rules miss every voyage: methanol on every in-scope leg, and a fixed
  methanol share per voyage. It also pins the newbuild's fuel-oil burn at 0.78 of its sisters' per nautical mile at the same speed.
* **What it cannot show.** Any other rotation's net (above).
* **Twin pair.** Overlap legs 14 and 27 are identical on every column of the voyage report: ports, distance, speed, scope class, weather
  band and cargo. The newbuild burned methanol for all of leg 14 and for 46% of leg 27, so the in-scope CO2 it avoided differs 2.2×. Leg 27
  followed a Rotterdam call at which the bunker barge was weather-bound, leaving the tank part-drawn. Only the tank sequence reproduces both.
* **Resemblance points at the decoy.** By ship size and in-scope burn, TA3's replaced ship most resembles the overlap's sister ships, so
  a solver transferring the overlap by resemblance stays on TA3.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fleet plan replaces each string's oldest ship. The supply contract delivers green methanol at Rotterdam and Valencia
  only. The scheme's class list governs scope, and from 2026 allowances are surrendered on 100% of in-scope emissions.
* **Empirical pins.** The burn rule and the 0.78 burn ratio come from the overlap. The replaced ships' full years come from voyage records.
* **Voices.** The sustainability director: "Put the cleanest ship where the dirtiest emissions are." The TA3 trade manager: "The methanol
  ship cut our string's emissions by two thirds in the trial." That is true for TA3.
* **Licensed wrong basis.** The fleet plan records that the lenders' green-loan adviser credits a dual-fuel ship with the replaced ship's
  full in-scope emissions and will review the placement on that basis.

## 8. Determinism by construction

* **Tank reserve.** The overlap's switch points cluster at 90% drawn (89.6% to 90.3%), and 85% or 95% reserves change no candidate's leg
  in which the switch falls.
* **Bunker sizes.** The newbuild fills to the same volume at every supply call in the overlap, so no partial-fill convention arises.
* **Speed.** Each candidate rotation's schedule speeds are filed, and the newbuild sails them exactly.
* **Phase-in.** All figures are for 2026 at 100% surrender, so the 40% and 70% years do not enter.
* **Rounding.** The answer, 44,206, sits 294 from the nearest thousand-allowance boundary.

## 9. Prompt sketch and deliverables

> We take delivery of one methanol dual-fuel ship in the spring, and I have to choose which string it joins, replacing that string's
> oldest ship. Our sustainability director thinks AE2 is the obvious home. Tell me which string gets it and how many EU allowances a year
> it saves us from 2026, to the nearest thousand, in one sentence for the fleet board. Send `newbuild_placement.xlsx`, a chart
> `string_allowances.png`, and a one-page `fleet_board_note.pdf`.

* `newbuild_placement.xlsx`: the five strings under the four rung bases, the leg sequences, the surcharge sheet (ask A) and the
  reliability sheet (ask B).
* `string_allowances.png`: for each string, a stacked bar of the replaced ship's in-scope CO2 split into avoided and still-burned parts,
  sorted by avoided, the chosen string highlighted and the tank switch leg named on each bar.
* `fleet_board_note.pdf`: the committed string, its allowance figure and the deciding comparison for MN4, AE2 and TA3.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each string, emissions-surcharge revenue billed per TEU in each quarter of last year.
  *Device:* credit notes for disputed surcharges post as negative lines that carry the original invoice number and the credit's own date,
  per the billing guide. Summing by posting date moves a fifth of each quarter's credits into the next quarter on the three strings with
  disputes.
* **Ask B (device-carried).** For each string, last year's share of port arrivals within 24 hours of schedule, and the count of omitted
  calls. *Device:* an omitted call stays in the schedule file as a row with the same voyage number and an omission status. Counting it as
  a late arrival halves AM1's reliability.
* **Ask C (validity).** Each string's avoided allowances under the four rung bases, and the overlap's reproduction count under the burn
  rule (39 of 39) and under the pooled ratio (TA3 only).
* **Decoupling.** Clearing the leg sequence changes no figure in asks A or B.

## 11. Rubric arithmetic

5 strings × 4 quarters (ask A) + 5 × 2 (ask B) + 5 × 4 bases + 2 reproduction counts (ask C) + the committed string, its figure, its margin
and the three deciding comparisons + 5 named chart parts + 3 files ≈ 66 criteria.

## 12. World-building constraints

* Replaced ships' in-scope CO2 (kt a year), report split and ship-year: AE2 62, CF1 52, AM1 50, TA3 44, MN4 30. Scheme fine classes:
  AE2 64, AM1 79, TA3 44, CF1 23.4, MN4 33. Rotation rebuild: TA3 75, AM1 62, AE2 58, MN4 46, CF1 23.4.
* Newbuild methanol share of in-scope fuel under the leg sequence: AE2 0.45, AM1 0, TA3 0.15, CF1 1.00, MN4 0.95. Fuel-oil burn 0.78 of the
  replaced ship's.
* Rung leaders AE2, AM1, TA3 and MN4, with margins of 1.19×, 1.23×, 1.21× and 1.33×. All twelve grid cells name as stated.
* The overlap holds 39 newbuild voyages with switch points between 89.6% and 90.3% of tank volume. Legs 14 and 27 are
  identical on every voyage-report column.
* Surcharge credits and omitted calls never touch fuel, voyages or scope classes.
