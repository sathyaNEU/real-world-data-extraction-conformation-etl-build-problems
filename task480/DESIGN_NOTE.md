# task480 design note: the 2027 Vehicle Retirement Program's intake counties

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task480.json` (architecture v2, architecture v1 in `lineage` as spent),
  registered 2026-10-21 at WARN: ETL in 9 of 12 is the lane; Gate G method_or_model_selection repeats task251 v4 and
  is answered by the decisive step being the estimator of a yearly amount at a future age from one cumulative reading
  per unit, not a reading or a rule; `test.same_driver_older` (time, G17, method_or_model_selection) is differentiated
  against task196 v1, which carries a rate forward from a panel; `driver.near` task133 v1 at 0.12 is a cumulative
  incidence filed among units that already survived part of the window, a left-truncation driver with nothing in
  common past the word cumulative. Axes redrawn before filing, each to the honester label: the stump strategy from
  grain_or_unit (task478's) to decomposition_attribution, because the golden splits each vehicle's cumulative miles
  across its years of age by the shape the inspected fleet shows and the default path splits them evenly; the decisive
  generator from G13 and then G2 (both in task476 v2's, task474 v6's and task478's signatures) to G17, the estimator of a
  rate at an age from a cross-section of totals, with G13 (a lifetime average put on one year) and G16 behind it; the
  context artifact from monitoring_export (task478's) to close_out_summary (the 2025 pilot's close-out); and, after
  task486 and task251 v4 filed at the pull, the organisation from a council of governments (local_government,
  council_or_assembly, programme_officer) to the state environmental quality department that runs both the inspection
  program and the retirement program (government_agency, funder_or_donor for the CMAQ request, operations_director for
  the section chief who runs both), which is also the honest owner of the inspection records.
- **Seed:** ET37 (a regional development agency replicating the cohesion categorisation of its regions). Kept: the
  decision form only, which territorial units a funded program designates, one unit at a time against a filed
  threshold. Replaced: the world (architecture 1's water utility is spent, and the seed's cohesion world carries no
  estimate) and the quantity, each county's 2027 NOx from the vehicles the program can retire, which is an estimate.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). The
  2027 inventory of the eligible fleet is conformed from the registration snapshot, the inspection records (the
  area's first biennial OBD cycle, 2024 and 2025, with each test's odometer reading), the station register, the
  model-year NOx rate table and the program guidelines, keyed by VIN with plate fallbacks, and its activity term (each
  vehicle's 2027 miles) has to be estimated from one cumulative reading per vehicle.
- **Shape:** other, a designation table: each county's eligible vehicles, their 2027 miles and their 2027 NOx with
  the county's verdict against the 10-ton line, the designated set, the chart's named parts, the asks' tables and the
  two files (arithmetic at stage 2 in `## Ask sheet`). Not 10 (one measure against one threshold per county, not a
  scorecard of several metrics) and not 07 (no grid of treatments).
- **Strategy:** decomposition_attribution. A vehicle's odometer is the sum of the miles it travelled at every age it
  has passed, and a car travels fewer miles each year as it ages; the reading over the vehicle's age spreads the total
  evenly across those years, while the inspected fleet's readings by age trace the cumulative curve whose rise at each
  age is that year's miles. Decisive generator G17, with G13 (the lifetime average put on one future year) and G16.
