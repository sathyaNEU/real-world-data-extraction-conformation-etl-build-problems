# task260 design note

Merrowdale Breast Screening Service: which AI reading-support tool to license for 2027, from three reader studies.

## Draw

- **Card:** `cards/task260.json`, registered 2026-10-15. Biomedical & Clinical Research, task type
  medical-imaging-reader-study-evaluation (how accurately film readers read screening mammograms with and without an AI
  tool, and whether the difference holds for the service's readers and examinations), objective Descriptive &
  Distribution Analysis; shape 01 (three tools on one score, the gain, behind a gate, the interval above zero, with a
  cap of one adoption); decision pick_one_of_n (one tool, or unaided reading kept); gap population (what the interval
  speaks for: the service's film readers and screening examinations, not the panel and the study set); pattern none,
  G16 then G17; Gate G signal_vs_noise_or_hold; strategy uncertainty_hold.
- **World:** Merrowdale Breast Screening Service, a fictional breast screening service in England, invites women aged
  50 to 71 every three years and reads about 45,000 screening studies a year at four static sites and three mobile
  units, with 26 film readers (consultant radiologists, consultant and advanced practitioner radiographers, breast
  clinicians) double reading every examination. In 2026 it ran one reader study per AI reading-support tool on
  ReadPoint, a fictional reader-study platform: Lumidra Detect (February to April), Ondrix Mammo (April to July) and
  Halvic Breast (July to September). In each study ten of the service's film readers (the panels overlap) read the
  same 300 examinations from the service's 2019 to 2022 archive (75 histology-confirmed cancers, screen-detected or
  interval, and 225 examinations normal at the next round) twice, unaided and with the tool, at least four weeks
  apart, half the panel aided first; each reading records a probability of malignancy (0 to 100) and a recall
  decision. The service's AI evaluation panel (forum committee_or_panel) picks one tool for a two-year licence from 1
  April 2027 (forcing event purchase_order_or_contract) under its evaluation protocol: the largest gain in the
  readers' average area under the empirical ROC curve among tools whose two-sided 95 per cent interval lies above zero
  for the service's film readers reading its screening examinations, else unaided double reading stays.
- **People** (guard.py names --geo UK --seed 260; Laura Atkinson skipped for a first name used in task255): Hayley
  Kelly, the service's clinical director, who chairs the evaluation panel; Darren Jenkins, AI evaluation lead (role
  family procurement_lead), who owns the protocol; Eileen Walton, research radiographer, who ran the three studies;
  Gary Pritchard, procurement manager; Leonard Hilton (Ondrix), Jemma Barnes (Halvic) and Kim Summers (Lumidra),
  the vendors' account managers.
- **Data-native sentence:** each study is fully crossed, so every reader's gain is measured on one shared set of 300
  examinations and every examination's effect is measured through one shared panel of ten; Ondrix's gain swings from
  reader to reader (some readers lean on its prompts and gain a lot, others read worse with it) and Lumidra's sits in
  the examinations its own case score moves for every reader (readers defer heavily to a score weaker than their own
  reads), so an interval that resamples only the examinations admits Ondrix and one that resamples only the readers
  admits Lumidra, and only an interval carrying both (Obuchowski-Rockette or DBM) leaves Halvic's smaller, steady gain
  as the one that holds.
- **Guard:** WARN overuse.shape (01 in 3 of the last 12, never in the last two): the call ranks three tools on one
  score behind a gate with one adoption, a ranked list under a cap of one, and no other shape carries a pick behind a
  statistical gate. WARN repeat.question_form (which, against task458): the call is a pick among three tools or none,
  and a pick asks which (guide-to-prompt 3). Gate G was redrawn from method_or_model_selection (the signature
  population, G16, method_or_model_selection is spent in task134 v1, task104, task501 and task70) to
  signal_vs_noise_or_hold, which is what carries the stump: each tool's gain judged against the noise of the right
  populations. Context artifact redrawn from filed_standard (task257) to operations_log (the ReadPoint exports carry
  the call). Nearest driver 0.05 (task255, lineage).
- **Pairing and shape:** the field's own analysis decides (multi-reader multi-case ROC analysis of a fully crossed
  reader study against a histology-confirmed reference standard), the objective is how reader accuracy and its gain are
  distributed over readers and examinations (the client taxonomy files reader-study evaluation under Descriptive &
  Distribution Analysis), and the call is a pick among three behind a gate (shape 01). Criteria: the call, each tool's
  gain and verdict, the reason each excluded tool fails, the asks' four site counts, the film readers in post and the
  three first-year costs, and the chart's parts.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution`: task253 shrank small noisy
  unit averages (one random factor, a count below a line), task257 counted dimensions on latent correlations, task255,
  task256, task258 and task259 spent tails, conditional distributions, threshold crossings and carried levels; none
  builds an interval over two crossed random factors. `guard.py mechanisms --gate-g signal_vs_noise_or_hold`: task186
  tests each unit's change against noise that carries a cycle shared within a place (one shared component left out of
  a within-unit test) and task128 reads a contact's effect where queues outran the team; this build crosses two random
  factors and each one-factor interval admits a different tool. The client's reader-study pattern 1 (readers and cases
  both random; shortcut pooled ROC and DeLong) gives the family; this build's own version is the three-way split, in
  which the smallest gain is the only one that holds. The client's exemplars carry no reader study.
