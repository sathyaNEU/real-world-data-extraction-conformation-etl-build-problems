# task156: a district council's pump station, whether a subdivision can connect in 2027 within the station's consented overflows (architecture 2)

Private, never ships. Architecture 1 (Millrind's 2027 paid moderation pool, a developer Q&A network's volunteer
reviewers carried on survival by tenure) shipped 2026-10-17, was returned by the portal on 2026-10-27 with both
responses on the call, and was reshipped the same day as loop 3 with its world, prompt and asks kept. The batch 1
triage of 2026-10-31 re-roots the slot in a new world: nothing of architecture 1 is carried (world, decision,
quantity, prompt shell, deliverables, asks and mechanism are all new), and its identity sits in the card's
`lineage` with its fate.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v2, registered 2026-10-31T18:27:04Z; architecture 1 (v1 loop 3, and v1 loops 1 and 2 before it) in `lineage`, its shell in `lineage_shells` |
| Domain / task type | `physical-environmental-sciences`, task type `hydrology-flood-frequency` (serves Forecasting): the deciding quantity is how often a pump station's capacity is exceeded under a long rainfall record, an exceedance frequency worked the way urban hydrology works it, by continuous simulation of a calibrated rainfall-derived infiltration and inflow model |
| Objective | Forecasting & Predictive Modeling: the station's average wet-weather overflows a year once the subdivision connects in 2027, a window not yet open, estimated the way the discharge consent states it (the network as it will be, run through the 2004 to 2023 record) |
| Shape | `other`: the call with the consent figure with and without the subdivision, the fitted infiltration components, a chart of the replay year by year against the limit, and row-set asks on records the call never reads (arithmetic in `## Shape` at stage 2) |
| Decision | `go_hold_or_stop`, answer unit `named_option`: connect in 2027, or hold the connection until the storage upgrade |
| Mechanism | population then time: the meter's 2024 to 2026 storms and dry days are not the population of days the consent's replay runs (Gap 2), and the decision is forward (Gap 1); generators G14 (conditioned yield: the infiltration a dry day and a storm drive is conditioned on the length of sewer below the water table, which the replay's wet years carry past anything the meter saw), G16 (the conditioned model chosen over one response per millimetre on storms it was not fitted on), G13; Gate G `forecasting`; strategy `forecast_method_backtest` (a rate stationary only in a constructed exposure, kilometres of sewer below the water table) |
| Layer 2 family / pattern | `forecast_uncertainty` (model choice on out-of-sample error); `own:submerged-length-conditioned-infiltration-chosen-out-of-sample` |
| Furniture | forum `council_or_assembly` (the elected district council resolves on the officers' report whether the subdivision connects in 2027), forcing event `other` (the developer's request under the development agreement to connect stage 1 from March 2027, which consent condition 8 makes the council assess), organisation family `local_government`, role family `capacity_planner` (the three waters operations manager assessing the station's capacity for growth), context artifact `monitoring_export` (the station's SCADA export the operations manager works from), calibration `realised_outcome_roster` (the station's overflow log, which both routes reproduce), opening `question-first`, question form `whether` |
| Spine | `pump_station_inflow_2024-2026.csv`, the station's SCADA inflow every 15 minutes for three years (about 105,000 rows, UTC), beside the council's rain gauge, the regional bore's daily groundwater level from 2006, the asset register's pipes with invert levels and the 2004 to 2023 hourly rainfall record; constructed for this build, no real dataset |
| Deliverables | `subdivision_connection_assessment_2027.xlsx` (the assessment), `council_report_subdivision_connection_2027.docx` (the officers' report to council), `replay_overflows_2004-2023.png` (the replay year by year against the limit) |
| People | drawn with `guard.py names --geo "New Zealand" --seed 156`: Aaliyah Beattie, Benjamin Gilbert, Anaru Boyce (roles fixed at stage 3; Sean McDowall passed over, his first name already on task105); the requester is in no file and not in the prompt |

**Guard answers (registered card, `guard.py check` WARN, no BLOCK, after rebasing on main).**
- Redrawn after the rebase: task191 and task250 were registered on main after this worktree's base, and with them in
  the window `committee_or_panel`, `purchase_order_or_contract` and `filed_standard` BLOCKed. The replacements are the
  honester labels: a subdivision's connection held back for capacity is a growth decision an elected council resolves
  on an officers' report at a scheduled meeting, not a staff panel's, and the file the operations manager works from is
  the station's SCADA export; the consent stays in the pack as the governing document.
- Redrawn in place at stage 3 (2026-10-31): after the PAUSED rebase the window before this draw held task306, task470 and task250 (task191 re-registered after it, task250's role family became operations_director), so `vote_or_meeting` met task306 and `operations_director` met task250. The forcing event is now `other` (the developer's request to connect, which condition 8 makes the council assess) and the role family `capacity_planner`, the honester labels; both values are clear of the builds drawn after this one too, so no later card meets a new collision.
- `repeat.question_form` against task250: the decision is a gate (connect in 2027 or hold to the upgrade), and a gate
  asks whether (`guide-to-prompt`); "whether" holds 10 per cent of prompts on file, under its 30 per cent quota, and
  the second-sentence opener ("the") and the deliverable set (docx, png and xlsx) differ from task250's.
- `test.same_driver_older` (population, G14, forecasting) is differentiated on the card against task134, task146,
  task165 and task173 v1, one line each naming how the driver differs. The redrawn labels are the honest ones: the
  first probe carried `validated_decoy` true and Gap 1 first, which BLOCKed on `two_layer.validated_decoy` and on a
  signature spent in five builds; the meter's own record refutes one response per millimetre for anyone who checks it
  against the high-water-table storms and the overflow log, so `validated_decoy` is false, and the decisive gap is
  that the meter's days are not the replay's population, which puts population first.

**Abstraction test.** Stripped of nouns: how often a fixed capacity is exceeded once a steady load is added, when the
standing load and each event's response scale with how much of a fixed network lies below a fluctuating level read
from a separate record, so a response and a standing load read off a short record whose level mostly stayed low
understate a long record whose level often rose past most of the network. Nearest by mechanism:
- task178 (lineage, hydrology) fits one stage-discharge relation whose form changes above a level few gaugings reach;
  here no relation changes form: infiltration is linear in the submerged length, and the nonlinearity sits in how that
  length grows with the water level, read from the register's inverts, which no flow record shows.
- task138 (hydrology) replays past weather seasons through a root-zone balance started from each field's store; the
  replay is shared furniture (continuous simulation over a record is the field's method), the decisive move is not:
  there the share of each input reaching the store, here the exposure that conditions the response.
- task165 conditions an upgrade's gain on each site's untreated share, read from each site's own record; here the
  conditioning state is in no record of the storms or days: it is built from a level series against fixed elevations.
- task173 v1 re-mixes a bench of first-contact takers; here nothing is re-mixed, the exposure is continuous and
  physical.
- task134 and task146 condition on an option's payoff and on refusal timing within a period; neither builds an exposure.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** The infiltration reaching the station through cracked joints and laterals runs only where a
pipe lies below the water table, so it scales with the kilometres of sewer whose inverts sit under that day's
groundwater level; on the river terrace that level follows the river's high flows from the upper catchment more than
local rain, the 2024 to 2026 meter ran through low-river years when the water table stood below most of the terrace's
sewers, and the consent's 2004 to 2023 record holds winters with it above most of them, so a response per millimetre
and a base flow read off the meter understate the replay's wet years.

**Sources read, one line each.**
- `guard.py recent`, `coverage`, `mechanisms --objective forecasting` (every forecasting driver on file, lineage
  included) and `slots` on the setting nouns (sewer, infiltration, water table, invert, pump station, overflow,
  groundwater; unit hydrograph, rainfall, replay, continuous simulation, consent, storage) and on the mechanism words:
  no slot note or card carries a sewer, infiltration or groundwater mechanism; the replay furniture is task138's and
  task178's, read above.
- The neighbouring re-roots' `pipeline.json` (task118, task130, task181, task191, task250, task268, task306, task470,
  task482): none touches physical-environmental-sciences hydrology this batch.
- `layer2-rigor-patterns.md`: no patterns filed for Physical & Environmental Sciences, so the pattern is the build's
  own.
- task174's paused notes: the forward condition must act through a quantity the change does not name and no unit in
  the record has reached, the data must reveal it, and the textbook validation passes only because the hold-out shares
  the training regime; here the meter's high-water-table weeks are the separating storms.

## Shape

`other`, the criteria from the answer's structure: the call (1) with its three replay figures (3), the four critical
components (4), the replay chart's parts (bars per year for both cases, the limit line at 2, the finding title, the
axis: 5), the files (3), Ask A's eleven quarters (11) and Ask B's twenty station-year figures and two network totals
(22). About 49 criteria before the instruction-following lines; the asks carry 33 of them.

## Default path

1. Averaged the SCADA export's good 15-minute inflow into UTC hours beside the climate station's hourly rain (the archive
   in NZST hour ending to 2025, the 2026 provisional telemetry at 15 minutes in UTC).
2. Took the station's dry weather flow, infiltration included, as the mean of the dry hours (no rain in the previous 72
   hours) for each hour of the week over 2024 to October 2026, the field's dry weather flow and base infiltration.
3. Fitted the rest of the flow as the field's RTK unit hydrograph: a fast and a slow triangular response per millimetre of
   rain, calibrated on every storm of the meter.
4. Checked it the textbook way: it reproduces the meter's two logged overflows (both in 2026) and fits 2026 within about
   1 L/s on average when 2026 is held out of the calibration.
5. Ran it through every hour of 2004 to 2023 with the subdivision's code of practice flow added, at the data sheet's
   112.0 L/s and 350 m3, and counted the overflows under consent condition 3.

Ends on: about 1 wet weather overflow a year with the subdivision (0.70), inside the limit of 2, so connect in 2027.
Golden: about 3 a year with the subdivision (3.20), above the limit, so hold the connection until the upgrade (about 1 a year after it).

## Stump sentence

Fitting one unit-hydrograph response per millimetre and the meter's own dry weather flow on 2024 to 2026 and replaying 2004
to 2023 files about 1 overflow a year with the subdivision (0.70), inside the consent's two, and connects it; the step that
lands it there is reading the station's response as fixed when its infiltration rises 4.2 L/s for every kilometre of sewer
below the water table, which stood a median 0.2 km over the meter and 2.1 km over the replay.

## Three rules

- Task type: physical-environmental-sciences / hydrology-flood-frequency (serves Forecasting): the deciding quantity is
  how often a hydraulic capacity is exceeded under a long rainfall record.
- Domain test: the station's average wet weather overflows a year under the consent's continuous simulation, worked the
  way urban hydrology works rainfall-derived inflow and infiltration: a calibrated unit hydrograph model with a dry weather
  flow, run through every hour of the long rainfall record and routed through the station's pumps and storage.
- Swap: "can the new ward open without breaching its consented overflow frequency" has no rainfall record to run, no
  sewer, no water table and no pipe inverts: the quantity that decides has no counterpart, so the task stops reading the same.
- Layer 1: the SCADA in UTC with six comms gaps and the hours when the RTU's calculated inflow reads the pumps alone (the
  wet well at the weir); the archive in NZST hour ending with four infilled gaps (quality 500) beside the 2026 telemetry in
  UTC at 15 minutes with a 13-hour logger gap; the bore as depth below its measuring point with five runs of missing days;
  eleven abandoned mains still on the register; each written by its own system and each asserted neutral (SF10, SF12, SF16, SF19, SF20).
