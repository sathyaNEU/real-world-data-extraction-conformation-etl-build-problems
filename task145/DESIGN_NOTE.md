# task145: Larchwood Express Canada, where six broker posts go across five gateways for 2027 (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC16. The seed (an express carrier's customs brokerage
placing six new broker posts across five import gateways, or holding them, on each gateway's forecast entries per
broker) was read at its header and Situation only. Its world, decision and quantity are kept: an express carrier's
licensed customs brokers file formal entries at five import gateways, six new broker posts are funded for 2027, a post
goes to the gateway with the most forecast entries per broker while that load is above the standard, and the rest are
held. The seed's mechanism (the entry forecasts' own error record setting a lower bound) is decoy-era design and is not
used; no back-test organ ships. The pitfall is re-found from how the records come to exist: a shipment needs a broker's
formal entry only when its value, set in the currency it is invoiced in, exceeds CAD 3,300 once converted at the
customs rate of its date, so a gateway's formal entries are the part of its shipments' value distribution that sits
above a line fixed in Canadian dollars, and the network plan sets 2027's exchange rates where no month of the history
has been.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task145.json`, architecture v1, registered 2026-10-15 after `git pull` (task262, task455 and task144 on file); `guard.py check` WARN (repeat.gate_g, answered below), no BLOCK; `guard.py validate` clean |
| Domain / task type | `economics-econometrics` (client domain; Economics & Econometrics has never carried a forecasting build), task type `forecasting-forecast-evaluation` (forecasting): the call rests on a conditional forecast of each gateway's 2027 formal import entries on the plan year's exchange rates, built from the declared values of the shipments the forecast carries |
| Objective | Forecasting & Predictive Modeling: each gateway's average monthly formal entries in calendar 2027, a window not yet open, on the 2027 network plan, and from it the broker posts placed and held |
| Shape | `05` allocation to a fixed total (the six posts across five gateways and the held bucket): six bucket counts, each gateway's forecast monthly formal entries and its entries per broker post once placed (10), the call and the blocking load (2), the asks' 40 figures and the deck's named parts; about 60 criteria |
| Decision | `allocation_to_total`, answer unit `count` (broker posts per gateway and held) |
| Mechanism | gap time (decisive: the routing the history records belongs to the exchange rates of its months, the plan year's rates differ, and at the euro rate no month since January 2021 reached) then population (OGD-regulated shipments are formal whatever their value, so a value-only re-routing drops them); pattern none, generators G16 decisive (the forecasting method: carry each shipment's invoice-currency value and re-apply the line, not the count, its share or a fitted elasticity), G13 (the plan year's window and its rates); Gate G `forecasting`; strategy `forecast_method_backtest` (stumping F6: the invariant is constructed, the natural fit fails forward) |
| Layer 2 family / pattern | `field_method`; `own:formal-entry-count-re-routed-at-the-plan-years-exchange-rates`: the field's way of projecting declarations above a nominal threshold (re-applying the line to the value distribution held in its invoice currencies at the projection's rates) against the generic move (extrapolating the count) |
| Furniture | forum `executive_team` (the Canada leadership team approves the brokerage establishment at its review of 22 October 2026), forcing event `vote_or_meeting` (that establishment review), organisation family `logistics_or_3pl` (Larchwood Express Canada, an express carrier), role family `capacity_planner` (the brokerage workforce planning lead), context artifact `filed_standard` (BRK-STD-03, the brokerage staffing standard, which files the placement rule and the forecast's basis and no method), calibration `none`, opening `question-first`, question form `where` |
| Spine | `highvalue_check_2025Q4.csv` to `highvalue_check_2026Q3.csv`, the clearance system's quarterly high-value check extracts (every inbound international shipment released with a value for duty of CAD 2,500 or more, and every OGD shipment, in two layouts), 246,908 rows (246,894 shipments, 14 amended shipments twice) over the twelve months to September 2026; constructed. The pack is 22 files in six formats (csv, docx, json, pdf, txt, xlsx) |
| Deliverables | `broker_posts_2027.xlsx` (the placement, each gateway's forecast and load, the two ask tables), `establishment_review_2027.pptx` (two slides for the leadership team: the placement and the desks' overtime by quarter) |
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
each unit's value, fixed in its own denomination, lands once converted at the forward period's factors; the history's
count, its share of all units and any sensitivity fitted to the history carry only the factors the history saw, so
forward factors that carry a cluster of values across the line in a direction no past period reached raise one
candidate's count and lower the others', and only re-applying the line to each unit's own value at the forward factors
gets the count. The three nearest on file (`guard.py check`): task253 v3 (units with a latent level below a line, seen
through noisy averages, 0.08), task98 v5 lineage (units scored on the class they had at entry, 0.07), task107 v4 (a
group under a line only on an entry rate its counterparty lifts at an anniversary, 0.07). None converts a unit's value
between denominations or moves a line through a forward conversion factor; task107's is a dated step in a rate the
history shows exactly, here the forward condition is a level the history never reached. task446 v2 (the closest in
shape, a derived rate carried onto a moved condition) has a classifier, a base rate and Bayes' rule; here the derived
quantity is a tail mass of a value distribution under a change of scale, and the shift is non-linear (clusters of price
points cross or leave the line), so no elasticity fitted on the history can carry it.

**Data-native sentence.** Larchwood's clearance system routes a shipment to a gateway's brokerage desk for a formal entry
when its value for duty, declared in the currency of its commercial invoice, exceeds CAD 3,300 once converted at the
customs exchange rate for its date, or when its goods fall under another government department's program; everything
else is released under the courier low-value program without a broker. European goods priced near EUR 2,000 and US
goods priced near USD 2,350 therefore sit on either side of the line according to the month's rates, so each gateway's
formal entries are the share of its shipments whose invoice values sit above 3,300 divided by the rate, and the 2027
network plan's planning rates (USD 1.340, EUR 1.680) put the euro line below Dorval's European price points, where no
month since January 2021 has had it, and the US line above Richmond's, Mississauga's and Winnipeg's.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (56 builds): renewal (132), conditional
survival (133), hazards by time since entry (134), selective labels (141), a period total built from its units (142), a
shared group effect (143), a feed cascade (144), a screen's yield under a moved base rate (446), an age-anniversary rate
step (107): none forecasts a count above a nominal line through a forward exchange rate. `layer2-rigor-patterns.md`,
economics: forecasting-forecast-evaluation/1 (real-time vintages) and /2 (proper scores) are not this build's; the
decisive line is a conditional forecast through the structure (the nearest library line is
healthcare-delivery-health-economics/utilization-access-demand-forecasting/2, project with the rates on the projected
structure against a trend on totals), here the structure being the declared-value distribution in its invoice
currencies and the rate the routing rule converts at. `two-layer-task-design.md`: "the data's real structure" and
"validating a forecast properly" are the client's families for the step. `measured-drivers.md`: held tasks put the
decisive move upstream of every graded figure; here every forecast, every load and every post inherits it.
`strategies.md` F6 (the invariant constructed from a log) and Part 6 (a dated cause stepping the series dies to an event
study: here the forward condition is a level, not a date, and the decisive euro crossing never happened in the
history). The seed's header and Situation (FC16) for the world, decision and quantity only.

**World.** Larchwood Express Canada Ltd. (Mississauga, Ontario) is an express carrier whose inbound international
shipments arrive at five import gateways: Mississauga (YYZ, Toronto Pearson), Dorval (YUL, Montréal-Trudeau), Richmond
(YVR, Vancouver International), Calgary (YYC) and Winnipeg (YWG). Each gateway has a brokerage desk of licensed customs
brokers in the Customs Brokerage department (vice-president Robin Larson). The clearance system values every shipment
on its commercial invoice in the invoice currency, converts it at the customs exchange rate for its date and routes it:
over CAD 3,300, or goods under another government department's (OGD) program, to the desk for a formal entry filed by a
broker; otherwise released under the courier low-value program (CLVS) by clearance operations. Shipments with a value
for duty of CAD 2,500 or more are checked against the commercial invoice before release (the high-value check), and the
check's extracts are pulled every calendar quarter. At peaks a desk sends entries to a contract broker, Brandmoor
Customs Services, which transmits them on Larchwood's account and invoices monthly. The brokerage staffing standard
BRK-STD-03 places new broker posts each autumn for the next calendar year: one at a time, at the gateway whose forecast
average monthly formal entries per broker post (posts already placed in the review counted) is highest, while that load
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
4. Divide by the establishment and run the placement: one post at each of Dorval, Calgary, Mississauga, Richmond and
   Winnipeg, one held.

Ends on: one post at each of the five gateways, one held.
Golden: two posts at Dorval, one at Calgary, three held: every shipment of the twelve months to September 2026
re-routed at the plan's planning rates (value for duty in its invoice currency times the plan's rate for that currency
against CAD 3,300, OGD-program shipments formal whatever their value) and scaled to the plan's volumes gives Dorval about
an eighth more formal entries (its European goods priced near EUR 2,000 cross the line at EUR 1.680) and Mississauga,
Richmond and Winnipeg about an eighth fewer (their US price points near USD 2,350 to 2,380 fall under it at USD 1.340).

## Stump sentence

A competent solver carries each gateway's formal entries per inbound shipment over the twelve months to September 2026
onto the 2027 network plan's shipments and places one post at each of the five gateways with one held (Ends on); the
step that lands it there is carrying the base year's routing into a plan year whose planning rates move the CAD 3,300
line in every invoice currency: re-routing the base year's shipments at the plan's rates, OGD-program shipments formal
whatever their value, sends Dorval's European goods priced near EUR 2,000 over the line at a euro rate no month since
2021 reached and Mississauga's, Richmond's and Winnipeg's US price points under it, and the placement is two posts at
Dorval, one at Calgary and three held.

## Three rules

- **Task type:** `economics-econometrics`, `forecasting-forecast-evaluation` (serves Forecasting): the call is a
  conditional forecast of each gateway's 2027 formal import entries on the network plan's exchange rates, built from the
  declared-value distribution of the shipments the forecast carries.
- **Domain test:** the deciding quantity is each gateway's 2027 formal entries, which trade economics forecasts
  conditionally on the plan year's exchange rates as the mass of declared values that will sit above a line fixed in
  Canadian dollars once each value, set in the currency it is invoiced in, is converted at the year's rate; the generic
  forecast (the count carried on its share of shipments, its trend, or an elasticity fitted to the monthly history)
  places a post at every gateway, so the call turns on the conditional forecast through the threshold.
- **Swap:** "two of the six posts go to Dorval and three are held because at the plan's euro rate Dorval's European
  goods priced near EUR 2,000 cross the CAD 3,300 line" read with another field's nouns ("two of the six nurses go to
  ward A because at next year's rate ward A's patients cross the line") loses the invoice currency, the conversion at
  the date's rate and the nominal line a price point crosses, so what moves the count stops making sense.
- **Layer 1:** on the call's path, the clearance system's high-value check extracts come in four quarterly files whose
  layout a February 2026 release changed (column names, date formats, the rate column's label); release times are
  stamped in UTC beside each gateway's local release date; a few shipments amended after release appear again in the
  next quarter's extract; the gateway monthly report has two layouts (the legacy brokerage system to September 2024
  counted formal entries by accounting date, the new one by release date); gateways are keyed by airport code, desk name
  and the plan's region labels; the plan's volumes are in thousands to one decimal; OGD program codes are blank or NONE
  where none applies; shipments are invoiced in CAD, USD, EUR, GBP, CNY and JPY, each row with the customs rate of its
  date. On the ask paths, two time and attendance systems (legacy to 31 October 2025, new from 1 November 2025) with two
  employee-number and pay-code schemes and the migration's carried week, the HR assignment history, call-back lines at
  the paid minimum, and the contract broker's monthly invoices, portal detail and a re-issued invoice. Each is what these
  systems write; none decides the call (each mishandled leaves the placement where it was, asserted: R2).
- **Layer 2:** `field_method`: the shortcut carries the base year's routing outcome (formal entries per shipment, their
  trend, or their fitted sensitivity to the rate) into the plan year; the expert carries each shipment's value in its
  invoice currency and re-applies the CAD 3,300 line at the plan year's rate for that currency, OGD shipments formal
  regardless, because the count above a nominal line is the tail of the value distribution under the year's conversion.
- **Decisive step:** forecasting each gateway's 2027 formal entries by re-routing its shipments of the twelve months to
  September 2026 at the 2027 planning rates (each shipment's value for duty in its invoice currency converted at the
  plan's rate for that currency, compared with CAD 3,300, OGD-program shipments formal regardless) and scaling to the
  plan's volumes, instead of carrying the base year's formal entries per shipment, their trend or an elasticity fitted
  to the months the history saw.
- **Not semantics:** every field, code, unit and definition can be read correctly (the value for duty in its invoice
  currency, the customs rate of its date, the value in CAD, the route, the OGD program, the line at CAD 3,300, the
  plan's volumes in thousands, the establishment) and the default path reads them all correctly and still places a
  post at every gateway, because it carries the base year's outcome; nothing in the pack says the plan's rates change
  the routing, and the answer moves only on how the 2027 count is forecast.
- **Not rule application:** BRK-STD-03 files the placement rule and the forecast's basis (the 2027 network plan's
  shipments and planning assumptions) and the clearance manual files how a shipment is routed on its date; no rule or
  procedure says how the plan year's formal entries are forecast, and executing every filed rule with the history's
  routing (which the system already applied at each month's rates) files a post at every gateway, so the step that moves
  it to two at Dorval, one at Calgary and three held is performed by no filed rule.
- **Analyst test:** a strong analyst who reads the staffing standard, the clearance manual and the network plan
  correctly forecasts each gateway's 2027 formal entries as the plan's shipments times its formal entries per shipment
  over the twelve months to September 2026 and places one post at each of the five gateways with one held (Ends on);
  the entries' own trend files the same placement, an elasticity of the formal share to the US and euro rates fitted on
  the monthly history and a re-routing at the US rate alone each hold more posts with one at Dorval, and only re-routing
  every shipment at its own currency's planning rate, OGD shipments kept formal, files two at Dorval, one at Calgary and
  three held (R3a and R3b asserted on the generator's clean truth).
- **Estimand:** BRK-STD-03 (`brk_std_03_brokerage_staffing_standard.pdf`) section 4: a gateway's load is its forecast
  average monthly formal entries in the plan year (every formal entry for a shipment released at the gateway in calendar
  2027, whoever transmits it) divided by its broker posts (the establishment at 1 January of the plan year and the
  posts already placed in the review); the forecast is made on the network plan for the year, its shipments for the
  gateway and its planning assumptions; posts placed one at a time while the highest load exceeds 560, the rest held.
  The network plan's assumptions page fixes the plan year's volumes, its shipment profile (each gateway's lanes,
  customers and goods as in the twelve months to September 2026) and its exchange rates; nothing files the forecast's
  method.
- **No decoy:** nothing is planted to be caught: no copied block, no hidden rule, and no memo, draft, briefing or
  stakeholder figure states a forecast, a load or a placement; the network plan states volumes and assumptions, the
  clearance manual the routing rule, and no document ranks the gateways on the decision; the distractors (the 2026
  network plan as issued in September 2025 and the export desk's declaration report) rank nothing.
- **No certified replay:** no published forecast, certified load or past placement ships to be reproduced; the method
  is forced by the routing rule and the plan's rates acting on the shipments on file, and no closed figure is matched
  to recover it.
- **Lesson:** a count of items above a fixed nominal line is the upper tail of their value distribution after
  conversion, so its history carries every exchange-rate move the window saw and none it did not; a forecast for a year
  whose rates differ re-applies the line to the values in the currencies they are set in, and a price point the
  history never saw cross can move a whole gateway; no build on file teaches a nominal threshold under a forward
  exchange rate (task446 teaches a screen's yield under a moved base rate, task107 an anniversary step in a rate the
  history shows exactly).

## Readability screen

| Rung (the move that climbs it) | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0: base-year formal entries per shipment carried on the plan (the default) | BRK-STD-03 4.3 and the plan's volumes | the gateway report's two columns | yes, the planner's ratio | no | no | yes, one ratio | readable |
| R0b: the formal entries' own trend (log-linear or exponential smoothing with seasons) | no | the 69-month series | yes, a forecasting default | no | no | no | readable |
| R1: the formal share fitted on the month's US dollar and euro rates, evaluated at the plan's rates | the plan lists its rates | the gateway report and a rate per month | no | no | no | yes, a regression | readable |
| R2: re-routing every foreign value at the US dollar's change alone | the routing clause names conversion | the register's rate column | no | no | no | yes, one factor | readable |
| R2b: re-routing at the plan's rates on value alone, the OGD program ignored | the routing clause names both tests | the register's OGD column | no | no | no | no | readable |
| R3 (decisive): every shipment of the twelve months to September 2026 re-routed at its own currency's planning rate against CAD 3,300, OGD shipments formal regardless, scaled to the plan's volumes | none: no sentence connects the plan's rates to the year's routing or to formal entries (asserted); CLR-OPS-11 states how a shipment is routed on its date and the plan lists its planning rates among nine assumptions, both read by the default path | the register's value, currency, customs rate and CAD value are the clearance system's audit trail of each valuation; nothing marks a shipment near the line or a route for the plan year | every forecasting reflex carries the routing (the ratio, the trend, smoothing, a fitted elasticity) and lands on a post at every gateway or a post at Richmond | none: no record scores a forecast | none: the battery passes on every route | no: a re-routing of about 247,000 shipments by currency, then a placement | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | broker posts | the establishment's posts at 1 January 2027 (filled or vacant) and the posts placed in the review | the brokers employed today | same call (asserted: the establishment table equals the posts the desks hold) | BRK-STD-03 4.4 ("posts on the gateway's establishment at 1 January of the plan year, filled or vacant") |
| SF2 | formal entries | every formal entry for a shipment released at the gateway, whoever transmits it | only entries the desk's own brokers transmit | the register carries no transmitter, so no other count exists | BRK-STD-03 4.2 ("whoever transmits it") |
| SF3 | average monthly formal entries in 2027 | the year's forecast formal entries over twelve | the busiest month | none | BRK-STD-03 4.2 ("the average month of the plan year") |
| SF4 | the load that places a post | forecast monthly formal entries over posts, the posts already placed in the review counted | the post being placed counted too | Dorval 1, five held (asserted) | BRK-STD-03 4.5 ("counting the posts already placed in this review") |
| SF5 | exceeds 560 | strictly above | at or above | same call (no load within 25 of 560, asserted) | BRK-STD-03 4.5 and C1 |
| SF6 | the plan year's exchange rates | the 2027 network plan's planning rates | the last customs rate on file; the base year's average | the last rate files a post at every gateway (R0 spot, asserted) | BRK-STD-03 4.3 ("on the network plan for the year, its shipments and its planning assumptions") and the plan's assumption 7 |
| SF7 | the forecast's shipments | the plan's 2027 shipments with the profile of each gateway's twelve months to September 2026 | another base window | same call (the register holds only that window) | the plan's assumption 2 and the extracts' coverage |
| SF8 | the plan's growth | plan 2027 shipments over the base year's, by gateway | month by month | same call (the plan's months are the base months grown, asserted to 0.1) | C1 |
| SF9 | invoice prices in 2027 | as in the base year (the plan assumes no change in what shippers invoice) | inflated 1 to 3 per cent | same call from 0.98 to 1.03 (asserted) | the plan's assumptions (none moves invoice prices) and C3 |
| SF10 | OGD-program shipments | formal whatever their value | routed on value alone | every post held (R2b, asserted) | CLR-OPS-11 3.1 (b) |
| SF11 | a shipment amended after release | the later extract's row once | both rows | same call and bins (asserted) | C1 |
| SF12 | the month of a release | the gateway's local release date | the UTC timestamp's date | same call and bins (asserted) | the extracts note and C1 |
| SF13 | shipments under CAD 2,500 | outside the check; none can cross CAD 3,300 at any plan rate (the largest rise is 6.5 per cent) | re-routed too | same call | C1, asserted |
| SF14 | the line | value for duty in CAD over 3,300.00 | at or over | same call (no value within CAD 0.75 of the line at the plan's rates, asserted) | CLR-OPS-11 3.1 (a) and C1 |
| SF15 | a shipment invoiced in CAD | converted at 1 | none | same call | CLR-OPS-11 3.2 |
| SF16 | rounding | the placement on unrounded loads; figures rounded once for the report | loads rounded before comparing | same call | BRK-STD-03 4.5 and the prompt |
| SF17 | tie-break | none needed: no two loads within 5 of each other at a placement step (asserted) | by gateway code | same call | C1 |
| SF18 | the plan's volumes | thousands of inbound international shipments to one decimal | units | none | the plan's own heading |

## Ladder

| Rung | Construction | Mississauga, Dorval, Richmond, Calgary, Winnipeg (2027 monthly formal entries) | Posts placed and held | Dies to |
|---|---|---|---|---|
| R0 (default) | base-year formal entries per shipment carried on the plan | 4,160, 3,209, 3,511, 2,581, 1,742 | one at each gateway, one held | the plan's rates move the line in every invoice currency |
| R0b | log-linear trend with month effects on the monthly formal entries | 4,413, 3,329, 3,518, 2,740, 1,867 | one at each gateway, one held | the trend carries the US dollar's rise through the price points |
| R0c | additive-trend, seasonal exponential smoothing | 4,560, 3,322, 3,738, 2,700, 1,890 | Mississauga 2, one at each other gateway, none held | the same |
| R0d | the last quarter's formal share on the plan | 4,207, 3,188, 3,628, 2,582, 1,744 | one at each gateway, one held | the same |
| R0e | the network's formal share on each gateway's plan | 5,293, 2,985, 3,478, 1,531, 1,921 | Mississauga 3, Dorval, Richmond, Winnipeg 1, none held | each gateway's own mix |
| R0f | the base year re-routed at the last customs rate on file | 4,218, 3,220, 3,640, 2,600, 1,762 | one at each gateway, one held | BRK-STD-03 4.3: the plan's rates |
| R1 | the formal share fitted on the month's US dollar and euro rates, at the plan's rates | 3,896, 3,257, 3,421, 2,462, 1,587 | Dorval, Richmond, Calgary 1, three held | the euro price points never crossed in the history, and the US crossing is not linear |
| R2 | every foreign value moved by the US dollar's change | 3,604, 3,064, 3,007, 2,449, 1,510 | Dorval 1, Calgary 1, four held | each currency has its own planning rate |
| R2a | only the euro shipments re-routed | 4,193, 3,659, 3,511, 2,581, 1,742 | Dorval 2, one at each other gateway, none held | the US dollar's rate moves too |
| R2b | every shipment re-routed on value alone | 2,280, 2,022, 2,488, 2,107, 995 | every post held | CLR-OPS-11 3.1 (b): OGD goods are formal whatever their value |
| R3 (golden) | every shipment re-routed at its currency's planning rate, OGD formal regardless, scaled to the plan | 3,682, 3,606, 3,068, 2,449, 1,510 | Dorval 2, Calgary 1, three held | none |

- **Constructions of the golden**, every one the same placement and the same rounded figures: the year at once
  (3,682.0, 3,606.0, 3,068.1, 2,448.5, 1,510.1), month by month on the plan's months (identical), the base year cut by UTC
  date (3,680.6, 3,604.8, 3,065.8, 2,447.6, 1,509.5), amended shipments counted twice (within 1.2 of the golden),
  invoice prices from 2 per cent lower to 3 per cent higher (the placement unchanged throughout).
- **Separation:** the placement steps are Dorval at 721.2, Calgary at 612.1, Dorval again at 601.0; the stop is
  Mississauga at 526.0, 6.1 per cent under 560 (flip condition: Mississauga's 2027 monthly formal entries would have to
  rise from 3,682 to 3,920 for a fourth post). Dorval's second post clears the line by 7.3 per cent (flip: Dorval under
  3,360 a month). Every rival's placement differs from the golden's in at least two buckets; the default in five of six.
- **Position:** the golden's two-post desk, Dorval, is second of five on the default's loads before posts (641.8 against
  Calgary's 645.3) and gets one post there; Richmond, Mississauga and Winnipeg, which the default all staff, get none.
- **Dominance:** the decisive move shifts Dorval by +12.4 per cent and Mississauga, Richmond and Winnipeg by -11.5,
  -12.6 and -13.3 per cent, against Calgary's -5.1; the largest move any lower rung makes on Dorval is R1's +1.5 per cent.
- **Grid:** every construction without the plan's rates files a post at Richmond (R0 to R0f, R1); every construction
  with one rate for every currency files Dorval 1 (R2); every construction that re-routes on value alone holds every
  post (R2b); only per-currency re-routing with OGD kept files Dorval 2, Calgary 1, three held.
- **Worth on the graded figures:** the decisive step moves every forecast (by -5 to +12 per cent), every load and five of
  the six buckets; no lower rung moves Dorval's forecast by more than 1.5 per cent.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every shipment the plan expects at the gateway in 2027, of the profile of its twelve months to September 2026 | BRK-STD-03 4.2 and 4.3, the plan's assumption 2; C1 |
| 2 Unit of account | a formal entry (one per shipment routed to the desk); broker posts | BRK-STD-03 4.2 and 4.4; the extracts note's grain line |
| 3 Attribution window | calendar 2027; the base year 1 October 2025 to 30 September 2026 by local release date | BRK-STD-03 4.2; C1 on UTC dates (SF12) |
| 4 As-of dating | the extracts pulled 7 October 2026; the establishment at 1 January 2027 | the extracts note; BRK-STD-03 appendix A |
| 5 Version basis | the 2027 network plan issued 18 September 2026; the amended row of an amended shipment | the plan's cover; C1 (SF11) |
| 6 Denominator | posts on the establishment plus posts placed | BRK-STD-03 4.4 and 4.5 (SF1, SF4) |
| 7 Weighting | each shipment once | C1 |
| 8 Window length | the twelve months the plan grows from | the plan's assumption 2; the register's coverage |
| 9 Boundary inclusivity | over CAD 3,300; exceeds 560 | C1 (SF5, SF14) |
| 10 Rounding path | the placement on unrounded loads; reported figures rounded once | BRK-STD-03 4.5; the prompt (SF16) |
| 11 Tie-break | none | C1 (SF17) |
| 12 Maturity and censoring | none: every base-year month closed at the pull, 2027 not begun | the extracts note |
| 13 Order of operations | re-route, count, scale to the plan, divide by posts, place one at a time | BRK-STD-03 4.5; C4 n.a. |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | an amended shipment once, its later row | C1 (SF11) |
| 16 Identity normalisation | gateways by code, desk name and plan region | the extracts note and the plan's legend |
| 17 Netting against gross | none | n.a. |
| 18 Dimensional units | CAD per unit of each currency; the plan in thousands | the plan's legend; the register's rate column (SF18) |
| 19 Code and status semantics | FORMAL and CLVS; OGD program codes | the extracts note; never the stump |
| 20 Integerisation | whole posts | BRK-STD-03 4.5 |
| 21 Clause scope | BRK-STD-03 4.5 per post; CLR-OPS-11 3.1 per shipment | the documents' own clauses |
| 22 Forward window contents | the plan's 2027 volumes and rates | the 2027 network plan ships; no 2027 record exists |

## Literal reader

Executed word for word, the prompt, BRK-STD-03 4.2 to 4.5 and appendix A, CLR-OPS-11 3.1 and 3.2 and the 2027 network
plan's volumes and assumptions give, for each gateway, the formal entries of its 2027 shipments (the plan's shipments,
of the profile of its twelve months to September 2026, each routed as CLR-OPS-11 routes a shipment, at the plan's
exchange rates) over its posts, and the placement one post at a time while the highest load exceeds 560. The text is
silent on how the year's formal entries are forecast; the readings are carrying the base year's routing (its ratio,
trend or fitted sensitivity) and routing the year's shipments at the year's rates. The first contradicts the literal
estimand (a 2027 shipment is routed at the rate of its 2027 date, which the plan sets), so the design forces the method
(`determinism-check` section 1, the design). Every term and convention converges or is ruled out by a quoted sentence
(SF1 to SF18, all asserted in `checks.py`); the easy answer comes from an easy method on the same literal estimand,
never from another reading.

## Oracles

- The gateway activity report (monthly inbound shipments, CLVS releases and formal entries since January 2021): the
  history every route reads; it ties on every route and ranks nothing for 2027.
- The 2027 network plan: volumes and assumptions; it ranks gateways by shipments, not by load, and states no formal
  entries.
- CLR-OPS-11: how a shipment is routed on its date; every route executes it on the history.
- The 2026 network plan (a distractor): last year's volumes and rates, superseded; it states no formal entries.
- The ask files (time and attendance, HR, Brandmoor's statements and portal, the AP register): the asks only; the call
  opens none (asserted).
- None ties only under the golden.

## Ask sheet

**Main call's declared row population:** the four high-value check extracts, the two gateway activity reports, the 2027
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

Mirror leakage: 10 per cent of the ask weight. The mirror (R0, a post at every gateway) runs the same ask paths as the
cracker, so it misses every Ask A and Ask B figure the cracker misses and keeps only the deck's chart form (one bar per
desk in each quarter, the five desks, the four quarters).
Pair ceiling: 34 (the cracker about 48 with the call, its components, the instructions and the chart's form; the
mirror about 20 with the instructions, the chart's form and the one bucket it shares, Calgary's post).

## Build record

Stage 3, 2026-10-15. `python3 task145/generator/build.py`: checks.py 148 assertions, 0 failed (input gates, R1 to R3c,
every rung by name, SF1 to SF18, the bins, every ask stop, the separation line, the distractors, the realism sweep,
each load-bearing fact in one file); verify.py from the bundle alone equal to figures.json, the workbook and the deck;
two builds byte-identical (target, golden, metadata.json, figures.json, target.zip). `figures_check.py` exit 0 (98
figures). Containers clean (`scrub_producer_metadata.py` on target and golden). `voice-check.py` PASS (867 characters).

- The call on the pack: Dorval 2, Calgary 1, three held; forecast Mississauga 3,700, Dorval 3,600, Richmond 3,050,
  Calgary 2,450, Winnipeg 1,500 a month (unrounded 3,682.0, 3,606.0, 3,068.1, 2,448.5, 1,510.1); loads after the
  review 525, 515, 510, 490, 505. The default path on the pack: one post at each gateway, one held.
- `leak.py --asof 2026-10-13`: REVIEW, every line harmless. The statements carry 165, 490 and 510 as an entry count and
  inside amounts (4,490.50, 2,510.71), coincidences of three-digit figures. BRK-STD-03 carries six of the call's eight
  words because it is the standard the call is made under (the desks, broker posts, new posts, the review); it states no
  placement. The design-note vocabulary in BRK-STD-03, CLR-OPS-11 and the two extracts notes is the field's own (shipment,
  currency, routing, exchange, planning as in workforce planning); none connects the plan's rates to the routing
  (asserted in checks.py). The filed inputs the write-up cites (the CAD 3,300 line, the planning rates, the standard
  560) are listed under `stated_inputs`.
- `guard.py heart`: WARN (repeat.gate_g against task144; test.same_driver_older a NOTE, differentiated on the card).
  `guard.py surface`: exit 0; track A has no promoted pair after the format mix was varied (task143 had been promoted on
  format and layout alone); task446 stays promoted on the card signature (gap time, G16, Gate G forecasting), the
  same-driver match the draw answered on the card (a screen's yield backed out through two error rates against a
  nominal CAD line re-applied to invoice-currency values at the plan's rates), for the author's clone-check.

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
