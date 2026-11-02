# task204, Carvale Police Service: how many series teams the summer plan needs

Architecture v2, drawn 2026-11-02 under the Batch 3 re-root. Architecture 1 (indoor air in an Irish
further-education block) shipped 2026-10-27 with no portal result; its world is closed and its record sits in
`## Architecture 1 record` below. Every figure in this note is a measurement on the cut pack, printed by
`generator/checks.py` (104 checks), `generator/verify.py` (13 claims, its own code path, bundle only) and
`generator/ceiling.py`, from a generator that rebuilds to byte-identical output twice over.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task204.json`, registered 2026-11-02 (`guard.py check`: WARN only, no BLOCK), checked again on the registered card as the last act of the draw |
| Domain / task type | `criminology-justice` (client domain), task type `crime-incidence-hotspot-analysis`, which serves anomaly-detection |
| Objective | Anomaly Detection & Diagnostics: a spring rise in phone robberies and thefts from the person; the diagnosis is which offender groups generate it, and the call is how many series teams the summer plan stands up and on what ground |
| Prompt shape | `07`, grid of cells: each team with its ground and series count, ten districts by three periods, nine stations by two measures |
| Decision type / answer unit | `designation_set` / `count`: the number of teams and each team's set of patrol districts |
| Gap / generators | `population` then `time`; `G7`, `G10`, `G2` |
| Gate G mechanism | `decomposition_attribution`: offences attributed to the groups behind them; no shipped artifact ranks groups or states a count |
| Strategy / Layer 2 | `identity_resolution` (the offender group resolved across station clusters through the scheduled trip, never a key); `estimand_identification`, pattern `own:offender-series-linked-along-the-line-by-the-train-trip-each-snatch-sits-on` |
| Calibration organ | none; no corpus, twin pair or colleague voice carries the call |
| Context artifact | `operations_log`: the transit peace officers' occurrence log, which answers its own question (what transit officers handled) correctly |
| World | Canada, Alberta, the fictional city of Carvale: Carvale Police Service (Crime Analysis Unit) and Carvale Transit's two-line light rail. Personas from `guard.py names --geo canada --locale en_CA`, seeds 204 and 2041, never typed: Emily Wagner (Deputy Chief, Operations), Joel Jackson (CAU supervisor), Steven House (Transit Security Operations), Kristin Weber (directive owner) |
| Forum / forcing event / org | `executive_team` / `budget_or_appropriation` (the summer deployment plan, signed 28 May with the seasonal overtime allocation that funds series teams, OPS-41 section 6) / `local_government` |
| Spine | `rms_occurrence_extract_20260511.csv`, 27,127 rows, one police occurrence of any type, 2 Feb to 11 May 2025 and 2 Feb to 10 May 2026 |
| Deliverables | `series_assessment_2026.xlsx`, `summer_series_deployment_memo.docx` |
| Fiction as-of | 15 May 2026 (assessment dated 4 May, extract pulled 11 May, files exported 15 May, plan signed 28 May) |

**Candidates screened at the draw** (each dropped one has its line in `## Tried and rejected`):

