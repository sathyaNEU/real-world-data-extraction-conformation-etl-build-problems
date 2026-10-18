# task198 design note

Motu Korero Research, a survey research institute running Tatauranga Aotearoa's continuous Household
Living Conditions Survey under contract. Whether the rise in dwellings with damp or mould that the
survey measured in Manawatu-Whanganui is established as a population change, and so whether that
region's 2027 Q1 addresses are issued to a fresh interviewer panel.

**Architecture 3 is live.** Architectures 1 (pensions answer-time) and 2 (interviewer attribution by
measurer portability, and its approved repair) are spent; both carry `### ARCHIVE` headings below and
their fates are in the card's `lineage` and in `## Tried and rejected`. Architecture 3 keeps
architecture 2's world, pack and variance component and moves the decision from a pick of one region to a
characterisation of one named region's move, which is the positive clause of the rule architecture 2's
death filed in `stumping` Part 3: a decisive step that moves a variance cannot carry a ranking, but it can
carry a verdict on one named candidate against a stated threshold.

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task198.json`, architecture v3, registered 2026-10-18, forum redrawn to `operations_desk`; `guard.py check` re-run against the registered card as the last act of stage 1 and returning **PASS**, no BLOCK and no WARN |
| Domain / subdomain | `survey-research-official-statistics` / `anomaly-detection` |
| Objective | Anomaly Detection & Diagnostics (fixed by the lane's task-number block) |
| Shape | 18, hypotheses versus evidence: the rival explanations for the move are the grid's cells |
| Decision type | `structural_verdict`, answer unit `rate_or_share`, question form `whether` |
| Gate G | `signal_vs_noise_or_hold` |
| Strategy | `uncertainty_hold`: the interval a record ships with is computed over groups that do not contain the error source that produced the move |
| Layer 2 family | `estimation_fit`, pattern `own:replication-groups-miss-the-error-source` |
| Gaps | `objective` (decisive), `population` |
| Generators | G3 record versus operation (decisive), G17 statistical rigor |

**Pairing.** Survey research is the one field that ships the uncertainty of its own estimates as data,
in replicate weights, and the question of whether a replication-based variance estimator spans the error
source at issue is the field's own: replicate weights formed on primary sampling units estimate sampling
error, the interviewer is not a sampling unit, and the published interviewer design effect exists because
that component sits outside the design variance.

**Data-native sentence.** In this pack each primary sampling unit is worked by one interviewer and each
interviewer works units across every stratum, so the interviewer groups cut across the replication groups
the design supplies: no replicate the file ships ever varies the interviewer composition of the named
region's quarter, and the only record that identifies the interviewer grouping is a workload log the field
operation keeps for pay and travel.

**The pincer case (case two, `stumping` 1.2b).** The between-interviewer component is a quantity the
records measure about their own production: the national workforce measures it directly (10.08 points on
218 interviewer-quarters), the field log fixes the grouping exactly, and nothing states it and nothing has
to be recovered as a rule.

**The pricing sequence, all four steps run before a word of design** (`stumping` Part 3).

1. **The residue is a method, not a knob.** With the estimand and the threshold filed, what stays open is
   over which groups the replication is formed. The alternative is not a value on a dial: it is PSU
   replication, which the design documentation supplies and which every microdata user applies, against
   grouping on the field workload, because units sharing an interviewer are not independent. Both are
   named, published positions. No tolerance, no cut-off, no nearest-k, no rounding. It is also none of the
   five parts of the WHAT: it is how the uncertainty of a fully filed quantity is estimated.
2. **The move available against the move needed.** To turn the supplied verdict over, the interval has to
   widen by `3.53 / 1.96 = 1.80`. Re-forming the replication over the workload widens it by
   **f = 3.95**. **Available 3.95 against needed 1.80, a ratio of 2.19.**
3. **The standard error of what the step must estimate.** The between-interviewer component, from the whole
   workforce: **4.1 per cent relative standard error**, and the estimator family (one-way random-effects
   ANOVA, REML, method of moments) spans **6.73 to 6.74 on the same data, 0.15 per cent**. The verdict holds
   at the family spread, at the relative standard error, at a 25 per cent error and at a 50 per cent error.
4. **The lever and the ranked quantity's noise are not the same variance, because nothing is ranked.** The
   region is named in the prompt and the lever acts on a threshold the framework states, which is the
   positive clause of the rule architecture 2's death filed. The residual exposure is that the realised
   change must land between the two intervals, which happened in 2 of 6 seeds at each rise setting, about a
   third; the generator fixes the seed and no role is hostage to it, because there is one region and one
   verdict rather than a loud and a quiet candidate to be kept apart.

**The general lesson, worth more than this build.** A verdict is a coin with two faces, so a screen that
only reads which side of the bar each route lands on is worthless: the abandoned first tuning had the right
faces, every reflex filing the supplied verdict and the golden filing not established, and no margin at
all, with the golden at z 1.83 against a 1.96 bar and the flip 8 per cent of the variance component away.
It would have shipped. What makes a verdict architecture sound is the distance to the flip, measured, and
the only honest defence of an interval-based call is that nothing in the estimator's own family can move
it: 61 per cent, fifteen relative standard errors, four hundred times the family's own spread. Measure the
margin, never the face.

**Measured margin, which is the number that matters and not the face.** The verdict is a coin with two
faces, so the sweep measures the distance to the threshold rather than which side of it a route lands on.
`sigma_int` would have to fall from 10.08 points to **3.94**, a fall of **61 per cent** and about **15
relative standard errors**, before the golden verdict flips to the supplied one.

**Sources read, one line each.**

- `guard.py check`: PASS, no BLOCK, no WARN. Nearest driver 0.07 (task195), then 0.06 (task452 v1), 0.05
  (task98 v3). Architecture 2's own driver does not reach the top four, so `test.own_lineage` is clear on
  the driver as well as on the axes.
- `guard.py mechanisms --objective anomaly-detection`: the three self-measuring builds are task192 (a
  validation subsample's rates and whether they transport outside their window), task195 (shared specimens
  making two screens' calls dependent) and task194 (two vintages measuring their own coding lag). This
  build's self-measuring quantity is what a supplied variance estimator spans, which is none of them.
- `stumping` Part 3, read from the skill: the variance-cannot-rank rule and the four-step pricing sequence,
  both run above.
- `determinism-check` sections 1, 3 and 5: the method may stay open only where the data forces it; the
  call's robustness is not the figures' determinacy; a robustness claim is graded over the whole range it
  names.

**The forum, and the window mechanism that cost two redraws.** `ban.forum`, `ban.forcing_event` and
`ban.org_family` run on the last three builds by draw time, and **registering this card reshuffled that
window itself**, because architecture 2's card had been sitting in it. So a forum that cleared before
registering can collide after: `committee_or_panel` collided with task166 and `customer_or_counterparty`
with task471, both of them after this card was filed. The check that counts is therefore the one run
against the **registered** card as the last act of stage 1, not the one run on the draft. The forum was
then drawn on the act rather than off the free list: no formal forum signs a quarterly regional figure, and
the act the verdict feeds is the field operations desk issuing the region's 2027 Q1 addresses to a
different interviewer panel, so `operations_desk` is honest where `executive_team` (which also cleared) is
the same stretch as `regulator_or_inspector` here. `period_close` and `research_or_statistics_office` are
clean on the same window.

**Build requirements this draw owes.** The field workload log reads as an operations record kept for pay
and travel and explains nothing. The quality framework and the commissioning letter pose a question and
name no method. The questionnaire change note states the item's wording and routing, not what to do about
them. No note says a file is the wrong basis. Every graded figure is records-fixed except the two
intervals, which are graded only because their estimator family is closed to 0.15 per cent, asserted.

## Default path

The pipeline a competent and careful analyst builds, using the most rigorous instrument the pack supplies.

1. Read `quarterly_release_2026q4.xlsx` for orientation: the provisional regional figures.
2. Notice the release is provisional and the comparison quarter has been revised, so rebuild from the
   dwelling records: stack `hlcs_dwelling_records_layout_a.csv` and `hlcs_dwelling_records_layout_b.csv`,
   confirm from `questionnaire_change_note_2026.pdf` that the damp-or-mould item's wording and routing are
   unchanged across the layouts, and take interviews achieved in the field quarter and the same quarter a
   year earlier.
3. Rebase Manawatu-Whanganui across the territorial authority amalgamation with
   `regional_boundary_concordance_2026.csv`, and confirm the rise holds on both bases.
4. Apply the calibrated weights the dwelling records carry.
5. Compute the change: **+6.6 percentage points**.
6. Rule out each rival explanation on a shipped fact: the mode mix from `mode_assignment_log.csv`, the
   layout change from the change note, the base change from the concordance, the vintage from the release's
   own revised column, seasonality by the comparison being the same quarter a year earlier, and the frame
   vintage from `dwelling_frame_vintage_note.csv`.
7. Judge the change with the survey's own supplied replicate weights, as `sample_design_documentation.pdf`
   directs: `hlcs_replicate_weights_2026q4.csv` and `hlcs_replicate_weights_2025q4.csv`, 84 jackknife
   replicates each. Standard error **1.86 points**, so the change is **3.53** standard errors, far past the
   framework's stated 95 per cent bar.
8. File the rise as an established population change, and leave the region's 2027 Q1 addresses with their
   existing panel.

Ends on: the rise is established as a population change, +6.6 points at 3.5 standard errors
Golden: the rise is not established, +6.6 points at 0.9 standard errors once the replication spans the
field workload, so the region's 2027 Q1 addresses go to a fresh interviewer panel

## Stump sentence

A competent solver rebuilds both quarters across the two questionnaire layouts, rebases the region across
the amalgamation, rules out every rival explanation the pack carries on a shipped fact, judges the +6.6
point change against the survey's own supplied replicate weights at 3.53 standard errors and files the rise
as an established population change, because every replicate the pack ships is formed on primary sampling
units and no replicate ever varies the interviewer composition of the quarter, so the interval cannot see
the one source that produced the move.

## Three rules

- **Task type:** `survey-research-official-statistics` / `anomaly-detection`, which serves Anomaly
  Detection & Diagnostics; the build works the field's own complex-survey variance estimation on a probed
  prevalence item whose collection the field workload log records.
- **Domain test:** the quantity that decides is what a replication-based variance estimator spans, which
  survey research settles by asking whether the replication groups contain the error source; replicate
  weights formed on primary sampling units estimate sampling error and omit the interviewer component, so
  the correct interval groups the units that share an interviewer and is wider by a factor set by the
  workload concentration.
- **Swap:** rewritten as "whether a district's megawatt-hour rise is established" there is no sample
  design, no replicate weights and no field workforce whose groups could differ from the sampling units, so
  there is nothing for a replication group to miss and the task stops existing.
- **Layer 1:** two questionnaire layouts spanning the comparison; a territorial authority amalgamation
  changing the published base; a provisional figure beside a revised one for the comparison quarter;
  face-to-face and telephone collection with different field periods inside the quarter; the workload log
  at assignment grain against the dwelling records' dwelling grain; interviewer identifiers recycled when
  field staff are re-engaged; design weights and calibrated weights both present; management stamps in UTC
  against New Zealand local time across a daylight saving change. Nothing is placed to be caught, and each
  item is a cell of the shape-18 grid that dies to a shipped fact.
- **Layer 2:** `estimation_fit`: the interval the record ships is computed over replication groups formed
  on the sampling structure, and the error source that produced the move acts on groups the record never
  replicates over, so the supplied interval understates the move's spread by a factor set by how
  concentrated the field work was.
- **Decisive step:** re-form the replication over the groups the field workload log identifies, the units
  that share an interviewer, or equivalently add the between-interviewer component the national workforce
  measures, which widens the standard error from 1.86 to 7.37 points and drops the change from 3.53 to 0.89
  standard errors.
- **Not semantics:** both routes read every field, code, unit and definition the same way, build the same
  achieved sample on the same two quarters at the same grain, apply the same weights, the same layout
  stacking and the same rebasing, and reach the same +6.6 point change; they differ only in which groups
  the replication is formed over, and no field, code or definition in the pack states that the supplied
  replicates omit a component.
- **Not rule application:** the quality framework files the five parts of the estimand and states the 95
  per cent bar, and the design documentation states the general replication method for the weights it
  supplies, but no filed sentence, column or procedure says that units sharing an interviewer are not
  independent, nor that the replication should be re-formed over the workload log; executing every stated
  rule in the pack, with the most rigorous instrument it supplies, files the rise as established.
- **Analyst test:** a strong analyst who stacks both layouts, rebases the region, reads every field
  correctly, rules out each rival on a shipped fact and then judges the change with the survey's own
  supplied replicate weights files the rise as established, because it clears that interval by 3.53
  standard errors.
- **Estimand:** filed in one sentence in `quality_framework_2026.pdf`: the change, in percentage points,
  in the share of occupied private dwellings with damp or mould observed or reported at interview, between
  the field quarter and the same quarter a year earlier, for the region on the amalgamated base, over every
  dwelling interview achieved in those quarters; reported as a population change only where it is
  significant at the 95 per cent level.
- **No decoy:** nothing is planted to be caught. The supplied replicate weights are correct for what they
  estimate and are formed exactly as the design documentation says; every interviewer carries a
  differential, as every real workforce does; the release states its own provisional basis and ranks
  nothing; the workload log records assignments as a field operation records them, for pay and travel.
- **No certified replay:** no published or certified figure is reproduced only by the golden method; the
  release's provisional and revised figures and the change itself tie under both routes, which differ only
  in the interval.
- **Lesson:** an interval is only evidence about a move if its replication groups contain the source that
  produced the move, and a survey's supplied replicate weights are formed on the sampling structure, not on
  the field operation, so the one error source a field workforce introduces is the one the shipped
  uncertainty cannot see. No build on file teaches it: task192 turns on a validation rate's reach, task195
  on a paired interval over shared units and task194 on when records arrive.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 release figure | the release states its own provisional basis | the release's own columns | yes, read the dashboard | none | no | yes, read off | readable |
| 1 rebuilt change | the framework files the window and the item | the dwelling records' columns | yes, the obvious group-by | none | the battery finds the layout and base joins | one group-by | readable |
| 2 supplied replicate weights (**the default path**) | the design documentation states the replication method for the weights it supplies | 84 replicate weight columns, named | yes, the rigorous reflex, and it is the right instrument for sampling error | none | no | one standard formula | readable |
| 3 replication re-formed over the field workload (**decisive**) | no sentence says units sharing an interviewer are not independent, nor that the replication should be re-formed | the workload log is at assignment grain and carries no outcome; the grouping must be built across three files | no: every reflex files the supplied verdict, measured, ten of them at z 2.38 to 4.14 | no control or published figure ties only under it | the battery passes under both replications | not a subtraction or a ratio of a reported figure; the component is estimated from the whole workforce | silent |

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the field quarter" | 2026 Q4, 1 October to 31 December | the fiscal quarter | `same call`, asserted | `quality_framework_2026.pdf` 2.1 names the field quarter and its dates |
| SF2 | "the same quarter a year earlier" | 2025 Q4 | the preceding quarter | `same call`: the change on 2026 Q3 is 1.1 points and not established either way, asserted | the framework's own words |
| SF3 | "damp or mould" | observed or reported at interview, the single item | the observed sub-item only | `same call`, asserted on the figure to one decimal | the change note states one item with unchanged wording and routing |
| SF4 | "the region" | Manawatu-Whanganui on the amalgamated base | the pre-amalgamation base | `same call`: the change is 6.4 points on the old base, asserted | the concordance; the framework names the amalgamated base |
| SF5 | "significant at the 95 per cent level" | a two-sided normal bar at 1.96 standard errors | a t bar on the replicate degrees of freedom | `same call`: 3.53 clears and 0.89 fails under both, asserted | the framework states the 95 per cent level; the convergence is asserted |
| SF6 | which weights | the calibrated weights the dwelling records carry | the design weights | `same call`: the change is 6.5 points, asserted | the framework names the published weighting |
| SF7 | the replication groups | the groups the field workload identifies | the primary sampling units the file supplies | the decisive step; closed by the data, not by a sentence: see `## Literal reader` |
| SF8 | provisional against revised | the revised figure for the comparison quarter | the provisional | `same call`: the change is 6.7 points on the provisional, asserted | the release carries both and labels them |
| SF9 | rounding path | once at the end, one decimal place in points | per quarter then differenced | `same call`, asserted | the prompt's last sentence |
| SF10 | "a population change" | a change in the dwellings, not in the measurement | any change in the published figure | the verdict itself | the framework defines the reported change as a change in the population |

