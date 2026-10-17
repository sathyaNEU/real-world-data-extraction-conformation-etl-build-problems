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

## Draw

```
Card filed with guard.py register before the ladder was written? yes (WARN, answered below)
Domain: physical-environmental-sciences / environmental-monitoring-exceedance   Objective: anomaly-detection
Task type: environmental monitoring and exceedance assessment, the only task type the client's taxonomy gives
  anomaly detection in this domain (README: environmental-monitoring-exceedance serves AD and DQ)
Shape: 01 (ranked list under a cap: each candidate)   Decision type: ranked_slate_under_cap
Answer unit: set_of_items   Question form: which   Opening move: question-first
Gap: objective (the measured total at a dwelling is a correct measurement and is not the quantity the
  mitigation slot is scored on)
Gate G mechanism: method_or_model_selection (two defensible ways to measure the residual in an energetic
  subtraction, one of them ruled out by the records' own structure)
Pattern: none (own); generator G3 (record versus operation: the meter's record is of the whole acoustic
  scene, not of the plant's own contribution)
Stump strategy: other (where the nuisance quantity in an energetic subtraction is measured from; no vocab
  key names it)   Layer 2 family: estimation_fit's neighbour field_method, pattern
  own:residual-measured-in-the-source-s-own-absence
Calibration form: none (no corpus, no closed-outcome ledger; the method is forced by the records)
Context artifact: register (the monitoring position register: dwelling, position, distance, bearing, screen)
Stakeholder role: the site's environmental engineer (role family field_unit_lead)
Forum: committee_or_panel (the site's environmental review panel confirms the quarter's list)
Forcing event: purchase_order_or_contract (the acoustic contractor's October slot is ordered on 26 October)
Org family: manufacturer (a milk processing site)
Decisive rule filed? no (the noise management plan files the quantity, the assessment period, the sample
  validity criteria, the tonality test, the positions and the slot, and nothing about the residual)
Official decoy? no   Validated decoy? no   stump_class: analytical
World: Ireland, the midlands, EUR. Tulcarra Foods' Drumlorne milk processing site, near Clonaraght.
People (guard.py names, en_IE, seed 1822): Keelan Moher (environmental engineer, the requester), Aiden
  Hawthorn (operations manager), Orla O'Hurley (monitoring technician), Cormac Cashman (process operator),
  Helen Deeny (maintenance planner)
Deliverables: specific_sound_levels.csv, mitigation_shortlist.pdf
As-of: 2026-10-16 (the extract), the slot ordered 2026-10-26
```

**Shape arithmetic (25 or more criteria before any file exists).** 14 positions x 1 specific level = 14; the
five dwellings, the sixth and its margin = 3; the valid and excluded minute counts = 28; six weeks x three
plant figures = 18; 14 positions x (highest band, tone) = 28; the chart's named parts = 4. **95 criteria.**

**Data-native sentence.** The blower house, the two centrifuges and the gas engine run through every weekday
hour the survey covers, so at a dwelling where the plant is audible the quietest minute of the record still
contains it, and the record cannot show what the dwelling would hear without it; the only minutes in the
survey that do are the ones inside the plant's own weekly process stops.

**Sources read, one line each.** `stumping` 1.4, gap 3 and the objective gap: the deciding quantity is not
the metric the records hand over, and here the handed-over metric (the measured total) is correct.
`stumping` Part 6, where a fresh stump comes from: pitfalls live where recording differs from the event, and
this one is a quantity the instrument cannot see while the source it belongs to is running. `measured-drivers`
held group: every one of the 18 holds because partial application of the decisive construction scores no
better than nothing, which is the property architecture 2's first draw failed and this one has by
construction (no background taken from the running record gets closer to the answer). `guide-to-prompt`
shape 01: the criteria come from the candidate list, doubled by a second figure per candidate.

