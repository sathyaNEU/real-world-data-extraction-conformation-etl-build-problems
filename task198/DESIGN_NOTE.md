# task198 design note

**Architecture 4 is being drawn** on healthcare-delivery-health-economics /
payment-claims-health-plan-analytics. Architectures 1 (pensions answer-time), 2 (interviewer attribution,
and its approved repair) and 3 (the replication groups a supplied interval is formed over) are all spent;
each carries `### ARCHIVE` headings below, their fates are in the card's `lineage`, and the measurements
that killed them are in `## Tried and rejected`.

**What the three deaths bought, and it governs this draw.** All three died on a variance lever. Architecture
1's residue was a knob; architecture 2's lever and its ranked quantity's noise were one variance;
architecture 3's lever was readable off the unit's own series, because a component has to be redrawn each
period to inflate a change's variance and that is exactly what makes a series wobble. Architecture 4
therefore takes a **bias in a point estimate the whole population estimates**, not a variance, which is the
one shape those three results leave open: a bias persists, so it is invisible in the unit's own series, and
it still moves the level.

## Draw

Keewatin Valley Health Trust, a member-governed employers' health purchasing cooperative running a
self-funded medical plan. Which of its eight contracted multi-specialty physician groups takes the one
contract renegotiation its trustees fund for the 2027 plan year.

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task198.json`, architecture v4, registered 2026-10-18; `guard.py check` re-run **against the registered card as the last act of stage 1**, returning **WARN, no BLOCK** |
| Domain / subdomain | `healthcare-delivery-health-economics` / `payment-claims-health-plan-analytics` (the one AD-serving task type this lane had never drawn) |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 07, grid of cells: the group by procedure-family grid of observed against contracted price |
| Decision type | `pick_one_of_n`, answer unit `named_option` plus one price level |
| Gate G | `method_or_model_selection` |
| Strategy | `other`: the reported value on a row is the lesser of an ask and an entitlement, and the decision is about the entitlement |
| Layer 2 family | `field_method`, pattern `own:contracted-price-behind-a-lesser-of-plateau` |
| Gaps | `objective` (decisive), `population` |
| Generators | G1 unit-of-value swap (decisive), G3 record versus operation |

**Why a bias and not a variance, which is what the three dead architectures bought.** Architecture 1's
residue was a knob; architecture 2's lever and its ranked quantity's noise were one variance; architecture
3's lever was readable off the unit's own series, because a component must be redrawn each period to
inflate a change's variance and that is exactly what makes a series wobble. **A bias is the shape those
three results leave open:** it persists, so it does not move the unit's series and is invisible in it, and
it still moves the level. Screens 4 and 5 below are where that shows up as numbers.

**The decisive step.** Every claim line is priced as the lesser of the group's billed charge and its
contracted rate, which is ordinary adjudication. So where a group bills below its own contract, the
allowed amount is its charge and not the price its contract entitles it to. The decision is about which
contract is dear; the file reports allowed amounts. The contracted percentage of the reference schedule is
recovered exactly from the codes a group does bill above, where its allowed amounts plateau at the rate.

**The five screens, run on the clean truth before a word of design** (`stumping` Part 3). Units are dollars
per standardised line, on one common service mix held identical across groups so that no composition lever
is in play.

1. **The residue is a method, not a knob.** With the estimand filed, what stays open is whether the
   contract's price level is the average allowed amount or the entitlement the allowed amounts are censored
   against. Both are exact computations on the shipped record. The pooling residue that a first cut had
   (recovering a rate from a sparsely populated plateau drifts with how many quarters are pooled) is closed
   structurally rather than pinned: the contract is **one** percentage of the schedule, as these contracts
   are written, so any code whose plateau is reached gives the same multiple and every reasonable estimator
   of it agrees exactly. **Case two of the pincer:** the book measures its own contract.
2. **Move available against move needed: 134.09 against 43.21, a ratio of 3.10.** The easy route names
   PG-ARDEN; the decisive route names PG-BRYMER, which holds the dearest contract at 2.05 times schedule
   while showing the fourth-highest observed price. Decisive margin 1.206x; easy-route margin 1.110x, which
   is under the 1.15 floor and is the first thing stage 2 widens.
3. **The standard error of what the step must estimate: 0.0000 per cent, for all eight groups.** The
   contract multiple is a plateau, so a single quarter recovers it exactly. This is the "quantity the whole
   population estimates" at its limit, against the 4.1 per cent of architecture 2's repair and the roughly
   100 per cent of its drawn step.
4. **The lever is not the ranked quantity's noise.** The golden group's bias is 134.15 while the quarterly
   standard deviation of its observed price is 0.642, a ratio of 209. The lever is a level bias fixed by
   billing practice and the noise is sampling in a mean, so making the lever bigger randomises nothing.
   This is the screen architecture 2 failed.
5. **The unit's own history does not estimate what the step computes.** The golden group's own
   quarter-to-quarter change in observed price has a standard deviation of 0.903 against a bias of 134.15,
   a ratio of 149, where the rule's threshold is a factor of two. A bias persists, so the series is flat
   and the bias is invisible in it. This is the screen architecture 3 failed, and it passes here for a
   structural reason rather than a tuned one.

**The enumerated sweep, per the rule the three deaths earned.** Enumerated by asking what the decisive
quantity is a substitute for, then listing every other way the pack measures that same thing. Eight
measures of a contract's price level, **every one naming a wrong group**:

| Measure of the contract's price level | Names | Verdict |
|---|---|---|
| mean allowed per standardised line (the easy route) | PG-ARDEN | loud |
| mean billed charge per standardised line | PG-ARDEN | loud |
| mean allowed-to-charge ratio, the discount | PG-ELLIOR | other wrong |
| mean allowed over the reference schedule | PG-ARDEN | loud |
| median allowed per code, standardised | PG-ARDEN | loud |
| trim 5 per cent each tail then average | PG-ARDEN | loud |
| 90th percentile of allowed per code | PG-ARDEN | loud |
| 99th percentile of allowed per code | PG-ELLIOR | other wrong |
| **the contract multiple off the plateau (decisive)** | **PG-BRYMER** | **golden** |

**Two thin margins stage 2 must widen, named now.** The 99th percentile names PG-ELLIOR with the golden
second at 1.007x, and the allowed-to-charge ratio at 1.002x. Neither reaches the golden, but a percentile
approaches the plateau from below, so the gap between the golden and the nearest decoy on those two
measures is widened in the data before the ladder is accepted.

**The two traps on this ground, screened at the draw and not in the design.** Completion and development of
immature periods is task194's live driver: both plan years are closed here, every line is final and nothing
is developed. Two capture channels with dependence is task196's: there is one record of each line and no
second channel. The subdomain's three existing cards are all ETL (task447 composition_mix, task451 and
task458 maturity_censoring) and none is anomaly-detection, so the pairing is unspent.

**Guard WARNs answered.** `repeat.decision` and `repeat.question_form`: the decision is a pick of one
contract from eight for one funded renegotiation, so the form follows the decision. `ban.org_family` fired
on the re-check and the organisation was redrawn from a university system to a member-governed purchasing
cooperative, which the world carries better anyway; the mechanism was this slot's own registration pushing
architecture 3 out of the three-build window and pulling task199 into it.

### ARCHIVE architecture 3 (spent): Draw

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

### ARCHIVE architecture 3 (spent): Default path

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

### ARCHIVE architecture 3 (spent): Stump sentence

A competent solver rebuilds both quarters across the two questionnaire layouts, rebases the region across
the amalgamation, rules out every rival explanation the pack carries on a shipped fact, judges the +6.6
point change against the survey's own supplied replicate weights at 3.53 standard errors and files the rise
as an established population change, because every replicate the pack ships is formed on primary sampling
units and no replicate ever varies the interviewer composition of the quarter, so the interval cannot see
the one source that produced the move.

### ARCHIVE architecture 3 (spent): Three rules

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

### ARCHIVE architecture 3 (spent): Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 release figure | the release states its own provisional basis | the release's own columns | yes, read the dashboard | none | no | yes, read off | readable |
| 1 rebuilt change | the framework files the window and the item | the dwelling records' columns | yes, the obvious group-by | none | the battery finds the layout and base joins | one group-by | readable |
| 2 supplied replicate weights (**the default path**) | the design documentation states the replication method for the weights it supplies | 84 replicate weight columns, named | yes, the rigorous reflex, and it is the right instrument for sampling error | none | no | one standard formula | readable |
| 3 replication re-formed over the field workload (**decisive**) | no sentence says units sharing an interviewer are not independent, nor that the replication should be re-formed | the workload log is at assignment grain and carries no outcome; the grouping must be built across three files | no: every reflex files the supplied verdict, measured, ten of them at z 2.38 to 4.14 | no control or published figure ties only under it | the battery passes under both replications | not a subtraction or a ratio of a reported figure; the component is estimated from the whole workforce | silent |

### ARCHIVE architecture 3 (spent): Semantic fork table

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

### ARCHIVE architecture 3 (spent): Ladder

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

### ARCHIVE architecture 3 (spent): Closure table

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

### ARCHIVE architecture 3 (spent): Literal reader

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

### ARCHIVE architecture 3 (spent): Oracles

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

### ARCHIVE architecture 3 (spent): Ask sheet

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

### Architecture 4 rung 2, killed by the completed enumeration (2026-10-18)

The first sweep scored eight measures and every one landed wrong, but all eight measured the **observed
price level**. None attempted the **contract rate itself**, which is the question the lesser-of clause
provokes. Completing the enumeration on the author's five:

| Measure of the contract rate | Names | Margin | Verdict |
|---|---|---|---|
| 1 maximum observed allowed per code, standardised | PG-BRYMER | 1.073x | **reaches the golden** |
| 2 modal allowed per code, standardised | PG-ELLIOR | 1.049x | lands wrong |
| 3a censored-line allowed, standardised over that group's censored codes | PG-BRYMER | 1.049x | **reaches the golden** |
| 3b hybrid: censored-line rate where available, observed mean elsewhere | PG-ELLIOR | 1.049x | lands wrong |
| 4 allowed over schedule on censored lines only, one ratio by the standard mix | PG-BRYMER | 1.206x | **reaches the golden, exactly** |
| 5 share of lines censored, highest first | PG-HOLLOWS | 1.000x | lands wrong |
| 5 share of lines censored, lowest first | PG-BRYMER | 0.998x | **reaches the golden** |

**Measure 4 is the kill and there is no defence of the clause that survives it.** It returns 433.283
against the decisive route's 433.283: not an approximation of the answer, the answer, from a two-step
filter and divide that is the most natural thing to compute after reading that allowed is a minimum.

**Why it is structural and not a tuning fault, and it is the same number on both sides for the fourth
time.** On a censored line `allowed == rate` exactly, by the very mechanic that creates the bias. Every
line does exactly one of two things: it is censored, and then it publishes the rate; or it is uncensored,
and then it creates the bias. So any group with any censored line publishes its own rate in full, and the
golden group publishes it on 38 per cent of its lines. There is no setting where the minimum censors the
observed price and does not simultaneously reveal the rate, **because here censoring is revelation.**
Driving the golden's censoring to zero would hide the rate from every route including the golden one.

The author's hint, that the golden's exposure might sit where the censoring is sparsest, does not save it:
measure 4 recovers the multiple from **any** censored line, because the contract is one multiple, and
sparseness does not matter when the quantity is constant. The thing that made screen 3 exact at 0.0000 per
cent is the thing that makes measure 4 exact.

**The structural change that would close it, named for the author's ruling and not implemented.** Make the
contracted rate a percentage of schedule that differs **by procedure family** rather than one multiple for
the whole contract, which is how these contracts are in fact written. Then a censored line reveals only
that family's multiple, and measure 4, a single pooled ratio over censored lines, returns a
censored-mix-weighted average of the family multiples instead of the standard-mix price level, wrong by
exactly the gap between a group's censoring mix and the filed standard mix. Measures 1 and 3a fail the
same way. The decisive step becomes recovering each family's multiple from its own censored lines and
reweighting to the filed mix, which is a construction rather than a filter, and screen 3 stays exact
because each family's multiple is still a plateau. This changes what the decisive construction is rather
than a parameter of it, so it is not a retune; whether it is worth taking is the author's call.

### Architecture 5: the ground enumerated through the dichotomy, one pass (2026-10-18)

Run `stumping` 1.2a first, as instructed, which asks whether the filed quantity is observed. That splits
the ground in two and both branches were searched. Screened against the two live traps (task194's
development of immature periods, task196's two dependent capture channels), against the 33 corpus cards
that touch claims, coverage or enrolment, and against the sixth screen architecture 4 earned.

**Branch A, the filed quantity is unobserved, so two estimators of it can stand.** What a health plan
genuinely cannot see in its own claims, taking the author's steer toward absence over transformation.

| Candidate unobserved quantity | Killed by |
|---|---|
| A1 claims incurred but not yet reported or paid | development of immature periods: task194 live, task451 and task130 on file |
| A2 the latent count behind imperfect discovery of other coverage | two dependent capture channels, task196 live; every discovery route is a channel |
| A3 a condition's prevalence, ascertained only through billed encounters | task458, in this very subdomain: a trait counted from events logged while each unit is observed |
| A4 care under a delegated sub-capitation, rows wholly absent and unflagged | not estimable from the pack except through a second channel (A2) or a rate transported from comparable groups, which is the comparison and so WHAT |
| A5 out-of-network care members never submitted, absent and selected on claim size | the correction is a size-truncation model: task182 v4's length-biased entry, and an estimator family the dichotomy says four architectures died on |
| A6 member cost-sharing actually collected, as against the obligation the plan records | genuinely unobserved and nothing in a claims pack estimates it, so not a design |
| A7 dependents who became ineligible, the event never recorded | estimable only from audit response, which is nonresponse selection, and `population_selection` is banned against the last three builds |
| A8 the coding a provider submitted before the plan's clinical editor acted | observed if the pack ships the submitted version or an edit reason code; otherwise the uncaught share needs the editor's sensitivity, which is A2 |
| A9 what the plan would have paid under a different contract | arithmetic on filed rates: rule application |
| A10 the plan's retained cost next year under its stop-loss attachment | a future value through a nonlinearity, which is task187's Jensen gap, and a forecast besides |

**Branch B, the filed quantity is recorded, so the only live levers are selection and nonlinearity in how
the records relate to it, and the decisive step must be records-fixed.**

| Candidate records-fixed step | Killed by |
|---|---|
| B1 which of billed, allowed, plan paid, member responsibility or reference amount the comparison runs on | filed is rule application, unfiled is a fork on the main recommendation |
| B2 the services absorbed into a global surgical period | the absence is rule-determined, so identifying them is executing the payment rule |
| B3 claims processed out of service-date order, so the cost-sharing accumulators misapply | replaying adjudication in service order is executing stated rules |
| B4 split lines against distinct encounters | invertible by grouping on the claim key, so the quantity is observed |
| B5 the contract rate behind the lesser-of plateau | architecture 4, killed by the sixth screen: censoring is revelation |
| B6 per-family rates reweighted to the filed mix against pooling at the censoring mix | two weightings of observed components separated by the estimand's unit, the shape qualified in 1.2 |

**The result, and it is a property of the ground rather than of the search.** A claims file is a payment
ledger, and the only things a payment ledger cannot see are **payments not yet made, payments made
elsewhere, conditions never billed, and what the rules would have done.** Those four are exactly
completion, capture, ascertainment and rule replay. Three are live or spent in this subdomain (task194 and
task451, task196, task458) and the fourth is banned as a decisive step by rule 3. Every absence on the
ground routes into one of them, into revelation on a subset, or into not being estimable at all.

**No candidate reached measurement, so there are no six screens to report.** Each died at the draw on a
named rule, and measuring a candidate already dead would be the dressing-up the pricing sequence exists to
prevent. The ground is not exhausted in the sense task182's thirteen affordances were, but the four latent
quantities a payment ledger admits are, and that is the part the decision needs.

### Architecture 6: the rate's denominator searched mechanism by mechanism, four measured (2026-10-18)

Architecture 5 enumerated latent quantities on the **numerator** only. All ten of its branch-A candidates ask
what a payment ledger cannot see about **payments**, and A6 (member cost sharing actually collected) was
retired with "nothing in a claims pack estimates it, so not a design". The **eligibility record and the
denominator never entered that enumeration**, which is the hole this pass searched. Four structurally distinct
Layer 2 mechanisms, each killed by a number computed on a clean truth generator before any file was cut.
Scripts: `screen_M2.py` and `screen_M1_M3_M4.py` in the builder's scratch directory.

- **M1, the exposure base itself** (a rate per covered-life month, against lives times twelve or a period-end
  stock). Dead on the WHAT screen and confirmed by measurement: with the unit filed as the rate's
  denominator, the span integral **is** the filed quantity, so the reflex "compute life-months from the
  spans" returns a reflex-over-golden ratio of **1.000000 for every one of twelve accounts**, and all four
  routes name the same account. A route that disagrees is not computing the filed quantity, which makes the
  error arithmetic rather than analysis.
- **M2, a repeat-event share evaluated at a common length of cover** (the share of lives reaching two or more
  admissions in a benefit year, which is convex in each life's own exposure and rises with the spread of use
  inside the account, so no exposure-normalised mean rate can order the accounts). The strongest of the four
  and the one the pass was opened on. Dead on the reflex sweep, run as code before separation was measured:
  of nine routes, **five reach the golden account and two of those are the crudest in the list**. The golden
  names HUATULCO at 7.72 per 1,000 with a margin of **1.075x** over its runner-up; the raw per-life share
  with no exposure handling at all names the same account with a margin of **1.382x**; restricting to the
  lives that carried a full year, a filter and a divide, names it at 8.85 with a margin of **1.147x**. Only
  the frequency rate per 1,000 life-months and a mean-only Poisson evaluated at twelve months land wrong
  (both on BERRENDO). Two routes land wrong and five land right, and the two crudest land right with a wider
  margin than the decisive route's own.
- **M3, the episode grain** (claims grouped into episodes on a clean-period window, so a per-episode cost is a
  per-claim cost times a grain the pack never states at one level). Dead on the residue test, measured: the
  call **moves with the window**, naming one account at 7, 14, 21 and 30 days and a different one at 45, 60
  and 90 days, with a margin of **1.006x** at the pivot and **1.000x** (an exact tie) at every window above
  it. The window is a knob and the answer is a function of the knob, which is architecture 1's death.
- **M4, left truncation of per-life spend at an account-specific deducible** (eligible expense per life is
  latent below each account's own deducible, and the book's spread of deducibles identifies it, which is the
  A6 that architecture 5 retired as not estimable). Two easy routes do land wrong, paid per life and the
  add-back of the deducible times the claimant count, both naming account B against the golden's I. Dead
  anyway, three times over: the **mean spend among claimants**, one groupby, names I; re-truncating at a
  common retention names I; and the plain high-cost-claimant rate names I. Structural reason, and it
  generalises: **a deducible suppresses only the bottom of the per-life distribution**, so every tail
  functional is exact (the largest deducible is MXN 150,000 against a 600,000 threshold, so no tail life is
  ever truncated away) and only the mean is latent, and recovering the mean is the paid-against-eligible
  basis question, which is branch B1's semantic fork on the main recommendation. Dead on lineage besides:
  task189, on this objective two days earlier, spends a per-unit average over measurements known only to lie
  below a limit that differs by the instrument that produced them, naming "censoring them all at one common
  limit" as a wrong route, which is this mechanism and this construction.

**Two reusable screens this pass earned, both measured rather than argued.**

- **The common-exposure subset screen.** A decisive step of the form "put the units on a common exposure
  before comparing them" cannot carry a stump, because the subset of units already at that exposure is a
  filter and a divide that estimates the same quantity without any model (8.85 against the golden's 7.72, the
  same account, at a wider margin). The only escapes are that no unit attains the exposure, which is
  completion and task194 holds it; that too few do, which is variance and three of this slot's four deaths
  were variance levers; or that the attaining subset is unrepresentative, which is a selection plant.
- **The truncation-direction screen.** Before designing on a threshold that suppresses records, ask which end
  it suppresses. One that suppresses the bottom leaves every tail functional exactly observable and leaves
  only the mean latent, and the mean is a basis question. Only a threshold that suppresses the **top** leaves
  a latent quantity a tail functional needs.

**Where the pass stopped, and it is an axis and not a mechanism.** `guard.py check` on a probe card carrying
the drawn axes returns **BLOCK ban.pairing, "domain plus objective pairing repeats a recent build against
task194 (v3)", fix: redraw the domain or the objective**, with task194 v3 registered in this same domain on
the anomaly-detection objective. An axis ban is not clearable by differentiation and `register` refuses a
BLOCK, so **no driver whatever makes this cell registrable while task194 v3 sits in the window**: the block
is independent of the mechanism and of everything above. The honest move is to hand it back rather than
relabel the pairing to pass, and the window clears on its own as later builds register. The remaining axes
drawn here all came back clear on that same probe (shape 03, `grain_or_unit`, `settled_transaction_ledger`,
`finance_controller`, `binding_constraint` legal, gap `population`, `committee_or_panel`, `period_close`,
`financial_institution`), so the pairing is the only thing standing.

### The pin pincer run on architecture 6's four candidates, and the client's four patterns for this task type (2026-10-18)

Run after the four measurements, on the author's correction. The test: **a rigor pattern whose pin fixes one
of the estimand's five parts (population, outcome, window, unit, comparison) cannot carry the decisive step.**
File the pin and the step is the execution of a filed clause, which rule 3 bans; leave it unfiled and the main
call forks across the licensed readings, which `precut.py` refuses on the fork table. Only a pattern whose
quantity is **estimated** rather than **defined** can carry HOW. This is not a new finding: it is already
filed at `stumping/SKILL.md` 211 to 224, earned by task200's slot, which is the read this pass owed before
designing and did not make. Its words: "what separates them is the estimand's unit, and the unit is one of the
five parts: name it and the computation follows from the clause, which is rule application; leave it unnamed
and the readings are three different numbers, which is a semantic fork on the main recommendation."

| Candidate | Part the pin fixes | Defined or estimated | Verdict |
|---|---|---|---|
| M1 member months (pattern 4) | **unit**, the rate's denominator | defined | **dead on the pincer**, both horns |
| M3 episode grain | **unit**, the grain | defined | **dead on the pincer**, both horns |
| M2 repeat-event share at a common length of cover | none; a functional of a distribution | **estimated** | escapes the pincer, dead on the reflex sweep |
| M4 left truncation at the deducible | none; mean eligible expense per life | **estimated** | escapes the pincer, dead on measurement and on task189 |

**The pincer predicted both measurements it applies to, which is the strongest evidence it is right.** M1's
filed horn is the measured 1.000000 reflex-over-golden ratio across all twelve accounts: the span integral
**is** the filed quantity, so no analytical step survives. M3's unfiled horn is the measured fork: one account
at 7, 14, 21 and 30 days, another at 45, 60 and 90, a margin of 1.006x at the pivot and an exact tie above it.
Neither needed killing twice, and the pincer would have killed both before a line of generator code.

**M2 and M4 escape the pincer and the distinction is worth keeping**, because it marks where this ground's
remaining room is: both quantities are functionals of a distribution rather than clauses of an estimand, so
two methods of estimating one filed quantity genuinely stand, which is what the screen at
`stumping/SKILL.md` 207 asks for. They died on the data instead, M2 because the subset already at the common
length of cover is a filter and a divide, M4 because a deducible suppresses only the bottom of the
distribution. So the room is real and the two mechanisms that occupy it are both spent.

**Ratio of totals is spent three times over in this slot**, and no later pass should re-screen it: the pincer
(weighting alone separates the two, so what separates them is the unit); the filed rule at
`stumping/SKILL.md` 211, earned by task200, which measured the unnamed clause at 12.22, 12.22 and 9.20 on one
cut and found no third position; and this note's own earlier closure-table death, that weighting is axis 7,
which `precut.py` requires closed, so it cannot also be the open decisive step.

**All four of the client's patterns for `payment-claims-health-plan-analytics` are now shut, with the reason
for each.** This is the part that decides whether the cell is worth another pass.

1. **Complete recent claims with lag-triangle factors.** Spent: task194's vintage family, with task451 and
   task130 on file.
2. **Voluntary bundles need a comparison group, DiD with checked pre-trends.** Pin: "voluntary participation;
   non-participant episodes available", which fixes the **comparison**, one of the five parts. Dead on the
   pincer, and `causal_design` sits next door on task199 and task163 besides.
3. **Reconcile in contract order.** Pin: "the contract sequence is stated". Rule application on its face,
   banned by rule 3 as a decisive step.
4. **Risk-adjusted PMPM as a ratio of totals over member months.** Pin fixes the **unit**. Dead on the
   pincer, measured as M1 at 1.000000, and spent three times over as above.

**The conclusion, and it is about the cell and not about this pass.** Architecture 5 enumerated the
**numerator's** latent quantities and found four, three live or spent in this subdomain and the fourth banned
by rule 3. Architecture 6 searched the **denominator** and found that it is the unit, so the pincer shuts it,
and that the two distribution-shaped escapes are both spent. The client's own library for the task type is
shut four ways. Both terms of a claims rate have now been searched, which is the part architecture 5 could not
claim. **The cell is shut for this objective on the mechanism**, independently of the `ban.pairing` BLOCK that
shuts it on the axis, and a further pass here should be spent only if the author reassigns the task type or
the objective.

### Architecture 7: the ground reassigned to accounting-audit-forensic, three mechanisms measured (2026-10-18)

The author reassigned the domain and the task type, which is the one condition architecture 6 named for
spending another pass here: card `domain` `accounting-audit-forensic` (a house domain, `client_domain`
`banking-credit-financial-risk`), task type `banking-credit-financial-risk/fraud-aml-detection`, objective
unchanged. The pairing has never been built, the domain has six never-drawn subdomains, and the task type
carries no client rigor pattern block, so `layer2_pattern` would take `own:<name>` and nothing in the
client library either constrains or helps. Two ground-specific bans were honoured and neither was
re-screened: monetary unit sampling (task190 architecture 3, probability proportional to size, dead at
stage 4 after two judge passes) and the two-channel capture overlap (task196, shipped on this very task
type the day before). Screens: `screen.py` in the builder's scratch directory, 12 units, clean truth, no
file cut.

- **M1, endogenous sample size under a sequential stop-or-go attribute plan.** Each unit's control test
  stops at its own filed count of deviations, so the examined count is a random variable set by what the
  examination found, and deviations over items tested is biased upward by a factor set by the unit's own
  stop number (measured 1.179x to 1.789x across the twelve, and the factor is monotone in the filed stop
  number). The design-unbiased estimate is `(k-1)/(n-1)`. **Dead on the reflex sweep, run as code before
  any separation was measured: the naive route already names the golden**, at a margin of **1.301x against
  the designed route's own 1.083x**, and **five of eight reflexes reach it**, the crudest of them ("rank on
  how few items it took to reach the stop") at **1.344x**, again wider than the designed route. Spearman
  against the truth is **+0.9371 for the naive route** and +1.0000 for the designed one, so the correction
  improves the ordering below the leader and never moves the leader. Dead a second way where it does move
  anything: the correction is `naive x (k-1)/k`, one multiplication by a filed column of the audit plan,
  which matches the designed route at Spearman **+0.9860**, so the decisive rung is readable on tests 1 and
  6 of the readability screen. **The structural reason, and it generalises: the stopping rule is
  informative about the quantity being estimated**, because a unit with a high deviation rate reaches its
  stop in fewer items, so the statistic the bias acts on (the examined count) is the statistic that carries
  the signal. Bias and signal are one number, which is architecture 2's "lever and noise are one variance"
  in the first moment rather than the second.
- **M2, the expected-by-chance coincidence baseline.** Vendor-master against employee-master shared
  attribute links (address, bank account) across twelve business units, where the attribute's own frequency
  distribution produces chance matches at a rate set by each unit's attribute concentration, so the genuine
  conflict count is latent and the field's object is observed minus expected under a configuration null.
  **Dead on magnitude, and the designed route itself cannot rank: it names a unit with 2 genuine links
  against the golden's 9.** At the golden unit the observed count is **42,595 against 9 genuine links**, so
  the signal is 2.1e-4 of the observable and the chance count's own sampling standard deviation is about
  **206 against a signal of 9, a ratio of 0.044**; the designed route's error at that unit (**-31.10
  against a truth of +9**) is 4.4x the entire quantity it is trying to recover. **No reflex reaches the
  golden either**, which is the diagnosis rather than a reprieve: the mechanism cannot rank at all. Single
  dial, both ends: the only way to lift the signal above the nuisance's noise is to make the attributes
  nearly unique, which removes the chance matches and with them everything the step corrects.
- **M3, right-censoring at the TOP.** The one shape the truncation-direction screen leaves open, taken
  deliberately: per-item losses recorded only up to a per-item cap, so each unit's total is latent above
  the cap and a tail functional is needed rather than a mean. **Dead on the forced-construction test**
  (`stumping` 1.6a, task194 architecture 3's death): the graded figure for the golden unit is
  **40,253,070 / 30,708,434 / 55,420,236 / 120,560,108** under lognormal, gamma, Weibull and Pareto-tail
  maximum likelihood on the same censored records, a spread of **3.926x** where a forced construction needs
  about 1.00x, and the **ranking forks too** (Weibull names a different unit from the other three). Pinning
  the family files the method and spends the stump; leaving it open forks the figure. Same dial, both ends.
  task130 reached the same place from the other side and closed it by eliminating distribution fitting
  outright.
- **A fourth family retired on lineage at no cost**, found in the probe's `driver.near` read rather than by
  screening: lead-driven (adaptive) examination, where the examined set is enriched by following leads from
  successful finds so the found rate over the examined count overstates the population total. **task124
  architecture 2 holds it** in both its loop-0 and harden-loop-1 forms ("a rate measured on units that were
  examined because they showed signs of the outcome is carried to a population"), at driver similarity 0.09
  and 0.13. It would also have died on the common-exposure subset screen, since the initial random sample
  alone is a filter and a divide.

**What the three kills leave, stated as the condition a fourth candidate has to meet.** Each died on a
different clause, and together they are a filter: the latent quantity must be **not collinear** with the
easy statistic (M1), **large** relative to the nuisance's own sampling noise (M2), and recoverable by a
construction **forced without a distributional family choice** (M3). The shapes that satisfy the third
clause are linear algebra, a design weight or an exact identity, not a fitted tail; design weights are
spent on this ground twice (task190's probability proportional to size, stratified projection), an exact
identity is revelation, and "an unobserved component of an observed total recovered by a fit" is task182's
spent family, which `slots` surfaced on the first probe. The task type's own estimated quantities were then
enumerated rather than brainstormed, and every one is spent, open-family or pincer-dead: the counterfactual
loss without the control (comparison, or a fitted family), the undetected loss (task196 capture, task194
completion), the recovery (censoring, task201 and task189), the model's performance on the rejected
population (reject inference, an openly contested estimator family), the reachable exposure (task28), the
number of distinct networks (task192 architecture 1), and the time to detection (task190 architecture 4).

**Where this pass stopped, and unlike architecture 6 it is the mechanism and not the axis.** `guard.py
check` on a probe card carrying this ground's axes returns **BLOCK, exit 1**, on `test.same_puzzle_older`,
`test.same_driver_older` and `ban.forcing_event` (`audit_or_inspection` against task194 v3) in the first
configuration, and a second probe clears both the forcing event (`period_close`) and the two-layer fields,
leaving **only the two structural signature tests, which are functions of whatever mechanism survives**.
**No `ban.pairing`, `ban.subdomain`, `ban.shape`, `ban.strategy`, `ban.calibration`, `ban.role`,
`ban.artifact`, `ban.spine`, `ban.org_family` or `ban.forum` fired on either probe**, so
`accounting-audit-forensic` x `anomaly-detection` at shape 01 is **open on every axis ban**, with
`uncertainty_hold`, `closed_decision_corpus`, `compliance_or_audit`, `filed_standard`,
`professional_services`, `auditor`, `period_close` and a Portugal / EUR world all clear. The honest
reading is therefore the opposite of architecture 6's: **the cell is available and the mechanism is what is
missing**, so a further pass here is worth spending, and it should start from the three-clause filter above
rather than from a candidate. The probes are `task198_probe_card.json` and `task198_probe2.json` in the
builder's scratch directory; neither was registered.

### Architecture 8: the ground reassigned to human-factors-ergonomics, three mechanisms measured (2026-10-18)

The ground moved again, to `human-factors-ergonomics` / `safety-incident-error-analysis`, objective
unchanged, with `structural_verdict`, `causal_design` and `confirm_surface_read` reserved and the one spent
anomaly-detection driver on the cell named for the pass to draw away from (task181: events arise when one
moving unit passes through the position of another present at the same time, so the expected count follows
the crossings a period's traffic creates rather than the time units spend). Three Layer 2 mechanisms were
screened as code on a clean truth, each killed by a measured number, no file cut (`screen_M1.py`,
`screen_M2.py`, `screen_M3.py`, `sweep_law.py`, each run twice to byte-identical output). The axis read came
back the other way from the mechanism read, as in architecture 7.

**What the slot search bought before any code ran, and it closed the cell's natural family.** `guard.py
slots` on the candidate nouns returned task149 (shipped: the hazard per unit of working time rises steeply
with how fast a fixed content of work is done, measured against that work's engineered content) and
task171's own kill of the duty-hour variant, which it retired as task149's driver by the abstraction test at
guard 0.15. Taken with task202's six designation-set kills on this exact cell and task182's experience
composition, **the whole workload, pace, fatigue, time-on-task, learning-curve and rate-in-cumulative-
experience family is spent on this ground**, which is what the brief's own hint list points at. The first
candidate drawn (a crew-shift's assigned work against the time it has for it, the demand-capacity mismatch
of work measurement) was retired free on that search: it is task149's driver in other nouns. **Its lexical
score was 0.27 against task149, a WARN and not a BLOCK**, so the guard would have passed it with a
differentiation line while the abstraction test kills it outright: the documented blind spot, measured again
here with a number.

**M1, the interruption channel behind a count rise.** Jobs, crews, a dispatch change that pushes reactive
work onto crews already on a planned job, an error hazard multiplied 3.4x on an interrupted job. Dead on the
first measurement: **the naive per-job before-and-after excess reaches the causal excess exactly** (seed 0,
83.0 against a truth of 84.2; the within-depot variant 83.0), so the channel construction is a decoration on
the graded figure. The golden's own estimator is also the noisier one, its hazard ratio spreading 2.98 to
5.02 over five seeds against a truth of 3.4, which is the pricing death of architecture 2 in another world.

**M2, interference through a shared authorising desk.** The same dispatch change raises the isolation
requests the converted depots send to one network control desk; the authoriser's own error rate rises
convexly with the desk's concurrent load, so the change's whole effect lands on jobs at every depot,
converted or not, and a weather-driven reactive shock in the same window moves the same load. The shape was
drawn from F9's one shipped hold (interference through a shared pool) along its own vary axis, the
interference structure (a congestion externality rather than a zero-sum transfer). Dead on measurement:
**the crude network before-and-after is the answer** (seed 0, 314 against a truth of 309; the rate-adjusted
read 294), the designed route returns 297 to 441 against a truth of 308 to 455, and **a one-line regression
of daily incidents on daily requests, a derived daily total, lands within 25 per cent with the same sign and
the same verdict** (228 against 309). The difference-in-differences did not go to zero either, 147 to 236,
because a depot's error count is proportional to its own requests, so the arms separate and the easy route
never files "exonerated".

**The law both deaths measured, and its boundary swept.** `sweep_law.py` varied the hazard multiplier (2.0,
3.4, 6.0), the affected share (0.25, 0.62) and the size of a second independent mover of the same total
(0.00, 0.15, 0.40). **With the intervention the only mover and the exposure base recorded, crude over truth
is 0.954, 0.953 and 1.001 at the three multipliers**: the crude before-and-after rate excess IS the causal
excess, and no comparison design can carry a graded figure built on it. The ratio only departs where a
second mover exists (1.14 to 1.96), and closing it is then a split of one total between two movers, which is
`decomposition_attribution` and another lane's ground, not a causal design. The one other regime where the
crude route is materially off, a small affected channel at a low multiplier, is sampling error on the graded
count (a 1.886 ratio on a truth of 8.9 incidents), not a ladder. **So on this ground a causal design may not
grade a total over the whole population and window**: the graded object has to be a per-unit effect inside
one window, which is what M3 was drawn to be.

**M3, the error-rate multiplier an interruption carries, identified inside one window.** No before and
after, so neither law can apply: 67,000 jobs, the hazard rising with each job's unrecorded difficulty and
multiplied 2.6x when the crew is pulled off it, the dispatcher choosing which job to interrupt on that same
unrecorded difficulty, the recorded work-type code too coarse to adjust it away, and the identifying
variation coming from the other depots' emergencies consuming a shared standby pool. The confounding worked
as drawn: **the raw contrast reads -0.08, +0.12 and -0.02 extra errors per 100 interrupted jobs against a
truth of 0.77**, so the easy route files that interruption costs nothing. It died on both of the remaining
screens at once. **The reflex lands the truth: adjusting for every recorded attribute returns 0.740, 0.801
and 0.751 against truths of 0.773, 0.770 and 0.767, inside 4 per cent**, because a job's recorded duration
is a proxy for the difficulty the design withholds (and the coarse-code stratification 0.72 to 0.79,
propensity matching 0.64 to 0.72). That proxy is structural, not a tuning fault: any authentic work-order
file carries durations, and tuning the correlation away would rest the build on asserting that how long a
job took says nothing about how hard it was. **And the decisive route cannot rank anyway: the Wald estimate
is 0.749, 1.073 and 1.323 with a bootstrap standard error of 0.88 to 1.14, which is 1.3 times its own point
estimate, and its 90 per cent interval runs -0.94 to +2.8**, covering zero in every seed; closing that to a
tenth of the effect needs about 150 times the depot-days the pack could carry.

**Where this pass stopped: the axis is open, the mechanism is missing, exactly as in architecture 7.**
`guard.py check` on a probe card carrying the whole reserved axis set (`human-factors-ergonomics` /
`safety-incident-error-analysis`, anomaly-detection, shape 11, gap `rule`, pattern C, `confirm_surface_read`,
`structural_verdict`, `causal_design`, `retry_or_revision_log`, `planning_thread`, `executive_team`,
`incident_or_complaint`, `utility_or_infrastructure`, `programme_officer`) returns **WARN, no BLOCK**: one
`people.first` WARN on a persona, nothing else. No axis ban fired, and neither `test.same_puzzle` nor
`test.same_driver` fired, because `structural_verdict` is unspent on this objective and gap `rule` with
pattern C and `confirm_surface_read` is a free triple; nearest driver 0.09 (task149). The probe is
`task198_probe3.json` in the builder's scratch directory and was not registered.

**What a ninth pass must satisfy, one clause per kill.** The graded object must be (a) **not a total over
the population and window**, since the crude before-and-after supplies that to within 5 per cent (M1, M2,
the sweep); (b) **not identified against a confounder any recorded attribute proxies**, since durations,
coarse codes and crew identity are all shipped and the adjustment on them lands the truth within 4 per cent
(M3); and (c) **not estimated from variation thin enough that its own standard error approaches the effect**,
which on a depot-day panel rules out every instrument a shared pool creates (M3). The three together say the
decisive quantity cannot be a hazard multiplier, a counterfactual count or an effect per unit of work on
this ground. What they leave is the shape the corpus's one Gate F strong hold actually used (task197): an
unobserved quantity whose forcing input sits in another file at another grain, with the construction forced
by arithmetic rather than by a fit, and the ninth pass should start from the file that does the forcing
rather than from the estimator. On this cell the unexamined candidates for that file are the investigation
record at barrier grain and the plant's own telemetry as a census (not a capture channel) of one error
class; both were named and neither was screened, and the second carries a tolerance that reads as a knob.

- The crew-shift's assigned work against the time it has for it, the demand-capacity mismatch of work
  measurement (architecture 8, retired free at the slot search 2026-10-18). It is task149's shipped driver in
  other nouns, at lexical 0.27 (a WARN, not a BLOCK) and an outright kill on the abstraction test, and
  task171 had already retired the duty-hour variant of it on the same grounds.
- The interruption channel behind a count rise (architecture 8, M1, measured 2026-10-18, nothing cut). The
  naive per-job before-and-after excess reaches the causal excess exactly, 83.0 against a truth of 84.2, so
  the construction is worth nothing on the graded figure; the designed route's own hazard ratio spreads 2.98
  to 5.02 against a truth of 3.4.
- Interference through a shared authorising desk, a congestion externality on F9's vary axis (architecture 8,
  M2, measured 2026-10-18, nothing cut). The crude network before-and-after is the answer, 314 against a
  truth of 309, a one-line regression on a derived daily total lands within 25 per cent, and the
  difference-in-differences stays positive at 147 to 236 so the easy route never files "exonerated".
- The error-rate multiplier an interruption carries, identified inside one window off a shared standby pool
  (architecture 8, M3, measured 2026-10-18, nothing cut). The reflex adjustment on recorded durations lands
  the truth inside 4 per cent (0.740 against 0.773) and the identifying instrument's standard error is 1.3
  times its own point estimate with a 90 per cent interval covering zero.

### Architecture 9: the draw inverted, file first, three constructions measured (2026-10-18)

Run under the rule filed at `stumping` Part 3, "where three screens close a cell, invert the draw": start from
the file that does the forcing, not from the field's estimator. The cell is unchanged
(`human-factors-ergonomics` / `safety-incident-error-analysis`, anomaly-detection) and the axis read from
architecture 8 held, so no time was spent on the guard. Screens are `screen_M1.py`, `screen_M1b.py`,
`screen_M2.py`, `screen_M2b.py`, `screen_proxy.py` and `screen_M3_family.py` in the builder's scratch
directory, all on a clean truth, each rerun to byte-identical output, no file cut.

**The file, and what it pins that nothing else pins.** The investigation record at barrier grain: one row per
(occurrence, barrier), carrying each credited barrier's state at the moment of the occurrence. It is the only
file on this ground that observes several barriers **jointly on one occasion**. The barrier register declares
design intent at hazard x layer grain, the assurance record tests each barrier alone on its own schedule, the
override register logs each inhibit separately, and the demand archive carries challenges with no barrier
detail. The joint cross-section exists nowhere else, and that is what the three constructions below were built
on. The telemetry-as-census candidate was not screened: its time tolerance is this number's architecture 1
death and the brief ruled it second.

**M1, the coincident-unavailability alignment count.** Graded object: the number of challenges in the window
that arrived while a hazard's credited protection was reduced to at most one available layer, built by
intersecting the layers' out-of-service intervals (override register, interval grain) against the demand
archive (event grain) under the register's credited set. Maintenance scheduled into each unit's quiet season,
one unit's layers taken out together on shared campaign permits while it was running. **Dead twice over.**
Graded as a count, the golden was the only two-layer hazard on all five seeds and `credited layer count`, one
sorted column, named it every seed, alongside the LOPA product and the proper independence expectation; with
the layer count held fixed at three the golden became the hazard with the **most challenges** on all five
seeds and **10 to 13 of 18 reflexes** reached it, the plain challenge count among them. Graded as a share to
divide the first-order driver out, the golden moved across seeds (H08, then H03 four times) at margins of
**1.080x to 1.436x**, mostly under the 1.15x floor, while `share of challenges with two or more layers down`
named it 5 of 5. **The law, and it generalises: a count of events falling inside a constructed condition is
first order in the event count and only second order in the condition, so the crude event count ranks it;
divide the event count out and the quantity becomes a time share that one group-by on the interval register
reproduces; what is left after both is the arrival noise, which is the same quantity that creates the
alignment.** Single dial, both ends.

**M2, the effective depth of a protection stack.** Graded object: the number of connected components of a
hazard's credited layers under "shares at least one plant element", against the credited count. Two grains,
the barrier register (hazard x layer) and the instrument register (layer x element); neither states effective
depth, and components are not edge counts, since sharing is transitive (A to B, B to C collapses three layers
to one group though A and C share nothing) and multiple (one pair sharing three elements is three shared
elements but one merge). **The reflex screen was the strongest measured on this ground, 0 to 1 of 12 routes
reaching the golden**, and it died anyway, three ways. As an integer the graded object tied **four hazards at
overstatement 2 on every seed**, an exact tie, because a quantity ranging over 0 to 2 carries one live degree
of freedom. Regraded as the field's continuous object, the risk reduction actually delivered (one credit per
independent group, best member of each), the golden moved across **three hazards over eight seeds** and the
set failing the filed target was **empty on three of the eight**. The sweep settled it: redrawing the
per-layer figures alone with the element topology held **completely fixed**, 40 redraws per setting, returned
**3 distinct golden hazards at every realistic range and 6 at the widest**, with the two ranges that held a
stable fail-set sitting at median margins of 1.066x and 1.528x. The topology cannot carry the verdict; the
assured-availability column decides it.

**The one-column proxy screen, filed mid-pass, run on everything.** A forcing file usually publishes a scalar
summary of the construction it forces. Measured here, 144 to 240 unit-draws per case:

| construction | plainest column of its own forcing file | corr | one-line route |
|---|---|---|---|
| M1 alignment count | the demand archive's own challenge count | **+0.6582** | **16/20** |
| M1 alignment count | challenges falling in any outage | +0.6930 | 14/20 |
| M2 depth overstatement | the register's sharing edge count | **+0.9631** | n/a |
| M2 depth overstatement | max element multiplicity | +0.8575 | n/a |
| C1 occurrences with a barrier verifiably available | the record's own "barriers in place" tally | **+0.9960** | **18/20** |
| C2 failed-on-demand split by breach order | the record's own degraded-barrier count | **+0.9817** | **17/20** |
| C6 hazards simultaneously at reduced depth | degraded count x the register's fan-out column | **+0.9905** | **19/20** |
| C4 potential-consequence 95th percentile | the actual-consequence 95th percentile | +0.7146 | 9/20 |
| C3 latent degradation among undetermined rows | the determined-degraded count | +0.6584 | 8/20 |
| C3 same, against the prompt-subset filter and divide | degraded found inside two days of the occurrence | +0.4580 | 5/20 |

**C1 is the brief's own named direction and it is the worst of the set.** "How many of a class of occurrences
had a given barrier actually available" correlates **+0.9960** with the tally the investigation record already
publishes, and the one-line route reaches the truth **18 of 20** draws. So the inversion was run correctly,
file first, and the file turned out to publish a scalar summary of the very quantity it forces. C4 is dead
besides on a law already on file: recovering a top-censored tail functional forks 3.926x across distribution
families (architecture 7, M3).

**What survived, and it is handed back rather than drawn.** C3 alone passes the proxy screen in both forms:
the degradation hidden in the barrier rows whose state the investigation could not determine, because making
the plant safe after an occurrence **removes the evidence of a degraded barrier and leaves the evidence of an
intact one**, so the undetermined rows are enriched in failures and the share computed over the determined
rows understates it most for the sites whose investigations open slowest. The prompt-subset filter and divide
does **not** reach it (+0.4580, 5/20), so the common-exposure subset screen does not close it. It is not
drawn here, for two reasons a tenth pass must settle first: the graded object as defined is still a count over
each unit's occurrences, so M1's tally law has to be answered before anything else, and `guard.py check`
surfaced **task31 R8 at 0.05** ("a milestone duration is estimated from a log whose slow cases are still open,
so dropping the censored rows understates") and **task199 at 0.06**, which are the same insight in other
nouns at a lexical score far under the WARN floor. The abstraction test, not a screen, is what that direction
needs first.

**The axes, probed twice and clear both times, neither card registered.** Probe A carries the reserved set
exactly as allocated (shape 11, gap `rule`, pattern `none`, `confirm_surface_read`, `structural_verdict`,
`causal_design`, `retry_or_revision_log`, `planning_thread`, `executive_team`, `incident_or_complaint`,
`programme_officer`) with `org_family` redrawn to `manufacturer` and a Netherlands specialty chemicals world:
**WARN, no BLOCK, nearest driver 0.05**, one `repeat.question_form` WARN against task248 and no persona WARN
at all. Probe B carries the honest labels for C3 (`generators` G12 first, absence of record against record of
absence, `method_or_model_selection`, `population_selection`, question form `whether`): **WARN, no BLOCK**,
the question-form WARN cleared, `repeat.gate_g` and `overuse.gate_g` raised and answerable in one line, and
`ban.strategy` silent on `population_selection`. With `pattern` `none` the guard reads `generators[0]` as the
decisive pattern, confirmed in both verdicts, and `test.same_driver` fired on neither triple. The cards are
`task198_card.json` and `task198_card_probeB.json` in the builder's scratch directory.

**Three axis corrections this pass earned.** `pattern` `C` was dropped for `none` plus a named G-code, since a
structural verdict has no candidate list for a serviceable share to sit behind. `org_family`
`utility_or_infrastructure` was dropped for `manufacturer`, which no longer repeats the cell incumbent's air
navigation service provider (task181) and is the native home of layer-of-protection analysis;
`manufacturer` is free because task194 moved to `software_or_platform`. And `causal_design` is **not honest**
for anything screened in architecture 9: none of M1, M2 or C1 to C6 is a comparison design, so the allocated
strategy value has no carrier on this ground and probe B records the honest substitute.

**Where the pass stopped: the axis is open for the third consecutive pass and the mechanism is missing again.**
Architecture 7 said it, architecture 8 said it, and this pass says it with the inversion run properly and the
forcing file named in advance. Taken with the pharmacology closure and architecture 6's claims closure, the
dichotomy is now measured on four separate grounds: **an administrative safety record supports only exact
arithmetic on a shipped structure, which is rule application, or a fit, which opens the estimator family, and
the barrier-grain investigation record does not escape it, because the construction it forces is published as
one of its own columns.** The cell is spent on the mechanism for this objective, and a tenth pass here should
be spent only on C3 with the abstraction test answered first, or the number should move.

- The coincident-unavailability alignment count, challenges arriving while a credited stack was reduced to one
  layer (architecture 9, M1, measured 2026-10-18, nothing cut). Graded as a count the credited layer count and
  then the plain challenge count name it on every seed with 10 to 13 of 18 reflexes reaching it; graded as a
  share the golden moves across seeds at 1.080x to 1.436x and one group-by names it 5 of 5. The demand
  archive publishes the challenge count at corr +0.6582 and the one-line route lands the truth 16 of 20.
- The effective depth of a protection stack by shared-element connected components (architecture 9, M2,
  measured 2026-10-18, nothing cut). Best reflex screen on this ground at 0 to 1 of 12, dead anyway: as an
  integer four hazards tie at overstatement 2 on every seed, as a continuous risk reduction the golden moves
  across three hazards over eight seeds with the fail-set empty on three, and redrawing the availability
  column alone with the topology fixed gives 3 distinct goldens at every realistic range. The register
  publishes the sharing edge count at corr +0.9631.
- The occurrence count at which a barrier was verifiably available, the direction the brief named
  (architecture 9, C1, measured 2026-10-18, nothing cut). The investigation record's own "barriers in place"
  tally is a proxy for it at corr +0.9960 and the one-line route reaches the truth 18 of 20 draws. With it,
  on the same screen: failed-on-demand split by breach order (C2, +0.9817, 17 of 20) and hazards
  simultaneously at reduced depth per barrier (C6, +0.9905, 19 of 20).

### Architecture 10: re-rooted onto environmental monitoring, the draw inverted, three constructions measured (2026-10-20)

The ground moved to `physical-environmental-sciences` / `environmental-monitoring-exceedance`, objective
unchanged, a cell this number has never carried. Two spent anomaly-detection drivers sit there and the pass
drew away from both (task180: an event enters the record only above the instruments' noise, and where that
noise follows a daily cycle the smallest events are recorded only in the quiet hours; task189: a per-unit
average over measurements known only to lie below a limit that differs by the instrument). A third card sits
on the cell on data quality (task247, censored or lagged release), so detection limits and release lag are
both worked here. The draw was run inverted, file first, under `stumping` Part 3, and step two, the one-column
proxy screen, was run on every construction before any separation was measured. Screens are
`screen_arch10.py`, `screen_m2_family.py` and `confirm_dial.py` in the builder's scratch directory, all on a
clean truth, each rerun to byte-identical output, no file cut.

**What the slot search bought before any code ran, and it closed the cell's whole air half.** `guard.py
slots` on the candidate nouns returned **task245**, which is already an air-quality exceedance-day build in
this physical setting: PM10 against 50 micrograms per cubic metre, the 35-day allowance, data capture per
station, informative outage, and the 90.4th percentile of reported daily means and the expected-exceedance
scaling named as the reflexes its ladder is built against. It also returned **task229** (a convex conversion
of a daily mean, hydrometric station-month grading), **task248** (24-hour composite samples with each
sample's load restored at a paired decay rate) and **task249** (recovery against the nominal failing good
batches). Four devices this cell's natural family would have used are therefore spent before the draw: the
exceedance-day count scaled for lost capture, the convexity of a conversion applied to a daily mean, the
holding-time decay restoration, and the laboratory recovery correction. No card records any of them on this
cell, and `recent`, `mechanisms`, `nearest` and `heart` cannot see them.

**The file, and what it pins that nothing else pins.** The hydrometric gauge archive: a continuous
15-minute record of flow and the runoff index at the catchment's gauges, running the whole statutory season.
It is the only file on this ground that observes **the driver of the exceedance on every day of the window,
including every day nobody attended**. The laboratory register observes concentration only on attended
occasions, the sampling rota pins who attended and when but carries no value, the site register is static,
the ratification log pins only the difference between two releases of the same attended days, and the
classification return publishes the season's verdict after the fact. The continuous record of the
unattended days exists nowhere else, and that is what all three constructions below were built on.

**M1, the at-source concentration recovered through holding time.** Graded object: each point's seasonal
95th percentile after each bottle is restored for the analyte lost between field collection and analysis,
with the decay rate estimated from the spread of holding times inside the record (the van rounds differ, so
points on a long round carry systematically longer holds). Dead on screen 2 and on screen 1 together. The
correcting input is **one scalar** (a single decay rate), so the construction is a monotone rescaling
sample by sample, and its per-point effect is carried entirely by the point's own mean holding time, which
the register prints: corr(correction factor, mean holding time) = **+0.9274**, and the one-line route, take
that column and divide, reaches the truth **12 of 20** against the construction's own **12 of 20**, an exact
tie. corr(construction output, naive statistic) = **+0.9613**. The attaining subset (the bottles analysed
same-day) reached **5 of 20**, so screen 3 does not fire, and it does not need to.

**M2, the season's percentile rebuilt against the flow-duration curve.** Graded object: each point's true
95th percentile of daily concentration over the 150-day season, where the crew's 20 bottles were all drawn
on scheduled settled-weather rounds while the exceedances arise on the runoff days, recovered by reading the
sampled concentrations against the gauged runoff and integrating over the season's own flow-duration curve.
**It passed screens 1, 2 and 3, the only construction on this ground that has.** Screen 1: the correcting
input is neither a scalar nor a looked-up per-unit figure, it is the point's own runoff response plus the
season's whole runoff distribution. Screen 2: corr(construction output, the forcing file's plainest column,
the mean runoff on the point's own sampling days) = **-0.0194**, corr(correction factor, that column) =
**-0.4566**, and the one-line route reached the truth **8 of 20** against the naive route's 8 of 20. Screen
3: the attaining subset, the bottles already drawn at above-median runoff, reached **7 of 20**. The
construction moved the graded figure by a median **4.64x** (p10 2.69x, p90 10.40x). **It died on the three
screens that kill survivors, all at once.** The estimator family: five forms a competent analyst would use
on the same records (log-log fit over the flow-duration curve, flow-band stratification on the season's
quintiles, inverse-probability reweighting onto the season, a quadratic in log runoff, a shared network
slope) returned **2.85 distinct worst points per draw, maximum 4, against a floor of 1.00**, and the graded
figure spread **3.744x at the median, 6.891x at p90 and 214.2x at the worst** on the true worst point. The
estimator's own standard error: a 200-draw bootstrap of the construction against the top-two margin came
back at **1.211 of the margin at the median and 19.0 at p90**, so the construction's own noise exceeds the
gap it has to rank on, which is architecture 2's death in new nouns. And the one repair the family screen
allows, pooling the response across the network so the fit is forced, **inverts the ladder**: the pooled
construction reaches the truth **4 of 20 against the one-line plain-column route's 7 and the naive route's
7**, worse than the route it corrects. Single dial, both ends: estimating the response per point forks the
figure, pooling it makes the construction worse than doing nothing. Measured hit rates on the family harness
put the per-point construction at 9 of 20 against the naive 7 of 20, so the lever was thin once priced
against the right comparison rather than against the raw percentile.

**M3, the exceedance count prorated over the sonde's service intervals.** Graded object: the number of days
in the season above the standard at each continuously monitored point, after each reading is corrected for
the fouling drift that accumulates between service visits and resets at each one, with the drift measured by
the pre-clean and post-clean readings the service log records at every visit. Dead on the naive route. The
construction reaches the truth **20 of 20** on the worst point and the naive count reaches it **19 of 20**;
the median correction factor is **1.0000** (p10 0.786, p90 1.193) and corr(construction output, naive
count) = **+0.9818**, because the drift direction is a coin flip per sensor and cancels across the network.
The exceeding-set separation that remains (construction 20 of 20, naive 12 of 20, plain-column route 12 of
20) rests entirely on points sitting inside the correction's own width of the boundary, which is the
seed-hostage failure `stumping` Part 3 prices at under one standard error to the boundary. Screen 3 also
fires: the days just after a service, a filter and a divide, reached 12 of 20.

**The one-column proxy screen, run on all three before any separation was measured.** 280 unit-draws each.

| construction | plainest column of its own forcing file | corr | one-line route |
|---|---|---|---|
| M1 holding-time restoration | the register's own mean holding time | **+0.9274** | **12/20 (ties the construction)** |
| M2 season percentile off the flow-duration curve | mean runoff on the point's own sampling days | **-0.0194** | 8/20 (naive 8/20) |
| M3 fouling prorated over service intervals | the service log's own pre-clean minus post-clean offset | -0.0028 | 13/20 (naive 19/20) |

**The abstraction test closed M2 a second time, independently of every measurement, and the guard could not
see it.** `guard.py check` returned **task461 at 0.06** ("the decisive quantity is a low quantile of a
distribution seen directly only over one short and unrepresentative period; the long record of a correlated
auxiliary series, carried to the target through the proportional relationship their overlap shows, gives the
distribution over the full range of conditions") and **task466 at 0.06** ("a low quantile of a yearly extreme
fitted to two records of the same process"). Stripped of nouns, task461 is M2: the same latent structure (a
quantile of a distribution observed only over an unrepresentative subset of the conditions), the same default
path (compute the quantile from the observed subset), and the same correction (carry it through a correlated
auxiliary series that was recorded over the full range). Both sit far under the 0.12 WARN floor, so the
lexical screen passes them, and both are shipped. M2 was therefore dead on lineage as well as on its three
measurements, and the measurements are what make the kill checkable.

**Twelve directions killed on paper before the three were coded, each on a closure already on file.** The
per-sample species conversion from total to un-ionised ammonia and the bioavailability correction (the
conversion is a filed formula, so the step is rule application, and the convex-over-a-spread version is
task229 and task187); the averaging-period mismatch, 15-minute peaks read off an hourly record (task202, a
within-aggregate upper cut taken from unit averages); the 1-in-3 or 1-in-6 sampling schedule read against a
day-of-week exceedance pattern, and the multiplexed analyser cycling across sample points (both are task180,
a cyclical pattern interacting with a unit-specific observation schedule); top-of-range saturation at
instrument-specific spans (task189 with the censoring direction flipped, same latent structure, same default
substitution, same censored-data correction); data capture and informative outage (task245 outright);
annualisation of a part-season record from long-running neighbours, and the diffusion-tube bias factor (the
periods-complete filter and divide, and a single scalar); the natural-source and regional-background
subtraction (the nuisance estimated where the signal vanishes, closed by task201 across negative controls,
calibration nulls and blank baselines); load estimation and the flow-weighted mean (a ratio of totals against
a mean of ratios, task200's estimand death and the denominator dichotomy); detection-corrected occupancy from
repeat visits (the attaining subset is the most-visited points, a filter and a divide, and the family is
task196's); the deconvolved count of truly non-compliant points (shrinkage is both the reflex and the better
estimator); the zone maximum over a varying number of sites (task191, an extremum against a null extremum);
and the shared-cylinder or shared-laboratory common-mode artifact, which fails rule 3's litmus outright, since
the number the task overturns is actually wrong and catching it is what defeats the model, so it is a plant.

**The axes, probed three times, and the window moved twice under the pass.** The brief's window named
task269, task270 and task271 as the last three registered builds; by the time the probes ran, `ban.shape` was
firing against **task471** and `ban.org_family` against **task471** (government_agency) and then **task475**
(local_government), neither of which existed when the cell was allocated. Probe A (shape 10, gap population,
G3 decisive, `method_or_model_selection`, `structural_verdict`, `other` as strategy, `field_unit_lead`,
`regulator_or_inspector`, `season_or_peak`, `published_series`, a Republic of Ireland world) returned four
BLOCKs: `ban.shape`, `ban.org_family` and the two structural signature tests. Probe B swapped the decisive
generator to G7 and the signature test moved rather than cleared (task271 and task471 instead of task468).
Probe C, shape **14** and org_family **utility_or_infrastructure**, clears **every axis ban**:
`ban.pairing`, `ban.subdomain`, `ban.pattern`, `ban.calibration`, `ban.role`, `ban.artifact`, `ban.spine`,
`ban.strategy`, `ban.shape`, `ban.forum`, `ban.forcing_event` and `ban.org_family` are all silent, and the
only BLOCKs left are `test.same_driver` (gap population, G3, `method_or_model_selection`, against task468)
and `test.same_driver_older` (the same signature in task126, task450 and task469). Those two are functions of
the mechanism, not of the world, exactly as in architectures 7, 8 and 9: **the axis set is open for the
fourth consecutive pass and the mechanism is missing again.** Three WARNs stand and are answerable in a line
each: `overuse.domain` (4 of the last 12), `repeat.gate_g` and `overuse.gate_g` (8 of the last 12). Cards are
`task198_arch10_probe.json`, `task198_arch10_probeB.json` and `task198_arch10_probeC.json` in the builder's
scratch directory; none registered.

**One axis label the pass refused rather than banked.** The honest `stump_strategy` for M2 is
`population_selection`, which `ban.strategy` blocks against task271, and an axis ban is not clearable by
differentiation. The probe carries `other` with the reason written into `notes` rather than a label picked
because it passes, and the block is reported rather than argued: on this ground the strategy that names the
mechanism is unavailable, and that is a fact about the window, not about the design.

**Where the pass stopped, and what it adds to the dichotomy.** Architectures 6, 7, 8 and 9 each reported an
open axis and a missing mechanism on four separate grounds. This pass says it on a fifth, with the inversion
run properly and the forcing file named in advance, and it sharpens the finding rather than repeating it:
**an environmental compliance record offers exactly two ways to reach the window the standard is written
over, and both are closed.** Either the record already covers the window, and then the exceedance statistic
is exact arithmetic on the shipped rows, which is rule application; or it covers only the occasions a crew or
an instrument produced, and then reaching the window needs a quantile or a count transported through an
auxiliary series, which is task461's and task466's shipped driver and which forks across the transport
family at 3.744x with a standard error of 1.211 of its own margin. The cell's measurement half (thresholds,
censoring, capture, lag, decay, recovery, drift) is spent across task180, task189, task245, task247, task248
and task249, and its window half is spent across task461 and task466 in other nouns. **The number should
move rather than take an eleventh pass here**, and if it stays, the only direction not yet priced is the one
architecture 9 handed back, C3, which still owes the abstraction test first.

**The thirteen `## Three rules` lines for M2, the candidate drawn furthest, with the three that do not pass
said plainly.** They are recorded because the client's check is what a rework has to answer, and those three
lines, `Decisive step:`, `Estimand:` and `Lesson:`, are the reason this draw is not filed.

