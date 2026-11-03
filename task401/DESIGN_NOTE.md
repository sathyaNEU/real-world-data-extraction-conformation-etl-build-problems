# task401 design note

Architecture 2, drawn 2026-11-03. The number was handed out against seed RC07 (a supplier's January imbalance bill
blamed on low wind by the desk and on plant trips by operations, the trips' cost filed as the reference for an
outage-cover decision). The seed's world could not carry an honest unbanned draw, and architecture 1 (a frailty virtual
ward's prevented admissions against care home closures, Epidemiology and Public Health) died at stage 2 when the
admission rates were set to published levels (`## Tried and rejected`). Architecture 2 keeps the seed's decision shape (a
loss with rival explanations, one figure filed as the reference for a buy-or-not decision) and re-roots in another
client domain, world and dataset under the same objective and number (`CLAUDE.md`, a dead design is re-rooted at once).

The world: Larkspur Hills Grain Ltd. (invented), a farmland operating company farming about 150,000 acres of owned and
leased land in west-central Saskatchewan from 31 farm yards in the Dark Brown and Black soil zones, canola on roughly
two fifths of its acres each year. In 2026 it moved about two fifths of its canola acres from the incumbent hybrid to a
new hybrid of the same maturity class. Its 2026 canola came in well below the 2020 to 2025 average, and the hybrid's
fields came in about a tenth below the incumbent's. The summer had a dry June and a heat wave from 10 to 18 July. The
executive team decides by the seed company's early-order deadline (15 December 2026) whether the hybrid stays on the
2027 order; the operator's variety policy keeps a hybrid when it gives up no more than five per cent of the incumbent's
yield on the operator's own fields.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v2 (v1 in `lineage` with its fate), drawn and
  registered 2026-11-03. `guard.py check` on the draft returned WARN: `overuse.objective` (root cause in 5 of the last
  12; the number sits in the root-cause range), `repeat.gate_g` and `overuse.gate_g` against task400 and task402
  (answered below). One older structural repeat is differentiated on the card (task111 v1). Nearest driver 0.05 (task118
  v3, task130 v4, task254 v2, task301 v1, task31 lineage), each screened below. A first draft drew `ban.artifact`
  (`register`, held by task402) and the context artifact was redrawn to `published_series`.
- **Pairing:** Economics & Econometrics (client domain) / `panel-data-estimation` / Root-Cause Analysis. The task type
  serves Experiment & Causal and Root-Cause; `economics-econometrics x root-cause` has never been built (`guard.py
  coverage`, 2026-11-03), and no slot note mentions canola, flowering, degree days, seeding, hybrids or crop yields
  (`guard.py slots`, mechanism and setting nouns run separately).
- **Objective and call:** how much of the 2026 canola shortfall the new hybrid itself caused, and so whether it stays on
  the 2027 seed order. The move to explain is the 2026 shortfall against the operator's 2020 to 2025 yields and the
  hybrid's deficit against the incumbent inside it; the rivals are the hybrid, the July heat, the dry June, and how the
  season's operations ran (seeding dates, which fields carried which hybrid). The call faces forward (the 2027 order);
  the attribution is retrospective because 2026 is the only season the hybrid ran at scale. The tag stays Root-Cause
  Analysis: the work is naming what produced the deficit, rivals ruled out on the record; nothing is forecast beyond
  carrying the hybrid's own effect into a season with normal seed delivery.
- **Shape:** `03`, bridge between two totals: the 2026 canola production against the 2020 to 2025 expectation, bridged
  by reconciling items (heat in the flowering window, the dry June, the hybrid fields' timing, the hybrid's own effect,
  the rest), by soil zone; written out in `## Ladder` at stage 2 with the asks' repeated units.
