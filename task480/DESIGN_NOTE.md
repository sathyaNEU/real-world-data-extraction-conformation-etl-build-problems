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
  1 January 2024, gasoline vehicles of model year 1996 and newer, the four newest model years exempt, even model years
  tested in even years) and its 2027 Vehicle Retirement Program (CMAQ-funded), which pays owners to retire registered
  gasoline cars and light trucks of model years 2001 to 2010 and holds intake events in each county whose eligible
  vehicles will emit at least 10 short tons of NOx in 2027. Counties (invented, screened against the US county and city
  register at edit distance two): Wexmoor, Linnmere, Halvering, Elkhollow, Dunmarsh, Quarrybrook, Marlbank, Larkhaven,
  Copperleaf, Thorncastle, Sallowford and Kinnard. Personas from `guard.py names --geo us --seed 480`: Bridget Palmer
  (Mobile Sources Section chief), Jacqueline Aguilar (Air Quality Division director).
- **Data-native sentence:** the area's inspections began in January 2024, so the first biennial cycle holds one
  odometer reading per vehicle; a car's yearly miles fall as it ages, from about 15,000 new to about 7,500 at twenty,
  so a reading divided by the car's age is the average of its longer early years, and the program's cars are the
  oldest the area has.
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

Task type: emissions-inventory (Physical & Environmental Sciences), which the taxonomy tags for ETL: the eligible fleet's 2027 NOx inventory is conformed from the registration snapshot, the inspection records, the station register and the model-year rate table, and its activity term is estimated from one cumulative odometer reading per vehicle.

Domain test: the quantity that decides the call is each county's 2027 on-road NOx from its eligible vehicles, the activity-times-rate sum a mobile source inventory builds, and the step that decides it is the inventory's mileage accumulation by age, estimated as the rise of the cumulative miles the inspected fleet has travelled by each age, with each vehicle's own reading setting its level.

Swap: "which of our twelve clinics' patients born in the 1960s will make at least 10,000 visits in 2027, each from a lifetime visit count" keeps the sentence and loses the analysis: a clinic records each visit when it happens, so nobody estimates this year's visits from a lifetime total, and nothing like a model-year emission rate, an inspection cycle that sees each vehicle once or an exemption for the newest model years shapes what the record holds.

Layer 1: biennial inspections by model-year parity with the four newest model years exempt; retests and aborted tests beside each initial test; VINs keyed by hand when the OBD read fails, joined back through the plate; odometer placeholders for unreadable odometers and kilometre readings on imported vehicles; registrations superseded by a transfer to another county left on file with a transferred status; tests at stations in another county than the registration; vehicles registered after the cycle with no reading yet; each asserted neutral on the call in checks.py.

Layer 2: estimation_fit. The methodological choice is how each eligible vehicle's 2027 miles are estimated from its one cumulative reading: the reading over the vehicle's age, that per-year average carried along its own trend by age, the fleet's yearly miles by age without the vehicle's own level, or the vehicle's own level against the fleet's cumulative curve by age times the curve's rise over the age the vehicle reaches in 2027.

Decisive step: estimating each eligible vehicle's 2027 miles as its own reading over the cumulative miles the inspected fleet has travelled by the vehicle's age at its test, times that cumulative curve's rise between the vehicle's ages at the start and the end of 2027, rather than as the reading over the vehicle's age.

Not semantics: reading every field correctly, the odometer as cumulative miles since new and the age from the model year as the guidelines set it, still leaves the easy route on the wrong counties: the reading over the age is a true average of every year the car has lived, and what it misses, that each year's miles fall with age, shows only in the cross-section of every inspected vehicle's reading read as a cumulative curve and differenced, which no file labels.

Not rule application: the guidelines file the population, the outcome (the miles a vehicle travels in calendar 2027 at the age it then is, times the Table 2 rate for its model year and class), the window, the unit, the 10-ton line, that a vehicle's 2027 miles are judged on its own reading, and the fill for vehicles without one; no filed rule says how a cumulative reading becomes one year's miles, and executing every stated rule with the reading over the age files the wrong set.

Analyst test: a strong analyst who conforms the registrations, the inspection records, the station register and the rate table and reads the guidelines correctly takes each eligible vehicle's reading over its age as its 2027 miles and files about seven counties; carrying that per-year average along its own trend by age still files six or seven; the fleet's yearly miles by age without each vehicle's own level files three; only each vehicle's level against the fleet's cumulative curve times the curve's rise over 2027 files the golden four (figures fixed at stage 2).

Estimand: the program guidelines file the population (gasoline cars and light trucks of model years 2001 to 2010 registered in a member county at 1 July 2026, including those with no 2024 to 2025 reading), the outcome (each vehicle's NOx in calendar 2027: its 2027 miles at the age it then is times the Table 2 rate), the window (calendar 2027), the unit (short tons per county) and the comparison (10 tons or more designates the county).

No decoy: nothing is planted to be caught: the state DOT's county road-mileage series and the fuel sales are genuine series on other bases, shipped as distractors; no memo, draft, earlier estimate or stakeholder figure ships; the 2025 pilot's close-out reports retirements and vouchers and no NOx; the decline of yearly miles with age is how cars are used, recorded nowhere as a rule.

No certified replay: no certified or published figure is reproduced to recover the method; no shipped table reports any county's 2027 miles or NOx, or any yearly mileage by age.

Lesson: one cumulative reading per unit holds the unit's level, not its current rate; the rate at an age is the rise of the cumulative curve the cross-section traces, and a unit's total over its age is the average of every age it has passed through, which overstates its rate wherever the rate falls with age.

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