- `Task type:` environmental-monitoring-exceedance, which the taxonomy serves with AD and DQ, so the pairing
  with anomaly-detection is legal. **Passes.**
- `Domain test:` the deciding quantity is the 95th percentile of a bathing water's seasonal daily
  concentration distribution, which the field estimates by reading sampled concentrations against the
  continuously gauged runoff that drives them and integrating over the season's flow-duration curve.
  **Passes.**
- `Swap:` put retail stores and footfall in for bathing waters and runoff and the call stops making sense,
  because there is no continuously recorded physical driver whose distribution over the unattended days is
  known, so the construction has nothing to integrate over. **Passes.**
- `Layer 1:` two source systems for one determinand with imperfect point keys, a provisional and a ratified
  release of the same season overlapping, a statutory bathing season against the laboratory's reporting
  year, cfu per 100 ml against the log10 units the classification table is written in, tablet local time
  against UTC gauge telemetry, results carried as text with qualifiers. Each is produced by the
  organisation's own systems and none carries the stump. **Passes.**
- `Layer 2:` `estimand_identification`, the methodological choice being whether the season's percentile is
  read off the attended occasions or rebuilt over the window the standard is written for. **Passes.**
- `Decisive step:` rebuild each point's seasonal percentile against the gauged flow-duration curve rather
  than from the settled-weather bottles. **Passes as a sentence and fails as a step**, because five standard
  forms of that rebuild return 2.85 distinct answers per draw.
