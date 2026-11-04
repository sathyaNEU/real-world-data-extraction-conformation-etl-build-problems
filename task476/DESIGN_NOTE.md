# task476 design note: Ochre Flats Farming Company's water year 2026 extraction return and transfer purchase

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first. Architecture 3, a
re-root drawn 2026-11-04 after architecture 2 (a city gas utility's leak methane by district) was spent at the 11-01
re-check; architectures 1 and 2 are in the card's lineage with their shell, and architecture 2's shipped pack
(5a46ee5a) stays at the portal, pending, until this build replaces it at ship.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task476.json` (architecture v3), registered 2026-11-04T05:06:12Z;
  `guard.py check` WARN only (the old prompt's shell, which this build replaces; test.same_puzzle_older against
  task140 differentiated on the card). Window at the draw: task461 v2, task193 v3, task192 v4, so the strategies
  other, population_selection and grain_or_unit, the forums regulator_or_inspector, line_manager_or_team and
  operations_desk, the forcing events statutory_or_regulatory_filing, period_close and shift_or_daily_cycle, the
  organisation families logistics_or_3pl, utility_or_infrastructure and local_government, the roles
  operations_director, field_unit_lead and other, and the artifacts operations_log, monitoring_export and
  filed_standard were all off the table; emissions-inventory BLOCKs on pairing and subdomain. Nearest driver
  task244 at 0.09.
- **Seed:** ET33's number, re-rooted twice; nothing of ET33's world is kept. The objective stays.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data
  Extraction & Conformation (ETL). The ranch conforms the electric utility's two interval exports, two contractors'
  pump efficiency test reports, its water level loggers and its totalizer meter reads into the groundwater
  sustainability agency's extraction return, one row per well, and the call is the transfer water it must buy.
- **Shape:** 15, fields conformed to one schema: each well's method, its monthly and water-year acre-feet and its
  spring and fall 2026 static depths to water on the agency's template, with the purchase and the power charges in
  the memo.
- **Strategy:** decomposition_attribution. Each hour's metered energy is the product of the water the pump lifted and
  the head it lifted it against, divided by the plant's efficiency; the field's energy-based method attributes the
  whole of it to water at the head of the day the pump was tested, and the step splits each hour's energy between
  water and head by that hour's own pumping level. Decisive generator G1 (energy standing in for water at an
  exchange rate that moves), with G16 (the conversion chosen from the data's structure) and G19 (the agency's
  allocation, carryover and transfer blocks). Gate G etl_conformance.
- **World:** United States, a fictional subbasin in California's San Joaquin Valley. Ochre Flats Farming Company, a
  family-owned grower of pistachios and almonds, pumps its own wells above and below the regional clay and takes
  Alkali Slough Water District's canal water in wet years; the Sallow Plains Groundwater Sustainability Agency
  allocates groundwater per gross acre with a carryover, and extraction over what a grower has available must be
  covered by a recorded transfer before the true-up. Personas from `guard.py names --geo "United States" --seed
  476`: Melinda Walter (the ranch's water manager), Nicholas Wolf (managing partner), Tamara Larson (the agency's
  program manager, who signs the notice).
- **Forcing fact:** the agency's notice of 15 October 2026 sets the water year 2026 return due 30 November 2026 and
  the transfer deadline 15 December 2026; the ranch's partners sign any transfer purchase agreement before then. The
  call faces forward (a purchase still to make); its quantity is the closed water year 2026 (1 October 2025 to 30
  September 2026), retrospective because the true-up settles a closed year.
- **Forum and forcing event:** executive_team (the managing partners approve the purchase),
  purchase_order_or_contract (the transfer purchase agreement). Organisation agriculture_or_food_producer; role
  procurement_lead (the water manager buys the ranch's water). Context artifact register (the well register).
- **Data-native sentence:** Ochre Flats' deep wells draw from the confined aquifer below the clay, whose level swings
  a hundred feet through the year, deepest in August and September when the pump contractor makes its annual round
  and shallowest in late winter, while its upper wells sit in water that barely moves; a turbine pump's energy per
  acre-foot is set by the head it lifts against, so the kilowatt-hours per acre-foot each deep well's test measured
  at the year's deepest water overcharge every hour the pump ran on the higher spring and early-summer water.
- **The WHAT screen.** Population: every well on the ranch's parcels (the agency's notice lists them by its well ID).
  Outcome: the volume of groundwater each well pumped. Window: water year 2026, 1 October 2025 to 30 September 2026,
  local time. Unit: acre-feet. Comparison: the ranch's total against its allocation plus carryover, the excess
  covered by a transfer recorded in blocks of 10 acre-feet. The decisive step settles none of them: it is how an
  unmetered well's energy record converts to water.
- **Deliverables:** `wy2026_extraction_return.csv` (the agency's template: each well's method, monthly and
  water-year acre-feet and its spring and fall 2026 static depths to water) and `transfer_purchase_memo.docx` (the
  purchase for the partners, the ranch's total against what it had available, each well's power charge for April
  to September 2026).
- **Sources, one line each:**
  - The field's energy-based extraction estimate (power consumption coefficient, kilowatt-hours per acre-foot from a
    pump efficiency test, applied to the well's metered energy) used where wells are unmetered; here it is rung 0.
  - Pump efficiency test practice: a test reports standing and pumping levels, discharge pressure, total head, flow,
    input power, overall plant efficiency and kilowatt-hours per acre-foot (1.0241 times total head over efficiency)
    at the conditions of the day.
  - `dataset-generation/references/layer1-messiness.md`: two utility exports across a portal change (local
    prevailing time against UTC, kWh against Wh, renumbered accounts), two contractors' report layouts, vented and
    non-vented loggers, totalizer rollovers and a replaced meter.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): none converts an energy record to a volume at a
    state another system records; task452's first architecture (a sampled concentration carried across unsampled
    days) and task474 (activity-expanded counts) are the nearest abstractions, and neither has a physical law fixing
    the conversion with no free parameter.

## Survivor anatomy

Actor: the head each lower-aquifer pump lifted against in each hour it ran has no column in any file: it is a
relation between the utility's interval energy and the same hour's reading in the well's logger file, two systems on
two clocks, joined through the well register, against the pump test's head on its own day.

Link: the conversion is read by pairing every power interval with that hour's pumping level from the logger keyed by
its serial, a cross-system join no key offers (the exports are keyed by service agreement, renumbered at the April
2026 portal change, the loggers by serial, the tests by the contractor's own well names) and no sentence invites.

Reflex: the field's method for an unmetered well's extraction (its energy times the acre-feet per kilowatt-hour its
latest pump efficiency test measured) sits at rung 0 and files the ranch inside what it had available, with no
transfer to buy (the default path's Ends on).

Back-test: the textbook route validates: on the four metered upper-aquifer wells the energy-based estimate at each
well's own test agrees with the totalizer within about 2 per cent, because their water hardly moves, so a solver who
checks the method against the meters finds it confirmed.

Second use: every file the step reads is read for its own reason: the power exports carry every well's energy for
the return and the memo's power charges, the pump tests carry the kilowatt-hours per acre-foot the default path
uses, and the logger files and the register carry the static depths to water the agency's return asks for.

Shock: the movement the step recovers reads as ordinary: water year 2026's energy by well is in line with the wells'
sizes, no well is the pack's outlier on any statistic, and the step moves every lower-aquifer well by a similar
share, so no sort of the wells on a shipped figure isolates the correction.

Pins: the WHAT is filed in the agency's notice in its own genre (the population by well ID, the water year, the
acre-foot, the allocation, carryover and transfer blocks, a metered well's meter); no filed sentence names a head, a
pumping level, a conversion or a pump test for the volume, so deleting any filed sentence leaves the step where it
was.

## Default path

1. Read the well register, link each service agreement in both utility exports to its well (the April 2026
   renumbering through the register's prior and current account columns) and each pump test report to its well
   (the contractors' names and state well numbers through the register), keeping each pump's latest test.
2. Sum each well's water year 2026 energy, the old export's hourly kWh in local prevailing time and the new export's
   15-minute Wh in UTC, inside 1 October 2025 to 30 September 2026 local time.
3. Read the four metered wells' totalizers (rollovers, units and the June 2026 replacement) for their volumes.
4. Convert every unmetered well's energy at its latest test's kilowatt-hours per acre-foot (the field's energy-based
   method), checked against the metered wells, where it agrees within about 2 per cent.
5. Sum the ranch, set it against the allocation plus carryover in the agency's notice and buy the excess in blocks
   of 10 acre-feet.

Ends on: no transfer to buy (0 acre-feet), the ranch about 300 acre-feet inside what it had available.

Golden: buy about 390 acre-feet of transfer water, the lower-aquifer wells converted hour by hour at the head each
pump lifted against.

## Stump sentence

The default path converts each unmetered well's water year 2026 energy at its pump test's kilowatt-hours per
acre-foot, which the metered upper-aquifer wells confirm within about 2 per cent, and files no transfer to buy (0
acre-feet), because it never asks what head each hour's power lifted water against: the deep wells were tested at
the confined aquifer's August low and pumped most of their water on spring and early-summer levels 60 to 110 feet
higher, so each of their kilowatt-hours bought about a tenth more water than the test's rate gives.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science): the utility's two interval exports, two contractors' pump test reports, the ranch's logger files and its totalizer reads integrated through the well register into the agency's extraction return, a conformation serving Data Extraction & Conformation (ETL).

Domain test: General statistics, so the swap is of the method: the deciding quantity is a data-integration estimate, each unmetered lower-aquifer well's water year 2026 volume integrated from the utility's interval energy and the well's own logger record through its pump test, each interval's energy converted at that hour's total head (the test's head moved by the gap between the hour's pumping level and the test's) at the test's overall efficiency; replacing it with a single-source summary (the test's kilowatt-hours per acre-foot, run hours times the tested flow, an average over tests) files no purchase.

Swap: "how many servers must the data centre lease to cover the requests its racks served in 2026, from the racks' power and a benchmark's requests per kilowatt-hour" keeps a metered input converted to an output and loses the step's ground: no head a pump lifts against, no pumping level falling and recovering through the year in another system's record, no test taken at the aquifer's low, so the swapped task has no counterpart to the hours a deep pump lifted water 100 feet less than on its test day.

Layer 1: the utility's two exports across its April 2026 portal change (hourly kWh in local prevailing time, the fall-back hour twice and the spring-forward hour absent, against 15-minute Wh in UTC, service agreements renumbered), the contractors' two report layouts (gpm against acre-feet a day, total lift and head against pumping level, discharge psi and total dynamic head), three superseded 2023 reports on pumps replaced in 2024, vented loggers reporting depth below the measuring point against non-vented loggers reporting total pressure head that the barologger compensates, logger clocks on Pacific standard time all year, totalizer reads in different units with a rollover and a replaced meter, and the register's three naming schemes; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the call holds under every mishandling that leaves the conversion alone.

Layer 2: field_method, the field's own method done right: the choice that flips the call is converting each hour's energy at that hour's head rather than at the head of the test day, which the confined aquifer's seasonal swing makes the deciding term.

Decisive step: rebuilding each lower-aquifer well's volume hour by hour as the interval's kilowatt-hours times the test's overall efficiency over 1.0241 times that hour's total head, the head read from the well's logger as the test's total head plus the hour's pumping level less the test's, so the spring and early-summer hours, lifted 60 to 110 feet less than on the late-summer test day, buy about a tenth more water per kilowatt-hour.

Not semantics: every field, unit and definition read correctly (both exports' clocks and units, the renumbered accounts, both report layouts, the loggers' references and compensation, the totalizers, the notice's terms) still leaves the easy route converting each well's energy at its test's kilowatt-hours per acre-foot, a figure that is exactly what its column says (the test day's energy per acre-foot); the step is the physical inference that the rate moved with the head through the year, which no field states.

Not rule application: the notice files the population, outcome, window, unit and comparison, the meter for a metered well and the transfer blocks, and says only that an unmetered well reports the volume it pumped estimated from its records; no rule says how energy becomes water, so executing every filed rule files no purchase; the enumerated family (the test's rate 0, run hours times tested flow 0, an average of tests 0, the nearest test 0, scaling by the pumping-level ratio alone well over 1,000, the hour's total head about 390, the month's mean pumping level about 390) spreads 0 to over 1,000 acre-feet of purchase, the standing family (the conversion at the recorded head under every licensed convention of the fork table) spreads about 380 to 400, and the ruling-out is silent: no sentence names a head, a pumping level or a conversion.

Analyst test: a strong analyst who conforms both exports, links every account and report to its well, reads the meters right and converts each unmetered well's energy at its latest test's kilowatt-hours per acre-foot, checked within about 2 per cent on the metered wells, files the ranch about 300 acre-feet inside what it had available and buys no transfer (0 acre-feet, the default path's Ends on); one who uses run hours times tested flow files further inside; only the hour-by-hour conversion at the recorded head files the ranch over, buying about 390 acre-feet; checks.py runs each route on the clean truth.

Estimand: the agency's water year 2026 allocation and true-up notice (Sallow Plains GSA, 15 October 2026, sections 2 to 4): the population (every well on the ranch's parcels, listed by agency well ID), the outcome (the volume of groundwater each well pumped), the window (water year 2026, 1 October 2025 to 30 September 2026, local time), the unit (acre-feet) and the comparison (the ranch's total against its allocation plus carryover, any excess covered by a transfer recorded in blocks of 10 acre-feet), a metered well reporting its meter.

No decoy: nothing is planted: the utility exports, the pump test reports, the logger files, the meter reads, the register, the notice and the tariff are the producing systems' records; no memo, earlier return, draft or stakeholder figure states or ranks the ranch's water year 2026 extraction, and the agency's template ships blank.

No certified replay: no certified, filed or published water year 2026 extraction figure ships, and the method is not recovered by reproducing any figure; the pump tests are measurements on their own day, which both routes use.

Lesson: a pump's energy per acre-foot follows the head it lifts against, so where a well's water swings through the year its metered energy converts to water only at each hour's own head, read from the well's level record, never at the head of the day it was tested; no build on file converts an energy record to a volume at a state another system records.

## Tried and rejected

- 2026-10-20, at the draw: the seed's moves (overlapping periods, a GEOID match, point estimates) as the decisive step;
  each is a filed fact or a reading here and sits on a lower rung. A period-specific population weight for split
  tracts' children was screened and set aside: it is task474's driver (a coarse total split by a period-specific
  indicator), and for a pure split any common weight leaves the child's rate equal to the parent's.
- 2026-10-20, architecture 1 spent at stage 4 (judge pass 1 SEND_BACK, Gate H rule_application; reader B landed the
  call and all 140 tract figures in about two minutes): a split 2020 tract's 2014 to 2018 rate rebuilt from the 2010
  block groups that tile it. The rebuild is exact arithmetic on published estimates, so once guidelines 3.2 files the
  estimand as the rate for the area the 2020 tract covers, the block-group table and the block relationship file
  leave only execution; without the sentence the unit is unfiled. No position holds both gates (the WHAT screen's
  own case), so the number re-roots. Ask A's reopened cases were also read straight off the event history, and the
  prompt's "median" contradicted guidelines 4.2's average.
- 2026-10-20, architecture 2 stage 4 readers 1 and 2 (pack 543b59b9): both missed the call on the default path
  (the midpoint start: Ashby, Elmwood and Ivers) and every repair-cost figure, and both took all 12 interruption
  figures by joining each ticket's address to its meters. That device kept as a hazard; Ask B's primary re-sited to
  the shared service lines. Reader 1 also read "local" as Eastern time: guidelines 2.2 now names Central time.
- 2026-10-20, architecture 2 stage 4 reader 3 (pack 5a46ee5a, shipped): missed the call (the midpoint start) and all
  24 ask figures.
- 2026-11-01, architecture 2 spent at the re-check's stage 4 (judge pass 4 NOT_DETERMINISTIC, SEND_BACK, Gate C/E
  underspecified_objective; Gate G method_or_model_selection, Gate H analytical): guidelines 2.2 file a start only for
  the called leaks, and a surveyed leak's start at the find, the previous survey, the midpoint or the seasonal
  expectation designates 0, 12, 3 or 5 districts with nothing filed ruling out the midpoint; the sentence that would
  close the fork names the decisive step, so the fork is the stump and no pin repairs it. The re-check's free-gate
  repair (the extract notes out of the pack, leak.py sweeps 1 and 12 LEAK; "our 12 districts" out of the prompt;
  survivor anatomy written, precut 61 checks, 0 WARN) went green on every free gate with no graded figure moved and
  is not shipped; the shipped pack (5a46ee5a) stays at the portal, pending.
- 2026-11-04, architecture 3 draw (the re-root after architecture 2's 11-01 SEND_BACK, run as a background agent of
  the orchestrating session, under its stop rule of forty screens across five task types): 55 candidates screened across
  the six task types that serve ETL, each with a default path ending wrong, the swap test, the survivor anatomy and the
  bin test on paper, the strongest priced in code; none clears guard.py check and the three rules together, so no card
  is registered and nothing is cut. The window at the draw is task276, task461 v2 and task193: emissions-inventory
  BLOCKs on ban.pairing and ban.subdomain against task461 v2, and the strategies binding_constraint, other and
  population_selection are banned against the three; probe cards on the other five cells clear every axis, so what
  refuses them is the mechanism, line by line below (S3.1 to S3.52, three lines holding two or more screens). Read beside task464 architecture 5's cell map
  (10-27), task479's screens 1 to 16 and task461 v2's screens 1 to 12, none of which is re-screened here.
- S3.1, the strongest, emissions-inventory, written in full. Default path: each 2026 load at a terminal's uncontrolled
  distillate bays charged by the loading-loss equation at the loaded product's own true vapour pressure (submerged
  loading, dedicated normal service), about 0.0165 lb per 1,000 gal, which files every rack far under a 10-tonne
  control threshold. Golden: a compartment whose previous load was petrol delivered through a Stage I station's vapour
  balance returns holding saturated petrol vapour, so diesel loaded into it at an uncontrolled bay pushes out about 9
  lb per 1,000 gal; the switch-loaded compartments read from each trailer's own load sequence across the main rack's
  automation export and the distillate rack's older meter system. Swap: holds (no vapour space, displacement or vapour
  balance in another field's nouns). Anatomy: Actor, Link (two systems, trailer identifiers crosswalked), Reflex,
  Back-test (the vapour combustion unit's test confirms saturation at the petrol bays), Second use, Shock and Pins all hold
  on paper. Bin: priced in proto_switch.py (session scratchpad, three seeds, six terminals): rung 0 files 0.2 to 0.8
  tonnes per rack, the compartment-history golden 10 to 125, the trailer-level shortcuts (any petrol in 2026; any
  petrol on the previous load) 2.0 and 1.6 times the golden. Dead the same hour, before any card: task461 v2 registered
  this mechanism at 03:18Z (its driver: a transfer into a container pushes out whatever the container held, so the
  release is set by the container's previous use), so the step is that build's, its honest strategy (other) is banned
  against it, and the cell is barred besides.
- S3.2, emissions-inventory, an anaerobic digester's gas holder venting at its relief valve only once a CHP outage has
  filled the holder's free volume (storage with memory): without a holder level log or a production meter the free
  volume at each outage is unidentified (Gate B); with either, the venting is one subtraction of metered flows (the
  linear death) or a row predicate on the level column (readability test 2); and its abstraction sits beside task479
  v7's (gas above a device's capacity leaving untreated).
- S3.3, emissions-inventory, prescribed and savanna fire emissions with fuel load by years since the last fire on each
  piece of ground: the field's savanna method already reads fuel age from the fire scar history (the golden is the
  method), and a within-year reburn needs a fuel load at age zero no table files (Gate B).
- S3.4, emissions-inventory, cold-start excess read from each vehicle's gap since its previous trip: the soak curve is a
  filed MOVES or COPERT function (rule application) and the gap is a sort and a difference (readable).
- S3.5, emissions-inventory, haul-road dust control decaying with time since the water truck's last pass: AP-42
  13.2.2's watering equation is filed and linear in the interval and the traffic (the linear death), and the water
  truck's log against the dust plan is record against operation alone (G3, a lone defect flip).
- S3.6, emissions-inventory, at-berth auxiliary engines on shore power, with the ship's load above the connection's
  rating met by its own engines: the plug-in log is the field's input (a header-found join), and the capped variant is
  task479 v7's driver; S3.7, the same at airport stands with ground power and air: the same two deaths.
- S3.8, emissions-inventory, portable equipment moved between permitted sites, its hours attributed through the
  transport log: attribution at a transition (G4: a sub-period error cannot carry an annual figure) under a filed rule.
- S3.9, emissions-inventory, a storage tank switched from diesel to petrol service, its register naming only the current
  product: a stored label before a silent switch, task479's ask device D2 and data semantics as a main call.
- S3.10, emissions-inventory, a batch vessel's purge venting the solvent of the previous step's wash: task479's world
  (a closed-vent batch plant) and the EIIP vapour equations filed (rule application).
- S3.11, emissions-inventory, refinery fuel gas carbon content set by which units feed the header at the hour:
  task479 v7's abstraction (a shared stream's property set by coincident contributors).
- S3.12, emissions-inventory, vapour balancing between tanks, a filling tank's vapour taken up by an emptying tank only
  when the two coincide: the coincidence family (task479 v7).
- S3.13, emissions-inventory, leaks on delay of repair venting until the turnaround: architecture 2's world (leaks) and
  the protocol's leak duration rule.
- S3.14, emissions-inventory, storage pile wind erosion per disturbance period: AP-42 13.2.5 files the per-disturbance
  method (the library test).
- S3.15, emissions-inventory, truck vapour tightness lapsed at the load date: an as-of join on a shipped key (readable)
  under a filed capture factor (rule application).
- S3.16, emissions-inventory, a recirculating scrubber's removal falling with the solvent the liquid has absorbed since
  its last change-out: the efficiency against loading is a fitted curve (Gate C) or a vendor curve that names the
  quantity (readability test 1), task479's screen 16 fork.
- S3.17, emissions-inventory, a feed additive's methane reduction lost on the days the premix ran out between
  deliveries: the swap fails (a stock-out of any input reads the same) and the ration log against deliveries is G3
  alone.
- S3.18, emissions-inventory, a marine loading's displaced vapour by the vessel's arrival tank condition read from its
  previous voyage: AP-42 tabulates loading factors by arrival condition (filed) and the cargo inspector's report
  carries the condition (a column).
- S3.19, emissions-inventory, an anaerobic lagoon's volatile solids carried month to month and reset at each emptying:
  the monthly conversion is a filed rate model and the emptying dates against the nominal plan are G3 alone.
- S3.20, emissions-inventory, a hydropower reservoir's degassing at the turbines by intake depth: the dissolved methane
  profile is sampled monthly (a model of the measurement).
- S3.21, emissions-inventory, a coal pile's reclaim order setting the fired coal's carbon against the as-delivered
  analyses: the sampling basis is a filed monitoring rule (rule application) and a lag that moves only the year-end
  stock.
- S3.22, emissions-inventory, a crematorium's mercury by the decedents' dental cohort: a composition one survey table
  hands over (task482 architecture 8's screen).
- S3.23, payment-claims, an anaesthesiologist directing more than four concurrent cases, so the cases fall to
  supervision payment: a stated rule over a hard construction (rule application).
- S3.24, payment-claims, non-emergency transport trips shared in one vehicle: a filed shared-ride rate (rule) and a
  self-join on vehicle and time (readable).
- S3.25, payment-claims, a hospice's aggregate cap under the proportional method across providers: a filed regulation
  (rule application).
- S3.26, payment-claims, single-dose vial wastage rebuilt from doses and vial sizes against the reported discard lines:
  the refund basis is the filed discard reporting (rule), and finding under-reporting is anomaly detection.
- S3.27, payment-claims, a family's out-of-pocket maximum across the medical and pharmacy vendors' accumulators: rule
  application over an identity link.
- S3.28, payment-claims, short stays discharged home with home health inside three days paid as transfers: a filed
  transfer policy and a key join.
- S3.29, payment-claims, specialty drugs dispensed by the pharmacy and billed again under the medical benefit: duplicate
  detection (a planted defect as the call, and anomaly detection ground).
- S3.30, payment-claims, retroactive re-enrolment claims after the Medicaid unwinding: the completion family (task451,
  task479 v5).
- S3.31, payment-claims, charge compression under a department's cost-to-charge ratio: the swap fails (any department
  markup ratio reads the same).
- S3.32, payment-claims, global maternity care billed at delivery, so prenatal care rendered in 2026 is unbilled for
  continuing pregnancies: task482 v14's episodes recorded only at their end.
- S3.33, payment-claims, rebate accruals at the old market-share tier after a generic launch: the contract's tier table
  (rule) over a group-by.
- S3.34, payment-claims, network adequacy against the locations providers actually bill from: the swap fails (a store
  locator reads the same) and the directory against claims is G3 alone.
- S3.35, payment-claims, a claims case definition's positive predictive value by setting, recovered from the treatment
  fills only true cases produce: task241 v2's driver in claims nouns (the abstraction test).
- S3.36, payment-claims, auto-refill shipments inflating adherence after a therapy switch: the adherence measure's
  specification is filed (rule application) and the measure is pharmacology ground.
- S3.37, payment-claims, out-of-network claims in independent dispute resolution at year end: decided awards not yet
  paid are an inner join (rule application) and pending outcomes a fitted win rate (Gate C).
- S3.38, census-register, a communal establishment's register count capped at its licensed capacity: a plausibility
  edit (rule application), and the lesser-of prints the capacity on every bound row.
- S3.39, census-register, addresses geocoded to postcode centroids placed in the wrong small area: allocation across
  areas is task486's driver, and identical coordinates are readable.
- S3.40, census-register, dwellings read as vacant from low grid import when rooftop solar covers the load: the signs of
  life family (task471 architecture 4, task464 architecture 5's three arms) with the solar register an inner join.
- S3.41, census-register, cattle on the tracing system never reported dead, caught by the herd's whole-herd test: the
  exact arm (a second register confirming every unit is an inner join, rule application).
- S3.42, census-register, a dwelling's vacancy observed only at the annual canvass taken in each ward's own month:
  architecture 2's driver in census nouns (test.own_lineage and the abstraction).
- S3.43, census-register, an address survey's unknown-eligibility cases that are vacant: the signs of life family, and
  the eligibility share is a filed response-rate convention.
- S3.44, official time-series production, seasonally closed establishments imputed as open non-respondents in the
  accommodation statistics: the pincer; the closure is confirmed by a record (a nil tourist-tax return, an inner join,
  rule application) or inferred from the unit's own past closures, which a judge reads as a competing imputation that
  only a sentence naming the step closes (the fork is the stump), and the register's establishment type is a proxy.
- S3.45, official time-series production, product relaunches under new barcodes in a scanner-data index: identity
  resolution may not decide, and the field's relaunch linking is its own method.
- S3.46, official time-series production, job vacancies as a stock on the reference date against postings in the
  month: re-timing (task123).
- S3.47, official time-series production, electricity consumption gross of rooftop self-consumption: a modelled yield
  and self-consumption ratio (a model of the measurement).
- S3.48, official time-series production, rail journeys per season ticket re-estimated from gated stations' taps: the
  audit arm (a selected subsample carried to the ungated stations, its interval wider than the step).
- S3.49, official time-series production, single against double deflation of a volume index after an input price
  shock: the field's textbook method is the golden (1.1b); S3.50, a rent index as a stock or a flow: a WHAT fork; S3.51,
  outlet substitution in a matched-outlet price index: a contested method (Gate C).
- S3.52, item-response-theory-test-equating and data-integration, four screens: forms assigned by test centre rather
  than spiralled (the random-groups precondition) is card 3's method and the cell's conversion closure; testlet local
  dependence is a model fork; instructional-weeks norms are a conversion; namesakes over-merged by a master patient
  index, split where their stays overlap, is linkage error propagation (task449, task456, task468, task473) with a
  partial correction landing further away (law L3).
- The three strongest, for the orchestrating session: S3.1 (blocked by task461 v2's registration of the same driver and
  by the window), S3.44 (blocked by the ETL pincer and the fork-is-the-stump test), S3.35 (blocked by the abstraction
  test against task241 v2). What the draw leaves: the ETL ground outside emissions-inventory is closed on mechanism by
  this pass and the earlier maps; emissions-inventory reopens to a new physical mechanism (neither capacity, task479 v7,
  nor a container's previous use, task461 v2) once task461 v2 leaves the three-build window.
- 2026-11-04, S3.44 re-tested on the orchestrating session's ruling (C2 confirm and C1 converge priced in
  proto_s344.py, session scratchpad, four seeds, eight regions, six rival corrections): dead. With closure calendars
  stable year to year, the field's own seasonality-aware imputation (same month of last year's final times the
  stratum's year-on-year ratio, R0b) lands within 0.6 to 1.7 per cent of the truth and agrees with both closure-aware
  corrections (last winter's status, a multi-winter pattern), so the easy route sits inside the golden family and two
  corrections survive; with calendars shifting (establishments starting or stopping winter closure, a shock closing
  more this winter) every family misses by 10 to 36 per cent on its worst region and the back-test's best basis (a
  modelled closure probability, 8 to 13 per cent off) selects nothing with margin, because the deciding configuration
  (this winter's new closures) is out of sample. No C2 criterion or C1 world serves both horns.
- 2026-11-04, after the S3.44 re-test, on the orchestrating session's second ruling (move the world; any ETL task type,
  house domains accepted, a fresh physical or behavioural mechanism): the window moved to task461 v2, task193 v3 and
  task192 v4 at 04:24Z, freeing binding_constraint and banning grain_or_unit. Seven more screens died before the draw:
- S3.53, census-register, dual-system estimates short for young men because the census and the coverage survey miss
  the same men, corrected by the sex ratio that birth and migration records fix: task471 v5's driver (the abstraction
  test).
- S3.54, item-response-theory-test-equating, rapid guesses in a low-stakes interim test scored as wrong answers: the
  estimand (achievement) is the scoring model's own construct, so the sentence closing a judge's fork would say that
  answers given without engagement are not evidence (the fork is the stump), and the rapid-guess threshold is a knob.
- S3.55, data-integration in an accounting world, a subsidiary's income translated at the year's average rate across a
  mid-year devaluation: the standard's own rule (rates at the transaction dates) is the golden, so reading it flips
  the call (data semantics and rule application at once).
- S3.56, data-integration in a fleet world, off-road distance for a road-user charge refund from GPS tracks that
  under-read winding forest roads: two road-type factors fitted from the hubodometer totals is an estimation grouping
  (1.1c).
- S3.57, payment-claims, grace-period members retro-terminated after the eligibility snapshot: the premium ledger
  makes it an inner join under a filed grace rule, and without it a forecast of who pays (the pincer).
- S3.58, data-integration in a contact-centre world, offered calls that include the attempts the carrier blocked when
  every trunk was busy: the population (the WHAT screen).
- S3.59, data-integration in a facilities world, office occupancy from each room's carbon dioxide balance: a model of
  the measurement with free generation and ventilation rates (the pincer's sampled arm).
- The draw that followed (energy-based groundwater extraction converted at each hour's pumping head, S3.60) is the
  `## Draw` above; priced first in proto_lift.py (session scratchpad, six seeds): with each deep well tested once at
  the confined aquifer's late-summer low, the test's rate files the ranch 5 to 6 per cent short of the truth (the deep
  wells 8 to 9 per cent), run hours times tested flow 7 to 8 per cent, an average or the nearest of the tests about 5,
  and every conversion at the recorded head within about 1 per cent, the family agreeing to about 1 acre-foot on the
  ranch; with the allocation set 2.5 per cent under the golden, every easy route buys nothing and the golden family
  buys 380 to 400 acre-feet on every seed. A first cut with half the deep wells also tested in an earlier spring
  priced the averaging route inside the golden (the spring and summer tests bracket the season), so the pack ships
  one current test per pump and the superseded reports only for pumps replaced since.
