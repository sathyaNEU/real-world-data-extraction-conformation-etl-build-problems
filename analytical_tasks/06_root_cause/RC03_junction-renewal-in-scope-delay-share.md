# RC03 — How many delay minutes a period the junction signalling renewal will take off the operator's trains

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · rail operations performance |
| Mirrors | Remediation sizing after an incident cluster (a cloud region's failing network fabric, a fulfilment hub's sorter faults, a supplier's line stoppages), where the cause is named correctly and the fix covers only part of the failing component's footprint |
| Decision shape | One figure committed at a date (a component): the junction's renewal-removable delay, filed in the performance improvement plan |
| Committed call | Delay minutes per four-week period, on the operator's services, that the junction signalling renewal removes, as the plan states scheme benefits |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join), with E17 (validated on one population, applied to another) at rung 1 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another · #4 never tests its reading against the control |
| Calibration form | Revision log: the delay-attribution revision log, every incident's provisional and final codes for the ten closed periods |
| Driving force | Every junction incident carries one location code, so "the junction's signalling delay" looks like the renewal's whole benefit. What the renewal replaces is a list of assets inside the scheme boundary. 28% of the junction's signalling delay comes from approach track circuits beyond that boundary: the same asset type, filed under the same location, reachable only from the fault record's asset id through the scheme's asset list. |

## 1. Situation

A commuter operator's punctuality collapsed over the last three four-week periods. The infrastructure manager's signalling engineers say failures at
one busy junction caused it, and a funded renewal will replace the junction's interlocking and train detection next year. The operator must file the
renewal's benefit in its performance improvement plan by the end of the month: delay minutes a period that the scheme removes. Its own performance
team had ranked causes by primary minutes and blamed fleet faults; the reactionary minutes that the attribution guide links to each incident make
the junction the larger cause.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the delay records, the reactionary links, the provisional and final codes, the fault records and the
  scheme's asset list. The engineers are right that the junction's signalling caused the deterioration, and nothing they report is overturned.
  The graded figure is the component of that cause the renewal can reach.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the engineers' view, the performance team's ranking and the licensed basis. The delay file still files every
  junction incident under one location code, and the natural build still credits the renewal with all of it.
* **Instrument repair.** Make every attribution final and every fault record perfect. The junction's signalling delay is then known exactly
  (rung 2's 3,400 minutes) and is still not what the renewal removes, because 950 minutes a period come from track circuits beyond the boundary.
* **Lens swap.** The naive figure is the delay the junction location suffered; the answer is the delay from assets the scheme replaces: a
  different set of incidents, selected through a different entity.

## 3. The driving force

A strong solver follows the attribution guide, links reactionary delay to each incident and averages the 13 periods the plan uses. It notices
that the last three periods are still provisionally coded and converts them with the revision log, by sub-code once it sees the junction's
provisional mix is unlike the network's. That figure is the junction's true signalling delay. It is not the renewal's benefit. The scheme replaces
the interlocking and the train detection between two boundary signals, listed asset by asset in the scheme's asset schedule. The delay file
records every incident against the junction's single location code, whether the failed equipment sits inside the boundary or on the approaches
a mile out. Only the fault record carries the failed asset's id, and only the asset schedule says whether that id is being replaced. The
approach track circuits that fail most are the same asset type as the ones being renewed, so no reading of type, code or location separates
them.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | 13-period average of primary plus linked reactionary minutes for incidents coded signalling at the junction, codes as filed | 4,700 minutes (+92%) | It follows the attribution guide exactly and uses the plan's 13 periods | The revision log shows the last three periods' codes are provisional, and provisional codes revise |
| 1 | Provisional periods converted at the pooled closed-period retention rate (67.6% of provisional signalling minutes stay signalling) | 3,900 (+59%) | The pooled rate reproduces every closed period's final network total exactly | The revision log's sub-code table: intermittent faults retain 15% and confirmed failures 95%, and the junction's provisional minutes are 60% intermittent against the network's 34% |
| 2 | Provisional periods converted by sub-code | 3,400 (+39%) | Every closed period reproduces by sub-code, and the figure is the junction's signalling delay the engineers describe | The scheme's asset schedule: 28% of these minutes trace through fault records to track circuits outside the boundary |
| 3 | **Decisive:** only incidents whose fault record names an asset on the scheme's schedule, converted by sub-code | **2,450 minutes a period** | — | — |

* **Figure shape.** Every correction walks the figure down (−17%, −13%, −28% per step). The answer is the minimum cell, so every partial
  application overstates the benefit.
* **Partial correction priced (L3).** A solver who sees that the renewal does not remove everything but scopes by asset type (interlocking and
  track circuits in, everything else out) removes nothing, because every out-of-scope fault is a track circuit: it lands on rung 2's 3,400,
  +39%. The delay file carries no finer location than the junction code, so no location-based scope exists.
* **Grid.** Conversion (none, pooled, sub-code) × scope (location code, asset schedule) gives six cells: 4,700, 3,900, 3,400, 3,384, 2,808 and
  2,450. The nearest wrong cell is 2,808 (+14.7%), which needs the asset schedule applied with the pooled rate that the sub-code table
  refutes in 7 of 10 closed periods.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The scheme document describes the works and lists the assets replaced. No document relates the asset schedule to delay
   records, and the attribution guide files incidents by location.
2. **Corpus blind for a computable reason.** *In every closed revision the fault record's asset id is fixed when the fault is logged and is never
   revised, so the revision log can change who and why but is arithmetically incapable of saying which incidents fall inside a scheme boundary.*
3. **No arithmetic symptom.** Primary and reactionary minutes, incident counts and period totals reconcile under every rung; the in-scope and
   out-of-scope incidents share one location, one reason group and one asset type.
4. **Not a row predicate on the delay file.** It needs a hop from incident to fault record to asset id, membership in a schedule held in a
   different document, and the reactionary minutes carried through each primary incident.
5. **The enumeration is arithmetic.** No column carries "in scope"; the 950 out-of-scope minutes are built from three files.
6. **No cutover date.** The renewal has not happened; the deterioration is a cluster of faults, not a step at a date.
7. **Survives deletion.** With every voice removed, the location-code build still credits the renewal with 3,400 minutes.

## 6. The calibration corpus

* **Form.** The delay-attribution revision log: every incident in the ten closed periods with its provisional code, provisional sub-code,
  each revision and its final agreed code, plus the same fields for the three open periods (no finals yet).
* **What it certifies.** The reactionary linkage (every closed incident's final impact reproduces from its linked delay records) and the
  sub-code conversion (rung 2): sub-code retention reproduces all ten closed periods' junction finals within 1.5%, while the pooled rate
  misses seven of them by 9% or more and overstates their total by 14%.
* **What it is blind to.** Scheme scope (above).
* **Twin pair.** Closed periods P04 and P08 carried identical provisional junction signalling minutes (6,200), incident counts (14) and
  primary-to-reactionary splits. Their finals were 5,394 and 2,418 minutes (2.23×), because P08's provisional minutes were 70% intermittent
  and P04's 10%. No pooled rate reproduces both; sub-code retention reproduces both exactly.
* **Resemblance points at the decoy.** On the period summary the three open periods resemble P04, whose minutes nearly all stayed signalling.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The regulator's improvement-plan template: a scheme benefit is stated as the average per period, over the last 13 periods,
  of the delay the scheme removes on the operator's services, primary and reactionary. The scheme document's appendix lists the assets
  replaced, by asset id.
* **Empirical pins.** Sub-code retention rates from the closed revisions; each incident's failed asset from its fault record.
* **Voices.** The infrastructure manager's signalling lead: "Every one of those failures is on our junction, and the renewal fixes the
  junction." The operator's performance manager: "Our own trains' faults were the story until the junction started failing."
* **Licensed wrong basis.** The template records that the infrastructure manager reports scheme benefits as all delay attributed to the
  scheme's location and will present the renewal on that basis at the plan review.

## 8. Determinism by construction

* **Reactionary linkage.** Every reactionary record carries its primary incident number, so linkage is a key match with no convention.
* **Provisional periods.** Conversion is the sub-code retention from the closed revisions; each open incident is weighted by its sub-code's
  rate, and the asset id is already on its fault record.
* **Scope.** Membership is exact: every junction fault record carries one asset id, and every asset id is either on the schedule or not.
* **Window.** The template fixes 13 four-week periods on the operator's services; no convention on calendar months enters.
* **Rounding.** The figure is filed to the nearest ten minutes and sits mid-bin.

## 9. Prompt sketch and deliverables

> The regulator wants the junction renewal's benefit in our improvement plan by the 30th, and the infrastructure manager says the junction is
> why our last three periods fell apart. Give me the delay minutes a period the renewal will take off our trains, to the nearest ten minutes,
> as one line I can put in the plan. Send `junction_benefit.xlsx` and a chart `junction_delay_bridge.png`.

* `junction_benefit.xlsx` — the benefit build, the service sheet (ask A), the fleet sheet (ask B) and the closed-period back-test (ask C).
* `junction_delay_bridge.png` — a waterfall from the location-code figure to the committed figure, with bars for the revision conversion and
  the out-of-scope track circuits, the 13 periods' junction minutes as a sparkline inset, and the committed figure labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the operator's 9 routes and each of the last three periods, trains planned and trains
  run. *Device:* the schedule extract files a short-term overlay as a second row beside the permanent schedule it replaces, with an overlay
  indicator, as the timetable data guide documents; counting rows double-counts 6% of trains, all on four routes.
* **Ask B (device-carried).** For each of the four unit classes, miles run and technical incidents over the 13 periods. *Device:* coupled
  formations record their mileage once, under the lead unit, with the trailing units listed in a formation field, as the fleet data guide
  documents; summing by unit id credits all formation miles to lead units and misstates miles per incident for the two classes that run
  coupled.
* **Ask C (validity).** For each of the ten closed periods, the junction's final signalling minutes and what the pooled and sub-code
  conversions predict from its provisional codes; and the benefit under each of the four rung constructions.
* **Decoupling.** Clearing the asset-schedule join changes no figure in asks A or B.

## 11. Rubric arithmetic

9 routes × 3 periods × 2 counts (ask A) + 4 classes × 2 figures (ask B) + 10 periods × 3 figures + 4 constructions (ask C) + the committed
figure, the out-of-scope minutes and the in-scope share + 4 named chart parts + 2 files ≈ 105 criteria.

## 12. World-building constraints

* Ten closed periods average 2,900 final junction signalling minutes; the three open periods carry 10,700 provisional minutes each.
* Retention: intermittent 15%, confirmed 95%; network provisional mix 34% intermittent (pooled 67.6%), the junction's open periods 60%
  (47.35%). Rung figures 4,700 / 3,900 / 3,400 / 2,450.
* 72% of the junction's signalling minutes trace to scheduled assets in closed and open periods alike; every out-of-scope fault is an
  approach track circuit filed under the junction's location code.
* P04 and P08 are identical on every period-summary field, with intermittent shares of 10% and 70%.
* Overlay rows and coupled-formation mileage touch no junction incident, fault record or scheduled asset.
