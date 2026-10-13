# task187 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task187.json`, architecture v1, drawn 2026-10-13 from seed AD10 (which
  turbine gets next summer's one leading-edge repair campaign, and the energy it recovers). The world, the decision and
  the quantity are the seed's; the seed's pitfall (following a rotor through the crane lift log) is a reading and sits on
  a lower rung only. The decisive pitfall is re-found from the turbines' ten-minute record.
- **Pairing:** Energy Systems & Utilities, `grid-reliability-outage-analysis` (the task type in this domain serving
  Anomaly Detection & Diagnostics), read as a generator's lost-production accounting: each turbine's shortfall split
  into downtime, curtailment and performance, and the performance shortfall split into what the blades cost and what the
  turbine's place costs. The anomaly is a real aerodynamic loss separated from an apparent one.
- **Niche:** Cairnhollow Community Energy, a community benefit society, owns and runs the ten-turbine Cairnhollow
  Community Wind Farm on an upland moor with a conifer plantation along its western edge. Its rope-access contractor can
  run one leading-edge repair campaign in summer 2027, on one turbine's blades; the society's O&M standard values a
  campaign by the energy the repaired blades recover over the twelve months after it.
- **Forcing and forum:** the summer weather window for rope access (`season_or_peak`); the society's board books the
  campaign (`board_of_directors`); the organisation is a generator (`utility_or_infrastructure`); the requester is the
  asset manager (`operations_director`).
- **Call:** the turbine whose blades are repaired, and the energy the repair recovers over the twelve months after it.
- **Shape 14** (cuts of a distribution by segment): each of the ten turbines carries its lost energy in the twelve
  months by cause, downtime and grid curtailment (20), the call and the recovered energy (2), a chart with named parts
  (4), files and units (3). Criteria arithmetic: 29.
- **Strategy and mechanism:** `decomposition_attribution` (a turbine's shortfall split into the part the repair
  recovers and the part its place costs, where the curve's shape decides the split); gap population then objective (a
  ten-minute record is a curve averaged over the wind's spread inside the ten minutes, not the curve at the mean wind;
  and the metric reported, the shortfall against the warranted curve, is correct and is not what the campaign recovers);
  decisive generator G2 (grain), G17 supporting, G4 on the lower rung (the rotor exchange); Gate G
  `decomposition_attribution`; calibration `none`.
- **Data-native sentence:** a ten-minute mean power is the turbine's capped, steeply curved power curve averaged over
  the gusts inside the ten minutes, so a turbine standing in the plantation's eddies, at about twice the farm's
  turbulence, produces less near rated power and more at low wind than its blades alone would give; its shortfall
  against the warranted curve is turbulence, which no blade repair touches.
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
  the grid operator's curtailment report, an asset register, a crane lift log by position code, a site layout, the
  warranted power curve) and the decision. Wind power-performance practice (IEC 61400-12-1, its Annex M turbulence
  normalisation; IEC 61400-26 production-based availability) gives the field's method. The client's two-layer example,
  "comparing against the right group, not a simple before and after", is the lesson, carried here by matched turbulence.

## Default path

1. Read the O&M standard: a campaign is valued by the energy the repaired blades recover over the twelve months after
   it, measured on the turbine's last twelve months of normal operation.
2. Clean the ten-minute record: keep the intervals the turbine's state code gives as normal operation, drop the
   intervals under a curtailment setpoint and the icing episodes, align the SCADA's local time with the met mast's UTC,
   correct the wind for air density from the mast's temperature and pressure, and keep for the turbine with the rotor
   exchange only the months since its present rotor went up (the lift log by position code, through the site layout).
3. Build each turbine's power curve by wind-speed bin and its energy shortfall against the warranted power curve over
   its year of wind.
4. Book the campaign on the turbine with the largest shortfall, and take that shortfall as the energy recovered.

Ends on: the plantation-edge turbine.
Golden: the turbine whose blades are eroded.

