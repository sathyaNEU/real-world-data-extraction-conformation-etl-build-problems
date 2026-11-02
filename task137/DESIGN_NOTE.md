# task137 design note

Architecture 5, drawn and registered 2026-11-02 (Forecasting lane, wave 2 slot). Architecture 1 (Kaimai Building
Society's maturity campaign, banking) was landed on the portal; architecture 2 (Calderbrook Care's adverse-drug-event
admissions) lost every decisive step to probes; architecture 3 (Calderwick Police's custody hub) was spent at stage 4;
architecture 4 (Hollinsfield and Brantmoor's phlebotomy hub) kept a sound call but was spent on its ask layer, and its
10-26 version stays on the portal as delivered. All four identities are in the card's lineage and their dead ends in the
last section; nothing of any of them is kept. This draw is Tarnfield Wholesale's 2027 motor claims fund: the collision
claims its 7.5-tonne delivery fleet will make in 2027 once a new schedule sends every store route out between 03:45 and
05:15 all year.

## Draw

1. **Card.** `.claude/skills/fingerprint/cards/task137.json`, architecture v5, registered 2026-11-02T20:53:26Z with
   architectures 1 to 4 in its lineage (architecture 4 marked `architecture_spent`, its shell in `lineage_shells`).
   `guard.py check` on the draft and on the registered card: PASS, with two NOTEs answered on the card
   (`test.same_puzzle_older` against task204, a room's unsteady ventilation balance; `driver.near` 0.16 against
   task121 v3, clock-hour matching of complaints to a facility). Axes redrawn at the draw because task458 v3 and task197
   v2 were filed minutes earlier and moved the window: forum `committee_or_panel` to `board_of_directors` (the board
   approves the self-insured claims fund), role `finance_controller` to `procurement_lead` (the manager buys the motor
   cover and runs the fund), org `other` to `logistics_or_3pl` (a delivered wholesaler whose business is distribution on
   its own fleet), strategy `forecast_method_backtest` to `composition_mix` (honest: the rate is stable within light
   condition and hour band, and the schedule moves the light mix), gap `time` to `objective` then `time` with G7 first
   (`test.same_puzzle` and `test.same_driver` blocked on time with G14 or G7 against task154's and task183's lineages).
2. **Pairing.** Actuarial Science & Insurance, task type `claims-frequency-severity` (serves Forecasting and
   Descriptive), objective Forecasting & Predictive Modeling: the call is a count of claims in a year not yet begun.
   The first draw of this slot in the client domain; no architecture of the lineage used it.
3. **Shape.** 02, a forecast across periods: the 2027 claims and its two seasons' (stage 4 moved the split from quarters),
   with the asks' figures beside
   them (the criteria arithmetic is in `## Ladder` and `## Ask sheet`).
4. **Strategy and mechanism.** `composition_mix`, generators G7 (when the driving physically happens against sunrise and
   sunset decides its rate), G6 (the forward exposure's light mix moves under a clock-hour mix the record already ran),
   G14 (the collision rate conditioned on the light each kilometre is driven in). Gate G `forecasting`.
5. **Data-native sentence.** The fleet ran its small-hours departures only on the May-to-August summer schedule, so
   most early-morning kilometres in the record were driven after sunrise and the record's driving in darkness happened on
   winter evenings' returns, December mornings and the summer schedule's earliest starts; the 2027 schedule runs the small-hours
   departures all year.
6. **Abstraction sentence.** "A rate per unit of exposure is stationary only once each unit is placed in a physical
   condition the clock tracks only by season, and a schedule that moves the exposure into hours the record ran only
   while the condition was absent leaves every clock-hour rate low." No approved build carries it: task501's meter drift
   and task139's accumulated use both swap one exposure clock for another (litres for months, use for months of cover);
   here the exposure measure is unchanged (kilometres) and what decides is the light each kilometre is driven in, a
   property of the date, the clock time and the depot's position that no clock-hour rate or month term recovers.
   task163 (shipped, pending) moves picks beside near-weight neighbours through a check-weigh's blind band, a filter and
   a layout; nothing here is filtered and nothing is rearranged in space.
7. **Mechanisms read** (`guard.py mechanisms --objective forecasting`, 92 builds): the exposure-clock family (task46
   cumulative service exposure, task139 accumulated use, task501 litres not months) spends the swap of one usage measure
   for another; task176 v2 an external age clock; task132 renewal restarts; task163 a filter's blind band moved by a
   layout; task121 v3 (dead) clock-hour matching to attribute events; none prices exposure by solar light.
8. **Slots read, both screens, before the first harness.** Setting nouns (darkness, sunrise, daylight, twilight, clock
   change): task182's architecture 8 screen rejected an hour-of-week profile in darkness-relative time as exact
   arithmetic on a shipped sunset table that settles the estimand's own clock; here the sunrise and sunset table ships as
   the driver handbook's lighting appendix (darkness must come from shipped records), the estimand (claims in 2027 by
   incident date) has its clock filed in the fund terms, and the light condition is the exposure model's HOW, which no
   filed sentence links to collisions; task138, task248,
   task119, task125 and task472 carry daylight saving only as Layer 1. Mechanism and world nouns (fleet, telematics,
   collision, motor insurer): task174's telematics onboarding score and task268's development by notifying route
   (spent as one join away) are other mechanisms; task165 and task153 use telematics as a spine for other quantities.
9. **Neighbouring slots' `resume` lines read** (every forecasting slot in flight): task130, task143, task145, task146,
   task148, task161, task170, task173, task176 and task178; task178's note that a reserving-development-triangles cell
   was searched and found nothing that holds is why this draw sits in claims-frequency-severity, not reserving; the
   recurring finding in task143, task148, task161 and task170 (ask layers spent once the cracker was made honest) is why
   the ask records were named before registration and are screened as code before any data is cut.
10. **The ask records, named at the draw.** (A) The receipts other insurers paid towards the fleet's own-damage repairs
    (the wholesaler self-insures own damage): the domain mechanic is subrogated recovery of the outlay at the other
    side's share of liability, contributory negligence splitting a collision 50:50 or 75:25, remitted under the paying
    insurer's own reference on many lines. (B) The bodyshop network's invoice feed: the domain mechanic is a feed
    resend under fresh invoice numbers beside genuine same-day second invoices on one repair (a supplementary after
    strip-down), the fleet register's forward sensors (a camera, or a camera and a radar) fixing how many
    calibrations one repair can carry; the engineer's authorisations were drafted and dropped as an oracle. Both are screened against the
    careful-solver cracker as code before the pack is cut (`## Ask sheet`).
11. **Sources.** Synthetic world on real geography and real rules: sunrise and sunset by the NOAA solar position
    equations at each depot's latitude and longitude; British Summer Time from the last Sunday of March to the last
    Sunday of October; England's bank holidays 2023 to 2027; UK motor claims practice (own damage, third-party property
    and injury, subrogated recovery at a liability split). People drawn with `guard.py names --geo GB --seed 137`.

## Three rules

- **Task type:** claims-frequency-severity (Actuarial Science & Insurance), which serves Forecasting: the expected number
  of claims a portfolio makes over a future exposure period, here the delivery trucks' collision claims in 2027.
- **Domain test:** the deciding quantity is the claim frequency per kilometre of exposure by rating factor, worked as the
  field works frequency: claims counted against the kilometres that produced them, rated on the factors the record
  supports, and carried onto the 2027 schedule's planned kilometres.
- **Swap:** "a hospital's patient falls in 2027 per occupied bed-day on a new night-shift rota": falls per bed-day would
  carry staffing, not sunrise, and the light each unit of exposure is spent in, the depot's latitude and the summer-time
  rule stop meaning anything; the call is a motor fleet's exposure priced by road light.
- **Layer 1:** two Gridtrak export templates (miles then kilometres, dd/mm/yyyy times then ISO stamps, registrations
  without then with the space, an overlap week, all in UTC), the insurer's listing in UK clock time under a report header
  with company cars, second notifications closed as duplicates and withdrawn notifications, October 2026 claims beyond
  the telematics' 30 September end, a register keyed by depot names the platform spells as groups, the bank's truncated
  payer narratives; each is what the producing system writes and none moves the call (SF1 to SF7).
- **Layer 2:** composition of exposure (the 2027 schedule moves the light mix of the kilometres under clock hours the
  record already drove); the choice that flips the call is whether a kilometre is rated on the clock or on the light.
- **Decisive step:** rating each kilometre on whether it was driven before sunrise or after sunset at its depot (Appendix
  C, by date row, with the summer-time rule), alongside the clock band, because the record drove the small hours only on
  the May to August schedule, mostly in daylight, and the 2027 schedule drives them all winter in the dark.
- **Not semantics:** every field read correctly (UTC converted, miles converted, cars and duplicates out, the right depot
  for each truck) still leaves the clock-band frequency model on 281.9, filed 300, because the small hours' low rate is a
  correctly measured daylight rate.
- **Not rule application:** no filed rule names a rating factor, a light condition or a model; the fund terms fix only
  what is counted. Enumerated family (overall, clock band, clock hour, month and band, depot and band, month by band
  cells, and the six light members) spans 281.0 to 360.6; the standing family after the data rule out the clock-only
  members (darkness LR 70.3 on one degree of freedom over the clock band, the back-test below) spans 334.0 to 368.1 over
  27 members (three constructions of light by nine models, SF20), all
  inside 350; the ruling-out is quiet, a likelihood ratio and a back-test nobody is told to run.
- **Analyst test:** a strong analyst who converts every clock, cleans the listing and fits collisions per kilometre by
  clock band (or hour, month or depot) files 300 (281.9 unrounded), the small hours looking the fleet's safest.
- **Estimand:** the fund terms (claims_fund_terms_2027.pdf sections 2 to 4): collisions of the delivery trucks on the
  register, route or spare, notified to Ravensby, duplicates and withdrawn notifications out, cars out, in the fund year
  and quarter of the incident date in UK clock time, for the 2027 route schedule and its delivery calendar.
- **No decoy:** nothing is planted: no memo, forecast, rate, factor, prior figure or stakeholder view of 2027 claims ships;
  the handbook's lighting appendix is the drivers' lighting rule and the schedule is the board's plan.
- **No certified replay:** no certified or published figure ties only under the golden; the method is not recovered by
  reproducing anything, it is chosen by the record's own fit and back-test.
- **Lesson:** a frequency rated on the clock is stationary only while the clock tracks the condition that drives the
  rate; when a plan moves exposure into hours the record drove only in another light, rate the exposure on the condition,
  and test the model where the record already observed that condition. No build on file prices exposure by solar light.

## Survivor anatomy

- **Actor:** the light each kilometre is driven in has no column in any file: it is a relation between a run's UTC
  ignition times, the date's summer-time rule, the truck's depot from the register and the handbook's sunrise and sunset
  row.
- **Link:** kilometres reach light only through a drivers' lighting appendix, joined on depot and seven-day date row
  after the clock is converted; no key, column or sentence pairs kilometres or claims with it.
- **Reflex:** the field's frequency model rated on time of day (band or hour, with month or depot) sits at rung 1 and
  files 300 here.
- **Back-test:** the textbook check passes the easy route: the clock-band rate fitted to September 2025 predicts the next
  twelve months at 281.0 against 278 observed (p 0.89), because the record's schedule never changed.
- **Second use:** every file the step reads is in the pack for its own reason: the handbook for drivers (checks, hours,
  lights, the collision procedure), the telematics and listing for any frequency model, the register for depots and the
  asks' sensors, the schedule for the 2027 plan.
- **Shock:** nothing in the pack reads as an anomaly: the small hours carry the record's lowest observed rate, monthly
  claims move from 15 to 36 with no trend, and the schedule change is the plan the prompt names.
- **Pins:** the fund terms file the population, the fund year and quarter by incident date in UK clock time, the 2027
  schedule and calendar, VAT and the recoveries' quarter; no filed sentence names the clock band, the light, a rating
  factor or a model, and deleting any of them leaves the light step exactly as hard.

## Default path

1. Read both Gridtrak day-summary exports to 30 September 2026 (miles to kilometres, UTC to UK clock time), each truck's
   depot from the register.
2. Took the listing's truck claims, cars, duplicates and withdrawn notifications out, to the same date: 840 claims.
3. Spread each run's kilometres over its clock hours and fitted collisions per kilometre by clock band (a Poisson
   frequency on kilometres; hour, month or depot terms give the same answer).
