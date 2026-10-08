# DS05 — Which four rail routes to suspend, when a sleeper's crews also work the trunk expresses and none of their shifts would go

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · transport operating economics |
| Mirrors | Product-line and market exits where the shared-resource structure decides what a cut actually saves (Amazon fulfilment-node closures with pooled labour, airline route exits under crew pairings, cloud region consolidation with shared on-call rotations) |
| Decision shape | An allocation under a cap: four suspension slots across eight candidate routes for the next timetable year |
| Committed call | The four routes suspended, and the net annual saving they deliver, in $M to one decimal |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join: crew cost goes only with duties that run wholly on the suspended route), with the quiet second trap (#11) at rung 2 |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure · #4 never tests its reading against the control · #6 treats a mixed segment all one way |
| Calibration form | Settled-transaction ledger: the settled cost and revenue lines for the twelve months either side of five past service withdrawals |
| Driving force | Every route's avoidable costs are correctly stated, and the costing standard counts crew as fully avoidable. Crews are paid by duty, though, and a duty only disappears if every train in it does. The Lakeshore sleeper's drivers and attendants work duties that also cover trunk expresses, so suspending it removes no shift, and its $68M crew line stays. The serviceable share is a property of the crew roster, two joins from the route P&L, and the largest saving on paper is the least serviceable. |

## 1. Situation

A regional passenger-rail operator's franchise allows it to suspend at most four routes in a timetable year. The board wants the four that
save the most next year. Eight routes are candidates: three long-distance services (two of them sleepers), three regional lines and two
branches, one of which feeds the trunk. The finance team holds a route P&L, the costing standard's avoidability table, a ticket journey
file of every itinerary, the crew roster of duties and their trains, and the settled ledger of five past withdrawals. The CFO believes the
long-distance sleepers are where the money goes.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The P&L's allocated losses, the avoidability table,
  the allocated leg revenue, the journey file and the roster are all right for what they state. The difficulty is that what a suspension
  saves in crew depends on which duties vanish, and that is a fact about the roster, not the route.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CFO's belief. Avoidable cost less every fare a suspension loses still puts the Lakeshore sleeper first, and
  every figure reconciles to the ledger.
* **Instrument repair.** No file the ladder uses is suspect: the P&L's crew and revenue lines are correct allocations (crew by
  train-miles, revenue by leg) and the avoidability table is a costing convention, so none claims what a suspension releases or loses; the
  journey file, the roster and the ledger are complete. Even a P&L that booked every connecting fare to the route only moves rung 1 to
  rung 2's Lakeshore, Valley, Harbour and Moorland, rung 0 still leads with Sunrise and Lakeshore on allocated loss, and the duty construction
  is still needed for Pennine.
* **Lens swap.** The naive read prices each route's own cost lines. The answer prices the duties that would cease to exist: a different
  population (roster duties), reached through the trains they carry.

## 3. The driving force

