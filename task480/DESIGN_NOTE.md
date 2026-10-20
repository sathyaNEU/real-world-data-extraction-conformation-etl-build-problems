# task480 design note: the 2027 network renewal zones of an intermunicipal water utility

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task480.json` (architecture v1), registered 2026-10-20 at WARN: ETL in 8
  of 12 is the lane; Gate G method_or_model_selection in 7 of 12 is answered by the decisive step being which
  comparison measures the old meters' error, not a reading or a rule; `test.same_puzzle_older` and
  `test.same_driver_older` (population, G16) are differentiated line by line against task236, task453 v1, task463,
  task104, task134 v1, task177, task501 v4 r1 and task70 v2, none of which measures an instrument's error against
  instruments not yet replaced. Nearest driver task73 world nine at 0.07.
- **Seed:** ET37 (a regional development agency replicating the 2021 to 2027 cohesion categorisation of its NUTS 2
  regions by GDP per head in PPS). Kept: the world (an EU member state's cohesion-funded eligibility, decided one
  territorial unit at a time against a filed threshold) and the decision (which units are eligible). Replaced: the
  quantity. GDP per head in PPS is a ratio of published aggregates, so once the NUTS version, the EU average and the
  vintage are read the categorisation is arithmetic; every route that puts an estimate into it is spent or banned
  (`## Tried and rejected`). Each metering zone's infrastructure leakage index is the quantity a cohesion-funded
  water loss call actually turns on, and it is an estimate.
- **Pairing:** Business & Operations Analytics (house domain, mapping to General Statistics & Data Science) /
  field-service-maintenance / Data Extraction & Conformation (ETL). The client task type is
  data-integration-record-linkage-entity-resolution: the zone water balance is conformed from bulk inlet meters,
  quarterly billing reads, the smart-meter rollout's work orders, the meter and customer registers, the network
  register, pressure loggers and the unbilled-use logs, and one source's measurement error (the old meters') has to
  be estimated from how two sources disagree over the same customers.
- **Shape:** 07, a grid: each zone's 2025 system input, authorised consumption, apparent losses, real losses,
  unavoidable real losses and index, the eligible set and its count, the chart's named parts and the two files.
- **Strategy:** causal_design. The rollout is a staggered replacement, zone by zone through 2024 and 2025; each
  replaced meter's step across its replacement is its old meter's under-registration plus whatever moved every
  customer's demand between the two windows, and 2025's hot dry summer raised houses' outdoor use far more than flats'.
  Decisive generator G16 (the comparison the design implies), with G3 (the meter's record against the water
  delivered) and G6 (the rise differs by customer class).
- **World:** Portugal, a fictional intermunicipal water utility in the Centro region, sixteen metering zones (ZMC),
  mechanical multi-jet and volumetric meters installed 1996 to 2021, ultrasonic smart meters from October 2023.
  The utility applies to the 2027 network renewal call of the national cohesion programme's water efficiency
  measure; the call funds mains and service renewal in metering zones whose 2025 infrastructure leakage index is 4.0
  or more. Personas from `guard.py names --geo Portugal --seed 480`: Adriana Paiva (head of non-revenue water),
  Leandro Vieira (operations director).
- **Data-native sentence:** the utility replaced its mechanical meters zone by zone through 2024 and 2025, and 2025's
  hot dry summer raised houses' garden use by about a tenth while flats barely moved, so a replaced meter's step
  across its replacement is its old meter's error plus that summer, and the zones still read on old meters in 2025
  are the ones whose balance the error inflates.
- **Forcing fact:** the call closes on 31 March 2027 and funds 2027 to 2029 works (forward); its quantity is the
  closed year 2025, the most recent complete water balance the call names.
