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
| Shape | `other`: the call (shifts a week) with its weekday counts and the posting schedule, then two decoupled asks on the watch-list complexes and a chart. Criteria: the call 1, the five weekday counts 5, the posting sets 3 (the platforms posted every weekday, those posted Tuesday to Thursday, Corran Junction's Line 5 not posted), Ask A 14 (each complex's escalator flow down and up), Ask B 7 (each complex's elevator-hours), the chart 3: 33 |
| Decision | `quantity_figure`, answer unit `count` (weekday-morning platform conductor shifts a week) |
| Mechanism | gap objective (decisive: a binding limit the proportional carry never checks, the room left on each arriving train) with time (the forward window's weekdays and its eight-car Line 5 trains are a regime the mid-week counts do not show); generators G8 (can the arriving train take them), G16 (the crowd model chosen on the counts it was not fitted to), G13 (the spring pick, its weekdays and its service plan); Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing); `own:platform-queue-behind-trains-arriving-full` |
| Calibration | `physical_verification`: the autumn platform counts, the Monday and Friday counts of the hybrid-day sample the out-of-sample test the crowd model is chosen on |
| Furniture | forum `operations_desk` (Rail Operations' station planning desk files the pick notice), forcing event `shift_or_daily_cycle` (the spring roster pick closes 20 January), organisation family `government_agency`, role family `capacity_planner`, context artifact `register` (the platform capacity register the call reads; re-keyed at stage 2 from `published_series` when the ridership dashboard became a distractor, `guard.py check` re-run clean but for the answered WARN), opening `question-first`, question form `how-many` |
| Spine | the fare back office's hourly entries per station complex and payment type (`vtc_fare_entries_hourly_2024-06-03_2027-01-10.parquet`, UTC, 761,596 rows, from the June 2024 parallel run), beside the legacy four-hour register reads to the July 2024 cutover (`afc_register_reads_2022-02-01_2024-06-30.csv`, local time, a distractor); constructed in the layout of a transit agency's open-data hourly ridership export |
| Deliverables | `spring_2027_platform_conductors.xlsx` (the posting schedule, the weekday counts and the ask tables) and `platform_escalators_am_peak.png` (Ask A's figures charted, never the decision quantity) |
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

Every figure below is built by `generator/calc.py` from the shipped pack and asserted in `generator/checks.py`.

1. Read the crowding standard: a conductor is posted on a watch-list platform on each weekday whose forecast morning
   peak (the highest quarter-hour mean of the people on the platform as each train arrives, 07:00 to 09:45) is more
   than 85 per cent of its rated capacity on 1 March 2027, forecast for an average Monday to Friday of the pick.
2. Take each platform's morning peak on its autumn 2026 mid-week count days (`platform_counts_autumn_2026.xlsx`) and
   average the two mornings.
3. From the fare export (UTC to local), take each complex's weekday index (06:00 to 09:59 entries by weekday over the
   autumn pick's weekdays, against the Tuesday-to-Thursday mean) and the spring-over-autumn ratio (spring 2026 over
   autumn 2025).
4. Carry each platform's mid-week peak to each spring weekday by its complex's index and the ratio; post the
   platform-weekdays over 85 per cent of capacity and count them.

Ends on: 35 shifts a week.

Golden: 26 shifts a week.

## Stump sentence

A competent solver carries each watch-list platform's mid-week counted peak to each spring weekday in proportion to its
complex's morning entries and files 35 shifts a week, posting Monday and Friday conductors on Sallow Park's Line 1 and
Line 4 southbound platforms and keeping Corran Junction's Line 5 westbound platform posted every weekday; the step that
lands it there is treating a mid-week crowd behind full trains as proportional to arrivals, when on Mondays, Fridays and
eight-car Line 5 trains every train takes everyone and the pick needs 26.

## Three rules

- **Task type:** `urban-regional-science` / `forecasting`, which serves Forecasting: the deciding object is each
  watch-list platform's forecast morning peak for each weekday of the spring 2027 pick, a window not begun at the as-of
  date, its crowd model chosen on counts it was not fitted to.
- **Domain test:** the quantity that decides the call is each platform's forecast peak quarter-hour accumulation by
  weekday, built the way transit capacity analysis builds platform loading: the arrivals over each headway against the
  room each arriving train still has, the room set by the riders the train already carries from its branch, with the
  riders a full train leaves behind waiting for the next; replacing it with a generic summary (the counted crowd scaled
  by entries) moves the call by nine shifts.
- **Swap:** "how many afternoon clinic shifts the spring rota funds when a waiting room is staffed above 85 per cent of
  its seats" reads as a staffing count, but nothing in a clinic sets how many waiting patients an appointment slot can
  take by how full it arrives from upstream, or lengthens a slot when the consist changes; the backlog behind full
  trains has no counterpart.
- **Layer 1:** each item is how the commission's own systems record the morning and none is placed to be caught, each
  asserted neutral in `checks.py` (R2, FAMILY, SF rows): the fare back office's hourly export in UTC across the 1
  November 2026 clock change, with federal holidays and the weekday-timetable holidays in it; complex ids in the export
  against complex names in the census and the count sheets; the census by platform access and passage, quarter-hours
  labelled by their start, island platforms counted whole with the two directions' riders together; the count
  contractor's sheets by complex, island counts noted by train direction, crowds of about 200 or more estimated in tens,
  timetable times against counted arrivals; the capacity register's effective-dated ratings (Ferrier Square's Line 4
  southbound re-rated while a stair is rebuilt); the June 2024 parallel run of the back office beside the legacy
  four-hour register reads, with Kennet Street a station of its own before March 2024, and the dashboard's rounded,
  preliminary month (both files distractors).
- **Layer 2:** `allocation_constraints`: the platform's crowd modelled as a backlog behind trains of limited room, the
  room built from the branch's own census flows on each weekday, against the proportional carry and the one-headway
  crowd; the proportional carry is rejected out of sample on the hybrid-day Monday and Friday counts and the one-headway
  crowd on the mid-week counts.
- **Decisive step:** treating the mid-week crowds at the first-interchange inbound platforms as backlogs of riders left
  behind by trains that arrive carrying their branch, so that the Monday, Friday and eight-car Line 5 crowds are a
  headway's arrivals rather than the mid-week crowd scaled by entries.
- **Not semantics:** no field, code or note says anyone was left behind: the count sheets record the people on the
  platform as each train arrives, the census the flows onto and off it, the fare export entries per complex; reading
  every column right still scales the counted crowd by the complex's entries and posts the Monday and Friday shifts.
- **Not rule application:** the standard files the measure, the threshold, the window and the posting unit; no filed
  rule says how a crowd responds to fewer riders or longer trains, so executing every stated rule leaves the crowd model
  open, and the natural proportional carry files the default path's figure.
- **Analyst test:** a strong analyst who converts the export to local time, maps the census and the counts onto
  platforms, reads the standard correctly and carries each platform's mid-week counted peak to each spring weekday by its
  complex's morning entries files 35 shifts a week; one who builds each crowd from one headway's arrivals files 20; only
  the backlog behind full trains, against the room each train brings from its branch on each weekday, files 26.
- **Estimand:** the platform crowding standard (`platform_crowding_standard_rev4.pdf`) fixes the population (the
  platforms in its schedule), the outcome (the people on the platform as each train arrives, the peak the highest
  quarter-hour mean among the quarter-hours starting 07:00 to 09:30), the window (an average Monday to Friday of the
  spring 2027 pick, every weekday the weekday timetable runs), the unit (one conductor per platform per weekday morning,
  a posting one shift a week) and the comparison (more than 85 per cent of the rated capacity in the register on 1 March
  2027).
- **No decoy:** nothing is planted to be caught: the counts, the census and the entries are what each system records,
  no memo or thread argues for any count, the hybrid-day sample is the count programme's own choice of each complex's
  top platform the year before, and no stakeholder figure is wrong so the task can overturn it.
- **No certified replay:** the method is not hidden and recovered by reproducing certified figures: nothing certifies a
  crowd forecast, and the hybrid-day counts are raw observations a forecast is tested against.
- **Lesson:** a crowd counted where trains arrive full is a backlog, not a multiple of the arrivals; forecast it from the
  arrivals over each headway against the room each train still has, carry the backlog, and test the model on days when
  the trains have room; no build on file teaches platform loading behind full trains.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the mid-week counted peaks carried to each spring weekday by the complex's entries (35) | the standard asks for a forecast by weekday, which invites carrying the counts | the count sheets and the export's weekdays | yes, the default | the hybrid-day Monday and Friday counts at COR-5W sit 1.0 to 1.2 times capacity under it, for an analyst who back-tests | no | yes, one index | readable |
| R0b the same with the hybrid-day counts read as they are where they exist (33) | no | the count sheets' Mondays and Fridays | yes, use the observation | nothing scores Sallow Park's Mondays, which were not counted | no | yes | readable |
| R1 each crowd one headway's arrivals from the census, every train taking everyone (20) | no | the census flows and the timetable | yes, the textbook platform load | the mid-week counts sit 1.0 to 1.7 times capacity above it at SAL-1S, SAL-4S and COR-5W | no | yes, flow times headway | readable |
| R2a a backlog model on the autumn timetable, Line 5 at six cars in the spring (29) | no | the timetable's cars column | a half-step | the spring service plan and the SPR27 timetable run Line 5 at eight cars | no | no | readable |
| R2b a backlog model whose trains keep their mid-week room on every weekday (28) | no | no | a half-step | the hybrid-day counts at COR-5W show no backlog on the Monday and Friday | no | no | readable |
| R3 (decisive) the backlog behind trains whose room is built from the branch's own riders on each weekday, run on the spring timetable (26) | no shipped sentence names a backlog, a train's room, riders left behind or how a crowd responds to fewer riders or longer trains | no column holds boardings, loads, room or riders left behind; the census counts flows, the sheets the people waiting | no: the reflexes scale the counts, use the observation, or take a headway's arrivals | the hybrid-day counts reject the carry at COR-5W on the autumn timetable; nothing scores a spring forecast, Sallow Park's Mondays or the eight-car Line 5 | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a train-by-train run of every branch | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs; every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "shifts a week" | one shift per posted platform-weekday | conductors (people) or hours | same count | the standard ("One posting is one weekday-morning shift a week, 06:45 to 10:00, for the length of the pick") |
| SF2 | "more than 85 per cent" | strictly greater | at least | same call (no platform-weekday within 0.07 of the line, asserted) | the standard; same call, asserted |
| SF3 | rated capacity | the register's rating in force on 1 March 2027 | the rating in force at the pull (Ferrier Square's Line 4 southbound at 300) | same call, asserted | the standard ("in the platform capacity register on the first day of the pick") |
| SF4 | the morning peak's window | quarter-hours starting 07:00 to 09:30 | a sliding window; quarter-hours to 09:45 inclusive of a 09:45 start | same call | the standard ("among the quarter-hours starting at 07:00, 07:15 and so on to 09:30, local time") |
| SF5 | an island platform's accumulation | everyone on the island | the arriving direction's riders only | Monday and Friday posts at the four islands fall away | the standard ("On an island platform it is everyone on the island, whichever train they are waiting for") |
| SF6 | "an average Monday ... of the pick" | the pick's average riding on that weekday | the month-by-month level, March to June | same call (March and June levels asserted) | the standard; same call, asserted |
| SF7 | clock | local time | UTC | same call | the standard ("local time"); the count sheets' method ("All times are local") |
| SF8 | the pick's weekdays | every weekday the weekday timetable runs (Memorial Day out, Juneteenth in) | calendar weekdays | same call (an average weekday) | the standard and the spring service plan |
| SF9 | "mean accumulation over the trains arriving in a quarter-hour" | the mean over that quarter's trains | the largest train's crowd | same call at the backlog platforms (asserted) | the standard |
| SF10 | accumulation | the people on the platform as a train arrives, before its doors open | the people left after the doors close | another quantity | the standard ("as a train arrives, before its doors open") |
| SF11 | the fare export's morning for the weekday index | 06:00 to 09:59 local | 07:00 to 09:59; 05:00 to 10:59 | same call, asserted | same call, asserted |
| SF12 | weekdays in the index | the autumn pick's weekdays, federal holidays out | holidays kept | same call, asserted | same call, asserted |

## Ladder

Built figures from `generator/calc.py` on the shipped pack, every row asserted in `generator/checks.py` (LADDER, OOS,
FAMILY). The graded quantity is a count of platform-weekdays; each rung names a different count.

| Rung | Construction | Shifts a week | Dies to |
|---|---|---|---|
| R0 default | mid-week counted peaks carried by the weekday index and the spring ratio | 35 (7 each weekday) | the hybrid-day counts at COR-5W (Monday 0.56 and Friday 0.52 of capacity counted, 1.73 and 1.58 carried) |
| R0b | R0 with the hybrid-day counts read as they are where they exist | 33 | Sallow Park was not counted on a Monday or Friday; the eight-car Line 5 |
| R0c | R0 with COR-5W scaled by six cars over eight | 35 | the backlog does not scale with the train: at eight cars it clears |
| R0d | the mid-week counts as every spring weekday's | 35 | the weekday index |
| R1 | one headway's arrivals from the census, every train taking everyone | 20 | the mid-week counts at SAL-1S, SAL-4S, COR-5W (2.17, 2.63, 2.09 of capacity counted against at most 0.71 under R1) |
| R2a | the backlog model with Line 5 at six cars in the spring | 29 | the spring timetable and service plan |
| R2b | the backlog model, trains keeping their mid-week room every weekday | 28 | the branch's own Monday and Friday riders; COR-5W's hybrid days |
| R2c | the backlog model at the fleet register's planning load (110 a car) | 33 | the hybrid-day counts (it builds backlogs where none was counted) |
| R2d | each complex's forecast against the sum of its watch-list platforms' capacities | 46 | the standard posts platforms |
| R2e | each complex's mean morning hour split equally over its platforms | 13 | the census's platform flows |
| R2f | R0 or the golden averaged over the week | 35 or 30 | the standard forecasts each weekday |
| R2g | the one-headway model scaled by one network factor fitted to the mid-week counts | 36 | the hybrid days |
| R2h | the one-headway model scaled platform by platform to its mid-week counts | 35 | the hybrid days |
| R3 decisive | the backlog behind trains of the spring timetable, each taking at most cars times 150 less the riders it brings from upstream plus those getting off, the branch's riders on each weekday | 26 (4, 6, 6, 6, 4) | golden |

**Position and margins.** The golden is the lowest count of every backlog-free carry and above every one-headway
count; the nearest rivals miss by two (R2b, 28) and three (R2a, 29) shifts, the default path by nine. Each platform-day
sits at least 0.10 of capacity from the line in the golden and 0.075 across its family.

**Convergence (C1, asserted).** Thirteen constructions of the golden file 26 with the same posts: island riders split
30/70, 50/50 or 70/30 between directions; the spring ratio from 2025, 2026, their mean, flat, 0.985 or 1.03; the weekday
index on 07:00 to 09:59 or 05:00 to 10:59; the trains' room scaled by 0.80, 0.85 or 0.90 (the back-cast that matches
the mid-week counts best sits at about 0.85). On the clean truth the golden holds from 6 per cent under to 6 per cent
over the forecast level, and one sigma of the spring level (the two years' ratios apart plus 2 per cent for the census
normalisation) leaves it unchanged.

