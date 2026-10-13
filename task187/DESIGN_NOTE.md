# task187 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task187.json`, architecture v1, drawn 2026-10-13 from seed AD10 (which
  turbine gets next summer's one leading-edge repair campaign, and the energy it recovers). The world, the decision and
  the quantity are the seed's; the seed's pitfall (following a rotor through the crane lift log) is a reading and sits on
  a lower rung only. The decisive pitfall is re-found from the turbines' ten-minute record.
- **Pairing:** Energy Systems & Utilities, `grid-reliability-outage-analysis` (the task type in this domain serving
  Anomaly Detection & Diagnostics), read as a generator's lost-production accounting: each turbine's year split into
  downtime, grid curtailment and performance, and the performance shortfall split into what the blades cost and what
  the turbine's inflow costs. The anomaly is a real aerodynamic loss separated from apparent ones.
- **Niche:** Cairnhollow Community Energy, a community benefit society, owns and runs the ten-turbine Cairnhollow
  Community Wind Farm (ten Hallvard H93-2.3, 2.3 MW, 93 m rotor, 80 m hub, commissioned 2014) on an upland moor in
  two rows: a west row facing a mature conifer plantation along the western edge (CH01, CH05 and CH07, the last nearest
  the trees) and a loch (CH02), and an east row standing in the west row's wakes in westerly winds (CH03, CH04, CH06,
  CH08, CH09, CH10; CH04 three and a half rotor diameters downwind of CH02). Its rope-access contractor can run one
  leading-edge repair campaign in summer 2027, on one turbine's three blades; the society's O&M standard OM-07 values a
  campaign by the energy the repaired blades add, measured on the turbine's last twelve months of normal operation.
- **Forcing and forum:** the summer weather window for rope access (`season_or_peak`); the society's board books the
  campaign in November (`board_of_directors`); the organisation is a generator (`utility_or_infrastructure`); the
  requester is the asset manager (`operations_director`).
- **Call:** the turbine whose blades are repaired, and the energy the repair recovers over the twelve months after it.
- **Shape 14** (cuts of a distribution by segment): each of the ten turbines carries its energy lost to downtime and to
  grid curtailment over October 2025 to September 2026 (20, nearest MWh), the call and the recovered energy (2, the
  energy to the nearest 50 MWh), a chart of both losses by turbine with named parts (4), files and units (3). Criteria
  arithmetic: 29.
- **Strategy and mechanism:** `decomposition_attribution` (a turbine's shortfall split into the part the repair
  recovers and the part its inflow costs, where the power curve's shape decides the split); gap population then
  objective (a ten-minute record is the power curve averaged over the wind's spread inside the ten minutes, not the
  curve at the mean wind; and the metric reported, the shortfall against the warranted curve, is correct as a shortfall
  and is not what the campaign recovers); decisive generator G2 (grain), G17 supporting, G4 on the lower rung (the
  rotor exchange); Gate G `decomposition_attribution`; calibration `none`.
- **Data-native sentence:** a ten-minute mean power is the turbine's capped, steeply curved power curve averaged over
  the gusts inside the ten minutes, so a turbine in the plantation's eddies produces less near rated power and more at
  low wind than its blades alone would give, a turbine in a neighbour's wake is lifted at low wind, and the turbine
  facing the loch, in the smoothest air on the site, falls short at low wind; each turbine's shortfall against the
  warranted curve mixes its blades with its inflow, and only the comparison at its own turbulence leaves the blades.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 19 builds): 25 a second-source inflow; 28 a
  reachable share; 33 forward yield cut by an intervention; 48 a two-sided pair grain; 54 exposure in custody; 68 a
  matched panel through identity successions; 76 a zero-conversion look-back class; 85 a unit's own window; 103 a
  fan-out through authorisations; 104 a self-adapting scorer replayed; 119 waits a unit could shorten; 182 a lagged
  response to a shared driver; 183 repeat failers in parts; 125 a recruitment filter carried through; 180 detection by
  quiet hours; 181 crossings of moving units; 184 host stand-down; 185 a reading-dependent instrument conversion; 186
  an own-history null under shared local cycles. None takes out an effect the averaging interval builds into each
  record; none turns on a capped curve averaged over a per-unit spread.