4. Priced every route and delivery day of the 2027 schedule at those rates: 281.9 claims.

Ends on: 300 claims (281.9 unrounded; April to September 150, the other six months 150)

Golden: 350 claims (346.9 unrounded; April to September 150, the other six months 200)

## Stump sentence

A competent analyst prices the 2027 schedule's kilometres at the record's collision rate per kilometre by clock band and
files 300 claims (281.9), the small hours looking the fleet's safest, where the golden is 350 (346.9); the step that lands
it there is reading collision risk off the clock instead of off the light: the small hours' low rate is a daylight rate
from the May to August schedule, and from October to March every 2027 route starts in the dark, up to five hours
before sunrise in midwinter, where the record's own dark kilometres, on winter evenings, December mornings and the
summer schedule's earliest starts, carry 2.59 times the daylight rate in the same clock band.

Data-native sentence: the fleet ran its small-hours departures only on the May to August summer schedule, so the record's
early kilometres were driven mostly after sunrise and its dark kilometres came from winter returns, December mornings and
the summer schedule's earliest starts; the 2027 schedule runs the small-hours departures all year.

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 overall collisions per kilometre (281.0) | no | no | yes: the frequency per unit of exposure | no | no | yes | readable |
| R1 the default path, by clock band or clock hour (281.9, 283.4) | no | yes: ignition times give the hour | yes: time of day is the fleet rating factor | yes: the time holdout passes it (281.0 against 278) | no | yes | readable |
| R1b month and clock band, month by band cells (283.5, 283.1) | no | yes | yes: seasonality | no | no | yes | readable |
| R1c depot and clock band (281.8) | no | yes: the register's depot | yes: territory | no | no | yes | readable |
| R2 (decisive) clock band and light from Appendix C (346.9; the light family 334.0 to 368.1) | no: no sentence links light, sunrise or darkness to collisions or rates | no: no column holds light; it is a relation between UTC times, the summer-time rule, the depot and a drivers' lighting table | no: the reflex rates on the clock, and the record's early hours look safest | no: no rate, factor or forecast ships | no: nothing in the files is wrong | no: a per-run split at hour edges, sunrise and sunset, then the fit and the 2027 pricing | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py` under its id.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | collision claims (population) | the trucks' claims | company cars counted | 350 | fund terms 2; same call |
| SF2 | a claim | one per collision | duplicates and withdrawn notifications counted | 350 | fund terms 2; same call |
| SF3 | the record's window | claims to 30 September with the kilometres | claims to 31 October | 350 | same call |
| SF4 | the two exports | the overlap week once | counted twice | 350 | same call |
| SF5 | 2027 delivery days | the calendar's Yes days, bank holidays included | bank holidays dropped | 350 (339.1) | the 2027 calendar; same call |
| SF6 | the fleet | route trucks and depot spares | spares out | 350 | fund terms 2 |
| SF7 | telematics clock | UTC, converted by the summer-time rule | read as UK clock time (285.8) | 300 | both export headers label UTC |
| SF8 | the 2027 seasons | the incident date in UK clock time | the notification date | 350; seasons unchanged | fund terms 3; same call |
| SF9 | the incident time | UK clock time | UTC | 350 | the listing header "Incident time (UK)" |
| SF10 | darkness | before sunrise or after sunset at the depot, Appendix C | civil twilight or another table | not computable from the pack | the handbook's lighting rule and Appendix C |
| SF11 | "the new schedule starts in January" | every 2027 delivery day from 2 January | 1 January counted | 350 | the calendar: 1 January no deliveries |
| SF12 | rounding | year and seasons to 50 | seasons forced to sum | 350 = 150 + 200 | the prompt; they sum |
| SF13 | recoveries' quarter | the collision's quarter | the receipt's quarter | ask figures move | fund terms 5 |
| SF14 | other insurers | third parties' insurers | the salvage agent's credits counted | ask figures move | fund terms 5 ("another party's insurer") |
| SF15 | money | net of VAT | gross | ask figures move | fund terms 5 |
| SF16 | a depot's collisions | the truck's depot on the register | the bodyshop site or cost centre | ask figures move | the register; Washington repairs two depots |
| SF17 | repair cost | repairs and a total loss's inspection and storage | repairs only | ask figures move | fund terms 5 |
| SF18 | the asks' periods | the collision's incident date | the invoice or posting date | ask figures move | fund terms 3 and 5 |
| SF19 | the asks' population | the trucks | cars | same figures | no car is repaired at Brantwick or recovered into the account |
| SF20 | the 2027 split (the unit) | April to September and the other six months, to 50 | calendar quarters to 25 | a member crosses: month, hour and light puts Q4 at 87.4; morning and evening multipliers and band by light cells on the last two years put it at 114.0 and 114.1 | the prompt's unit; every member of the 27 holds (table below) |

SF20, measured on the cut pack (`checks.py` prints the full table): three constructions of light (the exact split at
sunrise and sunset; each clock hour labelled by its midpoint for kilometres and claims alike; the last two years only) by
nine models (light only; band and light; hour and light; month, band and light; depot, band and light; band and light
with separate morning and evening multipliers; light only with them; month, hour and light; band by light cells).

| Construction | Year | April to September | Other six months | Q4 (the quarter that crossed) |
|---|---|---|---|---|
| exact split | 337.6 to 363.5 | 150.1 to 154.1 | 187.5 to 209.4 | 87.7 to 109.0 |
| hour-midpoint light, claims and kilometres alike | 337.3 to 347.8 | 149.5 to 152.7 | 186.7 to 196.5 | 87.4 to 102.0 |
| last two years | 334.0 to 368.1 | 146.2 to 153.1 | 187.8 to 217.9 | 88.9 to 114.1 |
| filed bins | 350 (325 to 375) | 150 (125 to 175) | 200 (175 to 225) | 100 (87.5 to 112.5) |

Nearest edges over the 27: the year 6.9, April to September 20.9, the other six months 7.1. Two constructions sit outside
the family and are recorded, not filed: the saturated hour by light cells (a dark hour with no claims gives a zero rate;
323.8 on the last two years, the judge's 323, rejected by the judge) and kilometres labelled by the hour's midpoint while
claims keep their exact times (numerator and denominator counted by different rules: up to 381.5 with separate morning
and evening multipliers or band by light cells).

## Ladder

| Rung | Route | 2027 claims | Filed | April to September, other six months |
|---|---|---|---|---|
| R0 | overall rate per kilometre | 281.0 | 300 | 150, 150 |
| R1 (default path) | clock band | 281.9 | 300 | 150, 150 (142.3, 139.6) |
| R1 | clock hour | 283.4 | 300 | 150, 150 |
| R1b | month and clock band; month by band cells | 283.5; 283.1 | 300 | 150, 150 |
| R1c | depot and clock band | 281.8 | 300 | 150, 150 |
| R2 (golden) | clock band and light | 346.9 | 350 | 150, 200 (150.7, 196.3) |
| R2 family | the 27 of SF20 | 334.0 to 368.1 | 350 | 150, 200; nearest edges 20.9 and 7.1 |

Shape 02 arithmetic: the year and its two seasons (3), the six recovery quarters (6), the twelve depot half-years (12),
the chart's named parts (record months, 2027 months, axis and legend: about 4) and the two files: 27.

Clean truth (the generator's world, exact times): clock band 284.8, golden 353.6; every clock route off 350 and every
light member on it (checks R2). Gate F: cheap routes reaching 350 on the pack, 0 of 6.

## Closure table

Each row's assertion is in `checks.py`.

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the delivery trucks' collisions notified to Ravensby, route trucks and spares, members not yet observed included (2027) | fund terms 2; SF1, SF2, SF6 |
| 2 | Unit of account | one claim per collision | fund terms 2; SF2 |
| 3 | Attribution window | the fund year and quarter of the incident date | fund terms 3; SF8 |
| 4 | As-of dating | listing as at 31 October 2026, telematics to 30 September 2026, schedule approved 14 October 2026 | file headers; SF3 |
| 5 | Version basis | one listing, one register, one schedule | asserted |
| 6 | Denominator | kilometres driven | design; the Poisson frequency on kilometres (HOW, forced by the fit) |
| 7 | Weighting | every kilometre counts once | design |
| 8 | Window length | the whole record, October 2023 to September 2026 | C1: no year term (LR p 0.80), time holdout |
| 9 | Boundary inclusivity | a kilometre at a sunrise or sunset edge split at the minute | C1: pieces split exactly |
| 10 | Rounding path | unrounded expectation, rounded once per figure | the prompt; SF12 |
| 11 | Tie-break | none arises | margins asserted over the 27-member family (year 6.9, seasons 20.9 and 7.1) |
| 12 | Maturity and censoring | late notifications to 31 October cover the record to 30 September | SF3 |
| 13 | Order of operations | clock conversion, split, fit, carry | design |
| 14 | Row order | none matters | sums |
| 15 | Duplicate resolution | the listing's duplicates out; the overlap week once | SF2, SF4 |
| 16 | Identity normalisation | registrations with and without the space; depot names and groups | the register; asserted by the verifier's own reader |
| 17 | Netting against gross | claims counted gross of recoveries | fund terms 1 and 2 |
| 18 | Dimensional units | miles converted to kilometres | the export header "Distance (mi)" |
| 19 | Code and status semantics | "Closed - duplicate of", "Withdrawn", "Car" | the listing's own values; fund terms 2; never the stump |
| 20 | Integerisation | none: expectations, rounded to 50 and 25 | the prompt |
| 21 | Clause scope | the terms cover the trucks and the 2027 fund year | fund terms 1 and 2 |
| 22 | Forward window contents | every route of the 2027 schedule on every delivery day of its calendar | fund terms 4; SF5, SF11 |

## Literal reader

The prompt and the fund terms executed word for word file 350 under every reading the pack leaves: the population,
window, unit and clock are filed (SF1 to SF12), the 2027 exposure is the schedule's routes on the calendar's delivery
days, and the method is left open and forced by the data, which reject every clock-only model (darkness LR 70.3 over the
clock band, 67.6 over month and band) and accept the light model's back-test where the record drove 04:00 to 07:00 in
the dark (48 claims against 37.6 expected, p 0.12; the clock rates expect 23.2 and 32.3). The golden's assumptions are
each tested in `checks.py` (A7): no month effect beyond darkness (p 0.54), no trend (p 0.80), no hour effect within bands
(p 0.55), one darkness multiplier morning and evening (p 0.23), a depot term at p 0.03 that leaves every figure in its
bin, Poisson dispersion 0.91, planned kilometres equal to the routes' recorded mean (0.995 to 1.004). The asks' literal
readings are closed by the terms (SF13 to SF19); their devices are found only by internal inconsistency (`## Ask sheet`).

