# task401 design note

Architecture 3, drawn 2026-11-03. The number was handed out against seed RC07 (a supplier's January imbalance bill
blamed on low wind by the desk and on plant trips by operations). The seed's world could not carry an honest unbanned
draw; architecture 1 (a frailty virtual ward's prevented admissions against care home closures, Epidemiology and Public
Health) died at stage 2 on published admission rates, and architecture 2 (a canola hybrid blamed for a shortfall that
July heat in late-seeded fields' flowering windows caused, Economics and Econometrics) died at stage 2 when the golden's
own window variants straddled the bar and flexible seeding-date controls landed the golden (`## Tried and rejected`,
the card's `lineage`). Architecture 3 re-roots in another client domain, world, dataset and shell under the same
objective and number (`CLAUDE.md`, a dead design is re-rooted at once; one architecture per world).

The world: an invented GB domestic energy supplier (about 640,000 accounts, electricity and gas, credit and Direct
Debit customers, traditional and smart meters) that tracks every new customer's satisfaction six months after the
switch. Six-month satisfaction fell between the first halves of 2025 and 2026. In the same year the supplier relaunched
its quote and switch journey (May 2025), moved billing to a new platform (phase 1 live 1 September 2025: every customer
who joined from July 2025 is billed on it), raised its variable tariffs in October 2025 and moved its contact centre to
an outsourcer in November 2025. Phase 2 of the billing platform (the remaining legacy accounts) is due to cut over on
1 February 2027; the executive team wants the cause of the fall named before it signs the cutover off.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v3 (v1 and v2 in `lineage` with their
  fates), registered 2026-11-03T16:08:03Z; `guard.py check` on the registered card returns WARN, exit 0, and `validate`
  reads 312 cards with none invalid. Two BLOCKs on the draft were cleared before registration: `ban.pattern` (the first
  decisive generator drafted, G9, repeats task402's) was redrawn to G6, which is the honest label (the per-customer
  satisfaction curve does not move; the 2026 pool shifted on a state no column holds), and `test.same_driver_older`
  against task181 v6 is answered on the card (task181 traces cases to a shared resource that handled them; nothing here
  handled customers differently). The WARNs: `overuse.objective` (root cause in 5 of the last 12; the number sits in
  the root-cause range); `repeat.gate_g` and `overuse.gate_g` against task400 and task402, answered under Strategy.
  NOTEs: `test.same_puzzle_older` and `test.same_driver_older` differentiated on the card against task121 v4 and v5 and
  task181 v6. Nearest driver 0.10 (task121 v4), under the 0.12 floor, screened below.
- **Pairing:** Marketing and Consumer Research (client domain) / `customer-satisfaction-driver-analysis` / Root-Cause
  Analysis. The task type serves Root-Cause Analysis only; `marketing-consumer-research x root-cause` has never been
  built (`guard.py coverage`, 2026-11-03), and the probe card passed the task-type rule. The supplier is the setting;
  the deciding quantity is the task type's own object, each driver's contribution to a fall in the share of satisfied
  customers.
- **Objective and call:** what pulled six-month satisfaction down between H1 2025 and H1 2026, and how much of the fall
  it carries, so the executive team knows whether the billing platform is to blame before phase 2 cuts over. The
  rivals on the record: the billing platform, the October tariff rise, the contact centre transfer and the quote
  journey relaunch. The attribution is retrospective because H1 2026 is the closed window the tracker has measured; the
  decision it feeds faces forward (the February 2027 cutover and what the 2027 quote journey does). It stays Root-Cause
  Analysis: the work is naming what produced the fall with the rivals ruled out on the record; nothing is forecast.
- **Shape:** `03`, a bridge between two totals: the H1 2025 share satisfied to the H1 2026 share, bridged by reconciling
  items (the quote journey's typical-use default, the billing platform, the tariff rise, the contact centre, the rest),
  by fuel; the criteria arithmetic is written at stage 2 with the asks' repeated units. Architecture 2 also carried a
  bridge; the shell is redrawn (question form what, a new second-sentence opener and a new deliverable set at stage 2).
- **Strategy and Gate G:** `decomposition_attribution` (F8: a correctly reported movement booked to the right driver),
  Gate G `decomposition_attribution`. The fall is real and the ratings report it correctly; they book it to billing
  accuracy and so to the platform, and the decisive move books it to the quote default through each customer's
  disconfirmation. `repeat.gate_g` against task400 and task402 is answered: it is the honest label, and the decisive
  families differ (task400 a staggered rollout's natural comparison, task402 courses broken off when an actor's block
  lapses, here the expectation a sale set against the use the meter then recorded). `causal_design` and
  `population_selection` are barred in the window, and neither is honest here: nothing in the platform's assignment
  needs repairing (every 2026 respondent is on it) and no one is missing from the tracker.
- **Gap, pattern, generators:** gap objective (the ratings and the driver analysis report the fall correctly and are
  not what the decision is scored on, the change that produced it); pattern none; generators G6 (composition shift: the
  2026 pool shifted on each customer's disconfirmation while the satisfaction curve held) and G14 (conditioned yield:
  the pooled driver weights do not apply to a pool conditioned on what each customer was quoted).
- **Furniture** (read off `guard.py check` against the live window task399, task400, task402): forum `executive_team`
  (the executive signs the phase 2 cutover off), forcing event `cutover_or_migration` (phase 2 on 1 February 2027),
  organisation `utility_or_infrastructure`, role `research_desk` (the head of customer insight owns the tracker),
  context artifact `close_out_summary` (the platform's phase 1 close-out report, which reports the programme's own
  defects and never ranks causes of the fall), calibration none. None is held by the window.
- **People** (`guard.py names --geo uk --seed 401`): Gerard Norris (head of customer insight), Sylvia Phillips (chief
  customer officer), Elliot Davies (billing programme director). None appears in the prompt.
- **Data-native sentence:** a new customer's first bills and first Direct Debit review are set by what the meter records,
  while what the customer was told to expect was set at the switch from the use they gave or, from May 2025, from
  Ofgem's medium typical consumption when they gave none, so the six-month tracker measures the distance between the
  two, and the supplier keeps the quote and the meter in different systems under different keys.
- **Abstraction sentence:** a fall in a share of satisfied members is booked to the service the members' own ratings
  blame, when it comes from the gap between what each member was told to expect at joining and what their own later use
  then cost, visible only by setting the joining record against each member's measured use. It is not writable against
  any approved build.
- **Same-puzzle and library tests:** the stump sentence is not "use X on Y" with X a named correction. The field's
  method (key driver analysis with Shapley shares, the client card's first pattern) is rung 0 and files the wrong
  answer; the decisive step is the judgment that this fall was formed against an expectation the sale set, which the
  driver analysis cannot see because no rating measures it. The guard's same-puzzle and same-driver NOTEs (task121 v5,
  task181 v6) are differentiated on the card.
- **Semantic screen, one line per nearest build on the insight it spends** (`guard.py mechanisms --objective
  root-cause`, the brief's list and the guard's nearest drivers):
  - task121 v4 (a satisfaction fall read on the operating conditions each journey ran under, because ratings of every
    candidate move with the overall verdict): here the operating record is the default's own rung (bills, Direct Debit
    reviews); what decides is a sales record no conditions file carries. task121 (rest rebuilt from duty records): no
    rest or duty here.
  - task129 (exposure and surroundings under a reliability standard), task202 (a source's input reaching the layer a
    response draws on), task398 (a path-dependent rule re-run), task399 (an advocate's absence at each call), task400 (a
    staggered rollout's natural comparison), task402 (courses broken off when an actor's block lapses, the loss read as
    the wait's), task187 (a shortfall against a reference curve at matched conditions): none sets an expectation given
    at entry against the cost the member then met.
  - task401 v1 (a composition shift by closures behind a credited effect): no pool lost or gained members here; each
    respondent's own quote moved. task401 v2 (a dated shock meeting each unit's own sensitive phase): no shock, no phase.
  - task181 v6 (cases traced through time-ordered records to a shared resource that handled them): nothing handled the
    customers differently. task474 v7 (an instrument's change read through members who sat both): no instrument changed.
  - task13, task11, task36, task50, task72, task84, task111, task500 (labels against evidence, a threshold rebate, a
    filed exclusion, exposure inside a funded window, an owner across transfers, copies on a composite key, which cause
    operates forward, a matched-reference method): none is an expectation set at a sale.
- **The three go/no-go screens, measured on the clean truth before the card** (`scratchpad/t401/a3/proto_e2.py` to
  `proto_e5.py`, 20 seeds unless stated; levels set first and cited under Sources):
  1. **Realistic levels.** Ofgem's medium typical consumption (2,700 kWh electricity, 11,500 kWh gas) against household
     use spread as the national consumption statistics show (lognormal, about 0.5 and 0.45 in logs), 45 per cent of
     switchers giving no use, six-month satisfaction near 78 per cent, a 30 per cent overrun worth about 25 points. In
     the base-wide relationship tracker the quote default carries only 0.54 points (1.35 if 2025's joiners used a fifth
     more) against a fall whose draw-to-draw spread is 0.66 (`proto_e2.py`): it fails, so the build runs on the
     six-month new-customer tracker, where every respondent was quoted at the switch. There the quote default carries
     2.31 points (sd 0.23) of a 3.14-point fall (sd 0.62), the platform's own effect is 0.36, and the default's driver
     analysis books 1.61 (sd 0.22) to the platform: **lever 1.25 points (sd 0.22), 1.00 to 1.47 across overrun effects
     of 3.0 to 5.5 in the logit.**
  2. **The golden's method holds the call.** Every form of the disconfirmation that keeps the overrun's size names the
     quote default: kinked log cost ratio 2.59, pounds 2.41, kWh ratio 2.01, first-review Direct Debit rise 2.70,
     flags at 20 and 30 per cent 1.71 and 2.18, kinked linear probability 2.53; **the lowest, 1.71, against an
     unexplained residual (the fall less the quote default, the tariff rise and the contact centre) of at most 0.83.**
     A symmetric linear term (1.52) still clears it; a 10 per cent flag (0.93) falls inside it and is rejected by the
     data, since satisfaction keeps falling with the overrun's size inside the flagged group (stage 2 asserts the fit).
  3. **No easy completion.** The use each customer was quoted on enters no default rung; once it is in hand the call
     holds across the forms above; and the cracker's flexible rungs all land wrong: **Shapley key driver analysis puts
     62 per cent (sd 5) of the fall on billing accuracy (the platform); first-review Direct Debit rises over a quarter
     went from 8.8 to 14.2 per cent of respondents, every one on the new platform (the platform's reviews); a use-by-
     period model books the fall to high-use 2026 respondents (the October tariff rise).**
- **Sources:** Ofgem, typical domestic consumption values (medium 2,700 kWh electricity, 11,500 kWh gas, from April
  2023) for the quote default; the Department for Energy Security and Net Zero's sub-national and NEED domestic
  consumption statistics for the spread of household use; the CMA Energy Market Investigation final report (2016) on
  how many customers do not know their annual use; Ofgem's Direct Debit guidance (2023) for how payments are set and
  reviewed; Oliver (1980, Journal of Marketing Research) and Anderson and Sullivan (1993, Marketing Science) for
  expectation-disconfirmation and its asymmetry; Fornell and colleagues (1996, Journal of Marketing) for the ACSI's
  expectations construct; Ofgem's consumer perceptions research for the level of supplier satisfaction. Every row in
  the pack is constructed and declared synthetic in `metadata.json`; no real supplier, vendor or comparison site is
  named.

## Default path

1. Read the six-month tracker for H1 2025 and H1 2026 (the vendor's export changed layout in January 2026) and take
   the share satisfied the measurement framework files.
2. Run the field's key driver analysis: overall satisfaction on the attribute ratings (billing accuracy, bill clarity,
   value for money, ease of contact, resolution, the app), Shapley shares; carry each attribute's change through its
   share: billing accuracy carries about three fifths of the fall and value for money most of the rest.
3. Link the respondents to their accounts, bills and Direct Debit reviews (account numbers re-mapped at migration):
   every H1 2026 respondent was billed on the new platform, first-review Direct Debit rises over a quarter went from
   about 9 to 14 per cent of respondents, and the respondents with large rises are the dissatisfied ones.
4. Check the other rivals: the October tariff rise (variable-tariff respondents), the contact centre transfer
   (respondents who called), consumption bands: each moves a few tenths.
5. Book most of the fall to the billing platform (its bills and its Direct Debit reviews) and hold phase 2 for
   remediation.

Ends on: the billing platform carries most of the fall, about 1.6 of the 3.1 points by the driver analysis, with every
large Direct Debit rise on it, so phase 2 is held.
Golden: the quote journey's typical-use default (from May 2025) carries about 2.3 of the 3.1 points and the platform
under half a point; customers quoted on their own use were as satisfied on the new platform as H1 2025's were on the
old, so phase 2 can cut over and the fix is the quote.

## Stump sentence

A competent solver runs key driver analysis on the six-month tracker, sees billing accuracy carry about three fifths of
the fall, ties the H1 2026 respondents' large Direct Debit rises to the new platform every one of them was billed on,
and books most of the 3.1-point fall (about 1.6 points by the driver analysis) to the billing platform, because they
never set the use each customer was quoted on at the switch against the use their meter then recorded, which puts about
2.3 points on the quote journey's typical-use default and leaves the platform under half a point.

## Three rules

Task type: `customer-satisfaction-driver-analysis` (Marketing and Consumer Research), which serves Root-Cause Analysis
in the taxonomy; attributing a satisfaction movement to its drivers is the task type's core.
Domain test: the deciding quantity is each driver's contribution to the fall in the share of satisfied new customers,
estimated by a satisfaction driver model that carries each customer's disconfirmation (the cost of the use the meter
recorded against the cost the customer was quoted at the switch), the expectation-disconfirmation paradigm and the
ACSI's expectations construct.
Swap: "six-month satisfaction fell because customers' bills ran above the use they were quoted on" read with school or
grid nouns ("attainment fell because pupils' bills ran above their quote") no longer parses; no school, ward or
substation has a sale that set an expectation, a meter that later measured the thing quoted, and a tracker of how the
customer felt about the difference.
Layer 1: the tracker vendor's export changed layout in January 2026 (the survey vendor); quotes keyed by quote reference
and meter point numbers while the tracker and billing key by account numbers re-numbered at migration (the sales
system and the platform); reads flagged actual, customer or estimated, with register rollovers, meter exchanges and
two-rate registers (the meters and the read agents); legacy timestamps in UK local time against the platform's UTC
across the clock changes (the two platforms); pence on the legacy export against pounds on the platform's, with
accounts on both during the parallel run (the migration). Each is produced by the system named; none is placed to be
caught.
Layer 2: field method (the satisfaction driver model done right): the driver set must carry what each customer was led
to expect, the disconfirmation that satisfaction is formed against, which no attribute rating measures.
Decisive step: setting each respondent's quoted use against the annual use their meter then recorded (cost at their
tariff), entering that disconfirmation in the driver model, and finding that it carries most of the fall while
customers quoted on their own use hold their H1 2025 level on the new platform.
Not semantics: every field, code, unit and date can be read correctly (the reads' flags, the registers, kWh, pence
against pounds, UTC against local time, the re-mapped accounts) and the driver analysis still books the fall to the
platform, because the error is in which driver the model carries, not in reading any column.
Not rule application: no filed rule or procedure sets a quote against metered use or says satisfaction is formed
against expectation; executing the measurement framework, the Direct Debit guidance and the tariff terms files the
default. The enumerated family (key driver analysis linear and Shapley, the bill and Direct Debit linkage, the rival
checks, a use-by-period model, the disconfirmation forms) spans the platform at about 1.0 to 1.8 points and the quote
default at 0.9 to 2.7; the standing family once the data rule out the forms that drop the overrun's size spans 1.7 to
2.7 on the quote default with the platform under a residual of at most 0.8; the ruling-out is the fit itself, quiet,
in a file the question gives no reason to open (the quotes).
Analyst test: a strong analyst who reads every rating, quote and meter record correctly runs key driver analysis with
Shapley shares, links the respondents to their bills and Direct Debit reviews, and books most of the fall (about 1.6 of
3.1 points) to the billing platform, holding phase 2 (the default path's `Ends on:`).
Estimand: the supplier's satisfaction measurement framework (a governing document in its own genre) files the WHAT:
the share of six-month respondents satisfied, the two half-year windows, and each change's part in the movement as the
H1 2026 share against the share had that change not been made, the others as they were; it names no driver model, no
quote, no consumption and no expectation.
No decoy: nothing is planted to be caught; no memo, briefing, draft or stakeholder figure argues for the platform, the
close-out report states the programme's own defects and no cause of the fall, and no file computes a driver's share.
No certified replay: no certified or published figure is reproduced to recover a method; the tracker's published
monthly shares agree with the respondents' records under every route.
Domain close call: Energy Systems and Utilities carries load, capacity, reliability, tariffs, assets and savings, and
none of its task types reads customer satisfaction; the deciding quantity here is a satisfaction driver attribution, so
the build sits in Marketing and Consumer Research, with the supplier as the setting and the energy shown where it is
honest (metered use, tariffs, Direct Debit reviews).
Lesson: satisfaction is formed against expectation, so before a fall is booked to the service the ratings name, a
driver analysis must carry what each customer was led to expect at the sale; no build on file teaches
expectation-disconfirmation from a sales record.

## Survivor anatomy

Actor: the deciding property, how far each customer's metered use ran above the use their quote assumed, has no column
in any file; the quote file holds the assumed use (the customer's own or a typical value), the reads file holds the
meter's registers, and the bills hold amounts.
Link: the comparison of the quote's assumed use with metered annual use is a cross-file comparison the driver analysis
never asks for, joined through quote references and meter point numbers to accounts re-numbered at migration.
Reflex: the field's method, key driver analysis with Shapley shares, is rung 0 and books about three fifths of the fall
to billing accuracy, so to the platform.
Back-test: the driver analysis explains H1 2025's satisfaction well with stable weights, and the platform's close-out
report shows estimated bills rising after go-live (true and small); the textbook route validates.
Second use: the quotes carry an ask on acquisitions; the reads carry an ask on estimated bills across the migration; the
Direct Debit history carries an ask on reviews; the tracker carries the measure itself.
Shock: the fall is modest, ordinary movement; the visible events of the year are the platform go-live, the October
tariff rise and the contact centre transfer, and no shipped statistic sorts the quote default's customers to an end.
Pins: the measurement framework files the measure, the windows and the WHAT of each change's part; no filed sentence
names quotes, typical consumption, expectations, disconfirmation or a comparison group.

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