- **Strategy and Gate G:** `decomposition_attribution` (F8, whose movement it is: a shared external driver decides the
  split), Gate G `decomposition_attribution`. The decisive move splits the hybrid fields' deficit between the hybrid
  and the July heat, which harmed a field only while that field was in flower; the hybrid's fields flowered into it
  because their seed reached most farms late and they were seeded about ten days after the incumbent's. Gate G names the
  mechanism carrying the stump, a correct deficit booked to the wrong cause. `repeat.gate_g` against task400 and task402
  is answered: it is the honest label, and the decisive families differ (task400 a staggered rollout's natural
  comparison of warning response, task402 attrition of broken-off therapy courses, here a crop's own phenological clock
  against a dated shock).
- **Why this label is the honester one, not the passing one:** `causal_design` BLOCKs on `ban.strategy` against task400, and seeding-date confounding reads naturally as a design problem, so the choice is argued on its merits: nothing in the hybrid's placement needs repairing (within a yard it went on fields at random); the late seeding is a pathway the hybrid's own seed delivery opened, and the shape 03 bridge splits the hybrid fields' deficit between that timing pathway (heat inside flowering windows it moved) and the variety's own effect, the split decided by how the heat met each field's flowering phase. A deficit booked to the right driver through a shared shock is F8's form.
- **Gap, pattern, generators:** gap objective (the yield by hybrid is reported correctly and is not what the order is
  scored on, the hybrid's own effect), then time (2026's seed arrived late; the 2027 order does not repeat it); pattern
  none; generators G7 (operating window: the heat counts only inside each field's flowering window) and G13 (horizon
  mismatch: the 2026 deficit carries a timing the 2027 season does not).