## Ladder

Four rungs, four distinct verdicts or figures. Each reproduces from the raw files and dies to one shipped
fact or construction.

| Rung | Analysis | Verdict | Figure | Dies to |
|---|---|---|---|---|
| 0 | the release's provisional regional figures | established | +8.1 points | the release labels itself provisional and the comparison quarter revised; the framework's window and base are the rebased ones |
| 1 | rebuild on the filed window, item, base and weights, test on a simple random sample basis | established | 4.14 standard errors | the design is stratified and clustered, so a simple random sample variance is not the survey's own |
| 2 | the survey's own supplied replicate weights (**the default path**) | established | +6.6 points at 3.53 standard errors | the replicates are formed on primary sampling units and no replicate varies the interviewer composition of the quarter |
| 3 | replication re-formed over the field workload (**decisive**) | **not established** | +6.6 points at 0.89 standard errors | nothing: the golden |

**Arithmetic, measured on the clean truth.** Supplied standard error 1.86 points against a correct 7.37,
inflation **f = 3.95**, against the 1.80 the verdict needs, a ratio of **2.19**. The named region's panel is
four interviewers with squared workload shares summing to 0.250 in each quarter. The between-interviewer
component is 10.08 points, measured on 218 interviewer-quarters outside the region.

**Reflex sweep, run as code before these separations were measured, ten reflexes, every one filing the
supplied verdict.** Supplied replicate weights 3.53; design standard error linearised on units 3.53;
bootstrap of the design, units within strata 3.40; simple random sample 4.14; trim the most extreme unit
each quarter 3.70; trim the three most extreme 3.77; stratify on visible interviewer attributes 3.53;
shrink the region 25, 50 and 75 per cent toward the national change 3.14, 2.76 and 2.38. **None reaches the
golden verdict**, and the nearest, three-quarter shrinkage at 2.38, still clears the bar by 21 per cent.

**Margin across the estimator range.** `sigma_int` must fall 61 per cent, to 3.94 points, before the
verdict flips: about 15 relative standard errors, and 400 times the estimator family's own spread.

**Grid.** Every cell of the rival-explanation grid is a named alternative that dies to a shipped fact (mode
mix, layout change, base change, vintage, seasonality, frame vintage), and every one of them leaves the
+6.6 point change and the supplied verdict standing, which is what makes the grid the construction layer
rather than the stump: cleaning the data does not decide the verdict.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every dwelling interview achieved in the region in the two quarters | framework 2.1 files it; no interview is pending at the extract |
| 2 | Unit of account | the region for the verdict; one row is one dwelling interview | framework names the region; the records are one row per interview |
| 3 | Attribution window | the quarter the interview was achieved in | framework 2.1; C1, no interview on a quarter boundary |
| 4 | As-of dating | the field quarter's close; the workload log as the field operation closed it | framework 2.2; the dates are in the file names and the manifest |
| 5 | Version basis | the revised figure where the release carries both | SF8; `same call` asserted |
| 6 | Denominator | dwelling interviews achieved, per quarter | framework 2.1 in its own words |
| 7 | Weighting | the calibrated weights the records carry | SF6; `same call` asserted |
| 8 | Window length | two quarters, the field quarter and the same quarter a year earlier | framework 2.1 |
| 9 | Boundary inclusivity | 1 October and 31 December inclusive | framework 2.1; C1, no edge case |
| 10 | Rounding path | once at the end, one decimal place in points | prompt's last sentence; asserted |
| 11 | Tie-break | none needed: the verdict is a threshold with 61 per cent of room | measured |
| 12 | Maturity and censoring | none: both quarters are closed and every interview is achieved | by construction, asserted |
| 13 | Order of operations | stack the layouts, then rebase, then weight | C1: the three commute on this record, asserted |
| 14 | Row order | file order cannot move a weighted mean or a replicate variance | C1 by construction, asserted over three permutations |
| 15 | Duplicate resolution | one interview per dwelling per quarter, identified by the dwelling key | C1 asserted on the de-duplicated count |
| 16 | Identity normalisation | interviewer identifiers recycled across the series; the roster carries the start and end dates that split them | `interviewer_roster_2026.csv`; C4, the raw read merges two people |
| 17 | Netting against gross | no netting: the change is a difference of two shares | framework has no offset |
| 18 | Dimensional units | percentage points throughout; the workload log in completed interviews | the framework and the log state both; C4 |
| 19 | Code and status semantics | the item's response codes are identical across layouts | the change note; never the stump |
| 20 | Integerisation | interview counts are whole; shares are not rounded before the end | by construction |
| 21 | Clause scope | the framework's 2.x governs the estimand and the bar; the design documentation's 4.x governs the replicate weights it supplies | each document names its scope |
| 22 | Forward window contents | the committed window (2027 Q1) holds no interviews: the verdict is about the closed quarters and the action is the panel the coming quarter's addresses are issued to | the framework files the quantity on closed quarters and the letter sets the 2027 Q1 decision |

## Literal reader

Executed word for word, `quality_framework_2026.pdf` files the estimand and states that a movement is
reported as a population change only where it is significant at the 95 per cent level, and
`sample_design_documentation.pdf` states the general replication method for the weights it supplies.
Neither says over which groups the replication must be formed when a movement is judged, and that is what
the data closes rather than a sentence: each primary sampling unit is worked by one interviewer and each
interviewer works units across every stratum, so the supplied replicates hold the interviewer composition
of the quarter fixed in every one of the 84 replicates, and the independence the supplied variance assumes
is contradicted by the workload log itself. Every licensed reading of the estimand's terms gives the same
+6.6 point change (SF1 to SF9, asserted), and the verdict is determinate under both bars (SF5) and across
the whole estimator family for the component, which spans 0.15 per cent, with 61 per cent of room to the
flip.

## Oracles

- `quarterly_release_2026q4.xlsx` reproduces on its own stated provisional basis under every method,
  golden and supplied alike, and presents regions in code order with no ranking and no interval. It
  confirms nothing about the verdict.
- `sample_design_documentation.pdf` and the replicate weight files tie to each other under both
  replications, because the supplied weights are correct for the sampling error they estimate; neither
  ties only under the golden.
- `population_benchmarks_2026.csv` ties to the calibrated weights under both routes, which is the Ask 2
  referee and hands over no interval.
- No control, published figure or reconciliation column in the pack ties only under the re-formed
  replication. The workload log records assignments as a field operation records them and explains nothing.

## Ask sheet

Three asks, 25 graded ask figures, solved by `generator/asks_measure.py`. Ask 1 is the one free
construction figure both responses bank; Ask 2 is a mirror device the cracker recovers by executing a
filed rate; Ask 3 carries the cracker's misses. The devices are re-skins of proven components, which is
permitted; no driver is re-skinned.

| Ask | Figures | Use | Primary device | Hazards | File and columns | Stops and lazy delta |
|---|---|---|---|---|---|---|
| 1 | 1: the national change in the item across all regions, in points | the commissioning letter opens on the national picture | none by design: it sits in the call's own population, where the separation line forbids a device row | the two layouts, the amalgamation base, the provisional and revised columns | both dwelling-record files, 9 columns | provisional basis 1.4; golden 0.4 |
| 2 | 4: the interviews the field cost claims cover in each 2026 quarter | the field operation owes the commissioning agency a cost reconciliation | D6 grain, a paper row covering many units of work: the three largest field areas are paid on a consolidated monthly claim covering every assignment completed in the month, and the claim carries no interview count, so the interviews are recovered as the claim amount over the schedule's per-interview rate | the schedule's two rate periods, to 30 September 2026 and from 1 October 2026 | `field_cost_claims_2026.csv`, 7 columns; `field_payment_schedule_2026.pdf` | lines counted as interviews 1,086 / 1,125 / 1,158 / 1,113; golden 1,788 / 1,860 / 1,914 / 1,839 |
| 3 | 20: the ten largest territorial authorities, each with its benchmark population at 30 June 2026 and its achieved interviews per 1,000 | the quality report reports achieved interviews per 1,000 benchmark population by authority | D9 self-validation, a rollup above its own parts: where authorities were amalgamated the demography team returns one benchmark for the amalgamated area against each constituent, so nine of the ten carry a group total, and the tenth is returned by another team and carries no figure at all. The per-area figure is in the published table, split into two age bands with no total anywhere in the pack | the amalgamation concordance; one authority's code changed mid-series | `population_benchmarks_2026.csv`, 4 columns; `published_population_table_2026.pdf` | nine grouped areas take the group total; the tenth is blank |

