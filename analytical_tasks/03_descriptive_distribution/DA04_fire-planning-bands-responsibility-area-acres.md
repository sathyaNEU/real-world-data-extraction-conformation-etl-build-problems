# DA04 — The planning bands a state fire agency adopts for its tankers and crews, when the acres it protects are not the fires that start on its ground

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · emergency aviation and crew pre-positioning |
| Mirrors | Planning response capacity on incidents that start in a region when the commitment is the impact inside it (cloud availability-zone incident tiers measured on customer-minutes in the zone, parcel-network disruption bands by affected lanes rather than origin depots, trust-and-safety queues sized on reach inside a market rather than where content was posted) |
| Decision shape | A structure the body adopts: the three planning-band boundaries (50%, 80% and 95% coverage) that set where contracted tankers and extended-attack crews are staged |
| Committed call | The three boundaries in acres of fire size, each rounded down to the nearest 10 acres, headed by the 80% boundary |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E18, the segment the plan protects (acres burned inside the State Responsibility Area) coarsened to the familiar one (fires that start there), with E33 (escaped prescribed fires behind the incident log) and record hygiene below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #5 takes the population a flag or filter suggests · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Gold-standard verification subsample: the 2024 data-quality audit of 820 incidents drawn at random from 2011–2025, each re-verified for type, duplicate status, origin and final size |
| Driving force | The plan protects acres inside the State Responsibility Area, and the agency's annual report counts fires that start there, at their whole size. A fire's planning weight is the part of its final perimeter inside the SRA map in force on its discovery date. Federal-origin megafires that ran into the SRA carry 31% of its burned acres and appear in no SRA-origin table, so every origin-based band sits too low. The audit that certifies everything else samples fires a crew can walk, and none of those crosses a line. |

## 1. Situation

