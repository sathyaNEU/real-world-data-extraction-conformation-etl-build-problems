# AD23 — Which area gets next year's temporary dense seismic array, when one area's catalog is swollen by another area's aftershocks

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · energy regulation and induced seismicity |
| Mirrors | Counting independent incidents when one large event's aftermath spills across the boundaries the counts are kept by (cascading outages counted per cloud region, fraud rings counted per marketplace category, ticket storms counted per product line) |
| Decision shape | Which of N gets one scarce thing: the commission's single 40-station temporary array for next year |
| Committed call | The one area of interest the array is deployed in, and its independent earthquakes per million barrels of deep disposal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · two flawless grains (E07): catalog events against independent earthquakes, the bridge built region-wide because aftershock productivity scales with mainshock size and crosses area lines; a suppressed cell bounded at the lower rung (E25) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #24 treats an unpublished figure as unknown · #14 coarsens the segment it was asked about |
| Calibration form | Counterparty acknowledgement file: the seismic network operator's acknowledgements of 340 events the commission queried, each classified as independent, an aftershock of a named event, or a blast |
| Driving force | The monitoring rule counts independent earthquakes, and a strong solver declusters each area's catalog. But a sequence belongs to the region, not to the area: B's M4.6 mainshock sat 3 km from the D line and threw 60 of its 140 aftershocks into D. Declustered inside D's own catalog, with no mainshock to hang them on, 54 of them pass as independent and D tops the ranking. Declustering the whole catalog and assigning each sequence to its mainshock's area is the only reading the network's acknowledgements reproduce. |

## 1. Situation

A state oil and gas commission has one temporary dense seismic array (40 stations) for next year, to be sited in one of six areas of
interest. Its monitoring rule sends the array to the area with the most independent earthquakes of magnitude 2.5 or more per million
barrels of deep disposal over the last twelve months. The pack carries the regional catalog, the public well-volume report (wells under a
confidentiality order shown as "C"), the commission's annual disposal summary with area totals, the area boundaries, and the network
operator's acknowledgement file.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: every catalogued event, every public volume, every area total and every acknowledgement. The
  seismologist's M4.8 is real and the largest. Nothing reported is overturned; the difficulty is that the rule's unit, the independent
  earthquake, is a region-level construction that no area's catalog contains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. Bounding the confidential volumes and declustering each area's catalog, the natural careful build,
  still names D.
* **Instrument repair.** Densify the network further; magnitude 2.5 is already well above completeness everywhere. A better instrument
  records the same aftershocks in the same places, and their dependence on a mainshock across a boundary is still a construction.
* **Lens swap.** The naive unit is the catalog event; the answer's unit is the independent earthquake, built region-wide and assigned by
  mainshock, a different population that removes 60 events from D and none from E.

## 3. The driving force

A strong solver refuses raw event counts, which the M4.8's 150 aftershocks dominate, divides by deep disposal, notices that confidential
wells leave B's public volume at a third of its true total and recovers it from the disposal summary's area totals, then declusters, as
the rule's "independent earthquakes" demands. It filters the catalog to each area, runs the windows, and finds D on top. Each step is
competent. But aftershock windows scale with the mainshock's magnitude, and B's M4.6 struck 3 km from the D line; 60 of its aftershocks
fall in D. Inside D's own catalog there is no M4.6 to attach them to, so the windows hang a few on each other and 54 survive as independent.
Declustered region-wide, every one of the 60 is a dependent of an event in B, and each sequence counts once, in the area of its mainshock.
D falls from 18.1 to 10.8 per million barrels and E, a steady rise of small independent quakes beside a growing disposal well, leads at 15.0.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Catalog events of magnitude 2.5 or more per area, last twelve months | A (212; 1.51× D) | The catalog as published, the largest earthquake inside it | The rule counts per million barrels of deep disposal, and A injects the most |
| 1 | Events per million barrels, confidential wells left out as unknown | B (33.3; 1.51× A) | The rule's denominator from the public report, nothing guessed | The disposal summary's area totals: B's confidential wells carry 8.2 of its 12.1 million barrels |
| 2 | Bounded volumes; each area's catalog declustered on its own | D (18.1; 1.21× E) | The rule's unit, independent earthquakes, by the standard windows, on the right denominator | The network's acknowledgements: 53 events in D that this build keeps are classified as aftershocks of B's M4.6 |
| 3 | **Decisive:** the whole catalog declustered, each sequence counted once in its mainshock's area | **E (15.0)** (5th of 6 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (97) and rung 1 (16.0) and 2nd on rung 2, 1.21× behind D, and leads only rung 3, 1.39× D.
  Intermediate leaders hold margins of 1.51×, 1.51× and 1.21×.
* **Discriminator dominance.** D carries a 1.21× advantage over E into rung 3. Region-wide declustering multiplies D's count by 0.60 and E's by
  1.00, an edge of 1.68 against the 1.2 × 1.21 = 1.45 required; net 1.39×.
* **Partial correction priced (L3).** A solver who bounds the volumes but counts events, not independent earthquakes, has C and D within 4%
  of each other (19.6 and 18.9) and names C. A solver who declusters region-wide but leaves confidential volumes out names B again, at 12.8.
* **Grid.** Volumes (public or bounded) × unit (events, per-area declustered, region-wide declustered) gives six cells: public-volume cells
  name B under every unit; bounded cells name C, D and E. Only bounded volumes with region-wide sequences name E, and the nearest wrong cell
  (D) needs each area's catalog declustered on its own.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule says "independent earthquakes" and names areas. No document says sequences cross area lines, and the
   catalog is published by area.
