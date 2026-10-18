# task169 design note: the cycleway to widen before summer 2027

## Draw

- **Slot.** Wave 7, new, Forecasting. Seed `analytical_tasks/01_forecasting/FC40` read for its world, decision and
  quantity only (a city choosing the one corridor to widen from counter data). The seed's year-on-year replay
  convention, its headline-counter ranking and its filed weakest-segment rule are dropped: the estimand is filed
  (which segments make up a cycleway, what a crowded day is, which summers are replayed, the coming summer) and
  the decisive step is a forecasting judgment the records force.
- **Pairing.** Client domain Urban & Regional Science, task type `forecasting` (it serves Forecasting & Predictive
  Modeling). Objective Forecasting & Predictive Modeling: the call is a forecast count of crowded days in a window
  not yet open (1 June to 31 August 2027), pinned by three summers of hourly counts.
- **Card.** `domain` urban-regional-science, `subdomain` forecasting, `objective` forecasting, `shape` other,
  `decision_type` pick_one_of_n, `answer_unit` named_option, `gap` [time, objective], `pattern` [none],
  `generators` [G14, G6, G2], `gate_g` forecasting, `calibration_form` none, `stump_strategy` composition_mix,
  `context_artifact` monitoring_export (the dashboard), `role_family` programme_officer, `forum` committee_or_panel,
  `forcing_event` vote_or_meeting, `org_family` local_government; `stump_class` analytical. People from
  `guard.py names --geo "United Kingdom" --seed 169`: Eleanor Phillips, Conor Reynolds, Judith Hughes, Kevin Hale,
  Adrian Hill.
- **Guard status at the draft.** `guard.py check` on the draft card blocks only on the window: the pairing,
  pattern G14 and org family against task165, the strategy composition_mix against task165 and task268, the
  context artifact monitoring_export against task248. Differentiation lines are on the card for task131, task183,
  task230 (same puzzle older) and task165, task164, task159. The card is held unregistered until those three
  leave the last-three window; nothing was relabelled around a ban.
- **Shape and criteria.** The call (1), its segment (1) and its hours (1); for each of the six volunteer count
  sites the counter's riders and its shortfall (12); for each of the six dashboard counters its 2025 hours
  recording nothing and its stoppages (12); the note (one page, the call stated) and the two files (4): 31.
- **Data-native sentence.** A segment crowds in the one hour its narrowest point carries most riders, and on
  Tolland Bridge that hour is the weekday commuting peak, whose riders grow at a different rate from the bridge's
  daily total and from the leisure riding the hot 2026 summer lifted on the Estuary Path, so the forecast has to
  be made where the capacity binds, with each day's weather held fixed.
- **Nearest builds, and how this differs.** task165 (urban forecasting, gain conditioned on prior coverage: no
  service upgrade here), task164 (a new load's draw at a seasonal peak: no load joins here), task159 (a counted
  stock that is a backlog: these counts are flows), task131 (a treatment's rebound at a design-day peak),
  task183 (parts' failure histories), task230 (coding bias under a looser rule). `guard.py slots` on the driver's
  words named task229, task117, task201, task123, task129, task135, task164, task159, task254; none carries the
  insight that the binding hour's growth differs from the total's and that weather confounds the record's growth.
- **Dead screens read first.** task171, task174 to task177 `## Tried and rejected`: levers of 5 to 20 per cent
  against noise of 1 to 3 per cent (here the lever is a categorical flip: the default path ranks Tolland Road
  fifth, the golden first, margin 1.2x or more in every specification); a coming window differing only in
  unfilled cells (here every summer is complete and the forecast is of a new summer); filter-and-divide on a
  subset already at exposure (screened below, misses); per-unit integer figures magnifying noise (the call is
  categorical); variance-only corrections (screened below, the step moves the point comparison).

## Default path

The pipeline a strong analyst builds from the prompt, the policy and the files' grain, every filed rule applied.

1. Conform the legacy 2024 export (local hours, Ch1 plus Ch2) and the platform's 2025-26 export (UTC, in plus
   out) onto each counted segment's local clock hours through the register, leaving no_data, estimated and blank
   hours out (policy 3.3).
2. Take each counted segment's capacity from its minimum width in the Path Inventory and Table 4.3.
3. Measure each counter's growth as its summer 2026 riders over its summer 2025 riders (the latest change in the
   record; the compound 2024 to 2026 rate gives the same answer).
