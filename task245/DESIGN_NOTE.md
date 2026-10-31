# task245 design note

Architecture 1, wave 4, seed DQ18 (which monitoring sites' annual compliance statistic is reportable): the seed's
world (a monitoring network's annual statistics), decision (which sites' statistic goes out as it stands and which
carries a data-capture flag) and quantity (each site's annual count of days above a daily limit) only. The seed's
pitfall is a data-capture rule (counting exceedances over whatever readings arrived), which executed is rule
application, so the pitfall is re-found in the data: the analysers that fault under heavy loading lose exactly the days
a bulk terminal's dust plume blows onto them, so a station's lost days are not like its reported days and have to be
rebuilt from the day's wind and the rest of the network.

Thornmouth (a fictional coastal borough in north-east England): the council's air quality team runs seven automatic
monitoring stations; the operator of the Thornmouth Bulk Terminal runs five PM10 stations around the terminal under its
environmental permit and shares their data with the council; the council's QA/QC contractor audits the network's 2027
data before the council's Annual Status Report. The UK air quality objective for PM10 is real: a 24-hour mean of 50
micrograms per cubic metre, not to be exceeded more than 35 times a calendar year.

## Draw

Card `cards/task245.json` (architecture 1, registered 2026-10-18). Guard verdict PASS; the one NOTE
(test.same_puzzle_older against task265 v1) is differentiated on the card: task265 corrects a survival curve's risk set
for units the record saw only after their start, while here every day of the year is in the population and the record
loses the heaviest days as they happen. Nearest driver task229 v3 at 0.06.

- **Pairing.** Physical & Environmental Sciences / environmental-monitoring-exceedance, a task type serving Anomaly
  Detection and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not banned against the last three
  builds (task164 energy load forecasting, task162 product feature adoption, task163 economics forecast evaluation).
  The object is the health of each station's 2027 record (whether the days its analyser lost change its standing
  against the objective), the call a monitoring decision: which stations' 2027 PM10 results go to the audit and into
  the Annual Status Report with the data-capture note.
- **Niche.** A borough network's data-capture review before its annual report: the PM10 objective counts days above
  50 over a calendar year, the stations around a bulk terminal see its dust only on their own wind bearing, and the
  terminal operator's older analysers fault on the heaviest hours and stay down until the next working-day visit.
- **The call.** Which of the 12 stations have a 2027 count of days above 50 over their valid days of 35 or fewer while
  their count over the whole year, every day counted (the days without a valid daily mean included), is more than 35;
  those stations cannot be reported as meeting the objective and carry the data-capture note.
- **Shape.** 10, a scorecard of metric-threshold checks: per station the count over valid days, the whole-year count
  with its accepted range and the note (12 stations), the noted set, the chart (each station's two counts against the
  35-day line) and the asks' per-station figures, well over 25 criteria before the rubric folds them. Decision
  designation_set, answer set_of_items, question form which.
- **Strategy.** population_selection: the reported days are a selected population, the year is the estimand. G9
  decisive (the reported days are the days the analyser survived, and it does not survive the heaviest hours), G12 (a
  lost day is the absence of a record, not a record of a clean day), G16 (a station's lost days filled from its own
  reported days, from the network alone, or from the network plus the station's own response to the wind); gap
  population; Gate G decomposition_attribution (each station's level split into the network's background and the
  terminal's plume by the hour's wind); calibration none; context artifact monitoring_export (the council's and the
  operator's hourly exports); Layer 2 family estimation_fit, pattern own:informative-outage-plume-sector-infill.
- **Forum, event, organisation.** auditor (the council's QA/QC contractor, whose annual audit signs off the network's
  2027 statistics before the report), audit_or_inspection (the audit closes on the 2027 data year), local_government
  (Thornmouth Borough Council). All clear the last three (task162, task163, task164: committee_or_panel,
  executive_team, regulator_or_inspector; cutover_or_migration, budget_or_appropriation, statutory_or_regulatory_filing;
  software_or_platform, professional_services, utility_or_infrastructure). Role compliance_or_audit (the council's air
  quality officer, who answers to the auditor), clear of field_unit_lead, finance_controller and programme_officer.
- **People** (`guard.py names --geo "United Kingdom" --seed 245`): Harriet Hopkins, the council's air quality officer,
  who asks; Marc Bevan, the QA/QC contractor's auditor; Jemma Holloway, the terminal operator's environmental manager,
  who sends the operator's export. None appears in the prompt.
- **Data-native sentence.** The terminal lies on a fixed bearing from each station, so its dust reaches a station only
  on the hours the wind blows from that bearing, and the operator's older analysers fault under exactly that loading
  and stay down until the next working-day visit; each such station's lost days are its plume days, not a random part
  of its year, while the rest of the network, off that bearing, reads an ordinary day.
- **Sources.** The client's two-layer standard (estimation_fit: an estimate that ignores the data's structure; here
  the structure is informative loss, the losses falling on the outcome's high values). layer2-rigor-patterns.md has no
  patterns for this domain, so the pitfall comes from the family, not a listed pattern. The seed DQ18 gave the world,
  the decision and the quantity only. UK local air quality management practice gave the reflexes the ladder is built
  against (data capture, the 90.4th percentile of daily means reported where capture is short, the expected-exceedance
  scaling a US reader brings), each of which treats the lost days as like the reported ones. The field's own tool for a
  station against the wind (the bivariate polar plot of concentration by wind direction and speed) is the decisive
  step's instrument; nothing in the pack names it.
- **Mechanisms on file** (`guard.py mechanisms --objective data-quality-monitoring`, 16 builds), the insight each
  spends: 229 a convex conversion of a daily mean (and, in lineage, a shared-parent standard error, checks seen just
  before reset, gated arrivals); 231 exits reaching the record late; 232 a transmission rate from delayed closed
  episodes; 230 a late channel moving items to default categories; 228 events clustered within randomised units; 233 a
  gold-standard follow-up carried across base rates; 234 a share in a source's output that transit loss cannot move;
  235 an item lost only once its device had its next chance; 236 a capture change changing which cases are reached; 237
  the share of a composite's variance due to its attribute; 238 a channel effect through a randomised nudge; 239 a
  group-level factor; 240 the error of a post-stratified total; 241 a sensor's error against a reference at a
  displaced position; 242 a detector whose sensitivity fades with time since the event; 243 a growth balance carrying
  movement. None spends losses that fall on the outcome's own high values, rebuilt from a driver the record does not
  lose.

## Survivor anatomy

Actor: that a plume station's analyser stopped on the days the terminal's dust reached it has no column; it is a relation between each lost hour (a fault, power or out-of-service status in the export or the operator's workbook), the met mast's wind that hour against the station's bearing to the terminal (the register's grid references) and the station's own response to the wind fitted on its valid hours, which nothing stores.
Link: each lost hour is rebuilt from the other stations' median that hour plus the station's own increment by wind sector, speed band and wet day, a construction across stations and files (the two operators' data, the mast, the register) that no key offers and no sentence invites.
Reflex: the field's own correction for short data capture, the valid-day count scaled by capture or the 90.4th percentile of the valid daily means as UK practice reports it, sits at rungs 0 and 1 and notes Market Street and Westholme Avenue (`Ends on:`), not the golden North Gate, Harbour Walk and South Yard.
Back-test: the two field corrections agree with each other, both naming Market Street and Westholme Avenue, so a solver who checks one against the other sees the easy route confirmed.
Second use: every file the step reads is in the pack for the network's ordinary reporting: the export and the workbook for every statistic (the NO2 ask reads the export), the mast because the terminal's dust plan requires it, the register for the report's site table and the service log for the outages and the NO2 ask's logger lines.
Shock: the plume stations' lost days read as ordinary analyser faults spread through the year, their capture (285 to 294 days) above the two long-outage roadside stations, so the stations with the shortest capture are the easy route's pair and the golden three are not the extreme of any shipped statistic.
Pins: AQ-QP-04 section 5.1 files the estimand (every day of the year counts by the concentration that day, a lost day included) and 5.2 the note; no sentence says how a lost day is estimated, that the analysers stopped on plume days, or names the wind.

## Default path

1. Read the council's export (the PM10 rows, status R) and the terminal's workbook (status OK; UK clock time, each hour
   stamped with its start, moved to GMT hour ending) onto one hourly grid of the 12 stations.
2. Daily means of the valid hours where at least 18 are valid (AQ-QP-04 section 3); per station the days above 50
   among them: every station 35 or fewer (North Gate 22, Harbour Walk 17, South Yard 19, Market Street 24, Westholme
   Avenue 27).
3. Data capture per station: Market Street 232 and Westholme Avenue 235 valid days of 365 after their long outages, the
   three plume stations 285 to 294, the rest 318 to 360.
4. The whole-year count of section 5.1 (every day counts): the valid-day count scaled by data capture (count times 365
   over the valid days, the expected count for the year), or the 90.4th percentile of the valid daily means against 50,
   which UK practice reports where capture is short.
5. The note of section 5.2 where the valid-day count is 35 or fewer and the whole-year count more than 35.

Ends on: Market Street (TH5) and Westholme Avenue (TH6) noted (scaled 37.8 and 41.9, 90.4th percentiles 50.8 and
51.9), the three plume stations scaled to 28.2, 21.1 and 24.2.

Golden: North Gate (TBT1), Harbour Walk (TH3) and South Yard (TBT4) noted, their lost hours rebuilt from the other
stations' median that hour plus each station's own mean increment by wind sector, speed band and wet day: 57, 51 and 51
over the whole year (every one of 288 rebuild readings 40 or more), Market Street and Westholme Avenue 30 and 30 (none
over 33).

## Stump sentence

A competent air quality analyst brings both operators' hourly data onto one GMT grid, counts each station's days above
50 among its valid daily means, finds every station at 35 or fewer and, because section 5.1 counts every day of the
year, corrects for the lost days the standard way, scaling each count by data capture or reading the 90.4th percentile
of the valid days, and ends on Market Street (TH5) and Westholme Avenue (TH6) noted; the step that lands it there is
treating each station's lost days as ordinary days for that station, when the plume stations' analysers stopped on the
days the terminal's dust reached them, so only a rebuild of the lost hours from the network's background and each
station's own response to the wind gives North Gate, Harbour Walk and South Yard.

## Three rules

- **Task type:** physical-environmental-sciences / environmental-monitoring-exceedance, which serves Data Quality
  Monitoring & Alerting (the stations' 2027 records are the monitored data, the data-capture note the monitoring
  decision the audit signs off).
- **Domain test:** the quantity that decides is each station's count of days above the PM10 24-hour objective over the
  whole calendar year, its lost days estimated the way an air quality network estimates a station's missing hours near
  a point source: the network's regional background that hour plus the station's own increment for the hour's wind
  sector and speed (its pollution rose, the conditional mean behind a bivariate polar plot), because the source lies on
  a fixed bearing from each station.
- **Swap:** "which stations' 2027 PM10 counts cannot be reported as meeting the 24-hour objective once their lost days
  are counted" rewritten as "which hospital wards' 2027 occupancy counts breach the bed limit once their missing census
  days are counted": there is no source on a bearing, no wind and no pollution rose to rebuild a lost day from, and no
  reason a ward census fails on its busiest days, so the task stops making sense.
- **Layer 1:** two operators' exports in their own layouts (the council's long file in GMT with hours ending 01:00 to
  24:00 and status codes; the terminal's quarterly wide workbook in UK clock time with each hour stamped at its start,
  the repeated 01:00 of 31 October and the missing 01:00 of 28 March), station names against the register's codes,
  calm and missing hours on the met mast, partial days under the 18-hour rule, NO2 and NOx rows in the same export. Each
  is produced by the system that records it; none is placed to be caught, and the call is the same under every handling
  of each (SF rows) or loudly wrong.
- **Layer 2:** estimation_fit: a count over a period whose missing days are informative, the losses falling on the
  outcome's high values, estimated by conditioning on the driver that predicts both (the hour's wind against the
  station's bearing to the source) rather than treating the lost days as like the recorded ones.
- **Decisive step:** rebuilding each lost hour from the network's background that hour plus the station's own response
  to the wind (sector, speed, wet or dry day) fitted on its valid hours, so that a station whose analyser stopped on its
  plume days gets its plume days back, rather than scaling the valid-day count by data capture, reading the 90.4th
  percentile, interpolating in time or filling from the network alone.
- **Not semantics:** reading every field right (both clocks, the status codes, the 18-hour rule, the register, the
  mast) still leaves the scaled count on Market Street and Westholme Avenue: the records say a station lost a day, never
  what the day was like, and section 5.1 says a lost day counts by the concentration that day without saying what it
  was.
- **Not rule application:** the procedure files the estimand (every day counts by its concentration, section 5.1) and the note
  (section 5.2) and no way of estimating a lost day; executing every stated rule with the field's usual correction
  (scaling or the 90.4th percentile) files the wrong pair.
- **Analyst test:** a strong analyst who reads every file right and applies section 5 as filed scales each station's
  valid-day count by its data capture (or reads its 90.4th percentile) and ends on Market Street and Westholme Avenue
  (TH5 and TH6) noted and the three plume stations at 21 to 28; on the simulator's clean truth the same route files the
  same pair and the decisive step alone gives the three (R3 in checks.py).
- **Estimand:** the procedure (`tbc_aq_network_qaqc_procedure_v4.pdf`, sections 5.1 and 5.2): a station's result is the
  number of days in calendar 2027 on which the daily mean concentration at the station exceeded 50, every day of the
  year counting, a day without a valid daily mean by the concentration at the station that day; the note where the
  count over valid daily means is 35 or fewer and the result more than 35; the prompt asks for each station's days
  above 50 over the whole of 2027 in whole days.
- **No decoy:** nothing is planted: no memo, earlier assessment or stakeholder figure argues a method or a station; the
  stations' outages come from their analysers, rounds and works as logged, last year's NO2 table and the background map
  (the distractors) count no PM10 days, and no file ranks the stations on the note.
- **No certified replay:** no certified or published 2027 count exists for a method to reproduce; the method is found
  from the data's structure (the losses falling on the stations' wind bearings).
- **Lesson:** a count over a year whose lost days are not like its recorded days cannot be corrected by scaling or
  infilling from the station's own record or the network's; the lost days have to be rebuilt from the driver that
  decided both what the day held and whether it was lost, here the wind against a fixed source. No build on file
  spends losses that fall on the outcome's own high values rebuilt from such a driver (task242 a detector fading with
  time, task231 exits reaching the record late, task243 a growth balance carrying movement).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) the valid-day count scaled by data capture, or the 90.4th percentile: TH5 and TH6 | section 5.1 counts every day, no method | the status codes | yes, the expected count and the LAQM percentile | none | no | a ratio | readable |
