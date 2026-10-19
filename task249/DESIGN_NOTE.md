# task249 design note

## Draw

Card `cards/task249.json`, architecture 2 (v1 in lineage), re-registered 2026-10-19 with `--force` on the author's
decision. The draw passed the guard when it was filed at 18:53 on 18 October; task268's re-registration at 23:10 moved
it after this card, so task247 (physical-environmental-sciences with data-quality-monitoring) slid into the last three
and `check` gave ban.pairing BLOCK. Sensor calibration has no other honest client domain, and against task247 the task
type, the world and the decisive step all differ (card notes and differentiation). Verdict after filing: WARN. Each
WARN, answered: overuse.objective (Data Quality Monitoring in 4 of the last 12): the lane is Data Quality Monitoring &
Alerting. repeat.gate_g and overuse.gate_g (method_or_model_selection after task268): the decisive step is which hours
read a filed span, a method choice, and no other key is true of it. repeat.question_form (which, after task268): the
call is a set of nodes. Nearest driver 0.30 is this slot's own v1 (lineage, differentiated); the next is 0.08 (task121
v3).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring. The object is the health of a low-cost ozone network's data, how far each node's span has drifted from
  true ozone since the heads were set at installation, and the call is a monitoring decision: which nodes go on the
  pull list for recalibration at the June 2028 round, before the summer ozone season.
- **The seed, re-found.** DQ22 gave the world (a low-cost sensor network serviced in rounds), the decision (the pull
  list for the next maintenance round) and the quantity (each sensor's drift against a tolerance). Its pitfall (the
  direction of the calibration regression at a collocation) belongs to a sensor sitting beside its reference; here no
  node sits beside one, and the decisive step is which hours read a node's span against analysers kilometres away.
- **Niche.** A public research foundation in the Spanish interior runs 36 low-cost ozone nodes (gas-sensitive
  semiconductor heads) on school and municipal roofs across a comarca, the towns on a plain at 676 to 731 m and four
  hill villages at 905 to 962 m, beside the regional government's four reference analysers (UV photometry) on the
  plain. The heads were set against a reference at installation in autumn 2027; their span drifts over months. At each
  round the contractor pulls the listed nodes, takes them to a reference station for a week, and resets them.
- **The call.** Which nodes go on the pull list for the June 2028 round, judged on each node's span over the eight
  weeks to 31 May 2028 against the quality plan's band of 0.85 to 1.15.
