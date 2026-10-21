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

Re-answered on 2026-10-21 against the measured Gate F failure, with the verdict on each line rather than
the claim the build shipped with. `generator/family_screen.py` is the measurement; six of the thirteen
lines fail.

- **Task type:** PASSES. epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection
  (serves Anomaly Detection): weekly mosquito surveillance flags every zone with positive pools and the
  call separates the real hot spot from signals made by the pooling and by the trap that caught the
  females.
- **Domain test:** PASSES on the quantity, FAILS on the estimator. The vector index, infected host-seeking
  Culex females per CO2 trap-night, is the field's own measure of human risk and no other field's nouns
  carry it. But the clause that made it the field's own analysis, "estimated by maximum likelihood from
  pools of varying size", carries nothing: on the shipped draw all 12 licensed pooled-prevalence
  constructions, the closed form at the mean pool size and the Poisson approximation among them, name the
  same zone.
- **Swap:** PASSES. "Which treatment zone gets the aerial application, by the estimated infected Culex
  females per CO2 trap-night" with schools put in reads "which school gets the grant, by the estimated
  infected pupils per CO2 test-night": a school has no pools of fifty, no trap-nights and no blood meals
  behind its counts, so the sentence and the analysis both stop making sense.
- **Layer 1:** PASSES, and is confirmed by the Gate F reader rather than contradicted by it. The county
  laboratory's results as tables in its PDF, the 15 June site-ID migration and its 22 June second load,
  species codes differing between the field database and the laboratories, set dates against pickup
  mornings, retested inconclusive pools, trap-nights lost to fan, CO2 and battery failures: the reader
  cleared the whole layer, keying the week-32 PDF of 1,155 pools with no mismatches, and the call did not
  move. That is what Layer 1 is for and it is all it did.
- **Layer 2:** FAILS. The family that was supposed to carry it has no spread. Enumerated once the filed
  WHAT is read, the licensed constructions for the infected share of a pooled-tested population (maximum
  likelihood for unequal pool sizes, Firth, Jeffreys, three posterior summaries, the equal-size closed form
  at the mean size, the complementary log-log approximation, Chiang and Reeves, a binomial GLM with a
  cloglog link and a log pool-size offset, and maximum likelihood on the full pools alone) return **1
  distinct designated zone of 12** on the shipped draw and a mean of **1.15 over 20 redraws**. Where the
  family does split, 3 of 20 redraws, the separation collapses with it (lever over ceiling 0.11 and 0.13).
  So there is no methodological choice here that flips the call.
- **Decisive step:** FAILS, in both halves. Half one, use the CO2-trap pools and not the gravid-trap pools,
  is the population, which `determinism-check` section 1 requires filed, and the pack files it three times
  over: protocol 3.1 says CO2 traps "draw females looking for a blood meal", 3.2 says gravid-trap females
  are "looking for water to lay their eggs in, each of which has already taken a blood meal", and the
  prompt itself says "per CO2 trap-night". Half two, estimate the infected share rather than count one
  infected mosquito per positive pool, is pointed at by protocol 4.1's "pools hold up to 50 females", and
  once taken it has the zero spread Layer 2 records above. The reader named 3.1, 3.2, 3.6, 4.1 and the
  prompt's own wording, which is readability test 1 five times.
- **Not semantics:** PASSES. Every field (pool size, result, species, trap type, status) read correctly
  still leaves the minimum infection rate on South Prairie and, taken over every pool the zone sent, on
  Riverside South; no code, unit or definition flips the call. This was never the build's problem.
- **Not rule application:** FAILS, and the number is the reason. The question is not whether a filed rule
  names the method, which none does, but whether anything is left to decide once every filed rule is read,
  and nothing is: **the measured spread of the estimator family the filed rules leave open is 0 distinct
  designated zones over 12 licensed constructions** (1.15 mean over 20 redraws), while the same family
  spreads the printed call figure over **4 values, 2.1 to 2.4, an exact spread of 0.3503 against a printed
  unit of 0.1, which is 3.5 printed units**. The residue the filed WHAT leaves moves the graded figure and
  never the call, which is the worst of both gates at once: Gate F reads the step as a reflex and Gate C
  reads the figure as forked.
- **Analyst test:** PASSES as a sentence, FAILS as a prediction. It is true that the minimum infection rate
  over every pool files Riverside South at 2.28 with Westbrook fourth at 1.47, and `checks.py` executes it
  on the clean truth. It is also measured that a strong analyst does not go there: the easy route is wrong
  in 18 of 20 redraws and the reader read 4.1 and 3.2 and stepped over it on the first pass.
