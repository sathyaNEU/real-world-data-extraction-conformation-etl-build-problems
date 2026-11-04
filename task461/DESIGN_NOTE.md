# task461 design note

Architecture 2, drawn 2026-11-04: a re-root of the number into a new client domain, world, dataset and prompt shell.
Architecture 1 (a battery's 2027 cycling threshold carried from a trading hub's long price record, General Statistics
& Data Science) was found spent at the 2026-11-02 re-check (its line in `## Tried and rejected`); its build files are
cleared from this folder and kept in history, and this build replaces it. No seed: the world, the decision and the
quantity are drawn new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task461.json`, architecture v2, registered 2026-11-04, architecture 1 in
  its lineage with its fate. `guard.py check` on the registered card: see the verdict line below; the two structural
  matches against older builds (task488, task308 v3) are differentiated on the card, and the WARN on Gate G repeating
  task200 is answered here: method_or_model_selection is the honest label (the field's per-product loading-loss
  equation against the compartment-state construction, the right one fixed by the field's own saturation factor for
  vapour-balanced service), in another domain and on another driver.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL. The task type serves ETL and DD; the
  objective is ETL because the call is read from a conformed return: two terminal automation exports across a July
  cutover, the dispatch system's delivery dockets, the tanker register and the vapour recovery unit's outlet log
  reconciled into the licence's annual return of VOC from product loading.
- **Why this cell, and why it is open:** the six ETL task types hold 68 cards, emissions-inventory 12 of them. Those 12
  spend the activity level (task470, task474, task480, task484), the rate against operating level (task459, task460,
  task478), detection and completeness (task452, task462), the dating of leaks found at inspection (task476, task487)
  and a shared control device's capped draw (task479 v7). None charges a release by a state the emitting container
  carries over from its previous use, and `guard.py slots` on the setting's nouns (switch, loading rack, vapour
  recovery, compartment, previous cargo, fuel terminal, petrol tanker) returns nothing on this ground.
- **Shape:** other, the return's grid (written out in `## Ask sheet` at stage 2): the year's loading VOC, whether it
  passed the licence's 20-tonne limit and by how much; the release at the vapour recovery stack and at each distillate
  bay in each quarter; the return's throughput section; the note's chart.
- **Strategy:** other (no vocabulary family is honest: each fill's release is a state its compartment carries from the
  previous delivery, rebuilt per load from a second system's record; not a mix shift or reweighting, not a grain or
  identity reading, not censoring). Gap objective (each load record is right about the liquid loaded and the release is
  scored on the vapour displaced), then population. Generators G14 (the release per litre conditioned on the
  compartment's previous delivery) decisive, G3 (the bay's record says diesel, the vapour that left was petrol) and G2
  (the emitting unit is the compartment's cycle from one delivery to the next load, not the load row) behind.
- **World:** Brennock Fuels (invented), a regional fuel distributor in Warrenby (a fictional Australian port city),
  owns the Warrenby terminal. Petrol bays 1 to 3 bottom-load through vapour collection to a carbon-adsorption vapour
  recovery unit, interlocked so no petrol loads while it is off; distillate bays 4 and 5 load diesel with no vapour
  collection. The retail fleet (six semi-trailers and three B-doubles) carries petrol grades and diesel to the
  distributor's metropolitan service stations, every petrol drop made through the station's vapour balance; under a
  supply exchange with Tarrant Energy part of the retail petrol is lifted at Tarrant's Selwyn Point terminal. Oakhurst
  Haulage, the contract carrier, takes diesel to farms and mines in dedicated trailers from bay 5, where retail trailers
  also load diesel when bay 4 queues. The Coastal Air Quality Authority's licence limits VOC from product loading to 20
  tonnes a calendar year and requires the annual return by 31 January.
- **Forcing fact:** the licence's return for 2026, due 31 January 2027. The call is retrospective by nature: a licence
  return reports the closed year, and whether the terminal kept within its limit is a fact about 2026.
- **Forum and forcing event:** regulator_or_inspector (the Authority receives the return), statutory_or_regulatory_filing
  (the return's due date). Organisation logistics_or_3pl (a fuel distributor's terminal and fleet); role
  operations_director (the terminal manager, who signs the return). Personas from `guard.py names --geo Australia --seed
  461`: Anna Gardner (terminal manager), Jeffrey Pruitt (dispatch manager).
- **Data-native sentence:** a multi-product retail fleet fills each compartment with whatever the next order needs, so
  about half of its diesel goes into compartments that last delivered petrol, and every petrol drop at the metropolitan
  stations runs through the station's vapour balance, which fills the emptying compartment with the station tank's
  saturated vapour; the distillate bays collect no vapour, so that petrol vapour leaves at the bay as the diesel goes in,
  while the terminal's own records hold each load's product and litres and never the vapour the compartment brought back.
- **Abstraction sentence:** "each transfer into a container releases what the container's previous use left inside it,
  so the release belongs to the pair (previous use, current fill) and not to the fill." Read against the approved and
  delivered builds it cannot be written of any: the nearest drivers on file (task184 v8 at 0.08, a container-level
  indicator saturating; task150 at 0.05, a carried member base) and the nearest by setting (task153, a yard island's
  draw capped at one tankful between visits) share a container word and no move.
- **Same-puzzle and same-driver:** gap objective, G14, quantity_figure, method_or_model_selection; the guard's two
  matches are older builds (task488's item difficulties seen through targeted members, task308 v3's units failing
  together), differentiated on the card; none in the last twelve.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: the field's own method done right (field_method); Physical &
    Environmental Sciences carries no client rigor cards, so the family comes from the five.
  - The field's reflex is the loading-loss equation of AP-42 Chapter 5.2 (release per litre from the saturation factor,
    the vapour pressure and molecular weight, the liquid temperature), with its saturation factors keyed to dedicated
    service; it is the opponent's first move, never filed in the pack.
  - `dataset-generation/references/layer1-messiness.md`: a system cutover with its layout and volume basis changed, clocks
    in UTC against local time across daylight saving, identifiers reissued at the cutover, an analyser swap in a
    monitoring log, product codes renamed.

