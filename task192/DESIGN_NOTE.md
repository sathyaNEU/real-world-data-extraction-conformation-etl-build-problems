# task192 design note

Architecture 4, drawn 2026-11-04. The slot keeps its number and its objective (Anomaly Detection &
Diagnostics) and leaves the Portuguese protest register for good: architecture 3 (a classifier corrected by
hand-coded audits) is spent, its shipped pack (060f8959) stays at the portal, pending, and its design is in the
git history of this file (commit 826dc6b and earlier). New client domain, world, dataset, generator and prompt
shell; no seed mechanism used. The 55 screens that preceded this draw are in the Tried and rejected section
(A4.1 to A4.55).

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task192.json`, architecture v4, registered 2026-11-04T04:24:23Z at WARN |
| Client domain / task type | Energy Systems & Utilities (`energy-systems-utilities`), `grid-reliability-outage-analysis` (serves RC and AD): finding the component that is breaking down on a distribution feeder is the network's reliability analysis of its own protective-device records |
| Objective | Anomaly Detection & Diagnostics: a real event (one insulator breaking down) separated from the ordinary momentary interruptions that raise the same counts (lightning, wind and tree contacts, squirrels, the exposure of long rural lines) |
| Decision | which feeder Kestrel Falls Municipal Utilities' one overhead line patrol crew works in the week of 9 November 2026, and the stretch of it to walk, or none; pick one of the city's feeders (`pick_one_of_n`), forward facing (the crew's coming week, before the component fails outright and locks the feeder out) |
| Shape | 07, a grid of cells: every feeder by its 2026 reliability indices (SAIDI, MAIFI-E, CEMI-2: the asks), plus the call, the stretch, the second choice and what keeps it second |
| Gap / pattern / generators | `objective` (the momentary counts are correct and are not what the patrol is scored on); pattern `none`; `G2` decisive (the record's unit is a protective operation, the decision's a failing point on a feeder), `G10` second (one point's failures counted as several events) |
| Gate G | `decomposition_attribution`: each feeder's momentary events attributed to storms, wind and trees, animals, exposure and one repeating point |
| Strategy | `grain_or_unit` (operations grouped into the points they came from); Layer 2 family `field_method`; pattern `own:repeat-faults-located-by-their-recorded-fault-current` |
| Forum, forcing event, org family | `operations_desk` (the distribution operations desk dispatches the crew), `shift_or_daily_cycle` (the weekly crew assignment), `local_government` (a city department, the electric division of a municipal utility) |
| Role | the utility's distribution reliability engineer (`other`) |
| Context artifact | `filed_standard`: the utility's Distribution Reliability Procedure DRP-04 (the patrol's purpose, the definitions and indices, the major event day rule, the storm patrol) |
| Calibration | none |
| Personas | Kelsey Sanford, Shawn Hartman (`guard.py names --geo us --seed 192`) |
| Deliverables | `line_patrol_2026-11-09.xlsx` (the call, the stretch, the second choice, the per-feeder indices, the eleven operations), `reliability_2026.svg` (each feeder's SAIDI against its MAIFI-E, the feeder the crew walks labelled) |
| WARNs answered | `three_rules.strategy_risk` (grain_or_unit): the analyst test below files a squirrel feeder with every field and rule read correctly, so the step is analytical; `overuse.objective`: the number's objective is fixed by START_HERE.md; `repeat.deliverables` (svg+xlsx, against task193 v3): a scatter of the two indices is the species that makes a feeder's standing read at a glance, and the prompt's other shell classes are under their quotas; the shell itself (question form `what`, second sentence `List`, the chart sentence `In ...`, no week number in the question or the file name) is drawn away from task194's crew-allocation shell, which `guard.py surface` promoted for adjudication |

**Data-native sentence.** A feeder head relay records, for every fault it trips on, the faulted phase and the
current the fault drew, and on a radial overhead feeder that current falls with the fault's distance from the
substation through the line's impedance (the device register's protection-study currents fall the same way,
device by device); one cracked insulator that flashes over on damp mornings and recovers when it dries draws the
same current on the same phase every time, so its flashovers are several momentary events sharing one signature,
which no count of events, no storm screen and no per-mile rate can tell from the squirrels, trees and lightning
that make up the rest of the record.

**Abstraction sentence (written to be refused).** "The decisive quantity is where a unit's repeated failures
come from, recovered by grouping its events on a recorded signature that stands for position along the unit."
No approved or delivered build carries it: task183 forecasts cable failures from each identified section's own
failure history (the parts are known by id and the call is a forward count), task303 removes the tickets every
feeder opened in the same minute as one upstream loss (a shared cause across units), task194 nets one area's rise
against a neighbour's simultaneous fall (supply passed between units), task200 re-measures detection on first
meetings with an image (a history-defined subset). Nearest driver on file 0.07 (task132).

**Sources.** Fully constructed operating layer for a fictional municipal electric utility in Missouri: the
feeder head relays' event records, the mid-line recloser controls' logs, the SCADA sequence-of-events log, the
outage management system's tickets (two layouts across its April 2026 replacement), the protective device
register with its in-service history and the protection study's available fault currents, the transformer list
and the service point extract from the GIS, the feeder register, the lightning detection network's strokes, the
airport weather station's hourly observations, the substation locations, the line clearance log, customer
contacts about blinking lights, and the Distribution Reliability Procedure. Provenance in `metadata.json`.

## Default path

1. Read DRP-04: the patrol goes to the feeder where a component on the overhead line is breaking down (5.2);
   a momentary interruption event is a customer's interruptions within five minutes of the first (2.5); a storm
   day for a substation is a day with a cloud-to-ground stroke within five miles or an airport gust of 40 mph or
   more (6.1).
2. Count each feeder's momentary interruption events for August to October 2026 from the SCADA log (feeder
   breakers) and the recloser controls' logs, operations within five minutes of the first making one event,
   converting the controls' standard time and SCADA's Central time.
3. Set aside each substation's storm days (the lightning file within five miles of the substation, the airport's
   gusts in knots against 40 mph).
4. Normalise each feeder's non-storm events by its overhead miles from the feeder register, and set the result
   against August to October 2025 to see which feeder's blinking is new.
5. Send the crew to the feeder whose non-storm rate rose most: NYD-3, up 2.53 events a mile, against 0.42 for
   the next feeder (MLR-1); the outage tickets' animal causes on NYD-3 (6 since August against 1 a year earlier)
   read as confirming that the rise is real.

Ends on: NYD-3 (North Yard 3, up 2.53 non-storm momentary events a mile on 2025)
Golden: MLR-2 (Millrace 2, eleven momentary faults on phase C at 1,423 to 1,448 A recorded by its breaker)

## Stump sentence

A competent solver who groups every feeder's reclosing operations into momentary interruption events, sets aside
the storm days, normalises by overhead miles and compares August to October 2026 with 2025 sends the patrol to
NYD-3, whose new blinking is squirrels, when MLR-2's breaker has recorded eleven momentary faults on phase C at one
current since mid-August because an insulator on its main line is breaking down.

## Three rules

Task type: `grid-reliability-outage-analysis` in `energy-systems-utilities`, which serves anomaly detection; locating the component that is breaking down on a distribution feeder from its protective devices' fault records is the utility's reliability analysis of its own network.
Domain test: the deciding quantity is whether a feeder's momentary faults keep coming from one place on its line, which distribution protection reads from the current each fault drew, because that current falls with the fault's distance from the substation through the feeder's impedance (the register's protection-study currents fall device by device the same way), so one insulator flashing over again and again records one current on one phase.
Swap: "send the inspector to the ward where a device is failing, read from the alarms each bed raised" keeps none of it: there is no feeder impedance, no fault current that falls with distance, no flashover that clears when the breaker recloses and no momentary interruption to count.
Layer 1: relay records in UTC against the SCADA log in Central time and the recloser controls on standard time all year (three systems, one event in two of them); fault terminals against feeder phases and kiloamps against amps (the controls' vendor); Cotter Road's old feeder, breaker and SCADA names before the 14 March 2026 rebuild (the asset register's crosswalk); outage tickets in two layouts across the April 2026 OMS replacement, partial restorations as child tickets in one and a steps sheet in the other; relay records lost on busy storm days outside August to October (the event buffer); taps moved between feeders at three dates (the register's dated rows); service points connected and retired through the period (the GIS); none placed to be caught.
Layer 2: `field_method` / grain: the feeder's operations are grouped into the points they came from; the methodological choice that flips the call is reading each momentary operation's recorded phase and fault current as a place on the feeder and looking for the place that keeps failing, instead of counting, screening and normalising the operations.
Decisive step: recognising that a breaking-down component announces itself as self-clearing faults that keep returning to one place, and finding that place by grouping each device's momentary operations on the faulted phase and the current the device recorded for them, counted across separate mornings.
Not semantics: every field, unit, clock and code read correctly (the relays' amps and UTC, the controls' kiloamps, terminals and standard time, SCADA's Central time, the five-minute event rule, the storm screen, the old Cotter Road names) still leaves the counts, the storm-screened counts, the per-mile rates and the change on 2025 on NYD-3, NYD-2, BLV-3 or SYC-1; no column holds a place or a repeat.
Not rule application: DRP-04 files the patrol's purpose, the definitions, the indices, the major event day rule and the storm patrol and nothing about where faults come from, so executing every filed rule files NYD-3; the enumerated family (momentary events, storm days set aside, per overhead mile, per customer, against 2025, damp mornings, phase share and chi-square, and the asks' own SAIDI, MAIFI-E and CEMI-2) spreads its first place over five feeders (NYD-3, NYD-2, BLV-3, SYC-1, SYC-3) and never puts MLR-2 first or second (ninth on the screen); the standing family once faults are placed by their current is one member whose band is a corridor (eleven against seven at every band from 1 to 5 per cent since August), and the ruling-out is loud: eleven same-phase operations at one current that no other feeder approaches (at most five).
Analyst test: a strong analyst who reads the SCADA log and the controls' logs into momentary events, sets aside storm days, normalises by overhead miles and compares with 2025 files the default path's feeder, NYD-3, whose rise the outage tickets put on squirrels, and never asks where on each feeder the faults were.
Estimand: DRP-04 5.2 to 5.4: the weekly patrol goes to the feeder where a component on the overhead line is breaking down, so that it is found and replaced before it fails outright; storm damage, animal contacts and tree contacts are the other programmes' work; the assignment names the feeder and the stretch to walk as a protective device's zone; filed in `procedures/DRP-04_distribution_reliability_procedure_rev6.pdf`.
No decoy: nothing is planted to be caught: no memo, draft, briefing or stakeholder figure names a feeder; the failing insulator is an ordinary component failure whose only trace is its own flashovers in the relay records, and the squirrel year, the overgrown taps and the phase B taps are the seasons those feeders have.
No certified replay: the method is not recovered by reproducing certified or published figures; no shipped figure is a fault location, a repeat count or a ranking of feeders.
Lesson: a feeder's momentary interruptions are a mixture of independent events and one repeating source, and the repeating source is found only by placing each fault on the line through the current it drew; no build on file teaches locating a failing component from repeated fault-current signatures.

## Survivor anatomy

Actor: the deciding property (one point on a feeder failing again and again) has no column in any file; it is a relation between a feeder's own momentary operations, the same phase and the same recorded current on separate mornings.
Link: the signal is read through a comparison the field's momentary-interruption method never asks for, each operation's fault current against the other operations' currents on the same device and phase; the register's available fault currents say a current is a place, but no key joins an operation to a pole.
Reflex: the field's named method for targeting patrols (momentary interruption events, storm days set aside, per overhead mile, against last year: IEEE 1366's worst-performing-circuit screen) sits at rung 0 and files NYD-3; the indices the prompt asks for file NYD-2, SYC-3 or SYC-1.
Back-test: the textbook route validates: NYD-3's rise is matched by its outage tickets' animal causes (6 since August against 1 a year earlier), and the line clearance log shows MLR-2 fully trimmed in March and April 2026, which is why its tree contacts and its counts fell exactly as the clearance programme expects.
Second use: the relay records carry every rung and the asks' momentary events; the controls' logs carry the recloser zones' events; the register carries the tree every ask walks and the protection study's currents its fuse links are sized against; the weather and lightning files carry the storm screen; deleting the decisive step removes no file.
Shock: MLR-2's August to October count is 16, ninth of sixteen; its rise on 2025 is 4 events (clearance took out its tree contacts); its non-storm change per mile is ninth; its phase-C share 0.69 is fifth; its SAIDI 139.3 is mid-pack; it is no sort's extreme.
Pins: the procedure files the patrol's purpose, the definitions, the indices, the major event day rule and the stretch's form; no filed sentence names fault currents, positions, repeats or phases.

## Readability screen

Reflex row from the field's vocabulary for where to patrol: momentary interruption events, MAIFI-E, worst-performing circuits by SAIDI, SAIFI and CEMI-n, storm-day screens, per mile and per customer rates, the change on last year, damp-weather flashover counts, single-phase concentration.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the momentary screen, storm days set aside, per mile, against 2025 (NYD-3) | DRP-04 2.5 and 6.1 define the event and the storm day | SCADA and the controls' logs | yes: the worst-performing-circuit screen | the OMS animal causes confirm it | no | one subtraction per mile | no | readable |
| R1 damp-morning momentary events (NYD-2) | no sentence | the airport file's humidity and fog codes | yes: contaminated insulators flash over in fog and dew | none | no | one filter | no | readable |
| R2 single-phase concentration (BLV-3) | no sentence | the relays' event types | yes: a phase problem shows on one phase | none | no | one share | no | readable |
| R2b the asks' indices, worst circuit first (NYD-2, SYC-3) | DRP-04 3.1 defines them | OMS and GIS | yes: patrol the worst circuit | none | no | one ratio | no | readable |
| R3 momentary faults grouped by device, faulted phase and recorded current across separate mornings (decisive) | no sentence names currents, phases, repeats or places (checks.py R3c) | no column holds a place or a repeat; the relays carry each trip's currents as every event summary does | no: the field's patrol reflex is the momentary screen; a fault is located by its current after a lockout, never across months of self-clearing faults | none: no record names a component | no: nothing duplicated, missing or mis-keyed in the window (every August to October breaker opening has its relay record) | no: a grouping per device and phase on a current band, counted on separate days | no: the relay archive serves every rung and the asks' momentary events, the register's currents its fuse coordination | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | customers served | service points supplied on 31 October 2026 | the feeder register's 2025 planning count; every row of the extract | same call (asks move) | DRP-04 2.1; the extract's feeder column and the register's dated tree agree on every service point, asserted |
| SF2 | major event days | days whose daily system SAIDI exceeds the filed 38.03 minutes over the filed 35,404 customers | a threshold recomputed from 2025 alone; UTC days | same call; 19 May and 27 June under every reading | DRP-04 4.1 and 4.2; every other 2026 day sits under 0.6 of the threshold and both sit over twice it, asserted |
| SF3 | an interruption's day | the local day it began, a continuation the day its outage began | the day a later ticket opened | same call | DRP-04 2.6 and 2.3; asserted |
| SF4 | sustained against momentary | more than five minutes against five or less | the OMS's tickets as the sustained record | same call | DRP-04 2.2; no SCADA opening lasts between 4.5 and 5.6 minutes, asserted |
| SF5 | customer minutes of a stepped restoration | each step's customers from the outage's start to their step | the parent's whole duration for everyone | same call (asks move) | DRP-04 2.4; asserted |
| SF6 | a momentary interruption event | per customer, the interruptions within five minutes of the first | per device | same call | DRP-04 2.5 says a customer's; the few two-device pairs inside five minutes are merged per customer, asserted |
| SF7 | a feeder's interruptions | those of its devices as the feeder stood when each began | today's tree | same call | DRP-04 3.2; asserted |
| SF8 | January to October 2026 | local calendar days 1 January to 31 October | UTC days | same call | the prompt and DRP-04 2.6; asserted |
| SF9 | rounding | minutes to one decimal, events per customer to two | other precisions | same call | the prompt; every figure clears its rounding edge by a tenth of a unit, asserted |
| SF10 | the band and window a repeat is read in | plus or minus 2 per cent since 1 August, separate days | 1 to 5 per cent; all trips or one per day; the phase current or the residual; since 1 August, September and October, or all of 2026 | MLR-2 under every one | asserted across 72 groupings: by 1.3x or more since August at every band from 1.5 per cent and over the year to 3 per cent, first under every grouping |
| SF11 | the runner-up | SYC-3, seven operations of recloser R-3114 on phase A at 996 to 1,005 A | the next feeder at a 5 per cent band | SYC-3 to a 3 per cent band | asserted; at 5 per cent unrelated faults on busy feeders join wide bands, which is why the band follows the relays' own spread |
| SF12 | which of two failing components the one crew takes | MLR-2 | SYC-3 | MLR-2 under every criterion | more operations (11 against 7), more customers behind the device (2,625 against 863), earlier onset, as recent; asserted |
| SF13 | the stretch to walk | the breaker MLR-F2-52's zone to recloser R-2207 at MLR2-P071 | a span of poles | same call | DRP-04 5.4 files the stretch as a device's zone; asserted |
| SF14 | a service ticket opened at the minute the device above closed | the same customer's interruption carrying on | a second interruption | same call (asks move) | DRP-04 2.3: the customer never regained supply; asserted |
| SF15 | an opening SCADA holds for 5.7 to 13.6 minutes with no ticket | a sustained interruption, timed by the SCADA log | not an interruption | same call (asks move) | DRP-04 2.2 defines it by duration, not by ticket, and 2.7 times it from the SCADA log; asserted |
| SF16 | customers already without supply when a device locks out | not interrupted again | counted by the OMS's device count | same call (asks move) | DRP-04 2.3; asserted |
| SF17 | a momentary event whose customers' sustained interruption begins in the event's minute (a fuse or transformer fuse blowing behind the operating device) | part of that customer's sustained interruption; a sustained interruption beginning after the event's minute leaves the event standing | absorbed by any sustained start up to five minutes after the first trip (the earlier generator) | same call (asks move: CTR-2's MAIFI-E) | DRP-04 2.5 second sentence, read at the outage system's minute (2.7); a fuse that blew on the reclose carries its operation's minute in the OMS, asserted; in the window the one sustained start after an event's minute and inside its five minutes is CTR-2's fuse of 26 July, blown by a second fault two minutes into a breaker event, which leaves the customers' first momentary interruption a momentary event under every literal reading, asserted; no sustained interruption begins in the minutes just before an event, asserted |
| SF18 | a legacy child ticket's Out | when the step was logged; the customers were out from the parent's Out | the customers' outage start | same call (asks move) | DRP-04 2.4; asserted |
| SF19 | a tap moved between feeders | its interruptions before the move with the old feeder | today's feeder | same call (asks move) | DRP-04 3.2; asserted |
| SF20 | a service point connected or retired during the period | interrupted only while connected | interrupted all period | same call | no service point is connected or retired on a day an interruption reached it, asserted |
| SF21 | the trips before a lockout | part of the sustained interruption | momentary events | same call | DRP-04 2.5; no momentary event sits in the five minutes before a crew lockout on its device, asserted |
| SF22 | an interruption's start and end where the OMS and the SCADA log both record it | the OMS's times, to the minute | the SCADA log's second | same call (asks move: SAIDI) | DRP-04 2.7, which also sends a recloser's momentary interruptions to its own event log (the log carries every recloser, SCADA or not); every SCADA opening over five minutes pairs with its ticket within a minute or has none within a day (73 paired, 13 with no ticket, the nearest 2.5 days away), asserted |
| SF23 | planned interruptions | counted like any other | left out, as many utilities report | same call (asks move: SAIDI and CEMI-2) | DRP-04 2.2 last sentence; the window holds planned tickets on nine feeders, asserted |
| SF24 | a service point connected or retired on the period's last day | none in the data | supplied or not on 31 October | same call | no service point is connected or retired on 31 October 2026 or after it: a date the event-day rule would carry onto the last day goes back to the latest free day before it, asserted |
| SF25 | the start of a sustained interruption the OMS does not record | the opening that locked out its breaker or recloser; the trips and recloses before it are part of it for counting (2.5) and do not move its start | the sequence's first opening (2.5's "part of the sustained interruption" read as a time); the sequence's second opening | same call (asks move: seven feeders' SAIDI by 0.2 to 0.8) | DRP-04 2.7 last sentence, the closing pin ("runs, for the indices, from the opening that locked out its breaker or recloser, as the outage management system times those it records"); corroborated by the OMS, which carries the lockout's minute on all 25 ticketed lockouts whose first opening and lockout fall in different minutes; asserted: the sentence, the 25, every unticketed lockout the last opening of a sequence under half a minute with no other opening in the five minutes before it, and the sixteen figures |

## Ladder

| Rung | Construction | Names | Figure | Runner-up | Margin | Dies to |
|---|---|---|---|---|---|---|
| R0 | momentary events since August, storm days set aside, per overhead mile, against 2025 (default path) | NYD-3 | 2.53 a mile | MLR-1 0.42 | 6.0x | its rise is squirrels (DRP-04 5.3), its operations scattered over the feeder: largest same-phase group 2 |
| R1 | non-storm momentary events on damp mornings (the insulator reflex) | NYD-2 | 18 | SYC-1 12 | 1.50x | wet limbs on overgrown taps (its tickets' vegetation causes), scattered currents: largest group 2 |
| R2 | single-phase concentration of momentary first trips (the phase reflex) | BLV-3 | share 0.96, chi-square 44.2 | CTR-2 0.72, 12.3 | 1.33x, 3.6x | its long phase B taps through the oaks: the concentration is its taps' phase, the currents spread (largest group 5) |
| R2b | the asks' indices, worst circuit first | NYD-2 (SAIDI 412.9, MAIFI-E 47.18), SYC-3 (CEMI-2 2,325) | | SYC-3 356.4, SYC-2 45.29, NYD-2 2,237 | 1.16x, 1.04x, 1.04x | the indices measure what customers lived through, not where a component is failing |
| R3 | momentary faults grouped by device, faulted phase and recorded current on separate mornings (decisive) | MLR-2 | 11 at 1,423 to 1,448 A, phase C, breaker MLR-F2-52 | SYC-3 7 at 996 to 1,005 A, phase A, recloser R-3114 | 1.57x | none |

- Position: MLR-2 ninth on R0, sixth on R1, fourth and fifth on R2, ninth on SAIDI, seventh on MAIFI-E and fourth on CEMI-2; first only on R3; never second within 1.2x on any rung (asserted on ten cheap constructions and five indices).
- Dominance: the decisive construction takes the screen's pick NYD-3 from first to a largest group of 2, against MLR-2's 11; MLR-2 leads the runner-up by 4 operations (1.57x) and every other feeder by 6 or more.
- Worth in bins: the call is a named feeder; the graded figures are exact counts and sums with no fitted parameter, each clear of its rounding edge by a tenth of a unit or more (asserted).
- Pricing: (1) the residue the WHAT leaves is which feeder's momentary faults keep coming from one place, a method; its band is a corridor (11 against 7 at every band from 1 to 5 per cent since August, SF10), not a knob. (2) MLR-2 must climb from ninth on the screen to first; the construction carries it there by 11 against at most 7. (3) The one-group-by routes a solver writes first (counts, rates, changes, shares by feeder) all file other feeders; the one grouping that files MLR-2 is the decisive step itself, on a current band no column holds. (4) No estimation: the group sizes are counts, MLR-2's 9 to 11 across the bands is the corridor's whole spread. (5) No variance lever. (6) MLR-2's own history shows no step: 12 momentary events in August to October 2025, 16 in 2026. (7) The eleven are 11 of 1,027 relay records, ordinary single-trip momentaries among 1,016 others. (8) The reflex sweep runs as code in checks.py: raw, change, non-storm, per mile, per customer, against 2025, damp mornings, phase share and chi-square, SAIDI, MAIFI-E (over the year and since August), CEMI-2 and its share each name another feeder.
- Clean truth: on the simulation's own operations, before any file is cut, the grouping names MLR-2 and the default path NYD-3 (checks.py R2).

## Closure table

| Axis | Name | Reading | Closure |
|---|---|---|---|
| 1 | Population | every feeder in the register, every service point the GIS lists, every interruption planned or not | DRP-04 1.1, 2.1 and 2.2; all sixteen graded; SF23 |
| 2 | Unit of account | the feeder for the call and the asks; the customer inside each index | DRP-04 3.1 and 3.2 |
| 3 | Attribution window | January to October 2026 for the asks; the call's operations since August, corridor to the whole year | prompt; SF10 asserted |
| 4 | As-of dating | an interruption's local start day, its start and end the OMS's where it holds the interruption and the SCADA log's where it does not | DRP-04 2.6 and 2.7; SF3, SF22 |
| 5 | Version basis | the register's row in force on the day | DRP-04 3.2; SF7, SF19 |
| 6 | Denominator | customers served on 31 October 2026; daily SAIDI over the filed 35,404 | DRP-04 2.1 and 4.2; SF1 |
| 7 | Weighting | each customer equally | DRP-04 3.1 |
| 8 | Window length | ten months for the asks | prompt |
| 9 | Boundary inclusivity | five minutes or less is momentary; no service point starts or ends on the last day | DRP-04 2.2; SF4 and SF24 asserted |
| 10 | Rounding path | compute exactly, round once at print | prompt; SF9 asserted |
| 11 | Tie-break | none needed: 11 against 7, and MLR-2 leads SYC-3 on every patrol criterion | SF12 asserted |
| 12 | Maturity and censoring | no interruption runs past 31 October | asserted by the build (the period's last restorations close inside it) |
| 13 | Order of operations | major event days first, then the indices | DRP-04 4.2 |
| 14 | Row order | not used | C1 |
| 15 | Duplicate resolution | SCADA reclosers in two logs counted once (the controls' logs carry every recloser); continuations not a second interruption | SF14; asserted |
| 16 | Identity normalisation | old Cotter Road names to new through the register's crosswalk | the Cotter Road sheet; asserted (OMS counts reproduced) |
| 17 | Netting against gross | customers already out netted from a later outage | SF16 |
| 18 | Dimensional units | kiloamps and amps, knots and mph | the files' headers; same call |
| 19 | Code and status semantics | event types and terminals to phases through the register's phasing | asserted (the verifier reads them independently) |
| 20 | Integerisation | CEMI-2 counts whole customers | DRP-04 3.1 |
| 21 | Clause scope | DRP-04 5.3 sets storm, animal and tree contacts aside from the patrol | SF12; same call |
| 22 | Forward window contents | the crew's week of 9 November | DRP-04 5.1; the call is the assignment for the week of 9 November |

## Literal reader

Executing DRP-04 word for word gives the indices (2.1 to 4.2, every convention closed by a quoted sentence, SF1 to SF9 and SF14 to SF25) and leaves the call to 5.2's literal estimand, the feeder where a component on the overhead line is breaking down: read literally, that is a fact about the line, and the only records of a component breaking down are the eleven same-phase operations at one current on MLR-2's breaker (and SYC-3's seven, which the one crew takes second under every criterion, SF12); no filed rule names a feeder, the storm screen of 6.1 is the storm patrol's, and every reading of the open band and window prints MLR-2 (SF10).

## Oracles

None that ties only under the golden. The OMS's cause codes confirm the screen's picks on the wrong path (NYD-3's animal causes, NYD-2's vegetation causes); the line clearance log explains MLR-2's fall in counts and confirms the screen's reading of it; the blinking-light contacts track momentary counts and rank NYD-3 and NYD-2 highest; the register's available fault currents bracket every feeder's faults alike and rank nothing.

## Ask sheet

Three asks, every figure per feeder, each on rows outside the main call's population (the call reads the feeder relays' first-trip records and the controls' TRIP rows of the momentary events since 1 August, and the register's terminal phasing).

- **A1, minutes of interruption per customer served, January to October 2026, major event days left out (one decimal), 16 figures.** H18: a measure every candidate carries that the call does not turn on. Primary device (D6/D8): in the legacy layout a partial restoration is a child ticket whose Out is when the step was logged, while its customers were out from the parent's Out. Second (D5/D1): customers already without supply when a device locks out are not interrupted again, while the OMS counts them in its device count (SF16). Hazards: the breaker and recloser openings SCADA holds for 5.7 to 13.6 minutes after the desk test-closes a lockout, which the OMS never ticketed because it opens an incident only for an outage still on after fifteen minutes (DRP-04 2.7 now times an interruption the OMS does not record from the SCADA log, so a careful reader goes looking, and the cracker is priced finding them), the steps sheet carrying the final step, the old Cotter Road names, the major event days, UTC against local. Stops: OMS parents at face value (mirror, 5 of 16), children at their own Out with the SCADA openings (cracker, 8 of 16), children from the parent's Out but the OMS alone (8 of 16), children from the parent's Out with the SCADA openings and no netting (13 of 16).
- **A2, momentary interruption events per customer served, same window (two decimals), 16 figures.** H18: the momentary record behind every feeder's blinking. Primary device (D6/D7): a fuse-saving fast trip that a fuse or transformer fuse blows behind in the same minute is part of those customers' sustained interruption (DRP-04 2.5), found only by matching each device event to the OMS tickets that begin in its minute on the devices below it. Second: customers already without supply when the device opens, and two devices opening on one customer inside five minutes (one event for that customer). Hazards: the relay archive's lost records on busy storm days (SCADA is complete), the SCADA reclosers in both SCADA and their logs, test closes inside five minutes (momentary, in SCADA and the logs only), the controls' standard time. Stops: device events times the customers below them (cracker and mirror, 1 of 16), absorption handled alone (9 of 16), absorption and the customers already out handled but not the per-customer merge (15 of 16).
- **A3, customers with more than two sustained interruptions, same window (whole), 16 figures.** H18: the customers each feeder's record leaves worst off. Primary device (D1, one event under two records): a service ticket opened at the minute the device above it closed is that customer's interruption carrying on (a storm-damaged drop, found when the crew closes the device or on the crews' later sweep), not a second one. Second: the SCADA-only sustained openings, now pointed at by DRP-04 2.7. Hazards: the register's dated rows (taps moved at three dates), connections and retirements, customers already out, the old names. Stops: tickets through today's tree (mirror, 4 of 16), every ticket counted on the dated tree with the SCADA openings (cracker, 9 of 16), continuations merged but the OMS alone (8 of 16), both handled (15 of 16).
- Separation: zero ask-device rows in the main population: the devices live in the OMS (continuations, child tickets, fuse tickets), SCADA (test-close durations) and the GIS; every August to October breaker opening has its relay record, and the call is the same on the clean truth (asserted).

| Ask | Cracker (lands the call, hygiene battery, every filed rule) | Mirror (the procedure's screen, the OMS as the record) | cracker verdict |
|---|---|---|---|
| A1 SAIDI | 8 of 16, children at their own Out, the SCADA openings found | 5 of 16 | miss |
| A2 MAIFI-E | 1 of 16, device events times customers below | 1 of 16 | miss |
| A3 CEMI-2 | 9 of 16, every ticket counted on the dated tree, the SCADA openings found | 4 of 16 | miss |

Pair ceiling: 44.5 (cracker 65.6 on the call, mirror 23.5 off it, 38 + 7 + 55 L)
Mirror leakage: 20.8 per cent of ask weight
Cracker keep: 37.5 per cent of ask weight, under two fifths; the full includer who handles one more device keeps 13 of 16 on A1, 9 of 16 on A2 (15 with the customers already out as well) and 15 of 16 on A3, and still misses the other asks' blocks
Measured by: generator/ceiling.py, run on the cut pack (digest printed by the script)

## Leak sweep answers

`leak.py task192 --asof 2026-11-04` on the cut pack (target.zip a8212703 at the hand-off, db115928 after the stage-4 FIX_NOW pass, dbbb2dce after the lockout pin, the same five lines on each): REVIEW, no LEAK. One line per REVIEW line.

- **Sweep 3, DRP-04 carries 12 of 17 distinctive words of the committed call: harmless.** The shared words are the
  procedure's own subject in sections 5.1 to 5.4 (the overhead line patrol crew, the week, the feeder, the breaker,
  recloser or fuse whose zone is the stretch to walk, the taps fused off it), which is the WHAT the call is filed
  against and the prompt states in the same words. DRP-04 names no feeder, device, pole, date, phase, current or
  count; the call's own words (MLR-2, MLR-F2-52, R-2207, MLR2-P071, 9 November) appear nowhere in the pack's
  documents, and `checks.py` lands MLR-2 on the clean truth without reading any document.
- **Sweep 8, `device_id`, `device_type`, `upstream_device` (protective device register), `protective_device`
  (transformer list) and `Device` (OMS export): harmless.** The sweep matches the house word "device"; here it is
  the field's own noun for breakers, reclosers and fuses, and the key a utility's GIS and OMS hold connectivity and
  outages under. No column carries a flag, a truth, a seed or a marker. `metadata.json` declares it under
  `field_terms`.
- **Sweep 12, DRP-04 names column names verbatim (Bluffview, event, feeder, gust, point, station): harmless.** They
  are ordinary words of the procedure's sentences (the feeders of the Bluffview substation, a momentary
  interruption event, a gust of 40 mph, a metered service point, the airport weather station) that coincide with
  column names or values in the data files. The procedure names no file, defines no column and describes no
  layout; it is the utility's governing document in its own genre (issued 12 January 2026 with its revision
  table), filed for the WHAT: the definitions, the indices, the major event day rule, the patrol and the storm
  patrol.
- **The single-use test.** Every file has a use beside the call: the relay and recloser records and the SCADA log
  feed the asks' momentary and sustained counts; the register and the service points feed every index; DRP-04
  governs the indices and the storm patrol; the weather, lightning, line clearance and blinking-lights files are
  the storm patrol's, the line clearance programme's and the call centre's own records (the three distractors).
  No sentence was added to the pack in the stage-3 pass.
- **The stage-4 reader's realism notes.** The service point, transformer and tap fuse numbers were uniformly random:
  they now carry the customer system's and the asset register's numbering (service points set up before 2025 by
  substation in meter-route order along each feeder, services connected since in the connection series 8; transformers
  and tap fuses by substation along each feeder, with retired and cancelled numbers as gaps), drawn on their own stream
  so no record and no graded figure moved with them. The workbooks' 1980 zip entry timestamps are what Excel itself
  writes, and the lightning file's near-duplicate rows milliseconds apart are the return strokes of one flash, which a
  detection network reports one row each, tens of milliseconds apart at or near one point: both harmless.
- **The sentences the stage-4 passes added to DRP-04.** 2.2's last sentence (planned interruptions counted) and 2.7 (an interruption's times are the OMS's; interruptions the OMS does not record, as with every momentary
  interruption, take the SCADA log's, and a recloser's momentary interruptions its own event log's; a sustained
  interruption the OMS does not record runs from the opening that locked out its breaker or recloser, as the OMS
  times those it records, the trips and recloses before it part of it under 2.5 and not moving its start) file
  the WHAT of asks 4 to 6 in the procedure's own definitions, 2.5 for counting and 2.7 for times; none touches
  the call's records, and 2.7 points a careful reader at the openings the OMS never ticketed, which the ask sheet
  prices as found (the A3 re-site onto the later-found continuation tickets pays for it). Each is single-use
  only in the sense every definition is: it governs every index the procedure reports.

## Judge residuals

The third judge pass returned DETERMINISTIC, APPROVE on dbbb2dce; its three residuals are ruled here and nothing in the
pack changes.

- **(1) The second choice against the grouping width: closed by the data.** MLR-2's eleven spread 1.8 per cent and
  SYC-3's seven 0.9 per cent, while BLV-F3-52's phase B trips since August run 1,266 to 3,085 A, so the call holds at
  every width tried (SF10) and SYC-3 stays second to a 3 per cent band (SF11). The optional DRP-04 sentence defining
  "one current" is declined: it would file the call's signal in the procedure and announce the move, and the
  solution's step 2 already states the plus or minus 2 per cent and the window for the graders.
- **(2) The legacy child tickets: derivable** from the SOE closes and the restoration-step sheets; the alternative,
  each child's customers out only from the child's own Out, is a clearly wrong reading (SF18).
- **(3) The momentary exclusion:** the literal 2.5 reading ("end in a sustained interruption", at the outage
  system's minute) reproduces the golden, as SF17 records.

## Tried and rejected
- The loop-4 reader, cold on the re-drawn record, **missed the call**: it filed 550 at 50 per cent
  with 600 at 20, 500 at 12, the stored-code count's 300 at 8 and the golden's 450 at **6**. That is
  the first cold thread in this wave to go wrong on a call, and it matters for more than Gate F: the
  pair ceiling assumes a ladder that keeps all but one response off the call, and until a cold thread
  misses it the measured pair is an assumption rather than evidence. task190 was retired today on
  exactly that premise failing. Here it holds, so this build's ask arithmetic means what it says.
  The reader's route is the predictive-value family again, now with an extra step: it treated the
  partner and line codes as ground truth because they agree on 205 of 205 overlapping actions, and
  corrected only the monitor-only actions. Without that step it lands on 605, the 600 cell.
- The realism list from that read, held until the judge reports. **The worst of it is that a realism
  defect is generating a wrong route:** the partner and line codes agreeing on 205 of 205 overlaps is,
  in the reader's words, the most generated-looking statistic in the pack, because independent
  reporters never agree perfectly, and that perfect agreement is what licensed it to treat those codes
  as truth. Breaking the agreement moves the filer-confrontational count, so it is a figure-moving fix.
  Next: the audit covers 54 per cent of accepted May to August reports, 91 per cent in May falling to
  22 in August, and a desk double-coding half of everything is a validation exercise rather than a
  sample. That one is answered by framing rather than data, since the protocol can say what the
  exercise was, and no figure moves. The classifier reads as a relabeller instead of an instrument,
  its errors concentrated in three labels while two stay almost clean. Identifiers are gap-free across
  three files. The exception file reuses identifiers, about two rows per identifier across 308 rows,
  which is a key-uniqueness defect the hygiene battery would flag and which nothing declares. The
  tension index contradicts itself, labelling a rise from 56.3 to 67.2 as falling. The media coverage
  file is a literal expansion of the monitor's own config weights. And the report lags have no long
  tail at all, the press maximum sitting at 20 hours.
- Credit where the pass earned it: the surge now touches new ground, 66 municipalities to 112 and 214
  localities to 421, which was the reader's complaint last round and is no longer one.
- **(architecture 3, the realism pass of 2026-10-17) A hand-coding worksheet drawn as a fixed half of each round's window.** Two cold readers read the file as built rather than kept: exactly 1,000 rows split 420 and 580, exactly 50.0 per cent of each round's pool, rows in identifier order with the coding dates running monotonically down the page, daily loads repeating, 47 notes from six stock phrases with ten of them on rows no second coder had seen, eleven of eighteen changed decisions ending on the classifier's own code, agreement flat at 74 to 79 per cent across all four coders, and not one report the desk could not code. The desk now has its own random stream (`SEED_DESK`), its own calendar and its own capacity: the lot is the sum of what its coders got through on the days they sat, which is 1,064 rows, 68.4 per cent of round one's pool and 43.5 per cent of round two's; the file is written as the desk's journal, by round, coding day and coder, so consecutive rows run up the identifier half the time (0.505); the daily load runs 5 to 45 over 58 coding days; a note sits only on a row a second coder read or a row nobody could code, composed from two pools into 35 distinct texts on 63 rows; a second coder reads a row far more often when the report is one the classifier also got wrong, so 15 of the 19 changed decisions end on a code the classifier did not give; each coder reads an ambiguous report as a neighbouring code of the same kind at their own rate, so exact agreement runs 0.614 to 0.737 across the four; and eight rows carry no manual code at all, with the dictionary and protocol 4.5 saying what an empty code means and SF27 asserting that reading those rows as ordinary codings gives the same call. **What it cost:** the audit's four cells, and therefore the committed count and every figure downstream of them, had to be re-tuned (see the entry on the design point below); the protocol's 4.5 now says the file carries the manual code "onde a mesa o conseguiu fixar".
- **(architecture 3, the realism pass) The six weeks with no coding in them.** `desk_calendar` worked each lot in the fixed 34 days before its own close, so round one coded 17 May to 19 June, round two 7 August to 9 September, and the 48 days between them were empty although round two's lot held reports dated from 20 June: either the desk worked that stretch or the round's dates were wrong. Each round now opens its lot the working day after the previous round closed and works it to its own close, with the association's holiday month thinner rather than empty and the odd catch-up Saturday. Coding now runs 4 May to 8 September with no gap longer than seven days and coding days in every month from May to September, asserted (`real.coding_calendar_has_no_hole`, `real.coding_covers_every_month`, `real.round_opens_on_the_previous_close.R2`). **What it cost:** the desk draws from the reports that had arrived by each coding day, so the lot is weighted towards the early part of each window: May gives 458 of the audit's rows and August 107. That is the stated process working, it strengthens rather than weakens the engine (the audit's prevalence sits 1.56 times the record's), and it moved every audit cell.
- **(architecture 3, the realism pass) The reposted August load keeping its original delivery stamps.** The second load of the August partner file carried the same `carimbo_entrega_utc` as the first while the import log said it arrived on 14 September and the ingest counter counted it there, so the only thing that marked the reload was the load id. The portal now stamps the second load's rows on the day the log says they arrived, spread across that morning, which is what actually double-counts a month. **What it cost:** the two stamps a reposted report now carries open a reading the pack had not had, so the dictionary's `carimbo_entrega_utc` line makes the delivery moment the first load's, SF28 carries the row, and the alternative is asserted to move the partner route's median from 1,385 to 1,450 minutes. The device is stronger for it: D1 now moves the A2 median as well as the counts.
- **(architecture 3, the realism pass) One clock profile across the three routes.** All three routes drew the action's start hour from one shared distribution, so the press monitor, the partner network and the public line filed on actions with the same mean hour of 14.0 to 14.2, the same standard deviation of 3.6, the same 07:00 floor and the same 21:55 cap. Each route now has its own hours and its own shape: the monitor's titles cover the set-piece daytime actions (mean 13.55, 07:00 to 21:59), a partner organisation writes up what its own people were at during their working day (11.76, 08:00 to 20:59) and the public line is where the evening and night-time blockades arrive (15.68, 05:00 to 23:59), asserted pairwise (`real.route_clocks_differ.*`, `real.route_clock_ranges_differ`). **What it cost:** the start hours move every receipt stamp, so the three route medians and the two partner columns moved with them.
- **(architecture 3, the realism pass) Start minutes on a quarter-hour lattice.** 52 per cent of start minutes were exactly a quarter hour, 26 per cent were one of eight other five-minute marks and the rest were uniform, which a reader read off as a lattice with a small second group ending 05, 10, 25 and 55. The minute is now drawn from a distribution with a quarter-hour mode and a shoulder around it: 44 per cent on a quarter hour, 22 per cent on another five-minute mark, 22 per cent within four minutes of a quarter hour and 12 per cent anywhere, which puts 45 per cent on the quarter hours, every one of the 60 minute values in the file and 29 per cent off a multiple of five, asserted (`real.minute_mode_is_the_quarter_hour`, `real.minute_lattice_broken`). **What it cost:** nothing beyond the stream: no graded figure reads a start minute, and the medians move only through the stamps.
- **(architecture 3, the realism pass) A surge that doubled the volume without touching new ground.** Monthly actions roughly doubled from September while the municipalities touched moved only between 117 and 119, because every action drew its municipality uniformly from the gazetteer's 119. The geography is now the register's own: each municipality carries a share of its district's standing contention (the district capital and the two island capitals most, a long tail of small ones), each dispute theme falls on the territory it belongs to, and the two themes the autumn brings, the transmission network and the fire season, run the municipality size the other way, because the lines and the burnt ground are where the people are not. The spring and summer months now touch 82, 83, 86 and 88 municipalities and the two autumn months 117, thirteen municipalities have no action in the register before 5 September, the interior districts' share rises by 37 per cent while the metro districts' falls, and Beja doubles, all asserted (`real.geography_moves_with_the_volume`, `real.register_does_not_start_saturated`, `real.surge_reaches_new_ground`, `real.surge_concentrates_in_districts`). **What it cost:** the fortnight municipality counts, the graded column of the A1 table, fell from 100 to 119 to 63 to 112, and the protocol's dispute-theme list went from fourteen themes to ten so that a theme-stratified correction has strata big enough to be worth computing (see the design point below). The earlier bulletins' three figure collisions with graded fortnight rows went with it.
- **(architecture 3, the realism pass) Re-tuning the design point on the coding desk's stream alone.** The first attempt searched `SEED_DESK` for a draw in which either round's cells alone land in the call's cell: 7,200 desk seeds gave one hit and none with both rounds inside the band. Measured, the reason is structural: the desk draws more than half of each round's pool, so a round's estimate is pinned by that window's own realised rates and the desk's draw only jitters it by about 30 actions. The two rounds' anchors are a property of the action layer, so the search moved there: 12,000 action seeds were screened on the pooled call, the two round anchors, the stratified family's anchors at seven reference desk draws, the seven wrong routes' cells, the record's dispersion in both regimes, the three medians and the fortnight ties, which gave twelve candidates, and the desk's own stream was then searched on the best of them. The shipped point is action seed 10461 with desk seed 4. **What it cost:** the two sub-routes of rung 1 now share the 250 cell while rung 0 sits at 300 and the audited prevalence at 700, so the ladder is six cells rather than the five it was, and rung 4a (the coded count scaled by the recall, 615.64) shares the default path's 600 cell, 1.1 actions from it, which is the one place the ladder is worth less than a cell. Against that, every route in the right family is now at least 7.7 actions from its cell edge where two of them used to sit 0.8 and 4.6 from one, and the family gap is 3.3 sigma where it was 2.7.
- **(architecture 3, the realism pass) The classifier's nominal rates at 0.46 and 0.0295 with a fourfold fall in the confrontational share.** The re-centring measured the candidates' positions as functions of the nominal recall, the nominal false-mark rate, the level of the confrontational share and its fall across the period, and the combination the ladder needs is a recall near one half, a false-mark rate near one in fifty, an audit prevalence near 15 per cent and a record prevalence near 10 per cent. The shipped values are 0.46 and 0.023 nominal, measured at 0.4783 and 0.0201 on the shipped worksheet, with the confrontational share falling by a factor of 2.6 rather than 4.2 so that the audit's prevalence stays inside the cell the audited-prevalence route needs. **What it cost:** nothing in the record's story, which still has a confrontational spring and summer and a peaceful autumn mobilisation; the marked rate still halves across the cut (8.8 against 4.3 per cent, p = 3.0e-09).
- **(architecture 3, the realism pass) The monitor and the public line stamping receipts at any hour.** With the start hours re-drawn, one press report landed at 23:21 on 30 October, 38 minutes from the period's edge, and the route table's zone-invariance assertion caught it: a solver who read the receipt stamps an hour out would have counted a different triple. The association's own intake hours, 06:00 to 23:00, are now in the monitor's configuration, and whatever lands outside them is written at the next collection, so no receipt stamp sits within an hour of either edge and the triple survives every zone in the pack by construction rather than by luck (`SF26.route_window_zone_invariant`). **What it cost:** the night's arrivals pile into the morning, which is what a real intake does, and the three medians moved with it.
- Loop 3, the route table shipped with no window. The loop-2 judge computed three windows off the same sentence (received in the period 4,346 / 1,204 / 945, received to the 6 November extract 4,658 / 1,313 / 988, reports of actions dated in the period 4,348 / 1,215 / 945, with the partner median moving 1,327.0 / 1,312.0 / 1,331.0), so the ask was an open fork. Closed with one `convencoes` row fixing the basis, scoped to the route figures: the partner table's own row beside it stays action-dated, so the two conventions read as the two different things they are. The row is load-bearing, not a giveaway: delete it and the three windows compute again, and it says nothing about the repost, the placement or the medians. Measured zone-robust before it was written, the nearest receipt stamp sitting 1.25 hours from a window edge.
- Loop 3, five figures graded that the prompt never asked for. The decomposition (4,200 / 427 / 302 / 30 / 1,000) and the per-fortnight shaded series left block 4; the decomposition stays in Critical Components, where it is a component of the call rather than an answer the rubric owes, and the shading stays in the bulletin as the house's own context, described but not graded.

- The seed's own architecture, a filed definition of a campaign plus a verification subsample that
  blesses one reading of it: the definition makes the count rule application and the subsample is a
  certified replay, both of which the client's rules ban as the decisive step. Re-rooted at the draw.
- Recovering the number of operations from a periodogram of the daily action counts: the number of
  peaks depends on the window, the detrending and the significance threshold, so the count would not
  be determinate. Replaced by the intervals read off the locations each operation alone touches, which
  needs no threshold.
- Letting the institute's flag file group the location-days into episodes: that ships an artifact that
  answers the decision question wrongly, which Gate G forbids. The flag file flags days and groups
  nothing.
- (architecture 2) A confrontation risk filed with an eight-week horizon from each episode's opening,
  the cohort the episodes opened in a window that ends a week before the extract: measured on the
  model, the complete-case share over the episodes with a full eight weeks of follow-up is an unbiased
  estimate of the same quantity and lands within a point of the golden, so the easy route reaches the
  answer. Replaced by the whole-life estimand.
- (architecture 2) Grading the share to one decimal: the weekly and fortnightly readings of the
  decisive estimate give 17.05 and 16.99 against the daily 17.03, which a one-decimal figure splits.
- (architecture 2) A ranked watch list of the live episodes by remaining confrontation risk: the
  remaining risk is a monotone function of an episode's age alone, so the ranking degenerates.
- (architecture 2) The whole competing-exit architecture, designed, built and gated: on the remote
  merge of 2026-10-17 task266 arrived with the same mechanism in other nouns, and task157 arrived with
  the same gap, decisive pattern and decision type while task190 v2 took the stakeholder role.
  Re-rooted at the draw rather than shipped into a clone finding.
- (architecture 3) Correcting the count by the classifier's precision alone, or by its recall alone:
  each carries one of the two measured error rates and lands two cells away, which is why both are
  rungs rather than the answer.
- (architecture 3) A double-coding sample that verifies every classifier positive and a sample of its
  negatives, which is what a real quality desk draws: it makes the predictive values the design-exact
  quantities and the sensitivity the derived one, which inverts the decisive step and leaves the
  weighting of the two strata arguable, so each round draws at random from the reports entered since
  the previous close and 4.5 says so.
- Dating the desk's hand coding forward from each round, the round day plus nought to eight days: the
  November round then codes reports after the 6 November extract, which the leak sweep caught.
  Replaced by the desk's own working calendar before each round's close, with the batch worked in the
  order the reports arrived.
- Partner rates of 5.25 and 6.15 euros for the amended agreement: the paid reports came to exactly
  892.50 euros, so a solver rounding half up and one rounding half to even would file different euros.
  Replaced by rates that land every total at least a quarter of a euro from its edge.
- **(architecture 3, the stage-4 determinism finding of 2026-10-17) A correction forced by nothing but
  the shape of the record, with a flat confrontational rate and a validation sample spread over the
  whole period.** The judge found eight routes standing between 226 and 237 on a golden of 234: a
  pooled predictive-value correction, its month-, theme- and round-stratified variants, the sample
  prevalence, a continuity adjustment, the hand-code-where-sampled route and the pooled Rogan-Gladen
  the golden used. Measured, the two families differ by less than their own sampling error (the gap's
  mean was 7 against a standard deviation of 24) because the two are algebraically the same quantity
  when the validation sample is representative of the population it corrects, and that sample's
  coverage varied while its prevalence did not (p = 0.81 across months). Nothing in the record could
  pick one. Re-rooted inside the architecture, not away from it: the audit's window now stops before
  the autumn surge, the confrontational share falls fourfold across the period, and the two families
  are 30.8 per cent apart at 2.78 standard deviations of the gap's own sampling error.
- **(architecture 3) Keeping the validation sample at 2,600 rows over 59.7 per cent of the period's
  accepted reports.** The reader's verdict was that no desk produces that file in that shape, and the
  arithmetic agrees: at the audited batch's size the stratified variants of the right family sit
  within a per cent of the pooled one, so they cannot be told from it, and the hand-code-where-sampled
  route closes to within 6 per cent of the answer. Measured over the repaired design, the audit has to
  sit between about 900 and about 1,350 rows: below 900 the theme-stratified route with a pooled
  fallback leaves the answer's cell, above about 1,400 the hand-code-where-audited route comes inside
  6 per cent of it. Built at 1,000 rows in two rounds, 23.8 per cent of the period's accepted press
  reports and about 500 a round, which is what the reader put a real desk's own output at.
- **(architecture 3) Grading the count as a whole number.** The audit's four cells carry a sampling
  standard deviation of 57.4 actions on the answer, so a whole number claims 0.2 per cent precision on
  a figure whose own standard error is 12.7 per cent, which is the arithmetic task190 paid for.
  Replaced by the nearest fifty actions, 0.87 of that standard deviation, with every candidate route's
  cell asserted.
- **(architecture 3) Cutting the audit to a few per cent of the record.** Measured rather than argued:
  the answer's relative sampling error is about 1.5 over the square root of the hand-coded
  confrontational reports, and that count is the audit's row count times the audited prevalence, so an
  audit of a few per cent of 4,200 press-reported actions would hold about a dozen such rows and carry
  a standard error near 30 per cent, at which no granularity separates the two families and no cell
  holds the right one. The record's volume cannot be raised to buy the coverage back without putting
  more than fifty contentious actions a day into a country of ten million. The audit is therefore
  sized by what it has to measure, 1,000 rows, and the coverage that follows, 23.8 per cent, is
  reported rather than disguised.
- (architecture 3) A single nine-day burst per round with four coders at equal loads and no second
  codings: the reader read it as a file built to be read by an analyst. Replaced by the desk's own
  working calendar, 65 coding days at loads from 1 to 41, unequal coder loads of 345, 290, 212 and
  153, 78 rows sent to a second coder with the desk's decision recorded on each, and 49 coding notes.
- (architecture 3) A classifier that relabels at random: the reader measured its agreement with the
  hand code at 21.8 per cent against 19.8 expected by chance, which reads as noise rather than an
  instrument. Replaced by a confusion matrix over the protocol's eight codes with a strong diagonal
  and neighbour confusion, which agrees with the hand code on 64.2 per cent of the worksheet's rows
  and confuses a code with a neighbour more often than with a distant one, both asserted.
- (architecture 3) Action start times on the quarter hour between 08:00 and 19:59 with nothing over
  lunch, no weekday to weekend difference, partner deliveries flat across the 24 hours and line lags
  bounded at 42 to 206 minutes: every one of them a tell the reader read off the pack in one pass.
  Replaced by start times from 07:00 to 21:59 with 82 per cent of minutes on a multiple of five, a
  working week in the daily counts, partner deliveries inside each organisation's working day, and
  lognormal lags, all asserted.
- **(architecture 3) The earlier bulletins' note that two dispute themes entered the register with
  the autumn mobilisation.** "O boletim de setembro registou a entrada de dois temas de disputa que o
  registo ainda nao tinha visto, energia e redes e florestas e fogos, com a mobilizacao do outono."
  Two independent cold readers named it, in the same company as 3.3, 4.5 and the classifier's
  stability line, as part of what lets a solver see that the autumn is unmeasured by the audit. Cut.
  It was the only optional member of that company and the pack loses nothing by it: the surge is
  visible in the monthly action counts, and the two themes are visible as codes that appear in the
  record only from September. The protocol's thematic table keeps both codes, because a code list is a
  code list and says nothing about when either theme entered the register. **Why the other three stay,
  so nobody cuts them later:** 3.3 files the estimand, so it is the WHAT; 4.5 with the dictionary's
  round definition files the sampling frame, which is also the WHAT and which `determinism-check` §1
  requires; and `config_monitor.json`'s "alteracoes_no_periodo: nenhuma" is a decisive fact Gate B
  requires shipped, because without it the classifier's error rates would not transport either and the
  problem would have no answer at all. Cutting the sentence moved no figure: `figures.json` is
  byte-identical across the rebuild and only the bulletins PDF's own bytes changed.
- **(architecture 3) Grading the fortnight's partner column as a share of the fortnight's actions.**
  The share put a one-decimal percentage in thirteen graded cells, and `determinism-check` §3 says
  never grade a percentage near a one-decimal edge, flatly, without an exception for a filed rounding
  path. Filing the path closed the one route that misprinted Q11, but managing one instance of a hazard
  class is not removing the class, and a judge reading the rule as written costs a determinism return.
  The column is now a count of the fortnight's actions the network reported. No data moved, so the
  call, the candidate table, the 2.8-sigma family gap and the audit's own draw are untouched; thirteen
  cells stay thirteen cells; and the difficulty is unchanged, because the count still turns on the
  action grain, the reposted load, the delivery lag against the action's own day and the gazetteer,
  measured at three misses on the cracker sheet. Exactly fourteen graded figures moved, the thirteen
  converted cells and P07's euro total, confirmed by diffing `figures.json`.
- **(architecture 3) A cracker sheet measured by hand.** Two builds in this wave shipped a sheet whose
  figure was the complement or the mirror of the truth, and the gate that reads the sheet cannot tell.
  The sheet is now the printed output of `generator/cracker.py`, which runs each named wrong path
  through `golden.py`'s own readers on the shipped bundle and exits non-zero if any row's cracker
  figure equals the golden.
- **(architecture 3, the author's pre-ship pass of 2026-10-17) Measuring a share's distance to its
  rounding edge as the distance to its printed value.** `checks.py` computed `abs(t - round(t))` on the
  share in tenths of a point, which is the distance to the middle of the printed cell and not to its
  edge, so it named Q9 at 0.0129 as the tightest when the real tightest is Q11 at 0.0013 and Q9 is
  comfortably clear at 0.0371. The judge found it. The check now computes `(0.5 - abs(t - round(t)))/10`
  and reports every one of the thirteen, and the seed hunt that had optimised the wrong quantity is
  superseded by filing the rounding path instead (axis 10). A bar of 0.010 points on all thirteen is
  reachable, 27 of 360 pack seeds clear it with no two-step drift, but reaching it means a different
  `SEED_PACK`, which re-draws all 69 graded ask cells, the audit's own draw and therefore the call, and
  voids the judge's reproduction table; held for the author's call rather than taken.
- (architecture 3) P07's rate at 6.15, which put its euro total at 731.85, 0.35 of a euro from its
  edge and the tightest of the seven: moved to 6.10, which lands 725.90 and 0.40, the clearance the
  other six have. Only that one graded figure moved, confirmed by diffing `figures.json` across the
  rebuild.
- (architecture 3) Leaving "the euros paid under its data agreement" to clause 6.2. Two independent
  threads reached two values on the same reading, 7,337.90 against 7,410.85 and P02 at 2,493.05
  against 2,504.95, because 6.2 pays a late delivery with the period it was delivered in and whether
  that excludes it here is one inferential step. Closed in the asking sentence rather than in 6.2,
  which sits next to the device: the ask now names the observable, the euros the agreement pays for the
  reports filed by the close. No golden figure moved, because the golden already computed exactly that.
- (architecture 3) Paragraph 4.5 saying each round draws from the reports entered since the previous
  round closed, while round two closed on 10 September and its batch stops at 31 August: the 305 press
  reports of 1 to 10 September were in neither reading and a close reader was left holding a
  contradiction, although the figure never moved because the dictionary's range is what controls. 4.5
  now gives each round a cut and a close, the batch runs from the previous cut to its own cut, and the
  round closes when the desk signs the batch off; the dictionary's `ronda` column states both dates for
  both rounds. Text only, no figure moved.
- (architecture 3) The dictionary saying the desk works the batch on working days while 56 of the
  1,000 rows carry a weekend coding date: the generator's own calendar already models the occasional
  catch-up Saturday, so the dictionary now admits it rather than the rows being moved. Text only.
- (architecture 3) Leaving each partner's own monthly return to be read as the delivered rows. The
  returns count a report by the month of its action and the portal stamps the delivery, so at a month
  boundary the two differ, P01's May reading 18 against 17 delivered. That is the pack's own basis
  difference and it is now a declared device in the ask sheet (D3) with the basis filed in the
  dictionary's description of the returns, rather than an accident a reader has to guess at.
- (architecture 3) Paragraph 4.5 closing on the desk's schedule, that the round the calendar puts in
  the autumn is done in the next reporting period: of the whole pack it was the one line nearest the
  signpost boundary, because its only function was to tell a reader that the autumn holds no audited
  report. Cut. The frame stays, which is the sentence saying what each round drew its batch from and
  over which period, and that is the WHAT the estimand owes; the coverage gap is visible in the
  worksheet's own dates and the uncomputability of every stratified route is asserted on the data
  rather than on that line. Dropping it moved no figure: `figures.json` is byte-identical across the
  rebuild and only the protocol's own bytes changed.
- (architecture 3) Three Azores municipalities in the gazetteer's "Ilhas" district beside the Madeira
  ones, with the clock offsets in no shipped file: a geography error of the pack's own making that
  left the medians open four ways. The gazetteer now carries "Acores" and "Madeira" as separate
  districts and the monitor's configuration states each one's offset and the 25 October change, which
  closes the medians and leaves the Azores hour as a device in A2 rather than an accident.
- **(architecture 3, the stage-2 re-measurement of 2026-10-21) The magnitude fix itself: widening the
  composition drop so the easy family sits further from the call.** Dead on the floor it spends. The
  drop and the margin on the nearest wrong rung are one quantity with two signs: sweeping
  `CONF_RATE_LO = CONF_RATE_HI / k` over k = 1.0 to 8.0 at the shipped surge, the reach `PV - RG` rises
  36.95, 89.56, 114.37, 139.19, **159.62 (shipped, k = 2.6)**, 180.05, 190.27, 197.57, 206.33 actions
  while the gap to rung 2 falls 180.10, 125.68, 105.57, 85.47, **68.91**, 52.35, 44.07, 38.16, 31.06
  and its ratio falls 1.3588, 1.2824, 1.2496, 1.2126, **1.1785**, 1.1423, 1.1245, 1.1103, 1.0919. The
  1.15x floor is crossed between k = 2.6 and k = 3.2, the gap falls under one printed cell by
  k = 4.0 (0.88 cells) and rung 2 shares the call's own printed cell at k = 8.0 (369.064 against
  338.000, both printing 350). Over twenty action seeds a setting, the floor passes falls from 20
  of 20 at k = 1.0 to 13 of 20 at the shipped point and 8 of 20 at k = 4.0. The shipped point is
  therefore already at or past the widest setting the floor allows, and the realism pass of
  2026-10-17 had already walked this dial down from a fall of 4.2 to 2.6 to keep a wrong route
  inside its own printed cell (its own entry above), which is this same trade read from the other
  side. `corr(reach, gap to the nearest rung)` = -0.5791 over the sweep.
- **(architecture 3, the stage-2 re-measurement) Widening on the volume axis instead, where the two
  separations do not trade off.** `ACTIONS_SURGE` 1.0 to 6.0 at the shipped drop raises the reach
  65.23, 82.77, **159.62**, 207.10, 250.98 actions with the floor holding (ratios 1.2027, 1.2306,
  **1.1785**, 1.1896, 1.2190), so it is the one axis that buys reach without spending the floor, and
  it is dead on Gate C: over 120 draws on that axis the licensed error-rate family is unanimous on
  one printed call in 5, going 2, 1, 2, 0, 0, 0 of 20 seeds at surges 1.0, 1.6, 2.45, 3.4, 4.5 and
  6.0. The axis that keeps the ladder splits the call.
- **(architecture 3, the stage-2 re-measurement) The architecture, on the identity behind both of
  those.** `PV - RG = N (p - p_a) [(PPV - (1 - NPV)) - 1/(r - f)]` holds to 1.3e-13 at every seed, so
  the reach the ladder stands on **is** the difference between the record's own marked rate and the
  worksheet's own marked rate, times a constant of the four cells. Both are one group-by on a shipped
  column (`codigo_acao` on the item log, `codigo_monitor` against a non-empty `codigo_manual` on the
  worksheet), so the exchange rate is fixed by arithmetic rather than by tuning: 26.90 actions of
  reach per sigma of the window comparison at the shipped point, 25.29 to 48.00 across the drop axis.
  Counted over the two axes at twenty action seeds a setting, 245 of 300 draws give a printed
  cell of reach or more and 66 leave the window comparison insignificant, 22 do both, and **0**
  of those 22 have the licensed family unanimous; the family is unanimous in 9 of the 300 and all
  nine sit where the comparison is significant below 0.05. **0** of 320 draws give reach, a
  unanimous family, the 1.15x floor and a mid-bin call together, and the three that give the
  first three are the shipped setting and two at surge 1.0. So every draw with reach and a quiet
  record forks the call and every draw that files one call announces the step: the dial's two
  ends are the same end, the failure is not magnitude and no magnitude fix exists. Re-root or
  retire, the author's call: this is architecture 3.
- **(architecture 3, the stage-2 re-measurement) Re-shipping this pack as it stands, independently
  of the screens.** `guard.py heart task192` now returns **BLOCK** where on 2026-10-17 it returned
  WARN with no BLOCK, because the corpus moved under it: `ban.role` on the `research_desk`
  stakeholder family, `ban.forum` on `trustees_or_governors` and `ban.forcing_event` on
  `vote_or_meeting` all against task266 (v1), now delivered or approved, and
  `test.same_driver_older` because the decisive gap, the decisive pattern and the Gate G mechanism
  all repeat task270 (v2, lineage) with no differentiation line on the card. The driver text is not
  the problem, its nearest neighbour on file sits at 0.06; the axes are. So the role, the forum and
  the forcing event have to be redrawn whatever is decided about the magnitudes, which is a second
  reason the number wants a re-root rather than a resumption. `guard.py validate` is clean (277
  cards, 0 invalid) and the pack itself is untouched: `verify.py` passes all 138 independent checks
  and `target/`, `golden/` and `target.zip` hash to what the ship recorded.
  `guard.py surface` is exit 0 with no BLOCK lines and no personas in the cut pack, and it now
  promotes **three** pairs for adjudication with task192 in all three, each at exclusion level
  with both sides delivered: task191 vs task192 at 0.101 (corpus pct 99, back to back, same
  decisive gap and same context-artifact type on the cards), task192 vs task193 at 0.100 (pct 98,
  back to back, same decisive gap) and task189 vs task192 at 0.101 (pct 99, same decision type).
  On 2026-10-17 only the task191 pair was promoted, so two have appeared since. These are B-track
  card-axis matches rather than driver text, and they point the same way as the heart BLOCK.
- **(architecture 3, the stage-2 re-measurement) A seventh cell nothing in the pack rules out, found
  on the way.** A calibration model fitted on the worksheet with the classifier's label and a month
  term, extrapolated over the two months the audit never reached, files 504.483 and prints **500**,
  which is neither the call nor the default path and has no row in the candidate table and no `cand.*`
  assertion. Without the month term the same model reproduces the default path exactly (614.530). It
  is a construction a competent analyst would use and it is an open Gate C candidate on the shipped
  pack, which the loop-4 judge never tested; recorded here because it would have to be closed by any
  repair and cannot be closed by a magnitude.
- **(2026-11-04) Architecture 3 spent, confirmed; the re-root to architecture 4 opened at stage 1 and no
  candidate cleared, so nothing was carded.** Architecture 3 (confrontational actions in an event record, a
  classifier corrected by hand-coded audits) was confirmed spent at the 2026-11-01 re-check (commit 91cee50):
  its seventh cell (a logistic fit of hand code on the classifier mark plus a month index, extrapolated over
  September and October) files 504 and prints 500 against the golden 450, and the sentence that would close it
  names what the decisive step recognises, so the fork is the stump (`stumping` 1.2). Its shipped pack
  (060f8959) stays at the portal, pending, and its card is marked `architecture_spent`. The architecture 4 draw
  screened 55 candidates across 13 task types (A4.1 to A4.55 below) on 2026-11-04, each against
  `guard.py mechanisms --objective anomaly-detection`, `guard.py slots` on the mechanism and the setting nouns,
  the default path, the swap, the survivor anatomy and the bin. The window moved during the pass: task461 v2 and
  task193 v3 registered at 03:18 and 03:21 UTC, which closed physical-environmental-sciences x
  anomaly-detection and environmental-monitoring-exceedance and opened energy-systems-utilities and
  human-factors-ergonomics (task194 v17 and task200 v6 left the last three). The three strongest are written in
  full first.
  - **A4.5, the storm overflow capacity fault (physical-environmental-sciences / environmental-monitoring-exceedance;
    prototyped, then banned against task193 v3).** Draw: a regulator's area team sends its one winter compliance
    investigation to the storm overflow whose own pass-forward capacity fell (a partly blocked throttle), read
    from event duration monitoring against the rain gauge network. Default path: each overflow's 2026 spills by
    the 12/24 count against its 2021 to 2025 counts, adjusted for its gauge's 2026 rainfall, dry-day spills
    screened, files the overflow whose rain-adjusted count rose most. Golden: the overflow whose spills now begin
    after far less rain (the rain before each spill's onset, 2026 against 2021 to 2025). Swap holds (rainfall
    runoff on dry-weather flow, a setting a blockage lowers, a tipping-bucket gauge, 12/24 counting). Anatomy
    answered on paper (no column holds the setting; the onset rain is a relation between the spill log and the
    gauge record; the count is the field's method; the published returns reconcile with it). Measured on the
    clean truth (scratchpad `cso/proto3.py`, 16 overflows on 6 gauges at 15 minutes, 2021 to 2026, six seeds):
    the onset family (rain in the 3, 6, 12 and 24 hours before onset, event depth to onset, its lower quartile)
    names the faulty overflow in 5 of 6 seeds at onset ratios of 0.44 to 0.51 against 0.73 to 1.71 elsewhere,
    but the rain-adjusted 12/24 count names it in 3 of 6, spill hours per unit rain in 4 of 6 and spill events per
    unit rain in 3 of 6. The easy route is a crude member of the same capacity family (`stumping` 1.1, convergence
    and reach are one dial), and the confounds strong enough to move it off the fault (a showery year, long winter
    spells counted in 24-hour blocks, a catchment that grew) move the onset family with it, because intense
    storms and wet antecedents also lower the rain an unchanged overflow needs to spill. Dead on the dial.
  - **A4.48, a PV fleet's hardware fault against soiling (energy-systems-utilities / grid-reliability-outage-analysis).**
    Draw: the O&M company's one repair crew to the site whose arrays lost output to a fault it can fix, when a
    new dust source soils another site. Default path: the IEC 61724 temperature-corrected performance ratio over
    the last 60 days, curtailment and outages netted, against the same weeks of 2025, files the soiled site.
    Golden: the ratio on the days just after the latest cleaning rain. Swap holds. Dead on `stumping` 1.1b:
    soiling read from the recovery after rain (the soiling ratio, RdTools' stochastic rate and recovery) is the
    field's own method for a site-wide loss in a dry spell, so the golden is the opponent's first move; the
    upper-quantile, recency and trend routes also read the clean state, so the dial fails as well.
  - **A4.44, wrong blood in tube against detection opportunity (human-factors-ergonomics / safety-incident-error-analysis).**
    Draw: which clinical area gets the 2027 electronic bedside labelling first, by how often its samples are taken
    from a patient other than the one on the tube, when a mislabel is caught only where the sample can be
    compared with an earlier, independently taken group of the same patient. Default path: detected WBIT per
    1,000 samples (the haemovigilance metric) files the area with the most repeat patients. Golden: detected WBIT
    per comparable sample, the emergency department. Swap holds (ABO and D groups, historical group checks, the
    two-sample rule). Dead twice: on the bin (about one WBIT in 2,000 samples leaves 10 to 25 detected events per
    area over two years, so the area ranking is seed-hostage at any plausible volume) and on the abstraction test
    against task200 v6 in the same task type (a safety rate re-measured on the subset of records each person's own
    history makes valid).
  - Environmental monitoring: A4.1 river phosphorus concentration-discharge hysteresis, spent (task249 v5's
    driver, task279's screen, landed by the field's hysteresis reflex); A4.2 reservoir manganese aligned to the
    turnover date from a thermistor chain, spent (the phase of a recurring cycle read from a continuous record);
    A4.3 autosampler carryover after high samples and A4.4 cross-contamination by non-dedicated purge pumps on a
    fixed route, Layer 1 carrying the stump (data validation, planted in effect); A4.6 roadside remote-sensing NOx
    with a thermal-window defeat strategy, task273 v2's re-weighting to the year's conditions by stratum, and the
    "same conditions" fork closes only by naming temperature; A4.7 accelerated monitoring after an exceedance
    inflating a sample mean, the fork (sample mean against time-weighted) closes only by naming the weighting;
    A4.8 ozone titration near roads, not an artifact; A4.9 fenceline benzene with a near-field source, the
    method's own correction and task201's wind-sector screen; A4.10 landfill gas probes under barometric pumping,
    task279's screen.
  - General statistics: A4.11 central statistical monitoring, low within-patient variability at a fabricating
    trial site, the client's own planted-defect example (copied readings); A4.12 Benford tests on expense claims
    with fixed-rate allowances, swap and task185's heaping; A4.13 Mahalanobis against univariate outliers, the
    library test.
  - Payment claims: A4.14 ambulance trips with no claim at the destination, swap (billed against actual distance
    reads the same for taxis) and the OIG's own audit; A4.15 capitated groups' encounters against their pharmacy
    and laboratory claims, task188 v2's driver; A4.16 coding intensity from diagnoses with no treatment evidence,
    a filed crosswalk executed (rule application, code semantics); A4.17 completion factors with one provider's
    faster submission, the grouping dichotomy (1.1c); A4.18 multiple-provider episodes counted by prescriber or
    by practice, the unit (WHAT screen); A4.19 provider-based billing after an acquisition, the outcome
    definition (WHAT screen).
  - Disease surveillance: A4.20 wastewater at a sewershed holding the regional hospital, task182's approved driver
    (a unit's level less its response to an external series) and the resident population is the WHAT; A4.21
    positivity with negatives reported in weekly batches, task181 v2's nowcast family; A4.22 a community cancer
    cluster drawn around its cases, task191's extremum against a null extremum; A4.23 community urine resistance
    under selective testing, task273 v2's re-weighting; A4.24 imported cases in a reproduction number, the field's
    reflex; A4.25 PMMoV normalisation at a works taking a pepper processor's effluent, planted in effect and an
    estimator choice.
  - Survey research: A4.26 chain drift in a scanner-data index, task463; A4.27 interviewer falsification from
    impossible travel between interviews, swap; A4.28 a stratum jumper's weighted impact, the surprise-stratum
    reflex; A4.29 a hot-deck donor reused across recipients, the imputation flag is a column; A4.30 mirror-trade
    asymmetry from goods in transit at the year end, time semantics and task68's world; A4.31 head-office
    allocation in regional statistics, task194's driver.
  - Banking fraud and AML: A4.32 bid rotation in a procurement ring, AD25 (task202's seed); A4.33 AIS dark gaps on
    financed voyages, swap; A4.34 mule deposits in bursts at one deposit machine, the aggregation reflex (fraud
    card 4); A4.35 cheque kiting across two banks, no float left to exploit in 2026.
  - Safety signals: A4.36 the Weber effect against older comparators, swap and reflex; A4.37 nocebo reports after
    a forced biosimilar switch, the stratify-by-switch reflex; A4.38 hot vaccine lots, age and week
    standardisation (reflex); A4.39 febrile seizures after co-administration, the co-prescribed-cause family.
  - Provider quality: A4.40 breast screening readers whose women's prior images were missing, the "same reading
    conditions" fork names the step; A4.41 surgeons' early learning-curve cases, task200's driver and the swap;
    A4.42 cardiac arrest calls and resuscitation decisions, the population of arrests (WHAT screen); A4.43 complex
    cases allocated to a senior surgeon by a multidisciplinary meeting, the meeting log one join from a column.
  - Human factors (open from 03:21 UTC): A4.45 drug diversion read within patient across nurses, swap and an
    individual accusation; A4.46 dispensing-cabinet overrides against the pharmacist's verification time, the
    population of inappropriate overrides (WHAT screen); A4.47 takeoff performance entered for the wrong weight or
    intersection, a column comparison (FMS weight against the load sheet) and a filed SOP (rule application).
  - Energy systems (open from 03:21 UTC): A4.49 a recloser's repeated self-clearing faults at one location,
    task183's driver; A4.50 a service reservoir's structural leak against an outlet meter's low-flow error,
    separable only by a fitted two-driver regression (Gate C), and the natural drop test is the field's named
    method; A4.51 a failing service connection from its own voltage against its own load, Ohm's law the reflex
    and the sibling-netted form task303's driver; A4.52 a peaking unit's failed starts against standby time,
    small numbers and the swap; A4.53 FLISR commissioning hiding sustained interruptions, a dated cutover in the
    register; A4.54 a reconfiguration moving customers behind a fault-prone spur, task194's driver; A4.55
    sympathetic trips on DER-rich feeders, task303's driver.
  - What the pass leaves: on every cell this objective holds, each decisive step screened here was the field's
    method, a WHAT (population, unit, comparison), a grouping, a crude member of its own estimator family (the
    dial), or a driver already on file (task182, task188, task191, task194, task200, task273 v2, task303). The two
    cells that opened during the pass (energy-systems-utilities and human-factors-ergonomics) were screened last;
    the next draw starts there, from what a file the question gives no reason to open pins (`stumping` Part 6),
    with the cheapest licensed member priced before the anatomy is written.

- **(2026-11-04, architecture 4 draw) The recloser repeat-fault design priced on the clean truth before carding**
  (scratchpad `rc/proto.py` to `rc/proto3.py`, 16 seeds). With the failing insulator firing 20 or more times a quarter,
  every count found it (the dial again). At six flashovers among realistic background rates (10 to 60 momentary
  operations a feeder a quarter) the same-phase, same-current group named it in 16 of 16 seeds (6 against at most 5
  elsewhere at plus or minus 2 per cent), but the change on 2025 named it in 10 of 16, the non-storm change in 9 and
  the phase-skew test in 2. The generator therefore carries the offsets real feeders carry (spring 2026 line
  clearance on the failing feeder, a 2026 squirrel year on another, single-phase laterals that concentrate faults on
  one phase, a short urban feeder) and the relays' stated 1 per cent current accuracy, and `checks.py` asserts every
  cheap route off the call.
- **(2026-11-04, architecture 4 stage 2 to 3) The fault-current strip chart dropped from the prompt.** The draw's
  prompt asked for one strip per feeder of the fault current each momentary operation recorded, coloured by
  phase: that hands the solver the decisive dimension in the deliverable's specification. Replaced by a scatter of
  each feeder's SAIDI against its MAIFI-E, the patrol's feeder marked.
- **SAIFI dropped from the asks.** Its only silent device was the sustained openings SCADA holds with no OMS
  ticket, and at realistic lockout rates those reach six or seven feeders in ten months, so a cracker executing
  the OMS kept most SAIFI cells. SAIDI keeps the same device beside the legacy child-ticket times, and CEMI-2 beside
  the continuation tickets.
- **CEMI-3 replaced by CEMI-2.** With realistic interruption rates CEMI-3 was zero on three to five feeders at
  the design points tried, so a blind nil response would have kept up to a third of the cells; CEMI-2 is zero on
  two.
- **A 2.5 beta threshold from 2025 alone was unstable as the filed value** (12 to 146 minutes across the
  realizations tried, putting ordinary storm days over it). The filed threshold is the 2.5 beta value or 1.8 times the
  largest ordinary 2026 day, whichever is higher (38.03 minutes here), stated in DRP-04 as computed from 2021 to
  2025, and every ordinary day sits under 0.6 of it (asserted).
- **Rate tuning alone could not keep the failing feeder ordinary on every cheap route.** At realistic background
  rates its eleven flashovers lead the non-storm counts, the damp-morning counts or the phase shares on most
  realizations (one seed in 40 passed every route at one stage of the acceptance set, scratchpad `a4gen/search_r6.out`). The competitors' signatures became the seasons those
  feeders are known for (North Yard 3's squirrel year, North Yard 2's wet-limb mornings, Bluffview 3's phase B
  taps), drawn at fixed counts with free times and places, and the design point is a fault-process seed chosen by
  a search with every acceptance test in code (scratchpad `a4gen/search.py`).
- **Design points 19207, 19211 and 19219 passed earlier acceptance sets and died on later ones**: 19207 and 19211
  on the major event day threshold and the CEMI zeros once the threshold was calibrated, 19219 because the
  failing feeder had the system's worst SAIDI (the worst-performing-circuit reflex, the asks' own index, would
  have landed the call) and its runner-up group borrowed an unrelated operation. 19268 passes every test,
  including the indices over the year and since August.
- **The coordinator's heads-up on task461 (external dependency) answered in the pack**: the protective device
  register carries the protection study's available fault current at every device, so "a fault's current marks
  its place on the feeder" is a shipped fact rather than outside physics; the call rests on the eleven recorded
  operations and needs no formula.
- **Momentary events counted per device were a fork against DRP-04 2.5**, which counts a customer's interruptions
  within five minutes of the first: three pairs of nested devices opened inside five minutes. The golden, the
  truth and the verifier now merge per customer (SF6).
- **(2026-11-04, stage 3) The first prompt shell, "Where should our overhead line patrol crew work in the week of 9
  November 2026", with `patrol_week46.xlsx`.** `guard.py surface` promoted task194 (same domain, subdomain,
  objective and decision type), whose prompt asks "Where should the leak detection crew work in week 46?" of
  `crew_allocation_week46.xlsx`, with "the runner-up and the gap between them" and "the crew's area marked". The
  shell is redrawn: a what question with no week number, `line_patrol_2026-11-09.xlsx`, "the second choice and
  what keeps it second", and a chart sentence opening "In reliability_2026.svg". A `which` question was tried first
  and dropped because the corpus holds that form at 38 per cent against the 30 per cent cap, then a `whether`
  question, dropped because it repeats task193 v3's form, one of the last two prompts (`guard.py heart`).
- **(2026-11-04, stage 4) Absorption read as any sustained start up to five minutes after an event's first trip.**
  The generator absorbed a momentary event's customers into such a start; DRP-04 2.5 ("end in a sustained
  interruption") and submission step 6 ("in the event's minute") read it at the event's minute, and the judge's literal
  reading kept two events the golden had absorbed (CTR-1 on 17 June, CTR-2 on 26 July). The generator, golden and
  verifier now absorb at the event's minute. The CTR-1 case was a fuse that blew two seconds after the recloser's
  first trip, across a minute boundary; the OMS now takes the start of an outage behind an operating device from the
  device's operation, so it sits in the event's minute and every reading absorbs it. The CTR-2 case is a second
  fault two minutes into a breaker event, which leaves the customers' first momentary interruption standing under
  every literal reading.
- **(2026-11-04, stage 4) A1 re-sited by a later OMS cutover.** With 2.7 filed the cracker finds the SCADA-only
  openings (A1 9 of 16, A3 11 of 16, 43.8 per cent of the ask weight kept). Moving the legacy layout's end from 31
  March to 1 June, 1 July or 1 August 2026 moved no cell: the window's stepped restorations sit in January and
  February and on the two major event days. The re-site went to A3 instead: the crews' later sweep finds more
  storm-damaged drops still dark after their device closed, each a service ticket at the minute the device closed,
  drawn on its own stream after the fault process so no protection record, weather file or main-call figure moves
  (cracker 37.5 per cent, pair ceiling 44.5).
- **(2026-11-04, stage 4 pass 2) An unrecorded lockout started at its sequence's first opening.** The second judge
  pass read 2.5's "part of the sustained interruption" as moving the start and said every ticketed lockout starts at
  the first operation; built, it moved seven SAIDI figures by 0.2 to 0.8. The OMS says otherwise: on all 25 ticketed
  lockouts whose first opening and lockout fall in different minutes it carries the lockout's minute (the other 56
  sit in one minute). The judge's table also matched the sequence's second opening, not the first (SYC-1 153.9
  against 154.0). Reverted to the lockout opening, and the fork closed with a sentence in DRP-04 2.7 in the
  procedure's own voice: 2.5 governs counting, 2.7 times.


## Architecture 2, blocked at the draw by the remote merge

Architecture 2 asked what share of the register's dispute episodes would have recorded a
confrontational action by the time they closed, with a quiet close treated as the other way an episode
ends rather than as an observation that stopped. It was drawn, designed, built and gated: 635 episodes
in the cohort, 89 with a confrontational action at the extract, 312 closed quietly, 234 still open,
and 108 episodes, 17 per cent, on the decisive estimate, against 89 on the recorded count, 141 on the
known outcomes and 178 on a product-limit survival. The pack carried 17 files in four formats and a
25,688-row item log, with 108 generator assertions, 99 independent checks in a verifier that read only
the bundle, two byte-identical rebuilds, `figures_check.py` exit 0 and `precut.py` at 0 FAIL and 0
WARN.

It is spent for one reason outside the build. The remote merge of 2026-10-17 brought in task266,
drawn the same day in sociology-demography, whose driver is that mechanism in other nouns, and the
clone check reads mechanisms rather than nouns; the same merge brought in task157, which took the
structural triple, and task190 v2, which took the stakeholder role. Competing risks against censoring
is therefore on this slot's banned list with the rest.

What architecture 3 keeps: the world, the three access routes, the settlement gazetteer, the partner
organisations and their agreements, the ask layer with its devices, and every pack writer that is not
about the decisive quantity. What it discards: the episode construction and its peace interval, the
whole-life cohort estimand, the four survival estimators, the ladder, the prompt, the goldens and the
submission. Its pack, zip, goldens, submission and metadata were removed from the task tree when the
draw was blocked, so that nothing a consumer discovers by name can be graded as this build's
(`reduce-house-fixes` H11); the architecture is on the slot's banned list and will not be rebuilt.

## Architecture 1, spent at stage 3 on measurement

The generator was written far enough to measure the ladder on the record itself, before any file was
cut. Two findings kill the architecture, and neither is a tuning problem.

**1. The default path has no parameter-free answer, and its parameter range covers the golden.**
"Group the flagged location-days that touch in time and place" is a single-linkage clustering, and its
one free parameter is the gap in days it tolerates. Measured on the record (748 location-days, nine
operations, reach 0.70):

| Gap tolerated | Components, no same-day link | Components, same-day link |
|---|---|---|
| 1 day | 673 | 65 |
| 2 days | 598 | 22 |
| 3 days | 562 | **9** |
| 5 days | 310 | 1 |

The count falls monotonically from 673 to 1 and passes through 9, so a solver who tunes the gap to a
sensible-looking cluster count can land the answer without the insight, and no parameter-free reading
of "contiguous" lands on a plausible count: the two parameter-free readings give 65 and 673, which
nobody files as a count of coordinated operations. The design note's 23 was never reproducible. A
ladder whose rung 0 is one live degree of freedom in the graded quantity holds nothing
(`stumping` Part 3), and the sweep over flag rules (seven variants, 196 to 602 flagged cells) moved
the component counts by two or three and never separated them from 9.

**2. The decisive quantity is not one the field estimates, so rule 1 fails on measurement.** The step
is recovering the number of arithmetic progressions in a union of them: per-settlement gcds of the
observed gaps return exactly `[4, 5, 6, 9, 11, 13, 17, 23, 29]` on the 20 settlements one operation
reaches, and nine distinct interval-and-phase pairs. That is signal processing, not conflict event
analysis: no monitoring institute estimates how many periodic processes generated its record, and the
swap reads unchanged with machines on fixed maintenance cycles in place of coordinated operations.
Exact lattices over six months is also the kind of structure a realism read calls constructed.

The architecture is spent. Re-root at stage 1 in the same number and objective. The world (a
Portuguese conflict monitoring institute, three access routes, a settlement gazetteer, partner
organisations under data agreements) is sound and can be kept; the decisive step cannot.

**Ruled out for the re-root, with the reason, so the new draw does not walk into one:**
- capture of one list measured on the overlap with another: task448's driver, spent;
- the selected extreme judged against the record of extremes at the same reach: task191, one build ago;
- a shared external driver with unit-specific lagged response: task182;
- composition against rate: task183, task125, task188;
- a count read before its records have arrived: task190, task457;
- an event entering the record only above a detection threshold that moves on a cycle: task180.

**How architecture 3 clears each of them.** The decisive step is none of the six: nothing is captured
from an overlap (the duplicate reports collapse to one action and the count is invariant to them,
asserted); nothing extreme is selected and no null of extremes is built; no external driver and no lag
appear; the count is a count with no composition against any rate, and although the record's own
composition moves across the period that movement is what rules a method out rather than the quantity
being compared; every report has arrived, the import log closes the one month that arrived twice, and
the gap is in what the classifier made of the reports rather than in the recording; and no detection
threshold exists, the action grain being filed and every accepted item carried.
- **(2026-10-25, measured) A blind reader landed the call exactly, took 92.5 per cent of the ask figures, and reproduced this note's whole ladder as its own list of rejected methods.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **450 confrontational actions** against the golden 450 (its exact 455 against the generator's 454.91), on 4,656 actions built as tema plus gazetteer locality plus occurrence day, and hit **98 of 106 ask figures**. It took the decisive step and said why: because the mix changed after the audited months it corrected the 271 press marks with recall and the false-mark rate only, `true = (marks - FPR x N) / (recall - FPR)`, "that correction does not depend on how common confrontation is, so it carries to the unaudited months". Then it listed, by figure, every rung this note designed: naive 320, recall only 616, times precision 269, audit prevalence 694, hand codes where audited 386. A theme-stratified cross-check gave 466, still rounding to 450.
- **(2026-10-25, measured) The seventh cell is CONFIRMED open by an independent reader.** Asked to fit the calibration model (hand code on classifier mark plus a month index, extrapolated over the two unaudited months) and to say whether anything in the bundle rules it in or out, the reader returned **504, reported as 500**, a different fifty-bucket from the call, and answered: **"Nothing in the bundle rules it in."** It argued against it on three grounds of its own (the audit stops in August, two themes appear only in September so no month or theme term can be fitted for them, and the month term is not significant at p = 0.088), but those are judgements a competent analyst could decide the other way, not a shipped fact. So the Gate C finding recorded above is not a paper worry: it is a reachable candidate on the shipped pack, it has no row in the candidate table and no `cand.*` assertion, and any repair of this number owes its closure.
- **(2026-11-01, the re-check under the new gates) Architecture 3 confirmed spent on the shipped cut; not repaired, not re-rooted.** The rebuild (`python3 task192/generator/build.py`, matplotlib installed into the container) reproduced the shipped target.zip byte for byte (060f8959) with 310 generator assertions and 138 independent checks green. The shipped cut fails three free gates: `leak.py` LEAK on sweep 12 (`protocolo_vigilancia_v4.pdf` names 11 of the data files' columns) and sweep 13 (`metadata.json` committed_answer carries 450); `precut.py` FAIL on SF27 (asserted in `checks.py`, absent from the fork table) with 8 survivor-anatomy WARNs; `guard.py heart` BLOCK on the inherited bans against task266 v1 and task270 v2 recorded on 10-21. voice-check PASS (WARN only on the corpus how-many quota), figures_check 111 of 111. The seventh cell was refitted on the shipped target with the pack's own loader: a logistic calibration of the hand code on the classifier mark alone files 614.530 (the default path), and with a month index added files 504.483 and prints 500 against the golden 450. Closing it needs a filed sentence separating a correction free of how common the class was in the audited months from one that is not, which is the property the decisive step recognises (stumping 1.2, the fork-is-the-stump test), so no closure is available inside this architecture and the leak repairs were not cut on a build the main call cannot ship from.
