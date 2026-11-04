# task461 design note

Architecture 2, drawn 2026-11-04: a re-root of the number into a new client domain, world, dataset and prompt shell.
Architecture 1 (a battery's 2027 cycling threshold carried from a trading hub's long price record, General Statistics
& Data Science) was found spent at the 2026-11-02 re-check (its line in `## Tried and rejected`); its build files are
cleared from this folder and kept in history, and this build replaces it. No seed: the world, the decision and the
quantity are drawn new. Every figure below is printed by `generator/checks.py`, `generator/ceiling.py` or
`generator/figures.json` on the built pack (world seed 4770).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task461.json`, architecture v2, registered 2026-11-04, architecture 1 in
  its lineage with its fate. The two structural matches against older builds (task488, task308 v3) are differentiated
  on the card, and the WARN on Gate G repeating task200 is answered here: method_or_model_selection is the honest label
  (the field's per-product loading-loss equation against the same equation applied to the vapour each compartment
  holds, the right one fixed by the field's own saturation factor for vapour-balanced service), in another domain and
  on another driver.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL. The objective is ETL because the call is
  read from a conformed return: two terminal management system exports across a 1 July cutover, the dispatch system's
  delivery dockets, the tanker register and the vapour recovery unit's monitor log reconciled into the licence's
  annual return of VOC from product loading.
- **Why this cell, and why it is open:** the six ETL task types hold 68 cards, emissions-inventory 12 of them. Those 12
  spend the activity level (task470, task474, task480, task484), the rate against operating level (task459, task460,
  task478), detection and completeness (task452, task462), the dating of leaks found at inspection (task476, task487)
  and a shared control device's capped draw (task479 v7). None charges a release by a state the emitting container
  carries over from its previous use, and `guard.py slots` on the setting's nouns (switch, loading rack, vapour
  recovery, compartment, previous cargo, fuel terminal, petrol tanker) returns nothing on this ground.
- **Shape:** other, the return's grid: the year's loading VOC, whether it passed the licence's 20-tonne limit and by
  how much; the release at the vapour recovery stack and at each distillate bay in each quarter; each storage tank's
  release over the year by the protocol's tank method; the covering note's monthly chart; and the terminal's own stock
  account of each tank's gain or loss in each quarter.
- **Strategy:** other (no vocabulary family is honest: each fill's release is a state its compartment carries from the
  previous delivery, rebuilt per load from a second system's record; not a mix shift or reweighting, not a grain or
  identity reading, not censoring). Gap objective (each load record is right about the liquid loaded and the release is
  scored on the vapour displaced), then population. Generators G14 (the release per litre conditioned on the
  compartment's previous delivery) decisive, G3 (the bay's record says diesel, the vapour that left was petrol) and G2
  (the emitting unit is the compartment's cycle from one delivery to the next load, not the load row) behind.
- **World:** Brennock Fuels, a regional fuel distributor in Warrenby (a fictional Australian port city), owns the
  Warrenby terminal. Petrol bays 1 to 3 bottom-load through vapour collection to a carbon-bed vapour recovery unit
  (VRU-1), interlocked so no petrol loads while it is off; distillate bays 4 and 5 load diesel with no vapour
  collection. The retail fleet (five semi-trailers and three B-doubles) carries petrol grades and diesel to the
  distributor's metropolitan service stations, every petrol drop made through the station's vapour balance; under a
  supply exchange with Tarrant Energy part of the retail petrol is lifted at Tarrant's Selwyn Point terminal. Oakhurst
  Haulage, the contract carrier, takes diesel to farms and mines in dedicated trailers. The Coastal Air Quality
  Authority's licence (EPL 20514) limits VOC from product loading to 20 tonnes a calendar year and requires the annual
  return by 31 January.
- **Forcing fact:** the licence's return for 2026, due 31 January 2027. The call is retrospective by nature: a licence
  return reports the closed year, and whether the terminal kept within its limit is a fact about 2026. As of 8 January
  2027 (the folder's assembly date, the `--asof` for `leak.py`).
- **Forum and forcing event:** regulator_or_inspector (the Authority receives the return), statutory_or_regulatory_filing
  (the return's due date). Organisation logistics_or_3pl (a fuel distributor's terminal and fleet); role
  operations_director (the terminal manager, who signs the return). Personas from `guard.py names --geo Australia --seed
  461`: Anna Gardner (terminal manager), Jeffrey Pruitt (dispatch manager).
- **Data-native sentence:** a multi-product retail fleet fills each compartment with whatever the next order needs, so
  about half of its diesel (5,126 of 9,379 retail distillate loads) goes into compartments that last delivered petrol,
  and every petrol drop at the metropolitan stations runs through the station's vapour balance, which fills the
  emptying compartment with the station tank's saturated vapour; the distillate bays collect no vapour, so that petrol
  vapour leaves at the bay as the diesel goes in, while the terminal's own records hold each load's product and litres
  and never the vapour the compartment brought back.
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
    the vapour pressure and molecular weight, the liquid temperature), with its saturation factors keyed to the
    cargo tank's service; it is the opponent's first move, never filed in the pack.
  - `dataset-generation/references/layer1-messiness.md`: a system cutover with its layout, volume basis and identifiers
    changed and a shadow run overlapping, timestamps carrying their own offsets across daylight saving, identifiers
    reissued at re-registration, an analyser swap in a monitoring log with its unit changed, product codes renamed.

## Default path

1. Conform the two terminal management system exports into one 2026 load register by bay, product and quarter: January
   to June in gross observed litres with a VCF column and trailer plates, July to December with gross observed and net
   litres at 15 C and the new system's tanker ids, the 29 and 30 June shadow rows and the cancelled transactions out.
2. Take the petrol bays' release as VRU-1's measured outlet mass, summed from its 15-minute log (VOC_OUT in kg/h to
   the May analyser swap, VOC_OUT2 in g/min after, each CAL interval at the mean of the hour either side), as protocol
   section 3 files.
3. Charge each distillate bay by the field's loading-loss equation per product: observed litres loaded times the
   saturation factor for submerged loading in dedicated normal service (0.6) times diesel's true vapour pressure and
   vapour molecular weight from the protocol's Tables 1 and 2 at each load's meter temperature, over R times the
   temperature.
4. Sum the year and set it against the licence's 20 tonnes.

- **Ends on:** 1.4 tonnes of VOC from loading in 2026, within the limit (the VRU-1 stack 1.1, bay 4 0.1, bay 5 0.2).
- **Golden:** 38.4 tonnes, over the limit by 18.4 (bay 4 32.7, bay 5 4.7, the VRU-1 stack 1.1).

## Stump sentence

The default path charges every diesel load at diesel's own vapour pressure and files 1.4 tonnes of VOC from loading for
2026, inside the 20-tonne limit; 5,126 of the retail fleet's 9,379 distillate loads went into compartments whose last
delivery was petrol through a station's vapour balance, so each pushed saturated petrol vapour out at an uncontrolled
distillate bay, and the terminal released 38.4 tonnes and exceeded its limit by 18.4.

## Three rules

- **Task type:** emissions-inventory (Physical & Environmental Sciences), which the taxonomy tags for ETL: the release
  at each loading point estimated from activity records conformed across two terminal management system exports, the
  dispatch dockets, the tanker register and the vapour recovery unit's monitor log, into the licence's annual return.
- **Domain test:** the deciding quantity is the VOC each loading releases, worked the way an emissions inventory works
  loading losses: the vapour the liquid displaces times the hydrocarbon that vapour carries, which for a compartment
  returning from a vapour-balanced petrol drop is saturated petrol vapour (the field's saturation factor for
  vapour-balanced service, 1.0) whatever liquid displaces it, and for a compartment returning from a diesel drop is
  diesel's negligible vapour.
- **Swap:** "how much VOC did our loading bays release in 2026" in a hospital's nouns ("how much aerosol did our ward's
  bed changes release") keeps the sentence and loses the task: nothing carries a saturated vapour from one use to the
  next, and no displacement makes one change's release depend on the use before it.
- **Layer 1:** the terminal management system changed on 1 July (the legacy export in gross observed litres with a VCF
  column, trailer plates and each trailer's own compartment numbers, the new one with net litres at 15 C, tanker ids,
  B-double compartments numbered through, cancelled transactions and a two-day shadow run overlapping the legacy
  export); the dispatch dockets stamp each time with its own offset (+11:00 under daylight saving, +10:00 outside it);
  the tanker register carries plates changed at re-registration; VRU-1's analyser was replaced in May (kg/h before,
  g/min after) with daily CAL intervals; product codes differ in each system. Each is what the system that writes the
  file produces; none carries the call (checks.py's R2 block: every mishandled item leaves the default near 1.4 tonnes
  and the golden over the limit, the VRU-1 channel read in the wrong unit at 11.8 tonnes of stack).
- **Layer 2:** estimation fitted to the data's generating process, the field's own method done right (field_method):
  the loading-loss equation's saturation and vapour pressure belong to the vapour the compartment holds when loading
  starts, which the multi-product fleet's previous deliveries set, not to the liquid loaded.
- **Decisive step:** charge each distillate load the vapour its compartment held when the diesel went in, rebuilt from
  that compartment's last delivery in the dispatch dockets (a vapour-balanced petrol drop leaves saturated petrol
  vapour, a diesel drop leaves none), the petrol the fleet lifted at the partner terminal included, which the terminal's
  own exports never see.
- **Not semantics:** every field, code and unit read correctly (both export layouts, gross and net litres, the dockets'
  offsets, the renamed product codes, the analyser's units, the dockets' vapour-hose field) still leaves the
  per-product equation at 1.4 tonnes; what moves the call is the analysis that the vapour leaving a distillate bay is
  the previous delivery's, which no field states.
- **Not rule application:** the licence and its return protocol file the estimand (the VOC released to air from product
  loading at the terminal in calendar 2026 local time, at each loading point, the vapour recovery stack at its measured
  outlet, in tonnes, against 20), the vapour tables and the temperature and volume convention; no filed rule says which
  vapour a load displaces, so executing every filed rule with the field's equation files the default path. Enumerated
  family on the built pack: 1.34 to 1.76 tonnes (the per-product equation at saturation factors 0.5 to 1.45), 32.2
  (each compartment's previous fill in the terminal's own exports), 38.4 (its previous delivery in the dockets), 69.0
  (every retail diesel load at petrol vapour), 23.6 (the dockets' construction at saturation 0.6). Standing family (the
  constructions that charge each fill its compartment's previous delivery, every closed convention): 38.36 to 38.43,
  one printed figure. Loudness of the ruling-out: quiet; no sentence or column names the previous delivery, and the
  per-product route passes the terminal's own stock account.
- **Analyst test:** with both terminal exports conformed, every docket read and the protocol's vapour tables applied, a
  strong analyst sums each bay's litres by product, charges them by the loading-loss equation at each product's own
  vapour pressure (diesel's is negligible) and adds VRU-1's measured outlet, filing 1.4 tonnes for 2026, well inside the
  20-tonne limit, because nothing asks what each compartment held when its diesel went in.
- **Estimand:** the licence's conditions L1, R1, R2 and D1 to D3 and the Authority's return protocol: the mass of VOC
  released to air from product loading at the terminal in calendar 2026 (local time), at each loading point (the bays
  connected to VRU-1 at the unit's measured outlet), in tonnes, against the 20-tonne limit, and the amount over it.
- **No decoy:** nothing is planted to be caught: compartments switch between products because a multi-product fleet
  fills them to the order, and the stations' vapour balance is the stations' own licence condition; no memo, prior
  return, draft or stakeholder figure ships, and no document argues for any figure.
- **No certified replay:** no certified or published figure carries a release or a switch count; VRU-1's outlet is
  measured and ties on every path; the annual stack test covers VRU-1 alone; the method is the analyst's.
- **Lesson:** a loading release is set by the vapour the compartment brings back, not the liquid that goes in, and the
  field's per-product loading equation holds only in dedicated service, which a multi-product fleet breaks load by
  load. No build on file teaches it: task479 v7 caps a shared device's draw, task476 and task487 date leaks found at
  inspection, task459 stages a ratio by operating level, task153 caps a draw at one fill between visits.

## Survivor anatomy

- **Actor:** pass. The deciding property, the vapour each compartment holds when its diesel goes in, has no column in
  any file: it is a relation between a load and the same compartment's previous delivery, across the terminal exports
  and the dispatch dockets (checks.py R1: no shipped column holds a previous product, a vapour state or a switch flag).
- **Link:** pass. The previous delivery sits in the dispatch dockets, keyed by fleet unit and dispatch compartment and
  stamped with its own offset; the load sits in the terminal exports, keyed by plate and trailer compartment (January to
  June) or tanker id and through-numbered compartment (July to December) on the terminal's clock; the tanker register
  crosswalks them, and no sentence invites the comparison, which the per-product method never asks for. The terminal
  exports' own self-join exists and misses the exchange trips (32.2 against 38.4 tonnes).
- **Reflex:** pass. The field's named method (the loading-loss equation per product, saturation 0.6 for submerged
  loading in dedicated normal service) is rung 0 and files 1.4 tonnes, the `Ends on:` figure.
- **Back-test:** pass. The per-product route validates on the solver's own check: the terminal's stock account (ask A)
  shows each tank's quarter within a few kilolitres of balance, as the per-product equation predicts, because the
  petrol vapour that leaves at the distillate bays came from the stations' tanks, never from the terminal's.
- **Second use:** pass. The terminal exports carry ask A's dispatches; the dispatch dockets carry the petrol rack's
  loads on manual bills of lading during two controller faults, which the stock account needs and the terminal exports
  never received (checks.py ask A D4b), so the dockets stay in the pack with the decisive step deleted; the tanker
  register is the terminal's own access register of approved units, plates and system ids, a crosswalk the
  organisation keeps; the delivery sites list ships as a declared distractor.
- **Shock:** pass. The switch fills are 54.7 per cent of the retail fleet's distillate loads, spread over every unit,
  month and both distillate bays, 42.9 per cent of them after a drop of petrol lifted at Selwyn Point; no shipped
  statistic singles them out, and nothing in the pack moves when they are counted.
- **Pins:** pass. The return protocol files the WHAT (released to air, each loading point, calendar 2026 local time,
  tonnes, the recovery unit at its measured outlet, the liquid temperature and observed volume at the bay meter, the
  vapour tables) and no sentence names a compartment's previous delivery, vapour balance or saturation (checks.py's doc
  block reads every governing sentence back with positive controls).

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second
use); the reflex row comes from the field's vocabulary for loading losses (saturation factor, true vapour pressure,
dedicated service).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the per-product loading-loss equation, S 0.6, plus VRU-1 (1.4 t) | protocol 4.1 to 4.4 and Tables 1 and 2 give every input | the product column | yes | the stock account balances | no | yes | no | readable |
| R1 every retail diesel load at petrol vapour (69.0 t) | no | the carrier and account columns split the fleet | no | no | no | yes | no | readable |
| R2 each compartment's previous fill in the terminal's own exports (32.2 t) | no | no column; a self-join of the exports by unit and compartment | no | no | no | no | no | silent |
| G (decisive) each compartment's previous delivery in the dispatch dockets, the Selwyn Point trips included (38.4 t) | no sentence names a previous delivery, vapour balance or saturation | no column holds a previous product or vapour state | no: the field's reflex is per product | no control ties only under it: the stock account and the stack test pass on every rung | no | no: a state rebuilt per load across two systems | the dockets also carry the manual-BOL loads ask A needs | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the population | every load at bays 4 and 5 in calendar 2026 local time, each at its own compartment's vapour | the loads of the retail fleet only | over, a lower figure | licence D2 (product loading at the premises' bays) and protocol 2.2 (each bay a loading point) |
| SF2 | the year's clock | local time | a UTC year | over, 38.3 t | licence D1 and protocol 2.1: "in the premises' local time" |
| SF3 | the volume in the estimate | the observed litres at the meter | net litres at 15 C | over, 38.3 t | protocol 4.4: "the observed volume (at that temperature) the loading meter records" |
| SF4 | the liquid temperature | each load's meter temperature | a month's mean product temperature | same call, same bins, 38.4 t | protocol 4.4, and asserted |
| SF5 | the grade season of the petrol vapour | the season of the month the diesel is loaded | the season of the previous drop | same call, 38.4 t | protocol 4.3: "A load takes the grade season of the month in which it is loaded" |
| SF6 | the saturation of the vapour a vapour-balanced drop leaves | 1.0 | 0.6 (dedicated normal service) | over, 23.6 t | the field's saturation table, dedicated vapour balance service 1.00; the docket's vr1_hose column records the balance on each drop |
| SF7 | the 29 and 30 June rows in both exports | once | twice | over, 38.6 t | the two exports carry the same loads on those days; the legacy export runs to 30 June and the new system's export starts on 29 June 06:00 |
| SF8 | cancelled transactions | out | counted | over, 38.5 t | the new export's Status column, each cancelled load re-loaded under a new transaction id |
| SF9 | a B-double's dog compartments in the legacy export | 6 to 9 on the dispatch numbering | 1 to 4 | over, 40.0 t | the tanker register's TMS compartment numbers (1 to 5 lead, 6 to 9 dog) |
| SF10 | a re-registered trailer's loads under its old plate | resolved through the register's previous regos | dropped | over, 37.9 t | the tanker register's Previous regos column with its dates |
| SF11 | a compartment carried empty for days | keeps its last drop's vapour | reset | same call | nothing in the pack records a compartment gas-freed; a closed compartment holds its vapour until displaced (242 such loads) |
| SF12 | by how much | the year's release less 20 t | a percentage | same call | licence R2: "the amount by which the limit was exceeded", and the prompt's tonnes |
| SF13 | VRU-1's CAL intervals | the mean of the valid readings in the hour either side | zero | over | protocol 3.2 |
| SF14 | a switched load's vapour | petrol vapour beside diesel's own | petrol vapour in place of diesel's | same call, same bins, 38.4 t | asserted: diesel's own vapour is under 0.2 per cent of the release |
| SF15 | a compartment split between two sites | one delivery product | two | same call | asserted: every split compartment delivered one product |
| SF16 | the stock at local midnight | the 06:00 AEST dip less the flows between midnight and the dip | the dip itself | same call (ask A only) | the prompt's "stock at local midnight"; asserted: no receipt or transfer runs between a quarter's midnight and its dip |
| SF17 | the tank method's day | the seal and vents the tank had at the start of the day | the completion day at the new rate | same call (ask B only) | protocol 5.2: "A day takes the rate for the construction, seal and vents the tank had at the start of that day" |
| SF18 | rounding | tonnes to one decimal, kilograms and kilolitres to the nearest whole unit | other precisions | same call | the prompt's closing sentence |

## Ladder

- **Rung 0, the field's reflex (1.4 t, within):** the per-product loading-loss equation at S 0.6 for every distillate
  load, plus VRU-1's measured 1.1 t. Every saturation factor in the field's table leaves it within (1.34 to 1.76 t).
- **Rung 1, the over-correction (69.0 t, over):** every retail diesel load charged petrol vapour (the carrier column
  read as the switch); 1.82 times the golden, since 45 per cent of the retail fleet's diesel follows a diesel drop.
- **Rung 2, the terminal's own history (32.2 t, over):** each compartment's previous fill in the two terminal exports;
  it misses every compartment whose last drop carried petrol lifted at Selwyn Point and charges the ones that drained a
  petrol load at a farm without vapour balance; the golden is 1.20 times it on the bays.
- **Rung 3, decisive (38.4 t, over by 18.4):** each compartment's previous delivery in the dispatch dockets: saturated
  petrol vapour (S 1.0, the season of the load month) beside diesel's own vapour (S 0.6) where the last drop was petrol
  through the vapour hose, diesel's own vapour otherwise.
- **Separation:** the call flips between rung 0 and every rung above it; the three over-limit rungs file three
  different amounts (32.2, 38.4, 69.0), each more than 1.15 times apart; the standing family prints one figure.
- **Mess neutrality:** every Layer 1 item mishandled keeps rung 0 within and the golden over (checks.py R2 block).

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | every load into road tankers at bays 1 to 5; bays 1 to 3 reported at the VRU-1 stack | filed: licence D2, protocol 2.2 |
| 2 Unit of account | VOC in tonnes per loading point and quarter; kilograms per tank and year | filed: protocol 6.3, the prompt |
| 3 Attribution window | a load counts in the local quarter it is loaded in | filed: licence D1, protocol 2.1; SF2 |
| 4 As-of dating | the 2026 records as exported 4 to 8 January 2027, every 2026 load closed | static, asserted |
| 5 Version basis | the protocol's 2026 edition, the only one shipped | filed: its title block |
| 6 Denominator | none, a total | not applicable |
| 7 Weighting | none, a sum over loads and intervals | not applicable |
| 8 Window length | calendar 2026 | filed: licence L1 and D1 |
| 9 Boundary inclusivity | a load at its meter timestamp, a quarter from its opening midnight; CEMS intervals that begin in the period | filed: protocol 3.1; SF16 |
| 10 Rounding path | unrounded quarters, the year their sum, each rounded once at print | asserted: bins under both constant forms of the equation |
| 11 Tie-break | none: every compartment's previous delivery completes before its next load | asserted (R1: none without a previous drop) |
| 12 Maturity and censoring | no load open at the year end; the dockets run from December 2025 | static |
| 13 Order of operations | each load's vapour from its own previous delivery, then the sums | SF14, same call |
| 14 Row order | sums independent of order | C1 |
| 15 Duplicate resolution | the shadow rows and the cancelled transactions once or not at all | SF7, SF8 |
| 16 Identity normalisation | plates and trailer compartments, tanker ids and through-numbered compartments, fleet units, all through the tanker register | SF9, SF10 |
| 17 Netting against gross | observed litres for the release; net litres at 15 C for the stock account | SF3; the prompt for ask A |
| 18 Dimensional units | kPa, kmol and kelvin in the equation; VRU-1 kg/h then g/min; litres to kilolitres | asserted: R2's unit mishandlings, the US-unit form keeps every bin |
| 19 Code and status semantics | product codes per system, Status Complete or Cancelled, CEMS VALID, CAL and OFF, vr1_hose Y | each file's own values; SF8, SF13 |
| 20 Integerisation | none in the call | not applicable |
| 21 Clause scope | L1 covers product loading only; the tank method feeds the return's TANKS section | filed: licence L1, D2, R1 |
| 22 Forward window contents | none: retrospective, the 2026 return | the reason in Draw |

## Literal reader

Executed word for word, the licence and the protocol fix the population (loading into road tankers at bays 1 to 5 in
local calendar 2026, bays 1 to 3 at the VRU-1 stack), the unit, the quarters, the measured stack's arithmetic (3.1,
3.2), the liquid properties (Tables 1 and 2, 4.3) and the temperature and volume of each load (4.4), and leave the
distillate bays to "a recognised estimation method" (4.1). The recognised method is the loading-loss equation, whose
saturation factor, vapour pressure and molecular weight are those of the vapour the loading displaces; applied as the
field states it to the vapour each compartment holds, the literal reader files the golden, 38.4 tonnes, and applied
to the liquid loaded it files rung 0. No filed sentence, read literally, fixes the vapour, so no filed sentence executes
to the easy answer; the one sentence that could (a saturation factor keyed to the product) does not exist.

## Oracles

None arbitrates the decisive step. VRU-1's monitor ties on every path (it measures the petrol bays alone); the annual
stack test (a declared distractor) covers VRU-1 alone and its petrol throughput figures are per run; the terminal's
stock account balances within a few kilolitres under every rung, because the vapour that leaves at bays 4 and 5 was
never in the terminal's tanks; the dispatch dockets' litres reconcile with the loads under every rung. The only route
to the golden is the field's physics applied to the dockets' previous deliveries.

## Leak review

`leak.py task461 --asof 2027-01-08` on the final cut: REVIEW, no LEAK. One line per REVIEW:
- Sweep 3, the figures 1.1 and 1.2 in the protocol, the licence and the stack survey: clause numbers (1.1, 1.2), not
  the stack's 1.1 t. Harmless.
- Sweep 3, the licence carries 8 of the call's 10 distinctive words: they are the licence's own nouns (product loading,
  VOC, the terminal, the limit, the calendar year); it carries no release figure and ranks nothing. Harmless.
- Sweep 4, the protocol and the licence each carry 6 stump terms (vapour, petrol, diesel, distillate, measured, liquid,
  system): the words of a petroleum premises' governing documents; checks.py reads every governing sentence back and
  none names a previous load, vapour balance, saturation, switching or a compartment. Harmless.
- Sweep 12, the protocol names 7 and the licence 5 column words verbatim (Diesel, Internal floating roof, Service,
  product, tank, time, unit, Brennock Fuels): Table 3's construction rows, Table 4's header and the licensee's name, the
  Authority's own text; neither document describes a column or a join. Harmless.
- Fixed on this cut: the stack survey's file name (it carried the author word test_), the licence strings in
  metadata.json (CC0-1.0 carried the figure 1.0) and two temperature columns (temp read as a generator's word), each in
  the generator.

## Ask sheet

Planning weights 38 / 7 / 55 (call and critical components / instruction-following / asks). The return's loading grid
(twelve quarter figures, the year, whether over the limit, the amount over) is the main call's construction by point
and quarter and is scored with the call. The asks are A, the stock account (20 figures), and B, the return's TANKS
section (5 figures), plus the covering note's chart (a content requirement).

- **Ask A, the stock account (warrenby_2026_stock_account.xlsx):** each tank's gain or loss in each quarter in whole
  kilolitres at 15 C. H18 home: the call's back-test, the terminal's own balance showing the tanks lost no product the
  release could have come from. Use: the terminal manager's books for the year end. Path: the two terminal exports (15
  and 13 columns), the gauging file (8), the shift log (5), VRU-1's controller log (4), the outturns (13), the work
  orders (9), the dispatch dockets (14), eight files. Primaries: D8, the gauging system's 06:00 dips on AEST all year
  (the shift log's daylight-saving notes and the TGS-1 work order), read on the terminal's clock, moving 11 cells; D7,
  the diesel header line-ups in the shift log, a night shift's entries after midnight dated by the shift, moving all
  8 diesel cells; D4, VRU-1's absorber returns in the controller log, booked to the tank the shift log's absorber
  line-ups name (TK-1 except three valve repairs), moving 7 cells when left out and 5 when all booked to TK-1; D4b, the
  petrol rack's loads on manual bills of lading during two controller faults, held only in the dispatch dockets with
  one bill quantity on each line a split compartment delivered, moving 4 cells when left out and 1 when summed per line.
  Hazards: the transfers (shift log meter readings), the shadow rows, the cancelled rows, the legacy VCF (gross times
  VCF, per-load rounding and the unrounded 54B form keep every cell), the receipts by the surveyors' shore figures.
  Pin test: the asking sentence pins the basis (kilolitres at 15 C), the grain (tank and quarter), the boundaries
  (local midnight) and the account's terms (received, pumped out); no pin names the dip clock, the shift dating, the
  returns' tank or the manual bills, so every device survives its pins. Realism: each device is what the terminal's
  systems write (a gauging server on standard time, a log dated by shift, a controller that knows its pump and not the
  field valves, a dispatch system that holds the manual bills the terminal system never received).
- **Ask B, the tank method (warrenby_2026_annual_return.csv, TANKS rows):** each tank's 2026 release in whole
  kilograms by protocol section 5. H18 home: the return's own TANKS section, lodged with the call under licence R1. Path:
  the tank register (12 columns), the work orders (9), the outturns (13), the protocol's Tables 3 and 4. Primary D2:
  the register shows each tank as it stands in January 2027 (secondary seals on TK-1 to TK-3, pressure-vacuum vents on
  TK-4 and TK-5), and the work orders date each fitting in 2026 (February, May and September seals; March and August
  vents); the register-only route files 1,481, 1,101, 796, 170 and 170 kg against 1,723, 1,615, 1,544, 184 and 215.
  Hazards: the ship's figures beside the shore figures (5.3 files shore), the receipts by commencement. Pin test: 5.2
  files the day rule and Table 3 the rates; the device sits in which fitting each tank had on each day, which no pin
  states.
- **Main population zero-counts:** no ask organ sits in a file the main call reads except the dockets, whose manual-BOL
  device rides two columns (source_doc, bol_litres_15c) the main call never reads; the release is unchanged with both
  blanked (checks.py separation). The ask devices move no figure of the call.
- **Referee:** none; every ask figure is forced by its records and recomputed on `generator/verify.py`'s own path.

| Ask figure | Cracker (06:00 dips on the terminal clock, calendar-dated header changes, no VRU-1 returns, the register's current seals and vents) | Golden | Cracker |
|---|---|---|---|
| A: TK-1 Q1 gain (kL) | 84 | 19 | miss |
| A: TK-1 Q2 gain (kL) | 34 | -3 | miss |
| A: TK-1 Q3 gain (kL) | 24 | 4 | miss |
| A: TK-1 Q4 gain (kL) | 5 | -10 | miss |
| A: TK-2 Q1 gain (kL) | 17 | 11 | miss |
| A: TK-2 Q2 gain (kL) | 10 | 3 | miss |
| A: TK-2 Q3 gain (kL) | 7 | 0 | miss |
| A: TK-2 Q4 gain (kL) | -9 | -2 | miss |
| A: TK-3 Q1 gain (kL) | -4 | 3 | miss |
| A: TK-3 Q2 gain (kL) | 7 | 1 | miss |
| A: TK-3 Q3 gain (kL) | 7 | 0 | miss |
| A: TK-3 Q4 gain (kL) | 5 | -3 | miss |
| A: TK-4 Q1 gain (kL) | -426 | 12 | miss |
| A: TK-4 Q2 gain (kL) | 849 | 1 | miss |
| A: TK-4 Q3 gain (kL) | 190 | -6 | miss |
| A: TK-4 Q4 gain (kL) | -511 | -9 | miss |
| A: TK-5 Q1 gain (kL) | 457 | 16 | miss |
| A: TK-5 Q2 gain (kL) | -772 | 13 | miss |
| A: TK-5 Q3 gain (kL) | -200 | -4 | miss |
| A: TK-5 Q4 gain (kL) | 413 | -14 | miss |
| B: TK-1 2026 VOC (kg) | 1481 | 1723 | miss |
| B: TK-2 2026 VOC (kg) | 1101 | 1615 | miss |
| B: TK-3 2026 VOC (kg) | 796 | 1544 | miss |
| B: TK-4 2026 VOC (kg) | 170 | 184 | miss |
| B: TK-5 2026 VOC (kg) | 170 | 215 | miss |
| A, the full includer (every primary noticed, the returns booked to TK-1, the bill quantities summed per line) | keeps 15 of 20 | 20 cells | miss |

Pair ceiling: 31.3 (the cracker 45.0 on the call keeping no ask figure, the mirror 17.6 off it at 1.4 t, r 10.6 for the
VRU-1 quarters it shares with the golden).
Mirror leakage: 0.0 per cent of ask weight (the mirror, stopping at rung 0, runs the same careful route on the asks and
keeps none of the 25 figures).
Measured by: generator/ceiling.py, on the cut pack.

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