**The WHAT screen (`stumping` 1.2), answered before the default path.** Decisive step: measure the residual
sound in the plant's own process stops rather than taking it from the record the plant was running in. The
five parts of the estimand and the sentence that files each: **population**, the 14 monitoring positions in
the register (noise management plan 2.1, "the positions listed in the monitoring schedule"); **outcome**, the
specific sound level of the effluent plant at the position, in dB LAeq (plan 3.1, "the sound level at a
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
   the sample validity criteria, the tonality test, the mitigation slot of five dwellings.
2. Read `monitoring_positions.xlsx` and `meter_deployments_2026.csv`: pair each deployment with its position
   and apply each deployment's drift from its pre- and post-deployment calibration check.
3. Read `sound_levels_1min_2026.parquet`, drop the repeated download block, convert the UTC stamps to Irish
   Standard Time and keep each position's assessment-period minutes.
4. Join `weather_10min_2026.csv` on the enclosing ten-minute record and drop the minutes the plan excludes
   (rain above 0.5 mm an hour, wind above 5 m a second).
5. Energetically average each position's valid LAeq minutes: the measured total at the dwelling.
6. Take the position's background from the same minutes, as the statistical background its own record shows
   (the tenth percentile of its LAeq minutes, or the energetic mean of its minute LA90 values).
7. Subtract background from total energetically: the plant's specific sound level at each dwelling.
8. Rank the 14 dwellings on that level and file the five highest.

Ends on: NSL03, NSL04, NSL06, NSL11 and NSL12
Golden: NSL04, NSL11, NSL07, NSL02 and NSL13

## Stump sentence

A competent solver pairs every deployment with its position, applies the calibration drift, excludes exactly
the minutes the plan excludes, energetically averages each position's weekday daytime LAeq, energetically
subtracts the background the position's own record shows and files NSL03, NSL04, NSL06, NSL11 and NSL12.
The step that lands it there is taking that background from a record the plant was running in: the blowers,
the centrifuges and the gas engine run through every assessment minute, so the background already contains
the plant, the subtraction returns the surroundings' own variability (29.3 to 40.9 dB against specific
levels of 37.5 to 53.1) and the slate fills with the dwellings on the Clonaraght road and the Glasha while
NSL07, NSL02 and NSL13, the quiet-surroundings dwellings the plant contributes most to, drop out.

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
- **Layer 1:** UTC meter exports against field sheets in Irish Standard Time; six meters rotated over fourteen
  positions so each has its own week and surroundings; pre- and post-deployment calibration checks with one
  meter drifting; the met station logging ten-minute means against the meters' minutes, and wind in metres a
  second before a sensor swap and kilometres an hour after it; positions known by a dwelling reference, a
  position code and the crew's shorthand, one position moved mid-week; a download repeated after a card
  error. Each comes from the survey's own equipment and paperwork and none is placed to be caught.
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
- **Not rule application:** no filed rule or procedure determines the residual. The plan files the quantity,
  the assessment period, the validity criteria, the tonality test, the positions and the slot's size, and
  stops there; executing every filed rule gives the measured total and the valid minute counts and leaves the
  residual to the analyst.
- **Analyst test:** a strong analyst who maps every deployment, applies the drift, excludes exactly the plan's
  minutes and does the energetic arithmetic correctly still takes the background from the running record and
  files NSL03, NSL04, NSL06, NSL11 and NSL12.
- **Estimand:** "the specific sound level of the effluent plant at a monitoring position is the position's
  measured sound level over the assessment period less the residual sound, in dB LAeq", filed at clause 3.1
  of `noise_management_plan.pdf`, with the population at 2.1, the assessment period at 3.2 and the slot at
  6.1.
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

Six tests per rung: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene battery, 6 linear.

