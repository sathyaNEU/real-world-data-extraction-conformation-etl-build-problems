# task147: the Weighhouse Hotel's housekeeping block week, August 2027 (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC18. The seed (a 480-room city hotel's in-house
housekeeping crew cleans 380 occupied rooms a night, and a staffing agency supplies one block of temporary housekeepers
for one Monday-to-Sunday August roster week, sent to the week with the most forecast occupied room-nights above the
crew's capacity) was read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism (the
festival week's bookings sold with free cancellation while the validated cancellation rate was fitted on a steady mix) is
a pooled rate against a moved mix, task146's driver in other nouns, and a plain rate-plan split is a reflex; it is not
kept. The pitfall is re-found from how a hotel's book fills: a stay is sold only when every night of it has a room, so a
night that is full at the forecast date blocks every later stay that would run through it, and the nights around it take
far less than their own history's pickup. Every figure below is measured on the shipped pack by `generator/calc.py` and
asserted in `generator/checks.py` (130 assertions); the clean truth (the world's accepted reservations, no file read) and
the world's own Monte Carlo continuation of the 2027 book are asserted to land in the same bins.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task147.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (repeat.question_form, answered below), no BLOCK; nearest drivers 0.08 and under |
| Domain / task type | `supply-chain-logistics` (house domain, the seed's: a hotel's room inventory is perishable stock and the block is staffing planned against the demand forecast for it) in client domain `general-statistics-data-science`, task type `resampling-simulation-monte-carlo-methods` (forecasting): the setting is another field's and the deciding statistical object is the resampled unit; the bookings still to come must be forecast as whole stays, blocks of consecutive nights each accepted only if every night has a room, not night by night, and the night-level summary changes the call |
| Objective | Forecasting & Predictive Modeling: the occupied rooms of each night from Monday 26 July to Sunday 29 August 2027, a window not yet open at the decision (Thursday 1 July 2027, the Thursday five weeks before the festival's opening night) |
| Shape | `other`: the pick, its room-nights above capacity, the runner-up and its figure, the critical components, the chart's named parts, and two ask tables on the 2026 season (about 50 criteria, `## Ask sheet`) |
| Decision | `pick_one_of_n` over the five roster weeks, answer unit `named_option` (with its room-nights above the crew's 380 a night to the nearest hundred) |
| Mechanism | gap objective (decisive: each night's occupied rooms are the right measure, and the constraint the night-level forecast never checks, that a stay needs a room every night, removes the natural pick) with population (the booking process's unit is the stay, not the room-night) and time (only the bookings after the confirmation date are blocked); pattern none; generators G8 (a stay through a full night cannot be sold: binary), G2, G13; Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `estimation_fit`; `general-statistics-data-science/resampling-simulation-monte-carlo-methods/1` (resample the independent unit, clusters or blocks, not rows): here the unit is the stay, a block of consecutive nights, and each night's capacity decides whether a resampled stay is taken |
| Furniture | forum `customer_or_counterparty` (the staffing agency receives the confirmation), forcing event `season_or_peak` (the festival season's roster), organisation family `hospitality_or_tourism`, role family `capacity_planner` (the executive housekeeper), context artifact `close_out_summary` (the night audit's daily statistics), calibration `none`, opening `question-first`, question form `which` |
| Spine | `pms_reservations_extract_2027-07-01.csv`, the property management system's reservation extract on the confirmation morning: one row per room reserved for arrivals from 1 January 2022, cancelled and no-show rooms kept (constructed, 361,527 rooms reserved) |
| Deliverables | `housekeeping_block_2027.xlsx` (the call, the runner-up, the two ask tables), `housekeeping_block_2027.pdf` (a one-page note with the week and the nightly forecast chart against the crew's 380) |
| People | drawn with `guard.py names --geo Ireland --seed 147`: Fergus Roddy (executive housekeeper, the requester; not in the prompt), Edel McCay (rooms division manager, owner of the housekeeping staffing standard), Naoise Meskill (Brennock Hospitality Staffing's account manager), Grainne McGuinn (HR and payroll administrator); room attendants, supervisors, temps, reception, reservations and visitors from the same tool on its en_IE, pl_PL, ro_RO and pt_BR pools (seeds 147, 1471, 1477), first names unique across the housekeeping people |

**Guard.** `guard.py check` on the registered card: WARN `repeat.question_form` (`which` beside task462). Answered: the
decision is a pick of one roster week among five, so the leading question asks which; task462 is an ETL designation set on
an emissions inventory and shares nothing else on the card. No BLOCK; the bans ran against task228, task461 and task462.
Client domain: `general-statistics-data-science` also hosts task140 (regression diagnostics) and task143 (posterior
inference); this build's task type, world and every card axis but the client domain differ, and the client's own rule for
the domain (the setting is always another field's; the deciding object is the task type's) is the reason it is the honest
home: no client domain is hospitality, and the deciding quantity is the resampled unit.

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
six or seven nights, and close to half of a festival night's rooms are booked in the five weeks before arrival; this year
two stadium concerts announced on 15 June sold out the hotel's Friday 13 and Saturday 14 August within days of going on
sale, so every week-long stay that would be booked after 1 July for the festival's first full week, and every
Saturday-arrival stay for the week after, needs a room on a night the hotel no longer has.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` and `--gate-g binding_constraint`: no
driver on file has requests spanning consecutive units blocked by a full unit (the nearest structures are a shared pool
under a joint cap, task87 v4, and shared return legs, task106). `layer2-rigor-patterns.md`: General Statistics,
resampling line 1 (resample the independent unit, not rows) is the client's line for the step; healthcare utilisation line
1 (observed visits are capped demand) is the neighbouring idea this build does not use. `two-layer-task-design.md`:
"handling the data's real structure" is the family. `strategies.md` F3 (a joint limit removing the natural pick, a removal
that re-places nobody) is the family record. The seed's header and Situation (FC18) for the world, decision and quantity
only.

**World.** The Weighhouse Hotel, 480 rooms, in the centre of Callowfort, an invented mid-sized Irish city. The Callowfort
Festival of Arts runs each August from the first Friday for twenty-four days, with a preview opening night on the Thursday
before. The in-house housekeeping crew can clean 380 occupied rooms a day; for the festival season Brennock Hospitality
Staffing supplies one block of temporary room attendants for one Monday-to-Sunday roster week, confirmed on the Thursday
five weeks before the opening night (Thursday 1 July 2027 this year), and the hotel's housekeeping staffing standard
(HK-04) sends it to the roster week whose nights carry the most occupied rooms above 380. The five roster weeks run from
Monday 26 July to Sunday 29 August 2027. The hotel has no revenue-management system; forecasts are built from the property
management system's book. On Tuesday 15 June 2027 the touring band Velloran announced two stadium concerts at Callowfort
Park for Friday 13 and Saturday 14 August, tickets on sale on Friday 18 June; the hotel sold both nights out, half of
them at its prepaid event rate, within days. Eleven past event weekends (rugby internationals, concerts, a conference)
filled Friday and Saturday nights weeks ahead since 2022, seven of them full five weeks out, none in August. Brennock also
supplies regular temps all summer and day temps on busy days; the 2026 block went to the festival's first full week,
10 to 16 August 2026.

## Default path

1. Read the reservation extract and build each night's rooms on the books at the extract (06:12 on Thursday 1 July 2027:
   rooms booked before, not cancelled by then), Monday 26 July to Sunday 29 August 2027.
2. For each of the five past Augusts (2022 to 2026), build the same book at the same point (the Thursday five weeks before
   that year's opening night, HK-04 4.2) for the nights aligned on the festival's opening (the same weekday and position in
   the festival, so the same days before arrival), and each night's final occupied rooms.
3. Each night's pickup is its final less its book; average it over the five years.
4. Add the average pickup to each 2027 night's book, cap at the hotel's 480 rooms, sum each night's rooms above 380 over
   each roster week (HK-04 3.2), and send the block to the largest.

Ends on: the concert week, Monday 9 to Sunday 15 August, about 600 room-nights above the crew's capacity (556 on the pack;
the closing week second at 419).
Golden: the closing week, Monday 23 to Sunday 29 August, about 400 room-nights above the crew's capacity (413 on the pack),
the concert week next at about 200 (182).

## Stump sentence

Forecasting each night's remaining bookings from its own past pickup at the same days before arrival puts the concert week
(9 to 15 August) first with about 600 room-nights above the crew's 380 a night (Ends on, 556); the step that lands it there
is treating each night's pickup as independent of the others, when a festival stay booked after the confirmation needs a
room on every night of it and the two concert nights are already full, so the stays that make much of that week's pickup
cannot be sold, the concert week falls to about 200 and the closing week (23 to 29 August, about 400) gets the block.

## Three rules

- **Task type:** general-statistics-data-science, resampling-simulation-monte-carlo-methods (serves Forecasting), in the
  house domain supply-chain-logistics: each August night's occupied rooms forecast from the bookings still to come,
  simulated with the booking process's independent unit, the stay, resampled as a whole block of nights against each
  night's remaining rooms.
- **Domain test:** the deciding quantity is the occupied rooms each festival-season night will carry, built from the
  stays still to be booked, and the task type's own rule decides it: resample the independent unit (a cluster or block),
  not the rows; a stay is a block of consecutive nights accepted only if every night has a room, so with two nights full
  the history's post-confirmation stays through them cannot recur, while the night-level summary (each night's own average
  pickup) treats a room-night as if it could be sold alone and changes the call.
- **Swap:** "which month gets the extra crew at a power station, on the megawatt-hours above the crew's capacity" keeps a
  forecast against a capacity line, but a megawatt-hour is not a block spanning several units that one full unit refuses,
  so the forecast unit by unit is the right one there and the quantity that decides this call stops making sense.
- **Layer 1:** the reservation extract one row per room (rooms booked together share a booking reference) with booking and
  cancellation times in UTC against arrival dates in local time, written by the property management system; date and
  guest-count changes in its separate amendment log, the extract carrying current dates; rate, channel and market codes
  in a separate code list, the online agencies renamed in the 2025 channel review; the night audit's daily statistics one
  sheet per year in two layouts after the 2024 system upgrade; complimentary, house-use and day-use rows beside sold
  rooms; the festival's dates in its own programme history; on the ask paths the housekeeping app's task log, its user
  list and the HR list as they stand now, Brennock's timesheets and invoice, the staff access system's badge events and
  reception's day-badge log, and the payroll overtime lines by pay period. Each is what these systems write; none moves
  the call (R2, asserted per item).
- **Layer 2:** `estimation_fit`, resample the independent unit: the bookings still to come are blocks of nights, each
  taken only if every night has a room, so the forecast for the concert week's other nights is their history's
  post-confirmation pickup less the stays that ran through the aligned Friday and Saturday, which cannot be sold this year;
  the easy route forecasts every night from its own pickup and files the concert week.
- **Decisive step:** forecasting the remaining bookings by stay: every past post-confirmation stay through the nights now
  full is unsellable, which takes about 420 room-nights from the concert week's other five nights and about 190 from the
  week after; this moves the block from the concert week (about 600) to the closing week (about 400), the concert week
  next at about 200.
- **Not semantics:** no field, code or definition says how many rooms the nights still to come will take, or that a night's
  pickup runs through other nights; the full nights are read correctly by everyone (480 rooms on the book, capped at the
  hotel's 480), the status and rate codes, the amendment log and the comp and day-use rows are read correctly on the easy
  route too, and an analyst who reads every one of them correctly forecasts each night from its own past pickup and files
  the concert week at about 600 room-nights above capacity.
- **Not rule application:** the strict rule 3 test, on every shipped sentence that bears on how the figure is computed: the
  prompt's question; HK-04 sections 2.1 (the roster weeks, numbered 1 to 5 in every season), 2.2 (a roster week covers the
  rooms occupied on its seven nights), 2.3 (an occupied room, complimentary and house-use rooms in, no-shows and day-use
  rooms out), 3.1 (the crew's 380 a day), 3.2 (rooms above capacity summed night by night), 4.1 (the block to the week
  with the most, forecast for the season) and 4.2 (confirmed on the Thursday five weeks before the opening night on the
  book as it stands that morning); the PMS export notes (one row per room under a shared booking reference, times in UTC,
  a reservation's nights, current dates, the hotel's 480 rooms). Executed word for word on the clean truth, together, they
  fix the target and give no forecast: they carry no pickup, rate, history or method, never say how the remaining bookings
  arrive, and none says a stay needs a room every night or that a full night blocks its neighbours; the estimators they
  admit (night-level pickup, ratio, regression, rate-plan realisation or the seasonal average) all file the concert week.
  The behaviour the decisive step turns on is inferred from the reservation history, and the data rejects the rival by a
  visible margin: on the seven past event weekends full five weeks out, night-level pickup over-forecast the 49 nights
  beside the full ones by 41.4 rooms a night (t 7.3, mean absolute error 43.5) while the stay-level forecast missed by -6.7
  (mean absolute error 14.7). Asserted in `checks.py` (the R3 strict block: the sentences ship word for word, none names a
  stay against availability, a pickup, a rate or a method, and executed they give no closing week; R3a and R3b on the
  clean truth and the pack).
- **Analyst test:** a strong analyst who reads every field, code and HK-04 correctly builds each night's book at the
  confirmation, adds each night's average pickup from the same days before arrival in the five past Augusts (or scales the
  book by its past final-to-book ratio, fits final on book, or splits the book's realisation by rate plan), caps the concert
  nights at 480 and calls the concert week at about 600 room-nights above capacity (Ends on: 556; every night-level variant
  479 to 563, the seasonal average 503); only the forecast by stay, the post-confirmation stays through the two full nights
  unsellable this year, calls the closing week at about 400 with the concert week next at about 200 (executed in
  `checks.py` on the clean truth and on the pack).
- **Estimand:** HK-04 4.1 and 3.2 with the prompt: the roster week, Monday to Sunday from 26 July to 29 August 2027, whose
  nights carry the most occupied rooms above 380, summed night by night, forecast on the book as it stood at the extract on
  Thursday 1 July 2027; an occupied room is every room with a guest overnight (HK-04 2.3), every stay still to be booked
  included. Population, outcome, window, unit and comparison are filed; the forecast's method is not.
- **No decoy:** no memo, earlier forecast, revenue-management output, agency proposal or stakeholder figure states or
  argues a week, a figure or a method; the night audit statistics and the events diary are records of the past and of the
  calendar; the distractors (the competitor rate shop and the city tourism office's monthly occupancy survey) rank nothing.
- **No certified replay:** nothing certified or published is reproduced; the remaining bookings' structure is estimated
  from the raw reservation history, and no past forecast ships (the 2026 block's week appears only as the invoice's week,
  a fact of that season).
- **Lesson:** a forecast of a capacity-limited stock built from requests that span several units must be simulated on
  the requests, not unit by unit: a unit that is already full removes the later requests that need it, so its neighbours
  take far less than their own history says, even while every unit's history is read correctly; no build on file teaches
  requests spanning consecutive units against a full unit (task87 v4 shares a pool under a joint cap, task106 shares
  return legs along a corridor, task16 floors per-cell shortfalls).

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear. Values
measured on the pack.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the seasonal average of the five past Augusts' finals at the aligned nights | no | no | yes: the seasonal naive | no | no | yes: one mean per night | readable |
| R1 (the default path) each night's book plus its average pickup at the same days before arrival | no | no | yes: classical additive pickup | no | no | yes: one sum | readable |
| R1m the book times its past final-to-book ratio | no | no | yes: multiplicative pickup | no | no | yes: one ratio | readable |
| R1r final regressed on book (weekday effects, or one effect per night) | no | no | yes: the obvious covariate | no | no | yes: one slope | readable |
| R1L last year's pickup only | no | no | yes: the latest-period rate | no | no | yes | readable |
| R2 the book realised by rate plan (the prepaid event rooms kept) | no | yes: the rate code | yes: a stratification on a visible column | no | no | yes | readable |
| R2b the full nights' block applied inside the concert week only (a partial of R3: the call right, the runner-up wrong) | no | no | no | no | no | no: a stay filter over past reservations | silent |
| R3 (decisive) the remaining bookings forecast by stay, every past post-confirmation stay through the two full nights unsellable this year | no: no sentence says a stay needs a room every night, how a night's pickup arrives or that a full night blocks others | no: no column marks a stay through another night; the stays are rows with arrival and departure, the full nights a count of rooms | no: night-level pickup is the reflex, and its back-test on past Augusts passes (no August had a night full at the confirmation) | no: no forecast, past block decision or certified figure ships | no: nothing in the files is wrong | no: a filter of five years' reservations by their nights against this year's full nights, then a pickup by night built from the survivors | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py`.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "roster week" | Monday to Sunday, the five from 26 July to 29 August 2027 | Sunday to Saturday; the week of cleaning days | not the standard's week (the closing week would still lead, 457) | HK-04 2.1 and 2.2 (a roster week covers the rooms occupied on its seven nights, Monday night to Sunday night) |
| SF2 | "occupied rooms" | every room with a guest overnight, complimentary and house-use rooms in, no-shows and day-use rooms out | sold rooms only | same call (asserted: W5 403, W3 180) | HK-04 2.3 |
| SF3 | "room-nights above the crew's capacity" | each night's occupied rooms above 380, summed over the week's seven nights | the week's occupied room-nights less 2,660 | same call and runner-up (asserted: W5 413, W3 139 netted) | HK-04 3.2 |
| SF4 | "the book as it stood this morning" | the extract, 06:12 on 1 July 2027 | the book at 00:00 on 1 July | same call (asserted: 417, 183) | the extract's stamp; HK-04 4.2 |
| SF5 | the comparable point in past years | the Thursday five weeks before each year's opening night (the same days before arrival for every aligned night) | 1 July of each year | same call, same bins (asserted: 380 and 175) | HK-04 4.2 |
| SF6 | the years the pickup is measured on | 2022 to 2026 | any four of them, the last three, the last two | same call, same bins (asserted: closing week 401 to 439, concert week 176 to 188) | none needed |
| SF7 | the cap on a full night | 480 rooms less the event rate's no-shows (3.3 per cent) | 480 | same call (asserted: W3 213) | the hotel's 480 rooms (PMS notes) |
| SF8 | "the week that would come next" | the roster week with the next most room-nights above capacity, on the same forecast | the calendar week after the block week (from Monday 30 August) | not a roster week of the season, so no figure of its own | HK-04 2.1 (the season's five roster weeks); the prompt ("with its own figure") |
| SF9 | rounding | each week's figure from unrounded nightly forecasts, to the nearest hundred, once | per night | asserted one arithmetic (413 both ways) | the prompt's last sentence |
| SF10 | booking and cancellation times | UTC in the extract, the cut at 06:12 local (05:12:44 UTC) | read as local | same call (asserted: 413, 182) | the PMS notes (times in UTC) |
| SF11 | the past books' dates | as they stood at the comparable point (amendments after it undone) | the current dates | same call (asserted: 417, 184) | the amendment log |
| SF12 | a reservation's nights | arrival to the night before departure | departure night included | not the hotel's count | the PMS notes |
| SF13 | status codes | OUT and INH stayed; CXL and NS did not; RES on the book | NS counted occupied | the call and the next week hold (asserted: W5 476, W3 200), the closing week's figure a bin up | HK-04 2.3 ("No-show and day-use rooms are not.") |
| SF14 | rooms booked together | one row per room, the booking reference shared | one room per booking reference | not the hotel's count: short of the night audit by 41 to 92 rooms on every past festival night (asserted) | the PMS notes |
| SF15 | "forecast" | the expected occupied rooms of each night | a pessimistic or high case | same call (the golden matches the world's own expectation in both bins) | the prompt; HK-04 4.1 |
| SF16 | the festival's alignment | each past night at the same weekday and position from the opening Friday (the same-numbered roster week) | the same calendar date | the call holds (asserted: W5 330, W3 169), the closing week's figure a bin down | HK-04 2.1 (roster weeks numbered 1 to 5 in every season); the programme history (the first Friday moves up to five days) |

## Ladder

Measured on the pack by `calc.py` (the accepted reservations as the extract holds them, every past book rebuilt at its
comparable point). Each figure is the roster week's forecast room-nights above 380 summed night by night; the pick and its
margin over the next week.

| Rung | Construction | W1 | W2 | W3 (concerts) | W4 | W5 (closing) | Pick | Dies to |
|---|---|---|---|---|---|---|---|---|
| R0 | the five past Augusts' finals at the aligned nights | 0 | 122 | 503 | 351 | 407 | W3 1.24x | the book: this year's concert nights are full five weeks out, and the history's finals carry the festival stays that cannot be sold this year |
| R1 (default) | book plus each night's average pickup at the same days before arrival | 15 | 129 | 556 | 229 | 419 | W3 1.33x | a stay needs a room every night: about 420 room-nights of the concert week's pickup ran through the aligned Friday and Saturday |
| R1m | book times its past final-to-book ratio | 57 | 122 | 502 | 147 | 418 | W3 1.20x | as R1 |
| R1t | book at its past realisation plus the past post-confirmation bookings | 9 | 128 | 557 | 236 | 413 | W3 1.35x | as R1 |
| R1L | last year's pickup only | 31 | 124 | 528 | 118 | 434 | W3 1.22x | as R1; and one year's pickup |
| R1r | final on book with weekday effects, pooled | 268 | 117 | 479 | 85 | 111 | W3 1.79x | as R1; and the pooled slope mixes July with the festival |
| R1rf | final on book with an effect per night | 6 | 128 | 563 | 251 | 415 | W3 1.35x | as R1 |
| R2 | R1t with the book realised by rate plan (event rooms at their own no-show rate) | 9 | 128 | 557 | 237 | 413 | W3 1.35x | as R1 |
| R2b | the full nights' block inside the concert week only | 9 | 128 | 182 | 236 | 413 | W5 1.75x | the Saturday-arrival week stays through Saturday 14 August also carried the week after: the runner-up is the concert week (182), not the week after (236 here, 137 when its own blocked stays come out) |
| golden (R3) | by stay: past post-confirmation stays through the two full nights unsellable, the full nights at 480 less the event rate's no-shows | 9 | 60 | 182 | 137 | 413 | W5 2.27x | (the golden) |

- **Every construction of the golden** (C1, asserted on the pack): all five years 413 (the concert week 182); each year
  left out 401 to 433 (176 to 188); the last three years 405 (186); the last two 439 (186); the additive form (book plus
  pickup less the blocked stays, R3b) 419 (189); the books at midnight 417 (183); the past books on 1 July of each year
  (SF5) 380 (175); the book realised by rate plan 413 (189); the full nights at 480 (SF7) 413 (213). Span 380 to 439 for
  the closing week, every one in the 400 bin (the last two years alone 11 room-nights below 450, the books on 1 July 30
  above 350, the golden 37 below 450); the concert week 175 to 213, every one in the 200 bin. The runner-up is the concert
  week under every construction (the week after 122 to 147). The clean truth's golden, computed straight from the
  world's reservations with no file read, is 413 and 182.
- **Stay replays (C4, asserted).** Re-selling the full nights' rooms that their own book will free (by rate code from the
  past seasons and the event rate from the past event weekends: 19 and 20 rooms) to each past season's later stays in
  booking order, the other nights against the book realised, files 408 and 201: the golden's bins. Two cruder replays
  keep the call and the next week and miss one figure each, and the data rejects both: replaying the stays against the
  2027 book as it stands (its future cancellations never freeing a room) files 345 for the closing week, and the same
  replay on the past Augusts under-forecasts each season's closing week every year (-55, -50, -24, -67, -39) and its
  concert week by 107 on average while the golden's form misses by -3 and -9; freeing the full nights at the pooled past
  realisation (55 rooms a night, no-shows included) files the concert week at 269, while the full nights' own book (half
  at the non-refundable event rate) frees about 20.
- **The world's own expectation** (`mc_truth`, 12 continuations of the 2027 book with fresh demand and the book's own
  cancellations after the extract): the closing week 424, the concert week 200, the week after 161: the golden method
  recovers the world in both bins.
- **Rate evidence.** The share of each night's post-confirmation pickup that ran through the aligned Friday and Saturday,
  2022 to 2026: the concert week's Monday 0.20, Tuesday 0.24, Wednesday 0.34, Thursday 0.54, Sunday 0.57; the week after
  Monday 0.30, Tuesday 0.17 and under 0.14 later; the opening week's Saturday and Sunday 0.14 and 0.19. In room-nights:
  about 420 a season on the concert week's other five nights, about 190 on the week after.
- **One sigma.** The golden's standard error from the five years' spread: the closing week 21.7 room-nights (413 plus or
  minus 22 stays inside 350 to 450), the concert week 7.5 (inside 150 to 250); the call holds at two sigma either way
  (369 against 197); it flips only if the concert week gains about 230 room-nights, about ten sigma.
- **The data rejects the default.** On the seven past event weekends full five weeks out (2022 to 2026, none in August),
  night-level pickup at the same days before arrival over-forecast the 49 nights beside the full ones by 41.4 rooms a
  night (t 7.3, mean absolute error 43.5); the stay-level forecast missed by -6.7 (mean absolute error 14.7). On the past
  Augusts at their comparable points (no night full) the night-level forecast's own back-test passes (mean error 4.3,
  -2.5, -0.5, -12.1 and 9.6 rooms a night by season).
- **Position and dominance.** On the default the golden week is second (419 against 556, 1.33x), the call's rival first;
  the decisive move takes 373 room-nights from the concert week (556 to 182) and 6 from the closing week (419 to 413), so
  the edge on the decisive axis (373) is 2.7 times the concert week's carried advantage on the default (136). Every lower
  correction (R1m, R1r, R1L, R2) leaves the concert week first.
- **Bins.** The default's concert week 556 (600 bin), the golden's closing week 413 (400 bin), two bins apart; the
  golden's concert week 182 (200 bin).
- **Worth.** Graded: the call and its figure, the runner-up and its figure, and the critical components (the concert
  nights full on the book; the concert week's forecast about 200; the closing week's about 400), never an intermediate.

## Closure table

Each row's assertion is in `checks.py`.

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every room occupied on each night 26 July to 29 August 2027, the stays not yet booked included | filed (HK-04 2.2, 2.3, 4.1); SF2 |
| 2 | Unit of account | occupied rooms, each room of a multi-room booking counted | filed (PMS notes: one row per room); SF14 |
| 3 | Attribution window | a night belongs to the roster week holding its date | filed (HK-04 2.1, 2.2); SF1 |
| 4 | As-of dating | the book at the extract, 06:12 on 1 July 2027; past books at each year's comparable point | the extract stamp; HK-04 4.2; SF4, SF5 |
| 5 | Version basis | past reservations as they stood at the comparable point (later amendments undone) | the amendment log; SF11 asserted |
| 6 | Denominator | none: rooms are counts | design |
| 7 | Weighting | each past year once | C1 across subsets (SF6) |
| 8 | Window length | five past Augusts | C1 (SF6) |
| 9 | Boundary inclusivity | a reservation's nights run from arrival to the night before departure | filed (PMS notes); SF12 |
| 10 | Rounding path | nightly forecasts unrounded, floored at 380 night by night, summed, rounded once to the nearest hundred | the prompt; SF9 |
| 11 | Tie-break | none arises | the golden 2.27 times the runner-up (asserted, 230 room-nights) |
| 12 | Maturity and censoring | past nights complete at the extract; 2027 nights forecast; the history's capacity censoring small | C1: the world's own expectation agrees (424 against 413) |
| 13 | Order of operations | stays filtered against the full nights, then nightly pickup, then the cap, the floor and the sum | the order is the decisive step (forced by the data: the event-weekend back-test 41.4 against -6.7) |
| 14 | Row order | none matters | C1 asserted (the extract read in reverse gives the same figures) |
| 15 | Duplicate resolution | none: one row per room, no repeated confirmation numbers | asserted |
| 16 | Identity normalisation | channel codes renamed in 2025 (no bearing on the call) | asserted texture |
| 17 | Netting against gross | occupied rooms are gross of nothing; no-shows not occupied | filed (HK-04 2.3); SF13 |
| 18 | Dimensional units | rooms a night; room-nights a week | the prompt; HK-04 3.2 |
| 19 | Code and status semantics | status (RES, INH, OUT, CXL, NS) and rate codes (BAR, BARBB, CORP, SAV14, ADV, ADVBB, EVT, GRP, COMP, HSE, DAY) | the PMS notes and the code list; never the stump |
| 20 | Integerisation | none before the final rounding | design |
| 21 | Clause scope | HK-04 covers the festival season's roster weeks | filed |
| 22 | Forward window contents | the season's nights: the August bank holiday on 2 August, the festival from 6 to 29 August, the concerts on 13 and 14 August, nothing else in the events diary | the events diary; the festival's programme history; the holiday list (asserted) |

## Literal reader

Executing the prompt, HK-04 and the PMS export notes word for word fixes the target (the roster week, Monday to Sunday
from 26 July to 29 August 2027, with the most occupied rooms above 380 summed night by night, forecast on the 1 July book)
and every term but the forecast's method; every reading converges on the golden's call and bins or violates a quoted line
(SF1 to SF16), and the easy answers come from easy methods on the same literal target (each night's own pickup, ratio or
regression; the seasonal average), never from another reading.

## Oracles

- The night audit statistics: each past night's occupied rooms, equal to the extract's rooms that stayed from 9 January
  2022 (asserted; before it the audit also counts December 2021 arrivals the extract does not hold); they confirm the
  finals under every method and are blind to the decisive step (they hold no book and no stay).
- The events diary: the dates of past and coming events, no figure; it lets an analyst find the past event weekends, the
  back-test the default fails, and ties under nothing.
- The festival's programme history: the dates, no figure.
- The competitor rate shop and the city tourism office's monthly occupancy survey (distractors): rank nothing; the call
  and both asks unchanged with either deleted (asserted).
- Nothing ties only under the golden: no forecast, past block decision or certified figure ships.

## Ask sheet

**Main call's declared row population:** the reservation extract's rows with a night from 26 July 2022 to 29 August 2027
in a festival season (the five past seasons and this one), the amendment log's rows for them, the code list, the
festival's programme history, HK-04 and the PMS export notes. Device and hazard rows in it: 0 (asserted: the call reads no
housekeeping, badge, timesheet, invoice or payroll file, and computed from the main files alone it is the golden).
Neither ask is keyed to the call, its construction or its figures; they share no primary device.

**Ask A. Last year's season by roster week: departure cleans and stayover services by the crew and by Brennock's temps,
and the crew's overtime** (25 figures: 5 weeks x (crew departures, crew stayovers, Brennock departures, Brennock
stayovers, crew overtime hours)).
- H18 home: how each of last season's roster weeks was carried, the workbook's second table, a measure every candidate
  week carries (its 2026 counterpart) that the call does not turn on; in the executive housekeeper's words ("departure
  cleans", "stayover services", "our crew", "Brennock's temps", "overtime").