## Oracles

No shipped artifact states, ranks or forecasts 2027 claims, a collision rate, a rating factor or a model output; the
handbook's appendix is a lighting table and the terms file no number of claims (asserted G3). No control total ties only
under an ask's golden: the engineer's authorisations, which summed exactly to the genuine invoices, were dropped for that
reason; the register's forward sensors are a vehicle attribute, and the receipts' amounts tie to a repair cost times a
liability share only after the reconstruction the ask needs.

## Ask sheet

Two ask blocks, on records the call never reads (the AP ledger, the bodyshop's job list and the recovery account), each
with its own primary from a different family. With the three ask-only files deleted the call files the same 346.9 (D3).

**Ask A, recoveries by the collision's quarter (6 figures), D7 the true key elsewhere.** 89 of the 171 receipts from other
insurers quote only the payer's own reference; each is the other side's share of one collision's net repair cost, paid
in full for a non-fault collision and at a quarter, a third, a half, two thirds or three quarters for a split one, and
exactly one claim of that payer matches each amount to the penny (D1). Over-cleaning half: matching on the full repair
cost alone places only the non-fault orphans. Shared hazard: the repair cost itself rides on ask B's device.

| Reading | A1 figures kept of 6 | Why it fails |
|---|---|---|
| orphans left out (no claim number) | 0 | the receipt reads as unattributable; a quarter to a half of each quarter's money goes missing |
| orphans by the receipt's own quarter | 0 | the payment lag is 38 to 190 days |
| payer and amount equal to the repair cost, else left out or the receipt's quarter | 0 | split collisions are paid a share |
| shares inferred from amounts on an exact-duplicate repair cost | 2 | the over-cleaned cost moves every two-sensor repair by 185 |
| golden: our number, else the one claim matching payer, share and net cost | 6 | |

**Ask B, Brantwick repair cost by depot and half-year (12 figures), D1 replay.** In three spells the bodyshop's feed sent each
invoice twice and AP posted the copy a week later under a fresh document number (210 copies, every line of the spell,
accident repairs included, which a job carries once); beside them sit genuine identical ADAS calibration lines, one per
sensor on the 148 repairs of trucks the register shows with camera and radar, 79 of them sent days after the first because
the radar certificate comes back late, many into the next weekly import. Over-cleaning half: an exact-duplicate pass deletes every second
calibration; a one-import-earlier twin rule deletes the late ones. A camera-only truck never carries two calibrations
outside the spells (D2), so the reading is forced by the register.

| Reading | B1 figures kept of 12 | Why it fails |
|---|---|---|
| every AP line | 0 | the copies add 10,000 to 47,900 a cell |
| exact duplicates dropped | 0 | every second calibration goes: 185 to 1,480 a cell |
| a line with a twin one import earlier dropped | 0 | late radar calibrations go: 185 to 740 a cell |
| twins paired one for one across imports | 2 | outside the spells the late radar calibration is consumed as a copy (two cells hold none) |
| golden: each invoice once, two calibrations on a camera-and-radar truck | 12 | |

Hazards: the payers' bank names truncated (both asks' joins), the bodyshop site serving two depots (B), receipts for 2024
collisions inside 2025 (A), the salvage agent's credits (A), gross beside net (both).

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A recoveries by collision quarter (6) | the hygiene battery's anti-join, orphans placed by payer and amount equal to the exact-deduplicated repair cost, else by receipt date or left out | every quarter off by 2,100 to 40,000 | miss |
| B repair cost by depot and half-year (12) | exact duplicates and re-sent lines dropped, summed by the truck's depot and incident date | every cell low by 185 to 1,480 | miss |
| the chart | the cracker's own forecast months beside the record | the record and its months | outside |

