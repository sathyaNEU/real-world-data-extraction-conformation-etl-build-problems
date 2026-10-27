# task307 design note

## Draw

- **Number and objective.** task307, Opportunity Sizing & Decision Support, architecture 1. The seed (OS09, a
  mini-split rebate programme's net savings) was left at the draw: every honest label for its decisive step
  (a comparison-group design, a population read, a decomposition of gross into net) was held by the guard
  window, and its furniture (a utility's filing with its regulator) was barred. Under the author's rule that a
  stuck build is unblocked rather than parked, the build moved to another client domain and dataset.
- **Pairing.** Urban & Regional Science, task type `optimization` (OS): which road project in a metropolitan
  planning organisation's 2028 Transportation Improvement Program takes its one congestion-relief slot, sized
  by the vehicle-hours a year it saves across the whole network.
- **World.** Merrimont, a fictional river metro in the United States, split by the Ashkettle River; the
  west bank's suburbs reach the east bank's downtown over three crossings (the Route 9 freeway bridge, the
  Center Street Bridge and the Southport Bridge). The Merrimont Area Metropolitan Planning Organization
  (MAMPO) runs the regional travel demand model. Personas drawn with `guard.py names --geo US --seed 307`:
  Krystal Cooke (travel demand modelling lead), Charles Cummings (executive director).
- **Decision and quantity.** Four candidate projects (the Route 9 widening on the west bank, the Ferry Street
  exit ramp, a lane each way on the Center Street Bridge, the Southport Avenue signal and turn-lane package);
  the call is the project that saves the most vehicle-hours in 2028's AM and PM peak hours across the
  network, with the annual hours each saves and the hours saved per million dollars.
- **Default path (written first).** Take the regional model's 2028 no-build loaded network, apply each
  project's capacity change to its own links, price the time saved on those links at the no-build volumes
  through the documented volume-delay functions, annualise and fund the largest: the Route 9 widening, whose
  segment carries the most vehicles at the worst volume to capacity ratio. Ends on: the Route 9 widening.
  Once trips re-route, the widened segment feeds the Route 9 bridge downstream, which binds, and the Center
  Street Bridge lane pulls trips off Route 9: the prototype keeps about four fifths of the widening's
  link-level saving and puts the Center Street lane about a third ahead.
- **Stump sentence.** A competent solver prices each project on its own links at the no-build volumes and
  funds the Route 9 widening; the step that lands it there is holding every trip on its no-build route, when
  trips re-route once a project opens and the widened freeway feeds the downstream crossing that binds.
- **Data-native sentence.** The trip table and the volume-delay functions are the network's own record, and
  re-assigning the 2028 trip table to equilibrium on each build network is the only way the record says where
  the traffic goes once a project opens.
- **Candidates written before this one (each with its default path and screen):**
  1. OS09 spillover by installers against their pre-registration baseline: the default (registered
     installers' unrebated sales as spillover) ends wrong, but the honest label is a comparison-group design,
     held by the window (task271).
  2. OS09 claims-lag completion of this year's rebated volume: a reflex chain-ladder completion; dead on the
     readability screen.
  3. Resource adequacy for a generation cooperative, forced outages conditioned on the cold that sets the
     heating peak: prototyped (the plan near the criterion on all-hours rates, near 190 MW short on
     temperature-conditioned rates, the tolling unit credited at about 60 MW not 97); task308's architecture
     3 registered the same world and driver first, so it is task308's.
  4. Screening yield by time since the last screen (a mobile screening unit across four districts): the
     decision frame and the yield-by-elapsed-time driver echo task301; dropped.
  5. Network equilibrium (this draw): no build on file assigns a trip table; `guard.py slots` on the
     mechanism (wardrop, equilibrium, assignment, rerouting, braess) and on the setting (traffic, congestion,
     route, link) returned no screen of it.

- **Guard at registration (2026-10-27, WARN).** `overuse.org_family` (government_agency in 40 builds): an
  MPO is a government agency, and the honest label stays. `repeat.decision` and `repeat.question_form`
  against task308 v3: the call is a pick among four projects, so it asks which. Differentiation filed
  against task158 (`test.same_puzzle_older`).

## Default path

The route a capable analyst takes with every file read and every filed rule executed:

1. Reads the subarea extract's two-way link records and Table 4.2, and takes the 2028 no-build volumes and times from
   MAMPO_v42_loaded_network_2028NB.csv, which reproduce the model's no-build vehicle-hours (2,682.0 AM, 2,206.4 PM).
2. Codes each candidate's capacity change from the Model coding sheet onto its own links and re-times those links
   through their volume-delay functions at the loaded no-build volumes, AM and PM.
3. Sums the time saved on the changed links, annualises it as guidance 2.2 sets out (times 247 times 2.9) and divides by
   each year-of-expenditure cost: Route 9 about 196,500 vehicle-hours a year (4,200 per million), Center Street
   95,700, Southport 93,200, Ferry Street 53,200.
4. Awards the largest annual benefit (guidance 3.1).

Ends on: the Route 9 Millbrook auxiliary lane (TIP-28-014), about 196,500 vehicle-hours a year.
Golden: the Center Street Bridge widening (TIP-28-009), 323,000 vehicle-hours a year (8,300 per million); Route 9
159,000 once trips re-route.

## Stump sentence

A competent solver prices each project on its own links at the regional model's no-build volumes and funds the Route 9
widening; the step that lands it there is holding every trip on its no-build route, when trips re-route once a project
opens, the widened segment feeds the Route 9 bridge that binds downstream, and the Center Street Bridge lane pulls trips
off Route 9.

Data-native sentence (as at the draw): the trip table and the volume-delay functions are the network's own record, and
re-assigning the 2028 trip table to equilibrium on each build network is the only way the record says where the traffic
goes once a project opens.

## Three rules

Task type: urban-regional-science / optimization (OS): one capital slot among four network improvements, sized by the
vehicle-hours each saves across the network.
Domain test: the deciding quantity is the change in the region's peak-hour vehicle-hours when a project opens, which
transport planning estimates by assigning the trip table to user equilibrium over volume-delay functions on the build
network; where traffic goes once a link widens (Wardrop's route choice, a downstream bottleneck that binds) is the
field's own question.
Swap: "fund the hospital ward whose extra beds save the most patient-hours" keeps the words and loses route choice,
link capacities and an equilibrium in which every trip's route depends on every other trip's; no field outside network
planning prices an added lane by re-solving where everyone travels.
Layer 1: two-way link records with lanes per direction, zones numbered with gaps, subzone trip tables loaded through
connectors, a loaded network file at model precision, a coding sheet beside the sponsors' descriptions, counts by hour
ending in local time with 23 and 25 hour days, a replaced station number, NR and EST hours, counters carrying a missed
poll, model volumes in passenger-car equivalents. Each is what a travel model, a count program and a probe vendor produce; none
moves the call (SF1 to SF16 asserted).
Layer 2: network equilibrium: the build network's vehicle-hours come from re-assigning the same trips to their own
equilibrium routes, so a capacity change moves traffic on links the project never touches.
Decisive step: re-assigning the 2028 trip table to user equilibrium on each build network instead of re-timing the
project's own links at the no-build volumes, which credits the Route 9 lane with traffic that, once trips re-route,
queues at the Route 9 bridge, and misses the trips the Center Street lane draws off Route 9.
Not semantics: every field, unit and code can be read right (FTYPE 12's bridge curve, lanes per direction, vehicles
against passenger-car equivalents) and the project links still be re-timed at fixed volumes, filing Route 9; the step is
whether traffic moves, which no field states.
Not rule application: guidance 2.1 files the estimand (the reduction in the region's peak-hour vehicle-hours with the
project open, from the model on the coded network) and the documentation files the model's assignment as its general
method; neither says that the loaded no-build volumes do not stand for the build network, and the fixed-volume route
uses the same model's volume-delay functions on the same coded network; the route family spans Route 9 at about 196,500
(fixed volumes, one all-or-nothing re-route) to Center Street at 323,000 (equilibrium, any convergence from three
Frank-Wolfe iterations to a gap of 1e-12, either peak alone), so what decides is whether the solver re-solves the
network.
Analyst test: a strong analyst who reads every record and rule correctly re-times each project's links at the loaded
no-build volumes through Table 4.2 and funds the Route 9 widening at about 196,500 vehicle-hours a year; the golden
re-assigns the trips on each build network and funds the Center Street Bridge widening at 323,000 (Route 9 159,000).
Estimand: guidance 2.1 to 2.3 files the population (the region's 2028 AM and PM peak-hour trips as the tables give
them), the outcome (total vehicle-hours on the network), the comparison (the opening-year no-build network against the
network with the project coded in), the window (the two peak hours, annualised by 247 times 2.9) and the unit
(vehicle-hours a year, and per million dollars of year-of-expenditure cost); the award rule is guidance 3.1.
No decoy: nothing is planted: the loaded network file is the model's true no-build output and is used by the golden's
no-build run as well; no memo, sponsor figure or draft ranks the candidates.
No certified replay: no certified or published figure is reproduced to recover a hidden method; the guidance states the
estimand and the trip tables and network carry the evidence.
Lesson: a capacity improvement saves what the network saves once every trip re-settles, which is not what its own link
saves at today's loads; widening the segment in front of a bottleneck moves the queue downstream.

## Readability screen

| Rung | Test 1 (a filed sentence names it) | Test 2 (a file or column names it) | Test 3 (the field's reflex reaches it) | Verdict |
|---|---|---|---|---|
| R1 the network's capacities and volume-delay functions | documentation 4.1, 5.1, Table 4.2 | yes | yes | readable |
| R2 the no-build vehicle-hours | the loaded network file | yes | yes | readable |
| R3 each candidate coded onto its links | the Model coding sheet | yes | yes | readable |
| R4 the trip table re-assigned on each build network (decisive) | no: guidance 2.1 says the benefit comes from the model on the coded network and the documentation that the model assigns to equilibrium; neither says the no-build loads do not hold on a build network | no: the only loaded network in the pack is the no-build one, and nothing names re-routing, a bottleneck or the Route 9 bridge | no for the sizing reflex: a loaded network and a volume-delay curve price a capacity change in one step | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the trips | vehicles, as the tables give them | passenger-car equivalents | same call | documentation 6.3; asserted |
| SF2 | the peak hours | AM plus PM | AM alone | same call | guidance 2.1, 2.2; asserted |
| SF3 | vehicle-hours on the network | links and connectors | links only | same call | connector time cancels; asserted |
| SF4 | convergence | relative gap below 0.000001 | exact, or ten times looser | same call | documentation 6.1; figures asserted at 1e-6 |
| SF5 | the no-build vehicle-hours | the model's no-build run | read from the loaded file | same call | within 0.1 vehicle-hours; asserted |
| SF6 | the Ferry Street project | exit and on-ramp (both directions) | exit only | same call | the coding sheet; asserted |
| SF7 | the Route 9 project | the lane-drop link 2 | Lakeview Road to Quarry Lane read long | same call | the coding sheet; asserted |
| SF8 | the Southport package | per-lane capacity both directions | one direction | same call | the coding sheet; asserted |
| SF9 | the annual factor | 247 times 2.9 | another common factor | same call | guidance 2.2; proportional |
| SF10 | FTYPE 12 capacity | the freeway's per lane with the bridge curve | the bridge's per lane | same call | Table 4.2; asserted |
| SF11 | the award rule | the largest annual benefit | the largest per million dollars | same call | guidance 3.1; asserted |
| SF12 | a zone as a way through | never | used | same call | one connector per zone; asserted |
| SF13 | subzone against macro-zone tables | the subzone tables | aggregated | same call | shared attachment nodes; asserted |
| SF14 | induced or suppressed trips | none | elastic demand | same call | guidance 2.1 |
| SF15 | the opening year | 2028 | another year | same call | the only tables in the pack; asserted |
| SF16 | the Route 9 section after widening | FTYPE 12 kept (the coding sheet changes lanes only) | recoded FTYPE 1 | same call | guidance 4 (the coding sheet is the record); asserted |

## Ladder

- R0 the project link carrying the most vehicles (the Route 9 lane drop, 4,105 in the AM peak hour against 3,800 of
  capacity): Route 9.
- R1 each project's own links re-timed at the loaded no-build volumes: Route 9, about 196,500 vehicle-hours a year
  against Center Street's 95,700 (the default path).
- R2 one all-or-nothing re-route on the build network at no-build times: Route 9 (asserted).
- R3 equilibrium, AM peak only: Center Street (the call lands; the figures do not).
- R4 equilibrium stopped early (Frank-Wolfe at 3, 10 or 50 iterations; MSA at 10 or 50): Center Street.
- Golden: equilibrium on each build network, AM and PM: Center Street 323,000, Route 9 159,000, Southport 126,000, Ferry
  Street 37,000. Center Street leads by 103 per cent.
- Cheap routes on the clean truth that land the call: any re-assignment to (near) equilibrium, which is the decisive
  step itself; and the screening heuristic of the worst volume to capacity ratio among the project links (the Center
  Street Bridge, 1.34 in the AM), which ranks congestion rather than sizing a benefit and carries no figure.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the region's 2028 AM and PM peak-hour trips in the subarea tables | filed (guidance 2.1, documentation 4.3) |
| 2 | Unit of account | vehicle-hours a year; vehicle-hours per USD 1 million | filed (guidance 2.2, 2.3) |
| 3 | Attribution window | the AM 7 to 8 and PM 5 to 6 peak hours of 2028 | filed (documentation 6.2) |
| 4 | As-of dating | the opening year 2028; counts for 2025 | filed |
| 5 | Version basis | TDM v4.2 and the TIP workbook's coding sheet | filed (guidance 4) |
| 6 | Denominator | year-of-expenditure cost in the Candidates sheet | filed (guidance 2.3) |
| 7 | Weighting | each vehicle trip once | filed (documentation 6.3); SF1 asserted |
| 8 | Window length | one peak hour each, annualised by 2.9 | filed (guidance 2.2) |
| 9 | Boundary inclusivity | counts by hour ending 8 and 18 | filed (manual 3.1, documentation 6.4) |
| 10 | Rounding path | unrounded vehicle-hours, rounded once at the stated unit | filed (the prompt) |
| 11 | Tie-break | none: Center Street leads by 103 per cent | asserted |
| 12 | Maturity and censoring | none | C1 |
| 13 | Order of operations | assign, difference, annualise, divide | filed (guidance 2.1 to 2.3) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | none in the call; the repeated autumn hour in the counts | filed (manual 3.1) |
| 16 | Identity normalisation | node numbers and LINK_ID shared across files; S-0103R continues S-0103 | filed (manual 3.3) |
| 17 | Netting against gross | no-build less build; connector time cancels | filed (guidance 2.1); SF3 asserted |
| 18 | Dimensional units | minutes, miles, miles an hour; vehicles against passenger-car equivalents | filed (documentation 4.1, 6.3) |
| 19 | Code and status semantics | FTYPE codes, count statuses | filed (Table 4.2, manual 3.2); never the stump |
| 20 | Integerisation | whole trips as given | C1 |
| 21 | Clause scope | guidance 2.1 to each candidate alone | filed |
| 22 | Forward window contents | the 2028 tables are the opening-year demand | filed (guidance 2.1); SF15 asserted |

## Literal reader

Executed word for word, guidance 2.1 asks for the reduction in the total vehicle-hours of the region's 2028 AM and PM
peak-hour trips with the project open, "taken from the current regional model, on the network the project is coded
into", and the documentation (6.1) says the model assigns each table to user equilibrium to a relative gap below
0.000001. Executed on the coded network, the model re-assigns the trips; a reading that re-times the project's links at
the no-build loads uses the model's curves but not the model's assignment of the coded network. Every member of the
convergence family from a gap of 1e-6 down to 1e-12 prints the same eight figures (SF4 asserted), and the call is Center
Street on every equilibrium route, either peak alone included.

## Oracles

The generator's clean truth (solve.py, the path solver on the macro-zone tables) and the pack's replay (pack.py, the
subzone tables read from the files) agree on every annual figure to 0.01 vehicle-hours; verify.py recomputes every graded
figure on its own code path (its own path equilibration, its own day and hour rules and its own fault detector for
the counts) with 0 failures; the routes, the fork rows and the ask devices are asserted in
checks.py.

## Ask sheet

**Ask A: each permanent count station's 2025 AADT and K-factor (16 figures, whole vehicles and three decimals).** H18:
the TIP application carries the design-hour volumes of the corridors the candidates touch, a measure every candidate
carries that the call does not read; the call reads none of the count files (asserted). Use: the count program's annual
table beside the ranking. Primary device, silent (D4 and D6): every station had one loop or detector-card fault in 2025,
a dead lane loop undercounting its direction by about that lane's share, or a crosstalking card overcounting it, from a
mid-day hour until the crew's repair; the hours stay status OK, and only the direction's share of the two-way traffic
against its usual share for that hour of the week, with the work order in the inventory's Maintenance 2025 sheet (which
gives the repair day, not the start), shows the days that are not a true count (manual 4.1). Fault starts sit clear of
holidays and clock changes, and two detectors written apart (a change point and a daily-median chain) recover every
window (asserted). Hazards (filed, executed by the cracker): the counters carrying a missed poll into the next answered
one, and restarting after a whole-day outage (manual 3.2), S-0103R continuing S-0103, NR and EST hours, 23 and 25 hour
days, AASHTO month by weekday. Stops (AADT / K hits of 8): the filed rules (the cracker) 0/0; status OK only 0/0;
faults found, carried polls kept 3/3; every hour after an NR dropped, whole-day outages too 0/8 (against manual 3.2);
the plain mean of valid days 0 AADT.

**Ask B: the 2025 base-year validation at the three river-bridge stations, by direction and peak hour (12 figures,
percent to one decimal).** H18: the credibility of the model the scores rest on, read at the screenline; the call does
not read the validation or count files. Primary device: the same loop and card faults, which fall in the validation
months at all three bridges (April, September, May), so the filed day rule without them averages undercounted or
overcounted days into the counts. Hazards (filed): passenger-car equivalents to vehicles through HV_PCT (which moves by
direction and peak), hour ending 8 and 18, valid Tuesdays to Thursdays in March to May and September to October, S-0103R
in the autumn months. Stops: the filed rules (the cracker) 0 of 12; the faults found 12 of 12.

Main population zero-counts: the call reads the link, node, trip and loaded-network files, the documentation's chapters
4 to 6.2, the guidance and the TIP workbook, and none of the count, station or validation files; the asks read those and
the documentation's 6.3 and 6.4 only. The probe file, the segment reference and the CMP memo are distractors (named in
metadata.json), with the crash summary and the transit ridership.

| Ask | Cracker (lands the call, executes every filed rule, runs the battery) | Verdict |
|---|---|---|
| A AADT and K-factor | 0 of 16 on the filed rules; the faults are on no filed path | miss |
| B validation | 0 of 12 on the filed rules; the faults are on no filed path | miss |

Pair ceiling: 26.0 ((45.0 + 7.0) / 2), the cracker keeping 0 of the 28 ask figures and the mirror (the fixed-volume
call) 0 of the 9 call figures.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Pre-ship check

- 2026-10-27, stage 4 on the cut pack. Leak reader (isolated, sonnet, medium): no decisive-step sentence, no file ranks
  the candidates, nothing reads as the answer; it calls the loaded network a mild helper (a check on a solver's own
  no-build run, carrying no build result), which is what it is. Its question 6 read the call as following a stated
  procedure (guidance 2.1 and 2.2 with documentation 6.1). Every REVIEW line harmless (documentation vocabulary; four
  hourly counts that coincide with answer figures in a 140,160-row series; zone-range labels; files that list stations,
  corridors, links, routes and segments rank nothing). The stump-vocabulary lines, ruled here: documentation 4 to 6 and
  the guidance carry network, equilibrium, capacity and no-build as their own subject, and neither says that the
  no-build loads do not hold on a build network.
- Judge pass 1 (/tmp/determinism-check-task307-1793113523): DETERMINISTIC, FIX_NOW. The main call and all four
  candidates' figures reproduced on its own solver (Center Street 322,911, Route 9 159,166, Southport 125,963, Ferry
  Street 37,203; every per-million figure); the easy route names Route 9 at 196,483. Gate G method_or_model_selection,
  analytical_non_defect, no surface read; Gate H domain pass, layers pass, decisive step analytical, borderline toward
  rule application because documentation 6.1 files user equilibrium. The judge settles the reader's question 6 on what
  the shipped sentences license (build-pipeline, stage 4): the guidance files the estimand and the documentation the
  model's general method, and the decisive step is seeing that the loaded no-build volumes do not stand for a build
  network. Three forks, all fixed in one pass: F1 the Route 9 section's facility type after widening (closed by guidance 4, the
  coding sheet changing lanes only, with a neutral sponsor description; SF16 asserted); F2 the counters carrying a missed poll and restarting after
  a whole-day outage (filed in manual 3.2, so the carry is a hazard and the loop faults carry ask A); F3 the probe
  stamps marking the interval end (filed in the CMP memo, which left the planning time index ask with no silent device,
  so that ask was dropped and the probe files ship as distractors).
- Realism fixes from the reader: transit ridership on route levels with a season and a trend; heavy-vehicle shares by
  direction and peak in the validation file; candidate costs stored as numbers; work orders numbered across every crew.
- After the repair: station seeds re-tuned so the repaired cracker misses every figure; checks 431, verifier 0
  failures, two byte-identical builds, figures_check, precut 0 FAIL, leak.py REVIEW (the same kinds of line).
- Judge pass 2 (/tmp/determinism-check-task307-1793114444) on the repaired pack: DETERMINISTIC, APPROVE; every graded
  figure reproduced (8 AADT, 8 K, 12 validation cells, all four candidates); Gate G method_or_model_selection,
  analytical_non_defect; Gate H analytical, borderline toward rule application as in pass 1. Its optional note, a
  missed poll carried across midnight, filed in manual 3.2 ("across midnight as at any other hour"); the Route 9
  description made neutral (SF16 closed by guidance 4). No graded figure moved; rebuilt twice byte-identically,
  verifier 0 failures, figures_check, leak.py REVIEW, precut 0 FAIL. Final isolated read: question 6 an analytical
  choice. Watch item for the portal: Gate H borderline (documentation 6.1 files user equilibrium).
- The 10/10 rules re-read against the built pack: the decisive step is re-solving where the 2028 trips go on each build
  network; the mess (two-way records, subzone tables, counts and their statuses, passenger-car equivalents) stays Layer 1.

## Tried and rejected

- 2026-10-27: OS09 (a mini-split rebate programme's net first-year savings) left at the draw: its honest
  stump labels were all held by the guard window and its furniture barred; moved to another domain.
- 2026-10-27: a resource adequacy design (cold-correlated forced outages, four capacity offers) prototyped
  and dropped before registration: task308's architecture 3 registered the same world and driver first.
- 2026-10-27: screening yield by time since the last screen dropped on paper as an echo of task301's
  yield-by-record-age driver.
- 2026-10-27: the planning time index ask (probe stamps marking the interval end as its silent device) dropped at
  stage 4: the judge read the stamp convention as an unfiled fork, and filing it hands the ask to every reader.