**Worth on the graded quantity.** Seeing the backlog at Sallow Park is worth four shifts (its Monday and Friday posts
fall away); carrying the backlog to the eight-car Line 5 is worth five more (COR-5W's posts fall away).

**Out of sample.** On the autumn timetable the backlog model puts COR-5W's hybrid Monday and Friday at 0.58 and 0.53 of
capacity against 0.56 and 0.52 counted, and errs 0.060 on average over the hybrid-day sample against the carry's 0.234.

**Strength.** P(one strong solver lands) about 0.15: it has to read the Sallow Park and Corran Junction crowds of about
twice capacity as riders left behind rather than riders arriving, build the trains' room from the branch census on each
weekday, and carry the result both to Sallow Park's uncounted Mondays and Fridays and to the eight-car Line 5. P(both
land) about 0.03 if independent, under 0.1 with any plausible correlation. The seed was fixed by rule (the task number,
then the as-of month and day: 1590111) before any data was generated and is never searched.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the platforms in the standard's schedule | filed (the standard's schedule) |
| 2 | Unit of account | the platform-weekday; a posting one shift a week | filed (the standard); SF1 |
| 3 | Attribution window | an average weekday of the spring 2027 pick | filed (the standard and the spring plan); SF6, SF8 |
| 4 | As-of dating | the pull of 11 January 2027; the export to the 10 January service day | the data dictionary; no record after the pull (asserted) |
| 5 | Version basis | the capacity rating in force on 1 March 2027 | filed (the standard); SF3 |
| 6 | Denominator | rated capacity | filed (the standard and the register) |
| 7 | Weighting | none: counts of platform-weekdays | n/a |
| 8 | Window length | the autumn pick for the weekday index, a year for the spring ratio | C1 across index windows and ratio years (asserted) |
| 9 | Boundary inclusivity | more than 85 per cent | filed; nothing within 0.07 of the line (SF2, asserted) |
| 10 | Rounding path | none before the count | n/a |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | the spring pick unobserved at the as-of | the decisive forecast itself; nothing in the pack covers it |
| 13 | Order of operations | the weekday and spring factors applied to the flows before the trains run | C1 (the factors multiply the flows; asserted across variants) |
| 14 | Row order | sums and train order by departure | C1 |
| 15 | Duplicate resolution | none on the call's rows | the realism sweep (no repeated complex-day or census block) |
| 16 | Identity normalisation | complex ids to names through complex_reference.csv | the reference table; the census carries both |
| 17 | Netting against gross | riders getting off free room on arriving trains | the decisive model; no netting rule filed |
| 18 | Dimensional units | people, people a minute, cars at 150 people | the fleet register; R2c rules out the planning load |
| 19 | Code and status semantics | to platform, from platform, passage; E estimated | the census notes and the count method (Layer 1, neutral) |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the standard applies from the autumn 2026 pick | filed (revision 4 in force from 8 September 2026) |
| 22 | Forward window contents | the spring pick's timetable and consists | the SPR27 timetable and the spring service plan ship |

