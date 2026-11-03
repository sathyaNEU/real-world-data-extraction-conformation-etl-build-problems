# task307 design note

Architecture 3, a re-root drawn on 2026-11-03 in the same objective (Opportunity Sizing & Decision Support) and the
same number, at the orchestrating session's call. Architecture 1 (a planning organisation's congestion slot) was found
spent at the 11-01 re-check because its guidance filed the HOW; architecture 2 (a hospital's side-room shadow price)
died on its own prototype on 11-02 because the counterfactual of a freed side room turned on unrecorded allocation
rules. Both are recorded in `## Architecture records` and in the card's lineage; architecture 1's pack stays at the
portal, pending, untouched. This architecture moves to a third client domain, a new world, dataset and prompt shell.

## Draw

| Item | Value |
|---|---|
| Pairing | `energy-systems-utilities` / `asset-condition-maintenance` (the task type serves Opportunity Sizing): the deciding quantity is the generation each unit would lose to an unplanned runner outage before 2032, set by the year its runner's cavitation pitting reaches the company's repair limit |
| Objective | Opportunity Sizing & Decision Support: the pool is the generation the fleet's runners put at risk of an unplanned outage before 2032, the realisable part is what the one runner the 2027 summer window can take spares, and that sized figure per million kroner decides where the window goes |
| Forward window | the 2027 summer outage window and the generation of 2027 to 2031; nothing in it has happened yet |
| World | Sørdal Kraft, a fictional western Norwegian municipality's hydropower company running a cascade of three stations (Øvre Sørdal, Sørdal and Nesvik) with seven Francis units; the 2027 summer window has crane, crew and runner-shop capacity for one runner refurbishment |
| People (not in the prompt) | Rita Haugen, head of production assets; Arild Sivertsen, maintenance planner (`guard.py names --geo norway --seed 307`) |
| Shape | 01, a ranked list with one pick: per unit the runner, pitting at the last inspection, pitting now, the year it reaches the limit, the generation at risk and that per million kroner (seven units, 42 cells), the pick, runner-up and gap (3), the chart's parts (3), and the asks' unit-year cells |
| Deliverables | `runner_2027.xlsx` (the decision workbook) and `runner_2027.svg` (the bar chart of generation spared per million kroner, chosen unit marked) |
| Card | `.claude/skills/fingerprint/cards/task307.json`, architecture v3, registered 2026-11-03; guard WARN `overuse.gate_g` and NOTE `test.same_puzzle_older` against task472 v2, differentiated on the card |
| Strategy and family | `other` (wear accruing inside one band of a unit's output range that a new duty moved units into, read from each unit's own output record); Layer 2 family `estimand_identification`; generators G7 (operating window) then G13 (horizon mismatch) |

**Data-native sentence.** Since 2022 Units 3 and 6 have held frequency containment reserve and run with headroom at
part load, and a Francis runner erodes by cavitation in the part-load rough zone, so their pitting has run ahead of
their running hours, while the maintenance system's hour counters and every inspection pair before 2022 were taken
under base-load duty, when an hour run and an hour in the rough zone moved together.

**The WARN, answered.** `overuse.gate_g`: forecasting is the honest mechanism, since the call turns on the year each
runner reaches its limit under the duty it now holds; the shell (where, set out, xlsx and svg) and the strategy
(`other`) differ from every build in the window, and the nearest driver on file sits at 0.09.

## Architecture records

- Architecture 1 (drawn 2026-10-27, urban-regional-science optimisation, a planning organisation's congestion slot
  scored by re-assigning trips on each build network): shipped; found spent at the 11-01 re-check because executing
  the scoring guidance with its documentation 6.1 gave the golden. Pack at the portal, pending.
- Architecture 2 (drawn 2026-11-02, healthcare patient flow, a hospital's side-room shadow price): spent at stage 2
  on its own prototype (11-02), no pack cut; the line is in `## Tried and rejected`.

## Tried and rejected

- 2026-10-27: OS09 (a mini-split rebate programme's net first-year savings) left at the draw: its honest
  stump labels were all held by the guard window and its furniture barred; moved to another domain.
- 2026-10-27: a resource adequacy design (cold-correlated forced outages, four capacity offers) prototyped
  and dropped before registration: task308's architecture 3 registered the same world and driver first.
- 2026-10-27: screening yield by time since the last screen dropped on paper as an echo of task301's
  yield-by-record-age driver.
- 2026-10-27: the planning time index ask (probe stamps marking the interval end as its silent device) dropped at
  stage 4: the judge read the stamp convention as an unfiled fork, and filing it hands the ask to every reader.
- 2026-11-01: architecture 1 found spent at the re-check under the new gates: executing guidance 2.1 with documentation
  6.1 (user equilibrium on the coded network) is the golden, so the analyst test fails and the decisive step is rule
  application (generator/analyst_test.py); the survivor anatomy holds only Actor. Not re-rooted on the orchestrating
  session's rule; the shipped pack stays at the portal, pending.
- 2026-11-02: re-rooted at the orchestrating session's call: architecture 1 died because 6.1 filed the HOW, so
  executing the guidance gave the golden, and only Actor held; architecture 2 moves to healthcare patient flow, a new
  world, dataset and shell, with no governing document filing the method.
- 2026-11-02: debt-sale censoring of an in-house recovery curve (collections) dropped at the draw: population selection
  is banned in the window (task273) and stratifying by the sale score is the grouping dichotomy.
- 2026-11-02: failed-payment notices triggering voluntary cancellations (subscriptions) dropped at the draw: a pilot's
  retention ITT lands it, and without one the triggered share is a model with a free baseline.
- 2026-11-02: an early-bleeding window for a 2027 anticoagulant switch cohort (pharmacology) dropped at the draw: the
  one-year cumulative incidence from past switchers is a reflex that lands it, and its honest label is banned.
- 2026-11-02: delayed entry at a system go-live (retention) dropped at the draw: its honest label, population
  selection, is banned in the window.
- 2026-11-02: cross-line common shocks for a clash cover (reinsurance) dropped at the draw: the treaty's occurrence
  clause files the unit (the WHAT screen) and the dependence model forks.
- 2026-11-02: short-borrow availability capping a long-short sleeve (quantitative finance) dropped at the draw: borrow
  cost is a quant default and the locate file would exist only for the step.
- 2026-11-02: bed-hours from a discharge lounge counted only when an ED patient waits (patient flow) dropped at the
  draw: boarding by hour is one group-by, and the world sits on task127's.
- 2026-11-02: redials inflating an Erlang sizing (a booking line) dropped at the draw: the retrial queue carries a free
  persistence parameter.
- 2026-11-02: regression dilution in a blood-pressure slope (health burden) dropped at the draw: the literature's
  usual-BP relative risks land it and the swap reads the same in any field.
- 2026-11-02: sold-out options narrowing observed choice sets (choice modelling) dropped at the draw: task302's
  substitution, and the choice model's specification forks.
- 2026-11-02: month-end snapshots hiding intra-month delinquency (collections) dropped at the draw: a grain reading.
- 2026-11-02: household secondary cases credited to a schools vaccination programme dropped at the draw: causal design
  (spillover) is banned in the window (task157).
- 2026-11-02: a care-home discharge-to-assess partnership as the scheme that frees side rooms, prototyped and replaced
  by the palliative partnership before carding: its vocabulary and world (care-home waits, medically optimised dates,
  discharge-to-assess) sit on task127's.
- 2026-11-02: a side-room pod as one of the candidate schemes dropped at the draw: a scheme that adds side rooms names
  the decisive step.
- 2026-11-02: architecture 2 (the side-room shadow price: a scheme credited with the bays it keeps open by freeing side
  rooms when every medical side room is full) spent at stage 2 on its own prototype, before any pack was cut: the
  counterfactual of a freed room is a queue, refilled by whoever needs a room next, so the honest replays (FIFO 858,
  infection-first 1,029 bed-days) file the modular ward (1,284), the default path's answer, and block 73 to 119
  recorded room takes the record cannot price, while only the naive per-closure check (1,615) files the partnership.
  The call depends on unrecorded allocation rules, so closing the fork files the HOW (a withheld rule either way).
  With this the number has screened fourteen candidates across eleven task types at the 11-02 re-root and none
  clears; PAUSED on the orchestrating session's rule.
- 2026-11-03, architecture 3 search, each dead at the draw: pooled testing with site-clustered positives (a replay
  of the rack order lands it and the swap reads the same in quality control); competitive anti-selection on
  comparison sites (task163's marginal entrant, and the window bans financial institutions); a streaming renewal
  (task302's substitution); a wind farm aero upgrade net of wakes (task187's world and task303's named-caveat
  screen); condition-based replacement under censoring (needs a decay model, Gate C); a tourist levy's base erosion
  (identity reconciliation, an ETL step); a heat pump peak at the coldest hours (task309's mild-against-severe
  abstraction); cyber misattestation (semantics, and a banned org family); a DGA reset (the resets family, task152 and
  task229); discolouration from the utility's own valve operations (task303 again); maintenance-induced failures (a key
  join plus a window fork).
- 2026-11-03: a council's area-based insulation round sized by metered gas with comfort take-back settling at the new
  fabric's level, prototyped to a clean ladder (scratchpad proto307/sim7.py, eight seeds) and dropped before
  registration: the decisive step is task258's landed lineage driver (a part settling at a fixed level rather than
  shrinking in proportion, which both top portal responses reached by back-testing), and the world is OS06's, task304's
  seed.
- 2026-11-03: indirect protection from a schools vaccination programme (task135 and task180 set it aside), N-1
  redundancy behind an asset (dead on file, task198), a dairy calving shift (task162's list), and a 2027 grant's
  fungibility kink against each recipient's own spending (task165's gain conditioned on prior coverage), all dead on
  the slot notes before any harness.
- 2026-11-03: a foundation's anchor grant sized net of crowd-out of each charity's other income, prototyped
  (scratchpad proto307c/sim1.py, sim2.py): at charity revenue's realistic year-to-year noise one grant episode per
  charity cannot identify its own crowd-out (estimates off by 0.2 to 0.4 at 3 per cent noise), and pooling by a
  visible trait makes it the grouping dichotomy. Dropped.
- 2026-11-03: VAT letters credited with their suppliers' extra declarations (the total equals the recipient's own
  extra output VAT, so the step is reading output against net VAT, semantics); cash transfers credited with market
  spillovers to non-recipients (task500 v2's spillover through a link); a small-cluster randomisation-inference hold on
  a labour market pilot (the swap reads the same in any field, a backdrop domain); average against marginal price
  response to a block tariff (average price is a common default, so two cheap routes land it); a water efficiency
  programme valued at each day's marginal source (task460's margin read interval by interval); postal bowel-screening
  kits losing haemoglobin in transit (task248's transit loss at a temperature-driven rate); a Real Living Wage uplift
  costed with contractors' differential policies recovered from past upratings (a withheld rule recovered from settled
  cases). All dead at the draw.
- 2026-11-03: a district heating renewal sized by the buildings a leak cuts off at the nearest valve crews can close,
  prototyped (scratchpad proto307c/dh1.py) and dropped at the guard check: it is task273's architecture 3 (spent on
  paper 10-27, the area bounded by the nearest operable boundary devices, operability kept in a maintenance history),
  which the lexical driver score missed at 0.07.
