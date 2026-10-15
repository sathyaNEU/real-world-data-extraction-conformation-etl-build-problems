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
6. 55-64 and 65-74 differ by about $235,000 against an error of about $145,000 (z about 1.6) and share a segment,
   as do 65-74 and 75 and over (z about -1.5); the range has four segments, 55-64 to 75 and over one of them.

Ends on: four segments, under 35 | 35-44 | 45-54 | 55 and over
Golden: five segments, under 35 | 35-44 | 45-54 | 55-64 | 65 and over

## Stump sentence

The default path files four segments, under 35 | 35-44 | 45-54 | 55 and over, because it takes the error of each
adjacent difference from the two age groups' own standard errors added as if the groups were independent samples;
both groups are drawn from the same 120 survey areas and their medians move together from replicate to replicate,
so the error of the difference recomputed on the replicate weights is about $98,000, not $145,000, and 55-64 stands
apart from 65-74 (z about 2.4), giving five segments.

## Three rules

Task type: complex-survey-estimation-variance (Survey Research & Official Statistics), which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the deciding quantity is the design-based standard error of a contrast between two domain medians in a stratified, clustered, multiply imputed household wealth survey, estimated with its replicate weights and the between-implicate variance; the survey field's own estimator decides which age groups the committee keeps apart.
Swap: "which adjacent school years share a reading programme by median test score" keeps a contrast but loses the survey's strata, areas, implicates and replicate weights that the error is built from; with a generic independent-samples error in place of the design-based one the boundaries move, so the call no longer reads the same.
Layer 1: five implicates per household stacked as rows of the summary extract (the survey's multiple imputation); a person file keyed by household and person number beside a household file keyed by household and implicate (the public-use release); a reference person chosen by an income hierarchy, so the older partner is often the other adult (the survey's household definition); replicate weights in their own file; the bulletin's medians rounded and its errors given as relative standard errors (the publication); negative net worth where debts exceed assets (the questionnaire). Nothing is placed to be caught.
Layer 2: the field-method family; the error of a difference between two age groups' medians is taken from the difference recomputed on each replicate weight, with the between-implicate variance of the difference added, because the groups share the survey's clusters.
Decisive step: estimating the standard error of a contrast between two domains of one clustered sample on the replicate weights, rather than combining the two domains' own standard errors in quadrature as if they were independent samples.
Not semantics: every field, code and definition read correctly (implicates, weights, replicate weights, the person file, the older partner, the bulletin's relative errors) still leaves the analyst combining the two groups' errors as independent, which files four segments.
Not rule application: the brief fixes the threshold and the user guide states how to compute the error of an estimate; no filed rule says how to obtain the error of a difference between two estimates, so executing both still files four segments.
Analyst test: a strong analyst who places households by the older partner, averages the implicates and reproduces the survey's error for each age group, then adds the two groups' variances for each adjacent difference, files four segments, under 35 | 35-44 | 45-54 | 55 and over (Ends on), when the difference's own replicate error files five.
Estimand: the brief files the population (households in the survey's 2025 wave, weighted), the outcome (household net worth as the survey defines it), the unit (the household, placed by the age of the older of its reference person and partner), the window (the 2025 wave) and the comparison (each adjacent pair's difference in median net worth against 1.96 standard errors of that difference).
No decoy: nothing is planted; the bulletin is the survey's own publication, correct for its own question (the reference person's age), and no memo, draft or stakeholder figure argues a structure.
No certified replay: the method is not recovered by reproducing a published figure; the bulletin publishes each age group's median and relative error, never a difference or its error.
Lesson: estimates for subgroups of one clustered survey share its clusters and move together, so the error of their difference comes from the difference recomputed on the replicate weights; no build on file teaches the covariance two domain estimates take from shared clusters (task229's lineage teaches the opposite move, the design effect on one mean).

## Tried and rejected

- Placing the decisive step on the between-implicate variance (Rubin's combination), rejected at the draw: the user
  guide states it for any estimate, so it is a filed method, and on wealth medians it moves each error by under 5 per
  cent, too little to carry a boundary; it stays a lower rung.
