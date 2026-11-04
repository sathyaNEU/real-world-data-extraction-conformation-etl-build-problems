# task210 design note (architecture 2)

Ashcombe Regional Transit's streetcar: the four restricted-speed slots of the January and February 2027 weekday peaks,
placed on each section direction's expected firm-braking rate after an autumn rise the record's own fields do not
explain. Architecture 1 (Ravensby Quarry's haul-noise world) was spent at stage 4 round 2 and is kept only in the card's
lineage and in `## Tried and rejected`.

## Draw

**Card.** `cards/task210.json`, architecture v2, registered 2026-11-04T14:49:22Z. Pairing `human-factors-ergonomics` /
`safety-incident-error-analysis` / Anomaly Detection & Diagnostics (the task type serves RC and AD). Shape 01 (ranked
list under a cap), decision `ranked_slate_under_cap`, answer unit `set_of_items`, gap time then population, pattern none
with G13 (horizon mismatch) then G16, Gate G `forecasting`, strategy `decomposition_attribution`, Layer 2 family
`estimation_fit`, pattern `own:low-sun-glare-geometry-carried-to-the-forward-window`, context artifact `filed_standard`,
calibration none. Forum `operations_desk`, forcing event `launch_or_rollout` (the January pick starts on 4 January
2027), org family `government_agency`, role `compliance_or_audit` (the chief safety officer). Personas from
`guard.py names --geo US --seed 210`: Brandi Lutz, Deanna Wagner, Maureen Phillips.

**Guard.** `check` WARN, exit 0, then `register`, then `check` on the registered card. Answered:
- `overuse.org_family` (government_agency in 43 builds): a regional transit authority is a government agency; any other
  family would mislabel the organisation that issues the orders.
- `test.same_driver_older` NOTE: (time, G13, forecasting) repeats seven older builds, each differentiated on the card
  (task102's business-day release rule, task130's reporting windows and judges' visits, task134's announced threshold
  step, task162's restart burst, task171's renewal clock, task178 redraw 1's tidal level, task501's cumulative path).
  Gate G was first drafted `decomposition_attribution`, which blocked against task401 v5 inside the batch; `forecasting`
  ("a forecast the correctly read past does not pin") is the honest key: the autumn record read correctly does not pin
  January's slate.
- Nearest driver 0.07 (task478 v4 lineage, position reports displaced along the direction of travel); every other
  driver on file 0.05 or under.

**Seed.** AD33 (a data-centre battery's January FCR-D offer). Its world became legal on the subdomain axis once
task211 registered and task402 left the window, and was set aside on screen 4 (`## Tried and rejected`). The build
keeps the seed's lesson shape only in the broadest sense (a usage set by where scheduled conditions fall, which averages
hide); world, decision, quantity and pitfall are this build's own.

**World.** Ashcombe, a fictional mid-sized city in the Mountain West on Mountain Time (about 38.8 N, 104.8 W), sunny
winters. Ashcombe Regional Transit (ART) runs a two-line streetcar, the Juniper Line and the Foundry Line: twelve
street-running sections and two on reserved track, each run in both directions, on a 7.5-minute headway from 06:00 to
24:00. The fleet's event data recorders were replaced in March 2026, so the firm-brake record (deceleration of 1.3 m/s2
or more held for a second, flagged by the recorder) runs from 1 April to 31 October 2026.

**Decision.** By the January pick (4 January 2027) the chief safety officer issues the Restricted Speed Orders for the
weekday peaks of 4 January to 26 February 2027. The pick's running times carry recovery for four restricted
section-direction peaks. ART's Safety Risk Management Procedure SRM-07 files the WHAT: every section of track in each
direction of travel in each weekday peak (06:30 to 09:00 and 16:00 to 18:30) is a candidate; the outcome is firm-brake
events per 1,000 passes; the window is the pick's weekdays; the basis is the pick timetable's scheduled passes under the
airport station's 1991 to 2020 normals; the four highest expected rates take the slots. No sentence names the sun, a
heading or a direction's orientation.

**Data-native sentence.** The recorder logs each firm brake's time and position and the survey gives each section
direction's line, but the sun's position appears in no file, and in Ashcombe's January the low sun crosses the peaks
ahead of other directions of travel than it did in the September and October record.

