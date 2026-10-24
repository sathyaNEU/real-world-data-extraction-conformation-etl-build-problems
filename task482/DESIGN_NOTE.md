# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 11, drawn 2026-10-24 after architectures 1
to 10 were spent at stage 4: a fresh world and pack in the ETL objective, an education technology company's first
settlement of the outcomes guarantee in its partner districts' 2025-26 order forms, each district's share of eligible
students at or above Proficient on a matrix-sampled spring science assessment estimated from the students' own answers
with the district in the population model.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v11, lineage v1 to v10 spent), checked
  2026-10-24 after a fetch of main: WARN, no BLOCK. The first draft (a county school system's own matrix-sampled
  science indicator naming middle schools for coaching) BLOCKed on `ban.org_family` (university_or_school against
  task179 v3), on `test.same_puzzle_older` (objective, G16, designation_set against task182 v1 and task465 v1) and on
  `test.same_driver_older` (objective, G16, method_or_model_selection, spent in four builds). The decisive generator is
  G14 under pattern E (does the pooled model hold for this group: the contractor's background model, pooled over every
  district, does not hold for a district whose students do better or worse than their backgrounds predict), which is
  the honest label for the step that decides, with G16 (the design and the field's principle entitle the
  district-conditioned estimate) as the frame. The setting-word run of `slots` then found task450 (a Texas district's
  own assessment naming the campuses below 40 per cent for coaching) and task464 (a state's literacy grants by a
  performance level) in the same assessment setting, so the world moved off a district's coaching list to a company's
  contract settlement; the role redrew from research_desk (`ban.role` against task179 v3) to portfolio_manager.
- **WARNs answered.** `people.first` (Amy against task130, Robert against task104, Barbara against task460, one older
  build each): kept. People drawn with `guard.py names --geo "United States" --seed 482`: Amy Hardin (the head of
  district partnerships, the requester), Robert Meyers (the director of efficacy research) and Barbara Frazier (the
  controller), owners in file properties only; Lawrence Hughes and Audrey Bautista (architecture 9) and Breanna Graham,
  Jeremy Cortez and John Huang (architecture 10) are not reused.
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL: the
  platform's eligibility file and roster uploads, the delivery system's sessions and scored responses, the contractor's
  item parameters and plausible values, the order forms, the professional learning export and the billing register
  conformed into the guarantee settlement (a row per partner district: the guarantee result and credit, the live
  professional learning hours against the order form and any shortfall credit) and the billing system's credit memo
  import file.
- **The decision and the quantity:** Lumenfold Learning, an online middle-school science platform, licenses to 58
  partner districts in six states (NC 12, OH 11, GA 9, TN 9, CO 9, AZ 8). Its 2025-26 order forms carry an outcomes
  guarantee for the first time (MSA version 4.0, section 9): a district whose Outcome Share, the percentage of its
  Eligible Students (rostered on 1 May 2026 with at least 20 lessons since the start of the term) who completed the spring
  2026 Lumenfold Science Outcomes Assessment whose achievement is at or above Proficient for their grade (500, 520 and
  540 on a scale of 500 plus 50 theta), is below the Guarantee Benchmark on its order form (12 to 35 per cent) is
  credited its Credit Percentage (10, 15 or 20) of its 2025-26 Subscription Fee. The assessment is matrix-sampled: eight
  modules of five items, each student answering two (28 forms), so no student has a score of their own. The contractor,
  Caldrith Assessment Partners, scaled the responses on the 2024 item parameters and drew five plausible values per
  student for the 2026 National Efficacy Report from a latent regression on grade, state, prior state-test band,
  economic disadvantage, English learner status and disability status. The settlement statements are due by 30
  November 2026, the credits issued with them. The quantity is retrospective (the spring 2026 administration is closed)
  because the contract fixes the measurement window; the commitment it drives (the credits on the 2026-27 invoices, or
  refunds) is forward.
- **Shape:** `07`, a grid read district by district: the call (which districts are owed the credit, and the credits'
  total), each district's result against its own benchmark, its live professional learning hours delivered against
  its order form (58) and any shortfall credit (20), and every credit's memo row in the billing system's import layout
  (36): 114 graded figures besides the call's count and totals.