A strong solver rejects the fully allocated P&L, takes avoidable costs from the standard's table and counts every connecting fare a
suspension loses. Each step is competent, and the ledger of past withdrawals confirms every category. The table counts crew as 100%
avoidable, which is true for every withdrawal in the ledger. Crews, though, are rostered in eight-hour duties, and a duty is paid whether
it carries three trains or four. Suspending a route saves a duty only if every train in it belongs to that route. Lakeshore's crews work
duties that also run trunk expresses (a serviceable share of 0), and so do most of the Sunrise and Mountain crews. Pennine's duties are 90%
self-contained, and the two branches' entirely. Joining trains to duties to routes moves $65M between Lakeshore and Pennine and changes
the four routes.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Fully allocated loss per route, largest four | Sunrise, Lakeshore, Mountain, Valley; $365.0M | The operator's own P&L, in the format the board reads | The avoidability table: overheads, shared stations and leased stock stay when a route goes |
| 1 | Avoidable cost less allocated leg revenue (the loud decoy beaten) | Lakeshore, Mountain, Valley, Kestrel; $152.0M | The textbook incremental correction | The journey file and the settled withdrawals: a suspension loses the whole fare of every connecting journey, $29M for Kestrel and $27M for Mountain |
| 2 | Connecting fares counted in full (#11, the quiet trap and its own control) | Lakeshore, Valley, Harbour, Moorland; $117.0M | Both P&L traps handled, and the ledger confirms every category to within 1% | The crew roster: none of Lakeshore's duties runs wholly on Lakeshore |
| 3 | **Decisive:** crew cost avoided only for duties every train of which is on the suspended route, from the trains-to-duties-to-routes join; the four re-chosen | **Valley, Harbour, Moorland, Pennine; $71.6M** | — | — |

* **Figure shape.** Every correction walks the claimed saving down, and the answer is the minimum of the eight toggle cells. Rung offsets:
  +410%, +112% and +63%.
* **Position.** Three of the four answer routes rank 6th, 7th and 8th on rung 0 (Harbour and Pennine tie at 45). No intermediate rung's
  four equals the answer. The fourth-to-fifth margins are 1.25, 1.22, 1.57 and 1.60.
* **Discriminator dominance.** Lakeshore carries a $21M rung-2 lead over Pennine (35 against 14). The decisive rung strips $68.0M of
  Lakeshore's crew line and $2.8M of Pennine's, a $65.2M swing, 3.1× the carried lead. Lakeshore ends at −$33.0M (suspending it loses
  money) and Pennine at +$11.2M.
* **Partial correction priced (L3).** Applying the duty rule while counting only the allocated leg of connecting fares names Harbour,
  Moorland, Pennine and Kestrel and claims $109.2M (+52%). The feeder enters because its duties are self-contained and its connecting
  fares are invisible. Applying the duty rule to rung 2's four without re-choosing keeps Lakeshore and delivers $27.4M (−62%).
* **Grid.** Cost basis (allocated, avoidable) × connecting fares (leg, full) × crew (per mile, per duty) gives 8 cells and seven distinct
  sets. Only the complete cell names the answer. The nearest wrong claim is $109.2M (+52%), and it costs one omission: the journey file.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The avoidability table says crew is 100% avoidable. No document says duties are paid whole, or that any route's
   duties are shared.
2. **No sweepable corpus nominates it.** *In every settled withdrawal the removed trains were worked by duties that ran wholly on the
   withdrawn service, because every past withdrawal was a branch-line frequency cut crewed from its own depot.* Crew cost fell in step with
   train-miles, so the per-mile and per-duty readings return the same five settlements.
3. **No arithmetic symptom.** Route costs sum to the P&L, fares tie to the journey file, and crew lines tie to payroll under every reading.
4. **Not a row predicate.** A duty's fate needs all its trains grouped and tested against the suspended set. A route's serviceable crew
   cost is then the sum over its duties that empty completely.
5. **The enumeration is arithmetic.** No column marks a duty as shared or a route's crew as unrecoverable. The serviceable share falls out
   of the join.
6. **No cutover date.** The roster is the standing winter roster, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The settled ledger: cost and revenue lines for the twelve months either side of five past withdrawals, with the network revenue
  ledger and the journey file's tickets for the same months.
* **What it certifies.** The avoidability table: every category moved by its table share (fuel, access, 80% of maintenance, 100% of crew),
  to within 1% in all five. Connecting fares: network revenue fell by the full fares of the connecting tickets in 5 of 5. The allocated-leg
  reading matches 0 of 5 and is 22% short on the total.
* **What it is blind to.** Shared duties (above).
* **Twin pair.** The Harbour evening withdrawal and the Kestrel Sunday withdrawal are identical on every ledger column a lookup sees: 0.21M
  train-miles, $3.1M allocated revenue, $5.4M avoidable cost, branch line, own depot. Their settled network revenue losses are $3.4M and
  $7.2M (2.1×). Only the journey file's connecting tickets separate them.
* **Every rule exercised.** One withdrawal ran on leased stock, so a lease line held flat. One served a shared station whose cost fell by the
  table's 50%.
* **Resemblance points at the decoy.** By route type, depot and size, Kestrel resembles the withdrawals that saved the most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The franchise agreement: at most four route suspensions in a timetable year. The board's brief: suspensions are chosen on
  the net annual saving they deliver. The costing standard: its avoidability table. One sentence each.
* **Empirical pins.** Full-fare connecting losses, from the settled ledger. Serviceable crew shares, from the roster.
* **Voices.** The CFO: "The long-distance sleepers are where the money goes." The planning director: "Crew is the most variable line we
  have." Kestrel's line manager: "Our feeder is the cheapest line on the network to run."
* **Licensed wrong basis.** The costing standard records that the ministry's review panel reads route cases on fully allocated loss and will
  see that basis.

## 8. Determinism by construction

* **Duty rule.** A duty disappears only if every train in it is suspended, and the roster gives each duty's trains, so no threshold
  exists. Duties are fixed eight-hour shifts, so a part-emptied duty costs the same.
* **Connecting fares.** No connecting journey has an alternative path that avoids a candidate route, so re-routing conventions return the
  same losses.
* **Leases and shared stations.** Fixed by the avoidability table, and identical under every rung above rung 0.
* **Rounding.** The answer's fourth route clears the fifth by 1.60×, so rounding of any line cannot change the four.

## 9. Prompt sketch and deliverables

> The franchise lets us suspend up to four routes next timetable year, and I have to tell the board which four and what they save us. Our
> CFO thinks the long-distance sleepers are where the money goes. Give me the four routes and the net annual saving in millions of dollars
> to one decimal. Send `suspension_case.xlsx`, a chart `saving_bridge.png`, and a one-page `board_brief.pdf`.

* `suspension_case.xlsx` — the eight routes' build, the punctuality sheet (ask A), the journeys sheet (ask B) and the basis sheet (ask C).
* `saving_bridge.png` — a bridge from the fully allocated claim to the committed saving, one bar per correction with its value labelled, and
  beneath it the eight routes' final values as a ranked strip with the four suspended routes marked.
* `board_brief.pdf` — the four routes, the saving, and why Lakeshore stays.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each route, last year's share of trains arriving within five minutes. *Device:* a train
  terminated short and completed by bus is logged with the bus's arrival time and a part-cancelled flag, and the performance standard counts
  it as cancelled. Counting it as an arrival lifts three routes by two to four points.
* **Ask B (device-carried).** For each route and quarter, passenger journeys from the gate system. *Device:* a passenger changing at the
  interchange passes two gates on one journey, marked by the interchange-transfer flag. Counting passes overstates the two routes that meet
  there by about 18%.
* **Ask C (validity).** Each route's net saving under the four rung bases, and the five settled withdrawals reproduced under the per-mile and
  per-duty crew readings.
* **Decoupling.** Clearing the roster join changes no figure in asks A or B. Performance records and gate passes never enter the savings.

## 11. Rubric arithmetic

8 routes (ask A) + 8 × 4 quarters (ask B) + 8 × 4 bases + 5 settlements (ask C) + the four routes, the saving and Lakeshore's swing + 6
named chart parts + 3 files ≈ 89 criteria.

## 12. World-building constraints

* Rung values ($M): Sunrise 115 / 25 / 5 / −38.2; Lakeshore 100 / 45 / 35 / −33.0; Mountain 90 / 33 / 6 / −16.4; Valley 60 / 38 / 35 / 13.4;
  Harbour 45 / 27 / 25 / 25.0; Moorland 38 / 23 / 22 / 22.0; Pennine 45 / 26 / 14 / 11.2; Kestrel 48 / 36 / 7 / 7.0.
* Crew lines and serviceable shares: Sunrise 48 at 0.10, Lakeshore 68 at 0, Mountain 32 at 0.30, Valley 36 at 0.40, Pennine 28 at 0.90,
  both branches and Kestrel at 1.0. Connecting fares: Kestrel 29, Mountain 27, Sunrise 20, Pennine 12.
* Every past withdrawal is a self-crewed branch cut. The twin withdrawals are identical on every ledger column.
* Performance flags and gate passes never touch costs, fares, duties or trains.