| # | Candidate | Verdict |
|---|---|---|
| 1 | A storm overflow's spill count judged against the typical-year rainfall series | dropped: the count turns on the filed block-counting rule, so the decisive step is rule application once the rule is filed |
| 2 | Wastewater surveillance of a respiratory virus normalised by the population present | dropped: the decisive step is a choice of normaliser, an estimator grouping that shows in the fit or forks (`stumping` 1.1c) |
| 3 | A pharmacovigilance signal inflated by time since launch | dropped: pharmacovigilance signal refinement is spent on this objective (task180 architecture 3) and the launch-age correction is a named reflex |
| 4 | Monitoring sampled more often after a high reading | dropped: the detection-by-design family is spent here (task180 architecture 4, task189) |
| 5 | Energy not supplied on a distribution network's interrupted feeders | dropped: the grid-reliability cards (task187, task197) hold the objective's recent draws and the pre-fault profile is a filed method |
| 6 | Spatial declustering of preferentially placed monitors | dropped: the weighting is an estimator choice with no deciding configuration in the record, and the monitor's location is a column |
| 7 | Offence series behind a spring robbery rise, linked along a light-rail line (seed AD27's world, decision and quantity only) | drawn |

**Data-native sentence.** Carvale's travelling group rides a published timetable, so its snatches sit on the
scheduled departures of single westbound trains at stations 1.5 km or more apart, and the field's linkage,
which measures the separation between offences in straight-line metres and days, can only see one group per
station: the relation that ties the group together sits in the timetable, at the minute grain of the 911 calls.

**Abstraction sentence (the card's driver).** The units that decide the count are groups behind the events,
and one group travels along a fixed network on a published schedule, so its events sit at the network's own
departure times in sequence along the route; linkage by straight-line distance and elapsed time splits that
group into one local cluster at each place it strikes, and only placing each event on the scheduled trip
leaving its place recovers one group across several areas.

**Sources.** A fully constructed operating layer, every file declared synthetic (CC0) with source, date and
role in `metadata.json`. The formats are the real ones: the GTFS reference (stops, trips with blocks,
stop_times, frequencies with exact times, calendar, calendar_dates), UTM zone 12N on NAD83 (EPSG:26912),
America/Edmonton daylight saving (9 March 2025, 8 March 2026), Alberta's Family Day and Good Friday. No public
spine: offence-grain police records with coordinates are not published.

**Guard answers.** `guard.py recent`, `coverage` and `mechanisms --objective anomaly-detection` read before the
draw; `forum`, `forcing_event`, `org_family` and the stump strategy clear of the last three builds (task185, task459, task178); task186 (airport screeners) and
task185 kept at distance on world, task type and driver; `guard.py check` WARN only and `register` done; the
re-check on the registered card is the draw's last act.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, every field read
correctly, both logs deduplicated, every clock on Mountain time and every filed rule applied.

1. From `rms_occurrence_extract_20260511.csv` take ROB-PERS and THFT-PERS with a phone in `property_taken`,
   `occurred_from_local` 9 February to 3 May 2026, and add the transit log's reports not already filed
   (OPS-41 section 2, one offence); keep the 99 offences with two or more suspects (section 3).
2. Link them the way crime linkage analysis does by default: the same MO code, overlapping suspect age
   ranges, within 1 km and 28 days of each other; a linked set of three or more is a series (section 3).
3. Put each series' offences in the 2026 patrol districts of `patrol_districts_2026.geojson` and give each
   series one team whose ground is every district holding one of its offences (section 4).

- **Ends on:** seven series teams (7): Hollin (district 5, 18), Cobb Street (district 8, 16), the district 6
  street group (14), Ashford Road (district 7, 13), Millbrook (district 6, 11), Ridgeview (district 9, 11) and
  Union Yards (district 4, 5).
- **Golden:** four series teams (4): the Eastline group on districts 4, 6, 7 and 9 (42), the Hollin station
  group on district 5 (18), the Cobb Street station group on district 8 (16) and the district 6 street robbery
  group (14).

## Stump sentence

A competent solver links the twelve weeks' phone offences the way crime linkage does by default, on method,
suspect description, straight-line distance and elapsed time, and files seven series teams (7), one at each
of the four Eastline platforms the travelling group works plus Cobb Street, Hollin and the district 6 street
group; the step that lands them there is measuring the separation between the travelling group's snatches in
metres and days instead of along the line, on the westbound train trip each snatch sits on, which joins
Ridgeview, Ashford Road, Millbrook and Union Yards into one group of 42 across four districts and leaves Cobb
Street, struck within three minutes of Union Yards on four evenings, a separate group.

## Three rules

- **Task type:** `crime-incidence-hotspot-analysis` in criminology-justice, the cell whose object is where
  and by whom a rise in crime is generated, which serves anomaly-detection.
- **Domain test:** the deciding quantity is the set of offence series behind the rise, which crime linkage
  analysis recovers from behavioural similarity and from the distance and elapsed time between offences;
  OPS-41 turns the series into teams and grounds.
- **Swap:** with a hospital's nouns ("how many infection-control teams for the transmission clusters behind
  the spring rise, and which wards should each cover") the offender group, the MO code and suspect descriptions
  the linkage runs on vanish and a published train timetable explains nothing, so the task does not read the
  same.
- **Layer 1:** the police records system and the transit officers' log hold overlapping reports of the same
  offences (file numbers, referrals left without a number); the transit log is stamped in UTC across the
  8 March 2026 change; fare-gate codes were reissued on 29 March 2026 while the gate arrays kept their ids and
  the code list is current only; the 1 January 2026 district realignment leaves 2025 rows on the old layout;
  the GTFS feed has two service periods, holiday swaps in calendar_dates, frequency templates and trips past
  24:00:00; the directive and station reference are PDF tables; station names are spelled three ways. Each is
  produced by the organisation's own systems and none moves the call (`checks.py` R2 rows).
- **Layer 2:** estimand identification: the unit that decides is the offender group, and the methodological
  choice that flips the call is the proximity measure that joins offences into series, straight-line distance
  and elapsed time against position on the network's scheduled trips.
- **Decisive step:** placing each platform offence on the scheduled train trips leaving its station within
  minutes of the call, and joining offences at different stations that sit on the same trip, so a travelling
  group's series spans every station it rides through.
- **Not semantics:** with every field (MO code, suspects, ages, coordinates, district, location text, every
  GTFS column) read correctly and both logs deduplicated, the field's linkage still files seven teams on the
  generator's clean truth (R3a); no field, code or definition carries the trip relation.
- **Not rule application:** OPS-41 defines group, series, period and ground and performs no joining of
  offences, so executing every filed rule on the field's linkage files seven. Enumerated family on the cut
  pack: 3 to 14 teams over 24 distance and time settings (7 at 400 m to 2 km and 14 to 90 days, 8 at 250 m,
  14 at 7 days, 3 unbounded), 6 one per district, 3 for the corridor merge; standing family (no filed sentence
  refutes it): 3, 4, 6 and 7 teams, a spread of four; what rules out 3, 6 and 7 is the timetable read at
  minute grain, silent (no sentence names a train, a trip or a distance), and for 3 the four evenings Cobb
  Street and Union Yards were struck within three minutes.
- **Analyst test:** with both logs deduplicated, every clock on Mountain time and OPS-41 read correctly, a
  strong analyst links on MO, description, 1 km and 28 days, gets seven series and files seven teams; yes,
  the easy analysis files the wrong count and the wrong grounds.
- **Estimand:** OPS-41 (`ops41_series_crime_response_directive.pdf`) sections 2 to 4 file the population
  (ROB-PERS and THFT-PERS with a mobile phone taken, reported to either body, counted once), the unit (an
  offender group, two or more people who offend together; a series, three or more of its offences), the window
  (the twelve completed weeks before the 4 May assessment, which the prompt states) and the ground (every
  2026 district where an offence of the series took place).
- **No decoy:** nothing is planted to be caught: no memo, briefing, prior assessment or stakeholder figure
  states a team count or ranks groups; the planning note asks for the assessment and two tables; the dealer
  returns and the school calendar are honest distractors.
- **No certified replay:** no certified or published figure exists to reproduce; no past series assessment,
  linked-series list or analyst workbook ships.
- **Lesson:** a model learns that a group moving on a fixed network is near in network time rather than in
  straight-line distance, and that a city's published timetable is evidence of who offended together; no
  build on file joins events through a scheduled trip (`guard.py heart`).

## Survivor anatomy

- **Actor:** the offender group has no column: offences carry MO, suspects, ages, coordinates and location
  text, and which group committed them is a relation between rows (two offences on one trip) that no file
  stores; the trip itself is a minute-grain match away, not a key.
- **Link:** offence time and station against scheduled departures in `gtfs/stop_times.txt`, expanded by
  `frequencies.txt` and `calendar_dates.txt`; the RMS has no trip field, its location text differs from the
  GTFS stop names, and no clause names both sides.
- **Reflex:** the field's linkage on MO, description, distance and time sits at rung 0 and files seven; one
  team per district holding a series (rung 1) files six.
- **Back-test:** the textbook route validates: each station series is behaviourally uniform, sits within
  60 m of its platform and runs without a gap past the linkage window, and the recorded districts, the
  boundaries and the station reference agree on every offence (SF4), so the seven series look clean.
- **Second use:** the GTFS feed ships for Transit's ask (scheduled Eastline train calls per station), the
  fare-gate files for the entries ask and the 2025 code bridge, the code list for station names; delete the
  decisive step and every file keeps its ask.
- **Shock:** the rise is spread over six districts and reads as ordinary local series: the travelling group's
  busiest station (Ashford Road, 13) is not the largest series (Hollin, 18), and no sort of stations by count,
  districts by rise or offences by hour isolates its four stations (district 6 holds one of them and the
  street group).
- **Pins:** OPS-41 files scope, group, series, window and ground in the directive's own genre; no filed
  sentence names a train, trip, timetable, distance, linkage window or method (R3c asserts the decoded text).

## Readability screen

Tests: 1 the property is a column; 2 a shared key or one join reaches it; 3 the field's reflex reaches it;
4 a shipped sentence names it; 5 the hygiene battery performs it; 6 a sort on one statistic isolates it;
7 a file exists only for it.

| Rung | T1 | T2 | T3 | T4 | T5 | T6 | T7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the field's linkage (MO, description, 1 km, 28 days) | no | no | yes | no | no | no | no | readable |
| R1 one team per district holding a series | no | yes | yes | yes (section 4) | no | yes | no | readable |
| R2 corridor merge of same-line platform series | no | no | no | no | no | no | no | readable |
| Golden (decisive): offences on the same scheduled trip at different stations | no | no | no | no | no | no | no | silent |

R2 is marked readable because a solver who notices the four Eastline stations share the snatch method reaches
it by merging on the line field of the station reference; it files three, and the four simultaneous evenings
refute it.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | offender group | two or more suspects | lone offenders linked too | many more series | OPS-41 section 3, "two or more people who commit offences together" |
| SF2 | series | three or more offences | two or more | same call (the one locally linked pair sits inside the Eastline group) | same call |
| SF3 | in the review period | occurred_from_local in 9 Feb to 3 May | reported_local in the window | same call | same call; section 4, "took place" |
| SF4 | patrol district | 2026 layout from coordinates | recorded `patrol_district`; station reference | same call (all three agree on every series offence) | same call |
| SF5 | a phone was taken | phone among the property taken | phone the only property | series lose offences | section 2, "in which a mobile phone was taken" |
| SF6 | reported to both is one offence | matched once | counted twice | same call (series offences are in the RMS only) | same call |
| SF7 | a team's ground | every district holding an offence of the series | the busiest district | Eastline ground shrinks to one | section 4, "every patrol district in which an offence ... took place" |
| SF8 | the offence's time | occurred_from | occurred_to | same call (equal on every series offence) | same call |
| SF9 | on the same trip | departure within 3 minutes | 1.5 to 5 minutes | same call | same call |
| SF10 | the field's linkage settings | 1 km, 28 days, MO and ages | 400 m to 2 km, 14 to 90 days, with or without ages | same call with the trip step | same call |
| SF11 | trip direction | either direction | westbound only | same call (the same 18 trips) | same call |
| SF12 | behind the spring rise | every group with a series in the period | only groups in districts that rose | same call (every ground district rose against 2025) | same call |
| SF13 | stand-down (section 6) | not applicable | a charged series stands down | same call (every series offence open) | same call |
| SF14 | the twelve weeks | 9 Feb to 3 May 2026 | another twelve-week reading | same call | the prompt and section 3 give one window |
| SF15 | transit-only reports | placed by station, one suspect | left out | same call | same call |
| SF16 | offence codes | ROB-PERS and THFT-PERS | any code with a phone taken | same call (no other code holds a described group record) | section 2 |
| SF17 | a team per group | one team per offender group | one per series | same call (each group holds one series) | same call |

Every row is asserted under its id in `generator/checks.py`.

## Ladder

| Rung | Construction | Teams | Grounds (offences) |
|---|---|---|---|
| R0, default | the field's linkage: MO, overlapping ages, 1 km, 28 days | 7 | 5 (18), 8 (16), 6 (14), 7 (13), 6 (11), 9 (11), 4 (5) |
| R1 | one team per district holding a series | 6 | 4 (5), 5 (18), 6 (25), 7 (13), 8 (16), 9 (11) |
| R2 | every same-line platform series merged (corridor) | 3 | 4, 6, 7, 8 and 9 (58), 5 (18), 6 (14) |
| Golden, decisive | R0 plus offences at different stations on the same scheduled trip | 4 | 4, 6, 7 and 9 (42), 5 (18), 8 (16), 6 (14) |

The corrections walk 7, 6, 3 and only the decisive step turns back to 4. Eighteen westbound trips carry two or
three of the Eastline group's offences each. C1 families, all asserted: the golden is exact under 84 linkage
settings (400 m to 2 km, 14 to 90 days, with or without the age test) and trip windows of 1.5 to 5 minutes;
R0 is seven and R2 three across the same settings; on the clean truth none of 35 distance, time and corridor
settings files the golden (F-cheap).

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | ROB-PERS and THFT-PERS with a phone taken, either body, once (section 2) | filed; SF5, SF6, SF16 asserted |
| 2 Unit of account | the offender group (section 3) and its series | filed; SF1, SF17 |
| 3 Attribution window | occurred time in 9 Feb to 3 May 2026 | filed by section 4 and the prompt; SF3 asserted C1 |
| 4 As-of dating | the 4 May assessment, 2026 layout | filed (section 3, patrol district) |
| 5 Version basis | the current code list against the code in force on the day | C1 for the call (R2-codes); ask device only |
| 6 Denominator | none: counts | not applicable, nothing divides |
| 7 Weighting | none | not applicable |
| 8 Window length | linkage window 14 to 90 days | C1 (SF10) |
| 9 Boundary inclusivity | trip window and linkage radius edges | C1, nothing near an edge (SF9, SF10) |
| 10 Rounding path | whole counts | the prompt: every count a whole number |
| 11 Tie-break | none arises | not applicable |
| 12 Maturity and censoring | offences reported after 3 May but occurring before | C1 (SF3) |
| 13 Order of operations | deduplicate, link, place | C1: the dedup leaves series unchanged (SF6) |
| 14 Row order | union-find over pairs | C1, order-free by construction |
| 15 Duplicate resolution | a report in both systems | filed (section 2) and C1 (SF6) |
| 16 Identity normalisation | station names three ways | the station reference and stop names resolve every location text (R2-names) |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | metres in EPSG:26912, degrees in stops.txt | C1 (R2-crs) |
| 19 Code and status semantics | MO codes, clearance status, gate codes | C1 (SF13, R2-codes); never the stump |
| 20 Integerisation | counts are whole | not applicable |
| 21 Clause scope | section 6 stand-down | C1 (SF13) |
| 22 Forward window contents | the summer plan's window holds no data | not applicable: the call is the team set the plan funds from the review period |

## Literal reader

Executing the prompt and OPS-41 word for word: the population is section 2's, the unit section 3's, the window
the prompt's (equal to section 3's), the ground section 4's. The only thing the text leaves open is how
offences are joined into series, which is method, not estimand. Every licensed reading of the open conventions
(SF2, SF3, SF4, SF6, SF8 to SF12, SF15, SF17) files the golden, asserted; the three that differ (SF1, SF5,
SF7) each violate a quoted sentence. The default path is the same literal estimand executed with the easy
method. For the asks, the planning note files the 2025 window (10 February to 4 May 2025), the occurrence
date ("took place") and the current layout; "train calls" counts every scheduled stop of an Eastline train,
and no Sunday service runs past midnight, so clock and service-date readings agree (A7).

## Oracles

No oracle ships. No file states a series, a group or a trip for an offence (R1 asserts the columns); no
document ranks groups or names a count (R3c-note); the station reference and the boundaries agree with the
recorded districts, so no cross-check ties only under the golden. The simultaneous evenings are a fact a
solver must find by comparing times across stations; nothing reports them. For the asks, no control total
ties only under the golden: the code list is current only, and the 2025 daily summary carries codes and arrays
without saying a reissue happened.

## Ask sheet

Asks (the prompt's grid; 48 ask figures beside the call's count, four grounds and four series counts):

1. **2025 by district (30 figures):** each 2026 district's phone offences that took place 10 February to
   4 May 2025, by four-week period. Devices: the transit log's 2025 station codes are the codes before the
   29 March 2026 reissue, the code list is current only and the bridge is the gate array id in
   `fare_gate_daily_summary_2025.csv` (D7, a reissued key with a false-clean join); 2025 RMS rows carry the
   2025 layout's districts (re-district by coordinates, filed by the note's "current district layout");
   referrals without a file number (D1); UTC stamps (D8).