- **Strategy:** `other` (imputations aggregated over a grouping their model left out; no vocabulary key names it:
  composition_mix would need a mix shift and population_selection a denominator, and neither is the move); Gate G
  `method_or_model_selection` (how each district's share is estimated, the design and the field's principle ruling out
  the easy routes); gap `objective` (the plausible values are correct for the national and subgroup figures they were
  drawn for, and are not what a district's guarantee is scored on); pattern E; generators G14 (decisive) and G16. Layer
  2 family `field_method`, pattern `own:plausible values carry only the groupings in their conditioning model, so a
  district's share needs the district in the model`. Calibration organ: none. Context artifact `filed_model` (the
  contractor's technical report, the conditioning variables in its Table 6).
- **World:** the United States, USD; Lumenfold Learning, the Lumenfold Science Outcomes Assessment, Caldrith Assessment
  Partners and the 58 partner districts invented, the districts' place names screened against every populated place of
  500 or more and the US counties (more than two edits from any, no distinctive place word of five letters or more
  inside, H21).
- **Forcing fact:** the settlement statements are due by 30 November 2026 and the credits issue that day.
- **Forum and forcing event:** customer_or_counterparty (the partner districts receive the settlement), period_close
  (the close-out of the 2025-26 subscription year, every district's term settled on its statement by 30 November
  2026). Redrawn at stage 3 from purchase_order_or_contract, which `guard.py heart` BLOCKed on `ban.forcing_event`
  against task306, filed after this draw: the contract is the forum's instrument, and what forces the call now is the
  year's close-out, so period_close is the honest label for the event and not only the passing one. Organisation
  software_or_platform; role portfolio_manager.
- **The physics:** a student's science achievement rises with prior achievement and falls with economic disadvantage,
  English learner status and disability, and a district's implementation moves its students up or down beyond what
  their backgrounds predict (district effects with a standard deviation of 0.45 on the theta scale among the 58, from
  -0.66 to +0.75). Two modules of five items measure one student with a reliability of about 0.68, so each student's
  plausible values lean on what the population model predicts for a student with that grade, state, band and
  background; the model has no district term, so it predicts every student as if their district were average for its
  state and background, and a district's mean over its plausible values keeps about 0.46 of its departure from that
  prediction (the slope across the 58, r = 0.99).
- **Data-native sentence:** each student answered two of the eight modules, so a student's plausible values lean on
  what the population model predicts for a student with that grade, state, prior band and background, and the
  population model has no term for the district.
- **Measured on the pack** (`checks.py`, `verify.py`): averaging the plausible values by district files 19 districts
  (USD 32,045.00), moving 7 districts across their benchmarks by 3.4 to 9.3 points; twelve constructions with the
  district in the population model file the golden's 16 (USD 25,493.75), every district at least 4.05 points from its
  benchmark across all of them; the world's own true shares file the same 16.
- **The WHAT screen.** Population: each partner district's eligible students who completed the spring 2026
  assessment (the contract). Outcome: achievement at or above Proficient for the grade, 500, 520 and 540 on the
  reporting scale. Unit: per cent of students, a district owed a credit when its share is below its benchmark. Window:
  the spring 2026 administration. Comparison: each district's share against its own benchmark. The decisive step settles
  none of them: it is how each district's share is estimated from two-module answers, which no record or filed rule
  states and which the design and the field's principle select.
- **Sources, one line each:**
  - the plausible-values methodology (Mislevy 1991; the NAEP and PISA technical documentation): plausible values are
    draws from each student's posterior given their responses and the conditioning variables, and support analyses of
    the variables in the conditioning model;
  - matrix sampling and balanced incomplete block designs in large-scale assessment;
  - latent regression item response models, marginal maximum likelihood on a quadrature grid;
  - outcomes-based contracting in education technology: guarantees that credit a share of the licence fee when a
    contracted outcome is missed.
- **Same-puzzle and same-driver tests:** (objective, E, designation_set) and (objective, E,
  method_or_model_selection) against the last twelve builds, lineage included: no match.
- **Abstraction test:** the nearest drivers (0.07) stripped of nouns: task271 v3 takes a trait carrier's chance of an
  outcome by a fixed age; task458 counts a population defined by a lasting trait from events logged while observed;
  task479 v4, this setting's nearest relative, estimated campuses with rapid-guessed answers set aside (sent back as
  cleaning contaminated data), and here no answer is set aside and every answer is used; task143 takes the weakest of a
  few members. Also task464, where counting each unit's regression-predicted value against a cut thins the tail and
  the decisive step is estimating a distribution instead of counting predictions: here the plausible values are already
  a distribution, correct for every figure their model covers, and the decisive step is the grouping the model left
  out. And task450, anchor items that changed for the new group: a different step on the same kind of data.

## Default path

1. Read MSA section 9: a district is owed when its Outcome Share, the percentage of its Eligible Students who completed
   the spring 2026 Assessment at or above Proficient for their grade (500, 520, 540), is below its Guarantee Benchmark;
   the credit is its Credit Percentage of the 2025-26 Subscription Fee.
2. Took each district's Eligible Students from the eligibility file's 1 May records and linked them through the student
   crosswalk to the contractor's plausible values file (every student with a submitted session).
3. Computed each district's share the way the technical report computes its results: the percentage of its eligible
   assessed students at or above their grade's level with each of the five plausible values, averaged over the five.
4. Compared each share with the district's benchmark and credited the districts below it.

Ends on: 19 districts owed the outcomes credit, USD 32,045.00 in total.

Golden: 16 districts owed the outcomes credit, USD 25,493.75 in total.

## Stump sentence

The default path averages the contractor's five plausible values by district, the standard use of plausible values,
and files 19 districts owed USD 32,045.00; the values were drawn for the national report from a population model on
grade, state, prior band and background with no district term, so each student's values lean on what students like
them score and each district keeps only about half of its departure from its background prediction, and re-estimating
each district's share from its eligible students' own two-module answers with the district in the population model
files 16 districts owed USD 25,493.75, crediting two districts the easy route clears (Merleywick and Belberbury) and
clearing five it credits.

## Three rules

Task type: item-response-theory-test-equating (Education & Learning Sciences), a task type serving Data Extraction &
Conformation (ETL): the platform's eligibility and roster records, the delivery system's sessions and scored responses,
the contractor's item parameters and plausible values, the order forms, the professional learning export and the
billing register conformed into the 2025-26 guarantee settlement and the billing system's credit memo import.

Domain test: the quantity that decides is each district's share of eligible assessed students whose achievement is at
or above Proficient on a matrix-sampled assessment where no student has a score, which educational measurement
estimates as a group's latent distribution from item responses through a population model; the field's estimator is a
latent regression with the reporting group in the conditioning model (posterior probabilities or plausible values from
it), because plausible values support only the groupings their model conditions on.

Swap: "which hospitals are owed a credit because the share of their patients at or above a level on two of eight
modules of a ten-item assessment, read from the contractor's plausible values, is below the benchmark" stops making
sense: no other field scores a unit's members on two of eight modules each and reports group results only through
draws from a population model, and what decides (the groupings the conditioning model holds) is the assessment
design's own.

Layer 1: each item with the system that writes it, its file, its natural mishandling and what that does to the call,
asserted in `checks.py` R2a to R2f and the SF rows. The delivery system logs an abandoned session before a student's
submitted one and leaves items blank at a session's end as not reached (lsoa_spring2026_sessions.csv,
lsoa_spring2026_item_responses.csv; the abandoned answers scored with the submitted ones, same call, R2e; not reached
scored incorrect, same call, R2b). The platform's eligibility file keeps a mover's record in the district they left and
a re-rostered student's superseded record (guarantee_eligibility_2025_26.csv; the 1 May record flagged eligible
decides, SF8). The crosswalk links a re-rostered student's two IDs to one test taker (student_id_crosswalk_2025_26.csv,
SF9). The districts upload rosters in their states' own codes and prior-test levels
(district_roster_uploads_spring2026.xlsx; Colorado's and Ohio's lowest levels mapped a band apart, same call, R2c; the
roster not joined at all, same call, R2d). Eligibility ignored altogether files the same call (R2a). Each is produced
by the systems that hold it and nothing is placed to be caught; no mishandling moves the golden or files it on the
default path (R2f).