- Construction: the housekeeping app's tasks of the 2026 season (27 July to 30 August 2026) completed as departure cleans
  or stayover services by service date (a re-clean after a failed inspection part of the service it repeats, do-not-disturb
  and refused stayovers not serviced, HK-04 2.4), credited to who did them (the login's user, or the person a supervisor's
  note names) and to Brennock when that person is on Brennock's timesheet for the day; the crew's overtime hours from the
  payroll lines, by the date worked in each line's reference.
- Golden: 27 July to 2 August 920, 1,100, 184, 206, 17.25 hours; 3 to 9 August 796, 986, 113, 166, 20.75; 10 to 16 August
  788, 1,336, 341, 577, 15.25; 17 to 23 August 929, 1,460, 145, 249, 11.25; 24 to 30 August 962, 1,574, 187, 276, 14.25.
- Primary device A1 (D2, an attribute at the wrong vintage, a type-2 row read current): three of Brennock's six regular
  temps of summer 2026 worked under app logins IT issued them on 20 and 21 July 2026 and were later taken on by the hotel
  (12 October 2026, 11 January 2027, 8 March 2027); their logins were moved to the in-house group and the HR list (both as
  they stand in June 2027) shows them as room attendants with start dates after the season. Every roster week of 2026 has
  their services, so reading the user list's group credits Brennock's work to the crew in all twenty service cells. Only
  Brennock's 2026 timesheets and the HR start dates show who they were then. Benign twins: four crew hired in 2026 and six
  summer contracts, logins created in 2026, on no Brennock timesheet.
