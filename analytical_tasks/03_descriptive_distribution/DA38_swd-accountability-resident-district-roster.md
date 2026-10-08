# DA38 — Which districts a state flags below the disability-subgroup target, when state special schools' results belong to other districts

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · school accountability |
| Mirrors | Holding the accountable owner to outcomes produced on a shared host (accounts run by an agency, marketplace orders fulfilled by a partner, support tickets worked by a vendor team), where the data files each result under the host that produced it |
| Decision shape | A structure the body adopts: the list of districts flagged below 40% proficiency for students with disabilities in mathematics, among 120 districts |
| Committed call | The list of districts flagged below the target, and their number |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a mixed segment split through a join (measured #6), with a quiet second trap carrying its own control at rung 2 (measured #11) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #6 treats a mixed segment all one way · #11 beats the headline trap, misses the quiet one · #2 counts file rows instead of the real unit |
| Calibration form | Parallel-run overlap: the prior year's federal parallel run, exact subgroup rates for 40 districts built from enrolment records, beside the state's school-coded file for that year |
| Driving force | The office's results file records each placed student's results under the state school where the student tested. Under the state's own rules, a placed student stays enrolled in, and accountable to, the district of residence. That split is reached only by joining the placement roster, and it moves near-zero proficiency from three host districts into dozens of small resident districts, five of which fall below the line. |

## 1. Situation

The state accountability office flags each district whose students with disabilities score below 40% proficient in mathematics. It holds
exact student-level results, coded by the school where each student tested, and publishes range-coded files for the public. Three
state-operated special schools serve placed students from across the state. Last year's draft flagged 37 districts from the public
files' midpoints. The pack holds the office's results file, the school directory, the official participation table, the accountability
plan, the state placement regulation, the placement roster, the public files, and the prior year's federal parallel run.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each student result, each roster line, each participation count, each parallel-run rate. The
  coalition's midpoint list rests on a different basis, and nothing reported is overturned. The difficulty is whose results a state
  school's results are.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the coalition's list and both voices. Exact first-attempt rates, coded by school, still flag 26 and still hold
  every placed student against the host.
* **Instrument repair.** Suspect: the public files, range-coded and suppressed. Published exactly, rung 0 returns rung 1's list of 23;
  rungs 1 and 2 already use the office's exact file and stay at 23 and 26. The results file records the school each student tested at,
  which is correct, and the roster is complete; a placed student's accountable district is a relation built through the roster, so the
  answer stays 29 and the join is still needed.
* **Lens swap.** The naive structure counts placed students in three host districts; the answer counts them in their 61 resident
  districts. Different students in each district's population.

## 3. The driving force

A strong solver discards the draft's midpoints and works from the office's exact results. It checks its tested counts against the
official participation table, finds the summer retests counted twice, and keeps each student's first attempt, the quiet second trap after
the loud one. That list flags 26 districts, and every count ties. But three of the state's special schools sit inside large districts, and
their students, nearly all scoring below proficient, are coded to those hosts. The accountability plan says a district's results include
every student enrolled in it. The placement regulation says a placed student remains enrolled in the district of residence. The roster
says where each placed student lives. Reassigned, two hosts rise above the line and leave the list, while five small resident districts,
each now carrying a dozen non-proficient placed students, fall below it. The list is 29.

## 4. The ladder

| Rung | Structure | Adopts | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Midpoint of each public range, weighted by valid counts, below 40% flagged | 37 flagged | The files the board has always seen, one best estimate per district | The office's results file: exact results for every student, which no range rounds |
| 1 | The office's exact results, every record, coded by school | 23 flagged | Exact, complete and the office's own | The participation table: its tested counts sit below the file's records in 31 districts, by exactly the students retested in summer |
| 2 | Each student counted once on the first attempt, as the participation table requires (the quiet trap, with its own control) | 26 flagged | Exact, deduplicated, every district tied to the official counts | The parallel run: 7 of 40 federal rates differ from the school-coded rates, all in host or resident districts |
| 3 | **Decisive:** placed students' results reassigned to their resident districts through the placement roster | **29 flagged** | — | — |

* **Structure shape.** Each rung adopts a different list, and the answer's list matches no earlier rung's: it drops two host districts
  from rung 2's list and adds five resident districts.
* **Partial correction priced (L3).** A solver who reassigns placed students by the host counties' enrolment shares instead of the roster
  spreads them across 38 districts and flags 27, two of them wrong. One who reassigns them but leaves the summer retests in flags 27 with
  three districts wrong. Neither lands on the answer's list.
* **Grid.** Results (public midpoints or exact) × retests (every record or first attempt) × attribution (school, county shares, roster) =
  12 cells, each with a different list. The nearest wrong list differs from the answer by two districts.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan says results include every enrolled student; the regulation says placed students remain enrolled in
   their district of residence; the roster ships for funding. The results file records schools, and no sentence joins the three.
2. **Pattern B, reproduction in the overlap.** Roster attribution returns all 40 parallel-run rates to the published decimal. School
   coding returns 33 and county shares 36, with every miss on a host or resident district. The attribution is a construction: placed
   students' first attempts joined from the roster, subtracted from hosts and added to residents.
3. **No arithmetic symptom.** State totals are identical under every attribution, the roster's school totals equal the state schools'
   first-attempt counts, and the participation table ties once retests are removed.
4. **Not a row predicate.** It needs results moved between districts by a roster at student grain, then each district's rate recomputed
   on both sides.
5. **The enumeration is arithmetic.** No column marks a result as belonging elsewhere.
6. **No cutover date.** Placements are stable through the year, and nothing steps.
7. **Survives deletion.** With every voice removed, rung 2's list of 26 still reconciles everywhere it is checked.

## 6. The calibration corpus

* **Form.** The prior year's federal parallel run: 40 districts' exact subgroup rates built from enrolment records, beside that year's
  school-coded file.
* **What it certifies.** First attempts as the counting rule, which a solver back-testing on districts with no placements confirms.
* **What pins the attribution.** The seven districts whose federal rates only roster attribution returns, three hosts and four residents.
* **Twin pair.** Districts Pellham and Coldridge match on every school-coded column: tested students, first attempts, proficient counts.
  Their federal rates are 36% and 18% (2.0×): Coldridge is the residence of 14 students placed at a state school in a neighbouring
  district.
* **Resemblance points at the decoy.** Resident districts look like ordinary small districts whose school-coded rates sit above 40%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The accountability plan: the 40% target, and "a district's results include every student enrolled in it, each student
  counted once". The placement regulation: a placed student remains enrolled in the district of residence.
* **Empirical pins.** The counting rule, from the participation table; the attribution, from the overlap.
* **Voices.** The accountability director: "The school files are the official record; each district answers for the schools it runs."
  The draft's author: "Midpoints are the best single estimate we have."
* **Licensed wrong basis.** The plan records that the advocacy coalition publishes district rates by midpoint substitution from the
  public files and will present its list at the board meeting.

## 8. Determinism by construction

* **Roster.** Each placed student has one resident district, and the roster's school totals equal the state schools' first-attempt
  counts.
* **Retests.** Every retest record carries the student ID of a first attempt in the same district.
* **Line.** No district's rate lies within 0.5 points of 40% under any rung.
* **Size.** Every flagged district has at least 10 first attempts under every attribution.

## 9. Prompt sketch and deliverables

> The board adopts this year's disability-subgroup flags on the 22nd, and last year's draft flagged 37 districts off the public files'
> midpoints. I need the list of districts below 40% and how many there are, as the list in the board resolution. Send `swd_flags.xlsx`,
> a chart `district_rates.png`, and a one-page `flags_note.pdf`.

* `swd_flags.xlsx` — rates for all 120 districts under each rung, the participation sheet (ask A), the trend sheet (ask B) and the
  parallel-run table (ask C).
* `district_rates.png` — each district's rate as a dot sorted by rate, the 40% line drawn, host and resident districts marked,
  school-coded and roster-attributed rates joined, and the parallel run's federal rates as crosses.
* `flags_note.pdf` — the adopted list, its count, and the attributions a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 regional service areas, all-student mathematics participation. *Device:*
  medically exempt students carry their own code and leave the denominator under the participation rule; counting them understates
  four areas.
* **Ask B (device-carried).** For each area, the change in all-student proficiency since last year. *Device:* the assessment was
  re-scaled, and the technical report's concordance maps last year's levels to this year's; comparing raw levels misstates seven areas.
* **Ask C (validity).** Each rung's flagged count, and how many of the 40 parallel-run rates each attribution returns.
* **Decoupling.** Clearing the roster attribution changes no figure in asks A or B.

## 11. Rubric arithmetic

12 areas (ask A) + 12 areas (ask B) + 4 flagged counts and 3 return counts (ask C) + the 29 flagged districts and their number + 5 named
chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Three state schools in three host districts; 412 placed students resident in 61 districts.
* Flagged: 37 / 23 / 26 / 29. The answer drops two host districts from rung 2's list and adds five resident districts.
* Retests: 1,940 summer retest records in 31 districts, proficient at 2.3 times the rate of first attempts.
* Parallel run returned: roster 40, county shares 36, school coding 33. Pellham and Coldridge match on every school-coded column.
* Exemption codes and the re-scaling never touch a subgroup result.