Measured by: generator/ceiling.py on the cut pack (the honest cracker lands the call and runs the battery; the mirror
keeps every line and leaves orphans out; routes beyond the battery printed; the full includer reproduces figures.json).

Mirror leakage: 0.0 per cent of the ask weight (the mirror keeps no ask figure).

Pair ceiling: 28.5 (cracker on the call 45.0 with no ask figure, mirror off it 12.0); two careful responses on the call
45.0 each; a cracker on the call with the best route beyond the battery (an import-pairing resend rule and shares
inferred from amounts, 6 of 18) 63.3.

## Layer 1 inventory

Every item is what its producing system writes; none moves the call (SF1 to SF7, asserted).
- Gridtrak: the export template changed in March 2025 (miles to kilometres, date formats, registration spacing, group
  names), one reporting week in both exports, every time in UTC.
- Ravensby listing: a four-line report header, company cars on the same policy, second notifications closed as
  duplicates (a few bodyshop jobs quote the second number), withdrawn notifications, claims to 31 October beyond the
  telematics' 30 September.
- Fleet register: depot names that differ from the platform's groups and the schedule's codes; write-offs and their
  replacements.
- AP ledger and jobs: dd/mm/yyyy dates, site cost centres, net, VAT and gross; recovery account: truncated payer names,
  references run together, salvage credits and month-end sweeps.

## Stage 3 gates

Re-run on the final cut after the stage 4 watch item, 2026-11-02 (target.zip md5 90f3dba97187bcf182764a196ae51bbb, seed
13; the pack did not move, the prompt, write-up and goldens did):
- `generator/make.py`, twice: checks 0 failures (the M, R2, L1 to L5, A7, SF1 to SF20, D0 to D3 and G1 to G8 blocks);
  byte-identical rebuild; verify 0 failures; ceiling as in `## Ask sheet`.
- `precut.py task137 --quiet`: PASS task137: 61 checks, 0 FAIL, 0 WARN.
- `voice-check.py task137`: PASS.
- `figures_check.py task137 --quiet`: PASS task137: 42 figures in blocks 1 to 4, 0 absent from generator/figures.json.
- `leak.py task137 --asof 2026-11-02 --quiet`: REVIEW, no LEAK; each line ruled:
  - sweep 3, 43,200 in the old Gridtrak export: a run's 18:43 ignition-off time beside its 200.2 miles; no figure.
  - sweep 3, the fund terms carry the call's words: the terms define the estimand (delivery trucks, collision claims,
    the fund year and its quarters) and state no number of claims (G3).
  - sweep 4, the handbook's record, records and sunrise: "record it on the Gridtrak tablet", the claims handler
    "records the date and time", and the lighting rule with Appendix C, the shipped darkness carrier; no sentence
    relates light to collisions, risk or rates (G3).
  - sweep 9, dates after 2 November 2026 in the bank-holiday feed and the 2027 calendar: both are forward-looking
    records the organisation holds before the year starts (the gov.uk feed publishes 2027; the board's 2027 plan).
- `guard.py surface task137`: exit 0; promoted pairs task139 (the same domain and objective two apart: its exposure
  clock is accumulated use, here the exposure is unchanged and the rating factor is the light), task135 (G7 two back),
  task204 (gap, pattern and decision type: the NOTE already differentiated on the card, a room's unsteady ventilation
  balance), task147, task179 and task154 (surface vocabulary in the corpus top 1 per cent); the people NOTE "Carlisle
  Darlington" is two place names in the handbook's table header.
- `guard.py heart task137`: HEART VERDICT: PASS (NOTEs against task204 and task121, differentiated on the card).
- `freeze.py snapshot task137`: 10 main-call figures (7 figures.json keys), 2 ask files, the call sentence frozen.
- Input gates: 12 files, 4 formats (csv, json, pdf, xlsx), gridtrak_day_summary_2025-03_2026-09.csv at 119,448 rows,
  two distractors (store_delivery_windows_2027.xlsx, bank-holidays-england-and-wales.json), metadata.json with source,
  date and licence for every file.
- House fixes: PDFs read by pdfplumber, pdftotext and pypdf in strict mode; container metadata clean in target and
  golden (scrub audit); goldens through golden-realism (finding titles, source line, a terms footnote, a notes sheet,
  the chart on the validated two-slot palette), the note one page.

## Pre-ship check

The 10/10 rules read again against the cut after stage 4 (the leak reader clean, its question 6 an analytical choice;
the judge DETERMINISTIC, APPROVE, Gate G method_or_model_selection, Gate H PASS).
- Domain: the deciding quantity is the fleet's collision frequency per kilometre by the light each kilometre is driven
  in, carried onto the 2027 schedule's exposure, which is how claims-frequency work prices a portfolio's next year; the
  swap to a hospital's falls per bed-day breaks it (sunrise, latitude and the summer-time rule stop meaning anything).
- Two layers: the mess (two Gridtrak templates in UTC, miles then kilometres, the listing's cars, duplicates and
  withdrawn notifications, the overlap week, the October claims past the telematics) is what the systems write and stays
  neutral (SF1 to SF7); the analysis decides: every clock route files 300, every light-aware member of the 27 files 350
  (M2 to M4, SF20).
- Rule 3: nothing is planted, no field reading decides the call, and no filed sentence names light, a rating factor or a
  model (G3); the decisive step is analytical, a rating factor the record's own fit and back-test choose (A7, L4).
- The watch item: the judge's quarters were thin, and the measured family put three members across a quarter's edge
  (SF20), so the 2027 split moved to the unit the family holds, April to September and the other six months to the
  nearest 50 (nearest edges 20.9 and 7.1 over 27 members), with the repair-cost ask regrained to depot by half-year to
  keep the rubric at 27; no method was filed and the world was not re-centred. The prompt changed, so the reader and the
  judge run once more.
- Stage 4, final (2026-11-02): the leak re-read on the season-split prompt is clean (Q1 to Q4 none, Q6 an analytical
  choice, the handbook's sunrise appendix read as a driving rule, not a risk statement); the re-judge on the unchanged
  pack (target.zip 90f3dba9) is DETERMINISTIC, APPROVE (determinism_check_report_pass8.md): every daylight-aware model
  files 350, split 150 and 200, the clock routes 300; all 12 depot half-year costs and six quarterly recoveries
  reproduce; Gate G analytical_non_defect, Gate H pass. Its watch items stand recorded: the ledger-duplicate and ADAS
  pair convention (derivable, penny-certified), the seven repair jobs on duplicate-closed notifications (counted, the
  ask says collisions), one half-up penny match (Ingleby, Q3 2025), stump power moderate.
- Every gate re-run on the final cut 90f3dba9 (2026-11-02): precut 61 checks 0 FAIL; voice-check PASS; figures_check 42
  figures 0 absent; leak.py REVIEW, no LEAK (every line ruled in the note); guard surface exit 0; guard heart PASS.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
- Forum `line_manager_or_team` (the head of deposits signing the block order alone): task136 moved its forum to the same
  key after this card was registered, and `ban.forum` blocked; the Deposits Committee now approves the block.
- Write-up figures rounded coarser than they read: the list's retention-offer share to the nearest 5 per cent (60,
  against 62.1) and its non-reaching dials to the nearest 500 (67,500, against 67,354.8); the judge read both as wrong.
  Now whole per cent and nearest 100 (62, 67,400), with freeze.py allowing the two keys
  (`components.retention_share_pct`, `steps.non_reaching_dials`); the Final Recommendation and Critical Components move
  only by that 60 to 62.
- The judge's wording for the Ask A clause (a deposit counts if any of its maturity proceeds were in a society term
  deposit, its principal the amount in term deposit then): "maturity proceeds" is the transfer extract's narrative and
  points at Ask A's device, and "the amount on term deposit then" reads as the new deposit's whole balance, new money
  included (the whole-principal stop). Filed as: counting a deposit if any of its principal was, and only the part that
  was.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because its decisive step, the share of
  conversations going to the retention offer conditioned on each deposit's drop from its locked rate to the card, was
  the strong model's reflex and the field's textbook model: a logistic of the retention outcome on term with a separate
  locked-rate slope per term booked about 5,496 hours, inside the golden's 5,500 bin, without reading any card; the
  share by locked rate sat one bin under; Ask B's migration batches file announced the overlap and an account-level
  dedup against it cracked the ask; Ask A's clause (a deposit counted if any of its principal was kept, and only that
  part) signalled the partial-move device; and the swap test passed only narrowly (insurance renewals priced off a rate
  card read almost the same). Round 2 keeps the world, the call and the asks' populations and moves the decisive step
  to the class of the money, a reason only deposit repricing behaviour has.