- `Not semantics:` holds. Every clock, unit, qualifier and classification band can be read correctly and the
  empirical percentile of the attended occasions is still the wrong number. **Passes.**
- `Not rule application:` holds for the transport step, since no filed rule says to reweight the season onto
  the gauged distribution, and the classification table only converts a percentile into a class.
  **Passes.**
- `Analyst test:` a strong analyst computes the empirical 95th percentile of the season's twenty bottle
  results against the classification table and files the named water as sufficient. **Passes**, and it is
  executable on the clean truth.
- `Estimand:` the 95th percentile of the daily concentration distribution at the named point over the
  statutory season, every day of the window in the population. **Fails.** Filed literally, the window's
  every day is in the population and the method of reaching the unattended days is left open, and the data
  does not separate the candidates: the spread across the licensed forms is 3.744x at the median against a
  figure printed to one decimal.
- `No decoy:` holds. Nothing is planted, no memo argues the wrong answer, and the settled-weather bias is a
  property of how a crew works rather than a defect laid to be caught. **Passes.**
- `No certified replay:` holds. No certified or published figure is reproduced to bless the method, and the
  classification return is published after the window rather than used to recover the construction.
  **Passes.**
- `Lesson:` a model would learn to rebuild a window's quantile from the driver recorded over the whole window
  rather than from the occasions a crew attended. **Fails on uniqueness**, because task461 and task466 both
  ship that lesson, in a correlated auxiliary record and in a censored earlier record, at driver scores of
  0.06 that the lexical guard does not reach.

