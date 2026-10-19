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
| Layer 1 | the AVL system replaced on 1 October 2023 (legacy segment-by-shift summaries in kilograms and local time, then one row per pass in tonnes and UTC); the 2023 GIS re-segmentation splitting long arterial and Priority 2 segments through a crosswalk; the storm log's layout change in 2023; free-text revision reasons; each winter's own swing in salt per point, common to every road; and on the asks' rows only, the supplier's re-issued dispatch schedule, the survey's capture window in UTC, weighings at another yard's scale house, trucks still weighed on the way for a day after each scale came back (the supplier's trucks on round trips from its terminal, each scale house's stored tares by account), inter-yard transfers, older controllers writing a run's total on each segment (four replaced in 2025, in Fleet Services' work orders), contractor circuits outside the telematics, the July 2026 yard realignment and the platform showing a renamed circuit's current code on its old passes (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `council_or_assembly` (spending above the contract quantity needs council's approval under the City's procurement by-law, so the winter operations manager's commitment goes to council as a one-page report before the supplier's 1 October deadline), forcing event `purchase_order_or_contract` (the supply contract's 1 October deadline for seasonal tonnage), organisation family `local_government`, role family `operations_director` (the roads division's winter operations manager), context artifact `register` (the winter route register), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the fleet telematics platform's segment-pass export (one row per spreader pass over one route segment, with the rock salt put down), 1 October 2023 to 23 September 2026, 344,770 rows, beside the legacy AVL's segment-by-shift summaries for November 2021 to March 2023; constructed in the layout of a winter-maintenance telematics export |
| Deliverables | `salt_commitment_2026-27.xlsx` (the commitment, its working and the ask tables) and `seasonal_salt_commitment_council_report.docx` (a one-page staff report to council recommending the commitment, with the chart of the arterial figures) |
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
each collector's Priority 2 winters in the spreader records measure how much of it was already treated (more of a short
block, whose intersection approaches are a larger share of it, and much more of a hill or a run of curves); the 377
collectors the route audit moved to Priority 1 from 2022 to 2025 were mostly hill, school, hospital and inner-suburb
transit streets moved because they were hazardous or dense with intersections, while the redesign put frequent service
on flat outer-suburb collectors whose Priority 2 trucks salted little beyond their intersections, so the gain the
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
4. Take the 216 segments' own rock salt per lane-km per WSI point over the five winters, all at Priority 2 (1.58 t a
   lane-km in a 61.7-point winter, about 700 t over the 424.0 lane-km).
5. The gain is (3) less (4), times 424.0 lane-km and 61.7 points: 2,613.3 t.

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
  the present salt) moves the call by about 400 t or 700 t.
- **Swap:** "how many more megawatt-hours to contract when 424 km of feeders move to a higher reliability tier" reads as
  a quantity, but no feeder tier treats only its hazard spots, so nothing makes the upgrade's gain fall with how much of
  each unit the old tier already served, and there is no storm severity to plan a winter at.
- **Layer 1:** each item is how the city's systems record a winter and none is placed to be caught, each asserted
  neutral on the call in `checks.py` (R2 rows): the legacy AVL's segment-by-shift summaries in kilograms and local time
  against the telematics platform's passes in tonnes and UTC; the 2023 GIS re-segmentation and its crosswalk (no
  main-population segment is split); the storm log's layout change; free-text revision reasons; the asks' own records
  (survey times in UTC, weighings at another yard's scale and the trucks still weighed there on the way after each
  changeover, the supplier's round trips and the scale houses' stored tares, transfers, dispatch re-issue, run totals on
  every segment, combined salt and brine mass, the fleet's work orders, contractor circuits, the yard realignment and
  the current circuit codes on old passes) sit on no row the call reads. Trucks rotate
  between circuits of their yard, the route audit keys each change in a few sittings and some after the change takes
  effect, the register pull holds the salted network only (the manifest says so), and each winter carries its own swing
  in salt per point that the index does not carry (about 14 per cent between winters, common to every road; netted
  against the never-moved collectors or not, the call holds, SF14).