| Rung | 1 filed | 2 schema | 3 reflex | 4 bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 complaints ranking | no | the register's complaint reference | yes, the forcing event | no | no | yes, a count | readable |
| 1 measured total, no correction | no | no | yes, the meter's own column | no | no | yes, one average | readable |
| 2 statistical background (default) | no | no | yes, the standard correction | no | no | one subtraction | readable |
| 2b quietest interval as background | no | no | yes | no | no | one subtraction | readable |
| 2c arithmetic means of levels | no | no | yes | no | no | one subtraction | readable |
| 3 residual in the plant's stops (decisive) | no | no | no | no | no | no | silent |

- **Test 1.** No shipped sentence names a background, a percentile, a stop, a shutdown window or a period
  without the plant. The plan's clause 3.1 names the residual sound as a term of the subtraction and defines
  it no further; the event log records starts and stops because that is what a process log records, and no
  sentence in the pack connects the two. Asserted as a word sweep in `checks.py`.
- **Test 2.** No column marks the stops, no flag separates the stopped minutes, and the meter records carry
  no plant state. The join that reaches them is from the event log's timestamps to the meter minutes, which
  the solver has to think of.
- **Test 3.** The opponent's reflexes all land wrong: take the measured level (rung 1), apply the standard
  background correction (rung 2), use the quietest interval (rung 2b), average the levels arithmetically
  (rung 2c), and all five rank the dwellings by their surroundings rather than by the plant.
- **Test 4.** No control, corpus or certified figure scores the methods. The boundary monitor is not shipped.
- **Test 5.** The hygiene battery reaches the duplicated download block, the drift, the unit change and the
  identity variants, every one of them Layer 1, and none of them the decisive step.
- **Test 6.** The decisive step is not a subtraction or a ratio of shipped quantities: it is a set of minutes
  selected by another file's timestamps, and the quantity is then an energetic difference of two means.

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Ruled out by |
|---|---|---|---|---|
| SF1 | specific sound level | the measured level less the residual sound, energetically, in dB LAeq | the measured level itself | plan 3.1 names the subtraction in its definition |
| SF2 | residual sound | the sound at the position with the plant's rotating equipment down | the statistical background of the position's own record | the quantity is the sound without the plant, and the event log shows the plant running through every minute a background would be taken from (asserted); this is the stump, not a reading: both readings execute, and the records decide |
| SF3 | assessment period | weekday 07:00 to 19:00 inside the position's own deployment | every hour of the deployment | plan 3.2 states the period; weekend and night minutes are outside it |
| SF4 | the position's level | the energetic mean of its valid assessment minutes | the arithmetic mean of the same minutes | plan 3.1 states the level is an energy-equivalent level; same slate either way, asserted |
| SF5 | valid minute | a minute whose enclosing met record is inside the plan's rain and wind criteria | every logged minute | plan 4.2 states the criteria; the slate and every printed level are unchanged either way, asserted |
| SF6 | calibration drift | the deployment's own adjustment from its pre- and post-deployment check | the certificate's nominal sensitivity | plan 4.1 states the field check governs; same call either way, asserted |
| SF7 | the stops | every interval in which all three plant sources are recorded down | the weekly planned stop only | every printed level is identical to one decimal under both (asserted) |
| SF8 | the total | the energetic mean over the assessment minutes outside the stops | the same including the stopped minutes | every printed level is identical to one decimal under both (asserted) |
| SF9 | duplicated download | one copy of the repeated block | both copies | every printed level is identical to one decimal under both (asserted) |
| SF10 | position identity | the position code in the register | the dwelling reference or the crew's shorthand | the register maps all three, one to one (asserted) |
| SF11 | rounding | levels and the margin to one decimal, the slate on unrounded levels | the slate on rounded levels | the prompt's closing sentence; no two positions share a printed level and none sits within 0.25 dB of a rounding edge (asserted) |
| SF12 | the five dwellings | the five highest specific levels | the five highest measured totals | the prompt asks what the slot is picked on, which plan 6.1 defines as the specific sound level |

## Ladder

Each figure is that rung's specific-level estimate in dB for the position, as built and measured in
`generator/figures.json`; the slate is the five highest.

