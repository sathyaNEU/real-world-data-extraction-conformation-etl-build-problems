# task210 design note

Architecture 1, drawn 2026-11-04. Wave 8 of the sathay3012 backlog, Anomaly Detection and Diagnostics, seed AD33.

## Draw

**Why the world moved.** Seed AD33 is a data-centre battery's January FCR-D offer. Its only legal home on this
objective is `energy-systems-utilities/grid-reliability-outage-analysis` (the one energy task type that serves
Anomaly Detection), and task402 holds that domain and subdomain inside the live window: a probe card returned
`BLOCK ban.subdomain` against task402. No other client domain hosts a frequency-reserve task honestly (General
Statistics would be a relabel), so the draw moved to another client domain, world and dataset under the same
objective and number (CLAUDE.md, A stuck build is unblocked). What the seed's decision did is kept: one figure
committed by 10 December for January, a cap the per-unit consumption divides into, and a per-unit consumption
that concentrates in a handful of moments the averages hide.

**Card.** `cards/task210.json`. Pairing `physical-environmental-sciences` / `environmental-monitoring-exceedance`
(serves AD and DQ; tagged AD). Shape 04 (setting one dial: the predicted haulage level at every fleet size).
Decision `dial_setting`, unit count (articulated dump trucks). Gap objective then population; pattern none;
generators G14 (conditioned yield), G3 (record against operation), G13 (horizon); Gate G
`decomposition_attribution`; strategy `decomposition_attribution`; calibration `pilot_log`; context artifact
`filed_standard`; role `operations_director` (the quarry manager); forum `regulator_or_inspector` (the mineral
planning authority receives the working scheme); forcing event `statutory_or_regulatory_filing` (the January
working scheme, due 10 December under the planning permission); org family `manufacturer` (an aggregates
producer). People from `guard.py names --geo uk --seed 210`: Garry Fry (quarry manager), Maurice Russell (planning officer), Leanne Smith (acoustic consultant).

**The world.** Calderwick Stone works Ravensby Quarry, a limestone quarry in the north of England whose
processing plant sits about 450 m south-west of the village of Ulverthorpe. A Class 1 sound level meter at
monitoring location MP1 (Ulverthorpe Lane, free field, 1.5 m) has logged 15-minute levels (UTC, period-end stamps)
since May 2026. Three to seven of the haulage contractor's articulated dump trucks (ADTs) haul each weekday from
two of three faces. South and west face loads go down to the pit floor and either tip on the run-of-mine
stockpile there or climb Haul road 1 to the primary crusher hopper, its last stretch behind the plant compound's
screening bund. North face loads either drop to the stockpile by Bench ramp N, in the pit, or climb out on Haul
road 2, which runs over the original ground to the hopper with nothing between it and the Lane. The north bench
takes one or two trucks. Which face a truck works and where each load tips (the primary's demand, a slow walk
through the shift) are separate choices, so the face does not determine the route. In January the first bench of
the Phase 4 extension opens and all its loads go to the primary on the Phase 4 haul road, whose surveyed
alignment and levels put it over the same kind of ground at the same distances from MP1 as Haul road 2 (within
0.3 dB of passage geometry). The January working scheme must state how many ADTs go on that road; the noise
management plan holds haulage at MP1 to 44.0 dB LAeq,1h of the 45 dB limit.

**The decision.** How many ADTs go on the Phase 4 haul road in January 2027 (a whole number; the scheme's 4.5
loaded movements per ADT-hour converts a movement rate into trucks).

**The quantity.** The sound energy one haul movement on the Phase 4 road delivers at MP1 (one loaded trip to the
hopper and its empty return), which the 44.0 dB share's hourly energy divides into.

**The anomaly and its diagnosis.** MP1's loudest working hours of May to October are not its busiest haul hours:
they fall when north face loads went to the primary on Haul road 2. Every other movement (north loads to the
stockpile, south and west loads to either tip) runs in the pit or behind the bund. No ticket, column or note
records a movement's route; only each truck's loaded run (its first and last fix) read against the survey's face,
hopper and stockpile points shows it. The January road runs in the Haul road 2 state, so its per-movement energy is
the Haul road 2 movements' own, apportioned out of a record in which they are about one in 9 movements.

