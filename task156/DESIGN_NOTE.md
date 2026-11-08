# task156: a rapid-charging operator, which hubs fall below 99 per cent availability in 2027 (architecture 4)

Private, never ships. Architectures 1 to 3 were each returned FAILED_TO_STUMP by the portal: Millrind's paid
moderation pool (product analytics), the Riverbank Road pump station's consented overflows (physical and
environmental sciences) and the union branch's protected action ballots (political science and public policy, both
responses on the golden 11 councils on 2026-11-07). The slot is re-rooted in a fourth domain: world, decision,
quantity, data, generator, prompt shell, deliverables, asks and mechanism are all new, architecture 3's build outputs
left the folder at this draw (git history keeps them), and the three identities sit in the card's `lineage` with
their fates.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v4, registered 2026-11-08; architectures 1 to 3 in `lineage`, their three shells in `lineage_shells` |
| Domain / task type | `energy-systems-utilities`, task type `asset-condition-maintenance` (serves Forecasting): the deciding quantity is each high-power charge point's availability in the 2027 contract year, forecast from each failure mode's frequency and the downtime it costs through the visits, repairs and asset changes the year will run under |
| Objective | Forecasting & Predictive Modeling: availability in the contract year 1 January to 31 December 2027, a window not yet open; the asset base is the partnership's renewal programme of record (the legacy units out at its hubs by 18 December 2026) |
| Shape | `10`, a scorecard against one threshold: every hub carries a side of the 99 per cent standard for its high-power charge points, and the call is the set below it |
| Decision | `designation_set`, answer unit `set_of_items`: the hubs the operator names in its 2027 availability plan because a high-power charge point there is forecast below 99 per cent |
| Mechanism | gap time (the hang record comes from units powered down every month, the 2027 bet is on units powered down a few times a year); generators G7 (a hang can only happen inside an uptime window that the hub's power-downs open or shut), G14 (the hang rate measured on units sharing a pillar with a legacy unit does not apply once it goes), G13 (the 2027 regime differs from every year on record at the programme hubs); Gate G `forecasting`; strategy `forecast_method_backtest` |
| Layer 2 family / pattern | `estimation_fit`; `own:hang-hazard-on-the-hub-power-down-clock-carried-through-a-changed-repair-regime` |
| Furniture | forum `customer_or_counterparty` (the North Midlands Charging Partnership, the concession's grantor, reviews the plan), forcing event `audit_or_inspection` (the partnership's annual concession review in December 2026), organisation family `utility_or_infrastructure` (Ardvane Charge DAC, a public rapid-charging operator), role family `operations_director` (the operator's network performance lead), context artifact `monitoring_export` (the back office's status history), calibration `none`, opening `question-first`, question form `which` |
| Spine | `connector_status_history_2023-2026.csv`, one row per status change a charge point reported to the back office or the back office wrote when its heartbeats stopped (27,342 rows, UTC), beside the asset register, the two contractors' work orders, the planned maintenance schedule, the supply interruption log and the 2026 charging sessions; constructed for this build, no real dataset |
| Deliverables | `hub_availability_2027.csv` (the partnership's plan return, one row per hub, the asks in its columns), `availability_plan_2027.pdf` (the covering letter naming the hubs) |
| People | drawn with `guard.py names --geo ireland --seed 156`: Sorcha Jackman (the operator's network performance lead), Bronagh Allis (the partnership's concession manager), Ailis Fee (the maintenance contractor's service manager); Henry Dunford passed over, his first name already on task457 |

**The hubs.** Thirty hubs, each with one legacy Tavrin RC50 (50 kW, 2017 to 2019) and one to four Korrant HX150 (150
kW, 2021 to 2023). At 25 hubs every unit is fed from one supply pillar; at the three coastal hubs (Bunacurry Pier,
Rossnabeg Harbour, Portavaddy Seafront) and at Carrowkeel Business Park and Tobernalt Road the HX150 units sit on a
pillar of their own, a fact no file stores. The RC50's monthly cabinet service, and its cabinet repairs, isolate the
pillar it stands on. Motorway service hubs (planned visits every two months): Carrigvane Services, Lismoy Services,
Ardcree Services, Knockvane Services, Drumtane Services, Monaleen Services. The renewal programme takes the RC50 out at
twelve hubs by 18 December 2026: the first three motorway hubs, seven standard hubs (Kilbeg Retail Park, Tullymore
Market Square, Clonlea Leisure Centre, Rathmoy Station Road, Glenfad Shopping Centre, Ballinkeel Main Street, Derrylane
Park and Ride) and two hubs on long rural supply spurs (Annagh Cross, Cloonfin Crossroads), with a new HX150 at the
ten that are not on the spurs. The other ten hubs keep their RC50 and share its pillar.

**Guard answers (check on the draft and again on the registered card).** WARN `repeat.decision` (designation_set
repeats task268): the decision is a set of named hubs because the concession's plan names hubs, and no other answer
type fits the review. WARN `repeat.question_form` (which repeats task482): a pick of a set asks which, as the
guide-to-prompt rule says; the shell differs from task482's at the second sentence and the deliverable set. NOTE
`test.same_puzzle_older` (task451) and `test.same_driver_older` (task105 v1, task162 v2, task170 v1, task229 v3):
differentiated on the card, one line each. Variants measured at the draw and refused: pattern E (same puzzle as
task235 and task445, same driver as eight builds), G14 decisive (`ban.pattern` against task250), G13 decisive
(`ban.pattern` against task482), pattern A (ten older drivers). Forum, forcing event, organisation family, role
family, context artifact and strategy clear the last three builds (task250, task482, task268). `voice-check.py` WARN
`shell quota` (which at 32 per cent of prompts on file): the decision is a pick of hubs, so the question asks which; the
shell differs from every approved build at the second sentence's opener (Return) and the deliverable set (csv and
pdf), and from the slot's three dead shells on all three axes.

**The data-native sentence.** The back office's status history records each charge point going offline, and the only
place a pillar's power-down shows is the minute in which every unit on it drops at once; the HX150 controller hangs,
which only an on-site power cycle clears, come after the days since the unit last powered up, and the RC50's monthly
cabinet service, which isolates its pillar, is what kept those spells short at 25 hubs through 2023 to 2026.

**The abstraction sentence.** "A unit's failures run on a clock that its neighbours' repairs reset, so a plan that
removes the failing neighbours raises the survivors' failures." It cannot be written against the nearest approved
builds: task132 (a failure resets the failed item's own wear curve), task303 (a shared upstream loss every unit logs
in the same minute is taken out of a figure), task162 (a device acts only above its setting), task141 (a cap moves
every unit to the at-ceiling rate), task169 (a closed route had pre-empted the open one), task175 (a vacant lot's
take-up follows its own street's fill); nor against task156's spent architectures (a closed pool's falling leaving
rate, infiltration scaled by submerged sewer, a delegate in post at the worksite); nor against the two nearest
drivers by text, task127 v4 (supporting one firm prevents its dependants' failures) and task173 v3 (work on a unit
breaks the parts attached to it soon after).

## Shape

Shape 10, a scorecard against one threshold. Criteria: the set (1), each hub's side of 99 per cent (30), the asks
(each hub's January to October 2026 high-power charges and the energy they delivered, 60), the two deliverables (2):
93, supplied by the answer's structure. The prompt names no count.

## Default path

1. Read the asset register (the June 2025 back-office migration re-keyed every charge point; the register carries both
   IDs and the serial the contractors log), the status history (UTC), the two contractors' work orders (Irish time, a
   new job-code list from the April 2024 contract change), the planned maintenance schedule, the supply interruption
   log, Schedule 4 of the concession agreement and the partnership's renewal programme.
2. Rebuild each HX150's availability for 2023 to 2026 under Schedule 4 (Faulted, Unavailable and Offline minutes count;
   notified planned maintenance and supply interruptions, with the half hour after each, are excluded).
3. Fit the failure model per unit and failure mode: controller hangs (offline until a technician power cycles the unit)
   and other faults, a Poisson rate per unit-year on hub type, coast, the hub's unit count, commissioning year, 2026
   charges a day, planned visits a year, supply interruptions a year and the legacy unit's work orders a year, unit
   effects shrunk to the hub and the fleet; the downtime each event costs from the status history and the work orders.
4. Validate: leave each unit out, and back-test 2025 from 2023-24 and January to October 2026 from 2023-25: mean errors
   of 0.12, 0.31 and 0.27 points, and 58, 52 and 53 of 58 units on their side of 99 per cent (`checks.py`).
5. Carry the rates into 2027 on the programme's asset base (the RC50 out at its hubs with its own isolation minutes,
   the new HX150 units at fleet rates, every covariate at its 2027 value) and list the hubs with an HX150 below 99.

Ends on: 5 hubs (Bunacurry Pier, Carrowkeel Business Park, Portavaddy Seafront, Rossnabeg Harbour, Tobernalt Road).
Golden: 12 hubs (Ballinkeel Main Street, Bunacurry Pier, Carrowkeel Business Park, Clonlea Leisure Centre, Derrylane
Park and Ride, Glenfad Shopping Centre, Kilbeg Retail Park, Portavaddy Seafront, Rathmoy Station Road, Rossnabeg
Harbour, Tobernalt Road, Tullymore Market Square).

## Stump sentence

Carrying each high-power charge point's controller-hang and fault rates from 2023 to 2026, validated leaving each unit
out and on two back-tests, files 5 hubs below 99 per cent in 2027, the five whose HX150 units already hang two or three
times a year; the step that lands it there is reading each unit's hang rate as its own, when a hang comes only after
about 75 days without a power-up and the RC50's monthly cabinet service powers down every unit on its pillar, so only
the units at those five hubs (on a pillar of their own) ever ran that long, and at the seven standard programme hubs,
which keep neither two-monthly visits nor frequent supply interruptions once the RC50 goes, the HX150 units will hang
three or four times a year and the set is 12.

## Three rules

Task type: asset-condition-maintenance (Energy Systems & Utilities), which serves Forecasting & Predictive Modeling: each high-power charge point's availability in the 2027 contract year, forecast from each failure mode's frequency and repair downtime under the visits, repairs and asset changes the year will run under.
Domain test: the deciding quantity is each high-power charge point's 2027 availability against the concession's 99 per cent standard, worked the way asset condition and maintenance forecasting works it, each failure mode's frequency and the downtime each event costs carried through the year's planned visits, repairs and asset changes; with another field's nouns there is no failure a power cycle clears and no repair that powers its neighbours down, so the forecast stops reading.
Swap: put "hospital wards" for "hubs" and "beds" for "charge points": a ward has no supply pillar that a neighbour's service opens and a bed does not seize until it is power cycled; put "megawatt-hours" for "minutes available" and the restart clock has nothing to count.
Layer 1: the June 2025 back-office migration re-keyed every charge point (the register carries both IDs, the contractors log serials); the status history is in UTC and the work orders, visit schedule and supply log in Irish local time; the back office writes Offline only after three missed heartbeats, about fifteen minutes after a drop; status notifications are re-sent and duplicated; the two maintenance contractors used different job-code lists before and after April 2024; the planned maintenance schedule changed layout between its 2025 and 2026 sheets; the session export splits a charge when the back office loses a unit for more than five minutes and when a card's pre-authorisation runs out; Schedule 4 and the programme are PDFs with tables. Nothing is placed to be caught.
Layer 2: estimation_fit: the hang rate has to be estimated on the clock that drives it, the days since each unit last powered up, each spell ended by the next power-down or restart, and the 2027 forecast run on the power-down regime the programme leaves; the choice that flips the call is reading each unit's recorded hang rate as a property of the power-down regime it was measured in.
Decisive step: recognising that the HX150 hangs come only after about 75 days without a power-up, that every unit on a pillar restarts whenever the pillar is isolated for the RC50's monthly service or a repair, a planned visit or a supply interruption, and that the programme takes the RC50 away, so each 2027 unit's hangs follow the days between its hub's remaining power-downs.
Not semantics: every field, code and clock read correctly (IDs and serials crosswalked, UTC converted, the heartbeat lag allowed for, duplicates removed, both contractors' job codes mapped, Schedule 4's exclusions applied) still leaves the unit-level route on 5 hubs; no field records a power-up or a pillar, and no file defines a hang by uptime or names the restart.
Not rule application: no filed rule or procedure says a hang depends on the days since a power-up or that the RC50's service powers down other units; Schedule 4 files only the availability definition, its exclusions and the standard. Enumerated family (each unit's own rate carried, rates shrunk to hub and fleet, the full-covariate Poisson model with the RC50's work orders, visits and interruptions at their 2027 values, a regression tree on the same covariates, the RC50's recent jobs and the days since its last job as daily covariates, the 2026 availability carried, each unit's monthly series smoothed): on the clean truth the members file sets of 3 to 8 hubs, none the golden and none holding more than one of the seven standard programme hubs (the Ladder's counts, asserted in checks.py); standing family once the restart clock is seen (the hang rate by days since power-up read as a 5-day or 1-day life table or a fitted onset, run through the 2027 regime by simulation or by renewal arithmetic): the same 12 hubs, so the standing spread on the graded set is zero only after the step; what rules the cheap members out is the hangs' onset in the days since power-up, which only the pillar-wide Offline minutes in the status history show.
Analyst test: a strong analyst who maps the IDs, converts the clocks, applies Schedule 4 and reads the programme fits each high-power charge point's hang and fault rates with every covariate the pack holds, validates them leaving each unit out and on 2025 and 2026 back-tests, carries them into 2027 with the legacy units removed and files 5 hubs (the five whose HX150 units already hang); seven standard programme hubs it passes fall below 99 per cent once the hangs are read on the days since the units last powered up.
Estimand: Schedule 4 of the concession agreement files the population (every high-power charge point in service at a hub in the contract year, new units included), the outcome (the share of the year's minutes, notified planned maintenance and supply interruptions with the half hour after each excluded, in which it was not Faulted, Unavailable or Offline), the window (the 2027 contract year), the unit (the charge point), the comparison (below 99 per cent) and the asset base (the partnership's approved programme for the year), and its clause 4.6 names the hubs the plan must list (any hub with a high-power charge point forecast below the standard).
No decoy: nothing is planted: no memo, briefing, forecast or stakeholder figure ranks the hubs or argues a set; the programme says which units go and why (Tavrin's support for the RC50 ends in 2026), not what availability follows; the customer survey and the tariff schedule are distractors that carry no availability figure.
No certified replay: the method is not hidden behind a certified figure to be reproduced; no availability statement for a past year ships, both routes reproduce the history the status log records, and the decisive step changes the forward window, not the fit to the past.
Lesson: a failure rate measured on units whose clock their neighbours' repairs kept resetting belongs to that repair regime, and a plan that removes the neighbours has to be forecast on the clock that drives the failure, not on the rate; no build on file has a unit's failure clock reset by work done on another unit.

## Survivor anatomy

Actor: the deciding property is each HX150's days since it last powered up, which no column holds: a power-up shows only as an Available row after an Offline one, a pillar's power-down only as the minute in which every unit on it goes Offline at once, and which units share a pillar with the RC50 is in no file (the register lists units and hubs, not pillars).
Link: the relation is the coincidence of Offline rows across sibling charge points at one hub, in the status history the availability rebuild already reads; the join it needs is hub by minute across units, and the missing key is a power-down or pillar identifier, which no file carries; the work orders log the RC50's monthly service at every hub, the five where it powers down only the RC50 included, so the work orders alone give the wrong clock.
Reflex: the field's method for the deciding quantity, each unit's failure rate per mode carried with its repair downtime (a Poisson rate with unit effects shrunk to the hub, the full-covariate model beside it), sits at rung 0 and files 5 hubs.
Back-test: leave-one-unit-out and the 2025 and January to October 2026 back-tests pass on the rate route, because every unit ran under one power-down regime throughout 2023 to 2026 (an RC50 stood at every hub all four years).
Second use: the status history is the availability rebuild's input, the work orders give repair downtime and classify the hangs, the visit schedule and the supply log give Schedule 4's exclusions, the programme gives the asset base and the register the IDs; deleting the decisive step leaves every file in the pack.
Shock: the seven standard programme hubs are among the most available in the record (no HX150 hang there in four years), the change reads as an asset renewal that removes the RC50's own isolation minutes, and the golden is not an interval of any shipped statistic (the five hubs that already hang sit at the bottom of every sort, the seven at the top).
Pins: Schedule 4 files the WHAT (each high-power charge point in service in the contract year, the availability formula, its exclusions, the 99 per cent standard, clause 4.6's listing rule, the programme as the asset base); no filed sentence names power-ups, uptime, pillars, restarts or what the RC50's service does to other units.

## Readability screen

| Rung | What a solver has to see | Where it shows | Verdict |
|---|---|---|---|
| 0: each unit's hang and fault rates carried with their downtime (the reflex) | hangs and faults per unit-year, attendance and repair times | status history, work orders | readable |
| 1: the five hubs that hang read as coast or hub effects | the high-hang hubs share no stored attribute but three are on the coast | register, status history | readable |
| 2 (decisive): hangs follow the days since power-up, and an RC50 isolation powers up every unit on its pillar | Offline rows of every unit at a hub in one minute, and every hang at 75 or more days after the unit's last power-up | status history only, as a relation across sibling units | silent |
| 3: the 2027 power-down regime per hub | the 2027 visit plan, each hub's supply interruption rate, the programme's hubs | visit schedule, supply log, programme | readable |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | hub | each of the thirty hubs in the register | a hub counted once per supply pillar | same call | Schedule 4 clause 4.6 names hubs; same call, asserted |
| SF2 | high-power charge point | every HX150 in service at the hub in 2027, the programme's new units included | the existing units only | same call | Schedule 4 4.1 (in service in the contract year); same call, asserted |
| SF3 | availability | Schedule 4's minutes formula with the exclusions out of both terms | planned visits and interruptions counted as downtime | same call | Schedule 4 4.3; same call, asserted |
| SF4 | below 99 per cent | strictly below | at or below | same call | no forecast sits within 0.3 of 99, asserted |
| SF5 | forecast | each unit's expected 2027 availability | the median simulated year | same call | Schedule 4 4.6 (forecast availability); same call, asserted |
| SF6 | a hub's side | its lowest HX150 | the mean of its HX150 units | same call | clause 4.6 (any high-power charge point); same call, asserted |
| SF7 | the contract year | 1 January to 31 December 2027, Irish time | the year in UTC | same call | Schedule 4 4.2; same call, asserted |
| SF8 | the asset base | the programme of record: RC50 out at its twelve hubs by 18 December 2026, new HX150 at ten | the register as at the extract | same call at every hub outside the programme; the programme is the filed base | Schedule 4 4.6 (the approved programme) |
| SF9 | Offline minutes | as the back office recorded them (from the Offline row) | back-dated fifteen minutes to the drop | same call | same call, asserted |
| SF10 | duplicated status rows | one row per change | every row read | same call | same call, asserted |
| SF11 | the half hour after an exclusion | excluded (Schedule 4 4.3) | not excluded | same call | Schedule 4 4.3; same call, asserted |
| SF12 | supply interruptions in 2027 | each hub's 2023 to 2026 rate | the last twelve months' rate | same call | same call, asserted |
| SF13 | attendance in 2027 | each hub's 2023 to 2026 hang attendance | the fleet's | same call | same call, asserted |
| SF14 | the new units' start | commissioned by 18 December 2026, uptime from the programme works | uptime from 1 January 2027 | same call | same call, asserted |
| SF15 | hang classification | an Offline spell of three hours or more ended by a power cycle (the work order) | every Offline spell over an hour | same call | same call, asserted |

## Ladder

Pricing sequence on the generator's clean truth (`checks.py` asserts each number; the generator's figures are the
source of the counts below, this table quotes them):

| Rung | Construction | Set filed | Reaches golden |
|---|---|---|---|
| 0 | each unit's hang and fault rates carried, the RC50's isolation minutes dropped at the programme hubs | 5 hubs (the five whose units hang on record) | no |
| 0b | rates shrunk to hub and fleet (gamma-Poisson) | 5 hubs | no |
| 0c | the full-covariate Poisson model (hub type, coast, unit count, commissioning year, 2026 charges a day, visits, interruptions, the RC50's work orders a year) at 2027 values | 4 hubs (the RC50's work runs high where the units hang, so its removal lowers the forecast) | no |
| 0d | a regression tree on the same covariates | 5 hubs | no |
| 0e | the daily model given the RC50's jobs in the last 60 days and the days since its last job | 3 hubs (the coast alone) | no |
| 0f | the January to October 2026 availability carried | 8 hubs, two outside the golden and one programme hub | no |
| 0g | each unit's monthly availability series smoothed | 7 hubs, two outside the golden | no |
| 1 | the restart clock built from the work orders (every RC50 job a power-up for every unit at its hub) | none (the hangs then fall on short uptimes and spread thin) | no |
| 2 | the restart clock from the status history, but 2027 run without the visits or the interruptions | 15 hubs (adds two motorway hubs and a rural spur hub) | no |
| 3 (golden) | hangs read on the days since power-up from the coincident Offline rows, run through the 2027 visit plan, each hub's interruption rate and attendance | 12 hubs | yes |

Gate F: cheap routes reaching the golden on the clean truth, 0 of 7 (rungs 0 to 0g); standing family after the step, 6
of 6 constructions on the golden (5-day and 1-day life tables and a fitted onset, each run by simulation and by
day-step arithmetic); margins over 20 redraws of the world as printed by `checks.py` (the Gates line below).

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every HX150 in service at a hub in 2027 (Schedule 4 4.1), new units included | filed; SF2 asserted |
| 2 Unit of account | the charge point, the hub listed by its lowest | filed (4.6); SF6 asserted |
| 3 Attribution window | the 2027 contract year in Irish time | filed (4.2); SF7 asserted |
| 4 As-of dating | the programme of record approved 21 October 2026 | filed (4.6) |
| 5 Version basis | the status history as exported 2 November 2026, one version | C1 |
| 6 Denominator | the year's minutes less excluded minutes | filed (4.3) |
| 7 Weighting | none: each unit's own availability | filed (4.6) |
| 8 Window length | the whole 2023 to 2026 record for rates and attendance | C1 across windows (SF12, SF13) |
| 9 Boundary inclusivity | strictly below 99 | C1, nothing within 0.3 (SF4) |
| 10 Rounding path | the side only is graded, no availability figure | C1 |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | uptime spells still open at 31 October 2026 censored | C1, asserted on the standing family |
| 13 Order of operations | exclusions before the share | filed (4.3) |
| 14 Row order | none: rows sorted by time per unit | C1 |
| 15 Duplicate resolution | a re-sent status row counts once | C1 (SF10) |
| 16 Identity normalisation | old and new IDs and serials through the register | the register's own crosswalk, C4 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | minutes | C1 |
| 19 Code and status semantics | Faulted, Unavailable and Offline count (4.3) | filed |
| 20 Integerisation | none | C1 |
| 21 Clause scope | clause 4.6 lists hubs for the contract year | filed |
| 22 Forward window contents | the 2027 visit plan sheet, the programme's dates, each hub's interruption record | shipped driver files |

## Literal reader

Executed word for word: Schedule 4 fixes the population, the formula, the exclusions, the standard and the asset base,
and clause 4.6 lists every hub with any high-power charge point forecast below 99 per cent; the prompt adds nothing
the schedule does not carry. Every literal reading of a convention (SF1 to SF15) files the same set or is ruled out by
a quoted clause. The easy answer (5 hubs) comes from an easy method on the same literal estimand, a rate carried, never
from another reading; the golden (12 hubs) comes from the same estimand worked on the clock the data show.

## Oracles

None ships. No availability statement, forecast or plan for any past or future year is in the pack; the programme
gives dates and units, never availability; the supply log, the visit schedule and the work orders each tie to the
status history under every handling, and nothing arbitrates between the rate route and the restart clock except the
status history's own rows.

## Ask sheet

The call's population is the status history, the work orders, the visit schedule, the supply log, the register and
the programme. Both asks read the January to October 2026 session export, which the call reads only for a charges-a-day
covariate that moves no forecast (asserted: the default path's set and the golden are unchanged under every handling
of the session devices). Zero device or hazard rows sit in the call's population (asserted by count).

**Ask A, each hub's high-power charges begun January to October 2026 (30 figures, whole charges).** H18: each hub's
use of the units the plan forecasts, which the partnership's return carries beside the side. Schedule 6 files the
WHAT: a charge is a vehicle's connection to a connector in which energy was delivered, from connection to
disconnection, counted once in the month it began (Irish time). Primary 1 (D4 with D1, a charge under two records
with its middle in neither): when the back office hears nothing from a unit for five minutes it closes the charge at
its last meter reading and records the rest, when the unit reconnects, as a new charge with no token; every hub's
units drop out several times a week, so every figure moves by dozens. Found only by the meter register: the resumed
record starts above the last one's closing register with no charge between. Primary 2 (D6, a charge at the payment
grain): a card charge that reaches its pre-authorisation is closed and continued under a new pre-authorisation one
to four seconds later, both records with no token. Hazards: a re-sent page of exact duplicate rows in the September
export; failed starts with no energy; genuine back-to-back card charges two and a half minutes or more apart (a merge
by time alone over-merges them). Pin test: Schedule 6 names the unit (a connection) and the month rule, never which
records belong to one connection.