**The default path M2 would have shipped, its named wrong answer, the golden and the stump sentence**, kept
because the next pass on this cell should not rediscover them.

1. Read the laboratory register, conform the three point-identifier spellings across the agency and council
   returns, drop superseded rows and keep the ratified release where both exist.
2. Convert every result to cfu per 100 ml, resolve the text qualifiers, and restrict to the statutory season
   on the sampling date rather than the analysis date.
3. Per bathing water, take the season's twenty results and compute the 95th percentile, log-normally as the
   classification table's own definition does.
4. Read each percentile against the classification bands and file the class.
5. `Ends on:` Carrowbeg Strand sufficient, at a seasonal 95th percentile of about 780 cfu per 100 ml.
6. `Golden:` Carrowbeg Strand poor, at a rebuilt seasonal 95th percentile above the 1,000 cfu per 100 ml
   band edge, because the season's twenty bottles were all drawn on settled-weather rounds and the runoff
   days that carry the exceedances are not among them.

`Stump sentence:` A competent solver conforms both returns, reads every qualifier and clock correctly and
computes each bathing water's log-normal 95th percentile from its season of bottle results, and files
Carrowbeg Strand **sufficient** at about 780 cfu per 100 ml, because the percentile is taken over the
occasions the crew attended rather than over the season the standard is written for.

