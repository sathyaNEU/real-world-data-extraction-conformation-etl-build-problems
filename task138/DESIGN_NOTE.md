# task138: Kestrel Bend Irrigation District, the 2027 season order with the Tolan Valley Project (architecture 1, round 2)

Private, never ships. A new build (wave 2), numbered from seed FC09: the seed's world, decision and quantity are kept (an
irrigation district orders its season's water from its supplying project by 1 February, at the headgate requirement
covered in 24 of 30 replayed weather seasons through a daily soil-water model of each crop; nine laterals, 412
turnouts); its architecture (canal losses as a fill per refill plus seepage per wetted day, recovered from closed
lateral balances) is not used, because that driver is task67's fixed-plus-variable cost carried per unit onto a denser
period.

**Round 2 (2026-10-14).** The 10/10 audit found round 1 compliant but weak (`## Tried and rejected`): its stump (start
each replay from the depletion each field carries on 31 January instead of full) was the same gap as its one open fork
(no filed sentence fixed the 1 February state), and three things in the pack pointed at it. Round 2 files the start as
part of the estimand, WOP 2.4's "from its root zone as it stands at the end of 31 January", which makes round 1's golden
the default path, and moves the decisive step to how that state is rebuilt: each field's 2026 season run through the
balance on the water its delivered sets put in, which shows that the drip, micro-sprinkler and sprinkler fields were held
at a working deficit all summer and never returned to field capacity after the spring, so their last sets were not
refills. The world was rebuilt for it (the growers' irrigation by method, a wet 2025-26 winter that fills every root
zone before the 2026 season, the west spur of Lateral 5 re-fed from Lateral 6), the order is now in whole thousands of
acre-feet, the monthly schedule and the setting replay's requirement are no longer asked, and the asks carry four
figures per lateral, the shares on two independent devices.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task138.json`, architecture v1, registered 2026-10-12, edited in place at round 2 (2026-10-14) with the round 1 identity in `lineage` and no new filing stamp (the draw and its furniture date from 12 October; a fresh stamp would move this build behind task501's 14 October re-filing in draw order); `guard.py check` WARN on `repeat.gate_g` and `repeat.decision` (task137, answered below), NOTE `test.same_puzzle_older` (task126, task82) and `driver.near` (0.43 against the slot's own round 1), each differentiated on the card; `guard.py validate` clean |
| Domain / task type | physical-environmental-sciences / hydrology-flood-frequency (a client domain, its hydrology task type): a season's irrigation requirement read off an ensemble of replayed weather traces at a non-exceedance level (covered in 24 of 30), each trace run through a daily root-zone balance from the soil water each field holds at the order date |
| Objective | Forecasting & Predictive Modeling: the headgate requirement of the 2027 irrigation season (1 February to 31 October 2027), a window not yet open when the order is placed, forecast as thirty replays of past weather from the state the fields are in |
| Shape | 13 (scenarios and the flip point): the thirty weather-year replays with the order at the 24th smallest, drawn as a chart with its named parts (about 6 criteria), the order itself (1), four figures for each of the nine laterals from the 2026 records (36), the two files (2): about 45 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (acre-feet, the order in whole thousands) |
| Mechanism | gap population then time (decisive: what one row of the delivery record does to a root zone, a quantity of water reaching it at the field's efficiency rather than a refill; the time gap, the state at the forecast date, is filed and is the default path's own); pattern none; generators G3 (record against operation: the state is rebuilt from the water the record delivered, not from the replays' rule that an irrigation refills) then G16 (the season forecast conditioned on that state); Gate G `forecasting` (the thirty past seasons, read correctly, do not pin the 2027 requirement without the state the 2026 record leaves); strategy `other` (named in the card's notes: no as-of date, grain, identity or rule decides) |
| Layer 2 family / pattern | `field_method` (irrigation hydrology's water-balance tracking: a root zone's state run forward on the water applied to it at its efficiency, which is how FAO-56 tracks depletion on a field irrigated by known depths); `own:operation-record-hindcast-of-the-forecast-start-state` |
| Furniture | forum `customer_or_counterparty` (the order goes to the Tolan Valley Water Authority), forcing event `season_or_peak` (the 2027 order is due by Monday 1 February 2027), organisation family `local_government` (a California irrigation district under an elected board), role family `procurement_lead` (the water resources manager sources the district's supply), context artifact `filed_standard` (the Water Order Procedure), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | `kbid_irrigation_orders_2023-2026.csv`, the water ordering system's export: one row per irrigation set (water ordered through one turnout onto one field for one run, with its flow, start, end and status), four seasons, 107,067 rows; constructed |
| Deliverables | `kbid_order_2027.xlsx` (the order with its basis, the thirty replays, the four figures per lateral), `kbid_order_2027.svg` (the thirty replayed seasons' headgate requirements from smallest to largest with the order drawn across them) |
| People | drawn with `guard.py names --geo "United States" --seed 138`: Sherry Nixon (water resources manager, the requester), Brittany Wall (general manager), Colleen Ramsey (water master: riders, meter book, weir sheets), Dennis Zhang (SCADA and instrumentation: the heading loggers, the yard station), Travis Grimes (district engineer: structures, the Lateral 5 to 6 connector; drawn at round 2 in place of round 1's engineer, whose first name the guard WARNs against task449), Adam Arnold (Authority water accounting), Kristin Lucas (water conservation coordinator: the requests, the crop survey); none appears in the prompt |

**Guard.** `guard.py check` on the round 2 card: WARN. `repeat.gate_g` (`forecasting`, task137): the key is honest, the
past seasons read correctly do not pin the forward requirement without the state the record leaves, and task137's
mechanism (a retention share conditioned on a repricing gap) shares nothing with it. `repeat.decision`
(`quantity_figure`, task137): the decision is the seed's, an order volume. The bans ran against task130, task136 and
task137, the three builds before this one by draw order: shape `other` (both of the last two) is not used (13 here),
the forum, forcing event, organisation family, role, context artifact and strategy all differ from theirs. The round 1
card's `three_rules.strategy_risk` WARN is gone with the strategy (`time_semantics` no longer describes the decisive
step: the as-of state is filed and is the default path's).

**Same-puzzle and same-driver tests.** Decisive gap population, decisive pattern G3 (pattern none, first generator),
decision `quantity_figure`: no build in the last twelve carries the three together; task126 v1 and task82 v2 are older
carriers, differentiated on the card (task126 splits chained work records through a separate credit ledger to measure
a duration; task82 attributes checkout records under one-off keys to members through a second ledger; here nothing is
split, joined or reattributed, and the delivered water is run through a soil-water balance). Gap, pattern and Gate G
together (population, G3, forecasting): none in the last twelve. Own lineage: round 1's driver (0.43), differentiated.

**Abstraction test.** Stripped of nouns, the driver is: a forward requirement replayed over past driver traces starts
every trace from the store each unit holds at the forecast date, and the store has to be rebuilt by running each unit's
recorded replenishments through the season from the last time the record shows it full, because units run at a working
deficit are replenished by about what they used and never return to full; taking the last recorded replenishment as a
refill, starting full or spinning up on the model's own refill rule each leaves out the deficit. The nearest drivers
(`guard.py`: task117 0.05, a forward peak on per-unit caps reached through a dated join with re-timed follow-on
operations; task45 0.05, a per-holder floor measured from each holder's replenishment history and back-tested on closed
cases) share no latent structure: task45 recovers an unstated floor from a history and confirms it on a corpus, here
nothing is recovered or confirmed, the state is the balance run forward on recorded quantities. Read by idea: round 1
of this slot (the state carried from each field's last set taken as a refill) is this build's default path; task46 (a
rate law in cumulative exposure rebuilt from a movement log) indexes a rate along a curve, here the rebuilt quantity is a
simulation's initial condition.

**Data-native sentence.** Kestrel Bend's drip, micro-sprinkler and sprinkler fields (501 of the 631 on accepted 2027
requests) are irrigated to hold a working deficit through the summer, each set putting back about what the crop used
since the last, so after the spring (each was last at field capacity between 21 March and 27 May 2026) none returned to
field capacity, and each ended its last 2026 set 0.48 to 3.99 inches short (acre-weighted 2.19), while the 130 border
fields refill with every set; the wet 2025-26 winter (13.19 inches of rain from October to January, the second wettest in
the record) had every root zone full at the end of 27 January 2026, and the October 2026 to January 2027 that followed was the
driest in the district's weather record (1.36 inches against a median of 7.05 over 32 winters; all asserted). A field's
state at the order date therefore lives in the water its sets put in through the whole season (each set's ordered flow
for the hours it ran, at the field's application efficiency), not in the date of its last set.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: hazards by time since entry (134),
selection on the outcome (124), the maturity of a claims window (130), a campaign carried per untapped member (136), a
retention share conditioned on a repricing gap (137), corpus-recovered conversion rates (27, 29, 30, 78), censored
delays (31, 99), a fixed-plus-variable cost carried per unit (67, the seed's mechanism), a cumulative exposure rebuilt
from a log (46), and this slot's round 1 (the state from the last set taken as a refill): none rebuilds a forecast's
start state by running an operation's record of inputs through the season. `stumping/references/client/two-layer-task-design.md`:
Physical & Environmental Sciences has no library patterns, so the pitfall comes from the `field_method` family, here
the water-balance tracking an irrigation hydrologist runs before a season forecast. `stumping/references/client/measured-drivers.md`:
the held tasks put a construction upstream of every graded figure that the solver's hypothesis space does not hold;
here the default path already holds the as-of state and stops at the reflex that an irrigation is a refill. The seed's
header (FC09) for the world only.

**World.** Kestrel Bend Irrigation District is a California irrigation district on the east side of the San Joaquin
Valley, formed in 1921 and governed by a five-member elected board. It takes surface water from the Tolan Valley Canal
at its headgate (milepost 41.2), under a water service contract with the Tolan Valley Water Authority, the joint powers
authority that runs the Tolan Valley Project. A main canal carries the water to nine laterals, which serve 412 turnouts
and their fields (almonds, pistachios, walnuts, wine grapes, citrus, alfalfa and irrigated pasture; 648 fields in the
register, 631 of them on accepted 2027 requests for 40,309 acres: 196 drip, 255 micro-sprinkler, 50 sprinkler, 130
border). The contract quantity is 241,000 acre-feet a year. The canal runs from 1 February to 31 October and is dry from
November to January for maintenance. The Authority asks each contractor for its season's order by 1 February. The
district's Water Order Procedure (WOP, adopted 2019, revised December 2025, tables adopted each December) sets the order
at the smallest whole number of thousands of acre-feet that would have covered the season's headgate requirement in at
least 24 of the 30 weather years 1997 to 2026, each weather year's 1 February to 31 October weather run through the
procedure's daily root-zone balance for every field on the coming season's requests from its root zone as it stands at
the end of 31 January, with the lateral and main canal loss allowances on top. In June 2026 the district engineer's
connector put the west spur of Lateral 5 (turnouts 05-021 to 05-034) on Lateral 6.

As-of dates: the growers' 2027 water requests closed on 15 January 2027; the weather record and the irrigation orders
are extracted on 1 February 2027 (weather through 31 January); the 2026 meter book was closed on 30 November 2026; the
request is made on Monday 1 February 2027, and the order is due at the Authority that day.

## Default path

1. Read the Water Order Procedure: the order rule (WOP 2.3, 24 of 30, whole thousands), the replay (2.4: every field run
   day by day from its root zone as it stands at the end of 31 January, under the weather year's 1 February to 31 October
   weather), the daily root-zone balance (3.1 to 3.5: crop coefficients by month on reference evapotranspiration, rain
   beyond field capacity draining, depletion capped at the root zone's total available water, in a replay an irrigation
   at the allowable depletion returning the root zone to field capacity, delivery at the method's application
   efficiency) and the loss allowances (4.1).
2. Assemble the coming season's fields: the latest accepted 2027 request for each field, joined to the field register for
   its turnout, lateral and soil unit, and to the procedure's tables (631 fields, 40,309 acres).
3. Splice the weather record as WOP 6.1 sets it (station 39 to 30 April 2014, the yard station after, its missing days
   from station 39), station 39's millimetres in inches.
4. Build each field's root zone at the end of 31 January 2027: from the irrigation orders, its last Delivered 2026 set,
   taken as an irrigation in the procedure's sense (the field ends that day at zero depletion), then WOP 3.1's balance
   on the record's weather with Table 1's November to January coefficients to 31 January 2027 (acre-weighted 3.401
   inches, 448 of the 631 fields at or past their allowable depletion).
5. For each weather year 1997 to 2026, run every field from that state through 1 February to 31 October; sum the
   deliveries by lateral and add the loss allowances (WOP 4.1).
6. Take the 24th smallest of the thirty headgate requirements and round it up to the next thousand.

Ends on: 209,000 acre-feet (the 24th smallest requirement 208,241.37 acre-feet, the 2012 replay; asserted in `checks.py`
and recomputed by `verify.py`).
Golden: 215,000 acre-feet (the 24th smallest 214,499.45, the 2012 replay): each field's root zone at the end of 31
January 2027 rebuilt by running its 2026 season through WOP 3.1's balance from the end of 27 January 2026 (every root
zone at field capacity after the wet winter's last rain; the run converges from any earlier start) on the water its delivered sets put in,
each set's ordered flow for the hours it ran on each day times the Table 4 efficiency of the field's method, then on to
31 January 2027 (acre-weighted 4.353 inches, 598 of 631 fields at or past their allowable depletion).

## Stump sentence

A competent solver starts every replay from each field's root zone at the end of 31 January 2027 as WOP 2.4 files it,
takes each field's last delivered 2026 set as a refill to field capacity, carries it through the record's dry October to
January and files 209,000 acre-feet (Ends on); the step that lands it there is not running each field's 2026 season
through the balance on the water its delivered sets put in, from the wet winter's field capacity, which shows that the
501 drip, micro-sprinkler and sprinkler fields ended the season 0.48 to 3.99 inches short of field capacity after their
last sets: the golden is 215,000 acre-feet.

## Three rules

- **Task type:** physical-environmental-sciences, hydrology-flood-frequency (serves Forecasting): the 2027 season's
  headgate requirement read at 24 in 30 replayed weather years through a daily root-zone balance, an ensemble forecast
  of a season not yet open, run from the state the fields are in at the order date.
- **Domain test:** the deciding quantity is a season's irrigation requirement from a daily root-zone water balance (crop
  coefficients on reference evapotranspiration, allowable depletion, rain beyond field capacity draining, application
  efficiency), forecast as an ensemble of past weather traces started from the soil water each field holds on 31
  January, which an irrigation hydrologist rebuilds by tracking the balance through the season on the water actually
  applied; the field's own estimator decides the start, not a sort or a stated score.
- **Swap:** "order the warehouse's season stock at the 24th of 30 replayed demand years from each bin's stock on 31
  January, rebuilt from last year's receipts" keeps a starting store, but a store refilled by rain only up to a capacity
  set by soil and root depth, drawn down by crop evapotranspiration by month, fed at an application efficiency and held
  at a working deficit by drip irrigation has no meaning outside a root zone, so the call and its pitfall stop making
  sense.
- **Layer 1:** a weather record spliced from two stations (station 39 in millimetres to April 2014, the yard logger in
  inches after, an overlap month, the yard's missing days filled from station 39), a field register re-mapped in March
  2025 after parcel splits (former field ids on the 2023 and 2024 orders), revised and withdrawn water requests (the
  latest accepted version governs), orders cancelled before water ran, turnout ids written three ways (ordering system
  `05-031`, meter book `5-31`, GIS `T05031`), and on the ask paths meter swaps logged among the meter shop's work orders,
  register rollovers, magnetic meters registering hundreds of cubic feet, a spur re-fed from another lateral in
  mid-season, heading logger days without a total (the Water Master's estimates in the operations log), flashboards in
  the riders' weir remarks and alternate-day weir reads in August. Each is what these systems produce; none decides the
  call, and the call is unchanged with every ask file removed (asserted).
- **Layer 2:** `field_method`, the start state of an ensemble season forecast: the shortcut takes the state from each
  field's last irrigation as a refill (the replays' own idea of an irrigation); the expert tracks each field's root
  zone through the season on the water applied, which separates the border fields (refilled by every set) from the
  drip, micro-sprinkler and sprinkler fields held at a working deficit.
- **Decisive step:** rebuild each field's root zone at the end of 31 January 2027 by running its 2026 season through the
  balance on the water its delivered sets put in (each set's ordered flow for the hours it ran, at the field's
  application efficiency) from the wet winter's field capacity, instead of resetting it to field capacity at its last
  set; this moves the 31 January state from 3.401 to 4.353 inches acre-weighted and the order from 209,000 to 215,000.
- **Not semantics:** every status, unit, id, version, date and coefficient can be read correctly, and the default path
  reads them all correctly (the latest accepted requests, the Delivered sets, the splice, the 25.4 millimetres to the
  inch, the register's laterals) and still files 209,000; nothing flips on what a field, code or unit means, only on
  how the state at the order date is estimated from the record.
- **Not rule application:** no filed sentence says how to build the 31 January state, that a delivered set refills or
  does not refill a root zone, that the season should be run on the delivered water, or that the drip fields carry a
  deficit; WOP 2.4 files only what the state is (the root zone as it stands), WOP 3.4 files the replays' irrigation rule
  in its own words ("In a replay"), and executing every filed rule leaves the solver to choose an estimator, where the
  reflex (the last set as a refill) files 209,000.
- **Analyst test:** a strong analyst who reads the procedure and every file correctly, assembles the 631 fields,
  splices the weather, builds each field's 31 January state from its last delivered set taken as a refill through the
  observed winter, replays the thirty years and applies the loss allowances files 209,000 acre-feet (Ends on), six
  bins under the 215,000 the 2026 record supports; the routes the audit measured file less (full on 1 February
  196,000; each year's own winter 199,000; the replay rule run through 2026 199,000), and the near corrections still
  miss (the record run from the first set 212,000, without the efficiency 210,000, with cancelled sets 214,000); the
  easy route on the generator's clean truth files the same 209,000 and the record run 215,000 (R3a, R3b asserted).
- **Estimand:** WOP 2.3 and 2.4 in `KBID_Water_Order_Procedure_rev2025.pdf`: the smallest whole number of thousands of
  acre-feet covering, in at least 24 of the weather years 1997 to 2026, the water the headgate would take from 1
  February to 31 October 2027 if that year's 1 February to 31 October weather fell on it, every field on its latest
  accepted 2027 request (WOP 6.2) run day by day "from its root zone as it stands at the end of 31 January"; the
  population, outcome, window, unit, comparison and start state are filed, the estimator of that state is not.
- **No decoy:** no memo, briefing, past order, past requirement, soil reading or stakeholder figure states or argues a
  start state or a 2027 number; the wet winter, the working deficit on the drip and micro-sprinkler fields and the dry
  winter are the world's state, written in the orders and the weather, not defects; the three distractors (groundwater
  levels, the 2026 crop survey, the Authority's allocation notice) rank nothing.
- **No certified replay:** no past season's requirement, district balance, soil-moisture survey or published state
  ships, and the 2023 to 2025 orders are the growers' own schedules that the replays' rule does not reproduce, so the
  31 January state cannot be recovered by matching certified figures; it is built forward from the record.
- **Lesson:** an ensemble forecast started from the state at the forecast date has to rebuild that state by running the
  operation's record of what went in through the same balance, because an operation that holds its units at a working
  deficit never returns them to full, and the model's own event rule (an irrigation refills) is not the record; no build
  on file rebuilds a forecast's initial condition by tracking recorded inputs through a season (round 1 of this slot
  stopped at the last input taken as a reset, now this build's default path).

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a
reflex of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction,
ratio or half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every replay full on 1 February | WOP 2.4 names the state as it stands at the end of 31 January | no | yes (FAO-56's start after winter rain) | no | no | no | readable |
| R1 each weather year from the state its own autumn and winter left | WOP 2.4 (the state as it stands; a year contributes only its 1 February to 31 October weather) | no | yes (a modeller's spin-up) | no | no | no | readable |
| R2 the replays' irrigation rule run through 2026, then the observed winter | WOP 3.4 ("In a replay") | no | yes (a spin-up through the latest season) | no | no | no | readable |
| R2b every field full at the canal's close, then the observed winter | WOP 2.4 | no | yes (the canal closed with the fields watered) | no | no | yes (a district-wide winter deficit) | readable |
| R3 each field's last delivered set taken as a refill, then the observed winter (the default path) | WOP 2.4 asks for the state; WOP 3.4's refill reads across by analogy | the orders' status and set_end give each field's last set | yes (an irrigation resets the depletion to zero, FAO-56's full irrigation) | no | no | no | readable |
| R3c the record run from each field's first delivered set taken as a refill | no | no | yes (anchor the run at a known refill) | no | no | no | readable |
| R4g the record run on the delivered water with no efficiency | Table 4 defines the efficiency as the share the root zone receives | no | no | no | no | no | readable |
| R2d the record run with cancelled sets as water | the dictionary: a cancelled set delivered no water | the status column | no | no | yes (status filter) | no | readable |
| R4 (decisive) each field's 2026 season run through the balance on the water its delivered sets put in, from the wet winter's field capacity, to 31 January 2027 | no: WOP 2.4 names what the state is and the default path already answers it; no sentence names the season's water, a set's volume, a working deficit, the spring or a hindcast, and WOP 3.4's refill is scoped to a replay without a word on the record | no: no column holds soil water, a set's volume, a refill or a deficit; `ordered_cfs`, `set_start` and `set_end` are every order's columns, in the file the default path already reads for each field's last set | no: the reflex for an irrigation is a refill, the procedure's own replay rule says so, and the default state reconciles (every field between zero and its total available water, 448 at or past its allowable depletion) | no: no soil reading, past requirement or district balance ships; the meter book is at turnout grain on the ask paths, and scaling each set by its turnout's metered season leaves the order where it is (SF16) | no | no: per field and per day, each set's flow for the hours it ran at its efficiency through a balance floored at zero and capped, over a year of daily weather; the 31 January difference is 1.199 inches acre-weighted on the held fields and zero on the border fields, and it reaches the order through each replay's irrigation test | silent |
| O2 the golden start with the cap dropped | WOP 3.1 caps the depletion | no | no | no | no | no | readable |
| O1 the full-start replays plus the 31 January depletion as a flat addition | WOP 3.1 (a replay's rain refills part of it) | no | no | no | no | yes | readable |

The decisive rung is silent because round 2 moved the question the pack raises onto the default path: the procedure
asks for the state at the end of 31 January, and the default path builds it, from the same orders file, with the same
November to January coefficients and the same winter weather the audit named as round 1's cues. What it skips is a
question no file asks: whether the last set filled the field. The answer lives in the season's water, set by set,
and only a run of the whole season shows that the held fields never refilled after the spring.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs, then the asks' rows. `checks.py`
asserts each (the alternative computed and shown to move the call or its figures, or shown to converge). WOP is the
Water Order Procedure; T1 to T5 its tables.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the 2027 season" | deliveries at the headgate 1 February to 31 October 2027 | calendar 2027 | same call: the canal is dry 1 November to 31 January (asserted: no delivered set outside the season in any year on file) | WOP 2.1 |
| SF2 | "how much water ... order" | the smallest whole number of thousands of acre-feet covering the requirement in at least 24 of the 30 weather years (the 24th smallest, rounded up) | the interpolated 80th percentile of the thirty; the 24th rounded to the nearest thousand | the percentile converges on 215,000; the nearest thousand files 214,000 (both asserted) | WOP 2.3 ("the smallest whole number of thousands of acre-feet that would have covered") |
| SF3 | the fields | each field's latest accepted 2027 request; withdrawn requests and superseded versions out | every request row | 234,000 | WOP 6.2; the requests' Status in the dictionary |
| SF4 | a field's acres | those on its accepted 2027 request, in the replays and the record run | the register's GIS acres | 217,000 | WOP 6.2 ("Each field's crop, irrigation method and acres are those on its water request") |
| SF5 | a root zone's total available water | T3 capacity times the lesser of the T2 root depth and the T3 depth limit | no depth limit | 214,000 | WOP 3.3 |
| SF6 | the weather record | station 39 to 30 April 2014, the yard station from 1 May 2014, a day the yard did not record from station 39 | station 39 throughout; the yard from its first day (April 2014); missing yard days as zero | station 39 throughout 219,000; the yard from April converges (0.0); missing days as zero converges (-113.6) (each asserted) | WOP 6.1 |
| SF7 | a replay's days | each weather year's own 1 February to 31 October, 29 February kept in a leap year | 29 February dropped | converges (-56.4, asserted) | WOP 2.4 ("its 29 February included in a leap year") |
| SF8 | a replay day's arithmetic | previous depletion plus the day's ET less its rain, then the floor and cap, then the irrigation test at the day's end | the irrigation test before rain; the rain taken first | 216,000; rain first converges (both asserted) | WOP 3.1, 3.4 ("on any day at whose end its depletion has reached or passed") |
| SF9 | where each replay starts | each field's root zone as it stands at the end of 31 January 2027 (WOP 2.4), estimated from the record | full on 1 February (R0); each weather year's own preceding autumn and winter (R1); the replay rule run through 2026 (R2); full at the canal's close (R2b) | each files its own order (Ladder) | R0 and R2b by WOP 2.4 on the record (no rain or irrigation since the fields' last sets brought any of them to zero, and the driest winter on record added depletion); R1 by WOP 2.4 (a weather year puts only its 1 February to 31 October weather on the coming season; the start is the root zone as it stands); R2 by WOP 3.4 ("In a replay": the replays' rule is not the record, whose 2026 sets are on the orders) |
| SF10 | the water in the record | orders with status Delivered | cancelled orders counted (R2d) | 214,000 | the dictionary ("Cancelled: cancelled before water ran; no water was delivered") |
| SF11 | the water a set puts into a root zone | its delivered water times the T4 efficiency of the field's method | the delivered water whole (R4g) | 210,000 | T4 ("The share of the water delivered to a field that its root zone receives") |
| SF12 | the record run's start | field capacity at the end of 27 January 2026 (every root zone, from either November state, asserted) | field capacity on 1 February 2026; from 1 November 2025 at field capacity or at total available water; from 1 February 2023 through every season's record, former ids through the register | converges: identical states at 31 January 2027 (asserted to 1e-9; the 2025-26 winter fills every root zone) | the records converge |
| SF13 | a set's water by day | the ordered flow for the hours it ran on each day | all on the set's first day; all on its last day | converges (+3.1, -2.3, asserted) | the records converge |
| SF14 | the record's water within a day | with the day's ET and rain, then the floor and cap | after the day's floor and cap; before the day's ET and rain | converges on the order and the year (-0.2, +83.0, asserted) | the records converge |
| SF15 | a field's acres in the record run | the request acres | the register's GIS acres | converges (+242.8, asserted) | WOP 6.2; the records converge |
| SF16 | the water a set delivered | its ordered flow for the hours it ran (the dictionary: "the rider sets the turnout to it") | each set scaled by its turnout meter's season over its ordered season (0.965 to 1.032) | converges (-61.0, asserted) | the dictionary's `ordered_cfs`; the records converge |
| SF17 | a field's efficiency in 2026 | its 2027 request's method | its 2026 method | converges: every field kept its 2026 method (asserted against the crop survey) | the records converge |
| SF18 | a requested field with no 2026 delivered set | none exists | (a start for a new field) | converges (asserted: every requested field took a delivered set in 2026) | the records converge |
| SF19 | the crop through 2026 and the winter | the 2027 request's crop | the 2026 crop | converges: every requested field carries its 2026 crop (asserted) | the records converge |
| SF20 | the root-zone cap | depletion never above total available water | uncapped (O2) | 216,000 | WOP 3.1 ("never more than the root zone's total available water") |
| SF21 | the loss allowances | a lateral's water is its fields' deliveries over one less its allowance; the headgate's is the laterals' over one less the main canal's | deliveries times one plus each allowance | 212,000 | WOP 4.1 |
| SF22 | a west spur field's lateral (turnouts 05-021 to 05-034) | the register's lateral as it stands: Lateral 6 (asserted for every spur field) | Lateral 5 (the turnout number, or the feed before 15 June) | converges (-266.9, asserted) | WOP 6.2 ("as the District's field register stands when the order is calculated") |
| SF23 | ties at the order's rank | none: the 23rd (2011, 212,936), 24th (2012, 214,499) and 25th (2003, 215,850) smallest stand apart | (a tie-break) | n/a (asserted at 1,000 acre-feet) | the records converge |
| SF24 | reference evapotranspiration | the ET0 the weather record reports | recomputed from the stations' temperatures (Hargreaves) | 225,000 | WOP 3.2 ("the reference evapotranspiration the District's weather record reports for the day") |
| SF25 | rain | every inch counts until the root zone is full, the rest drains | an effective-rain fraction (75 per cent) | 219,000 | WOP 3.1 |
| SF26 | units | inches of depletion, ET and rain; acre-feet as inches times acres over 12; a cubic foot per second for an hour is 3,600 cubic feet | (none) | n/a (the model's own arithmetic reproduces each replay, asserted) | WOP 3.1, 3.5 |
| SF27 | station 39's millimetres in inches | divided by 25.4, carried unrounded | each value rounded to the yard's hundredths; 0.0394 inches per millimetre | both converge on 215,000 (-252.1, +126.6, asserted) | the dictionary ("25.4 millimetres to the inch") |
| SF28 | Ask 1 and 3: a west spur turnout's lateral on a read interval | the lateral that fed it: Lateral 5 for intervals ending at or before its 15 June read, Lateral 6 after | the register's Lateral 6 all season | Lateral 5 16,440 against 18,160 and Lateral 6 19,930 against 18,210, both shares off (asserted) | the ask's terms (a delivery counts against the heading its water passed); the operations log's 13 and 15 June entries; no water ran to the spur from 13 to 15 June and every spur meter was read on 15 June (asserted), so no interval straddles the change |
| SF29 | Ask 2 and 3: a lateral's water on a day its logger kept no total | the Water Master's estimate in the operations log | the day left out | every lateral low by 142 to 704 acre-feet (asserted) | the days without a logger total are exactly the estimated days, each a day water ran at the lateral's turnouts (asserted); the dictionary's `volume_af` ("the heading logger's daily total") |
| SF30 | Ask 1: the season's reads | from each turnout's read before 1 February to its read after 31 October | (a window inside the season) | converges: the book brackets the season at every turnout and no water ran outside it (asserted) | the records converge |
| SF31 | Ask 4: when a board change takes effect | at the reading the note sits on (each of the 24 notes timed ahead of its sheet's reading, asserted) | from the next day | Lateral 2 640, Lateral 4 280, Lateral 6 660 (asserted) | the notes' own times |
| SF32 | Ask 4: a day without a sheet | the last reading stands until the next | the day at zero | Lateral 3 410, Lateral 7 490, Lateral 8 410 (asserted) | the dictionary ("A reading stands for its day and for each following day until the weir's next reading") |
| SF33 | Ask 1: a swap's registers | the shop's `Reg. out` and `Reg. in` (new meters at 0.00, rebuilt meters with the register they carried) | (none: the registers bracket the book's reads) | converges: each removal register sits just past the old meter's last read and each installation register at or just under the new meter's first (asserted) | the records converge |
| SF34 | crediting the 2026 record to a root zone (the judge's round 2 residual: WOP never says in so many words to credit past deliveries) | the root zone as it stands at the end of 31 January 2027 is the one the record's delivered sets, the weather and the T1 coefficients left | no delivered set credited (full on 1 February, R0); a simulated 2026 season in place of the delivered sets (the replay rule run through 2026, R2) | 196,000; 199,000 | WOP 2.4 ("as it stands": a state of the fields, not of a model); the data: on the generator's clean truth the record run misses the fields as they are by 0.027 in acre-weighted, the full start by 4.33 in and the simulated season by 2.93 in (asserted); WOP 3.4's refill is scoped to a replay; no sentence is added to WOP |
| SF35 | what decides the call (the reader's round 2 Q6: the replay is filed, so the call reads as rule application) | an analytical choice: WOP 2.3 and 2.4 file the WHAT (the order rule, the start's date and that it is the fields' own state), and no filed sentence says how that state is estimated | executing the filed rules alone | (no order: the filed rules leave the 31 January state to be estimated; the easy estimator, the last set as a refill, files 209,000) | the estimand and the data: no document names a start (R3c, asserted), and on the clean truth, every rule read correctly, the two estimators of the same filed state stand a full order apart (209,000 against 215,000, R3a and R3b), the last set as a refill missing the fields as they are by 0.96 in acre-weighted (asserted) |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads them
all as the golden does. SF9 lists starts the filed estimand rules out; the two estimators of the filed state that the
ladder carries (the last set as a refill, R3, and the record run, R4) are methods, separated by the record itself: on
every one of the 501 held fields, the crop's use less rain from the day it was last full to the end of its last set
exceeds the water its sets put in by at least the depletion the record run leaves (asserted), so a refill at the last
set needs water the record never delivered. The judge's round 1 residual (the 1 February start) is closed by WHAT
(WOP 2.4), and every defensible construction of the record run (SF12 to SF17, SF22, SF27 and the converging cells of
SF6 to SF8) lands within 267 acre-feet of the golden's 24th replay, inside its thousand. The judge's round 2 residual (crediting past deliveries) and the reader's round 2 Q6 (the call as rule application) are
SF34 and SF35, each closed by the estimand and the data and asserted on the clean truth; WOP gains no method sentence
(that would file the HOW and make the decisive step rule application).

## Ladder

Every rung is a complete pipeline on the same literal estimand (WOP 2.3 and 2.4), computed by `checks.py` from the pack
(631 fields on accepted requests, 40,309 acres); the default path and the golden again by `verify.py`.

| Rung | Start of each replay | 24th smallest (AF) | Order | Setting year | Against the golden |
|---|---|---|---|---|---|
| R0 | full on 1 February | 195,251.98 | 196,000 | 2003 | -8.97 per cent |
| R2b | full at the canal's close, then the observed winter | 196,470.41 | 197,000 | 2003 | -8.41 per cent |
| R1 | each weather year's own autumn and winter | 198,331.55 | 199,000 | 2008 | -7.54 per cent |
| R2 | the replay rule run through 2026, then the observed winter | 198,546.59 | 199,000 | 2008 | -7.44 per cent |
| R3 (default) | each field's last delivered set taken as a refill, then the observed winter | 208,241.37 | 209,000 | 2012 | -2.92 per cent |
| R4g | the record run on the delivered water, no efficiency | 209,173.15 | 210,000 | 2012 | -2.48 per cent |
| R3c | the record run from each field's first delivered set taken as a refill | 211,803.48 | 212,000 | 2012 | -1.26 per cent |
| R2d | the record run with cancelled sets as water | 213,280.97 | 214,000 | 2012 | -0.57 per cent |
| R4 golden | the record run on the water each delivered set put in | 214,499.45 | 215,000 | 2012 | 0 |
| O2 | the golden start with the cap dropped | 215,619.79 | 216,000 | 2012 | +0.52 per cent |
| O1 | the full-start replays plus each field's 31 January depletion as a flat addition | 215,808.58 | 216,000 | 2003 | +0.61 per cent |

- **Separation.** Every start that reads the record less fully files less: full, own winter, canal close and the
  replays' rule 7.4 to 9.0 per cent under (asserted floors 6 to 7), the default path 2.9 (floor 2.5), the near
  corrections 0.6 to 2.5 (floors 0.4 to 2), each a full thousand or more under the order (asserted); the two
  over-corrections that break a filed rule (no cap; a flat addition that ignores each replay's own rain) file a thousand
  more. R0 to R2b also move the setting year (2003, 2008); the default path and the near corrections keep 2012, which
  is why the setting year is not asked.
- **Position.** The 24th smallest sits 499.45 acre-feet above 214,000 and 500.55 under the order (asserted between 400
  and 600), its neighbours 1,563 under (2011) and 1,351 over (2003), asserted at 1,000; every converging construction
  sits within 267 of it.
- **The decisive move.** R3 to R4 moves the 31 January state by 0.952 inches acre-weighted (1.199 on the held fields,
  none on the border fields, which refill with every set) and the order by six thousands; it reverses no rung below it
  and no single lower correction reaches it (R3c, R4g, R2d asserted).
- **Worth on the graded figures.** The call is one figure, and nothing the default path files survives on it; the
  chart's order line and its covered count move with it.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | every field on its latest accepted 2027 request (WOP 6.2), 631 fields; each took a delivered set in 2026 and carries its 2026 crop and method (SF17 to SF19 asserted); members not yet observed: none, the requests closed on 15 January and a field without an accepted request is not run (WOP 6.2) |
| 2 | Unit of account | acre-feet at the headgate; the field (one request) is the balance's unit; the order in whole thousands (WOP 2.3) |
| 3 | Attribution window | the season 1 February to 31 October (WOP 2.1); each replay the weather year's own 1 February to 31 October (2.4); the start at the end of 31 January 2027 (2.4) |
| 4 | As-of dating | the register and the requests as extracted on 1 February 2027; the weather and the orders through 31 January 2027; the state "as it stands at the end of 31 January" |
| 5 | Version basis | the latest accepted request version (WOP 6.2); the register as it stands (6.2, SF22) |
| 6 | Denominator | the loss allowances divide (WOP 4.1, SF21); no rate is estimated |
| 7 | Weighting | none: sums over fields and laterals |
| 8 | Window length | the thirty weather years 1997 to 2026 (WOP 2.3) |
| 9 | Boundary inclusivity | 1 February and 31 October inclusive; "at least 24"; "reached or passed" its allowable depletion (WOP 3.4). Every allowable depletion is an odd number of hundred-thousandths of an inch, off every lattice a day's depletion sits on; the closest approach over every day of the thirty golden replays is 5.9e-6 inch (asserted in `checks.py` and `verify.py`) |
| 10 | Rounding path | carried unrounded; the order rounded up once to the thousand (WOP 2.3); the 24th smallest 499.45 above 214,000 (asserted between 400 and 600), every converging construction within 267 of it (C1) |
| 11 | Tie-break | none needed: the 23rd, 24th and 25th smallest 1,563 and 1,351 acre-feet apart (asserted at 1,000) |
| 12 | Maturity and censoring | none: the weather has every day from October 1995 to 31 January 2027 (station 39 complete, the yard's missing days from station 39) and the 2026 orders are closed (no set runs past the canal's close, asserted) |
| 13 | Order of operations | per replay day ET and rain together, then the floor and cap, then the irrigation test (WOP 3.1, 3.4, SF8); the record's water within a day with the day's ET and rain, after the floor or before them, converges (SF14) |
| 14 | Row order | file order changes nothing (asserted: the orders file reversed files the same order and requirement) |
| 15 | Duplicate resolution | request versions: the latest accepted (SF3); orders: every order number unique (asserted) |
| 16 | Identity normalisation | the 2025 and 2026 orders and every request carry the register's field ids (asserted); the 2023 and 2024 orders' former ids map through the register (SF12); turnout id formats matter only on the ask paths |
| 17 | Netting against gross | rain and a set's water net the day's ET, floored at zero and capped (WOP 3.1, SF14); nothing else nets |
| 18 | Dimensional units | station 39 in millimetres at 25.4 to the inch, unrounded (SF27); the yard in inches; acre-inches to acre-feet over 12; cubic feet per second for hours at 3,600 cubic feet an hour (SF26) |
| 19 | Code and status semantics | request status, order status (SF10) and station quality flags are defined in the dictionary (field semantics, never the stump) |
| 20 | Integerisation | the order in whole thousands (WOP 2.3) |
| 21 | Clause scope | WOP 3.4's irrigation rule and its refill apply in a replay, its own words; the record's sets put in their water at the Table 4 efficiency (T4's definition, SF11); WOP 3.5 is a replay's delivery |
| 22 | Forward window contents | the thirty weather years' 1 February to 31 October weather, all in the record; the 2027 requests; the 31 January 2027 state from the 2026 orders and the weather to 31 January |

## Literal reader

Executed word for word, the prompt and the Water Order Procedure define the order as the smallest whole number of
thousands of acre-feet covering, in at least 24 of the 30 weather years 1997 to 2026, the water the headgate would take
from 1 February to 31 October 2027 with that year's weather on the season (WOP 2.3, 2.4), every field on its latest
accepted request (6.2) run day by day through the balance of WOP 3 "from its root zone as it stands at the end of 31
January" and carried to the headgate by 4.1. The start is a fact about each field, not a convention: the literal reader
estimates it from what the pack records, the 2026 orders (each delivered set's flow and hours; a cancelled set
delivered no water), Table 4 (the share of the delivered water the root zone receives) and the daily weather, through
the same balance (3.1). WOP 3.4's refill is a replay's ("In a replay"); no sentence says a 2026 set refilled a field.
Run on the record from any start before the 2025-26 winter (SF12), the season leaves 598 of 631 fields at or past their
allowable depletion on 31 January and files 215,000. The steps the text leaves open are the estimator of the state,
which the record separates (a refill at each held field's last set would need water the record never delivered,
asserted), and the arithmetic. Every term in the fork table resolves to one reading or converges.

## Oracles

- **None on the call path.** No past season's requirement, district balance, order, soil reading or schedule ships;
  nothing states a 2027 figure or a field's state. The 2023 to 2025 orders are the growers' own schedules (sets at the
  growers' own intervals, lengths and flows), which the replays' rule does not reproduce, so replaying 2026 and
  comparing with the orders confirms no start.
- **The WOP tables** state coefficients, depths, capacities, efficiencies and allowances: inputs every rung uses alike.
- **The meter book** measures turnouts, not fields, weekly: scaling each set by its turnout's metered season moves the
  golden 61 acre-feet and leaves the order (SF16), and the default path is not refuted by it either; it ties on every
  basis.
- **The ask paths** (the meter book, the meter shop log, the heading loggers, the operations log, the tail weir sheets,
  the structures workbook): no rung of the call reads them, and nothing in the pack states a lateral's 2026
  deliveries, water put in, loss or spill, so none ties only under the golden.

## Ask sheet

**Main call's declared row population:** every row of `kbid_water_requests_2027.xlsx`,
`kbid_field_register_2027-02-01.csv`, `station39_daily_1995-2027.csv` and `kbid_station_daily_2014-2027.csv`, the 2026
rows of `kbid_irrigation_orders_2023-2026.csv` (each delivered set's flow and hours decisive), the Water Order Procedure
and its tables. The asks' devices live in `kbid_meter_book_2026.csv`, `kbid_meter_shop_log_2026.xlsx`,
`kbid_lateral_headings_daily_2026.csv`, `kbid_canal_operations_log_2026.docx`, `kbid_tail_weir_sheets_2026.csv` and
`kbid_canal_structures.xlsx`, which no rung of the call reads; `checks.py` asserts the call unchanged with all six
removed (and the three distractors), and the four asks unchanged with the distractors removed. The register's 14 west
spur rows serve both, read the same way: the call takes their lateral as WOP 6.2 files it and converges under either
lateral (SF22); Ask 1 needs the operations log's dates, not another reading of the row (SF28). Zero device rows sit in
the call's population: the swaps, the logger outages and the boards are in files the call never opens.

The four asks, nine laterals each (36 figures), share one use, the audit trail of an input the call consumes: the
order carries each lateral's Table 5 loss allowance (WOP 4.1), and the asks are each lateral's 2026 water account from
the operating records, the measured loss that allowance stands against. Every figure is a 2026 lateral quantity on rows
outside the call's population; none is keyed to the order or its construction.

**Ask 1. Each lateral's 2026 turnout deliveries** (9 figures, acre-feet to the nearest 10).
- H18 home: the first term of each lateral's 2026 water account, the audit trail of the Table 5 allowance the order
  carries (an input reconciled to another system's total, the gap made of devices); the order uses the filed allowances
  and does not turn on it.
- Construction: each turnout's metered season from the riders' weekly reads of each meter's register, in the meter's
  own units (the 42 magnetic meters in hundreds of cubic feet, 435.6 to the acre-foot), registers that rolled over
  carried, a meter swapped in the season chained through the shop's registers at the swap (`Reg. out` less the old
  meter's last read, the new meter's first read less `Reg. in`), each read interval summed on the lateral that fed the
  turnout over it.
- Primary device (D7, the true key elsewhere, a prior-id chain): 31 turnouts, 2 to 5 on every lateral, had their meter
  swapped in mid-season; the book carries each meter's reads under its own serial, and the water between the old meter's
  last weekly read and the swap, and between the swap and the new meter's first read, appears only in the meter shop's
  work orders, among 47 routine work orders on meters left in place; 14 replacements came new at 0.00 and 17 rebuilt
  with the register they carried (the shop's `Unit` column). Differenced within each serial (the battery's habit) the
  book silently loses 18 to 79 acre-feet a lateral; differenced by turnout across a swap it picks up two unrelated
  registers (21,400 to 52,630 a lateral, loud); a new meter's first read counted from zero recovers only part of it
  (still 18 to 68 short).
- Second device on Laterals 5 and 6 (D2, an attribute at the wrong vintage): the west spur's 14 turnouts were fed from
  Lateral 5 to their 15 June reads and from Lateral 6 after (the operations log's 13 and 15 June entries); the register
  carries their current lateral, so its lateral puts the spring's water on Lateral 6 (Lateral 5 16,440 against 18,160,
  Lateral 6 19,930 against 18,210).
- Hazards: HA2 (loud) magnetic meters in hundreds of cubic feet on every lateral; HA3 (loud) seven registers roll over
  (turnouts on Laterals 1, 2, 5 and 7, one of them on the west spur).
- Path (6 files, 20 columns): the meter book (`turnout`, `meter`, `read_date`, `read_time`, `reading`, `reg_units`),
  the shop log's work orders (`Date`, `Time`, `Turnout`, `Meter out`, `Reg. out`, `Meter in`, `Reg. in`) and inventory
  (`Meter`, `Register units`, `Register capacity`), the register (`turnout_id`, `lateral`), the operations log's 13 and
  15 June entries, the dictionary.
- Stops (each computed and asserted): S1 by turnout across swaps (9 of 9 off); S2 within serial (9 of 9 off, 18 to 79
  low); S2b new meters from zero (9 of 9 off, 18 to 68 low); S3 chained on the register's lateral (Laterals 5 and 6
  off); answer. Lazy delta: S2 wrong on 9 of 9.
- Realism: meters are swapped through the season and the riders' book is kept by serial; the shop logs its swaps
  among its other jobs; a spur re-fed from a neighbouring lateral is ordinary capital work.

**Ask 2. The water put into each lateral in 2026** (9 figures, acre-feet to the nearest 10).
- H18 home: the other term of the account, the water each allowance divides (WOP 4.1).
- Construction: each heading logger's daily totals, and for each day a logger kept no total the Water Master's
  estimate from the operations log.
- Primary device (D4, absence as the signal, evidenced in a file no habitual join reaches): every heading logger lost 2
  to 5 days of the season (32 in all: power, sensors, a card fault, a firmware fault, a silted stilling well); those days
  are simply absent from the SCADA daily report, and the Water Master's estimates sit in the operations log's
  restoration entries, a Word table of free text. Summed as filed, every lateral is low by 142 to 704 acre-feet.
- Converging readings (asserted): the days without a total are exactly the estimated days, each a day water ran at the
  lateral's turnouts.
- Path (3 files, 5 columns): the headings (`date`, `lateral`, `volume_af`), the operations log (`Date`, `Entry`), the
  dictionary.
- Stops: S1 the logger totals alone (9 of 9 off); answer. Lazy delta: S1 wrong on 9 of 9.
- Realism: SCADA loggers fail and the daily report carries only what they logged; the water master's estimates live in
  the log where the outage was recorded.

**Ask 3. The share of each lateral's water put in that its turnouts did not deliver** (9 figures, per cent to one
decimal).
- H18 home: the measured loss share each Table 5 allowance is set against.
- Construction: water put in less deliveries, over water put in.
- Devices: Ask 1's chain and spur and Ask 2's absence together; no share lands unless both primaries are handled
  (asserted per lateral: the chain without the estimates files 5.7 to 12.2 against 8.1 to 14.9, the estimates without
  the chain 8.4 to 15.2, neither off too, every lateral off under each; the spur moves Laterals 5 and 6 under any).
- Stops: S1 neither device (9 of 9 off); S2 the chain only (9 of 9 off); S3 the estimates only (9 of 9 off); S4 both on
  the register's lateral (Laterals 5 and 6 off); answer. Lazy delta: S1 wrong on 9 of 9.

**Ask 4. The water that went over each lateral's tail weir in 2026** (9 figures, acre-feet to the nearest 10).
- H18 home: the operational spill within each lateral's loss, the part the allowance treats alike with seepage (a
  measure every lateral carries that the call does not turn on).
- Construction: each morning's staff gauge reading standing for its day and each day until the next (the dictionary);
  the head over the crest in place that day, the structures sheet's crest gauge reading raised 2 inches for each board
  the riders' notes put in; the sheet's weir equation (Q = C x L x H^1.5); cfs-days to acre-feet.
- Primary device (D2, an attribute at the wrong vintage): the structures sheet gives each weir as built (its crest
  gauge reading); riders set and pull 2-inch flashboards through the season to hold water in the tail reach and note
  each change only as shorthand in the day's remarks ("set 2in brd 0715", "added 2in brd 0727", "pulled 1 brd", "brds
  out 0703", each with its time), 24 notes on all nine laterals among 91 other remarks of seven kinds. Read against
  the bare crest, the boards' height counts as head, and every figure runs 1.5 to 4.9 times the golden (660 to 1,460
  against 270 to 650).
- Hazards: HB1 (D8) three laterals (3, 7 and 8) read on alternate days in August (the dictionary's standing rule; left
  at zero they file 410, 490 and 410); HB2 each board note timed ahead of its sheet's reading (taken from the next day
  instead, Laterals 2, 4 and 6 move).
- Path (3 files, 9 columns): the weir sheets (`sheet_date`, `lateral`, `read_time`, `gauge_ft`, `remarks`), the
  structures workbook's tail weirs (`Crest length L (ft)`, `Crest gauge reading (ft)`, `Coefficient C`, the weir
  equation line), the dictionary.
- Stops: S1 the bare crest (9 of 9 off); S2 boards, alternate days at zero (3 off); S3 boards from the next day (3
  off); answer. Lazy delta: S1 wrong on 9 of 9.
- Realism: tail weirs carry flashboards and riders note board changes on their sheets; the engineer's inventory holds
  the weir as built.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 the west spur re-fed | the 2026 connector | Asks 1 and 3 (Laterals 5 and 6) | four figures (S3, S4) |
| HA2 meters in hundreds of cubic feet | the 2025 magnetic meter program | Asks 1 and 3, loud | every lateral, if unconverted |
| HA3 register rollovers | old propeller registers | Asks 1 and 3, loud | four laterals, if uncarried |
| HB1 alternate-day reads | August rider cover | Ask 4 | three laterals (S2) |
| HB2 board change timing | the riders' notes | Ask 4 | three laterals (S3) |

**The cracker sheet.** The cracker filed 215,000, ran the hygiene battery (turnout ids normalised across the three
systems, exact duplicates, every join matched or explained, no fan-out, counts that tie), converted every register's
units, carried every rollover and executed every filed rule, the dictionary's standing reading included:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, 9 deliveries | reads differenced within each meter serial, units converted, rollovers carried, summed by the register's lateral | each swap's water on either side of the swap is only in the shop's work orders; the spur's spring water belongs to Lateral 5 | miss |
| Ask 2, 9 water put in | the heading loggers' daily totals summed | 32 days without a total, their estimates only in the operations log | miss |
| Ask 3, 9 shares | the two above | both, on every lateral | miss |
| Ask 4, 9 tail weir spills | the weir equation on the gauge less the structures sheet's crest, each reading standing until the next | the boards in place, noted only as shorthand in the remarks | miss |
| Chart and the order (recommendation block, not asks) | from the replays | carried by the call, scored with it | outside |

The mirror sheet (the same response stopped at R3, 209,000) differs only on the recommendation criteria: no ask couples
to the call.

Mirror leakage: 7 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation (the order, the chart's named parts, the critical components), 7
instruction following (the two files, the rounding), 55 asks over 36 figures (1.53 each). With no device cracked the
cracker keeps the method credit: C = 38 + 7 + 3.9 = 48.9; the mirror (R3) keeps r of about 4 (the files' form and the
chart's structure; the setting year, which R3 shares, is not asked): S = 4 + 7 + 3.9 = 14.9, a pair of 31.9. The most
obvious device is Ask 1's chain (a turnout's serial changes in the book, and differenced by turnout the swap throws
errors of thousands): a cracker who chains through the shop's registers fixes 7 deliveries (Laterals 5 and 6 still carry
the spur, and no share moves without Ask 2's estimates), adding 9.9 (7 figures less the credit counted): C = 58.8, a pair
of 36.8. The single device with the largest payoff is Ask 2's absence or Ask 4's boards, 9 figures each: C = 61.6, a
pair of 38.2. Both top responses on the call with no device cracked: 48.9; with one of them also cracking the chain,
53.8, which needs the decisive step held by no response.

Pair ceiling: 38.2

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| WOP 2.1 to 2.4 | 1, the District's board-adopted procedure | the season, the order rule (24 of 30, whole thousands), the replay, and its start: each field's root zone as it stands at the end of 31 January | how that state is estimated, the 2026 season's water, a last set, a deficit |
| WOP 3.1 to 3.5 and T1 to T4 | 1 | the daily balance; a replay's irrigation rule and delivery; the efficiency as the share of the delivered water the root zone receives | that a 2026 set refilled or did not refill a field; a hindcast |
| WOP 4.1 and T5 | 1 | the loss allowances' arithmetic | a measured loss |
| WOP 6.1, 6.2 | 1 | the weather record's splice; the fields, their versions and attributes | the winter; the record's water |
| The dictionary | 4 | field semantics: request and order statuses (a cancelled set delivered no water), the ordered flow (the rider sets the turnout to it), station 39's millimetres (25.4 to the inch), register units, the heading logger's daily total, the weir reading's standing rule | how to build a state, how to chain a meter, where a missing day's water is, that boards raise a crest |

## Prompt

`prompt.txt`, rewritten at round 2 and gated by `voice-check.py` (in `precut.py`, 690 characters): the call as a
question with its forcing fact (the order due on 1 February), the workbook's order, the chart's named parts, the four
figures per lateral tied to the call by the allowance the order carries for each lateral, the rounding once at the
close (the order in whole thousands, every other volume to the nearest 10 acre-feet, the shares to one decimal). The monthly schedule, the
setting year and its requirement are no longer asked (`## Tried and rejected`).

