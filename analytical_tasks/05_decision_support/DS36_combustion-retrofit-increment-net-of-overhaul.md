# DS36 — Which gas turbine gets the year's combustion retrofit, when scheduled overhauls will remove most exceedances anyway

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · power generation fleet investment |
| Mirrors | Crediting an upgrade with improvements that scheduled maintenance would deliver anyway (fleet retrofits at airlines and data-centre operators, security tooling credited with incidents a planned platform upgrade removes, model refreshes credited with gains from a scheduled data migration) |
| Decision shape | Which of N gets one scarce thing: the OEM's single retrofit crew and budget this year, among six units |
| Committed call | The unit retrofitted, and the permit-exceedance hours the retrofit avoids over the next five years, to the nearest ten |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · S10, the governing verb is causal ("avoids"), so the baseline is built from the maintenance plan and overhaul-only outages, with a latent attribution marker (E19) at rung 1 |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #7 uses the ready-made measure · #17 guesses an attribution the data can settle · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: the fleet book of eight units over six years, with fired hours, exceedance hours and every outage's scope |
| Driving force | The capital plan funds the retrofit where it avoids the most exceedance hours, and avoiding is a difference against what would happen without it. Major overhauls, already scheduled, restore combustors and remove about 80% of exceedances on their own. The OEM's "91% fewer" comes from retrofits done in the same outage as an overhaul; one retrofit done alone cut 55%. The units with the most hours ahead are the ones due an overhaul. |

## 1. Situation

A utility runs six gas turbines (GT1–GT6) under an air permit that counts every hour whose average NOx exceeds 25 ppm at 15% oxygen.
The OEM can retrofit one unit's combustion system this year, and the capital plan sends it to the unit where it avoids the most permit
exceedance hours over the next five years. The compliance dashboard counts last year's exceedance hours by unit; GT3 and GT4 share one
stack and one emissions monitor. The OEM's brochure reports 91% fewer exceedance hours at the units it has retrofitted.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the monitors, the dashboard, the dispatch plan, the maintenance plan, the fleet book and the
  brochure's before-and-after counts. No stakeholder read is overturned: retrofitted units really did see 91% fewer hours. The difficulty is
  that the decision is scored on what the retrofit causes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the OEM's figure and the compliance manager's view. Projecting each unit's hours forward and applying the
  before-and-after reduction the fleet book shows at retrofitted units still names GT2.
* **Instrument repair.** Give every unit its own perfect monitor. Rung 1 falls away, and the answer does not move: the overhauls are still
  scheduled, and they still remove most of the hours the brochure credits to the retrofit.
* **Lens swap.** The naive read and the answer differ in population and moment: the hours each unit will have, against the hours it will
  have only because it was not retrofitted, a counterfactual nobody has observed.

## 3. The driving force