**Ask B, the energy those charges delivered (30 figures, MWh to one decimal).** H18: the energy the partnership's
return reports per hub. Schedule 6 files the WHAT: the energy the charge point's meter registered for the charge.
Primary (Primary 1's other face): the energy delivered while the unit was out of contact is in neither record's
energy column, only in the step between the first record's closing register and the second's opening one, so every
hub's figure sits several tenths of a MWh under the golden when the columns are summed. Hazards as Ask A. Pin test:
the meter is named, the continuity across records is not.

| Ask | Figures | Cracker path (lands the call, runs the battery, executes every filed rule) | Cracker keeps | Verdict |
|---|---|---|---|---|
| A, charges | 30 | duplicates out, failed starts out, records with one token on one connector less than 30 minutes apart merged | 0 of 30 | miss |
| B, energy | 30 | energy column summed over the cracker's charges | 0 of 30 | miss |
| A and B, full includer (merges every record that opens above the last one's closing register, energy from the registers, card continuations left) | 60 | as the cracker, plus the register merge | 30 of 60 (charges 0, energy 30) | miss |
| A and B, register advance (each unit's register advance over the window for energy, the cracker's charges) | 60 | as the cracker, energy from the registers | 30 of 60 (charges 0, energy 30) | miss |

| Ask | Mirror (the rate route's set, same ask handling) | Mirror keeps |
|---|---|---|
| A | as the cracker | 0 of 30 |
| B | as the cracker | 0 of 30 |

Pair ceiling: 28.5 (one response on the call and one off it, both handling the asks the cracker's way; measured on the
cut pack).
Mirror leakage: 0.0 per cent of the ask weight.
Measured by: generator/ceiling.py (on the cut pack).

## Gates at stage 3

- `checks.py`: 62 assertions, 0 failed: R1 to R3c on the clean truth (the default path files the 5, the restart clock
  alone files the 12, the two lower rungs stay wrong, no copied block); Gate F, 0 of 7 cheap routes on the golden and 6
  of 6 standing constructions on it; margins over 20 redraws of the world, 20 of 20 on the truth's set (closest
  forecast 0.21 points from 99, median 0.40); SF1 to SF15; the asks (the golden handling reproduces the true charges and
  energy exactly, every energy figure at least 0.013 MWh from its rounding edge, the cracker keeping 0 of 60 and the full
  includer 30 of 60); the separation line; the input gates; H1 on every workbook and PDF, the golden letter included; the
  realism sweep.
- `verify.py`: 0 disagreements on its own code path (pandas readers, its own spell and cluster logic, its own day-step
  forecast): the same 12 hubs, its closest forecast 0.25 points from 99, the rate route's 5, and 30 of 30 charges and 30
  of 30 energy figures.
- Two consecutive builds byte-identical (every file under target/ and golden/, figures.json, metadata.json,
  submission.md); target.zip cut twice to one sha256 (`generator/zip_target.py`), its ten files at the root.
- `figures_check.py` PASS (69 figures); `precut.py` exit 0; `voice-check.py` PASS (578 characters; the shell-quota
  WARN answered under Guard answers); `ceiling.py` pair 28.5, mirror leakage 0.0.
- `guard.py heart` WARN (repeat.decision against task268, repeat.question_form against task482, both answered under
  Guard answers). The surface screen was run as `fingerprint.py extract --tasks task156` and `screen --focus task156`
  against the cached corpus, because the full re-extract unpacks every build's pack and the largest needs 173 MB
  this machine's disk does not have: 127 builds screened, 0 pairs promoted; `guard.py people`: no BLOCK.
- `leak.py --asof 2026-11-06`: REVIEW, no LEAK, each line ruled. Sweep 4: the schedules', the programme's and the
  tariff's words (schedule, record, register, service, forecast, minutes, status, supply) are those documents' own
  vocabulary, and none names power-ups, uptime, pillars or what the RC50's service does to other units. Sweep 6: the
  programme lists its twelve hubs with works dates and serials, and the register, the visit schedule and the work
  orders name every hub because they are about every hub; none ranks hubs on 2027 availability. Sweep 9: the 2027
  plan sheet's visit dates, forward by nature. Sweep 11: the shell-quota WARN. Files leak.py flagged that may be named
  to the reader: asset_renewal_programme_2027.pdf, charge_point_register.xlsx, planned_maintenance_schedule.xlsx and
  work_orders_2023-2026.xlsx (sweep 6), planned_maintenance_schedule.xlsx (sweep 9).

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
- Architecture 2 (the PS03 overflow replay with each day's own water table), returned FAILED_TO_STUMP on 2026-11-07:
  both responses landed the hold call. Response 1 replayed 2004 to 2023 and filed 48 overflows against the 40 the
  consent allows, then 2 after the upgrade; Response 2 filed the same hold. Any full-record replay with the subdivision
  already broke the consent, so the decisive step (each replay day's own water table) was never needed. Lesson: the easy
  route has to be the one strong solvers actually file, and it has to land on the wrong side; a count of rare
  exceedances spreads with every modelling choice, so the call now sits on a mean quantity whose naive family is tight.
- Judge round 1 (2026-11-07, FIX_NOW on the asks; the call forced, Gate G analytical_non_defect, Gate H pass). Ask A's
  window read literally dropped the platform councils' last run (a 2 July 2026 date in the period-end column): FP-04 now
  files the record's own convention (a pay period ends on a Sunday and is paid later that week; credited to the year it
  ends in), naming no platform and no weekday the advices carry. Ask B's unit was open (raw, per invitation and day, or
  per organiser, invitation and day): the asking sentence now files it (a visit two organisers made counts for both, a
  moved booking once as held). Both asks were scoped to the 30 councils the branch covers while the prompt read as the
  round: cut to the round's 24, the regional platform's twelve councils re-sited inside the round on the same pay
  cycles, so no in-round figure moved. Ask 1's turnout figures had no rounding and a refit evaluating members at the
  extract sat about 0.7 points under: the guide now files each member as they will stand when the ballot period closes
  and the tracker files that period (1 to 15 March 2027); whole-per-cent figures were not adopted because five councils
  sit within 0.05 of a half point (Corrigan Valley 62.53, Halston 59.53, Pellham 58.49, Rosedene 45.51, Underhill 40.54),
  so a worksite-effects refit (lift 1.027) can cross a rounding edge; the prompt asks only whether each council reaches
  half, the side being determinate under every refit. freeze.py: the main side unmoved; the twelve out-of-round ask
  figures and block 4's turnout percentages were dropped by the repair (allowed, this line).
- Hardening noted, not applied (the judge rated stump power moderate to good: a model that fits the delegate term lands
  the call): ship the 2026-28 term as the organising coordinator's separate July 2026 election return rather than a
  sheet of the delegate register, so the register a solver opens holds the terms the online votes cover and the new
  term sits in a file read for its own purpose; the call, the stump and every figure would stay frozen.
- Judge round 2 (2026-11-07): DETERMINISTIC, the call reproduced with 6 points either side and no respecification
  flipping a council, stump power moderate to high. Before ship: step 8 reworded (the golden keeps the later, last
  updated row of a moved booking); the xlsx inputs' creator and last-modified-by set to the branch, the body that
  issues them; the 2021 declarations given the Producer of the LibreOffice release current at their June 2021 export
  (7.1; the info dictionary is the last object, so startxref moves and every object offset is asserted unchanged), the
  other four PDFs dated after 24.2's February 2024 release; and the hardening above applied: the 2026-28 term now ships
  as `delegate_election_return_2026.xlsx`, the returning officer's return, and `delegate_register_2018-2026.xlsx` holds
  the terms to 2024-26. No graded figure moved (freeze.py); the input gates hold (17 files).
- Surface at ship promoted three pairs on card axes alone: task157 (back to back, the same domain and objective; a
  petition sample's pair defects, not a turnout forecast, differentiated on the card), task154 (the calibration form
  realised_outcome_roster repeated two builds apart: redrawn to counterparty_acknowledgement, the agent's declared
  results being a counterparty's record) and task265 (left truncation in a descriptive survival estimate,
  differentiated on the card); heart PASS; left for the author's adjudicated clone check.
- Architecture 3 (the union branch's protected action ballots, each member read with the delegate in post at the
  ballot): FAILED_TO_STUMP on the portal 2026-11-07, both responses on the golden 11 councils. Both put worksite
  delegate coverage in the turnout model from the start and evaluated it at the ballot close with the 2026-28
  delegates, so the decisive step was the forecaster's reflex (a recorded covariate's forward value), and the July
  2026 election return, read by nothing else, announced it. Re-rooted to architecture 4 in a new domain and world.
- Architecture 4 draw screens (2026-11-08), each rejected before any card or data: vacancy chains through a
  fixed-post hierarchy (dead in task174's and task137's notes, and a stock-and-flow check of posts finds it); a
  programme's lead-in audience (task115 and task174); one facility's overflow into a sibling removed by an expansion
  (task308's reader named railheading and the full car park's hidden demand, and the swap reads the same for wards
  or car parks); ward acquisitions per colonised patient-day (task181: infection prevention's own reflex); errors
  per interruption or per handover (task198 and task173); wear accrued only in hours inside a band after a duty
  change, and pump failures per start after a control change (task307's driver); admissions that rise with spare
  beds (a filed bed opening prompts the question, and the forecast needs a fixed point whose estimator forks);
  speculative double bookings (the hygiene battery's de-duplication reaches it and the identity match is Layer 1);
  bus headways under a denser timetable (task308's probe replayed the operation and carried every knock-on).
- First prototype of this draw (hangs on days since power-up, any site-wide power-down a reset): the parameters put
  every hub below 99 per cent; the legacy cabinet repairs now isolate the hub every few weeks, hangs start only after
  about 75 days, and the high-power units sit near 99.5 per cent on the record.
- Hang restarts isolating the whole hub: the units then restart one another and the programme hubs stay above 99 per
  cent; a hung unit is restarted at its own breaker, and only the legacy unit's cabinet repairs, planned visits and
  supply interruptions restart the whole hub.
- Three hubs whose legacy units rarely needed the cabinet opened, failing on both routes: the hubs' legacy repair
  counts then predict the high-power hangs across hubs, and a hub covariate (legacy units at the hub, or their
  repairs) would extrapolate to the golden, architecture 3's failure again; every hub now has exactly one legacy unit
  with cabinet repairs of 10 to 12.5 a year, and the hubs that fail on both routes are three coastal hubs whose
  high-power units suffer ordinary corrosion faults.
- The learner given the hub's legacy jobs in the last 60 days, the days since its last legacy job or the days since
  its last planned visit (prototype, clean truth): none reaches the golden; at the programme hubs they carry 0.7, a
  noisy 0 to 1.4 and 0.4 to 0.7 hangs a unit-year against about 3.3, so each files the default path's set.
- Prototype 7 (the RC50's cabinet repairs at random, 10 to 12.5 a year, every unit at a hub on one pillar): the
  hub-year count of the RC50's work orders predicts the HX150 hangs (z of minus 4.8), and the Poisson model carried at
  the programme's zero files the golden plus a rural spur hub; the count of pillar power-downs files the golden
  exactly. A covariate's forward value lands the call, architecture 3's failure again.
- Prototype 8 (motorway visits two-monthly only from April 2024, rural spurs at 4.5 interruptions a year): the
  full-covariate model filed the naive set with programme hubs 0.01 to 0.3 from 99, a coin flip per hub over redraws.
- Prototype 9 (the coastal hubs' HX150 units on their own pillar, the RC50's repairs still random): the model on the
  RC50's work orders alone still filed the golden exactly; the random repairs carry the signal however the pillars sit.
- Prototype 10, adopted: the RC50's cabinet service is monthly, so its work orders a year carry no hang signal (z of
  0.3) and the HX150 units on its pillar never run 75 days; the hubs whose HX150 units sit on a pillar of their own
  carry every hang on record. Two inland hubs share that arrangement with the three coastal ones, because a record in
  which only coastal units ever ran long could not tell the sea air from the uptime (the deciding configuration has to
  be on record off the coast).
- Ask screens refused: double counting on a meter shared by two connectors (a billing defect a real operator fixes, so
  planted); tariff re-rate copies with new session IDs (a near-duplicate the battery's de-duplication reaches); a hub
  code renumbering (the battery re-derives the code from the charge point); meter replacements to break a register
  shortcut for Ask B (each needs a work order in a main-call file, an ask organ there), so a solver who takes each
  unit's register advance over the window keeps Ask B.
- The first cut's register opened on its Charge points sheet: leak.py sweep 12 read the first two rows' cells (the
  units' IDs, makes and models, which the programme names) as column names and called the programme a dictionary
  (LEAK); the register now opens on its Hubs sheet, the order an asset team keeps it in, and no figure moved.
- The full-covariate model before the RC50's work rose with the coast (the RC50's repairs as random at every hub): it
  filed 11 of the 12 on the clean truth, because the hang hubs' RC50 jobs ran low by chance and the zero at the
  programme hubs extrapolated far below the record; the RC50s at the five own-pillar hubs now need about twice the
  repairs (the coastal units' corrosion, the inland pair's 2017 units), so its removal lowers that model's forecast.
