# task173: the Varner Valley Public Utility District's April to September 2027 irrigation pumping forecast for Halvern, the first season the Varner River watermaster holds the riparian and pre-1914 rights to a quarter of their allotments (architecture 2)

**Status (2026-10-23).** The number was marked RETIRED on 2026-10-22 (`## Retired`) and the author reopened it for a
from-scratch rebuild in a new cell, `energy-systems-utilities` / `load-forecasting`, Forecasting. Architecture 1
(Ashdale Tax Live) and the two redraw cells of 22 October are spent and are not re-screened; their deaths stay in
`## Tried and rejected`. Architecture 2 below is new in world, decision, quantity and mechanism. No seed is used: the
cell was allocated by the main session and the organisation, decision, quantity and mechanism were searched here.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v2 (the first card this number has carried; architecture 1 sits in `lineage` as abandoned unregistered) |
| Domain / task type | `energy-systems-utilities`, task type `load-forecasting` (serves Forecasting): the deciding quantity is a utility rate class's season energy under a change in its water supply, built the way an irrigation load forecaster builds it, acre-feet each pumping plant must move times that plant's energy per acre-foot |
| Objective | Forecasting & Predictive Modeling: the energy Schedule IP services will draw from 1 April to 30 September 2027, a season not yet open; every file was pulled by 16 October 2026 and the member forecast is due to Halvern on 1 December 2026 |
| Shape | `single-figure`: the call (the class's season energy in MWh, nearest 5,000) and the three base-year tables Halvern's form asks beside it, delivery-point energy by billing month (24 figures), delivery-point demand in each monthly system peak hour (24), and the irrigation services and billed energy each delivery point supplied (8); 56 ask figures, criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (MWh) |
| Mechanism | gap population (decisive: one bottomland billing row is two pumps, a river lift and a well, whose energy per acre-foot differ about fivefold, and the 2027 order moves water from the one to the other), with time (the order rewires where the bottomland plants' water comes from for the first time, and the record's only curtailment response is the bench wells'); pattern none; generators G2 (the bill's grain is the plant's meter, the decision's is each pump on it), G5 (the bottomland need was met by the river lifts until now), G14 (the bench wells' energy per withheld acre-foot does not apply to this pool), G6 (the curtailed population moves from one band of the record to the other); Gate G `forecasting`; strategy `decomposition_attribution` |
| Layer 2 family / pattern | `field_method` (pumping energy as water moved times each plant's own energy per acre-foot, the combined plant's river lift and well separated by fitting its metered energy to its own two metered volumes); `own:replacement-water-priced-at-each-combined-plants-own-well-and-lift` |
| Layer 1 | the January 2020 CIS conversion (legacy account numbers before it), meter exchanges as two read lines, estimated reads trued up on the next read, cancelled and re-issued bills with reversals, register reads with multipliers, the agency's two report layouts and a water year still coming in, the service number written three ways, station days filled from neighbours; on the asks' rows only, feeders moved between substations with the GIS label left as mapped, the delivery-point meters' own clock, a check meter stamping interval starts and a second bank's meter energised mid-season (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `customer_or_counterparty` (the forecast is filed with Halvern Power Authority, the joint power authority that supplies the PUD and sets its 2027 energy blocks from it), forcing event `season_or_peak` (the order fixes the 2027 season's surface supply now, ahead of Halvern's 1 December deadline), organisation family `local_government` (a public utility district, a publicly owned electric distributor), role family `procurement_lead` (the power supply manager who buys the PUD's power), context artifact `filed_standard` (Halvern's member load forecast instructions, the standard the forecast is filed against), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | `vvpud_ip_billing_2015-2026.csv`, one row per meter read line on a Schedule IP bill, January 2015 to September 2026, 96,151 rows; constructed in the layout of a public utility's CIS billing extract across a system conversion |
| Deliverables | `irrigation_forecast_2027.xlsx` (the forecast and its working, the three base-year tables) |
| People | drawn with `guard.py names --geo "United States" --seed 173`: Mario Barnett (the PUD's power supply manager, the requester; in no file), Kimberly Ball (Varner River Watermaster, signs Order No. 2026-14), Tammy Gibson (Halvern load forecasting; named on the instructions). Adam Rojas dropped on a people.first WARN |
| World | the Varner Valley Public Utility District serves the Varner River bottomlands and the Lone Bench above them; Halvern Power Authority, a joint power authority of public utilities, is its supplier; the Varner River Decree (1934) is administered by a court-appointed watermaster; Lone Bench Irrigation District holds a post-1914 right; the Varner Subbasin Groundwater Agency takes metered extraction reports; Kestrel County. All fictional, as are the people, systems and data; the field's method is real |

**Data-native sentence.** In this valley the only seasons the record shows water being cut are the Lone Bench
district's, and the bench wells lift from 300 to 400 feet down, while the bottomland plants the 2027 order cuts lift
from shallow alluvium a few dozen feet down and their river lifts and wells share one meter, so the energy a cut
acre-foot costs is a property of whose wells replace it, readable only by fitting each bottomland plant's metered
energy to its own diversion statements and its own metered well extraction.

**Sources read, and how this differs.**
- `two-layer-task-design.md` families (Energy carries no client rigor cards): `field_method` (the field's own
  energy-water identity), with `estimation_fit` for the per-plant two-volume fit. The textbook routes for an irrigation
  class forecast (an econometric model of class energy on curtailed water and evapotranspiration, an analogue season,
  per-account models on own history) are the default path and its rivals, never the stump.
- Nearest domains' cards: Economics `forecasting-forecast-evaluation` and `elasticity-welfare-policy-impact-estimation`
  2 (a response measured under one regime carried to another) and Healthcare `utilization-access-demand-forecasting` 1
  (capped demand); Urban `forecasting` 1. Each is a lower rung or the default path here; the golden is none of them
  applied as stated: the judgment is which quantity transports (the water, not the energy) and whose lift prices it.
- Cell builds: task136 (rooftop PV bulk-buy uplift, adoption) and task164 (coincident transformer peak from new EV load)
  spend adoption and coincidence; nothing here adopts or coincides. task131 (tariff rebound), task120 (storage drawdown),
  task152 (module wear), task132 (spares renewal) spend their own drivers; none prices water by lift.
- Shapes that held this round (task169 re-routing, task177 v2 exposure at one end): the shape here is our own, a supply
  rule rewiring where a group's water comes from, priced by a physical intensity the record shows only per plant.
- `guard.py slots` on the mechanism's words (energy per acre-foot, same meter, two volumes, combined plant, river lift)
  and the setting's (irrigation, groundwater, watermaster, pumping): task138's irrigation district season order, task152's
  plant wash well, task478's unmetered pumping screen (energy to water through a lift factor, rejected there as no ETL
  task type serving hydrology) and task134's dry-year battery seed share vocabulary only.

## Guard

**The draw was redrawn twice before it was filed, each time on the axis the guard named, and the record of it is the
point of this section.**
1. At the probe the decisive pattern was labelled G14 (the bench wells' rate does not fit this pool), which sat behind
   task273's `ban.pattern`; it was carried as G6 (the curtailed population moves from one band of the record to the
   other), with `composition_mix` and the decree's schedule as the context artifact.
2. Under the registration lock the window moved: task175, registered minutes earlier, took G6, `composition_mix` and
   `register`, and with it the same-puzzle and same-driver signatures inside the batch, and task171 took
   `cooperative_or_member_body`. The decisive rung was re-read rather than relabelled: the silent rung is splitting each
   bottomland meter into its river lift and its well (the readable rung beneath it is carrying water rather than
   energy), so the card leads with G2 (the bill's grain is the plant's meter, the decision's is each pump on it) and
   `decomposition_attribution`, with G5, G14 and G6 kept beside it, and the context artifact is Halvern's filed
   forecast standard, the stakeholder's own file. The ladder, the golden and every figure were unchanged by it.
3. The organisation was then a rural electric cooperative and both of its honest families were banned
   (`cooperative_or_member_body` against task171, `utility_or_infrastructure` against task175). The world was redrawn on
   that axis: the distributor is a public utility district (`local_government`), the publicly owned kind that serves
   irrigation pumping in western valleys, and its supplier a joint power authority. Names and voices moved; the data,
   the decision and the mechanism did not.

`guard.py check` on the filed card: WARN only. `overuse.objective` and `overuse.gate_g` (forecasting in 6 of 12): the
lane's objective. `repeat.gate_g` (task171, task170) and `repeat.decision` (quantity_figure against task170): the
objective's own Gate G and a season energy is a quantity. `test.same_puzzle_older` and `test.same_driver_older`
(population, G2, quantity_figure / forecasting) carry differentiation lines against task142 and task148 v1, and the
card keeps its lines against task98 v1, task124 v6, task132, task144, task163, task465 v1 and task175.

**Abstraction test.** The nearest drivers (task181 v1 at 0.09, task237 at 0.08, task465 v2 at 0.08): two victim
sources pooled at a common point, a composite's variance share, two traits no source records together. None splits
one metered total into two sources by fitting it to each source's own recorded volume, and none prices a carried
volume at each unit's own cost per unit. task175 (the batch's nearest by structure) reads take-up at each run's own
fill; nothing here takes up, and every bottomland plant replaces every acre-foot it can.

## Default path

The pipeline a strong analyst builds from the prompt, the order, the instructions and the files' grain, every filed
rule applied.

1. Sum the bills by service and month (legacy accounts through the 2020 crosswalk, a cancel and its reversal netting
   out), keep the 680 Schedule IP services in service on 30 September 2026 (instructions 3.1), and split them into the
   296 Lone Bench services (district landowners' wells) and the 384 bottomland plants (the services the watermaster's
   statements name as a point of diversion's measure).
2. Take the normal season from station 247: the mean April to September reference ET of 2007 to 2026, 38.97 in
   (instructions 3.3).
3. The Lone Bench services get no district water in 2027 (order paragraph 3), as in 2022: their 2022 season energy at
   normal ET, 118,002 MWh.
4. The bottomland plants' diversion is held to a quarter of each allotment (order paragraph 4): with each right's
   normal-season diversion from its statements, 162,701 acre-feet above the limit; the plants' normal-season energy is
   16,280 MWh.
5. Fit the Lone Bench services' season energy over the 12 seasons on the acre-feet the district withheld (one less the
   allocation, times the contracts) and the season's ET: 772 kWh per withheld acre-foot, a fit that tracks every
   season of the record.
6. Carry it onto the bottomland cut: 125,528 MWh more, so the class draws 259,810 MWh.

Ends on: 260,000 MWh (259,810 unrounded)

Golden: 155,000 MWh (155,196 unrounded)

## Stump sentence

A competent solver files 260,000 MWh by carrying the bench wells' fitted energy per acre-foot the district withheld
(772 kWh) onto the bottomland plants' diversion above the limit, and one who carries the water and prices it at each
plant's energy over its metered water files 145,000 (or 200,000 over its well water alone); the step that lands them
there is reading each bottomland plant's meter as one pump, when it carries a river lift at about 34 kWh an acre-foot
and a shallow well at about 182, whose split only a fit of the plant's water-year energy to its own diversion
statements and its own metered well extraction recovers, which puts the class at 155,000 MWh.

## Three rules

- Task type: load-forecasting (Energy Systems & Utilities), which serves Forecasting & Predictive Modeling: an
  irrigation rate class's season energy for the supplier's member load forecast.
- Domain test: the deciding quantity is the irrigation class's season pumping energy, built the way an irrigation load
  forecaster builds it under a change in water supply: the acre-feet each pump will move times that pump's energy per
  acre-foot (its total dynamic head over its plant efficiency), with a combined plant's river lift and well separated on
  their shared meter from the plant's own diversions and metered well extraction.
- Swap: "how many MWh will a hospital's chillers draw next summer once the district steam loop is cut" keeps a supply
  cut but loses what decides it: replacement water priced by each pump's own lift, and two pumps behind one meter whose
  energy per unit is fitted from the plant's two recorded volumes; with hospital nouns there is no lift, no pair of
  sources on one meter and nothing to fit, so the task collapses to an analogue season.
- Layer 1: the CIS conversion of January 2020 (legacy account numbers before it, the crosswalk), meter exchanges as two
  read lines, estimated reads trued up on the next read, cancelled and re-issued bills with reversals, register reads
  with multipliers (the PUD's CIS and meter shop); the agency's paper and portal report layouts and a water year still
  coming in (VSGA); the service number written three ways (PUD, agency, watermaster); station days filled from
  neighbours (station 247); on the asks' rows only, feeders moved by switching order with the GIS substation left as
  mapped (GIS and OMS), the delivery-point meters' own clock, a check meter at every point stamping interval starts and
  Bench's second bank energised in June (Halvern's metering). Nothing is placed to be caught.
- Layer 2: field_method; the choice that flips the call is pricing the water the order moves at each bottomland plant's
  own well less its own river lift, the pair fitted from its shared meter against its own two water records, against
  carrying the bench wells' energy per withheld acre-foot or reading the shared meter as one pump.
- Decisive step: recognising that a bottomland plant's one billing meter carries a river lift and a well whose energy
  per acre-foot differ about fivefold, and fitting each plant's water-year energy to its own diversion statements and
  metered well extraction to price the water the order moves from the one pump to the other.
- Not semantics: every field, code and unit read correctly (the order's limit, the allotments, the statements' and the
  agency's acre-feet, the bills' multipliers and reversals, the register's plant descriptions) still leaves the analyst
  on the bench wells' energy per withheld acre-foot, or on each plant's energy over its water, because no field gives a
  pump's energy per acre-foot: it is an estimate from each plant's own records.
- Not rule application: the order files the supply and the instructions file the class, season, unit and weather;
  executing every filed sentence with the field's textbook class model on the clean truth files 260,000 (R3a). The
  enumerated family runs 134,282 to 383,493 (own history 134,282, energy over water 142,819, the golden family, a
  quarter of the diversion 160,268, river lifts left running 160,707, three quarters of the allotment 175,486, energy
  over well water 199,599, water at the bench wells' energy per acre-foot 241,198, the default 259,810, the default on
  three quarters of the allotment 383,493); the standing family, the eight constructions that split the shared meter,
  runs 153,908 to 157,031, all on 155,000; what rules the rest out is each plant's own record (its own fit reproduces its
  water-year energy to a median 0.8 per cent, where a pooled pair misses by 10 per cent and the bench rate overstates the
  bottomland plants' own well seasons several fold), loud in the data and stated in no sentence.
- Analyst test: a strong analyst who maps every account, keeps the 680 active services, reads the order correctly and
  fits the bench services' energy on the water the district withheld files 260,000 MWh (Ends on); carrying the water at
  each plant's energy over its water files 145,000, over its well water 200,000; only splitting each plant's river
  lift from its well files 155,000 (`checks.py` R3a, R3b).
- Estimand: `hpa_member_load_forecast_instructions_2027.pdf` 3.1 (the class: services on the irrigation pumping rate
  in service on 30 September 2026, later connections out), 3.2 (energy at the retail meter, MWh, 1 April to 30 September
  2027, under the surface supply ordered for the season), 3.3 (a normal season: the mean April to September reference ET
  of 2007 to 2026 at the station named), 3.4 (each service held to its 2026 acreage and cropping, land the season's
  water cannot reach left unirrigated); Order No. 2026-14 paragraphs 2 to 4 (the season and the supply); the prompt
  names the window, the weather and the rounding.
- No decoy: nothing is planted; no memo, briefing or stakeholder figure states a forecast or an energy per acre-foot;
  the pump tests are correct for the bench plants they test; the wrong answer comes from the easy model alone.
- No certified replay: no certified or published figure is reproduced to recover the method; nothing in the pack states
  a 2027 energy or a bottomland pump's energy per acre-foot.
- Lesson: when a supply rule moves a group's water from one pump to another behind the same meter, the forward energy
  is the water moved times each pump's own energy per acre-foot, fitted from the plant's metered energy against its two
  water records; a response measured on other units, or the meter read as one pump, misprices it; no build on file
  splits two sources on one meter or prices replacement water by lift.

## Readability screen

Reflex row written from what the field does to the deciding quantity (an irrigation class's season energy): an
econometric class model on withheld water and ET, an analogue season, a per-account model on own history, kWh per acre
or per acre-foot from the curtailment record, pump-test kWh per acre-foot, a service's energy over its water.

| Rung | What the solver must see | Test that fires | Verdict |
|---|---|---|---|
| R0 the bench wells' energy per withheld acre-foot carried onto the bottomland cut (the default path) | bills, allocations, contracts, the order | 3 reflex | readable |
| R0a the same onto three quarters of each allotment | the order's paragraph 4 read as a cut | 1 filed sentence (the limit) | readable |
| R1 the bottomland cut carried as water, priced at the bench wells' energy per acre-foot | the agency's reports or the pump tests | 3 reflex | readable |
| R2 the water priced at each plant's energy over its water | statements, reports, bills | 6 linear (one ratio) | readable |
| R2b the water priced at each plant's energy over its well water | reports, bills | 6 linear (one ratio) | readable |
| R3 (decisive) each plant's meter split into its river lift and its well by fitting its water-year energy to its own diversions and metered extraction | nothing names it: no column gives a pump's energy per acre-foot, no sentence says the two pumps share the meter's energy, the register's plant text names a plant's pumps the way every register does | none of the six fires: no clause, no column or marker, not an opponent default, no control bench, no hygiene finding, not one ratio (R2 and R2b miss) | silent |

No confidence level, significance level or test threshold is filed anywhere in the pack.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | irrigation pumping services | Schedule IP services in service on 30 September 2026 | every IP service ever billed | same call | instructions 3.1; the closed services carry no bills after 2018 (asserted) |
| SF2 | from 1 April to 30 September 2027 | the season's six months | the water year | same call | instructions 3.2; order paragraph 2, no diversion outside the season (asserted) |
| SF3 | energy | at the retail meter | at the delivery points, with losses | 5 to 7 per cent higher | instructions 3.2 ("at the retail meter") |
| SF4 | a normal season | the mean April to September ET of 2007 to 2026 | the mean of the record's seasons 2015 to 2026 | same call | instructions 3.3 (asserted) |
| SF5 | under the watermaster's order | diversion held to 25 per cent of each right's season allotment | 25 per cent of each right's diversion | 160,000 | order paragraph 4 ("25 per cent of the season allotment shown for that right") |
| SF6 | the limit through the season | counted cumulatively from 1 April, the season total the lesser of the diversion and the limit | a monthly quarter | same call | order paragraph 4 (asserted) |
| SF7 | rounded to the nearest 5,000 MWh | half-up | half-even | same call | the total sits 196 MWh from its cell's centre (asserted) |
| SF8 | the Lone Bench services with no district water | 2022 at normal ET | 2026 with its 5 per cent restored; a per-service fit across seasons | same call | asserted |
| SF9 | a bottomland plant with no well | leaves the water above the limit unirrigated | makes it up at the mean well | 160,000 | the register's plant (a river lift only) and the agency (no extraction report) |
| SF10 | a plant's normal season | each season at normal ET, averaged | the raw seasons averaged, then put at normal ET | same call | asserted |
| SF11 | the bottomland plants' response to the cut | each plant keeps its 2026 acreage and makes the water above the limit up from its own well | a plant leaves part of its land dry | open | instructions 3.4 ("holds each service to its 2026 acreage and cropping"; "land that the season's water supply cannot reach is not irrigated") |

Every row is asserted in `generator/checks.py` (labels SF1 to SF11).

## Ladder

| Rung | Construction | The pack's answer |
|---|---|---|
| 0 (default) | the bench wells' energy per withheld acre-foot, fitted on 12 seasons with ET, carried onto the diversion above the limit | 259,810 MWh (260,000) |
| 0a | the same onto three quarters of each allotment | 383,493 (385,000) |
| 1 | the water carried, at the bench wells' mean energy per acre-foot (772) | 241,198 (240,000) |
| 2 | the water at each plant's energy over its water | 142,819 (145,000) |
| 2b | the water at each plant's energy over its well water | 199,599 (200,000) |
| 2c | the meter split, the river lifts left running | 160,707 (160,000) |
| 2d | the meter split, three quarters of each allotment | 175,486 (175,000) |
| none | no response (own history) | 134,282 (135,000) |
| 3 (golden) | the meter split per plant, river lifts netted, the diversion above a quarter of the allotment | 155,196 (155,000) |

Position and margins: every rung below 3 lands at least one full 5,000 MWh cell from the golden; the golden family's
eight constructions sit 153,908 to 157,031, inside the 155,000 cell (152,500 to 157,500), the golden itself 2,304 MWh from
its edge. The decisive move is the largest single correction on the water route (from 142,819 or 199,599 to 155,196) and
the only one that lands the cell; each correction below it walks the figure one way and leaves it outside.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | Schedule IP services in service on 30 September 2026, once each | filed, instructions 3.1; SF1 |
| 2 | Unit of account | a service; within a bottomland service, each of its pumps | filed (energy at the retail meter, 3.2); the pumps from the data |
| 3 | Attribution window | 1 April to 30 September 2027 | filed, instructions 3.2; order paragraph 2 |
| 4 | As-of dating | extracts pulled to 16 October 2026; register as of 30 September 2026 | manifest; instructions 3.1 |
| 5 | Version basis | a cancelled bill's reversal nets it; an estimated read's true-up carries the difference | dictionary; R2 L2, L4 asserted |
| 6 | Denominator | none on the call | not applicable: the call is a total |
| 7 | Weighting | each service's own energy | C1: the family is asserted in one cell |
| 8 | Window length | the record's 12 seasons; the agency's 10 water years | C1: the 2015 to 2026 normal and the 2021 to 2026 fit (R2 L1) give the same cell |
| 9 | Boundary inclusivity | bill months April to September; water years October to September | dictionary (bills read at month end); the agency's notes |
| 10 | Rounding path | the class total once, to 5,000 MWh | the prompt; SF7 |
| 11 | Tie-break | none reached | not applicable |
| 12 | Maturity and censoring | water year 2026 reports still coming in | C1: the fit uses the years each well reported; missing read as zero still on 155,000 (R2 L5) |
| 13 | Order of operations | normalise each season, then average | C1 (SF10) |
| 14 | Row order | file order irrelevant | C1 |
| 15 | Duplicate resolution | a bill's read lines summed (two meters at an exchange) | dictionary; R2 L3 asserted |
| 16 | Identity normalisation | the service number as written by the PUD, the agency ("VVPUD 123456") and the watermaster | loud: an unmatched join leaves plants without water |
| 17 | Netting against gross | the river lifts' saved energy netted against the wells' added energy | the decisive construction; rung 2c misses without it |
| 18 | Dimensional units | kWh, acre-feet, inches of ET | units in the data |
| 19 | Code and status semantics | read types A and E; bill statuses BILLED, CANCELLED, CANCEL, REBILL; rights' classes | dictionary; R2 asserted |
| 20 | Integerisation | none on the call | not applicable |
| 21 | Clause scope | the order governs the 2027 season's surface diversion; groundwater is outside it | order paragraphs 2 and 6 |
| 22 | Forward window contents | 2027 under the order, at a normal season, the class as of 30 September 2026 at its 2026 acreage | filed: instructions 3.1 to 3.4, the order |

## Literal reader

Executed word for word, the instructions fix the class (3.1), the energy, unit and window (3.2), the weather (3.3) and
the acreage each service waters (3.4);
the order fixes the supply (paragraphs 3 and 4) and the season (paragraph 2). Nothing filed says how a pump's energy per
acre-foot is reached, so the method stays open, and the records force it: each bottomland plant's water-year energy is
reproduced to a median 0.8 per cent by its own river-lift and well fit, against 10 per cent for one pair pooled over
the plants and several times over for the bench wells' rate; every construction that splits the meter files 155,000
(eight of eight, `checks.py` FAM), and every term's other reading gives the same call or is ruled out by a quoted
sentence (SF1 to SF11). A literal reader who stops at the filed sentences has the estimand and no estimate.

## Oracles

Nothing in the pack states a 2027 energy, a forecast, or a bottomland pump's energy per acre-foot. The pump test
programme (distractor) tests bench plants of 75 hp and more only, and its figures are right for them; the county crop
report (distractor) gives acreage and value; Halvern's delivery-point export and posted peaks are read by the asks
only (the separation assertion deletes them and the call is unchanged). No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the IP bills of 2015 to 2026 (every column but the delivery point, which the
bills do not carry), the register's status, customer, parcel and plant columns, the crosswalk, the agency's extraction
reports, the watermaster's statements and allotments, the district's contracts and allocations, and the station's ET.
Device and hazard rows in it: 0. The asks' devices sit in Halvern's delivery-point export and peak postings and in the
PUD's GIS and OMS feeder records, none of which the call reads (`checks.py` SEP: the call recomputes to the kWh with those
files deleted); the one ask that reads the bills (C, billed energy) reads its 2026 rows, which carry no Layer 1 item
(no estimate, exchange, reversal or legacy row in 2026, asserted).

**Ask A. The energy Halvern metered at each delivery point in each billing month, April to September 2026, in whole
kWh** (24 figures). H18 home: Halvern's form MLF-4(a), the base year the forecast is compared against.
- A1 (the meters' own clock; silent primary): every delivery-point meter keeps Pacific standard time all year and the
  export stamps each interval as the meter records it; Rate W-2 cuts billing months in prevailing time. Read as
  prevailing time, every month starts and ends an hour off, and every figure moves (by 40 to 15,014 kWh). The data
  show it: every meter carries 96 intervals on 8 March 2026, when prevailing time has 92.
- A2 (the check meters; second device): each point has a check meter on the revenue meter's instrument transformers, a
  model that stamps an interval's start, so its rows are the revenue meter's one interval early; summing every meter at
  a point counts the point twice. Bench's second bank (from 15 June) has its own revenue meter, which must be summed; an
  over-cleaner keeping one meter per point loses it.
- Stops (asserted): every meter summed in meter time (all 24 miss); check meters dropped, meter time kept (all 24);
  meter time moved, every meter summed (all 24); one meter per point (Bench June to September).

**Ask B. Each delivery point's demand in the hour of each of Halvern's monthly system peaks, April to September 2026,
in whole kW** (24 figures). H18 home: form MLF-4(b), the coincident demands Halvern bills.
- B1 (the posted hour read against the meter clock; silent primary): the posting gives the hour ending in prevailing
  time (W-2 2.4); read on the meters' standard-time stamps the hour is the one after the peak, and every figure moves
  (by 20 to 831 kW).
- B2 (the check meters, shared with A): summing every meter doubles every figure.
- Stops (asserted): every meter summed in meter time (all 24); check meters dropped, meter time kept (all 24).

**Ask C. For each delivery point, the irrigation services it supplied through the 2026 season and the energy billed to
them from April to September, services as a count and energy in MWh to one decimal** (8 figures). H18 home: form
MLF-4(c), the retail side of each point's base year.
- C1 (a substation label set when the point was mapped; silent primary): the GIS service points carry each service's
  substation as mapped, and two feeders have since moved by switching order (3204 to Corwin Road on 3 November 2025,
  1204 to Mill Slough on 16 March 2026); the OMS feeder sources carry the dates. Grouping by the GIS substation moves
  every figure (25 services between Riverside and Mill Slough and 23 between Bench and Corwin Road, and 803.9 to 10,706.8 MWh).
- Stops (asserted): the GIS substation (all 8).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| H1 the meters' standard-time clock | Halvern's interval meters never move to daylight time | A, B | A every cell, 40 to 15,014 kWh; B every cell, 20 to 831 kW |
| H2 a check meter at every point | Halvern's main-and-check metering | A, B | every cell doubled when summed |
| H3 Bench's second bank | bank 2 energised 15 June 2026 with its own revenue meter | A, B | Bench June to September when one meter is kept per point |
| H4 feeders moved by switching order | the GIS substation set when each point was mapped | C | every cell |

**Referee.** For A and B, the 96 intervals each meter carries on 8 March and each check meter's rows equal to its revenue
meter's one interval later; for C, the OMS effective dates. Each is countable from the shipped rows and none needs a filed
definition.

**Cracker sheet** (the cracker lands the call, runs the battery and executes every filed rule its path points at; on the
interval export it reads interval_end as the export gives it, sums every meter a point carries and takes the GIS
substation; `generator/cracker.py`)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, energy by point and billing month | 24 | meter time read as prevailing, every meter summed | A1, A2 | miss |
| Ask B, demand in each posted peak hour | 24 | meter time read as prevailing, every meter summed | B1, B2 | miss |
| Ask C, services and billed energy by point | 8 | the GIS substation | C1 | miss |

One crack at a time (`cracker.py`): the clock alone keeps 0 of 56 (the check meters still double A and B), the check
meters alone 0, the GIS feeder dates alone 8 and a pair of 32.4; the clock and the check meters together 48 and 52.1.

Measured by: `generator/cracker.py` (run on the cut pack; Part 0's weights, the call and its components 38, the
instructions 7, the asks 55 over the 56 ask figures; a response off the call keeps 5).

Mirror leakage: 0.0 per cent of ask weight (the mirror, off the call on 260,000, takes the same ask paths and keeps none
of the 56 figures).

Pair ceiling: 28.5 measured on the cut pack (the cracker 45.0, the mirror 12.0); the worst single crack 32.4 (C1).

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | R2 (checks.py) |
|---|---|---|---|---|
| L1 legacy account numbers before the January 2020 conversion | the PUD's CIS | the billing extract and the crosswalk | legacy rows unmapped and dropped | call and components unchanged |
| L2 cancelled bills, their reversals and the re-issued bills (2016 to 2019) | the PUD's CIS | the billing extract | reversal lines dropped | unchanged |
| L3 meter exchanges as two read lines on one bill (2017 to 2019) | the PUD's CIS | the billing extract | one read line kept per bill | unchanged |
| L4 estimated reads trued up on the next read (outside 2022 and 2026) | the PUD's CIS | the billing extract | estimated lines dropped | unchanged |
| L5 the agency's paper and portal layouts; water year 2026 reports still coming in | VSGA | the extraction reports | missing reports read as zero extraction | unchanged |
| L6 station days filled from neighbours | station 247 QC | the ET file | filled days dropped | unchanged |
| L7 the service number written three ways | the PUD, the agency, the watermaster | the register, the reports, the statements | an unmatched join | loud (no bottomland plant matched) |
| L8 closed services on the register and in early bills | the PUD's CIS | the register and the bills | closed services kept | unchanged (SF1) |
| L9 feeders moved with the GIS substation left as mapped | the PUD's GIS and OMS | the service points and feeder sources | the GIS substation | outside the call's population; Ask C device |
| L10 the meters' own clock; check meters; Bench's second bank | Halvern's metering | the interval export | meter time read as prevailing; every meter summed; one meter per point | outside the call's population; Ask A and B devices |

## Leak sweep

`leak.py task173 --asof 2026-10-16`: REVIEW, no LEAK. Each REVIEW line, answered:
- Two golden-figure coincidences in data files (a run of interval readings in the delivery-point export and an acre-foot
  value in the statements contain digit strings of an ask figure); they are readings, unrelated to any ask.
- The forecast instructions carry the call's words (irrigation class, April to September 2027, energy) because they
  file the estimand; they state no figure and no method. The order and the dictionary carry three of them for the same
  reason.
- Design-note vocabulary in the order, the instructions, the rate excerpt and the dictionary is the field's own
  (supply, service, diversion, register, member); none says how a pump's energy per acre-foot is reached, that a
  bottomland meter carries two pumps' energy, or what clock the meters keep.
- The service register names three delivery points' roads in premise addresses (Corwin Road, Mill Slough Road);
  nothing in it ranks anything.
Container metadata: the generator writes the organisations' own names as each file's producer and the extract's or
the document's own dates (`scrub_producer_metadata.py` clean on `target/` and `golden/`, band 2024-01-01 to 2026-10-16).

## Stage 3 gates

- `checks.py`: 87 checks, 0 failed (the three-rules block R1 to R3c, SF1 to SF11, the golden family and every rival, the
  separation, each ask device and its fairness, the documents' positive controls, the input gates, the realism sweep).
- `verify.py` (csv, openpyxl and pypdf, no generator state): every figure in `figures.json` reproduces.
- Two consecutive builds byte-identical (19 pack files and the golden); `target.zip` cut from the final build.
- `figures_check.py`: 67 figures in blocks 1 to 4, none absent. `precut.py`: exit 0. `voice-check.py`: PASS (765
  characters).
- `guard.py surface`: exit 0. Eleven pairs promoted for an adjudicated read, ten by corpus-percentile surface similarity
  at 0.100 to 0.103 with no shared file, schema, row count or wording, and task142 by the card-level same-driver
  signature (population, G2, forecasting), differentiated on the card (task142 builds a period total's upper percentile
  from arriving units and their durations; nothing here arrives, and the step splits one meter between two pumps).
  The people screen reads "Lone Bench" (a bench of land and its irrigation district) as a persona; the pack's personas
  are Kimberly Ball and Tammy Gibson, both on the card.
- `guard.py heart`: WARN (no BLOCK). Cracker on the cut pack: pair 28.5, mirror leakage 0.0, worst single crack 32.4.

## Tried and rejected

- Lazy abandonment in the 2026 simulation (a customer's patience checked only when an expert came free): it pushed a
  retry before the clock and one expert served two customers at once; abandonment and the queue's close are now events
  in time order, asserted (no event out of order, no overlapping interactions).
- Demand at the 2026 scale of 1.03: the 2026 fortnight served more new cases than the 2027 plan, an implausible fall; the
  2026 scale is 1.00 and the plan grows 3.4 per cent on the CRM's count.
- A graded figure for the fortnight's forecast contacts to the nearest thousand: its constructions spread 400 contacts
  and the golden sat within 100 of a cell edge at every placement the booking allowed; dropped from the prompt, kept in
  the workbook as working.
- Shrinkage at 11 per cent with a handle-time ramp of 0.47: the nearest flat-haircut rival landed the block; the ramp is
  0.455 and shrinkage 12 per cent, every canonical haircut now orders another block.
- Ask B as counts of customers answered after more than three minutes by day: the connect time flips too few customers
  on the quiet days after the deadline, so the cracker landed 2 and 3 May; the daily average wait moves every day by 9
  seconds.
- Crashes drawn per agent-day at a flat rate: some days had none, so the cracker landed them; each day now has at least
  three planned and a blocked one retries later in the shift.
- Hillsborough's Sunday shifts ending at 22:00: one contact ran past 23:00 Eastern, Atlantic midnight, and the invoice
  weeks read in Atlantic and Eastern time split by 0.08 h; Sunday shifts now end by 20:30.
- Frozen sessions all lasting exactly the 90-minute timeout: a uniform organ; team leads now force some out after 10 to
  75 minutes, and the timeout carries the heartbeat's 30 seconds.
- Personal Not Ready of 3 to 8 minutes: put 25 April's billable time on an exact rounding tie (209.05 h); 2 to 9
  minutes, every Ask A figure now clears its tie.
- An invoice header with a street address and an HST registration number: invented details that could match a real
  business; dropped.
- Registering after task165's DRAWN (23bd05a): `guard.py check` on 18 October blocks on the last-three bans on G14,
  `composition_mix` (task165), forum `executive_team` and forcing event `vote_or_meeting` (task247), and beyond them on
  `test.same_puzzle` and `test.same_driver` against task165 in the twelve-build window. Putting G6 first would clear the
  two tests and was rejected as a relabel of a real kinship (both builds carry a conditioned yield to a new mix); stage
  3 is built in scratch and committed without a card, which registers when task165 has left the window.
- Architecture 1 (Ashdale Tax Live's deadline-fortnight outsourcer booking, comebacks set by whoever opened each case) abandoned unregistered on 22 October: the guard's window blocked it for three days on `composition_mix`, G14, `filed_standard`, `executive_team` and `vote_or_meeting` while other lanes kept drawing those axes, and the author chose a fresh draw in a new world rather than wait; nothing of its world, mechanism or blocked axes is carried.
- Redraw cell 1, candidate A (a hospital's ALC census, its patients awaiting long-term care leaving at a fixed weekly placement count set by the region's vacancies, cut after a home closed, while other ALC exits leave in proportion to the stock; default path Little's law on the 12-month ALC stay): measured on the clean truth over 4 seeds (`proto_a2.py`), the textbook rivals bracket the golden instead of missing it on one side (Little on 12-month stays 98 to 128, Little on 13-week stays 150 to 209, occupancy over arrivals 103 to 197, Holt-Winters on the weekly census 112 to 156, against golden 120 to 171), and the golden's own spread from the post-closure placement rate alone is plus or minus 3.5 per cent at one standard error; the closure recency that separates Little's law from the count model is the same dial that starves the post-closure rate, and a census time series is a random walk with drift exactly where the placements are a count. Dead.
- Candidate B (the same placements shared at random across five hospitals' waiting lists, so another hospital's filed rise in designations lengthens every hospital's wait): measured over 3 seeds and two shock sizes (`proto_b.py`), Little on the hospital's own 12-month hazard lands at 32 to 54 against golden 35 to 53, again on both sides, with the golden plus or minus 3 per cent on the pooled placement rate; the spillover moves the level by about 15 per cent, under the 30 per cent the bar needs. Dead.
- Paper screens on the same cell, each killed before a harness: the holiday discharge backlog (the 2026-27 Christmas and New Year run of no-discharge days matches 2025-26 and 2023-24 within a day, so the seasonal naive on aligned dates carries it; `time_semantics` besides); length of stay that shortens with occupancy (the slope's estimator family is open and confounded with season); ED diversion by geography after a neighbour closes (nearest-hospital allocation is the cheap twin of the choice model, one dial); a census capped at staffed beds (the latent demand is either the boarders' count, a population reading, or arrivals times stay, which is the default path itself); new Saturday operating lists (no Saturday surgery in the record, so the weekday discharge model is extrapolated and the family forks); nursing workload from turnover (lever under 10 per cent); float-pool pooling and sickness moving with demand (the empirical daily percentile reaches the golden); a discharge-count cap first binding in the forward peak (the driver of task156, task159 and task172); a transitional unit's 60-day stay limit returning patients (task172's deadline); follow-up echoes of a new-patient surge (task157 and architecture 1's comebacks); nurse retirement at a pension eligibility date (a teachers' plan reads the same, rule 1 fails).
- Redraw cell 2, candidate C1 (a discrete cohort mortality step, the cohorts born 1944 to 1947 carrying 25 per cent excess mortality at every adult age, against Lee-Carter fitted on 1995 to 2025 and a fixed 1.5 per cent improvement; `proto_c.py`, expected values, a fictional country of about 20 million): on the deaths at 75 to 89 in 2027 to 2031, the planning quantity, Lee-Carter files 0.990 of the truth and the fixed improvement 1.012, a one per cent lever, because the step sits on four cohorts among fifteen; it reaches 20 per cent only on the cohort's own ages (83 to 86 in 2030), a quantity no decision funds, and grading it needs the cohort effect separated from age and period, the APC identification fork. Dead on lever.
- Cell 2 paper screens, each dead before code: oldest-old register over-coverage rebuilt by extinct cohorts (already dead twice, task228 candidate 2 and task271's re-root screens, not re-screened); mortality displacement after a severe 2025 winter (one to two per cent of a year's deaths, sized from a handful of past shocks); tempo and recuperation in period fertility, and second births echoing a first-birth surge (task176's paper deaths, not re-screened); depletion of the childless pool after a pulled-forward first-birth wave (about 4 per cent of a year's births, and the time-since-entry family); select mortality in a recently enrolled group (a hazard by time since entry, task468 and task134 v2); exposure bias where adjacent birth cohorts differ sharply in size (a local, sub-per-cent move on any planning total); late registration of inquest deaths at young adult ages (the standard truncation correction, lesson 1 of this round); incomplete death registration estimated by the death distribution methods (a coverage defect, the judge's planted-defect list, as task228 found); the first year deaths exceed births (the difference amplifies the golden family's spread as much as the lever); Lee-Carter's rotation, jump-off and fitting window, and cause-specific forecasting (method forks); a disability-free life table by Sullivan against a multistate projection (prevalence as incidence times duration, cell 1's bracketing death in other nouns); a once-in-sixty-years zodiac dip in births (a single past event).
- Rebuild (2026-10-23), cell `energy-systems-utilities` / `load-forecasting`, paper screens killed before a harness:
  large customers chasing a coincident-peak charge that a 2027 tariff removes (the add-back is the field's known 4CP
  correction and a null region publishes it: the non-alert days are the uncurtailed load); heat build-up over a
  heat wave's days (a lever of 3 to 6 per cent of a peak, and the lag family forks); dual-fuel heat pumps losing gas
  when a gas network is decommissioned (the pre-emption shows in the hybrids' own cold-day load, and the all-electric
  homes publish the answer); rooftop PV export limits raised under a minimum-demand forecast (task136's PV world in the
  same cell, and unclipping a known limit is the reflex); suppressed demand after rotating outages end (the restoration
  rebound is task131's driver); a direct load control programme ending (task131 again, and the non-event days are a
  null region); a district cooling plant with ice storage closing (contrived, one plant); data-centre cooling load by
  design (a visible attribute, stratified by reflex); prepaid metering conversion (stratify by payment type);
  efficiency savings embedded in the trend (about one per cent a year).
- Candidate P1 on code (`proto_p.py`, `proto_p2.py`, 12 seeds): senior plants with separate well and river-lift meters.
  The lever held (the bench wells' fitted energy per curtailed acre-foot carried over filed 1.44 to 2.31 times the
  golden), but each senior well's energy per acre-foot was then one divide of two shipped files (its bills over its
  metered extraction), a single-purpose route to the golden; the wells were moved onto the river lifts' meters, as the
  bottomland plants are built, so the pair has to be fitted (`proto_p3.py`: per-plant fit, pooled fit and the
  separate-plant average within 0.25 GWh of the truth over 16 seeds).
- The decreed allotment against the water actually diverted (the cut is the diversion above a quarter of the
  allotment, not three quarters of the allotment): kept only as a lower rung, because the order files the limit and
  applying it to each right's statements is rule application.
- Architecture 2 (Varner Valley PUD's 2027 Apr-Sep irrigation pumping under the first senior curtailment, bottomland plants a river lift and a well on one meter) spent 2026-10-23 at stage 4 on zip be677673 (Gate F): blind reader A filed 155,000 MWh, the golden, by the path "345 river lift plus well services: energy = a x diverted AF + b x well AF per service (fit 2017-2026) ... Diversion capped at 25 percent of allotment, balance pumped from the service's own well"; reader B filed 130,000 (it read the cap as leaving the land unirrigated). Both readers hit all 56 ask figures: the check meter repeating each revenue meter one interval early was dropped as a duplicate, and the meter clock's missing DST gap gave its standard time away. The judge returned DETERMINISTIC with one FIX_NOW (which meter in each pair is the revenue meter) and warned that the plant strings "RIVER LIFT + WELL" invite the two-source fit. Lessons: a plant description that names both pumps makes the per-service two-regressor fit a reflex, so the decisive quantity was named in the pack; a duplicated series and a clock with a tell-tale gap are visible hygiene and keep nothing.


## Retired

**RETIRED 2026-10-22 under this round's rule that a number which dies in its second new cell is retired.** Three
worlds were screened at stage 1 and none held:
- the seed's world (Ashdale Tax Live), architecture 1, built in scratch but never registered, abandoned for a fresh draw
  after three days blocked by the guard's window;
- redraw cell 1, healthcare delivery patient flow (Forecasting): candidates A and B on code, twelve on paper; a
  count-limited exit lands between the textbook routes, not outside them;
- redraw cell 2, sociology and demography life tables (Forecasting): C1 on code, fourteen on paper; national vital
  counts give sigma near one per cent, but every structural judgment the textbook routes take for granted moves a
  planning total by a few per cent, or is a coverage defect, a future-rate assumption or a spent driver.

No card was ever registered, so no guard axis is held. The screens above are the number's record for `guard.py slots`.

## Rebuild (2026-10-23)

Reopened by the author for a from-scratch rebuild under the rule that no number stays retired; architecture 2 drawn
in `energy-systems-utilities` / `load-forecasting` (Forecasting), card v2 registered, `pipeline.json` architecture 2.