**Separation line.** Zero device rows and zero hazard rows sit in the main call's declared population. The
call reads the two dwelling-record files, the two replicate-weight files, the design documentation, the
quality framework, the boundary concordance, the questionnaire change note, the mode log, the frame
vintage note and the field workload log; Ask 2's devices are in `field_cost_claims_2026.csv` and
`field_payment_schedule_2026.pdf`, Ask 3's in `population_benchmarks_2026.csv` and
`published_population_table_2026.pdf`, and the call reads none of those four. Deleting every device leaves
the verdict, the change and both intervals unchanged, asserted by count in `generator/checks.py`.

**Measured forcing, per device, on the ask-side truth.** Ask 2: the natural read returns 1,086 against the
golden's 1,788 in the first quarter and the **smallest quarterly gap is 702 interviews**, on figures stated
in whole interviews. Ask 3: the **smallest gap between the group-total rate and the golden rate on a
grouped authority is 6.3 per 1,000** and the largest is 8.8, against a 0.05 bin half-width, so the nearest
device is forced by a factor of 126; for the tenth authority the file carries no figure at all. No graded
benchmark figure ships verbatim: each is the published table's two age bands added, asserted in
`verify.py`.

**Referee.** `field_payment_schedule_2026.pdf` arbitrates Ask 2's disagreement and states no interview
count; `published_population_table_2026.pdf` arbitrates Ask 3's and states no authority-level rate and no
total.

The cracker is the response that landed the verdict, ran the hygiene battery, executed every filed rule
the pack points at and matched every published figure it carries. Ask 3 is the primary it is measured
against; one row per move it makes, and the verdict is whether that move reaches the device.

| Cracker move | What it does on Ask 3's benchmarks | Verdict |
|---|---|---|
| key uniqueness | every authority code is unique in the benchmarks file | miss |
| exact duplicates | no two rows are equal; the repeated benchmark figures sit on rows differing in code, name and returning team | miss |
| unmatched joins | the blank benchmark for the tenth authority is a visible gap that sends the reader to the published table for that one authority only | miss |
| fan-out and count ties | the file is one row per authority, so nothing fans out and no count ties | miss |
| executes every filed rule the pack points at | the dictionary states the column is the benchmark as returned by the demography team; nothing in the pack says a return may cover an amalgamated area | miss |
| matches every published figure | the pack ships no benchmark total, in the file or the published table, so there is no control for the file to fail against | miss |

**What the landing response banks, figure by figure.** `asks_measure.py` has the cracker keeping **7 of the
25** graded ask figures: Ask 1's national change, because it is computed over exactly the rows the call's
own comparison is computed over, where the separation line forbids any device row; Ask 2's four quarterly
counts, because the schedule's per-interview rate is a filed rule and every consolidated claim is an exact
multiple of it, so a response that executes the schedule recovers the count and making it unrecoverable
would break law 6; and the tenth authority's two figures, because the blank sends any reader to the
published table. The mirror keeps three of those seven: Ask 1's figure and the blank authority's two. It
loses Ask 2's four because it counts claim lines as interviews, and the other eighteen because it takes
the benchmarks file's group totals.

**Pair ceiling:** 39.5, solved on Part 0's weights (38 recommendation and critical components, 7
instruction-following, 55 asks) with both responses rescored from their own readings and both columns
printed: the cracker lands the verdict and keeps 7 of 25, scoring 38 + 7 + 55 x 0.2800 = **60.4**; the
mirror stops at rung 2 and files the rise as established, counts claim lines as interviews and takes the
benchmarks file's group totals, keeps 3 of 25 and scores 5 + 7 + 55 x 0.1200 = **18.6**. The two ask
columns differ because the mirror does not execute the schedule and does not notice the grouped return, not
because any ask consumes the call's construction.

**Mirror leakage:** 12.0 per cent of ask weight.

**Measured by:** `generator/asks_measure.py`, which at this stage solves on the generator's clean truth
in `generator/core.py` and prints both columns; at stage 3 its figure lookups are re-pointed through
`verify.py`'s own bundle pipeline so the ceiling is measured on what ships rather than on the truth. It
exits 1 unless the pair is at or under 40 and the leakage under 35, and it also prints each device's
forcing gap. Re-run after every change to the asks or the pack.

**Mirror leakage:** 12.0 per cent of ask weight.

**Rounding sentence, and the figures it governs.** The prompt's last sentence governs the change in points,
the standard error and Ask 3's ten rates, all to one decimal place. Ask 1's national change is in points to
one decimal; Ask 2's four counts and Ask 3's ten benchmark populations are whole numbers that no rounding
sentence governs. `verify.py` carries this list and checks each figure's printed precision in the shipped
write-up, because `figures_check.py` compares values and cannot see precision.

### ARCHIVE architecture 2 (spent): Draw

Motu Kōrero Research, a survey research institute running the national statistics office's continuous
Household Living Conditions Survey under contract. Which region's rise in dwellings with damp or mould
takes the one boosted sample in the 2027 Q1 field quarter.

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task198.json`, architecture v2, registered 2026-10-18, `guard.py check` WARN, no BLOCK |
| Domain / subdomain | `survey-research-official-statistics` / `anomaly-detection` (assigned ground) |
| Objective | Anomaly Detection & Diagnostics (fixed by the lane's task-number block, task180 to task227) |
| Shape | 07, grid of cells: the region by interviewer grid of the quarter's achieved sample |
| Decision type | `pick_one_of_n`, answer unit `named_option` plus one observed rate |
| Gate G | `decomposition_attribution` |
| Strategy | `other`: a measured difference between units attributed to the person who collected it rather than to the unit, identified by that person's portability across units |
| Layer 2 family | `estimand_identification`, pattern `own:measurer-portability-across-units` |
| Gaps | `objective` (decisive), `population` |
| Generators | G3 record versus operation (decisive), G14 conditioned yield |

**Pairing.** Survey research is the one field whose own estimators measure the error its own production
introduces, and the interviewer component is its signature one: the interviewer design effect
`1 + (m - 1) rho_int` is published for probed items precisely because the workforce, not the population,
moves them. The decision is the field's own triage question, which of a set of regional movements is the
population's own, and the quantity that settles it is an error component the field estimates from the
random allocation of issued addresses among the interviewers working an area.

**Why this ground, under the pincer.** The decisive step is case two of the pincer (`stumping` 1.2b): the
interviewer component is a quantity the records measure about their own production, not a fact about how
they were produced. Nothing states it, nothing has to be recovered as a rule, and it is exactly computable
from shipped columns, because the allocation of addresses to interviewers is random within area and the
sample management log records it.

**Data-native sentence.** In this pack the regions differ in how few people collected them: a region's
quarter is worked by two to twelve interviewers, every interviewer carries a differential on an item that
has to be probed, and a minority of interviewers work more than one region because rural workloads cross
territorial authority boundaries, so the record contains the same interviewer's own differential measured
away from the region that looks worst, which is the only thing that separates her from it.

**Priced ceiling, computed before any row is cut** (`stumping` Part 3, and the rule this slot earned).
At an item prevalence of 0.20 the person-level SD is 0.400, so the between-interviewer SD of the realised
rate is `0.400 x sqrt(rho_int)`: 5.66 points at `rho_int` 0.02, 8.00 at 0.04, 9.80 at 0.06, all inside the
published range for probed items. An interviewer 1.8 SD out carrying a 0.65 workload share lifts her
region's measured rate by 6.62 points at `rho_int` 0.02 and **9.36 points at 0.04**. The ladder needs about
**4.5 points**: enough to put the loud region above the golden on the measured ranking, and enough to leave
the golden ahead once the differential is attributed. **About 9.4 available against about 4.5 needed, a
ratio of about 2.1.**

**And the two separations are financed by independent quantities**, which is the structural contrast with
architecture 1 and with task194's architecture 3. Separation 1, the easy route must file the loud region,
is financed by the lift, `workload share x interviewer differential`. Separation 2, the golden must lead
once the differential is attributed, is financed by `golden true rise - loud true rise`. Those are set by
different parameters, so buying one does not spend the other, and the ratio above holds at every lift:
at lifts of 4.0, 6.0 and 9.4 points the golden's lead after attribution is 2.0 points throughout. Both
numbers are re-measured on the cut pack before the ladder is accepted.

**Build requirements this draw already owes.**

- **Orthogonality.** The interviewer differentials are drawn independent of everything that predicts the
  item, and the correlation is measured and asserted near zero, so that no finer standardisation on a
  visible attribute reaches the golden for free.
- **No size tell.** The loud region is not simply the smallest. Its concentration comes from a staffing gap
  in the quarter (one of its interviewers on leave), so `corr(decisive measure, region size)` is measured
  and asserted near zero at the decision grain.
- **The dangerous reflex.** Leave-one-interviewer-out re-ranking must land wrong, which requires the golden
  region to carry a dominant interviewer too. The full reflex sweep runs as code before any separation is
  measured: interviewer fixed effects, clustering on interviewer, leave-one-out, trimming the extreme
  interviewer, weighting by workload, standardising on interviewer count.
- **Documents pose a question.** The survey's quality framework and the commissioning agency's letter ask
  which movement is the population's own and name no method; no note says a file is the wrong basis, and
  nothing explains the structural break the answer depends on.

**Sources read, one line each.**

- `guard.py mechanisms --objective anomaly-detection`, 31 builds, every spent driver read before drawing.
  The three self-measuring builds are task192 (a validation subsample's error rates and whether they
  transport outside their window), task195 (shared specimens making two screens' calls dependent) and
  task194 (two vintages measuring their own coding lag); this build's self-measuring quantity is none of
  those, and the card carries a differentiation line against each.
- `guard.py nearest`, every driver on file: nearest 0.05 (task97), then task186, task195 and task181 v1 at
  0.04, all far under the 0.12 WARN threshold.
- The domain's own cards: task125 is the nearest build here and ruled the rotation-group family out before
  design (its artifact comes from the point units are recruited and builds through the waves a unit stays
  in; this build has no panel, no waves and no recruitment effect). task238 spends mode effects, task231
  and task264 nonresponse, task240 and task261 design variance and reliability, task230 coding quality.
- `stumping/references/client/layer2-rigor-patterns.md`: the field's shortcut is to treat a survey's
  achieved sample as if the design and the workforce did not touch it; this build differs from the variance
  version of that shortcut by moving a point estimate rather than an interval.

### ARCHIVE architecture 2 (spent): Default path

The pipeline a competent analyst builds from the release's own words and the files' grain, without asking
who collected each region's quarter.

1. Read the quarterly monitoring extract for orientation: achieved sample and the damp-or-mould rate by
   region, on the published provisional basis.
2. Notice the release's window is the field quarter, so rebuild from the dwelling records: stack the two
   questionnaire layouts, resolve the issued-address log to the person and dwelling grain, convert the
   management system's UTC stamps to New Zealand local time across the daylight saving change, and take
   interviews achieved in the quarter.
3. Apply the calibrated weights the person file carries, not the design weights, as the release does.
4. Rebase the regional breakdown across the territorial authority amalgamation so the quarter and its
   comparison quarter are on one base.
5. Compute each region's damp-or-mould rate for the quarter and for the comparison quarter, and take the
   change in percentage points.
6. Rank the regions on that change and read off the largest rise.
7. Check it against the published provisional and revised figures for the comparison quarter, which tie.
8. Commit the region with the largest rise.

Ends on: the loud region, the largest measured rise, with its own observed rate
Golden: the region whose rise survives attribution to its interviewers, with its own observed rate

### ARCHIVE architecture 2 (spent): Stump sentence

A competent solver stacks both questionnaire layouts, resolves the address log to the dwelling grain,
converts the stamps, rebases the regions across the amalgamation and weights to the design correctly,
ranks the regions on the quarter-on-quarter change in dwellings with damp or mould, and commits the loud
region on its largest measured rise, because most of that rise is the differential of the one interviewer
who carried two thirds of that region's quarter while a colleague was on leave, a differential her own
records reproduce in the other regions she worked.

### ARCHIVE architecture 2 (spent): Three rules

- **Task type:** `survey-research-official-statistics` / `anomaly-detection`, which serves Anomaly
  Detection & Diagnostics; the build works the field's own interviewer-variance method on a probed
  prevalence item collected by a workforce the sample management log records.
- **Domain test:** the quantity that decides is the interviewer component of the survey's own measurement
  error, which survey research estimates from the random allocation of issued addresses among the
  interviewers working an area, the interpenetrated assignment behind every published interviewer design
  effect `1 + (m - 1) rho_int`.
- **Swap:** rewritten as "which district's megawatt-hours rose most" there is no workforce collecting the
  measurement, no allocation to randomise and no workload crossing units, so nothing can make a measured
  difference travel with a person rather than a place and the task stops existing.
- **Layer 1:** two questionnaire layouts across the comparison period (a revision); face-to-face and
  telephone collection with different field periods inside the quarter; the sample management log at
  issued-address grain against the person file's person grain; interviewer identifiers recycled when field
  staff leave and are re-engaged; a territorial authority amalgamation changing the published regional
  base mid-series; design weights and calibrated weights both present; management system stamps in UTC
  against New Zealand local time across a daylight saving change; a provisional and a revised figure for
  the same quarter. Nothing is placed to be caught.
- **Layer 2:** `estimand_identification`: a measured difference between units is attributed to the person
  who collected it rather than to the unit, and because most interviewers work one region only, the
  interviewer and the region are collinear, so the attribution comes only through the interviewers whose
  workload crosses regions.
- **Decisive step:** before ranking regions on the change, split each candidate region's change by the
  interviewers who collected it and ask whether each interviewer's own differential reproduces in the
  other regions she worked, which separates a differential that travels with the interviewer from a rise
  that stays with the region.
- **Not semantics:** both routes read every field, code, unit and definition the same way, build the same
  achieved sample on the same window at the same grain, apply the same weights and the same rebasing, and
  reach the same regional rates; they differ only in whether the change is attributed to the interviewers
  who collected it, and no field, code or definition in the pack states that an interviewer carries a
  differential.
- **Not rule application:** the quality framework files the five parts of the estimand and the release
  files the weighting and the rebasing, and no filed sentence, column or procedure says to split a change
  by interviewer, nor that a differential measured in one region should be read against another;
  executing every stated rule in the pack files the loud region.
- **Analyst test:** a strong analyst who stacks both layouts, resolves the address log, converts the
  stamps, rebases the regions and weights to the design ranks the regions on the measured change and
  commits the loud region, because that change is a correct measurement of what its interviewers collected.
- **Estimand:** filed in one sentence in the survey's quality framework: the change, in percentage points,
  in the share of occupied private dwellings with damp or mould observed or reported at interview, between
  the field quarter and the same quarter a year earlier, for the region as the unit, over every dwelling
  interview achieved in the quarter on the amalgamated regional base.
- **No decoy:** nothing is planted to be caught. Every interviewer carries a differential, as every real
  workforce does; no interviewer is written to be found, no memo or draft argues a region, the monitoring
  extract states its own basis and ranks nothing, and the staffing gap is recorded as the roster would
  record it.
- **No certified replay:** no published or certified figure is reproduced only by the golden method; the
  provisional and revised figures tie under both routes, because both reach the same regional rates and
  differ only in attribution.
- **Lesson:** a difference between places is only the places' if it does not travel with the people who
  measured them, and where each place is measured by a handful of people the two are collinear, so only
  the measurers whose work crosses places can tell them apart. No build on file teaches it: task192 turns
  on a validation rate's reach, task195 on a paired interval and task194 on when records arrive.

### ARCHIVE architecture 1 (spent): Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task198.json`, registered 2026-10-17, `guard.py check` WARN, no BLOCK |
| Domain / subdomain | `business-operations-analytics` / `service-operations-sla` (house domain; client domain `general-statistics-data-science`) |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 08, rule replayed on history: the service standard replayed over each FY2026 quarter's cells |
| Decision type | `pick_one_of_n`, answer unit `named_option` plus one rate |
| Gate G | `method_or_model_selection` |
| Strategy | `other`: a specification error in reading a conditional expectation off a filed pool (the matching quantity), named in the card's `notes` |
| Layer 2 family | `allocation_constraints` (capacity and queueing), pattern `own:queue-scale-service-level` |
| Gaps | `objective` (decisive), `time` |
| Generators | G14 conditioned yield (decisive), G12 absence of record versus record of absence |