## Literal reader

Executing the prompt and the standard word for word gives the count of watch-list platform-weekdays whose forecast
morning peak (the highest quarter-hour mean of the people on the platform as trains arrive, quarter-hours starting 07:00
to 09:30 local) for an average weekday of the spring 2027 pick is more than 85 per cent of the rating in force on 1 March
2027; no shipped sentence says how to forecast a crowd, so a literal reader must model it, the easy method on the same
literal estimand (carrying the mid-week counts by entries) files 35, and the fork table leaves no reading under which a
rung is the golden.

## Oracles

- The hybrid-day counts (COR-5W, GAR-2, HES-3, FER-5W, ALB-6, QUA-6 on a Monday and a Friday): autumn observations on the
  autumn timetable; on the wrong path they confirm nothing (the carry misses COR-5W's by more than capacity), and they tie
  as well with reading them as they are (R0b, 33) as with the backlog model, so they do not tie only under the golden.
  No spring observation ships.
- The fare export and the census: inputs every method reads alike; neither ranks a platform.
- The ridership dashboard (a distractor): average weekday entries by complex and month, consistent with the export on
  its own definition; it ranks nothing on the decision.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the station census, the platform counts, the fare export's `entries` column,
the weekday timetables, the fleet register, the platform capacity register, the complex reference, the crowding
standard and the two service plans. Device and hazard rows in it: 0 (asserted, SEPARATION: the golden reads none of the
ask files and the asks read none of the call's records; the asks' devices sit in the inventory's direction and speed
columns, the work orders' times and the monitoring's modes).

**Ask A. For each watch-list complex, the people a minute its platform escalators can carry at their rated flows down to
the platforms and up from them between 07:00 and 09:30 on the autumn 2026 pick's weekdays** (14 figures, whole people a
minute).
- H18 home: a measure every candidate complex carries that the call does not turn on, how fast the morning's riders
  reach and leave its platforms, read beside the posting schedule for the conductors' post orders.