2. **Entries per Eastline station (9 figures):** the same reissue in `fare_gate_entries_hourly_2026.csv`
   (codes move to other stations on 29 March, arrays keep their ids) and UTC hours read onto Mountain dates.
3. **Scheduled Eastline train calls per station (9 figures):** frequency templates (one stop_times trip
   stands for every departure in its band) and Family Day and Good Friday running Sunday service.

| Ask block | Figures | Device | Cracker's route | Cracker |
|---|---|---|---|---|
| Ask 1, cells reached by transit-only 2025 reports at reissued codes | 11 | codes reissued, arrays keep ids | codes read on the current list | miss |
| Ask 2, entries at stations whose codes moved or that opened | 6 | the same reissue in the hourly file | gate code read on the current list | miss |
| Ask 3, every station's train calls | 9 | frequency templates; holiday swaps | stop_times rows with the calendar | miss |

The cracker keeps the 19 cells of ask 1 and the 3 entries no device reaches: 22 of 48 ask figures, 0.458 of
ask weight, landing at 70.2. The full includer keeps 0.8125. The mirror (the default path's own handling)
keeps 5 of 48 and lands at 17.7.

- **Pair ceiling:** 44.0 (70.2 and 17.7); 60.5 if both landed the call, which the ladder keeps from happening.
- **Mirror leakage:** 10.4 per cent of ask weight.
- **Measured by:** `generator/ceiling.py` on the cut pack (`generator/ceiling.json`).

## Architecture 1 record

Architecture v1, drawn 2026-10-27, shipped 2026-10-27, no portal result. Domain
`physical-environmental-sciences`, task type `environmental-monitoring-exceedance`, objective
anomaly-detection, shape `07`, decision `quantity_figure`. World: Beldarrig ETB's Kilmoneen Further Education
Campus, Tulrohan Block (Ireland). Call: the block's outdoor-air supply per occupant present against the
8 litres per second per person of TGD-M4, and whether January's minor-works allocation funds the air-handling
replacement or a timetable change. Default path: the steady-state relation on each session's mean carbon
dioxide excess, occupant-weighted, ending on 11.0 (clears the standard). Golden: 5.0 from integrating each
space's unsteady balance across the timetabled sessions (fails it). Stump: reading a concentration still
rising as settled, in spaces whose response time runs 3.5 to 6.5 times a session. Deliverables
`tulrohan_ventilation_assessment.xlsx` and `tulrohan_co2_day_profile.png`. Its leak and determinism reports
are kept beside this note with an `_arch1` suffix.

## Tried and rejected

- Curtailed or inverse sampling (a measurement programme that stops at a filed count of findings), killed
  at the slots screen before any code: task198's note measures the same mechanism (M1) with the naive route
  already naming the golden at 1.301x against the designed route's 1.083x, five of eight reflexes reaching
  it, and the correction reducing to one multiplication by a filed column.
- The non-equilibrium balance read as "the omitted stock term", killed at the abstraction test against
  task120's shipped driver; kept only in the re-rooted form above, where the unknown is the balance's
  transport coefficient and not a residue, with the differentiation line on the card.
- First-order sensor lag with a response-time deconvolution, killed by arithmetic before any code: a
  first-order lag preserves the integral, so a total is untouched, and recovering a peak needs a
  regularisation choice, which is a free parameter.
- Top-truncation of an over-range analyser channel recovered against a conserved register, killed on
  readability test 5: the recovery is the hygiene battery's own reconciliation of the series against the
  register, one group-by and one subtraction.
- Per-case multiplicative corrections on this ground (laboratory recovery factors, calibration drift,
  holding-time decay), killed on the dispersion ceiling: every candidate measured sd(log factor) well under
  1.4, where `stumping` prices the shape as closed.
- Interval placement of an onset against a shipped inspection schedule, killed twice over: the brief's
  closed family names the interval union, and `stumping` 1.1e has already measured the parameter-free
  correction at 0.95 to 0.96 of the golden, which is a lever of five per cent.
- Flow-weighted or diurnally weighted loads and inclusion-probability reweightings, killed on the swap test
  at the sentence, which is where the brief puts it: each reads identically with any field's nouns.
- Stage 3, the ask sheet's figure counts moved and the prompt was rewritten to carry every graded figure.
  At stage 2 the prompt asked for two of the four asks and the write-up would have graded the other two,
  which `determinism-check` section 5 calls an open fork by construction. Ask A now grades the recorded
  occupied hours beside the hours over the indicator, so no cell is empty for a well ventilated room and a
  cracker cannot bank a zero; ask D gained the period, which the day-window path cannot name. Prompt back
  through `voice-check.py` at 997 characters.
- Stage 3, the capital bid sheet's volume column was cut. It made the as-built room data sheets no longer
  the only record of a room's volume, which is the Layer 1 item the card files; the bid sheet now carries
  the as-built sheet reference instead and `checks.py` asserts the volume appears in one file only.
- Stage 3, the scattered sample losses were changed from a per-stamp rate to a counted number of
  teaching-day samples per space. At a rate, four of the fourteen capture shares collided at one decimal
  and the cracker's calendar-day base sat 0.05 of a point away from the golden in six cells; as counts the
  fourteen shares are distinct, each sits within 0.004 of a bin centre, and the cracker misses all
  fourteen by at least 0.79 of a point.
- Stage 3, ask A's hours moved from one decimal to two. An hour count that is a multiple of five minutes
  lands exactly on a one-decimal rounding boundary once every six values, and resting 112 graded figures on
  a filed rounding direction is a fragility the two-decimal report removes: the closest any figure now sits
  to an edge is 0.0017 hours against a half-bin of 0.005.
- Stage 3, the staff school column was derived from the group's own programme rather than drawn. Drawn, it
  produced tutors filed to one school whose every session taught another, which is the defect the measured
  task464 read names.
- Stage 3, the block's response times came out at 189 to 355 minutes, and 191 to 358 after the stage 4
  recut, rather than the 253 to 543 the stage 2
  prototype measured. Raising the six spaces' occupancy and their supply together leaves every
  concentration where it is and only shortens the response time, which is what lifted the peak-sample rung
  off the 1.15x floor; the ratio the stump turns on is unchanged and the note's figures are the cut pack's.
- Stage 4, the per-person population was filed. The leak reader found nothing in the pack choosing
  among the register's roles and marks, which is the shape that spent a sibling build the same day.
  `determinism-check` section 1 requires the population filed, so EST-14 gained section 4; it names
  which persons count and says nothing about how a supply rate is obtained, so the decisive step stays
  an analytical choice. No graded figure moved, because the golden's denominator was already that
  population.
- Stage 4, the chart was renamed from `tulrohan_session_balance.png` to `tulrohan_co2_day_profile.png`
  and the commissioning firm from Westmeath Air Balancing Services to Westmeath Commissioning Services.
  The reader named the word balance in a deliverable's own name as one of the two most pointed hints in
  the pack toward the decisive step. The pack is now swept for that word and its kin by name and by
  content.
- Stage 4, the commissioning engineer and two maintenance technicians were redrawn. They had been
  taken from the campus staff list, so the same person signed an outside firm's commissioning record
  and taught in the building; the three organisations now hold disjoint people.
- Stage 4, the determinism judge returned NOT_DETERMINISTIC on the integration rule, and the close was
  a recut rather than a pin. Procedure note EST-14 section 3's sentence "each logged reading
  represents the five minutes beginning at its timestamp" was written for the occupied-hours and
  monthly returns, and read literally it also licensed two integrations of the session balance, which
  file 4.649 and 5.475. Filing how the balance is integrated would have filed the HOW, which rule 3
  bans as the decisive step, so nothing was pinned: the sentence was scoped in its own words to the
  counting of hours and of readings, and the block's supply rates were scaled by 0.991 to put the
  seven licensed constructions mid-bin. They now span 4.972 to 5.086, 0.227 of a bin, every one
  printing 5.0, with the widest 0.164 from its cell edge against 0.117 before. The fork sat inside the
  decisive step rather than at it: both the trapezoid and the rectangle already carry the stored term,
  and the default path is still the settled read at 11.0, 8.49 bins away.
- Stage 4, the unweighted mean of session rates (5.473) was added to the fork table rather than left
  implicit. It dies to the standard's own reporting clause, which reports the rate over the whole of
  the period assessed rather than for a single group.
- Stage 4, the mail thread's two messages were separated by a rule. Without it the first message's
  sign-off sat directly above the second's From line, and `guard.py surface`'s persona reader took the
  pair as a name, Aileen From, and exited 1 on an undeclared persona. With the separator the reader
  finds Aileen Menton, Benjamin Garavan and Conall Murtagh and the screen exits 0. The thread reads
  better for it, and nothing graded moved.
- Stage 4, `guard.py surface` promotes three pairs for adjudication, task204 against task254, task193
  and task249, every one of them promoted on the same ground: the decisive gap, the decisive pattern
  and the Gate G mechanism collide on the cards. All three are the pairs the card's own
  `differentiation` block was written against at the draw, and `guard.py heart` reports the same
  collision as a NOTE with the nearest driver text at 0.06. The adjudicated `/clone-check` is the
  author's call and is not run here.
- Reporting the requirement as a multiple of the achieved rate (1.59 times). Died at determinism pass 2 on
  Gate A: the shipped rate is rounded to the nearest half by the asking sentence, so a judge recomputing
  8 over 5.0 gets 1.60 while the generator wrote 8 over the unrounded 5.027. Replaced with the shortfall in
  the same unit, 3.0, which prints the same from either, so the write-up's own figure cannot fork on a
  rounding path.
- Closing the block-aggregation fork with a filed sentence in the procedure note (EST-14 section 6, filing
  the quantity a block return reports). Died on the leak read: it was the only section of the note about a
  rate, it sat outside the note's own stated scope, it duplicated the standard, and its closing sentence
  warned against one specific wrong route, so the reader read it as written for whoever had to answer the
  prompt. Taken out and closed by C1 instead, by lifting the two lowest spaces so the worst space's own
  rate prints the block's figure. The lesson is the one the closure table already prefers: C1 before a pin,
  because a pin that answers a real fork can still read as authored.
- Drawing the supply-terminal counts twice, once for the zone assignment sheet and once for the as-built
  room data sheets. Died on the leak read as a planted discrepancy: two systems holding the same asset
  count disagreed with no reason in the world. One draw now serves both.
- Leaving the assessment sheet's third row on the number format the multiple had used. Caught on a read of
  the shipped workbook after the Gate A repair: the cell held the shortfall, 3.0, and would have displayed
  as 3.00x under a label reading litres per second per occupant present. The format is now the rate's own.
  The lesson is that replacing a figure means replacing its presentation too, because a cell format
  outlives the figure it was written for and no assertion on the value sees it.
- Closing the plain-mean-of-session-rates fork with a sentence in the standard's reporting clause, extending
  TGD-M4 4.4 to state the reported quantity as the outdoor air supplied across the period against the
  persons present through it. Died on the leak read for the same reason the EST-14 attempt did, and more
  sharply: the reader called the clause authored ("a real design guide would not write Where a space serves
  groups of different size"), said the trailing gloss tells you which aggregation to use, and answered the
  decisive-step question with "with 4.4 as written, the aggregation is stated for you", which is a rule 3
  finding. Reverted to the clause's own wording. Two attempts at this fork by a filed sentence have now been
  read as authored, and the lesson is a rule rather than an incident: a sentence written to close a fork
  reads as authored whenever it names the situation the task is in, and moving it to a different document
  does not help. What closes a fork without that cost is the records (C1) or, where C1 is arithmetically
  unavailable, the existing clause plus a measured argument from the data, with the residual stated.
- Converging the plain mean with the pooled figure by scaling the supply, the lever that closed the
  space-level fork. Refused on arithmetic before any rebuild: the plain mean sits a factor of 1.0876 above
  the pooled figure and the printed cell is 10 per cent wide, so the two cannot both sit inside it with
  any clearance (landing the mean at 5.2499 puts the pooled figure 0.0770 from the 4.75 edge). Compressing
  the gap instead means cutting the per-session rate variance by about two thirds, which is the day-to-day
  mixing and the trace noise, and a block of teaching spaces whose sessions all behave identically is not
  a record a building produces. Asserted in `checks.py` so the next pass does not retry it.
- Architecture 1 as a whole (the Tulrohan block's outdoor-air supply from an unsteady carbon dioxide
  balance), re-rooted 2026-11-01 at the Batch 3 queue reset after shipping 2026-10-27 with no portal result.
  The indoor-air world is closed, so architecture 2 moves to criminology-justice.
- Draw candidate, a storm overflow's spill count against the typical-year rainfall series: dropped at the
  WHAT screen, because the count turns on the filed block-counting rule and filing it makes the decisive step
  rule application.
- Draw candidate, wastewater surveillance normalised by the population present: dropped on `stumping` 1.1c,
  the choice of normaliser being an estimator grouping that either shows in the fit or forks the answer.
- Draw candidate, a pharmacovigilance signal inflated by time since launch: dropped, the family is spent on
  this objective (task180 architecture 3) and the launch-age correction is a named reflex.
- Draw candidate, monitoring sampled more often after a high reading: dropped, detection by design is spent
  here (task180 architecture 4, task189).
- Draw candidate, energy not supplied on interrupted feeders: dropped, the grid-reliability cards (task187,
  task197) hold the objective's recent draws and the pre-fault load profile is a filed method.
- Draw candidate, spatial declustering of preferentially placed monitors: dropped, the weighting is an
  estimator choice with no deciding configuration in the record and the property is a column.
- Stage 3, joining whole local series through shared trips. Under 14- and 21-day linkage windows the
  Eastline group lost the Union Yards offences that stood alone at their station and fell from 42 to 41, so
  the trip step now joins any two group offences at different stations on the same trip, and every licensed
  window prints the golden.
- Stage 3, the district 6 street group spread over a 450 m radius dropped offences at a 400 to 500 m
  linkage radius; it now spreads over 230 m, and the travelling, Hollin and street groups never pause longer
  than ten, twelve and ten days, so a 14-day window keeps each whole.
- Stage 3, "scheduled departures" for Transit's ask. A train's last stop carries a departure time in
  stop_times, so a literal reader could count terminating rows; the ask now counts train calls, every
  scheduled stop, and three station pairs served by the same trains share their figure honestly.
- Stage 3, Sunday service running past midnight. The window opens and closes on a Sunday night, so clock
  time and service date counted different calls at the edges; Sunday service now ends before midnight and
  the two readings agree (A7).
- Stage 3, the 2025 comparison window. "The same twelve weeks of 2025" read by calendar date and by week
  gives grids a day apart; the planning note now files 10 February to 4 May 2025 and the offences that took
  place in it, which also closes the reported-date reading that moves two cells.
- Stage 3, the code list's revision line said "the Eastline renumbering", which narrated the reissue the
  entries and 2025 asks ride on; it now reads only "Code list revision 14, 30 March 2026".
- Stage 3, eight series offences carried CLEARED-CHARGE at random, which let a literal reader stand a team
  down under section 6. The groups are unidentified, so their offences stay open (SF13).
- Stage 3, the golden memo typed "six evenings" for the Cobb Street and Union Yards coincidences; the figure
  is now emitted from the analysis (four).
- Stage 3, the golden's 2025 grid dropped every transit-only report, because the 2025 summary writes gate
  arrays as GA-1426 and the lookup expected ga1426. Caught by the independent verifier, which normalised the
  id on its own path; the golden now normalises it too.
- Stage 3, background offences were placed at Fairgrounds before it opened on 29 March 2026 and two 2025
  transit reports carried no station code; they now fall at Millbrook, its district's open station, and
  `checks.py` asserts nothing is recorded at Fairgrounds before it opened.
- Stage 3, RMS rows reported after the 11 May pull, and toolchain stamps in the Office containers
  ("generated by python-docx", the spreadsheet library's application name): the extract now holds only what
  was reported by the pull and every container carries the Office application's own properties.
- Stage 3, the card's stump strategy `grain_or_unit` and forcing event `season_or_peak`. Clear at
  registration, both were banned at the re-check on the registered card once task178 v4 took them in the
  window; redrawn to `identity_resolution` (the group resolved across stations through the trip) and
  `budget_or_appropriation` (the plan signs the seasonal overtime allocation), and the prompt's second
  sentence reworded to clear a shell repeat with task304 v5.