- **Seed:** DA10 (a credit-union association's 60 merger-readiness engagements shared among leagues by projected small
  credit-union exits) gave the lane's number only: its quantity is a projected exit count shared by a stated rule, a
  forecast the Descriptive lane does not own, and its natural step (a credit union's size class now against when the
  panel first saw it) reads as the size definition once the estimand is filed, so it would be semantics; the world is
  redrawn, as task255 to task257 redrew theirs.
- **Forward facing:** the call picks the tool the service's readers use in 2027 and 2028, a window not yet open; the
  deciding quantity is each tool's gain for the service's readers and examinations, estimated from the 2026 studies.

## Default path

1. Stack the three studies' ReadPoint exports (the third in the platform's newer layout), keep each reading's final
   revision, drop the practice cases at the start of each session, and join each study's case list for the reference
   standard (cancer or normal).
2. For each reader and condition, compute the area under the empirical ROC curve of the probability-of-malignancy
   ratings (Mann-Whitney, ties counted half).
3. Each tool's gain is the panel's average aided area minus its average unaided area.
4. For each tool's 95 per cent interval, bootstrap the study's 300 examinations (cancers and normals resampled
   separately, the ten readers kept as they are) and take the 2.5th and 97.5th percentiles of the gain; DeLong's test
   on the readers' average area gives the same verdicts.
5. Keep the tools whose interval lies above zero (Ondrix and Halvic; Lumidra's crosses zero) and adopt the one with
   the larger gain.

Ends on: Ondrix Mammo
Golden: Halvic Breast

- Ondrix's is the largest gain whose interval clears zero with the panel held fixed (0.042, interval 0.011 to 0.073,
  against Halvic's 0.026; Lumidra's 0.047 runs from -0.013 to 0.108); Halvic is the only tool whose interval stays
  above zero once readers and examinations are both treated as samples of the service's (0.014 to 0.038), and
  Ondrix's (-0.013 to 0.097) and Lumidra's (-0.015 to 0.109) cross zero.

## Stump sentence

The default path bootstraps each study's examinations with its ten readers held fixed and files Ondrix Mammo, whose
interval clears zero and whose gain is the largest that does; the step that lands it there is treating the panel as
the only readers the decision is about, when the protocol's interval is for the service's film readers reading its
screening examinations and Ondrix's gain swings from reader to reader, so only an interval that carries both
readers and examinations as samples (Obuchowski-Rockette or DBM) shows that Halvic Breast's smaller, steady gain is
the one that holds; the opposite one-factor interval (a paired t-test across the readers) files Lumidra Detect.

## Three rules

