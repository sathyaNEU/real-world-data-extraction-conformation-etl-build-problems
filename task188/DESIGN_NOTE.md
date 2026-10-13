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
- **Shape 01** (a ranked list, each candidate): the call, the chosen zone's index, the runner-up's and the gap (4); each
  zone's index and infection rate (16); a chart with named parts (4); the asks (human cases by zone and type, the
  season's trap-night effort) and the files (3 or more). Criteria arithmetic: 27 before the asks.
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

Every figure is the prototype's until the generator asserts the built values.

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