| 1 the lost days filled from the network that day (median, ratio, regression, nearest station, station-and-hour fit): none | none | the register's other stations | yes, infill from neighbours | none | no | a ratio or offset | readable |
| 2 interpolation in time (daily or hourly), or short gaps interpolated and long outages from the network: none | none | the hourly series | yes, gap filling | none | no | a line between two hours | readable |
| 3 (decisive) every lost hour rebuilt from the network's background plus the station's own increment by wind sector, speed and wet day: TBT1, TH3, TBT4 | no sentence names the wind, the bearing, the plume or a rebuild; the procedure files only that every day counts | no column marks a lost day as dusty; the mast is a separate file joined by time | no: every reflex treats the lost days as ordinary for the station | no control, published count or earlier year's result | no | not linear: a response fitted by wind cell over 8,760 hours, then 288 readings | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | days above 50 | daily mean above 50 | at least 50 | same call | no valid daily mean within 0.6 of 50 (asserted) |
| SF2 | the daily mean | unrounded | rounded to whole units first | same call | same counts (asserted) |
| SF3 | the terminal's clock | UK clock time moved to GMT | read as GMT throughout | same call | same call (asserted); the workbook's note and the dust plan say UK clock time |
| SF4 | the terminal's stamps | the start of the hour | the end of the hour | same call | same call (asserted); "marks the start of the hour" |
| SF5 | a valid daily mean | at least 18 of 24 hours | another threshold | ruled out | section 3: "at least 18 of the day's 24 hourly means are valid" (asserted) |
| SF6 | the station's result | every day of the year, a lost day counting by the concentration that day | the valid days only, or every lost day as an exceedance | ruled out | section 5.1: "such a day counts if the concentration at the station that day exceeded 50 µg/m³, and not otherwise" (asserted) |
| SF7 | the repeated 01:00 of 31 October | BST then GMT | read once, as GMT | same call | same call (asserted) |
| SF8 | calm and missing mast hours | the nearest reported direction | interpolated through the wind vector | same call | same call (asserted) |
| SF9 | more than 35 | strictly more | 35 or more | same call | no station within one of 35 under any rebuild (asserted) |
| SF10 | a day without a valid mean | its valid hours kept, the rest rebuilt | every hour rebuilt | same call | both in the family of readings (asserted) |
| SF11 | a wet day | the mast's rain over 0.2 mm | over 0 or over 1 mm | same call | same call (asserted) |
| SF12 | the year | calendar 2027, GMT days | none differs | converge | the procedure's GMT days; 365 days (asserted) |
| SF13 | the background | the median of the other stations that hour | the council's background stations, the rural station, a station-and-hour fit | same call | all in the family of readings (asserted) |
| SF14 | the council's hours not R | no value | none differs | converge | every such hour is blank (asserted) |
| SF15 | the terminal's hours not OK | no value | none differs | converge | every such hour is blank (asserted) |
| SF16 | a day on the terminal's wind (the evidence) | six hours or more within 22.5 degrees of the bearing to the stockyard centre | another count of hours or width | same call | the lost days carry that wind at least twice as often as the valid days at every noted station (asserted) |