A state forestry agency's fire division signs its annual operating plan on 20 March. The plan stages contracted air tankers and twelve
extended-attack hand crews by planning band: the fire sizes above which fires account for 50%, 80% and 95% of the acres burned in the
State Responsibility Area (SRA) in 2011–2025. The pack holds the incident records (origin point, discovery date, type, final size,
reporting agency, the dispatcher's responsibility field), the incident event log, final perimeters for every fire of 300 acres or more,
the SRA map with its annual effective-dated revisions, the agency's annual statistical reports and the 2024 audit. The federal
partners in the region bring their own bands to the same meeting.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: incident sizes, perimeters, the map, the annual reports (tabulated by responsibility area of
  origin, and labelled so) and the audit. Nobody's reading of their own numbers is overturned. The difficulty is which acres the plan's
  bands are drawn on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the aviation manager's view, the statistician's view and the federal partners' licensed basis. The incident
  file still carries an origin responsibility field and a final size on every row, and area-weighted bands off it still follow the
  method's arithmetic exactly.
* **Instrument repair.** Make every report, perimeter and map perfect; they already are. The planning weight is an intersection of two
  correct layers, the perimeter and the map in force that day, and no better incident record carries it.
* **Lens swap.** The two reads cover different populations: 9,412 SRA-origin fires at their whole size, against 10,268 fires that burned
  SRA acres, 856 of them federal- or local-origin, each at its SRA portion.

## 3. The driving force

A strong solver takes fires whose origin is in the SRA, merges the mutual-aid duplicates the audit confirms, adds the prescribed fires
the event log shows escaped, and weights each fire by its final size. Every step is checked against the audit, which agrees exactly. But
the plan protects SRA acres. A fire that starts in a national forest and runs eleven miles into SRA grassland is an SRA planning event
for every acre it burns there, and an SRA-origin fire that runs into federal timber leaves most of its size behind. Weighting by the
part of each final perimeter inside the map in force on the discovery date moves 31% of the SRA's burned acres onto fires no origin-based
table contains. They are the largest fires on record, so 80% of SRA acres is reached only far higher up the size scale. The audit cannot
see any of it, because its protocol samples fires a ground crew can walk.

## 4. The ladder

| Rung | Construction | Lands on (80% boundary) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Fires typed wildfire with SRA origin on the dispatcher's field, weighted by final size | 1,300 acres (−51.7%) | The annual report's own population, ties to it fire for fire | The audit: 64 of 820 audited records are second reports of a fire another agency also filed |
| 1 | Hygiene: mutual-aid duplicates merged through the national incident number | 1,460 acres (−45.7%) | A real double count removed; the audit's duplicates all resolve | The audit: 31 audited fires typed prescribed had escaped and are wildfires from their conversion date in the event log |
| 2 | Escaped prescribed fires added from the event log's conversion events (E33) | 1,680 acres (−37.5%) | Population matches the audit 820 of 820, sizes within 0.5% | The perimeter file: intersected with the map in force, 31% of SRA burned acres lie in fires that started outside the SRA |
| 3 | **Decisive:** every wildfire weighted by its SRA acres (final perimeter inside the map in force on its discovery date), accumulated in order of final size | **2,690 acres** | — | — |

* **Figure shape.** The answer is the maximum cell of the grid; every partial construction stages tankers and crews for fires smaller
  than the ones that burn the SRA. The adopted structure is 21,300 / 2,690 / 310 acres; rung 0 files 9,870 / 1,300 / 140.
* **Partial correction priced (L3).** A solver who intersects perimeters but keeps only SRA-origin fires (cutting the SRA portions of
  their runs into federal land and adding nothing from outside) lands at 1,520 acres (−43.5%), below rung 2.
* **Grid.** Duplicates (kept or merged) × prescribed escapes (out or in) × weight (whole size of SRA-origin fires or SRA acres of every
  fire) gives 8 cells. The nearest non-answer cell is SRA acres with duplicates kept at 2,400 acres (−10.8%), and every toggle moves the
  boundary the same way.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The method says bands cover "50, 80 and 95 per cent of the State Responsibility Area's burned acres". Nothing says
   a fire's acres can fall on both sides of the line, and the annual reports' "SRA acres" are, as labelled, by area of origin.
2. **Corpus blind for a computable reason.** *In every audited fire the final perimeter lies wholly inside one responsibility area,
   because the audit protocol samples fires under 1,000 acres that a ground crew can walk, and none of the 820 crosses a line.* On every
   audit case the SRA portion equals the final size, so rungs 2 and 3 agree.
3. **No arithmetic symptom.** Origin-based totals tie to the annual reports, perimeter areas tie to final sizes within 0.5%, and SRA acres
   sum to the map-intersected total. Nothing fails under any rung.
4. **Not a row predicate.** A fire's weight is the area of its perimeter inside the map version in force on its discovery date, then
   accumulated in size order into a weighted boundary. No incident row carries it.
5. **The enumeration is arithmetic.** 856 outside-origin fires enter the population, and 1,104 SRA-origin fires lose part of their
   weight, by intersection only.
6. **No cutover date.** Map revisions are small annual adjustments that move under 2% of origins, and no series steps. The escaped
   prescribed fires are scattered across all fifteen years.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the incident file still offers origin and size on every
   row.

## 6. The calibration corpus

* **Form.** The 2024 data-quality audit: 820 incidents drawn at random from 2011–2025, each re-verified on the ground and from imagery
  for incident type at final status, duplicate status, origin point, responsibility at origin and final size.
* **What it certifies.** The lower rungs. It confirms 64 duplicates resolved through the national incident number, 31 escaped prescribed
  fires classed as wildfires from their conversion date, responsibility at origin (the dispatcher's field and the map in force agree on
  all 820), and final sizes within 0.5%.
* **What it is blind to.** SRA portions of boundary-crossing fires (above). A solver who back-tests is confirmed at rung 2.
* **Twin pair.** The Ash Creek and Barlow planning units are identical on SRA-origin fires (612 each), their final sizes (88,400 acres
  each), size classes, reporting agencies and escaped prescribed fires. Their SRA acres burned in 2011–2025 are 171,000 and 84,000 (2.04×),
  because three fires from the national forest bordering Ash Creek ran into it. Only the perimeter intersection separates them.
* **Resemblance points at the decoy.** The 2011–2025 SRA-origin size profile most resembles the 2016 annual report's, a season with no
  boundary-crossing megafire, in which origin-based and SRA-acre bands nearly coincide.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The coordination method: "Planning bands cover 50, 80 and 95 per cent of the State Responsibility Area's burned acres,
  2011–2025, accumulated from the largest fire down, and each is stated as a fire size rounded down to the nearest 10 acres." The map
  metadata lists the responsibility classes (state, federal, local) with effective dates. The annual report's tables are headed "by
  responsibility area of origin".
* **Empirical pins.** Duplicate resolution and the escaped-fire rule come from the audit.
* **Voices.** The aviation programme manager: "We plan for the fires that start on our ground; everything else is somebody else's
  dispatch." The agency statistician: "The annual report's SRA acres are the official count, and they reconcile to every incident."
* **Licensed wrong basis.** The method records that the federal partners draw their bands on all fires in the region at their final
  size and will present them at the operating-plan meeting.

## 8. Determinism by construction

* **Small fires.** Fires under 300 acres have no perimeter. In the world none of them starts within a mile of a responsibility line, so
  each one's acres sit wholly on its origin side under any convention.
* **Map version.** Revisions take effect on 1 July. No fire of 300 acres or more burned across a revision date in a parcel whose class
  changed, so "map in force at discovery" and "map in force at containment" give the same intersections.
* **Re-burns.** Overlapping perimeters count once per fire, as burned acres. No band boundary falls between two fires within 10 acres of
  each other, so rounding down and tie rules do not move it.
* **Conversion timing.** An escaped prescribed fire counts its whole final size. Its pre-conversion acres are under 2% of each such fire,
  and including or excluding them files the same rounded boundaries.

## 9. Prompt sketch and deliverables

> The operating plan is signed on 20 March, and its planning bands decide where our contracted tankers and extended-attack crews sit
> next season. Our aviation manager's view is that the fires we plan for are the ones that start on our ground. Give me the three band
> boundaries in acres, each rounded down to the nearest ten, as the line that goes in the plan, and send `planning_bands.xlsx` with the
> build and the sheets below, plus `band_curves.png`.

* `planning_bands.xlsx` — the band build, the four constructions' boundaries with their audit agreement counts (ask C), the retardant
  sheet (ask A) and the crew-availability sheet (ask B).
* `band_curves.png` — the cumulative share of SRA burned acres against fire size on a log axis, from the largest fire down, for the
  origin-based and SRA-acre weightings; the three adopted boundaries as labelled vertical lines; the Ash Creek and Barlow totals
  annotated; and the 31% outside-origin share shaded.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Retardant delivered from each of the five tanker bases in each month from June to October 2025,
  in gallons of mixed product. *Device:* the two bases that mix on site log concentrate and the other three log mixed product, as each
  base's log header and the retardant contract's 1:5.5 mix ratio document. Summing the logs as they stand understates two bases by more
  than 80% in every month.
* **Ask B (device-carried).** Days each of the twelve contracted crews was available to the state in the 2025 season (15 June to
  15 October). *Device:* the national resource system marks a crew available on the day it demobilises, but the crew contract's
  schedule imposes two days' mandatory rest after any assignment of 14 days or more. Counting the system's available days overstates
  eight crews by 2 to 8 days.
* **Ask C (validity).** The three boundaries under each of the four rung constructions, with each construction's agreement count against
  the audit's 820 cases.
* **Decoupling.** The base logs and the crew system share no row with the incident file. Clearing the SRA-acre weighting changes no
  figure in asks A or B.

## 11. Rubric arithmetic

5 bases × 5 months (ask A) + 12 crews (ask B) + 4 constructions × (3 boundaries and an agreement count) (ask C) + the three committed
boundaries and the twin units' totals + 5 named chart parts + 2 files ≈ 67 criteria.

## 12. World-building constraints

* 2011–2025: 9,412 SRA-origin wildfires after merging, 856 outside-origin fires that burned SRA acres, and 31% of SRA burned acres from
  outside-origin fires. 1,104 SRA-origin fires lose part of their weight to federal or local land.
* Duplicates are mostly 300- to 1,600-acre fires on the state-federal line that both agencies staffed. Escaped prescribed fires are 4,000
  to 41,000 acres. Every toggle raises the 80% boundary.
* 80% boundaries by rung are 1,300 / 1,460 / 1,680 / 2,690 acres. The other grid cells are 2,090, 1,500, 2,340 and 2,400 acres, and none
  lies within 10% of 2,690.
* The audit's 820 cases are all under 1,000 acres and none crosses a responsibility line. The dispatcher's responsibility field agrees
  with the map in force at every origin, so origin needs no repair.
* Ash Creek and Barlow are identical on every incident column. Their SRA-acre totals differ only through three perimeters.
* The base logs and the crew system touch no incident.
