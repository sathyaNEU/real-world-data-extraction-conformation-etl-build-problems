# task231 design note

Architecture 2, a re-root drawn on 2026-11-01 in the same objective (Data Quality Monitoring & Alerting) and the same
number, after architecture 1 (the Brevland Central Bank's business survey fieldwork extension, Survey Research &
Official Statistics) was retired at the batch 1 audit. The Sawyer Divide Highway District runs a road weather
information system of environmental sensor stations along its mountain highways in Montana's northern Rockies. Every
station's hourly readings pass through the quality control of its vendor, Quillan Road Weather Systems, whose spatial
test withholds an air temperature that sits more than 6.0 C from the inverse-distance-weighted mean of the station's
neighbours within 45 km, each neighbour carried to the station's elevation at 6.5 C a kilometre. A withheld reading
never reaches the district's maintenance decision support or its 511 road conditions. The district's road weather
data quality standard has a station's spatial test re-tuned before the next winter when, over the winter just closed,
the test withheld the air temperature, although the reading was the air at the sensor, in more than 2 per cent of the
station's winter hours. The 2027/28 configuration is frozen for the season, so the re-tune list for winter 2027/28 is
set now, in May 2027, from winter 2026/27's record.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task231.json`, architecture v2, drawn and registered 2026-11-01 after a
  pull (registered 2026-11-01T00:33:44Z). Physical & Environmental Sciences (client domain), task type
  `sensor-calibration-measurement` (it serves Data Quality Monitoring & Alerting only), objective Data Quality
  Monitoring & Alerting. Shape 10 (each station's share of winter hours its spatial test withheld a right reading,
  checked against the standard's 2 per cent line), decision `designation_set`, question form whether (a gate per
  station: re-tune or not, none a grammatical answer). Gap rule then objective (nothing in the pack states how a
  withheld reading is judged; the test's withheld count is a correct record and the call is scored on true readings
  withheld), no A to E pattern, decisive generator G6 (the pooled vertical profile the test assumes does not fit the
  basin floors on still nights, one band moving against the rest), then G16 (which comparison the data entitle) and
  G17. Gate G `method_or_model_selection`: the comparison a withheld reading is judged against. Strategy
  `classification_error` (the test's misclassification of true cold air as fault is the object, and the decisive step
  is the basis a reading is classified on). Calibration `physical_verification` (the October 2026 pre-season checks,
  every sensor against a reference thermometer). Context artifact `operations_log` (the vendor's QC log). Stakeholder:
  the district's road weather program manager (`field_unit_lead`), deciding with the district's road weather data
  review panel (`committee_or_panel`) ahead of the season's configuration freeze (`season_or_peak`); organisation
  `government_agency`.
- **People:** drawn with `guard.py names --geo US --seed 231` and `--seed 2310`: Melissa Hayden, Lynn Dalton, Robyn
  Reeves; the pre-season technicians Kathy Phillips and David Glenn from the same draw.
- **Data-native sentence:** on still clear winter nights the district's enclosed basins fill with cold air under an
  inversion, each basin to its own depth and strength and some of them for days under a winter high, so a basin-floor
  station's air matches only the other stations inside its own basin's pool, while the spatial test's neighbours within
  45 km, carried up or down at 6.5 C a kilometre, sit in other basins, in windy gaps that never pool, or above the
  pool's top.
- **Abstraction sentence:** none can be written against an approved build. The nearest approved anatomies are task303
  (tickets every sibling feeder opened in the same minute are the parent's event, removed by simultaneity), task182
  (each bore's own lagged response to a shared driver) and task236 (an independent fixed-protocol network measures the
  routine system's capture). Here no event is removed and no second system measures capture: each rejected reading is
  judged against the units that share its own still-air pool, the pool's membership read from how the units' records
  move together, which no distance, elevation band, route or listed grouping gives.
- **Guard:** `guard.py check` on the registered card: WARN only. `overuse.org_family` (government_agency, 43 builds):
  a state highway district is a government agency, and the honest key is kept. `repeat.gate_g` (method_or_model_selection
  against task125 v4): task125 forecasts a crime count moved between sites by a schedule; this build's mechanism is the
  comparison a quality check's rejection is judged against. `test.same_driver_older` against task309 differentiated on
  the card. Axes redrawn at registration, when task130 v6, task125 v4 and task145 v2 filed ahead of this draw:
  `composition_mix` to `classification_error` (the strategy the build honestly carries, the check's classification
  being the object), `monitoring_export` to `operations_log` (the vendor's QC log is the file the program manager works
  from), `customer_or_counterparty` to `committee_or_panel` (the district's review panel decides; the vendor only
  receives the list) and `purchase_order_or_contract` to `season_or_peak` (the configuration freeze for the 2027/28
  season forces the list). Gap and pattern redrawn from population and G16 (spent signatures in the older corpus) to
  rule and G6.
- **Sources, one line each.**
  - Boundary-layer climatology: cold-air pools in mountain basins under winter anticyclones (persistent pools, the
    nocturnal inversion, its break-up after sunrise) are a documented phenomenon of the intermountain West; the depths,
    strengths and break-up times used here are authored for the task within published ranges, no dataset reused.
  - Road weather quality control: range, step, persistence, like-instrument and spatial tests with an elevation
    adjustment at a standard lapse rate follow the public descriptions of US road weather QC practice (the Clarus and
    MADIS test families); the parameters are the vendor's in this world.
  - NTCIP 1204 environmental sensor stations report air temperature in tenths of a degree Celsius; the district's own
    sheets use Fahrenheit and feet.
  - Every file is synthetic, authored for this task, CC0 1.0.
- **Shape arithmetic (10):** each station's share of winter hours with a right reading withheld and its verdict, about
  two figures a station over the network's stations, the call (the re-tune list), the runner-up (the station nearest
  the line on each side) and the memo chart's named parts (a bar per station, the 2 per cent line, the re-tuned
  stations marked, the title naming them); the asks follow at stage 2.

## Default path

The field's own check of a spatial flag: verify each withheld reading against the background field, the regional
lapse profile of the hour (or the HRRR point forecast for the site), and count what agrees with it as wrongly
withheld.

1. Join the ESS export to the site register (RPU to site code), readings in tenths of a degree C, re-sent rows once,
   and take the QC log's spatial-test air temperature rows, one per station and hour.
2. Each hour, fit the regional lapse line to every station's reading on its elevation (or read the HRRR forecast for
   the site at that hour).