| Rung | What it computes | Slate | 5th to 6th | Dies to |
|---|---|---|---|---|
| 0 complaints | rank by the complaints register's own count per dwelling | NSL01, NSL03, NSL06, NSL09, NSL12 | 1 complaint | plan 6.1: the slot is picked on the specific sound level, not on complaints |
| 1 measured total | the energetic mean of each position's valid assessment minutes, uncorrected | NSL02, NSL04, NSL06, NSL07, NSL11 | 0.38 dB | plan 3.1's definition, which subtracts the residual |
| 2 statistical background (default) | total less the energetic mean of the position's minute LA90 values | NSL03, NSL04, NSL06, NSL11, NSL12 | 1.34 dB | the event log: the plant ran through every minute of that background |
| 2' tenth percentile | total less the tenth percentile of the position's LAeq minutes | NSL02, NSL03, NSL04, NSL06, NSL07 | 0.24 dB | the same event log |
| 2b quietest interval | total less the quietest quarter hour of the position's record | NSL03, NSL04, NSL06, NSL07, NSL11 | 0.14 dB | the same event log |
| 2c arithmetic means | the arithmetic mean of the minute levels less the arithmetic mean of the minute LA90s | NSL03, NSL04, NSL06, NSL11, NSL12 | 1.24 dB | the same event log, and plan 3.1's energy-equivalent level |
| **3 residual in the plant's stops (answer)** | total less the energetic mean of the position's minutes inside the plant's recorded stops | **NSL04, NSL11, NSL07, NSL02, NSL13** | **0.80 dB** | nothing in the pack |

**As built (`generator/figures.json`).** Specific sound levels 37.5 to 53.1 dB LAeq, residual sounds 29.3
to 40.9 dB, measured totals 38.5 to 53.3 dB, every position's total at least 5.7 dB above its own residual,
240 stop minutes behind every position's residual, and 6,190 to 6,900 valid assessment minutes a position.
The slate is NSL04 (53.1), NSL11 (49.9), NSL07 (47.9), NSL02 (47.2) and NSL13 (46.0); NSL06 is the first
dwelling off the list at 45.2, 0.8 dB behind. Five distinct wrong slates sit on the ladder above, and the
thinnest of their own boundaries is 0.14 dB, on a route whose two sides are both wrong slates.

**Worth of each rung, on the graded quantity.** Rung 1 moves one member of the slate (NSL06 for NSL13) and
every printed level by 0.2 to 1.7 dB. Rung 2 moves three members and every printed level by 5 to 15 dB. Rung
2b and 2c move the same three members by different amounts. No rung is a partial version of the decisive
move: a background taken from the running record cannot be improved into the residual, because every
percentile, interval and average of that record contains the plant. That is the property architecture 2's
first draw lacked and the reason this ladder holds.

**Dominance and position.** The answer's slate is not the complaints slate (rung 0 shares one member), not
the measured-total slate (four of five), and not the default path's slate (two of five). The default path's
own winner, NSL04, is also the golden's first, which is correct and not a rung-0 artifact: it is the nearest
dwelling and the plant dominates there, and the ladder's work is at the fourth and fifth places.

