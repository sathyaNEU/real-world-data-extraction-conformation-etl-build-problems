# task462 design note

Architecture 2, drawn 2026-11-04: a re-root of the number into a new domain, world, dataset, generator and prompt shell.
Architecture 1 (a gas basin's methane ratings from aerial surveys) was found spent at the 2026-11-02 re-check; its line
is in `## Tried and rejected`, its build files are cleared from the folder and kept in history, and its shipped pack
(target.zip 33e6d0c4) stays at the portal, pending. This build replaces it at ship. No seed: the world, the decision and
the quantity are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task462.json`, architecture v2, registered 2026-11-04T08:31:13Z, v1 in its
  lineage with its fate. `guard.py check`: WARN only (repeat.deliverables, svg and xlsx against task192 v4; answered:
  the chart is a vector file for the works' intranet page beside a workbook, and the rest of the shell differs, a
  how-many question, a second sentence led by the beds, a rounding sentence led by the unit).
- **Pairing:** house domain Supply Chain & Logistics (inventory-demand-planning), mapped to the client domain General
  Statistics & Data Science, task type data-integration-record-linkage-entity-resolution, objective ETL. The call is read
  from a conformed set: a year of monthly drone surveys of the ore yard by two survey contractors (two grids, two height
  systems, two export formats) conformed into one surface record, each bed's December volume taken against the pad
  beneath it, times the laboratory's bulk density for its product. The client task type is the one task476 v3 holds;
  its driver there is an identity resolution across two registers, here a base surface conformed from a survey archive.
- **Why this cell:** the last three draws hold record linkage (task476 v3), emissions inventory (task461 v3) and grid
  reliability (task192 v4); architecture 1's card is spent and holds no axis. The draw screened every ETL task type
  (the screens below, each with its death); the survivor is a stock measurement on a physical record, where the
  forcing file pins a surface rather than an identity, a grain or a clock.
- **Forum and forcing event:** committee_or_panel (the works' raw materials steering group signs the winter reserve
  statement) and season_or_peak (the Bothnian Bay ice season: the supplier's winter option cargo must be nominated by 8
  January for an ice-class loading in late January, and nothing else reaches the yard in volume until the spring
  opening). Organisation manufacturer; role capacity_planner (the raw materials manager plans the yard's stock against
  the blast furnaces' plan). Personas from `guard.py names --geo Finland --seed 462`: Kirsi Salo (raw materials manager,
  signs the statement), Aaro Miettinen (works survey engineer), Maarit Vainio (laboratory), Pekka Jalonen (yard
  operations).
- **World:** Perämeren Teräs Oy's integrated works on the Gulf of Bothnia coast: two blast furnaces fed from an ore yard
  of six beds on a pad built on reclaimed land, a ship unloader at the works harbour, a stacker and reclaimers on rails.
  Iron-bearing burden: pellets from Tornedal Mineral AB, pellets and lump ore from Ofoten Ore AS, and spot cargoes of
  both bought through Kattegat Ore Trading ApS. The yard is surveyed each month by drone, by one contractor to June 2026
  (the works grid, N60 heights, ESRI ASCII grids) and another from July (ETRS-TM35FIN, N2000 heights, XYZ text).
- **Forcing fact:** the winter reserve procedure's floor (days of the first-quarter plan's planned reclaim at the
  December survey) and the supply agreement's winter option, nominated by 8 January 2027. The call faces forward (the
  first quarter of 2027 is not yet run). As of 4 January 2027 (the folder's assembly date, the `--asof` for `leak.py`).
- **Data-native sentence:** the beds stand on reclaimed land and have been stacked on the same footprints for years, so
  the pad has consolidated into a bowl under each long-standing bed, which the December survey cannot see because the
  bed covers it; the year's monthly surveys show each such bed reclaimed to the pad once, in one or the other
  contractor's grid and height system, while the bed on the pad section added in 2025 has no bowl and so confirms the
  base through the toe wherever anyone checks it.
- **Abstraction sentence:** "an amount held above a surface that has sunk under its loads is understated by a surface
  through the loads' edges; the record shows the true surface only where a load was taken away." Nearest drivers on
  file at 0.07 (task251 v4 lineage) and 0.05, none a base surface.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: the field's method at rung 0 and the decisive step its
    violated precondition (a base through the toe assumes the pad under a pile continues the pad at its edge).
  - `dataset-generation/references/layer1-messiness.md`: two contractors on two grids and height systems, ESRI ASCII
    grids against semicolon XYZ with decimal commas, NODATA where a machine stood, a laboratory unit change, a port
    system in UTC against the works' Finnish time, a plant historian's catch-up after communication losses, a
    belt-scale integrator replaced mid-year, a trading house shipping a producer's cargo under its own name.

## Tried and rejected

- 2026-10-15, draw: the seed's own world, plant CO2 per MWh across CAMD, GHGRP and EIA through the EPA-EIA crosswalk.
  Rejected: task459 shipped those files, and in that world the decisive candidates were the crosswalk key, scope and
  net-against-gross readings (data semantics) or the operating level (task459's step); the many-to-many keys stay as
  Layer 1 here.
- 2026-10-15, build: each producer's tonnes with the detection curve's form left open. Rejected: the call held under
  every form, but a complementary log-log, a wind-normalised or a binned curve moved the tonnes 5 to 25 per cent from the
  logistic, so a judge choosing its own form would not reproduce the graded figures; Talmora's note now gives the
  curve's form and the standard how campaigns combine into the year, the weighting itself left unstated.
- 2026-10-15, build: the production extract from July 2025. Rejected: summing the whole extract moves the call, a Layer
  1 item carrying weight; the extract holds the rating year.
- 2026-10-15, build: a permit shared by a pad and a battery on different flight lines. Rejected: the coverage file gave
  the pad passes it never had; a permit is shared only where both sit under the same lines.
- 2026-10-15, build: gas to one decimal of a million cubic feet. Rejected: sums of whole Mcf sat within 2 Mcf of a
  rounding edge; whole million cubic feet, with the plant's and the commission's streams drawn so every ask figure sits
  0.04 MMcf or more from its edge.
- 2026-10-15, build: every producer's site count a multiple of five and its year of gas a round level. Rejected as
  realism tells; the register leaves out a few imaged sites that carry no source and sit 400 m or more from every
  plume, and each producer's gas takes a non-round level.
- 2026-11-02, re-check under the new gates: architecture 1 spent, not re-rooted. The easy routes on the clean truth
  file wrong slates (blanks as zeros eight, carried sources none, detected share ten), but the golden is the field's
  own POD-corrected aerial inventory (each plume over its detection probability from controlled releases) applied as
  the textbook states it, with nothing in the data violating its precondition, every curve form and the coarse
  correction landing the same four, the release study read by the decisive step alone, and the four the bottom four of
  the default sort (Reflex, Link, Back-test, Second use and Shock fail on the honest anatomy).
- 2026-11-04, re-root: architecture 1 left as spent (above), its build files cleared from the folder (kept in history);
  architecture 2 drawn in a house world (supply chain inventory) mapped to GSDS data integration, on a new world,
  dataset and prompt shell. The screens of this draw follow, each with the default path ending wrong, the swap test,
  the anatomy lines or the bin test priced on paper or in a prototype; the last was carded.
- 2026-11-04, screen 1, seasonal-adjustment-official-time-series-production, inventories in the national accounts
  revalued from book values to current prices (the inventory valuation adjustment) with FIFO stock turning over: a
  prototype (proto_fifo.py) put the standard turnover-window adjustment within 1 to 3 per cent of a full FIFO replay,
  so the decisive step was worth under one bin; the end-price and quarter-average deflations missed by about 15 per
  cent, but they are not what the field does.
- 2026-11-04, screen 2, stockpile volume above a plane through the toe on a crowned pad (the pad's drainage crown under
  the pile): a prototype (proto_pad.py) put the toe plane about 1 per cent from the truth, a lever no call can stand on.
- 2026-11-04, screen 3, payment claims, backdated pay-award arrears paid in one month for several earlier months: the
  arrears month carries several periods' amounts in one field, so the answer turns on reading that field correctly
  (data semantics), like the client's own rainfall example.
- 2026-11-04, screen 4, census-register, automatic bicycle counters that also count e-scooters after a firmware change:
  the loop counter's capture is traffic engineering on a register backdrop (task229 rejected the same cycle-counter
  draw as a domain backdrop).
- 2026-11-04, screen 5, payment claims, a hospital's cost-to-charge ratio after a chargemaster increase: the swap test
  fails (the ratio is a ledger quotient in any field), as task476's S3.31 found.
- 2026-11-04, screen 6, item-response-theory-test-equating, a spiralled old form with drifting anchor items: random
  groups equating is the field's reflex for spiralled forms and lands the golden, so the decisive step is the method.
- 2026-11-04, screen 7, item-response-theory-test-equating, anchor items affected by a scrolling display change: which
  anchors to drop is a fork resolved by a filed list or not at all, and the method is heavy for its worth.
- 2026-11-04, screen 8, item-response-theory-test-equating, remote-proctored candidates allowed scratch paper on one
  form: the condition is a column read (a proctoring code), data semantics.
- 2026-11-04, screen 9, emissions-inventory, a plastic packaging levy whose recycled-content share lags through a
  dryer's FIFO buffer: the swap test fails (a generic buffer delay), and the annual totals are invariant to the delay.
- 2026-11-04, screen 10, emissions-inventory, a ship's sulphur during an emission-control-area fuel changeover mixing in
  the service tank: the object is an exceedance in a window (anomaly detection), not a conformed inventory.
- 2026-11-04, screen 11, seasonal-adjustment, shrinkflation in scanner data for a price index: the product identity
  across a pack-size change is identity resolution and grain, both barred as the decisive step.
- 2026-11-04, screen 12, seasonal-adjustment, direct against indirect adjustment of an aggregate: a method fork the
  shipped files cannot close without naming X-13's options (an external dependency).
- 2026-11-04, screen 13, census-register, a deposit return scheme's return rate with cross-border returns: the
  population of eligible containers is the WHAT, so filing it is rule application and leaving it open is a fork.
- 2026-11-04, screen 14, stockpile reserve with the survey contractor's own volume report computed on the toe base:
  the report ranks the decision quantity wrongly (Gate G) and the step becomes rejecting a document.
- 2026-11-04, screen 15, stockpile reserve with the pad's as-built surface model shipped: surface-to-surface against a
  base survey is the field's reflex when a base survey exists, so the golden would be the method, not its violated
  precondition.
- 2026-11-04, screen 16, census-register, age heaping in birth dates from a register migration: a Layer 1 grouping
  item, and the smoothing is an estimator choice (the grouping dichotomy).
- 2026-11-04, prototype of the carded draw (proto_dish.py, proto_yard.py to proto_yard4.py): bowls 0.5 to 1.1 m under
  5.5 to 7 m piles put the toe plane at 0.93 of the truth; at yard scale with the crest at the stacker's fixed height
  and the slopes running down into the bowl, a bed only partly stacked at the December survey left its bowl's open
  end in view, where the lowest ring point fell into the hollow and landed within 1 per cent of the truth; with every
  bed stacked to its full length in December (the yard full before the ice season, crest heights varying) the base
  through the toe lands at 0.923, the ring's lowest and mean points at 0.931 and 0.923, every bed's own bare survey at
  1.001 and the lowest of all aligned surveys at 1.002, and using the bare surveys only where the December contractor
  flew them lands at 0.956. The December piles are full length in the build for that reason.
- 2026-11-04, prototype: one survey window per bed reaching into its neighbour's footprint double-counted the
  neighbour's pile against the lowest surface of every survey; each cell belongs to one bed, the beds 20 m apart.
