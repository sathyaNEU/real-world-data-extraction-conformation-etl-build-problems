# task468 design note: Larkhaven's frequent corridor nominations

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json` (architecture v1), registered 2026-10-17 after a pull, so
  every card filed before it was in the check, and re-checked after the design moved the decisive step onto the
  review's design weights. Guard check WARN only, each answered here: identity_resolution as the strategy (no field
  resolves an unmatched departure's route; the review measures the routes only on a sample, so the step is error
  propagation, not a reading); the data-integration pattern already carried by task449 (false links diluting a share
  among k equally plausible targets), task454 (imputation within a known stratum) and task466 (a log-Pearson fit to
  two linked records), where here missed links select and the clerical review must be weighted by its own design;
  Gate G method_or_model_selection repeats task239 and is in six of the last twelve (it is the honest key: the review's
  raw route mix against the mix its design weights give); the question form "which" repeats task239 and task158 and
  comes from the decision, a slate of routes. Differentiated against task116 v3, task452 and task454 on the card.
- **Seed:** ET25 (a transit agency brands routes Frequent Network, and qualifies them for a state capital grant, when
  they meet a service standard on weekdays; a GTFS checker certified a 30-minute route and rejected a frequency-based
  10-minute one). Kept: the world (a transit agency, its GTFS feed, a state capital program), the decision (which
  routes qualify and are nominated) and the quantity (each route's frequency in every hour of the weekday span).
  Dropped: the seed's mechanisms (service days, times past 24:00, frequency-based trips), which are data semantics;
  they survive as Layer 1.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL, client
  pattern 1 (propagate linkage error to the estimate, match weights and clerical review: false links attenuate, missed
  links select; shortcut, links above a cutoff as truth). The state counts delivered departures, and the department's
  only record of them is the AVL vendors' stop events, which reach a route only through the vendors' trip matchers; the
  conformed evidence is a linked dataset, and the deciding counts are estimates from it. GSDS is a methods domain, so
  the swap is of the method: replacing the propagation of the matchers' error (the clerical review weighted by its
  design) with the links taken as truth, a share-out in proportion to the links, or the review's raw mix moves the
  nominations.
- **Shape:** 01, a ranked list under a cap: each of the eleven candidate routes passes or fails the delivered
  standard, and the state takes at most five per agency, the highest in average weekday boardings first; the criteria
  are each route's verdict, the five, the first qualifying route left out, plus each candidate's count of outbound stops with no shelter on 30 June 2026.
- **Strategy:** identity_resolution (linking records to the units they belong to), decisive generator G6 (the
  unmatched departures' route mix is not the matched mix, and the review's raw mix is not the unmatched mix), with G12
  (no route on a record is not no departure) and G3 (the AVL record against the bus that ran).
- **World:** the United States, an unnamed Midwestern state. The City of Larkhaven runs Larkhaven Transit as a city
  department (about 64 buses out on a weekday, fourteen routes through five transfer points). The state Department of
  Transportation's Frequent Transit Corridors Program funds stop, shelter and signal-priority work on routes that
  delivered frequent service; for the FY2027 round an agency nominates at most five routes, each of which must have
  averaged at least four departures from its designated stop in each clock hour from 6 a.m. to 7 p.m. on the weekdays
  from January to June 2026 (state holidays excluded), counted from the agency's AVL records whether or not the records
  tie a departure to its route; an agency with more qualifying routes nominates those with the highest average weekday
  boardings in its ridership report. Larkhaven's CAD/AVL vendor changed at 7 p.m. on 31 March 2026 (Arbor Fleetware to
  Quinnell Transit Systems, whose export is in UTC, keyed by public stop code and asset tag and concatenated from daily
  files); both vendors' trip matchers tie a stop event to a scheduled trip when the bus is within seven minutes of the
  timetable and leave it with no trip otherwise. Service Quality reviews the matchers each month: it lists the bus-days
  with at least one unmatched event at the five transfer points, draws 400 at random, and reviews one unmatched event
  on each, chosen at random, against the bus's CCTV, recording the route the bus was operating or that it was out of
  service.
- **Forcing fact:** the state's application closes on 1 December 2026; the City Council authorizes the nominations by
  resolution at its 17 November 2026 meeting, and the service planning manager's workbook goes to the council's
  Transportation Committee first. As-of: 30 October 2026. The call is retrospective by the program's own design (it
  certifies service delivered in a closed period) and faces forward in what it funds (FY2027 work on the five routes).
- **Forum and forcing event:** council_or_assembly (Larkhaven City Council), vote_or_meeting (the authorizing
  resolution). Organisation local_government; role programme_officer. Personas from `guard.py names --geo "United
  States" --seed 468`: Wendy James (Manager, Service Planning and Grants, who prepares the nominations), Eric Thomas
  (ITS systems administrator, who signs the cutover notes) and Alfred Hensley (Service Quality analyst, who runs the
  trip-matching review), with Mitchell Boyd and Jeffery Collins, the Service Quality analysts who share the reviews
  (initials in the log); Diane Beck replaced, her first name in task105.
- **Data-native sentence:** the matcher ties a stop event to a scheduled trip only when the bus is within seven minutes
  of the timetable, and the buses outside it are the late ones on the trunk routes that share the Transit Mall, so the
  events left without a trip are mostly the trunk routes' and pile up on their bus-days; a review that takes one event
  from each sampled bus-day sees each late trunk bus-day once however many of its events went unmatched, so its raw
  route mix understates exactly the routes the matcher failed most.
