# task214 design note

Wave 8, Anomaly Detection & Diagnostics. A new draw in another client domain: the Larix world of seed AD37 is set
aside (## Tried and rejected) and nothing of that seed is used.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task214.json`, architecture v1, drawn and filed 2026-11-07. Guard:
  WARN only (org family government_agency overused; objective anomaly-detection 4 of the last 12, the lane's own
  objective; Gate G decomposition_attribution 6 of the last 12, kept because the decisive step does attribute each
  case's exposure among the assets that delivered its water, and no other key is honest). Nearest drivers 0.07 and
  under.
- **Pairing:** client domain Epidemiology & Public Health, task type `disease-surveillance-outbreak-anomaly-detection`
  (AD, DQ in the taxonomy), drawn as the client domain itself. Least spent on AD: one card in the cell (task188,
  pooled mosquito tests). Barred domains avoided: General Statistics & Data Science (task212), Banking (task213),
  Pharmacology (task211), Human Factors' safety-incident-error-analysis (task210).
- **World:** a fictional New Zealand district: the district council's drinking-water supply (six service
  reservoirs, sixteen supply zones fed through feed and link mains, eleven normally closed boundary mains between
  zones of different reservoirs) and the regional public health service. Spring 2027: a cryptosporidiosis outbreak in
  two zones that the supply-zone register puts on reservoir R4. The decision, on Tuesday 19 October 2027: which asset
  the council takes out of service before the 26 October renewal of the feed main to those zones. The call faces
  forward: the renewal will back-feed the same zones again.
- **The mechanism (clean truth):** while a zone's feed main is shut for a repair, crews keep it in supply by opening a
  boundary main from a neighbouring zone, so for those days the zone drinks another reservoir's water. Boundary main
  BM3 runs through a grazed paddock with a damaged air valve; when it carries water within two days of heavy rain,
  runoff is drawn in. On 4 to 6 October 2027, after 94 mm in three days, FM11 was shut for a burst repair and zones Z11
  and Z12 were back-fed through BM3 from Z05 (reservoir R2's network). Cases follow each zone's actual water through
  each case's own incubation period (1 to 14 days, median 7).
- **Golden:** each asset's attack rate, cases per 100,000 resident-days its water reached, with each case's incubation
  window laid over the supply path its zone actually had on each day (rebuilt from the valve operations through the
  network model): BM3, far ahead of everything else. **Default path's answer:** R4, the register's source for the two
  worst zones.
- **Shape:** 18 (hypotheses against evidence): each candidate asset with its cases carried and its attack rate, the
  call, the runner-up and the gap; arithmetic in ## Ladder at stage 2.
- **Strategy:** decomposition_attribution (each case's exposure attributed among the assets its water passed through
  on the days its incubation window covers). Layer 2 family estimand_identification, pattern
  `own:exposure-traced-through-network-operations`. Card: gap time then population, generators G5 (provision
  elsewhere) then G3 (record versus operation), Gate G decomposition_attribution, decision pick_one_of_n.
- **Data-native sentence:** in this network a zone's water comes from whichever reservoir the valves connect it to on
  the day, and crews back-feed a zone through a boundary main whenever its own feed main is shut, so the supply-zone
  register (the normal arrangement) and the water people drank part company exactly on repair days, which no
  notification, register or zone table records.
- **Abstraction sentence:** an event's source is the one whose output reached the event's area during the event's own
  exposure window under the configuration a switch log sets, not the one a register of normal assignments names. Not
  writable against an approved build: task162 (approved) reads valves in a water network too, but its insight is a
  control valve acting only while its inlet runs above its setting (pressure-conditional leakage); task156 (NZ
  wastewater) is infiltration below a water table; task181's tray-to-steriliser tracing finds a faulty processing
  step and judges units net of it, while here the register's own source is innocent and the decisive object is which
  path the water took in each case's window.
- **Furniture (live window task211 to task213):** forum committee_or_panel, executive_team, line_manager_or_team held;
  forcing events purchase_order_or_contract, season_or_peak, period_close held; org families
  hospital_or_health_provider, logistics_or_3pl, software_or_platform held. Drawn: forum regulator_or_inspector (the
  medical officer of health directs the supplier), forcing event incident_or_complaint (the outbreak), org family
  government_agency (the honest label; WARN answered above).
- **Guard probes (2026-11-07):** gap population with G3 and decomposition_attribution BLOCKs test.same_driver against
  task399 and older builds, and same_puzzle_older against task270, task275, task450 and task468; gap time with G5
  then G3 clears. Question form `which` warned against task212; the decision locates a source on the network, so the
  form is `where`.
- **Personas:** `guard.py names --geo new-zealand --locale en_NZ --seed 214`: Anna Gullery (medical officer of
  health), Rhys Cook (network operations lead). Elizabeth Morgan was drawn first and dropped (first name in task128).
- **Sources for the levels (screen 1):** cryptosporidiosis incubation 1 to 12 days, about 7 on average (US CDC,
  Cryptosporidiosis clinical overview; Health New Zealand, Communicable Disease Control Manual); New Zealand
  notifications about 25 to 30 per 100,000 a year with a spring peak at calving and lambing (ESR, Notifiable diseases
  in New Zealand annual reports); a damaged air valve in a grazed field drawing contamination into a main, about
  16,000 properties under a boil-water notice and more than 100 confirmed cases (Brixham, Devon, May 2024, UKHSA and the
  Drinking Water Inspectorate); a Cryptosporidium outbreak in a New Zealand town supply with about 70 cases
  (Queenstown, September 2023, Health New Zealand); water main failures of the order of 10 to 20 per 100 km a year
  (Water New Zealand, National Performance Review); average household size about 2.6 (Stats NZ, 2023 Census).
  Measured on the clean truth: 35 to 72 notified outbreak cases among about 10,000 back-fed residents (0.4 to 0.7 per
  cent, against Brixham's 0.4), 2 to 9 sporadic cases in the review window.

### The five go/no-go screens (clean truth, `generator/screens.py`, seeds 1 to 40)

1. **Levels and lead:** golden BM3 equals the truth 40 of 40; lead over the runner-up at or above 1.2 in 40 of 40,
   minimum 3.80, median about 5.7 (runner-up LM12 or FM11 by redraw).
2. **The golden's own method:** BM3 under every variant 20 of 20 on each block: incubation weights lognormal (median 7)
   or flat over 1 to 12, 2 to 14, 3 to 10 and 1 to 14 days; the served window opening 1 August or 1 September;
   residents or properties as the denominator (one constant per zone, same call).
3. **First look** (the zone with most cases, then its register source) wrong 40 of 40 (R4).
4. **Careful readers**, each wrong 40 of 40: (a) attack rates by zone and by register source, R4; (b) constructing:
   the onset-day path and the report-day path (FM11 or LM12, because the back-feed ended before nearly every onset),
   the dated event (the burst repair on FM11, repair-site ingress), the nearest reservoir to the cases and to the two
   worst zones (R4); (c) per-record zone-by-week cells on every joinable attribute (R4; the valve operations join to
   no case attribute); (d) mechanism-naming: waterborne attack rates by supply zone through the register (R4) and
   post-repair ingress at the burst (FM11); (e) literal replay of every stated fact, R4.
5. **Literal execution of the filed WHAT** (the asset whose water reached the cases, taken through the register as
   written) names R4, 40 of 40; the golden needs the step the WHAT does not tell anyone to compute: each zone's
   supply path day by day from the valve operations through the network model.

### What each spent AD driver spends (`guard.py mechanisms --objective anomaly-detection`, one line each)

task25 a second source's missing inflow completes a forward ranking; task28 the reachable share of a flagged excess;
task33 forward yield of a shift still in force, truncated at a filed intervention; task48 a gap visible only at a
two-sided pair grain; task54 loss borne by every unit in custody; task68 like-for-like change across identity
successions; task76 a look-back class with zero conversion; task85 each unit's own observation window from an
intermediary's lead time; task103 contacts fanned out through authorisations against records of service; task104 a
self-adapting scorer replayed at an unrun setting; task119 failed waits the unit could have shortened; task183 parts
that keep failing defeat trailing rates; task180 detection thresholds riding a daily noise cycle; task185 a device
conversion sized at the value; task186 shared local cycles inflating a within-unit test; task187 Jensen over a curved,
capped response; task188 pooled-test infection rates by maximum likelihood; task189 left-censoring under
instrument-specific limits; task195 a paired difference's uncertainty against overlapping intervals; task193 room for
an ordering set by first exposure in the window; task192 a validation batch covering only the window's opening;
task197 a unit's response to a shared signal along a scheduled trajectory; task196 two capture channels, the second
produced by the first; task194 a coding lag read through two vintages; task182 length-biased snapshots (lineage: a
lagged driver response, a background under a running source, residual deterrence screened dead in architecture 8);
task198 a value capped at the lesser of ask and entitlement; task199 events recorded only where watchers filed;
task201 exposure-time missing an opening interval set by the number of reporters; task184 a saturating container
indicator (lineage: interval-censored cycles); task204 a transport rate from a unit's own unsteady balance; task181 a
shared upstream processing step (trays through one steriliser) adding risk to the cases it handled (lineage: two
pooled sources, an arrival-delay nowcast, near-repeat runs, crossings, residence against workplace); task191
informative censoring of slow-closing rare outcomes; task125 scheduled occasions at a bordering site moved by the coming
calendar; task190 found errors scaling with second-record coverage; task210 a per-pass hazard set by the sun against
each heading; task211 a transient after each member's first encounter with a changed version, by supply point;
task212 each case's load from the cases scanned into its container after it; task213 control shown by flows that
return across two ledgers to their source. None reads where a network's operations sent each case's exposure.

### Slot screens (`guard.py slots`, mechanism nouns then setting nouns, before any harness)

- Seeding and carriers (driver sentence; care home, agency staff, shared staff; introduction, seeding, importation):
  no slot holds the insight; task234 mentions care-home outbreaks in passing. Set aside anyway on paper: every carrier
  design reads as task181's shared step adding risk to the cases it handles.
- Patrol, deterrence, Koper, hot spot: task182 architecture 8 screened residual deterrence and it failed; closed.
- Cryptosporidium, waterborne, supply zone, treatment works, valve, boil water; reservoir, attack rate, incubation,
  back-feed, district metered, exposure window: no slot. Supply zone and water supply: task271 v4 (insurance claims
  carried by a water authority's supply zone, a per-unit rate carried to new homes) and task402's rejected fluoridated
  zones; neither is this insight.
- Resume lines read (every slot touching the cell, the objective or the client domain): task188, task234, task236,
  task242, task248, task301, task304, task501, task149 (epidemiology), task156 (NZ water, forecasting), task211,
  task212 (in flight; its filed lowest-BIC criterion is not reused here), task213. None screened this mechanism.

## Tried and rejected

- 2026-11-07, paper: data skew read from input size (a column; the Mantri reflex reaches it).
- 2026-11-07, paper: upstream lateness from the dependency log as the decisive step (one join; critical path is the
  field's own method, so it sits at rung 1).
- 2026-11-07, paper: the trigger's launch delay as the decisive step (a stated rule executed: rule application).
- 2026-11-07, paper: the backup's remote-read penalty (a locality column makes it schema-readable).
- 2026-11-07, paper: credits avoided across families through the dependency graph (the step settles which credits
  count, the population: the WHAT screen kills it).
- 2026-11-07, paper: the cap as concurrent slots in correlated bad nights (a stated cap executed: rule application);
  commit-lock waits (indeterminate); cold image pulls on deploy days (an aggregate spike around dated events).
- 2026-11-07, prototype v1 to v8 (scratch t214/proto): the golden's before and after windows starved on fail-slow
  hosts; the naive culprit rules (slowest co-tenant, contemporaneous magnitude) landed the call while disk-bound
  shards of the winning families shared fail-slow hosts with each other; fixed by the platform's own placement
  (anti-affinity within a job, the search index on its dedicated storage nodes) and workload mix (CPU-bound general
  families), not by wording.
- 2026-11-07, candidate 1 SPENT at screen 4(c), never registered: the reverse-causality straggler (a heavy
  card-settlement shard slows its own host's co-tenants while it runs, so the bad-machine check credits a backup
  that would rerun the same work; the golden read the host's co-tenants before the shard started and after it
  ended). v9, 20 redraws: golden = clean truth = payments clearing + regulatory reporting 20/20, lead min 1.197,
  median 1.391; credits paid, every late job with a straggler, the textbook replay, the host check, magnitude,
  slowest co-tenant, per-record host x hour residual and host-night straggler count all wrong 20/20; but the
  per-record reader with host x night cells, reading the residual as the shard's own work, reached the golden set
  20/20, and the golden's both-sides variant held only 14/20. v10 (skew 3 to 18 times, fail-slow 4 to 72 hours):
  host x 4-hour and x 8-hour residual readers 20/20, host x night 16/20, golden lead median 1.158 (14/20 under
  1.2), both-sides variant 0/20. Why it dies: the information that decides (the host's state outside the
  straggler's run) is a host-by-time aggregate, and any cell wider than a heavy shard's run and narrower than a
  fail-slow episode separates the two; no realistic setting separates them in time without starving the golden's
  own before and after test. A copy escapes exactly the host component, so a correct host-versus-rest
  decomposition by cells is a correct method, which is the blind route.
- 2026-11-07, queued on paper after candidate 1 (not yet screened): (a) a commit wait behind another family's write
  to a shared output table read from heartbeat trajectories (risk: output-table x time cells recover it); (b)
  shard-level input waits through the catalogue's shard-to-part mapping (risk: the field's critical path at shard
  level is a reflex); (c) a self-dependent job whose late night pushes the next night's start (risk: a careful
  dependency replay is the field's method). Preferred next: transient stalls (escaped by any fresh copy) against a
  shard's heavy nights set by its clients' own cycles through the client-to-shard table (repeated by every copy),
  which no host-time cell, day-of-month interaction or lag reveals (pipeline.json resume).
- 2026-11-07, the Larix world SET ASIDE (seed AD37 dropped) before any second candidate: its only honest Anomaly
  Detection home is General Statistics & Data Science's exploratory-data-analysis-distribution-assessment, held by
  task212 in flight; the draft card reached it through the house label business-operations-analytics, which clears
  ban.pairing only by its label, and a card is never relabelled to pass a ban. Candidate 1's measured death stands
  above. The build moves to Epidemiology & Public Health, a new world and dataset (## Draw); world.py, method.py and
  screens.py are replaced with the new world's harness.
- 2026-11-07, paper, at the new draw (each before any harness): residual patrol deterrence for hot-spot selection
  (dead in task182 architecture 8); care-home outbreaks seeded by staff working across homes, and float nurses
  carrying colonisation between wards (both read as task181's shared step adding risk to the cases it handles, and
  outbreak counts per home are too sparse for a 19 of 20 separation); a surgeon's learning curve counted across a
  national audit (healthcare delivery, more spent, and a career total is an aggregate view a strong reader takes
  first); physiotherapy visits after each patient's functional plateau (the plateau threshold is either filed, rule
  application, or open, a fork); releasees' loss of tolerance behind an overdose excess (excluding releasees lands the
  call); susceptible reconstruction after past epidemics (a time-since-epidemic marker reaches it); a food lot on the
  shelf by first-in first-out stock rotation (the practice is either filed, a replay, or withheld); a pool's
  contaminated days (pool-by-day cells reveal it); continuous blending at zone boundaries from inlet meters (a
  zone-by-hour aggregate of one table).
