# RC33 — How many of the state's two lost maths points the new framework caused, when a fifth of the tested students were not in their test school all year

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · K-12 assessment and curriculum policy |
| Mirrors | Feature-impact attribution when the measured user is not the user exposed for the whole period (Meta and Google experiments where accounts switch devices or regions mid-test, subscription products whose end-of-period panel holds users who churned and returned), so an end-of-period snapshot assigns every user to the arm they finished in |
| Decision shape | One figure committed at a date (a component): the framework's share of the grade-8 maths decline, given to the committee before its repeal vote |
| Committed call | The scale points of the state's 2.0-point grade-8 maths decline caused by the Pathways framework, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · the population a field suggests: the test file places each student at the school where they sat the test, and the evaluation's population is students enrolled there all year, a chain of enrolment spells; with the saturated measure of measured #19 at rung 2 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #19 breaks a big tie instead of questioning it · #11 beats the headline trap, misses the quiet one |
| Calibration form | Retry or revision log: the department's three releases of its science-framework evaluation, each with its data vintage and estimate |
| Driving force | The test file places every student at the school where they sat the test. The evaluation plan estimates a curriculum on students taught under it for the full academic year, and 22% of tested students changed school during the year. In two non-adopting districts the movers are students in temporary housing, moved between schools by the districts' housing programme, and their scores fell five points for reasons that have nothing to do with the maths curriculum. They drag the comparison group down and pull every all-student estimate toward zero. On the full-year population, built from enrolment spells, the framework caused 1.5 of the 2.0 points. |

## 1. Situation

The state's grade-8 maths mean on its census assessment fell 2.0 scale points in the first year of the Pathways framework, which 41 of 70
districts adopted in September. Every school in an adopting district taught it from the first day. A legislative committee wants to repeal
it and votes on the 9th, and the education department must give the committee one number: the points of the decline the framework caused.
The department's analysts know the grade-8 population shifted toward groups that score lower. The department's evaluation plan is its
template, and its evaluation of the science framework three years ago is the precedent.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the scores, the adoption register, the enrolment spells, the three enrolment files and the
  published means. The chair is right that scores fell, and the framework's part is quantified. No one's reading of their own figures is
  overturned. The difficulty is which students the comparison is made on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's view and every voice. The within-group comparison with the participation rule still runs on every
  tested student and still returns −1.0.
* **Instrument repair.** Suspect: the three enrolment files disagree, and two of them are stale. Repair: one current enrolment count for every
  school. Rung 0 still returns −2.3, rung 1 −1.3 and rung 2 −1.0, because none of them asks who was enrolled all year; none reaches −1.5.
  The test file is not suspect: its school field records where each student sat the test, correctly for every student, and the enrolment
  spells are complete. A full-year population is a chain of spells that no row records, so the decisive construction is still needed.
* **Lens swap.** The naive population is every student tested in each district. The answer's is students enrolled in their test school from
  the count date to the test date, a different population defined over the year rather than on test day.

## 3. The driving force

A strong solver does not take the committee's word. It removes the composition shift with cross-classified groups, the textbook Simpson
correction. It applies the accountability manual's participation rule, which takes away inflated means at schools where low scorers
went untested. Then it estimates the framework's effect as the difference between adopting and non-adopting districts, within groups, and
the estimate is −1.0 points, a modest effect. But the test file assigns every student to the school where they sat the test, and the
evaluation plan's population is students taught under a curriculum for the full academic year. The enrolment spells show that 22% of tested
students changed school during the year. In two non-adopting districts most movers are students in temporary housing, moved between schools
by the districts' housing programme, and their scores fell five points. They sit in the comparison group and make the framework look
harmless. On students enrolled in their test school from the 1 October count to the test date, the framework cost 1.5 points.

## 4. The ladder

