# task487 design note: an upstream oil producer's 2026 release-event methane for the province's release-event levy, each event found at a lease operator's visit split between the share the previous visit started and the share that arose between visits (architecture 1)

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-26. The slot's seed (ET44,
an online wholesaler's loyalty tiers from a net-spend distribution) was read for its header and situation only: once its
decoy-era mechanism is set aside the world carries no quantity the field estimates (a tier cut of a spend distribution
is a sort, and the seed's steps are semantics), so the first draw is made in the emissions-inventory cell on what the
seed's quantity shares with this one, a total built from records whose own durations are not recorded. The candidates
screened before this draw are in the last section, Tried and rejected.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task487.json` (architecture v1), registered 2026-10-26T13:07:47Z and
  checked again after filing: PASS, one NOTE (driver similarity 0.16 against task476 v2, differentiated on the card).
  The window the axis bans read at filing (task485 v4, task121 v5 and task308 v1, the live cards filed last; task270
  v5, task137 v2, task486 v3 and task269 v4 are spent and skipped) closes the pairing survey-research-official-
  statistics / etl and the subdomain census-register-administrative-data-quality, the strategies maturity_censoring,
  causal_design and binding_constraint, the shapes 18 and other, the forums minister_or_cabinet, committee_or_panel and
  board_of_directors, the forcing events vote_or_meeting, other and budget_or_appropriation, the organisations
  research_or_statistics_office, government_agency and financial_institution, the roles statistical_office_head,
  compliance_or_audit and portfolio_manager, the artifacts published_series, monitoring_export and filed_standard and
  the generators G9, G4 and G14. The draw's honest labels clear all of them: the operator files its 2026 release events
  with the provincial regulator (regulator_or_inspector, statutory_or_regulatory_filing), the requester is the area
  production superintendent who signs the filing (field_unit_lead), the stakeholder's own file is the lease operators'
  visit log (operations_log), and the organisation is an upstream oil producer (other: no vocabulary key fits and
  utility_or_infrastructure would be untrue).
- **Labels redrawn at the draw, and why the filed ones are the honester:** the first draft carried G3 decisive (record
  against operation: the previous visit did it) with Gate G method_or_model_selection, and BLOCKed on
  `test.same_puzzle_older` (task126, task138, task82) and `test.same_driver_older` (task126, task275, task450 v1, task468
  v4, task469); with G7 decisive and method_or_model_selection it BLOCKed on `test.same_driver` against task308's
  lineage inside the batch. What carries the stump is a split of correctly recorded events between two drivers (the
  previous visit, and the hours since), which is `decomposition_attribution`, and what fixes when the started share
  began is the visit log's departure times, an operations file pinning when the event could have begun (G7), with the
  record-against-operation reading (G3) second. The gap is population (Gap 2, the file is not the thing): the event
  log's windows stand in for active hours they are not.
- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The deliverable is the conformed 2026 release-event inventory in the regulator's event schema, one row per
  event, built from two lease operator apps (a mid-year migration), the operator's event register, the SCADA tank
  pressure alarm journal, daily production, the batteries' tank vapour analyses and the battery register.
- **The world and the decision.** A fictional western Canadian province's energy board (the Provincial Energy Board)
  levies upstream operators on the methane their release events vent (an open thief hatch, a combustor whose pilot is
  out, a tank relief valve that has not reseated), assessed each year on the previous calendar year's events and banded
  by the operator's total tonnes (Directive 17, Table 1: under 36 t, 36 to under 48, 48 to under 60, 60 to under 72,
  72 and over), each band carrying a levy rate for each battery held (CAD 330 to 2,000). Vennholt Energy
  runs 180 tank batteries in its Kesmere field on twelve lease operator routes: most batteries are visited once a
  weekday, two routes also on Saturdays, high producers twice a weekday and low producers on Mondays, Wednesdays and
  Fridays, with spring road bans and holidays, so the window between one visit's departure and the next arrival runs
  from a couple of hours to most of a week. Every visit gauges the tanks through the thief hatch and checks the
  combustor, and every event present at an arrival is found then and closed on site; at the 40 per cent of batteries
  with tank pressure telemetry a relief valve that lifts and does not reseat raises an alarm and is timed exactly.
- **Timing (the pack's present is mid-January 2027).** The 2026 records are complete; the return is due 31 March 2027
  and its band fixes the 2027 levy. The quantity is retrospective by construction (a closed
  year's events) and the call it fixes is forward: what the operator budgets and staffs in 2027.
- **Shape:** `15`, fields to one schema: the Board's event schema for every release event found in 2026, each field
  from its source by its transform (the battery and licence from the register, the kind from the register's text, the
  start from the alarm or as the expected start given the visit window, the find and the closure in local time, the
  active hours and the methane from production and the vapour analyses), with the year's methane, its band and the
  levy, and Schedule B's fugitive methane for each route in each half of 2026 (24 figures) as the asks. A bridge from
  the methane the records date to the return's was dropped at stage 4 (its items by kind move with the estimator while
  the band does not, the round 1 judge), as a bridge by route was at stage 2 (stumping 1.1j).
- **Guard:** `repeat.gate_g` WARN against task121 v6 (retired): that build attributes a rise in under-triaged calls to
  rest before shifts; this one decomposes an event's active hours into a visit-started share and an hourly share, and
  only the label is shared.
- **The default path holds the field's practice (stumping 1.1b).** An inventory that cannot date an event's start takes
  the midpoint of the window since the equipment was last known good, or the conservative last-known-good start; the
  alarm-timed relief valves, whose starts sit across their windows (mean position 0.43 over 54 events), confirm the
  midpoint to a careful analyst. The golden is the decomposition the data force: the chance that a window ends in an
  open hatch is a share the departing visit starts (0.85 per cent of departures) plus a rate an hour between visits
  (0.066 per cent), and each hatch's expected start follows from its window.
- **Measured on the cut pack (zip e59b21a9, `checks.py`):** the clean truth's own starts give 54.94 t; the golden
  54.54 t (band C); every undated start mid-window 45.18 t (band B); every undated start at the previous departure
  87.46 t (band E); hatches at the departure and the rest mid-window 82.69 t (band E); hatches a quarter into their
  windows 63.96 t (band D). The standing family files band C at 53.86 to 56.98 t: the share fitted per route 55.13, per
  visit schedule 55.27, per battery 56.76, a Weibull chance 53.86, the isotonic fit 56.98, a straight line 55.55. Twice
  the log-likelihood gain of the hatch share over none is 96.1; pilots 0.5 and relief valves 3.3, which no visit starts.
- **Data-native sentence:** the lease operators found 24.2 open hatches in every thousand windows after a weekday window
  and 51.7 after a weekend one, 2.1 times as many for 3.0 times the hours, while relief valves rose 2.8 times, because a
  share of the hatches were left open by the visit before and vented the whole window, and the relief valves the alarms
  time exactly arose evenly in the hours between and so sit like a midpoint.
- **People** (drawn with `guard.py names --geo canada --seed 487`): Rhonda Wheeler (area production superintendent, the
  requester), Charlene Logan (regulatory analyst, the return workbook's author). Lease operators and control room staff
  appear only by their system user IDs.

## Default path

The route a competent compiler builds first, with every field read correctly and every filed rule applied.

1. Conform the route app (local wall clock, to 30 June) and the check-in app (local time with its UTC offset, from 1 July and from
   15 June on R03 and R09) into one visit timeline per battery, the check-in app's geofence re-entries and the June visits in
   both apps taken once, BT-0907 carried to BT-0907A.
2. Join each register event found in 2026 to the visit that found it, its window from the previous visit's departure.
3. Start each relief valve that did not reseat at a telemetered battery at its alarm in the SCADA journal; seeing those
   starts spread across their windows, start every other event halfway through its window.
4. Price each hour at the battery's tank vapour methane that day (directive s.3.3), sum, and read the band.

Ends on: band B, 45.2 t of release-event methane, a 2027 levy of CAD 115,200.
Golden: band C, 54.5 t of release-event methane, a 2027 levy of CAD 171,000.

## Stump sentence

The default path starts every event the records do not date halfway through its window, which the alarm-timed relief
valves appear to confirm, and files band B at 45.2 t for a 2027 levy of CAD 115,200; the step that lands it there is
pricing the open thief hatches at half their windows when 0.85 per cent of departing visits leave a hatch open that
vents the whole window (twice the log-likelihood gain 96.1), read from hatches rising only 2.1 times from a weekday
window to a weekend one for 3.0 times the hours; the hatches' expected starts given their windows put the return at
54.5 t, band C, CAD 171,000.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences), tagged in the taxonomy for Data Extraction & Conformation (ETL): the conformed event-level release inventory the regulator's schema requires, from two lease operator apps, the event register, the alarm journal, production and vapour analyses.
Domain test: The deciding quantity is the operator's 2026 vented methane from release events, each event's tank vapour rate (flash vapour from the battery's oil throughput and vapour analysis) over its active hours, where the active hours of an event a lease operator finds at a visit are split between the share the previous visit starts and the share that arises between visits, read from how often each kind of event is found against the window's length.
Swap: put a ward's fall rounds in for the lease operators' visits and the gauging that opens a thief hatch, the flash vapour that leaves through it, the knockout drain that drowns a combustor pilot and the relief valve the tank pressure alarm watches stop making sense, and with them the vapour rate each hour is priced at.
Layer 1: the route app's local wall-clock times to 30 June against the check-in app's times with their UTC offset from 1 July (the register's times in each app's format); check-in app geofence re-entries splitting one visit in two; routes R03 and R09 logged in both apps from 15 June; BT-0907 re-licensed as BT-0907A on 17 August with its earlier records under the old code; the register naming each kind several ways; the SCADA journal in UTC with the RTU's own stamp in each message; production in cubic metres against analyses in mole per cent. Each is produced by the operator's ordinary systems and none is placed to be caught; each mishandled leaves band C (`checks.py` R2, 53.61 to 54.67 t).
Layer 2: estimation_fit: an event's start inside an observation window that the inspecting visit itself opens, so the window's placement carries information about the start and the even-spread (or uninformative interval-censored) placement is misspecified; the share started by the visit is identified by incidence against window length.
Decisive step: splitting each kind's events found at visits into a per-visit part, started as the previous visit left, and a per-hour part arising evenly between visits, from how often each kind is found against the length of the window since the previous departure, and running each found event's expected hours from that split.
Not semantics: every field reads as what it is (departures, arrivals, finds, closures, alarms); no code, note or column marks an event's cause or start, every visit gauges and checks the combustor alike, and an analyst who conforms every file exactly still files band B by spreading each start evenly through its window.
Not rule application: the directive files the WHAT (each event's methane from its start to its closure, the start at its expected value given the licensee's records where they do not date it) and nothing about how a start is placed; the enumerated family (mid-window, the alarm-confirmed mid-window, the previous departure, hatches at the departure, hatches a quarter in) spreads across bands B, C, D and E (45.18 to 87.46 t), the standing family (the share fitted pooled, per route, per schedule, per battery, as a Weibull chance, an isotonic fit or a straight line) spreads 53.86 to 56.98 t inside band C, and what rules the rest out is a fitted per-visit share (twice the log-likelihood gain 96.1 for hatches) that no table shows until incidence is set against window length.
Analyst test: A strong analyst conforms both apps, joins every find to the previous departure, prices each event at the battery's vapour rate, starts it halfway back (the alarm-timed relief valves sit across their windows) and files band B, 45.2 t, where the golden is band C at 54.5 t.
Estimand: each 2026 release event's vented methane from its start to its closure, its start where the records do not date it taken at its expected value given the licensee's records, summed over the events found in 2026 and banded by the directive's Table 1 (`peb_directive_17_release_event_return_2025.pdf`, sections 3 and 4).
No decoy: nothing is planted: the visit logs, the event register, the alarm journal, production and analyses are the operator's ordinary records; no memo, draft, prior return or stakeholder figure argues for a band or a placement, and the alarm journal ships because the alarm-timed events' own hours are in the inventory.
No certified replay: no certified or published figure sits in the pack to be reproduced, and no method is recovered from one.
Lesson: an inspection that can start the events it later finds leaves those events running for their whole windows, so the found events' active time is longer than half their windows by a share that falls as the windows lengthen; the share is read from how incidence grows with the window, and an exactly timed record of a kind the inspection cannot start confirms the even spread it misprices. No build on file reads an inspection-started share from incidence against window length (nearest driver 0.16, task476 v2, a seasonal start profile from a second record).

## Readability screen

Measured by the generator on the cut pack (`checks.py` restates every figure on each build). Release-event methane by
rung, tonnes: the golden 54.54 against mid-window 45.18, the previous departure 87.46, hatches at the departure 82.69,
hatches a quarter in 63.96.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 mid-window (default) | every undated start halfway between the previous departure and the find's arrival | directive s.3.2 read as an even spread; the alarm-timed relief valves sit across their windows (mean position 0.43) | readable |
| L1 last known good | every undated start at the previous departure | the field's conservative practice for an undated event; nothing in the directive asks for it | readable |
| L2 hatches by the gauger | open hatches at the previous departure, the rest mid-window | the gauging every visit does through the thief hatch | readable |
| L3 a guessed share | hatches a quarter (or a half) of the way in, the rest mid-window | nothing: a split taken without a fit | readable |
| G golden (decisive) | each kind's chance that a window ends in an event fitted as a share the departing visit starts plus a rate an hour, each start at its expected value given its window | nothing labels a visit-started event: the share shows only when finds are set against the window's length, and the only exactly timed events are a kind no visit starts | silent |

The one-group-by route to the golden, written before the first harness (stumping 1.1): finds per window by kind and
window band, a line through them, its intercept as the visit's share. It reaches band C (the straight-line member,
55.55 t) only after the reader has asked whether finds grow with the hours; the group-by is cheap and the question is
the step.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | found in 2026 | the register's find in the calendar year, local time | the find's UTC date | same call (0 events differ; asserted) | directive s.3.1, s.3.3 (calendar days in local time) |
| SF2 | the window | from the previous visit's departure to the find's arrival | from the previous arrival | same call (54.87 t; asserted) | the visit's own departure is when the battery was last left |
| SF3 | a visit | a check-in app geofence exit and re-entry within ten minutes is one visit | every check-in a visit | same call (53.61 t; asserted) | same call |
| SF4 | a stuck valve's start | the first alarm of the last lift before its find | the burst's last alarm | same call (54.54 t; asserted) | directive s.3.2 (the alarm at which it lifted) |
| SF5 | the expected start | the start at its expected value, its methane from there | the methane's expected value over the start's spread | same call (54.33 t; asserted) | directive s.3.2 |
| SF6 | the fit's windows | pilots on combustor batteries, relief valves on untelemetered ones | every battery for each kind | same call (54.28 t; asserted) | same call |
| SF7 | the anchor | the start counted back from the find's arrival | counted back from the register's find time | same call (54.35 t; asserted) | same call |
| SF8 | an hour's methane | that day's oil, analysis and 24 hours | the find day's rate for every hour | same call (54.42 t; asserted) | directive s.3.3 |
| SF9 | the analysis in effect | the latest taken on or before the day | the nearest in time | same call (54.62 t; asserted) | directive s.3.3 |
| SF10 | the windows fitted | windows ending at an arrival in 2026 | windows opening in 2026 | same call | directive s.3.1 |
| SF11 | events with December windows | in the return by their 2026 find | split at the year's end | same call (asserted) | directive s.3.1 |
| SF12 | the grouping of the fit | all of the operator's 2026 windows by kind | per route, per visit schedule, per battery | same call (55.13, 55.27, 56.76 t; asserted as the family) | same call |
| SF13 | the fit's form | a share plus a constant rate an hour | Weibull, isotonic, a straight line | same call (53.86, 56.98, 55.55 t; asserted as the family) | same call |

## Ladder

Measured by the generator on the cut pack; `checks.py` asserts every row on each build.

| Rung | Release-event methane (t) | Band | 2027 levy (CAD) | Call kept |
|---|---|---|---|---|
| L0 mid-window (default) | 45.18 | B | 115,200 | no |
| L1 every start at the previous departure | 87.46 | E | 360,000 | no |
| L2 hatches at the departure, the rest mid-window | 82.69 | E | 360,000 | no |
| L3 hatches a quarter in, the rest mid-window | 63.96 | D | 244,800 | no |
| G golden | 54.54 | C | 171,000 | yes |

The golden sits 6.54 t above band C's floor and 5.46 t below its ceiling; the standing family's nearest approach to
either edge is 53.86 t (the Weibull chance) and 56.98 t (the isotonic fit), and a per-tank form the windows reject comes
no nearer than 50.4 t. L0 sits 2.82 t under the floor (every midpoint reading the round 3 judge ran, 44.8 to 45.7 t) and
L3 3.96 t over the ceiling. A hatch split guessed at a third (57.70 t) lands band C; it is a guess and no route a reader
states.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the release events found at the licensee's batteries in calendar 2026 | filed (directive s.3.1); SF1, SF11 |
| 2 | Unit of account | an event, its methane in kilograms summed to tonnes | filed (directive s.3.1, s.3.4) |
| 3 | Attribution window | each event from its start to its closure | filed (directive s.3.2); SF2 |
| 4 | As-of dating | the exports pulled 8 to 13 January 2027 | C1 (one pull of each system) |
| 5 | Version basis | one export of each system | C1 |
| 6 | Denominator | none on the call | not applicable |
| 7 | Weighting | each hour at that day's tank vapour methane | filed (directive s.3.3); SF8 |
| 8 | Window length | the calendar year in local time; each event's own hours; Schedule B's halves to 30 June and from 1 July | filed (directive s.1, s.5.3) |
| 9 | Boundary inclusivity | bands from their lower bound to under their upper bound; the levy at the band's rate for each battery held at the start of 2027 (180) | filed (directive Table 1, s.4) |
| 10 | Rounding path | unrounded total banded; the year's methane on the fit of all the year's windows; Schedule B to one decimal | filed (prompt) |
| 11 | Tie-break | none needed | asserted: no standing construction within 3.0 t of a band edge |
| 12 | Maturity and censoring | an undated start at its expected value given the records | filed (directive s.3.2); the decisive step; SF5, SF12, SF13 |
| 13 | Order of operations | conform visits, join finds, date or expect each start, price each hour, sum, band | linear |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a geofence re-entry and a visit in both apps taken once | asserted (R2, SF3) |
| 16 | Identity normalisation | BT-0907 to BT-0907A; check-in app sites to batteries | asserted (R2) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | m3 of oil, m3 of gas per m3, mole per cent, 0.6785 kg a cubic metre | filed (directive s.3.3) |
| 19 | Code and status semantics | the register's kinds from its text; ALARM and NORMAL in the journal | asserted (R2, pooled kinds) |
| 20 | Integerisation | none on the call | not applicable |
| 21 | Clause scope | release events only; routine relief is not one; fugitive leaks in Schedule B | filed (directive s.2.2, s.5) |
| 22 | Forward window contents | none: a closed year | not applicable |

## Literal reader

Executing the prompt and every filed sentence word for word: the directive's return covers each release event found in
2026, its methane from its start to its closure at the battery's tank vapour methane in each hour, the start of a relief
valve that did not reseat at its alarm and every other start at its expected value given the licensee's records, and
the year's total sets the band. A literal reader dates the alarm-timed relief valves, and for every other event has to
say what start the records make expected: the records are the visit times and the finds, so the expectation is over how
events of each kind come to be found after windows of each length. Every way of taking that expectation from the
records (pooled, per route, per schedule, per battery; a share plus a rate, Weibull, isotonic, a straight line) files
band C at 53.86 to 56.98 t, and a per-tank form the windows reject (2 dlogL 145 on equal parameters) still files band C
at 50.4 to 51.8 t; only placing the start without asking the records (mid-window, the departure, a guessed split)
leaves band C. The directive names no placement, so the literal reading is the expectation and the golden.

## Oracles

No file ties only under the golden or only on a wrong read. The alarm-timed relief valves are exact on every reading and
are a kind no visit starts, so they sit evenly across their windows under the golden as under the default path; they
are evidence for the relief valves' placement only. No shipped file states a start for an event the records do not
date, a cause, a share or a band. The directive's band table and levies are fixed inputs. The ask's referees are each
device's own evidence and never an answer: the points each session in the survey log screened against its battery's
surveys, a contract work order's field ticket against its Completed day, the run each visit app records against each
visit (the route app's Route, the check-in app's run) against the register's 2027 runs, and a later leak repair work
order naming a tag the tracker had closed. No route total, count or control ties only under the golden's sessions,
repairs or runs.

## Ask sheet

The call's declared population is the release events found in 2026 with their windows (the visit timelines), the
register, the stuck relief valves' alarms in the SCADA journal, production on the events' days and the tank vapour
analyses. The one ask computes over none of it: the leak survey log, the leak tracker and the maintenance work orders
are read by no step of the call (asserted), and the visit apps' run fields and the register's route column are read by
no step of the call (the pooled fit; the family's route grouping reads the route app's runs). The hauler's tickets and
the sales gas meter statements ship as distractors: the vapour rate is read from production, not loads, and conserved
gas is no part of the return; no golden figure opens them.

- **Ask A, each route's 2026 fugitive methane in January to June and in July to December, from the leaks at the
  batteries it ran in that half, tonnes to one decimal (24 figures).** H18 home: Schedule B of the same return
  (directive s.5), the fugitive emissions the Board records beside the levied events, half-yearly like the surveys, rolled
  up by the runs the field manages its leaks by. User: the regulatory analyst who files the return. The directive files
  what a leak is (one component's escape from when it starts until the component is repaired, the same leak however
  many surveys find it before then), its rate (measured when first found) and its window; the data notes say what the
  tracker's Received and Closed record, that the survey log holds the camera crews' sessions at the batteries with the
  points each screened, and what a work order's Reference holds. Primary device (silent, D6 a log read as a roster): the
  survey log holds, beside each battery's three surveys, 318 re-checks of repaired fittings that the crews ran 30 to 75
  days after the tracker closed their tags, each screening 2 to 20 points and tagging nothing; a leak vents from its
  battery's last survey before it was found, so a reader who takes every session as a survey starts most of the year's
  autumn leaks weeks late. Only the points screened, read against the battery's own surveys, say which sessions are
  surveys. Twin: 124 of the 540 surveys tagged nothing either, so an empty tag count does not mark a re-check. Second
  device (silent, D8 a settlement date for the event date): a contract work order is completed in the maintenance system
  when the field foreman approves the contractor's field tickets, on the 10th of the next month or the next working day,
  and the tracker closes its tags that day; the day of the repair sits only in the field ticket's number in the Reference
  column (251 contract leak orders). The field's own maintainers complete theirs on the day of the work, and their
  references are the notifications the orders were raised on, so every reference's date read as the repair dates the
  field's own repairs at their notification. Twin: contract work outside the leak program completes the same way. The
  two devices pull opposite ways (a late start cuts a leak, a late repair adds to it), so their seeds (136 and 139) put
  the reader path and each half-fix off every cell. Hazards, each seen or filed in round 3: the runs redrawn on 1 July
  and 4 January (the register carries the 2027 runs), 36 re-checks that found a first repair still leaking (a later
  work order naming the tag), a deferred leak tagged again, the second crew's Friday sync, autumn 2025 leaks clipped at
  1 January, the battery's old code before its re-licensing. Stops, measured on the cut pack: the round 3 readers' path
  (every session a survey, each work order's Completed day: the cracker) 0 of 24, the same with every tag a leak (the
  mirror) 0, the register's runs with the tracker's closures and every session (the naive handling) 0, the sessions read
  right with Completed days 0, the field tickets read right with every session 0, the empty sessions dropped instead of
  the small ones 20, every reference's date as the repair 5, the tracker's closures 1, every tag a leak 0, Received as
  the survey day 0, one leak a component 2, the latest rate 4, the golden.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | as both round 3 readers did: the filed leak, rate and window rules, each half's runs from the two apps and each repair from the last work order naming its tag, with every session in the survey log a survey and each work order's Completed day its repair | misses |

Measured by: `generator/ceiling.py` on the cut pack (zip 3556c4e7).

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A fugitive methane by route in each half of 2026 | 24 | 0 | 0 | 0 | misses |

Over the 24 figures the cracker keeps 0.0 per cent of ask weight (scores 45.0 with the call), the mirror 0.0 per cent
(12.0), the naive handling 0.0 per cent; a reader who reads one device right and not the other keeps none, and one who
drops the survey log's empty sessions in place of its small ones keeps 20 (only 16 spring surveys tagged nothing).

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The construction layer is the event file and the band, which the cracker has with the call and the mirror misses with
it. This is the paper measurement of the cracker the script models, built on round 3's two readers' own path; the stage
4 readers measure the real one.

## Leak sweep rulings

`leak.py` on zip 3556c4e7 (verdict REVIEW, no LEAK; the dates sweep clean at the as-of 14 January 2027). The answer-figure
lines: the directive's band table carries each band's rate for each battery (the golden band's rate among them, as every
band's must be), and two route figures share their digits with the directive's section numbers 3.2 and 3.3; none is an answer,
and the directive's wording shares the call's vocabulary because the call is the directive's own levy. The
design-note vocabulary lines, ruled here rather than handed to a reader: the data notes and the directive share the
pack's own nouns (operator, vapour, relief, register, battery, journal, starts, expected, production) with the stump
paragraph, and neither says when an undated event began, how a start is placed, or that a visit can start an event; the
directive's one sentence on an undated start files the estimand (its expected value given the records) and nothing about
how it is taken. The tracker's notes and statuses never say a tag was found before, leaked on or synced late, the
register says it is as at 8 January 2027, no file says the runs were redrawn, and no shipped text says a session
re-checks, verifies or approves anything (asserted).

## Pre-ship check

1. Domain: an emissions inventory's own estimate of each release event's active hours where the start is undated,
   read from how often each kind is found against the window since the last visit; with another field's nouns there is
   no thief hatch a gauger opens, no flash vapour priced by the hour and no relief valve an alarm times.
2. Real work, nothing planted: every Layer 1 item is what the operator's systems write (two apps across a migration,
   geofence re-entries, a parallel run, a re-licensed battery, free-text kinds, a UTC journal with RTU stamps); none is
   on the decisive step (`checks.py` R2, every mishandling 53.61 to 54.67 t, band C).
3. The step that flips the call is analytical: the per-visit share of hatches (twice the log-likelihood gain 96.1),
   read from incidence against window length; no clause makes the choice (the directive files the expected start, not
   how it is taken).
4. Analyst test: every field and rule read correctly, mid-window starts file band B (R3a on the clean truth, 45.18 t);
   the decisive step alone files band C (R3b, 54.54 t), and the clean truth's own starts give 54.94 t.
5. The directive files the estimand (events found in 2026, each from its start to its closure, the undated start at its
   expected value given the records, each hour at that day's tank vapour methane, the bands); the standing family files
   band C at 53.86 to 56.98 t across groupings and forms (SF12, SF13), the per-tank form the windows reject 50.4 to
   51.8 t, and every convention row is asserted (SF1 to SF11).
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest driver 0.16 (task476 v2), differentiated on the card.
8. Asks: 24 Schedule B figures on columns and files the call never reads; round 3's readers' path (the cracker) and the
   mirror keep none (pair ceiling 28.5, `ceiling.py`); either primary read right alone keeps none, the empty sessions
   dropped keeps 20.

## Stage 4 round 1 (zip b85062d5, 2026-10-26)

Readers A and B (sonnet, medium, fresh copies) both filed band B and CAD 115,200, every undated start halfway through its
window (45.1 t and 44.9 t); neither read a share started by the departing visit. Reader A kept 31 of 47 ask figures
(every pneumatic and casing figure: the work orders rolled back, the minutes found from the set of fractions, the
wellbores from the location part; score_reader FAIL), reader B 14 (29.8 per cent). The isolated judge thread returned
DETERMINISTIC on the call (band C forced: every fit the windows support 54.0 to 54.5 t, the rate-only and midpoint
readings rejected by the data; Gates G and H pass) with FIX_NOW: the golden's tank hours counted the whole journal and
overlapping lifts on one point made their pairing a fork, and the one-decimal methane, the split by kind, the dated
bridge and the fit's parameters rest on an unfiled estimator. The fix pass withdrew the routine venting asks with their
five files, re-sited Schedule B onto the leak tracker with two silent primaries, dropped every lift that began inside
another excursion, stated the year's methane with its standing range (53.9 to 57.0 t), dropped the incidental
figures, defined the year in local time with the province's 2026 clock change in the data notes, and gave the
register's entry lags and the journal's receipt delays their real tails; the call and all 1,660 event rows stay
byte-identical to round 1's (asserted against the round 1 rows).

## Stage 4 round 2 (zip 5b6b5f54, 2026-10-26)

Readers C and D (fresh copies) both filed band B and CAD 115,200 (45.1 t, every undated start halfway through its window)
and kept 5 of 31 scored figures (16.1 per cent: the event counts and one route cell), each counting every tag as a leak
of its own and both mapping the second crew's Friday tags to their surveys. The isolated judge returned the call forced
(band C; the share-and-rate fits 54.0 to 54.2 t against the midpoint's 45.1 t; Gates G and H pass) and Schedule B open:
the directive never said whether a second tag on a component whose earlier tag was unrepaired is the same leak, nor
whose rate it carries, and nothing shipped said the second crew's tracker dates are its sync days. A Gate C failure
confined to the ask with the call forced is an ask-layer repair: the directive now files the leak, its rate and its
window, the data notes say what Received and Closed record, and the ask rides on two devices that stay true with every
term defined (the runs redrawn twice, the re-checks that found a repair had not held); the call and all 1,660 event
rows stay byte-identical (asserted against round 2's pack).

## Stage 4 round 3 (zip c216be49, 2026-10-26)

Readers E and F (fresh copies) both filed band B and CAD 115,200 (45.6 t and 45.1 t, every undated start halfway through
its window) and kept 28 of 29 scored figures each (96.6 per cent, score_reader FAIL): both read each half's runs from the
visit apps (E also found the 4 January reassignments) and took each repair from the later work order naming a re-checked
tag, so the redrawn runs and the re-check repairs were seen, not silent. The isolated judge (order kept) returned
DETERMINISTIC with FIX_NOW: band C and CAD 171,000 forced (the window-length hit rates carry an intercept, LR 44, under
day-night and weekend hazards), Schedule B reproduced in all 24 cells, Gates G and H pass; the blocks' "every fit the
windows support: 53.9 to 57.0 t" overstated how tightly the windows pin the figure (a per-tank form 51.8 t, 50.4 t on
windows to 60 h, the Poisson link 53.7 t), and the lowest of those sat 0.4 t over the 50 t floor. The per-tank form
scales a battery's chance with its tanks and the windows reject it (2 dlogL 145 on equal parameters; within each window
length the hatch rate does not rise with tanks), but the band edges moved to 36, 48, 60 and 72 t so that even it clears
the floor by 2.4 t while every midpoint reading sits 2.3 t or more under it, and the blocks state 54.5 t on the fit of
all the year's windows, band C, with no range. The ask layer was re-sited onto two silent primaries on the readers' own
path (the crews' re-check sessions in the survey log, contract work completed at its tickets' approval); the eight files
the call reads are byte-identical to round 3's (md5 asserted), so the call, all 1,660 event rows and every rung stand.

## Stage 4 round 4 (zip 3556c4e7, 2026-10-26)

Readers G and H (sonnet, medium, fresh copies) both filed band B and CAD 115,200 (45.1 t and 45.2 t, every undated
start halfway through its window, G's previous visit the last complete inspection) and kept 4 of 29 scored figures each
(13.8 per cent, the event counts; score_reader exit 0 twice): both read the survey log's sessions of 20 points or fewer
as re-checks and took each repair on its order's Completed day, so the contract approval held both and Schedule B kept
0 of 24 (G's 24 cells and 21 of H's are exactly the sessions-right, Completed-day handling the ceiling prices at 0).
The FIX_NOW re-judge (order kept) returned DETERMINISTIC and APPROVE: band C and CAD 171,000 forced (six share-plus-rate
fits 53.71 to 54.27 t, 5.7 t from both edges; every midpoint reading 44.6 to 45.3 t, band B; the found time 0.64 t,
band A; the previous departure about 89 t, band E), Schedule B reproduced in all 24 cells, Gate G
method_or_model_selection and analytical_non_defect, Gate H domain, layers and decisive step pass. Its two residual
notes, weighed and left as built: R10's July to December figure is 7.8497 t, 272 g under its rounding edge; of the
conventions that move one cell alone, only a fall-back hour on 1 November moves it (2.1 kg), the data notes say the
province kept its clocks at UTC-6 then, and the filed day convention gives the figure exactly; the survey and repair cut-offs are read from the data (sessions of 2 to 20
points that tag nothing against surveys of 100 to 410, field tickets against approval days), which the judge weighs as
data-supported and not reasonably contested, and pinning what a survey is in the notes would hand the device over.
Shipped on zip 3556c4e7.

## Tried and rejected

- 2026-10-26, draw screen for this number, each dead on file, on the rules or on paper before a card was written: the
  seed's own world (loyalty tiers cut from a spend distribution: a sort over a conformed column, and every step the seed
  names is semantics); customer identity across a wholesaler's accounts and marketplace channels (identity resolution, a
  rule or a reading); seasonal annualisation of part-year spend (task123, task474); claims completion, bundles against a
  comparison group, contract-order reconciliation, risk-adjusted ratios of totals and high-cost regression to the mean
  (the payment-claims cell's patterns, banned in the window or rule application); NEAT method choice under a large group
  difference (task471's screen: a fork), anchor drift, position effects, plausible values and rater drift (task450,
  task482 v6 and v11, task471 v2); quasi-identifier coincidences between two hashed lists (task468's false links on
  common identifiers, and too small at a fine key); random-effects pooling of emission-factor studies (a meta-analysis
  outside the record-linkage task type, and the interval estimators fork); clustered stack-test runs behind a revision
  (task261's driver); temporal disaggregation for a recession trigger and turning points on a trend-cycle (the survey
  research pairing is banned against task485 in this window); catalyst ageing per cumulative hours, fouling per fuel
  burned, cold starts by soak time and flare efficiency by wind (a rate carried across an operating condition: task459,
  task478 v7, task480); tank losses from gauge readings taken just before each refill (task229's driver, checks see the
  state just before resetting it); a storage tank's overflow at its own fill time (one subtraction once the gauge sheet is
  joined); the same visit-started events placed at a slate of hours (stumping 1.1h's two horns: the graded quantity here
  is one total, not a slate).
- 2026-10-26, stage 2: a share started by the visit for both hatches and pilots (every subset of kinds placed at the
  departure, hatches alone or pilots alone, lands within 7 to 12 per cent of the golden, so a domain guess files the
  band); one kind carrying the share leaves the shortcuts outside it.
- 2026-10-26, stage 2: doubling bands (under 50, 50 to 100, over 100 t): the midpoint and the gauger's shortcut cannot
  both leave the golden's band when the share and the hourly part sum to the golden (infeasible on paper); bands 10 t
  wide around 55 t carry it.
- 2026-10-26, stage 2: a bridge with one reconciling item per route: the routes' items move 1 to 3 t with the grouping
  the share is fitted over while the total moves under 2.5 t, so the items fork where the band does not (stumping 1.1j);
  the bridge is by kind.
- 2026-10-26, stage 3: Check-in app times exported in UTC: read as local wall time they move every summer find by six hours
  against its visit and file band E (92.5 t), a Layer 1 item carrying the call; the check-in app exports local time with its UTC
  offset and the register keeps each app's format, so every reading of the offsets files band C.
- 2026-10-26, stage 3: buffered alarms released in random order at the link's return made a held return-to-normal land
  before its alarm, so the journal's time column stretched lifts by days; the RTU's buffer now releases in order.
- 2026-10-26, stage 4 round 1 (zip b85062d5): Schedule B by route on the pneumatic survey rolled back through the work
  orders (D2 with D4 removals), the casing tests' hours and minutes with re-completions under a second well event (D3
  with D7) and the RTU-buffered alarms (D8): reader A kept 31 of 47 ask figures (every pneumatic and casing figure) and
  reader B 14; each device sits on the hygiene battery's list (change files over base lists, minutes logged per session,
  a clock against its stamp), so a careful reader executes it; withdrawn with their files, the ask re-sited onto the
  leak tracker.
- 2026-10-26, fix pass: the field's three routine venting totals kept beside the leak ask as construction figures: the
  cracker keeps all three and precut refuses an ask the cracker keeps; withdrawn.
- 2026-10-26, fix pass: the leak ask on one primary (a deferred leak tagged again) with leaks and methane by route: one
  leak a component (the over-cleaning reflex) kept every route's count of leaks unrepaired at the year's end, since one
  point holds one open leak at a time; with the counts moved to leaks that vented in 2026, a reader who cracked the one
  primary would keep every figure, so a second silent primary (one crew's sync dates) went in, on a half-year split
  that moves every figure under either primary mishandled alone.
- 2026-10-26, fix pass: the leak stream's seed 62 put both half-year totals on whole tonnes (99.0 and 64.0 t), which
  reads as invented; seed 72 keeps both twins on every route and lands 103.3 and 60.3 t.
- 2026-10-26, stage 4 round 2 (zip 5b6b5f54): a deferred leak tagged again as the ask's primary rode on the undefined
  word "leak" and the unfiled rate of a re-found leak (judge Gate C), and the second crew's sync dates on no shipped
  basis; defining all three hands both devices to every reader who reads the directive, so they stay as filed hazards
  and the ask moves onto data a defined term does not settle.
- 2026-10-26, repair: the re-check failures as the second per-figure device: over 40 seeds of the failure draw in the
  built world, at a quarter of repairs or more, the tracker's closures move 11 to 18 of the 24 route halves, never all
  (a spring repair's re-check lands mostly after 30 June); kept as a device moving 18 (seed 117), with the runs' two
  layers moving every figure.
- 2026-10-26, repair: a check that no lease operator is on two sites at once found 17,832 overlaps in the world itself
  (run slots 33 minutes apart against visits of 15 to 40 minutes, and relief operators double-booked on some days):
  the visit timelines are the call's population and stay as built; the redraws trade batteries at the same place in
  their runs' day, so they add no overlap of their own (asserted on the morning slot).
- 2026-10-26, stage 4 round 3 (zip c216be49): the runs redrawn twice and the re-checks that found a repair still
  leaking, found by both readers (28 of 29 each): each half's run is a column on every visit and the later work order
  names its tag and says why, so noticing either is repairing it (a code re-derived from the finer key, a comment read
  for what it says); kept as hazards, the ask moved onto two primaries whose evidence is a cardinality and a reference.
- 2026-10-26, fix pass: the contract posting device alone moved 21 to 23 of 24 cells over seeds, never all: a first
  half's methane is mostly the spring-to-June share of leaks found in the autumn, set by the window's start, which a
  repair date cannot reach; the re-check sessions work the start, and since the two pull opposite ways the pair was
  seeded where the reader path and each half-fix miss every cell.
- 2026-10-26, fix pass: dropping the survey log's empty sessions in place of its small ones keeps 20 of 24, because
  only 16 spring surveys tagged nothing; recorded as the weak over-cleaning stop rather than built up (more empty spring
  surveys need a thinner leak world, which moves every figure the two primaries were measured on).
- 2026-10-26, fix pass: the band edges at 40, 50, 60 and 75 t left a per-tank form the judge fitted 0.4 t over the
  floor; the windows reject it, but a floor that close to a member anyone fits is margin fragility (task482 v10), so the
  edges moved to 36, 48, 60 and 72 t, the levies unchanged.
