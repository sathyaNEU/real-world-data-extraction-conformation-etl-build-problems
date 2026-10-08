# DS12 — Which corridor gets the five-year pavement warranty contract, when the contractor accepts a corridor only if every section outlives the term

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · public works asset management |
| Mirrors | Placing a scarce performance-guarantee contract where the counterparty underwrites the weakest component, not the average (cloud provider SLAs priced on the worst availability zone, Apple and Amazon supplier warranties accepted only if every lot passes, fleet maintenance contracts that exclude a whole depot for one failing unit) |
| Decision shape | Which of N gets one scarce thing: this year's single performance-based preservation contract |
| Committed call | The corridor that gets the contract, and its lifecycle saving over the five-year term, in $M to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units recovered from the counterparty's acknowledgements (Pattern B), with deterioration curves validated on the Interstates and applied to arterials (#13) at rung 2 |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #13 validates on one population, applies to another · #4 never tests its reading against the control · #3 stops at a close but inexact match · #14 coarsens the segment it was asked about |
| Calibration form | Counterparty acknowledgement file: the warranty contractor's accept or decline on 38 past corridor nominations, with each nomination's section data |
| Driving force | The contractor underwrites a corridor only if every one of its sections stays above the warranty trigger for the full five years. Its acknowledgements never state that, and corridor averages cannot reproduce them at any threshold. Remaining life is a construction: each section's traffic run through the arterial deterioration curves to the trigger. Hollins Road, the best corridor on lifecycle saving, has one 400 m section over a culvert with 3.1 years left, so the contractor would decline it. |

## 1. Situation

A state DOT can place one performance-based preservation contract this year. The contractor treats one corridor and guarantees its
condition for five years. The preservation policy sends the contract to the corridor with the largest lifecycle saving over the term among
corridors the contractor will accept. Six arterial corridors are candidates. The DOT has its section inventory with condition histories
and traffic, the pavement manual's deterioration curves, the annual condition report, the contract's warranty trigger, and the
contractor's acknowledgements of 38 past nominations from this DOT and two neighbouring states. The district engineers want the contract on
the worst corridor.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the inventory, the manual's curves (exact
  on the Interstates they were fitted to), the condition report, the trigger and every acknowledgement. The difficulty is the acceptance
  rule. It is a minimum over sections of a constructed quantity, and the contractor has never written it down.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the district engineers' view. Lifecycle saving on class-calibrated curves still names Hollins Road, and every
  figure reconciles.
* **Instrument repair.** Survey every section perfectly. The culvert section's subgrade still gives it 3.1 years, and the contractor's
  decision still turns on the worst section, not the corridor.
