# task468 design note: Glenbrae Water's 2026 trade waste COD masses, converted from TOC on the samples' own chloride

Status lives in `pipeline.json`; this note holds the design of architecture 6, drawn on 2026-11-01 as a batch 1
re-root. Read `## Tried and rejected` first: architectures 1 to 4 (transit nominations, specialty pharmacy staffing, a
Medicaid plan's linkage-corrected mortality bonus) and architecture 5 (Harrowmere's repeat-sales pressured wards, sent
back by its stage 4 judge) are spent. Nothing of their worlds is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json`, architecture v6, registered 2026-11-01T01:02:25Z after a
  pull; `guard.py check` PASS on the filed card. The first filings were refused on the window and redrawn honestly:
  shape 10 (task231), pattern G4 (task146), G14 and the statutory filing (task445 v3, registered minutes earlier),
  purchase order or contract (task145), G16 and G6 (same-puzzle and same-driver records); architecture 5 and the
  earlier four are in the card's lineage.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory (serves ETL and DD) / Data Extraction &
  Conformation (ETL). Healthcare delivery and survey research are spent for this slot; education's equating cell
  carries task445 v3 (registered this hour) and three in-cell builds. The inventory is a utility's releases to sewer:
  each trade waste customer's mass of chemical oxygen demand discharged in 2026, conformed from two laboratory
  systems, hourly flow telemetry and the field job log.
- **The ETL move:** conform a year of measurements made on two bases onto the agreement's reference basis. From
  2 February 2026 the laboratory reports total organic carbon in place of dichromate COD; the policy makes the COD of
  a TOC sample the COD the reference method would have reported, estimated from the samples tested both ways in the
  October to December 2025 parallel run.
- **World:** Glenbrae Water, a fictional regional water and sewerage utility in south-east Queensland, its trade
  waste unit and its laboratory; its industrial customers, among them Coolabah Olives (an olive and pickle packer),
  Tallowood Tannery, Mt Edwin Cheese, Glenbrae Meats (an abattoir), Riverbend Poultry and Sunvale Dairy Ingredients.
- **Furniture:** forum customer_or_counterparty (the review notices go to the customers), forcing event
  audit_or_inspection (the state regulator's audit of the trade waste programme in March 2027), organisation
  utility_or_infrastructure; none repeats the last three builds.
- **Personas** (`guard.py names --geo au --seed 468`): Erik Marks, Trade Waste Manager; Mitchell Boyd, Laboratory
  Manager; Brent Fisher, Field Services Coordinator (the first draw's Diane sat in an older build and was redrawn).
- **Retrospective quantity, forward call:** the agreement reviews and the regulator's audit fall in 2027; the test
  reads the closed 2026 discharge year, as the policy files it.

- **Shape other (a designation over a scorecard):** each customer's verdict against its limit (12), the set (1), the
  chart's parts (the shares, the limit line, the exceeders marked: 3), the files (2), and the two asks (16 tankered
  waste cells, 12 suspended solids masses).
- **Data-native sentence:** Coolabah Olives brines its fruit in salt and Tallowood Tannery salts its hides, so their
  effluent carries five to twelve grams of chloride a litre, which the dichromate COD test oxidises with the carbon
  and the TOC analyser never sees; Mt Edwin Cheese started recovering its whey brine in May 2026 and Tallowood took
  salted hides from a new supplier from March, so their chloride is not what their 2025 parallel samples carried.
- **Abstraction sentence (tested against every approved build):** a quantity reported on a new measurement basis is
  converted to the reference basis through the samples both bases measured, but the reference basis also reads a
  constituent the new basis cannot see, at levels that differ between senders and that moved for some of them after
  the overlap, so only a conversion carrying each sample's own level of the constituent places every sender.

## Survivor anatomy

Actor: the deciding property, how much of each 2026 sample's dichromate COD is chloride's demand, has no column in any file; LabWare reports TOC and chloride side by side, the policy names no constituent, and the property exists only as a relation the parallel samples carry between COD, TOC and chloride.
Link: no key or sentence ties chloride to the conversion: the policy's section 5 asks for the COD the reference method would have read, estimated from the samples tested both ways, and chloride sits in both laboratory exports for its own reason (every compliance sample carries it), with no document naming it beside COD or TOC.
Reflex: the field's method for a TOC to COD bridge is a COD to TOC ratio, pooled or, better practice, each site's own ratio from its parallel samples (the site-specific correlation laboratories issue); the pooled ratio and the pooled regression file Glenbrae Meats, Riverbend Poultry and Sunvale Dairy, each customer's own ratio files Coolabah Olives, Mt Edwin Cheese, Glenbrae Meats and Riverbend Poultry.
Back-test: the site-specific ratio validates on the parallel run itself: each customer's own ratio reproduces its own October to December 2025 COD within its method noise, so nothing in the overlap refutes it; only the 2026 chloride, which moved for Mt Edwin and Tallowood, shows it no longer holds.
Second use: every file the decisive step reads sits in the pack for its own reason: the legacy LIMS export carries the January COD and the parallel run the policy names, LabWare carries the TOC and the suspended solids the second ask needs, and deleting the decisive step leaves both in the pack.
Shock: the customers whose verdict the decisive step moves are not the largest dischargers (Glenbrae Meats and Sunvale Dairy discharge more), Mt Edwin's 2026 COD to TOC ratio falls from 4.6 to about 3.3, and the golden set is not the top of any one-column sort (COD per kilolitre, TOC mass, chloride level or volume; asserted in checks.py).
Pins: the WHAT sits in the policy (the calendar year in Queensland time, both meters across an exchange, the volume-weighted mass, duplicates out, re-issued results replacing, half the reporting limit, the COD the reference method would have read estimated from the samples tested both ways, a limit exceeded when the mass is greater); no filed sentence names chloride, an interference, a factor or a model.

## Default path

1. Conform the two laboratory exports (the crosswalk, LabWare's UTC to Queensland time, duplicates out, re-issued results in) and the flow telemetry (both meters across each exchange, the job log's final and opening reads).
2. Convert each 2026 TOC sample to COD with each customer's own COD to TOC ratio from its October to December 2025 parallel samples (the site-specific correlation).
3. Apply the policy's mass formula: the year's volume times the volume-weighted mean COD of the year's samples, January on the measured COD.
4. Compare each customer's mass with its agreement's limit.

Ends on: Coolabah Olives, Mt Edwin Cheese, Glenbrae Meats and Riverbend Poultry over their limits (Tallowood Tannery under)
Golden: Coolabah Olives, Tallowood Tannery, Glenbrae Meats and Riverbend Poultry over their limits (Mt Edwin Cheese under)

## Stump sentence

The default path conforms both laboratory systems and the meters, converts each 2026 TOC result to COD with each customer's own COD to TOC ratio from its parallel samples and files Coolabah Olives, Mt Edwin Cheese, Glenbrae Meats and Riverbend Poultry; the step that lands it there is taking a customer's 2025 ratio as its conversion, when the dichromate test also oxidises the chloride brine effluents carry and TOC never sees, Mt Edwin cut its chloride with brine recovery in May 2026 and Tallowood's rose with salted hides from March, so with COD estimated on each sample's own TOC and chloride Tallowood is over its limit and Mt Edwin under.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences), which serves ETL: a utility's releases to sewer conformed from two laboratory systems, hourly meter telemetry across three meter exchanges and a field job log onto the agreements' reference basis.
Domain test: the quantity that decides is each customer's mass of chemical oxygen demand discharged in 2026 on the dichromate reference method, the trade waste chemist's own load, and its conversion from TOC turns on how the dichromate test responds to chloride, which a water chemist knows and a reader of the files must find in the parallel samples.
Swap: put hospitals' bed-days or a utility's megawatt-hours in place of effluent and there is no oxidant demand, no interfering ion, no parallel run of two methods and no conversion to carry; the task does not survive the swap.
Layer 1: two laboratory exports in different layouts, codes and clocks (local before the migration, UTC after), a site code crosswalk, quality-control duplicates and re-issued results under suffixed identifiers, suspended solids below the reporting limit, hourly cumulative registers across three meter exchanges whose final and opening reads live only in the field job log, limits in tonnes for some agreements and kilograms for others, a receival log and the state's manifests in two systems' keys; each comes from the system that keeps it and every careful handling of it leaves the call.
Layer 2: estimation_fit, a method bridge validated on its overlap: the reference method's reading carries a component the new method cannot see, so the conversion is a model of the reference reading on the new reading and the interfering constituent, fitted on the parallel samples and carried to each 2026 sample's own chloride.
Decisive step: estimating each 2026 sample's dichromate COD from its own TOC and chloride through a regression on the October to December 2025 parallel samples, instead of a ratio per customer or for all.
Not semantics: every field, code and unit read correctly still leaves the ratio routes, because no field marks chloride as part of COD; the residuals of any TOC-only conversion track chloride (correlation 0.98 on the parallel samples, asserted) and that relation exists only across the three columns.
Not rule application: no filed rule names chloride, a factor or a model, so executing the policy on any defensible conversion runs; the enumerated family (a pooled ratio, a pooled regression on TOC, each customer's own ratio by sum or median, each customer's own regression, the chloride regression with or without a constant or weighted by the inverse square) files three answers: the pooled routes' three customers, the per-customer routes' four with Mt Edwin, and the golden four with Tallowood; the standing family (the chloride members) agrees on the golden four with every customer at least 6.4 per cent from its limit, and the ruling-out is done by the parallel samples' residuals and the 2026 chloride.
Analyst test: a strong analyst who conforms both laboratory systems and the meters, applies every policy rule and converts with each customer's own parallel-run ratio files Coolabah, Mt Edwin, Glenbrae Meats and Riverbend; every field is read and every rule executed, and the call is wrong because Mt Edwin's and Tallowood's 2026 chloride is not what their 2025 ratios carried.
Estimand: glw_trade_waste_policy_v4.pdf sections 2 to 6: population, every customer with an agreement in force for 2026; outcome, the mass of COD on the dichromate reference method discharged in the year; window, the 2026 calendar year in Queensland time; unit, the customer; comparison, greater than the agreement's annual limit.
No decoy: nothing is planted to be caught: no memo, factor or published conversion argues any route; the brine customers' chloride is their own process's, recorded on every sample, and the changes are ordinary process changes the samples show.
No certified replay: no certified or published 2026 COD mass or conversion ships; the laboratory's notice states only that both methods ran in the parallel period.
Lesson: a method bridge validated only on its overlap carries every constituent the reference method reads; a model that gets this right learns to ask what the old reading responds to besides the thing the new one measures, and whether that has moved since the overlap, before trusting a ratio carried forward.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 a pooled ratio or regression on TOC | section 5 licenses an estimate | COD and TOC in the parallel rows | a conversion factor | none | runs it | one ratio | none | readable |
| 2 each customer's own ratio from its parallel samples | section 5 | the same rows by site | the site-specific correlation | each ratio reproduces its own parallel run | runs it | one ratio per site | none | readable |
| 3 (decisive) COD on each sample's own TOC and chloride | none names chloride | chloride sits in another column with no stated role | not the ratio reflex | no file states an interference | no battery item | the 2026 chloride carried sample by sample | the parallel run, kept for its own reason | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the COD the reference method would have reported | estimated on each sample's TOC and chloride | a ratio per customer or for all | different sets (the ladder) | the parallel samples' residuals (C4); same call across the chloride family (C2) |
| SF2 | the agreement year | the calendar year in Queensland time | UTC | same call (asserted) | policy section 2 |
| SF3 | an exchanged meter | both meters, the job log's final and opening reads | the register's meter only | not computable: the installed meter has no reading before its exchange (asserted) | policy section 3 |
| SF4 | the mass | volume times the volume-weighted mean | the unweighted mean | same call (asserted) | policy section 4 |
| SF5 | duplicates and re-issues | duplicates out, re-issues replace | kept | same call (asserted) | policy section 4 and the laboratory notice |
| SF6 | below the reporting limit | half the limit | the limit or zero | same call (no COD rides it) | policy section 4 |
| SF7 | January 2026 | the measured COD | converted from TOC | no TOC in January | the laboratory notice |
| SF8 | the limit's unit | tonnes or kilograms as the register states | all tonnes | same call (asserted) | the register's unit column |
| SF9 | exceeded | greater than the limit | at or over | no customer within 6 per cent | policy section 6 |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 1 | a pooled COD to TOC ratio or regression | Glenbrae Meats, Riverbend Poultry, Sunvale Dairy | the brine customers' parallel samples sit far off any TOC-only line |
| 2 | each customer's own parallel-run ratio (sum, median or regression) | Coolabah, Mt Edwin, Glenbrae Meats, Riverbend | Mt Edwin's and Tallowood's 2026 chloride is not their 2025 chloride |
| 3 (decisive) | COD on each sample's own TOC and chloride, fitted on the parallel run | Coolabah, Tallowood, Glenbrae Meats, Riverbend | the golden |

- **Margins on the cut pack** (asserted in checks.py): on the golden route every customer sits at least 6.5 per cent
  from its limit (Sunvale Dairy the nearest, under); the chloride family members (no constant, inverse-square
  weights) keep at least 6.4 per cent.
- **No free parameter.** The decisive model has no knob: the chloride term enters linearly, its coefficient (0.23
  mg/L of COD per mg/L of chloride) is fitted, and every family member files the same set.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every customer with an agreement in force for 2026 | the register |
| 2 Unit of account | the customer | policy section 6 |
| 3 Attribution window | samples and discharge by local date | policy section 2 |
| 4 As-of dating | the exports as issued in January 2027 | the files' dates |
| 5 Version basis | a re-issued result replaces the earlier one | policy section 4 (SF5) |
| 6 Denominator | the year's volume-weighted sample volume | policy section 4 (SF4) |
| 7 Weighting | each sample by its day's volume | policy section 4 |
| 8 Window length | the calendar year | policy section 2 |
| 9 Boundary inclusivity | greater than the limit | policy section 6 (SF9) |
| 10 Rounding path | masses unrounded against the limit; volumes to the kilolitre, suspended solids to 0.1 t | the prompt |
| 11 Tie-break | none needed | no customer within 6 per cent |
| 12 Maturity and censoring | the 2026 results all authorised by the exports | the exports |
| 13 Order of operations | conform, convert, weight, compare | C1 |
| 14 Row order | file order | none needed |
| 15 Duplicate resolution | duplicates do not report the sample | policy section 4 (SF5) |
| 16 Identity normalisation | legacy codes and points through the crosswalk | the crosswalk |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | mg/L, kL, tonnes and kilograms | the files (SF8) |
| 19 Code and status semantics | -D and -R suffixes, the less-than flag | the laboratory notice |
| 20 Integerisation | none on the call | not applicable |
| 21 Clause scope | section 5 governs every TOC sample | policy section 5 |
| 22 Forward window contents | the 2027 reviews follow the 2026 verdicts | policy section 6 |

## Literal reader

Executing the policy word for word gives each customer's mass of COD on the dichromate reference method for the 2026
calendar year in Queensland time, from both meters across an exchange and the volume-weighted mean of the year's
compliance samples, with each TOC sample's COD the COD the reference method would have read, estimated from the
samples tested both ways; no file states how that estimate is formed, so every literal reading has to fit it, and
every fit that carries each sample's chloride files Coolabah, Tallowood, Glenbrae Meats and Riverbend, while a ratio
per customer or for all (an easy estimate of the same literal quantity, not a reading of a sentence) files another set.

## Oracles

- The parallel run ties every route on its own samples within method noise except the pooled ones on the brine
  customers; it refutes the pooled routes and not the per-customer ones.
- January's measured COD ties every route (no conversion).
- none ties only under the golden.

## Ask sheet

Two asks in the figures workbook, each sited on rows the call never reads, each with a primary device that only a
reconstruction across two systems finds. Figures are the generator's (`generator/figures.json`, `ask_a`, `ask_b`);
deltas are asserted in `checks.py` (C6 to C10).

**Ask A, the volume of each kind of tankered liquid waste the treatment plant received in each quarter of 2026 (16
figures).**
- H18 home: the annual return reports the liquid waste the plant received beside the trade waste customers.
- Files and columns: the receival station's log (docket, received, truck, transporter, volume, status) and the state
  waste tracking manifests (manifest, waste code, receival docket).
- Primary (D6, an event recorded on two lines that one record covers): when the pit's high-level alarm stops a
  discharge the driver finishes the load in a second pass minutes later under a second docket, and the manifest
  carries only the first; the waste code of a second pass is read from the same truck's pass before it, an identity
  no field states.
- Hazards: dockets of loads rejected at the gate; manifests collected the day before receival.
- Pin test: the sentence pins the waste, the quarter and "received"; the device sits in which dockets are one load.

**Ask B, the mass of suspended solids each customer discharged in 2026 (12 figures).**
- H18 home: the suspended solids line of the same return.
- Files and columns: both laboratory exports, the inspections log, the meters.
- Primary (D4, a population boundary evidenced in another file): trade waste officers take grab samples at their
  inspection visits and LabWare registers them in the same series at the same points; they carry suspended solids and
  pH only, and the policy's mass reads the compliance composites, so the grabs are found by the analytes they lack and
  the inspections log's visits, neither enough alone.
- Hazards: quality-control duplicates and re-issued results (filed); results below the reporting limit.
- Pin test: the sentence pins the customer, the year and the mass; the device sits in which samples are compliance
  samples.

**Separation (asserted, C10):** no grab carries COD, TOC or chloride, so no device row enters the call's population;
the receival log and the manifests are not read by the call.

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at rung 2) | Verdict |
|---|---|---|---|
| A, 16 cells | joins dockets to manifests and drops the unmatched: 0 of 16 kept | the same join: 0 of 16 | miss |
| B, 12 customers | every LabWare sample of the year a compliance sample: 0 of 12 kept | the same, duplicates kept: 0 of 12 | miss |

The full includer (second passes given their truck's preceding code, the grabs set aside) keeps 28 of 28; it is a
stress row, not the gate.

Pair ceiling: 28.5 (the cracker on the call at 45.0, the mirror off it at 12.0, keeping 0 and 0 of 28 ask figures).
Mirror leakage: 0.0 per cent of the ask weight.
Measured by: generator/ceiling.py (run on the cut pack)

## Leak check

`leak.py task468 --asof 2027-01-12` on the final cut: REVIEW, no LEAK. Each REVIEW line, ruled:
- Sweep 1, the register's Notes sheet: the Trade Waste unit's two lines on the agreements in force and who prepared
  the register; it names no column of any other file. Harmless.
- Sweep 4, the laboratory notice and the policy: the stump terms are the documents' own words (method, sample,
  reference, laboratory, and chloride as an analyte the laboratory reports on every compliance sample); neither names
  an interference, a factor, a model or a conversion. Harmless; the reader's question 1 asks it cold.
- Sweep 6, the register, the field jobs, the inspections and the production returns name the customers beside
  numbers: limits, reads, visits and production, none a COD mass or a verdict. Harmless.
- Sweep 9, the register's review dates in 2027: the agreements' forward review dates, a register's planned dates.
  Harmless.
- Sweep 11, the prompt's question form over the corpus quota (a voice-check WARN, PASS).

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method (it survives as Ask C's device, which the 10/10 rules leave free).
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
- 2026-10-17, stage 2: the review as a simple random sample of the unmatched events, its raw route mix the decisive
  step: a single insight the review file signposts (133 v1 died on a development sample pointing at its decisive
  step); the review is now a bus-day sample with one event each, so using it is R2 and weighting it is the move.
- 2026-10-17, stage 2: the composition varying by time band (trunk routes late in the afternoon only, pull-in deadheads
  at night): pooled and band-level shares gave different calls on Route 17, a grain fork (H14); lateness now flat
  through the day and out-of-service movements spread over it, so every stratification agrees.
- 2026-10-17, stage 2: Riverside failing on a four-an-hour timetable: Good Friday's Saturday service pulled its
  timetable average under four too, so the timetable rung landed on the golden; Riverside now runs five an hour and
  its afternoon runs went a quarter short of operators.
- 2026-10-17, stage 2: each candidate's lowest hourly average graded to one decimal: the weighted variants spread up
  to 0.3 on Route 2, so the prompt asks for the verdicts and the workbook carries the figures as supporting detail.
- 2026-10-17, stage 3: on-time shares to one decimal of a per cent: two routes' shares sat within a hundredth of a
  rounding edge, so the shares are graded to the whole per cent (every share further from its edge than one departure
  moves it, asserted); Hillcrest's lateness and timetable jitter moved so its share and its wait sit clear of their edges.
- 2026-10-17, stage 2: a scheduled-departures table from both feeds as an ask: a GTFS-literate cracker executes the
  calendar, calendar_dates and frequencies correctly, so no device held; replaced by the waits (an analytical device).
- 2026-10-17, stage 4: Ask A, Quinnell's April to June record by stop and service-day month: both outside readers
  found the file-head repeats by bus, stop and second and assigned the service days, the judge read the repeats as a
  fork, and no silent device reaches the record without touching the review's frame; dropped (the repeats, the 31
  March copy and the after-midnight service stay as Layer 1 on the call's path, asserted neutral).
- 2026-10-17, stage 4: Ask C, the scheduled wait on 13 May: the prompt's definition made the waiting-time paradox a
  literal integral both readers computed, the frequency window's end read two ways, and no representation of the feed
  hides a departure from a careful reader; dropped (the frequency trips now exact times, each block ending between
  two trips).
- 2026-10-17, stage 4: the on-time device as Quinnell's DeviationSec taken at arrival: both readers timed the
  departures from the timestamps and read the field as noise, and guidance 4.2's "as the AVL system records it"
  invited it; DeviationSec is now the departure against ScheduledDeparture, and the device is Arbor's minute-held
  schedule against the feeds' half minute.
- 2026-10-17, stage 4: Route 6's on-time share at 47.46, 0.04 from its edge (a reader rounding to one decimal first
  filed 48): the half-minute bands, set per transfer point, put every share at least 0.19 from its edge.
- 2026-10-17, stage 4: the eleven candidates named only by route colour in routes.txt (the judge's Gate B and E
  finding): Planning's candidate list now ships with each route's designated stop.
- 2026-10-17, stage 4: the on-time device as Arbor's minute-held schedule against the feeds' half minute: judge pass 2
  read the two schedule sources as an open fork (FIX_NOW), the pin naming the published timetable in guidance 4.1 and
  4.2 closed it, and reader round 3 then timed all eleven shares against the feeds. A device whose basis a filed
  sentence must name dies with the pin, and every other column the ask reads (the departure, the trip tie, the window,
  the days) is the call's own population, so no device on this ask can stay off the call's rows.
- 2026-10-19, repair: the stop-hour grain fork (reader round 3): the review drew 250 bus-days a month, so the
  stop-by-clock-hour cells held one to seven reviewed events and the minimum of thirteen noisy hourly estimates sat
  biased low; at 400 bus-days a month, with the within-bus-day draw on its own stream, every weighted grain (stop, stop
  and hour, band, month, vendor, the within-bus-day weight, counting-day reviews) files the golden and every raw grain
  the R2 slate (checks.py R3b, verify.py's stop-hour estimator).
- 2026-10-19, repair: replacing the dead on-time ask, measures tried on paper and dropped: the average scheduled wait
  (computed exactly from the feeds by any GTFS-literate solver, and "a weekday of current service" splits on the class
  days); missed trips from a dispatch log (it would hand every solver each route's delivered departures, the call's own
  quantity); APC boardings at the designated stops (doors open only in service, which would identify the out-of-service
  passes the review estimates); the fleet roster's asset tags moved between buses (it would move the review's bus-day
  join on the call's path); evening and Saturday counts (Quinnell's repeats and the cutover overlap are seen, not
  silent). The shelter ask takes none of the call's rows.
- 2026-10-19, architecture 1 spent (the transit nominations): four isolated readers landed the call, so the review
  weighted by its design was read off the memo's sampling procedure by every careful solver (Gate F, score_reader exit
  1), and judge pass 3 found the shelter ask NOT_DETERMINISTIC (no file states the moved-stop rule, and stating it
  hands over the device). The author chose to re-root.
- 2026-10-19, architecture 2 spent at stage 4 (the specialty pharmacists by months on therapy): the isolated reader
  projected the caseload by tenure since first fill from past month ends, its first move once it saw the program year
  unobserved, and landed the call (10 of 10) and 27 of 28 ask figures (score_reader exit 1); the bulletin's step-therapy
  sentence and the caseloads' 2026 starters made the duration mix visible, and the rebate statement's repeated
  product-quarter amount was caught on sight. A forward window over a record that shows the process invites the
  conditional development; the next architecture needs a decisive step the record does not display.
- 2026-10-19, architecture 3 drawn: the same world, the decisive step moved to the clock. Members who stopped a drug
  and came back after a lapse restart its persistence curve, so the development is indexed by months in the current
  episode; v2's first-fill development is now the analyst test's wrong answer (57 against 54). Tried first: a wave of
  returners 30 per cent of the step-therapy classes' past stoppers (GLP 177 of 1,809 back, first-fill clock only half
  a pharmacist off), raised to 60 per cent; a separation by back-test (both clocks pass the earlier Junes alike,
  returns being rare before 2026), replaced by the record's own comparison of returners with continuing members and
  new starters. The rebate statement's repeated product-quarter amount (caught on sight by v2's reader) kept as a
  hazard; the primary moved to the contract year's February start.
- 2026-10-19, architecture 3 spent at stage 4 (the specialty pharmacists by months in the current episode): the
  isolated reader built persistence by time since episode start, an episode broken by a gap of more than 100 days,
  because the refill gaps were a few days and the returns months, and landed the call (10 of 10; score_reader exit 1).
  A clock the gap distribution displays is not silent; architecture 4 is drawn fresh.
- 2026-10-20, the three architectures read together (the author's rule: no retirement, so a fresh architecture 4
  follows): architecture 1 fell to readers who read the review's weighting off the memo; architecture 2 (judged
  DETERMINISTIC and APPROVE) to a reader whose first move on an unobserved window was the tenure-conditioned
  projection; architecture 3 to a reader who read the episodes off the bimodal refill gaps. A forward window over a
  record that displays the process invites the careful reader's persistence model, and every clock the record shows
  plainly is a reflex at medium effort: the next architecture needs a decisive step the record does not display.
- 2026-10-20, architecture 4 calibration: the pooled rate by the link's pass was first the only stratification other
  than the class that the hospitals' mixes separated; hospital-by-pass rates also landed the golden set while each
  hospital's members without a number were mostly one surname type, and stopped doing so once Varden's members
  without a number became low-risk workers whose recorded deaths include none without a number, so its own rates
  borrow the pass's (R4c). Kept: the class is what drives the error, and a hospital's own rates are not identified
  where its controls are empty.
- 2026-10-20, architecture 4 build: dropping Carrisford's encounters moved Tamsin General (1.05) over the line on a third
  fewer admissions, so Layer 1 was not neutral; Tamsin General now sits at 0.93 and Calloway at 1.32, and every Layer 1
  mishandling leaves the five (SF1, SF6, SF7).
- 2026-10-20, architecture 4 build: a two-part surname read from a hyphen only puts most two-part surnames with the
  single ones and adds Varden; dropped from the fork table as no reading of the enrollment file (88 per cent of two-part
  surnames are written with a space), while a space-only reading files the five (SF8b).
- 2026-10-20, architecture 4 asks: interim bills carrying a stay's payment to date (a summed interim history double
  counts) and newborns billed under the mother's identifier (a stay-key deduplication drops them) were drafted for the
  bonus ask and dropped: the first is not how a plan's paid column behaves, the second reaches only the hospitals with
  deliveries, so no device moved all fifteen figures. The platform conversion's conventions move all fifteen and live
  in a column the call never reads.
- 2026-10-20, architecture 4 ask device: the CPS and platform replacement conventions, left unfiled, were the primary.
  Reader round 1 (on b1bc148c) read them off the amounts (CPS replacements centred on zero, 63 per cent negative, none
  on the platform) and confirmed them on hospital totals landing within a few dollars of round bonus figures, 15 of 15
  (score_reader exit 1), and the judge's first pass required the convention filed (inferable, not filed). A convention is
  a fork, not a device: filed in the extract notes, it is a hazard, and the device moved to the dispute log's awards
  that a reprocessed bill already carries. The base rates that had centred every bonus in its cell were retuned so each
  sits 15 to 35 dollars off centre.
- 2026-10-20, architecture 4 estimator: seven hospital classes with no links among the admissions no control reaches
  gave estimates below zero, which the golden floored and step 6 did not, so the judge's unfloored recompute differed
  at the first decimal (Calloway 189.5 against 189.8 deaths, Varden 24.3 against 24.5, Fairhaven 1.05 against 1.06).
  Filing a floor would be rule application on the decisive step; instead each such class now carries the links its
  false-link share expects (one more of its members found by the Office), so floored and unfloored agree (C1, C1b). The
  call is unchanged; Varden moves to 1.03 and Fairhaven to 1.09.
- 2026-10-31, architecture 4 retired at the batch audit (re-rooted, not repaired): it fell short of the survivor
  anatomy on the Reflex. Its golden was the field's own linkage-error correction (each class's false-link and
  missed-link rates applied to the Office's matches), so the field's named method sat at the top of the ladder,
  where a reader who knows record linkage applies it as a first move, and the Office's shipped match file was the key
  the link rode on; architecture 5 is drawn fresh in another client domain.
- 2026-10-31, architecture 5 draw: a constant-quality house price designation on hedonic attributes or a stock
  aggregation is spent (task482 architectures 4 and 5, both landed by readers who fitted the handbook's model); the
  draw keeps the field's repeat-sales index at rung 1 and moves the decisive step to the identifying assumption no
  sales file shows, the dwelling unchanged between its sales.
- 2026-10-31, architecture 5 stage 2: the developers' works at four to five residual standard deviations on a
  noise-only price model: a 3-sd residual trim on every pair dropped them and landed the golden set without the
  register; each dwelling now drifts about its ward's path (a spread growing with the holding period, as repeat-sales
  records show) and the works add 14 to 23 per cent, so no filter on the sales sees them (SF9).
- 2026-10-31, architecture 5 stage 2: owner works of every kind in the register, structural alterations among them:
  a reading that counts only enlarging work moved Kestrel Rise's published change by 0.2, a fork at the graded
  decimal; owners' works are now extensions, lofts and garage conversions, and every reading of "building work"
  files the same figures (SF2).
- 2026-10-31, architecture 5 stage 2: June 2021 postcode recodes split pairs across the recode and moved two wards'
  figures at the decimal between the literal address and a linked reading: dropped (SF4b).
- 2026-10-31, architecture 5 stage 2: a block of flats certified at its last flat's date let a flat's first sale
  precede its block's certificate, so a postcode-and-number match set aside pairs the full address kept (Calder Bank
  8.0 against 8.1): each block is now certified complete on one date (SF4).
- 2026-10-31, architecture 5 asks: the register's ward column holding the 2019 wards (a label stored before the
  boundary review) as Ask A's primary: an asking sentence naming the May 2023 wards kills it, and without one the
  register's own column is a literal reading of "ward", a fork; the column now carries the current wards and the
  primary is the approver's blank loss.
- 2026-10-31, architecture 5 asks: Ask B as a count of additional entries: every handling of the update reproduces
  the count (the battery's latest-version rule), so the count carried no device; the ask is the money paid.
- 2026-10-31, architecture 5 asks: Ask C's re-claims as one-to-one repeats of Brackwell's claims (postcode, start and
  homes): the battery's re-keyed-record match finds them; Brackwell now claims its sites phase by phase and
  Calderstone each site once, so a re-claim equals only the phases' sum.
- 2026-10-31, architecture 5 shock: Pellbury's 2024 and 2025 company purchases made it the largest count of
  additional entries in those years; the city-centre and student-let wards now carry their own company buying, and
  Pellbury sits second of the twelve.
- 2026-10-31, architecture 5 leak screen: the price paid field guide (a PDF listing every column) is a dictionary
  under leak sweep 1 and 12; dropped, and the price paid files carry the publisher's header row instead.
- 2026-11-01, architecture 5 dead at its stage 4 judge (NOT_DETERMINISTIC, SEND_BACK): Harrowmere's pressured wards on a
  repeat-sales index with the pairs spanning building work set aside. The methodology's section 3, executed word for
  word, pairs every two consecutive sales, so Pellbury reads 6.0 per cent and the uplift splits four ways; the golden's
  set-aside rested on the intent phrase "same dwelling at the same quality", a narrower certificate reading (new
  dwellings and conversions only) was equally licensed, and filing the set-aside would have made linking the
  completions register a rule executed (task445 architecture 2's death). Ask 3's net additional dwellings also failed
  to reproduce (365 against 348). An inclusion or exclusion over a second source has no safe filing; the report is
  kept as determinism_check_report_arch5.md, and architecture 6 re-roots into another domain with the decisive step an
  estimate.
- 2026-11-01, architecture 6 at stage 3, every free gate green but one: `guard.py heart` BLOCKs the pairing, the
  subdomain, the role, the context artifact and the forcing event against task456 v2 (a US flexible packaging
  converter's 2026 VOC emissions, physical-environmental-sciences / emissions-inventory ETL), registered at
  01:00:52Z, 93 seconds before this card, its DRAWN commit reaching main only after this card's `guard.py check` passed
  on a fresh pull. The guard forbids relabelling a card or waiting for the window, and this world has no honest
  draw outside the physical-environmental-sciences cell, so architecture 6 re-roots unless the author has task456
  yield the cell; the build is kept whole on target.zip for that decision.
