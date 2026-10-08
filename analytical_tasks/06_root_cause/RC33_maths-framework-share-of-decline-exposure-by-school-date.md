# RC33 — How many of the state's two lost maths points the new framework caused, when the adoption flag is not who was taught under it

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · K-12 assessment and curriculum policy |
| Mirrors | Feature-impact attribution when the rollout flag is not exposure (Meta and Google features flagged on by account while clients updated on their own schedule, Apple opt-in features, staged enterprise rollouts at Microsoft), where some flagged units never got the feature and some unflagged units did |
| Decision shape | One figure committed at a date (a component): the framework's share of the grade-8 maths decline, given to the committee before its repeal vote |
| Committed call | The scale points of the state's 2.0-point grade-8 maths decline caused by the Pathways framework, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the population a flag suggests: exposure is set by each school's implementation date in the register's revision log, not by the district flag |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #19 breaks a big tie instead of questioning it · #11 beats the headline trap, misses the quiet one |
| Calibration form | Retry or revision log: the department's three releases of its science-framework evaluation, each with its data vintage and estimate |
| Driving force | The curriculum register flags districts as adopters. Who was actually taught under Pathways depends on each school's implementation date, recorded in the register's revision log. Waiver schools in adopting districts never implemented, January schools implemented halfway through the year, and charter schools in non-adopting districts implemented early. The charters sit in the flag's comparison group carrying the framework's own effect, so every flag-based estimate is pulled toward zero. |

## 1. Situation

The state's grade-8 maths mean on its census assessment fell 2.0 scale points in the first year of the Pathways framework, which 41 of 70
districts adopted. A legislative committee wants to repeal it and votes on the 9th. The education department must give the committee one
number: the points of the decline the framework caused. The department's analysts know the grade-8 population shifted toward groups that
score lower. The department's evaluation plan estimates a curriculum's effect on students taught under it, using schools whose means are
reportable under the accountability manual.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: scores, cross-classified group shares, enrolment files, the register and its revision log,
  and the science evaluation's releases. The committee is right that the framework cost points, and the figure quantifies how many. No one's
  reading of their own numbers is overturned.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the committee's belief and every voice. The register's flag still defines the natural treated group, and every
  flag-based estimate still lands short.
* **Instrument repair.** Measure every student's score without error. Who was taught under the framework is still a date in a revision log
  joined to an enrolment history, and the flag still differs from it at 15% of students.
* **Lens swap.** The naive treated group is students in flagged districts. The answer's is students in schools that had implemented, and the
  two differ at 15% of students, on both sides of the comparison.

## 3. The driving force

A strong solver does not take the committee's word. It removes the composition shift with cross-classified groups, the textbook Simpson
correction. It applies the accountability manual's participation rule, which takes away inflated means at schools where low scorers
went untested. Then it estimates the framework's effect as the difference between flagged and unflagged districts, within groups. The
estimate is −1.0 points, a modest effect. But the flag is a district attribute, and exposure is a school's. The register's revision log
dates every school's implementation: September for most, January for some, never for nine waiver schools, and early for six charter
schools in districts that did not adopt. Those charters carry the framework's full effect inside the comparison group, so every flag-based
estimate is pulled toward zero. With exposure dated by school, the dose-response is clean at −3.0 points a full year, and the state's
exposure-weighted share is −1.5 points.

## 4. The ladder

| Rung | Construction | Lands on (points of the 2.0 decline) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Raw change in flagged against unflagged districts, scaled by the flagged share | −2.2 (+45%) | The committee's comparison, cleanly computed | Cross-classified shares: flagged districts' grade-8 mix shifted 1.5 points more toward lower-scoring groups |
| 1 | Within-group difference-in-differences by the flag, composition removed | −1.3 (−14%) | The Simpson correction, cross-classified, every cell reconciled | The accountability manual's participation rule |
| 2 | Hygiene of a saturated measure: participation recomputed against the largest enrolment count of record, and 23 schools under 95% dropped | −1.0 (−33%) | Reportable means only, as the evaluation plan requires | The register's revision log: implementation dates by school, which differ from the district flag at 15% of students |
| 3 | **Decisive:** exposure by school implementation date, joined to each student's enrolment spells, then dose-response and the exposure-weighted share | **−1.5** | — | — |

* **Figure shape.** The corrections walk the figure toward zero (−2.2, −1.3, −1.0), and the decisive move reverses them to −1.5. The 2.0
  decline is composition −1.0, Pathways −1.5 and other within-group change +0.5.
* **Partial correction priced (L3).** Rung 2 sits 0.5 from the answer. A solver who uses implementation dates only inside adopting
  districts finds the waiver and January schools but leaves the charters in the comparison group, and lands on −1.0 again. Treating
  January schools as fully exposed changes nothing, because their whole change enters either way.
* **Grid.** Exposure (flag or dates) × participation rule (off or on) × composition (raw or within-group) = 8 cells. The nearest wrong cell
  is dates without the participation rule (−1.7, 12% away). It requires keeping 23 schools whose means the manual says are not reportable.
* **Which guard binds.** A figure, so separation binds. Per-rung offsets are +45%, −14% and −33%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The evaluation plan says "students taught under the framework". No document says the flag misstates exposure or
   points at the revision log's dates.
2. **Corpus blind for a computable reason.** *Every school implemented the science framework on its district's adoption date, because that
   framework was imposed by regulation on the 31 pilot districts, with no waivers inside them and no early adoption outside.* The flag and
   the dates coincide in every release of the science evaluation.