- Layer 2: forecast_uncertainty, the model chosen on hours it was not fitted on: carrying the meter's response forward, or
  conditioning the infiltration on the kilometres of sewer below the water table before the replay, flips the call.
- Decisive step: recognising that the station's base infiltration and slow storm response scale with the length of sewer
  lying below the terrace water table, building that length for every day from the bore's level and every in-service
  main's two inverts, and replaying each day of 2004 to 2023 with its own water table.
- Not semantics: reading every field, clock, unit and definition correctly, the consent's "each day as it occurred"
  included, still leaves the single response on connect, because no file says the response moves with the water table;
  the meter shows it only where its residuals are cut against the bore.
- Not rule application: no filed rule says how the station's inflow responds to anything, so executing every consent
  condition and the code still needs an inflow model; the enumerated family (the meter's own rate, one response per
  millimetre, one per season with a monthly base, the bore as a straight level, the length below the water table) spans
  0.70 to 3.20 a year with the subdivision; the standing family (what the June 2025 held-out weeks do not refute: the length
  model and its near shapes and conventions, SF10 to SF17) spans 3.0 to 3.3; what rules the rest out is a held-out miss of
  about 43 L/s on those weeks, loud only to someone who holds them out.
- Analyst test: a strong analyst who reads every file and rule correctly separates the dry weather flow, fits one
  unit-hydrograph response per millimetre on the 2024 to 2026 storms, carries the meter's base flow into the replay with
  the subdivision's flow added, and files about 1 overflow a year (0.70), inside the consent's two, so the connection proceeds.