Task type: medical-imaging-reader-study-evaluation (Biomedical & Clinical Research), which serves Descriptive & Distribution Analysis in the client taxonomy.
Domain test: The deciding quantity is each tool's gain in the readers' average area under the empirical ROC curve of their malignancy ratings against a histology-confirmed reference standard, judged by its multi-reader multi-case interval (Obuchowski-Rockette or DBM, readers and examinations both random), the reader-study field's own analysis of a fully crossed design.
Swap: "Which of three grading apps should a school district adopt, by the gain in its teachers' average marking accuracy whose interval clears zero?" keeps a pick and an interval but loses the ROC area of each reader's malignancy ratings against histology, the enriched cancer set and the fully crossed reader-by-examination design the interval is built on, so the task no longer reads the same.
Layer 1: ReadPoint's export layout changing between platform versions (renamed columns, the probability as a fraction, the recall decision in words), resubmitted readings exported beside the final revision, practice cases at the start of every session outside the study set, per-study pseudonymous reader ids and UTC timestamps on the call's path; on the asks' path the imaging system's migration and its parallel run, mobile units recorded under their own codes and re-hosted mid-year, and technical repeats recorded as separate studies of one screening episode; each is what these systems produce and none is placed to be caught.
Layer 2: field_method, the reader-study field's own method: each study is fully crossed, so every reader's gain is measured on one shared set of examinations and every examination's effect through one shared panel, and an interval speaks for the service's readers and examinations only when it carries both reader and examination sampling (Obuchowski-Rockette or DBM).
Decisive step: Judging each tool's gain with an interval that treats the ten panel readers and the 300 study examinations both as random samples of the service's film readers and screening examinations (Obuchowski-Rockette or DBM), because Ondrix's gain varies from reader to reader and Lumidra's varies from examination to examination the same way for every reader, and each looks precise when only the other factor is resampled.
Not semantics: Every export, case list and protocol clause read correctly still leaves the analyst building an interval, and the bootstrap over examinations with the panel fixed, DeLong's test, or a paired t-test across the readers are each a correct reading of every field; no field, code or definition says how the interval is built.
Not rule application: The protocol states the outcome, the comparison, the populations and the 95 per cent level and leaves the interval's construction to the analyst; executing every stated rule with either one-factor interval files Ondrix or Lumidra, and no filed rule decomposes the gain's variance into its reader and examination parts.
Analyst test: A strong analyst who cleans the exports and reads every rule correctly computes each reader's area with and without each tool, bootstraps the examinations with the readers held fixed, and files Ondrix Mammo, the default path's answer (executed on the generator's clean ratings in checks.py); a paired t-test across the readers instead files Lumidra Detect.
Estimand: The gain in the readers' average area under the empirical ROC curve of their probability-of-malignancy ratings, aided minus unaided, with its two-sided 95 per cent interval, for the service's film readers reading the service's screening examinations; adopt the largest gain whose interval lies wholly above zero, else keep unaided double reading (ai_evaluation_protocol_v2.pdf, sections 3 and 4).
No decoy: Nothing is planted: no vendor, study or interim report states a gain, an interval or a verdict, the vendors' product summaries carry standalone accuracy on their own datasets (another quantity), and no record is copied, withheld or written to carry the wrong answer.
No certified replay: No certified or published result exists for a method to reproduce; the verdicts are forced by the ratings' own structure, where every interval with readers and examinations both random (Obuchowski-Rockette with jackknife or DeLong covariances, DBM, a two-way bootstrap) admits Halvic alone.
Lesson: A fully crossed reader study measures every reader on the same examinations, so an interval that resamples one factor treats the other's variation as fixed and admits whichever tool's gain that factor carries; the field's multi-reader multi-case analysis carries both, and no build on file teaches two crossed random factors (task186 adds one shared within-place cycle, task253 shrinks noisy unit averages).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the examinations resampled with the panel held fixed (a case bootstrap, or DeLong's test on the readers' average area) (default) | none: the protocol files the measure, the comparison, the populations and the level, and no method | one row per reading; nothing marks a factor | yes: resampling the test cases is the opponent's default for comparing two readers or models | none | no | no | readable |
| R1 the readings pooled into one ROC curve per condition, DeLong on the pooled readings | none: the protocol defines the readers' average area | the export stacks every reader's readings in one column | yes | none | no | no | readable |
| R2 the readers resampled with the examinations held fixed (a paired t-test or signed-rank test across the ten readers, or a bootstrap over readers) | none | the per-reader areas form a two-column table that invites a paired test | yes: each reader as their own control is the clinical default | none | no | yes: one paired test on ten differences | readable |
| R3 (decisive) readers and examinations both random (Obuchowski-Rockette with jackknife or DeLong covariances, DBM, a two-way bootstrap) | none names an interval, a variance component or a random factor; the populations clause reads as satisfied by either one-factor interval (resampled examinations speak for the service's examinations, a test across readers for its readers) | no column marks a reader-by-tool interaction or an examination-by-tool effect; both are latent in the ratings | no: the opponent's resampling reflex treats one factor; variance components across two crossed factors are the specialist's analysis | no study report, vendor reader study, published interval or interim result ships | the battery (duplicates, practice cases, revisions, joins, ranges) never measures how the interval is built | no: a variance decomposition over 6,000 readings per study with covariances across readers and conditions and Satterthwaite degrees of freedom | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "gain" | the readers' average aided area minus their average unaided area | the area of all readings pooled per condition | Lumidra (pooled gains 0.061, 0.046 and 0.026; asserted) | the protocol, 3: a reader's accuracy is their own area, and the gain is the readers' average |
| SF2 | "area under the ROC curve" | the empirical (Mann-Whitney) area, ties counted half | a fitted binormal area; the trapezoid rule | another quantity; the trapezoid rule is the same area (asserted) | the protocol, 3: the empirical ROC curve |
| SF3 | the rating | the probability of malignancy | the recall decision as a two-point rating | another quantity | the protocol, 2 and 3 |
| SF4 | a reading submitted twice | the final revision | the first, or both | same call (asserted) | ReadPoint's export guide |
| SF5 | practice cases | not in the study set | read as study cases | same call: they have no reference standard and fall out of the join (asserted) | the export guide and the case lists |
| SF6 | the probability's scale | 0 to 100, or 0 to 1 in the 4.2 export | either | same call: the area is unchanged by the scale (asserted) | the export guide |
| SF7 | interval cancers | cancers (the case lists' outcome) | normal at that screen | another reference standard | the protocol, 2, and the case lists |
| SF8 | the 95 per cent interval | two-sided, each tool's own | one-sided 95 per cent | same call (asserted) | the protocol, 4.1 |
| SF9 | three tools judged | no adjustment for three comparisons | Bonferroni at 98.3 per cent | same call (asserted) | the protocol, 4.1: each tool's own interval |
| SF10 | the populations | the service's film readers reading its screening examinations, both beyond the panel and the study set | the panel's ten readers, or the study's 300 examinations | Ondrix (examinations only) or Lumidra (readers only), each a method on the golden estimand | the protocol, 1.2, 2.2, 2.3 and 4.1: the licence is for the service's film readers on its routine screening (about 45,000 studies a year), and each study's panel is ten of those readers and its set 300 archive examinations |
| SF11 | the interval with both random | any construction | Obuchowski-Rockette with jackknife or DeLong covariances, DBM, a two-way bootstrap, the normal approximation | same call (asserted) | convergent (C1) |
| SF12 | 26 readers, a finite population | no correction | a finite-population correction on the reader variance | same call (asserted) | convergent (C1) |
| SF13 | the order of reading | counterbalanced, no period term | a period term | same call (asserted) | the protocol, 2 |
| SF14 | "largest gain" | among qualifying tools | across all tools | Lumidra (asserted) | the protocol, 4.2 |
| SF15 | cost | assessed after the clinical decision | weighed with the gain | another decision | the protocol, 4.4 |
| SF16 | no tool qualifying | unaided double reading kept | the best of the three | not reached: one qualifies | the protocol, 4.3 |
| SF17 | "the readers' average" | the plain mean over the panel's ten readers | weighted to the service's role mix | same call: every gain moves by under 0.003 and every verdict holds under a weighted two-way bootstrap (asserted) | the protocol, 3.2 (the readers' average) and 2.2 (the panel drawn within each role in proportion to the service's film readers) |
| SF18 | the set's enrichment | no reweighting: each area compares the set's cancers with its normals | each class reweighted to the screening cancer rate (about 8 per 1,000) | same call: a weight per class leaves every area unchanged (asserted) | the protocol, 3.1: the area under the empirical ROC curve |

## Ladder

| Rung | Construction | Verdicts | Pick | Dies to |
|---|---|---|---|---|
| R0 (default) | each reader's empirical area per condition, the panel's average gain, the examinations bootstrapped (cancers and normals separately) with the readers held fixed, or DeLong's covariance of the readers' average | Ondrix and Halvic qualify, Lumidra's interval crosses zero | Ondrix (0.042, interval 0.011 to 0.073, against Halvic's 0.026) | the readers: Ondrix's gain swings from reader to reader (three of the ten read worse with it), and the protocol's interval is for the service's readers |
| R1 | every reading pooled into one ROC curve per condition, DeLong on the pooled readings | all three qualify | Lumidra (the largest pooled gain, 0.061) | the protocol's measure (3) and the readings' dependence |
| R2 | the ten per-reader gains tested across readers (paired t-test or signed-rank, or a bootstrap over readers), the examinations held fixed | Lumidra and Halvic qualify, Ondrix's crosses zero (-0.007 to 0.091) | Lumidra (0.047, interval 0.027 to 0.067) | the examinations: Lumidra's gain varies from examination to examination the same way for every reader (all ten did better with it), and the protocol's interval is for the service's examinations |
| R3 (decisive) | readers and examinations both random: Obuchowski-Rockette with jackknife or DeLong covariances, DBM, a two-way bootstrap | only Halvic qualifies | Halvic | the golden |

- **Position and margin.** Halvic has the smallest gain of the three (0.026 against 0.042 and 0.047, 1.62 and 1.82
  times it; at least 1.15 asserted). With both random, Halvic's gain stands 4.41 standard errors above zero against a
  critical value of 2.10 (18.5 degrees of freedom), Ondrix's 1.60 against 2.09 (19.0) and Lumidra's 1.49 against 1.96
  (1,446); asserted: Halvic at least 3.0 and 0.9 over its critical value, Ondrix at most 1.65 and Lumidra at most
  1.55, each at least 0.4 under its own. With the panel fixed Ondrix stands 2.64 above zero; with the examinations
  fixed Lumidra stands 5.32 against 2.26 and Ondrix 1.93. No bound lies within 0.005 of zero and every gain sits at
  least 0.15 thousandths from a rounding edge (asserted).
- **Every reflex lands wrong.** Examinations bootstrapped (stratified or not), DeLong's test on the readers' average:
  Ondrix; the pooled ROC curve, a paired t-test, a signed-rank test or a bootstrap over readers: Lumidra; only
  intervals carrying both factors give Halvic (asserted for each).
- **Convergence of the decisive rung (C1).** Obuchowski-Rockette with jackknife or DeLong covariances and Hillis's
  degrees of freedom, DBM pseudovalues, a two-way bootstrap of readers and examinations (2,000 resamples), the normal
  approximation in place of t, a finite-population correction for 10 of 26 readers, one-sided 95 per cent and
  Bonferroni at 98.3 per cent: Halvic alone qualifies (asserted).
- **Clean truth.** On the generator's own ratings (no revisions, practice cases or layout drift) R0 files Ondrix, R2
  Lumidra and R3 Halvic (asserted, dataset-generation 7.1).
- **Grid.** Two moves (which factors the interval treats as random; which tools then qualify): examinations only,
  Ondrix; readers only, Lumidra; neither (pooled), Lumidra; both, Halvic. No single-error cell lands on the golden.
  Halvic's two-way bootstrap interval (0.007 to 0.045) is the widest of the both-random constructions and still clears
  zero.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the service's film readers reading its screening examinations, of which each study's panel and set are samples | filed (protocol 1, 4.1); SF10 |
| 2 | Unit of account | the reading; a reader's area per condition; a tool's gain | filed (protocol 3) |
| 3 | Attribution window | each tool on its own 2026 study | filed (protocol 2) |
| 4 | As-of dating | readings as submitted; the final revision | export guide; C1 (SF4) |
| 5 | Version basis | the final revision of each reading | export guide; C1 (SF4) |
| 6 | Denominator | the ten panel readers in the average; each study's 75 cancers and 225 normals in an area | filed (protocol 2, 3) |
| 7 | Weighting | every reader and every examination once | filed (protocol 3) |
| 8 | Window length | one study per tool | filed (protocol 2) |
| 9 | Boundary inclusivity | an interval touching zero does not lie wholly above it | filed (protocol 4.1); no bound within 0.005 of zero (asserted) |
| 10 | Rounding path | the verdicts on unrounded bounds; gains rounded to three decimals at the end | prompt; every gain at least 0.15 thousandths from a rounding edge (asserted) |
| 11 | Tie-break | the largest gain among qualifying tools | filed (protocol 4.2); one qualifies |
| 12 | Maturity and censoring | the reference standard is complete: 2019 to 2022 screens, interval cancers within 36 months known by 2026 | by construction (protocol 2) |
| 13 | Order of operations | clean, area per reader and condition, average, difference, interval | method-level; C1 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | the final revision per reading; practice cases out; for the asks, an imaging record loaded twice is one study and a reader with two contracts one person | export guide; C1 for the call; the asks' devices (ask sheet) |
| 16 | Identity normalisation | per-study pseudonymous reader ids, each study analysed alone | by construction |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | probability of malignancy 0 to 100 (4.1) or 0 to 1 (4.2); costs in pounds excluding VAT | export guide; SF6; the quotes |
| 19 | Code and status semantics | arm and condition codes, recall wording; for the asks, examination codes and booking statuses | export guide and code table; never the stump |
| 20 | Integerisation | costs in whole pounds; counts whole | prompt |
| 21 | Clause scope | the protocol governs the clinical decision; cost is assessed after it | filed (protocol 4.4) |
| 22 | Forward window contents | the licence covers 2027 and 2028 reading by the service's film readers | filed (protocol 1) |

## Literal reader

Executed word for word, the prompt and the protocol fix the estimand (each tool's gain in the readers' average area
under the empirical ROC curve, aided minus unaided, with a two-sided 95 per cent interval for the service's film
readers reading its screening examinations; the largest gain whose interval lies wholly above zero, else unaided
reading) and name no method; every literal reading of the terms gives the same measure and populations (SF1 to SF18),
those populations make readers and examinations both random, every interval built that way admits Halvic alone
(asserted, C1), and Ondrix and Lumidra come from intervals that hold one of the two populations fixed, never from
another reading.

## Oracles

None on the main call: no study report, interim analysis, vendor reader study or published interval ships. The
vendors' product summaries carry each tool's standalone area on the vendor's own datasets, a declared wrong-basis
distractor ruled out by the protocol, 3 (the measure is the service's readers' accuracy with the tool); the screening
KPIs carry rates by screening year (April to March), no counts; the readers' 2025 self-assessment scores are another
test.
None bears on the gains or the intervals on either path, and none ties to an ask figure under any handling.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, screening studies each of the four sites, mobile units included, sent for reading in the 12 months to 30 September 2026 | 4 | the volume the vendors price on, traced from the imaging system's records to each site | each site's deployment and the per-study quote | D1: during each site's go-live fortnight on the new RIS part of its studies were also registered in the legacy RIS, and the legacy history load brought those records in again under their legacy accession numbers with the legacy local clock in the UTC field, so a copy matches its original's time before 29 March and sits exactly an hour later after it; genuine same-day pairs (implant-displaced views registered as a second routine study, 4 to 12 minutes apart) sit beside them | D7 the mobile unit code MBSU2 carried over in June 2026 to the replacement vehicle hosted by Wendlow (the location table carries only the current host; the visit schedule shows the old vehicle's host, Corrowby Road); D5 assessment and symptomatic mammograms in the same export (code table); D4 cancelled bookings; D8 the window by study date | ris_mammography_studies (accession, patient_ref, study_datetime, location_code, exam_code, status, images, views), ris_examination_codes (exam_code, programme), screening_locations (code, type, site, host_site), mobile_unit_visits (Unit, Host site, From, To); 4 files, 18 columns | no deduplication: Corrowby Road +149, Wendlow +72, Copse Lane +227, Tallowmere Park +191; same woman, day, location and code deduplicated: -151, -90, -191, -194 (implant pairs lost); exact-time deduplication: +99, +72, +227, +191 (copies after 29 March kept); the location table's current host: Corrowby Road -5,152, Wendlow +5,152; the answer 11,569, 7,298, 13,253, 13,758 | a migration with a parallel run, a replaced vehicle keeping its unit's code and implant views as a second study are what a screening service's imaging records hold |
| B, each tool's cost in its first contract year under its vendor's quote | 3 | each candidate's cost, which the protocol assesses after the clinical decision (4.4) | the licence budget | D1: a technical recall on a later day registered under the routine screening code when the woman came back to another site or unit opens no second screening episode; only her second routine study weeks after the first (and, on new-RIS rows, its one or two views) shows it (Lumidra prices per episode, one per woman and screening round, counted with its routine study) | Ask A's copies and implant pairs (Ondrix prices per study received); Ask C's reader count (Halvic prices per reader seat and per site, Lumidra per reader account); D8 the extract's first fortnight: 14 technical repeats of routine studies made before 1 October 2025 (their episodes began before the 12 months); each quote's minimum charge and one-off fee | as A, with the three quotes and the workforce list; 8 files, 22 columns | routine study days counted as episodes: 44,386 against 44,262 (124 later-day recalls), Lumidra 111,003 against 110,745; every woman with a screening study counted: 44,276, Lumidra 110,774; Ask A's same-day deduplication: 45,252 studies, Ondrix 88,108 against 89,122; employee numbers counted: 28 seats and accounts, Halvic 104,200 against 101,750, Lumidra 111,085; the answer | per-study, per-episode and per-seat prices are how screening AI is sold |
| C, film readers in post on 1 April 2027 | 1 | the seats the licence and the training cover | the per-seat quote and the training plan | D7: one reader holds a substantive post and a bank contract, two employee numbers and one professional registration number, the bank row under the full legal name with a middle name | D8 a retirement on 31 March 2027 and a starter on 1 April 2027; a reader whose post changed in July 2026 (two rows, one registration, the old row ended; the key's benign twin); D5 mammographers and assistant practitioners who do not read films | film_reader_workforce (Employee number, Name, Professional registration, Reads films, Start date, End date); 1 file, 6 columns | employee numbers counted: 28; names counted: 28 (the bank row's name differs); the answer 27 | double contracts and changed posts are what an HR extract of a hospital workforce holds |
| D, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's gains and intervals | R0 to R3 intervals | the analyst's own exhibit |

- **Main population zero-counts.** No ask device or hazard sits in the ReadPoint exports or the case lists (asserted:
  no RIS, location or workforce field in any export, and the call computed with every ask file removed is the same);
  deleting every ask file leaves the call and Ask D unchanged.
- **Hazard table.** The copies (A primary) move every site in A and Ondrix in B; MBSU2's carried-over code moves
  Corrowby Road and Wendlow in A and nothing in B (Ondrix prices the total); the later-day technical recalls (B
  primary) move Lumidra only; the double contract (C primary) moves C, and Halvic and Lumidra in B; implant pairs move every site
  in A and Ondrix under a same-day deduplication.
- **Referee.** None for the primaries; the code table and the location table define each code (the WHAT only), and
  the visit schedule's host is per visit block; no filed sentence says the history load repeated the go-live
  fortnight, that a later-day technical recall can carry the routine code, or that a reader holds two contracts.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A studies per site (4) | completed MAMS and MAMT studies by code and status, mobile units through the location table, the overlap deduplicated on woman, day, location and code | Corrowby Road 6,326, Wendlow 12,300, Copse Lane 13,062, Tallowmere Park 13,564 against 11,569, 7,298, 13,253, 13,758: every site off (asserted for every deduplication and host pairing) | miss |
| B Ondrix | per study received at the cracker's Ask A total (45,252) | 88,108 against 89,122 (asserted) | miss |
| B Lumidra | one episode per woman with a routine study (the quote's round), reader accounts at the employee-number count (28) | 111,085 against 110,745 (asserted) | miss |
| B Halvic | per seat at the employee-number count (28), per site | 104,200 against 101,750 (asserted) | miss |
| C readers in post | film readers in post on 1 April 2027 by employee number | 28 against 27 (asserted) | miss |
| D the chart | the golden's intervals | right | outside |

Mirror leakage: 5 per cent of the ask weight on the most attractive wrong rung (Ondrix on the bootstrap over
examinations): it misses every Ask A, B and C figure as the cracker does, and of the chart keeps the axes and the gains,
its intervals drawn with the panel fixed.
Pair ceiling: 34 (the cracker about 52 with the call, its verdicts, reasons and the chart; the Ondrix mirror about 16
with the gains and two of three verdicts).

## Build record

- **Generator.** `task260/generator/build.py`: world (26 readers with persistent traits, panels drawn within roles,
  three studies from seeds 146, 195 and 32 chosen by a search against this note's margins, the RIS year with the
  go-live fortnights, the visit schedule, the workforce), records, docs, deliver (the golden from the pack alone),
  checks (190 assertions: input gates, bundle against the clean truth, R1 to R3c, SF1 to SF18, every route's pick,
  margins, every ask stop and the cracker sheet, separation, goldens, realism), verify (independent: scipy's
  Mann-Whitney, a brute-force jackknife, its own Obuchowski-Rockette and asks), two byte-identical builds, target.zip.
- **Pack.** 18 files in four formats (CSV, XLSX, PDF, JSON); the RIS export 55,920 rows; the three ReadPoint exports
  6,456, 6,474 and 6,465 rows; distractors: the vendors' product summaries (declared wrong-basis: standalone areas
  rank Lumidra first), the screening KPIs and the readers' self-assessment scores.
- **Golden.** Halvic Breast: gains 0.047 (Lumidra), 0.042 (Ondrix), 0.026 (Halvic); intervals with both random
  -0.015 to 0.109, -0.013 to 0.097 and 0.014 to 0.038; 3 of Ondrix's 10 readers read worse with it, all 10 of
  Lumidra's better; 45,878 screening studies (Corrowby Road 11,569, Wendlow 7,298, Copse Lane 13,253, Tallowmere
  Park 13,758), 44,262 episodes, 27 film readers; first-year costs Lumidra 110,745, Ondrix 89,122, Halvic 101,750.
- **Gates.** figures_check exit 0 (30 figures); golden-realism pass (source line, number formats, chart title and
  zero label); containers audited clean; leak.py REVIEW, no LEAK (the call's frame words in the protocol and quotes,
  site lists that rank nothing, forward-dated workforce rows); guard surface clean (0 promoted; personas on the
  card); heart WARN (overuse.shape, repeat.question_form, answered in the Draw), nearest 0.05.

## Pre-ship check

- **Rule 1, the domain, on the built pack.** The call is decided by each tool's multi-reader multi-case interval on
  the readers' empirical ROC areas, computed from the three ReadPoint exports (one row per submission; 6,456, 6,474
  and 6,465 rows) against the case sets' histology-backed outcomes; no shipped column holds an area, a gain, an
  interval or a verdict (asserted). With another field's nouns the reader-by-examination ROC design and its two
  random factors are gone.
- **Rule 2, two layers.** Layer 1 on the call's path is the platform's own mess, each item neutral (asserted): the
  4.2 layout with the probability as a fraction (same areas), resubmissions (56, 74 and 65 second submissions; the
  first submission in place of the last leaves the call), practice cases opening every session (outside the case
  sets, they fall out of the join), per-study reader ids and UTC times. Layer 2 is the interval's random factors,
  which no cleaning step touches: on the generator's clean ratings the easy route files Ondrix and the decisive step
  alone files Halvic (R3a, R3b).
- **Rule 3, the decisive step.** No filed sentence names a variance method, a random factor or a resampling unit
  (asserted on every shipped document after "at random" was taken out of the protocol); protocol 4.1 files the
  populations only. Executing every stated rule with an interval that resamples one factor files Ondrix or Lumidra;
  nothing planted, copied or withheld carries the answer (R3c), and the product summaries' standalone areas rank
  Lumidra first on another basis (declared in metadata.json, ruled out by protocol 3).
- **Determinism.** Every interval with readers and examinations both random (Obuchowski-Rockette with jackknife or
  DeLong covariances, DBM, a two-way bootstrap, the normal approximation, a finite-population correction, one-sided
  95 per cent, Bonferroni) admits Halvic alone; the asks' devices each have one handling that reproduces the
  generator's truth exactly (asserted), and the cracker's path misses every ask figure.

## Tried and rejected

- One fully crossed study of four conditions (unaided and the three tools) on the same readers and examinations,
  rejected at the draw: the textbook Obuchowski-Rockette or DBM analysis of four conditions pools the variance
  components across them, so every pairwise interval has one width and the largest gain qualifies first; a pooled
  analysis could never pick the smallest gain, and the design forked between pooled and pairwise analyses. Each tool
  now has its own two-condition study, as a sequential procurement runs them, so no pooling exists.
- Lumidra's lift drawn as a mixture of lifted and lowered cancers, rejected in the prototype: lowering a visible cancer
  costs more area than lifting a subtle one gains, so the net gain went negative across seeds; replaced by readers
  deferring heavily to Lumidra's own case score, which is weaker than their own reads.
- Panels of 18 and 12 readers, rejected in the prototype: a gain that fails a test across readers needs a reader
  spread near 0.1 in area with 18 readers; ten readers, the protocol's panel size, needs about 0.08.
- Ondrix's reader spread tuned at 0.72 latent standard deviations, rejected at stage 3: one reader fell from 0.813 to
  0.684 and another rose to 0.981. The case-driven tool now carries the largest gain, so the default path no longer
  needs Ondrix to fail a test across readers, and Ondrix's spread is 0.55 (readers' changes -0.065 to 0.125).
