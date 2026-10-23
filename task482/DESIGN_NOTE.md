# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 9, drawn 2026-10-23 after architectures 1
to 8 were spent at stage 4: a fresh world and pack in the ETL objective, a mid-sized Ontario city's bike-share
programme naming its Q1 2027 priority stations from each station's share of Q4 2026 service minutes with a bike in
working order docked.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v9, lineage v1 to v8 spent), registered
  2026-10-23 after a fetch of main, `check` re-run on the filed card: WARN, no BLOCK. The first draft carried G3 as its
  decisive generator and BLOCKed on `ban.pattern` against task275, `test.own_lineage` against this slot's v8 and
  `test.same_driver_older` against task477; the decisive generator is G12 (absence of record against record of
  absence: a renter's choice not to take a bike is the record), which is the honest one, with G3 (the feed's record
  against the fleet's operation) as the frame. Against G12 the older task270 v2 and task192 v3 repeat gap, pattern and
  decision type or Gate G and are answered on the card: task270 scales a reported count by a size distribution and
  task192 carries a validation batch's rates; here nothing is scaled or carried, a listed bike's working order is read
  from what renters and the vans did with the bikes in front of them.
- **WARNs answered.** `repeat.gate_g` and `overuse.gate_g` (method or model selection, against task275): the decisive
  step is an estimate of a state no record holds, which is what the mechanism names; no other mechanism on the list
  carries it. `repeat.question_form` (which, against task275): the decision is a set of stations, so the question asks
  which. The deliverable set was moved off svg plus xlsx (task483) and png plus xlsx (task179, task275) to a workbook
  and an HTML chart page, the form a city publishes its station figures in.
- **Pairing:** General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, which
  serves ETL, through the supply-chain-logistics house domain's transportation network: the City's archive of the
  operator's station status feed, the operator's trips, fleet moves and rider fault reports and the City's station
  list conformed into Schedule C's monthly availability for each station, the figure the priority designations read;
  the pay-station vendor's sales export, work orders, register and alarm log conformed to each station for the asks.
- **The decision and the quantity:** the City of Wellhaven runs 24 public bike-share stations and 310 classic bikes
  under an operating agreement with Northlane Mobility. Schedule C makes every station whose availability (the share of
  a calendar month's service minutes, 6:00 to midnight Eastern, that start with a bike in working order docked) is
  under 90 per cent in any month of a quarter a priority station for the next quarter: Northlane keeps a rebalancing
  crew within ten minutes of each priority station through the weekday peaks of February to April 2027. Forward facing:
  the set fixes where the crews stand through the spring.
- **Shape:** `07`, a grid read at its binding cell: each station's availability in its lowest month (24 figures in
  whole per cent), the designation per station and the set, the station that cleared the line by the least and its
  margin; two asks of one figure per station on files the call never reads (24 card-sales figures to the cent, 24
  card-downtime figures in whole hours); a chart's named parts and the two files. About 80 criteria on structure.
- **Strategy:** `other` (a unit's usable state, held in no record, is read from what users and the operator did with
  the units in front of them); Gate G `method_or_model_selection`; gap `objective` (the feed's count is correct for
  what the operator knew and is not the bikes in working order the designation is decided on); pattern none;
  generators G12 (decisive) and G3. Layer 2 family `estimation_fit`, pattern `own:a listed unit's unusability read
  from users passing it over for units of its own type`. Calibration organ: none.
- **World:** an Ontario city, CAD; the City of Wellhaven's Transportation Services and its bike-share programme; the
  operator Northlane Mobility; the pay-station vendor Corlund Kiosk Systems. People from `guard.py names --geo canada
  --seed 482`: Audrey Bautista (the City's bike-share contract manager) and Lawrence Hughes (Northlane's general manager
  for Wellhaven); neither appears in the pack. Every invented name is screened against real organisations, products and
  places before any reader sees the pack (H21).
- **Forcing fact:** Schedule C has the City name the next quarter's priority stations by the 15th day of that quarter
  (15 January 2027), from the quarter just closed.
- **Forum and forcing event:** customer_or_counterparty (the City designates under the agreement and the operator is
  bound by the notice), purchase_order_or_contract. Organisation local_government; role procurement_lead.
- **The physics:** a bike that breaks on a ride (a flat tire, a slipped chain, a seized brake) is docked by its rider.
  About a third of riders report it in the app, and Northlane marks a reported bike out of service within about two
  hours, after which the feed counts it in `num_bikes_disabled`. An unreported broken bike stays in
  `num_bikes_available` until a mechanic's inspection or a van visit takes it to the depot for repair, hours to days
  later. While it is docked every renter at its station takes another bike; at a busy origin station the working bikes
  go first and the broken one is left as the last bike listed. The feed then shows the station with a bike available
  and raises no empty alert; the station is empty to every arriving renter until a returning rider docks a bike or a
  van takes the broken one away.
- **Data-native sentence:** in the trip records a broken bike shows only as a bike that stays docked while renter after
  renter at its station rides away on another bike, until a van takes it to the depot and it is off the street for a
  day or more.
- **Default path and golden, by count:** the feed's available bikes taken as the bikes in working order designate one
  station, W-16 Birch Hill; the bikes rebuilt from the trips and fleet moves, each one that broke on a ride counted out
  of working order until a van took it in, designate four, W-02 Queen and Albert, W-12 Maple Grove, W-16 Birch Hill and
  W-19 Willow Crescent.
- **The WHAT screen.** Population: the City's numbered stations (A.1). Outcome: the minutes of service hours that start
  with a bike in working order docked (C.1). Unit: per cent of the month's service minutes (C.2). Window: each calendar
  month of Q4 2026 on Eastern time (A.3, C.1). Comparison: 90 per cent (C.3). The decisive step settles none of them:
  it is which docked bikes were in working order, which no record or filed rule states.
- **Sources, one line each:**
  - the General Bikeshare Feed Specification's station status and station information fields;
  - bike-share operations practice: riders' fault reports in the app, mechanics' station inspections, rebalancing by
    van on the dispatch system's alerts, winter storage runs;
  - operators' trip export layouts (one row per trip, the bike, its start and end station and times) and kiosk vendors'
    sales exports, work orders, asset registers and alarm logs.
- **Same-puzzle and same-driver tests:** (objective, G12, designation_set) and (objective, G12,
  method_or_model_selection) against the last twelve builds, lineage included: no match in the last twelve; the older
  task270 v2 and task192 v3 matches are differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns: task230 v1 reads a switch's effect against users not yet
  switched; task478 v1 completes a count no instrument recorded by the units that passed; task471 v3 weights a trait
  sampled from two overlapping lists; task486 v2 counts distinct units joined only by pairwise findings. Here nothing is
  completed, weighted or linked across lists: the listed units users passed over and the operator then took in are
  taken out of the usable count minute by minute.

## Default path

1. Read Schedule C: a minute of service hours (6:00 to midnight Eastern) is available at a station when a bike in
   working order is docked there at its start (C.1); a station under 90 per cent of a month's service minutes in any
   month of Q4 2026 is a priority station for Q1 2027 (C.2, C.3).
2. Took the City's archive of the status feed (a row per station whenever a poll found its status changed, polled_at in
   UTC epoch seconds), read each station's last row at or before each minute, carried across the spells the poller was
   down, and read W-17 Linden Avenue under feed ID 117 until feed ID 125's first row.