4. Carry every recorded day of 2024, 2025 and 2026 to 2027 at that growth, count the days any counted segment
   exceeds its capacity in an hour from 06:00 to 22:00, and take the mean over the three summers (policy 3.4).
5. File the cycleway with the most forecast crowded days.

Ends on: Estuary Path, the cycleway CW3

- The default path's forecast crowded days on the pack: Estuary Path 42.7, Market Street 41.0, Wardle Park 39.3,
  Brickfields 23.3, Tolland Road 21.0.

Golden: Tolland Road (CW1), widened at Tolland Bridge, which crowds between 08:00 and 09:00 on weekday mornings.

## Stump sentence

A competent solver replays the three recorded summers at each counter's 2025 to 2026 growth in total riders and
files Estuary Path (CW3), because the hot, dry summer of 2026 lifted the path's leisure riding and that rise is read as
trend, while Tolland Bridge's daily total, half of it flat midday riding, hides how fast the weekday 08:00
commuting hour that crowds it is growing; only each counter's growth at its own hour and day group, with each
day's rain and temperature held fixed, files Tolland Road.

## Three rules

- Task type: forecasting in Urban & Regional Science, which serves Forecasting & Predictive Modeling: a demand
  forecast for a capacity decision on a transport network.
- Domain test: the deciding quantity is each counted segment's forecast number of summer 2027 days on which its
  two-way hourly cycle flow exceeds its design capacity, estimated as a transport planner forecasts cycle demand:
  growth by trip purpose at the hour that binds, with the weather elasticity of riding taken out of the trend.
- Swap: "which ward will be over its bed capacity on the most days next winter" keeps the replay but loses the
  thing that decides it here: a commuting peak growing against declining leisure riding, and a summer's heat and
  rain moving leisure riding far more than commuting; with megawatt-hours for riders the hour-by-purpose growth
  and the weather confound have no counterpart in the same files.
- Layer 1: a counter platform migration (local hours and two channels in 2024, UTC by direction in 2025-26), two
  legacy loggers wired with Ch1 away from the centre, outages flagged no_data or left blank, platform estimates,
  partly lost hours, a replaced Corn Exchange unit under a new id, missing weather days, bank holidays inside the
  summers and events that close or fill paths; each is produced by the council's own systems and listed in the
  Layer 1 inventory with its R2 assertion.
- Layer 2: forecast_uncertainty. The methodological choice that flips the call is the growth model: growth at
  each counter's own hour and day group with each day's rain and temperature held fixed, against the counter's
  growth in total riders carried to every hour; a back-test on summer 2026 rejects the rivals out of sample.
- Decisive step: estimate each counter's growth where its capacity binds, at its own hour and day group, with the
  day's weather in the model, and carry each recorded hour to 2027 at that growth; the commuting hour on Tolland
  Bridge grows 11 to 14 per cent a year once the weather is held, the leisure hours on the Estuary Path fall.
- Not semantics: every field, unit, clock and code read correctly (UTC converted, channels summed, outages left
  out, capacities from the right band) still leaves the default path on Estuary Path; the error is the growth
  model, which no field or definition fixes, and R2 shows no mishandled mess item moves the call.