- **Estimand:** PASSES. `prompt.txt` asks for the estimated number of West Nile virus-infected Culex
  females collected per CO2 trap-night in each zone in the week ending 15 August 2026: population, the
  Culex tarsalis and Culex pipiens females caught in the zone's CO2 traps on its functioning trap-nights
  that week; outcome, infected with the virus; unit, females per trap-night; comparison, across the eight
  zones. Filed literally, and that is the trouble: filing it fully is mandatory and it leaves the method
  with nothing to choose between.
- **No decoy:** PASSES. Nothing is planted to be caught: no bulletin, memo, briefing or prior ranking
  computes an index, the county report gives pool results only, and the human-case line list and the
  gravid-trap pools are real surveillance streams with their own uses.
- **No certified replay:** PASSES. No published or certified index has to be reproduced and no back-test
  selects the method.
- **Lesson:** FAILS. "A pooled-test infection rate is estimated by likelihood, on the population the index
  counts" is a reflex rather than a lesson: 12 of 12 licensed constructions file the committed zone, and a
  binomial GLM with a cloglog link and a log pool-size offset, which is the house reflex for a pooled
  prevalence, files all four committed graded figures exactly. A model learns nothing from getting this
  right that it did not already do by habit.

## Readability screen

Re-run on 2026-10-21 against the measurement. The decisive rung's verdict moves from `silent` to
`readable`: test 1 fires five times (protocol 3.1, 3.2, 3.6, 4.1 and the prompt's own "per CO2
trap-night"), test 3 fires once (a binomial GLM with a cloglog link and a log pool-size offset is the
house reflex for a pooled prevalence and files all four committed figures), and test 6 fires once (the
construction is an identity in a two-group-by route, correlation +0.9972). `precut.py` therefore refuses
the note on the `decisive rung silent` row, which is the correct signal: the rung is dead.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 human cases this season by zone (Coulee Hills) | the case log is the risk signal everyone reads first | a zone column on every case | count cases by zone | none | none | a count | readable |
| R0 CO2 catch times the minimum infection rate of every pool (Riverside South, the default) | none needed | pool results beside pool sizes | the common reading of an infection rate | none | none | one ratio per zone | readable |
| R1 CO2-trap pools only, minimum rate (South Prairie) | protocol 3.1 and 3.2 say what each trap type draws and that a gravid female has already fed; the prompt says "per CO2 trap-night" | trap type on each collection, one join from a pool | stratify on a visible attribute | none | none | an identity in positive pools per trap-night, correlation +0.999976, maximum absolute difference 9.7e-03 | readable |
| R2 maximum likelihood on every pool (Old Town) | protocol 4.1: pools hold up to 50 females, so a positive pool cannot hold exactly one | pool sizes beside results; gravid pools near nine in ten positive | the pooled-testing estimator arbovirus workers know | none | none | a likelihood estimate | readable |
| R3 (decisive) maximum likelihood on the CO2-trap pools only (Westbrook) | five sentences compose into it: 3.1 and 3.2 give the population, 3.6 the denominator, 4.1 the pool sizes, and the prompt the trap type | trap type sits on the collection, one join from the pool | a cloglog GLM with a log pool-size offset files all four committed figures; 12 of 12 licensed constructions name the zone | nothing shipped to back-test an index against | duplicates, keys and failures do not touch it | an identity in (pools per trap-night) times minus the log of the negative share, correlation +0.9972, 18 of 20 redraws | readable |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the week ending 15 August 2026" | trap-nights set Monday 10 and Tuesday 11 August (MMWR week 32) | trap-nights by pickup date (11 and 12 August) | Westbrook | same call: every week-32 trap-night is set and picked up inside 9 to 15 August (C1, asserted) |
| SF2 | "Culex females" | Culex tarsalis and Culex pipiens females | adding Culex not identified to species | Westbrook | same call: no unidentified Culex in the week-32 CO2 catches (C1, asserted) |
| SF3 | "CO2 trap-night" | a CO2-baited trap that ran from set to pickup (status OK) | every CO2 trap set, failures included | Westbrook | the protocol's definition of a trap-night (3.4); same call and figures either way (C1, asserted) |
| SF4 | "virus-infected" | a pool's final RT-PCR result, a retest replacing an inconclusive first result | the first result taken as final | Westbrook | the protocol's retest rule (4.3); same call either way (C1, asserted) |
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
| 5 Version basis | the final result after a retest | the protocol's retest rule (4.3); C1 on the call |
| 6 Denominator | functioning CO2 trap-nights | the protocol's definition; C1 with failures counted |
| 7 Weighting | total females over total trap-nights | C1 against the mean of site means |
| 8 Window length | one week | the prompt |
| 9 Boundary inclusivity | no trap set on 9 or 15 August | C1 by schedule (Monday and Tuesday nights only) |
| 10 Rounding path | each figure from unrounded catch and infection, rounded once to one decimal | the prompt's closing sentence; asserted |
| 11 Tie-break | none needed | margins asserted (1.25 or more) |
| 12 Maturity and censoring | no week-32 pool awaiting a result | C1, asserted |
| 13 Order of operations | species summed after their own estimates, or one genus rate | C1, asserted |
| 14 Row order | none | n/a, nothing order-dependent |
| 15 Duplicate resolution | a retest replaces an inconclusive result; no pool is listed twice | protocol 4.3; C1 |
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

