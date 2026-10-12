# task138: Kestrel Bend Irrigation District, the 2027 season order with the Tolan Valley Project (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC09: the seed's world, decision and quantity are kept (an
irrigation district orders its season's water from its supplying project by 1 February, at the headgate requirement
covered in 24 of 30 replayed weather seasons through a daily soil-water model of each crop, rounded up to the next 100
acre-feet; nine laterals, 412 turnouts); its architecture (canal losses as a fill per refill plus seepage per wetted day,
recovered from closed lateral balances) is not used, because that driver is task67's fixed-plus-variable cost carried
per unit onto a denser period. The loss allowances are filed and are depth; the pitfall is re-found from how a season's
requirement depends on the soil water each field already holds when the order is placed.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task138.json`, architecture v1, registered 2026-10-12; `guard.py check` WARN on three findings (`three_rules.strategy_risk`, `repeat.gate_g`, `repeat.decision`, answered below) and one NOTE (`test.same_puzzle_older` against task446, differentiated on the card); `guard.py validate` clean |
| Domain / task type | physical-environmental-sciences / hydrology-flood-frequency (a client domain, its hydrology task type): a season's irrigation requirement read off an ensemble of replayed weather traces at a non-exceedance level (covered in 24 of 30) is hydrology's frequency analysis applied to a water-balance forecast |
| Objective | Forecasting & Predictive Modeling: the headgate requirement of the 2027 irrigation season (1 February to 31 October 2027), a window not yet open when the order is placed, forecast as thirty replays of past weather through the district's daily root-zone balance |
| Shape | 02 (forecast across many periods): the order and its monthly schedule (February to October, nine months), the weather year whose replay sets the order and that replay's requirement (12 figures), the replays chart's named parts (about 5), and two asks on 2026 rows the call never reads (each lateral's deliveries and the share of its water not delivered, 18 figures; each lateral's tail weir spill, 9 figures), the two files: about 46 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (acre-feet, the order in whole hundreds) |
| Mechanism | gap time (decisive: the replays are statements about past seasons, each of which began from whatever its own winter left in the soil; the order bets on a season that begins from a known, depleted state); pattern none, generators G16 (method selection: a season forecast conditioned on the state at the forecast date against an unconditioned replay of past seasons) then G3 (record against operation: that state is rebuilt from the delivery record, not from the model's own irrigation rule); Gate G `forecasting` (the thirty past seasons, read correctly, do not pin the 2027 requirement without the antecedent state); strategy `time_semantics` (F1: the as-of state at the forecast date, a clock already in the data, time since each field's own last irrigation) |
| Layer 2 family / pattern | `field_method` (hydrologic forecasting's own method: an ensemble of historical weather traces run from the current initial conditions, as in ensemble streamflow prediction); `own:antecedent-state-conditioned-season-replay` (Physical & Environmental Sciences has no library patterns; the nearest library line, urban-regional-science/forecasting/1, teaches features known as of the forecast origin, and here the origin's state has to be rebuilt) |
| Furniture | forum `customer_or_counterparty` (the order goes to the Tolan Valley Water Authority, the supplying project), forcing event `season_or_peak` (the 2027 season's order is due by Monday 1 February 2027, the day the canal opens), organisation family `local_government` (a California irrigation district, a special district under an elected board), role family `procurement_lead` (the water resources manager sources the district's supply), context artifact `filed_standard` (the district's Water Order Procedure, adopted by the board), calibration `none` (the delivery history and the closed lateral balances are the district's own records, not an organ), opening `question-first`, question form `how-much` |
| Spine | `kbid_irrigation_orders_2023-2026.csv`, the district's water ordering system export: one row per irrigation set (water ordered through one turnout onto one field for one run, with its status), four seasons, 64,887 rows; constructed |
| Deliverables | `kbid_order_2027.xlsx` (the order, its monthly schedule, the setting weather year and its requirement, the two asks), `kbid_order_2027.svg` (the thirty replayed seasons' headgate requirements from smallest to largest with the order drawn across them) |
| People | drawn with `guard.py names --geo "United States" --seed 138 --n 30`, keeping only names the guard clears: Sherry Nixon (water resources manager, the requester), Brittany Wall (general manager, signs the Water Order Procedure's annual tables), Colleen Ramsey (water master, runs the ditch riders and the meter book), Dennis Zhang (SCADA and instrumentation technician, the flumes and the weather station), Catherine Bradford (district engineer, the 2026 Lateral 5 tail realignment), Adam Arnold (water accounting, Tolan Valley Water Authority, the monthly delivery statements), Kristin Lucas (water conservation coordinator, collects the growers' 2027 water requests); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN. `three_rules.strategy_risk` (`time_semantics`): the analyst test
below names the easy analytical route that still fails once every field and rule is read correctly (every replay starts
with the root zone full, or with whatever each past year's own winter left); nothing in the pack is read two ways, and
the date each field was last watered is a plain fact in the orders. `repeat.gate_g` (`forecasting`, task137): the key is
honest, the past seasons read correctly do not pin the forward requirement without the state at the forecast date, and
task137's mechanism (a retention share conditioned on a repricing gap) shares nothing with it. `repeat.decision`
(`quantity_figure`, task137): the decision is the seed's, an order volume. The bans ran against task130, task136 and
task137, the three builds before this one by draw key: shape `other` (two of them) moved to 02, the forum off
`line_manager_or_team`, the forcing event off `purchase_order_or_contract` (the order is filed as the season's
deadline, `season_or_peak`), the organisation family off `utility_or_infrastructure` and `cooperative_or_member_body`,
the role off `research_desk` and `product_manager`, the context artifact off `capacity_report`, `register` and
`planning_thread`; a first people draw carried a first name used in task102 (replaced), and a PNG chart would have
repeated task136's deliverable set (the chart ships as SVG).

**Same-puzzle and same-driver tests.** Gap time, decisive G16, decision `quantity_figure`, Gate G `forecasting`: no build
in the last twelve carries the gap, the G-code and the decision together; task446 v2 (gap time, G16, a quantity) is the
older carrier and is differentiated on the card (there a filed leave-one-cohort-out test chooses which screening rate
carries across years; here no test chooses anything, and the replays must start from a state rebuilt from the record).

**Abstraction test.** Stripped of nouns, the driver is: a forward requirement replayed over past driver traces has to
start every trace from the store each unit actually holds at the forecast date, rebuilt from the unit's own last
recorded replenishment and the drawdown observed since; starting full, letting each trace inherit its own past year's
store, or rebuilding the store from the model's replenishment rule instead of the record each understates it. The
three nearest drivers (`guard.py nearest`: task51 lineage 0.05, a cumulative decomposition against a fixed reference
year; task134 v2 0.05, an inflow hazard from a pool outside the register; task229 v2 lineage 0.04, checks that see a
unit just before resetting it) share no latent structure, default path or correction with it. Read by idea rather than
by score: task46 (a rate law stationary only in cumulative exposure rebuilt from a movement log) also rebuilds a state
from a log, but the state there indexes a rate along a curve and the cohort crosses a step; here the state is an
initial condition of a water balance and the replays never see it. task133 (condition a filed curve on survival to date)
conditions a probability on the unit's past; here nothing is a probability, and the move is the start of a simulation.
task67 (the seed's own mechanism in other nouns) is the reason the seed's architecture was dropped.

**Data-native sentence.** Kestrel Bend's growers stop irrigating at harvest, so every field took its last 2026 water in
September (374 of the 619 requested fields) or October (245), most of them weeks before the canal closed for the winter
on 31 October, and the October to January that followed was the driest in the district's weather record (1.36 inches
of rain against a median of 6.81 over 32 winters; asserted); each field therefore enters the 2027 season short of field
capacity by an amount set by its crop, its soil and the date of its own last set (3.39 inches acre-weighted, 446 of the
619 fields at or past their allowable depletion), an amount that lives only in the irrigation orders and the daily
weather, and that none of the thirty past seasons the procedure replays ever started from.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (48 builds): hazards by time since entry
(134), selection on the outcome (124), the maturity of a claims window (130), a campaign carried per untapped member
(136), a retention share conditioned on a repricing gap (137), corpus-recovered conversion rates (27, 29, 30, 78),
censored delays (31, 99), a fixed-plus-variable cost carried per unit (67, the seed's mechanism), a cumulative exposure
rebuilt from a log (46): none starts a replayed forecast from a stored state at the forecast date.
`stumping/references/client/two-layer-task-design.md`: Physical & Environmental Sciences has no library patterns, so
the pitfall comes from the `field_method` family, here hydrologic forecasting's conditioning on initial state.
`stumping/references/client/measured-drivers.md`: the held tasks are a construction upstream of every graded figure that
the solver's hypothesis space does not hold; the state here is built per field from two files (the orders and the
weather) that the default path reads for other things or not at all. The seed's header (FC09) for the world only.

**World.** Kestrel Bend Irrigation District is a California irrigation district on the east side of the San Joaquin
Valley, formed in 1921 and governed by a five-member elected board. It takes surface water from the Tolan Valley Canal
at its headgate (milepost 41.2), under a water service contract with the Tolan Valley Water Authority, the joint powers
authority that runs the Tolan Valley Project. A main canal carries the water from the headgate to nine laterals, which
serve 412 turnouts and their fields (almonds, pistachios, walnuts, wine grapes, citrus,
alfalfa and irrigated pasture; 636 fields in the register, 619 of them on accepted 2027 requests for 39,399 acres). The
contract quantity is 241,000 acre-feet a year. The canal runs from 1 February to 31 October and is dry from November to
January for maintenance. The Authority asks each contractor for its season's order by 1 February. The district's Water Order
Procedure (WOP, adopted 2019, tables revised each December) sets the order at the smallest whole number of hundreds of
acre-feet that would have covered the season's headgate requirement in at least 24 of the 30 weather years 1997 to
2026, each weather year's 1 February to 31 October weather run through the procedure's daily root-zone water balance
for every field on the coming season's water requests, with the procedure's lateral and main canal loss allowances on
top, and spreads the order over the months in proportion to the replays' monthly requirements. The district's weather
record is the state agricultural weather network's station 39 to 30 April 2014 and the district's own station at the
Kestrel Bend yard from 1 May 2014.

As-of dates: the growers' 2027 water requests closed on 15 January 2027; the weather record and the irrigation orders
are extracted on 1 February 2027 (weather through 31 January); the 2026 meter book, flume and weir records were closed on
30 November 2026; the request is made on Monday 1 February 2027, and the order is due at the Authority that day.

## Default path

1. Read the Water Order Procedure: the order rule (24 of 30, whole hundreds), the daily root-zone balance (crop
   coefficients by month on reference evapotranspiration, rain beyond field capacity draining, depletion capped at the
   root zone's available water, irrigation at the allowable depletion back to field capacity, delivery at the
   application efficiency of the field's method), the loss allowances and the monthly schedule rule.
2. Assemble the coming season's fields: the latest accepted 2027 water request for each field, joined to the field
   register for its turnout, lateral, soil unit and irrigable acres, and to the procedure's tables for its crop
   coefficients, root depth, allowable depletion and application efficiency.
3. Splice the weather record as the procedure sets it (station 39 to 30 April 2014, the district station after, its
   missing days from station 39), in inches.
4. For each weather year 1997 to 2026, run every field from 1 February to 31 October with its root zone at field
   capacity on 1 February; sum the deliveries by lateral, add the lateral and main canal loss allowances.
5. Take the 24th smallest of the thirty headgate requirements, round up to the next 100 and spread it over the months.

Ends on: 189,800 acre-feet, set by the 2003 weather year (its requirement 189,784.57 acre-feet; asserted in
`checks.py` and recomputed by `verify.py`).
Golden: 202,700 acre-feet, set by the 2012 weather year (its requirement 202,657.77, to the nearest 10 acre-feet
202,660): every replay starts from the depletion each field carries at the end of 31 January 2027, built from its last
2026 delivered set (the orders) through the observed autumn and winter weather with the same daily balance.

## Stump sentence

A competent solver assembles the 2027 fields, splices the weather record, replays the thirty weather years through the
procedure's daily root-zone balance with every field at field capacity on 1 February, adds the loss allowances and
files 189,800 acre-feet set by 2003 (Ends on); the step that lands it there is not starting each replay from the
depletion each field actually carries on 31 January 2027, which every field built from a last set in September or
October through the driest October to January on record: the golden is 202,700 acre-feet set by 2012.

## Three rules

- **Domain test:** the deciding quantity is a season's irrigation requirement from a daily root-zone water balance (crop
  coefficients on reference evapotranspiration, allowable depletion, rain beyond field capacity draining), forecast as
  an ensemble of past weather traces started from the soil water each field holds when the order is placed, which is
  how an irrigation hydrologist conditions a season's water forecast on its antecedent state; with another field's
  nouns there is no root zone, field capacity or reference evapotranspiration for the carry-over to live in.
- **Analyst test:** a strong analyst who reads the procedure and every file correctly, takes the latest accepted
  requests, splices the weather record, replays the thirty weather years field by field and applies the loss
  allowances still starts every replay with the root zone full (189,800 acre-feet), or lets each weather year start
  from the state its own past winter left (193,100), or runs the planning model through 2026 with its own irrigation
  rule, which keeps watering every field into late October, before carrying the state forward (193,800); each is 8,900
  to 12,900 acre-feet short of the season the fields will actually start (202,700).
- **Layer 1:** a weather record spliced from two stations (station 39 in millimetres to April 2014, the district
  station in inches after, an overlap month in April 2014 and the yard's missing days filled from station 39), a field
  register re-mapped in March 2025 after parcel splits (former field ids on the 2023 and 2024 orders), revised and
  withdrawn water requests (the latest accepted version governs), orders cancelled before water ran, turnout ids
  written three ways (the ordering system `05-031`, the meter book `5-31`, the GIS `T05031`), and on the ask paths a
  meter book with mid-season meter changes, register rollovers and meters registering hundreds of cubic feet, a
  lateral tail reach re-served from another lateral in mid-season, heading flume days estimated through sensor outages,
  and riders' weir sheets with board changes in free text and alternate-day reads in August. Each is something these
  systems produce; none decides the call.
- **Layer 2:** the shortcut is to replay past seasons as they were (start full, or start where each past winter left
  the soil); the expert runs the ensemble from the state the system is in at the forecast date, rebuilt field by field
  from the delivery record and the observed weather with the same balance the replays use.

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a
reflex of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction,
ratio or half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 every request row summed (superseded and withdrawn versions in), full start | WOP 6.2 names the latest accepted version | the requests' `status` column | yes | no | yes (duplicate fields) | yes | readable |
| R0 every replay starts at field capacity on 1 February (the default path) | no | no | yes (FAO-56's own start for a season after winter rain) | no | no | no | readable |
| R1 each weather year starts from the state its own preceding autumn and winter left (the model run through the year before) | WOP 3.1's recursion asks for a start state | no | yes (a modeller's spin-up) | no | no | no | readable |
| R2 the 31 January 2027 state from the replay rule run through the 2026 season, then the observed winter | WOP 3.1 and 3.4 read as one model run continuously | no | yes (a spin-up through the latest season) | no | no | no | readable |
| R2b every field full on 31 October 2026, the canal's close, then the observed winter | no | no | yes (the canal closed with the fields watered) | no | no | yes (a district-wide winter deficit) | readable |
| R2c each turnout's last delivered set taken as every field's on it | no | the orders' `turnout` column | yes (the delivery point is the turnout) | no | no | no | readable |
| R3 (decisive) every replay starts from the depletion each field carries at the end of 31 January 2027, rebuilt from its own last delivered 2026 set (the orders, field by field) through the record's autumn and winter weather with the same daily balance | no sentence names a start state, a last irrigation, the winter or the orders; WOP 2.4 substitutes only each year's 1 February to 31 October weather, and every daily balance needs a start, which FAO-56 and the default reading take as a full root zone | no column holds soil water, a start state or a last irrigation; the orders are at set grain with statuses, and the date that matters is each field's own latest delivered set | no: the reflexes are R0 to R2c, and each files its own wrong order | no closed record scores it: no past season's requirement, district balance or order ships, and the 2023 to 2025 orders are growers' own schedules that no planning model reproduces | no | no: per field, floored at zero and capped at the root zone's available water, and each replay's February and March rain refills part of it | silent |

The decisive rung is silent because nothing in the pack is about the soil at the start of the season: the procedure
describes a balance and a replay window, the orders are a booking system's export, and the autumn and winter weather
sits at the end of a thirty-one-year record whose replays never use it. The default path reads every file correctly
and never needs either.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move the call or its figures, or shown to converge). WOP is the Water Order
Procedure; T1 to T5 its tables.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the 2027 season" | deliveries at the headgate 1 February to 31 October 2027 | calendar 2027 | same call: the canal is dry from 1 November to 31 January (asserted: no delivered set outside the season in any year on file) | WOP 2.1 |
| SF2 | "how much water ... order" | the smallest whole number of hundreds of acre-feet covering the headgate requirement in at least 24 of the 30 weather years (the 24th smallest, rounded up) | the 80th percentile interpolated across the thirty (the 24.2nd value); the 24th rounded to the nearest hundred | the interpolated percentile files 203,200; the nearest hundred converges on 202,700 (both asserted) | WOP 2.3 |
| SF3 | the fields | each field's latest accepted 2027 water request; withdrawn requests and superseded versions out | every request row; withdrawn requests in; the 2026 crop report's fields | every request row files 218,800 (R-1) | WOP 6.2; the requests' `Status` defined in the dictionary |
| SF4 | a field's acres, crop and irrigation method | those on its accepted 2027 request | the register's GIS acres | 204,400 | WOP 6.2 |
| SF5 | a field's total available water | T3 available water capacity times the lesser of the crop's T2 root depth and the soil unit's T3 depth limit | capacity times root depth with no depth limit | 202,300 | WOP 3.3 |
| SF6 | the weather record | station 39 to 30 April 2014, the District station from 1 May 2014, a day the District station did not record taking station 39's values; station 39's millimetres in inches | station 39 throughout; the District station from its first day (April 2014); missing yard days as zero (dropped) | station 39 throughout 205,500; the yard from April 2014 the same order, setting year and requirement but other months (April 10,180 against 10,290); missing days as zero 202,600 (each asserted) | WOP 6.1 |
| SF7 | a replay's days | each weather year's own 1 February to 31 October, 29 February kept in a leap year | 29 February dropped | the same order and setting year, other months (asserted) | WOP 2.4 ("its 29 February included in a leap year") |
| SF8 | a day's arithmetic (the order of operations within a day) | the previous day's depletion plus the day's ET less its rain, then the floor at zero and the cap at total available water, then the irrigation test at the day's end | the irrigation test before rain; the rain taken first, its excess over the depletion drained, then the day's ET | 205,000; 202,800 (both asserted) | WOP 3.1 ("A day's depletion is the previous day's depletion plus the crop's evapotranspiration for the day less the day's rainfall. It is never less than zero"), 3.4 ("on any day at whose end its depletion has reached or passed") |
| SF9 | where each replay starts | the depletion each field carries at the end of 31 January 2027 (R3) | full (R0); each weather year's own preceding autumn and winter (R1); the replay rule run through 2026 (R2); full at the canal's close (R2b); the turnout's last set (R2c) | each files its own order (Ladder) | R0 by WOP 3.1 on the record (each day's depletion is the previous day's plus ET less rain, and no rain or irrigation since each field's last set brought it to zero); R1 by WOP 2.4 (only each year's 1 February to 31 October weather is put on the 2027 season, whose autumn and winter already fell); R2 by WOP 3.4 (its irrigation rule is the replays'; the 2026 irrigations are on the orders); R2b by WOP 3.1 (the canal's close is not an irrigation); R2c by the orders (every set names its one field) |
| SF10 | "an irrigation" in the record | an order with status Delivered | cancelled orders counted (R2d) | moves the order | the dictionary ("Cancelled: cancelled before water ran; no water was delivered") |
| SF11 | the day of a field's last irrigation | the day its last delivered set ran | the set's start day against its end day | converges: every field's last 2026 delivered set starts and ends on one day (asserted) | the records converge |
| SF12 | a field on the 2027 requests with no 2026 delivered set | none exists | (a start state for a new field) | converges (asserted: every requested field took a delivered set in 2026) | the records converge |
| SF13 | the crop in the 2026-27 autumn and winter | the crop on the 2027 request | the 2026 crop | converges: every requested field carries the crop it had in 2026 (asserted) | the records converge |
| SF14 | the winter cap | depletion never above total available water | uncapped | moves the order (O2) | WOP 3.1 |
| SF15 | the loss allowances | water put into a lateral is its fields' deliveries over one less the T5 allowance; the headgate requirement is the laterals' water over one less the main canal allowance | deliveries times one plus each allowance | 200,200 | WOP 4.1 |
| SF16 | a field's lateral (the 20 fields on turnouts 05-045 to 05-058, fed from Lateral 6 through the connector since 15 June 2026) | the register's lateral as it stands: Lateral 6 (asserted for all 14 turnouts) | Lateral 5, by the turnout number's 05 or by the reach's feed before 15 June | 202,500 (asserted) | WOP 6.2 ("The fields, their turnouts, laterals and soil units are as the District's field register stands when the order is calculated") |
| SF17 | "the weather year whose replay sets it" | the weather year of the 24th smallest requirement | the 25th (the first year not covered) | names another year | WOP 2.3 ("covered ... in at least 24") |
| SF18 | "that replay's headgate requirement" | its unrounded requirement, to the nearest 10 acre-feet | the order itself | different figure | the prompt (two figures asked) |
| SF19 | the monthly schedule | each month's requirement summed over the thirty replays over their total, times the order, each month to the nearest 10 acre-feet, October the difference | the setting replay's own months; the mean of the thirty years' monthly shares | moves every month | WOP 5.1 |
| SF20 | reference evapotranspiration | the ET0 the weather record reports | ET0 recomputed from the stations' temperatures (Hargreaves) | 214,800 | WOP 3.2 ("the reference evapotranspiration the District's weather record reports for the day") |
| SF21 | rain | every inch counts until the root zone is full, the rest drains | an effective-rain fraction (75 per cent) | 206,600 | WOP 3.1 |
| SF22 | units | inches of depletion, ET and rain; acre-feet as inches times acres over 12 | (none) | n/a (the model's own arithmetic reproduces each replay, asserted) | WOP 3.1, 3.5 |
| SF23 | ties at the order's rank | none: the 23rd (2000, 201,412), 24th (2012, 202,658) and 25th (2003, 204,982) smallest stand apart (asserted at 300 acre-feet, margins printed) | (a tie-break) | n/a | the records converge |
| SF24 | the root zone after a field's last 2026 set | field capacity: the field ends the day of the set at zero depletion | the 2026 season run through the balance from a full root zone on 1 February with each delivered set's volume (cubic feet per second times hours) times the application efficiency taken off the depletion | 206,200 (asserted) | WOP 3.4 ("An irrigation returns the root zone to field capacity: a field ends the day of an irrigation at zero depletion") |
| SF25 | the day of a field's last 2026 set, in the carry to 31 January | the field ends that day at zero depletion and the balance runs from the next day | that day's ET and rain counted after the set | 203,200 (asserted) | WOP 3.4 ("a field ends the day of an irrigation at zero depletion") |
| SF26 | Ask A: a Lateral 5 tail turnout's lateral on a read interval | the lateral that fed it: Lateral 5 for intervals ending at or before its 15 June 2026 read, Lateral 6 after (no water ran to the reach from 13 to 15 June and every tail meter was read on 15 June, both asserted, so no interval straddles the change) | the register's Lateral 6 all season; the turnout number's Lateral 5 all season | S3: Lateral 5 15,290 and 15.0, Lateral 6 18,510 and 7.9; the turnout number's lateral leaves Lateral 5 delivering 19,690 against 17,990 put in, a negative share (both asserted) | the ask's own terms (the share of the water put into a lateral that its turnouts did not deliver: a delivery counts against the heading its water passed); the operations log's 13 and 15 June entries ("Turnouts 05-045 to 05-058 now fed from Lateral 6 through the connector"); the register's `lateral` ("The lateral the turnout is on") as it stands on 1 February 2027 |
| SF27 | Ask A: Laterals 5 and 6's water put in after the connector | each heading's daily volumes as recorded (from 15 June the reach's water passes Lateral 6's heading) | the reach's metered water after 15 June moved from Lateral 6's heading to Lateral 5's, the reach on Lateral 5 all season | Lateral 5 19,690 and 7.1, Lateral 6 14,110 and 16.5 (asserted) | the dictionary's `volume_af` ("Water that passed the lateral's heading structure on the day"); the operations log's 15 June entry (the reach fed from Lateral 6 through the connector) |
| SF28 | Ask B: the head over a tail weir with flashboards in | the gauge reading less the crest gauge reading less 2 inches for each board the remarks show in place | the gauge less the bare crest | every lateral high, 1.5 to 5 times (S1, asserted) | the physical fact that a board set in a weir's slots raises its crest by the board's height (the structures sheet gives the weir as built, its crest gauge reading and two flashboard slots, H the head over the crest); the riders' 24 board notes, each timed ahead of its sheet's reading (asserted), converge on the boards in place at each reading, and a change taken from the next day instead (Lateral 2 640, Lateral 4 280, Lateral 6 660) is ruled out by those times |
| SF29 | station 39's millimetres in inches | divided by 25.4 and carried unrounded (closure axes 10 and 18) | each converted value rounded to the yard's hundredths of an inch; 0.0394 inches per millimetre | 202,400; 202,800 (both asserted; neither is a literal reading) | the inch is 25.4 millimetres by definition, and the dictionary's station 39 entry gives it ("millimetres (25.4 millimetres to the inch)"); no sentence rounds the network's values before the balance (WOP 3.2 takes the reference evapotranspiration "the District's weather record reports for the day") |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads them
all correctly. SF9 lists methods, not readings; each competing start is priced and refused by a quoted sentence on the
record, never by a reading. SF26 to SF28 are the asks' readings the leak reader raised, closed the same way; SF29 is the
judge's unit margin (the 24th smallest sits 42.23 acre-feet under the order's edge, so a non-literal conversion moves the
order), closed by the inch's definition, which the dictionary states as a unit fact.

## Ladder

Every rung is a complete pipeline on the same literal estimand (WOP 2.3 and 2.4), computed by `checks.py` from the
pack (619 fields on accepted requests, 39,399 acres) and the default path and golden again by `verify.py`.

| Rung | Start of each replay | 24th smallest (AF) | Order | Setting year | Against the golden |
|---|---|---|---|---|---|
| R0 (default) | full on 1 February | 189,784.57 | 189,800 | 2003 | -6.35 per cent |
| R1 | each year's own autumn and winter | 193,082.95 | 193,100 | 2008 | -4.72 per cent |
| R2b | full at the canal's close, then the observed winter | 191,081.72 | 191,100 | 2003 | -5.71 per cent |
| R2 | the replay rule run through 2026, then the observed winter | 193,792.30 | 193,800 | 2008 | -4.37 per cent |
| R2c | each turnout's last delivered set | 200,347.25 | 200,400 | 2012 | -1.14 per cent |
| R2d | a field's last 2026 order whatever its status | 200,944.81 | 201,000 | 2012 | -0.85 per cent |
| R3 golden | each field's own last delivered set through the observed winter | 202,657.77 | 202,700 | 2012 | 0 |
| O2 | R3 with the winter cap dropped | 203,112.90 | 203,200 | 2012 | +0.22 per cent |
| O1 | R0 plus each field's 31 January depletion as a flat addition | 205,621.34 | 205,700 | 2003 | +1.46 per cent |

- **Separation.** The golden is the grid's extreme reachable cell from below: every start that reads the record less
  fully (full, own winter, canal close, model history, turnout, cancelled orders) files less, the first four by 4.4 to
  6.4 per cent; the two over-corrections that break a filed rule (no cap, a flat addition that ignores the replays' own
  rain) file more. On R0, R1, R2 and R2b the setting year moves off 2012 (2003, 2008, 2008, 2003) and the schedule and
  its February figure move with it (asserted; February is 10 acre-feet on R0 against 13,520); R2c and R2d keep 2012 and
  file other orders. The asserted floors: R0, R2b at least 5 per cent under, R1 4.5, R2 3, R2c 1, R2d 0.6.
- **Position.** The 24th smallest sits 57.77 acre-feet above 202,600 (42.23 under the order), its neighbours 1,246
  under (2000) and 2,324 over (2003); every month at least 1.88 acre-feet from a rounding edge, the setting
  requirement 2.77 (asserted at 1.5).
- **Grid.** The nine starts on both weather records (WOP 6.1's splice, station 39 throughout), 18 cells computed in
  `checks.py`: the golden cell alone files 202,700 (asserted); on station 39 the starts file 191,100 to 207,500, R3
  205,500. Every other fork alternative is computed one at a time against the golden start (the `SF` rows).
- **Worth on the graded figures.** R3 moves the order and all nine monthly figures; against R0 to R2b it also moves the
  setting year and its requirement. Nothing graded on the call survives the default.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | every field on its latest accepted 2027 request (WOP 6.2); every such field took a delivered set in 2026 and carries its 2026 crop (asserted, SF12, SF13); members not yet observed: none, the requests closed on 15 January and a field without an accepted request is not irrigated in the replays (WOP 6.2) |
| 2 | Unit of account | acre-feet at the headgate; the field (one request) is the balance's unit; the order in whole hundreds |
| 3 | Attribution window | the season 1 February to 31 October (WOP 2.1); each replay the weather year's own 1 February to 31 October (WOP 2.4) |
| 4 | As-of dating | the register and the requests as extracted on 1 February 2027; the weather and the orders through 31 January 2027 |
| 5 | Version basis | the latest accepted request version (WOP 6.2); the register as it stands (6.2) |
| 6 | Denominator | the loss allowances divide (WOP 4.1, SF15); no rate is estimated |
| 7 | Weighting | none: a sum over fields, laterals and months |
| 8 | Window length | the thirty weather years 1997 to 2026 (WOP 2.3) |
| 9 | Boundary inclusivity | 1 February and 31 October inclusive; "at least 24"; "reached or passed" its allowable depletion (WOP 3.4). Every allowable depletion in Tables 2 and 3 is an odd number of hundred-thousandths of an inch, off every lattice a day's depletion can sit on (station 39's tenths of a millimetre, the yard's hundredths of an inch, two-decimal coefficients), so no replay day lands on one; the closest approach over every day of the thirty golden replays is 1.2e-6 inch (asserted in `checks.py` and `verify.py`) |
| 10 | Rounding path | carried unrounded; the order rounded up once (WOP 2.3), the setting replay's requirement to 10 acre-feet, the months by WOP 5.1; the 24th smallest sits 57.77 acre-feet above 202,600 (asserted between 25 and 75), the setting requirement 2.77 and every month at least 1.88 acre-feet from a rounding edge (asserted at 1.5, flip distances printed) |
| 11 | Tie-break | none needed: the 23rd, 24th and 25th smallest 1,246 and 2,324 acre-feet apart (asserted at 300) |
| 12 | Maturity and censoring | none: the weather record has every day from October 1995 to 31 January 2027 (asserted: station 39 complete, the yard's missing days take station 39's) and the 2026 orders are closed (the canal closed 31 October) |
| 13 | Order of operations | per day ET and rain together, then floor and cap, then the irrigation test (WOP 3.1, 3.4, SF8); the day of a field's last 2026 set ends at zero and the carry runs from the next day (WOP 3.4, SF25) |
| 14 | Row order | file order changes nothing (asserted: the orders shuffled and the requests reversed file the same order, requirement and months) |
| 15 | Duplicate resolution | request versions: the latest accepted (SF3); orders: every order number unique (asserted) |
| 16 | Identity normalisation | field ids since the March 2025 re-mapping on both the 2026 orders and the 2027 requests (asserted: every one in the register); turnout id formats matter only on the ask paths |
| 17 | Netting against gross | rain nets ET within a day, floored at zero (WOP 3.1); nothing else nets |
| 18 | Dimensional units | station 39 in millimetres, the District station in inches (SF6), station 39 converted at 25.4 millimetres to the inch and carried unrounded (SF29); acre-inches to acre-feet over 12 |
| 19 | Code and status semantics | request status, order status and station quality flags are defined in the dictionary (field semantics, never the stump) |
| 20 | Integerisation | the order in whole hundreds, the months in tens (WOP 2.3, 5.1) |
| 21 | Clause scope | WOP 3.4's first sentence (an irrigation returns the root zone to field capacity) applies to every irrigation, the 2026 sets on the record included (SF24); its second (the irrigation rule) in a replay |
| 22 | Forward window contents | the thirty weather years' 1 February to 31 October weather, all in the record; the 2027 requests |

## Literal reader

Executed word for word, the prompt and the Water Order Procedure define the order as the smallest whole number of
hundreds of acre-feet covering, in at least 24 of the 30 weather years 1997 to 2026, the water the headgate would take
from 1 February to 31 October 2027 if that year's 1 February to 31 October weather fell on the 2027 season (WOP 2.3,
2.4), every field on its latest accepted request run day by day through the balance of WOP 3 and carried to the
headgate by WOP 4.1. WOP 3.1 makes each day's depletion the previous day's plus the crop's ET less the rain, so the
first day of every replay needs each field's depletion at the end of 31 January 2027; the same sentence gives it from
the field's last irrigation (WOP 3.4: an irrigation ends its day at zero depletion), which the orders date for every
field (status Delivered; the dictionary says a cancelled order delivered no water), through the record's weather to 31
January. No sentence starts a replay full, borrows another year's autumn and winter, or applies the replays' irrigation
rule to 2026. Every term in the fork table resolves to one reading or converges; the only steps the text leaves open
are how to carry each field to 31 January, which the text then settles, and the arithmetic.

## Oracles

- **None on the call path.** No past season's requirement, district balance, order or schedule ships; nothing states
  a 2027 figure. The 2023 to 2025 orders are the growers' own schedules (sets at the growers' own intervals and
  lengths), which no planning model reproduces: replaying 2026 under either start and comparing with the 2026 orders
  confirms neither.
- **The WOP tables** state coefficients, depths, capacities, efficiencies and allowances: inputs every rung uses alike.
- **The ask paths** (the meter book, the meter shop log, the lateral headings, the tail weir sheets): no rung of the
  call reads them, and nothing in the pack states a lateral's 2026 deliveries, loss or spill, so none ties only under
  the golden.

## Ask sheet

**Main call's declared row population:** every row of `kbid_water_requests_2027.xlsx`, `kbid_field_register_2027-02-01.csv`,
`station39_daily_1995-2027.csv` and `kbid_station_daily_2014-2027.csv`, the 2026 delivered sets of
`kbid_irrigation_orders_2023-2026.csv` (each field's last one decisive), the Water Order Procedure and its tables. The
asks' devices live in `kbid_meter_book_2026.csv`, `kbid_meter_shop_log_2026.xlsx`, `kbid_lateral_headings_daily_2026.csv`,
`kbid_tail_weir_sheets_2026.csv` and `kbid_canal_structures.xlsx`, which no rung of the call reads; `checks.py`
asserts the call unchanged with all five removed (and the three distractors), and both asks unchanged with the
distractors removed. HA1's root, the Lateral 5 tail realignment, reaches the call only through the register's lateral,
which WOP 6.2 fixes (SF16: the Lateral 5 reading files 202,500).

**Ask A. Each lateral's 2026 deliveries, and the share of the water put into it that its turnouts did not deliver**
(9 laterals by 2 figures, 18: acre-feet to the nearest 10, per cent to one decimal).
- H18 home: the order carries each lateral's loss allowance (WOP T5); the 2026 measured losses are the reconciliation
  the allowances are set against (an input reconciled to another system's total, the gap made of devices). The call
  does not turn on it (the order uses the filed allowances).
- Construction: each turnout's metered season volume from the riders' meter book (weekly reads of each meter's
  register, in the meter's own units), meters changed in mid-season chained through the meter shop's removal and
  installation reads, registers that rolled over carried, converted to acre-feet, summed by the lateral that fed the
  turnout on each read interval; the lateral's water in from its heading's daily volumes (estimated days included, as
  the record); share = (in less deliveries) over in.
- Primary device (D7, the true key elsewhere: a prior-id chain): 31 turnouts, on every lateral, had their meter
  replaced in mid-season; the book carries each meter's reads under its own serial, and the water that ran between the
  old meter's last weekly read and its removal, and between the new meter's installation and its first weekly read,
  appears only in the shop log's removal and installation reads. Differenced within each serial the book loses that
  water (25 to 82 acre-feet a lateral); differenced across the change by turnout it picks up the gap between two
  unrelated registers (the shop fits 14 new meters, registers at 0.00, and 17 of its rebuilt meters, each with the
  register it carried out of its last service; the shop log says which). Every lateral moves under both; counting a
  new meter's first read from zero recovers only part of the gap (S2b); nothing in the book flags a change except the
  serial column, and the dictionary describes the shop log flatly.
- Hazards: HA1 (D7, as-of) the Lateral 5 tail reach (14 turnouts) was re-served from Lateral 6 through a new connector
  from the 15 June 2026 read; the register carries their current lateral (6), and the operations log records the
  change in its own day's entry, so the register's lateral puts their spring water on Lateral 6; HA2 (D3, loud) 42
  magnetic flowmeters, on every lateral, register hundreds of cubic feet; HA3 (loud) seven registers roll over, on
  Laterals 1, 4, 5, 8 and 9; HA4 (D4) the headings' estimated days (sensor outages: Lateral 2 four days, Lateral 4 six,
  Lateral 6 three, Lateral 9 five) are part of the record (the dictionary), and dropping them lowers those four
  laterals' water in.
- Converging readings (asserted): the book brackets the season at every turnout (opening reads before 1 February,
  closing reads after 31 October, no water outside the season); every one of the 14 tail meters was read on 15 June
  2026, the realignment day, so no read interval straddles it.
- Path (6 files, 20 columns): the meter book (`turnout`, `meter`, `read_date`, `read_time`, `reading`), the shop log's
  2026 changes (`Date`, `Time`, `Turnout`, `Meter removed`, `Register at removal`, `Meter installed`, `Register at
  installation`) and meters in service (`Meter`, `Register units`, `Register capacity`), the field register
  (`turnout_id`, `lateral`), the lateral headings (`lateral`, `volume_af`, `quality`), the operations log's 13 and 15
  June entries, the dictionary.
- Stops (each computed and asserted in `checks.py`): S1 natural, differenced by turnout across changes (all 18 off:
  deliveries 18,700 to 52,640 acre-feet, every share negative); S2 within serial (all 18 off, each lateral's
  deliveries 25 to 82 acre-feet low, shares 0.2 to 0.5 points high); S2b within serial with each new meter's first
  read counted from zero (all 18 off, 11 to 66 acre-feet low, Lateral 7's the thinnest at one bin and 0.1 points);
  S3 chained, the register's lateral (Laterals 5 and 6, four figures off: 15,290 and 15.0, 18,510 and 7.9); S4
  chained, as-of lateral, estimated days dropped (four shares off: Lateral 2 7.0, Lateral 4 11.7, Lateral 6 12.2,
  Lateral 9 12.6); answer.
- Lazy delta: S1 wrong on 18 of 18.
- Realism: meters are swapped through the season and the riders' book is kept by serial; a reach re-served from a
  neighbouring lateral is ordinary capital work.

**Ask B. The water that went over each lateral's tail weir in 2026** (9 figures, acre-feet to the nearest 10).
- H18 home: operational spill is the part of each lateral's loss the allowance treats alike with seepage; the 2026
  split is the reconciliation's second line (a measure every lateral carries that the call does not turn on).
- Construction: each morning's staff gauge reading at the tail weir stands for its day and each following day until
  the next reading (the dictionary); flow over the weir from the structures sheet's weir equation (Q = C x L x H^1.5,
  coefficient, crest length, crest gauge reading) on the head above the crest in place that day, the crest raised by
  each 2-inch flashboard the riders' remarks record as in, in acre-feet per cfs-day.
- Primary device (D2, an attribute at the wrong vintage): the structures sheet gives each weir's crest gauge reading
  with no boards and its `Flashboard slots` (2), no board height; riders set and pull boards through the season to hold
  water in the tail reach and record it only in the free-text remarks of the day's sheet, with the time of the change
  ("07:33 set one 2-inch board", "added a 2-inch board", "pulled one board", "pulled boards", each after its time).
  Read against the bare crest, every day with boards in counts the boards' height as head; every lateral carried
  boards for part of the season, so all nine figures run high (1.5 to 5 times the golden).
- Converging readings (asserted): each of the 24 board notes carries a time ahead of its sheet's reading, so the change
  is in place at that reading; a change taken only from the next day would move three laterals (Lateral 2 640,
  Lateral 4 280, Lateral 6 660).
- Hazards: HB1 (shared, D8) three laterals (3, 7 and 8) were read on alternate days in August (the reading stands until
  the next one, per the dictionary); HB2 (D3, texture) the weir coefficient is in feet and seconds.
- Path (3 files, 8 columns): the tail weir sheets (`sheet_date`, `lateral`, `gauge_ft`, `remarks`), the structures
  workbook's tail weirs (`Crest length L (ft)`, `Crest gauge reading (ft)`, `Coefficient C`, `Flashboard slots`), the
  dictionary.
- Stops (computed and asserted): S1 natural, the bare crest every day (9 of 9 off: 660 to 1,460 acre-feet against 270
  to 650); S2 boards from the remarks but the alternate-day gaps left at zero (three off: Lateral 3 410, Lateral 7 490,
  Lateral 8 410); answer.
- Lazy delta: S1 wrong on 9 of 9.
- Realism: tail weirs carry flashboards and riders note board changes on their sheets; the structures sheet holds the
  weir as built.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 the Lateral 5 tail reach re-served | the 2026 connector | Ask A (Laterals 5 and 6) | four figures (S3) |
| HA2 meters in hundreds of cubic feet | the 2025 magnetic meter program | Ask A, loud | every lateral (all nine carry one), if unconverted |
| HA3 register rollover | old propeller registers | Ask A, loud | five laterals, if uncarried |
| HA4 estimated heading days | flume sensor outages | Ask A shares | four shares (S4) |
| HB1 alternate-day reading | August rider cover | Ask B | three laterals (S2) |

**The cracker sheet.** The cracker filed the golden order, ran the hygiene battery (keys unique after normalising,
exact duplicates, every join matched or explained, no fan-out, counts that tie) and executed every filed rule. Every
ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 9 lateral deliveries | units converted, rollovers carried, reads differenced within each meter serial, summed by the register's lateral | each changed meter's water between its last weekly read and the swap, and between the swap and the new meter's first read, appears only in the shop log | miss |
| Ask A, 9 loss shares | the same deliveries against the headings | the same | miss |
| Ask B, 9 tail spills | the weir equation on the gauge less the structures sheet's crest | flashboards in place for part of every lateral's season, recorded only in the remarks | miss |
| Chart and call figures (recommendation block, not asks) | from the replays | carried by the main call, scored with it | outside |

Mirror leakage: 7 per cent of the ask weight (the mirror files R0 and answers both asks as the cracker does; no ask
figure couples to the call; the leakage allows for a figure a device moves by less than its bin, which the build
asserts against).

**Pair arithmetic.** Planning weights 38 recommendation (the order, the nine months, the setting year, its requirement,
the chart's named parts), 7 instruction following (the two files), 55 asks over 27 figures. The cracker keeps about 7
per cent of the ask weight: C = 38 + 7 + 3.9 = 48.9. The mirror (R0) keeps r of about 4 (the chart's form and the
files) and the same 3.9: S = 4 + 7 + 3.9 = 14.9.

Pair ceiling: 31.9

If the rubric grades the nine monthly figures as asks, the cracker keeps them and the mirror does not: C rises by about
9 and S is unchanged, a pair of about 36. Recomputed from the generated rubric when it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| WOP 2.1 to 2.4 | 1, the District's board-adopted procedure | the season, the order rule (24 of 30, whole hundreds), the replay as a weather year's 1 February to 31 October weather put on the 2027 season | where a replay starts, anything about the soil at the order date |
| WOP 3.1 to 3.5 and T1 to T4 | 1 | the daily balance, the replays' irrigation rule, what an irrigation does, the delivery | a start state, a last irrigation, the orders |
| WOP 4.1 and T5 | 1 | the loss allowances' arithmetic | a measured loss |
| WOP 5.1 | 1 | the monthly schedule | a month's figure |
| WOP 6.1, 6.2 | 1 | the weather record's splice, the fields, their versions and attributes | the winter |
| The dictionary | 4 | field semantics: order and request statuses, station quality flags, station 39's millimetres (25.4 to the inch), the meter book's units, the weir sheet's reading | how to start a replay, how to chain a meter, that boards raise a crest |

## Prompt

`prompt.txt`, gated by `voice-check.py` (in `precut.py`): the call with its unit and the forcing fact (the order due on 1
February), the workbook's call figures (the order, its monthly schedule, the setting weather year and its requirement),
the chart's named parts, the two asks per lateral with the motive (the allowances set against 2026), and the rounding
once at the close. 791 characters.

## Build record

- Generator `task138/generator/` (`build.py` runs everything): `common.py` constants and the procedure's tables,
  `weather.py` the two stations (FAO-56 Penman-Monteith ET0 from generated daily weather, the October 2026 to January
  2027 rain cut to a tenth of its climatology), `world.py` the district, the growers' sets (each field's own streams,
  its last set's date drawn first), the requests, the 2026 meters, headings and weirs, `records.py` and `docs.py` the
  files, `calc.py` the procedure and every rung, `deliver.py` the goldens and `figures.json`, `checks.py` (132,242
  assertions), `verify.py` (an independent recompute from the shipped files alone), `metadata.py`.
- The growers' irrigation answers to the fields as they are (`PHYS_*` in `common.py`, never shipped); the procedure's
  Tables 1 to 3 are the District's planning values, so a table value can move without moving a 2026 delivery or an
  ask figure.
- 18 files, 5 formats (pdf, xlsx, csv, docx, txt), the orders file 64,887 rows; distractors (metadata only): the
  groundwater levels, the 2026 crop report, the Authority's allocation notice. Two consecutive builds byte-identical
  (target, golden, `metadata.json`, `figures.json`, `target.zip`).
- Stage 4: the leak reader (pass 1, clean on Q1 to Q4) and the judge (DETERMINISTIC, APPROVE,
  `determinism_check_report.md`), then one generator pass; the reader's targeted re-read of the four changed files
  quoted nothing for Q1 to Q4, its readings close by SF26, SF27 and the filed loss share, and its realism notes (a
  tidy operations log, a regular shop log, stock request remarks) are left as minor, each further edit a document
  change for no graded figure:
  - every reading the reader raised has its fork row: SF8 gains the rain-first order of a day (202,800), SF16 its
    quoted sentence (the connector turnouts for the call), SF25 the day of the last set in the carry (203,200), SF26
    and SF27 Ask A's tail turnouts by read interval and the headings after the connector, SF28 Ask B's head with
    boards in, SF29 the judge's unit margin (202,400 and 202,800); each asserted;
  - the dictionary's station 39 entry gains "(25.4 millimetres to the inch)", a unit fact (a changed document);
  - the meter shop log gains a `New or rebuilt` column: the 14 new meters go in at 0.00 and the book reads them from
    zero, the 17 rebuilt meters keep the registers they carried out of their last service (the reader's
    random-looking registers); S2b asserted, every Ask A figure still off;
  - the request remarks say what each revision changed (all 46 revisions changed acres only, and 17 had read "method
    changed"), a withdrawal's reason fits its crop, and a few accepted requests carry an account remark or, where the
    2026 method differs, a system remark (the reader's templated remarks); asserted;
  - the operations log dates each entry the day it happened (six entries had logged later events in advance: the
    laterals' fill days, the four heading outages' ends, the closing reads), names Check 2's gate as the overshot gate
    the structures workbook lists (it read "radial"), fills the time column its header promised, adds initials and 12
    routine entries (38 against 20; the reader's evenly spaced log); the outage entries asserted against the
    headings' estimated days;
  - the stray quote characters are not a generator bug: a weir-sheet or meter-book remark carrying a comma is quoted
    as every CSV writer quotes it, every line's quotes balance and a CSV reader returns the remark whole; no change.
  Five files changed; `golden/` and `figures.json` byte-identical; `freeze.py check task138 --mode determinism` PASS.
- Gates on the final build: `precut.py` 38 checks, 0 FAIL, 0 WARN (29 fork rows); `voice-check.py` exit 0 (791
  characters); `figures_check.py` 68 figures, none absent; the container audit (`scrub_producer_metadata.py`) clean
  on `target/` and `golden/`; `guard.py validate` clean; `guard.py heart` WARN (the three draw WARNs answered under
  `## Draw`; nearest stump 0.08).
