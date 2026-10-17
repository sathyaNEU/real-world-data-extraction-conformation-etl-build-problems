# task155: Kellaway's relief crew for the four trading weeks to Christmas Eve 2026 (architecture 1)

Private, never ships. A new build (wave 5), numbered from seed FC26. The seed (which of eight Australian grocery stores
gets the one 25-person relief crew for the four trading weeks to Christmas Eve, and the crew hours it will work there)
was read at its header and Situation only. Its world, decision and quantity are kept. Its borrowed-cover mechanism (the
workforce system's offer order, own casuals by seniority then cluster casuals, retrying) ships only as system behaviour
in the call-in module's own notes, and executing it literally needs each casual's chance of saying yes, which no shipped
sentence gives. The placement standard's estimand (the crew goes where it will work the most hours that would otherwise
go unworked) is filed as the WHAT. The pitfall is re-found from how a casual answers a call-in: an offer that carries on
from the casual's own rostered shift at the same store costs no extra trip to work and is taken many times as often as
one that needs a separate trip in.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task155.json`, architecture v1; `guard.py check` PASS, one NOTE (`test.same_driver_older`, differentiated against task117, task137, task37, task44 and task97 in the card); nearest driver 0.04 (task98 v2, lineage) |
| Domain / task type | `economics-econometrics`, task type `discrete-choice-limited-dependent-variable-modeling` (serves Forecasting): each open shift's chance of going unfilled is the product of its eligible casuals' accept-or-decline choices, a binary labour-supply decision at the extensive margin with a fixed cost per trip to work, estimated on the offer log and aggregated over the published roster |
| Objective | Forecasting & Predictive Modeling: the hours each store's call-ins will leave unworked in the four trading weeks 27 November to 24 December 2026, a window not begun at the as-of date (Friday 13 November 2026, the day after the Christmas rosters were published) |
| Shape | `09` (funnel): the call (one store of eight, and its crew hours) carried by row-set asks on each store's call-in funnel and roster; criteria counted in `## Ask sheet` |
| Decision | `pick_one_of_n`, answer unit `named_option` (the store), with the crew hours it will work there to the nearest 10 |
| Mechanism | gap time (decisive: the history's offers seldom sat against the offeree's own rostered shift, and the Christmas roster's Werribee uplift does) with population (the register's fill rate is struck over the call-ins raised, mostly absences at short notice, not over the Christmas open shifts); pattern E (conditioned yield: the split by whether an offer carries on from the casual's own shift is absolute, rebuilt by joining each offer to the roster, and no column names it); generators G14, G6 (the Christmas pool's offers move against the history's mix on that property), G7 (offers go out 07:00 to 21:00 local and a casual on shift answers when the shift ends); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `field_method` (a discrete-choice model of labour supply with a fixed cost of a trip to work); `own:fixed-cost-of-a-trip-in-extra-shift-take-up` |
| Layer 1 | timestamps in UTC in the workforce system against store-time rosters across the daylight-saving changes of October 2025, April 2026 and October 2026; two staff keys (the workforce system's person code and the payroll employee number, a rehire getting a new number); the roster export's layout changed when rostering moved into the workforce system in February 2026; store names, location ids and cost centres; shifts ending at midnight written 24:00; the effective-dated home store; the unpaid 30-minute meal break on shifts over five hours; re-offers written as new call-ins, given-back fills raised again and an absence reported twice (the asks' records); the full inventory is in `## Layer 1 inventory` |
| Furniture | forum `operations_desk` (the workforce planning desk places the crew), forcing event `season_or_peak` (the four trading weeks to Christmas Eve), organisation family `retailer_or_ecommerce`, role family `capacity_planner` (the workforce planning manager), context artifact `capacity_report`, calibration `none`, opening `question-first`, question form `which` |
| Spine | `callin_offers_20250829_20261112.csv`, the workforce system's offer history report, shifts 29 August 2025 to 12 November 2026 (one row per offer of one call-in shift to one casual, with the response), 139,549 rows; constructed |
| Deliverables | `relief_crew_placement_xmas2026.pdf` (a one-page placement brief with the chart of each store's expected unworked hours) and `relief_crew_xmas2026.xlsx` (the working and the ask tables); the format set is in none of the last three builds |
| People | drawn with `guard.py names --geo "Australia, Victoria" --seed 155` and checked clean of first-name repeats: Beth Hill (workforce planning manager, owner of the placement standard), Meredith Stevens (workforce systems lead, the call-in module notes and the extract file list), Kristina Patel (payroll and HR systems analyst, the casual register notes), Belinda Friedman (general manager, retail operations, signatory on the standard); the requester is in no file and not in the prompt |
| World | Kellaway's (checked: no Australian grocer, supermarket or retailer trades under the name), a family-owned chain of eight Victorian stores: Altona, Werribee, Sunshine and Williamstown (west cluster), Box Hill, Camberwell and Ringwood (east cluster), Ballarat (no cluster) |

**Guard.** The first card (gap population first) met two BLOCKs: `test.same_puzzle_older` against task228, task28,
task30, task32 and task53, and `test.same_driver_older` against the task124 lineage. The gap order was wrong as well as
spent: the decisive gap is time (what the history's offers were against what the Christmas roster offers), and the
population gap is the frame. With time first the puzzle triple (time, E, pick_one_of_n) is in no build; the driver
triple (time, E, forecasting) is in five older builds, each differentiated on the card in one line (none of them in
the batch window). The personas first drawn (James, Christine, Shane) repeated first names in task108, task104 and
task125 and were redrawn; the pptx and xlsx set repeated task156, the docx and xlsx set task264, so the brief is a PDF.

**Same-puzzle and same-driver tests.** Gap time, pattern E, decision `pick_one_of_n`: no build carries the triple.
Gap time, pattern E, Gate G `forecasting`: task117 (closed operations replayed with dependent start times), task137
(a repricing share conditioned on a unit class rebuilt from entry cohorts), task37 (a withheld coupling rule recovered
from an outcome roll), task44 (a moderator measured over a prior instance of the window) and task97 (a place's history
carried across occupants). None conditions a take-up on the taker's own scheduled work at the same place.

**Abstraction test.** Stripped of nouns: a member's chance of taking on an extra task is high when the task carries
straight on from work it is already scheduled to do at the same place and low when it needs a separate start, so the
share of a forward period's open tasks that get taken rests on how many sit directly against work already scheduled; a
take-up rate or model measured on a history where open tasks seldom sat against scheduled work writes off the site whose
open tasks do.

**Kinship, answered (the five builds the brief names, and the lane's nearest).**
- task106 nets each candidate against a shared, finite pool of spare capacity and the double booking is the stump. Here
  the sister-store casuals are a pool the stores share, but the standard counts only the placed store's hours, nothing is
  summed across candidates, and the decisive split is in each casual's answer, not in a pool that two winners draw on.
- task140 strikes a residual after higher reservations, one of which depends on the tier promised. Nothing here is a
  residual or a reservation; the crew's hours are the open shifts of one store.
- task148 drains a queue by abandonment, with patience censored for the served. Here no call-in leaves a queue: the
  cascade stops at the first yes, so later casuals on the list are never asked, but that stopping is the system's
  behaviour, every response routes it, and the decisive step is the price of an offer, not a waiting time or its
  censoring.
- task16 floors each cell's shortfall at zero before summing. Nothing here nets surpluses across cells; a filled shift
  at one store fills nothing at another.
- task150 carries steady arrivals that a ratio on the base misprices. Nothing here arrives at a steady count; the
  forward exposure is read from the roster already published.
- task149 (the lane's last forecasting build) reads a hazard per hour within each unit against work speed. Here the
  property is between offers, not within units over time, and the forward period's mix comes from the published roster,
  not from a plan's implied speed.

**WHAT screen (stumping 1.2).** The decisive step estimates how a casual answers an offer that carries on from their own
rostered shift; it settles none of the estimand's five parts, each filed in the shipped text: population (the open
shifts listed in each store's published Christmas roster), outcome (paid hours of those shifts that call-ins would leave
unfilled), window (the four trading weeks 27 November to 24 December 2026), unit (paid hours, store by store) and
comparison (the eight stores, the crew at one, its hours the store's open shifts). No shipped sentence says how an
offer's acceptance depends on the casual's own roster, and the call-in module's notes say only how offers are made.

**Data-native sentence.** Kellaway's call-in module offers each open or vacated shift to the store's own casuals in
order of service date, then to sister-store casuals who opted in, one at a time, 07:00 to 21:00, and records every
answer against the casual's person code in UTC; joining those offers to the published rosters on the payroll number
shows that an offer starting as the casual's own shift at the same store ends, or ending as it starts, is taken many
times as often as one that needs a separate trip in, and in the 2026 Christmas roster Werribee's uplift is listed open
from 2 pm and from 6 pm until midnight, against the 8-to-2 and 2-to-6 shifts its new university intake already holds,
while Camberwell's online-picking uplift sits 10 to 4 on weekdays, when its school-age casuals are in class and almost
no casual's shift abuts it.

**Sources read, one line each.**
- Seed FC26 header and Situation (`status.py task155`): the world, the 25-person crew, the four weeks and the crew-hours
  quantity; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: the forecasting drivers on file price units, cohorts, queues, capacity
  residuals and hazards; none conditions a take-up decision on the taker's own schedule.
- The kin cards the brief names (task106, task140, task148, task16, task150) and the lane's task149, answered above.
- `two-layer-task-design.md`: "the right comparison group" and "the data's real structure" are the frames (the offers
  that carry on from a shift are a group the history barely holds and the forward roster is full of).
- `layer2-rigor-patterns.md`, economics: discrete choice on the extensive margin with a fixed cost of participation
  (the labour-supply reading of a trip to work) is the field's own method, learned, not copied.

## Default path

Figures from the built pack (`generator/routes.txt`, written by `checks.py`; the golden from `generator/figures.json`).

1. Read the placement standard (the crew works every shift its store's published Christmas roster lists open; it goes
   where it will work the most hours that would otherwise go unworked), the call-in module notes, the call-in register
   and the published Christmas rosters.
2. Sum each store's open paid hours in the Christmas roster: Werribee 3,254, Box Hill 2,602, Altona 1,770, Sunshine
   1,378, Ringwood 1,140, Camberwell 1,092.5, Ballarat 876 and Williamstown 641.5.
3. Take each store's share of call-in hours filled over the register's rows in the ordinary weeks (29 August to
   27 November 2025 and 25 December 2025 to 12 November 2026, last Christmas's weeks set aside): Werribee 0.33, the
   other stores 0.37 to 0.61.
4. Multiply each store's open hours by the share left unfilled and place the crew at the largest.

Ends on: Werribee, 3,250 crew hours (about 2,190 of them otherwise unworked, Box Hill next at about 1,100, Camberwell
fifth at about 590).

Golden: Camberwell, 1,090 crew hours (about 670 of them otherwise unworked, Ringwood next at about 400, Werribee about
320): each open shift's chance of going unfilled is the chance every casual the module would offer it to says no, each
casual's answer priced on whether the shift carries on from their own rostered or booked shift at that store, on the
December season and on the other terms the offer log shows, run through the module's offer order and limits.

## Stump sentence

Taking each store's call-in fill rate from the register (ordinary weeks or last Christmas, by posting or by shift), or
fitting each offer's acceptance on shift time, length, notice, sister-store travel, weekly hours, the December season
and whether the casual is rostered that day, and applying it to the open shifts in the published Christmas rosters
sends the crew to Werribee, its 3,250 open hours the crew hours; the step that lands it there is pricing every offer as
a separate trip to work, when a casual whose own rostered shift at that store ends as the open shift starts, or starts
as it ends, takes it many times as often, and Werribee's Christmas uplift is listed against its own casuals' rostered
shifts, so Camberwell, whose weekday daytime uplift almost no casual's shift abuts, is the store, with 1,090 crew hours.

## Three rules

- Task type: discrete-choice-limited-dependent-variable-modeling (Economics & Econometrics), which serves Forecasting: each open Christmas shift's chance of going unfilled is the product, over the casuals the call-in module would offer it to, of each casual's chance of saying no, a binary choice estimated on the offer log and aggregated over the published roster.
- Domain test: the deciding quantity is each store's expected unfilled open hours, built from a labour-supply choice at the extensive margin: taking an extra shift carries a fixed cost of getting to work that an offer carrying straight on from the casual's own rostered shift at the same store does not, so the field's estimator is a choice model whose specification carries that participation cost, fitted on every offer and its answer and applied to the open shifts' position against each casual's rostered shifts.
- Swap: "which of eight power stations gets the one maintenance crew for the four weeks to Christmas, on the megawatt-hours its standby units would leave unserved" keeps the arithmetic of open hours times a shortfall rate, but no standby unit chooses whether to make a trip, so there is no fixed cost a schedule can remove and the construction that decides the call has nothing to act on.
- Layer 1: the workforce system (KWS) writes offer and call-in times in UTC while rosters are in store time, across the daylight-saving changes of October 2025, April 2026 and October 2026; offers carry the KWS person code and rosters the payroll number, and payroll issues a new number on rehire; the roster export changed layout when rostering moved into KWS on 27 February 2026 (the legacy export dated dd/mm/yyyy with store names and span hours, the KWS export ISO dates, location numbers and paid hours); the Christmas roster writes shifts ending at midnight as 24:00; payroll keeps the home store effective-dated while KWS holds only the current one; the unpaid 30-minute meal break on shifts over five hours; a call-in that runs out of casuals closes UNFILLED and the shift is raised again as a new call-in at 07:00 the next day; a casual who gives back an accepted call-in reports an absence and the shift is raised again naming them; an absence reported both in the app and by phone raises two call-ins for one line; KWS offers no shift within an hour of the casual's shift at another store. Each comes from how the system records its own work, and none carries the call.
- Layer 2: field_method, the labour-supply choice model: the methodological choice that flips the call is specifying the participation cost, separating offers that carry on from the casual's own rostered shift at that store from offers that need a separate trip, estimated on the history where such offers are about one in sixty-five (2,159 of 139,549) and applied to a Christmas roster where every one of Werribee's open shifts could be taken that way.
- Decisive step: estimating the take-up of an extra shift with the fixed cost of the trip to work in the model, so that an offer starting as the casual's own rostered shift at that store ends, or ending as it starts, is priced as staying on rather than as a separate trip, and applying that to which casuals' published Christmas shifts each open shift abuts.
- Not semantics: no field, code, column or definition marks an offer as an extension; the property exists only when each offer's shift is joined, through the person code and payroll number, to the casual's own roster that day, and an analyst who reads every field and definition correctly is left with a fill rate or an acceptance model on the offer log's own columns, both of which send the crew to Werribee.
- Not rule application: no filed rule or procedure says how a casual answers; the call-in module notes say who is offered a shift, in what order and when, and executing them literally needs each casual's chance of accepting, which the analyst must estimate; executed with any estimate that prices every offer as a separate trip, the notes and the standard file Werribee, so the step that reaches Camberwell is the model's specification, not a rule.
- Analyst test: a strong analyst who reads every field and rule correctly computes each store's call-in fill rate (ordinary weeks or last Christmas, by posting or by shift) or fits an offer-level acceptance model on shift time, length, notice, sister-store travel, weekly hours, the December season and whether the casual is rostered that day, applies it to every store's open Christmas shifts and sends the crew to Werribee with 3,250 crew hours, because none of those routes separates an offer that carries on from the casual's own rostered shift from one that needs a separate trip.
- Estimand: the relief crew placement standard (`relief_crew_placement_standard.pdf`) files every part: the population (the shifts each store's Christmas roster published on 12 November lists open, which the crew works and which are then not posted to call-in), the outcome (the paid hours of those shifts the store's call-ins would leave unfilled, counted as if the crew were at no store), the window (the four trading weeks Friday 27 November to Thursday 24 December 2026), the unit (paid hours, net of the unpaid meal break) and the comparison (the eight stores, the crew at the one with the most, its crew hours the paid hours of that store's open shifts).
- No decoy: nothing is planted to be caught; no memo, briefing, manager's request or stakeholder figure argues for a store, no document ranks the stores, and the 2025 crew's shifts on Werribee's 2025 roster are last year's history, which the standard does not mention and the call does not read.
- No certified replay: no certified, published or approved figure exists for a method to reproduce; the acceptance split is estimated from the offer log and the rosters, and nothing in the pack scores one model against another.
- Lesson: a model of extra-shift take-up has to carry the fixed cost of the trip to work, because a rate or model measured where offers seldom carried on from the worker's own shift does not transfer to a roster where they mostly do; no build on file conditions a take-up decision on the taker's own schedule at the same site (the duplicate check's nearest text scores 0.05, task149's stump).

## Layer 1 inventory

Each item is how the chain's own systems record their work; each is asserted neutral for the call in `checks.py`
(R2), or ledgered to the asks it moves.

| Item | Written by | Where | Natural mishandling | Assertion |
|---|---|---|---|---|
| times in UTC against store-time rosters, across the daylight-saving changes | KWS | register shift and raise times; offer and response times | offer times read as store time | R2.1 (the call holds); SF6; Ask A/B hazard HA1 |
| two staff keys | KWS person code; payroll employee number | offer log, people extract; roster lines | offers joined to rosters on the wrong key | R1b (the term is built through the payroll key) |
| a rehire under a new payroll number | payroll | payroll register `previous_employee_no` | earlier numbers not followed | R2.6 (the call holds) |
| the roster export's layout change on 27 February 2026 | the legacy rostering tool, then KWS | legacy export (dd/mm/yyyy, 12-hour times, span `Hrs`, store names); KWS roster lines (ISO dates, location ids, paid hours) | the legacy export left out | R2.4 (the call holds) |
| store names, location ids and cost centres | legacy tool, KWS, payroll | the three sources; `stores.csv` maps all three | stores left unmapped | R2.2 and R2.4 run through the map |
| shifts ending at midnight written 24:00 | KWS roster report | the Christmas roster (Werribee only) | 24:00 read as the same day's 00:00 | R2.7 (no crew-hours line touches them) |
| home store kept effective-dated in payroll, current only in KWS | payroll; KWS | payroll cost-centre history; people extract | home store read current | R2.2 (the call holds); Ask B filed reading (the transmittal: the cost centre on the shift date), the current-store reading asserted off (B S1) |
| the unpaid 30-minute meal break on shifts over five hours | the enterprise agreement | EA summary; the legacy export's span `Hrs` | span hours as paid | R2.3 (the call holds); SF3; HA2 |
| a call-in whose list runs out closes UNFILLED and the shift is raised again as a new call-in at 07:00 the next day (filed in the module notes) | KWS register | call-in register | every row a shift; the identical open lines a roster lists merged with the re-raises | Ask A filed readings S1 and S1b asserted off; device A1's over-cleaning half (S2); the golden reads no posting outcome (SEP1) |
| a given-back fill keeps its FILLED outcome and the shift is raised again as an ABS call-in naming the casual (filed in the module notes) | KWS register | call-in register | the first fill kept as cover, or its re-raise counted as another shift | Ask A filed readings S3 and S3c asserted off; Ask B S3c; R2.5 for the call |
| an absence reported both in the app and by phone, two ABS call-ins for one vacated line, the second closed UNFILLED when the first fills (6 per cent of absences) | KWS register | call-in register | each call-in raised other than at 07:00 counted as a shift | Ask A device A3 (S3b); the golden's vacated lines are a set (SEP1) |
| no offer within an hour of the casual's shift at another store (filed in the module notes' skip rule) | KWS | offer log against both roster exports and the register's fills | none: the rule holds on every offer | RZ11 (0 of 139,549 offers); the golden's forward cascade applies it |

## Readability screen

Six tests per rung: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | Verdict |
|---|---|---|---|---|---|---|---|
| R0 store fill rate from the call-in register times the Christmas open hours | the standard names the open hours and the unworked hours, which invites it | the register's outcome column | yes, the natural reflex | none | none | one ratio | readable |
| R1 last Christmas's fill rate, by posting or by shift | the dates in the standard invite the season | the register's dates and raise times | yes, the season reflex | none | none | one ratio on a subset | readable |
| R2 offer-level acceptance model on the log's columns, eligible casuals from the Christmas roster and the module notes | the module notes describe the offer order and eligibility | the offer log's response column and shift fields | yes, for a strong analyst | none | none | no | readable |
| R3 (decisive) the take-up model carries the trip cost: offers that carry on from the casual's own rostered shift at that store priced apart | no sentence names a casual's own shift as a term in the answer | no column marks an extension; it exists only through the person-code to payroll-number join to each day's roster | no: the reflexes add a store, season, notice or same-day term, and the same-day term still files Werribee | none scores a model | the battery finds nothing; every row is valid | no: an interval join across two files and two keys | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the four trading weeks to Christmas Eve" | Friday 27 November to Thursday 24 December 2026, four roster weeks, local dates | the calendar weeks of December, or to 25 December | same call (Christmas Day is closed; no roster line falls outside 27 November to 24 December) | the standard's dates, asserted in checks.py |
| SF2 | "the hours the crew will work there" | the paid hours of every shift the store's published Christmas roster lists open | the expected otherwise-unworked hours | different figure | the standard: the crew is rostered into every open shift and works them |
| SF3 | paid hours | span less the unpaid 30-minute meal break on a shift over five hours | span hours | different figure, same call | the enterprise agreement summary's meal-break clause |
| SF4 | "open" | a line the published roster lists with no employee | a line later vacated by an absence | same call | the standard: absences go to call-in as usual, the crew takes only the published open shifts |
| SF5 | the counterfactual | each store's open shifts posted with the crew at no store | the crew at the runner-up | same call (the runner-up's casuals are not the ones Camberwell's shifts reach) | the standard: counted as if the crew were at none, asserted |
| SF6 | time zone | shift dates and times in store time, offer and call-in times in UTC | everything in store time | same call | the module notes' sentence on times, asserted |
| SF7 | the candidates | all eight stores, Ballarat included | the seven cluster stores | same call | the standard lists eight |
| SF8 | the roster version | the Christmas roster as published on 12 November 2026 | a later edit | same call (no later edit ships) | the standard and the workbook's header |
| SF9 | summary of the forecast | the expected (mean) unfilled hours | a median or a percentile | same call, asserted on the simulation's runs | the standard's "the most hours" on the best forecast |
| SF10 | crew capacity | the crew can work every open shift at any store (25 people at up to 38 hours a week) | capacity binds | same call | the standard's crew paragraph and the EA's hours limits; asserted by rostering 25 crew greedily into every open shift of each store under 11 paid hours a day, 38 a week and 10 hours between days |
| SF11 | which casuals a shift reaches | the store's own casuals, then sister-store casuals who opted in | every casual in the chain | same call | the module notes' offer order |

## Ladder

Figures from the built pack (`generator/routes.txt`, every route recomputed from `target/` by `checks.py`).

| Rung | Construction | Winner | Margin | Camberwell's place |
|---|---|---|---|---|
| R0 | the register's fill share over the ordinary weeks, by posting or by shift, times each store's Christmas open hours | Werribee | 1.64 to 1.99 | 5th or 6th |
| R1 | the same share over last Christmas's weeks | Werribee | 1.22 to 2.11 | 6th or 8th |
| R2 | an offer-level logit on the log's own columns (shift length, finish, start, Sunday, notice, a repeat offer, sister store, weekly hours, the Christmas weeks, age band, home store), with or without a rostered-that-day term, static or run through the module's cascade | Werribee | 1.21 to 2.21 over Camberwell | 2nd or 3rd |
| R3 (decisive) | the same model with the trip-cost term: an offer that starts as the casual's own rostered or booked shift at that store ends, or ends as it starts, priced apart from a second, separate shift that day | Camberwell | 1.74 to 2.22 | 1st |

- Position and dominance: every construction without the trip-cost term files Werribee (12 of 12 in `routes.txt`: the
  open-hours sum, four register routes and seven offer models); every construction with it files Camberwell (6 of 6,
  static or run through the cascade, with or without age, store or December terms), as do the golden (24 runs, 1.69
  over Ringwood) and the world's own Christmas (32 runs, 1.53 over Sunshine).
- Hardening before the cut (`stumping` Part 8, the winner's default-path rank worse): Box Hill and Altona list
  Christmas uplift against their own casuals' afternoon shifts as Werribee does (96 and 79 per cent of their open
  shifts reachable by staying on), so Camberwell is sixth on open hours, fifth or lower on every register route and
  second or third on every offer model, at least 1.21 behind the leader; asserted (R3a, L1 to L3).
- The weakest wrong route is the static model with one rostered-that-day term (Werribee 849 against Camberwell 703,
  1.21; 1.25 before this world's last re-draw, 1.36 and 1.21 on seeds 156 and 160). The term pools the 2,159 offers that
  carry on from the casual's own shift (33 per cent taken) with the 16,224 offers of a second, separate shift on a
  rostered day (0.26 per cent taken), so it reads a casual already rostered that day as a little less willing than one
  on a day off (4.2 against 4.9 per cent); the second-shift cell's take-up is what moves this route (`## Tried and
  rejected`).
- Worth on the graded figures: the store and the crew hours both change when the decisive rung is undone (Werribee
  3,250 against Camberwell 1,090); every critical component (the 33 against 4 per cent split, the share of each store's
  open shifts its casuals could take by staying on, Camberwell's 1,090 open hours) is upstream of the call.
- Strength against the opponent (lesson 2): P(one strong solver builds the trip-cost term and applies it to the
  published roster) is put at 0.15 (about half take a register route, a third an offer model on the log's columns, a
  sixth join the rosters and test adjacency); P(both top responses) about 0.04 with correlation; the free gates assert
  every natural route's verdict.
- Stability: the deciding split rests on 2,159 offers and 721 acceptances; a one-sigma move in the trip-cost
  coefficient either way keeps Camberwell first (2.05 and 2.11, L4).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the open lines of each store's published Christmas roster | filed in the standard (section 4); SF4 (a line is OPEN exactly when no employee is on it) |
| 2 | Unit of account | paid hours, store by store | the standard and the prompt; the meal break in the EA summary |
| 3 | Attribution window | 27 November to 24 December 2026 by local shift date | the standard; SF1 (every Christmas line falls in 27 November to 24 December, none on Christmas Day) |
| 4 | As-of dating | the roster as published 12 November, the extract to 12 November, as-of 13 November | the standard and the transmittal; RZ3 (no document dated after the as-of) |
| 5 | Version basis | the published roster; the KWS people extract as at 12 November | one version of each ships (SF8) |
| 6 | Denominator | none: the call is a count of hours | n/a: no share is graded on the call |
| 7 | Weighting | hours-weighted unfilled shifts | the standard counts hours |
| 8 | Window length | the history the analyst fits on | the golden fits on every week; C8: fitted on ordinary weeks alone, the trip-cost model keeps Camberwell |
| 9 | Boundary inclusivity | 27 November and 24 December inclusive | the standard; SF1 (no line falls outside the window, so either reading counts the same lines) |
| 10 | Rounding path | crew hours summed unrounded then rounded to the nearest 10 | the prompt; C10 (the exact sum sits inside its bin, not on an edge) |
| 11 | Tie-break | none needed | R3b: the golden's leader by 1.2 or more over the runner-up |
| 12 | Maturity and censoring | the cascade stops at the first acceptance, so later casuals are never asked | the route table: every offer-level model, static or run through the cascade, and every register route keeps its verdict (R3a, R3b) |
| 13 | Order of operations | estimate, then apply to eligible casuals per shift | static against the cascade simulation, both in R3b |
| 14 | Row order | none matters | C14 (the fit on a permuted offer log) |
| 15 | Duplicate resolution | reposted call-ins are new records; offers keep their own ids | by construction: the golden reads offers and roster lines, never the postings' outcomes (SEP1) |
| 16 | Identity normalisation | person code to payroll number, rehires through the payroll register's previous number | the KWS people extract and the payroll register; R2.6 (rehires' earlier payroll numbers not followed: the call holds) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | hours throughout; times in UTC against store time | the module notes; R2.1 (offer times read as store time: the call holds) and SF6 |
| 19 | Code and status semantics | responses ACCEPTED, DECLINED, NO RESPONSE; reasons OPN, ABS, LVE | the module notes; C19 (NO RESPONSE offers left out of the fit: same call) |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the standard governs the 2026 placement only | the standard's own scope line |
| 22 | Forward window contents | the published Christmas roster for all four weeks | C22 (every store and every trading day) and C22b (the profile in force at the extract gives every casual's windows on every Christmas date) |

## Literal reader

Executed word for word, the standard fixes the population, outcome, window, unit and comparison and the crew hours
(SF1 to SF11 converge); the module notes say who is offered each shift and when, and leave each casual's answer to be
estimated; a reader who estimates it from the offer log on the log's own columns files Werribee, and only one who
builds the trip-cost term from the rosters files Camberwell, so the easy answer comes from an easy method on the same
literal estimand, never from another reading.

## Oracles

None. No control, published figure or reconciliation column ranks the stores or ties under one method; the call-in
register's fill rates are history, not a control, and they agree with every method on the past because the past
seldom put an extension offer to anyone. The history refutes the separate-trip model only on the extension offers
themselves (2,159 offers, 33 per cent taken against 4 per cent of the rest), a cut the default path never makes.

## Ask sheet

**Main call's declared row population:** the offer log's offers (shift fields, person code, offer and response times,
response), the roster lines' start and end times and payroll numbers on the days of offers, the KWS people extract's
person code, payroll number, home store, opt-in and service date, the payroll register's previous numbers and
cost-centre history, the availability profiles, and every line of the published Christmas roster. Device rows in it:
none. The golden reads the call-in register only for fills and vacated lines (SEP1; an absence reported twice vacates
the one line), the call holds with call-in fills left out of each casual's day (R2.5) and with home stores read current
(R2.2), and the asks read neither the Christmas roster nor the offer log (SEP2).

**What the filing settled (judge round 1).** The module notes and the transmittal now say, as how KWS and payroll keep
their records: an open line is put out when the roster is published (OPN) and a vacated line when its absence or leave
is raised (ABS, LVE), except the open lines of the store where the crew is placed (the standard says the same); a
call-in whose list runs out closes UNFILLED and the shift is raised again as a new call-in at 07:00 the next day, so a
shift offered over several days has a call-in for each day; a casual who gives back a call-in reports an absence, the
shift is raised again as an ABS call-in naming them, their own call-in keeps its FILLED outcome and KWS offers them
nothing more that day; KWS keeps times in UTC; a casual's home store on a date is the store whose cost centre payroll
applied that day. Each is a work order the cracker executes, and each other reading is asserted off the golden.

**Ask A. Last Christmas's call-ins by store** (24 figures, paid hours to one decimal place): for each store, the hours of
the shifts it put out to call-in for the four trading weeks to Christmas Eve 2025 (Friday 28 November to Wednesday
24 December), and how many of those hours call-ins covered and how many they left uncovered.
- H18 home: how call-in cover held up at each store last Christmas, the brief's context table beside the call; a
  measure every store carries that the call does not turn on.
- Primary A1 (D6, a ledger at another grain than its name, the over-cleaning half; silent): each shift has a call-in
  for each day it was offered, and the stores also list identical open shifts on one day (Box Hill listed 14 vacant
  4-to-8 pm lines each weekday last Christmas), each its own shift; folding a shift's call-ins on store, date and times
  (with reason and absent payroll number) merges them. Fair: every open line is raised at the roster's publication
  (10:00 on 13 November 2025), a re-raise at 07:00, and the 2025 legacy roster export lists the vacant lines (the
  referee: open postings at publication match the vacant lines at every store).
- Primary A3 (D1, a resubmission that opens no second case; silent): an absence reported both in the app and by phone
  raises two ABS call-ins for the one vacated line, naming the same payroll number, the second closed UNFILLED when the
  first fills (6 per cent of absences, at seven stores in the window); telling re-raises by their 07:00 raise counts
  both. Fair: one person holds one line at a time, so two call-ins for the same shift naming the same absent number are
  one vacated line.
- Hazards: HA1 UTC against store dates (shifts starting before 11:00 on Friday 28 November 2025 sit on 27 November in
  UTC); HA2 the meal break (span against paid hours); HA3 Werribee's open Christmas shifts went to the 2025 crew and
  were never put out.
- Stops (each a complete pipeline in `asks.py`, asserted in `checks.py`): S1 every register row a shift, 23 of 24
  figures off; S1b every row but those closed the minute they were raised, 23; S2 the fold on store, date, times, reason
  and absent number (A1), 24; S3 a give-back's re-raise counted as another shift with the first fill kept, 14; S3b
  re-raises told by their 07:00 raise (A3), 14 (put-out and uncovered hours; covered untouched); S3c a give-back counted
  once with its first fill kept as the cover, 14; S4 UTC dates, 16; S5 span hours, 24; S6 open lines left out, 24; S7
  fills voided by any absence their casual reported that day: the golden, 0 of 24 (KWS offers such a casual nothing
  more that day, asserted). Every golden figure is exact at one decimal (paid hours come in half hours).
- Span: the call-in register, the legacy roster export, the KWS people extract, the payroll register, the EA summary,
  the module notes (6 files); store, shift start and end, reason, absent payroll number, raised, closed, outcome,
  filled by.

**Ask B. Cover across stores last Christmas** (16 figures, paid hours to one decimal place): for each store, the hours of
its call-ins in those weeks covered by casuals from other stores, and the hours its own casuals covered at other stores.
- H18 home: how far stores leant on each other last Christmas, beside the crew's case; a measure every store carries.
- Filed (round 1): the home store is the payroll cost centre on the shift date. 47 casuals have another home store now
  than on 10 December 2025 (Ballarat students moving to Melbourne for university, moves between sister stores); read
  current, 15 of the 16 figures move and Ballarat, which offers to no other store's casuals, shows 127.5 hours of imports
  it never had. A given-back sister-store fill is not cover (credited to its first filler, 3 of 16 move).
- Primary: none of its own since the filing. Ask B moves with A1's over-cleaning (the merged identical lines lose their
  fills, 14 of 16 off) and with the hazards.
- Hazards: HA1, HA2; every register row a shift (5 of 16); a give-back's re-raise counted as another shift (5 of 16).
- Stops: S1 current home store, 15 of 16 off; S3c, 3; the fold (A1), 14; re-raises told by their 07:00 raise: the
  golden, 0 of 16.
- Span: the call-in register, the KWS people extract, the payroll register, the store list (4 files).

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC | KWS stores times in UTC | A, B | the Friday 28 November morning shifts at every store |
| HA2 meal break | the EA's unpaid break | A, B | half an hour per shift over five hours, every figure |
| HA3 the 2025 crew | Werribee's open shifts went to the crew | A | none (Werribee's put-out hours are its absences and leave) |

**Referee.** Ask A: the 2025 legacy roster export's vacant lines count the open shifts put out at publication; Ask B:
the offer order shows who the module treated as a store's own casual on the day. Neither hands over an ask figure.

**Cracker sheet**

| Ask row | Figures | Cracker's path | Cracker's figures kept | Verdict |
|---|---|---|---|---|
| Ask A, last Christmas's call-ins | 24 | each shift's call-ins folded on store, date, times, reason and absent payroll number (the notes' "a call-in for each day" executed on the shift's identity), give-backs voided, store dates, paid hours | 0 | miss |
| Ask B, cover across stores | 16 | the same shifts, each filler's home store the payroll cost centre on the shift date | 2 (Ballarat's two zeros) | miss |

**The other path, and the open risk.** A cracker who tells each re-raise by its 07:00 raise instead of folding on the
shift's identity handles A1 and falls only into A3: it keeps Ask A's covered column and Ringwood's two other figures
(10 of 24) and all of Ask B (16 of 16), 26 of 40, and on that path the pair would sit near 64. The judge's round-1 path
was of that kind. Once the cost-centre and give-back conventions are filed, Ask B carries no silent device of its own,
so this build's ask layer rests on which of the two folds the top responses use; it is flagged for the author as the
case for a `/fix-rubric` pass on Ask B (a device on the fills themselves) if the portal scores the asks high.

Mirror leakage: 5.0 per cent of ask weight on the fold (2 of 40 figures; the mirror is R2, Werribee, and runs the
cracker's ask paths), 65 per cent on the 07:00 path.

Pair ceiling: 31.3 on the fold (the cracker C = 38 + 7 + 55 x 2/40 = 47.8; the best miss S = 5 + 7 + 55 x 2/40 = 14.8),
64.3 on the 07:00 path (C = 80.8, S = 47.8), rerun from the generated rubric.

## Surface screen

`guard.py surface task155` promotes six pairs for adjudication; none carries a hard tell (no shared file name, column
set, same-seed table, invented name or masked prompt wording: Track A rests on the shared folder layout and format mix
alone), and `guard.py heart` passes (nearest text 0.05, task149's stump; nearest driver 0.04, task98 v2). The pack names
Beth Hill, Meredith Stevens, Kristina Patel and Belinda Friedman, the four drawn personas, and no one else. For the
author, who alone runs the adjudicated `/clone-check`:
- task154 against task155 (back to back, surface 0.100): the cards pair economics-econometrics with forecasting and both
  put the decisive gap at time, and both packs ship csv, json, pdf, txt and xlsx with a one-page PDF and a workbook as
  deliverables; the drivers share nothing (task154 revalues each industry's stock over its own holding period to
  separate volume from price in an advance GDP estimate; task155 prices a casual's answer to a call-in on whether the
  shift carries on from their own rostered shift at that store). task154 was registered at 03:13, before this draw at
  09:07, and `guard.py check` passed then; task154 is held at its draw for a different decisive move; the keys here are
  the honest ones (a labour-supply choice model is econometrics, and the call is a forecast) and are not relabelled. The
  card carries a task154 differentiation line.
- task37, task44, task137, task117 and task97 (surface 0.082 to 0.094): the card-level same-driver signature (gap time,
  pattern E, Gate G forecasting), each differentiated on the card at the draw; none conditions a take-up on the taker's
  own scheduled work at the same place, and none shares a file, column set or sentence with this pack.

## Leak sweep

`leak.py task155 --asof 2026-11-13`: REVIEW, no LEAK (`leak_check_report.md`). Each REVIEW line, read:
- Sweep 3 (the call's words in the pack): the placement standard and the module notes carry "relief crew", "work",
  "hours" and the store names because the standard is the placement rule for the eight stores and the notes list the
  call-in clusters; Camberwell appears in each only inside a list of stores, and neither document ranks a store or
  gives a figure for one.
- Sweep 4 (the design note's vocabulary): the transmittal, the EA summary, the module notes and the standard are the
  chain's own documents about rosters, call-ins and pay and share their workaday words (roster, casual, offers,
  payroll); none names staying on, a trip to work, an extension or an offer's position against the casual's own shift.
  The module notes' sentences on a casual's own shifts are skip rules (an overlapping shift; a shift at another store
  ending or starting within an hour) and the give-back rule; they say who is offered a shift, never how a casual
  answers. The notes and the transmittal gained the filed conventions after the round-1 reading, so the reader re-reads
  them at round 2.
- Sweep 9 (dates after the as-of): the Christmas roster lists the shifts of 27 November to 24 December 2026 as
  published on 12 November, the forward window the call is about; the school-terms calendar is the state calendar with
  the term's end and the Christmas public holidays (a distractor). No extract column runs past 12 November (RZ3).
- Sweep 10: no writer signature in any container (INFO); the container audit is clean on the pack and the goldens.

## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is still analytical: the standard files the estimand
  (the open shifts of each store's published Christmas roster, the paid hours of them call-ins would leave unfilled
  with the crew at no store, the four trading weeks, the eight stores) and no shipped sentence says how a casual
  answers an offer; executed with any separate-trip estimate, the notes and the standard file Werribee (R3a, 12
  routes); only the trip-cost term, built by joining each offer to the casual's own roster that day through the payroll
  key, files Camberwell (R3b, 6 of 6). Layer 1 (UTC, two keys and rehires, the layout change, 24:00 ends, the
  effective-dated home store, the meal break, re-raises, give-backs and absences reported twice) is neutral for the
  call: each mishandled reading leaves Camberwell first (R2.1 to R2.7), and the register's records move only the asks.
- **Free gates on the final rebuild.** `checks.py` 76 assertions, 0 failed; `verify.py` 0 failed on its own path;
  two builds byte-identical (15 files) and `target.zip` cut from the final build; `figures_check.py` 64 figures,
  0 absent; `precut.py` exit 0 (49 checks); `voice-check.py` PASS (889 characters); the container audit clean on the
  pack and the goldens; `guard.py heart` PASS (nearest text 0.05); `guard.py surface` six promotions, no hard tell
  (## Surface screen); `leak.py` REVIEW, no LEAK (## Leak sweep).
- **House-fix pass (H1 to H24).** H1 the containers clean. H2 every figure in the write-up and the goldens recomputes
  (`figures_check.py`, `verify.py`), and the note's figures come from `routes.txt` and the checks. H3 the brief read
  figure by figure; its statements about Werribee's February intake and Camberwell's weekday availability are asserted
  (RZ9, RZ8). H4 the zip holds the 15 declared files at its root; the brief's chart opened and read. H5 each ask's
  reading is closed: the asking sentences count shifts and their hours, the module notes file how re-raises and
  give-backs are recorded and the transmittal the home store on the shift date (round 1), each other reading asserted
  off. H6 the memo's rules run over the record (RZ8, RZ9, the 33 against 4 per cent split). H7
  the zip cut from the final rebuild, two builds byte-identical. H8 the brief cites WP-04 section 4 and the EA summary,
  both shipped. H9 the transmittal lists every shipped file but itself (RZ7). H11 one `submission.md` and one
  `prompt.txt`. H12 and H13 `voice-check.py` PASS. H16 only the Christmas roster and the calendar carry dates past the
  extract, both forward by nature (RZ3 for the extract). H18 both asks are context for the placement (last
  Christmas's cover at each store and between stores), neither a second decision. H20 the prompt carries the call-in
  system's own nouns (our eight stores, the relief crew, the placement standard, call-ins, casuals). H21 Kellaway's
  checked against Australian grocers and retailers at the draw. H23 no ask presupposes a non-empty subset (Ballarat's
  zero cover reads 0.0). H24 no file under `target/` says the pack was built. H10, H14, H15, H17, H19 and
  H22 are covered or do not apply: no calibration corpus; every grain the offer log allows (static or cascade, with
  age, store or December terms, ordinary weeks alone) keeps the call (R3b, C8); the referees are computed on the raw
  register; the batch voice check shows no repeated phrase; one archive, this build's; no real download.
- **Personas in the pack.** Beth Hill, Meredith Stevens, Kristina Patel and Belinda Friedman (drawn with `guard.py
  names`), all on the card.

## Build record

- Generator: `world.py` (the stores, casuals and permanent staff, their availability, the rosters, the call-ins their
  absences and open lines raise, the module's offer cascade and each casual's answer), `records.py` (the records and
  their writers), `docs.py` (the standard, the module notes, the EA summary, the transmittal), `xlsx.py` (the Christmas
  roster workbook, the trading plan), `postprocess.py` (container normalisation), `common.py`, `calc.py` (the bundle
  reader, the offer features, the logit, the forward cascade, the register routes), `asks.py` (both asks and their
  stops), `deliver.py` (the brief, the workbook, `figures.json`), `submission.py`, `metadata.py`, `checks.py`
  (76 assertions: the three-rules block, the ladder and routes, SF1 to SF11, the closure axes, both asks with
  their filed readings, devices, stops and the cracker, the separation line, the realism sweep, the input gates and the
  distractors),
  `verify.py` (its own path), `build.py` (two byte-identical builds, the zip).
- Pack: 15 files in five formats (csv, json, pdf, txt, xlsx); the largest the offer history at 139,549 rows;
  distractors the Christmas trading plan and the school terms and public holidays calendar, named in `metadata.json`.

## World seed

Fixed before the first production run (17 October 2026), never searched: the world seed is 155, the task number; every
stream is drawn from `numpy.random.SeedSequence([155, k])` with k a fixed stream number per component (staff, each
roster period, call-ins, the history cascade, each Christmas run), so a change to one component re-rolls no other.
The Christmas forecast's ground truth is the mean over 32 runs, run r on stream 1000 + r. Robustness is read on world
seeds 156 to 160, which never ship; a design that holds only on 155 is redesigned, not shipped.

Read again on the final world (the travel rule, the duplicate absence reports and the give-back day rule in place) on
seeds 156 and 160, with the shipped generator and checks: the world's own Christmas puts Camberwell first (1.48 and
1.54 over the next store, 8 runs); every trip-cost construction and the golden file Camberwell (the golden 1.18 ahead
on seed 156, where Werribee lists 3,377 open hours, more than its staying-on casuals absorb, and 1.48 ahead on seed
160); and every no-trip-cost route files Werribee, at least 1.21 ahead of Camberwell (the static rostered-that-day
model on seed 160; 1.36 on seed 156). On seed 156 Werribee's uplift is more than 25 crew can work under
the EA's limits, so the capacity closure (SF10) is a property of the shipped world, asserted there.

## Tried and rejected

- Prototype v1 to v5 (uplift rostered with the base positions): the open hours were whatever the roster builder could
  not fill, too small and uncontrolled to carry a call; the uplift is now listed open by design and the base rostered.
- Prototype v6 to v9 (declines retried every round): every Christmas shift filled at every store and nothing separated
  them; a decline is now final, only a non-response is offered again, and December lowers separate-trip take-up.
- Prototype v10 to v16: Camberwell won on every route, the open-hours sum included; Werribee was reshaped (a university
  intake rostered on the 8-to-2 and 2-to-6 shifts, fewer casuals free on their days off, its separate-trip take-up lower).
- Prototype v17 to v22: a model with one "rostered that day" term landed Camberwell, because extension offers were
  common in ordinary weeks; ordinary-week extensions were made rare, a second separate shift on a rostered day was
  priced below a day off, and the 2025 Christmas uplift no longer sat against rostered shifts.
- Prototype v23 and v24 (the extension effect not additive in the logit): the truth flipped with the casual's own
  propensity, and a fixed-effects model forked from a pooled one; returned to an additive term.
- Prototype v25: a 52-casual intake left Werribee's added positions open, so its open hours were not its uplift;
  the intake is 56 and the added positions are all against the uplift.
- Production engine, run 1 (the prototype's store settings): Ballarat could not staff its own base lines, 1,304 of its
  2,078 open Christmas hours were base lines the roster builder left empty, and the world put Ballarat first; Ballarat
  took a February intake (nine school students, three flexible casuals) and its open hours are its listed uplift again.
- Production runs 2 to 5 (a larger Camberwell uplift, then a 70-casual Werribee intake): the static model with one
  "rostered that day" term and the pooled cell-rate route filed Camberwell (x1.06 to x1.12) or led it by only 1.02;
  Camberwell's uplift was cut back and Werribee's intake is 64 casuals on five working days at 21 to 27 hours a week.
- Production run 6 (Werribee's uplift raised to 3,760 open hours): the routes held, but 25 crew at 38 hours for four
  weeks is 3,800 hours, so capacity nearly bound at the default path's store and opened a capacity fork; cut back.
- The production truth first scaled the staying-on effect with each casual's own propensity, and the trip-cost model run
  through the cascade led the runner-up by only 1.10; the truth is an additive logit, its staying-on term raised from
  4.2 to 4.8 when the cascade's lead sat at 1.22 to 1.31 on seeds 157 and 158.
- Robustness seeds: Altona's and Box Hill's evening uplift, then Williamstown's early uplift, came within 1.16 of
  Camberwell under the trip-cost model run through the cascade; their uplift was trimmed, and school students keep
  their term-time availability until Boxing Day (the term ends 18 December; they change their profile after Christmas).
- Build 4: the availability profile in force at the extract disagreed with the engine on 16 casual-days at Christmas,
  because the university semester ended on a Friday (6 November) and the Friday windows changed only on 13 November,
  after the extract closed; the semester ends on Thursday 5 November, so every weekday's post-semester windows are in
  the extract (C22b).
- The brief's first share of open shifts reachable by staying on counted any casual whose shift abutted the open one
  and put Camberwell at 63 per cent, though most of them could not take it (over their hours, unavailable, or at
  another store); the share counts only casuals the module would offer the shift to, 2 per cent at Camberwell.
- Ask figures to the nearest hour: paid hours come in half hours, so many figures sat exactly on a rounding edge; the
  asks are to one decimal place, where every figure is exact.
- The cracker sheet first took the laziest ask path (every register row a shift, 2 of 40 figures kept); the cracker
  chains reposts into their shifts, which keeps six stores' uncovered hours (a dropped fill moves put-out and covered
  hours together and leaves uncovered hours alone), 8 of 40 figures, and the pair ceiling is struck on that.
- The offer log's response column was first named `answer`, a generator's word to the leak sweep; it is the module's
  `response`, with `responded_at`.
- Build 5: with the profiles corrected, the static model with one "rostered that day" term led Camberwell by only 1.10
  (R3a needs 1.15). Three more open shifts a weekday at Werribee (270 more open hours) widened it to 1.21 but left 25 crew
  unable to work every Werribee open shift under the EA's limits and made Werribee the golden's runner-up; Camberwell's
  weekday uplift lost one 10-to-4 shift a day instead (1,092.5 open hours), and every no-trip-cost route now leads
  Camberwell by 1.25 or more.
- Judge round 1 (`determinism_check_report_round1.md`: the call DETERMINISTIC, FIX_NOW on both tables): Table 1
  reproduced only under readings no shipped text stated (a shift's daily re-raised call-ins, UTC, a fill voided when
  its casual later reported absent), and Table 2 needed the payroll cost centre on the shift date. Each is filed once
  as how KWS and payroll keep the record (the module notes' Call-ins and Responses, the transmittal's payroll note),
  the standard and the notes now say alike that open lines go to call-in except at the crew's store, and every other
  reading is asserted off the golden (A S1, S1b, S3, S3c, S4, S6; B S1, S3c). The filing spent Ask A's give-back device
  and Ask B's home-store device; an absence reported twice (A3) is the silent device added beside A1's over-cleaning
  half.
- The judge's covered hours ran 4.0 below the golden at Camberwell, Ringwood and Williamstown: the engine let a casual
  who gave back a call-in take another call-in later the same day, which a reader voiding every fill on a day its
  casual reported an absence drops. KWS now offers such a casual nothing more that day (the notes say so), and voiding
  by the day agrees with voiding by the shift's own re-raise on all 40 figures (asserted).
- Realism, the rule-3 audit's two cells: offers carrying on from the casual's shift at another store (488, none taken)
  and a second, separate shift on a rostered day (0.3 per cent of 16,070). A cross-store carry-on term was tried first,
  taken 3 to 6 per cent of the time: sister-store casuals finishing a morning shift then carry on into Camberwell's
  10-to-4 shifts, the world's own lead fell from 1.51 to 1.38 (3 per cent) and 1.30 (6 per cent), and on robustness
  seed 156 the golden filed Werribee (x1.02 at 3 per cent, x1.05 at 6). A casual cannot be at one store as their shift there ends and at another as the next one
  starts, so KWS now skips a casual with a shift at another store ending less than an hour before the call-in starts or
  starting less than an hour after it ends (filed in the notes' skip rule, applied by the golden's forward cascade,
  RZ11: no offer of 139,549 breaks it): the cell is gone, not empty. The second-shift cell stays at 0.26 per cent (42 of
  16,224): 91 per cent of those offers start one to two hours after the casual's own shift at the same store, and every
  higher take-up lends the pooled rostered-that-day model the carry-on effect (scratch trials on the shipped seed:
  0.4 to 0.6 per cent, Werribee x1.15 to x1.24 over Camberwell; 0.8 per cent, x1.07 to x1.14; 1.7 to 2.0 per cent,
  Camberwell first by x1.09 to x1.17; 4.35 per cent, the audit's "a little under the day-off rate", Camberwell first by
  x1.78). The route's margin is kept at the cost of that cell's realism, which RZ10 asserts only as taken and under a
  fifth of the day-off rate. The travel rule re-draws the history, and the route sits at 1.21 on the shipped world
  (1.21 to 1.27 across draws at this take-up).
- The cracker sheet's path moved from chaining re-raises (build 8) to folding a shift's call-ins on its identity:
  with the filed "a call-in for each day" the fold is the literal execution, and it falls into A1. The chaining path,
  which the round-1 judge took, keeps Ask B whole once its conventions are filed (26 of 40 figures); both are written
  in `## Ask sheet` and the pair ceiling is struck on the fold.
