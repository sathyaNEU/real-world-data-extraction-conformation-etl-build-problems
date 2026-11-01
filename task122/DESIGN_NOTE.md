# task122 design note: whether an en-route conflict probe becomes mandatory (architecture 4 on the card)

Architecture v4 on the card (the third architecture built for this slot; v1 was a draft redrawn before
registration), re-rooted 2026-10-31 at batch 1. v3, the VMK-4410 phase 3 dose read on the eGFR slope, is spent (its
line in Tried and rejected); its sections are retired, and a compact record of it is kept at the end of this note
beside v2's. Its pack, generator and goldens are removed from the tree and kept in history.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task122.json`, architecture v4, guard WARN only (the shell line read the
  retired prompt), registered 2026-10-31 after a fetch of main. The first draws collided and were moved: (objective,
  G6, go_hold_or_stop) repeated task306 v3 in the batch, committee_or_panel was banned by task468 v5, and (objective,
  G16) with either Gate G name repeated task182, task190, task191 and task228; the card files G14, decisive pattern
  conditioned yield, under decomposition_attribution.
- **Pairing.** Client domain human-factors-ergonomics, task type usability-task-performance-studies (which serves
  Experiment & Causal Analysis), objective Experiment & Causal Analysis: the effect of a controller's decision aid on
  how often the conflict alert fires, a task-performance effect read from an operational trial. The pairing has never
  been built; biomedical-clinical-research is spent for this slot after two architectures, and criminology was set
  aside because task125 drew police hot spot patrols the same day.
- **Niche.** Tasman Air Navigation (fictional), New Zealand's air navigation service provider, runs six en-route
  sectors around the Auckland hub from its area control centre (KAIPARA, HAURAKI, WAIKATO, TARANAKI, TAUPO, KAPITI),
  combined in pairs overnight. Since 1 April 2026 the planner controller of each sector has had PROBE-M, a medium-term
  conflict probe that predicts conflicts up to twenty minutes ahead and tests a planned trajectory change before the
  clearance is given, to switch on at the planner's own discretion. The short-term conflict alert (STCA) is the safety
  net that fires when two aircraft are predicted to lose separation within about two minutes.
- **Decision.** Whether PROBE-M becomes mandatory at every en-route planner position from 1 April 2027 (training in the
  first quarter of 2027), decided by the executive team at its November 2026 meeting on the human factors lead's paper.
  Forward facing: the mandate governs the 2027 operation.
- **The quantity.** The acceptance criteria (Safety Review Board, April 2026) file it: the share of the STCA
  activations the trial sectors would have raised in the time the probe was running that its use prevented, over the
  trial from 1 April to 30 September 2026, activations counted as the safety performance report counts them; the bar is
  one in five.
- **Data-native sentence.** Planners switch the probe on as climbing and descending traffic gathers in the sector,
  around the hub's departure and arrival banks, and almost every activation involves an aircraft climbing or
  descending, so the minutes the probe ran hold more climbing and descending traffic than the minutes it did not even
  at the same number of aircraft in the sector; the probe's own effect shows only when its minutes are set against
  minutes with the same count and the same climbing and descending mix, rebuilt minute by minute from the crossings.
- **Default path.** The safety report's measure, STCA activations per 1,000 flight hours, with the probe running
  against without (about twice as high with it running), then the traffic-adjusted comparison at like occupancy (the
  probe's minutes still raise about 15 per cent more than the same count without it): no benefit, keep the probe
  discretionary.
- **Golden.** At like count and like climbing and descending mix, the probe prevented about 30 per cent of the
  activations the sectors would have raised in its running time: mandatory from 1 April 2027.
- **Shape.** 07, grid of cells: the asks' sector-by-month grids (flight hours and the STCA rate the safety report
  publishes, with the flights each sector handled), beside the call, the share and the chart.
- **Shell.** Question form whether; deliverables docx and xlsx; forum the executive team, forcing event the mandate's
  rollout, organisation family utility or infrastructure, all clear of the last three builds (task468, task445,
  task272).
- **Personas.** Tessa Freeman (human factors lead), Kieran McMurray (safety analyst), Neil Hoskins (manager, area
  control centre), from `guard.py names --geo "New Zealand" --seed 122`; the prompt names no one.

**Mechanisms on file (Experiment & Causal), one line on the insight each spends.**
- task6: a non-randomised pilot read against each arm's own baseline once a hidden record stream is recovered.
- task12 and task15: an arm-correlated population or arm's rows recovered from a second system.
- task43, task44 and task83: a pooled effect carried onto a population whose moderator mix differs, or an effect
  conditioned on each unit's own treatment history.
- task69: overlapping contributions in a capped set; an assignment rate that moved across periods.
- task122 v1 to v3: a library-fill clause; outcomes logged only before a session closes; a chronic slope read after a
  one-off recovery.
- task131: a randomised tariff's effect on a design-day maximum where moved load returns after the window.
- Across objectives: task128's capacity cut as a natural experiment, task141's rota decision-makers' let-through
  shares, task121's rest before a shift, task136 and task137's not-yet-treated comparisons.
- None estimates a discretionary aid whose use follows the conditions that produce the outcome, read at like
  conditions measured at the grain the aid is switched at; none is in air traffic control.

**Sources, one line each.**
- The client's two-layer standard: the field's own measure decides here (the STCA rate per flight hour, and its
  traffic-adjusted form), worked where this trial's use of the aid departs from its preconditions, never a stated
  score or a window rule.
- The client's library has no human factors patterns; the nearest family is estimand_identification (confounding by
  the conditions of use), and the pattern is our own, `own:confounding-by-the-conditions-of-use-at-the-grain-of-use`.
- Field practice: STCA as the safety net and its activation rate per flight hour as an ANSP safety indicator; the
  quadratic growth of conflicts with traffic; climbing and descending traffic as the main source of conflict alerts;
  medium-term conflict detection at the planner position; the build carries the practice, not any provider's figures.

**Pricing on the cut pack (target.zip bb6963b0; every value from generator/figures.json and asserted in checks.py).** Share prevented by route: the report's rate per flight hour -108.1 per cent (the probe reads as raising activations); the hour's traffic held -109.9; like occupancy minute by minute -15.0 (with the hour of day -12.2; per aircraft pair -20.9; per climbing or descending aircraft-minute 14.2); like count and like mix, the standing family (strata, observed against expected, Poisson forms with the count as factors or pairs and the climbing count), 30.2 to 30.9, every member printing 30. The bar is 20: every route without the climbing count sits 5.8 points or more under it, and the standing family 10.2 points or more over it.

## Default path

1. Read SRB 2026/04 section 3.1: the probe becomes mandatory if its use prevented at least one in five of the STCA
   activations the six sectors would have raised in the time it was running, counted as the Safety Performance
   Report counts them.
2. Clean the records the report's way: each flight's latest plan revision from the FDPS crossing list, live
   activations once per event in the sector where they began, the planner workstation log's New Zealand time taken to
   UTC, a combined position's display covering both sectors.
3. Take the report's own measure, activations per 1,000 flight hours, with the probe running against without: 136.5
   against 65.6, the probe's minutes higher.
4. Recognise that the planners run the probe in busy traffic and hold the traffic: compare each sector's minutes with
   the probe running against its minutes without at the same number of aircraft in the sector (the field's
   traffic-adjusted comparison, conflicts growing with the aircraft present): the probe prevented -15.0 per cent.
5. File: short of the one in five, keep the probe discretionary.

Ends on: -15.0 per cent prevented, keep PROBE-M discretionary
Golden: 30 per cent prevented (30.3), mandatory from 1 April 2027