3. Took `num_bikes_available` (the docked bikes Northlane had not marked out of service) as the bikes in working
   order; a minute is available when it is 1 or more at the minute's start.
4. Divided each station's available minutes by its month's service minutes and listed the stations under 90 per cent
   in any month of the quarter.

Ends on: one priority station, W-16 Birch Hill (87 per cent in October).

Golden: four priority stations, W-02 Queen and Albert, W-12 Maple Grove, W-16 Birch Hill and W-19 Willow Crescent
(88, 88, 86 and 88 per cent in October).

## Stump sentence

The default path counts a station available in every minute the status feed lists a bike there and names one priority
station, Birch Hill (W-16, 87 per cent in October); a bike that breaks on a ride is docked by its rider and stays listed
until a van takes it to the depot for repair, and at the busiest stations it was left as the only bike listed while
renters rode away on the others, so with every bike's spells rebuilt from the trips and fleet moves and each bike the
vans took in for repair counted out of working order from the end of the ride that left it, four stations fall under 90
per cent in October: Queen and Albert, Maple Grove, Birch Hill and Willow Crescent.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), through the
supply-chain-logistics house domain's transportation network, a task type serving Data Extraction & Conformation
(ETL): the feed archive, trips, fleet moves and station list integrated bike by bike into Schedule C's monthly
availability for each station, the file the priority designations read.