- Not rule application: policy 3.4 files the replay (each day of three summers at the numbers expected in the
  coming summer) but not how the expected numbers are estimated; executing every filed sentence with the natural
  growth (each counter's total) files Estuary Path, and no shipped sentence says growth differs by hour or that
  weather confounds the record's change.
- Analyst test: a strong analyst who conforms both exports, reads every capacity and rule correctly and replays the
  three summers at each counter's 2025 to 2026 growth in total riders files Estuary Path (CW3); growth by hour
  without weather files Estuary Path too, weather-held daily growth files Estuary Path, and only hour-level growth
  with weather held files Tolland Road.
- Estimand: policy AT-POL-07 (cycleway_widening_allocation_policy_2026.pdf) files the population (each cycleway's
  counted segments, 3.1), the outcome (a crowded day: any clock hour 06:00 to 22:00 local, both directions above
  the Table 4.3 capacity at minimum width, 3.2 and 3.3), the window (1 June to 31 August 2027, 2.2), the unit
  (days, the mean over the replayed summers of 2024, 2025 and 2026, 3.4) and the comparison (the most forecast
  crowded days, 2.1).
- No decoy: nothing is planted: no memo, draft, briefing or stakeholder figure argues Estuary Path; the dashboard
  answers another question (monthly riders at six sites) and the policy's history line only says the 2022 criteria
  were replaced, without naming them; the wrong answer comes from the easy growth model alone.
- No certified replay: no certified or published figure is reproduced to recover the method; the record carries no
  crowded-day count, forecast or growth figure, and the back-test is the analyst's own on the raw counts.
- Lesson: a capacity forecast is made at the cell that binds, and the record's year-on-year change is a mix of
  trip purposes and of the weather the record happened to get; no build on file teaches growth decomposed by the
  binding hour with a weather-confounded record (task165 conditions a gain on prior coverage, task164 a load's
  draw at a peak).

## Readability screen

| Rung | What the solver must see | Test that fires | Verdict |
|---|---|---|---|
| R0 replay the three summers at each counter's growth in total riders | policy 3.4 and the counts | 3 reflex | readable |
| R1 conform clocks, channels and outages | data notes sections 3 and 4 | 1 filed sentence | readable |
| R2 capacities from the minimum width and Table 4.3 | policy 3.2, the guide | 1 filed sentence | readable |
| R3 weather held fixed in a growth fitted on daily totals | the weather file ships | 3 reflex | readable |
| R4 (decisive) growth at each counter's own hour and day group with the day's rain and temperature held fixed | nothing names the hour's growth or the confound; only the records show the commuting peak outgrowing the day and the 2026 heat lifting leisure riding | none of the six fires: no clause, no column or marker, not an opponent default, no control bench, no hygiene finding, not one subtraction | silent |

No confidence level, significance level or test threshold is filed anywhere in the pack (stumping 2.1, test 1):
the 1.0 mm wet-day line is the golden's own modelling choice, and the family agrees without it (rain in
millimetres, any rain, log rain).

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | crowded | any clock hour 06:00 to 22:00 local, both directions, above capacity | daily mean over capacity; one direction | not computed | policy 3.3 quoted |
| SF2 | capacity | Table 4.3 at the minimum width | inclusive or exclusive band edges | same call | no counted width sits on an edge (C1) |
| SF3 | exceed | strictly above | at or above | same call | no forecast hour equals a capacity (C1) |
| SF4 | forecast crowded days | the mean over the three summers | the total over three summers | same call | ranking identical |
| SF5 | counted segments | inventory segments with a counter | every segment | same call | uncounted segments carry no counts |
| SF6 | 06:00 to 22:00 | hours beginning 06:00 to 21:00 | hours beginning 06:00 to 22:00 | same call | asserted identical |
| SF7 | an hour a counter did not record | no_data, estimated and legacy blanks out | estimated read as recorded | same call | asserted |
| SF8 | the numbers expected in the coming summer | growth to the 2027 level by whole years | growth to the same date in 2027 | same call | asserted |
| SF9 | both directions together | Ch1 plus Ch2, in plus out | one channel | same call | two-way sums are direction-free |
| SF10 | the hours it crowds | local clock hours | UTC hours | 07:00 label | policy 3.3 "local time" |
| SF11 | the segment that crowds it | Tolland Bridge, the only Tolland Road segment over capacity | any narrow segment | same call | asserted per summer |
| SF12 | the three most recent summers | 2024, 2025 and 2026 | the latest two | not used | policy 3.4 names them |
| SF13 | the coming summer | 1 June to 31 August 2027 | the 2027 calendar year | not used | policy 2.2 |
| SF14 | equal forecasts | the committee chooses | a tie-break rule | not reached | no tie (policy 2.3) |
| SF15 | the Corn Exchange's units | one site, the unit of record each year | two sites | same call | register: one segment, two units |
| SF16 | each day as an equally likely day | days counted in 92-day summers | shares of days | same call | every summer has 92 days |

