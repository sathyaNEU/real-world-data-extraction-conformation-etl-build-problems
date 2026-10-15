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
- **World.** An unnamed Canadian province; a fictional private foundation (the Ellery Foundation) choosing the region
  for its 2027 Opportunity Pathways program; a fictional Provincial Research Data Centre's linked extract: children
  born 1984 to 1988 who lived with their parents at the 2001 census (long-form households), their parents' total
  income for 2000 from the census, the parents' income tax history for 2001 to 2005 where a parent filed in every
  year, and the children's earnings at 30 to 34 from their own returns. Eight invented regions: Arlow Metro,
  Halverston, Tamsey North, Brannock Valley, Corrin Lakes, Fennick Coast, Ostler Plains, Wyecombe. Every record is
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

Ends on: Halverston, the region whose families nearly all filed every year.
Golden: Brannock Valley.

## Stump sentence

The default path names Halverston because it measures each region's elasticity only on the families with a complete
five-year tax history, a narrower and better-off slice everywhere but Halverston, whose own five-year averages still
carry part of the year-to-year swing; across every child, with the census year's transitory part taken out by the
variance the tax history shows within families, Brannock Valley stands highest, its persistence carried by the
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
Analyst test: a strong analyst who deflates, links and reads every field correctly takes the brief's long-run income where the tax history has five years of it, regresses children's earnings on it among the families that filed every year and files Halverston (Ends on), when the whole cohort's census-year elasticity corrected by the transitory variance files Brannock Valley.
Estimand: the foundation's program brief files the population (every child born 1984 to 1988 who lived with a parent in the region at the 2001 census), the outcome (the log of the child's average earnings at 30 to 34), the unit (the child, with the family's long-run income), the comparison (the slope of the outcome on the log of the parents' long-run income, region by region) and long-run income (the level a family's yearly income moves around).
No decoy: nothing is planted; the tax history's coverage is the data centre's own release rule, no memo, draft or published figure argues a region, and the context artifact (the previous program's close-out) answers its own question.
No certified replay: the method is not recovered by reproducing a published figure; no file publishes an elasticity, a reliability ratio or a transitory variance.
Lesson: a reliability ratio belongs to the sample it was measured in, while the year-to-year swing of income carries across families; correcting one year's income for the swing measured on a better-off slice, rather than for that slice's reliability, is what the field's attenuation correction asks, and no build on file teaches which part of a validation sample transfers.

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
