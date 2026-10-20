# task475 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-20 from seed ET32.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task475.json` (architecture v1), registered 2026-10-20 after a pull. Guard
  WARN on `overuse.objective` only (ETL in 7 of the last 12 builds): the lane is ETL by assignment, so the objective is
  not a free axis here. Nearest driver on file task268 v1 at 0.10 (people present in small areas from a commuting
  table), which shares no latent structure with this one.
- **Redrawn at the draw, and why the replacements are the honester labels.** The sibling's re-registration of task474
  put `filed_standard` and `budget_or_appropriation` into the three-build window, and the first card's signature (gap
  population, G6, allocation) repeats five older builds. Gap moved to `objective`, which is the truer gap: the credit
  claims count in the IRS tables is correct and complete, and the allocation is scored on a different count, the claims
  with children. Gate G moved to `etl_conformance`: the decisive step derives the policy's field from fields the source
  does carry. The forcing event is the council's 2027 weatherization plan filed with the state (`statutory_or_regulatory_filing`),
  and the context artifact is the program's 2026 close-out summary the program director works from, which the asks
  build on. `government_agency` and `nonprofit_or_charity` are banned in the window, so the deciding body is a regional
  council of governments (`local_government`), which administers weatherization for its member counties.
- **Seed:** ET32 (a state energy office splits a fixed weatherization fund across counties in proportion to tax returns
  claiming the earned income credit, capped at 12 per cent, from IRS ZIP-code tables taken to counties through the
  HUD crosswalk; the capital county's share jumped). Kept: the world (a public body, a fixed weatherization fund, the
  IRS ZIP-code tables, the ZIP-to-county relationship file, a seat county), the decision (the capped proportional split)
  and the quantity (earned income credit claims by county, narrowed to claims with qualifying children). The seed's
  mechanisms (the crosswalk's direction, its ratio type, the other-ZIP-codes line) are not the stump: the policy files
  the direction and the residential ratio, and each is Layer 1 the analyst executes.
- **Pairing:** Demographic & Social Science (house domain, income and poverty statistics from tax returns; card
  subdomain `income-poverty-inequality`) sitting in Survey Research & Official Statistics, task type
  `census-register-administrative-data-quality`, which serves ETL. The work is official statistics from an
  administrative source: the IRS ZIP-code tables for two tax years in two layouts, conformed through the residential
  ZIP-to-county file into the county table the council's allocation policy defines, with one field the source does
  not carry and has to be derived. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the council's allocation policy splits the 2027 weatherization fund across its
  fourteen member counties in proportion to each county's tax-year 2024 returns claiming the federal earned income
  credit with at least one qualifying child, filed from residential addresses in the county; no county receives more
  than 12 per cent, the excess shared in proportion among the rest. Forward facing: the 2027 program year has not
  opened and the plan is due to the state before the subgrantee contracts are signed.
- **Shape:** `05`, an allocation to a fixed total: fourteen county allocations (14), the cap decision and the largest
  county with its share (2), the conformed county table's families with children per county (planned as the CSV's
  rows, graded through the allocation), a chart with its parts (4), the files (2), and two asks over the program's
  2026 record (planned 12): about 34 criteria from the structure, none stacked.
