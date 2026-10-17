# task468 design note: Larkhaven's frequent corridor nominations

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json` (architecture v1), registered 2026-10-17 after a pull, so
  every card filed before it was in the check. Guard check WARN only, each answered here: identity_resolution as the
  strategy (no field resolves an unmatched departure's route; the review sample measures the routes only in aggregate,
  so the step is error propagation, not a reading); the data-integration pattern already carried by task449 (false
  links diluting a share among k equally plausible targets) and task454 (imputation within a known stratum), where here
  missed links select; Gate G method_or_model_selection repeats task239 and is in six of the last twelve (it is the
  honest key: proportional allocation and allocation by the reviewed shares, the second pinned by the review sample);
  the question form "which" repeats task239 and task158 and comes from the decision, a slate of routes. Differentiated
  against task116 v3 and task454 on the card.
- **Seed:** ET25 (a transit agency brands routes Frequent Network, and qualifies them for a state capital grant, when
  they meet a service standard on weekdays; a GTFS checker certified a 30-minute route and rejected a frequency-based
  10-minute one). Kept: the world (a transit agency, its GTFS feed, a state capital program), the decision (which
  routes qualify and are nominated) and the quantity (each route's frequency in every hour of the weekday span).
  Dropped: the seed's mechanisms (service days, times past 24:00, frequency-based trips), which are data semantics;
  they survive as Layer 1 and as the ask's devices.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL, client
  pattern 1 (propagate linkage error to the estimate: false links attenuate, missed links select; shortcut, links above
  a cutoff as truth). The state counts delivered departures, and the department's only record of them is the AVL
  vendor's stop events, which reach a route only through the vendor's trip matcher; the conformed evidence is a
  linked dataset, and the deciding counts are estimates from it. GSDS is a methods domain, so the swap is of the
  method: replacing the propagation of the matcher's error (the reviewed sample's shares) with its links taken as
  truth, or with a share-out in proportion to the links, moves the nominations.
- **Shape:** 01, a ranked list under a cap: each of the eleven candidate routes passes or fails the delivered
  standard, and the state takes at most five per agency, the highest in average weekday ridership first; the criteria
  are each route's verdict and place, the five, the first route below the line, plus the asks.
- **Strategy:** identity_resolution (linking records to the units they belong to), decisive generator G6 (the
  unmatched departures' route mix is not the matched mix), with G12 (no route on a record is not no departure) and G3
  (the AVL record against the bus that ran).
- **World:** the United States, an unnamed Midwestern state. The City of Larkhaven runs Larkhaven Transit as a city
  department (about 60 peak buses, 24 routes). The state Department of Transportation's Frequent Transit Corridors
  Program funds stop, shelter and signal-priority work on routes that delivered frequent service; for the FY2027 round
  an agency nominates at most five routes, each of which must have averaged at least four departures an hour from its
  designated stop in every hour from 6 a.m. to 7 p.m. on weekdays (state holidays excluded) from January to June 2026,
  counted from the agency's automatic vehicle location records; an agency with more qualifying routes nominates those
  with the highest average weekday ridership. Larkhaven's AVL vendor changed on 1 April 2026 (a new CAD/AVL system,
  its export in UTC); both vendors run a trip matcher that ties each stop event to a scheduled trip when the bus is
  within its window of the timetable, and leaves the event's trip and route blank otherwise. The department's
  Service Quality unit reviews a random sample of the unmatched events each month and records the route each belonged
  to.
- **Forcing fact:** the state's application closes on 1 December 2026; the City Council authorizes the nominations by
  resolution at its 17 November 2026 meeting, and the service planning manager's workbook goes to the council's
  Transportation Committee first. As-of: 30 October 2026. The call is retrospective by the program's own design (it
  certifies service delivered in a closed period) and faces forward in what it funds (FY2027 work on the five routes).
- **Forum and forcing event:** council_or_assembly (Larkhaven City Council), vote_or_meeting (the authorizing
  resolution). Organisation local_government; role programme_officer. Personas from `guard.py names --geo "United
  States" --seed 468`: Wendy James (Manager, Service Planning and Grants, who prepares the nominations), Eric Thomas
  (ITS systems administrator, who signs the AVL vendor's change notes) and Alfred Hensley (Service Quality analyst,
  who runs the trip-matching review; Diane Beck replaced, her first name in task105).
- **Data-native sentence:** the matcher ties a stop event to a scheduled trip only when the bus is within its window
  of the timetable, and the buses outside it are the late ones in the afternoon and evening peaks on the trunk routes
  that share the downtown stops, so the events left without a route are not a sample of the routes' departures but
  mostly the trunk routes'.
- **The WHAT screen.** Population: departures by buses of the route in revenue service from its designated stop, on
  weekdays January to June 2026, state holidays out (the state's guidance). Outcome: the average number of such
  departures in each clock hour from 6 a.m. to 7 p.m. Window: the first half of 2026. Unit: departures. Comparison:
  four an hour in every hour, then the five-route cap by ridership. The decisive step settles none of them: it is how
  the departures of a route are counted from records a third of which, in the binding hours, carry no route, and the
  data's structure (the reviewed sample's route mix differs from the matched mix) rules out the two easy counts.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution 1: the
    client's own pattern for the task type; here the missed links select by lateness and the clerical review is the
    department's routine trip-matching audit.
  - `dataset-generation/references/layer1-messiness.md`: two vendor exports, UTC against local time, repeated events at
    file boundaries, renumbered stops, GTFS frequency-based trips, times past 24:00, a school-day service; none on
    the decisive step, each to be asserted neutral.

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method.
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