## Default path

1. Conform the two terminal automation exports into one 2026 load register by bay, product and month: January to June
   in gross observed litres with a volume correction factor column and trailer plates, July to December in net litres
   at 15 C with the new system's tanker ids.
2. Take the petrol bays' release as the vapour recovery unit's measured outlet mass, summed from its 15-minute log (the
   ppm-as-propane months before the May analyser swap converted), as the return protocol files.
3. Charge each distillate bay by the field's loading-loss equation per product: litres loaded times the saturation
   factor for submerged loading in dedicated normal service (0.6) times diesel's true vapour pressure and vapour
   molecular weight from the protocol's vapour tables at the bay meter's temperature, over R times the temperature.
4. Sum the year and set it against the licence's 20 tonnes.

- **Ends on:** about 1.4 tonnes of VOC from loading in 2026, within the limit (the vapour recovery stack about 1.1,
  bay 4 about 0.1, bay 5 about 0.2).
- **Golden:** about 48 tonnes, over the limit by about 28 (bay 4 about 41, bay 5 about 6, the stack about 1.1).

## Stump sentence

The default path charges every diesel load at diesel's own vapour pressure and files about 1.4 tonnes of VOC from
loading for 2026, inside the 20-tonne limit; about half of the retail fleet's diesel went into compartments whose last
delivery was petrol through a station's vapour balance, so each of those loads pushed saturated petrol vapour out at
an uncontrolled distillate bay, and the terminal released about 48 tonnes and exceeded its limit.

## Three rules

- **Task type:** emissions-inventory (Physical & Environmental Sciences), which the taxonomy tags for ETL: the release
  at each loading point estimated from activity records conformed across two terminal automation exports, the dispatch
  dockets, the tanker register and the vapour recovery unit's outlet log, into the licence's annual return.
- **Domain test:** the deciding quantity is the VOC each loading releases, worked the way an emissions inventory works
  loading losses: the vapour the liquid displaces times the hydrocarbon that vapour carries, which for a compartment
  returning from a vapour-balanced petrol drop is saturated petrol vapour (the field's own saturation factor for
  vapour-balanced service, 1.0) whatever liquid displaces it, and for a compartment returning from a diesel drop is
  diesel's negligible vapour.
- **Swap:** "how much VOC did our loading bays release in 2026" in a hospital's nouns ("how much aerosol did our ward's
  bed changes release") keeps the sentence and loses the task: nothing carries a saturated vapour from one use to the
  next, and no displacement makes one change's release depend on the use before it.
- **Layer 1:** the terminal automation system changed on 1 July (the old export in gross observed litres with a VCF
  column and trailer plates, the new one in net litres at 15 C with its own tanker ids and B-double compartments
  numbered through); the dispatch system writes dockets in UTC while the terminal runs on local time (AEST, AEDT from 4
  October); the tanker register carries plates changed at re-registration and access cards reissued at the cutover;
  the vapour recovery unit's analyser was replaced in May (ppm as propane before, mg per cubic metre after) with flagged
  calibration intervals; cancelled and re-issued bills of lading; the ULP 91 code renamed when E10 replaced it in March.
  Each is what the system that writes the file produces; none carries the call (every mishandled item leaves the
  default near 1.4 tonnes and the golden near 48).
- **Layer 2:** estimation fitted to the data's generating process, the field's own method done right (field_method):
  the loading-loss equation's saturation and vapour pressure belong to the vapour the compartment holds when loading
  starts, which the multi-product fleet's previous deliveries set, not to the liquid loaded.
- **Decisive step:** charge each distillate load the vapour its compartment held when the diesel went in, rebuilt from
  that compartment's last delivery in the dispatch dockets (a vapour-balanced petrol drop leaves saturated petrol
  vapour, a diesel drop leaves none), the petrol the fleet lifted at the partner terminal included, which the terminal's
  own exports never see.
