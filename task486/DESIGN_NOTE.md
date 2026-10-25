# task486 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

Architecture 3, drawn 2026-10-25, re-rooted fresh after architecture 2 (a linkage unit's pairwise findings resolved into
people) was spent at stage 4 when scored reader A landed the call. The author's rule holds: no retirement, a fresh rebuild.
The draw keeps the lane's objective and moves to survey research and official statistics' census-register task type, the
honest home architecture 2 could not take while task479 held the pairing.

## Draw

| Field | Value |
|---|---|
| Domain and task type | survey-research-official-statistics / census-register-administrative-data-quality (ETL) |
| Objective | Data Extraction & Conformation (ETL): the tax authority's PAYE employer returns, the valuation list's 2017 and 2023 editions, six district councils' ratepayer accounts, the companies register and the town centre postcode lookup conformed into one table of workplace retail employment by designated town centre for March 2022 and March 2026 |
| Niche | an island nation's statistics office placing the PAYE register's employers, each held at its PAYE address, at the premises they occupy in the valuation list, to name the designated town centres whose workplace retail employment fell by 8 per cent or more between March 2022 and March 2026, the eligibility test of the government's 2027 Town Centre Renewal Fund |
| World | Lundwold, a fictional self-governing island nation in the British Isles: six districts (Rookgate, the capital, Dorrstead, Glenholt, Ingmouth, Neshdale, Skelrigg), 31 designated town centres, the Revenue Office (PAYE), the Valuation Office (the rating list), the district councils (rates billing), Lundwold Statistics, the Department for the Economy (the fund) and the Council of Ministers. An island with one PAYE register and one valuation list holds every employer and every premises, which a sub-national region does not (`## Tried and rejected`) |
| People | Frances Davies (head of economic statistics at Lundwold Statistics, the requester), Stewart Sheppard (the Revenue Office's data-sharing lead), Irene Walters (the Department's fund programme manager); drawn with `guard.py names --geo "United Kingdom" --seed 486` |
| Stakeholder | the head of economic statistics, whose team compiles the island's employment statistics from the PAYE returns and prepares the fund's eligibility schedule (statistical_office_head) |
| Forum, forcing event | the Council of Ministers approves the fund's list of eligible centres at its meeting of 10 December 2026 (minister_or_cabinet, vote_or_meeting) |
| The call | which of the 31 designated town centres meet the fund's test, workplace retail employment (employees of retail employers, SIC 2007 division 47, at the premises they work in) down by 8 per cent or more from March 2022 to March 2026 |
| Decision type, unit | designation_set; a set of centres |
| Shape | 10, a scorecard against a threshold: each centre's workplace retail employment in both Marches, its change and its eligibility, every centre graded |
| Deliverables | `town_centre_fund_2027_eligibility.xlsx` (the schedule, and the asks' tables) and `town_centre_retail_employment_2022_2026.png` (each centre's change against the 8 per cent line) |
| Card | `.claude/skills/fingerprint/cards/task486.json`, architecture v3, registered 2026-10-25, architectures 1 and 2 in its lineage with their fates |
| Guard | the window task269, task303, task166 banned the first furniture (task269's council_or_assembly, budget_or_appropriation, local_government): the island's statistics office compiles and the Council of Ministers approves at a scheduled meeting, which is who would on an island with one register. test.same_puzzle_older and test.same_driver_older (population, G14, designation_set and etl_conformance) differentiated on the card against task233, task273, task280, task458 and task473, none of which places a recorded total at sites. WARN only: three_rules.strategy_risk (grain_or_unit, answered in `## Three rules` at stage 2: the register's grain is the first rung, the class density the decisive step), repeat.question_form (which, beside task485 v3, spent; the call is a set) |
| Nearest drivers | task470 0.09, task267 v0 0.08, task486 v1 0.07, task192 v3 0.07; `slots` on the mechanism's words (employment density, single-site, rateable value, apportion premises staff) and the setting's (head office, PAYE, local unit, valuation list, town centre, distribution centre) found no build that places an employer's staff at its premises; task305 reads the rating list's retail floor area into a spatial-interaction model |

**The decisive step.** The Revenue Office's PAYE returns hold each employer's employees paid in March at its PAYE
address, which for a chain is its head office or its payroll bureau. The valuation list holds each premises' rating
description, floor area and rateable value, and the districts' ratepayer accounts name each premises' occupier, so a
chain's premises are known while its staff are known only in total. Placing each multi-site employer's staff at its
premises by floor area, or by rateable value, is the standard apportionment and the easy route. But a shop holds about
six staff per 100 square metres, a superstore about four, a retail warehouse under one and a half and a distribution
centre under one, and between the two Marches several chains opened retail park units and distribution centres while
closing small town centre shops: a share by floor area moves a chain's staff out of its shops into the sparse premises it
opened, and gives a shop it closed a share far below the staff it had. The densities are measured by the register's
single-site employers, each matched to its one premises, as staff over floor area within each rating class. Each chain's
staff are placed at floor area times its class's density, scaled to the chain's total; nothing in the pack states a
density or names the step.

**Data-native sentence.** A distribution centre a chain opened in 2025 has a hundred times the floor area of one of its
shops and about fifteen times its staff.

**Retrospective count, forward call.** The fund's 2027 round is the forward decision; the quantity it turns on is the
change between two closed Marches, because the Department's prospectus files that change as the eligibility test.

## Tried and rejected

- 2026-10-21, the seed's world (ET43, U.S. pharmaceutical exports to Germany against Germany's imports from the U.S.):
  every lever is a filed concept (CIF against FOB valuation, country of origin against destination, recording date,
  classification) or an estimated rate small against the gap (freight margins by weight) or a composition rate of the kind
  task481 just spent (the asymmetry ratio by product mix, the re-dispatched share through Dutch hubs); dropped before any
  data was cut.
- 2026-10-21, survey research's census-register task type for this world: the honest home, but its ETL pairing was taken by
  task479's re-root (BLOCK ban.pairing, and ban.artifact on published_series); the build is filed in data integration.
- 2026-10-21, a single-area figure or a per-area allocation as the call: the allocation's decision type repeats task471's
  puzzle triple (population, none, allocation_to_total) and the per-dollar rounding cannot hold two unbiased estimators in
  one bin; the call is the census table itself, counts to the nearest ten.
- 2026-10-21, noise added to each cell at the block level with no structural zeros (the demonstration-data behaviour):
  four to five per cent of the county's residents landed in blocks with no housing, a symptom the hygiene battery flags
  and a share no production release would show; the release leaves such blocks empty, which also silences the device.
- 2026-10-21, block groups alike in age within a tract: the tract route then matched the golden on most counts and left
  two estimators in one bin for some and not others; block groups now differ in age within a tract, as they do, and the
  tract route is a rung (6 of 12 off).
- 2026-10-21, ask B's prior-number deaths left to chance: a death hazard spread over a decade put no unreported death under
  an earlier number in the four rural providers; the July 2026 review not held, and at least one such death per provider,
  give the device mass everywhere.
- 2026-10-21, each block's total held to its own precise count (as the production release holds block totals) with the
  age cells forced to it: on paper the drift between blocks turns into flattening inside each block toward the 46
  cells' even share, which moves a rural block's 60-and-over count only by the gap between its true share (about 31 per
  cent) and the cells' 35, a few residents per area against the 40 to 190 the per-cell processing moves; kept the
  per-cell processing, under which small blocks publish more residents than their housing would hold.
- 2026-10-21, architecture 1 (each provider area's census-day counts built from the release's block groups, cut groups split by census-day housing units, against the block sum), spent at stage 4: the judge returned NOT_DETERMINISTIC and SEND_BACK, competing_defensible_answer, because nothing shipped showed the published block counts biased, so the block sum read as a defensible estimate (Gates G and H passed); documenting the bias would leave the step to whoever reads the notes. Both scored readers filed the block sum (0 of 12) and kept all 12 service figures: the roster's meals_per_day capped the re-sent rows and the registry's links chained the earlier numbers, so both devices sat on the careful path.
- 2026-10-21, architecture 2 draw, screened before the entity-resolution step (each dead on file or on measurement):
  left truncation in an asset or licence register (task133's delayed entry, rejected again in task262, task257, task265);
  the oldest-old counted by extinct generations (task228); non-detects under several reporting limits (task189); triple
  collocation (task228); age heaping (task230's rejected draw); a lowered reporting threshold bridged by an overlap ratio
  (task481's conversion rates); a benchmark-to-indicator ratio carried past the last benchmark (task457's report against
  final); landfill first-order decay (task480's age-declining increments); load estimation from sparse samples (Jensen,
  task229); a staggered rollout of a measurement change (task453, and task480 v2's meter exchange in flight); pooled
  medians from brackets (the never-average reflex, task480's screen); degree-day temperature adjustment (fresh, but a
  per-unit degree-day regression is the textbook route and lands it); hedonic quality adjustment (the estimand's own words,
  constant quality, name the method, and the specification family forks); equipercentile against linear equating on random
  groups (task450's ground, a moderate stump); Fellegi-Sunter frequency weights (the linker's own error is task468's).
- 2026-10-21, architecture 2 draw, the card's first labels: population, G2 or G12 and method_or_model_selection repeat four
  older builds' signature (test.same_driver_older, test.same_puzzle_older against task142); relabelled G17 with G2 beside
  it and gate etl_conformance, the call being the region's conformed count with the resolution inside it. Then task251 v5
  entered the window and blocked local_government and operations_log: the integrator is the region's nonprofit HMIS lead
  and the context artifact the published point-in-time count.
- 2026-10-21, architecture 2 draw, the prototype (20,000 people over two fiscal years, half of the names drawn from a
  concentrated list): chaining every link left the region 387 short, 115 of the chained groups holding two records of one
  source and 112 holding two people with no such conflict. A merge with no conflict cannot be refuted by anything shipped,
  so the generator keeps every wrong link inside a conflict (no undetectable merge) and gives every partial record its own
  person among the records it links, or the resolved count would differ from the people served by a quantity no method
  can see.
- 2026-10-23, the linkage weights as first drawn (a birth month or day disagreement at -3.0 and -3.5): two different
  people of one name and year who agree on the month or the day alone scored 10.5 to 11.5 and linked, and 35 of 207
  merged groups then split one way under an exact constrained optimum and another strongest first; the disagreements
  weigh -6.0, as they do between true matches, and the generator's tidy step makes every licensed resolution return the
  same people (strongest first under any order of equal links, on FY2026 records only, and every optimum of three
  objectives).
- 2026-10-23, materiality at 24,000 to 30,000 households: the default path moved Halvering's amount by about 18,000
  dollars; 44,000 households, with the City's outreach team also meeting downtown single adults outside the street count,
  give 130 Halvering people and 28,815 dollars.
- 2026-10-23, the bridge as the graded shape (03): its opening items, each source's records with FY2026 service, need no
  linkage, so every response banks them; the graded structure is the allocation's buckets (05).
- 2026-10-23, ask B over households: 147 households moved in twice in FY2026, so an average per household forks; the ask
  is per move-in. Its figures needed placing mid-bin, so the move-in waits are drawn from their own stream after the
  world is fixed, with a knob by Continuum and household type.
- 2026-10-23, ask A's 16 cells beside ask B's 5: one repair (a person's night counted once) gave a solver 16 of 21 ask
  figures; ask B is split by household type, 10 figures.
- 2026-10-23, Melbray's enrollment keys written as E- and six digits: 875 ids collided and exits joined to the wrong
  stays; the vendor's key carries seven digits.
- 2026-10-23, the world's first names (Calvera, Mardell, Ostry, Pellam, Valley Street Medicine, Safe Harbor, Riverside,
  New Hope, Mercy Commons): house fix H21 against a register of U.S. counties, states and cities found Calvera two letters
  from California's Calaveras County and Pellam one from Pelham, with Sartell, Story County, Valley Stream, Safety Harbor
  and New Hope near the rest; renamed Halvering, Melbray, Ondrava, Pyrenna, Wayfarer Street Health, Hearthstone, Elm
  Street and Brightwater, Stepping Stone and Kestrel Commons, with Continuum codes HAL, MEL, OND and PYR chosen to keep
  the old codes' alphabetical order so no draw moved (every figure unchanged, asserted by the rebuild).
- 2026-10-23, architecture 2 (the unit's pairwise findings resolved into people so no person holds two records of one
  source), spent at stage 4: scored reader A, on a fresh copy of the prompt and the pack, merged the LINK findings,
  counted each merged group's records by source, found the 225 groups holding two records of one source ("which cannot
  be one person"), clustered strongest first refusing a shared source or a NONLINK and landed the call exactly (all five
  amounts and people; score_reader FAIL, 22 of 32 ask figures, every night cell, no wait). It named the guide's
  one-record-per-person sentences as what decided it: the grains the determinism needs are the cue, and a conflict a
  per-group count shows is a visible relation. Reader B and the judge thread were stopped at the spend. Re-rooted fresh
  by the author's rule (no retirement).
- 2026-10-25, architecture 3 draw, screened before the class-density step (each dead on file or on measurement): member
  months and the ratio of totals (spent); length bias (task182 v4 and others); net against gross misclassification
  (task481, task244); trend uncertainty (task482 v10); moving holidays (task162, task467); deductible leveraging and a
  plan-year clock (task479 v3, task478's screen); adverse selection (task174, task479); over-coverage and signs of life,
  extinct cohorts, death completeness (spent); a lagoon's volatile solids (a kinetic fork); truth discovery across sources
  (Layer 1); suppressed cells (task465, task475); rater severity (task471 v2); clock drift (spent); tankering (the bottom-up
  burn table is the reflex, task153 a sibling driver); surprise-billing arbitration (an open-dispute maturity replica of
  task482 v14, or composition, or a final-offer model that fails the swap); fuel factors by stoichiometry (the hourly fuel
  records cover the units that matter); testlet and subscore reliability (not the objective); deadband logs (fails the
  swap); fertiliser forestalling (cue and determinism); a bridge detour (task474 v6's world); rice water regimes (forks);
  aircraft auxiliary power by stand (the ground power logs cover it); surname-change blocking misses (Layer 1 keys);
  second homes (task305); point-source subtraction (semantics); central payroll profiling read from accounts notes (a
  cue, and zero-employee retailers show in a per-unit check).
- 2026-10-25, a head office's staff placed at premises with a local-unit file shipped: a reflex join once the file ships
  (task485's own screen); here no local-unit staff ship, and a premises' staff exist only through the density.
- 2026-10-25, a sub-national region (a combined authority) as the world: national chains are registered outside it, so
  their staff sit outside the region's PAYE extract while their shops sit inside its town centres; the island holds one
  register and one valuation list.
- 2026-10-25, the prototype with chains whose class mix holds still (proto2): floor area and rateable value named the
  golden set exactly (25 of 25), because a share by size is biased in level but not in change when a chain's sparse share
  does not move. Chains that open retail park units and distribution centres and close small shops between the Marches
  separate them (proto3: floor area adds five centres, rateable value three, the premises count drops four, the PAYE
  postcodes miss three; five density variants agree, the rateable-value density flips one centre at minus 7.47 per cent,
  a margin to build at stage 2).
- 2026-10-25, the card's first furniture (the combined authority's board, its budget round, local government) against the
  window: task269's council_or_assembly, budget_or_appropriation and local_government; redrawn with the world.
