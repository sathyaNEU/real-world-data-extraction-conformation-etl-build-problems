# DS38 — Where five storm crews go before landfall, when a facility is exposed through the substation that feeds it

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · storm preparedness for coastal energy facilities |
| Mirrors | Pre-positioning scarce response capacity where a site is exposed through an upstream dependency (cloud regions exposed through their power or fibre feeds, fulfilment centres exposed through their carrier hubs, stores exposed through their distribution centre) |
| Decision shape | An allocation under a cap: five mobile crews among twelve facilities at the 72-hour advisory |
| Committed call | The five facilities that get a crew, and the expected loss the placement avoids, in $ millions to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B with a reproduction gate (E01), whose reproducing construction joins each facility to its feeding substation, with a subgroup calibration (E17) at rung 1 |
| Gate G mechanism | method_or_model_selection, with forecasting |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #13 validates on one population, applies to another |
| Calibration form | Change-log natural experiments: the storm log of six past storms, 52 facility-advisories, each with the exposure the risk team published at the time, the crews sent and whether the facility lost supply |
| Driving force | The storm plan uses an exposure method only if it reproduces every exposure the risk team published in the storm log. Scoring each facility's own point reproduces 44 of 52, every miss low. The eight misses are facilities whose feeding substation, in the network register, sits nearer the coast; only exposure at the facility or its substation reproduces all 52. It moves two inland facilities into the five. |

## 1. Situation

An energy company has twelve coastal facilities and five mobile storm crews, each of which halves the expected outage loss at a facility
it reaches before landfall. The storm plan sends the crews where expected avoided loss is greatest, an exposure probability times a filed
avoided-loss figure per facility, and allows an exposure method only if it reproduces every exposure published in the company's storm log.
The 72-hour advisory for a Gulf storm is out and the crews must move tonight. Operations has always sent crews to facilities inside the
forecast cone.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the advisories, the forecast-error archive, the verification report, the facility and network
  registers, the avoided-loss table and the storm log. No stakeholder read is overturned: the cone is drawn correctly, and the full error
  history is real. The difficulty is what a facility's exposure is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete operations' habit and the modeller's view. An exposure built on each facility's point from the error archive
  still ranks the coastal facilities first and still misses eight published exposures.
* **Instrument repair.** Give the company a perfect track forecast. The storm's path would be known, but whether a facility stays up would
  still depend on whether its substation is in the wind field, which no measurement at the facility shows.
* **Lens swap.** The naive read and the answer differ in population: the facility's own site, against the facility together with the
  substation it cannot run without, reached through a register no forecast product mentions.

## 3. The driving force

A strong solver drops the cone, takes the archive's forecast-error vectors at 72 hours, displaces the forecast track by each, and scores a
facility exposed when the displaced storm's 34-knot radius covers it during the window. It calibrates the errors to Gulf storms, whose
72-hour errors the verification report puts 30% below the all-basin figure, and ranks by exposure times avoided loss. Every step is
reasoned, and the storm log, which the plan makes the test, comes back 44 of 52. The eight misses all run low, so the misses also put the
log's total exposure out by 9.6%. Each missed facility draws its power from a substation the network register places nearer the coast than
the facility itself. A facility goes dark when either it or its substation is in the wind field, and only that union reproduces every
published exposure. For this storm, two inland facilities whose substations sit on the barrier coast join the five.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The operations rule: facilities inside the 72-hour cone, nearest the track first, each treated as exposed | F1, F2, F3, F4 and F5; $31.0M (+26.0%) | The established rule and the forecast graphic everyone trusts | The storm plan: crews go by exposure probability times avoided loss, by a method reproducing the storm log |
| 1 | Exposure from all 3,900 archive error vectors at 72 hours, facility point, maximum 34-knot radius | F2, F3, F1, F7 and F4; $21.4M (−13.0%) | A probabilistic model on the full error history | The verification report's published aggregates: Gulf storms' 72-hour errors run 30% below the all-basin figure |
| 2 | The same with the 1,240 Gulf error vectors | F2, F3, F1, F6 and F5; $18.9M (−23.2%) | Calibrated to the storm's own population; 44 of 52 published exposures reproduced | The storm log: the eight misses all run low, every one a facility whose feeding substation sits nearer the coast |
| 3 | **Decisive:** a facility is exposed when its point or its feeding substation (from the network register) falls within the radius; Gulf vectors | **F2, F9, F3, F11 and F1; $24.6M** | — | — |

