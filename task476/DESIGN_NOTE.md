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

## Tried and rejected

- 2026-10-20, at the draw: the seed's moves (overlapping periods, a GEOID match, point estimates) as the decisive step;
  each is a filed fact or a reading here and sits on a lower rung. A period-specific population weight for split
  tracts' children was screened and set aside: it is task474's driver (a coarse total split by a period-specific
  indicator), and for a pure split any common weight leaves the child's rate equal to the parent's.
