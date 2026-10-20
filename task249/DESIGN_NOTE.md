# task249 design note (architecture 5)

## Draw

Card `cards/task249.json`, architecture 5, a fresh draw on the retired number at the author's request ("whatever was
retired do a fresh rebuild from scratch"), registered 2026-10-20. Architectures 1 to 4 are in the card's lineage with
their fates and in `## Tried and rejected`. Guard verdict WARN, no BLOCK; test.same_puzzle_older and
test.same_driver_older are NOTEs, differentiated on the card against task230, task134, task149 and task452. Each WARN,
answered: repeat.gate_g and overuse.gate_g (method_or_model_selection after task473): the mechanism that carries the
stump is the choice of the calibration model, a relation conditioned on the hydraulic regime against one on turbidity
alone, and no other key is true of it; repeat.question_form (which, after task473): the decision is a designation of
stations to re-issue, so it is asked as which. Two axes were redrawn at registration, each to the honester label and
not merely the passing one: stump_strategy from composition_mix (task473 in the window) to population_selection, which
names the cause, the samples selected by when the field team can reach the river, where composition_mix named its
arithmetic, and which is how this lane files non-random observation timing (task245); org_family from
utility_or_infrastructure (task472) to professional_services, with the world redrawn to match: the programme is run
under contract by an environmental consultancy, whose data manager decides, for the hydropower company that owns the
stations.

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring & Alerting only. Not banned against the last three live builds at the draw (task474 survey-research ETL,
  task473 general statistics ETL, task472 supply-chain ETL). The object is the health of a published data product,
  each station's 2027 suspended-sediment load computed from a turbidity surrogate, and the call is the spring review's
  monitoring decision: which stations' loads fall outside the 15 per cent tolerance and are re-issued before the
  reservoir flushing plan uses them.
- **The seed, re-found.** DQ22 gave the world (a sensor network's published series), the decision (which units'
  published data are pulled or re-issued) and the quantity (each unit's error against a tolerance). The low-cost air
  sensors and their drift are left (spent twice on this number); the pitfall is re-found in surrogate calibration.
- **Niche.** Vasslia Miljørådgiving AS, an environmental consultancy, runs the Fjellbrekke sediment monitoring
  programme under contract for Fjellbrekke Kraft AS, a Western Norwegian hydropower company in inner Sogn: 14
  suspended-sediment stations on the rivers feeding Breiavatn, Kvitstølvatn and Djupevatn, six glacier-fed, five
  rain-fed, three lake outlets. Each logs discharge and turbidity every 15 minutes; the consultancy's field team takes
  depth-integrated samples on routine rounds and on flood callouts; a contract laboratory weighs them. Each station's
  annual load is published to the company from a log-log regression of concentration on turbidity (procedure SMP-03
  v3) and feeds the company's sediment budgets and its flushing plan, fixed on 20 March 2028.
- **The call.** Which stations' published 2027 loads misstate the sediment that passed by more than the review
  tolerance (15 per cent, section 8), and whether over or under. Golden: SKB, JVB, FND and ESK over; the ten others
  within.
- **Shape.** 10, a scorecard of 14 stations checked against one tolerance (verdict and direction), beside two
  per-station audit lines of the loads' inputs (14 hours, 14 counts) and a chart of every station's published load
  against the estimate: 14 + 4 + 28 + 5 = 51 criteria before instruction-following. Decision designation_set, answer
  set_of_items, question form which.
- **Strategy.** population_selection: the calibration samples are selected by when the field team can reach the river,
  a selection correlated with the regime that sets the concentration per unit of turbidity, and the relation fitted on
  the selected samples is applied to the whole year. G14 decisive (the relation conditioned on the regime), G7, G6; gap time then population; Gate G method_or_model_selection; calibration
  physical_verification (the depth-integrated samples); context artifact monitoring_export (the published load report);
  Layer 2 family field_method, pattern own:surrogate-calibration-conditioned-on-hydrograph-limb.
- **Forum, event, organisation.** operations_desk (the programme's data desk signs off the loads), season_or_peak (the
  company's spring flushing window before the melt), professional_services (an environmental consultancy running the
  programme under contract). Role compliance_or_audit (the programme's data manager, who reviews the published loads
  against the procedure's tolerance).
- **People** (`guard.py names --geo Norway --seed 249`): Marianne Lunde, the programme's data manager, who asks; Lise
  Pettersen, the field team lead; Laila Pedersen, the laboratory's quality manager. None appears in the prompt.
- **Data-native sentence.** Sand moves only while a river rises and turbidity barely sees sand, so a unit of turbidity
  carries more sediment on rising water; the field team's working-hours rounds on the glacier rivers land on the melt's
  daily rise and its early flood callouts reach the rivers on the rising limb, so at four stations most calibration
  samples were taken on rising water, and a regression on turbidity alone carries their sand into every steady and
  falling hour of the year.
- **As-of.** Monday 6 March 2028 (the request); the review is dated 13 March, the plan fixed on 20 March. The call is
  retrospective by design: the monitored product is the published 2027 load, and the decision it drives (re-issue
  before the plan reads it) faces forward.
- **Sources.** The client's two-layer standard (field_method); published sediment-monitoring practice: turbidity as a
  surrogate for suspended-sediment concentration calibrated on depth-integrated samples with a log-log regression and
  Duan's smearing, loads summed over 15-minute records, and hysteresis between rising and falling limbs from sand
  entrained on the rising limb. task229 (hydrometry, a daily mean through a convex conversion) and task241 (profiling
  float salinity against ship references) are the nearest builds in the subdomain; neither conditions a surrogate on a
  regime.

## Default path

1. Join the field sheet to the laboratory's results on year and bottle number (final results, both sheets of the
   workbook) and pair each sample, at its UTC time, with the station's nearest 15-minute turbidity reading.
2. Refit the procedure's regression (section 6: log10 concentration on log10 turbidity, Duan's smearing) and apply it
   to 2027's intervals (section 7): every published load reproduces to within 0.1 per cent.