- **Layer 2:** `estimation_fit`: the Priority 2 to Priority 1 gain carried from the 377 collectors moved in 2022 to 2025
  to the 216 new ones conditioned on each street's own Priority 2 salt per lane-km per point, against the pooled gain and
  the pooled Priority 1 level; both rivals are rejected out of sample (each move year held out, ten-fold
  cross-validation, and the new streets' band predicted from the rest), and every standard conditioned form, a power law
  included, files the same 2,200 t, the coarse ones closing on it as they are refined.
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
  own Priority 2 salt at the planning severity files 2,600 t; one who measures the before-and-after gain of the 377
  collectors moved since 2022 files 1,500 to 1,600 t; only the gain read off each earlier move's own Priority 2 salt
  files 2,200 t.
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
| R0b the Priority 1 network's salt per lane-km per point, gross, at the planning severity (5,400) | the procedure's "over what they needed before" | the register's priority | yes, the first rate | the earlier moves' gains are under a third of it | no | yes | readable |
| R1 default: the Priority 1 collectors' rate less the new streets' own Priority 2 salt (2,600) | the procedure's comparison invites it | the register's class and priority | yes, the careful netting | the earlier moves' post-move levels rise with their pre-move salt, for an analyst who looks | no | yes, one subtraction | readable |
| R2 the earlier moves' pooled before-and-after gain (1,500 to 1,600) | no | the revision log's dates | yes, the event study | holding out each move year shows its error following the year's coverage | no | yes, a mean | readable |
| R2b the gain of the transit-driven earlier moves only (1,500) | no | the revision reasons | yes, stratify on a visible field | the transit moves' coverage still sits well over twice the new streets' | no | yes | readable |
| R2c the pooled gain stratified by yard, lanes or length band (1,500) | no | the register's columns | yes, reweight | as R2 | no | yes | readable |
| R2d the golden's gain at last winter's 58.4 points (2,100) | the plan's severity normal | the storm log | a half-step | the procedure's planning severity | no | yes, a ratio | readable |
| R3 (decisive) the earlier moves' gain read at each new street's own Priority 2 salt (2,200) | no shipped sentence says how a street's salt responds to its service level or how much of it Priority 2 salts | no column holds coverage, hazard length or a gain; the property exists only as each street's own Priority 2 salt | no: the reflexes pool, net, stratify on visible fields, reweight or add controls, and each lands wrong | the held-out move years, the folds and the new streets' band score it, and score every rival wrong | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a fit across 377 streets read at 216 others | silent |

**The common-exposure subset screen, answered.** Read by its letter the screen applies: 151 of the earlier moves have
Priority 2 salt within 1.0 t a lane-km of the new streets' 1.58, and their lane-km weighted gain over 424 lane-km at 61.7
points files 2,189.5 t (within 0.5 t, 105 streets, 2,240.4 t), with no model. The subset is the golden method in its
cheapest form, not a bypass of it: it is defined on each street's own pre-move Priority 2 salt, the effect modifier the
solver must first decide to condition on, unlike an exposure the estimand names. Matched on any visible field instead
(yard, lanes, length band, the transit reason), the earlier moves file 1,500 to 1,600 t. So the difficulty sits in
recognising what to condition on, which no file names, and not in the arithmetic. One caveat stands: the plan's own
service-level line ("Salted at intersections, hills and curves during and after each event") tells a domain-literate
solver why coverage varies, which makes the effect easier to suspect; it says nothing of the gain or how to carry it
across, and it is the plan any roads division files.

## Semantic fork table

Every term in the main ask and every convention the main computation needs; every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "above the rolled-over 39,100 t contract" | only the change's additional salt | the change plus the rollover's own shortfall in a planning-severity winter | another quantity | the procedure 4.2 ("For each change in winter service approved since the last winter closed"); the redesign is the only priority change since 31 March 2026 (asserted) |
| SF2 | the additional salt | over what the same roads needed at Priority 2 | their whole Priority 1 salt | 2,900 t | the procedure 4.2 ("over what they needed before it") |
| SF3 | "424 lane-km" | the register's lane_km of the 216 segments (424.0), rates per lane-km | rates and lengths in centreline km | 1,900 t | the plan 2 ("application rates, which are set in kilograms per lane-km") |
| SF4 | the winter | 1 November to 31 March, local dates | the platform's dates in UTC; the supply season from 1 October | same call (no collector pass within six hours of a season boundary, none in October or April, asserted) | the procedure 4.2; C1 |
| SF5 | the severity | 61.7 WSI points | last winter's 58.4; the five winters' mean | 2,100 t; 2,000 t | the plan 4 ("Material planning uses the planning severity of 61.7 WSI points") |
| SF6 | salt against severity | per WSI point | a line with an intercept through the five winters | another figure: each winter's swing tilts the line (the never-moved collectors' five winters give an intercept of about a fifth of a winter's salt, 980 t of 4,700 t) | the plan 4 ("plans each road's salt per WSI point"), asserted |
| SF7 | "rock salt" | material RS | sand and salt rows | same call (collectors carry RS only, asserted) | the dictionary's material codes |
| SF8 | the moved roads | the revision log's 30 August 2026 entries | the transit agency's street list | same segments (asserted) | C1, asserted |
| SF9 | units in the legacy export | kilograms | tonnes | a thousandfold off, loud | the dictionary ("kilograms") |
| SF10 | rounding | the total to the nearest 100 t, once | the gain per lane-km rounded first | same call | the procedure 4.2 |
| SF11 | the earlier moves | every collector moved Priority 2 to Priority 1 on 1 November 2022, 2023, 2024 and 2025 | those with a transit reason only | 1,500 t (R2b, a rung, not a reading) | the revision log; the golden reads all 377 (asserted) |
| SF12 | the gain component's precision | about 5 t a lane-km, the whole tonne every family member shares (5.13 to 5.23) | one decimal (5.2 on the golden, 5.1 under four bands or the power law) | same call; the component is stated where every construction agrees | block 2 states it to the tonne; SF12 asserts every member rounds to 5 |
| SF13 | the own-salt component's basis | their salt over their lane-km and the five winters' points together (670.7 t, 1.58 t a lane-km) | the mean of the 216 streets' rates (1.70), of the five winters' rates (1.57), the three telematics winters (1.58) | the same figure at the stated precision (about 700 t, under 2 t a lane-km); a single winter alone (1.46 to 1.67) is outside the component's window | the component's own words ("over the five winters"), asserted on every basis |
| SF14 | each winter's swing | each winter by its WSI, the windows pooled | each winter netted against the never-moved collectors' same winter; one winter either side of each move | same call: netted 2,186.3 to 2,211.5 t; un-netted one-winter windows 2,162.5 to 2,227.1 t | C1 (FAMILY and SF14, asserted) |

## Ladder

Built figures from `generator/calc.py` on the shipped pack, every row asserted in `generator/checks.py` (LADDER, HEDGE,
OOS, FAMILY, CRUDE, SIGMA, ORTHO, TWIN). The graded quantity is the seasonal tonnage; each rung files a different figure.

| Rung | Construction | Tonnes | Dies to |
|---|---|---|---|
| R0 | last winter's Priority 1 network salt per lane-km, gross, at last winter's severity | 5,000 (5,045.3) | the procedure's comparison and planning severity |
| R0b | the same per point at the planning severity | 5,400 (5,392.8) | the procedure's comparison; arterials are not collectors |
| R1 default | the Priority 1 collectors' rate less the new streets' own Priority 2 salt | 2,600 (2,613.3) | the earlier moves' Priority 1 levels rise with their Priority 2 salt |
| R1b | the same with only the earlier moves' Priority 1 winters | 2,600 (2,586.5) | as R1 |
| R1c | the default at last winter's 58.4 points | 2,500 (2,473.5) | as R1, and the plan's planning severity |
| R1d | the default at the five winters' mean | 2,400 (2,354.9) | as R1c |
| R2 | the earlier moves' pooled gain per lane-km per point | 1,500 to 1,600 (1,516.2; its stratified, transit-only and never-moved forms 1,504.6 to 1,520.3) | held out by move year it misses by up to 18.8 per cent; the new streets' band predicted from the rest misses by half |
| R2b | the transit-driven earlier moves' gain | 1,500 (1,508.1) | their coverage is still well over twice the new streets' |
| R2c | the pooled gain stratified by yard, by lanes or by length band | 1,500 (1,504.6 to 1,520.3) | as R2 |
| R2d | the golden's gain at last winter's 58.4 points | 2,100 (2,095.3) | the plan's planning severity |
| R2e | the golden's gain at the five winters' mean severity | 2,000 (1,994.8) | as R2d |
| R2f | the earlier moves' ratio of Priority 1 to Priority 2 salt applied to the new streets' own salt | 600 (585.3) | the ratio falls steeply with coverage |
| R2g | the pooled gain trended across the four move years | 1,800 (1,773.3) | as R2 |
| R2h | the pooled gain against the never-moved Priority 2 collectors, winter by winter | 1,500 (1,507.1) | as R2 |
| R3 decisive | the earlier moves' gain regressed on each street's own Priority 2 salt per lane-km per point, read at the new streets' | 2,200 (2,213.7) | golden |

**Re-centring rule (written before the stage 4 changes to the noise and the coverage model were made).** After any
change to the world's noise or coverage model, only R_MID moves, in steps of 0.005 t a lane-km, and only until the
lane-km weighted golden sits within 15 t of its bin's centre; no other parameter is tuned against the golden, a rung, a
hedge or a crude construction. Applied after the first stage 4 changes: the golden came out at 2,202.6 t, so R_MID did
not move. Applied after the round 2 changes (each winter's own swing, the earlier moves' yearly counts set by their
programmes, the audit keyed in sittings): the golden came out at 2,219.0 t, 19.0 t from the centre; R_MID stepped from
6.297 to 6.282 in three steps (2,217.2, 2,215.5, 2,213.7 t) and stopped at the first inside 15 t. Nothing else moved
against a figure.

**Position and margins.** The golden is bracketed: every netting of an average Priority 1 level sits above it (R1 by
400 t), every average gain below it (R2 by 698 t), and the severity slips on either side of it off its bin (R2d 118 t
below, R1c 260 t above). Each correction from R0b walks down; only the decisive move turns up from the average gain.

**Hedges (asserted, HEDGE).** The golden is not the midpoint of the rivals: the midpoint of the default and the pooled
gain files 2,064.7 t, of the moves' own level and the pooled gain 2,051.3 t, of the default and the transit moves' gain
2,060.7 t, each at least 50 t outside the golden's bin. Last winter's totals netted with no planning severity (the
Priority 1 collectors' 7.25 t a lane-km less the new streets' 1.48) file 2,449.6 t, 2,400 t.

**Convergence (C1, asserted on the cut pack).** The golden family, 19 members: the gain or the post-move level regressed
on the pre-move salt, weighted by lane-km or not; the prediction summed street by street or at the pool's mean; each
winter against the never-moved Priority 2 collectors, or each winter's points netted by their swing, with the windows
pooled or one winter either side of each move; rates as the mean of each winter's; quadratic; outliers dropped; the 10,
20 or 40 nearest earlier moves; four, five or eight equal-count bands of Priority 2 salt. Every member files 2,200 t,
from 2,176.2 t (four bands) to 2,219.4 t (unweighted), the nearest 26.2 t from the bin's edge, and every member's gain is
about 5 t a lane-km (5.13 to 5.23; component 2 is stated at that precision, SF12). The power law (log Priority 1 level on
log Priority 2 salt) files 2,176.5 t, the same bin.

**Each winter's swing (asserted, SF14).** The never-moved Priority 2 collectors' salt per point runs from 0.925 to 1.051
of its five-winter level (2023-24 low, 2024-25 high), and the Priority 1 collectors' rate per point from 7.10 to 8.09 t a
lane-km in a 61.7-point winter, about 14 per cent: event mix, pavement temperatures and freezing rain the index does not
score, common to every road. A window of one winter either side of a move carries that winter's swing, so the family
reads one-winter windows netted against the never-moved collectors' same winter (2,194.5 to 2,211.5 t); un-netted they
stay in the bin (2,162.5 to 2,227.1 t), the first winter after each move 12.5 t from its edge.

**Crude settings (asserted, CRUDE).** Settings within the new streets' own spread of Priority 2 salt (0.51 t a lane-km)
file the golden: fixed 1.5 t and 1 t bands (2,198.5 t, 2,196.6 t), windows of 0.2 t and 1 t either side of the pool's
mean (2,234.4 t over 44 streets, 2,189.5 t over 151) and a 0.62 t kernel (2,185.0 t). Coarser settings slip toward the
pooled gain and close on the golden as they are refined: equal-count bands from two to six file 2,105.2, 2,147.8,
2,176.2, 2,195.5 and 2,198.4 t (three bands' second band, 2.2 to 5.2 t a lane-km, holds the new streets' upper eighth and
sits 1.1 t above them), kernels of 1.23, 0.9, 0.62 and 0.45 t file 2,120.7, 2,158.6, 2,185.0 and 2,198.6 t. Thin
settings settle in the bin once 30 or more streets carry them: the 10 and 20 earlier moves nearest the pool's mean file
2,294.9 and 2,280.3 t, 30 to 60 of them 2,233.5 to 2,235.1 t; a 0.1 t window (24 streets) 2,255.5 t. The range trim's
plain average (the earlier moves inside the new streets' range, R2i before) files 2,136.4 t, 2,100 t. The mean of
per-street ratios files 1,076.6 to 1,132.0 t (unweighted, by lane-km), 1,100 t.

**Standard error (asserted, SIGMA).** A bootstrap over the 377 earlier-moved streets puts one standard error of the
golden at 15.0 t; the golden plus or minus two of its own standard errors stays in its bin (36.3 t of clearance against
29.9 t), and every family member's point value sits more than one of the golden's standard errors inside the bin
(nearest 26.2 t). The claim holds with the golden's own error: the noisier members carry larger errors of their own
(the recheck measured 19 t for three bands and 52 t for the 10 nearest the mean on the previous draw), so they land on
the shipped draw rather than by construction, which is why the coarse and thin settings are listed apart. The relation
rests on 377 streets over four move years (136, 69, 119 and 53, each year's programmes) and five winters, one to four
winters either side of each move; each street carries its own persistent multiplier (5 per cent), a winter-to-winter
multiplier (7 per cent), each winter's common swing and each event's scatter.

**Out of sample (asserted, OOS).** Holding out each move year in turn, the conditioned gain predicts the held-out year's
total closer than the pooled gain in every year (5.2, 1.1, 4.1 and 1.9 per cent off, each year carrying its own
winters' swing, against 18.8, 6.4, 6.1 and 10.0 for the pooled gain); ten-fold cross-validation puts the line's weighted
squared error at 0.0507 against the power law's 0.0596 and the pooled gain's 0.5728; fitted on the moves above the new
streets' 90th percentile of Priority 2 salt and read on the 140 below it, the line misses their total gain by 1.9 per
cent, the power law by 12.8 per cent and the pooled gain by 50.9 per cent.

**Sweep (asserted, stumping Part 6).** Every reflex lands off the golden's bin and at least 100 t from the golden (the
nearest rung, R2d, by 118 t): pooled; stratified by yard, by reason, by lanes or length band; trended across move years;
with a control group of never-moved Priority 2 collectors; the ratio; netting the level. The hazard share (hills and
curves) is drawn independently of yard, lanes, length and route code (each sample correlation inside three sampling
errors, the largest 0.115 with length among the earlier moves against 0.155, asserted). The intersection approaches are
a larger share of a short segment, so Priority 2 salt per lane-km rises as segments shorten: plainly on the redesign's
streets, whose hazard share is small and alike (correlation with one over length 0.82), and hardly on the earlier moves
(0.01), whose hills, school frontages and hospital approaches vary far more than their intersection share and overlap
it (asserted on both pools, and 0.19 over the never-moved collectors).

**Twin pair (O1).** RS168717 and RS168888, two sections of Canterbury Street moved on the same date under the same
reason, same yard and lanes, centreline lengths within 0.06 km: gains 5.19 t and 2.16 t a lane-km in a 61.7-point winter
against Priority 2 salt of 1.93 t and 6.41 t. No visible field tells them apart.

**Worth on the graded quantity.** Seeing the conditioning is worth 400 t against the netting and 698 t against the
pooled gain; planning at 61.7 points rather than last winter's is worth 118 t.

**Strength (adversarial route list, P per strong solver).** The default netting (R1, R1b, 2,600) 0.30; the event study on
the earlier moves (R2, R2b, R2c, R2g or R2h, 1,500 to 1,800) 0.30; a severity slip on any route (2,000 to 2,500) 0.06; a
gross level (5,000 to 5,400 or 2,900) 0.04; a hedge between the rivals (2,000 to 2,100) 0.04; a contingency on a rival
(R2 plus 20 per cent, 1,800) 0.03; a coarse or thin conditioning (two or three bands, a wide kernel, the range trim, the
10 or 20 streets nearest the mean: 2,100 or 2,300) 0.05; the mean of ratios (1,100) 0.01; the conditioned gain in any of
its standard forms, netted or not, the power law included (2,200) 0.13; anything else 0.04. P(one strong solver lands)
about 0.13; P(both land) about 0.05 with a correlation of 0.3 allowed (0.13 squared plus 0.3 of 0.13 times 0.87). The
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
| 8 | Window length | all five winters against fewer | C1 across pre- and post-move windows, one-winter windows netted against the never-moved collectors (asserted; un-netted they stay in the bin, SF14) |
| 9 | Boundary inclusivity | the season's first and last days | nothing within six hours of either (asserted) |
| 10 | Rounding path | the total once, to the nearest 100 t | filed (the procedure); SF10 |
| 11 | Tie-break | none | n/a, one figure |
| 12 | Maturity and censoring | the new streets' Priority 1 winter not yet observed | the decisive forecast itself; nothing is censored in the records |
| 13 | Order of operations | normalise per point, then fit, then scale to 61.7 | filed (the plan plans salt per WSI point, SF6); C1 |
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

- The earlier moves (377 collectors, before and after): the evidence every route reads; on the wrong path they confirm
  the pooled gain in sample, and only a held-out year, a fold or the new streets' band shows the bias, which the solver
  has to run. They do not tie only under the golden.
- The never-moved Priority 2 collectors: a control for each winter's swing (the family's netted members read it);
  blind to the decisive move because none of them changed service (their gain is nil under every basis).
- The storm log's WSI: an input every route reads alike.
- The asks' referees (the scale houses' own times, tares and dockets, the trucks' round trips, the plan's pre-wet rate
  and the tandems' calibrations against the rows' litres, the work orders' controller replacements, the contractor's
  returns) sit on no row the call reads.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the AVL rows (both exports) of every collector segment, the winter route
register's collector rows, the revision log's priority entries for collectors, the storm log's WSI, the procedure and the
plan. Device and hazard rows in it: 0 (asserted, SEPARATION: every older-controller unit is an arterial tandem whose every
pass is on an arterial circuit, the collectors spread dry salt, no collector segment the call reads is split by the
crosswalk, no collector pass falls within six hours of a season boundary, the contractor and the realignment touch
arterials only, and the golden is unchanged with every ask file deleted). Against the shipped pack (target.zip d87ff77a)
the rubric repair left the files the call reads byte-identical, the platform export's collector rows identical and its
arterial rows identical in every column but the two realigned circuits' codes, the dictionary's rows for the call's files
identical, and R0 and R0b at 5,045.3 and 5,392.8 (asserted, SEPARATION).

**Ask A. For each works yard, the rock salt in its dome on 1 November 2026 once the October deliveries booked with the
supplier have landed, and the tonnes more the dome can then take** (8 figures, tonnes to one decimal).
- H18 home: where the seasonal tonnage can go, read beside the commitment for its delivery schedule; a measure every
  yard carries that the call does not turn on.
- Basis (filed in the plan's materials section, the owner's voice): "Each dome's stock is taken from its September
  survey and brought forward by the loads weighed in to it and out of it at the scale houses." The dome register gives
  capacities; the supplier's latest dispatch issue gives the October bookings.
- Primary A3 (D1, the same records under two sources; silent; the re-site of A2): when Lakeshore's new scale came into
  use on 15 September and Mapleford's was back from recertification on 21 September, the first B-trains bound there still
  weighed at Ridge and Kelvin Road on the way, as the outage routing had them do: a gross and six to nine minutes on the
  scale without tipping, then in again at their own yard's scale, where they tipped. On three of them the operator kept
  the outage remark ("for Lakeshore", "LKS", "MPF") and with it the receiving yard's account, whose stored tare the
  outage weighings used, so the two tickets repeat gross, tare and net; a reader who routes a remarked weighing to the
  dome it names counts the load twice, Lakeshore by 87.5 t and Mapleford by 43.2 t. The two tickets carry the two
  trailers' dockets of one B-train, one apart.
- Primary A4 (D7, the true key elsewhere; silent; the same cause): two more such trucks weighed at Ridge on 16 September
  and at Kelvin Road on 21 September with no remark, on that scale house's own account and its own stored tare for the
  truck, 260 kg and 240 kg below the receiving yard's, so their nets differ and only the truck, the day, the gross, the
  times and the docket pair tie the two tickets; a reader counts each as the weighing yard's own delivery, Ridge high by
  44.3 t and Kelvin Road by 44.4 t.
- Exposed by a consistency check, A3 and A4 alike (asserted): Northgrit's trucks run from its terminal, so none is back
  at a City scale with another load sooner than the drive back, the loadout and the drive out; every other same-truck
  pair of one truck's weighings on a day is 2 hours 36 minutes or more apart, and the five pairs are 35 to 58 minutes
  apart on one gross, the
  earlier ticket six to nine minutes on the scale and the later the 14 to 31 minutes of a load tipped there. The same
  weighing cannot be two loads without a truck reloading inside the hour. Once found it admits one handling: the later
  ticket is the load weighed in to the dome (the plan's basis), the earlier put nothing in to either dome, and the
  receiving yard's ticket carries the tare that yard's account stores for the truck on every load it tipped there (each
  scale house keeps one stored tare a truck for each account, asserted). Fair: no two loads that tipped share a truck, a
  day and a gross across the scale houses (asserted).
- Hazards: HA1 the supplier's dispatch schedule re-issued on 21 September (two loads cancelled, three moved into
  November, one added at Ridge); HA2 Ridge's salt sent to the rebuilt Lakeshore dome on a city tandem, weighed out at
  Ridge and in at Lakeshore; HA3 a wet supplier load weighed in and turned back at Mapleford, weighed out on the truck
  that brought it; HA4 (was A1) each dome's capture window in UTC in the survey's flight log, the yard holding deliveries
  through each flight; HA5 (was A2) the outage weighings at Ridge for Lakeshore (24 August to 14 September) and at
  Kelvin Road for Mapleford (14 to 18 September), the receiving dome in the operator's remarks in four spellings.
- Stops (each a complete pipeline in `calc.py`, asserted): both blind readers' paths and the judge's literal reading
  (every weighing after each flight, remarks routed, the double weighings kept: every dome high by 43.2 t or more); only
  the exact repeats of gross, tare and net dropped (Kelvin Road and Ridge, 44.3 t or more); from the day after the
  survey by sheet (every figure, 272.5 t or more); the day after the survey with the remarks read (every figure, 130.0 t
  or more); the survey day whole (every figure, 29.2 t or more); UTC as local (every figure, 86.9 t or more); by sheet
  (every figure, 272.5 t or more); supplier loads only (three yards, 42.8 t or more); the first dispatch issue (three
  yards, 17.0 t or more); the golden.
- Span: the survey report, the scale-house log, the dispatch schedules (both issues), the dome register, the plan, the
  dictionary (7 files).

**Ask B. For each works yard, the rock salt spread on its Priority 1 arterial circuits in each of the winters 2023-24,
2024-25 and 2025-26, counting each circuit under the yard it belonged to that winter** (12 figures, to the nearest
50 t).
- H18 home: an audit of the input the call consumes. The call reads the telematics export's collector rows; this ask
  reconciles the same export's arterial rows, by yard and winter, to the route audit's history and the contractor's
  returns, on rows the call never reads.
- The yard basis is WHAT and is filed in the ask's own sentence (the yard each circuit belonged to that winter, which
  the revision log's 1 July 2026 ROUTE and YARD entries give), so the register's current yard, the fleet list's current
  yard and the current code a pass carries are misreadings, not second readings.
- The 50 t rounding is what every honest correction of the older controllers shares: the records' own route (each run
  total once, the brine's mass taken off at the plan's 1.18 kg a litre) and the salt read back from the older
  controllers' litres at the plan's 40 litres a tonne agree to 0.07 t, every cell 17.9 t or more from a 50 t edge
  (asserted, and recomputed by the verifier on its own path). A flat halving of the older controllers' rows is a rougher
  correction (11 t below to 89 t above) and moves five of the twelve figures. Where a cell would sit within 16 t of an
  edge, the City trucks' newer-controller passes of that yard and winter carry the difference in proportion (a fraction
  of a per cent of each), on the simulated truth, so the platform and every total follow.