Every row is asserted in `generator/checks.py` (labels SF1 to SF16).

## Ladder

| Rung | Construction | Cycleway it files (forecast crowded days, the pack) |
|---|---|---|
| 0 | the latest summer replayed at each counter's 2025-26 total growth | Estuary Path 47.0 (Tolland Road 26.0) |
| 1 | the three summers at each counter's 2025-26 total growth (the default path) | Estuary Path 42.7 (Tolland Road 21.0) |
| 1b | the three summers at each counter's 2024-26 compound growth | Estuary Path 40.0 |
| 1c | each cycleway's dashboard counter growth for all its segments | Market Street 51.3 |
| 1d | one flat rate for every counter, 4 to 18 per cent | Market Street (0 to 3 per cent: Estuary Path) |
| 2a | weather held fixed in daily-total growth (weekday or weekend, or term, holiday, weekend) | Estuary Path 18.3 to 19.0 |
| 2b | growth by hour cell, no weather | Estuary Path 42.0 (Tolland Road 35.3) |
| 2c | growth by hour cell with rain but no temperature | Estuary Path 34.7 to 39.3 |
| 2d | each day's busiest-hour growth with weather | Brickfields 22.3 |
| 2e | hour-cell mean ratios with no model: 2024 to 2025 (the hot summer left out), 2024 to 2026, dry days only | Estuary Path 39.3, 41.3, 34.7 |
| 2f | rules of thumb at the weekday peaks (10 per cent there and flat elsewhere; 5 per cent there and -2 per cent elsewhere) | Estuary Path 35.3, 30.3 |
| 3 (golden) | growth by counter, hour and day group with rain and temperature held | Tolland Road 24.3 to 35.0 across 23 specifications, first in each by 1.20x or more; the same step by filtering (hour cells on dry 18 to 22 C days) gives Tolland Road 30.7 |

Separation on the clean truth and on three redraws of the world (seeds 1169, 2169, 3169): the golden family names
one cycleway in every redraw and the default path and each half-step miss in every one (`checks.py` REDRAW). The
prototype sweep (ten seeds, `scratch proto/sw15*.out`) gave the same: 14 of 14 golden variants agreeing in every
seed, every reflex route missing.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each cycleway's counted segments | filed, policy 3.1 |
| 2 | Unit of account | a day of the coming summer | filed, policy 3.4 |
| 3 | Attribution window | clock hours 06:00 to 22:00 local | filed, policy 3.3 |
| 4 | As-of dating | the three summers named; the pull 9 October 2026 | filed, policy 3.4; manifest |
| 5 | Version basis | the unit of record per site | register, C1 (one segment) |
| 6 | Denominator | mean over three summers | filed, policy 3.4 |
| 7 | Weighting | each replayed day equally likely | filed, policy 3.4 |
| 8 | Window length | three summers | filed, policy 3.4 |
| 9 | Boundary inclusivity | widths off band edges; no hour on a capacity | C1, asserted |
| 10 | Rounding path | none on the call (categorical) | C1 |
| 11 | Tie-break | committee, never reached | filed, policy 2.3; no tie |
| 12 | Maturity and censoring | every summer complete | C1 |
| 13 | Order of operations | growth then replay then count | one order forced by policy 3.4 |
| 14 | Row order | file order irrelevant | C1 |
| 15 | Duplicate resolution | none in the counts | C1 |
| 16 | Identity normalisation | legacy site names and platform ids to segments through the register | dictionary semantics, C1 |
| 17 | Netting against gross | two directions added | filed, policy 3.3 |
| 18 | Dimensional units | riders an hour against riders an hour | units in the data |
| 19 | Code and status semantics | no_data, estimated and blanks not recorded | data notes; R2 asserted |
| 20 | Integerisation | counts are whole riders | C1 |
| 21 | Clause scope | the 2026-27 round | filed, policy 2.2 |
| 22 | Forward window contents | the coming summer's days are the replayed days | filed, policy 3.4 |