- Second device A2 (D7, the true key elsewhere): Brennock's day temps on busy days had no app login; the floor supervisor
  logged their rooms under her own login with the temp in the task note ("Brennock - Ewa", "Nela (Brennock)", "agency -
  Stella"); 139 such tasks, in the first, fourth and fifth weeks. Attribution by login credits them to the crew. Benign
  twin: 54 tasks a supervisor closed for a crew member whose tablet was down ("Ruth's rooms, tablet down").
- Third device A3 (D8, a settlement date for the event date): payroll posts overtime in the fortnightly pay period after
  the one it was worked in, the date worked only in the line's reference ("OT 12/08/26 2.25h"); allocation by the pay
  period end puts 4.25, 0, 18.75, 0 and 36 hours in the five weeks against 17.25, 20.75, 15.25, 11.25 and 14.25.
- Hazards: HA1 re-cleans logged as a second task with the parent task referenced, closed by the same login (154); HA2
  do-not-disturb and refused stayovers (276 and 162); HA4 the app's times in UTC beside a local service date (no service
  crosses midnight).
- Stops (measured, each asserted): S1 the user list's current group, all 20 service cells off (27 July week 999, 1,199,
  105, 107); S2 attribution by login with the notes unread, all 20 off; S3 the cracker (S1 and S2 with every filed rule,
  the battery and the overtime by pay period), all 25 off; S4 overtime by pay period, all 5 weeks off; S5 re-cleans
  counted, every week's departures high (27 July week 941 and 189); S6 the over-clean (every login created in 2026 counted
  as Brennock's), all 20 off (27 July week 651, 732, 453, 574).