- A market-gap stump for round 2 (each deposit's locked rate against a published market rate for its term and opening
  month, the deposits far above the market leaving): the market table made the premium a visible column and the step
  one join (readability tests 2 and 6); the class is rebuilt from each list's own cohorts instead, with no table naming
  it.
- Other round-2 candidates for the decisive step, dropped at the draw: the term structure of the card alone (still the
  drop, read term by term, the reflex the audit measured); the best card across terms as the rate a deposit is compared
  with (a second reading of the rate it reinvests at, a fork and never a stump); money above the Depositor Compensation
  Scheme's per-depositor cover leaving at maturity (a filed limit executed on a visible principal column, rule
  application read off the schema).
- Round 2's first prototype kept round 1's January to March 2027 card (four years 3.15 per cent, so the special's drop
  was 2.50 points): past special money dominated the 2.50 band, so the share by drop alone booked near the golden, and
  the locked-rate-by-term logit carried the special's deposits at about 0.8. The 2027 card was turned up (four years
  4.00, a drop of 1.65), a band in which past conversations are 89 per cent member money.
- The card's gap reordered to population first: `guard.py check` blocked on `test.same_driver` (population, E,
  forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
  order for a premium that lapses at first maturity.
- January's share of the 2023 four-year special's sales at 0.242: January's hours sat near a rounding edge and the drop
  and term logistic landed January's bin (1,250); the sales by month are now 0.184, 0.408 and 0.408, January's golden
  1,206.9 and that rival's January 1,000.
- Ask B at six figures (each month's maturing principal on and off the list): with Ask B the most obvious device, the
  cracker's pair ceiling rose to 41; cut to four figures (the three months and the quarter's part not on the list),
  39.0.
- Ask A's device as a posting date (D8, maturity proceeds posted on the next business day): the hygiene battery's
  unmatched-join count found it at once; moved to the payments system's settlement account with the matured deposit
  named only in the narrative (D7).
- The write-up's past share for member money (15 per cent, 14.57 unrounded) and all past conversations' share in the
  special's band (35 per cent, 34.55): both within 0.07 of a rounding edge; dropped from figures.json, the write-up, the
  note and the workbook, the band given by class instead (88 and 28 per cent, 0.24 and 0.18 from an edge).
- The note's chart title "Seven in ten hours are conversations, most of them retention offers": under the round-2
  shares January's conversations go to the offer 45 per cent of the time and the retention offer's minutes are under
  half the talk in January and March; retitled to the measured two-thirds (0.665 to 0.693, asserted).
- Band shares as a Critical Component (88 against 28 per cent at drops of 1.50 to 1.75): a corridor member (special
  money pooled, a logistic within each class) never computes them; the component keeps the class's 87 per cent and the
  bands stay in the steps.
- Portal round 1 (2026-10-25): response 1 landed the call exactly, 5,250 agent-hours (1,250, 2,000 and 2,000 by maturity month), so reading each reached holder's retention-offer share by the class of the money (the 2023 four-year special's block at 5.65 per cent against its cohort's 5.15) is a reflex for the portal's model, as the drop was for the audit's; with both the drop and the class spent, the world's deposit behaviour layer has no decisive step left, and the one structural step it still holds (a reached holder's conversation settling the holder's later deposits on the list, so hours follow holders, not deposits) reads the same with a clinic's reminder calls, a backdrop by the swap test.
- Re-root to architecture 2 (2026-10-25): architecture 1 spent on portal round 1 (above); the slot moves to a new
  cell, healthcare-delivery-health-economics / utilization-access-demand-forecasting, with nothing of the seed's world kept.
- Architecture 2 draw, coastal high-water flood days in 2027 from the window's astronomical tide plus skew surge
  (climate-weather-extremes): dead on the slots screen, it is task178's architecture 1, spent at Gate F when a scored
  reader conditioned on the 2027 tide table; the prototype (`tide.py`) had shown 2027's tide-only exceedances 15 to 25
  per cent under 2026's at a semidiurnal port.
