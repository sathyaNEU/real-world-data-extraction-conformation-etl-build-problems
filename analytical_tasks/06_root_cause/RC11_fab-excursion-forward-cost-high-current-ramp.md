# RC11 — Which tool gets the fab's engineering week, when the chamber that cost the excursion the most wafers is not the fault that will cost the most next quarter

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · semiconductor manufacturing yield |
| Mirrors | Excursion triage on lines whose product mix is shifting (wafer and panel lines at Apple and Google hardware suppliers, fulfilment lines at Amazon re-sorting totes between pick and pack), where the past excursion is attributed correctly and the fix is bought for a period whose items pass the faulty step on a different recipe |
| Decision shape | Which of N root causes gets the fix: one week of the yield engineering team on one tool or chamber |
| Committed call | The tool or chamber the engineering week goes to, and the failing wafers its fault would cost among next quarter's starts if left in place, with the runner-up's figure |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E08 (past exceedance against forward yield: each fault's cost among next quarter's starts, the moderator in how the period treats the wafer, I2's high-current recipe on 30% of its starts against 15% in the excursion weeks), with E22 (isolated counterfactual excess from a joint model) at rung 1 and E20 (an implicit join through the sorter's scribe-id log) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #18 joins only on the visible key · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Change-log natural experiments: fourteen closed excursions in the equipment change log, each with the chamber fixed and the yield before and after |
| Driving force | Linked to each wafer's own history through the sorter's scribe-id log, the excursion's excess failing wafers put deposition chamber D2-C first. The yield board buys next quarter. D2-C's showerhead deposit clears at its wet clean, due in the second week, and returns only late in each cycle. Implanter I2's worn aperture costs wafers only on its high-current source/drain recipe, which was 15% of its excursion-week wafers and is 30% of next quarter's starts as the new product ramps, so its pooled rate understates every forward week. Each fault's cost among next quarter's starts, from its own trajectory and recipe mix, makes I2 the costliest. |

## 1. Situation

A logic fab's sort yield fell over six weeks: 2,200 more failing wafers than the baseline rate. The yield engineering team can spend one week on one tool
or chamber: etch tool E3 (A), scanner S4 (B), CMP polisher P1's carrier head 3 (C), deposition chamber D2-C (D) or implanter I2 (E). The fab manager
suspects a focus drift on the scanner, the etch module owner points at the etch bay, and the data scientist's wafer-level model puts the CMP head on
top. The yield board's charter governs how the week is assigned. The equipment change log records every past excursion and the fix that ended it.
Next quarter's start plan ramps the fab's new system-on-chip product.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sort results, process history at every step, the sorter's log, the equipment logs, the recipe table, the
  start plan and the change log. Nobody's reading of their own numbers is overturned, and the excursion's attribution to D2-C is right. The
  difficulty is that the week is bought for next quarter's wafers, which pass the faulty steps on a different mix.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the licensed basis. The wafer-level model still attributes the excursion, on either link, to a
  tool other than I2, and its constant projection still names that tool for next quarter.
* **Instrument repair.** Suspect file: process history's lot-and-slot key, which records the slot a wafer held at each step, not the wafer.
  Repaired so that every step records each wafer's scribe id, rung 0's lot ratios still name A (lot grain, untouched), and rungs 1 and 2 both
  return D (900, the scribe-linked excess); none returns E. The answer still needs each fault's cost among next quarter's starts: I2's excess
  sits in a recipe that doubles its share next quarter, and D2-C's clears at its wet clean, and no record of the excursion weeks, however
  complete, measures next quarter's wafers.
* **Lens swap.** The naive build attributes the six excursion weeks' failing wafers; the answer counts failing wafers among next quarter's
  starts, a different population of wafers, on a different recipe mix, at a different time.

## 3. The driving force

