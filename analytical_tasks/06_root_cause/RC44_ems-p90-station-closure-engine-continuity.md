# RC44 — Which fix the city funds for a 90-second rise in medical response times, when the closed station's engine is still working, two areas away

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · emergency response fleet deployment |
| Mirrors | Latency root causes at cloud platforms and delivery networks when a node is retired and its work continues from a successor node (a retired availability zone's traffic served from a neighbour, a closed fulfilment centre's orders shipped from the next one), so the retired node's degradation reads as the retirement while the successor's own growth is draining the capacity |
| Decision shape | Which of N root causes gets the fix: one investment this year, five aimed at five causes of the P90 rise |
| Committed call | Fund a peak-hour engine at Station 9: Area 9's call growth accounts for 36 of the 90 seconds, twice any other cause |
| Gap · Pattern | Gap 2 (population) at the decisive rung, Gap 3 (objective) at rung 1 · continuity across a closure (measured #23): Station 14's engine continues from Station 9, and its hours on Area 9's calls explain most of Area 14's loss, with the coarsened segment of measured #14 at rung 1 |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #23 reads a closure notice as a market exit · #14 coarsens the segment it was asked about · #12 stops at the first control that passes |
| Calibration form | Published control set with a reproduction clause: the department's published quarterly P90 for life-threatening medical calls by battalion, eight quarters (72 cells), which any admissible decomposition must reproduce |
| Driving force | Station 14 closed in March and its engine moved to Station 9. Area 14's P90 rose three minutes, and the department's area drill-down books that to the closure. But Engine 14 still reaches 80% of Area 14's calls first, from 1.4 miles further away, which costs 10 seconds of the citywide P90. The rest of Area 14's loss is the hours Engine 14 was not available to it. Housed at Station 9, it is second-due for Area 9, whose calls grew 40% with a new housing district, and it was on Area 9 calls for 24% of the hours Area 14 needed it. Followed across the relocation, Area 9's growth accounts for 36 of the 90 seconds. |

## 1. Situation

The city's 90th-percentile response time for life-threatening medical calls rose by 90 seconds year on year. The council can fund one
investment this year, each aimed at one cause: signal priority on the main corridors (traffic), more call-takers (call processing), a new
station alerting system (turnout), a peak-hour engine at Station 9 (Area 9's call growth), or an interim engine posted in Area 14 (the
closure of Station 14, which the department shut in March and whose engine now runs from Station 9). The memo funds the investment aimed at
the cause behind the largest part of the rise. The mayor's office says traffic.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the incident timestamps, the unit dispatch records, the run cards, the home-station mapping,
  the department's area tables and the published quarterly P90s. Area 14 really did lose three minutes, and Station 14 really did close. No
  one's reading of their own figures is overturned. The question is whose calls cost Area 14 its engine.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the mayor's view and every voice. The department's Shapley decomposition with the area drill-down still books
  34 seconds to the closure, and nothing in it points at Area 9.
* **Instrument repair.** Suspect: 3% of incident records have a missing or out-of-order timestamp. Repair: complete timestamps on every
  record. Rung 0 still names signal priority (70), rung 1 call-takers (40) and rung 2 the interim engine (34); none names Station 9's engine.
  The home-station mapping is not suspect: it places Engine 14 at Station 9, correctly, and the run cards record every first-due assignment.
  Area 9's growth reaches Area 14 only through Engine 14's busy hours, a unit history across the relocation that no row records, so the
  continuity construction is still needed.
* **Lens swap.** The naive grain is the area where a call came from. The answer follows a unit across its relocation and charges Area 14's
  missing engine to the calls that held it, a different population of seconds.

## 3. The driving force

A strong solver does not compare segment P90s, because percentiles do not add. It restricts to life-threatening calls, the class the
question names, rather than the department's monthly table of all medical calls. It builds the quantile-mapped counterfactuals and the
Shapley decomposition that reproduce every published quarterly cell, then drills into areas. Area 14 stands out with a three-minute rise
after Station 14 closed in March, and the closure looks like the obvious cause. But the closure did not take Area 14's engine away. Engine
14 runs from Station 9 and still reaches 80% of Area 14's calls first, 1.4 miles further away. Area 14 lost the other 20% because Engine 14
was busy, and the run cards make it second-due for Area 9, where a new housing district pushed calls up 40%. Ordered in time, Engine 14's
dispatch history shows it on Area 9 calls for 24% of the hours Area 14 needed it. Charged to the calls that held the engine, Area 9's growth
costs the city 36 seconds and the closure's distance only 10.

## 4. The ladder

| Rung | Construction | Names (seconds of the 90-second P90 rise) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Segment P90s for all medical calls from the department's monthly table, compared year on year | Signal priority (travel 70, 7.0× processing 10) | The department's own table and the mayor's reading | The dispatch protocol's determinant list: the question is life-threatening calls, 31% of medical calls |
| 1 | Segment P90s for life-threatening calls, compared year on year | Call-takers (processing 40, 1.33× travel 30) | The class the question names, from the protocol's own list | The published control set: segment P90 differences reproduce none of the eight quarterly totals |
| 2 | Quantile-mapped counterfactuals within area and Shapley over segments, which reproduce all 72 published cells, with travel drilled down by area of incident | Interim engine for Area 14 (34, 1.89× call-takers' 18) | Every published cell reproduced, and Area 14's jump dates to the closure | Engine 14's dispatch history: it still reaches 80% of Area 14's calls first, and for 24% of the hours Area 14 needed it, it was on an Area 9 call |
| 3 | **Decisive:** each unit followed across the relocation, and the seconds a first-due unit's absence cost charged to the area whose calls held it | **Peak-hour engine at Station 9 (36, 2.0× call-takers' 18)**, 4th on rung 0 | — | — |

* **Position table.** Station 9's engine ranks 4th on rungs 0 and 1 (at zero) and 5th on rung 2 (12), and leads only rung 3. Rung margins are
  7.0, 1.33, 1.89 and 2.0.
* **Discriminator dominance.** The interim engine carries a 22-second lead over Station 9's engine into rung 3 (34 against 12). Continuity
  moves 24 seconds from one to the other, a 48-second swing, 2.18× the carried lead. The floor is 1.2×, so the edge has 1.82× headroom.
* **Partial correction priced (L3).** A solver who sees Engine 14 still answering Area 14 but never asks where it was when it could not leaves
  Area 14's out-of-area seconds with the closure and names the interim engine at 34, 1.89× call-takers. One who traces Engine 14's busy
  hours but counts only the Area 9 calls where it went as the first unit, not as second-due cover, moves 9 seconds and names the interim
  engine at 25, 1.19× Station 9's engine. Neither half names Station 9.
* **Grid.** Call class (all medical, life-threatening) × decomposition (segment P90s, Shapley) × attribution (area of incident, unit within
  its first-due area, unit followed across the relocation) gives 12 cells. Only life-threatening calls under Shapley with units followed
  across the relocation name Station 9. Every other cell names signal priority, call-takers or the interim engine, the nearest being the
  first-due-only tracing at 1.19×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The run cards list first-due and second-due units by area. No document says Engine 14's Area 9 work costs Area 14,
   or links the closure to Area 9's growth.
2. **Corpus blind for a computable reason.** *Every published cell is a P90 by battalion of incident, and every attribution of the seconds
   reproduces it identically, because following a unit moves seconds between causes, not between battalions.* The
   control set certifies rung 2's machinery 72 of 72.
3. **No arithmetic symptom.** Timestamps, dispatch records, run cards and the published cells reconcile on every rung, and the 90 seconds are
   partitioned exactly on rungs 2 and 3.
4. **Not a row predicate.** The charge needs each unit's assignments ordered in time, the area each one came from, and the run card in force,
   joined to every incident whose first-due unit was absent.
5. **The enumeration is arithmetic.** No field says why a first-due unit was missing. The hours come from the dispatch history.
6. **No cutover date.** The closure is dated, but it is the decoy. Area 9's calls grew month by month with the housing district, and the
   charge follows that growth, not a step.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The department's published quarterly P90 for life-threatening medical calls, by battalion, for the last eight quarters
  (72 cells), and the memo's clause that any decomposition used for investment must reproduce them.
* **What it certifies.** Rung 2's machinery: first-arriving units, validated timestamps, the life-threatening class and quantile-mapped
  Shapley within area reproduce all 72 cells. Segment P90 differences reproduce none, and Shapley on all medical calls reproduces 9.
* **What it is blind to.** Which cause the seconds belong to (property 2).
* **Twin pair.** Engines 14 and 6 are identical on assignments, busy hours, segment times and the share of their own area's calls they
  reached first (80% each). Engine 14 spent its away hours on Area 9 calls and Engine 6 mostly on its own area's, so their areas went without
  them because of another area's calls for 610 and 300 hours (2.03×). Only the ordered dispatch histories separate them.
* **Resemblance points at the decoy.** Area 14's jump matches the department's planning standard for a closed station, a three-minute rise
  at P90 in the area it served.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The memo: "The council funds the one investment aimed at the cause behind the largest part of the P90 rise, and a
  decomposition is admissible only if it reproduces every published quarterly P90." The dispatch protocol lists the Echo and Delta
  determinants as life-threatening. The run cards list each area's first-due and second-due units by date.
* **Empirical pins.** The quantile-mapped Shapley comes from the published cells. Busy hours come from the dispatch records.
* **Voices.** Mayor's office: "It's traffic; every commuter in the city can tell you that." Station 14's captain: "Close a station and its
  area pays. That is what happened." Union steward: "Crews are slower out of the door since the new shift pattern." Battalion 3 chief: "My
  area's units are holding up fine."
* **Licensed wrong basis.** The memo records that the council's budget committee reads response times from the department's monthly table
  of all medical calls and will see the investment on that basis.

## 8. Determinism by construction

* **First-arriving unit.** Every incident's first on-scene time is unique, and no unit arrives within a second of another.
* **Busy hours.** A unit is busy from dispatch to available, both stamped on every assignment. No assignment overlaps another for the same
  unit.
* **Run cards.** One card per area is in force on every date, and Engine 14 is first-due for Area 14 and second-due for Area 9 throughout
  the year.
* **Quantile mapping.** Every area-segment cell holds at least 200 incidents in each year, so the mapping's interpolation rule cannot move a
  second.
* **Maturity.** Every incident in the year closed before the extract.

## 9. Prompt sketch and deliverables

> Our P90 for life-threatening medical calls is up 90 seconds and the council will fund one fix this year. The mayor's office is sure it is
> traffic. Tell me which fix we fund, in a sentence for the council, with the seconds of the rise you put on each of the five causes, to the
> nearest second. Send `p90_causes.xlsx`, a chart `p90_bridge.png`, and a one-page `council_note.pdf`.

* `p90_causes.xlsx` — the five causes on every construction, the handover sheet (ask A), the call-answering sheet (ask B) and the
  control-set back-test (ask C).
* `p90_bridge.png` — a bridge from last year's P90 to this year's with one bar per cause, an inset of Engine 14's hours by the area it was
  working in, and a title naming the funded fix.
* `council_note.pdf` — the named fix and why each other cause is smaller.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine battalions and each quarter, the share of hospital handovers completed within
  20 minutes. *Device:* the patient care record stamps "at destination" when the ambulance parks and "transfer of care" when the nurse signs,
  while the handover standard starts the clock at the hospital's own arrival stamp in the shared handover log. Using the parking stamp
  overstates handover times by two to four minutes at the two hospitals with long ambulance bays. Handovers never enter response times.
* **Ask B (device-carried).** For each quarter, the share of 911 calls answered within 15 seconds. *Device:* the phone system writes each
  transfer as a new leg under one call ID, and the answering standard times only the first leg. Counting legs as calls overstates fast
  answers by about a tenth.
* **Ask C (validity).** For each of the eight published quarters, the citywide P90 beside the one your construction gives.
* **Decoupling.** Clearing the continuity construction or the call-class restriction changes no figure in asks A or B.

## 11. Rubric arithmetic

9 battalions × 4 quarters (ask A) + 4 quarters (ask B) + 8 quarters (ask C) + the named fix, the five causes' seconds and the winning margin +
5 named chart parts + 3 files ≈ 63 criteria.

## 12. World-building constraints

* The rise is 90 seconds. On rung 3 it splits into call-takers 18, turnout 14, traffic 12, Area 9's growth 36 and the closure's distance 10.
  On rung 2 the closure carries 34 and Area 9's growth 12.
* Segment P90 differences are travel 70, processing 10 and turnout 10 for all medical calls, and 30, 40 and 20 for life-threatening calls.
* Engine 14 reaches 80% of Area 14's calls first and was on Area 9 calls for 24% of the hours Area 14 needed it. Area 9's calls grew 40%.
* Engines 14 and 6 are identical on every dispatch column except where their away hours were spent (610 and 300 hours).
* The 72 published cells are reproduced exactly by rung 2's machinery and by rung 3.
* Handover stamps and phone legs never touch incident timestamps or dispatch records.
