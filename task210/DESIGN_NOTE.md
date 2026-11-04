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
the yard's pull-out sheets, the Foundry depot's release log, the run sheets (duty and revenue hours), the operator
roster, the badge card register, SRM-07 (PDF), the January pick timetable (PDF), the station normals (PDF), the rail
operations dashboard (workbook), and four distractors named only in `metadata.json` (pedestrian counters, the arena's
events, track maintenance, the school calendar). Seventeen files, five formats, the AVL log about 620,000 rows.

**Task400 setting line.** task400 is an iron-ore mine's haul-truck collision alerts after a firmware change, read from
vehicle event recorders and braking-type events: its driver is a device change's effect on alert counts; here no device
changes, and the driver is an external light source computed from a clock and a bearing that re-sorts which directions
of travel carry the excess in the forward window.

**Gate G.** No shipped artifact ranks or sorts section-direction cells or flags a top set: the dashboard is monthly
and line-level, unsorted, with FB, EB and OS counts and the line's FB rate as data; no file lists cells with a rate.

**The five go/no-go screens, on the real generator** (`scratchpad t210/a2/proto/screens_gen.py`, 20 redraws, seeds
21001 to 21020, `screens_gen_run.txt`; the shipped seed's numbers asserted in `generator/checks.py`):

1. **Realistic levels and the lever.** Sun position from NOAA's General Solar Position Calculations; January and
   February sunshine 68 per cent of possible (station normals); glare raises crash risk on approaches facing a low sun
   (Mitra 2014, Safety Science 70, 246 to 254), glare situations predicted from alignment and sun position (Jurado-Pina
   and Pardillo Mayora 2009, Transportation Research Record 2120, 12 to 17); darkness raises pedestrian risk severalfold
   (Sullivan and Flannagan 2002, Accident Analysis and Prevention 34, 487 to 498). World-set: firm braking 20 per 1,000
   street passes and 8 on reserved track; the full-alignment multiplier 3.2 under full sun, a modelling choice at the
   upper end of the published excesses. The slate holds across full-alignment multipliers 2.2 to 4.5 and street bases
   12 to 30 per 1,000 on the shipped realization (asserted). Lever: the golden recovers the true slate in 17 of 20
   redraws; at the shipped seed (21009) the fourth slot clears the fifth by 21.0 per cent on the clean truth and 15.0
   per cent from `target/`.
2. **The golden's own method holds the call.** Fifteen generator specifications agree in 11 of 20 redraws, every redraw
   with a separation of 10 per cent or more; at the shipped seed twenty readings from `target/` (sun time, sky join,
   brake assignment, darkness, cone 15 to 35, four elevation profiles, linear and box shapes, no controls, no hour
   effects) print the same slate, so only slot membership is graded (rates spread 27.8 to 40.8).
3. **The first look lands wrong**: 20 of 20, at most two cells shared.
4. **The careful readers land wrong**, 20 of 20 each: (a) field-decomposing, at most two shared; (b) constructing (a
   non-directional low-sun term; sun-time by elevation bins), at most two and one; (c) per-record in three month pools,
   at most two, one and three; (d) the glare-naming reader that carries the record forward (the observed September to
   October alignment, or the fitted model with each cell's April to October or September to October alignment held),
   at most one shared; (f) each cell's monthly trend carried to January (four forms), at most three shared. Reader (e)
   is the golden; its inputs are plain facts in the pack: the location and each section's bearing (the survey's
   coordinates), what low sun and darkness are (SRM-07 3.8 and 3.9), the January peak hours (SRM-07 3.5 and the pick
   timetable), the clock (the timetable on local time, the recorder's stamps labelled UTC). Executing those facts alone
   on the pick files three of four (J6 outbound AM, reserved track, in place of F5 outbound PM): the golden needs each
   cell's base and the low-sun excess estimated from the record.
5. **Literal execution** of SRM-07's WHAT, five operationalisations: 20 of 20 wrong, at most three shared.

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
  headways and running times. None is placed to be caught and none decides the call (each asserted inert in checks.py).
- Layer 2: estimation that fits the data (`estimation_fit`): the excess braking is attributed to the low sun ahead of
  each direction of travel, fitted on every pass of the record, and carried to the pick's passes under January's and
  February's sun; the choice that flips the call is reading the excess as a property of the sun's position rather than
  of the cell where it was measured.
- Decisive step: the sun's position at every pass, computed from the clock and the city's latitude and longitude, set
  against each section direction's line from the survey, with the excess it produced fitted on the record and carried
  to the January and February peaks.
- Not semantics: reading every field, code, clock and unit correctly (the UTC stamps, the coordinates, SRM-07's
  definitions of low sun and darkness, the sky codes) still leaves each cell's measured rate, which carries the autumn
  sun's excess, and executing the filed definitions on the pick alone files J6 outbound AM in place of F5 outbound PM.
- Not rule application: SRM-07 files the population, outcome, window, basis and comparison and nothing about how the
  expected rate is formed, so executing it leaves the projection open; the enumerated family (rate tables, the
  field-decomposing and per-record models, two sun-elevation constructions, five literal executions) files 0 of 24
  golden slates and shares at most two of four cells, while the standing family (nine glare and model specifications)
  agrees in 18 of 24 redraws and at the shipping candidate, and what rules the enumerated family out is loud on the
  record: the excess sits only on sunny passes, only in one direction of a section, and only while the sun is low ahead.
- Analyst test: a strong analyst who conforms the recorder's UTC events to the surveyed sections and the AVL passes,
  removes the trailing cars' copies, nets new operators, darkness, sky cover and the school term, and reads SRM-07's
  normal-weather basis correctly slates the four cells with the highest record rates, the east-running morning and
  west-running evening directions that rose this autumn (the default path's `Ends on:`), while January's sun stands
  ahead of the south-east and south-west-running directions that carry the golden slate.
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
4. Net the autumn's visible confounders with a Poisson model by cell and month: the September operator class (from the
   training register), dark passes, sky cover from the airport observations, the school term.
5. Carry each cell's adjusted rate (or its September to October level) to January and February, with January's dark
   share and the normals' sky cover.
6. Slate the four highest cells.

Ends on: the east-running morning and west-running evening cells that rose this autumn (on the shipping candidate the
default slate shares no cell with the golden).
Golden: the south-east-running morning cells and the south-west-running evening cells, quiet all season.

## Stump sentence

The default path ends on the east-running morning and west-running evening cells that rose this autumn because it reads
each cell's measured rate, adjusted for operators, darkness, sky cover and the school term, as the rate January's peaks
will see; the excess was the low sun standing ahead of those directions in September and October, and in January and
February it stands ahead of the south-east and south-west-running directions, which take the four slots.

## Survivor anatomy

- Actor: the deciding property is how much firm braking the low sun adds on each section direction and where January's
  low sun will stand, and no file has a column for either: SRM-07 3.8 files what low sun is (the geometry, as plain
  fact), the survey two coordinates per section and the AVL log each pass's times, but the sun's position at a pass,
  the excess it produced and each cell's low-sun-free base are relations nothing stores.
- Link: the signal is read by setting the sun's computed position (from the pass's clock and the city's coordinates)
  against the bearing the survey's coordinates give each direction of travel, a comparison the field's incident rate
  never asks for and no key, code or clause offers; SRM-07 names neither the sun nor a heading.
- Reflex: the field's own estimator for the deciding quantity, the near-miss exposure rate per section direction
  (firm brakes per 1,000 passes), adjusted for the visible confounders by a Poisson model by cell and month, sits at
  rung 1 and files the cells that rose this autumn (`## Default path`).
- Back-test: OPEN. The default path's month-by-cell model fits the record it is fitted on and the dashboard's line
  rates tie to the cell totals, but month-over-month carry-forward is weak on the shipped seed (Spearman 0.49 between
  September and October cell rates, top-four overlap 1; April to August against September to October 0.41), so a
  careful solver sees cell rates move; the resumed session decides whether this is a search signal to answer.
- Second use: every file the decisive step reads is in the pack for its own reason: the survey for the section ids
  and the asks' positions, the AVL log as the exposure every reader needs, the airport observations for sky cover
  (every careful reader nets it), the pick timetable for the pick's passes and SRM-07 for the WHAT; delete the glare
  step and the pack loses nothing.
- Shock: the autumn excess reads as ordinary explained movement (a new operator class in September, the school term
  from 17 August, darker October mornings), and the golden slate is not an interval of any shipped statistic: the four
  golden cells rank 4, 12, 32 and 39 of 52 on April to October rates, 7, 9, 16 and 19 on September to October and 2,
  5, 7 and 10 on October alone.
- Pins: SRM-07 files the WHAT in the agency's own procedure (every section-direction peak, firm brakes per 1,000
  passes, the pick's weekdays at the pick's scheduled times in the normal weather, the four highest expected rates) and,
  as plain fact, what low sun (3.8) and darkness (3.9) are; no filed sentence names the model, the excess, a clock rule
  or which cells January's low sun reaches.

## Readability screen

| Rung | What it reads | Verdict |
|---|---|---|
| 0 first look | each cell's April to October rate | readable |
| 1 the field's rate, netted (default path) | rates by cell and month, Poisson-netted for operators, darkness, sky and school | readable |
| 2 low sun, non-directional | a low-sun term from the sun's elevation | readable |
| 3 glare named, record carried (reader d) | the glare model with each cell's autumn alignment held | readable |
| 3x stated facts alone | SRM-07 3.8's low sun on the pick's passes at the normals' sunshine (J6 outbound AM in for F5 outbound PM) | readable |
| 4 each cell's low-sun-free base and the low-sun excess estimated from the record, carried to the pick's sun (decisive) | the record's passes with the sun's position against each direction, fitted, then the pick's passes | silent |

Rung 4 is silent: SRM-07 3.8 says what low sun is, never how much firm braking it adds, on which cells, or where
January's sun stands; executing the filed facts alone (rung 3x) files a wrong slate, so the step is an estimate.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | pass | one train's traverse, one or two cars | one per car | same call | SRM-07 3.3; same call asserted |
| SF2 | firm brake | an FB record from the active cab | FB and EB records together | same call | SRM-07 3.4; same call asserted |
| SF3 | weekday peak | by the time the train enters the section | by the pass's midpoint or exit | same call | SRM-07 3.5; same call asserted |
| SF4 | normal weather | the normals' 68 per cent sunshine in January and February | 50, 90 or 100 per cent | same call | SRM-07 4.1 and Appendix C; same call asserted |
| SF5 | rate | per 1,000 passes | per pass | same call | SRM-07 3.7; a scale |
| SF6 | the pick's weekdays | weekdays with the weekday timetable (holidays run Sunday service) | holidays kept as weekdays | same call | the pick timetable's holiday line; same call asserted |
| SF7 | the sun's time at a pass | the pass's midpoint | its entry | same call | same call asserted |
| SF8 | sky cover for a pass | the observation in the pass's clock hour | the nearest observation; the :53 report read as the next hour's | same call | same call asserted |
| SF9 | a firm brake's pass | the car's pass whose section is nearest the recorded position | the pass by time alone | same call | same call asserted |
| SF10 | darkness | sun below the horizon | sunset at minus 0.833, minus 3, civil twilight minus 6 | same call | SRM-07 3.9; same call asserted |
| SF11 | low-sun cone | 25 degrees either side of the direction | 15, 20, 30, 35 | same call | SRM-07 3.8; same call asserted |
| SF12 | low-sun elevation profile | greatest below 12, none from 25 degrees | boxes to 15 and 20; 8 to 20; 15 to 30 | same call | SRM-07 3.8; same call asserted |
| SF13 | low-sun shape | fading off the line of travel (cosine squared) | linear, box | same call | SRM-07 3.8; same call asserted |
| SF14 | controls | section direction, hour, weekend, darkness | none; no hour effects | same call | same call asserted |
| SF15 | the detector outage week | passes and brakes both left out | the week dropped on every section | same call | same call asserted |
| SF16 | clock | Mountain local time, MDT in the record and MST in the pick | UTC as stamped | same call once converted | SRM-07 3.5 ("Mountain local time") |
| SF17 | the candidate | one section, one direction, one weekday peak | a section pooled over directions | another call | SRM-07 3.6, quoted |
| SF18 | the basis | the pick's scheduled passes | the record's own passes | another call | SRM-07 4.1 ("at the pick's scheduled times on the pick's weekdays") |
| SF19 | ask A's month | the Mountain-time month | the UTC month (moves 11 of 14 figures) | another figure | the asking sentence ("each Mountain-time month") |
| SF20 | ask B's day | the service day | the calendar day | same figures | same figures asserted |
| SF21 | a record on a month's edge | none within 15 seconds of a month boundary | a recorder clock moving one across | same figures | asserted on the shipped rows |
| SF22 | ask B's window | 30 calendar days from each operator's first day in revenue service | 30 days worked | another figure | the asking sentence ("in the 30 days from") |

## Ladder

| Rung | Route | Slate on the shipped seed | Shares with the golden |
|---|---|---|---|
| 0 | first look, each cell's April to October rate | autumn's east-running AM and west-running PM cells | 1 of 4 |
| 1 | default path: the field's rate netted by a Poisson model by cell and month, October's level carried | the cells that rose this autumn | 0 of 4 |
| 2 | non-directional low sun, or sun-time by elevation bins | the low-sun-exposed autumn cells | 0 and 1 of 4 |
| 3 | per-record models in three month pools | the autumn cells | 0 to 1 of 4 |
| 3d | glare named, each cell's observed alignment carried to January | the autumn-aligned cells | 0 to 1 of 4 |
| L | five literal executions of SRM-07 (April to October, October, September to October, normal-weather, dark share) | the autumn cells | 0 to 2 of 4 |
| 4 | the golden: the sun against each direction at every pass, fitted, carried to the pick's passes | J4 outbound AM, J5 outbound AM, F5 outbound PM, F6 outbound PM | 4 of 4 |

Every rung below 4 is a complete pipeline that files a definite wrong slate; asserted in `generator/checks.py`.

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
| 8 Window length | the whole record fits the model | C3, the slate identical across the specifications (SF11 to SF14) |
| 9 Boundary inclusivity | the peak by entry time, 06:30 to 08:59 and 16:00 to 18:29 | filed, SRM-07 3.5; SF3 |
| 10 Rounding path | no graded rate; the slate is graded | C3 corridor: rates spread 27.8 to 40.8 across variants, membership fixed |
| 11 Tie-break | none needed, the fourth clears the fifth by 15 per cent | C4, asserted |
| 12 Maturity and censoring | none in the main call; ask B's windows close inside the record | C1, asserted |
| 13 Order of operations | attach, fit, project | C1, the variants agree |
| 14 Row order | file order irrelevant | C1 |
| 15 Duplicate resolution | no FB copies (active cab only) | filed, SRM-07 3.4; separation asserted |
| 16 Identity normalisation | car to AVL vehicle; badge to operator through the register | the systems' own keys |
| 17 Netting against gross | none | not applicable, stated |
| 18 Dimensional units | firm brakes per 1,000 passes | filed, SRM-07 3.7 |
| 19 Code and status semantics | FB is the firm brake, EB the emergency loop, OS overspeed | filed, SRM-07 3.4 |
| 20 Integerisation | four slots | filed, SRM-07 5.1 |
| 21 Clause scope | weekdays only, both lines | filed, SRM-07 2 and 3.5 |
| 22 Forward window contents | the pick timetable's trips and running times, the normals' sunshine | shipped driver files (the pick PDF, the normals PDF) |

## Literal reader

Executed word for word, SRM-07 gives the population, outcome, window, basis and comparison and leaves the expected rate
to be formed; every reading of a term or convention (SF1 to SF22) prints the golden slate, or is ruled out by a quoted
sentence, and the five literal executions that carry the record's own rates (rungs L) file wrong slates, so the
easy answer comes from an easy method on the same literal estimand, never from another reading.

## Oracles

None that ties only under the golden. The dashboard's line-level monthly FB rates tie to the per-cell totals under
every reading and rank nothing; its EB column is the raw record count (copies and depot tests included), which agrees
with the naive ask A route and is a seen-wrong control, never an arbiter. The normals and the pick are drivers, not
checks.

## Ask sheet

- Ask A: each line's emergency brake applications in revenue service in each Mountain-time month, April to October
  2026 (14 figures). Primary devices: A1 (D1 duplication under two clocks: a two-car train's application logged by the
  trailing car's free-running recorder up to 3.5 minutes off, paired only by block, position and time); A2 (D5 scope:
  a car bad-ordered in service is repaired and brake-tested on the depot loop the same day, so the yard sheet puts it
  on a block while it sits in the depot, and the spare that took the block over is on no sheet); hazard A3 (D4: AVL
  onboard-unit drop-outs leave revenue trips unlogged, so revenue read off the AVL log loses applications); the UTC
  month (pinned).
- Ask B: the May and August 2026 classes' overspeeds in the 30 days from each operator's first day in revenue
  service, with the class's revenue hours and overspeeds per 100 revenue hours (6 figures). Primary devices: B2 (D5
  window: route-training ride-alongs put each new operator on the run sheets with an instructor before the first solo
  run, so the first run-sheet row and the class date both open the window early); B1 (D7 keys: old four-digit badges
  until each card's reissue after the July migration, mapped only through the card register).
- Pair ceiling: 47.8 (one response on the call keeping 35 per cent of the ask figures, the other off it with the same
  ask handling); both on the call 64.2.
- Mirror leakage: 35.0 per cent of the ask weight.
- Full includer: keeps 30 to 35 per cent of the ask figures across its three routes (yard sheets with the Loop
  signature, yard sheets with the release log, the AVL log), under two fifths.
- OPEN: with the coordinator's filed meanings (the run sheet's duty column, the release log's check, the yard's
  pull-out cars, SRM-07 3.4's codes) ask B is rule application with no silent device on the careful path, and the
  cracker keeps all six of its figures; ask B is redrawn before precut (resume line).
- Measured by: generator/ceiling.py on the cut pack (shares no code with the generator; its own golden handling is
  asserted equal to figures.json).

| Ask | Cracker handling | Cracker keeps | Verdict |
|---|---|---|---|
| A (14 figures) | revenue read off the AVL log; copies and depot tests fall away, drop-out trips lose applications | 1 of 14 | miss |
| B (6 figures) | each window opened at the first operator duty; badges through the register | 6 of 6 | keeps |

## Tried and rejected

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
