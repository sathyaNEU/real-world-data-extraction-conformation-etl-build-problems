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
| Card | `.claude/skills/fingerprint/cards/task155.json`, architecture v1; `guard.py check` PASS, one NOTE (`test.same_driver_older`, differentiated against task117, task137, task37, task44 and task97 in the card); nearest driver 0.05 (task98 v2, lineage) |
| Domain / task type | `economics-econometrics`, task type `discrete-choice-limited-dependent-variable-modeling` (serves Forecasting): each open shift's chance of going unfilled is the product of its eligible casuals' accept-or-decline choices, a binary labour-supply decision at the extensive margin with a fixed cost per trip to work, estimated on the offer log and aggregated over the published roster |
| Objective | Forecasting & Predictive Modeling: the hours each store's call-ins will leave unworked in the four trading weeks 27 November to 24 December 2026, a window not begun at the as-of date (Friday 13 November 2026, the day after the Christmas rosters were published) |
| Shape | `09` (funnel): the call (one store of eight, and its crew hours) carried by row-set asks on each store's call-in funnel and roster; criteria counted in `## Ask sheet` |
| Decision | `pick_one_of_n`, answer unit `named_option` (the store), with the crew hours it will work there to the nearest 10 |
| Mechanism | gap time (decisive: the history's offers seldom sat against the offeree's own rostered shift, and the Christmas roster's Werribee uplift does) with population (the register's fill rate is struck over the call-ins raised, mostly absences at short notice, not over the Christmas open shifts); pattern E (conditioned yield: the split by whether an offer carries on from the casual's own shift is absolute, rebuilt by joining each offer to the roster, and no column names it); generators G14, G6 (the Christmas pool's offers move against the history's mix on that property), G7 (offers go out 07:00 to 21:00 local and a casual on shift answers when the shift ends); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `field_method` (a discrete-choice model of labour supply with a fixed cost of a trip to work); `own:fixed-cost-of-a-trip-in-extra-shift-take-up` |
| Layer 1 | timestamps in UTC in the workforce system against local rostered times (AEDT from 4 October 2026, AEST between); two staff keys (the workforce system's person code and the payroll employee number, a rehire getting a new number); the roster export's layout changed when the rostering tool moved into the workforce system in 2026; store numbers against names and cost centres; shifts ending at midnight written 00:00; effective-dated home store and sister-store opt-in; the unpaid 30-minute meal break on shifts over five hours |
| Furniture | forum `operations_desk` (the workforce planning desk places the crew), forcing event `season_or_peak` (the four trading weeks to Christmas Eve), organisation family `retailer_or_ecommerce`, role family `capacity_planner` (the workforce planning manager), context artifact `capacity_report`, calibration `none`, opening `question-first`, question form `which` |
| Spine | the workforce system's call-in offer log, 29 August 2025 to 12 November 2026 (one row per offer of one call-in shift to one casual, with the answer), about 200,000 rows; constructed |
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
while Camberwell's online-picking uplift sits 10 to 4 on weekdays, when its school-age casuals are in class and no
casual's shift abuts it.

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

Figures from the design prototype (`proto/world26`), to be replaced by `generator/calc.py` on the shipped files and
asserted in `generator/checks.py`.

1. Read the placement standard (the crew works every shift its store's published Christmas roster lists open; it goes
   where it will work the most hours that would otherwise go unworked), the call-in module notes, the call-in register
   and the published Christmas rosters.
2. Sum each store's open paid hours in the Christmas roster: Werribee 2,848, Camberwell 2,220, Box Hill 2,148,
   Sunshine 1,996 and the rest under 1,600.
3. Take each store's share of call-in hours filled in the register's ordinary weeks (September 2025 to November 2026,
   the 2025 Christmas weeks set aside): Werribee 0.48, Camberwell 0.70, the rest 0.61 to 0.76.
4. Multiply each store's open hours by the share left unfilled and place the crew at the largest.

Ends on: Werribee, 2,850 crew hours (about 1,490 of them otherwise unworked, Box Hill next at about 840, Camberwell
third at about 670).

Golden: Camberwell, 2,220 crew hours (about 1,340 of them otherwise unworked, Sunshine next at about 850, Werribee
about 750): each open shift's chance of going unfilled is the chance every casual eligible for it says no, each casual's
answer priced on whether the shift carries on from their own rostered shift at that store, on the December season and
on the other terms the offer log shows.

## Stump sentence

Taking each store's call-in fill rate from the register (ordinary weeks, last Christmas or long-notice call-ins), or
fitting each offer's acceptance on shift time, length, notice, sister-store travel, weekly hours and the December
season, and applying it to the open shifts in the published Christmas rosters sends the crew to Werribee, its 2,850
open hours the crew hours; the step that lands it there is pricing every offer as a separate trip to work, when a
casual whose own rostered shift at that store ends as the open shift starts, or starts as it ends, takes it many times
as often, and Werribee's Christmas uplift is listed against its own casuals' rostered shifts, so Camberwell, whose
picking uplift no casual's shift abuts, is the store, with 2,220 crew hours.

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