- **Guard:** WARN `overuse.objective` (this lane) and `repeat.decision` (a pick is the seed's decision: one campaign,
  one turbine). NOTE same driver key as task48, differentiated on the card (task48 regroups transactions to a pair grain;
  task187 keeps the turbine grain and takes out the averaging's turbulence effect). Nearest drivers 0.05 (task500 v3, a
  matched-reference change effect; task184, host stand-down; task115, a second response at a rival's level): the
  abstraction test maps none onto this driver.
- **Sources:** the seed (AD10) gives the world (ten turbines of one model, a rope-access campaign, SCADA, a met mast,
  curtailment, an asset register, a crane lift log by position code, a site layout, the warranted power curve) and the
  decision. Wind power-performance practice gives the field's method: IEC 61400-12-1 (the method of bins, Annex A's
  disturbed sectors, Annex M's turbulence normalisation) and IEC 61400-26 (production-based availability, lost
  production by cause). The client's two-layer example, "comparing against the right group, not a simple before and
  after", is the lesson, carried here by the comparison at matched turbulence. Turbulence physics: the Gaussian
  averaging of a zero-turbulence power curve over a ten-minute spread (Annex M), the Frandsen wake-added turbulence and
  the Jensen wake deficit.

## Default path

1. Read OM-07: a campaign is valued by the energy the repaired blades add over the turbine's last twelve months of
   normal operation (running or waiting for wind), and a blade set that went up within the twelve months is measured
   on its own months.
2. Clean the ten-minute record: keep normal operation, set aside power-limited, iced, faulted, serviced and stopped
   intervals, join the met mast for air density and correct the nacelle wind to standard density, and take CH09's
   months since its present rotor went into service on 25 April 2026 (the crane lift log by pad code, through the site layout).
3. Build each turbine's power curve by the method of bins (0.5 m/s bins of density-corrected nacelle wind) and its
   energy shortfall against the warranted power curve over its year of wind.
4. Book the campaign on the turbine with the largest shortfall, and take that shortfall as the energy recovered.

Ends on: the plantation-edge turbine.
Golden: the turbine whose blades lose the most at matched turbulence.

Every figure is the prototype's until the generator asserts the built values.

## Stump sentence

The default path ranks the turbines by their energy shortfall against the warranted power curve after cleaning the
record, which reads the plantation-edge turbine's turbulence loss near rated power as blade erosion and books the
campaign on the plantation-edge turbine; the shortfall at each turbine's own turbulence leaves it sound and names CH04,
whose blades lose about 2.4 per cent of their power below rated (89 MWh over the year), a loss its neighbour's wake
hides at low wind.

## Three rules

- Task type: energy-systems-utilities / grid-reliability-outage-analysis, which serves anomaly-detection; the build
  separates a generator's real performance loss from apparent ones, inside its lost-production accounting.
- Domain test: the deciding quantity is the energy each rotor's blades lose to leading-edge erosion, measured as the
  power-curve shortfall at each turbine's own turbulence (the turbulence normalisation of a ten-minute power curve in
  IEC 61400-12-1 Annex M, or the comparison within turbulence bins), because a ten-minute mean power averages a capped,
  near-cubic curve over the turbulence inside the interval.
- Swap: put clinics and visits, or pumps and flows, in place of turbines and wind and the task dissolves: there is no
  capped cubic curve averaged over a per-unit turbulence, so no shortfall that turbulence alone creates near a cap and
  reverses at low input; the deciding effect is the wind turbine's own.
- Layer 1: the SCADA export joins the site server's archive (UK local time, the October 2025 clock change's repeated
  hour) to the hosted platform's export from 3 February 2026 (UTC) in one timestamp column; the met mast's UTC
  interval-start stamps; turbine state codes, one power-limited state shared by the network operator's ANM limits and
  the planning condition's night-time noise mode on the four turbines nearest the village; silent intervals while a
  controller is isolated for service or a crane job, after a converter trip, during a site communications outage and
  during a grid loss; winter icing stops; the warranted curve as a table in a contract schedule. None is placed to be
  caught; each is asserted neutral for the call and the recovered energy's bin (the clock read either way, the repeated
  hour dropped, the mast's stamps read as interval ends). The rotor exchange recorded by the crane contractor under pad
  codes is the lower rung R0', not Layer 1.
- Layer 2: estimand_identification, what the same turbine would produce in the same winds with its blades as new, the
  counterfactual the shortfall must be measured against for the repair's energy.
