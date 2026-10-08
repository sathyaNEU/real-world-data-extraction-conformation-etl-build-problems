# FC41 — The next six-month order of adult HIV treatment, when the children of a scale-up five years ago are about to grow into it

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · public-health commodity procurement |
| Mirrors | Buying for an installed base whose members migrate between product lines at a property each unit reaches on its own clock (device trade-ups when a cohort ages out of a support tier, account seats graduating from a starter plan, parts demand when a fleet cohort crosses a service threshold) |
| Decision shape | One figure committed at a date: the cycle order, in bottle-months of adult TLD |
| Committed call | The adult TLD order for cycle C7 (January–June), filed at the national quantification review |
| Gap · Pattern | Gap 1 (time) over Gap 4 (rule) · S4, the forward window generated under a regime the closed window never reached, with Pattern B for the switch rule |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #5 takes the population a flag suggests · #4 never tests its reading against the control |
| Calibration form | Revision log: the regimen-switch log of every patient who changed formulation in the closed cycles |
| Driving force | Adult demand reads as a clean trend because, in every closed cycle, almost no children crossed the switching weight. A paediatric cohort enrolled in a scale-up five years ago now crosses it in waves. Its size comes only from fitting each child's own weight trajectory, and its timing from a switch rule written nowhere but recoverable from the switch log. |

## 1. Situation

The Central Medical Stores (CMS) files the order for adult TLD at the quantification review in three weeks. The SOP holds the stock plan to a
5% probability of a national stock-out before the first C7 arrival. Six closed cycles of adult consumption show steady growth of about 4% a
cycle, and the quantification lead's cohort model reproduces them well. The paediatric programme sits with a different team, and its
register has never been part of quantification.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: adult consumption, the ART register, the paediatric register's weights and visits, the switch log. No
  claim about anyone's own numbers is overturned. The difficulty is that the population buying adult TLD in C7 is not the population that
  bought it in C1–C6.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Remove the lead's note and every voice. The adult series still extrapolates cleanly, and nothing in the pack says
  children will join it.
* **Instrument repair.** Make every register perfect and complete. The wave is still in the future, so nothing about it can be read from a
  better instrument of the past.
* **Lens swap.** The naive read and the answer are different populations: patients already on adult TLD in closed cycles against those
  joining in C7.

## 3. The driving force

The obvious unit is "patients on adult TLD", and the history of that unit is exemplary. But whether a child is on adult TLD is an
eligibility state reached when a child's weight crosses a threshold. The children who will cross it in C7 were enrolled five years ago, in a
scale-up that put 2,400 children aged 3 to 6 on treatment within two years. In the closed cycles that cohort weighed under 25 kg, so it left
no mark on adult consumption. To see it, a solver has to open a register it has no reason to open. It then has to fit each child's own
growth trajectory from repeated visit weights, which is a fit within units, and apply a switch rule that only the closed switch log reveals.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Adult consumption trend (six cycles) × months covered + safety stock to the 5% clause | 29% below the answer | Textbook consumption method; growth is smooth and the fit is excellent | The ART register shows adult enrolment from testing outpacing the trend's implied growth |
| 1 | Hygiene: patients transferred between facilities counted once, not as active at both sites in the transfer month | 35% below | A real double count is fixed, and every count now reconciles to the register | Cohort projection on the register (rung 2) explains closed cycles better than the trend |
| 2 | Cohort model: adult actives × retention curve + new adult enrolment at the testing yield | 18% below | Reproduces all six closed cycles to within 0.4% | The paediatric register shows children whose weights will cross the switching weight inside C7 |
| 3 | **Decisive:** add paediatric transitions, from each child's within-child weight trajectory and the switch rule recovered from the switch log | **The answer** | — | — |

* **Figure shape.** The answer is the maximum cell of the grid, so every partial application under-orders.
* **Partial correction priced (L3).** A solver who adds transitions by projecting the cohort's mean weight curve, not each child's, lands
  24% below. The mean crosses 30 kg two cycles later than the fast-growing third of the cohort does. A solver who switches children on the
  day they cross 30 kg, ignoring the visit rule, lands 9% above the answer, because nobody switches between visits.
* **Grid.** Hygiene × cohort model × transitions (mean or individual) × switch timing (crossing date or rule) = 16 cells. The nearest
  non-answer cell is 9% away and needs a switch timing the corpus refutes in 38 of 41 cases.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The dosing table (shipped as background, disclaimed) gives weight bands. No document links paediatric growth to adult
   ordering, and no document states when a child switches.
2. **Corpus blind to the wave's size.** *In every closed cycle fewer than 150 children crossed the switching weight, because the scale-up
   cohort was then aged 6–9 and under 25 kg.* The switch log pins the timing rule but carries too few switches to show any wave.
3. **No arithmetic symptom.** Adult consumption, issues and register counts reconcile on every rung.
4. **Not a row predicate.** Projected crossing needs a within-child fit across repeated visits, followed by a count over children whose
   projected crossing falls before their next scheduled visit in C7.