**Pairing.** Service operations is the one field whose own estimators say what service level a queue
should reach: offered load against staffed positions, and the pooling relation that makes a small queue
worse than a large one at the same utilisation. The decision is the field's own triage question, which of
a set of breach clusters is a process loss rather than an artifact of how the work arrived and who was
rostered, and the quantity that settles it is a service level the field estimates rather than a stated
threshold anyone can check.

**Guard WARNs answered** (`guard.py check`, 2026-10-18: WARN, no BLOCK, nearest driver 0.05 against
task470).

- `repeat.gate_g` and `overuse.gate_g`, `method_or_model_selection` in 7 of the last 12: it is the honest
  mechanism and no other key fits. Two expectations of one filed quantity stand and the data selects
  between them; the alternatives are untrue here (nothing is forecast, no constraint binds, no movement is
  attributed, every candidate does not fail, and the reported number is not correct-and-over-corrected).
  What varies across the batch is the content: this build's two candidates differ in the matching
  quantity, not in a model family.
- `repeat.question_form`, "which" repeating task469: the form is taken from the decision, and the decision
  is a pick of one queue from nine, which asks which. Changing it would misdescribe the call.

**Data-native sentence.** In this pack the waits are generated by the queues themselves: each
queue-quarter's delay comes from its own offered load and its own staffed positions, so the record
contains, inside single queues, quarters that carried the same work per head at two different team sizes
and reached service levels a factor of two apart, which is what makes the load-per-head match the wrong
way to read the queue's own history and the offered-load match the right one.

**Sources read, one line each.**

- `guide-to-prompt/references/domains/README.md`: the client's taxonomy. Teaches that a house-domain draw
  names its client domain and that the task type must serve the objective; this build names
  `general-statistics-data-science` / `exploratory-data-analysis-distribution-assessment`.
- `stumping/references/client/layer2-rigor-patterns.md`, `patient-flow-beds-workforce-optimization` #1:
  "Size beds by blocking probability, queueing or loss model. Shortcut: mean census / 85 per cent."
  Teaches that the field's shortcut is a flat utilisation figure; this build differs by putting the
  utilisation shortcut inside a within-unit comparison rather than inside a sizing calculation.
- `stumping/references/client/layer2-rigor-patterns.md`,
  `exploratory-data-analysis-distribution-assessment` #2: "Stratify before reading a correlation. Shortcut:
  report the pooled trend." Teaches the family; this build's stratum is the queue's own team size, which no
  column names as a stratum.
- `stumping/references/client/two-layer-task-design.md`: the client's standard. Teaches that the estimand
  is filed and the design implies the method; followed by filing the five parts in the service assurance
  framework and leaving only the matching method open.
- `guard.py mechanisms --objective anomaly-detection`, 28 builds: every spent driver on this objective was
  read before drawing. The nearest are task194 v2 (excess over a standard the candidate's own composition
  implies, where the standard is stale), task187 (a Jensen gap inside one unit) and task191 (a selection
  effect in the noise). This build's driver is none of those: the expectation is the unit's own record and
  the error is matching it on a ratio instead of on the quantity itself.
- `analytical_tasks/02_anomaly_detection/AD21`: world only, one scarce investigation to one of N
  candidates committed with a rate. Its mechanism rows were not read.

### ARCHIVE architecture 1 (spent): Default path

The pipeline a competent analyst builds from the framework's words and the files' grain, without stopping
to ask what a queue of a given size can reach.

1. Read `service_monitoring_export.xlsx` for orientation: per-queue breach rates by calendar quarter on
   cases closed in the quarter, elapsed working days from receipt. Transfers in is worst at 46.4 per cent.
2. Notice the framework's window is the financial year, so rebuild from the case record: stack
   `member_cases_gemini_fy2023_fy2024.csv` and `member_cases_orbit_fy2025_fy2026.csv`, drop the Gemini rows
   superseded at the 1 April 2024 migration on `legacy_case_ref`, convert the Orbit UTC stamps to Irish
   local time, and take cases received 1 April 2025 to 31 March 2026.
3. Apply the standard's clock from `member_service_standard_2025.pdf`: working days against the queue's
   target, less the days the case stood with the member, Irish public holidays from
   `public_holidays_ie_2022_2026.csv`; count a case unanswered at the 30 April 2026 extract late once its
   clock has passed its target.
4. Rank the nine queues on that FY2026 breach share. Investment switches is worst at 24.4 per cent,
   Member data corrections next at 25.8 per cent.
5. Build each queue's offered load: cases received times the standard minutes per case from
   `work_measurement_standard_2022.pdf`, over rostered positions times productive minutes, with the 0.88
   net productive factor; take the rostered positions per quarter from
   `rostered_capacity_by_queue.xlsx`.
6. Normalise, because the queues differ in size and the framework compares each queue with its own
   history: divide the offered load by the staffed positions to get each quarter's occupancy, the field's
   workload measure.
7. For each queue take its FY2023 to FY2025 quarters at the same occupancy and read off the breach share
   they reached, then subtract: Member data corrections carried 4.7 positions-equivalents on five positions in
   FY2026, an occupancy of 0.93, and its own quarters at that occupancy reached 9.8 per cent, so it
   stands 16.0 points above its own history, half again the next queue's gap.
8. Commit Member data corrections, FY2026 breach share 25.8 per cent.

Ends on: Member data corrections, FY2026 breach share 25.8 per cent
Golden: Contribution queries, FY2026 breach share 12.4 per cent

### ARCHIVE architecture 1 (spent): Stump sentence

A competent solver rebuilds every queue's FY2026 breach share correctly across both case systems on the
financial year with the clock rules and the unanswered cases applied, compares each queue with its own
FY2023 to FY2025 quarters at the same load per staffed position, and commits Member data corrections at
25.8 per cent, because that queue carried eleven positions through the two years its own history is read
from and five in FY2026, and at the same work per head a five-position queue cannot reach the service
level a fourteen-position queue reaches.

### ARCHIVE architecture 1 (spent): Three rules

- **Task type:** `general-statistics-data-science` / `exploratory-data-analysis-distribution-assessment`,
  which serves Anomaly Detection & Diagnostics; the build works its pattern 2 (stratify before reading a
  relationship) on a service-operations quantity, and the field's own estimator for that quantity is the
  queueing service level of `patient-flow-beds-workforce-optimization` #1.
- **Domain test:** the quantity that decides is the share of cases answered outside target that a queue's
  own offered load and staffed positions produce, which service operations estimates from a delay model on
  offered load and staffed servers and which falls steeply as positions grow at unchanged utilisation (the
  pooling relation behind every contact-centre and back-office staffing model).
- **Swap:** rewritten as "which district's megawatt-hours stand furthest above what its own load history
  implies" there is no pooled stream of work served by a counted number of parallel servers, so nothing
  makes a smaller unit worse at the same utilisation and the whole comparison collapses into a rate
  against a rate; the task stops existing.