3. Review the regression the way a surrogate rating is reviewed: residuals against discharge and season, discharge
   added as a second variable where it tests significant (no station moves past 15 per cent), seasonal terms (JVB
   alone), the trip type of each bottle (TVE in, JVB out).
4. Compare each published load with the refitted estimate under the review tolerance.

Ends on: no station re-issued, all 14 within 15 per cent

Golden: SKB, JVB, FND and ESK over by more than 15 per cent, re-issued; the ten others within

## Stump sentence

A competent analyst refits each station's turbidity regression on all its samples, with discharge or season added
where they test significant, reproduces the published loads and ends on no station re-issued, all 14 within 15 per cent
(or JVB alone); the step that lands it there is treating the calibration samples as a fair draw of the year, when sand
moves only while the river rises and at four stations most samples were taken on rising water (the melt season's
working-hours rounds at JVB, SKB and FND, the early flood callouts at ESK, SKB and FND). Conditioning each station's
relation on whether the river was rising at the sample, read from the 15-minute discharge, and applying it to every
interval of 2027 with that interval's own state puts SKB (+39 per cent), JVB (+105), FND (+42) and ESK (+78) over, and
every other station within 7 per cent.

## Three rules

- **Task type:** physical-environmental-sciences / sensor-calibration-measurement, which serves Data Quality Monitoring
  & Alerting: the published loads are the monitored data product and the call is the review's monitoring decision, which
  station series fall outside the tolerance and are re-issued.
- **Domain test:** the quantity that decides is each station's 2027 suspended-sediment load, which sediment monitoring
  estimates through a turbidity surrogate calibrated on depth-integrated samples (log-log regression, Duan's smearing,
  summed over the 15-minute record), here conditioned on the hydrograph limb because sand is entrained on rising water
  and turbidity barely registers sand.
- **Swap:** "which of our 14 hospitals' published 2027 admissions misstate what happened by more than our tolerance"
  keeps the sentence and loses the task: there is no turbidity sensor blind to one size of particle, no hydrograph whose
  rising limb moves sand, no melt cycle or flood callout setting when samples are taken, so a relation conditioned on
  rising water has nothing to act on.
