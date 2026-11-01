# task273 design note

Architecture 6, drawn 2026-11-01 at the Batch 3 queue reset: the author had every queued task rebuilt as a fresh,
unique architecture built on what the approved builds share, so architecture 5 (shipped 10-28) was re-rooted with no
portal result on it. One architecture per world: the zone-substation load world is closed and the slot moves to a
dairy processing site's bore field, inside the same client domain (water supply sits in Energy Systems & Utilities, as
task124, task162 and task120 do). Its record sits under `## Architecture 5 record`.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task273.json`, architecture v6, v5 moved into `lineage` with its fate.
   `guard.py check` on the registered card: WARN only (`repeat.gate_g`, answered below; `shell.repeat` read the old
   prompt and cleared with the new one). Axes redrawn at the check: generators[0] from G5 to G3, the role family to
   `capacity_planner` (a utilities engineer setting what the bore field can carry), the forum to the site's drought
   committee, the forcing event to the summer season, the organisation to a manufacturer (a dairy co-operative's
   processing site runs its own bore field; local government and utility were both inside the ban window). Each is
   the honest label for this world.
2. Pairing: Energy Systems & Utilities / `asset-condition-maintenance` / Forecasting & Predictive Modeling. The
   deciding quantity is each production bore's pumping water level through a design drought, the figure a water
   supplier's source assessment forecasts for each bore before a summer.
3. Niche: a new production bore drilled between two existing ones, whose draw on its neighbours shows only in the
   footprint its commissioning test left in their daily level logs.
4. Call and shape: whether the 2026-27 summer bore plan passes the site's drought test, and if not which bores and
   months fail (`go_hold_or_stop`, question form whether); shape 07, a grid of eight bores by four months, each cell
   the lowest pumping water level (32 cells), plus the call, PB9's verdict and the two footprint figures.
5. Gate G `forecasting` (answered WARN: the batch's last build also carries it; it is the honest label for a
   predicted level the record pins), strategy `decomposition_attribution` (a bore's level is the sum of its own
   drawdown and every neighbour's, and the forecast has to split it), gap population, pattern none, generators G3,
   G6, G5.
6. **Data-native sentence:** the site has pumped its eight bores in the same proportions for twelve years, so each
   bore's own drought curve already carries its neighbours' steady draw and back-tests perfectly; the one bore whose
   draw the record has never carried is PB9, and the only days it pumped are the seven of its October 2026
   constant-rate test, when PB3's and PB4's daily levels moved by what PB9 will take from them all summer.
7. **Abstraction sentence** (the one sentence a reviewer holding this build and its nearest approved build would say
   is the same): none writable. Against task162 (valves holding outlet pressure only while the inlet is above them,
   the mill's draw on the shared main taking the inlets below): there a nonlinear device meets a varying pressure and
   the step is the device's cap; here a linear superposition meets a newcomer whose coefficient exists only in a
   seven-day test footprint. Against task124 (a street's service lines laid with its main, read from the other lines'
   tap cards): there the era of a unit is read off its siblings' records; here no unit's own record changes, a new
   neighbour's future draw does.
8. Same-puzzle test: gap population, pattern none (G3) and `go_hold_or_stop` match no build in the last twelve;
   `test.same_driver_older` cleared with differentiation lines against task138 and task178 v2.
9. People from `guard.py names --geo NZ --locale en_NZ --seed 273`: Megan Pickering (site utilities engineer,
   prepares the plan and signs the test), Allan Morris (owner of SWS-03, keeps the bore register). Invented names:
   Ruawaro Dairy Co-operative, the Kaitanga site, Mangarewa Stream, Matarae Regional Council, Waipa Drilling.
10. Pack (twelve files, three formats: CSV, XLSX, PDF): the SCADA daily log of each bore's take, mean pumping water
    level and pump run hours, 2014 to October 2026 (CSV, 37,000 rows); the council's MB1 monitoring bore daily
    levels (CSV); the bore register (XLSX: bores, pumps, monitoring); PB9's hourly test logger record (CSV, UTC);
    the summer bore plan (XLSX); SWS-03 (PDF, the governing WHAT); the water permit (PDF); the council's 15-minute
    permit-meter telemetry for 2025-26 (CSV, 280,000 rows); the metering provider's half-hourly pump ICP data (CSV,
    105,000 rows); the ICP and meter register (CSV); distractors: quarterly nitrate results and the site weather
    station's rainfall.
11. Sources, one line each:
    - Source yield practice: a water supplier forecasts each production bore's pumping water level for a design
      drought from the bore's drought curve (level against its own output, carried on the regional groundwater
      level), against the level its pump needs (UKWIR's source deployable output method is the common written form).
    - Well-field hydraulics: in a confined or semi-confined gravel aquifer the drawdown at one bore is the sum of the
      drawdowns every pumping bore causes there (superposition), and the drawdown bore A causes at B equals the one B
      causes at A (reciprocity).
    - A constant-rate test is how a new bore's yield and its effect on neighbours are measured; the neighbours'
      routine logs record that effect whether or not anyone reads them for it.

## Survivor anatomy

- **Actor:** PB9's drawdown on each existing bore has no column anywhere: the register holds coordinates, the daily
  log holds each bore's own take and level, the test record holds PB9's own level and discharge. The property is a
  relation across two files by date (PB9's test days against PB3's and PB4's daily levels), and nothing joins them.
- **Link:** the test record is hourly, in UTC, keyed by a logger serial; the daily log is local days keyed by bore
  tag. No key offers the join and no sentence invites a comparison: SWS-03 says nothing about neighbours, the plan
  and register say nothing about interference, and the field's own method (a drought curve per bore) never asks
  for one bore's level against another bore's take.
- **Reflex:** the field's method, each bore's drought curve on its own record carried on MB1's 2019-20 recession,
  with PB9's own drawdown from its test, is rung 0 and files the plan as holding with every bore at least 1.47 m
  above its minimum operating level.
- **Back-test:** each bore's own curve reproduces its 2019-20 and 2022-23 summer levels to about 0.2 m on average
  (0.35 m at the worst bore), because the bores were always pumped in near-fixed proportions; the textbook route
  validates on the pack's own record and nothing in it refutes the curve.
- **Second use:** the daily log is the spine for everything (and the run hours feed the electricity ask); the test
  record gives PB9's own drawdown and static level, which every route needs; MB1 is the drought and the permit's
  trigger; the register gives every level its datum and minimum. Delete the decisive step and every file stays.
- **Shock:** PB3's dip in the week of 7 October 2026 is 2.9 m on a series whose own take swings move it by 7 m
  every winter shutdown; sorted on the shipped statistics PB3 sits in the middle: second on mean pumping level
  behind PB4, second nearest to PB9 behind PB4, third closest to its minimum on the default path behind PB7 and PB4.
- **Pins:** SWS-03 files the WHAT (every production bore in the plan including one entering supply, its pumping
  water level as the logger's daily mean, at the planned take every day, with the aquifer at MB1's December 2019 to
  March 2020 levels, against the register's minimum operating level). No filed sentence names neighbours,
  interference, the test, a window or a method; deleting any one sentence leaves the call forced.

## Default path

1. Read the plan's takes for December to March and SWS-03's test; conform the daily log (old tags, the re-sent
   batch, levels to reduced levels with the register).
2. For each existing bore, build its drought curve the way a source assessment does: its level less MB1's on its
   own daily take over the record, a line per bore.
3. Carry each curve on MB1's lowest level in each month of December 2019 to March 2020 at the bore's planned take.
4. For PB9, take its static level and its drawdown per ML/d from the constant-rate stage of its test, and carry it
   the same way at 4.40 ML/d.
5. Compare each bore and month with the register's minimum operating level.

Ends on: the plan holds, every bore above its minimum operating level in every month
Golden: the plan fails, PB3 below its minimum operating level in February and March

## Stump sentence

A competent analyst builds each bore's drought curve on its own record, carries it on MB1's 2019-20 levels at the
planned takes, adds PB9 from its own test, and files that the plan holds, every bore above its minimum operating
level in every month; the step that lands it there is reading each bore's level as its own take's alone, when PB9 will
lower PB3 by 3.0 m at 4.40 ML/d, which only the dip PB9's constant-rate test left in PB3's daily log measures.

## Three rules

- **Task type:** energy-systems-utilities asset-condition-maintenance, which serves forecasting: the forecast is the
  condition each production bore will run at (its pumping water level against its pump's limit) through the coming
  summer.
- **Domain test:** the deciding quantity is each production bore's pumping water level through the design drought,
  which a water supplier forecasts from the bore's drought curve on the aquifer's recession; in a bore field the
  level is the aquifer's response to every bore's take at once (superposed drawdown), the field's own hydraulics.
- **Swap:** "whether the bore field's summer plan keeps every bore above its pump's minimum level" with wards for
  bores and beds for megalitres: nothing lowers one ward's capacity by another ward's admissions through a shared
  aquifer, and no test footprint measures it; the sentence stops making sense.
- **Layer 1:** SCADA tags renamed at the May 2019 upgrade; a gateway batch re-sent after the August 2021 outage;
  1.1 per cent of bore-days missing from telemetry gaps; a logger swap at PB6; MB1 on NZVD2016 against bores reduced
  on Moturiki 1953; the PB9 logger in UTC against local days; the council's meters in NZST; a CT meter's register
  advance; each written by the system named, none placed to be caught, each neutral on the call (R2 in checks.py).
- **Layer 2:** decomposition of a superposed response, family estimand_identification: the level at a bore splits
  into its own drawdown and its neighbours', and the forecast for a new configuration needs the term for the
  newcomer, which the record measures only in its commissioning test's footprint.
- **Decisive step:** reading PB9's drawdown on each neighbour from the dip its 7 to 14 October 2026 constant-rate
  test left in their daily level logs, and adding it at PB9's planned take.
- **Not semantics:** every field read correctly (the levels, datums, tags, clocks, the plan, the minimum operating
  levels) still leaves the easy route on "the plan holds", because no field holds PB9's effect on another bore.
- **Not rule application:** no filed rule or procedure computes one bore's effect on another; executing SWS-03 word
  for word with the default construction files "the plan holds". The enumerated family for PB9's effect on PB3
  spans 0 (left out, rungs 0 and 1) through 1.62 m (log distance from the existing pairs, rung 2) to 2.92 m (the
  test footprint), a spread of 2.9 m on PB3's lowest level; the standing family once the data are read (the test
  footprint by regression on every bore's take with PB9's test days in, or by the before-and-after dip, or the fit on
  the last six years alone) spreads 0.02 m and gives the same graded half-metre in all 32 cells; what rules out the
  rest is the footprint itself, a 2.9 m dip in PB3 and 0.5 m in PB4 against the distance relation's 1.6 m and 2.1 m.
- **Analyst test:** a strong analyst who conforms every log and reads the plan and SWS-03 correctly builds each
  bore's drought curve, adds PB9 from its own test and files that the plan holds, every bore above its minimum
  operating level in every month; R3a in checks.py runs it on the clean truth.
- **Estimand:** SWS-03 section 4: for each month December to March, every production bore in the plan (PB9
  included) at its planned take every day, the aquifer at MB1's level on each day of the same month of 2019-20, the
  pumping water level (logger daily mean, m below measuring point) against the register's minimum operating level.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure argues the plan holds; the plan
  states takes, not a result; the test record is the driller's own log; no file ranks the bores.
- **No certified replay:** the golden reproduces no certified or published figure; no consultant's report on PB9
  ships, and the method is the field's hydraulics applied to the logs.
- **Lesson:** a bore's own drought curve is a statement about the field it was pumped in; when the field changes,
  the forecast needs the newcomer's footprint, and the record holds it only where the newcomer was tested. No build
  on file teaches superposition across units read from a commissioning footprint.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 own drought curves, PB9 on its own test | SWS-03 test | no | the field's method | none | none | yes | no | readable |
| R1 interference among existing bores | none | no | multi-bore fit is a known refinement | none | none | yes | no | readable |
| R2 PB9 by log distance from existing pairs | none | coordinates in the register | Thiem distance is textbook | none | none | yes | no | readable |
| R3 PB9 footprint from its test days in the neighbours' logs (decisive) | no sentence names neighbours, interference or the test footprint | no column, no key between the hourly UTC test and the daily local logs | the field's method asks for a bore's own curve, not another bore's take | no control scores it | no battery item compares a test record with other bores' logs | one dip per neighbour, but only once the relation is seen | the test record serves PB9's own curve and the daily log everything | silent |

## Semantic fork table

| Id | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | pumping water level | daily mean, daily minimum | SWS-03 section 3 defines it as the logger's daily mean; the log carries only that |
| SF2 | February in the design drought | with or without 29 February 2020 | SWS-03 "each day of the same month"; same call and same graded levels either way (checks.py) |
| SF3 | datum | MB1 on NZVD2016, bores on Moturiki 1953 | a constant any fit absorbs; no graded level moves (checks.py) |
| SF4 | which bores are tested | existing only, or PB9 too | SWS-03 section 2, a bore entering supply under the plan |
| SF5 | the take on each day | the plan's average, or a daily profile | SWS-03 section 4, the planned take on every day |
| SF6 | PB9's own level | its test static carried, or adjusted for its neighbours' takes by reciprocity | PB9 holds by more than 2 m either way (checks.py) |
| SF7 | the record the response is read from | 2014 to 2026, summers only, the last six years | same graded levels in all 32 cells (checks.py, verify.py) |
| SF8 | how PB9's footprint is measured | coefficient on its test days, or before-and-after dip | same graded footprint and levels (checks.py, verify.py) |
| SF9 | the test's day boundaries | UTC days or local days | same call (checks.py) |
| SF10 | falls below | strictly deeper, or at the level | no cell within 0.3 m of its minimum (checks.py) |

## Ladder

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| R0 | each bore's own drought curve, PB9 from its test (the default path) | the plan holds; smallest margin 1.47 m | PB3's daily log dips 2.9 m on PB9's test days |
| R1 | every existing bore's take on every bore's level, PB9 left out | the plan holds; smallest margin 1.61 m | the same dip, which no existing bore's take explains |
| R2 | R1 plus PB9 by the existing pairs' log-distance relation (0.37 m per ML/d on PB3, 0.47 on PB4) | PB4 fails in February (36.56 m against 36.1); PB3 holds by 0.79 m | PB4's log moved 0.5 m on PB9's test days, PB3's 2.9 m |
| R3 | R1 plus PB9's footprint from its test days (0.663 m per ML/d on PB3, 0.108 on PB4) | PB3 fails in February (35.45 m) and March (35.50 m) against 35.0; nothing else | golden |

- Separation: each rung names a different answer (none, PB4 February, PB3 February and March), asserted by name.
- Margins: golden PB3 February and March at least 0.45 m below; December and January at least 0.52 m above; every
  other cell at least 0.3 m above; R2's PB4 February 0.46 m below; R0's smallest margin 1.47 m (checks.py).
- Dominance: PB9's footprint on PB3 is 1.8 times what distance gives, on PB4 under a quarter.
- Pricing: the move the call needs is 0.5 m at PB3 in February; the footprint supplies 2.9 m. The standard error of
  the footprint is about 0.003 m per ML/d by the fit (0.015 m at the planned take), larger by the bare dip. The one-group-by route
  (each bore's own curve) is rung 0 and files the hold. Plan takes were set at last summer's averages in 0.05 ML/d
  steps and nudged within that step so every graded level sits at least 0.1 m inside its half-metre bin.

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | every production bore in the plan, PB9 included | filed (SWS-03 section 2); SF4 |
| 2 Unit of account | pumping water level, m below measuring point | filed (SWS-03 section 3) |
| 3 Attribution window | December to March | filed (SWS-03 section 2) |
| 4 As-of dating | MB1's level on each day of the same month of 2019-20 | filed (SWS-03 section 4); SF2 |
| 5 Version basis | the plan of 28 October 2026; the register as exported | one version shipped |
| 6 Denominator | none (levels) | C1 |
| 7 Weighting | none | C1 |
| 8 Window length | each calendar month | filed |
| 9 Boundary inclusivity | 1 December 2019 and 31 March 2020 inside | filed (SWS-03 section 3) |
| 10 Rounding path | each level rounded once to 0.5 m from unrounded metres | C1; every cell 0.1 m inside its bin (C4) |
| 11 Tie-break | none: no cell within 0.3 m of its minimum | C2; SF10 |
| 12 Maturity and censoring | none: the record runs to 31 October 2026 | C1 |
| 13 Order of operations | conform, fit, carry, compare | C1 |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | the re-sent August 2021 batch is exact | neutral (R2) |
| 16 Identity normalisation | old SCADA tags to PB1 to PB8 | the register's bore ids; neutral (R2) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | m3 to ML; L/s to ML/d; datum offset | SF3 |
| 19 Code and status semantics | the test stages (static, step, constant rate, recovery) | the logger's own stage column |
| 20 Integerisation | none | C1 |
| 21 Clause scope | the permit's MB1 trigger binds the take, not the test; MB1 never falls below it in the drought | asserted above 30.05 m |
| 22 Forward window contents | December 2026 to March 2027 at the plan's takes in the 2019-20 drought | filed (SWS-03 section 4) |

## Literal reader

Executed word for word, SWS-03 takes each production bore in the plan, PB9 included, at its planned take every day of
each month, with the aquifer at MB1's level on each day of the same month of December 2019 to March 2020, and asks
whether any bore's daily mean pumping water level falls below the register's minimum operating level. Nothing filed
says how a bore's level responds to takes; the literal reader building it from the logs and the test with every
bore's take in it files the golden, and one building it from each bore's own take files the hold.

## Oracles

none: no control, published figure or reconciliation column confirms either reading; the permit's MB1 trigger is
never reached in the design drought, and no file reports a bore's level under the plan.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling and its effect |
|---|---|---|---|
| tags renamed at the May 2019 SCADA upgrade | the historian | daily log | a bore split in two; fitting from May 2019 alone leaves the call |
| re-sent August 2021 batch | the telemetry gateway | daily log | kept twice; leaves the call |
| telemetry gaps | the radio network | daily log | rows missing; none on a design-drought day |
| PB6 logger swap | site instruments | daily log | serial changes; no level step |
| NZVD2016 against Moturiki 1953 | the council's datum since 2018 | MB1 | constant offset; absorbed (SF3) |
| PB9 logger in UTC | the driller's logger | test record | days shifted 13 hours; leaves the call (SF9) |
| council meters in NZST | the council's telemetry | permit meters | quarter edges an hour out; the ask files local dates |
| CT meter register advance | the metering provider | ICP data | read as kWh; PB2 after 11 February 2026 a fortieth (ask A hazard) |

## Ask sheet

Two asks on the 2025-26 year the site reports to the council, both on files the call never reads.

**Ask A, each existing bore's pump electricity per megalitre the permit meters measured, each quarter of the year to
30 June 2026 (32 figures, whole kWh/ML).** Home: the asset-condition review of the pumps the plan leans on.
- Primary device: switchboards SB-3 (PB5, PB6) and SB-4 (PB7, PB8) each carry two pumps on one ICP; the one
  handling that reproduces each pump's draw is its daily run hours times its motor rating (both on file, the pumps
  sheet and the daily log), and a run-hours or volume split misses all 16 of those figures.
- Second device (from Ask B): the megalitres are the permit meters', so a meter read as the bore Schedule 1 lists
  against it carries the wrong denominator for PB1, PB2, PB5, PB6, and PB4 after 17 February.
- Hazards: interval stamps in UTC; the PB2 CT meter's x40 from 11 February 2026.

**Ask B, each existing bore's volume as the council's permit meters measured it, each quarter (32 figures, ML to one
decimal).** Home: the permit's annual report (condition 4).
- Primary device: the council's loggers were refitted in May 2023 and two pairs went back on each other's meters
  (Schedule 1's Bore 1 logger reads Bore 2, Bore 5's reads Bore 6); only matching each meter's days to the SCADA take
  it tracks (outage days are zero on both) finds it.
- Second device: PB4's meter was replaced on 17 February 2026 under a new logger, WM-40958, which Schedule 1 does
  not list.
- Hazards: totaliser rollovers on two meters; missed polls; NZST against local quarters.

Pin test: the asking sentences pin the source (the permit meters), the unit, the rounding and local dates; no pin
names a logger, a board or a split. The main population carries zero device rows (the call reads the daily log, MB1,
the register, the test, the plan and SWS-03; the devices sit in the telemetry, ICP and ICP register files).

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| A, 16 shared-board figures | splits each board by run hours | miss |
| A, PB1 and PB2 by quarter | denominators from Schedule 1's swapped loggers | miss |
| A, PB4 Q3 and Q4 | the replacement meter left out | miss |
| B, PB1, PB2, PB5, PB6 by quarter | Schedule 1's swapped loggers | miss |
| B, PB4 Q3 and Q4 | the replacement meter left out | miss |

Pair ceiling: 45.7 ((38 + 7 + 55 x 0.31) and (5 + 7 + 55 x 0.31), averaged)
Mirror leakage: 31.2 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack)

## Architecture 5 record (spent 2026-11-01)

Shipped 2026-10-28 (target.zip f641cf2c, seven of sixteen zone substations designated) and re-rooted on 2026-11-01 at the Batch 3 queue reset, when the author had every queued task rebuilt as a fresh architecture. Its draw and stump, kept for the record:

### Architecture 5 draw

1. Card: `.claude/skills/fingerprint/cards/task273.json`, architecture v5, architecture 4 moved into `lineage` with its portal fate (v1 to v3 already there). `guard.py check` on the registered card returns WARN with no BLOCK. The window at the draw held task464 v10 (registered 2026-10-29 01:27Z by another session), task268 and task270, which bans utility_or_infrastructure, committee_or_panel, vote_or_meeting, register, shape 07 and the strategies decomposition_attribution, forecast_method_backtest and composition_mix; the minimum-load assessment sits honestly with the state energy department that sets the minimum-load framework (government_agency), decided by the minister (minister_or_cabinet) before the spring season (season_or_peak), advised by its director of energy security (policy_adviser). WARNs answered: `overuse.org_family` (a state department is a government agency, the plain label); `overuse.gate_g` (forecasting is the honest key: the call is a forecast the correctly read 2026 record does not pin until each tank's reach is read); `repeat.question_form` against task268 (the call designates a set of substations, so the question asks which).
2. Pairing: Energy Systems & Utilities / `load-forecasting` / Forecasting & Predictive Modeling. The deciding quantity is the field's own: each zone substation's minimum demand under a load-control retiming, built the way network and system planners build it, from a reference day's demand, the solar connection pipeline and each controlled-load tank's recovery replayed from its new release.
3. Niche: a retiming of a central load-control signal whose reach is a property of each meter's switching device, recorded only through the meter's model in a register the network keeps for metering.
4. Call and shape: which of the sixteen substations will fall below their minimum-load threshold at the lowest half-hour between 10.00 am and 3.00 pm on the October 2027 reference Sunday (`designation_set`, question form which); shape 13, the substations' lowest demand under the retiming as notified, and the flip point for each designated substation (the share of its time-switch tanks that would have to take the signal for it to clear its threshold), sized at stage 2.
5. Gate G `forecasting`, strategy `population_selection` (the population a scheduled retiming moves is the tanks whose device takes the signal, never every controlled-load tank), gap population then time, generators G8 (can the retiming actually move the load), G7 (when each tank heats), G13 (the October 2027 window against the 2026 record).
6. Data-native sentence: the controlled-load channel data show every tank heating overnight, ripple-switched, relay-switched and time-switched alike, because every device is set to the overnight window today; only the meter register's model codes, read through the meter model list, show the tanks (about a third, concentrated in the older suburbs behind a few substations) whose meters switch the hot water element from an internal time switch that the network's signal never reaches, so those tanks keep heating overnight after 1 September 2027.
7. Sources, one line each:
   - Minimum-load practice: system and network operators assess the spring minimum from a reference day's demand, the rooftop solar expected by the season and any load moved into the middle of the day; controlled load moved by a central signal is the network's main lever (solar soak), and its effect is each moved tank's recovery from its release.
   - Load control in Australian distribution networks: off-peak hot water is switched by ripple receivers or meter relays that follow the network's signal, or by time switches inside older meters that keep their own clock until the meter is reprogrammed on site or replaced.
   - The client library's load-forecasting patterns (weather normalisation, peak decomposition) are not this step; this build's own pattern is `own:a-load-control-retiming-reaches-only-tanks-whose-meter-takes-the-network-signal`.
   - This lane: task258 carries a validated intervention only to units whose served document lets it act (the device, a reach read off a record kept for another purpose, is shared and licensed; nothing here is validated or back-tested); task164 sets plug-in vehicles' effect on transformer evening peaks by tariff schedule; task464 rebuilds conductor currents from loads and a solar farm's export; task230's first architecture held a counterfactual pool to phones that could take an app update.
8. People, drawn with `guard.py names --geo australia --seed 273`: Megan Robertson (director of energy security, the department), Jacob Barnes (Tallowbark Networks' manager of network operations, signs the solar-soak notice). Invented names (Tallowbark Networks, Saltgrass Coast, Quorrabin, Brindlemoor and the other fourteen zone substations) pass `guard.py check` (tell.names); the zone substation names drawn first (Kurrajine, Merrigal, Corrimba, Kalbarrup and others) sat within two letters of real places (Kurrajong, Merriwa, Corrimal, Kalbarri) and were redrawn at stage 3 (H21).
9. Pack (twelve files, four formats): the sixteen substations' net demand from the SCADA historian, spring 2026, half-hourly in UTC (CSV, 69,856 rows, the spine); the Department's monitored sample of rooftop PV output per kW of inverter capacity (JSON, local time with offsets); Tallowbark's solar connections outlook to 1 October 2027 (XLSX); the metering installations register, current and removed meters for 91,000 NMIs (CSV, 114,571 rows); the approved meter models list (XLSX); spring 2026 consumption by meter register for the controlled-load customers (CSV, 78,047 rows); the load-control register (CSV, 31,832 heaters); the solar connection applications register (XLSX, 53,400 rows, the asks only); the Department's minimum-load framework v2 (PDF); network notice NN-2027-02 (PDF); distractors declared in `metadata.json`: the summer 2027-28 demand outlook (PDF) and the 2026 customer voltage enquiries (CSV).

### Architecture 5 stump sentence

The default path moves every controlled-load heater into the midday window and ends on four substations, Ondarra, Mundaree, Wirrandel and Tarravine, because the 8,575 heaters whose meters switch from an internal time switch never see the new signal and keep heating overnight; at Kinnabar, Quorrabin and Gerrimbal, where 49 to 62 per cent of heaters are time-switched, their recovery is 1.26 to 1.73 MW of load the midday minimum does not have.


## Architecture 4 record (spent 2026-10-28)

Wardale and Isles Health Board's 2027/28 couples' carrier screening panel (biomedical-clinical-research / statistical-genomics, Descriptive): which of 30 conditions reach one carrier in 200 in the Board's genome study, each phase's genotype calls scaled by its members' depth-dependent chance of a call. Golden 14 conditions (ARSACS, Joubert syndrome type 2 and diastrophic dysplasia joining at 7, 6 and 6 per 1,000) against the current 11 on the plain count and the depth-filtered count. Judge pass 1 SEND_BACK (the plain count read as a literal answer), repaired in the data with a within-gene contrast; judge pass 2 DETERMINISTIC, APPROVE; shipped on ea742c6b. At the portal on 2026-10-28 both responses filed the golden, one reporting observed and sensitivity-adjusted frequencies: the contrast made the missed calls visible and the per-phase detection correction is a published estimator a solver enumerates.

## Architecture 3 record (spent 2026-10-27)

Carrisford Water's 2027 critical mains register: which mains go on it once each burst is shut off at the valves the exercising programme says will close and what that cuts off is counted (urban-regional-science / network-analysis). Prototype only, never cut: golden 173 mains against 93 on the drawn segments and 50 by link removal (seed 5). Dead on paper at stage 2: the decisive rung readable on tests 1 to 3 (the shut-off clause the estimand needs, the programme's operable flag as a row predicate once segments exist, unreachable demand as the task type's own pattern) and deletion tests 3 and 6 firing.

## Architecture 2 record (spent 2026-10-27)

The Stonereach Valley Regional Transportation Commission's Commercial Fleet Safety Programme from 1 July 2027: which of seven commercial vehicle uses caused crashes at 1.5 times private drivers' rate per mile over 2021 to 2025, when no record counts any use's miles. Golden four (taxicabs, ride-hail, parcel delivery, app-based delivery) by induced exposure taken within road class, day type and hour and scaled by the Department's miles for each stratum (rung R4); the default path's pooled struck share filed airport shuttles and paratransit. Stage 3 green (target.zip 73efe129, 17 files, the units file 339,100 rows); stage 4: five isolated in-house readers all off the call (four on the pooled pair, one on road class alone), judge pass 2 DETERMINISTIC, APPROVE. Shipped 2026-10-23. At the portal on 2026-10-27 both responses estimated every use's miles by the stratified construction and filed the golden four: a published estimator a solver reaches with the literature carried no stump, and every refinement the crash records allow stacks a rung above R4.

## Architecture 1 record (spent 2026-10-22)

Closed-loop load tests and each pod's garbage-collection log: each endpoint's 99th percentile at the forecast peak over the requests customers send, rebuilt from the run of record's service times and every pod's pauses (golden EP01, EP02, EP05, EP16, EP22), against the recorded percentile (EP02, EP16, EP22) and HdrHistogram's back-fill (ten). Stage 3 green on target.zip 837ff5a0. Stage 4: both isolated scored readers (r273a, r273b) named coordinated omission, ran the per-pod open-arrival rebuild and landed the call (r273b every ask figure, 48 of 48; r273a Ask A 24 of 24 and Ask B 12 of 24); each pointed at standard 1.2 ("thousands of clients, each working to its own schedule") with 2.2's pause clause and the plan's closed workload, the sentences the estimand needs to be determinate. The judge DETERMINISTIC, APPROVE, Gate G method_or_model_selection, Gate H pass. The asks' devices failed with the call: the backward walk of the subscription events, which a strong solver runs anyway, undoes the re-signed accounts' anchor, and the carried-forward memo names the migration's balances.

## Tried and rejected

- The seed's world (an open-source security fund's 60 maintainer stipends to the eligible packages with the most dependents, at most 20 from one ecosystem), set aside at the draw on 2026-10-22: its quantities are counts the fund's filed rules fix (dependents as the certification counted them, monthly downloads, the cap per ecosystem), so its only decisive steps are grain, identity or rule application, which the three rules bar; the seed's own stump (dependent projects against dependent packages) is a grain reading.
- The same mechanism prototyped with one-second think times (`co1.py`, first setting): each thread then misses only one or two sends per pause and the recorded percentile sits within a few per cent of the rebuilt one; the test clients send back to back, as a throughput test at a fixed thread count does, so a two-second pause costs each blocked client dozens of sends.
- A blanket time weighting of the recorded requests (each weighted by its own response time): it credits every slow request, stalled or not, and flags most endpoints; recorded as a reflex, not a candidate.
- Architecture 1 (the closed-loop load test's coordinated omission, rebuilt per pod from the GC log), spent at stage 4 on 2026-10-22: both isolated readers recognised the closed workload's under-sampling of the pauses from the plan's workload paragraph and the standard's population and pause clauses (the WHAT the call needs to be determinate) and ran the open-arrival rebuild; a mechanism a field's practitioners know by name and a model reaches from the estimand's own sentences is landable whatever the ladder, and the asks' devices (a backward walk of the events, a memo naming the balance) were each one solver step from the answer.
- Architecture 2 draw, screens run on 2026-10-22 before any prototype; none cleared, so the draw is paused rather than forced. The guard window (task482, task478, task249) also closes `composition_mix`, `other` and `causal_design`, the `season_or_peak`, `budget_or_appropriation` and `statutory_or_regulatory_filing` forcing events, and the utility, cooperative and statistics-office organisations.
  - Event times known only between inspections: the midpoint reflex reaches the golden (task201's measurement).
  - Members a detector, a list or a survey never saw (a probability-of-detection weighting, capture across lists, unseen-species counts): whether they are in the population is the estimand's WHAT, task190's death.
  - A finer interval's tail read from coarser averages (change of support): a ratio carried over from a finely measured subset is the reflex, and the within-interval model forks the figure.
  - A counter blind for a fixed time after each count, the blind time read from its own shortest gaps: defensible only where arrivals are physically random, and there (radiation, particle counts) the dead time is a filed instrument constant and its correction a formula; for people or vehicles the shortest gaps are as much spacing as blindness.
  - Completion as the slowest of several parallel parts (a fan-out's calls, a permit's reviews): reweighting by width lands inside the observed range, log-linear extrapolation lands near the golden beyond it, and the parallel structure shows in the log.
  - Failures of repaired units read as renewals when the units wear on: the clock-choice family of task46, task132 and task134, and its call is a forecast.
  - Emission factors applied at the mean speed or load rather than its distribution: a Jensen gap, task229's and task187's drivers; startup emissions by thermal state: a mix of operating conditions, composition (task450's rejection) and closed by the window.
  - Readings taken more often when the state is bad, time-weighted: closed-loop sampling run backwards, this slot's own architecture 1.
  - Censored costs by inverse probability of follow-up: with exchangeable cohorts the complete-follow-up cohort is unbiased too, and the two forms fork by sampling noise.
  - Late entry, competing endings, informative loss, partial verification, size-biased sampling, range restriction, ascertainment through a case and blended measurements: each spent once in this lane (task263 to task271).
- Architecture 2 draw, 2026-10-22: induced exposure on its own (each use's pooled share of the not-at-fault vehicles taken as its share of the miles) weighed as the decisive step and kept only as a rung: the field names the method, and a reader asked for a rate per mile with no mileage on file reaches for it; what decides is where that sample measures miles, within each road class and hour, scaled by the state's mileage for the stratum.
- Architecture 2 draw: drivers grouped by age band set aside, because a reader's prior that older drivers crash more per mile than per licence invites the exposure question; vehicle uses carry no such prior.
- Architecture 2 draw: the struck-while-stopped refinement (only rear-ended stopped vehicles as the exposure sample) set aside, because parcel vans and ride-hail cars stop far more per mile than private cars, so that sample measures time stopped rather than miles.
- Stage 4, 2026-10-22: a PERSON_NO clause in the dictionary ("a later report on the crash numbers on from the earlier ones"), added to file which of a person's two listings is the later one; reader r273f followed it to the later listings and kept every ask figure (14 of 14), where the three readers before it, without it, kept none; withdrawn, the persons line made neutral instead.
- Architecture 2 as shipped, spent at the portal on 2026-10-27: both responses filed the golden four (taxicabs, ride-hail, parcel delivery, app-based delivery), each saying it had estimated every use's miles, and rung R4 is the only construction that files those four, so both walked the field's own stratified induced exposure (Stamatiadis and Deacon's relative crash propensity taken where it measures miles, within road class, day type and hour, scaled by the Department's miles). The five in-house readers had stopped at R2 or R3a; a published estimator a solver reaches with the literature and forty minutes is not a stump. No redesign is left in this world: finer strata, each year apart, only struck vehicles that were moving, and the struck share read as time on the road rather than distance each stack a rung above R4, which a returned build may not do.
- Architecture 3 paper screen (2026-10-27, before any card): a tail share freed of within-unit variation (task201's candidate 14, dead on task202's driver), dual-frame multiplicity (task280's screen, population_selection), dependence across units in a pooled tail (task198's arch6 screens), change of support and a bunching counterfactual (task269's and task272's lists): each already dead on file, so no candidate is carried to a plan-only reader yet.
- Architecture 3 search, 2026-10-27, each dead on paper before a card (the coordinator's plan-only and call-only screens were not run: CLAUDE.md's STOP block bans every probe, so the draw is argued on paper):
  - mixed-population flood frequency (annual maxima from two storm types fitted apart): task255's tails by kind;
  - period fertility's timing distortion against completed cohort fertility: completing the open cohorts forks the figure, and a cohort table makes the near-complete cohorts a direct read;
  - multivariate accommodation in anthropometric design (the percentile fallacy): with individual records the joint count is the direct route, and with summary percentiles it rests on an assumed correlation;
  - cookie churn in campaign reach and frequency: identity resolution, and the logged-in subset that would calibrate it is a partial verification, dead in this lane;
  - small-unit bias in a segregation index: the shrinkage and funnel family (task183, task194);
  - protest counts that track media reach: detection, dead;
  - a GP list's registration artefact, roadworks diversions in short traffic counts, a library's floating collection, overflow between emergency call centres: each turned on reading a field or on Layer 1 mess, or left the domain a backdrop;
  - valve seizure forecast from the years since each valve was last turned: task178's candidate (held on code, died on its guard bans), a different insight and not used: the valve state here is the programme's latest recorded result;
  - a reservoir's storage outlasting a repair (the supply point as a cap in time): repair durations and storage endurance fork the figure, so the reservoir supplies through any repair, filed at stage 2;
  - one-way devices (pressure reducing valves) in the supply path: a reading of a device type would decide the call, so the network carries no one-way link a back-feed could cross.
- Architecture 3 draw, prototype p2 (the same district as a looped town grid without estates on single entry mains, at realistic densities): the seized valves moved the register by 6 mains of 82 at 500 properties and by none above 1,000, because a burst in a looped grid shuts off a few small segments whatever the valves, so the drawn-segment analysis was the golden there; the estates hung off the town on one entry main (the district's subdivision pattern, p3) are what make a valve that will not close cut off hundreds of properties.
- Architecture 3 (Carrisford Water's critical mains register, each burst's shut-off composed through the valves the exercising programme says will close, plus what it cuts off), dead on paper at stage 2 on 2026-10-27, before any data was cut: the decisive rung is readable on tests 1 to 3 (the shut-off clause the estimand needs sends the solver to the valves, the programme's operable flag makes the closable valves a row predicate once segments exist, and unreachable demand is the task type's own pattern), and deletion tests 3 (the drawing against the programme's visits is a change of lens) and 6 (the clause's natural execution plus one reflex correction is the golden) fire. The prototype's separation was real (golden 173 mains against 93 on the drawn segments and 50 by link removal at seed 5) but every move between them is shown to the solver, the coin-flip signature; a pass or fail per visit is how any valve programme records condition, and hiding it would make the call turn on a reading. Not rescued inside the architecture: the card's decisive step is this composition, and a different decisive step is a fourth architecture.
- Architecture 2 as shipped, at the portal's determinism check on 2026-10-28: both judge runs failed it. Run 1 (underspecified_objective) found the KSI and cost asks forked on the duplicate person records (the later record against the most severe, 14 figures, the cost PDF's most-severe convention on the model's side); run 2 (competing_defensible_answer) found the main call forked, the unstratified relative involvement ratio filing airport shuttles and paratransit against the golden's four, and asked for a methodology note filing the estimator and its strata, which files the method. With the call already landed at the portal there was nothing to repair; re-rooted to architecture 4 in a new domain.
- Architecture 4 search, 2026-10-28, each dead on paper before a card: a pathway counterfactual quantized by weekly meeting sittings and capacity-limited clinic sittings (a cancer alliance's 62-day standard under a one-stop clinic; a parcel network under a faster sorter): the decisive step is generic scheduling, so the swap test reads the same with depots for trusts, and the temporal-allocation screen on file (task281) records schedule replays as rule application once the schedule is read; classroom ventilation from CO2 (task279's screen: the decay method is a reflex; the lesson-time build-up against a closed-window decay needs a filed window sentence that announces it); shelf fill-to-fill windows (generic inventory, swap test); censored demand at sell-outs (a named correction the opponent enumerates); misclassification-corrected prevalence through a validation sample (adjusted classify-and-count is a published estimator, task455's register correction on file); a lot's contamination through well-mixed silos (no client task type serves a food-process call under Descriptive); OOH board audiences after dark (the lit flag decides it, a reading); HSMR coding depth (the look-back is either filed, rule application, or open, a fork).
- Architecture 4 prototype, 2026-10-28: with phase 1 depth at the founder variants left free (a negative binomial around 7 to 12 reads), the member-weighted estimator split from the per-phase one by up to 0.44 points (weights up to 64 at 6 reads) and the 20-read filter kept enough island members to land; the Study's 8-read top-up floor (a real QC rule for reportable sites) bounds every weight under three and holds the licensed family to a 0.045-point spread over 40 draws (`search3.py`).
- Architecture 4 stage 4, judge pass 1 (2026-10-28, target.zip 05374e98): NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer on the main call: every figure reproduced under the golden's construction, but the judge read policy 2.1's "carries" with the methods report's line that every member without a row "was called reference" as licensing the plain count of calls (3.4, 3.9, 3.4 per 1,000, panel 11), and found no shipped sentence choosing the correction. Its proposed repair, a filed sentence saying frequencies are corrected for calling sensitivity, files the method and is not taken. Repaired in the data instead: the reference sentence deleted (a variant-only export states only what it lists), and two genes without a founder effect given one thinly read variant each beside an ordinary one (Pompe disease c.-32-13T>G, Usher syndrome type 2A c.2299del), so inside each gene phase 1 calls the thin variant at 0.38 and 0.48 of phase 2's rate and the ordinary one level, an inconsistency that refutes the call count from the files. The leak reader's fixes went in the same pass (geography-free nominators, texture variants inside each gene's coding length with a protein change, uneven register ids, area sizes 3,187, 4,846, 11,338, 3,419 and 3,207, a 25,997-member register). Seed re-searched to 2907; TMEM216's founder rate set to 19.0 per 1,000 to clear a rounding edge. One re-judge is this architecture's last pass.
- Architecture 4 stage 4, judge pass 2 (2026-10-28, target.zip f17337a6): DETERMINISTIC, APPROVE; Gate G method_or_model_selection, Gate H domain pass, layers pass, decisive step analytical. Its one note, that the depth-filtered and pooled rival figures quoted in block 1's prose did not rebuild to their exact values, is met by dropping those figures from the prose (the plain count's figures, which it rebuilt, stay). Edits after the pass, none moving a graded figure (figures.json compared key by key): the forum redrawn to the Director of Public Health (policy 3.1, the paper's header) after `heart` BLOCKed ban.forum on task174 once task270's card was marked spent; the prompt's "for the executive team" cut (a named reader); the second reader's realism tells fixed from a separate texture stream (codon-consistent protein changes, spread dates, a word processor as the PDFs' producer).
- Architecture 4 as shipped (target.zip ea742c6b), spent at the portal on 2026-10-28: both responses filed the golden 14 conditions (ARSACS, Joubert syndrome type 2 and diastrophic dysplasia joining), one saying it computed observed and sensitivity-adjusted frequencies; the within-gene contrast added to answer the first judge pass made the missed calls visible, and once a solver sees calls missing at low depth, each phase's calls over its members' binomial chance of a call is a published correction it enumerates and executes. A named statistical correction the data make findable (detection weighting, induced exposure, coordinated omission) carries no stump in this lane; re-rooted to architecture 5.
- Architecture 5 draw screens, 2026-10-28, run on paper before any card against the lane's record (this slot's four architectures, the neighbouring slots' notes in task268 to task281, `guard.py recent`, `coverage`, `mechanisms --objective descriptive-distribution` over all 51 drivers, and `slots` on both mechanism and setting nouns). Each died on a named screen, so none was carded:
  - a second biomedical-genomics direction (a count of participants carrying a change whose consequence has to be read across the gene's own coding structure rather than per annotated change): the same spent cell as architecture 4, and the composition reduces to reading the release's annotation fields, which is data semantics as the decisive step.
  - quantitative-finance / market-microstructure-execution-cost (never drawn; which brokers or algorithms stay on a 2027 execution panel on each one's cost per order): the benchmark and the unexecuted remainder's valuation are the estimator family, so the main call forks on Gate C unless the policy files them, and filing them is rule application; the honest organisation family is also `financial_institution`, banned against task268 in the window.
  - marketing-consumer-research / media-reach-frequency-audience-measurement (never drawn; which markets a 2027 plan reaches at three or more exposures): the three mechanics the pack can carry are interval containment of each spot inside a viewing statement (a merge a careful reader runs by reflex, task270's own note), cross-device identity (identity resolution, barred from deciding), and the panel's in-tab weighting (a free weighting choice, the family this lane keeps dying on); the broadcast-rotation world is spent on paper in task270's architecture 6 probes and the radio four-week reach in its architecture 4 screens.
  - physical-environmental-sciences / emissions-inventory (which sites join a 2027 significant-source list): temporal allocation against a production schedule is rule application once the schedule is read (recorded for task482 v7 and task485 v3), concentration times flow read at the annual means is the Jensen gap spent in task229, task187 and task450, and transfer-station double counting is cross-dimensional duplication, a reading.
  - survey-research-official-statistics / complex-survey-estimation-variance, sample-design-allocation-weighting and small-area-estimation: the first is the variance-only screen (a correction that only widens moves the call one way and every conservative reflex lands it), the other two are the free weighting and shrinkage family whose spread the designation screen measures above one.
  - product-analytics / funnel-journey-analysis and metric-definition-measurement-science: the mechanics available are batched client events timed on the device clock (time semantics), cross-platform identity, and an intervention whose measured effect reaches only the units whose own served document satisfies its precondition, which is task258's driver on its own cell and approved at the portal, so the differentiation line cannot be written.
  - human-factors-ergonomics / anthropometric-design-fit (the only task type the domain serves on this objective): the share inside a box of correlated ranges is task256's driver and the percentile fallacy is recorded dead in task270's architecture 4 screens.
  - healthcare-delivery-health-economics / provider-quality-risk-adjustment (which units join a 2027 improvement programme on a rate per 1,000 at-risk days): the at-risk-day file would ship only to make the rate computable, which readability test 7 fires on, and task194's architecture 6 measured a published standardised ratio absorbing a withheld patient-flow driver on this ground.
  - the roster-pinned opportunity family that `stumping` 1.1e blesses (the censoring mechanism's parameters recorded because a contract depends on them): here the reconstruction is a calendar join a careful analyst runs by reflex, and it is already spent at ask level in task281's re-sited devices and task269's architecture 5.
- The pincer this slot has now measured four times, written for whoever takes the number next: our own rules bar the device every one of the client's measured held tasks uses (a control set the wrong construction cannot reproduce is an oracle under `stumping` 2.4, and a recovered rule is barred by rule 3), so the only refutation left to the data is an internal contrast between two shipped records. Architecture 4 measured both ends of it: with no contrast the first judge pass read the plain count of calls as a second literal execution (SEND_BACK, competing_defensible_answer), and with the within-gene contrast added both portal responses saw the missed calls and executed the published correction. A design that makes the easy route refutable from the data makes the decisive step findable, and one that hides it forks the main call. The next move on this number is the author's: a ban or clone waiver that reopens adjacent ground (the task258 reach family with a different mechanism, or a control set treated as the client treats it), retirement after four architectures, or re-tasking the number to another objective.
- The slot re-tasked by the author on 2026-10-28 (the coordinating session's decision, made after the four descriptive architectures above and the nine-direction screen of the same day): the number moves from Descriptive & Distribution Analysis to Forecasting & Predictive Modeling, retirement is not taken, and architecture 5 is drawn as a Forecasting build whose decisive step is a domain mechanic that changes how the forecast is built, visible only by joining a file at another grain, never a named statistical correction.
- Architecture 5 draw, 2026-10-28, a coastal causeway's 2027 high-water closures read through the 18.61-year lunar nodal modulation (diurnal and semidiurnal constituents swinging with opposite phase, so a short record's trend in crossings is mostly the cycle's rising half): dead on paper, because the field's own method (harmonic prediction from the hydrographic office's constants, nodal corrections included) is the golden, which puts the field's method at the top of the ladder (`stumping` 1.1b), and a count of crossings over surge residuals forks on the residual distribution and the mean sea level extrapolation.
- Architecture 5 draw, 2026-10-28, a pathology network's 2027 hub workload with each specimen's analyte stability read against the courier timetable (night and afternoon collections at the spokes outlasting the stability of unspun potassium, glucose or coagulation tubes): dead on paper, because transport feasibility against stability is the first question any consolidation planner asks (readability test 3), and the mechanic gates which items a planned change reaches, which is task258's driver by abstraction.
- Architecture 5 draw, 2026-10-28, also screened on paper and dropped: bus on-time performance through vehicle blocks and driver duties (generic scheduling, the swap test reads the same with surgeons and theatres), a diesel station's fuel after solar with its minimum load and fuel-curve intercept (task67's fixed-plus-variable driver), insulin pens' 28-day in-use life and multi-dose vaccine vials discarded at each session's end (a per-unit floor or ceiling read at the mean, the Jensen gap spent in task229, task187 and task450), O-negative red cells rotated before expiry (perishable stock rotation reads the same for any item), and inverter volt-watt curtailment on high-voltage connections (the new fleet against the old one is a validated decoy, and the voltage the curtailment needs moves with the forecast PV itself).
- Architecture 5 draw, 2026-10-28, measured on a prototype before any card: a growth area's drinking water trunk main carrying the potable top-up of a dual-reticulation (recycled water) network, the recycling plant's output the smaller of its membrane capacity and its sewage feed times recovery. Dead by identity: in a replay that scales each day's per-lot quantities to the forecast lots, production, feed and demand scale together, so the feed-limited regime cannot newly appear and "last summer's production scaled by lots and capped at the licence figure" reproduces the golden on every day (`proto/p1.py`: the cap route equalled the golden at 26.5 on the peak day, the proportional routes at 26.33); every way to break the proportionality (an old town's sewage that does not grow, trade waste, a golf course's offtake) is task67's fixed-plus-variable driver, and a factory exit or a shutdown is a forward condition the history blesses. The utility setting closed anyway when task464 v10 registered at 01:27Z with `utility_or_infrastructure`.

- Architecture 6 draw, 2026-11-01, candidates set aside before the card: the leak survey of a gas main by years since its last survey (the regrowth-clock abstraction task129 already spent); a pump station's catchment after a facility closure by each user's second choice (a closure redistribution task174 recorded as reading the same for a store); a wellfield's interference left to the field's Theis or Jenkins method as the golden (the field's method at the top of the ladder, 1.1b); the borehole idea kept with the field's method at rung 0 and the newcomer's test footprint as the step.
- Architecture 5 (the zone-substation solar soak) re-rooted 2026-11-01 at the Batch 3 queue reset with no portal result on it: the author had every queued task rebuilt as a fresh architecture; one architecture per world closed the load world.
