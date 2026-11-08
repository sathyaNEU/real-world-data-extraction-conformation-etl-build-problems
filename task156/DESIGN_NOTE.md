# task156: a rapid-charging operator, which hubs fall below 99 per cent availability in 2027 (architecture 4)

Private, never ships. Architectures 1 to 3 were each returned FAILED_TO_STUMP by the portal: Millrind's paid
moderation pool (product analytics), the Riverbank Road pump station's consented overflows (physical and
environmental sciences) and the union branch's protected action ballots (political science and public policy, both
responses on the golden 11 councils on 2026-11-07). The slot is re-rooted in a fourth domain: world, decision,
quantity, data, generator, prompt shell, deliverables, asks and mechanism are all new, architecture 3's build outputs
left the folder at this draw (git history keeps them), and the three identities sit in the card's `lineage` with
their fates.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v4, registered 2026-11-08; architectures 1 to 3 in `lineage`, their three shells in `lineage_shells` |
| Domain / task type | `energy-systems-utilities`, task type `asset-condition-maintenance` (serves Forecasting): the deciding quantity is each high-power charge point's availability in the 2027 contract year, forecast from each failure mode's frequency and the downtime it costs through the visits, repairs and asset changes the year will run under |
| Objective | Forecasting & Predictive Modeling: availability in the contract year 1 January to 31 December 2027, a window not yet open; the asset base is the partnership's renewal programme of record (the legacy units out at its hubs by 18 December 2026) |
| Shape | `10`, a scorecard against one threshold: every hub carries its high-power charge points' lowest 2027 availability and a side of the 99 per cent standard, and the call is the set below it |
| Decision | `designation_set`, answer unit `set_of_items`: the hubs the operator names in its 2027 availability plan because a high-power charge point there is forecast below 99 per cent |
| Mechanism | gap time (the hang record describes hubs powered down every few weeks, the 2027 bet is on hubs powered down a few times a year); generators G7 (a hang can only happen inside an uptime window that the hub's power-down regime opens or shuts), G14 (the hang rate measured on hubs with a legacy unit does not apply to hubs without one), G13 (the 2027 regime differs from every year on record); Gate G `forecasting`; strategy `forecast_method_backtest` (each unit's hang rate is stationary only per day of uptime past the onset, a quantity rebuilt from the status history, while a per-unit calendar rate belongs to the regime it was measured in) |
| Layer 2 family / pattern | `estimation_fit`; `own:hang-hazard-on-the-hub-power-down-clock-carried-through-a-changed-repair-regime` |
| Furniture | forum `customer_or_counterparty` (the North Midlands Charging Partnership, the concession's grantor, reviews the plan), forcing event `audit_or_inspection` (the partnership's annual concession review in December 2026), organisation family `utility_or_infrastructure` (a public rapid-charging operator), role family `operations_director` (the operator's network performance lead), context artifact `monitoring_export` (the back office's connector status history), calibration `none`, opening `question-first`, question form `which` |
| Spine | `connector_status_history_2023-2026.csv`, one row per status change a charge point reported to the back office or the back office wrote when its heartbeats stopped (about 90,000 rows, UTC), beside the asset register, the contractors' work orders, the planned maintenance schedule and the operator's supply interruption log; constructed for this build, no real dataset |
| Deliverables | `hub_availability_2027.csv` (the partnership's plan return, one row per hub, the asks in its columns), `availability_plan_2027.pdf` (the covering letter naming the hubs) |
| People | drawn with `guard.py names --geo ireland --seed 156`: Sorcha Jackman (the operator's network performance lead), Bronagh Allis (the partnership's concession manager), Ailis Fee (the maintenance contractor's service manager); Henry Dunford passed over, his first name already on task457 |

**The hubs.** Thirty hubs, each with one legacy 50 kW unit (DPS 50, 2017 to 2019) and one to four high-power 150 kW
units (DPS Velo 150, 2021 to 2023). Motorway service hubs: Carrigvane Services, Lismoy Services, Ardcree Services,
Knockvane Services, Drumtane Services, Monaleen Services (planned visits every two months). Programme hubs besides the
three motorway ones above: Kilbeg Retail Park, Tullymore Market Square, Clonlea Leisure Centre, Rathmoy Station Road,
Glenfad Shopping Centre, Ballinkeel Main Street, Derrylane Park and Ride, Annagh Cross, Cloonfin Crossroads (the last
two on long rural supply spurs). Coastal hubs: Bunacurry Pier, Rossnabeg Harbour, Portavaddy Seafront. The other
twelve keep their legacy units.

**Guard answers (check on the draft and again on the registered card).** WARN `repeat.decision` (designation_set
repeats task268): the decision is a set of named hubs because the concession's plan names hubs, and no other answer
type fits the review. WARN `repeat.question_form` (which repeats task482): a pick of a set asks which, as the
guide-to-prompt rule says; the shell differs from task482's at the second sentence and the deliverable set. NOTE
`test.same_puzzle_older` (task451) and `test.same_driver_older` (task105 v1, task162 v2, task170 v1, task229 v3):
differentiated on the card, one line each. Variants measured at the draw and refused: pattern E (same puzzle as
task235 and task445, same driver as eight builds), G14 decisive (`ban.pattern` against task250), G13 decisive
(`ban.pattern` against task482), pattern A (ten older drivers). Forum, forcing event, organisation family, role
family, context artifact and strategy clear the last three builds (task250, task482, task268).

**The data-native sentence.** The back office's connector status history records each charge point going offline,
and the only place a hub's power-down shows is the minute in which every unit there drops at once; the high-power
units' controller hangs, which only an on-site restart clears, come after the days since the unit last powered up,
and the legacy unit's cabinet repairs, which isolate the whole hub at its main switch, are what kept those spells
short through 2023 to 2026.

**The abstraction sentence.** "A unit's failures run on a clock that its neighbours' repairs reset, so a plan that
removes the failing neighbours raises the survivors' failures." It cannot be written against the nearest approved
builds: task132 (a failure resets the failed item's own wear curve), task303 (a shared upstream loss every unit logs
in the same minute is taken out of a figure), task162 (a device acts only above its setting), task141 (a cap moves
every unit to the at-ceiling rate), task169 (a closed route had pre-empted the open one), task175 (a vacant lot's
take-up follows its own street's fill); nor against task156's spent architectures (a closed pool's falling leaving
rate, infiltration scaled by submerged sewer, a delegate in post at the worksite); nor against the two nearest
drivers by text, task127 v4 (supporting one firm prevents its dependants' failures) and task173 v3 (work on a unit
breaks the parts attached to it soon after).

## Shape

Shape 10, a scorecard against one threshold. Criteria: the set (1), each hub's side of 99 per cent (30), the asks
(each hub's January to October 2026 high-power sessions and the energy they dispensed, 60), the two deliverables (2):
well over 25, supplied by the answer's structure. The prompt names no count.

## Default path

1. Read the asset register (the June 2025 back-office migration re-keyed every charge point and the register carries
   both IDs), the connector status history (UTC), the two maintenance contractors' work orders (Irish local time, a
   different job-code list after the April 2024 contract change), the planned maintenance schedule, the supply
   interruption log, Schedule 4 of the concession agreement and the partnership's renewal programme.
2. Rebuild each high-power charge point's availability for 2023 to 2026 under Schedule 4 (Faulted, Unavailable and
   Offline minutes count; notified planned maintenance and supply interruptions are excluded).
3. Fit the asset-condition forecaster's failure model for each high-power charge point and failure mode: controller
   hangs (offline until a technician restarts the unit on site) and other faults, a rate per unit-year on model,
   commissioning year, sessions, hub and month, unit effects shrunk to the fleet, with the downtime per event from the
   work orders' attendance and repair times.
4. Validate: leave each charge point out, and back-test 2025 from 2023-24 and January to October 2026 from 2023-25;
   each hub's availability lands within a few tenths of a point and on the right side of 99 per cent.
5. Carry the rates into 2027 on the programme's asset base (legacy units out at its hubs, new 150 kW units in) and
   list the hubs with a high-power charge point below 99 per cent.

Ends on: 3 hubs (Bunacurry Pier, Portavaddy Seafront, Rossnabeg Harbour).
Golden: 10 hubs (Ballinkeel Main Street, Bunacurry Pier, Clonlea Leisure Centre, Derrylane Park and Ride, Glenfad
Shopping Centre, Kilbeg Retail Park, Portavaddy Seafront, Rathmoy Station Road, Rossnabeg Harbour, Tullymore Market
Square).

## Stump sentence

Carrying each high-power charge point's controller-hang rate from 2023 to 2026, validated leaving each unit out and on
two back-tests, files 3 hubs below 99 per cent in 2027, the three coastal hubs on their ordinary faults; the step that
lands it there is reading each unit's hang rate as its own, when a hang comes only after about 75 days without a
restart and the legacy unit's cabinet repairs restarted every unit at its hub every few weeks, so at the seven
programme hubs with neither two-monthly visits nor frequent supply interruptions the high-power units run months
between restarts, hang three or four times a year, and the set is 10.

## Three rules

Task type: asset-condition-maintenance (Energy Systems & Utilities), which serves Forecasting & Predictive Modeling: each high-power charge point's availability in the 2027 contract year, forecast from each failure mode's frequency and repair downtime under the visits, repairs and asset changes the year will run under.
Domain test: the deciding quantity is each high-power charge point's 2027 availability against the concession's 99 per cent standard, worked the way asset condition and maintenance forecasting works it, each failure mode's frequency and the downtime each event costs carried through the year's planned visits, repairs and asset changes; with another field's nouns there is no failure a power cycle clears and no repair that powers a whole hub down, so the forecast stops reading.
Swap: put "hospital wards" for "hubs" and "beds" for "charge points": a ward has no main switch that a neighbour's repair opens and a bed does not seize until it is power cycled; put "megawatt-hours" for "minutes available" and the restart clock has nothing to count.
Layer 1: the June 2025 back-office migration re-keyed every charge point (the register carries both IDs); the status history is in UTC and the work orders in Irish local time; the back office writes Offline only after three missed heartbeats, about fifteen minutes after a drop; status notifications are re-sent and duplicated; the two maintenance contractors used different job-code lists before and after April 2024; the planned maintenance schedule changed layout between its 2025 and 2026 sheets; Schedule 4 and the programme are PDFs with tables. Nothing is placed to be caught.
Layer 2: estimation_fit: the hang rate has to be estimated on the clock that drives it, the days since each unit last powered up, each spell ended by the next power-down or restart, and the 2027 forecast run on the power-down regime the programme leaves; the choice that flips the call is reading each unit's recorded hang rate as a property of the repair regime it was measured in.
Decisive step: recognising that the high-power units' hangs come only after about 75 days without a restart, that every unit at a hub restarts whenever the hub is isolated for a legacy cabinet repair, a planned visit or a supply interruption, and that the programme takes the legacy repairs away, so each 2027 unit's hangs follow the days between its hub's remaining power-downs.
Not semantics: every field, code and clock read correctly (IDs crosswalked, UTC converted, the heartbeat lag allowed for, duplicates removed, both contractors' job codes mapped, Schedule 4's exclusions applied) still leaves the unit-level route on 3 hubs; no field records a power-up or ties a high-power unit to a legacy repair, and no file defines a hang by uptime or names the restart.
Not rule application: no filed rule or procedure says a hang depends on the days since a restart or that a legacy repair restarts the hub's other units; Schedule 4 files only the availability definition, its exclusions and the standard. Enumerated family (each unit's own rate carried, a hierarchical rate by hub, a flexible learner on each unit's history and the hub's attributes, last year's availability carried, the fleet's monthly series, the learner given the hub's recent legacy jobs or the days since its last planned visit): 3 hubs on every member, measured on the prototype and to be asserted in checks.py; standing family once the restart clock is seen (the hang rate by days since power-up read as a life table, a piecewise rate or a fitted onset, run through the 2027 regime by simulation or by renewal arithmetic): the same 10 hubs, so the standing spread on the graded set is zero only after the step; what rules the cheap members out is the hangs' onset in the days since power-up, which only the hub-wide offline minutes in the status history show.
Analyst test: a strong analyst who maps the IDs, converts the clocks, applies Schedule 4 and reads the programme fits each high-power charge point's hang and fault rates, validates them leaving each unit out and on 2025 and 2026 back-tests, carries them into 2027 with the legacy units removed and files 3 hubs (the three coastal hubs); seven programme hubs it passes fall below 99 per cent once the hangs are read on the days since the hub last powered down.
Estimand: Schedule 4 of the concession agreement files the population (every high-power charge point in service at a hub in the contract year), the outcome (the share of the year's minutes in which it was not Faulted, Unavailable or Offline, minutes of notified planned maintenance and of supply interruptions excluded), the window (the 2027 contract year), the unit (the charge point) and the comparison (below 99 per cent), and its clause 4.6 names the hubs the plan must list (any hub with a high-power charge point forecast below the standard).
No decoy: nothing is planted: no memo, briefing, forecast or stakeholder figure ranks the hubs or argues a set; the programme says which units go and why (end of life, parts withdrawn), not what availability follows; the customer survey and the tariff schedule are distractors that carry no availability figure.
No certified replay: the method is not hidden behind a certified figure to be reproduced; no availability statement for a past year ships, both routes reproduce the history the status log records, and the decisive step changes the forward window, not the fit to the past.
Lesson: a failure rate measured on units whose clock their neighbours' repairs kept resetting belongs to that repair regime, and a plan that removes the neighbours has to be forecast on the clock that drives the failure, not on the rate; no build on file has a unit's failure clock reset by repairs made to other units.

## Tried and rejected


- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
- Architecture 2 (the PS03 overflow replay with each day's own water table), returned FAILED_TO_STUMP on 2026-11-07:
  both responses landed the hold call. Response 1 replayed 2004 to 2023 and filed 48 overflows against the 40 the
  consent allows, then 2 after the upgrade; Response 2 filed the same hold. Any full-record replay with the subdivision
  already broke the consent, so the decisive step (each replay day's own water table) was never needed. Lesson: the easy
  route has to be the one strong solvers actually file, and it has to land on the wrong side; a count of rare
  exceedances spreads with every modelling choice, so the call now sits on a mean quantity whose naive family is tight.
- Judge round 1 (2026-11-07, FIX_NOW on the asks; the call forced, Gate G analytical_non_defect, Gate H pass). Ask A's
  window read literally dropped the platform councils' last run (a 2 July 2026 date in the period-end column): FP-04 now
  files the record's own convention (a pay period ends on a Sunday and is paid later that week; credited to the year it
  ends in), naming no platform and no weekday the advices carry. Ask B's unit was open (raw, per invitation and day, or
  per organiser, invitation and day): the asking sentence now files it (a visit two organisers made counts for both, a
  moved booking once as held). Both asks were scoped to the 30 councils the branch covers while the prompt read as the
  round: cut to the round's 24, the regional platform's twelve councils re-sited inside the round on the same pay
  cycles, so no in-round figure moved. Ask 1's turnout figures had no rounding and a refit evaluating members at the
  extract sat about 0.7 points under: the guide now files each member as they will stand when the ballot period closes
  and the tracker files that period (1 to 15 March 2027); whole-per-cent figures were not adopted because five councils
  sit within 0.05 of a half point (Corrigan Valley 62.53, Halston 59.53, Pellham 58.49, Rosedene 45.51, Underhill 40.54),
  so a worksite-effects refit (lift 1.027) can cross a rounding edge; the prompt asks only whether each council reaches
  half, the side being determinate under every refit. freeze.py: the main side unmoved; the twelve out-of-round ask
  figures and block 4's turnout percentages were dropped by the repair (allowed, this line).
- Hardening noted, not applied (the judge rated stump power moderate to good: a model that fits the delegate term lands
  the call): ship the 2026-28 term as the organising coordinator's separate July 2026 election return rather than a
  sheet of the delegate register, so the register a solver opens holds the terms the online votes cover and the new
  term sits in a file read for its own purpose; the call, the stump and every figure would stay frozen.
- Judge round 2 (2026-11-07): DETERMINISTIC, the call reproduced with 6 points either side and no respecification
  flipping a council, stump power moderate to high. Before ship: step 8 reworded (the golden keeps the later, last
  updated row of a moved booking); the xlsx inputs' creator and last-modified-by set to the branch, the body that
  issues them; the 2021 declarations given the Producer of the LibreOffice release current at their June 2021 export
  (7.1; the info dictionary is the last object, so startxref moves and every object offset is asserted unchanged), the
  other four PDFs dated after 24.2's February 2024 release; and the hardening above applied: the 2026-28 term now ships
  as `delegate_election_return_2026.xlsx`, the returning officer's return, and `delegate_register_2018-2026.xlsx` holds
  the terms to 2024-26. No graded figure moved (freeze.py); the input gates hold (17 files).
- Surface at ship promoted three pairs on card axes alone: task157 (back to back, the same domain and objective; a
  petition sample's pair defects, not a turnout forecast, differentiated on the card), task154 (the calibration form
  realised_outcome_roster repeated two builds apart: redrawn to counterparty_acknowledgement, the agent's declared
  results being a counterparty's record) and task265 (left truncation in a descriptive survival estimate,
  differentiated on the card); heart PASS; left for the author's adjudicated clone check.
- Architecture 3 (the union branch's protected action ballots, each member read with the delegate in post at the
  ballot): FAILED_TO_STUMP on the portal 2026-11-07, both responses on the golden 11 councils. Both put worksite
  delegate coverage in the turnout model from the start and evaluated it at the ballot close with the 2026-28
  delegates, so the decisive step was the forecaster's reflex (a recorded covariate's forward value), and the July
  2026 election return, read by nothing else, announced it. Re-rooted to architecture 4 in a new domain and world.
- Architecture 4 draw screens (2026-11-08), each rejected before any card or data: vacancy chains through a
  fixed-post hierarchy (dead in task174's and task137's notes, and a stock-and-flow check of posts finds it); a
  programme's lead-in audience (task115 and task174); one facility's overflow into a sibling removed by an expansion
  (task308's reader named railheading and the full car park's hidden demand, and the swap reads the same for wards
  or car parks); ward acquisitions per colonised patient-day (task181: infection prevention's own reflex); errors
  per interruption or per handover (task198 and task173); wear accrued only in hours inside a band after a duty
  change, and pump failures per start after a control change (task307's driver); admissions that rise with spare
  beds (a filed bed opening prompts the question, and the forecast needs a fixed point whose estimator forks);
  speculative double bookings (the hygiene battery's de-duplication reaches it and the identity match is Layer 1);
  bus headways under a denser timetable (task308's probe replayed the operation and carried every knock-on).
- First prototype of this draw (hangs on days since power-up, any site-wide power-down a reset): the parameters put
  every hub below 99 per cent; the legacy cabinet repairs now isolate the hub every few weeks, hangs start only after
  about 75 days, and the high-power units sit near 99.5 per cent on the record.
- Hang restarts isolating the whole hub: the units then restart one another and the programme hubs stay above 99 per
  cent; a hung unit is restarted at its own breaker, and only the legacy unit's cabinet repairs, planned visits and
  supply interruptions restart the whole hub.
- Three hubs whose legacy units rarely needed the cabinet opened, failing on both routes: the hubs' legacy repair
  counts then predict the high-power hangs across hubs, and a hub covariate (legacy units at the hub, or their
  repairs) would extrapolate to the golden, architecture 3's failure again; every hub now has exactly one legacy unit
  with cabinet repairs of 10 to 12.5 a year, and the hubs that fail on both routes are three coastal hubs whose
  high-power units suffer ordinary corrosion faults.
- The learner given the hub's legacy jobs in the last 60 days, the days since its last legacy job or the days since
  its last planned visit (prototype, clean truth): none reaches the golden; at the programme hubs they carry 0.7, a
  noisy 0 to 1.4 and 0.4 to 0.7 hangs a unit-year against about 3.3, so each files the default path's set.