- Estimand: consent AUTH-2024-0418 conditions 3, 6, 7 and 8: the network draining to EO-03 as connected at the assessment
  plus the connection at full development with the Code of Practice's design flows, run through every hour of the KRC 1187
  record from 1 January 2004 to 31 December 2023 each day as it occurred, wet weather overflows under the 24-hour rule, their
  count divided by twenty against the limit of two.
- No decoy: nothing is planted: no memo, draft, prior assessment or stakeholder figure argues connect; the meter's dry
  groundwater years are the world's weather; the developer's report declines to model the station; the logged overflows are
  the station's own record and both routes reproduce them.
- No certified replay: no certified or published figure exists for a method to reproduce; the consent prescribes the
  estimand and no method, and the overflow log ties under every route.
- Lesson: an infiltration-dominated station's capacity rides on how much of its network lies below a moving water table,
  so a model calibrated in low-groundwater years has to be conditioned on a constructed exposure (sewer length below the
  water table, from a level record against asset inverts) before it is run through a long record; no build on file builds
  an exposure from a register's elevations against a level series.

## Survivor anatomy

- Actor: each day's kilometres of PS03 sewer below the water table has no column in any file: it is a relation between the
  regional bore's level and every in-service main's two inverts in the asset register, built by arithmetic for every day.