Layer 2: field_method; each district's share at or above Proficient estimated the way large-scale assessment
estimates a group's results from matrix-sampled responses, with the group in the population model, and the
methodological choice that flips the call is whether the conditioning model behind the plausible values holds the
district.

Decisive step: re-estimating each district's share from its eligible students' own scored responses with the district
in the latent regression (as posterior probabilities, or as plausible values drawn from that model), rather than
aggregating by district the contractor's plausible values, whose population model has no district term.

Not semantics: every field can be read correctly (the session statuses, the not-reached and omitted rules, the
eligibility flag, the state codes and bands, the 2PL parameters, the reporting scale and the cuts) and the default path
still files the wrong set, because the plausible values are exactly what the technical report says they are and its
Table 6 lists their conditioning variables correctly; no field, code or definition says they cannot be aggregated by
district.

Not rule application: MSA section 9 files the population, the outcome, the cuts and the comparison, and no filed rule or
procedure says how a district's share is estimated from two-module answers; executing every stated rule with the
technical report's own way of computing results (each statistic with each plausible value, averaged) files 19
districts. Measured on the pack (`checks.py`): the enumerated family (the plausible values by district over the
eligible or every assessed student, as the contractor's posterior probabilities or with each student's mean value
counted; expected a posteriori values counted under the contractor's model, under no model and under the golden model;
maximum likelihood values counted; number correct through the test characteristic curve; and the twelve
district-conditioned constructions) files nine wrong sets of 13 to 25 districts besides the golden's 16, the
plausible-value routes moving districts by up to 16 points; the standing family (the twelve constructions with the
district in the population model: with and without background, a spread per district, district by grade cells, five
plausible values drawn from it under three seeds, fitted on every assessed student, its implied share, each district
fitted alone with and without background, district effects with no grade term) spans at most 4.79 points of share in
any district and files one set, every district at least 4.05 points from its benchmark; what does the ruling out is no
filed clause and no one-line comparison but the design (two modules give a reliability of about 0.68, so a point
estimate's spread is not the population's and a draw leans on its model's prediction) and the data (district effects
with a standard deviation of 0.45 on the theta scale against the contractor model's residual of 0.65), which the
district-conditioned model reads and the contractor's cannot.

Analyst test: with every file read and every rule applied, the easy route computes each district's share from the
contractor's plausible values the way the technical report computes its results and files 19 districts owed the
outcomes credit, USD 32,045.00 in total (the default path's Ends on), two of the golden's districts cleared and five
others credited.

Estimand: MSA section 9 (lumenfold_msa_v4_2025.docx): a district is owed the Credit Percentage of its 2025-26
Subscription Fee when its Outcome Share, the percentage of its Eligible Students (rostered on 1 May 2026 with at least
20 lessons, as the eligibility file records) who completed the spring 2026 Assessment whose science achievement on the
reporting scale is at or above 500, 520 or 540 for their grade, is below its order form's Guarantee Benchmark.

No decoy: nothing is planted to be caught; the plausible values are the contractor's real deliverable for the national
report and correct for every figure it reports (Table 8's grades, states and groups, all in the conditioning model); no
memo, draft or stakeholder figure carries the default path's answer and no file states any district's share.

No certified replay: the method is not hidden and recovered by reproducing certified or published figures; Table 8's
results are for groups both the contractor's model and the golden's carry, so matching them selects nothing, and no
file holds a district result to match.

Lesson: a plausible value is a draw from a posterior that leans on its population model, so it supports only the
groupings that model conditions on; a group the model leaves out is pulled toward what its members' covariates
predict, and its result must be estimated with the group in the model. No build on file teaches it: task450 and
task464 sit in this assessment setting with other steps (anchor items that changed, counting predicted values against
a cut).

## Readability screen

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 number correct through the test characteristic curve | each student's number correct turned into a theta on their form's curve and counted against the cut (13 owed) | the item parameters and forms invite a score per student; the report says ten items are too few for one | readable |
| L4 maximum likelihood counted | each student's own estimate counted (13 owed) | the same | readable |
| L3 expected a posteriori counted, no model | each student's posterior mean under one normal prior counted (21 owed) | the report's statement that results are estimated through a population model | readable |
| L2 expected a posteriori counted, the contractor's model | (25 owed) | the same | readable |
| L1c each student's mean plausible value counted | (24 owed) | the report's statement that a result is computed with each plausible value and averaged | readable |
| L1 plausible values by district (the default) | the share with each plausible value, averaged over the five, over each district's eligible assessed students (19 owed) | the plausible values file and the report's own way of computing results | readable |
| L5 the golden model's expected a posteriori counted | the district in the model, each student's posterior mean counted (18 owed) | the report's statement that results come from a population model | readable |
| G (decisive) the district in the population model | each district's share as the mean posterior probability under a latent regression with district, grade, band and background (16 owed) | nothing names it: Table 6 lists the contractor's conditioning variables without comment, no sentence says a grouping outside them is biased, and no file carries a district result | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the Outcome Share's denominator | Eligible Students who completed the assessment | every Eligible Student, those not assessed counted below Proficient | same call | MSA 9.2 ("of its Eligible Students who completed the spring 2026 Assessment"); asserted |
| SF2 | completed the assessment | a submitted session | any session, abandoned ones included | not computed (an abandoned session is not scored) | technical report section 2; C1: one submitted session per assessed student (asserted) |
| SF3 | Proficient | 500, 520 and 540 in grades 6, 7 and 8 | 500 for every grade | another set | MSA 9.2 and the report's section 3 |
| SF4 | at or above | the posterior mass at or above the grade's cut | above it | same call | C1: the grid's cells end on every cut, so no mass sits on a cut |
| SF5 | the reporting scale | 500 plus 50 theta, 2PL with D = 1 on the 2024 parameters | D = 1.7; parameters recalibrated on 2026 | not computed | technical report section 3 ("not recalibrated", D = 1) |
| SF6 | items not reached | left out of the likelihood | scored incorrect | same call | technical report section 2; R2b |
| SF7 | items omitted | scored incorrect | left out | not computed | technical report section 2 |
| SF8 | an Eligible Student | the 1 May record flagged eligible, one per student | a mover's record in the district left; a superseded record | not computed (neither is flagged eligible) | MSA 9.1 and the eligibility file; C1 asserted |
| SF9 | one student | a test taker; two student IDs linked to one test taker are one student | each student ID a student | same call | the crosswalk; C1 asserted |
| SF10 | the population the model is fitted on | the eligible assessed students | every assessed student | same call | convergent (F5) |
| SF11 | the conditioning covariates beside the district | grade, prior band, the three status flags | grade only | same call | convergent (F1) |
| SF12 | the residual spread | one for every student | one per district | same call | convergent (F2) |
| SF13 | the district's share from the model | mean posterior probability of being at or above the cut | five plausible values drawn from the model, averaged | same call | convergent (F4, three seeds) |
| SF14 | the outcomes credit | the Credit Percentage of the 2025-26 Subscription Fee before any credit, a whole number of cents | net of the professional learning credit | not computed | MSA 1.2 and 9.3; C1: every fee times its percentage a whole cent, so no rounding tie (SF14b, asserted) |
| SF15 | below the benchmark | strictly below | at or below | same call | C1: no district within 4.8 points of its benchmark |
| SF16 | live professional learning | virtual live and on site sessions delivered in the district's subscription term | recorded webinars and on-demand courses counted | the ask only | MSA 8.1 |
| SF17 | a joint session | counts in full for each district attending | counted once, or split | the ask only | MSA 8.2 |
| SF18 | the shortfall credit | USD 250 an hour of the shortfall, the hours delivered counted to the nearest half hour | the hours delivered unrounded; rounded down | the ask only | MSA 8.3 and the prompt; C1: no district's minutes on a quarter hour, so the half hour has no tie (asserted) |
| SF19 | the invoice a credit applies to | the open 2026-27 subscription invoice on the order form's bill-to account with the earliest due date; a refund by check where none is open | any open invoice on the account; a district's other account | the ask only | MSA 10.1 and the import layout |
| SF20 | the credit date | 30 November 2026 | the statement's own date | the ask only | the prompt ("issued on 30 November 2026") |

## Ladder

Measured on the pack (`checks.py`; the share of each district's eligible assessed students at or above Proficient).

| Rung | Districts owed | Flips from the golden | Call kept |
|---|---|---|---|
| L0 number correct through the test characteristic curve | 13 | 3 | no |
| L4 maximum likelihood counted | 13 | 3 | no |
| L3 expected a posteriori counted, no model | 21 | 5 | no |
| L2 expected a posteriori counted, the contractor's model | 25 | 11 | no |
| L1c each student's mean plausible value counted | 24 | 10 | no |
| L1 plausible values by district (default) | 19 | 7 (3.4 to 9.3 points) | no |
| L1a the same over every assessed student | 19 | 7 | no |
| L1b the contractor's posterior probabilities | 19 | 7 | no |
| L5 the golden model's expected a posteriori counted | 18 | 2 | no |
| G golden (district, grade, band, background) | 16 | none | yes |

Every rung files a different set from the golden's, and every rung but L1b a different count; the standing family of
twelve files the golden's set with every district at least 4.05 points from its benchmark (F0). The world's own true
shares file the same 16 (T1), and the default route's error tracks the district effect (r = 0.88, T3).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each district's Eligible Students who completed the spring 2026 assessment | filed (MSA 9.1 and 9.2); SF1, SF2, SF8 |
| 2 | Unit of account | a district's share of students | filed (MSA 9.2) |
| 3 | Attribution window | the spring 2026 administration; the eligibility roster of 1 May 2026 | filed (MSA 9.1, 9.2); C1: every session inside the window |
| 4 | As-of dating | the eligibility file as recorded; the billing register of 20 November 2026 | filed (MSA 9.1; the register's own date) |
| 5 | Version basis | the submitted session, not an abandoned one; the 2024 item parameters | filed (technical report sections 2 and 3); SF2, SF5 |
| 6 | Denominator | eligible students who completed the assessment | filed (MSA 9.2); SF1 |
| 7 | Weighting | every student once | filed (MSA 9.2, a percentage of students); SF9 |
| 8 | Window length | one administration | filed |
| 9 | Boundary inclusivity | at or above the grade's level; below the benchmark | filed (MSA 9.2, 9.3); SF4, SF15 |
| 10 | Rounding path | the share unrounded against the benchmark; credits to the cent | filed (the prompt); C1: no district within 4.8 points |
| 11 | Tie-break | none needed | C1: no family member within 4.05 points of a benchmark (F0) |
| 12 | Maturity and censoring | none: the administration is closed | C1 |
| 13 | Order of operations | eligibility, then the submitted session, then the share, then the comparison, then the credit | filed (MSA 9) |
| 14 | Row order | none | C1: the settlement is order-free |
| 15 | Duplicate resolution | one submitted session per student; one eligible record per student | filed (technical report section 2; the eligibility flag); SF2, SF8 |
| 16 | Identity normalisation | a student is a test taker; two student IDs on one test taker are one student | the crosswalk; SF9 |
| 17 | Netting against gross | the outcomes credit on the fee before any credit | filed (MSA 1.2); SF14 |
| 18 | Dimensional units | theta and the scale (500 plus 50 theta); per cent; USD; hours | filed (technical report section 3; MSA 8.3); SF5 |
| 19 | Code and status semantics | session statuses, response statuses, state roster codes and levels (Table 5) | filed (technical report sections 2 and 4, Table 5); never the stump |
| 20 | Integerisation | hours to the nearest half hour, dollars to the cent | filed (the prompt; MSA 8.3); C1: no district on a quarter hour and every credit a whole cent (SF14, SF18) |
| 21 | Clause scope | section 9 for every partner district's 2025-26 order form | filed |
| 22 | Forward window contents | the credits apply to the 2026-27 invoices open on the credit date or are refunded | filed (MSA 10.1, the import layout); SF19, SF20 |

## Literal reader

Executing the prompt and every filed sentence word for word: MSA 9.2 defines the Outcome Share as the percentage of a
district's eligible assessed students whose achievement on the reporting scale is at or above the grade's level, and
the technical report says no student has a score because each answers ten items, so the share is a property of the
district's students' latent distribution, estimated from their responses. A reader who takes the contractor's
plausible values as that estimate computes a quantity the report defines for its own conditioning variables, which do
not include the district; the reader who estimates the district's distribution with the district in the model lands
the golden under every standing construction (one set, at least 4.05 points of margin in every district). Where the
text is silent on a convention (the fitting population, the covariates beside the district, the residual spread, the
summary of the posterior), the readings converge (SF10 to SF13, F1 to F9).

## Oracles

No file ties only under the golden or only on a wrong read. The pack holds no district share, result or credit; Table 8
reports national, grade, state and group results that both the contractor's model and the golden's reproduce (all in
both conditioning models); Table 6's coefficients describe the contractor's model and rank no district. For the asks,
the catalog's whole-hour schedule and the MSA's rules are the only referees, and no file states a district's delivered
hours or a credit.

## Ask sheet

**Ask A, professional learning: each district's live professional learning hours delivered in its 2025-26 subscription
term against its order form, to the nearest half hour, and any shortfall credit, 58 hours and 20 credits.** H18: a
component of each district's settlement statement (MSA 8.3 credits sit beside the outcomes credit on the same statement
and the same memo import). Use: the statements and the billing import. Primary device (D3, units set per source: hours
and minutes in a decimal column): every offering is scheduled in whole hours, and the scheduling export holds the time
each session actually ran as the scheduling system takes it, hours and minutes after the point (1.40 is an hour and
forty minutes); nothing in the export or the documents says so. A session that ran to time reads the same either way,
so the device lives only in the sessions that ran short or long (192 rows, never past 59 after the point): read as
decimal hours, the field misses 51 of 58 districts' hours and every shortfall credit (0 of 20 right), and setting each
session to its catalog length, the repair round 1's reader A made for the series rows, misses 47 and gets 1 of 20 (AD1,
AD1b, AD2). Evidence split: the export's entries, none past .59, and the catalog's whole-hour schedule, neither enough
alone. Hazards: joint regional sessions sharing a session id across two to four districts (a de-duplication on the
session id misses 29 districts, AD3); rescheduled sessions kept as a Rescheduled row beside the delivered one;
cancellations; recorded webinars and on-demand courses (MSA 8.1); the summer institute's July 2025 and July 2026 cohorts
and July 2026 make-ups against terms running July to June or August to July. Stops: the field as decimal hours keeps 7
of 58 hours and 0 of 20 credits; the catalog lengths 11 of 58 and 1 of 20. Realism: facilitators type an hour and forty
minutes as 1.40 in a duration field, and a scheduler stores it as typed.

**Ask B, the credit memo import: every outcomes and professional learning credit in the billing system's layout, 36
rows.** H18: the settlement's audit trail into billing (MSA 10.1). Use: Billing Operations loads it on 30 November.
Device (D5, out-of-scope rows known only by structure): the 2026-27 invoice register also holds 2025-26 seat true-ups
invoiced after the term closed (their service period the 2025-26 term), professional learning add-ons and lab kit
orders, some open with earlier due dates than the subscription instalments, and six districts' virtual academies bill
on accounts of their own; the earliest open invoice on the account, any description, misplaces 6 of 30 credited
districts' credits (AD4). Hazards: semester instalments (the first paid, the second open), invoices paid before the
register date, three districts without a 2026-27 order (refund by check). Rows coupled to the call: the 16 outcomes
credits (the mirror carries 14 of them); rows coupled to ask A: the 20 shortfall credits.

**Measured, round 1 (zip 632eeb37):** both scored readers filed the default path's 19 districts. Reader A replaced the
series rows' hours with the catalog's hours per session and kept 107 of 110 ask figures (exit 1); reader B summed the
export's hours and kept 17 of 110 (its outcomes memo rows on the 14 districts it shares with the golden, exit 1 on the
per-field count). The series device was re-sited onto the session times, and the readers' memo rows are now scored one
key per row.

Main population: the call reads no session, booking, invoice or catalog row, and the asks read no student (X1, X2).

| Ask | The cracker's path (lands the call, runs the hygiene battery, executes every filed rule) | Kept | Verdict |
|---|---|---|---|
| A | delivered live rows in each district's term, the export's hours read as decimal hours, joint sessions kept, totals to the nearest half hour, credits at USD 250 an hour | 7 of 78 | miss |
| B | the golden's outcomes credits and the cracker's shortfall credits, each applied by the layout's rule | 16 of 36 | miss |

Mirror leakage: 18.4 per cent of ask weight (the default rung keeps 7 hours, 0 credits and 14 memo rows of 114).
Pair ceiling: 39.1 (cracker 56.1, mirror 22.1) on the cut pack, the call's 16 outcomes memo rows the cracker's main
exposure on ask B.
Measured by: task482/generator/ceiling.py (on the cut pack: the export's hours as decimal hours keep 7 of 58 hours and
0 of 20 credits; the memo rows keep 16 and 14 of 36).

## Pre-ship check

1. Domain: educational measurement's own estimate of a group's share at or above a performance level from
   matrix-sampled responses, with the group in the population model; with a hospital's or a utility's nouns no unit's
   members answer two of eight modules and no result exists only through a population model's draws.
2. Real work, nothing planted: every Layer 1 item is what the producing system writes (the delivery system's
   abandoned sessions and not-reached items, the platform's eligibility records for movers and re-rostered students,
   the crosswalk's two IDs, the states' roster codes), each mishandled the natural way in checks.py R2a to R2e with the
   call unchanged; no ask device row reaches the call (X1, X2).
3. The step that flips the call is analytical: estimating each district's share with the district in the population
   model; no clause makes that choice (MSA 9.2 files the share of students at or above the level, the report how its
   own results were computed).
4. Analyst test: every field and rule read correctly, the plausible values averaged by district file 19 districts (L1),
   and every other crude route a different wrong set (L0 to L5); the decisive step alone files the 16 (G).
5. The MSA files the estimand (population, outcome, cuts, comparison) and no estimator; the standing family of twelve
   files one set at a margin of at least 4.05 points (F0), and the asks' conventions are filed (SF16 to SF20).
6. No decoy, no withheld rule against a stated one, no certified replay: the pack holds no district share and no
   figure any construction reproduces.
7. The lesson is on no other card: the nearest driver is task271 v3 at 0.07; task450, task464 and task479 v4 are this
   setting's builds with other steps.

## Architecture 10 record (spent 2026-10-24)

Architecture 10 accrued each Medicare hospice provider number's FY2026 aggregate cap repayment at the December 2026
close, each beneficiary counted under the proportional method on the days to come from their state at the close (an
open stay by its length so far, a live discharge by its time out, returns read at every hospice from the benefit
periods extract), against the default path that runs the open stays on and takes the live discharges as finished
(Fallowmere USD 0.3 million against nothing). At stage 4 all four isolated readers across two rounds missed the call
and the round 1 judge returned DETERMINISTIC, APPROVE; the round 2 judge returned NOT_DETERMINISTIC, SEND_BACK
(margin_or_boundary_fragility and competing_defensible_answer): the printed 0.3 needed Fallowmere's count inside a
window of 2.9 beneficiaries while independent builds of the projection scattered about a beneficiary either way, and
the pool start, the number of later elections and the Kaplan-Meier tail were left unfiled (0.248 to 0.447 on the
judge's variants); ask A's routine-paid days read as an unstated rule. A designation set would have held (every variant
put Fallowmere above its cap); a figure printed to USD 0.1 million on a three-beneficiary window did not.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.
- v10 stage 2, 2026-10-24: a lifetime projection with Brackwater, Lindmoor and Wexmoor owing beside Fallowmere: the
  standing family (Aalen-Johansen or empirical return chances, three valuations of a return, the open stays' later
  returns overall or from their time so far) moves each core program's cap by USD 30,000 to 70,000 against cells of
  USD 100,000, and the overall-rate route kept three of the four amounts; the core programs were placed under the cap
  and Fallowmere carries the call alone (nothing accrued on the default path, USD 0.3 million on the golden).
- v10 stage 2, 2026-10-24: pooled models across provider numbers and a split by discharge reason each moved
  Fallowmere's count by up to 1.3 per cent on cells of small programs; the policy files the reference class (the same
  provider number and diagnosis group), and Fallowmere's seller's system records no revocation against discharge
  reason, so the reason split is not available for its history.
- v10 stage 2, 2026-10-24: with return stays as long as first stays the overall rate times the census average landed
  the golden's cell (0.325 against 0.300); re-elections run shorter (the beneficiary comes back in decline) and seldom
  end alive again, so that route files 0.53 and the census-average valuation by time out 0.19.
- v10 stage 2, 2026-10-24: the outside share of Fallowmere's returns was raised from a third to four in five, so the
  route that reads returns from Elderglen's own records files nothing (cap ratio 0.971) instead of landing beside the
  golden.
- v10 stage 3, 2026-10-24: the organisation and program names Elderglen, Brackwater, Corrinbrook, Dunsmere, Lindmoor,
  Pennacott, Sallowfield and Wexmoor sat within two edits of real places in the GeoNames register (Eden Glen,
  Blackwater, Swallowfield and Fallowfield, Dunmore and Dinsmore, Wyndmoor, Dixmoor) or carried a place word (Penna,
  and Cornbrook in Manchester two edits from Corrinbrook); renamed Wendleglen, Brindlemoor, Corvelfield, Darrelbrook,
  Marrellford, Rennickdale, Varrowmere and Farrinridge in the generator, every figure unchanged. The lines above keep the
  names they were written with.
- v10 stage 4 round 1, 2026-10-24: both scored readers missed the call (each ran the open stays on and took the
  live discharges as finished, nothing accrued) and the judge returned DETERMINISTIC, APPROVE (Gate G analytical, Gate H
  pass); reader A joined the claim lines to the remittance register and kept all 24 ask A figures (exit 1), so the
  device that the latest version is not the paid one sat off the careful path. Re-sited: the contractor's prepayment
  review pays some held inpatient days at the routine rate, visible only by repricing the paid version, with the
  returned replacements kept as a hazard and moved more than 118 days before the close (reader B had priced them as
  pending, cutting payments); the census report's length-of-stay table, blank on a group key mismatch, now prints.
- v10 stage 4 round 2, 2026-10-24, architecture spent: both fresh scored readers again missed the call (open stays
  run on, live discharges finished, nothing accrued) and kept 0 of 24 ask figures, but the judge thread returned
  NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, competing_defensible_answer): Fallowmere's printed 0.3
  needs its count inside 177.6 to 180.5, a window of 2.9 beneficiaries (USD 0.1 million at the cap amount and 98 per
  cent), while independent builds of the same projection scatter about a beneficiary either way (0.248 to 0.311 on the
  judge's variants, 0.279 to 0.314 on the standing family), and it named four choices the policy leaves open (the
  Kaplan-Meier tail, one later election or several, stays begun before 1 October 2016, the last provider number when the
  open stay is at another hospice); it also read ask A's routine-paid days as an unstated counting rule. Lesson: a cap
  repayment printed to USD 0.1 million moves a cell every 2.9 beneficiaries of count, so a projection whose honest
  spread is a beneficiary cannot print one cell; the next architecture's call has to be a quantity whose cell is wider
  than its estimator family's spread, measured on independent builds rather than on the author's own family.
- 2026-10-24, architecture 11 draw, screened on paper before any code against v10's lesson (a call whose cell is wider
  than its estimators' measured spread): Medicare Advantage post-payment recoupments or denial overturns for a
  hospital's 2027 contract notices carry v10's latent structure (a terminal-looking state that is not final) and
  task451's (amounts still to arrive).
- Architecture 11 draw: Medicaid procedural reinstatements and COBRA retroactive elections: retroactive eligibility was
  screened at task451 and task479 v5, and COBRA's selection is population_selection, banned against task275.
- Architecture 11 draw: ACA risk adjustment transfers estimated from competitors' public prior-year transfers: carrying
  a competitor's risk forward is a fork; ACA grace-period cures: rule-heavy, with the cure rate carried across the 2026
  subsidy expiry.
- Architecture 11 draw: censored transplant costs by inverse probability of censoring weights: mature cohorts are
  unbiased without a trend, and a trend makes the stump a dated step; authorization- or ADT-based claims reserves: the
  completion family, and a leading indicator is a reflex.
- Architecture 11 draw: price-standardised total cost of care tiers: the standardisation is a WHAT (filed is rule
  application, unfiled a fork); deductible leveraging is task479 v3's driver; prescription abandonment by out-of-pocket
  cost: the lever is too small; stop-loss and high-cost claimant pooling: non-linear aggregation at claimant level and
  level-dependent counts are closed.
- Architecture 11 draw: hospital coding intensity after an EHR conversion, separated by the same patients' successive
  admissions: adjacent to task453 (a measurement change read from a within-design contrast that nets a drift), the event
  study is the reflex and the WHAT signposts the method.
- Architecture 11 draw: low-voltage anode effect PFCs at aluminium potlines: task459's driver (a ratio with a fixed
  component carried across activity levels), and the IPCC slope method files it; wastewater digester relief-valve
  venting: v9's Gate G risk (an unmetered event inferred from indirect evidence); idle and shut-in wells: a setting clone
  of task462 and task450 v1; stack test-day tune-ups: population_selection and a surface read.
