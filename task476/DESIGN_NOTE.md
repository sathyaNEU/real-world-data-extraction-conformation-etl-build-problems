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
  converted on), with G16 (method selection). Gate G signal_vs_noise_or_hold (whether the post-storm departures from the rating are measurement noise or a moved control).
- **World:** United States, a fictional creek in Oregon's western Cascade foothills. Tallis Creek Paper Company runs one
  run-of-river hydro project at its mill: a diversion dam, a 150 cfs unit and a bypassed reach whose License Article 403 minimum is 50 cfs
  from July through September and 30 cfs otherwise. The plant's gate controller holds the bypass flow gauge BP-1 reads
  through Rating 7 (2023) on a setpoint 4 cfs (3 in October) over the minimum. A thunderstorm on 27 July tripped the
  unit, sent about 1,400 cfs down the reach and left gravel on the gauge's riffle control. Personas from `guard.py names
  --geo "United States" --seed 476`: Marissa Harmon (environmental manager), Melinda Walter (consultant hydrographer),
  Krista Soto (plant superintendent).
- **Forcing fact:** the licensee files its 2026 minimum-flow deviation report with the Commission; the quantity is the
  closed 2026 season (retrospective, because the license measures the season just ended).
- **Forum and forcing event:** regulator_or_inspector, statutory_or_regulatory_filing. Organisation
  manufacturer (the licensee is the mill); role compliance_or_audit. Context artifact register (the station register).
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

## Three rules

- Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), serving Data
  Extraction & Conformation (ETL): a stage logger's export, a station register, a rating memo and a field visit log
  conformed into one daily flow record on local days, and the license's deviations read from it.
- Domain test: the deciding quantity is each day's mean flow in the bypassed reach, the hydrographic record the field
  computes from a continuous stage record through a stage-discharge relation held to the discharge measurements made
  at the gauge (USGS record computation), against the license's daily minimum.
- Swap: replace the relation the measurements establish with the station's published table and the call moves from
  88 deviation days to none; the deciding object is the record computed on a measured relation, so the GSDS swap of
  method changes the call, and no sort or filter of shipped columns files it.
- Layer 1: the logger keeps Pacific Standard Time all year while the license counts local days; the expanded table stops
  at 4.00 ft and the high-water segment is an equation in the 2023 memo; the plant logs setpoints in local time and in
  the controller's rated cfs; visits fall between logger intervals; the export carries a header block and runs a few
  days either side of the season. Each is how its system writes, and none is placed to be caught.
- Layer 2: the field's own method done right: the stage-discharge relation is an estimate the discharge measurements
  test, and the choice that flips the call is whether the record is computed on the published table or on the relation
  the 2026 measurements establish after the event that moved the control.
- Decisive step: setting each 2026 measurement against Rating 7 at its own gauge height, seeing the four after the 27
  July storm sit 11.7 to 17.4 per cent below while the four before agree within 0.4 per cent, and carrying the measured
  stage correction (0.10 ft) from the storm's peak through the season.
- Not semantics: reading every field and document right (the stage in feet on standard time, Rating 7's table, the memo's
  segments, the setpoints in rated cfs, Article 403's local days and minimums) still leaves the published table on no
  deviation, because no field or definition says the table no longer holds; only the measurements set against it do.
- Not rule application: no filed rule or procedure says which relation converts which interval; executing Article 403,
  the monitoring plan and the register's table files no deviation. Enumerated family on the call: Rating 7 throughout
  (no deviation), the days a measurement fell below the minimum (3 days), the measured shift from the storm's peak (88
  days), prorated between measurements (88), a flow ratio from the post-storm measurements (88); standing family once
  the measurements are read: the three measured-relation members, spread zero on the periods, the day count and the
  shortfall to the nearest 100 acre-feet. Rating 7 stands outside it because every post-storm measurement refutes it by
  more than twice the 5 per cent the memo accepts, and nothing but that cross-file comparison says so.
- Analyst test: a strong analyst who reads every field and rule correctly converts the stage record through Rating 7,
  the rating in force, takes local daily means, compares them with Article 403's minimums and files no deviation in 2026
  (every day's mean at or above its minimum).
- Estimand: License Article 403 (`license/license_order_excerpt_2019.pdf`): population, every local calendar day; outcome,
  the day's mean flow in the bypassed reach below the day's minimum; window, the 2026 season; unit, cfs, daily mean;
  comparison, 50 cfs from July 1 through September 30 and 30 cfs otherwise.
- No decoy: nothing is planted: the stage record, the register and the measurements are each exact; no memo, draft or
  stakeholder figure argues compliance; the 2025 report is last year's, true on its own year; no block is copied.
- No certified replay: no certified or published 2026 flow exists to reproduce; the pack ships no computed flow at all,
  only stage, the relation's documents and the measurements.
- Lesson: a converted record that sits exactly on its controller's target is the controller's own reading, not a flow;
  the field's own checks, the measurements set against the relation, decide whether the relation still holds, and no
  build on file teaches a controller holding the converted proxy on target while the conversion moved under it.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 Rating 7 throughout (no deviation) | no | no | yes, the station's rating in force | no | no | no | no | readable |
| 1 the measured days alone (three days) | no | yes, the measured discharge column | yes, a spot check read as the day | no | no | no | no | readable |
| 2 (decisive) the relation the measurements establish, from the storm's peak (88 days) | no, no sentence names a shift or the rating's error | no, no column holds a flow, a shift or a rating comparison | no, the reflex is rung 0 and files none | no, the 2025 report and the memo validate Rating 7 | no, the battery finds no duplicate, gap, bad code or clock fault that moves a day | no, a per-measurement inversion of the relation across three files | no, the visit log and the register are the station's own records, kept to run the gauge | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "calendar day, local time" | Pacific Daylight Time days | the logger's standard-time days | same call | same call |
| SF2 | the minimum's change days (1 July, 1 October) | each day's own minimum | the next day's | same call | same call (those days sit 6 per cent or more clear) |
| SF3 | "below the minimum" | strictly below | at or below | same call | same call |
| SF5 | the shift's timing | from the storm's peak | prorated from measurement to measurement | same call | same call |
| SF6 | the shift's form | a stage correction | a flow ratio | same call | same call |
| SF7 | the shift's level | the post-storm measurements' mean | each measurement's own | same call | same call |
| SF8 | the measurements before the storm | no shift (within 0.4 per cent) | their own small shifts prorated | same call | same call |
| SF9 | flows above the table (4.00 ft) | the memo's high-water segment | the table's law, slope or top extended | same call | same call (the call never reaches 4 ft) |
| SF10 | "daily mean flow" | mean of the 10-minute flows | flow at the day's mean stage | same call | same call |
| SF11 | "flow in the bypassed reach" | gauge BP-1 | a point further down | same call | monitoring plan section 1: BP-1 is "upstream of any tributary inflow" |
| SF12 | "each deviation period" | a run of consecutive deviation days | a calendar month | same call | same call |

## Ladder

| Rung | Route | Answer | Dies to | Carrying files |
|---|---|---|---|---|
| 0 | Rating 7 on the stage record | no deviation | four post-storm measurements 11.7 to 17.4 per cent below the rating at their gauge heights | register, visit log |
| 1 | the days a measurement fell below the minimum | 29 July, 25 August, 6 October | Article 403 counts every day's mean, and the held stage is the same on every day between visits | license, stage record |
| 2 | the measured relation from the storm's peak | 29 July to 13 September, 21 September to 31 October | (golden) | stage, register, visit log, memo |

- **Margins:** on the golden every day sits 6 per cent or more from its minimum (the held flows 46.1 cfs in August
  against 50, 27.0 in October against 30); on Rating 7 every day sits above it by 6 per cent or more (53.8 cfs the lowest
  July to September day).
- **Worth of the decisive step:** about 8 cfs on every held day from 29 July (4 cfs under the minimum against 4 over), 88
  days and about 600 acre-feet of shortfall.
- **Pricing sequence:** (1) the residue the WHAT leaves is the stage-discharge relation each interval is converted on,
  a method the measurements decide, with no knob: every member that uses the measurements files the same periods; (2)
  the call needs the held flow down 4 cfs and the moved control takes it down 8; (3) the one-step route is the table
  lookup and files none; (4) the measured relation has a standard error of a few tenths of a cfs at the held stages
  against a 4 cfs margin; (5) the answer is a verdict per day 6 per cent or more from its line; (6) the pre-storm days
  are the unit's own history and every one passes on both relations; (7) the subset the step uses, the four
  post-storm measurements, hands nothing over by itself: no column compares them with the rating; (8) the reflex sweep
  runs in `checks.py` (R3b, G2, G3, SF5 to SF10).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every local calendar day of the season | Article 403; the record covers 1 July to 31 October |
| 2 Unit of account | the day's mean flow at BP-1 | Article 403 |
| 3 Attribution window | local calendar days | Article 403; SF1 same call |
| 4 As-of dating | the season as recorded to 4 November | one export, nothing later |
| 5 Version basis | Rating 7, the measurements of 2026 | C1: every measured-relation member files the same call |
| 6 Denominator | none (a daily mean against a minimum) | Article 403 |
| 7 Weighting | equal 10-minute intervals | SF10 same call |
| 8 Window length | one calendar day | Article 403 |
| 9 Boundary inclusivity | below the minimum | SF3 same call |
| 10 Rounding path | flows to whole cfs, volumes to the nearest 100 acre-feet, at the close | the prompt; A2 to A4, A8 assert the bins |
| 11 Tie-break | none | no day within 6 per cent of its line |
| 12 Maturity and censoring | the season closed on 31 October | the record runs to 3 November |
| 13 Order of operations | relation first, then daily means | SF10 same call |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | none present | the stage record carries one row per interval |
| 16 Identity normalisation | one gauge, one station id | the register |
| 17 Netting against gross | a day's deficit is not netted against another day's surplus | Article 403 counts each day |
| 18 Dimensional units | feet, cfs, acre-feet (1.98347 per cfs-day) | the register and the license |
| 19 Code and status semantics | none decisive | the visit log's remarks state facts only |
| 20 Integerisation | whole cfs at the close | the prompt |
| 21 Clause scope | Article 403 per day, Article 404 May and June | the license |
| 22 Forward window contents | none | retrospective: the season the license measures is closed |

## Literal reader

Executed word for word, Article 403 marks a day whose mean flow in the bypassed reach is below its minimum, the plan
computes that flow from BP-1's stage record by standard USGS methods, and on the measured relation (Rating 7 to the
storm's peak, a 0.10 ft stage correction after it) every reasonable member files 29 July to 13 September and 21
September to 31 October; every other reading of a term is SF1 to SF12, each the same call or ruled out by a quoted
sentence.

## Oracles

- `reports/2025_annual_flow_compliance_report.pdf`: last year's record on Rating 7, compliant; true of 2025, ties under
  every route for 2026 (it carries no 2026 figure).
- `gauge/bp1_rating7_report_2023.pdf`: its 17 measurements validate Rating 7 to 2023; ties under every route.
- `operations/bypass_release_log_2026.csv`: setpoints in rated cfs; ties under every route (the controller held them).
- No control ties only under the golden; no computed flow ships.

## Ask sheet

- **Ask A, the May and June bypass volumes** (two figures, nearest 100 acre-feet). H18 home: Article 404's report, part
  of the same filing. Primary device (D7, the true relation elsewhere): the register's expanded table stops at 4.00 ft,
  and the high-water segment that converts the freshet's stages above it is an equation in the consultant's 2023 memo;
  extending the table by its own law, its last slope or its top value files every one of them wrong. Hazard: standard
  time against local days (moves nothing at the nearest 100). Path: stage record, register, memo: 3 files, 4 columns.
  Pin test: the license fixes the months and the unit; no pin names the high-water segment.
- **Ask B, the spring peak flow and its time** (whole cfs, local time). Same home and primary; second device (D8): the
  logger's standard-time clock against the local time the report gives. Path: stage record, register, memo.
- **Zero-counts:** high-water rows among the deviation days the call reads: 0 (A6).
- **Hazard table:** standard time moves Ask B's time and no call; the table's extension moves Ask A and Ask B and the two
  storm days in the record.
- **Referee:** none.

| Cracker sheet | Figures | Cracker keeps | Verdict |
|---|---|---|---|
| Ask A, May and June volumes | 2 | 0 of 2 | miss |
| Ask B, spring peak flow | 1 | 0 of 1 | miss |

- Mirror leakage: 0.0 per cent of ask weight (the mirror, on Rating 7 throughout, extends the table as the cracker does)
- Pair ceiling: 27.0 (cracker 44.8 on the call with the daily record, mirror 9.1); the full includer that also takes the
  memo's high-water segment scores 100.0 and the pair with it on the call is 54.6
- Measured by: generator/ceiling.py

## Pre-ship check

- [ ] precut.py exit 0; checks.py and verify.py green; two byte-identical builds; figures_check.py exit 0
- [ ] leak.py on the cut pack; scrub audit; guard.py surface and heart; the card current
- [ ] golden-realism on both deliverables; submission.md from figures.json
- leak.py REVIEW, sweep 3: 403 and 404 are the license's article numbers in the license, the plan and the 2025
  report; 142 is a 2022 measurement in the 2023 memo's table; harmless.
- leak.py REVIEW, sweep 3: the 2025 report shares the call's words because it is last year's filing of the same
  article, true of 2025 and carrying no 2026 figure; harmless.
- leak.py REVIEW, sweep 4: the memo's and the plan's shared words (rating, measurements, station, control, method) are
  their genre's own nouns; neither names a shift, the storm's effect or the rating's error; harmless.

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
- 2026-11-04, at the hand-off: the final pull brought task462 v2 (registered 08:40:22Z, before this card) into the window, and `guard.py heart` BLOCKed on ban.org_family (utility_or_infrastructure); the organisation axis was redrawn (the licensee is the paper mill that owns the project, manufacturer) and the Gate G mechanism moved to signal_vs_noise_or_hold, which also cleared the surface screen's same-driver promotion against task274.
