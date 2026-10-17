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
arithmetic, and the sensitivity against a perfect clause-executing reader, is in `## Ask sheet` below.

## STAGE 4, ROUND 2 (the seven rulings, and what each cost)

Round 2 of stage 4 returned **NOT_DETERMINISTIC, FIX_NOW** again, with Gate G and Gate H passed and Gate F
moderate: the call, the stump and the decisive step stand, and the findings were on one shipped log
sequence, the per-position runs column, two unstated bases, two rounding edges and a realism list. The
author ruled on all six findings and on the realism pass; the rulings are the specification this round
executed, and every fix is in the generator.

1. **The 10 September CF-02 sequence stays, and the golden stops reading it two ways.** The log carries a
   stop at 13:06, a second stop at 13:38 for a machine already stopped, a start at 14:06 the log never
   stops, and the next start for that machine on 11 September at 06:16. Two starts with no stop between
   them is a cardinality violation the log carries on its own, so the device is findable without the other
   records and it stays. What was not allowed was the golden treating that start as spurious for the
   per-position minutes while the weekly count of 13 counted it as a start. Plan 5.2 is reworded (a run is
   a start and the first stop the log records for the same machine after it; a start the log does not stop
   before that machine starts again is not a run; a week's runs are the runs that start in it), and
   executing that wording gives the weekly runs, the per-position runs and the per-position minutes on one
   reading, the unstopped start excluded from all three. The week beginning 7 September is 12 runs.
   `checks.py` asserts the cardinality rule and names the one start it holds, and measures the naive count
   that keeps it (13) beside the 12 the clause gives, so the hazard is measured rather than asserted.
2. **The per-position runs column was a golden bug and an undefined term, and both are fixed.** The
   committed 14, 14, 11 ... came from counting only the first run that covered each minute, which is a
   CF-01-only reading. The term is now defined in the asking sentence (a run reached into the period when
   it overlaps any minute of it), the golden computes exactly that from the log under the new 5.2, and the
   column is 22, 22, 18, 22, 22, 18, 18, 18, 23, 23, 20, 20, 15, 19. `verify.py` recomputes it twice from
   the bundle alone, once minute by minute and once by interval arithmetic against the deployment record's
   own windows.
3. **The minutes basis is stated in the asking sentence.** "The valid minutes of its assessment period a
   centrifuge was running": the committed figures were valid minutes only and the two bases differ by
   about a fifth (4,306 against 5,336 at NSL01). Every figure, unit and rounding word is otherwise
   unchanged, and the call sentence is untouched (963 characters, `voice-check.py` exit 0).
4. **Every weekly blower figure is off its rounding edge.** The week beginning 21 September sat at exactly
   699.5 against a whole-unit ask, and the other five sat 0.1 from theirs, because the trim's own variation
   was invisible at the totaliser's printed resolution. The blower header now follows its dissolved-oxygen
   trim (an AR(1) wander on top of the diurnal shape), so the totaliser's quarter-hour steps are not all
   equal, and the draw was scanned for a week set clear of the edges: 688.7, 667.9, 677.8, 701.1, 659.0 and
   683.0, every one of them 0.2 or more of a whole unit from its edge, asserted per week in `checks.py` and
   again in `verify.py`.
5. **The minute file's stamp convention is filed at authority, once.** Plan 2.2 already filed that the
   meter stamps in UTC; it now reads "each record at the start of the interval it measures". That is the
   sentence in the pack that speaks for the instrument, and it is not the survey notes. The pack ships no
   logger manual and the deployment record is a flat CSV with no description block, so neither of the two
   homes the ruling named exists; the clause that already files the other half of the same convention is
   where a real plan states it. The survey notes do not restate it (asserted). This closes the reading that
   moved four printed levels by a tenth and the margin from 1.3 to 1.2.
6. **The fifth-to-sixth margin is off its edge.** 1.2548 sat 0.0048 from the 1.25 edge. The lever is
   NSL06's own level, since NSL13 is the fifth and the five levels are frozen: NSL06's specific level is
   44.6817 (printed 44.7, 0.032 from its edge, 0.018 off its printed value) and the margin is 1.2877
   (printed 1.3, 0.038 from its edge). The five levels, the sixth's printed level and the printed margin
   are byte-identical to the shipped build. The cost is the sixth-to-seventh gap, which falls from 0.098 to
   0.062 dB, because the margin can only be moved by moving the sixth's own level; it is reported in the
   ladder section rather than tuned away.
7. **The realism pass, item by item.** The plant's sound now reaches each position through the weather: a
   downwind-and-upwind term on the mast's own wind and the position's bearing, a night-time inversion that
   grows with distance and calm, and turbulent scattering minute to minute. Measured on the shipped
   columns, the minute level now correlates with the wind's direction at -0.35 to +0.67 by position (0.02
   before), with its speed at -0.25 to +0.32 and with temperature at -0.39 to +0.06, and a night minute
   moves 0.6 to 2.7 dB about its hour (0.4 to 0.7 before). Two positions measured in the same week no
   longer carry one shape between them: their hourly means correlate 0.15 to 0.90, median 0.60, over 52
   pairs, where a shape that was only scaled would sit at 1.00. The plant's own step times are still shared,
   because one plant is being heard at fourteen places and the dewatering shift starts when it starts;
   what differs position by position is how much of it arrives. The round is now a round: the five meters go in and come out at
   different minutes of the Monday morning between 04:48 and 06:41, no record is a week of minutes (25
   different lengths from 9,948 to 10,159), and the record carries what the technician did at the
   microphone, the handling minutes as the tripod goes up and comes down and the field check itself, which
   reads the level the deployment sheet records, to the tenth. Every one of those minutes falls outside
   every assessment period and outside every process stop (asserted), so no graded level moves, and the
   loudest minute in the file is now the calibrator at 94.9 dB rather than 59.3. The band export carries
   the same minutes, the calibrator in its own 1 kHz band. The schedule's grid references are a survey
   again: each sits within 9 m of its scaled distance and bearing and the fourteen no longer reduce to one
   gable point. The complaints register carries 24 contacts in 24 different sentences. The process channels
   wander instead of jumping (lag-1 0.5 or more on the blower channel), and the totaliser's printed steps
   take five or more values. The engine's hour counter still steps 0.25 a running quarter, which is what an
   hour counter does and is left alone. `survey_notes.md` is stripped: no bolding anywhere, and the
   sentence about the early morning at the roadside positions is gone. The call survives that cut and it is
   proved rather than argued: `checks.py` asserts that the only minutes of any record with every source
   down are the intervals the log shows them all down in, and that the residual taken from the weekday
   hours before 05:00, from the nights, from the Sundays or from the minutes with both centrifuges off
   files a slate with NSL06 in and NSL13 out.