- **World:** United States, an unnamed state: the Department of Environmental Quality's Mobile Sources Section runs
  the enhanced inspection program of a fictional twelve-county ozone nonattainment area (biennial OBD tests from
  1 January 2024, gasoline vehicles of model year 1996 and newer, the four newest model years exempt, the first
  cycle's inspection year set by the last digit of the VIN) and its 2027 Vehicle Retirement Program (CMAQ-funded),
  which pays owners to retire registered gasoline cars and light trucks of model years 2005 to 2014 (the 2025 pilot
  took 2001 to 2010) and holds intake events in each county whose eligible
  vehicles will emit at least 10 short tons of NOx in 2027. Counties (invented, screened against the US county and city
  register at edit distance two): Wexmoor, Linnmere, Halvering, Elkhollow, Dunmarsh, Quarrybrook, Marlbank, Larkhaven,
  Copperleaf, Thorncastle, Sallowford and Kinnard. Personas from `guard.py names --geo us --seed 480`: Bridget Palmer
  (Mobile Sources Section chief), Jacqueline Aguilar (Air Quality Division director).
- **Data-native sentence:** the area's inspections began in January 2024, so the first biennial cycle holds one
  odometer reading per vehicle; a car's yearly miles fall as it ages, from about 15,000 new to about 8,000 at twenty,
  so a reading divided by the car's age is the average of its longer early years, and the program's cars are among
  the oldest the area has.
- **Forcing fact:** the funding request for the 2027 program year (forward); the quantity is calendar 2027's NOx from
  vehicles registered at 1 July 2026, a year not yet begun.
- **Forum and forcing event:** funder_or_donor (the state DOT's CMAQ office approves the request and its intake
  county list), budget_or_appropriation (the 2027 CMAQ obligation). Organisation family government_agency.
- **Sources, one line each:** seed ET37 (the decision form only); EPA MOVES activity inputs (vehicle age
  distributions and relative mileage accumulation by age, learned, never shipped); California EMFAC's mileage accrual,
  estimated from Smog Check odometer readings by age (the field method the decisive step is: the rise of the
  cumulative curve, not the reading over the age); OBD-II inspection program practice (biennial by model-year parity,
  new-vehicle exemptions, retests, the odometer as keyed by the inspector); CMAQ cost-effectiveness practice for
  vehicle retirement (tons of NOx a retired vehicle would have emitted).

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences), which the taxonomy tags for ETL: the eligible fleet's 2027 NOx inventory is conformed from the registration snapshot, the inspection records, the body codes and the model-year rate table, and its activity term is estimated from one cumulative odometer reading per vehicle.

Domain test: the quantity that decides the call is each county's 2027 on-road NOx from its eligible vehicles, the activity-times-rate sum a mobile source inventory builds, and the step that decides it is the inventory's mileage accumulation by age, estimated as the rise of the cumulative miles the inspected fleet has travelled by each age, with each vehicle's own reading setting its level.

Swap: "which of our twelve clinics' patients born in the 1960s will make at least 10,000 visits in 2027, each from a lifetime visit count" keeps the sentence and loses the analysis: a clinic records each visit when it happens, so nobody estimates this year's visits from a lifetime total, and nothing like a model-year emission rate, an inspection cycle that sees each vehicle once or an exemption for the newest model years shapes what the record holds.

Layer 1: the first cycle's inspection year set by the last digit of the VIN, with the four newest model years exempt; aborted attempts and retests beside each initial test; VINs typed by hand where the OBD read fails, joined back through the plate and model year the lane found; odometers entered as 0 or 999999 when unreadable, and kilometre readings; transferred records left on file when a vehicle moved county; tests at stations in another county; vehicles registered after their cycle year with no reading yet (the 3.4 fill); each mishandled in checks.py R2 with the call and every county's whole tons unchanged.

Layer 2: estimation_fit. The methodological choice is how each eligible vehicle's 2027 miles are estimated from its one cumulative reading: the reading over the vehicle's age, that per-year average carried along the trend of lifetime averages by age, the fleet's cumulative curve without the vehicle's own level, or the vehicle's own level against the fleet's cumulative curve by age times the curve's rise over the ages the vehicle passes through in 2027.

Decisive step: estimating each eligible vehicle's 2027 miles as its own reading over the cumulative miles the inspected fleet has travelled by the vehicle's age at its test, times that cumulative curve's rise between the vehicle's ages at the start and the end of 2027, rather than as the reading over the vehicle's age.

Not semantics: reading every field correctly, the odometer as cumulative miles since new and the age from the model year as the guidelines set it, still leaves the easy route on the wrong counties: the reading over the age is a true average of every year the car has lived, and what it misses, that each year's miles fall with age, shows only in the cross-section of every inspected vehicle's reading read as a cumulative curve and differenced, which no file labels.