## Stump sentence

The default path holds the number of aircraft in the sector, minute by minute, finds the probe's minutes raising
activations at -15.0 per cent below the rate without it, short of the one in five, and keeps PROBE-M discretionary;
the step that lands it there is holding only the count, when the planners switch the probe on as climbing and
descending traffic gathers and almost every activation involves an aircraft climbing or descending, so at the same
count and the same number climbing or descending the probe prevented about 30 per cent of the activations its running
time would have raised, and becomes mandatory.

## Three rules

Task type: usability-task-performance-studies (Human Factors & Ergonomics), which serves Experiment & Causal Analysis: the effect of a controller's decision aid on how often the conflict alert fires, read from an operational trial with the aid at the planner's discretion.
Domain test: the quantity that decides is the share of STCA activations the conflict probe prevented, a task-performance effect the field estimates by comparing the alert rate with and without the aid at matched traffic load (activations per flight hour, then at like occupancy, since conflicts grow with the aircraft present); with a hospital's or a retailer's nouns there is no sector, no vertical mix and no conflict alert, and the task stops reading the same.
Swap: "should the ward's early-warning tool be mandatory, on the share of rapid-response calls it prevented" has no aircraft pairs, no climbing or descending traffic and no planner switching the aid on into a traffic mix, so the comparison that decides it does not exist there.
Layer 1: the FDPS crossing list's plan revisions (a revision re-issues the flight's whole list, so a superseded route's crossings drop out), the STCA log's continuation records when an alert carries into the next sector, inhibited and test activations beside live ones, combined sectors overnight on operational names against the crossings' elementary sectors, the planner workstation log in New Zealand time across both daylight-time changes against UTC everywhere else, re-entries into a sector; each is what the systems produce and none is placed to be caught.
Layer 2: estimand_identification, confounding by the conditions of use: the probe is switched on when the climbing and descending traffic that produces the alerts gathers, so its minutes and its idle minutes differ in that mix at any count of aircraft, and the counterfactual for its minutes has to be read at like count and like mix.
Decisive step: setting the probe's running minutes against minutes without it in the same sector at the same number of aircraft and the same number of them climbing or descending, both rebuilt minute by minute from the crossings' entry and exit levels, and reading the activations prevented from the difference.
Not semantics: reading every field, code and definition correctly (the revisions, the continuation records, the combined sectors, the local time) still leaves the report's rate at -108.1 per cent and the like-occupancy comparison at -15.0 per cent; no column marks a climbing aircraft or holds a minute's traffic mix.
Not rule application: SRB 2026/04 files the estimand (the share of the activations the sectors would have raised in the probe's running time) and the report the counting; no clause says which minutes stand for the probe's minutes without it, and executing every filed rule files whatever comparison the analyst picks; the enumerated family spreads from -157.1 to 30.9 per cent, the standing family (the strata, observed against expected, the Poisson forms with the count of aircraft as factors or pairs and the climbing count) from 30.2 to 30.9, every member printing 30, ruled by the data's own structure (probe use and activations both rising with the climbing and descending count at every occupancy).
Analyst test: a strong analyst cleans the records the report's way, takes the report's rate per 1,000 flight hours (-108.1 per cent prevented), holds the number of aircraft minute by minute (-15.0 per cent prevented) and keeps the probe discretionary; every field is read and every filed rule applied, and the call is wrong because the probe's minutes carry more climbing and descending traffic at any count of aircraft.
Estimand: probe_m_trial_acceptance_criteria.pdf section 3.1: the share of the STCA activations the trial sectors would have raised in the time PROBE-M was running that its use prevented; population, the six sectors' minutes with the probe running (section 3.3); window, 1 April to 30 September 2026, New Zealand time; unit, activations counted as the Safety Performance Report counts them (section 3.2); comparison, the same time without the probe.
No decoy: nothing is planted to be caught: no memo, draft, briefing or stakeholder figure argues a share or a call, the report's rates are its own published series for 2024/25, and the request asks for the paper and the tables without a view.
No certified replay: no certified or published figure reproduces any route; no file carries a share prevented, a rate with and without the probe, or a recommendation.
Lesson: an aid used at the operator's discretion is switched on when the conditions that produce the outcome gather, so its effect has to be read at like conditions measured at the grain the aid is switched at, the traffic's mix as well as its count; no build on file teaches confounding by the conditions of use.

## Survivor anatomy

Actor: the deciding property, how many of the aircraft in a sector are climbing or descending at a given minute, has no column; it is a relation between the crossing rows present in the same minute whose entry and exit levels differ, and the probe's minutes hold more of it at every count of aircraft.
Link: the probe's running time comes from the planner workstation log in New Zealand time on operational, sometimes combined, sectors, the traffic from the FDPS crossings in UTC on elementary sectors, the activations from the STCA log; no key joins them, only time intervals on the configuration in force, and the report's measure never compares a minute's traffic mix across the three.
Reflex: the field's measure, activations per 1,000 flight hours with the probe running against without (-108.1 per cent prevented), and its traffic-adjusted form at like occupancy (-15.0), sit at rungs 0 and 2 and file a wrong call.
Back-test: the textbook route validates: the trial's minutes without the probe run at the report's 2024/25 rates for each sector, and the like-occupancy comparison is steady when the hour of day is added (-12.2 per cent), so nothing in the record flags the comparison it rests on.
Second use: every file the decisive step reads is in the pack for a reason it independently has: the crossings for the flight hours and flights handled the tables owe, the STCA log for the activation rates, the planner log for the probe's running time the criterion names; the entry and exit levels are the crossing list's own fields.
Shock: the climbing and descending mix swings with the hub's departure and arrival banks every day, ordinary movement; no sector, month or day stands out, and the probe's share prevented holds in every sector.
Pins: the WHAT sits in SRB 2026/04 (the share of the activations the sectors would have raised in the probe's running time, the counting by the report, the window, the combined positions) and no filed sentence names the traffic, the count or the mix of aircraft, or a comparison; deleting section 3.1 unforces the call and the section names no step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 the report's rate per 1,000 flight hours, probe running against not | the report defines the rate | flight hours from the crossings | the field's measure | none refutes it | the battery runs it | one ratio | none | readable |
| 1 the hour's traffic held | none | hourly counts from the crossings | a careful variant | none | yes | one stratification | none | readable |
| 2 like occupancy, minute by minute | none | the crossings give the count | the traffic-adjusted reflex | none | yes | one stratification | none | readable |
| 2b per aircraft pair | none | pairs from the count | the conflict-geometry reflex | none | no | one ratio | none | readable |
| 3 (decisive) like count and like climbing and descending mix | none names the mix, the levels or a comparison | no column holds a minute's climbing count | not the reflex: the field adjusts for load | none | no battery item | not affine in a shipped column | the levels are the crossing list's own fields | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the activations the sectors would have raised in the time it was running | the counterfactual for the probe's minutes | the rate of the minutes without it | the off-time rate files discretionary | SRB 2026/04 3.1 ("would have raised"); asserted |
| SF2 | the time it was running | the planner log's New Zealand time taken to UTC | the log read as UTC | moves the call (asserted) | the planner guide section 4 ("in New Zealand time") |
| SF3 | activations counted as the report counts them | live, once per event where it began | every live record, or every status | same call; same printed share for the continuation reading (asserted) | the report section 2; SRB 3.2 |
| SF4 | a combined-sector activation | the elementary sector of the first-named aircraft | the first sector of the combined name | same printed share (asserted) | the report section 2 |
| SF5 | the trial window | 1 April to 30 September 2026, New Zealand time | UTC dates | same call (the export is the window; asserted) | SRB 2026/04 section 2 |
| SF6 | the share prevented | over the probe's running minutes | a pooled rate ratio | same printed share (asserted) | none needed |
| SF7 | an aircraft or a probe display in a minute | the minute's midpoint inside the interval | the minute's start, or any overlap | same printed share (asserted) | none needed |
| SF8 | a flight's crossings | its latest plan revision's list | the latest revision of each flight and sector | same printed share; moves the asks (asserted) | the crossing list (a superseded crossing overlaps the flown one in time) |
| SF9 | climbing or descending | entry and exit levels differ | a threshold on the change | same call (levels equal or 40 or more apart; asserted) | the crossing list |
| SF10 | the share's rounding | the nearest five per cent | other units | the prompt files it; mid-bin asserted | the prompt |
| SF11 | the asks' months | New Zealand calendar months | UTC months | moves 30 or more of 36 cells (asserted) | the prompt; the report section 2 |
| SF12 | flights handled | each flight once in each sector it entered | crossings | moves every sector (asserted) | the report section 2 |
| SF13 | an activation's month and sector | its start in New Zealand time, where it began | its end, or the receiving sector | the report's counting (asserted in figs) | the report section 2 |
| SF14 | further strata (hour of day, configuration, weekday) | not needed | added | same printed share (asserted) | none needed |
| SF15 | the climbing count's resolution | each exact count | bins (none, one, two, three or more), both counts binned, or the climbing count without the count of aircraft | binned cells print 20 (20.2; both binned 21.2), a binned Poisson files discretionary, the climbing count alone prints 35 (36.6) | the data: the exact cells hold all but 52 of the probe's running minutes, a top bin of three or more fails a likelihood ratio at p < 0.001, and inside it the probe's minutes carry more climbing aircraft at the same sector and count (asserted) |
| SF16 | the adjustment's form | the cells, or a Poisson with the counts as factors (or log pairs) | a Poisson linear in the count of aircraft and the climbing count, or sector by the two counts linear | the linear form files discretionary (19.4), sector by linear counts prints 20 (22.2) | the data: the linear form fails a likelihood ratio against the factor form at p < 0.001 on every minute and on minutes with two aircraft or more (asserted); the factor, log-pair and climbing-linear forms agree at 30 |
| SF17 | one pair's records close together in one sector | none occur (a hand-over record is in the next sector, 0 to 2 s on) | merged as one activation | no count moves (asserted in A4) | the data: one pair's records in one sector sit 243 s apart or more |

## Ladder

| Rung | Construction | Share prevented (per cent) | Dies to |
|---|---|---|---|
| R0 | per flight hour | -108.1 | the probe's minutes are busier, with more aircraft and more of them climbing or descending |
| R1 | hourly traffic | -109.9 | the hour's traffic misses the minute's: the probe runs in the hour's climbing and descending minutes |
| R1b | same sector-hour | -157.1 | within the hour the probe runs in the minutes the climbing and descending traffic fills |
| R2 | like occupancy | -15.0 | at like occupancy the probe's minutes still hold more climbing and descending aircraft |
| R2 | like occupancy and hour of day | -12.2 | at like occupancy the probe's minutes still hold more climbing and descending aircraft |
| R2b | per aircraft pair | -20.9 | per pair still leaves the climbing and descending mix unheld |
| R2c | per climbing or descending aircraft | 14.2 | per climbing aircraft leaves the aircraft around it unheld, and the probe's minutes hold more of them |
| R3 | Mantel-Haenszel (sector, n, T) | 30.7 | a standing member; prints 30 |
| R3 | Poisson, count factors, climbing count linear | 30.2 | a standing member; prints 30 |
| R3 | Poisson, log aircraft pairs and climbing count | 30.2 | a standing member; prints 30 |
| R3 | Poisson, sector, count and climbing count as factors | 30.3 | a standing member; prints 30 |
| R3 | observed against expected (sector, n, T) | 30.3 | the golden |
| R3 | strata with hour of day | 30.9 | a standing member; prints 30 |

- **Margins on the cut pack** (asserted in checks.py): every rung sits under the bar by more than the golden
  clears it (highest rung -12.2, the golden 10.3 over); the crude mix route, per climbing or descending aircraft-minute,
  sits 5.8 points under; every standing member prints 30, from 30.2 to 30.9, clear of the bin's edges; the golden 30.3
  sits mid-bin.
- **Separation.** The default path is wrong on the clean truth (T2) and the like-count-and-mix route on the world's
  own records is the golden (T2); the pack's handling recovers the truth minute by minute (T1).
- **Gate F.** No route that skips the climbing count reaches the bar (asserted).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the six sectors' minutes with the probe running | filed (SRB 2026/04 3.1, 3.3) |
| 2 Unit of account | an STCA activation, once per event | filed (the report section 2) |
| 3 Attribution window | 1 April to 30 September 2026, New Zealand time | filed (SRB 2026/04 section 2) |
| 4 As-of dating | the extracts of 5 October 2026 | the files' own period |
| 5 Version basis | each flight's latest plan revision | C1 (SF8) |
| 6 Denominator | the probe's running minutes' expected activations | filed (SRB 3.1) |
| 7 Weighting | the probe's own minutes (observed against expected) | C1 (SF6) |
| 8 Window length | the trial | filed |
| 9 Boundary inclusivity | at least one in five | filed (SRB 3.1) |
| 10 Rounding path | the share unrounded, printed to the nearest five | the prompt; C1 |
| 11 Tie-break | none | C1 |
| 12 Maturity and censoring | the trial closed on 30 September; the log is complete | filed |
| 13 Order of operations | clean, rebuild the minutes, stratify, compare | C1 |
| 14 Row order | none: set operations by sector and minute | C1 |
| 15 Duplicate resolution | a continuation record is the same event | filed (the report section 2; SF3) |
| 16 Identity normalisation | callsign and time to the flight's crossing | SF4 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | minutes, flight hours, activations per 1,000 flight hours | the files' own fields |
| 19 Code and status semantics | LIVE, INHIBITED, TEST | filed (the report section 2) |
| 20 Integerisation | whole activations and aircraft | C1 by construction |
| 21 Clause scope | SRB section 4's survey and training plan inform the rollout, not the decision | filed scope |
| 22 Forward window contents | the mandate from 1 April 2027 | filed (SRB 2026/04 section 1) |

## Literal reader

Executed word for word, SRB 2026/04 section 3.1 asks for the share of the STCA activations the six sectors would have
raised in the time PROBE-M was running that its use prevented. Read literally, the minutes without the probe stand for
the probe's minutes only where they carry the same traffic: the same sector, the same aircraft present and the same of
them climbing or descending, since the planners switched the probe on as that traffic gathered and the activations
come from it; the probe's running time raised 1,542 activations, and its minutes at combinations that also occur without
it (all but 52 of them) raised 1,520 against 2,181, about 30 per cent prevented. The asks' months, counts and flights read
literally on the report's definitions give the figures in figures.json.

## Oracles

None on the main call: no file carries a share prevented, an activation rate with and without the probe, or a
recommendation; the report's rates are for July 2024 to June 2025, before the probe. The asks have no oracle either:
the report's tables cover a year with no overlap with the trial.

## Ask sheet

Three asks on the trial's records, each read through a reconstruction across two systems or grains no sentence
states.

**Ask A, flight hours by sector and New Zealand month (36 figures).**
- Files: the FDPS crossing list.
- Primary (D9, a superseded plan): a revision re-issues the flight's whole crossing list, so a rerouted flight's
  first-plan crossing through a sector it never flew stays in under the natural de-duplication (the latest revision
  of each flight and sector); only each flight's latest revision is flown.
- Hazards: month ends in New Zealand time against UTC timestamps, across both daylight-time changes.

**Ask B, STCA activations per 1,000 flight hours by sector and month (36 figures).**
- Files: the STCA log, the crossing list.
- Primary: the continuation record an alert opens as it carries into the next sector is the same event, found only
  by its pair and its start at the hand-over second; a combined-sector activation goes to the first-named aircraft's
  sector, read from the crossings.
- Hazards: inhibited and test activations; Ask A's hours as the denominator.

**Ask C, flights handled by sector over the trial (6 figures).**
- Files: the crossing list.
- Primary: Ask A's superseded crossings put flights in sectors they never entered.
- Hazard: re-entries counted once (the report).

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at like occupancy) | Verdict |
|---|---|---|---|
| A, 36 monthly figures | takes the latest revision of each flight and sector | the same | miss |
| B, 36 monthly figures | the same hours under the rates | the same | miss |
| C, 6 figures | counts the superseded crossings' flights | the same | miss |

Pair ceiling: 36.9 (keeps 12 of 79 ask criteria, response 53.4).
Mirror leakage: 15.2 per cent of the ask weight.
Measured by: generator/ceiling.py (run on the cut pack, target.zip bb6963b0)

## Leak sweep

`leak.py task122 --asof 2026-10-09` on target.zip bb6963b0: REVIEW, no LEAK; each line ruled.
- Sweep 3 on `probe_m_trial_acceptance_criteria.pdf` and `probe_m_planner_guide_v2.1.pdf` (the call's words:
  PROBE-M, mandatory, en-route planner position, 1 April 2027): harmless; the criteria state the decision the
  executive team takes and the guide names the tool and its position, and neither carries a share, a rate with and
  without the probe or a recommendation.
- Sweep 4 on the guide (traffic, minutes, aircraft, sectors) and the safety report (traffic, aircraft, sectors):
  harmless; the guide says what the probe predicts and the report defines its counts, and neither names a mix, a
  level, a comparison or a count of aircraft to hold (asserted by reading, and the Pins line).
- Fixed before this run: the 2024/25 report's published figures moved off every figure this trial owes (a flight-hour
  cell printed as one of the trial's), and the request's signature no longer repeats its sender's first name.

## Pre-ship check

1. Three rules: the decisive step (the probe's minutes against minutes without it at like sector, count and climbing
   and descending count) is analytical; nothing planted, read or executed decides (the Three rules lines).
2. Determinism: SRB 2026/04 files the WHAT; the standing family converges on 30 across strata, observed against
   expected and the Poisson forms, every presence convention, revision and continuation reading and added stratum
   (SF1 to SF17, asserted; SF15 and SF16 by the data's rejection of the coarser and linear forms).
3. Gates on the final cut (target.zip bb6963b0): generator checks, the independent verifier on every graded figure, two
   byte-identical builds, figures_check.py, precut.py, voice-check.py, leak.py REVIEW with no LEAK, guard.py heart
   and surface; the leak reader and the determinism judge run from the main thread.
4. Surface: the one promoted pair, task81 (economics, a regional employment incentive costed from employer schedules,
   a descriptive quantity), rides the place name New Zealand, a real country and not an invented name, and the
   published-series context type; its domain, objective, decision type and driver all differ, so it is not a clone.

## Tried and rejected

- First draft (v1, drafted 2026-10-08, never registered): every proposal failed a different launch condition and the test-calendar
  library-fill clause widened the choice to the registered library, where only E cleared all three. Died at checkpoint A because the
  decisive step was a written rule a strong solver follows once no proposal qualifies (measured trap #9 alone scored 0.58 in its
  nearest exemplar, so the stump leaned on lower rungs firing first, and the nearest dead shape is argmax under a stated rule over a
  filed candidate list, task36), and because its honest Gate G, binding_constraint, collided on (objective, G11, binding_constraint)
  with task106 and 13 older builds and passed only after the card relabelled it method_or_model_selection.
- Redraw candidate, 2026-10-09, the leader outside the logger's reach: B's pinned listings fall outside the logger's per-session
  candidate pool on most new-buyer sessions, so its new-buyer guardrails are not identified and B cannot be certified (#13, G15,
  guard PASS). Dropped before registration: it fails Gate G's instrument repair (a logger able to draw B's rankings observes the
  decision's quantity directly and the task collapses, the 89 v6 dead shape), and it carries an arithmetic symptom, B's
  self-normalising weight sum at a fraction of the session count, visible to any solver who prints the normaliser or the
  unnormalised estimate beside the normalised one.
- Other decisive moves screened at the redraw and rejected on paper: carrying a correct pooled lift onto the Q1 traffic mix (the
  transport driver of task43 iteration A, task44 v2 and task83); habituation measured from each buyer's prior exposure count (task83's
  conditioning on each unit's own treatment history); shared unique listings depleted across buyers (task106's shared-pool driver);
  the Q1 control being a retrained incumbent (a dated release-calendar line that asks the question for the solver); and a test-power
  or clustering argument (G2 is banned against task120 and G17 is supporting only).
- Design stage, 2026-10-09, grading the draw's 48 guardrail cells as the shape's grid: rejected on the pair
  arithmetic. The guardrail read is on the main call's path and on the kept basis only B's row moves out of its
  bins, so the response that lands E keeps all 48 and the best response that stops at B keeps about 40; the pair
  sits above 50 on paper. The grid became each policy's fee income by cell, and the guardrail moved to hatching.
- Design stage, 90 per cent lower bounds as graded figures and as the lift condition: rejected. A delta-method bound
  and a bootstrap bound differ in the first decimal, and B's kept bound sat at +0.4 against a zero bar, a knife
  edge on the runner-up. All three conditions became point rules with stated margins.
- Design stage, a fee charged once per checkout and repeated on every order line (D6) as the grid's primary:
  rejected. Splitting a bundle's fixed fee between the carousel order and the other items in the same checkout is an
  allocation fork on every bundled cell.
- Design stage, refunds on cancelled orders as a fee-path device: rejected. Cancellations visible on the ask path
  invite taking cancelled orders out of the main call's lift, a fork on a graded figure.
- Design stage, the offers clock (UTC acceptance against local checkout at a 24-hour expiry) as a hazard: rejected on
  magnitude, about 0.4 per cent on a cell, inside the one-decimal bin.
- Design stage, shipping each archived session's follow-up orders so the archive is blind by construction in the
  pack: rejected. The column names the other outcome and hands route 1 over; the archive ships in-session orders
  only and the blindness is asserted in the generator with the hidden follow-ups.
- Design stage, a first-time-seller ask on a prior-account chain (D7): dropped for this pack. Its construction layer
  is level (B's brought-forward orders rarely go to first-time sellers) and its two files take the pack past 24;
  kept in reserve as an ask device for a hardening loop.
- Design stage, the draw's four-rung sketch (A, C, B, E) carried as the ladder: below the pipeline's five-rung floor,
  because replay and per-render weights both named A, so the two refused estimators were one rung. Split by giving
  the logger's D allocation to the pickup cities (replay over the render rows names D) and A its gain in long
  sessions (render weights name A); every leader is still a different policy.
- Build stage, 2026-10-09, the design's render-weights figures for B (8.31 in-session, 7.70 kept): infeasible.
  With B's session-weighted borrowing at 4.73, the render-weighted borrowing cannot fall below 4.73 x 150,400 /
  404,990 = 1.76 even with every borrowed order in a single-render session, so B's render-weighted kept could
  not exceed 6.55 and the render/eight-cells/kept grid cell would not name B by 1.15x over E. Repaired in the
  data rather than the ladder: B's added new-listing orders rise with session length in the new-buyer cells, so
  B's render-weighted in-session figure is about 9.0 and its render-weighted kept about 7.0 (1.20x over E), and
  A's render-weighted figure rises to about 11.0 to keep rung 1's margin at 1.22x over B.
- Build stage, 2026-10-09, the design's 90 per cent bound check (a bound above zero passes B, D and E and fails F):
  dropped. On the kept basis every policy's per-session outcome includes three weeks of orders, so a delta-method
  bound straddles zero for every policy and the sentence would be false; the charter's conditions are point rules
  and the charter says so, which is the closure, and no assertion claims a variance result.
- Build stage, 2026-10-09, organic watched-listing exposure for the five rankers that do not read saves (the design's
  "plus 0.03 of organic watched exposure" and borrowed 0.06 to 0.30 for A, C, D, E, F): dropped. Route 1 and route 2
  agree to the order and to the cent only if each (cell, ranker) group's in-session watched purchases are a
  multiple of eight with five in eight bought anyway; at an organic purchase rate of 0.1 to 2.3 per 1,000 a group
  of 400 to 3,000 sessions can only hold 0 or 8, so one octet put 3 borrowed orders per 1,000 into a single cell
  (F, web 30-179) and erased F's young-to-old spread that the restatement device needs. Now only the velocity
  boost's build shows a buyer's watched listings (every other ranker, archived ones included, draws from a pool
  that leaves them out, which is also why no archived test could see the borrowing); the other five policies' kept
  and in-session figures are equal, and the decomposition applied to B alone files E at 5.7, a cracker.

- Build stage, 2026-10-09, the design's assertion 13 as written (any segment's anyway rate, applied to every
  session, files the same kept figures): infeasible. B's kept lift moves about 7.5 per 1,000 per unit of the rate, so
  a segment 0.008 off the pooled 62.5 per cent (four-render sessions, 63.3) nets B to 3.25, across its bin edge, and
  no position of B inside its bin survives a spread of 0.01 either way. Replaced by the readings a solver actually
  runs: every segmentation netted stratum by stratum (cell, ranker, cell by ranker, platform, tenure band, renders,
  watch-list size, weekday, ISO week, half) and each natural sub-population's rate (incumbent arm, velocity arm,
  each platform, each half, one-render and up-to-two-render sessions) applied to every session, all filing E 5.7
  and B 3.3; the most extreme single segment applied everywhere is recorded as the thinnest boundary, not asserted.
