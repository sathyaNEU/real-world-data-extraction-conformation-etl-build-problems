# OS06 — What next year's whole-home retrofit track will verifiably save, when half the homes in its pipeline were under-heated before and will take the retrofit as warmth

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · utility energy-efficiency programmes |
| Mirrors | Projecting a programme's measured per-user effect onto a new cohort when the effect is all-or-nothing on a behaviour visible only in each user's own history (smart-thermostat savings at Google Nest that vanish for households already rationing heat, battery-saver features that do nothing for light users, engagement nudges at Meta that move only users above a usage baseline) |
| Decision shape | One figure committed at a date: verified first-year savings for next year's track, filed in the annual efficiency plan |
| Committed call | The track's verified first-year site-energy savings next year, in GWh to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern E (conditioned yield on a property built by a fit within each home), with Pattern D (project and dwelling-unit grains, both flawless) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #2 counts file rows instead of the real unit |
| Calibration form | Prior-period close-out: last programme year's evaluated close-out, 2,380 projects with their packages, units and verified first-year savings |
| Driving force | Verified savings split absolutely on how each home was heated before. Homes whose pre-retrofit bills show a heating slope below 0.020 kWh per degree-day per square foot were rationing heat and verified almost nothing, because they took the retrofit as warmth; every other home verified about 42%. The slope is a fit within each home from 24 monthly bills against degree-days, reached from the pipeline list through billing and weather, and no column carries it. Last year's participants were 6% under-heated; next year's pipeline, drawn mostly from the bill-assistance referral list, is 55%. |

## 1. Situation

A utility runs a whole-home retrofit track (insulation, air sealing, duct sealing and a heat pump as one package). Its annual efficiency
plan, due at the commission on 1 March, must state the verified first-year savings next year's track will deliver. The plan targets
4,000 dwelling units: 3,000 in single-family homes and 1,000 in duplexes and triplexes, all already in the scheduled pipeline. Last
year's evaluated close-out reports 2,380 projects and 21.4 GWh. The utility holds two years of monthly bills for every premise. The
programme director is confident next year will look like last year, only bigger.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the deemed single-measure values, the close-out's verified savings, the unit counts, the bills and
  the weather. No stakeholder read is overturned. The difficulty is which yield applies to next year's homes, and that is fixed by a
  property of each home's own history.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. The close-out still offers a clean per-unit savings rate, every visible segment of the
  pipeline matches last year's, and the rate transports in arithmetic.
* **Instrument repair.** Meter every home's heating use directly. Under-heated homes still verify nothing, and next year's pipeline still
  holds nine times their share.
* **Lens swap.** The naive read is last year's participants' yield. The answer is the yield of a different population, next year's
  homes, conditioned on how they heated before.

## 3. The driving force

A strong solver knows single-measure savings do not add up in a package, so it uses the close-out's verified package savings. It sees
that the close-out's headline is per project while the plan counts dwelling units, and divides by units, building type by building type.
It checks visible segments (income flag, size, vintage, contractor) and finds the pipeline matches last year on all of them. Every step is
correct, and the result is 30.6 GWh. But verified savings are all-or-nothing on one thing: whether the home was rationing heat before.
A home whose bills barely respond to cold weather is kept cool to save money, and after the retrofit its occupants simply heat the home;
it verifies about 0.2 MWh. Last year 6% of units were like that. Next year's pipeline comes mostly from the bill-assistance referral list,
and fitting each pipeline home's own bills shows 55% are.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Sum of the deemed single-measure savings (13.6 MWh a unit) × 4,000 units | 54.4 GWh (+262%) | The plan's own method and the commission's deemed values | The close-out: verified package savings average 9.0 MWh a project, a third below the summed singles |
| 1 | Close-out savings per project × the plan's 4,000 | 36.0 GWh (+140%) | Verified, interactive and in the evaluator's own headline | The plan counts dwelling units, and the close-out's 2,380 projects hold 2,800 units; duplex and triplex units save 5.2 MWh each against 8.5 |
| 2 | Close-out savings per dwelling unit, by building type, × next year's units | 30.6 GWh (+104%) | Right grain, standardised for building type, and every visible segment of the pipeline matches last year | The pipeline homes' own bills: 55% have heating slopes below 0.020 kWh per degree-day per square foot, against 6% last year |
| 3 | **Decisive:** per-unit savings conditioned on each home's bill-fitted heating slope (0.2 or 9.0 MWh single-family, 0.1 or 5.5 multi-unit), × next year's units by slope class | **15.0 GWh** | — | — |

