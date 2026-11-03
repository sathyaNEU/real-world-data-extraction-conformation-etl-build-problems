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
| Pairing | `energy-systems-utilities` / `asset-condition-maintenance` (the task type serves Opportunity Sizing): the deciding quantity is the generation each unit would lose to an unplanned runner outage in the 2027 to 2031 planning window, set by the year its runner's cavitation pitting passes the company's repair limit |
| Objective | Opportunity Sizing & Decision Support: the pool is the generation the fleet's runners put at risk of an unplanned outage in 2027 to 2031, the realisable part is what the one runner the 2027 summer window can take spares, and that sized figure per million kroner decides where the window goes |
| Forward window | the 2027 summer outage window and outages beginning in 2027 to 2031; nothing in it has happened yet |
| World | Sørdal Kraft, a fictional western Norwegian municipality's hydropower company running a cascade of three stations (Øvre Sørdal, Sørdal and Nesvik) with seven Francis units; the 2027 summer window has crane, crew and runner-shop capacity for one runner refurbishment |
| People (not in the prompt) | Rita Haugen, head of production assets; Arild Sivertsen, maintenance planner (`guard.py names --geo norway --seed 307`) |
| Shape | 01, a ranked list with one pick: per unit the runner, pitting at the last inspection, pitting now, the year it passes the limit, the generation at risk and that per million kroner (seven units, 42 cells), the pick, runner-up and gap (3), the chart's parts (3), and the asks' 14 unit figures: 62 graded figures |
| Deliverables | `runner_2027.xlsx` (the decision workbook) and `runner_2027.svg` (the bar chart of generation spared per million kroner, chosen unit marked) |
| Card | `.claude/skills/fingerprint/cards/task307.json`, architecture v3, registered 2026-11-03; guard WARN `overuse.gate_g` and NOTE `test.same_puzzle_older` against task472 v2, differentiated on the card |
| Strategy and family | `other` (wear accruing inside one band of a unit's output range that a new duty moved units into, read from each unit's own output record); Layer 2 family `estimand_identification`; generators G7 (operating window) then G13 (horizon mismatch) |

**Data-native sentence.** Since 2022 Sørdal G1 and Nesvik G1 have held frequency containment reserve and run with
headroom at part load, and a Francis runner pits by cavitation in its part-load band, so their pitting has run ahead
of their running hours, while the governors' hour counters and every inspection pair the register holds were taken
before the reserve duty began, when an hour run and an hour in the band moved together.

**The WARN, answered.** `overuse.gate_g`: forecasting is the honest mechanism, since the call turns on the year each
runner passes its limit under the duty it now holds; the shell (where, set out, xlsx and svg) and the strategy
(`other`) differ from every build in the window, and the nearest driver on file sits at 0.09.

## Survivor anatomy

Actor: the hours each unit ran inside the restricted band (30 per cent of its rating up to 58 per cent) have no column in any file; they are a relation between each unit's hourly output rows and its rating, and the pitting a runner carries now has no column either, only the pitting found at its last inspection.

Link: the rate pitting grows per band hour is read across sibling runners, the base-load runners' inspection pairs against the Sørdal G3 peaker's, which the field's per-runner condition record never compares; the peaker's pairs show ten times the base-load pitting per running hour and the same pitting per band hour within one per cent, and no sentence invites reading a reserve unit against the peaker.

Reflex: the field's own condition reasoning, pitting carried forward from the last inspection at a wear rate per operating hour (the equivalent-hours logic hydro condition schemes use, the governors' hour counters the maintenance system reads at every overhaul), sits at rung 0 and rung 1 and files Nesvik G2.

Back-test: the per-hour rate validates: across the five base-load inspection pairs (2016 to 2023, the peaker set aside as the peaker), pitting per running hour agrees within 13 per cent, and the counters' hours match the output record's running hours on every pair, so the hour route looks sound wherever the solver checks it.

