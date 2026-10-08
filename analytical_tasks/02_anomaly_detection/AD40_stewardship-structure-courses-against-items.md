# AD40 — What the board's antibiotic excess is made of, and which practices go to which intervention, when items and courses tell two stories

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · health-system administration |
| Mirrors | Usage-anomaly programmes that rank accounts by transaction rows when a few heavy recurring users generate most of the rows (cloud cost-anomaly reviews where scheduled jobs dominate line items, subscription reviews where auto-renewals swamp new purchases, recurring delivery orders against one-off orders at Amazon) |
| Decision shape | A structure the body adopts: how many intervention populations the three-year stewardship plan names and which practices sit in each, scored on each population holding excess at the grain its intervention acts on |
| Committed call | The populations and their member practices, adopted into the stewardship plan at the board meeting in March |
| Gap · Pattern | Gap 2 (population: courses started and residents on prophylaxis, not items) over Gap 3 (objective) · Pattern D (items and courses, both flawless, differ in shape because repeat prophylaxis concentrates items in few patients), with a suppressed cell bounded from published totals below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #6 treats a mixed segment all one way · #24 treats an unpublished figure as unknown |
| Calibration form | Change-log natural experiments: the board's log of 38 pharmacist visits (2022–2025), with each visited practice's prescribing for six months before and after |
| Driving force | The prescribing file counts items, and the board's standard ranks practices on items per STAR-PU. A pharmacist visit acts on decisions to start a course; a care-home review acts on residents kept on long-term prophylaxis. In practices serving nursing homes, forty residents on monthly prophylaxis write as many items as five hundred acute courses, so the item ranking mixes two populations needing different interventions. Rebuilding courses and prophylaxis episodes from the board's linked patient-level prescriptions splits the excess into two populations with different members, which the visit log cannot see because no visited practice ever served a care home. |

## 1. Situation

An integrated care board's antibiotic items per STAR-PU run 14% above the national mean across its 62 practices. Its three-year
stewardship plan must name the intervention populations: practices for pharmacist visits (which review how courses are started) and
practices for care-home medication reviews (which review residents on long-term prophylaxis). The plan scores each population on the excess
its intervention can act on. The board holds the national prescribing file (items by practice, chemical and month, with chemical cells under
five suppressed), quinary list sizes and STAR-PU weights, its own linked patient-level prescriptions, practice care-home contracts and the log
of past visits. Until this plan, practices with care-home contracts were served only by the care-home pharmacy team. The GP lead expects the
usual twenty practices.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: items, list sizes, STAR-PU weights, the published cells and their suppression, the patient-level
  records and the visit log. The GP lead is right that the same practices top the item ranking every year. Nothing is overturned; the
  difficulty is that the item ranking describes a mix of two populations.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the GP lead's view and the dashboard. The board's own standard, items per STAR-PU with bounded broad-spectrum
  shares, still yields one population of sixteen.
* **Instrument repair.** Make the item file and the list sizes perfect: they are. An item is still an item, and a monthly prophylaxis
  prescription is still twelve of them a year; only the patient-level episodes say what the items were for.
* **Lens swap.** The naive structure is built on prescription items; the answer is built on two different patient populations (people
  starting acute courses and residents on prophylaxis), with different practices in each and one practice in neither.

## 3. The driving force

