# DS07 — How many main breaks the anode programme will avoid next year, when the pilot's effect lives only in corrosive soil

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · regulated water utility performance |
| Mirrors | Committing to the benefit of a fix that a pilot measured on a different mix of units (Google and Meta reliability fixes that only help one hardware generation, Amazon warehouse interventions that only work on one floor layout, cloud mitigations effective on one kernel line) |
| Decision shape | One figure committed at a date: breaks avoided next year, filed as a regulatory performance commitment |
| Committed call | The number of main breaks the 620 km anode programme will avoid next regulatory year, in whole breaks |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern E (conditioned yield: the pooled pilot effect applies to no main), with a suppressed cohort rate recovered from published totals (#24) at rung 1 |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #13 validates on one population, applies to another · #24 treats an unpublished figure as unknown · #6 treats a mixed segment all one way · #15 follows the requester's hunch over the rule |
| Calibration form | Parallel-run overlap: soil-resistivity probes and the national soil survey observed side by side on all 412 pilot segments for 18 months |
| Driving force | The pilot's 48% (after controlling for the hard winter) is correct and applies to no main on next year's list. Anodes stop corrosion breaks. Cast-iron mains in shrink-swell clay break from ground movement, and every retrofitted main in clay broke at its control's rate. Corrosivity sits in the soil survey, reached by a spatial join the pilot log never makes. The pilot's baseline breaks were 60% in corrosive soil; next year's list, picked for its break counts, is 29% corrosive. |

## 1. Situation

A water utility must file, by the end of the month, the number of main breaks its anode retrofit programme will avoid next regulatory
year. The regulator holds the utility to that figure. The programme list is fixed: 620 km of small cast-iron mains, chosen because they
break most. A three-year pilot retrofitted 412 segments and logged breaks before and after, alongside a listed set of control mains. The
planning standard sets baselines from the regulator's published cohort rates, and the regulator's table suppresses the smallest cohort. The
asset director wants the filing to carry the pilot's number.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The pilot's before-and-after 41% and its controlled
  48% are right for the pilot, and so are the regulator's table, the soil survey, the probes and the corrosion-zone map. The difficulty is
  that the effect is a mixture of two soils, and next year's list carries the other mix.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. The pilot's controlled effect applied to a correct baseline still files 145 breaks, and every
  count reconciles.
* **Instrument repair.** Record every break perfectly and probe every main. The pooled effect is still 48%, the clay mains still break from
  movement, and the list is still 29% corrosive.
* **Lens swap.** The naive figure transports the pilot's segments to next year's list. The answer re-weights a soil-specific effect to a
  different population of mains, in a year the pilot does not cover.

## 3. The driving force

A strong solver builds the list's baseline from the regulator's cohort rates, recovers the suppressed cohort from the published row total,
and replaces the pilot's raw before-and-after with a difference-in-differences against the listed control mains, because a hard winter
raised breaks network-wide in the after period. Each step is competent, and the controlled 48% is right. But anodes only arrest corrosion.
Joined to the soil survey, the pilot splits absolutely: in corrosive soil, retrofitted mains broke 80% less than their controls, and in
non-corrosive clay they broke at exactly their controls' rate. The pilot sites were chosen by break history, and 60% of their baseline
breaks were in corrosive soil. Next year's list was chosen the same way, but in a valley where the high break counts come from clay
movement, and only 29% of its baseline breaks are in corrosive soil. Nothing in the pilot log carries soil, so every group-by on its own
columns returns the pooled figure.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Regulator cohort rates × km for the list (the suppressed corrosive cohort read at its row's published rate, 48.4), pilot before-and-after 41% | 116 (+68%) | The planning standard and the pilot's own figure | The regulator's table: the row total and the published clay cell fix the corrosive cell at 62.0 breaks per 100 km |
| 1 | Suppressed cell recovered from the published totals (#24) | 124 (+79%) | A complete baseline with no unknown cell | The control mains: breaks rose 13% network-wide in the after period, so before-and-after understates |
| 2 | Difference-in-differences against the listed control mains (48%) | 145 (+109%) | A controlled effect on a correct baseline | The soil survey joined to the pilot segments: every retrofitted main in non-corrosive soil broke at its control's rate |
| 3 | **Decisive:** effect by corrosivity through the survey join (80% and 0%), applied to the list's corrosive baseline (86.8 breaks) | **69 breaks** | — | — |

* **Figure shape.** The corrections walk up (+6.7%, +17.1%) and the decisive move reverses them (−52%). Offsets from the answer: rung 0
  +68%, rung 1 +79%, rung 2 +109%.
* **Partial correction priced (L3).** Conditioning on the planners' corrosion-zone polygons instead of the survey marks 70% of the list
  corrosive and files 170 (+144%), further off than rung 2. Comparing anode mains with unretrofitted mains across the network finds the
  anode mains breaking 1.3× as often and files zero (−100%), because historical anodes went on the worst corrosive mains.
* **Grid.** Suppressed cell (row rate, recovered) × effect (before-and-after, controlled) × conditioning (pooled, survey) gives 8 cells. The
  four pooled cells file 116 to 145. The nearest wrong cell is the recovered cell with before-and-after conditioning, 59 (−14.6%), and it
  costs one omission: the control mains. Skipping the recovery files 54 (−22%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one effect. No document links anodes to soil, or says clay mains break from movement.
2. **No sweepable corpus nominates it.** *In the pilot log every zone, material, diameter and age band holds corrosive and clay segments in
   the same proportion, because the pilot sites were chosen on break history alone.* Every group-by on the log's own columns returns 48%,
   and the split appears only through the spatial join.
3. **No arithmetic symptom.** Pilot breaks, control breaks, list kilometres and cohort rates reconcile under every rung, and the pooled
   effect is exactly the pilot's.
4. **Not a row predicate.** It needs a spatial join of segments to survey map units, a difference-in-differences within each soil class,
   and a re-weighting of the list's cohort baseline by soil.
5. **The enumeration is arithmetic.** Which of next year's breaks are preventable is computed from the survey and the cohort rates. No column
   marks a main as treatable.
6. **No cutover date.** The hard winter is a decoy that the control mains absorb. The soil effect is constant through the pilot and steps no
   series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The parallel run: for 18 months, field resistivity probes and the national soil survey's corrosivity class were both recorded on
  all 412 pilot segments.
* **What it certifies.** That the survey measures the property. Probe readings fall below 1,800 or above 3,200 ohm-cm, with none between,
  and the survey's class matches the probe side on 412 of 412. The planners' corrosion-zone polygons match on 281.
* **What it pins, and what it cannot.** It pins the survey as the join for next year's list, which has no probes. It carries no break data,
  so it says nothing about the effect until joined to the pilot log.
* **Twin pair.** Pilot zones Millbrook and Ashby are identical on every pilot-log column: 64 km each, the same material and age mix, 61
  breaks in the three years before retrofit, retrofitted in the same quarter. Their controlled after-period breaks are 46 and 24 (1.9×),
  at corrosive shares of 30% and 75%. Only the survey join separates them.
* **Every rule exercised.** One zone is entirely clay, which tests the zero, and one is entirely corrosive, which tests the 80%.
* **Resemblance points at the decoy.** By material, diameter and age, next year's list most resembles Ashby, the pilot's best zone.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The regulator's performance-commitment rule: the utility files the breaks a funded programme will avoid in the next
  regulatory year. The planning standard: baselines are the regulator's cohort rates × km. The pilot design note: the list of control mains.
  One sentence each.
* **Empirical pins.** The 80% and 0% effects, from the pilot joined to the survey. The survey's validity, from the parallel run.
* **Voices.** The asset director: "The pilot showed 41%; that's what we commit." The network engineer: "Cast iron is cast iron, whatever
  it's buried in." The regulatory liaison: "They'll expect the pilot's number in the filing."
* **Licensed wrong basis.** The regulator's guidance records that its engineers review programmes on the pilot-average effect and will see
  that basis.

## 8. Determinism by construction

* **Spatial join.** No segment crosses a survey map-unit boundary, so centroid and majority-length assignment agree.
* **Probe gap.** No probe reading falls between 1,800 and 3,200 ohm-cm, so any class threshold in that range selects the same segments.
* **Controls.** The design note lists every control main, and the hard winter lifts controls and retrofits alike.
* **Suppressed cell.** The table publishes km and rates for the row and the clay cell, so the corrosive cell is exact (62.0), not bounded.
* **Maturity.** Every pilot segment has a full 24-month after period, and the figure is filed in whole breaks (69.4 rounds to 69).

## 9. Prompt sketch and deliverables

> Our filing to the regulator is due on the 30th, and it has to commit to the main breaks the anode programme will avoid next year. The
> asset director wants to put in the pilot's number. Give me the figure we should commit to, in whole breaks, in a sentence I can put in
> the filing. Send `anode_commitment.xlsx`, a chart `breaks_avoided.png`, and a one-page `filing_note.pdf`.

* `anode_commitment.xlsx` — the commitment build, the leakage sheet (ask A), the interruptions sheet (ask B) and the pilot sheet (ask C).
* `breaks_avoided.png` — two panels: the pilot's controlled effect by soil class for each pilot zone as paired bars, and the commitment
  under the four rung constructions with the answer marked and the list's corrosive share annotated.
* `filing_note.pdf` — the committed figure, and why it is not the pilot's.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine pressure zones, water lost per km of main per day over the last year.
  *Device:* the zone meters were recalibrated in March, and the metering standard applies the logged correction factors back six months.
  Raw readings misstate four zones by 6–11%.
* **Ask B (device-carried).** Supply interruptions of more than three hours, by month. *Device:* one burst affecting several streets is one
  event in the interruption register, with a child record per street. Counting child records inflates the winter months by a third.
* **Ask C (validity).** Breaks avoided under each of the four rung constructions, and the pilot's controlled effect for each zone by soil
  class.
* **Decoupling.** Clearing the survey join changes no figure in asks A or B. Zone meters and interruption events never enter the commitment.

## 11. Rubric arithmetic

9 zones (ask A) + 12 months (ask B) + 4 constructions + 9 zones × 2 soils (ask C) + the committed figure, the list's corrosive share and
the two soil effects + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* The list: 480 km in clay at 45.0 breaks per 100 km (published) and 140 km in corrosive soil at 62.0 (suppressed; the row is 2,000 km at
  48.4 and the clay cell 1,600 km at 45.0). Baseline 302.8 breaks, 86.8 corrosive.
* The pilot: 60% of baseline breaks in corrosive soil. Pooled before-and-after 41% and controlled 48%; by soil 80% and 0% (68.3% and 0%
  before-and-after).
* Rung figures 116 / 124 / 145 / 69. The nearest wrong cell is 59. The polygons mark 70% of the list corrosive.
* The twin zones are identical on every pilot-log column. Every zone, material and age band in the log is balanced on soil.
* Meter corrections and interruption child records never touch breaks, segments, soils or cohort rates.
