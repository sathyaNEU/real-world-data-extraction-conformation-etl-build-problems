# task188 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task188.json`, architecture v1, drawn 2026-10-13 from seed AD11 (which
  customer gets next quarter's one routing-hygiene engagement, judged by the pages it removes). The seed's world, a
  network operations centre paging on route-origin changes, sits in no client domain whose task type serves Anomaly
  Detection (Product Analytics' task types serve EC, DD, DQ, F, OS and RC only), so under the 10/10 domain rule and the
  author's instruction that a task which reads the same with another field's nouns is not domain fit, the draw keeps
  the seed's decision shape (one scarce response this week, for one of eight flagged candidates, judged by what it does
  about the alarms) and moves to the field whose own analysis decides it: arbovirus surveillance.
- **Pairing:** Epidemiology & Public Health, `disease-surveillance-outbreak-anomaly-detection` (serves AD and DQ), read as
  a mosquito control district's weekly West Nile virus surveillance: every zone returned positive pools in the week, and
  the call separates the real hot spot (the most infected host-seeking Culex females) from signals inflated by
  gravid-trap pools, understated by large pools, or carried by human cases from an earlier focus.
- **Niche:** Rindal County Vector Control District, a special district in the Red River Valley of North Dakota (the
  county, the city of Fjelstad and every organisation are fictional), runs eight treatment zones. CO2-baited light traps
  (host-seeking females) stand in every zone; gravid traps (females seeking an oviposition site, mostly Culex pipiens)
  in the two town zones. Culex females are pooled by site, night and species and tested by RT-PCR: the four northern
  zones' pools at the district laboratory (up to 50 females a pool), the four southern zones' at the Rindal County
  Public Health Laboratory under an interlocal agreement (up to 10 a pool). The contract applicator, Ostby Aviation,
  flies one aerial ULV adulticide block a week, Thursday night, weather permitting.
- **Forcing and forum:** the weekly surveillance-to-application cycle (`shift_or_daily_cycle`): trap-nights Monday and
  Tuesday, laboratory results by Saturday, the block named Monday for Thursday's flight; the district's operations desk
  books it (`operations_desk`); a special district (`local_government`); the requester is the operations manager
  (`field_unit_lead`).
- **Call:** the zone flown on Thursday 20 August 2026, judged by the estimated number of West Nile virus-infected Culex
  females collected per CO2 trap-night in the week ending Saturday 15 August 2026 (MMWR week 32).
- **Shape 01** (a ranked list, each candidate): every zone carries its locally acquired human cases this season and its
  CO2 trap-nights run and lost since 1 June (24, whole numbers); the call, its figure, the runner-up and its figure, and
  the infection rate that would flip the flight (5); a chart of each zone's cases by week of onset with named parts (4);
  the files (3). Criteria arithmetic: 36. The zones' own indices are not asked for: a table or chart of the decision
  quantity is keyed to the construction (`supplemental-stumping` Part 1.2).
- **Strategy and mechanism:** `composition_mix` (an infection rate measured on one sampled population, every Culex
  pool in the zone, carried onto another, the females the CO2 traps caught) with method selection forced by the data
  (a positive pool read as one infected mosquito); gap rule then population; decisive generator G14 (conditioned yield),
  G16 alongside; Gate G `method_or_model_selection`; calibration `none`.
- **Data-native sentence:** an infection rate read from pools counts at most one infected mosquito in each positive
  pool, so it understates infection exactly where the district laboratory's pools of fifty run hot, and a gravid trap
  catches only females that have already fed, which carry several times the infection of the host-seeking females a
  CO2 trap catches; the index of infected females per CO2 trap-night needs the likelihood estimate from the CO2 pools
  themselves.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 20 builds): 25 a second-source inflow; 28 a
  reachable share; 33 forward yield cut by an intervention; 48 a two-sided pair grain; 54 exposure in custody; 68 a
  matched panel through identity successions; 76 a zero-conversion look-back class; 85 a unit's own window; 103 a
  fan-out through authorisations; 104 a self-adapting scorer replayed; 119 waits a unit could shorten; 182 a lagged
  response to a shared driver; 183 repeat failers in parts; 125 a recruitment filter carried through; 180 detection by
  quiet hours; 181 crossings of moving units; 184 host stand-down; 185 a reading-dependent instrument conversion; 186
  an own-history null under shared local cycles; 187 a capped curve averaged over a per-unit spread. None estimates a
  rate from grouped tests; none separates the populations two sampling devices collect.