- Basis (filed in the station planning manual, chapter 5, the owner's voice): "An escalator's rated flow depends on its
  step width: 40 people a minute for a 600 mm step, 60 for an 800 mm step and 80 for a 1,000 mm step at 0.5 metres a
  second, and in proportion to its speed at other speeds. An escalator carries its rated flow in the direction it is set
  to run." A rated flow is a capacity, so an escalator stopped by a fault on a morning keeps its figure.
- Primary A1 (D2, an attribute at the wrong vintage): the engineering inventory records each escalator's running
  direction as surveyed at midday; in the morning peak station operations turn the pair at a boarding platform both
  down and at an alighting platform both up; the escalator controllers' log carries every direction change. Fair: the
  log gives every escalator one direction from 07:00 to 09:30 on every autumn weekday (asserted). Silent: the inventory's
  direction is complete and valid, and no shipped sentence mentions a morning reversal.
- Primary A2 (D2, a label stored before a silent switch): the inventory keeps each escalator's design speed (0.5 m/s);
  the Lines 1 to 4 escalators were slowed to 0.45 m/s in the 2019 step-chain programme, a setting only the maintenance
  system's asset register holds. Fair: the register gives every unit's controller speed. Silent: the inventory's speed
  is a valid design value, and nothing narrates the slowdown.
- Hazards: HA1 step widths in inches on Lines 1 to 4 and millimetres on Lines 5 and 6 (the dictionary says so); HA2
  street escalators in the same inventory (the ask counts platform escalators); HA3 UTC in the log.
- Stops (built and asserted, every figure missed by each): the inventory's directions and speeds (S1: Garnett Street
  120 down, 120 up against the golden 72, 144); the log's directions with the design speed (S2: 80, 160); the
  inventory's directions with the controllers' speeds (S3: 108, 108); the golden.