* **Figure shape.** Rungs 1 and 2 walk the figure down from the cone's $31.0M; the decisive move reverses them. Every other cell sits at
  least 11.0% from $24.6M.
* **Position table.** F9 and F11, the facilities that enter at rung 3, rank 9th and 11th on rung 0's cone distance, 8th and 10th on rung 1
  and 7th and 9th on rung 2. F4, F5, F6 and F7, which each lead a slot at rungs 0 to 2, leave.
* **Discriminator dominance.** F6, rung 2's fifth, carries a 1.38× advantage over F9 into rung 3: the two carry the same avoided-loss
  figure, and F6's point exposure is 0.29 against F9's 0.21. F9's substation is exposed at 0.58, so its union exposure is 0.66 against
  F6's 0.29 (F6's substation is inland), a 2.28× edge against the required 1.2 × 1.38 = 1.66, past the 2.15 the edge needs with headroom.
* **Partial correction priced (L3).** Neither half names the answer's five. Adding substations to the all-basin vectors reproduces 47 of
  52 and files $27.3M (+11.0%) on F2, F9, F3, F1 and F7: the wider errors keep F7, 1.21× ahead of F11 ($3.4M against $2.8M). Scoring
  substations alone, without the facility point, reproduces 39 and files $20.2M (−17.9%) on F2, F9, F3, F11 and F8: F1, nearest the track
  but fed from a substation 60 km inland, falls out, and F8, fed from the barrier coast, leads it 1.63× ($3.1M against $1.9M).
* **Grid.** Error sample (all-basin, Gulf) × exposure unit (point, substation, union) = 6 cells beyond the cone; only Gulf and union
  reproduce 52 of 52, and every other cell names a different five.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan states the gate; the network register lists feeding substations for switching purposes. No document says
   a facility's exposure includes its substation.
2. **The log pins it, and the reproducing rule is a construction.** The union with Gulf vectors reproduces 52 of 52 published exposures to
   the percentage point; the best rival, point exposure with Gulf vectors, reproduces 44, missing low every time. The substation location
   is a property of a different entity reached through the register, so no setting of the error sample or the radius recovers it.
3. **No arithmetic symptom.** Error vectors, advisories and facilities reconcile, and every exposure is a valid probability under every
   construction.
4. **Not a row predicate.** Exposure is a share over 1,240 displaced tracks, each tested against two locations per facility within the
   window.
5. **The enumeration is arithmetic.** No column marks a facility as exposed through its substation.
6. **No cutover date.** The log spans six storms; nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the point-exposure model still reproduces 44 of 52 and reads
   as close enough.

## 6. The calibration corpus

* **Form.** The storm log: six past storms, 52 facility-advisories, each with the exposure the risk team published, the crews sent, and
  whether the facility lost supply.
* **What it pins.** The construction (above), and the Gulf error sample for Gulf storms.
* **Twin pair.** Two facility-advisories from different storms are identical on every column the log and the advisories show: 140 km from
  the forecast track on the right-hand side, 72-hour lead, the same intensity and 34-knot radius. Their published exposures are 0.18 and
  0.36 (2.0×). The second facility's substation sits 40 km nearer the track. Only the register join separates them.
* **Outcomes.** Nine of the 52 facility-advisories lost supply, four of them with their own site outside the wind field and their
  substation inside it.
