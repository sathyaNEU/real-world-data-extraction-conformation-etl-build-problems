# task191 design note

Architecture 3, drawn 2026-10-31 at the batch 1 re-root: a municipal bus company's forward-collision and pedestrian
warnings, read for the depots whose drivers let genuine warnings pass. Architecture 2 (a knockout-screen world) was
spent at stage 2 with no data cut and architecture 1 (the interconnect worst-window) is kept below as a record.

## Draw

- **Card.** `cards/task191.json`, architecture v3, re-root of the slot in the same objective; architecture 2 moved to
  the card's lineage with its fate beside architecture 1; registered 2026-10-31T19:28:35Z and checked again on the
  registered card: PASS. Redrawn on the way: the first triple (gap population, G2 grain mismatch, designation set)
  BLOCKed `test.same_puzzle` inside the batch against task270 v11 and `test.same_puzzle_older` and
  `test.same_driver_older` against task239, task264 v1, task48 v2, task187, task263 and task279, so the gap and the
  pattern were redrawn rather than differentiated: the decisive gap is objective (the dashboard's no-brake share is
  computed correctly and is not what the programme decides on) and the decisive generator G15 (evidence-standard
  exclusion: a warning that fails the terms' own standard of a genuine warning is set aside), with G2 and G18 behind
  it. First name Santiago (people.first against task151) was replaced from the same draw. The draft's `shell.repeat`
  WARN read architecture 1's prompt, which this commit removes; architecture 3's prompt comes at stage 2. The window
  moved under the draft too: task156 and task130 registered first, which freed classification_error and composition_mix
  and banned forecast_method_backtest, monitoring_export, local_government, council_or_assembly and
  line_manager_or_team, so the context artifact is the programme's filed terms rather than the dashboard export.
- **Pairing.** Human Factors & Ergonomics / safety-incident-error-analysis, a task type the taxonomy tags for Root-Cause
  and Anomaly Detection & Diagnostics; drawn for AD (no AD card on file in the cell). The anomaly is a depot whose
  drivers do not brake on collision warnings that were real; the artifact is a warning the system raises at a fixed
  structure on nearly every pass, where nothing is in the bus's path and not braking is the right response.
- **Niche.** Empresa Municipal de Autobuses de Lorvega runs the city's buses from seven depots. Every bus carries an
  advanced driver-assistance camera that raises a forward-collision warning and a pedestrian and cyclist warning and
  reports each one, with the bus, the position, the speed and whether the brake was applied within two seconds, to the
  telematics platform. The December 2025 network change opened a busway with retractable bollards, sent two corridors
  under a low rail bridge and over a hill road with a tight barriered bend, and moved routes between depots.
- **The call.** Where the 2027 driver-attention programme runs: the depots whose drivers, from January to October
  2026, did not brake on genuine collision warnings at 1.3 times the fleet's rate or more, by the programme's terms
  (a genuine warning is one raised when a vehicle, cyclist or pedestrian was in the bus's path; not braked on means no
  brake application within two seconds; a driver's depot is the depot the driver was assigned to on the day).
- **Shape.** other, written out at stage 2: each depot's genuine warnings, the ones not braked on, its rate and its
  ratio to the fleet's, the fleet's own rate, the depots taken in, the closest depot left out and the chart's parts,
  with the asks beside. Decision designation_set, answer set_of_items, question form where, deliverables
  `attention_programme_depots_2027.docx`, `warning_response_by_depot_2026.xlsx` and
  `genuine_warning_response_2026.svg`.
- **Strategy.** classification_error: the warning file classes every warning as a collision hazard, and at the network's
  new fixed structures that class is wrong on nearly every warning; the misclassified warnings are told apart from the
  busy streets where warnings are real but frequent only by the share of bus passages on which a place fires, from the
  running-time database's passages by link, which no count of warnings at a place carries. This is not the
  misclassification-correction family task242, task192 and task228 spent (a classifier's or an investigator's error
  rates read off a validation panel and inverted): nothing here is inverted and no panel exists; each warning's class is
  settled by its place's share of passes. Gap objective then population; G15 decisive, G2 (the class lives at the
  place-and-pass grain, the warning file at the event grain) and G18 (the over-correction that drops every busy place)
  behind it. Gate G decomposition_attribution (the no-brake share is split between warnings with nothing in the path and
  drivers who let real ones pass). Calibration none. Context artifact filed_standard (the programme's terms of
  reference). Layer 2 family estimand_identification.
- **Forum, event, organisation.** executive_team (the company's management committee approves the programme),
  launch_or_rollout (the programme starts on 11 January 2027), utility_or_infrastructure (a municipal transport
  operator). Role compliance_or_audit (the head of driving safety, who proposes the depots).
- **People** (`guard.py names --geo Spain --seed 191`, locale es_ES): Miriam Vilanova, head of driving safety;
  Paulina Mariño, managing director, who chairs the management committee; Trinidad Arévalo, telematics and
  driver-assistance lead; Baudelio Carballo, scheduling, who keeps the running-time database; Luciana Berrocal, depot
  operations; Pío Roig, driver training. None appears in the prompt.
- **Data-native sentence.** A forward camera that judges time to collision from what it sees ahead fires at a low
  bridge, a line of bollards or a barrier on a tight bend on almost every pass at speed, and drivers who meet that every
  day stop braking for it, which is correct; in a market street a pedestrian really steps into the path on a few passes
  in a hundred, and those warnings are genuine however many of them there are, so only the share of passes on which a
  place fires, read from the passages the scheduling database keeps for running times, tells the two apart.
- **Abstraction sentence.** Each unit's failure to act on alarms is read only on alarms whose trigger was real, and a
  place that raises an alarm on nearly every occasion is told from a place where real hazards cluster only by the share
  of occasions on which it raises one; no approved build on file carries that sentence (task236 reads a capture share
  against an independent sample's volume and positivity, task196 a latent count from two overlapping channels, task119
  each unit's waits through its own free resource, task182 a lagged response to a shared driver, task103 a handed-over
  quantity in standard amounts, task104 the least sensitive paging threshold).
- **Same-puzzle and library tests.** The triple (objective, G15, designation_set) and the driver triple (objective,
  G15, decomposition_attribution) repeat nothing in the last twelve or older, measured by `guard.py check`. The library
  test: the golden is not "use X on Y" with X a named correction; the field's own measure of warning compliance (the
  no-brake share, with nuisance places set aside by how many warnings they raise or how seldom drivers brake there) is
  rung 0 and rung 1, and the decisive step is the recognition that this record breaks its precondition (that a busy
  place or an ignored place is a false one).
- **As-of.** Monday 9 November 2026, the extracts cut on Sunday 1 November; the management committee meets on Tuesday
  24 November 2026.
- **Forward facing.** The call places the 2027 programme; its estimand is each depot's drivers' compliance with
  genuine warnings over January to October 2026, the period the programme's terms read, and the depots are those the
  drivers belong to now. The tag stays Anomaly Detection: no future value is predicted.
- **Sources.** Breznitz 1984 (Cry Wolf: the psychology of false alarms); Bliss 2003 and Bliss and Dunn 2000 (alarm
  reaction patterns and the probability matching of responses to alarm reliability); Dixon, Wickens and McCarley 2007
  (false alarms and misses in diagnostic automation: false alarms reduce compliance); Lees and Lee 2007 (driver response
  to imperfect collision warning systems, nuisance and unnecessary alarms); Regulation (EU) 2019/2144 (the general
  safety regulation's advanced driver-assistance requirements for buses); `guard.py slots` on the mechanism's nouns
  (warning, alarm, false, nuisance, telematics, reliability, compliance) and the setting's (bus, driver, collision,
  passage, running time): no slot holds the mechanism or the setting.

## Architecture 2 record (spent 2026-10-31 at stage 2)

A cancer institute's genome-wide knockout screen of one cell line, read for the line's own dependencies net of the
copy-number cutting effect, drawn and registered 2026-10-31 (commit a0836137) and spent at stage 2 with no data cut:
the previous fork's drafting of the world was interrupted by a safety classifier, and the slot re-rooted to a cell far
from genome editing, laboratory biology and anything dual-use. The card's lineage holds its identity and fate.

## Architecture 1 record (spent 2026-10-31)

Judging the worst of many monitored series when the worst was chosen for being worst.

### Measured refusal

**Architecture 1 is refused on measurement, not redesigned. The decisive step has no estimator
content.** Everything below this section is the record of the refused design and is kept as history;
nothing in it is resumed. The re-root starts at stage 1 with a new draw.

The wave 8 blind reader at medium effort, holding only a fresh unzip of `target.zip`, `prompt.txt`
and the figure names, landed the call (fund no augment, HVT-01 worst at 318 kbps) and took 111 of
119 ask figures. It named the decisive step as comparing each port's worst shortfall against that
port's own non-congested noise level with clause 4.4's evenings removed, quoted clauses 4.2 and 4.4
as what sent it there, and reported a baseline of 330 kbps against the 398 to 489 this note ships.
That divergence is the whole finding, and it was priced before any redesign work was done.

`generator/screen_estimator_family.py ../target` is the harness. It runs on the goldens' own reading
of the pack, prints all three screens and is byte-identical over two runs
(md5 `2b3635593d0488408a01958568840c89`).

**Screen 1, the estimator family clause 4.2 leaves open.** 48 constructions of "the shortfall the
network's own record shows the measurement produces without congestion", computed on the clean
truth. 35 of 48 file the committed hold, 13 file a fund. The spread the family puts on the graded
figures is **0.0 kbps on every one of them**: the decided 318 kbps is a maximum and no reference
enters it, the 21 grid worst-window figures and their dates do not read a reference at all, the
closest interconnect is the same name under all 48, and clause 4.4 fixes the 14 evenings. Only the
binary call moves. The reader's 330.2 kbps is `HVT-01`'s own prior-record 99th percentile, and it
holds; so does the same statistic for all seven interconnects (322.1 to 368.9 kbps against worst
windows of 249 to 318), so the reader's route funds nobody.

**The selection-breadth axis the architecture rests on is not the dial.** The reach this note calls
the only admissible one (the quarterly worst window) holds 10 of 10, and the reach it calls wrong
(the single interconnect's own record) holds 7 of 8. Read off the prior record at any reach the call
holds 34 of 38; read off this quarter at any reach it holds 1 of 10. What decides the call is which
file is opened, `evening_quality_daily.csv` or the quarter's own windows, and clause 4.2 says in its
own words to open the record. Executing a filed sentence is rule application.

**Screen 2, the cheapest licensed construction as algebra.** The designed construction is an exact
identity with one column maximum: max over the eight quarterly worst windows 489.000000000000
against `prior["shortfall"].max()` 489.000000000000, difference **0.000e+00**, because the maximum
of a partition's maxima is the maximum. Slope 1, intercept 0. Seven of the eight draws of the
statistic enter no graded figure, because `golden.compute` reads the eight quarterly maxima only
through `by_q.iloc[0]`. The one-group-by route to the call is one line: subtract the rollup's two
median columns, drop clause 4.4's evenings, take one `idxmax` over all 17,139 kept rows; it lands in
2026Q1 on `RHN-01` at 489 kbps, not in 2027Q1, so fund nothing. A filter and a count file it too:
282 of the 15,330 prior record windows already sit at or above 318 kbps.

**Screen 3, the lever against the ceiling, which is empty by construction.** The ladder needs the
decided figure above the easy route's reference, `HVT-01`'s own 2027Q1 99th percentile at 248.0
kbps. Gate C needs it at or below every licensed reference, and the smallest licensed reference is
that same 248.0 kbps, because the easy route is itself a licensed construction. At the 6 per cent
margin `checks.py` asserts the admissible window is [262.9, 234.0], **empty by 28.9 kbps**. As
shipped the decided figure clears the easy reference by 28.2 per cent and therefore clears the
smallest licensed reference by the same 28.2 per cent, which is the Gate C failure in the same
number as the ladder's margin. The family spread is 264.2 kbps on a graded quantity of 318 kbps, 83
per cent of its own level and 264 printed units wide at the prompt's nearest kbps, and the decision
boundary sits inside it, 2.0 kbps above the nearest licensed reference below and 12.2 kbps below the
nearest above. One dial, both ends the same end: raising the decided figure to clear the easy route
is what carries it past the licensed references that hold, and lowering it under every licensed
reference puts the easy route on the hold as well.

**What the re-root may not reuse.** Not clause 4.2's filed comparison criterion in any wording, not
a reference built as a statistic of a statistic over the same panel (it is an identity with one
column maximum), not a two-year rollup of the same quantity shipped beside the quarter it is
compared with, and not a decisive step whose whole output is a binary while every graded figure is
invariant to it. The pack itself is sound: 153 generator assertions and 168 independent checks are
green on the shipped `target/`, and the refusal is of the design, not of the data.

### Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task191.json`, filed and committed with this note |
| Domain, task type | general-statistics-data-science, `multiple-testing-selective-inference` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 13, scenarios and the flip point |
| Decision | go_hold_or_stop, named_option |
| Gate G | `signal_vs_noise_or_hold`; decisive generator G17, G18 |
| Strategy | `uncertainty_hold` |
| Layer 2 | `forecast_uncertainty`, own pattern `own:null-of-the-selected-maximum` |
| World | Netherlands, video streaming platform, EUR |
| As-of date | 2027-04-12 |
| Guard | registered at PASS; the deciding forum redrawn to the capacity committee after `heart` blocked a board of directors against task263 |

**Data-native sentence.** The figure the augment case is built on is the single worst interconnect
evening of the quarter, picked out of 630 path-evening cells by a monitoring dashboard that reports
only the worst, so the only reference at the same selection is the worst cell of a quarter, and this
panel carries eight earlier quarters of exactly that cell at exactly that selection.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD14: the decision shape only, one capacity upgrade
  funded among candidates that all show an evening shortfall. Its own architecture compares the
  strongest gap against a filed reference band, which is a stated score deciding the call, so the card
  re-roots on the field's treatment of a maximum selected for being largest.
- `guard.py mechanisms --objective anomaly-detection`, read before the draw: the spent drivers there
  are detection delay by route, a reporter not yet filed, a check that sees a unit before it resets,
  and a yield carried onto a different base rate. None of them is a selection effect on an extreme.
- `guard.py nearest` on the driver: 0.08 at task181 v2 (a count read before its records arrive), 0.06
  at task98 v2. Nothing on file judges a maximum against the distribution of maxima.
- `stumping/references/client/measured-drivers.md`: the held group includes the maturity attack, whose
  shape is that the graded object crystallises outside the natural pipeline's reach. This build's
  decisive reference is in the pack but at a selection breadth the natural pipeline never matches.

### Default path

1. Read `panel_throughput_minutes.csv`, the client telemetry at one row per interconnect per minute for
   the retained evening band and the retained daytime band of every day of 2027 Q1.
2. Read the quality standard's definition of the delivered-bitrate shortfall and compute it per
   interconnect per evening: the median of the daytime band's minute values less the median of the
   evening window's minute values, in kbps.
3. Take the worst evening window of the quarter. It is `STR-01` on 2027-02-08 in the 20:00 window at
   569 kbps.
4. Test it against that interconnect's own window-to-window variation over the quarter. It sits far
   outside, so the shortfall is not ordinary variation on that path.
5. Check the register and the maintenance schedule for anything that disqualifies the evening, leave
   out the fourteen evenings clause 4.4 names, and recompute. The worst window is now `HVT-01` on
   2027-02-17 in the 19:00 window at 318 kbps, which stands 29 per cent above `HVT-01`'s own 99th
   percentile for the quarter at 247 kbps.
6. Correct for having looked at seven interconnects: the per-path tail probability times seven still
   clears, because the selection the monitoring made was over windows, not over paths.
7. Fund the augment on `HVT-01`.

**Ends on:** fund the augment on `HVT-01`, the worst evening shortfall of the quarter at 318 kbps.
**Golden:** fund no augment this cycle. `HVT-01` comes closest at 318 kbps, and fourteen evenings are
left out.

### Stump sentence

A competent solver cleans the panel, leaves out the booked evenings, takes the quarter's worst
evening window at 318 kbps, tests it against that interconnect's own variation and against a
seven-path multiplicity correction, finds it clears both and files fund the augment on `HVT-01`, where
318 kbps is smaller than the worst window every one of the eight earlier quarters produced at the same
reach and the call is to fund nothing.

### Three rules

Re-answered against the screens above rather than against the design's intent. Six of the thirteen
lines fail, and each failing line says so in its first words.

- **Task type:** **HOLDS on the label, FAILS on the work.** `multiple-testing-selective-inference`
  does serve Anomaly Detection & Diagnostics, and the call is nominally whether one monitored extreme
  is a real degradation or what monitoring 1,851 windows produces on its own. But nothing selective
  is computed: screen 2 shows the construction is one column maximum, so the task type is the label
  on the design and not the work the solver does.
- **Domain test:** **FAILS.** The deciding quantity was meant to be the null distribution of a
  maximum over many series and many periods. Measured, that distribution enters the call only through
  its own maximum, which equals the pooled maximum of the same rows to 0.000e+00, so the deciding
  quantity is a single recorded number the record already holds and there is nothing for selective
  inference to estimate. A quantity the records fix exactly is not one the field estimates
  (`stumping` 1.2a).
- **Swap:** **FAILS the method swap, which is the swap that binds in General Statistics.** Replace
  the distribution of the quarterly worst cell with any summary of the same record and the call does
  not move: the quarterly-worst reach holds 10 of 10 and the single interconnect's own record holds 7
  of 8. The call survives deleting the whole selective layer, so the method is not what the task
  turns on.
- **Layer 1:** **HOLDS.** The panel is minute grain with collector dropouts, written in UTC while the
  framework states the windows in local time and the Netherlands moves to summer time on 28 March
  inside the quarter; two vantage points measure the same traffic at different grains, the client
  telemetry per minute and the edge per five minutes; one interconnect was renamed on 12 February and
  the register carries both codes; nine evenings on one path sit inside a planned maintenance window;
  the cost workbook is one wide sheet per month. Every one of these is what the platform's own systems
  produce, none is placed to be caught, and the reader joined the rename unprompted, which is what a
  sound Layer 1 does.
- **Layer 2:** **FAILS.** `forecast_uncertainty` with own pattern `null-of-the-selected-maximum` was
  to make the breadth of the selection the methodological choice that flips the call. Screen 1
  measures that breadth as inert: it is which record is opened, not at what breadth it is read, and
  clause 4.2 names the record. There is no Layer 2.
- **Decisive step:** **FAILS.** As designed it was to calibrate the statistic at the selection that
  produced it. As measured it is: open `evening_quality_daily.csv`, subtract its two median columns,
  drop clause 4.4's evenings and take one `idxmax`; the largest row of nine quarters sits in 2026Q1 on
  `RHN-01`, so fund nothing. One group-by, or not even that.
- **Not semantics:** **HOLDS.** Every field, code, unit and definition read correctly still leaves 318
  kbps standing as a correct figure for a real evening on a real interconnect. The dictionary gives
  the timezone, the register resolves the rename, the standard defines the shortfall and the framework
  names the booked evenings and the three windows. The reader read all of it right and the figure it
  reached was the golden's, so the call never turned on a reading. This line was never the problem.
- **Not rule application:** **FAILS, and the measured family spread is the proof: 0.0 kbps on every
  graded figure of the call.** The question is not whether a filed rule names the method but whether
  anything is left to decide once every filed rule is read, and here nothing is. Clause 4.2 files the
  criterion ("larger than the shortfall the network's own record shows the measurement produces
  without congestion") and the 48-construction family it leaves open puts a spread of exactly **0.0
  kbps** on the decided 318 kbps, **0.0 kbps** on each of the 21 grid worst-window figures, **0
  names** on the closest interconnect and **0** on the 14 evenings; the reference spread itself is
  264.2 kbps but no graded figure reads it. 35 of 48 constructions file the committed hold, 34 of the
  38 read off the record do, and the reader's own 330.2 kbps is one of them. A spread of zero means
  the step is a reflex whatever the documents say.
- **Analyst test:** **FAILS, measured.** The test claimed a strong analyst tests the quarter's worst
  cell against the interconnect it fell on, adds a seven-path multiplicity correction, clears both and
  files fund the augment on `HVT-01`, the default path's `Ends on:` at 318 kbps. The blind reader did
  exactly the per-port comparison the test predicts, against that port's own non-congested record at
  330.2 kbps rather than its current-quarter spread at 248.0, and filed the golden hold. The easy
  route lands the answer, so there is no stump.
- **Estimand:** **HOLDS.** Clause 4.2 files the quantity as the largest shortfall any interconnect in
  the register shows in any evening window of the reporting quarter, one figure for each interconnect
  and each window, the interconnects being those the register has in service at the quarter end
  including any renamed inside it, and the evenings being every date of the quarter outside the
  maintenance windows clause 4.4 names. It is filed literally and its literal execution is the
  golden's quantity. Filing it is also what leaves nothing behind it.
- **No decoy:** **HOLDS.** Nothing is planted to be caught. No block of readings is copied, no memo
  argues a call, no stakeholder figure carries an answer, no draft or briefing ships, and the
  maintenance window is a real schedule the framework points at. The eight earlier quarters are the
  rollup the platform's own quality pipeline keeps and carry no determination to reproduce.
- **No certified replay:** **HOLDS.** No published figure is reproduced to recover a method. The
  published quarterly report states the platform-wide delivered bitrate and nothing per interconnect,
  and the reference is computed, never published.
- **Lesson:** **FAILS.** The intended lesson was to calibrate an extreme at the breadth it was
  selected at. A model that gets this build right learns nothing of the kind, because the breadth does
  not reach the call: it learns to open the two-year rollup the pack ships, which the reader did
  without being told.

### Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the quarter's worst cell against its own path | clause 4.2 names the quantity | the panel's own columns | yes, the first move | none | the battery does not reach it | one subtraction | readable |
| 1 the maintenance evenings excluded, then the same test | clause 4.4 names the evenings | the maintenance file keys on path and date | yes | none | yes, a date join | one filter | readable |
| 2 the path's own eight-quarter history, and a seven-path correction | no | the rollup carries path and evening | yes, the back-test reflex | the rollup is a bench for the path, not for the cell | no | no | readable |
| 3 the quarterly worst cell against the eight earlier quarterly worst cells (decisive) | no sentence names a selection breadth; clause 4.2 files the statistic and says nothing about its reference | the rollup's schema is path and evening, the same as the panel's, and nothing in it marks a quarter maximum | no reflex computes a maximum of maxima | the rollup funds under its natural per-path use, so the bench points the other way | no sweep computes a statistic of a statistic | no, it is a distribution of an extreme | silent |

### Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | interconnect | one port in the register, the renamed one being one interconnect | the peer, or each code as its own interconnect | the cell set changes | the register's `current_port_code` and in-service dates; asserted on counts |
| SF2 | evening window | the three windows clause 4.3 reports on | one window of the solver's choosing | the grid changes | clause 4.3, quoted; the call is identical in all three, asserted |
| SF3 | shortfall | the daytime band's median less the evening window's median, per the standard | the evening median less the daytime median, or a mean | the sign or the level changes | the standard's definition, quoted; asserted |
| SF4 | the clock | the windows in local time on timestamps the dictionary states are UTC, summer time from 28 March | the windows applied to UTC directly | the worst cells change | clause 4.3 "in local time" and the dictionary's UTC sentence, both quoted; asserted |
| SF5 | median | the median of the band's minute values | the median of the seconds behind them, or a session-weighted mean | the level changes | the standard's definition of the minute value and of the band median, quoted |
| SF6 | a usable evening | the evenings the collector captured both bands of, whole | a completeness rule of the solver's choosing | `same call`, asserted: a collector loss takes a whole band for a whole day on one port, so every band the panel holds is whole and every completeness rule selects the same evenings |
| SF7 | maintenance evenings | the nine evenings clause 4.4 names, excluded | kept, or a wider exclusion around them | the worst cell changes | clause 4.4, quoted; asserted |
| SF8 | the quarter | 1 January to 31 March 2027 | the four quarters to 31 March, or the fiscal quarter | the cell set changes | clause 4.1 and the prompt's quarter close, quoted |
| SF9 | worst | the largest shortfall | the smallest delivered bitrate, or the most evenings below the floor | the candidate changes | clause 4.2 "the largest shortfall", quoted; asserted |
| SF10 | comes closest | the interconnect with the largest worst-evening shortfall | the one nearest the record on its quarter mean | the named interconnect changes | clause 4.2, which takes the decision on the largest any interconnect shows in any window, quoted; asserted that the mean reading names a different one |
| SF11 | rounding | to the nearest kbps, once, at the end | per window, or per minute value | `same call`, asserted at the nearest kbps and at one decimal |
| SF12 | ties | none: the seven worst-evening figures are distinct in every window | a tie at the top | `same call`, asserted |
| SF13 | the earlier quarters | the eight whole quarters the rollup covers before 2027 Q1 | the trailing eight quarters including the current one | `same call`, asserted: every quarter of the record is above the quarter's own worst window either way |
| SF14 | the reference band | 12:00 to 14:59 local, the band the standard names | the whole non-evening day | the alternative cannot be computed: the panel retains no minute outside the two bands, asserted | the standard's own sentence, quoted |

### Ladder

| Rung | Analysis | Names | Figure | Dies to |
|---|---|---|---|---|
| 0 | the quarter's worst evening window, tested against its own interconnect's spread | `STR-01` | 569 kbps on 2027-02-08 in the 20:00 window | clause 4.4, which names the evenings that window sits in |
| 1 | the same test after the booked evenings are left out and the clock is read in local time | `HVT-01` | 318 kbps on 2027-02-17 in the 19:00 window | the window was selected as the maximum over 1,890 windows, so the interconnect's own spread is not its reference |
| 2 | the interconnect carrying the largest shortfall across the quarter, not on one evening | `DLF-01` | a quarter mean of 132 kbps, 12.7 per cent above the next interconnect | its own 2026 fourth quarter mean was 136 kbps, so the record shows that level is ordinary for this path |
| 3 (decisive) | the quarter's worst window against what the record produces at the same reach | no augment | every one of the eight earlier quarters produced a larger worst window, from 398 kbps to 489 | nothing: it is the answer |

**Position and margins.** On rung 0 the answer is not a candidate at all, which is what a hold build
gives in place of a position; the blocking quantity is the quarterly worst window's rank, and it is
asserted. `HVT-01`'s 318 kbps sits 25.2 per cent below the smallest worst window any earlier quarter
produced and 29 per cent above `HVT-01`'s own 99th percentile for the quarter at 247 kbps, so the two
references are 54 per cent apart on the same number. Rung 0's 569 kbps sits 16.4 per cent above the
largest the record holds, so a solver who keeps the booked evenings funds confidently and wrongly.
Rung 2's `DLF-01` stands 15.3 per cent above the next interconnect on the quarter mean, so that rung
is a confident pick that the record itself answers.

**The reference is forced by the data, not by the clause.** Clause 4.2 names the record the comparison
is against and says nothing about which figure of it to take, so `checks.py` sweeps eleven figures a
planner might take, the largest, smallest, mean and median of the quarterly worst windows, their 90th
percentile, the pooled windows' 99th, 99.9th and 99.99th percentiles, and the per-port quarterly
maxima's median, 90th percentile and largest, and asserts every one of them is at least 6 per cent
above the quarter's own worst window. That is what makes the call forced while leaving the reach to
the solver.

**The grid.** Two axes, cleaning and reference breadth, every cell a named answer:

| | the path's own spread | the path's own 270 windows | the quarter mean | the quarterly worst window |
|---|---|---|---|---|
| maintenance evenings kept | `STR-01` | `STR-01` | `DLF-01` | `STR-01` at 544 against 489 |
| maintenance evenings excluded | `HVT-01` | `HVT-01` | `DLF-01` | no augment |

Seven of the eight cells name an interconnect and one is the golden, so the golden needs the filed
exclusion and the decisive step together. The corrections walk one way, toward a smaller candidate
set, and only the breadth of the reference reverses the call.

**Worth, on the graded quantity.** The decisive step changes the recommendation, the closest
interconnect's standing and the flip figure. It does not change the 42 grid figures, which are the
construction layer every top response computes, so the ladder is carried by the call and the asks
carry the rest.

**A hold is determinate here.** The blocking quantity is a computed rank that reproduces from the pack
(the quarterly worst cell against eight earlier draws of the same statistic); every interconnect fails
for a named reason (none of the seven worst-evening cells reaches 489 kbps in any window, asserted
cell by cell); the prompt licenses the non-pick on equal footing with the seven; the default path still
(none of the seven interconnects' worst evening windows reaches 489 kbps,
asserted path by path); the prompt licenses the non-pick on equal footing with the seven; the default
path still names an interconnect; and a worst evening window above 489 kbps, or a quarter mean above
what the eight earlier quarters produce for that path, would have made it a pick.

### Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which interconnects and which evenings | clause 4.2 files the register's in-service interconnects at quarter end and every evening of the quarter outside clause 4.4's windows; the renamed port is one interconnect, asserted |
| 2 | Unit of account | the port, the peer, or the code | the register's `current_port_code`, one port per peer among the seven; transit ports are not in the register, asserted |
| 3 | Attribution window | which evening a minute belongs to | the local calendar date of the window's start; no window crosses midnight, asserted |
| 4 | As-of dating | the register at the quarter end or at the pull | clause 4.2 files the quarter end; the register's in-service set is identical at both dates, asserted |
| 5 | Version basis | the restated commitments and the reissued build numbers | ask-side only; the main call reads no restated record, asserted |
| 6 | Denominator | none: the shortfall is a difference, not a ratio | nothing to close, stated |
| 7 | Weighting | minute values weighted equally inside a band | the standard's band median, quoted; no session weighting anywhere in the call |
| 8 | Window length | the quarter, and the eight earlier quarters | clause 4.1; the rollup's own quarter boundaries, asserted equal in length |
| 9 | Boundary inclusivity | 19:00 to 22:59 and the band edges | the standard states the bands inclusive of both minutes; no cell turns on an edge minute, asserted |
| 10 | Rounding path | once at the end, to the nearest kbps | the prompt's last sentence; asserted identical at one decimal |
| 11 | Tie-break | two interconnects level | none: the seven figures are distinct in every window, asserted |
| 12 | Maturity and censoring | the quarter is closed and the rollup's quarters are whole | clause 4.1 and the rollup's own coverage; no partial quarter is in either, asserted |
| 13 | Order of operations | exclude then rank, or rank then exclude | C1: the excluded evenings are the same set either way, asserted |
| 14 | Row order | the panel's file order | C1, asserted over three permutations |
| 15 | Duplicate resolution | repeated minute rows from a collector retry | C1: every repeat is byte-identical on the measured columns, so any resolution gives the same median, asserted |
| 16 | Identity normalisation | the renamed port across the panel, the register and the rollup | the register's `current_port_code`; asserted that the rollup and the panel resolve to the same seven |
| 17 | Netting against gross | may a positive evening offset a negative one | nothing is netted: each cell stands alone and the maximum is taken, stated |
| 18 | Dimensional units | kbps in the panel, Mbps in the edge file, Gbps in the register | the dictionary states each; the call reads only the panel's kbps, asserted |
| 19 | Code and status semantics | the collector status codes and the in-service flag | the dictionary; never the decisive step |
| 20 | Integerisation | none in the call | stated; the asks round once |
| 21 | Clause scope | clause 4.4 per path and date, or per path | the clause states both, quoted; asserted that the nine evenings resolve to one path |
| 22 | Forward window contents | the quarter ahead the augment would serve | the pack carries no record of it and the call is about the closed quarter's evidence, stated |

### Literal reader

Executing the prompt, clauses 4.1 to 4.4, the quality standard's definitions and the dictionary word
for word selects the seven in-service interconnects, the three evening windows in local time, and every
evening of 2027 Q1 outside the nine maintenance evenings, and asks for the largest shortfall in each
path and window and whether an augment is funded. The text is silent on what the largest shortfall is
compared against, so every option was computed: the interconnect's own evening spread funds `HVT-01`,
its own two hundred and seventy windows fund `HVT-01`, a seven-path correction funds
`DLF-01`, and the distribution of the quarterly worst cell funds nothing. The easy ones are easy
methods on the same literal estimand, not other readings of it, and every other term and convention has
an SF row ruled out by a quoted sentence or asserted to give the same call.

### Oracles

- `evening_quality_daily.csv`, the eight earlier quarters at one row per interconnect per evening,
  confirms nothing: it carries no determination, no placement and no ranking, and under its natural
  per-path use it funds `DLF-01`, so it points away from the answer rather than toward it.
- The published quarterly quality report confirms the platform-wide delivered bitrate by quarter and
  states nothing per interconnect; it ties under every rung.
- `collector_health_log.csv` confirms the panel's gaps; it ties under every rung and the call's
  completeness is C1-closed without it.
- The edge five-minute file confirms traffic volumes in Mbps; it carries no shortfall and ties under
  every rung.
- No control, published figure or corpus scores an interconnect or an augment, and no past augment
  decision ships. There is no calibration organ.

### Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 billable 95th percentile per peer against the commitment it was billed on, and the overage in euros | 3 per peer | the audit trail from an input the call consumes to another system's control total | the quarter's peering invoices are being closed | D2 version: one commitment was restated after the quarter opened and the record billed on is the latest accepted, not the latest delivered | D6 the samples are per port and two transit peers hold two ports each; D3 Mbps against Gbps; D8 the sample clock | `edge_traffic_5min.csv`, `peering_commitments.csv`, `commitment_amendments.csv`, `interconnect_register.csv`, `invoice_credits.csv`, dictionary, standard, handover inventory; 13 columns | 4 stops, lazy delta 11.4 per cent of the overage | a peering team closing a quarter's invoices against commitments that move |
| A2 sessions and the share that rebuffered, per client build | 2 per build | a measure every candidate carries that the call does not turn on | the release train's own quality review | D7 keys reissued: a build number was reused after a rollback, so one string covers two builds | D4 a channel absent for part of the quarter; D1 a re-sent daily file | `client_sdk_sessions.csv`, `sdk_release_log.json`, `rebuffer_events_daily.csv`, `collector_health_log.csv`, dictionary, handover inventory, register, standard; 11 columns | 4 stops, lazy delta 2 builds misread | a client team reading its own release quality |
| A3 incidents opened, those restored inside the standard, and those whose recorded cause sits outside the platform, per month | 3 per month | the trail from an input the call consumes through rows it never reads to a control total | the operations review the board sees with the augment paper | D4 absence as the signal: the standard measures to service restoration and only some rows carry the restoration time, the rest evidenced in a file no habitual join reaches | D8 the ticket close against the restoration time; D5 a partial extract of one queue | `incident_log.csv`, `incident_restoration_extract.csv`, `service_standard` in the framework, `collector_health_log.csv`, dictionary, handover inventory; 12 columns | 5 stops, lazy delta 7 incidents a quarter | an operations manager reporting against a service standard |

**The main population's zero counts.** Zero device rows and zero hazard rows in
`panel_throughput_minutes.csv`, `evening_quality_daily.csv`, `interconnect_register.csv` and
`maintenance_windows.csv` for the seven in-service interconnects in 2027 Q1 and the eight earlier
quarters, asserted by count. Deleting every device leaves the call exactly as hard.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D6 port against peer grain | A1, A2 | A1 two peers, A2 one build |
| D3 unit scale | A1 | the overage on every peer |
| D8 clocks | A1, A3 | A1 one sample day, A3 four incidents |
| D4 absence | A2, A3 | A2 one build, A3 seven incidents |

**The referee.** `telemetry_handover_inventory.csv` states each file's row count and date range and arbitrates the
one designed disagreement, the partial queue extract in A3, without naming a level.

**The cracker sheet, refuted by measurement.** The table below is the author's model of the opponent
and the wave 8 reader beat all three of its rows. It is kept as the record of what was predicted. The
reader answered 119 of the 128 non-call leaves in `generator/figures.json` and hit 111, so each of
A1's version device, A2's reissued build key and A3's absent restoration times was defeated at medium
effort, and at least 40 of the 48 device-bearing figures were taken.

**And the ask layer cannot be rescued on this pack, by arithmetic rather than by judgement.** Of the
128 graded non-call figures, only **48 can carry a device at all** (A1's 21, A2's 18, A3's 9). The
other **80 (62.5 per cent)** are the call's own construction layer: the deliverable's 42 worst-window
cells and dates, the 8 quarterly worst windows, the 7 own 99th percentiles and 23 call-side
singletons. `supplemental-stumping` requires the devices to be decoupled from the call, so none of
those 80 may carry one, and the prompt shape that supplies the 25 criteria is what puts them in the
deliverable. So the **best achievable ask result from re-cutting only the asks is 80 of 128, 62.5 per
cent**, with every one of the three devices working perfectly. That is over the bar on the ask side
alone before a single device is designed, which is why the ask layer is re-cut inside the stage 1
re-root and not against this pack.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 overage per peer | the commitment as delivered, ports read as peers | overage on two peers too high and on two peers absent | the amended commitments, ports rolled to peers | miss |
| A2 rebuffer share per build | the build string as the key | two builds blended into one | the release log's build windows | miss |
| A3 restored inside the standard per month | the ticket close as the restoration | seven incidents counted inside | the restoration extract joined on the incident reference | miss |

**Pair ceiling:** 93.3 measured, against the 39.5 this sheet predicted before the pack was cut
**Mirror leakage:** 93.3 measured, against the 20.0 predicted; the reader held the ask weight while
also landing the call, so there is no mirror to leak into
**Measured by:** `.claude/skills/leak-check/score_reader.py`, wave 8, one blind Sonnet reader at
medium effort holding only a fresh unzip of `target.zip`, `prompt.txt` and the figure names: 1 of 1
on the call and 111 of 119 on the ask figures

### Pre-ship check

The pack as built, read against the gates one last time.

- **Free gates.** 153 generator assertions, 168 independent checks in `verify.py` (it reads only
  `target/` and `figures.json`), `precut.py` 49 checks 0 FAIL 0 WARN, `figures_check.py` 103 of 103,
  `voice-check.py` exit 0 at 979 characters, `leak.py` REVIEW with four answered lines, `guard.py heart`
  PASS at nearest 0.05 (task130 v3), `guard.py surface` clean with no persona in the pack. Two rebuilds
  byte-identical (pack md5 b584b3b0c7f86c594b8ab3532861bbe9), `target.zip` cut from the final rebuild,
  22 entries, md5 3314fa1c8e8d9edaa14011ff8cdad913, every entry matching disk.
- **Input gates.** 22 files, 4 formats (csv, pdf, xlsx, json), three files over 25,000 rows
  (`edge_traffic_5min.csv` 311,040, `panel_throughput_minutes.csv` 224,460, `evening_quality_daily.csv`
  17,178), five distractors named in `metadata.json`, none named in a file name.
- **The three rules against the built pack.** The decisive step is still the analytical one: clause 4.2
  names the record and never which figure of it, and the eleven figures of the record that `checks.py`
  sweeps (every quarter's maximum, the per-interconnect maxima, their mean, the pooled 99th and 99.5th
  percentiles, the same-quarter-a-year-ago maximum, the most recent quarter's) are each asserted at
  least 6 per cent above the quarter's 318 kbps, so no reasonable reading of the record funds anything
  and the solver's own choice of comparison is what decides. The mess stays in Layer 1: UTC minute
  stamps against local evening windows, a port renamed mid-quarter, whole bands the collector missed,
  a stale commitment row beside an accepted amendment and an unaccepted one, ticket-closed against
  restored time. Nothing is planted to be caught: the booked maintenance evenings are filed in clause
  4.4 and excluded by rule, a lower rung, and the figure they would otherwise produce (569 on STR-01)
  is above every quarter of the record, so skipping that rule files a wrong answer without being the
  stump.
- **Gate G.** No shipped artifact ranks the seven interconnects on the decision question.
  `peering_capacity_plan.xlsx` ranks them on headroom, declared in `metadata.json` as the wrong-basis
  distractor and ruled out by its own footnote saying headroom carries no quality measure; the ranking
  it implies (STR-01, OPL-01, HVT-01 tightest) is not the shortfall ranking. Delete every wrong number
  in the pack and the call still turns on which figure of the record the 318 is measured against.

## Tried and rejected

- The seed's own architecture, the strongest evening gap against a filed band of what uncongested ports
  have shown: a filed reference band is a stated score deciding the call, which the client's rules ban
  at any depth, and the band is an official decoy to a literal judge. Re-rooted at the draw.
- Estimating the null of the selected maximum from a hand-picked quiet subset of the same quarter: it
  is circular, because knowing which paths are quiet is the call, and a literal judge reads the subset
  as the author's own choice. Replaced by the eight earlier quarters, which select nothing.
- Estimating the null from the quarter's own daytime band at the same breadth: the daytime band carries
  a fraction of the evening's sessions, so the measurement noise is on another scale and a careful
  analyst would rightly refuse the comparison. Dropped before any data was cut.
- A filed alarm rule with a nightly threshold, so that the statistic becomes a count of alarm nights:
  the alarm rule is a stated score and the selection collapses to seven paths, which a strong model
  corrects by reflex. Dropped: the selection has to be over cells for the step to be worth a rung.
- Architecture 1 itself, the quarterly worst window judged against the eight earlier quarterly worst
  windows: refused on measurement, not redesigned. The licensed family of 48 constructions puts a
  spread of 0.0 kbps on every graded figure of the call, the designed maximum-of-maxima is an exact
  identity with one column maximum of the same rows (0.000e+00), and the ladder's margin and Gate C's
  requirement are the same number, so the admissible placement of the decided figure is empty by 28.9
  kbps. The selection breadth the architecture rests on is inert: the record holds the call at every
  reach, 34 of 38. See `## Measured refusal`.
- Resuming architecture 1 by re-siting the reference (a trailing-four-quarter reference, a per-port
  reference, a pooled-window percentile): killed by screen 1 before it was designed. Every one of
  those is already in the 48-member family and 34 of the 38 record-based members file the committed
  hold, so moving the reference moves no graded figure and cannot restore a ladder.
- Re-cutting the ask layer alone on this pack: refused by arithmetic. Only 48 of the 128 graded
  non-call figures can carry a device; the other 80 (62.5 per cent) are the call's own construction
  layer, which `supplemental-stumping` forbids a device to touch, and the prompt shape that supplies
  the 25 criteria is what puts them in the deliverable. Perfect devices on all three asks still bank
  62.5 per cent of the ask weight, over the bar on its own. The asks are re-cut inside the stage 1
  re-root.

- 2026-10-31, the batch 1 re-root, architecture 1 spent (see `## Architecture 1 record`): its decisive step measured as
  landed in-house before any portal result, the multiple-testing cell, the filed comparison criterion and the
  statistic-of-a-statistic reference retired with it.
- 2026-10-31, at the draw, Human Factors & Ergonomics / safety-incident-error-analysis, signals passed at danger per
  occasion a train met the signal at danger, rebuilt from the signalling aspect log against the trains' berth records:
  dead before a card, measured in two slots (task180: the exposure is either named, rule application, or a fork against
  trains passing; task181: a stop-aspect exposure is the first thought once an aspect log ships).
- 2026-10-31, at the draw, the same cell, fatigue involvement in a trucking operator's incidents, each regional
  investigation team identifying fatigue at its own hit rate, corrected by a fatigue specialist's review of a sample:
  dead before a card, the misclassification-correction family is spent (task242 shipped a Rogan-Gladen correction on a
  validation panel, task192 a classifier's rates, task228 rejected a flag's prevalence corrected the same way).
- 2026-10-31, at the draw, the first card's decisive triple (gap objective, G16, designation_set): `test.same_puzzle`
  BLOCK inside the batch against task270 v4; the decisive generator is G3 (record against operation), the honest one,
  since the question the step answers is whether the gene's loss or the guide's cut killed the cells.
- 2026-10-31, at the draw, the decisive G3 and a designation set: `ban.pattern` and `test.same_puzzle` BLOCK against
  task470 v2, registered while this card was drafted; G16 decisive with G3 second, the slate under the round's
  capacity, shape 10 (01 banned against task470), the chart as SVG (pdf and xlsx repeated task306 v3).

- 2026-10-31, architecture 2 (the knockout-screen world, drawn in commit a0836137): spent at stage 2 with no data cut,
  because the previous fork's drafting of the world was interrupted by a safety classifier; re-rooted to a cell far
  from genome editing, laboratory biology and anything dual-use, and its card moved to the lineage. The two
  human-factors designs this note already screens dead stay dead (signals passed at danger per approach at danger;
  fatigue misclassification corrected by a specialist review).
- 2026-10-31, at the architecture 3 draw, set aside before a card: a card issuer's fraud screen read through its random
  holdout (the honest label is population_selection, banned against task250's card in this window); a breach's
  exposure window read as the step in each day's later-fraud share at a skimmed merchant (the step is visible on a plot
  and the change-point estimators split); a shared decline budget whose cut-off drifts and lets other segments' fraud
  through (filing what the model team decides on names the fixed cut-off, rule application); vehicle or yard-block
  hazards read within the operators who worked them (the handler-plus-unit regression task201's architecture 13 measured
  as the reflex); descriptor-change disputes (task181's own rejection, one self-join); an issue cohort read off a Lexis
  table (task173's cohort step died on its lever and the identification fork, and the honest label is composition);
  an inspector's misses read at the line's target prevalence (a fitted prevalence curve is a free form); confirmations
  answered from a swapped SIM (the closing sentence names the swap, the fork is the stump).
