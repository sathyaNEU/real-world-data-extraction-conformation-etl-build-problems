# task182 design note (architecture 2)

Architecture 1 (make-good bore assessments at a central Queensland coal mine) shipped on 2026-10-11, the
portal solved it, and the slot came back `FAILED_TO_STUMP`. The diagnosis is below, written before anything
was changed. Architecture 2 is a fresh draw on the same number and objective: the card's lineage carries
architecture 1's identity and fate, `architecture` is 2 and `loops` 0. Architecture 1's own ladder, pack and
build record are not reproduced here; the card holds its identity and `## Tried and rejected` its deaths.

## PORTAL RETURN AND DIAGNOSIS (architecture 1, written before any change)

Shipped 2026-10-11, left off the author's portal list: the call landed, so the build is `FAILED_TO_STUMP`
and goes back to stage 2 (`build-pipeline`, Returned tasks).

**Which of the five diagnoses: the response executed the rung as a work order.** The rung was announced, and
the announcement is the pack's own inventory rather than any sentence.

- The decisive rung (rung 4) is each bore's own lagged climate response fitted before 4 July 2022 and run
  forward. The in-house round-1 response already held that whole architecture: its step 5 is "monthly
  pre-take (before Jul 2022) regressions of each bore on same-aquifer references ... with lags of a few
  months" and its step 6 is "mine-caused decline = predicted natural September 2026 level minus observed"
  (`solver_rounds/round-1.md`). It did not have to find the step; it had to fit it better. Its own note says
  what it swapped in instead: "the rainfall file could not reproduce the hydrographs, so it was not used for
  the correction". Between that response and the golden sat a numerical fitting exercise, not an analytical
  insight, and the portal did the fitting.
- The isolated leak reader, which saw only a fresh unzip and `prompt.txt` and nothing of the design, reached
  the answer with a lagged-rainfall model (`pipeline.json`, `leak.reader`, pass 1). A cold reader of the pack
  arriving at the decisive move is an announced rung by definition.
- **Where it was announced.** `daily_climate_1990-2026.csv` ships 13,422 days of rainfall and Morton areal
  potential evaporation, and no graded figure, ask or distractor reads it: only the decisive rung does.
  Beside it the pack files the causal quantity (MG-02 4.1, "the decline the mine's take has caused"), a
  baseline date per bore (5.1), the take's start date (the dewatering record) and three bores labelled
  outside the predicted drawdown. That is a calibration window, a driver series and a causal estimand handed
  over together. The PINS section banned the vocabulary (counterfactual, response function, cumulative
  rainfall departure) and not the presence of the one file the correction needs, which is the first item
  under what `leak.py` cannot see: "a file whose presence is the hint".
- Not the other four. Not "walked the default path to the golden": the default path (the decline since the
  baseline) names the alluvial bores and KV-LB18, and the in-house round confirms it lands wrong. Not "never
  saw the rung yet landed": it was seen, so the magnitudes are not the finding. Not "saw the rung and
  declined it": that was the in-house round, which declined the rainfall fit for KV-LB16 as a control and
  missed; the portal executed it. Not "missed only on a misread field or misapplied rule": every level,
  change and trigger in the in-house round reproduces exactly, so no lower rung was in play.