5. **The enumeration is arithmetic.** Which children switch in C7 is computed, not flagged; no column says "transitioning".
6. **No cutover date in any outcome series.** The scale-up is five years old and stepped no consumption series; the wave lives only in the
   forward window.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The regimen-switch log: 41 children who moved from paediatric to adult formulation during C1–C6, each with their visit dates and
  recorded weights.
* **What it pins (Pattern B).** The switch happens at the first scheduled visit on or after the visit where weight is at least 30.0 kg. 41
  of 41 switches reproduce under that rule. The rival "switch at crossing date" fits 3 of 41, and "switch at the next cycle start" fits 9.
* **What it cannot show.** The size of the coming wave (above).
* **Twin pair.** Two districts identical on adult actives, retention, enrolment and testing yield, whose C7 orders differ 2.1× because one
  hosts the scale-up's paediatric sites.
* **Free training instance (O3).** One district ran an early paediatric programme, and its small wave passed in C5. It is visible in that
  district's consumption and harmless, because the district held eight months of stock.
* **Resemblance points at the decoy.** C7's adult demand profile most resembles C6, a cycle the cohort model reproduced to 0.2%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The SOP fixes the 5% service level. The ART guideline (shipped as background) carries the dosing bands as a table, with no
  narrative about transitions.
* **Empirical pins.** The switch rule (first scheduled visit at or above 30.0 kg) is recovered from the switch log. Visit schedules come from the
  paediatric register's appointment fields.
* **Voices.** The quantification lead: "Children are the paediatric team's budget line, not ours." The paediatric programme manager: "Our
  kids switch when they're ready, it's a clinical call" (true, and the log shows how).
* **Licensed wrong basis.** The SOP records that the donor's quantification guideline forecasts adult products from adult consumption alone,
  and that the donor will present it at the review.

## 8. Determinism by construction

* **Growth-fit form.** Every child has at least four weight visits, and the world is built so linear and quadratic within-child fits
  produce the same set of children crossing inside C7.
* **Visit-schedule drift.** Children with missed visits are rescheduled one month later in the register, so the "next scheduled visit"
  field resolves without a convention.
* **Demand windows.** Six-, nine- and twelve-month adult demand windows converge for the rounded order.
* **Maturity.** All six closed cycles are fully reported, and the extract date falls between visit weeks.

## 9. Prompt sketch and deliverables

> I have to read one adult TLD order for C7 into the minutes of the quantification review on the 18th, rounded to the nearest thousand
> bottle-months, with our 5% stock-out ceiling met. The lead believes adult consumption is all we need to look at. Send me `c7_order.xlsx`
> holding the order build and the district sheet, a chart `c7_demand_path.png`, and a one-page `c7_order_note.pdf` that commits to the
> figure.

* `c7_order.xlsx` — the order build, the per-district sheet (ask A) and the facility reconciliation (ask B).
* `c7_demand_path.png` — monthly adult TLD demand from C1 to C7: actuals, the adult-cohort projection and the paediatric transitions as a
  stacked series, with the cohort crossing month annotated.
* `c7_order_note.pdf` — the committed order and the alternatives a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 district stores, the adult TLD bottle-months that will expire before use under
  first-expiry-first-out issuing at current consumption, worst first, with batch numbers. *Device:* three batches carry an expiry
  extension, filed in a separate certificate register. A solver reading label expiry over-counts expiry in five districts.
* **Ask B (device-carried).** For the last complete month, each district's months of stock, and the facilities whose report and stock card
  disagree by more than 5%. *Device:* inter-facility transfers post on the stock card and report a month later, as the reporting manual
  says. A naive comparison flags eleven facilities; the right answer is two.
* **Ask C (validity).** The C7 order under each of the four rung constructions, with each one's probability of a national stock-out.
* **Decoupling.** Clearing the transition wave changes no figure in asks A or B.

## 11. Rubric arithmetic

14 districts × 2 figures (ask A) + 14 × 2 (ask B) + 4 constructions × 2 (ask C) + the committed order, the transition count and the margin
to the 5% line + 5 named chart parts + 3 files ≈ 75 criteria.

## 12. World-building constraints

* The scale-up enrolled about 2,400 children aged 3 to 6 within two years. Each child has at least four weight visits. Growth trajectories
  are heterogeneous, with a fast-growing third crossing 30 kg about two cycles before the cohort mean.
* Fewer than 150 crossings fall in any closed cycle. The 41 logged switches all obey the first-visit-at-or-above-30.0-kg rule.
* Rung figures are fixed at −29% / −35% / −18% / answer, and no cell of the 16-cell grid sits within 9% of the answer.
* The twin districts are identical on every adult-side field. The early-programme district's C5 wave is visible and harmless.
* District batches, expiry extensions and stock-card transfers are independent of every quantity in the order build.
