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
recorded in `metadata.json` at stage 3: the recorder export (UTC, WGS84), the AVL section-pass log (local time), the
track survey (State Plane, US survey feet), hourly airport observations (METAR sky condition), the operator roster and
training register, the yard's consist log, the January pick timetable (PDF), SRM-07 (PDF), the station normals table,
and distractors (pedestrian counters, the arena's events calendar, track maintenance) named only in `metadata.json`.

**The five go/no-go screens** (prototype `scratchpad t210/a2/proto/screens_a2.py`, 24 redraws on the clean truth,
seeds 21001 to 21024; results in `screens_a2.json`; to be re-run and asserted in `generator/checks.py` at stage 2):

1. **Realistic levels and the lever.** Levels and their sources:
   - sun position: NOAA Global Monitoring Laboratory, General Solar Position Calculations (the golden's geometry);
   - January and February sunshine about 68 per cent of possible: NOAA NCEI, Comparative Climatic Data (Front Range
     stations near 70 per cent in winter); April to October 62 to 72 per cent;
   - sun glare raises crash risk on approaches facing a low sun (Mitra 2014, Safety Science 70, 246 to 254); glare
     situations predicted from road alignment and sun position (Jurado-Pina and Pardillo Mayora 2009, Transportation
     Research Record 2120, 12 to 17). The full-alignment multiplier here is 3.2 under full sun (glare-weighted mean
     about 1.9 on the exposed passes), at the upper end of the published excesses, a modelling choice stated as such;
   - darkness raises pedestrian crash risk severalfold (Sullivan and Flannagan 2002, Accident Analysis and Prevention 34,
     487 to 498); here 1.30 on street-running firm braking, 1.15 on reserved track;
   - US daylight saving time ends on 1 November 2026 (Energy Policy Act of 2005 schedule);
   - world-set, no published rate to cite: firm braking at 20 per 1,000 street-running section passes and 8 on reserved
     track (about one firm brake in 50 street passes, ART's own 2025 dashboard level), new operators 1.3 times for
     their first months, the school term 1.1 times in the morning peak.
   Lever: the golden recovers the true slate in 23 of 24 redraws; every rival's slate differs from the golden in 24 of
   24, sharing at most two of the four cells; the golden's fourth cell stands above the best rival-only pick by a
   median 12 per cent of its own estimate (minimum 1 per cent); the shipping candidate (seed 21009) has its fourth and
   fifth cells 27.6 per cent apart and every rival-only pick 28 per cent below the fourth. Pack size planned under 15 MB.
2. **The golden's own method holds the call.** Nine specifications (glare half-widths 20, 25 and 35 degrees; linear and
   box forms; elevation profiles 8 to 20 and 15 to 30 degrees; a log-linear glare term; sunshine at 85 per cent of the
   normals; no hour effects) give the same slate in 18 of 24 redraws and all nine at the shipping candidate.
3. **The first look lands wrong** (each cell's April to October rate): 24 of 24, at most one golden cell shared.
4. **The careful readers land wrong**, 24 of 24 each:
   (a) field-decomposing (cell, month, darkness, sky cover; October's level carried): at most two shared;
   (b) constructing, two forms (a non-directional low-sun term from solar elevation; sun-time bins read by elevation):
   at most two and one shared;
   (c) per-record, three month pools (section direction by peak by clock hour by sky, all months, September and
   October, October): at most one, two and two shared.
5. **Literal execution** of SRM-07's WHAT, five operationalisations (April to October rate, October, September to
   October, the rate re-weighted to the normals' sky cover, the rate re-weighted to January's dark share): 24 of 24
   wrong, at most two shared. The golden needs a step SRM-07 never names: the sun's computed position against each
   direction of travel, the excess it produced fitted on the record and carried to the pick's passes.

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
- Layer 1: the recorder's UTC stamps against the AVL log and timetable on Mountain time across the 1 November clock
  change (the recorder system and the AVL system each keep their own clock); recorder positions in WGS84 with GPS scatter
  against a survey in State Plane US survey feet (the GIS team's standard); the trailing car's copy of each brake on
  two-car consists (each car carries its own recorder); short-turned and cancelled trips and a timepoint outage week in
  the AVL log; operator badges renumbered in the July HR migration; the August firmware update that renamed the event
  codes; METAR sky-condition codes with missing hours; the January pick published as a PDF table of headways. None is
  placed to be caught and none decides the call.
- Layer 2: estimation that fits the data (`estimation_fit`): the excess braking is attributed to the low sun ahead of
  each direction of travel, fitted on every pass of the record, and carried to the pick's passes under January's and
  February's sun; the choice that flips the call is reading the excess as a property of the sun's position rather than
  of the cell where it was measured.
- Decisive step: the sun's position at every pass, computed from the clock and the city's latitude and longitude, set
  against each section direction's line from the survey, with the excess it produced fitted on the record and carried
  to the January and February peaks.
- Not semantics: reading every field, code, clock and unit correctly (the UTC stamps, the coordinates, the consist
  copies, the badges, the firmware codes, the sky codes) still leaves each cell's measured rate, which is the autumn
  sun's rate, and no field, code or definition anywhere states where the sun stands.
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

1. Read the recorder export, convert its UTC stamps to Mountain time, and map each firm brake to its section and
   direction against the track survey; drop the trailing car's copy on two-car consists.
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

## Tried and rejected

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
