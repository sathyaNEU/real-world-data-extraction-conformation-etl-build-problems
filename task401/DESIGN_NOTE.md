# task401 design note

Architecture 4, drawn 2026-11-03. The number was handed out against seed RC07 (a supplier's January imbalance bill).
The seed's world could not carry an honest unbanned draw; architecture 1 (a frailty virtual ward against care home
closures, Epidemiology and Public Health) and architecture 2 (a canola hybrid against July heat, Economics and
Econometrics) died at stage 2, and architecture 3 (a GB energy supplier's new-customer satisfaction fall booked to its
billing platform that its quote journey caused, Marketing and Consumer Research) was spent at stage 4, round 2, on an
ask's unfiled re-attribution while its main call held (`## Tried and rejected`, the card's `lineage`). One architecture
per world: architecture 4 moves to Physical and Environmental Sciences, a water and sewerage company's river catchment,
a new dataset and a new shell (`CLAUDE.md`, a dead design is re-rooted at once).

The world: Wendmoor Water, an invented water and sewerage company in the English East Midlands. Its Coldmere Water
Recycling Centre (an activated sludge works serving about 41,000 people and a handful of trade dischargers) discharges
to the River Allery, a lowland, high-alkalinity river whose water body must reach good ammonia status. A continuous
water quality monitor went in below the works in spring 2025 under the company's section 82 programme. From November
2025 the monitor logged a run of days with total ammonia above the good-status standard. In the same weeks the works
switched on an ammonia-based aeration control to save energy (27 October 2025), the housing growth of the last three
years took the works close to its design load, the winter was cold, and Thornlea Dairy, a trade discharger to the
works' sewer, commissioned a new yoghurt line with its own clean-in-place set (3 November 2025). The company's asset
plan carries a GBP 14.2 million nitrification upgrade at Coldmere, and the environment programme submission due to the
Environment Agency in January 2027 needs to say whether that upgrade is the answer.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v4, registered after `guard.py check` at WARN
  (overuse.objective: the slot's objective is fixed by its number; repeat.gate_g and overuse.gate_g: the mechanism that
  carries the stump is a split of failures between sources, honestly `decomposition_attribution`, and the strategy
  window is answered by the decisive move's family below). Structural tests against task36 R1, task83 v1 and task127 v2
  answered by differentiation lines on the card: none of them reads a contributor's excursions through a shared
  process's recovery.
- **Pairing:** Physical and Environmental Sciences (client domain), task type `pollution-source-attribution`, which
  serves Root-Cause Analysis in the taxonomy; objective Root-Cause Analysis; shape 12 (drill-down to one leaf: the
  winter's exceedance days, river to works to the works' failure episodes to the one discharger and its excursions).
- **Strategy:** `population_selection`, pattern C (the serviceable share behind a join): the deciding quantity is the
  share of the exceedance days each option can reach, the dairy's pre-treatment against the works' upgrade, behind a
  join of the dairy's fifteen-minute discharge record and the works' daily effluent record (strategies.md F7, approved
  on 25 and 28). Generators G8 reachability versus magnitude (by load the dairy barely registers; by reach it carries
  most exceedance days), G3 record versus operation, G7 operating window. Gap population (the works' failures are not
  the works' own), objective second (the load apportionment is correct and is not what the decision is scored on).
  The window bans `binding_constraint`, `causal_design` and `decomposition_attribution` (task399, task400, task402); the
  decisive move is the construction of the reachable population, so the label is the move's own family, not a relabel.
- **Data-native sentence:** Thornlea's clean-in-place cycles end in a caustic rinse that its own fifteen-minute
  discharge monitor logs as a run of pH above 11 for twenty to forty minutes; the works receives it hours later, its
  nitrifiers stop for two to four days, and the weekly composite and daily meter volume that charging rests on average
  the run away, so nothing the charging or compliance records hold marks those days.
- **Abstraction sentence:** a small contributor's short excursions switch off a shared process for days, so the share of
  downstream failures that acting on the contributor would reach is read through the process's recovery in two records,
  not apportioned by load. It is not writable against the nearest approved builds: task202 matched an input's physical
  state to a receiver's layers (no process switched off), task303 paired sibling events in one minute to find a shared
  upstream fault (no recovery window, no reach against magnitude), and task182's lineage read a running source's share
  at receptors.
- **Same-puzzle and library tests:** gap, pattern and decision type repeat only older lineage (task36 R1, task83 v1),
  differentiated; the golden is not a named correction (no textbook names "set a discharger's pH log against a works'
  recovery"), and the field's method for the deciding quantity, river source apportionment by load and the works'
  process model, sits at rungs 0 and 1.
- **Layers:** Layer 1 is the company's own record-keeping (fifteen-minute telemetry with logger gaps and the October
  clock change, weekly composites against daily meter volumes, the monitor's provisional and ratified releases with
  maintenance flags, returns in cubic metres against a meter in litres, SCADA tags renamed at the aeration upgrade).
  Layer 2 is the reachable share read through the works' recovery.
- **People** (`guard.py names --geo "United Kingdom, England" --seed 401`; Joanne O'Brien and Elliot Davies skipped,
  architecture 3's card holds them): Gerard Norris (environment programme manager, who owns the submission), Katy Hughes
  (trade effluent officer), Sylvia Phillips (Coldmere's process scientist). The prompt names no one.
- **Furniture redrawn at registration:** task402's redraw took `capacity_planner` into the window, so the role family
  moved to `programme_officer`: the environment programme manager owns the submission the upgrade goes into, the honest
  owner of the call. Forum `regulator_or_inspector` (the Environment Agency's review of the submission), forcing event
  `statutory_or_regulatory_filing`, organisation family `utility_or_infrastructure`, context artifact `register` (the
  trade effluent consent register) and shape 12 all clear the window read off `guard.py check` on the registered card.
- **Sources:** synthetic throughout, built to the structure of the public records it imitates: the Environment Agency's
  water quality archive for spot samples; section 82 continuous monitoring for the river monitor; event duration
  monitoring returns for the storm tank; Water UK and company charges schemes for the Mogden formula; the Water
  Environment (Water Framework Directive) (England and Wales) Directions 2015 for the ammonia standards; levels from the
  wastewater literature (nitrification optimum pH 7.5 to 8.6, inhibited above about 9.5; caustic clean-in-place at 1 to
  2 per cent sodium hydroxide; recovery of two to five days after an upset). Every file's source, date and licence is
  recorded in `metadata.json` at stage 3.

### Go/no-go screens (prototype on the clean truth, 20 redraws each; `scratchpad/t401/a4/proto3.py`, `proto3b.py`)

1. **Levels and the lever against the rivals' estimates.** At documented levels (good-status 0.6 mg/l, 90th
   percentile, lowland high alkalinity; normal effluent 0.5 to 1.5 mg/l and 8 to 20 mg/l during inhibition; dilution of
   four to ten; excursions at 0.95 to 2.1 a week from the new line), the exceedance days attributed to the dairy's
   excursions beat the largest rival estimate (the aeration control, the cold, rain) by a minimum of 13.4 days (median
   20.5) at 0.95 excursions a week and 23.8 (median 46.1) at 2.1, in 20 of 20 redraws each; the window holds 45 to 88
   exceedance days against 3 to 7 the winter before. Every graded figure is set mid-bin at the shipped seed at stage 3.
2. **The golden's own method holds the call.** Every exposure form (recovery windows of one to two, one to three, one to
   four, one to five and nought to three days; the large-excursion and any-excursion definitions) names the dairy with a
   margin over 10 days in 20 of 20. The share of exceedance days inside the windows spreads 0.50 to 1.00 across forms, so
   no graded figure is a raw window share: stage 2 defines the reach on the works' own recovery episodes in its effluent
   record and grades only at the precision every form reproduces.
3. **No easy completion.** The decisive variable (the days inside the works' recovery after an excursion) is not one
   the default path brings in: the dairy enters it only as a load and a compliance record, both normal. With the
   excursions in hand the exposure is binary, so nothing rests on a functional form, and the cracker's flexible default
   (cold in bins, cold by aeration, load by cold, no excursions) still books 61 to 93 per cent of the window's
   exceedance days to the aeration control.
4. **Literal execution.** The filed WHAT (stage 2: the population, outcome, window, unit and comparison, and the reach
   of each option, in the company's own investigation brief) executed literally for every candidate lands wrong: mass
   balance at the monitor names the works; the works' process review on temperature, load and the dated aeration
   control names the control (61 to 93 per cent of exceedance days); a dated before-and-after with every candidate's own
   filed date (the control on 27 October, the dairy's line on 3 November, the housing connections by month) cannot part
   the control from the line a week apart and names the control. The golden needs the excursion days, which the WHAT
   does not tell a solver to compute.

## Default path

1. Load the downstream monitor's fifteen-minute record and the Environment Agency's spot samples, take daily means and
   count the days above 0.6 mg/l from November 2025 to March 2026 against the winter before.
2. Apportion the downstream ammonia by mass balance with the upstream monitor and the gauged flow (the field's river
   source apportionment): the works' effluent carries about nine tenths of the excess, so the works is the source.
3. Model the works' final-effluent ammonia from its SCADA export on wastewater temperature, the incoming load and the
   aeration control's go-live (the field's process review): the control's term carries most of the winter's excess,
   the cold the rest, and the works runs at 93 per cent of its design load.
4. Check the trade dischargers by load and compliance: Thornlea's ammonia load from the charging data (weekly
   composites times daily volumes) is a few per cent of the works' and its monthly pH compliance passes, so it is
   dismissed; storm tank spills and upstream farming explain a handful of days.
- **Ends on:** the aeration control and nitrification capacity in cold weather; the GBP 14.2 million upgrade goes into
  the submission.
- **Golden:** Thornlea Dairy's caustic clean-in-place excursions: most of the winter's exceedance days fall inside the
  works' recovery after an excursion in the dairy's own fifteen-minute record; on excursion-free days the works meets
  its permit at equal temperature and load and the aeration control costs nothing, so the upgrade would reach few of
  the days and pre-treatment at the dairy would reach most.

## Stump sentence

A competent analyst apportions the Allery's ammonia to the works by mass balance, models the works' final-effluent
ammonia on temperature, load and the aeration control, and books the winter's exceedance days to the new control and
the works' nitrification capacity, ending on the GBP 14.2 million upgrade, because they never set Thornlea Dairy's
fifteen-minute discharge record against the works' daily effluent record, which puts most of the exceedance days inside
the works' recovery after the dairy's caustic excursions.

## Three rules

- **Task type:** physical-environmental-sciences / pollution-source-attribution, which serves Root-Cause Analysis.
- **Domain test:** the deciding quantity is the share of the downstream exceedance days that fall inside the days the
  works' nitrification needs to recover after a caustic excursion in one trade discharger's own fifteen-minute record,
  worked as river source apportionment through the works' process response rather than by each source's load.
- **Swap:** "most of the Allery's exceedance days follow Thornlea's caustic excursions within the works' recovery, so the
  upgrade would not stop them", rewritten as "most of the ward's infections follow the supplier's batches", loses the
  dilution, the nitrifiers' recovery after a pH excursion and the consented strength that make the share computable,
  and stops reading.
- **Layer 1:** fifteen-minute telemetry with logger gaps and the October clock change (the dairy's monitor); weekly
  composites against daily meter volumes (charging); provisional against ratified monitor releases with maintenance
  flags (the river monitor); cubic metres against litres (the returns against the meter); SCADA tags renamed at the
  aeration upgrade (the works). Each is produced by the system named; nothing is placed to be caught.
- **Layer 2:** estimand identification: the share each option reaches is the population of exceedance days inside the
  works' recovery after an excursion, built by joining two records, not the load each source sends.
- **Decisive step:** set Thornlea's fifteen-minute pH record against the works' daily effluent record, mark the days
  inside the works' recovery after each excursion, and read the exceedance days on and off them: on excursion-free days
  the works meets its permit at equal temperature and load, so the aeration control and the capacity reach almost none
  of the days.
- **Not semantics:** every field reads plainly (pH units, mg/l, the monitor's flags, the consent's limits), and reading
  each correctly still leaves the mass balance on the works and the process model on the aeration control and the cold;
  no field, code or definition marks an excursion as a trigger of anything at the works.
- **Not rule application:** no filed rule or procedure links a discharger's pH record to the works' failures (the
  consent's pH limits are met; charging rests on weekly composites), so executing every stated rule files the control.
  The enumerated family the WHAT leaves open (recovery windows of one to five days, excursion thresholds from pH 10.5 to
  11.5, the large-excursion and any-excursion definitions) spreads 0.50 to 1.00 in the share of exceedance days across
  20 redraws with every member naming the dairy; the standing family (the consent's own excursion definition, recovery
  read from the works' effluent record) is measured at stage 2 and graded only at the precision it shares; nothing does
  the ruling-out but the two records set side by side.
- **Analyst test:** a strong analyst with every field read and every rule applied apportions by mass balance to the works,
  models the works' effluent on temperature, load and the aeration control, dismisses the dairy on load and compliance,
  and ends on the aeration control and nitrification capacity, backing the GBP 14.2 million upgrade (`Ends on:`).
- **Estimand:** filed at stage 2 in the company's investigation brief for the submission: the population (every day from
  1 November 2025 to 31 March 2026 at the downstream monitor), the outcome (a day whose mean total ammonia exceeds the
  good-status standard), the window, the unit (the monitor day) and the comparison (the same months a year earlier),
  with the question each option answers (which days it would have prevented); no sentence names a recovery window, an
  excursion or a join.
- **No decoy:** nothing is planted: the aeration control's go-live, the housing growth, the cold and the storm spills are
  real changes with their own records; no memo, draft, briefing or stakeholder figure argues for the upgrade or blames
  the control or the dairy.
- **No certified replay:** no certified or published figure is reproduced to recover a method; the golden's construction
  reproduces nothing in the pack.
- **Lesson:** a source's share of a failure is its reach through the process that fails, not its share of the load: a
  small discharger whose excursions stop a works' nitrification owns the days the works needs to recover, and only its
  own high-frequency record set against the works' daily record shows it; no build on file teaches a process switched off
  by a minor contributor's excursions.

## Tried and rejected

- 2026-11-03, the seed's world (RC07, a supplier's January imbalance bill against plant trips and low wind), every
  candidate screened before the card. The trips' effect on the supplier's own imbalance volume at the system price is
  settlement accounting: each unit's metered shortfall against its notified output in the window before the desk can
  re-trade, priced per settlement period, reconciles exactly to the bill, so nothing is left to decide (rule
  application). The price the supplier would have faced without its own units' trips re-runs the system's price
  formation on the changed path, task398's spent insight in other nouns. Netting the desk's replacement trades out of a
  trip's cost is the same insight again (the cause owns the response it triggered). Which settlement periods a trip owns
  (gate closure, the share of an interval) is a market rule or a time-semantics read, banned as decisive. The cost
  spike's drivers identified from interval data need a driver the settlement data does not meter, and in this market
  every driver is metered. Dual imbalance pricing makes the portfolio's net position matter, but executing the price
  rule on the with-and-without positions is rule application. The honest strategy, `decomposition_attribution`, and the
  seed's forum (the board) are both held by task398 in the window. Moved, per `CLAUDE.md`.
- 2026-11-03, other moves screened and set aside before this draw: gas turbine inlet icing in freezing fog read against
  temperature (the winter measures on the table name the mechanism, so a reader checks each one's conditions and lands
  it; two cheap routes); a groundwater nitrate rise read against travel time through the unsaturated zone (task202's
  reach-the-receptor insight in other nouns, and the field's first move); a bathing water's sources separated by marker
  decay in transit (task202's reach and task248's transit loss); selective in-migration behind a widening mortality gap
  (task68's entrants and task134 v2's newcomers, and the prior-diagnosis read lands the decision without it); depletion
  of the frail by a winter's deaths before an intervention's evaluation (dead on lever at realistic excess mortality, as
  task173's screens found for mortality displacement, and its frailty proxy forks the expectation); the Will Rogers
  stage migration (the field's stage-specific comparison collapses into which stage field to read, data semantics);
  attenuation by a mediator's or a predictor's unreliability (task262's insight); regression dilution of a risk factor
  in a disparity decomposition (task262 again); a funnel's downstream rate falling when an upstream filter loosened (the
  end-to-end funnel is the field's reflex); a two-stage complaint escalation's selection (the per-complaint view lands it);
  a mode or non-response shift in a satisfaction tracker (task121 v4's linkage and halo).
- 2026-11-03, prototypes before the card (`scratchpad/t401/proto1.py` to `proto3.py`, expected values with Poisson draws):
  winter-only counts in a city of 600,000 left the default and the golden overlapping across draws (default 5th to 95th
  percentile 23 to 179, golden -38 to 119), so the build runs at integrated-care-system scale over October-to-September
  years with the closures in the year between the baseline and the pilot; there the default's expectation is 912 (spread
  208) against a golden of 392 (spread 215, truth 389), and the trend-adjusted golden forms agree within a median of 6.4
  admissions once the framework files the comparison; without the comparison filed, the no-trend form differs from them
  by a median of 77 (a fork the framework's comparison sentence closes, a WHAT naming no method).
- 2026-11-03, architecture 1 dies at stage 2 on the coordinator's realism check, before any data was cut. Set to published
  English levels (a care home resident aged 80 and over about 0.70 to 0.75 emergency admissions a year, community
  residents by band 0.24 to 0.58, a same-age ratio near two, not the prototype's five), the composition lever is about
  113 admissions for the 440 Core20 residents the closures moved (sd 26), against draw-to-draw spreads of 202 in the
  default and 214 in the golden on a one-year baseline and about 160 on three years (`scratchpad/t401/proto4.py`, 400
  draws). A bar at the midpoint separates default above from golden below in 22 per cent of draws (27 on three years);
  900 residents moved gives 41 to 51 per cent and 1,400 gives 58 to 72, and 1,400 is two fifths of Core20's care home
  places in one system closing in a year, which no honest care group failure produces. A larger 80 and over population
  scales the spread with the lever, and a bar nearer the truth only moves the coin flip. The stump was the noise. Re-rooted.
- 2026-11-03, the redraw's other candidates, set aside before the card: regression to the mean of units chosen on a
  noisy outcome (task130 v3 landed it; task149 and task174 rejected it on that lineage); a satisfaction fall read against
  the conditions each respondent met, or a tracker's mode or response shift (task121 v4); a storable good's purchases
  pulled forward before an announced price rise and paid back after (the pre-rise spike is the pack's largest movement
  and announces the step); a distributor's orders falling as channel stock is drawn down (sell-through is the field's
  reflex and lands it); a local policy confounded by a common shock loading on each unit's exposure (the council
  furniture is banned in the window and the exposure needs data no operator holds); transformer insulation ageing under
  new loads (electricity is spent, task129, task196, task201, task303, and F6's 46 already holds a rate stationary in a
  constructed exposure); in the crop world itself, a hybrid placed on clubroot or hail-struck fields (a lab result or an
  adjuster's claim names the field, readable), and a hybrid whose own later flowering met the heat (`crop2.py`: a three-day
  shift moves the season-long panel only 3 to 5 per cent, and the forward step then needs a climatology fork).
- 2026-11-03, prototypes for architecture 2 (`scratchpad/t401/crop1.py`, `crop3.py`, ten weather draws each, the
  hybrid's own effect nil and equal phenology): with most of the hybrid's seed late by 8 to 14 days, the season-long
  panel files minus 9.1 per cent (sd 9.8 across weather draws), farm-by-year effects minus 9.3, a linear seeding-date term
  minus 7.0, raw 2026 means minus 11.6, the flowering-window exposure minus 0.1 (sd 0.9), its variants (thresholds 28 and
  31 C, windows 14 and 22 days, 490 and 550 heat units to flower) minus 3.5 to plus 0.5, and fields seeded on the same
  days on the same farm minus 0.6 (the same insight by matching). The spread across draws is the weather's: the pack's
  July heat wave and seed delay are set by design, never picked from draws.
- 2026-11-03, architecture 2 dies at stage 2 on its own ladder (`generator/ladder.py`, seed 4012026, measured at commit
  7d3a3cd), before any data was cut. First, the golden's own method forks the main call: the flowering-window variants
  land +2.1 (28 C), -2.5 (31 C), -12.0 (a 14-day window), +3.4 (a 22-day window), -8.2 (490 heat units to flower) and
  +4.9 (550 units) against the 5 per cent bar, so two agronomically defensible variants drop the hybrid and four keep
  it; filing the window or the heat metric would name the decisive step, and the generator cannot close the spread under
  realistic catch-up (a 17-day seeding gap became a 6-day flowering gap). Second, the stump rests on a functional-form
  choice: the default path's own rung 4 already rebuilds seeding dates from the seeder's logs, and every flexible form of
  that variable then lands the golden (seeding-week bins +3.6, a cubic +4.4, same-day matching +9.3); only a linear term
  stays wrong (-10.1 in the season panel, -8.3 with farm-by-year effects), so Gate F would rest on the solver choosing a
  straight line. Spent; one architecture per world, so the crop and weather world is closed to this slot. Re-rooted at
  architecture 3 in another client domain, world and dataset.
- 2026-11-03, architecture 3's draw, candidates set aside before the card. In the never-built satisfaction cell, the
  client card's moves (Shapley shares, a Net Promoter change's multinomial error, penalty against reward, loyalty read
  on later behaviour) are reflexes, and reading a fall on the conditions each response was made under is task121 v4's.
  A broadband provider's speed promise against delivered speed died on the regulator's own reflex (the share of plan
  speed delivered is the standard metric). The energy quote mechanism in the supplier's base-wide relationship tracker
  carried 0.54 points (1.35 with 2025's joiners using a fifth more) against a fall whose draw-to-draw spread is 0.66
  (`scratchpad/t401/a3/proto_e2.py`), architecture 1's death in other nouns, so the build runs on the six-month
  new-customer tracker. In the concentrated form a first harness with the platform's own effect at 1.3 points left the
  golden's 10 and 20 per cent flags (0.98, 1.78) under the residual (`proto_e3.py`); at the platform's realistic small
  effect the standing forms clear it (`proto_e4.py`). Other cells screened: education multilevel (the client's three
  cards are reflexes; teacher reassignment and special-needs assessment waits fail screen 1 or repeat the actor family),
  health equity (an inhaler switch run practice by practice is task400's staggered rollout; discharge after a missed
  appointment repeats task402's broken-off cases), pollution source attribution (every wind, tide and capture-zone route
  is task202's reach), water network reliability (the isolation extent per burst is one group-by; transients read
  through topology sit beside task303), the human factors cells (the pairing is barred against task400), and
  interpretability (ruled a backdrop at task129 v1).
- 2026-11-03, stage 2 on architecture 3, three cuts. (a) The first world set the first Direct Debit from the quote, so
  the review rise was a near-copy of the gap and a solver asking why payments rose walked to the quote; the payment is
  now set from the meter point's industry quantity at registration, and the Direct Debit change books 0.35 points and
  names the platform (`## Ladder`, R2b). (b) A Direct Debit policy document stating that rule was drafted and dropped:
  its sentence on industry quantities would send a reader to set quotes against quantities, and the golden never needs
  it. (c) The contact centre ask and its two call logs were cut for budget; the contact rival stays on the tracker's own
  contact question. The asks' first devices as drafted (stale legacy status, re-runs keyed on the legacy reference,
  withdrawals) were each executable from the cutover plan's and the asking sentences' own pins, so they were re-sited
  onto an erroneous-transfer return, a reload chain with a pilot twin, and a gas registration raised under its own
  reference.
- 2026-11-03, stage 2 on architecture 3, the full includer (precut FAIL: one primary per ask). The coordinator's candidates
  were screened against the full includer: (a) Ask B, an account whose gas was removed between its first load and its
  reload: the full includer that walks the chain takes the last load's row, fuels with its week, and keeps the block, and
  the sentence that closes the fork (the fuels that load carried) makes it a work order; (b) Ask C, broker switches
  registered on the broker's lead reference: noticing the unmatched reference and joining on the prospect is one act, and
  every quote under a broker's lead is a broker quote, so nothing goes wrong after the notice; re-sited onto a broker sale
  re-quoted by the phone team after the registration; (c) Ask A, two-rate registers alone: a work order once the plan
  files day and night together; the device is the register set changing at an exchange, and gas has no register. Also set
  aside: split-fuel legacy accounts merged on load (one platform number on two rows, and the filed unit, the account the
  platform holds, makes it a work order); a requested supply start on legacy sales (the industry registration date in the
  quantities fixes it in one act); fuel add-ons across the migration renumbering (the solver who landed the call already
  built the crosswalk).
- 2026-11-03, stage 2, the full includer at 36 of 58 (62 per cent of the ask weight, 79.1 on the call): one second device
  per ask on its own block left a full includer and an on-call cracker pairing near 62. Widened: Ask A gained a change of
  occupier on the same meter points (the primary's own repair keeps the leaving account), Ask B's returned accounts take
  both fuels, Ask C's re-quotes reach every channel; the full includer keeps none of the 58.
- 2026-11-03, stage 4 round 1 (judge NOT_DETERMINISTIC and SOLUTION_WRONG, SEND_BACK light on the workbook asks alone, main
  call forced, Gates G and H passing; reader clean on the main call): Ask B's second device, the 410 accounts loaded and
  returned to the legacy platform, died to its own WHAT. Filing what counts as moved (the new platform billing the account
  at the end of 2 November 2025) closed the judge's fork 1 and made the returns a work order: with the sentence filed and
  nothing else changed, the full includer keeps 16 of 18 Ask B figures (`scratchpad/t401/fix/remeasure_b.py`). The returns
  stay as a hazard; the second device is re-sited onto 389 accounts the legacy platform took back during 2026 on a change
  to prepayment, where the repair the sentence invites is right before the close and wrong after it (the full includer
  keeps 0 of 18).
- 2026-11-03, stage 4 round 1, the Gate A anomaly: the change-of-occupier branch drew the leaving account's supply start
  without reference to its closure, so two Closed accounts began after they closed and took their meter points from the
  live occupiers (Eastern and London one account short under the golden's own rule). The leaving account's start now
  precedes its closure, asserted over every account. Fork 3 was closed by "no withdrawn registration counted" rather than
  by dating the boundary in the asking sentence (shorter, and true whatever the date), with every withdrawal now dated
  before the start it requested, as switching allows.
- 2026-11-03, stage 4 round 2, architecture 3 spent. The round-2 judge returned NOT_DETERMINISTIC, SEND_BACK (narrow), on
  the switches table: "credited to the sale it was registered on", read word for word, takes each registration's
  quote_ref, and 596 Phone registrations name a quote dated 2 to 10 days after the registration; the golden moves each to
  the prospect's latest quote on or before it, a rule no file states, and for 94 of those prospects latest against
  earliest moves about 20 cells. The literal ask executor in checks.py had carried the re-attribution as though it were
  the field's own value, so it never saw the fork. Every round-1 finding closed, and the main call held in both rounds
  (forced and reproduced; Gate F good; Gate G analytical_non_defect; Gate H analytical), but the judge noted that
  Critical Component 2's "more than half" depends on the cut (a binary covered split puts 14 per cent of the fall on the
  quote mix, five bands 60, eight bands 85, the kinked model 75). A second round without APPROVE spends the architecture
  under the round-1 ruling; the slot re-roots at architecture 4 in another domain, world, dataset and shell. Lessons: a
  literal executor takes every field at its face value, so a golden that overrides a field's own link (a reference, a
  date, a status) carries a filed WHAT or the data are regenerated so the face value is the golden; and every quantity
  the write-up states for the main call holds at every natural granularity of the comparison, or is stated so it does.
- 2026-11-03, architecture 4's draw, candidates set aside before the card (four go/no-go screens, `scratchpad/t401/a4/`).
  The strategy window (binding_constraint, causal_design and decomposition_attribution held by task399, task400 and
  task402) bars the natural attribution labels, so each candidate's decisive move was labelled before it was priced.
  (a) An online retailer's checkout conversion fall booked to a checkout release, caused by a collection partner
  withdrawing urban points while adding as many in suburbs (`proto1.py`, `proto2.py`, 20 redraws): it fails screens 2
  and 3, since the access effect acts only on latent collection-preferring shoppers through a continuous distance, so its
  share runs 0.84 to 2.50 points across defensible exposure forms and the release's residual -0.62 to 2.67, and it fails
  the swap test (collection points read the same as clinics); it also sits beside task129's surroundings exposure and
  task399 v3's supply behind a journey, and task177 had called a nearest-locker reading a replay. (b) Opportunity to
  learn in a primary trust's mid-year maths tests, a new scheme's sequence placing tested topics after the test date:
  an intrinsic fork, because the scheme's sequencing is itself a counterfactual cause of the measured spring fall, so
  the default's "the scheme" and the golden's "the sequence against the test date" name one candidate. (c) A school
  trust's illness absence driven by classroom ventilation cut to save energy: at published levels (about 0.5 to 0.9
  points of absence per 1,000 ppm) the lever is a fifth to a half of the rise. (d) Deploy-spanning journeys breaking
  in-flight checkouts: task129 v1 spent the first-use-after-a-version-change shape. (e) Split shipments across
  fulfilment centres: task175's seed and task277's reflex. (f) Tampered HGVs read from roadside remote sensing: task202
  screened it. (g) Storm overflows against the load apportionment model: the overflow record is the zeitgeist's first
  check, and the move is attribution. (h) A charity upgrade appeal's anchored figure, a norm boomerang and a goal
  difficulty gap: the levels are not documented, or the gap is architecture 3's family. (i) Composition designs in
  every cell: this slot has spent two (architecture 1's closures, architecture 3's mix standardisation).