- Link: no key joins the bore to the register or the SCADA; the link is elevation (the level against each pipe's inverts)
  and the day, no sentence names it, and the field's method (dry weather flow plus a unit hydrograph per millimetre) never
  asks for the bore.
- Reflex: the field's named method, an RTK unit hydrograph per millimetre with the meter's dry weather flow (rung 1, and its
  seasonal form at rung 2), files about 1 overflow a year with the subdivision, connect: the default path's Ends on.
- Back-test: the textbook route validates: it reproduces the meter's two logged overflows and fits 2026 within about 1 L/s
  when 2026 is held out; only the June 2025 high-river weeks, which no calendar split isolates, show its 43 L/s miss.
- Second use: the bore file is in the pack for the upgrade tank's flotation check (the brief names it as the design
  groundwater source), the register is the network's asset extract the operations team works from, and the archive is the
  consent's own record; delete the decisive step and every file stays.
- Shock: the June 2025 rise in dry weather flow is the meter's biggest movement, but it comes with no rain and no overflow
  and reads as a wet season's ordinary infiltration; the replay's wet years carry ordinary rainfall, and the call is one
  verdict, not a set of units a sort could interval.
- Pins: the consent files the WHAT (population of days, catchment and connection, outcome, unit, limit) in the regulator's
  own genre; no filed sentence names groundwater, infiltration, the bore, the water table, a season or a model.