- **Strategy:** `decomposition_attribution`: the decisive move splits each county's credit claims in the lowest AGI
  class into childless workers and families by their paired credit amount. `composition_mix` names the shortcut's
  failure (the statewide mix applied everywhere) rather than the move, and it is banned in the current window; the
  move is the split, so the decomposition label is the honest one. Gate G `etl_conformance`; gap `objective`, then
  `population`; pattern none, generators G6 (composition shift: each county's own mix of families and childless
  workers), G2 (ZIP code against county), G19 (the policy's county table); Layer 2 family `estimation_fit`, pattern
  `own:mixture recovered from a count and its paired amount by known per-kind averages`.
- **Data-native sentence:** the earned income credit pays a childless worker at most about six hundred dollars and
  phases it out below about twenty-five thousand of income, while a family's credit runs to several thousand, so the
  lowest AGI class is the only one where both kinds claim, and a county's credit amount in that class divided by its
  claims is a weighted average of the two kinds' averages that fixes its own share of families; the seat county, with
  a university and the region's hospitals and many young single workers, has far more childless claimants than the
  state, so the statewide share overstates its families.
- **Sources, one line each:** seed ET32 (the world, the decision and the quantity, never its mechanisms); the client's
  census-register patterns (net against gross classification error, dual-system estimates) for the task type's
  register-quality ground, neither used; strategies F6 composition rows (the statewide mix applied to every unit is the
  shortcut); the slot search on mixtures and paired amounts (task124's main kinds, task198's allowed amounts at a rate
  plateau: a price level, not a composition), none of which recovers a composition from a count and its amount.
- **Same-puzzle test:** gap objective, decisive generator G6, decision allocation_to_total against the last twelve
  builds, lineage included: no match. Same-driver test (gap objective, G6, etl_conformance): no match.
- **Abstraction test:** the nearest drivers stripped of nouns (task268's people present carried by commuting flows,
  task190's space-time pairs, task253's voucher split by response rates) carry no count and paired amount fixing a
  composition; none maps onto this driver.

## Default path

A strong analyst with every field read correctly:

1. Reads the allocation policy: tax-year 2024 returns claiming the earned income credit with at least one qualifying
   child, filed from residential addresses in each member county; the 12 per cent cap with the excess shared in
   proportion among the rest until no county exceeds it.
2. Conforms the IRS ZIP-code table for tax year 2024 to counties through the ZIP-to-county relationship file's
   residential ratio (the policy's direction and ratio), drops the state total and other-ZIP-codes lines, sums the
   credit claims by county and AGI class.
3. Finds that no table at ZIP or county level splits the claims by qualifying children; takes the Department of
   Revenue's statewide table of claims by AGI class and number of qualifying children, and applies the statewide share
   of claims with children in each AGI class to every county's claims in that class (all but a handful of claims above
   the lowest class are families, so the share matters in the lowest class).
4. Shares the fund in proportion and applies the cap.

**Ends on:** Tallis County, the seat, at the 12 per cent cap ($2,400,000) with its excess shared among the other
thirteen counties. The golden leaves Tallis County below the cap (planned near 11.7 per cent, about $2,34x,xxx) and
moves every other county's allocation; the built values replace these at design.

## Stump sentence

The default path applies the statewide share of claimants with children in each AGI class to every county's credit
claims and caps the seat county at 12 per cent, because it never asks what each county's own credit amounts say about
its mix of families and childless workers; Tallis County's claims in the lowest class average far less than the
state's, which only a childless share well above the state's can produce, so its families fall below the cap.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics, the client domain the house domain demographic-social-science maps to): county statistics built from an administrative register's ZIP-code aggregates, the ZIP-to-county relationship file and the Department of Revenue's statewide credit statistics, conformed to the council's county table, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each member county's number of working families with children claiming the earned income credit, which tax-policy and income statistics read from the credit's own schedule: a childless worker's credit tops out near six hundred dollars and ends below about twenty-five thousand of income, a family's runs to several thousand, so in the lowest AGI class a county's claims count and credit amount fix how many of its claimants are families, the estimator being the two-kind decomposition by the statewide average credit of each kind in the class.

Swap: "which hospital wards get the new beds, in proportion to the patients with private cover, from each ward's admissions and total charges" keeps a count and an amount but loses the mechanism: no schedule fixes what each kind of patient is charged, so a ward's charges say nothing reliable about its mix, and the decomposition the call turns on does not exist.

