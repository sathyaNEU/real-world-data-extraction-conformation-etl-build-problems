# task476 design note: Carrow's 2027 Neighborhood Stabilization Fund designations

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task476.json` (architecture v1), registered 2026-10-20; `check` re-run
  on the registered card: WARN only. Redrawn at the draw: the role family (programme_officer is task473's;
  policy_adviser is honest, the analyst prepares the designations the council votes on), the decisive generator (G2
  repeats task269's and three older builds' signature; G4, attribution at a transition, names the step honestly: the
  2014 to 2018 rate has to be carried across the 2020 redrawing of tract lines onto the new tracts), the people (one
  first name in an older build) and the question form (which repeated the last two prompts; the call is a count of
  designated neighbourhoods and their names). Structural matches on older builds differentiated on the card
  (task243, task450 v2). WARNs answered: grain_or_unit's strategy risk (the analyst test below runs on the clean
  truth with every field and rule read correctly and still files the wrong set); objective ETL in 4 of 12 (the lane's
  objective); Gate G method_or_model_selection in 8 of 12 and after task249 v5 (the decisive step is which estimate of
  the earlier rate the test runs on, among defensible ones, forced by the geography's own nesting). Nearest driver
  task19 at 0.08.
- **Seed:** ET33 (a city's neighbourhood-stabilization fund designates a neighbourhood when at least 3 of its 8
  tracts show a statistically significant poverty increase and a current rate of at least 20 per cent; the analyst
  compared overlapping ACS periods and matched tracts by GEOID). Kept: the world, the decision (which neighbourhoods
  the fund designates) and the quantity (each tract's poverty change judged against both periods' sampling errors).
  Changed: five candidate neighbourhoods, the fund's own guideline filing the non-overlapping periods. Dropped as the
  decisive step: the seed's moves (overlapping periods, a GEOID match, point estimates), each a lower rung or a
  filed fact here.
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / Data Extraction
  & Conformation (ETL). The city's community development department conforms the Census Bureau's five-year ACS
  estimates for two non-overlapping periods, published on two tract geographies (2010 tracts for 2014 to 2018, 2020
  tracts for 2019 to 2023), into one table on the 2020 tracts the fund designates on, with each estimate's margin of
  error, and tests each tract's change. The deciding quantity is each 2020 tract's 2014 to 2018 poverty rate on its
  own territory, a survey estimate the Bureau never published for that tract.
- **Shape:** 07, a grid: each candidate 2020 tract's 2014 to 2018 and 2019 to 2023 poverty rates and its verdict
  (current rate 20 per cent or more and a significant rise), each neighbourhood's count of qualifying tracts and its
  designation, the count of designated neighbourhoods, the chart, the files. Five neighbourhoods of five to seven
  tracts carry about 30 tracts, so the grid alone supplies the criteria.
- **Strategy:** grain_or_unit. A 2010 tract that grew past the Bureau's size limit was split in 2020, and the Bureau
  drew the line along 2010 block-group boundaries; the 2014 to 2018 estimates exist for the parent tract and for each
  of its block groups. The standard conformance gives each child its parent's rate (the relationship file and a
  population or area weight scale the counts, not the rate). Decisive generator G4 (the earlier quantity attributed
  across the redrawing), with G17 (the change judged against both periods' margins of error). Gate G
  method_or_model_selection: two defensible estimates of the child's earlier rate, the parent's and the block
  groups', forced by the nesting of the block groups inside the child.
- **World:** United States, an unnamed Midwestern state. The City of Carrow (Hollis County) runs a Neighborhood
  Stabilization Fund whose 2027 to 2029 round designates neighbourhoods for housing rehabilitation grants and code
  enforcement support; the council votes on the designations the Community Development Department recommends under
  the fund's guidelines. Five neighbourhoods are candidates this round. Personas from `guard.py names --geo us --seed
  476`: Tamara Larson (the department's housing data analyst), Brandon Freeman (the fund's program manager).
- **Forcing fact:** the department recommends the 2027 designations to the council on 12 April 2027 (council vote
  26 April); the guidelines take the latest ACS five-year release (2019 to 2023, released December 2024) against the
  latest non-overlapping one (2014 to 2018). As-of: 15 March 2027. The call faces forward (the 2027 to 2029 round);
  its quantity is the two closed periods the guidelines name (retrospective by the fund's own rule: designation runs
  on published estimates).
- **Forum and forcing event:** council_or_assembly (the city council votes), vote_or_meeting (the 26 April 2027 vote).
  Organisation local_government; role policy_adviser.
- **Data-native sentence:** Carrow's growing tracts were split in 2020 along the 2010 block-group lines that separated
  the old public-housing and rental blocks from the new subdivisions, so in 2014 to 2018 a parent tract's poverty
  sat almost wholly in the block groups that became one child, and that child's 2014 to 2018 rate is about twice its
  parent's.
- **The WHAT screen.** Population: each 2020 census tract in a candidate neighbourhood (the guidelines' tract list).
  Outcome: the share of the population for whom poverty status is determined that is below the poverty level, each
  period, with its margin of error. Window: the ACS 2014 to 2018 and 2019 to 2023 five-year estimates. Unit: the 2020
  tract (its 2014 to 2018 rate is the rate for the area it covers). Comparison: a rise significant at the 90 per cent
  level, and a 2019 to 2023 rate of 20.0 per cent or more; three qualifying tracts designate a neighbourhood. The
  decisive step settles none of them: it is which estimate of the earlier rate on the 2020 tract the test runs on.
- **Deliverables:** `nsf_2027_tract_poverty_change.xlsx` (the conformed tract table with both periods, margins and
  verdicts, and the neighbourhood summary) and `nsf_2027_designation_memo.docx` (the recommendation to the council
  with a chart of each tract's change against its margin).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, `census-register-administrative-data-quality` 1 and 2
    (coverage within post-strata; net against gross error): both teach measuring a record's quality inside the strata
    where it is homogeneous; here the stratum is the block group, the finest unit both periods publish, and the
    homogeneity the parent rate assumes is what the split breaks.
  - `complex-survey-estimation-variance` 2 (domain estimates keep the full design): the child is a domain of the
    parent's sample; here the domain is not a subset to re-estimate but a union of published block groups.
  - `dataset-generation/references/layer1-messiness.md`: two table layouts across releases, GEOIDs with and without
    the summary-level prefix, a 2020 tract code reused for different ground, the relationship file's land and water
    parts, controlled estimates with no margin; each asserted neutral on the call.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task474 splits a coarse published total across
    a crossing partition by a period-specific indicator (weights are the move); here no weight is estimated: the
    finer units tile the new unit exactly and are summed. task473 completes a selectively tested item; task472
    decomposes a vessel delay.

## Default path

1. Read the fund guidelines: designate a neighbourhood when at least three of its 2020 tracts have a 2019 to 2023
   poverty rate of 20 per cent or more and a rise from 2014 to 2018 significant at the 90 per cent level.
2. Read the Bureau's 2019 to 2023 tract poverty table (2020 tracts) and 2014 to 2018 table (2010 tracts), each with
   its margins of error, and the 2010 to 2020 tract relationship file.
3. Conform 2014 to 2018 onto the 2020 tracts with the relationship file: an unchanged tract keeps its estimate, merged
   tracts are summed with margins combined as the root sum of squares, and each child of a split tract is given its
   parent's poverty rate (the counts scaled by the 2010 population share, so the rate and its relative margin are the
   parent's).
4. Test each tract's change: the difference over the root sum of the two standard errors (margin over 1.645), against
   1.645; keep tracts with a significant rise and a 2019 to 2023 rate of 20 per cent or more; count by neighbourhood.

Ends on: two neighbourhoods designated, Dunmore Heights and Linden Row.

Golden: two neighbourhoods designated, Dunmore Heights and Kestrel Park.

## Stump sentence

The default path gives each child of a split 2010 tract its parent's 2014 to 2018 poverty rate and designates
Dunmore Heights and Linden Row (Ends on), because in Linden Row the children that took their parents' poor block
groups show a significant rise that is only the split, while in Kestrel Park the children that took the
better-off block groups hide a real one; rebuilding each child's earlier rate from the 2010 block groups that make
it up designates Dunmore Heights and Kestrel Park.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which the taxonomy
tags for ETL: conforming the Bureau's five-year estimates published on two tract geographies into one table on the
2020 tracts, with margins of error, for the fund's designation.

Domain test: the quantity that decides the call is each 2020 tract's 2014 to 2018 poverty rate on its own ground and
the significance of its change, worked as official statistics works a small-area survey estimate across a geography
change: the estimate rebuilt from the published units that tile the new unit, its margin combined from theirs, the
change tested against both periods' sampling errors at the guidelines' level.

Swap: "which hospital wards' infection rates rose significantly since the wards were reorganised" keeps the words
but loses what makes the step available: no finer published unit nests exactly inside the new ward with its own
sampling error in the earlier period, and the redrawing of census tracts along block-group lines when they outgrow
the Bureau's size limit is what splits a parent's poverty unevenly between its children.

Layer 1: two ACS table layouts (the 2014 to 2018 download's column names against 2019 to 2023's), GEOIDs with and
without the "1400000US" summary-level prefix, a 2020 tract code reused for different ground, the relationship file's
land and water area parts, controlled estimates printed with no margin, the block-group download's footnote rows;
each produced by the Bureau's own products, each asserted neutral on the call.

Layer 2: estimand_identification. The methodological choice is which survey estimate of a 2020 tract's earlier-period
rate the change is tested on: the parent tract's rate, which assumes the parent's poverty spread evenly over its
children, or the sum of the block groups that tile the child, which estimates the child's own ground at the cost of
a wider margin.

Decisive step: rebuilding each split child's 2014 to 2018 poverty count and universe from the 2010 block groups that
make it up (the relationship file shows every block of a child inside whole block groups), with margins combined from
theirs, before the change is tested.

Not semantics: every field, code, unit and definition read correctly (the two table layouts, the GEOID prefix, the
reused tract code, the relationship file's parts, the margins at 90 per cent) still leaves the standard conformance,
a child given its parent's rate, which is what the relationship file and every crosswalk deliver; nothing in any file
says a child's poverty differs from its parent's, and the step is the choice of estimate, not a reading.

Not rule application: the guidelines file the population (the candidate neighbourhoods' 2020 tracts), the two
periods, the 20 per cent line, the 90 per cent level and the three-tract rule; no filed rule or procedure says how a
2020 tract's earlier rate is estimated, and executing every stated rule on the standard conformance designates the
default path's set.

Analyst test: a strong analyst who reads every file and rule correctly conforms 2014 to 2018 to the 2020 tracts with
the relationship file, gives each split tract's children their parent's rate and margin, tests each change at 90 per
cent and designates Dunmore Heights and Linden Row (the default path's Ends on); only the block-group rebuild of each
child's earlier rate designates Dunmore Heights and Kestrel Park.

Estimand: the fund's guidelines (section 3) file the population (each 2020 census tract in the candidate
neighbourhood), the outcome (the poverty rate, the share of persons for whom poverty status is determined who are
below poverty), the window (the ACS 2014 to 2018 and 2019 to 2023 five-year estimates), the unit (the 2020 tract; its
2014 to 2018 rate is the rate for the area it covers) and the comparison (a rise significant at 90 per cent with a
2019 to 2023 rate of 20.0 per cent or more; three such tracts designate).

No decoy: nothing is planted to be caught; no memo, draft, earlier designation list or stakeholder figure ships, and
the relationship file and the tract tables are the Bureau's ordinary products, true as published.

No certified replay: no certified or published figure is reproduced to recover the method; the block-group estimates
are published survey estimates the rebuild sums, not a calibration the method is fitted to.

Lesson: a survey estimate for a unit drawn after the period is not its parent's estimate relabelled; where finer
published units tile the new unit, they estimate its own ground, and a split made along those units' lines is
exactly where the parent's average misleads. No build on file teaches carrying a survey estimate across a redrawn
geography from nested published units.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, point estimates only: a tract qualifies when its 2019 to 2023 rate is 20 per cent or more and above its 2014 to 2018 rate (Dunmore Heights, Kestrel Park, Linden Row) | guidelines 3.1(b) asks a rise significant at 90 per cent: fires | the margin columns beside each estimate: fires | none | none | none | one comparison: fires | readable |
| R1, tracts matched by code: a 2020 tract with no 2014 to 2018 row (every split child) left out (Dunmore Heights) | guidelines 3.2, the 2014 to 2018 rate for the area each 2020 tract covers: fires | the relationship file: fires | none | none | an unmatched join: fires | none | readable |
| R1b, the parent tested whole: the children summed for 2019 to 2023 and the parent's change given to each child (Dunmore Heights) | guidelines 3.1, each 2020 tract tested: fires | none | aggregating to a stable geography: fires | none | none | one sum: fires | readable |
| R2 (default path), each child given its parent's 2014 to 2018 rate through the relationship file, by area or 2010 population (Dunmore Heights, Linden Row) | none | the relationship file's parts: fires | the standard crosswalk conformance: fires | none | none | none | readable |
| G (decisive), each split child's 2014 to 2018 count and universe rebuilt from the 2010 block groups whose blocks make it up, margins combined (Dunmore Heights, Kestrel Park) | no clause names a block group, a rebuild or a parent's spread; 3.2 files only the area | the block groups sit in a separate table no tract step reads; the block relationship file joins 2010 blocks to 2020 blocks, not block groups to tracts | none of the conformance reflexes (crosswalk, area or population weight, stable geography) uses the finer published units | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | poverty rate | persons below poverty over persons for whom poverty status is determined (B17001_002 over B17001_001; B17021 at block groups, the same universe) | a published percentage | same call: no percentage table ships | guidelines 3.2 |
| SF2 | 20 per cent or more | the 2019 to 2023 rate unrounded against 0.200 | the rate rounded to one decimal | same call (asserted: no candidate tract within 0.002 of 0.200) | guidelines 3.1(a) |
| SF3 | a significant rise | the difference over the root sum of the two standard errors (margin over 1.645) above 1.645 | one-sided at 90 per cent (1.282); intervals that do not overlap | same call (asserted: no golden z between 1.0 and 2.2, and the overlap reading names the same tracts) | guidelines 3.1(b), the Bureau's test as written there |
| SF4 | a derived proportion's margin | the Bureau's proportion formula, the ratio formula where the radicand is negative | the ratio formula throughout | same call (asserted) | guidelines 3.2 |
| SF5 | a sum's margin | the root sum of squares of the parts' margins | none other filed | same call | guidelines 3.2 |
| SF6 | the two periods | ACS 2014 to 2018 and 2019 to 2023 five-year estimates | 2018 to 2022 against 2019 to 2023 (overlapping) | not shipped; ruled out | guidelines 3.1(b) "shares no year" |
| SF7 | the neighbourhood's tracts | the 2020 tracts on the candidate list | every tract touching the neighbourhood | same call (the list is the population) | the candidate list; guidelines 3.1 |
| SF8 | a 2020 tract's 2014 to 2018 rate | the rate for the area the 2020 tract covers | the parent tract's rate | the decisive step, an estimate of the filed quantity, not a reading: both estimate the area's rate and the data separate them | guidelines 3.2 (the WHAT); the method is open |
| SF9 | three tracts | at least three tracts meeting both tests | more than three | same call (asserted: no neighbourhood at four under the golden) | guidelines 3.1 |
| SF10 | an unchanged tract with a boundary touch-up | its own 2010 tract's estimate | an area-weighted mix of the two 2010 tracts it touches | same call and every figure (asserted: the touched blocks hold no population) | the relationship file; guidelines 3.2 |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (the rates are persons below poverty over persons for
whom poverty status is determined, the z the change over the root sum of the two standard errors).

- **R0, point estimates only (Dunmore Heights, Kestrel Park, Linden Row).** Four tracts each in Dunmore Heights,
  Kestrel Park and Linden Row are above 20 per cent and above their earlier rate. Dies to guidelines 3.1(b).
- **R1, tracts matched by code (Dunmore Heights).** Every split child lacks a 2014 to 2018 row and drops out. Dies
  to guidelines 3.2 (each 2020 tract's earlier rate is the rate for its area).
- **R1b, the parent tested whole (Dunmore Heights).** Kestrel Park's parent 0403 rose little as a whole (its poor
  child fell, its better-off child rose), so neither child qualifies. Dies to guidelines 3.1 (each 2020 tract).
- **R2, the default path: each child at its parent's rate (Dunmore Heights, Linden Row).** Linden Row's 0303.01,
  holding its parent's two poor block groups, rises from the parent's 17.8 to 31.6 per cent (z 3.64) and makes
  Linden Row's third tract; Kestrel Park's 0403.02, holding the better-off block groups, rises from the parent's 19.1
  only to 21.4 (z 0.90) and leaves Kestrel Park at two. Dies to the block groups: 0303.01's own ground was at 28.9
  per cent in 2014 to 2018 (z 0.56) and 0403.02's at 9.5 (z 4.29).
- **G, the decisive move (Dunmore Heights, Kestrel Park).** Each split child's 2014 to 2018 count and universe are
  the sums of the 2010 block groups whose blocks make it up (the block relationship file puts every block of a
  child inside whole 2010 block groups), margins as the root sum of squares, the rate's margin by the proportion
  formula; the ratio formula, and both periods from the block groups, give the same verdicts.
- **Margins (cut pack, checks.py):** every golden z sits at least 0.67 from 1.645 (nearest Dunmore Heights 0203.00
  at 0.75 and Sorrel Bend 0602.02 at 2.61); the default path's decisive tracts sit at 3.64 and 0.90; every candidate
  tract's 2019 to 2023 rate at least 0.005 from 0.200; every rate and margin at least 0.004 points from a
  one-decimal edge.
- **Position, separation and dominance:** a designation, not a ranking: the five routes name four different sets;
  only the block-group rebuild puts Kestrel Park in and keeps Linden Row out together.
- **Worth:** the call and the grid of 28 tracts; R2 keeps every unsplit tract's figures and verdicts, so the asks
  carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 2020 tracts on the candidate list, five neighbourhoods (guidelines 3.1; the list) |
| 2 | Unit of account | the 2020 census tract; a neighbourhood by its count of qualifying tracts |
| 3 | Attribution window | the ACS five-year periods 2014 to 2018 and 2019 to 2023 (guidelines 3.1(b)) |
| 4 | As-of dating | the Bureau's releases as published (2014 to 2018 in December 2019, 2019 to 2023 in December 2024); the city's extracts of 15 March 2027 for the asks |
| 5 | Version basis | the published five-year tables; no revision is issued for ACS five-year estimates |
| 6 | Denominator | persons for whom poverty status is determined (SF1) |
| 7 | Weighting | none: survey estimates as published, summed where needed |
| 8 | Window length | five years each, sharing no year |
| 9 | Boundary inclusivity | 20.0 per cent or more; z above 1.645 (SF2, SF3) |
| 10 | Rounding path | rates and z unrounded for the tests, reported to one decimal in per cent |
| 11 | Tie-break | none: each tract against the tests, each neighbourhood against three |
| 12 | Maturity and censoring | none: both periods closed and published |
| 13 | Order of operations | counts and universes summed, then the rate and its margin, then the test |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | none in the Bureau's tables; the asks' cases and payments are the asks' |
| 16 | Identity normalisation | GEOIDs with and without the summary-level prefix; tract codes with and without the decimal point |
| 17 | Netting | none on the call |
| 18 | Dimensional units | persons; rates as shares, reported in per cent |
| 19 | Code and status semantics | the tables' variable codes and the relationship file's columns; never the stump |
| 20 | Integerisation | estimates are whole persons as published; nothing rounded before the test |
| 21 | Clause scope | guidelines 3: the 2027 round |
| 22 | Forward window contents | the 2027 to 2029 round designated on two closed periods (a retrospective quantity, Draw) |

## Literal reader

Executed word for word, the guidelines fix the population (the listed 2020 tracts), the outcome (persons below
poverty over persons whose poverty status is determined), the two periods, the 20 per cent line, the test (the change
over the root sum of the two standard errors, above 1.645), the margins of derived and summed estimates, and the
three-tract rule; 3.2 says a 2020 tract's 2014 to 2018 rate is the rate for the area it covers. One thing is left
open: how that rate is estimated for a tract the 2014 to 2018 tables do not publish. The candidates are the parent
tract's rate carried through the relationship file (by area or by 2010 population, the same rate for a split), the
parent tested whole, the tract left out, and the sum of the 2010 block groups that tile the child. The data separate
them: the block relationship file puts every block of each split child inside whole 2010 block groups, whose 2014 to
2018 estimates are published, so the block-group sum is the survey's own estimate for exactly the area 3.2 names,
while the parent's rate is the estimate for a larger area; the parent tested whole and the left-out tract leave 3.1's
"each 2020 tract" unexecuted. Every variant of the block-group estimate (the proportion or the ratio formula, the
2019 to 2023 side from the tract table or from its own block groups) gives the same verdicts (checks.py). Every
write-up step names the file and rule it executes.

## Oracles

None. No control, published figure or reconciliation column ties only under the golden: the tract tables equal the
sums of their block groups under every route, and no designation list, earlier round or memo ships.

## Ask sheet

- **Ask A, each candidate neighbourhood's residential properties with a housing code case open on 31 December 2026
  and the median days those cases had then been open: 10 figures.** H18 home: guidelines 4.2 has the designation
  memo show each candidate's open code workload, which the fund's code enforcement support is sized on; a measure
  every candidate carries that the call does not turn on. Path: the code case export (case, parcel, type, status,
  opened, closed), the case event history, the parcel file (parcel, land use, 2020 block), the candidate list, the
  guidelines: five files, eleven columns. Primary device: D2, a field overwritten later. The case export is the
  system's current record: a case closed during 2026 and reopened in 2027 shows open with its closed date cleared,
  and a case open on 31 December and closed in 2027 shows its 2027 closed date; only the event history gives the
  status on 31 December. Second device: D8, an anchor on the current record. Cases carried into the 2021 system keep
  the migration date as opened, the first complaint only in the history, so days open read from the export are
  short for every migrated case. Hazards: two cases on one property (count properties), non-residential land uses,
  parcel numbers re-keyed in 2025 (the parcel file's prior number), cases outside the candidate tracts.
- **Ask B, each candidate neighbourhood's rehabilitation grant dollars the fund paid in calendar 2026 and the
  properties paid: 10 figures.** H18 home: guidelines 4.2, the fund's current activity in each candidate, which the
  council weighs beside the designation; a measure every candidate carries. Path: the payment register (two fiscal
  year sheets, entry, date, grant, parcel, amount, reference), the parcel file, the candidate list: three files,
  eight columns. Primary device: D8, amendments by period, not filing. The register is an append-only journal: a
  check voided in 2027 is reversed by a negative entry dated on the void date that references the original entry,
  so a 2026 check voided and reissued in 2027 was never paid in 2026, and a date filter keeps it. Hazards: the city's
  July to June fiscal years (calendar 2026 spans two sheets), retainage released as its own entry, a void and
  reissue inside 2026 (nets out under every handling), a grant's payments to two parcels after a lot split.
- **The construction layer:** the designated set, the 28 tracts' rates and verdicts and the chart; the cracker has
  them.
- **Main population zero-counts (asserted):** the call reads no code case, event, parcel or payment row, so neither
  ask's device moves a call figure.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, open residential code properties on 31 December 2026 and median days open | the export's status and dates read as of 31 December (opened on or before, closed after or blank), properties counted once, residential land uses, parcels re-keyed, days from the export's opened date; the reopened cases counted open and the migrated cases' days short, so every neighbourhood's count and median fall outside their bins | miss |
| B, grant dollars paid in 2026 and properties paid | both fiscal sheets, entries dated in 2026 netted within the year, retainage kept, properties counted once; the 2026 checks reversed in 2027 kept, so every neighbourhood's dollars fall outside their bins | miss |

- Mirror leakage: 0.0 per cent of ask weight (the asks read no rung's construction; every rung's response handles
  them as the cracker does).
- Pair ceiling: 36.5 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 20 ask figures; the mirror, R2, keeps 62 of the grid's 84 figures, every unsplit tract's, 28.0).
- Measured by: generator/ceiling.py

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Domain: the deciding quantity is each 2020 tract's 2014 to
  2018 poverty rate on its own ground and the significance of its change, a small-area survey estimate carried
  across the decennial redrawing; checks.py executes the analyst test on the generator's clean truth (the parent's
  rate files Dunmore Heights and Linden Row, the child's own ground Dunmore Heights and Kestrel Park). Layers: the mess
  (two table layouts, GEOID prefixes, the relationship files' parts, the touch-up blocks, re-keyed parcels, fiscal
  sheets) is the Bureau's and the city's own and is neutral on the call (SF1 to SF10); the call reads no city row.
  Three rules: no decoy, memo or earlier list ships; no field reading decides (every SF row converges or is closed by
  a filed sentence); executing every filed rule on the standard conformance designates Dunmore Heights and Linden Row.
- **Free gates (2026-10-20):** checks.py 25 of 25, verify.py clean, two builds byte-identical, target.zip cut from
  the final build (14 files), figures_check.py 195 of 195, precut.py 51 checks clean, voice-check clean, guard.py
  surface clean and heart WARN (strategy risk, objective and Gate G overuse), containers normalised.
- **leak.py REVIEW lines, each harmless:** section numbers 4.1 and 4.2 match two margins; the guidelines carry the
  domain's nouns (estimates, Bureau, five-year, significant) and name no block group, rebuild or parent's spread;
  the candidate list names the five candidates beside their tract codes and ranks nothing. The tract names are
  declared in metadata.json as stated inputs.

## Tried and rejected

- 2026-10-20, at the draw: the seed's moves (overlapping periods, a GEOID match, point estimates) as the decisive step;
  each is a filed fact or a reading here and sits on a lower rung. A period-specific population weight for split
  tracts' children was screened and set aside: it is task474's driver (a coarse total split by a period-specific
  indicator), and for a pure split any common weight leaves the child's rate equal to the parent's.
- 2026-10-20, architecture 1 spent at stage 4 (judge pass 1 SEND_BACK, Gate H rule_application; reader B landed the
  call and all 140 tract figures in about two minutes): a split 2020 tract's 2014 to 2018 rate rebuilt from the 2010
  block groups that tile it. The rebuild is exact arithmetic on published estimates, so once guidelines 3.2 files the
  estimand as the rate for the area the 2020 tract covers, the block-group table and the block relationship file
  leave only execution; without the sentence the unit is unfiled. No position holds both gates (the WHAT screen's
  own case), so the number re-roots. Ask A's reopened cases were also read straight off the event history, and the
  prompt's "median" contradicted guidelines 4.2's average.
