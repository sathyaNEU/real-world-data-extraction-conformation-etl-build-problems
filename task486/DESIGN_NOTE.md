# task486 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

Architecture 1, drawn 2026-10-21. The number came from seed ET43 (mirror trade statistics: U.S. pharmaceutical
exports to Germany against Germany's imports from the U.S.); the seed's world was screened and dropped (see `## Tried and
rejected`), and the draw keeps only the lane's objective and the seed's question, which of two ways of reading one
published source gives the right count.

## Draw

- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data Extraction &
  Conformation (ETL). The world is an area agency's census work for its provider areas, which sits by nature in Survey
  Research & Official Statistics' census-register task type; that pairing with ETL was taken by task479's re-root an hour
  before this draw, and the build's own object is the data-integration one: fusing a formally private release's nested
  tables with an exact housing count into one conformed dataset, each quantity taken from the source and level whose error
  does not accumulate.
- **World:** Kelvane County, in an unnamed U.S. state (the county, its towns Wickmoor and Fallowmere, the agency and the
  people are fictional). The Kelvane Area Agency on Aging, a nonprofit the state designates for the county, funds six
  senior-services providers, one per provider area: Wickmoor City and Fallowmere Town (the two towns' cores) and North,
  East, South and West Kelvane, whose boundaries the 2023 redraw moved in to the towns' ring roads and the river, so they
  cut twelve block groups at the town edges. The agency's FY2027 area plan update to the State Department on Aging carries
  each provider area's census-day counts of residents aged 60 and over and 75 and over, which the agency's allocation
  policy uses to split its meal funds among the providers, and each provider's FY2026 home-delivered meals and active meal
  clients. Priscilla Kemp, the agency's planning analyst, builds the counts; Donald Castillo, its planning and grants
  officer, files the update. Names drawn with `guard.py names --geo "United States" --seed 486`.
- **Niche:** fusing a formally private census release's nested block, block group and tract tables with census-day housing
  counts into counts of older residents for provider areas whose boundaries cut block groups.
- **Shape:** 14, cuts of a distribution per segment: two age cuts (60 and over, 75 and over) for each of six provider
  areas, twelve graded counts on the call side; the asks add each provider's FY2026 home-delivered meals and its active
  meal clients on 30 September 2026 (twelve more); with the instruction points the generated rubric runs past 25 criteria.
- **Decision type:** conformed_dataset (the area plan update's census table, filed with the state; the allocation follows
  from it under the agency's adopted policy). Question form how-many.
- **Strategy:** other (a truncation bias from post-processing a noise-infused release to non-negative, consistent counts,
  read by geographic level). Gap population (the published block counts are not the residents), pattern none, generators
  G2 (the level the release is unbiased at against the level the boundaries need), G16, G12. Gate G etl_conformance, with
  the estimator choice inside the conformance as the stump; a judge may read it as method_or_model_selection.
- **Data-native sentence:** the release's block counts of each sex-by-age cell were noise-infused and then forced to
  non-negative whole numbers adding up to their block group's count, so inside the block groups the provider boundaries cut
  at the town edges the sparse rural blocks can only gain and the dense town blocks give it back, and an area that holds
  only the rural side of a cut group keeps the gain.
- **Sources, one line each:**
  - The client's data-integration pattern 1 (propagate linkage error to estimates) teaches that an integration step's
    error lands in the estimate; here the error is the release's own processing, not a link.
  - Survey research's census-register pattern 1 (dual-system estimates within post-strata) is the census-quality frame;
    this build estimates no coverage and turns on the release's disclosure processing.
  - Public evaluations of the 2020 census's formally private release (small counts pushed up and large ones down by the
    non-negativity and consistency post-processing, and the advice to build custom areas from larger tabulated levels) are
    the real-world basis; the pack's notes describe the processing as a release's notes do and give no such advice.
  - task471 v5 (nearest driver, 0.07) estimates each area's true count by dual-system estimation with a correlation bias;
    nothing here is a second count, and the bias comes from where an area cuts the tabulation hierarchy.
  - task475 (0.06) recovers an unpublished subtotal from a paired amount; nothing here is unpublished, the finest
    published cells are biased when added.
  - task474 v1 (spent) split coarse totals by an indicator scaled to each unit; here the split measure is exact and the
    decisive move is the level the counts come from, not the indicator.
- **Guard:** `guard.py check` WARN only (overuse.objective, the lane's own objective). The census-register pairing, the
  published-series artifact, pattern G16 and two forums were redrawn after BLOCKs against task479 v2, task478 and task480
  as the window moved during the draw, and the forcing event (a statutory filing) and the organisation (local government)
  after task251 v4's card entered the window a quarter of an hour before this one was filed: the agency is a nonprofit, as
  many area agencies are, and the forcing event is the FY2027 allocation round the counts feed. `slots` on the driver's
  words and on the setting's words returns no earlier screen of a formally private release or of custom-area census counts.
- **Same-puzzle and same-driver tests:** (population, none, conformed_dataset) and (population, G2, etl_conformance)
  match no build in the last twelve; the allocation decision type was dropped because (population, none,
  allocation_to_total) is task471's.

## Default path

1. Read the state's area plan instructions and the agency's allocation policy: residents aged 60 and over and 75 and over
   in each provider area as drawn since 1 July 2023, household and group quarters, on census day (1 April 2020),
   estimated from the 2020 census release, to the nearest ten.
2. Take the provider-area assignment in force (effective 1 July 2023) and restore the block identifiers' leading zeros.
3. Join the release's block table (long extract) and add each block's 60-and-over cells (two sexes by eight age groups)
   and its 75-and-over cells (two sexes by three age groups).
4. Add the blocks of each provider area; check that the six areas add to the county's published totals (they do: every
   level of the release adds up, 23,621 and 7,751).
5. Round each count to the nearest ten.

Ends on: North Kelvane 850 residents aged 60 and over (East 590, South 860, West 1,100, Wickmoor City 15,380, Fallowmere
Town 4,840; 75 and over 250, 210, 290, 330, 5,070 and 1,590).
Golden: North Kelvane 700 (East 560, South 760, West 1,060, Wickmoor City 15,580, Fallowmere Town 4,960; 75 and over 200,
190, 240, 310, 5,150 and 1,660), each area built from its block groups' counts, whole groups whole and cut groups split by
census-day housing units.

## Stump sentence

Summing the release's block counts over each provider area's blocks files North Kelvane at 850 residents aged 60 and over
where it held about 700, every rural area 4 to 21 per cent high and both towns 1 to 3 per cent low, because noise-infused
counts forced to be non-negative and consistent with their block group drift from the dense town blocks into the sparse
rural blocks of the block groups the boundaries cut.

## Three rules

- Task type: general-statistics-data-science / data-integration-record-linkage-entity-resolution, which serves ETL in the
  taxonomy: one conformed dataset fused from a release's nested tables and an exact housing count.
- Domain test: the deciding quantity is each provider area's census-day count of older residents fused from a formally
  private release's nested tables, each quantity taken from the level whose error does not accumulate when cells are added
  (the block groups' counts, split inside a cut group by census-day housing units); the generic integration, summing the
  finest cells over the area, changes every rural and town count.
- Swap: "how many residents aged 60 and over lived in each provider area on census day" read with a hospital's nouns ("how
  many patients aged 60 and over were admitted from each catchment area") keeps a count by area but loses all that
  decides this one: no release forced consistent after noise, no hierarchy of tables, no exact housing count; and swapping
  the method (the fusion for the finest-cell sum) changes every area's count, which is the swap this task type's own
  object asks for.
- Layer 1: the block table as a long extract against the wide block-group and tract tables; block identifiers stored as
  numbers in the county's assignment export, leading zeros dropped; provider areas redrawn in 2023 with an effective date
  per block; the county's 2026 address points carrying the units built since census day; group quarters residents in
  facility blocks with no housing units; meal deliveries uploaded twice from a route tablet beside genuine second meals;
  frozen and shelf-stable packs; a route lent between providers; episodes closed late after a death and a quarterly
  review not held; re-registered clients under new registry numbers; each produced by the release's, the county's, the
  agency's and the state's systems as they run, none placed to be caught.
- Layer 2: estimation_fit; the methodological choice that flips the call is the level of the release the counts are taken
  from and the measure that splits a block group a boundary cuts.
- Decisive step: build each provider area from its block groups' counts (whole groups whole, cut groups split by
  census-day housing units), because the release's block counts, noise-infused and then forced to non-negative whole
  numbers consistent with their block group, carry residents from the dense town blocks into the sparse rural ones, and
  an area that holds one side of a cut group keeps that drift when its blocks are added.
- Not semantics: reading every field and the release notes correctly (counts noise-infused, then post-processed to
  non-negative whole numbers consistent from block to county; housing units and group quarters facilities held exact;
  blocks with neither left empty; small areas less accurate than large ones) still leaves the block sum, which the notes'
  remark that accuracy grows with size seems to bless; nothing says the post-processing pushes small counts up, and no
  field or code marks the drift.
- Not rule application: no filed rule says how to build an area the release does not tabulate; the state's instructions
  and the agency's policy fix the population, the ages, the day and the rounding, and executing them on the blocks files
  the block sum; which level to take the counts from, and what splits a cut group, is an estimation choice no document
  makes.
- Analyst test: with the data cleaned and every rule read correctly, a strong analyst adds each area's blocks and files
  North Kelvane at 850 residents aged 60 and over (the `Ends on:` figure), every rural area high and both towns low, where
  building from the block groups gives about 700; on the generator's clean truth (the release's expected published values,
  noise averaged over draws) the block sum still files the rural areas high and the decisive step alone files the golden
  (checks.py).
- Estimand: the state's area plan instructions (FY2027), section 3, and the agency's allocation policy file the population
  (residents of each provider area as drawn since 1 July 2023, household and group quarters), the outcome (persons aged 60
  and over, and 75 and over), the window (census day, 1 April 2020, estimated from the 2020 census release because
  provider areas are not tabulation areas), the unit (persons, each area's count to the nearest ten) and the comparison
  (none; the areas' counts stand side by side and add to the county's).
- No decoy: nothing is planted; the release is as published, with its notes; no memo, earlier filing, draft or
  stakeholder figure argues for the block sum or any other count.
- No certified replay: no certified or published figure for a provider area exists to be reproduced, and the method is
  not recovered from one; the county totals tie under every route.
- Lesson: counts made non-negative and consistent after noise are biased by their size, so an area built across a group
  from its small cells inherits the drift; take the counts from the level the area does not cut and split only by what the
  release keeps exact. No build on file turns on a formally private release.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the area's blocks added (the default path: North Kelvane 850) | the instructions' "estimated from the 2020 census release" and the notes' "accuracy grows with size" send the solver to add blocks: fires | the block table joins the assignment on the block: fires | adding the finest cells is the first conformation: fires | every total ties: fires | none | one sum: fires | readable |
| R1, cut block groups split by the county's 2026 address points (North 830) | the county's points file is the housing count to hand: fires | address points carry the block: fires | the current register for a split: fires | none | none | a share per cut group: fires | readable |
| R2, cut block groups split by the blocks' published population (North 810) | the release's own population as the weight: fires | the block table's total: fires | weight by people, not houses: fires | none | none | a share per cut group: fires | readable |
| R3, cut tracts split by census-day housing units (North 710; 6 of 12 counts off) | the notes name the housing counts as exact: fires | the tract table: fires | the largest level as the safe one: fires | none | none | a share per cut tract: fires | readable |
| R4 (decisive), each area from its block groups' counts, cut groups split by census-day housing units (North 700) | no clause names a bias, a level or a split; the notes state the processing and the exact counts only: silent | no column marks a drifted block; housing units are a column every route can use: silent | the reflexes stop at the block sum or the rungs above: silent | no control ties only here; every total ties on every route: silent | structural zeros leave no impossible row; the battery finds nothing: silent | 24 cell totals in twelve cut groups split by a second table, with the whole groups taken whole: silent | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | residents | household and group quarters population | household population only | another count (asserted: the towns lose their facility residents) | instructions 3: "household and group quarters population" |
| SF2 | aged 75 and over | 75 to 79, 80 to 84, 85 and over | 75 to 84 | another count (asserted) | instructions 3: "aged 75 and over"; the release's groups |
| SF3 | provider area | each block's area in the assignment row in force since 1 July 2023 | the rows before the redraw | another population (asserted: North 560 by the block sum) | instructions 3: "as drawn since 1 July 2023"; the assignment's effective dates |
| SF4 | census day | 1 April 2020 as estimated from the 2020 census release | the ACS five-year table; the county's 2026 estimates | other counts (asserted) | instructions 3: "on census day, 1 April 2020, ... from the 2020 census release" |
| SF5 | to the nearest ten | each area's count rounded once, persons split inside a cut group kept fractional | each cut group's parts rounded to whole persons first | same call (asserted: every count in the same ten, nearest edge 2.3 persons) | instructions 3: "round each area's count to the nearest ten" |
| SF6 | housing units for a split | the release's census-day housing unit count | the county's 2026 address points | another count (asserted, R1) | instructions 3's census day; the points file's own note that it is the current register |
| SF7 | a block with no housing units and no group quarters facility | no residents | dropped or kept | same call (asserted: the release leaves them empty) | the release notes: such blocks are empty by design |
| SF8 | group quarters in a cut block group | none sits in one | split with the housing units | same call (asserted: all six facilities lie in whole groups) | the facility list's blocks |
| SF9 | block identifier | the release's 15-character identifier | the assignment's number with leading zeros dropped | same call once restored (asserted: every block matches) | the release's identifier; state code 57 |
| SF10 | the county total | the release's county count, which every level adds to | the sum of the six areas | same call (asserted: equal on every route) | the release notes: each level adds up to the one above |

## Ladder

Seed 889, the release's block noise 1.6 persons a cell. Each route is a complete pipeline (methods.py); the counts are
each area's, to the nearest ten, 60 and over then 75 and over, in the order Wickmoor City, Fallowmere Town, North, East,
South, West.

| Rung | Route | 60 and over | 75 and over | Off the golden |
|---|---|---|---|---|
| R0 | the area's blocks added | 15,380 4,840 850 590 860 1,100 | 5,070 1,590 250 210 290 330 | 12 of 12 |
| R1 | cut groups split by the 2026 address points | 15,410 4,860 830 580 840 1,090 | 5,100 1,630 240 200 270 320 | 12 of 12 |
| R2 | cut groups split by the blocks' published population | 15,410 4,850 810 600 860 1,090 | 5,100 1,620 230 200 270 320 | 12 of 12 |
| R3 | cut tracts split by census-day housing units | 15,570 4,940 710 560 770 1,080 | 5,150 1,650 200 190 240 310 | 6 of 12 |
| R4 | each area from its block groups, cut groups by census-day housing units (golden) | 15,580 4,960 700 560 760 1,060 | 5,150 1,660 200 190 240 310 | 0 |

- **Winners and margins:** R0 sits 3 to 20 tens from the golden on every count (North +15, South +10, Wickmoor City -20,
  Fallowmere Town -12; 75 and over North +5, South +5). R3 is the nearest rung, one to two tens off on six counts, because
  the block groups inside a cut tract differ in age (their published 60-and-over residents per housing unit run 0.48 to
  0.97) and a
  tract-wide split ignores the block groups' own published counts.
- **Position and dominance:** the decisive step moves every rural count down 4 to 21 per cent and both towns up 1 to 3
  per cent; no other rung moves a count by more than half as much. The drift is visible to a grader: inside the cut
  groups, blocks of one to four housing units publish 1.94 residents aged 60 and over per unit against 0.57 for blocks of
  twenty or more (true 0.59 and 0.65), while the whole rural block groups publish 0.80 against a true 0.79.
- **Grid:** the rungs are alternative constructions, not stacked corrections; dropping blocks with no housing (the hygiene
  reflex) changes nothing, since the release leaves them empty, and raking the remaining blocks to their block group
  gives back the block sum.
- **Worth:** the decisive step flips all twelve graded counts; every reflex (add the blocks, clean, rake, weight by people,
  weight by the current register, take the larger level) lands on R0 to R3.
- **Clean truth:** averaged over 40 draws of the release's noise, the block sum still puts every rural area above the
  block-group route (60 and over: North +119, South +101, West +54, East +43; 75 and over +15 to +40) and both towns below
  it (Wickmoor City -202, Fallowmere Town -116) (checks.py, R1 to R3 of the three rules).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | residents of each provider area as drawn since 1 July 2023, household and group quarters (instructions 3; SF1, SF3) |
| 2 | Unit of account | persons; one count per provider area and age cut (instructions 3) |
| 3 | Attribution window | census day, 1 April 2020 (SF4); the asks' meals by delivery date in FY2026, clients on 30 September 2026 |
| 4 | As-of dating | the release as published; the assignment row in force since 1 July 2023; the roster and the logs pulled 9 October 2026; the death match runs to 5 October 2026 |
| 5 | Version basis | the assignment's current rows (SF3); one vintage of the release |
| 6 | Denominator | none (counts) |
| 7 | Weighting | the split of a cut group by census-day housing units, forced by the release (housing units exact, block counts drifted); every other weight misses all twelve counts (C4, the ladder) |
| 8 | Window length | none (one day) |
| 9 | Boundary inclusivity | the age groups start at 60 and at 75 (SF2); nothing sits on a boundary |
| 10 | Rounding path | each area's count rounded once to the nearest ten; rounding the parts first lands in the same ten (SF5, asserted) |
| 11 | Tie-break | none (no ranking) |
| 12 | Maturity and censoring | none on the call; the asks' deaths count only on or before 30 September 2026 (instructions 4) |
| 13 | Order of operations | the split and the sum commute (asserted) |
| 14 | Row order | file order moves nothing (asserted over a shuffle) |
| 15 | Duplicate resolution | the release has one row a block and cell; the asks' replayed deliveries (ask device) |
| 16 | Identity normalisation | block identifiers' leading zeros (SF9); the asks' registry numbers |
| 17 | Netting against gross | none |
| 18 | Dimensional units | persons; the asks' meals by item code |
| 19 | Code and status semantics | the release's age-group labels and sexes (SF2); the asks' item codes and close reasons |
| 20 | Integerisation | persons split inside a cut group kept fractional to the area's count (SF5) |
| 21 | Clause scope | instructions 3 governs the census counts, instructions 4 the service figures |
| 22 | Forward window contents | none: census day and FY2026 are closed |

## Literal reader

Executing the prompt, the state's instructions (sections 3 and 4) and the agency's policy word for word fixes the
population, ages, day, unit and rounding of every count and leaves only the method open; every literal reading of a term
lands on one population (SF1 to SF10, asserted), and the method is forced by the release's own structure: the block
counts drift by size (the published residents per housing unit of small and large blocks in one group, asserted), the
block groups' counts are published, and the housing units are the only exact measure inside a group, so the block-group
route with a housing-unit split is the one estimator the data leave standing; the tract route differs on six counts and
ignores published block-group counts that disagree with it.

## Oracles

- The county's totals: every route adds to them (23,621 and 7,751). Ties everywhere.
- Each block group's and tract's published count: the blocks inside add to it on every route, by the release's own
  consistency. Ties everywhere.
- The ACS five-year table (a distractor): another concept and period; ties under no route and is ruled out by SF4.
- None ties only under the golden; nothing in the pack scores the routes.

## Ask sheet

- **Ask A, home-delivered meals served from October 2025 through September 2026, each provider (6 figures, whole
  meals).** H18 home: the area plan's service table (instructions 4), the measure every provider carries beside its
  census counts and the call never reads. Path: the route tablets' delivery log (client_id, route, provider_code,
  delivery_date, item_code, uploaded_at), the client roster (client_id, block, meals_per_day), the item code list (meals
  per item), the provider-area assignment (block to area), the provider directory (routes), the instructions: six files,
  twelve columns. No row of it is in the call's population.
  Primary device: D1, a replay under fresh ids beside genuine same-day pairs. After the January 2026 app update some
  tablets re-sent a whole day's stops on reconnecting, under new delivery numbers and a later upload time; clients on the
  two-meal plan get two hot meals at one stop, two rows with the same client, day and code. Only the roster's
  meals_per_day separates them: counting every row keeps the replays (all six providers high), collapsing every repeated
  client-day item (the hygiene reflex) drops the second meals (all six low), and only collapsing to the plan's meals
  is right. Upload gaps do not separate them: second meals logged at the end of a route and replays re-sent minutes later
  overlap.
  Hazards: the spring 2026 loan of a Wickmoor route to a North Kelvane route (the log keeps the route's provider; the
  instructions count by the client's); frozen and shelf-stable packs counted as their meals; holidays.
- **Ask B, active home-delivered meal clients on 30 September 2026, each provider (6 figures, whole clients).** H18
  home: the same service table. Path: the client roster and episodes (client_id, state_id, block, enrolled, closed,
  provider), the state's death match (state_id, date_of_death, match_run), the registry's number links (prior_id,
  current_id), the provider-area assignment, the instructions: five files, eleven columns, two shared with ask A.
  Primary device: D7, the true key in a prior-id chain. The state's monthly death match runs against every number the
  registry ever issued and reports the one it matched, which for a client re-registered after a lapse is often the
  earlier number; the file is statewide, so most rows match no Kelvane client and an unmatched join looks normal. With
  the July 2026 quarterly review not held, deaths since the April review that no family reported are open in the roster;
  joining the match on the roster's number misses the ones under an earlier number, at least one in every provider.
  Hazards: the roster's provider is the enrolling one, so clients enrolled before the 2023 redraw on a moved block are
  another provider's now; deaths matched in the October run after 30 September stay active.
- The cracker lands the call, runs the battery, executes every filed definition (meals per code, the client's provider by
  block, deaths on or before the day) and collapses the repeated client-day items; it misses all twelve figures.

| Ask figure | The cracker's reading | Golden | Cracker |
|---|---|---|---|
| Meals, Wickmoor City | 122,674 | 139,058 | misses |
| Meals, Fallowmere Town | 36,160 | 40,951 | misses |
| Meals, North Kelvane | 8,475 | 9,793 | misses |
| Meals, East Kelvane | 7,826 | 8,883 | misses |
| Meals, South Kelvane | 8,916 | 9,855 | misses |
| Meals, West Kelvane | 11,340 | 12,558 | misses |
| Active clients, Wickmoor City | 399 | 397 | misses |
| Active clients, Fallowmere Town | 116 | 114 | misses |
| Active clients, North Kelvane | 26 | 25 | misses |
| Active clients, East Kelvane | 23 | 22 | misses |
| Active clients, South Kelvane | 28 | 27 | misses |
| Active clients, West Kelvane | 33 | 31 | misses |

- **Mirror.** The best response off the call (R0, the block sum) keeps none of the twelve census counts and reads the
  service figures the careful way: 0 of 12.
- Pair ceiling: 26.0 (cracker 45.0, mirror 7.0, weights 38 / 7 / 55 with each census count 38/12 and each service figure
  55/12).
- Mirror leakage: 0.0 per cent of the ask weight.
- Measured by: generator/ceiling.py (the bundle in memory now, the cut pack at stage 3).
- **Sensitivity.** A cracker that also reads the two-meal plan keeps 6 of 12 (pair 39.8; 53.5 if the mirror does too);
  one that follows the registry's earlier numbers keeps 6 (pair 39.8); both keeps 12 (pair 53.5).

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