- **Layer 1:** the laboratory's former system's 2025 sheet in Norwegian headers beside the current system's 2026 and
  2027 sheet (the LIMS migration); corrected results kept beside the replaced ones (the laboratory's re-weighing); bottle
  numbers restarting every year (the field labels); sample times in local time with their UTC offset against loggers
  in UTC (the field app); rows re-sent after logger outages (the telemetry); the load table inside the report's PDF
  (the annual report); discharge to three significant figures (the hydrometry system). None is placed to be caught, and
  the call is the same under every handling (R2 and SF6 to SF10 in checks.py).
- **Layer 2:** field_method: the surrogate relation conditioned on the hydrograph limb, the method a sediment
  hydrologist uses when the samples' timing is not representative of the record, where the easy routes refit the
  published relation or add the reflex covariates (discharge, season, trip type).
- **Decisive step:** adding an indicator of rising water at each sample, from the rate of rise of the 15-minute
  discharge, to each station's log-log relation and applying it to every 15-minute interval of 2027 with that
  interval's own indicator, rather than refitting on turbidity alone or with discharge, season or trip type.
- **Not semantics:** reading every field, code, unit and definition right (final results, both LIMS layouts, the
  offset on each sample time, the procedure's method, the tolerance) leaves the refit on no station re-issued: no file
  names rising water, a limb or sand, and the samples' excess shows only when their residuals are read against the
  discharge's rate of change.
- **Not rule application:** the procedure files the estimand (the sediment that passed, the year, the tolerance) and
  the published method; executing every filed rule reproduces the published loads to 0.1 per cent and re-issues none,
  and no filed rule mentions the hydrograph.
- **Analyst test:** a strong analyst who reads every file right refits each station's regression, adds discharge and
  season where they test significant, and ends on no station re-issued, all 14 within 15 per cent (JVB alone with
  season); on the generator's clean truth the published method overstates the same four and the rising-water term
  alone files the golden (R3a, R3b in checks.py).
- **Estimand:** procedure SMP-03 v3 sections 7 and 8 with the prompt: for each of the 14 stations in the register,
  the published 2027 load (1 January 00:00 to 31 December 23:45 UTC, tonnes) against the suspended sediment that passed
  the station in that year, re-issued when it misstates it by more than 15 per cent, over or under.
- **No decoy:** nothing is planted: the report's loads are right on their own method and are the comparison the call
  needs; no memo, draft or voice argues a set; the request names no station; the two distractors (precipitation,
  reservoir levels) rank nothing.
- **No certified replay:** no certified or validated load exists for a method to reproduce; the conditioning is found
  in the samples' own residuals against the discharge record, and the published loads tie under the easy route.
- **Lesson:** a surrogate relation calibrated on samples whose timing over-represents one hydraulic regime carries
  that regime into the whole record, and conditioning the relation on the regime, read from a second continuous
  variable, is the field's correction. No build on file teaches it (task229 converts a daily mean through a convex
  rating, task241 calibrates float salinity against ship casts, task247 reads near-real-time against reprocessed SST).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a
reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the published loads: none | the report | the report's table | yes | none | no | read off | readable |
| 1 (default) the procedure refitted: none | procedure section 6 | the field sheet, LIMS, record | yes, reproduce the published figure | the report ties to 0.1 per cent | no | one regression | readable |
| 2 discharge added (the field's two-variable surrogate): none | none | discharge_m3s | yes | the report | no | one regression | readable |
| 3 season or hour of day: JVB | none | the timestamps | partly | none | no | one regression | readable |
| 4 the bottle's trip type: ESK, FND, SKB, TVE | none | the field sheet's trip column | yes, every visible attribute held | none | no | one regression | readable |
| 5 routine bottles only: ESK, GRV, TVE | none | the trip column | partly, storm samples set aside | none | no | a filter | readable |
| 6 2027 bottles only: JVB and SKB under | none | the sample dates | partly, the latest calibration | none | no | a filter | readable |
| 7 (decisive) the relation conditioned on rising water, read from the 15-minute discharge's rate of rise, applied per interval: SKB, JVB, FND, ESK | no sentence names rising water, a limb or sand; the procedure names only turbidity | the rate of rise is in no column; it is computed from the discharge series at another grain | no: the reflexes are discharge, season and the trip type | the samples refute the turbidity-only relation only when their residuals are read against the discharge's rate of change (t from 18 to 44 at the four, the trip type then near nought) | no | not linear: a state per sample and per interval, a fit per station, a sum over 35,040 intervals | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the 2027 load's year | 1 January 00:00 to 31 December 23:45 UTC | the Norwegian calendar year | same call | asserted (procedure section 7 names UTC) |
| SF2 | the published load | the report's tonnes | recomputed from the report's coefficients | same call | asserted: the report's loads are the procedure's |
| SF3 | misstates by more than 15 per cent | against what passed | against the published load | same call | asserted |
| SF4 | over or under | published above what passed is over | none differs | converge | all four over (asserted) |
| SF5 | the calibration samples | every accepted sample of 2025 to 2027 | 2027's alone | JVB and SKB under | procedure section 6 "2025 to 2027 for the 2027 loads" (asserted read back) |
| SF6 | a bottle's result | the final result | the replaced result kept | same call | asserted |
| SF7 | the 2025 results | the former system's sheet read with the current one | 2025 left out | same call | asserted |
| SF8 | pairing a sample with turbidity | the nearest 15-minute reading | interpolated between readings | same call | asserted |
| SF9 | a sample's time | the field app's time with its offset | the wall clock read as UTC | the refit misses the report | the offset on every value; the wall clock does not reproduce the published loads (asserted) |
| SF10 | re-sent record rows | each interval once | duplicates kept | same call | none in 2027 or near a sample (asserted) |
| SF11 | which bottles calibrate | every river sample in the sheet | none differs | converge | every bottle is a river sample (asserted) |
| SF12 | retransformation | Duan's smearing (procedure section 6) | none | same call | asserted |
| SF13 | logarithm base | log10 (procedure) | natural logs | converge | a constant factor (asserted) |
| SF14 | discharge | the record's one series, three significant figures | none differs | converge | asserted |
| SF15 | the stations | the register's 14 | none differs | converge | asserted |
| SF16 | Ask A's years | 2025 and 2026 in UTC | in Norwegian time | same figures | nothing unusable within two hours of either edge (asserted) |
| SF17 | Ask A's hours | intervals over four, whole hours | none differs | converge | no station on a half hour (asserted) |
| SF18 | Ask A's repeated rows | an interval once (procedure section 5 counts intervals) | rows | same figures | every repeat is exact (asserted) |
| SF19 | Ask A's upper end of the range | 1,000 FNU on a TS-10 until the station's TS-40W (procedure section 2, register, maintenance log) | 4,000 FNU throughout | moves four stations | procedure section 2 gives each sonde's range; no TS-10 reading above 1,000 (asserted) |
| SF20 | Ask A's fouled or sonde-out rows | F and M, and G and O before 14 April 2026 | F and M alone | moves every station | the maintenance log: the O and M rows are exactly its logged sonde-out times, the G spans end at its "flagged back to last clean" visits (asserted) |
| SF21 | Ask A's checked readings | K and C usable | counted unusable | moves every station | procedure section 5 (C is usable); K sits on each logged handheld check before the migration (asserted) |
| SF22 | Ask B's 2027 samples | every bottle sampled in 2027 | none differs | converge | the batch export holds each once (asserted) |
| SF23 | Ask B's control concentration | the lot's concentration in the quality statement | the export's nominal 50.0 for every lot | moves 13 stations | procedure section 4 "the control suspension's concentration"; the statement's table gives KS-27-06 at 54.0 (asserted read back) |
| SF24 | Ask B's blank | a change of more than 0.5 mg either way | gains only | moves stations | section 4 "changes by no more than 0.5 mg"; a blank below -0.5 mg ships (asserted) |
| SF25 | Ask B's aliquot agreement | against their mean (section 4) | against the larger aliquot | same figures | asserted |
| SF26 | Ask B's samples per station | one line per sample | none differs | converge | asserted |

## Ladder

Seven wrong rungs and the golden, each a complete defensible analysis, each dying to one fact of the samples (sets on
the cut pack, printed by `generator/pair.py --ladder`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | the published loads | none | the review exists to test them |
| 1 (default) | the procedure refitted on every sample | none | the residuals split by whether the river was rising at the sample |
| 2 | discharge added | none | turbidity already carries discharge; the residual split stays |
| 3 | season or hour of day | JVB | the split appears at every season at SKB, FND, ESK and inside JVB's own summers |
| 4 | the trip type | ESK, FND, SKB, TVE | with rising water in the model the trip type adds nothing at any station (absolute t under 2.5); TVE's callouts fell mostly on falling water |
| 5 | routine bottles only | ESK, GRV, TVE | routine rounds land on the melt's rise as surely as callouts land on a flood's |
| 6 | 2027 bottles only | JVB, SKB under | 44 to 101 bottles become 14 to 34; the procedure calibrates on three years |
| 7 (golden) | the relation conditioned on rising water, applied per interval | SKB, JVB, FND, ESK over | |

- **Margins.** Every rising-water specification on file (thresholds 0 to 3 per cent an hour, unsmoothed, the past hour
  or two, separate fits, discharge and season added, a linear or positive rate of rise, rising turbidity smoothed over
  one to six hours) files the four: the smallest flagged misstatement 18.5 per cent (rising turbidity over an hour), the
  largest other station 6.9 per cent (asserted).
- **Position.** No wrong rung reaches the four; rungs 4 and 6 reach two or three of them with a wrong station or a
  wrong direction.
- **Dominance.** On rising water a unit of turbidity carries 2.2 to 2.8 times the concentration at the four (10 to the
  0.34 to 0.45), and 48 to 75 per cent of their samples were taken on rising water against 1 to 16 per cent of 2027's
  intervals.
- **Worth.** Four re-issues of 14; the clean truth's sediment puts the same four over (R3 in checks.py).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's 14 stations (SF15) |
| 2 | Unit of account | one station's annual load, in tonnes (section 7) |
| 3 | Attribution window | calendar 2027 UTC (section 7, SF1) |
| 4 | As-of dating | the review of March 2028 on the report of 15 February 2028; 2027's records complete |
| 5 | Version basis | procedure v3; the report as issued; LIMS final results (SF6) |
| 6 | Denominator | the misstatement against what passed (SF3) |
| 7 | Weighting | each 15-minute interval's concentration times its discharge (section 7) |
| 8 | Window length | the three calibration years (SF5) |
| 9 | Boundary inclusivity | more than 15 per cent re-issues; nothing within 3 points of it on any specification |
| 10 | Rounding path | none before the comparison; asks in whole hours and whole samples (SF17) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every 2027 interval and every bottle reported |
| 13 | Order of operations | results, pairing, fit, prediction per interval, sum, comparison |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | final over replaced results (SF6); re-sent rows once (SF10, SF18) |
| 16 | Identity normalisation | year and bottle number across the sheet and both LIMS layouts; station codes |
| 17 | Netting against gross | none |
| 18 | Dimensional units | mg/L equals g per cubic metre; cubic metres per second times 900 seconds; tonnes |
| 19 | Code and status semantics | trip types; LIMS status; the record's flags (SF20, SF21) |
| 20 | Integerisation | whole hours, whole samples |
| 21 | Clause scope | section 8 applies to every station, both directions |
| 22 | Forward window contents | the plan reads 2027's loads as published or re-issued; nothing forecast |

## Literal reader

Executing the prompt and the procedure word for word: for each of the 14 stations, the published 2027 load against
the suspended sediment that passed the station in calendar 2027 UTC, re-issued when it misstates it by more than 15 per
cent either way. What passed is not observed; it is estimated from the shipped samples and the 15-minute record, and
the procedure gives the published method, not the truth. Every estimate whose relation is conditioned on rising water
(any of the sixteen specifications under Margins) files the four, and every fork row files the same call; the easy
answer, none, comes from the easy method on the same literal estimand, never from another reading.

## Oracles

None for the call: no validated load, sediment survey or earlier review ships. The report ties under the easy route by
construction, which is the stump's own identity. For the asks, the maintenance log (sonde-out times, the fouling
remarks, the handheld checks, the sonde change) and the quality statement (each control lot's concentration) referee
the devices; neither names a station's figure.

## Ask sheet

**Ask A, each station's hours in 2025 and 2026 without a usable turbidity reading (14 figures, whole hours).** H18: the
turbidity record of the calibration years is the input the regression pairs every sample with, so its health is the
audit trail of the call's input; the call reads the record only at the samples' own intervals and in 2027, which no
device reaches (asserted). Use: the review sheet's record line, as every spring. Primary devices: D2, a label stored
before a silent switch, twice over. The data team's database migration of 14 April 2026 changed the flag letters (G
fouled and O sonde out before it, F and M after; K and C for a handheld check), and procedure section 5 and the
dictionary give the current letters only, so executing the filed letters misses every older fouled or sonde-out
interval (-15 to -350 hours at all 14), while counting every flag counts the checks (+1 to +4 at all 14); the old
letters are found only through the maintenance log, whose sonde-out times the O rows match exactly and whose "flagged
back to last clean" visits end each G span. The register gives each station's current sonde (TS-40W, 4,000 FNU) and its
installation in autumn 2026; the TS-10's limit of 1,000 FNU before it holds the readings at the upper end of the range,
unflagged (-2 to -16 at four stations on the register's sonde). D4: an interval the logger never sent has no row (-51 to
-300 at all 14 counting rows only). Hazards: rows re-sent after outages, exact repeats. Path: the record, the
register, the maintenance log, the procedure, the dictionary (5 files, 7 columns). Realism: logger and database
migrations change flag letters and leave old rows as they were; sondes saturate at full scale.

**Ask B, each station's 2027 samples weighed in a batch that failed its quality control (14 figures, whole samples).**
H18: the 2027 bottles are a third of the regression's samples, and the batch quality control is the audit trail of
their concentrations; the call reads the laboratory's results and never the batch export. Primary device: D2, the
export's control column is the LIMS template's nominal 50.0 mg/L on every line, while lot KS-27-06, in use from 1 July
2027, is 54.0 mg/L in the quality statement; recovery against the nominal fails good batches through the second half
of the year (13 of 14 stations moved, by up to 4). D3: each aliquot's concentration is its net mass over its own volume
(200 or 250 mL). Hazards: the batch's results repeated on every sample line (a batch counts once in deciding failure,
its samples each once per station); a blank below -0.5 mg. Path: the batch export, the quality statement, the field
sheet, the procedure (4 files, 9 columns). Realism: a LIMS template keeps its default nominal when a control lot
changes; certified lots differ from the nominal they were prepared to.

Main population zero-counts: the call reads the field sheet, both LIMS sheets' results, the record's discharge and
turbidity in 2027 and at each sample's interval, and the report; no flag, gap, check, sonde limit or re-sent row sits
within three hours of a calibration sample or anywhere in 2027 (asserted per station), and the call never opens the
batch export, the quality statement or the maintenance log.

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the migration's old letters G and O (D2, primary) | A | -350 hours |
| the checks K and C counted as flags | A | +4 hours |
| the TS-10's 1,000 FNU limit read off the register's TS-40W (D2, primary) | A | -16 hours |
| intervals with no row (D4) | A | -300 hours |
| the export's nominal 50.0 for lot KS-27-06 (D2, primary) | B | +4 samples |

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed on the fields it names) | Verdict |
|---|---|---|
| Ask A, hours, all 14 stations | a full 15-minute grid, re-sent rows once, the procedure's letters F and M, the TS-10's limit before each station's TS-40W | miss |
| Ask B, samples, all 14 stations | each batch once, concentrations from mass and volume, recovery against the export's control column | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 1 of the 28 ask figures (KVF's nought under both
controls), the mirror (off the call, the same ask paths) 1; a response that decodes the old letters through the
maintenance log and reads each lot's concentration keeps all 28.