- Span: the task log, the app's user list, the HR list, Brennock's timesheets, the payroll overtime lines, HK-04's service
  definitions (6 files); 15 columns.
- Realism: an agency's regulars get logins and are later hired; a supervisor logs a day temp's rooms under her own login;
  payroll pays overtime the period after it is approved.

**Ask B. Last year's block week: the hours Brennock may bill for the block each day, and the week's charge before VAT**
(8 figures: 7 days' hours and the week's charge).
- H18 home: an audit trail of last season's block, the workbook's third table, the budget line for this year's; a
  measure the call does not turn on.
- Construction: the framework agreement's billing rules (4.1 the later of the booked start and the first entry to the
  earlier of the booked end and the last exit, in whole quarter hours rounded down; 4.2 thirty minutes off a shift over six
  hours; 4.3 at least four hours for a booked shift attended; 5.1 EUR 22.56 an hour, Sundays at one and a quarter), each
  block temp's entries and exits from the staff access records, the temps known by reception's day-badge log (by date and
  name), the block's temps and booked shifts from Brennock's timesheets.
- Golden: 59.25, 59.50, 55.75, 59.25, 59.75, 59.75 and 59.75 hours from Monday 10 to Sunday 16 August 2026; the week's
  charge EUR 9,654.27.
- Primary device B1 (D8, a clock against a filed cutoff): the loading-bay reader LB-02, added to the access system in May
  2026, exports its events in UTC while the staff entrance exports local time; nothing says so; two or three block temps
  returning linen carts leave by the loading bay at the end of the shift on every day of the block week, so their last
  exit reads an hour early and every day's hours and the week's charge come out low. Only a cross-file cut shows it (the
  housekeeping app's last completions after the apparent exit) or the loading bay's exits clustering an hour before the
  entrance's (median 15:10 against 16:10, asserted).
- Hazards: HB1 day badges reissued from a pool every morning (22 badges, the busiest issued 10 times; a join on the badge
  alone fans out); HB2 a temp sent home at 10:00 on the Wednesday (four hours billed); HB3 the Sunday rate; HB4 the break
  deduction; HB5 rounding down to the quarter hour; HB6 Brennock's invoice billing the booked shifts (7.50 hours each).
- Stops (measured, each asserted): S1 the access times as exported (B1 missed), every day off (56.75 to 57.75 hours on the
  full days); S2 the invoice's booked hours (60.00 a day, EUR 9,813.60), all 8 off; S3 the cracker (S1 with every rule),
  all 8 off; S4 the minimum missed, Wednesday and the charge off; S5 the Sunday rate missed, the charge off; the
  over-correction (every reader moved an hour) all 7 days off.
- Span: the access system's events, reception's day-badge log, Brennock's timesheets, Brennock's invoice and the framework
  agreement (5 files); 12 columns.
- Realism: a second door reader added later keeps its controller's default clock.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 re-cleans | the app logs a re-clean as a new task | Ask A departures and stayovers | 154 tasks counted twice when counted |
| HA2 DND and refused | the app closes a stayover the guest declines | Ask A stayovers | 438 tasks when counted |
| HA4 UTC task times | the app's database | Ask A | none (no service crosses midnight) |
| HB1 reissued day badges | reception's badge pool | Ask B | fan-out when joined on the badge alone |
| HB2 the sent-home temp | the hotel cancelled a shift on the day | Ask B Wednesday and the charge | 2 hours when missed |
| HB3 to HB6 the rules and the invoice | the framework agreement; Brennock's billing | Ask B | each rule's own cells |

**Referee.** For Ask A, Brennock's 2026 timesheets and the HR start dates give who was Brennock's that summer, and the
task notes name the day temps; for Ask B, the housekeeping app's completions and the entrance's exits give each day's
working time against the loading bay's apparent exits. Each is a source the golden reads, not a control: no file ties only
under the golden, and no filed sentence says the loading bay's clock, the login moves or the supervisor's logging
(asserted).

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A services by week, crew and Brennock (20) | the user list's current group and the login, every filed definition, the battery (re-cleans, DND, refusals handled) | every cell off (27 July week 1,018, 1,216, 86, 90) | miss |
| A crew overtime by week (5) | the payroll lines by pay period end | 4.25, 0, 18.75, 0, 36 against 17.25, 20.75, 15.25, 11.25, 14.25 | miss |
| B hours by day (7) and the week's charge (1) | the access times as exported, every framework rule applied | every day off by about an hour per loading-bay leaver | miss |
| the note's chart | the cracker's nightly forecast drawn as the golden draws it | its parts carry the cracker's call only when the call lands | outside |

Mirror leakage: about 8 per cent of the ask weight. The mirror is the most attractive wrong rung, R1 (night-level pickup,
the concert week at about 600); it runs the same ask paths as the cracker, so it misses every Ask A and Ask B figure and
keeps about three of the chart's five parts (the nights, the 380 line, the full nights marked; it highlights the concert
week).
Pair ceiling: 34 (the cracker about 52 with the call, its components, the instructions and the chart's parts; the mirror
about 16 with the instructions, three of the chart's parts and the component it shares, the concert nights full on the
book; it misses the call, the runner-up and both figures; 38 ask criteria). The most obvious device is A3 (the date
worked sits in each payroll line's reference): cracked, the cracker keeps the five overtime figures and the pair is 38.
A1 or B1 cracked alone keeps eight figures each (A1 the second and third weeks' services, A2 still moving the others; B1
all of Ask B): pair 40. A2 cracked alone keeps nothing (A1 moves every service cell).

## Build record

Stage 3, 2026-10-16. `generator/build.py`: the world (`world.py`, 304,867 accepted reservations, seed 1472027), the PMS
files (`records.py`), the 2026 season's housekeeping, payroll, access and agency records (`ops2026.py`, `cast.py`), the
documents (`docs.py`), the distractors (`distract.py`), the goldens and `figures.json` (`deliver.py`), `metadata.json`;
then `checks.py` (130 assertions, 0 failed), `verify.py` (its own code path, standard library and openpyxl: the call W5
413, the next week W3 182, the default W3 556, both asks' 33 figures equal in the workbook), a second full build compared
byte for byte (20 target files, 2 goldens, metadata.json, figures.json, target.zip identical) and target.zip. Gates:
`figures_check.py` PASS (every figure in blocks 1 to 4 in figures.json); `precut.py` exit 0; `voice-check.py` PASS (932
characters); `scrub_producer_metadata.py` clean on target and golden; `leak.py --asof 2027-07-01` REVIEW (no LEAK, every
line answered below); `guard.py surface`, `heart` and `validate` recorded in pipeline.json.

## Leak review

- Sweep 3, `pms_export_notes.txt` carries 480 ("The hotel has 480 rooms"): the hotel's size, a filed fact every route
  reads (the full nights hold it), not an answer; the call's figures (400, 200) appear in no input. Harmless.
- Sweep 3, `HK-04_housekeeping_staffing_festival_season.pdf` shares 14 of 20 words with the committed call: it is the
  standard that defines the decision in the same vocabulary (the block, a Monday-to-Sunday roster week, room-nights above
  the crew's capacity, forecast); it names no week, date or figure of 2027 (the R3 strict block asserts it). Harmless.
- Sweep 4, `HK-04_housekeeping_staffing_festival_season.pdf`, `brennock_framework_agreement_2025.pdf` and
  `pms_export_notes.txt` share three to six words with the stump paragraph (nights, festival, confirmation, booking,
  reservation, arrival, extract): the standard's definitions, the agreement's bookings and the export's field notes; none
  names a stay against a full night, a pickup or a method (the R3 strict block asserts it). Harmless.
- Sweep 9, dates after 1 July 2027 in the extract and amendment log (future arrivals on the book), the rate shop (the
  season's nights shopped), the festival's programme (the 2027 edition) and the events diary (coming events): forward-
  looking records on the allow-list (H16); nothing dated after the extract was made after it (asserted). Harmless.

## Tried and rejected

- The seed's mechanism (the festival week's bookings sold with free cancellation against a cancellation rate fitted on a
  steady mix): a pooled rate carried onto a moved mix, the driver of task146 and task137 in other nouns, and splitting the
  cancellation rate by rate plan is a stratification reflex on a visible column; kept only as rung R2.
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
- Festival stays of three to five nights arriving Thursday to Saturday (prototype 1): the full Friday and Saturday blocked
  little of the week's Monday to Wednesday, and the default and golden landed within the year-to-year noise; the festival
  stays are week stays, most arriving on a Saturday, as a three-week arts festival's guests book.
- Festival bookings on one lognormal lead (median 50 to 80 days): the booking curve was steepest at the confirmation, so the
  past books on 1 July against the same days before arrival moved the closing week by about 70 room-nights; a spring wave
  after the programme's launch and a summer wave in the last five weeks put the confirmation in the trough between them.
- The festival's first full week normally strongest by a wide margin with the closing week far behind: the golden's
  closing week came out near the concert week's floor (its two full nights alone carry about 180 room-nights above 380);
  the closing week strengthened (its finale weekend), which narrows the default's margin to 1.2 to 1.4 times, kept.
- Poisson request counts: the five past Augusts' weekly pickup swung by 80 to 130 room-nights, a standard error near 40 on
  the golden's figure; counts drawn with a tenth of Poisson's variance (the hotel's demand is steady year to year) bring
  it to about 22, inside the 100-room-night bin.
- Every roster week's figure in the prompt: the opening week (60) and the week after the concerts (137) sit within one sigma
  of a rounding edge at the nearest hundred; the prompt asks for the block week and the runner-up only.
- The runner-up asked as "the concert week's forecast beside it": presupposes the concert week is not the pick (a leak);
  asked as the week that would come next, with its own figure.
- A third ask on overtime alone: folded into Ask A as its fifth column (the same weeks, its own device).
- The city named Carrigeen and the band Rossmore (stage 2): both are real Irish place names (H21); renamed Callowfort and
  Velloran at the generator, both searched clear of real places, acts and venues; the hotel and agency names searched
  clear too. Visitors on the day-badge log first written as initials and contractor brands: replaced by drawn names and
  plain purposes.
- HA3, a stayover converted to a departure when the guest leaves early: needs early departures in the reservation history
  to stay consistent with the extract and the amendment log; dropped from Ask A, whose devices and hazards stand without
  it.
- The replay of each past season's later stays, whole, against the 2027 book as it stands: the book's future
  cancellations never free a room, so the near-full closing weekend refuses stays and the closing week falls to 345 (300
  bin); kept as a C4 rival the past Augusts reject (it under-forecasts every season's closing week).
- Freeing the full nights at the pooled past realisation before the replay: frees 55 rooms a night against the 20 the
  full nights' own book (half non-refundable) will release, and puts the concert week at 269; kept as a C4 rival.
- No-shows counted as occupied and calendar-date alignment as same-call readings (stage 2 note): each keeps the call but
  moves the closing week's figure a bin (476, 330); closed by HK-04 2.3's sentence and by numbering the roster weeks 1 to 5
  in every season (HK-04 2.1).
- Fourteen Ask B figures (each day's hours and charge): one device (B1) carried all fourteen, and cracked it lifted the
  pair to about 42; the ask keeps each day's hours and one week's charge (eight figures), pair 40 with B1 cracked.
- The night audit computed from the extract's bookings only: the first nights of January 2022 lacked the guests who
  arrived in December 2021; the audit now counts every stay, and the check that it equals the extract starts on 9 January.
