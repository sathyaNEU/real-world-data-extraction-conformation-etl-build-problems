# task231 design note

Architecture 2, a re-root drawn on 2026-11-01 in the same objective (Data Quality Monitoring & Alerting) and the same
number, after architecture 1 (the Brevland Central Bank's business survey fieldwork extension, Survey Research &
Official Statistics) was retired at the batch 1 audit. The Sawyer Divide Highway District runs a road weather
information system of environmental sensor stations along its mountain highways in Montana's northern Rockies. Every
station's hourly readings pass through the quality control of its vendor, Quillan Road Weather Systems, whose spatial
test withholds an air temperature that sits more than 5.0 C from the inverse-distance-weighted mean of the station's
neighbours within 50 km, each neighbour carried to the station's elevation at 6.5 C a kilometre. A withheld reading
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
  Reeves.
- **Data-native sentence:** on still clear winter nights the district's enclosed basins fill with cold air under an
  inversion, each basin to its own depth and strength and some of them for days under a winter high, so a basin-floor
  station's air matches only the other stations inside its own basin's pool, while the spatial test's neighbours within
  50 km, carried up or down at 6.5 C a kilometre, sit in other basins, in windy gaps that never pool, or above the
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
