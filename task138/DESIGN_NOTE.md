# task138: Kestrel Bend Irrigation District, the 2027 season order with the Tolan Valley Project (architecture 1, round 3)

Private, never ships. A new build (wave 2), numbered from seed FC09: the seed's world, decision and quantity are kept (an
irrigation district orders its season's water from its supplying project by 1 February, at the headgate requirement
covered in 24 of 30 replayed weather seasons through a daily soil-water model of each crop; nine laterals, 412
turnouts); its architecture (canal losses as a fill per refill plus seepage per wetted day, recovered from closed
lateral balances) is not used, because that driver is task67's fixed-plus-variable cost carried per unit onto a denser
period.

**Round 3 (2026-10-15), the rule 3 rework.** The rule 3 audit failed round 2 as rule application (`## Tried and
rejected`): its start state was the procedure's own daily balance (WOP 3.1 to 3.3) executed on the 2026 delivery record
at Table 4's efficiency, which the table then defined as the share of a field's delivered water its root zone receives,
so the filed sentences executed word for word gave the golden with nothing left to estimate. Round 3 keeps the world,
the order rule (WOP 2.3), the replay model and the estimand sentence (WOP 2.4, "from its root zone as it stands at the end
of 31 January"), and makes the start an estimate: Table 4 is now the design efficiency WOP 3.5's replays use and nothing
else, no filed sentence says what share of the record's water reached a root zone, and the District's soil moisture
network (eleven capacitance-probe stations on cooperating growers' almond, vine, pasture and alfalfa blocks, daily
readings from December 2025 to January 2027) ships as the evidence. A drip, micro-sprinkler or sprinkler set that puts
back only part of the deficit loses little below the root zone, so the record's water reached the root zones at about 4
per cent more than Table 4 allows; the stations' season shows it set by set, while their 31 January readings are the
same under any efficiency (the dry autumn took every drip, micro-sprinkler and sprinkler station to the bottom of its
root zone, and a border set runs past field capacity). The growers still size their sets on Table 4, so the 2026 record and
every ask file are byte for byte round 2's; the order moves from 215,000 to 212,000, and 215,000 is now the default
path's answer.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task138.json`, architecture v1, registered 2026-10-12, edited in place at rounds 2 and 3 with each earlier identity in `lineage` and no new filing stamp (the draw and its furniture date from 12 October); `guard.py check` answered below; `guard.py validate` clean |
| Domain / task type | physical-environmental-sciences / hydrology-flood-frequency (a client domain, its hydrology task type): a season's irrigation requirement read off an ensemble of replayed weather traces at a non-exceedance level (covered in 24 of 30), each trace run through a daily root-zone balance from the soil water each field holds at the order date |
| Objective | Forecasting & Predictive Modeling: the headgate requirement of the 2027 irrigation season (1 February to 31 October 2027), a window not yet open when the order is placed, forecast as thirty replays of past weather from the state the fields are in |
| Shape | 13 (scenarios and the flip point): the thirty weather-year replays with the order at the 24th smallest, drawn as a chart with its named parts (about 6 criteria), the order itself (1), four figures for each of the nine laterals from the 2026 records (36), the two files (2): about 45 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (acre-feet, the order in whole thousands) |
| Mechanism | gap population then time (decisive: what the monitored blocks say about the unmonitored ones, a process parameter of the irrigation method that transfers, not the state the blocks hold; and when it shows, through the irrigation season, not at the order date, when every station's state is the same under any efficiency); pattern none; generators G3 (record against operation: the record's delivered water against what the operation put into the root zones, as the stations measure it, not the design efficiency) then G13 (horizon: the evidence speaks for the season the sets ran in, not the order date); Gate G `forecasting` (the thirty past seasons, read correctly, do not pin the 2027 requirement without the state the record leaves at the share the stations' season shows); strategy `other` (named in the card's notes) |
| Layer 2 family / pattern | `field_method` (irrigation hydrology's soil-water balance calibrated against soil moisture monitoring and carried to the unmonitored fields by its parameter, the way a hydrologist regionalises a model from gauged to ungauged catchments); `own:monitored-season-calibration-carried-through-each-units-record` |
| Furniture | forum `customer_or_counterparty` (the order goes to the Tolan Valley Water Authority), forcing event `season_or_peak` (the 2027 order is due by Monday 1 February 2027), organisation family `local_government` (a California irrigation district under an elected board), role family `procurement_lead` (the water resources manager sources the district's supply), context artifact `filed_standard` (the Water Order Procedure), calibration `physical_verification` (the soil moisture stations' readings), opening `question-first`, question form `how-much` |
| Spine | `kbid_irrigation_orders_2023-2026.csv`, the water ordering system's export: one row per irrigation set (water ordered through one turnout onto one field for one run, with its flow, start, end and status), four seasons, 107,067 rows; constructed |
| Deliverables | `kbid_order_2027.xlsx` (the order with its basis, the thirty replays, the four figures per lateral), `kbid_order_2027.svg` (the thirty replayed seasons' headgate requirements from smallest to largest with the order drawn across them) |
| People | drawn with `guard.py names --geo "United States" --seed 138`: Sherry Nixon (water resources manager, the requester), Brittany Wall (general manager), Colleen Ramsey (water master: riders, meter book, weir sheets), Dennis Zhang (SCADA and instrumentation: the heading loggers, the yard station), Travis Grimes (district engineer: structures, the Lateral 5 to 6 connector), Adam Arnold (Authority water accounting), Kristin Lucas (water conservation coordinator: the requests, the crop survey, the soil moisture network); none appears in the prompt |

**Guard.** `guard.py check` on the round 3 card: WARN, no BLOCK. The bans ran against task130, task136 and task137, the
three builds before this one by draw order. A decisive G16 was refused (`ban.pattern`, task136 decides on G16, and
gap population with G16 is spent in four older builds), so the card names the mechanism by its other honest reading,
G3 then G13 (the record against what the operation put into the root zones, and the season against the order date).
`repeat.gate_g` (`forecasting`, task137) and `repeat.decision` (`quantity_figure`, task137) are round 2's, answered
there: the forecast key is honest and the decision is the seed's order volume. `people.last` and `people.first`
(Grimes, Adam against task457): this build drew Travis Grimes and Adam Arnold on 12 October; task457, drawn 14 October,
carries those names among its faculty; answered on the card. The calibration form `physical_verification` is none of
the three builds'. NOTEs (task126, task82, this slot's rounds 1 and 2) are differentiated on the card.

**Same-puzzle and same-driver tests.** Decisive gap population, pattern none, decisive generator G3, decision
`quantity_figure`, Gate G `forecasting`: no build in the last twelve carries the gap, the pattern and the decision
together, or the gap, the pattern and Gate G; task126 v1 and task82 v2 are older carriers of the first three,
differentiated on the card (neither fits a physical parameter on a monitored season nor carries it through each unit's
record). Own lineage: round 2's driver (the record run at Table 4, now this build's default path) and round 1's (the last
set as a refill, now a lower rung), each differentiated on the card.

