# AD20 — Which tool unit comes down for the fab's one engineering hold, when the units that look worst are running products whose designs pattern their own wafers

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · semiconductor fab operations |
| Mirrors | Separating a unit's own failures from what its workload would show anyway (host fault attribution in hyperscale fleets where some workloads fail on any host, CI flake attribution where some suites fail on any runner, commonality analysis in contract manufacturing where some designs carry inherent defects) |
| Decision shape | Which of N gets one scarce thing: this week's single engineering hold, one tool unit taken down for inspection |
| Committed call | The one tool unit held for inspection this week |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · a constructed counterfactual for a causal verb (E10): the standard asks which unit causes systematic loss, and each product's own qualification rate is the baseline its wafers would show on any tool; the deciding comparison (E22) at the rung below |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #7 uses the ready-made measure · #20 leaves the deciding comparison unstated · #13 validates on one population, applies to another |
| Calibration form | Pilot log: last quarter's twelve pilot holds under the new hold standard, each with its unit, the unit's product mix, its systematic share and the inspection finding |
| Driving force | The standard sends the hold to the unit causing the most systematic loss, and at wafer grain the deposition chamber that runs only product K looks worst at 62.4%. But K's edge ring is a design signature: its qualification lots carried it on 60% of wafers, on every tool, and every product has its own rate (Q's centre spot 50%, M 4%, P 8%). A unit's share mostly reflects what it runs. Subtracting each wafer's product rate, the counterfactual the product engineering file supplies, leaves CMP head 2, whose scratch arcs mark a third of what it polishes, at 27.1 points against 17.8 for the next unit; setting aside only K's familiar edge ring names the Q-heavy implant source instead. |

## 1. Situation

A wafer fab can take one tool unit down for an engineering hold this week. Its hold standard gives the hold to the unit whose processing
causes the most systematic loss over the last 14 days, measured on the unit's wafers whose final-test maps show a systematic pattern
(join-count z of 3 or more with at least five failing dies). Four products run in the window. The pack carries the 14 days' wafer maps,
the MES lot history, the tools' chamber logs (every wafer by unit), the product engineering file (each product's qualification lots and
their pattern rates), the fault-detection log, the fab's pattern-to-tool reference table, the maintenance log and the pilot log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: every map, lot record, chamber-log line, qualification lot and pilot finding. The deposition
  chamber's 62.4% is exactly its wafers' patterned share. Nothing reported is overturned and no stakeholder read is corrected; the
  difficulty is how much of a unit's patterned share its products would carry on any tool.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the reference table. The wafer-grain systematic share, the natural careful build from the maps
  and the chamber logs, still names C.
* **Instrument repair.** No file the ladder uses is suspect: the maps, the lot history and the chamber logs record every wafer and every
  unit it passed, and the product file holds every product's qualification rate. The pattern flag records spatial clustering, which K's edge
  ring and Q's centre spot genuinely are, and the pattern-to-tool table is a generic guide, not a record of these wafers; no field claims to
  record which unit caused a pattern. Perfect files leave rung 0 at D (684), rung 1 at C (62.4%) and rung 2 at F (52.0%), so the excess over
  each wafer's product rate is still needed for E.
* **Lens swap.** The naive population is every patterned wafer a unit processed; the answer's is the patterning in excess of what each
  wafer's product shows on any tool, a different population, near zero for C and 27 points of everything CMP head 2 polishes.

## 3. The driving force