Domain test: the deciding quantity is each station's monthly share of service minutes with a bike in working order
docked; integrating the feed with the trips and fleet moves reads each docked bike's working order from what happened
to it (renters passing it over for the bikes around it, then a van taking it to the depot for a day or more), and the
generic count of the bikes the feed lists names one of the four stations the golden names.

Swap: General Statistics, so the swap is of the method: replace the bike-by-bike working order with the feed's listing
and the designated set falls from four stations to one; with another field's nouns ("beds open" for "bikes docked")
there is no renter choosing among the units in front of them and no van taking the passed-over ones away, and the
evidence the decision rests on is gone.

Layer 1: the City's poller archive (rows only on change, UTC epoch seconds, seven spells it was down); trips exported
in Eastern time across the 1 November clock change, with staff rides among them and the week of 16 November appended a
second time; bike numbers prefixed WHB- in the fleet moves log and bare in the trips; the night crew's moves stamped
with their manifest's minute; Linden Avenue moved across the street on the evening of 8 November under a new feed ID
and the same name; four docks added at Birch Hill and Willow Crescent; in the ask files the pay-station vendor's UTC
stamps, voided sales, terminal serials, a sales export naming each terminal's present pay station, and an alarm log of
raises, clears and restarts. Each is what these systems write, none is placed to be caught, and the call holds under
every obvious handling (checks.py L1 to L6), the staff rides kept as the bikes' own records require (L2).

Layer 2: estimation that fits the data (estimation_fit): whether a docked bike could be ridden is recorded nowhere and
has to be read from what happened to it at its station; the feed's count counts every broken bike Northlane had not
yet found.

Decisive step: rebuilding every bike's spells docked at each station from the trips and fleet moves and counting a
docked bike out of working order from the end of the ride that left it when renters passed it over and a van then took
it to the depot for repair, then counting a station's minute available only when a bike in working order was docked.

Not semantics: every field reads as written (the feed's `num_bikes_available` as the docked bikes Northlane had not
marked out of service and `num_bikes_disabled` as the ones it had, the trips' bikes, stations and times, the vans'
moves); read correctly, the listed count still includes every broken bike Northlane had not found, the easy routes
take it (or it less the bikes customers reported) as the bikes in working order, and only what renters and the vans
did with each bike, which no field states, separates the two.

Not rule application: the agreement files the WHAT (the City's numbered stations, the minutes of service hours that
start with a bike in working order docked, each month of Q4 2026 on Eastern time, per cent of the month's service
minutes, under 90 per cent) and no rule or procedure says which docked bikes were in working order. Measured on the cut
pack (checks.py G2, G3): the enumerated family (the feed as listed; the feed less the bikes customers reported, from the
ride that left them; dwell cut-offs of 24 and 48 hours of any end or ended by a van; every bike a van took away; depot
stays of 6 to 48 hours; bikes passed over once or three times) files five distinct sets with the lowest months spread
up to 4.1 points: W-16 alone (the feed, the reported bikes, a 48-hour van dwell), W-16 with W-23 (a 48-hour dwell of any
end), W-12, W-16 and W-19 (a 24-hour van dwell), nineteen or more stations (a 24-hour dwell of any end), and the golden
four (every reading by the vans' pickups); the standing family, the readings the records leave defensible (a depot stay
of 6, 12 or 20 hours, a pass by a renter before the van took the bike, every van pickup but the station move, and their
intersections), files the golden four at a spread of exactly zero on all 72 station-months. What rules the rest out is
the data itself, silent: the feed and the reported bikes alone by bikes passed over by renter after renter and then
kept at the depot for days, the 48-hour and 24-hour van dwells by broken bikes the daily downtown inspection took in
within hours, the any-end dwells by working bikes left alone at quiet stations and ridden by the next renter, and the
station move by its bikes dropped across the street 25 minutes later and ridden.