Every figure is the prototype's until the generator asserts the built values.

## Stump sentence

The default path ranks the turbines by their energy shortfall against the warranted power curve after cleaning the
record, which reads the plantation-edge turbine's turbulence loss near rated power as blade erosion and books the
campaign on the plantation-edge turbine; the shortfall at matched turbulence leaves that turbine sound and names the
turbine whose blades are eroded, losing about five per cent of its power below rated.

## Three rules

- Task type: energy-systems-utilities / grid-reliability-outage-analysis, which serves anomaly-detection; the build
  separates a generator's real performance loss from an apparent one, inside its lost-production accounting.
- Domain test: the deciding quantity is the energy each rotor's blades lose to leading-edge erosion, measured as the
  power-curve shortfall at matched inflow (the turbulence normalisation of a ten-minute power curve in IEC 61400-12-1
  Annex M), because a ten-minute mean power averages a capped cubic curve over the turbulence inside the interval.
- Swap: put clinics and visits, or pumps and flows, in place of turbines and wind and the task dissolves: there is no
  capped cubic curve averaged over a per-unit turbulence, so no shortfall that turbulence alone creates near a cap and
  reverses at low input; the deciding effect is the wind turbine's own.
- Layer 1: the SCADA's local time against the met mast's UTC across the clock changes (how the two loggers store
  time); turbine state codes, curtailment setpoints and the grid operator's monthly curtailment shares by connection;
  winter icing; air density from the mast; a rotor exchange recorded by the crane contractor under position codes, with
  the site layout and the asset register. None is placed to be caught; each is asserted neutral for the call.
- Layer 2: estimand_identification, what a clean rotor would produce in the same turbulence, the counterfactual the
  shortfall must be measured against for the repair's energy.
- Decisive step: comparing each rotor's power with the warranted curve at matched turbulence (normalising each ten-minute
  record to the warranted curve's turbulence, or comparing within turbulence bins) instead of at matched mean wind only.
- Not semantics: every field, code and unit (state codes, setpoints, UTC, density, the lift log's position codes, the
  rotor serials) is read the same on the easy route and the golden one; a reader who reads them all correctly and ranks
  the shortfall at matched mean wind still books the plantation-edge turbine.
- Not rule application: the O&M standard files the value of a campaign (the energy the repaired blades recover) and the
  normal-operation filter, but no filed rule says how turbulence enters the comparison; executing every stated rule with
  the binned shortfall still books the plantation-edge turbine.
- Analyst test: a strong analyst who cleans the ten-minute record (normal operation, curtailment, icing, air density, the
  March rotor exchange) and ranks each turbine's energy shortfall against the warranted power curve books the campaign
  on the plantation-edge turbine, not the turbine whose blades are eroded.
- Estimand: the O&M standard's valuation sentence (the energy the repaired blades would add over twelve months of the
  turbine's normal operation, on its last twelve months of wind), in the O&M standard.
- No decoy: no memo, report or stakeholder figure names a turbine for the campaign or states a shortfall; the monthly
  production report answers how much each turbine produced and ranks nothing on blade condition.
- No certified replay: no certified or published figure is reproduced to recover the method; the comparison at matched
  turbulence comes from the record itself.
- Lesson: a record that averages a curved, capped response over a spread carries the spread into its level, so units in
  different spreads cannot be compared at matched mean input alone; no build on file teaches the averaging interval's
  own effect on a unit's curve (19 Anomaly Detection drivers read above).

## Tried and rejected

- The seed's pitfall, following the eroded rotor through the crane lift log to its present turbine, as the decisive
  step: a reading of the lift log, the position codes and the register (identity resolution); it stays as the lower
  rung.
- Wake shadow (a turbine's shortfall against the met mast in waked sectors) as the decisive step: a power curve on the
  turbine's own nacelle anemometer absorbs the wake's lower wind and finds the eroded rotor directly, so the easy route
  lands for any analyst using the nacelle wind.