- Primary B1 (D6, an event's quantity on every line it covers; silent): the arterial tandems still carrying the older
  spreader controller report a run's total, and the platform writes that total on every segment row of the run; the
  rows carry their own segment and entry times, so no key repeats and nothing is a duplicate. Summed as rows, every
  figure is high. No column isolates the older controllers: the fleet list carries no controller column and no loader
  log ships; Fleet Services' work orders, a maintenance record of every City unit's jobs from July 2023 (services,
  inspections, calibrations, repairs), name a controller model only on the four replaced, M410 to M720, in the summer
  of 2025. Fair: every row of an older-controller run repeats one total (asserted over 18,705 runs), the run reference
  groups them, the unit-winters whose runs do so are exactly the 32 that ran an M410, and each of the four replaced
  units stops repeating its run totals across its work order (asserted).
- Primary B1b (D3, a meaning set per source; silent): the same controllers report the run's material as one mass, salt
  and spinner brine together, where the newer controllers report the salt alone beside the brine litres. With the run
  totals taken once and the brine left in, every figure is high by 48.8 t or more and lands a full 50 t cell or more
  above the golden's (asserted).
- Exposed by a consistency check, B1 and B1b (asserted): litres a tonne against the plan's pre-wet rate (40 litres to
  the tonne of salt, the brine 1.18 kg a litre) and every City tandem's calibration work order each autumn ("pre-wet
  checked at 40 L/t", the older units' included, so 38.2 is no lower setting). The newer controllers' rows carry
  40.0 and the older ones 38.2, and each replaced unit goes from 38.2 to 40.0 across its work order: the older
  controllers' tonnes cannot be salt alone. Once found it admits one handling: only the brine's whole weight off each run
  total restores the plan's 40.0; the brine's salt alone (23 per cent) leaves 38.6, and the brine's salt off every row
  puts the newer rows at 40.4.