**What this round cost the ask layer, measured.** Rulings 1 to 3 put every A2 and A3 figure inside a filed
rule. The clause-executing cracker, written as code in `generator/cracker.py` and run on the cut pack,
keeps 70 of 70 ask criteria: the pair is 75.2 and the mirror keeps 70.0 per cent. The Part 1.1 cracker
still measures 39.1 and 4.3. The ask sheet states both and names the re-cut that would close the gap; it is
an open finding for the author, not a sensitivity, and it is not papered over.

## Draw

**Pairing.** Domain physical and environmental sciences, task type environmental monitoring and exceedance,
objective anomaly detection and diagnostics. The decision-maker is the site's environmental engineer; the
forum is the site's own mitigation programme; the forcing event is the contractor's slot, ordered on Monday
26 October 2026. As-of 2026-10-16, the date the folder was handed over. Prompt shape 01, a ranked list under
a cap: which five dwellings of the fourteen monitored the October acoustic treatment slot covers.

**Shape arithmetic (criteria before any file exists).** 14 specific levels + 14 dewatering-minute figures +
14 run counts + the five as a set, the sixth and the margin (3) + the ranked chart's named parts (4) + six
weeks x three plant figures (18) + the tone summary (3) = 70 ask criteria, on top of the recommendation and
instruction-following criteria. Over the 25 the spec asks for, and dense rather than stacked: every figure
is a row of one of two deliverables.

**Data-native sentence.** The blower house, the two centrifuges and the gas engine run through every weekday
daytime minute of a six-week survey, so the only record of the sound without the plant is the two hours a
week the plant is down for its inspection, which fall outside the assessment period the plan fixes for the
measurement itself.

**Sources read, one line each.** `stumping` 1.4, gap 3 and the objective gap: the deciding quantity is not
in any shipped column and has to be estimated from the records. `guide-to-prompt`: the pairing, the shape
and the 25 criteria. `supplemental-stumping`: the ask layer, re-cut in the stage-4 pass. The client's 10/10
rules: the three-rules block below. The seeds were read for the world, the decision and the quantity only.

