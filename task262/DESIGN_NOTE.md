# task262 design note: which region a foundation's 2027 mobility program goes to

## Draw

- **Slot.** Wave 3, sathay3012, Descriptive lane, new. Seed DA12 (a commerce platform's order-notification P99 for its
  merchant agreement) set aside at the draw: the quantity is a census percentile of order latencies, and its only
  candidate stumps were the fulfilment-order join (a data-semantics and ETL step), a pull-date censoring that a
  seconds-scale percentile shrugs off, and percentile averaging (a reflex every strong analyst avoids); none is a
  domain-native analytical step. Redrawn inside Descriptive, keeping the number (START_HERE: a redraw stays in the
  objective).
- **Pairing.** Sociology & Demography, task type `social-mobility-inequality-measurement` (serves Descriptive),
  objective Descriptive & Distribution Analysis: how strongly children's adult earnings are tied to their parents'
  long-run income in each of eight regions, the intergenerational elasticity.
- **Card.** shape 07 (a grid: each region's elasticity and the children it rests on), decision `pick_one_of_n`, gap
  `population` (whose spread of long-run income the reliability of one year's income belongs to), pattern none,
  generators G14 and G16, Gate G `method_or_model_selection`, strategy `composition_mix`, Layer 2 family
  `estimation_fit` (client pattern social-mobility 2: single-year income attenuates persistence), context artifact
  `close_out_summary` (the foundation's close-out of its previous program), forum `trustees_or_governors` (the board
  of trustees), forcing event `launch_or_rollout` (the program launches in 2027), organisation
  `foundation_or_funder`, role `programme_officer` (the director of programs).
- **World.** An unnamed Canadian province; a fictional private foundation (the Wrenmore Foundation) choosing the region
  for its 2027 Opportunity Pathways program; a fictional Provincial Research Data Centre's linked extract: children
  born 1984 to 1988 who lived with their parents at the 2001 census (long-form households), their parents' total
  income for 2000 from the census, the parents' income tax history for 2001 to 2005 where a parent filed in every
  year, and the children's earnings at 30 to 34 from their own returns. Eight invented regions: Torvale Metro,
  Halverston, Kestry North, Selvane Valley, Danholt Lakes, Caskell Coast, Ostler Plains, Wendmoor. Every record is
  constructed and declared so. People (guard.py names --locale en_CA --seed 262): Monique Webb, director of programs;
  Carl Mcclain, chair of the board of trustees; Lawrence Ferguson, analyst at the data centre.
- **Data-native sentence.** The five-year tax history exists only for families in which a parent filed in every year,
  so in the north it covers a narrow, better-off slice of families, while the census year covers every family once
  with its year-to-year swing inside it; the size of that swing is the one thing the tax history measures that holds
  for the families it does not cover, and the reliability of one year's income is not, because it depends on how far
  apart the families' long-run incomes sit.
- **Sources.** `client/layer2-rigor-patterns.md`, social-mobility-inequality-measurement 2 (single-year income
  attenuates persistence; shortcut one year at any age) teaches the attenuation; this build's decisive step is which
  piece of the validation data carries to the rest of the population: the transitory variance, not the reliability
  ratio, because the families with a complete history are a narrower slice. Pattern 1 (rank-rank against log
  elasticity) is closed by the brief's estimand (an elasticity of earnings on income, the foundation's measure).
  `guard.py mechanisms --objective descriptive-distribution`: task253 counts latent levels below a line through
  shrinkage; task256 carries a reference survey's conditional distribution to a workforce; task261 takes the error of
  a contrast on shared clusters; none separates a measurement's noise variance from its signal to de-attenuate a slope
  where the validation sample's spread differs from the population's.
- **Guard.** WARN only, registered 08:18 UTC on 15 October: the question form `which` repeats task455 v2 (retired);
  the decision is a pick of one region, so `which` is its form. The structural tests repeat task256 v1 and task54 on
  gap, pattern and Gate G and are differentiated on the card (task256 carries a multivariate conditional distribution
  to a share inside a box; task54 multiplies a forward exposure by recovered rates; this build de-attenuates an
  elasticity by a repeated-measures variance). Nearest drivers 0.06 (task459, task253 v3, task34 lineage).

## Default path

1. Read the brief: the elasticity of children's earnings at 30 to 34 on their parents' long-run income, every child of
   the 1984 to 1988 cohorts in each region; long-run income is the level a family's income moves around from year to
   year.
2. Take the parents' tax history (2001 to 2005, constant dollars) and average each family's five years: the brief's
   long-run income, measured directly.
3. Join the averages to the cohort extract (children's earnings at 30 to 34, the region at 2001) and keep the
   families with a five-year history.
4. Regress the log of each child's average earnings on the log of the family's five-year average, region by region.
5. Pick the region with the largest slope.

Ends on: Halverston.
Golden: Selvane Valley.

On the built pack the default path files Halverston at 0.35, 1.16 times the next region; the golden files Selvane
Valley at 0.49, 1.21 times Torvale Metro.

## Stump sentence

The default path names Halverston because it measures each region's elasticity only on the families with a complete
five-year tax history, a narrower and better-off slice in most regions, whose own five-year averages still carry part
of the year-to-year swing; across every child, with the census year's transitory part taken out by the variance the
tax history shows within each region's families, Selvane Valley stands highest, its persistence carried by the
lower-income families the tax history misses and hidden in the census year by the narrow spread of its families'
long-run incomes.

## Three rules

Task type: social-mobility-inequality-measurement (Sociology & Demography), which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the deciding quantity is the intergenerational elasticity of children's adult earnings on their parents' long-run income, the social-mobility field's own measure, estimated across every child with the transitory part of the census year's income removed by the variance the parents' five-year tax history shows within families.
Swap: "which plant's output depends most on its long-run input price" keeps a slope but loses the parent-child link, the census and tax sources split by who filed, and the transitory swing of family income that the correction rests on, so the call no longer reads the same.
Layer 1: census income for 2000 in census-year dollars against a tax history in constant 2005 dollars (the data centre's two sources); 2001 region codes against the foundation's region names (a boundary recode, one to one); a tax history only for families in which a parent filed in each year (filing coverage); children's earnings over five years with years of no earnings (the returns); a parent-child link file beside the person rows (the census household roster). Nothing is placed to be caught.
Layer 2: the estimation-fit family; the elasticity on long-run income is taken from every child's census-year income with the transitory variance, measured within the filers' five years, removed from its spread, because the filers' own reliability ratio belongs to their narrower spread and the census year carries the swing.
Decisive step: separating the transitory variance of one year's income from the spread of long-run income, and carrying the variance (not the reliability ratio) from the families with a complete history to every family, so each region's elasticity is de-attenuated by its own spread.
Not semantics: every field read correctly (the census year, the five-year history, its coverage, the constant dollars, the earnings window) still leaves the analyst regressing on the filers' five-year averages, or on the census year, or rescaling by the filers' reliability ratio, each of which names another region.
Not rule application: the brief fixes the estimand (the elasticity on long-run income across every child) and the data centre's guide describes the sources; no filed rule says how to estimate an elasticity on a quantity measured in full only for some families, so executing every stated rule still files the default path's region.
Analyst test: a strong analyst who deflates, links and reads every field correctly takes the brief's long-run income where the tax history has five years of it, regresses children's earnings on it among the families that filed every year and files Halverston (Ends on), when the whole cohort's census-year elasticity corrected by the transitory variance files Selvane Valley.
Estimand: the foundation's program brief files the population (every child born 1984 to 1988 who lived with a parent in the region at the 2001 census), the outcome (the log of the child's average earnings at 30 to 34), the unit (the child, with the family's long-run income), the comparison (the slope of the outcome on the log of the parents' long-run income, region by region) and long-run income (the level a family's yearly income moves around).
No decoy: nothing is planted; the tax history's coverage is the data centre's own release rule, no memo, draft or published figure argues a region, and the context artifact (the previous program's close-out) answers its own question.
No certified replay: the method is not recovered by reproducing a published figure; no file publishes an elasticity, a reliability ratio or a transitory variance.
Lesson: a reliability ratio belongs to the sample it was measured in, while the year-to-year swing of income carries across families; correcting one year's income for the swing measured on a better-off slice, rather than for that slice's reliability, is what the field's attenuation correction asks, and no build on file teaches which part of a validation sample transfers.

## Survivor anatomy

Actor: the quantity that decides, the transitory part of a family's yearly income, has no column in any file; it exists only as the year-to-year spread within each filing family's five tax years, a relation among the history's rows, and it acts on the spread of every family's census-year income in the cohort file.
Link: the step carries a variance from one source (the families with a complete tax history) to another (the census-year incomes of every family, filers or not), region by region; the history joins to the cohort by family number, but no key, clause or column asks for the within-family variance to be computed or moved, and the field's correction moves a reliability ratio instead.
Reflex: the field's standard routes, the multi-year average of parents' income measured directly on the filers (rung 0) and the census year corrected by the filers' reliability ratio, file Halverston and another region; the census year across every child (rung 1) files Torvale Metro.
Back-test: the textbook route validates: among the filing families the five-year average's slope exceeds the census year's in every region (0.257 against 0.123 in Caskell Coast, 0.345 against 0.279 in Halverston), as attenuation predicts, and the two incomes agree in level (census over five-year means 0.987 to 1.011), so the history reads as a sound long-run measure.
Second use: every file the step reads is in the pack for its own reason: the tax history is the brief's long-run income measured directly (rung 0), the cohort file holds the population and the census income, the earnings file the outcome, the price index the dollars, the recode file the region names.
Shock: nothing reads as an anomaly: Selvane Valley is fifth of eight on the census-year slope across every child (0.229), sixth on the filers' census-year slope and sixth on their five-year slope, so no sort of the regions on a shipped statistic puts it first.
Pins: the brief files the population (every child of the cohorts in the region), the outcome, the unit and long-run income as a level a family's income moves around; no filed sentence names a variance, a reliability ratio, a correction or which families to measure it on, and deleting the long-run definition leaves the estimand an elasticity on long-run income and the step where it was.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (default) the brief's long-run income measured directly: the five-year average of the tax history, regressed on by region among the families that have it | the brief defines long-run income as the level a family's income moves around, and the tax history is the only file with more than one year of it | the tax history carries five years per family; the join to the cohort is one key | yes: measure the quantity the brief names where it is measured | none: no published elasticity | the battery finds nothing | yes: one regression per region | readable |
| R1 every child on the census year, the slope of earnings on one year's income | the brief's population is every child, and the census income covers every family | the cohort extract carries the census income on every row | yes: use the source that covers the whole population | none | none | yes | readable |
| R2 the census-year slope divided by each region's reliability ratio, the filers' five-year averages regressed on their census year | none names a correction | both files share the family key | yes: the textbook correction for an error-prone regressor, calibrated on the validation subsample | none | none | yes: one ratio per region | readable |
| R3 (decisive) the census year's spread less the transitory variance measured within the filers' five years, the elasticity as the covariance over that | none names a transitory variance, a reliability ratio or a correction; the brief defines long-run income, the data centre's guide says which families the history covers | no column holds a variance, a ratio or an elasticity | no: the opponent carries the validation sample's reliability ratio, not its noise variance, and takes the filers as a sample of the population | no published figure to reproduce | the battery (keys, duplicates, constant dollars, zero years) never asks what part of the filers' data holds for the families it misses | no: a within-family variance, eight regional covariances and spreads | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the region | the child's region at the 2001 census, through the data centre's recode to the foundation's names | the region of the child's address in 2022 | same call | the brief: children are placed by the region they lived in at the 2001 census; the extract carries no later address |
| SF2 | the children | every child born 1984 to 1988 in a long-form household at the 2001 census, with a parent's census income above zero and earnings in at least one year at 30 to 34 | children with earnings in all five years | Kestry North | the brief: a child counts where the child had earnings in at least one year from age 30 to 34, a year without earnings counting as zero |
| SF3 | earnings as adults | the child's average yearly earnings at ages 30 to 34 in constant 2005 dollars, years without earnings counted as zero | the average over earning years only | same call | the brief defines the outcome; asserted: same call |
| SF4 | parents' long-run income | the level the family's total income moves around from year to year (the brief) | the five-year average of 2001 to 2005 | another region (the default path) | the brief: long-run income is the level, of which any year or average of years is a measure; the five-year average exists for only some families |
| SF5 | parents' income | the total income of the child's parents in the household, summed | the census household's total income | same call | the extract carries the parents' income only |
| SF6 | depend most | the slope of the log of the child's earnings on the log of the parents' long-run income (the elasticity) | the rank-rank slope; the correlation | another region | the brief names the elasticity and defines it as that slope |
| SF7 | every child | each child once, siblings each a row | one child per family | same call | the brief: every child; asserted: same call |
| SF8 | constant dollars | 2005 dollars by the CPI table | nominal dollars | same call | the slope of logs is unchanged by a dollar scale per year; asserted |
| SF9 | the transitory variance's scope | each region's own variance, measured on its families with a complete history | one provincial variance | same call (Selvane Valley 0.55, 1.23 times the next) | the data: the regions' variances run from 0.109 (Halverston) to 0.223 (Kestry North), each on 1,065 to 5,377 families, so a provincial variance misstates each region's; asserted |
| SF10 | the number of children | the children the region's elasticity rests on (SF2) | every child in the extract | different count, same call | the prompt asks for the children the elasticity rests on |
| SF11 | rounding | each elasticity to two decimals, computed unrounded | rounding the inputs | same call | the prompt's last sentence; every graded elasticity at least 0.0015 from a rounding edge under every estimator of the swing (within-family, year-to-year changes, census year as a sixth year, families weighted by their children in the sample, only families with a child in the sample), asserted |
| SF12 | the 2001 to 2005 history years | five tax years with the census year 2000 apart | treating the census year as a sixth history year | same call | the guide: the census income is for 2000; asserted: same call |

## Ladder

Values on the built pack (stops.py; asserted in checks.py).

| Rung | Construction | Winner | Margin | Killed by |
|---|---|---|---|---|
| R0 (default) | the filers' five-year averages, regressed on by region | Halverston 0.35 | 1.16 over Danholt Lakes 0.30 | the brief's population: every child, not the filers |
| R1 | every child on the census year | Torvale Metro 0.33 | 1.16 over Halverston 0.29 | one year carries the transitory swing: the slope is attenuated by each region's own spread |
| R2 | the census-year slope over each region's filers' reliability ratio | Kestry North 0.82 | 1.23 over Wendmoor 0.67 | the filers' reliability belongs to their narrower spread |
| R3 (decisive) | the census year's spread less the region's transitory variance from its filers, covariance over it | Selvane Valley 0.49 (golden) | 1.21 over Torvale Metro 0.40 | the golden |

- **Position.** Selvane Valley is 6th on R0 (0.24) and 4th on R1 (0.23), 3rd on R2 (0.61) behind Kestry North and
  Wendmoor, never first or second before R3.
- **Dominance.** The decisive move raises Selvane Valley's census slope 2.13 times against Torvale Metro's 1.21 times,
  an edge of 1.76, at least 1.2 times Torvale Metro's census-year lead of 1.45 (asserted).
- **Reflexes.** A provincial transitory variance keeps Selvane Valley (0.55, 1.23 times the next; the figures move,
  the call holds); the filers' averages with their residual swing removed name Wendmoor (0.41); instrumented by the
  census year, Halverston (0.38); reweighted by the inverse of each family's chance of filing, Halverston (0.35); the
  rank-rank slope, Torvale Metro (0.35). Each leaves Selvane Valley at least 1.08 times behind.
- **Convergence.** The swing measured by within-family deviations, by half the squared year-to-year changes, with
  the census year as a sixth year, with each family weighted by its children in the sample, or over the families
  with a child in the sample only gives the same two-decimal elasticity in every region, and Torvale Metro is second
  by at least 0.012 under each (draws chosen per region,
  binfit.py).
- **Worth.** Every graded elasticity moves between rungs; the call moves at each rung.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every child born 1984 to 1988 in a long-form household at the 2001 census, parents' census income above zero, earnings in at least one year at 30 to 34 | filed (the brief); SF2 |
| 2 | Unit of account | the child, with the family's long-run income | filed (the brief); SF7 |
| 3 | Attribution window | earnings at ages 30 to 34; parents' income in 2000 (census) and 2001 to 2005 (tax) | filed (the brief, the guide) |
| 4 | As-of dating | the child's region at the 2001 census | filed (the brief); SF1 |
| 5 | Version basis | the data centre's 2026 release of the linked extract | by construction (one release) |
| 6 | Denominator | the spread of the parents' long-run income in each region | filed (the brief's estimand); the decisive step |
| 7 | Weighting | each child once, unweighted (the long-form sample is drawn at one rate) | filed (the guide); SF7 |
| 8 | Window length | five earnings years per child; five history years per family | filed |
| 9 | Boundary inclusivity | born 1984 to 1988 inclusive; ages 30 to 34 inclusive | filed |
| 10 | Rounding path | elasticities computed unrounded, rounded to two decimals; dollars to the thousand | prompt; SF11 |
| 11 | Tie-break | none needed: the elasticities differ by more than a rounding step | asserted |
| 12 | Maturity and censoring | every child reaches 34 by 2022, the last earnings year | by construction (the 1988 cohort turns 34 in 2022) |
| 13 | Order of operations | average earnings then log; deflate before averaging | filed (the brief); SF3, SF8 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | one row per child in the extract; one row per family-year in the history | by construction; the asks' devices |
| 16 | Identity normalisation | the family number joins the extract and the history; the child number joins the earnings | by construction |
| 17 | Netting against gross | total income nets self-employment losses, as the census and the returns define it | filed (the guide) |
| 18 | Dimensional units | census income in 2000 dollars, the history and earnings in constant 2005 dollars by the CPI table | filed (the guide); SF8 |
| 19 | Code and status semantics | region codes, filing coverage; for the asks, program statuses and ledger accounts | the guide and the region recode; never the stump |
| 20 | Integerisation | children and young people whole; dollars to the thousand | prompt |
| 21 | Clause scope | the brief's estimand governs the call; the program's records govern the asks | filed |
| 22 | Forward window contents | the 2027 program's region rests on the cohorts the extract follows to 34, the latest whose adult earnings are complete | filed (the brief) |

## Literal reader

Executed word for word, the prompt and the brief fix the estimand: for every child born 1984 to 1988 who lived with a
parent in a long-form household at the 2001 census, the slope, region by region, of the log of the child's average
constant-dollar earnings at 30 to 34 on the log of the parents' long-run income, long-run income being the level a
family's yearly income moves around. Every literal reading of the terms gives the same population and outcome
(SF1 to SF12); long-run income is observed for no family, one year of it (the census) for every family and five
years of it for the families in which a parent filed every year, so the elasticity has to be estimated, and every
consistent estimate on the whole cohort (the census year's covariance over its spread less the transitory variance,
pooled or by region) names Selvane Valley; Halverston, Torvale Metro and Kestry North come only from estimating on
the filers, on the census year unadjusted, or with the filers' reliability ratio, never from another reading.

## Oracles

None on the main call: no file publishes an elasticity, a reliability ratio, a transitory variance or a regional
ranking on persistence; the regional economic indicators (a distractor) publish medians and rates, the aspirations
survey (a distractor) plans after school. For the asks, the close-out summary reports spending by year as posted,
every cost centre, which ties under every handling (the accruals and their reversals net to zero over the program),
and reports no start count.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each region, how many young people the 2019 to 2023 Bridges program started | 8 | the program the foundation ran in every region, the record the 2027 program's reach is set against | the board's view of what each region's office started | D1 and D7: at the April 2021 move to Northstar, CaseTrack was switched off with each open case still showing active, and the case was carried into Northstar at the same office with its intake date under a new reference, no link kept; joining the two needs the office, the intake date and the date of birth | H1 (D3): CaseTrack took some dates of birth month first (Northstar put them right), so an exact match on date of birth misses every region's swapped cases; H2 (D7): a move to another office counts at the first office (the guidelines), and a pre-migration mover's carried record has no transfer link; H3: intakes on Mondays, so office and date alone do not pair | the participant export (participant_ref, source_system, office, intake_date, date_of_birth, status, transfer_from), the office list, the guidelines, the close-out; 4 files, 9 columns | every record: over by 22 to 59 a region; transfer chains (the guidelines): over by 16 to 55; chains with rows repeating office, intake date and date of birth dropped (the cracker): over by 2 to 14; CaseTrack active rows dropped: off by 0 to 3, one region hit | a case-management migration that leaves the old system frozen and re-keys open cases, with dates of birth typed month first in the old system, is what such systems hold |
| B, for each region, what the program spent there, to the nearest thousand dollars | 8 | the program's cost in every region, the trail the 2027 budget is set against | the board's view of what each region cost | D6 and D2: offices whose December mentor invoices had not arrived accrued them at year end, the December invoices were posted in January, and finance reversed each year's accruals in one line at the central cost centre; shared among the regions with the central team's costs, the reversal leaves each accruing office's December fees counted twice and takes the offset from every region by starts | H4 (D5): the close-out's final bursaries and evaluation posted January to March 2024; H5: the central share is by A's starts, so A's devices move every B figure | the program ledger (posting_date, cost_centre, account, amount, description), the office list, the guidelines, the close-out, the participant export; 5 files, 12 columns | reversal shared by starts, whichever start count: off by $2,373 to $7,699 a region (the cracker's: $2,957 to $7,226); negative lines dropped: over by $2,546 to $20,867; 2019 to 2023 postings only: under by $3,218 to $11,534; office lines alone: under by $51,000 to $141,000; accruals taken back with the cracker's starts: off in 5 regions | year-end accruals reversed centrally in one journal and close-out payments after a program ends are what a grant ledger holds |
| C, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's elasticities | R0 to R3 | the analyst's own exhibit |

- **Main population zero-counts.** No ask device or hazard sits in the cohort extract, the earnings file, the tax
  history, the region recode, the price index or the brief: the call computed from the five call files alone equals
  the golden, and the asks computed from the three Bridges files alone equal theirs (asserted).
- **Hazard table.** H1 moves every A figure on the cracker's path and every B figure through the share; H2 moves A's
  starts in the regions moves leave and join; H3 moves A for an analyst pairing on office and date; H4 moves every B
  figure; H5 moves every B figure by A's error.
- **Referee.** The guidelines file the counting rules (a young person counts once, as a start at the office of first
  enrolment; a region's spending is the cost of its office's work with the central team's costs shared by starts;
  the accounts close when the final bursaries and evaluation are paid), the WHAT; no file says which records the
  migration carried or which reversals undo which offices' accruals.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A starts (8) | transfer chains followed back to the first record, rows repeating office, intake date and date of birth dropped | over by 2 to 14 in every region (the carried cases whose CaseTrack date of birth is month first) | miss |
| B spending (8) | each office's ledger lines plus the central cost centre's lines, the reversals included, shared by the cracker's starts | off by $2,957 to $7,226 in every region | miss |

Mirror leakage: the mirror (rung 0, Halverston) takes the asks the cracker's way and misses all 16; it keeps the chart
parts only where the chart is drawn, under 35 per cent of ask weight.
Pair ceiling: 32.5 (the cracker banks the call and its components, 45 with instruction-following, and the chart's
five parts from its own elasticities, and none of the 16 Bridges figures; the mirror 5 plus 7 plus the chart's form, 3).
Measured by: `generator/cracker.py`, run on the cut pack after every change (checks.py runs it and asserts it): the
cracker keeps 0 of 16 ask figures (A 0 of 8, B 0 of 8), and the mirror, taking the asks the same way, 0 of 16.

## Build record

- **World.** Eight regions drawn from named streams by census code (common.py): families' long-run log income, a
  kinked slope of children's log earnings on it, filing every year as a logistic in the family's level, and each
  region's own year-to-year swing (from 0.33 in Halverston to 0.47 in Kestry North and Wendmoor, seasonal work in the
  north and on the plains). The tax-year draws of Torvale Metro, Kestry North, Selvane Valley and Wendmoor and the
  upper slopes of Kestry North, Selvane Valley, Caskell Coast, Ostler Plains and Wendmoor were chosen (binfit.py) so every
  consistent estimate of the swing gives the same two-decimal elasticity in every region; the ladder margins were
  re-checked after (stops.py, checks.py).
- **Pack.** 14 files (15 before the 10-31 reship removed the data dictionary): the data centre's cohort extract (58,441 children), the children's earnings (525,969
  child-years), the parents' income history (25,290 families, 126,450 family-years), the region recode, the price
  index, the user guide; the foundation's brief, the Bridges participant export (1,640 records),
  ledger (2,056 lines), office list, 2019 guidelines and 2024 close-out; two distractors (the 2021 regional economic
  indicators, the 2023 youth aspirations survey).
- **Gates.** checks.py 82 assertions (three rules, ladder, reflexes, SF1 to SF12, convergence, bins, asks' goldens
  against the generator's truth, cracker stops, separation, distractors, input gates, realism sweep, H21), verify.py
  green on the bundle alone, two builds byte-identical, target.zip identical to target/, figures_check 65 of 65,
  precut 49 checks, leak.py REVIEW (no LEAK), guard surface clean, heart WARN (question form), H1 audit clean.

- **Stage 4.** Leak reader loop 1: no decisive-step sentence, no ranking file, the deciding step analytical; realism
  residue fixed (the brief's template parts, a one-line dictionary, central licence and evaluation lines booked to
  materials, plans open at the close). Judge r1 DETERMINISTIC, APPROVE (Gate G analytical_non_defect; Gate H domain
  pass, layers pass, decisive step analytical); its one optional finding (the swing weighted per child moved
  Wendmoor's second decimal and put Selvane Valley on 0.495) closed in the data, every estimator of the swing now
  giving the same two-decimal elasticities and runner-up. Reader loop 2: the brief's application statistics and the
  aspirations survey's respondent total fixed. Reader loop 3 on the final pack: nothing found.

## Pre-ship check

- **Rule 1, the domain, on the built pack.** The call is decided by each region's intergenerational elasticity of
  earnings, estimated from the microdata (58,202 children with their parents' census income, 525,969 child-years of
  earnings, 25,290 families' five tax years): the census year's covariance with children's earnings over its spread
  less the region's transitory variance. No shipped column holds an elasticity, a slope, a variance or a reliability
  (asserted, R1). With another field's nouns the parent and child, the census and tax sources split by filing and the
  transitory part of one year's income are gone.
- **Rule 2, two layers.** Layer 1 on the call's path is the data centre's own release: three dollar bases, a 2021
  rename of the census regions, census incomes at or below zero, a nine-year earnings file from which each cohort's
  ages 30 to 34 are taken, siblings sharing a family number; each mishandled leaves the call (asserted, R2). Layer 2
  is the measurement-error correction: which part of the filers' five-year history carries to every family. On the
  generator's clean truth the filers' averages file Halverston and the census year less each region's transitory
  variance files Selvane Valley (R3a, R3b).
- **Rule 3, the decisive step.** No shipped sentence names a transitory variance, a reliability ratio or a correction
  (asserted on every document); the brief defines long-run income as the level a family's income moves around, the
  guide says which families the history covers. Executing every filed rule on the obvious measure (the history's
  five-year average, among the families that have it) files Halverston; nothing planted, copied or withheld carries
  the answer (R3c).
- **Determinism.** The swing measured within families, from year-to-year changes, with the census year as a sixth
  year, with each family weighted by its children in the sample, or over the families with a child in the sample
  gives the same two-decimal elasticity in every region, each at least 0.0015 from a rounding edge, and the same
  runner-up (the judge's one optional finding, the per-child weighting, closed in the data); a provincial swing keeps
  the call; the asks' goldens are exact under the guidelines' counting and spending rules and every
  region's spending sits at least $190 from a thousand-dollar edge; the cracker's path misses every ask figure
  (asserted).

## Tried and rejected

- The seed's world (an order-notification P99 for a merchant agreement), rejected at the draw: its only candidate
  stumps were a fulfilment-order join (data semantics, ETL), a pull-date censoring a seconds-scale percentile shrugs
  off, or percentile averaging; none is the field's analysis.
- Late-life moves into long-term care with death competing and delayed entry at a population extract's opening,
  rejected at the draw: task133's shipped round 2 (another author's) already carries left truncation at a system
  go-live with a competing exit, so the driver repeats in other nouns.
- Health expectancy (Sullivan) with care-home residents outside a household survey, rejected at the draw: the
  survey's scope statement and a residents file make the decisive step a coverage reading, and the residents'
  disability needs a filed assumption.
- Small-unit bias of a dissimilarity index, rejected at the draw: the estimand either names the random-allocation
  benchmark (the method filed) or reads as raw unevenness (the corrected index then contradicts it).
- A completions ask (how many of each region's starts completed) beside starts, dropped at build: completion
  status rides on the same migrated records, so it added no new device and doubled the ask on one path.
- An "Imported from" note on each carried Northstar record, dropped at build: a single column naming every device
  row is a marker, and the cracker linking on it lands every start count.
- One transitory spread for the province, dropped at build: with a common true variance the regional and provincial
  estimates differ only by noise and split the two-decimal elasticities; each region now has its own swing (seasonal
  work in the north and on the plains), which forces the regional estimate.
- "Spending in a region is what was charged to its office" in the guidelines, rewritten at build: read literally it
  shares the central reversal of the offices' accruals by starts and files the cracker's figure; the guidelines now
  say the cost of the office's work and the central team's costs.
- Six invented names (five regions and the foundation), renamed at build: each sat within one letter of a real place
  (Harlow, Ramsey, Corran, Fenwick, Wycombe; a former region name one letter from North Shields) or shared its word
  with another build's world; checks.py screens every invented name (H21).
- 2026-10-31, re-check under the 10-30 gates: `leak.py` LEAK on the data centre's data dictionary (section 3: no shipped file describes the data). Removed, with the user guide's file-by-file section and the brief's mention of it; the guide keeps the release's coverage, units and filing rule, which the data centre publishes, and the columns name their own units. `metadata.json` no longer lists which files the call and the asks read. The prompt drops its region count and asks where, not which. Every graded figure unchanged (84 checks).