**The grid (measured on the built pack, asserted in `checks.py`).** The licensed readings of the golden's
own route all give the golden slate and the same fourteen printed levels: the planned stops alone against
every interval the log shows with all three sources down (identical to 0.000 dB, since the only other stop
in the log falls before the first deployment), and the total over the assessment minutes against the total
over the same minutes outside the stops (identical, since no stop minute falls in the assessment period).
Two readings that violate a filed rule keep the slate and move figures: the calibration correction skipped
(plan 4.1) moves ten printed levels by up to 0.31 dB, and the met exclusions skipped (plan 4.2) moves one
by 0.08 dB. Every background taken from the running record gives a wrong slate, in the five rows above.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the 14 monitoring positions in the register's schedule | plan 2.1; the met mast and the plant's own positions are not monitoring positions (asserted) |
| 2 Unit | one monitoring position at one dwelling | plan 2.1 |
| 3 Window | weekday 07:00 to 19:00 within each position's deployment | plan 3.2 |
| 4 As-of | records to 2026-10-16, the extract date; the slot ordered 2026-10-26 | no date after 2026-10-16 in any shipped file (asserted) |
| 5 Version basis | one row per logged minute; the repeated download block counted once | SF9, convergent to one decimal |
| 6 Divisor | none; levels are energetic means over the minutes in scope | SF4 |
| 7 Weighting | every valid minute weighted equally in energy | plan 3.1's energy-equivalent level |
| 8 Window length | each position's own deployment week, weekday daytime only | plan 3.2 |
| 9 Boundary | the slate's 5th to 6th gap is 0.80 dB and every rung's is 0.71 dB or more | asserted |
| 10 Rounding | levels and the margin to one decimal, counts and hours whole, the slate on unrounded levels | prompt's closing sentence; every printed level at least 0.25 dB from a rounding edge, no two equal (asserted) |
| 11 Tie-break | none needed: no two positions share a printed level | asserted |
| 12 Maturity | every deployment is complete and downloaded; the survey closed 2026-10-09 | asserted |
| 13 Order | identity, deployment pairing, drift, time base, validity, energetic mean, residual, subtraction, rank | the plan's own order of clauses |
| 14 Row order | irrelevant; every figure is an aggregate | asserted |
| 15 Duplicates | the repeated download block, identical minute for minute | SF9 |
| 16 Identity | position code, dwelling reference and the crew's shorthand all map through the register | SF10 |
| 17 Netting | energetic subtraction of the residual, once, at the position level | plan 3.1 |
| 18 Units | dB(A) for levels, mm an hour for rain, m a second for wind after conversion from km an hour | the survey notes state the met channels' units and the swap date |
| 19 Code semantics | the equipment identifiers and states in the event log, mapped in the survey notes | asserted |
| 20 Integerisation | the minute counts are counts; no rounding of intermediate levels | asserted |
| 21 Scope | sound only; the effluent quality and complaint files are outside the question | plan 1.2 |
| 22 Forward window | none: the quantity is measured over a closed survey, and the slot it drives is not yet ordered | the design note's retrospective-quantity line below |

**Retrospective quantity, forward call.** The specific levels are measured over a survey that closed on 9
October 2026; the call they drive (which five dwellings the October slot covers, ordered on 26 October) is
about a window not yet closed. The plan fixes the survey as the assessment, so the quantity is
retrospective by design and the decision is forward facing.

## Literal reader

Executed word for word, the prompt and `noise_management_plan.pdf` give one quantity per position (the
measured level over weekday 07:00 to 19:00 less the residual sound, in dB LAeq, to one decimal) and one slate
(the five highest), and leave exactly one thing open, where the residual is measured; every reading of every
other term is either the golden's or ruled out in the fork table, and the two open readings of the residual
are separated by the records rather than by a sentence, which is the stump.

## Oracles