**The WHAT screen (`stumping` 1.2), answered before the default path.** Decisive step: measure the residual
sound in the plant's own process stops rather than taking it from the record the plant was running in. The
five parts of the estimand and the sentence that files each: **population**, the 14 monitoring positions in
the register (noise management plan 2.1, "the positions listed in the monitoring schedule"); **outcome**,
the specific sound level of the effluent plant at the position, in dB LAeq (plan 3.1, "the sound level at a
position attributable to the plant, the measured level less the residual sound"); **window**, weekday 07:00
to 19:00 inside the position's own deployment (plan 3.2); **unit**, one monitoring position (plan 2.1);
**comparison**, none, the quantity is a level and the slot is a cap of five from the prompt. The decisive
step settles none of them: it is where in the record the residual term of a filed subtraction is measured,
and the plan files the subtraction's meaning without naming a window for it. Two ways of measuring it stand
(the statistical background of the position's own record, and the record inside the plant's stops), and the
records rule the first out: the plant's own event log shows the blowers, centrifuges and engine running
through every minute a position's background would be taken from, so that background contains the quantity
being subtracted.

**Guard WARNs answered.** `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, against task192
v3 and five of the last twelve): the key is the honest one, two defensible estimators of one filed quantity
with the data ruling one out, and the mechanism is unlike every other carrier of that key on file, the
nearest driver on the corpus standing at 0.07 (task263, separated in the card's differentiation).

## Default path

1. Read `noise_management_plan.pdf`: 14 monitoring positions, the assessment period weekday 07:00 to 19:00,
   the sample validity criteria, the tonality test, the process-record conventions, the mitigation slot of
   five dwellings.
2. Read `monitoring_positions.xlsx` and `meter_deployments_2026.csv`: pair each deployment with its position
   and take each deployment's field-check deviation off its levels where clause 4.1 calls for it.
3. Read `sound_levels_1min_2026.parquet`, drop the repeated download block, convert the UTC stamps to Irish
   Standard Time and keep each position's assessment-period minutes.
4. Join `weather_10min_2026.csv` on the enclosing ten-minute record and drop the minutes the plan excludes,
   with the minutes the meter recorded nothing for.
5. Energetically average each position's remaining minutes for its measured sound level.
6. Take the position's background from the same minutes, as the statistical background its own record
   shows: the energetic mean of its minute LA90 values (or the tenth percentile of its LAeq minutes,
   which is the same family and files its own wrong slate).
7. Subtract that background from the measured level in energy and call the result the specific sound level.
8. Rank the fourteen positions on it and file the five highest.

Ends on: NSL03, NSL04, NSL06, NSL11 and NSL12
Golden: NSL04, NSL11, NSL07, NSL02 and NSL13

## Stump sentence

A competent solver pairs every deployment with its position, takes each deployment's field-check deviation
off its levels, excludes exactly the minutes the plan excludes, energetically averages each position's
weekday daytime LAeq, energetically subtracts the background the position's own record shows and files
NSL03, NSL04, NSL06, NSL11 and NSL12. The step that lands it there is taking that background from a record
the plant was running in: the blowers, the centrifuges and the gas engine run through every assessment
minute, so the background already contains the plant, the subtraction returns the surroundings' own
variability (31.1 to 42.2 dB against specific levels of 37.4 to 53.0) and the slate fills with the dwellings
on the Clonaraght road and the Glasha while NSL07, NSL02 and NSL13, the quiet-surroundings dwellings the
plant contributes most to, drop out.

## Three rules

- **Task type:** `environmental-monitoring-exceedance` (physical-environmental-sciences), the
  domain's only anomaly-detection task type in the client taxonomy, and the build is the assessment itself:
  a monitoring survey reduced to one attributable level per position.
- **Domain test:** what decides the slate is the determination of a specific sound level, the separation of one
  source's contribution from the residual sound by energetic subtraction, which is the acoustics
  practitioner's own method and which requires the residual to be measured with the source shut down.
- **Swap:** "which five dwellings does the plant contribute most sound to" rewritten with a hospital's nouns
  ("which five wards does the ventilation plant contribute most infections to") stops making sense, because
  infections do not add in energy, a ward's background infection rate is observable while the plant runs, and
  there is no quantity that the presence of the source makes unmeasurable.
- **Layer 1:** UTC meter exports against field sheets in Irish Standard Time; five meters rotated over
  fourteen positions so each has its own week and surroundings; a field check either side of all 28
  deployments, two meters reading outside the plan's window all survey and in opposite directions; the met
  station logging ten-minute means against the meters' minutes, its rain gauge counting tips since midnight,
  and wind in metres a second before a sensor swap and kilometres an hour after it; minutes the meter wrote
  its no-data value for; positions known by a dwelling reference, a position code and the crew's shorthand,
  two deployments standing at a height the schedule did not set; a download repeated after a card error; a
  process historian carrying a counter that wraps, an hour counter changed mid-survey, a blower channel
  logged as both a rate and a totaliser, a feed channel at a quarter of an hour against an event log to the
  minute, and six spells with no rows at all. Each comes from the survey's own equipment and paperwork and
  none is placed to be caught.
- **Layer 2:** field_method, own:residual-measured-in-the-source-s-own-absence. The methodological choice that
  flips the call is where the residual term of the energetic subtraction is measured: the position's own
  running record, or the minutes inside the plant's weekly process stops.
- **Decisive step:** determine the residual sound at each position from the measurements made while the plant's
  rotating equipment was down, and subtract that from the measured total, rather than correcting the total by
  a statistical background of a record the plant was in.
- **Not semantics:** every field read correctly leaves the trap standing. The plan's own words define the
  specific level as the measured level less the residual sound; the meter columns are what they say they are;
  the dB(A) unit, the time base, the drift and the exclusions can all be handled exactly and the easy route
  still subtracts a background that contains the plant, because nothing in any field or definition says that
  the plant never stops.
- **Not rule application:** the judge's caveat is that plan 3.1 and 7.1 "give most of the recipe, so the step
  is close to rule application". They do give the recipe for everything except the one term that decides the
  answer. 3.1 says the specific level is the measured level less the residual sound and defines the residual
  as the sound from sources other than the plant; 7.1 says the slot takes the dwellings in order of that
  level. Executing every filed clause end to end yields the measured level, the valid minute counts, the
  energetic arithmetic and the ranking rule, and leaves the residual term unmeasured: no clause says over
  which minutes of a six-week record the sound from sources other than the plant is to be taken, and no
  clause says the plant ever stops. **The step no filed clause performs is choosing the plant-off window as
  the residual's record**, which means reading the process log for the intervals where the blowers, the
  centrifuges and the gas engine are all down, deciding that those 240 minutes a position are the only
  record of the quantity 3.1 names, and accepting that they sit outside the assessment period 3.2 fixes for
  the measured level. A solver who executes the plan and never opens the equipment log has every figure but
  that one, and files a wrong slate; the five rungs above are what the record's own statistics give instead.
- **Analyst test:** a strong analyst who maps every deployment, applies the drift, excludes exactly the plan's
  minutes and does the energetic arithmetic correctly still takes the background from the running record and
  files NSL03, NSL04, NSL06, NSL11 and NSL12.
- **Estimand:** "the specific sound level of the effluent plant at a monitoring position is the position's
  measured sound level over the assessment period less the residual sound, in dB LAeq", filed at clause 3.1
  of `noise_management_plan.pdf`, with the population at 2.1, the assessment period at 3.2 and the slot at
  7.1.
- **No decoy:** nothing is planted and no document argues a position. The complaints register records
  complaints and no levels, the effluent file is unrelated monitoring, the plan names no background method,
  no memo or draft carries a slate and no stakeholder quotes a figure.
- **No certified replay:** no certified, published or closed figure is shipped for a method to reproduce. The
  residual is measured, not recovered: the plant's event log and the meter records are both primary, and the
  method follows from the fact that the two cannot be separated in a record that holds both.
- **Lesson:** a quantity defined as a difference has to be measured where the difference is observable, and the
  windows that make it observable come from the operating record of the thing being measured, not from the
  statistics of the measurement. No build on file teaches it: the nearest, task263, inverts mixtures of many
  sources by mass balance, and task186 judges a change against a shared cycle.

## Readability screen

Each rung, and whether a solver reads it off the pack or has to construct it.

| Rung | Read off the pack? | Verdict |
|---|---|---|
| 0 complaints | the register counts contacts per dwelling, so the ranking is a sort | readable |
| 1 measured total | the energetic mean of a position's own minutes, one aggregation | readable |
| 2 statistical background | a percentile or an LA90 mean of the same minutes, one more aggregation | readable |
| **3 residual in the plant's stops (decisive)** | nothing names the stops as a measurement, nothing in the pack reports a level for them, and the intervals have to be built from the event log's per-unit starts and stops before a single minute can be averaged | **silent** |

## Semantic fork table

Every term and convention the main call runs on, with the reading the golden executes, the nearest
alternative a literal reader could take, and what closes it. `checks.py` asserts every row.

| id | Term or convention | Golden reading | Alternative | Ruled out by |
|---|---|---|---|---|
| SF1 | specific sound level | the measured level less the residual sound, energetically, in dB LAeq | the measured level itself | plan 3.1 names the subtraction in its definition |
| SF2 | residual sound | the sound at the position with the plant's rotating equipment down | the statistical background of the position's own record | the quantity is the sound without the plant, and the event log shows the plant running through every minute a background would be taken from (asserted); this is the stump, not a reading: both readings execute, and the records decide |
| SF3 | assessment period | weekday 07:00 to 19:00 inside the position's own deployment | every hour of the deployment | plan 3.2 states the period; weekend and night minutes are outside it |
| SF4 | the position's level | the energetic mean of its valid assessment minutes | the arithmetic mean of the same minutes | plan 3.1 states the level is an energy-equivalent level; the arithmetic reading files its own wrong slate (ladder rung 2c) |
| SF5 | valid minute, rain | a minute whose ten-minute met record counted rain on the gauge | the same record read as a rate above a limit | plan 4.2 states the test as a count and states no rate; a rate test on the ten-minute record selects exactly the same records, since one tip is 1.2 mm an hour (asserted equal, record by record) |
| SF6 | valid minute, the met record | the record whose ten minutes contain the minute, the stamp being its start | the record stamped at the end of those ten minutes | the survey notes file the stamp as the start of the ten minutes each record covers (asserted present) |
| SF6b | the meter record's stamp | the record covers the minute it is stamped at, the start of the interval | the stamp read as the end of the minute it covers | plan 2.2 files it in the sentence that already files the UTC stamp ("the meter stamps its records in UTC, each record at the start of the interval it measures"), stated there and nowhere else; unfiled, the end-of-minute reading moved four printed levels by a tenth and the margin from 1.3 to 1.2 |
| SF7 | valid minute, no measurement | a minute whose levels are the instrument's no-data value is not valid | the no-data value read as a level | plan 4.2's last sentence; the notes file the value, the deployment remarks file each spell, and no no-data minute falls inside a process stop (asserted) |
| SF8 | calibration correction | the deployment's deviation, the mean of its two field checks less 94.0 dB, taken off its levels, with its sign | the same difference taken as an absolute value | plan 4.1 defines the deviation as the mean less the reference and says it is taken off, so the sign follows the arithmetic; the two meters outside the window sit on opposite sides, so the signed reading is the only one that returns both to the calibrator |
| SF9 | the stops | every interval in which all three plant sources are recorded down | the weekly planned stop only | every printed level is identical to one decimal under both (asserted) |
| SF10 | the total | the energetic mean over the assessment minutes outside the stops | the same including the stopped minutes | every printed level is identical to one decimal under both, since no inspection reaches into the assessment period (asserted) |
| SF11 | the two deployments | the position's residual over both of its weeks pooled | the mean of its two deployments' own residuals | every printed level is identical to one decimal under both (asserted) |
| SF12 | duplicated download | one copy of the repeated block | both copies | every printed level is identical to one decimal under both (asserted) |
| SF13 | position identity | the position code in the register | the dwelling reference or the crew's shorthand | the register maps all three, one to one (asserted) |
| SF14 | rounding | levels and the margin to one decimal, the slate on unrounded levels | the slate on rounded levels | the prompt's closing sentence; no two positions share a printed level and none sits within 0.017 dB of a rounding edge (asserted) |
| SF15 | the five dwellings | the five highest specific levels | the five highest measured totals | the prompt asks what the slot is picked on, which plan 7.1 defines as the specific sound level |
| SF16 | the band file's time base | stamped UTC, like the minute file | stamped local | the notes file it; the tone verdicts are the same under both (asserted) |
| SF17 | tonality, the adjacent mean | the mean of the two adjacent band levels as the file writes them | the energetic mean of the same two | plan 4.3 says the mean of the levels; both give the same verdict at every position (asserted) |
| SF18 | the week, for a process figure | the counter reading at 00:00 on the Monday taken from the reading at 00:00 on the Monday after | the sum of the readings the historian holds inside the week | plan 5.1 files the two readings and says a spell it did not record leaves them as they stand |
| SF19 | a centrifuge run | one start of a centrifuge in the equipment log and the first stop the log records for the same machine after it; a start the log does not stop before that machine starts again is not a run | a block of feed in the process channel, or the bare count of START rows, which keeps the start of 10 September the log never stopped | plan 5.2 files all three parts of it, so one reading gives the weekly runs, the per-position runs and the per-position minutes; the channel's blocks count 6 or fewer where the log counts 8 to 13, and the bare count of starts gives 13 in the week beginning 7 September against the 12 the clause gives (both measured in `checks.py`) |
| SF20 | the minutes a centrifuge was running | the valid minutes of the position's assessment period, which is what the ask asks for | every minute of that period, valid or not | the ask states the basis in its own sentence ("the valid minutes of its assessment period"); the two readings differ by about a fifth (4,306 against 5,336 at NSL01), and plan 4.2 defines what a valid minute is |
| SF22 | a run reaching into the assessment period | a run that overlaps any minute of that period | a run that starts inside it, or one wholly inside it | the ask states the test in its own sentence ("overlapped any minute of that period"); counting the starts inside the period instead differs at ten or more of the fourteen positions (asserted) |
| SF21 | the engine's hours | the hour counter's own reading at the week boundaries, with the counter changed at the inspection on 15 September | the quarter hours whose export reading is above zero | plan 5.1 reads a week's figure off the counter; the counter was changed with the engine down, so no running hour falls either side of the change (asserted) |

## Ladder

Each figure is that rung's specific-level estimate in dB for the position, as built and measured in
`generator/figures.json`; the slate is the five highest.

| Rung | What it computes | Slate | 5th to 6th | Dies to |
|---|---|---|---|---|
| 0 complaints | rank by the complaints register's own count per dwelling | NSL01, NSL03, NSL06, NSL09, NSL12 | 1 complaint | plan 7.1: the slot is picked on the specific sound level, not on complaints |
| 1 measured total | the energetic mean of each position's valid assessment minutes | NSL02, NSL04, NSL06, NSL07, NSL11 | 0.48 dB | plan 3.1's definition, which subtracts the residual |
| 2 statistical background (default) | total less the energetic mean of the position's minute LA90 values | NSL03, NSL04, NSL06, NSL11, NSL12 | 0.08 dB | the event log: the plant ran through every minute of that background |
| 2' tenth percentile | total less the tenth percentile of the position's LAeq minutes | NSL02, NSL04, NSL06, NSL07, NSL11 | 0.52 dB | the same event log |
| 2b quietest interval | total less the quietest quarter hour of the position's record | NSL02, NSL04, NSL06, NSL07, NSL11 | 0.70 dB | the same event log |
| 2c arithmetic means | the arithmetic mean of the minute levels less the arithmetic mean of the minute LA90s | NSL03, NSL04, NSL06, NSL07, NSL11 | 0.43 dB | the same event log, and plan 3.1's energy-equivalent level |
| **3 residual in the plant's stops (answer)** | total less the energetic mean of the position's minutes inside the plant's recorded stops | **NSL04, NSL11, NSL07, NSL02, NSL13** | **1.29 dB** | nothing in the pack |

**As built (`generator/figures.json`).** Specific sound levels 37.4 to 53.0 dB LAeq, residual sounds 31.1
to 42.2 dB, measured totals 38.6 to 53.2 dB, every position's total at least 4.2 dB above its own residual,
240 stop minutes behind every position's residual, and 5,463 to 6,130 valid assessment minutes a position
against 1,070 to 1,737 excluded. The slate is NSL04 (53.0), NSL11 (49.9), NSL07 (47.8), NSL02 (47.3) and
NSL13 (46.0); NSL06 is the first dwelling off the list at 44.7, 1.3 dB behind (1.2877 dB unrounded, 0.038
from its rounding edge). Four distinct wrong slates
sit on the ladder above (the tenth-percentile and quietest-interval routes land on the measured total's
slate), and where a wrong rung's own boundary is thin the slate across it is wrong too, asserted rung by
rung rather than assumed.

**The flip conditions, as numbers.** The fifth and sixth places are NSL13 at 46.0 (45.9694) and NSL06 at
44.7 (44.6817). NSL06 enters the slate only once its residual falls below 38.17 dB; the record puts it at
42.23, so 4.1 dB of residual has to go missing before the call moves. NSL13 leaves only once its own
residual rises above 40.75 dB; the record puts it at 32.42, 8.3 dB below that. One extra minute of record
moves a position's level by under 0.003 dB; no printed level sits closer than 0.015 dB to its rounding edge
and none is closer than 0.018 dB to the printed value itself; the margin sits 0.038 dB from its own edge.
The sixth and seventh places (NSL06 and NSL09) stand 0.06 dB apart, which is the price of carrying the
margin on NSL06's own level: it is reported rather than tuned away, since the five levels are frozen and
NSL13 is the fifth.

**Worth of each rung, on the graded quantity.** Rung 1 moves one member of the slate (NSL06 for NSL13) and
every printed level by 0.2 to 1.8 dB. Rung 2 moves three members and every printed level by 4 to 15 dB.
Rungs 2', 2b and 2c move one to three members by different amounts. No rung is a partial version of the
decisive move: a background taken from the running record cannot be improved into the residual, because
every percentile, interval and average of that record contains the plant. That is the property architecture
2's first draw lacked and the reason this ladder holds.

**Dominance and position.** The answer's slate is not the complaints slate (rung 0 shares one member), not
the measured-total slate (four of five), and not the default path's slate (two of five). The default path's
own winner, NSL04, is also the golden's first, which is correct and not a rung-0 artifact: it is the nearest
dwelling and the plant dominates there, and the ladder's work is at the fourth and fifth places.

**The grid (measured on the built pack, asserted in `checks.py`).** The licensed readings of the golden's
own route all give the golden slate and the same fourteen printed levels: the planned stops alone against
every interval the log shows with all three sources down (identical, since the only other stop in the log
falls before the first deployment and the engine's own stops leave the blowers and centrifuges running);
the total over the assessment minutes against the total over the same minutes outside the stops (identical,
since no inspection reaches into the assessment period); and the position's residual pooled over its two
weeks against the mean of the two weeks' own residuals (identical to one decimal at all fourteen). Two
readings that violate a filed rule keep the slate and move figures: the calibration correction skipped
(plan 4.1) moves ten printed levels by up to 0.39 dB, and the met exclusions skipped (plan 4.2) moves four
by up to 0.19 dB. Every background taken from the running record gives a wrong slate, in the rows above. So does every
other window the pack permits, asserted window by window on the clean truth: the weekday hours before
05:00, the nights from 23:00, the Sundays and the minutes with both centrifuges off each file a slate with
NSL06 in and NSL13 out, because the blowers and the engine run through all of them. `checks.py` asserts
that the only minutes of any record with every source down are the intervals the log shows them all down
in, so no window but those is free of the plant.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the 14 monitoring positions in the register's schedule | plan 2.1; the met mast and the plant's own positions are not monitoring positions (asserted) |
| 2 Unit | one monitoring position at one dwelling | plan 2.1 |
| 3 Window | weekday 07:00 to 19:00 within each position's deployment | plan 3.2 |
| 4 As-of | records to 2026-10-16, the extract date; the slot ordered 2026-10-26 | no date after 2026-10-16 in any shipped file except the instruments' verification due dates (asserted) |
| 5 Version basis | one row per logged minute; the repeated download block counted once, and a minute whose columns carry the instrument's no-data value counted as no measurement | SF12 and SF7, convergent to one decimal |
| 6 Divisor | none; levels are energetic means over the minutes in scope | SF4 |
| 6b Process figures | each week's figure is the difference of two counter readings at its boundaries, and its runs are the log's starts inside it | plan 5.1 and 5.2, SF18, SF19 and SF21 |
| 7 Weighting | every valid minute weighted equally in energy | plan 3.1's energy-equivalent level |
| 8 Window length | each position's own deployment week, weekday daytime only | plan 3.2 |
| 9 Boundary | the slate's 5th to 6th gap is 1.2877 dB, 0.038 from its printed edge; NSL06 needs 4.1 dB of residual to go missing to enter, NSL13 8.3 dB to appear to leave | asserted in `checks.py` and again in `verify.py` |
| 10 Rounding | levels and the margin to one decimal, counts whole, engine hours to one decimal, the slate on unrounded levels | prompt's closing sentence; every printed level at least 0.015 dB from a rounding edge and at least 0.018 dB off the printed value itself, no two equal; the margin 0.038 from its edge; every week's delivered air at least 0.15 of a whole unit from its edge (asserted in `checks.py` and again in `verify.py`) |
| 11 Tie-break | none needed: no two positions share a printed level | asserted |
| 12 Maturity | every deployment is complete and downloaded; the survey closed 2026-10-11 | asserted |
| 13 Order | identity, deployment pairing, drift, time base, validity, energetic mean, residual, subtraction, rank | the plan's own order of clauses |
| 14 Row order | irrelevant; every figure is an aggregate | asserted |
| 15 Duplicates | the repeated download block, identical minute for minute | SF12 |
| 16 Identity | position code, dwelling reference and the crew's shorthand all map through the register | SF13 |
| 17 Netting | energetic subtraction of the residual, once, at the position level | plan 3.1 |
| 18 Units | dB(A) for levels, tips of 0.2 mm for rain, m a second for wind after conversion from km an hour, cubic metres and thousands of normal cubic metres for the plant's counters, hours for the engine | the survey notes state the met channels' units and the swap date, and the process channels' headers carry theirs |
| 18b Stamp | every record covers the interval it is stamped at, the meters' minutes and the mast's ten minutes alike | plan 2.2 for the meters (SF6b), the survey notes for the mast (SF6); the deployment record carries the minute each meter was set running and the minute it was stopped, so no minute is claimed by two deployments |
| 19 Code semantics | the equipment identifiers and states in the event log, mapped in the survey notes | asserted |
| 20 Integerisation | the minute counts and the run counts are counts; the counter figures round once, at the answer; no rounding of intermediate levels | asserted |
| 21 Scope | sound only; the effluent quality and complaint files are outside the question | plan 1.2 |
| 22 Forward window | none: the quantity is measured over a closed survey, and the slot it drives is not yet ordered | the retrospective-quantity line below |

**Retrospective quantity, forward call.** The specific levels are measured over a survey that closed on 11
October 2026; the call they drive (which five dwellings the October slot covers, ordered on 26 October) is
about a window not yet closed. The plan fixes the survey as the assessment, so the quantity is
retrospective by design and the decision is forward facing.

## Literal reader

Executed word for word, the prompt and `noise_management_plan.pdf` give one quantity per position (the
measured level over weekday 07:00 to 19:00 less the residual sound, in dB LAeq, to one decimal) and one slate
(the five highest), and leave exactly one thing open, where the residual is measured; every reading of every
other term is either the golden's or ruled out in the fork table, and the two open readings of the residual
are separated by the records rather than by a sentence, which is the stump. The supplementary figures are
closed the same way: the rain test is a count of tips and the nearest rate reading selects the same records
(SF5), the meters' minutes and the mast's ten minutes are both stamped at the start of the interval they
cover (SF6b and SF6), the no-data minutes are filed as no measurement (SF7), the week's process figures are
two counter readings (SF18 and SF21), and a run is a logged start with the first stop that closes it, a
start the log never stops before that machine starts again counting for nothing (SF19). The two quantities
the position table asks for state their own basis in the asking sentence, the valid minutes of the
assessment period and the runs that overlap any minute of it (SF20 and SF22), so executing plan 5.2 gives
the weekly runs, the per-position runs and the per-position minutes on one reading of the log, with the
start of 10 September the log never stopped excluded from all three.

## Oracles

No control, calibration corpus, certified figure or reconciliation column scores the method. The complaints
register (rung 0's material and a declared distractor) records complaints and no levels. The met record
decides sample validity and no level. The plant's event log and the historian record what ran and when, and
neither states a level or a background. The 1/3-octave file carries band levels for the tonality summary and
no broadband level that could stand in for a total (asserted: no shipped file holds a specific sound level, a
residual level or a corrected level for any position).

## Ask sheet

The ask layer was re-cut after the determinism pass, because closing the judge's five supplementary forks
left it carrying 28 forced, device-free criteria on the band and tone table and 28 more on minute counts
whose every convention was now filed. The weight moved to the quantities the decision needs that run
through the plant's own records, where the devices live. `generator/cracker.py` scores it on the cut pack.

| Ask | Figures | Home (H18) | Primary device | Shared hazards | Files on the path |
|---|---|---|---|---|---|
| A1 the 14 specific levels, the slate, the sixth, its margin and the ranked chart | 21 | the call's own construction | none (construction); the cracker has it by design | the Layer 1 set | plan, register, deployments, parquet, met, event log |
| A2 the minutes behind each level with a centrifuge running, and the runs they span | 28 | the operating state each level was measured under, which is what makes positions measured in different weeks comparable | D6, a quantity the plant records twice at two grains: the equipment log's starts and stops to the minute, and a fifteen-minute feed channel that cannot resolve either | D4 the historian's gaps, D8 the log in local time against the meters in UTC, D5 the validity mask behind the level | event log, SCADA, deployments, parquet, met, plan |
| A3 the blower air delivered, the centrifuge runs and the engine's hours, per survey week | 18 | the plant's load through each survey week, the qualifier the note's comparability claim rests on | D6 and D4, a flow logged as both a rate and a totaliser, an engine logged as both a rate and an hour counter, and six spells the historian did not record at all | D2 the counter roll-over and the hour counter changed mid-survey, D6 the log's per-machine grain | SCADA, event log, plan, notes |
| A4 whether a tone is prominent, where, and in which band | 3 | the mitigation case: a tonal source takes different treatment | none (forced); kept small for that reason | D8 time base, D4 the meters without the band module | third-octave file, plan, deployments |

**Separation.** Zero device rows sit in the main call's declared population (the 14 positions' valid
assessment minutes, the event log's all-down rows and the register's position rows), asserted by count. A2's
and A3's devices are in the process channel and the historian's gaps, which the call reads for nothing: the
call reads the log only for the intervals where all three sources are down. Every printed specific level is
identical to one decimal with the met exclusions skipped, the unit swap misread, the repeated block kept and
the no-data minutes read as levels (asserted).

**The cracker sheet (the Part 1.1 cracker).** The cracker landed the call, ran the hygiene battery (key
uniqueness, exact duplicates, unmatched joins, fan-out, count ties), executed the filed rules that battery
points at and the clauses its own quantities name (3.1 and 3.2 for the level, 4.1 and 4.2 for validity, 4.3
for tonality), and took the plant's records at face value, which means the process channel the historian
writes. Scored figure by figure on the cut pack by `generator/cracker.py`, and asserted in `checks.py`. The
clause-executing cracker is scored in the same script and reported under the pair ceiling below.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A2 the minutes behind each level with a centrifuge running | the fifteen-minute feed channel, every quarter hour with feed counted as fifteen minutes | wrong at all 14 positions, by 30 to 430 minutes: the channel cannot see a start inside its quarter hour and holds no rows at all for the historian's six gaps | the equipment log's starts and the stops that close them, per plan 5.2, intersected with the minutes behind the level | miss |
| A2 the runs those minutes span | blocks of feed in the same channel | wrong at all 14: the channel merges the two machines and a split run, so it counts 2 where the log counts 8 to 14 | the log's runs, per plan 5.2 | miss |
| A3 the blower air delivered, six weeks | the rate channel summed over the week | wrong in all six weeks, by 8 to 84 thousand Nm3, because the historian holds no rows for its gaps | the header's flow totaliser at the week boundaries, per plan 5.1 | miss |
| A3 the centrifuge runs, six weeks | blocks of feed in the channel | wrong in all six: 6 or fewer against 8 to 13 | the starts the log carries in the week, per plan 5.2 | miss |
| A3 the engine's hours, six weeks | the quarter hours whose export reading is above zero | wrong in all six, by 1 to 20 hours, for the same gaps | the engine's own hour counter at the week boundaries, with the counter changed at the inspection on 15 September | miss |

**Pair ceiling:** 75.2 (ask weight 55 over 70 criteria, 0.786 a criterion: the cracker executes plan 5.2
on the log, plan 5.1 on the counters and the ask's own two stated bases over the validity mask it already
holds, and keeps all 70, 55 points, so 38 + 7 + 55 = 100.0; the mirror, which stops at the
statistical-background rung, loses A1's 21 and keeps the other 49, 38.5 points, so 5 + 7 + 38.5 = 50.5;
the pair averages 75.2). **Over the ceiling, and the gate fails on it.**
**Mirror leakage:** 70.0
**Measured by:** `generator/cracker.py`, run on the cut pack after every change and asserted figure by
figure in `generator/checks.py`

**Why these are the figures and not the 39.1 this sheet carried.** Part 1.1 defines the cracker as the
response that landed the call, ran the hygiene battery **and executed every filed rule it points at**. Once
plan 5.2 was reworded, the minutes basis stated and the overlap defined, the rules the A2 and A3 quantities
point at are filed rules that a cracker executes, so the clause-executing reader *is* the cracker and 75.2
is the ceiling. The 39.1 belongs to a weaker response that stops short of section 5; it is not a second
reading of the same measurement and it is not a ceiling. The ask layer is being re-cut (below).

**The weaker reader, for the record.** The same script also scores a response that stops short of section
5 and takes the plant's records at face value, which means the process channel the historian writes: it
keeps 24 of 70 and its pair is 39.1 with 4.3 per cent mirror leakage. That is the sheet this build shipped
with, and it was the wrong measurement: a response that reads none of the filed sentences its own
quantities name is the mirror, not the cracker.

**What the measurement says about the design, which is the finding.** There was no legal device in the A2
and A3 figures to lose. The judge failed Gate A on a runs column that reproduced under no reading, Gate C
on the minutes basis and Gate E on both terms, and the only repair for an undefined term is to define it,
so rulings 1 to 3 were forced. But the device rode on exactly those terms being undefined, and a device
that evaporates when the definitions are forced was the ambiguity wearing a device's clothes: ban 1 forbids
a device a filed rule adjudicates, and once the rule is filed, it does. A device that survives every term
being written out fully defined rides on the data. The ask layer is therefore re-cut onto quantities whose
correct computation needs a step no filed sentence performs, found by an internal inconsistency only, on
rows outside the call's declared population; the call, the stump, the ladder and every graded call figure
stay exactly as they are.

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