Pair ceiling: 30.5 ((38 + 7 + 55 x 1/28) and (5 + 7 + 55 x 1/28), averaged)

Mirror leakage: 3.6 per cent of ask weight

## Tried and rejected

- Drift forecast from the cumulative particle load through an optical PM sensor (drift accrues with dose, not calendar
  time): the lesson is task46's (a rate law stationary only in cumulative service exposure), so the driver is spent.
- Seasonal confounding of a PM sensor's gain by humidity growth or aerosol type: the shape of task248's driver (a
  covariate moving over the year against a level comparison), one build earlier.
- An analyser ask (each analyser's 2027 days over 120 micrograms on the EU maximum daily 8-hour mean): every device it
  carried (span-check hours flagged N, the old analyser's parallel rows) is adjudicated by the station sheet, so the call-landing
  response executes it and keeps every figure; dropped for the node quarter's single silent device.
- Architecture 1 (each node's span read from its spread against the four distant analysers, the paired slope
  attenuated by the sites' partial hourly agreement): the stage 4 reader (medium effort, about two minutes) landed the
  call with an errors-in-variables slope instrumented by the other stations' mean, cued by plan 4's "true ozone
  concentration at its inlet", and kept all 36 ask figures after reading the vendor's firmware note. Regression dilution
  is textbook statistics, so the decisive step is readable to a strong model; and an ask one device deep falls to one
  document read. Realism tells it named: firmware dates cycling in ten-day steps, installation dates on a fixed
  five-week pattern, visit slots on a fixed cadence, the ES4104A analyser's model against its serial (T400 and API400E),
  head serials stepping by 37. The judge's pass on the same bundle: DETERMINISTIC (write-up wording only); its residual
  reading F1, the spread of the four stations' averaged series, gives 10 nodes, so architecture 2's write-up says the
  analysers' hours are pooled.
- Ask A on firmware 4.2's renumbered codes alone, the release note carrying a table of the codes up to 3.7 and from
  4.2: architecture 1's stage 4 reader read the note and kept 36 of 36. The note now gives 4.2's codes only (the records
  show the old meaning: before each node's update its status-1 records are the two warm-up hours after a restart), and
  the restart clocks stand beside it as a second primary, each moving all 36 figures alone.
- The firmware table without a date for OZ19 read as OZ19 never reaching 4.2: the spare's records after the 25 January
  rename lost their humid hours (OZ19 +89 against +18 to +24 elsewhere); OZ19 runs 4.2 from the spare's start at 11:00
  on 9 January, in the solver, the verifier and A1.
- Architecture 2 (each node's span read on the mixed afternoon hours, the hill villages above the night's surface
  layer): the stage 4 reader (Sonnet, medium, about four minutes) landed the call with a regression on the four
  analysers, the 900 m sites' night-time intercepts and the register's altitudes pointing it to the midday hours;
  the judge's pass on the same bundle was DETERMINISTIC, APPROVE, and Ask A held (0 of 36). A site's night-time
  decoupling shows in any residual by hour of day, so the decisive step is readable to a strong model.
- Architecture 3 draw, 2026-10-19, candidates that died before the card was filed: register coverage by dual-system
  estimation within post-strata after erroneous enumerations (task448 already runs capture estimated within route
  strata in the same task type); an adaptive item bank's drift under compromise read with purified anchors (filed as
  drift on the bank's scale, its literal reading is the contaminated thetas, so the estimand forks unless it names
  the purification, which files the method); rapid guessing read from item-specific response-time thresholds (the
  decisive step is a threshold choice, a coin flip in the client's measured runs); this world's forward referral rate
  under the SE-scaled rule (1.645 times the standard error of the difference: the rule's own scaling compresses every
  account into 2 to 9 per cent, too thin for a cap) and a fixed eight-point band (elite accounts at 40 to 60 per cent,
  no firm would adopt it, and a 2028 verification record would let a solver carry each account's empirical shortfall
  forward). The confidence-band rule on the verification score, with the check new in 2029, keeps the spread
  realistic and leaves no per-account history to carry.
- Ask A's highest weekly exposure of any item (four figures): any response that checks the attempts against the
  register keeps it whole, so the ask's weight sat on the one device a careful response can find; replaced by the
  count of items rested for 2029, which the suite moves as well, and the ask cut to five figures.
- Appeal outcomes recorded as later rows of the original case: each case's latest row, the habitual read of a decision
  log, filed the golden, so the impersonation ask carried no device. The desk now logs an appeal as a case of its own,
  as its own sheet would, and a sitting's standing is the latest decision across the candidate's cases.
- The synthetic suite's sittings labelled release 5.3.2 in the week of 3 July, before the release went live: a marker
  isolating the device rows in one week. They now carry the release in service, as the platform stamps every attempt.
- Shrinkage of each pool's top share with each candidate's reported error (Kelley's formula at the estimate) taken as a
  competing reading: it adds NVK, UJB and OJS, but the study's own top tenth of MAT-R scorers refutes it (it predicts
  their MAT-V a tenth of a logit lower than scored) while the shrinkage at the ability, the full posterior and the
  world's own truth all file the 15. Kept as a rung and stated in the write-up's critical components, so a judge sees
  the refutation in the shipped data.
- Architecture 3 (each account's 2029 referral share read through its shortlist's regression to the mean, MAT-R's
  error at the ability and the retest gain at the interval): the stage 4 reader (Sonnet, medium, about eleven
  minutes) landed the call with a latent-ability model (a tier prior deconvolved from the 2028 pool, Table 4.3's
  errors, the study's fitted gain), checked against the study's referral rates by interval and by MAT-R level, and
  kept all 19 ask figures, finding the 6,400 Monday-night identities outside the register, each candidate's latest
  case decision and the fresh booking references from release 5.3.2; the judge's pass on the same bundle was
  DETERMINISTIC, APPROVE. Selection on a noisy score is the textbook regression to the mean, a shrink the author file
  names as a reflex, so the decisive step is readable to a strong model, and three devices one cross-file check deep
  each fall to the hygiene battery. Realism tells it named: round plan counts and shortlist ratios, the suite's
  identical early-Monday timing and short sittings, uniform selection-day spreads, the study's fixed interval grid.
- Candidate 1 as offered to the author (signed-out visitors on other browsers as the comparison for signed-out WebKit identifiers): in a world without a meter it is the golden, and holding every visible status fixed is the careful opponent's reflex, so it would be landed by the first thorough reader; prototyped at the draw (proto3 and proto4 in the session scratchpad), the decisive step moved to what that reflex gets wrong, the sign-in the capped meter produces. A first cut of the print-subscriber skew modelled print readers as daily readers and moved nothing (the skew shifted the device-only route by 0.5 points): daily readers never reset, so print subscribers are drawn as the weekly and occasional online readers a print household is.
- The sign-in trap at the draw's weekly gaps (eight to nine days, two to three registration chances in ten on WebKit):
  the sign-in split fell only 2.6 points short of the golden on the meter editions, inside a reader's variant of it;
  weekly readers now come every eight to twelve days, so WebKit's meter almost never reaches the wall, and the gap is
  5.5 to 6.6 points.
- The hybrid (signed-in browsers from the register, signed-out identifiers by every other browser) at the draw's
  reader mix: within 1.5 points of the golden everywhere, because removing the few signed-in WebKit readers barely
  moves the pool's revisits; it lands the call unless the signed-in pool is large and frequent. A local edition's
  loyal core (daily and regular readers about a third of the month's browsers, registered on every engine) makes it
  fall 4.4 to 5.7 points short on the meter editions.
- Print-heavy editions under the line to catch the signed-in ratio: the ratio over-corrected them by only 2.5 points
  at a realistic print share; with the loyal core the ratio falls 10 points short on every non-print edition, so it
  needs no print-below rung, and those editions became ordinary unnoted ones.
- Ask B's primary as return slips dated by collection (weekly points covering the week before): the quarter starts on
  a Monday and ends on a Saturday, so a slip never straddles it and shifting every slip one publication day gives the
  exact answer; dropped for the COMBI's e-paper on the e-paper platform.
- Ask A's primary as contacts archived after the year's end and missing from the export: their groups at archiving
  would have to ship somewhere, which marks them; dropped for the export's current groups after the new year's mailing.
- A 0.6 scale world with 5.3 million sessions at full scale: the export reached 75 MB; the populations were scaled by
  0.6, daily readers' sessions a day trimmed, and the export sorted by identifier (3.0 million rows, 34 MB).

- Architecture 4, stage 4 round 1 (2026-10-19): reader 1 (Sonnet, medium, about thirteen minutes) landed the call without
  the decisive step. Every browser had carried one user-agent string and one address all quarter (3,048 prefixes,
  about 65 identifiers each), so chaining the anonymous WebKit identifiers within user agent, address and edition, each
  new one at least seven days after the chain's last session, matched the register's devices within 0.04 per cent and
  filed the golden's eight. Reader 2 fell on the trap (three editions, the signed-in ratio bridged by state). The judge's
  pass on the same bundle was DETERMINISTIC, APPROVE. The landing came through a construction defect, the browsers
  observable through a fingerprint no real export carries, not through the decisive step. Repaired in the generator:
  - Addresses now vary by session: household lines that reconnect (daily, weekly, monthly or fixed) inside each
    edition's region's provider blocks, mobile networks' shared pools, and office lines on weekday daytimes.
  - User agents are shared by version and move with each release at the browser's own lag; Safari's system token is the
    one Safari has reported since version 26.

  After the repair, reader 1's chain misses the register's devices by 24 to 64 per cent. Every chaining key fails its
  own check on the registered identifiers by 12 to 43 per cent and files 0, 4 or 9 editions (chain_test.py in the
  session scratchpad). The route table is byte for byte the same.
- Ask A's primary as the export's current groups after the new year's mailing, with the mailing's additions in the
  group-change log: both stage 4 readers reversed the log and kept all twelve figures (a change file over a base list,
  which the hygiene battery executes). The mailing's additions now come through the newsletters' one-click links,
  recorded only as clicks in the activity log among the article clicks; the preference centre's log does not hold them.
- Ask B's primary as the COMBI's e-paper counted again: both readers matched order_ref Kombi to the COMBI and kept every
  figure (one dictionary line and the reference settle it). It stays a hazard. The primary is now the circulation
  system's release of 6 November, which wrote the date of a saved change into the start date until the fix of
  4 December; only the numbers' entry order finds it.
- Realism tells the readers named:
  - Fixed: e-paper accesses starting in 1974, before the e-paper existed (each plan now starts no earlier than its
    launch); one order reference on two accesses (now unique); start dates spread evenly back to 1974 (now a tenure
    curve, with subscriptions older than the system carrying its go-live date).
  - Kept: 88 per cent of sessions signed in, which a registration wall after five free articles produces in frequent
    readers; Rhineland-Palatinate's editions print-heavy and Hesse's digital, a rural against commuter-belt geography.
- Stage 4 round 2 (2026-10-19, target.zip d00ed7b6): both readers missed the call. Reader 3 filed the default path's
  four (the signed-out replay with edition weights); reader 4 filed nine, Bergstetten marginal (signed-in readers
  reweighted by session count). The newsletter device held for both: each noticed 49 contacts whose groups the
  preference centre's log does not explain and left them as exported. Reader 4 kept all twelve sold-copies figures (12
  of 24, exit 1). It was cued by twelve subscriptions the release had re-dated past their own end date, an impossible
  record that a start-before-end check finds, then the numbers' entry order and the COMBI accesses' earlier starts. The
  judge: DETERMINISTIC, APPROVE. Repaired: the release re-dates only a subscription still delivered when the change is
  saved; customer numbers are unique (reader 3 found trials sharing a daily subscriber's number); retail points keep
  a weekly rest day or a holiday closure (reader 4: exactly 378 rows on every issue).
- Stage 4 round 3 (2026-10-19, target.zip 31ad0d1e, the final pack). Reader 6 missed the call: the sign-in split's
  four, with 0 of 24 ask figures. Reader 5 landed the call with 0 of 24 ask figures (exit 1). It calibrated each
  anonymous WebKit identifier's share of a browser on the signed-in WebKit browsers, stratified by edition, by whether
  the cookie predates the quarter, and by the identifier's sessions in the month (1, 2, 3, 4 or more), and filed the
  eight with Bergstetten at 24.2. Round 2's reader 4 took the same calibration with the strata pooled over editions and
  filed nine (Bergstetten 25.8). The light strata of the signed-in WebKit pool are mostly print subscribers, the
  readers whose sign-in the meter does not select, so the stratified calibration leans on the very population the
  golden validates on, without the reader naming it. The judge's pass on this pack: DETERMINISTIC, APPROVE (the 24 ask
  figures exact). The cap's selection runs through visit spacing, which an identifier's own session count partly
  shows, so any calibration stratified on activity recovers most of it. Four of five clean readers across rounds 1 to
  3 missed the call (one landing, one more within one marginal edition); round 1's other landing came through the
  repaired fingerprint. Under the two-reader rule a call any reader lands is spent. Hardening the ladder against one
  estimator is not a repair, so shipping as measured, a fifth architecture or retirement is the author's call.
- Architecture 4 as a whole (WebKit's seven-day cookie cap, the meter's selection of who signs in, the transport within
  edition, month and device class): spent at stage 4 round 3 when reader 5 landed the call. The cap selects through
  visit spacing, which an identifier's own session count records, so a calibration stratified on activity recovers the
  selection. The number was retired on 2026-10-20 at the author's choice.
- Retired on 2026-10-20 at the author's choice when architecture 4 was spent (four architectures: 1 and 2 a PES
  low-cost sensor network's drift pull list, 3 a psychology verification check's genuine referral rate, 4 Product
  Analytics' WebKit cookie cap), and un-retired the same day at the author's request for a fresh rebuild. The lesson
  the four paid for: a transport or selection a unit's own trace can reconstruct is spent; architecture 5 puts the
  regime in a second continuous record and the selection in when the field team could reach the river.
- Architecture 5 draw, candidates set aside before the card was filed: a stage-discharge rating's hysteresis on the
  rising limb (task229's hydrometry world, the subdomain's spent neighbour); a seismic network's station leverage (the
  golden's and the easy route's ranges overlapped, 72 to 89 against 84 to 93 per cent); a solar array's soiling
  (task152's ground); a fixed sampling clock aliasing the tide; light traps under the lunar cycle; sensor warm-up after
  restarts. The turbidity surrogate conditioned on the hydrograph limb was the one whose decisive step the samples
  themselves force and no file names.
- The prototype's routine rounds drew fractional days, so rounds fell at any hour and the glacier stations' summer
  rounds missed the melt's rise; fixed before any tuning was trusted.
- MKE as a sand-rich glacier station sampled on evening rounds with early callouts (a trap for the trip type): the
  linear and positive rate-of-rise relations read it at +12 to +20 against the rising indicator's near nought, a fork
  on the main call; MKE is now a silty station below a proglacial lake, inside 8 per cent on every specification.
- JVB with one round a month: some rising-water specifications fell to +5 to +9 (rising turbidity, positive rate of
  rise), too close to the tolerance; two rounds a month in the melt season and a sandier bed put every specification
  above +18.
- Stations drawn on shared random seeds had identical discharge histories (four glacier rivers, three rain rivers,
  three lake outlets); every river now runs its own hydrology under one regional storm calendar.
- The field app's wall-clock time without its offset: in the prototype, read as UTC, it moved several stations inside
  the tolerance past 15 per cent on the golden method, so Layer 1 carried the call (R2); every sample time now carries
  its offset, and the wall clock read as UTC fails to reproduce the report (SF9).
- Every station's bottle count a multiple of six (no round ever missed, every callout two bottles): rounds are now
  missed at a realistic rate and callouts bring back one to three bottles (44 to 101 per station).
- A field remark "rising, brown water" on callout bottles named the decisive regime; the remarks say "high water" and
  "brown water" only.
- Ask B per month (12 figures of nought to three): the template's nominal moves only the second half's months, so the
  cracker kept the first half's; per station, the stale lot moves 13 of 14 figures.
- A laboratory re-run of a failed batch as an Ask B device: suspended sediment by whole-sample filtration cannot be
  re-run; dropped as unrealistic.