## Build record

- Generator `task138/generator/` (`build.py` runs everything): `common.py` constants, the procedure's tables and the
  growers' working targets by crop and month (never shipped), `weather.py` the two stations (FAO-56 Penman-Monteith
  ET0 from generated daily weather; the 2025-26 October to January rain at 1.9 times its draw, the October 2026 to
  January 2027 rain at a tenth of its climatology), `world.py` the district, the growers' irrigation (border fields
  refilled at each set, drip, micro-sprinkler and sprinkler fields held at their crop's working target with rain-aware
  holds, a last set on one day; each field simulated day by day from 1 February 2023 to 31 January 2027 on the yard's
  true weather), the orders, the requests, the 2026 meters, swaps and work orders, the heading loggers and their
  outages, the weirs, `records.py` and `docs.py` the files, `calc.py` the procedure and every rung, `deliver.py` the
  goldens and `figures.json`, `checks.py` (the three-rules block on the clean truth, every rung and floor, SF1 to SF35,
  the asks with every stop, the separation line, the gates and the realism sweep), `verify.py` (an independent
  recompute from the shipped files alone), `metadata.py`.
- Texture knobs, each on the ask paths only and each tuned so every ask figure sits mid-bin (asserted at 2.5 acre-feet
  and 0.02 points from every rounding edge; the nearest are 2.91 acre-feet and 0.0201 points): a calibration offset
  shared by each lateral's meters, the 2026 loss factor of each lateral, the spill scale, and the draw of which
  replacements came new (`UNIT_SALT`, redrawn so that a new meter's first read counted from zero misses on every
  lateral). None reaches a main-call file (the call is unchanged with every ask file deleted, asserted).