**Data-native sentence.** Which face a truck loads at and where each load tips change load by load with the blasting, the stocking and the primary's demand through the shift, and together they decide whether a movement climbs out on Haul road 2 over the original ground or stays in the pit or behind the bund, so the monitoring record is mostly screened movements and the loud ones are a minority no record labels.

**Abstraction sentence (written to be tested, not to be shipped).** The per-unit effect at a receptor depends
on a configuration state no file records, the forward plan runs wholly in one state while the record is mostly
the other, and the effect has to be estimated on the record's units in the forward state, identified from their
own position tracks against a survey of the ground. Against the approved builds: task182 (each bore's own lagged
response to a shared driver), task196 (two capture channels, one produced by the firm's own follow-up), task120
(a day's use as production less storage gain) and task187-style matched comparisons (turbulence is a recorded
ten-minute statistic there) are not this sentence. It is not writable against any approved build on file.

**Semantic screen against the nearest drivers** (`guard.py mechanisms --objective anomaly-detection`, one line
each on the insight it spends, then whether this decisive step is it in other nouns):
- task125: events from a steady part plus scheduled occasions that the coming schedule moves to another site. Not
  this: nothing here is scheduled or moved; the January road's state is read from geometry, not a calendar.
- task156 (forecasting): a response that scales with a fluctuating level read from a separate record. Not this:
  there is no exogenous level; the state is each movement's own route, read from its own track.
- task181: a shared upstream resource added risk to the cases it handled. Not this: no shared resource and no
  stretch of time; every movement is classified on its own.
- task182 v1: each unit's own lagged response to a shared driver. Not this: no driver series and no lag.
- task182 v3: one continuously running source's share of a measured total, with the nuisance measured outside the
  window. Not this: the sources are discrete movements, the nuisance (residual and plant) is measured inside it.
- task184 v8: inverting a saturating observation map per record. Not this: energy adds linearly; nothing saturates.
- task185: a conversion between two instruments sized at the value converted. Not this: one instrument throughout.
- task187: a shortfall read at matched spread of inputs. Nearest in spirit (condition on a state before reading a
  per-unit effect); the difference is that task187's state (turbulence) is a recorded ten-minute statistic and a
  matched comparison of units, while here the state has no column and is built per movement from a second file.
- task192 v1: distinct processes behind overlapping bursts. Not this: no repetition structure is used.
- task197: a unit's response measured over seconds while its output follows a scheduled trajectory. Not this:
  no response gain, no trajectory.
- task204: a transport rate from an unsteady balance across short windows. Not this: no balance or response time.
- task139 (forecasting): events accrue on the scale wear runs on. Not this: no accumulated use.
- task400 (root cause, in the window): a mine's collision warnings after a firmware change. Shares the setting's
  nouns (haul trucks, ramps) and nothing else; the pack's vocabulary is a small English quarry's, not a mine's.
- task182 arch 2 (archived): ranking noise monitoring positions by specific level after background subtraction.
  Shares the genre; its decisive step (the statistical background) is not used here, where the residual is netted
  as an ordinary covariate and the decision is a fleet size.
The decisive step is none of these in other nouns.

**WARN answers.** `repeat.gate_g` and `overuse.gate_g` (decomposition_attribution in 6 of the last 12): the label
is the honest one, since the decisive step apportions MP1's sound energy among movements by route state;
`method_or_model_selection` collides with task483 inside the batch (`test.same_driver`), so the label stays and
the strategy differs from all three window builds. `test.same_driver_older` against task122 v4 and
`test.same_puzzle_older` against task488 carry differentiation lines on the card.

**Slot screen before any harness.** `guard.py slots` on the setting nouns (quarry noise, decibel, sound power,
minerals planning, screening bund, map matching, dump truck, declared sound) returned nothing in this sense; haul
road returned task400 (setting only, above) and noise monitor returned task182 arch 2 (above). On the seed's own
setting nouns, deterministic frequency returned task197 and hour boundary returned task111, task117 and task119.

**The five go/no-go screens** (`generator/screens.py` on the clean truth, 24 redraws from the shipped seed
21038, asserted in `generator/checks.py`; every figure is the call in ADTs, the golden 3.52 on the shipped
seed's clean truth and 3.428 on the cut pack):
1. *Realistic levels, and the lever against every rival.* Working-hour LAeq,1h at MP1 runs 41.7 to 45.2 dB (5th to
   95th percentile, median 43.6); the operations' specific level tops 45 dB in 2 of 1280 hours and never by
   more than a fraction of a decibel, so the pilot record shows no breach of condition 17. The count separates the
   golden from every rival in 24 of 24 redraws.
2. *The golden's own method holds.* The core family (hour-of-day effects, wind toward MP1, blast hours out,
   residuals trimmed at three standard deviations) files the golden count in 18 of 18 redraws whose golden sits clear of
   its bin edge; the whole family (with the other routes lumped, and route-resolved BS 5228 and ISO 9613-2
   calibration) in 11 of 11 mid-bin redraws and on the shipped seed. On the cut pack the family spans 3.33 to
   3.81 movements-per-truck units against a bin of 3 to 4 (golden 3.428).
3. *The first look lands wrong.* The busiest pilot hour inside 45 dB at MP1, at 4.5 movements a truck: 8 trucks on
   the shipped seed, wrong in 24 of 24.
4. *The careful readers land wrong* (the coordinator's two constructing readers included): per-face calibration
   from the telematics load point or the shift report's faces 6; crusher tips against stockpile tips 8;
   BS 5228-1 Annex F from the register's declared 109 dB with standard screening road by road from the survey, hard
   ground 2 and soft ground 6; the same calibrated on the pooled record (each hour less its LA90) 1, ISO
   9613-2 barriers 1. Every route wrong in 24 of 24. Two readers added at the coordinator's review: the additive reader (face and tip as separate main effects, no interaction) lands 4 on the shipped seed (4.54) and is wrong in 23 of 24 (the one hit at a golden of 3.04); the loudest-hours reader (top 2, 3 or 5 per cent of hours against the rest on wind, the shift report's faces, trucks, blasts, hour, face movements, tip mix and the route state, calibrated per movement on the best separator) picks the route state itself in 18 of 24 redraws and on the shipped seed at all three cut-offs, and then lands the golden: that path is the decisive step taken, which is legitimate; in the other 6 it picks hopper tips and lands 7 to 9. With the route state off its menu it picks hopper tips (8 on the shipped seed) and is wrong in 24 of 24.
5. *Literal execution of the filed WHAT.* A haul movement as NMP 6.2 defines it, every movement alike, its energy
   apportioned from the record: 15 trucks on the shipped seed, wrong in 24 of 24. No filed sentence asks
   which pilot movements share the Phase 4 road's state.

**The filed WHAT** (the organisation's voice; no method): condition 17 (45 dB LAeq,1h specific level at MP1, 07:00
to 19:00 Monday to Friday); NMP 4.1 (15-minute LAeq, LA90, LA10, LAFmax at MP1, stamped at period end on the
logger's clock; the specific level of an activity is the level at MP1 attributable to it over one hour); NMP 5.2
(plant 37.5 dB; haulage held to 44.0 dB LAeq,1h); NMP 6.1 (each scheme states the ADTs allocated to its haul road,
set so the specific level of the scheme's haulage at MP1 at the scheme's haul rate is within the share); NMP 6.2 (a
haul movement is one loaded trip from the face to its tipping point and the empty return; the haul rate is trucks
times loaded movements per truck-hour); NMP 6.3 (whole trucks); the January scheme (the Phase 4 road's surveyed
alignment, all Phase 4 loads to the primary, 4.5 loaded movements per ADT-hour from the bench trial, haulage 07:00
to 17:00 with a half-hour break, the allocation left to be confirmed).

**Sources for the levels.** Declared sound power of 35 to 45 tonne ADTs under Directive 2000/14/EC of about 107 to
110 dB LWA, and BS 5228-1:2009+A1:2014 Annex C at 107 to 111 dB; the loaded climb runs 2.6 to 3.4 dB above the
declaration (the generator's 111.6 to 112.4 dB) and the empty return near 106 dB. Planning Practice Guidance,
Minerals, paragraph 021 for rural limits (45 dB at a quiet village edge is ordinary). Screening: BS 5228-1 Annex F
(5 and 10 dB) and ISO 9613-2 barriers; the generator's actual screening runs below the standard estimates (pit
7.2 to 8.4 dB, bund 3.6 to 4.8 dB, the bund hiding the cab but not the exhaust stack). Ground 3.2 to 3.8 dB and air
1.9 dB/km after ISO 9613-1 and -2. Cycle 4.5 loaded movements per ADT-hour on a short haul with face and hopper
queues (the pilot ran 4.6 to 4.8). Class 1 meter to BS EN 61672-1, free field to BS 7445-1.

## Default path

The field's own method sits at rungs 0 and 1: the specific level apportioned to the haulage as a whole, and the
BS 5228 prediction from declared sound power.

1. Read condition 17, NMP 5.2 and 6.1 to 6.3 and the January scheme: share 44.0 dB, 4.5 loaded movements per
   ADT-hour, whole trucks.
2. Read MP1's export, convert the UTC period-end stamps to local time, keep weekday 07:00 to 17:00 hours on haul
   days, and sum each hour's four quarter-hour energies.
3. From the telematics, count each hour's haul movements (loaded runs ending in a tip).
4. Fit each hour's energy at MP1 against its movement count (the intercept carries plant and residual): the energy
   of one haul movement at MP1, the specific-level apportionment an acoustician runs.
5. Divide the share's hourly energy by it for the movements an hour within the share, and that by 4.5.

Ends on: 15 ADTs
Golden: 3 ADTs

## Stump sentence

The default path files 15 ADTs because it apportions MP1's energy to the pilot's average haul movement, five in
six of which ran in the pit or behind the bund, while the Phase 4 road runs over the original ground as Haul road 2
does; only the route state built per movement (where the loaded run began and where it tipped, from each truck's
GPS track against the survey) isolates the Haul road 2 movement's energy, and that allows 3 ADTs, with 4 over the
share.

## Three rules

Task type: environmental-monitoring-exceedance (Physical and Environmental Sciences), source apportionment behind a monitored level, tagged Anomaly Detection: the loud hours are separated from the ordinary ones and diagnosed.
Domain test: the sound energy one Haul road 2 movement delivers at MP1, estimated by apportioning each working hour's measured energy at MP1 among that hour's movements by route state, the specific-level apportionment of BS 4142 and BS 5228 practice; the share's energy divided by it sets the trucks.
Swap: "how many delivery lorries can a hospital's loading bay take within its noise share at the ward window" keeps the noise physics; put megawatt-hours or patients in place of decibels and route states and the logarithmic energy budget, the screening by ground and the apportionment by route stop meaning anything.
Layer 1: the logger's UTC period-end stamps and two Saturday battery gaps (the meter), one-minute fixes with GPS scatter in UTC (the fleet system), CRS84 survey coordinates (the surveyor's export), the foreman's face codes and remarks, a 10-minute weather record, free-text complaints, and on the ask side the June 2026 product renumbering, the Monday keying of portable-weigher collections, the controller's stop logged at boot and the loader's unordered buckets; nothing is planted and none moves the call when handled.
Layer 2: decomposition and attribution: a per-unit effect conditioned on a state the forward plan runs wholly in, estimated from a pooled record whose state mix differs.
Decisive step: apportioning MP1's hourly energy to haul movements by route state, each movement's state read from its own loaded run against the survey, and carrying the Haul road 2 state's energy (not the pilot's average movement, a face's average or a standard prediction) to the Phase 4 road.
Not semantics: every field is read right on the default path (the UTC clock converted, loaded runs counted, the share, cycle and whole trucks read as filed) and it still files 15 trucks; the miss is the estimand of the apportionment (the average movement), not a misread field or code.
Not rule application: no filed rule says which pilot movements share the Phase 4 road's state; NMP 6.1 asks only that the haulage's specific level stay within the share, which every route claims. The enumerated family (pooled, per face, crusher tips, BS 5228 hard and soft ground, pooled-record calibration, ISO 9613-2) spans 1 to 15 trucks on the shipped seed; the standing family (route-state apportionment with hour effects, wind, blast hours out, trimming, lumped other routes, quarter-hours, route-resolved standard calibration) spans 3.33 to 3.81 in movements-per-truck units, every member 3 trucks; what rules the others out is loud: the survey puts the Phase 4 road on Haul road 2's ground, and the route fit gives a Haul road 2 movement several times any other.
Analyst test: a strong analyst converts the clock, counts the movements, fits the hour's energy against them and divides the share: 15 trucks, against 3; the careful variants file 6 (per face), 8 (crusher tips), 2 or 6 (BS 5228) and 1 (pooled-record calibration).
Estimand: NMP 6.1 and 6.2 in ravensby_noise_management_plan_rev3.pdf (trucks allocated to the scheme's haul road so the scheme haulage's specific level at MP1 at the scheme's haul rate is within the 44.0 dB share of 5.2; a movement is a loaded trip and its empty return; the rate is trucks times the scheme's 4.5), with 4.1 (specific level over one hour) and 6.3 (whole trucks); the scheme docx for the road and the rate.
No decoy: nothing is planted to be caught: no memo, prior estimate, draft allocation or stakeholder figure; the scheme leaves the allocation to be confirmed; the plant register's declared sound power is the declaration it carries for every machine, not a figure placed for the call; complaints and shift remarks use ordinary wording.
No certified replay: no certified or published figure is reproduced to recover a method; the pilot record is apportioned on its own.
Lesson: an effect per unit read from a pooled monitoring record has to be conditioned on the state the forward plan runs in, with each unit's state built from its own position track against a survey; no build on file teaches it (the abstraction sentence in Draw).

## Survivor anatomy

Actor: the haul movement has rows (one-minute fixes) but its route state, Haul road 2 over the original ground against the pit or behind the bund, has no column anywhere: it is a relation between a loaded run's first and last fixes and the survey's face, hopper and stockpile points.
Link: a spatial join with no key (each loaded run's ends to the nearest surveyed face and tip), then MP1's UTC period-end quarter-hours to the movements' tip hours; no file names a route and no sentence invites the join.
Reflex: the field's method sits at rungs 0 and 1 and files wrong here: the specific level apportioned to all haulage (15), BS 5228 from declared sound power (2 or 6), its calibration on the pooled record (1).
Back-test: the pooled fit validates: it explains the hourly record nearly as well as the route fit, its residuals show no pattern by hour or month, and the pilot's six or seven trucks ran inside the limit, so nothing says the average movement is the wrong estimand.
Second use: the telematics carry the ask's haul loads to the primary, the survey the hopper, stockpile and plant compound the asks read, MP1 the complaints review; no file is in the pack for the decisive step alone.
Shock: Haul road 2 movements are about one in 9 of the record, the loud hours are ordinary haul hours, and no unit is the pack's largest anomaly or present in one period only.
Pins: NMP 4.1, 5.2 and 6.1 to 6.3 and the scheme file population, outcome, window, unit and comparison; nothing names the route state, a grouping, the time base or a method.

## Readability screen

| Rung | What a reader needs to take it | Verdict |
|---|---|---|
| Rung 0, pooled average movement | MP1 and a movement count from the telematics | readable |
| Rung 1, BS 5228 from declared sound power | the register's 109 dB and the survey | readable |
| Rung 2, per-face calibration | the load point or the shift report's faces | readable |
| Rung 2b, crusher tips against stockpile tips | the tip point | readable |
| Rung 3 (decisive), route state per movement | each loaded run's ends against the survey's faces and tips, no column or note | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | haulage share | 44.0 dB LAeq,1h (NMP 5.2) | 45 dB less the 37.5 dB plant | 3 | same call |
| SF2 | haul movement | loaded trip plus empty return (NMP 6.2) | each passage a movement | 3 | same call (energy halves, movements double) |
| SF3 | hour | clock hour, LAeq,1h | rolling sixty minutes | 3 | same call (per-hour allocation) |
| SF4 | cycle | 4.5 per ADT-hour (scheme) | the pilot's measured cycle | 3 | same call |
| SF5 | logger clock | UTC, period end | local time | moves the fit | the export header "Logger clock,UTC" and NMP 4.1 |
| SF6 | fitting window | 07:00 to 17:00 (the haul) | 07:00 to 19:00 (condition 17) | 3 | same call |
| SF7 | whole trucks | the most within the share | nearest whole truck (4) | 4 | NMP 6.1 "within the 44.0 dB share" (4 trucks exceed it) |
| SF8 | Phase 4 road state | Haul road 2's (survey geometry) | site average | 3 | the scheme's coordinates against the survey |
| SF9 | January 2027 | each haulage hour | month average | 3 | same call (no calendar term) |
| SF10 | tonnes per haul load | belt tonnes from haul loads over loads tipped in the hopper | belt tonnes over loads | asks | the asking sentence "per haul load tipped into the primary hopper" |
| SF11 | running hour | crusher start to stop, the supply's loss a stop | as logged | asks | the asking sentence "per running hour" |
| SF12 | tonnes sold by product | net tonnes by the product charged on the ticket | product ordered | asks | the asking sentence "of each product as charged" |
| SF13 | week | Monday to Sunday by the day weighed, January days only | ticket date | asks | the asking sentence "by the day the lorry was weighed" |
| SF14 | month | calendar month of the tip, local time | UTC month | asks | same figures (no tip within an hour of midnight) |

## Ladder

| Rung | Route | Trucks on the shipped seed (clean truth) |
|---|---|---|
| 0 | pooled average movement (literal WHAT) | 15 |
| 0b | busiest pilot hour inside 45 dB | 8 |
| 1 | BS 5228 declared, soft ground | 6 |
| 1b | BS 5228 declared, hard ground | 2 |
| 1c | BS 5228 or ISO 9613-2 calibrated on the pooled record | 1 |
| 2 | crusher tips against stockpile tips | 8 |
| 2b | per face | 6 |
| 3 | route state per movement (golden) | 3 |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | weekday 07:00 to 17:00 hours on haul days, four quarters; the scheme's January haulage hours | C1, asserted (07:00 to 19:00 same call, SF6) |
| 2 Unit of account | the haul movement as NMP 6.2 defines it; trucks as NMP 6.1 | filed; SF2 same call |
| 3 Attribution window | a movement to the hour of its tip | C1 (quarter-hours and hours file 3) |
| 4 As-of dating | the pilot May to October 2026; the scheme of 27 November | filed |
| 5 Version basis | NMP revision 3; the survey of April 2026 | filed |
| 6 Denominator | the share's hourly energy over one movement's energy | filed (NMP 6.1) |
| 7 Weighting | hours equally weighted in the fit | C1 (trimmed and hour-effect fits file 3) |
| 8 Window length | the whole pilot | C3 (every month's fit sits in bin 3, asserted family) |
| 9 Boundary inclusivity | within the share means at or under 44.0 dB | C1 (no setting within 0.3 dB of 44.0) |
| 10 Rounding path | no intermediate rounding; trucks floored once | filed (NMP 6.3) |
| 11 Tie-break | none arises | C1 |
| 12 Maturity and censoring | incomplete hours (battery gaps) left out | C1 |
| 13 Order of operations | energy summed before the fit | C1 (dB-domain fits are rivals, not readings) |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | no duplicate fixes | C1 |
| 16 Identity normalisation | truck by telematics unit | C1 |
| 17 Netting against gross | plant and residual in the intercept | C1 (LA90 netting files 3 in the family) |
| 18 Dimensional units | energy in Pa squared seconds, dB re 20 microPa | units in the data |
| 19 Code and status semantics | payload state LOADED and EMPTY | the field's own values |
| 20 Integerisation | floor (within the share) | filed, SF7 |
| 21 Clause scope | condition 17 working day; NMP 5.2 haulage share | filed |
| 22 Forward window contents | January: Phase 4 road only, all loads to the primary | filed (the scheme) |

## Literal reader

Executed word for word: NMP 6.1 asks for the trucks that keep the scheme haulage's specific level at MP1 within
44.0 dB at 4.5 movements a truck; NMP 4.1 makes the specific level the level attributable to the activity over an
hour; the scheme puts every January movement on the Phase 4 road. The literal reader must estimate one Phase 4
movement's energy at MP1 from the pilot; the text is silent on how, so every licensed reading was computed (SF1 to
SF9, the family in screen 2): each files 3 or violates a quoted sentence (SF5, SF7). The easy answer (15) comes
from an easy method on the same literal estimand (the average movement), never from another reading.

## Oracles

None. No file states a per-movement energy, a route label, a screening value for any road, a recommended
allocation or the Phase 4 road's state; no file says "in view", "unscreened" or "line of sight" (asserted). The
register's declared sound power is a declaration, not a referee, and the scheme does not compare its road with
Haul road 2.

## Ask sheet

Two asks, each with two primaries from different families, blocks disjoint, on files the call never reads:
- Ask P (primary feed, May to October 2026). P1 tonnes per haul load tipped into the primary hopper by month (6
  figures), D5 scope: the loader's unordered buckets are reclaim fed to the belt (before the first trucks, during
  rain stand-downs) and re-handling that never reached it (over the haul's lunch break, while the primary runs the
  hopper down after five, through an outage, after the stop); only buckets in belt bins carrying tonnage are feed,
  evidence the loader log against the belt scale. P2 primary tonnes per running hour by month (6 figures), D4
  absence: a supply loss stops the crusher and the controller logs the missed stop at boot on the supply's return;
  the run ends at the network operator's "supply lost" time, evidence the interruption notices against the PLC.
- Ask Q (January 2026 sales). Q1 tonnes of each product as charged (7 figures), D2 version: the June 2026 list
  renumbered every code and 7.5 per cent of collections loaded another product than ordered; the old code-to-product
  pairing is read from the order book's majority and applied to every ticket. Q2 tonnes by Monday to Sunday week of
  the day weighed (5 figures), D8 clocks: portable-weigher collections were keyed the next Monday at the keying time,
  some vehicles' runs on one order keyed as one ticket with summed weights; re-dated by matching each Monday ticket
  to one portable record or a vehicle's day of records summing to it.

| Ask row | Cracker's route | Cracker value against golden | Verdict |
|---|---|---|---|
| P1 tonnes per haul load, six months | subtract unordered buckets logged while the PLC shows the crusher running | 34.1 to 37.2 t against 34.7 to 37.8 | miss |
| P2 tonnes per running hour, six months | PLC starts and stops as logged | 434.2 to 516.5 t/h against 441.2 to 523.1 | miss |
| Q1 tonnes by product, seven products | product from the order book (the finer key) | every product off by 6 to 383 t | miss |
| Q2 tonnes by week, five weeks | re-keyed tickets matched one to one on vehicle and net | every week off by 43 to 795 t | miss |

Full includer (notices every device, natural remedy): keeps P2 through the interruption notices, misses P1 (lunch
and run-down re-handling inside running), Q1 (gate changes) and Q2 (summed tickets): 25 per cent of the ask figures.
Mirror leakage: 0.0 per cent of ask weight
Pair ceiling: 35.4
Measured by: generator/ceiling.py (independent readers over target/, scored against figures.json)

## Tried and rejected

- 2026-11-04, seed AD33's world itself (a data-centre battery's January FCR-D offer): undrawable on this objective
  while task402 holds energy-systems-utilities/grid-reliability-outage-analysis in the window (`ban.subdomain`); its
  mechanism also sat near task197 (a unit's frequency response during scheduled ramps) and task125 (occasions a
  forward schedule moves).
