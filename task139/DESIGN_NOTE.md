# task139: Copperline Vehicle Protection, whether the Fareline rideshare channel renews in 2027 at its price, at the high-use surcharge, or lapses (architecture 3)

Private, never ships. Re-rooted on 2026-10-27 for the second time. Architecture 1 (where Haverline's nurse teams work, read
per claim against per intake) was solved by both portal responses; architecture 2 (the same world, the opening call both
pilot arms received) was spent at stage 2 before any pack was cut (`## Architecture 2 record`). At the author's
instruction nothing is kept: a new world, a new task type, a new decision and a new mechanism. Shipped 2026-10-27.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task139.json`, architecture v3, registered 2026-10-27; architectures 1 and 2 in `lineage` with their fates |
| Domain / task type | actuarial-science-insurance / pricing-ratemaking-credibility (serves Forecasting): the deciding quantity is the expected claims cost of a vehicle service contract over its cover, the service-contract actuary's frequency and severity per mile of exposure by odometer, carried along each contract's mileage path to its mileage or time limit |
| Objective | Forecasting & Predictive Modeling: the lifetime loss ratio of the contracts the rideshare channel will sell in 2027, none of which exists yet, forecast from the channel's six months and the retail book's seven years |
| Shape | 04 (setting one dial: each allowed setting): the three renewal settings each carry a forecast loss ratio, with the asks' grids supplying most of the criteria (arithmetic under `## Ask sheet` at stage 2) |
| Decision | `renew_replace_lapse`, answer unit `named_option` (renew at current rates, renew with the maximum high-use surcharge, or let the channel lapse) |
| Mechanism | gap objective (the channel's cost per month of cover is correct and is not what the cover costs) then time (its six months have seen only the start of a cover that runs twenty); pattern none, generators G13 (the horizon the channel's six months cover against the roughly 21 months a cover runs) then G1 (the unit of exposure: a mile at the odometer, not a contract-month); Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `field_method` (the exposure base done right); `own:exposure-on-the-odometer-not-the-contract-clock` |
| Furniture | forum `customer_or_counterparty` (the election is Copperline's written notice to Fareline, due by 1 December 2026 for the 1 January 2027 renewal), forcing event `vote_or_meeting` (the product committee's November meeting the request is made for), organisation family `professional_services` (a service-contract obligor and administrator, its contracts backed by Tarrant Mutual Casualty's contractual liability policy), role family `product_manager` (the head of the rideshare and fleet programme), context artifact `register` (the contract register), calibration `existing_book_actuals` (the retail book's seven years of contracts, readings and claims), opening `question-first`, question form `which` |
| Spine | `odometer_readings_2019-01_to_2026-09.csv`, the administrator's odometer history: one reading on one contracted vehicle from a repair order, a maintenance-proof upload or the platform's weekly mileage feed; constructed |
| Deliverables | `fareline_channel_renewal_2027.pptx` (the committee deck: the election, the forecast and the chart it rests on), `drive_plus_channel_review_2027.xlsx` (the forecast's working and the asks) |
| People | drawn with `guard.py names --geo us --seed 1393` and `--seed 1397`: Nicholas Reed (head of the rideshare and fleet programme, the requester), Emily Willis (pricing actuary), Jason Livingston (claims director), Kirsten Weaver (administration systems), Philip Butler (Fareline's driver-benefits lead), Nicole Monroe (Tarrant Mutual's programme underwriter); none in the prompt |

**Guard.** `guard.py check` on the draft BLOCKed `ban.forum` (committee_or_panel) and `ban.org_family`
(financial_institution) against task304 in the window; the forum is honestly the executive team (the product committee
of a company this size is its executives), and the organisation is honestly a service-contract obligor and
administrator, a professional-services firm whose insurance sits with the contractual liability insurer, not a
financial institution. Registered at WARN: `three_rules.strategy_risk` (grain_or_unit), answered in `## Three rules`
(the unit is an exposure basis the analysis chooses, no field or rule names it); `people.first` on Kirsten (task457) and
Nicole (task243), older builds; `repeat.gate_g` (forecasting, beside task171 v5), the lane's own mechanism;
`repeat.question_form` (which, beside task270), the decision is a pick of one of three settings.

**Axes redrawn at stage 3 (2026-10-27).** `guard.py heart` BLOCKed `ban.pattern` (G1) and `ban.forum` (executive_team)
against task307 and `ban.forcing_event` (purchase_order_or_contract) against task308, both registered after this draw. The
election is a written notice to Fareline, so the counterparty is the honest recipient; the request is made for the
committee's November meeting; and the horizon the channel's six months cover against a cover of about 21 months is what
makes the per-mile reading necessary, so G13 leads G1. `check` then WARN only.

**Same-puzzle and same-driver tests.** Gap objective, decisive G1, `renew_replace_lapse`, Gate G `forecasting`: no
structural block in the last twelve or older.

**Abstraction test.** Stripped of nouns: a unit's events accrue with its accumulated use and climb steeply with it, and
the record's dominant population accumulates use slowly from a low start; a new population that accumulates four times
faster from a higher start reaches the steep part within months while its own short history shows only its beginning,
so the cost of its whole cover is read per unit of use at the same accumulated use from the slow population, not per
month of cover from either. Nearest drivers on `check` (0.06 and under): task170 v5 (a per-attempt failure probability
falling with each operator's own count), task161 (stock ahead of a cost step), task130 v4's lineage (a cover paying only
for events reported inside its own window): none reads a cover's cost on an exposure scale other than the cover's own
clock. `guard.py slots` on the mechanism's words (usage scale, per-mile hazard, mileage limit, odometer, telematics) and
the setting's (vehicle service contract, rideshare drivers, premium deficiency) returns no earlier screen of it.

**Data-native sentence.** Copperline's repair claims accrue with the miles a car is driven and climb with its odometer,
both in how often a covered part fails and in what the repair costs; a rideshare driver puts about 44,000 miles a year
on a car bought at 50,000 to 100,000 miles, so the 75,000 covered miles run out within two years at odometers the retail
book reaches only in its last years, and the channel's own six months have seen only the start of the cover.

**World.** Copperline Vehicle Protection (Fort Worth, Texas) has sold Copperline Drive Plus vehicle service contracts
through about 340 franchised and independent dealers in Texas and Oklahoma since 2019, administering its own claims; a
contractual liability policy from Tarrant Mutual Casualty insures its obligations. Drive Plus covers the powertrain and
major systems of a used car under ten model years old and under 100,000 miles at sale, for 60 months or 75,000 miles
from the sale date and odometer, whichever comes first, with a 100 dollar deductible a repair visit; the price is set
by vehicle class from the rate manual. In April 2026 Copperline opened a channel with Fareline, a rideshare platform,
selling Drive Plus to its drivers at the class price with a 20 per cent commercial-use loading. The agreement renews on
1 January 2027 and Copperline elects, by 1 December 2026, to renew at current rates, to renew with the rate manual's
maximum high-use surcharge of 40 per cent on the class price, or to let the channel lapse. The rate manual's channel
review standard: a channel renews at current rates if the forecast lifetime loss ratio of its next year's sales is 70
per cent or less, with the surcharge if the surcharged loss ratio is 70 per cent or less, and otherwise lapses. The
records run to 30 September 2026; the request is made in October 2026 by the head of the rideshare and fleet programme
for the committee's November meeting.

**On paper, then on the pack** (`generator/paper/` prototypes; the built world is 14,000 retail and 6,000 Fareline
contracts, retail mostly sold at 15,000 to 55,000 miles with a fifth at 60,000 to 115,000 and driven about 12,500 miles
a year, Fareline sold from April 2026 at 50,000 to 100,000 miles and driven about 44,000; repair claims per mile and
their cost flat to 70,000 miles and climbing past it; prices by vehicle class and odometer band at sale), every route
measured by `golden.routes` on the cut pack and asserted in `checks.py`:

| Route | Lifetime loss ratio, current price | Election |
|---|---|---|
| the channel's own cost per contract-month over the months its drivers take to use the cover | 16.9 | renew at current rates |
| the channel's own cost per contract-month by contract age, a linear trend carried over the cover | 55.2 | renew at current rates |
| the retail book's cost by contract age over 60 months, with the 20 per cent loading | 29.6 | renew at current rates |
| the retail book's cost by contract age on a clock sped up by the mileage ratio | 38.3 | renew at current rates |
| the book's pooled cost per mile, over the 75,000 covered miles | 21.6 | renew at current rates |
| claim frequency per mile by odometer band, at the book's average claim | 51.6 | renew at current rates |
| cost per mile by the rate manual's odometer-at-sale band (the 50,000 to 99,999 band), times 75,000 | 33.0 | renew at current rates |
| cost per mile at the odometer, every contract's miles run on at its own rate to its 60 months or 30 September (no cover ended early) | 58.2 | renew at current rates |
| the channel's own cost per contract-month over the full 60 months (the mileage limit dropped) | 48.2 | renew at current rates |
| golden: cost per mile at each odometer from the whole book, along each contract's mileage path to its limit | 75.0 | renew with the surcharge (53.6 surcharged) |

The nearest route sits 11.8 points under the 70 per cent line (the per-mile reader who keeps every cover in force); the standing family (band width, the last reading's
tail, frequency and severity apart, interpolation) runs 74.4 to 75.4 at the current price and 53.2 to 53.9 surcharged,
so the call and both nearest-5 figures hold on every member. The world's own loss ratio is 75.8.

## Three rules

- **Task type:** actuarial-science-insurance, pricing-ratemaking-credibility (serves Forecasting): the lifetime loss
  ratio of next year's rideshare sales, forecast from the exposure each contract will run before its limit.
- **Domain test:** the deciding quantity is the expected claims cost of a contract over its cover, which the service-contract
  actuary builds as frequency and severity per mile of exposure by odometer band, the exposure base the cover's wear
  generates, carried over each contract's mileage path to the earlier of its mileage and time limits; the 70 per cent
  standard reads that cost against the price.
- **Swap:** "should a hospital renew its agency-nurse contract at the current rate, with a surcharge, or not, from the
  agency's first six months" has no dual mileage-or-time limit, no covered parts that wear with use, no repair cost that
  climbs with an odometer and no earned exposure base for a cover; the quantity the call turns on, cost per mile at the
  odometer, has nothing to be, and the task stops reading the same.
- **Layer 1:** odometer readings from three sources (repair orders, maintenance-proof uploads and the platform's weekly
  feed) at different grains, with typed and rolled values; contract numbers re-keyed when the administration system
  moved in 2024, joined through a crosswalk; claims at repair-order line grain with authorised, paid and reversed lines
  and goodwill payments; cancellations refunded pro rata by days or miles with dealer chargebacks; dealer-remitted
  premium bordereaux in each dealer's layout; vehicles by VIN with make and model-year normalisation. Each is what these
  systems write; none is placed to be caught, and none carries the call.
- **Layer 2:** `field_method`, the exposure base done right: the cover's cost accrues per mile driven at each odometer,
  so it is read per mile at the odometer from the population that has driven every band and integrated along the new
  contracts' faster mileage paths to their limits.
- **Decisive step:** cost the cover per mile at the odometer rather than per month of cover, reading each odometer
  band's frequency and claim cost from the retail book and running every 2027 rideshare contract's mileage path through
  them to the earlier of its 75,000-mile and 60-month limits.
- **Not semantics:** every field, code and unit read correctly (the terms, the readings, the claim lines, the
  deductible, the loading) still leaves the easy route on the channel's own cost per contract-month: nothing in the pack
  marks the odometer as the clock, the channel's months are real, correctly priced experience, and the step is an
  exposure choice the analyst makes.
- **Not rule application:** the terms file the cover (60 months or 75,000 miles) and the standard files the 70 per cent line and the population (next year's sales, like this year's); no rule names an exposure base, a band or a curve. Enumerated family on the pack: eight constructions spread the lifetime loss ratio from 16.9 to 75.0 per cent (58 points, two elections); the standing family (cost per mile at the odometer from the whole book, 5,000-, 10,000- or 20,000-mile bands, interpolated or not, frequency and severity apart or together, with or without the last reading's tail) spreads 1.0 point (74.4 to 75.4) and files one election; what rules the per-month routes out is one cross-section nothing invites, the book's cost per mile by odometer band, flat at about 4 dollars a thousand miles to 70,000 and over twenty times that by 130,000.
- **Analyst test:** a strong analyst who reads the terms, the readings, the claims and the standard correctly takes the
  channel's own cost per contract-month over the months its drivers need to use 75,000 miles (or the retail book's cost
  by contract age with the loading, or a pooled cost per mile), forecasts a lifetime loss ratio between 17 and 58 per
  cent and renews the channel at current rates; only the cost per mile at the odometer files the golden (asserted in
  `checks.py` on the generator's clean truth).
- **Estimand:** the rate manual's channel review section (`drive_plus_rate_manual_2026.pdf`): the lifetime loss ratio of
  the contracts the channel will sell in its next year, the claims Copperline pays over each contract's cover (covered
  repairs net of the deductible, at 2026 repair costs, no trend) over the contract price, for contracts like those the
  channel sold in its first year (vehicle, odometer at sale, driving); renew at current rates at 70 per cent or less,
  with the 40 per cent surcharge if that brings it to 70 or less, otherwise lapse. Population, outcome, window, unit and
  comparison are filed; the exposure base is not.
- **No decoy:** no memo, briefing, prior review or stakeholder figure states a cost, a loss ratio or an election; the
  20 per cent loading is the price Copperline actually charged, a fact of the contracts, never argued as adequate; the
  dealer bordereaux and the cancellation file are declared distractors that rank nothing.
- **No certified replay:** no published loss ratio, prior channel review or certified figure ships, so the exposure
  base cannot be recovered by matching certified numbers; the retail book's experience is raw records every route uses.
- **Lesson:** a cover's cost accrues on the scale its wear runs on, and a population that runs that scale four times
  faster from further along it is costed per unit of use at the same accumulated use, from whoever has driven that far,
  never per month of cover from its own short start. No build on file reads a cover's cost on an exposure scale other
  than the cover's own clock (task130 v4's lineage reads a reporting window, task170 v5 an operator's own attempt count).

## Default path

1. Read the terms (60 months or 75,000 miles from sale, 100 dollar deductible) and the channel review standard (renew at
   70 per cent or less; with the 40 per cent surcharge if that reaches 70; otherwise lapse).
2. Build the rideshare contracts from the register (sold since April 2026) and their claims from the repair-order lines
   (paid net of reversals, the deductible taken off).
3. The channel's cost per contract-month: its claims cost over its contract-months in force to 30 September 2026.
4. The months of cover a 2027 contract runs: 75,000 miles over the channel's average driving (from the platform feed),
   about 20 months, under the 60-month limit.
5. A 2027 contract's lifetime cost is step 3 times step 4; over the average 2026 price, the lifetime loss ratio.
6. Apply the standard.

Ends on: renew the channel at current rates (a lifetime loss ratio of about 17 per cent on the pack).
Golden: renew with the maximum high-use surcharge (about 75 per cent at current rates and 55 per cent surcharged).

## Stump sentence

A competent solver costs a 2027 rideshare contract by its months of cover, the channel's own claims cost per
contract-month run over the months a rideshare driver takes to use the 75,000 covered miles (or the retail book's cost by
contract age with the loading, the book's pooled cost per mile, or its cost per mile at the odometer with every cover kept
in force to its term), forecasts a lifetime loss ratio between 17 and 58 per
cent and files renew the channel at current rates (Ends on); the step that lands it there is costing the cover by its
months, when repair claims accrue per mile and both their frequency and their cost climb with the odometer past 70,000
miles, and a rideshare cover runs from 50,000 to 100,000 miles at sale through 75,000 miles more in under two years, past
anything the channel's six months have reached: read per mile at each odometer from the retail book and stopped at each
contract's limit, the cover costs about 75 per cent of the price, so the channel renews only with the maximum high-use
surcharge, at about 55 per cent.

## Readability screen

Measured by the generator on the cut pack (`checks.py` restates every figure on each build): the lifetime loss ratio
at the current price, the golden against the default path's routes.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the channel's months | the channel's own claims cost per contract-month to 30 September, run over the months a driver takes to use 75,000 miles (16.9), or over 60 months (48.2) | the terms' 60 months or 75,000 miles; the channel's own six months are the only Fareline experience | readable |
| L1 the channel's age trend | the channel's cost per contract-month by month of contract age, a linear trend carried over each cover (55.2) | the same six months, read as a development pattern | readable |
| L2 the retail clock | the retail book's cost per contract-month by contract age over 60 months, with the 20 per cent loading (29.6), or on a clock sped up by the mileage ratio (38.3) | the agreement's commercial-use loading; the retail book's seven years | readable |
| L3 per mile, pooled | the book's claims cost over its miles under cover, times 75,000 (21.6), or frequency per mile by odometer band at the book's average claim (51.6) | the terms' 75,000 miles; the readings' odometers | readable |
| L3b per mile by the price table's band | the retail book's cost per mile for contracts sold in the rate manual's 50,000 to 99,999 band (every Fareline car's band), over their miles, times 75,000 (33.0) | rate manual 2: the price is set by the odometer at sale in those bands | readable |
| L4 per mile at the odometer, every cover in force to term | the golden's cost per mile at each odometer, but each contract's miles under cover run on at its own rate to its 60 months or 30 September, the cars sold and the covers cancelled kept on cover (58.2) | the terms 4 and 6: a cancelled contract's CarLink reporter is removed and sends a closing reading on the day the contract ends; the cancellation requests for 2025 and 2026 | readable |
| G golden (decisive) | the claims cost per mile in each odometer band from the whole book, each 2026 Fareline contract run from its odometer at sale at its own mileage to the earlier of 75,000 miles and 60 months (75.0) | nothing names the odometer as the cover's clock: the rate manual files the estimand and no exposure base, and the one cross-section that rules the other rungs out (the book's cost per 1,000 miles by odometer band, about 4 dollars to 70,000 miles and over 20 times that by 130,000) is invited by no document | silent |