- **Guard:** WARN `overuse.objective` (this lane), `overuse.shape` (a ranked list fits eight zones), `repeat.gate_g` and
  `overuse.gate_g` (method selection here is forced by the pools' own structure, with no filed back-test or standard),
  `repeat.decision` (a pick is the seed's decision) and `repeat.question_form` (a pick asks which). Nearest drivers 0.05
  (task450 v2, task116, task253 v3, task500 v3): the abstraction test maps none onto this driver.
- **Sources:** the seed (AD11) gives the decision shape. Arbovirus surveillance practice gives the field's method: the
  vector index (estimated infected vector females per trap-night, summed over vector species) as the measure of human
  risk; the minimum infection rate (positive pools over mosquitoes tested) assumes one infected mosquito per positive
  pool and understates infection when pools are large or infection high, and the maximum likelihood estimate for pools
  of varying size does not (a Chicago gravid-trap study recorded MLE near 60 per 1,000 at the August peak while MIR
  stayed under 30); gravid females have taken a blood meal, so gravid-trap pools run hotter than CO2-trap pools; zone
  index thresholds of 0.5 and 0.75 trigger adulticide consideration in Colorado practice. The client's Layer 2 example
  "handling the data's real structure" is the lesson, carried here by the pooled structure of the tests.

## Default path

1. Read the surveillance protocol: CO2 traps run Monday and Tuesday nights, Culex females are pooled by site, night and
   species, and a trap-night lost to a fan, CO2 or battery failure is not effort.
2. Count each zone's Culex tarsalis and Culex pipiens females per functioning CO2 trap-night in week 32.
3. Take each zone's infection rate, by species, as positive pools over females tested, per 1,000 (the minimum infection
   rate), across all its week-32 Culex pools from both laboratories.
4. Index each zone as the sum over the two species of females per CO2 trap-night times infection per 1,000 / 1,000;
   fly the zone with the highest index.

Ends on: Riverside South.
Golden: Westbrook.

Figures below are the built pack's, asserted in `generator/checks.py`.

## Stump sentence

The natural index, each zone's Culex females per CO2 trap-night times the minimum infection rate of all its Culex pools,
names Riverside South for the aerial application, because counting one infected mosquito in every positive pool
understates the infection in Westbrook's pools of fifty, where more than half come back positive, and because the
gravid-trap pools of the two town zones carry the infection of females that have already fed into an index of the
females the CO2 traps catch.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection (serves Anomaly Detection):
  weekly mosquito surveillance flags every zone with positive pools, and the call separates the real hot spot from
  signals made by the pooling and by the trap that caught the females.
- **Domain test:** the deciding quantity is the vector index, infected host-seeking Culex females per CO2 trap-night,
  estimated the way arbovirus surveillance estimates it: CO2-trap abundance by species times the infection of those
  same females by maximum likelihood from pools of varying size.
- **Swap:** "which treatment zone gets the aerial application, by the estimated infected Culex females per CO2
  trap-night" with schools put in reads "which school gets the grant, by the estimated infected pupils per CO2
  test-night": a school has no pools of fifty, no trap-nights and no blood meals behind its counts, so the sentence and
  the analysis both stop making sense.
- **Layer 1:** the county laboratory's results arrive as tables in its PDF report (its reporting system); site codes
  were migrated on 15 June 2026 (the district's database migration, crosswalk shipped); species codes differ between
  the field database and the laboratories; field crews record the night a trap was set and laboratories the morning it
  was collected; inconclusive pools are retested with the final result in a later row (laboratory QA); trap-nights are
  lost to fan, CO2 and battery failures (field status codes). Nothing is placed to be caught; each resolves one way
  from the shipped protocol, crosswalk and dictionary.
- **Layer 2:** estimation_fit: the likelihood estimate of infection from pools of varying size, taken on the
  population the index counts (the females the CO2 traps caught), not the minimum infection rate across every pool.
- **Decisive step:** estimate each zone's infection by maximum likelihood from the pools of its CO2-trap females only,
  then multiply by their abundance per functioning CO2 trap-night; maximum likelihood alone names Old Town, the CO2
  pools alone name South Prairie, and only both together name Westbrook.
- **Not semantics:** every field (pool size, result, species, trap type, status) read correctly still leaves the
  minimum infection rate across all of a zone's pools, the common reading of an infection rate, on Riverside South; no
  code, unit or definition flips the call.
- **Not rule application:** no filed rule says how infection is estimated from pools or which pools stand for the
  CO2-caught females; the protocol says how pools are made and tested, and executing every filed step still files
  Riverside South.
- **Analyst test:** a strong analyst who reads every field and the protocol correctly computes infected Culex per CO2
  trap-night as each zone's CO2 catch rate times positive pools over females tested across all its Culex pools, and
  files Riverside South; maximum likelihood alone moves it to Old Town and CO2-trap pools alone to South Prairie.
- **Estimand:** `prompt.txt` asks for the estimated number of West Nile virus-infected Culex females collected per
  CO2 trap-night in each zone in the week ending 15 August 2026: population, the Culex tarsalis and Culex pipiens
  females caught in the zone's CO2 traps on its functioning trap-nights that week; outcome, infected with the virus;
  unit, females per trap-night; comparison, across the eight zones.
- **No decoy:** nothing is planted to be caught: no bulletin, memo, briefing or prior ranking computes an index; the
  county report gives pool results only; the human-case line list and the gravid-trap pools are real surveillance
  streams with their own uses.
- **No certified replay:** no published or certified index has to be reproduced and no back-test selects the method;
  the method is forced by the pools themselves.
- **Lesson:** a pooled-test infection rate is estimated by likelihood, on the population the index counts: reading a
  positive pool as one infected mosquito saturates in hot, large pools, and gravid-trap females carry their feeding
  history; no build on file estimates a rate from grouped tests or separates two sampling devices' populations.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 human cases this season by zone (Coulee Hills) | the case log is the risk signal everyone reads first | a zone column on every case | count cases by zone | none | none | a count | readable |
| R0 CO2 catch times the minimum infection rate of every pool (Riverside South, the default) | none needed | pool results beside pool sizes | the common reading of an infection rate | none | none | one ratio per zone | readable |
| R1 CO2-trap pools only, minimum rate (South Prairie) | the protocol says what each trap type collects | trap type on each collection, one join from a pool | stratify on a visible attribute | none | none | a filter | readable |
| R2 maximum likelihood on every pool (Old Town) | none | pool sizes beside results; gravid pools near nine in ten positive | the pooled-testing estimator arbovirus workers know | none | none | a likelihood estimate | readable |
| R3 (decisive) maximum likelihood on the CO2-trap pools only (Westbrook) | no sentence names an estimator, a pool population or what a gravid female has done | no column says which pools stand for the CO2-caught females; trap type sits on the collection, not the pool | each reflex lands elsewhere: likelihood alone on Old Town, trap-type strata with the minimum rate on South Prairie, catch alone on North Bottoms, infection alone on Maple Ridge | nothing shipped to back-test an index against | duplicates, keys and failures do not touch it | a likelihood estimate on a chosen subset of pools | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the week ending 15 August 2026" | trap-nights set Monday 10 and Tuesday 11 August (MMWR week 32) | trap-nights by pickup date (11 and 12 August) | Westbrook | same call: every week-32 trap-night is set and picked up inside 9 to 15 August (C1, asserted) |
| SF2 | "Culex females" | Culex tarsalis and Culex pipiens females | adding Culex not identified to species | Westbrook | same call: no unidentified Culex in the week-32 CO2 catches (C1, asserted) |
| SF3 | "CO2 trap-night" | a CO2-baited trap that ran from set to pickup (status OK) | every CO2 trap set, failures included | Westbrook | the protocol's definition of a trap-night (3.2); same call and figures either way (C1, asserted) |
| SF4 | "virus-infected" | a pool's final RT-PCR result, a retest replacing an inconclusive first result | the first result taken as final | Westbrook | the protocol's retest rule (5.3); same call either way (C1, asserted) |
| SF5 | "estimated number" | the maximum likelihood estimate of infection from the pools | the bias-corrected estimate (Firth), or the Jeffreys-penalised likelihood | Westbrook | same call, same one-decimal figures and the same whole-number flip rate (C3, asserted) |
| SF6 | summing the two species | each species' infection times its catch, summed | one Culex infection rate across both species times the total catch | Westbrook | same call, same one-decimal figures and flip rate (C3, asserted; pools are species-pure, so the species-wise sum is the natural reading) |
| SF7 | "per CO2 trap-night" | total females over total functioning trap-nights | the mean of each site's mean | Westbrook | same call and same one-decimal figures (C1, asserted) |
| SF8 | a trap's zone | the zone in the field database, which the 2026 register repeats | none | Westbrook | one zone per site, the two files agreeing on every site (C1, asserted) |
| SF9 | "the runner-up and its figure" | the zone second on the same estimate | the zone second on any other index | Westbrook | "its figure" is the same figure the question defines |
| SF10 | "the infection rate per 1,000 Culex females below which the chosen zone would lose the flight" | the chosen zone's infection among its CO2-caught Culex females at which its figure equals the runner-up's | a threshold per species | Westbrook | "per 1,000 Culex females" is one rate across the genus |
| SF11 | "collected" | females caught; males are counted apart and never pooled | males added to the catch | Westbrook | same call: CO2 catches of males are recorded separately and never pooled (C1, asserted) |
| SF12 | "the single aerial adulticide application" | one treatment zone, the contract's one block a week | a block split across zones | Westbrook | the contract: one block, one zone, one night |
| SF13 | (ask) "locally acquired human cases by onset from 1 June to 15 August" | confirmed and probable cases with onset in the window, exposed in the county, one per state case ID, by residence section on the 2026 zone map | the log's zone label, event date, every row, confirmed only | asks only | the 2026 zone map, the protocol's redraw date and the log's read-me (its zone list dates from March 2025; confirmed and probable both reported as cases); moves no main-call figure (asserted) |
| SF14 | (ask) "CO2 trap-nights run and lost to trap failures" | one record per trap and night, the 22 June import's second copies counted once, status OK run and the four failure codes lost | every row counted, or keyed deduplication on site and set date | asks only | protocol 3.3 ("A site runs one trap a night", Monday and Tuesday nights, with 3.5's enhanced nights) and 3.4's trap-night, with protocol 6.2 and the dictionary's `entered` line recording the second load of 22 June: every copy falls on a Wednesday, which the protocol schedules for no zone but Maple Ridge's enhanced fortnight of 17 to 25 June, and on no night its site ran, so no pair of records asks which reading of one night to keep (asserted per record in `checks.py` and `verify.py`) |

## Ladder

Built values (week 32, infected Culex females per CO2 trap-night unless stated), asserted in `generator/checks.py`.

| Rung | Analysis | Winner (figure) | Margin to second | Westbrook's place | Dies to |
|---|---|---|---|---|---|
| R-1 | human cases with onset this season, by zone | Coulee Hills (7) | 1.75 | 5th | the onsets sit in late June to late July, and Coulee Hills' week-32 CO2 pools carry 4.5 infected per 1,000 |
| R0 | CO2 catch per trap-night times the minimum infection rate of all the zone's pools (default) | Riverside South (2.28) | 1.27 | 4th (1.47) | its gravid-trap pools stand in for the CO2-caught females, and a positive pool is read as one infected female |
| R1 | CO2-trap pools only, minimum rate | South Prairie (1.71) | 1.17 | 2nd (1.47) | 42 of Westbrook's 70 Culex tarsalis pools are positive, 41 of them full pools of fifty: a positive pool holds more than one infected female |
| R2 | maximum likelihood, all pools | Old Town (2.98) | 1.20 | 3rd (2.33) | gravid-trap females have already fed: Old Town's gravid pools carry 43.2 per 1,000 against 9.1 in its CO2 pools, Riverside South's 34.5 against 6.8 |
| R3 (decisive) | maximum likelihood on the CO2-trap pools only | Westbrook (2.33) | 1.29 | 1st | none |

- **Position:** Westbrook 4th on the default, never first on an intermediate rung, second on one (R1, by 1.17).
- **Dominance:** under the decisive method Westbrook leads the default's Riverside South by 1.30 infected females per
  trap-night (2.33 against 1.03); Riverside South's carried advantage under the default is 0.81 (2.28 against 1.47);
  1.59 times, over the 1.2 floor.
- **Grid (estimator by pools):** minimum rate on all pools Riverside South; minimum rate on CO2 pools South Prairie;
  likelihood on all pools Old Town; likelihood on CO2 pools Westbrook. Reflex cells: catch alone North Bottoms (258.9
  Culex females a trap-night); infection alone Maple Ridge (28.3 per 1,000 against Westbrook's 23.4); positive pools
  counted Old Town (116); share of pools positive Old Town (0.60); cases Coulee Hills; one Culex rate in place of the
  two species lands on the same cells; a trap-night of either kind with every pool Old Town. Every cell but the last
  rung names a wrong zone; the answer is the grid's extreme cell, so a half-applied correction cannot fall onto it.
- **Worth on the graded quantity:** the default files Riverside South at 2.28 (true 1.03 on the decisive method);
  likelihood alone files Old Town at 2.98 (true 1.07); CO2 pools alone file South Prairie at 1.71 (true 1.81, second);
  Westbrook's own figure moves from 1.47 on the default to 2.33.
- **Bins:** under the likelihood estimate, the bias-corrected (Firth's modified score) estimate, the
  Jeffreys-penalised likelihood and a single Culex rate, Westbrook sits in 2.3 (2.26 to 2.33), South Prairie in 1.8
  (1.78 to 1.81) and the flip rate in 18 per 1,000 (18.0 to 18.3), at least 0.014, 0.03 and 0.2 inside their bins;
  Westbrook first by 1.25 or more under each. The bins were bought by draw (`world.SALT`) and by Westbrook's fifteen
  CO2 sites; the likelihood estimate's own bias is what separates the variants.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the Culex tarsalis and pipiens females caught in each zone's CO2 traps on functioning trap-nights set 10 and 11 August 2026 | the prompt's estimand with the protocol's trap-night; C1 on unidentified Culex and males (none in the week's CO2 catches) |
| 2 Unit of account | infected females per trap-night, one figure per zone | the prompt names the unit |
| 3 Attribution window | MMWR week 32, 9 to 15 August | C1: every week-32 trap-night is set and picked up inside the week |
| 4 As-of dating | laboratory results final at the extract (county report 14 August, district results through 15 August) | C1: every week-32 pool carries a final result |
| 5 Version basis | the final result after a retest | the protocol's retest rule; C1 on the call |
| 6 Denominator | functioning CO2 trap-nights | the protocol's definition; C1 with failures counted |
| 7 Weighting | total females over total trap-nights | C1 against the mean of site means |
| 8 Window length | one week | the prompt |
| 9 Boundary inclusivity | no trap set on 9 or 15 August | C1 by schedule (Monday and Tuesday nights only) |
| 10 Rounding path | each figure from unrounded catch and infection, rounded once to one decimal | the prompt's closing sentence; asserted |
| 11 Tie-break | none needed | margins asserted (1.25 or more) |
| 12 Maturity and censoring | no week-32 pool awaiting a result | C1, asserted |
| 13 Order of operations | species summed after their own estimates, or one genus rate | C1, asserted |
| 14 Row order | none | n/a, nothing order-dependent |
| 15 Duplicate resolution | a retest replaces an inconclusive result; no pool is listed twice | protocol 5.3; C1 |
| 16 Identity normalisation | species written CXTA and CXPI in the field database and in full by both laboratories | the data dictionary's species table; C1 |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | females per pool, per trap-night, per 1,000 | units in the data and the prompt; C4 against per-pool reading |
| 19 Code and status semantics | status OK is a trap-night; FAN, CO2, BAT and STOLEN are failures; NS is a trap not set | the dictionary; never the stump |
| 20 Integerisation | none in the main call | n/a |
| 21 Clause scope | "CO2 trap-night" covers the CO2 traps only | the prompt's own words |
| 22 Forward window contents | the application flies on 20 August on the week-32 state | filed: the question judges on week 32; no driver needed for later weeks |

## Literal reader

Executed word for word, the estimated number of virus-infected Culex females collected per CO2 trap-night in week 32
is each zone's females per functioning CO2 trap-night times the infected share of those same females; the only
measurement of that share is the RT-PCR result of the pools made from them, and a positive pool of up to fifty holds
an unknown number of infected females, so the estimate is the one that does not fix that number at one. Every
reading in the fork table lands on Westbrook (SF1 to SF12); the easy answer, Riverside South, comes from an easy method
on the same estimand (a positive pool read as one infected female, and every pool in the zone taken for the
CO2-caught females), never from another reading.

## Oracles

None. No shipped file prints an infection rate, a minimum infection rate, an index or a ranking of the zones: the
county laboratory's report lists pools and results, the district laboratory's table the same, and the human case log
is a line list. Nothing ties only under the golden or only on the wrong path.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, each zone's locally acquired human cases by onset, 1 June to 15 August | 8, whole numbers | a measure every zone carries that the call does not turn on | the memo reads the season's human toll beside the week's mosquitoes | D2, a label stored before a silent switch: the county epidemiologist's log carries each case's zone from the district's zone list of March 2025 (its read-me says so), and the district redrew its zones by section on 1 May 2026 (protocol 2.2); eight cases live in sections that changed zone, moving every zone's count (Coulee Hills -2, South Prairie +1, Riverside South +2, Airport East -1, Old Town -1, North Bottoms -1, Maple Ridge +1, Westbrook +1 between the label and the map) | three presumptive viremic donors (North Bottoms, Westbrook, South Prairie) with the donation date as the event date; two travel-acquired cases (Old Town, Maple Ridge); three notifications ruled out on convalescent serum (Maple Ridge, Riverside South, Airport East); two patients notified again by the neighbouring county (Coulee Hills, Westbrook); two late-May onsets whose event date is the June specimen (Coulee Hills, South Prairie) | case log (zone, residence section, onset, event and report dates, classification, presentation, exposure, state case ID), the register's Zone sections sheet, protocol 2.2 (3 files, 10 columns) | the log's zone label with every exclusion right (every zone off by its net move); label and every row (every zone off); the 2026 map and every row (every zone off); event date for onset (Coulee Hills and South Prairie off); the answer | a county epidemiologist's working log keeps the zone list she was sent, and a district redraw by section is announced in the district's own protocol |
| B, each zone's CO2 trap-nights run and lost to trap failures, 1 June to 15 August | 16, whole numbers | the audit trail of the effort every index stands on | the memo's surveillance-effort table | D1, the same records under two key schemes: the second load of 22 June brought the June Tuesday nights in again under the new site IDs with the pickup morning in the set-date field (206 records, entered that day, as protocol 6.2 and the dictionary's `entered` line record; neither says the copies repeat nights or how the load dated them), so every site's early-June nights stand twice, the copy dated a day later with the same status and catch; deduplication on site, date and catch keeps both | Maple Ridge's genuine Wednesday and Thursday nights of 17 to 25 June, the fortnight after its first positive pool of 10 June (protocol 3.5); removing every night off Monday and Tuesday clears the copies and over-cleans Maple Ridge; a June failure in every zone's copied nights; NS rows (traps not set in the holiday week) are neither run nor lost; gravid traps are not CO2 traps | trap_nights (status, set date, entered), catches, sites, status_codes, protocol 3.3 to 3.5 (3 files, 9 columns) | every row counted (run and lost high in every zone); keyed deduplication on site and set date (no copy collides, so every zone stays high); exact duplicates removed (the same); nights off Monday and Tuesday removed after the copies (Maple Ridge low by its enhanced nights); NS counted as lost (every zone's lost high); the answer | a migration followed by a re-import keyed by pickup date, beside a genuine enhanced-trapping fortnight |
| Chart, each zone's cases by week of onset | 4 named parts | the memo's exhibit of A | the reader sees where and when people fell ill | inherits A's device | inherits A's hazards | A's path | A's stops on every bar | a public health memo's standard exhibit |

- **Main population zero-counts:** the main call reads the week-32 CO2 trap-nights, their catches and their pools; no
  re-imported copy, enhanced night, NS row, case or zone label sits in it (asserted in `checks.py`); the case log and
  the June records are read by no main-call figure.
- **Hazard table:** donors move A for North Bottoms, Westbrook and South Prairie; travel for Old Town and Maple Ridge;
  ruled-out notifications for Maple Ridge, Riverside South and Airport East; repeat notifications for Coulee Hills and
  Westbrook; May onsets for Coulee Hills and South Prairie (every zone has at least one, and the label stop misses
  every zone with them left in); NS rows move B's lost column in every zone; Maple Ridge's enhanced nights of 17 to 25 June move B's run column for
  Maple Ridge only.
- **Referee:** the protocol's trap-night definition (3.4) arbitrates B's run and lost columns and ties no figure by
  itself; the log's read-me arbitrates what a case is.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A cases by zone | every exclusion right, onset used, zone from the log's label | every zone off by its net move between the March 2025 list and the 2026 map | miss |
| B trap-nights run by zone | exact-duplicate removal on site, date and catch, NS excluded | every zone high by the second load's Wednesday rows | miss |
| B trap-nights lost by zone | the same, failures read from status | every zone high by the failures those rows repeat | miss |
| Chart bars | A's cracker path by week of onset | every zone's bars off in the week a moved case falls | miss |

Mirror leakage: about 6 per cent of the ask weight (the chart's title, axes and legend; every count misses on the
default path's ask handling, which shares the cracker's).
Pair ceiling: about 33 (the cracker at about 49 with the call and the chart's presence parts, the mirror at about 17).

## Build record

- **Generator:** `generator/build.py` (world, ecology, records, cases, docs, pack, analysis, deliver, checks, verify,
  metadata, postprocess); 12 files, 6 formats; the field database holds 9,104 trap-night records (206 of them the 22
  June second load's copies), 57,074 catch rows, 35,573 pools and 34,469 tests; the county report lists the 1,155
  week-32 county pools over 21 pages; the case log holds 37 notifications.
- **checks.py:** 939 assertions with the three-rules block: R1 every pool ships with its size and result, and no file
  states a rate, an index or a ranking; R2 the pack's four ladder cells equal the clean truth's, and failed traps
  counted, first results taken as final and males added each leave the call; R3a the easy route on the clean truth
  files Riverside South; R3b the decisive step alone files Westbrook, the CO2 pools alone South Prairie, the likelihood
  alone Old Town; R3c no file recommends a zone and the county report names none.
- **verify.py:** independent, from target/ only (SQL over the database, pypdf over the report, the pooled likelihood
  maximised directly): 1,385 checks; Westbrook 2.328, South Prairie 1.811, flip 18.29 per 1,000; 25 cases; 1,878
  CO2 trap-nights run and 57 lost; 206 copies from the second load, each on a day the protocol schedules no trap and
  on no night its site ran; every workbook row and the memo's figures as stated.
- **Two builds byte-identical**; target.zip cut from the final build; `figures_check.py` 42 of 42; `precut.py` 49 of
  49; containers clean on the scrub audit (target and golden).
- **Guard:** heart WARN (objective, shape and Gate G overuse, a pick after a pick; nearest driver 0.05, task450 v2);
  surface promotes task186 (two apart, on the gap key `rule` and the decision type `pick_one_of_n` only; the Gate G
  mechanisms, patterns and drivers differ: there each station's price change was judged against its own changes when
  nothing happened, here an infection rate is estimated from grouped tests and carried onto the population one
  sampling device collects; surface 0.075, the corpus's 43rd percentile, and the two worlds share no file, format or
  noun).

## Judge record

- **Pass 1 (stage 4):** DETERMINISTIC, SOLUTION_WRONG, FIX_NOW on one write-up figure. The thread recomputed the call
  from the bundle (Westbrook 2.328, South Prairie 1.811, every other zone at or below 1.07), the flip rate (18 per
  1,000), Westbrook's 99.0 Culex females per CO2 trap-night and its 23.5 per 1,000, every zone's human cases and every
  trap-night figure. It ruled the minimum infection rate the only open reading of the prompt and the data's own
  refutation of it (60 per cent of Westbrook's pools of fifty positive, so the minimum rate is a floor), and reported
  the bootstrap probability that Westbrook leads South Prairie at about 0.85 on a point-estimate question. Gate G:
  method_or_model_selection, analytical_non_defect, no surface read, no sole data defect. Gate H: domain pass, layers
  pass, decisive step analytical. Its finding: step 8 said "452 records" where the 22 June import entered 432 (452 is
  the count of records sharing a site and set date). Fixed in the write-up; nothing in the prompt, the data or any
  graded figure moved.
- **Pass 2 (after the write-up fix, before the recut):** DETERMINISTIC, APPROVE, no fix. It reproduced the call, both
  figures, the flip rate and every ask figure, rated the likelihood estimate forced ("the prompt asks for an estimated
  number and a minimum is not one"; pool sizes of 50 against 10, 60 per cent of Westbrook's pools positive, protocol
  3.2 on gravid females), and put the cluster bootstrap probability that Westbrook leads at about 0.88. Gate G
  method_or_model_selection, analytical_non_defect, no surface read, no sole data defect; Gate H domain, layers and
  decisive step all pass.
- **Its soft spot, closed by the recut:** no shipped document said a second load had happened, so the judge reached
  the count from the content match and the Monday and Tuesday schedule alone. Protocol 3.3 now pins one trap a site a
  night and 6.2 records the 22 June load with the dictionary's `entered` line, and the load now brings back the June
  Tuesday nights only, so every copy sits on an unscheduled Wednesday and no two records describe one night two ways.
  Neither document says the copies repeat nights or how the load dated them, so the cracker's keyed deduplication
  still keeps all 206 and misses every zone.

## Reader record

- **Pass 1 (partial, the documents only):** nothing quoted for question 1; no file ranks the zones; nothing reads as
  the answer; question 6 analytical. Its finding, fixed: the protocol was dated 27 April 2026 and spoke in the past
  tense of the 1 May redraw and the 15 June migration, so it is now issued 27 April and revised 26 June, with the
  revision in its own history table.
- **Pass 2 (the whole bundle):** question 1 none ("the prompt names only the metric"); question 2 none (the flight log
  lists past blocks only); question 3 the register, the dictionary and the manifest, each a register a district keeps;
  question 4 none; question 5 the prompt's estimand with protocol 3.4, 3.6 and 4.3, none naming an estimator;
  question 6 "an analytical choice: the pooled-infection-rate estimator with unequal pool sizes, scaled by trap-night
  exposure"; question 8 nothing machine-made or out of fiction.
- **Its question 7, the finding that recut the data:** on ask B the second load's records were open to three readings
  (keep the first entry, keep the second, keep both), because 226 of the 432 copies landed on a night the site had
  already run with a different status and catch. The second load now brings back the June Tuesday nights only: every
  copy falls on a Wednesday, which the protocol schedules for no zone but Maple Ridge's enhanced fortnight, and on no
  night its site ran, so one reading survives. Asserted per record in `checks.py` and `verify.py`.

## Leak review

`leak.py --asof 2026-08-17`: REVIEW, no LEAK. Each line's disposition:
- Sweep 2, `trap` in the protocol and the dictionary: the field's sampling device (CO2 traps, gravid traps,
  trap-nights), declared under `field_terms` in `metadata.json`; no file name carries it.
- Sweep 3, 2.3 in the agreement and the protocol is clause 2.3 of each; 186 in the county report is site RC-186.
- Sweep 4, stump-paragraph terms in the protocol, the county report, the agreement and the dictionary (zones,
  laboratories, species, positive, caught): the field's ordinary vocabulary; none names an estimator, a pool
  population or what a gravid female's infection means for an index (asserted in `checks.py`); the prompt's first
  sentence carries the decision's own nouns.
- Sweep 6, zone names beside numbers in the register (sections, coordinates), the zones file (section counts), the
  protocol (clause numbers), the case log (one row per case), the database (site rows) and the flight log (past
  blocks): none ranks the zones on infected Culex per CO2 trap-night in week 32.

## Pre-ship check

- **Call:** fly Westbrook on Thursday 20 August 2026, 2.3 estimated virus-infected Culex females per CO2 trap-night in
  the week ending 15 August (2.3275 before rounding); South Prairie second at 1.8 (1.8112); the flight lost below 18
  per 1,000 Culex females (18.29), against Westbrook's own 23.5.
- **Default path:** each zone's CO2 catch per trap-night times the minimum infection rate of all its pools files
  Riverside South at 2.28, with Westbrook fourth at 1.47.
- **The three rules on the built pack:** the deciding quantity is the field's own vector index, estimated the way
  arbovirus surveillance estimates infection from pools of varying size; Layer 1 (the county laboratory's results in
  a PDF, the June migration and its second load, species codes, set against pickup dates, retested pools, failed
  trap-nights) complicates the work and carries nothing decisive, each item asserted neutral for the call; the
  decisive step is analytical, and `checks.py` executes the easy route on the generator's clean truth and files
  Riverside South with every field read and every filed rule applied.
- **Gates:** 939 generator assertions with the R1 to R3c block, 1,385 independent checks from the bundle alone, two
  byte-identical builds, target.zip cut from the final build, figures_check 42 of 42, precut 49 of 49, voice-check
  PASS, scrub clean (target and golden), leak.py REVIEW with no LEAK, guard heart WARN and surface one promoted pair
  answered.
- **Deliverables:** aerial_spray_recommendation.pdf (the call, how the figure is built, why two shortcuts give another
  zone, the two leading zones' table, the flip point, the source line), zone_season_2026.xlsx (Zones, Cases by week,
  Notes), human_cases_by_zone.png (eight panels, Westbrook's bar set apart); target.zip, 12 files.
- **Card current:** answer, answer source, spine rows 57,074.

## Tried and rejected

- Seed AD11's own world (route-origin paging at a cloud platform, RPKI invalid against not-found): no client domain's
  Anomaly Detection task type does routing analysis, and General Statistics' multiple testing would make network
  operations a backdrop; rejected at the draw on the domain rule.
- Political science conflict event data (attacks on civilians estimated from the overlap of the commission's monitors
  and the media, multiple systems estimation): capture-recapture reads the same in epidemiology with two surveillance
  lists, so the swap test survives; rejected at the draw.
- Pharmacovigilance signal triage (co-reporting and masking in disproportionality): the comparison has to be filed for
  determinism and filing it names the decisive step; rejected at the draw.
- Legionnaires' source attribution (plume touchdown and where cases were exposed): root cause, not anomaly detection,
  and practice disinfects every tower in the area at once; rejected at the draw.
- Influenza positivity standardised by days from onset to swab: a measurement-condition normalisation, the lane's third
  after task180 (noise) and task187 (turbulence); rejected at the draw.
- A resident-weighted index (traps sited on the marsh rather than among residents): an estimand that names residents
  makes the solver ask where they live (readability test 1); rejected as the decisive step at the draw.
- Westbrook with eleven CO2 sites (22 trap-nights a week): the likelihood estimate's own bias put the likelihood,
  bias-corrected and Jeffreys-penalised figures up to 2.4 per cent apart, straddling a one-decimal bin in most draws;
  four sites added in the zone's untrapped sections (30 trap-nights) and the draw chosen with every variant inside one
  bin, asserted.
- A second load that re-entered every 1 to 14 June night (432 records, keyed by the pickup morning): half of them
  landed on a night the site had already run, with that night's own status and catch, so the ask had three defensible
  readings (keep the first entry, keep the second, keep both) and the leak reader found the fork. The load now brings
  back the June Tuesday nights only (206 records), every one on a Wednesday the protocol schedules for no zone but
  Maple Ridge's enhanced fortnight.
