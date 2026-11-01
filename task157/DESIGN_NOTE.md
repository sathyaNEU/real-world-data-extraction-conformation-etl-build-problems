# task157 design note: Thornsby Bridge closure, the routes the Disruption Notice names (architecture 3)

Status lives in `pipeline.json`; this note holds the design. Read `## Pre-ship check

- 2026-11-01, stage 4 on the cut pack. Leak reader 1 (isolated, Sonnet, medium, `prompt.txt` and `target/` only):
  no decisive-step sentence, no ranking or helper file, no answer-like figure; question 5 quotes Schedule 7 7.6.1,
  whose literal execution is the golden's estimand (every route, every day of 11 January to 28 March 2027, on the
  registered timetable, below 80 per cent) with the method left open; question 6 analytical. Every REVIEW line
  harmless (`leak_check_report.md`, Solver's-eye read).
- The reader's realism notes, each reproduced before any repair: the AVL "uniform offset" did not reproduce (the
  steady gap is the UTC clock; lateness grows along each journey and peaks at 08:00 to 09:59 and 17:00 to 18:59);
  the control room remarks did (83 forms over 559 rows) and are now written in three controllers' hands by shift
  from a stream of their own (172 forms, the commonest 2 per cent); the distractors carry their registers' own
  fields; the plan's timetable sentence is now the bus liaison meeting's agreed outcome, the same fact. figures.json
  byte-identical through all of it.
- Leak reader 2 (fresh, after the plan's sentence changed): the same answers; question 6 analytical with one doubt,
  whether applying the plan's per-band minutes is rule application, ruled harmless (executed as filed they give the
  default path, route 41 alone; the call turns on the departures the minutes reach through the relieved drivers).
- Judge pass 1 (/tmp/determinism-check-task157-r1): DETERMINISTIC, FIX_NOW. The call, the nine autumn figures and
  the boardings total reproduced; Gate G forecasting, analytical_non_defect, no surface read; Gate H domain pass,
  layers pass, decisive step analytical. The thread measured the driver link in the record (arrival-to-departure
  lateness correlation 0.82 at route 27's 3-minute joins, 0.88 at route 58's 4-minute joins, about 0.1 at route
  33's 26 minutes or more). FIX_NOW on lost kilometres (routes 6, 27 and 41, Lot 2 3,075 against 3,174): the whole
  99 km sits in four duty pieces relieved after midnight (route 6 duty 312 piece 1 on 30 September and 2 December,
  route 27 duty 318 piece 2 on 3 September, route 41 duty 584 piece 3 on 21 November), which a reader taking the
  relief time on the booking day leaves empty. The golden stands (a piece cannot end before it starts; the
  rebuild from the log, the returns and the AVL is asserted exact); step 5 now names the handling. No figure moved.
- Judge pass 2 (/tmp/determinism-check-task157-r2, the FIX_NOW re-judged once): DETERMINISTIC, APPROVE. Every
  lost-kilometre, reliability and autumn figure reproduced, the boardings within the 0.6 per cent of sales the AVL
  lost; its own replay files 27 at 72.9, 41 at 65.1 and 58 at 72.0, every other route above (route 19 at 82.8, the
  thinnest margin, flat at 82 to 84 in the published finals). Gate G and Gate H as pass 1. Its optional note, the
  boardings ask's band basis and direction, closed by filing the WHAT in the asking sentence ("the direction the
  bus was travelling and the traffic management plan's time band each boarding fell in"); the golden already did
  both, so nothing moved. The prompt changed, so the reader ran a third time.
- Surface (`guard.py surface`, after the column renames): one promoted pair, task159, on the domain and objective
  pairing alone (urban-regional-science and forecasting, two numbers apart). Harmless: task159 forecasts a US subway
  commission's platform crowding train by train to staff conductor shifts; nothing in its driver, world, decision,
  deliverables or shell recurs here. The task308 column-set match is gone. Heart WARN only (nearest task469, 0.11).
- The 10/10 rules re-read against the built pack: the decisive step is the forecaster's choice of the population the
  closure's minutes reach (the departures route 41's relieved drivers take over a few minutes after their arrival),
  forced by the duty schedule and the autumn record and not by any sentence, an analytical choice; the mess (UTC
  clocks, re-sent AVL messages, two key schemes for lost work, ticket machines left on summer time, provisional and
  final published rows) stays Layer 1 and decides nothing on the main call.

## Tried and rejected` first. Architecture 1
(the January 2027 winter guarantee qualifier forecast) was spent on its second portal return when its graded bin
proved finer than its estimator; architecture 2 (an Arizona elections division's projection of a filed initiative
petition from the statutory sample) shipped 10-27 and came back from the portal with the call landed and a
determinism finding. One architecture per world, so architecture 3 is drawn afresh in another client domain, world,
dataset and prompt shell under the same objective and number. Every figure in the live sections below is measured
on the cut pack by the generator and asserted in `generator/checks.py` (81 assertions); `generator/verify.py`
rebuilds every graded figure from `target/` alone.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task157.json`, architecture v3, registered 2026-11-01 with
  architectures v1 and v2 in `lineage`, each with its fate. `guard.py check` on the registered card: WARN only, no
  BLOCK (repeat.gate_g and overuse.gate_g, the forecasting mechanism every forecasting build carries;
  repeat.decision and repeat.question_form against task273, answered below); `validate` clean on 306 cards.
  Personas from `guard.py names --geo "England" --seed 157`: Molly Hughes (the Combined Authority's head of bus
  network performance, author of the close-out note and the golden), Shaun Brown (Pellbridge Buses' operations
  director), Damien Ward (the council's bridges and structures manager, author of the traffic management plan),
  Elliott Sharp (the depot's scheduler, the duty schedule's author) and Yvonne Warner (the depot traffic office,
  the daily returns).
- **Pairing:** `urban-regional-science` / `forecasting`, objective **Forecasting & Predictive Modeling**, shape
  **10** (a scorecard: each route's forecast punctuality checked against the 80 per cent floor), decision type
  `designation_set` (the routes the Disruption Notice names), answer unit `set_of_items`.
- **Niche:** a combined authority that franchised its buses forecasting each route's departure punctuality during an
  emergency closure of the Thornsby Bridge, because its performance regime (Schedule 7, 7.6) lifts the punctuality
  deduction from every route the notice forecasts below the 80 per cent floor, and the notice has effect only if it
  is issued 21 days before the closure starts.
- **As-of and window:** Friday **11 December 2026**. The bridge's principal inspection on 2 November 2026 found
  bearing section loss; the council's traffic management plan (version 2, 27 November) closes the bridge from Monday
  **11 January to Sunday 28 March 2027**. Route 41 diverts over the Ring Road crossing. The notice is due by 21
  December. The AVL extract runs from Tuesday 1 September to Sunday 6 December 2026 under the winter timetable and
  duty schedule (both in force 31 August 2026 to 3 April 2027). The window the call is about has not opened, so the
  call faces forward.
- **Why Forecasting.** The call is each route's share of on-time departures over eleven weeks that have not yet run,
  predicted from the operating record of the timetable and duty schedule that will run them. It is not Descriptive
  (nothing in the window is observed) and not Anomaly Detection (no event in the record is being diagnosed).
- **Strategy:** gap `population` then `time`, generators **G7** (operating window: a departure inherits lateness
  only where the gap in the driver's duty is shorter than the delay) and **G4** (attribution at transition: the
  lateness belongs to the inbound route at the relief point), Gate G `forecasting`, strategy `causal_design`
  (interference between routes carried by shared crews), Layer 2 family `estimand_identification`, pattern
  `own:relief-point-lateness-carried-through-crew-duties`, calibration `prior_period_close_out` (the 2025 Marsh
  Lane close-out, read only for the diversion's realised running time), context artifact `operations_log` (the
  control room log), `stump_class: analytical`, no official decoy, no validated decoy, decisive rule not filed.
- **Data-native sentence.** A franchised bus network's punctuality record is kept route by route, while the people
  who drive it are scheduled duty by duty, and the depot at the Ravensholme end of route 41 crews its city routes by
  having drivers work a 41 into Merchant Row Interchange and step straight onto a route 27 or route 58 departure
  three or four minutes after the arrival; so a late route 41 arrival is recorded as a late departure on a different
  route, whose own path and timetable never changed.
- **The abstraction sentence**, the one a reviewer holding this build beside its nearest approved build would say
  about both: "a unit's start inherits another unit's late finish through a shared worker who passes from one to
  the other inside a short gap, so a delay imposed on the other unit reaches this one only where the gap is
  shorter than the delay." It is not writable against any approved build. task303 (the nearest in spirit) reads a
  shared upstream supply as simultaneity across sibling feeders; task162 rebuilds a device's benefit hour by hour
  from a third party's draw; task117 replays per-unit draw caps reached through a dated join; task141 and task175
  carry a rate across a covariate; task179 adds another agency's record. None links two units by a worker who
  passes between them.
- **Same-puzzle and library tests.** `guard.py check` clears `test.same_puzzle` and `test.same_driver` on
  (population, G7, designation_set) and (population, G7, forecasting). The library test: the stump sentence does
  not read "use X on Y"; there is no named correction for crew-carried lateness, and the field's named method (the
  route-level disruption assessment: the diverted route's added running time, the corridor's added traffic delay,
  every other route at its own record) is rung 0.
- **Shell, drawn with the world.** The question opens "What routes" (the card's form is `which`; the corpus quota
  for `which` is over 30 per cent, so the first sentence is worded as a `what` question, which `voice-check.py`
  counts under its cap); the second sentence opens "Build" (not "Put"), the rounding sentence opens "Round" (not
  "Give"), and the deliverable set is an xlsx with an svg chart (task273 shipped docx and xlsx; architecture 2
  shipped xlsx and png). The lineage shells (v1 how-much, v2 how-many with xlsx and png) are not kept.
- **Fiction.** England, an invented city region (Grainford), the Grainford City Region Combined Authority as the
  franchising authority, Pellbridge Buses as the Lot 2 franchise operator at Saltmeadow depot, the Thornsby Bridge
  between the city and Ravensholme. Forum `customer_or_counterparty` (the notice goes to the operator under the
  franchise agreement), forcing event `incident_or_complaint` (the inspection's defect and the emergency closure),
  org family `local_government`, role family `operations_director`.
- **Deliverables:** `closure_punctuality_forecast_2027.xlsx` (the notice's routes; each route's autumn punctuality
  and closure forecast against the floor; reliability; the unserved stops' boardings) and
  `closure_punctuality_by_route.svg` (each route's autumn 2026 punctuality and closure forecast against the 80 per
  cent line).
- **The pack (15 files, csv, xml, xlsx, pdf).** Spine `avl_timing_point_events.csv` (one AVL departure or arrival
  at a registered timing point, journey by timing point by operating day, stamped in UTC, 473,000 rows); the
  registered timetable as TransXChange XML; the depot's duty schedule workbook; the franchise agreement's Schedule 7;
  the council's traffic management plan; the 2025 Marsh Lane close-out; the authority's published monthly
  punctuality; the control room log; the depot's daily returns; the route 41 ticket machine extract (95,000 rows);
  the fleet register; the fare stage table; the cause codes; and the two distractors (the Ring Road crossing's
  traffic counts, the street works permits for the first quarter of 2027).
- **Sources, one line each.** `guard.py recent`, `coverage` and `mechanisms --objective forecasting` (92 builds)
  read before drawing; `guard.py slots` run on the mechanism nouns (relief, duty, driver, interchange, crew,
  roster, handover, lateness, interlining, layover, propagation) and on the setting nouns (bus, punctuality,
  diversion, roadworks, timing point, vehicle working, stand time): no slot note screens a delay carried between
  routes by crew reliefs. task469's note set aside delay propagation through aircraft rotations on the WHAT screen;
  task159, task254 and task269 are transit worlds with other drivers (a platform backlog, segment delays, excess
  wait on a common corridor). The nearest driver on file is 0.11 (task469).

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, with the field's own method
for a disruption's punctuality impact in it.

1. Convert the AVL events from UTC to local time across the 25 October clock change, drop the re-sent messages,
   match each event to its registered journey and timing point in the timetable export, and map registrations to
   fleet numbers.
2. Apply Schedule 7's on-time rule (a departure from a timing point between one minute early and five minutes
   fifty-nine seconds late, a journey's last timing point excluded, departures the AVL did not record left out) and
   compute each route's punctuality over the autumn record: every route sits between 82.8 and 88.4 per cent.
3. Back-test the persistence of that record on the authority's published monthly punctuality for 2025 and 2026:
   each route's autumn level reproduces its own previous autumn within about a point and a half, and the 2025 Marsh
   Lane close-out shows the plan's running time estimates within half a minute of the AVL.
4. Apply the traffic management plan: route 41's journeys run the diversion, the plan's 13 minutes in the weekday
   peaks and 10 at other times added at every timing point after Tenter Street (outbound) or Ravensholme Road
   (inbound), Thornsby Road and Thornsby Quay unserved; route 41 falls to 65.1 per cent.
5. Apply the plan's 2 minutes on the Ring Road crossing to routes 6 and 12 in the weekday peaks: they fall to 86.5
   and 85.9 and stay above the floor.
6. Check for knock-on effects through the vehicles: carry each late arrival into the same bus's next journey beyond
   its stand time. Route 41's buses cycle on route 41 all day, so no other route takes a bus off route 41; 41 falls
   to 46.9, routes 6 and 12 to 83.8 and 84.5, every other route keeps its autumn figure.

Ends on: **route 41 alone**, every other route above the floor (route 27 at 84.0 per cent, route 58 at 85.4, route
33 at 84.3), so the notice names route 41 only.

Golden: **routes 27, 41 and 58.** The duty schedule has route 41's inbound drivers take over route 27 departures at
Merchant Row three minutes after their scheduled arrival and route 58 departures four minutes after it, so during
the closure those departures inherit the diversion's minutes, and the buses carry them into their next journeys:
route 27 falls to 57.3 per cent and route 58 to 57.3; route 33's relieving drivers take a personal needs break first,
their departures leaving 26 minutes or more after the 41 arrival, which absorbs the delay, and route 33 stays at 83.2. The exact figures are measured on
the cut pack and asserted in `generator/checks.py`.

## Stump sentence

A competent solver who converts the AVL to local time, matches every departure to its registered timing point,
applies Schedule 7's window, backs the autumn record against the published monthly series and adds the traffic
management plan's diversion minutes to route 41 and its corridor minutes to the Ring Road routes, carrying late
buses into their next journeys, names **route 41 alone** for relief; the step that lands them there is treating
every other route's departures as independent of route 41, when the duty schedule hands route 41's inbound drivers
onto route 27 and route 58 departures at Merchant Row Interchange within a few minutes, so those departures inherit
the diversion and both routes fall below the 80 per cent floor.

## Three rules

- Task type: urban and regional science, transport forecasting (`urban-regional-science` / `forecasting`): each
  route's punctuality forecast over a window not yet run, from the operating record of the timetable and the duty
  schedule that will run it; it serves Forecasting & Predictive Modeling in the taxonomy.
- Domain test: the deciding quantity is each route's forecast timing-point punctuality under the closure, the
  share of AVL-recorded departures inside the one-minute-early to 5:59-late window, built the way bus operations
  planning builds a disruption assessment: the diverted route's added running time from the journey time model,
  the corridor's added delay, replayed on the recorded operation.
- Swap: "which wards will the ward closure take below the four-hour target" in hospital nouns keeps the words and
  loses the call: a hospital has no timetable of timing points with stand times, no running board that carries a
  late vehicle into its next trip, and no duty that hands a driver from one route's arrival to another route's
  departure three minutes later; the quantity is the AVL departure distribution under a timetable, and it does not
  survive the swap.
- Layer 1: the AVL archive stamps in UTC across the 25 October clock change against a timetable in local time (the
  AVL system); it identifies vehicles by registration without the space the fleet register prints (the AVL feed);
  it repeats about 1,200 messages and drops about 1 per cent, loses 26 vehicle-days part way when a unit stops
  reporting and every event in a GPS outage on 17 November (the feed); journeys turned short end with an arrival
  at the stop where they turned (the AVL system); the duty schedule keys pieces by running board and time in the
  operator's own stop codes and prints after-midnight times on the clock (the scheduling system); the published
  series carries October twice, provisional and final (the authority's release cycle). Nothing is placed to be
  caught.
- Layer 2: estimand identification under interference between units: the population of departures the closure
  touches is not route 41's alone; it includes every departure a route 41 driver works next inside a gap shorter
  than the delay, which only the duty schedule joined to the AVL reveals.
- Decisive step: recognising that the routes are not independent units, because the depot's duties pass route 41's
  drivers straight onto routes 27 and 58 at the interchange, and replaying the closure's added minutes through the
  duty schedule's running changeovers (the driver is ready when his 41 arrives, three or four minutes before the
  departure he takes over) as well as through the buses.
- Not semantics: every field, code, unit and definition read correctly (the clock converted, the window applied,
  the plan's minutes added, the unserved stops dropped, the duty schedule's times and stop codes decoded) still
  leaves the easy route on route 41 alone, because no field or code says that a route 27 departure depends on a
  route 41 arrival; the dependence is a relation between consecutive rows of a duty and two journeys' times.
- Not rule application: no filed rule or procedure performs the step (Schedule 7 files the estimand, the plan files
  the closure's minutes, neither says anything about drivers or other routes), so executing every stated rule files
  route 41 alone; the enumerated family (route-level, vehicle carry only, driver carry with walking time 0 to 4 and
  turnaround 0 to 2 minutes, drivers without buses, every join, seasonal shift, the closure's day mix) spans route
  27 from 44.5 to 84.0 and route 58 from 44.6 to 85.4; the standing family (every member that passes the minutes
  through the drivers) spans 44.5 to 78.3 and 44.6 to 78.0, always below the floor, with route 33 at 81.6 to 84.3
  and every other route above 82, so the data leave one set standing, ruled by the record (the AVL shows the relieved
  departures leaving late when 41 arrives late, slope 0.96 over 1,824 reliefs).
- Analyst test: a strong analyst who cleans the AVL, applies Schedule 7, the plan's minutes and the corridor delay,
  and carries late buses into their next journeys, files **route 41 alone** (the default path's `Ends on:`).
- Estimand: Schedule 7, 7.6.1 (`franchise_lot2_schedule7_performance_regime.pdf`): "for each Route, the
  Authority's forecast of that Route's Punctuality over the whole Disruption, every day of it, on the Registered
  Timetable for those days", Punctuality defined in 7.2.1, the floor in 7.3.1, a Route below the floor named under
  7.6.2; the Disruption's dates in the traffic management plan.
- No decoy: nothing is planted to be caught: no copied block of AVL records, no hidden rule, no memo, draft,
  briefing or stakeholder figure carries the wrong answer; the traffic management plan names route 41 as the bus
  service that crosses the bridge, which is true, and says nothing about any other route.
- No certified replay: the method is not hidden and recovered by reproducing certified figures; the published
  monthly series and the 2025 close-out confirm the autumn record and the plan's minutes, and no shipped figure is
  a forecast for the closure to be reproduced.
- Lesson: a model that gets it right learns that a disruption's reach in a crewed network runs through the people
  as well as the vehicles: units joined by a shared worker inside a short gap are one population for a delay
  imposed on either. No build on file teaches interference through a shared worker's schedule.

## Survivor anatomy

- Actor: the deciding property, that a route 27 or route 58 departure is taken over by a driver stepping off a route
  41 arrival three or four minutes earlier, has no column in any file: it is a relation between consecutive rows of
  a duty in the duty schedule (piece n on a 41 board ending at stand D, piece n+1 on a 27 or 58 board starting at
  stand B or C) and the two journeys those pieces' times pick out of the timetable.
- Link: the signal is read through a link no key offers: a duty piece names a running board, a time and an operator
  stop code; the timetable keys journeys by journey code and block number; the AVL by journey and registration.
  Joining a duty's consecutive pieces to the two journeys and comparing the gap with the closure's delay is a
  cross-file comparison the route-level disruption assessment never asks for, and no sentence invites it.
- Reflex: the field's named method (the route-level disruption assessment, the diverted route's added running time
  and the corridor's delay on the routes that use it, every other route at its own record) sits at rung 0 and files
  route 41 alone; the vehicle-working check at rung 1 does too, because route 41's buses never leave route 41.
- Back-test: the textbook route validates: each route's autumn level reproduces its previous autumn in the published
  series within about a point and a half, and the 2025 close-out shows the plan's minutes within half a minute of
  the AVL and the 2025 notice's single route correct; that closure was outbound only at the outer end, so route 14's
  buses reached the city on time, which no shipped file says.
- Second use: every file the decisive step reads has its own use: the AVL builds every route's punctuality, the
  timetable every journey and stand time, the duty schedule the second ask's expansion of the depot's uncovered
  work into journeys and kilometres, the plan the closure's minutes; delete the decisive step and every file stays.
- Shock: the step's movement reads as ordinary: routes 27 and 58 sit 2nd and 6th of nine in the autumn ranking
  (19, 27, 33, 41, 14, 58, 22, 12, 6), the named set is not an interval of it or of any shipped statistic, and their
  late relieved departures on the days route 41 ran late are unremarkable among their own variation.
- Pins: Schedule 7 files the WHAT (7.6.1 the estimand over every day, 7.2.1 the on-time rule, 7.3.1 the floor,
  7.6.2 the named routes), the plan files the closure's dates and minutes and that route 41 keeps its timetable,
  and the duty schedule's own header files that it stays in force to 3 April 2027; no filed sentence names drivers,
  reliefs, knock-on, other routes or a method.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Survives deletion | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 route-level assessment (41 diverted, 6 and 12 on the crossing) | the plan's minutes | no | yes, the field's method | no | no | yes | yes | readable |
| R0b R0 with the published winter shift | no | the published series | yes, seasonality | no | no | yes | yes | readable |
| R1 late buses carried into their next journeys | no | the AVL's registrations | yes, vehicle working check | no | no | no | yes | readable |
| R2 every route a 41 driver works next inherits the full delay (over-corrected) | no | no | half a reflex once the duty schedule is open | no | no | yes | yes | readable |
| Drivers relieved off route 41 inside a gap shorter than the delay (decisive) | no: Schedule 7 and the plan say nothing of drivers or other routes | no: no column links a piece to the piece before it or a departure to an arrival on another route | no: the route-level, vehicle and seasonal reflexes all file route 41 alone | no: no control ties only under the golden | no: nothing in the battery joins a duty's consecutive pieces to two journeys | no: a replay through two networks of joins, not one subtraction | yes: nothing is wrong, nothing to delete | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a departure | every timing point of a journey but its last | the last (an arrival) counted too | 6, 12, 19, 27, 33, 41 and 58 | 7.1: "other than the last Timing Point of the journey, which is an arrival" |
| SF2 | on time | -60 to +359 seconds | -59 to +359; -60 to +360; -61 to +358 | same call (asserted); the autumn figures of some routes move at one decimal | 7.2.1 "no more than one minute before, and no more than five minutes fifty-nine seconds after"; 7.2.2 "to the second" |
| SF3 | a departure the AVL does not record | left out of both numbers | counted as not on time | same call (asserted) | 7.2.1: "left out of both numbers" |
| SF4 | the clock | local time | UTC as recorded | punctuality under 60 per cent everywhere before 25 October (asserted) | 7.2.2: "in local time" |
| SF5 | a re-sent AVL message | one departure | counted twice | same call; no route crosses the floor (asserted) | 7.1 counts Departures, not messages |
| SF6 | the autumn window | 1 September to 6 December 2026 | September to November (the published months) | same call (asserted) | the prompt's dates |
| SF7 | the forecast's days | every day of the closure | weekdays only | same call (asserted) | 7.6.1: "every day of it" |
| SF8 | the closure's day mix | the record's days weighted to the closure's (54 weekdays, 11 Saturdays, 12 Sunday-timetable days with Good Friday) | the autumn's own mix | same call (asserted) | converges |
| SF9 | below the floor | strictly below 80.0 | at or below | same call: no licensed forecast within 1.58 of 80 (asserted) | 7.6.2 "below the Punctuality Floor"; converges |
| SF10 | the diversion's minutes | the plan's 13 and 10 | scaled to the 2025 close-out's realised ratio, or 10 per cent lower | same call (asserted) | converges |
| SF11 | a journey's diversion band | by its scheduled time where it leaves its line | by its first departure | same call (asserted) | converges |
| SF12 | the unserved timing points | no departures there, so none counted | counted as not on time | same call (asserted) | 7.2.1 and converges |
| SF13 | the Ring Road delay | 2 minutes on the crossing in the weekday peaks for 6 and 12 | none; banded by the first departure; applied at all times | same call for the first two (asserted); 6, 12, 27, 41 and 58 at all times | the plan: "in the weekday peaks ... No change is expected there at other times" |
| SF14 | the timetable during the closure | the registered winter timetable | route 41 retimed | not computable from the pack | the plan: "service 41 runs to its registered timetable on the diversion"; the TXC period ends 3 April 2027 |
| SF15 | the duty schedule during the closure | the winter schedule | re-cut for the closure | not computable from the pack | the schedule's header: "In force 31 August 2026 to 3 April 2027" |
| SF16 | seasonality | the autumn record as recorded | the published winter shift added | same call (asserted) | converges |
| SF17 | the time a relieving driver needs, and a bus's turnaround | ready on the arrival; one minute | walking 1 to 4 minutes; turnaround 0 or 2 | same call for every combination (asserted) | converges |
| SF18 | a late bus's next journey | leaves late beyond its recorded stand time | the bus recovers fully at every stand (drivers alone) | same call: 27 at 78.3, 58 at 78.0 (asserted) | the record: every bus 7 or more minutes late at a stand of 6 minutes or less left its next journey 2 or more minutes late |
| SF19 | joins of 30 minutes or more | pass nothing (a meal relief or a split) | every join passes the lateness on | same call (asserted) | converges |
| SF20 | the operating day | the file's operating_day | the UTC date | same call: the 417 events stamped on another UTC date all lie within the hour either side of midnight | the AVL's own column |
| SF21 | the rounding path | punctuality from whole-second counts, rounded once to one decimal | none open | same call | 7.2.2 |

## Ladder

| Rung | Reading | Routes named | Route 27 / 58 / 33 / 41 | Killed by |
|---|---|---|---|---|
| R0 | route-level assessment: 41 diverted, 6 and 12 on the crossing, every other route at its record | 41 | 84.0 / 85.4 / 84.3 / 65.1 | the duty schedule's running changeovers off route 41 |
| R0b | R0 with the published winter shift | 41 | 84.6 / 85.9 / 84.8 / 64.8 | the same |
| R1 | R0 with late buses carried into their next journeys (the vehicle check) | 41 | 84.0 / 85.4 / 84.3 / 46.9 | route 41's buses never leave route 41; the drivers do |
| R2 | every piece a 41 driver works next inherits the full delay, whatever the gap | 27, 33, 41, 58 | 51.3 / 49.1 / 69.2 / 41.8 | route 33's relieved departures leave 26 minutes or more after the 41 arrival, so a 13 to 20 minute delay is absorbed |
| Answer | the closure's minutes passed on by buses and by drivers relieved inside a gap shorter than the delay | **27, 41, 58** | **57.3 / 57.3 / 83.2 / 46.9** | |

- **Convergent routes (C1):** every member that passes the minutes through the drivers names 27, 41 and 58: walking
  time 1, 2 or 4 minutes (27 at 54.9, 53.5, 52.7), turnaround 0 or 2 minutes (65.7, 49.0), both moved (44.5),
  drivers without buses (78.3 and 78.0), every join (57.2), the plan's minutes scaled (54.6, 62.2), the closure's
  day mix (57.4), weekdays only (54.1), after the clock change only (54.9), the published winter shift (57.8);
  route 33's lowest member 81.6, every other route's 82.4 or more (asserted).
- **Satisfying to stop at.** R0 is the disruption assessment the field writes; R1 adds the knock-on check a careful
  operations analyst runs and finds nothing; R2 is the half-handled reading once the duty schedule is open.
- **Direction.** Every wrong rung names fewer or more routes than the answer: R0 and R1 drop 27 and 58, R2 adds 33.
- **The decisive move against the seven properties.** 1 no sentence states it; 2 no column marks a relief or a
  feeding route; 3 no reflex reaches it (all three reflexes file route 41); 4 no control bench (no shipped figure
  forecasts the closure); 5 the battery joins nothing across a duty's pieces; 6 not linear (a replay through the
  boards and the duties); 7 survives deletion (nothing is wrong).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every Lot 2 route's Departures over every day of the closure (7.6.1); members not yet observed: the closure's days, forecast from the autumn record (SF7, SF8) |
| 2 | Unit | the Route (7.1, a service number); punctuality per route, not per direction |
| 3 | Attribution window | the closure, 11 January to 28 March 2027 (the plan); the record, 1 September to 6 December 2026 (the prompt) |
| 4 | As-of dating | the timetable and duty schedule in force for the closure's days (both to 3 April 2027; SF14, SF15) |
| 5 | Version basis | the plan's version 2 (it supersedes version 1); the published October final, not provisional, for any back-test (converges) |
| 6 | Denominator | Departures the AVL records (7.2.1); unserved timing points have none (SF12) |
| 7 | Weighting | departures pooled over the window; the closure's day mix converges (SF8) |
| 8 | Window length | the whole autumn record; September to November only converges (SF6) |
| 9 | Inclusivity | the on-time window's edges in whole seconds (SF2); strictly below the floor (SF9) |
| 10 | Rounding path | counts to one percentage to one decimal, once (SF21); the forecast's side of 80 is graded |
| 11 | Tie-break | none needed: no licensed forecast within 1.58 of 80 |
| 12 | Maturity | the autumn record is closed; Sunday 6 December is the last day |
| 13 | Order of operations | the closure's minutes added before the knock-on is passed on; the knock-on in time order through boards and duties |
| 14 | Row order | irrelevant: the replay sorts by scheduled time |
| 15 | Duplicate resolution | a re-sent AVL message is one departure (SF5) |
| 16 | Identity | journeys by journey_ref; vehicles by registration (AVL) against fleet number (register); duty pieces by running board and time against the timetable's block number and times |
| 17 | Netting | none |
| 18 | Units | minutes and seconds; the AVL in UTC, the timetable in local time (SF4) |
| 19 | Code semantics | the AVL's DEP and ARR; a journey turned short ends with an ARR (SF1); the duty schedule's operator stop codes (SMD, MRB, MRC, MRD, RVB) |
| 20 | Integerisation | none on the main call |
| 21 | Clause scope | 7.6.1 forecasts every Route; 7.6.4 keeps reliability measured during the closure (the asks) |
| 22 | Forward window | the closure's days run the winter timetable and duty schedule; Good Friday runs Sunday's timetable (SF8) |
| decisive | the knock-on through the drivers | design-forced: every member of the standing family names 27, 41 and 58 and the record shows the relieved departures leaving late when 41 arrives late (slope 0.96 over 1,824 reliefs); every member without the drivers names 41 alone |

## Literal reader

Executing the prompt, Schedule 7 and the plan word for word, a reader forecasts each Lot 2 route's Punctuality
(7.2.1: departures from timing points other than a journey's last, between one minute early and five minutes
fifty-nine seconds late, in local time, to the second, departures the AVL does not record left out) over every day
of the closure from 11 January to 28 March 2027 (7.6.1, the plan) on the registered timetable (the plan: route 41
keeps its timetable; the TXC to 3 April 2027), with route 41 diverted at the plan's 13 and 10 minutes and Thornsby
Road and Thornsby Quay unserved, the Ring Road crossing 2 minutes slower in the weekday peaks, and names every route
forecast below 80 per cent (7.6.2). The text names no method for the forecast, so every replay of the autumn record
is an option: each one that passes the closure's minutes through the drivers the duty schedule relieves off route
41 names 27, 41 and 58; each one that does not names 41 alone. The easy answer comes from an easy method on the
same literal estimand; no sentence in the pack, read literally, gives it.

## Oracles

None on the main call: no shipped figure forecasts the closure, ranks the routes on it or names the routes a notice
should carry; the published monthly series confirms the autumn record (a Layer 1 control, not a referee of the
call), and the 2025 close-out confirms the plan's running time model. On the asks, the AVL is the one referee of the
designed disagreement between the depot's returns and the control room (a journey the AVL saw run was not lost),
and it hands over no level: it does not carry the lost kilometres, the causes or the boardings.

## Ask sheet

**Main call's declared row population** (the zero-counts run against it): every AVL row; every TransXChange
journey, stop and route link; every row of the duty schedule's Duties and Pieces sheets; Schedule 7 and the plan.
Device and hazard rows: every row of the control room log, the depot's daily returns, the ticket machine extract,
the fleet register, the fare stage table and the cause codes (outside by file). No device writes an AVL, timetable
or duty schedule row (asserted: the main call reads none of the ask files; the uncovered and lost journeys are
absent from the AVL as operation, not as a device).

**The asks** (the workbook's Reliability and Unserved stops sheets):

| Ask | Figures | Construction | Devices on the path | Use |
|---|---|---|---|---|
| Lost kilometres not excused, by route | 9, total 3,174 | every lost span once (the control room log's journeys and part journeys, the depot's uncovered work expanded through the duty schedule and the timetable to journeys, less any the AVL saw run), Schedule 7.5's excused causes left out, part journeys by the route links not run | DV-A1, DV-A2, HZ-A3, HZ-A4, HZ-A5 | the reliability reference 7.6.4 keeps through the closure |
| Reliability, by route | 9, Lot 2 99.60 | scheduled km of the registered timetable over the autumn's days (school journeys on term days) less the lost km above, over the scheduled km | the same | the same |
| Weekday boardings at the unserved stops | 6 (direction by the plan's time bands), total 488 | fare stages 3 and 4 (every stop the diversion leaves unserved), each sale on the journey its bus was running by the AVL, each machine's clock checked against its bus, re-sent uploads once, after-midnight sales on their operating day, 43 weekdays | DV-B1, DV-B2, HZ-B3, HZ-B4 | the passengers the closure leaves without a stop |

**Device ledger.**

- **DV-A1, primary, the same lost journeys under two key schemes (D1).** The control room logs lost journeys by
  journey reference; the depot returns uncovered work by duty and piece. The controller logged most but not all of
  the journeys an uncovered piece lost. Right: expand each returned piece through the duty schedule (running board,
  takes-over and relieved times) and the timetable (the block's journeys between them) to journeys and count each
  journey once with the log's. Wrong stops: sum (the two added, 4,471 in all), controller only (2,463).
- **DV-A2, primary, returned work a spare covered later (D4, absence evidenced in a file no habitual join reaches).**
  On 16 days the depot returned a piece uncovered and the control room found a spare later, so its journeys ran; the
  AVL records them, the log notes half of them as a spare on the board. Every route carries at least one. Right:
  leave out every expanded journey the AVL saw run. Wrong stop: the union without the AVL (3,735), the careful
  solver's path; it moves every route's kilometres and reliability.
- **HZ-A3, the excused list (filed).** Turning a journey short for late running (TR) is not excused (7.5.2); read as
  excused, nine routes move (3,207).
- **HZ-A4, part journeys (filed).** A journey that ends early or starts late loses the route links it does not run
  (7.4.1); counted whole, every route moves (4,413).
- **HZ-A5, part-covered pieces and after-midnight relieved times (visible).** The returns' "Covered from" column and
  the duty schedule's clock times after midnight; taken whole, 4,214.
- **DV-B1, primary, the machine's journey selection (D7, the true key elsewhere).** A driver who does not select his
  next journey at a terminus sells on the previous one, so 5.5 per cent of sales carry the other direction. Right:
  place each sale on the journey its bus was running (fleet register to registration, the AVL's events converted to
  local time; the running board's timetabled journey where the AVL lost the bus). Wrong stop: the machine's
  direction (68 / 38 / 207 against 77 / 39 / 217 inbound; 21 / 40 / 115 against 12 / 38 / 106 outbound).
- **DV-B2, second primary, two machines kept summer time (D8).** Two ticket machines on route 41's buses did not
  change their clocks on 25 October, so their November sales sit an hour late; only their buses' AVL passages at the
  bridge stops show it. Right: shift those machines' sales back an hour before placing and banding them. Wrong stop:
  the AVL placement on the machine's clock (69 / 39 / 206 inbound, 17 / 39 / 119 outbound), the careful solver's
  path.
- **HZ-B3, re-sent uploads (hygiene, seen).** Three nights a machine's day was uploaded twice (747 rows).
- **HZ-B4, after-midnight sales (visible).** Sales after midnight on the last journeys belong to the day the journey
  ran.

**Assertions for the builder** (all in `generator/checks.py`): the logs, the returns and the AVL rebuild the lost
kilometres exactly; each wrong stop of DV-A1 and DV-A2 moves every route's kilometres and reliability; each hazard
moves five routes or more; every route carries late-covered work; DV-B1 and DV-B2 each move four of six cells or
more; no graded figure sits on a rounding tie; no sale at stages 3 and 4 is stamped on a band edge second.

**Pair arithmetic** (`generator/cracker.py` on the cut pack; weights 38 / 7 / 55 over 27 ask figures; the main
side split as the call 10, the nine floor checks 13.5 and the nine autumn figures 14.5). The cracker lands the call
and takes the full includer's path on the asks (the log and the returns merged journey by journey, Schedule 7's
rules executed, the re-sent uploads dropped, every sale placed by the AVL); it keeps 2 of 27 ask figures (route 41's
inbound PM peak cell and the boardings total). The mirror stops at R0, keeps the nine autumn figures and seven floor
checks, and handles the asks the same way.

| Ask figure | Where the cracker's path goes | Mirror (stops at R0) | Cracker (lands the call, executes every filed rule) |
|---|---|---|---|
| Lost km by route (9) | the returned work a spare covered is counted lost | miss | miss |
| Reliability by route (9) | the same kilometres | miss | miss |
| Lost km and reliability, Lot 2 (2) | the same | miss | miss |
| Inbound boardings, AM peak and other times (2) | the two machines' November sales banded and placed an hour late | miss | miss |
| Outbound boardings, all bands (3) | the same machines' sales on the wrong journey | miss | miss |

- **Main-path figures in the ask layer:** the inbound PM peak cell (39) and the boardings total (488) are the same
  under the cracker's path; they are counted in the pair arithmetic, not in the cracker sheet.
- Mirror leakage: 7.4 per cent of ask weight (2 of 27 figures).
- Pair ceiling: 42.6 (C = 38 + 7 + 55 x 2/27 = 49.1; S = 25.0 + 7 + 55 x 2/27 = 36.1).
- Measured by: generator/cracker.py, run on the cut pack by `generator/checks.py` on every build
  (`generator/cracker_sheet.csv`).

## Gate G

- **Litmus.** No reported number in the pack is wrong and nothing is overturned: the AVL, the timetable, the duty
  schedule, the plan and the published series are correct for what they describe. The difficulty is that the route
  is the wrong unit for a delay that people carry between routes.
- **Mechanism:** forecasting: Schedule 7 files the estimand only; the decisive step is the forecaster's own choice
  of the population the closure touches, forced by the duty schedule and the record.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Delete every wrong number:** there are none to delete.
- **No artifact ranks or forecasts.** No prior forecast, no draft notice, no route list for the closure ships; the
  plan names the one bus service that crosses the bridge, which is a fact.

## Tried and rejected

- The blind-reader evidence this screen first recorded as owed at stage 4 is withdrawn, not deferred.
  CLAUDE.md gained a STOP block on 2026-10-27 retiring the solver flow under every name (no scored reader, no
  cold or blind reader, no call-only or draw probe, no isolated thread that answers the task), leaving stump
  power to the paper argument and the portal. The nine-route sweep computed on the clean truth stands as that
  argument. The isolated leak reader and the determinism judge are unaffected and remain stage 4.

- Architecture 1, the January 2027 qualifier forecast from the seasonal return wave (spent 2026-10-27 on its
  second portal return): the graded bin is finer than the estimator. Measured above in `## Architecture 1 is
  spent`. The decisive step was worth 0.58 of a 50,000 bin, the smallest gap in the ladder; the choice between
  two measurable subgroups for the un-returned remainder is worth 0.90 bins and the sampling error on the right
  one another 0.31, so no pin, world parameter or rounding choice forces one bucket. Three repairs were built and
  measured: a later return profile (0.58 to 2.08 bins, still open), positioning the golden by the campaign size
  (about 8,500 of slack a side), and a coarser bin (kills the stump). Re-rooted, not retired.

- Market dilution (riders' January demand is fixed, so returning drivers split a fixed pool of trips and fewer clear 40), worked at the draw: the qualification count needs the hours distribution and a demand forecast stacked on the supply forecast, and the defensible constructions spread wider than any graded bin; dropped before registration.
- A moved threshold with bunching at the old and new lines (the notch response estimated from past windows), worked at the draw: the deciding analysis is a labour-supply response to a notch, honestly economics-econometrics, whose pairing with forecasting task155 holds in the ban window; dropped rather than relabelled.
- The trips-per-driver distribution against the threshold as the decisive step: task151's driver (a stepped payout as the sum of chances from a resampled distribution); kept only as last year's observed rates, never decisive.
- The campaign recruits' type read from when each stopped (an exit-timing reference class): task146's lesson, and the campaign's bonus drivers stopped in April with its seasonal workers; kept only as a rival that misses.
- Holiday drivers (December-only drivers) inside the wave, prototyped: they separate the aggregate KPI route but their share inside each December band changes year to year, which moved every band-priced construction of the golden by up to $140,000 in the prototype; left out of the world.
- A wave timed by each driver's own anniversary, or by weather: neither is what seasonal trades do, and either would make the timing ratio a property of the group; the timing is the trades' common calendar.
- Each seasonal driver's return week fixed once for life (dealt from a profile at entry), built at stage 3: each winter's returners then kept their own mix of weeks, and the January-to-December ratio ran 1.11, 1.01 and 0.97 across the three winters, wider than the fund's bin; replaced by the trades' calendar dealt afresh each winter (which driver returns which week changes, the calendar does not), after which the winters read 1.098, 1.093 and 1.074.
- New drivers priced from the onboarding app's approvals at the as-of, built at stage 3, while drivers approved during the window could still reach 40 trips: the pool-only and every-new-qualifier constructions differed by about $25,000; closed by the terms' eligibility clause (accounts approved by the Sunday before the window, as in 2025 and 2026; 73 drivers who completed 40 trips in the 2026 window on later accounts were not paid), with "every eligible driver" in the prompt.
- Ask A as twelve figures (main run, later runs, returns, recoveries, net, drivers, both years): the main runs and later runs carry no device and hand the strongest response free points; cut to the six device-bearing figures, the chart keeping the full bridge.
- HB3 (an approved applicant whose account was opened under a second email): the applications export carries the driver id an approval opened, so the hazard had no record to live in; dropped.
- Occasional drivers coming back on at 6 per cent a week: they sat in last winter's drivers often enough to swing the June-to-October-blank construction by $13,000; raised to 15 per cent a week (shorter breaks, fewer in the winter group), the construction now within $4,000.
- Approvals stamped at any hour, and Sunday decisions moved back to the Saturday: 24 decisions fell before their own resubmission; decisions are now taken on working days in office hours, a Sunday's on the Monday.

- 2026-10-26, the portal's determinism block, both judges `competing_defensible_answer` on the main call,
  fix location `input_files`. Two forks, both closed without moving a graded figure (`freeze.py check
  --mode determinism` PASS). SF14, the shipped rider demand plan: it carried 316,650 completed trips for the
  guarantee's window, 72.5 per cent of the 436,733 the window actually takes, because it assumed 11.8 per
  cent growth where the autumn ran 19 to 38 per cent ahead and the window itself grew 53.7 per cent. Read as
  a trip ceiling it gave 3,500 drivers and $1,250,000 against the golden's 4,700, and nothing shipped ruled
  that reading out, so a declared distractor was doing the work of an official decoy. Closed by C1 rather
  than by a pin: the generator now sets the plan's growth off the autumn's own year-on-year rate, the window
  carries 447,500 trips, and three assertions hold that no demand-constrained reading binds. SF15, the
  out-of-sample line: "within 2 per cent" did not say what it was 2 per cent of, and the second judge read
  it as the fund's own precision, about plus or minus 94 drivers on 4,700. The write-up now names the counts,
  308 against 306 and 413 against 405, which are returns in the hundreds. The stump is untouched: the
  default path still files $1,450,000 against the golden's $1,650,000, four bins apart.

- **Architecture 2 draw hunt, 2026-10-27 (screens run on paper before any card was registered, under the bin law now filed in `determinism-check`).** Four directions screened against the brief's test, that the decisive step's worth in bins must exceed the defensible-subgroup spread plus the golden estimator's own sampling interval, and that it must not be the smallest rung gap.
  - **Pharmacology, population pharmacokinetics and exposure response (a weight-banded concentrate's forward vial commitment, the requirement built from each patient's own measured elimination rather than the per-kg label dose): dead before measurement.** `guard.py slots` put it on `task170/DESIGN_NOTE.md` line 667, where the same cell was screened with twenty in-cell candidates before any card and every one fell into one of four graves, "effective half-life on sparse troughs" among them as a fit whose estimator family forks the graded figure, with the note's own verdict "the cell is spent for this slot". Bins never reached: the candidate dies on determinacy, which is the (b) term.
  - **Media reach and frequency (a 2027 schedule's net reach from a single-source panel's pairwise duplication against a random-duplication product of marginals): bins pass and Gate F does not.** Measured on paper at a target of 4.21 million with the bin at 100,000 people: decisive step 490,000 people or 4.9 bins, panel sampling interval about 48,000 or 0.48 bins, subgroup spread about 0.2 bins. It dies on readability test 7 instead, because the panel that makes the golden computable makes it a one-group-by (count the distinct respondents the schedule's vehicles reach), and the escape of carrying the joint across a longer window is already recorded dead in `task270/DESIGN_NOTE.md` line 155, a radio schedule's four-week reach from one-week diaries.
  - **A council's already-born cohort (a forward intake read off births and the dwellings completing rather than off each area's own birth-to-intake ratio): dead on the corpus.** task150 is a school-by-school cohort-component projection with a kindergarten-to-births ratio in its own stump sentence and task153 already differentiates against it; the direction is occupied rather than fresh.
  - **A regional waste authority's permitted void (the exhaustion quarter built from the settlement consecutive surveys of one lift measure, against the latest survey's filled volume over a lifetime density): bins pass, the guard blocks.** Measured with the bin at one quarter: decisive step about 3 quarters or 3 bins, survey volume error about 0.4 bins, subgroup spread about 0.2 bins, and the decisive gap is the largest rung gap. `guard.py check` returns BLOCK `test.same_driver` inside the batch against task304 on (time, G3, forecasting), which differentiation does not clear, and BLOCK `test.same_driver_older` against task169 v2; the abstraction test also maps its driver onto task89 v9 and v10, time to exhaustion as a stock over the right net change rather than the published stock over a gross outflow (`guard.py nearest` 0.05). Available only on a redrawn gap or decisive pattern.
  - **Carried forward as the hunt's recommendation:** a pairwise defect's inclusion probability under a sampling design (a filed petition's duplicate signatures seen only when the sample draws both members of a pair, so the duplicate burden expands at the square of the sampling fraction while every single-signature ground expands at the fraction). `guard.py check` WARN, no BLOCK, nearest driver 0.09; measured at 11.4 bins for the decisive step against 2.30 for the sampling interval and at most 0.12 for the subgroup spread. Its two risks are named for whoever takes it: the abstraction adjacency to task264 (an inclusion probability the record's own design sets) and the measured Gate F death of task190's architecture 3, where a design-based projection had to ship the manual that then handed the route back.

- **Stage 2 of architecture 2, 2026-10-27. Four things died or were re-specified under measurement, each with
  the number that killed it (`generator/cracker.py`, six seeds, byte-identical over two runs).**
  - **The draw's own figures.** 1,043,000 filed, a three per cent sample, a 623,212 threshold and 95 and 110
    per cent bands are California's statute on an Arizona card. Rebuilt on Arizona's: 540,000 lines, five per
    cent of the signatures filed, 384,924 required, bands at 95 and 105. The decisive step is unmoved and in
    fact only exact under the new world, because Arizona samples signature lines, so a pair's inclusion is the
    square of the fraction; a three per cent sample of whole sections would have made a same-section pair's
    inclusion the fraction itself and the registered driver wrong as written.
  - **The merged disposition code as neutral Layer 1: rejected.** At a 9.2 per cent share of the sampled
    duplicate strikes, unfolding it moved the golden 0.61 bins while four of six seeds sat 0.03 to 0.19 bins
    from a cell edge, so it was load-bearing on the graded figure and therefore a fork. Closed by C1 in the
    world (SF4): the old-code county's sampled lines carry no duplicate strike at all.
  - **The calibration organ as drawn: rejected in both of its only two directions.** A prior measure projected
    from its own sample and then fully counted either reproduces its full count under the linear expansion,
    which blesses the naive method and is the validated decoy the guard blocks, or fails to, which refutes the
    naive read and is readability test 4 on the decisive rung. Replaced by a prior measure that fell under the
    sampling threshold and was verified by full count only, carrying no projection and no duplicate figure.
  - **A world with a five per cent triple-signer share: rejected.** The all-doubles expansion is then biased
    0.59 bins and the multiplicity mix is not identified from the sample at all, which is a Gate B failure
    rather than a tuning problem. The world draws multiplicity near binary (150 triple signers against 60,000
    double signers) and the bias is measured at 117 signatures, 0.0233 bins, and asserted under 0.05.
  - **Chao1 on the sample's singletons and doubletons, screened as the rival a solver reaches for:** it returns
    minus 3,482,881 valid signatures, so it refutes itself rather than standing as a competing defensible
    answer, and it is recorded in `## Convergence` rather than used as a rung.