Analyst test: with every field and rule read correctly, a strong analyst takes the status feed's `num_bikes_available`
at each station each minute as the bikes in working order (Northlane's own count of the bikes it had not taken out of
rental), computes each station's share of each month's service minutes with one docked, and names one priority
station, W-16 Birch Hill (87 per cent in October): the default path's Ends on (checks.py T1 on the clean truth, T2 on
the pack); the decisive step alone files the golden four (T1, T2).

Estimand: the operating agreement's Schedule C (bike_share_operating_agreement_schedules.pdf, C.1 to C.3, with A.1 and
A.3): the population (the City's numbered stations, a station moved within its block one station), the outcome (the
minutes of service hours, 6:00 to midnight Eastern, at whose start at least one bike in working order is docked, a bike
being in working order when a customer can unlock it and ride it away), the window (each calendar month of Q4 2026),
the unit (per cent of the month's minutes of service hours) and the comparison (under 90 per cent in any month).

No decoy: nothing is planted: the bikes broke on rides as bikes do and were docked by their riders, the feed is
Northlane's ordinary status feed as the City's poller kept it, the fault reports are the ones customers made, and no
memo, report, draft or stakeholder figure states any station's availability or argues for the listed count.

No certified replay: the method is not recovered by reproducing certified or published figures; Northlane's quarterly
report states no station's availability, and no figure in the pack ties only under the golden.

Lesson: a count of units a system lists as available includes units nobody can use; integrated with the records of
what users and the operator did with each unit, a listed unit passed over while the units around it were taken, and
then taken in for repair, is read as unusable from the moment it was left, and availability is counted from the usable
ones; no build on file reads a unit's state from what was done with the units in front of it.

## Readability screen

| Rung | What a solver has to see | Where it is | Verdict |
|---|---|---|---|
| R0 the feed as listed (the default) | `num_bikes_available` per station per minute | the archive and its notes | readable |
| R1 the bikes customers reported, from the ride that left them | the fault reports and the feed's disabled count | the reports file, D.1 | readable |
| R2 the station move, the repeated week, staff rides, the clock change | the station list, a second copy of a week, the rider type, durations | the trips, the station list | readable |
| R3 (decisive) the bikes that broke on a ride, read from renters passing them over and a van taking them to the depot for a day or more | each bike's spells rebuilt from two files, and what happened at the end of each | no sentence; only the trips and the fleet moves together | silent |

No sentence in the pack says a listed bike may be broken, that renters passed bikes over, or that a van pickup can mean
a repair: C.1 defines working order by what a customer can do, D.1 says when a reported bike is marked out of service,
D.2 that mechanics take faulty bikes to the depot, and the notes give the feed's fields in GBFS's words.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | station | the City's numbered station (W-17 one station under feed IDs 117 and 125) | each feed ID a station | same call (Linden Avenue is clear of the line under either) | A.1: a station moved within its block keeps its number and remains the same station |
| SF2 | service hours | 6:00 to midnight Eastern every day | the same hours in UTC | same call | C.1 and A.3: Eastern time |
| SF3 | available minute | a bike in working order docked at the minute's start | docked at the minute's end | same call | C.1: "at the start of the minute" |
| SF4 | bike in working order | a bike a customer can unlock and ride away | a bike Northlane lists as available | W-16 alone | C.1 defines the bike by what a customer can do with it; D.1 marks a bike out of service only after a report; the listed count is a measurement of the term, and its bias is the decisive step, not a reading |
| SF5 | calendar month | the month on Eastern time | the UTC month | same call | A.3 |
| SF6 | under 90 per cent | strictly under | at or under | same call (no lowest month within half a point of 90: 88.2 and 90.7 the nearest) | C.3: "under 90 per cent" |
| SF7 | the quarter | October to December 2026 | none | same call | C.3: the calendar months of the quarter |
| SF8 | rounding | the line compared on the unrounded share | the share rounded first | same call | nothing within half a point of 90 |
| SF9 | docked | a bike in a dock at the station | a bike in a van at the station | same call | C.1: docked at the station |
| SF10 | the station move | no bike docked at either site from 23:00 to the drop at 125 | the 25 minutes left out | same call (W-17's lowest month is October) | C.1: minutes of service hours with a bike docked |
| SF11 | the poller's down spells | not read by the golden | carried or left dark on the default path | same call (the golden reads no feed row) | the golden is rebuilt from the trips and moves |
| SF12 | the repeated week | each trip once | the week counted twice | same call (asserted, L1) | exact repeats of the same trip ids |
| SF13 | staff rides | kept: they moved bikes | dropped as not customer trips | W-12 and W-16 | the bikes' own records: dropped, 461 rides start where the bike was not (L2) |
| SF14 | the repeated hour of 1 November | each trip placed by its duration | the first reading of the hour | same call | duration_s |
| SF15 | the start of the records | a bike first recorded leaving a station docked there from 20:00 on 23 September | left out until its first record | same call | the quarter starts a week into the records |
| SF16 | priority station for Q1 2027 | under 90 per cent in any month of Q4 2026 | none | same call | C.3 |
| SF17 | the station that cleared the line by the least | the lowest month's margin above 90 among the stations not designated | an average over the months | same call (the line is cleared only when every month clears) | C.3: any month |
| SF18 | ask A, a station's card sales | approved sales less voids at the pay station the sale was made at | the export's pay_station column | every station's figure | the work orders' terminal replacements and the register's install dates |
| SF19 | ask A, the fourth quarter | Eastern time | UTC | four stations' figures | A.3 and the City's quarter |
| SF20 | ask B, could not take a card payment | a COMMS_LOST or READER_FAULT alarm active, from its raise to its clear or the pay station's next restart | each raise paired with its code's next clear | every station's figure | the log itself: after a restart a fault still present is raised again in the same second, and sales resume after restarts with no clear (B4) |
| SF21 | ask B, the service hours | a set of hours, overlapping alarms counted once, inside 6:00 to midnight | durations summed | same figures at whole hours (B3) | the asking sentence: the hours in which it could not |

## Ladder

| Rung | What the response does | Call | What refutes it |
|---|---|---|---|
| 0 | the feed's available count as the bikes in working order (the default) | W-16 | bikes passed over by renter after renter, then kept at the depot for days, stood in that count |
| 1 | the feed less the bikes customers reported, each from the ride that left it | W-16 | two thirds of the bikes the vans took in for repair were never reported |
| 2 | a dwell cut-off: a bike docked 24 hours or more before a van took it is counted out | W-12, W-16, W-19 | the daily downtown inspection took broken bikes in within hours at Queen and Albert |
| 2b | staff rides dropped before the spells are rebuilt | W-12, W-16 | bikes then leave from stations they were never at |
| 3 (decisive) | every bike passed over and taken to the depot for repair counted out of working order from the ride that left it | W-02, W-12, W-16, W-19 | nothing: the standing family files it at a spread of zero |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the City's 24 numbered stations, W-17 under two feed IDs | filed (A.1); SF1 asserted |
| 2 Unit of account | a station's month; a docked bike's spell within it | the question names the station; C.2 the month |
| 3 Attribution window | each calendar month of Q4 2026 on Eastern time | filed (A.3, C.1, C.3); SF2, SF5 |
| 4 As-of dating | the records to the 10 January extract; each minute's state at its start | filed (C.1); SF3 |
| 5 Version basis | none on the main path: the trips once each | SF12 |
| 6 Denominator | the month's minutes of service hours | filed (C.2) |
| 7 Weighting | none: each minute counts once | filed (C.2) |
| 8 Window length | 6:00 to midnight each day | filed (C.1) |
| 9 Boundary inclusivity | under 90 per cent | filed (C.3); C1, nothing within half a point (SF6) |
| 10 Rounding path | the line on the unrounded share; figures rounded once | SF8; the prompt's rounding |
| 11 Tie-break | none: no lowest month on the line | C1, asserted |
| 12 Maturity and censoring | every Q4 spell's end is inside the records (to 10 January) | C1, asserted (the golden equals the truth) |
| 13 Order of operations | spells rebuilt before the minutes are counted; one order | C1 |
| 14 Row order | none: every figure is a set computation over sorted events | C1 |
| 15 Duplicate resolution | the repeated week counted once | SF12, asserted |
| 16 Identity normalisation | feed IDs to City stations through the station list; bike numbers with and without WHB- | the station list; L5 |
| 17 Netting against gross | none on the main path; ask A nets voids | SF18 |
| 18 Dimensional units | minutes and per cent; dollars; hours | filed (C.2); the prompt |
| 19 Code and status semantics | rider types, move actions, alarm codes | file semantics; never the stump; SF13, SF20 |
| 20 Integerisation | minute counts whole | C1 by construction |
| 21 Clause scope | Schedule C's test for every station, every month | filed (C.3) |
| 22 Forward window contents | the designation governs Q1 2027; the call rests on closed records | not live: Schedule C reads the quarter just closed |

## Literal reader

Executed word for word, the prompt and Schedule C ask for each numbered station's share of each Q4 2026 month's minutes
of service hours that start with at least one bike a customer could unlock and ride away docked there, and for the
stations under 90 per cent in any month. No record holds whether a docked bike could be ridden: the feed holds what
Northlane had marked, the trips and fleet moves hold where each bike was and what was done with it. So the literal
estimand is unobserved and is estimated from the records, bike by bike; every licensed reading of the records (a depot
stay of 6 to 20 hours, a renter's pass, every van pickup but the station move, and their intersections) files the same
72 station-months to the minute, and every term in the fork table files the same call or is ruled out by a quoted
sentence. The golden is the literal estimand's estimate, not a reading of a term.

## Oracles

- No file states a station's availability: Northlane's quarterly report gives system trips, casual trips, fleet moves
  and fault reports by month, nothing by station.
- The feed's available plus disabled bikes equal the bikes rebuilt as docked at every minute the poller ran (T3): an
  identity every reading passes, which separates nothing.
- The pay-station sales export's quarter total is the same under the export's own column and under the terminals'
  history (A2): no control ties only under the golden.
- The alarm log carries no per-station downtime total; the work orders carry no hours.

## Ask sheet

Two asks, both on files the call never reads: the pay-station vendor's sales export with its work orders and register
(ask A), its alarm log with the register's alarm codes (ask B). Zero device rows sit in the call's population: no trip,
move, report or status row is read by either ask, and no pay-station row by the call (X1 and X2).

- **Ask A, each station's Q4 2026 pay-station card sales, dollars to the cent (24 figures).** H18 home: a second
  measure every station carries, the fares its pay station took beside the availability it is judged on. User: the
  City's bike-share programme (the fares are the City's under the agreement). Primary device: D7 a field overwritten
  later (the vendor's export names each sale's pay station from the terminal's present pay station, and every pay
  station's terminal was replaced in the autumn refurbishment by one from the pool, the one taken out refurbished and
  installed elsewhere, so every station's pre-replacement sales are filed under another station; the quarter's total
  is unchanged, so nothing ties wrong). Evidence, split: the register's install dates (a terminal installed on 12
  November cannot have sold at its present pay station in October) and the work orders' replacements (which terminal
  left which pay station when). Hazards: voided sales as rows of their own, the stamps in UTC (the quarter on UTC moves
  four stations), Linden Avenue's move (its pay station kept its number). Stops: the export's column (0 of 24), the
  sales before each terminal's install dropped (0), voids kept (2), the quarter on UTC (20), the golden.