- Architecture 11 draw: a landfill's pre-record waste read from the volume survey: the gas collection record calibrates
  the decay model and absorbs the missing waste; refinery turnaround cycles: a schedule in a file is read; fuel switched
  during gas curtailments: a degree-day normalisation is the reflex.
- Architecture 11 draw: Fellegi-Sunter term-frequency weights: adjacent to task468 (false links on common
  identifiers); address agreement decaying with the gap between records: adjacent to task468 v1.
- Architecture 11 draw: majority-drifted or released anchors (v6, task450); rater severity drift on a shared
  constructed-response subset (task471 v2's driver); rapid guessing in a low-stakes sitting (task479 v4, sent back as
  cleaning contaminated data); speededness and not-reached items (an anchor-drift screen catches them).
- Architecture 11 draw: queue position for open appeals or a coding backlog against timely filing limits: the waiting
  time is a generic queue quantity, so the swap test fails and the domain is a backdrop; censored demand behind
  capacity is task18, task108 and task168; capture-recapture is task199, task243, task248 and task448.
- Architecture 11 draw: newborns and deliveries predicted from current pregnancies in an employer group's renewal: the
  base projection's credibility and trend choices fork, in a large group last year's deliveries already carry the
  component, and the honest strategy (who is in the 2027 population) is population_selection, banned against task275.