- **Forum and forcing event:** funder_or_donor (the programme's managing authority receives the application),
  budget_or_appropriation (the call's allocation round). Organisation family utility_or_infrastructure.
- **Sources, one line each:** seed ET37 (the world and the decision, never its quantity or mechanism); the client's
  canonical Layer 2 example (a staggered rollout read against units not yet treated) learned, not copied: here the
  treatment is an instrument swap, the effect is the instrument's own error, and the comparison has to match the
  customer class whose demand moved; IWA water balance and infrastructure leakage index (the filed estimand and the
  unavoidable-loss formula, Layer 1 and rule application in the lower rungs); AWWA M36 / IWA apparent-loss practice
  (bench tests at standard flows understate in-service error, a rung the call's rule closes).

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science, the client domain the house domain business-operations-analytics maps to), which the taxonomy tags for ETL: the zone water balance is conformed from bulk inlet meters, billing reads on two meter technologies, the rollout's work orders and four registers, and the old meters' measurement error is estimated from how the two technologies disagree over the same customers.

Domain test: the quantity that decides the call is each zone's current annual real losses, the IWA water balance residual once authorised consumption and apparent losses are taken out, set against the zone's unavoidable real losses; water loss management measures the customer-meter part of apparent losses from meters in service, here from the step each meter's replacement reveals, read against customers of the same class whose old meters were not yet replaced over the same quarters.

Swap: "which of our sixteen hospitals' bed-days per admission reach 4.0 once the old admission system's undercount is taken out" keeps the sentence and loses the analysis: no balance residual absorbs an instrument's error, no instrument ages, and no staggered replacement reveals what the old one missed.

Layer 1: quarterly manual reads with estimated reads trued up at the next actual read (the billing system's no-access rule); the old meter's final read and the new meter's start read on each work order, splitting a billing period; bulk inlet meters with SCADA gaps and inter-zone transfer meters; unbilled authorised use from firefighting and flushing logs; pressure loggers reporting in bar or in metres head; customer, meter and premises registers keyed by different identifiers; each asserted neutral on the call in checks.py.

Layer 2: estimand_identification. The methodological choice is what each replaced meter's step is read against: nothing (billed consumption taken as delivered), the manufacturer's or the bench's curve, the meter's own consumption a year earlier, every not-yet-replaced customer, or not-yet-replaced customers of the same class, by meter age.

Decisive step: measuring each old meter's under-registration as its consumption step across replacement net of the change shown over the same quarters by customers of the same class whose meters were not yet replaced, fitted on meter age, and applying it to the 2025 consumption still read on old meters before the real losses and the index are formed.

Not semantics: reading every field correctly, including that the old meters' reads are what they recorded and the smart meters' are what was delivered, still leaves the easy route on the wrong zones: the step a careful analyst measures from each meter's own history is a true difference of two correct reads, and what it carries besides the error (2025's summer, which no file labels) is visible only against the customers not yet replaced.

Not rule application: the call files the threshold, the IWA balance, the unavoidable-loss formula and that metering inaccuracy is measured from meters in service; no filed rule says against what a replaced meter's step is measured, and executing every stated rule with each meter's own before-and-after files the wrong set.

Analyst test: a strong analyst who conforms every source and reads the IWA balance and the call correctly measures each replaced meter's under-registration as its consumption after replacement against the same quarters a year earlier, over-corrects the zones still read on old meters in 2025 and files the default path's Ends on set; taking billed consumption as delivered files a larger wrong set; only the step net of same-class customers not yet replaced, by meter age, files the golden set.

Estimand: the call's rules 3.1 to 3.4 (network_renewal_call_2027.pdf) file the population (the utility's sixteen metering zones), the outcome (each zone's 2025 infrastructure leakage index: current annual real losses from the IWA water balance over unavoidable annual real losses from the IWA formula), the window (calendar 2025), the unit (the index to one decimal, computed unrounded) and the comparison (4.0 or more is eligible); rule 3.3 files that customer metering inaccuracy is measured from the utility's meters in service and that manufacturers' curves, bench tests and default percentages are not accepted.

No decoy: nothing is planted to be caught: the bench-test records are the meter workshop's genuine tests at standard flows, shipped as a distractor and closed by rule 3.3; no memo, draft, earlier application or stakeholder figure ships; the 2025 summer is weather, recorded nowhere as a cause.

No certified replay: no certified or published figure is reproduced to recover the method; the meters' error is measured from the utility's own reads, and no shipped table reports any zone's index or real losses.

Lesson: an instrument being replaced shows its error only as a step across its replacement, and that step also carries whatever moved the measured quantity between the two windows; the error is read against units not yet replaced over the same periods and of the same kind, and a balance residual inherits every error left in its terms; no build on file measures an instrument's error from a staggered replacement or corrects a mass balance with it.

## Default path

1. Read the call: zones whose 2025 infrastructure leakage index is 4.0 or more are eligible; the index is current
   annual real losses over unavoidable annual real losses; real losses are system input less authorised
   consumption less apparent losses; metering inaccuracy is measured from meters in service.
2. Conform each zone's 2025 system input from its inlet meters less its transfer meters, SCADA gaps filled.
3. Conform 2025 billed metered consumption per zone from the billing reads (estimated reads trued up, the
   replacement work orders splitting the period), unbilled authorised use from the logs, unauthorised use at the
   guide's allowance.
4. Measure metering inaccuracy on the rollout: for each replaced meter, its consumption after replacement against
   the same quarters a year earlier on the old meter, the step fitted on meter age; apply it to 2025 consumption
   read on old meters.
5. Form real losses, the unavoidable real losses from mains length, connections, private pipe length and average
   pressure, and the index; list the zones at 4.0 or more.

Ends on: to be cut at stage 2 from the design prototype (fewer zones than the golden: the old-meter zones over-corrected)

Golden: to be cut at stage 2 from the design prototype

## Stump sentence

The default path measures each replaced meter's under-registration as its own step from the same quarters a year
earlier and files the Ends on set: the step carries 2025's rise in houses' demand into the meters' error, so every
zone still read on old meters in 2025 is over-corrected and the leakiest of them fall below 4.0; taking billed
consumption as delivered files a larger wrong set; only the step net of same-class customers whose meters were not
yet replaced, by meter age, files the golden set.

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
