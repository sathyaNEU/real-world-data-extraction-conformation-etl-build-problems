# task249 design note

## Draw

Card `cards/task249.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. test.same_puzzle_older
and test.same_driver_older are NOTEs, differentiated on the card against task104, task134 (v1 lineage), task236,
task453 (v1 lineage), task463, task501 (v4 lineage) and task70 (v2): none of them reads a unit's gain against
references elsewhere. Each WARN, answered: overuse.objective (Data Quality Monitoring in 4 of the last 12): the lane is
Data Quality Monitoring & Alerting; repeat.gate_g and overuse.gate_g (method_or_model_selection after task268): the
decisive step is the choice of estimator for a filed quantity, and no other key is true of it. Nearest driver 0.06
(task253 v3 lineage).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring; not banned against the last three builds (task165 urban forecasting, task268 survey descriptive, task248
  epidemiology data quality). The object is the health of a low-cost ozone network's data, how far each node's span has
  drifted from true ozone since the heads were set at installation, and the call is a monitoring decision: which nodes
  go on the pull list for recalibration at the June 2028 round, before the summer ozone season.
- **The seed, re-found.** DQ22 gave the world (a low-cost sensor network serviced in rounds), the decision (the pull
  list for the next maintenance round) and the quantity (each sensor's drift against a tolerance). Its pitfall (the
  direction of the calibration regression at a collocation) belongs to a sensor sitting beside its reference; here no
  node sits beside one, and the decisive step is how a node's span is read against analysers kilometres away.
- **Niche.** A public research foundation in the Spanish interior runs 36 low-cost ozone nodes (gas-sensitive
  semiconductor heads) on school and municipal roofs across a comarca, beside the regional government's four reference
  analysers (UV photometry). The heads were set against a reference at installation in autumn 2027; their span (the
  change in the reading per unit change in true ozone) drifts over months. At each maintenance round the contractor
  pulls the nodes on the list, takes them to a reference station for a week, and resets them.
- **The call.** Which nodes go on the pull list for the June 2028 round, judged on each node's span over the eight
  weeks to 31 May 2028 against the quality plan's band of 0.85 to 1.15.
- **Shape.** 10, a scorecard: each of the 36 nodes against the band, the list, the count, each listed node's direction,
  and the asks; over 25 criteria. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** other, named in the card's notes: an errors-in-variables attenuation from a remote reference. G16
  decisive (which estimator of a filed span), G5 beside it; gap population (the analyser's hourly series is not the air
  at the node's inlet); Gate G method_or_model_selection; calibration none (no corpus of settled outcomes ships; the
  analysers' own record shows the shared regional distribution); context artifact filed_standard (the network's quality
  plan); Layer 2 family estimation_fit, pattern own:span-from-distributions-against-a-regional-reference-not-paired-slope.
- **Forum, event, organisation.** operations_desk (the network coordinator sends the list to the maintenance
  contractor), season_or_peak (the June round is the last before the summer ozone season), research_or_statistics_office
  (a public research foundation). Role field_unit_lead (the network coordinator).
- **People** (`guard.py names --geo Spain --seed 249`, locale es_ES): Matilde Criado, the network coordinator, who
  asks; Adán Ruano, the contractor's field technician; Edelmira Urrutia, the regional network's data officer; Paulino
  Cardona, the centre's sensor scientist. None appears in the prompt.
- **Data-native sentence.** Ozone is a regional pollutant, so the background sites of a comarca share one distribution
  of hourly ozone over weeks, but two sites kilometres apart agree only partly hour by hour (a shower, a sea of cloud, a
  plume reaching one and not the other), and a slope fitted on paired hours is pulled toward zero by exactly that
  partial agreement: a healthy node far from every analyser looks as if it has lost span, and a node whose span has
  risen looks healthy.
- **As-of.** Thursday 1 June 2028, after the export of 31 May and before the round of 12 June.
- **Sources.** The client's two-layer standard (estimation_fit); the low-cost sensor literature's proxy methods for
  network calibration (a node's distribution over a window matched to a nearby regulatory station's, used for drift
  detection in dense ozone networks) and the regression-dilution result for a slope whose regressor carries error. No
  build on file reads a sensor's gain against a reference elsewhere through the spread of their distributions (task241
  compares a float with a reference on a conserved coordinate; task246 removes measurer offsets from single readings;
  task262 carries a reliability ratio from a selected subsample).

## Default path

1. Read the quality plan (span against the band 0.85 to 1.15 over the eight weeks before the list; the regional
   network's analysers are the reference between rounds), the node export, the register and the provisional release.
2. Convert the analysers' micrograms to ppb (1.996 at 20 degrees C), put both on UTC (the network's hora is the hour
   ending, UTC+1), keep each node's accepted hourly readings (OZN-B half-hours averaged into hours) in 6 April to 31 May
   2028 local time.
3. Pair each node's hours with its nearest analyser (the register's current site) and fit the node on the analyser by
   ordinary least squares; the slope is the span.
4. Pull every node whose slope lies outside 0.85 to 1.15.

Ends on: 16 nodes to the bench: OZ03, OZ06, OZ17, OZ21, OZ22, OZ23, OZ24, OZ25, OZ26, OZ27, OZ28, OZ30, OZ31, OZ32,
OZ35, OZ36 (eleven healthy heads far from an analyser added, and OZ29, OZ33 and OZ34, which read high, left off).
Golden: 8 nodes to the bench: OZ06, OZ17, OZ21, OZ25 and OZ32 reading low, OZ29, OZ33 and OZ34 reading high.

## Stump sentence

A competent analyst regresses each node's hourly ozone over the eight weeks on its nearest analyser and files 16 nodes
for the bench, eleven of them healthy heads far from any analyser and none of the three that read high, because a slope
fitted on paired hours between sites kilometres apart is pulled toward zero by how weakly the two sites agree hour by
hour; read from the spread of each node's hourly ozone against the regional analysers' spread over the same weeks, the
list is the 8 nodes of the golden.

## Three rules

Task type: sensor-calibration-measurement (Physical & Environmental Sciences), which serves Data Quality Monitoring.
Domain test: the deciding quantity is each node's span against true ozone at its inlet, which the low-cost sensor field estimates remotely against a reference network by matching a node's distribution over weeks to the reference's, because ozone is a regional pollutant whose background sites share a distribution while their hourly values part with distance.
Swap: "which of our 36 school canteens' tills go for recalibration, judged on each till's gain against the head office's four counting points" stops making sense: there is no regional field the sites share, no analyser kilometres away, no span of a gas-sensitive head.
Layer 1: the nodes' UTC and ppb against the network's hour-ending UTC+1 and micrograms at 20 degrees (both exports as written); OZN-B half-hour records (the hardware); records sent twice after link drops (the mobile buffer); OZ19B (the spare unit's temporary id, the maintenance log); firmware 4.2's renumbered status codes (the vendor); two nodes moved in March (the cleaning round); the network's provisional and validated releases. Nothing placed to be caught.
Layer 2: estimation_fit: a slope fitted on paired hours against a reference elsewhere is attenuated by the sites' partial hourly agreement (regression dilution with the error in the regressor); the span is read from the spreads.
Decisive step: reading each node's span from the spread of its hourly ozone against the regional analysers' spread over the window, not from a slope on paired hours against the nearest analyser.
Not semantics: every field, unit, clock and status read correctly still leaves the paired slope at 16 nodes; the step is an estimator for a filed quantity, not a reading of a field or a definition.
Not rule application: the plan files what the span is, the window and the band; nothing files how to read a span between rounds, so executing every stated rule still leaves the analyst choosing an estimator, and the natural one is wrong.
Analyst test: a strong analyst who reads every file correctly and pairs each node with its nearest analyser files 16 nodes, the default path's Ends on, because the slope is attenuated.
Estimand: QA plan v3 section 4: each node's span (the change in its reading for a unit change in true ozone at its inlet, as the bench measures it) over the eight weeks before the list is set (6 April to 31 May 2028), outside 0.85 to 1.15, every one of the 36 nodes; section 5 makes the four analysers the reference.
No decoy: nothing is planted; no memo, draft or figure argues for the paired slope; the analysers' releases are correct.
No certified replay: no published or certified span ships; the method is not recovered by reproducing figures, and the as-found bench results that would score it do not exist yet (the June round is the first).
Lesson: a slope between two instruments at different sites measures their hour-to-hour agreement as much as the instrument's gain; when only distant references exist, a gain is read from what the sites share, their distributions. No build on file teaches it (task241 compares a float with a reference on a conserved coordinate; task246 removes measurer offsets; task262 carries a reliability ratio).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 slope on paired hours, nearest analyser: 16 | the plan's reference sentence | the register's positions | yes, a calibration regression | none | no | no | readable |
| 1 slope on daily means: 19 | none | none | yes, the 24-hour comparison | none | no | no | readable |
| 2 ratio of means over the window: 7 | none | none | yes, a gain as a ratio | none | no | a ratio | readable |
| 3 slope on the four analysers' mean: 10 | none | none | yes, a regional reference | none | no | no | readable |
| 4 (decisive) span from the spreads against the regional analysers: 8 | none (the plan files the quantity, not the estimator) | none | no (the reflex is a regression) | none (no as-found corpus exists) | no | no | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | span | the change in reading per unit true ozone at the inlet (plan 4) | the slope on paired hours | 16 nodes, ruled out | plan 4 defines the quantity; the paired slope estimates agreement times span |
| SF2 | the eight weeks to 31 May | 6 April to 31 May, local | the same dates in UTC | same call | asserted |
| SF3 | outside 0.85 to 1.15 | strictly outside | edges included | same call | no node within 0.04 of an edge (asserted) |
| SF4 | the reference | the four analysers pooled | each node's nearest analyser | same call | asserted |
| SF5 | accepted in the window | status 0 or 1 (firmware 4.2) | status 0 only | same call | asserted |
| SF6 | micrograms to ppb | 1.996 (20 degrees, station sheet) | 1.962 (25 degrees) | same call | asserted |
| SF7 | records sent twice | the latest received | the first received | same call | identical values (asserted) |
| SF8 | OZN-B half-hours | averaged into hours | used as they are | same call | asserted |
| SF9 | reads high or low | above 1.15 high, below 0.85 low | none | converge | the band |
| SF10 | span against the as-left setting | the span itself (set to 1.00, plan 3) | span relative to 1.00 | same call | identical |

## Ladder

| Rung | Method | List | Wrong by |
|---|---|---|---|
| 0 | slope on paired hours against the nearest analyser | 16 | adds OZ03, OZ22, OZ23, OZ24, OZ26, OZ27, OZ28, OZ30, OZ31, OZ35, OZ36; drops OZ29, OZ33, OZ34 |
| 1 | slope on daily means | 19 | adds twelve far heads; drops OZ33 |
| 2 | ratio of the window's means | 7 | adds OZ09, OZ13 (zero drift); drops OZ21, OZ25, OZ34 |
| 3 | slope on the four analysers' mean | 10 | adds OZ22, OZ26, OZ27; drops OZ29 |
| 4 | span from the spreads (golden) | 8 | none |

Separation: every rung names a different list; the decisive rung reverses the walk (rungs 0, 1 and 3 drop the heads
reading high, rung 4 restores them). Margins: the golden's spans sit at least 0.065 from a band edge; every spread
variant (nearest analyser, pooled, interquartile, 10th to 90th percentile, quantile line, daily means) and the orthogonal
fit file the golden with at least 0.049 to spare. The analysers themselves give paired slopes of 0.78 to 0.92 against
one another while their spreads agree within 0.03.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 36 nodes in the register, every one judged |
| 2 | Unit of account | one node (its current unit and head) |
| 3 | Attribution window | 6 April to 31 May 2028, local (plan 4, SF2) |
| 4 | As-of dating | 1 June 2028; node export and provisional release to 31 May 23:00 UTC |
| 5 | Version basis | plan v3; the provisional release for 2028, the validated release for 2027 (station sheet) |
| 6 | Denominator | the pooled analysers' spread (SF4) |
| 7 | Weighting | each hour once; OZN-B half-hours averaged (SF8) |
| 8 | Window length | eight weeks (plan 4) |
| 9 | Boundary inclusivity | strictly outside the band; no node near an edge (SF3) |
| 10 | Rounding path | spans unrounded before the band; hours and days whole |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every node reported through the window; none pending |
| 13 | Order of operations | dedup, ids, status, hours, window, spread, band |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | the latest received (SF7) |
| 16 | Identity normalisation | OZ19B is OZ19 (log); stations by code |
| 17 | Netting against gross | none |
| 18 | Dimensional units | ppb; micrograms over 1.996 (SF6) |
| 19 | Code and status semantics | firmware 4.2's codes from each node's date (release note, log); V, P, N flags |
| 20 | Integerisation | hours and days whole |
| 21 | Clause scope | plan 4 applies to every node; plan 6 to data capture |
| 22 | Forward window contents | the June round acts on the window's spans; heads drift about a per cent a month, under every margin |

## Literal reader

Executed word for word, plan 4 defines the span as a property of the head against true ozone at its inlet and plan 5
names the analysers as the reference; the only literal estimators of that property from distant references are those
that use what the sites share, and every one of them (spreads, quantiles, the orthogonal fit) files the golden list
(asserted). The paired slope is not a reading of plan 4 but an estimator of agreement times span.

## Oracles

none. No as-found bench result exists (the June round is the first recalibration); no published span or list ships.
The analysers' own inter-comparison confirms the shared distribution for a reader who looks, but scores no rule and ranks no node.

## Ask sheet

- Ask A, each node's hours with an accepted reading, 1 November 2027 to 31 January 2028 (36 figures). Use: the
  foundation's quarterly report on the network's first full winter quarter. Primary device D2 (an attribute at the wrong
  vintage): the dictionary lists the status codes the export carries now; before each node's firmware 4.2 date
  (maintenance log, 10 to 19 January) status 1 was the warm-up after a restart (the vendor's release note), so the
  dictionary's codes read over the whole quarter add 19 to 24 hours to every node. Hazards: OZ19B is OZ19's spare
  unit (D7, OZ19 alone, 377 hours if dropped); OZN-B half-hours (rows over-count 12 nodes, D6); records sent twice after
  the December link drop (D1); the quarter in local time against the export's UTC (D8, no count moves).
- Separation: no device row sits in the window: no OZ19B record after 25 January, every node on 4.2 before 6 April
  (asserted S1, S2); the firmware device is read only by the quarter.

| Ask | Cracker's path (lands the call) | Cracker's figures | Mirror (paired slope, same habits) | Cracker |
|---|---|---|---|---|
| A, 36 hours | the dictionary's codes over the quarter, OZ19B joined, distinct local hours | every node 19 to 24 high, 0 of 36 | 0 of 36 | misses |

- Measured by: task249/generator/pair.py on the cut pack
- Pair ceiling: 28.3
- Mirror leakage: 0.0 per cent of ask weight
- If the cracker also reads the release note: 55.8; if neither response lands the call and both read it: 66.6. The ask is one device deep, so the bar then rests on the call.

## Pre-ship check

1. Domain: the call stands on each node's span against true ozone at its inlet, read the way the low-cost sensor field
   reads a node remotely against a reference network (the node's distribution over weeks against the regional
   analysers'), because ozone is a regional pollutant whose background sites share a distribution while their hourly
   values part with distance; with another field's nouns there is no regional field, no analyser kilometres away and
   no span drift of a gas-sensitive head, so the task stops making sense.
2. Two layers: Layer 1 (UTC and ppb against hour-ending UTC+1 and micrograms, OZN-B half-hours, records sent twice,
   OZ19B, firmware 4.2's codes, the March moves, the two releases) is neutral on the call (SF2, SF4 to SF8, S1, S2).
   Layer 2 is the estimator: asserted on the clean truth, the paired slope files a wrong list and the spread alone
   files the golden (R3a, R3b).
3. No banned stump decides: nothing is planted (no memo, figure or ranking argues for the paired slope); not semantics
   (every field read right, the paired slope still files 16); not rule application (the plan files the span, the
   window and the band, and no estimator).
4. Analyst test: the default path's 16 nodes, executed on the clean truth (R3a).
5. Estimand: plan v3 sections 4 and 5; the literal reader's estimators all file the golden (asserted).
6. No decoy memo, draft or briefing: none ships.
7. No certified replay: no span, list or as-found result ships to reproduce.
8. Lesson: not on file (task241, task246, task262 differ, card differentiation).

## Architecture 2 (in design)

The world, the decision and the quantity stay (the June pull list on each node's span against the band); the decisive
step moves from a statistical correction any strong model makes (the attenuated paired slope) to the field's own
physics of the comparison. At night a stable surface layer forms and ozone near the ground is lost to deposition and
titration; the regional network's four analysers and most nodes sit on the plain, but the nodes on the hill villages
stand above the night's surface layer and keep their ozone, so their hourly distribution is narrower than the plain's
for reasons that are not the head's. Every comparison over all hours, whether the paired slope, an errors-in-variables
slope or the spreads, reads a healthy hill node as low and a hill node drifted high as healthy; only a comparison
restricted to the hours of the well-mixed afternoon, when the comarca shares one ozone, reads every node's span.
Rungs: paired slope over all hours; errors-in-variables or spreads over all hours (the reader's route); the afternoon
comparison (decisive), asserted across afternoon windows (C3). The register carries each site's altitude; nothing filed
names the afternoon or the surface layer. Ask: each analyser's 2027 days over 120 micrograms comes back with a silent D3
device (the validated release written dd/mm/yyyy by the validation system, the provisional release in ISO time),
beside the node quarter's firmware vintage; the reader's realism tells fixed in the generator.

Measured on the cut pack (generator state of 2026-10-18, field seed 268, night loss with hill exposure 0.68 to 0.75,
afternoon mixing): golden, spreads on the hours starting 12:00 to 17:00 local against the four analysers' pooled
hours, files OZ06, OZ17, OZ21, OZ25, OZ32 (low) and OZ29, OZ33, OZ34 (high), 0.079 from the nearest edge; the nearest
analyser (0.055), the 10th to 90th percentiles (0.083), the quantile line (0.090), the interquartile range (0.042) and
the windows 11 to 17, 13 to 17 and 12 to 16 (0.074 to 0.099) file the same list. All-hours routes: spreads 9 nodes
(adds OZ22, OZ31, OZ36, drops OZ33, OZ34), orthogonal fit 10, paired slope 9 (adds OZ22, OZ31, OZ35, OZ36, drops OZ29,
OZ33, OZ34), daily spreads 10, slope on the four analysers' mean 10, ratio of means 8 (OZ13 and OZ35 for OZ21 and OZ25).

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