- Build stage, 2026-10-09, the two halves of the logged window stratified on in-session outcomes only: each
  policy's kept lift differed between the halves by up to 12 per 1,000 (B 9.4 against -2.8), because three weeks of
  background orders per session fell at random between the halves, which hands a solver who checks stability a
  reason to distrust route 1. Equal half sums of in-session and 21-day orders per (cell, ranker) then still left C
  and D 0.4 to 0.5 apart on the kept basis, because a group with an odd session count puts one more session in one
  half and a kept base of about 1.8 orders a session moves that half's mean. Now each group's halves hold the same
  mean of both counts to within one order, the odd orders and sessions placed by a search that matches each
  ranker's half gap to the incumbent's; every policy's halves agree within 0.09 on either basis.
- Build stage, 2026-10-09, placing the fee cells by whole-euro price moves on plain orders alone: could not carry
  the price-paid device out of the bin where the arm's accepted-offer discount per session matched the
  incumbent's (shifts of -0.008 to 0.034 in five cells), and in two cells the January row and the asking price
  cancelled. Replaced by three levers on the cell's own in-session orders, searched together: a plain order's price
  moves the figure and every reading alike, the asking price of an order bought on an accepted offer moves only the
  asking-price readings, and the price of an order paid in person moves only the readings that charge it; every
  one of the seven device combinations and the natural read now clears all 48 cells, the two under EUR 1.00 included.