**Abstraction sentence (against the nearest approved builds).** Against task102 (a release rule moves a forward
period's payments) and task162 (a device acts only above its setting), no sentence a reviewer holding both would call
the same: here an external, computable source re-sorts which units carry an excess, so the units that rose are not the
units that will. The driver with the nouns stripped is on the card.

**Sources.** Every file synthetic, generated from one seed, invented world, no real organisation, licence CC BY 4.0,
recorded in `metadata.json`: the recorder export (UTC, WGS84), the AVL section-pass log (local time, lead vehicle), the
track survey (GeoJSON, RFC 7946 longitude and latitude), hourly airport observations (METAR sky strings at :53 UTC),
the yard's block sheets (pull-out cars, out and in times), the Foundry depot's release log, the run sheets (the
day's schedule, duty and revenue hours), the operator
roster, the badge card register, the maintenance system's defect reports (operator cards and inspection findings,
each with the time it was entered),
SRM-07 (PDF), the January pick timetable (PDF), the station normals (PDF), the rail operations dashboard (workbook), and
three distractors named only in `metadata.json` (pedestrian counters, the arena's events, track maintenance) beside
the school calendar the careful readers use. Eighteen files, five formats, the AVL log 623,550 rows at the actual
running (trips leave late and run times vary; the pick gives scheduled times, revised by direction). SRM-07
files no definition of low sun or darkness: the survey's coordinates, the pick's clock and the normals are plain
operating facts, and the glare response is the analyst's to estimate.

**Task400 setting line.** task400 is an iron-ore mine's haul-truck collision alerts after a firmware change, read from
vehicle event recorders and braking-type events: its driver is a device change's effect on alert counts; here no device
changes, and the driver is an external light source computed from a clock and a bearing that re-sorts which directions
of travel carry the excess in the forward window.

**Gate G.** No shipped artifact ranks or sorts section-direction cells or flags a top set: the dashboard is monthly
and line-level, unsorted, with FB, EB and OS counts and the line's FB rate as data; no file lists cells with a rate.

**The five go/no-go screens, on the corrected sun and the corrected blocks** (`generator/solar.py` wraps the hour angle;
the first draw's sun put every Mountain evening sun east of the meridian; every block now runs out and back,
`## Block repair`). Forty redraws on the real generator (seeds 21001 to 21040, scratchpad `t210/a2/blocks/redraws.py`),
then a cut pack for each of the 22 seeds that passed the main-call screens and for 21019 (`seedpack.py`: the
separation from `target/` and every ask route) and the corridor for the four that passed the asks (`corridor.py`); the
shipped seed
21030 is the one that holds every proof, and its numbers are asserted in `generator/checks.py`:

1. **Realistic levels and the lever.** Sun position from NOAA's General Solar Position Calculations, anchored at every
   build against NOAA's solar calculator equations (`generator/solar_ref.py`, a separate implementation the generator
   never imports): sunrise and sunset on 21 June, 21 December and 15 January and the January peak hours' sun against
   the J4 and F5 bearings agree within 0.5 degrees in `checks.py`, and `verify.py`'s Almanac sun agrees too; January and February sunshine 68 per cent of
   possible (station normals); glare raises crash risk on approaches facing a low sun (Mitra 2014, Safety Science 70,
   246 to 254), glare situations predicted from alignment and sun position (Jurado-Pina and Pardillo Mayora 2009,
   Transportation Research Record 2120, 12 to 17); darkness raises pedestrian risk severalfold (Sullivan and Flannagan
   2002, Accident Analysis and Prevention 34, 487 to 498). World-set: firm braking 20 per 1,000 street passes and 8 on
   reserved track; the full-alignment multiplier 3.2 under full sun. The golden recovers the true slate in 34 of 40
   redraws; at the shipped seed the fourth slot clears the fifth by 36.9 per cent on the clean truth, 37.0 per cent
   from `target/` (J5-O AM over J3-O AM) and 33.8 per cent in the independent verifier (the truth's own margin 28.3).
2. **The golden's own method holds the call, and the record decides the glare form.** No sentence defines low sun, so
   the response's cone, elevation profile and shape are the analyst's. On `target/` all 75 forms were fitted (cones 15
   to 35, five elevation profiles, cosine-squared, linear and flat shapes): every tapering form at every cone and
   profile, and every flat form to 20 degrees, prints the golden slate (60 cells, the fourth slot at least 13.2 per
   cent clear); the 36 forms the record supports (twice the log-likelihood within 10 of the best) print it too. The 5
   forms that print another slate are all flat at 35 degrees, and the record refutes them by 42.4 or more: its own
   excess is 1.73 with the sun 0 to 5 degrees off the line of travel, 1.11 at 10 to 15, 0.74 at 15 to 20 and 0.00 at
   20 to 25 (standard errors 0.13 to 0.25).
3. **The first look lands wrong**: 40 of 40, at most two slots shared.
4. **The careful readers land wrong**, 40 of 40 each: (a) field-decomposing (the default path), at most two shared;
   (b) constructing (a non-directional low-sun term; sun-time by elevation bins), at most two and one; (c) per-record
   in three month pools, at most two (every month), two (September to October) and two (October); (d) the glare-naming
   reader that carries the record forward (the observed September to October alignment, or the fitted model with each
   cell's April to October or September to October alignment held), at most two, one and two; (f) each cell's monthly
   trend carried to January (four forms), at most two, two, two and three. At the shipped seed the first look, the
   default path and readers (d) share no slot; the non-directional low-sun term shares one, the October pool two and
   the trend forms one, one, two and two.
5. **Literal execution of SRM-07, with no definition of low sun filed**: the record's rate since 1 April (4.2), that
   rate at the normals' sunshine (4.1), at the pick's clock hours and sunshine, and with January's dark share: 40 of 40
   wrong, at most two slots shared across the redraws and at most one at the shipped seed (one each from `target/`).
   The recency readings (October alone, September to October) share at most two and two.

Competing causes (new operators, school mornings, darkness) are real, documented and modest; removing each from the
shipped realization (thinned, not redrawn) leaves the golden slate (asserted).
## Three rules

- Task type: Human Factors & Ergonomics, `safety-incident-error-analysis` (serves RC and AD): firm-brake events are
  the streetcar's near-miss record, and the task diagnoses what produced their autumn rise and where that condition
  will bear in the coming pick.
- Domain test: the deciding quantity is the firm-braking excess the low sun produces when it stands ahead of the
  operator, a visual performance-shaping factor estimated from the event recorder against the sun's computed position
  relative to each direction of travel, the way human-factors incident analysis attributes errors to the condition that
  produced them.
- Swap: "what drove the autumn rise in the ward's medication errors, and on which ward and shift must the four extra
  pharmacists go in January" keeps a rise, a slate and a capped resource but loses the operator's line of sight, the
  sun standing ahead of a direction of travel and the season moving it onto other directions, so the call stops
  reading.
- Layer 1: the recorder's UTC stamps against the AVL log on Mountain daylight time and the January pick on standard
  time (the recorder system and the scheduling system keep their own clocks); recorder positions with GPS scatter; the
  AVL onboard units' drop-outs and a detector outage week at Arsenal Road; cars swapped in service with the yard sheet
  keeping the pull-out car; METAR sky-condition strings at :53 with missing hours; the January pick as a PDF table of
  headways and running times; the maintenance system's cards keyed the morning after. None is placed to be caught and
  none decides the call (each asserted inert in checks.py).
- Layer 2: estimation that fits the data (`estimation_fit`): the excess braking is attributed to the low sun ahead of
  each direction of travel, its response estimated from the record, and carried to the pick's passes under January's
  and February's sun; the choice that flips the call is reading the excess as a property of the sun's position rather
  than of the cell where it was measured.
- Decisive step: the sun's position at every pass, computed from the clock and the city's latitude and longitude, set
  against each section direction's line from the survey, with the excess it produced estimated on the record and
  carried to the January and February peaks.
- Not semantics: reading every field, code, clock and unit correctly (the UTC stamps, the coordinates, the sky codes,
  SRM-07's population, outcome and basis) still leaves each cell's measured rate, which carries the autumn sun's excess;
  no filed sentence names the sun, low sun or glare, so nothing read correctly points at the step.
- Not rule application: SRM-07 files the population, outcome, window, basis and comparison and nothing about how the
  expected rate is formed, and no sentence defines low sun, so executing every filed rule (the record's rate, at the
  normals' sunshine, at the pick's hours) files a wrong slate in 40 of 40 redraws, sharing at most two slots; the
  enumerated family (rate tables, the field-decomposing and per-record models, two sun-elevation constructions, four
  trend forms, the literal executions) files 0 golden slates in 40 redraws, while the standing family (every glare
  form the record supports) agrees on the slate, and what rules the enumerated family out is loud on the record: the
  excess sits only on sunny passes, only in one direction of a section, and only while the sun is low ahead.
- Analyst test: a strong analyst who conforms the recorder's UTC events to the surveyed sections and the AVL passes,
  nets new operators, darkness, sky cover and the school term, and reads SRM-07's normal-weather basis correctly slates
  F3-I AM, F4-O PM, J2-O AM and J3-O AM (the default path's `Ends on:`), the east-running morning and west-running
  evening cells with the record's highest rates, while January's sun stands ahead of the south-east-running morning and
  south-west-running evening directions that carry the golden slate.
- Estimand: SRM-07 section 4 (the procedure PDF) files the population (every section of track in each direction of
  travel in each weekday peak), the outcome (firm-brake events per 1,000 passes), the window (the January pick's
  weekdays, 4 January to 26 February 2027), the basis (the pick timetable's scheduled passes under the airport station's
  1991 to 2020 normals) and the comparison (the four highest expected rates take the slots).
- No decoy: nothing is planted to be caught; no copied block, hidden rule, memo, draft, briefing or stakeholder figure
  carries a wrong slate, and ART's monthly dashboard reports line-level rates only, never a ranking of cells.
- No certified replay: no published or certified figure is shipped for the golden's method to reproduce; the projection
  is argued from the record and the sun's geometry, and the standard states the WHAT in full.
- Lesson: an anomaly's driver can be an external condition no record holds but physics computes, and when the coming
  window moves that condition onto other units, the units that rose are not the units that will; no build on file
  carries a computed light source re-sorting units (`guard.py slots` on glare, sun, solar, azimuth and dazzle: none).
## Default path

1. Read the recorder export, convert its UTC stamps to Mountain time, and attach each firm brake to the AVL pass of the
   car that logged it (section and direction from the log, checked against the survey's coordinates).
2. Count each section direction's passes in each weekday peak, April to October, from the AVL log.
3. Rate each section-direction peak as firm brakes per 1,000 passes (the field's exposure rate for near misses).
4. Net the autumn's visible confounders with a Poisson model by cell and month: the new operator classes (the roster
   and run sheets), dark passes, sky cover from the airport observations, the school term.
5. Carry each cell's adjusted rate (its October level) to January and February, with January's dark share and the
   normals' sky cover.
6. Slate the four highest cells.

Ends on: F3-I AM, F4-O PM, J2-O AM and J3-O AM, the east-running morning and west-running evening cells with the
record's highest rates (no cell of the golden).
Golden: J4-O AM, J5-O AM, F5-O PM and F6-O PM, the south-east-running morning and south-west-running evening cells.
## Stump sentence

The default path ends on F3-I AM, F4-O PM, J2-O AM and J3-O AM, the east-running morning and west-running evening cells
with the record's highest rates, because it reads each cell's measured rate, adjusted for operators, darkness, sky cover
and the school term, as the rate January's peaks will see; their excess was the low sun standing ahead of those
directions from April to October, and in January and February it stands ahead of the south-east-running morning and
south-west-running evening directions (J4-O AM, J5-O AM, F5-O PM, F6-O PM), which take the four slots.
## Survivor anatomy

- Actor: the deciding property is how much firm braking the low sun adds on each section direction and where January's
  low sun will stand, and no file has a column for either: the survey gives two coordinates per section and the AVL log
  each pass's times, but the sun's position at a pass, the excess it produced and each cell's low-sun-free base are
  relations nothing stores, and no document defines low sun.
- Link: the signal is read by setting the sun's computed position (from the pass's clock and the city's coordinates)
  against the bearing the survey's coordinates give each direction of travel, a comparison the field's incident rate
  never asks for and no key, code or clause offers; SRM-07 names neither the sun nor a heading.
- Reflex: the field's own estimator for the deciding quantity, the near-miss exposure rate per section direction
  (firm brakes per 1,000 passes), adjusted for the visible confounders by a Poisson model by cell and month, sits at
  rung 1 and files the cells with the record's highest rates (`## Default path`).
- Back-test: the default path's month-by-cell model fits the record it is fitted on and the dashboard's line rates tie
  to the cell totals; month-over-month carry-forward is weak on the shipped seed (Spearman 0.33 between September and
  October cell rates, one cell shared between the two months' top fours; April to August against September to October
  0.66), which a careful solver reads as noisy cells, not as a moving cause: no validation record refutes the rate.
- Second use: every file the decisive step reads is in the pack for its own reason: the survey for the section ids
  and the asks' positions, the AVL log as the exposure every reader needs, the airport observations for sky cover
  (every careful reader nets it), the pick timetable for the pick's passes and SRM-07 for the WHAT; delete the glare
  step and the pack loses nothing.
- Shock: the autumn excess reads as ordinary explained movement (new operator classes, the school term from 17
  August, darker October mornings), and the golden slate is not an interval of any shipped statistic: the four golden
  cells rank 5, 22, 22 and 31 of 52 on April to October rates, 7, 7, 23 and 37 on September to October and 2, 3, 8
  and 25 on October alone.
- Pins: SRM-07 files the WHAT in the agency's own procedure (every section-direction peak, firm brakes per 1,000
  passes, the pick's weekdays at the pick's scheduled times in the normal weather, the four highest expected rates);
  no filed sentence names the sun, low sun, glare, a heading, the model, the excess, a clock rule or which cells
  January's sun reaches.
## Readability screen

| Rung | What it reads | Verdict |
|---|---|---|
| 0 first look | each cell's April to October rate | readable |
| 1 the field's rate, netted (default path) | rates by cell and month, Poisson-netted for operators, darkness, sky and school | readable |
| 2 low sun, non-directional | a low-sun term from the sun's elevation | readable |
| 3 glare named, record carried (reader d) | the glare model with each cell's autumn alignment held | readable |
| L literal execution of SRM-07 | the record's rate at the normals' sunshine and the pick's hours, no definition of low sun filed | readable |
| 4 each cell's low-sun-free base and the low-sun excess estimated from the record, carried to the pick's sun (decisive) | the record's passes with the sun's position against each direction, fitted, then the pick's passes | silent |

Rung 4 is silent: no shipped sentence names the sun, low sun or glare; the step is an estimate made from the record
(how much the low sun ahead adds, and how fast it fades off the line of travel) and carried to January's sun, and the
literal execution of every filed rule (rung L) files a wrong slate.
## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | pass | one train's traverse, one or two cars | one per car | same call on the shipped seed (asserted) | SRM-07 3.3, quoted |
| SF2 | firm brake | an FB record from the active cab | FB and EB records together | same call | SRM-07 3.4; same call asserted |
| SF3 | weekday peak | by the time the train enters the section | by the pass's midpoint or exit | same call | SRM-07 3.5; same call asserted |
| SF4 | normal weather | the normals' 68 per cent sunshine in January and February | 50, 90 or 100 per cent | same call | SRM-07 4.1 and Appendix C; same call asserted |
| SF5 | rate | per 1,000 passes | per pass | same call | SRM-07 3.7; a scale |
| SF6 | the pick's weekdays | weekdays with the weekday timetable (holidays run Sunday service) | holidays kept as weekdays | same call | the pick timetable's holiday line; same call asserted |
| SF7 | the sun's time at a pass | the pass's midpoint | its entry | same call | same call asserted |
| SF8 | sky cover for a pass | the observation in the pass's clock hour | the nearest observation; the :53 report read as the next hour's | same call | same call asserted |
| SF9 | a firm brake's pass | the car's pass whose section is nearest the recorded position | the pass by time alone | same call | same call asserted |
| SF10 | darkness (a control) | sun below the horizon | sunset at minus 0.833, minus 3, civil twilight minus 6; no darkness term | same call | same call asserted (C3) |
| SF11 | the glare response's width | a 25-degree cosine-squared taper | 15, 20, 30, 35 degrees | same call | same call asserted; the record decides (C3 over its supported forms) |
| SF12 | the glare response's elevation profile | full below 12 degrees, none from 25 | flat to 15 or 20; 8 to 20; 15 to 30 | same call | same call asserted (C3) |
| SF13 | the glare response's form | any tapering form (cosine-squared or linear, every cone 15 to 35, every elevation profile), or a flat form to 20 degrees | a flat form at 35 degrees | another call (5 of 75 cells) | the record's own fit (2dlogL 42.4 or more worse) and its offset profile (excess 0.00 at 20 to 25 degrees); the call holds across every supported form (asserted) |
| SF14 | controls | section direction, hour, weekend, darkness | none; no hour effects | same call | same call asserted |
| SF15 | the detector outage week | passes and brakes both left out | the week dropped on every section | same call | same call asserted |
| SF16 | clock | Mountain local time, MDT in the record and MST in the pick | UTC as stamped | same call once converted | SRM-07 3.5 ("Mountain local time") |
| SF17 | the candidate | one section, one direction, one weekday peak | a section pooled over directions | another call | SRM-07 3.6, quoted |
| SF18 | the basis | the pick's scheduled passes | the record's own passes | another call | SRM-07 4.1 ("at the pick's scheduled times on the pick's weekdays") |
| SF19 | ask A's month | the Mountain-time month | the UTC month (moves 4 of 7 figures) | another figure | the asking sentence ("each Mountain-time month") |
| SF20 | ask B's day | the day the card was written: the one day in the week before it was entered on which its car ran its block (the cars the yard sheets name and the car the AVL log shows taking a block over) | the MMS entered date; the day before entry; the car's last day out; the entry day | another figure (the first three each move 6 of 6) | the asking sentence ("each counted on the day it was written"); C1: every card's car ran its block on exactly one day in the week before entry and never on the entry day, so the latest such day in a 7, 14 or 30-day window, with or without the entry day, is one day (asserted) |
| SF21 | a record on a month's edge | none within 15 seconds of a month boundary | a recorder clock moving one across | same figures | asserted on the shipped rows |
| SF22 | ask B's weekday service | days the weekday timetable ran (the run sheets' Weekday schedule) | calendar weekdays (the three holidays, moves 2 of 6) | another figure | the asking sentence ("only if the weekday timetable ran that day"); the run sheets' schedule and the AVL log's start before 07:00 agree on every day (asserted) |
| SF23 | ask A's in service | SRM-07 6.2: from the car's pull-out onto a block until it pulls in (the yard sheet's car from the block's out time until the AVL log shows another vehicle on the block, that vehicle from then to the in time) | a logged AVL pass (moves 7 of 7); the yard sheet's pull-out car alone (moves 6 of 7); the block's trips | another figure, or same figures | SRM-07 6.2, quoted; the trip reading and 6.2 read on the clean truth count the golden's 707 applications (asserted); the AVL reading differs only by the 42 on passes the AVL log lost |
| SF24 | ask A's one application | the depot loop's running brake test after a release is not one; a two-car train's two records are one | the tests kept; the two records twice; another pairing window or the second car dropped | another figure, or same figures | SRM-07 6.2 and 3.4; one set under pairing within 60, 120 or 360 seconds, by dropping the second car, with or without the release log (asserted) |
| SF25 | ask B's period | April to October as a whole | per month | another figure set | the asking sentence ("over those months as a whole") |
| SF26 | ask B's line | the card's car's line | the card's block's line | same figures | every card's car and block name one line (asserted) |
## Ladder

| Rung | Route | Slate on the shipped seed | Shares with the golden |
|---|---|---|---|
| 0 | first look, each cell's April to October rate | F3-I AM, F4-O PM, J2-O AM, J3-O AM | 0 of 4 |
| 1 | default path: the field's rate netted by a Poisson model by cell and month, October's level carried | F3-I AM, F4-O PM, J2-O AM, J3-O AM | 0 of 4 |
| 2 | non-directional low sun, or sun-time by elevation bins | the low-sun-exposed cells, or the record's highest | 0 to 1 of 4 |
| 3 | per-record models in three month pools | the record's highest cells, or October's | 0 to 2 of 4 |
| 3d | glare named, each cell's observed alignment carried to January | the autumn-aligned cells | 0 of 4 |
| 3f | each cell's monthly trend carried to January (four forms) | the cells rising into October | 1 to 2 of 4 |
| L | literal executions of SRM-07 (the record's rate, at the normals, at the pick's hours, with January's dark share) | the record's highest cells | 0 to 1 of 4 |
| 4 | the golden: the sun against each direction at every pass, the response estimated, carried to the pick's passes | J4-O AM, J5-O AM, F5-O PM, F6-O PM | 4 of 4 |

Every rung below 4 is a complete pipeline that files a definite wrong slate; asserted in `generator/checks.py`. The
fourth slot (J5-O AM) clears the fifth (J3-O AM) by 37.0 per cent; across the 40 redraws the readers share at most
three slots and the default path at most two.
## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every section of track in each direction in each weekday peak of the pick | filed, SRM-07 2 and 3.6 |
| 2 Unit of account | the section-direction peak | filed, SRM-07 3.6; SF17 |
| 3 Attribution window | the pick's weekdays, 4 January to 26 February 2027 | filed, SRM-07 5.1 and the pick |
| 4 As-of dating | the record to 31 October 2026, the procedure in force | C1, one revision shipped |
| 5 Version basis | one export per system, no restatement | C1 |
| 6 Denominator | passes, one per train | filed, SRM-07 3.3 and 3.7; SF1 |
| 7 Weighting | each pass of the pick equally | filed, SRM-07 4.1 (the rate its passes see) |
| 8 Window length | the whole record fits the model | C3, the slate identical across every glare form the record supports (SF11 to SF14) |
| 9 Boundary inclusivity | the peak by entry time, 06:30 to 08:59 and 16:00 to 18:29 | filed, SRM-07 3.5; SF3 |
| 10 Rounding path | no graded rate; the slate is graded; the asks are whole numbers | C3 corridor: membership fixed across the supported glare forms; the asks' counts are integers |
| 11 Tie-break | none needed, the fourth clears the fifth by 37.0 per cent (13.2 or more in every corridor cell) | C4, asserted |
| 12 Maturity and censoring | none in the main call; ask B's cards entered after the 2 November export are not in it, and every card in it dates to one day in the week before its entry, never the entry day | C1, asserted (SF20) |
| 13 Order of operations | attach, fit, project | C1, the variants agree |
| 14 Row order | file order irrelevant | C1 |
| 15 Duplicate resolution | no FB copies (active cab only); a two-car train's two EB records one application | filed, SRM-07 3.4 and 6.2; one set under every pairing (SF24) |
| 16 Identity normalisation | car to AVL vehicle; badge to operator through the register; the car on a block from the yard sheets and the AVL log's change-offs | the systems' own keys; C1 (SF20, SF23) |
| 17 Netting against gross | none | not applicable, stated |
| 18 Dimensional units | firm brakes per 1,000 passes | filed, SRM-07 3.7 |
| 19 Code and status semantics | FB is the firm brake, EB the emergency loop, OS overspeed | filed, SRM-07 3.4 |
| 20 Integerisation | four slots | filed, SRM-07 5.1 |
| 21 Clause scope | weekdays only, both lines | filed, SRM-07 2 and 3.5 |
| 22 Forward window contents | the pick timetable's trips and running times, the normals' sunshine | shipped driver files (the pick PDF, the normals PDF) |

## Literal reader

Executed word for word, SRM-07 gives the population, outcome, window, basis and comparison and leaves the expected rate
to be formed, and it defines no low sun; every reading of a term or convention (SF1 to SF26) prints the golden slate
or the golden figures, or is ruled out by a quoted sentence or by the records (SF13, SF20, SF22, SF23), and the literal
executions that carry the record's own rates (rung L) file wrong slates, so the easy answer comes from an easy method
on the same literal estimand, never from another reading.
## Oracles

None that ties only under the golden. The dashboard's line-level monthly FB rates tie to the per-cell totals under
every reading and rank nothing; its EB column is the raw record count (copies, depot tests and brake checks included), which agrees
with the naive ask A route and is a seen-wrong control, never an arbiter. The maintenance system's entered date
is the date of its entered time on every row (both the keying), so it confirms the keying lag rather than the card's
day. The normals and the pick are drivers, not checks.
## Ask sheet

- Ask A: the streetcar's emergency brake applications in service in each Mountain-time month, April to October 2026
  (7 figures: 99, 99, 99, 113, 105, 97, 95). H18 home: the braking record beside the firm brakes the call reads, on
  rows the call never reads (EB, not FB). The WHAT is SRM-07 6.2 in the procedure's own voice: a car is in service on a
  block from the time it pulls out onto the block until it pulls in; a running brake test on the depot loop after a
  release is not an application in service; a two-car train's application, which both cars' recorders record (3.4), is
  one. No sentence says which register shows which car was on a block when. Primary devices: A2 (D7, the true key
  elsewhere: a Foundry car bad-ordered in service runs on to Foundry Loop and pulls in, and the spare that pulls out
  onto the block's next inbound trip is on no sheet, because the yard sheet keeps the pull-out car; only the AVL log
  shows the spare on the block, so the yard sheets' register misses its 14 applications, moving six of seven months);
  A3 (D4 absence: AVL onboard-unit drop-outs leave revenue trips unlogged, 42 applications on passes the AVL log lost,
  so the AVL log's register misses every month). Hazards: A4 (D5 scope: the yards' monthly brake check, an emergency
  application on a car that ran no block that day, 147 records, which every reading of in service excludes and a count
  of every record less the named exceptions keeps, moving every month); A1 (D1, a two-car train's two records, the
  trailing recorder up to 45 seconds off: dead as a device once 6.2 files the rule and the yard sheet names the second
  car, kept as texture); the release log's tests (named by 6.2); the UTC month (pinned by the asking sentence). The
  golden is the in-service map across both registers: the yard sheet's car or cars from the block's out time until the
  AVL log first shows another vehicle on the block, that vehicle from then to the in time.
- Ask B: each line's defect cards that operators wrote, each counted on the day it was written and only if the
  weekday timetable ran that day, over April to October 2026 as a whole, for brakes, for doors and for all other
  defects (6 figures: Juniper 46, 55, 171; Foundry 44, 34, 122). H18 home: the equipment side of the diagnosis (did
  brakes or doors on the cars drive the autumn rise), on the maintenance system's rows, which the call never reads.
  Counting units filed as WHAT in the asking sentence: the day written, the weekday timetable, the months as a whole;
  the MMS source "Operator card", the car's line, the MMS defect group. Primary device B1 (D8, a recorded date for the
  event date): the MMS export carries only the time each card was entered (entered_at, entered_date), the yard clerk
  keying cards the next business morning and now and then a day later; after noticing, a card is dated only by its car
  and block against the cars that ran each block, the one day in the week before entry (never the entry day) on which
  its car ran its block. The natural remedies are wrong: the entered date, the day before entry (Friday cards on
  Sunday), the car's last day out (a weekend block between). Second device B2 (D7, the same real cause as A2): every car
  that ran a block writes cards, and the spare that took a swapped Foundry block over is named on the block only by the
  AVL log, so the yard sheets' register orphans its cards and the Foundry figures move; the AVL log's register orphans a
  two-car train's trailing car's cards and the Juniper figures move. Hazard B3 (D3): the weekday timetable against
  calendar weekdays (pinned by the asking sentence; the run sheets carry each day's schedule). Realism: a clerk keying
  paper cards each morning is how a depot's maintenance system fills; the card's block box is on the form.
- Pin test: SRM-07 6.2 pins in service, the depot test and the two-car rule, and ask A's devices sit in which car was in
  service on a block when (the spare on no sheet, the passes the AVL log lost) and in the records out of service (the
  brake checks); ask B's sentence pins the day written, the weekday timetable and the months as a whole, and its devices
  sit in how a card's day is recovered and which register names the car that ran the block.
- Separation line: zero device rows in the main call's population (the call reads FB rows, the AVL passes, the survey,
  the airport file and the pick; ask A reads EB rows, the yard sheets and the release log, ask B the MMS export, the
  yard sheets and the run sheets), asserted in `checks.py`; SRM-07 carries ask A's definition (6.2), the WHAT, and none
  of its devices' organs. The brake checks join the export after every draw on the shared stream, so the main call's
  records are byte-identical (asserted by G, the slate and the chart's bytes).
- Pair ceiling: 32.7 (one response on the call keeping the crackers' ask figures, the other off it with the same ask
  handling); both on the call 49.2; at the full includer's keep the pair is 45.4 and both on 61.9.
- Mirror leakage: 0.0 per cent of the ask weight.
- Full includer: keeps 30.8 per cent of all ask figures at its best route (under two fifths). It reads every file and
  acts on every stated fact against one register per question; a car no register names is an orphan and is set aside:

| Full includer route | Ask A | Ask B |
|---|---|---|
| full includer, yard (the yard sheet's car from pull-out to pull-in, release log, second car dropped; cards by the yard sheets) | 1 of 7 | 3 of 6 |
| full includer, AVL (AVL passes; cards by the AVL log) | 0 of 7 | 3 of 6 |
| full includer, yard paired (pairs within a minute; cards by the yard sheets) | 1 of 7 | 3 of 6 |
| full includer, signature (the Loop's walking-pace signature, pairs within a minute; each card on its car's last day out) | 0 of 7 | 0 of 6 |

- Stress rows (not the gate, the reconstructions the golden makes): the in-service map across the yard sheets and the
  AVL log for A with the yard sheets for B, 10 of 13 (76.9 per cent); the yard sheets for A with B's undated cards put
  on the business day before entry, 7 of 13 (53.8 per cent); the golden's handling, 13 of 13.
- Every ask figure is a whole number, 0.5 of a unit from its rounding edges; the tightest is any of them (all at 0.5).
- Measured by: generator/ceiling.py on the cut pack (shares no code with the generator; its own golden handling is
  asserted equal to figures.json).

| Ask row (cracker sheet) | Ask A kept | Ask B kept | Verdict |
|---|---|---|---|
| cracker (AVL passes; each card on the day before it was entered) | 0 of 7 | 0 of 6 | miss |
| second cracker (yard sheets, release log, pairs in a minute; each card on its car's last day out) | 1 of 7 | 0 of 6 | miss |
| no-repair (every EB record, UTC month; each card on its entered date, calendar weekdays) | 0 of 7 | 0 of 6 | miss |
| blind (every record but the named exceptions; each card on the business day before entry) | 0 of 7 | 0 of 6 | miss |
| mirror (the observed-rate rung; the cracker's ask handling) | 0 of 7 | 0 of 6 | miss |
## Realism pass (stage 3)

Texture only, each change on its own random stream or on the same draws, so the realization is unchanged: the slate,
ask A's 14 figures, ask B's 6 and the slot plan's marks are the same; the fitted G moved from 2.292 to 2.296 and the
chart's rates by hundredths, from the AVL log's actual running. Asserted in `checks.py` (`realism 1` to `realism 8`,
the three-rules block R1 to R3c and the write-up's steps executed as written): 155 of 155 at stage 3, 167 of 167 with
the block assertions (`## Block repair`).
- The AVL log carried the timetable (one run time per section direction, trips on the exact headway, entry seconds on 32
  values). It carries the actual running now: trips leave late, never early (a gamma lateness, mean near 45 seconds,
  now and then a disruption of minutes), street run times vary with signal stops; the recorder's event times and the
  run sheets' revenue hours follow it, and the hazard truth stays on the schedule.
- The January pick printed one running time for both directions of every section; its revised times differ by a few
  seconds by direction, the forward truth and the PDF read from one table.
- Ids: the recorder's event numbers and the MMS work orders stepped by one, and the depot's repair work orders were
  random and out of time order. The recorder numbers every event it logs and the export carries FB, EB and OS only; the
  MMS rows and the depot repairs share one agency series with gaps, in the order opened. The AVL trip key is the
  scheduling system's (line, scheduled departure, direction), not a counter from 00000.
- Operator numbers rose along each day's runs (the rotation over the roster in number order). The same numbers now
  follow the order operators qualified; who drove which pass is unchanged.
- The dashboard was cut from the clean truth: identical trip and pass counts for both lines, the same in April as in
  June, and a November row of 2 trips at an FB rate of 2750. It is now the AVL log as shipped by service month beside
  the recorder's counts by UTC month, April to October, with Excel's own application properties, created at the first
  month-end download and modified at the last.
- The three PDFs carried reportlab's invariant stamp (1 January 2000 on all three) and its comment lines; each carries
  its office's own creation and modification stamps now, at equal length, with the comment lines blank. SRM-07 is
  revision 4, effective 1 October 2026: revision 3 of September 2025 cited the April 2026 commissioning and the January
  2027 pick.
- The MMS status column read Closed on every row, cards keyed that morning included: dropped. The airport's temperature
  jumped hour to hour and its visibility took two values: the same draws, filtered and binned. The bundle's export
  stamp now follows the MMS extract of 11:00 on 2 November. The pedestrian counters' codes no longer run in alphabetical
  order. Decelerations thin out above the firm brake's 1.3 trigger and centre near 2.75 for an emergency application,
  from the same draws.
- Goldens: the slot plan carries the line, the peak window and the order's 10 mph limit (SRM-07 3.5 and 5.2); the chart
  takes the finding as its title, states its basis and sources, and fits its frame.
## Block repair

The defect (`## Tried and rejected`, a2 stage 3), measured on the stage-3 pack with scratchpad
`t210/a2/blocks/audit_blocks.py`: every Foundry block ran one direction all day (46,625 of 46,625 trip-to-trip
transitions repeated a direction). The Juniper's blocks alternated only because nine is odd, and both lines shared the
other faults: the early run handed over at 14:00 in the middle of a trip (11 trips' recorder events carried two
operators), J01 uncoupled and J02 coupled its trailing car at Mesa Park, 34 in-service swaps changed car inside a trip,
and all seventeen blocks ran on Saturdays and Sundays with layovers near an hour.

Fixed in the world (`simulate.blocking`, `records.realised` and the swaps in `records.records`):
- The scheduling department's blocks for each line and day type. Each departure takes the car that has laid over
  longest once its scheduled layover has run (the Juniper 12 minutes at Mesa Park and 19 at Union Yard, the Foundry 9
  at each end); a pull-out from the yard at the outer end (Union Yard; the Foundry depot at Foundry Loop) covers a
  departure no car is ready for, by deadhead where the trip leaves the inner end; a car not needed (the cars ahead of
  it already cover the first departure it could take) pulls in, from the inner end after a deadhead, as do the last
  arrivals. Weekdays run 9 Juniper and 8 Foundry
  blocks (two of each pull in after the 19:00 change to 10 minutes), Saturdays 7 and 6, Sundays and holidays 5 and 4;
  scheduled layovers run 9.9 to 27.6 minutes.
- J01 and J02 are the two Juniper blocks that come into Union Yard just before each strengthening window and leave it
  again after, so each window opens inbound out of Union Yard and closes outbound into it, and the pick's sentence on
  trips leaving 06:30 to 09:29 and 15:30 to 18:44 holds as written; trailing cars stand on the yard sheet only on
  weekday-timetable days.
- Each block's early run hands over to the late run at the outer end, in the layover nearest the middle of the block's
  day: each run sheet row's revenue hours cover whole trips, and no trip's recorder events carry two operators.
- A bad-ordered Foundry car runs on to Foundry Loop and pulls in, and the spare pulls out onto the block's next inbound
  trip: every car change on a block falls between an outbound trip and the next inbound one, and every release follows
  the car's last pass that day.
- A car coming in late leaves on its block's next trip no sooner than two minutes after (the same draws, the knock-on
  carried).

Asserted in `checks.py` as `realism 9` (12 assertions on the clean truth and on `target/`): 167 of 167.

The truth is untouched: the blocking draws nothing, so the section noise is byte-identical under both generators for
every seed and each seed's truth slate stands. The realization moved with every operator's passes and every car's
trips: at 21019 the separation fell to 9.5 per cent clean and 15.5 from `target/`, the second cracker kept 4 of 14 and
the full includer 45 per cent. Reselected on the corrected redraws (`## Draw`): 34 of 40 golden equal to the truth, 33
of those with no reader over two slots, 23 cut and measured (20 at 15 per cent or more from `target/`), four holding
every ask proof (21015, 21030, 21033 and 21040), and only 21030's corridor clears 10 per cent in every cell (13.2,
against 9.0, 4.1 and 4.7). The call holds.

Moved figures, each re-measured on 21030; every moved `figures.json` key is named by `--allow` (131 keys, the list in
scratchpad `t210/a2/blocks/allow_keys.txt`):
- Unchanged: the slate, every Final Recommendation and Critical Components number (the four bearings, the pick's 38
  weekdays and 68 per cent sunshine), the slot plan's marks, the prompt, the card's driver.
- `ask_b.Foundry.Doors`, 38 to 46: an ask figure equal to the pick's 38 weekdays by coincidence, so freeze.py keys it as
  a main-call figure; the realization moved it.
- The other 13 ask A figures that moved (Juniper June stays 46) and 5 ask B figures (block 4): the realization moved.
- Step 1's 11,778 FB records and 94 per cent to 11,955 and 95; step 3's G 2.3 to 2.5 (`G_hat` 2.296 to 2.498); the
  fourth and fifth rates and the separation 24.1 to 37.0 per cent, the fifth F3-O PM to J3-O AM; the 52 expected and 52
  observed rates (the chart's bars).
- The stump sentence, the card's stump and analyst test, the default path's `Ends on:` and the ladder's slates: the
  default path now files F3-I AM, F4-O PM, J2-O AM and J3-O AM (the record's four highest cells, east-running mornings
  and a west-running evening, two of which fell from April to August into September and October), where 21019 filed
  F3-I AM, F4-I AM, J1-O AM and J2-O AM, so the stump sentence no longer calls them the morning cells that rose this
  autumn. The card's concrete driver sentence drops "which were quiet all season": one golden cell ranks fifth of 52
  on April to October rates at 21030.
- `figures.json` gains `glare_factor` and `pick_dates`, the write-up's glare formula and the pick's dates (read from
  the pick PDF), which `figures_check.py` had matched only by coincidence against two observed rates.

`freeze.py check task210 --mode determinism --allow <the 131 keys>`: exit 1, 6 items, the stump sentence, the card's
stump, the ladder, the default path and both ask blocks of Deliverable Answers (a determinism repair moves no graded
figure; this repair moves the realization). `--mode rubric` with the same keys: exit 1, 4 items, the stump sentence, the
card's stump, the ladder and the default path; 132 ask-side figures moved (the 130 non-main keys and the two new ones).
Neither mode's contract matches a world repair that reselects the seed, so both outputs stand as recorded
(scratchpad `t210/a2/blocks/freeze_determinism.txt`, `freeze_rubric.txt`), and nothing frozen on the main call moved.
## Ask repair (stage 4 round 1)

The round-1 judge read the main call as forced and correct (Gates F high, G forecasting and analytical_non_defect, H
analytical) and failed Gates C and E on the asks alone: no file defined revenue service (read against the AVL log's
passes ask A was 666, against the yard sheets' block assignment the golden's 707, all 14 cells different), and ask B
rested on an unstated re-dating (the MMS `reported` column read as the writing day gave other figures; 68 cards had the
keyed day as a second candidate; the three weekday holidays and per month against the period were open). The leak
reader was clean on the main call and flagged the same ask terms. An ask-layer repair, no architecture spent; the call,
the stump sentence, the ladder, the default path, the chart and the slot plan are frozen (`freeze.py --mode rubric`,
below).

Fixed in the world and filed as WHAT, never the handling:
- SRM-07 6.2, in the procedure's voice: the Rail Safety Office reports the streetcar's emergency brake applications in
  service by month; a car is in service on a block from the time it pulls out onto the block until it pulls in; a
  running brake test on the depot loop after a release is not one; a two-car train's application is one. The yard
  sheets carry each block's out and in times (`simulate` untouched; the times from the realised first and last trips on
  their own stream). Every application lies on one of its block's trips; the trip reading, the literal reading of 6.2 on
  the clean truth (each car from its own pull-out to its own pull-in) and the golden's in-service map from `target/`
  count the same 707 applications, and the AVL-passes-only reading differs only by the 42 on passes the AVL log lost
  (asserted, SF23 and SF24).
- Ask A asked of the streetcar by Mountain-time month (7 figures) rather than of each line (14): `## Tried and
  rejected`. The yards' monthly brake check (147 records on cars that ran no block that day) joins the export after
  every draw on the shared stream; the trailing recorder's clock is the same draws scaled to 45 seconds.
- Ask B: the keying day is never a candidate (a card is written only where its car ran its block on exactly one day in
  the week before entry and not on the entry day, under the cars that ran each block, the spare that took a swapped
  block over included), one card per defect per car per day, and every car that ran a block writes cards (the
  bad-ordered car and the spare now included). The MMS export's `created` and `reported` are `entered_at` and
  `entered_date`, so no column claims the writing day. The run sheets carry each day's schedule (Weekday, Saturday,
  Sunday; the three holidays Sunday). The asking sentence files the day written, the weekday timetable and the months
  as a whole; the narrow and broad readings of each card's day (7, 14 or 30 days, with or without the entry day) are
  one set (asserted, SF20, SF22, SF25, SF26).

Moved, each re-derived from the corrected world on seed 21030 (`figures.json`):
- Ask A, 14 per-line figures to 7 monthly figures (99, 99, 99, 113, 105, 97, 95; the three 99s are the record's own
  counts, equal to the flag truth): `ask_a.Juniper 04` to `ask_a.Juniper 10` and `ask_a.Foundry 04` to `ask_a.Foundry
  10` leave, `ask_a.04` to `ask_a.10` arrive. The re-site and the filed WHAT move them.
- Ask B, 6 figures (Juniper 55, 56, 153 to 46, 55, 171; Foundry 37, 46, 139 to 44, 34, 122): the world fix (the entry
  day ruled out, one card per defect per car per day, the swapped blocks' cars writing cards) redraws the cards on
  their own stream.
- Unchanged: the slate, G 2.498, the separation 37.0 per cent (33.8 in `verify.py`), every Final Recommendation and
  Critical Components number, the 52 expected and observed rates, `slot_plan_jan_feb_2027.csv` and `braking_shift.png`
  byte for byte, the stump sentence, the card's stump and driver, the ladder and the default path.

`freeze.py check task210 --mode rubric --allow <the 20 moved ask keys>`: exit 0, PASS (the main call, the stump and every
frozen figure unchanged; 27 ask figures moved). `--mode determinism` with the same keys: exit 1, 4 items, the Deliverable
Answers blocks of both asks (a determinism repair moves no graded figure; this repair re-derives the asks from a
corrected world and re-sites ask A), so its contract does not match the repair and both outputs stand as recorded
(scratchpad `t210/a2/fix/freeze_determinism.txt`, `freeze_rubric.txt`). The 20 keys: `ask_a.Juniper 04` to
`ask_a.Juniper 10`, `ask_a.Foundry 04` to `ask_a.Foundry 10`, `ask_b.Juniper.Brakes`, `ask_b.Juniper.Doors`,
`ask_b.Juniper.All other`, `ask_b.Foundry.Brakes`, `ask_b.Foundry.Doors`, `ask_b.Foundry.All other`.
## Leak sweep rulings

`leak.py --asof 2026-11-02`: REVIEW, no LEAK, sweeps 1, 2, 5, 7, 8, 10 and 11 clean. Each REVIEW line, harmless:
- Sweep 3, SRM-07 names the Juniper Line beside decision words: its scope sentence names both lines as the population.
- Sweep 3, the pick names the Juniper Line beside numbers: its running-time table lists every section of both lines.
- Sweep 3, the pick carries 22 of the call's 30 words: the call names four sections by their stops and the pick's dates,
  and the pick names every section, every stop and its own dates alike.
- Sweep 4, SRM-07 holds seven stump terms (record, passes, highest, weekdays, recorder, expected and the normals):
  the procedure's filed WHAT (the recorder's codes and the record since 1 April, passes as the denominator, the pick's
  weekdays, the expected rate in the normals' weather, the four highest expected rates, and 6.2's applications in
  service, which each car's recorder records); it names no sun, glare, bearing or excess (asserted). The term list is
  re-read from the design note at every run; the stage-4 ask repair added 6.2 and no stump term.
- Sweep 6, the pick names every candidate beside numbers: scheduled running times in network order, ranking nothing.
- Sweep 6, the survey names every candidate beside numbers: coordinates and lengths in network order (the raw material
  R1 asserts), ranking nothing.
- Sweep 9, the school calendar's 154 dates after 2 November: a district publishes its school year ahead of it.
## Tried and rejected

- 2026-11-04 (a2 stage 4 fix), ask A's WHAT filed as the brief's example, an application made while the car was running
  one of its block's trips: a trip reading makes the AVL log, its gaps filled from the yard sheets, the careful route,
  and that route counts the golden in every cell (the spare is a logged vehicle and the Foundry carries no other
  device), so the WHAT is filed as SRM-07 6.2's pull-out onto a block to pull-in, whose natural register is the yard
  sheets, which keep the pull-out car.
- 2026-11-04 (a2 stage 4 fix), ask A by line once 6.2 filed the two-car rule: the Juniper half's only device was the
  trailing car's copy, and with the yard sheet naming the second car, dropping its records is exact, so the yard full
  includer kept 8 of 14 and the layer 11 of 20 (55 per cent); re-sited onto the streetcar's monthly totals, where the
  Foundry's in-service swap (the spare on no sheet) moves six of seven months.
- 2026-11-04 (a2 stage 4 fix), the monthly totals with the trailing recorder up to 3.5 minutes off: the copies a
  one-minute pairing leaves unpaired offset the spare's applications in April, June and September (a subset of
  mishandlings composing back in the bin), so the second cracker kept 3 of 7 and the yard paired full includer 46 per
  cent; the trailing clock is the same draws scaled to 45 seconds, and every pairing window from one to six minutes
  counts one set.
- 2026-11-04 (a2 stage 4 fix), every EB record less the named exceptions (the release log's tests, the second car's
  records) counted the golden in all seven months, nothing out of service being left in the export: the yards' monthly
  brake check on cars out of service that day is added (147 records), which every reading of in service excludes.
- 2026-11-04 (a2 stage 4 fix), the brake checks first joined the export before the per-record draws on the shared
  stream, which shifted the AVL drop-outs drawn after them and moved G from 2.498 to 2.385: they now join after every
  shared draw, each field from their own stream, and the main call is byte-identical.
- 2026-11-04 (a2 stage 4 fix), ask B with the holidays filed and nothing else: the yard-sheet dater kept 6 of 6 once the
  calendar-weekday reading was ruled out, so every car that ran a block writes cards, the swapped block's spare
  included, which the yard sheets never name on its block; a dater that falls back on the business day before entry for
  the cards it cannot date recovers them (swaps fall on weekdays), recorded as a stress row (53.8 per cent), not a full
  includer under the house standard (a car no register names is set aside).
- 2026-11-04 (a2 stage 3), the Foundry blocks alternated to fix their one-way working (each Foundry block runs one
  direction all day, the trip index modulo eight, which no car or operator could work): the change moves every
  operator's passes and so the whole realization, and at seed 21019 the slate holds on the clean truth but the
  separation falls from 27.3 to 17.2 per cent, short of what the corridor's 10 per cent floor needs from `target/`;
  repaired at the stage-4 hand-off as a whole blocking, not an alternation alone (`## Block repair`): every block on
  both lines out and back from its pull-out at the outer end, layovers at the termini, pull-ins there, reliefs there
  between trips, J01 and J02 coupling in Union Yard, bad-ordered cars swapped at Foundry Loop and fewer blocks at
  weekends; on the full blocking 21019's separation fell to 9.5 per cent clean and its second cracker kept 4 of 14, so
  the shipped seed was reselected over 40 corrected redraws to 21030, the one that holds every proof.
- 2026-11-04 (a2 resume), the generator's sun: `solar.py` never wrapped the hour angle, so for UTC hours 00 to 06
  (Mountain evenings after 18:00 MDT and 17:00 MST) the sun's azimuth was mirrored into the east (20 June at 20:00 MDT
  it gave 62.7 degrees against 297.2); the truth put summer-evening glare on east-heading passes and the golden only
  reproduced with the same bug (an independent Almanac sun fitted a glare multiplier of zero). Fixed; every screen
  re-measured on the corrected world; seed 21009's separation fell to 3.1 per cent and 21006's ask A kept 5 of 14 for
  the yard-sheet cracker, so the shipped seed is 21019, selected on the corrected screens and the ceiling.
- 2026-11-04 (a2 resume), SRM-07 3.8 (low sun, within 25 degrees either side and below 25 degrees, worst below 12)
  and 3.9 (darkness): 3.8 named what the decisive step recognises (the fork-is-the-stump test) and executing it alone
  filed three of four; both are removed, and the glare form is closed by the record (SF11 to SF13).
- 2026-11-04 (a2 resume), the corridor as first instructed (every cone 15 to 35, every elevation profile, linear and
  flat shapes): a flat response from 25 degrees out leaves the slate (15 of 75 cells in the buggy-sun world, 10 of 75 on
  the corrected seed 21019), so the corridor is every tapering form and every flat form to 20 degrees (60 cells, all on
  the slate), and the flat forms from 25 degrees are refuted by the record's offset profile and fit (45.5 or more worse).
- 2026-11-04 (a2 resume), ask B on the May and August classes' overspeeds in their first 30 days in revenue service:
  with the run sheet's duty column and the card register filed, the cracker kept 6 of 6 (rule application); redrawn on
  the maintenance system's defect cards, keyed the next business morning (D8) and dated only by their car and block
  against the yard sheets.
- 2026-11-04 (a2 resume), ask B's weekday service read from the AVL log's trips per day (90 per cent of the busiest
  day): drop-outs put four weekdays under the line and moved four figures; weekday service is a Monday to Friday whose
  service starts before 07:00 (the Sunday timetable starts at 07:00), exact on all 150 days.
- 2026-11-04 (a2 resume), ask B's first card rates: Juniper doors moved one card under the cracker (few Friday cards
  fell in it); the rates were raised by half so every figure carries its Friday cards.
- 2026-11-04 (a2), the low-sun geometry left unfiled and carried as a C3 corridor (cones 15 to 35, bands, shapes all
  giving the golden slate): the coordinator's lesson from task211 (a withheld practice recovered from the records is a
  planted step at Gate H) binds every input the projection needs, so SRM-07 now files low sun (3.8) and darkness (3.9)
  as plain fact; measured, executing the filed facts alone (the pick's low-sun exposure at the normals) files J4, J5 and
  J6 outbound AM with F6 outbound PM, three of four, and the golden needs each cell's base and the excess estimated
  from the record.
- 2026-11-04 (a2), asks resting on unfiled conventions (two-car copies, depot running tests, ride-along rows, the yard
  sheet's meaning): lesson 2 files each in the producing system's own form (SRM-07 3.4's codes and what each car
  records, the release log's check column, the yard's pull-out cars, the run sheet's duty column); ask A still holds
  (the cracker keeps 1 of 14), ask B became rule application and the cracker keeps 6 of 6, so ask B is redrawn.
- 2026-11-04 (a2), competing causes tested by redrawing the world without them: a redraw changes the Poisson draws, so
  the school-free redraw moved the slate by sampling noise alone; the test now thins or tops up the same realization.

- 2026-11-04, seed AD33's world itself (a data-centre battery's January FCR-D offer): undrawable on this objective
  while task402 holds energy-systems-utilities/grid-reliability-outage-analysis in the window (`ban.subdomain`); its
  mechanism also sat near task197 (a unit's frequency response during scheduled ramps) and task125 (occasions a
  forward schedule moves).
- 2026-11-04, a nuclear site's fence-line gamma monitors at go-live, the alarm level set against rain-induced
  radon-progeny washout (prototype `proto_gamma.py`, `screens_gamma.py`, seeds 1 to 5, two climates): the golden
  needs a fitted dynamic washout model with call-out merging; event regressions with an antecedent dry-time term
  land 6 to 12 nSv/h off it and the first look sometimes lands near it, so screens 1 and 2 fail.
- 2026-11-04, occupational blood lead at a secondary lead smelter (January furnace shifts under the action level):
  its decisive state is a shared upstream resource (task181) or each unit's lagged response (task182), and a
  monthly AR(1) careful route sits close to the kinetic golden.
- 2026-11-04, a data centre's UPS battery strings on thermal age and a device fleet failing on uptime since the last
  reset: both are task139's wear-clock insight and task132's renewal, in other nouns.
- 2026-11-04, hydropeaking under a filed rating curve (downstream stage ramps at winter base flow): task156's
  response scaled by a level read from a separate record.
- 2026-11-04, darkness-relative crime hours, susceptible depletion, backlog draining, road salt, build-up and
  wash-off, immortal time, an extremal index and tide aliasing: each already screened dead in another slot's note
  (`guard.py slots`: task182 arch 8, task178 and task202, task174, task165, task121, task122, task178 and task194,
  task249).
- 2026-11-04, world 1 (a north crest road in view, a west crest road behind the bund, cycle 3.6): the face fixed
  the route, so a reader classifying days by face from the shift report or the blast register reached the golden;
  redrawn so north loads split between Haul road 2 and the in-pit stockpile ramp, the tip set by the primary's demand.
- 2026-11-04, the golden as Haul road 2 against every other movement lumped: the lumped coefficient carries the
  north stockpile movements and drifts with the face mix (0.2 to 0.5 of a bin above the route fit); the golden fits
  one coefficient per route (face and tip).
- 2026-11-04, six or seven trucks every day: total movements nearly constant, so the intercept and the other routes'
  energy were confounded and an hour-effects fit fell 2.4 dB below the pooled one (a negative coefficient); truck
  availability now varies (three to seven, half-day services, rain stand-downs logged in the shift report).
- 2026-11-04, wind at 1.6 to 2.1 dB on the haul: a chance correlation of wind with north days moved the wind-adjusted
  fit 0.7 of a bin; wind now 0.7 to 1.0 dB and the weather file stays a distractor.
- 2026-11-04, BS 5228 calibrated hour by hour on route-resolved predictions lands the golden: it takes the decisive
  step (each movement's route state), so it is a family member; the coordinator's pooled-record acoustician is the
  ratio of measured to predicted energy over the pilot, and lands 1.
- 2026-11-04, three trucks on the north bench: the operations' specific level topped 45 dB in 6 per cent of pilot
  hours (a visible breach of condition 17); the north bench now takes one or two.
- 2026-11-04, haulage levels on the dial graded to 0.1 dB: the golden family spreads about 0.2 dB, and a mid-bin call
  puts the call's own level near 43.5 dB, so no rounding holds every setting; the dial files each setting's verdict
  and the levels show only on the chart.
- 2026-11-04, ask devices a full includer remedies on notice (unpaired PLC starts, one-to-one re-keyed tickets, the
  order book's product, unordered buckets after the stop): re-sited into reconstructions (stops logged at boot,
  summed Monday tickets, gate changes, lunch and run-down re-handling while the primary runs).
- 2026-11-04, stage 4 round 1, the residual left unfiled: NMP 5.1 names two contributors, so the judge took the
  plant plus the night ambient as the baseline and filed 2 trucks against the free intercept's 3 (SEND_BACK, Gate C);
  NMP 5.2 now files the residual measured with the site stopped in the haul window.
- 2026-11-04, stage 4 round 1, the Phase 4 road as Haul road 2 reflected across the diagonal and scaled 1.16, its
  last 153 m classed as screened by the plant while in the open: its stretch at road level 60 m or higher was 2.1 times
  Haul road 2's on the survey, and "the same ground at the same distances" was not literally true; the site was
  re-laid so the road is Haul road 2's counterpart about the hopper's bearing.
- 2026-11-04, fix pass, the hopper on the old bearing with the road mirrored about it: the mirror falls inside the
  existing pit; the hopper moved onto a bearing between the pit and the extension.
- 2026-11-04, fix pass, a 68 m bund across the compound's village side: it shadowed Haul road 2's last 52 m, cut its
  energy 1.4 dB and made Haul road 1 louder; the bund is 20 m.
- 2026-11-04, fix pass, Haul road 2 surveyed from the north face and the Phase 4 road from its ramp top with no bench
  crest in any file: a line-of-sight reader counts the ramps differently (0.2 to 0.3 dB, and 2 to 3 dB with the
  Phase 4 ramp in the alignment); Haul road 2 starts at the pit crest, the North face ramp is surveyed apart, and the
  scheme files the bench crest and its access ramp.
- 2026-11-04, fix pass, a 108 dB declaration on the register (the Bell B40E): BS 5228 hard ground from it landed 2.99
  trucks; the declarations are 109, 110 and 111 dB.
- 2026-11-04, fix pass, the physics drawn wide per redraw (sound power within 0.4 dB, ground 0.3 dB, speeds 1 km/h)
  with wind at 0.7 to 1.0 dB: the free intercept landed 3 in 20 of 24 redraws (round 1's own screens); the ranges
  narrowed and wind halved, now 24 of 24.
- 2026-11-04, fix pass, each route's passages stamped at the haul's midpoint, a four-minute hopper queue and tips on
  the next whole-minute fix: the free intercept carried 0.2 dB of spilled haul energy, and the quarter-hour fit sat
  0.31 above the hourly one (3.87); passages timed on each road, the hopper wait moved to the face and a fix logged
  on the payload change, the gap is 0.11 (3.64).
- 2026-11-04, fix pass, sales streams 905 and 963: a week total on a rounding edge (5,005.5 t), then with orders drawn
  naturally a portable day with no multi-run ticket, so the one-to-one route kept a week; stream 1144 (every sales
  figure 0.21 of a bin or more from an edge, every wrong route 2.7 t or more off).
- 2026-11-04, fix pass, the guard against two keyed tickets summing alike nudging one run: it never ended on twin runs
  of equal weight (redraw 21053); it now turns about the ticket's runs.
- 2026-11-04, fix pass, payload stream 606 on the new haul: a tonnes-per-load cell 0.05 of a bin from an edge;
  stream 647 (every plant figure 0.159 of a bin or more).
- 2026-11-04, architecture 1 (Ravensby Quarry, the Phase 4 haul allocation under the village noise share) spent at stage 4
  round 2: the judge returned DETERMINISTIC with a solution-only FIX_NOW, but its blind derivation, written before the graded
  blocks, filed the golden 3 trucks by fitting MP1's haulage energy per face-by-tip route from the telematics against the survey
  and reading the Phase 4 road off the survey as Haul road 2's twin. The round-1 closure of the exposure fork (re-laying the
  site so the forward road mirrors an observed one) made the transfer exact and visible: Gate F paid for what Gate C gained.
  Re-root in another world.
- 2026-11-04, architecture 2 draw, seed AD33's own world re-probed after task211 registered: task402 left the window, so
  `ban.subdomain` cleared (the probe card's remaining BLOCKs were axis values drawn for the probe), but every driver of
  the battery's night activation energy a pack could carry (each boundary's schedule ramp, the operator's disturbance
  log, the system's reserve volume) is one pairwise join from the pilot log plus a per-cell rate, the per-record
  reader's own route, so it fails screen 4 before a harness.
- 2026-11-04, architecture 2 draw, screened in other slots' notes and set aside before a harness: colonisation pressure
  on a ward (task177, task181), the previous room occupant (task252 architecture 1's carryover in other nouns), crew
  familiarity (task178's familiarity curve died on lever and determinacy), sequence priming and look-alike selection
  (task399), screener vigilance and prevalence (task171, task177), rail signals passed at danger per red approach
  (task180, task181, task191, task398), mortality displacement (task173, task177).
- 2026-11-04, architecture 2 draw, low-sun glare on a UK tram network at 53.4 N with the worst clock hour as the estimand
  (`proto/glare_screen.py`): winter sunshine near 0.22 of daylight leaves the best-aligned south-facing hour at about
  1.9 times base, under the evening peak's darkness level, so the glare could not carry the call.
- 2026-11-04, architecture 2 draw, the same glare in a sunny Mountain-time city with emergency braking near 3 per 1,000
  passes, peak passes only (`proto/g2.py`, `g3.py`, `g4.py`): about 7 events per section-direction peak over the
  record, so the golden's own slate moved between 3 and 25 cells across seeds and its threshold sat inside the noise;
  repaired by the firm-braking flag (20 per 1,000 street passes), every pass of the record in the fit and a slate
  capped at four (`proto/g5.py`, `g6.py`, `screens_a2.py`).