- The names Ardelle, Quintara, Velmora, Wynford, Ellerby, Stannard and Ashby Cross, rejected at the house-fix pass: a
  first name the persona scan reads, a real company, an invented name in task126, a real village, names in other
  builds and the client's exemplars; renamed Halvic, Ondrix, Lumidra, Wendlow, Corrowby, Tallowmere and Lindhallow,
  and the mobile units' locations given invented venue names in place of common surgery names.
- "Drawn at random" and "sampled at random" in the protocol's panel and study-set clauses, rejected at the leak pass:
  two sentences calling both factors random samples point at the decisive step; protocol 4.1 alone files the
  populations.
- Per-site invitation counts in the KPI distractor, rejected: a figure a solver could hold the site counts against.
- One template for the three vendors' quotes, rejected after the leak reader read them as one generator's output:
  each vendor's proposal now carries its own layout, typeface, section names and footer.
- A GMC number on a radiographer's row (the reader whose post changed in July), rejected after the leak reader: the
  changed post is now an advanced practitioner radiographer's promotion, and the bank system records the registration
  number without its GMC or HCPC prefix, so the double contract shows only once the numbers are compared.

- An episode count resting on a 28-day grouping no shipped file stated, rejected by the determinism judge: every woman
  with a screening study gave 44,276 (14 women whose only study is an early-October repeat of a September screen) and
  a 28-day window by the clock 44,263 (one recall 28.09 days after its screen). Lumidra's quote now counts one
  episode per woman and screening round, in the period of its routine study, and every window converges (asserted).
