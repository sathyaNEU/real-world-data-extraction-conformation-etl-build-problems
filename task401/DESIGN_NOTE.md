# task401 design note

Architecture 1, drawn 2026-11-03. The number was handed out against seed RC07 (a supplier's January imbalance bill,
three times a normal winter month, blamed on low wind by the trading desk and on plant trips by operations, with the
board filing the trips' cost as the reference figure for an outage-cover decision). The seed's world could not carry an
honest unbanned draw (`## Tried and rejected`, the first lines), so the build keeps the seed's decision shape (one
figure filed as the reference for a buy-or-not decision on a protective programme, with rival explanations for a
move) and moves to another client domain, world and dataset under the same objective and number (`CLAUDE.md`, a stuck
build is unblocked, never parked; task398 and task400 moved on the same grounds).

The world: the Kirkhaven integrated care system (an invented city in the north of England and four neighbouring
boroughs, about 2.6 million people). Kirkhaven Community Healthcare NHS Trust ran a frailty virtual ward (hospital at
home for frail older people) for residents aged 80 and over in the system's Core20 neighbourhoods (the small areas in
the most deprived fifth of England's by the 2019 index) from 1 October 2025. The integrated care board will commission
the ward across the whole system from April 2027 only if the pilot year prevented at least a filed number of emergency
admissions among those residents. Between the year before the pilot was commissioned and the pilot year, the Wrenford
Care Group went into administration and eleven of its Core20 care homes closed; their residents moved to homes outside
Core20 or outside the system.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v1, drawn and registered 2026-11-03.
  `guard.py check` on the draft returned WARN: `overuse.objective` (root cause in 4 of the last 12; the number sits in
  the root-cause range) and `repeat.gate_g` against task400 (answered below). Two older structural repeats are
  differentiated on the card (task156 v2, task238, task303). Nearest driver 0.06 (task89 lineage); task156's v1 loop 3
  lineage (a pool whose leaving rate falls as its fast leavers go first) reads 0.05 and is screened below.
- **Pairing:** Epidemiology & Public Health (client domain) / `health-equity-disparity-decomposition` / Root-Cause
  Analysis. The task type serves Root-Cause only, and `epidemiology-public-health x root-cause` has never been built
  (`guard.py coverage`, 2026-11-03).
- **Objective and call:** whether the pilot cleared the board's bar, decided by how many emergency admissions of Core20
  residents aged 80 and over the ward prevented in its pilot year. The move to explain is the fall in Core20's admission
  rate against the rest of the system; the rivals are the ward, the winter vaccination drive, the season, and a change
  in who Core20's residents aged 80 and over were. The decision faces forward (the extension runs from April 2027); the
  pricing is retrospective because the commissioner's bar is set on the pilot year, the only year the ward ran. The tag
  stays Root-Cause Analysis: the work is naming what moved Core20's rate, rivals ruled out on the record; nothing is
  forecast.
- **Shape:** `other`, written out in `## Ladder` at stage 2: the call (bid or not) with the prevented admissions, the
  move and its pieces, and the asks' repeated units.