**The WHAT screen (`stumping` 1.2), run on architecture 1.** Decisive step: measure each bore's decline
against its own climate-only path fitted before the take rather than against its baseline level. It settles
**the comparison**: MG-02 1.2 files the population (the register's landholder bores), 4.1 the outcome (the
decline in water level) and the window (the September 2026 assessment level, the take from 4 July 2022), and
the register files the unit (one bore), but what the observed level is set against is exactly what rungs 1
to 4 differ on (the baseline assessment level filed at 5.1, the reference bores' change, KV-LB16's level,
the bore's own fitted path). File the comparison and the computation follows from the clause; leave it
unfiled and the call is not determinate, which is why judge pass 1 had to carry the declines on a 0.3 m
band. That is task193 v1's shape, the comparison population of a measure, and no hardening saves it.

**Routing.** The decisive step has to change, and the shared-driver mechanism is spent as a mechanism in its
own right, so the slot is re-rooted at stage 1 as architecture 2 rather than hardened: architecture 1's
identity moves into the card's `lineage` with its fate, `architecture` becomes 2, `loops` 0, and every other
axis is drawn independently.

## STAGE 4 ROUND (the judge and the reader, architecture 2)

The determinism judge returned **NOT_DETERMINISTIC, FIX_NOW**, with the call and the stump standing: all 14
specific levels, the ranked five, the critical components, the 240 residual minutes and every band and tone
verdict reproduced from the bundle on its own code path, Gate G and Gate H passed, and probe 1 confirmed the
design (LA90, a median, an arithmetic dB mean or no subtraction each put the sixth position in and the fifth
out, and each contradicts plan 3.1). Five supplementary answers were not forced and one write-up line was
wrong. The isolated reader reached the five dwellings from the bundle alone and listed the same open choices,
plus a realism list.

**What this pass changed, in one generator pass.**

1. **The instrument's own columns were impossible.** The reader measured 36 per cent of minutes with LAmax
   below LAeq and 13 per cent with LA90 above it; the judge found 77 minutes of one residual window reading
   -120.2 dB LAeq while LA90 in the same minutes read 6 to 33 dB. The cause was one index: `residual_shape`
   read the position tuple's event rate as its steady share and its quietest-interval figure as the event
   rate, so the residual's steady term carried a negative coefficient and the within-minute statistics came
   out in the wrong order, with the negative energies clamping to -120. Fixed at the index; the ordering
   now holds on every shipped row and is asserted there and in the verifier. The -120.2 values were that
   bug, not a sentinel: a real dropout is now built on purpose, three spells named in the deployment
   remarks, filed as a rule in plan 4.2 and as a fact in the notes, written into all four level columns and
   never inside a process stop.
2. **The rain test.** Clause 4.2 asked for a rate ("above 0.5 mm an hour for the ten minutes") while the
   golden read a trailing hour, which moved every minute count by 30 to 130. The clause now files the test
   as the gauge's own count of tips in the ten minutes, and the nearest reading a solver could reach for, a
   rate on the same record, selects exactly the same records (one tip is 1.2 mm an hour), asserted record by
   record. The notes file which end of its ten minutes a met record is stamped at.
3. **The week's process figures.** Plan 5 is new: 5.1 files a week's figure as the counter reading at 00:00
   on its Monday taken from the reading at 00:00 on the Monday after, with the roll-over added back, and
   says a spell the historian did not record leaves those readings as they stand; 5.2 files a centrifuge run
   as one start in the equipment log. The blower header now ships as a totaliser beside its rate channel,
   so the gap week's delivery is 700 against the rate sum's 617, and the runs come from the log (10 to 13 a
   week) rather than from feed blocks (6). The write-up's "two deployments" is now the 11 of 28 the plan's
   window catches, emitted from the generator.
4. **Two construction tells.** Ten of 14 levels sat within 0.002 dB of a one-decimal value; every printed
   level now sits 0.018 to 0.033 dB off its own printed value and 0.017 dB or more from its rounding edge,
   and the flip conditions are stated as numbers in the ladder section. The top band at NSL09 was decided by
   0.04 dB; the two tones' survival now turns on screening as well as distance, which is how a barrier
   works, and every position's highest band wins by 1.07 dB or more with every tone verdict 1.48 dB or more
   clear of the 5 dB test.
5. **The reader's realism list.** The plant's own load now moves over the day and the week, so no position's
   hourly means are flat (1.2 to 1.6 dB of spread); the minute-to-minute swing of the source gives minute
   standard deviations of 0.70 to 2.31 dB with lag-1 autocorrelation 0.44 to 0.68 and 11 to 16 per cent of
   consecutive minutes equal, where it was 37; the one-third-octave excess now differs between a position's
   two deployments; the field checks differ deployment by deployment and the certificates moved to their own
   file; the deployment record carries who deployed each meter and the height it stood at, which the
   schedule now matches; the complaints register carries 24 distinct texts with the channel each came in on;
   the met mast's wind has a diurnal cycle (2.3 to 4.2 m/s by hour) and a direction that sits for a day
   rather than sweeping; the effluent file carries a laboratory, its references, detection limits and
   non-detects; and the export manifest is a provenance record with the source, extract date and licence of
   every file instead of a tidy list of the gaps. The five pieces of mess the reader read as real (the
   dropout, the repeated download, the counter roll-over, the replaced hour counter and the historian's
   gap) are all kept.
6. **The Gate H caveat** ("3.1 and 7.1 give most of the recipe, so the step is close to rule application")
   is answered in the `Not rule application:` line of `## Three rules`, which names the step no filed clause
   performs.
7. **The ask layer, re-cut.** The band and tone table (28 criteria) became a three-criterion summary, the
   excluded-minute column went, and the weight moved to two quantities the decision needs that run through
   the plant's own records: the minutes behind each level that a centrifuge was running and the runs they
   span (28 criteria), and the blower air, centrifuge runs and engine hours per survey week (18). Both sit
   on a device the pack already had and nothing filed adjudicates on the solver's path: the plant records
   the same facts twice, as an event log to the minute and as a fifteen-minute channel that cannot resolve
   a start, and the historian holds no rows at all for six spells. Biogas was dropped from the ask, because
   its two reading paths differ by only a few cubic metres. The plant's own pattern was opened up to carry
   it: the dewatering shift's hours now move day to day, two days have no dewatering at all, and the gas
   engine comes off load on its own five times, which the equipment log, the process channels and the sound
   record all show together (a 1 dB dip at the positions while the blowers carry on).

**What this pass cost, and the pass that paid it.** Four of the five fork closures removed a way for a
careful solver to miss a supplementary figure: measured, the ask layer fell to a pair ceiling of 69.2
against a bar of 40, with 28 forced criteria on the band and tone table and 28 more on minute counts whose
every convention was now filed. The ask layer was then re-cut, in this same pass, onto the quantities the
decision needs that run through the plant's own records, where the devices live. `generator/cracker.py`
scores it on the cut pack, and the measured ceiling is 39.1 with 4.3 per cent mirror leakage. The whole
arithmetic, and the sensitivity against a perfect clause-executing reader, is in `## Ask sheet

The ask layer was re-cut after the round-2 measurement. The figures it carried (the dewatering minutes and
runs behind each level, and the week's runs and engine hours) were quantities a filed rule answered once
the judge forced the run definition, the minutes basis and the overlap to be written out, so the device
they rode on was the ambiguity and not the data: ban 1 forbids a device a filed rule adjudicates, and once
the rule is filed, it does. The weight moved to quantities whose correct computation needs a step no filed
sentence performs, found by an internal inconsistency only, on rows the call reads for nothing.
`generator/cracker.py` scores them on the cut pack.

| Ask | Figures | Home (H18) | Primary device | Shared hazards | Files on the path |
|---|---|---|---|---|---|
| A1 the 14 specific levels, the slate, the sixth, its margin and the ranked chart | 21 | the call's own construction | none (construction); the cracker has it by design | the Layer 1 set | plan, register, deployments, parquet, met, event log |
| A2 the air the blowers delivered, through each position's assessment period and through each survey week | 20 | the plant's load behind each level, which is the qualifier the note's comparability claim rests on | D5/D9, the header's flow meter is upstream of where the third blower was tied in at the upgrade, so the channel named for the blowers' air is two machines of three. Nothing says so: the records do. The air per cubic metre the works treats holds to 4.9 per cent week to week on the two meters together and swings 24.1 per cent on the header alone, each counter's quarter-hour step is its own rate channel and nothing else, and the duty rotates so BL-03 carried 0.24 to 0.40 of the air | D4 the historian's six dropouts, which put the rate route out by 8 to 13 thousand Nm3; D2 the biogas counter's roll-over and the hour counter changed mid-survey; D6 the quarter-hour grain against the assessment period's own hours | SCADA, deployments, plan, register, notes |
| A3 the quarter hours the historian did not record the plant's state in, and the longest unbroken run of them, per position and per week | 40 | the audit trail of that qualifier: how much of the plant's record behind a level is not there | D1/D9, when the link to the PLC drops the interface holds the last value it had and writes it again, so the row is there and the quarter hour's state is not. Found by what the rows are: a counter standing still while its own rate channel reads above zero, and every channel the same as the row before. Nothing narrates it, and the held spells sit against the week's own dropout, so the run the record does not cover is longer than the run of rows it is missing | D4 the dropouts themselves (half the answer); D6 the stamp convention, which cannot move the count because no window edge is a quarter hour the record misses | SCADA, deployments, plan, register |
| A4 whether a tone is prominent, where, and in which band | 3 | the mitigation case: a tonal source takes different treatment | none (forced); kept small for that reason | D8 time base, D4 the meters without the band module | third-octave file, plan, deployments |

**The ask ladders, measured on the cut pack.** A2 at NSL01: the header's rate summed 344.8, the header's
counter alone 354.5 (the cracker), both rates summed 508.8, both counters 521.4 (the answer). Week by week
the cracker's air is 528, 431, 484, 415, 492, 466 against 694, 684, 672, 691, 665, 676. A3 at NSL01: none
noticed 0, the rows the historian is missing 11 (the cracker), the quarter hours it holds no record of 20
(the answer), and the longest run 11 against 14. Every stop is a complete, competent pipeline and every one
of them lands outside the bin.

**Separation.** Zero device rows sit in the main call's declared population: both primaries live in
`scada_15min_2026.csv`, and the call reads that file for nothing. Asserted by deleting it and recomputing:
every one of the call's figures, the fourteen levels, the slate, the sixth, the margin, the valid, excluded
and stop minutes and every tone verdict, reproduces from the rest of the bundle (over 200,000 checks on
`verify.call_only`). The call reads the event log only for the intervals in which every source is down,
and no ask reads the log at all.

**The referee.** One, and it hands over no figure: the works' own inlet flow channel, against which the
air per cubic metre treated is steady on the two meters together and not on the header alone. It states no
air figure and no level.

**The cracker sheet.** The cracker landed the call, ran the hygiene battery (key uniqueness, exact
duplicates, unmatched joins, fan-out, count ties) and executed every filed rule it points at: plan 5.1 for
a process figure read off the plant's own counters at the boundaries of its window, 3.1, 3.2, 4.1 and 4.2
for the level and its valid minutes, 4.3 for tonality. It takes the records at face value, which means the
channel named for the blowers' air is the air and a row the historian wrote is a record. Scored figure by
figure on the cut pack by `generator/cracker.py`, and asserted in `generator/checks.py`.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A2 the air behind each level | the counter named for the blowers' air, at 07:00 and 19:00 on each weekday of the position's deployments | wrong at all 14, short by 149 to 167 thousand Nm3: the header meter is upstream of BL-03's tie-in | the two counters the plant's three blowers are metered on, over the same hours | miss |
| A2 the air, six weeks | the same counter at the week's own boundaries, per plan 5.1 | wrong in all six, short by 166 to 276 thousand Nm3 | the two counters at those boundaries | miss |
| A3 the quarter hours not recorded, per position | the stamps the historian wrote no row for | wrong at all 14: 9 to 13 short, because the rows that hold the quarter hour before them are rows | the stamps with no row, and the stamps whose row is the one before it written again | miss |
| A3 the quarter hours not recorded, six weeks | the same count over the week | wrong in all six: 5 to 12 short | the same, over the week | miss |
| A3 the longest run of them, per position | the longest run of stamps with no row | wrong at all 14: the held spells sit against the dropout and lengthen the run | the longest run of quarter hours the record does not cover | miss |
| A3 the longest run of them, six weeks | the same over the week | wrong in all six | the same, over the week | miss |

**Pair ceiling:** 37.3 (ask weight 55 over 84 criteria, 0.655 a criterion: the cracker banks A1's 21 and
A4's 3 and misses every one of the 60 device criteria, so 24 of 84, 15.7 points, and 38 + 7 + 15.7 = 60.7;
the mirror, which stops at the statistical-background rung, keeps A4's 3 alone, 2.0 points, and 5 + 7 + 2.0
= 14.0; the pair averages 37.3)
**Mirror leakage:** 3.6
**Measured by:** `generator/cracker.py`, run as code on the cut pack after every change, with every device
row asserted to miss in `generator/checks.py`

**The rule this build paid for.** A device that evaporates when every term of its ask is written out fully
defined was never a device: it was the ambiguity wearing one's clothes, and it is collected either by the
determinism block or by the ask measurement. The design-time test is to write each ask's terms out fully
defined first, and then ask whether the device still bites. These two do: the air is short whatever the
wording, because one meter does not see one machine, and the record is thinner than its row count,
whatever the wording, because an interface that holds a value writes rows that are not records.

## Pack

| File | Format | Role |
|---|---|---|
| `sound_levels_1min_2026.parquet` | parquet | spine: one minute of logged level per position (LAeq, LA90, LAmax, LAmin), the handling and field-check minutes at either end of each record, the volume gate |
| `meter_deployments_2026.csv` | csv | which meter at which position, the minute it was set running and the minute it was stopped on the next round, the height it stood at, the field check either side, who deployed it, remarks |
| `monitoring_positions.xlsx` | xlsx | context artifact: the register of positions, dwellings, distances, bearings, screening |
| `noise_management_plan.pdf` | pdf | governing document: the quantity, the period, the validity criteria, the tonality test, the slot |
| `survey_notes.md` | md | the technician's notes: meters, identities, time base, met channels, file conventions |
| `plant_equipment_events_2026.csv` | csv | the process operator's equipment log: every start and stop of a blower, a centrifuge or the gas engine, per machine, with the shift's reason |
| `scada_15min_2026.csv` | csv | plant process channels at fifteen minutes: the blower header as a rate and as a totaliser, the biogas counter, the centrifuge feed, the engine's export and hour counter, the inlet; six spells missing where the link dropped |
| `weather_10min_2026.csv` | csv | the met mast at ten minutes: wind, rain, temperature |
| `third_octave_15min_2026.csv` | csv | one-third-octave band levels per position and quarter hour |
| `calibration_records_2026.csv` | csv | the laboratory certificates for the five meters and the field calibrator, as found and as left |
| `complaints_register_2026.xlsx` | xlsx | distractor, declared in metadata.json: complaints, dates, dwellings |
| `effluent_quality_2026.csv` | csv | distractor, declared in metadata.json: the laboratory's discharge results, with its references, detection limits and non-detects |
| `export_manifest.csv` | csv | provenance: per file what it is, what it covers, the system it came off, when it was extracted and on what terms |

## Build record

- `generator/build.py` runs everything: the survey (`world.py`, `sim.py`), the pack (`pack.py`, `docs.py`,
  `postprocess.py`), the golden (`golden.py` over `analysis.py`, `deliver.py`), `metadata.py`,
  `figures.py`, `submission.py`, then `checks.py` and `verify.py`.
- Final run: `checks.py` **1,263 assertions passed**; `verify.py` **282,108 independent checks passed**
  (the per-minute instrument-ordering check runs on every shipped row, which is most of that count); two
  consecutive builds byte-identical over `target/`, `golden/` and `metadata.json` (combined sha256
  ab9b5efda9bb4309); about 11 seconds.
- `verify.py` reads only the bundle (standard library, numpy-free, pyarrow for the parquet), encodes the
  plan's clauses as its own code and rebuilds every figure: the fourteen specific levels, totals,
  residuals, valid, excluded and stop minutes, each level's distance to its rounding edge, the slate, its
  order, the sixth, the margin and its distance to its edge, the default path's own slate, the highest band
  and tone verdict at every position, the six weeks of plant figures with each week's air measured against
  the whole-unit edge, the log's one unstopped start, and the per-position runs twice over (minute by
  minute, and by interval arithmetic against the deployment record's windows), against
  `generator/figures.json` and against the golden table. It also checks, on every shipped
  minute, that the four level columns order as an instrument reports them and that a minute with no
  measurement carries no statistics.
- `figures_check.py` exit 0: 68 figures in blocks 1 to 4, none absent from `figures.json`.
- Parameters chosen by search in scratch and never shipped: the designed specific levels and residuals
  (`world.POSITIONS`), the residual texture (`EVENT_DB`, `JITTER`, `SLOW`), the plant's own load curve and
  minute-to-minute swing (`sim.plant_load`), the propagation to each position (`sim.plant_propagation`,
  which the normalisation takes the mean out of, so it moves the spread of a record and not its level),
  the evening and night texture (`world.NIGHT_TEX`, 0.2), the within-minute depth of the plant's own level
  (`world.F90`), the blower trim's draw (`world.AIR_SEED`, 2, scanned for a week set clear of the
  whole-unit edges), the two tones' survival to each position (`BARRIER`, `TONE_K`, `pack._spectra`) and
  the per-position micro-adjustments (`world.SHIFT`, at most 0.93 dB) that leave all 14 printed levels
  distinct, each 0.015 dB or more from its rounding edge and 0.018 dB or more off the printed value itself,
  so no level sits on a round number. Two of those moved this round: NSL06's, which carries the margin
  (ruling 6), and NSL09's, which keeps the repeated-download reading inside its own printed tenth.
- The deployment windows come from `world.visit`, the Monday round: a start time per meter per week, the
  record running from the minute the meter was set going to twenty minutes before the next round reaches
  it. The week's own series is generated on the week grid it always was and the collection Monday's
  minutes continue it (`sim.residual_shape`'s `i0` and `carry`), so no printed level moved when the
  records stopped being a round week.
- Invented names: Drumlorne, Tulcarra Foods, Clonaraght, and the townland-style dwelling names in the
  register, checked against the thirty-one Irish local authorities and the sixty largest towns (edit
  distance above 2, no containment). No offline register of Irish townlands was available, which is
  recorded here as the limit of that check.

## Leak check (mechanical half)

`leak.py task182 --asof 2026-10-16`: **REVIEW, no LEAK**, four lines, each answered here.

- Sweep 3, `noise_management_plan.pdf` carries three of five distinctive words of the committed call: the
  words are October, treatment and slot, which clause 7.1 needs to say what the mitigation programme is. No
  figure of the answer appears in any shipped file (asserted: no shipped file holds a specific level, a
  residual level or a corrected level for any position).
- Sweep 4, the plan carries ten and the survey notes seven of the stump paragraph's twenty-five terms:
  they are the field's own nouns (position, measured, residual, record, reading, register, process,
  counter, deployment), and the plan defines the residual because the estimand has to be filed. The
  sweep's own test is whether the document names the move; it does not, and `checks.py` asserts the plan
  names no background, percentile, L90, stop or non-operating state, and the notes name no residual,
  background, percentile or stop window. The notes lost their bolding and their sentence about the early
  morning at the roadside positions this round, so nothing in them points at a window at all.
- Sweep 9, `calibration_records_2026.csv` carries six dates after the as-of: they are the five meters' and
  the calibrator's verification due dates, a forward validity window, which `reduce-house-fixes` H16 puts
  on the allow-list.

`guard.py surface task182`: 220 pairs in scope, **0 promoted**; nearest neighbour task228 at 0.096.
Personas in the cut pack: Aiden Hawthorn and Orla O'Hurley, with the engineer and the operations manager
by initials on the deployment records. `guard.py heart task182`: **WARN, not BLOCK**; nearest driver 0.07
(task263), answered in the card's differentiation.

## Pre-ship check (client, eight points)

1. **Domain.** The build is a noise survey reduced to one attributable level per dwelling, which is the
   acoustics practitioner's own determination of a specific sound level. The swap test breaks it: another
   field's nouns have no energetic summation and no quantity that the source's own presence makes
   unmeasurable.
2. **Real work, nothing planted.** The inputs take work to put in order: UTC meters against local
   paperwork, five meters rotated over fourteen positions on a Monday round that starts at a different
   time each week, records that are not a round week and carry the technician's own handling and field
   check at either end, a field check either side of all 28 deployments with 11 of them outside the plan's
   window, a met mast at ten minutes with a mid-survey unit change and a tip counter, minutes the meters
   recorded nothing for, a repeated download, three names per position, and band levels on three meters of
   five. Every one of them comes from the survey's own equipment.
3. **The flip is a method choice.** What flips the call is where the residual term of the plan's own
   subtraction is measured: the position's own running record, or the minutes inside the plant's weekly
   process stops. The plan files the quantity and no method.
4. **The analyst test holds.** A strong analyst who cleans every reading and executes every filed clause
   still files NSL03, NSL04, NSL06, NSL11 and NSL12, and `checks.py` runs that route on the clean truth and
   asserts it.
5. **One defensible method.** The plan fixes the population, the outcome, the window and the unit; the
   residual is measurable only where the plant is down, and every licensed reading of that measurement
   gives the same fourteen printed levels and the same slate.
6. **No decoy.** Nothing is planted and no document argues a position: the complaints register holds
   complaints and no levels, the effluent file is unrelated monitoring, and no memo or draft ships.
7. **Nothing hidden and recovered.** No certified or published figure ships for a method to reproduce. The
   residual is measured, not recovered.
8. **A new lesson.** A quantity defined as a difference has to be measured where the difference is
   observable, and the windows that make it observable come from the operating record of the thing being
   measured. The guard's heart check found no near driver (nearest 0.07).

## Tried and rejected

- Seed AD05 as written: a prescriber's high-dose count pinned by the board's reviewer determinations, which is a
  certified-figure replay. Its world repeats task180's role, forum and organisation family.
- Left-censored arsenic results across a laboratory reporting-limit change (a bore watch list for a water company).
  It had the same gap, G-code and Gate G as task134, a third censoring stump in a row, and its forum, forcing event,
  organisation family and shape would have repeated task228 and task229, which sort after task182 in draw order.

- A wet 2021-22 season (the design's "wet 2020 to 2022"): every alluvial and basalt baseline then sat at a peak, so the
  decline from the 2012 to 2022 mean (rung 1b) fell under the trigger at most alluvial bores and at B4. The 2021-22
  season is average and the wet seasons are 2019-20 and 2020-21.
- Short alluvial responses (shape 1, 60 to 110 days) with each gain set from its baseline decline: single storms lifted
  the water table 10 to 30 m, above ground. Alluvial responses are 140 to 200 days at shapes 1.5 to 2, and six datums
  were deepened so every water table stays 1.5 m or more below ground.
- Coal-measure responses of shape 1 to 12 with means of 3.5 to 6.5 years: with failed seasons at 55 per cent of the
  mean rainfall, each had stopped rising by 2026 as the drought reached it, so the rise the mine hides was gone or
  turning. Shape 16 with means of 6.2 to 6.8 years keeps it rising through September 2026 (asserted).
- An exponential family without delay and a rainfall-departure family without lag: no positive rainfall response exists
  at short lags for the coal-measure bores, so a plain exponential has no fit and a no-lag window reads A1 alone. Both
  families carry a fitted delay or lag.
- The single-window regression taken at face value: its fitted slope is negative at every coal-measure bore, which
  forecasts a rise in the drought and put CM3 into rung 3's set at 4.5 m. A negative slope is read as no response (the
  bore's pre-July 2022 mean).
- A basalt reference falling about 1.5 m (the design's figure): B4 would then need at most 5.25 m of decline for rung 2
  and at least 6.25 m for rung 1. The basalt reference falls 5.16 m, the alluvial ones 4.84 and 5.02.
- A robust outlier rule on the median of all dips within 60 days (5 MAD): it flagged 31 fast seasonal falls and missed
  33 pumped dips. Replaced by the median of up to two readings either side within 50 days, with pumped drawdowns in the
  alluvium of 1.7 to 2.8 m.
- Coal-measure drawdowns of 7.4 to 9.2 m: the rainfall-departure family put CM4 at 5.9 to 6.1 m, inside the 25 per cent
  margin. Raised to 8.1 to 9.4 m.
- The property name Tea Tree Flat: the people scan reads "Tea Tree" as a person. Renamed Lancewood Flat.
- Cutting KV-LB05's first logger record at 11 February 2019 to match its "no data since" comment: it takes 15 days out
  of the fit behind KV-LB05's 9.3 m. The comment now agrees with the record (a low battery warning at that visit).
- AD04's temporary-pump volume carved out of pit sump 1 (AD03's out of pit sump 2), then a random litre nudged between
  meters until each day summed right: pandas sums a day's printed volumes with Kahan compensation, and on days such as
  17 April 2023 the six smaller volumes cannot land on the one-ulp-high double the four-meter file gave, whatever
  litre is moved between any two meters. Both carved out of pit sump 2 (pit sump 1 only when it ran low), which keeps
  the addends' error capacity, a deterministic search over meter pairs and shifts reproduces every day's double.
- The dip remark "dusty" (EM writes "Dusty"): the people scan read "Dusty Dogs" (beside "Dogs tied up") as a person.
  Renamed "dust about".
- The coarse-grid gamma fit as the golden's printed decline (shapes in ten steps, 40 means, f in steps of 0.025): it
  left KV-LB04 at RMSE 0.22 m where a continuous fit reaches 0.027, and 11 of the 18 one-decimal declines did not
  reproduce (judge pass 1). The golden refits continuously and the decline is graded on a ±0.3 m band; the call, the
  impaired set and the offers did not move.

- Architecture 2's first draw, a static flux chamber campaign on a capped landfill (the rate at placement
  against the straight-line slope over the deployment): killed at the ladder measurement, before any file was
  cut. Measured on 120,000 parameter sets under the constraint that the golden slate keeps a 1.20 boundary
  gap: the quadratic initial slope lands the golden slate in 97 per cent of them, a ten-minute window in 84
  per cent, and in every set where both miss, their own boundary gaps fall under 1.15. The straight-line
  bias is a monotone function of one visible feature, so every partial correction walks toward the answer and
  a response that merely notices the curvature lands the call; the top two would have averaged about 59.
  Replaced by a mechanism whose wrong routes are not partial versions of the right one.

- Architecture 1, the shared-driver counterfactual (which landholder bores the mine's take drew down past
  the 5 m trigger, each bore's decline read against its own climate-only path fitted before the take):
  shipped 2026-10-11 and solved at the portal, FAILED_TO_STUMP. The portal response executed the rung as a
  work order, which is the diagnosis written above: the in-house round had already held the
  fit-before-the-take construction, the isolated leak reader reached the answer from the pack alone with a
  lagged-rainfall model, and the WHAT screen then killed the design outright because the decisive step
  settles the estimand's comparison, task193 v1's shape. Re-rooted at stage 1 rather than hardened, the
  mechanism being spent in its own right.

- The residual texture read off the wrong tuple fields (`ev, strm = p[8], p[9]`): the steady share came out
  as 0.4 to 5.1 and the event rate as 3.4 to 11.3, so the steady term carried a negative coefficient. It
  produced 36 per cent of minutes with LAmax below LAeq, 13 per cent with LA90 above it, and clamped
  negative energies to -120.2 dB, which both stage-4 threads found from opposite sides. One index.
- Clause 4.2's rain test stated as a rate (0.5 mm an hour on a ten-minute record), with the golden reading a
  trailing hour: 30 to 130 minutes a position between the two readings, and the judge was right that neither
  is forced. Replaced by the gauge's own count of tips, which the nearest rate reading matches record for
  record.
- The blower air taken from the rate channel alone: the historian's 20-hour gap loses about 84 thousand Nm3,
  so "the air delivered in the week" had two defensible answers. The header now ships its totaliser too, and
  plan 5.1 files the boundary readings.
- Centrifuge runs counted as blocks of feed in the process channel: 6 a week against the equipment log's 10
  to 13, and nothing said which was a run. Plan 5.2 files it.
- Printed levels tuned onto the one-decimal value (ten of 14 within 0.002 dB): a tuning signature the judge
  read straight off the figures. The scan now targets an offset of 0.018 to 0.033 dB from the printed value.
- The two tones' survival set by distance alone: the 100 Hz and 400 Hz bands crossed over between 240 and
  300 m, so the highest band at NSL09 was decided by 0.04 dB. Screening now takes the higher tone much
  harder than the lower one, and the thinnest band gap is 1.07 dB.
- A second ask-side device for A4, searched and abandoned in this pass: an A-weighted reading of the band
  levels (closed by the column names and the notes, and it moves only 2 of 10 answers), a band export in
  local time (converges), a wider window (moves nothing), a module serial needing a crosswalk and a repeated
  band block (both surfaced by the hygiene battery's join and duplicate checks). The band world as built is
  a robust physical measurement; a device aimed at it either breaks a clearance the judge asked for or is
  caught by the battery, so the ask sheet records the cracker's hit instead of claiming a miss.

- The ask layer as it stood after the determinism closures: measured at a pair ceiling of 69.2 against a bar
  of 40, because 28 criteria of band and tone and 28 of minute counts were forced and device-free once every
  convention behind them was filed. Re-cut onto the process records rather than defended on paper.
- A device aimed at the band and tone world, searched and abandoned: an A-weighted reading (closed by the
  column names and the notes, and it moves only 2 of 10 answers), a band export in local time (converges), a
  wider window (moves nothing), a module serial needing a crosswalk and a repeated band block (both caught
  by the hygiene battery). The band world is a robust physical measurement; the ask was cut to three
  criteria instead of being propped up.
- The biogas figure as an ask: the single-pass increment path and the boundary reading differ by 0 to 3 m3,
  so five of six weeks missed and one hit by luck. Dropped from the prompt rather than tuned.
- The union of the two centrifuges' run intervals as the device for the per-position ask: summing the
  machines' durations instead gives nearly twice the window, which is impossible on its face and so loud,
  not silent. The device is the channel's quarter-hour grain and the historian's gaps, which are both quiet
  and bite every row.
- Stops of different lengths (105 to 145 minutes) to vary the residual windows: the two deployments of a
  position then held different numbers of minutes, and the pooled residual stopped agreeing with the mean of
  the two at one decimal, reopening SF11. The inspections are 120 minutes again, started when the shift got
  to them, and the engine's own stops carry the weekly variation instead.
- The engine's stops modelled only in the log and the channel: the sound record would have shown nothing
  when a fifth of the plant came off load, which is the kind of contradiction between shipped records a
  judge is right to call. The plant's sound is now built source by source, so an engine stop shows as a 1 dB
  dip while the blowers carry on.

- The record generated over its own window once the deployments stopped starting at Monday 00:00: the
  residual's draws moved with the window, which moved the stop-window residual and every printed level. The
  week's series is generated on the week grid it always was and the collection Monday's minutes continue it
  (`i0` and `carry`), so the levels, the totals, the residuals and the minute counts are what they were.
- Sorting the deployment list by the new start times: it reassigned every `D` number and with them the
  field-check sequence per meter, so the corrections moved. The list is still ordered by date and meter and
  only the stamps are new.
- The propagation term at five times the amplitude it ships at (plus or minus 4 dB at 300 m): it overstated
  what the field sees and it flipped the LA90 rung's own 0.08 dB boundary, which the stump sentence names.
  Scaled to the 1 to 3 dB a receptor at 100 to 500 m actually swings, with the within-minute factors drawn
  on the week grid so only the propagation moves that rung.
- The evening and night texture at full amplitude: measured, at 0.45 of full the weekday hours before 05:00
  landed the golden slate, because the texture's own size tracks each position's event rate and so tracked
  the residual's ranking. Cut to 0.2, where every night, Sunday and centrifuges-off window files a slate
  with NSL06 in and NSL13 out, asserted window by window.
- A per-position residual diurnal shape as the answer to the reader's "same shape, scaled": it moves the
  residual inside the stop window and so every printed level and NSL04's two critical components. The
  propagation carries the per-position shape instead, and the texture that does touch the residual is
  confined to 19:00 to 04:30, outside every assessment period and every stop.
- NSL13's own level as the margin's lever: ruled out by the author, NSL13 being the fifth. NSL06's level
  carries it, at the cost of the sixth-to-seventh gap falling to 0.062 dB, which is reported.
- The engine hour counter made exact to the minute, which would have answered the reader's "regular
  increments": it collapses the counter onto the log's own up-time and spends the only disagreement the
  weekly engine figure rides on. The counter still steps 0.25 a running quarter, which is what an hour
  counter does; the channels that were white noise around a sine are the ones that changed.