3. **No arithmetic symptom.** Flagged and unflagged enrolment reconcile to the state total, the revision log reconciles to the register's
   current state, and every cell's mean ties to the published means.
4. **Not a row predicate.** Exposure joins each student's enrolment spells to each school's implementation date as of the test date, so a
   student who moved schools mid-year carries a split exposure.
5. **The enumeration is arithmetic.** No field says who was taught under Pathways. The answer is a dated join.
6. **No cutover date.** Implementation is staggered by school across the year, so no statewide series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The department's revision log for its evaluation of the 2019 science framework: three releases, each with its data vintage
  (late test records and rescoring) and its published estimate.
* **What it certifies.** Rung 2's construction (cross-classified composition, the participation rule, the flag-based difference) reproduces
  all three releases from their vintages exactly. Without the participation rule, the second and third releases miss by 0.2 and 0.3 points.
* **What it is blind to.** Flag-date divergence (property 2).
* **Twin pair.** Ashby and Corran districts are identical on the flag, enrolment, cross-classified shares, first-year means and
  participation (all above 95%). Their within-group changes were −1.4 and −2.9 (2.07×). Half of Ashby's grade-8 enrolment sits in waiver
  schools, and all of Corran's implemented in September. Only the revision log's dates reproduce both.
* **Resemblance points at the decoy.** The Pathways rollout resembles the science rollout on its calendar and district list, and the
  science evaluation settled on the flag.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The evaluation plan: "A curriculum's effect is estimated on students taught under it, in schools whose means are
  reportable." The accountability manual's participation rule: "Participation is tested students over the largest enrolment count in any
  file of record; below 95% a mean is not reportable." The register states that its revision log is the record of implementation.
* **Empirical pins.** The participation counts come from three enrolment files. The dose-response is fitted on exposure.
* **Voices.** Committee chair: "Scores fell the year Pathways arrived; that is the whole story." Department analyst: "It's the
  population, not the framework." District superintendents' association: "Our members adopted Pathways in September, and that is the date
  that matters."
* **Licensed wrong basis.** The evaluation plan records that the committee's research office compares adopting and non-adopting districts
  by the register's flag, and will present its estimate at the hearing.

## 8. Determinism by construction

* **Exposure fraction.** January schools enter at half a year. Counting them as fully exposed leaves the share unchanged, because their
  whole change enters the exposure-weighted sum either way.
* **Mobility.** Students who changed schools carry exposure pro rata by days. No mover changed schools within 30 days of a school's
  implementation date, so the day-count convention cannot matter.
* **Participation.** The three enrolment files agree for every school above the floor, and the 23 schools under it sit below 92%, so
  rounding and file order cannot move a school across 95%.
* **Dose-response.** Linear and stepwise fits give −3.0 a full year within 0.05.
* **Maturity.** The test file is the final vintage, with every rescoring posted.

## 9. Prompt sketch and deliverables

> The committee votes on repealing Pathways on the 9th and wants one number from the department: how many of the 2.0 points our grade-8
> maths mean lost the framework caused, to one decimal. The chair is certain the framework did all of it. Give me the figure in a sentence
> I can read into the record, with `pathways_effect.xlsx`, a chart `decline_bridge.png`, and a one-page `committee_answer.pdf`.

* `pathways_effect.xlsx` — the estimate on every construction, the attendance sheet (ask A), the accommodations sheet (ask B) and the
  revision-log back-test (ask C).
* `decline_bridge.png` — a bridge from the first-year mean to the second with composition, Pathways and other within-group change. An inset
  plots school within-group change against implementation exposure with the fitted line, and the title states the Pathways figure.
* `committee_answer.pdf` — the committed figure and what the flag comparison misses.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine regions and grades 6, 7 and 8, the share of students chronically absent
  (missing at least 10% of enrolled days). *Device:* attendance is recorded per enrolment spell, and the attendance guide combines spells for
  students who transferred. Computing per spell misclassifies about a fifth of mobile students. Attendance never enters the framework
  estimate.
* **Ask B (device-carried).** For each region, grade-8 students receiving each of three testing accommodation types. *Device:* the
  accommodations file holds one row per accommodation, and a student can have several. Counting rows overstates students by about 40%
  in two regions.
* **Ask C (validity).** For each of the three science-evaluation releases, the published estimate beside the one your construction gives on
  that release's vintage.
* **Decoupling.** Clearing the date-based exposure changes no figure in asks A or B. Ask C runs on a rollout where flag and dates coincide.

## 11. Rubric arithmetic

9 regions × 3 grades (ask A) + 9 regions × 3 accommodation types (ask B) + 3 releases (ask C) + the committed figure, the composition and
other components and the exposed share + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Student shares: September implementers 38%, January 12%, waiver schools 9% (all flagged), early charters 6%, low-participation schools 8%
  and other unflagged 27%.
* Full-year effect is −3.0. Low-participation schools' observed change is +2.0 against a true 0. Flagged districts' composition shift
  exceeds unflagged by 1.5 points.
* Rung figures are −2.2 / −1.3 / −1.0 / −1.5, and every other cell sits at least 12% from −1.5.
* Ashby and Corran are identical on every register and assessment column except implementation dates.
* The science pilot's 31 districts all implemented on their adoption date.
* Attendance spells and accommodation rows never touch scores, the register or participation counts.