A strong solver knows lot-level commonality is confounded by scheduling, so it fits a joint model with week effects at wafer level and compares
isolated counterfactuals, the excess failing wafers each tool accounts for with the others held fixed. Joined to process history on lot and
slot, every row matches and the CMP head leads. The CMP module's loading procedure assigns wafers to carrier positions by measured thickness,
which the sorter does by moving them between slots, so for 38% of wafers the documented key gives them a neighbour's pre-sorter history; linked
through the scribe id the sorter reads, deposition chamber D2-C leads with 900 excess wafers. That is the excursion's past, and the yield board
buys next quarter. The scanner's focus drift ended at its week-2 lens recalibration. D2-C's showerhead deposit grows with RF hours and clears at
the wet clean, due in the second week of next quarter; in each of its last four cycles the excess vanished at the clean and returned only in the
cycle's last five weeks. Implanter I2's worn aperture clips the beam only on its high-current source/drain recipe: 25% of those wafers fail
against 0.5% on the medium-current recipe, and high current was 15% of I2's wafers in the excursion weeks and is 30% of next quarter's starts.
Each fault's cost among next quarter's starts, from its own trajectory and recipe mix, puts I2 at 1,020 failing wafers, E3 at 650 and D2-C at
540.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lot-level commonality: failing-lot rate for lots through each tool against lots not through it | A, etch tool E3 (1.74×) | The standard commonality screen, run on the yield board's own lots | The week mix: E3 ran 70% of the excursion weeks' lots, and its ratio collapses with week effects |
| 1 | Wafer-level joint model with week effects, sort results joined to process history on lot and slot; each tool's isolated counterfactual excess | C, CMP head 3 (790 wafers) | Confounding removed at the finest grain, on the documented key, every row matched, the excess summing to 2,200 | The sorter log: 38% of this quarter's wafers changed slot before CMP, each with its scribe id |
| 2 | The same model with every wafer linked to its own history through the scribe id in the sorter log, projected over next quarter | D, deposition chamber D2-C (900 excursion wafers, 1,950 projected) | Every wafer carries its own past; the change log certifies the model (14 of 14 fixed chambers found) and its constant projection | D2-C's RF-hour log: its wet clean falls due in the second week of next quarter, and in each of its last four cycles the excess vanished at the clean |
| 3 | **Decisive:** each fault's cost among next quarter's starts, from its own trajectory and next quarter's recipe mix through the route | **E, implanter I2 (1,020 wafers)** (4th of 5 on rung 0) | — | — |