## Literal reader

Executed word for word, the policy fixes everything but the growth model: 3.1 the segments, 3.2 the capacities,
3.3 the crowded day, 3.4 the replay and the summers, 2.1 the comparison. "At the numbers of cyclists expected in
the coming summer" leaves the estimator of those numbers open, and the records force it: the back-test on summer
2026 (fit 2024 and 2025, predict each 2026 hour from its own day's weather) gives a mean squared log error of
0.026 with hour cells, rain and temperature against 0.036 with temperature alone, 0.037 with rain alone and 0.054
with no weather, and at each counted segment's busiest 2026 cell a mean absolute log bias of 0.021 against 0.041
for the counter's daily growth carried to the hour (Tolland Bridge's 08:00 cell: 0.032 against 0.100). Every
specification that keeps hour cells and temperature names Tolland Road (23 of 23); every reading of the policy's
terms gives the same call (SF1 to SF16).

## Oracles

Nothing in the pack ranks the cycleways on forecast crowded days. The dashboard (monitoring_export, a distractor)
answers monthly riders at the six dashboard sites and its summer growth ranks Market Street first; the activity
app's rides (distractor) rank Market Street; the events programme (distractor) names event days, which the golden
keeps as part of each day's calendar. The policy's history line says the 2022 criteria were replaced without naming
them. No file carries a crowded flag, a growth figure or a forecast (R1 asserted).

## Ask sheet

**Main call's declared row population:** the summer counts (legacy 2024 and platform 2025-26) of all 22 counted
segments, the register, the inventory, the guide, the policy, the weather on summer days and the term dates.
Device and hazard rows in it: 0 (asserted: the count week is in May 2026, the laptop clocks ran 17 March to 29 May
2026, and no log device spell falls in a summer; deleting the three ask files leaves the golden's forecast
unchanged).

