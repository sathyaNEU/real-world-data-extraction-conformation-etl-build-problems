# task471 design note: the 2027 small-municipality supplement on the register's adjusted resident population

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task471.json`, architecture v4, registered 2026-10-20T14:00:47Z after a
  pull. Lineage: v1 (the route pitch, Gate F), v2 (the licensure form, Gate G), v3 (the dual-frame well survey, Gate F).
  - Guard: WARN only.
    - ETL in 7 of the last 12: the lane's objective.
    - Gate G method_or_model_selection repeats task474 v3 and runs in 8 of 12: which post-strata carry a register's
      absence process is a model chosen on honest data, not a planted figure.
    - designation_set repeats task474 v3: the decision designates the municipalities that qualify.
  - Differentiation lines against task470, task167, task268, task30, task31, task448, task500, task53, task57, task69
    and task76 (the signature population, E, method_or_model_selection is spent in older builds; each line names how
    this driver differs: an over-count removed at audit rates set by a clock and a migration history).
  - Personas from `guard.py names --geo netherlands --seed 471`: Ilse Spreeuw (head of population statistics at the
    Bureau), Luka Bosman (the audit's methodologist), Kay Wolfswinkel (analyst at the ministry's municipal finance
    directorate). Nobody from v1 to v3 is reused.
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / ETL.
  - The integration: a municipal population register extract, its event history, the national Register Coverage Audit
    with its working extract of the audited persons' register records and histories, the merger crosswalk and the
    ministry's delivery specification, conformed into one adjusted-population file.
  - The deciding quantity: each in-play municipality's adjusted resident population on 1 January 2026, its register
    count less the registered persons estimated, from the audit, not to have been living there; a register's erroneous
    enumerations estimated within post-strata, the task type's own statistical object.
- **World:** an unnamed EU country modelled on the Netherlands. The National Bureau of Statistics (population
  statistics division) delivers adjusted populations to the Ministry of the Interior's municipal finance directorate.
  - Municipal Fund Regulation 2027: the small-municipality supplement goes to municipalities whose adjusted resident
    population on 1 January 2026 is below 5,000.
  - Register Coverage Audit 2026: a simple random sample of persons registered nationally on 1 January 2026, each
    verified in the field (visit and records check) as living, or not, in the registered municipality on that date.
  - The in-play municipalities: every municipality whose register count on 1 January 2026 lies between 4,500 and 6,000
    (two former municipalities merged on 1 January 2026, so the history carries their old codes).
  - Internal moves are registered when a person registers in the new municipality; a departure abroad must be
    reported, and many are not, so the register's over-count is persons who emigrated (or died abroad) unreported.
- **Decision:** which in-play municipalities qualify for the 2027 supplement, and how many. Faces forward: the 2027
  allocation, decided in December 2026 on the adjusted 1 January 2026 population.
- **Shape:** 10, a scorecard: each in-play municipality against the 5,000 line, with the asks per municipality.
- **Strategy:** composition_mix (`own:erroneous-enumerations-post-stratified-by-the-migration-career`), Gate G
  method_or_model_selection, generators G14, G6, G19, calibration form gold_standard_subsample, context artifact
  register.
- **Data-native sentence:** in a population register an internal move is always recorded (the new municipality
  registers the person) and a departure abroad often is not, so the records left behind belong to people early in a
  stay in the country and to people who have come and gone before; the register's own date at the current address is
  reset by every internal move and stops measuring the stay, and only the event history dates the latest arrival.
- **Sources** (one line each; what it teaches, how this build differs):
  - Client pattern census-register 1 (dual-system estimates within post-strata, after erroneous enumerations): the
    erroneous-enumeration rate must be measured within post-strata; here it is the whole estimate and the post-strata
    are the analysis.
  - Register-based population statistics (over-coverage concentrated among recent immigrants, by duration of
    residence and earlier migration): the field's model of silent emigration; here the clock must be rebuilt from the
    event history because the register's address date is reset by internal moves.
  - task473 and task470 in this lane (a rate taken at each unit's own level): here the over-count is removed, not
    completed, and the conditioning properties are a clock and a history, never a recorded level.

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