- Decisive step: comparing each turbine's power with an as-new turbine at its own ten-minute turbulence (normalising
  each record to the warranted curve's turbulence with the nacelle anemometer's standard deviation, or comparing within
  turbulence bins) instead of at matched mean wind only.
- Not semantics: every field, code and unit (state codes, the power-limited state, UTC and local time, density, the lift
  log's pad codes, the rotor serials) is read the same on the easy route and the golden one; a reader who reads them all
  correctly and ranks the shortfall at matched mean wind still books the plantation-edge turbine.
- Not rule application: OM-07 files the value of a campaign (the energy the repaired blades add, in the same winds) and
  the normal-operation filter, but no filed rule says how turbulence enters the comparison; executing every stated rule
  with the binned shortfall still books the plantation-edge turbine.
- Analyst test: a strong analyst who cleans the ten-minute record (normal operation, curtailment, icing, air density, the
  April rotor exchange) and ranks each turbine's energy shortfall against the warranted power curve books the campaign
  on the plantation-edge turbine, not CH04, whose blades are eroded.
- Estimand: OM-07's valuation sentence (the energy the turbine would have produced over its last twelve months of normal
  operation, in the same winds, had its blades been as new, less the energy it produced), in the O&M standard.
- No decoy: no memo, report or stakeholder figure names a turbine for the campaign or states a shortfall; the monthly
  production report answers how much each turbine's counters recorded and ranks nothing on blade condition.
- No certified replay: no certified or published figure is reproduced to recover the method; the comparison at matched
  turbulence comes from the record itself.
- Lesson: a record that averages a curved, capped response over a spread carries the spread into its level, raising it
  where the curve bends up and lowering it near the cap, so units in different spreads cannot be compared at matched
  mean input alone; no build on file teaches the averaging interval's own effect on a unit's curve (19 Anomaly Detection
  drivers read above).

## Readability screen

The six tests per rung (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear), verdict last.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0' the whole year's shortfall against the warranted curve | OM-07's blade-set sentence sends the solver to the lift log | the lift log's pad codes and the layout's pads | no | no | no | a sum per bin | readable |
| R0 the shortfall against the warranted curve at matched mean wind, the rotor exchange handled (the default path) | OM-07 values the energy the blades add | the warranted curve and the SCADA | yes | no | no | one subtraction per bin | readable |
| R1 the partial-load deficit (power or power coefficient below rated), the erosion signature | no | no | yes, for an analyst who knows erosion acts below rated | no | no | a ratio per bin | readable |
| R1b disturbed sectors excluded (Annex A), the mast's turbulence used to normalise, the mast's wind used as the turbine's (each files CH07) | no | the layout's coordinates | yes | no | no | no | readable |
| R2 (decisive) the shortfall at each turbine's own ten-minute turbulence (Annex M normalisation on the nacelle anemometer's standard deviation, turbulence bins against the fleet, or the records in the fleet's usual turbulence) | no: OM-07 values the energy in the same winds and names no turbulence | no column holds a turbulence intensity; the nacelle wind's standard deviation is an ordinary SCADA channel | no: the reflexes land CH07, CH02 or CH06 | none ships | the battery is clean on every path | no: a per-record expectation or a two-way binning | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | normal operation | ten-minute intervals in state 10 (running) or 20 (waiting for wind) | state 10 only; states 10, 11 and 20 (power-limited kept) | state 10 only: same call, same bin (asserted); power-limited kept: CH08, a noise-mode turbine's limit read as blade loss (the default stays CH07) | OM-07 3.1, the normal-operation sentence |
| SF2 | the blades as new | the same turbine in the same winds, turbulence included, with only the blades changed | the warranted curve at the measured mean wind (the default path) | CH07 | OM-07's valuation sentence (in the same winds, the blades alone as new) and the record: CH07 runs above the warranted curve between 5 and 9 m/s, which no blade does |
| SF3 | the turbine's wind | the nacelle anemometer's density-corrected ten-minute mean | the met mast's wind | CH07 (every turbine 110 to 840 MWh short) | the valuation sentence: the mast's wind charges the wakes, the terrain and the plantation's slower air to the blades, which the repair does not change |
| SF4 | the turbulence | the nacelle anemometer's standard deviation over its mean, each record | the mast's turbulence intensity | CH07 | the valuation sentence: the same winds are the turbine's own; the mast does not see the plantation's eddies at CH07 |
| SF5 | density correction | the wind normalised by the cube root of the density ratio, as OM-07 4.6 writes it | no correction | same call, the energy off its bin (every turbine 50 to 200 MWh short at a site density of 1.19) | Schedule 3 states the curve at 1.225 kg/m3 |
| SF6 | the twelve months | the ten-minute intervals ending 1 October 2025 to 30 September 2026 | calendar months by UTC or by local time at the edges | same call, same bin (asserted) | the extract and OM-07's twelve months, and same call |
| SF7 | a blade set changed within the year | CH09 measured from 25 April 2026 (its present rotor) | CH09's whole year | CH09 (its old rotor's erosion) | OM-07's blade-set sentence |
| SF8 | the method of bins against per-record interpolation | either | either | same call, same bin (asserted) | same call |
| SF9 | the matched-turbulence method | Annex M normalisation on the mast's turbulence (89 MWh) | Annex M on the site's typical turbulence or a flat 10 per cent (89, 116); turbulence bins of 0.25 or 0.5 m/s by 0.01 to 0.05 against the fleet's mean, median or the sound turbines' mean (24 variants, 80 to 90); the records in the usual turbulence scaled to the year (93) | CH04 every time, leading by 1.18x or more, every figure in the 100 MWh bin (asserted) | same call |
| SF10 | the SCADA clock for the mast join | local time to 3 February 2026, UTC after | local throughout; UTC throughout | same call, same bin (asserted) | same call |
| SF11 | the repeated October hour | both copies kept as two intervals | one copy dropped | same call, same bin (asserted) | same call |
| SF12 | the recovered energy's rounding | to the nearest 50 MWh: every matched-turbulence variant is 100 | whole MWh or the nearest 10 (the variants spread 80 to 116) | same call | the prompt |
| SF13 | the campaign | the three blades of one turbine | part of a rotor | same call | OM-07's campaign sentence |
| SF14 | the energy | the turbine's ten-minute active power over the interval | the export meter at the connection | same call | the export meter is the farm's, not a turbine's |