No control, calibration corpus, certified figure or reconciliation column scores the method. The complaints
register (rung 0's material and a declared distractor) records complaints and no levels. The met record
decides sample validity and no level. The plant's event log and SCADA record what ran and when, and neither
states a level or a background. The 1/3-octave file carries band levels for the tonality ask and no
broadband level that could stand in for a total (asserted: no shipped file holds a specific sound level, a
residual level or a corrected level for any position).

## Ask sheet

| Ask | Figures | Home (H18) | Primary device | Shared hazards | Files on the path |
|---|---|---|---|---|---|
| A1 the 14 specific levels, dB to 1 dp, and the slate, the sixth and its margin | 17 | the call's own construction | none (construction) | the Layer 1 set | plan, register, deployments, parquet, met, event log |
| A2 valid and excluded assessment minutes per position | 28 | the audit trail of the input the call consumes | D3, the met channels' unit swap and the rain gauge's cumulative tips | D8 time base, D1 the repeated block | met, parquet, deployments, notes |
| A3 the hours the blower house ran, the biogas burned and the centrifuge runs, per survey week | 18 | the plant's load through each position's week, the qualifier that makes the levels comparable | D2, the engine hour counter replaced mid-survey and the SCADA counter rollover | D8 time base, D4 the comms gap | SCADA, notes, event log |
| A4 the highest one-third-octave band and the tone verdict per position | 28 | a component of the mitigation case: a tonal source needs different treatment | D6, bands reported as LZeq with two bands missing on one meter and no band file for the last week | D8 time base | third-octave file, plan, deployments |

**Separation.** Zero device rows sit in the main call's declared population (the 14 positions' assessment
minutes, the event log's stop rows and the register's position rows), asserted by count. A2's and A3's
devices move counts and hours, not levels: every printed specific level is identical to one decimal with the
met exclusions skipped, the unit swap misread, the repeated block kept, the hour counter read as continuous
and the SCADA gap filled (asserted, six assertions). A4's devices touch no file the call reads except the
plan.

**The cracker sheet.** The cracker landed the call, ran the hygiene battery, executed every filed rule and
reconciled every total.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A2 valid and excluded minutes | the met record joined on the nearest ten-minute stamp in UTC, wind read in one unit throughout | 11 of 14 positions' excluded counts too low, two too high | the enclosing met record in local time, km an hour converted after the swap date | miss |
| A3 blower hours, biogas, centrifuge runs | the SCADA counters differenced end to start | three weeks' biogas short by the rollover and the engine's replaced counter | the counter's resets and the replacement read from the maintenance rows, the comms gap from the daily log | miss |
| A4 highest band and tone | the A-weighted band levels, missing bands read as zero | the wrong band at nine positions and the tone verdict wrong at four | the unweighted band levels, the missing bands absent and the last week's positions answered none | miss |

**Pair ceiling:** 39.5 (ask weight 57 over 95 criteria: construction 14 criteria = 8.4 points, devices 81 =
48.6; the cracker takes 38 + 7 + 8.4 + 15 per cent of the devices = 60.6, the best miss takes 5 + 7 + 12 per
cent = 17.8, and the pair averages 39.2, which the regrade margin rounds to 39.5)
**Mirror leakage:** 12.0

## Pack

| File | Format | Role |
|---|---|---|
| `sound_levels_1min_2026.parquet` | parquet | spine: one minute of logged level per position (LAeq, LA90, LAmax, LAmin), the volume gate |
| `meter_deployments_2026.csv` | csv | which meter at which position, from and to, mounting, calibration checks, remarks |
| `monitoring_positions.xlsx` | xlsx | context artifact: the register of positions, dwellings, distances, bearings, screening |
| `noise_management_plan.pdf` | pdf | governing document: the quantity, the period, the validity criteria, the tonality test, the slot |
| `survey_notes.md` | md | the technician's notes: meters, identities, time base, met channels, file conventions |
| `plant_equipment_events_2026.csv` | csv | the process operator's equipment log: starts, stops and reasons |
| `scada_15min_2026.csv` | csv | plant process channels at fifteen minutes (air flow, biogas, centrifuge, inlet) |
| `weather_10min_2026.csv` | csv | the met mast at ten minutes: wind, rain, temperature |
| `third_octave_15min_2026.csv` | csv | one-third-octave band levels per position and quarter hour |
| `calibration_records_2026.csv` | csv | meter and calibrator serials, certificates, field checks |
| `complaints_register_2026.xlsx` | xlsx | distractor, declared in metadata.json: complaints, dates, dwellings |
| `effluent_quality_2026.csv` | csv | distractor, declared in metadata.json: the site's discharge monitoring |
| `export_manifest.csv` | csv | provenance: what each file is, covers and omits |

## Build record

