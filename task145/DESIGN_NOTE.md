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
| Spine | `highvalue_check_2025Q4.csv` to `highvalue_check_2026Q3.csv`, the clearance system's quarterly high-value check extracts (every inbound international shipment released with a value for duty of CAD 2,500 or more, in two layouts), about 250,000 rows over the twelve months to September 2026; constructed |
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
