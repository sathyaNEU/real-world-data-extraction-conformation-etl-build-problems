# task165: Quellbrook's seasonal rock salt for 2026-27, after the bus network redesign moved 424 lane-km of collectors to Priority 1 (architecture 1)

Private, never ships. A new build (wave 6), numbered from seed FC36. The seed was read at its header and Situation only
(`status.py task165`). Its world (a northern city's public works department buying rock salt under a contract that rolls
over at last winter's delivered tonnage), its decision (the seasonal tonnage committed above the rollover by 1 October)
and its quantity (the additional rock salt for November to March, in tonnes to the nearest hundred, after the redesign
moved frequent service onto 424 lane-km of collectors that the snow and ice policy now treats as Priority 1) are kept.
The seed's own mechanism is dropped: no materials-planning tool ranks anything, no usage model or back-test ships, and
no route-register field decides the call. The pitfall is re-found from how a Priority 2 truck salts a collector: it
salts the intersections, hills and curves and drives the stretches between them with the spinner idle, so what moving a
street to Priority 1 adds depends on how much of it Priority 2 already salted.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task165.json`, architecture v1; `guard.py check` PASS at filing (no BLOCK, no WARN; the WARNs earlier windows raised are answered below) with two NOTEs (`test.same_puzzle_older`, `test.same_driver_older`, differentiated on the card against task134, task146, task465 and task54); nearest driver 0.11 (task118, differentiated on the card) |
| Domain / task type | `urban-regional-science`, task type `municipal-service-demand-resource-allocation` (serves Forecasting): the deciding quantity is the rock salt a city service level will need on a set of streets in a winter not yet begun, forecast from the spreader records of the streets that went through the same change of service before |
| Objective | Forecasting & Predictive Modeling: the salt the 424 lane-km will need from 1 November 2026 to 31 March 2027 at the planning severity, over what they needed at Priority 2; every file was pulled on Friday 25 September 2026 and the commitment is due 1 October |
| Shape | `single-figure`: the call (tonnes to the nearest 100) carried by two decoupled asks (each yard's dome stock and room on 1 November 2026, 8 figures; each yard's Priority 1 arterial rock salt in each of the three winters since October 2023, 12 figures) and the council report's chart of the second; criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (tonnes of rock salt) |
| Mechanism | gap population (decisive: the gain was measured on collectors moved because they were hazardous, and the new streets are not), with time (the coming winter at the planning severity, not last winter's or the five winters' mean); pattern none; generators G14 (the earlier moves' gain conditioned on each street's own Priority 2 salt), G6 (the new pool's coverage sits far below the earlier moves'), G13 (the planning severity); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `estimation_fit` (a treatment gain carried from earlier treated units to new ones conditioned on the covariate that drives it, measured in each unit's own history); `own:service-upgrade-gain-conditioned-on-prior-partial-coverage` |
| Layer 1 | the AVL system replaced on 1 October 2023 (legacy segment-by-shift summaries in kilograms and local time, then one row per pass in tonnes and UTC); the 2023 GIS re-segmentation splitting long arterial and Priority 2 segments through a crosswalk; the storm log's layout change in 2023; free-text revision reasons; and on the asks' rows only, the supplier's re-issued dispatch schedule, the survey's capture window in UTC, weighings at another yard's scale house, inter-yard transfers, older controllers writing a run's total on each segment, contractor circuits outside the telematics and the July 2026 yard realignment (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `council_or_assembly` (spending above the contract quantity needs council's approval under the City's procurement by-law, so the winter operations manager's commitment goes to council as a one-page report before the supplier's 1 October deadline), forcing event `purchase_order_or_contract` (the supply contract's 1 October deadline for seasonal tonnage), organisation family `local_government`, role family `operations_director` (the roads division's winter operations manager), context artifact `register` (the winter route register), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the fleet telematics platform's segment-pass export (one row per spreader pass over one route segment, with the rock salt put down), 1 October 2023 to 23 September 2026, 318,889 rows, beside the legacy AVL's segment-by-shift summaries for November 2021 to March 2023; constructed in the layout of a winter-maintenance telematics export |
| Deliverables | `salt_commitment_2026-27.xlsx` (the commitment, its working and the ask tables) and `seasonal_salt_commitment_memo.docx` (a one-page report to council recommending the commitment, with the chart of the arterial figures) |
| People | drawn with `guard.py names --geo "Canada" --seed 165`: Doris Wilkerson (manager, winter operations, owner of the winter maintenance plan), Mary Huynh (fleet telematics analyst, the exports and the data dictionary), Kristin Gonzalez (service planning, Quellbrook Regional Transit, the frequent network street list), Andre Nixon (director of roads, who approved the procurement procedure and the plan); the requester is in no file and not in the prompt |
| World | Quellbrook (checked: no Canadian or United States place of the name), a fictional lakeshore city in southern Ontario of about 410,000, whose public works roads division runs winter maintenance from four works yards (Kelvin Road, Mapleford, Ridge and Lakeshore); Quellbrook Regional Transit runs the buses; Northgrit Salt Supply (supplier), Tessaline Geomatics (dome survey) and Kettlewood Road Services (arterial contractor) are fictional, as are the people, systems and data; each invented name was searched and none sits within two letters of a well-known organisation or place (H21) |

**Guard.** The draw waited out bans on its honest keys rather than relabel them: `local_government` (twice),
`purchase_order_or_contract` and `composition_mix`, then `operations_director`, `line_manager_or_team` and the context
artifact `register`, each while a build in the last three registrations carried it; each lapsed as other builds
registered. When `line_manager_or_team` was banned a second time (task247) the forum was redrawn in the build itself,
not on the card alone: the procurement procedure sends spending above the contract quantity to council, and the
deliverable is a report to council (`## Tried and rejected`). With the pattern written as E the
structural tests collided with five older builds (task31, task44, task56, task57, task76); E's discriminator is an
absolute split, which this build does not have (the gain falls continuously with coverage), so the pattern is none and
the decisive generator G14. The (population, G14, quantity) and (population, G14, forecasting) triples then repeat
task134 v3, task146, task465 v2 and task54, each differentiated on the card. The WARNs the window raises are answered here: `repeat.gate_g`, `overuse.gate_g`, `overuse.objective` and
`repeat.decision` (forecasting builds committed as one quantity) are the honest keys for a seasonal tonnage forecast
for a winter not yet begun; `repeat.question_form` (how-much) is the form a tonnage takes; `repeat.deliverables`
(xlsx and docx) is the pair a roads division sends council, a workbook of the working and a one-page report. None
is a ban.

**Same-puzzle and same-driver tests.** Gap population, G14, `quantity_figure`: task134 v3 (a raised allowance's yield
from each lot's rebuild chance), task146 (a calendar turn releasing refused units), task465 v2 (a joint count from a
small source's within-cell association), task54 (loss per event under a withheld rule); gap population, G14, Gate G
`forecasting`: task134 v3 and task146. None transfers a treatment gain from earlier treated units by the share of each
unit the old treatment already covered.

**Abstraction test.** Stripped of nouns: the extra input an upgraded service level puts into a unit is the part of the
unit the old level left untreated, so the average gain measured on units upgraded earlier, chosen because the old level
already treated much of them, understates the gain for units the old level barely reached, while their upgraded level
less the new units' present input overstates it; only the gain conditioned on how much of each unit the old level
already treated, read from each unit's own record under it, carries across. Against `guard.py nearest`: task118 (0.11:
a specialist team's gain netted of the volume each unit already treats itself). There the netting is the correction;
here netting the new streets' own Priority 2 salt from the upgraded level is the default path and lands wrong, because
the upgraded level itself rises with prior coverage. task258 v1 (0.08), task459 (0.07) and task182 v1 (0.06) map onto
nothing here.

**Kinship, answered (the builds the brief names, and every road or winter card).** No card on file is a road,
winter-maintenance or salt build (searched: salt, winter, snow, plough, spreader, de-icing, pavement).
- task155 (a relief crew placed where call-ins carrying on from a rostered shift fill most): a take-up rate conditioned
  on adjacency to the taker's own roster; here nothing chooses, a truck's spinner treats what the service level tells it
  to, and the conditioning variable is how much of a street the old service already treated.
- task159 (platform conductors where crowds behind full trains are backlogs): a queue behind batch service; nothing
  here queues or binds.
- task148 (a 911 late shift's Erlang A with censored patience): a queue with abandonment; nothing here is censored.
- task134 (net new homes on upzoned lots): the nearest urban build; a lot's rebuild chance once a permitted option pays,
  not a treatment gain carried across by prior coverage.
- task124 lineage (analogs' draws conditioned on heat): an analog pool whose measured value was held down by an
  intervention; here the analog pool is honest and only its composition differs.

**WHAT screen (stumping 1.2).** The decisive step estimates the filed quantity; it settles none of the estimand's five
parts, each filed: population (the 216 segments, 424.0 lane-km, the route audit moved to Priority 1 on 30 August 2026,
procedure 4.2 "the roads the change moves" and the revision log), outcome (the rock salt they will need, 4.2), window
(1 November 2026 to 31 March 2027 in a winter at the planning severity, 4.2 and the plan's 61.7 WSI points), unit
(tonnes, rounded to the nearest 100 t, 4.2) and comparison (over what the same roads needed before the change, 4.2).
No shipped sentence says how a street's salt changes with its service level, and nothing says the change depends on
how much of the street Priority 2 salted: that is inferred from the earlier moves' own records.

**Data-native sentence.** Quellbrook's Priority 2 trucks salt only a collector's intersections, hills and curves, so
each collector's Priority 2 winters in the spreader records measure how much of it was already treated; the 202
collectors the route audit moved to Priority 1 from 2022 to 2025 were mostly hill, school, hospital and inner-suburb
transit streets moved because they were hazardous or dense with intersections, while the redesign put frequent service
on long, flat outer-suburb collectors whose Priority 2 trucks salted little beyond their intersections, so the gain the
earlier moves show belongs to their coverage, not to these streets.

**Sources read, one line each.**
- Seed FC36 header and Situation (`status.py task165`): the world, the rollover at 39,100 t, the 424 lane-km and the 1
  October deadline; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: the forecasting drivers on file price censored clocks, queues, capacity
  residuals, conditioned take-ups and composition shifts; none carries a treatment gain across by prior partial coverage.
- `two-layer-task-design.md`: "comparing against the right group" and "Simpson's paradox across strata"; here the group
  is right and its mix is not, so the gain is carried across conditioned, not pooled.
- `layer2-rigor-patterns.md`, urban and regional science, land-use pattern 3 (upzoning goes where growth already was):
  learned, not copied; here earlier service changes went where hazards already were, and the before-and-after on them is
  honest for them and wrong for the new streets.
- `strategies.md` F5 (composition): the property (prior coverage) is rebuilt from each street's own spreader history,
  never read off a column, and one band (the flat new streets) moves against the earlier moves.
- `guide-to-prompt/references/examples.md` 1 (task133, the divisor no sentence names): the decisive step is a quantity a
  careful analyst computes by default the wrong way, here the average gain or the average Priority 1 level.

## Default path

Every figure below is built by `generator/calc.py` from the shipped pack and asserted in `generator/checks.py`.

1. Read the procurement procedure (`road_salt_procurement_procedure_RO-PR-07.pdf`, 4.2): the seasonal tonnage is the
   additional rock salt the roads a service change moves will need from 1 November to 31 March, over what they needed
   before it, in a winter at the planning severity, rounded to the nearest 100 t; the winter maintenance plan gives the
   planning severity, 61.7 WSI points.
2. Take the 216 segments the route audit moved to Priority 1 on 30 August 2026 (`route_audit_revision_log.csv`), 424.0
   lane-km in the winter route register.
3. Join both AVL exports to the register (the crosswalk for the legacy ids, kilograms to tonnes, passes in season by
   local date) and take, for every collector segment in each winter it was Priority 1 (the inner-city frequent streets
   every winter, each earlier move from its first Priority 1 winter), the rock salt per lane-km per WSI point.
4. Take the 216 segments' own rock salt per lane-km per WSI point over the five winters, all at Priority 2 (1.6 t a
   lane-km in a 61.7-point winter).
5. The gain is (3) less (4), times 424.0 lane-km and 61.7 points: 2,603.6 t.

Ends on: 2,600 t.

Golden: 2,200 t.

## Stump sentence

A competent solver takes the Priority 1 collectors' rock salt per lane-km per severity point, less the 424 lane-km's
own Priority 2 salt, at the planning severity and files 2,600 t; the step that lands it there is carrying an average
Priority 1 level across to streets whose Priority 2 coverage differs, when the moved collectors' Priority 1 salt rises
with how much of each street Priority 2 already salted and the gain is mostly the length Priority 2 left untreated, so
only the gain read off each earlier move's own Priority 2 salt, at the new streets' Priority 2 salt, files 2,200 t.

## Three rules

- **Task type:** `urban-regional-science` / `municipal-service-demand-resource-allocation`, which serves Forecasting:
  the deciding object is the rock salt a service level will need on 424 lane-km of streets in a winter not yet begun,
  forecast from the city's own spreader records.
- **Domain test:** the quantity that decides the call is the extra rock salt per lane-km a collector needs when it moves
  from Priority 2 (salted at intersections, hills and curves) to Priority 1 (bare pavement over its length), sized the
  way winter maintenance engineers size a level-of-service change, per point of storm severity at the planning
  severity, carried across from the spreader records of the collectors moved before by how much of each street
  Priority 2 already salted; replacing it with a generic summary (the average gain, or the average Priority 1 rate less
  the present salt) moves the call by 400 t or 700 t.
- **Swap:** "how many more megawatt-hours to contract when 424 km of feeders move to a higher reliability tier" reads as
  a quantity, but no feeder tier treats only its hazard spots, so nothing makes the upgrade's gain fall with how much of
  each unit the old tier already served, and there is no storm severity to plan a winter at.
- **Layer 1:** each item is how the city's systems record a winter and none is placed to be caught, each asserted
  neutral on the call in `checks.py` (R2 rows): the legacy AVL's segment-by-shift summaries in kilograms and local time
  against the telematics platform's passes in tonnes and UTC; the 2023 GIS re-segmentation and its crosswalk (no
  main-population segment is split); the storm log's layout change; free-text revision reasons; the asks' own records
  (survey times in UTC, weighings at another yard's scale, transfers, dispatch re-issue, run totals on every segment,
  combined salt and brine mass, contractor circuits, the yard realignment) sit on no row the call reads.
- **Layer 2:** `estimation_fit`: the Priority 2 to Priority 1 gain carried from the 202 collectors moved in 2022 to 2025
  to the 216 new ones conditioned on each street's own Priority 2 salt per lane-km per point, against the pooled gain and
  the pooled Priority 1 level; both rivals and a power-law form are rejected out of sample (each move year held out,
  ten-fold cross-validation, and the new streets' band predicted from the rest).
- **Decisive step:** recognising that a moved collector's gain falls, and its Priority 1 level rises, with how much of
  it Priority 2 already salted, so the earlier moves' gain has to be read at the new streets' own Priority 2 salt rather
  than averaged or netted from an average level.
- **Not semantics:** no field, code or note says how much of a street Priority 2 salts or that the gain depends on it:
  the register carries lane-km, class, priority, yard and lanes, the revision log reasons in free text, the exports
  salt per pass; reading every column right still averages the gain or the level.
- **Not rule application:** the procedure files the estimand (population, window, severity, comparison, unit) and the
  plan files the severity normal; no filed rule says how a street's salt responds to its service level, so executing
  every stated rule leaves the gain to be estimated, and the natural estimate files the default path's figure.
- **Analyst test:** a strong analyst who maps both AVL exports onto the register, converts kilograms and clocks,
  normalises every winter by the filed WSI and takes the Priority 1 collectors' salt per lane-km less the new streets'
  own Priority 2 salt at the planning severity files 2,600 t; one who measures the before-and-after gain of the 202
  collectors moved since 2022 files 1,500 t; only the gain read off each earlier move's own Priority 2 salt files 2,200 t.
- **Estimand:** the procurement procedure (`road_salt_procurement_procedure_RO-PR-07.pdf`, 4.2) fixes the population
  (the roads the service change moves, the route audit's 30 August 2026 entries), the outcome (the rock salt they will
  need over what they needed before), the window (1 November to 31 March, a winter at the planning severity), the unit
  (tonnes, the nearest 100 t) and the comparison (over the same roads' needs before the change); the winter maintenance
  plan (`winter_maintenance_plan_2026-27.pdf`) files the planning severity, 61.7 WSI points.
- **No decoy:** nothing is planted to be caught: the earlier moves' records are what the trucks put down, the reasons in
  the revision log are the route audit's own, no memo, model, tool ranking or stakeholder figure argues for a tonnage,
  and no record is copied, backfilled or wrong.
- **No certified replay:** the method is not hidden and recovered by reproducing certified figures: nothing certifies a
  gain or a tonnage, and the earlier moves are raw spreader records a forecast is tested against.
- **Lesson:** what an upgraded service adds to a unit is what the old service left undone there, so a gain measured on
  units chosen because they were already well served has to be carried across conditioned on how much each was served,
  read from each unit's own history; no build on file teaches a treatment gain conditioned on prior partial coverage.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a row
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6
one subtraction, ratio or half of a figure).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0b the Priority 1 network's salt per lane-km per point, gross, at the planning severity (5,300) | the procedure's "over what they needed before" | the register's priority | yes, the first rate | the earlier moves' gains are under a third of it | no | yes | readable |
| R1 default: the Priority 1 collectors' rate less the new streets' own Priority 2 salt (2,600) | the procedure's comparison invites it | the register's class and priority | yes, the careful netting | the earlier moves' post-move levels rise with their pre-move salt, for an analyst who looks | no | yes, one subtraction | readable |
| R2 the earlier moves' pooled before-and-after gain (1,500) | no | the revision log's dates | yes, the event study | holding out each move year shows its error following the year's coverage | no | yes, a mean | readable |
| R2b the gain of the transit-driven earlier moves only (1,500) | no | the revision reasons | yes, stratify on a visible field | the transit moves' coverage still sits well over twice the new streets' | no | yes | readable |
| R2c the pooled gain stratified by yard, lanes or length band (1,500) | no | the register's columns | yes, reweight | as R2 | no | yes | readable |
| R2d the golden's gain at last winter's 52.6 points (1,900) | the plan's severity normal | the storm log | a half-step | the procedure's planning severity | no | yes, a ratio | readable |
| R3 (decisive) the earlier moves' gain read at each new street's own Priority 2 salt (2,200) | no shipped sentence says how a street's salt responds to its service level or how much of it Priority 2 salts | no column holds coverage, hazard length or a gain; the property exists only as each street's own Priority 2 salt | no: the reflexes pool, net, stratify on visible fields, reweight or add controls, and each lands wrong | the held-out move years, the folds and the new streets' band score it, and score every rival wrong | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a fit across 202 streets read at 216 others | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs; every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "above the rolled-over 39,100 t contract" | only the change's additional salt | the change plus the rollover's own shortfall in a planning-severity winter | another quantity | the procedure 4.2 ("For each change in winter service approved since the last winter closed"); the redesign is the only priority change since 31 March 2026 (asserted) |
| SF2 | the additional salt | over what the same roads needed at Priority 2 | their whole Priority 1 salt | 2,900 t | the procedure 4.2 ("over what they needed before it") |
| SF3 | "424 lane-km" | the register's lane_km of the 216 segments (424.0), rates per lane-km | rates and lengths in centreline km | 1,900 t | the plan 2 ("application rates, which are set in kilograms per lane-km") |
| SF4 | the winter | 1 November to 31 March, local dates | the platform's dates in UTC; the supply season from 1 October | same call (no collector pass within six hours of a season boundary, none in October or April, asserted) | the procedure 4.2; C1 |
| SF5 | the severity | 61.7 WSI points | last winter's 52.6; the five winters' mean | 1,900 t either way | the plan 4 ("Material planning uses the planning severity of 61.7 WSI points") |
| SF6 | salt against severity | in proportion | a line with an intercept | same call (the never-moved collectors' intercept within 3 per cent of nil, asserted) | C1, asserted |
| SF7 | "rock salt" | material RS | sand and salt rows | same call (collectors carry RS only, asserted) | the dictionary's material codes |
| SF8 | the moved roads | the revision log's 30 August 2026 entries | the transit agency's street list | same segments (asserted) | C1, asserted |
| SF9 | units in the legacy export | kilograms | tonnes | a thousandfold off, loud | the dictionary ("kilograms") |
| SF10 | rounding | the total to the nearest 100 t, once | the gain per lane-km rounded first | same call | the procedure 4.2 |
| SF11 | the earlier moves | every collector moved Priority 2 to Priority 1 on 1 November 2022, 2023, 2024 and 2025 | those with a transit reason only | 1,500 t (R2b, a rung, not a reading) | the revision log; the golden reads all 202 (asserted) |

## Ladder

Built figures from `generator/calc.py` on the shipped pack, every row asserted in `generator/checks.py` (LADDER, HEDGE,
OOS, FAMILY, SIGMA, ORTHO, TWIN). The graded quantity is the seasonal tonnage; each rung files a different figure.

| Rung | Construction | Tonnes | Dies to |
|---|---|---|---|
| R0 | last winter's Priority 1 network salt per lane-km, gross, at last winter's severity | 4,600 | the procedure's comparison and planning severity |
| R0b | the same per point at the planning severity | 5,300 | the procedure's comparison; arterials are not collectors |
| R1 default | the Priority 1 collectors' rate less the new streets' own Priority 2 salt | 2,600 (2,603.6) | the earlier moves' Priority 1 levels rise with their Priority 2 salt |
| R1b | the same with only the earlier moves' Priority 1 winters | 2,600 (2,560.6) | as R1 |
| R2 | the earlier moves' pooled gain per lane-km per point | 1,500 (1,536.2) | each move year's error follows its coverage when held out; the new streets' band predicted from the rest misses by half |
| R2b | the transit-driven earlier moves' gain | 1,500 (1,487.5) | their coverage is still well over twice the new streets' |
| R2c | the pooled gain stratified by yard, by lanes or by length band | 1,500 (1,532.1 to 1,546.4) | as R2 |
| R2d | the golden's gain at last winter's severity | 1,900 (1,879.3) | the plan's planning severity |
| R2e | the golden's gain at the five winters' mean severity | 1,900 (1,945.1) | as R2d |
| R2f | the earlier moves' ratio of Priority 1 to Priority 2 salt applied to the new streets' own salt | 600 | the ratio falls steeply with coverage |
| R2g | the pooled gain trended across the four move years | 1,600 (1,611.5) | as R2 |
| R2h | the pooled gain against the never-moved Priority 2 collectors, winter by winter | 1,500 (1,525.0) | as R2 |
| R2i | the 127 earlier moves whose Priority 2 salt lies inside the new streets' range, their gain averaged | 2,000 (1,981.9) | matched on the range, not the level: their Priority 2 salt averages 2.4 t a lane-km against the new streets' 1.6 |
| R3 decisive | the earlier moves' gain regressed on each street's own Priority 2 salt per lane-km per point, read at the new streets' | 2,200 (2,204.5) | golden |

**Position and margins.** The golden is bracketed: every netting of an average Priority 1 level sits above it (R1 by
399 t), every average gain below it (R2 by 668 t), and the severity errors below it (R2d by 325 t). Each correction from
R0b walks down; only the decisive move turns up from the average gain.

**Hedges (asserted, HEDGE).** The golden is not the midpoint of the rivals: the midpoint of the default and the pooled
gain files 2,069.9 t, of the moves' own level and the pooled gain 2,048.4 t, of the default and the transit moves' gain
2,045.6 t, each at least 50 t outside the golden's bin. The first parameterisation put the golden on the midpoint of R1
and R2 (`## Tried and rejected`).

**Convergence (C1, asserted on the cut pack).** The golden family, 18 members: the gain or the post-move level regressed
on the pre-move salt, weighted by lane-km or not; each earlier move's pre-move winters pooled or only the last; the
post-move winters pooled or only the first; each winter normalised by its own WSI, rates as the mean of each winter's,
or each winter against the never-moved Priority 2 collectors; quadratic; outliers dropped; the 10, 20 or 40 nearest
earlier moves; three, four, five or eight bands of Priority 2 salt; the prediction summed street by street or at the
pool's mean. Every member files 2,200 t, from 2,187.9 t to 2,212.1 t, each at least 37.9 t from the bin's edge.

**One sigma (asserted).** A bootstrap over the 202 earlier-moved streets puts one standard error of the golden at 13.0 t;
the golden plus or minus two standard errors stays in its bin (45.5 t of clearance), and every family member plus or
minus one standard error stays in it. The relation rests on 202 streets over four move years and five winters, one to
four winters on each side of each move.

**Out of sample (asserted, OOS).** Holding out each move year in turn, the conditioned gain predicts the held-out year's
total within 2.5 per cent, the pooled gain misses by up to 15.3 per cent; ten-fold cross-validation puts the line's
weighted squared error at 0.0102 against the power law's 0.0257 and the pooled gain's 0.3139; fitted on the moves above
the new streets' 90th percentile of Priority 2 salt and read on the 75 below it, the line misses their total gain by 1.5
per cent, the power law by 18.5 per cent and the pooled gain by 51.9 per cent. The power law alone files 2,270 t and is
rejected by all three.

**Sweep (asserted, stumping Part 6).** Every reflex lands off the golden by at least 200 t (the nearest, R2i, by 223 t): pooled; stratified by yard,
by reason, by lanes or length band; trended across move years; with a control group of never-moved Priority 2
collectors; the ratio; netting the level. Coverage is drawn independently of yard, lanes, length and route code (its
correlation with lanes and length under 0.05 and with any one yard under 0.16 among the earlier moves, asserted), and it
never ships.

**Twin pair (O1).** RS175687 and RS175751, consecutive sections of Bridgeport Crescent at Kelvin Road: four lanes, 0.67
km and 2.68 lane-km each, moved on 1 November 2024 under the same council motion; gains 5.77 t and 1.45 t a lane-km in a
61.7-point winter against Priority 2 salt of 1.20 t and 6.91 t. No visible field tells them apart.

**Worth on the graded quantity.** Seeing the conditioning is worth 399 t against the netting and 668 t against the
pooled gain; planning at 61.7 points rather than last winter's is worth 325 t.

**Strength (adversarial route list, P per strong solver).** The default netting (R1 or R1b, 2,600) 0.35; the event
study on the earlier moves (R2, R2b, R2c or R2h, 1,500) 0.30; a severity slip on any route (1,900 or lower) 0.05; a
gross level (5,300 or 2,900) 0.05; a hedge between the rivals (2,000 to 2,100) 0.04; a contingency on a rival (R2 plus
20 per cent, 1,800) 0.03; a match on the new streets' range of Priority 2 salt (R2i, 2,000) 0.03; the conditioned gain,
its nearest-neighbour or banded form (2,200) 0.12; the power law (2,300) 0.02; anything else 0.01. P(one strong solver lands) about 0.12; P(both land) about 0.03 with the correlation allowed. The
seed is fixed by rule (the task number, then the as-of month and day: 1650925) before any data is generated and is
never searched.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 216 segments moved on 30 August 2026, 424.0 lane-km | filed (the procedure's "roads the change moves"; the revision log); SF8 |
| 2 | Unit of account | tonnes of rock salt | filed (the procedure); SF7, SF9 |
| 3 | Attribution window | 1 November 2026 to 31 March 2027 | filed; records clear of the boundaries (SF4, asserted) |
| 4 | As-of dating | the exports to 23 September 2026; the register of 14 September 2026 | the data dictionary and manifest; no record after the pull (asserted) |
| 5 | Version basis | each segment's priority in each winter from the revision log | the revision log; the register carries the current priority |
| 6 | Denominator | lane-km and WSI points | the register, the plan's per lane-km rates and the storm log; SF3, SF6 |
| 7 | Weighting | lane-km weighted or not | C1 across the golden family (asserted) |
| 8 | Window length | all five winters against fewer | C1 across pre- and post-move windows (asserted) |
| 9 | Boundary inclusivity | the season's first and last days | nothing within six hours of either (asserted) |
| 10 | Rounding path | the total once, to the nearest 100 t | filed (the procedure); SF10 |
| 11 | Tie-break | none | n/a, one figure |
| 12 | Maturity and censoring | the new streets' Priority 1 winter not yet observed | the decisive forecast itself; nothing is censored in the records |
| 13 | Order of operations | normalise per point, then fit, then scale to 61.7 | C1 (order-free under proportional scaling, asserted in SF6) |
| 14 | Row order | sums only | C1 |
| 15 | Duplicate resolution | none on the call's rows | the realism sweep (no repeated pass key; no copied block) |
| 16 | Identity normalisation | legacy ids to current through the crosswalk | the crosswalk; no main-population segment is split (asserted) |
| 17 | Netting against gross | over what the roads needed before | filed (SF2) |
| 18 | Dimensional units | kilograms in the legacy export, tonnes in the new | the dictionary; SF9 |
| 19 | Code and status semantics | material RS; priority 1, 2, 3 | the dictionary and the plan (Layer 1, neutral) |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the procedure's 4.2 for every service change since the 2025-26 winter closed | filed; the redesign is the only change (SF1, asserted) |
| 22 | Forward window contents | a winter at the planning severity | filed (the plan); no forward weather ships |

## Literal reader

Executing the prompt, the procedure and the plan word for word gives the rock salt the 216 segments moved on 30 August
2026 will need from 1 November 2026 to 31 March 2027 over what they needed at Priority 2, in a winter of 61.7 WSI points,
rounded once to the nearest 100 t; no shipped sentence says how a street's salt responds to its service level, so a
literal reader must estimate it from the records, the easy estimates on the same literal estimand (the netted average
level, 2,600 t; the pooled gain, 1,500 t) file other figures, and the fork table leaves no reading under which a rung is
the golden.

## Oracles

- The earlier moves (202 collectors, before and after): the evidence every route reads; on the wrong path they confirm
  the pooled gain in sample, and only a held-out year, a fold or the new streets' band shows the bias, which the solver
  has to run. They do not tie only under the golden.
- The never-moved Priority 2 collectors: a control for winter effects; blind to the decisive move because none of them
  changed service (their gain is nil under every basis).
- The storm log's WSI: an input every route reads alike.
- The asks' referees (the scale houses' own times, the yard loading log, the contractor's returns) sit on no row the
  call reads.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the AVL rows (both exports) of every collector segment, the winter route
register's collector rows, the revision log's priority entries for collectors, the storm log's WSI, the procedure and the
plan. Device and hazard rows in it: 0 (asserted, SEPARATION: no older-controller unit serves a collector circuit, the
collectors spread dry salt, no collector segment the call reads is split by the crosswalk, no collector pass falls within
six hours of a season boundary, the contractor and the realignment touch arterials only, and the golden is unchanged with
every ask file deleted).

**Ask A. For each works yard, the rock salt in its dome on 1 November 2026 once the October deliveries booked with the
supplier have landed, and the tonnes more the dome can then take** (8 figures, tonnes to one decimal).
- H18 home: where the seasonal tonnage can go, read beside the commitment for its delivery schedule; a measure every
  yard carries that the call does not turn on.
- Basis (filed in the plan's materials section, the owner's voice): "Each dome's stock is taken from its September
  survey and brought forward by the loads weighed in to it and out of it at the scale houses." The dome register gives
  capacities; the supplier's latest dispatch issue gives the October bookings.
- Primary A1 (D8, a clock against a filed cutoff; silent): each dome was flown on a different September morning and
  the survey report gives each capture window in UTC in its flight log; on every survey day the yard weighed supplier
  loads in both before and after the flight, so the stock moves forward only by what crossed the scale after the
  capture's end, local time. Rolled forward from the day after the survey, from the survey day whole, or from the UTC
  times read as local, every figure moves. Fair: the scale-house log times every weighing to the minute.
- Primary A2 (D7, the true key elsewhere; silent): while Lakeshore's scale was replaced (24 August to 14 September) its
  supplier loads were weighed at Ridge, and while Mapleford's was recertified (14 to 18 September) at Kelvin Road; the
  weighing yard's sheet carries them with the receiving dome only in the operator's remarks, in four spellings. Counted
  by sheet, all four figures move. Fair: every such row names its dome.
- Hazards: HA1 the supplier's dispatch schedule re-issued on 21 September (two loads cancelled, three moved into
  November, one added at Ridge); HA2 Ridge's salt sent to the rebuilt Lakeshore dome on a city tandem, weighed out at
  Ridge and in at Lakeshore; HA3 a wet supplier load weighed in and turned back at Mapleford.
- Stops (each a complete pipeline in `calc.py`, asserted): from the day after the survey with loads by sheet (the
  cracker's natural read, every figure off by 147 t or more); the day after the survey with the remarks read (every
  figure, 130 t or more); the survey day whole (every figure, 29 t or more); UTC as local (every figure, 87 t or more);
  by sheet (every figure, 272 t or more); supplier loads only (three yards, 43 t or more); the first dispatch issue (three
  yards, 17 t or more); the golden.
- Span: the survey report, the scale-house log, the dispatch schedules (both issues), the dome register, the plan, the
  dictionary (7 files).

**Ask B. For each works yard, the rock salt spread on its Priority 1 arterial circuits in each of the winters 2023-24,
2024-25 and 2025-26** (12 figures, tonnes to one decimal).
- H18 home: the yard table of the annual salt management report, read beside the commitment as the arterial
  programme's own use; a measure every yard carries that the call does not turn on.
- Primary B1 (D6, an event's quantity on every line it covers; silent): the arterial tandems still carrying the older
  spreader controller report a run's total, and the platform writes that total on every segment row of the run; the
  rows carry their own segment and entry times, so no key repeats and nothing is a duplicate. Summed as rows, every
  figure is high. Fair: the run reference groups them, and the fleet list dates each controller's replacement.
- Primary B1b (D9, a rollup above its parts; silent): the same controllers report the run's material as one mass, salt
  and spinner brine together, where the newer controllers report the salt alone beside the brine litres; the plan files
  the brine's weight (1.18 kg a litre). With the run totals taken once and the brine left in, every figure is high by 30
  t or more. Fair: the yard loading log shows those trucks spreading more than they were loaded.
- Primary B2 (D4, a reporter absent): three arterial circuits at Kelvin Road and Mapleford are run by Kettlewood Road
  Services under contract RW-2023-07, whose trucks report to its own system; its salt is in its monthly returns. Six
  figures move by 462 t or more.
- Hazards: HB1 UTC against the season's dates (frost patrols on arterials late on 31 October 2024 at Lakeshore and late
  on 31 March 2026 at Ridge); HB2 the 1 July 2026 realignment moved two Mapleford arterial circuits to Kelvin Road in the
  register, while the passes' route codes carry the yard that ran them.
- Stops (asserted): every row summed (the cracker's natural read, every figure off by 636 t or more); run totals once,
  brine left in (every figure, 30 t or more); brine netted on every row, run totals repeated (every figure, 578 t or
  more); the contractor left out (six figures); the register's yard (six figures, 817 t or more); season dates in UTC
  (two figures, 5 t or more); the golden.
- Span: the telematics export, the fleet list, the plan, the contractor's returns, the register, the revision log, the
  dictionary, the yard loading log (8 files).

**The report's chart** (`seasonal_salt_commitment_memo.docx`): Ask B's figures, each yard's three winters as labelled bars;
graded on its content (Ask B) and its parts (every yard and winter shown and labelled; the title).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 dispatch re-issue | the supplier re-cut its October schedule on 21 September | A | three yards' stock and room by 17 to 73 t |
| HA2 transfers | Ridge filled the rebuilt Lakeshore dome on a city tandem | A | Ridge and Lakeshore by 221 t when supplier loads only are counted |
| HA3 wet load turned back | a supplier load weighed in and out at Mapleford | A | Mapleford by 43 t when only inbound supplier loads are counted |
| HB1 UTC | the platform stores UTC | B | two figures, by 5.1 t and 6.5 t |
| HB2 realignment | arterials moved between yards on 1 July 2026 | B | Kelvin Road and Mapleford, every winter, by 817 t or more |

**Referee.** Ask A: the scale-house log's own times against the survey's flight log; Ask B: the yard loading log.
Neither hands over a figure.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control; both paths run on the cut pack by `generator/cracker.py`)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, dome stock and room | 8 | the survey's tonnes brought forward from the day after each survey by every weighing in and out on the yard's own sheet, transfers both ways, the latest dispatch issue | A1 the capture window in UTC and A2 the weighings at another yard's scale | miss |
| Ask B, arterial salt by yard and winter | 12 | the platform's arterial rows summed by the route code's yard, local season dates, the contractor's returns added | B1 the run totals written on every segment and B1b the combined salt and brine mass | miss |

Blind responses (`checks.py`): one network rate times each yard's arterial lane-km recovers none of Ask B's cells; no
single fill share of capacity recovers more than one of Ask A's.

Measured by: `generator/cracker.py` (run on the cut pack: each response scored on a rubric modelled on Part 0's weights,
the call and its components 38, the instructions 7, the asks 55 over every ask figure and the chart's parts).

Mirror leakage: 8.7 per cent of ask weight (the chart's two parts), measured on the cut pack.

Pair ceiling: 33.3 measured on the cut pack (the cracker 49.8, the mirror 16.8); with one device cracked 33.3, with both
of Ask A's devices cracked 42.8, with both of Ask B's 48.8.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | On the call |
|---|---|---|---|---|
| legacy summaries in kilograms, local time, per shift | the legacy AVL (to 30 September 2023) | the legacy export | kilograms read as tonnes | loud (a thousandfold); converted, same call (R2) |
| passes in tonnes and UTC | the telematics platform | the pass export | UTC dates for the season | same call (R2, asserted) |
| re-segmentation | the 2023 GIS release | the crosswalk | legacy ids joined without it | same call: no main-population segment is split (R2, asserted) |
| storm log layouts | the operations centre's incident board (2023) | the storm log | the Season WSI row summed with its events | the row equals the events' sum (R2, asserted) |
| night shifts dated by their start | the legacy AVL | the legacy export | dated by their end | same call: no collector shift on a season boundary (R2, asserted) |
| free-text revision reasons | the route audit | the revision log | none | none |
| dispatch re-issue, survey clock, weighings at another scale, transfers, wet load | the supplier, the survey contractor, the scale houses | the asks' files | the stops in `## Ask sheet` | none: no row the call reads |
| run totals, combined mass, contractor circuits, realignment | the older controllers, the contractor, the route audit | the pass export's arterial rows, the returns, the register | the stops in `## Ask sheet` | none: no row the call reads |

## Tried and rejected

- Pattern E on the card: E's discriminator is an absolute split, which this build does not have (the gain falls
  continuously with coverage), and the structural tests collided with five older builds; the pattern is none with G14.
- The city named Halbrook: within one letter of Holbrook (a real place); renamed Quellbrook after a check.
- The first collector parameters (Priority 1 hazard spots at 10.0 t and Priority 2 at 9.0 t a lane-km): the golden
  (2,206 t) sat on the midpoint of the default (2,652 t) and the pooled gain (1,768 t), so a response averaging two
  rivals filed the call; the hazard rates were re-set (9.7 and 10.2) and the earlier transit moves given inner-suburb
  coverage, so every midpoint of rivals now files 2,000 to 2,100 t.
- Centreline km asserted as neutral on the call: rates and lengths taken in centreline km throughout file 1,900 t,
  because collectors have two or four lanes; closed by the plan's application rates set per lane-km (SF3), not by data.
- One device carrying Ask B (the run totals alone): a cracker who dedupes per run recovered all twelve figures; the
  combined salt and brine mass (B1b) was added on the same controllers.
- Ask A's second device as transfers alone: it moved two yards only; the weighings at another yard's scale (A2) move
  all four, and the transfers stay as a hazard.
- Passes of one truck overlapping in time (two runs entering one segment in the same second): the sweep found them; a
  circuit's passes now run one after another on its one truck, with every tonnage unchanged.
- The forum `line_manager_or_team` (the director of roads signing the commitment): `ban.forum` blocked registration
  against task247, so the forum was redrawn to `council_or_assembly` in the build itself: procedure RO-PR-07 5 sends
  spending above the contract quantity to council under the procurement by-law, the deliverable became a one-page
  report to council, and the prompt names council; every figure unchanged.
- The supplier named Brackwater and the contractor Pellard: one letter from Blackwater and Pollard (H21); renamed
  Northgrit and Kettlewood after a search, every tonnage unchanged.
- Cross streets named without a suffix (a naming bug in the second round of street names): fixed in the generator,
  every tonnage unchanged.