- Lumidra priced on episodes alone once the episode was pinned, rejected: the cracker's per-woman count landed its
  cost. Lumidra's quote now also charges a reader account for each film reader in post, so the double contract that
  holds Halvic's cost holds Lumidra's too.
- A blank FTE and a prefix-free registration on the one bank row of a double contract, rejected after the leak
  re-read as a marker: every bank row now carries the bank system's conventions (no contracted hours, the bare
  registration, the full legal name), and a mammographer holds a double contract too.
- One sentence of scope and terms shared by the three quotes, rejected after the leak re-read: each vendor now
  writes its own scope, basis and commercial terms.

## Stage 4

- **Leak reader (loop 0).** Question 1: no file names the decisive step; protocol 4.1 states a population and no
  method. Questions 2 to 4: none (the vendors' standalone areas read as a labelled lure, declared). Question 5:
  protocol 3.1, 3.2 and 4.1 fix the measure and the populations, the reader declining to name a pick without
  computing. Question 6: an analytical choice (how the interval is built from reader and case variation). Every
  REVIEW line harmless. Realism tells fixed in one generator pass: the quotes' shared template, a GMC number on a
  radiographer's row. The reader's "gain for the service's reader mix" reading is closed as SF17 (protocol 3.2 files
  the readers' average; role weighting moves no verdict, asserted). Uniform visit lengths and polite venue names kept
  as texture.
- **Determinism judge (loop 0).** NOT_DETERMINISTIC, FIX_NOW, on Ask B's Lumidra cost only: the episode grouping was
  unfiled (44,276 every woman, 44,263 a 28-day window by the clock, 44,262 the golden). The call reproduced under
  Obuchowski-Rockette, DBM and a two-way bootstrap (Halvic 0.014 to 0.038; Ondrix and Lumidra crossing zero), and
  every other ask figure reproduced. Gate G: statistical_rigor, analytical_non_defect, no surface-read dependency, no
  sole data defect. Gate H: domain pass, layers pass, decisive step analytical. Residual risks noted: the location
  table's host without a date (Ask A), and one reader's washout of 27.8 days by the clock against the protocol's four
  weeks.
- **Leak re-read (loop 1).** Question 1: no file announces the decisive step; protocol 4.1 states the populations
  only. No file ranks the tools on the question; nothing reads as the answer. Every REVIEW line harmless. New reading
  closed: reweighting the enriched set to the screening rate (SF18, same areas). Realism tells: the bank row's blank
  FTE as a marker, the quotes' shared sentences.
- **Fix pass (one generator pass).** Lumidra's quote pins the episode (one per woman and screening round, counted in
  the period of its routine study) and adds a reader account per film reader in post; the location table defines
  host_site as the host at export; the second condition's sessions start at least 29 days after the first's, so the
  washout holds by the clock; bank rows share one convention and a mammographer's double contract joins the
  reader's; each quote has its own scope and terms. The call, the gains, the intervals, the studies, the episodes and
  the film readers are unchanged; Lumidra's first-year cost is now 110,745.
- **Leak re-read (loop 2, after the fix pass).** Question 1: no file announces the decisive step; protocol 4.1 fixes
  the populations and names no method. No ranking, no answer-like figure; question 6 an analytical choice. Every
  REVIEW line harmless; the location table's host at export and the staff list's double contracts read as layered,
  credible records. Nothing to fix.
- **Determinism re-judge (loop 1, the single re-judge after FIX_NOW).** DETERMINISTIC, APPROVE: every figure
  reproduced from a fresh unzip (gains 0.047, 0.042, 0.026; only Halvic's interval above zero under
  Obuchowski-Rockette and a two-way bootstrap; 45,878 studies by site, 44,262 episodes, 27 film readers, costs
  110,745, 89,122 and 101,750). Gate G statistical_rigor, analytical_non_defect, no surface-read dependency, no sole
  data defect; Gate H domain pass, layers pass, decisive step analytical. Its one minor fork, routine studies alone
  as the site count (11,351, 7,163, 13,003, 13,495), already closed by the code table and Ondrix's quote, is pinned
  in the prompt as the thread suggested ("routine and technical-repeat screening studies"); no figure or file moved,
  voice-check and precut pass, and the leak reader read the new wording (loop 3).
- **Leak re-read (loop 3, after the prompt pin).** No file announces the decisive step; the prompt's new phrase says
  what to count, not how to repair a record. The reader's case-mix question (screen-detected against interval
  cancers) is closed by protocol 3.1's empirical area on the study set, with no service mix in the pack to weight
  to. Realism tells kept as texture. Ready to ship.