- **Layer 1:** two case systems either side of the 1 April 2024 platform migration, with Gemini rows
  superseded at cutover carried in both (the migration project's own reconciliation extract); Orbit stamps
  in UTC against Gemini in Irish local time (two vendors' conventions); the administrator's financial year
  against the monitoring export's calendar quarters (a dashboard built for the client-reporting pack);
  working-day clocks needing Irish public holidays, St Brigid's Day present only from 2023 (the statute);
  rostered capacity in a workbook whose sheets change from monthly hours to quarterly FTE at the FY2025
  planning change; the trustee statement reporting active membership split by contribution status while
  the participating scheme register carries one figure as returned, and none at all for the master trust,
  whose trustees return their own; standard minutes in a PDF table (the 2022 work-measurement study); the monitoring export
  missing 2024 Q2 (the migration quarter) and marking 2026 Q1 provisional. Nothing is placed to be caught.
- **Layer 2:** `allocation_constraints`, capacity and queueing: the expectation a queue is judged against
  has to be read off the quarters that carried the same work, not the same work per head, because the
  queue's own record spans two team sizes and the service level at a given utilisation is not scale free.
- **Decisive step:** match each queue's FY2026 quarters to its own earlier quarters on the offered load
  itself rather than on the offered load divided by staffed positions, so Member data corrections is read
  against the quarters when it ran five positions on the same work rather than against the quarters when
  eleven positions carried twice the work at the same occupancy.
- **Not semantics:** both routes read every field, code, unit and definition the same way, build the same
  case population, the same clock, the same offered load in the same positions-equivalents and the same
  rostered positions; they differ only in which of the queue's own quarters the expectation is read from,
  and no field, code or definition in the pack states that the service level at a given occupancy depends
  on the number of positions.
- **Not rule application:** the framework files the five parts of the estimand and the fee schedule files
  the charges, and no filed sentence, column or procedure says how to read "the quarters that carried the
  same offered load" off twelve quarters, nor that a ratio match is a different match; executing every
  stated rule in the pack and taking the field's own workload measure files Member data corrections.
- **Analyst test:** a strong analyst who has stacked both case systems, de-duplicated the migration,
  converted the stamps, applied the clock and the exclusions and counted the unanswered cases divides each
  quarter's offered load by its staffed positions, reads each queue's own history at that occupancy, and
  commits Member data corrections at 25.8 per cent, because occupancy is the field's workload measure and
  the record offers it a clean within-queue comparison on it.
- **Estimand:** `service_assurance_framework_2026.pdf` section 4.2 files it in one sentence: the review
  candidate is the queue whose share of cases received in the financial year answered later than its
  standard target stands furthest above, in percentage points, the share the same queue reached in those
  of its FY2023 to FY2025 quarters that carried the same offered load, counting every case received in the
  year including cases unanswered at the extract, at the queue as the unit.
- **No decoy:** nothing is planted to be caught. There is no copied block, no withheld rule, no memo or
  draft arguing a queue, and no stakeholder figure that exists to be overturned; the Pensions Authority
  letter names no queue and no metric, the monitoring export states its own basis and ranks nothing, and
  the roster workbook records the temporary posts as the resourcing papers would.
- **No certified replay:** no published or certified figure in the pack is reproduced only by the golden
  method; the monitoring export reproduces on its own stated basis under the wrong method too, and the
  billing extract ties to the fee schedule under both ask readings.
- **Lesson:** a within-unit comparison is only like for like on the quantity it is matched on, and
  matching a queue on work per head rather than on work silently compares it with a differently sized
  version of itself. No build on file teaches it: the nearest, task194 v2, turned on a stale external
  standard and task187 on a Jensen gap inside one unit.

### ARCHIVE architecture 1 (spent): Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 export basis | the export states its own basis | the export's own columns | yes, read the dashboard | none | no | yes, read off | readable |
| 1 rebuilt metric | the standard files the clock | the case columns | yes, the obvious group-by | none | the battery finds the migration duplicates | one group-by | readable |
| 2 occupancy match (default path) | the framework names offered load, not the ratio | occupancy is not a column, it is built from three files | yes, the field's workload measure | none | no | one ratio | readable |
| 3 offered-load match (decisive) | no sentence says the service level at a given occupancy depends on the position count | no column marks team size as a stratum; positions sit in a workbook whose sheets change basis | no: every reflex (pool, index on workload, add positions as a control, trend, own-history average) lands on another queue, measured | no control or published figure ties only under it | the battery passes under both matches | not a subtraction, ratio or half of a reported figure | silent |

### ARCHIVE architecture 1 (spent): Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "financial year" | 1 April to 31 March | calendar year | Contribution queries | `service_assurance_framework_2026.pdf` 2.1 states the financial year as 1 April to 31 March; `same call` either way, asserted |
| SF2 | "cases received in the year" | by receipt date, including cases unanswered at the extract | cases closed in the year | Investment switches at rung 1, Member data corrections at rung 2 | framework 4.2 "every case received in the year, including cases not yet answered at the extract date" |
| SF3 | "answered later than target" | the standard's clock in working days, less days with the member | elapsed calendar days | Transfers in | `member_service_standard_2025.pdf` 3.1 and 3.4 state working days and the exclusion |
| SF4 | a case unanswered at the extract | late once its clock has passed target, within target otherwise | excluded from the year | `same call`: Contribution queries either way, asserted on the figure | standard 3.6 states the treatment; the convergence is asserted |
| SF5 | "offered load" | cases received times standard minutes over productive minutes per position, in positions-equivalents | cases received; standard minutes total | `same call`, and the same matched quarters for every queue, asserted | C1: within a queue the standard minutes per case are constant, so all three select the same pool quarters |
| SF6 | "the quarters that carried the same offered load" | the queue's own FY2023 to FY2025 quarters nearest on offered load | the queue's own quarters nearest on load per staffed position | Member data corrections | the decisive step; closed by the data, not by a sentence: see `## Literal reader` |
| SF7 | "staffed positions" | rostered positions for the quarter from the capacity workbook | positions at the year end | `same call`, asserted | framework 4.3 "the positions rostered for the quarter" |
| SF8 | "breach share" | late cases over cases received, pooled over the year's four quarters | the mean of the four quarterly shares | `same call`, asserted on the figure to one decimal | framework 4.2 states the share over the year's cases |
| SF9 | rounding path | once at the end, to one decimal place in percentage points | per quarter then averaged | `same call`, asserted | prompt's last sentence; SF8 fixes the path |
| SF10 | "the ten largest participating schemes by FY2026 cases received" | participating schemes as the register lists them, the master trust's five sub-codes rolled up to one scheme | the case record's scheme codes as they stand, so the trust counts as five schemes | a different ten and different rates | `schemes_register_2026.csv` header note states one row per participating scheme and names the trust's five administrative sub-codes; the tenth and eleventh sit 117 cases apart, asserted |
| SF10b | "the runner-up" | not asked and not graded | the queue second on the decisive read | varies with the number of matched quarters: Death benefits, Transfers in or Member data corrections | removed from the prompt and from framework clause 4.4 once measured; `checks.py` and `verify.py` assert that second place varies while the call leads every reading by 1.2x or more |
| SF11 | "the chargeable cases our scheme charging covers" | the cases the charges cover, recovered as each line's charge over the schedule's per-case fee | the charge lines counted as cases | the ask's four figures, 4,584 against 7,582 | a line is a charge, not a case: `fee_schedule_2025.pdf` states the per-case fee for each chargeable case type and the two rate periods, and every consolidated line's charge is an exact multiple of it |
| SF12 | "its active members at 31 March 2026" | the per-scheme figure in the trustee membership statement | the register's `active_members` as returned by the sponsor, which is the group total where the sponsor returns for several schemes | the ask's eighteen grouped figures, register rates 41.9 to 151.0 against golden 158.0 to 182.1 | the asking sentence's own words: the register's note states the column is active members as returned by the sponsor, not a per-scheme figure at 31 March 2026, and the trustee statement is headed active members at 31 March 2026 by scheme |

### ARCHIVE architecture 1 (spent): Ladder

Four rungs, four distinct winners. Each reproduces from the raw files, names its own candidate and dies
to one shipped fact or construction.

| Rung | Analysis | Winner | Figure | Dies to |
|---|---|---|---|---|
| 0 | the monitoring export's own per-queue figures | Transfers in | 46.4 per cent | the export states it measures cases closed in the calendar quarter on elapsed working days; the framework's window is the financial year and the standard's clock excludes days the case stood with the member |
| 1 | rebuild the share on the filed window, population and clock | Investment switches | 29.8 per cent | the framework compares each queue with its own history, so a level ranking is not the quantity clause 4.2 names |
| 2 | each queue against its own history at the same load per staffed position (**the default path**) | Member data corrections | +16.0 points | the queue's own record carries five positions in FY2023 and FY2026 and fourteen in FY2024 and FY2025 at the same occupancy, with breach shares of 22.9 and 2.1 per cent |
| 3 | each queue against its own history at the same offered load (**decisive**) | Contribution queries | +10.2 points, 12.4 against 2.2 per cent | nothing: the golden |

**Arithmetic, measured on the cut pack.** Golden position on rung 1: Contribution queries is 4th of 9 on
the level ranking (29.8, 25.8, 13.4, 12.4) and 4th on the export basis. Decisive margin: +10.23 points
against the next queue, a factor of 3.71 at three matched quarters and 4.53, 3.75, 3.71, 2.82 and 1.46 at
one through five, so the call leads every reading by more than 1.2x. Rung-2 margin for the default path:
+16.00 against +10.23, a factor of 1.56, so stopping at rung 2 is satisfying. Dominance: the winner's
edge on the decisive axis is 7.47 points against the decoy's 5.77-point advantage on the carried axis,
which clears the 1.2x bar. Graded figure: 12.4074 per cent prints 12.4 at one decimal, edge distance
0.0426 of a point against the 0.03 floor.

**Second place is not graded, and that is a finding the build acted on.** The queue in second on the
decisive read changes with the number of matched quarters (Death benefits at one and three, Transfers in
at four, Member data corrections at five), because every queue other than the call sits between -1.0 and
+2.8 points, which is the noise floor of a nearest-quarters match on cells of 100 to 400 cases. An open
method pins the queue that leads by 3.7x; it does not pin the ordering inside the floor. The prompt and
clause 4.4 therefore ask for the call and its own observed figures, and nothing asks for a runner-up.
`checks.py` and `verify.py` both assert that second place varies and that the call does not.

**Grid.** Every cell of the four-way grid (window basis, clock basis, matching quantity, population) is a
named wrong answer: export basis Transfers in; fiscal window with elapsed clock Transfers in; fiscal
window, netted clock, level ranking Investment switches; occupancy match Member data corrections; load
match Contribution queries. No cell is saturated and no partial application reaches the golden.

**Reflex sweep, measured on the cut pack.** Pooled cross-queue fit on occupancy: Investment switches.
Cross-queue fit on occupancy plus staffed positions as an additive control: Investment switches.
Cross-queue fit on cases per staffed position: Investment switches. Own-history average with no load
conditioning: Member data corrections. Occupancy match: Member data corrections, +16.00. Every reflex
lands wrong.

**Decisive-route robustness.** Seven estimators of "the share its own quarters at the same offered load
reached" all name Contribution queries: nearest one, two, three, four and five quarters by load, a fitted
logit of the queue's own breach share on log load, and the ratio rather than the difference basis. The
three licensed readings of offered load (positions-equivalents, standard minutes, cases received) also
all name it, at margins of 3.71x, 1.43x and 1.43x.

### ARCHIVE architecture 1 (spent): Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | cases received 1 April 2025 to 31 March 2026, including cases unanswered at the 30 April 2026 extract | framework 4.2 files it with the unobserved members stated; SF2, SF4 |
| 2 | Unit of account | the case queue; one row is one case | framework 4.2 names the queue as the unit; the case record has one row per case |
| 3 | Attribution window | the quarter a case was received in | framework 2.1; C1, receipt stamps clear of the fiscal boundary except the 11 cases SF-asserted in both readings |
| 4 | As-of dating | the 30 April 2026 extract; rostered positions as rostered for the quarter | framework 4.3; the extract date is in the prompt and the file names |
| 5 | Version basis | the case as the later system holds it; Gemini rows superseded at the migration drop | the migration reconciliation extract states the supersession; C1 asserted on the de-duplicated count |
| 6 | Denominator | cases received in the window, per queue | framework 4.2 in its own words |
| 7 | Weighting | pooled over the year's cases, not the mean of quarterly shares | SF8; `same call` asserted |
| 8 | Window length | the comparison pool is FY2023 to FY2025, twelve quarters | framework 4.2 names the three years |
| 9 | Boundary inclusivity | receipt on 1 April 2025 and 31 March 2026 inclusive | framework 2.1; C1, no case on the excluded edge |
| 10 | Rounding path | once at the end, one decimal place | prompt's last sentence; asserted |
| 11 | Tie-break | none needed: the decisive gap is 4.30 points | measured; the second level (the observed share) is filed in 4.2 if ever needed |
| 12 | Maturity and censoring | cases unanswered at the extract are in the population and late once their clock passes target | standard 3.6; SF4 convergence asserted |
| 13 | Order of operations | de-duplicate the migration, then convert stamps, then apply the clock | C1: the three steps commute on this record, asserted |
| 14 | Row order | file order cannot move a share | C1 by construction, asserted over three permutations |
| 15 | Duplicate resolution | one case, identified by its original reference across the two systems | the migration extract's `legacy_case_ref`; C1 asserted |
| 16 | Identity normalisation | queue codes differ between systems; one queue was renamed in FY2025 | `queue_reference.csv` carries both codes and both names; C4, the raw join misses 4 of 9 queues |
| 17 | Netting against gross | no netting: a late case is late | framework 4.2 has no offset |
| 18 | Dimensional units | standard minutes against productive minutes per position; rostered hours against FTE across the workbook's sheets | the work-measurement study states minutes and the 0.88 factor; the workbook states hours per month and FTE per quarter; C4, the unconverted read moves occupancy by a factor of 7.3 |
| 19 | Code and status semantics | status codes differ between systems; the standard names the statuses that stop the clock | `case_status_codebook.csv`; never the stump |
| 20 | Integerisation | case counts are whole; no package arithmetic | by construction |
| 21 | Clause scope | the framework's 4.2 governs the review candidate only; the standard's 3.x governs the clock | each clause names its scope |
| 22 | Forward window contents | the committed window (H1 2027) holds no cases: the call is which queue takes the review, and the quantity is FY2026's | the framework files the quantity on the closed year, and the Authority letter sets the H1 2027 slot |

### ARCHIVE architecture 1 (spent): Literal reader

Executed word for word, the framework's 4.2 says to take each queue's FY2026 breach share and the share
the same queue reached in those of its FY2023 to FY2025 quarters that carried the same offered load, and
to rank on the difference in percentage points; every licensed reading of "offered load" (positions-
equivalents, standard minutes, or cases received) selects the same pool quarters within a queue because
the standard minutes per case are constant inside a queue, so the literal reading lands Contribution
queries at 12.4 per cent under all three (SF5, asserted). The one quantity the sentence does not name is
how to read a value "at the same offered load" off twelve quarters, and the data closes it rather than a
sentence: a match on load per staffed position does not reproduce the record it is read from, because
Member data corrections' own quarters at 0.93 occupancy carry five positions in four of them and fourteen
in eight, with breach shares of 22.9 and 2.1 per cent, so the load-per-head match reads a five-position
quarter against fourteen-position quarters and reports a gap the queue's own five-position history denies.
Seven estimators of the load match agree on the name and the graded figure is the observed share, which
is determinate under all of them.

### ARCHIVE architecture 1 (spent): Oracles

- `service_monitoring_export.xlsx` reproduces on its own stated basis (cases closed in the calendar
  quarter, elapsed working days) under every method, golden and wrong alike, and presents queues in queue-
  code order with no ranking, no excess and no expectation. It confirms nothing about the call.
- `fee_schedule_2025.pdf` and `scheme_billing_extract_fy2026.csv` tie to each other under both ask
  readings of a billing line (per row and per case covered), so neither ties only under the golden; the
  disagreement they carry is the ask's, arbitrated by the fee schedule alone.
- `schemes_register_2026.csv` ties to `trustee_report_membership_2026.pdf` only on the participating-scheme
  roll-up, which is the Ask 3 referee and hands over no level in the call.
- No control, published figure or reconciliation column in the pack ties only under the decisive match.
  The roster workbook records the temporary posts as a resourcing fact, not as an explanation.

### ARCHIVE architecture 1 (spent): Ask sheet

Three asks, 25 graded ask figures, solved on the cut pack by `generator/asks_measure.py`. Ask 1 is the
one free construction figure both responses bank; Ask 2 is a mirror device the cracker recovers; Ask 3
carries the cracker's misses.

| Ask | Figures | H18 home | Use | Primary device | Hazards | File and columns | Stops and lazy delta |
|---|---|---|---|---|---|---|---|
| 1 | 1: the cases received in FY2026 that were answered later than target, across the operation | the call's own working at the operation level | the Authority response opens on the operation's own year | none by design: the call's population carries no device row | the cutover de-duplication, the UTC conversion, the holiday calendar, the clock exclusions | both case files, 11 columns | elapsed-clock read 3,312; export basis 1,186; golden 1,799 |
| 2 | 4: the chargeable cases the scheme charging covers in each FY2026 quarter | an input reconciled to another system's total, the gap made of devices | member operations charges schemes per chargeable case and owes the Authority a charge reconciliation | D6 grain, a paper row covering several ledger lines: the three largest participating schemes are charged on a consolidated monthly statement, so one line covers every chargeable case of one type whose response issued for that scheme in the month, and the line carries no count; the cases are recovered as the line's charge over the schedule's per case rate | the schedule's two rate periods, to 30 September 2025 and from 1 October 2025; responses late in a month charged in the month following | `scheme_charges_fy2026.csv`, 8 columns; `fee_schedule_2025.pdf` | lines counted as cases 4,364; cases the charges cover 7,291; per quarter 944 against 1,593, 1,168 against 1,967, 1,169 against 1,920, 1,083 against 1,811 |
| 3 | 20: the ten largest participating schemes by FY2026 cases received, each with its active members at 31 March 2026 and its FY2026 cases received per 1,000 active members | a measure every candidate carries that the call does not turn on | the trustee reporting pack reports case load per 1,000 members by scheme | D9 self-validation, a rollup above its own parts: where one sponsoring employer returns membership for more than one of its schemes, the participating scheme register carries the group's total against each of that sponsor's schemes, and nine of the ten largest sit in such a group; the master trust's trustees return their own membership, so the register carries no figure for it at all. The per-scheme figure is in the trustee statement, split by contribution status, and the register's rows contradict it with no total anywhere in the pack to reconcile them against | the master trust's five administrative sub-codes rolling up to one participating scheme; one queue renamed mid-history | `schemes_register_2026.csv`, 4 columns; `trustee_report_membership_2026.pdf` | register rates 113.6, 130.6, 111.6, 126.3, 142.6, 143.4, 42.5, 137.6, 50.8 against golden 182.4, 185.6, 183.1, 167.6, 175.3, 169.1, 173.6, 159.5, 171.4 |

**Separation line.** Zero device rows and zero hazard rows sit in the main call's declared population.
The call reads the two case files, the roster workbook, the work-measurement study, the service standard,
the assurance framework, the queue reference, the status reference and the holiday calendar; Ask 2's
devices are in `scheme_charges_fy2026.csv` and `fee_schedule_2025.pdf`, Ask 3's in
`schemes_register_2026.csv` and `trustee_report_membership_2026.pdf`, and the call reads none of those
four. The scheme code the case record carries is read by no ask device and by the call not at all.
Deleting every device leaves the call unchanged, asserted by count in `generator/checks.py`.

**Measured forcing, per device, on the cut pack.** Ask 2: the natural read returns 4,364 against the
golden's 7,291 cases covered, and the smallest quarterly gap is 649 cases on a figure stated in whole
cases. Ask 3: the smallest gap between the register rate and the golden rate on a grouped scheme is 21.9
per 1,000 against a 0.05 bin half-width, and the largest is 131.1; for the master trust the register
carries no figure at all. Graded-set boundary: the tenth largest participating scheme has 513 FY2026
cases against the eleventh's 411, a gap of 102 cases, so the membership of the graded set holds under
every licensed reading. No graded membership figure ships verbatim: each is the trustee statement's two
status parts added, asserted in `verify.py`.

**Referee.** `fee_schedule_2025.pdf` arbitrates Ask 2's disagreement and states no case count;
`trustee_report_membership_2026.pdf` arbitrates Ask 3's and states no scheme-level rate and no total.

The cracker is the response that landed the call, ran the hygiene battery, executed every filed rule the
pack points at and matched every control and published figure it carries. Ask 3 is the primary it is
measured against; one row per move it makes, and the verdict is whether that move reaches the device.

| Cracker move | What it does on Ask 3's register | Verdict |
|---|---|---|
| key uniqueness | every participating-scheme code is unique in the register | miss |
| exact duplicates | no two register rows are equal; the repeated membership figures sit on rows differing in code, name and sponsor | miss |
| unmatched joins | the master trust's five sub-codes resolve through the dictionary's own note, and the register's blank membership for the trust is a visible gap that sends the reader to the trustee statement for that one scheme only | miss |
| fan-out and count ties | the register is one row per participating scheme, so nothing fans out and no count ties | miss |
| executes every filed rule the pack points at | the register's dictionary entry states the column is active members as returned by the sponsor; nothing in the pack says a sponsor return may cover more than one of its schemes | miss |
| matches every control and published figure | the pack ships no membership total, in the register or the trustee statement, so there is no control for the register to fail against | miss |

**What the landing response banks, named figure by figure.** The table above is the cracker sheet proper.
`asks_measure.py` has the cracker keeping **7 of the 25 graded ask figures**, and these are the seven.

| Figure banked by the response that lands the call | Golden | Why it is not a device's to take |
|---|---|---|
| FY2026 cases answered later than target, across the operation | 1,799 | Ask 1 is the construction layer. It is computed over exactly the rows the call's own comparison is computed over, where the separation line forbids any device row, so it is free by design (`supplemental-stumping` 2.2: the cracker has it, so it never stands alone). |
| FY2026 Q1 chargeable cases covered | 1,593 | Ask 2 is a mirror device. The schedule's per case rate is a filed rule and every consolidated line's charge is an exact multiple of it, so a response that executes the schedule recovers the count. Making the count unrecoverable instead would break law 6. |
| FY2026 Q2 chargeable cases covered | 1,967 | as above |
| FY2026 Q3 chargeable cases covered | 1,920 | as above |
| FY2026 Q4 chargeable cases covered | 1,811 | as above |
| RMT-000 active members | 41,789 | the register carries no figure for the master trust, so its blank sends any reader to the trustee statement for this one scheme, where the two status parts add to the answer |
| RMT-000 cases per 1,000 active members | 125.4 | as above |

The mirror keeps three of those seven: Ask 1's figure and the master trust's two. It loses Ask 2's four
because it counts charge lines as cases, and the other eighteen Ask 3 figures because it takes the
register's membership.

**Pair ceiling:** 39.5, solved on the cut pack on Part 0's weights (38 recommendation and critical
components, 7 instruction-following, 55 asks) with both responses rescored from their own readings and
both columns printed: the cracker lands the call and keeps 7 of 25 ask figures, scoring
38 + 7 + 55 x 0.2800 = 60.4; the mirror stops at rung 2, counts charge lines as cases and takes the
register's membership, keeps 3 of 25 and scores 5 + 7 + 55 x 0.1200 = 18.6. The two ask columns differ
because the mirror does not run the battery and does not execute the schedule, not because any ask
consumes the call's construction; the separation assertions above are the evidence that it does not.

**Mirror leakage:** 12.0 per cent of ask weight.

**Measured by:** `generator/asks_measure.py`, which at this stage solves on the generator's clean truth in
pipeline, so the ceiling is measured on what ships rather than on the generator's truth. It exits 1
unless the pair is at or under 40 and the leakage under 35, and it also prints the graded-set boundary
and the precision each graded figure is printed at. Re-run after every change to the asks or the pack.

**Rounding sentence, and the figures it governs.** The prompt's last sentence governs the breach share
and the rates per 1,000, both to one decimal place: the committed call's 12.4 per cent and Ask 3's ten
rates. Ask 1's count, Ask 2's four quarterly counts, Ask 3's ten membership figures and the call's 6,480
cases received are whole counts that no rounding sentence governs. `verify.py` checks each figure's
printed precision against this list, because `figures_check.py` compares values and cannot see
precision.

## Build rules carried forward

Three rules filed during this build, each binding on stage 3, plus the one the ask layer already met.

- **Printed precision is a graded property.** `figures_check.py` compares values and cannot see
  precision, so `verify.py` carries the list in the Ask sheet's rounding paragraph and checks each
  figure's printed precision in the shipped write-up against the prompt's last sentence: the call's
  9.2 per cent, Ask 1's 7.7 per cent and Ask 3's ten rates to one decimal place, Ask 2's four counts and
  Ask 3's ten membership figures as whole numbers.
- **One verifier assertion per shipped format, from the shipped bytes.** `verify.py` reads the bundle only
  and owes an assertion per format it ships (csv, xlsx, pdf), each read back from the shipped bytes with a
  positive control on the same code path: a sentence or value the assertion must not find, so a silent
  no-op fails loudly. A format only `checks.py` can read is asserted by the hand that wrote it and does
  not count.
- **No rejected route named in the write-up without recomputing it.** `submission.md` states the call, its
  components and a reproducible path, and names no candidate a rejected route would yield unless that
  route is recomputed and the candidates it yields named exactly. The ladder's rung winners stay in this
  note, not in the write-up.
- **The pair ceiling is solved, not asserted.** Met: `generator/asks_measure.py` scores both responses
  from their own readings on Part 0's weights and prints both columns, and it is re-run after every change
  to the asks or the pack.

## Tried and rejected

- Cross-queue expectation as the decisive step (the queue's breach share against what queues of its size
  and load reach across the operation). Died at the draw: which pool supplies the expectation is the
  comparison, which `determinism-check` section 1 requires filed, and filing it turns the step into
  executing it. This is the shape that killed task194's architecture 2 and it was abandoned before any
  data was cut.
- The decisive step as an omitted scale argument in a cross-queue fit (condition the expectation on the
  position count as well as on occupancy). Died on the reflex sweep: "hold the pool to every visible
  attribute" is an opponent default, the position count is a column, and an additive control on it reached
  the golden in the measured grid, so the decisive rung was readable.
- Right-censoring at the extract as the decisive step (the breach share of cases received in the window,
  with cases still open treated as a survival quantity). Died twice over: the population, including
  members not yet observed, is one of the five parts the estimand must file, and `maturity_censoring` is
  banned against the last three builds. The censoring stayed as Layer 1 and as rung 2's population step.
- A pure M/M/s discrete-event simulation as the generating process. Died on tuning: a FIFO queue's delay
  is a cliff in utilisation, so the nine queues either breached under 1 per cent or ran unstable at 100
  per cent, with no stable band in between. Replaced by the standard heavy-traffic delay formula at each
  queue-quarter's own load and staffing, which is the same relation the decisive step recovers.
- Unbracketed FY2026 occupancies (the load-driven queues stepping outside anything their own history
  covered). Died on measurement: every route, the decisive one included, then reported a large excess for
  the load-driven queues, because the expectation was extrapolating rather than interpolating. Replaced by
  seasonal peaks, so each queue's FY2026 quarters sit inside its own historical range.
- Shape 08's full replay grid (four quarters by four outcome cells, sixteen graded figures) as the criteria
  source. Died on the pair arithmetic: those figures sit in the call's own population, so no device may
  touch them and both top responses bank all sixteen, which puts the pair over 50 whatever the device mass
  elsewhere. Cut to four quarterly figures, with the criteria count carried by the two device asks.
- The telephony export as a fourth ask. Dropped for span rather than legality: it shares no primary family
  with Asks 2 and 3 but adds a third file set to build for eight more figures, and the pair arithmetic is
  already met. It stays in the pack as a distractor.
- A 22-figure ask layer with a four-quarter free construction ask and a sixteen-figure scheme ask. Died on
  the solved ceiling: the construction figures sit in the call's own population, so both responses bank
  them, and at four free figures of 22 the pair came out at 41.6. Folded to one operation-level figure and
  the scheme ask widened to the ten largest, which solved to 39.5.
- The scheme weights as first drawn. Died on the measurement rather than on paper: the graded set's tenth
  and eleventh members sat 3 cases apart, so the membership of Ask 3's graded set would have flipped under
  any licensed reading. The tail weights were widened to a 117-case gap and the ceiling re-solved.
- A telephony export as a fourth ask. Dropped for span rather than legality: it adds a third file set for
  eight more figures and the pair arithmetic is already met. It stays in the pack as a distractor.
- Grading the runner-up and the gap, which the prompt and framework clause 4.4 asked for at first. Died on
  measurement: the queue second on the decisive read changes with the number of matched quarters, because
  every queue but the call sits inside a noise floor of about three points. An open method pins the leader
  by 3.7x and does not pin the ordering below it, so a graded runner-up was a Gate C finding waiting to
  happen. Both the prompt and clause 4.4 now ask for the call and its own observed figures, and the
  instability is asserted rather than hidden.
- A second process drift, first on Transfers out and then on Member data corrections, to make the runner-up
  a designed figure instead of noise. Died on the arithmetic: every share that lifted second place far
  enough to be stable also shrank the call's own margin or moved it off fourth on the level ranking, and
  one setting put the committed figure 0.002 of a point from its bin edge. Not grading second place costs
  nothing and fixes it.
- Grading the ten schemes' active members as the register states them. Died on `leak.py` sweep 3: ten
  golden figures appeared verbatim in the trustee statement, which is their source. The statement now
  reports active membership split by contribution status, as a scheme return does, so every graded
  membership figure is the two parts added and none ships verbatim; the register carries no figure at all
  for the master trust, whose trustees return their own.
- Grading each scheme's FY2026 cases received instead of its membership, tried as the fix for that leak.
  Died on the solved ceiling: the sub-code roll-up moves only the master trust's count, so nine of the ten
  figures were free and the pair came out at 54.9.
- Nine per-queue breach shares as graded chart figures. Died on the same arithmetic: free determinate
  figures are the most expensive thing in an ask layer, and nine of them put the pair over 50. The chart is
  graded as a content requirement, which is what `submission-writeup` provides for, and the per-queue
  shares ride in the workbook as context the write-up does not grade.
- A pure utilisation story for the roster swing, with Member data corrections at eleven temporary positions
  and 2.2 times the caseload. Died on the dominance test: the winner's edge on the decisive axis has to
  clear 1.2 times the decoy's advantage on the carried axis, and at eleven positions it did not. Fourteen
  positions and 2.8 times the caseload clears it at 7.47 points against 5.77.

### Architecture 1, spent at stage 4 (2026-10-18)

- The load-matched within-queue baseline as the decisive step (each queue's FY2026 share against the
  share it reached in those of its FY2023 to FY2025 quarters that carried the same offered load). Died at
  stage 4: determinism judge NOT_DETERMINISTIC / SEND_BACK, Gates C and E failing on a flip and Gate H
  reading the decisive step as rule application, with the isolated reader reaching the same finding
  independently. Clause 4.2 filed the comparison, which was correct and mandatory because the comparison
  is one of the five parts of the WHAT, and the only residue left open was how closely "the same" must
  match. Three queues win across licensed readings: Contribution queries under the nearest one to four
  quarters pooled or a load band of 0.05 to 0.2, Investment switches (the plain highest-share answer)
  under a band of 0.22 to 0.3 or load rounded to whole positions-equivalents, Member data corrections
  under five or more nearest quarters pooled or no matching. Pinning the tolerance closes C and E and
  finishes F, because with the comparison filed and the tolerance filed nothing analytical is left. The
  rule it earned is in `determinism-check` section 1.

### Architecture 2 candidate mechanisms screened at the draw, each with the rule that killed it

Measured or screened before any design time was spent, so no later pass repeats them.

- A cross-queue expectation (a queue's share against what queues of its size and load reach across the
  operation). Dead on the WHAT screen: which pool supplies the expectation is the comparison. This is also
  the shape that killed task194's architecture 2.
- Right-censoring the cases unanswered at the extract. Dead twice: the population, including members not
  yet observed, is one of the five parts, and `maturity_censoring` is banned against the last three builds
  while task194 holds it.
- Arrival-process variability as the omitted argument (the G/G/s delay is linear in the squared
  coefficient of variation of arrivals, which the generator already carries at 1.8 to 4.0 across queues,
  so an expectation built on mean load alone misreads every bursty queue). Dead on lineage, not on the
  residue test: architecture 1's driver is already "an expectation built on the ratio alone omits an
  argument of the delay function", and changing the omitted argument from the server count to the arrival
  variability is the same driver in other nouns, which the abstraction test reads as one insight. Measured
  as unsupported by the pack as cut in any case: arrivals are assigned to uniform random working days, so
  the shipped timestamps are Poisson (variance over mean 0.59 to 1.95 across queues) and the burstiness
  would have to be built.
- A within-scheme (crossed scheme by queue) comparison, re-finding the seed's "the worst rate belongs to
  one bad batch" without a withheld rule. Dead on lineage: architecture 1 already stratifies an expectation
  on a dimension no column marks as a stratum (team size), and stratifying on the scheme instead is the
  same driver with a different stratum.
- Cluster-robust inference on the excess (scheme-event clustering as the unit of variation). Dead on rule
  1: the swap test fails, because clustered inference reads identically with another field's nouns in and
  nothing about pensions administration or service operations makes it the deciding quantity.
- A ratio of totals against a mean of quarterly shares as the decisive step, which `stumping` 1.2 blesses
  as surviving the WHAT screen. Dead on the closure table: weighting is axis 7, which `precut.py` requires
  closed, so it cannot also be the open decisive step.
- Re-basing the 2022 work-measurement study's standard minutes to a current vintage. Dead on lineage
  against task194's architecture 2 (an external standard fixed at a stale vintage, re-based), which is
  named in this card's own `differentiation`.
- A filed back-test selecting the baseline, which is the determinism judge's own suggested lever. Dead on
  the readability screen, test 4 and test 3 together: a corpus that scores the candidate methods is a
  control bench, and back-testing is an opponent reflex (`stumping` Part 0), which is how task181's
  architecture 3 died at design on this same objective.
- The queue-time against touch-time decomposition (a process re-engineering review moves the work content,
  not the time a case waits for a caseworker, so the filed outcome's unmovable component has to be
  separated). Measured on the generator's clean truth and it does re-rank: the easy route on the FY2026
  breach share files Investment switches at 29.8 per cent, while the work component over target files
  Contribution queries, where the process drift actually sits, at a margin of 1.41 times the next queue.
  Dead on the residue test as it stands: the only knob-free identification of the split runs through the
  delay formula at the queue's own load and positions, which is architecture 1's driver, and every
  model-free identification (the queue's own lowest-load quarters, a fitted intercept at zero congestion)
  is a cut-off or a functional form, which is exactly the knob the re-root constraint bans. Little's Law
  does not rescue it: it returns the whole time in system, and splitting out the waiting part needs the
  number in service, which no shipped field records.
- The distribution's shape as the discriminator (congestion scales a queue's whole answer-time
  distribution, while a process fault shifts a subset of it, so the bend in the quantile ratio should
  isolate the fault without any model of load). Measured on the generator's clean truth and it does not
  separate: the FY2026 over FY2023-25 quantile ratio bends most for Member data corrections at 1.237,
  against Contribution queries at 1.158, because the roster swing from five to fourteen positions moves
  congestion's own contribution to the shape. Viable only if the main call's generating process is retuned.

### Architecture 2 route 3, the input-property family, screened 2026-10-18

Route 3 keeps the call shape and files the comparison with zero reading residue (each queue's own FY2023
to FY2025 quarters, all twelve, pooled: no matching, no nearest-k, no band, no tolerance) and puts the
decisive step on a property of the records feeding it. Under that filing the default path lands **Member
data corrections at +20.36 points** (FY2026 25.69 against its own 5.33), with Investment switches second
at +11.57, so a candidate must move the call by **8.79 points** to decide anything. Each candidate below
carries the two exact computations a competent analyst would choose between, and the rule that killed it.

- **The platform cutover, 506 overlapping cases, two extracts covering different years.** (a) Build
  FY2023 and FY2024 from the Gemini extract as the system of record for those years, where the 506 TRF
  rows carry no outcome; (b) stack both extracts and resolve the 506 on `legacy_case_ref`, taking the
  outcome from Orbit. Both exact, no parameter in either. **Dies twice, both measured.** Magnitude: the
  cutover population is about one per cent of every queue's history, so if every cutover case flipped its
  outcome the largest possible move in any queue's historical share is 2.644 points (Death benefits),
  0.685 for Member data corrections and 0.760 for Investment switches, against the 8.79 needed. Two
  orders of magnitude short, so it cannot decide the call however it is computed. Semantics: the status
  reference documents TRF as the case carried to Orbit quoting the Gemini number, and the dictionary
  documents `legacy_case_ref` the same way, so (b) follows from reading a shipped sentence correctly, and
  architecture 1's own default path already performed it at step 2 as a hygiene reflex.
- **The roster's basis change, monthly hours to quarterly FTE.** (a) Convert the FY2023 and FY2024 hours
  sheets to positions by the stated conversion; (b) rescale each queue's hours-based history by that
  queue's own hours-to-FTE ratio observed over a period carried on both bases. **Dies on identifiability,
  verified in the workbook:** the basis changes cleanly at FY2025 (FY2023 and FY2024 hours by month,
  FY2025 and FY2026 FTE by quarter) and **no period is carried on both bases**, so (b) is not computable
  at all, while the Notes sheet states the conversion ("one rostered position is 7.0 rostered hours a
  working day"), which makes (a) rule application. Building the overlap to make (b) computable turns it
  into a reconciliation the hygiene battery performs and a control bench that refutes the naive read
  (readability test 4); weakening the stated conversion puts (b) on a fact in no shipped sentence.
- **The renamed queue, Record amendments to Member data corrections.** (a) Map Gemini RA to MS-DC by
  `queue_reference.csv` and read the queue's own history as its RA quarters; (b) where the rename
  accompanied a reorganisation, the comparable history is the pooled history of every predecessor that
  fed the new queue. (b) is exact only for a merge, since a split needs an allocation, which is a knob.
  **The one candidate magnitude does not kill**, because it bears on Member data corrections, the default
  winner, and a scope change could deliver the 8.79 points. **Dies on the pincer:** if the reference file
  maps both predecessors, reading it correctly gives (b), which is identity resolution and rule
  application; if it maps only one, (b) rests on a reorganisation in no shipped sentence and has to be
  recovered from a volume discontinuity, which is a withheld rule and banned as the decisive step. The
  case record also carries no case-type field, so the admissible merge version needs a predecessor queue
  the pack does not have.
- **The charge extract's April 2026 lines inside a FY2026 window.** (a) Count the cases the charges cover
  by charge date; (b) by response date. **Dies on the separation line before the pincer is reached:**
  `scheme_charges_fy2026.csv` and `fee_schedule_2025.pdf` are Ask 2's own files, the main call reads
  neither, and moving the call onto them consumes the mirror device the measured pair ceiling of 39.5
  rests on. It is a date-basis reading in any case, which is data semantics, and the reader's half-
  sureness about it is an ask fork to close in the ask layer.

**The pincer, which is the general result and the reason the stop rule fires.** For an input-property
break to decide the call, the analyst has to get it wrong, and there are only three cases. One, the pack
states the break, and the right computation follows from reading a shipped sentence: data semantics or
rule application, banned. Two, the pack does not state the break and the break is a quantity the records
measure about themselves: this is the only live case, and it is the one task194 took, where two vintages
of one series measure their own coding lag. Three, the pack does not state the break and it is not
exactly measurable: either it is recovered as a rule, which is a withheld rule and banned, or it is
unidentifiable and the design needs a field the pack does not have. **None of the four families is of the
second kind**, because each is a fact about how the records were produced (a cutover, a basis change, a
rename, an extract window) rather than a quantity the records measure about themselves: a cutover does
not measure its own capture difference, a basis change with no overlap measures nothing, a rename
measures nothing, and an extract window measures nothing.

**Screen worth reusing:** the magnitude bound killed the cutover candidate in one computation, before any
design argument. Before accepting an input-property candidate, compute the points the call needs to move
and the largest move the affected population can produce if every one of its records flipped.

### Architecture 2 decisive step, spent at stage 2 measurement (2026-10-18), before any data was cut

The reflex sweep was run as code before any separation was measured, which is what caught this, and the
sweep killed the decisive step rather than a reflex.

- **The decisive step as drawn** (attribute each candidate region's change to the interviewers who
  collected it, by measuring each interviewer's differential within the quarter from the other regions she
  worked, then netting the change in the workload-weighted lift). **Dies on Gate C, measured.** Over
  twelve seeds the decisive route named the golden region in **2 of 12** at a differential persistence of
  0.25 and **3 of 12** at 0.95, scattering across eight different regions; the easy route named the loud
  region in only 7 of 12. The route does not rank.
- **The cause is structural, not a tuning fault.** The quantity the step has to recover is a *per
  interviewer* differential, and the record measures it only through that interviewer's own out-of-region
  workload in the quarter, which at a realistic field load is 33 dwellings (median workload 33, mean 51).
  At an item prevalence of 0.20 that is a standard error of **6.96 points**, against a golden rise of 3.0
  points and a ladder margin needing the differential to about 1 to 2 points. The correction therefore
  injects several times more noise than the bias it removes, and it lands on whichever small region drew
  unluckily. A 1-point standard error needs **1,600 dwellings per interviewer per quarter** against a
  realistic 50 to 80, and the noise falls only as the square root, so no feasible pack closes it. This is
  `determinism-check` section 1's named failure, the candidates differing by less than their own sampling
  error.
- **Both ends of the persistence dial fail, for opposite reasons**, which is what makes it structural. With
  a persistent differential the pooled estimate is precise, but then the additive time-invariant
  interviewer control a solver reaches for is the right analysis and the schema tell reaches the golden.
  With a non-persistent differential the reflex lands wrong, as required, but the within-quarter estimator
  is too noisy to rank. There is no setting where the reflex lands wrong and the decisive route is
  determinate.

**The lesson, which extends the pricing rule rather than restating it.** Pricing the move against the
ceiling is necessary and was done correctly: 9.4 points of interviewer-induced bias available against
about 4.5 needed, with the two separations financed by independent parameters. It was also not sufficient,
because it priced the **bias** the mechanism can deliver and said nothing about the **variance of the
estimator that has to recover it**. Both belong in the same computation before a draw is accepted: the
move available, the move needed, and the standard error of the quantity the decisive step must estimate,
all in the graded figure's own units. A decisive step whose estimator's standard error exceeds the
ladder's margin cannot rank, however large the bias it is chasing. This is the sufficient condition the
pensions screen and this draw together point at, and it is cheap, because it is one square root.

### Architecture 2 repair (the interviewer design effect), spent at its own pricing (2026-10-18)

The repair was approved with three conditions, all to be met before design time. **Two passed and the
third failed, and the third's failure is exact rather than tunable.**

- **Condition 2, the driver check against task186: PASSED.** Driver similarity **0.05 against task186**,
  0.07 against task191 (the nearest on file), 0.06 against task58 v6, all far under the 0.12 bar. The
  distinction holds as the author framed it: task186 and task191 ask whether an effect clears noise at all
  (task191's cure is a multiplicity correction, the same for every candidate), while this asks which
  variance component belongs in the comparison, a named published quantity the design standard error
  omits, whose size per unit is an exact function of that unit's workload concentration. One BLOCK,
  `test.same_driver_older` against task191, was differentiable rather than a redraw.
- **Condition 3, the estimator family: PASSED.** The between-interviewer SD comes out at **6.73 points by
  one-way random-effects ANOVA, 6.74 by REML and 6.73 by method of moments** on 774 interviewer-cells, and
  the name is identical under all three. The family is closed in effect, and every graded figure
  (the concentration index, the counts, the printed rates) is records-fixed.
- **The repair did fix what it was meant to fix.** The variance component's relative standard error is
  **4.1 per cent** over 14 seeds (mean 7.12 points, SD 0.29), against about 100 per cent for the dead
  per-interviewer differential, a factor of **24**. A quantity the whole workforce estimates does beat one
  estimated per unit from that unit's own thin slice, exactly as the filed rule now says.
- **Condition 1, the full pricing: FAILED on name stability.** Over 14 seeds the decisive route named the
  golden region in **2 of 14**, scattering across eight regions, and the easy route named the intended loud
  region in only **4 of 14**. The intended rises were 0.4 to 5.5 points and the realised changes ran from
  +17.1 to -17.2.

**Why it is exact, and the general result.** The ranking is `change / spread`. The lever is entirely in the
denominator: a region's interviewer-induced spread is `sigma_b x sqrt(HHI_cur + HHI_cmp)`, so the
two-interviewer region at HHI 0.642 carries 1.13 `sigma_b` against the fourteen-interviewer region's 0.38,
a ratio of three whatever `sigma_b` is, and that is what flips the ranking between the design standard
error and the full spread. **But that same quantity is the random swing in the numerator.** The spread that
makes a concentrated region's movement flip is the spread that makes its measured movement noise, because
they are one variance. Large enough to flip means large enough to randomise, so the easy route cannot be
relied on to name any particular region and the designed roles do not survive the draw. Shrinking
`sigma_b` stabilises the numerator and removes the lever in the same stroke; this is the dial failing at
both ends again, and the two ends are not merely opposed, they are the same number.

**What this is and is not.** It is not a Gate C failure: on any one cut pack the analysis gives one answer,
and the estimator family is closed. It is a failure to be buildable to specification. The ladder's rungs,
margins, Gate G story and the loud and golden roles would all be hostage to the seed, so the build would
be a tuned seed rather than a designed mechanism, and `dataset-generation`'s rung exactness could not be
asserted.

**The rule it earns, and it rules out a family rather than a build.** A decisive step that moves a
*variance* cannot carry a *ranking*, because the variance that reorders the candidates is the variance
that randomises the quantity they are ranked on. Judge-against-noise mechanisms are sound where the answer
is a verdict on one named candidate, or a flag against a stated threshold on a given pack; they cannot
decide which of N is largest. Price this before drawing any such step: compute the lever's size in the
denominator and the same quantity's contribution to the numerator's spread, and if they are the same
variance the step cannot rank.

### Architecture 3, settings abandoned at stage 2 (2026-10-18)

- The first tuning (true rise 6.4 points, four-interviewer panel, `sigma_int` 8.82) gave the right faces,
  every reflex filing the supplied verdict and the golden filing not established, but the wrong margin:
  the golden sat at z 1.83 against the framework's 1.96 bar, so `sigma_int` had only to fall 8 per cent,
  about two relative standard errors, for the verdict to flip. Replaced by a true rise of 3.0 points at
  the same panel, which puts the golden at z 0.89 and the flip 61 per cent away, about fifteen relative
  standard errors. This is the author's instruction to measure the margin rather than the face, and the
  first setting would have passed a check that only read which side of the bar each route landed on.
- An ask layer with two ungrouped benchmark authorities. Died on the solved ceiling: ungrouped authorities
  carry no device, so both responses bank their four figures and the pair came out at **48.3** with a
  mirror leakage of 28.0 per cent, under the bar of 50 but far above the build-to-40 target. Every
  authority but the blank one is now inside an amalgamated return, which solves to 39.5 and 12.0.

### Architecture 3 decisive step, spent at stage 3 on a reflex nobody listed (2026-10-18)

The ten reflexes on the author's list all land wrong, measured: supplied replicate weights 4.57, design
standard error 4.57, bootstrap of the design 3.71, simple random sample 4.60, trim the most extreme unit
4.57, stratify on visible interviewer attributes 4.57, shrink 25, 50 and 75 per cent to the national change
4.03, 3.49 and 2.95, every one of them filing the supplied verdict against a 1.96 bar. An eleventh reflex,
which is not on the list and which I added while building `checks.py`, reaches the golden verdict:

- **Judge the rise against the region's own historical quarter-to-quarter variation.** The named region's
  six quarterly rates give five consecutive changes with a standard deviation of 9.15 points, against an
  observed rise of 7.64, so z is **0.83** and the verdict is not established, with no interviewer
  component, no workload log and no re-formed replication anywhere in the route. Measured across seeds:
  **in 5 of 5 seeds where the design works (z_supplied above 1.96 and z_correct below it), the own-history
  reflex reaches the golden verdict.** It is not a coin flip, it is a reliable route.

**Why it is structural, and this is the third time the same number has been on both sides.** The
interviewer component inflates the variance of a *change* only if the differential is redrawn each
quarter: a differential that persists cancels out of the difference entirely, leaving the supplied
interval correct and no stump at all. But a component that is redrawn each quarter is exactly what makes
the region's own series wobble, so the series displays the very spread the decisive step computes
analytically. The supplied interval can only be wrong by a factor the unit's own history already shows.

- Component fresh each period: it inflates the change's variance, and it is readable off the series.
- Component persistent: it is invisible in the series, and it does not inflate the change's variance.

Attempting to separate them fails on plausibility. Making the history stable relative to the field quarter
needs the panel to have been far more dispersed before the consolidation; a ten-to-four consolidation was
measured and does not do it (the history's own change standard deviation stays at 9.06 and the supplied
route drops to z 1.775, which breaks rung 2), and the gap only opens at something like thirty-to-four,
which no field operation does.

**The rule this earns, which rules out a family.** A decisive step that corrects an understated variance
cannot be silent for a call about a *change* when the unit's own history is in the pack, because the
component that makes the supplied interval wrong is the component that makes the history wobble, so an
empirical standard deviation over the unit's own periods estimates the correct spread with none of the
mechanism. Such a step is sound only where the unit has no usable history in the pack, or where the call
is about a level rather than a change. Price it with one computation before drawing: take the unit's own
period-to-period standard deviation and the correct standard error, and if the first is within about a
factor of two of the second, the decisive rung is readable off the series.

**What this is not.** It is not a Gate C failure: the analysis is determinate, the estimator family is
closed to 0.08 per cent and the verdict holds to a 30 per cent error in the component. It is a Gate F and
readability failure, the decisive rung not being silent. It is also a gate hole worth naming: `precut.py`
exits 0 on this design and the reflex sweep as listed passes, because neither can see a reflex nobody
listed, so the sweep is only as good as the enumeration behind it.

### A third gate hole, found by the same route (2026-10-18)

`precut.py`'s "semantic forks asserted" check is **inert while `generator/checks.py` does not exist**. At
stage 2 this design had ten `SF` rows and no generator, and precut exited 0 with that check passing; as
soon as `checks.py` appeared carrying assertions for SF2 and SF4 only, the same check failed and named the
other eight. So the stage-2 gate can be passed with **zero** forks asserted, and the failure surfaces only
at stage 3 when the generator arrives. The current true state of this build is `precut.py` **exit 1**, one
FAIL, on SF1, SF3, SF5, SF6, SF7, SF8, SF9 and SF10 not being asserted.

That is the same shape as the two holes already filed from this wave: a gate that checks for the presence
of a thing rather than the behaviour of it. The `Measured by:` check located a script instead of running
it; the fork check counts assertions only once there is a file to count them in; and the reflex sweep is
only as good as the enumeration behind it. The common repair is to make each gate fail loudly when the
thing it depends on is absent, rather than pass quietly.