## Readability screen

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0, the meter's own rate (2 overflows in 2.84 years) | no | no | yes, the record's rate | no | no | yes | no | readable |
| 1, one response per millimetre and the meter's base | no | no | yes, RTK per mm | the log ties | no | no | no | readable |
| 2, a response per season and the base by month | no | no | yes, seasonal RTK | the log ties | no | no | no | readable |
| 3 (decisive), the length below the water table, each day replayed | no sentence names it | no column holds it | not the field's default | no control scores it | the battery never builds it | not a ratio of a shipped figure | the bore and register have their own uses | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | average a year | twenty years' overflows over twenty | a year's maximum | same call | condition 7, "divided by twenty" |
| SF2 | an overflow | discharges under 24 hours apart are one | 12 hours, or each discharge | same call | condition 3 |
| SF3 | the record | 2004 to 2023 | the archive's 22 years | same call | condition 7 |
| SF4 | as connected at the assessment | the meter's catchment | scaled to the rating snapshot | same call and figure | condition 7; inert, asserted |
| SF5 | the connection | full development, 260 dwellings | stage 1 only | same call | condition 8, "at its full development" |
| SF6 | design flows | 2.7 persons, 200 litres, Table 5.2 by hour | a flat average | same figure | the code's section 5.2 |
| SF7 | what the station can pump | both pumps, 112.0 L/s | one pump, 61.8 L/s, or the duty pump alone below an assist level | same call (asserted); ask 1's counts read 4, 4 and 1 under the one-pump reading | the data sheet's drawdown test, condition 2, and the SCADA's storm drawdowns at 112 L/s |
| SF8 | what it can store | 350 m3, duty start to the weir crest | the chamber's 312 m3 | same call | the data sheet |
| SF9 | the upgrade | 1,100 m3 more below the crest | none | same call | the brief, "fills before the weir" |
| SF10 | the archive's stamps | hour ending, NZST | hour beginning | same figure | the archive's own header |
| SF11 | sewer below the water table | invert below the level | centreline or crown | same call | the meter: centre and crown fit at least 30 per cent worse |
| SF12 | the mains counted | in service | abandoned ones too | same figure | the register's status; inert |
| SF13 | which mains infiltrate | every in-service main | PE mains left out | same figure | inert, asserted |
| SF14 | the domestic pattern's clock | NZ local time | NZST all year | same figure | the code's "New Zealand time"; inert |
| SF15 | dry hours | no rain in the previous 72 hours | 48 hours | same figure | inert, asserted |
| SF16 | hours at the weir crest | set aside from the fit | kept | same figure | inert, asserted |
| SF17 | the response shapes | the best-fitting triangles | any within 5 per cent of it | same figure | the meter's fit, asserted |
| SF18 | each day as it occurred | each day with its own water table | the meter's water table held | connect | condition 7, "each day as it occurred" |
| SF19 | bore gaps | joined straight | carried | same figure | short gaps in dry spells; inert |
| SF20 | the 2026 logger gap | left out | read as zero | same figure | the gap fell on dry hours; inert |

## Ladder

| Rung | Construction | With the subdivision | Call |
|---|---|---|---|
| 0 | the meter's own rate carried forward (2 overflows in 2.84 years) | 0.70 | connect |
| 1 (default) | one response per millimetre and the meter's base, replayed | 0.70 | connect |
| 2 | a response per season and the base by month | 0.85 | connect |
| 3a | the bore as a straight level above its low | 1.00 | connect |
| 3 (decisive) | kilometres of sewer below the water table, each day replayed | 3.20 | hold |