A strong solver attributes the shared stack's hours properly, projects each unit's exceedance hours over five years from its fired hours
and its degradation since its last overhaul, and applies the retrofit's measured effect. GT2, the unit longest since overhaul, wins:
its hours are climbing. But the plan's verb is "avoids", a difference between two futures. In both futures GT2 gets its major overhaul next
spring, as the maintenance plan schedules, and in the fleet book every overhaul alone cut the unit's hours to about 20% of what they had
been. The brochure's 91% comes from two retrofits done in the same outage as an overhaul. The third retrofit in the book, done between
overhauls, cut 55%, and 1 − 0.20 × 0.45 = 0.91 accounts for the brochure exactly. The retrofit's own effect is 55% of the hours a unit
would otherwise have, and a unit about to be overhauled will have few. GT5 is not due an overhaul for six years.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last year's exceedance hours from the dashboard, the shared stack split by each unit's load share | GT1 (410 against GT4's 330) | The regulator watches the unit with the most violations | The regulator's settled notice of violation for the shared stack names 64 hours as GT4's; the load-share split puts 23 of them on GT4 |
| 1 | Shared-stack hours attributed to whichever unit was ramping above 8 MW a minute, the marker that reproduces all 64 | GT4 (470 against GT1's 380) | The attribution the regulator itself settled | The capital plan: the retrofit is judged on hours avoided over the next five years, not hours past |
| 2 | Five-year projection from the dispatch plan and each unit's degradation since its last overhaul, times the brochure's 91% reduction for retrofitted units | GT2 (1,480 against GT4's 1,210) | Forward-looking, built on the fleet's own record | The maintenance plan: GT2 and GT4 have major overhauls inside the window, and the book's overhaul-only outages show what those do alone |
| 3 | **Decisive:** both futures include the scheduled overhauls; the retrofit's own effect (55%) separated from the overhaul's (80%) using the overhaul-only and retrofit-only outages; avoided hours are the difference | **GT5, 695 hours** (4th of six on rung 0) | — | — |

* **Position table.** GT5 is 4th on rung 0 (210, level with GT6), 4th on rung 1 and 3rd on rung 2 (1,150); it never leads and is never
  second below rung 3. Rung margins: GT1 over GT4 1.24×, GT4 over GT1 1.24×, GT2 over GT4 1.22×, GT5 over GT1 1.24× (695 against 560).
* **Discriminator dominance.** GT2 carries a 1.29× projected-reduction advantage over GT5 into rung 3 (1,480 against 1,150). GT5 keeps
  0.60 of its rung-2 figure and GT2 0.20, an edge of 3.1×, more than 1.2 × 1.29 = 1.55.
* **Partial correction priced (L3).** A solver who nets the overhauls but keeps the brochure's 91% names GT5 at 1,150 hours, the right unit
  and a figure 65% high. One who uses the standalone 55% but ignores the overhaul schedule names GT2 at 890. Neither half reaches 695.
* **Grid.** Attribution (load share, ramping unit) × retrofit effect (91%, 55%) × baseline (no overhauls, scheduled overhauls) = 8 cells.
  They name GT1, GT2 or GT4, or GT5 at 1,150; only the ramping unit, 55% and scheduled overhauls give GT5 at 695.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The capital plan says "avoids"; the maintenance plan lists dates; the book lists outages and their scope. No
   document connects overhauls to emissions or says the brochure's figure is a compound of two effects.
2. **The book pins the effects, as a construction.** Treating overhaul and retrofit as separate multiplicative effects reproduces all seven
   past outages' following-year hours within 2%: four overhaul-only (79–81% reductions), two combined (91%) and one retrofit-only (55%). A
   single retrofit factor reproduces the two combined outages and misses the other five. The construction needs the outage scope, the
   maintenance plan's dates for every candidate and two future paths per unit; it is not a setting.
3. **No arithmetic symptom.** Monitor hours reconcile to the dashboard, fired hours to the dispatch plan, and every projection is positive
   and feasible.
4. **Not a row predicate.** Avoided hours are a difference between two projected paths per unit, each composed from the degradation curve,
   the overhaul date and the retrofit effect.
5. **The enumeration is arithmetic.** No column holds an avoided figure or a counterfactual.
6. **No cutover date.** Past outages are measurement instances; the decisive fact is a schedule of future overhauls, and no series in the
   decision steps.
7. **Survives deletion.** No wrong number exists to delete. Without the OEM, the book's own before-and-after reductions still credit the
   retrofit with the overhaul's work.

## 6. The calibration corpus

* **Form.** The fleet book: eight units (the six here and two at the sister plant) over six years, with fired hours and exceedance hours by
  year, and seven outages with their scope.
* **What it certifies.** The degradation curve: exceedance hours per thousand fired hours rise at the same slope after every overhaul in
  the book, for each unit model. The ramp attribution, through the notice of violation.
* **What it pins.** The separate effects (above).
* **Twin pair.** GT5 and GT6 are identical on every dashboard, dispatch and brochure column: 210 hours last year, 6,100 fired hours a
  year, the same model and the same hours since overhaul. Retrofitted, GT5 avoids 695 hours over five years and GT6 300 (2.3×), because
  GT6's major overhaul falls next spring and GT5's in year six. Only the maintenance plan separates them.
* **Resemblance points at the decoy.** By model and hours since overhaul, GT2 most resembles the OEM's two flagship retrofits.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital plan: the retrofit goes to the unit where it avoids the most permit-exceedance hours over the next five
  years. The permit: an exceedance is an hour above 25 ppm NOx at 15% oxygen. The dispatch plan: fired hours by unit and year. The
  maintenance plan: each unit's next major overhaul.
* **Empirical pins.** The degradation slope, the overhaul and retrofit effects and the ramp marker, from the book and the notice.
* **Voices.** The OEM's sales engineer: "Our retrofit cuts exceedance hours by more than 90% wherever it goes." The compliance manager:
  "The unit with the most violations is the one the regulator watches." The maintenance planner: "Overhauls are about hot-gas-path life,
  not emissions."
* **Licensed wrong basis.** The capital plan records that the regulator's liaison will present the units ranked by last year's
  exceedance hours at the review.

## 8. Determinism by construction

* **Composition.** The retrofit-only outage pins the standalone effect, and the combined outages match the product of the two effects to
  within 1 point, so additive and multiplicative readings cannot both fit.
* **Overhaul timing.** Every scheduled overhaul falls at least two months from a year boundary, so annual and monthly projections give the
  same totals to ten hours.
* **Ramp marker.** In every shared-stack exceedance hour exactly one unit ramped above 8 MW a minute, so thresholds from 6 to 10 attribute
  identically.
* **Rounding.** GT5's 695 and GT1's 560 sit clear of the nearest-ten boundaries.

## 9. Prompt sketch and deliverables

> We fund one combustion retrofit this year, and six units are candidates. The OEM's view is that its retrofit cuts exceedance hours by
> more than 90% wherever it goes. Tell me which unit gets it and how many permit-exceedance hours it avoids over the next five years, to the
> nearest ten, as the line for the capital plan. Send `retrofit_case.xlsx`, a chart `exceedance_paths.png`, and a one-page
> `capital_plan_entry.docx`.

* `retrofit_case.xlsx` — each unit under the four rung bases with the outage reproduction table (ask C), the starts sheet (ask A) and the
  ammonia sheet (ask B).
* `exceedance_paths.png` — for each unit, five years of projected exceedance hours with and without the retrofit as paired lines, the
  scheduled overhauls marked as vertical rules, the avoided area shaded and labelled, and GT5 highlighted.
* `capital_plan_entry.docx` — the committed unit and avoided hours, and why the brochure's figure is not the retrofit's.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six units, last year's starts and median minutes from ignition to minimum load.
  *Device:* a start that trips during ignition is logged as an attempt followed by a restart under one sequence ID, as the control-system
  event guide documents. Counting attempts overstates starts at four units and shortens their median.
* **Ask B (device-carried).** For each month of last year, the plant's ammonia use per MWh at the shared stack's catalyst. *Device:*
  ammonia is recorded at delivery, when the tank is filled, and consumption is deliveries adjusted by the change in the tank-level log.
  Reading deliveries as use puts three months' consumption in the months the tanker came.
* **Ask C (validity).** Each unit's five-year avoided hours under each of the four rung bases, and the number of the seven past outages
  each effect model reproduces.
* **Decoupling.** Clearing the overhaul netting changes no figure in asks A or B. Start sequences and tank levels touch no exceedance,
  dispatch or outage record.

## 11. Rubric arithmetic

6 units × 2 (ask A) + 12 months (ask B) + 6 units × 4 bases + 3 model hit counts (ask C) + the committed unit, its avoided hours, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 63 criteria.

## 12. World-building constraints

* Rung 0: GT1 410, GT4 330, GT2 300, GT5 210, GT6 210, GT3 205. Rung 1: GT4 470, GT1 380, GT2 300, GT5 210, GT6 210, GT3 95. Rung 2: GT2
  1,480, GT4 1,210, GT5 1,150, GT6 1,150, GT1 980. Rung 3: GT5 695, GT1 560, GT6 300, GT2 290, GT4 240, GT3 150.
* Overhauls: GT2 and GT6 next spring, GT4 in year two, GT1 in year five, GT3 in year four, GT5 in year six.
* Book: four overhaul-only outages (79–81%), two combined (91%), one retrofit-only (55%). The notice names 64 shared-stack hours, all on the
  ramping unit.
* Start sequences and ammonia deliveries are independent of every main-call record.