`Data-native sentence:` the crew's rounds are scheduled and settled-weather, the gauges run every day of the
season, and the determinand is produced by runoff, so the record's occasions and the window's exceedances
are generated by opposite halves of the same driver.

- The at-source concentration recovered through holding time (architecture 10, M1, measured 2026-10-20,
  nothing cut). The correcting input is one scalar, so the construction is a monotone rescaling whose
  per-point effect is the register's own mean holding time at corr +0.9274, and the one-line route ties the
  construction exactly at 12 of 20. Spent besides as a device in task248.
- The season's 95th percentile rebuilt against the gauged flow-duration curve (architecture 10, M2, measured
  2026-10-20, nothing cut). The only construction on this ground to pass screens 1, 2 and 3 (corr -0.0194,
  the attaining subset 7 of 20, the plain-column route 8 of 20), and dead four ways: five licensed forms give
  2.85 distinct answers per draw and spread the graded figure 3.744x at the median, the bootstrap standard
  error is 1.211 of the top-two margin at the median and 19.0 at p90, pooling the response to force the fit
  inverts the ladder to 4 of 20 against the naive 7, and stripped of nouns it is task461's and task466's
  shipped driver at 0.06.
- The exceedance count prorated over the sonde's service intervals (architecture 10, M3, measured
  2026-10-20, nothing cut). The naive count reaches the worst point 19 of 20 against the construction's 20,
  the median correction factor is 1.0000 because the drift direction is a coin flip per sensor, and the
  remaining set separation sits inside the correction's own width of the boundary. The days just after a
  service, a filter and a divide, reach 12 of 20.