Second use: every file the decisive step reads is in the pack for its own reason: the hourly output record feeds the generation and starts asks, the inspection register is the runner register's evidence, the unit register carries the ratings every generation figure needs and the operating ranges the operators work to.

Shock: nothing that moves reads as an anomaly: the reserve units' output since 2022 sits at part load as their reserve contracts require, their running hours barely changed, and the one runner with large wear per hour is the documented peaker, whose starts explain it; sorted on pitting at the last inspection, its age, running hours since, starts, generation, rating, quote, winter generation per kroner, reserve capacity or a runner's own wear per running hour, Nesvik G1 is never first (asserted).

Pins: the WHAT is filed in the company's runner standard and outage planning note (the repair limit as a total pitted area, a runner past it removed for a 14-week repair from 1 December of that year, the outage valued at the unit's mean generation over those weeks of the last five winters, the 2026 duty carried through the window); no filed sentence names the band as a wear driver, a wear rate, the reserve duty's effect or the peaker as evidence.

## Default path

The competent route, written from the prompt's words and the files' grain, with the field's condition method in it:

1. Read TS-07: the repair limit is 2,400 cm2 of total pitting; a runner past it comes out for a 14-week repair from 1 December of the year it passes.
2. Take each unit's present runner from the unit register and its pitting at its last inspection from the inspection register.
3. Fit the wear rate the field uses: pitting added per running hour across the inspection pairs, the hours from the governors' counters or the output record, with the Sørdal G3 peaker set aside as a peaker (pooled, it raises every rate and files Øvre Sørdal G1).
4. Carry each runner forward from its last inspection to 31 December 2026 at that rate times its running hours since, then year by year at its 2026 running hours (planning note 2.4).
5. Find the year each runner passes 2,400 cm2 in 2027 to 2031 and value its 14-week winter outage at the unit's mean generation over those weeks of the last five winters; divide by the quote excluding VAT.
6. Rank the units on generation spared per million kroner.

Ends on: Nesvik G2

Golden: Nesvik G1

Nesvik G2 is the only runner the per-hour rate takes past the limit before 2032 (2,072 cm2 at the cut, past 2,400 in 2030, its 2019 inspection the oldest and its hours the longest); carried at the rate per band hour, Nesvik G1 stands at 2,250 cm2 and passes the limit in 2027, Sørdal G1 at 1,990 in 2029 and the new Sørdal G3 runner at 890 in 2031, and Nesvik G2 stays short of it.

## Stump sentence

A competent analyst carries each runner's pitting from its last inspection at the fleet's pitting per running hour and refurbishes Nesvik G2, the only runner that rate takes past the limit before 2032; the step that lands it there is taking an hour run as an hour of wear, when the runners pit only in the restricted band and Nesvik G1 and Sørdal G1 have run there about one hour in nine since they took up frequency reserve in 2022, so Nesvik G1's runner passes the limit in 2027 and spares 4,650 MWh per NOK million against Sørdal G1's 3,820.

## Three rules

Task type: energy-systems-utilities / asset-condition-maintenance, which serves Opportunity Sizing: the call sizes the generation a refurbishment spares against the outage a worn runner would force.

Domain test: the deciding quantity is the year each runner's cavitation pitting passes the repair limit, which hydro asset management forecasts from inspections and duty; a Francis runner pits in the part-load band of its range, so the pitting a unit adds depends on where in its output range its hours fell.

Swap: "which ward should the hospital refit, sparing the most bed-days" keeps the sentence and loses the task: there is no band of an output range, no cavitation, no runner and no duty for a reserve contract to move a machine into.

Layer 1: the 2023 historian migration (tag names, local time with its autumn hours to UTC, a three-day overlap), the old historian's slots wired by the old RTUs until each station's replacement, runner serials against units with two runner changes, decimal commas and Norwegian headers, cumulative governor counters read at overhauls, reserve contracts priced in EUR; each produced by the company's own systems, none placed to be caught.

