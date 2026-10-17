# task159: the Vellmouth Transit Commission's spring 2027 platform conductor pick (architecture 1)

Private, never ships. A new build (wave 5), numbered from seed FC30. The seed was read at its header and Situation only
(`status.py task159`). Its world (a city transit agency posting weekday-morning platform conductors where crowding is
forecast), its decision (the weekly shift count filed in the spring roster pick notice) and its quantity (one conductor
per platform per weekday morning whose forecast peak 15-minute accumulation is more than 85 per cent of rated capacity)
are kept. The 85 per cent standard is an estimand and a threshold and is filed as the WHAT. The seed's own mechanism
(counts kept per station complex against posting per platform) is kept as the pack's lower rungs and its Layer 1: the
fare system counts entries per complex, and a platform's arrivals have to be built from the census and the counts. The
pitfall is re-found from how a crowded platform actually fills: a six-car train that reaches the first interchange of a
suburban branch already carrying the branch takes only part of the platform's crowd, and the rest wait for the next.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task159.json`, architecture v1; `guard.py check` WARN (`overuse.org_family`, answered below), one NOTE (`test.same_driver_older`, differentiated against task147 on the card); nearest driver 0.07 (task451 v2) |
| Domain / task type | `urban-regional-science`, task type `forecasting` (serves Forecasting): the deciding quantity is each watch-list platform's peak quarter-hour accumulation forecast for each weekday of a window not yet begun, built from the fare history, the autumn station census and platform counts, and the spring service plan |
| Objective | Forecasting & Predictive Modeling: the spring 2027 pick runs Monday 1 March to Friday 25 June 2027; the as-of date is Monday 11 January 2027 (the fare export to Sunday 10 January); the pick notice closes Wednesday 20 January |
| Shape | `other`: the call (shifts a week) carried by its critical component, each watch-list platform's posted weekdays, and by decoupled asks on rows the call never reads (the arithmetic is written at stage 2) |
| Decision | `quantity_figure`, answer unit `count` (weekday-morning platform conductor shifts a week) |
| Mechanism | gap objective (decisive: a binding limit the proportional carry never checks, the room left on each arriving train) with time (the forward window's weekdays and its eight-car Line 5 trains are a regime the mid-week counts do not show); generators G8 (can the arriving train take them), G16 (the crowd model chosen on the counts it was not fitted to), G13 (the spring pick, its weekdays and its service plan); Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing); `own:platform-queue-behind-trains-arriving-full` |
| Calibration | `physical_verification`: the autumn platform counts, the Monday and Friday counts of the hybrid-day sample the out-of-sample test the crowd model is chosen on |
| Furniture | forum `operations_desk` (Rail Operations' station planning desk files the pick notice), forcing event `shift_or_daily_cycle` (the spring roster pick closes 20 January), organisation family `government_agency`, role family `capacity_planner`, context artifact `published_series` (the ridership dashboard), opening `question-first`, question form `how-many` |
| Spine | the fare system's hourly entries per station complex and payment type (`vtc_fare_entries_hourly_2024-07-01_2027-01-10.parquet`, UTC), with the legacy four-hour register reads before the July 2024 back-office cutover (`afc_register_reads_2022-02-01_2024-06-30.csv`, local time); constructed in the layout of a transit agency's open-data hourly ridership export |
| Deliverables | `spring_2027_platform_conductors.xlsx` (the posting schedule and the ask tables) and `spring_2027_platform_conductors.png` (a chart on an ask, never on the decision quantity) |
| People | drawn with `guard.py names --geo "United States" --seed 159`: Beth Lewis (station planning manager, owner of the crowding standard), Ralph Chambers (service planning, author of the spring service plan), Mary Wheeler (ridership data, owner of the fare export and dashboard), Caleb Rowe (count programme supervisor); the requester is in no file and not in the prompt |
| World | Vellmouth (checked: no real city, county or transit agency of the name; the nearest hits are a novel's imaginary resort, Valmouth, and unrelated European hamlets), a United States city whose transit commission runs a six-line subway; the commission, its stations, people, systems and data are fictional |

**WARN answered.** `overuse.org_family`: a city transit commission is a government agency; no other key is honest, and
the guard's bans (forum, forcing event, organisation family against the last three builds) all pass.

**Same-puzzle and same-driver tests.** Gap objective, pattern none, `quantity_figure`: no build in the last twelve
carries the triple. Gap objective, no pattern, Gate G `binding_constraint`: task147 (multi-night stays blocked by two
sold-out nights), older than the window and differentiated on the card: there a request is lost when any unit of its run
is full, here nobody is lost, the riders a full train cannot take wait for the next one, so the backlog inflates the
heavy days' counted stock and is absent on the light days.

**Abstraction test.** Stripped of nouns: a stock counted at each stop on the heaviest days is mostly the backlog left by
services that arrive with less room than one interval's arrivals, a backlog that builds only while that shortfall
lasts; on lighter days, when the arrivals and the services' own incoming loads both fall, and once a service is
lengthened, no backlog forms and the stock is one interval's arrivals. Against `guard.py nearest`: task451 v2 (a period
total completed for the part not yet observed), task190 v1 (undetected cases a scarce reviewer would meet), task150 (a
cohort-component projection); none maps onto it. Against the capacity builds in this lane, the nearest by shape though
not by text: task156 (a volunteer tier whose capacity shows only where it fell short, the overflow volume each period
graded) and task153 (a per-visit cap summed segment by segment). Here the capacity is known to move with the weekday's
upstream riders and with the consist, it is built from the census of the branch upstream, and the graded quantity is a
backlog that accumulates train by train over the peak and vanishes on the light days.

**Kinship, answered (the builds the brief names, and every transit card).**
- task254 (a hospital shuttle's latest departure from probe segment times read when the vehicle reaches each segment):
  a trip time; nothing here times a trip, and the only vehicle quantity is how much room a train has.
- task134 (net new homes on upzoned lots around transit stations): land development near stations; no rider, train or
  platform is modelled.
- task123 (cycle-read gas bills calendarised by a measured daily shape): splitting a total over periods by a measured
  profile; here no total is split over periods, and the within-morning profile comes from the census as counted.
- task148 (a 911 late shift's Erlang A with censored caller patience): a queue drained by callers who give up; nobody
  here leaves, the backlog is the riders a full train could not take, set by how full each train arrives from upstream,
  and the rival rejected is proportional scaling of a counted crowd, not the patience-free queue.
- task150 (classrooms placed on cohort-component projections, transfers on the sending school's base): every rider
  source here follows one weekday pattern, and nothing is carried on a sender's base.
- task155 (a relief crew placed where call-ins carrying on from a rostered shift would fill the most): a take-up rate
  conditioned on adjacency; here nobody chooses, the train's room decides who boards.
- task468 (a city transit department's delivered frequency, AVL departures linked to routes): an ETL linkage of vehicle
  records; no vehicle record ships here, and the call is a forecast of platform crowds.
- task256 (a transit authority's operator workstation fitted to the operators' body dimensions): shares the employer
  type only.

**WHAT screen (stumping 1.2).** The decisive step forecasts the filed quantity; it settles none of the estimand's five
parts, each filed in the crowding standard: population (the watch-list platforms in its schedule, every one of them
counted last autumn, none of the spring weekdays yet observed), outcome (a platform's accumulation is the number of
people on it as each train arrives, before its doors open; the peak is the highest quarter-hour mean from 07:00 to
09:45), window (the spring 2027 pick's weekdays, Memorial Day out, each weekday forecast on its own), unit (one conductor
per platform per weekday morning; the call is shifts a week) and comparison (more than 85 per cent of the platform's
rated capacity in the register at the pick's start). No shipped sentence says how a crowd responds to fewer riders or to
longer trains.

**Data-native sentence.** Vellmouth's six-car trains on Lines 1, 4 and 5 reach the first interchange of their suburban
branches already carrying the branch, so on Tuesday to Thursday mornings a train takes only part of the crowd at
Sallow Park and Corran Junction and the rest wait for the next; the count sheets record the crowd as each train arrives,
the fare system counts entries per complex, the census counts the flows onto and off every platform, and no record says
who was left behind, so the backlog shows only as crowds several headways' worth of arrivals deep, and as its absence on
the Mondays and Fridays the count programme sampled.

**Sources read, one line each.**
- Seed FC30 header and Situation (`status.py task159`): the world, the 85 per cent standard per platform, the pick dates
  and the pack's file kinds; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: the forecasting drivers on file price units, cohorts, censoring,
  conditioned yields, constructed exposures and capacity residuals; none forecasts a backlog behind batch service whose
  room is set upstream.
- `two-layer-task-design.md`: "handling the data's real structure" (the counted crowd is a queue) and "validating a
  forecast properly (testing it only on data it was not built on)" (the hybrid-day counts) frame the decisive step.
- `layer2-rigor-patterns.md`, urban and regional science, forecasting pattern 1 (backtest from the forecast origin):
  learned, not copied; here the counts the crowd model is not fitted to are the test.
- `strategies.md` F3 (the limit the metric never checked): the limit is a train's remaining room, shared by every rider
  on the platform and moved by the riders upstream, never a per-candidate cap.
- `guide-to-prompt/references/examples.md` 1 (task133, the divisor no sentence names): the stump is a step a careful
  analyst takes by default, here carrying a counted crowd in proportion to the complex's entries.

## Default path

Design targets from the prototype (`b159/proto/roster.py` in the scratchpad); fixed from `generator/calc.py` at stage 2.

1. Read the crowding standard: each watch-list platform is staffed on each weekday morning whose forecast peak
   quarter-hour accumulation is more than 85 per cent of its rated capacity; the forecast is each weekday of the pick.
2. Take each platform's peak quarter-hour accumulation from its autumn mid-week count days.
3. Take each complex's weekday index (each weekday's morning entries over the Tuesday to Thursday mean, autumn 2026) and
   its spring growth (the pick's months against autumn) from the fare export.
4. Carry each platform's mid-week peak to each spring weekday by its complex's index and growth; staff the
   platform-weekdays above 85 per cent of rated capacity and count them.

Ends on: about 51 shifts a week (design target).

Golden: about 42 shifts a week (design target).

## Stump sentence

A competent solver carries each watch-list platform's mid-week counted peak quarter-hour to each spring weekday in
proportion to its complex's morning entries and files about 51 shifts a week, posting Monday and Friday conductors at
Sallow Park's Line 1 and Line 4 platforms and keeping Corran Junction's Line 5 platform staffed every weekday; the step
that lands it there is treating a mid-week crowd behind full trains as proportional to arrivals, when on Mondays,
Fridays and eight-car Line 5 trains every train takes everyone and the pick needs about 42.

## Three rules

- **Task type:** `urban-regional-science` / `forecasting`, which serves Forecasting: the deciding object is each
  watch-list platform's forecast peak quarter-hour accumulation for each weekday of the spring 2027 pick, a window not
  begun at the as-of date, its crowd model chosen on counts it was not fitted to.
- **Domain test:** the quantity that decides the call is each platform's forecast peak quarter-hour accumulation by
  weekday, built the way transit capacity analysis builds platform loading: the arrivals over each headway against the
  room each arriving train still has, the room set by the riders the train already carries from its branch, with the
  riders a full train leaves behind waiting for the next; replacing it with a generic summary (the counted crowd scaled
  by entries) moves the call.
- **Swap:** "how many afternoon clinic shifts the spring rota funds when a waiting room is staffed above 85 per cent of
  its seats" reads as a staffing count, but nothing in a clinic sets how many waiting patients an appointment slot can
  take by how full it arrives from upstream, or lengthens a slot when the consist changes; the backlog behind full
  trains has no counterpart.
- **Layer 1:** each item is how the commission's own systems record the morning and none is placed to be caught (each
  asserted neutral at stage 3, `checks.py` R2): the fare system's two export layouts across the July 2024 back-office
  cutover (legacy four-hour register reads in local time, then hourly entries per payment type in UTC), local time
  against UTC across the 1 November 2026 clock change, complex ids in the export against complex names and platform
  labels on the count sheets, the dashboard's preliminary and revised months, the count contractor's sheet per platform
  and day with large crowds estimated in tens, the census tables by element, counted arrivals against the timetable.
- **Layer 2:** `allocation_constraints`: the platform's crowd modelled as a backlog behind trains of limited room, the
  room built from the branch's own census, against the proportional carry and the one-headway crowd, the proportional
  carry rejected out of sample on the hybrid-day Monday and Friday counts and the one-headway crowd on the mid-week
  counts.
- **Decisive step:** treating the mid-week crowds at the first-interchange inbound platforms as queues of riders left
  behind by trains that arrive carrying their branch, so that the Monday, Friday and eight-car Line 5 crowds are a
  headway's arrivals rather than the mid-week crowd scaled by entries.
- **Not semantics:** no field, code or note says anyone was left behind: the count sheets record the people on the
  platform as each train arrives, the census the flows onto and off it, the fare export entries per complex; reading
  every column right still scales the counted crowd by the complex's entries and posts the Monday and Friday shifts.
- **Not rule application:** the standard files the measure, the threshold, the window and the posting unit; no filed
  rule says how a crowd responds to fewer riders or longer trains, so executing every stated rule leaves the crowd model
  open, and the natural proportional carry files the default path's figure.
- **Analyst test:** a strong analyst who stitches the two fare-export layouts, maps the census and the counts onto
  platforms, reads the standard correctly and carries each platform's mid-week counted peak to each spring weekday by
  its complex's morning entries files about 51 shifts a week; one who builds each crowd from one headway's arrivals
  files about 36; only the backlog behind full trains, against the room each train brings from its branch, files about
  42.
- **Estimand:** the platform crowding standard (`platform_crowding_standard.pdf`) fixes the population (the watch-list
  platforms in its schedule), the outcome (the people on the platform as each train arrives, the peak the highest
  quarter-hour mean from 07:00 to 09:45), the window (each weekday of the spring 2027 pick, Memorial Day out), the unit
  (one conductor per platform per weekday morning, shifts a week) and the comparison (more than 85 per cent of the rated
  capacity in the register at the pick's start).
- **No decoy:** nothing is planted to be caught: the counts, the census and the entries are what each system records, no
  memo or thread argues for any count, the hybrid-day sample is the count programme's own choice of last spring's top
  platforms, and no stakeholder figure is wrong so the task can overturn it.
- **No certified replay:** the method is not hidden and recovered by reproducing certified figures: nothing certifies a
  crowd forecast, and the hybrid-day counts are raw observations a forecast is tested against.
- **Lesson:** a crowd counted where trains arrive full is a backlog, not a multiple of the arrivals; forecast it from the
  arrivals over each headway against the room each train still has, carry the backlog, and test the model on days when
  the trains have room; no build on file teaches platform loading behind full trains.

## Tried and rejected

- Weekday patterns by rider source (transfers on the feeding line's week, street entries on the complex's): rejected at
  the draw before any card was filed, because its kernel (an inflow carried on its sender's driver, not the receiver's)
  is task150's.
- A train-load file pinning each train's room: rejected at the draw; it would hand over platform boardings on every
  uncrowded day and break the seed's complex-level premise; the room is built from the census of the branch upstream.
- Trains' room assumed constant across weekdays when only mid-week rooms are inferable: rejected at the draw; the
  Monday verdicts then turn on an assumption the data cannot settle (a Gate C fork), so the room is pinned from the
  branch census and the weekday entries.