* **Resemblance points at the decoy.** F1, nearest the track, most resembles the facility-advisories with the highest published exposures.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The storm plan: crews go where exposure times the filed avoided loss is greatest, one crew per facility; an exposure
  method may be used only if it reproduces every exposure in the storm log to the percentage point. The risk memo: errors are the
  archive's forecast-minus-best-track vectors at the advisory's lead time, each displacing the forecast once; the 34-knot radius is the
  advisory's maximum; the window runs to 24 hours after landfall. The avoided-loss table by facility.
* **Empirical pins.** The error subgroup and the exposure unit, from the storm log.
* **Voices.** The operations vice-president: "The cone is what everyone watches, and it has served us." The risk modeller: "Use the full
  error history; more data beats a subset." The grid liaison: "Substations are the utility's problem, not ours."
* **Licensed wrong basis.** The storm plan records that the board's risk committee receives the cone map with the facilities inside it
  marked.

## 8. Determinism by construction

* **No random draws.** Each archive vector displaces the track once, so exposures are exact shares and reproduce without a seed.
* **Subgroup.** "Gulf storm" is the verification report's own category, assigned in the archive; no storm sits on its boundary.
* **Distances.** No facility or substation lies within 2 km of the radius on any displaced track that would change its exposure by more
  than 0.001.
* **Placement.** Facilities are independent, so the top five by value is optimal; fifth and sixth differ by $0.7M.

## 9. Prompt sketch and deliverables

> The 72-hour advisory is out and our five mobile crews have to be moving tonight. Operations has always sent them to the facilities
> inside the cone. Tell me which five facilities get a crew and the expected loss they avoid, in $ millions to one decimal, as the
> instruction for the storm desk. Send `crew_allocation.csv`, a map `exposure_map.png`, and a short `storm_desk_instruction.md`.

* `crew_allocation.csv` — the twelve facilities' exposure and value under each rung's construction with the storm-log reproduction counts
  (ask C), plus the outage rows (ask A) and the fuel rows (ask B).
* `exposure_map.png` — facilities and their substations with lines between them, the cone, the 34-knot exposure contours from the Gulf
  vectors, each facility's union exposure labelled, and the five crew destinations marked.
* `storm_desk_instruction.md` — the five facilities and the avoided loss, and why two inside the cone get no crew.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve facilities, total outage hours in the last three storm seasons. *Device:*
  the outage system opens a new record each time a facility's status changes, and an outage that spans a restore attempt appears as two
  records linked by the incident number the outage guide documents. Summing records double-counts eleven outages and splits their
  durations.
* **Ask B (device-carried).** For each of the twelve facilities, backup-generator fuel on site at the last inspection, in hours of running
  time. *Device:* tank readings are in centimetres of depth, and each tank's strapping table converts depth to litres non-linearly.
  Treating depth as proportional to volume misstates every horizontal tank.
* **Ask C (validity).** For each of the four rung constructions, the storm-log reproduction count, and each facility's exposure under it.
* **Decoupling.** Clearing the substation union changes no figure in asks A or B. Outage records and tank readings touch no error vector,
  advisory or register record.

## 11. Rubric arithmetic

12 facilities (ask A) + 12 facilities (ask B) + 4 reproduction counts + 12 facilities × 4 constructions (ask C) + the five facilities, the
avoided loss and the margin at fifth place + 5 named chart parts + 3 files ≈ 92 criteria.

## 12. World-building constraints

* Rung sets and figures as in the ladder; partial cells $27.3M and $20.2M. Reproduction: 52 / 47 / 44 / 39 for union-Gulf, union-all,
  point-Gulf and substation-Gulf; point with all-basin vectors reproduces 31.
* F9's point exposure 0.21, substation 0.58, union 0.66; F6's point 0.29 with an inland substation and the same avoided-loss figure as
  F9. F1's substation lies 60 km inland; F8's on the barrier coast.
* The twin facility-advisories match on every log and advisory column.
* Outage records and tank strapping are independent of every main-call record.