* **Position table.** E ranks 4th on rung 0, 5th on rung 1 and 4th on rung 2, and leads only rung 3. Rung leaders beat their runners-up by
  1.26×, 1.41×, 1.50× and 1.57× (1,020 against E3's 650).
* **Discriminator dominance.** D2-C carries a 3.60× lead into rung 3 (900 against 250 excursion wafers). The forward build multiplies I2's
  figure by 4.08 and D2-C's by 0.60, an edge of 6.80×, 1.57 times the required 1.2 × 3.60 = 4.32; the net margin over D2-C is 1.89×.
* **Partial correction priced (L3).** Each half of the forward build names a wrong tool. Projecting each tool's scribe-linked weekly excess
  over next quarter as a constant gives D 1,950 against the scanner's 1,300 (1.50×). Following each fault's trajectory (the scanner's drift
  over, D2-C's wet clean) but carrying I2 at its pooled excursion-week rate gives A 650 against D's 540 (1.20×), E 540. Taking I2 by recipe
  while carrying D2-C as a constant gives D 1,950 against E's 1,020 (1.91×).
* **Grid.** Link (lot and slot, scribe id) × forward (constant, trajectories with I2 pooled, I2 by recipe with D2-C constant, trajectories with
  I2 by recipe) gives eight wafer-level builds, and the lot ratios and the lot-level joint model (B 640) two more. Every build on the
  documented key names C, because head 3 inherits D2-C's thick wafers and its excess runs steadily; on the scribe link the constant and
  recipe-only builds name D, trajectories with I2 pooled name A, and only trajectories with I2 by recipe name E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter says "would cost among next quarter's starts"; the start plan lists products and the recipe table beam
   currents. No document says I2's fault is confined to high current, that the ramp doubles that share, or that D2-C's deposit clears at its
   wet clean.
2. **Corpus blind for a computable reason.** *Every closed excursion predates both the sorter's thickness routine and the new product's ramp,
   so in every closed case each wafer kept its slot and the fixed chamber's recipe mix held from the excursion weeks into the following
   quarter: the lot-and-slot key equals the scribe link, and a constant projection matches the yield recovered after each fix within 7%.* The
   change log certifies the wafer-level model and its constant projection, and cannot see the relink or the ramp.
3. **No arithmetic symptom.** The documented key matches 100% of rows, wafer counts tie at every step, the excess sums to 2,200 under both
   links, and the start plan ties to capacity.
4. **Not a row predicate.** Each fault's forward cost joins next quarter's start plan through the route and recipe tables to a rate measured
   on a different mix, and follows D2-C's RF-hour cycle across its wet clean.
5. **The enumeration is arithmetic.** Next quarter's failing wafers are a projection built from three files; no column holds them.
6. **No cutover date.** I2's aperture wear is steady and the new product ramps over the quarter; the dated events (the scanner's week-2
   recalibration, D2-C's wet clean) belong to decoys.
7. **Survives deletion.** With every voice gone, the wafer-level model still names the CMP head on the documented key and D2-C on the scribe
   link.

## 6. The calibration corpus

* **Form.** Fourteen closed excursions in the equipment change log, each with its weeks, the chamber or tool fixed, and sort yield before and
  after the fix, plus the full wafer-level data of each excursion's weeks and the following quarter.
* **What it certifies.** The wafer-level joint model with isolated counterfactuals: it names the fixed chamber in 14 of 14 cases, the lot-level
  joint model in 8, lot-level single-factor ratios in 5. The yield recovered after each fix matches the model's constant projection for that
  chamber within 7%.
* **What it is blind to.** The relink and the recipe ramp (above).
* **Twin pair.** Pilot lots L-4471 and L-4519 of the new product followed identical lot-level routes through identical tools and chambers in
  the same week and failed 12 and 6 wafers (2.0×). Only the wafer-level recipe log separates them: twelve of L-4471's wafers took I2's
  high-current source/drain recipe in the pilot's split and six of L-4519's, though both lots' route cards show the same step on I2.
* **Resemblance points at the decoy.** This excursion's lot-level profile matches EX-09, a closed CMP-head excursion, on product, weeks and
  failing-bin signature.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The yield board's charter: the engineering week goes to the tool or chamber whose fault, left in place, would cost the most
  failing wafers among next quarter's starts, against the baseline rate. The CMP module's loading procedure: incoming wafers are assigned to
  carrier positions by measured film thickness to balance removal rates.
* **Empirical pins.** The joint model's form, certified by the change log; each wafer's chamber from the scribe-linked history; D2-C's cycle
  from its RF-hour log; I2's rate by recipe from the recipe log.
* **Voices.** The data scientist: "Every wafer-level model I run puts the CMP heads on top." The etch module owner: "At lot level the failing
  lots all came through my bay that week; it's a scheduling story."
* **Licensed wrong basis.** The charter records that corporate quality ranks tools by lot-level commonality and will present that ranking at
  the board.

## 8. Determinism by construction

* **Baseline.** The failing-wafer rate of the eight weeks before the excursion, by product; the charter fixes the window.
* **Model.** Additive excess by tool or chamber with week and product effects; the excesses sum to the total under every link.
* **Link.** Every re-slotted wafer has exactly one sorter event with a readable scribe id; no wafer was re-slotted twice.
* **Forward.** Next quarter's 52,000 starts follow the start plan; I2 takes a quarter of them, as in the excursion weeks. Each fault's rate is
  its scribe-linked rate by recipe class; the scanner's stays at baseline after its recalibration, D2-C's follows its RF-hour cycle with the
  wet clean at 2,000 RF hours, and E3's and head 3's hold.
* **Failing wafer.** A wafer fails when its final sort bin is a failing bin, per the binning guide; retests resolve to the last test.
* **Rounding.** Failing wafers to the nearest ten; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Sort yield has been bleeding for six weeks and the yield team has one week to spend on one tool. The fab manager is sure the scanner's focus has
> drifted. Tell me which tool or chamber gets the week and what its fault will cost us in failing wafers if we leave it, set against the next
> candidate's, in a sentence for the yield board. Send `excursion_case.xlsx` and a chart `cost_by_tool.png`.

* `excursion_case.xlsx` — the five candidates under each construction, the SPC sheet (ask A), the equipment-state sheet (ask B) and the
  change-log back-test (ask C).
* `cost_by_tool.png` — paired bars of each candidate's excursion excess and its forward cost, an inset of I2's failing rate by beam current with
  each period's high-current share marked, D2-C's RF-hour cycle as a sparkline, and the committed candidate and its runner-up labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 inline metrology steps and each excursion week, out-of-control points on the SPC
  charts. *Device:* metrology records nine sites per wafer and the control charts are kept on the wafer mean, as the SPC plan documents;
  counting out-of-control sites overstates every step and reorders the worst three.
* **Ask B (device-carried).** For each of the five candidates, availability and unscheduled down events over the quarter. *Device:* the
  equipment-state log follows the industry state model, in which engineering time is neither productive nor down, as the state guide documents;
  counting engineering time as down understates availability for the two tools that ran qualification lots.
* **Ask C (validity).** For each of the fourteen closed excursions, the chamber each wafer-level construction names against the chamber fixed,
  and the recovered yield against the constant projection; and each candidate's figure under each construction.
* **Decoupling.** Clearing the forward build changes no figure in asks A or B.

## 11. Rubric arithmetic

12 steps × 6 weeks (ask A) + 5 candidates × 2 figures (ask B) + 14 excursions × 2 checks + 5 candidates × 4 constructions (ask C) + the
committed candidate, its figure and the runner-up's + 5 named chart parts + 2 files ≈ 140 criteria.

## 12. World-building constraints

* 2,200 excess failing wafers. Lot-level ratios A 1.74, B 1.38, C 1.12, E 1.02, D 1.00; lot-level joint excess B 640, A 310, C 190, E 150, D 0;
  wafer-level on the documented key C 790, B 560, D 520, A 190, E 140; scribe-linked D 900, B 600, A 300, E 250, C 150.
* 38% of this quarter's wafers re-slotted before CMP: 84% of D2-C's wafers against 23% of the rest; D2-C's wafers are 2.4× more likely than
  others to be routed to head 3.
* I2 ran 6,000 wafers in the excursion weeks, 15% on the high-current recipe, and takes 13,000 of next quarter's starts, 30% high-current;
  failing excess 25% on high current, 0.5% on medium. The scanner's excess falls entirely in weeks 1 and 2. D2-C's wet clean falls in week 2 of
  next quarter, after which its excess returns only in the cycle's last five weeks.
* Forward cost: E 1,020, A 650, D 540, C 325, B 0. Constant projection D 1,950, B 1,300, A 650, E 540, C 325; I2 pooled with trajectories
  A 650, D 540, E 540; I2 by recipe with D2-C constant D 1,950, E 1,020.
* Change log: 14 closed excursions, all before the sorter routine and the ramp; wafer-level joint model 14/14, lot-level joint 8,
  single-factor 5; constant projection within 7% of the recovered yield in every case.
* L-4471 and L-4519 identical on every lot-level column.
* SPC sites and engineering states touch no sort result, sorter event, process-history row or start.