- `guard.py surface`: two promoted pairs, both on the card axes alone. task137 against task138, back to back (surface
  0.094): the decisive gap (time) and the decision type (`quantity_figure`) collide; the pattern does not (E and G14
  there, none and G16 here), and the drivers share nothing (a retention share conditioned on a repricing gap there,
  a replay started from the state at the forecast date here), so the same-puzzle test passes and the card's
  differentiation answers it; with task137 shipped (12 October) the screen rates the pair an exclusion risk, a
  shippable build against a delivered one. Main-session adjudication (12 October): a card-axis echo (the gap time
  and the decision type `quantity_figure`, which forecasting quantity calls commonly share) with a different domain,
  world, pattern and driver, surface 0.094, the same-puzzle test passing: not a clone, the card's differentiation
  answers it, and the author can still ask for `/clone-check`. task138 against task446 (surface 0.093), severity
  history (task446 is retired, rule application); the card's differentiation answers it. No persona from outside the
  card appears in the pack.
- `leak.py --asof 2027-02-01`: REVIEW, no LEAK, the same lines before and after the fix pass. Each line harmless: "the
  model" is the procedure's own name for its crop water model (WOP 3); the meter book's "37,270" is a time and a
  register read run together ("13:37,270.39"); the procedure and the working-files note carry the call's nouns
  (district, project, order, acre-feet, season) and no figure; the stump-term counts in the procedure, the note, the
  Authority's notice and the operations log are the domain's ordinary words (orders, October, record, procedure,
  station, requests, quantity, winter maintenance), none naming a start state; the yard logger's `Flag` column is its
  export's own missing-day flag, defined in the dictionary.