Margins: rung 1 sits 1.30 under the limit and the golden 1.20 over it (60 per cent); every licensed variant of the golden
stays in the whole-number bin of 3 (SF4 to SF17 asserted); after the upgrade 0.75, inside the limit by 1.25. Worth: the
decisive move is the only one that reverses the call; the rungs below it all walk the same way. Pricing: the residue the
filed WHAT leaves is the inflow model (a method, not a knob); the move is worth 2.5 overflows a year against a call that
needs 1.3; the one-group-by route (a response per season) lands connect; the step estimates one coefficient from 1,000
dry days across 0 to 21 km (4.20, its standard error under 0.01), so its noise is far below the move.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every hour of 2004 to 2023, each day as it occurred; the catchment as connected plus 260 dwellings | condition 7 and 8, filed |
| 2 Unit of account | wet weather overflows at EO-03 | condition 3 |
| 3 Attribution window | the replay's years by NZST | condition 7; no overflow straddles a year end by more than hours (C1) |
| 4 As-of dating | the catchment at the assessment (the meter) | condition 7; inert (SF4) |
| 5 Version basis | the archive as verified, 2026 as provisional | the files' own headers; 2026 is meter only |
| 6 Denominator | twenty years | condition 7 |
| 7 Weighting | none | not applicable |
| 8 Window length | the full meter for the fit | C1 across held-out splits |
| 9 Boundary inclusivity | the limit is "shall not exceed two" | 3.20 against 2, far from the edge |
| 10 Rounding path | the average computed unrounded, compared with 2, reported whole | the prompt's rounding; edges cleared (asserted) |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | hours at the weir crest read the pumps alone | set aside; inert (SF16) |
| 13 Order of operations | model, then route, then count | the routing is the station's own sequence |
| 14 Row order | none | not applicable |
| 15 Duplicate resolution | discharges merged under 24 hours | condition 3 |
| 16 Identity normalisation | PS03's mains by catchment field | the register's own field |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | L/s, m3, mm, m NZVD2016 | units in the headers and the data sheet |
| 19 Code and status semantics | in-service against abandoned mains; quality codes | the register's status (SF12); headers |
| 20 Integerisation | overflow counts are whole | by construction |
| 21 Clause scope | condition 8 applies to 50 or more dwellings | 260 dwellings |
| 22 Forward window contents | the replay's driver files: the archive and the bore for 2004 to 2023 | shipped |

## Literal reader

Executing the prompt, consent conditions 3 and 6 to 8, the Code of Practice's section 5.2 and the data sheet word for
word fixes everything but the inflow model, which no sentence states; the data force it (SF11, SF17, the held-out June
2025 weeks), and every reading of every term gives the golden's call (SF1 to SF20), the easy answer coming from an easy
model on the same literal estimand, never from another reading.

## Oracles

- The overflow log (two overflows, both in 2026): reproduced by the single response and by the golden alike, so it ties on
  both paths and arbitrates nothing.
- The treatment plant's inlet readings (a declared distractor): show the June 2025 rise town-wide, on both readings alike.
- The billing policy's and the consent's sentences: each ask's referee, none touching the call.

## Ask sheet

The call's population is PS03's SCADA inflow, the climate archive and telemetry, bore 72_1043 and the register's PS03
mains. Every ask reads other rows: Ask A the catchment's water meters, accounts, rating snapshot and building consents;
Ask B the other five stations' monitor messages, the lines company's outages and the council's electricity sites. Zero
device or hazard rows sit in the call's population (asserted: PS03's monitor carries only its two 2026 overflows, PS03's
ICP never changed, no PS03 emergency overflow, the call reads no ask file).

**Ask A, residential water use per dwelling per day in each quarter, January 2024 to September 2026 (11 figures, whole
litres).** H18: a component of the subdivision's design flow (the code's 540 litres a dwelling against what the
catchment's dwellings use). Construction: the billing policy's section 4 (spread from the first reading's day to the day
before the second, estimates out, exchange readings in). Primary (all eleven quarters): the rating information is a
snapshot of 31 October 2026, and 36 dwellings (minor dwellings, a unit added to a block of flats, four new houses) were
certified during the window, so carrying the snapshot's parts back over every quarter overstates the dwellings and every
quarter misses by 1 to 8 litres; only each rating unit's parts dated by the building consents' code compliance
certificates lands, a reconstruction across the rating and consent systems. Hazards: cross-lease flats on one meter,
each on its own account; sales that close one account and open the next on the same meter; estimated readings; meter
exchanges; commercial rating units. Pin test: the policy files the measure (basis, spreading, grain), not which records
date a dwelling.