3. A withheld reading within 5 C of that background is a false rejection; anything further off was rightly withheld.
4. Each station's share is its false-rejection hours over the winter's 5,088 hours; re-tune above 2 per cent.

Ends on: SD-147, SD-226, SD-318 (Kimball Grade, Echo Grade and Ptarmigan Grade only)
Golden: SD-118, SD-122, SD-131, SD-147, SD-204, SD-211, SD-226, SD-318

## Stump sentence

The background-field check calls every cold basin-floor reading the test withheld wrong and re-tunes only SD-147,
SD-226, SD-318 (the three grades above the pools), because neither the hour's regional lapse line nor the HRRR
forecast holds the basins' cold pools; judged against the stations that share its air that hour, every one of those
floor readings was right, and SD-118 Halvorsen Meadow, SD-122 Bitterbrush Flat, SD-131 Teller Junction, SD-204 Cutler
Meadow and SD-211 Ransom Creek go on the list as well.

## Three rules

Task type: sensor-calibration-measurement (Physical & Environmental Sciences), which serves Data Quality Monitoring & Alerting: the object is the health of a sensor network's automated quality control and the call is a monitoring decision (which stations' test is re-tuned).
Domain test: the deciding quantity is each station's false-rejection share of the vendor's spatial check, which the field settles by meteorological verification of each withheld observation against the air it was measuring, using the boundary layer's structure (the free-atmosphere profile and the basins' nocturnal inversions).
Swap: "which hospital laboratories have their analyser's delta check re-tuned" stops making sense, because nothing in a laboratory's samples pools by night, decouples from a regional profile or moves together inside a basin; the deciding relation is co-movement inside a cold-air pool, which only a meteorological network has.
Layer 1: the ESS export in NTCIP tenths with UTC hour-end stamps and RPU ids (the RPU export), observations re-sent by the server's re-polls, the QC log mixing step, spatial and dew-point range rows across the mid-winter 4.3.2 release (the vendor's QC), a dew-point no-data code at Coyote Gap (the RPU), the modem swaps and the shop spare (the district's telemetry), the pavement export in each sensor's own units under two firmware code tables (the RPUs); nothing is placed to be caught.
Layer 2: comparison-group choice under spatial structure: the reference a withheld reading is judged against has to be the stations sharing its air that hour, which on still nights is a basin's own cold pool, not the pooled vertical profile the test and the field's background check both assume.
Decisive step: recognising that a basin floor's air on a still night is shared only by the other floor stations of its own pool, found from how their night records move together on the hours the QC passed, and judging each withheld reading against those stations (any other station against the free air around it carried to its elevation).
Not semantics: with every column, unit, code and clock read correctly the background-field route still files SD-147, SD-226, SD-318 alone, because the lapse line and the forecast are correct readings of the free atmosphere and wrong references for a pooled floor; no field, code or definition flips the call.
Not rule application: the standard defines a false rejection by the probe's accuracy against the air at the station and says nothing of how that air is known; the enumerated family (trust the test, every withheld reading right, lapse refit, the two nearest stations within 150 m, night and low, the station's own percentiles, co-withheld neighbours, the HRRR forecast) files six different sets from none to twelve stations, the standing family (pool mates by co-movement, tolerance 1.5 to 4.5 C, six groupings, three radii, any mate or the median) files one set with identical hours at every station, and the ruling-out is quiet: only the co-movement on the hours the QC passed separates the pools.
Analyst test: a strong analyst who reads every field and the standard verifies each withheld reading against the regional lapse profile of the hour or the HRRR forecast, the field's background check, and files SD-147, SD-226, SD-318 (the floor readings look like faults against both).
Estimand: the standard (Rev 2, sections 2 and 3, sdhd_road_weather_data_quality_standard_rev2.pdf) files the population (each station, each automated test), the outcome (a winter hour on which the test withheld an air temperature within 0.3 C of the air at the station), the window (1 October 00:00 to 1 May 00:00 Mountain time), the unit (the share of the winter's hours) and the comparison (above 2 per cent).
No decoy: nothing is planted to be caught: the faults (rime at two passes, a connector, a radiation shield, a wet filter) are what such a network sees and are rightly withheld, no memo, draft or stakeholder figure argues a set, and the review request carries no figure or method.
No certified replay: no file publishes a verdict on any withheld reading or a share to reproduce; the vendor's acceptance record is a summer archive with injected faults and the October checks are against a reference thermometer, neither the winter's record.
Lesson: a spatial consistency check's rejections are judged against the stations that share the observation's air, which in mountain terrain on still nights is a cold pool's membership read from co-movement, not distance, an elevation band or a regional profile; no build on file judges a quality flag against an air-mass grouping inferred from the records.

## Survivor anatomy

Actor: the deciding property, which stations share a reading's air that hour, has no column: the register carries coordinates, elevations and routes, the QC log the vendor's estimate and deviation, and no file names a basin, a pool or a group.
Link: the pool's membership is read through the co-movement of the stations' night residuals on the hours both readings passed the QC, a link no key offers; distance and elevation only bound it (gaps and grades inside the bounds do not co-move) and no sentence invites the comparison.
Reflex: the field's background check for a spatial flag, the hour's lapse refit or the HRRR forecast, sits at rung 2 and files SD-147, SD-226, SD-318.
Back-test: the vendor's acceptance record (summer 2024, every injected fault withheld, 0.3 per cent of clean observations withheld) and the October pre-season checks (every probe within 0.3 C of the reference) both validate the textbook routes of trusting the test or the probes.
Second use: every file the decisive step reads has its own use: the ESS export and the QC log are the review's record, the register is the network's inventory and carries the pavement sensors the asks read, and the standard governs the asks' indicators too.
Shock: the pooled floors' withheld hours read as ordinary cold nights in a mountain winter; sorted by withheld hours the faulted plateau and passes interleave with the floors (Big Prairie 349 sits between Teller Junction and Ransom Creek), so the golden set is not an interval of any single sorted statistic.
Pins: the standard files the WHAT (population, outcome, window, unit, comparison) in the district's own genre; no filed sentence names a pool, a co-movement, a grouping, a tolerance or a reference station, and deleting any one filed sentence leaves the call forced by the readings.

## Readability screen

| Rung | What a solver reads that points at it | Verdict |
|---|---|---|
| R0 trust the test | the acceptance record (every injected fault withheld) | readable |
| R1 every withheld reading right | the October checks (every probe within 0.3 C) | readable |
| R2 hourly lapse refit within 5 C (default path) | the QC configuration's own 6.5 C per km; the field's background check | readable |
| R3 buddy check, two nearest within 150 m | the field's vocabulary (buddy check, like-instrument test) | readable |
| R4 night and below 1,600 m | the cold nights at the low stations in the QC log | readable |
| R6 the station's own month-hour range | the field's vocabulary (climatological range test) | readable |
| R7 withheld with a neighbour within 30 km | simultaneous rows in the QC log | readable |
| R8 HRRR forecast within 5 C | the forecast file in the pack | readable |
| R5 pool mates by co-movement (decisive) | no sentence, column, key or code names a pool or its members | silent |

Reflex row, from the field's vocabulary for verifying a spatial flag (buddy check, background field, model
analysis, climatological range, inversion screening by elevation band): each lands on R2, R3, R4, R6 or R8 above, none
on the golden.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | winter | 1 October 00:00 to 1 May 00:00 Mountain time, 5,088 hours | the window from UTC midnight | same call | standard s2; checks.py SF1 |
| SF2 | share | false-rejection hours over the hours of the winter | over the hours the station delivered | same call | standard s3 "as a percentage of the hours of the winter"; checks.py SF2 |
| SF3 | above 2 per cent | strictly above | at or above | same call | standard s3; no share within a point of the line, checks.py SF3 |
| SF4 | right | within 0.3 C of the air at the station that hour | 0.3 C as the tolerance between stations | drops SD-118 and others | standard s2 (the probe's accuracy against its own air); stations sharing a pool differ by more than 0.3 C on 59 per cent of the hours the QC passed, which the October checks contradict; checks.py SF4 |
| SF5 | the stations sharing its air | the median of the pool mates | any one pool mate within the tolerance | same hours | checks.py SF5 and G7 |
| SF6 | withheld by that test | the spatial test's rows | every air temperature row (the step test too) | same call | standard s3 "by that test"; checks.py SF6 and R2 |
| SF7 | the test | configuration 4.3 under both releases | 4.3.0 and 4.3.2 as two tests | same call | QC configuration s4 (air temperature tests unchanged); checks.py SF7 |
| SF8 | station | the site code, joined from the RPU | the RPU as the station | same call | one RPU per site; checks.py SF8 |

## Ladder

| Rung | Route | Files | Against the golden |
|---|---|---|---|
| R0 | trust the test: nothing it withheld was right | none | misses all eight |
| R1 | every withheld reading right | twelve stations | adds SD-158, SD-277, SD-336, SD-344 |
| R2 | hourly lapse refit within 5 C (default path) | SD-147, SD-226, SD-318 | misses the five floors |
| R3 | the two nearest stations within 150 m, within 2 C | SD-131, SD-147, SD-226, SD-318 | misses four floors |
| R4 | night and below 1,600 m | six stations | misses SD-226, SD-318 |
| R6 | the station's own month-hour 2nd to 98th percentile | twelve stations | adds the four faulted |
| R7 | withheld with a neighbour within 30 km | seven stations | misses SD-318 |
| R8 | HRRR forecast within 5 C | SD-147, SD-226, SD-318 | misses the five floors |
| R5 | pool mates by co-movement, others against the free air (golden) | the eight | |

Margins: the lowest re-tuned share is 3.83 per cent (SD-226) and the highest other 0.45 (SD-307), so the line sits in
a gap and no rung's error is a rounding.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | every station of the register, every winter hour | filed (standard s3); C1 |
| 2 Unit of account | the station and the test | filed (standard s3) |
| 3 Attribution window | the hour ending at the observation's stamp | filed (standard s2); C1 (SF1) |
| 4 As-of dating | the readings as the export holds them | C1: re-sent rows identical |
| 5 Version basis | QC configuration 4.3 under both releases | filed (QC configuration s4); C1 (SF7) |
| 6 Denominator | the winter's hours | filed (standard s3); C1 (SF2) |
| 7 Weighting | none: an hour count per station | C1 |
| 8 Window length | the one winter | filed |
| 9 Boundary inclusivity | above 2 per cent | filed; C1, nothing near the edge (SF3) |
| 10 Rounding path | hours counted, the share rounded once to one decimal | filed in the prompt |
| 11 Tie-break | none arises | C1 |
| 12 Maturity and censoring | the winter is closed | C1 |
| 13 Order of operations | judge each withheld reading, then count | C1 |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | a re-sent observation once | C1: identical readings (R2) |
| 16 Identity normalisation | RPU to site through the register | C1 (SF8) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | tenths of a degree C in the export, C in the QC log | C1: the two agree reading for reading |
| 19 Code and status semantics | the QC log's test column | filed (QC configuration s1); C1 (SF6) |
| 20 Integerisation | whole hours | C1 |
| 21 Clause scope | the spatial test of the air temperature | filed (standard s3, per test) |
| 22 Forward window contents | the 2027/28 configuration is set from the closed winter | filed (standard s3, the 1 June list) |

## Literal reader

Executed word for word: the standard's false rejection needs the air at the station in each withheld hour, which no
file holds, so a literal reader must estimate it; every estimate from the stations sharing the air (median or any
mate, tolerance 1.5 to 4.5 C, six groupings, three radii) gives the golden hours at every station (checks.py G5 to G7),
the only literal alternative to that estimate (0.3 C between stations, SF4) contradicts the October checks, and the
reader who estimates the air from a regional profile is the default path, not another reading of the text.

## Oracles

None ships. No file says which withheld readings were right; the vendor's estimate in the QC log is the test's own,
the HRRR forecast is a distractor that agrees with the default path (checks.py L3), and the October checks confirm the
probes, not the winter's readings. The generator's truth (each reading within 0.3 C of its station's air) never leaves
the generator; checks.py G1 asserts the golden reproduces it hour for hour.

## Ask sheet

Asks as built: each station's unavailable hours under Schedule B (31 figures), and its travel-lane freezing hours and
ice hours (62 figures). Devices: the modem register's removed rows and the shop spare's messages placed only through
the ESS export (D7), server times in local civil time with their zone (D8), a message's several hours (D6), re-sent
pavement rows (D1), each sensor's own units and a replaced sensor under an old serial (D3, D7), the firmware code
table switch per serial (D2), bridge-deck ports (D5).

Pair ceiling: 82.9, measured on the cut pack: over the 60 ceiling; the asks are executable from what the register,
Schedule B and the standard file, and must be reworked before stage 4's judge (resume step in pipeline.json).
Mirror leakage: 98.9 per cent of ask weight kept by the default-path response (the asks are decoupled, so the mirror
keeps what the cracker keeps).
Measured by: generator/ceiling.py

| Ask | Cracker (lands the call, executes every filed rule, runs the hygiene battery) | Mirror (stops at R2) | Verdict |
|---|---|---|---|
| A unavailable hours (31) | keeps 30 (drops the unregistered spare at SD-171) | keeps 30 | keeps |
| B freezing hours (31) | keeps 31 | keeps 31 | keeps |
| B ice hours (31) | keeps 31 | keeps 31 | keeps |

## Architecture 1 record (spent 2026-10-31)

- Draw: Survey Research & Official Statistics, `nonresponse-calibration-measurement-error-adjustment`; the Brevland
  Central Bank's quarterly Business Conditions Survey, which regions go into the September 2026 round's reminder-call
  extension, read on the round's response rate over the panel firms still trading on the frame date. Shipped 10-13.
- Default path: the business register as it stands taken for the in-scope population; ended on five regions into the
  extension. Golden: Capital and Harbour into the extension, Islands and Western Uplands onto the email, from the
  closure share of the round's silent firms read from rounds the register had caught up with.
- Fate: no portal result; retired at the batch 1 audit (the survivor anatomy absent, the pair ceiling unmeasured, a
  count the data hold in the prompt, three files that describe the data). Its judge report is kept as
  `determinism_check_report_arch1.md`.

## Tried and rejected


- Seed pitfall kept (Rubin's rules over shipped implicates): a reflex for any strong solver once the implicates ship;
  rejected at the draw.
- GSD missing-data framing (meter reads imputed in a utility network): the deciding quantity reads the same in any
  field, the backdrop the author keeps getting returned; rejected at the draw.
- Product analytics SRM alert, psychometric reliability under a population change, consensual observer drift, SSI
  post-discharge ascertainment, AMR cascade testing, airport noise-monitor capture: each either read as a reflex (ramp
  SRM, a pilot alpha), split into competing defensible methods (CTT against IRT, drift indices), sat in a pairing the
  wave's epidemiology seeds need, or turned on a fleet mix (composition, banned in the window); rejected at the draw.
- Silence run as the decisive rung (closure share by rounds since the last return): prototype 2026-10-13 put the
  pooled and run-based estimates within 0.3 points of each other; the run is a corridor variant, not a rung.
- An insolvency wave to make the run decisive: the settled history stops transporting to the wave regions (the
  estimate misses the truth by about 5 points there); rejected.
- Per-region response rates as graded figures: the reasonable settled-round estimators (pooled, by region, by rounds
  silent, by size) differ by up to 1.4 points in a region because a region's closure share among non-returners falls as
  its response rate falls; graded at whole per cent they would split rigorous solvers. The graded figure became the
  standard's alert level, which every settled estimator lands identically (2026-10-13).
- Register lags of 900 days and a five-year settled window, to make pooling all history a rung on the call: the
  settled-estimator corridor widened to 1.8 points (Islands) without moving the all-history route off the extension list;
  reverted to the 780-day liquidation route and a four-year window (2026-10-13).
- Reminder calls on the simulation's calendar days 15 to 20, weekends included: moved to working days from day 15 to the
  close, which reshuffles every region's draws; propensities recentred and stream offsets re-searched (2026-10-13).
- An all-history route one region off the call (Border only): the re-search found offsets where every route short of the
  settled share also sends Islands and Western Uplands into the extension; adopted (2026-10-13).
- Enterprise-group calls logged once under the group's lead firm, as the firms-reached device: the group's firms carry
  independent call outcomes in every other round, so the convention contradicts the history; replaced by calls firms make
  to the inbound desk (2026-10-13).
- The codebook's definition of reached as the only device on firms reached: a careful solver executes it; the inbound
  desk's callbacks added (2026-10-13).
- Panel IDs reissued from any freed identifier: earlier holders sit in the settled rounds, so a join through the register
  would mislink the main population; reissue limited to the 2024 expansion block, freed before July 2025 (2026-10-13).
- Contractor-style six-digit company numbers in the main files: an exact join would miss those firms' closures silently
  and move the call; the main files carry the check-digit form only, the six-digit form stays in the contractor's call
  records and the cancelled duplicate recruitment records (2026-10-13).
- A main close on Christmas Day 2020 and 2026 and on Christmas Eve 2021 (the Friday on or before the 25th taken
  literally), found by the leak reader: the December close moves to 23 December when that Friday is the 24th or 25th, and
  the post room keeps the Christmas and New Year holidays; the settled share moves from 15.32 to 15.30 per cent and no
  level or margin moves (2026-10-13).
- A second analytical layer at the author's request (2026-10-14): the panel's closures rising 1.84 times from January 2025, read off the voluntary dissolutions the register records within months, carrying the settled share to 27.8 per cent. The leak reader was clean and the first judge pass approved, but the re-judge after closing a completeness-nowcast fork returned SEND_BACK: the defensible nowcasts of the current closed share (other rise windows, a ramp-weighted rise, contact-centre calibration, lag corrections, regional rises) spread from about 19 to 36 per cent, while Islands and Western Uplands stay amber only from 23.8 to 32.2, a band the rates' geometry near the lines fixes at about nine points; filing the estimator would make the step rule application. Reverted to the shipped build (8fd3d48), which rebuilds byte-identical.
- Architecture 1 (the Brevland Central Bank's Business Conditions Survey extension, shipped 10-13) retired at the batch 1 re-root (2026-10-31): the audit found the survivor anatomy short in every part (no Actor, Link, Reflex, Back-test, Second use, Shock or Pins line in the note), the pair ceiling never measured by a script on the cut pack (precut FAIL), the prompt stating a count the data hold ("our twelve regions") and three shipped files that describe the data (a data dictionary, the register's extract notes and an export manifest, each a leak.py LEAK); re-rooted in a new world rather than repaired, so the portal sees one strong build.
- Architecture 2 draw (2026-11-01), candidates weighed and set aside before the card: selective antimicrobial testing
  by ward (the untested isolates rebuilt ward by ward is stand-ins reweighted within the selecting class, the family
  task275's observed and unobserved trips already spent at approval); a fleet failure hazard by analyser age since
  overhaul (a replacement restarting the wear curve, task132 approved); a calibration hour that coincides with the
  daily peak (gaps that are not random over a count above a level, task245 delivered); airport noise monitors' capture
  of loud departures (the field's own noise-power-distance prediction is the golden, a reflex at rung 1); a quality
  check's false rejections with a winter maintenance log in the pack (every station the log shows fault-free hands over
  its pooled readings as right, so the log route lands the call without the basin comparison; the pack carries only the
  October pre-season checks); trigger-truncated blast vibration records (the censored fit is a named correction and
  the model family stays open); the queue cap of a phone SDK (task235's world, delivered).
- 2026-11-01, architecture 2 build: a freezing-fog rime fault at N1, added to break the co-withheld rung, was dropped. It broke the N pool's co-movement and left N2 judged against the free air; moved to Q3, it contaminated the median of Q2's two-mate reference. The floor fault became Q3's wet filter on spring afternoons, which no pool mate shares.
- 2026-11-01, architecture 2 build: the spatial test first ran on every reading the export eventually held. A real QC run at 20 minutes past the hour sees only what the server holds, and with that change every withheld floor reading has a delivered mate in the export (checks.py G13). Planned work was booked at the mountain sites, and the long telemetry dropouts were kept inside the RPU's 96-hour buffer.
- 2026-11-01, architecture 2 build: two-decimal shares were dropped for one decimal. Across the median-based family the hours are identical; a mean of the stations sharing the air, or each hour's fitted lapse, moves a few hours at named stations (checks.py G7, G8) and never the set.
- 2026-11-01, architecture 2 asks: the Schedule B unavailable hours and the pavement freezing and ice hours, as built, measured a pair ceiling of 82.9 (generator/ceiling.py). Every device except the shop spare is executed from a filed rule or a register sheet. The asks return to stage 2 (supplemental-stumping) before stage 4's judge; the main call and its pack stay as built.