A strong solver drops items per 1,000 patients for STAR-PU, applies the board's dual standard (excess items above an overdispersed limit and a
broad-spectrum share above 10%), bounds the suppressed chemical cells instead of dropping three practices, and confirms on 38 past visits that
a visit cuts items per STAR-PU by about a fifth. Every step is correct, and every step counts items. A visit changes how often a clinician
starts a course; it does not touch a resident whose prophylaxis a specialist started. In the six practices with nursing-home contracts, most
excess items are monthly repeats for a few dozen residents, and in three dispensing practices seven-day courses go out as two items. Grouping
each patient's prescriptions into episodes (items within 14 days are one course; six or more consecutive monthly repeats of one drug are
prophylaxis) and standardising each by STAR-PU gives two excesses with different members, and the visit log, drawn only from practices
without care-home contracts, shows items and courses falling together and cannot tell them apart.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Items per 1,000 registered patients, top twenty | One population of 20, mostly retirement-town practices | The board's dashboard | The STAR-PU weights: age and sex explain most of the dashboard's spread |
| 1 | The board's dual standard on items per STAR-PU, practices with suppressed chemical cells left out as unverifiable | One population of 14 | The board's own standard, applied to what is published | The published section totals: each suppressed cell is bounded by the section total less the published chemicals |
| 2 | The dual standard with suppressed cells bounded (two of three practices qualify under every value in their bounds) | One population of 16 | Standard, case-mix and suppression all handled | The care-home contracts and the linked records: six of the sixteen owe most of their excess to residents on monthly prophylaxis |
| 3 | **Decisive:** episodes rebuilt per patient; acute courses per STAR-PU and residents on prophylaxis per STAR-PU, each against its own overdispersed limit | **Two populations: visits for 9 practices (7 from rung 2 and 2 new), care-home reviews for 6; 3 of rung 2's sixteen in neither** | — | — |

* **Structure table.** Four structures: twenty by raw rate, fourteen and sixteen by the standard, and the two-population answer. Two of the
  answer's visit practices appear on no lower rung, because their acute-course excess sits below the item limit.
* **Separation at the decisive rung.** The six care-home practices run at 1.41× the board's items per STAR-PU and 1.02× its acute courses;
  the two new visit practices run at 1.08× on items and 1.37× on courses. The three dropped dispensing practices sit at 1.29× on items and
  0.97× on courses.
* **Partial correction priced (L3).** A solver who removes care-home residents' items from the item counts but keeps the item grain for
  everyone else still lists the three dispensing practices for visits and misses the two new ones: one population of ten, further from the
  answer than rung 2's sixteen on membership.
* **Grid.** Denominator (patients or STAR-PU) × suppressed cells (dropped or bounded) × grain (items or episodes) = 8 cells. Every item-grain
  cell yields one population (20, 20, 14 or 16); episode cells yield two populations, and only with STAR-PU and bounded cells do they hold
  nine and six.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan's scoring clause says what each intervention acts on. No document says that items and courses diverge, or
   where.
2. **Corpus blind for a computable reason.** *In every logged visit, items and acute courses fell by the same share (17–25%), because every
   visited practice was one without a care-home contract and so carried almost no prophylaxis.* The log certifies that visits cut items per
   STAR-PU, the rung 2 grain, and cannot separate items from courses.
3. **No arithmetic symptom.** Items tie to the national file, patient-level items tie to the practice totals, list sizes tie to STAR-PU
   denominators, and every bound sits inside its published total.
4. **Not a row predicate.** Episodes need each patient's prescriptions ordered in time and grouped by gap and repeat pattern, then counted per
   practice against STAR-PU.
5. **The enumeration is arithmetic.** Which items are prophylaxis is computed from sequences; no column marks them.
6. **No cutover date.** Care-home prophylaxis and dispensing habits are standing; no series steps.
7. **Survives deletion.** Remove the GP lead and the dashboard, and the standard-based single population is still the natural build.

## 6. The calibration corpus

* **Form.** The visit log: 38 pharmacist visits in 2022–2025, with each visited practice's items and courses per STAR-PU for six months
  either side.
* **What it certifies.** A visit cuts items per STAR-PU by 21% (17–25%) at the practices it has reached, so a back-tester is confirmed in
  treating items as what a visit moves.
* **What it is blind to.** Practices whose items are not courses (above).
* **Twin pair.** Practices Hollins Road and Wexcombe have identical items per STAR-PU (1.38× the board), list sizes, age profiles,
  broad-spectrum shares and rurality. Hollins Road's excess is 470 acute courses and Wexcombe's 230, 2.0× apart, because 40 of Wexcombe's
  residents are on monthly prophylaxis; only the episode grain separates them.