2. **The corpus pins a construction, not a menu.** Region-wide declustering reproduces 340 of 340 acknowledged classifications; per-area
   declustering 287, every miss an aftershock it calls independent, so it also overstates the queried set's independent count. The rule is
   a construction: windows applied across the whole catalog, sequences linked across boundaries, and each assigned to its mainshock's area,
   with no column carrying the assignment.
3. **No arithmetic symptom.** Events tie to the catalog, bounded volumes to the area totals within rounding, and per-area declustering runs
   cleanly.
4. **Not a row predicate.** It needs space-time windows scaled by each event's magnitude, applied across all areas, a linkage of dependents to
   mainshocks, and a re-count by mainshock area.
5. **The enumeration is arithmetic.** Which events are dependent is computed; nothing in the catalog marks an aftershock.
6. **No cutover date.** B's sequence has a date, and its effect on B is visible to anyone; its spill into D shows no step in D's own series
   that per-area declustering does not absorb.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The network operator's acknowledgement file: 340 events the commission queried over three years, each acknowledged as
  independent, as an aftershock of a named event, or as a blast.
* **What it pins.** Region-wide Gardner–Knopoff and nearest-neighbour declustering both reproduce all 340; per-area declustering 287;
  Reasenberg's method region-wide 331, keeping E first.
* **Twin pair.** D's first and fourth quarters are identical on events (35 each), magnitude distribution and depth profile. The
  acknowledgements count 34 and 17 independent earthquakes (2×): the fourth quarter's events include 18 of B's aftershocks.
* **Every rule exercised.** One queried event was a quarry blast, so blasts are excluded under every rule; one sequence in the corpus crossed
  two boundaries, so assignment by mainshock is tested.
* **Resemblance points at the decoy.** By catalog profile D most resembles the area where last year's array mapped a newly active fault.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The monitoring rule: the array goes to the area with the most independent earthquakes of magnitude 2.5 or more per million
  barrels of deep disposal over the last twelve months. The disposal summary's area totals include confidential wells.
* **Empirical pins.** Region-wide declustering with assignment by mainshock, from the acknowledgement file.
* **Voices.** The commission's seismologist: "A 4.8 is a 4.8; the array belongs where the biggest one struck." D's area manager: "D's catalog
  has doubled this year; something is waking up under it."
* **Licensed wrong basis.** The rule records that the operators' association counts catalog events per area and will present its counts at
  the siting hearing.

## 8. Determinism by construction

* **Completeness.** Magnitude 2.5 is at least 0.7 above completeness in every area in both years, so no completeness choice moves a count.
* **Declustering.** Gardner–Knopoff and nearest-neighbour methods agree event by event region-wide; Reasenberg differs on nine events and
  changes no rank.
* **Volumes.** Area totals are published to 0.1 million barrels, so each bounded volume is exact within 0.05; E's wells are all public.
* **Window.** Twelve months by origin time; B's sequence and all its aftershocks fall inside it.

## 9. Prompt sketch and deliverables

> Next year's temporary dense array can go to one area of interest. Our seismologist would put it where the largest earthquake struck. Name
> the area in a sentence for the commission's order, with `array_siting.xlsx` holding the sheets below, the map `sequence_attribution.png`,
> and a short `order_memo.pdf`.

* `array_siting.xlsx` — the area build under each unit, the citation sheet (ask A), the felt-report sheet (ask B) and the acknowledgement
  back-test (ask C).
* `sequence_attribution.png` — a map of the six areas with the last twelve months' events coloured by the sequence they belong to, B's
  mainshock and its aftershocks across the D line outlined, area boundaries drawn, and each area's independent count per million barrels in
  its label.
* `order_memo.pdf` — the committed area and why A, B and D are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each area, disposal wells cited for pressure-monitoring violations last year and the share
  re-cited. *Device:* a violation cited again after a failed correction is logged as a new citation carrying a repeat flag and the
  original's number, per the enforcement guide. Counting citations as wells overstates the three areas with repeat citations. The array
  build never reads citations.
* **Ask B (device-carried).** For each area, public felt reports in each quarter of the last year. *Device:* a respondent who revises a
  report keeps the same respondent ID and the revision replaces the original, as the felt-report guide documents. Counting submissions
  double-counts revisions in every quarter with a large event.
* **Ask C (validity).** For each of the four rung constructions, the acknowledged classifications it reproduces out of 340.
* **Decoupling.** Clearing the region-wide declustering changes no figure in asks A or B.

## 11. Rubric arithmetic

6 areas × 2 (ask A) + 6 areas × 4 quarters (ask B) + 4 constructions (ask C) + the committed area, its rate and the margin over D + 5 named
chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* A: M4.8 with 150 aftershocks, 62 independent, 14.0 million barrels. B: M4.6 with 140 aftershocks (80 in B, 60 in D), 50 independent, 12.1
  million (3.9 public). C: M4.1 with 70 aftershocks, 61 independent, 6.7 million. D: 80 independent plus B's 60, 7.4 million; per-area
  declustering keeps 54 of the 60. E: 91 independent, 6.06 million. F: 60 independent, 7.1 million.
* Rung leaders are A, B, D, E; E is 5th / 5th / 2nd (1.21×) / 1st and leads rung 3 by 1.39×.
* The acknowledgement file holds 340 events; D's first and fourth quarters are identical on every catalog column.
* Repeat citations and revised felt reports never touch the catalog, the volumes or the acknowledgements.