- **Stage 3 of architecture 2, 2026-10-27. What the build measured and what it moved.**
  - **Architecture 1's `generator/checks.py`, `verify.py`, `calc.py` and `ops.py`: replaced or deleted.**
    The old checks asserted SF1 to SF15 for forks this architecture does not have, which is the FAIL
    `precut.py` was fixed to catch. The new `checks.py` asserts this build's own eight rows and runs 134
    checks; `ops.py` and the old `calc.py` were architecture 1's fund arithmetic and are gone (138 checks
    after the house-fix pass added a second PDF extractor, the citation resolution and the denominator
    refusal).
  - **The design-stage figures: superseded by the pin.** The note carried a golden of 388,460 against a
    default path of 431,420 at a slip of 400 and a duplicate count of 92. The stage 3 pin (the
    double-signer count, the single-ground rates and the share of the March cancellations falling after
    their signers' dates) moves them to 390,200 against 420,520, which is what the band and cell targets
    cost: the decisive step's full worth falls from 6.99 bins to 4.64 and its worth at the last rung from
    4.33 to 2.96, against (b) plus (c) of at most 1.44.
  - **Rung 2 outside the statutory band at all six seeds: not reachable, and recorded rather than
    smoothed.** Sixty parameter sets were measured over the six seeds against the author's two position
    targets and the rung-2 band together, and none met both, because rung 2 is the golden plus 0.62 of the
    duplicate burden while the golden must sit 2.5 bins clear of both boundaries. The shipped seed keeps
    rung 2 outside the band by 850 signatures and the other five put it inside with its figure three cells
    from the golden's.
  - **SF4's duplicate fold: re-rooted into two single-signature grounds.** The design stage had Navajo's
    merged code covering duplicates and the general class, closed by that county carrying no duplicate
    strike. A wrong split of 34 lines would then have moved the call by 12,920 signatures, 2.6 bins, so the
    fold was a live fork on the main call. The merged code now covers two grounds that both carry at the
    sample's factor (not registered, and registration cancelled), the split is forced by the registration
    the recorder matched, and `checks.py` asserts the projection identical under either reading.
  - **The ask layer: rebuilt on three primaries after the first one measured 0.495 of the ask weight.**
    The design-stage sheet's four devices were a code fold, a correction file, a sheet key and a
    determined-by filter, every one of them documented in a shipped file or found by the hygiene battery,
    so the cracker kept 45 of 91 ask figures and a single response scored 72.0. Rebuilt on three
    reconstructions over dated records (the registration state at the day signed, the firm as at the day
    signed, the day-first dates), with the free per-code ask cut, the cracker keeps 16 of 90 and the worst
    honest reading is 66.4 for a single response and 44.1 for the pair.
  - **SF5 closed by a filed sentence rather than by convergence.** The firms' manifests claim 543,380
    lines against the office's 540,000, which at the design stage was asserted convergent. Measured, the
    manifest basis projects 392,488, which does print the golden's own cell, but the margin is a draw, so
    the filing record now states flatly that the 240 sheets presented in duplicate were struck at receipt
    and are not part of the filing, and the row is closed by that sentence with the convergence reported
    beside it.
  - **Every sheet exactly full: dropped.** 540,000 lines on 36,000 sheets of fifteen makes the sheet
    register a constant column, which the realism sweep reads as a generator's arithmetic. The office now
    receipts 38,080 sheets carrying 5 to 15 lines each and summing to the statutory 540,000, asserted.
  - **The circulator register without the firm on the sheet index: the only way ask B's primary is not a
    fork.** With a firm column on the sheet index or the receipt log there are two defensible firm
    attributions and the ask is forked rather than deviced; both columns are gone and the circulator
    registration extract is the single source, so the as-of join is the work and not a choice.
  - **Floating point in the two expansion factors: removed.** The sample's factor and the pair's
    denominator are computed as integers (twenty and four hundred) because `61 / (0.05 * 0.05)` is
    24,399.999999999996 and cost a signature to rounding in the first write-up.
  - **The global sheet sequence: dead, and the assertion that passed over it with it.** The instruction and
    the filing record both file that a sheet number is the circulator's own series running from one, which
    is what makes the line key need the circulator's registration number as well. The generator numbered
    sheets 1 to 15,044 in one global sequence across all 329 circulators, so no circulator had a series of
    its own and the key claim was false in the data while `checks.py` passed on it: the assertion tested
    that some number repeated across circulators, which a global sequence satisfies by coincidence because
    the returns carry the same number under different circulators only by accident of the draw. Each
    circulator is now numbered from one over its own sheets in receipt order, 412 distinct numbers over
    44,120 sheets, and the assertion tests the claim instead: every circulator's own series is one to n and
    contiguous, and a number is shared by two circulators under different serials.
  - **Ask A's count of each recorder's own determinations: cut, measured.** It was 15 of the sheet's 90
    figures and the cracker kept all 15, because the verification instruction tells a reader how to filter
    the division's lines. Cutting it took the cracker's keep from 0.178 of the ask weight to 0.040 and the
    worst honest single response from 66.4 to 58.2, under the build target of 60, with the main call and
    the projection untouched. The population it supplied now lives inside ask A's own asking sentence,
    where it is not separately graded.
  - **The per-code ask kept in the prompt after its table was cut: a prompt that asked for a deliverable
    the pack's goldens did not carry.** The asks were restructured at stage 3 and `prompt.txt` was not
    rewritten with them, so the shipped prompt asked for a per-disposition-code figure with no table behind
    it and gave the per-month ask the sheet serials instead of the figure the workbook holds. The prompt is
    now written from the three asks the goldens carry, and the month range is pinned in the asking sentence
    (January to June 2028) rather than left to the data.
  - **Two ask-side forks closed by the filing record's own sentences rather than by a convention in the
    code.** A circulator who moves firm is withdrawn on the day its new registration takes effect, so 17
    sampled lines sit on a handover day and the firm they belong to was a convention; and one firm's two
    trading names on one registration number split 141 lines into a fifth firm against an asking sentence
    that names four. Clearing the handover days in the generator was tried first and cannot work: the
    circulators who move are the busiest, so there is no day inside the window on which they gathered
    nothing. The filing record now carries a `Circulator registrations` section stating both conventions,
    which is legitimate on this side of the build because rule 3 binds the main call's decisive step and
    the asks are free of it, and `checks.py` asserts both against the extract's own rows.
  - **The primary-cost assertion rewritten to test its claim.** It asserted that each primary solved on its
    own lifts the cracker's total, which is false once two primaries compose: solving the firm as at the day
    signed while still reading dates month first scores two figures below the cracker's baseline, because
    the right firm with the wrong month moves cells that had matched by accident. It now asserts what is
    actually claimed, that every primary is load-bearing (a response solving the other two without it keeps
    16, 29 and 55 of 75) and that no primary solved alone reaches a third of the ask weight.
  - **Seventy-three per cent of sheets at exactly fifteen lines, consecutive bundle ids and round-robin
    receiver ids: all three dropped as procedural shapes.** The weighted draw over 4 to 15 lines now leaves
    a 27.6 per cent mode at the pad's full fifteen, bundle ids step by one to four, and the six receiving
    staff ids carry an uneven load (274, 228, 174, 94, 82, 53) instead of cycling. The two statewide
    snapshots no longer carry the same row count or a monotonic identifier column, status_changed_utc
    equals the registration date only for the quarter of rows never touched since registration, the query
    notices are spread over ten dates after each line's own return rather than all on one day, and the
    instruction PDF's creation and modification stamps differ.
  - **The 2024 close-out as a pointer: re-subjected rather than cut.** It read as a file placed to be
    compared with this filing. Its county table is now subjected on the examination itself (lines examined,
    examiner days, examination closed) and its header states that every signature line filed was examined
    and no sample was drawn, so it carries its own subject and still ties under every expansion basis.  - **Ask 2's and ask 4's three live forks: closed in the asking sentence, at the cost of the ask's biggest
    device.** The stage 4 re-judge returned NOT_DETERMINISTIC on ask 2 and one boundary line in ask 4 with
    the main call, the projection, ask 1 and ask 3 forced. Which lines count (487 against 484 and 489),
    whose record establishes the registration state on the day signed (the snapshot's own dates, 487,
    against the recorder's finding, 506 to 515 and differing in 11 of 15 counties) and the same-day
    cancellation (487 and 488 against 488 and 489) are now named in the sentence, with the lapsed test
    stated once for both asks. Naming the record and the boundary files the reconstruction as a rule, so
    the registration state at the day signed stopped being a device: it moved into `cracker.py`'s
    `DOCUMENTED` set, the cracker's keep went from 0.040 of the ask weight to 0.240, the single response on
    the call from 58.2 to 66.3 and the pair ceiling from 36.2 to 45.7. Left where it landed: this pass was
    not licensed to chase the ceiling, and 45.7 is what the bar measures.
  - **Closing the same-day boundary by moving the data: not attempted, and would have broken the freeze.**
    The alternative to wording was to move the one Pima signer's cancellation off the day it signed, which
    changes a snapshot row the main call's own registration step reads, so `freeze.py check --mode rubric`
    would have failed on a frozen figure. The wording closure moves nothing graded, which is why ask 2's
    and ask 4's figures are unchanged at 487 and 488.
  - **The primary-lift assertion rewritten again, for the same reason as the first time.** With the
    registration state documented, the assertion that no primary solved alone lifts a response to a third
    of the ask weight was measuring the cracker's whole total rather than the primary's lift, and the total
    is already gated at two fifths. It now measures the lift itself (the day-first dates plus 0.147, the
    firm as at the day signed minus 0.027) and leaves the total to the gate that owns it.
  - **The reconstruction-moves-the-counties assertion re-based.** It compared ask 2's figures with the
    cracker's, which collapsed to one county once the lapsed test was filed. It now compares them with the
    easy route that counts every signer the snapshot shows cancelled (14 of 15 counties move) and asserts
    separately that the day-first dates still move exactly one county's figure, Mohave's.


- **Architecture 2, the Arizona petition sample projection (shipped 10-27), spent 2026-11-01.** The author's Batch 5
  sheet reports the portal's return as "determinism, landed": the call landed. The decisive step (a duplicate
  strike is a property of a pair of lines, so its inclusion probability is the square of the sampling fraction) is
  the field's own design-based expansion for duplicates, the random-sample duplicate formula an elections reader
  reaches for from memory, which the shipped note had named as its standing risk. It was the field's method at the
  top of the ladder, which `stumping` 1.1b says lands. One architecture per world: re-rooted into another client
  domain, world, dataset and shell; nothing of the petition world is carried.
- **Architecture 3 draw screens, 2026-11-01, each set aside on paper before any harness, with what killed it.**
  - The election-polling cell as a whole: task171's slot note screens it across poll averages, house effects,
    turnout after a surge, swing scales, tactical switching, late count streams, mail returns by time since
    mailing, notional boundaries, ranked-choice caps and signature duplicates; with architecture 2 spent there is no
    unscreened driver left in the one Forecasting task type the domain carries, so the domain moves.
  - An amendment that needs a majority of all ballots, roll-off driven by which card of a multi-card ballot the
    question sits on: the card is a column of the ballot layout, so the decisive property is a row predicate
    (readability test 2), and laying the card out in its place is rule application.
  - A new primary school's first reception intake, families with an older child at another school staying there:
    the new school's take-up among children with no sibling tie has no history to measure it, a free parameter
    that forks the golden; the sibling echo of a bulge class at an existing school spreads over four intakes and a
    trend in sibling offers catches it.
  - Landfill void exhaustion with settlement of capped cells counted as void: the survey's cut-and-fill
    conventions fork the consumption, and the regional planning cell is a thin home for an engineering quantity.
  - A teachers' pension plan's retirement wave at first eligibility for an unreduced pension (age plus credited
    service of 85): the eligibility rule is filed, so dating it is rule application, and a step at a service
    milestone is task107's driver.
  - A second-homes council tax premium base eroding as holiday lets cross the business rates letting threshold:
    the flip is a behaviour with no measured response, and the variable is the one the change names.
  - A housing trajectory whose back-test passes because optimistic large sites offset unplanned windfalls: the
    history blesses the naive method until the window breaks it (the validated decoy), as task485's note records.
  - Bus punctuality carried through vehicle workings (a route's departures made by buses arriving late off another
    route): the vehicle chain sits in the AVL the solver already opens, so it is the careful reader's next rung, and
    task469's note set aside delay propagation through aircraft rotations. Kept as rung 2 of this architecture
    (route 41's buses do not interwork), with the crew link as the decisive rung.
  - Reserving, mortality and longevity, deposit runoff, stress testing, event-driven trials, cemetery capacity and
    scaling laws: screened dead in task170, task171, task173 and task174's notes (caps, scheduled dates, persistence
    landing at one year, families that fork), not re-screened.
- **Architecture 3 design, 2026-11-01, approaches set aside while the world was cut.**
  - Route 33 crewed off route 41 with a 12-minute personal needs break: the closure's route 41 arrivals, 13 to 20
    minutes late, reached route 33's departures and took it to 81 to 82 under some replays; the break is 20 minutes
    (gaps of 26 to 35 in the schedule), so no licensed replay brings route 33 under 81.6.
  - Route 58's departures timed four minutes after route 41's arrivals at the same twelve-minute slot as route 27's
    three-minute ones: every 41 arrival frees one driver, so route 58 drew half the feeds it needed; reliefs are now
    placed slot by slot so each arrival crews one departure.
  - A replay passing the closure's minutes through the drivers but not the buses landed routes 27 and 58 at 79 to
    81 on several duty-schedule draws; the autumn levels moved (route 27 to 84.0, route 58 to 85.4) so every member
    of the family lands both below 80 while the named routes stay apart in the autumn ranking (2nd, 4th and 6th).
  - The plan's sentence "no change is expected at other times or elsewhere on the network" read as a network-wide
    claim about bus delays (a Gate G risk); cut to the crossing alone.
  - A lost-mileage ask resting only on the log and the returns being the same journeys under two keys: the careful
    solver merges them journey by journey, so a second device was needed; work the depot returned uncovered and a
    spare covered later (the AVL saw it run) now carries it.
  - Personas Hazel Atkinson and Richard Willis tried and dropped: the card's guard draw (Molly Hughes, Shaun Brown,
    Damien Ward) is kept, with Elliott Sharp and Deborah Stevenson from the same draw for the workbooks' authors.
  - Deborah Stevenson dropped as the returns' author: `guard.py heart` flagged the first name against task130
    (people.first); Yvonne Warner, from the same draw, takes the place.
