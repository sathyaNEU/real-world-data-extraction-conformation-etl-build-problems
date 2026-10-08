# RC37 — How many points of saving each point of tiered standard bought, when a third of the suppliers had already imposed their own restrictions

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · water resources regulation |
| Mirrors | Measuring a platform-wide mandate after some units adopted their own version first (company-wide policies at Google and Meta after some organisations moved early, app-store rules after some developers complied ahead of the deadline), where early adopters' steps look like a pre-trend |
| Decision shape | One figure committed at a date (a component): the tiered mandate's own savings slope, filed in the board's rulemaking record on reusing tiers |
| Committed call | The points of conservation saving per point of assigned standard that the tiered mandate caused, to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · a latent attribution marker assigns a treatment no field records, an exact run in the enforcement fields, graded as a component, not a correction |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #17 guesses an attribution the data can settle · #20 leaves the deciding comparison unstated · #26 picks a window across a documented confounder |
| Calibration form | Gold-standard verification subsample: the state's audit of 40 suppliers' local restriction ordinances, with stages and adoption months verified from council records |
| Driving force | In the year before the state mandate, 120 suppliers, mostly high-baseline inland systems, adopted their own mandatory restrictions at staggered dates. No report field records them. Every one of them, and no other supplier, filed enforcement warnings in three or more consecutive months from the month its ordinance took effect. Read as a smooth pre-trend, those staggered steps put the tier slope at 0.71 before trend adjustment and 0.48 after. Entered as staggered treatment dated by the warning run, they give 0.55. |

## 1. Situation

After the drought, the state water board must decide whether its next emergency regulation reuses tiered standards. The last one assigned
suppliers reductions from 4% to 36% according to their 2013 residential use per person. The board's evaluation found a steep slope from
assigned standard to achieved saving. An economist told the board that the high-standard suppliers were already cutting before the
mandate. The rulemaking record needs one figure: the saving each point of standard actually caused. The board chair believes the tiers
did the work.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: monthly supplier reports, assigned standards, enforcement fields and the audited ordinance
  records. The economist is right that high-standard suppliers were cutting early, and the board is right that the tiers caused savings.
  The figure quantifies the tiers' share. No one's reading of their own figures is overturned.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair and the economist. The event study still shows a pre-period drift, and the textbook responses (ignore
  it, or detrend it) still miss.
* **Instrument repair.** Suspect: no supplier report records a local ordinance. Repair: add a field dating each supplier's ordinance. Rung 0
  still returns 0.92, rung 1 0.71 and rung 2 0.48, because none of them treats part of the pre-period as treated. Entering the ordinances as
  a second, staggered treatment is still needed to reach 0.55. The repair makes the warning-run dating unnecessary, and the
  staggered-treatment construction carries the call.
* **Lens swap.** The naive comparison treats the pre-period as untreated. The answer dates a different treatment, local ordinances from July
  2014 to March 2015, inside that window.

## 3. The driving force

A strong solver throws out the board's cross-sectional slope, because standards were assigned on baseline use. It fits the intensity
difference-in-differences with supplier and region-by-month effects. It reads the event study and notices that no pre-period quarter is
significant on its own, but jointly they drift down for high-standard suppliers. So it adds supplier-specific trends, which is the
economist's correction, and the slope falls to 0.48. But the drift is not a trend. It is 120 local ordinances taking effect at different
months, each a step of about 12%. A straight line through a step overcorrects, because it carries the step forward as a slope through the
mandate period. No field names these suppliers, but the enforcement fields do it exactly: a supplier under an ordinance files warnings
every month from adoption, while elsewhere warnings come singly, after complaints. Dated by the first month of a run of three or more,
the ordinances enter as their own staggered treatment, and the tiers' slope is 0.55.

## 4. The ladder

| Rung | Construction | Lands on (points per point of standard) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Cross-sectional slope of post-period saving on assigned standard | 0.92 (+67%) | The board's evaluation, cleanly computed | Standards were assigned on 2013 use, so the cross-section confounds assignment with response |
| 1 | Intensity difference-in-differences with supplier and region-by-month effects | 0.71 (+29%) | The textbook design, with weather absorbed | The pre-period event-study coefficients, read jointly rather than one at a time |
| 2 | The deciding comparison: the joint pre-period test fails, so supplier-specific linear trends are added | 0.48 (−13%) | Parallel trends restored, which is the economist's correction | The audited ordinances: the drift is staggered 12% steps, which a straight line carries forward as slope |
| 3 | **Decisive:** local ordinances dated by each supplier's warning run and entered as staggered treatment | **0.55** | — | — |

* **Figure shape.** Corrections walk the slope down (0.92, 0.71, 0.48). The decisive move reverses the last one, and the answer sits
  between the two textbook estimates, closer to neither.
* **Partial correction priced (L3).** Rung 2 sits 0.07 away. Dating ordinances only for the 40 audited suppliers gives 0.66. Dating them by
  the first month with any warning, which complaint-driven warnings put one to four months early, gives 0.43. Dating them by structural
  breaks in residential use gives 0.64. Each half-insight lands further away than rung 2.
* **Grid.** Pre-period handling (none, linear trends, or ordinances dated by the run, by audit only, by any warning or by break) × weather
  effects (region-by-month or none) = 12 cells. The nearest wrong cell is rung 2, 13% away.