**Ask B, each other pump station's wet weather overflows and spill hours in 2024 and in 2025, and the network's emergency
overflows in each year (22 figures, whole numbers).** H18: the consent's own record across the network, the reporting
the connection is decided under. Construction: conditions 3 and 5 on the monitors' messages, read on the monitors' own
NZST clock, each serial placed by the installation history. Primary: three stations' supplies were renewed in 2025 and
their earlier outages sit under the closed ICPs, which only the council's electricity site list holds against the same
address; matching outages through the asset register's current ICP turns four emergency overflows into wet weather ones,
missing ten figures (PS02 2024, PS04 2025, PS06 2024 and 2025, counts and hours, and both network totals). Hazards: a
monitor serial reissued from PS02 to PS05 in 2025 (placed by date); the gateway's received times lagging the monitors'
own on emergency messages; the float switches' chatter (the 24-hour rule). Pin test: the consent files what an emergency
overflow is, not which ICP a station had.

| Ask | Figures | Cracker path (lands the call, runs the battery, executes every filed rule) | Cracker keeps | Verdict |
|---|---|---|---|---|
| A, water use per dwelling | 11 | the policy's spreading, actual and exchange readings, distinct rating units per meter, the snapshot's parts in every quarter | 0 of 11 | miss |
| B, other stations' overflows | 22 | the monitors' own clock, serials placed by date, the 24-hour rule, outages through the register's current ICPs | 12 of 22 | miss |

| Ask | Mirror (the single response's connect, same ask handling) | Mirror keeps |
|---|---|---|
| A | as the cracker | 0 of 11 |
| B | as the cracker | 12 of 22 |

Pair ceiling: 48.5 (one response on the call and one off it, both handling the asks the cracker's way).
Mirror leakage: 36.4 per cent of the ask weight.
Measured by: generator/ceiling.py (on the cut pack: the cracker keeps 12 of 33 ask figures; the full includer, a stress row, keeps all 33).

## Gates at stage 3

- Generator: `checks.py` 59 assertions, 0 failed (the input gates, the call and its margins, R3a and R3b, the rungs, the
  deciding configuration in the record, SF1 to SF20, both asks' devices and margins, the separation, the realism sweep);
  `verify.py` reproduces the three call figures by its own parsing and fit and every ask figure, 0 failed.
- Two consecutive builds byte-identical: target, golden, figures.json and submission.md; target.zip sha256 200b0014d310ee60e8a5fb9b86bb8eec3ea9b5845bbfc7ed7f5e4c3daf9f91e3.
- `figures_check.py`: PASS, 45 figures in blocks 1 to 4, none absent. `precut.py`: PASS, 61 checks. `voice-check.py`:
  PASS, 977 characters, every shell class under its quota. Container audit (`scrub_producer_metadata.py`): clean.
- `leak.py` (as of 2026-11-04): REVIEW, sweep 4 only, both lines ruled here. The consent carries record, overflow,
  condition and inflow because they are its estimand's own words; the upgrade brief carries groundwater because the tank's
  flotation check takes its design level from the regional bore, a fact about the tank's design and the bore's second use,
  which says nothing of the station's inflow. Neither names the move.
- `guard.py heart`: WARN (repeat.question_form against task250, answered at the draw); task130 v5, registered after this
  draw with the same structural signature, differentiated on the card. `guard.py surface`: personas in the pack are the
  three drawn names; five pairs promoted on card axes alone at surface similarity 0.080 to 0.084: task130, task134,
  task146 and task165 on the structural signature (each differentiated on the card) and task154 on the calibration form
  and context artifact (an economics stock revaluation sharing no world, data or driver), left for the author's
  adjudicated clone check.
- Measured on the cut pack: the conditioned replay files 2.90, 3.20 and 0.75 overflows a year (58, 64 and 15 in twenty
  years); one response per millimetre 0.65 and 0.70; a response per season with the base by month 0.85; the bore as a
  straight level 1.00; held out of each fit, the June 2025 high-river weeks are missed by 43 L/s on average by one response
  per millimetre and by 0.2 L/s by the conditioned model. Pair ceiling 48.5, mirror leakage 36.4 per cent (`ceiling.py`).

## Tried and rejected

- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