## Pre-ship check

1. Domain: a season's irrigation requirement read at 24 in 30 replayed weather years through a daily root-zone balance
   (crop coefficients on reference evapotranspiration, allowable depletion, rain beyond field capacity draining), the
   field's ensemble forecast run from the state at the forecast date; with another field's nouns there is no root
   zone or reference evapotranspiration for the carry-over to live in.
2. Real work, nothing planted: a weather record spliced from two stations (millimetres and inches, an overlap month,
   missing yard days), a field register re-mapped after parcel splits, revised and withdrawn requests, cancelled
   orders, turnout ids written three ways; on the ask paths new and rebuilt meter swaps, rollovers, hundred-cubic-foot
   meters, a reach re-served in mid-season, estimated flume days and flashboards in free text; each what these systems
   produce, none deciding the call.
3. The flip is a method choice: where each replayed season starts (the state the fields hold at the end of 31 January
   2027, rebuilt from the delivery record and the observed winter), not a field read, a unit or a stated rule; every
   rule in the pack is read the same on the default path.
4. The analyst test holds: full on 1 February files 189,800 set by 2003, each year's own winter 193,100, the replay
   rule run through 2026 193,800; only each field's last delivered set carried through the observed winter files
   202,700 set by 2012.
5. One defensible answer: WOP 2.3, 2.4, 3.1 to 3.5, 4.1, 5.1, 6.1 and 6.2 file the estimand, the 29 fork rows are each
   asserted, and the judge returned DETERMINISTIC, APPROVE (`determinism_check_report.md`); its residual, that no
   sentence names the start, is the decisive rung forced by WOP 3.1 and 3.4 on the record, and its unit margin is
   closed by SF29.
