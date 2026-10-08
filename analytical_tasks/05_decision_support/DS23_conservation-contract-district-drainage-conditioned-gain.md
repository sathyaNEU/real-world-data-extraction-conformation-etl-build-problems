# DS23 — Which irrigation district gets the reservoir's conservation contract, when water saved on a field reaches the reservoir only where its drains do not

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · water resource management |
| Mirrors | Paying for savings that count only where the saved resource would not have come back anyway (Google and Microsoft watershed-replenishment credits, Amazon data-centre water stewardship, utility efficiency programmes where the saved energy rebounds) |
| Decision shape | Which of N gets one scarce thing: the water authority's single on-farm conversion contract this year, $10.0M of drip conversions in one district |
| Committed call | The district that gets the contract, and the water a year it adds to the reservoir, in acre-feet to the nearest hundred |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield: the pooled saving reaches the reservoir only where drainage does not return it), with a latent district marker on shared-turnout deliveries (#17) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #17 guesses an attribution the data can settle · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: last year's water-accounting close-out, every diversion, delivery and gauged drain flow by subbasin reconciled to the reservoir balance, covering the programme's first 40 contracts |
| Driving force | The authority funds the contract where it adds the most water to the reservoir per dollar. A converted acre cuts applied water by its district's over-application, and that saving is real at the farm. But a field whose drains run back to the river above the reservoir was already returning most of that water. Joined to the drainage map by subbasin, last year's close-out splits absolutely: 95% of a saving reaches the reservoir where drains run to the closed sump and 5% where they run to the river. Last year's contracts sat mostly over river drains, so the pooled 45% applies to nobody, and Saltbush's flood acres lie almost all over the sump. |

## 1. Situation

A water authority must keep its reservoir above the protection level, and this year it can fund one $10.0M on-farm conversion contract
(flood to drip) in one of six irrigation districts: Cottonwood, Riverbend, Orchard Flats, Sand Ridge, Saltbush and Tablelands. The programme
rules fund the contract where it adds the most water to the reservoir per dollar. The authority holds the conversion pilot's results (1.4
acre-feet of applied water saved per converted acre, pooled), each district's conversion cost per acre, the delivery records and the
districts' water-order books, the settled water bills, last year's water-accounting close-out with its drain gauges, and the drainage map.
The general manager wants the contract where the most water is wasted.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The pilot's 1.4 acre-feet, the delivery records, the
  bills, the close-out and the drainage map are all right. The difficulty is that the reservoir gains only the share of a farm saving that
  was not already flowing back to it, and that share is set by where each field drains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the general manager's view. Over-application per dollar, with every delivery attributed correctly, still names
  Orchard Flats, and every figure ties to the delivery records and the bills.
* **Instrument repair.** The suspect file is the delivery record, which leaves the district blank on 18% of deliveries at the turnouts the
  Main Canal shares between Riverbend and Saltbush. Filled, rung 1 lands on rung 2's Orchard Flats, and rungs 0 and 2 stay at Cottonwood and
  Orchard Flats; no lower rung names Saltbush. The pilot, the close-out, the drain gauges and the drainage map are complete, and no field
  claims a district's reservoir gain, so the destination split is still needed.
* **Lens swap.** The naive read prices water saved at the farm. The answer prices the water that reaches the reservoir, a different
  population of flows: drainage that was not already returning.

## 3. The driving force

