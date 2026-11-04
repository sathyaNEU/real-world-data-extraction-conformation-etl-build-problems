# task461 design note

Architecture 3, drawn 2026-11-04: a re-root of the number into a new world, dataset, generator and prompt shell.
Architecture 2 (a fuel terminal's 2026 loading VOC) died at the stage-4 determinism judge the same day and
architecture 1 (a battery's cycling threshold) at the 2026-11-02 re-check; each has its line in `## Tried and
rejected`, their build files are cleared from the folder and kept in history, and architecture 1's shipped pack stays
at the portal, pending. This build replaces it at ship. No seed: the world, the decision and the quantity are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task461.json`, architecture v3, registered 2026-11-04T05:38:59Z, v1 and
  v2 in its lineage with their fates. `guard.py check`: WARN only (Gate G etl_conformance and decision quantity_figure
  repeat task476 v3; answered here: the Gate G label is the honest one for a residual whose subtracted set is
  conformed from the meters' own data, on another driver in another domain).
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL. The call is read from a conformed set:
  the supplier's half-hourly settlement data for the building's import, the building management system's cumulative
  sub-meter registers, the meter register and the tenancy schedule conformed into the loan's base building electricity
  and its Scope 2 intensity, beside the building's Scope 1 lines (generator diesel, chiller refrigerant).
- **Why this cell:** the last three draws hold record linkage (task476 v3), groundwater exceedance (task193 v3) and
  grid reliability (task192 v4); architecture 2's card is spent and holds no axis. Emissions-inventory's twelve cards
  spend activity levels, rates by operating level, detection, leak dating, a control device's capped draw and (spent)
  a container's previous use; none subtracts a metered set whose members nest.
- **Forum and forcing event:** customer_or_counterparty (Corvane Bank, the lender) and audit_or_inspection (the
  facility's annual KPI verification). Organisation other (a listed office property trust); role portfolio_manager.
  Personas from `guard.py names --geo "United Kingdom" --seed 461`: Alice Evans (head of sustainability, signs the
  report), Kate Harding (facilities manager).
- **World:** Wexmoor Office Trust owns Pellow House, a fourteen-storey office tower in Wexmoor (a fictional northern
  English city), let floor by floor to seven occupiers with the roof licensed to Mastlink Networks for a mobile
  network equipment room. The trust's revolving credit facility with Corvane Bank is sustainability-linked: the
  margin steps up if the base building's Scope 2 emissions intensity for 2026 exceeds the schedule's target.
- **Forcing fact:** the KPI report for calendar 2026, verified in January 2027. The call is retrospective by nature: a
  covenant test reports the closed year. As of 15 January 2027 (the folder's assembly date, the `--asof` for
  `leak.py`).
- **Data-native sentence:** three occupiers fitted comms rooms on their own floors and each room's supply was metered
  by the landlord's building management system for the occupier's recharge, downstream of the occupier's own supply
  meter, so the register lists every tenancy meter at one level and the base building residual subtracts each room
  twice; the half-hourly registers show the hierarchy (each room's half-hours inside its tenancy's, both at zero when
  the June switchboard maintenance isolated that supply), while the roof licensee's equipment room, also a comms room
  by name, is a supply of its own.
- **Abstraction sentence:** "a remainder taken by subtracting metered parts double-counts the parts that sit inside
  other parts; the parts' own time series show which do." Nearest drivers on file at 0.06 (task471 v3 lineage,
  task270 v4 lineage), neither a hierarchy.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: estimand identification (which meters measure the
    estimand's subtracted set), the data's real structure.
  - `dataset-generation/references/layer1-messiness.md`: settlement periods on the local clock (46 and 50 on the
    change days), a building management system logging local time with the autumn hour twice and a server gap,
    registers in watt-hours on two older meters, a meter replaced under a new tag, a contractor's own plant codes.

## Default path

1. Conform the supplier's half-hourly settlement data into the building's monthly import (settlement date and period
   on the local clock).
2. Read each tenancy meter in the meter register from the building management system's cumulative registers at each
   month's local midnight boundaries (the replaced meter's two tags joined, the watt-hour registers converted).
3. Subtract every meter the register lists as a tenancy supply (the seven occupiers' meters, their comms rooms and the
   roof licensee's room) from the import, month by month, and sum the year.
4. Multiply by the schedule's conversion factor and divide by the schedule's net lettable area; set the intensity
   against the 2026 target.

- **Ends on:** about 15.8 kg CO2e per square metre for 2026, inside the 17.6 kg target.
- **Golden:** about 18.3 kg CO2e per square metre, over the target by about 0.7.

## Stump sentence

The default path subtracts every tenancy meter in the register from the building's import and files about 15.8 kg CO2e
per square metre for 2026, inside the loan's 17.6 kg target; three of those meters measure comms rooms that sit inside
their occupiers' own supply meters, so the default takes them out twice, and the base building's intensity is about
18.3 kg, over the target.

## Three rules

- **Task type:** emissions-inventory (Physical & Environmental Sciences), which the taxonomy tags for ETL: a building's
  Scope 2 and Scope 1 lines estimated from metered activity conformed across the supplier's settlement data, the
  building management system's registers, the meter register and the tenancy schedule.
- **Domain test:** the deciding quantity is the base building's electricity, worked the way an energy auditor works a
  sub-metered building: the building's import less each tenancy's supply, every supply counted once where it leaves
  the landlord's switchboard, with the metering hierarchy verified from the interval data rather than taken from the
  register's flat list.
- **Swap:** in a hospital's nouns ("the ward's cost less each department's metered cost") the sentence survives and the
  task does not: what decides here is that an electrical sub-circuit's half-hours sit inside its parent's and fall to
  zero when the parent supply is isolated, which no cost ledger has.
- **Layer 1:** settlement periods numbered on the local clock (46 on 29 March, 50 on 25 October); the building
  management system logging local time, the autumn hour twice, a nine-hour server gap; two older meters registering in
  watt-hours; a tenancy main replaced in August under a new tag; the generator tank dipped in millimetres; fuel
  dockets split across two notes; the refrigerant contractor's own plant codes. Each is what the producing system
  writes and none carries the call (asserted in checks.py's R2 block).
- **Layer 2:** estimand identification: the base building residual is defined on each tenancy's supply, and which
  meters are supplies is a structure of the metering the register does not record and the data show.
- **Decisive step:** take out of the subtracted set every tenancy meter whose half-hours sit inside another tenancy
  meter's (contained all year, and at zero exactly when that supply was isolated in the June maintenance), keeping the
  roof licensee's room, a supply of its own though named like a comms room.
- **Not semantics:** no field, code, unit or label records the hierarchy; every field read correctly (the register's
  descriptions, both clocks, the watt-hour registers, the replaced tag) still leaves the default at about 15.8 kg, and
  the names mislead both ways (a comms room that nests, a comms room that does not).
- **Not rule application:** the KPI schedule files the WHAT (the import less the electricity supplied to the tenancies,
  metered at each tenancy's supply, over the net lettable area, at the filed factor); executing it with the register's
  list files the default, and no rule says which meters are supplies.
- **Analyst test:** with the settlement data and the registers conformed and the KPI schedule applied, a strong analyst
  subtracts every meter the register lists as a tenancy supply from the import and files about 15.8 kg CO2e per square
  metre, inside the 17.6 kg target, because nothing asks whether one tenancy meter sits inside another.
- **Estimand:** the KPI schedule: Base Building Electricity for calendar 2026 (the building's local time) is the
  electricity imported through the revenue meter less the electricity supplied to the tenancies (every part let or
  licensed, the roof licence included) as metered at each tenancy's supply; its Scope 2 emissions at the schedule's
  factor; the intensity over the schedule's net lettable area; the target.
- **No decoy:** nothing is planted: comms rooms metered for recharge downstream of an occupier's supply are how fitted
  offices are wired, and the June maintenance isolates supplies because it tests the switchboard; no memo, prior
  report, draft or stakeholder figure ships.
- **No certified replay:** no certified figure carries a base building total; the energy performance certificate (a
  declared distractor) is an asset rating, not an operational figure.
- **Lesson:** a remainder after subtracting metered parts is only right when the parts are disjoint, and a flat meter
  list does not say whether they are; the interval data do. No build on file teaches it.

## Survivor anatomy

- **Actor:** pass. The deciding property, whether a tenancy meter sits inside another, has no column in any file: it
  is a relation between two meters' half-hourly series.
- **Link:** pass. The relation is between rows of one export under different tags, and no key, column or sentence
  pairs a comms room with its parent supply.
- **Reflex:** pass. The field's reflex (import less every listed tenancy meter) is rung 0 and files the `Ends on:`
  figure.
- **Back-test:** pass. The reflex passes the auditor's usual control: the tenancy meters sum to well under the import
  in every half-hour, so nothing looks double counted.
- **Second use:** pass. Every file the decisive step reads has its own use: the registers and the settlement data are
  the KPI's inputs on every path, the meter register is the recharge list, the tenancy schedule carries the lettable
  areas.
- **Shock:** pass. The nested rooms are three of eleven tenancy meters, ordinary loads running all year; nothing in
  the pack singles them out.
- **Pins:** pass. The schedule files the WHAT (import, tenancy supplies, area, factor, period) and no sentence names
  a comms room, a hierarchy or the maintenance.

## Tried and rejected

- 2026-10-15, draw: the seed's own stump, a replay grouped by UTC dates that moves the charge and discharge hours across
  the operating day. Rejected: catching the clock is reading a field correctly (data semantics), banned as the decisive
  step; the clocks stay as Layer 1 mess and must leave the call where it is.
- 2026-10-15, design: a mild 2026 that lowered every day's swing (the year's average spread 34 per cent under the
  others). Rejected: an average that low after seven flat years reads as a structural break, a defensible reason to
  keep the node's year, and the additive premium landed within a dollar of the golden's level; the windy year that
  widens the tail and keeps the average, with an earlier windy year that reverted, replaced it.
- 2026-10-15, design: the BMS's own cumulative cycle counter in the export. Dropped: it recovered the dropped hours'
  energy at the BMS's usable-energy denominator, a second recovery that disagreed with warranty 4.3 at two decimals.
- 2026-10-15, design: the node's spread exactly 2.2 times the hub's every day (correlation 1.000). Replaced by a daily
  congestion variation (the ratio's spread 0.25), which reads as a market and leaves every rung where it was.
- 2026-11-02, re-check under the new gates: architecture 1 found spent, no repair made. The node's-own-year reading is
  either refuted by the data, and then the standing family (every pooled extension, every persistence model fitted
  to the record) is unanimous on $20 and the golden is the field's textbook long-term correction applied as stated
  (the Reflex line fails, standing spread zero), or it stays open on the current stretch's persistence and is a fork
  whose only closing sentence names the record the step recognises (the fork-is-the-stump test). Either way a gate
  fails; the shipped cut also fails leak.py (the data dictionary and the manifest by name; metadata.json carrying 300)
  and precut (no Measured by line on the ask sheet), and guard heart now BLOCKs (same puzzle and same driver against
  task174, task178, task242 and task476, not caused by this re-check). The re-root is the orchestrating session's call.
- 2026-11-04, re-root: architecture 1 left as spent (above), its build files cleared from the folder (kept in
  history); architecture 2 drawn in Physical & Environmental Sciences on a new world, dataset and prompt shell, one
  architecture per world. The screens of this draw, each with a default path ending wrong, the swap test, the anatomy
  lines and the bin test on paper, follow; the thirteenth was priced in code and carded.
- 2026-11-04, screen 1, emissions-inventory, a river port's transit emissions from AIS speed over ground in a tidal
  current: for vessels holding their speed through the water the round trip's bias is STW^4 / (STW^4 - c^4), 1.006 at
  11 knots in a 3-knot current, so the decisive step is worth under one per cent (bin test dead); the current record
  would ship only for the step (dedicated organ) and its spread along the channel forks.
- 2026-11-04, screen 2, emissions-inventory, a landfill's methane with collection efficiency weighted by cover area
  against by modelled generation (young cells under daily cover generate most): the area weighting is the reporting
  rule's own formula, so filed it is an official decoy and unfiled the golden is a model of the measurement whose every
  input is a default (decay rate, generation potential, efficiency by cover), forking past the step's worth.
- 2026-11-04, screen 3, emissions-inventory, floating-roof landings at a tank farm: the level record against each
  tank's leg height on the register is a row predicate on two shipped columns, and landing losses are a named term of
  the field's own tank equations (readable, a reflex).
- 2026-11-04, screen 4, emissions-inventory, a flare's destruction falling at low vent-gas flow under minimum steam:
  the combustion-zone heating value test is the field's named check, and the abstraction equals task479 v7's (a control
  device's tested removal fails in the intervals where coincident flows breach its operating condition).
- 2026-11-04, screen 5, emissions-inventory, catalyst warm-up after cold starts at peaking engines: with the dosing log
  shipped the uncontrolled minutes are present in the records (rule application); without it the cool-down constant is
  a free parameter (Gate C).
- 2026-11-04, screen 6, emissions-inventory, a river's phosphorus load with storm hysteresis on the rising limb: the
  rating regression is the field's method and the limb term is a specification extension, closed as a class by the
  bin-test identity (determinism-check section 3).
- 2026-11-04, screen 7, payment-claims, a plan's cost per member month with capitated encounters at zero paid: paid zero
  beside the capitation flag is a column, and repricing at the fee schedule is a filed rule.
- 2026-11-04, screen 8, item-response-theory-test-equating, optional essay questions of unequal difficulty linked
  through the compulsory section: task450's driver (two groups that differ in instrument and in group, linked only
  through a shared subset).
- 2026-11-04, screen 9, seasonal-adjustment-official-time-series-production, traffic count expansion factors for short
  counts near a single facility: task474's driver (sites serving one facility follow its own schedule, which the
  reference sites never see).
- 2026-11-04, screen 10, data-integration, a plant's mass-balance reconciliation with meter errors correlated through a
  shared densitometer: finding a drifted shared instrument is a planted defect when it flips the call (Gate G), and the
  covariance is a fitted structure (Gate C).
- 2026-11-04, screen 11, emissions-inventory, ammonia from broiler houses on litter reused across flocks: the
  emission-by-litter-age curve is a fitted dose response (a model of the measurement), and the honest label
  composition_mix BLOCKs ban.strategy against task200.
- 2026-11-04, screen 12, emissions-inventory, ethylene oxide off-gassing from product after shortened aeration: the
  desorption needs two rate constants (heated aeration, ambient warehouse) fitted from residual tests (Gate C).
- 2026-11-04, prototype 1 of screen 13 (proto_switch.py, three seeds): a 22-set fleet put 363 ML of diesel through the
  bays and lifted the partner's petrol inside mixed trips, so the terminal-exports-only compartment history landed
  within 5 per cent of the dockets' (no rung) at volumes no regional terminal moves; retuned (proto_switch2.py) to six
  semi-trailers, three B-doubles and a five-trailer dedicated carrier, with the exchange as all-petrol trips: rung 0 at
  0.33 tonnes on the distillate bays, the exports-only history at 0.84 of the golden, every retail diesel load at petrol
  vapour at 1.89, the dockets' construction about 47 tonnes, the temperature convention inert (0.998), saturation 0.6
  at 0.60 of the golden, on three seeds.
- 2026-11-04, build: dockets stamped in UTC with the terminal on local time. Dropped: reading the UTC stamps as local
  moved every compartment's previous delivery by ten or eleven hours and left the release at 16.2 tonnes, inside the
  limit, so Layer 1 carried the call; the dockets now carry each time with its own offset.
- 2026-11-04, build: a fixed bin floor (0.01 t on every quarter, 0.06 kL on the first-half gains) chosen by hand.
  Replaced by the spreads the readings put on each figure, measured in checks.py (the equation's US-unit form and the
  exact gas constant on every loading figure; per-load rounding and the unrounded 54B VCF on every gain), with the
  world seed searched until every figure keeps its bin under them.
- 2026-11-04, build: the stock account and the tank method with five cells no device reached (TK-2 and TK-3 in the
  third quarter and TK-3 in the fourth, whose boundaries fall in standard time; TK-4 and TK-5, whose register entry was
  their whole 2026 history), so the careful route kept them. Re-sited onto the terminal's own records: VRU-1's absorber
  moved to TK-2 and TK-3 during three valve repairs (the shift log's line-ups), and the diesel tanks' vents changed in
  March and August (the work orders); the careful route now keeps none of the 25.
- 2026-11-04, build: the dispatch dockets read only by the decisive step (the second-use test). Given their own use: the
  petrol rack's loads on manual bills of lading during two controller faults, which the dispatch system holds and the
  terminal system never received, enter the stock account from the dockets; the delivery sites list, read by nothing,
  is declared a distractor.
- 2026-11-04, architecture 2 died at the stage-4 determinism judge (NOT_DETERMINISTIC, SEND_BACK; report in
  determinism_check_report.md): gates B, C and E on external dependency (the golden needed a previous-cargo
  displaced-vapour rule, the saturation factors 1.0 and 0.6 and the loading-loss equation, none in a shipped file, and
  protocol 4.4 read literally charged bays 4 and 5 at diesel's own vapour, the easy answer), nothing in the pack
  separated the readings (vr1_hose was Y on every petrol line and blank on every diesel one, a product flag, and bays
  4 and 5 had no measurement), and Gate H read the step as rule application bordering a withheld rule; the leak reader
  found the call decided by stated procedure and two ask devices stated in plain words (a shift log and a work order
  naming the gauging clock). Re-rooted, never resumed; the lesson carried into architecture 3: the filed WHAT executes
  literally to the golden, no filed sentence executes to the easy answer, the correction is forced by the shipped data
  with margin and needs no outside constant, and no log line or work order states a clock or unit convention.