## Ladder

Three wrong rungs and the golden, each a defensible way to count the lost days, each dying to one fact of the record
(figures on the cut pack, printed by `generator/pair.py --ladder`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | the valid-day count scaled by data capture; the 90.4th percentile of the valid daily means (four methods) | TH5 and TH6 (scaled 37.8 and 41.9; percentiles 50.8 to 52.5); the three plume stations 21.1 to 28.2 | the mast: the lost days at the three carry the terminal's wind on 103 of 229 days against 72 of 866 valid days |
| 1 | the lost days filled from the network that day (nine readings) | none; the three at 20 to 28 | the same: on their valid days with the terminal's wind the three average 53.9, 82.1 and 63.0 against the other stations' median daily mean of 19.9, 22.2 and 21.0 |
| 2 | interpolation in time (daily, hourly, or gaps up to 24, 72 or 168 hours interpolated and the rest from the network); monthly scaling | none, or TH6 alone by monthly scaling; the three at 18 to 31 | the same: the stations stopped on the plume's day and restarted after it |
| 3 (golden) | every lost hour rebuilt from the network's background plus the station's own increment by wind cell | TBT1, TH3, TBT4 | |

- **Margins.** The three sit at 57, 51 and 51 (288 readings: 40 to 60, 46 to 57, 45 to 55; each accepted range a day
  wider); the other nine at 33 or under under every reading (TH6 27 to 33, TH5 24 to 32, East Berth 12 to 16, West Gate
  9 to 15). No easy route puts any of the three over 31.
- **Position.** The three are reached by no other rung; the default path and the percentile file TH5 and TH6, the
  network and interpolation file nobody, monthly scaling TH6 alone.
- **Dominance.** The decisive move takes the three from 21 to 28 (scaled) to 51 to 57 and the quiet-gap pair from 38
  and 42 to 30 and 30; it moves the six well-recorded stations by two days or less.
- **Grid.** Scaling or the percentile (TH5, TH6); the network alone (none); interpolation or hybrids (none); monthly
  scaling (TH6); any wind-aware rebuild (the three). On the simulator's clean truth scaling files TH5 and TH6 and the
  wind rebuild the three (R3). Counting each analyser stop as a dusty day also gives the three (59, 46, 53; East Berth
  26): that route already treats the lost days as the dust days, the decisive insight.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the network's 12 stations, the council's seven and the terminal's five (the register; procedure section 1) |
| 2 | Unit of account | one station's 2027 result, one note per station (section 5.2) |
| 3 | Attribution window | calendar 2027, GMT days 00:00 to 24:00 (sections 2.1 and 3; SF12) |
| 4 | As-of dating | the ratified export; the terminal's workbook of 6 March 2028; the request of 17 March 2028 |
| 5 | Version basis | AQ-QP-04 version 4; the terminal's plan revision 3 |
| 6 | Denominator | none for the count; data capture over 365 days |
| 7 | Weighting | none for the count; NO2 a mean of hours, deposition days-weighted (plan section 3) |
| 8 | Window length | 365 days |
| 9 | Boundary inclusivity | above 50 (SF1); more than 35 (SF9); 35 or fewer over valid days |
| 10 | Rounding path | daily means unrounded (SF2), whole days, the whole-year count accepted inside its range |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | ratified 2027 data; nothing later arrives |
| 13 | Order of operations | grid, validity, daily means, rebuild, whole-year count, note |
| 14 | Row order | no step depends on file order but the repeated 01:00 (BST first, SF7) |
| 15 | Duplicate resolution | no PM10 hour repeated; the NO2 week sent twice counted once (ask A) |
| 16 | Identity normalisation | the terminal's station names to the register's codes |
| 17 | Netting against gross | none |
| 18 | Dimensional units | µg/m³, days, mg/m² per day |
| 19 | Code and status semantics | R, F, X, S, P, O; OK, FAULT, REJECTED, SERVICE, POWER, OFF (SF14, SF15) |
| 20 | Integerisation | counts of days |
| 21 | Clause scope | sections 5.1 and 5.2 apply to every station, the terminal's included (section 1) |
| 22 | Forward window contents | the 2027 Annual Status Report the note goes into; nothing is forecast |

## Literal reader

Executing the prompt and sections 5.1 and 5.2 word for word: for each station the number of days in 2027 whose daily
mean exceeded 50, every day counting, the days without a valid daily mean included, and the note where the count over
valid daily means is 35 or fewer and that number more than 35. The lost days' means are recorded nowhere, so the
literal estimand needs an estimate of them; the files hold the network's other stations and the port's mast, and every
reading of the field's estimate from those (288 a station: four backgrounds, 4 to 36 sectors or a smooth fit in the
direction, with or without speed and rain, the valid hours kept or not) files the three. The easy answer, TH5 and TH6,
comes from an easy method on the same literal estimand (the lost days scaled as ordinary days), never from another
reading: every row of the fork table files the three.