| Rung | Construction | Lands on (points of the 2.0 decline) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Raw change in adopting against non-adopting districts, scaled by the adopting share | −2.3 (+52%) | The committee's comparison, cleanly computed | Cross-classified shares: adopting districts' grade-8 mix shifted 1.5 points more toward lower-scoring groups |
| 1 | Within-group difference-in-differences by adoption, composition removed | −1.3 (−13%) | The Simpson correction, cross-classified, every cell reconciled | The accountability manual's participation rule |
| 2 | Hygiene of a saturated measure: participation recomputed against the largest enrolment count of record, and 23 schools under 95% dropped | −1.0 (−33%) | Reportable means only, as the evaluation plan requires | The enrolment spells: 22% of tested students changed school during the year, and in two non-adopting districts the movers' scores fell five points |
| 3 | **Decisive:** the comparison restricted to students enrolled in their test school from the 1 October count to the test date, built from enrolment spells, then scaled by the adopting share | **−1.5** | — | — |

* **Figure shape.** The corrections walk the figure from −2.3 to −1.0, and the decisive move reverses them to −1.5. Offsets from the answer are
  −0.8, +0.2 and +0.5.
* **Partial correction priced (L3).** Rung 2 sits 0.5 from the answer. A solver who requires continuous enrolment in the district rather than
  the school keeps the within-district movers, who are the comparison group's drag, and lands at −0.8. One who drops movers only in the
  adopting districts, where the city's displacement has been in the news, lands at −0.9. Both are further from −1.5 than rung 2.
* **Grid.** Composition (off, on) × participation (off, on) × population (every tested student, district-continuous, school-continuous)
  gives 12 cells. The nearest wrong cells are −1.3 (13%), −1.7 (the full-year population without the participation rule, 15%) and −1.75
  (district-continuous without composition, 17%). Every other cell is at least 23% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The evaluation plan says "taught under it for the full academic year", and the accountability manual dates the count.
   No document says the test file's school is not the full-year school, or that movers' scores fell.
2. **Corpus blind for a computable reason.** *In every release of the science evaluation every tested student had been in the test school
   since the count date, because the science assessment is sat in the first week of October, before any student has moved.* The releases
   certify rung 2's construction 3 of 3.
3. **No arithmetic symptom.** The test file's school counts reconcile to the published means and to enrolment on test day.
4. **Not a row predicate.** Full-year status is continuity across a student's enrolment spells from the count date to the test date, a chain
   across records, and it enters through a difference-in-differences.
5. **The enumeration is arithmetic.** No field marks a student as full-year. The population is built from spell dates.
6. **No cutover date.** Moves are spread across the year, so no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The department's revision log for its evaluation of the science framework: three releases, each with its data vintage (late test
  records and rescoring) and its published estimate.
* **What it certifies.** Rung 2's construction (cross-classified composition, the participation rule and the adoption difference) reproduces
  all three releases from their vintages exactly. Without the participation rule, the second and third releases miss by 0.2 and 0.3 points.
* **What it is blind to.** Mobility (property 2).
* **Twin pair.** Draycott and Elsworth, two non-adopting districts, are identical on enrolment, cross-classified shares, last year's means,
  participation and the test file's school counts. Their within-group changes were −1.4 and −0.7 (2.06×). On full-year students both
  changed −0.5. Twenty per cent of Draycott's tested students had moved between its schools during the year, against 4% of Elsworth's, and
  only the enrolment spells reproduce both.
* **Resemblance points at the decoy.** The Pathways rollout resembles the science rollout on its calendar and district list, and the science
  evaluation settled on every tested student.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The evaluation plan: "A curriculum's effect is estimated on students taught under it for the full academic year, in
  schools whose means are reportable." The accountability manual: "Enrolment is counted on 1 October." Its participation rule:
  "Participation is tested students over the largest enrolment count in any file of record; below 95% a mean is not reportable."