- The air half of the cell, retired free at the slot search (architecture 10, 2026-10-20). task245 already
  ships PM10 exceedance days with data capture, informative outage and the 90.4th-percentile and
  expected-exceedance reflexes; task229 ships the convex conversion of a daily mean; task248 the decay
  restoration of a composite; task249 the laboratory recovery correction. No card on this cell records any of
  the four.

- Architecture 11, wave 8, 2026-10-20. The number moved off human-factors-ergonomics to
  `business-operations-analytics` x anomaly-detection on the author's allocation, with
  `decomposition_attribution` reserved. Three candidates screened on clean truth, nothing cut, no card
  registered. All three dead; the allocated strategy is BLOCKed by the guard and was displaced. Detail in
  `### Architecture 11 (wave 8, business operations): three measured deaths and one axis finding` below.

### Architecture 11 (wave 8, business operations): three measured deaths and one axis finding

Harness `screen.py` and `screen2.py` in the builder's scratch directory
(`scratchpad/w8_198/`), both run three times with byte-identical output, both run under `python3 -I` so the
script directory stayed off `sys.path`, no pickle and no cache. Nothing was written to `target/` or
`golden/` and no card was registered.

**The axis finding, which came first and is reusable.** `guard.py check` on a probe card returns
`BLOCK ban.strategy`, "stump strategy decomposition_attribution repeats a recent build against task475".
task475 registered 2026-10-20T12:58:04Z and sits inside the live three-card window, so the allocated
strategy was already spent when it was allocated. A sweep of all fifteen strategy values against the same
window: BLOCK on `decomposition_attribution` (task475) and `composition_mix` (task471); WARN
`three_rules.strategy_risk` on `withheld_rule_corpus_fit`, `stated_rule_hard_construction`,
`grain_or_unit`, `time_semantics` and `identity_resolution`, which rule 3 bars from deciding a call;
clear on `forecast_method_backtest`, `maturity_censoring`, `binding_constraint`, `population_selection`,
`causal_design`, `uncertainty_hold`, `other` and `withheld_rule_official_decoy`. The same probe also
returns `BLOCK test.same_driver_older` against task107 for the triple (gap `objective`, pattern G3, Gate G
`decomposition_attribution`), so the Gate G axis is shut on this cell independently of the strategy label.

