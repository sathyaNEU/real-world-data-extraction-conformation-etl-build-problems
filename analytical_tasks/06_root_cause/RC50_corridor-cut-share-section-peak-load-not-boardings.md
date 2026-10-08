# RC50 — How much of the bus corridor's decline the new rail line caused, when the riders it took still board the buses

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · bus network planning |
| Mirrors | Cannibalisation sizing when a new product takes an old product's longest sessions and leaves its short ones (a short-video feed taking long viewing sessions from a streaming app at YouTube and Netflix, an express checkout taking a store's large baskets at Amazon Fresh), so session or transaction counts barely move while the capacity the old product needs falls |
| Decision shape | One figure committed at a date (a component): the new line's share of the fall in peak load on the parallel sections, which the frequency review sets against its 30% bar for cutting them |
| Committed call | The new line caused 41% of the fall in peak load on the corridor's parallel sections, above the review's 30% bar |
| Gap · Pattern | Gap 2 (population) at the decisive rung, Gap 4 (rule) at rung 1 · Pattern D (two grains, boardings and section peak load, differing in shape because the riders the line took were the corridor's longest), standardised inside partially exposed routes; with the deciding comparison of measured #20 at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: the eight weeks before the opening in which the operator's ride-check surveys of on-board loads ran beside the automatic passenger counters on every corridor bus |
| Driving force | Boardings on the corridor's routes fell 9%. Against the network's other routes, with the strike periods set aside, the new line's share is 14%, under the review's 30% bar, and the parallel run shows peak section load at a fixed 0.61 of boardings on every corridor route. But the frequency standard sets a section's peak frequency by its peak load, and the riders the line took were the corridor's longest: commuters who boarded on the outer sections and rode the parallel section into the centre. They still board, now only as far as the interchange. Each kept a boarding and gave up a whole section of load. Against the same routes' other sections, the line caused 41% of the parallel sections' peak-load fall. |

## 1. Situation

A city opened a cross-town rail line beside a bus corridor of 12 routes. Each route runs a parallel section, between the first and last of
its stops within 500 m of a new station, and outer sections beyond it. Over the 13 four-week periods after the opening, boardings on the 12
routes were 9% lower than in the 13 before. The frequency review will cut peak frequencies on the parallel sections if the new line caused at
least 30% of their decline. The budget review wants the cuts. Planners say the whole market is smaller and that bus share has slid for a
decade.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the counters' boardings and on-board loads, the network's route boardings, the strike
  record, the ride checks and the frequency standard. The planners are right that most of the corridor's boarding loss is the market and
  the drift, and the budget review is right that the parallel sections emptied. No one's reading of their own figures is overturned. The
  question is at what grain the decline is measured.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the budget review, the planners and every voice. The comparison against the network's other routes still gives
  14%, and the parallel run still certifies boardings as a fixed proxy for load.
* **Instrument repair.** No file is suspect. The automatic counters on every bus record each stop's boardings, alightings and on-board load,
  balanced each trip, and the ride checks agree with them in the parallel run. The strike periods are real service losses in the operations
  log, not gaps. Boardings record boardings, a correct field for a different attribute from load. With nothing to repair, rung 0 still
  returns 100%, rung 1 20% and rung 2 14%. How much of a section's peak load the line took is a comparison no row records, so the decisive
  rung is still needed.
* **Lens swap.** The naive population is every boarding on the corridor routes, all day. The answer's is the riders on board along the
  parallel sections in the peak hour, a different population at a different moment.

## 3. The driving force

A strong solver does not book the whole 9% to the new line. It sets the corridor's routes against the network's other routes, which fell
7.2% with the smaller market and the long drift in bus share, and finds the extra loss on the corridor. It reads the operations log, sets
aside two after-window periods in which a strike at the corridor's garage cut 30% of service, and the line's share falls to 14%. The parallel
run confirms the grain: in the eight weeks before the opening, peak load on every parallel section was 0.61 of its route's boardings. But
the frequency standard sets a section's peak frequency by its peak-hour load, and the riders the line took were the corridor's longest. They
boarded on the outer sections and rode the whole parallel section into the centre. They still board the same buses, now only as far as the
interchange, so boardings hardly moved while peak load on the parallel sections fell 18%. The routes' own outer sections, exposed to the
same market, strike and drift but not to the line, fell 10.6%. The line caused 41% of the parallel sections' peak-load fall.

## 4. The ladder

| Rung | Construction | Lands on (the line's share of the decline) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Corridor routes' boardings, 13 periods after against 13 before, the whole fall booked to the line | 100% (+143%) | The budget review's comparison, on the published route figures | The network's route boardings: the other routes fell 7.2% over the same windows |
| 1 | The deciding comparison: the corridor routes' fall against the network's other routes, the extra fall booked to the line | 20% (−51%) | Market and drift removed by the comparison the planners asked for | The operations log: in two after-window periods a strike at the corridor's garage cut 30% of its service |
| 2 | Hygiene of the windows: the strike periods dropped from both windows, the comparison rerun | 14% (−65%) | Every confounder in the record removed, and the parallel run fixes peak load at 0.61 of boardings | The frequency standard: a section's peak frequency is set by its peak-hour load, and on the parallel sections peak load fell 18% while boardings fell 8.4% |
| 3 | **Decisive:** peak-hour load on each parallel section against the same route's outer sections, the extra fall booked to the line | **41%** | — | — |

* **Figure shape.** The corrections walk the share down from 100% to 14%, and the decisive move reverses them to 41%. Offsets from the answer
  are +59, −21 and −27 points.
* **Partial correction priced (L3).** Rung 2 sits 27 points from the answer. A solver who moves to peak section load but keeps the network's
  other routes as the comparison lands at 60%. One who measures load within routes but all day lands at 36%. One who splits boardings by
  section and compares within routes lands at 16%. Every half lands at least 12% from 41%.
* **Grid.** Grain (route boardings, section boardings, all-day section load, peak section load) × comparison (none, the network's other
  routes, the same routes' outer sections) gives 11 feasible cells. The nearest wrong cells are all-day load within routes at 36% (13% away)
  and all-day load against the network's other routes at 49% (18% away). Every other cell is at least 41% away.
* **The deciding comparison.** Parallel sections against the same routes' outer sections, 18% against 10.6%. The share rests on that
  difference, and the note has to state it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The frequency standard defines peak frequency by peak-hour load. The review's rule says "caused at least 30% of their
   decline". No document says the decline must be read in load, or that the line's riders still board.
2. **Corpus blind for a computable reason.** *In every parallel-run week the line was not yet open, so the corridor's trip lengths were the
   old ones and each section's peak load was a fixed 0.61 of its route's boardings.* The run certifies boardings as the grain on 12 of 12
   routes.
3. **No arithmetic symptom.** Boardings, alightings and loads balance on every trip, and route boardings sum to the published corridor
   figure.
4. **Not a row predicate.** The answer needs each trip's stop-by-stop load, aggregated over the parallel and outer sections in the peak hour,
   and the two sections' changes differenced within each route.
5. **The enumeration is arithmetic.** No field marks a rider as lost to the line. The share is a difference of section changes.
6. **No cutover date.** The opening is dated, but the comparison is between sections running through the same dates, so no step carries the
   answer.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The eight weeks before the opening in which the operator's ride-check surveyors counted on-board loads on every corridor route
  beside the automatic counters.
* **What it certifies.** The counters' loads match the ride checks within 2% on every section, and peak section load is 0.61 of route
  boardings on all 12 routes, within 0.01.
* **What it is blind to.** A change in trip length (property 2).
* **Twin pair.** Routes 25 and 86 are identical on boardings in both windows (−8.4% each), on their share of stops in the parallel section
  and on the parallel run's ratio. Route 25's riders were mostly commuters riding through the parallel section, and Route 86's short hops.
  Peak load on their parallel sections fell 30% and 15% (2.0×). Only section loads separate them.
* **Resemblance points at the decoy.** The corridor's boarding change most resembles the planning archive's 2016 tram corridor, where a
  boardings-based share of 15% held up at the next review.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The frequency standard: "A section's peak frequency is set so that its peak-hour load stays within 80% of the capacity
  offered." The review's rule: "Parallel sections are cut where the new line caused at least 30% of their decline." The network's stop list
  defines each route's parallel section by the 500 m rule.
* **Empirical pins.** The load-to-boarding ratio comes from the parallel run. The strike periods come from the operations log.
* **Voices.** Budget reviewer: "The line opened, journeys fell, and those buses are running empty." Lead planner: "The market is smaller and
  bus share has slid for a decade; the line is a sideshow." Garage manager: "It was the strike that hurt the corridor, not the trains."
  Passenger group: "People still ride our buses to the new stations every morning."
* **Licensed wrong basis.** The planning memo records that the budget review reads bus performance in boardings by route and will see the
  frequency review on that basis.

## 8. Determinism by construction

* **Peak hour.** The peak hour is 07:30 to 08:30 inbound. Any 60-minute window between 07:00 and 09:30 gives between 38% and 44%.
* **Sections.** Every route's parallel section runs between its first and last stops within 500 m of a station, from the stop list, and
  every route has outer sections on both sides.
* **Strike.** Within a route the strike cut both sections' service alike, so the decisive comparison returns 41% with the strike periods
  kept or dropped. Route-level comparisons drop the two periods from both windows.
* **Counters.** Trips whose loads do not balance to zero at the last stop are rebalanced by the operator's validation run, and any rule for
  them moves the share by under a point.
* **Maturity.** The final validation run for the last period closed before the extract.

## 9. Prompt sketch and deliverables

> The frequency review meets on the 9th and will cut the corridor's buses if the new line caused at least 30% of their decline. The budget
> review says the buses are running empty. I need the line's share, in whole percentages, in a sentence the review can minute, with the
> comparison it rests on. Send `corridor_share.xlsx`, a chart `section_loads.png`, and a one-page `review_note.pdf`.

* `corridor_share.xlsx` — the share on every construction, the reliability sheet (ask A), the concession sheet (ask B) and the parallel-run
  back-test (ask C).
* `section_loads.png` — peak load along each corridor route, stop by stop, before and after, with the parallel section shaded and the
  interchange marked, a bar pair for parallel and outer sections, and a title stating the share.
* `review_note.pdf` — the share, the comparison it rests on and why boardings understate it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 corridor routes, kilometres operated as a share of kilometres scheduled in the
  after window. *Device:* the schedule file records a curtailed trip as operated, with a curtailment code and the lost kilometres in a
  separate field, as its guide states. Counting trips operated overstates reliability by about 4 points on the curtailed routes. Kilometres
  never enter loads.
* **Ask B (device-carried).** For each of the 13 after-window periods, the concessionary journeys the operator is reimbursed for. *Device:*
  the concession scheme pays one journey for boardings linked within 60 minutes, and the ticket-machine log records each boarding.
  Summing boardings overstates reimbursable journeys by about 15%. The main call reads the counters, never the ticket-machine log.
* **Ask C (validity).** For each of the eight parallel-run weeks, the ride-checked peak load on the corridor beside the load your
  construction gives.
* **Decoupling.** Clearing the section-load construction changes no figure in asks A or B. Ask C holds no week after the opening, by
  property 2.

## 11. Rubric arithmetic

12 routes (ask A) + 13 periods (ask B) + 8 weeks (ask C) + the share, the parallel and outer sections' changes and the boarding comparison +
5 named chart parts + 3 files ≈ 46 criteria.

## 12. World-building constraints

* Corridor boardings fall 9.0% (8.4% with the strike periods dropped), and the network's other routes 7.2%.
* Peak load on the parallel sections falls 18.0% and on the same routes' outer sections 10.6%. All-day section loads fall 14% and 9%.
* The share is 100% / 20% / 14% / 41% by rung. Every grid cell other than the answer is at least 13% from 41%.
* The parallel run's ratio is 0.61 on every route. Routes 25 and 86 are identical on every boarding column, with parallel peak-load falls of
  30% and 15%.
* Curtailment fields and ticket-machine rows never touch the counters' boardings or loads.