- Primary B3 (D2, an attribute at the wrong vintage, a rename; silent; the re-site of HB2): the platform carries a
  renamed circuit's current code on every pass it ever made, so the two Mapleford circuits that passed to Kelvin Road
  on 1 July 2026 show KLV-A15 and KLV-A16 back to October 2023 and no pass carries MPF-A01 or MPF-A02; a reader who takes
  the yard from the code a pass carries counts both circuits at Kelvin Road in all three winters, six figures by 962.1 t
  or more. Fair: the revision log's ROUTE entries of 1 July 2026 take each current code back to the circuit it was
  (asserted); the dictionary describes the field as the circuit the pass ran on.
- Mirror device B2 (D4, a reporter absent): three arterial circuits at Kelvin Road and Mapleford are run by Kettlewood
  Road Services under contract RW-2023-07, whose trucks report to its own system; its salt is in its monthly returns,
  which the plan points to. Six figures move by 351.7 t or more.
- Hazards: HB1 UTC against the season's dates (frost patrols on arterials late on 31 October 2024 at Lakeshore and late
  on 31 March 2026 at Ridge, 8.2 t each way), which at the nearest 50 t moves no figure; HB2 the register's current yard
  against the yard a circuit belonged to that winter (six figures, 962.1 t or more).
- Stops (asserted): every row summed (every figure off by 1,032.3 t or more); run totals once, brine left in, which is
  the second blind reader's path and the judge's first reading (every figure, 48.8 t or more, a cell or more); the
  brine's salt off the older runs (every figure); brine netted on every row, run totals repeated (every figure, 939.2 t
  or more); the contractor left out (six figures, 351.7 t or more); the register's yard or the code's own yard (six
  figures, 962.1 t or more); the first blind reader's path (every figure); the golden. The judge's second reading, the
  brine's salt off every row, keeps seven of the twelve (`## Residual`).