- Architecture 2 draw, candidates killed on the lane's dead lists before code: bike-share pairs and pupil yield by
  estate age (task170's ninth cell), event prediction and illness-death states (task171, task174), the disposition
  effect in listings and notification habituation (task177's rate-by-state screens), vacancy chains (too close to
  task166's live junior-on-senior driver), OR-list overruns and clinic slot cascades (task170's replay law).
- Architecture 2 draw, a liability book's back-loaded accident year (`res1.py`, two seeds): the accident-year chain
  ladder missed by -36 to -42 per cent but Bornhuetter-Ferguson and frequency-severity on earned exposure landed within
  5 to 14 per cent: the textbook fallback for an immature year is the golden, so dead.
- Architecture 2 draw, warranty claims on a months-in-service clock a new retail channel delays (`war1.py`, two seeds):
  the shipment-clock default missed by only -2 to -5 per cent; dead on lever.

- Interacting pairs as the decisive step (the registered card's, 2026-10-25, restarted thread): a strong enumerator's own
  pick, so on the enumerable chain. On the generator's world a logistic with the canonical pairs wins out of sample
  (log-likelihood -1,629.7 against -1,741.2 per medicine and -1,641.8 for every two-way pair, 2023 to mid-2025 fitted,
  the next nine months scored), and replayed on the regimens the reviews left it files 191 admissions against the
  golden's 343; the pairs stay as a rung any solver climbs, and the decisive step moves to the stopped medicines'
  restarts.
- The dead thread's restart world with the programme counting as each resident's annual review: the 2027 annual reviews
  then all fall in October to December 2027, and leaving them out filed 9 per cent high, a fork between two readings of
  the procedure; the programme is now additional to the annual review, which continues in its usual month, so an
  implicit stop hazard over every month and explicit 2027 reviews agree within 1 per cent (345.4 against 343.0).
- Start hazards scaled by frailty: the pooled restart clock then sat 3 to 6 per cent under the truth, so a frailty-
  stratified estimator would have crossed a bin; the start and restart hazards are frailty-free and the record's clock
  recovers the truth within 1 per cent.
- Pair partners stopped only where the pair is held, with small main effects for NSAIDs and benzodiazepines: the per-
  medicine model with a pooled start hazard landed within 1 per cent of the golden (two errors of opposite sign); the
  criteria now stop NSAIDs and benzodiazepines in every regular user, their own effects carry most of their harm, and
  that route sits at 329 (4 per cent under).

- The restart clock as the decisive step (the stopped medicines restarted on the record's clock from each earlier
  stop), probed 2026-10-26 on a six-file pack (golden 343.0, nearest 25 = 350; frozen 191 to 220, pooled Markov 295):
  two isolated Opus call-only probes landed it, p137a at 350 (355.4) and p137b at 350 (361.9), each with a monthly
  Poisson rate on the month's medicines and their combinations, frailty and care type, validated on October to December
  2026, every medicine switched month by month with recent stoppers restarting faster and about three in ten stopped at
  an annual review, a leaving hazard and a microsimulation, back-tested on the 2024 and 2025 year-start cohorts within 2
  to 5 per cent. Any transition the record shows as a rate gets measured; dead. Their realism catches carried forward:
  the programme stopped 93 per cent of the NSAIDs and benzodiazepines it reviewed against 31 per cent at annual reviews
  under criteria the schedule called the same; no annual reviews after 26 October 2026; 24 admissions overlapping the
  person's previous stay; discharge dates after the pull.
- The blanket-programme restart curve (the programme's stops restarting like Ferncliffe's 2025 blanket programme rather
  than like selective annual-review stops), prototyped 2026-10-26 before a probe: the pooled clock landed 9 to 17 per cent
  under it and the per-medicine model with the pooled clock within one bin (two errors of opposite sign); set aside
  unprobed for the coordinator's evidence from five probe deaths: every dead step put the decisive attribute on the frame's
  own units, where a thorough modeller joins it and measures it, and the survivors (task305, task306) carry a body the
  frame does not hold; re-registered on the step-down guests.

- The step-down guests as the decisive step (re-registered 2026-10-26, d1f3551d), probed on a six-file pack (probe3):
  Opus probe p137c took the step, filing 500 (502.4) as 407.4 for the long-term residents plus 95.0 for the step-down
  guests (37 drug-event readmissions over 23,576 occupied bed-days, 180 beds at 92.1 per cent occupancy), because Annex A
  split each home's beds into long-term and step-down. No honest rebuild hides them: the golden is determinate only if a
  file states the 2027 step-down beds (an annex, a bed plan, a purchase order or a registration variation), and the
  probe cross-matched every file by NHS number (it found the 81 guests who became long-term residents, none on the
  register); if the trusts' returns carry the guests, they are an unmatched block, and if they do not, the guests' rate
  has no determinate source (an analogue choice is a fork). Dead in this world.
- The households other councils placed in Hartmoor's hotels and hostels as the decisive step (architecture 3's first
  candidate, a borough council's 2027 Part 7 assessments; probe pack probe5, golden 1,400 against the frame's 1,200, never
  registered): Opus probe p137f landed it exactly, 1,400 (1,383) and both asks. The block bookings showed as 655 s208
  notices in Q4 2026 against about 20 a quarter, and normalised addresses linked 151 of the 324 earlier placed households
  to later cases (47 per cent, about 27 per cent within a year), a direct analogue in the same files, carried to the 2027
  window by a Kaplan-Meier curve. Every landing so far had an anomaly that invites a look plus an analogue a join can
  measure; the next candidate keeps the outside body steady and quiet, applies a validated model to a situation the
  record's units never had, ties the body to the quantity by an indirect domain link, and forces its size and rate from
  ordinary data with other uses.
- The serving personnel beside a new urgent treatment centre as the decisive step (architecture 3's second candidate,
  Harrowdown ICB's Wexley UTC, 2027 attendances; probe pack probe6, golden 12,500 against the model's 11,000, never
  registered): Opus probe p137h landed it, 12,500 (12,456.7) and the ask. It ran the model as filed (10,846), then
  calibrated the open centres' other attendances as 0.98 per cent of ICB attendances plus 0.99 times the model's demand
  for the census defence population, a fit that matched all three centres and explained Tolland's higher share by the
  RAF station; it knew the personnel are registered with Defence Medical Services, and it excluded the prison and the
  halls students correctly. Defence was the communal establishment table's largest category, and the open centres
  carried enough of it to calibrate the rate. The next candidate's outside body is small wherever the solver can
  measure it, absent from the open units, concentrated on the new one, and sized from data the model does not use.

- Re-root to architecture 3 (2026-10-26): architecture 2, the care world, is spent on probes (the pairs, the restarts and
  the step-down guests above), so the number moves to urban-regional-science / municipal-service-demand-resource-allocation
  with nothing of Calderbrook kept; architecture 3's first two candidates (above) died at the probe gate before
  registration, and the third, the Tanner Street custody hub (Harrowdown Police's on the probe pack, Calderwick Police's since stage 3), was missed by both probes (`## Draw`).

- Stage 3, ask B as each suite's initial health assessments in each quarter (16 figures): the closures reached only the
  quarters they fell in (six of sixteen cells), so a reader who joined the handover lines and kept the labelled suites
  kept ten; moved to day and night by suite (eight figures), every one of which a closure reaches (B6, B7).
- Stage 3, ask B framed as the custody healthcare tender: a second decision with its own owner (H18); its home is now
  the medical rooms of the same fit-out contract.
- Stage 3, Wendle Cross's refit as the only closure: it reaches two suites; Eastmoor's 19-day flood closure in August
  2025, with its team at Northgate, reaches the other two.
- Stage 3, an overflow booking into Wendle Cross during its refit: the nearest-suite overflow ignored the closure, so
  the arrest records' longest Wendle Cross gap fell inside the refit (22 December to 12 January); a closed suite takes
  no overflow.
- Stage 3, the refit's move at its planned 08:00: assessments of detainees booked before the move but seen after it
  read either way; the move is the minute after the last booking, and Eastmoor's planned closure was set at 14:20 so
  that no assessment of a detainee booked before either closure falls after it (B4, C1).
- Stage 3, co-defendants charged at the first-named defendant's time: the file's charge time served every defendant on
  it, so attaching them at the file's times was right; they are now charged in turn after the first-named defendant.
- Stage 3, every file keyed to its own detention: the co-defendant join was the only reconstruction and the reverse
  unmatched join finds it; 104 of the 2025-26 files now carry the case's earlier arrest, as a remand file does when the
  person was released and arrested again.
- Stage 3, a file matched to its detention by suite and charge time alone: two unrelated Southfields defendants were
  charged at 05:18 on 10 October 2025; the linked arrest is taken first and the charge-time match only where the linked
  arrest is an earlier release.
- Stage 3, the detention clock on UK wall-clock times: a hold across the October clock change came out an hour long;
  the clock is elapsed time in UTC and the remand times are its UK reading.
- Stage 3, remand stream 0 and 1: a cell-hours sum 0.02 hours from its rounding edge and a hold within two minutes of 24
  hours; stream 8 clears both (A4, A5).
- Stage 3, the probe pack's personas (Charlene Dale, Hugh Metcalfe): `guard.py names --geo GB --seed 137` does not give
  them; replaced with Liam Clayton and Emma Roberts from that draw.
- Stage 3, the BTP part as a graded figure to the nearest 10: the four sizings print 260, 270, 280 and 290; the part is
  stated with its method in the write-up and only the call is graded on its print.
- Stage 3, the city and force named Harrowdown (the probe pack's name): it contains Harrow, a real London borough
  with its own school, and is the name of a real Oxfordshire hill (H21); renamed Calderwick, with the estate's postcodes
  moved off the real HD and CV areas to unassigned ones (CK, CL). No figure moved.
- Stage 3, the prompt's question without the catchment: the estimand read only "the detentions the hub will book";
  it now names the six city centre wards the hub takes over, which is model 2.1's population and the domain's
  catchment (H20).
- Architecture 3 spent at stage 4 (2026-10-26, on d1d38e72): the determinism judge returned DETERMINISTIC on every
  committed figure with disposition SEND_BACK. Gate G read the call as a single conceptual flip (stumping family
  surface_read_rejection, surface_read_dependency yes, sole_data_defect yes) and Gate H its decisive step as
  data_semantics: the flip rests on the brief's coverage line ("one row per arrest by a Calderwick Police officer") and
  allocation note 2, and any BTP figure from 121 to 371 rounds to 4,000, so once the note is read nothing analytical can
  go wrong. Both scored readers landed 4,000: reader A (Sonnet) quoted note 2 as the decisive-step sentence (5 of 21 ask
  figures, 23.8 per cent, all five the chart's years; score_reader exit 1), and reader B (Opus, 3,754 plus about 265 BTP)
  wrote that what flips the answer between 3,750 and 4,000 is close to reading a stated rule and a field's definition.
  Neither took an ask figure: both re-keyed the files carrying a case's earlier arrest and missed the co-defendants, and
  both counted the closed suites' teams at their own suites. The probes missed only while the coverage fact was unfiled;
  filing it, which determinism needs, makes it semantics and lands it, so the same fact cannot be both Gate B's pin and
  silent. The judge's other findings, kept for the record and not fixed: pin 19:00 (nine first assessments start
  exactly then), pin the assessment unit and the "where it happened" wording, say defendants are counted from the arrest
  records, and the model PDF's header still reads HARROWDOWN POLICE (an upper-case leftover of the rename); reader B
  also flagged the HDL licence prefix and four arrests at the spring clock change booked before their arrest time (a
  local time in the skipped hour converted as GMT). By build-pipeline an architecture is spent on a SEND_BACK, and the
  retirement rule applies to this third spent architecture unless the author sets another cap; that decision is the
  author's, and no architecture 4 is drawn.

- Re-root to architecture 4 (2026-10-26): architecture 3 spent at stage 4 (above) and the author's ruling the same day
  that task137 is neither retired nor paused; the number moves to healthcare-delivery-health-economics /
  utilization-access-demand-forecasting with nothing of Calderwick kept.
- Architecture 4 backup candidate (probe8, 2026-10-26, never registered): Kestermoor District Council's 2027-28 Annual Tonnage Nomination to the Thrumley ERF, kerbside residual after a staggered weekly food waste rollout (two caddy-only pilot waves, then three waves that also swapped in a 180-litre residual bin, the 48-round wave 4 six periods in, wave 5 live from 2027-28 period 1), golden 53,000 against 55,000 to 58,000 for the static and pooled TWFE routes; died on Opus probe p137lb, which landed 53,000 (53,174.5) by comparing each wave period by period with wave 5, the one not yet treated, splitting the two packages and running wave 4 along wave 3's path: the package column in the rollout schedule hands over the clean comparison by package, so a staggered rollout with a documented package split is a reflex for the probe model, not a stump.
- Architecture 4 draw, explorer B's families: demand censored by capacity and vintages, never the staggered rollout. The
  recapture form (a patient turned away comes back on a later day and is counted twice, so only the refusals that never
  return are demand the record missed) was dropped before code: a regression of later days' visits on the turned-away
  counts is the opponent's own return check, which both probes then ran unprompted on probeB1. The deterrence form
  (a week of run-outs keeps the next week's patients away) went to the probe pack.
- Architecture 4 probe pack probeB1 (seed 16, a deterrence of 0.30 on every arrival, golden 54,000 against the default
  51,000 at the nearest 1,000): both Opus probes missed (`## Draw`), but its own rolling five-day share attenuated to
  52,000 (52,046) and its clean-day fits printed 49,000 and 52,000, forks a full pack could not ship.
- Stage 2 prototypes v2 and v3 (the deterrence on every arrival, the run-outs from staffing shortfalls): whenever the
  run-outs were scattered the rolling-window members attenuated a cell under the previous-week share, and a vacancy
  overlapping a surge gave the vacancy a t of 3 or more. The run-outs now come mostly from the hospital clinics' recall
  programmes, which run for weeks; the vacancy sits in summer; the bank backfills the long-term sickness lines; so every
  window files one call and staffing has no effect of its own (t 0.29 for the vacancy, -0.20 for staff on the floor).
- The deterrence on every GP-referred patient: it is now held by the seven practices with their own phlebotomy clinics
  (arrivals times exp(-0.45 x the previous week's run-out share)), the five without one untouched, so the step is a
  referral pattern the request forms' practice codes show rather than a property of every patient.
- The plan to the nearest 1,000: the deterrence specifications spread 44,035 to 45,114 across two cells. At the nearest
  2,500 they sit in one (43,750 to 46,250), with the default (42,561) and both careful-frame methods one cell under.
- A practice barcode blank on 3.1 per cent of GP forms: a solver counting GP-referred visits by practice code would
  have moved the call; 0.6 per cent now (426 forms), the same call either way (SF1).
- The annual report's sentence on the hospital clinics' recall programmes (which months each specialty recalled its
  patients): it named the run-outs' driver and made the GP dips readable beside it; removed, the programmes show only
  in the hospital-form visits by clinic code, which ask A counts.
- Personas outside the seed-137 draw (Liam Clayton, carried from architecture 3) and from it with first names older
  builds use (Rachel Reynolds, Patricia Bryant; Richard, Rebecca and Duncan also warn): replaced with Charlene Dale,
  Bethan Matthews and Joseph Wood from `guard.py names --geo GB --seed 137`.
- Strategy `causal_design` on the card: `ban.strategy` against task121's architecture 6 inside the three-build window,
  and `informative_censoring`, the nearest key, is task487's; filed as `other`.
- Brantmoor Community Hospital's booked clinic left unstated: with the turned away offered a booked slot there, "the hub
  takes every patient with a GP request, walk-in and booked" left open whether Brantmoor's own booked patients move to
  the hub, which no file counts; the annual report now says the booked clinic at Brantmoor carries on as now (SF10).
- A family-spread assertion at 0.4 of the printed unit: the 27 specifications spread 0.43 (44,035 for the programme-week
  dummy to 45,114 for the quiet-period fit over ten clinic days), every one at least 285 inside the cell; the assertion
  is one printed cell and a spread under 0.45, with the figure stated rather than the family trimmed.
- Stage 4 on zip 6611e937 (2026-10-26): the judge returned DETERMINISTIC with APPROVE (Gate G statistical_rigor,
  analytical_non_defect; Gate H analytical), and both scored readers missed the call at 42,500 (Sonnet on seen plus
  turned away, Opus on run-out days completed from the arrival profile); the asks leaked, the Opus reader keeping 36 of
  36 and the Sonnet reader 8 of 36.
- Ask A's device as a same-string reallocation of the clinic codes on 1 April 2026 with `code_in_use_from` in the
  register: the Opus reader read the column, mapped each old code by its request weekdays to the register's clinic days
  and took all 28 cells. Replaced by the new PAS's codes from 16 March 2026 and the 2026-27 templates from 1 April, which
  make that same weekday route name every old code wrongly; the link runs through the March fortnight instead.
- Ask B's device as one long-term sickness row carrying the absence's hours (270.00 and 337.50 on one day): an
  impossible day both readers spread over clinic days, taking all eight cells. Replaced by the e-roster unassigning a
  holder's line after five clinic days of sickness, so the absence reads as vacancy unless the holder is followed.
- The annual report's sentence dating the two long-term absences: it narrated ask B's device and went; the report keeps
  the one vacant post, and its definition now says vacant posts rather than vacant lines, so the literal execution is the
  golden.
- Clinic days left on the old weekdays after 1 April 2026: the old codes' weekdays then match their own specialties in
  the register and the careful route is exact; the 2026-27 templates give each specialty another's old weekdays, every
  set moving, so no old code keeps its match.
- Post-April requests moved to the nearest earlier template session: General medicine's requests stayed on Fridays while
  the register lists Tuesday, Wednesday and Friday; they are now drawn over the template's sessions in the week before,
  from their own random stream, so no other record moves.
- Item (a) of the judge's report: the underlying base printed as 41,714 reproduces only under the generator's exact
  specification (the judge refitted 41,663, the same plan); block 1, critical component 3, steps 3 and 4 and the golden
  workbook now state the model's figures to the nearest 100 (about 41,700, about 2,000 kept in-house, about 44,700 grown,
  a coefficient of about -0.21), counted figures exact. freeze.py rubric mode reports those three numbers as moved, which
  is item (a); nothing else on the main side moved.
- Item (b): "walk-in and booked" in section 6 left open whether booked GP patients at other sites join the hub; the
  report now says the hub's booked slots are for the same patients, who can book rather than queue.
- Stage 4 round 2 on zip d3c6d25d (2026-10-26): the judge returned DETERMINISTIC with a FIX_NOW on the intermediates'
  wording (applied as bands, the ship-ready zip 5c27c2ab), the Sonnet reader filed 42,500 with 0 of 36 asks, and the Opus
  reader landed 45,000 with 8 of 36: it fitted open days' GP-referred visits on weekday, financial year and month terms
  and ten daily lags of the days the kiosk filled (the lags summing to about -33 visits a run-out, peaking a week later,
  placebo leads flat) and predicted every 2025-26 day with no run-outs. The previous-week version died there: with the
  practices' in-housing held to the one calendar week after a run-out week, a fortnight of daily lags held all of it,
  so the careful reader's model was the golden's.
- Hardening screen on the clean world (seeds 26 to 37, the practices' in-housing persisting L weeks with a uniform
  weight, strength K): L 4 at K 0.45 to 0.9 left the ten-lag route at 45,000 on one to three seeds of 12, and twenty lags
  landed on 10 to 12; L 6 put the ten-lag route at 42,500 on 11 or 12 of 12, but twenty lags landed on 1 to 8 and thirty
  on 10 to 12; L 8 at K 0.75 to 0.8 put the ten-lag route at 42,500 on 12 of 12 with 1,120 or more to spare, twenty lags
  on none, thirty on 2 to 4, and the window chosen by AIC at 45,000 on 12 of 12. A geometric decay chosen by AIC read
  high (45,552 to 46,635 at K 0.8, one seed at 47,500), so the shipped seed was chosen with it at least 250 under the
  cell's top.
- Shipped-world seed screen (`generator/seeds.py`, the staffing seed 31 kept so the e-roster and ask B are unchanged;
  demand seeds 1 to 60 under L 8 at K 0.75 and 0.8 and L 7 at K 0.8 and 0.85): 31 of 240 worlds held every clean-world
  margin and 24 of them kept thirty lags off the call too. On the cut pack demand seed 48 at K 0.75 counted the
  parallel-run fortnight twice into 47,500 (46,408) and left an exposure form 136 inside the cell's top; seeds 1, 11,
  18, 21, 46, 55 and 56 each failed one or more assertions (an exposure form or twelve weekly lags within 250 of an
  edge, the fortnight counted twice leaving the cell, the trend cheaper than 100 in AIC, five weeks within 50 of the
  best, the eight-week window not picked, thirty lags reaching 45,000, a repeated count); demand seed 14 at K 0.8 passed
  every one.
- Records seed 31 under demand seed 14: Rheumatology's 2025-26 hospital-clinic visits read 363 in three quarters and
  Renal medicine's 411 twice, and seed 32 repeated a Gastroenterology quarter; a row with a value repeated across its
  quarters reads as a fill-down error, so seed 33, the first with four distinct quarters in every row, ships, and the
  rule is an assertion.
- The intermediates' band over the previous week's share and the previous ten clinic days' share (the round 2 fix): both
  windows are rungs now, so the band runs over the window the fit picks and the window next to it in fit (eight and
  nine weeks, 2.7 apart in AIC).
- The shipped pack carried `data_dictionary.csv` (column descriptions for seven files), which the new leak gate reads as a
  file describing the data: dropped 2026-11-01. Closure axis 19 now rests on the annual report's activity note and the
  systems' own labels, asserted with the data's convergence; the ask-side lines (Vacant line, request_date, clinic_days,
  clinic_code) left unstated, since the report's section 4 and the prompt's pins close the asks without them.
- Step 3's "every window of five weeks or fewer at least 67 worse" (the whole record's own margin) shipped on 8f5c6aa2;
  judge pass 5 reproduced 65.3 on the whole record and 62.6 on a common sample, so the step now states a bound computed over
  four samples (60, SF11), and steps 5 and 6 each gained one clause on the evidence that separates ask A's late-March
  link from the register's clinic_days and ask B's holder stretches from vacancies (SF12, SF13), no document changed.
- The ceiling recorded on the reship cut was a narrowed cracker's (2026-11-01, honest-cracker audit): the careful solver, every field read by its plain meaning, every filed rule executed and the hygiene battery run, keeps 8 of 36 against the recorded 0 of 36, SPENT on Ask B (Ask A holds, weakly), pair 40.7; the reason in one line: the annual report's section 4 names the one vacant post, so reading every unassigned line as vacant contradicts a filed fact; the other 67 follow a holder's Sickness lines. The ask layer is owed a /fix-rubric pass before delivery; the leak repair stands.
- The /fix-rubric re-site of Ask B (2026-11-01, after the honest-cracker audit) found no device that passes both tests, so nothing shipped: section 4 fixes each quarter's filled post-days (427, 411, 448, 441), the kiosk's 40 and 32 ticket rule and the queue bays fix which holders were off the floor each day (40, 45, 56, 31 holder-days), so only the label on those days is free and only the run it sits in can force it, which is the battery's sequence check; an as-of bank label on a holder's absence lines (43 label flips, 46 days at six substantive lines), a shadow key carrying her absences (never on the floor, 46 days at eight lines), a sickness keyed as worked (the ticket rule broken on every such day) and a relabelled absence type (no file records the type, so unforced) all died, new hospital-side records hand over Ask A's code link and GP-side ones carry the in-house signal; Ask A cannot be strengthened cheaply, its rows sitting in the queue export the call reads.
- The sickness ask cut and Ask A measured on its own (2026-11-02, the coordinator's decision after the re-site found no Ask B device): the cut moved no pack byte (target.zip md5 8f5c6aa2, every file the call reads asserted byte-identical) and no main-call figure (freeze rubric PASS), but the careful-solver cracker lands Ask A, because a careful solver tests the register's clinic_days on the 805 register-coded 2025-26 visits before naming the 16,417 old-code visits by them, the test fails on 328 of them with every off-schedule form issued 16 to 31 March and none from 1 April, and the late-March link follows (generator/ceiling.py: 28 of 28, pair 83.5, mirror leakage 100.0 per cent); nothing shipped, and the ask layer is owed a device on records the call does not read.
- The full replacement on new ask-only records (2026-11-02, /fix-rubric step 4b) found no device that passes both tests, so nothing shipped. The attempt was the anticoagulation service's dosing-system export of 2025-26 INR results, asked as the venous INR checks the walk-in clinic drew each month and the patients they were for each quarter (16 figures, the INR part of block A's residual that the ICB letter's 12 per cent a year moves to community pharmacies), prototyped on the generator's world and dead on the careful solver both ways: the anticoagulation clinic's own venous confirmations surface as same-patient same-day pairs in the near-duplicate item (101 pairs; 6 to 20 minutes after the clinic's fingerprick against 31 minutes or more after a pharmacy's), and Brantmoor's booked venous INRs surface in the received clock's hour profile (12 to 21 results in one minute on Monday and Thursday mornings, the courier's batch) and in the per-day check against block A's Haematology-form visits (28 days over), with the delay alone no clean forcing (walk-in up to 26 minutes, Brantmoor from 19); a reader told either finds it in a few lines. On paper: every hospital-clinic visit count is pinned by the frozen queue export (day, code and issue date, the new codes naming their specialties and the late-March weekday sets linking the old), hospital-clinic patients carry only identity devices (the batch's monoculture), requests, orders and re-bleeds die to key uniqueness and near-duplicates or are the refiled family, staff records are fixed by the bays and the 40 and 32 ticket rule, consumables, incidents, pay arrears and survey records die to the battery or fail H18, other service lines (inpatient rounds, the INR line's base) fail H18, GP-side records carry the in-house signal and Brantmoor's activity reopens SF5 and SF10. The ask layer needs a route outside /fix-rubric scope.
- The re-cut of the hospital forms' request_org and request_date, the fields the call never reads (2026-11-02, the main thread's route, one ask-only record allowed), found no device that passes both tests, so nothing shipped and no pack byte moved (target.zip md5 8f5c6aa2): each quarter's hospital-clinic visits are pinned by the check-ins the standing family reads, so the specialty split is the ask's only free dimension, and with no patient key or test on a hospital form the only hard contradiction of the register's mapping is a schedule one, which the careful solver's code-against-schedule validation and re-key item perform. Measured on the generator's world (session scratchpad task137_askrw2, nothing written to the pack): every variant that keeps a late-March link is landed (the shipped and a six-day window 28 of 28, off-schedule 0.43 and 0.55 before April against nil after; benign off-template forms at 0.05, 0.15 and 0.30 still 28, 28 and 24 of 28 at 0.45 to 0.50 against 0.04 to 0.21); a three-day window leaves the link unique for two codes of seven (8 of 28 landed, the rest unforced); the no-overlap re-cut (new codes and templates both from 1 April) is missed in all 28 cells but leaves the register's weekday mapping a clean one-to-one reading that no row contradicts (no form on a bank holiday or after its visit, and level continuity across April as good under the mapping for three codes, x0.81 to 1.07, as under the truth, x0.87 to 1.24 outside Rheumatology's recall); a fasting-share fingerprint on the free pathway field links six codes of seven and keeps both readings coherent (every fasting share moving at April, or every weekday set); Haematology's forms losing their barcode from 1 October 2025 drain its coded Q4 to nil beside 495 blanks, seen by a per-specialty series check and read literally as unattributed visits; an ask-only PAS session list under the new codes forces the link (exact weekday sets, seven of seven) and is the re-key item's own crosswalk (28 of 28); on paper, a shared block printer's code is re-derived by weekday or, on a shared weekday, unforced, and a request number with stale-form scans resolved by a bay collections file leaves the scanned form and the drawn request as two readings of a visit's specialty, the two sources' disagreement sending the careful solver to the bay-and-time join.
- Re-root to architecture 5 (2026-11-02): architecture 4 (the phlebotomy hub) kept a sound call (judge pass 6
  APPROVE) but its ask layer was spent: the honest-cracker audit landed both asks, and every /fix-rubric route on that
  world (the e-roster re-site, the INR replacement, the hospital forms' request fields) found no device both tests pass.
  The slot moves to Actuarial Science & Insurance (claims frequency for a self-insured delivery fleet), a client domain
  no architecture of the lineage used, with a new world, dataset, generator and shell (how-many | use | docx+xlsx
  against architecture 4's how-many | plan | png+xlsx); the ask records were named before registration this time.
- Draw candidates screened and dropped before this one (2026-11-02, paper and code): unemployment insurance benefit
  weeks after a potential-duration cut (the exit hazard riding the weeks left to exhaustion is task176 v2's external
  clock, and the behavioural response is the labour field's own reflex); job-search displacement at full rollout
  (`causal_design` in the three-build window, and the swap test fails: a hospital's discharge team competing for care
  home beds reads the same); selective lapse after a repricing (adverse selection is the insurance reflex); a TV
  campaign's audience decaying through longer breaks (a layout moving units into worse positions, task163's abstraction);
  a fleet forecast with the darkness rate taken from a ramp through civil twilight at 2.6 and day runs returning before
  dark (prototype `proto2.py` to `proto4.py`: the record's dark kilometres were 4 to 5 per cent, the dark rate's own
  noise spread the golden family by up to 15 per cent, and the overall per-kilometre rate landed within 5 per cent of
  the golden on most seeds because the darkness only moved from evening rush to quiet mornings).
- The engineer's staged authorisations as ask B's forcing record (2026-11-02, before any data was cut): they summed
  exactly to the genuine invoices, a control that ties only under the golden and a reconciliation the careful solver's
  battery runs, so they were an oracle; dropped, and the register's forward sensors (camera, or camera and radar) force
  the genuine calibration pairs instead.
- Ask B forced by the resend spells alone (copies paired one for one inside spells found by their share of week-old
  twins): the spells' first and last imports fall under any threshold (two cells kept copies worth 2,716 and 5,942), and
  outside the spells a late radar calibration is indistinguishable from a copy; the sensors close both.
- Darkness from an external formula (the NOAA equations at the depots' coordinates): replaced by the driver handbook's
  Appendix C (sunrise and sunset in GMT by seven-day row, with the summer-time rule), so every 2027 route-hour's light is
  recovered from shipped records alone (asserted, L2).
- The asks over the whole of 2026: repairs and recoveries of autumn 2026 collisions are incomplete at the pack date;
  the asks run to June 2026.
- The 2027 claims by calendar quarter to the nearest 25 (stage 4 watch item, 2026-11-02): the judge found the split thin
  (Q1 3.1 above 87.5; a pooled-hour light-only variant at Q4 112.8). Measured over 27 members (three constructions of
  light by nine models), month, hour and light puts Q4 at 87.4 and separate morning and evening multipliers or band by
  light cells on the last two years put it at 114.0 and 114.1, so the quarters would not hold; the split moved to April
  to September and the other six months at the nearest 50 (every member holds, nearest edges 20.9 and 7.1) and the
  repair-cost ask to depot by half-year (12 figures, the honest cracker still misses all), keeping the rubric at 27.