- `generator/build.py` runs everything: the survey (`world.py`, `sim.py`), the pack (`pack.py`, `docs.py`,
  `postprocess.py`), the golden (`golden.py` over `analysis.py`, `deliver.py`), `metadata.py`,
  `figures.py`, `submission.py`, then `checks.py` and `verify.py`.
- Final run: `checks.py` **377 assertions passed**; `verify.py` **234 independent checks passed**; two
  consecutive builds byte-identical over `target/`, `golden/` and `metadata.json` (combined sha256
  0373bc0f07eea0f6); about 40 seconds.
- `verify.py` reads only the bundle (standard library, numpy-free, pyarrow for the parquet), encodes the
  plan's clauses as its own code and rebuilds every figure: the fourteen specific levels, totals,
  residuals, valid, excluded and stop minutes, the slate, its order, the sixth and the margin, the default
  path's own slate, the highest band and tone verdict at every position, and the six weeks of plant
  figures, against `generator/figures.json` and against the golden table.
- `figures_check.py` exit 0: 90 figures in blocks 1 to 4, none absent from `figures.json`.
- Parameters chosen by search in scratch and never shipped: the designed specific levels and residuals
  (`world.POSITIONS`), the residual texture (`EVENT_DB`, `JITTER`, `SLOW`), the tone survival (`BARRIER`,
  `TONE_K`) and the per-position micro-adjustments (`world.SHIFT`, at most 0.87 dB) that put every printed
  level mid-bin, all 14 distinct, none within 0.038 dB of a rounding edge.
- Invented names: Drumlorne, Tulcarra Foods, Clonaraght, and the townland-style dwelling names in the
  register, checked against the thirty-one Irish local authorities and the sixty largest towns (edit
  distance above 2, no containment). No offline register of Irish townlands was available, which is
  recorded here as the limit of that check.

## Leak check (mechanical half)

`leak.py task182 --asof 2026-10-16`: **REVIEW, no LEAK**, five lines, each answered here.

- Sweep 3, `noise_management_plan.pdf` carries three of five distinctive words of the committed call: the
  words are October, treatment and slot, which clause 6.1 needs to say what the mitigation programme is. No
  figure of the answer appears in any shipped file (asserted: no shipped file holds a specific level, a
  residual level or a corrected level for any position).
- Sweep 4, the plan and the survey notes share eight of the stump paragraph's terms: they are the field's
  own nouns (position, measured, residual, record, register, period), and the plan defines the residual
  because the estimand has to be filed. The sweep's own test is whether the document names the move; it
  does not, and `checks.py` asserts the plan names no background, percentile, L90, stop or non-operating
  state.
- Sweep 4, the prompt carries two stump terms: the prompt has to name the quantity (the specific sound
  level) and the window (the assessment minutes), which is the WHAT every build files. It names no method.
- Sweep 9, `calibration_records_2026.csv` carries five dates after the as-of: they are the meters'
  calibration due dates, a forward validity window, which `reduce-house-fixes` H16 puts on the allow-list.

`guard.py surface task182`: 216 pairs in scope, **0 promoted**; nearest neighbour task228 at 0.096.
Personas in the cut pack: Aiden Hawthorn and Orla O'Hurley, both on the card.
`guard.py heart task182`: **WARN, not BLOCK**; nearest driver 0.07 (task263), answered in the card's
differentiation.

## Pre-ship check (client, eight points)

1. **Domain.** The build is a noise survey reduced to one attributable level per dwelling, which is the
   acoustics practitioner's own determination of a specific sound level. The swap test breaks it: another
   field's nouns have no energetic summation and no quantity that the source's own presence makes
   unmeasurable.
2. **Real work, nothing planted.** The inputs take work to put in order: UTC meters against local
   paperwork, five meters rotated over fourteen positions, two field-check corrections, a met mast at ten
   minutes with a mid-survey unit change and a tip counter, a repeated download, three names per position,
   and band levels on three meters of five. Every one of them comes from the survey's own equipment.
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