- **The WHAT screen.** Population: departures by buses of the route in revenue service from its designated stop on the
  counting days (guidance 3.2 and 3.4, departures counting whether or not the record ties them to the route; no
  departure goes unrecorded). Outcome: the average number of such departures in each clock hour from 6 a.m. to 7 p.m.
  by the time the bus left (guidance 3.3). Window: service days 1 January to 30 June 2026, weekdays less four state
  holidays (125 days). Unit: departures. Comparison: four in every one of the thirteen hours, then the five-route cap
  by the ridership report (guidance 5.1). The decisive step settles none of them: it is how a route's departures are
  estimated from records a sixth of which carry no trip, through a review whose raw mix the data's own structure (the
  review's one event per bus-day against bus-days carrying 1 to 16 unmatched events) shows to be unrepresentative.
- **Deliverables:** `larkhaven_frequent_corridor_nominations_fy2027.xlsx` (the call, each candidate's verdict and
  lowest hour, its outbound stops with no shelter on 30 June 2026, and the chart of the lowest hours).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution 1: the
    client's own pattern for the task type; here the missed links select by lateness and the clerical review is the
    department's routine trip-matching audit, whose design (one event per sampled bus-day) is part of the propagation.
  - `stumping/references/client/measured-drivers.md`: the held group is compound (a conjunction whose partial
    application scores wrong); 133 v1 died on a development sample signposting its decisive step, so here using the
    review is the rung below the decisive move and weighting it is the move.
  - `dataset-generation/references/layer1-messiness.md`: two vendor exports (local against UTC, stop ids against stop
    codes, fleet numbers against asset tags), a cutover overlap, repeated rows at daily-file heads, renumbered stops,
    schedule times one vendor holds to the minute against the feeds' half minute, GTFS frequency-based trips, times
    past 24:00, a class-day service; none on the decisive step, each asserted neutral.

## Default path

1. Conform the two AVL exports to one table of departures at the five designated stops in local time: Arbor's stop
   ids to stop codes through the January feed's stops.txt, Quinnell's UTC to Central time and its asset tags to fleet
   numbers through the roster, Quinnell's repeated file-head rows and its share of the evening of 31 March dropped.
2. Keep the counting days (125 weekdays, the four state holidays out) and the clock hours 6 a.m. to 7 p.m.
3. Count each route's departures in each hour from the events the matchers tied to its trips; 17,112 of the window's
   106,687 events have no trip.
4. Share each stop-hour's events with no trip among the stop's routes and "out of service" by the route mix Service
   Quality's review found at that stop (the share of reviewed events by route).
5. Average over the 125 counting days, take each route's lowest hour and compare it with four; Route 17's lowest hour
   is 3.6, Route 2's 4.2.
6. Rank the routes that qualify by average weekday boardings and take five.

Ends on: Routes 2, 4, 6, 22 and 11

Golden: Routes 2, 4, 6, 17 and 22

## Stump sentence

The default path shares each stop's events with no trip by the raw route mix of Service Quality's reviewed events, but
the review takes one event from each sampled bus-day, so a Prairie Road bus-day with a dozen unmatched events counts
once like a Lincoln Avenue bus-day with one, Route 17's share at the Transit Mall comes out at 35 per cent against the
57 its bus-days carry, Route 17's lowest hour falls to 3.6 and the default path nominates Routes 2, 4, 6, 22 and 11;
weighted by each reviewed event's bus-day count of unmatched events, Route 17 averages at least 4.7 in every hour and
the five are Routes 2, 4, 6, 17 and 22.

## Three rules

Task type: data-integration-record-linkage-entity-resolution: two AVL vendors' stop events conformed to one record and linked to the timetable's trips by the vendors' matchers, whose missed links are propagated into each route's departures through the department's clerical review, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each route's departures per hour estimated from a linked record whose missed links select (late trunk buses fall outside the seven-minute window), and the field's estimator is the clerical review's measure of the missed links' route mix, weighted by the review's own sampling design (one event of a bus-day's unmatched events, so each reviewed event stands for its bus-day's count); taking the links as truth, sharing the misses in proportion to the links or reading the review's raw mix each moves the nominations.

Swap: "a hospital's discharges per ward counted through a patient-matching engine, the unmatched discharges shared out by a chart review that pulls one chart per sampled shift" keeps the shape, because in a methods field the setting is always another field's; the swap is of the method, and the call fails the moment the design-weighted review is replaced by the raw review mix or a proportional share-out, while the seven-minute window, the Transit Mall's interlined trunk routes and the bus-day as the review's unit are the department's own.

Layer 1: Arbor's export in local time keyed by GTFS stop id and fleet number with each event's service date; Quinnell's in UTC keyed by public stop code and asset tag, concatenated from daily files whose heads repeat the previous file's last ten minutes under new EventIDs, its schedule times to the second from the feeds; Arbor's schedule times held to the minute where the timetable sets some departures at the transfer points to the half minute; both systems recording the evening of 31 March; the April timetable's renumbered stop ids; Good Friday on the Saturday timetable and the 3 February snow day run on it though the feed shows a weekday; the feeds' frequency-based University Connector, College Hill's class-day trips in calendar_dates only, trips past 24:00. Each is the department's systems as they run, asserted neutral for the call (checks.py R2 and the separation check, which blanks every schedule field).

Layer 2: estimation_fit, the design-based estimate of the missed links' composition: the clerical review samples bus-days with equal probability and one event within each, so each reviewed event carries its bus-day's count of unmatched events as its weight, and the raw mix understates the bus-days the matcher failed most.

Decisive step: weighting each reviewed event by its bus-day's unmatched events at the five stops (and each month by its bus-days listed over the 400 drawn) before taking each stop's route mix, which puts Route 17 at 56 per cent of the Transit Mall's events with no trip against the raw 35 and lifts its lowest hour from 3.6 to 4.8, nominating Routes 2, 4, 6, 17 and 22 instead of Routes 2, 4, 6, 22 and 11.