Layer 1: the IRS ZIP-code tables in two tax years with a changed column layout, amounts in thousands of dollars, AGI classes coded 1 to 6, a state total line and an other-ZIP-codes line; the ZIP-to-county relationship file's four ratios with a county-to-ZIP file beside it; P.O. Box ZIP codes with no residential addresses; ZIP codes created and retired between the file's quarter and the tax year; the Department of Revenue's statewide statistics as tables inside its annual report PDF; each is the systems as they publish, nothing is placed to be caught, and each is executed from a filed sentence or the source's own documentation.

Layer 2: estimation_fit, a two-kind mixture recovered from a count and its paired amount: the policy's count of claims with children is never published below the state, and the choice that flips the call is estimating each county's families from its own claims and credit amount instead of carrying the state's share of families to every county.

Decisive step: recovering each county's claims with children in the lowest AGI class from the class's claims count and credit amount, by the statewide average credit of a childless claim and of a family claim in that class, so that a county whose average credit sits low has more childless claimants than the state, instead of applying the statewide share of families to every county's claims.

Not semantics: every field, unit and definition read correctly (the policy's "at least one qualifying child", amounts in thousands, the AGI class codes, the residential ratio, the state and other-ZIP lines, the Department's table by number of children) still leaves the easy route applying the statewide share of families in each class, because no field says that the county's amount carries its own mix; the step is an estimation the analyst chooses, not a reading.

Not rule application: the policy fixes the population, the tax year, the residence rule, the cap and its sharing, and no rule or procedure says how to obtain a county's claims with children from tables that never split them; executing every filed rule with the statewide share files Tallis County at the cap, so the step no rule performs is using each county's credit amount to fix its own mix.

Analyst test: a strong analyst who conforms the ZIP tables to counties correctly, reads the basis correctly and applies the Department's statewide share of claims with children in each AGI class caps Tallis County at 12 per cent ($2,400,000) and shares its excess (the default path's Ends on); the decomposition by each county's own credit amount leaves Tallis County below the cap and moves every allocation; checks.py will run both on the clean truth.

Estimand: the council's weatherization allocation policy (filed in the pack): the population (tax-year 2024 federal returns claiming the earned income credit with at least one qualifying child, filed from residential addresses in a member county), the outcome (each county's count of such returns), the unit (returns; allocations in dollars), the window (tax year 2024, the latest the IRS has published at the plan date) and the comparison (each county's share of the fourteen counties' total, capped at 12 per cent with the excess shared in proportion until no county exceeds it).

No decoy: nothing is planted: the IRS tables, the relationship files and the Department's statistics are the sources' own publications, and the policy states the basis without a method; no memo, earlier allocation, staff draft, briefing or stakeholder figure ranks the counties or carries a statewide-share estimate.

No certified replay: no certified or published county count of claims with children ships, so nothing is recovered by reproducing a number; the method comes from the credit's schedule and each county's own count and amount.

Lesson: when a published total of mixed kinds comes with its paired amount and the kinds carry known, very different average amounts, the area's own count and amount fix its mix, and a region-wide share discards exactly the local information the amount carries; no build on file recovers a composition from a count and its amount (task124 splits mains by kind from the era, task198 reads a price level from allowed amounts).

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): the crosswalk's direction, its
  ratio type and the other-ZIP-codes line each flip only on reading a file or a field correctly, so each is data
  semantics; all three stay in the pack as Layer 1 under filed sentences.
- Apportioning split ZIP codes by a better weight than residential addresses (2026-10-20, screened): a crossing
  partition split by an indicator whose ratio to the target differs within the coarse unit, which task474's first
  architecture spent at stage 4 (a reader landed it) and task476's first architecture carried to a SEND_BACK.
- Suppressed small cells recovered against the state total (2026-10-20, screened): task465 recorded the same stump
  sitting in Layer 1, and task201 found disclosure bounds reduce to interval arithmetic with no estimation choice.
- Late-filed returns completed from processing-year files, and two administrative lists for the families' true count
  (2026-10-20, screened): maturity and capture strategies, both banned in the current window and spent in this lane.