Every route below the golden files renew at current rates, at least 11.8 points under the 70 per cent line (L4, the
per-mile reader who keeps every cover in force to term, is the nearest); every
standing member files the surcharge, the current-price figure 74.4 to 75.4.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the odometer band | 10,000-mile bands | 5,000- or 20,000-mile bands | same call (asserted; 74.6 to 75.2, 75 and 55 at the nearest 5) | same call |
| SF2 | the last reading | miles under cover to each contract's last reading in cover | on to the cover's end or 30 September at the contract's own rate | same call (asserted) | same call |
| SF3 | the cost per mile's form | cost per mile in the band | frequency per mile times the band's own average claim, or interpolated between band midpoints | same call (asserted) | same call |
| SF4 | the contracts standing for 2027 | the 2026 Fareline contracts with a feed reading after sale | all 2026 contracts, the rest at the channel's mean mileage | same call (asserted) | the rate manual 5 (contracts like those sold) |
| SF5 | the book the cost is read from | the whole book | the retail contracts only | same call (asserted) | same call |
| SF6 | the loss ratio's form | total claims cost over total price (the mean cost over the mean price) | the mean of each contract's own ratio | same call (asserted; 75.0 and 75.9) | same call |
| SF7 | a contract's annual mileage | its last feed reading since sale | a straight line fitted to its feed | same call (asserted) | same call |
| SF8 | goodwill payments | not claims cost | counted | same call (asserted) | the rate manual 4 |
| SF9 | reversed lines | netted | the positive lines only | same call (asserted) | the rate manual 4 |
| SF10 | the deductible line | netted | not netted | same call (asserted) | the rate manual 4 |
| SF11 | claims and readings under pre-2024 numbers | joined through the crosswalk | dropped | same call (asserted) | the crosswalk |
| SF12 | the 60 months | calendar months from the sale | 1,826 days | not a fork: under 2 per cent of the contracts run near the time limit (asserted) | the terms 2 |