**The cell is virgin on its label and occupied on its ground, and that is measured.**
`business-operations-analytics` is a house domain, so `precut.py`'s `Task type:` line and `guard.py`'s
`three_rules.task_type` rule route the draw through the client task types it inherits. It inherits five
that serve anomaly-detection (`general-statistics-data-science/exploratory-data-analysis-distribution-assessment`,
`general-statistics-data-science/multiple-testing-selective-inference`,
`human-factors-ergonomics/safety-incident-error-analysis`,
`healthcare-delivery-health-economics/provider-quality-risk-adjustment`,
`healthcare-delivery-health-economics/payment-claims-health-plan-analytics`), and those five carry
**6 of the 34 AD cards** (task181, task182, task185, task191, task194, task198), one of them this slot's
own architecture 4. `guard.py coverage` prints 0 for the pairing because it counts the house label. The
same arithmetic on `accounting-audit-forensic`: coverage 0, four inherited AD cards (task182, task185,
task191, task196). Three house domains (`product-analytics`, `economics`, `marketing-consumer-research`)
inherit no AD-serving task type at all and are undrawable there.

**M1, failures per unit of duty-weighted wear exposure (equipment rental, telematics as the forcing
file).** Main file: service records and contract days per machine class. Forcing file: the telematics
interval log, which records engine state and a load signal at a grain no attribute of the class-level file
carries. Construction: failures per 1,000 duty-weighted hours. This one passed four screens and died on
the fifth, which is why it is worth recording in full. Screen 1 passes, the correcting input is a load
factor per machine-day and not a scalar. Screen 2 does **not** fire on the published engine-hours column,
corr +0.7302 (Spearman +0.7429, range +0.2363 to +0.9795) and the one-divide route reaches the truth only
9 of 20; the naive routes are genuinely wrong, 6 of 20 on failures per machine-year, 8 of 20 on failures
per 1,000 rental days, against the designed route's 20 of 20. Screens 3 and 10 do not fire either: the
full-load subset, measured with its own Poisson noise at about 42 events per class per year, reaches the
truth 6 to 14 of 20 across unaffected shares of 0.05 to 0.99, because the subset's sampling error swamps a
1.077x gap between the top two classes. Screen 11 does not apply, there is no constructed benchmark.
Screen 12 does not fire on its own terms, a telematics log is not a quality indicator the deciding
organisation is obliged to publish. The ceiling is healthy, 1.820x of load-factor spread available against
1.077x needed. **It dies on determinacy.** Duty-weighted hours are the integral of load to a power, and
nothing in the record fixes the power: across the five exponents a competent analyst would use (0.5, 1.0,
1.6 as a damage exponent, 2.0, 3.0 as an S-N exponent) the designated class takes **2.55 distinct values
of 5, up to 4 on one draw**, and the graded rate at the golden class spreads 2.5531 per 1,000 duty hours
against a level of 2.3667, which is 107.9 per cent of the figure and 255 times a printed precision of 0.01.
The discretising rescue does not reach it, because what forks is the designation itself. Two further kills
stand behind that one: if the telematics file publishes duty or load hours as a column, which is the
commercial purpose of fleet telematics, the one-divide route reaches the truth 20 of 20 at corr +1.0000;
and an equipment maker's own severity-adjusted service schedule, which realism puts in the pack, is a filed
sentence naming the decisive quantity.
- **Law earned:** a per-case correcting input that is a physical *intensity* (load, severity, pressure,
  temperature) is not "forced arithmetically" however fine the second file's grain, because converting
  intensity into the damage the decision is about needs an exponent the record does not carry. The wave's
  surviving clause holds only where the second file's quantity enters the construction linearly and by
  identity, as a count, a duration or a currency amount.

