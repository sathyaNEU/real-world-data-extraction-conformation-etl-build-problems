# FC50 — How many of the ten summer surge medic units each battalion district needs, when district dispatch changes which calls a unit serves and every closed summer was staffed area by area

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · fire and emergency medical services planning |
| Mirrors | Percentile staffing of over-dispersed demand when the pool that serves it changes shape (contact centres merging queues, trust-and-safety teams moving to follow-the-sun pools, field-service crews dispatched across territories), where every closed period was staffed queue by queue |
| Decision shape | An allocation under a cap: up to ten surge medic units for the summer's weekend evenings, across three battalion districts, the rest released to the county |
| Committed call | Surge units for the North, Central and South districts, and how many of the ten are released, as whole numbers |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · L1 with S4 (the close-outs certify area-level staffing and are blind to the pooled requirement district dispatch creates), with a suppressed cell bounded (measured #24) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the department's summer close-outs for 2023–2026, per planning area and block, with calls, units on duty, shortfall evenings and unanswered-call minutes |
| Driving force | The standard staffs so that on nine weekend evenings in ten the units that answer a call can answer every call in the block. Until now that meant each planning area's own units, so area-level 90th percentiles were the requirement and every close-out confirms them. From June, units dispatch across battalion districts, so the units answering a North call serve both North areas, and the requirement is the 90th percentile of the district's evening, which is smaller than the sum of its areas' because the areas' busy evenings do not all coincide. Shared heat evenings make the saving smaller than independence suggests, so it must be read from the areas' joint evening counts. |

## 1. Situation

A city fire department runs medic units from five planning areas. For June to August it holds a surge pool of ten medic units for the
weekend 20:00–24:00 block; any it does not need go to the county's mutual-aid roster for the summer. The deployment standard staffs so that
on nine weekend evenings in ten the units that answer a call can answer every call in the block, at 1.2 unit-hours a call. From June the
deployment plan dispatches medic units across three battalion districts: North (areas 1 and 2), Central (areas 3 and 4) and South (area 5).
The pack holds the public call dataset (station-area counts by block and day, cells of one or two calls suppressed), the unsuppressed
planning-area daily totals, the unit status log, the close-outs, the base roster and the deployment plan. The deployment order is signed
on 1 May.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published counts and totals, the status log, the close-outs and the roster. No stakeholder's
  reading of their own numbers is overturned; each area really did need its area-level units on nine evenings in ten. The difficulty is
  which calls the units will answer next summer, which no closed summer recorded.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the planning analyst's view and every voice. Area-level percentiles summed into districts are still the
  natural build, every close-out still confirms them, and they still take all ten surge units.
* **Instrument repair.** Imagine every call recorded unsuppressed. The areas' counts would be exact, but no closed summer dispatched across
  districts; the district requirement still has to be built from the areas' joint evenings.
* **Lens swap.** The naive read and the answer staff different populations: each area's calls for each area's units, against each
  district's calls for the units that will serve the whole district.

## 3. The driving force

A strong solver builds each planning area's weekend-evening counts, sees variance far above the mean and fits a negative binomial rather
than a Poisson, and recovers the suppressed station-area cells from the published area totals instead of reading them as zero. Area by area
the 90th-percentile evenings need 6, 5, 8, 3 and 3 units against 3, 3, 5, 2 and 2 on the base roster, so all ten surge units go out:
North 5, Central 4, South 1. The close-outs confirm the method for every closed summer. Every step is correct for a department that
dispatches inside areas. But from June the units answering a North call are the North district's units, wherever in the district they
stand, so the requirement is the 90th percentile of the district's evening, not the sum of its areas' 90th percentiles: an evening when
area 1 is at its 90th percentile is seldom one when area 2 is. The saving is real but not the independent one: shared heat evenings move
both areas together, so the joint percentile has to come from the areas' counts on the same evenings. North needs 9 units, not 11; Central
10, not 11. Seven surge units cover the summer, and three go to the county.

## 4. The ladder

| Rung | Construction | Lands on (surge units: North / Central / South; released) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Poisson 90th percentile per area on the published counts, suppressed cells read as zero | 2 / 1 / 0; 7 released | The department's existing staffing sheet, run on the public data | The close-outs: every area's weekend-evening variance runs two to four times its mean, and Poisson staffing reproduces none of the closed shortfall evenings |
| 1 | Negative binomial per area, suppressed cells read as zero | 3 / 2 / 0; 5 released | Over-dispersion handled, and the fit tracks the close-outs' shortfall pattern | The planning-area daily totals: summing station areas with suppressed cells as zero falls short of the published totals on 61% of evenings |
| 2 | Suppressed cells bounded by the area totals less the other blocks, negative binomial per area | 5 / 4 / 1; 0 released | Exact counts, the right distribution, and the close-outs reproduced evening by evening | The deployment plan: from June medic units dispatch across battalion districts, so a call is answered by any unit in its district |
| 3 | **Decisive:** the 90th percentile of each district's evening, read from its areas' counts on the same evenings | **3 / 3 / 1; 3 released** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the surge up (3, 5, 10 units) and the decisive rung reverses it to 7, inside the walk, so a solver who
  stops at rung 2 commits every surge unit and leaves the county three short.
* **Partial correction priced (L3).** A solver who pools by district but convolves the areas' fitted distributions as if independent
  needs 8 units in North, not 9, and releases 4 (surge 6, −14%). One who pools on counts with suppressed cells read as zero releases 6
  (surge 4, −43%). One who pools the whole city as one district needs 4 surge units (−43%).
* **Grid.** Distribution (Poisson, negative binomial) × suppressed cells (zero, bounded) × service unit (area, district) = 8 cells. Area
  cells give 3, 4, 5 and 10 surge units; district cells give 2 to 4 except the full construction at 7. The nearest wrong cells are 5
  (−29%) and 10 (+43%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard speaks of the units that answer a call; the deployment plan speaks of response times and districts.
   No document says the requirement changes, or that it is a percentile of a district's evening.
2. **Corpus blind to the pooling.** *In every closed summer each area's medic units answered only that area's calls, because dispatch was
   locked to planning areas (move-ups on under 2% of evenings), so the units answering an area's calls and the area's own units were the
   same population, and area-level percentiles reproduced every close-out's shortfall evenings.*
3. **No arithmetic symptom.** Station-area counts with their bounds reconcile to the area totals, the roster to the status log, and every
   rung's requirement follows from its counts.
4. **Not a row predicate.** The district requirement is a quantile of a sum taken evening by evening across areas, after the suppressed
   cells are bounded; no filter on calls or evenings yields it.
5. **The enumeration is arithmetic.** No column holds a district's evening count; it is built from the areas' bounded counts on matching
   evenings.
6. **No cutover date in any series the forecast reads.** District dispatch starts in June and steps nothing in the closed record.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The summer close-outs for 2023–2026: per planning area and block, calls, units on duty, shortfall evenings and unanswered-call
  minutes, with the unit status log behind them.
* **What it certifies.** The negative binomial at area level and the bounded counts: together they reproduce every closed summer's
  shortfall evenings in every area.
* **What it is blind to.** The district requirement (above); the closed record holds no summer of district dispatch.
* **Twin pair.** Two weekend evenings in summer 2025 each brought 17 calls into area 1's evening block against its 3 units, at the same
  temperature. Area 1's unanswered-call minutes were 31 and 66 (2.1× apart), because on the first area 2 had 5 calls and moved a unit up and
  on the second it had 14 and could not. Area 1's own count predicts them equal; only the North pair's joint evening reproduces both.
* **Resemblance points at the decoy.** By calls, temperature and calendar, next summer most resembles the 2025 summer, whose close-out
  area-level staffing reproduced evening by evening.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The deployment standard: on nine weekend evenings in ten the units that answer a call can answer every call in the
  20:00–24:00 block, at 1.2 unit-hours a call, rounded up to whole units. The deployment plan's three districts. The base roster: 3, 3, 5,
  2 and 2 units on duty in the block in areas 1 to 5. The surge pool of ten.
* **Empirical pins.** The areas' evening counts and their joint behaviour, from the bounded counts of the last three summers (78 weekend
  evenings).
* **Voices.** The deputy chief of operations: "District dispatch is about response times; it doesn't change how many units we need." The
  planning analyst: "Every area has to cover its own nine evenings in ten; that's the standard." The union representative: "Ten surge
  units is the floor; summer is always worse than the plan."
* **Licensed wrong basis.** The deployment plan records that the county EMS levy board funds surge units on the sum of area-level
  requirements and will review the request on that basis.

## 8. Determinism by construction

* **Bounds.** Every suppressed cell on an evening near any area's or district's 90th percentile is recovered exactly from the area total;
  the cells left as ranges fall on quiet evenings that sit below every percentile under either end of their range.
* **Percentiles.** Every 90th percentile sits clear of a unit boundary (1.2 hours ÷ 4 hours crosses a whole unit every 3⅓ calls): areas 18,
  15, 25, 9 and 8 calls; North 28 and Central 31 jointly; inverted-CDF and interpolated percentiles give the same units.
* **Window.** The last three summers' 78 weekend evenings; any two of the three summers give the same district units.
* **Districts.** Fixed by the deployment plan; area 5 is a district alone, so South's requirement is area 5's under either reading.
* **Release.** Units not needed by any district are released whole; no fractional surge arises.

## 9. Prompt sketch and deliverables

> The summer surge pool holds ten medic units for the weekend evenings, and the June deployment order is signed on 1 May. Our planning
> analyst says every area has to cover its own nine evenings in ten. Tell me how many surge units each battalion district gets and how
> many we release to the county, in one line for the order, and send `surge_plan.xlsx` with the build and the sheets below, a chart
> `district_evenings.png`, and a one-page `deployment_note.pdf`.

* `surge_plan.xlsx` — area and district evening counts with the bounded cells, the requirements under each construction, the turnout sheet
  (ask A) and the alarms sheet (ask B).
* `district_evenings.png` — for each district, the distribution of weekend-evening calls as a histogram with its 90th percentile marked,
  the sum of the areas' 90th percentiles marked beside it, the base and surge units drawn as call-capacity lines, and the units released
  labelled.
* `deployment_note.pdf` — the committed allocation, why district dispatch changes the count, and why the saving is smaller than an
  independent calculation shows.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five areas and each summer month last year, the engine companies' 90th-percentile
  turnout time. *Device:* an engine re-dispatched while returning from another call logs its turnout from the original dispatch in the
  apparatus table, with the re-dispatch in the status-change table, as the dispatch data guide documents; reading the apparatus table
  overstates turnout in three areas. Engines enter no part of the medic plan.
* **Ask B (device-carried).** For each area, last summer's commercial fire-alarm activations, split false and confirmed. *Device:* an alarm
  reset and re-activated within ten minutes is one incident with two activation records, linked in the alarm-event table, as the
  monitoring guide documents; counting activations overstates incidents in every area. Alarms enter no part of the medic plan.
* **Ask C (validity).** Surge units by district and units released under each of the four rung constructions.
* **Decoupling.** Clearing the district pooling changes no figure in asks A or B.

## 11. Rubric arithmetic

5 areas × 3 months (ask A) + 5 areas × 2 (ask B) + 4 constructions × 3 districts (ask C) + the three committed district allocations and
the units released + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Weekend-evening 90th percentiles (bounded counts): areas 18, 15, 25, 9, 8 calls (6, 5, 8, 3, 3 units); North 28 (9 units), Central 31
  (10), South 8 (3). Independent convolution: North 25 (8 units), Central 31 (10).
* Suppressed cells read as zero: negative binomial area percentiles 15, 13, 22, 6, 5; Poisson 12, 11, 18, 5, 4. Area totals exceed the
  zero-filled sums on 61% of evenings.
* Surge by rung: 3 / 5 / 10 / 7 units (North 2/3/5/3, Central 1/2/4/3, South 0/0/1/1); partials 6, 4 and 4.
* Variance runs two to four times the mean in every area; shared heat evenings raise the areas' joint percentile above independence.
* The twin evenings are identical in area 1's count, units and temperature; unanswered-call minutes 31 and 66.
* Re-dispatched engines and re-activated alarms touch no medic call, unit or bound in the plan.