The live rows are asserted as cross products in `checks.py`: SF1 by SF2 by SF3 (18 cells) and SF4 by SF5 by SF6 by SF7
by SF1 (48 cells), every cell filing the surcharge with 75 and 55 at the nearest 5 per cent.

## Ladder

Measured by the generator on the cut pack; `checks.py` asserts every row on each build.

| Rung | Lifetime loss ratio at the current price, per cent | Call | Call kept |
|---|---|---|---|
| L0 the channel's months over the months of cover | 16.9 | renew at current rates | no |
| L0 the channel's months over 60 months | 48.2 | renew at current rates | no |
| L1 the channel's age trend | 55.2 | renew at current rates | no |
| L2 the retail clock with the loading | 29.6 | renew at current rates | no |
| L2 the retail clock sped up by the mileage ratio | 38.3 | renew at current rates | no |
| L3 the pooled cost per mile | 21.6 | renew at current rates | no |
| L3 frequency by band at the book's average claim | 51.6 | renew at current rates | no |
| L3b per mile by the rate manual's odometer-at-sale band (retail contracts sold at 50,000 to 99,999 miles, over their own miles, times 75,000) | 33.0 | renew at current rates | no |
| L1b the channel's own trend in every common form (linear weighted 55.2, unweighted 62.0; quadratic 215 to 240; exponential 287 to 548) | 55.2 to 548 | renew at current rates or lapse, never the surcharge | no |
| L4 per mile at the odometer, every cover in force to term | 58.2 | renew at current rates | no |
| G golden: cost per mile at the odometer along each contract's path | 75.0 (53.6 surcharged) | renew with the maximum high-use surcharge | yes |

