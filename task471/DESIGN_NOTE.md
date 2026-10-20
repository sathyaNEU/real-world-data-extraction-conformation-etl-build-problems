# task471 design note: the 2027 enrolment campaign's organisers on the census-day adults not on the roll

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

Architecture 5, drawn 2026-10-20 after architecture 4 (the register over-coverage audit) was spent at Gate F. Card
`.claude/skills/fingerprint/cards/task471.json` (v5), registered 2026-10-20T17:17:37Z; guard check WARN only.

- **Pairing.** Survey Research & Official Statistics / census-register-administrative-data-quality (client domain
  survey-research-official-statistics), objective Data Extraction & Conformation (ETL): the National Statistics Office
  conforms the 2025 Census, its Post-Enumeration Survey, the vital and border statistics and the Electoral Commission's
  roll at census day into the enrolment-gap file the Commission shares its 2027 campaign organisers on.
- **Shape 05, allocation to a fixed total.** 150 organisers shared among the 16 regions in proportion to each
  region's adults not on the roll (estimated adults usually resident on census day less electors on the roll that
  day), largest remainders, at least two each. Criteria: each region's organisers and adults not on the roll (32),
  the call, the chart's named parts, the asks.
- **Decision.** allocation_to_total, answer unit count, question form how-many; forum the Commission
  (committee_or_panel), forcing event the 2027 general election (vote_or_meeting), org family
  research_or_statistics_office, stakeholder the office's manager of population estimates (statistical_office_head).
- **Strategy.** population_selection, decisive generator G8 (reachability against magnitude): the people both counts
  reach are not the people there are; Gate G method_or_model_selection; Layer 2 family field_method, pattern
  own:dual-system-correlation-bias-corrected-by-demographic-analysis-sex-ratios.
- **Data-native sentence.** In a census the people a count misses are not missed at random: men aged 18 to 49 with no
  settled household are missed by the census and by its coverage survey alike, so the survey's recount, which the
  dual-system estimate treats as an independent second count, cannot see them, and only the population that births,
  deaths and border movements fix can; and because the gap the Commission allocates on is a small difference of two
  large counts, the men left out move the organisers between regions.