* **Figure shape.** Every correction walks the figure down and the answer is the minimum cell. The decisive move removes 51% of the rung-2
  figure.
* **Partial correction priced (L3).** A solver who spots the near-zero projects in the close-out and conditions on them, but carries last
  year's 6% share instead of fitting the pipeline's bills, lands exactly on rung 2. One who conditions on the income flag finds no
  difference: in last year's close-out income-qualified homes verified slightly more (9.3 against 8.9 MWh a project).
* **Grid.** Savings basis (summed singles, close-out package) × grain (project, dwelling unit) × yield (pooled, slope-conditioned) gives 8
  cells. The nearest wrong cell is the conditioned yield at project grain, 17.7 GWh (+17.6%), which costs counting projects against a
  target filed in dwelling units. Summed singles conditioned lands at 24.5 GWh (+63%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The evaluator's method note describes the billing analysis. No document says savings depend on how a home was
   heated before, and the pipeline file has no heating-behaviour field.
2. **The close-out pins the split by construction, not by menu.** Per-unit savings conditioned on the fitted slope reproduce all 2,380
   projects within 5%. The pooled per-unit rate ties the close-out total, as any average of it must, yet misses every one of the 144
   under-heated projects about fortyfold and the West cohort by 84%, so it fails row by row. The line is drawn by the data: no home in
   either year has a slope between 0.020 and 0.031, so no threshold is chosen, and the slope is a fit within each home rather than a
   column a solver can scan.
3. **No arithmetic symptom.** Verified savings tie to the close-out total, units tie to the building file, and next year's 4,000 units tie
   to the pipeline.
4. **Not a row predicate.** Each home's slope needs its 24 monthly bills joined to the weather station's degree-days and fitted, then a
   share computed over the pipeline, then savings recombined by slope class and building type.
5. **The enumeration is arithmetic.** Under-heating is computed for 4,000 pipeline units; nothing flags it.
6. **No cutover date.** Slopes are stable across both pre-period years, and the referral channel is a recruitment source, not an event.
7. **Survives deletion.** Removing the director's view and the deemed values leaves the close-out certifying a pooled rate.

## 6. The calibration corpus

* **Form.** Last year's close-out: 2,380 projects (2,100 single-family, 280 duplexes and triplexes holding 700 units), each with its
  package, contractor, units and verified first-year savings, plus the participants' pre-period bills.
* **What it certifies.** Package savings (9.0 MWh a project, 7.65 a unit, 21.4 GWh in all), and conditioned yields of 9.0 and 0.2 MWh a
  single-family unit and 5.5 and 0.1 a multi-unit unit, normal against under-heated.
* **What it cannot show.** Next year's mix: last year's 6% under-heated share is a fact about last year's recruits.
* **Twin pair.** Contractor cohorts East and West (120 single-family projects each) are identical on size, vintage, fuel, income flag
  and package. East verified 8.6 MWh a unit and West 4.6, 1.9× apart, because 5 of East's homes and 60 of West's were under-heated.
  Only the bill-fitted slope separates them.
* **Resemblance points at the decoy.** Next year's pipeline is heavier in income-qualified homes, and last year's income-qualified homes
  verified the most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The commission's order: the plan states verified first-year site-energy savings, and the track's target and savings are
  counted per dwelling unit. The pipeline schedule: 4,000 units next year, 3,000 single-family and 1,000 multi-unit. The evaluator's
  method note: savings are verified by billing analysis against twelve months of post-retrofit bills.
* **Empirical pins.** Conditioned yields and the slope split, from the close-out and the bills.
* **Voices.** The programme director: "Next year is last year, only bigger." The income-programmes lead: "Our low-income homes always
  save the most; they have the leakiest houses."
* **Licensed wrong basis.** The commission's order records that intervenors will present the plan's savings on deemed single-measure
  values and will argue that basis at the hearing.

## 8. Determinism by construction

* **Slope fit.** Linear and change-point fits, and degree-day bases of 15.5°C or 18°C, all classify every home in both years the same
  way, because no slope falls between 0.020 and 0.031.
* **Building mix.** Next year's single-family share (75%) equals last year's, so pooled and type-standardised per-unit rates agree
  exactly (30.6 GWh).
* **Maturity.** Every close-out project has twelve post-retrofit months of bills; the close-out holds no partial-year project.
* **Pipeline.** All 4,000 units are scheduled and every one has 24 months of pre-period bills at the same account.
* **Rounding.** The committed figure is 15.01 GWh, mid-bin at one decimal.

## 9. Prompt sketch and deliverables

> Our efficiency plan goes to the commission on 1 March and has to state the verified first-year savings next year's whole-home retrofit
> track will deliver, in GWh to one decimal. The programme director is confident next year will look like last year, only bigger. Give
> me the figure as the sentence for the plan, with `savings_build.xlsx`, a chart `heating_slope_split.png`, and a one-page
> `plan_figure_note.pdf`.

* `savings_build.xlsx` — the build by building type and slope class, last year's back-test, the contractor sheet (ask A) and the survey
  sheet (ask B).
* `heating_slope_split.png` — a script-rendered two-panel chart: left, verified savings per unit against pre-period heating slope for
  last year's projects, with the empty band from 0.020 to 0.031 shaded; right, the slope distribution of last year's participants and
  next year's pipeline overlaid, with the 6% and 55% shares labelled.
* `plan_figure_note.pdf` — the committed figure and the bridge from the plan's deemed-values figure.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight contractors, last year's average days from audit to completion and the share
  of jobs with a change order. *Device:* a job paused for an inspection closes and reopens under the same number with a resume event, and
  the contractor guide times a job from first audit to final completion. Timing from the resume understates duration at three contractors.
* **Ask B (device-carried).** For each contractor, the share of participants rating the job 4 or 5, weighted to participants. *Device:* the
  survey drew one respondent per building and its codebook carries a unit weight; unweighted shares over-represent single-family homes and
  move two contractors across the programme's 80% line.
* **Ask C (validity).** Next year's figure under each of the four rung bases, and the close-out total and the East and West cohorts'
  savings per unit as predicted by pooled per-project, pooled per-unit and slope-conditioned per-unit savings.
* **Decoupling.** Replacing conditioned yields with the pooled rate changes no figure in asks A or B. Contractor job logs and the survey
  touch neither bills nor verified savings.

## 11. Rubric arithmetic

8 contractors × 2 (ask A) + 8 weighted shares and the programme share (ask B) + 4 bases and 3 rules × 3 back-test figures (ask C) + the committed
figure, the pipeline's under-heated share and the two conditioned yields + 5 named chart parts + 3 files ≈ 50 criteria.

## 12. World-building constraints

* Last year: 2,100 single-family units and 700 multi-unit units in 280 projects; 6% under-heated in both types. Verified per unit: 9.0
  and 0.2 MWh single-family, 5.5 and 0.1 multi-unit. Total 21,414 MWh.
* Next year: 3,000 single-family and 1,000 multi-unit units, 55% under-heated in both types and in both income groups.
* Rung figures 54.4 / 36.0 / 30.6 / 15.0 GWh; project-grain conditioned cell 17.7; singles conditioned 24.5.
* No home in either year has a slope between 0.020 and 0.031 kWh per degree-day per square foot.
* East and West match on every close-out column; 5 and 60 of their 120 homes were under-heated. Within each class, verified savings per
  unit vary by no more than ±2%.
* Contractor job logs and survey responses never touch bills, slopes or verified savings.
