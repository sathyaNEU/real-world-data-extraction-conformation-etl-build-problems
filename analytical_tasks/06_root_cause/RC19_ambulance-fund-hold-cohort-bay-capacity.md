# RC19 — Which scheme the ambulance winter fund buys, or none, when the handover queues it would clear are worst exactly when there is nowhere to put the patients

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · emergency services administration |
| Mirrors | Capacity funding where the measured bottleneck is real but the fix can only reach part of it (releasing on-call engineers blocked on a degraded dependency at cloud platforms, freeing delivery vans held at full docks in Amazon's network, adding chat agents when the queue is waiting on a back-office team) |
| Decision shape | Hold, forced by a blocking quantity: fund one winter scheme, or hold the money |
| Committed call | Hold the fund, with the blocking figure: the largest category 2 improvement any scheme can deliver this winter is 3.1 minutes (the H1 cohort area) against the fund's 4.0-minute floor |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join: cohort-area bays free in the hours crews wait), with E16 (finer controls separate constructions) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with binding_constraint |
| Measured traps engaged | #10 notes a binding limit as a risk · #12 stops at the first control that passes · #9 picks from the offered options when none passes |
| Calibration form | Existing-book actuals: the region's eleven past winter schemes, each with crew-hours released and the category 2 change that followed |
| Driving force | Crews held outside emergency departments are lost capacity, and a staffed cohort area takes patients off them only when it has a free bay. A cohort area's bays fill in the same evening hours the queues peak, because the emergency department it sits beside is fullest then. Free bays come from the department's hourly census, a different file from the handover data, and they cut the worst hospital's releasable hours to 31% of its excess. No scheme then reaches the floor. |

## 1. Situation

A regional ambulance service's mean category 2 response rose from 32 to 51 minutes this winter on 4% more incidents. The service's board wants more
crews; the acute trusts say crews are lost queueing at their doors. The region has one winter fund. It will buy additional crews (A), an expansion of
hear-and-treat triage (B), or a staffed cohort area for handovers at one of three hospitals, H1 (C), H2 (D) or H3 (E). The fund rule buys the scheme
that cuts the category 2 mean the most at this winter's demand, and only if the cut is at least four minutes; otherwise the money is held. The region
keeps the actual results of every past winter scheme.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: incidents and outcomes, handover times by hospital and hour, the emergency departments' hourly census,
  the scheme proposals and the book of past schemes. The trusts are right that crews are queueing, and the board is right that crews are short.
  Nothing is overturned; the fund's floor binds once each scheme's reach is computed.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the board's request, the trusts' view and the licensed basis. The handover data and the book's queueing conversion
  still commit the fund to the H2 cohort area.
* **Instrument repair.** None suspect: incidents and outcomes, handover times by hospital and hour, each department's hourly census, the
  proposals and the book are complete; the handover clock times every handover and the census counts every occupied bay each hour. Every rung
  reads complete files, so rung 0 still commits A (6.2 minutes), rung 1 C (9.4) and rung 2 D (6.6); none holds. What a cohort area can release
  is the smaller of crews waiting and bays free in each hour, a quantity built across two organisations' files that no record holds.
* **Lens swap.** The naive build counts crew-hours lost at each hospital; the answer counts the crew-hours a cohort area could take back in the
  hours they are lost, a different set of hours.

## 3. The driving force

A strong solver knows response time is a symptom of utilisation, so it does the Little's-law accounting: crew-hours consumed by jobs plus
crew-hours held at handover. Handover dominates, H1 has the largest excess, and converted at the region's average minutes per crew-hour it
clears the floor by a wide margin. It then checks the conversion against the book of past schemes. Every conversion reproduces the book's total
(the salient control), and only a queueing curve, in which an hour released at high utilisation is worth far more, reproduces the book's weekly
results. H2's queues sit in the evening peak, so on the curve H2's cohort area wins at 6.6 minutes, and the solver commits. A cohort area,
though, takes a patient off a crew only when it has a free bay. H2's department is full in exactly those evening hours, its cohort bays with it,
so only 31% of H2's evening excess is releasable; H1's is 60%. The share comes from the department's hourly census set against each scheme's
bays. Carried through the curve, no scheme reaches four minutes; the best is the H1 cohort area at 3.1.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Incidents against response time; minutes bought per crew-hour at the region's average | A, extra crews (6.2 min) | Demand rose 4% and response 60%, so capacity, priced the obvious way | The handover data: 38% of crew-hours this winter were spent waiting outside emergency departments |
| 1 | Little's-law crew-hours: job time plus handover excess by hospital, converted at the average | C, H1 cohort area (9.4 min) | Where capacity went, accounted exactly, with the worst hospital first | The book's weekly results: an average conversion matches the book's total but misses 8 of 11 schemes' weekly changes |
| 2 | Conversion on the queueing curve the book's weekly results reproduce, applied hour by hour | D, H2 cohort area (6.6 min) | Both the book's total and its finer weekly controls reproduce; H2's queues sit in the hours worth most | The departments' hourly census: H2's cohort bays would be full in the evening hours its queues occupy |
| 3 | **Decisive:** each cohort scheme's releasable hours, the smaller of crews waiting and bays free in each hour, then the curve | **Hold: best is C at 3.1 minutes** | — | — |

* **Why every candidate fails.** On the rung-3 basis: H1 3.1 minutes, crews 2.4, H2 2.0, H3 1.1, hear-and-treat 0.9. One standard, the
  fund's four-minute floor at this winter's demand, refuses all five.
* **Blocking quantity and its distance.** The best improvement, 3.1 minutes, is 0.9 short of the floor (23%). The decision would turn if H1's
  cohort area could take 77% of its excess instead of 60%, or H2's 61% of its evening excess instead of 31%.
* **Position table.** Rungs 0–2 commit to A, C and D, each above the floor, leading their runners-up by 4.13×, 1.34× and 1.27×.
* **Partial correction priced (L3).** A solver who caps releasable hours by each scheme's bay count over the whole day, rather than by the bays
  free in each hour, releases 74% of H2's excess and commits D at 4.9 minutes. One who applies the census but converts at the average rather than
  on the curve commits C at 5.6 minutes. Both commit; neither holds.
* **Grid.** Accounting (incidents, crew-hours) × conversion (average, curve) × reach (gross, daily bay cap, hourly free bays) gives eight
  feasible builds. Six commit to A, C or D. Two hold: the decisive build, on H1's 3.1 minutes, and the incidents-only build on the curve,
  which never values a handover scheme and holds on the crews' 2.4 minutes, a different blocking figure.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The scheme proposals give bay counts; the census is a department file. No document says a cohort area can only take a
   patient when a bay is free, or relates the census to handover queues.
2. **Corpus blind for a computable reason.** *Every past cohort scheme in the book ran at a hospital whose department was rebuilt with spare
   bays, so its cohort area never filled and its released hours equal its gross handover excess in every closed winter.* The book certifies the
   curve and cannot see the bay limit.
3. **No arithmetic symptom.** Crew-hours, incidents, handovers and response times reconcile under every rung; H2's queues and its census are
   both correct and agree.
4. **Not a row predicate.** Releasable hours are a minimum, hour by hour, of a quantity from the handover data and a quantity from another
   organisation's census, summed before conversion.
5. **The enumeration is arithmetic.** No column carries "releasable"; it is built per hospital-hour.
6. **No cutover date.** Queues and crowding run all winter; the dated event (the January flu peak) raises every scheme alike and is the decoy.
7. **Survives deletion.** With every voice gone, the curve still commits the fund to H2.

## 6. The calibration corpus

* **Form.** The book: eleven past winter schemes (crew additions, hear-and-treat expansions, cohort areas at four hospitals), each with the
  crew-hours it released by week and the category 2 mean by week before and during it.
* **What it certifies.** The queueing curve (rung 2). The salient control, the book's total change against total hours released, is matched
  by the average, Little's-law and curve conversions alike; only the curve matches the finer controls, the weekly changes, in all eleven schemes.
* **What it is blind to.** The bay limit (above).
* **Twin pair.** Schemes W-17 and W-22 released the same crew-hours (2,400) over the same eight weeks at the same hospital type. The category 2
  mean fell 5.8 and 2.7 minutes (2.15×): W-17's hours fell in weeks running above 90% utilisation, W-22's below 80%. Only the curve reproduces
  both.
* **Resemblance points at the decoy.** H2's proposal matches W-19, a cohort area that released its whole gross excess, on bays, queue length and
  evening share.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rule: the fund buys the scheme that reduces the region's category 2 mean response the most at this winter's demand,
  and only if the reduction is at least 4.0 minutes; otherwise it is held. The scheme proposals (crew-hours, bays, hours of operation).
* **Empirical pins.** The queueing curve, from the book; free bays by hour, from each department's census.
* **Voices.** The ambulance service's chief executive: "We can't reach patients; we need crews on the road." The trusts' chief operating
  officer: "H2's handover queues are the worst in the region; start there."
* **Licensed wrong basis.** The fund rule records that the regional performance team sizes handover schemes on gross crew-hours lost and will
  present that sizing.

## 8. Determinism by construction

* **Releasable hours.** In each hour, the smaller of crews waiting beyond 15 minutes and bays free in the proposed cohort area; the census and
  the handover data share hourly timestamps.
* **Curve.** One curve for the region, fitted on the book; every scheme's released hours are applied hour by hour at that hour's utilisation.
* **Demand.** This winter's incidents and outcomes, as the rule specifies; no forecast enters.
* **Crews.** The fund buys 9,800 crew-hours at the framework rate, spread over the rota's hours.
* **Rounding.** Minutes to one decimal; no scheme sits within 0.4 minutes of the floor.

## 9. Prompt sketch and deliverables

> Category 2 response has gone from 32 to 51 minutes and the region has one winter fund. Our board is sure the answer is more crews. Tell me
> which scheme the fund buys, or tell me we hold it, with the figure that decides it, in a sentence for the regional board. Send
> `winter_fund_case.xlsx`, a chart `releasable_hours.png` and a one-page `fund_decision.pdf`.

* `winter_fund_case.xlsx` — the five schemes under each construction, the call-answer sheet (ask A), the fleet sheet (ask B) and the book
  reproduction (ask C).
* `releasable_hours.png` — for each hospital, crews waiting and cohort bays free by hour of day as two lines with the releasable hours shaded
  between them, a side bar of each scheme's minutes against the 4.0-minute floor, and the blocking figure labelled.
* `fund_decision.pdf` — the hold, the blocking figure and what would change it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six dispatch areas and each winter week, the 90th-percentile time to answer 999 calls.
  *Device:* calls transferred from the non-emergency line carry both that line's answer time and the 999 connect time, and the standard
  measures from the 999 connect, as the call-data guide documents; using the first answer time overstates two areas.
* **Ask B (device-carried).** For each of the 28 stations, vehicle availability over the winter. *Device:* vehicles off the road for planned
  servicing carry a planned code that the availability measure excludes from the denominator, as the fleet guide documents; counting them as
  unavailable understates availability at the nine stations with workshop days.
* **Ask C (validity).** For each of the eleven past schemes, the actual weekly changes and those predicted by the average, Little's-law and
  curve conversions; and each scheme's minutes under each rung construction.
* **Decoupling.** Clearing the bay limit changes no figure in asks A or B.

## 11. Rubric arithmetic

6 areas × 13 weeks (ask A) + 28 stations (ask B) + 11 schemes × 4 figures + 5 schemes × 4 constructions (ask C) + the hold, the blocking figure
and the two turning points + 5 named chart parts + 3 files ≈ 185 criteria.

## 12. World-building constraints

* Minutes by rung (A / B / C / D / E): 6.2 / 1.5 / 1.1 / 0.9 / 0.6; 6.2 / 1.5 / 9.4 / 7.0 / 4.1; 2.4 / 0.9 / 5.2 / 6.6 / 2.6; 2.4 / 0.9 / 3.1 /
  2.0 / 1.1.
* Releasable shares of gross excess: H1 0.60, H2 0.31, H3 0.44; daily bay caps would give H2 0.74.
* 38% of crew-hours spent at handover; incidents +4%.
* W-17 and W-22 identical on hours released, weeks and hospital type.
* Transferred-call stamps and planned-servicing codes touch no handover, census or scheme row.