- 18 files, 5 formats (pdf, xlsx, csv, docx, txt), the orders file 107,067 rows; distractors (metadata only): the
  groundwater levels, the 2026 crop survey, the Authority's allocation notice. Two consecutive builds byte-identical
  (target, golden, `metadata.json`, `figures.json`, `target.zip`).
- Gates on the round 2 build (stage 3, 2026-10-14): `checks.py` 213,898 assertions; `verify.py` green (the order, the
  default path, the closest approach, the 36 lateral figures and the total row, the winter-full fact, all from the
  bundle alone); two consecutive builds byte-identical (target, golden, `metadata.json`, `figures.json`, `target.zip`);
  `precut.py` 49 checks, 0 FAIL, 0 WARN (33 fork rows); `voice-check.py` exit 0 (690 characters); `figures_check.py`
  60 figures, none absent; the container audit (`scrub_producer_metadata.py`) clean on `target/` and `golden/` with
  the floor at 2010 (the engineer's structures inventory was started in June 2012 and revised in March 2025);
  `guard.py validate` clean; `guard.py heart` WARN (`repeat.gate_g`, `repeat.decision` against task137, answered under
  `## Draw`; NOTEs differentiated); `target.zip` members equal `target/` by name, no enclosing folder.
- `guard.py surface`: two pairs promoted on the card axes alone, no surface overlap. task126 against task138 (surface
  0.080, corpus percentile 61) and task82 against task138 (0.077, percentile 51): the decisive gap (population), the
  decisive generator (G3) and the decision type (`quantity_figure`) collide. task126 splits work records a succession
  link chained, read off a separate credit ledger, to measure a duration (Descriptive, a patent office); task82
  attributes checkout records filed under one-off keys to members through a second ledger to count holders over a
  threshold (ETL, a pet retailer); here no record is split, joined or reattributed, and each field's delivered water is
  run through a soil-water balance to rebuild a forecast's start state (Forecasting, an irrigation district). Not
  clones on this reading; both are differentiated on the card, and the main session can ask for `/clone-check`. No
  persona from outside the card appears in the pack.
- `leak.py --asof 2027-02-01`: REVIEW, no LEAK, sweep 11 clean. Each line harmless: "the model" is the procedure's own
  name for its crop water model (WOP 3); "13,110" in the groundwater file is a date and a depth run together
  ("2023-10-13,110.8") and "17,370" in the meter book a time and a register ("13:17,370.64"); the procedure, the
  working-files note and the operations log carry the call's nouns (district, project, order, acre-feet, season) and no
  figure; the stump-term counts in the procedure (14), the note (6), the operations log (4) and the prompt's chart
  sentence are the domain's ordinary words (record, January, fields, weather, replay, balance, orders, winter
  maintenance), and the procedure files the start state as WHAT (WOP 2.4) without naming the record run; the yard
  logger's `Flag` column is its export's own missing-day flag, defined in the dictionary.