The clean-truth run (`checks.py`, the world's exact claims and odometers without the pack's mess) files renew at
current rates on every route and the surcharge on the golden; the world's own loss ratio is 75.8.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the contracts the channel will sell in 2027, like the 2026 sales (vehicle, odometer at sale, driving) | filed (rate manual 5); SF4 |
| 2 | Unit of account | the lifetime loss ratio, per cent of the contract price | filed (rate manual 5) |
| 3 | Attribution window | each contract's whole cover | filed (terms 2, rate manual 5) |
| 4 | As-of dating | records to 30 September 2026 | filed (the prompt, the file names) |
| 5 | Version basis | the 2026 rate manual and its prices | filed (rate manual 1, 2) |
| 6 | Denominator | the contract price at current rates, and the surcharged price | filed (rate manual 3, 5) |
| 7 | Weighting | each contract once | linear (SF6 asserted) |
| 8 | Window length | 60 months or 75,000 miles, whichever first | filed (terms 2); SF12 |
| 9 | Boundary inclusivity | 70 per cent or less | filed (rate manual 5) |
| 10 | Rounding path | the forecast compared unrounded, reported to the nearest 5 per cent | filed (the prompt) |
| 11 | Tie-break | current rates before the surcharge before a lapse | filed (rate manual 5) |
| 12 | Maturity and censoring | covers still running at 30 September counted to their last reading | the decisive step's exposure (SF2 asserted) |
| 13 | Order of operations | claims cost, miles by band, cost per mile, each contract's path, average, ratio | linear |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a repeated maintenance upload is one reading | linear (a repeated reading adds no miles, asserted) |
| 16 | Identity normalisation | pre-2024 contract numbers through the crosswalk; the Fareline feed by VIN | filed (the crosswalk, the agreement 3); SF11 |
| 17 | Netting against gross | net of the deductible and reversed lines, goodwill out | filed (rate manual 4); SF8 to SF10 |
| 18 | Dimensional units | miles, dollars | not applicable |
| 19 | Code and status semantics | line types PARTS, LABOR, DEDUCTIBLE, GOODWILL | filed (rate manual 4) |
| 20 | Integerisation | none on the call | not applicable |
| 21 | Clause scope | the Fareline channel's next agreement year | filed (rate manual 5, the agreement 1 and 4) |
| 22 | Forward window contents | the odometers a 2027 cover runs through, 50,000 to 175,000 miles | the decisive step (the cover is costed per mile at each odometer from the book that has driven it) |

