# DS34 — Which route gets the year's stop-consolidation programme, when the trunk route's surviving stops cannot load its buses

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · bus network operations |
| Mirrors | Consolidating service points where the survivors have a throughput limit (merging delivery stations or parcel lockers, consolidating checkout lanes or warehouse docks, data-centre consolidation where the surviving cluster's I/O binds) |
| Decision shape | Which of N gets one scarce thing: the planning and works crew for one route's stop consolidation this year, among six routes |
| Committed call | The route consolidated, and the weekday rider-minutes its admissible plan saves, to the nearest ten |
| Gap · Pattern | Gap 3 (objective) into Gap 1 (time) · Pattern C behind a binding limit (E14: the surviving stops' peak loading capacity once riders consolidate onto them), with an implicit join (E20) at rung 2 |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #10 notes a binding limit as a risk · #18 joins only on the visible key · #20 leaves the deciding comparison unstated |
| Calibration form | Gold-standard verification subsample: 240 manually ride-checked trips across the six routes, with boardings, alightings and dwell by stop |
| Driving force | Removing stops on the trunk route saves the most rider-minutes on paper, because its buses are frequent and full. But each removed stop's riders board at a neighbour, and the neighbour's dwell grows. At 30 buses an hour, three of the trunk's surviving stops would pass the loading capacity the curb register gives them, and buses would queue. The plan the standards allow saves 45% of the paper figure; a moderate route's keeps 98%. |

## 1. Situation

A city transit agency can staff one stop-consolidation programme this year, and six routes (A–F) are in the running. The service standards
send it to the route whose admissible plan saves the most weekday rider-minutes, measured by the planning memo's method (through-riders
times time saved per avoided stop, weighted by the chance the bus would have stopped, less the walking added for the stop's own riders).
A plan is admissible only where every remaining stop stays within its loading capacity in the peak hour, as the city's curb guide defines
it. The draft went to the route with the most lightly used stops.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: automatic passenger counts, the GTFS schedule, the stop register, the curb register and the ride
  checks. No stakeholder read is overturned: the draft's route does have the most lightly used stops, and the trunk route's paper saving is
  the largest. The difficulty is that removing stops changes the stops that remain.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the draft, the scheduler's view and the council's basis. The memo's method on correctly joined counts still
  names the trunk route.
* **Instrument repair.** Ride-check every trip and measure every dwell exactly. Today's stops would be measured perfectly, and none of them
  is the merged stop the plan creates; its dwell exists only after the plan.
* **Lens swap.** The naive read and the answer differ in moment and population: today's stops and their riders, against the surviving
  stops carrying the removed stops' riders next year.

## 3. The driving force

A strong solver joins passenger counts to the schedule, builds through-loads by direction, applies the memo's method, and re-evaluates
neighbours after each removal. The trunk route C wins clearly: thirty buses an hour, full through the busy segment, every avoided stop worth
many rider-minutes. But the riders of a removed stop do not vanish. They board at the nearest remaining stop, and that stop's dwell per bus
grows by their boardings. The curb guide sets a stop's loading capacity from its loading areas and its dwell, and the curb register gives
each stop one area or two. On route C, three surviving stops with one loading area would see dwell rise from 19 to 31 seconds, which takes
their capacity from 34 buses an hour to 24, below the 30 the route runs. The standards allow only plans that keep every stop within
capacity, so route C's admissible plan removes five stops, not eleven, and saves 1,650 rider-minutes. Route E, at 12 buses an hour with
two-area stops on its dense segment, keeps 98% of its paper saving.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Stops under 50 weekday boardings per route, the draft's measure | A, a crosstown route (14 such stops against B's 10) | Lightly used stops are the obvious waste, and the draft says so | The planning memo: savings are measured in rider-minutes, through-riders against walkers |
| 1 | The memo's method on passenger counts joined to the schedule on the stop code they share | B, a radial route (2,950 against C's 2,400) | The agency's own method, carefully applied with neighbour re-evaluation | The stop register: 23 stops relocated last year carry new schedule IDs linked to the old counter codes through its "replaces" field, six of them twice |
| 2 | The same with counts joined through the relocation chain; greedy removal with the memo's spacing rule | C, the trunk route (3,700 against B's 3,020) | Every boarding is now placed, and the ride checks confirm the counts | The curb register and guide: with removed stops' riders boarding at their neighbours, three of C's surviving stops fall below 30 buses an hour of loading capacity |
| 3 | **Decisive:** each route's best plan that keeps every surviving stop within peak loading capacity, dwell rebuilt from the consolidated boardings | **E, a cross-river route, 2,450 rider-minutes** (5th of six on rung 0) | — | — |