- **Shape.** 10, a scorecard: each of the 36 nodes against the band, the list, the count, each listed node's
  direction, and the ask; over 25 criteria. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** other, named in the card's notes. G16 decisive (which estimator of a filed span); gap population (an
  analyser's hourly series is the node's air only when the boundary layer mixes them); Gate G method_or_model_selection;
  calibration none; context artifact filed_standard (the network's quality plan); Layer 2 family field_method, pattern
  own:remote-span-on-the-mixed-afternoon-not-all-hours.
- **Forum, event, organisation.** operations_desk (the network coordinator sends the list to the maintenance
  contractor), season_or_peak (the June round is the last before the summer ozone season), research_or_statistics_office
  (a public research foundation). Role field_unit_lead (the network coordinator).
- **People** (`guard.py names --geo Spain --seed 249`, locale es_ES): Matilde Criado, the network coordinator, who
  asks; Adán Ruano, the contractor's field technician; Edelmira Urrutia, the regional network's data officer; Paulino
  Cardona, the centre's sensor scientist. None appears in the prompt.
- **Data-native sentence.** At night a stable surface layer forms over the comarca's plain and the ozone near the
  ground is lost to deposition and titration, while the hill villages 170 to 270 m higher stand above that layer and
  keep their ozone; so over all hours a hill node's readings spread less than the plain's analysers' for reasons that
  are not its head's, and only in the convective afternoon, when the boundary layer mixes the comarca into one air
  mass, do a node and the analysers see the same ozone.
- **As-of.** Thursday 1 June 2028, after the export of 31 May and before the round of 12 June.
- **Sources.** The client's two-layer standard (field_method); the low-cost sensor literature's remote calibration of
  dense networks (a node's distribution over weeks matched to a regulatory station's), with the practice of comparing
  sites on the well-mixed afternoon hours when their exposures differ; the boundary-layer chemistry of nocturnal ozone
  loss under the stable layer, which elevated sites escape. No build on file restricts a comparison to the hours a daily
  process mixes the medium: task121 v3 compares a unit's exposure at the same clock hours against a valley's wind,
  task241 compares a float with a reference on a conserved coordinate, task246 removes measurer offsets.

## Default path

1. Read the quality plan (span against the band 0.85 to 1.15 over the eight weeks before the list; the regional
   network's four analysers are the reference between rounds), the node export, the register and the provisional
   release.
2. Convert the analysers' micrograms to ppb (1.996 at 20 degrees C), put both on UTC (the network's hora is the hour
   ending, UTC+1), keep each node's accepted hourly readings (OZN-B half-hours averaged into hours) over 6 April to 31
   May 2028 local time.
3. See that a slope on paired hours against an analyser kilometres away is pulled toward zero by the sites' partial
   hourly agreement (the analysers' own paired slopes run 0.885 to 0.954 while their spreads agree within 0.005), so
   read each node's span as the standard deviation of its hourly ozone over the window against the four analysers'
   pooled hours, or by an errors-in-variables slope.
4. Pull every node outside 0.85 to 1.15.

Ends on: 9 nodes to the bench: OZ06, OZ17, OZ21, OZ22, OZ25, OZ29, OZ31, OZ32, OZ36 (the healthy hill nodes OZ22, OZ31
and OZ36 added, and OZ33 and OZ34, which read high, left off).
Golden: 8 nodes to the bench: OZ06, OZ17, OZ21, OZ25 and OZ32 reading low, OZ29, OZ33 and OZ34 reading high.

## Stump sentence

A strong analyst who corrects the paired slope's attenuation and reads each node's span from the spread of its hourly
ozone against the four analysers over every hour of the eight weeks files 9 nodes for the bench, the healthy hill nodes
OZ22, OZ31 and OZ36 among them and OZ33 and OZ34, which read high, left off, because at night the hill villages stand
above the surface layer where the plain loses its ozone, so their hourly spread is narrower for reasons that are not
the head's; read on the afternoon hours of the mixed boundary layer, the list is the golden 8.

## Three rules

Task type: sensor-calibration-measurement (Physical & Environmental Sciences), which serves Data Quality Monitoring.
Domain test: the deciding quantity is each node's span against true ozone at its inlet, read remotely against a reference network the way the field reads it, on the hours of the well-mixed afternoon boundary layer, because at night elevated sites stand above the surface layer that strips the plain's ozone.
Swap: "which of our 36 school canteens' tills go for recalibration, judged on each till's gain against the head office's four counting points" stops making sense: there is no boundary layer mixing the sites by afternoon, no night stripping the plain and sparing the hills, no span of a gas-sensitive head.
Layer 1: the nodes' UTC and ppb against the network's hour-ending UTC+1 and micrograms at 20 degrees (both exports as written); OZN-B half-hour records (the hardware); records sent twice after link drops (the mobile buffer); OZ19B (the spare unit's temporary id); firmware 4.2's status codes and the restart clocks (the vendor's firmware); two nodes moved in March (the cleaning round); the register's altitudes; the network's provisional and validated releases. Nothing placed to be caught.
Layer 2: field_method: ozone's nocturnal loss under the stable surface layer, which elevated sites escape, makes every all-hours comparison misread the hill nodes; the comparison is restricted to the convective afternoon, when the comarca shares one ozone.
Decisive step: reading each node's span on the hours of the mixed afternoon boundary layer (hours starting 12:00 to 17:00 local) against the analysers' same hours, not over every hour of the window.
Not semantics: every field, unit, clock and status read correctly and the paired slope's attenuation corrected still leave the all-hours spreads at 9 nodes; the step is which hours carry the comparison, which no field, code or definition fixes.
Not rule application: the plan files the span, the window, the band and the reference; nothing files which hours read a span between rounds, so executing every stated rule still leaves the analyst choosing the comparison's hours, and every reflex (all hours, daily means, the window's means) is wrong.
Analyst test: a strong analyst who reads every file correctly and corrects the paired slope's attenuation over all hours files 9 nodes, the default path's Ends on, executed on the clean truth in checks.py (R3a, R3b).
Estimand: QA plan v3 section 4: each node's span (the change in its reading for a unit change in true ozone at its inlet, as a bench week measures it) over the eight weeks before the list is set (6 April to 31 May 2028), outside 0.85 to 1.15, every one of the 36 nodes; section 5 makes the four analysers the reference.
No decoy: nothing is planted; no memo, draft or figure argues for an all-hours comparison, the analysers' releases are correct and the register's altitudes are the sites'.
No certified replay: no published or certified span ships; the method is not recovered by reproducing figures, and no as-found bench result exists (the June round is the first).
Lesson: a remote reference shares a site's air only when the boundary layer mixes it, so an instrument compared with a distant reference over all hours is read through the sites' night-time difference as much as through its own gain. No build on file teaches it (task121 v3 compares clock hours against a valley's wind; task241 compares on a conserved coordinate; task246 removes measurer offsets).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 slope on paired hours, nearest analyser, all hours: 9 | the plan's reference sentence | the register's positions | yes, a calibration regression | none | no | no | readable |
| 1 spreads or errors-in-variables over all hours: 9 to 10 | none | none | yes, the attenuation correction a strong model makes | none | no | a ratio of spreads | readable |
| 2 slope or spreads on daily means: 15 or 10 | none | none | yes, the 24-hour comparison | none | no | no | readable |
| 3 ratio of the window's means: 8, the wrong ones | none | none | yes, a gain as a ratio | none | no | a ratio | readable |
| 4 (decisive) afternoon hours, spreads against the pooled analysers: 8 | none (nothing filed names the afternoon or the surface layer) | none (the altitudes describe sites; no column marks hours) | no (the reflex keeps every hour) | none (no as-found corpus exists) | no | no | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | span | the change in reading per unit change in true ozone at the inlet (plan 4) | the node's mean over the analysers' mean | 8 nodes, OZ13 and OZ35 for OZ21 and OZ25 | plan 4: a change per unit change, and a node's zero is not a reason to take it down |
| SF2 | the eight weeks to 31 May | 6 April to 31 May, local | the same dates in UTC | same call | asserted |
| SF3 | outside 0.85 to 1.15 | strictly outside | edges included | same call | no node within 0.04 of an edge (asserted) |
| SF4 | the reference | the four analysers pooled | each node's nearest analyser | same call | asserted |
| SF5 | accepted in the window | status 0 or 1 (firmware 4.2) | status 0 only | same call | asserted |
| SF6 | micrograms to ppb | 1.996 (20 degrees, station sheet) | 1.962 (25 degrees) | same call | asserted |
| SF7 | records sent twice | the latest received | the first received | same call | identical values (asserted) |
| SF8 | OZN-B half-hours | averaged into hours | used as they are | same call | asserted |
| SF9 | reads high or low | above 1.15 high, below 0.85 low | none | converge | the band |
| SF10 | span against the as-left setting | the span itself (set to 1.00, plan 3) | span relative to 1.00 | same call | identical |
| SF11 | the afternoon's hours | starts 12:00 to 17:00 local | an hour either way (11 to 17, 13 to 17, 12 to 16, 11 to 18) | same call | asserted |

## Ladder

| Rung | Method | List | Wrong by |
|---|---|---|---|
| 0 | slope on paired hours against the nearest analyser, all hours | 9 | adds OZ22, OZ31, OZ35, OZ36; drops OZ29, OZ33, OZ34 |
| 1 | spreads against the pooled or nearest analysers, all hours | 9 | adds OZ22, OZ31, OZ36; drops OZ33, OZ34 |
| 1 | errors-in-variables slope, interquartile or 10th to 90th ranges, quantile line, all hours | 10 | adds OZ22, OZ31, OZ35, OZ36; drops OZ33, OZ34 |
| 2 | slope on daily means | 15 | adds OZ01, OZ08, OZ22, OZ23, OZ27, OZ28, OZ30, OZ31, OZ35, OZ36; drops OZ29, OZ33, OZ34 |
| 2 | spreads of daily means | 10 | adds OZ31, OZ36 |
| 3 | ratio of the window's means | 8 | adds OZ13, OZ35; drops OZ21, OZ25 |
| 3 | slope on paired afternoon hours | 9 | adds OZ26, OZ28; drops OZ33 (still attenuated) |
| 4 | afternoon spreads against the pooled analysers (golden) | 8 | none |

Separation: every rung names a different list, and the decisive rung reverses the walk: every all-hours rung keeps
OZ33 and OZ34 (high) off and adds healthy hill nodes; the afternoon restores them. Measured on the cut pack: over all
hours the hill nodes read OZ22 0.797, OZ31 0.820, OZ36 0.835 (healthy, read low) and OZ33 1.068, OZ34 1.060 (high,
read healthy); on the afternoon 0.988, 0.970, 0.995 and 1.293, 1.331. The golden's spans sit 0.079 or more from a band
edge; every afternoon variant files it (nearest analyser 0.055, interquartile 0.042, 10th to 90th 0.083, quantile line
0.090, errors-in-variables 0.056, daily afternoon means 0.086), and so do the windows 11 to 17, 13 to 17, 12 to 16 and
11 to 18 (SF11).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 36 nodes in the register, every one judged |
| 2 | Unit of account | one node (its current unit and head) |
| 3 | Attribution window | 6 April to 31 May 2028, local (plan 4, SF2) |
| 4 | As-of dating | 1 June 2028; node export and provisional release to 31 May 23:00 UTC |
| 5 | Version basis | plan v3; the provisional release for 2028 (plan 5) |
| 6 | Denominator | the pooled analysers' spread over the same afternoon hours (SF4, SF11) |
| 7 | Weighting | each hour once; OZN-B half-hours averaged (SF8) |
| 8 | Window length | eight weeks (plan 4) |
| 9 | Boundary inclusivity | strictly outside the band; no node near an edge (SF3) |
| 10 | Rounding path | spans unrounded before the band; hours whole |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every node reported through the window; none pending |
| 13 | Order of operations | restart clocks placed, duplicates, ids, status, hours, window, afternoon, spread, band |
| 14 | Row order | no step depends on file order (the export is in arrival order) |
| 15 | Duplicate resolution | the latest received (SF7) |
| 16 | Identity normalisation | OZ19B is OZ19 (log); stations by code |
| 17 | Netting against gross | none |
| 18 | Dimensional units | ppb; micrograms over 1.996 (SF6) |
| 19 | Code and status semantics | in the window every node is on 4.2 (S2): status 0 or 1 accepted (SF5); V, P, N flags |
| 20 | Integerisation | hours whole |
| 21 | Clause scope | plan 4 applies to every node; plan 6 to data capture |
| 22 | Forward window contents | the June round acts on the window's spans; heads drift about a per cent a month, under every margin |

## Literal reader

Executed word for word, plan 4 files the span as the head's response to true ozone at its inlet, as a bench week
measures it, and plan 5 names the analysers as the reference between rounds; neither names the hours. The analysers
read a node's inlet ozone only when the node's air and theirs are one, which the records show for the afternoon (the
plain nodes' and the analysers' afternoon distributions agree) and not for the night at the hill villages. Every
comparison restricted to the mixed afternoon (spreads pooled or nearest, quantile ranges, the quantile line, the
errors-in-variables slope, daily afternoon means; windows 11 to 17 up to 13 to 17) files the golden list (C2, C3,
asserted); a comparison over all hours measures the hill sites' night as much as the heads. The ask's quarter is filed
in local time (plan 6) and a stamp as the start of the record's interval in UTC (plan 2).

## Oracles

none. No as-found bench result exists (the June round is the first recalibration); no published span or list ships.
The analysers' own inter-comparison confirms their shared distribution for a reader who looks, but scores no rule and
ranks no node.

## Ask sheet

- Ask A, each node's hours with an accepted reading, 1 November 2027 to 31 January 2028 (36 figures, whole hours).
  H18: the foundation's quarterly report on the network's first full winter quarter, a measure every node carries
  that the call does not turn on; the call reads no record before 6 April. Two primaries, each moving all 36 figures
  alone:
  - D2 (a label stored before a silent switch): the dictionary and the firmware note give 4.2's status codes; before
    each node's update (maintenance log, 10 to 19 January, 10:00 local; OZ19 from the spare's start on 9 January) the
    node ran 3.7, whose status 1 was the warm-up after a restart. Nothing marks a record's firmware; the records show
    it (before the update every status-1 record sits in the two hours after a restart, the Sunday 03:00 one or the
    storm's 19:00 on 27 November, reading low; from it status 1 falls in humid hours and the warm-ups are status 2),
    and the note says humidity compensation came with 4.2. 4.2's codes over the whole quarter: +18 to +24 at every
    node (A1).
  - D8 (a clock): after any restart but the weekly one a node's clock counts from 2000-01-01 until the Sunday 03:00
    restart sets it, so the records after each node's update, after the storm (nine nodes) and after the spare's start
    are stamped in 2000. The quarter's filter drops them silently and the reflex repair (dropping impossible stamps)
    drops them too: -15 to -164 at every node (A6). A stamp is the start of the interval in UTC (plan 2) and a record
    arrives minutes after its interval ends, so the received time places each one, the same placement the log's
    restarts give (A8).
  Hazards: OZ19B is OZ19's spare (D7, OZ19 alone, -377 if dropped); OZN-B half-hours (rows counted: +1,506 to +2,172
  at the 12 OZN-B nodes, D6); records sent twice after the December link drop (D1); the quarter in local time against
  the export's UTC (D8, no count moves); the storm's and the update's restart episodes share stamps in 2000 at the nine
  storm nodes, so deduplicating before placing them loses the storm's hours.
- Separation: no device row sits in the window: every record stamped from a restart clock arrived before 6 April (S3),
  no OZ19B record after 25 January, every node on 4.2 before 6 April (S1, S2); the call computes the same with every
  ask device met or missed.

| Ask | Cracker's path (lands the call) | Cracker's figures | Mirror (all-hours spreads, same habits) | Cracker |
|---|---|---|---|---|
| A, 36 hours | the dictionary's codes over the quarter, records at their stamps (the quarter's filter drops those stamped in 2000), OZ19B joined, distinct local hours | -146 to +5, 0 of 36 | 0 of 36 | misses |

- Stops measured: the firmware met with the stamps as written keeps 0 of 36; the stamps placed with the dictionary's
  codes keeps 0 of 36; rows counted keeps 0 of 36; the orphan dropped keeps 0 of 36.
- Measured by: task249/generator/pair.py on the cut pack
- Pair ceiling: 28.3
- Mirror leakage: 0.0 per cent of ask weight
- If the cracker meets both primaries: 55.8; if neither response lands the call and both meet both: 66.6. Each primary
  alone keeps 0 of 36, so a response banks the ask only by meeting both.

## Pre-ship check

1. Domain: the call stands on each node's span against true ozone at its inlet, read the way the field reads a node
   remotely against a reference network, on the afternoon hours of the mixed boundary layer, because at night the
   hill villages stand above the surface layer that strips the plain's ozone; with another field's nouns there is no
   boundary layer, no nocturnal ozone loss and no span drift of a gas-sensitive head, so the task stops making sense.
2. Two layers: Layer 1 (UTC and ppb against hour-ending UTC+1 and micrograms, OZN-B half-hours, records sent twice,
   OZ19B, firmware 4.2's codes, the restart clocks, the March moves, the altitudes, the two releases) is neutral on the
   call (SF2, SF4 to SF8, S1 to S3). Layer 2 is the comparison's hours: asserted on the clean truth, the all-hours
   spreads file a wrong list and the afternoon alone files the golden (R3a, R3b).
3. No banned stump decides: nothing is planted (no memo, figure or ranking argues for all hours); not semantics (every
   field read right, the all-hours spreads still file 9); not rule application (the plan files the span, window, band
   and reference, and no hours).
4. Analyst test: the default path's 9 nodes, executed on the clean truth (R3a, R3b).
5. Estimand: plan v3 sections 4 and 5; every afternoon variant files the golden (C2, C3, SF11).
6. No decoy memo, draft or briefing: none ships.
7. No certified replay: no span, list or as-found result ships to reproduce.
8. Lesson: not on file (task121 v3, task241, task246 differ; card differentiation).

## Leak check

leak.py (as-of 2028-06-01): REVIEW, no LEAK; file names, author vocabulary, announcements, ranking artifacts, hidden
content, column names, dates and the prompt gate clean. Each REVIEW line, answered:

- The QA plan carries 0.85 and 1.15 and the words of the call (nodes, bench, June round): the band and the round are
  the filed estimand, stated once at authority; no document names a node on the list.
- The maintenance log carries the call's words (nodes, bench, round): the log of installation, events and the
  firmware rollout; it names no node's span and no list.
- Design-note vocabulary in the documents (network, analysers, firmware, records, comparison, method, comarca): the
  domain's own words. No document names the afternoon, the surface layer, the boundary layer, the night's ozone loss or
  the hill villages' exposure; the QA plan's night-time readings are the zero's re-setting, a fact of practice, and the
  station sheet's comparison is the old analyser's parallel run. The restart in the log, the release note and the
  dictionary is the warm-up's cause, and no document mentions a node's clock.

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