A strong solver turns away from counts of patterned wafers, which follow throughput, because the standard compares patterned with
processed wafers. It builds each unit's systematic share at wafer grain from the maps and the chamber logs and finds the deposition
chamber that runs only product K on top at 62.4%. Each step is competent, and the deciding comparison is stated. Then the product file
shows K's edge ring on 60% of its qualification wafers, on every tool, and the solver sets K's edge rings aside as design; the Q-heavy
implant source rises to the top at 52.0%. But every product carries its own design signature: Q's centre spot sat on half its
qualification wafers, M's and P's patterns on 4% and 8%. The standard's verb is causal, and what a unit causes is the patterning beyond
what its wafers' products show anyway. Subtracting each wafer's product rate, unit by unit, leaves the deposition chamber at 2.4 points,
the implant source at 4.3, and CMP head 2 at 27.1: its worn pad conditioner leaves scratch arcs on a third of everything it polishes, mostly
low-pattern products whose raw shares looked ordinary.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Patterned wafers per unit over 14 days, from the maps and the chamber logs | D, CMP head 1 (684; 1.30× B) | The loss itself, unit by unit, every wafer placed | The hold standard compares a unit's patterned wafers with all it processed; D's 684 are 40% of the 1,722 it polished, the fab's busiest unit |
| 1 | Systematic share: patterned over processed wafers per unit | C, deposition chamber (62.4%; 1.20× F) | The standard's comparison, stated and computed at wafer grain | The product file: K's qualification lots carried the edge ring on 60% of wafers on every tool, and C runs only K |
| 2 | The share with K's edge rings set aside as design | F, implant source 2 (52.0%; 1.25× E) | The known design pattern removed, every other pattern charged to the tool | The pilot log: four holds at units whose share sat at their products' qualification rates found nothing, and F runs 95% Q, whose qualification lots carried the centre spot on half their wafers |
| 3 | **Decisive:** each unit's share in excess of its wafers' product qualification rates, wafer by wafer | **E, CMP head 2 (27.1 points)** (4th of 9 on rung 0) | — | — |

* **Position table.** E ranks 4th on rung 0 (440), 3rd on rung 1 (47.4%) and 2nd on rung 2 (41.5%, 1.25× behind F), and leads only rung
  3, 1.52× I (17.8). Intermediate leaders hold margins of 1.30×, 1.20× and 1.25×.
* **Discriminator dominance.** F carries a 1.25× advantage over E into rung 3 (52.0% against 41.5%). The product baseline keeps 0.65 of E's
  figure and 0.08 of F's, an edge of 7.99 against the 1.2 × 1.25 = 1.50 required, 5.3× headroom.