Layer 2: estimand identification in the wear model: pitting accrues per hour in the band, read across sibling runners against the peaker, and the reserve duty since 2022 moved two units into that band, so the wear per running hour the inspections validated under base-load duty no longer carries forward.

Decisive step: counting each unit's hours inside the restricted band from its own hourly output and carrying pitting at the rate per band hour the inspection pairs give, instead of at the rate per running hour.

Not semantics: every field read correctly (ratings, output, counters, inspection areas, the repair limit, the operating ranges) still leaves the per-hour route on Nesvik G2, because no field states where in the range wear accrues and the reserve units' running hours look ordinary.

Not rule application: no filed rule or procedure says how pitting grows, so executing every stated rule (the limit, the outage weeks, the valuation, the carried duty) still files Nesvik G2; the enumerated wear family (per running hour pooled, per running hour on each runner's own pairs, per counter hour, per running hour with the peaker pooled, per start, per band hour) spreads the pick over four units (Nesvik G2, Øvre Sørdal G1, Sørdal G3, Nesvik G1), while the standing family, the band-hour rate under six estimators (pooled, mean of ratios, median, base-load pairs only, peaker pairs only, least squares), has a spread of zero on the pick and on every graded figure, and what rules the others out is loud only across units: the peaker's ten-fold wear per running hour beside a band rate every pair shares within one per cent.

Analyst test: a strong analyst who reads every file and rule correctly carries pitting at the fleet's rate per running hour and refurbishes Nesvik G2, the default path's answer; only the rate per band hour, counted from each unit's hourly output, gives Nesvik G1.

Estimand: the runner standard and the outage planning note (runner_standard_TS07_rev3.pdf sections 2.1, 4.2 and 6.1; outage_planning_note_2027.docx 1.1 to 4.1) fix the population (the seven units' present runners), the outcome (generation lost to a 14-week unplanned outage from 1 December of the year a runner passes 2,400 cm2), the window (outages beginning 2027 to 2031), the unit (MWh at the generator terminals) and the comparison (per million kroner of the runner shop's quote excluding VAT).

No decoy: nothing is planted to be caught: no memo, draft, briefing, vendor note or stakeholder figure argues for a unit or a wear rate, and the governors' counters are the maintenance system's ordinary record, read at overhauls as it always is.

No certified replay: no published or certified figure is reproduced to recover a hidden method; the wear rate is read from the company's own inspection measurements and nothing certifies the per-hour route.

Lesson: wear accrues where a machine runs in its range, not by the hours it runs, so a duty change that moves a unit into a damaging band breaks a wear rate validated under the old duty; no build on file reads wear from an output band a new duty occupies.

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second use); the reflex row comes from the field's vocabulary for runner condition (equivalent operating hours, starts, hours since overhaul, the last inspection's finding).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 pitting per running hour, fleet pooled with the peaker set aside (Nesvik G2) | TS-07 names the limit, not a rate | governor counters | yes | the base-load pairs fit within 13 per cent | no | yes | no | readable |
| R1 pitting per running hour on each runner's own pairs (Nesvik G2) | no | governor counters | yes | the pairs fit | no | yes | no | readable |
| R2 pitting per start (Sørdal G3) | no | start counters | yes, wear by starts | the pairs do not fit | no | yes | no | readable |
| R3 (decisive) pitting per hour inside 30 to 58 per cent of rating, from each unit's hourly output (Nesvik G1) | the register's operating ranges name the band as an operating range; no clause ties pitting to it | no column holds hours in a band or present pitting | no: the field's reflex counts hours run | no control scores the band | no | no: a relation across each unit's output rows and its rating | the output record is there for the generation and starts asks | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | pitting | total cavitation-pitted area over all blades and the band, cm2 | the worst blade's area | same call | TS-07 4.2: "Pitting means the total pitted area of the runner's blades and band"; every register row sums to its total (asserted) |
| SF2 | the repair limit | 2,400 cm2 of total pitting | a per-blade limit | same call (none is filed) | TS-07 4.2, asserted |
| SF3 | as it stands now | 31 December 2026, the end of the record | the plan date in 2027 | same call | planning note 1.2: "Condition is stated at 31 December 2026" |
| SF4 | the year it will reach the repair limit | the first year at whose end the carried pitting is 2,400 cm2 or more | the year read hour by hour with 2026 repeated | same call (asserted, same year for every passing runner) | TS-07 6.1 |
| SF5 | an unplanned runner outage | 14 weeks from 1 December of that year | 14 weeks valued at the year-round mean | same call (asserted) | TS-07 6.1 and planning note 3.1 |
| SF6 | the generation it would cost | the unit's mean generation over the 14 weeks from 1 December, Norwegian time, in the winters 2021/22 to 2025/26 | every winter since 2016/17 | same call (asserted) | planning note 3.2 |
| SF7 | the planning window | outages beginning 2027 to 2031 | outages ending before 2032 | same call (asserted) | planning note 1.3: "outages beginning in those years" |
| SF8 | the duty carried forward | each unit's 2026 band hours repeated in 2027 to 2031 | the 2022 to 2026 mean | same call (asserted) | planning note 2.4: "as it ran in 2026" |
| SF9 | each unit's runner | the runner installed at 31 December 2026, with its history across units | each unit's latest register row | same call (asserted, the rows coincide) | unit register; TS-07 2.1; planning note 1.1 |
| SF10 | refurbishment cost | the runner shop's 2027 quotation excluding VAT, NOK million | including VAT | same call (asserted) | the quotation and planning note 4.1 |
| SF11 | the restricted band | 30 per cent of rating inclusive to 58 per cent exclusive, on hourly mean output | other band edges | same call (asserted at 25 to 60 and at both edges) | unit register, Driftsområder: "Fra og med" 30 %, Normal from 58 % |
| SF12 | generation (ask) | gross at the generator terminals, MWh, each hour of the record once | the overlap hours twice | not the call (ask) | production report 2025, definitions |
| SF13 | since the start of 2016 (ask) | 1 January 2016 00:00 to 31 December 2026 24:00, Norwegian time | UTC bounds | same figures (the record holds no hour outside, asserted) | production report 2025, definitions: years in Norwegian local time; planning note 1.2 |
| SF14 | starts (ask) | changes from zero to non-zero hourly output between consecutive hours | the governors' start counter | not the call (ask) | production report 2025, definitions |

