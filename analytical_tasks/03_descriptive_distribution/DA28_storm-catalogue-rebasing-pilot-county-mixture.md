# DA28 — Which rebasing structure a reinsurer adopts for its convective loss catalogue, when the damage estimates changed basis between the decades it compares

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · catastrophe loss trends and reinsurance pricing |
| Mirrors | Trend studies across a change in how the outcome is measured (incident severity scored on a new rubric, revenue booked under a new recognition standard, cloud cost data after a metering change), where a published overlap of the two measures is the only bridge |
| Decision shape | A structure the body adopts: the catalogue structure (peril scope and conversion populations) the model governance committee approves for the frequency study |
| Committed call | The rebasing structure adopted, and the decade ratio of large-loss episodes it implies, to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (a reproduction gate over the overlap's published cells), with a mixed segment split through a join at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #6 treats a mixed segment all one way |
| Calibration form | Parallel-run overlap: the 2014–2016 dual-estimate pilot, publishing survey-basis and claims-basis property damage for 48 state × event type × year cells |
| Driving force | Claims-linked damage estimates were produced only for damage in counties enrolled in an insurer-reporting pilot; everywhere else the claims field repeats the survey figure. Each published overlap cell is a mixture of the two, weighted by its damage in pilot counties, a property reached by joining the county roster to the episode records. Only that mixture reproduces all 48 cells, and it converts the earlier decade's large metropolitan hailstorms far more than any per-peril factor. |

## 1. Situation

A reinsurer's research team reports that convective storm episodes causing at least $100 million of property damage (2023 dollars) nearly
doubled between 1996–2005 and 2014–2023, and proposes a frequency loading at the January renewals. The model governance committee must first
approve the catalogue structure the trend is measured on. Between the decades the national damage record began carrying a claims-linked
estimate. A three-year pilot published both estimates side by side for 48 cells. The governance standard sets the gate a rebasing must
pass.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the storm records, both damage estimates, the pilot's published cells, the price and housing
  series. The research team's count is right on its basis and nobody's figure is overturned. The difficulty is which conversion makes two
  decades comparable.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the research team's note and both voices. Price- and exposure-adjusted counts still show a near-doubling, and
  the obvious per-peril rebasing still leaves a 23% rise.
* **Instrument repair.** Make every estimate perfect on its own basis: the earlier decade still has no claims-linked estimate, because
  that instrument did not exist. Putting the two decades on one basis remains a choice the overlap must settle.
* **Lens swap.** The naive comparison sets 1996–2005 survey estimates against 2014–2023 claims-linked ones. The answer restates the earlier
  decade's episodes on the later basis, county by county: different figures for a different decade's population.

## 3. The driving force

A strong solver aggregates events to episodes, restates damage in 2023 dollars and at 2023 housing exposure, applies the treaty's named-storm
clause to flash floods, and then sees the pilot. It converts the earlier decade with one factor per peril from the pilot's totals, a
standard rebasing, and the rise falls from 75% to 23%. The governance standard will not take it: it reproduces 11 of the 48 published
cells. The cells vary because each one mixes two populations. Damage in counties enrolled in the insurer-reporting pilot carries a claims
estimate 2.30 times the survey figure for hail and 1.45 times for wind. Damage elsewhere carries the survey figure unchanged. The earlier
decade's large hailstorms fell mostly on pilot metropolitan counties, so the mixture converts them far more than the pooled factor does.
On one basis the decade ratio is 1.04.

## 4. The ladder

| Rung | Construction | Adopts | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | National convective event group, 2023 dollars and housing exposure, no rebasing | Ratio 1.95 (41 to 80 episodes): a frequency trend | The research memo's own adjustments, applied cleanly | The treaty wording: flood within 72 hours of a named system's passage is named-storm peril |
| 1 | Treaty scope: flash floods inside a tropical system's footprint moved out through the track file (a mixed segment split by a join) | Ratio 1.75 (40 to 70) | The peril now matches the contract the loading prices | The pilot's cells: claims-linked estimates run above survey estimates |
| 2 | Earlier decade rebased by one factor per peril from the pilot totals (hail 1.62, wind 1.21, tornado 1.00, flood 1.05) | Ratio 1.23 (57 to 70) | The textbook rebasing, and it uses the committee's own overlap | The governance gate: it reproduces 11 of 48 published cells |
| 3 | **Decisive:** two conversion populations per peril, pilot-county damage and the rest, mixed by each episode's county damage | **Ratio 1.04 (67 to 70)**: no frequency trend | — | — |

* **Figure shape.** Every correction walks the ratio down and the answer is the minimum cell. Rung offsets from the answer are +87%, +68%
  and +18%.
* **Partial correction priced (L3).** A solver who applies the pilot factors to hail but not wind lands at 1.15 (+10%). One who reads the
  roster as of the earlier decade, when no county was enrolled, converts nothing and is back at 1.75.
* **Grid.** Scope (national group or treaty) × rebasing (none, per peril, per state and peril, pilot mixture) = 8 cells: 1.95, 1.36, 1.29,
  1.16 and 1.75, 1.23, 1.17, 1.04. The nearest wrong cell is the pilot mixture on the national scope, 1.16 (+11%), which needs the decisive
  construction with the treaty clause ignored.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot's documentation describes the claims-linked field but not where it was produced. The county roster ships
   in the pilot's annual report as a list of participating counties, with no link to the estimates.
2. **Pattern B, a gate passed by a construction.** The pilot mixture reproduces 48 of 48 cells to the published two decimals. The best
   rival (one factor per state and peril) reproduces 30 of 48, and one factor per peril 11 of 48. Every rival under-converts the cells
   with high pilot shares, so they miss in one direction and fail the overlap totals too. The mixture is a construction: it needs the
   roster joined to each cell's survey damage by county and two factors per peril recovered across cells.
3. **No arithmetic symptom.** Episode totals tie to event rows, the cells reconcile to survey totals, and per-episode ratios are not
   published, so no bimodality shows.
4. **Not a row predicate.** Cell weights are damage shares by county pilot status; factors are recovered across cells; the earlier
   decade's episodes are converted county by county and recounted above the threshold.
5. **The enumeration is arithmetic.** No column marks an estimate's basis or a county's enrolment.
6. **No cutover date.** The pack carries only the two reference decades and the overlap. Enrolment dates are not shipped, and no series
   covers the years the claims field was phased in.
7. **Survives deletion.** With every voice removed, the per-peril rebasing still stops at 1.23.

## 6. The calibration corpus

* **Form.** The dual-estimate pilot, 2014–2016: survey-basis and claims-basis property damage published for 48 cells (10 states × the
  perils present × 3 years), with episode counts.
* **What it certifies.** That the bases differ, and by how much in total, so a solver who back-tests finds rung 2's factors exactly.
* **What pins the structure.** The reproduction gate: only the pilot-county mixture returns every cell, with factors hail 2.30, wind 1.45,
  tornado and flood 1.00.
* **Twin pair.** Two 2015 hail cells in neighbouring states are identical on survey damage, episode count, metropolitan share and peril.
  Their published ratios are 2.12 and 1.05 (2.0×). 86% of the first cell's damage fell in pilot counties and 4% of the second's.
* **Resemblance points at the decoy.** Cells of the same peril look alike on every published column, which invites one factor per peril.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The governance standard: a catalogue may be rebased only by a conversion that reproduces every published pilot cell,
  and rebasing restates the earlier decade on the later decade's basis. The treaty wording carries the named-storm clause. The research
  memo fixes 2023 dollars, housing-unit exposure weighted by county damage share, and episode aggregation.
* **Empirical pins.** The two conversion populations and their factors, from the cells.
* **Voices.** The research lead: "Twice the large storms is twice the hazard; the signal is in the counts." The pricing actuary: "Every
  rebasing I have signed used one factor per peril."
* **Licensed wrong basis.** The governance standard records that the broker's analytics team trends the national convective group in real
  dollars without rebasing and will present that view at the renewal meeting.

## 8. Determinism by construction

* **Counties.** Each county belongs to one forecast area and its roster status is fixed across the overlap and the later decade.
* **Episodes.** Every episode has one ID; multi-county episodes are converted county by county on their survey damage shares.
* **Threshold.** No converted earlier-decade episode lands within 3% of $100 million, so rounding conventions converge.
* **Named-storm clause.** Footprint and timing come from the track file, and every flash-flood episode is either inside a footprint within
  72 hours or at least 10 days clear.

## 9. Prompt sketch and deliverables

> The committee approves the catalogue structure for the convective frequency study before anyone prices a loading, and research tells me
> the big storms have doubled. Tell me which structure we adopt and the decade ratio of large-loss episodes it gives, to two decimals, in
> a sentence for the minutes. Send `catalogue_structure.xlsx`, a chart `decade_ratio_by_structure.png`, and a one-page
> `committee_paper.pdf`.

* `catalogue_structure.xlsx` — the rebasing build, the tornado sheet (ask A) and the record-coverage sheet (ask B).
* `decade_ratio_by_structure.png` — decade ratios under the four rung structures as a descending staircase, with each structure's
  reproduced-cell count labelled, the twin cells inset and the adopted structure marked.
* `committee_paper.pdf` — the adopted structure, its ratio, and why each rival fails the gate.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 10 states, tornado episodes rated 2 or higher in each decade. *Device:* the rating
  scale changed in 2007, and the dictionary's crosswalk maps the old scale to the new one. Counting the raw ratings mixes scales and
  shifts six states' later-decade counts.
* **Ask B (device-carried).** For each state and decade, the share of episodes carrying a property damage estimate. *Device:* the export
  format note distinguishes "0.00K" (surveyed, no damage) from blank (not surveyed); treating both as zero inflates coverage in the earlier
  decade. Every large-loss episode carries an estimate.
* **Ask C (validity).** Cells reproduced and the decade ratio under each of the four rung structures.
* **Decoupling.** Clearing the pilot mixture changes no figure in asks A or B.

## 11. Rubric arithmetic

10 states × 2 decades (ask A) + 10 × 2 (ask B) + 4 structures × 2 (ask C) + the adopted structure, its ratio and the two decade counts + 5
named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Large-loss episodes: rung 0 41 → 80; rung 1 40 → 70; rung 2 57 → 70; rung 3 67 → 70. Grid cells 1.95, 1.36, 1.29, 1.16 / 1.75, 1.23,
  1.17, 1.04. Hail-only rebasing gives 61 → 70 (1.15).
* Pilot factors: hail 2.30 and wind 1.45 in pilot counties, 1.00 elsewhere and for tornado and flood. The overlap's hail damage is 47.7%
  in pilot counties; the earlier decade's large hail damage is 80%.
* Cells reproduced: mixture 48, per state and peril 30, per peril 11. The twin cells match on every published column.
* Rating-scale changes and blank estimates never touch an episode of $100 million or more.