**M2, concurrency-adjusted labour minutes per work type (back-office processing, the operator session log
as the forcing file).** Redrawn on paper before any harness, on the brief's own instruction, because the
`Not rule application:` line cannot be written: dividing each item's recorded open minutes among the items
the same operator held open at the same instants is exact arithmetic over the session log's start and end
stamps, and an item's recorded open minutes are already defined by those stamps. One number taken anyway,
because it is one line: the one-group-by route (each type's recorded minutes over that type's mean
concurrency) reaches the truth **20 of 20 at corr +1.0000**, and the solo-handled subset publishes the
truth exactly, 20 of 20.

**M3, the share of a queue's inbound volume its own outbound caused (service operations, the outbound
dispatch log as the forcing file).** Failure demand, a real service-operations object. The naive routes are
emphatically wrong, inbound volume per day 1 of 20 and inbound per outbound item 0 of 20, and the designed
lag-1 regression is right 20 of 20. It dies twice. **The quiet-day route, one group-by over the days whose
previous day dispatched nothing, reaches the truth 20 of 20 at corr +0.9992**, and the dial has no middle:
swept over quiet-day shares of 0.02, 0.05, 0.10, 0.20, 0.35, 0.50 and 0.70 the quiet route scores
19, 20, 20, 20, 20, 20 and 20 of 20 at corr +0.9761 rising to +0.9998. And the family forks: the graded
share at the golden queue spreads **0.4429** across the three licensed lag structures (same-day, lag 1,
distributed lag 0 to 3) against a printed precision of 0.001, with the same-day form right only 8 of 20.
- **Law confirmed on commercial ground:** task201's rule that "estimate the nuisance where the signal
  vanishes" fails by construction is not specific to a null region in an instrument's range. A quiet
  period in an operations log is a null region, so any construction that separates a baseline from a
  response has its baseline published by the days the response is absent, and an operations record always
  has those days.

**What the three deaths say about the cell, for whoever draws it next.** Business operations is adverse to
a silent decisive rung for a structural reason, and it is the mirror of the mandated-indicator law rather
than an instance of it. There is no statutory quality framework, so screen 12 does not fire; but the
organisation documents its own metrics, and the files realism requires the pack to carry (the metric or KPI
dictionary, the costing policy, the service standard, the maker's maintenance schedule) are exactly the
files that name the operational quantities the field decides on. Rule 1 pushes the deciding quantity
towards something the field estimates, and readability test 1 pushes it away from anything a filed sentence
names, and on this ground those two pull in opposite directions. The quantities with no entry in anybody's
dictionary turned out, three times running, to be the ones that are not operations quantities at all.