- Architecture 11 draw: race and ethnicity imputed from surname and geography for group counts: summing the
  probabilities is the reflex for counts, and the weighting-against-regression choice for rates needs a gold-standard
  subsample, banned against task275.
- Architecture 11 draw: the payroll survey's birth-death model against the lagged QCEW census is reserved for task484
  v2, and drawing it here through a house domain would game the survey x ETL ban against task483.
- Architecture 11 draw, first world: plausible values aggregated by school for a county school system's coaching list
  reskins task450's world and call (a district's own assessment naming the campuses below a share for coaching), so the
  mechanism moved to a company's guarantee settlement with its partner districts.
- Architecture 11 placement, benchmarks by prior tercile (12 to 20 for the lowest, up to 30 for the highest): no
  district the plausible values pull down could cross a benchmark it met, since the strong-implementation districts
  with weak backgrounds sit in the lowest tercile, so benchmarks became whole numbers from 12 to 35 per order form.
- Architecture 11 placement, a 5.5-point margin to the family's envelope with 2.5 points of crossing for every route:
  no maximum likelihood or curve-inversion count crossed anywhere, the routes' upward bias peaking near 9 points; the
  shipped margin is 4 points to the whole family's envelope with 1.5 to 3 points of crossing by route.
- Architecture 11 asks, a series' total on each row with series of up to 12 hours: the hours column summed put most
  districts at two to three times their contract, which reads as wrong at a glance; the series were cut to 3 and 4
  hours and the summer institute booked by day.