- **Strategy and Gate G:** `composition_mix`, Gate G `decomposition_attribution`. The decisive move is F5's own form: a
  rate measured on one pool (Core20's residents aged 80 and over in the year before commissioning) applied to a pool
  whose mix on a property no outcome or population column carries (living in a care home, read from the care homes'
  own records) has moved. It is not a split of one total between two movers: the graded quantity is one causal
  quantity, the admissions the ward prevented, and the decisive step is the expected admissions those residents would
  have had. Gate G names the mechanism carrying the stump, the fall booked to the wrong cause. `repeat.gate_g` against
  task400 is answered: Gate G is the honest label for what carries this stump, and the decisive families differ
  (task400's natural comparison inside a staggered rollout against a composition shift here).
- **Gap, pattern, generators:** gap population (the pool the baseline rate was measured on is not the pool the pilot
  year evaluates), then time (the closures fall between the two years); pattern none; generators G14 (does the pooled
  rate apply to this pool), G6 (did the population shift under it).
- **Furniture:** forum `executive_team` (the trust's executive decides whether to bid for the extension), forcing event
  `purchase_order_or_contract` (the board's commissioning round for April 2027 closes on a filed date), organisation
  `hospital_or_health_provider` (a community health NHS trust), role `programme_officer` (the trust's head of business
  intelligence, who owns the pilot's evaluation), context artifact `capacity_report` (the care capacity tracker the
  discharge teams read every week), calibration none. None is held by the last three live cards (task398, task399,
  task400).
- **People** (`guard.py names --geo "United Kingdom" --seed 401`): Aimee Williams (head of business intelligence, owner
  of the evaluation framework), Gerard Norris (director of community services, the ward's sponsor), Sylvia Phillips (the
  board's commissioning manager for older people's services). None appears in the prompt.
- **Data-native sentence:** a care home resident aged 80 and over goes into hospital as an emergency about five times as
  often as a neighbour of the same age living at home, care home places sit unevenly across neighbourhoods and move with
  the care market rather than with anything the NHS records, and the admission and registration extracts carry each
  person's neighbourhood but not whether they live in a care home, so a care group's failure between two years moves
  Core20's admission rate with no change in anyone's risk.
- **The abstraction sentence** (what a reviewer holding this build beside its nearest approved build would call the
  same): "a group's rate is read before and after an intervention against the other groups, but between the periods
  the group lost a block of members whose rate is several times the rest's, to an event no outcome or population record
  names; the earlier rate does not fit the later pool, and standardising on that property, read from a capacity record,
  leaves the intervention its own share." Written against every driver `guard.py mechanisms --objective root-cause`
  prints and the near composition drivers on file; it cannot be written against any of them (the screen below).
- **Same-puzzle and same-driver tests:** gap population, decisive G14, decision go-or-hold repeats no card in the last
  twelve; the older repeats are differentiated on the card.
- **Library test:** the golden is not a named correction applied as a card states it. The field's method for the
  deciding quantity, age-standardised rates compared across the deprivation fifths in a difference in differences, sits
  at rung 1; the decisive step is recognising that this dataset violates that method's precondition (a stable pool on
  the property that drives the rate), which the data shows only through the care homes' own records.

**The semantic screen, one line per nearest build** (`guard.py mechanisms --objective root-cause`, plus the near
composition drivers the guard printed):

- task13 spends re-attribution by physical evidence against a filed reason label in an exceptions-only log: nothing here
  is relabelled.
- task11 spends a threshold rebate's value on a ledger rebuilt from omitted channels: no threshold or ledger.
- task36 spends a filed eligibility exclusion and a counterfactual conditioned on a property that cancels it: no filed
  exclusion; the counterfactual here is a pool's mix.
- task50 spends exposure inside a funded window projected by a filed issue order: no window or order.
- task72 spends the owner at the time under a filed clause across a hand-over: no ownership.
- task84 spends identical copies that compete and raise each other's price: no competition.
- task111 spends which measured cause still operates in the forward window: the window here is closed and the cause is
  a composition change.
- task500 spends a matched-reference method, a spillover through another entity's register and a hold line crossed by
  block consolidation: none of them.
- task129 spends a rise booked to a provider that arises outside the zone it touches and scales with each unit's
  surroundings: no surroundings property; the property is a care setting whose population a capacity record shows
  moving out of the group.
- task121 spends rest rebuilt from worked periods, a self-healing exposure, identity behind signed-out accounts, a daily
  cycle read case-crossover, the halo in ratings, and feeder schools' carried effect: none of them.
- task202 spends how much of each source's input reaches the layer the response draws on: nothing travels or arrives.
- task398 spends a path-dependent counterfactual re-running a filed rule on the changed path: no rule is re-run; the
  expectation is built on the pilot year's own pool.
- task399 spends an advocate's absence at each call and unmet demand behind an empty capacity stock: the capacity record
  here says who is in the pool, not what demand went unmet.
- task400 spends a staggered rollout's natural comparison separating a system change from its users: no rollout.
- task156 v1 loop 3 (lineage) spends a pool whose leaving rate falls as its fast leavers go first: no dynamic selection
  here; an identifiable stratum was removed by an outside event, and its members' rates did not change.
- task68 spends entrant inflow masking a matched incumbent base's collapse: no entrants; the construction is a
  setting-standardised expectation, not a matched panel.
- task134 v2 and task83 spend a hazard by time since entry and conditioning on prior treatment history: the property
  here is a place of residence, not a history.
- task262 and task473 spend an attenuation correction and a detection share: nothing is mismeasured.

The decisive step is none of these in other nouns.

- **Sources** (every file synthetic, generated by `generator/` from seed 401, invented world, no real organisation;
  licence CC BY 4.0, recorded in `metadata.json` at stage 3): emergency admission episodes of residents aged 80 and
  over at the system's three acute trusts (the spine), the quarterly GP registration extract, the 2019 deprivation
  lookup and the 2011-to-2021 small-area lookup, the regulator's care home register, the care capacity tracker, the
  trust's pilot evaluation framework, the board's commissioning letter, the ward's monthly returns, the winter
  vaccination uptake, and distractors named in `metadata.json` (stage 2 fixes the list).

## Default path

The route a competent analyst builds without thinking, from the prompt's words and the files' grain, with the field's
method for the deciding quantity in it:

1. Collapse the three acute trusts' episodes into continuous inpatient spells (one trust's patient administration
   system changed in April 2024; transfers between trusts inside one spell count once), keep emergency admissions of
   residents aged 80 and over, and place each by the patient's small area through the 2021-to-2011 lookup into Core20 or
   the rest of the system.
2. Build the population at risk from the quarterly registration extract, by Core20 and age band, for each year from
   October to September.
3. Compute age-standardised emergency admission rates for Core20 and the rest in the baseline year (October 2023 to
   September 2024) and the pilot year (October 2025 to September 2026), and check the pre-period: the two groups moved
   in parallel from 2021-22 to 2023-24.
4. Take the difference in differences as the ward's effect on Core20's rate and multiply by Core20's pilot-year
   population: the admissions the ward prevented. Read the vaccination drive and the season against it (both small).
5. Read the result against the board's bar and recommend.

Ends on: about 1,000 admissions prevented in the pilot year, clearing the bar of 750, so the trust bids for the
extension (the prototype's expected default is 912 with a draw-to-draw spread of 208; stage 3 fixes the shipped figure).

Golden: about 400 admissions prevented, below the bar, so the trust does not bid: Core20's pilot-year residents aged 80
and over held about 440 fewer care home residents than its baseline-year residents, after the Wrenford homes closed,
and the expected admissions standardised to the pilot year's mix of care home and community residents by age band, with
the change outside Core20 standing for Core20's change, leave the ward about 400 (the prototype's trend-adjusted forms
agree within a median of 6 and at most 30 admissions; stage 3 fixes the shipped figure, mid-bin).

## Stump sentence

A competent solver collapses the episodes into spells, places every admission in Core20 or the rest, takes the
age-standardised difference in differences from the baseline year to the pilot year and files about 1,000 admissions
prevented (the `Ends on:`), clearing the bar of 750, so the trust bids for the extension; the step that lands it there
is applying Core20's baseline-year rate, set while the eleven Wrenford homes were full, to a pilot-year pool that held
about 440 fewer care home residents, whose emergency admission rate is about five times the community's, so the
difference in differences books the closed homes' missing admissions to the ward.

## Three rules

Task type: health-equity-disparity-decomposition (Epidemiology & Public Health), which the taxonomy serves with
Root-Cause Analysis: the move is a narrowed deprivation gap in emergency admission rates, decomposed into what the
population's mix did and what the ward did.
Domain test: the deciding quantity is the admissions the ward prevented, read as expected against observed admissions
for the population actually at risk, the expectation built by indirect standardisation on the strata that drive the
rate (age band and care setting) with the comparison area's change standing for the counterfactual trend.
Swap: "how many sales did the loyalty scheme add in the poorest postcodes, against the other postcodes" keeps a
difference in differences but loses the care homes whose residents carry five times the rate and whose places move with
a market the outcome records never see, so the call stops reading the same.
Layer 1: three acute trusts' episode extracts to be collapsed into continuous spells across a patient administration
system change and inter-trust transfers (the trusts' own systems); 2021 small-area codes in the extracts against 2011
codes in the deprivation lookup, with splits and merges (the national geography); quarterly registration snapshots
against an October-to-September year (the registration service); a capacity tracker with missed weekly returns and homes
re-registered under a new operator (the care providers' own returns); nothing placed to be caught.
Layer 2: `estimand_identification`: the counterfactual for the pilot year's own residents, which the baseline rate
supplies only for a pool with the same mix on the property that drives the rate.
Decisive step: recognising that Core20's pool of residents aged 80 and over lost several hundred care home residents
between the two years, and building the expected admissions on the pilot year's own mix of care home and community
residents by age band rather than carrying the baseline year's pooled rate forward.
Not semantics: every field, code, unit and date read correctly (spells, small areas, ages, the year, the bar) still
leaves the difference in differences on about 1,000, because no outcome or population column says who lives in a care
home; the property is a relation between each person's address and the care homes' own register and returns.
Not rule application: the evaluation framework files the population, the outcome, the years, the comparison and the
bar, and no filed rule or procedure says on what the expected admissions are standardised; the enumerated family
(crude, age-standardised and ratio differences in differences, with or without the vaccination and season terms)
spreads from about 850 to about 1,150, all over the bar, while the standing family (expectations standardised on care
setting, by age band or not, with the comparison's change pooled, by setting or by stratum) spreads by a median of 6
and at most 30 admissions around about 400, and the property that rules the enumerated family out is visible only in the
care homes' records, which the field's method never opens.
Analyst test: a strong analyst who collapses the spells, maps every small area and reads the framework and the bar
correctly takes the age-standardised difference in differences and files about 1,000 admissions prevented, clearing the
bar of 750, when the setting-standardised expectation leaves about 400.
Estimand: the trust's pilot evaluation framework (a governing document in the pack) files the population (residents
aged 80 and over of Core20 small areas registered with the system's practices), the outcome (emergency admissions
counted as continuous inpatient spells beginning in the year), the window (the pilot year, October 2025 to September
2026), the comparison (the year before the pilot was commissioned, with the change outside Core20 over the same years
standing for the change Core20 would have seen without the ward), and the quantity (the admissions the pilot-year
Core20 residents would have had without the ward, less the admissions they had); the board's letter files the bar.
No decoy: nothing is planted; the care homes closed because their operator failed, the trust's own interim reading of
the pilot is not shipped, no memo or draft argues a figure, and no stakeholder figure is set to be overturned.
No certified replay: the method is not recovered by reproducing published figures; no file publishes a prevented-
admissions figure, a standardised rate or an expectation the golden must match.
Lesson: an evaluation that carries a baseline rate onto a later pool is right only if the pool kept its mix on what
drives the rate, and a care market can move that mix between two years without any health record noticing; no build on
file teaches a composition shift read off the providers' own capacity record behind an intervention's credited effect.

## Survivor anatomy

Actor: the property that decides, whether each resident aged 80 and over lived in a care home in each year, has no
column in the admission or registration extracts; it is a relation between a person's address and the regulator's care
home register, and its movement shows only in the capacity tracker's weekly returns.
Link: the step reads the care homes' register and returns against the population and the admissions through postcodes
and neighbourhoods; no key joins a care home to the evaluation's population, and no sentence in the framework, the letter
or the prompt invites the comparison of the two years' pools on care setting.
Reflex: the field's method for the deciding quantity, an age-standardised difference in differences across the
deprivation fifths, sits at rung 1 and files about 1,000, over the bar.
Back-test: the textbook route validates: Core20 and the rest moved in parallel through the three pre-commissioning years
(their age-standardised rates within a point of a common trend), so the difference in differences reads as a sound design.
Second use: every file the step reads is in the pack for its own reason: the register and the tracker serve the discharge
teams' vacancy reporting (an ask), the registration extract is the denominator, the admissions are the outcome.
Shock: nothing reads as an anomaly: the closures are eleven quiet deregistrations among several hundred homes, Core20's
pilot-year fall sits inside its own year-to-year range, and no sort of the neighbourhoods on a shipped statistic puts
the care homes' movement first.
Pins: the framework files the population, the outcome, the years, the comparison and the quantity, and the letter files
the bar; no filed sentence names care homes, a setting, a standardisation stratum or the closures, and deleting the
quantity's sentence leaves the step where it was.

## Readability screen

(Stage 2.)

## Semantic fork table

(Stage 2.)

## Ladder

(Stage 2.)

## Closure table

(Stage 2.)

## Literal reader

(Stage 2.)

## Oracles

(Stage 2.)

## Ask sheet

(Stage 2.)

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