**Ask A. For each site in the May 2026 volunteer count, the riders the counter recorded over the intervals both it
and the volunteers counted, and its shortfall against the volunteers' count of riders on the track** (12 figures:
whole riders, per cent to one decimal). H18 home: the check on the counters policy 4.2 reports beside the forecast.
Basis and grain in the asking sentence: the intervals both recorded, per site.
- A1 (D8, a clock against the volunteers' quarters; silent): the platform's interval export stamps each quarter at
  its end, in UTC, and selects on the stamp, so the file's range looks like quarter beginnings; nothing says which.
  Found only by the Station Sq gap sitting at 15:15 to 16:00 UTC against the log's 16:05 to 16:50 pause, or by the
  counter's ramps trailing the volunteers' by a quarter. Read as beginnings, every site's figures move.
- A2 (D8, a logger on the wrong clock; silent): the Quayside and Corn Exchange loggers were restarted from a laptop
  on local time (17 March, 21 April) and kept it until the summer round reset them on 29 May, so their stamps are
  local; the log carries the restarts and the reset, the counts carry an hour's lag. Missed, both sites move.
- Hazards: the Station Sq hour the logger did not keep (left out on both sides, as the ask says), road riders on the
  sheets (the ask says track), the Corn Exchange morning tallied by the hour.
- Stops (asserted): stamps read as beginnings (all six sites); laptop clocks missed (two sites); road riders counted
  (all six shortfalls); the Station Sq gap left in the volunteers' count (one site).

**Ask B. For each dashboard counter, the hours the maintenance log shows it recording nothing in 2025 and the
number of separate stoppages behind them** (12 figures: hours to one decimal, whole stoppages). H18 home: the
dashboard's own health, read beside the forecast's inputs; the log's summer rows never enter the main population.
- B1 (D6 with its over-cleaning half): follow-up visits linked by parent_job repeat their job's downtime and are no
  new stoppage; a visit that found the counter down again (Cathedral Green, Station Sq, Exchange St) carries its own
  downtime and is one. Summing every row or dropping every child both miss.
- B5 (D1, the same stoppage under two sources; silent): a fault the unit could not clear has the unit's job for the
  whole stoppage and the contractor's own job for its attendance inside it, unlinked (Quayside, Corn Exchange).
- B3 (D8, a stoppage across the year's edge; silent): Exchange St's New Year's Eve power cut and Southgate's New
  Year's Eve vandalism split at local midnight.
- B2 (D7): the Corn Exchange's February fault sits on the replaced unit CVC-0388; Station Sq's May battery job is
  keyed to CVC-1180, an id the register does not hold, with the site written correctly.
- Hazards: contractor downtime in minutes and the unit's in h:mm; two stoppages across a clock change, where
  wall-clock arithmetic is an hour out; blank-downtime firmware, inspection and replacement jobs.
- Stops (asserted): follow-ups summed (five counters); every child dropped (three); joined by asset id (one); by
  reported year (two); by closed year (two); contractor twins summed (two); wall-clock recompute (two).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 Station Sq gap | manual download paused the logger 16:05 to 16:50 on 13 May | A | Station Sq shortfall to 16.0 if kept in the volunteers' count |
| HA2 road riders | the forum tallies the carriageway too | A | every shortfall up 1.3 to 5.4 points |
| HB1 units | contractor minutes against the unit's h:mm | B | every contractor stoppage 60 times if read as hours |
| HB2 clock changes | stoppages across 30 March and 26 October 2025 | B | Cathedral Green and Quayside by an hour on a wall-clock recompute |

**Referee.** Ask A: the maintenance log's pause and restart times against the export's gap and lag. Ask B: the
register's unit dates and site names. Neither hands over a figure.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule, converted the
UTC, read the register's two Corn Exchange units as one site, left the gap out on both sides, counted track riders,
converted minutes and treated follow-up visits as no new stoppage; run on the cut pack by `generator/cracker.py`)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, counter riders and shortfall by site | 12 | interval stamps read as beginnings, the two laptop loggers read as UTC | A1 at every site, A2 at Quayside and Corn Exchange | miss |
| Ask B, 2025 hours and stoppages by counter | 12 | rows joined by asset id, every child row dropped, reported year, contractor twins summed | B1, B5, B3, B2 | miss |

One crack at a time (`cracker.py`): A1 cracked, the cracker keeps 8 figures and the pair is 37.7; B5 cracked, 4
figures, 33.1; B1 cracked, 3 figures, 31.9; B3 cracked, 2 figures, 30.8; A2 or B2 alone, none. Blind responses
(`checks.py` BLIND): a single constant shortfall matches at most one site. Screens from supplemental-stumping 1.1c
run before the cut: no release note announces a device (the data notes describe the interval export without saying
where a stamp sits), no device lands on a round multiple, and no device's two handlings tie.

Measured by: `generator/cracker.py` (run on the cut pack; each response scored on Part 0's weights, the call and its
components 38, the instructions 7, the asks 55 over the 24 ask figures; a response off the call keeps 5).

Mirror leakage: 0.0 per cent of ask weight, measured on the cut pack (the mirror, off the call on Estuary Path,
handles the asks as the cracker does and keeps none of the 24 figures).

Pair ceiling: 28.5 measured on the cut pack (the cracker 45.0, the mirror 12.0); both responses on the call 45.0;
the worst single crack 37.7 (A1).

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | R2 (checks.py) |
|---|---|---|---|---|
| L1 legacy local clock, hour beginning | legacy logging platform archive | counts_summer2024_legacy.csv | read as UTC | call and segment unchanged |
| L2 platform UTC, hour beginning | counter platform | counts_summer2025_2026.parquet | read as local | call and segment unchanged |
| L3 Ch1 wired away from the centre at two sites | legacy loggers | counts_summer2024_legacy.csv | channels taken as in and out | two-way sums identical |
| L4 outages: no_data with count 0, legacy blanks | platform and archive | both count files | read as zero riders | unchanged |
| L5 platform estimates for short gaps | counter platform | counts_summer2025_2026.parquet | read as recorded | unchanged |
| L6 partly lost hours recorded short | loggers | both count files | dropped as unrecorded | unchanged |
| L7 days the weather station did not report | station CVM-WX1 | weather CSV | filled with the month's mean | unchanged |
| L8 bank holidays inside the summers | term dates file | school_term_dates_2023-2027.csv | read as weekdays | unchanged |
| L9 events closing or filling paths | the city's programme | the counts | event days dropped | unchanged |
| L10 Corn Exchange unit replaced in March 2025 | register | counter_register.xlsx | 2024 lost by a join on the current unit | unchanged |
| L11 SF2 logger asleep overnight in August 2024 | legacy logger | counts_summer2024_legacy.csv | blanks read as zero | unchanged |
| L12 interval stamps at quarter ends, two loggers on laptop time | platform and loggers | count_week_15min_2026-05-11_15.csv | Ask A device | outside the main population |
| L13 follow-ups, contractor twins, minutes, mis-keyed and replaced ids | job system | counter_maintenance_log_2024-2026.csv | Ask B device | outside the main population |
| L14 a morning tallied by the hour | Cycle Forum sheets | volunteer_count_may2026.xlsx | none (sums the same) | outside the main population |

## Tried and rejected

- Candidate A with five summers of record (2022 to 2026): the extra cool summers made growth by hour without
  weather land Tolland Road on most seeds, so the no-weather rung stopped missing; dropped for three summers.
- Candidate A with four summers: the same failure on three seeds of ten.
- Hybrid-working layer (Tuesday to Thursday commuting above Monday and Friday): Market Street dominated and pooled
  weekdays offset the effect; the layer added no separation and was dropped.
- Grading the forecast crowded days as a whole number: the golden family spans 25 to 35 days for Tolland Road, so
  the figure is not determinate; the call is graded categorically with the segment and the hour, and blocks 1 to
  3 carry only record facts and the family's shared range.
- Weather-only decisive step (no hour cells): growth with weather held on daily totals lands Estuary Path, so the
  weather alone carries no stump; the decisive step needs the binding hour too.
- Ramp-up of a new route, factor-group expansion (spent by task177) and saturation at capacity (spent by task168):
  rejected on paper before any prototype.
- Summer holiday commuting at 0.72 of term (to keep every crowded morning in term): Brickfields rose to within 1.12x
  of Tolland Road and an evening hour appeared on the bridge; reverted to 0.80 and the hours are stated as weekday
  mornings.
- Ask A with the Quayside laptop clock as its only second device: cracking the stamp convention alone left 10 of 24
  ask figures to the cracker and a single-crack pair of 40.0; the Corn Exchange restart from the same laptop was
  added, measured 37.7.
- Ask B with a contractor twin and a recurrence on the same Cathedral Green fault: the two mishandlings cancelled on
  the stoppage count (the cracker kept it); the fault was made the unit's own and the twin kept elsewhere.
