# DA38 — Which districts a state flags as certainly below the disability-subgroup target, when state special schools' results belong to other districts

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · school accountability |
| Mirrors | Holding the accountable owner to outcomes produced on a shared host (accounts run by an agency, marketplace orders fulfilled by a partner, support tickets worked by a vendor team), where the data files each result under the host that produced it |
| Decision shape | A structure the body adopts: the three-way classification of 120 districts (certainly below, undetermined, certainly at or above 40% proficiency for students with disabilities in mathematics), scored on consistency with every published count |
| Committed call | The list of districts certainly below the target, and the number left undetermined |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a mixed segment split through a join (measured #6), with a quiet second trap carrying its own control at rung 2 (measured #11) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #6 treats a mixed segment all one way · #11 beats the headline trap, misses the quiet one · #24 treats an unpublished figure as unknown |
| Calibration form | Parallel-run overlap: one prior year in which the state's exact internal rates for 40 districts were produced alongside the public range-coded files |
| Driving force | The public files code each state-operated special school's results under the district that hosts it. Under the state's own rules, a placed student stays enrolled in, and accountable to, the district of residence. That split is reached only by joining the placement roster, and it moves near-zero proficiency from three host districts into dozens of small resident districts, five of which fall certainly below the line. |

## 1. Situation

The state accountability office classifies each district's students with disabilities in mathematics against a 40% proficiency target,
and flags districts certainly below for targeted support. Public school-level results are range-coded ("20-29", "GE50", "LT5", "PS") with
valid test counts, and district-level files carry their own ranges. Last year's draft substituted midpoints and flagged 37 districts. The
pack holds both public files, the accountability plan, the state placement regulation, the placement roster, and the prior year's
parallel run.

## 2. Gate G: why this is legal

* **Litmus.** Every published range and count is correct, and so is every roster line. The draft's midpoint list is not shipped as a
  ranking, and nothing reported is overturned. The difficulty is whose results a state school's results are.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the draft and both voices. Bounds built from the public files, tightened by the district file, still classify
  every state-school student with the host district.
* **Instrument repair.** Publish every cell exactly: the state school's results would still sit under its host district, correctly, since
  that is where the tests were taken. Accountability to residence is a rule about ownership, not a measurement gap.
* **Lens swap.** The naive structure counts placed students in three host districts; the answer counts them in their 61 resident
  districts. Different students in each district's population.

## 3. The driving force

A strong solver discards midpoints, bounds each district's rate from the ranges and counts, and tightens suppressed cells against the
district file's own range, the quiet second trap after the loud one. That structure flags 24 districts. But three of the state's special
schools sit inside large districts, and their students, nearly all scoring below proficient, are coded to those hosts. The accountability
plan says a district's results include every student enrolled in it. The placement regulation says a placed student remains enrolled in
the district of residence. The roster says where each placed student lives. Reassigned, the hosts' bounds rise and two leave the list,
while five small resident districts, each now carrying a dozen non-proficient placed students, fall certainly below. The list is 27, with
21 undetermined.

## 4. The ladder

| Rung | Structure | Adopts | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Midpoint of each range, weighted by valid counts, below 40% flagged | 37 flagged, none undetermined | A single best estimate per district | The scoring basis: a flag must hold under every count the files allow |
| 1 | Bounds from school ranges, suppressed cells as 0–100% | 19 below, 31 undetermined | Exactly what the ranges permit | The district-level file publishes its own range, which the school bounds exceed in 26 districts |
| 2 | School bounds intersected with the district file's range (the quiet trap, with its own control) | 24 below, 22 undetermined | Both published grains honoured; every parallel-run rate falls inside its bound for non-host districts | The parallel run: 7 of 40 exact rates fall outside their host-coded bounds |
| 3 | **Decisive:** state-school results reassigned to resident districts through the placement roster, then bounded and intersected | **27 below, 21 undetermined** | — | — |

* **List shape.** Each rung adopts a different list: rung 2 holds 24, including two host districts the answer clears and none of the five
  resident districts the answer adds.
* **Partial correction priced (L3).** A solver who reassigns placed students but skips the district-range intersection flags 22 with 29
  undetermined, because three of the five resident districts stay undetermined without the district file's tighter range. A solver who
  reassigns by the host counties' enrolment shares instead of the roster spreads the placed students thinly across 38 districts and flags
  25, two of them wrong. Neither lands on the answer's list.
* **Grid.** Midpoint or bounds × suppressed cells (open or intersected) × attribution (host, county shares, roster) = 12 cells, each with
  a different list. The nearest wrong list differs from the answer by three districts.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan says results include every enrolled student; the regulation says placed students remain enrolled in
   their district of residence; the roster ships for funding. No sentence joins them, and the public files' district codes look complete.
2. **Pattern B, reproduction in the overlap.** Roster attribution puts all 40 parallel-run rates inside their bounds. Host attribution
   contains 33, and county shares 36, with every miss on a host or resident district. The attribution is a construction: placed students
   aggregated by school and resident district from the roster, then subtracted from hosts and added to residents.
3. **No arithmetic symptom.** State totals are identical under every attribution, and school ranges reconcile to the district files
   wherever no state school sits.
4. **Not a row predicate.** It needs counts moved between districts by a roster at student grain, followed by new bounds on both sides.
5. **The enumeration is arithmetic.** No column marks a result as belonging elsewhere.
6. **No cutover date.** Placements are stable through the year, and nothing steps.
7. **Survives deletion.** With every voice removed, rung 2's list of 24 still reconciles everywhere it is checked.

## 6. The calibration corpus

* **Form.** The prior year's parallel run: 40 districts' exact internal rates under the plan, beside that year's public range-coded
  files.
* **What it certifies.** That bounds contain the truth and that the district file tightens them, which carries a solver to rung 2.
* **What pins the attribution.** The seven exact rates outside their host-coded bounds, all on host or resident districts.
* **Twin pair.** Districts Pellham and Coldridge match on every public range, valid count and district-file range. Their exact rates are
  36% and 18% (2.0×): Coldridge is the residence of 14 students placed at a state school in a neighbouring district.
* **Resemblance points at the decoy.** Resident districts look like ordinary small districts whose ranges sit above 40%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The accountability plan: the target, the three classes, and "a district's results include every student enrolled in
  it". The placement regulation: a placed student remains enrolled in the district of residence. The range parse table.
* **Empirical pins.** The attribution, from the overlap.
* **Voices.** The accountability director: "The school files are the official record; each district answers for the schools it runs."
  The draft's author: "Midpoints are the best single estimate we have."
* **Licensed wrong basis.** The plan records that the advocacy coalition publishes district rates by midpoint substitution and will
  present its list at the board meeting.

## 8. Determinism by construction

* **Roster.** Each placed student has one resident district, and the roster's school totals equal the state schools' valid counts.
* **Ranges.** The parse table fixes every code, including "PS" before intersection.
* **Line.** No district's final bound lies within 0.5 points of 40%.
* **Proficiency of placed students.** The state schools publish their own ranges; every reassigned student carries the school's bound.

## 9. Prompt sketch and deliverables

> The board adopts this year's disability-subgroup classification on the 22nd, and last year's draft flagged 37 districts off midpoints.
> I need the list of districts certainly below 40%, scored on whether each flag holds under every count the published files allow, and
> how many districts stay undetermined. Send `swd_classification.xlsx`, a chart `district_bounds.png`, and a one-page
> `classification_note.pdf`.

* `swd_classification.xlsx` — the bounds for all 120 districts, the participation sheet (ask A), the trend sheet (ask B) and the overlap
  table (ask C).
* `district_bounds.png` — each district's interval as a horizontal bar sorted by midpoint, the 40% line drawn, host and resident districts
  marked, and the parallel run's exact rates as dots.
* `classification_note.pdf` — the adopted list, the undetermined count, and the attributions a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 regional service areas, all-student mathematics participation. *Device:*
  medically exempt students carry their own code and leave the denominator under the participation rule; counting them understates
  four areas.
* **Ask B (device-carried).** For each area, the change in all-student proficiency since last year. *Device:* the assessment was
  re-scaled, and the technical report's concordance maps last year's levels to this year's; comparing raw levels misstates seven areas.
* **Ask C (validity).** Each rung's class counts, and how many of the 40 parallel-run rates each attribution's bounds contain.
* **Decoupling.** Clearing the roster attribution changes no figure in asks A or B.

## 11. Rubric arithmetic

12 areas (ask A) + 12 areas (ask B) + 4 rungs × 3 class counts and 3 containment counts (ask C) + the 27 flagged districts and the
undetermined count + 5 named chart parts + 3 files ≈ 74 criteria.

## 12. World-building constraints

* Three state schools in three host districts; 412 placed students resident in 61 districts.
* Class counts: 37/0/83, 19/31/70, 24/22/74, 27/21/72. The answer drops two host districts from rung 2's list and adds five resident
  districts.
* Overlap containment: roster 40, county shares 36, host 33. Pellham and Coldridge match on every public column.
* Exemption codes and the re-scaling never touch a disability-subgroup range.