- Build stage, 2026-10-09, the slot-total placement as first written scored distance from the round hundred, which
  pushed the totals toward the bin edges (A's orders sat 14 from one). Now scored on distance to the edges, 20 to
  45, with every wrong reading of every total at least 5 outside its hundred.
- Build stage, 2026-10-09, the pooled-lift stop on ask 2 (one pooled kept lift times the planned total) against a
  planned Q1 cell mix that matched the logged summer mix: it filed the same hundred as the cell-by-cell total for
  B, C, E and F (4 to 23 orders apart). The weekly table now carries a January new-buyer surge in both years (the
  0-29 band peaks 8 points above its base share in early January, the 30-179 band 4 points), which puts the pooled
  and cell-by-cell totals at least 138 orders apart for every policy before placement.
- Solver round 1 (plain, 2026-10-09), the five-rung build as shipped: LANDED, proxy 89.8, asks 6 of 8. The solver walked every
  rung without friction and executed the decisive one at its step 6 as a work order: "Lift outcome: all orders by the buyer (any
  channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days. HC-33 pins watch-list
  listings in tiles 1-2, which cannibalises favourites/alerts orders in the 180+ tenure cells, so its net log-mix lift is 3.30
  against a gross carousel lift of 7.96." The charter's lift definition (orders during the test, every channel) plus a shipped
  all-channel order file keyed by buyer makes the any-channel window the default outcome, so the netting is never a construction.
  It also kept every ask figure (48 fee cells, 12 totals), and it weighted the headline to 5.8 on the slot mix against the
  golden's 5.7 on the logged mix while using the slot mix for the totals, a determinism finding on the headline basis.
- Harden loop 1, diagnosis of round 1 (the borrowed-order netting as the decisive rung; P1 in-person pickups, P2 the R2
  restatement, HZ1 the deferred tariff, HZ2 the price paid and HZ3 the app gating as the ask devices): the decisive quantity
  was the charter's own observable, so the solver never had to think of borrowing at all. Its "Lift outcome: all orders by
  the buyer (any channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days"
  is charter 2.2 executed on the one extract that already holds every order by buyer, and the netting of B fell out of it as
  a by-product ("which cannibalises favourites/alerts orders in the 180+ tenure cells"). Every ask device died the same way:
  each organ sits in a file the ask's own path opens with its rule beside it ("recomputed at the 1 Sep 2026 tariff ...
  because KB-2027-01 was deferred", "Pickup orders paid directly carry no fee", "R2 restatement 2026-W01..W12 (it matches the
  account-service tenure), app only from W03 because of the release 27.1 gate"). Dead: a decisive rung whose correct basis
  is the definition's own observable on a shipped extract, and an ask device whose rule is filed in a document the ask path
  reads anyway. What the trace holds fixed without checking is that the logger's in-session columns measure the charter's
  quantities whenever the charter is not about orders over the test (its guardrail is read "from ordered_tiles"), which is
  where loop 1 goes. Harden loop 1 of 3 on this architecture.
- Harden loop 1, the come-back orders credited to the session the tile was in (home_session_id = the logged session): the
  habitual tie between ordered_tiles and the carousel orders credited to each session then failed in 202 sessions, every one
  outside C, an arithmetic symptom on the wrong path that points straight at the device. Now each come-back is credited to
  the session it was placed in, the tie holds in all 150,400 sessions, and the field reference's seven-day rule lets the
  listing alone attribute the order to its tile.
- Harden loop 1, no come-back orders at all under C: one zero in a by-arm count reads as a marker; C now comes back at 0.15
  of the others' rate (3 orders, none in app 0-29).
- Harden loop 1, charter 2.4 as written ("its orders placed from a home carousel tile"): it also admits every carousel order
  by the arm's buyers in a window, a reading under which C passes and is filed; 2.4 now counts the orders placed from the
  carousel tiles the arm served.
- Harden loop 1, the January new-buyer surge at 8 and 4 points (built for the pooled stop on ask 2): it put the slot-mix
  headline at 5.8 against the logged window's 5.7, round 1's determinism finding. Cut to 2 and 1 points, the headline
  converges (5.716 against 5.697) and the pooled totals fall 14 to 41 orders from the cell-by-cell ones for B and E, which
  no placement can carry out of the hundred, so the pooled stop is retired: pooled readings are placed at least 5 from the
  edges on either side and recorded.
- Harden loop 1, every fee reading as a stop on ask 2: B with only P1 mishandled and F on the first release alone sit 25
  and 14 euros from their golden totals, under the 25 a stop needs with the golden 20 from its edges; both are carried as
  either-side readings at least 5 from the edges (both inside) and the placement reached 6.4 of slack.
- Harden loop 1, fee cells placed anywhere from 0.35 to 0.65 of the bin: 7 of 48 landed within 0.003 of the round
  one-decimal value (7.0001, -14.5997 and so on), a receipt; the window now leaves out the middle tenth.
- Harden loop 1, a fresh silent device for the order totals (the logger slice held out of slot arms, a weekly table
  counting home sessions rather than carousel sessions, Easter falling in the slot's last week, staff and monitor
  accounts in the weekly table): each needs a new organ on the traffic path or a rate the pack cannot pin, or reads as
  sabotage; the order half keeps P2 and HZ3 and the pair arithmetic counts it as leaking to both sheets.
- Harden loop 1 as built, graded in the re-run of round 1 (labelled "round 2, plain", 48.7, call missed, 3 of 8 items):
  the tile count held the call (the solver filed C at 9.8 with E as runner-up, its step "Guardrail on the in-session
  carousel order rate: the only breach is HC-31 in web 730+" never sees rung 3), but the ask layer leaked exactly as the
  stated exposure said: "This reconciles exactly to the Finance Q3 sheet (the 6,147 July shipped orders missing from
  payments supply EUR 8,205.17)". Reading the referee settled F1 (VAT out) and F2 (balance purchases charged), so all 48
  fee cells and all twelve totals landed. A referee that ties to the cent only under the golden fee basis is a recipe
  the solver reconciles to, not a silent organ; the fee devices cannot rest on the referee going unread.
- Harden loop 2, diagnosis of round 2 (loop 1's ask layer: F1 fee income net of VAT and F2 balance purchases charged as the
  silent primaries, P1, HZ1 and HZ2 stacked on every fee figure, P2 and HZ3 on the totals, and Finance's Q3 statement as the one
  referee, tying to the cent only under the golden fee basis): the tile count held the call, and every fee figure fell to one
  reconciliation, in the solver's words at its step 7, "Fee income is taken excl. 21% VAT. This reconciles exactly to the Finance
  Q3 sheet (the 6,147 July shipped orders missing from payments supply EUR 8,205.17)". A statement scoped to the extract's own
  buyers that ties to the cent under exactly one fee basis arbitrates all five fee devices at once and hands over the level,
  which is the oracle law 8 bans, not a referee; every device it did not settle was a filed rule the path reads ("KB-2027-01 was
  deferred by the 6 Oct pricing committee", "uncaptured pickups were paid directly and carry no fee", "app uses W03 to W12
  because the first app release on or after 4 Jan 2027 is 27.1"). Dead: a fee device whose correct handling is also the only
  basis on which the logged window's statement ties. Harden loop 2 of 3.
- Harden loop 2 build, the in-person price lever as single-euro moves within plus or minus 30: it moves only the full-cover
  half of a cell, and F app 730+ (23 in-person orders) could then clear its bin by no more than 0.0035; the lever now moves
  up to 3 euros an order over plus or minus 60 units, applied round robin across the cell's orders.
- Harden loop 2 build, traffic readings within 30 of a hundred's edge treated as stops: B's fee total with only the cover
  change mishandled sits 6.3 inside its hundred and no set of traffic factors carried every stop out (the placement score
  stayed negative); the near band is 40 and the readings in it are either-side readings, B's FX-alone total among them
  (recorded as kept by round 2's path).
- Harden loop 2 build, every fee reading at least 0.03 outside its bin: D app 0-29 with only the January row applied can
  sit no further than 0.0246 outside, because the two tariffs differ too little on that cell's orders for the price
  levers to widen it; the floor is 0.02.
- Harden loop 2 build, VAT taken off order by order converging without a lever: on an early placement one B web cell's
  per-order rounding fell 0.0031 outside the golden bin; a pair lever (plus and minus one euro on two plain orders, which
  moves only the per-order rounding) was added, and on the final placement it needed no pairs (0.0227 inside at the
  nearest).
- Harden loop 2 as built, graded in the re-run of round 1 (labelled "round 3, plain", token proxy 51.1, call missed, 4 of 8
  items by token; read-corrected about 23 to 31, because notebook items 1 and 2 and image items 2 to 4 were credited on HC-37,
  5.7, HC-33 and HC-34 named in the solver's screen-out and negation sentences): the tile count held the call for the second
  round running (C filed at 9.8, E runner-up at a gap of 4.1, at the same step, "Condition (b), each cell's carousel order rate
  against HC-24: HC-31 web 730+ is -2.74% and fails. All other policies' cells are within -1.5% (HC-34 app 0-29 -0.96%)"), but
  loop 2's ask layer leaked whole again: all 48 fee cells and all six policies' twelve-week totals landed, at its step 8, "covered
  orders are shipped orders plus pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee
  excl. VAT exactly ... Tariff for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01", and at
  step 9 it read P2, HZ3 and the 1 March cover change straight off the filed notes. Dead: a fee basis that still ties Finance's
  Q3 statement to the cent (the referee survived loop 2 as an oracle under a new cover rule) and traffic and tariff devices whose
  rule sits in a document the ask path opens. Harden loop 3 of 3 on this architecture is the last before a re-root.
- Harden loop 3, diagnosis of round 3 (loop 2's ask layer: FX, the 1 March 2027 checkout change in the capacity note's
  overlaps section, as the fresh primary on all 48 cells and the six fee totals; F1 VAT, F2 balance purchases, HZ1 the
  deferred January row and HZ2 the price paid stacked on every fee figure; P2 the R2 restatement and HZ3 the app release
  gate on the totals; Finance's Q3 statement as the one referee, still tying to the cent on the logged window's cover): the
  call held at the tile count, and the whole ask layer fell to two habits the solver runs by default. It reconciled its fee
  model to the referee, which still ties the logged window under the golden's own per-purchase basis and so settles VAT,
  balance purchases and in-person pickups in one pass, in its words at step 8, "covered orders are shipped orders plus
  pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee excl. VAT exactly ... Tariff
  for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01 even though the tariff register
  lists it"; and it executed every rule filed on the traffic path as a work order, at step 9, "The app arm starts 18 Jan
  2027 (release 27.1 after the code freeze), so app runs W03-W12 and web W01-W12 ... From 1 Mar 2027 (W09-W12) every
  pickup order is paid at checkout and carries the fee", so FX, built to sit off the fee path, was read in the same pass as
  HZ3 because both sit in the capacity note. Dead: a referee whose figure the golden's fee basis reproduces on the logged
  window (whatever changes for the slot, the statement hands over every logged-window device at once), and any device whose
  rule is a dated, named sentence in a document the ask path opens (the minutes, the release log, the capacity note), because
  the solver reads every note on its path and carries out what it says. Harden loop 3 of 3.
- Harden loop 3 build, the either-side band at 40 (a wrong total under 40 from its golden placed on whichever side of the
  edge it falls): infeasible on this pack. E's fee total has two compound readings on the twelve-week app traffic, one 52
  above the golden and one 55 below, and no placement keeps the golden 20 from the edges while carrying both out of a
  hundred-wide bin by 5 (best score -0.03 after refinement). The band is 56, which adds only those two readings.
- Harden loop 3 build, the traffic placement with every first-release total scaled linearly by the placement factors: the
  restatement's moves were counted on the placed table, so a placed cell's first-release sessions were not the factor times
  the unplaced cell's, and B's fee total on the first release with balance purchases uncharged and the logged checkout
  landed 0.21 inside its hundred's edge in the files against at least 5 predicted (the build stopped on
  ask2.every_reading_clear_of_the_edges.B). The moves are now counted on the unplaced table and added to the placed one, so
  a first-release total is the placed table's plus a constant and the placement is exact.
- 2026-10-10, retired: it passed both solver rounds after three hardening loops, but the determinism judge sent it back on Gate G: the answer wins only by reading the charter's outcome definitions in place of the logger's in-session reads (a single conceptual flip), and the shipped planning thread ranks the candidates. Under the author's standing rule a Gate G send-back is retired like a dead build, and DS11 takes the slot in a later wave.
- 2026-10-13, re-root under the 10/10 rules (v2 to v3): v2 is FAILED_TO_STUMP in perssathya's backlog. Its
  decisive step, the logger's in-session order column read against the charter's count of every order placed from
  the tiles an arm served, is a field read under a filed charter condition (data semantics plus rule application),
  and its estimator was pinned by nine certified archived tests (a validated decoy); a redesign inside the world
  would keep the carousel's nouns, and with app or retail nouns the slot question reads the same. The slot moves to
  Biomedical & Clinical Research, a domain never built.
- Re-root candidate, pharmacoepidemiology (new users of inhaled COPD treatments, time in hospital that the
  dispensing record cannot see): dropped on paper. The answer turns on the grace period and how inpatient days
  count against a supply, conventions a filed sentence would have to fix, and once fixed the step is rule
  application.
- Re-root candidate, protopathic bias with a long prodrome (a drug started for the early symptoms of the outcome
  it is then blamed for): dropped. The lag that decides is a convention the field disputes, so determinism rests on
  a pinned lag, and a solver who knows the drug class's literature reaches the answer from priors.
- Re-root candidate, criminology (reporting falls in hot-spot patrol areas): dropped; one obvious move (use calls
  from the public, not officer-initiated records), close to reading a field.
- Re-root candidate, assessment-time bias (progression found sooner in an arm scanned more often): dropped; the
  interval-censored estimate (NPMLE) is not unique and a solver's method choice moves the graded figures.
- Re-root candidate, eGFR off-treatment decomposition (the phase 3 end point read four weeks after the last dose,
  part of the early fall at the top dose not coming back): dropped as the decisive step. The natural construction
  (the week-56 off-treatment difference plus two more years of chronic slope) lands the golden, so it sits inside a
  strong solver's hypothesis space; with monotone dips and slopes, the one-year view and the slope-only view
  bracket the three-year answer, so in a pick of three one simple view always lands the call.
- Re-root candidate, a titration step at week 12 for the top dose (its further fall after the field's month-3
  knot read as a steeper chronic slope): dropped as the decisive step. The step is in the protocol and is a
  4.6 mL/min drop in one arm between two visits, a visible symptom a solver investigates; it also penalises the
  top dose in the same direction as the golden's dip, so the margins the conventional route needs are thin.
- Re-root candidate, slow drug accumulation (a long half-life, the haemodynamic fall deepening for five months):
  dropped. An exponential approach that is half done at month 3 is not finished by month 12, so no clean chronic
  window remains in 52 weeks, and one that finishes by month 6 leaves too little after month 3 to move the call.
- Re-root candidate, anti-drug antibodies (loss of response lagging antibody onset, so a 24-week maintenance read
  overstates week 52): kept in reserve, not drawn. The arm curves do not show the coming loss, which is its
  strength, but the projection rests on the loss distribution after onset estimated from a few early converters,
  and in a pick of three "fewest antibodies" or "the balanced regimen" lands the call by heuristic.
- Re-root candidate, detection bias through organ volume (a drug that shrinks the prostate makes biopsy more
  sensitive): dropped; the setting is the textbook case (the 5-alpha-reductase prevention trials), so a frontier
  solver recalls the resolution, and the adjustment's detection model is a fork.
- Re-root candidate, leaky against all-or-none vaccine protection carried to a high-transmission setting: dropped;
  the invariant-under-base-rate insight is task446's and task230's family, and the mechanism is identified only
  through a model of exposure.
- Re-root candidate, HbA1c lag (a 16-week dose-ranging read before glycation catches up): dropped on the swap
  test; the decisive move, the steady state of a lagged average, reads the same with a trailing business metric.
- Stage 3, 2026-10-13, the arms calibrated to the arm-mean line alone: the mixed model with a random intercept and
  slope per patient, the field's own slope estimator, read 10 mg about 0.4 higher on every measurement draw, because
  the few patients who left or stopped in an arm pulled its later visit means. Fixed in the data: the dropout, stop
  and potassium streams are drawn so the arm-mean line and the within-patient estimators agree, then the measurement
  draw so every estimator from week 24 sits in the golden's bins.
- Stage 3, the claim that a knot anywhere from week 24 to week 32 gives the golden figures on any draw: a slope from
  three visits carried to month 36 multiplies visit noise about sixfold, so the corridor is a property of the
  shipped draw, asserted, never of the design alone.
- Stage 3, treatment policy as a same-figures fork (SF5): values after a permanent stop show the early fall reversed
  and lift the late visit means; on the shipped draw 40 mg's figure moves a bin. SF5 is closed by the synopsis's
  intercurrent-event strategy (C4), the call unchanged.
- Stage 3, a chance baseline imbalance: a 40 mg arm whose baseline sat 0.85 below placebo's moved the level reading
  of the prompt's "how much higher eGFR would be" a bin. The randomisation's block order is drawn so every arm's
  baseline sits within 0.1 of placebo's, and the level and change readings converge (SF3).
- Stage 3, visits outside their windows at any week: dropping the few late ones from weeks 24 to 52 moved 40 mg's
  figure across an edge. Sites keep to the window from week 24 (out-of-window visits fall before it), so the mess
  cannot reach the decisive fit.
- Stage 3, clinic visits on weekends and a missed dispensing visit leaving one bottle for seven months: dates moved to
  the nearest weekday and drug collected at the site on the missed visit's day.
- 2026-10-31, at the re-root, architecture 2 on the slot (card v3, the VMK-4410 eGFR phase 3 dose) spent: the
  portal has recorded no responses for it (PENDING_REVIEW since 10-13; the FAILED_TO_STUMP entry in pipeline.json's
  returned record is v2's carousel build, retired 10-10 on a Gate G send-back and never submitted), so no landed
  call's step can be read from the record. It dies on the batch audit instead (precut FAIL with no survivor
  anatomy, leak.py LEAK on the shipped data dictionary and export manifest, the prompt counting the doses), and the
  step it meant to stop solvers on, starting the chronic slope at month 3 rather than at week 24 once the week-12
  diuretic easing had run its course, rides a clock the protocol states in writing, which a reader of the protocol
  reaches without the analysis; the redraw refuses any decisive step that a filed clock or sentence points to.
- 2026-10-31, at the draw: criminology hot spot patrols with displacement to the adjacent street segments as the
  decisive step: set aside when task125 drew police hot spot patrols the same day, and the interference family is
  spent by task131 v1 (left off the approved list).
- 2026-10-31, at the draw: a decision-maker design (job seekers allocated to advisers by rota, the effect read from
  each adviser's referral share): task141's approved driver, rota decision-makers' let-through shares, is the device.
- 2026-10-31, at the draw: staggered adoption against not-yet-treated units: spent by task136 and task137, the latter
  landed by a probe that compared each wave with the waves not yet treated.
- 2026-10-31, at the draw: regression to the mean behind comparably selected controls, the dip before programme
  entry, and immortal time from an ever-treated label: each has a textbook remedy a strong solver applies on sight (a
  discontinuity at the selection cut, a baseline before the dip, time-varying exposure), and immortal time sits one
  join from a column.
- 2026-10-31, at the draw: a fast-track review route confounded by the decision maker's queue: the swap test fails
  (the task reads the same with a hospital's nouns), and a faster route shortens the queue it is adjusted for.
- 2026-10-31, at the draw: ambulance auto-allocation confounded by the vehicles free at each allocation: task121's
  world (a county 911 centre dispatching ambulances).
- 2026-10-31, design prototype: the probe confounded by occupancy alone (the count of aircraft in the sector): the
  per-flight-hour rate and the like-occupancy comparison bracket the truth, and a solver who builds the minute grid to
  split flight hours by probe status holds occupancy by reflex, so the decisive step moved to the climbing and
  descending mix at like occupancy.
- 2026-10-31, design prototype: an activation risk built on aircraft pairs, each pair's risk by whether it includes a
  climbing or descending aircraft: parametric adjustments (linear or quadratic terms) spread four points round the
  stratified estimate; the risk is set log-linear in the count and in the climbing and descending count, so every
  standing adjustment agrees within two points.
- 2026-10-31, design prototype: the probe tracking the climbing and descending count tightly: overlap thinned at high
  counts and the observed-against-expected route drifted five points from the strata; each watch's own habit with the
  probe (unrecorded, drawn per watch and not per controller, so no controller's habit is an instrument) gives the
  overlap.
- 2026-11-01, stage 4 judge on target.zip c74f2a16 (FIX_NOW, a minor SOLUTION_WRONG): Critical Component 1 put 1,520
  activations in the probe's running time, where its minutes raised 1,542 and the 1,520 are those at combinations of
  sector, count and climbing count that also occur without it (52 running minutes have no such match); the write-up,
  the paper and the workbook now state both figures from figures.json.
- 2026-11-01, the same judge: one pair's STCA alerts drawn independently minute by minute left nine same-sector,
  same-pair records overlapping in time, so a deduplicating reading moved seven rate cells by about one per 1,000
  flight hours; closed in the data and not by a counting rule: one pair's records sit 243 s apart or more in any
  sector, a hand-over record aside (A4, SF17).
- 2026-11-01, the same judge: the safety report's dodge loop added an hour to a sector's first month each time the
  year's totals printed as a trial figure (TPO July 2024 at 2,838 flight hours against about 1,500 in every other
  month); the moves now rotate across the months and R1 holds every month within 4 per cent of the seasonal profile.
- 2026-11-01, the same judge's method forks, left open and closed by the data rather than by filing the comparison or
  the covariates (filing them hands over the decisive step): the climbing count binned none, one, two, three or more
  (20.2 on c74f2a16), both counts binned (20.9 to 21.5), the climbing count alone by sector (36.6), sector by the two
  counts linear (22.2) and a Poisson linear in the counts (19.4, the one that files discretionary); SF15 and SF16
  assert the likelihood ratios that reject the coarser and the linear forms.

## Architecture v3 record (spent 2026-10-31)

Registered 2026-10-13 under the 10/10 rules, built, judged DETERMINISTIC (APPROVE, one pass) and shipped the same
day; pending review with no portal responses on record when the batch 1 audit spent it (Tried and rejected).

| Axis | Value |
|---|---|
| Domain / task type | Biomedical & Clinical Research / longitudinal-outcomes-repeated-measures |
| Objective | Experiment & Causal Analysis |
| Niche | a Copenhagen-area biotech's phase 3 dose of its aldosterone synthase inhibitor VMK-4410, from a 52-week phase 2b in albuminuric chronic kidney disease |
| Shape | 11 before and after with a control |
| Decision type / unit | pick one of four doses; mL/min/1.73 m2 of eGFR against placebo at month 36 |
| Gap / pattern / generators | time; none; G4, G13, G16 |
| Gate G mechanism | method_or_model_selection |
| Stump strategy | decomposition_attribution |
| Forum / forcing / org family | line_manager_or_team / statutory_or_regulatory_filing / other |
| Deliverables | `VMK-4410_phase3_dose_recommendation.pdf`, `VMK-4410_phase2b_tables.xlsx` |
| Answer | 20 mg, 3 mL/min/1.73 m2 above placebo at month 36 (40 mg 2, 10 mg 1, 5 mg 0) |

Stump: a competent solver fits each dose's eGFR with the two-slope model, an acute effect to month 3 and a chronic
slope after it, carries the chronic slope to month 36 and files 40 mg; the step that lands it there is starting the
chronic slope at month 3, when the patients whose eGFR fell most had their loop diuretics eased only from week 12 and
recovered part of the fall over the following weeks; from week 24 the slope leaves 20 mg furthest above placebo.

## Architecture v2 record (spent 2026-10-13)

Realised analytical_tasks note DS01 (carousel test slot); registered 2026-10-09 after checkpoint A, built, three
harden loops and five solver rounds, retired 2026-10-10 after a Gate G send-back, never submitted, then put in the
author's backlog as FAILED_TO_STUMP and re-rooted here.

| Axis | Value |
|---|---|
| Domain / subdomain | Product Analytics / experimentation-measurement |
| Objective | Experiment & Causal Analysis |
| Niche | a Dutch peer-to-peer second-hand fashion platform (Vouwlijn) choosing which of six registered ranking policies takes its home carousel's Q1 2027 A/B test slot, every policy scored off-policy on randomised carousel logs |
| Shape | 07 grid of cells |
| Decision type / unit | pick one of six policies (named option) |
| Gap / pattern / generators | time, rule, population; none, B; G13, G9, G16, G2, G11 |
| Gate G mechanism | decomposition_attribution |
| Stump strategy | decomposition_attribution; decisive rule filed, official decoy, validated decoy (nine archived tests pinned the estimator) |
| Calibration form | pilot_log |
| Stakeholder / forum / forcing / org family | head of marketplace science / executive_team / vote_or_meeting / software_or_platform |
| Deliverables | `carousel_slot_q1_2027.ipynb`, `carousel_slot_q1_2027_cells.png` |
| Answer | E, the sequence ranker with the fresh-listing interleave (HC-37), 5.7 extra orders per 1,000 carousel sessions |

Stump (harden loop 1 onward): a solver who scores the six policies with the session-weighted estimator that alone
reproduced the nine archived tests and reads the cell guardrail on the render log's in-session ordered tiles
commits the slot to C, the session-sequence model; the charter counts every order placed from the tiles an arm
served, and buyers under every other ranker come back to order from a tile left on screen after the session
closes, so C fails the guardrail in app 0-29 and E is the largest lift that clears every condition.

Fate: solver rounds 2 to 5 held below 52 after round 1 cracked the draw's rung; the determinism judge sent it back
on Gate G (the answer wins only by reading the charter's outcome definition in place of the logger's in-session
read, a single conceptual flip, and the shipped planning thread ranked the candidates). Under the 10/10 rules the
decisive step is data semantics and rule application, so the architecture is spent.
