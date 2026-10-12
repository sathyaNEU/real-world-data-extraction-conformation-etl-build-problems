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
| Shape | 02 (forecast across many periods): the order and its monthly schedule (February to October, nine months), the weather year whose replay sets the order and that replay's requirement, the exceedance chart's named parts, and two asks on 2026 rows the call never reads (each lateral's 2026 balance; the main canal by month); about 60 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (acre-feet, the order in whole hundreds) |
| Mechanism | gap time (decisive: the replays are statements about past seasons, each of which began from whatever its own winter left in the soil; the order bets on a season that begins from a known, depleted state); pattern none, generators G16 (method selection: a season forecast conditioned on the state at the forecast date against an unconditioned replay of past seasons) then G3 (record against operation: that state is rebuilt from the delivery record, not from the model's own irrigation rule); Gate G `forecasting` (the thirty past seasons, read correctly, do not pin the 2027 requirement without the antecedent state); strategy `time_semantics` (F1: the as-of state at the forecast date, a clock already in the data, time since each field's own last irrigation) |
| Layer 2 family / pattern | `field_method` (hydrologic forecasting's own method: an ensemble of historical weather traces run from the current initial conditions, as in ensemble streamflow prediction); `own:antecedent-state-conditioned-season-replay` (Physical & Environmental Sciences has no library patterns; the nearest library line, urban-regional-science/forecasting/1, teaches features known as of the forecast origin, and here the origin's state has to be rebuilt) |
| Furniture | forum `customer_or_counterparty` (the order goes to the Tolan Valley Water Authority, the supplying project), forcing event `season_or_peak` (the 2027 season's order is due by Monday 1 February 2027, the day the canal opens), organisation family `local_government` (a California irrigation district, a special district under an elected board), role family `procurement_lead` (the water resources manager sources the district's supply), context artifact `filed_standard` (the district's Water Order Procedure, adopted by the board), calibration `none` (the delivery history and the closed lateral balances are the district's own records, not an organ), opening `question-first`, question form `how-much` |
| Spine | `kbid_irrigation_orders_2023-2026.csv`, the district's water ordering system export: one row per irrigation set (water ordered through one turnout onto one field for one run, with its status), four seasons; constructed |
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

**Data-native sentence.** Kestrel Bend's growers stop irrigating at harvest, so most fields took their last 2026 water in
September or early October, weeks before the canal closed for the winter on 31 October, and the autumn and early winter
that followed were among the driest in the district's weather record; each field therefore enters the 2027 season short
of field capacity by an amount set by its crop, its soil and the date of its own last set, an amount that lives only in
the irrigation orders and the daily weather, and that none of the thirty past seasons the procedure replays ever
started from.

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
serve 412 turnouts and about 600 fields (some 37,000 irrigated acres: almonds, pistachios, walnuts, wine grapes, citrus,
alfalfa and irrigated pasture). The canal runs from 1 February to 31 October and is dry from November to January for
maintenance. The Authority asks each contractor for its season's order by 1 February. The district's Water Order
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

Ends on: about 174,000 acre-feet (design-stage estimate on a prototype; the build recomputes and asserts it).
Golden: about 184,000 acre-feet: every replay starts from the depletion each field carries at the end of 31 January
2027, built from its last 2026 delivery (the orders) through the observed autumn and winter weather with the same
daily balance.

## Stump sentence

A competent solver assembles the 2027 fields, splices the weather record, replays the thirty weather years through the
procedure's daily root-zone balance with every field at field capacity on 1 February, adds the loss allowances and
files about 174,000 acre-feet (Ends on); the step that lands it there is not starting each replay from the depletion
each field actually carries on 31 January 2027, which most fields built from a last set in September or early October
through the driest autumn and early winter on record: the golden is about 184,000.

## Three rules

- **Domain test:** the deciding quantity is a season's irrigation requirement from a daily root-zone water balance (crop
  coefficients on reference evapotranspiration, allowable depletion, rain beyond field capacity draining), forecast as
  an ensemble of past weather traces started from the soil water each field holds when the order is placed, which is
  how an irrigation hydrologist conditions a season's water forecast on its antecedent state; with another field's
  nouns there is no root zone, field capacity or reference evapotranspiration for the carry-over to live in.
- **Analyst test:** a strong analyst who reads the procedure and every file correctly, takes the latest accepted
  requests, splices the weather record, replays the thirty weather years field by field and applies the loss
  allowances still starts every replay with the root zone full (about 174,000 acre-feet), or lets each weather year
  start from the state its own past winter left (about 177,000), or runs the planning model through 2026 with its own
  irrigation rule, which keeps watering every field into late October, before carrying the state forward (about
  175,000); each is several thousand acre-feet short of the season the fields will actually start (design-stage
  estimates).
- **Layer 1:** a weather record spliced from two stations (station 39 in millimetres to April 2014, the district
  station in inches after, an overlap month and missing days filled from station 39), a field register re-mapped after
  2025 parcel splits (old field numbers on the 2023 and 2024 orders), revised water requests (the latest accepted
  version governs), orders cancelled before water ran, turnout ids written three ways (the ordering system, the meter
  book, the GIS register), and on the ask paths a meter book with meter changes and register rollovers, a lateral tail
  reach re-served from another lateral in mid-season, a headgate flume logged in Pacific Standard Time all year and
  re-rated after a cleanout. Each is something these systems produce; none decides the call.
- **Layer 2:** the shortcut is to replay past seasons as they were (start full, or start where each past winter left
  the soil); the expert runs the ensemble from the state the system is in at the forecast date, rebuilt field by field
  from the delivery record and the observed weather with the same balance the replays use.

## Tried and rejected

- The seed's loss-per-refill mixture (fill per refill plus seepage per wetted day, recovered from the 270 closed lateral
  balances): the same driver as task67 (a fixed-plus-variable cost carried per unit onto a denser period), and its
  dry-out gap was a rule recovered from a closed corpus; dropped at the draw.