A strong solver sets aside the pilot's pooled saving, because the delivery records show applied water per flood acre ranging from 3.1 to
5.4 acre-feet across districts, and it prices each district's over-application against its conversion cost. It attributes the unassigned
deliveries at the shared turnouts by matching each to the same-day, same-volume order in one district's order book, which reproduces every
settled bill. Each step is competent, and Orchard Flats leads. But the authority buys reservoir water, not farm savings. Where a field's
drains return to the river above the reservoir, cutting its applied water mostly cuts its return flow, and the reservoir sees about 5% of
the saving. Where drains run to the closed Saltbush Sink, the saving stays in the river, about 95%. The close-out, joined to the drainage map
by subbasin, shows exactly that split, and last year's contracts sat 70% over river drains, which is why the pooled ratio is 45%. Orchard
Flats drains 90% to the river; Saltbush's flood acres lie 95% over the sump. Its $10.0M adds 5,900 acre-feet a year.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The pilot's pooled saving (1.4 acre-feet per acre) per dollar of conversion cost | A, Cottonwood (1.00 acre-feet per $1,000) | The authority's own pilot and its own cost schedule | The delivery records: applied water per flood acre ranges from 3.1 to 5.4 acre-feet, so over-application differs by district |
| 1 | Each district's over-application from deliveries, the unassigned shared-turnout deliveries split by acreage | B, Riverbend (1.30) | District-specific savings from the authority's own meters | The settled bills: the acreage split reproduces 2 of 6, and matching each delivery to the same-day, same-volume order reproduces 6 of 6 (#17) |
| 2 | Deliveries attributed through the order books | C, Orchard Flats (0.86) | Every delivery attributed, every bill reproduced | The close-out joined to the drainage map: 95% of a saving reaches the reservoir over sump drains, 5% over river drains |
| 3 | **Decisive:** reservoir gain = over-application × the destination ratio of the subbasins under each district's flood acres, per dollar | **E, Saltbush (0.59)** (5th of 6 on rung 0) | — | — |

* **Position table.** Saltbush is 5th on rung 0 (0.54), 6th on rung 1 (0.35, its deliveries split away to Riverbend) and 3rd on rung 2
  (0.65, 1.32× behind Orchard Flats). It leads only rung 3, 1.56× over Cottonwood (0.38). Rung margins: 1.43, 1.51, 1.23, 1.56.
* **Discriminator dominance.** Orchard Flats carries a 1.32× advantage into rung 3 (0.86 against 0.65). On the decisive axis, the share of a
  saving that reaches the reservoir, Saltbush sits at 0.905 and Orchard Flats at 0.14, an edge of 6.46. Product: 6.46 / 1.32 = 4.89, the
  final margin between them (0.59 against 0.12), against a required 1.2 × 1.32 = 1.58.
* **Partial correction priced (L3).** The destination split applied to the pilot's pooled saving names Cottonwood (0.59 against
  Saltbush's 0.49, 1.21×). The split with deliveries divided by acreage names Cottonwood (0.38, 1.21× over Saltbush's 0.31). Conditioning
  on crop, the close-out's visible column, names Orchard Flats (0.54, 1.64× over Saltbush). Last year's realised ratio by district, with the
  pooled 45% for Saltbush, which had no contract, names Cottonwood (1.29×). No half lands on Saltbush.
* **Grid.** Saving (pilot pooled, deliveries by acreage, deliveries by order) × reservoir share (none, by crop, by destination) gives 9
  cells, naming A, A, A, B, C, A, C, C and E. Only order-matched deliveries with the destination split name Saltbush. Its nearest wrong
  cells are one toggle away and name Cottonwood at 1.21×, costing the order matching or the delivery records.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The programme rules say "water added to the reservoir". The pilot report gives a farm saving, and no document says a
   saving over river drains was already reaching the reservoir.
2. **No sweepable corpus nominates it.** *In the close-out every contract's applied-water cut equals the cut in its turnout deliveries,
   whatever its subbasin, because the meters sit at the turnouts.* Every group-by on the contract file's own columns (district, canal, crop,
   size) returns ratios near the pooled 45%, and the split appears only when contracts are joined to subbasins and subbasins to drain gauges.
3. **No arithmetic symptom.** Diversions, deliveries, drain flows and the reservoir balance reconcile under every rung, and the pooled ratio
   is exactly the close-out's.
4. **Not a row predicate.** It needs each district's flood acres joined to subbasins on the drainage map, each subbasin's destination ratio
   from the gauged drains, an acreage-weighted ratio per district, and the product with over-application and cost.
5. **The enumeration is arithmetic.** No column records reservoir gain; Saltbush's 0.905 falls out of the join.
6. **No cutover date.** Drainage destinations are fixed by the drain network, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Last year's water-accounting close-out: every diversion, turnout delivery and gauged drain flow by subbasin, reconciled monthly
  to the reservoir balance, with the programme's first 40 contracts and their applied-water cuts.
* **What it certifies.** Over sump drains the river kept 95% of each cut, and over river drains 5% (drain return fell by 95% of the cut).
  70% of last year's contracted acres were over river drains, so the pooled ratio is 45%. Order matching reproduces all six settled bills.
* **What it is blind to.** Saltbush, which held no contract last year, and any district whose acres are mostly over the sump.
* **Twin pair.** Subbasins S-4 and S-9 are identical on every visible column: almonds, 640 converted acres, an 880 acre-foot cut in applied
  water. The reservoir gained 440 and 836 acre-feet (1.9×). Only the drainage map separates them: S-4's drains split between the river and
  the sump, and S-9's all run to the sump.