- Span: the telematics export, the plan, the contractor's returns, the revision log, the work orders and the
  dictionary (6 files, under Part 4's eight, `## Residual`); the register and the fleet list are read by its
  misreadings.

**The report's chart** (`seasonal_salt_commitment_council_report.docx`): Ask B's figures, each yard's three winters as
labelled bars, beside the council report's line that the rolled-over contract carries the arterial programme; graded on
its content (Ask B) and its parts (every yard and winter shown and labelled; the title).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 dispatch re-issue | the supplier re-cut its October schedule on 21 September | A | three yards' stock and room by 17 to 73 t |
| HA2 transfers | Ridge filled the rebuilt Lakeshore dome on a city tandem | A | Ridge and Lakeshore by 221 t when supplier loads only are counted |
| HA3 wet load turned back | a supplier load weighed in and out at Mapleford | A | Mapleford by 43 t when only inbound supplier loads are counted |
| HA4 survey clock | the flight log is in UTC | A | every dome by 86.9 t or more when the UTC end is read as local |
| HA5 outage weighings | Lakeshore's and Mapleford's loads weighed at Ridge and Kelvin Road | A | every dome by 272.5 t or more when counted by sheet |
| HB1 UTC | the platform stores UTC | B | none at the nearest 50 t (two cells by 8.2 t) |
| HB2 realignment | arterials moved between yards on 1 July 2026 | B | Kelvin Road and Mapleford, every winter, by 962.1 t or more, when the register's current yard is read |

**Referee.** Ask A: the scale houses' own times against the survey's flight log, each truck's times between scale
houses against its round trip from the terminal, the stored tare each scale house keeps for a truck on each account,
and the dockets of one B-train on two tickets; Ask B: the plan's pre-wet rate and brine weight and every tandem's
calibration at 40 L/t against the rows' own litres, and the work orders' four controller replacements by unit and date.
None hands over a figure. The yard loading log the shipped pack carried handed over every arterial cell (each unit's
winter at its loader tonnes is the salt it spread, within its hopper's carry), so it is withdrawn (`## Tried and
rejected`).

**Cracker sheet** (the cracker landed the call and takes each blind scored reader's own path on the asks,
re-implemented in `generator/cracker.py` from that reader's method and run on the cut pack, with the determinism
judge's literal readings beside them)

| Ask row | Figures | Cracker's paths | Devices that hold | Verdict |
|---|---|---|---|---|
| Ask A, dome stock and room | 8 | reader 1: the survey's tonnes brought forward by every weighing in and out after each flight's start, a weighing at another yard's scale counted at the dome its remarks name, transfers both ways, the wet load netting to nil, the latest dispatch issue's BOOKED October lines; reader 2 and the judge: the same from each flight's end, the double weighings kept | A3 the remarked weighings on the way and A4 the unremarked ones on another account's tare (0 of 8 on every path) | miss |
| Ask B, arterial salt by yard and winter | 12 | reader 1: the arterial rows by the yard of the code each pass carries, the fleet list's older controllers halved (none named), the contractor's returns added; reader 2 and the judge's first reading: each older run once, the brine left in, the codes taken back, the returns added; the judge's second: the brine's salt off every row | B1b the combined salt and brine mass, and on reader 1's path B1 and B3 too (0 of 12 on both readers' paths and the judge's first reading; the judge's second keeps 7, `## Residual`) | miss |

Blind responses (`checks.py`): one network rate times each yard's arterial lane-km recovers none of Ask B's cells; no
single fill share of capacity recovers more than one of Ask A's.

Measured by: `generator/cracker.py` (run on the cut pack: each response scored on a rubric modelled on Part 0's weights,
the call and its components 38, the instructions 7, the asks 55 over every ask figure and the chart's parts). Both
readers' paths keep 0 of the 20 ask figures. One new device found on either path: the exact repeats dropped give back 4
(Lakeshore and Mapleford); the trucks' round trips checked give back all 8 dome figures; on reader 2's path the brine's
whole weight off gives back all 12 arterial cells; on reader 1's path the older runs once or the codes taken back give
back none.

Mirror leakage: 8.7 per cent of ask weight (the chart's two parts), measured on the cut pack.

Pair ceiling: 33.3 measured on the cut pack on either reader's path (the cracker 49.8, the mirror 16.8); with the exact
repeats dropped 38.1, with the trucks' round trips checked 42.8, with the brine found on reader 2's path 48.8.

Measured on the reshipped pack (target.zip 7fc71582) by two fresh blind scored readers (scored-task165c and
scored-task165d): both missed the call (2,600 and 2,700 t) and all eight dome figures (each kept both weighings of the
changeover trucks); on the arterials one found the run totals and the brine's weight from the work orders and the litres
a tonne and kept all twelve cells, the other kept none. The measured pair is 28.5. The re-judge on the final write-up
(judge-task165f) reproduced the call (2,200.06 t), all eight dome figures and all twelve arterial cells with block 3's
handling.

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
| trucks still weighed on the way after a scale came back, on one stored tare or another | the scale houses during the two changeovers (the outage routing kept for a day) | the scale-house log | a weighing counted at the dome its remark names, or at its own yard | none: no row the call reads |
| supplier trucks on round trips from the terminal, one stored tare a truck for each account at each scale house, dockets in loadout order (one to each trailer of a B-train) | the supplier's terminal and dispatch, the scale houses' weighing software | the scale-house log | none of itself (it is the check that exposes the weighings on the way) | none: no row the call reads |
| work orders on every City unit (services, inspections, calibrations, repairs, the four controller replacements of 2025) | Fleet Services' maintenance system | the work orders | a calibration's 40 L/t read as the controller's reporting | none: no row the call reads |
| run totals, combined mass, contractor circuits, realignment | the older controllers, the contractor, the route audit | the pass export's arterial rows, the returns, the register | the stops in `## Ask sheet` | none: no row the call reads |
| a renamed circuit's current code on every pass it made | the telematics platform (a circuit is one record, renamed in place) | the pass export's arterial rows | the yard of the code a pass carries | none: the call reads collectors by segment (its rows identical to the shipped export, asserted) |
| trucks rotating between circuits | yard dispatch (a spare or a swap most storms) | the pass export, the timesheets | a circuit read as one truck | none: the call reads salt by segment, whoever spread it |
| route audit sittings | the route audit keys each change in sittings of 40 to 90 segments on working days, a segment's priority and route rows together, one change in four finished after it took effect | the revision log | the entry date read as the effective date | none: the call reads the effective date (asserted no priority change after 31 March 2026 but the redesign's) |
| each winter's swing in salt per point | the weather the index does not score (event mix, pavement temperatures, freezing rain), common to every road | every salt record | one winter either side of a move read as typical | same call, netted against the never-moved collectors or not (SF14, asserted) |
| a pull of the salted network only | the register export's filter (Priority 1 and 2, and the Priority 3 hills) | the register, the manifest says so | the register read as every street | none |

## Residual

What stage 4 round 3 leaves standing, as measured (each figure from `generator/checks.py`, `calc.py` or the judge's
report):
- The round 3 judge's first advisory, on the dome asks: the scale-house log ends on 24 September and the supplier's
  October schedule starts on 1 October, so a movement on 25 to 30 September is in no shipped file; the golden, and the
  only literal answer the files support, counts none, and no competing answer can be derived from the pack. The judge's
  optional pin (one clause, movements to 24 September) was not taken: the prompt does not change.
- Its second advisory, on the arterial asks: the older controllers' fault (a run's total written on every segment row,
  gross of the spinner brine) is filed nowhere, by design, and no column names the controllers. Since the rubric
  repair's second round the pack documents them where a fleet would: Fleet Services' work orders replace four M410
  controllers with M720s in the summer of 2025 and calibrate every tandem's pre-wet at 40 L/t each autumn. The fault is
  found by consistency: one repeated total per run reference on exactly the 32 unit-winters that ran an M410, ending on
  each replaced unit across its work order, and 38.2 litres a tonne on them against the plan's and the calibrations' 40,
  which only the brine's whole weight restores. Layer 1 plus semantics inside the asks, which the rules allow, on rows
  the call never reads.
- The main call's margin. The golden files 2,213.7 t, 36.3 t inside its bin. The judge's own construction (the new
  streets' own Priority 2 salt as the mean of the five winters, 665 t) files 2,203.7 t, 54 t over 2,150 and 46 t under
  2,250, and its estimators land from 2,158 to 2,221 t; the one exception it found, a fit on the 2025 cohort alone (53
  moves, one winter after the move), files 2,300 t.
- The constructions outside the bin (Ladder, CRUDE): two and three equal-count bands (2,105.2 and 2,147.8 t), a 1.23 t
  kernel (2,120.7 t), the range trim's plain average (2,136.4 t), the 10 and 20 earlier moves nearest the pool's mean
  (2,294.9 and 2,280.3 t) and a 0.1 t window over 24 streets (2,255.5 t); each closes on the golden as it is refined or
  thickened. Inside the bin but near an edge: a 0.9 t kernel (2,158.6 t) and the un-netted first winter after each move
  (2,162.5 t).
- The arterial cells sit 17.9 t or more from a 50 t edge under the records' route, and the salt read back from the
  older controllers' litres agrees to 0.07 t; the brine left in lands a full cell high in every cell, and the UTC season
  dates move none.
- The rubric repair, two rounds. The first blind scored reader kept 14 of the 20 ask figures on the shipped pack while
  missing the call at 2,700 t; on round 1's pack the second kept none of the 20 (missing the call at 2,600 t) and the
  re-judge (judge-task165d) reproduced the call at 2,203.7 t but neither ask, keeping both weighings of each changeover
  truck (it could not find the rule) and reading the brine as an unfiled convention. Round 2 makes each device the
  finding of a consistency check (the trucks' round trips for A3 and A4; litres a tonne against the plan, the
  calibrations and the controller replacements for B1 and B1b) without filing either. Measured by `generator/cracker.py`
  on this pack: both readers' paths keep 0 of the 20; the judge's readings that keep the double weighings, the brine,
  or take the brine's salt off the older runs only keep none; the judge's other reading, the brine's salt (1.09 per cent
  of a tonne of salt) off every row, keeps 7 of the 12 arterial cells, because that cut sits within a few tonnes of the
  older runs' brine weight in seven cells; it cannot be moved without moving the frozen rows, and the newer rows'
  litres a tonne refute it (40.4 against the plan's 40). The price of a device a grader can find: one check gives back a
  whole ask, the trucks' round trips all eight dome figures (pair 42.8) and the brine on the second reader's path all
  twelve arterial cells (pair 48.8), both over the build's 40 and under the bar's 50; dropping only the exact repeats
  gives back 4 (38.1). Ask B's golden path is six files, under Part 4's span floor of eight; the realism of the
  changeover weighings rests on the outage routing being kept a day after each scale came back. Measured since on the
  reshipped pack: two fresh blind readers missed the call and every dome figure, one kept all twelve arterial cells and
  the other none, a measured pair of 28.5 (`## Ask sheet`).
- The round 3 reader's mild tells, left as they are: the survey's stocks sit a little off its printed volumes times
  1.20 t a cubic metre (4,980.4 t against 4,980.0), because the report converts the measured volume and prints volumes
  to the nearest cubic metre, as it says; one density serves all four domes (the bulk density agreed with the City); the
  two dispatch issues differ by a handful of reshuffled rows. The readings it noted on the asks (which dispatch issue, deliveries after 1 November,
  the realignment) are closed by the prompt's "October deliveries booked with the supplier", the later issue and "under
  the yard it belonged to that winter".
- The recheck's realism items not changed: the gain line reads r = -0.95 (it judged real records nearer -0.8), and
  1,338 km of collectors is on the large side for a city of 410,000.
- Duplicates: guard heart PASS (nearest driver 0.11, task118, differentiated at the draw); guard surface promotes nine
  pairs (task164 back to back and task453 and task159 on surface similarity; task163 and task167 two apart on the
  decisive gap and decision type; task465, task134, task146 and task54 on gap, pattern and decision family), each with
  a differentiation line on the card, left to the author's optional clone-check.

## Pre-ship check

The 10/10 rules read again against the shipped pack (target.zip d87ff77a):
- Rule 1, the domain: the deciding quantity is the extra rock salt per lane-km a collector needs when it moves from
  Priority 2 (salted at intersections, hills and curves) to Priority 1 (bare pavement), per point of storm severity at
  the plan's 61.7, which a roads division sizes from its own spreader records of the collectors it moved before,
  carried across by how much of each street Priority 2 already salted; the swap test holds (the judge's Gate H: pass,
  every round).
- Rule 2, two layers: Layer 1 is the AVL replacement (kilograms, local time and segment-by-shift summaries against
  tonnes, UTC and one row per pass), the 2023 crosswalk, the storm log's two layouts, the route audit's free-text
  reasons and sittings, trucks rotating, the register pull, each winter's own swing, and on the asks' rows only the
  dispatch re-issue, the survey's UTC capture, weighings at another yard's scale, transfers, the wet load, the older
  controllers' run totals and combined mass, the contractor's circuits and the realignment, each asserted neutral on
  the call (R2, SF4, SF14, SEPARATION). Layer 2 decides: the earlier moves' gain read at the new streets' own Priority
  2 salt, chosen over the pooled gain and the netted level out of sample (each move year held out, ten folds, the new
  streets' band).
- Rule 3: nothing planted, no filed method, no field marks coverage: the procedure files the WHAT (population, window,
  comparison, severity, unit), the plan files the severity and that salt is planned per WSI point (read by the round 3
  reader as its ordinary severity convention), and no column holds a coverage, a hazard length or a gain. The easy
  route on the clean truth files 2,600 t (R3a); the decisive step alone files 2,200 t (R3b). The rule 3 audit read PASS
  twice: round 1 (rule3/task165, on 24bfc51e) with two strength defects (the default at last winter's severity landing
  by coincidence, the common-exposure screen) and data too smooth, P(both) about 0.07, repaired (the 2025-26 winter
  redrawn to 58.4 points, each street's own variation, coverage by block length, the earlier moves widened, trucks
  rotating); round 2 (rule3/task165b, on 62835bde) at P(one) about 0.15 and P(both) about 0.06, its forks (the gain
  component's rounding, the own-salt basis, the one-sigma wording, the pooled rung's label, the length statement) and
  realism items (no common winter swing, the audit keyed row by row, steady yearly counts) repaired on d87ff77a. The
  note's own count at ship: P(one) about 0.13, P(both) about 0.05.
- Determinism: judge round 1 (judge-task165, on the stage 3 cut) NOT_DETERMINISTIC on supplementary answer 3 only (the
  arterial yard basis unfiled, no exact route for the older controllers), the main call DETERMINISTIC with Gates F, G
  and H passing, FIX_NOW: the yard basis filed in the ask's sentence, the pre-wet rate and the brine's weight in the
  plan; round 2 (judge-task165b, on 62835bde) DETERMINISTIC, FIX_NOW on the arterial precision (the loading-log
  calibration within 0.2 to 6.6 t of the exact route, unpinned at the tonne): the arterial figures asked to the nearest
  50 t, both routes 17.2 t or more from every edge; round 3 (judge-task165c, on d87ff77a) DETERMINISTIC, APPROVE, no
  fix: 2,203.7 t by its own construction, estimators from 2,158 to 2,221 t, the easy routes rejected on a hold-out (the
  mean gain 12 per cent off, the benchmark 7, the fit 3), all 8 dome and 12 arterial figures exact, Gates G and H and
  hygiene passing, its two advisories under Residual.
- Readers: round 1 (leak-task165) clean, Q6 an analytical choice; round 2 (leak-task165b) clean, with mild realism
  tells only; round 3 (leak-task165c) clean, the plan's per-point sentence read as its ordinary severity convention,
  its mild tells under Residual.
- Duplicates: guard heart PASS; guard surface's nine promoted pairs (Residual), each differentiated on the card and left
  to the author.
- Forum: the draw's `line_manager_or_team` was banned against task247, so the forum was redrawn in the build itself to
  `council_or_assembly` (procedure RO-PR-07 5 sends spending above the contract quantity to council under the
  procurement by-law; the deliverable is a one-page report to council and the prompt names council), every figure
  unchanged, the card's dates and stamps untouched.
- Gates at ship: checks 162, verify 29 on its own path, two byte-identical builds (target, golden, figures, write-up),
  figures_check 39, precut 51 checks with no FAIL or WARN, voice-check PASS, leak.py REVIEW answered (no LEAK),
  container audit clean on target/ and golden/, guard validate clean, heart PASS, surface exit 0, cracker pair ceiling
  33.3 and mirror leakage 8.7 per cent; the archive's 21 members equal the tree and metadata.json by content; target.zip
  d87ff77a from the final rebuild.
- Reship after the rubric repair (target.zip 7fc71582): the call side frozen (freeze.py rubric PASS; the eight files
  the call reads byte-identical, the platform export's collector rows and the dictionary's call rows the shipped rows,
  R0 and R0b unchanged), so rules 1 and 3 stand as read above; rule 2's Layer 1 on the asks' rows now carries the
  changeover trucks weighed twice among the supplier's round trips and the scale houses' stored tares, the older
  controllers found from their own rows beside Fleet Services' work orders, and the platform's current codes on the
  realigned circuits' old passes, each asserted off the call's rows (SEPARATION). Judges on the repair: judge-task165d
  (round 1's pack) and judge-task165e (round 2's) DETERMINISTIC on the call, SOLUTION_WRONG on asks whose handling the
  write-up did not name; judge-task165f (round 3's write-up) DETERMINISTIC, every figure reproduced, its two wording
  findings fixed in step 6. Readers: scored-task165b on round 1 kept none of the 20 ask figures; scored-task165c and
  scored-task165d on round 2 as above (measured pair 28.5). Gates at reship: checks 187, verify 33 on its own path, two
  byte-identical builds, figures_check 57, precut 51 with no FAIL or WARN, voice-check PASS, leak.py REVIEW (no LEAK, the
  ship's seven lines), container audit clean on golden/, guard validate clean, heart PASS, freeze rubric PASS; target.zip
  7fc71582 from the final rebuild, unchanged by round 3.

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
- The 2025-26 winter at 52.6 WSI points: the default netting at last winter's severity, or last winter's totals netted
  with no planning severity, landed 2,200 t by coincidence (52.6 sat inside the band, about 51 to 54 points, where the
  netting's figure scales into the golden's bin); the storm sequence was redrawn to 58.4 points, the per-point golden
  unchanged, and the route now files 2,400 t (asserted, LADDER R1c and HEDGE).
- Street rates as steady as a model (a 4 per cent winter-to-winter variation, the gain line at r = -0.98) and coverage
  blind to block length: each street now carries its own winter-to-winter multiplier, Priority 2 salt rises as blocks
  shorten, and the earlier moves were raised from 202 to 431 so that one standard error stays under 16 t; the golden
  came out at 2,202.6 t, inside the re-centring rule's 15 t, so R_MID did not move.
- The earlier flat moves given less coverage than the new streets (a different hazard share): the banded estimators
  then filed 2,100 t; the flat streets each reason brought in now carry the redesign's own hazard share, and every
  standard banding files 2,200 t.
- Ask B's arterial figures to one decimal with the yard basis left to the reader: the judge found the register's
  current yard a licensed second reading (about 800 t a winter at Kelvin Road and Mapleford) and no exact route for the
  older controllers; the ask now files the yard each circuit belonged to that winter, the plan files the pre-wet rate
  that makes the combined mass exactly checkable, and the figures are asked to the nearest tonne, which every honest
  construction shares.
- Every circuit run by one truck for three winters: trucks now swap between circuits of their yard and kind about one
  storm in seven; every tonnage unchanged in kind.
- The council item filed as a memo: a council item is a staff report, so the deliverable is
  `seasonal_salt_commitment_council_report.docx`, with the chart introduced as the programme the rolled-over contract
  carries.
- Cross streets named without a suffix (a naming bug in the second round of street names): fixed in the generator,
  every tonnage unchanged.
- Winters as steady as the index (the Priority 1 collector rate per point within 2 per cent across winters of 38.9 to
  67.2 points, the recheck's realism finding): each winter now carries a swing the index does not carry, common to every
  road (a winter's multiplier drawn with a 3 per cent spread, the realised rate per point spanning 14 per cent, inside the
  10 to 25 per cent real fleets show); R_MID then moved by the re-centring rule alone.
- Salt in proportion to severity closed by the data (the never-moved collectors' intercept near nil): under each
  winter's swing five winters tilt the line (an intercept of about a fifth of a winter's salt), so the plan now files
  that salt is planned per WSI point (SF6).
- One-winter windows as plain family members: each carries its winter's own swing; the family reads them netted against
  the never-moved collectors' same winter, and un-netted they stay in the bin, no longer a quarter-bin clear.
- 431 earlier moves in steady yearly counts (122, 112, 107, 90): each year now carries its own programmes (136, 69, 119,
  53, 377 in all); one standard error rose from 14.7 to 15.0 t.
- Three equal-count bands as a family member: on the new draw its second band (2.2 to 5.2 t a lane-km) holds the new
  streets' upper eighth and sits 1.1 t above them, and it files 2,147.8 t; it is listed with the median split and the
  wide kernels as a coarse setting that closes on the golden as it is refined, and nothing was moved to bring it back.
- The 10 earlier moves nearest the pool's mean as a crude setting that lands: it files 2,294.9 t on this draw; thin
  settings are asserted from 30 streets up, where they settle in the bin.
- R2i (the earlier moves inside the new streets' range, averaged) as a rung 100 t or more from the golden: it now sits
  77 t below (2,136.4 t), so it is listed with the crude conditioned forms.
- The gain component at one decimal (5.2, 0.045 from its edge, with four family members at 5.1 on the previous draw):
  stated as about 5 t a lane-km, the precision every construction shares (SF12).
- The own-salt component at one decimal (1.7 lane-km weighted against 1.8 as the streets' unweighted mean, the
  recheck's fork): stated over the five winters as about 700 t, under 2 t a lane-km, which every basis shares (SF13).
- The arterial figures to the nearest tonne: the loading-log calibration came within 0.2 to 6.6 t of the records'
  route, so the correction of the older controllers was unpinned at the tonne; the figures are asked to the nearest
  50 t and every cell sits a quarter-bin or more from its edge under both routes (asserted), while the brine left in
  still lands a full cell high and the run totals summed every row miss by a tonne a row.
- Route audit entries keyed row by row (the redesign over 52 days, a segment's priority and route rows on one day 2.8
  per cent of the time): the audit keys each change in a few sittings on working days, both rows of a segment together,
  and the change numbers follow the keying order.
- The one-sigma claim as written (every family member within one standard error): it holds with the golden's own
  error, not each member's; restated in `## Ladder` and in SIGMA.
- "On every pool alike" for the length effect: measured, it shows plainly on the redesign's streets and hardly on the
  earlier moves; the note now says what the data show and both pools are asserted.
- A2, the weighings at another yard's scale with the receiving dome in the remarks: the stage 4 blind reader read the
  four spellings and moved each load to the dome they name (Lakeshore's only after its flight), keeping all eight dome
  figures; re-sited as A3 and A4, the trucks still weighed on the way for a day after each scale came back, which the same
  remark routing counts twice or keeps at the weighing yard; the outage weighings stay as texture (HA5).
- A1, the survey's capture window in UTC: the reader converted the flight log to Eastern daylight time and cut at each
  flight's start; a clock re-sited onto the scale houses (a terminal on standard time, or one stamping UTC) was tried and
  dropped, since the yards held deliveries through every flight, so a cut at the flight's start agrees with one at its
  end for any offset under an hour, and a log stamped in UTC has nothing in the pack that forces the reading; it stays as
  texture (HA4).
- HA1, the dispatch re-issue: the reader took the latest issue's BOOKED October lines; re-siting it as an October booking
  delivered early in late September was tried and dropped, since nothing in the pack ties a September weighing to an
  October booking without a filed note; it stays as texture.
- B2, the contractor's circuits: the reader added every row of Kettlewood's returns, which is right; two re-sitings were
  tried and dropped, relief operators on City trucks reported in the returns (the rows would have to name City units,
  which announces it, and a contractor reporting a City truck's salt reads as planted) and returns by billing period, the
  26th to the 25th (it moves only Kelvin Road's and Mapleford's 2024-25 cells, the one winter with storms after 25
  March); it stays as the mirror device.
- HB2, the register's current yard: the reader took the yard from the route code as run and kept MPF-A01 and MPF-A02 at
  Mapleford; re-sited as B3, the platform carrying the two circuits' current Kelvin Road codes on every pass they made,
  so the code a pass carries is the misreading and the revision log's 1 July 2026 entries are the key.
- B1 and B1b, the run totals and the combined mass: they held six cells, and the reader landed the other six by halving
  the fleet list's M410 rows after reading them double against the loader log (a yard's runs average about two segments,
  so halving sits inside a cell where the brine and the run lengths offset); the evidence is re-sited from the fleet
  list's controller columns and the loader log to the rows' own run references and litres, the rows untouched (R0 and R0b
  read them as written).
- The yard loading log: each unit's winter at its loader tonnes is the salt it spread within its hopper's carry, so a
  loader-only route lands every arterial cell and the per-unit ratio hands any reader the halving, an oracle under ban 3;
  withdrawn, with the settle that kept the loader calibration inside each cell left as it was so the arterial rows stay
  byte for byte.
- The changeover weighings as one device: with every copy on the receiving yard's stored tare, dropping exact repeats gave
  back all eight dome figures (a pair of 42.8 with one device found, against the build's 40); the two unremarked copies
  carry their own scale house's older stored tare, so only the truck, the day and the gross tie them (A4).
- HB1, the UTC season dates: the reader converted them; nothing at a season boundary carries enough salt to move a cell,
  so it stays as texture.
- A3 and A4 as built in the repair's first round: invisible to a grader who checks consistency, since the supplier's
  trucks were drawn at random for each load (some at two scale houses minutes apart on ordinary days) and the tares at
  random for each weighing, so nothing contradicted a load weighed twice; the re-judge (judge-task165d) kept both
  weighings and could not find the golden's rule. The trucks now run round trips from the terminal and each scale house
  keeps one stored tare a truck for each account, so the five pairs are the only trucks back inside a round trip.
- B1 and B1b with nothing naming the controllers (the first round): the re-judge read the counting once as inferred and
  the brine as an unfiled convention, its brine's salt off every row keeping seven cells; Fleet Services' work orders
  now carry the four replacements and every tandem's calibration at 40 L/t, so the litres a tonne force the brine's whole
  weight and the work orders tie the repeated totals to the controller.
- A supplier's delivery statement by docket as Ask A's referee: one reconciliation would expose all five weighings at
  once and its loadout weights would offer a second dome basis beside the scale houses; the trucks' own times between
  scale houses do the work inside the log the ask already reads.
- Filing the older controllers' conventions in the dictionary (the re-judge's fix): a filed sentence that adjudicates,
  handing B1 and B1b to every reader; not taken.
- The controller model on every calibration work order: a controller list by unit and winter, the fleet list's
  withdrawn columns in another file; the model is named only where a controller was replaced.
- The asks' handling left to the pack alone (rounds 1 and 2): both re-judges, cold on the pack, took the readers' paths,
  and judge-task165e never tested the trucks' round trips, so the dome figures read as wrong although every arterial
  cell reproduced; block 3 now names each ask's handling, its filed basis and its result (steps 6 and 7), the pack
  unchanged.
- Step 6's first wording (round 3): the dome stocks followed the dispatch file's BOOKED October loads, and
  judge-task165f read them as the booked loads; each figure now carries its label, and the home yard's ticket cites
  RO-PR-07 section 2's "weighed at the yard's scale house".