- **Ask B, each station's Q4 2026 service hours its pay station could not take a card payment, whole hours (24
  figures).** H18 home: the same stations' pay-station service, a second measure beside availability. User: the
  City's bike-share programme. Primary device: D4 absence as the signal (a pay station restarts every night at 3:00
  and on its own watchdog after an hour without a network; a restart clears its alarms and it raises again, in the same
  second, any fault still there, so an alarm a restart cured has no clear, and the terminal replacements end their
  reader alarms the same way). Evidence, split: the restarts and the same-second raises in the log, and sales resuming
  after restarts in the sales export. Hazards: non-blocking codes (receipt paper, the service door, the cabinet heater on
  cold days), overlapping alarms (summed alike at whole hours), the service-hours window, the stamps in UTC. Stops: each
  raise paired with its code's next clear (0 of 24, and 3,868 sales inside those spans), alarms with no clear dropped
  (0), an open alarm ended at the next event of any kind (4), every code counted (0), the golden.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | the sales export's own pay_station column, voids netted, the quarter on Eastern time | miss |
| B | each COMMS_LOST and READER_FAULT alarm paired with its code's next clear, inside service hours, overlaps merged | miss |

Measured on the cut pack: ask A keeps 24 of 24 once each sale is placed by its terminal's history and 0 of 24 by the
export's column; ask B keeps 24 of 24 once restarts end alarms, 4 of 24 if an open alarm is ended at the next event of
any kind, 0 of 24 under every other pairing. A response that finds both devices and lands the call scores 100; one that
lands the call and finds neither scores 45; the default path with neither scores 12.