## Ladder

| Rung | Construction | Runners past 2,400 cm2 in 2027 to 2031 | Call | Margin |
|---|---|---|---|---|
| R0 | fleet pitting per running hour, the peaker set aside, carried from each last inspection (the default path) | Nesvik G2 in 2030 | Nesvik G2 | the only runner past the limit |
| R0' | the same rate from the governors' counters | Nesvik G2 in 2030 | Nesvik G2 | |
| R0'' | per running hour with the peaker pooled | every unit but Sørdal G2 and G3 | Øvre Sørdal G1 | |
| R1 | each runner's own pitting per running hour from its own pairs | Nesvik G2 in 2030 | Nesvik G2 | |
| R2 | pitting per start | Sørdal G3 in 2027 | Sørdal G3 | |
| R3 | pitting per band hour (golden, 0.240 cm2 per hour) | Nesvik G1 in 2027, Sørdal G1 in 2029, Sørdal G3 in 2031 | Nesvik G1 | 4,650 against 3,820 MWh per NOK million, 1.22 times |

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the seven units' runners installed at 31 December 2026 | filed: TS-07 2.1, planning note 1.1 (SF9) |
| 2 Unit of account | MWh of generation; cm2 of pitting; NOK million of quote | filed: planning note 3.2, TS-07 4.2 |
| 3 Attribution window | an hour's output belongs to the hour it was recorded in, Norwegian time | SF13, asserted |
| 4 As-of dating | condition at 31 December 2026, the end of the record | SF3 |
| 5 Version basis | TS-07 revision 3, the only one shipped | C1 |
| 6 Denominator | per million kroner of the runner shop's quote excluding VAT | SF10 |
| 7 Weighting | none, sums over hours and inspection pairs | not applicable |
| 8 Window length | outages beginning 2027 to 2031 | SF7 |
| 9 Boundary inclusivity | the band from 30 per cent inclusive to 58 per cent exclusive | SF11, asserted |
| 10 Rounding path | unrounded throughout, rounded once at the stated units; per-kroner figures agree whether taken from the rounded or the unrounded generation (asserted) | checks.py |
| 11 Tie-break | none; pick and runner-up 830 MWh per NOK million apart | asserted |
| 12 Maturity and censoring | every 2026 hour recorded; inspections dated | C1 |
| 13 Order of operations | carry pitting to the cut, then year by year at the 2026 duty | SF4, SF8 |
| 14 Row order | sums independent of order | C1 |
| 15 Duplicate resolution | the March 2023 overlap counted once (asks; the call is unmoved either way, asserted) | SF12 |
| 16 Identity normalisation | runner serials to units through the register; old historian slots to units through the logged outages before each RTU replacement (asks; the call reads no swapped hour, asserted) | SF9, asserted |
| 17 Netting against gross | gross generation at the terminals | SF12 |
| 18 Dimensional units | MW hourly means to MWh; EUR only in the reserve contracts | C1 |
| 19 Code and status semantics | register fields; hourly output zero means stopped | SF14 |
| 20 Integerisation | starts are whole numbers | C1 |
| 21 Clause scope | TS-07's limit is the removal trigger for the whole runner | SF2 |
| 22 Forward window contents | 2027 to 2031 duty assumed as 2026 (filed), no runner refurbished but the one chosen (note 2.3) | SF8 |