- Stage 4, round 2 (2026-10-14). Judge: DETERMINISTIC, APPROVE, no fix; every graded figure reproduced (the 24th replay
  2012 at 214,499, the order 215,000); Gate H analytical; stump power moderate (`determinism_check_report_round2.md`).
  Its residual, that WOP never says in so many words to credit past deliveries to the root zone, is SF34, closed by the
  estimand and the data, asserted on the clean truth; no method sentence is added to WOP. Reader: no figure handed over;
  its Q6 leaned to rule application without computing (it did not reach how the 31 January state is built), recorded
  as SF35, closed the same way. The pack, the goldens and every graded figure are unchanged (`freeze.py check --mode
  determinism` clean; `target.zip` byte-identical to the stage 3 cut).
- Realism notes from the reader, left as they are: the operations log's sensor failure and recovery pairs with the
  Water Master's estimate lists read alike because the log is the District's own standing form for an outage, and those
  entries carry the estimates Ask 2 and 3 read (SF29, the days without a logger total exactly the estimated days,
  asserted); rewording them, the shop log's repair dates or the 15 June connector entry would change a document an ask
  reads and need another reader pass for a presentation note that moves no figure. Kept for a later round if the
  portal raises realism.

## Pre-ship check

Round 2, written at stage 3 against the built pack; the reader and judge lines are stage 4's.