- Span: the station elements inventory, the escalator controller log, the escalator asset register, the station
  planning manual, the data dictionary (5 files).
- Realism: transit systems reverse escalators by time of day to the main flow, and an engineering inventory keeps the
  surveyed direction and the design speed while the maintenance system keeps the controller settings.

**Ask B. For each watch-list complex, the elevator-hours its elevators were out of service between 07:00 and 09:45 on
the autumn 2026 pick's weekday mornings** (7 figures, one decimal).
- H18 home: a measure every candidate complex carries that the call does not turn on, how often its riders who need
  the elevators met one out in the morning peak, read beside the posting for the conductors' post orders.
- Basis (filed in the station planning manual, chapter 5): "An elevator is out of service whenever it is not in normal
  passenger service: from the moment it stops or is taken out of service to the moment it is back in normal passenger
  service." The window and the pick's weekdays are the prompt's and the autumn service plan's.
- Primary B1 (D8, an anchor on the record, not the event): the control centre opens a work order when the station
  reports the fault, so its out-of-service time runs after the car stopped; the remote monitoring logs the stop.
  Fair: the monitoring gives each fault's stop and its return to normal service. Silent: every work order is complete
  and valid, its out-of-service time earlier than its return.
- Primary B2 (D4, a reporter or channel absent): the remote monitoring receives the controller's passenger-service
  modes (normal, fault, independent, shutdown); planned maintenance runs the car on inspection operation, which the
  monitoring does not receive, so planned maintenance is only in the work orders (type PM, "the car on inspection
  operation for the work" in the dictionary). Fair: every PM work order carries its own start and end, and inspection
  operation is not normal passenger service. Silent: the monitoring log is complete for the modes it receives.
- Hazards: HB1 times in UTC across the 1 November clock change (the dictionary says UTC); HB2 outages running over
  more than one morning (the windows clip them); HB3 Columbus Day and Veterans Day run the weekday timetable (in), the
  Thanksgiving days the holiday timetable (out).
- Stops (built and asserted): the work orders alone (every figure missed by 0.7 to 2.0 hours: Garnett Street 27.2
  against the golden 27.9); the monitoring alone (missed by 1.2 to 7.0 hours: Garnett Street 21.0); the golden.
- Span: the elevator work orders, the elevator monitoring, the station planning manual, the autumn service plan, the
  data dictionary (5 files).
- Realism: maintenance systems stamp a work order when it is opened, and remote monitoring vendors report the
  passenger-service modes rather than the mechanic's inspection operation.

**The chart** (`platform_escalators_am_peak.png`): Ask A's figures, down and up for each complex, each bar labelled;
graded on its content (Ask A's figures) and its parts (both directions for every complex, labelled; the title).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| Units (inches and millimetres for escalator steps) | A | A: a step read in the wrong unit lands in another flow band |
| Clocks (UTC in the controller log, the work orders and the monitoring; local windows) | A, B | B: November and December windows an hour out under a fixed offset |
| Scope (street against platform escalators; weekday-timetable holidays) | A, B | A: street escalators add to a complex's figures; B: two mornings in or out |

**Referee.** The controllers' log and the asset register (Ask A), the monitoring and the PM work orders (Ask B); none
hands over a level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, seven complexes' flows down and up (14) | the manual's rated flows on the inventory's escalators, steps converted to millimetres, platform escalators only | A1 the morning reversals and A2 the slowed controllers, each alone enough | miss |
| B, seven complexes' elevator-hours (7) | the work orders' out-of-service times clipped to 07:00 to 09:45 local on the pick's weekdays | B1 the report lag and B2 the maintenance the monitoring does not report, each alone enough | miss |

Measured by: generator/cracker.py (run on the cut pack: each response scored on a rubric modelled on the generated
one, the call and its components 35, the instructions 7, the asks 58 over every ask figure and the chart's parts).

**Mirror sheet.** The mirror stops at R0 (35 shifts) and meets the same devices; it keeps the chart's two parts and no
Ask A or B figure. Cracking any one device (A1, A2 or B1) leaves its ask missed, since each ask has a second device.

Mirror leakage: 8.3 per cent of ask weight (the chart's two parts).

Pair ceiling: 29.3 (the cracker 46.8, the mirror 11.8; with the most obvious device cracked 29.3; both top responses on
the call with no device cracked 46.8). Rerun from the generated rubric at stage 4.

## Surface screen

`guard.py surface task159` promotes one pair, at the card level only: task147 against task159 (gap objective, pattern
G8, Gate G `binding_constraint`, the same-driver signature), differentiated on the card at the draw: there a multi-night
request is lost when any night of its run is sold out; here nobody is lost, the riders a full train cannot take wait
for the next one, so the backlog inflates the heavy days' counted crowds and is absent on the light days. No hard tell
(no shared file name, schema, invented name or same-seed table). `guard.py heart` WARN (`overuse.org_family`, answered
at the draw), nearest driver 0.07 (task451 v2). The persona sweep reads "Line Early" off the service plans' headway
table, where the column heading "Early" follows the row heading "Line"; it is not a person.

## Leak sweep

`leak.py task159 --asof 2027-01-11` returns REVIEW (no LEAK); every line answered:
- Sweep 3, the crowding standard names the watch-list platforms beside the call's vocabulary: the schedule is the
  population the call executes and the standard is the rule it runs on; it carries no count, forecast or posting.
- Sweep 4, stump-paragraph terms in the standard and the service plans (counts, trains, forecast, capacity, Monday,
  Friday, timetable, headway): each document's own subject (the measure and the count programme; the weekday service
  and its consists); none names a backlog, a train's room, riders left behind or how to carry a crowd (asserted in
  `checks.py`, R3c).
- Sweep 6, files naming the watch-list complexes beside numbers (the legacy reads, the elevator work orders, the
  capacity register, the dashboard, the census, the inventory): records per complex of entries, outages, ratings,
  flows and elements; none ranks the platforms on the posting question.
- Sweep 9, dates after the as-of: the capacity register's restored rating for Ferrier Square's Line 4 southbound from
  2027-02-13 (the works end 2027-02-12) and the change register's spring entries from 2027-03-01, forward-looking
  records allowed by file (`reduce-house-fixes` H16).
- Sweep 10: no writer signature or out-of-band stamp; the fare export's Parquet footer carries Arrow's own writer
  string, as any export from that toolchain does.

## Build record

Stage 3, 2026-10-17. `build.py`: checks 97 run, 0 failed (the three-rules block R1 to R3c on the generator's clean
truth, the R2 mess-neutrality variants, every SF row SF1 to SF12, the ladder's fifteen rungs and rivals, the
out-of-sample test, thirteen family constructions and the one-sigma corridor, both asks with their routes and edges,
the separation line, the input gates, the distractors' deletion test, the realism sweep and the dates allow-list);
`verify.py` (pandas, no generator import) 6 passed, 0 failed; two consecutive builds byte-identical (target, golden,
figures.json, submission); `figures_check.py` 0 absent (40 figures); `voice-check.py` PASS (860 characters);
`precut.py` exit 0 (50 checks); `leak.py` REVIEW, no LEAK; the H1 audit clean on the pack and the goldens; `guard.py
validate` clean, `heart` WARN (answered), `surface` one card-level pair (above); `generator/cracker.py` pair ceiling
29.3, mirror leakage 8.3 per cent. 20 files in 4 formats (parquet, csv, xlsx, pdf), the largest the fare export at
761,596 rows; distractors `afc_register_reads_2022-02-01_2024-06-30.csv` and
`ridership_dashboard_avg_weekday_2025-2026.xlsx` in `metadata.json`. Invented names checked: Vellmouth (no real city
or transit agency), the count contractor Halvorsen Field Counts (no firm of the name in a web search); station names
are ordinary street and place names; the car and escalator builders are real manufacturers named descriptively;
personas from `guard.py names`. The seed was fixed by rule (1590111) before any data was generated and never searched.

## Tried and rejected

- Weekday patterns by rider source (transfers on the feeding line's week, street entries on the complex's): rejected at
  the draw before any card was filed, because its kernel (an inflow carried on its sender's driver, not the receiver's)
  is task150's.
- A train-load file pinning each train's room: rejected at the draw; it would hand over platform boardings on every
  uncrowded day and break the seed's complex-level premise; the room is built from the census of the branch upstream.
- Trains' room assumed constant across weekdays when only mid-week rooms are inferable: rejected at the draw; the
  Monday verdicts then turn on an assumption the data cannot settle (a Gate C fork), so the room is pinned from the
  branch census and the weekday entries.
- Near-threshold platforms off the backlog lines (an island at 0.77 to 0.97 of capacity, posted Tuesday to Thursday):
  dropped at stage 2, because the island counts' noise (the other direction's riders, a delayed train) and the census
  split of island riders by direction moved those platform-days across the line between defensible constructions; the
  ratings were set so every platform off the backlog lines is at least 0.10 from the line.
- A Sallow Park backlog only 4 per cent above its knee on Thursdays: deepened at stage 2 (the branch riders 3 per cent
  up and the mid-week weekdays within a point of each other), so the golden holds from 6 per cent under to 6 per cent
  over the forecast level.
- Revenue protection's evasion survey reconciled to the fare system as an ask: dropped, because every natural device
  sat at one or two complexes and none moved every figure; the census's array counts would have put an ask organ in a
  document the call reads.
- Escalator sizes by nominal width as the second escalator device: dropped, because the manual's "step width" and a
  step-width column in the asset register adjudicate it; the slowed controllers replace it.
- The ask anchored "at 08:00" on the controllers' settings: dropped, because a clock time sends the solver to the log;
  the ask now names the morning peak window.
- Planned maintenance logged in the elevator monitoring: dropped, because with every mode logged the monitoring alone
  answers the ask once found; inspection operation is now reported only in the work orders.