## Oracles

None for the call: no earlier year's PM10 counts, published 2027 result or station ranking ships; last year's NO2
table counts no PM10 day, and the background map gives modelled annual means on 1 km squares, which no count ties to.
For the asks, last year's NO2 table differs from 2027 by more than the device moves any station (it scores no basis),
and the plan's 200 mg/m² action level ties to no period.

## Ask sheet

**Ask A, each council NO2 station's 2027 annual mean, µg/m³ to one decimal** (6 figures). H18: a measure each council
station carries for the same audit sign-off (the request: "Marc also checks two other figures for each site at the
audit"); the call reads no NO2 row. Primary device D3 (units set per date): the new data loggers fitted on the council
technician's June rounds convert NO2 and NOx from ppb at 1.88 µg/m³ per ppb, their default, so from each station's
fitting the export is 1.6 per cent low against the procedure's 1.91 (section 5.3); only the service log's logger lines
say so, and nothing in the export moves. Hazards: a week of two stations' hours imported twice from the analyser's
store (D1, exact repeats), the NOx rows beside the NO2 rows (D5). Path: the export, the service log and the procedure (3 files, 11 columns: site_code, pollutant, date, time_end, value, status; the log's Date, Time (UK clock),
Site, Type, Notes). Stops: the export as it stands -0.25 to -0.13 (all six missed); every hour rescaled +0.12 to +0.21
(all six); the re-sent week kept +0.00 to +0.11 (moves TH2 and TH5). Realism: a telemetry upgrade fitting loggers with
the supplier's 25 C default is a common source of a 1 to 2 per cent NO2 bias that ratification misses.

**Ask B, each terminal gauge's 2027 dust deposition rate, mg/m² per day, whole number** (5 figures). H18: a measure
each terminal station carries for the same audit; the call reads no deposit result. Primary device D2 (an attribute at
the wrong vintage): the gauges became Frisbee gauges with a 227 mm collecting diameter (0.0405 m²) at the 7 June
exchange, while the laboratory's sheet keeps the funnel gauge's 0.0731 m² and divides by it, so its rates and anything
recomputed from its area column run 45 per cent low from June; the plan's Annex A gives the gauge, the service log the
exchange it was fitted at, and neither alone dates the change. Hazards: the exposure periods across the year end
(periods that started in 2027, plan section 3; D8), the void period at East Berth (D4). Path: the laboratory's sheet,
the plan, the service log, the register (4 files, 12 columns: Site, Date on, Date off, Days exposed, Total deposit (mg),
Collecting area (m2), Deposition rate, Remarks; the log's Date, Site, Type, Notes). Stops: the laboratory's rates
-18.2 to -11.2 (all five missed); its area throughout -18.2 to -11.3 (all five); the Frisbee area throughout +17.0 to
+22.6 (all five); periods that ended in 2027 -3.2 to +1.2 (four of five); the void period's days kept -4.7 (East Berth).
Realism: laboratories key a gauge's collecting area once and keep it, and a gauge change is recorded where the
technician works, not where the laboratory reads.

Main population zero-counts: the call reads the PM10 rows of the export, the terminal's workbook, the mast and the
register; no NO2 or NOx row, deposit result, logger line or plan sentence is among them (S1 asserted, the call computed
from the PM10 rows alone), and no re-sent block falls at a plume station.

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the loggers' 1.88 from June (D3) | A | -0.25 |
| every hour rescaled (D3 over-correction) | A | +0.21 |
| the week imported twice (D1) | A | +0.11 |
| the laboratory's area kept (D2) | B | -18.2 |
| the Frisbee area on every period (D2 over-correction) | B | +22.6 |
| periods ending in 2027 (D8) | B | -3.2 |
| the void period's days kept (D4) | B | -4.7 |

Referee: the service log for the loggers' conversion and the gauge exchange; the plan's Annex A for the gauge.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, TH1, TH2, TH3 | exact repeats dropped, valid hours, the export taken as the procedure's 20 C basis | miss |
| Ask A, TH4, TH5, TH6 | the same | miss |
| Ask B, North Gate, East Berth, Rail Sidings | periods started in 2027, void out, days-weighted, total over the laboratory's collecting area | miss |
| Ask B, South Yard, West Gate | the same | miss |

Measured by: generator/pair.py on the cut pack (target.zip 7987c653, re-measured at the 10-31 repair): the cracker keeps 0 of the 11 ask figures (also 0 taking the
laboratory's rates, 0 putting the Frisbee area on every period, 0 rescaling every NO2 hour); the mirror (stopped at the
scaled count) keeps 0 of 11, Ls 0, and 15.4 of the 38 recommendation points (7 of 12 notes, 6 of 12 whole-year counts
inside the accepted range).

Pair ceiling: 33.7 ((38 + 7 + 55 x 0) and (15.4 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each station's count of days above the PM10 24-hour objective over the whole year, the
   lost days rebuilt from the network's background and the station's own response to the wind on its bearing to the
   terminal; with hospital wards or megawatt-hours in place of stations and PM10 there is no source on a bearing, no
   wind and no pollution rose, and the task stops making sense.
2. Two layers: Layer 1 (two operators' layouts and clocks, the clock changes' repeated and missing hours, status
   codes, the 18-hour rule, calm and missing mast hours, NO2 and NOx in one export) is neutral on the call: every
   handling keeps the three or is loudly wrong (SF1 to SF16, L1 rows; reading the terminal's clock an hour off keeps
   the call). Layer 2 is the rebuild conditioned on the wind, asserted alone to move the default path to the golden on
   the simulator's clean truth (R3).
3. No banned stump decides: nothing is planted (no count, earlier assessment or ranking ships, and no filed sentence
   ties a stop to the dust or the wind, R3c); not semantics (every field read right, scaling still files TH5 and TH6);
   not rule application (the procedure files the estimand and the note and no way of estimating a lost day).
4. Gate G: no shipped artifact ranks the stations; the two distractors count no PM10 days.
5. Determinism: the three hold under all 288 readings a station (40 or more) and the other nine at 33 or under; each
   whole-year count is graded inside its accepted range (the readings' range a day either side), every station on
   its own side of 35; NO2 figures at least 0.034 and deposition at least 0.16 from a rounding edge; 16 fork rows
   asserted; the verifier recomputes the call by its own route (the clock through the London time zone) and reads back
   every format; two builds byte-identical.
6. Fingerprint: heart PASS (test.same_puzzle_older NOTE, differentiated against task265); nearest driver task182 v1
   (lineage) at 0.08; surface: the analyst who writes the goldens added to the card's people.
7. Judge (one isolated thread a pass, Sonnet, medium, the bundle and the graded blocks only). Pass 1 on the first cut:
   DETERMINISTIC, APPROVE; all 12 whole-year counts and both asks reproduced exactly; its notes (the method open but
   forced by the data, its own grid one under an accepted range, 102 against 103 wind days) were taken with the
   reader's findings in one generator pass: the 4-sector rebuild joined the readings, each accepted range widened by a
   day, the wind days counted on reported directions only. Pass 2 on the shipped bundle: DETERMINISTIC, APPROVE; every
   figure reproduced (all 12 counts, the wind evidence, NO2, deposition), 80 rebuild variants inside the accepted
   ranges; Gate G method_or_model_selection, analytical_non_defect; Gate H domain, layers and decisive step pass. Its
   one note: a ratio rebuild from Town Hall or Grangefield alone puts Market Street at 36 or 40, which the data's own
   back-test refutes (that ratio predicts 35 valid-day exceedances at Market Street against the 24 recorded).

## Leak check

`leak.py --asof 2028-03-17`: REVIEW, no LEAK. Each REVIEW line:
- Sweep 3 and sweep 5, the procedure (`tbc_aq_network_qaqc_procedure_v4.pdf`): it carries the call's vocabulary and
  section 5.2's definition of the note, because the note is its own subject; it names no station, no count and no way
  of estimating a lost day. A governing clause that would exist without the build. Harmless.
- Sweep 4, last year's NO2 table and the procedure (the dictionary and the README withdrawn at the 10-31 repair): the shared terms are the field's nouns
  (network, record, monitoring, background, source, concentration); none names the wind, the bearing, a rebuild or the
  plume, and R3c in checks.py asserts that no filed sentence ties a stop to the dust or the wind. Harmless.
- Sweep 6, the service log, the deposit results, the terminal's workbook, the council's export and the procedure's
  Annex A: the records and the station list name the stations beside their readings, visits and analysers; none
  counts days above 50 or ranks the stations on the note. Harmless.

Reader, three reads (one isolated agent each, Sonnet, medium, the prompt and the pack only):
- Read 1 (the first cut): Q2 to Q4 none; it read section 5.1 as the move and found it ambiguous (a lost day with no
  daily mean could count as an exceedance or as nothing), and found Market Street's NO2 capture under 75 per cent once
  its analyser went off with the works, which last year's table implies would be annualised. Fixed in one generator
  pass: section 5.1 now says a lost day counts if the concentration at the station that day exceeded 50, and not
  otherwise (the estimand, filed; nothing on how to know it); Market Street's NO2 analyser stays running through the
  works; section 2.2 says the terminal's statuses are ratified on the procedure's terms. Its realism
  notes were taken: the procedure gained document control, a calibration section, a station annex and a history; the
  service log's notes vary; the deposit cells are numbers; the terminal's quarterly sheets split on its own clock.
- Read 2 (after the fix): Q1 none beyond the estimand ("Nothing says to estimate those days ... it does not say how
  to find the no-data days' concentrations"), Q2 to Q4 none, Q5 section 5.1 fixes the estimand and leaves the method
  open (the design: the data separate the methods), Q6 an analytical choice. Every REVIEW line harmless; section 5.2 a
  "low severity" note on the call's shape, the stated criterion and not the stump. Its realism note on the register's
  tidy offsets from the stockyard was taken: the register now gives Ordnance Survey grid references with surveyed
  scatter, the background map sits on national grid squares, and the plan gives the stockyard's grid reference.
- Read 3 (the final pack): Q1 none ("No sentence names it ... It does not say what to do about them"), Q2 none, Q3 none
  (the background map a mild candidate, an ordinary ASR input and a named distractor), Q4 none, Q5 section 5.1 closes
  the population and window and leaves the lost days' estimate open (the design), Q6 an analytical choice; every REVIEW
  line harmless. Its remaining realism notes are kept as they are: the alarm lines are the logger's own text and
  repeat by nature, and the technicians' calibration lines are their boilerplate; the exchange pattern and the one
  void period are the laboratory's.


## Tried and rejected

- A regional-dust design in a Spanish network (every station sees the same Saharan intrusions, the golden filling each
  station's lost days from the other stations that day): rejected at the draw; filling lost days from correlated
  stations is the generic imputation reflex and would land the call, and the pack's working documents would be in
  Spanish.
- TEOM stops driven by cumulative filter loading since the last filter change: rejected in prototype; the stops fell on
  ordinary days as often as on plume days, so the losses carried little information and interpolation in time
  recovered most of the lost exceedances.
- A daily plume with a narrow, speed-sensitive kernel: rejected in prototype; a station's valid days on its bearing were
  too weak to predict its lost plume days, so the wind-aware rebuild itself fell under 36 for two stations.
- Wind regimes lasting two days or more, faults tripping on any rise past 60 and eight hours rejected before a fault:
  rejected in build; the gaps sat inside multi-day plume episodes, so interpolating the short gaps in time and filling
  the two long outages from the network landed the call for any gap limit from 72 hours up.
- Faults tripping only on the plume's arrival from clean air: rejected in prototype; trips were too rare (3 to 13 a
  year) and the plume stations measured their own exceedances.
- East Berth as a plume station (its plume on the 270 degree westerlies): rejected in tuning; its plume rides the
  prevailing winds, so its plume days run together and interpolation in time or the network recovered them under every
  fault draw; it stays a clear station and the call is three stations.
- Independent hourly wind scatter (22 degrees) with regimes switching at midnight: rejected in checks; reading the
  terminal's clock one hour off moved North Gate and South Yard under 35, so the call hung on a Layer 1 reading. The
  scatter now persists from hour to hour and a change of regime veers over a few hours.
- 2026-10-31, the README and the data dictionary: withdrawn at the batch 1 repair (files describing the data; the
  dictionary listed every column of the met mast's file); the clocks, the status codes and the daily-mean rule are the
  procedure's (sections 2 and 3) and the operator workbook's, the dust plan's and the service log's own notes.
- 2026-10-31, the prompt naming the stations (the council's seven and the terminal's five) in a which-form question: the
  counts withdrawn and the question asked in the whether form (which is over its corpus cap); the metadata's subdomain,
  which named the rebuild from the background and the wind, now says what the task decides.