1. Domain: a season's irrigation requirement read at 24 in 30 replayed weather years through a daily root-zone balance,
   every replay run from each field's state at the order date, which the field's own water-balance tracking rebuilds
   from the season's applied water; with another field's nouns there is no root zone, working deficit or application
   efficiency for the start state to live in.
2. Real work, nothing planted: a weather record spliced from two stations, a field register re-mapped after parcel
   splits, revised and withdrawn requests, cancelled orders, turnout ids written three ways; on the ask paths meter swaps
   among the shop's work orders, rollovers, hundred-cubic-foot meters, a spur re-fed in mid-season, logger outages with
   the estimates in the operations log, flashboards in shorthand remarks; each what these systems produce, none deciding
   the call.
3. The flip is a method choice: how the filed state at the end of 31 January is estimated (the season run on the
   record's water against the last set taken as a refill), not a field read, a unit or a stated rule; every rule in the
   pack is read the same on the default path.
4. The analyst test holds: the default path files 209,000, the audit's routes 196,000 to 199,000, the near corrections
   210,000 to 214,000; only the record run files 215,000 (and on the generator's clean truth the same two figures).
5. One defensible answer: WOP 2.3, 2.4, 3.1 to 3.5, 4.1, 6.1 and 6.2 file the estimand, the start state included; the 35
   fork rows are each asserted; every defensible construction of the record run lands within 267 acre-feet of the 24th
   replay, 499 from either edge of its thousand.
6. No decoy: no file states a 2027 figure, a past requirement, a field's state or a schedule; the groundwater levels, the
   crop survey and the Authority's notice are declared distractors; no memo or voice argues for a start.
7. Nothing hidden and recovered: no certified figure or past order pins the state; it is built forward from the record.
8. A new lesson: a forecast's initial condition rebuilt by tracking an operation's recorded inputs through the season,
   because a unit held at a working deficit never returns to full; round 1's last-input-as-reset is this build's default
   path.
9. Leak reader (stage 4): nothing quoted that hands over a figure; its Q6 lean to rule application is SF35 (no filed
   sentence builds the 31 January state; the two estimators separate on the clean truth); REVIEW lines harmless.
10. Judge (stage 4): DETERMINISTIC, APPROVE, no fix; Gate H analytical; the residual is SF34, closed without a WOP
   sentence.

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
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK, 2026-10-14), because its stump (each replay started
  from the depletion each field carried on 31 January, from its last set taken as a refill, against a full start) was the
  same gap as the judge's one open fork (no filed sentence fixed the 1 February state, so the DETERMINISTIC verdict was
  conditional on it), the decisive step was visible (the 64,887-row orders file the one large non-distractor file the
  default path never read, Table 1's November to January coefficients, the weather run to 31 January 2027; the judge and
  the reader both found it unprompted), and Ask A's meter chaining was crackable through the shop log's registers with no
  second device on the figures it moved.