Not rule application: the guidelines file the population, the outcome (the miles a vehicle will travel in calendar 2027 times the Table 2 rate for its model year and class), the window, the unit, the 10-ton line, that a vehicle's 2027 miles are judged on its own reading, and the fill for vehicles without one; no filed rule says how a cumulative reading becomes one year's miles, and executing every stated rule with the reading over the age files the wrong set (checks.py R3a).

Analyst test: a strong analyst who conforms the registrations, the inspection records and the rate table and reads the guidelines correctly takes each eligible vehicle's reading over its age as its 2027 miles and files nine counties, the golden five plus Dunmarsh, Larkhaven, Quarrybrook and Copperleaf; carrying that per-year average along the trend of the lifetime averages by age still files the nine; the fleet's cumulative curve without each vehicle's own level files four, Dunmarsh in and Elkhollow and Marlbank out; only each vehicle's level against the fleet's cumulative curve times the curve's rise over 2027 files the golden five (checks.py R3a and R3b, on the generator's clean truth as on the pack).

Estimand: the program guidelines file the population (gasoline and flex-fuel cars and light trucks of model years 2005 to 2014, GVWR class 1 or 2a, with an ACTIVE record in a member county on the 1 July 2026 snapshot, including those with no 2024 to 2025 reading), the outcome (each vehicle's NOx in calendar 2027: the miles it will travel in 2027 times the Table 2 running exhaust rate), the window (calendar 2027), the unit (short tons of 907,184.74 grams per county) and the comparison (10.0 tons or more, before rounding, designates the county).

No decoy: nothing is planted to be caught: the state DOT's county road mileage, the fuel sales and the population estimates are genuine series on other bases, shipped as distractors; no memo, draft, earlier estimate or stakeholder figure ships; the 2025 pilot's close-out reports letters, applications and approvals and no NOx or per-county figure; the decline of yearly miles with age is how cars are used, recorded nowhere as a rule.

No certified replay: no certified or published figure is reproduced to recover the method; no shipped table reports any county's 2027 miles or NOx, any yearly mileage by age or any inventory.

Lesson: one cumulative reading per unit holds the unit's level, not its current rate; the rate at an age is the rise of the cumulative curve the cross-section traces, and a unit's total over its age is the average of every age it has passed through, which overstates its rate wherever the rate falls with age.

## Default path

1. Conform the snapshot: the ACTIVE records in the twelve member counties of model years 2005 to 2014, fuel G or F,
   GVWR 1 or 2a (65,305 vehicles), each with its first completed initial test by VIN, else by plate and model year
   for a typed VIN, 0 and 999999 dropped and kilometres converted (61,865 with a reading).
2. Take each vehicle's 2027 miles as its odometer over its age at the test, the age from 1 January of its model year:
   the miles a year it has travelled.
3. Fill the vehicles without a reading with their county and model year's average (3.4), multiply by the Table 2
   rate for the model year and class, sum each county in short tons.
4. Designate the counties at 10.0 tons or more.

Ends on: nine counties, the golden five plus Dunmarsh, Larkhaven, Quarrybrook and Copperleaf
Golden: five counties, Wexmoor, Halvering, Linnmere, Elkhollow and Marlbank

## Stump sentence

The default path takes each eligible vehicle's odometer over its age as its 2027 miles and files nine counties, the
golden five plus Dunmarsh, Larkhaven, Quarrybrook and Copperleaf, because the reading over the age is the average of
every year the car has been driven and a car is driven fewer miles each year as it ages; the readings of every
inspected vehicle by age trace the cumulative curve whose rise over 2027 is a car's 2027 miles at the ages it then
passes through, each vehicle's reading against that curve sets its own level, and that files the golden five.

## Readability screen

| Rung | What the solver must see | Where it is | Verdict |
|---|---|---|---|
| R0, the area's average reading over age on every vehicle | one number from the readings | the first thing a reading invites | readable |
| R1, each vehicle's reading over its age (the default path) | the guidelines' own reading, an age, a divide | 3.3 names the reading and the age convention | readable |
| R1c, that average carried along the trend of lifetime averages by age | lifetime averages fall with age across the fleet | a plot of reading over age against age | readable |
| R2, the fleet's cumulative curve's rise without the vehicle's level | yearly miles fall with age; the curve's rise is a year's miles | the cross-section read as a cumulative curve | readable |
| R3 (decisive), the vehicle's level against the cumulative curve times the curve's rise over 2027 | the reading is the vehicle's level on the curve, not its rate; its 2027 miles are its level times the curve's rise at its 2027 ages | no file states a yearly mileage, a curve or a level; only the readings of every age read together as one cumulative curve and differenced | silent |
| R3t, the vehicle's level times the curve's slope at its test age | the window: the rate at the 2024 or 2025 test, not 2027 | 3.2's "in calendar year 2027" | readable |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | eligible car or light truck | 2.1: fuel G or F, model year 2005 to 2014, GVWR 1 or 2a | any fuel, any weight | another population | 2.1 filed |
| SF2 | registered on 1 July 2026 | an ACTIVE record in the county on the snapshot | any record dated before the snapshot | another population | 2.1 filed |
| SF3 | in 2027 | calendar year 2027 | the program year or the fiscal year | same window | 3.1 and 1 (program year 1 January to 31 December) |
| SF4 | 10 short tons or more | the unrounded county total against 10.0 | rounded first | same call | 3.1 filed; no county within 7 per cent of the line across the family |
| SF5 | short ton | 2,000 pounds, 907,184.74 grams | metric tonne | another figure | 3.2 filed |
| SF6 | the rate's class | the body code's program class | GVWR class | another rate | 3.2 filed; every eligible body code maps |
| SF7 | the reading | the first completed initial test | an aborted attempt, a retest | same call | 3.3; aborts carry no odometer; R2 asserts the retest reading |
| SF8 | the vehicle's age | years from 1 January of the model year | from the title date | another age | 3.3 filed |
| SF9 | no usable reading | the county and model year average of the 2027 miles | dropped, the county average | another figure | 3.4 filed; every county and model year has read vehicles |
| SF10 | kilometre odometers | converted to miles | read as miles | same call | the notes name KM; R2 asserts |
| SF11 | a typed VIN that matches no registration | the plate and model year the lane found | left unread | same call | the notes; R2 asserts |
| SF12 | the miles over 2027 | the curve's rise from the age on 1 January 2027 to 1 January 2028 | the slope at the mid-2027 age | same call and figures | checks.py asserts |
| SF13 | the cumulative curve | any smooth fit of every completed initial reading | cubic, quartic, local linear, one-year means, model-year means, through the origin, lifetime-average fits, eligible model years only, ages 10 and over, county curves, exponential decay | same call and figures | the fifteen-member family in checks.py; the power and log-quadratic forms rejected by the one-year means |
| SF14 | a vehicle | one ACTIVE record per VIN | each record | same call | checks.py asserts one ACTIVE record per VIN |
| SF15 | member counties | county_codes.csv's twelve | the counties on the snapshot | same set | 3.5 filed |
| SF16 | to the nearest short ton | from the unrounded county total | rounded per vehicle | same figures | the prompt; no family member within 0.16 of an edge |
| SF17 | NOx | running exhaust (Table 2) | with starts | another figure | 3.2 filed |
| SF18 | program class codes | PC and LT | any other | same rate | the body code list carries two |

## Ladder

| Rung | Route | Files | Separation |
|---|---|---|---|
| R0 | the area's average reading over age on every read vehicle | nine: the five plus Dunmarsh, Larkhaven, Quarrybrook, Thorncastle | every county figure missed |
| R1 | each vehicle's reading over its age (default path) | nine: the five plus Copperleaf, Dunmarsh, Larkhaven, Quarrybrook | the four added at 11.37 to 12.81 tons, Thorncastle out at 8.55; every county figure missed |
| R1c | R1 carried along the trend of lifetime averages by age | the same nine | every county figure missed |
| R1d | each county's linear slope of readings on age | the same nine | every county figure missed |
| R2 | the fleet curve's rise over 2027 without the vehicle's level | four: Wexmoor, Halvering, Linnmere, Dunmarsh (10.75) | Elkhollow 9.10 and Marlbank 9.29 out; 11 of 12 figures missed |
| R3t | the vehicle's level times the curve's slope at its test age | the golden five | 11 of 12 county figures missed (the window) |
| Golden | the vehicle's level against the curve times its rise over 2027 | five: Wexmoor 15, Halvering 14, Linnmere 13, Elkhollow 12, Marlbank 11 | Marlbank 10.94 lowest in, Dunmarsh 8.94 highest out; across the family 10.72 and 9.15 |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | ACTIVE records on the 1 July 2026 snapshot in a member county, 2.1's model years, fuels and weights, unread vehicles included | filed at 2.1 and 3.4; transferred records C1 (R2) |
| 2 Unit of account | the vehicle, summed to the county | the question; one ACTIVE record per VIN (SF14) |
| 3 Attribution window | calendar 2027 at the ages a vehicle passes through in it | filed at 3.1 and 3.2; SF12 converges |
| 4 As-of dating | the snapshot of 1 July 2026; the 2024 to 2025 cycle's readings | filed at 2.1 and 3.3 |
| 5 Version basis | one snapshot, one test extract, one rate table | nothing to choose |
| 6 Denominator | none in the call; the fill averages the read vehicles of the county and model year | filed at 3.4 |
| 7 Weighting | every reading counted once in the curve | C3: one-year and model-year means, subsets and county curves agree (SF13) |
| 8 Window length | the whole first cycle | C1: every vehicle has one cycle |
| 9 Boundary inclusivity | 10.0 or more, unrounded | filed at 3.1; nothing within 7 per cent of the line |
| 10 Rounding path | county totals unrounded, whole tons at the end | the prompt; edges 0.16 or more (SF16) |
| 11 Tie-break | none | no two counties within a ton of each other at the line |
| 12 Maturity and censoring | vehicles not yet inspected carry no reading | filed fill at 3.4; the exempt newest model years lie outside 2005 to 2014 |
| 13 Order of operations | 2027 miles, the fill, then each vehicle's own rate | filed: 3.4 fills the 2027 miles and 3.2 applies the vehicle's rate to them |
| 14 Row order | the earliest completed initial test | C1: one completed initial per vehicle |
| 15 Duplicate resolution | no repeated test record; aborts and retests beside the initial | R2 asserts both readings |
| 16 Identity normalisation | VIN, else plate and model year for a typed VIN | R2: same call unmatched |
| 17 Netting against gross | none | nothing nets |
| 18 Dimensional units | odometer units; grams to short tons | the notes name KM; 3.2 files the ton |
| 19 Code and status semantics | record_status, fuel_code, gvwr_class, body codes to class | the notes and 2.1, 3.2 |
| 20 Integerisation | none in the call | miles and grams continuous |
| 21 Clause scope | 3.4's fill covers both no test and an unreadable odometer | filed in 3.4's parenthesis |
| 22 Forward window contents | 2027's miles from the 2024 to 2025 readings | the decisive step; the method open, forced by the data (SF13, the family and the rejected forms) |

## Literal reader

Executing the prompt and guidelines 2.1 to 3.5 word for word: the eligible vehicles are 2.1's; each vehicle's 2027
miles are "judged on its own odometer reading at its initial inspection" (3.3), which names the evidence and leaves
the estimator to the analyst, and 3.2 makes the quantity "the miles it will travel in calendar year 2027"; the
reading over the age is a different quantity, the mean of the years already travelled; the cumulative curve's rise
over 2027 at the vehicle's level is the year's miles, and every smooth fit of the curve on every reasonable subset of
the readings (fifteen members, checks.py) gives the golden five and the same whole tons in every county; every other
term (SF1 to SF18) has one filed reading or converges.

## Oracles

None ship. No file states any county's 2027 miles or NOx, any yearly mileage by age or the designated set; the pilot
close-out gives letters, applications, approvals and declines, no per-county retirements or payments; the 2024 annual
report lists the stations and no per-county test counts; the DOT road mileage, fuel sales and population series are
on other bases (distractors in metadata.json, each ruled out by 2.1 or 3.3) and no shipped artifact ranks the counties.

## Ask sheet

- **Ask A, the 2025 pilot** (8 figures): the vehicles the pilot retired in each of its four counties and what the
  Department paid dismantlers for them. Its tie to the call: the funding request the call goes into prices the 2027
  program on what the pilot actually retired and paid. Devices: D5, a PAID voucher whose vehicle has an ACTIVE record
  again on the snapshot was not retired (62 vouchers; benign twins, 53 voucher vehicles carry a transferred record
  from a move before the pilot and were retired); D6, Oakhaven Salvage & Parts' billing export writes each invoice's
  total on every line (1.56 times Elkhollow's true charges), while the other two dismantlers bill one amount per tow
  zone and 4.2 says the charges are the same at every dismantler.
- **Construction layer** (the call's own rows): each county's NOx and verdict and the chart of the twelve against the
  line; no device rows in the call's population (the 62 reinstated vehicles dropped leave every figure, asserted).

Pair ceiling: 32.1 (cracker 45.0 on the call with no ask figure kept, mirror 19.2 at R1 keeping 8 of the 25 main criteria; the cracker's ask path is the one all six stage 4 readers took, every PAID voucher priced at its tow zone's charge)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/ceiling.py on the cut pack

| Ask | Figure | Golden | The cracker's path | Cracker |
|---|---|---|---|---|
| A | Elkhollow vehicles retired | 222 | 238 (every PAID voucher) | miss |
| A | Elkhollow dismantler charges | $59,050 | $63,405 (reinstated left in, zone charges) | miss |
| A | Dunmarsh vehicles retired | 201 | 214 | miss |
| A | Dunmarsh dismantler charges | $53,985 | $57,640 | miss |
| A | Larkhaven vehicles retired | 154 | 171 | miss |
| A | Larkhaven dismantler charges | $42,590 | $47,280 | miss |
| A | Kinnard vehicles retired | 102 | 118 | miss |
| A | Kinnard dismantler charges | $26,625 | $30,720 | miss |

## Tried and rejected

- 2026-10-20, at the draw: the seed's own quantity, each NUTS 2 region's GDP per head in PPS against 75 and 100 per
  cent of the EU-27 average: every input (regional GDP, average population, national PPPs, the EU average) is a
  published aggregate, so the categorisation is arithmetic once the NUTS version, the average and the vintage are
  read; the seed's three moves are data semantics and rule application by construction.
- 2026-10-20, at the draw: putting an estimate into the seed's quantity: rebuilding regions across a NUTS boundary
  that splits a NUTS 3 unit is task474 v1's and task476 v1's spent split driver; a nowcast of the latest year's
  regional GDP is Forecasting with an open estimator family; carrying the national statistics institute's coming
  benchmark revision into the regional figures through the overlap years recovers the institute's method from its
  own published vintages (a certified replay); a register's population over-coverage is the census-register ground
  task471, task448 and task455 have spent.
- 2026-10-20, at the draw: other worlds screened before this one: attendance rebuilt from tickets by a show-up rate
  conditioned on booking lead time (composition_mix sat in the ban window behind task481, and a yield conditioned
  on a per-case property and measured where the record is complete is task473's driver); length of stay from
  stock over entries by Little's law (one divide, readable); weekly overtime from biweekly totals (the after-migration
  ratio per site lands the golden); direct-store-delivery shortages against theft (the warehouse-supplied categories
  are an unaffected subset that ranks stores with no model); a pooled percentile from published percentiles (the
  "never average percentiles" reflex reaches the mixture).
- 2026-10-20, stage 2: the under-registration rising with meter age, fitted by age: linear, quadratic and banded fits
  of a slope of 0.3 points a year moved the town-centre zones' indices by 0.05 to 0.1 across forms, so the graded
  indices forked; the meters' error is now one level for the mechanical fleet, varying meter to meter.
- 2026-10-20, stage 2: the town-centre flats exchanged last and the suburbs first with only a class-level summer:
  every pooled control landed within 0.5 points of the golden by composition (already-exchanged suburbs match the
  exchanged suburbs), so the first reflex reached the call; the rollout now opens and closes on town-centre zones and
  2024 was a normal year, so every pooled and tariff route over-corrects.
- 2026-10-20, stage 2: route reads spread nine days either side of the quarter end with estimated reads at 4 per
  cent: the smeared mechanical quarters put the per-meter averages 0.4 to 1.0 points under the volume share and pulled
  the tariff route's per-meter median onto the golden; reads now fall within three days of the quarter end and 1.5
  per cent are estimated.
- 2026-10-20, stage 2, asks: contracts in force at the end of 2025 (no device a reader would not adjudicate from the
  status and date columns); mains failures across a work-management cutover (migration duplicates are executed by
  the hygiene battery, proven-in-production Part 2); asbestos-cement length across a material-code renumbering (the
  old code book is nowhere in the pack, so the device is not fair).
- 2026-10-21, architecture 1 spent at stage 4 (the water utility's zone leakage index, the old meters'
  under-registration read across the staggered smart-meter exchange against same-type premises whose meters did not
  change): scored leak reader 2 landed the call, eight zones at 4.3 per cent, by netting each exchanged meter's step
  against unchanged premises of the same type and checking it with a placebo, and reader 1 filed seven with type
  controls stratified by consumption band, so the matched comparison is a medium reader's reflex once a staggered
  rollout is visible; both readers kept all 32 ask figures (the SCADA UTC stamps fell to the daylight-saving shift of
  the night profile, the GIS 2008 install-year placeholder to its spike and the works register); the judge returned
  DETERMINISTIC with FIX_NOW on the 4.3 per cent figure, whose estimator family spans 3.5 to 4.5 per cent against a
  printed unit of 0.1. Re-rooted fresh by the author's rule: no staggered rollout or treated-against-untreated
  comparison in the new world, every graded figure printed at the precision its estimator family supports, and no ask
  device a clock profile or a value spike can find.
- 2026-10-21, stage 2: the 2027 program's model years 2001 to 2010: their 2027 ages, 17 to 27, sit at the thin old end
  of the readings, where an exponential decay of yearly miles fits the one-year means as well as the quadratic
  (chi-square 33 against 33 on 27) and puts every county 4 to 5 per cent higher, so the whole tons forked across
  forms the record cannot separate; the program now takes model years 2005 to 2014, whose 2027 ages lie inside the
  bulk of the readings, and the fifteen-member family agrees in every county.
- 2026-10-21, stage 2: first sales centred three months before the model year began: the cumulative curve then has an
  intercept, and fits through the origin or of the lifetime average moved every county by 4 to 7 per cent; first
  sales now centre on 1 January of the model year.
- 2026-10-21, stage 2: county-by-county curves on the counties' first random draws spread up to 9 per cent around the
  pooled curve; each county's draw is now the one whose own curve agrees with the pooled one, and its intensity sets
  its level mid-bin.
- 2026-10-21, stage 2, asks: station numbers given again only between counties whose drivers do not cross left three
  counties' counts unchanged under the current licence; each reissued pair now shares a commuting corridor.
- 2026-10-21, stage 2: a lane computer's re-sent March 2025 rows (exact repeats at one station): a copied block is a
  plant kind even when the call ignores it; removed.
- 2026-10-21, stage 4 round 1, ask B: the station register's licensed_since column: both scored readers compared each
  test date with it, took the 2024 report's county before it, and kept all twelve station figures (score_reader 20 of
  44 each, call missed by both on the default path); the register now carries no licence date, so the reissue is a
  cross-file conflict and the hand-over is the pause in the number's own tests.
- 2026-10-21, stage 4 round 2, ask B: with no licence date on the register, reader C still split each reused number
  at the pause in its tests and kept all twelve station figures, and reader D kept seven from the 2024 report's
  closure dates; a station number reused across counties is a map every careful reader reconciles, so the station
  ask is retired, the register stays as a declared distractor, and the ask layer is the pilot (0 of 8 for all four
  readers).