- **Furniture:** forum `executive_team` (the operator's executive team signs the 2027 seed order), forcing event
  `purchase_order_or_contract` (the seed company's early-order deadline, 15 December 2026), organisation
  `agriculture_or_food_producer` (one build on file), role `research_desk` (the agronomy director, who owns the variety
  policy's evaluation), context artifact `published_series` (the provincial crop insurer's published average canola
  yields by risk zone and year, which answer what the region yielded), calibration none. None is held by the last three
  live cards (task399, task400, task402).
- **People** (`guard.py names --geo canada --seed 401`): Lacey Caldwell (agronomy director, owner of the variety
  policy), Brandi Carlson (chief operating officer, signs the seed order), Elaine Gregory (seed and inputs buyer). None
  appears in the prompt.
- **Data-native sentence:** canola loses most of what heat costs it only while it is in flower, and when a field
  flowers is set by the heat units it has gathered since its own seeding date at its own station, so in a season with a
  nine-day July heat wave two fields of the same hybrid seeded ten days apart lose very different shares; the operator
  keeps no seeding date on the field record, only the seeder's own timestamped passes.
- **Abstraction sentence:** a candidate is blamed for a loss a dated shock caused, because a one-off delay started its
  units' own clocks late enough that their sensitive phase sat on the shock, and every season-wide, unit-level or linear
  start-date control leaves the loss on the candidate.
- **Same-puzzle and library tests:** the stump sentence is not "use X on Y" with X a named correction. The field's named
  method (the season-long degree-day panel of Schlenker and Roberts, with farm and year effects) is rung 1 and files the
  wrong answer; the decisive step is the judgment that this season's heat struck through each field's own flowering
  window, which the season-long exposure averages away.
- **Semantic screen, one line per nearest build on the insight it spends** (`guard.py mechanisms --objective
  root-cause`, the brief's list, and the guard's nearest drivers):
  - task121: rest rebuilt from duty records as each event's exposure to an unstated condition. Here the exposure is
    weather every field at a station shares; what is rebuilt is when each field was vulnerable to it. Different insight.
  - task129: a provider blamed for a rise that scales with each unit's surroundings. Here fields at one station share
    their surroundings and still lose differently; the loss turns on each field's own timing against a dated shock, not
    a static property. Different insight.
  - task111 (now and v1): which cause operates in the forward window; failures traced back to an earlier period's work
    through a crosswalk. Here nothing carries over from an earlier period or system; the forward step only carries the
    hybrid's own effect into a season whose seed arrives on time. Differentiated on the card.
  - task202: how much of each source's input reaches the layer a response draws on. No transport or receiving layer
    here. task398: a path-dependent counterfactual re-running a rule on the changed path. No rule is re-run here.
  - task399: an advocate's absence at each call, and a capacity stock rebuilt from its events. task400: a staggered
    rollout separating a system change from its users. task402: outcomes lost from courses broken off when the actor
    leaves. None is a growth-stage exposure.
  - task13 (labels against physical evidence), task11 (a threshold rebate), task36 (a filed exclusion), task50 (exposure
    inside a funded window), task72 (an owner by agreement across transfers), task84 (identical copies grouped on a
    composite key), task500 (a matched-reference method; household spillover): none is a timing of vulnerability.
  - Nearest drivers at 0.05: task118 v3 (a harm easing with time since exposure began, priced from the first record),
    task130 v4 (a cover paying only for events reported inside its own window), task254 v2 (a cut of a time-to-event
    distribution seen through events already observed), task301 v1 (a deposit falling off with distance from a source),
    task31 (plan volume phased over a year). None places a unit's sensitive phase by its own start date against a shock.
- **Sources:** Schlenker and Roberts (2009, PNAS) for the season-long degree-day yield panel the field reaches for first;
  the Canola Council of Canada's crop development guidance on heat during flowering and growth stages by heat units;
  Environment and Climate Change Canada's daily climate data (Open Government Licence, Canada) as the template for the
  station files; Saskatchewan Crop Insurance's published yields by risk zone as the template for the context series.
  Every row in the pack is constructed and declared synthetic in `metadata.json`.

## Default path

1. Read the field register and the harvest records for 2020 to 2026; calibrate each farm's combine yield-monitor totals
   to its elevator scale tickets; key fields across seasons by legal land description; keep the canola field-seasons.
2. Link each field to its nearest weather station and build the season's growing degree days and extreme degree days
   above 29.5 C over May to August, and June rainfall, from the daily station records.
3. Fit the field's standard yield-weather panel: log yield on the hybrid indicator, the season's degree days and extreme
   degree days, June rainfall, farm effects and year effects (Schlenker and Roberts); check it on 2020 to 2025, where it
   tracks each farm's yields.
4. Read the hybrid's coefficient as what it costs: about nine per cent of yield in 2026. The within-farm comparison of
   2026 hybrid and incumbent fields agrees (about nine), and a seeding-date term built from the seeder's logs, entered
   linearly, still leaves about seven.
5. Compare with the variety policy's five per cent and drop the hybrid from the 2027 order.

Ends on: a hybrid penalty of about 9 per cent, past the 5 per cent bar, so the hybrid comes off the 2027 order.
Golden: about 0 per cent once the heat enters inside each field's own flowering window (placed by heat units from its
seeding date at its station), so the hybrid stays on the order; the deficit was the July heat meeting fields its late
seed delivery had pushed about ten days later.

## Stump sentence

A competent solver fits the season-long degree-day yield panel with farm and year effects, files a hybrid penalty of
about 9 per cent, past the 5 per cent bar, and drops the hybrid from the 2027 order, because it compares hybrid fields
with incumbent fields that had flowered before the July heat, when the hybrid's fields, seeded about ten days later after
their seed arrived late, flowered into it.

## Three rules

Task type: `panel-data-estimation` (Economics & Econometrics), which serves Root-Cause Analysis in the taxonomy; the
field-by-season yield panel with weather exposure is its applied core in agricultural economics.
Domain test: the deciding quantity is the hybrid's own yield effect in a field-season panel once weather enters as the
crop meets it, inside each field's flowering window placed by thermal time from its seeding date; the field's estimator
is the yield-weather panel with farm and year effects and a growth-stage exposure.
Swap: "the new protocol's wards had more readmissions because the July heat struck each ward's patients only in their
flowering window" no longer parses; no hospital, school or shop has a unit whose own planting date and local heat
accumulation decide when a dated heat wave can harm it.
Layer 1: yield monitors that read above the elevator scale tickets (combines), fields renamed, split and merged between
seasons and typed by operators into the seeder (farm operations), seeder logs in UTC against the farm's year-round
Central Standard Time (the seeder's controller), climate records with flagged missing days and a station that changed
climate identifier (the weather service), bushels per acre against tonnes per hectare (the farm against the crop
insurer), seeded acres that differ from GPS areas (the insurance reports); each is produced by the system named, and none
is placed to be caught.
Layer 2: estimand identification (the right counterfactual): the hybrid's effect is read against the incumbent at the
same exposure to the season's shock, and the exposure that matters is the heat inside each field's own flowering
window, which the season-long and farm-level forms average away.
Decisive step: entering the July heat through each field's own flowering window, timed by heat units from that field's
seeding date (read from the seeder's passes) at its nearest station, and reading the hybrid's coefficient at equal
heat in flower; or, equivalently, comparing hybrid and incumbent fields seeded on the same days on the same farm.
Not semantics: every field, code, unit and date can be read correctly (bushels against tonnes, UTC against CST, the
calibrated yields, the station link) and the season-long panel still files about 9 per cent, because the error is in
which weather the crop met, not in reading any column.
Not rule application: no filed rule or procedure places a field's flowering window or says that heat counts only in
flower; executing the variety policy, the crop insurer's definitions and the yield calibration files the default. The
enumerated family (raw 2026 means, the season-long panel, farm-by-year effects, a linear seeding-date term, the
flowering-window exposure at thresholds of 28 to 31 C and windows of 14 to 22 days, matching on seeding date within
farm) spans about minus 12 to plus 1 per cent on the prototype; the standing family once the data rule out the
season-long and linear forms (their residuals carry the timing) spans about minus 3.5 to plus 0.5, every member inside
the bar; the ruling-out is the fit itself, quiet, in a file the question gives no reason to open (the seeder's logs).
Analyst test: a strong analyst who calibrates the yields, keys every field and links every station fits the season-long
degree-day panel with farm and year effects and files a hybrid penalty of about 9 per cent, past the 5 per cent bar, and
drops the hybrid (the default path's `Ends on:`).
Estimand: the variety policy (a governing document in the operator's own genre) files the WHAT: the share of yield the
hybrid would give up against the incumbent on the operator's fields in the coming season, with its seed delivered under
the order's standing terms; it names no method, no weather window and no seeding date.
No decoy: nothing is planted to be caught; no memo, briefing, draft or stakeholder figure argues for dropping the
hybrid, and no file computes the hybrid's yield penalty.
No certified replay: no certified or published figure is reproduced to recover a method; the provincial yields by risk
zone answer what the region yielded and agree with the operator's own records under every route.
Domain close call: the domains README reads Economics as macro, labour, trade and fiscal reads, and a farm operator's seed order is none of those; it stays here because the deciding quantity is the econometrics literature's own estimate (the yield-weather panel with farm and year effects), the failure is an identification failure in a two-way fixed-effects panel (exposure timing confounded with treatment), and no client domain carries agronomy; the economics shows where it is honest, in the order's seed cost per acre net of the hybrid's premium (an ask), while the filed 5 per cent yield bar stays the rule.
Lesson: weather harms a crop through its growth stage, so a variety compared across fields seeded on different dates
must be read at equal exposure inside each field's own sensitive window; no build on file teaches a growth-stage
exposure or a clock started by each unit's own date against a dated shock.

## Survivor anatomy

Actor: the deciding property, how much of the July heat fell inside each field's flowering window, has no column; no
file stores a flowering date or a seeding date on the field (the seeder's logs hold timestamped passes with operator-typed
field names, the stations hold daily temperatures).
Link: each field's seeding date is rebuilt from the seeder's passes (a name that only partly matches the register,
located by legal land description) and its flowering by heat units at the nearest station, a link no key offers and no
sentence invites; the delivery register shows when each farm's seed arrived, never when it was due.
Reflex: the field's named method, the season-long degree-day panel with farm and year effects (Schlenker and Roberts),
is rung 1 and files about 9 per cent, past the bar.
Back-test: the season-long panel tracks every farm's 2020 to 2025 canola yields, and the provincial yields by risk zone
agree with the operator's own; the textbook route validates.
Second use: the seeder's logs carry the seeding-rate and seed-use asks and reconcile seed delivered against seed sown;
the station files feed the season-long panel the default already uses; the delivery register is the buyer's record of
inputs received.
Shock: the July heat wave is the season's ordinary explained weather, read by every route; nothing in the hybrid's
fields is an outlier on any shipped statistic, and the hybrid's deficit is not the pack's largest movement (the dry
June and the heat move every field).
Pins: the variety policy files the WHAT (the share of the incumbent's yield the hybrid gives up on the operator's fields
in a season under the order's standing delivery terms); no filed sentence names seeding dates, flowering, a weather
window, a threshold or a comparison group.

## Readability screen

(Stage 2.)

## Semantic fork table

(Stage 2.)

## Ladder

Stage 2 in progress (`generator/world.py` clean truth, `generator/ladder.py` routes; the hybrid's own effect is nil by
construction). Measured 2026-11-03 on seed 4012026 with the heat wave starting 20 July (the coordinator's 10 to 18 July
was moved once the climatology was set to west-central Saskatchewan normals: with May to July at normal temperatures
canola seeded in early May flowers about 1 July and the late-seeded hybrid about two weeks later, so a mid-July wave
would strike both):

| Route | Hybrid effect | Lands |
|---|---|---|
| Raw 2026 means | -24.6 | drop |
| Season-long degree-day panel, farm and year effects (rung 1, the field's method) | -18.1 | drop |
| Farm-by-year effects | -15.0 | drop |
| Season panel plus a linear seeding-date term (dates rebuilt from the pass logs) | -10.1 | drop |
| Farm-by-year plus a linear seeding-date term | -8.3 | drop |
| Season panel plus seeding-week bins by season | +3.6 | keep |
| Cubic in seeding day by season | +4.4 | keep |
| Fields seeded within the same three days on the same farm (20 hybrid fields matched) | +9.3 | keep (noisy) |
| Heat in each field's flowering window, 520 heat units base 5 C, 18 days, 29.5 C | +1.0 | keep |
| Window variants: 28 C, 31 C, 14 days, 22 days, 490 and 550 units | +2.1, -2.5, -12.0, +3.4, -8.2, +4.9 | mixed |

Findings to settle before precut. First, said plainly: once the seeding dates are rebuilt from the seeder's pass logs,
every flexible seeding-date route lands about nil and keeps the hybrid; only a linear term still files a penalty past
the bar. The stump therefore rests on whether the solver rebuilds seeding dates at all, and the Gate F argument is that
no file states them, no ledger, memo or invoice dates the hybrid's seed arrival (the inputs ledger carries invoice dates
from the early-order programme), and the field's method, run on every column the field register and harvest records
carry, files about -15 to -18. Second, the window variants spread too widely to grade the hybrid's effect finer than the
call: canola catches up when seeded late (a 17-day seeding gap became a 6-day flowering gap in a hot June), so the
generator must set 2026's monthly anomalies (normal May to July apart from the wave) to hold the flowering clusters about
12 days apart, and the graded figure becomes the call with a band; each bridge item is graded only at a precision every
defensible window reproduces, or replaced by a model-free figure (seeding dates, yields by zone and hybrid).

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