- 2026-11-04, a nuclear site's fence-line gamma monitors at go-live, the alarm level set against rain-induced
  radon-progeny washout (prototype `proto_gamma.py`, `screens_gamma.py`, seeds 1 to 5, two climates): the golden
  needs a fitted dynamic washout model with call-out merging; event regressions with an antecedent dry-time term
  land 6 to 12 nSv/h off it and the first look sometimes lands near it, so screens 1 and 2 fail.
- 2026-11-04, occupational blood lead at a secondary lead smelter (January furnace shifts under the action level):
  its decisive state is a shared upstream resource (task181) or each unit's lagged response (task182), and a
  monthly AR(1) careful route sits close to the kinetic golden.
- 2026-11-04, a data centre's UPS battery strings on thermal age and a device fleet failing on uptime since the last
  reset: both are task139's wear-clock insight and task132's renewal, in other nouns.
- 2026-11-04, hydropeaking under a filed rating curve (downstream stage ramps at winter base flow): task156's
  response scaled by a level read from a separate record.
- 2026-11-04, darkness-relative crime hours, susceptible depletion, backlog draining, road salt, build-up and
  wash-off, immortal time, an extremal index and tide aliasing: each already screened dead in another slot's note
  (`guard.py slots`: task182 arch 8, task178 and task202, task174, task165, task121, task122, task178 and task194,
  task249).