* **Empirical pins.** The participation counts come from the enrolment files. The full-year population comes from the spell dates.
* **Voices.** Committee chair: "Scores fell the year Pathways arrived; that is the whole story." Department analyst: "It's the population,
  not the framework." Superintendents' association: "Every school in our member districts taught Pathways from the first day."
* **Licensed wrong basis.** The evaluation plan records that the committee's research office compares adopting and non-adopting districts
  on every tested student, and will present its estimate at the hearing.

## 8. Determinism by construction

* **Full year.** A student is full-year if one enrolment spell in the test school runs from 1 October to the test date. No student left the
  roll for fewer than ten days, so short gaps cannot be read two ways.
* **Composition.** Cross-classified cells are fixed by the accountability manual's groups, and every cell holds at least 40 students on each
  side.
* **Participation.** The three enrolment files agree for every school above the floor, and the 23 schools under it sit below 92%, so rounding
  and file order cannot move a school across 95%.
* **Scaling.** Every science release scales its estimated effect by the adopting districts' share of all tested students, and every rung
  here does the same. That share is 65%, whichever population the effect is estimated on.
* **Maturity.** The test file is the final vintage, with every rescoring posted.

## 9. Prompt sketch and deliverables

> The committee votes on repealing Pathways on the 9th and wants one number from the department: how many of the 2.0 points our grade-8
> maths mean lost the framework caused, to one decimal. The chair is certain the framework did all of it. Give me the figure in a sentence
> I can read into the record, with `pathways_effect.xlsx`, a chart `decline_bridge.png`, and a one-page `committee_answer.pdf`.

* `pathways_effect.xlsx` — the estimate on every construction, the staffing sheet (ask A), the accommodations sheet (ask B) and the
  revision-log back-test (ask C).
* `decline_bridge.png` — a bridge from the first-year mean to the second with composition, Pathways and other within-group change. An inset
  sets adopting against non-adopting change for full-year students and for movers, and the title states the Pathways figure.
* `committee_answer.pdf` — the committed figure and what the all-student comparison misses.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine regions and each school phase (elementary, middle, high), unfilled maths
  teaching posts at the start of the year, in full-time equivalents. *Device:* the staffing file lists a post shared between two schools once
  per school, each row carrying the post's full FTE and a split percentage, as the staffing guide's split-post convention documents. Summing
  rows at full FTE overstates vacancies by about a fifth in the two rural regions where posts are shared. Staffing never enters scores.
* **Ask B (device-carried).** For each region, grade-8 students receiving each of three testing accommodation types. *Device:* the
  accommodations file holds one row per accommodation, and a student can have several. Counting rows overstates students by about 40% in
  two regions.
* **Ask C (validity).** For each of the three science-evaluation releases, the published estimate beside the one your construction gives on
  that release's vintage.
* **Decoupling.** Clearing the full-year construction changes no figure in asks A or B. Ask C runs on an assessment sat before anyone moved.

## 11. Rubric arithmetic

9 regions × 3 phases (ask A) + 9 regions × 3 accommodation types (ask B) + 3 releases (ask C) + the committed figure, the composition and
other components and the full-year share of tested students + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Tested-student shares and within-group changes: adopting full-year 52% (−2.80), adopting within-district movers 6% (−3.00), adopting
  arrivals from other districts 7% (−3.64), non-adopting full-year 18% (−0.50), non-adopting within-district movers 6% (−5.00), non-adopting
  arrivals 3% (+0.66), low-participation schools 8% (observed +0.65, all full-year).
* Adopting districts' composition shift exceeds non-adopting districts' by 1.5 points.
* Rung figures are −2.3 / −1.3 / −1.0 / −1.5, the partial corrections −0.8 and −0.9, and every other cell sits at least 13% from −1.5.
* Draycott and Elsworth are identical on every register and assessment column, with 20% and 4% within-district movers.
* The science assessment is sat in the first week of October, and no student in the science evaluation moved before sitting it.
* Staffing rows and accommodation rows never touch scores, enrolment spells or participation counts.