## Literal reader

Executed word for word, the prompt, TS-07 and the planning note give, for each unit's present runner, its pitting at its last inspection and at 31 December 2026, the first year in 2027 to 2031 it passes 2,400 cm2 with 2026's duty carried forward, the generation of a 14-week outage from 1 December of that year at the unit's mean over those weeks of the last five winters, and that generation per million kroner of the quote excluding VAT; the method that carries pitting from an inspection to the cut is left to the evidence, and the inspections fix it: only a rate per band hour fits every runner's pairs, the peaker's included.

## Oracles

- `generator/checks.py`: the three rules on the clean truth (every rung's pick, no cheap route on the call), the standing family's zero spread on every graded figure, every SF row, separation of the asks' handling from the call, the device masses, the input gates and the realism sweep.
- `generator/verify.py`: an independent recomputation of every graded figure from target/ only, the old slots re-assigned from the logged outages.
- `generator/figures.json` and `figures_check.py`: every graded figure.
- `generator/ceiling.py`: the cracker, the mirror and the full includer on the cut pack.

## Ask sheet

- **Ask A, each unit's generation since the start of 2016** (seven figures, MWh to the nearest 100). H18 home: the duty each candidate unit's runner has carried, the production record the investment plan sets beside the call. Path: historian_export_2016_2023.csv (Tidspunkt, seven slot tags), historian_export_2023_2026.csv (time_utc, seven unit tags), historian_tag_map_2023.csv (old_tag, new_tag), maintenance_history.csv (date, unit, event, detail), production_report_2025.pdf (definitions): five files, fourteen columns. Primary device: D2, a label stored before a silent switch. The old historian named its tags by the old RTUs' slots, and at each station the slots were not wired in unit order until the station's RTU was replaced (Øvre Sørdal 1 August 2016, Sørdal 12 June 2017, Nesvik 24 July 2017); the 2023 tag map pairs each old tag with its unit as wired since, and the three-day overlap with the new historian confirms it, so stacking the exports through the map puts every unit's early hours on a sibling's tag. Only the logged overhauls and annual maintenance show it (a unit's tag running while the unit stood for its overhaul), and each station's replacement date bounds it. Hazards: the overlap counted twice (moves every figure by 700 to 3,900 MWh), the autumn hours of the local-time export de-duplicated on their labels (moves every figure by 70 to 370 MWh), the year bounds in UTC (no hour falls outside, asserted).
- **Ask B, each unit's starts since the start of 2016** (seven figures, whole numbers). H18 home: the start duty beside the running duty. Path: the same five files. Primary device: the same slot wiring, which moves the peaker's starts onto a base-load tag (by about 830) and every other unit's by 3 to 15. Hazard: the autumn labels de-duplicated (moves every figure by 2 to 7).
- **Use:** the duty record is how the head of production assets reports what each runner has carried, beside the condition figures.
- **Separation:** the call reads no hour the slot wiring touches (every inspection pair and projection window starts after the station's RTU replacement, asserted), and its graded figures are unchanged under the tag map as given, the overlap counted twice and the autumn labels de-duplicated (asserted in checks.py).
- **Literal pins:** SF12, SF13 and SF14 fix the definitions on the production report's definitions page; no filed sentence names the slot wiring, the overlap or the autumn hours.
- **Full includer:** a response that reads every old tag against the logged outages re-assigns the slots and keeps both asks; no second family sits on these figures, which the pair line below prices.

| Ask figure group | Cracker (lands the call, stacks the exports on UTC with the overlap once and the autumn hours kept, maps the old tags through the 2023 tag map as given) | Golden | Cracker |
|---|---|---|---|
| Øvre Sørdal G1 and G2 generation since 2016 | each carries the other's January to July 2016 | each unit's own | miss |
| Sørdal G1, G2 and G3 generation since 2016 | each carries a sibling's 2016 to June 2017 | each unit's own | miss |
| Nesvik G1 and G2 generation since 2016 | each carries the other's 2016 to July 2017 | each unit's own | miss |
| Øvre Sørdal G1 and G2 starts since 2016 | swapped for January to July 2016 | each unit's own | miss |
| Sørdal G1, G2 and G3 starts since 2016 | the peaker's starts on Sørdal G2 | each unit's own | miss |
| Nesvik G1 and G2 starts since 2016 | swapped for 2016 to July 2017 | each unit's own | miss |

Measured on the cut pack (generator/ceiling.py): the cracker keeps 0 of 14 ask figures (45.0), the mirror on the default path keeps 0 of 14 (12.0), a pair of 28.5; with one of the two a full includer who re-assigns the slots, the pair is 56.0; with both full includers and one on the call it is 83.5, the case the ask layer does not hold.

Pair ceiling: 56.0

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py on the cut pack

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

- 2026-11-03, stage 3: asks as each unit's generation and starts in each year 2016 to 2026 (154 cells), priced on the
  cut pack: the slot wiring reaches about a fifth of the cells and the battery handles the rest, a pair near 72; re-cut
  to each unit's figures since 2016, every one of which the wiring moves.
- 2026-11-03, stage 3: the Sørdal G3 peaker rated 24 MW: a slot swap involving it puts output above its rating on its
  tag, an impossible row the band computation meets; rated 38 MW like its siblings.
- 2026-11-03, stage 3: monthly counters since overhaul controlled the old slots month by month; replaced by the
  governors' cumulative counters read at overhauls, which hold no pre-2016 interval.
- 2026-11-03, stage 3: a seven-day historian overlap moved Sørdal G1's present pitting across a rounding mark when
  counted twice; cut to three days, call-neutral (asserted).
- 2026-11-03, stage 3: reserve capacity (Nesvik G1 9.5 MW against 8.0) and a runner's own pair wear per running hour
  (Nesvik G1's 6 per cent base share in the band) each ranked Nesvik G1 first, a one-dimensional sort on the call;
  rebalanced so Sørdal G1 leads both (asserted).
- 2026-11-03, stage 3: a 450 cm2 per-blade repair rule in TS-07 contradicted the register's whole-runner repairs (no
  blade reaches 450); deleted.