- Architecture 11 ask A, the offering's catalog hours on every session row (a series' total on each of its sessions):
  round 1's reader A set the series rows beside the catalog's hours per session and replaced them, keeping all 58 hours
  and 18 credits (exit 1); the catalog every reader opens for the live and recorded formats holds the tell one lookup
  away. Re-sited onto the session times the scheduler holds as hours and minutes after the point, every offering
  scheduled in whole hours so only the sessions that ran short or long carry minutes.
- Architecture 11, credits on quarter-dollar seat prices: a 15 per cent credit on a fee of 11,537.50 is 1,730.625, so the
  cent had a tie that no file breaks (judge pass 1, FIX_NOW); seat prices moved to whole half dollars, every credit a
  whole cent, the call's set unchanged.
Architecture 11 (the contractor's plausible values drawn from a conditioning model with no district term, each district re-estimated with the district in the model), spent at stage 4 round 2 on zip ce5456c3: reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, validated its fit on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75, and kept every ask figure (58 of 58 hours, 20 of 20 shortfall credits, 36 of 36 memo rows) by reading the hours field as hours and minutes from its fractions. A conditioning model that omits the grouping variable is a reflex for a reader who knows plausible values, so the round-3 PD re-site (series credit hours stacked on h.mm) is moot and the slot re-roots.