- Filing the start state (WOP 2.4) on round 1's world: the literal estimand made round 1's golden the default path with
  nothing left to decide (every field's last set had refilled it in that world); the growers were rebuilt so the drip,
  micro-sprinkler and sprinkler fields are held at a working deficit, which only the record's water shows.
- An unscoped sentence that an irrigation returns the root zone to field capacity (round 1's WOP 3.4): its literal
  execution on the 2026 sets is the default path (a filed sentence whose literal reading gives the easy answer, a
  main-call fork); scoped to the replays ("In a replay").
- Filing a field-capacity start on 1 February 2026, or the record run itself: names the method (rule application); left
  to the data (SF12, the run converges from any start before the wet winter).
- Grading the monthly schedule (WOP 5.1): R3's monthly shares matched the golden's from May to September, five of nine
  months free to the default path; dropped from the prompt.
- Grading the setting replay's requirement to the nearest 10 or 100 acre-feet: defensible constructions of the record
  run (SF13 to SF16, SF22, SF27) move it by up to 267 acre-feet, across those bins; dropped, and the order moved to whole
  thousands so every construction lands in one bin.
- Asking for the setting weather year: the default path and every near correction also land on 2012, a free criterion
  for the mirror; dropped.
- The Lateral 5 tail reach (05-045 to 05-058) re-served through a connector: replaced by the west spur (05-021 to
  05-034), every spur meter read on the change day and no water across it, so the as-of assignment converges.
- A heading logger cutover (a clock change in mid-season) as Ask 2's device: it moved only the days at the season's
  edges and announced itself in the daily series; replaced by the logger outages whose estimates sit in the operations
  log.
- Closing SF14 (the record's water within a day) by an evening convention: abandoned; the three orders of a day converge
  on the order and the year (asserted).
- `UNIT_SALT` 0 (the first draw of which replacements came new): a new meter's first read counted from zero landed
  Lateral 2's deliveries in the golden's bin (1.5 acre-feet off); redrawn (14), every lateral 18 acre-feet or more off.
- Cancelled sets placed after a field's last set and allowed to run past 31 October: two 2026 orders ended on 1
  November, a set the ordering system would not take after the canal's close; such a set is no longer placed.
- The asks' motive as round 1 worded it ("Our loss allowances will be set against what the laterals did in 2026"): it
  named a later decision with another owner (the Board's next allowances), the H18 defect; retied to the call as the
  audit trail of the allowance the order carries for each lateral.
- The record run started at field capacity on 1 February 2026 and the golden's note saying the winter had every root zone
  full then: four dry days after the 27 January rain left every field up to 0.17 inches short on 1 February, so the note
  was not true of the record (H6); the run now starts from the end of 27 January 2026, when every root zone was full
  from any November state (asserted), and files the same state on 31 January 2027.
- A WOP sentence crediting each field's 2026 delivered sets to its root zone, to answer the judge's round 2 residual:
  refused. It files the HOW, the decisive step's own estimator, and turns the record run into rule application; the
  residual is closed by the estimand and the data instead (SF34, asserted on the clean truth).