* **Every rule exercised.** Some subbasins drain wholly to the river, some wholly to the sump and two split, so the ratio is tested at both
  ends and in between.
* **Resemblance points at the decoy.** On crop and canal, Saltbush resembles the row-crop districts whose contracts realised the lowest
  ratios last year.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rules: the contract goes where it adds the most water to the reservoir per dollar. The cost schedule: each
  district's conversion cost per acre. The budget: $10.0M. One sentence each.
* **Empirical pins.** Destination ratios, from the close-out and the drainage map. Over-application by district, from order-matched
  deliveries.
* **Voices.** The general manager: "Fund the district that wastes the most water." The pilot's agronomist: "Drip saves water wherever we
  have tried it." The Riverbend board chair: "Our canal carries the most water; the savings are there."
* **Licensed wrong basis.** The rules record that the state water board reviews contracts on applied water saved per dollar and will see
  that basis.

## 8. Determinism by construction

* **Drainage.** Every field sits in one subbasin, and every subbasin drain discharges to the river or the sump; the two split subbasins
  carry gauged shares.
* **Orders.** Every unassigned delivery matches exactly one same-day, same-volume order, with no duplicate volumes on any day.
* **Cost and budget.** Conversion costs are filed per acre, and Saltbush has more than the 3,846 flood acres the budget converts.
* **Rounding.** Saltbush's gain is 5,917 acre-feet, filed to the nearest hundred (5,900), and no rival is within 1.5×.

## 9. Prompt sketch and deliverables

> We have $10 million for one district's on-farm conversion contract this year, to keep the reservoir off its protection level. Our
> general manager wants it where the most water is wasted. Tell me which district gets it and how many acre-feet a year it puts in the
> reservoir, to the nearest hundred, in a line for the board. Send `conservation_case.xlsx`, a chart `reservoir_gain.png`, and a one-page
> `contract_note.pdf`.

* `conservation_case.xlsx` — the six districts under each rung, the subbasin build, the rights sheet (ask A), the outage sheet (ask B) and
  the validity sheet (ask C).
* `reservoir_gain.png` — for each district, applied water saved per $1,000 split into the part reaching the reservoir and the part already
  returning, with the chosen district highlighted, and an inset of the close-out's subbasins (applied cut against reservoir gain) coloured
  by drain destination.
* `contract_note.pdf` — the committed district and figure, and why the wasteful districts lose.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each district, the number of active water-right holders at season start. *Device:* a right
  split by inheritance keeps the parent record beside two child records with its priority date, as the rights register documents. Counting
  every record overstates three districts by 6–10%.
* **Ask B (device-carried).** Monthly outage hours on each canal last season. *Device:* an outage running past midnight is logged as two rows
  with a continuation flag. Counting rows as outages, rather than summing hours per outage, double-counts the long ones.
* **Ask C (validity).** Each district's settled bill under acreage-split and order-matched attribution (hits), and each district's figure
  under the four rungs.
* **Decoupling.** Clearing the destination split and the order matching changes no figure in asks A or B. Rights and outages never enter a
  delivery, a drain flow or a ratio.

## 11. Rubric arithmetic

6 districts × 4 rungs + 6 bills × 2 attributions (ask C) + 9 grid cells + 6 rights counts (ask A) + 3 canals × 6 months (ask B) + the
committed district, its gain and the runner-up + 5 named chart parts + 3 files ≈ 80 criteria.

## 12. World-building constraints

* Conversion cost ($k per acre): Cottonwood 1.4, Riverbend 2.0, Orchard Flats 2.2, Sand Ridge 2.4, Saltbush 2.6, Tablelands 2.8. Pilot
  saving 1.4 acre-feet per acre.
* Over-application (acre-feet per acre), order-matched / acreage-split: 0.9 / 0.9, 1.4 / 2.6, 1.9 / 1.9, 1.3 / 1.3, 1.7 / 0.9, 1.2 / 1.2.
  18% of Main Canal deliveries carry no district; order matching reproduces 6 of 6 bills, the acreage split 2.
* Share of flood acres over sump drains: 0.60, 0.25, 0.10, 0.55, 0.95, 0.80, giving reservoir ratios 0.59, 0.275, 0.14, 0.545, 0.905,
  0.77. Crop-level ratios in the close-out: 0.50, 0.40, 0.62, 0.45, 0.50, 0.48. Last year's contracts: 70% over river drains, pooled 45%.
* Subbasins S-4 and S-9 are identical on every visible column. Rights records and outage rows never touch deliveries or drains.