* **Which guard binds.** A figure, so separation binds. Per-rung offsets are +67%, +29% and −13%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** No document lists the local ordinances outside the audit's 40, and no document says enforcement fields date them.
2. **The audit pins a construction, not a menu.** The warning-run rule reproduces all 40 audited adoption months exactly. First-warning
   dating reproduces 31, and structural breaks reproduce 29 to within a month. Run lengths from three to six give the same 120 suppliers and
   dates, because no unmandated supplier has a run longer than one month and every mandated supplier's run lasts at least seven.
3. **No arithmetic symptom.** Production, population, residential share and enforcement counts reconcile on every rung. The 40 audited
   ordinances agree with the reports.
4. **Not a row predicate.** A run is a property of a supplier's monthly sequence, and its first month dates the treatment. A single month's
   warnings say nothing.
5. **The enumeration is arithmetic.** Eighty of the 120 ordinances appear in no record but the run.
6. **No cutover date.** The ordinances start in nine different months. The state mandate's date is the one every textbook design already
   uses.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The state's ordinance audit: 40 suppliers, each with its local restriction stage and adoption month verified from council
  minutes.
* **What it pins.** The dating rule, 40 of 40 against the best rival's 31. The rivals' misses all run early, so each also biases the slope in
  one direction.
* **Twin pair.** Ridgemont and Las Palmas Valley are identical on 2013 baseline, standard (28%), region, population and cumulative saving by
  the end of the mandate. Their post-minus-pre changes were −4.9 and −9.8 points (2.0×), because Ridgemont's ordinance took effect in August
  2014 and Las Palmas's in February 2015. Only the warning-run dates reproduce both.
* **Resemblance points at the decoy.** The audited 40 are the state's largest urban systems, which adopted early and close together, so in
  the subsample the pre-period looks like a smooth decline that a trend would absorb.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's terms of reference: "The record states the saving each point of assigned standard caused." The reporting
  manual defines the enforcement fields: "warnings issued under the supplier's own rules this month".
* **Empirical pins.** The dating rule comes from the audit. The ordinance effect, about 12%, is estimated from the dated steps.
* **Voices.** Board chair: "Look at the slope; the tiers did exactly what they were built to do." Economist: "High users were already
  cutting; take their trend out and the effect halves." Inland supplier association: "Our members did what the state asked, when it asked."
* **Licensed wrong basis.** The terms record that the governor's drought task force reads the mandate's effect from the board's
  cross-sectional evaluation and will cite that slope at the hearing.

## 8. Determinism by construction

* **Outcome and window.** Residential use per person in logs, against the same month of 2013, from June 2014 to February 2016. Values outside
  20–600 gallons are set missing, and no supplier with an ordinance has a missing month.
* **Ordinance effect.** Entered as a step from the run's first month. Steps that phase in over two months change the slope by under 0.01.
* **Overlap.** Once the state mandate starts, a supplier under an ordinance is treated by both, additively. Interacting the two changes the
  slope by 0.01.
* **Clustering.** Standard errors are clustered by supplier, and the committed figure is the point estimate.
* **Maturity.** Every report through February 2016 is final, with no revisions after the extract.

## 9. Prompt sketch and deliverables

> The board decides next month whether the next emergency regulation reuses tiered standards, and the record needs one figure from me: how
> many points of saving each point of assigned standard actually caused, to two decimals. Our chair is certain the tiers did the work. Give
> me the figure in a sentence for the record, with `tier_effect.xlsx`, a chart `tier_event_study.png`, and a one-page `rulemaking_note.pdf`.

* `tier_effect.xlsx` — the slope on every construction, the recycled-water sheet (ask A), the water-loss sheet (ask B) and the pre-period
  evidence (ask C).
* `tier_event_study.png` — quarterly event-study coefficients for the plain design and the staggered-treatment design, with ordinance
  adoption months as a rug. The mandate start is a labelled line, and the title states the committed slope.
* `rulemaking_note.pdf` — the committed figure and why the cross-sectional and detrended slopes differ from it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Recycled-water deliveries by hydrologic region and quarter across the window. *Device:* suppliers
  report recycled water in acre-feet or million gallons with a units field, as the reporting manual states. Summing unconverted values
  understates deliveries in the four regions where most suppliers use acre-feet. Recycled water never enters residential use.
* **Ask B (device-carried).** Real losses for each of the 40 audited suppliers from their validated water-loss audits. *Device:* the audit
  method expresses losses per connection per day for dense systems and per mile of main per day for sparse ones, by a density rule the
  method guide documents. Mixing the two misstates 14 of the 40.
* **Ask C (validity).** Each pre-period quarter's coefficient in the plain design and the joint comparison across them.
* **Decoupling.** Clearing the ordinance dating changes no figure in asks A or B. Ask C belongs to the plain design.

## 11. Rubric arithmetic

10 regions × 2 years (ask A) + 40 suppliers (ask B) + 4 quarters and the joint test (ask C) + the committed slope, the ordinance count and
the ordinance step + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* 400 suppliers with standards of 4% to 36%. 120 ordinances, each a step of about 12%, adopted between July 2014 and March 2015, 40 of them
  audited.
* Every ordinance supplier files warnings for at least seven consecutive months from adoption, and every other supplier's warnings are
  isolated months.
* Slopes: cross-section 0.92, plain 0.71, detrended 0.48, answer 0.55. Partials: audit-only 0.66, first warning 0.43, structural break 0.64.
* Ridgemont and Las Palmas Valley are identical on every report column except their ordinance months.
* The audited 40 are urban systems that adopted between July and October 2014.
* Units fields and audit density classes never touch residential use or enforcement fields.