## Literal reader

Executing the prompt and every filed sentence word for word: rate manual 5 fixes the forecast quantity (the claims
cost Copperline will pay over each 2027 contract's cover, at current repair costs and with no trend, over the contract
price), the population (contracts like those the channel sold in its current year: the same vehicles, odometers at
sale and driving) and the rule (renew at current rates at 70 per cent or less, otherwise with the maximum surcharge if
that brings it to 70, otherwise lapse); rate manual 4 fixes claims cost (net of the deductible and reversed lines,
goodwill out); the terms fix the cover (60 months or 75,000 miles from the sale date and odometer). How the cover's
claims cost is forecast is left to the analysis, and the records select it: the claims accrue per mile and climb with
the odometer (cost per 1,000 miles about 4 dollars to 70,000 miles and over 20 times that by 130,000, with the retail
book's odometers at every band), so a forecast on any other clock reads the cover's first months as its whole. Every
licensed construction on the odometer (any band width, the tail or not, frequency and severity apart, interpolation,
either book, either population, either ratio form) files the surcharge at 75 and 55 to the nearest 5 per cent.

## Oracles

No file ties only under the golden or only on a wrong read. No shipped file states a loss ratio, a cost per mile, a
prior channel review or an election, and none ranks the three settings. The agreement summary states the 20 per cent
loading as the price charged, never as adequate. Tarrant Mutual's policy summary and the repair facility directory ship
as distractors.

## Ask sheet

The call's declared population is the Fareline contracts sold in 2026 and the whole book's claims and odometer
readings. The two asks read files the call never opens (the cancellation requests, the dealer bordereaux, the bank's
returns report, the dealer directory) and run over retail contracts only; the Fareline contracts carry no lienholder
and no bordereau, so no ask device row sits in the call's population, and the call is unchanged with every ask device
removed (asserted: `golden.py` reads none of the ask files).

- **Ask A, cancellations in 2026: retail contracts cancelled, refunds owed and of which to lienholders, by quarter
  (9 figures).** H18 home: the channel review's cancellation experience beside the forecast, the refunds the book owes
  this year. Primary device (silent, an identity judgment): a lienholder's payoff request names a VIN and the
  lienholder, never a contract, and when a car is sold its next owner often buys a contract of their own on the same
  VIN through a dealer within weeks, so the payoff request often arrives after the next owner's contract is written.
  Joined on its VIN as of the date received (the hygiene battery's own as-of join), the request lands on the next
  owner's contract and cancels it, or double-cancels nothing and drops the old one; the golden takes the contract on
  that VIN that shows the requesting lienholder. Twin: VINs sold once, requests by contract number, cars traded with
  the dealer's request first. Hazards: the first request received decides (terms 5), the free look within 30 days with
  no claim made, the odometer from the request or the latest record, the refund to the lienholder. Stops on the cut
  pack: the as-of join (208, 294,574, 146,162; 213, 261,454, 157,824; 206, 316,318, 160,135); the requests with a
  contract number only (174, 202,349; 186, 204,722; 177, 242,869); every request a cancellation (281, 303, 278); the
  golden 191, 225,091, 120,674; 202, 222,805, 136,837; 193, 264,816, 145,907.
- **Ask B, 2025 dealer premium: received to 30 September 2026 and outstanding, by quarter of sale (8 figures).** H18
  home: the channel review's dealer remittance control beside the channel's own price. Primary device (silent, a
  reconstruction): each dealer remits a month's contracts on one ACH payment under one reference; the bank's returns
  report names the originator by its account name in capitals, its own trace number, the payment's total and its
  settlement date, never the bordereau reference, and about half of the returned payments are re-sent on a later
  month's bordereau with the same lines. The golden rebuilds each dealer-month payment from its lines, matches each
  return on the dealer (name to code through the directory), the settlement month and the payment's total, and keeps
  the re-sent payment as received. Matched on the dealer and the amount alone, the re-sent payment is taken off too;
  with a contract's second line dropped as a duplicate first (the battery's own key), the re-sent payment is lost and
  the returned one taken off. Twin: dealer-months never returned, payments in the same amount in other months.
  Hazards: three layouts (Brazos in cents with its own deal number; the independents by VIN and day-first sale date,
  a VIN resold carrying two contracts), the remittance lag of one or two months. Stops: duplicates first (1,224,227
  and 57,273 in 2025Q1), dealer and amount only (1,223,077 and 58,423), returns ignored (outstanding negative), VIN
  alone (1,245,718 and 35,782), cents read as dollars; the golden 1,252,537 and 28,963; 1,322,803 and 4,174;
  1,341,549 and 25,274; 1,276,743 and 41,758.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | the first request received per contract (terms 5), a lienholder's payoff request joined on its VIN as of the date received, the refund formula executed | misses |
| B | the three layouts read, cents to dollars, the independents on VIN and sale date, a contract remitted twice kept once, then the returned payments taken off | misses |

Measured by: `generator/ceiling.py` on the cut pack.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Cracker |
|---|---|---|---|---|
| A cancellations and refunds by quarter | 9 | 0 | 0 | misses |
| B dealer premium received and outstanding by quarter | 8 | 0 | 0 | misses |

Over the 17 ask figures the cracker keeps none (it scores 45.0 with the call), the mirror none (12.0 off the call).

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The construction layer is the deck's chart and the workbook's cost per mile by band, which the cracker has with the
call and the mirror misses with it. Ask B's returned-payment organ differs from architecture 1's (bank returns there
carried the payment's own reference on an indemnity payment; here the bank's keys never meet the bordereau and the
payment has to be rebuilt from its lines and told from its re-sent copy by the settlement month).

## Pre-ship check

- The three rules re-read against the built pack: the decisive step is still the exposure base (rate manual 5 files the estimand and no clock; nothing names the odometer as the cover's clock), the mess is Layer 1 only (the 2024 crosswalk, three reading sources, line-grain claims with reversals and goodwill, three bordereau layouts), and the asks' devices sit in files the call never opens.
- Call: renew with the maximum high-use surcharge, 75.0 per cent at the current price and 53.6 surcharged; the standing family 74.4 to 75.4 (75 and 55 at the nearest 5 on every member, 48 plus 18 cross-product cells); every route on the default path and below files renew at current rates, the nearest the per-mile reader who keeps every cover in force (58.2), the rate manual's odometer-at-sale band at 33.0, and the channel's own trend files renew or lapse in every common form, never the surcharge; the clean-truth analyst test files renew on every route; the world's own loss ratio 75.8.
- Asks: cracker 0 of 17, mirror 0 of 17, pair ceiling 28.5 (`ceiling.py`); every ask golden equals the world truth (`checks.py`).
- Inputs: 13 files in three formats (9 CSV, 4 PDF, 1 XLSX), the odometer readings at 612,712 rows, two distractors named in `metadata.json`, no dictionary or notes file; golden metadata clean.
- Gates: checks 254, verify 27 of 27, two byte-identical builds (3019a830, goldens included), figures_check 50 of 50, precut 53 checks 0 FAIL, voice-check PASS (930 characters), leak.py REVIEW with every line ruled, two leak readers clean with Q6 analytical, judge pass 1 DETERMINISTIC and APPROVE (its two optional pins applied), guard heart WARN after the stage 3 axis redraw.

## Architecture 2 record (spent 2026-10-27)

Haverline Workers' Compensation Trust, the same seventeen Early Return Nursing teams as architecture 1, re-rooted on the
opening call both pilot arms had received before the file was randomised (the default path read the usual-handling arm
as a unit with no team; the golden read the call's saving from the intakes the triage screen never drew). Registered
2026-10-26 and spent the next day at stage 2 before any pack was cut: the decisive step rested on one sentence of the
pilot protocol, which a careful reader meets first, inside the world the portal had already solved.

## Architecture 1 record (spent 2026-10-26)

Haverline Casualty Company, a stock carrier writing Missouri employers; drawn 2026-10-12, shipped 2026-10-15 (commit
1384f0e9, `target.zip` sha256 da3c19bf42dff8ef; checks.py 343 assertions, verify.py, byte-identical rebuilds,
figures_check 67, precut 49 with 0 FAIL, voice-check PASS, leak.py REVIEW answered, guard heart PASS, surface exit 0).
Stage 4: the leak reader found no leak (Q6 analytical); the judge returned NOT_DETERMINISTIC on supplementary 3 only,
FIX_NOW applied (the intake filed as a WHAT in the dictionary, Ask 1's silent device redrawn as EDI resends merged into
their claims), and the re-judge DETERMINISTIC and APPROVE, stump power moderate (`determinism_check_report.md`,
`determinism_check_report_pass2.md`).

**The design.** The pilot's nurses kept a fifth to a quarter of the strain intakes from ever paying indemnity, and the
review verified 100 indemnity claims a unit and group, so ERN's verified claims were the costlier remainder. The default
path compared the two groups' mean verified claim and valued a team per place-day of an indemnity claim; the decisive
step read the pilot per assigned intake (each group's share paying indemnity times its own verified severity) over an
ERN intake's place-days. The ladder: per verified claim 0 3 0 3 2 3 3 3 at 2,048,524 (booked 2,000,000); the per-claim
family 2.0 to 2.2 million; per assigned intake without the place-day 3,793,208, with an indemnity claim's place-days
3,398,667, without the fill check 4,200,799; the golden 3 3 2 0 3 3 0 3 at 4,105,562 (booked 4,100,000), RW-SS held to
the two teams its 944 intakes keep in use (teams listed HC-SS, HC-OT, RW-SS, RW-OT, MF-SS, MF-OT, CN-SS, CN-OT).

**Portal result, 2026-10-26.** Both responses placed three teams each in HC-SS, MF-SS, MF-OT, CN-OT and HC-OT, two in
RW-SS and none in RW-OT or CN-SS, and booked the 4.1 million dollar credit, with the workbook and the note: the golden
exactly.

**Why it was reachable, and it is not a near miss.** Reading a randomised pilot per assigned intake is the textbook
reading, analyse as randomised, which this note quoted as the client's pin, so readability test 3 fired on the decisive
rung where the screen had recorded it silent; the default path it overturned conditions on a status the treatment
moves, which a strong analyst refuses by reflex. And the whole ladder sat inside the register's two arms: once a reader
read the arms per intake, nothing in the pack was left to find.

**The constraint it leaves.** Inside the two arms the per-intake contrast is unbiased and the design forces it, so any
further step there is a stratification of it (the triage tier, the office), the opponent's first group-by, or a
transport of its average onto the intakes the 2027 teams reach, which is task177 v2's driver and needs that population
filed. Architecture 2 finds what the two arms share that the counterfactual lacks: the opening call.

## Stump-vocabulary sweep, ruled

- `drive_plus_contract_terms.pdf` (odometer, contract, months, reading, repair, covered): the cover's dual limit, the
  refund formula and the CarLink records clause; none names an exposure base or a cost per mile. Harmless.
- `drive_plus_rate_manual_2026.pdf` (odometer, contract, claims, repair, loading, agreement): the price table by
  odometer at sale and the channel review's estimand; it files what is forecast and never how. Harmless.
- `fareline_channel_agreement_summary.pdf` (odometer, contract, mileage, loading, agreement): the weekly mileage feed
  and the loading as the price charged. Harmless.

## Tried and rejected

- The seed's light-duty conditioned yield (the saving exists only at employers with a record of temporary-partial
  payments, carried onto segments whose mix of such employers differs from the pilot's): a conditioned yield under a
  composition shift, pattern E and `composition_mix`, both spent on task137 inside the ban window; dropped at the draw.
- The saving per place-day alone (Little's law on the pilot's files, the teams valued per place-day rather than per
  claim): a strong solver computes a capacity-bound team's yearly throughput by segment by reflex once the charter
  states twenty places; kept as a rung, never the decisive step.
- An Erlang loss model on the triage stream (intakes lost when every place is taken): the effect is under a sixth of a
  team's value at matched load, it never moves a whole team, and a replay or a monthly fluid model files a different
  figure from the formula; rejected on determinism.
- A transient count of 2027 intakes from empty teams on 4 January (the first twenty in each team): the answer turns on
  the whole duration distribution and a reading of the AY window, `time_semantics` is spent on task138; closed instead by
  the pick memo's run-rate convention.
- A twelve-month pilot drawing one in three intakes with 40 to 50 verified claims a stratum (2026-10-15): a segment's
  realised saving per team-year had a standard deviation of 120,000 to 300,000 dollars across draws against values of
  120,000 to 330,000, so the segment ranking was noise; the pilot runs 24 months and the review verifies 100 a stratum.
- The review as a census of every pilot indemnity claim (2026-10-15): it would cut the noise further, but the join of the
  review to the register would then show 451 usual-handling claims against 338 ERN claims in healthcare strains, the
  frequency effect on the surface of the file the default path reads; the review samples a fixed 100 a stratum.
- A check run sent twice with its cancellation only in a treasury register (Ask 2's first device, 2026-10-15): the
  register would have been a single-purpose file announcing the device, and a duplicate run whose checks are voided after
  the pull leaves "paid" indeterminate; replaced by the line grain and the bank's returns.
- The draft charter's "units with the most intakes would be considered first" (stage 3, 2026-10-15): a staff draft
  stating a placement basis reads as a decoy draft (R3c); the draft now leaves the basis to be settled with Pricing.
- Ask 1's two devices left silent (stage 4, 2026-10-15): the judge's literal reader took `time_off_at_report` as the
  dictionary then defined it and counted both listings of a parallel-run claim, so the golden held only under the
  author's reading (NOT_DETERMINISTIC, FIX_NOW); a silent label switch and an unkeyed double listing cannot be both
  silent and forced, so both are filed and the ask's silence is gone.
- Ask 1 regenerated to the flag as filed (stage 4, 2026-10-15): it would count later indemnity conversions and the
  parallel run's second listings as intakes against charter 4.1, mark the careful count wrong and leave the ask with no
  device; the organisation's definition is filed instead.
- The parallel-run note without its fields (stage 4, 2026-10-15): matched on office, segment, class, injury and report
  dates without `disability_began`, one converted claim listed once pairs a new-number claim; the note names all six.
- Memo paragraph 2's restated comparison (stage 4, 2026-10-15): "what those intakes would pay with their adjusters
  alone, less what they pay with a team" restated the credit as a subtraction over the intakes, which the judge read as
  the estimand stated nearly literally; the credit is stated once and the counterfactual left to charter 4.2.
- A second form for the review's control digit (stage 4 realism, 2026-10-15): the digit sits on the call's join of the
  review to the register, so a second form would be a main-path mess item; the references and remarks vary instead.
- The FIX_NOW pass's Ask 1 (stage 4, 2026-10-15): both devices filed for determinism and nothing silent left, the cracker
  landing all eight figures and a pair of 58.2; redrawn with the merge file.
- A state FROI filing log carrying the cancels of claims filed in error (Ask 1 redraw, 2026-10-15): a second source of
  reported lost-time claims in the state's voice, its originals counting later conversions as reports and a cancel for a
  wrong-carrier report not plainly outside "intakes"; the claims system's own merge file instead.
- A closed-outcome field on the extract (Ask 1 redraw, 2026-10-15): a value naming the device rows in the habitual file
  is a marker, and its denied or withdrawn outcomes in the call's window would move the fill count when mishandled.
- Legacy claims parked as unassigned (G9) and converted to GN-AL (Ask 1 redraw, 2026-10-15): the injury class cannot be
  recovered from the class code, so the true segment would be a guess.
- 2026-10-26, architecture 1's decisive step (the pilot read per assigned intake, each group's own indemnity-claim rate
  times its own verified severity, instead of per verified indemnity claim), after both portal responses landed the
  placement and the 4.1 million credit. Spent, not repairable: analysing a randomised pilot as randomised is the
  domain's own reflex, so readability test 3 fires on the decisive rung, and the whole ladder sat inside the register's
  two arms, so a reader who reads the arms per intake has nothing left to find. Every further step inside those arms is
  a stratification of the contrast or a transport of its average, both spent or filed. The re-root is recorded in
  `## Portal result and the stage 2 diagnosis`.
- 2026-10-26, at the architecture 2 draw: the triage tier as the decisive step (2027 teams take intakes highest
  predicted lost time first, so a unit's teams reach the top of its tier distribution, where the file saves least in the
  strain units and most in the other-injury units). Measured on paper (200,000 intakes a unit, five tiers): the golden
  4.28 million against the pilot average's placement at 4.16 million, both booking 4.3 million, so the credit did not
  separate; the stratification by tier is the opponent's first group-by, the teams' population has to be filed, and the
  driver is task177 v2's (a randomised average carried to the part of the population the deployment reaches).
- 2026-10-26, at the draw: employer spillover (a nurse's suitable-duty work at an employer also helping its
  usual-handling claimants), the randomised contrast understating the at-scale effect: the interference family of
  task131 v1 and task249, a parent unit's shared resource; dropped unmeasured.
- 2026-10-26, at the draw: the file's effect falling with the team's load (the pilot ran below the full load 2027
  teams will carry), a dose-response read from the pilot's daily open-file counts: a fitted curve with a free form,
  and a randomised average carried to one covariate value again; dropped.
- 2026-10-26, at the draw: the pilot's claims developed to ultimate arm by arm (a file closing claims sooner, so one
  set of book factors overstates ERN's ultimates): the chain-ladder variants a reader would defend fork the graded
  figures (stumping 1.6a's task194 death), and the review already projects the open claims; dropped.
- 2026-10-26, at the draw: segment savings blended by credibility before placing: shrinkage is the opponent's reflex,
  and the credibility standard would have to be filed, which is the method; dropped.
- 2026-10-27, architecture 2 spent at stage 2 before any pack was cut (the opening call both pilot arms received): the decisive
  step rests on one sentence of the pilot protocol, which a careful reader meets first, and the world is the one the portal
  already solved; re-rooted at the author's instruction for a fully fresh architecture.
- 2026-10-27, architecture 3 draw screens, each dead before a card: a larger die's yield read through the wafer-level
  spread of defect density (task143's driver, a joint chance under a shared group effect, in new nouns); regression
  dilution corrected with replicate readings (task166 and task178: the probe's reflex); delayed entry for a taken-over
  book (task133); hearing-loss claims filed after separation (task166's lineage, the probe sliced claimants by status);
  non-synchronous covariances (task135); a first claims-made year's cost from the report-lag pattern (task130 v4's
  lineage, and the same-calendar-year claims give it in one filter); long-term disability reserves without the coming
  Social Security offsets (the field's standard assumption, so a reflex); second deaths after a bereavement (last year's
  claims rate lands it); a miners' trust's amount-weighted release (task171's screen: last year's release lands it).
- 2026-10-27, the rideshare channel opened in January 2025 or 2026: with nine or more months of its own experience, the
  channel's cost per contract-month by contract age, its trend carried forward, landed inside the golden's band; opened
  in April 2026, its six months stay on the flat part of the wear curve and the trend files renew.
- 2026-10-27, a retail book sold across 20,000 to 100,000 miles: its cost by contract age with the loading reached 72 to
  81 per cent, inside the band; the retail book is now mostly sold at 15,000 to 55,000 miles, with a fifth at 60,000 to
  115,000, which drives every odometer band the rideshare cover reaches.
- 2026-10-27, cost per mile rising as a power of the odometer from zero: the channel's own six months saw the rise and
  its trend landed; claims are flat to 70,000 miles and climb past it, as major components start to fail.
- 2026-10-27, stage 3: ask B's re-sent payments matched to the bank's returns on the dealer and the amount alone: the
  re-sent bordereau carries the same lines and total, so it was taken off as well; the golden matches on the settlement
  month too, and the dealer-and-amount match is kept as a rival (`match_any_month`) that misses every figure.
- 2026-10-27, stage 3: ask B kept as the returned-payment reconstruction although architecture 1's ask carried bank
  returns: a replacement keyed on the independents' deal dates (VIN and nearest sale date) was screened and refused,
  because noticing the unmatched lines and choosing the nearest sale date are one act (supplemental-stumping 1.0); the
  organ differs from architecture 1's (there the return carried the payment's own reference).
- 2026-10-27, stage 3: the full refund within 30 days read on a claim "paid": the claims file's paid dates trail the
  repair order by up to three weeks, so "paid" and "made" could part on a contract cancelled in its first month; terms 5
  now say no claim made by then (a repair order dated on or before the cancellation date).
- 2026-10-27, stage 3: miles under cover for a car whose readings stop before its 60 months left unexplained: a reader
  could run every cover on to its term at its own rate (58.2, renew at current rates); the terms' records clause now
  states the CarLink reporter's closing reading and its removal on cancellation, a fact of the source, and the
  in-force reading is a lower rung (L4), not a fork.
- 2026-10-27, stage 3: the crosswalk unused, claims dropped while their exposure is kept (55.0, renew at current rates):
  37.8 per cent of the claims carry a pre-2024 number, an unmatched join the hygiene battery flags, so it is a broken
  join rather than a reading; the R2 assertion leaves the unmapped contracts out whole (78.2, the surcharge).
- 2026-10-27, after ship: the Fareline count moved off the round 6,000 a leak reader flagged. Measured on the clean world
  at 6,013, 6,029, 6,037, 6,043, 6,051, 6,061 and 6,079 contracts, the channel's own linear age trend runs 60.8 to 72.8
  (72.8 at 6,043 files the surcharge by luck), against 55.2 at 6,000; the shipped world keeps 6,000, the clearest of the
  draws, and `checks.py` now asserts that no trend form (linear, quadratic or exponential, weighted or not) files the
  golden on it.
- 2026-10-27, after ship: ask B's returned-payment organ screened for a replacement, so that no ask device repeats architecture 1's. The
  replacements screened (the independents' deal date a day or two before the sale date, joined on VIN and the nearest
  sale; dealer pay-plan instalments read as duplicates; a dealer group's catch-up remittance after an acquisition) were
  each found and fixed in one act, or left "received" without a payment record; all weaker than the dealer-month
  reconstruction, which stays.