- **Not semantics:** every field, code and unit read correctly (both export layouts, gross and net litres, UTC against
  local time, the renamed product code, the analyser's units, the dockets' vapour-hose field) still leaves the
  per-product equation at about 1.4 tonnes; what moves the call is the analysis that the vapour leaving a distillate
  bay is the previous delivery's, which no field states.
- **Not rule application:** the licence and its return protocol file the estimand (the VOC released to air from product
  loading at the terminal in calendar 2026, at each bay, the vapour recovery stack at its measured outlet, in tonnes,
  against 20), the vapour tables and the temperature convention; no filed rule says which vapour a load displaces, so
  executing every filed rule with the field's equation files the default path. Enumerated family on the prototype
  (seed 461, distillate bays): 0.27 to 0.80 tonnes (the per-product equation at saturation factors 0.5 to 1.45), 39.6
  (each compartment's previous fill in the terminal's own exports), 46.8 (its previous delivery in the dockets), 87.7 to
  88.3 (every retail diesel load, or every load after a trip carrying petrol, at petrol vapour), 28.2 (the dockets'
  construction at saturation 0.6). Standing family (the constructions that charge each fill its compartment's previous
  delivery, every closed convention): 46.7 to 46.8, under one printed tonne. Loudness of the ruling-out: quiet; no
  sentence or column names the previous delivery, and the per-product route passes the terminal's own diesel stock
  balance.
- **Analyst test:** with both terminal automation exports conformed, every docket read and the protocol's vapour tables
  applied, a strong analyst sums each bay's litres by product, charges them by the loading-loss equation at each
  product's own vapour pressure (diesel's is negligible) and adds the vapour recovery unit's measured outlet, filing
  about 1.4 tonnes for 2026, well inside the 20-tonne limit, because nothing asks what each compartment held when its
  diesel went in.
- **Estimand:** the licence's annual return condition and the Authority's return protocol: the mass of VOC released to
  air from product loading at the terminal in calendar 2026 (local time), at each loading point, the bays connected to
  the vapour recovery unit at the unit's measured outlet, in tonnes, against the 20-tonne limit (the licence and the
  protocol, both PDF, written at stage 3).
- **No decoy:** nothing is planted to be caught: compartments switch between products because a multi-product fleet
  fills them to the order, and the stations' vapour balance is the stations' own licence condition; no memo, prior
  return, draft or stakeholder figure ships, and no document argues for any figure.
- **No certified replay:** no certified or published figure carries a release or a switch count; the vapour recovery
  unit's outlet is measured and ties on every path; the method is the analyst's.
- **Lesson:** a loading release is set by the vapour the compartment brings back, not the liquid that goes in, and the
  field's per-product loading equation holds only in dedicated service, which a multi-product fleet breaks load by
  load. No build on file teaches it: task479 v7 caps a shared device's draw, task476 and task487 date leaks found at
  inspection, task459 stages a ratio by operating level, task153 caps a draw at one fill between visits.

## Survivor anatomy

- **Actor:** pass. The deciding property, the vapour each compartment holds when its diesel goes in, has no column in
  any file: it is a relation between a load and the same compartment's previous delivery, across the terminal exports
  and the dispatch dockets.
- **Link:** pass. The previous delivery sits in the dispatch dockets, keyed by fleet unit and compartment and stamped
  in UTC; the load sits in the terminal exports, keyed by plate (January to June) or tanker id (July to December) on
  local time; the tanker register crosswalks them, and no sentence invites the comparison, which the per-product method
  never asks for. The terminal exports' own self-join exists and misses the exchange trips (39.6 against 46.8 on the
  prototype).
- **Reflex:** pass. The field's named method (the loading-loss equation per product, saturation 0.6 for submerged
  loading in dedicated normal service) is rung 0 and files about 1.4 tonnes, the `Ends on:` figure.
- **Back-test:** pass. The per-product route validates on the solver's own check: the terminal's diesel stock balance
  (receipts against loaded litres and the tank dips) shows no evaporation loss beyond meter tolerance, as the
  per-product equation predicts, because the petrol vapour that leaves at the distillate bays came from the stations'
  tanks, never from the terminal's.
- **Second use:** pass. The dispatch dockets ship for the return's exchange and delivery figures and the tanker register
  for the cutover's crosswalk; deleting the decisive step leaves both in the pack.
- **Shock:** pass. The switch fills are about half of the retail diesel fills, spread over every trailer, month and both
  distillate bays; no shipped statistic singles them out, and nothing in the pack moves when they are counted.
- **Pins:** pass. The return protocol files the WHAT (released to air, each loading point, calendar 2026, tonnes, the
  recovery unit at its measured outlet, temperatures at the bay meter, the vapour tables) and no sentence names a
  compartment's previous delivery, vapour balance or saturation.

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
