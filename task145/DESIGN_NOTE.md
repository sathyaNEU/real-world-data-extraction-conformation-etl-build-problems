# task145: Larchwood Express Canada, where six broker posts go across five gateways for 2027 (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC16. The seed (an express carrier's customs brokerage
placing six new broker posts across five import gateways, or holding them, on each gateway's forecast entries per
broker) was read at its header and Situation only. Its world, decision and quantity are kept: an express carrier's
licensed customs brokers file formal entries at five import gateways, six new broker posts are funded for 2027, a post
goes to the gateway with the most forecast entries per broker while that load is above the standard, and the rest are
held. The seed's mechanism (the entry forecasts' own error record setting a lower bound) is decoy-era design and is not
used; no back-test organ ships. The pitfall is re-found from how the records come to exist: a shipment needs a broker's
formal entry only when its value for duty exceeds CAD 3,300 once its invoice value is converted at the customs rate of
its date, so a gateway's 2027 formal entries depend on where its goods' CAD values land under the plan's exchange rates,
and goods differ in which value they hold from year to year. Goods priced in the invoice currency keep their invoice
value and carry the rate into their CAD value; goods priced in Canadian dollars and invoiced at that price converted at
the day's rate keep their CAD value whatever the rate. How far the rate passes through is an estimate, segment by
segment, from the consignments the same importers ship in both years on file.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task145.json`, architecture v1, registered 2026-10-15 after `git pull` (task262, task455 and task144 on file); `guard.py check` WARN (repeat.gate_g, answered below), no BLOCK; `guard.py validate` clean; re-checked after the rule 3 rework (below) |
| Domain / task type | `economics-econometrics` (client domain; Economics & Econometrics has never carried a forecasting build), task type `forecasting-forecast-evaluation` (forecasting): the call rests on a conditional forecast of each gateway's 2027 formal import entries on the plan year's exchange rates, through the exchange-rate pass-through into each segment's declared values |
| Objective | Forecasting & Predictive Modeling: each gateway's average monthly formal entries in calendar 2027, a window not yet open, on the 2027 network plan, and from it the broker posts placed and held |
| Shape | `05` allocation to a fixed total (the six posts across five gateways and the held bucket): six bucket counts, each gateway's forecast monthly formal entries and its entries per broker post once placed (10), the call and the blocking load (2), the asks' 40 figures and the deck's named parts; about 60 criteria |
| Decision | `allocation_to_total`, answer unit `count` (broker posts per gateway and held) |
| Mechanism | gap time (the plan year's rates sit where no month on file has been, and the euro rate where none since January 2021 has) then population (the segments differ in how the rate passes into their values: Calgary's US-dollar goods and the Chinese goods at Mississauga and Richmond hold their CAD values, every other segment its invoice prices; OGD-regulated shipments are formal whatever their value); pattern none, generators G16 decisive (the forecasting method: the conditional forecast through each segment's estimated pass-through, against the count's ratio, a mechanical re-conversion of every shipment or one pooled share), G13 (the plan year's window and its rates); Gate G `forecasting`; strategy `forecast_method_backtest` (stumping F6: the invariant is constructed, the natural fit fails forward) |
| Layer 2 family / pattern | `field_method`; `own:formal-entry-count-at-the-plan-years-rates-through-segment-pass-through-from-repeat-consignments`: the field's way of projecting declarations above a nominal threshold under a forward exchange rate (estimate, by segment, which goods pass the rate into their CAD value from repeat transactions, and re-apply the line at the forward rate to that share alone) against the generic moves (extrapolate the count, re-convert everything, pool one share) |
| Furniture | forum `executive_team` (the Canada leadership team approves the brokerage establishment at its review of 22 October 2026), forcing event `vote_or_meeting` (that establishment review), organisation family `logistics_or_3pl` (Larchwood Express Canada, an express carrier), role family `capacity_planner` (the brokerage workforce planning lead), context artifact `filed_standard` (BRK-STD-03, the brokerage staffing standard, which files the placement rule and the forecast's basis and no method), calibration `none`, opening `question-first`, question form `where` |
| Spine | `highvalue_check_2024Q4.csv` to `highvalue_check_2026Q3.csv`, the clearance system's quarterly high-value check extracts (every inbound international shipment released with a value for duty of CAD 2,500 or more, and every OGD shipment, in two layouts), eight quarterly files over October 2024 to September 2026 (the four of the plan's base, 245,702 shipments with 13 amended shipments twice, and the four pulled for the 2026 review, 234,415 shipments), 480,130 rows; constructed. The pack is 26 files in six formats (csv, docx, json, pdf, txt, xlsx) |
| Deliverables | `broker_posts_2027.xlsx` (the placement, each gateway's forecast and load, the forecast basis, the two ask tables), `establishment_review_2027.pptx` (two slides for the leadership team: the placement and the desks' overtime by quarter) |
| People | drawn with `guard.py names --geo Canada --seed 145 --n 30` and `--locale fr_CA --seed 145`, every name the guard clears: Laura Parks (lead, brokerage workforce planning; the requester), Robin Larson (vice-president, trade and brokerage services; owner of BRK-STD-03), Wanda Armstrong (manager, network planning; the network plan), Brian Stewart (treasury manager; the planning rates in the plan), Clémence Sirois (manager, clearance operations, Dorval; the clearance manual), Theresa Rowe (HR systems analyst; the time and attendance migration); none appears in the prompt. The HR roster's brokers are drawn from seeded locale pools in the generator |

**Guard.** `guard.py check` on the registered card: WARN, no BLOCK. Answered: `repeat.gate_g` (forecasting beside
task144): the stump sits in a projection for a window not yet open, which is what the Forecasting objective is; task144's
forecasting gate carries a cascade through follower feeds, nothing of a nominal line or an exchange rate.
`test.same_driver_older` (gap time, decisive G16, Gate G forecasting) is differentiated on the card against task127 v3
(a development triangle restated at the latest resolution shares), task138 (a starting store rebuilt before replaying
driver traces) and task446 v2 (a screen's yield under a moved base rate, backed out through two error rates). The first
draft of the people (Daniel, Sandra, Sean, Nina) each met a WARN on an older build and was redrawn from the same pools.

**Same-puzzle and same-driver tests.** Gap time, decisive G16, decision `allocation_to_total`, Gate G `forecasting`: no
build in the last twelve carries gap time at all (coverage: 0 in the window), so `test.same_puzzle` and
`test.same_driver` pass; the older matches are the three differentiated above.

**Abstraction test.** Stripped of nouns, the driver is: the forward count of units above a fixed line is set by where
each unit's value lands at the forward period's conversion factors, and units differ in which value they hold fixed
from period to period, their own denomination or the line's; the history's count carries only the past factors, a
mechanical re-conversion of every unit at the forward factors treats every unit as holding its own denomination, and
one pooled share of holders treats unlike groups alike; only estimating each group's mix of holders from the units seen
in both periods, and re-converting the own-denomination share alone, gets the count. The three nearest on file
(`guard.py check`): task253 v3 (units with a latent level below a line, seen through noisy averages, 0.08), task98 v5
lineage (units scored on the class they had at entry, 0.07), task107 v4 (a group under a line only on an entry rate its
counterparty lifts at an anniversary, 0.07). None converts a unit's value between denominations or estimates which
value a unit holds; task107's is a dated step in a rate the history shows exactly. task446 v2 (the closest in shape, a
derived rate carried onto a moved condition) has a classifier, a base rate and Bayes' rule; here the derived quantity
is a tail mass of a value distribution under a change of scale that only part of each segment undergoes, and the part
is read off repeat transactions.

**Data-native sentence.** Larchwood's clearance system routes a shipment to a gateway's brokerage desk for a formal entry
when its value for duty, declared in the currency of its commercial invoice, exceeds CAD 3,300 once converted at the
customs exchange rate for its date, or when its goods fall under another government department's program; European
goods priced near EUR 2,000 and US goods priced near USD 2,350 therefore sit on either side of the line according to
the month's rates, while Calgary's importers of US goods and the Chinese sellers shipping to Mississauga and Richmond
sell on Canadian-dollar prices (Calgary's price points run from CAD 3,329 to 3,399) and invoice them at the day's
conversion, so those goods' CAD values, and their routes, stay where they are whatever the plan's US dollar and
renminbi rates do.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (56 builds): renewal (132), conditional
survival (133), hazards by time since entry (134), selective labels (141), a period total built from its units (142), a
shared group effect (143), a feed cascade (144), a screen's yield under a moved base rate (446), an age-anniversary rate
step (107): none forecasts a count above a nominal line through a forward exchange rate. `layer2-rigor-patterns.md`,
economics: forecasting-forecast-evaluation/1 (real-time vintages) and /2 (proper scores) are not this build's; the
decisive line is a conditional forecast through the structure (the nearest library line is
healthcare-delivery-health-economics/utilization-access-demand-forecasting/2, project with the rates on the projected
structure against a trend on totals), here the structure being each segment's pass-through, estimated from repeat
transactions the way trade economics estimates producer-currency against local-currency pricing.
`two-layer-task-design.md`: "the data's real structure" and "validating a forecast properly" are the client's families
for the step. `measured-drivers.md`: held tasks put the decisive move upstream of every graded figure; here every
forecast, every load and every post inherits it. `strategies.md` F6 (the invariant constructed from a log) and Part 6
(a dated cause stepping the series dies to an event study: here the forward condition is a level, not a date). The
seed's header and Situation (FC16) for the world, decision and quantity only.

**World.** Larchwood Express Canada Ltd. (Mississauga, Ontario) is an express carrier whose inbound international
shipments arrive at five import gateways: Mississauga (YYZ, Toronto Pearson), Dorval (YUL, Montréal-Trudeau), Richmond
(YVR, Vancouver International), Calgary (YYC) and Winnipeg (YWG). Each gateway has a brokerage desk of licensed customs
brokers in the Customs Brokerage department (vice-president Robin Larson). The clearance system values every shipment
on its commercial invoice in the invoice currency, converts it at the customs exchange rate for its date and routes it:
over CAD 3,300, or goods under another government department's (OGD) program, to the desk for a formal entry filed by a
broker; otherwise released under the courier low-value program (CLVS) by clearance operations. Shipments with a value
for duty of CAD 2,500 or more are checked against the commercial invoice before release (the high-value check), and the
check's extracts are pulled every calendar quarter. Most of the network's goods are priced in the currency they are
invoiced in; Calgary's importers of US goods (western distributors and e-commerce sellers buying on Canadian price
lists) and the Chinese sellers on the Mississauga and Richmond lanes sell on Canadian-dollar prices and invoice them at
the day's conversion. No file records which: the extracts carry each shipment's importer, tariff item, invoice value,
customs rate and CAD value, in both years. At peaks a desk sends entries to a contract broker, Brandmoor Customs
Services, which transmits them on Larchwood's account and invoices monthly. The brokerage staffing standard BRK-STD-03
places new broker posts each autumn for the next calendar year: one at a time, at the gateway whose forecast average
monthly formal entries per broker post (posts already placed in the review counted) is highest, while that load
exceeds 560; posts not placed are held to the next review. The forecast is made on the network plan for the year
(Network Planning issued the 2027 plan on 18 September 2026, its volumes by gateway and month and its planning
assumptions, Treasury's planning rates among them). The establishment at 1 January 2027 is 25 broker posts (Mississauga
7, Dorval 5, Richmond 6, Calgary 4, Winnipeg 3); six new posts are funded. The review sits on 22 October 2026; the
extracts were pulled from 5 to 9 October 2026 and the request is dated 13 October.

## Default path

1. Read BRK-STD-03 (posts placed one at a time where the forecast 2027 average monthly formal entries per broker post,
   posts already placed counted, is highest, while above 560; the rest held; the forecast on the 2027 network plan) and
   the 2027 network plan (inbound international shipments by gateway and month, in thousands).
2. From the gateway monthly report take each gateway's inbound international shipments and formal entries for the
   twelve months to September 2026 (the plan's base), and its formal entries per shipment.
3. Multiply each gateway's 2027 planned shipments by that ratio and divide by twelve: the forecast average monthly
   formal entries.
4. Divide by the establishment and run the placement: one post at each of Calgary, Dorval, Mississauga, Richmond and
   Winnipeg, one held.

Ends on: one post at each of the five gateways, one held.
Golden: two posts at Dorval, one at Calgary, three held: each segment's pass-through (gateway and invoice currency) read
off the base year's shipments that repeat a consignment of the year before (at the same invoice value, the rate passes
into the CAD value; at the same CAD value, it does not: Calgary's US-dollar goods 0.009, the Chinese goods at Mississauga
0.011 and Richmond 0.013, every other segment 0.958 to 1.000), that share of each segment's base-year shipments
re-routed at the plan's planning rate against CAD 3,300 and the rest kept at the CAD value and route the base year gave
it, OGD shipments formal regardless, scaled to the plan's volumes. Dorval gains about an eighth (European goods priced
near EUR 2,000 cross the line at EUR 1.680), Mississauga, Richmond and Winnipeg lose about a tenth (US price points
near USD 2,350 to 2,380 fall under it at USD 1.340), and Calgary holds within 0.2 per cent of its base year.

## Stump sentence

A competent solver carries each gateway's formal entries per inbound shipment over the twelve months to September 2026
onto the 2027 network plan's shipments and places one post at each of the five gateways with one held (Ends on); the
step that lands it there is forecasting the 2027 count without asking how each segment's CAD values respond to the
plan's exchange rates: most of the network's goods keep their invoice-currency prices, so the plan's rates move their
line, while Calgary's US-dollar goods and the Chinese goods at Mississauga and Richmond keep their CAD values, so the
plan's rates do not, and only the pass-through estimated by gateway and invoice currency from the repeat consignments
files two posts at Dorval, one at Calgary and three held; re-routing every shipment at the plan's rates, or one share
for the network or for each currency, drops Calgary under 560 and holds four.

## Three rules

- **Task type:** `economics-econometrics`, `forecasting-forecast-evaluation` (serves Forecasting): the call is a
  conditional forecast of each gateway's 2027 formal import entries on the network plan's exchange rates, through the
  pass-through of those rates into each segment's declared values, estimated from repeat consignments.
- **Domain test:** the deciding quantity is each gateway's 2027 formal entries, which trade economics forecasts
  conditionally on the plan year's exchange rates as the mass of declared values above a line fixed in Canadian dollars,
  where the rate reaches a declared value only as far as its goods are priced in the invoice currency (producer-currency
  against local-currency pricing, the exchange-rate pass-through the field estimates from repeat transactions); the
  generic forecasts (the count carried on its share, its trend, an elasticity fitted to the monthly history, a full
  re-conversion of every shipment) place a post at every gateway or hold four, so the call turns on the pass-through.
- **Swap:** "Calgary keeps its post because its US goods are sold on Canadian prices and hold their CAD values at the
  plan's dollar rate" read with another field's nouns ("ward B keeps its nurse because its patients are billed in local
  units and hold their value at next year's rate") loses the invoice currency, the conversion at the date's rate, the
  choice of pricing currency and the nominal line a price point crosses, so what moves the count stops making sense.
- **Layer 1:** on the call's path, the clearance system's high-value check extracts come in eight quarterly files whose
  layout a February 2026 release changed (column names, date formats, the rate column's label); release times are
  stamped in UTC beside each gateway's local release date; a few shipments amended after release appear again in the
  next quarter's extract; the gateway monthly report has two layouts (the legacy brokerage system to September 2024
  counted formal entries by accounting date, the new one by release date); gateways are keyed by airport code, desk name
  and the plan's region labels; the plan's volumes are in thousands to one decimal; OGD program codes are blank or NONE
  where none applies; shipments are invoiced in CAD, USD, EUR, GBP, CNY and JPY, each row with the customs rate of its
  date, and a CAD value converted from a US-dollar invoice of a CAD price lands a cent either side of that price on some
  days. On the ask paths, two time and attendance systems (legacy to 31 October 2025, new from 1 November 2025) with two
  employee-number and pay-code schemes and the migration's carried week, the HR assignment history, call-back lines at
  the paid minimum, and the contract broker's monthly invoices, portal detail and a re-issued invoice. Each is what these
  systems write; none decides the call (each mishandled leaves the placement where it was, asserted: R2).
- **Layer 2:** `field_method`: the expert estimates, by gateway and invoice currency, the share of goods whose CAD value
  moves with the rate (repeat consignments at the same invoice value) against those whose CAD value holds (repeats at
  the same CAD value), and forecasts the count above the line by re-applying it at the plan's rate to the first share
  alone; the shortcuts carry the base year's routing (pass-through nil everywhere), re-convert every shipment (full
  pass-through everywhere) or pool one share across segments that behave in opposite ways.
- **Decisive step:** estimating each segment's exchange-rate pass-through from the consignments the same importers ship
  in both years (Calgary's US-dollar goods repeat at the same CAD value 13,169 times and at the same invoice value 117;
  the Chinese goods at Mississauga and Richmond 2,161 and 3,731 times at the same CAD value; every other segment's
  repeats keep their invoice values, 54,126 of 54,444), and forecasting the 2027 count through it: the plan's rates
  applied to the invoice-held share, the base year's CAD values and routes kept for the CAD-held share. Executing the
  filed rules gives no share; the full re-conversion they suggest files Dorval 2 and four held.
- **Not semantics:** every field, code, unit and definition can be read correctly (the value for duty in its invoice
  currency, the customs rate of its date, the value in CAD, the route, the OGD program, the line at CAD 3,300, the
  plan's volumes in thousands and its rates, the establishment) and the default path and the full re-conversion both
  read them all correctly and still miss; no field, code or definition says how a shipment is priced, and the shares
  come from the joint behaviour of invoice values, CAD values and rates across the two years, an estimate whose
  segmentation and estimator the analyst chooses.
- **Not rule application:** the shipped sentences on how a figure is computed are CLR-OPS-11 2.1 and 2.2 (each shipment
  valued on its commercial invoice in the invoice currency, converted at the customs rate of its release day), 3.1 and
  3.2 (formal over CAD 3,300 or under an OGD program, a CAD invoice on its value), BRK-STD-03 4.2 to 4.5 (the load and
  the placement) and 4.3 (the forecast on the plan's shipments and planning assumptions), and the plan's assumption 7
  (Treasury's planning rates for 2027); executed word for word they route a 2027 shipment whose value is known and say
  nothing on what a 2027 shipment's invoice or CAD value will be. Completing them mechanically (each base-year shipment
  at its base-year invoice value, converted at the plan's rate: a filed assumption executed through a filed rule) is
  rival (b), which files Dorval 2 and four held; the golden needs an estimate no sentence performs, the share of each
  segment whose CAD value moves with the rate, read off the repeat consignments with a segmentation and an estimator the
  data separates (gateway and currency against one share for the network, 0.737, or for the US dollar, 0.719, rejected
  by a homogeneity statistic of 71,119 on 11 degrees of freedom).
- **Analyst test:** a strong analyst who reads the staffing standard, the clearance manual and the network plan
  correctly forecasts each gateway's 2027 formal entries as the plan's shipments times its formal entries per shipment
  over the twelve months to September 2026 and places one post at each of the five gateways with one held (Ends on); the
  stronger one who sees that the plan's rates move the line re-routes every base-year shipment at its own currency's
  planning rate, because the manual values a shipment on its invoice, and files two posts at Dorval with four held
  (Calgary at 2,000 a month, 505 a post on its four); pooling one pass-through share for the network (0.737) or for each
  currency (0.719 for the US dollar) files the same; only the shares by gateway and invoice currency, Calgary's US-dollar
  goods and the Chinese goods holding their CAD values, file two at Dorval, one at Calgary and three held (R3a, R3b and
  R3c asserted on the generator's clean truth, the world's own 2027 filing the golden's placement and every rounded
  figure).
- **Estimand:** BRK-STD-03 (`brk_std_03_brokerage_staffing_standard.pdf`) section 4: a gateway's load is its forecast
  average monthly formal entries in the plan year (every formal entry for a shipment released at the gateway in calendar
  2027, whoever transmits it) divided by its broker posts (the establishment at 1 January of the plan year and the
  posts already placed in the review); the forecast is made on the network plan for the year, its shipments for the
  gateway and its planning assumptions; posts placed one at a time while the highest load exceeds 560, the rest held.
  The network plan's assumptions page fixes the plan year's volumes, its base (the twelve months to September 2026), its
  shipment profile (each gateway's lanes, customers and goods as in the base) and its exchange rates as the year's
  rates; nothing files how the goods are priced, how a rate passes into a value, or the forecast's method.
- **No decoy:** nothing is planted to be caught: no copied block, no hidden rule, no file, column or flag that marks a
  shipment's pricing (the evidence is the extracts' own invoice values, CAD values and rates in both years), and no
  memo, draft, briefing or stakeholder figure states a forecast, a load, a share or a placement; the network plan states
  volumes and assumptions, the clearance manual the routing rule, and no document ranks the gateways on the decision;
  the distractors (the 2026 network plan as issued in September 2025 and the export desk's declaration report) rank
  nothing.
- **No certified replay:** no published forecast, certified load, pass-through table or past placement ships to be
  reproduced; the method is forced by the routing rule and the plan's rates acting on the shipments on file, with each
  segment's share estimated from them, and no closed figure is matched to recover it.
- **Lesson:** a count of items above a fixed nominal line under a forward exchange rate is set by how far the rate
  reaches each item's declared value, and that depends on the currency its price is set in, not the currency it is
  invoiced in; the pass-through is estimated by segment from repeat transactions (the same goods at the same invoice
  value, or at the same domestic value), and neither a full re-conversion nor one pooled share survives segments that
  behave in opposite ways; no build on file teaches producer-currency against local-currency pricing (task446 teaches a
  screen's yield under a moved base rate, task107 an anniversary step in a rate the history shows exactly).

## Readability screen

| Rung (the move that climbs it) | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0: base-year formal entries per shipment carried on the plan (the default) | BRK-STD-03 4.3 and the plan's volumes | the gateway report's two columns | yes, the planner's ratio | no | no | yes, one ratio | readable |
| R0b: the formal entries' own trend (log-linear or exponential smoothing with seasons) | no | the 69-month series | yes, a forecasting default | no | no | no | readable |
| R1: the formal share fitted on the month's US dollar and euro rates, evaluated at the plan's rates | the plan lists its rates | the gateway report and a rate per month | no | no | no | yes, a regression | readable |
| R2: every foreign-currency shipment re-routed at its currency's planning rate on its base-year invoice value | CLR-OPS-11 2.1 to 3.1 and the plan's assumption 7, read together | the register's value, currency and rate columns | yes, once the rates are seen to move the line | no | no | yes, one conversion per shipment | readable |
| R2a, R2b: one pass-through share for the network, or one per invoice currency | no | the register's importer, tariff item and two value columns | no | no | no | no | readable |
| R3 (decisive): each segment's pass-through (gateway and invoice currency) estimated from the base year's repeat consignments of the year before, the plan's rate applied to the invoice-held share, the CAD-held share kept at its base-year routes, OGD formal regardless, scaled to the plan's volumes | none: no sentence says how the goods are priced, how a rate reaches a value, or connects the plan's rates to the year's routing or to formal entries (asserted); CLR-OPS-11 states how a shipment is routed on its date and the plan lists its planning rates among nine assumptions, both read by the default path | the register's importer, tariff item, invoice value, customs rate and CAD value are the clearance system's audit trail of each valuation; no column marks a shipment's pricing or a repeat | every forecasting reflex carries the routing (the ratio, the trend, smoothing, a fitted elasticity) or re-converts every shipment, and lands on a post at every gateway or four held | none: no record scores a forecast | none: the battery passes on every route | no: a match of 245,702 shipments to the year before on two keys, twelve shares, a re-routing by segment, then a placement | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | broker posts | the establishment's posts at 1 January 2027 (filled or vacant) and the posts placed in the review | the brokers employed today | same call (asserted: the establishment table equals the posts the desks hold) | BRK-STD-03 4.4 ("posts on the gateway's establishment at 1 January of the plan year, filled or vacant") |
| SF2 | formal entries | every formal entry for a shipment released at the gateway, whoever transmits it | only entries the desk's own brokers transmit | the register carries no transmitter, so no other count exists | BRK-STD-03 4.2 ("whoever transmits it") |
| SF3 | average monthly formal entries in 2027 | the year's forecast formal entries over twelve | the busiest month | none | BRK-STD-03 4.2 ("the average month of the plan year") |
| SF4 | the load that places a post | forecast monthly formal entries over posts, the posts already placed in the review counted | the post being placed counted too | Dorval 1, five held (asserted) | BRK-STD-03 4.5 ("counting the posts already placed in this review") |
| SF5 | exceeds 560 | strictly above | at or above | same call (no load at a step or the stop within 25 of 560, asserted) | BRK-STD-03 4.5 and C1 |
| SF6 | the plan year's exchange rates | the 2027 network plan's planning rates | the last customs rate on file; the base year's average | the last rate (with the golden's shares) files a post at every gateway (R0f, asserted) | BRK-STD-03 4.3 ("on the network plan for the year, its shipments and its planning assumptions") and the plan's assumption 7 |
| SF7 | the forecast's shipments | the plan's 2027 shipments with the profile of each gateway's twelve months to September 2026 | the two years' profile | same call and the same monthly forecasts to the nearest 50 (asserted) | the plan's assumptions 1 and 2 ("The twelve months October 2025 to September 2026", "as in the base") |
| SF8 | the plan's growth | plan 2027 shipments over the base year's, by gateway | month by month | same call (the plan's months are the base months grown, asserted to 0.1) | C1 |
| SF9 | price levels in 2027 | as in the base year, each in the currency its goods hold | every price 1 to 3 per cent lower or higher, invoice and CAD prices alike | same call from 0.98 to 1.03 (asserted) | the history (no list price moved in two years in either currency) and C3 |
| SF10 | OGD-program shipments | formal whatever their value | routed on value alone | Calgary 1, five held (R2e, asserted) | CLR-OPS-11 3.1 (b) |
| SF11 | a shipment amended after release | the later extract's row once | both rows | same call and bins (asserted) | C1 |
| SF12 | the month of a release | the gateway's local release date | the UTC timestamp's date | same call and bins (asserted) | the extracts note and C1 |
| SF13 | shipments under CAD 2,500 | outside the check; none can cross CAD 3,300 at any plan rate (the largest rise is 6.5 per cent) | re-routed too | same call | C1, asserted |
| SF14 | the line | value for duty in CAD over 3,300.00 | at or over | same call (no value within CAD 0.75 of the line at the plan's rates, and no CAD value on file at 3,300.00, asserted) | CLR-OPS-11 3.1 (a) and C1 |
| SF15 | a shipment invoiced in CAD | converted at 1 | none | same call | CLR-OPS-11 3.2 |
| SF16 | rounding | the placement on unrounded loads; figures rounded once for the report | loads rounded before comparing | same call | BRK-STD-03 4.5 and the prompt |
| SF17 | tie-break | none needed: no two loads within 5 of each other at a placement step (asserted) | by gateway code | same call | C1 |
| SF18 | the plan's volumes | thousands of inbound international shipments to one decimal | units | none | the plan's own heading |
| SF19 | the value a 2027 shipment carries | by segment: the base-year invoice value (re-routed at the plan's rate) for the share whose repeats keep their invoice values, the base-year CAD value (the route on file) for the share whose repeats keep their CAD values | every shipment at its base-year invoice value (rival b); every shipment at its base-year CAD value (the default's basis) | the first files Dorval 2, four held; the second the default, one post at each gateway (both asserted) | the history, not a sentence: Calgary's US-dollar goods 13,169 repeats at the same CAD value against 117 at the same invoice value, the Chinese goods at Mississauga 2,161 against 24 and Richmond 3,731 against 50, every other segment's repeats at their invoice values (54,126 of 54,444); within those consignments the CAD value holds (slopes 0.009 to 0.013) or moves one for one (0.970 to 1.000); Calgary's 15 CAD price points recur in both years while their US-dollar invoice values move against the rate. No document files how the goods are priced (asserted) |
| SF20 | the pass-through estimator | shares of repeat shipments by gateway and invoice currency, the full key (gateway, importer, tariff item, currency, value to the cent), the year before against the base | shares counted by consignment; both years matched each way; the key without the tariff item, alone or counted by consignment; the CAD value within a cent, alone or by consignment; the CAD value to the dollar; the within-consignment regression of the log CAD value on the log rate; the regression of the change in the log CAD value on the change in the log rate; each repeat routed as its own consignment behaves; the world's truth | same call and every rounded figure (asserted, twelve constructions) | the data: every estimator lands each segment within 0.02 of its share |
| SF21 | the segment a share is estimated for | gateway and invoice currency | one share for the network; one per invoice currency; one per gateway | Dorval 2, four held; Dorval 2, four held; the golden's placement on other figures (Mississauga 540 and Richmond 520 a post, Richmond 3,150 a month) (all asserted) | the data: the US-dollar goods keep their invoice values at the four other gateways (0.980 or more) and their CAD values at Calgary (0.009); at Mississauga and Richmond the Chinese goods keep their CAD values (0.011, 0.013) and the US-dollar goods their invoice values (1.000); homogeneity across the twelve segments rejected (71,119 on 11 degrees of freedom) |

## Ladder

| Rung | Construction | Mississauga, Dorval, Richmond, Calgary, Winnipeg (2027 monthly formal entries) | Posts placed and held | Dies to |
|---|---|---|---|---|
| R0 (default) | base-year formal entries per shipment carried on the plan | 4,173, 3,216, 3,484, 2,605, 1,730 | one at each gateway, one held | the plan's rates move the line for the invoice-priced goods |
| R0b | log-linear trend with month effects on the monthly formal entries | 4,438, 3,320, 3,527, 2,605, 1,875 | one at each gateway, one held | the trend carries the US dollar's rise through the price points |
| R0c | additive-trend, seasonal exponential smoothing | 4,546, 3,393, 3,755, 2,590, 1,876 | Mississauga 2, one at each other gateway, none held | the same |
| R0d | the last quarter's formal share on the plan | 4,229, 3,254, 3,603, 2,659, 1,752 | one at each gateway, one held | the same |
| R0e | the network's formal share on each gateway's plan | 5,288, 2,982, 3,449, 1,563, 1,909 | Mississauga 3, Dorval, Richmond, Winnipeg 1, none held | each gateway's own mix |
| R0f | the golden's pass-through at the last customs rate on file | 4,218, 3,227, 3,599, 2,605, 1,749 | one at each gateway, one held | BRK-STD-03 4.3: the plan's rates |
| R1 | the formal share fitted on the month's US dollar and euro rates, at the plan's rates | 3,928, 3,255, 3,425, 2,620, 1,563 | one at each gateway but Winnipeg, two held | the euro price points never crossed in the history, and the crossing is not linear |
| R2 (rival b) | every foreign-currency shipment re-routed at its currency's planning rate | 3,718, 3,601, 3,039, 2,023, 1,501 | Dorval 2, four held | the repeat consignments: Calgary's US goods and the Chinese goods keep their CAD values |
| R2a (rival c) | one pass-through share for the network (0.737) | 3,837, 3,500, 3,156, 2,176, 1,561 | Dorval 2, four held | the segments behave in opposite ways (SF21) |
| R2b (rival d) | one pass-through share per invoice currency (US dollar 0.719) | 3,872, 3,614, 3,198, 2,186, 1,565 | Dorval 2, four held | Calgary's US goods against the other four gateways' (SF21) |
| R2c | the golden's pass-through, every value moved by the US dollar's change alone | 3,669, 3,073, 3,047, 2,600, 1,501 | Dorval 1, Calgary 1, four held | each currency has its own planning rate |
| R2d | the golden's pass-through, only the euro shipments re-routed | 4,203, 3,652, 3,484, 2,605, 1,730 | Dorval 2, one at each other gateway, none held | the US dollar's rate moves too |
| R2e | the golden's pass-through, OGD goods on value alone | 2,318, 2,007, 2,517, 2,258, 990 | Calgary 1, five held | CLR-OPS-11 3.1 (b): OGD goods are formal whatever their value |
| R2f (rival e) | one pass-through share per gateway | 3,771, 3,598, 3,129, 2,600, 1,501 | Dorval 2, Calgary 1, three held, on other forecasts and loads | the Chinese goods and the US goods at Mississauga and Richmond (SF21) |
| R3 (golden) | each segment's pass-through from the repeat consignments, that share re-routed at the plan's rate, the rest at its base-year route, OGD formal, scaled to the plan | 3,743, 3,601, 3,091, 2,600, 1,501 | Dorval 2, Calgary 1, three held | none |

- **Constructions of the golden**, every one the same placement and every rounded figure: the world's own 2027, each
  shipment routed as its own pricing behaves (3,742.6, 3,601.8, 3,090.8, 2,601.7, 1,500.9); the twelve SF20 estimators
  (Mississauga 3,742.6 to 3,755.3, Dorval 3,594.4 to 3,602.0, Richmond 3,090.6 to 3,094.9, Calgary 2,592.6 to 2,601.7,
  Winnipeg 1,500.9 to 1,506.6); month by month on the plan's months; the base year cut by UTC date; amended shipments
  counted twice; the two years' profile instead of the base's (3,732.4, 3,579.8, 3,081.4, 2,623.1, 1,509.0, the same
  figures to the nearest 50, ruled out by the plan's assumptions 1 and 2); every price 2 per cent lower to 3 per cent
  higher.
- **Separation:** the placement steps are Dorval at 720.3, Calgary at 650.0, Dorval again at 600.2; the stop is
  Mississauga at 534.8, 4.5 per cent under 560 (flip condition: Mississauga's 2027 monthly formal entries would have to
  rise from 3,743 to 3,920 for a fourth post). Dorval's second post clears the line by 7.2 per cent (flip: Dorval under
  3,360 a month); Calgary's clears it by 16 per cent (flip: Calgary under 2,240, which every rival that re-routes its US
  goods reaches). Every rival's placement differs from the golden's in at least two buckets but rival (e), which keeps
  the placement and misses Mississauga's and Richmond's figures; the default differs in five of six.
- **Position:** the golden's two-post desk, Dorval, is second of five on the default's loads before posts (643.3 against
  Calgary's 651.3) and gets one post there; Richmond, Mississauga and Winnipeg, which the default all staff, get none.
- **Dominance:** against the default the decisive step shifts Dorval by +12.0 per cent and Mississauga, Richmond and
  Winnipeg by -10.3, -11.3 and -13.3 per cent, against Calgary's -0.2; against the full re-conversion it lifts Calgary by
  28.6 per cent and Mississauga and Richmond by 0.7 and 1.7 per cent; the largest move any rung keeping the history's
  rates makes on Dorval is the smoothing's +5.5 per cent.
- **Grid:** every construction that keeps the base year's routing files a post at Richmond (R0 to R0f); every one that
  re-routes Calgary's US goods at the plan's dollar rate loses Calgary's post (R2, R2a, R2b); one rate for every currency
  or an elasticity fitted on the history holds two to four (R1, R2c); re-routing on value alone holds five (R2e); one
  share per gateway files the golden placement on other forecasts (R2f); only the shares by gateway and invoice currency
  file Dorval 2, Calgary 1, three held on the golden's forecasts.
- **Worth on the graded figures:** against the full re-conversion, the pass-through moves Calgary's bucket, the held
  count, and Calgary's, Mississauga's and Richmond's forecasts and loads (2,000 to 2,600, 3,700 to 3,750 and 3,050 to
  3,100 a month; 505 to 520, 530 to 535 and 505 to 515 a post), and keeps Dorval's and Winnipeg's.
- **Rounding:** each gateway's entries per post is the same five from the unrounded forecast and from the forecast to
  the nearest 50 (535, 515, 515, 520, 500); the unrounded loads sit 1.97 or more from their edges, and the loads from
  the rounded forecasts, fixed by their bins, 0.83 or more (Richmond's 3,100 over six, 516.67); each step's load is 2.2
  or more from its edge (asserted).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every shipment the plan expects at the gateway in 2027, of the profile of its twelve months to September 2026, each at the value its segment holds (the invoice value for the invoice-held share, the CAD value for the CAD-held share) | BRK-STD-03 4.2 and 4.3, the plan's assumptions 1 and 2; the value basis from the history (SF19); C1 |
| 2 Unit of account | a formal entry (one per shipment routed to the desk); broker posts | BRK-STD-03 4.2 and 4.4; the extracts note's grain line |
| 3 Attribution window | calendar 2027; the base year 1 October 2025 to 30 September 2026 by local release date | BRK-STD-03 4.2; C1 on UTC dates (SF12) |
| 4 As-of dating | the extracts pulled 7 October 2026; the establishment at 1 January 2027 | the extracts note; BRK-STD-03 appendix A |
| 5 Version basis | the 2027 network plan issued 18 September 2026; the amended row of an amended shipment | the plan's cover; C1 (SF11) |
| 6 Denominator | posts on the establishment plus posts placed | BRK-STD-03 4.4 and 4.5 (SF1, SF4) |
| 7 Weighting | each shipment once; each segment's share over its repeat shipments | C1; every SF20 estimator files the same rounded figures |
| 8 Window length | the twelve months the plan grows from for the profile; the two years on file for the pass-through | the plan's assumptions 1 and 2; the two years' profile files the same rounded forecasts (SF7, asserted) |
| 9 Boundary inclusivity | over CAD 3,300; exceeds 560 | C1 (SF5, SF14) |
| 10 Rounding path | the placement on unrounded loads; reported figures rounded once | BRK-STD-03 4.5; the prompt (SF16) |
| 11 Tie-break | none | C1 (SF17) |
| 12 Maturity and censoring | none: every base-year month closed at the pull, 2027 not begun | the extracts note |
| 13 Order of operations | estimate the shares, re-route by segment, count, scale to the plan, divide by posts, place one at a time | BRK-STD-03 4.5; C4 n.a. |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | an amended shipment once, its later row | C1 (SF11) |
| 16 Identity normalisation | gateways by code, desk name and plan region; a consignment by gateway, importer, tariff item and currency | the extracts note and the plan's legend; SF20 for the key |
| 17 Netting against gross | none | n.a. |
| 18 Dimensional units | CAD per unit of each currency; the plan in thousands | the plan's legend; the register's rate column (SF18) |
| 19 Code and status semantics | FORMAL and CLVS; OGD program codes | the extracts note; never the stump |
| 20 Integerisation | whole posts | BRK-STD-03 4.5 |
| 21 Clause scope | BRK-STD-03 4.5 per post; CLR-OPS-11 3.1 per shipment | the documents' own clauses |
| 22 Forward window contents | the plan's 2027 volumes and rates; each segment's goods at the value the history shows them holding | the 2027 network plan ships; no 2027 record exists; SF19, SF21 |

## Literal reader

Executed word for word, the prompt, BRK-STD-03 4.2 to 4.5 and appendix A, CLR-OPS-11 2.1 to 3.2 and the 2027 network
plan's volumes and assumptions give, for each gateway, the formal entries of its 2027 shipments (the plan's shipments,
of the profile of its twelve months to September 2026, each routed as CLR-OPS-11 routes a shipment, at the plan's
exchange rates) over its posts, and the placement one post at a time while the highest load exceeds 560. The text is
silent on what a 2027 shipment's invoice value or CAD value will be and on how the year's formal entries are forecast;
filling the gap with the base year's invoice values is an assumption the text does not make (rival b), and filling it
with the base year's CAD values is the default's. The history decides, segment by segment: the consignments repeated
across the two years show which goods keep their invoice values and which their CAD values (SF19), at a segmentation
the data separates (SF21) and with every estimator landing the same figures (SF20). On that basis a 2027 shipment of an
invoice-held segment is routed at the plan's rate and one of a CAD-held segment at the CAD value it holds, so the data
and the design force the method (`determinism-check` section 1). Every term and convention converges or is ruled out by
a quoted sentence or by the history (SF1 to SF21, all asserted in `checks.py`); the easy answers come from easy methods
on the same literal estimand, never from another reading.

## Oracles

- The gateway activity report (monthly inbound shipments, CLVS releases and formal entries since January 2021): the
  history every route reads; it ties on every route and ranks nothing for 2027.
- The 2027 network plan: volumes and assumptions; it ranks gateways by shipments, not by load, and states no formal
  entries and no pricing.
- CLR-OPS-11: how a shipment is routed on its date; every route executes it on the history.
- The year before the base in the high-value check (the 2026 review's four extracts): the evidence for each segment's
  pass-through; it ranks nothing and states no forecast; read on the default path's question (the base year's ratio) it
  is idle, and read for the full re-conversion it is not needed.
- The 2026 network plan (a distractor): last year's volumes and rates, superseded; it states no formal entries.
- The ask files (time and attendance, HR, Brandmoor's statements and portal, the AP register): the asks only; the call
  opens none (asserted).
- None ties only under the golden.

## Ask sheet

**Main call's declared row population:** the eight high-value check extracts, the two gateway activity reports, the 2027
network plan, BRK-STD-03, CLR-OPS-11 and the clearance extracts note. Device and hazard rows in it: 0 (asserted: the call
opens no time and attendance, HR, Brandmoor or AP file, and computed with every ask file removed it is the golden; the
asks computed with every main-call file removed are the asks). Both asks read fiscal 2025-26 (April 2025 to March 2026),
the time and attendance exports, the HR files, the finance cost-centre map, Brandmoor's statements, portal export and
rate schedule, the AP register and the payroll extracts note, outside the call's population. Neither is keyed to the
call, its construction or its figures; no exchange rate, value or route appears on either path; they share no primary
device.

**Ask A. The overtime hours worked at each gateway's brokerage desk in each quarter of fiscal 2025-26, to the nearest
hour** (20 figures; the deck's second slide charts them).
- H18 home: the strain each desk's establishment carries, a measure every gateway carries that the placement does not
  turn on (BRK-STD-03 4.6 has the review report each desk's overtime for the last fiscal year beside its load). Use: the
  deck's second slide and the workbook's overtime table, in the planner's words ("the overtime hours worked at each
  desk").
- Construction: every overtime line (OT15 and OT20 in the legacy export, OT1.5 and OT2.0 in the new) at its hours,
  every call-back at the time between its punches, the last open week of October 2025 once, each line on the desk the
  employee was assigned to on the work date (the HR assignment changes), the quarter by the work date.
- Primary device (D2, an attribute at the wrong vintage): each time and attendance line carries the employee's home
  cost centre as the export found it (31 October 2025 for the legacy export, 6 October 2026 for the new one), so the
  brokers who moved between desks carry their new desk on the hours they worked at the old one; every desk sends or
  receives a mover in every quarter.
- Second device (D1, the same records under two key schemes): the migration loaded the open timecards of 27 to 31
  October 2025 into the new system as they stood (source MIGRATED, employee numbers and earning codes in the new
  scheme, the legacy hours and punches), so those days stand in both exports, line for line (asserted), and no
  exact-duplicate check pairs them.
- Third device (D3, one column meaning two things by code): a call-back line's hours are the paid minimum of three
  where the call-back was shorter; its punches give the time worked.
- Hazards: HA1 the legacy export's dates month first (MM/DD/YYYY) beside ISO dates; HA2 legacy and new pay codes (the
  payroll note names CALLB and CB call-back overtime); HA3 cost centres in two schemes, mapped in the finance file; HA4
  trainees beside licensed brokers on every desk.
- Stops (computed at the build and asserted, the nearest cell to the golden): S1 the line's home cost centre, every
  figure off, nearest 4.0 hours; S2 call-backs at their paid hours, every figure off, nearest 2.42; S3 the migration
  week twice, every October to December figure off, nearest 2.30; S4 all three (the cracker), every figure off, nearest
  1.30; S5 the HR staff file's current desk for every line, every figure off, nearest 2.35. Every golden figure sits
  0.167 hour or more from its rounding edge.
- Span: the two time and attendance exports, the HR staff file, the HR assignment changes, the finance cost-centre map
  and the payroll extracts note (6 files); employee number and legacy id, work date, pay code, hours, punch in, punch
  out, home cost centre, source; effective date, change, from desk, to desk; cost centre, scheme, desk.
- Realism: time and attendance exports join the employee master when they are pulled, a system migration carries the
  open week across, and a call-back pays a minimum.

**Ask B. What Brandmoor charged, before tax, for the entries it transmitted for each desk in each quarter of fiscal
2025-26, to the nearest dollar** (20 figures).
- H18 home: the cost of the overflow each desk sends out, which the review sets beside its load (BRK-STD-03 4.6). Use:
  the workbook's contract broker table, in the planner's words ("what Brandmoor charged us").
- Construction: each statement's charges before tax (entry fees, rush surcharges and the monthly minimum adjustment,
  once) on the month its entries were transmitted (the month before the statement's), Mississauga's February 2026
  transmissions as re-issued on 23 March 2026 (the original reversed by credit memo BCM-2026-00118 of 6 April 2026),
  March 2026's transmissions from the statements of 1 April 2026 in the AP register.
- Primary device (D8, a settlement date for the event date): Brandmoor issues each statement on the first business day
  of the month after the transmissions it bills, titles it with its issue month, and the AP register posts it then, so
  the statements and the postings run a month behind the entries; they agree with each other on every handling.
- Second device (D5, a silently partial extract): the portal export (the portal's JSON statement detail) was pulled by
  statement month (April 2025 to March 2026), so it holds the transmissions of March 2025 to February 2026; March 2026
  is absent from it.
- Third device (D6, an event's quantity on every line it covers): the portal export repeats its statement's minimum
  charge adjustment on every entry line of the statement.
- Fourth device (D2, a replacing restatement): Mississauga's statement for its February 2026 transmissions (issued 2
  March 2026) carried 64 entries flagged rush in error; it was disputed and re-issued on 23 March 2026, and the credit
  memo reversing the original is dated 6 April 2026, after the year end.
- Hazards: HB1 GST, HST and QST on the statements, Dorval's in French; HB2 schedule B's 2026 rates apply to statements
  issued from 1 February 2026, and the portal shows every line at the 2026 rates whatever its statement; HB3
  Brandmoor's client codes for the desks; HB4 entries on the portal export with their timestamps in Eastern time.
- Stops (computed at the build and asserted, the nearest cell to the golden): S1 the AP register by posting date (the
  cracker, reconciled to the statements), every figure off, nearest CAD 108.05; S2 the statements by their titled
  month, every figure off, nearest 108.05; S3 the portal by transmission date with the adjustment on every line, every
  figure off, nearest 437.90; S4 the portal by transmission date with the adjustment once, every figure off, nearest
  189.90; S5 the disputed original kept beside its re-issue, Mississauga's January to March off by 3,704.40. No golden
  figure sits on a half dollar.
- Span: the statements, the portal export, the AP register, the rate schedule, the finance cost-centre map and the
  payroll extracts note's vendor lines (6 files); statement number, statement month, issue date, desk, entry lines,
  rush, minimum adjustment, subtotal, taxes; transmitted, statement, client code, fee; posting date, cost centre,
  net.
- Realism: a contract broker bills last month's work on the first of the month, a client portal filters by statement,
  and a billing system prints a statement's adjustment beside every line it covers.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 month-first legacy dates | the legacy export's locale | Ask A, April to October 2025 | lines on days 1 to 12 move quarters when read day first |
| HA2, HA3 two pay-code and cost-centre schemes | the time and attendance migration | Ask A | none when mapped |
| HA4 trainees on the desks | the establishment's trainee posts | Ask A | none: every desk employee counts |
| HB1 sales taxes by province | Brandmoor's statements | Ask B | the taxes, when read as charges |
| HB2 the 2026 schedule | the rate revision and the portal's current rate card | Ask B, every quarter on the portal path | the portal's fees at 2026 rates for every 2025 statement |
| HB3, HB4 client codes and Eastern time | Brandmoor's portal | Ask B | none when mapped |

**Referee.** For Ask A the HR assignment changes give each mover's desk on each day; for Ask B the portal's transmission
dates give each statement's month. Each is a source the golden reads, not a control: the time and attendance totals,
the statements and the AP register each tie on every handling. No filed sentence says when a home cost centre was
stamped or which month a statement bills (asserted).

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A overtime hours (20) | both exports stacked, codes mapped, each line on its home cost centre, call-backs at their hours, the migration week twice | every desk and quarter off (computed at the build) | miss |
| B Brandmoor charges (20) | the AP register by posting date, reconciled to the statements by their titled month | every desk and quarter a month behind (computed at the build) | miss |
| the deck's overtime chart | the cracker's hours drawn as the golden draws them | its bars carry Ask A's miss | outside |

Mirror leakage: 10 per cent of the ask weight. The mirror is now the most attractive wrong rung, rival (b), every
shipment re-routed at the plan's rates; it runs the same ask paths as the cracker, so it misses every Ask A and Ask B
figure the cracker misses and keeps only the deck's chart form (one bar per desk in each quarter, the five desks, the
four quarters).
Pair ceiling: 37 (the cracker about 48 with the call, its components, the instructions and the chart's form; the
mirror about 26 with the instructions, the chart's form and the call's components it shares: Mississauga's, Dorval's,
Richmond's and Winnipeg's buckets, Dorval's and Winnipeg's forecasts and loads, two of the three step loads; it misses
the call, Calgary's bucket and the held count, Calgary's, Mississauga's and Richmond's forecasts and loads and the
blocking load).

## Build record

**Stage 3, 2026-10-15** (first cut, target.zip c150b43f): checks 148, verify, byte-identical rebuilds, figures_check,
precut, voice-check, leak.py REVIEW answered, heart WARN, surface with task446 promoted on the card signature.

**Stage 4, 2026-10-15.** The leak reader was clean (Q1 to Q4 none, Q6 analytical, every REVIEW line harmless; its ask
readings are the devices: desk by assignment date, call-backs at punch time, the minimum once, the transmission month).
The judge returned DETERMINISTIC and APPROVE (`determinism_check_report.md`) with two findings, closed in the repair
(target.zip db04473c): the per-post rounding fork (the plan's growth re-set so both rounding routes give the same five)
and Gate H borderline on rule application (the plan's assumption 2 no longer filed the goods' invoice prices; the two
years of extracts carried the pricing instead). The re-judge returned DETERMINISTIC and APPROVE again, its Gate H line
still reading the repricing as partly rule execution.

**Rule 3 rework, 2026-10-15.** The client's strict reading of rule 3: with the plan's rates filed as the year's rates
and the clearance manual valuing each shipment on its invoice, re-routing every base-year shipment at the plan's rates
is a filed assumption executed through a filed rule, so a golden that is that re-routing lands from the HOW sentences
with no modelling choice left. The decisive step moved to the exchange-rate pass-through: importers differ in the
currency their prices are set in, the mix differs by segment, and the golden estimates each segment's share from the
repeat consignments. The world now prices Calgary's US-dollar goods (99 per cent of them, its background goods and 15
price points from CAD 3,329 to 3,399) and the Chinese goods at Mississauga and Richmond (99 per cent) in Canadian
dollars, invoiced at the day's conversion; a few per cent of the euro, sterling, yen and Dorval's US-dollar goods are
priced in CAD too, where their wedge at the plan's rates is small; every price point sits on a standing consignment
(one tariff item per importer's line), so both pricing kinds recur at the same rate per consignment; a base-year
shipment that would repeat a consignment of the year before on both values (a day of the same rate) is not drawn. The
call is kept (Dorval 2, Calgary 1, three held) on new forecasts (Mississauga 3,750, Dorval 3,600, Richmond 3,100,
Calgary 2,600, Winnipeg 1,500; loads 535, 515, 515, 520, 500), the plan's growth re-set (Mississauga 2.5, Dorval 3.3,
Richmond 3.9, Calgary 4.0, Winnipeg 2.2 per cent) so every forecast sits 15.6 or more from its 50 edge and every load
1.97 or more from its 5 edge. No filed sentence names pass-through, repricing or how a 2027 value is formed (asserted);
the plan states its volumes and its rates as the year's rates; the evidence sits in the extracts' own columns, no
single-purpose file or column. The prompt and the asks are unchanged.

**Rivals and the margins by which the data rejects them.** (a) the default, the base year's formal entries per shipment
carried: one post at each gateway, one held. (b) every foreign-currency shipment re-routed at the plan's rates
(pass-through one everywhere): Dorval 2, four held, Calgary at 2,023 a month (505.7 a post on four); the data puts
19,061 of the 19,252 repeats in the three CAD-held segments at the same CAD value (Calgary's US-dollar goods 0.009, 95
per cent interval plus or minus 0.002, about 1,200 standard errors from one; the Chinese goods 0.011 and 0.013), and
their within-consignment slopes of the log CAD value on the log rate are 0.009 to 0.013 against the one the rival
assumes. (c) one share for the network (0.737): Dorval 2, four held, Calgary at 544.0 a post on four; the twelve
segments split into two groups (0.958 to 1.000 and 0.009 to 0.013) and homogeneity is rejected with a statistic of
71,119 on 11 degrees of freedom, Calgary's share about 900 standard errors under the pooled one. (d) one share per
currency (US dollar 0.719): Dorval 2, four held, Calgary at 546.6; the other four gateways' US-dollar goods sit at 0.980
or more. (e) one share per gateway: the golden's placement on other figures (Richmond 3,150 a month, Mississauga 540 and
Richmond 520 a post), the Chinese and US goods at Mississauga and Richmond behaving in opposite ways. Every SF20
estimator files the golden's placement and every rounded figure; the estimators that count a CAD value rounded to the
whole dollar without the tariff item, or once per key, are not among them: a large importer's one-off shipments meet
others in the same dollar by chance (about 2,000 at Mississauga), which no repeat consignment does.

**Gates after the rework:** checks 189 assertions, 0 failed; verify from the bundle alone equal to figures.json, the
workbook (now with its Forecast basis sheet) and the deck; two builds byte-identical (target.zip sha256 2ef27adf);
figures_check exit 0 (133 figures); precut exit 0 (49 checks, no FAIL or WARN, pair ceiling 37); voice-check PASS (the
prompt unchanged, 867 characters); containers clean (target and golden); leak.py REVIEW, no LEAK; guard check and heart
WARN (repeat.gate_g; the older same-driver match a NOTE, differentiated on the card), surface exit 0 with task446
promoted on the card signature as before, for the author's clone-check; validate 184 cards, 0 invalid. freeze.py
against the stage 4 snapshot: the call, the posts placed, the prompt and all 40 ask figures are unchanged; the
forecasts, loads and blocking load, the card's stump and driver and the note's ladder and default path move, by design
(a re-root of the decisive step, not a repair of a reading).

**leak.py REVIEW lines, each harmless:** 117, 165 and 500 inside Brandmoor amounts, and 500 inside CLR-OPS-11's CAD
2,500 check floor, three-digit coincidences; BRK-STD-03 carries the call's words because the call is made under it and
states no placement; the design-note vocabulary in BRK-STD-03, CLR-OPS-11 and the two notes is the field's own (invoice,
currency, shipment, the gateways' names), and no document says how the goods are priced, how a rate passes into a value
or connects the plan's rates to the routing (asserted).

## Tried and rejected

- The seed's own architecture (the entry forecasts' 80th-percentile error at twelve months as the bar): not drawn; it
  leans on a filed back-test organ and its decisive step was the error record's construction, decoy-era design.
- A lower bound from the forecast's record (ex-post against ex-ante errors of a plan-driven forecast): rejected on
  paper; the plan's past variances against actuals are a column in any volume report, so the decisive step reads off
  the schema.
- New-account volume not yet signed as the decisive step: rejected on paper; the gateway totals' own trend carries the
  historical new-business rate and lands near it, so a reflex reaches the golden.
- Account ramp curves by months since go-live: rejected on paper as the same latent structure as task134 v2 (a
  forward quantity set by an age profile after a surge).
- Capacity-capped filed entries (demand above a desk's capacity sent to the contract broker): rejected on paper; which
  entries count is a reading of the estimand, and the overflow file hands it over.
- Brandmoor's dispute on Richmond's January 2026 statement: too small to move any Richmond cell out of its bin; the
  dispute moved to Mississauga's February 2026 statement, 64 entries flagged rush in error.
- A December 2025 rate credit on the January 2026 statements: it dated the statements' billing month on their face and
  handed over the timing device; dropped, the 2026 rates now apply by statement issue date.
- The portal at each statement's own rates: the portal path reproduced the golden for April to December 2025; the portal
  now shows every line at the rate card in force when it is viewed.
- The first time and attendance stream: a Winnipeg January to March figure fell on the half hour (quarter-hour punches)
  and the legacy overtime hours differed from their punches by up to a third of a minute a line; the stream was redrawn
  and the legacy clock's overtime minutes kept to multiples of three, so its hundredths of an hour are exact.
- The pack in the same four formats as task143 (csv, pdf, txt, xlsx): guard surface promoted the pair on format and
  layout alone; the portal export now ships as the portal's JSON and CLR-OPS-11 as Clearance Operations' Word file.
- The plan filing the goods' invoice prices (assumption 2: "the prices those goods are invoiced at, as in the base"):
  with BRK-STD-03 4.3 and assumption 7 it spelled the re-routing out, and the judge read part of the decisive step as a
  stated assumption executed through a stated rule; the clause was dropped and the two years of extracts now carry the
  pricing (list prices and repeat consignments at their invoice values, CAD values moving with the rate).
- Entries per post at the first growth figures: from the forecast to the nearest 50 they rounded to 530 at Mississauga
  and 500 at Winnipeg against 525 and 505 from the unrounded forecast; the plan's growth was re-set by gateway so both
  routes give the same five everywhere.
- Standing consignments drawn above the check's floor at the lowest rate of the two years: they sat higher in the value
  distribution than the fresh shipments and lifted every gateway's formal share about 2 per cent; drawn at the two
  years' average rate instead.
- full repricing at plan rates: rule application (filed assumption plus filed rule), per the rule 3 read
- Annual repricing to hold the CAD price (the invoice value reset once a year): rejected on paper; within a year such a
  consignment repeats at one invoice value and across years at neither value, so the repeats carry no clean signal and
  a regression's share depends on how consignments are paired across years; the CAD-priced goods are invoiced at the
  CAD price converted at the day's rate instead.
- CAD pricing at 2 to 5 per cent in every segment: a US-dollar invoice converted from a CAD price lands a cent either
  side of the price on about three conversions in ten, so counting repeats by consignment doubled the CAD-held
  consignments, and a CAD value to the whole dollar met chance matches; Mississauga's, Richmond's and Winnipeg's
  forecasts moved across their bins by estimator. CAD pricing stays out of the segments with a large wedge at the plan's
  rates unless it is near total (Calgary's US goods, the Chinese goods, whose fine currency unit hits the CAD price to
  the cent).
- Price points drawn fresh for each shipment (a random importer and tariff item): the CAD price points were sparse
  combinations against dense invoice ones, so a consignment-weighted share moved Calgary across its load bin; every
  price point is now a standing consignment, one tariff item per importer's line.
- Calgary's US goods the only CAD-held segment: the full re-conversion then missed only Calgary's bucket, forecast and
  load and the held count and kept twelve of the call's sixteen per-gateway figures, a mirror near the pair ceiling;
  the Chinese goods at Mississauga and Richmond are CAD-priced too, so it misses their forecasts and loads as well.
- Richmond's forecast in the 3,050 bin (3,036.5 a month): 3,050 over six posts is 508.33, which rounds to 510, while the
  unrounded load, 506.1, rounds to 505; the plan's growth for Richmond was set so the forecast sits mid-bin at 3,100.