- **Pass 3 (the recut bundle, the recorded pass):** DETERMINISTIC, APPROVE, no fix. It settled the second load from the
  files alone: the 206 records entered on 22 June are the Tuesday nights of 2 and 9 June shifted a day (catches match
  572 of 572 and 589 of 589 rows against 50 to 60 for any other pair of nights, status and crew 174 of 174 on the CO2
  records), no copy lands on a night its site ran, and protocol 3.3, 3.5, 4.1 and 6.2 each exclude them as runs, so
  "one reading is forced" and the only rival, counting as entered, contradicts four clauses. It reproduced the call
  (Westbrook 2.3275, South Prairie 1.8112, every other zone at or below 1.07), the flip rate (18.3, so 18 per 1,000),
  both single-rate and Firth variants in the same one-decimal bins, every human case count and every trap-night figure.
  Gate G method_selection, no surface read, no sole data defect; Gate H domain, layers and decisive step all pass.
  Its residual risk, recorded and accepted: no file names the estimator, which is the stump ("a minimum-infection
  index is a count, not an estimate, and saturates" at 42 of Westbrook's 70 pools positive).

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
- **Judge:** pass 1 FIX_NOW on one write-up count, pass 2 DETERMINISTIC APPROVE, pass 3 DETERMINISTIC APPROVE on the
  recut bundle with the trap-night ask settled from the files alone.
- **Gates:** 939 generator assertions with the R1 to R3c block, 1,385 independent checks from the bundle alone, two
  byte-identical builds, target.zip cut from the final build, figures_check 42 of 42, precut 49 of 49, voice-check
  PASS, scrub clean (target and golden), leak.py REVIEW with no LEAK, guard heart WARN and surface one promoted pair
  answered.
- **Deliverables:** aerial_spray_recommendation.pdf (the call, how the figure is built, why two shortcuts give another
  zone, the two leading zones' table, the flip point, the source line), zone_season_2026.xlsx (Zones, Cases by week,
  Notes), human_cases_by_zone.png (eight panels, Westbrook's bar set apart); target.zip, 12 files.
- **Card current:** answer, answer source, spine rows 57,074.

## Gate F re-screen

The measurement that spends architecture 1, run on the generator's clean truth before any design work, by
`generator/family_screen.py` (two runs byte-identical; 20 redraws salt the night-level draw for all eight
zones). It answers the Gate F failure the wave 8 blind reader measured: a Sonnet reader at medium effort,
holding only a fresh unzip of `target.zip`, `prompt.txt` and the figure names, took 18 of 18 call figures
and 60 of 82 ask figures, filed the zone, the flight date, the rate to four decimals and the flip point,
rebuilt infected females per CO2 trap-night species by species with the maximum-likelihood rate for pools
of unequal size, scored both upper rungs in its own words, and named protocol 3.1, 3.2, 3.6, 4.1 and the
prompt's own wording as what sent it there.

**Screen 1, the estimator family.** Once the filed WHAT is read, the only thing left open is how the
infected share of a pooled-tested population is estimated. Twelve constructions a competent analyst would
use: maximum likelihood for unequal pool sizes (the golden), Firth, Jeffreys, posterior mean under a
uniform and under a Jeffreys prior, posterior median, the equal-size closed form at the mean pool size,
the complementary log-log approximation, Chiang and Reeves size-stratified, a binomial GLM with a cloglog
link and a log pool-size offset, maximum likelihood on the full pools alone, and maximum likelihood by
size stratum recombined.

| Graded figure | Printed unit | Distinct values over the 12 | Exact spread | In printed units |
|---|---|---|---|---|
| designated zone | n/a | **1** (Westbrook) | 0 | 0 |
| runner-up | n/a | **1** (South Prairie) | 0 | 0 |
| the call's figure | 0.1 | 4 (2.1, 2.2, 2.3, 2.4) | 0.3503 | **3.5** |
| the runner-up's figure | 0.1 | 3 (1.7, 1.8, 1.9) | 0.1140 | 1.1 |
| the flip rate | 1 | 2 (18, 19) | 1.151 | 1.2 |

Four of the twelve file all four committed figures, and one of those four is the cloglog GLM, which is the
house reflex for a pooled prevalence and returns the golden to four decimals (2.3275). The shipped
`checks.py` enumerated three members, maximum likelihood, Firth and Jeffreys, which are three score
variants of one likelihood and therefore agree by construction; the posterior summaries (2.4) and the
closed-form, Poisson and stratified routes (2.1 and 2.2) were never in the enumeration, so the APPROVE
never tested them. That is `stumping` 1.2's warning executed: count the family wide enough to include the
forms that skip the conditioning the decisive step adds.

**Screen 2, the algebra on the cheapest licensed construction.** The one-group-by route to the call, in
one line, with no pool size in it:

    index(z) = sum over the two species of (CO2 pools / CO2 trap-nights) times (minus ln(share of pools negative))

The designed construction is an identity in it: correlation **+0.997243** over the eight zones, the same
designated zone and the same runner-up, three of the four committed graded figures (Westbrook 2.2 against
2.3, South Prairie 1.8, flip 18), and over 20 redraws it names the golden zone in **18 of 20** and the
golden runner-up as well in **17 of 20**. Why it is an identity, which is the clause the design never
wrote down: with tested females T equal to the sum of the pool sizes, T times the maximum likelihood
estimate tends to (pools) times (minus ln(1 minus the positive share)) as the pool size grows, so the pool
size cancels out of the leading term. The laboratory split into pools of 50 and pools of 10, the
per-species abundance table and the whole unequal-pool-size likelihood are decoration on the graded
figure. Worse one rung down: the minimum infection rate index is **exactly** positive CO2 pools per
functioning trap-night (correlation +0.999976, maximum absolute difference 9.7e-03, the residue being
pools made from failed trap-nights), so rung 1 is one group-by and one divide. What separates rung 1 from
rung 3 is only the saturation multiplier minus ln(1 minus q) over q, a monotone function of the share of a
zone's pools that came back positive, and q is itself one group-by.

**Screen 3, the lever against the ceiling, over 20 redraws.** The lever is the separation the decisive
step buys on the graded quantity; the ceiling is the spread the licensed family puts on the same figure.

| Measurement | Value |
|---|---|
| lever (graded units) | mean 0.513, range 0.020 to 1.298 |
| ceiling (graded units) | mean 0.330, range 0.075 to 0.730 |
| ceiling in printed units of the call figure | mean **3.3**, 3.5 on the shipped draw |
| lever over ceiling | mean 1.77, range 0.11 to 4.73 |
| redraws where the family splits on the designation | **3 of 20** (mean 1.15 distinct zones) |
| redraws where the one-group-by route names the golden zone | 18 of 20 |
| redraws where the easy route is wrong | 18 of 20 |

One dial, both ends, and the two ends are the same end. In the 17 redraws where the separation is real the
family is unanimous, so nothing methodological decides the call; in the 3 where the family splits the
separation has collapsed to 0.11 and 0.13 of the family's own spread, so the call is seed-hostage. There is
no setting of this world at which the estimator choice both matters and is determinate. The design bought
the agreement deliberately (`## Tried and rejected`: four CO2 sites added to Westbrook so every variant
sits inside one bin), which is exactly the trade that killed it: the convergence Gate C rests on is the
reach Gate F pays.

**Verdict: measured refusal.** The decisive step has no estimator content, so architecture 1 is spent and
is not resumed. Nor can the ladder be re-sited on this pack: the only other candidate decisive steps here
are which pools stand for the CO2-caught females (the population), which trap-nights count (the
denominator and the unit) and which window (the window), and every one of them is a part of the estimand
that `determinism-check` section 1 requires filed, so filing it is rule application and leaving it unfiled
forks the main call. Re-rooting the ladder inside this world is therefore not available; the number needs a
stage 1 re-root onto a quantity whose construction the data forces, with the forcing input in a second
file at a finer grain than anything the pool table carries.

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
- Resuming architecture 1 after the wave 8 Gate F failure by moving the protocol's filed definitions (the plan in `pipeline.json`'s resume line): refused on measurement before any design work. The decisive step's estimator family returns 1 distinct designated zone of 12 licensed constructions on the shipped draw and 1.15 over 20 redraws, so the step is a reflex whatever the protocol says and rewording 3.1, 3.2, 3.6 and 4.1 cannot put content into it; the same family spreads the printed call figure 3.5 printed units, so the clauses were load-bearing for Gate C and not for Gate F (`generator/family_screen.py`, `## Gate F re-screen`).
- Re-siting the decisive step onto which pools stand for the CO2-caught females, or onto which trap-nights count: each settles a part of the estimand (the population, the denominator and unit), which `determinism-check` section 1 requires filed, so filing it is rule application and leaving it unfiled forks the main call; dead on the WHAT screen with no hardening available.
- Keeping the unequal-pool-size likelihood as the decisive construction on any redraw of this world: the lever and the ceiling are one quantity. Over 20 redraws the family splits on the designation in 3, and in those 3 the separation is 0.11 and 0.13 of the family's own spread; in the other 17 the family is unanimous. No setting makes the estimator choice both matter and be determinate, so the architecture is spent rather than mistuned.