Not semantics: every field, code, unit and definition read correctly (stop ids and codes, UTC, asset tags, the repeated file heads, the review's route and finding, the guidance's departures whether or not tied to the route) still leaves the easy route sharing the unmatched events by the review's raw mix, because no field says the reviewed events are unequally likely to be drawn; the review memo states how the sample is drawn, as every audit does, and turning that into weights is the estimator's choice, not a reading.

Not rule application: the guidance fixes the population, the hours, the counting days, the standard and the cap, and the review memo fixes how Service Quality draws its sample; no rule or procedure says how the unattributed departures are shared among routes, and executing every filed rule with the review's raw mix files Routes 2, 4, 6, 22 and 11, so the step no rule performs is weighting the review by its design.

Analyst test: a strong analyst who conforms both exports, reads every field and applies every program rule shares the unattributed departures by the review's raw route mix and files Routes 2, 4, 6, 22 and 11 (the default path's Ends on), with Route 17 at 3.6 in its lowest hour; one who shares them in proportion to the attributed departures files Routes 2, 4, 9, 22 and 11; the design-weighted review files Routes 2, 4, 6, 17 and 22.

Estimand: the State Department of Transportation's FY2027 program guidance (3.2 a departure is a bus of the route in revenue service leaving its designated stop, counted in the clock hour it left; 3.3 the standard, an average of at least four departures in each of the thirteen clock hours beginning 6 a.m. through 6 p.m. over the counting days; 3.4 the counting days and the evidence, departures counting whether or not the agency's records tie them to the route; 5.1 the cap of five by average weekday boardings in the agency's ridership report).

No decoy: nothing is planted to be caught; the exports are the vendors' records as delivered, the review log and memo are Service Quality's routine audit and state no route shares, no memo, draft or briefing argues a method, a share or a route list, and the ridership report, the candidate list, the fleet roster, the farebox workbook and the Title VI report are what the department keeps.

No certified replay: no published or certified figure reproduces only under one method; the review memo's monthly tally (bus-days listed, drawn, reviewed, findings by kind) ties under every handling, no document gives a route's departures or a nomination, and nothing is recovered by matching a filed number.