- **Sources.**
  - Client card census-register/1 (dual-system estimates within post-strata, after erroneous enumerations) is the
    textbook route and this build's default path; the decisive step is the judgment that route takes for granted (the
    census and the survey miss people independently) and the data settle (`stumping` 1.3; the Layer 2 library header).
  - `measured-drivers.md`, held group: the construction a solver never considers is outside its hypothesis space; a
    coverage survey's reader looks inside the survey, and the benchmark that settles the dependence sits in the vital
    and border statistics.
  - This lane's record: readers missed every call that turned on a structure of the process no document names
    (task472, task473, task475, task476, task477) and landed every call that turned on a textbook design correction a
    document made readable (this slot's v1, v3 and v4).
  - task448 and task473 (capture measured on an overlap; a catch rate by the trait's level): differentiation lines on the
    card. Here no capture rate is measured for the people both counts miss; their number comes from a sex ratio.
- **WARNs answered.** overuse.objective: the ETL lane is this author's lane. repeat.gate_g and overuse.gate_g against
  task474 v4: the honest key for a call pinned by the data's internal consistency; task474's driver (renewal churn in
  payment claims) shares nothing else. repeat.question_form against task474 v4: the call is a count per region.
- **Personas** (`guard.py names --geo "New Zealand" --seed 471`): Chelsea Buckley, Bryan Tapp.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own moves, a round-trip itinerary fare read as a one-way fare and the New York
  airports left as three markets: data semantics and a market definition (the estimand's unit), so neither may decide;
  kept as Layer 1 and as ask devices.
- 2026-10-18, at the draw: a windshield census (cards put on every car parked in the lots at sweep times), whose cards
  over-represent long stays in proportion to their length: population_selection, banned against task245 at the draw,
  and the label is not moved to pass the guard; replaced by the entry-plaza handout, a different mechanism (replies
  censored by the collection close, which thins the long stays instead of inflating them).
- 2026-10-18, at the draw: the fare premium over a log-log fare-distance benchmark, decided by retransformation bias:
  generic econometrics, and a clinic's charges against a severity curve read the same (swap test fails).
- 2026-10-18, at the draw: the three markets with the highest premium in thin ticket-sample cells, decided by
  shrinkage (the winner's curse): the shrinkage method is not forced by anything filed, a coin flip for determinism.
- 2026-10-18, at the draw: leakage read from an agency ticket dataset whose capture depends on the sales channel,
  measured where the ticket sample sees everything: the same lesson as task448 and task470 (capture by unit measured
  on the overlap).
- 2026-10-18, at the draw: a departure-lounge survey with a fixed quota of interviews per flight (unequal inclusion):
  a ratio within each destination sidesteps it, and by house precedent (task452) a design-weight stump is
  population_selection, banned at the draw.
- 2026-10-18, at the draw: capacity-censored (spilled) demand on full flights to the hubs: the demand turned away is
  model-dependent and every demand model is a fork.
- 2026-10-18, at the draw: the share of one-way tickets that are residents' trips (a one-way ticket's origin is not
  its traveller's home): turns on reading what the ticket origin field means, data semantics.
- 2026-10-18, at the draw: business travel by market from the fare-class proxy corrected for its false positives
  (Rogan-Gladen): the lesson task456 teaches (an imperfect record's false positives subtracted, not only its misses).
- 2026-10-18, at the build: the party verbatim beside the coded party in the cards file, with a filed rule sending the
  analyst to the verbatim for parties of nine or more: the rule pointed every careful solver at the verbatim column,
  where the sums sit in plain view; the verbatims moved to their own file and the cap dropped.
- 2026-10-18, at the build: home ZIPs keyed with a plus-four on 16 per cent of cards: matched as keyed they moved every
  trips figure out of its hundred, so a Layer 1 item carried figure difficulty; cut to a realistic 0.3 per cent and
  asserted neutral, with the two-county ZIP made a small rural office and the repeated batch chosen so its second copy
  moves no figure out of its hundred.
- 2026-10-18, at the build: passengers on the default path's weights ranked Washington, Phoenix and Tampa, the golden's
  three, so ranking on passengers was a shortcut to the call; the winter markets' parties cut to couples and singles
  (1.65 to 1.75) and Myrtle Beach's summer family trips raised to 3,000, so passengers on any weighting carry Myrtle
  Beach.
- 2026-10-18, at the build: the first realisation (seed 471) put New York within 1.12 of the third market once the party
  draw moved onto each card; New York and Dallas set lower in the world and a seed search run over 60 worlds; seed 504.
- 2026-10-18, at stage 4: seed 504's world, where New York led Dallas for the first market left out by 2 per cent and
  a reweighting or a dropped batch could swap them (reader round 1); the handout coverage reworked plaza by plaza and
  day by day with lot choice independent of the stay, and a 120-world search run with the fourth against the fifth at
  1.07 or more; one world passed, seed 512.
- 2026-10-18, at stage 4: the passengers device cut one way (a sum written on the card coded as its first number):
  reader round 2 read Q4 in the verbatims against `party` and recoded every party, the sums added.
- 2026-10-18, at stage 4: the same device cut both ways (the parties written with who they cover coded right, so adding
  every number written counts them twice): reader round 3 recoded every party right. Both cuts are mirror devices: the
  verbatims are documented beside the coded column (methods report 4.2), so reconciling them is the cracker's reflex,
  and no reading of Q4 the frozen documents leave open is both determinate and missed by a careful parser.
- 2026-10-19, re-root tried on paper: the same parking survey with the third pick held unless its lead over the first
  market left out clears twice its design-based standard error (cards clustered by handout day, weighted by the return
  window). Measured on the v1 pack it cannot bind: 73,909 returned cards put Phoenix, Tampa and Washington each 3.5
  standard errors clear of New York on the weighted card-level variance and 2.3 to 3.4 clustered by day; binding it
  would need a tenfold smaller sample and same-day group travel, a planted structure, and the clustering unit itself
  is arguable when the waves are consecutive days. Dropped before any data was cut.
- 2026-10-20, re-root: architecture 1 (the parking card survey, replies censored by the collection close) spent at
  Gate F, every reader landing the call, with its ask device a mirror device; by the author's rule (no retirement)
  architecture 2 is a fresh world in the least-drawn ETL task type, its decisive step one the record does not display.
- 2026-10-20, at the draw: repeat candidates who saw the anchor items on an earlier attempt, left in the equating
  sample: an anchor-contamination screen beside task450's, and the sample definition has to be filed anyway (a
  convention), which files the step; kept only as the filed sample (first attempts), with no exposure in the data.
- 2026-10-20, at the draw: Tucker against Levine under a large cohort difference (the anchor's reliability): the two
  differ by less than their sampling error at the cut and nothing a pack can carry forces one, a fork.
- 2026-10-20, at the draw: 2025 responses re-scored as a labelled trend sample: the label names the drift check, so
  the organ announces the step; replaced by the contractor's validity papers, which its QC summary reports only as
  agreement rates.
- 2026-10-20, at the draw (prototype 1): an anchor of 15 multiple-choice items and two of the three written
  assignments, heavier in written work than the test: the golden's methods split (Tucker 56 against chained
  equipercentile 57) and missed the generating truth; the anchor made proportional (20 items and one assignment, 44
  per cent written by points, as the test is).
- 2026-10-20, at the draw: filing the program's equating method (Tucker) in the 2025 technical report to close the
  equipercentile spread: its literal execution on the anchor as scored is the default path's cut, an official decoy;
  the method stays unfiled and the world is tuned so that Tucker, Levine and chained linear (each at three synthetic
  weights) and chained equipercentile agree on one cut with margin.
- 2026-10-20, stage 3: WA2's validity papers scored by the 2025 leaders' consensus (an audit set): `heart` blocked
  ban.calibration and ban.artifact against task473 once task249 was marked spent; redrawn as June 2025 responses
  carrying the score both of their 2025 reads gave, the two scoring regimes' overlap on the same responses and the
  operational metric the 2025 anchor scores are on (validity sample drawn on its own stream so the shift sits mid-bin:
  0.98 anchor points, raw 49 with 0.38 and 0.37 of margin, every rung and set unchanged).
- 2026-10-20, stage 4: architecture 2 itself, the rater-severity shift on the anchor's written assignment measured on
  the validity papers and taken out before the link. The judge (v2r1) found it DETERMINISTIC on the main call, but its
  Gate G disposition was SEND_BACK (planted_defect_flip, surface_read_rejection, sole_data_defect yes): on consistent
  scoring the anchor as scored is right and the task collapses, so the stump is catching that the as-scored anchor
  misleads. Gate H passed only as analytical (borderline planted). Both scored readers missed the call on the drop-WA2
  rung and all 32 ask figures, but a measurement bias in recorded values is a defect to catch, not an analysis on
  honest numbers. Spent; architecture 3 is a fresh draw on honest data.
- 2026-10-20, at the architecture 3 draw: a joint replacement registry whose earlier hips were back-loaded on each
  hospital's joining only if still in place, read by delayed entry. task265 already spends exactly that insight, so it
  was dropped before registering.
- 2026-10-20, at the v3 build: the parcel list alone (and the parcel-drawn share scaled to the wells on the lists)
  named the golden six by coincidence, because the parcel-only wells carried nearly every exceedance; Alderwick placed
  as a county whose permit-only wells run high (its parcel list alone gives 79), so no single list lands the six.
- 2026-10-20, at the v3 build: each county's estimate as a graded figure: the design-based estimators that all name
  the six differ by up to 59 wells in one county (Dunmere 164 to 223), so no figure is determinate; the estimate is
  charted and the graded grid is each county's verdict and its wells on the lists.
- 2026-10-20, at the v3 build: the retest ask's routing on one border town per county could not move every county's
  figures (several counties had no border retests); each county's border town drawn from its two smaller towns, and the
  search also kept the portal-only path off every figure, so the mirror keeps none of the 32.
- 2026-10-20, at the v3 build: results printed at 10.00, or Kinsale results between 44.0 and 44.27 mg/L NO3, would
  split the standard's "more than 10" from "10 or more" and the design report's factor from the fact sheet's; every
  result within 0.1 of the standard moved clear of it on its own side (SF1, SF12).
- 2026-10-20, stage 4: architecture 3 itself, the county estimate over two overlapping lists sampled separately,
  each tested well counted at one over its chance of selection from either list. The judge (run v3r1) found it
  DETERMINISTIC and APPROVE (Gate G method_or_model_selection, analytical_non_defect; Gate H analytical), but both
  scored readers landed the call and all 32 ask figures: reader A by the inclusion probabilities, reader B by the
  post-stratified estimator. The design report must describe the two lists and their separate draws for the estimate
  to be determinate, and once described the dual-frame estimator is executed as a work order; the routing county on
  the retest requests fell to a consistency check of the request's county against the first kit's. Spent on Gate F.
- 2026-10-20, at the v4 draw: a coarse privacy-preserving linkage key whose chance agreements inflate each county's
  linked count, corrected by the expected chance matches: the lesson task468 v4 teaches (false links for common
  identifiers), shipped in this lane today.
- 2026-10-20, at the v4 draw: the dual-frame world with a nonresponse weighting class added: stacks a second step on a
  rung both readers already executed, and the weighting class rests on a missing-at-random assumption a judge reads as
  open.
- 2026-10-20, at the v4 draw: an annual quantity read from a seasonal record: an annual estimand announces the season,
  and the driver is task476's (onset season against inspection timing).
- 2026-10-20, at the v4 draw: persons registered at crowded addresses as a second absence stratum: for the audited
  persons the address context would have to ship as a column or an address-member table, either of which displays it.
- 2026-10-20, at the v4 draw: school proficiency rates from point-estimate classification against expected counts
  (plausible values): the estimand would have to name an expected count, which files the method.
- 2026-10-20, at the v4 draw: chained volume components summed: reads as a unit's semantics (chained dollars are not
  additive), so the decisive step would be data semantics.
- 2026-10-20, at the v4 draw: the register's registration lag completed by its delay distribution: maturity_censoring,
  banned at the draw against task250.
- 2026-10-20, at the v4 build: the asks' first devices (rejected messages sent again, late reports, former residents'
  deaths): every one is executed by a careful solver who joins the hub's acknowledgements and applies the filed
  residency condition, so the cracker landed both asks; re-sited onto departures and deaths the register annulled as
  entered in error, found only in the persons' own histories.
- 2026-10-20, at the v4 build: the year-end batch as the deaths' primary: determinate only with a filed local-time
  convention, which a careful solver executes; kept as a hazard shared by both asks.
- 2026-10-20, at the v4 build: persons removed after an address investigation who had died before it (registered when
  they died), to make residency two-sided: with the year-end batch and the annulled deaths a three-error reading
  cancelled back to the golden in 21 of 24 municipalities; removed, residency now one-sided.
- 2026-10-20, at the v4 build: a third ask, former residents living abroad on 1 January 2026, with non-resident records
  never closed for persons who came back: determinate only with a filed re-registration condition, which hands the
  device over; dropped.
- 2026-10-20, at the v4 build: the national circular migrants' gaps of one to six years: the seasonal-work towns'
  long-gap migrants then sat in a seven-person cell of stay by earlier departure by first settlement, and that cross
  filed six with a municipality 0.1 from the line; national gaps widened to 1 to 14 years, every cross now files nine.
- 2026-10-20, stage 4: architecture 4 itself, the register's erroneous enumerations post-stratified by the migration
  career rebuilt from the event history. Both scored readers on target.zip b6990395f2efabc2 landed the call
  (score_reader exit 1 on each, 2 of 2 call figures). Reader A fitted a logistic model with a returnee flag and years
  since the last IMM; reader B built cells of country of birth by years since the last arrival by an earlier
  emigration. Report 5's "the respects that bear on it" plus 12,000 audited persons with histories invites testing
  which characteristics predict absence, and time since immigration and return migration are the field's textbook
  covariates, so the step was the reflex rather than the analysis a solver skips. Both readers also executed both
  asks' devices: the annulled departures and deaths came from a check of the hub's log against the register's ANN
  events, and the year-end batch from converting UTC to CET. They missed the 48 ask figures only by counting messages
  sent in 2025 whatever the event date, a reading the v4 spec's "departures abroad in 2025 ... from the messages ...
  sent in 2025" left open once "with a departure date in 2025" was dropped (a fork, not a device). Spent on Gate F.
- 2026-10-20, re-root: architecture 4 (the register over-coverage audit) spent at Gate F when both readers
  post-stratified the audit on the field's textbook covariates; architecture 5 is a fresh world (a census and its
  post-enumeration survey) whose decisive step is a judgment the textbook estimator takes for granted.
- 2026-10-20, at the v5 draw: council membership set by population bands on the census-day population, a threshold
  scorecard over the districts near a band edge: shape 10 banned against task251, and the same call shape as v4.
- 2026-10-20, at the v5 draw: one representation quota for every district, set as the lowest that keeps the councils'
  total within a statutory cap: a near-uniform correction is absorbed by the quota itself (it rises with the
  populations), so most districts' councillors do not move and only the setting discriminates.
- 2026-10-20, at the v5 draw: seats apportioned among districts by a divisor method: a relative allocation that a
  correction proportional to each district's men aged 18 to 49 barely moves (0.05 of a seat for a six-seat district).
- 2026-10-20, at the v5 draw: an anchor block moved to the end of a speeded new form, not-reached responses scored
  wrong: item response equating again in this slot (architecture 2's family, anchor contamination), and a not-reached
  code read as missing is data semantics.
- 2026-10-20, at the v5 draw: a scheduled-date field the office re-aligns once a case starts, which back-tests
  perfectly on closed cases: the re-alignment is a field reading, and the guard's validated-decoy shape.
- 2026-10-20, at the v5 draw: decisive generator G16 (method selection) and G12 (absence of record against record of
  absence): the population/G16 signature is spent in six builds and G12 is banned against task250; G8 (reachability
  against magnitude) states this step honestly and is unspent with this gap.
