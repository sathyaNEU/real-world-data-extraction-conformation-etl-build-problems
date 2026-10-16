# task147: the Weighhouse Hotel's housekeeping block week, August 2027 (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC18. The seed (a 480-room city hotel's in-house
housekeeping crew cleans 380 occupied rooms a night, and a staffing agency supplies one block of temporary housekeepers
for one Monday-to-Sunday August roster week, sent to the week with the most forecast occupied room-nights above the
crew's capacity) was read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism (the
festival week's bookings sold with free cancellation while the validated cancellation rate was fitted on a steady mix) is
a pooled rate against a moved mix, task146's driver in other nouns, and a plain rate-plan split is a reflex; it is not
kept. The pitfall is re-found from how a hotel's book fills: a stay is sold only when every night of it has a room, so a
night that is full at the forecast date blocks every later stay that would run through it, and the nights around it take
far less than their own history's pickup.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task147.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (repeat.question_form, answered below), no BLOCK; nearest drivers 0.08 and under |
| Domain / task type | `supply-chain-logistics` (house domain, the seed's: a hotel's room inventory is perishable stock and the block is staffing planned against the demand forecast for it) in client domain `general-statistics-data-science`, task type `resampling-simulation-monte-carlo-methods` (forecasting): the setting is another field's and the deciding statistical object is the resampled unit; the bookings still to come must be simulated as whole stays, blocks of consecutive nights each accepted only if every night has a room, not night by night, and the night-level summary changes the call |
| Objective | Forecasting & Predictive Modeling: the occupied rooms of each night from Monday 26 July to Sunday 29 August 2027, a window not yet open at the decision (Thursday 1 July 2027, the Thursday five weeks before the festival's opening night) |
| Shape | `other`: the pick and its room-nights above capacity, the concert week's forecast and the room-nights it loses to the full nights, the chart's named parts, and two ask tables on August 2026 operations (arithmetic set at stage 2 in `## Ask sheet`) |
| Decision | `pick_one_of_n` over the five roster weeks, answer unit `named_option` (with its room-nights above the crew's 380 a night to the nearest hundred) |
| Mechanism | gap objective (decisive: each night's occupied rooms are the right measure, and the constraint the night-level forecast never checks, that a stay needs a room every night, removes the natural pick) with population (the booking process's unit is the stay, not the room-night) and time (only the bookings after the confirmation date are blocked); pattern none; generators G8 (a stay through a full night cannot be sold: binary), G2, G13; Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `estimation_fit`; `general-statistics-data-science/resampling-simulation-monte-carlo-methods/1` (resample the independent unit, clusters or blocks, not rows): here the unit is the stay, a block of consecutive nights, and the capacity of each night decides whether a resampled stay is taken |
| Furniture | forum `customer_or_counterparty` (the staffing agency receives the confirmation), forcing event `season_or_peak` (the festival season's roster), organisation family `hospitality_or_tourism`, role family `capacity_planner` (the executive housekeeper), context artifact `close_out_summary` (the night audit's daily statistics), calibration `none`, opening `question-first`, question form `which` |
| Spine | `pms_reservations_extract_2027-07-01.csv`, the property management system's reservation extract on the confirmation morning: one row per room reserved for arrivals from 1 January 2022, cancelled and no-show rooms kept (constructed, about 300,000 rows) |
| Deliverables | `housekeeping_block_2027.xlsx` (the call, each roster week's forecast, the two ask tables), `housekeeping_block_2027.pdf` (a one-page note with the nightly forecast chart against the crew's 380) |
| People | drawn with `guard.py names --geo Ireland --seed 147`: Fergus Roddy (executive housekeeper, the requester; not in the prompt), Edel McCay (rooms division manager, owner of the housekeeping staffing standard), Naoise Meskill (Brennock Hospitality Staffing's account manager), Grainne McGuinn (HR and payroll administrator) |

**Guard.** `guard.py check` on the registered card: WARN `repeat.question_form` (`which` beside task462). Answered: the
decision is a pick of one roster week among five, so the leading question asks which; task462 is an ETL designation set on
an emissions inventory and shares nothing else on the card. No BLOCK; the bans ran against task228, task461 and task462.

**Same-puzzle and same-driver tests.** Gap objective, pattern none (decisive G8), decision `pick_one_of_n`, Gate G
`binding_constraint`: no build in the last twelve (task142 to task462) carries gap objective. Older binding-constraint
drivers (task32 a constraint binding at a finer time resolution, task64 a ceiling on an orthogonal grouping, task79 a
piecewise inverse past a capacity, task94 a delivery on top of held stock, task106 return legs shared along a corridor,
task140 a dependent reservation solved with the residual) share no latent structure: none has requests spanning several
units, each accepted only if every unit it spans has room.

**Abstraction test.** Stripped of nouns: demand arrives as requests for runs of consecutive units, a request is taken only
if every unit of its run has room, and when a few units are full at the forecast date every later request through them is
lost, so the units around them take far less than their own history's intake; a unit-by-unit intake forecast overstates
the group holding the full units and names it. The nearest drivers by score (task138 v1 lineage, a requirement replayed
from each unit's store at the forecast date; task87 v4 lineage, several requests competing for one pool under a joint cap;
task130 v4 lineage, a short reporting window) share neither the run structure nor the default path.

**Data-native sentence.** The Weighhouse's festival guests come for the week, most arriving on a Saturday or Sunday for
six or seven nights, and about a third of a festival night's rooms are booked in the five weeks before arrival; this year
two stadium concerts announced in mid-June sold out the hotel's Friday 13 and Saturday 14 August within days, so every
week-long festival stay that would be booked after 1 July for the festival's first full week, and every Saturday-arrival
stay for the week after, needs a room on a night the hotel no longer has.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` and `--gate-g binding_constraint`: no
driver on file has requests spanning consecutive units blocked by a full unit (the nearest structures are a shared pool
under a joint cap, task87 v4, and shared return legs, task106). `layer2-rigor-patterns.md`: General Statistics,
resampling line 1 (resample the independent unit, not rows) is the client's line for the step; healthcare utilisation line
1 (observed visits are capped demand) is the neighbouring idea this build does not use. `two-layer-task-design.md`:
"handling the data's real structure" is the family. `strategies.md` F3 (a joint limit removing the natural pick, a removal
that re-places nobody) is the family record. The seed's header and Situation (FC18) for the world, decision and quantity
only.

**World.** The Weighhouse Hotel, 480 rooms, in the centre of Carrigeen, an invented mid-sized Irish city. The Carrigeen
Festival of Arts runs each August from the first Friday for twenty-four days, with a preview opening night on the Thursday
before. The in-house housekeeping crew can clean 380 occupied rooms a day; for the festival weeks Brennock Hospitality
Staffing supplies one block of temporary room attendants for one Monday-to-Sunday roster week, confirmed on the Thursday
five weeks before the opening night (Thursday 1 July 2027 this year), and the hotel's housekeeping staffing standard sends
it to the roster week whose nights carry the most occupied rooms above 380. The five roster weeks run from Monday 26 July
to Sunday 29 August 2027. The hotel has no revenue-management system; forecasts are built from the property management
system's book. On Tuesday 15 June 2027 the touring band Rossmore announced two stadium concerts for Friday 13 and Saturday
14 August, tickets on sale on Friday 18 June; the hotel sold both nights out at its prepaid event rate by the following
week.

## Default path

1. Read the reservation extract and build each night's rooms on the books at 00:00 on 1 July 2027 (rooms booked before,
   not cancelled by then), Monday 26 July to Sunday 29 August 2027.
2. For each of the five past Augusts (2022 to 2026), build the same book for the nights aligned on the festival's opening
   (the same weekday and position in the festival) at the same number of days before arrival, and each night's final
   occupied rooms.
3. Each night's pickup is its final less its book; average it over the five years.
4. Add the average pickup to each 2027 night's book, cap at the hotel's 480 rooms, sum each night's rooms above 380 over
   each roster week, and send the block to the largest.

Ends on: the concert week, Monday 9 to Sunday 15 August, about 500 room-nights above the crew's capacity (set on the built
pack at stage 3).
Golden: the closing week, Monday 23 to Sunday 29 August, about 400 room-nights above the crew's capacity (set on the
built pack at stage 3).

## Stump sentence

Forecasting each night's remaining bookings from its own past pickup at the same days before arrival puts the concert week
(9 to 15 August) first with about 500 room-nights above the crew's 380 a night (Ends on); the step that lands it there is
treating each night's pickup as independent of the others, when a festival stay booked after the confirmation needs a room
on every night of it and the two concert nights are already full, so the stays that make most of that pickup cannot be
sold and the closing week (23 to 29 August) carries the most room-nights above capacity.

## Tried and rejected

- The seed's mechanism (the festival week's bookings sold with free cancellation against a cancellation rate fitted on a
  steady mix): a pooled rate carried onto a moved mix, the driver of task146 and task137 in other nouns, and splitting the
  cancellation rate by rate plan is a stratification reflex on a visible column; not kept (a lower rung at most).
- Capacity censoring of past sold-out nights (unconstraining the festival's demand from stop-sell dates): needs a reason
  this year's position against capacity differs from the history's, and "the festival sells out every year" is a reflex
  that lands; the unconstrained-demand family is task18 and task108.
- The expected excess over capacity under forecast uncertainty (a Jensen gap on the nightly floor): at most four tenths of
  a sigma a night, far smaller than the gaps between the festival weeks; it cannot move the pick.
- Timing against demand in the book's pace (a regression of final on book with night-type effects): shrinkage is an
  opponent reflex, and a fitted model on the obvious covariate lands on it.
- Additive against multiplicative pickup chosen by back-test: an enumerable two-way choice a back-testing solver settles.
- Cleaning work weighted by departures against stayovers: the estimand would have to be filed (the WHAT), and the pooled
  minutes per room against the festival's long-stay mix is composition again.
- A city client domain (`urban-regional-science`, forecasting): the deciding quantity is the booking process's resampled
  unit, not a regional forecast; the domain would read as a backdrop.