Lesson: a clerical review that samples clusters (bus-days) and takes a fixed number of records within each must be weighted by each cluster's size before its mix stands for the records it audits, because the clusters the linkage fails most hold the most unmatched records and are seen no more often than the rest; no build on file propagates linkage error through a review whose within-cluster take makes its raw mix unrepresentative.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the timetable's departures (Routes 2, 4, 6, 17 and 9) | guidance 3.4 counts departures from the AVL records, not the timetable: fires | none | the feeds are the obvious schedule source: fires | none | none | one count per route-hour: fires | readable |
| R1, the departures the matchers tied to a route (Routes 4, 22, 11 and 40) | guidance 3.4 counts a departure whether or not the record ties it to the route: fires | the blank trip on a sixth of the events: fires | none | none | none | one group-by: fires | readable |
| R1c, the unattributed shared in proportion to the attributed (Routes 2, 4, 9, 22 and 11) | none | none | proportional allocation of unknowns is the reflex: fires | the review's mix at every stop contradicts it: fires | none | one ratio per stop-hour: fires | readable |
| R2, the review's raw route mix (Routes 2, 4, 6, 22 and 11) | the review memo says what the review is: fires | the review log carries the route: fires | using the audit sample's mix is the reflex once found: fires | none | none | one share per stop: fires | readable |
| R3 (decisive), the review weighted by its design (Routes 2, 4, 6, 17 and 22) | the memo says how the sample is drawn and nothing about weighting or about bus-days carrying different numbers of events: silent | no column carries a bus-day's count of unmatched events or a weight; it has to be built from the AVL record by bus and service day: silent | the reflex reweight is to a population margin (post-stratifying by stop, band or month), which leaves the raw mix in place: silent | no control or published share scores the review's estimate: silent | every file reconciles, nothing is anomalous: silent | the weight is a count joined from another file, not a ratio of reported figures: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | departure | a bus of the route in revenue service leaving the designated stop | every stop event at the stop, out-of-service movements included | a different five (the out-of-service events shared to routes) | guidance 3.2 "in revenue service"; the review records out-of-service movements |
| SF2 | the clock hour of a departure | the hour in which the bus left, local time | the scheduled hour, or UTC | same call on the scheduled hour (asserted); UTC is not a clock hour of the day in Larkhaven | guidance 3.2 "counted in the clock hour in which the bus left the stop"; 1.4 times are Central time |
| SF3 | each hour from 6 a.m. to 7 p.m. | the thirteen hours beginning 6:00 a.m. through 6:00 p.m. | fourteen hours including 7 p.m. | same call (every candidate's 7 p.m. hour scheduled below four is off the standard, asserted) | guidance 3.3 "the thirteen clock hours beginning 6:00 a.m. through 6:00 p.m." |
| SF4 | averaged over the counting days | the hour's departures summed over the 125 counting days, divided by 125 | over the days with a record, or a mean of daily minima | same call (every counting day has records; asserted) | guidance 3.3 "the total ... divided by the number of counting days" |
| SF5 | the counting days | weekdays 1 January to 30 June 2026 less the four state holidays (125), Good Friday and the snow day in | Good Friday and the snow day out | same call (asserted) | guidance 3.4 lists the holidays; Good Friday is not one |
| SF6 | departures whether or not tied to the route | an event with no trip is still the departure of whichever route's bus it was | events with no trip are not the route's departures | R1, Routes 4, 22, 11 and 40 | guidance 3.4 "a departure counts whether or not the agency's records tie it to the route" |
| SF7 | meets the standard | the unrounded average at or above 4.0 in every hour | rounded to one decimal first | same call (no candidate's lowest hour within 0.05 of 4.0, asserted) | guidance 3.3 "at least four" |
| SF8 | the cap's order | average weekday boardings in the department's ridership report, January to June 2026 | boardings recomputed or Saturday ridership | same call | guidance 5.1 "as reported in the agency's ridership report" |
| SF9 | the first qualifying route left out | the qualifying route with the next highest boardings after the five | the highest-ridership route that fails | Route 9 (fails the standard) | the prompt asks for the first qualifying route left out |
| SF10 | the cutover evening | 31 March's service from Arbor's export (Quinnell's copy of 7 p.m. onward dropped), or the reverse | both copies kept | same call (outside the counting hours; asserted) | C1: the main population holds none of these events |
| SF11 | Quinnell's repeated file-head rows | dropped (same bus, stop and second as the row before them) | kept | same call (23:50 to midnight, outside the counting hours; asserted) | C1 |
| SF12 | the review's frame | bus-days by service day with at least one event with no trip at the five stops, any hour | counting days and hours only | same call (asserted) | the review memo's procedure |
| SF13 | the stops its outbound trips serve | every stop in the stop_times of the route's direction 0 trips in the spring feed, the first, the last and the designated stop included | the stops after the designated stop only; both directions | the call untouched (an ask term); every candidate's count moves under either | the candidate list's direction ("Outbound, to ...") and the feed's direction_id; every outbound trip of a route serves the same stops (asserted) |
| SF14 | the timetable that began on April 5 | the spring feed (larkhaven_gtfs_20260405.zip) | the winter feed | the call untouched; Routes 2, 17 and 40 move (stops closed in April) | the prompt names the date; the feed's start date is 20260405 |
| SF15 | had no shelter on June 30, 2026 | the shelter standing at the stop on that date: work orders completed by then count, scheduled and cancelled ones do not, and one completed in July is undone where the inspection came after it | the inventory's flag as extracted on July 10 | the call untouched; every count moves under the extracted flag (asserted) | the prompt's date; the work-order log's status and completion dates |
| SF16 | for each candidate | a stop two candidates serve counts for each | each stop counted once across the candidates | the call untouched; five shared stops (the transfer points and College Dr & Pell St) | the ask is per candidate |

## Ladder

- **R0, the timetable (Routes 2, 4, 6, 17 and 9).** The feeds as published, averaged over the counting days, put every
  candidate but Routes 14, 31 and 51 at or above four in every hour (Riverside 4.98); the first qualifying route left out
  is Route 22. Dies to one filed sentence: guidance 3.4 counts departures from the AVL record, and Riverside's afternoon
  runs went short of operators.
- **R1, the links as truth (Routes 4, 22, 11 and 40).** Only four routes reach four from the departures the matchers
  tied to a route; Route 17's lowest hour is 1.5, Route 2's 3.6, Route 6's 2.8. Dies to one filed sentence: guidance
  3.4 counts a departure whether or not the record ties it to the route.
- **R1c, the obvious correction: proportional (Routes 2, 4, 9, 22 and 11).** Sharing each stop-hour's events with no
  trip in proportion to the routes' attributed departures gives Riverside 5.0 (Main St & 9th St's misses are Oak
  Street's late buses, shared to Riverside by its punctual record) and leaves Route 17 at 2.2 and Route 6 at 3.8. Dies
  to one shipped fact: the review finds Riverside in about 6 per cent of Main St & 9th St's events with no trip, not
  the 59 per cent its attributed departures would give it.
- **R2, the sophisticated one: the review's raw mix (Routes 2, 4, 6, 22 and 11).** Sharing by the reviewed events'
  route mix puts Route 17 at 35 per cent of the Transit Mall's misses and its lowest hour at 3.6; Route 2 at 4.3. Dies
  to one construction: each reviewed event is one of its bus-day's unmatched events (1 to 16 of them), so weighting it
  by that count puts Route 17 at 56 per cent.
- **R3, the decisive move: the review weighted by its design (Routes 2, 4, 6, 17 and 22).** Route 17's lowest hour 4.8,
  Route 9's 3.7, Route 6's 4.7, Route 2's 4.8; the first qualifying route left out is Route 11.
- **Bins and margins:** the verdicts are the graded quantities; under every weighted variant (the full weights, the
  within-bus-day weight alone, by month, by vendor, by time band, by stop and clock hour, counting-day reviews only)
  Route 17's lowest hour sits 0.45 or more above four, Route 9's 0.28 or more below, Route 2's 0.33 or more above,
  Route 6's 0.43 or more above; under every unweighted variant (by stop, month, band, stop and clock hour, the stage-1
  factor alone) Route 17 sits 0.41 or more below four (asserted). The review draws 400 bus-days a month, so the
  stop-hour cells hold enough reviewed events that the finest grain agrees with the stop grain. The flip: Route 17
  qualifies once its share of the Transit Mall's events with no trip passes about 43 per cent; the raw review gives 35
  and the weighted 56.
- **Position, separation and dominance:** a slate; each rung names its own five (R0 with Riverside, R1 four routes, R1c
  Riverside and the Connector, R2 the Connector, R3 Prairie Road and Fairgrounds); no two adjacent rungs share a slate.
  Every correction from R1 walks the trunk routes up; R1c walks Riverside up past the line and only the review turns it
  down; only the weights turn Prairie Road up.
- **Worth on the graded quantities:** the eleven verdicts move between rungs on Routes 2, 6, 9 and 17 (R1 four of
  them, R1c three, R2 one, R0 one); the five and the first route left out move on every rung.
- **Grid:** the corrections (count the unattributed; use the review; weight it) taken in order land on R1, R1c or R2,
  R3; weighting the proportional share-out is not defined; the review taken as extra links lands on R1's slate.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | departures in revenue service from the designated stop (guidance 3.2), tied to a trip or not (3.4); out-of-service movements out by the review's finding |
| 2 | Unit of account | the departure; the standard in departures per clock hour |
| 3 | Attribution window | service days 1 January to 30 June 2026; the counting hours carry no event from another service day (asserted) |
| 4 | As-of dating | the exports as delivered (Arbor's of 2 April, Quinnell's of 6 July); the review log closed 31 July |
| 5 | Version basis | one export per system; Quinnell's repeated file heads and its copy of 31 March's evening dropped (C1 on the call); for the shelters the spring feed (SF14), the inventory as last inspected and the work-order log as of 10 July |
| 6 | Denominator | the 125 counting days (guidance 3.3) |
| 7 | Weighting | each reviewed event by its bus-day's events with no trip at the five stops, each month by its bus-days listed over drawn; the within-bus-day weight alone, by month, by vendor, by time band and by stop and clock hour give the same five (C1, asserted) |
| 8 | Window length | the half-year as filed |
| 9 | Boundary inclusivity | an hour from :00:00 to :59:59 by the departure second; "at least four" inclusive (guidance 3.3); the shelter on June 30 counts work completed that day (SF15); the frequency blocks end between two trips, so either reading of an end time gives the same trips |
| 10 | Rounding path | unrounded averages compared with four; no candidate within 0.05 of it (asserted) |
| 11 | Tie-break | none in the ridership order (distinct boardings) |
| 12 | Maturity and censoring | the period closed 30 June; the review covers every month |
| 13 | Order of operations | conform, keep the counting days and hours, share, average, compare, rank |
| 14 | Row order | no dependence (asserted on shuffled files) |
| 15 | Duplicate resolution | Quinnell's file-head repeats (same bus, stop and second) dropped; none in the counting hours (C1) |
| 16 | Identity normalisation | stop ids to stop codes by the feeds' stops.txt; asset tags to fleet numbers by the roster; the review's bus and stop code join both |
| 17 | Netting | none |
| 18 | Dimensional units | departures, hours, local time; Quinnell's UTC converted (guidance 1.4); stops whole |
| 19 | Code and status semantics | MatchStatus and a blank trip both mean no trip; the review's "Not in service" a non-departure |
| 20 | Integerisation | departures whole; averages unrounded |
| 21 | Clause scope | guidance 3 for the standard, 5 for the cap; the review memo describes its own sample only |
| 22 | Forward window contents | none: the program certifies a closed period |

## Literal reader

Executed word for word, the guidance takes each candidate's revenue departures from its designated stop on the 125
counting days, counted in the clock hour each bus left and whether or not the record ties it to the route, and asks
whether each of the thirteen hours from 6 a.m. averaged at least four; the records tie five events in six to a trip,
and the rest are estimated, which the guidance requires without saying how; of the estimates the files support, the
proportional share-out is contradicted by the review's route mix at every stop and the review's raw mix by its own
draw (one event per bus-day, bus-days holding 1 to 16), and the design-weighted review is the one every stratification
agrees on, so the literal execution nominates Routes 2, 4, 6, 17 and 22 with Route 11 the first qualifying route left
out; no filed rule, basis or formula reads to another list. For the shelters, the prompt read literally takes
each candidate's direction 0 trips in the spring feed, every stop they serve, and asks which had no shelter on 30 June
2026: the inventory says what stood where Facilities last inspected each stop, the work-order log what was installed,
moved or taken down since, and the feeds where each stop stands; a stop the spring timetable moved after its inspection
stands away from the inventory's position, so its shelter is whatever a completed work order put at the new position.

## Oracles

- The review memo's monthly tally (bus-days listed, drawn and reviewed; findings by kind): counts, true under every
  handling; it states no route share.
- The ridership report: filed boardings, used as filed for the cap; no figure in it depends on the AVL estimate.
- The GTFS feeds: the timetable rung (R0) reads them; nothing in them ties to delivered departures.
- The farebox workbook and the Title VI report (distractors): revenue by route and 2025 equity classifications, with
  no departure counts; no figure ties under any reading.
- The Title VI report's "stops with shelter" (2025, every stop of each route in both directions, as a percentage): a
  different year, scope and unit; it ties under no reading of the shelter ask.
- The work-order log's statuses and dates: true under every handling; the log states no count of stops without a
  shelter, and no file does.
- None ties only under the golden.

## Ask sheet

- **The shelter ask: for each candidate, how many of the stops its outbound trips serve in the timetable that began on
  April 5 had no shelter on June 30, 2026 (whole stops; 11 figures).** H18 home: a measure every candidate carries that
  the call does not turn on; the program funds stop and shelter work on the routes nominated (guidance 1.1), and each
  candidate's unsheltered stops are the scope of that work. Use: the Transportation Committee reads each route's shelter
  gap beside its verdict before the council signs. Path: the spring feed (stops.txt with positions, trips.txt with
  direction_id, stop_times.txt), the winter feed's stops.txt, Facilities' amenity inventory (stop_code, location,
  latitude, longitude, shelter, last_inspected), Capital Projects' work orders (stop code, work, status, completed), the
  candidate list: five files, sixteen columns.
  Primary device: D7 with D4, the true key elsewhere and absence as the signal. The spring timetable moved stops on
  every route to the far side of their intersections (58 to 112 metres) and kept each stop's code and name; Facilities
  inspects each stop about once a year, so the inventory still holds 32 moved stops where they stood before April, with
  the shelter that stood there. A shelter moves only under a Capital Projects work order; where none was completed by
  June 30 the shelter stayed on the old pad and the stop at its new position had none. Joined on stop code, every
  inventory row matches its stop, every name agrees, nothing repeats, and the work orders carry the inventory forward
  correctly, so no sweep sees it; it shows only at a cross-file cut nothing invites, the inventory's position against
  the spring feed's (or the winter feed's position against the spring feed's for the same code). Every candidate holds
  one to three such stops (asserted). Benign twins: 13 moved stops whose row reads right (re-inspected after the move,
  relocated by a completed work order, or never sheltered), and every other stop within 11 metres of the feed (the
  inspectors' GPS).
  Hazards: work orders scheduled or cancelled; seven completed in July, after the date asked: five relocations at moved
  stops and two new shelters at stops Facilities inspected a few days later, whose rows record a shelter that was not
  there on June 30; stops the spring timetable closed (still in the inventory, out of
  service); the inventory's posted routes column (the routes on the sign at inspection, both directions); the Title VI
  report's 2025 shelter percentages.
  Stops (asserted, checks.py and generator/ceiling.py): the inventory carried forward and back by the work orders, joined
  on stop code (the cracker) misses all 11 (Route 2 13 against 15, Route 4 14 against 16, Route 6 6 against 8, Route 9
  4 against 6, Route 11 7 against 9, Route 14 8 against 10, Route 17 10 against 13, Route 22 6 against 8, Route 31 5
  against 7, Route 40 10 against 12, Route 51 12 against 13); the inventory as extracted misses all 11; the inventory
  rows whose posted routes include the candidate miss all 11; the golden equals the stops' true shelters on June 30.
  Fair: the moved stops are exactly those standing more than 30 metres from their inventory position (at least 60
  metres; every other stop within 11), and exactly those the spring feed moved before their inspection was due (C1,
  asserted). Realism: a far-side stop programme carried out with a timetable change, a facilities inventory refreshed on
  an annual inspection cycle, and shelters on concrete pads that only a contractor moves.
- **The construction layer:** the call, the eleven verdicts, the five and the first route left out; the cracker has
  them.
- **Main population zero-counts (asserted):** the call reads the counting-day events from 6 a.m. to 7 p.m. (departure
  time, stop, bus, trip, route, match status), the review log and the ridership report's period averages, and no stop
  position, shelter or work order; the distractor copy test deletes the inventory's and the log's rows from nothing the
  call reads, and the separation check blanks every schedule field with the same five. The device lives only in the
  feeds' stop positions, the inventory and the work-order log.
- **Hazard table (asserted):** the extracted flag moves all 11 counts; the posted-routes column moves all 11; the two
  July shelters move Routes 4 and 22 under the extracted flag and nothing once the work orders are carried back.
- **Referee:** the winter feed's position for the same stop code, which agrees with the inventory's for every stop the
  spring timetable moved before its inspection: split evidence that the stop moved, never a count.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| Stops without a shelter by candidate | joins the spring feed's outbound stops to the inventory on stop code (every code matches, every name agrees), carries each flag forward by the work orders completed after the inspection and back by those completed after June 30: 0 of 11 | miss |

- Mirror leakage: 0.0 per cent of ask weight (the mirror on R2 scores the best of the cracker's path, the extracted
  flag and the posted routes, 0 of 11).
- Pair ceiling: 36.5 (planning weights 38 / 7 / 55, the main block split as the call 10, the five 8, the first route
  left out 4 and the eleven verdicts 16, the ask weight over the eleven counts; the cracker 45.0 with 0 of 11, the
  mirror on R2 27.9 with ten verdicts, four of the five, instruction-following and 0 of 11).
- Measured by: generator/ceiling.py on the cut pack (cracker 45.0, mirror 27.9, pair ceiling 36.5, mirror leakage 0.0
  per cent).

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method (it survives as Ask C's device, which the 10/10 rules leave free).
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
- 2026-10-17, stage 2: the review as a simple random sample of the unmatched events, its raw route mix the decisive
  step: a single insight the review file signposts (133 v1 died on a development sample pointing at its decisive
  step); the review is now a bus-day sample with one event each, so using it is R2 and weighting it is the move.
- 2026-10-17, stage 2: the composition varying by time band (trunk routes late in the afternoon only, pull-in deadheads
  at night): pooled and band-level shares gave different calls on Route 17, a grain fork (H14); lateness now flat
  through the day and out-of-service movements spread over it, so every stratification agrees.
- 2026-10-17, stage 2: Riverside failing on a four-an-hour timetable: Good Friday's Saturday service pulled its
  timetable average under four too, so the timetable rung landed on the golden; Riverside now runs five an hour and
  its afternoon runs went a quarter short of operators.
- 2026-10-17, stage 2: each candidate's lowest hourly average graded to one decimal: the weighted variants spread up
  to 0.3 on Route 2, so the prompt asks for the verdicts and the workbook carries the figures as supporting detail.
- 2026-10-17, stage 3: on-time shares to one decimal of a per cent: two routes' shares sat within a hundredth of a
  rounding edge, so the shares are graded to the whole per cent (every share further from its edge than one departure
  moves it, asserted); Hillcrest's lateness and timetable jitter moved so its share and its wait sit clear of their edges.
- 2026-10-17, stage 2: a scheduled-departures table from both feeds as an ask: a GTFS-literate cracker executes the
  calendar, calendar_dates and frequencies correctly, so no device held; replaced by the waits (an analytical device).
- 2026-10-17, stage 4: Ask A, Quinnell's April to June record by stop and service-day month: both outside readers
  found the file-head repeats by bus, stop and second and assigned the service days, the judge read the repeats as a
  fork, and no silent device reaches the record without touching the review's frame; dropped (the repeats, the 31
  March copy and the after-midnight service stay as Layer 1 on the call's path, asserted neutral).
- 2026-10-17, stage 4: Ask C, the scheduled wait on 13 May: the prompt's definition made the waiting-time paradox a
  literal integral both readers computed, the frequency window's end read two ways, and no representation of the feed
  hides a departure from a careful reader; dropped (the frequency trips now exact times, each block ending between
  two trips).
- 2026-10-17, stage 4: the on-time device as Quinnell's DeviationSec taken at arrival: both readers timed the
  departures from the timestamps and read the field as noise, and guidance 4.2's "as the AVL system records it"
  invited it; DeviationSec is now the departure against ScheduledDeparture, and the device is Arbor's minute-held
  schedule against the feeds' half minute.
- 2026-10-17, stage 4: Route 6's on-time share at 47.46, 0.04 from its edge (a reader rounding to one decimal first
  filed 48): the half-minute bands, set per transfer point, put every share at least 0.19 from its edge.
- 2026-10-17, stage 4: the eleven candidates named only by route colour in routes.txt (the judge's Gate B and E
  finding): Planning's candidate list now ships with each route's designated stop.
- 2026-10-17, stage 4: the on-time device as Arbor's minute-held schedule against the feeds' half minute: judge pass 2
  read the two schedule sources as an open fork (FIX_NOW), the pin naming the published timetable in guidance 4.1 and
  4.2 closed it, and reader round 3 then timed all eleven shares against the feeds. A device whose basis a filed
  sentence must name dies with the pin, and every other column the ask reads (the departure, the trip tie, the window,
  the days) is the call's own population, so no device on this ask can stay off the call's rows.
- 2026-10-19, repair: the stop-hour grain fork (reader round 3): the review drew 250 bus-days a month, so the
  stop-by-clock-hour cells held one to seven reviewed events and the minimum of thirteen noisy hourly estimates sat
  biased low; at 400 bus-days a month, with the within-bus-day draw on its own stream, every weighted grain (stop, stop
  and hour, band, month, vendor, the within-bus-day weight, counting-day reviews) files the golden and every raw grain
  the R2 slate (checks.py R3b, verify.py's stop-hour estimator).
- 2026-10-19, repair: replacing the dead on-time ask, measures tried on paper and dropped: the average scheduled wait
  (computed exactly from the feeds by any GTFS-literate solver, and "a weekday of current service" splits on the class
  days); missed trips from a dispatch log (it would hand every solver each route's delivered departures, the call's own
  quantity); APC boardings at the designated stops (doors open only in service, which would identify the out-of-service
  passes the review estimates); the fleet roster's asset tags moved between buses (it would move the review's bus-day
  join on the call's path); evening and Saturday counts (Quinnell's repeats and the cutover overlap are seen, not
  silent). The shelter ask takes none of the call's rows.

## Leak check

- `leak.py --asof 2026-10-30`: REVIEW, no LEAK. Sweep 3: the guidance carries the program's name, which the call's
  sentence repeats; not an answer. Sweep 4: the guidance, the change note and the memo use the program's and the
  matching review's own words (review, sample, bus-day, timetable); the memo states how its sample is drawn and nothing
  about weighting (R1). Sweep 6: the ridership report is the cap's filed order (guidance 5.1), the farebox workbook
  and the Title VI report are the declared distractors, the candidate list runs in route-number order. Sweep 7: the
  two GTFS feeds, zipped as an agency publishes them.
- Reader round 1 (an isolated copy of prompt.txt and target/, one sonnet thread at medium): no sentence names the
  decisive step (the pieces sit in guidance 3.4 and the memo's procedure), no file ranks the candidates on the
  standard, no file exists only to help, no figure reads as the answer, every question-5 sentence executes to the
  golden (the trip-tied-only reading is R1, ruled out by 3.4), and the decisive step is an analytical choice. It filed
  the golden five, and on the old asks the on-time shares from the timestamps and the waits from the integral.
  Fixed in the generator: the eleven candidates unnamed (the candidate list ships); DeviationSec unrelated to the
  timestamps (now the departure against ScheduledDeparture); the folder list saved on 30 October (now 3 August, after
  the last paper); every bus with CCTV (the column is gone, and bus lengths vary); one reviewer on 1,500 rows and an
  empty "early beyond window" column (three analysts; the column is gone); route 11's explicit schedule times beside
  frequencies.txt (exact_times 1, each block ending between two trips). Harmless: Good Friday and the snow day as
  counting days (the guidance's literal reading, SF5); Arbor's one-decimal adherence (the device's lazy path).
- Reader round 2 (the rebuilt pack, the same brief): nothing quoted for question 1, no ranking file, no answer-like
  figure, the question-5 sentences executing to the golden's estimand, the decisive step "an estimand and sampling
  choice, not a field reading or a planted item". It filed the golden five and timed the on-time shares against the
  exports' own adherence fields: every share in a different whole per cent from the golden's (the device held on all
  eleven). Fixed: the folder list read as a build artefact (question 3), so it no longer ships; its dates stay as each
  file's saved date. Harmless: the file-head repeats and the cutover overlap (outside the window, explained by the
  daily files), the review's 250 a month (the memo's design), route 11's ten-minute headway, stop-by-hour shares
  (Route 17 still qualifies).
- Reader round 3 (the pinned pack, target.zip 2c828983, the same brief): question 1 quotes guidance 3.4 and 5.2 and
  the memo's procedure and finds nothing saying to weight; no ranking file, no helper file, no answer-like figure; the
  question-5 sentences execute to the golden's estimand; the decisive step "estimand and estimator choice, not
  semantics". It filed the golden five and all eleven on-time shares, timing against the feeds as guidance 4.1 and 4.2
  now name them: the ask's device died with the pin (Ask sheet, Tried and rejected). Open finding on the call, an H14
  grain fork: the review's weighted mix applied per stop and clock hour (thin cells, Stop D holding one to seven
  reviewed events an hour) files Routes 4, 6, 22, 11 and 40, Route 2 at 3.94 and Route 17 at 3.86; per stop over the
  half year (the golden), per stop and time band and per stop and month all give Routes 2, 4, 6, 17 and 22. Harmless:
  Arbor's minute-held schedule and route 11's trip ids (the Layer 1 the ask reads), the night-time file-head repeats
  (outside the window), Route 17's stark numbers (its late buses are the story).

## Pre-ship check

- **Three rules, re-read against the rebuilt pack.** Domain: the deciding quantity is each candidate's departures per
  hour estimated from a linked record whose missed links select, the field's estimator being the clerical review's
  measure of the missed links' route mix weighted by the review's own design; the links as truth file Routes 4, 22, 11
  and 40, the proportional share-out Routes 2, 4, 9, 22 and 11, the review's raw mix Routes 2, 4, 6, 22 and 11, and the
  design-weighted review Routes 2, 4, 6, 17 and 22, on the clean truth and on the pack (checks.py R3a, R3b). Two
  layers: the Layer 1 inventory in `## Three rules`, each asserted neutral for the call (R2: the repeated file heads
  kept, both copies of 31 March's evening, Quinnell's copy instead of Arbor's, calendar dates for service days, all the
  same five; the separation check: every schedule field blanked, the same five); the shelter device confined to the
  stops' positions, the amenity inventory and the work-order log; Layer 2 the weighting. The decisive step is none of the three banned kinds,
  each executed in `checks.py`: not a plant (R1, R3c); not data semantics (SF1 to SF16: every term read right still
  leaves the raw mix on Routes 2, 4, 6, 22 and 11); not rule application (R3a, R3b).
- **Judge pass 1** (2026-10-17, `determinism_check_report.md`): NOT_DETERMINISTIC on the asks only, SEND_BACK in the
  judge's sense (a fix that changes what solvers see); the call forced and reproduced (Route 17 at 4.81 weighted, 3.56
  raw; the seven qualifiers and the five under every allocation it tried); Gate F good; Gate G statistical_rigor,
  analytical_non_defect, no surface read, no sole defect; Gate H domain pass, layers pass, decisive step analytical.
  The four ask-side findings closed in the generator: the candidate list; the record ask dropped; the on-time basis
  (the trip's scheduled departure, bounds included, DeviationSec coherent); the waits ask dropped.
- **Judge pass 2** (the one re-judge, `determinism_check_report_pass2.md`): DETERMINISTIC, FIX_NOW. Every figure
  reproduced from the bundle (125 days, 106,687 departures, 17,112 without a trip, Route 17 at 57 per cent weighted and
  35 unweighted, its lowest hour 4.81, the seven qualifiers, the five and Route 11, all eleven on-time shares against
  the feeds); a bootstrap of the review keeps every qualifier at or above four (Route 17's low end 4.56); Gate G
  statistical_rigor, analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical. The one finding:
  only the write-up named the feeds as the on-time basis, and Arbor's minute-held schedule moves every share. Closed at
  authority rather than in the prompt (which carries the question and no convention): guidance 4.1 now has the
  application carry "the GTFS feeds of its published timetable" and 4.2 times each departure against "the trip's
  scheduled departure in the published timetable" (SF15, asserted). The pin was taken to leave the device silent for a
  solver who trusts the export's schedule; reader round 3 timed every share against the feeds instead, so it does not
  (Ask sheet). The judged bundle and the pinned one differ in that sentence and in the folder list's removal; no third
  judge (the pipeline licenses one re-judge).
- **Gates.** 13 files in 4 formats (csv, pdf, xlsx, zip); avl_stop_events_2026q2_quinnell.csv at 83,843 rows; two
  distractors (the farebox workbook and the Title VI report) the solution never reads, each deletion asserted; 53
  generator checks; `verify.py` from the bundle alone (its own readers for the exports, the feeds, the candidate list
  and the workbooks, its own conformance, weights, estimate and on-time shares against the feeds); two builds
  byte-identical; `figures_check.py` (48 figures), `precut.py` and `voice-check.py` exit 0; `leak.py` REVIEW (no
  LEAK); guard heart WARN (answered in the draw); the surface screen's three promotions are card-level and go to the
  author; the containers clean (H1 audit, pack and golden); the golden workbook prints on one landscape page with the
  chart under the table.
- **Paused at stage 4** (2026-10-17), not shipped. Reader round 3 left two findings the gates cannot pass: the on-time
  ask's device died with the guidance pin (a cracker on the pinned text hits all eleven shares, pair ceiling 91.5
  against the bar of 40), and the call carries an H14 grain fork at the stop-hour grain (Routes 4, 6, 22, 11 and 40).
  The repair order is in pipeline.json: the review's draw first (each sampled bus-day's reviewed event drawn so every
  stop-hour's weighted mix tracks its stop's, the raw mix still failing Route 17 at every grain, the stop-hour
  estimator asserted in checks.py and verify.py), then a new ask on a measure the call does not read, carrying a
  device a GTFS-literate cracker misses.