## Ladder

Built figures (seed 187), each asserted by name in `generator/checks.py`, MWh over the twelve months to September 2026.

| Rung | Construction | Campaign | CH07 | CH05 | CH01 | CH04 | CH02 | CH09 |
|---|---|---|---|---|---|---|---|---|
| R0' | the whole year's shortfall against the warranted curve at the same mean wind | CH09 | 235 | 114 | 115 | 93 | 71 | 369 |
| R0, the default path | the same, CH09 on its present rotor (OM-07 2.5) | CH07 | 235 | 114 | 115 | 93 | 71 | -3 |
| R1 | partial-load shortfall, 3 to 10 m/s (any cut from 3-5 to 8-12 m/s) | CH02 | -24 | -20 | -34 | 42 | 77 | -10 |
| R1b | disturbed sectors excluded; the mast's turbulence; the mast's wind | CH07, CH07, CH07 | 250, 225, 836 | 137, 107, 668 | 131, 109, 271 | 92, 85, 683 | 93, 64, 294 | 3, -5, 110 |
| R2, decisive | the shortfall at each record's own turbulence (Annex M on the mast's turbulence) | CH04 | 0 | 0 | 0 | 89 | 65 | 0 |

- **Kills, one fact each:** R0' by OM-07 2.5 and the lift log (a pool rotor went up on pad P08, CH09, in April 2026);
  R0 by the valuation sentence and the record (CH07, CH05 and CH01 run above the warranted curve from 4 to 8.5 m/s and
  below it from 9.5 to 12 m/s, and lose less than 1 MWh at their own turbulence); R1 by the same (CH02's partial-load
  deficit is mostly its low turbulence over the loch, and CH04's erosion is lifted out of sight below 8 m/s by CH02's
  wake); R1b because none of the three measures the turbine's own turbulence (the plantation is not a turbine, the mast
  is upwind of the eddies, the mast's wind charges wakes and terrain to the blades); R2 stands.
- **Why each is satisfying:** R0 is the textbook SCADA power-curve audit, cleaned by the book, with a 2.04x winner; R1
  is the erosion specialist's partial-load check; R1b is the power-performance engineer's sector screen.