- 2026-11-04, world 1 (a north crest road in view, a west crest road behind the bund, cycle 3.6): the face fixed
  the route, so a reader classifying days by face from the shift report or the blast register reached the golden;
  redrawn so north loads split between Haul road 2 and the in-pit stockpile ramp, the tip set by the primary's demand.
- 2026-11-04, the golden as Haul road 2 against every other movement lumped: the lumped coefficient carries the
  north stockpile movements and drifts with the face mix (0.2 to 0.5 of a bin above the route fit); the golden fits
  one coefficient per route (face and tip).
- 2026-11-04, six or seven trucks every day: total movements nearly constant, so the intercept and the other routes'
  energy were confounded and an hour-effects fit fell 2.4 dB below the pooled one (a negative coefficient); truck
  availability now varies (three to seven, half-day services, rain stand-downs logged in the shift report).
- 2026-11-04, wind at 1.6 to 2.1 dB on the haul: a chance correlation of wind with north days moved the wind-adjusted
  fit 0.7 of a bin; wind now 0.7 to 1.0 dB and the weather file stays a distractor.
- 2026-11-04, BS 5228 calibrated hour by hour on route-resolved predictions lands the golden: it takes the decisive
  step (each movement's route state), so it is a family member; the coordinator's pooled-record acoustician is the
  ratio of measured to predicted energy over the pilot, and lands 1.
- 2026-11-04, three trucks on the north bench: the operations' specific level topped 45 dB in 6 per cent of pilot
  hours (a visible breach of condition 17); the north bench now takes one or two.
- 2026-11-04, haulage levels on the dial graded to 0.1 dB: the golden family spreads about 0.2 dB, and a mid-bin call
  puts the call's own level near 43.5 dB, so no rounding holds every setting; the dial files each setting's verdict
  and the levels show only on the chart.
- 2026-11-04, ask devices a full includer remedies on notice (unpaired PLC starts, one-to-one re-keyed tickets, the
  order book's product, unordered buckets after the stop): re-sited into reconstructions (stops logged at boot,
  summed Monday tickets, gate changes, lunch and run-down re-handling while the primary runs).
