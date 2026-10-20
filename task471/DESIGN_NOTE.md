# task471 design note: the 2027 private-well arsenic assistance counties

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task471.json`, architecture v3, registered 2026-10-20 after a pull.
  - Lineage: architecture 1 (Kessick Valley's route pitch, spent at Gate F) and architecture 2 (the program reviews on
    the 2026 licensure test form, spent at Gate G).
  - Guard: WARN only.
    - government_agency is the organisation in 36 builds: the state health department runs the private-well program.
    - ETL in 6 of the last 12: the lane's objective.
    - Gate G method_or_model_selection repeats task476 and task477 and runs in 9 of 12: how two separately sampled,
      overlapping lists combine into one estimate is an estimator chosen on honest data.
    - Question form "which" repeats: the decision picks counties.
  - Differentiation lines against task264 v2 (members weighted by event count within one sample of events) and task131
    v1 (interference between sibling sub-units).
  - Personas from `guard.py names --geo us --seed 471`. Donald Lara (v1) and Wanda Reed (v2) are not reused, and Linda
    is out (an older build has the first name).
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL.
  - The integration: the program links two incomplete, overlapping lists of private wells into one frame, conforms
    three laboratories' results and combines two separately drawn testing samples into one county estimate.
  - The deciding quantity: each county's total of wells above the arsenic standard over the union of the lists. This is
    dual-frame estimation, the task type's own statistical object.
- **World:** an unnamed U.S. state's health department and its private-well program.
  - The two lists: the state's well-permit database (wells drilled under permit since 1986) and the county assessors'
    parcel records of homes without public water. They overlap: many permitted wells sit on such parcels.
  - Testing: each list was sampled separately for a free arsenic test in 2025-26, and three certified laboratories
    report the results.
- **Decision:** which counties have enough private wells above the arsenic standard to qualify for the 2027
  treatment-system rebate allocation.
- **Strategy:** population_selection (`own:dual-frame-weights-for-wells-on-both-lists`), Gate G
  method_or_model_selection, calibration form none, context artifact register.
- **Data-native sentence:**
  - The permit list and the parcel list were each sampled at their own rate, and a well on both could have been drawn
    from either.
  - The parcel-only wells (older, dug or shallow, unpermitted) exceed the standard far more often than permitted wells.
  - So the tested wells are not a sample of the union: pooling them understates the parcel-only wells, and adding the
    two lists' estimates counts the shared wells twice.

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