- **Position:** CH04 is fourth on R0 (behind CH07, CH01 and CH05), fourth on R0', second on every partial-load cut
  (never first in 32 cuts from 3-5 to 8-12 m/s; the closest, 5 to 11 m/s, leaves it 1.01x behind), fourth on the sector
  screen, first only on R2. **Separation:** R0' CH09 over CH07 1.57x; R0 CH07 over CH01 2.04x; R2 CH04 over CH02 1.36x
  on Annex M and 1.18x or more on all 26 matched-turbulence variants.
- **Dominance:** at matched turbulence the default's winner keeps nothing (CH07 0 MWh), so the carried advantage is
  zero and CH04's edge (89 MWh) is the whole margin.
- **Grid:** the rotor exchange (handled or not) by the comparison (mean wind, partial load, sector screen, the mast's
  wind, the mast's turbulence, own turbulence): unhandled lands CH09 on the mean-wind and own-turbulence comparisons (its
  old rotor's erosion, 361 MWh at its own turbulence, is real at any turbulence); handled lands CH07, CH02, CH07, CH07,
  CH07 and CH04. Every cell but one is a named wrong answer.
- **Worth:** on the graded name, R2 moves CH07 to CH04; on the graded figure, the default files 235 MWh (250 to the
  nearest 50) on the wrong turbine, the golden 89 (100 to the nearest 50). CH04's own shortfall at the same mean wind
  (93) also rounds to 100: a solver who lands CH04 by the partial-load route without the decisive step would file the
  figure, but that route lands CH02.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | each turbine's normal-operation intervals in the twelve months; CH09 from 25 April 2026 | OM-07's normal-operation and blade-set sentences |
| 2 | Unit of account | the turbine (its three blades) | OM-07's campaign sentence |
| 3 | Attribution window | intervals ending 1 October 2025 to 30 September 2026 | the extract and OM-07; no campaign-relevant record within an hour of either edge moves a bin (C1) |
| 4 | As-of dating | the extract of 9 October 2026; the campaign is summer 2027 | the extract notes and OM-07 |
| 5 | Version basis | one SCADA export, the warranted curve of the supply agreement | none needed |
| 6 | Denominator | none: an energy, not a rate | none needed |
| 7 | Weighting | each ten-minute interval equally | C1 (bins or records give one figure, SF8) |
| 8 | Window length | twelve months | OM-07 |
| 9 | Boundary inclusivity | bin edges at multiples of 0.25 m/s off the centres | C1, same bin under either side (asserted) |
| 10 | Rounding path | the recovered energy rounded once, to the nearest 10 MWh | the prompt (SF12) |
| 11 | Tie-break | none needed | asserted: CH04 leads at matched turbulence by 1.8x |
| 12 | Maturity and censoring | the twelve months are closed | none needed |
| 13 | Order of operations | normal operation, density, turbulence, comparison, sum | C1 (SF5, SF9) |
| 14 | Row order | none affects a bin mean or a sum | C1 |
| 15 | Duplicate resolution | the repeated October hour is two intervals | C1 (SF11) |
| 16 | Identity normalisation | the lift log's pad codes to turbines through the layout | the site layout |
| 17 | Netting | turbulence gains at low wind and losses near rated net within a turbine's year | the valuation sentence (the blades alone) |
| 18 | Dimensional units | kW, m/s, degrees C, hPa, MWh | units in the data and the extract notes |
| 19 | Code and status semantics | state codes 10 and 20 are normal operation | the state code table and OM-07 |
| 20 | Integerisation | none | none needed |
| 21 | Clause scope | the blade-set sentence reads the blade set now fitted | OM-07 |
| 22 | Forward window contents | the twelve months after the campaign are valued on the last twelve months' winds | OM-07's valuation sentence |

## Literal reader

Executing OM-07 word for word: the twelve months, normal operation and the blade-set rule are filed and execute to one
set of intervals per turbine; the valuation sentence asks what the same turbine would have produced in the same winds
with its blades as new. The warranted curve is not that turbine in those winds: CH07 runs above it between 5 and 9 m/s
(no blade is better than new) and below it near rated, CH02 the other way, and the east row above it at low wind,
because each ten-minute power is the curve averaged over that interval's turbulence. The literal counterfactual is the
as-new curve averaged over each record's own turbulence, measured by normalising each record (Annex M) or by comparing
within turbulence bins; every such reading (SF9) names CH04 and files its energy inside one 10 MWh bin. The easy answer
comes only from the easy comparison on the same estimand.

## Oracles

- The monthly production report (each turbine's energy counters by month): it ties the ten-minute record's energy in
  every month but November 2025, whose counters carry the communications outage's production; it confirms no shortfall
  and ranks nothing on blade condition, the same on every path.
- The warranted power curve: every path uses it; it confirms nothing about turbulence.
- No published shortfall, campaign value or turbulence figure ships.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| D, each turbine's energy lost to downtime, October 2025 to September 2026 | 10, nearest MWh | the case's accounting of every candidate's year: what each turbine lost besides its blades | the board reads each turbine's year by cause beside the campaign | D4, a controller isolated for its annual service writes nothing: each service isolates the turbine twice, at the start straight from running (the record silent between a running row and a service row) and at the end before a restart to waiting for wind (silent between a service row and a waiting row); only the service work orders (isolation times) and the counters (no energy in those hours) show the turbine stopped | the site communications outage of 18 and 19 November 2025 (every turbine silent while running, the counters' energy shows it); the grid loss of 24 January 2026 (every turbine silent, stopped by the grid, neither downtime nor curtailment); the SCADA clock (the mast's wind joined an hour off) | SCADA states and power, mast wind, temperature and pressure, warranted curve, OM-07, work orders, production report, state code table, extract notes (8 files, 14 columns) | the states as recorded, silent intervals dropped (every turbine low, 4.6 to 66 MWh); states filled forward (every turbine low by its start isolation, 2.1 to 38 MWh); filled backward (every turbine low by its end isolation, 1.4 to 5.6 MWh); every silent interval counted (every turbine high by 40.5 MWh, the outage and the grid loss); the answer | a controller isolated for service records nothing, and a site switch failure silences every turbine while its counters run |
| G, each turbine's energy lost to grid curtailment over the same months | 10, nearest MWh | the same accounting | the same | D8, the SCADA platform moved on 3 February 2026 from the site server (UK local time) to the hosted platform (UTC), and the export joins both in one unlabelled timestamp column, while the network operator's ANM log is in UTC: read as local throughout, every instruction from 29 March 2026 sits an hour late (its first hour lost, an unlimited hour after it gained); read as UTC throughout, the October 2025 instructions sit an hour early; only the repeated hour at the October 2025 clock change, the missing nothing at the March 2026 change and the platform date in the extract notes place the switch | noise mode writes the same power-limited state as an ANM limit; ANM trips (export limit zero) write the external-stop state; the grid loss writes the grid state | SCADA timestamps, states and power, ANM log, mast, warranted curve, OM-07, state code table, extract notes (7 files, 13 columns) | the power-limited state read as curtailment (the six turbines without noise mode low by about 75 MWh, the trips; the four with it high by 78 to 182 MWh); the ANM log on the SCADA read as local throughout (every turbine low by 15.8 to 20.3 MWh); read as UTC throughout (every turbine low by 2.3 to 4.0 MWh, the October instructions); the answer | a SCADA migration to a hosted platform changes the clock, and noise mode and grid limits share a controller state |
| Chart, both losses by turbine | 4 named parts | the paper's exhibit of D and G | the board reads the year at a glance | inherits D's and G's devices | inherits their hazards | D's and G's paths | D's and G's stops on every bar | a board paper's standard exhibit |

- **Main population zero-counts:** the main call reads normal-operation rows (states 10 and 20) and the mast; no
  silent interval has a row; no ANM instruction, work order or counter is read by the main call; the clock moves only
  the mast join for density, asserted neutral (SF10); asserted by count in `checks.py`.
- **Hazard table:** the communications outage and the grid loss move D under "every silent interval counted" (every
  turbine, 40.5 MWh together); noise mode (CH06, CH08, CH09, CH10) and the 15 trips move G on the state path (every
  turbine); the clock moves D through the mast join in the months it misplaces (0.0 to 5.7 MWh, none relied on).
- **Referee:** the monthly production report arbitrates which silent intervals were running (D) and ties no ask figure.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| D downtime by turbine | fault, repair and service states as recorded, silent intervals dropped or filled forward | every turbine low by its isolation hours | miss |
| G curtailment by turbine | the ANM log joined to the SCADA read as UK local time throughout | every turbine low by the first hours of the April to September instructions | miss |
| Chart values | D's and G's cracker paths | every bar off | miss |

Mirror leakage: about 6 per cent of the ask weight (the chart's title and axis parts; every loss figure misses on the
default path, which shares the cracker's ask paths).
Pair ceiling: about 35 (the cracker at about 52 with the call and the chart's presence parts, the mirror at about 18).

## Build record

- **Generator:** `generator/build.py` (world, wind, ops, records, docs, analysis, deliver, checks, verify, metadata,
  postprocess); 14 files, 5 formats; SCADA 522,159 rows (52,560 intervals for ten turbines, less the silent intervals,
  plus the repeated October hour), mast 52,560 rows, 120 ANM instructions (15 trips, 18 before the October change).
- **checks.py:** 442 assertions, the three-rules block included (R1 the anemometer's deviation is the deciding input:
  with the mast's turbulence in its place the comparison files CH07; R2 the clock either way, the repeated hour and the
  mast's stamps leave the call and the 100 MWh bin; R3a the default on the clean truth files CH07; R3b the decisive step
  alone files CH04 and each lower rung's correction alone stays wrong; R3c no file names the campaign or a shortfall).
- **verify.py:** independent, from target/ only: call CH04 (88.9 MWh on Annex M, 83.2 on turbulence bins, 100 to the
  nearest 50), default CH07, runner-up CH02, farm downtime 1,417 and curtailment 2,979 MWh, every turbine's figures as
  the workbook states.
- **Two builds byte-identical**; target.zip cut from the final build; `figures_check.py` 55 of 55 figures in
  figures.json; containers clean on the scrub audit.
- **leak.py REVIEW lines, each harmless:** OM-07 carries most of the call's distinctive words (campaign, leading-edge,
  repaired blades, recover): it is the standard that governs the campaign and names no turbine or figure; OM-07, the
  schedule and the extract notes carry design-note words (warranted, ten-minute, record, standard, nacelle, layout):
  the domain's own vocabulary, none names turbulence or the comparison.
- **Guard:** heart WARN (objective overuse in the lane; a pick follows a pick); surface clean of promoted pairs, the
  company secretary's first name moved off one used in task108.

## Judge record

- **Pass 1 (stage 4):** DETERMINISTIC, APPROVE. The thread recomputed the blade loss three ways (Annex M at each
  record's own turbulence 88.9 MWh, fleet bins 82.8, bins against the four clean east-row turbines 88.1): CH04 first,
  CH02 second by 13 to 24 MWh, the energy 100 MWh to the nearest 50 every time; the default (Schedule 3 at the same mean
  wind) files CH07, 235 MWh, refuted by CH07's own curve signature. It derived the SCADA clock from the data (the mast
  correlation peaks at an hour's shift before the repeated October hour, at none after), reproduced all twenty lost
  production figures, and classified the outage and the grid loss from the export meter and the grid state. Gate G: no
  shipped artifact ranks the turbines on the campaign. Gate H: domain pass, layers pass, decisive step analytical.
- **Its optional pin, declined:** adding "wind speed and turbulence as recorded at the nacelle" to OM-07 2.4 would name
  the decisive quantity in the governing standard (readability test 1), turning the analytical step into a reading;
  the judge itself kept the verdict DETERMINISTIC without it, the data refuting the mean-wind reading (CH07 above the
  warranted curve from 4 to 8.5 m/s).
- Its realism note (CH08 and CH09 sharing a hub serial) was the reader's too, fixed before the verdict arrived.

## Pre-ship check

- Call: the 2027 campaign goes to CH04; its blades cost 89 MWh over normal operation in the twelve months to September
  2026 against the same turbine with blades as new at each record's own turbulence; 100 MWh to the nearest 50 MWh.
  CH02 second (65 MWh), every other turbine under 1 MWh.
- Default path: Schedule 3 at the same mean wind files CH07 (235 MWh, 2.04 times the next); the partial-load cut files
  CH02; the sector screen, the mast's turbulence and the mast's wind file CH07; the whole year files CH09.
- Gates: 443 checks with the R block, independent verifier, two byte-identical builds, figures_check 55 of 55, precut
  49/0, voice-check PASS, scrub clean, leak.py REVIEW (no LEAK), guard heart WARN (lane overuse, a pick after a pick),
  surface clean.
- Deliverables: le_repair_campaign_2027.pdf (two pages: the call, why not CH07, why not CH02 and how CH04's loss was
  hidden, CH09's exchange, the table, the lost production chart, notes), lost_production_2025_26.xlsx (twenty figures,
  the campaign sheet, notes); target.zip from the final rebuild, 14 files.
- Card current: answer, spine rows 522,159, stump and driver at the built values.

## Leak record

- **leak.py** (as-of 2026-10-09): REVIEW only. OM-07 carries the call's vocabulary (campaign, leading-edge, repaired
  blades, recover) as the standard that governs the campaign, naming no turbine and no figure; OM-07, the schedule and
  the extract notes carry design-note words that are the domain's own (warranted, ten-minute, record, standard,
  nacelle, layout). Both harmless, the reader agreeing.
- **Reader, pass 1:** question 1 none (OM-07 2.4 and 2.5 fix the estimand and leave the as-new reference open); question
  2 no file ranks the turbines on the campaign (the 2024-25 report ranks last year's downtime and curtailment, a
  declared distractor); question 3 none; question 4 nothing reads as the answer; question 5 OM-07 2.4 to 2.6 with 3.1:
  each turbine's normal-operation intervals in the twelve months, CH09 from its pool rotor, the as-new reference left
  to the analyst; question 6 an analytical choice (the as-new baseline), with 2.5 and 3.1 rule-following on lower rungs.
  Its realism findings, fixed in the generator: CH08 and CH09 shared a hub serial; CH09's register blades sat outside
  the farm's serial series; the serials ran too evenly; every corrective work order carried one summary; the crane log
  recorded the pool rotor's blade condition; the OM-07 revision entry named clause 2.5.
- **Reader, pass 2 (the changed files):** no decisive-step sentence, no pointer to a turbine, no repeated serial, no
  text written by someone who knows the answer; one shared commissioning date kept (one project, one handover).

## Tried and rejected

- The seed's pitfall, following the eroded rotor through the crane lift log to its present turbine, as the decisive
  step: a reading of the lift log, the position codes and the register (identity resolution); it stays as the lower
  rung.
- Wake shadow (a turbine's shortfall against the met mast in waked sectors) as the decisive step: a power curve on the
  turbine's own nacelle anemometer absorbs the wake's lower wind and finds the eroded rotor directly, so the easy route
  lands for any analyst using the nacelle wind.
- One eroded turbine in clean flow, with only the plantation-edge turbine against it: a partial-load comparison (power
  or power coefficient below rated) landed the eroded turbine, because turbulence lifts a ten-minute power at low wind;
  the eroded turbine now stands in a neighbour's wake, whose turbulence lifts its low-wind power, and the loch-facing
  turbine, mildly eroded in the smoothest air on the site, leads every partial-load cut.
- Wake turbulence as the default's lead (waked turbines first on the shortfall): a wake adds most turbulence at low
  wind, where it lifts power, so waked turbines run near or above the warranted curve and cannot carry the default.
- Erosion tapered to nothing at 13 m/s: unphysical; erosion is a constant fractional loss of the power coefficient up to
  rated, so its energy loss peaks just below rated.
- A 3.45 MW, 117 m turbine: ten of them is a large farm for a community society; ten 2.3 MW turbines (23 MW) is its
  scale.
- The recovered energy to the nearest 10 MWh: the defensible matched-turbulence readings spread from about 80 MWh
  (turbulence bins against a fleet holding the other eroded rotor) through 89 (Annex M) to 93 (a turbulence band) and
  116 (Annex M on a flat 10 per cent), three bins; to the nearest 50 MWh every one is 100.
- A flatter ambient turbulence (0.085 + 0.10/v): the Annex M fit lost the cut-in (2.5 m/s) and left the plantation
  turbines 10 MWh at their own turbulence; the site's turbulence falls with wind speed as the type test's does.
- Noise mode on every turbine in westerly nights: it took a fifth of the westerly records out of normal operation and
  handed the widest partial-load cut to CH04; the planning condition now covers the four turbines nearest the village.
- The limited state written only where a limit bound: the records kept near a cap were the ones below it, a selection
  that biased every comparison at matched turbulence; the controller now reports the limited state while a setpoint is
  in force.
- The ready state below 2.9 m/s whatever the turbine made: every turbine showed 3.6 MWh of loss against the as-new curve
  at low wind; ready now means the turbine made nothing.
- Annual services on any weekday pair: calm days left some turbines' isolations worth under 0.5 MWh, inside the
  rounding; the contractor now climbs in moderate wind (6 to 11 m/s over each isolation), as rope and climb rules
  require anyway.
