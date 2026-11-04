# task476 design note: Tallis Creek's 2026 bypass minimum flow

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first. Architecture 5, a
re-root drawn 2026-11-04 after architecture 4 (remeasured plot trees re-linked where tags were lost) was spent at stage 4
on Gate H; architectures 1 to 4 are in the card's lineage with their shells, and architecture 2's shipped pack (5a46ee5a)
stays at the portal, pending, until this build replaces it at ship.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task476.json` (architecture v5), registered 2026-11-04T09:00:03Z;
  `guard.py check` PASS (one NOTE: the same-driver signature against task274, differentiated on the card). The window
  before the card: task192 v4, task461 v3 and task488 v2, so their forums (operations_desk, customer_or_counterparty,
  committee_or_panel), forcing events (shift_or_daily_cycle, audit_or_inspection, incident_or_complaint), organisation
  families (local_government, other, cooperative_or_member_body), decision types and strategies were off the table.
  Nearest driver task178's lineage at 0.08.
- **Seed:** ET33's number, re-rooted four times; nothing of any earlier world is kept.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data
  Extraction & Conformation (ETL). The licensee rebuilds its bypassed reach's 2026 flow record from the gauge's stage
  record, the station register, the consultant's rating report and the hydrographer's visit log, conformed to local
  days, and files its minimum-flow deviations with the regulator.
- **Shape:** 17, periods around a change point: the deviation periods either side of the 27 July storm and the pulse.
- **Strategy:** forecast_method_backtest. The record is computed on a stage-discharge relation, and the hydrographer's
  discharge measurements test the published relation the way a back-test tests a method: they pass Rating 7 before the
  storm and fail it after. Decisive generator G4 (attribution at the transition: which relation each interval is
  converted on), with G16 (method selection). Gate G method_or_model_selection.
- **World:** United States, a fictional creek in Oregon's western Cascade foothills. Tallis Creek Power Company runs one
  run-of-river project: a diversion dam, a 150 cfs unit and a bypassed reach whose License Article 403 minimum is 50 cfs
  from July through September and 30 cfs otherwise. The plant's gate controller holds the bypass flow gauge BP-1 reads
  through Rating 7 (2023) on a setpoint 4 cfs (3 in October) over the minimum. A thunderstorm on 27 July tripped the
  unit, sent about 1,400 cfs down the reach and left gravel on the gauge's riffle control. Personas from `guard.py names
  --geo "United States" --seed 476`: Marissa Harmon (compliance manager), Melinda Walter (consultant hydrographer),
  Krista Soto (plant superintendent).
- **Forcing fact:** the licensee files its 2026 minimum-flow deviation report with the Commission; the quantity is the
  closed 2026 season (retrospective, because the license measures the season just ended).
- **Forum and forcing event:** regulator_or_inspector, statutory_or_regulatory_filing. Organisation
  utility_or_infrastructure; role compliance_or_audit. Context artifact register (the station register).
- **Data-native sentence:** gauge BP-1 sits on a gravel riffle control, so a flood that moves gravel moves the stage at
  which every flow passes, and because the plant's controller steers the release by the flow the gauge reads through
  Rating 7, the converted record holds its 54 cfs target to the decimal while the reach carries what the moved control
  passes at that stage; only the hydrographer's measurements after the storm, taken at the held stages, show it.
- **The WHAT screen.** Population: every local calendar day of the 2026 season. Outcome: the day's mean flow in the
  bypassed reach below Article 403's minimum. Window: May 1 to October 31. Unit: cubic feet per second, daily mean.
  Comparison: the article's minimum for the day. The decisive step settles none of them: it is which stage-discharge
  relation converts the stage the gauge recorded into the flow the reach carried.
- **Abstraction sentence:** "a converted record sits on its target because a controller steered the proxy, and the
  conversion moved under it at an event; only checks taken after the event show it." Not writable against an approved
  build: task461's nested meters subtract parts twice, task274 regroups readings by calibration epoch, task178's
  lineage fitted a flood rating to sparse peaks; none has a controller holding the converted value on target.
- **Sources (all constructed, declared in `metadata.json`):** the stage record (10-minute, Pacific Standard Time), the
  station register (station sheet, Rating 7's expanded table to 4.00 ft, rating history), the consultant's 2023 rating
  report (both segments' equations and the measurements behind them), the 2026 field visit log, the release log, the
  license articles, the 2024 flow monitoring plan, the 2025 compliance report, and three files the solution never reads
  (water temperature, daily generation, powerhouse precipitation).
- **Deliverables:** `bypass_flow_record_2026.xlsx` (every local day's mean flow and whether it met the minimum) and
  `minimum_flow_deviation_report_2026.docx` (the deviation periods, the cause, the shortfall, and the May and June bypass
  volumes Article 404 counts).

## Survivor anatomy

Actor: the flow the reach carried has no column anywhere: the stage record holds stage, the release log holds the
controller's rated setpoints, and the moved relation exists only as a disagreement between rows of two files (each
post-storm measurement against Rating 7 at its own gauge height).

Link: the link is read by evaluating Rating 7 at each visit's gauge height and comparing it with the discharge measured
there, a cross-file check across the register, the rating report and the visit log that no key and no sentence invites.

Reflex: the field's method for a gauged record, the station's current rating applied to the stage, sits at rung 0 and
files no deviation, because the controller held the rated flow on its targets.

Back-test: the textbook route validates: every measurement before the storm agrees with Rating 7 within 3.3 per cent,
the 2025 compliance report computed on Rating 7 passed, and the converted record never dips below its setpoint.

Second use: every file the step reads is read for its own reason: the stage record and the register for every flow,
the visit log for the gauge checks and spring measurements, the release log for the setpoints and the storm's trip.

Shock: the movement the step recovers reads as nothing at all: the converted record is flat on target through August
and September, and the storm day itself is far above the minimum on every relation.

Pins: the WHAT is filed in License Article 403 (a daily mean flow in the bypassed reach of at least the month's minimum)
and the monitoring plan (flows computed from the gauge's stage record by standard USGS methods); no filed sentence names
the rating, a shift or a measurement comparison.

## Default path

1. Read the stage record, convert each 10-minute stage to flow through Rating 7's expanded table (the station register),
   and average the flows by local calendar day.
2. Compare each day's mean with Article 403's minimum for the day.
3. File the days below it.

Ends on: no deviation in 2026 (every day's mean flow at or above its minimum).

Golden: deviations from 29 July through 13 September and from 21 September through 31 October 2026.

## Stump sentence

The default path converts the stage record through Rating 7, the station's rating in force, takes local daily means and
files no deviation in 2026, because the plant's controller held the rated flow on its targets; it never sets the
hydrographer's post-storm measurements against the rating, which sit 13 to 18 per cent below it at the held stages, and
on the relation they establish the reach fell below its minimum from 29 July through 13 September and from 21 September
through 31 October.

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
- 2026-11-04, architecture 3 abandoned at the stage-4 re-judge (pass 2 NOT_DETERMINISTIC, competing_defensible_answer; the pass 1 FIX_NOW filing pass, target.zip 80bcc4b9, moved no figure): Gate C on the main call with Gates G and H passing, so by the gate table it was not spent; it was re-drawn rather than repaired because separating the two conversions needed a new data organ, a metered deep well, inside a 24 acre-foot decision margin. nothing shipped forced the head-adjusted conversion over holding each test's kWh per acre-foot constant. The reports' printed definitions say how the test-day figure was derived, not that energy converts at a moved head on other days, and the loggers show the head moved, which is not the same thing. The only metered wells were the upper-aquifer ones, where the candidates coincide (constant even fits them better, +0.7 against +1.1 per cent annual bias), while no deep well, where the methods diverge by about 6 per cent, was metered: constant files 15,020 and no purchase against the golden's 15,583 and 250, the golden 24 acre-feet inside its 50-acre-foot block. The rule it paid for: an open method needs shipped instances where the candidates diverge, separating them with margin, and a decision band wide against every candidate's spread. The second reader's realism tell: one sentence ("original bowls, 1998 installation; rebuild recommended") sat verbatim on reports from two different firms.
- 2026-11-04, architecture 4 spent at stage 4 (judge SEND_BACK on Gate H, determinism_check_report_arch4.md; the reader's answers in leak_check_report_arch4.md): the decisive step was classed a planted identity defect with Layer 2 missing. On the clean truth, with no tag lost, the tag join is exactly right, so the easy route failed only because the identifiers were destroyed (imperfect keys are Layer 1), and once the stem-map match is thought of there is nothing left to estimate or choose (48 of 48 settings, zero spread); the card's analyst test described the corrupted data, not the clean truth. Secondary: the per-acre estimator on the asks was unpinned. The rule it paid for: run the analyst test on the generator's clean truth before carding, and put the decisive step on an estimate or a method choice the field makes on correctly keyed data, the data separating the candidates with margin.
- 2026-11-04, the draw that followed (architecture 5, a hydro bypass minimum flow on a gauge whose control a storm moved while the plant's controller held the rated flow on target) was priced on the clean truth before carding (screen5.py, session scratchpad): Rating 7 on the stage record files no deviation; the truth files 88 days in two periods, 29 July to 13 September and 21 September to 31 October; every day sits 7.6 per cent or more from its minimum; the measurements before the storm agree with Rating 7 within 3.3 per cent and those after it sit 13.3 to 17.9 per cent below.