6. No decoy: no file states a 2027 figure, a past requirement, a start state or a schedule; the procedure files the
   balance and the replay window only; the groundwater levels, the 2026 crop report and the Authority's notice are
   declared distractors; no memo or voice argues for a start.
7. Nothing hidden and recovered: no certified figure or past order pins the start; the 2023 to 2025 orders are the
   growers' own schedules, which no planning model reproduces.
8. A new lesson: a season forecast replayed over past weather has to start from the state the system holds at the
   forecast date, rebuilt from its own delivery record, because each past season started from its own winter
   (`guard.py heart` WARN on the three draw findings answered under `## Draw`, nearest stump 0.08; `surface` promotes
   task137, now shipped, back to back on the gap and the decision type, adjudicated a card-axis echo and not a clone,
   and task446 on the card axes; both differentiated on the card).

## Tried and rejected

- The seed's loss-per-refill mixture (fill per refill plus seepage per wetted day, recovered from the 270 closed lateral
  balances): the same driver as task67 (a fixed-plus-variable cost carried per unit onto a denser period), and its
  dry-out gap was a rule recovered from a closed corpus; dropped at the draw.
- Seed 1380202 for the world: the setting year was the same on every rung, so the setting year and its requirement
  carried nothing; moved to 1380206.
- Six-inch flashboards with the board height in the structures sheet: the bare-crest spill exceeded a lateral's whole
  measured loss, so the device announced itself; cut to 2-inch boards whose height is only in the riders' remarks.
- Planning tables with even last digits (root depths in whole feet, allowable depletion fractions of 0.50): replay days
  landed exactly on an allowable depletion in most weather years, so the irrigation test was settled by floating-point
  noise and several monthly figures moved between the two tie-breaks; Tables 2 and 3 re-cut so every allowable
  depletion is an odd number of hundred-thousandths of an inch (asserted), and the walnut June coefficient set at 1.11
  to keep the months clear of their rounding edges.
- One WOP 2.4 sentence stating that a replay starts from each field's depletion at the end of 31 January, carried from
  its last delivered 2026 set (the judge's optional hardening, 12 October): refused. It names the decisive rung and
  pins the method, turning R3 into rule application; the start stays forced by WOP 3.1 and 3.4 on the record (SF9).
- Every replacement meter at a near-zero register (the reader's random-looking registers): a solver who counts a new
  meter's first read from zero would recover 307 of the 500 acre-feet the 31 swaps hide, and bench-test registers
  summing to 0.8 acre-feet on Lateral 3's two would put its delivery back in the golden's bin; kept the shop's real
  mix instead, 14 new meters at 0.00 and 17 rebuilt with their carried registers, every Ask A figure off on that
  path (S2b).