Pair ceiling: 28.5 (the cracker 45.0 with none of 48 ask figures, the mirror 12.0 with none; with the next-event repair
on both, 33.1).

Mirror leakage: 0.0 per cent of ask weight.

Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

1. Domain: bike-share operations' own reading of station availability, a docked bike's working order read from what
   renters and the vans did with it (passed over while the bikes around it were taken, then taken to the depot for
   repair) against the operator's listing; with a hospital's nouns ("beds open") no renter chooses among the units in
   front of them and no van takes the passed-over ones away.
2. Real work, nothing planted: every Layer 1 item is what the producing system writes (the City's change-only poller
   archive with its down spells, the trips across the clock change with staff rides and a re-run week, the moves log's
   prefixed bike numbers and manifest-stamped night moves, the station move under a new feed ID, the dock expansions,
   the pay-station vendor's UTC stamps, voids, present-location column and restart-cleared alarms); none is on the
   decisive step, and no ask device row sits in the call's population (X1, X2).
3. The step that flips the call is analytical: estimating a state no record holds (whether a docked bike could be
   ridden) from two records integrated bike by bike; no clause makes the choice (C.1 defines working order by what a
   customer can do, D.1 and D.2 say how bikes are marked and taken in).
4. Analyst test: every field and rule read correctly, the feed's available count names W-16 Birch Hill alone (87 per
   cent in October), asserted on the clean truth and on the pack (T1, T2); the reported bikes alone keep it (G3).
5. Schedule C files the estimand (A.1, A.3, C.1 to C.3) and no estimator; the standing family (depot stays of 6 to 20
   hours, a renter's pass, every van pickup but the station move, and their intersections) files the golden four at a
   spread of zero on all 72 station-months (G2), and every bike it counts out of working order in a minute it decides
   broke on the ride that left it (G4: 95 spells, none not).
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest drivers task471 v3, task98 v2 and task230 v1 at 0.07; task270 v2 and task192
   v3 differentiated on the card.
8. Re-read against the built pack at stage 4: (the scored readers' result, filled on their return).
9. Judge: (the judge's verdict, filed on its return).

leak.py REVIEW lines (zip 14ceb178), each harmless:
- the agreement's and the archive notes' estimand vocabulary (docked, minute, working, Eastern, available): Schedule C
  and the feed's GBFS field definitions, which exist without the trap; neither says a listed bike may be broken;
- the trips, station list, GBFS snapshot and pay-station files naming every station beside numbers: identifiers, trip
  times, capacities, sales and serials; none ranks the stations on availability;
- the archive notes naming three stations beside numbers: Linden Avenue's two feed IDs and the two expanded stations'
  docks.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