* **Lens swap.** The naive read ranks corridors on their own savings. The answer first applies the counterparty's underwriting, which is
  decided by a different population (each corridor's weakest section).

## 3. The driving force

A strong solver sets aside worst-first, computes each corridor's lifecycle saving from the manual's curves, then recalibrates the curves
by functional class, because the condition report shows arterials cracking faster after year six than the Interstate curves allow. Each
step is competent, and Hollins Road wins at $12.8M. But the saving exists only if the contractor accepts the corridor. Its 38
acknowledgements give accept or decline and nothing else. Corridor-average rules cannot reproduce them: mean remaining life tops out at 27
of 38 at every threshold from six to eleven years, a flat loss curve. Worst-section cracking reaches 31. One rule reproduces all 38: every
section's remaining life to the trigger, under the arterial curves and that section's own traffic, must cover the five-year term. Hollins
Road's culvert section has 3.1 years and Pell Street's worst has 3.8, so both would be declined. Garrow Avenue's weakest section has 7.2
years, and it leads every accepted corridor.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Lane-miles below good condition, worst first | A, Ashby Parkway (42) | The commission's own condition measure | The policy: the contract goes on lifecycle saving over the term, not on current deficiency |
| 1 | Lifecycle saving from the pavement manual's curves | B, Pell Street ($14.2M) | The department's standard method, applied correctly | The condition report: arterials crack faster after year six than the Interstate-fitted curves allow |
| 2 | Lifecycle saving on curves recalibrated by functional class (#13) | C, Hollins Road ($12.8M) | The right curves for the right roads | The acknowledgement file: one rule reproduces all 38, and under it Hollins Road's culvert section (3.1 years) gets it declined |
| 3 | **Decisive:** keep only corridors whose every section's remaining life to the warranty trigger, under the arterial curves and its own traffic, covers five years; rank those on saving | **E, Garrow Avenue ($10.4M)** (4th of 6 on rung 0) | — | — |

* **Position table.** Garrow Avenue is 4th on rung 0 (26 lane-miles), 4th on rung 1 ($9.1M) and 2nd on rung 2 (1.23× behind Hollins Road).
  It leads only rung 3, 1.24× over Dunmore Road ($8.4M). Rung margins: 1.20, 1.23, 1.23, 1.24.
* **Discriminator dominance.** Hollins Road carries a 1.23× saving advantage into rung 3. On the decisive axis, the weakest section's life
  against the term, Garrow Avenue stands at 1.44× and Hollins Road at 0.62×, a 2.32× edge. Product: 0.81 × 2.32 = 1.89, so no curve or
  trigger convention rescues Hollins Road.
* **Partial correction priced (L3).** Applying the every-section rule on the manual's Interstate curves lengthens every section's life,
  admits Pell Street (5.6 years) and Hollins Road (5.2), and names Pell Street, which is rung 1's decoy. A corridor-mean rule admits Hollins
  Road (mean 8.0 years). A worst-cracking rule admits it too, because the culvert section cracks little and fails underneath.
* **Grid.** Curves (Interstate, arterial) × acceptance (ignored, corridor mean, worst cracking, every-section life) gives 8 cells. They
  name B, B, B, B, C, C, C and E. The nearest wrong cell is the every-section rule on Interstate curves (Pell Street), and it costs one
  omission: the condition report.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The contract gives the trigger and the term. No document states the contractor's underwriting rule or says a
   single section decides a corridor.
2. **The reproducing rule is a construction, not a menu.** Every-section remaining life reproduces 38 of 38. The best rival, worst-section
   cracking, reproduces 31 at its best threshold, and corridor-mean life 27 at every threshold from six to eleven years. The winning rule's
   input is not a column: each section's remaining life is a projection of its own traffic through the class curve to the trigger, and the
   rule is then the minimum of that over the corridor's sections.
3. **No arithmetic symptom.** Sections, lane-miles, traffic and savings reconcile under every rung. The acknowledgements give no reason
   codes to contradict anything.
4. **Not a row predicate.** It needs a per-section projection joined to traffic counts, then a minimum inside each corridor, compared
   with the term.
5. **The enumeration is arithmetic.** No column says a section will hit the trigger early, or that a corridor is underwritable.
6. **No cutover date.** The acknowledgements span six years of nominations with a stable rule, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The acknowledgement file: 38 nominations, each with its sections' condition, traffic and class at nomination, and the
  contractor's accept or decline.
* **What it pins.** The minimum-over-sections rule on class-calibrated curves, 38 of 38. On the manual's Interstate curves the same rule
  reproduces 33 of 38, which also pins the recalibration.
* **Twin pair.** Two past nominations are identical on every corridor-level column: 14 km, 22 sections, mean cracking 6.1%, mean
  remaining life 8.2 years, 18,000 vehicles a day, both arterials. One was accepted and one declined. The declined corridor holds a 400 m
  sag section with 3.4 years left, and no corridor-level rule reproduces both.
* **Every rule exercised.** Four nominations were declined for a single section, and three were accepted with a weakest section between
  5.6 and 6.0 years. No nomination's weakest section falls between 4.6 and 5.4 years, so the threshold is pinned without a fork.
* **Resemblance points at the decoy.** On every corridor-level column Hollins Road looks like the accepted nominations.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The preservation policy: the contract goes to the corridor with the largest lifecycle saving over the term among
  corridors the contractor will accept under warranty. The contract: a five-year term with a cracking or roughness trigger. The pavement
  manual: its curves, noted as fitted on the Interstate network. One sentence each.
* **Empirical pins.** The acceptance rule, from the acknowledgements. Class curves, from the condition report.
* **Voices.** The district engineer: "Fix the worst roads first." The asset manager: "The manual's curves are the department standard." The
  programme analyst: "A corridor in fair shape on average is a safe warranty."
* **Licensed wrong basis.** The policy records that the state transportation commission ranks corridors on lane-miles below good and will
  see that basis.

## 8. Determinism by construction

* **Remaining life.** The trigger is filed (15% cracking or roughness of 170). The class curves come from the condition report's published
  progression by class, and every section has a traffic count.
* **The gap.** The weakest-section lives of current candidates sit at 3.1, 3.8 and 2.2 for the declined corridors and 5.9 or more for the
  accepted ones, all clear of 4.6–5.4.
* **Saving.** A 4% discount rate and the residual-value rule are filed in the policy, and savings use the same curves as acceptance.
* **Sections.** Inventory section boundaries are fixed, and the milepost equations never split a candidate section.

## 9. Prompt sketch and deliverables

> We can place one performance-based preservation contract this year, and the district engineers want it on the worst corridor. Tell me
> which corridor gets it and the lifecycle saving it buys over the five-year term, in millions to one decimal, in a sentence for the
> commission briefing. Send `corridor_case.xlsx`, a chart `section_life.png`, and a one-page `commission_brief.docx`.

* `corridor_case.xlsx` — the six corridors under each construction, the resurfacing sheet (ask A), the crash sheet (ask B) and the
  acknowledgement sheet (ask C).
* `section_life.png` — one strip per corridor showing every section's remaining life under the arterial curves, the five-year term as a
  labelled reference line, each corridor's saving printed at the strip's end, and the culvert section on Hollins Road annotated.
* `commission_brief.docx` — the committed corridor and saving, and why Hollins Road cannot be placed.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each corridor, lane-miles resurfaced in each of the last five years. *Device:* realignments
  changed mileposts, and the milepost-equation table maps old to new. Raw mileposts put three projects in the wrong corridor and misstate
  two corridors' totals by 9–16%.
* **Ask B (device-carried).** For each corridor, crashes per 100 million vehicle-miles over the last three years. *Device:* the safety
  manual assigns crashes within 250 ft of a ramp gore to the mainline, while the crash database codes them to the intersecting route.
  Reading the code directly understates two corridors by a fifth.
* **Ask C (validity).** The 38 acknowledgements reproduced under four rules (hits of 38), and each corridor's saving and weakest-section
  life under both curve sets.
* **Decoupling.** Clearing the acceptance rule changes no figure in asks A or B. Project mileposts and crash codes never enter a remaining
  life or a saving.

## 11. Rubric arithmetic

6 corridors × 5 years (ask A) + 6 crash rates (ask B) + 4 hit counts + 6 × 2 savings + 6 × 2 weakest-section lives (ask C) + the committed
corridor, its saving and the runner-up + 6 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Savings ($M), manual curves / arterial curves: Ashby 9.8 / 7.6, Pell 14.2 / 10.1, Hollins 11.5 / 12.8, Dunmore 8.0 / 8.4, Garrow 9.1 /
  10.4, Fenner 6.2 / 6.0. Lane-miles below good: 42 / 35 / 31 / 22 / 26 / 18.
* Weakest-section remaining life, arterial / Interstate curves: Ashby 2.2 / 3.9, Pell 3.8 / 5.6, Hollins 3.1 / 5.2, Dunmore 6.4 / 8.8,
  Garrow 7.2 / 9.5, Fenner 5.9 / 8.0.
* Acknowledgements: 38, reproduced 38 / 33 / 31 / 27 under the four rules. The twin nominations are identical on every corridor-level column.
* Milepost equations and crash codes never touch sections, traffic, curves or acknowledgements.
