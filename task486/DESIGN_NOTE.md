# task486 design note

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

Architecture 1, drawn 2026-10-21. The number came from seed ET43 (mirror trade statistics: U.S. pharmaceutical
exports to Germany against Germany's imports from the U.S.); the seed's world was screened and dropped (see `## Tried and
rejected`), and the draw keeps only the lane's objective and the seed's question, which of two published figures for one
quantity is right.

## Draw

- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data Extraction &
  Conformation (ETL). The world is a county's census work for its aging services, which sits by nature in Survey Research
  & Official Statistics' census-register task type; that pairing with ETL was taken by task479's re-root an hour before
  this draw, and the build's own object is the data-integration one: fusing a formally private release's nested tables
  with an exact housing count into one conformed dataset, each quantity taken from the source and level whose error
  does not accumulate.
- **World:** Kelvane County, in an unnamed U.S. state (the county, its towns Wickmoor and Fallowmere, its offices and its
  people are fictional). The county Office on Aging funds six senior-services providers, one per provider area: Wickmoor
  City and Fallowmere Town (the two towns' cores) and four rural areas (North, East, South and West Kelvane), whose
  boundaries, redrawn in 2023, run along roads that cut the block groups at the towns' edges. The county's FY2027 area plan
  update to the state must carry each provider area's census-day counts of residents aged 60 and over and 75 and over,
  which the county's allocation policy uses to split its Title III funds among the providers. Priscilla Kemp, the planning
  department's demographer, prepares the counts; Donald Castillo, the Office on Aging's planning and grants officer, files
  the update. Both names drawn with `guard.py names --geo "United States" --seed 486`.
- **Niche:** fusing a formally private census release's nested block, block group and tract tables with the county's
  housing count into census-day counts of older residents for provider areas whose boundaries cut block groups.
- **Shape:** 14, cuts of a distribution per segment: two age cuts (60 and over, 75 and over) for each of six provider
  areas, twelve graded counts on the call side; the asks add each provider's FY2026 home-delivered meals and its active
  meal clients on 30 September 2026 (twelve more), with the county totals and the instruction points, about 27 criteria.
- **Decision type:** conformed_dataset (the area plan update's census table, filed with the state; the allocation follows
  from it under the county's adopted policy). Question form how-many.
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
- **Guard:** `guard.py check` WARN only (overuse.objective, the lane's own objective); the SROS pairing, the
  published-series artifact, pattern G16 and the forum were redrawn after BLOCKs against task479 v2, task478 and task480 as
  the window moved during the draw. `slots` on the driver's words and on the setting's words returns no earlier screen of a
  formally private release or of custom-area census counts.

## Default path

1. Read the state's area plan instructions and the county's allocation policy: residents aged 60 and over and 75 and over
   in each provider area as drawn since 1 July 2023, on census day (1 April 2020), to the nearest ten.
2. Take the provider-area assignment in force (effective 1 July 2023) and restore the block identifiers' leading zeros.
3. Join the release's block table (long extract) and add each block's 60-and-over cells (two sexes by eight age groups)
   and its 75-and-over cells (two sexes by three age groups).
4. Add the blocks of each provider area; check that the six areas add to the county's published totals (they do, since
   every level of the release adds up).
5. Round each count to the nearest ten.

Ends on: North Kelvane 420 residents aged 60 and over (the four rural areas a fifth to two fifths above their residents,
the two towns 1 to 2 per cent below).
Golden: North Kelvane 350 (each area built from its block groups' counts, whole groups whole and cut groups split by
census-day housing units).

The figures are the prototype's (seed 3) and are re-set from the generator at stage 2.

## Stump sentence

Summing the release's block counts over each provider area's blocks files North Kelvane at 420 residents aged 60 and over
where it held about 350, and every rural area a fifth to two fifths high and both towns low, because noise-infused counts
forced to be non-negative and consistent with their block group drift from the dense town blocks into the sparse rural
blocks of the block groups the boundaries cut.

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
  per block; the county's 2026 address points carrying the subdivisions built since census day; group quarters residents
  in blocks with no housing units; meal deliveries uploaded twice from a driver's tablet beside genuine second meals,
  frozen weekend packs, a route lent between providers; client episodes closed late after a death; each produced by the
  release's, the county's and the providers' systems as they run, none placed to be caught.
- Layer 2: estimation_fit; the methodological choice that flips the call is the level of the release the counts are taken
  from and the measure that splits a block group a boundary cuts.
- Decisive step: build each provider area from its block groups' counts (whole groups whole, cut groups split by
  census-day housing units), because the release's block counts, noise-infused and then forced to non-negative whole
  numbers consistent with their block group, carry residents from the dense town blocks into the sparse rural ones, and
  an area that holds one side of a cut group keeps that drift when its blocks are added.
- Not semantics: reading every field and the release notes correctly (counts noise-infused, then post-processed to
  non-negative whole numbers consistent from block to county; housing units and group quarters facilities held exact;
  blocks less accurate than larger areas) still leaves the block sum, which the notes' own remark that accuracy grows with
  size seems to bless; nothing says the post-processing pushes small counts up, and no field or code marks the drift.
- Not rule application: no filed rule says how to build an area the release does not tabulate; the state's instructions
  and the county policy fix the population, the ages, the day and the rounding, and executing them on the blocks files the
  block sum; which level to take the counts from, and what splits a cut group, is an estimation choice no document makes.
- Analyst test: with the data cleaned and every rule read correctly, a strong analyst adds each area's blocks and files
  North Kelvane at 420 residents aged 60 and over (the `Ends on:` figure), every rural area high and both towns low, where
  building from the block groups gives about 350; on the generator's clean truth (the release's expected published values,
  noise averaged over draws) the block sum still files the rural areas high and the decisive step alone files the golden
  (checks.py).
- Estimand: the state's area plan instructions (FY2027) and the county's allocation policy file the population (residents
  of each provider area as drawn since 1 July 2023), the outcome (persons aged 60 and over, and 75 and over), the window
  (census day, 1 April 2020, as counted by the 2020 census), the unit (persons, to the nearest ten) and the comparison
  (none; the areas' counts stand side by side and add to the county's).
- No decoy: nothing is planted; the release is as published, with its notes; no memo, earlier filing, draft or
  stakeholder figure argues for the block sum or any other count.
- No certified replay: no certified or published figure for a provider area exists to be reproduced, and the method is
  not recovered from one; the county totals tie under every route.
- Lesson: counts made non-negative and consistent after noise are biased by their size, so an area built across a group
  from its small cells inherits the drift; take the counts from the level the area does not cut and split only by what the
  release keeps exact. No build on file turns on a formally private release.

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