* **Position table.** E is 5th on rung 0, 4th on rung 1 (1,850) and 3rd on rung 2 (2,500); it is never second and leads only rung 3.
  Rung margins: A over B 1.40×, B over C 1.23×, C over B 1.23×, E over B 1.20× (2,450 against B's 2,040 admissible).
* **Discriminator dominance.** C carries a 1.48× paper advantage over E into rung 3 (3,700 against 2,500). C's admissible plan keeps 0.45
  of its paper saving and E's 0.98, an edge of 2.2×, more than 1.2 × 1.48 = 1.78.
* **The deciding comparison (#20).** C's admissible 1,650 rider-minutes against E's 2,450 is what the board paper has to state; neither
  route's paper figure computes it.
* **Partial correction priced (L3).** A solver who checks loading capacity on today's dwell, not the consolidated dwell, finds every stop
  within capacity and names C. One who flags C's capacity as a risk and caps its saving by the share of peak buses that would queue names
  C at 2,900. One who rebuilds dwell from consolidated boardings but on the daily average rather than the peak hour finds one stop over
  capacity, not three, and names C at 2,720. Each partial reading stays on C.
* **Grid.** Join (visible key, relocation chain) × measure (low-boarding count, memo method) × capacity (none, today's dwell, consolidated
  dwell) = 12 cells. They name A, B or C except the one cell with the chain, the memo method and consolidated dwell.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standards say plans must keep stops within capacity, and the curb guide says how capacity is computed. No
   document says that a removal changes the dwell at the stop that absorbs its riders, or that the trunk route is where this bites.
2. **Corpus blind for a computable reason.** *In every ride-checked trip the bus served the stops as they stand, so no checked dwell ever
   carried a removed stop's riders, and the checks cannot show a merged stop's capacity.* They certify the counts, the relocation chain and
   the dwell per boarding.
3. **No arithmetic symptom.** Counts reconcile to the ride checks, through-loads close at each terminal, and every stop is within capacity
   today.
4. **Not a row predicate.** Capacity after the plan needs riders reassigned to the nearest surviving stop by direction, dwell rebuilt from
   peak boardings per bus, the curb guide's formula per stop, and the plan re-searched under the constraint.
5. **The enumeration is arithmetic.** Which stops would exceed capacity depends on the removal set; no column marks a stop as at risk.
6. **No cutover date.** The consolidation is a forward plan; no series in the pack steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice the memo's method still names C.

## 6. The calibration corpus

* **Form.** 240 ride-checked trips across the six routes, with checkers' boardings, alightings and dwell seconds by stop, recorded against
  schedule stop IDs.
* **What it certifies.** Counts joined through the relocation chain, at the counter correction factor of 1.04, reproduce the checks within
  2% at every checked stop-trip; the visible-key join misses all 23 relocated stops. Dwell is 5 seconds of door time plus 2.6 seconds per
  boarding and 1.4 per alighting, at every checked stop.
* **What it is blind to.** A merged stop (above).
* **Twin pair.** Two candidate removals, one on C and one on E, are identical on every count and schedule column: 210 weekday boardings,
  through-load 3,400, neighbours 190 and 240 metres away, the same walking penalty. Removed in its route's plan, the E stop saves 410
  rider-minutes and the C stop 205 (2.0×), because C's absorbing neighbour has one loading area and C runs 30 buses an hour. Only the curb
  register separates them.
* **Resemblance points at the decoy.** By frequency, load and spacing, route C most resembles the trunk route consolidated three years ago,
  whose rider-minute saving the agency still cites.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The service standards: the programme goes to the route whose admissible plan saves the most weekday rider-minutes by the
  planning memo's method, and a plan is admissible only where every remaining stop stays within its peak-hour loading capacity under the
  curb guide. The curb guide: capacity in buses an hour is 3,600 × loading areas × 0.275 ÷ (dwell seconds + 10), the 0.275 combining
  the signal's green share with the guide's queuing margin. The memo: a removed stop's riders board at the nearest remaining stop in their
  direction; the peak hour is the AM clock hour with the most scheduled buses.
* **Empirical pins.** Dwell per boarding and alighting, and the counter correction factor, from the ride checks.
* **Voices.** The scheduling manager: "Lightly used stops are pure waste." The planning lead: "Through-riders pay for every stop, and the
  trunk has the most of them." The streets liaison: "Curb space is ours to approve, not yours to plan around."
* **Licensed wrong basis.** The standards record that the riders' advisory council reviews consolidations on stop-level boardings and will
  see the draft list.

## 8. Determinism by construction

* **Capacity margins.** C's three offending stops fall 4 to 6 buses an hour below 30 after consolidation; on every other route each
  surviving stop keeps at least 3 buses an hour of headroom, so dwell constants within the checks' range move no verdict.
* **Plan search.** No route has more than 14 removable stops, so an exhaustive search over removal sets matches the greedy plan on every
  route, with and without the constraint.
* **Redistribution.** Nearest remaining stop by walking distance along the street network shipped with the stop register; no removed stop
  sits within 20 metres of equidistance.
* **Rounding.** E's 2,450 and B's 2,040 are mid-bin at the nearest ten.

## 9. Prompt sketch and deliverables

> We can staff one stop-consolidation programme this year, and six routes are in the running. The draft went to the route with the most
> lightly used stops. Tell me which route gets the programme and how many rider-minutes a weekday its plan saves, to the nearest ten, as the
> line for the service board. Send `consolidation_routes.xlsx`, a chart `route_savings_capacity.png`, and a one-page `board_paper.pdf`.

* `consolidation_routes.xlsx` — each route's plan under every rung basis (ask C), the fare sheet (ask A) and the punctuality sheet (ask B).
* `route_savings_capacity.png` — paper and admissible savings per route as paired bars, with route C's three surviving stops shown as a
  capacity panel (buses an hour against capacity before and after consolidation), the 30-bus line labelled and the chosen route marked.
* `board_paper.pdf` — the committed route and saving, and the comparison that decides it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six routes, last quarter's fare revenue per boarding and the share of boardings on
  passes. *Device:* pass boardings record no fare, and the fare guide apportions pass revenue to routes by the pass-use table. Counting only
  cash and card fares understates revenue per boarding on every pass-heavy route, most on A and D.
* **Ask B (device-carried).** For each of the six routes, last quarter's on-time performance at its timepoints and the share of early
  departures. *Device:* the standards measure punctuality on departure at every timepoint except the last, measured on arrival. Using
  arrival times throughout misclassifies held buses as late at three routes.
* **Ask C (validity).** Each route's weekday rider-minutes under each of the four rung bases, and the surviving stops each route's paper
  plan would push past capacity.
* **Decoupling.** Clearing the capacity check changes no figure in asks A or B. Fare apportionment and timepoint records touch no count,
  dwell or curb record.

## 11. Rubric arithmetic

6 routes × 2 (ask A) + 6 routes × 2 (ask B) + 6 routes × 4 bases + 6 counts of offending stops (ask C) + the committed route, its saving,
the runner-up and C's admissible saving + 5 named chart parts + 3 files ≈ 66 criteria.

## 12. World-building constraints

* Rung figures: low-boarding stops A 14, B 10; rung 1 B 2,950, C 2,400, A 2,100, E 1,850; rung 2 C 3,700, B 3,020, E 2,500; rung 3 E 2,450, B
  2,040, C 1,650.
* Route C runs 30 buses an hour in the peak; three of its one-area surviving stops go from 19 s to 31 s of dwell, from 34 to 24 buses an
  hour of capacity. Route E runs 12 an hour with two-area stops on its dense segment.
* 23 relocated stops, six moved twice, concentrated on C's busy segment. The twin removals match on every count and schedule column.
* Fare apportionment and timepoint records are independent of every main-call record.