* **Partial correction priced (L3).** A solver who subtracts one fab-wide rate (42.4%) from every unit instead of each product's own names
  C (20.0 points against F's 9.6, 2.08×; E 5.0). A solver who sets aside only K's edge ring, the design pattern everyone knows, names F
  (52.0% against E's 41.5%, 1.25×). A solver who applies the product baselines at lot grain, where the two CMP heads share every lot and
  head 2's excess is diluted to the pair's 9.5, names I (17.8, with A next at 17.7). No half lands on E.
* **Grid.** Grain (lot or wafer) × baseline (none, fab-wide, K only, every product) gives eight cells: no-baseline and fab-wide cells name
  C, K-only cells name F, and every-product baselines name I at lot grain and E only at wafer grain. The nearest wrong cell (I) needs only
  the chamber logs left unread.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard asks what a unit causes and measures patterned wafers. Nothing says products pattern on their own,
   and the qualification rates sit in a product file kept for yield forecasting.
2. **The corpus pins a construction, not a menu.** Excess over the product mix's qualification rates reproduces all twelve pilot findings:
   faults at the five held units 24 points or more above their baseline, none at the seven 19 or fewer above. Raw shares reproduce 5 of 12
   and the K-only correction 8, both by holding units whose products carried the patterns. The construction weighs each wafer against its
   own product's rate across a unit's mix, and no column holds a unit's excess.
3. **No arithmetic symptom.** Maps tie to final test, the chamber logs to the tools' wafer counters, and every share reconciles.
4. **Not a row predicate.** It needs every wafer joined to its unit and its product, a baseline per product from another file, and a
   weighted excess per unit.
5. **The enumeration is arithmetic.** Which unit causes the most excess is computed; no field marks a pattern as tool-made.
6. **No cutover date.** The conditioner has worn steadily since before the window, and every product's mix holds across it; no series
   steps.
7. **Survives deletion.** With every voice and the reference table removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The pilot log: twelve holds taken last quarter under the new standard, each with the unit held, its product mix, its systematic
  share, the inspection finding, and that period's maps and chamber logs.
* **What it pins.** A fault was found at every held unit whose share stood 24 points or more above its products' qualification rates and
  at none standing 19 or fewer above; no held unit fell between.
* **Twin pair.** Pilot holds H-04 and H-09 are identical on systematic share (51%), wafers (1,300), unit type (CMP head) and days since
  maintenance (12). Their excess over their product mixes was 26 and 13 points (2×): H-09 polished mostly a design-patterned product.
  Inspection found a worn pad conditioner at H-04 and nothing at H-09.
* **Every rule exercised.** One held unit ran a single product, so the baseline is that product's rate alone; one ran four products, so the
  weighting by mix is tested.
* **Resemblance points at the decoy.** By share and unit type C most resembles the pilot's one confirmed fault at a deposition chamber.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The hold standard: the hold goes to the unit whose processing causes the most systematic loss over the last 14 days,
  measured on wafers whose maps show a systematic pattern. The yield manual's pattern flag. The product file's qualification rates are the
  product engineers' record of each design's patterns.
* **Empirical pins.** The excess over each product's qualification rate, and its split between 19 and 24 points, from the pilot log.
* **Voices.** The yield manager: "Hold whichever unit is putting out the most patterned wafers." The deposition module lead: "Edge rings
  come from deposition; every fab knows it."
* **Licensed wrong basis.** The standard records that the customer's quality team audits holds on each unit's raw systematic share and
  will review this week's on that basis.

## 8. Determinism by construction

* **Baselines.** Qualification rates, each product's rate on the step's other units, or its fab-wide rate all leave E first, the last
  by the widest margin, because every other unit's excess falls toward zero; the counterfactual converges.
* **Wafer identity.** Every wafer's scribed ID is read at every step, so the maps, the lot history and the chamber logs join on wafer ID.
* **Window.** The 14 days are filed; 10 or 21 days keep E first by at least 1.4×.
* **Pattern flag.** No wafer sits within 0.2 of the join-count line or within one die of the five-die minimum.

## 9. Prompt sketch and deliverables

> The fab has one engineering hold this week: one tool unit comes down for inspection. Our yield manager wants it on whichever unit is
> putting out the most patterned wafers. Name the unit in a line for the hold notice, with `hold_choice.xlsx` holding the sheets below,
> the chart `excess_over_design.png`, and a short `hold_notice.pdf`.

* `hold_choice.xlsx` — every unit's patterned count, raw share, product mix and excess over its products' qualification rates, the
  maintenance sheet (ask A), the starts sheet (ask B) and the pilot back-test (ask C).
* `excess_over_design.png` — the nine units' raw shares as bars with each unit's product baseline drawn inside, the excess labelled, and the
  twin pilot holds shown as an inset.
* `hold_notice.pdf` — the committed unit and why C and F are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine units, maintenance hours in the last quarter and the mean time between
  maintenances. *Device:* a maintenance that runs across a shift change is logged as two records linked by a continuation ID, per the
  maintenance system's guide. Counting records doubles those maintenances and shortens the mean interval at four units. The hold build
  never reads the maintenance log.
* **Ask B (device-carried).** For each of the four products, wafer starts in the window and the share on priority lots. *Device:* a lot split
  into child lots keeps its parent's start date and gains a suffix, as the MES guide documents. Counting child lots as starts overcounts
  the two products split most.
* **Ask C (validity).** For each of the four rung constructions, the pilot findings it reproduces out of 12.
* **Decoupling.** Clearing the product baselines changes no figure in asks A or B.

## 11. Rubric arithmetic

9 units × 2 (ask A) + 4 products × 2 (ask B) + 4 constructions (ask C) + the committed unit, its excess and the margin over I + 5 named
chart parts + 3 files ≈ 41 criteria.

## 12. World-building constraints

* Product mix of the window's 2,650 wafers: K 30%, Q 25%, M 30%, P 15%; qualification rates K 60%, Q 50%, M 4%, P 8%.
* CMP head 2 polishes 928 wafers (K 15%, Q 15%, M 45%, P 25%) and scratches 34% of them; head 1 polishes the rest cleanly.
* Raw shares: C 62.4, F 52.0, E 47.4, G 43.2, D 39.7, B 37.6, H 34.5, I 24.2, A 23.7. Excess: E 27.1, I 17.8, A 17.7, H 13.9, B 11.2,
  G 8.6, F 4.3, C 2.4, D 0.
* Rung leaders are D, C, F, E. E is 4th / 3rd / 2nd (1.25×) / 1st; E leads rung 3 by 1.52×.
* The pilot log holds twelve holds; H-04 and H-09 are identical on every unit-level column but their product mix.
* Continuation maintenance records and child lots never touch the maps, the chamber logs or the product file.
