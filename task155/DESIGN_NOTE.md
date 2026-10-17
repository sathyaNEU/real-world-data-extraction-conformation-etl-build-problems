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
| Layer 1 | timestamps in UTC in the workforce system against store-time rosters across the daylight-saving changes of October 2025, April 2026 and October 2026; two staff keys (the workforce system's person code and the payroll employee number, a rehire getting a new number); the roster export's layout changed when rostering moved into the workforce system in February 2026; store names, location ids and cost centres; shifts ending at midnight written 24:00; the effective-dated home store; the unpaid 30-minute meal break on shifts over five hours; re-offers written as new call-ins, given-back fills raised again, an absence reported twice, the 2025 roster import raising some open lines twice, and store moves payroll recorded as re-engagements keyed before they began (the asks' records); the full inventory is in `## Layer 1 inventory` |
| Furniture | forum `operations_desk` (the workforce planning desk places the crew), forcing event `season_or_peak` (the four trading weeks to Christmas Eve), organisation family `retailer_or_ecommerce`, role family `capacity_planner` (the workforce planning manager), context artifact `capacity_report`, calibration `none`, opening `question-first`, question form `which` |
| Spine | `callin_offers_20250829_20261112.csv`, the workforce system's offer history report, shifts 29 August 2025 to 12 November 2026 (one row per offer of one call-in shift to one casual, with the response), 156,070 rows; constructed |
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
while Camberwell's Christmas online-picking uplift sits 9 to 3 on weekdays: plenty of casuals are free then, most of
them from Box Hill and Ringwood, but no casual's shift abuts it, so each would need a separate trip in.

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
   27 November 2025 and 25 December 2025 to 12 November 2026, last Christmas's weeks set aside): Werribee 0.34, the
   other stores 0.43 to 0.60.
4. Multiply each store's open hours by the share left unfilled and place the crew at the largest.

Ends on: Werribee, 3,250 crew hours (about 2,140 of them otherwise unworked, Box Hill next at about 1,030, Camberwell
seventh at about 450).

Golden: Camberwell, 1,090 crew hours (about 630 of them otherwise unworked, Sunshine next at about 440, Werribee about
350): each open shift's chance of going unfilled is the chance every casual the module would offer it to says no, each
casual's answer priced on whether the shift carries on from their own rostered or booked shift at that store, on the
December season and on the other terms the offer log shows, run through the module's offer order and limits. The
shipped write-up states the ranking and the margin in words only (the round-2 judge's own simulation put Camberwell at
about 580 to 640 and the runner-up lower than the golden does).

## Stump sentence

Taking each store's call-in fill rate from the register (ordinary weeks or last Christmas, by posting or by shift), or
fitting each offer's acceptance on shift time, length, notice, sister-store travel, weekly hours, the December season
and whether the casual is rostered that day, and applying it to the open shifts in the published Christmas rosters
sends the crew to Werribee, its 3,250 open hours the crew hours; the step that lands it there is pricing every offer as
a separate trip to work, when a casual whose own rostered shift at that store ends as the open shift starts, or starts
as it ends, takes it many times as often, and Werribee's Christmas uplift is listed against its own casuals' rostered
shifts, so Camberwell, whose weekday 9-to-3 uplift no casual's shift abuts, is the store, with 1,090 crew hours.

## Three rules

- Task type: discrete-choice-limited-dependent-variable-modeling (Economics & Econometrics), which serves Forecasting: each open Christmas shift's chance of going unfilled is the product, over the casuals the call-in module would offer it to, of each casual's chance of saying no, a binary choice estimated on the offer log and aggregated over the published roster.
- Domain test: the deciding quantity is each store's expected unfilled open hours, built from a labour-supply choice at the extensive margin: taking an extra shift carries a fixed cost of getting to work that an offer carrying straight on from the casual's own rostered shift at the same store does not, so the field's estimator is a choice model whose specification carries that participation cost, fitted on every offer and its answer and applied to the open shifts' position against each casual's rostered shifts.
- Swap: "which of eight power stations gets the one maintenance crew for the four weeks to Christmas, on the megawatt-hours its standby units would leave unserved" keeps the arithmetic of open hours times a shortfall rate, but no standby unit chooses whether to make a trip, so there is no fixed cost a schedule can remove and the construction that decides the call has nothing to act on.
- Layer 1: the workforce system (KWS) writes offer and call-in times in UTC while rosters are in store time, across the daylight-saving changes of October 2025, April 2026 and October 2026; offers carry the KWS person code and rosters the payroll number, and payroll issues a new number on rehire; the roster export changed layout when rostering moved into KWS on 27 February 2026 (the legacy export dated dd/mm/yyyy with store names and span hours, the KWS export ISO dates, location numbers and paid hours); the Christmas roster writes shifts ending at midnight as 24:00; payroll keeps the home store effective-dated while KWS holds only the current one; the unpaid 30-minute meal break on shifts over five hours; a call-in that runs out of casuals closes UNFILLED and the shift is raised again as a new call-in at 07:00 the next day; a casual who gives back an accepted call-in reports an absence and the shift is raised again naming them; an absence reported both in the app and by phone raises two call-ins for one line, and booking the shift closes the second FILLED with the casual booked; the legacy tool's import raised some of the 2025 Christmas open lines twice, booking either copy closing the other FILLED with the casual booked; KWS offers no shift within an hour of the casual's shift at another store; payroll recorded store moves before April 2026 as a resignation and a re-engagement, the new cost centre dated from the day it was keyed. Each comes from how the system records its own work, and none carries the call.
- Layer 2: field_method, the labour-supply choice model: the methodological choice that flips the call is specifying the participation cost, separating offers that carry on from the casual's own rostered shift at that store from offers that need a separate trip, estimated on the history where such offers are about one in seventy (2,241 of 156,070) and applied to a Christmas roster where every one of Werribee's open shifts could be taken that way.
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
| a given-back fill keeps its FILLED outcome and the shift is raised again as an ABS call-in naming the casual; a shift is covered by the casual who works it (both filed in the module notes) | KWS register | call-in register | the first fill kept as cover, or its re-raise counted as another shift; give-backs looked for only on open-line fills | Ask A filed readings S3, S3c and S3d asserted off; Ask B S3c; R2.5 for the call |
| an absence reported both in the app and by phone, two ABS call-ins for one vacated line (12 per cent of absences; filed in the module notes); booking the shift closes the second FILLED with the casual booked | KWS register | call-in register | each call-in raised other than at 07:00 counted as a shift, each FILLED call-in as cover | Ask A detection device A3 (S3b); Ask B S3 (every FILLED call-in as written); the golden's vacated lines are a set and a casual is booked on a shift once (SEP1, R2.9) |
| the 2025 Christmas rosters came into KWS through the legacy tool's import, which raised some open lines twice (12 to 32 per cent of the lines at the seven stores whose uplift was put out); booking either copy closed the other FILLED with the casual booked | the legacy import into KWS | call-in register against the 2025 legacy roster export | each posting at publication counted as a line, each FILLED close as cover | Ask A device A4 (the 07:00 chain, 21 of 24); the golden counts open lines from the 2025 roster export (the A4 referee check); R2.9 for the call |
| store moves before payroll's April 2026 transfer screen recorded as a resignation and a re-engagement under a new number, the re-engagement form dating the new cost centre from the day it was keyed (the November roster review's moves on 20 November 2025, the Ballarat leavers' on 15 December), so the new number's cost-centre row starts before its engagement | payroll | payroll register; KWS people (the new number) | the home store read from the number KWS holds, on the cost-centre rows' own dates | Ask B device B2 (S8); R2.8 (the call holds) |
| no offer to a casual with a shift at another store within an hour (filed in the module notes' skip rule: a shift at another store counts from an hour before its start to an hour after its finish) | KWS | offer log against both roster exports and the register's fills | none: the rule holds on every offer | RZ11 (0 of 156,070 offers); the golden's forward cascade applies it |

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
| R0 | the register's fill share over the ordinary weeks, by posting or by shift, times each store's Christmas open hours | Werribee | 1.61 to 2.07 | 7th |
| R1 | the same share over last Christmas's weeks | Werribee | 1.25 to 2.16 | 6th or 8th |
| P | the pool: the casuals the module would offer each open shift (the store's own and its cluster's opted-in casuals, the module's checks passed), read thinnest-first per open shift-hour, hours-weighted or as each store's median per shift | Williamstown | Camberwell's pool 1.59 to 2.75 times the thinnest | 3rd to 5th thinnest |
| R2 | an offer-level logit on the log's own columns (shift length, finish, start, Sunday, notice, a repeat offer, sister store, weekly hours, the Christmas weeks, age band, home store), with or without a rostered-that-day term, static or run through the module's cascade; or every casual in a shift's pool saying yes at one rate (the log's take-up, or December's on a day off) | Werribee | 1.75 to 2.94 over Camberwell | 2nd to 5th |
| R3 (decisive) | the same model with the trip-cost term: an offer that starts as the casual's own rostered or booked shift at that store ends, or ends as it starts, priced apart from a second, separate shift that day | Camberwell | 1.44 to 1.85 | 1st |

- Position and dominance: every construction without the trip-cost term files another store (17 of 17 in
  `routes.txt`: the open-hours sum, four register routes, seven offer models and two one-rate routes file Werribee, the
  three pool measures Williamstown); every construction with it files Camberwell (6 of 6, static or run through the
  cascade, with or without age, store or December terms), as do the golden (24 runs, 1.45 over Sunshine) and the
  world's own Christmas (32 runs, 1.38 over Sunshine).
- Hardening before the cut (`stumping` Part 8, the winner's default-path rank worse): Box Hill and Altona list
  Christmas uplift against their own casuals' afternoon shifts as Werribee does (96 and 79 per cent of their open
  shifts reachable by staying on), so Camberwell is sixth on open hours, sixth to eighth on every register route and
  second to fifth on every offer model, at least 1.59 behind the leader on every easy route; asserted (R3a, L1 to L3).
- The pool (round 3): Camberwell's Christmas online picking runs 9 to 3 on weekdays, so no 4 pm shift abuts it, and the
  East stores' university students and flex casuals mostly opt in to sister-store call-ins, the three stores sitting
  close together. The module would offer each 9-to-3 shift to a median of 30 casuals, 60 of the 67 from Box Hill or
  Ringwood and 42 of those 18 to 24 (RZ8), against a median of 12 across Williamstown's open shifts. Counted, Camberwell's pool is
  among the deeper ones; priced, every casual in it needs a separate trip, most to another store, and few take one.
  Every pool measure files Williamstown, whose early shifts its own casuals reach by starting early, and puts
  Camberwell third to fifth thinnest.
- The weakest wrong offer model is the static model with one rostered-that-day term (Werribee 986 against Camberwell
  562, 1.75; 1.20 a round ago, before Camberwell's pool reached the sister stores). The term pools the 2,241 offers
  that carry on from the casual's own shift (32 per cent taken) with the 21,315 offers of a second, separate shift on
  a rostered day (0.23 per cent taken), so it reads a casual already rostered that day as a little less willing than
  one on a day off (3.2 against 4.4 per cent).
- Worth on the graded figures: the store and the crew hours both change when the decisive rung is undone (Werribee
  3,250 against Camberwell 1,090); every critical component (the 32 against 4 per cent split, the share of each store's
  open shifts its casuals could take by staying on, Camberwell's 1,090 open hours) is upstream of the call.
- Strength against the opponent (lesson 2): P(one strong solver builds the trip-cost term and applies it to the
  published roster) is put at 0.15 (about half take a register route, a third an offer model on the log's columns or
  a pool count, a sixth join the rosters and test adjacency); P(both top responses) about 0.03 to 0.04 with
  correlation. Before round 3 a pool count reached Camberwell without the term (its 10-to-4 uplift had a median of 5
  casuals a shift, the thinnest), which would have put P(one) nearer 0.25; every pool and one-rate route now files
  another store, and the free gates assert every natural route's verdict.
- Stability: the deciding split rests on 2,241 offers and 713 acceptances; a one-sigma move in the trip-cost
  coefficient either way keeps Camberwell first (1.80 and 1.84, L4).

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
themselves (2,241 offers, 32 per cent taken against 4 per cent of the rest), a cut the default path never makes.

## Ask sheet

**Main call's declared row population:** the offer log's offers (shift fields, person code, offer and response times,
response), the roster lines' start and end times and payroll numbers on the days of offers, the KWS people extract's
person code, payroll number, home store, opt-in and service date, the payroll register's previous numbers and
cost-centre history, the availability profiles, and every line of the published Christmas roster. Device rows in it:
the re-engagement rows of the 23 store moves dated before April 2026 (Ask B's device B2 sits in the payroll register
the call also reads); read on the rows' own dates they mis-home those casuals' offers from the keying date to the
move, and the call holds (R2.8, x1.81). The import's second raise of a 2025 open line (device A4) sits in the register,
which the call reads only for fills and vacated lines; its FILLED close kept in the casual's day, the call holds (R2.9,
x1.83). No other device or hazard row touches it. The golden reads the call-in register only for fills and vacated
lines (SEP1), the call holds with call-in fills left out of each casual's day (R2.5) and with home stores read current
(R2.2), and the asks read neither the Christmas roster nor the offer log (SEP2).

**What the filing settles (judge rounds 1 and 2).** The module notes and the transmittal say, as how KWS and payroll keep
their records: an open line is put out when the roster is published (OPN) and a vacated line when its absence or leave
is raised (ABS, LVE), except the open lines of the store where the crew is placed (the standard says the same); a
call-in whose list runs out closes UNFILLED and the shift is raised again as a new call-in at 07:00 the next day, so a
shift offered over several days has a call-in for each day; a casual who gives back a call-in reports an absence, the
shift is raised again as an ABS call-in naming them, their own call-in keeps its FILLED outcome and KWS offers them
nothing more that day; KWS keeps times in UTC; a casual's home store on a date is the store whose cost centre applied
to them that day (round 1). A casual can report an absence in the app or by phone, and an absence reported both ways
raises one ABS call-in for each report; a shift is covered by the casual who works it, and a casual who gives a shift
back has not covered it (round 2, the notes); the prompt's Table 2 sentence counts the hours of each store's call-in
shifts. Each is a fact or a definition, not a procedure: the text fixes every figure, and finding the give-backs, the
duplicate reports and the import's second raises in the register is the reader's work. Every other reading is asserted
off the golden. Under the filing sit three silent devices (A1, A4, B2) and one detection device (A3), measured below on
both cracker paths.

**Ask A. Last Christmas's call-ins by store** (24 figures, paid hours to one decimal place): for each store, the hours of
the shifts it put out to call-in for the four trading weeks to Christmas Eve 2025 (Friday 28 November to Wednesday
24 December), and how many of those hours call-ins covered and how many they left uncovered.
- H18 home: how call-in cover held up at each store last Christmas, the brief's context table beside the call; a
  measure every store carries that the call does not turn on.
- Primary A1 (D6, a ledger at another grain than its name, the over-cleaning half; silent): each shift has a call-in
  for each day it was offered, and the stores also list identical open shifts on one day (Box Hill listed 14 vacant
  4-to-8 pm lines each weekday last Christmas), each its own shift; folding a shift's call-ins on store, date and times
  (with reason and absent payroll number) merges them. Fair: the 2025 legacy roster export lists every vacant line, and
  a re-raise comes at 07:00.
- Primary A4 (D1, a resubmission that opens no second case, on the open lines; silent): the 2025 Christmas rosters
  reached KWS through the legacy tool's import, which raised some open lines twice (12 to 32 per cent of each store's
  open lines at the seven stores whose uplift was put out; Werribee's uplift went to the 2025 crew), each copy its own OPN call-in at
  publication, booking either closing the other FILLED with the casual booked. Telling re-raises by their 07:00 raise
  counts every posting at publication as a line and both closes as cover: the 07:00 chain misses 21 of 24 with the
  duplicate reports merged as filed, 7 of the 8 covered figures among them. Fair: a shift put out as OPN is a line left
  open on a published roster (the notes), the 2025 legacy export lists the lines (its vacant lines, the shifts put out;
  the register raised more postings than lines at all seven of those stores), and a copy closed FILLED with the casual booked on
  its twin at the same minute is one booking.
- Detection A3 (D1, the same on a vacated line): an absence reported both in the app and by phone raises two ABS
  call-ins for the one vacated line (12 per cent of absences), and booking the shift closes the second FILLED with the
  casual booked. The notes file the fact; finding the pairs (two call-ins for one shift naming the same absent number)
  is the reader's, and a reader who misses them, with the import's second raises, counts each as a shift and each
  second close as more cover (S3b, 23 of 24).
- Hazards: HA1 UTC against store dates (shifts starting before 11:00 on Friday 28 November 2025 sit on 27 November in
  UTC); HA2 the meal break (span against paid hours); HA3 Werribee's Christmas uplift went to the 2025 crew and was
  never put out.
- Readings asserted off (each a complete pipeline in `asks.py`, asserted in `checks.py`): S1 every register row a
  shift, 23 of 24 figures off; S1b every row but those closed the minute they were raised, 23; S3 a give-back's
  re-raise counted as another shift with the first fill kept (the round-2 judge's Fork S1, Altona 1,636.5 and 860.5 on
  that draw), 14; S3c a give-back counted once with its first fill kept as the cover, 14; S3d give-backs looked for only
  on fills of open-line call-ins (the round-2 judge's Sunshine 5.5 hours: a fill of an absence's call-in given back on
  9 December, 4 to 10 pm, three such in the window), 4; S4 UTC dates, 19; S5 span hours, 24; S6 open lines left out,
  24; S7 fills voided by any absence their casual reported that day: the golden, 0 of 24 (KWS offers such a casual
  nothing more that day, asserted). Devices: S2 the fold (A1), 24; S3b (A3 and A4), 23; the 07:00 chain (A4), 21. Every
  golden figure is exact at one decimal (paid hours come in half hours).
- Span: the call-in register, the legacy roster export, the KWS people extract, the payroll register, the EA summary,
  the module notes (6 files); store, shift start and end, reason, absent payroll number, raised, closed, outcome,
  filled by.

**Ask B. Cover across stores last Christmas** (16 figures, paid hours to one decimal place): for each store, the hours of
its call-in shifts in those weeks covered by casuals from other stores, and the hours its own casuals covered at other
stores.
- H18 home: how far stores leant on each other last Christmas, beside the crew's case; a measure every store carries.
- Filed (round 1): the home store is the payroll cost centre on the shift date. Read current, 14 of the 16 figures
  move. Filed (round 2): a shift is covered by the casual who works it. Every FILLED call-in counted as written (the
  round-2 judge's Fork S2, Altona 33.5 and 5.5 on that draw), 11 of 16 move; a given-back sister-store fill credited to
  its first filler, 6.
- Primary B2 (D2, an attribute at the wrong vintage; D7, the true key elsewhere; silent): before its April 2026 transfer
  screen payroll recorded a casual's move between stores as a resignation and a re-engagement under a new employee
  number, the re-engagement form dating the new cost centre from the day it was keyed: the November roster review keyed
  its new-year moves on 20 November 2025, and the Ballarat school leavers' moves to Melbourne were keyed on
  15 December, the Monday after the VCE results. KWS keeps the person code and holds the new number. Read from that
  number on the cost-centre rows' own dates, 23 movers' December shifts take the store they moved to weeks later, and
  12 of the 16 figures move; no join fails and no row fans out. Fair: the same row carries an engagement start weeks
  after the cost centre's effective date, the transmittal says a row is a period a cost centre applied to an
  engagement, and the earlier number (previous_employee_no) runs until the day before the move; the offer log's order
  (a store's own casuals asked before sister-store ones) agrees with the golden's homes on every posting (SF11).
- A4 in Table 2: on the 07:00 chain the import's second raise of a line booked by a sister-store casual counts that
  cover twice.
- Hazards: HA1, HA2.
- Readings asserted off: S1 current home store, 14 of 16; S3 every register row a shift, 11; S3c, 6; S8 the
  re-engagements read on the rows' own dates (B2), 12; the fold (A1 with B2), 13; the 07:00 chain (A4 with B2), 14 (11
  with the golden's home read). The first payroll row covering the date, in the register's own order (the round-2
  judge's read), reaches the old engagement's row first and keeps all 16 on the golden's shifts.
- Span: the call-in register, the KWS people extract, the payroll register, the store list, the transmittal (5 files).

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC | KWS stores times in UTC | A, B | the Friday 28 November morning shifts at every store |
| HA2 meal break | the EA's unpaid break | A, B | half an hour per shift over five hours, every figure |
| HA3 the 2025 crew | Werribee's Christmas uplift went to the crew | A | none (Werribee's put-out hours are its absences and 14 rostered lines it left open) |

**Referee.** Ask A: the 2025 legacy roster export's vacant lines are the open shifts put out (the register raised more
postings at publication than there are lines at all seven stores whose uplift was put out, from Williamstown's 325
for 290 to Ringwood's 406 for 308, and as many as lines at Werribee, 14 for 14); Ask B: the offer order shows who the module treated as a store's
own casual on the day. Neither hands over an ask figure.

**Cracker sheet** (both paths run on the cut pack by `generator/cracker.py`, every figure scored at its stated rounding;
the round-2 judge's own route run beside them for the record)

| Ask row | Figures | Cracker's path | Cracker's figures kept | Verdict |
|---|---|---|---|---|
| Ask A, the shift-identity fold | 24 | each shift's call-ins folded on store, date, times, reason and absent payroll number, give-backs voided, store dates, paid hours | 0 | miss |
| Ask B, the shift-identity fold | 16 | the same shifts, each filler's home store the payroll cost centre on the shift date, read from the number KWS holds | 3 (Ballarat's two figures and Werribee's imports, all zero) | miss |
| Ask A, the 07:00 re-raise chain | 24 | each re-raise told by its 07:00 raise and chained to its shift, an absence's two reports one shift as filed, give-backs voided, store dates, paid hours | 3 (Werribee's three: its uplift went to the 2025 crew, and the import raised none of its 14 open lines twice) | miss |
| Ask B, the 07:00 re-raise chain | 16 | the same shifts and home-store read | 2 (Ballarat's exports and Werribee's imports, both zero) | miss |
| Ask A, the round-2 judge's route (for the record) | 24 | open lines counted from the day's postings, an absence's reports merged, give-backs looked for on open-line fills | 3 (Werribee's three) | miss |
| Ask B, the round-2 judge's route (for the record) | 16 | the home store from the first payroll row covering the date | 5 (Ballarat's two, Werribee's imports, Altona's exports, Williamstown's imports) | miss |

Blind responses (`cracker.py`): one register fill rate on each store's register row hours recovers 0 of Table 1's 24
cells; every cell nil 0 of 24 and 3 of 16 (the three true zeros); the best constant 1 of 24 and 3 of 16.

Measured by: `generator/cracker.py` (run by `checks.py` on every build).

Mirror leakage: 20.0 per cent of ask weight on the round-2 judge's route (8 of 40 figures), 12.5 per cent on the 07:00
chain (5 of 40), 7.5 per cent on the fold (3 of 40); the mirror is R2, Werribee, and runs the cracker's ask paths.

Pair ceiling: 39.5 on the round-2 judge's route, run for the record (C = 38 + 7 + 55 x 8/40 = 56.0; S = 5 + 7 + 55 x
8/40 = 23.0); on the two cracker paths 35.4 on the 07:00 chain (C = 51.9, S = 18.9) and 32.6 on the fold (C = 49.1, S
= 16.1), measured on the cut pack.

## Surface screen

`guard.py surface task155` promotes six pairs for adjudication; none carries a hard tell (no shared file name, column
set, same-seed table, invented name or masked prompt wording: Track A rests on the shared folder layout and format mix
alone). `guard.py heart` warns on one persona's first name only (Kristina, which task240 drew at 18:42 on 17 October,
after this build's draw at 09:07); its nearest text is 0.05 (the stumps of task254 and task149) and its nearest driver
0.09 (task469, the share of future tasks that will outrun a shorter allowance, nothing to do with a take-up). The pack
names Beth Hill, Meredith Stevens, Kristina Patel and Belinda Friedman, the four drawn personas, and no one else. For
the author, who alone runs the adjudicated `/clone-check`:
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
- task151 (surface 0.101 a round ago, promoted then on surface similarity alone, no longer promoted): the folder
  layout and format mix only; task151 accrues a stepped bonus on a unit's season total from its position's rate per
  appearance, and shares no driver, file, column set or sentence with this pack.

## Leak sweep

`leak.py task155 --asof 2026-11-13`: REVIEW, no LEAK (`leak_check_report.md`). Each REVIEW line, read:
- Sweep 3 (the call's words in the pack): the placement standard and the module notes carry "relief crew", "work",
  "hours" and the store names because the standard is the placement rule for the eight stores and the notes list the
  call-in clusters; Camberwell appears in each only inside a list of stores, and neither document ranks a store or
  gives a figure for one.
- Sweep 4 (the design note's vocabulary): the transmittal, the EA summary, the module notes and the standard are the
  chain's own documents about rosters, call-ins and pay and share their workaday words (roster, casual, offers,
  payroll); none names staying on, a trip to work, an extension or an offer's position against the casual's own shift.
  The module notes' sentences on a casual's own shifts are the skip rule (an overlapping shift, a shift at another
  store counting from an hour before its start to an hour after its finish) and the give-back rule; they say who is
  offered a shift, never how a casual answers, and no sentence on acceptance mentions a casual's own shifts. The
  round-2 sentences (an absence reported both ways raises one ABS call-in for each report; a shift is covered by the
  casual who works it, a casual who gives a shift back has not covered it) are records and a definition for the
  asks, and say nothing of who takes a shift. The trading plan's Camberwell note gives the Christmas picking hours
  (9:00 to 15:00), as a trading plan would.
- Sweep 9 (dates after the as-of): the Christmas roster lists the shifts of 27 November to 24 December 2026 as
  published on 12 November, the forward window the call is about; the school-terms calendar is the state calendar with
  the term's end and the Christmas public holidays (a distractor). No extract column runs past 12 November (RZ3).
- Sweep 10: no writer signature in any container (INFO); the container audit is clean on the pack and the goldens.

## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is still analytical: the standard files the estimand
  (the open shifts of each store's published Christmas roster, the paid hours of them call-ins would leave unfilled
  with the crew at no store, the four trading weeks, the eight stores) and no shipped sentence says how a casual
  answers an offer; executed with any separate-trip estimate, the notes and the standard file Werribee, and counted
  as pools they file Williamstown (R3a, 17 routes); only the trip-cost term, built by joining each offer to the
  casual's own roster that day through the payroll key, files Camberwell (R3b, 6 of 6). Layer 1 (UTC, two keys and
  rehires, the layout change, 24:00 ends, the effective-dated home store, the meal break, re-raises, give-backs,
  absences reported twice, the 2025 import's second raises and the re-engagement records) is neutral for the call:
  each mishandled reading leaves Camberwell first (R2.1 to R2.9), and the register's records move only the asks.
- **Free gates on the final rebuild.** `checks.py` 86 assertions, 0 failed; `verify.py` 0 failed on its own path;
  two builds byte-identical (15 files) and `target.zip` cut from the final build; `figures_check.py` 62 figures,
  0 absent; `cracker.py` both paths at or under 40 (35.4 on the 07:00 chain, 32.6 on the fold; 39.5 on the round-2
  judge's route, for the record); `precut.py` exit 0 (50 checks); `voice-check.py` PASS (895 characters); the
  container audit clean on the pack and the goldens; `guard.py heart` WARN on a persona's first name only, which task240
  drew after this build (nearest text 0.05); `guard.py surface` six promotions, no hard tell (## Surface screen); `leak.py` REVIEW, no LEAK (## Leak sweep).
- **Residual, accepted and recorded.**
  - A pool count of a store's own casuals only, against the module's offer order that reaches the cluster, still
    files Camberwell (own casuals only, a median of 4 a shift across its open shifts, Williamstown's 6); every count
    the module's order gives (own store and cluster) files Williamstown.
  - A reader who also checks that no casual is booked twice on one shift catches device A4's covered column: the
    07:00 chain then keeps 14 of 40 (pair 47.8, under the 50 bar, over the 40 build target).
  - The round-2 judge's own route, run for the record, keeps 8 of 40 (pair 39.5, on the ceiling).
  - The second-shift cell stays at 0.23 per cent (50 of 21,315), well under the day-off rate (`## Tried and
    rejected`); the pooled rostered-that-day route it once protected now leads Camberwell by 1.75.
  - On seed 156 the golden leads by only 1.20 (over Werribee, whose 3,377 open hours there are more than its
    staying-on casuals absorb); the world's own lead there is 1.40.
  - Under the natural read of the re-engagement rows Ballarat shows 28.5 hours of imports though it is in no cluster,
    a tell a careful reader can follow to device B2.
  - Table 2 holds three true zeros (Ballarat's two, Werribee's imports), which an all-nil response recovers (3 of 16).
- **House-fix pass (H1 to H24).** H1 the containers clean. H2 every figure in the write-up and the goldens recomputes
  (`figures_check.py`, `verify.py`), and the note's figures come from `routes.txt` and the checks. H3 the brief read
  figure by figure; its statements about Werribee's February intake and Camberwell's 9-to-3 pool are asserted (RZ9,
  RZ8), and it states no forecast magnitude beyond its chart and table. H4 the zip holds the 15 declared files at its
  root; the brief's chart opened and read. H5 each ask's reading is closed: the asking sentences count shifts and their
  hours, the module notes file how re-raises, give-backs, duplicate reports and cover are recorded and the transmittal
  the home store on the shift date (rounds 1 and 2), each other reading asserted off. H6 the memo's rules run over the
  record (RZ8, RZ9, the 32 against 4 per cent split). H7 the zip cut from the final rebuild, two builds byte-identical.
  H8 the brief cites WP-04 section 4 and the EA summary, both shipped. H9 the transmittal lists every shipped file but
  itself (RZ7). H11 one `submission.md` and one `prompt.txt`. H12 and H13 `voice-check.py` PASS. H16 only the Christmas
  roster and the calendar carry dates past the extract, both forward by nature (RZ3 for the extract). H18 both asks are
  context for the placement (last Christmas's cover at each store and between stores), neither a second decision. H20
  the prompt carries the call-in system's own nouns (our eight stores, the relief crew, the placement standard,
  call-ins, casuals). H21 Kellaway's checked against Australian grocers and retailers at the draw. H23 no ask
  presupposes a non-empty subset (the zero cells read 0.0). H24 no file under `target/` says the pack was built. H10,
  H14, H15, H17, H19 and H22 are covered or do not apply: no calibration corpus; every grain the offer log allows
  (static or cascade, with age, store or December terms, ordinary weeks alone) keeps the call (R3b, C8); the referees
  are computed on the raw register; the batch voice check shows no repeated phrase; one archive, this build's; no real
  download.
- **Personas in the pack.** Beth Hill, Meredith Stevens, Kristina Patel and Belinda Friedman (drawn with `guard.py
  names`), all on the card.

## Build record

- Generator: `world.py` (the stores, casuals and permanent staff, their availability, the rosters, the call-ins their
  absences and open lines raise, the module's offer cascade and each casual's answer), `records.py` (the records and
  their writers), `docs.py` (the standard, the module notes, the EA summary, the transmittal), `xlsx.py` (the Christmas
  roster workbook, the trading plan), `postprocess.py` (container normalisation), `common.py`, `calc.py` (the bundle
  reader, the offer features, the logit, the forward cascade, the register and pool routes), `asks.py` (both asks and
  their stops), `deliver.py` (the brief, the workbook, `figures.json`), `submission.py`, `metadata.py`, `checks.py`
  (86 assertions: the three-rules block, the ladder and routes, SF1 to SF11, the closure axes, both asks with
  their filed readings, devices, stops and both measured cracker paths, the separation line, the realism sweep, the
  input gates and the distractors), `cracker.py` (both cracker paths, the round-2 judge's route and the blind
  responses run on the cut pack), `verify.py` (its own path), `build.py` (two byte-identical builds, the zip).
- Pack: 15 files in five formats (csv, json, pdf, txt, xlsx); the largest the offer history at 156,070 rows;
  distractors the Christmas trading plan and the school terms and public holidays calendar, named in `metadata.json`.

## World seed

Fixed before the first production run (17 October 2026), never searched: the world seed is 155, the task number; every
stream is drawn from `numpy.random.SeedSequence([155, k])` with k a fixed stream number per component (staff, each
roster period, call-ins, the history cascade, the 2025 import's second raises, each Christmas run), so a change to one
component re-rolls no other. The Christmas forecast's ground truth is the mean over 32 runs, run r on stream 1000 + r.
Robustness is read on world seeds 156 to 160, which never ship; a design that holds only on 155 is redesigned, not
shipped.

Read again on the round-3 world (the 9-to-3 picking uplift at Camberwell, the East stores' opt-in, the 2025 import's
second raises, the duplicate reports, the give-back day rule, the travel rule and the re-engagement records in place)
on seeds 156 and 160, with the shipped generator and checks: the world's own Christmas puts Camberwell first (1.40 and
1.46 over the next store, 8 runs); every trip-cost construction and the golden file Camberwell (the golden 1.20 ahead
on seed 156, over Werribee, which lists 3,377 open hours there, more than its staying-on casuals absorb, and 1.47 ahead
on seed 160); every no-trip-cost route files another store (Werribee on every offer model, one-rate and register route
but one, Box Hill by 1.03 on seed 160's last-Christmas register route; Ballarat on every pool measure, Camberwell third
to fifth thinnest); and both cracker paths stay at or under 40 (seed 156: the fold 31.2, the 07:00 chain 35.4; seed
160: 29.9 and 36.8; the round-2 judge's route 39.5 and 38.1). On seed 156 Werribee's uplift is more than 25 crew can
work under the EA's limits, so the capacity closure (SF10) is a property of the shipped world, asserted there.

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
- Round 2 (the 07:00 chain kept Table 2 whole, 26 of 40, a pair near 64): Table 2's own device is payroll's
  record of a store move before its April 2026 transfer screen, a resignation and a re-engagement under a new number
  whose cost centre the form dates from the day it was keyed (B2). Coded first with the Ballarat leavers keyed three
  weeks before their February moves, once their university places were known, it moved 8 of 16 figures and the chain
  kept 10 of 40 (pair 42.2); the leavers are keyed in results week instead, so their December shifts read as
  Melbourne casuals' too, 10 of 16 move and the chain keeps 8 (39.5). The cost is a tell: under the natural read
  Ballarat shows 56.5 hours of imports though it is in no cluster.
- Round 2, Table 1's covered column under the 07:00 chain: at 6 per cent duplicate reports, with the second call-in
  closed UNFILLED, the chain kept all eight covered figures. Booking the shift now closes the second call-in FILLED
  with the casual booked (KWS closes the other call-in out for a booked shift), and duplicate reports rose to 12 per
  cent of absences; the chain keeps one covered and one uncovered figure. The higher rate re-drew the history: every
  ask figure moved and the call held (Camberwell, 1,090; the golden 1.69, the world 1.51, the narrowest easy route
  1.20).
- Round 2, the travel rule's first wording ("a shift that ends less than an hour before this one starts or starts less
  than an hour after it ends") spoke of shifts meeting end to start, next to the decisive feature; it is now the
  overlap filter it is: a shift at another store counts from an hour before its start to an hour after its finish.
- The cracker sheet is measured by `generator/cracker.py` on the cut pack, both folds, every figure at its rounding,
  with the blind responses; the prose sheet of round 1 had the 07:00 chain at 26 of 40 only once it was coded.
- Round 3, the judge's Forks S1 and S2 (counting a shift once, its final state, a given-back fill as no cover and an
  absence's two call-ins as one shift, none stated): filed as facts and a definition in the module notes, in Workforce
  Systems' voice (a casual can report an absence in the app or by phone, and an absence reported both ways raises one
  ABS call-in for each report; a shift is covered by the casual who works it, and a casual who gives a shift back has
  not covered it), and the prompt's Table 2 sentence now reads "call-in shifts". With the duplicate reports filed, the
  07:00 chain merges them and becomes the golden's own count of Table 1 (24 of 24, a pair near 70); device A4 (the 2025 roster import raised
  some open lines twice, 12 to 32 per cent at seven stores, booking either copy closing the other FILLED with the
  casual booked) puts it at 5 of 40, and the golden counts open lines from the 2025 roster export.
- Round 3, the pool-size bypass (the casuals free for each open shift put Camberwell's 10-to-4 picking uplift thinnest,
  a median of 5 a shift, so a pool count reached Camberwell without the trip-cost term): more university students in
  Camberwell's own mix (14 and 20 per cent) staffed its base lines, cutting its open hours to 944 so the crew hours
  moved, and their day-off offers filled the uplift (the world's lead fell to 1.15, then Ringwood led); a chain-wide
  rise in university opt-in (45 and 60 per cent) thickened every store's pool and left Camberwell thinnest on the
  median and first on a one-rate count at the log's own take-up. Kept: the uplift runs 9 to 3, so no 4 pm shift abuts it, and
  the East stores' university students and flex casuals opt in at 75 per cent (the three stores sit close together):
  Camberwell's pool is among the deeper ones, every casual in it needs a separate trip, most to another store, every
  pool measure files Williamstown and every one-rate route Werribee or Williamstown, and the world's lead holds at 1.38
  (32 runs).
- Round 3, the judge's Sunshine 5.5 hours (2,028.5 and 1,084.5 against 2,023.0 and 1,079.0): a give-back of a call-in
  raised for an absence (9 December 2025, 4 to 10 pm: the casual who took the re-raised absence call-in reported an
  absence and the store raised it again naming them), which the golden carries under the filed give-back rule; the
  judge looked for give-backs only on fills of open-line call-ins. Not an engine edge; asserted as reading S3d.
- Round 3, the forecast's magnitudes (about 670 at Camberwell, about 400 at Ringwood) did not reproduce in the judge's
  own simulation (580 to 640, and 175 to 225): the write-up's step 4 and the brief's opening state the ranking and the
  margin in words, no magnitude; the chart and the table keep the golden's own forecast.
- Round 3, Werribee's 2025 note: "Werribee's open Christmas shifts went to last year's relief crew and were never put
  out" was wrong for 14 rostered lines Werribee left open and did put out; the note now says its uplift went to the crew.