* **Resemblance points at the decoy.** By item rate and list profile, the care-home practices most resemble the visited practices whose items
  fell by a fifth.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The plan's scoring clause: a visit is scored on the decisions to start courses it can act on, and a care-home review on the
  residents on long-term prophylaxis it can act on. The board's dual standard. The suppression rule of the national file. One sentence each.
* **Empirical pins.** The episode gap and the prophylaxis run, from the absolute split in the patient records (below).
* **Voices.** The GP lead: "It is the same twenty practices every year; visit them." The prescribing adviser: "Items per STAR-PU is the
  national measure, and it has never let us down."
* **Licensed wrong basis.** The plan's terms record that the regional commissioning team reports the board on items per STAR-PU and will
  present its practice list at the March meeting.

## 8. Determinism by construction

* **Episodes.** Gaps between a patient's antibiotic items are under 7 days or over 21, so any episode gap in that range builds the same
  courses; repeat runs are either under 3 months or 6 and over, so the prophylaxis cut-off is threshold-free.
* **Bounds.** Both qualifying practices clear 10% broad-spectrum at the low end of their bounds, and the third falls short at the high end.
* **Limits.** Each population's overdispersed limit is estimated the same way as the board's standard; winsorising at 10% or 5% changes no
  member.
* **Linked coverage.** Every practice's patient-level items tie to its national item total within 0.5%.

## 9. Prompt sketch and deliverables

> Our three-year stewardship plan has to say what our antibiotic excess actually is and which practices get pharmacist visits and which get
> care-home medication reviews. The GP lead is sure it is the same twenty practices it always is. Give me the structure (how many groups and
> which practices in each) in a paragraph the board can adopt in March, and send `stewardship_structure.xlsx`, a chart
> `items_against_courses.png`, and a one-page `plan_note.pdf`.

* `stewardship_structure.xlsx` — every practice on both grains with its population (ask C), the prescriber sheet (ask A) and the care-home
  sheet (ask B).
* `items_against_courses.png` — each practice as a point, items per STAR-PU against acute courses per STAR-PU, both limits drawn and
  labelled, care-home practices in one marker, the two adopted populations outlined and the three dropped practices annotated.
* `plan_note.pdf` — the committed structure and why each rung's structure falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five primary care networks, the share of antibiotic items written by nurse and
  pharmacist prescribers. *Device:* prescriber type sits in the prescriber register, effective-dated because prescribers move between
  practices; joining on the current row misattributes a sixth of items in two networks. The structure never uses prescriber type.
* **Ask B (device-carried).** For each of the twelve care homes linked to the board's practices, residents on census day and the share with a
  medication review in the last twelve months. *Device:* the census guide counts respite residents only if resident on census day, and the
  home register's bed counts are capacity, not residents; using beds understates review shares in five homes.
* **Ask C (validity).** Each of the four rung structures with its populations, members and total excess.
* **Decoupling.** Clearing the episode grain and the bounds changes no figure in asks A or B.

## 11. Rubric arithmetic

5 networks × 2 (ask A) + 12 homes × 2 (ask B) + 4 structures × 3 (ask C) + the committed populations, their fifteen members and each
population's excess + 5 named chart parts + 3 files ≈ 58 criteria.

## 12. World-building constraints

* 62 practices. Rung structures: 20, 14, 16, and the answer's 9 + 6, with 3 dropped and 2 new.
* Six care-home practices: items 1.41×, courses 1.02×. Two new visit practices: items 1.08×, courses 1.37×. Three dispensing practices: items
  1.29×, courses 0.97×.
* The visit log holds 38 visits, none at a practice with a care-home contract; items and courses fall within one point of each other in all.
* Hollins Road and Wexcombe are identical on every item-level column.
* Prescriber register and care-home census never touch items, list sizes or the patient-level records.
