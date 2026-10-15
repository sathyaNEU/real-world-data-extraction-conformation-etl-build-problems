# task261 design note: where a life insurer's 2027 retirement range draws its segment boundaries

## Draw

- **Slot.** Wave 3, sathay3012, Descriptive lane, new. Seed DA11 (a retirement-products committee segmenting adjacent
  age groups by median household net worth from a multiply imputed wealth survey with replicate weights): its world,
  decision and quantity are kept; the seed's mechanism rows are decoy-era design and were not read. The stump family
  this world produces (whether a difference stands above its error) waited for task260's `uncertainty_hold` and
  `committee_or_panel` to leave the guard's last three.
- **Pairing.** Survey Research & Official Statistics, task type `complex-survey-estimation-variance` (serves
  Descriptive), objective Descriptive & Distribution Analysis: how household net worth is distributed across the six
  age groups of the older partner, and which neighbouring groups' medians differ by more than the error of the
  difference.
- **Card.** shape 14 (cuts of a distribution: each age group's median and each adjacent difference with its error),
  decision `structural_verdict`, gap `rule` (the committee's filed criterion, 1.96 standard errors of the difference,
  and the survey's clustered design settle which error estimator is right), pattern none, generators G17 and G16,
  Gate G `signal_vs_noise_or_hold`, strategy `uncertainty_hold`, Layer 2 family `field_method`, context artifact
  `published_series` (the survey's results bulletin), forum `committee_or_panel` (the retirement product committee),
  forcing event `vote_or_meeting` (the committee meets on 27 January 2027), organisation `financial_institution` (a
  life insurer), role `product_manager` (its head of retirement products).
- **World.** Australia; a fictional national household wealth survey (the 2025 wave) run by a fictional independent
  research centre, released as a public-use file: a household summary extract with five implicates per household,
  a person file, 200 bootstrap replicate weights in their own file, a user guide and a results bulletin; a fictional
  life insurer's brief for its 2027 retirement range, with the insurer's own retirement income book (its client
  register, its Retirement Income Account pensions and their nominations, and its lifetime annuity lives) for the
  asks. Every record is constructed and declared so. Invented names: Kelvane Life, the Household Finance Research
  Centre, the National Household Wealth Survey. People (guard.py names --locale en_AU --seed 261; the AU geography
  key falls back to the US list): Tracey Zimmerman, head of retirement products; Ryan Ferrell, chair of the
  retirement product committee; Wendy Koch, senior actuary, valuations.
- **Data-native sentence.** The survey samples households in clusters (two areas in each of 60 strata) and housing
  wealth moves with the area, so every age group's median rises and falls with the same areas from one replicate to
  the next; a difference between two age groups' medians therefore varies far less than the two medians'
  separate errors suggest, and only the difference recomputed on the replicate weights shows it.
- **Sources.** `client/layer2-rigor-patterns.md`, complex-survey-estimation-variance 1 (variance reflects strata and
  PSUs; shortcut the SRS formula) teaches the design effect on one estimate; this build's decisive step is the
  covariance the same clusters put between two estimates, which runs the other way (the shortcut's error is too
  large). Pattern 2 (domain estimates keep the full design) is met by the replicate weights and is not a rung.
  `guard.py mechanisms --objective descriptive-distribution`: task253 counts latent levels below a line through
  shrinkage; task260 widens an interval to two random factors; task229's lineage widens the error of a mean over
  units that fail together; none takes an error from a contrast whose two terms share clusters.
- **Guard.** PASS at 06:16 UTC on 15 October, once task143's registration took task260 (strategy
  `uncertainty_hold`, forum `committee_or_panel`) out of the last three; nearest drivers task143 (0.09, a
  weakest-member chance in a new group) and task229 v1 in lineage (0.09, the error of a mean over units failing
  together through a shared parent): task229's move widens one estimate's error for its clusters, this build's move
  is the covariance the same clusters put between two estimates, which narrows the error of their difference.

## Default path

1. Read the brief (`retirement range brief`): six age groups of the older partner, one product per segment, two
   adjacent groups kept apart when their difference in median household net worth exceeds 1.96 standard errors of
   that difference.
2. Join the person file to the household summary on the household id, take the older of the reference person and
   partner, and place each household in its age group.
3. Compute each age group's weighted median net worth on each of the five implicates and average them.
4. Compute each age group's standard error as the user guide does for an estimate: the replicate variance on
   implicate 1 plus 1.2 times the variance between the five implicate medians (the bulletin's relative standard
   errors are reproduced this way for the reference person's age).
5. For each adjacent pair take the error of the difference as the square root of the two groups' variances added,
   and keep the pair apart when the difference exceeds 1.96 times it.
6. 55-64 and 65-74 differ by about $258,000 against an error of about $165,000 (1.6 times) and share a segment, as
   do 65-74 and 75 and over (1.2 times); the range has four segments, 55-64 to 75 and over one of them.

Ends on: four segments, under 35 | 35-44 | 45-54 | 55 and over
Golden: five segments, under 35 | 35-44 | 45-54 | 55-64 | 65 and over

## Stump sentence

The default path files four segments, under 35 | 35-44 | 45-54 | 55 and over, because it takes the error of each
adjacent difference from the two age groups' own standard errors added as if the groups were independent samples;
both groups are drawn from the same 120 survey areas and their medians move together from replicate to replicate
(correlation 0.70), so the error of the difference recomputed on the replicate weights is about $95,000, not $165,000,
and 55-64 stands apart from 65-74 (2.7 times its error), giving five segments.

## Three rules

Task type: complex-survey-estimation-variance (Survey Research & Official Statistics), which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the deciding quantity is the design-based standard error of a contrast between two domain medians in a stratified, clustered, multiply imputed household wealth survey, estimated with its replicate weights and the between-implicate variance; the survey field's own estimator decides which age groups the committee keeps apart.
Swap: "which adjacent school years share a reading programme by median test score" keeps a contrast but loses the survey's strata, areas, implicates and replicate weights that the error is built from; with a generic independent-samples error in place of the design-based one the boundaries move, so the call no longer reads the same.
Layer 1: five implicates per household stacked as rows of the summary extract (the survey's multiple imputation); a person file keyed by household and person number beside a household file keyed by household and implicate (the public-use release); a reference person chosen by an income hierarchy, so the older partner is often the other adult (the survey's household definition); replicate weights in their own file; the bulletin's medians rounded and its errors given as relative standard errors (the publication); negative net worth where debts exceed assets (the questionnaire). Nothing is placed to be caught.
Layer 2: the field-method family; the error of a difference between two age groups' medians is taken from the difference recomputed on each replicate weight, with the between-implicate variance of the difference added, because the groups share the survey's clusters.
Decisive step: estimating the standard error of a contrast between two domains of one clustered sample on the replicate weights, rather than combining the two domains' own standard errors in quadrature as if they were independent samples.
Not semantics: every field, code and definition read correctly (implicates, weights, replicate weights, the person file, the older partner, the bulletin's relative errors) still leaves the analyst combining the two groups' errors as independent, which files four segments.
Not rule application: the brief fixes the threshold and the user guide states its general method for the error of any estimate; no filed sentence says that two age groups' medians move together or that their difference is to be treated as an estimate in its own right, so the analyst who executes the guide on each median and adds the two errors still files four segments; seeing the difference as the estimate whose error the replicates must carry is the step no rule performs.
Analyst test: a strong analyst who places households by the older partner, averages the implicates and reproduces the survey's error for each age group, then adds the two groups' variances for each adjacent difference, files four segments, under 35 | 35-44 | 45-54 | 55 and over (Ends on), when the difference's own replicate error files five.
Estimand: the brief files the population (households in the survey's 2025 wave, weighted), the outcome (household net worth as the survey defines it), the unit (the household, placed by the age of the older of its reference person and partner), the window (the 2025 wave) and the comparison (each adjacent pair's difference in median net worth against 1.96 standard errors of that difference).
No decoy: nothing is planted; the bulletin is the survey's own publication, correct for its own question (the reference person's age), and no memo, draft or stakeholder figure argues a structure.
No certified replay: the method is not recovered by reproducing a published figure; the bulletin publishes each age group's median and relative error, never a difference or its error.
Lesson: estimates for subgroups of one clustered survey share its clusters and move together, so the error of their difference comes from the difference recomputed on the replicate weights; no build on file teaches the covariance two domain estimates take from shared clusters (task229's lineage teaches the opposite move, the design effect on one mean).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (default) each age group's error from the replicate weights and the implicates (the user guide's method for an estimate), the two groups' errors added in quadrature for each neighbouring difference | none: the brief files the threshold in standard errors of the difference and the user guide the error of an estimate | the bulletin's table pairs each median with its relative standard error, one row per group | yes: the root of the two variances added is the opponent's default for comparing two published estimates | the bulletin's relative errors, reproduced on the reference person's age, confirm each group's error and say nothing about a difference | no | yes: one square root per pair | readable |
| R1 the published series' basis: households placed by the reference person's age, as the bulletin is, with either error | the brief: placed by the older of the reference person and partner | the summary extract carries `hrp_age`; the partner's age needs the person file | yes: reproduce the published series first | the bulletin ties to it | no | no | readable |
| R2 errors as if the households were a simple random sample (a Woodruff interval on each weighted median, or a bootstrap over households), the difference tested with them | the user guide: every standard error is estimated with the replicate weights and the implicates | the replicate weights sit in their own file | yes: a bootstrap over the rows is the opponent's default without design variables | none | no | no | readable |
| R3 (decisive) the difference itself recomputed on every replicate weight (and implicate), its variance taken from those replicate differences with the between-implicate variance of the difference added | none names the error of a difference, a covariance or shared areas; the user guide's worked example is one group's median | the public file carries no stratum or area code; the shared areas live only in which households each replicate doubles or drops | no: the opponent compares two estimates by their own errors; that two domain estimates of one clustered sample covary is the survey specialist's point | no difference or error of a difference is published anywhere in the pack | the battery (implicates stacked, weights summed, top-codes, negatives) never asks how two medians covary | no: 200 replicate weights by five implicates by two medians, a weighted median per cell | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a household's age group | the older of the reference person and partner (person file relationship codes 1, 2 and 3) | the reference person's age; the oldest member | six segments (reference person, contrast) or five (oldest member, z 1.99) | the brief: households placed by the age of the older of the reference person and partner |
| SF2 | "partner" | relationship code 2 (husband, wife or registered partner) or 3 (de facto partner) | code 2 only | same call (asserted) | the user guide's relationship codes and the brief's "partner" |
| SF3 | household net worth | the summary extract's `networth` (assets less debts, negative values kept) | assets only; negatives dropped | another quantity | the user guide's definition and the brief |
| SF4 | the median | weighted by the household weight `wgt` | unweighted | another estimate | the user guide: estimates use the weights |
| SF5 | the weighted median's convention | the first value at which the cumulative weight reaches half | interpolated between neighbouring values | same call (asserted) | convergent (C1) |
| SF6 | the five implicates | each estimate on every implicate, averaged (the user guide's combining rules) | implicate 1 alone; the five stacked as one file at a fifth of the weight | same call (asserted) | the user guide; convergent (C1) |
| SF7 | the replicate variance | mean squared deviation of the 200 replicate values from the full-sample value, on implicate 1 as the user guide's shortcut allows | on all five implicates averaged; about the replicates' mean | same call (asserted) | the user guide; convergent (C1) |
| SF8 | the between-implicate variance | added at (1 + 1/5) times the variance between implicates | omitted | same call (asserted) | the user guide's combining rules |
| SF9 | 1.96 standard errors | the normal value the brief names | a t value on 60 or 59 degrees of freedom (about 2.00) | same call (asserted) | the brief; no pair's ratio lies between 1.90 and 2.05 (asserted) |
| SF10 | "exceeds" | strictly greater | at least | same call: no ratio within 0.3 of 1.96 (asserted) | the brief |
| SF11 | neighbouring groups and segments | only the five neighbouring pairs are tested; a segment is a run of groups no neighbouring test keeps apart | every pair tested | same call (asserted: 55-64 against 75 and over differs by under one standard error) | the brief |
| SF12 | the age top-code at 85 | 85 and over sit in 75 and over | none | same call | the user guide |
| SF13 | the weight across implicate rows | the household weight once per household and implicate | summed over the five rows | same medians (asserted) | the user guide |
| SF14 | households with no partner | placed by the reference person | none | same call | the brief |
| SF15 | the difference's direction | the older group's median less the younger's | the reverse | same call | the brief's test is on the size of the difference |
| SF16 | the 95 per cent interval in the chart | the difference plus and minus 1.96 of its standard errors | a t interval | same chart (asserted) | the prompt and the brief |

## Ladder

| Rung | Construction | Kept apart | Segments | Dies to |
|---|---|---|---|---|
| R0 (default) | each group's error from the replicate weights and the implicates, the pair's errors added in quadrature | every pair to 55-64; 55-64 and 65-74 (1.57 times) and 65-74 and 75 and over (1.20) not | four: under 35, 35-44, 45-54, 55 and over | the shared areas: the 55-64 and 65-74 medians move together across the replicates (correlation 0.70), so the difference's own error ($95,000) is far below the quadrature ($165,000) |
| R1 | households placed by the reference person's age (the bulletin's basis), with either error | under 35 to 55-64 apart; 55-64 and 65-74 not (0.47 in quadrature, 0.81 on the difference) | four, on other medians ($84,000, $311,000, $593,000, $888,000, $963,000, $803,000) | the brief's placement (the older of the reference person and partner) |
| R2 | errors as if a simple random sample (a Woodruff interval on each weighted median, or a bootstrap over households) | every pair, 65-74 and 75 and over included (2.50 and 2.61 times) | six | the user guide (errors from the replicate weights); the design effect on each median is 1.9 to 4.7 |
| R3 (decisive) | the difference recomputed on every replicate weight, with the implicates' variance of the difference | every pair but 65-74 and 75 and over (55-64 and 65-74 2.71 times; 65-74 and 75 and over 1.56) | five: under 35, 35-44, 45-54, 55-64, 65 and over | the golden |

- **Position and margin.** The decisive pair, 55-64 against 65-74, differs by about $258,000; its error recomputed on
  the replicates is about $95,000 (2.71 times, 0.75 above the line) against about $165,000 in quadrature (1.57 times,
  0.39 below it). 65-74 against 75 and over stays together on every design-based route (1.56 on the difference, 1.20 in
  quadrature) and parts only without the design (2.50 Woodruff, 2.61 bootstrap). The younger boundaries hold on every
  route (at least 2.43 times in quadrature). Every golden ratio sits at least 0.3 from 1.96, and every graded dollar
  figure at least $100 from a rounding edge (asserted).
- **Every reflex lands wrong.** Quadrature on the user guide's errors: four segments; the reference person (the
  bulletin's basis): four with either error, on other medians; errors without the design: six; a t value for 1.96,
  Bonferroni for five tests or every pair tested: no change to the four or the six. Only the difference recomputed on
  the replicates gives five (asserted for each).
- **Convergence of the decisive rung (C1).** Replicates on implicate 1 or on all five, the variance about the
  full-sample value, the between-implicate term in or out, the lower or the interpolated median, z or t: five segments
  (asserted).
- **Clean truth.** On the generator's own wealth before imputation and with every household's true placement, R0 files
  four segments and R3 five (asserted, dataset-generation 7.1).
- **Grid.** Two moves (placement: reference person or older partner; error: without the design, quadrature, or the
  difference on the replicates): four, four, four, six, four and five segments; only the older partner with the
  difference on the replicates gives the golden, and no single-error cell lands on it.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | households in private dwellings in the survey's 2025 wave, as its final weights represent them | filed (the brief, the user guide); SF4 |
| 2 | Unit of account | the household, placed by its older partner's age | filed (the brief); SF1, SF2, SF14 |
| 3 | Attribution window | the 2025 wave's interviews | filed (the user guide) |
| 4 | As-of dating | ages at interview; for the asks, 31 December 2026 | filed (the user guide; the prompt) |
| 5 | Version basis | the public-use release of the 2025 wave | by construction (one release) |
| 6 | Denominator | each group's weighted households | filed (the user guide) |
| 7 | Weighting | the household weight; replicate weights for errors | filed (the user guide); SF4, SF13 |
| 8 | Window length | one wave | filed |
| 9 | Boundary inclusivity | "exceeds" strict; ages 35, 45, 55, 65, 75 open their groups | filed (the brief); SF10; no ratio within 0.3 of 1.96 (asserted) |
| 10 | Rounding path | the test on unrounded estimates; medians and errors rounded for the exhibit, dollars to the thousand at the end | prompt; every graded figure at least $150 from a rounding edge (asserted at build) |
| 11 | Tie-break | none needed: each pair is tested on its own | filed (the brief) |
| 12 | Maturity and censoring | none: one completed wave; for the asks, December deaths reported in January are known at the pull | by construction; the asks' devices |
| 13 | Order of operations | estimate per implicate and replicate, then combine; place households before the medians | filed (the user guide's combining rules); C1 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | five implicate rows per household are one household; for the asks, a merged client number is one client | the user guide (implicates); the register's merge column |
| 16 | Identity normalisation | the household id joins the three survey files; for the asks, client numbers join the insurer's files | by construction |
| 17 | Netting against gross | net worth nets debts against assets by definition | filed (the user guide) |
| 18 | Dimensional units | Australian dollars, whole dollars in the files | filed |
| 19 | Code and status semantics | relationship codes; for the asks, pension types, nomination types, life numbers and statuses | the user guide; the insurer's data dictionary; never the stump |
| 20 | Integerisation | household counts whole; dollars to the nearest thousand | prompt |
| 21 | Clause scope | the brief's rule governs the main call; the PDS and the annuity fact sheet govern the asks' products | filed |
| 22 | Forward window contents | the 2027 range's segments rest on the 2025 wave, the latest the survey has released | filed (the brief) |

## Literal reader

Executed word for word, the prompt and the brief fix the estimand (households in the survey's 2025 wave as its weights
represent them, net worth as the survey defines it, each household placed by the older of its reference person and
partner in the brief's six age groups; each neighbouring pair kept apart when its difference in weighted median net
worth exceeds 1.96 standard errors of that difference, errors estimated with the replicate weights and implicates as
the user guide sets out for any estimate) and name no construction for the error of a difference; every literal
reading of the terms gives the same groups and medians (SF1 to SF16); the difference is itself an estimate, every way
of estimating its error that keeps the survey's design gives five segments (asserted, C1), and four come only from
adding the two groups' errors as if they were independent samples, never from another reading.

## Oracles

None on the main call: the results bulletin publishes medians and relative standard errors by the reference person's
age in the centre's ten-year bands from 30 (none sharing a boundary with the brief's groups), never a difference or the error of one; reproducing it confirms the replicate method on a
single estimate on both the default and the golden path and is declared a wrong-basis distractor (the brief places
households by the older partner). No study, draft or prior paper ranks the boundaries. For the asks, no file carries a
control total: the insurer's extracts hold records, and the PDS and the annuity fact sheet hold terms and rates, none of
which ties to an ask figure under one handling only.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each of the three groups from 55, our customer households holding a Retirement Income Account pension at 31 December 2026, their combined balance and the annual payments set for them for 2026-27 | 9 | the pension book each candidate group's product would take over (a measure every group carries; the call does not turn on it) | the committee's view of the members and money each segment's product would serve | H1 (D8, D7): December 2026 deaths the fund learnt of in January, open at 31 December under the deceased; with a reversionary nominated the pension had passed to the survivor (the PDS), without one it had stopped, so the pensions of members alive at 31 December miss the reverted pensions in every group | D4 (filed at stage 4): a member's partner who is not a Kelvane client appears in no register and is known only from the member's nominations (the dictionary), so a household placed by the register's clients alone sits a group too young when that partner is older; H2 (D8): January 2027 deaths, alive at 31 December, the register's status reading Deceased; H5 (D7, repaired right): 2026 client merges, the pension system still holding the retired number | ria_accounts_20261231 (account_no, member_id, balance, annual payment), crm_clients_20270112 (client_id, household_id, date_of_birth, status, date_of_death, merged_into), ria_nominations_20261231 (account_no, nomination_type, nominee_date_of_birth, relationship), the PDS (death and reversion terms), the brief (placement); 5 files, 14 columns | the register's clients only: 55-64 +11 households, 65-74 +4, 75 and over -29 (balances +2.2M, +0.5M, -11.3M); December deaths dropped: -2, -9, -3; the naive read (every account under its member, merged numbers unfollowed, every register member counted): +7, +42, -14; status filter: 75 and over -37; the answer 442, 1,168, 746 households, $207.7M, $520.5M, $249.6M, payments $11.4M, $30.3M, $18.0M | spouses outside the client register, reversions processed after the year end and merged client numbers are what a superannuation fund's member and client systems hold |
| B, for each of the three groups from 55, our customer households being paid a lifetime annuity at 31 December 2026 and the annual income it was paying them | 6 | each candidate group's annuity book | the annuity income each segment's range would carry | D6: the valuation listing has one row per life; a reversionary annuity's second life carries the amount it would be paid after the first life's death, so the listing's amounts summed over the lives alive at 31 December add income no one was being paid (benign twins: single-life contracts; reversions already in payment, whose first life is deceased) | H3 (D2): amounts as at the 12 January 2027 pull, after the January anniversaries' increase (the fact sheet's rates); H4 (D5): deferred lifetime annuities bought but paying from 80 or 85; H2: January deaths; A's D4 for annuitants who also hold a pension | annuity_lives_20270112 (contract_no, life_no, client_id, date_of_birth, commenced, payments_start, indexation, annual_amount, life_status, date_of_death), crm_clients_20270112, ria_accounts and ria_nominations (cross-holders' partners), the annuity fact sheet (reversion, indexation and deferral terms), the data dictionary; 6 files, 17 columns | every life's amount summed (deferred left out): income +0.8M, +1.6M, +1.1M; deferred kept: households +22, +50, +13, income +0.8M, +1.9M, +0.5M; January increase kept: income +$2k to +$4k; nominations unread: 55-64 +6 households, 75 and over -7; the answer 176, 467, 284 households, $3.6M, $9.0M, $5.6M | reversionary lives in a valuation listing, an extract pulled after the January anniversaries and deferred annuities are what a life office's annuity system holds |
| C, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's differences and intervals | R0 to R3 intervals | the analyst's own exhibit |

- **Main population zero-counts.** No ask device or hazard sits in the survey's three files, its user guide or the brief
  (the call reads no insurer file; asserted: the call computed with every insurer file removed is the same); deleting
  every insurer file leaves the call and Ask C unchanged.
- **Hazard table.** A's D4 moves every A figure and B's households and income where an annuitant also holds a pension
  with a non-client partner nominated; H1 moves every A figure in the groups the December deaths touch (each group at
  least one, asserted); H2 moves A and B under a status filter; H3 moves every B income figure; H4 moves every B figure;
  B's D6 moves every B income figure.
- **Referee.** None for the primaries: the data dictionary defines each column and code (the WHAT, the household's
  partners at a date among them), the PDS states what happens
  to a pension on death, the fact sheet when payments increase and when a deferred annuity starts paying; the dictionary
  files where a non-client partner is known (stage 4), and no file says which deaths reached the fund after 31
  December or that a second life's amount is not being paid.
- **Build figures.** The stops and answers above are the final build's (checks.py asserts every stop off the golden in
  every group, at each figure's rounding).

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A households (3) | pensions open at 31 December, members alive then, merged numbers followed, households from the register's living clients and the filed non-client partners, placed by the oldest of them | 440, 1,159, 743 against 442, 1,168, 746 | miss |
| A balances (3) | the same households' balances | $206,961,000, $514,076,000, $248,006,000 against $207,655,000, $520,479,000, $249,568,000 | miss |
| A payments (3) | the same households' annual payments | $11,411,000, $29,938,000, $17,898,000 against $11,448,000, $30,320,000, $17,994,000 | miss |
| B households (3) | annuities begun by 31 December with a life alive then, deferred annuities included, households from the register and the filed partners | 198, 517, 297 against 176, 467, 284 | miss |
| B income (3) | every such life's listed amount summed | $5,312,000, $12,645,000, $7,200,000 against $3,606,000, $9,011,000, $5,614,000 | miss |
| C the chart | the golden's intervals | right | outside |

Mirror leakage: 6 per cent of the ask weight on the most attractive wrong rung (R0, quadrature): it misses every Ask A
and B figure as the cracker does, and of the chart keeps the axes and the differences, its intervals drawn about half
as wide again as the golden's.
Pair ceiling: 37 (the cracker about 52 with the call, its components and the chart; the quadrature mirror about 22
with the six medians, the 65 and over merge it shares with the golden and the chart's points).

## Build record

- **Generator.** `task261/generator/build.py`: world (the survey's design draw at seed 312, with the two oldest groups'
  own area effect and implicates that differ only on an imputed share of net worth; the design search is
  `search2.py` and `refine.py`, the per-group nudges `binfit.py`), the insurer's retirement book (`insurer.py`),
  records, docs, deliver (the golden from the pack alone), checks (240 assertions: input gates, the bundle against the
  clean truth, R1 to R3c, SF1 to SF16, every route and margin, every ask stop and the cracker sheet, separation,
  distractors, goldens, realism, H21), verify (independent: its own median, replicate and implicate arithmetic and
  table joins), two byte-identical builds, target.zip.
- **Pack.** 14 files in four formats (CSV, XLSX, PDF, DOCX); the household summary 29,940 rows; distractors: the
  results bulletin (declared wrong-basis: medians by the reference person's age in the centre's ten-year bands from
  30, none sharing a boundary with the brief's groups, so no structure for them can be read from it) and the customer
  research summary.
- **Stage 4, loop 0.** Leak reader: nothing names the move, the decisive step read as an analytical choice; it noted
  that the bulletin's then six reference-person groups, their errors added in quadrature, gave rung 0's structure
  (dataset-generation 8.3): the bulletin regrouped (first to five groups, at loop 5 to bands off the brief's), the pack rebuilt, the gates re-run, a re-read
  at loop 1. The judge's first preparation was discarded before its thread ran and prepared again on the final pack.
- **Stage 4, the judge.** r2 DETERMINISTIC on the call (every figure reproduced, Gate G statistical_rigor and
  analytical_non_defect, Gate H analytical), FIX_NOW on Ask A and B's households only: which nominee is the member's
  partner (any nomination type or reversionary only), a partner who died in December still named on the survivor's
  nomination, and one annuity's anniversary on the 12 January pull date. Fixed in the generator: the dictionary
  defines the relationship codes (Spouse the member's husband or wife, De facto partner a person the member lives with
  as a couple) and says nominee details are as the member gave them, not updated by the fund; no annuity starts on the
  pull date's day (one contract from 12 to 11 January, its listed amount and every figure unchanged). r3 (the one
  re-judge) DETERMINISTIC on the call again, the deceased partner and the anniversary closed, and one fork left on the
  same households: how a partner who is not a client is known (a first household line, partners at a date those
  alive on it, read as limiting partners to the register). Filed after the verdict, as task457 filed its second
  pass's ask findings: the nominations file's About line says a member's spouse or de facto partner who is not a
  client is known only from the nominations, whatever their type, and the register's household line says a household's
  partners at any date, clients or not, are those alive on that date. The nominee placement is thereby a filed work
  order, no longer a silent device; the cracker's path now takes it and still misses every Ask A and B figure
  (asserted). Leak reader loops 2 to 5 on each wording; loop 5 read the bulletin's then five reference-person groups
  (55 to 64 at $888,000 against 65 and over at $882,000) as a nudge to merge from 55, rung 0's answer, which a
  wrong-basis distractor may not give (dataset-generation 8.3): its age table moved to the centre's ten-year bands
  from 30, none sharing a boundary with the brief's groups (asserted), re-read at loop 6. Checks 240; every graded
  figure unchanged through every pass.
- **Golden.** Five segments: under 35, 35 to 44, 45 to 54, 55 to 64, 65 and over; medians $69,000, $281,000,
  $534,000, $790,000, $1,048,000, $815,000; errors of the neighbouring differences $24,000, $45,000, $77,000, $95,000,
  $149,000 (2.7 times at 65, 1.6 times at 75). Asks: 442, 1,168 and 746 pension households, $207,655,000,
  $520,479,000 and $249,568,000, payments $11,448,000, $30,320,000 and $17,994,000; 176, 467 and 284 annuity
  households, $3,606,000, $9,011,000 and $5,614,000 a year.
- **Gates.** figures_check exit 0 (198 figures); golden-realism pass (a finding as title, source lines, number formats,
  page footer, a total row, the chart's finding title and labels); containers audited (H1, asserted); leak.py REVIEW,
  no LEAK, each line answered below; guard surface promotes task259 (same domain and objective, two numbers apart; four
  builds apart in draw order, clear of the guard's pairing ban; differentiated on the card); heart PASS, nearest 0.11
  (task229's ledger row, the error of a mean over units failing together).
- **leak.py REVIEW lines.** The brief's 1.96 is the committee's rule, filed once, not an answer figure. The brief's six
  age-group names are the groups the decision is about; it states no structure. The user guide's estimation terms set
  out the error of one estimate and never a difference (asserted: no document carries "difference between two",
  "covariance", "correlat" or "quadrature"). The brief's terms are the committee's rule and the survey's placement. The
  annuity listing's later dates are deferred annuities' income start dates, forward-looking by nature.

## Pre-ship check

- **Rule 1, the domain, on the built pack.** The call is decided by each neighbouring difference's design-based
  standard error, computed from the survey's microdata (29,940 household-implicate rows, 14,038 persons, 200 replicate
  weights); no shipped column holds a median, a difference, an error or a ratio (asserted, R1). With another field's
  nouns the clustered design, its replicate weights and its implicates are gone.
- **Rule 2, two layers.** Layer 1 on the call's path is the release's own structure, each item neutral (asserted, R2):
  implicates stacked as rows, the person file beside the summary, replicate weights in their own file, negative net
  worth, the age top-code; the placement by the older partner is filed in the brief and is a lower rung, not mess.
  Layer 2 is the error of a difference between two domains that share the sample's areas: on the generator's clean
  wealth the quadrature files four segments and the difference's own replicate error five (R3a, R3b).
- **Rule 3, the decisive step.** No shipped sentence says how to estimate the error of a difference (asserted on every
  document); the user guide sets out its general method for any estimate with a single-group example (the judge noted
  at r2 that it executes directly on the difference, the design's own forcing of the HOW), and executing it per group
  with the two errors added files four segments. Nothing planted, copied or withheld carries the answer (R3c); the
  bulletin answers its own question on the reference person's basis and is declared.
- **Determinism.** Every construction of the difference's error that keeps the design (replicates on implicate 1 or
  on all five, the implicates' variance in or out, the lower or the interpolated median, z or t) gives five segments,
  every ratio at least 0.3 from 1.96; the asks' figures are exact under the filed terms (the PDS on reversion and
  death, the key facts on indexation, reversion and deferral, the dictionary's dates, codes and its household and nomination lines), the deflation residual under a
  dollar, and the cracker's path misses every ask figure (asserted).

## Tried and rejected

- Placing the decisive step on the between-implicate variance (Rubin's combination), rejected at the draw: the user
  guide states it for any estimate, so it is a filed method, and on wealth medians it moves each error by under 5 per
  cent, too little to carry a boundary; it stays a lower rung.
- Survey-side asks (each group's household count, home-ownership share or superannuation median), rejected at stage 2:
  they read the main call's files, so no device may sit on their path, and the cracker and the mirror both land them.
- A transition-to-retirement label left at TTR after the member's 65th birthday as Ask A's device, rejected at stage 2:
  determinate only with the PDS's 65 rule on the ask's path, and that filed sentence executes the device.
- Reversionary nominations counted per group as a third Ask A figure, rejected at stage 2: the ask sends the solver to
  the nominations file, the antidote to Ask A's primary device.
- A couple split across two client household numbers as a device, rejected at the draw: it is task260's double
  contract (one entity under two keys) in other nouns.