**Abstraction test.** Stripped of nouns, the driver is: a forward requirement replayed over past driver traces starts
from each unit's store at the forecast date, rebuilt by running each unit's recorded inputs through the balance at the
share of each input that reaches the store; the design share is not the record's, and only the monitored units'
readings through the input season identify the record's share, because at the forecast date every monitored unit's
store is the same under any share; carrying the design share, the monitored units' end-point readings, their
offset or their share of capacity to the unmonitored units misstates the units replenished late in the season, on which
the order turns. The nearest drivers on file (`guard.py nearest`: this slot's rounds; task46, a rate law in cumulative
exposure rebuilt from a movement log; task181, each route's own reporting delay against a pooled nowcast) share no
latent structure: task46 indexes a rate along a constructed exposure and task181 completes counts by route; here a
physical parameter is fitted on a monitored season and carried through every unit's own record of inputs.

**Data-native sentence.** The driest October to January in the District's weather record (1.36 inches against a median
of 7.05 over 32 winters) took the root zones the soil moisture network's drip, micro-sprinkler and sprinkler stations
watch to the bottom whatever share of the season's water had reached them (the almond and vine blocks, last watered in
September, between 6 and 23 October; the shallow sprinkler pastures, watered to late October, by 6 January), and the
border stations' last sets ran past field capacity under any share, so every station reads the same on 31 January
whatever the share; the late blocks (100 pistachio, 51 citrus and 44 walnut fields and the sprinkler alfalfa) carry
14,290 of the 16,850 acre-inches the share moves on 31 January (pistachios at 0.52 of total available water against 0.73
under Table 4, citrus 0.51 against 0.68, walnuts 0.59 against 0.70), and the stations' readings through the 2026 season
show that share set by set: about 4 per cent above Table 4's design efficiency at every drip, micro-sprinkler and
sprinkler station (all asserted).

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: hazards by time since entry (134),
selection on the outcome (124), the maturity of a claims window (130), a campaign carried per untapped member (136), a
retention share conditioned on a repricing gap (137), corpus-recovered conversion rates (27, 29, 30, 78), censored
delays (31, 99), a fixed-plus-variable cost carried per unit (67, the seed's mechanism), a cumulative exposure rebuilt
from a log (46), each route's delay against a pooled nowcast (181), and this slot's rounds 1 and 2 (the last set as a
refill; the record at the design efficiency): none fits a process parameter on a monitored season and carries it through
each unit's own record. `stumping/references/client/two-layer-task-design.md`: Physical & Environmental Sciences has no
library patterns, so the pitfall comes from the `field_method` family, here the calibration of a soil-water balance on
soil moisture monitoring that an irrigation hydrologist runs before trusting a model's start state.
`stumping/references/client/measured-drivers.md`: the held tasks put a construction upstream of every graded figure that
the solver's natural check passes; here the natural check, the stations' readings at the order date, passes the wrong
efficiency because the dry autumn erased the efficiency from every station's state. The seed's header (FC09) for the world only.

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
connector put the west spur of Lateral 5 (turnouts 05-021 to 05-034) on Lateral 6. Water Conservation runs an irrigation
scheduling program whose soil moisture network (eleven stations put in during 2024 under the state's on-farm water
conservation grant, on cooperating growers' almond, vine, pasture and alfalfa blocks) logs each station's profile water
at local midnight; the program's platform exports the sites and the daily readings.

As-of dates: the growers' 2027 water requests closed on 15 January 2027; the weather record, the irrigation orders and
the soil moisture network are extracted on 1 February 2027 (weather and readings through the end of 31 January); the
2026 meter book was closed on 30 November 2026; the request is made on Monday 1 February 2027, and the order is due at
the Authority that day.

## Default path

1. Read the Water Order Procedure: the order rule (WOP 2.3, 24 of 30, whole thousands), the replay (2.4: every field run
   day by day from its root zone as it stands at the end of 31 January, under the weather year's 1 February to 31 October
   weather), the daily root-zone balance (3.1 to 3.3: crop coefficients by month on reference evapotranspiration, rain
   beyond field capacity draining, depletion capped at the root zone's total available water), the replays' irrigation
   rule and delivery (3.4, 3.5, at Table 4's efficiency) and the loss allowances (4.1).
2. Assemble the coming season's fields: the latest accepted 2027 request for each field, joined to the field register for
   its turnout, lateral and soil unit, and to the procedure's tables (631 fields, 40,309 acres).
3. Splice the weather record as WOP 6.1 sets it (station 39 to 30 April 2014, the yard station after, its missing days
   from station 39), station 39's millimetres in inches.
4. Build each field's root zone at the end of 31 January 2027: its 2026 season run through the WOP 3.1 balance from
   field capacity after the wet winter, each delivered set's ordered flow for the hours it ran putting its water in at
   the Table 4 efficiency of the field's method (WOP 3.5's efficiency read across to the record), then the dry winter
   (acre-weighted 4.353 inches).
5. Check that state against the soil moisture network: join each station to its field through the parcel number, read
   each midnight reading as the end of the day before, and compare the 31 January readings (full point less profile
   water) with the run: all eleven stations within 0.094 inches of it.
6. For each weather year 1997 to 2026, run every field from that state through 1 February to 31 October; sum the
   deliveries by lateral and add the loss allowances (WOP 4.1); take the 24th smallest of the thirty headgate
   requirements and round it up to the next thousand.

Ends on: 215,000 acre-feet (the 24th smallest requirement 214,499.45 acre-feet, the 2012 replay; asserted in `checks.py`
and recomputed by `verify.py`).
Golden: 212,000 acre-feet (the 24th smallest 211,561.96, the 2012 replay): each field's 2026 season run on the water its
delivered sets put in at the share of it that reached the root zone as the stations' 2026 readings show it for the
field's method (each drip, micro-sprinkler and sprinkler station's season fitted by least squares on its own sets, the
method's stations averaged: drip 0.9353, micro-sprinkler 0.8822, sprinkler 0.7811; border at Table 4), from field
capacity at the end of 27 January 2026 to the end of 31 January 2027 (acre-weighted 3.935 inches, 535 of 631 fields at
or past their allowable depletion).

## Stump sentence

A competent solver builds each field's root zone at the end of 31 January 2027 by running its 2026 season through the
procedure's balance on the water its delivered sets put in at the Table 4 efficiency, finds every soil moisture
station's 31 January reading within 0.094 inches of that run, and files 215,000 acre-feet (Ends on); the step that lands
it there is taking Table 4's design efficiency as the share of the record's water that reached the root zones and
checking it at the order date, when the dry autumn and winter have left every station's state the same under any
efficiency: the stations' readings through the 2026 season, set by set, put that share above Table 4 at every drip,
micro-sprinkler and sprinkler station, and carried through every field's own record it leaves the late pistachio,
citrus, walnut and alfalfa blocks wetter: the golden is 212,000 acre-feet.

## Three rules

- **Task type:** physical-environmental-sciences, hydrology-flood-frequency (serves Forecasting): the 2027 season's
  headgate requirement read at 24 in 30 replayed weather years through a daily root-zone balance, an ensemble forecast
  of a season not yet open, run from the state the fields are in at the order date.
- **Domain test:** the deciding quantity is each field's root zone at the order date, the initial condition of a daily
  soil-water balance (crop coefficients on reference evapotranspiration, rain beyond field capacity draining, depletion
  capped at total available water), which an irrigation hydrologist estimates by calibrating the balance's application
  efficiency against soil moisture monitoring over the season the water went on and carrying that parameter through
  every unmonitored field's own record of applied water; no sort, filter or stated score decides it.
- **Swap:** "order a warehouse's season stock at the 24th of 30 replayed demand years from each bin's stock on 31
  January, the receipts' fill rate fitted on a dozen counted bins" keeps a fitted rate, but a store drawn down by crop
  evapotranspiration by month, refilled by rain only to a capacity set by soil and root depth, fed at an application
  efficiency that a deficit set raises, and emptied to the bottom of its root zone by a dry autumn on the monitored
  drip, micro-sprinkler and sprinkler blocks, has no meaning outside a root zone, so the call and its pitfall stop making sense.
- **Layer 1:** a weather record spliced from two stations (station 39 in millimetres to April 2014, the yard logger in
  inches after, an overlap month, the yard's missing days filled from station 39), a field register re-mapped in March
  2025 after parcel splits (former field ids on the 2023 and 2024 orders), revised and withdrawn water requests (the
  latest accepted version governs), orders cancelled before water ran, turnout ids written three ways (ordering system
  `05-031`, meter book `5-31`, GIS `T05031`), the soil moisture platform's export (stations keyed to the register only by
  the parcel number written without its dashes, readings stamped in UTC at local midnight across both daylight saving
  changes, two logger gaps, profile depths and full points in the site sheet), and on the ask paths meter swaps logged
  among the meter shop's work orders, register rollovers, magnetic meters registering hundreds of cubic feet, a spur
  re-fed from another lateral in mid-season, heading logger days without a total (the Water Master's estimates in the
  operations log, in each writer's own words), flashboards in the riders' weir remarks and alternate-day weir reads in
  August. Each is what these systems produce; none decides the call (the UTC date read as the day files the same order,
  asserted), and the call is unchanged with every ask file removed (asserted).
- **Layer 2:** `field_method`, the calibration of a model's initial condition on monitoring: the share of the record's
  water that reached the root zones is a parameter of the irrigation method, fitted on the stations' 2026 season where
  the sets act and carried through every field's own record; the shortcut takes the design value (Table 4) and checks it
  at the order date, where the dry autumn has erased the efficiency from every station's state, or carries the
  stations' January state, offset or share to the late blocks, whose state still turns on it.
- **Decisive step:** fit the application efficiency on each drip, micro-sprinkler and sprinkler station's 2026 readings
  (least squares on its own sets through the season), average it by method, and run every field's 2026 record with its
  method's efficiency, instead of the Table 4 design value or the stations' 31 January readings; this moves the 31
  January state from 4.353 to 3.935 inches acre-weighted (pistachios from 0.73 to 0.52 of total available water, citrus
  0.68 to 0.51, walnuts 0.70 to 0.59) and the order from 215,000 to 212,000.
- **Not semantics:** every status, unit, id, version, date, time stamp and coefficient can be read correctly, and the
  default path reads them all correctly (the latest accepted requests, the Delivered sets, the splice, 25.4 millimetres
  to the inch, the parcel number join, local midnight as the end of the day before, each station's full point less its
  profile water as its depletion, Table 4 as WOP 3.5's design efficiency) and still files 215,000; nothing flips on what
  a field, code or unit means, only on how the record's efficiency is estimated and where it is checked.
- **Not rule application:** no filed sentence gives the share of the record's water that reached a root zone or says
  how the 31 January state is estimated; WOP 2.4 files what the state is (the root zone as it stands), WOP 3.1 to 3.3 the
  balance's crop water use and bounds, WOP 3.4 and 3.5 a replay's irrigation and its delivery at Table 4, and Table 4's
  note ties it to WOP 3.5. Executing every filed sentence with Table 4 read across to the record files 215,000; the step
  no filed rule performs, fitting the efficiency on the stations' season and carrying it to every field, files 212,000.
- **Analyst test:** a strong analyst who reads the procedure and every file correctly, assembles the 631 fields,
  splices the weather, runs each field's 2026 record through the balance at the Table 4 efficiency, checks the result
  against the eleven stations' 31 January readings (all within 0.094 inches) and replays the thirty years files 215,000
  acre-feet (Ends on), three bins over the 212,000 the stations' season supports; the stations' January readings used on
  their own fields file 215,000 too, an offset by method 215,000, their share of total available water on every field
  218,000, a fitted model on the obvious covariates (the last set's day, the January crop coefficient, the method)
  216,000, the efficiency kept to the stations' crops 214,000, the last set as a refill 209,000, all of the record's
  water 210,000 and the routes the audit measured less (full on 1 February 196,000; each year's own winter 199,000); on
  the generator's clean truth the default files the same 215,000 and the stations' efficiency 212,000 (R3a, R3b
  asserted).
- **Estimand:** WOP 2.3 and 2.4 in `KBID_Water_Order_Procedure_rev2025.pdf`: the smallest whole number of thousands of
  acre-feet covering, in at least 24 of the weather years 1997 to 2026, the water the headgate would take from 1
  February to 31 October 2027 if that year's 1 February to 31 October weather fell on it, every field on its latest
  accepted 2027 request (WOP 6.2) run day by day "from its root zone as it stands at the end of 31 January"; the
  population, outcome, window, unit, comparison and start state are filed, the estimator of that state is not.
- **No decoy:** no memo, briefing, past order, past requirement, efficiency or stakeholder figure states or argues a
  start state, an efficiency or a 2027 number; the stations are the conservation program's monitoring, accurate to their
  reading noise, and their January readings agree with the Table 4 run because the dry autumn took each drip,
  micro-sprinkler and sprinkler station to the bottom of its root zone and each border station's last set ran past
  field capacity (they agree as well with the golden, and with every efficiency up to each station's own:
  asserted), not because anything was placed there; the three distractors (groundwater levels, the 2026 crop survey,
  the Authority's allocation notice) rank nothing.
- **No certified replay:** no past season's requirement, district balance, published efficiency or certified state
  ships; the efficiency is fitted forward from the stations' raw daily readings and the orders, and no shipped figure
  reproduces under one efficiency and not another except those raw readings, which the fit itself uses.
- **Lesson:** a model's initial condition is estimated by calibrating its process parameter where the parameter acts
  (the irrigation season) on the monitored units and carrying the parameter through every unit's own record, never by
  checking the design value at an end point where the monitored units are saturated, nor by carrying their end state
  to units that record shows are not; no build on file fits a physical parameter on a monitored season and transfers it
  through each unit's inputs (this slot's round 2, the design value on the record, is now the default path).

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a
reflex of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction,
ratio or half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every replay full on 1 February | WOP 2.4 names the state as it stands at the end of 31 January | no | yes (FAO-56's start after winter rain) | the stations' January readings refute it | no | no | readable |
| R1 each weather year from the state its own autumn and winter left | WOP 2.4 | no | yes (a modeller's spin-up) | the stations refute it | no | no | readable |
| R2 the replay rule run through 2026, then the observed winter | WOP 3.4 ("In a replay") | no | yes | the stations refute it | no | no | readable |
| R3 each field's last delivered set taken as a refill | WOP 3.4's refill reads across by analogy | the orders' set_end | yes (FAO-56's full irrigation) | the stations' season refutes it (every held station short of full after its last set) | no | no | readable |
| R4g all of the record's water reaching the root zone | no | no | no | the stations' season refutes it (misfit 1,411 against 8.9) | no | no | readable |
| T4 the record run at Table 4, checked at 31 January (the default path) | WOP 3.5 and Table 4 read across | Table 4 | yes (the procedure's own efficiency on its own model) | the stations' January readings pass it (all within 0.094 in) | no | no | readable |
| P1 the stations' January readings on their fields, Table 4 elsewhere | WOP 2.4 (the state as it stands) | the station export | yes (use the measurement where there is one) | passes at the stations | no | no | readable |
| AB the Table 4 run shifted by the stations' January offset | no | no | yes (bias-correct a model at the observation date) | the offsets are 0.005 to 0.094 in | no | yes | readable |
| MI the stations' January share of total available water on every field | no | the full point and profile columns | yes (impute from the monitored sample) | no | no | yes | readable |
| RG a fitted model on the obvious covariates | no | no | yes | no | no | no | readable |
| PT the stations' efficiency on the stations' crops only | no | the site sheet's crop | yes (do not extrapolate a fit) | no | no | no | readable |
| KC the stations' misfit put down to the crop coefficients | WOP 3.2 files the crop's evapotranspiration | no | yes (fit the most visible coefficient) | the stations' drawdown between sets follows Table 1 (misfit 21.6 against 8.9) | no | no | readable |
| G (decisive) the efficiency fitted on each station's 2026 season, carried through every field's record | no: WOP 2.4 names only what the state is; Table 4's note ties it to WOP 3.5; no sentence names the record's efficiency, a fit, a calibration or the stations | no: the export holds profile water and full points, no efficiency, deficit or depletion column; nothing marks a season or a set | no: the reflex for a filed efficiency is to use it, and the reflex check (the stations at the order date) passes it | no: no control scores it; the stations' season is the fit's own raw material (about 390 daily readings each, no efficiency, depletion or state column), and their January readings, the check the pack invites at the order date, tie under Table 4 and the golden alike | no | no: a least-squares fit of a parameter through a floored, capped daily balance per station over 390 readings, then every field's own record and the thirty replays | silent |
| O3 the stations' efficiency in the replays too | WOP 3.5 ("divided by the application efficiency of the field's irrigation method (Table 4)") | no | yes | no | no | no | readable |
| O2 the golden start with the cap dropped | WOP 3.1 caps the depletion | no | no | no | no | no | readable |
| O1 the full-start replays plus the 31 January depletion as a flat addition | WOP 3.1 (a replay's rain refills part of it) | no | no | no | no | yes | readable |

The decisive rung is silent because the question the pack raises, what state the fields are in on 31 January, has a
natural check that passes the wrong answer: the stations measure the state at the order date, and there every station's
state is the same under any efficiency. What the default path skips is a question no file asks: where in
the record the efficiency shows. It shows only through the season, set by set, and only a fit there finds it.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs, then the asks' rows. `checks.py`
asserts each (the alternative computed and shown to move the call or its figures, or shown to converge). WOP is the
Water Order Procedure; T1 to T5 its tables. Every record-run variant below refits the stations under the same variant.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the 2027 season" | deliveries at the headgate 1 February to 31 October 2027 | calendar 2027 | same call: the canal is dry 1 November to 31 January (asserted: no delivered set outside the season in any year on file) | WOP 2.1 |
| SF2 | "how much water ... order" | the smallest whole number of thousands of acre-feet covering the requirement in at least 24 of the 30 weather years (the 24th smallest, rounded up) | the interpolated 80th percentile of the thirty; the 24th rounded to the nearest thousand | the percentile converges on 212,000; the nearest thousand also 212,000 (the 24th sits 562 above 211,000) (both asserted) | WOP 2.3 ("the smallest whole number of thousands of acre-feet that would have covered") |
| SF3 | the fields | each field's latest accepted 2027 request; withdrawn requests and superseded versions out | every request row | 231,000 | WOP 6.2; the requests' Status in the dictionary |
| SF4 | a field's acres | those on its accepted 2027 request, in the replays and the record run | the register's GIS acres | 213,000 | WOP 6.2 ("Each field's crop, irrigation method and acres are those on its water request") |
| SF5 | a root zone's total available water | T3 capacity times the lesser of the T2 root depth and the T3 depth limit | no depth limit | 211,000 | WOP 3.3 |
| SF6 | the weather record | station 39 to 30 April 2014, the yard station from 1 May 2014, a day the yard did not record from station 39 | station 39 throughout; the yard from its first day (April 2014); missing yard days as zero | station 39 throughout 214,000; the yard from April converges (0.0); missing days as zero converges (-220.0) (each asserted) | WOP 6.1 |
| SF7 | a replay's days | each weather year's own 1 February to 31 October, 29 February kept in a leap year | 29 February dropped | converges (-73.1, asserted) | WOP 2.4 ("its 29 February included in a leap year") |
| SF8 | a replay day's arithmetic | previous depletion plus the day's ET less its rain, then the floor and cap, then the irrigation test at the day's end | the irrigation test before rain; the rain taken first | 214,000; rain first converges (+104.7) (both asserted) | WOP 3.1, 3.4 ("on any day at whose end its depletion has reached or passed") |
| SF9 | where each replay starts | each field's root zone as it stands at the end of 31 January 2027 (WOP 2.4), estimated from the record and the stations | full on 1 February (R0); each weather year's own autumn and winter (R1); the replay rule run through 2026 (R2); full at the canal's close (R2b); the last set as a refill (R3) | each files its own order (Ladder) | R0, R2b and R1 by WOP 2.4 and the stations' 31 January readings (every station deep in its root zone); R2 by WOP 3.4 ("In a replay"); R3 by the stations' season (every held station short of field capacity after its last set) |
| SF10 | the water in the record | orders with status Delivered | cancelled orders counted (R2d) | 211,000 | the dictionary ("Cancelled: cancelled before water ran; no water was delivered") |
| SF11 | the share of a set's water that reaches the root zone | the share the stations' 2026 readings show for the field's method (drip 0.9353, micro-sprinkler 0.8822, sprinkler 0.7811) | Table 4's design efficiency read across to the record (T4, the default path); all of it (R4g) | 215,000; 210,000 | Table 4's note ("Design application efficiency of each irrigation method, as WOP 3.5 uses it") files Table 4 for the replays only; the stations' season: misfit 670.6 at Table 4 and 1,411.2 at all of it against 8.9 at the fitted efficiency over 3,565 readings (asserted) |
| SF12 | the record run's start | field capacity at the end of 27 January 2026 (every root zone, from either November state, asserted) | field capacity on 1 February 2026; from 1 November 2025 at field capacity or at total available water; from 1 February 2023 through every season's record, former ids through the register; the stations fitted from 1 February 2026 | converges: identical states at 31 January 2027 (asserted to 1e-9) and each station's efficiency within 0.002 (asserted) | the records converge |
| SF13 | a set's water by day | the ordered flow for the hours it ran on each day | all on the set's first day; all on its last day | converges (+369.0, -398.0, asserted), and the stations reject both (misfit five times the hours' and more, asserted) | the records converge; the stations' daily readings |
| SF14 | the record's water within a day | with the day's ET and rain, then the floor and cap | after the day's floor and cap; before the day's ET and rain | converges on the order and the year (0.0, +156.1, asserted) | the records converge |
| SF15 | a field's acres in the record run | the request acres | the register's GIS acres | converges (-469.7, asserted) | WOP 6.2; the records converge |
| SF16 | the water a set delivered | its ordered flow for the hours it ran (the dictionary: "the rider sets the turnout to it") | each set scaled by its turnout meter's season over its ordered season (0.965 to 1.032) | converges (-181.7, asserted) | the dictionary's `ordered_cfs`; the records converge |
| SF17 | a field's efficiency in 2026 | its 2027 request's method | its 2026 method | converges: every field kept its 2026 method (asserted against the crop survey) | the records converge |
| SF18 | a requested field with no 2026 delivered set | none exists | (a start for a new field) | converges (asserted: every requested field took a delivered set in 2026) | the records converge |
| SF19 | the crop through 2026 and the winter | the 2027 request's crop | the 2026 crop | converges: every requested field carries its 2026 crop (asserted) | the records converge |
| SF20 | the root-zone cap | depletion never above total available water | uncapped (O2) | 213,000 | WOP 3.1 ("never more than the root zone's total available water") |
| SF21 | the loss allowances | a lateral's water is its fields' deliveries over one less its allowance; the headgate's is the laterals' over one less the main canal's | deliveries times one plus each allowance | 209,000 | WOP 4.1 |
| SF22 | a west spur field's lateral (turnouts 05-021 to 05-034) | the register's lateral as it stands: Lateral 6 (asserted for every spur field) | Lateral 5 (the turnout number, or the feed before 15 June) | converges (-264.4, asserted) | WOP 6.2 ("as the District's field register stands when the order is calculated") |
| SF23 | ties at the order's rank | none: the 23rd (2011, 210,008), 24th (2012, 211,562) and 25th (2003, 213,438) smallest stand apart | (a tie-break) | n/a (asserted at 1,000 acre-feet) | the records converge |
| SF24 | reference evapotranspiration | the ET0 the weather record reports | recomputed from the stations' temperatures (Hargreaves) | 223,000 | WOP 3.2 ("the reference evapotranspiration the District's weather record reports for the day") |
| SF25 | rain | every inch counts until the root zone is full, the rest drains | an effective-rain fraction (75 per cent) | 216,000 | WOP 3.1 |
| SF26 | units | inches of depletion, ET and rain; acre-feet as inches times acres over 12; a cubic foot per second for an hour is 3,600 cubic feet | (none) | n/a (the model's own arithmetic reproduces each replay, asserted) | WOP 3.1, 3.5 |
| SF27 | station 39's millimetres in inches | divided by 25.4, carried unrounded | each value rounded to the yard's hundredths; 0.0394 inches per millimetre | both converge on 212,000 (-213.2, +121.9, asserted) | the dictionary ("25.4 millimetres to the inch") |
| SF28 | Ask 1 and 3: a west spur turnout's lateral on a read interval | the lateral that fed it: Lateral 5 for intervals ending at or before its 15 June read, Lateral 6 after | the register's Lateral 6 all season | Lateral 5 16,440 against 18,160 and Lateral 6 19,930 against 18,210, both shares off (asserted) | the ask's terms (a delivery counts against the heading its water passed); the operations log's 13 and 15 June entries; no water ran to the spur from 13 to 15 June and every spur meter was read on 15 June (asserted), so no interval straddles the change |
| SF29 | Ask 2 and 3: a lateral's water on a day its logger kept no total | the Water Master's estimate in the operations log | the day left out | every lateral low by 142 to 704 acre-feet (asserted) | the days without a logger total are exactly the estimated days, each a day water ran at the lateral's turnouts (asserted); the dictionary's `volume_af` ("the heading logger's daily total") |
| SF30 | Ask 1: the season's reads | from each turnout's read before 1 February to its read after 31 October | (a window inside the season) | converges: the book brackets the season at every turnout and no water ran outside it (asserted) | the records converge |
| SF31 | Ask 4: when a board change takes effect | at the reading the note sits on (each of the 24 notes timed ahead of its sheet's reading, asserted) | from the next day | Lateral 2 640, Lateral 4 280, Lateral 6 660 (asserted) | the notes' own times |
| SF32 | Ask 4: a day without a sheet | the last reading stands until the next | the day at zero | Lateral 3 410, Lateral 7 490, Lateral 8 410 (asserted) | the dictionary ("A reading stands for its day and for each following day until the weir's next reading") |
| SF33 | Ask 1: a swap's registers | the shop's `Reg. out` and `Reg. in` (new meters at 0.00, rebuilt meters with the register they carried) | (none: the registers bracket the book's reads) | converges: each removal register sits just past the old meter's last read and each installation register at or just under the new meter's first (asserted) | the records converge |
| SF34 | crediting the 2026 record to a root zone (round 2's judge residual) | the root zone as it stands at the end of 31 January 2027 is the one the record's delivered sets, at the share the stations show, the weather and the T1 coefficients left | no delivered set credited (full on 1 February, R0); the record at Table 4 (T4); the last set as a refill (R3) | 196,000; 215,000; 209,000 | WOP 2.4 ("as it stands": a state of the fields, not of a model); the data: on the generator's clean truth the golden start misses the fields as they are by 0.074 in acre-weighted, the Table 4 run by 0.482, the last set by 0.500 and the full start by 3.871 (asserted) |
| SF35 | what decides the call (the audit's rule 3 test) | an analytical choice: WOP 2.3 and 2.4 file the WHAT, and no filed sentence gives the record's efficiency or how the state is estimated | executing the filed rules alone, Table 4 read across to the record | 215,000 (the default path) | the estimand and the data: on the clean truth, every rule read correctly, the Table 4 run files 215,000 and the stations' efficiency 212,000 (R3a, R3b) |
| SF36 | a station's field | the register's field on the station's parcel number (the site sheet's APN without its dashes) | (no other key: the export carries no field id) | converges: each of the 11 stations joins one 2027 field and every APN in the register names one field (asserted) | the records converge |
| SF37 | a reading's day | local midnight ends the day before (the platform stamps UTC; the dictionary: "The station logs once a day at midnight local time") | the UTC date taken as the reading's day; a day early | converges (-136.2, +85.9, asserted) | the dictionary's `Reading (UTC)`; the records converge |
| SF38 | a station's depletion | its full point less its profile water | (none) | converges: every station's reading at the end of 27 January 2026 within 0.15 in of its full point (asserted) | the dictionary's `Full point (in)` and `Profile water (in)` |
| SF39 | the period fitted | every reading from the end of 28 January 2026 to the end of 31 January 2027 | February to October 2026; May to October 2026 | converges (+5.2, +4.9, asserted) | the records converge |
| SF40 | the efficiency by method from the stations | each station's least-squares fit, the method's stations averaged | the median; one pooled fit per method; one factor over Table 4 for all three methods; acre-weighted | converges (+103.9, -3.3, -112.0, -75.0, asserted); one standard error of each method's mean either way also (+150.0, -256.7) | the records converge |
| SF41 | the efficiency's grain | the irrigation method (Table 4's grain) | the stations' efficiency on the stations' crops only, Table 4 elsewhere (PT) | 214,000 | the drip stations in almonds and in vines agree within 0.01 (asserted); Table 4 and WOP 3.5 carry efficiency by method |
| SF42 | the stations' own fields | the record run at the method's efficiency like every field | their 31 January readings in its place | converges (-3.0, asserted) | the records converge |
| SF43 | a border field's efficiency | Table 4 (its sets run past field capacity) | the border stations' own fit (0.6973 averaged); any value from Table 4's up | converges: every border field's 31 January state the same from 0.70 to 1.00 (asserted) and the border stations' fit files the same order (0.0) | the records converge |
| SF44 | what the stations' misfit at Table 4 is put down to | the share of the record's water reaching the root zone | a factor on the crop coefficients at the Table 4 efficiency (KC, 0.969) | 211,000 | WOP 3.2 files the crop's evapotranspiration (Table 1); the stations' drawdown between sets follows it: the crop coefficient fit leaves 21.6 of misfit against 8.9 (asserted) |
| SF45 | a replay's delivery | the depletion it replaces over Table 4's efficiency | over the stations' efficiency (O3) | 206,000 | WOP 3.5 ("divided by the application efficiency of the field's irrigation method (Table 4)") |
| SF46 | the stations' 31 January readings | the end of the run the fit is checked on, the same under any efficiency at every station (asserted at each station) | the readings on their own fields with the Table 4 run elsewhere (P1); the Table 4 run shifted by their offset by method (AB); their share of total available water on every field of the method (MI); that share regressed on the last set's day, the January crop coefficient and the method (RG) | 215,000; 215,000; 218,000; 216,000 | the data: every station's 31 January state is the same at Table 4 and at every efficiency up to its own (asserted), so the January readings cannot tell the efficiencies apart, and the late blocks they would be carried to are where the efficiency still moves the state (pistachios, citrus and walnuts at 0.52, 0.51 and 0.59 of total available water against 0.73, 0.68 and 0.70 under Table 4, asserted) |
| SF47 | a station's logger gaps | no reading on those days (KB-SM-03, 8 to 15 July; KB-SM-08, 17 to 22 March, both in the site sheet's notes) | (a value filled in) | converges: the fit uses the readings there are (asserted: two stations with gaps of 8 and 6 days) | the records converge |
| SF48 | what the prompt names of the inputs (the round 3 judge's optional clause) | the call, the two files and the asks, and no input: WOP 2.4 files the start as each field's "root zone as it stands at the end of 31 January" | the start filed in the prompt "from the root zone the District's 2026 deliveries and soil moisture readings put each field in on 31 January" | same call (the clause moves no figure) | declined at ship: naming the soil moisture readings in the prompt points at the decisive step's evidence (a single-purpose sentence), and the prompt carries the question and no convention; the judge found the method forced by the data without it (asserted: the prompt names no input file and none of soil, moisture, station or efficiency) |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads them
all as the golden does. SF11 and SF46 hold the two estimators of the record's efficiency that the ladder carries (Table 4
checked at the order date, and the stations' season fit), separated by the stations' own readings through the season,
75 times the misfit at Table 4; the January readings tie under both for a computable reason (the dry autumn erased the
efficiency from every station's state). Every defensible construction of the record run and of the fit (SF12 to SF16,
SF22, SF27, SF37 to SF40, SF42, SF43 and the converging cells of SF6 to SF8) lands inside the golden's thousand, the
nearest 469.7 under the 24th smallest (SF15) and 369.0 over it (SF13). The rule 3 audit's test is SF35: the filed sentences executed word for word file 215,000.

## Ladder

Every rung is a complete pipeline on the same literal estimand (WOP 2.3 and 2.4), computed by `checks.py` from the pack
(631 fields on accepted requests, 40,309 acres); the default path and the golden again by `verify.py`.

| Rung | Start of each replay | 24th smallest (AF) | Order | Setting year | Against the golden |
|---|---|---|---|---|---|
| R0 | full on 1 February | 195,251.98 | 196,000 | 2003 | -7.71 per cent |
| R2b | full at the canal's close, then the observed winter | 196,470.41 | 197,000 | 2003 | -7.13 per cent |
| R1 | each weather year's own autumn and winter | 198,331.55 | 199,000 | 2008 | -6.25 per cent |
| R2 | the replay rule run through 2026, then the observed winter | 198,546.59 | 199,000 | 2008 | -6.15 per cent |
| O3 | the golden start, the stations' efficiency in the replays too | 205,631.29 | 206,000 | 2012 | -2.80 per cent |
| R3 | each field's last delivered set taken as a refill, then the observed winter | 208,241.37 | 209,000 | 2012 | -1.57 per cent |
| R4g | the record run with all of each set's water reaching the root zone | 209,173.15 | 210,000 | 2012 | -1.13 per cent |
| R3c | the record run at the stations' efficiency from each field's first set taken as a refill | 210,150.36 | 211,000 | 2012 | -0.67 per cent |
| R2d | the record run at the stations' efficiency with cancelled sets as water | 210,160.56 | 211,000 | 2012 | -0.66 per cent |
| KC | the stations' misfit fitted by a crop coefficient factor at Table 4 | 210,972.30 | 211,000 | 2012 | -0.28 per cent |
| G golden | the record run at the efficiency the stations' 2026 season shows | 211,561.96 | 212,000 | 2012 | 0 |
| O2 | the golden start with the cap dropped | 212,366.37 | 213,000 | 2012 | +0.38 per cent |
| O1 | the full-start replays plus the 31 January depletion as a flat addition | 213,908.61 | 214,000 | 2003 | +1.11 per cent |
| PT | the stations' efficiency on the stations' crops, Table 4 on the rest | 213,936.09 | 214,000 | 2012 | +1.12 per cent |
| AB | the Table 4 run shifted by the stations' 31 January offset | 214,276.37 | 215,000 | 2012 | +1.28 per cent |
| P1 | the stations' 31 January readings on their fields, Table 4 elsewhere | 214,496.48 | 215,000 | 2012 | +1.39 per cent |
| T4 (default) | the record run at Table 4, checked at 31 January | 214,499.45 | 215,000 | 2012 | +1.39 per cent |
| RG | the stations' 31 January share regressed on the obvious covariates | 215,872.93 | 216,000 | 2012 | +2.04 per cent |
| MI | the stations' 31 January share of total available water on every field | 217,143.57 | 218,000 | 2012 | +2.64 per cent |
| HT | every drip, micro-sprinkler and sprinkler field at its total available water | 217,675.76 | 218,000 | 2012 | +2.89 per cent |

- **Separation.** The default path and every use of the stations' January readings file 215,000 to 218,000, three to six
  bins over the order; the record's other efficiencies (all of it, the last set as a refill) 209,000 and 210,000, two and
  three under; the starts that ignore the record 196,000 to 199,000. The near rivals each break a filed sentence or a
  data fact: R3c and R2d (211,000) the stations' season and the dictionary's Cancelled, KC (211,000) WOP 3.2 and the
  stations' drawdown between sets, O2 (213,000) WOP 3.1's cap, PT (214,000) the drip stations' agreement across crops,
  O3 (206,000) WOP 3.5 (each asserted a full bin from the order).
- **Position.** The 24th smallest sits 561.96 acre-feet above 211,000 and 438.04 under the order (asserted between 400 and
  600), its neighbours 1,554 under (2011) and 1,876 over (2003), asserted at 1,000; every defensible variant of the fit
  sits within 256.7 of it, every construction of the record run within 469.7.
- **The decisive move.** T4 to G moves the 31 January state by 0.418 inches acre-weighted (0.526 on the held fields;
  14,290 acre-inches on the late pistachio, citrus, walnut and sprinkler alfalfa blocks against 2,560 on the rest) and
  the order by three thousands; the default's own check (the stations' January readings) cannot see it.
- **Worth on the graded figures.** The call is one figure, and nothing the default path files survives on it; the
  chart's order line and its covered count move with it.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | every field on its latest accepted 2027 request (WOP 6.2), 631 fields; each took a delivered set in 2026 and carries its 2026 crop and method (SF17 to SF19 asserted); members not yet observed: none, the requests closed on 15 January and a field without an accepted request is not run (WOP 6.2); the eleven stations' fields are among the 631 (SF36) |
| 2 | Unit of account | acre-feet at the headgate; the field (one request) is the balance's unit; the efficiency is the irrigation method's (SF41); the order in whole thousands (WOP 2.3) |
| 3 | Attribution window | the season 1 February to 31 October (WOP 2.1); each replay the weather year's own 1 February to 31 October (2.4); the start at the end of 31 January 2027 (2.4); the stations fitted over their 2026 readings (SF39 converges) |
| 4 | As-of dating | the register and the requests as extracted on 1 February 2027; the weather, the orders and the station readings through the end of 31 January 2027; a station's midnight reading ends the day before (SF37) |
| 5 | Version basis | the latest accepted request version (WOP 6.2); the register as it stands (6.2, SF22) |
| 6 | Denominator | the loss allowances divide (WOP 4.1, SF21); the efficiency is a share of a set's delivered water (SF11) |
| 7 | Weighting | the method's stations averaged; the median, pooled, one-factor and acre-weighted fits converge (SF40) |
| 8 | Window length | the thirty weather years 1997 to 2026 (WOP 2.3); the stations' whole export (SF39) |
| 9 | Boundary inclusivity | 1 February and 31 October inclusive; "at least 24"; "reached or passed" its allowable depletion (WOP 3.4). Every allowable depletion is an odd number of hundred-thousandths of an inch, off every lattice a day's depletion sits on; the closest approach over every day of the thirty golden replays is 5.9e-6 inch (asserted in `checks.py` and `verify.py`) |
| 10 | Rounding path | carried unrounded; the order rounded up once to the thousand (WOP 2.3); the 24th smallest 561.96 above 211,000 (asserted between 400 and 600); the efficiency carried unrounded from the fit |
| 11 | Tie-break | none needed: the 23rd, 24th and 25th smallest 1,554 and 1,876 acre-feet apart (asserted at 1,000) |
| 12 | Maturity and censoring | none on the call: the weather has every day from October 1995 to 31 January 2027, the 2026 orders are closed, and the two station gaps leave no reading to fill (SF47); the January readings are bounded by each station's root zone, which is why they do not identify the efficiency (SF46) |
| 13 | Order of operations | per replay day ET and rain together, then the floor and cap, then the irrigation test (WOP 3.1, 3.4, SF8); the record's water within a day with the day's ET and rain, after the floor or before them, converges (SF14) |
| 14 | Row order | file order changes nothing (asserted: the orders file reversed files the same order and requirement) |
| 15 | Duplicate resolution | request versions: the latest accepted (SF3); orders: every order number unique (asserted); one reading per station per day |
| 16 | Identity normalisation | the 2025 and 2026 orders and every request carry the register's field ids (asserted); the 2023 and 2024 orders' former ids map through the register (SF12); a station through its parcel number without dashes (SF36); turnout id formats matter only on the ask paths |
| 17 | Netting against gross | rain and a set's water net the day's ET, floored at zero and capped (WOP 3.1, SF14); nothing else nets |
| 18 | Dimensional units | station 39 in millimetres at 25.4 to the inch, unrounded (SF27); the yard in inches; the stations' profile water and full points in inches; acre-inches to acre-feet over 12; cubic feet per second for hours at 3,600 cubic feet an hour (SF26) |
| 19 | Code and status semantics | request status, order status (SF10) and station quality flags are defined in the dictionary (field semantics, never the stump) |
| 20 | Integerisation | the order in whole thousands (WOP 2.3) |
| 21 | Clause scope | WOP 3.4's irrigation rule and its refill apply in a replay, its own words; Table 4 is WOP 3.5's design efficiency (its note), so the record's share is unfiled (SF11) and a replay's delivery stays at Table 4 (SF45) |
| 22 | Forward window contents | the thirty weather years' 1 February to 31 October weather, all in the record; the 2027 requests; the 31 January 2027 state from the 2026 orders, the stations and the weather to 31 January |

## Literal reader

Executed word for word, the prompt and the Water Order Procedure define the order as the smallest whole number of
thousands of acre-feet covering, in at least 24 of the 30 weather years 1997 to 2026, the water the headgate would take
from 1 February to 31 October 2027 with that year's weather on the season (WOP 2.3, 2.4), every field on its latest
accepted request (6.2) run day by day through the balance of WOP 3 "from its root zone as it stands at the end of 31
January" and carried to the headgate by 4.1. The start is a fact about each field, not a convention, and no filed
sentence supplies it: WOP 3.1 to 3.3 give the balance's crop water use and bounds, WOP 3.4 and 3.5 a replay's
irrigation and delivery, and Table 4's note ties its efficiencies to WOP 3.5. The literal reader estimates the state
from what the pack records, the 2026 orders (each delivered set's flow and hours; a cancelled set delivered no water),
the daily weather and the soil moisture network, through the same balance; the share of each set's water that reached
the root zone is the one quantity left to estimate, and the stations' readings through the season fix it (a least-squares
fit per station, 8.9 of misfit over 3,565 readings against 670.6 at Table 4), every defensible variant of that fit
landing in the same thousand. Run on the record from any start before the 2025-26 winter (SF12), the season at the
stations' efficiency files 212,000. The literal execution with Table 4 read across files 215,000, which no sentence
licenses and the stations' season rejects. Every term in the fork table resolves to one reading or converges.

## Oracles

- **None on the call path.** No past season's requirement, district balance, order, efficiency, state or schedule
  ships; nothing states a 2027 figure or a field's state. The 2023 to 2025 orders are the growers' own schedules, which
  the replays' rule does not reproduce, so replaying 2026 and comparing with the orders confirms no start.
- **The stations' 31 January readings** tie under every efficiency from Table 4's to each station's own (asserted at
  each station): the dry autumn erased the efficiency from each station's state (the drip, micro-sprinkler and
  sprinkler stations at the bottom of their root zones, the border stations refilled by their last sets), so they rule out only the starts that ignore
  the record (R0, R2b, R1) and cannot tell the default from the golden. They are blind for a computable reason, not a
  record built to bless the default: they tie under the golden too.
- **The stations' readings through the season** are the estimator's raw material, not a check of the call: they fix
  the efficiency by a fit, and the order still takes every field's own record run and the thirty replays; no shipped
  column holds an efficiency, a depletion or a state.
- **The WOP tables** state coefficients, depths, capacities, design efficiencies and allowances: inputs every rung uses
  alike.
- **The meter book** measures turnouts, not fields, weekly: scaling each set by its turnout's metered season moves the
  golden 182 acre-feet and leaves the order (SF16), and refutes no rung; it ties on every basis.
- **The ask paths** (the meter book, the meter shop log, the heading loggers, the operations log, the tail weir sheets,
  the structures workbook): no rung of the call reads them, and nothing in the pack states a lateral's 2026
  deliveries, water put in, loss or spill, so none ties only under the golden.

## Ask sheet

**Main call's declared row population:** every row of `kbid_water_requests_2027.xlsx`,
`kbid_field_register_2027-02-01.csv`, `station39_daily_1995-2027.csv`, `kbid_station_daily_2014-2027.csv` and
`kbid_soil_moisture_network_2026.xlsx`, the 2026 rows of `kbid_irrigation_orders_2023-2026.csv` (each delivered set's
flow and hours decisive), the Water Order Procedure and its tables. The asks' devices live in `kbid_meter_book_2026.csv`, `kbid_meter_shop_log_2026.xlsx`,
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
  restoration entries, a Word table of free text in each writer's own words (the estimates written four ways:
  "14 Apr 94.2", "12 May 166.3", "Jul 21 154.6", "6/23 142.9"). Summed as filed, every lateral is low by 142 to 704
  acre-feet.
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

The mirror sheet (the same response stopped at the default path, 215,000) differs only on the recommendation criteria:
no ask couples to the call.

Mirror leakage: 7 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation (the order, the chart's named parts, the critical components), 7
instruction following (the two files, the rounding), 55 asks over 36 figures (1.53 each). With no device cracked the
cracker keeps the method credit: C = 38 + 7 + 3.9 = 48.9; the mirror (R3) keeps r of about 4 (the files' form and the
chart's structure; the setting year, which the default path shares, is not asked): S = 4 + 7 + 3.9 = 14.9, a pair of 31.9. The most
obvious device is Ask 1's chain (a turnout's serial changes in the book, and differenced by turnout the swap throws
errors of thousands): a cracker who chains through the shop's registers fixes 7 deliveries (Laterals 5 and 6 still carry
the spur, and no share moves without Ask 2's estimates), adding 9.9 (7 figures less the credit counted): C = 58.8, a pair
of 36.8. The single device with the largest payoff is Ask 2's absence or Ask 4's boards, 9 figures each: C = 61.6, a
pair of 38.2. Both top responses on the call with no device cracked: 48.9; with one of them also cracking the chain,
53.8, which needs the decisive step held by no response.

Pair ceiling: 38.2

**Round 3.** The ask layer is round 2's: the 2026 record and every ask file are byte for byte as shipped except the
operations log, whose outage entries were rewritten in their writers' own words (a templated frame was a generator tell),
every estimate kept; all 36 lateral figures equal round 2's (asserted against the shipped values). The stations' export is
a main-call file no ask reads.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| WOP 2.1 to 2.4 | 1, the District's board-adopted procedure | the season, the order rule (24 of 30, whole thousands), the replay, and its start: each field's root zone as it stands at the end of 31 January | how that state is estimated, the 2026 season's water, a last set, a deficit |
| WOP 3.1 to 3.5 and T1 to T4 | 1 | the daily balance; a replay's irrigation rule and its delivery at Table 4's design efficiency (Table 4's note: "as WOP 3.5 uses it") | the share of the record's water that reached a root zone; that a 2026 set refilled or did not refill a field; a hindcast; a calibration |
| WOP 4.1 and T5 | 1 | the loss allowances' arithmetic | a measured loss |
| WOP 6.1, 6.2 | 1 | the weather record's splice; the fields, their versions and attributes | the winter; the record's water |
| The dictionary | 4 | field semantics: request and order statuses (a cancelled set delivered no water), the ordered flow (the rider sets the turnout to it), station 39's millimetres (25.4 to the inch), the soil moisture stations' columns (profile water, full point, profile depth, the UTC stamp of a midnight reading), register units, the heading logger's daily total, the weir reading's standing rule | how to build a state, what share of a set reaches a root zone, how to fit a station, how to chain a meter, where a missing day's water is, that boards raise a crest |

## Prompt

`prompt.txt`, rewritten at round 2 and gated by `voice-check.py` (in `precut.py`, 690 characters): the call as a
question with its forcing fact (the order due on 1 February), the workbook's order, the chart's named parts, the four
figures per lateral tied to the call by the allowance the order carries for each lateral, the rounding once at the
close (the order in whole thousands, every other volume to the nearest 10 acre-feet, the shares to one decimal). The monthly schedule, the
setting year and its requirement are no longer asked (`## Tried and rejected`).

Round 3 leaves the prompt as it is: the call, the deliverables and every ask sentence stand, and the
stations' export, like every input, is not named in it.

## Build record

- Generator `task138/generator/` (`build.py` runs everything): `common.py` constants, the procedure's tables, the growers'
  working targets by crop and month and the record's efficiency (`EA_RECORD` 1.0425 times Table 4 for drip,
  micro-sprinkler and sprinkler fields, `EA_SPREAD` 0.004 field to field; never shipped), `weather.py` the two stations,
  `world.py` the district, the growers' irrigation (sets sized on Table 4, the record unchanged from round 2), two daily
  balances per field (the grower's own reckoning at Table 4, which schedules and sizes the sets, and the root zone as it
  is at the record's efficiency), the orders, the requests (grower accounts drawn in the district's own idiom), the 2026
  meters, swaps and work orders, the heading loggers and their outages, the weirs, and the soil moisture network (eleven
  stations among the cooperating growers' almond, vine, pasture and alfalfa blocks, `STATION_SALT` 9; profile water at
  local midnight with 0.05 in of reading noise, stamped UTC, two logger gaps), `records.py` and `docs.py` the files
  (Table 4's note scoped to WOP 3.5; the station export; the operations log in its writers' words), `calc.py` the
  procedure, the stations' fit and every rung, `deliver.py` the goldens and `figures.json`, `checks.py` (the three-rules
  block on the clean truth, every rung and floor, the stations' blindness and misfit, the fit's variants and one standard
  error, SF1 to SF48, the asks with every stop and edge and each lateral figure as shipped at round 2, the separation
  line, the gates and the realism sweep), `verify.py` (an independent recompute from the shipped files alone, its own
  station fit), `metadata.py`.
- Texture knobs on the ask paths are round 2's (a calibration offset shared by each lateral's meters, the 2026 loss
  factor of each lateral, the spill scale, `UNIT_SALT`), untouched: every ask figure equals round 2's (asserted).
- 19 files, 5 formats (pdf, xlsx, csv, docx, txt), the orders file 107,067 rows; distractors (metadata only): the
  groundwater levels, the 2026 crop survey, the Authority's allocation notice.
- Gates on the round 3 build (stage 3, 2026-10-15): `checks.py` 214,111 assertions; `verify.py` green (its own station
  fit on a ten-thousandth grid, the order 212,000 set by 2012 at 211,562.0, the default path 215,000, the closest
  approach, the 36 lateral figures, all from the bundle alone); two consecutive builds byte-identical (target, golden,
  `metadata.json`, `figures.json`, `target.zip`); `precut.py` 49 checks, 0 FAIL, 0 WARN (47 fork rows);
  `voice-check.py` exit 0 (690 characters, the prompt unchanged); `figures_check.py` 59 figures, none absent; the
  container audit clean on `target/` and `golden/` with the floor at 2010; `guard.py validate` 184 cards, 0 invalid;
  `guard.py heart` WARN (`repeat.gate_g` and `repeat.decision` against task137, `people.first` and `people.last`
  against task457, answered under `## Draw`; NOTEs differentiated), no BLOCK; `target.zip` 19 members, equal to
  `target/` by name and bytes, no enclosing folder; one `submission.md` and one `prompt.txt` in the tree.
- `guard.py surface`: exit 0, the same two pairs as round 2 promoted on the card axes alone, no surface overlap: task126
  (surface 0.080, corpus percentile 60) and task82 (0.077, percentile 49), on the decisive gap (population), the
  decisive generator (G3) and the decision type (`quantity_figure`). task126 splits work records a succession link
  chained, read off a separate credit ledger, to measure a duration; task82 attributes checkout records filed under
  one-off keys to members through a second ledger; here nothing is split, joined or attributed: a physical parameter
  of the irrigation method is fitted on a monitored season and carried through each field's own record. Not clones on
  this reading; both are differentiated on the card. No persona from outside the card appears in the pack.
- `leak.py --asof 2027-02-01`: REVIEW, no LEAK, sweep 11 clean, the same lines as round 2. Each harmless: "the model"
  is the procedure's own name for its crop water model (WOP 3); "13,110" in the groundwater file is a date and a depth
  run together ("2023-10-13,110.8") and "17,370" in the meter book a time and a register ("13:17,370.64"); the
  procedure, the working-files note and the operations log carry the call's nouns (district, project, order,
  acre-feet, season) and no figure; the stump-term counts in the procedure (15), the note (9), the operations log (5)
  and the prompt's chart sentence are the domain's ordinary words: "station" in the operations log is canal stationing
  ("station 41", "stations 112 to 140"), the note's line for the soil moisture export says what the file holds (the
  eleven stations' sites and daily profile water), and the procedure files the start as WHAT (WOP 2.4) and Table 4 as
  WOP 3.5's efficiency without naming a fit; the yard logger's `Flag` column is its export's own missing-day flag,
  defined in the dictionary.
- Stage 4, round 3 (2026-10-15), both on the stage 3 cut (`target.zip` sha256 50c887dca427e7ad). Judge: DETERMINISTIC,
  APPROVE, no fix (`determinism_check_report.md`; rounds 1 and 2 in `determinism_check_report_round1.md` and
  `determinism_check_report_round2.md`): Gate H `decisive_step: analytical`; the call and all 36 lateral figures
  reproduced, its own 24th smallest about 211,565 and every fit variant it ran in the 212,000 bin (its nearest, the
  2026 record run on the register's GIS acres with the fit redone, 211,083 to 211,101, still inside it); Table 4's
  215,000 judged the intended trap, refuted by the stations' in-season readings and not by their 31 January ones. Its
  optional prompt clause naming the soil moisture readings is declined (SF48). Reader: no file ranks or states the
  figures and no figure reads as the answer; its Q6, without computing, read the filed replay and order procedure (WOP
  2.3 to 3.5) as rule application: that procedure is the order's machinery, which the default path executes as well;
  the decisive step is the unfiled estimate of the start state (WOP 2.4 files only what the state is), and executing
  every filed rule with Table 4 read across files 215,000 (SF35), as the rule 3 re-audit and the judge confirm. Its
  sweep verdicts of "leak" on the procedure's call words and stump terms and on the prompt's chart sentence are the
  governing procedure's own vocabulary and the chart's named parts, with no figure and no move named. Rule 3 re-audit
  of the round 3 build: PASS (the 31 January readings uninformative for a physical reason, asserted, not a planted
  check); its residual risk is under `## Pre-ship check` as accepted. The pack ships as built: `target/`, the goldens
  and every graded figure unchanged (the rebuild byte-identical to the stage 3 cut).
- Ship gates (2026-10-15): `checks.py` 214,114 assertions (SF48 added); `verify.py` green; two builds byte-identical,
  `target.zip` sha256 50c887dca427e7ad as cut at stage 3; `precut.py` 49 checks, 0 FAIL, 0 WARN (48 fork rows);
  `figures_check.py` 59 figures; `leak.py --asof 2027-02-01` REVIEW, no LEAK, the stage 3 lines; `guard.py validate`
  clean; `guard.py heart` WARN, no BLOCK.

## Pre-ship check

Round 3, written at stage 3 against the built pack; the reader and judge lines are stage 4's.

1. Domain: a season's irrigation requirement read at 24 in 30 replayed weather years through a daily root-zone balance,
   every replay run from each field's state at the order date, which irrigation hydrology estimates by calibrating the
   balance's application efficiency on soil moisture monitoring over the season and carrying it through each field's
   own record; with another field's nouns there is no root zone, deficit set, application efficiency or dry-winter floor
   for the start state or its pitfall to live in.
2. Real work, nothing planted: a weather record spliced from two stations, a field register re-mapped after parcel
   splits, revised and withdrawn requests, cancelled orders, turnout ids written three ways, a soil moisture export keyed
   by parcel number and stamped in UTC with two logger gaps; on the ask paths meter swaps among the shop's work orders,
   rollovers, hundred-cubic-foot meters, a spur re-fed in mid-season, logger outages with the estimates in the operations
   log, flashboards in shorthand remarks; each what these systems produce, none deciding the call.
3. The flip is a method choice: how the share of the record's water that reached the root zones is estimated (fitted on
   the stations' season and carried through every field's record, against Table 4 checked at the order date), not a
   field read, a unit or a stated rule; every rule in the pack is read the same on the default path.
4. The analyst test holds: the default path files 215,000, every use of the stations' January readings 215,000 to
   218,000, the fitted model on the obvious covariates 216,000, the record's other efficiencies 209,000 and 210,000, the
   audit's routes 196,000 to 199,000; only the stations' season fit files 212,000 (and on the generator's clean truth
   the same two figures).
5. One defensible answer: WOP 2.3, 2.4, 3.1 to 3.5, 4.1, 6.1 and 6.2 file the estimand, the start state included; the 48
   fork rows are each asserted; every defensible variant of the fit lands within 256.7 acre-feet of the 24th replay and
   every construction of the record run asserted here within 469.7, inside its thousand (the judge's nearest, the record
   run on the register's GIS acres with the fit redone, 211,083 to 211,101, inside it too).
6. No decoy: no file states a 2027 figure, a past requirement, an efficiency, a field's state or a schedule; the
   stations' January readings agree with the default because the dry autumn erased the efficiency from every station's
   state, and they agree with the golden as well; the groundwater levels, the crop survey and the Authority's
   notice are declared distractors; no memo or voice argues for a start.
7. Nothing hidden and recovered: no certified figure or past order pins the state or the efficiency; it is fitted
   forward from the stations' raw readings and the record.
8. A new lesson: a model's initial condition estimated by calibrating its process parameter where the parameter acts,
   on the monitored units, and carrying the parameter through every unit's own record; round 2's design value on the
   record is now this build's default path.
9. Leak reader (stage 4): no file ranks or states the figures and no figure reads as the answer; its Q6 lean to rule
   application is the filed order procedure, the order's machinery on both paths; the decisive step is the unfiled
   start-state estimate, and executing every filed rule files 215,000 (SF35); its sweep's "leak" lines are the
   procedure's own vocabulary, no figure and no move named.
10. Judge (stage 4): DETERMINISTIC, APPROVE, no fix; Gate H analytical; every graded figure reproduced; its optional
   prompt clause declined (SF48).
11. Accepted risk (the rule 3 re-audit, PASS): the end-point check is blind because three things hold together, the
   driest October to January in 32 winters, a network sited on almond, vine, pasture and alfalfa blocks with no station
   on the pistachio, citrus and walnut blocks that carry most of what the efficiency moves on 31 January, and almonds
   unwatered after September; a sceptical reviewer could read the world as arranged so the natural check passes. Rated
   low to moderate and accepted: each is plausible alone (a grant network on cooperators' blocks, a record dry winter,
   deficit irrigation after harvest), the blindness is physical and asserted (a root zone capped at total available
   water forgets its history; a border set runs past field capacity), and removing it would make the task easier
   without changing what decides it. The re-audit's cheap realism move (a cooperator-selection line in the Sites sheet
   in the program's own voice) is left for a later round, the pack shipping as built; a station on a late crop is never
   added (it would make the 31 January check informative and collapse the stump).

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
- Round 2 shipped design: decisive step read as rule application per the rule 3 audit (2026-10-15, VERDICT FAIL), because
  its start state was the procedure's daily balance (WOP 3.1 to 3.3) executed on the 2026 delivery record at Table 4's
  efficiency, which the table's note then defined as "the share of the water delivered to a field that its root zone
  receives", as WOP 2.4 pointed to; executed word for word on clean data it gave the golden (215,000) with no parameter
  fitted, no state uncertain and no candidate estimators separated by data. Kept the world, the order rule, the replay
  model and the estimand; the start is now an estimate (Table 4 scoped to WOP 3.5, the record's efficiency fitted on the
  soil moisture network), and 215,000 is the default path.
- The audit's proposed late-January probe snapshot on a random sample of fields of each method (prototype, 65 probed
  fields): the probed fields' mean share of total available water by method, an additive offset of the Table 4 run and
  a regression on the probes each landed in or next to the golden's bin (217,000 against 217,000 at an efficiency below
  Table 4; 212,000 and 213,000 against 212,000 above it), so the probe file's natural use was the answer and the file
  a signpost; replaced by a season-long station network whose 31 January readings cannot see the efficiency.
- A probe sample skewed by crop (no tubes in the shaken nut orchards) or by the last set (cooperators' later sets),
  prototype: the transfers' misses swung a bin either way with the efficiency and the draw, never a structural miss;
  replaced by stations in the early blocks, which the dry autumn takes to the bottom of their root zones under any
  efficiency, so the January snapshot is blind for a computable reason.
- The record's efficiency below Table 4 (systems short of design): the start saturates near total available water, the
  order flattens (216,100 to 216,400 across 0.88 to 0.94 times Table 4), the stations' January share lands the golden's
  bin, and the growers' orchards would have run far past allowable depletion all summer; replaced by an efficiency above
  Table 4 (a deficit set loses little below the root zone), 1.0425 times it give or take 0.004 field to field.
- Re-simulating the growers on the record's efficiency (each set sized to the true share): it moves every set, the
  meter book, the headings, the weirs and every ask figure; dropped: the growers keep sizing their sets on Table 4 (the
  2026 record unchanged byte for byte) and only the root zone as it is runs on the share that reaches it.
- Stations drawn without the January property (`STATION_SALT` 0 to 8 at 1.04 times Table 4): five to nine of the eleven
  stations blind, the rest still short of the bottom of their root zones on 31 January, so their January offsets showed
  the Table 4 run's excess and an offset correction moved to 214,000; redrawn (9): every station's 31 January state the
  same under Table 4 and under every efficiency up to its own (asserted), the order 212,000 with its 24th mid-bin.
- The grant's name ("water use efficiency") in the station export's title line: the stump's own word in a main-call
  file; the grant is named the state's on-farm water conservation grant.
- Fitting each station by golden section alone: on a small pasture root zone the misfit's floor is flat and bumpy (local
  minima 0.0005 apart), so the verifier's own search settled elsewhere and one replay crossed a 10 acre-foot line; the fit
  is now the best of a ten-thousandth grid, refined, and the verifier scans the same grid on its own code.
- The ranch names (a place or bird word plus Ranch, Farms, Vineyards: "Juniper Vineyards" on 11 request rows, 203 names
  over 688 rows) and the operations log's nine outage pairs in one frame ("Lateral N heading flume: ... No logger total;
  Water Master estimating ..."): generator tells under the wave 3 bar; replaced by grower accounts drawn the way an
  east-side district's accounts read (family farms, partnerships, trusts, a few road-named LLCs, account names unique) and
  outage entries in their writers' own words, every estimate and ask figure unchanged (asserted).
- A March station gap noted as the probe pulled for the grower's ripping, on an alfalfa block: ripping is an orchard and
  vineyard job; the note now says gophers chewed through the logger cable.
- The round 3 judge's optional prompt clause filing the start "from the root zone the District's 2026 deliveries and
  soil moisture readings put each field in on 31 January" (a WHAT, not the fit): declined at ship; it names the decisive
  step's evidence in the prompt, a single-purpose sentence the wave 3 bar bans, and the judge found the method forced by
  the data without it (SF48).
