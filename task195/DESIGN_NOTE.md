# task195 design note

Whether the genomics core laboratory's contamination screen changes for the quarter from 1 July 2027, and at
which of the validation protocol's listed cutoffs, decided on a parallel run in which both screens were read
on the same specimens.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task195.json`, filed and registered (WARN only) |
| Domain, task type | biomedical-clinical-research, `genomics-gwas-high-dimensional-association` (serves AD) |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 04, setting one dial: each allowed cutoff carries four figures |
| Decision | `dial_setting`, `named_option`: one of five listed cutoffs, or the change is held |
| Gate G | `method_or_model_selection`; decisive generator G16, supporting G17 |
| Strategy | `other` (the uncertainty of a paired difference against two marginal intervals) |
| Layer 2 | `field_method`, own pattern `own:paired-difference-against-marginal-intervals` |
| World | Norway, Genomkjernen, the genomics core of Nordfjell forskningsinstitutt |
| As-of date | 2027-06-21 (the validation extract); the quality review sits 2027-06-30 |
| Spine | `qc_screen_history_2026-02-15_2027-02-28.csv`, one row per release record of a specimen's quality-control screen |
| People | Laila Johannessen (screening lead), Dag Rasmussen (quality manager), both from `guard.py names --geo Norway --seed 195` |

**Data-native sentence.** Both screens were computed from the same archived read sets of the same specimens,
one library preparation each, so the two calls share every specimen's own marker noise and disagree on only
30 of the 393 confirmed events at the deciding cutoff, agreeing on 5,678 of the 5,839 specimens: the
increase is pinned far tighter than either
screen's own detection rate, and the laboratory's own records are what make the two rates' intervals the
wrong instrument here.

**Guard WARNs, answered.**
- `overuse.objective` (anomaly detection in 6 of the last 12): the lane's wave sits on this objective; what
  rotates is the mechanism (G16 decisive here, not G17 or G10), the Layer 2 family (`field_method`, unspent
  in the window) and the gap's expression.
- `repeat.gate_g` against task190 and task194: the label coincides, the driver does not. task190 selects
  between counting confirmed cases and nowcasting a stock under reporting delay; task194 selects between a
  level comparison and a return-to-mean counterfactual; task195 selects between two estimators of the
  uncertainty of one filed difference, both of which read the same rows. Measured driver similarity to both
  is 0.05. The draw was moved off `signal_vs_noise_or_hold` on purpose, so this batch does not read as the
  same strategy three times (task191, task193 carry it).
- `repeat.question_form` against task191: the call is a gate with a dial, so the prompt asks whether the
  screen in service is replaced and, if it is, at which listed cutoff. The alternative label, `which`,
  repeats task190 instead; either way the form follows the decision rather than the batch.
- `ban.org_family` (university_or_school against task233) appeared at the duplicate check once task233 was
  filed: the world moved from a university laboratory to the genomics core of a research institute, which is
  where Norwegian cohort genotyping services sit anyway. Nothing else about the build moved.
- `test.same_driver_older` against task228's lineage: differentiated on the card. task228 builds one rate's
  variance at the unit that was randomised, where the naive test understates it and the repair widens the
  interval against a false-alarm cap on a labelled corpus. Here the naive test overstates the uncertainty of
  a difference measured twice on the same material and the repair narrows it, with no corpus, no cap and no
  clustering in play (the plate-clustered variant is asserted to leave the call where it is).

**Sources read.** `analytical_tasks/02_anomaly_detection/AD18` header and Situation only (the world, the
decision and the quantity; the seed's own architecture, a parallel run that spoke about another season, is a
transportability argument already spent on this objective and is not used). `guard.py mechanisms --objective
anomaly-detection`, every spent driver read before the draw: 28 builds, none estimating the uncertainty of a
paired comparison; the nearest in family are task186 (an empirical null for shared local cycles) and task191
(the null of a selected maximum), both of which judge one series against a reference distribution, which this
build does not do. `layer2-rigor-patterns.md` biomedical patterns teach partial verification and in-sample
cutoffs; this build takes neither (verification is complete for the filed population and the cutoff set is
closed by the protocol).

## Default path

1. Read the two quality-control exports (`qc_screen_calls_gsqa_*.csv`, `qc_screen_calls_gsqb_*.csv`), keep
   the accepted reads, and join the re-run estimates (`mixture_fraction_rerun_v34.csv`) and the panel
   verdicts (`identity_panel_register_2027.csv`) on `specimen_id`.
2. Apply KVAL-07 3.1 and 3.2: in-scope project codes, an accepted read, an accepted read set with an
   estimate, a verdict of MIXED or CONCORDANT reported on or before 21 June 2027. The comparison holds 5,839
   specimens, 393 of them confirmed contamination events.
3. Count detections: the screen in service flags 292 of the 393; the candidate screen flags 294, 308, 310,
   319 and 326 at the cutoffs 0.050, 0.030, 0.020, 0.015 and 0.010.
4. Count false calls on the 5,446 CONCORDANT specimens: 91 for the screen in service, 61, 74, 80, 85 and 104
   for the candidate screen, so only the 0.010 cutoff breaches KVAL-07 4.1(b).
5. Establish the increase the way the protocol's 4.1(a) asks: compute each screen's detection rate with a 95
   per cent interval (74.30 per cent for the screen in service, 74.81 to 82.95 per cent across the cutoffs)
   and read the intervals against each other. Every interval at a compliant cutoff overlaps the screen in
   service's (Wilson 69.76 to 78.37 against 74.04 to 82.16 at 0.030), so no compliant cutoff shows an
   increase that the parallel run establishes.
6. Apply 4.1: no listed cutoff meets both conditions, so the change is not made and the parallel run
   continues into the next quarter.

**Ends on:** hold the change and continue the parallel run.
**Golden:** replace the screen in service at the 0.030 cutoff from 1 July 2027.

## Stump sentence

A competent solver reconciles the parallel run correctly, computes each screen's detection rate on the 393
confirmed events with its own 95 per cent interval, finds the interval at every compliant cutoff overlapping
the screen in service's, reads 4.1(a) as unmet and holds the change and continues the parallel run, where the
same specimens establish the 0.030 cutoff's increase of 16 specimens (4.07 percentage points) with a 95 per
cent interval of 1.37 to 6.77 points, clear of zero, and the change is made.

## Three rules

- **Task type:** genomics-gwas-high-dimensional-association, the anomaly-detection flavour: a sample-level
  anomaly (cross-contamination) called from a high-dimensional marker signal, and the laboratory's choice
  between two callers read over the same archived read sets.
- **Domain test:** the deciding quantity is the increase in confirmed contamination events detected when the
  same archived read sets are re-called by a second screen, which a laboratory validation estimates on the
  discordant specimens because one library preparation and one set of reads carry both calls. A generalist
  estimates each screen's own detection rate and compares the two intervals.
- **Swap:** "the inspection line's two rigs each catch more of the units they inspect" reads as a comparison of
  two separate measurement events on different material, where nothing pairs the readings and each rig's own
  marginal rate is all the evidence there is; the paired estimator then has nothing to pair, and the whole
  difficulty disappears. It survives only where one specimen's own data is re-analysed twice.
- **Layer 1:** two quality-control exports from two sequencers in the laboratory's semicolon-and-decimal-comma
  idiom beside a comma-and-dot pipeline export; voided reads from batches whose instrument control failed,
  carried with empty call fields; specimens with a second read set from a depth top-up; specimen identifiers
  that differ between the laboratory, the biobank's request register and the partner laboratory's reports;
  per-batch instrument control thresholds in the run log; tables inside the partner laboratory's weekly PDF
  reports and the protocol. Each is what these systems write; none is placed to be caught, and each is
  asserted neutral for the call.
- **Layer 2:** `field_method`, the field's own method done right: the uncertainty of a difference between two
  screens read on the same specimens is the uncertainty of the paired difference, carried by the discordant
  specimens, not the overlap or the two-sample combination of each screen's own interval.
- **Decisive step:** estimate the increase's uncertainty from the specimens the two screens disagree on, because
  both calls come from the same read sets, instead of from each screen's own detection rate.
- **Not semantics:** every field, code, unit and definition can be read correctly, the population reconciled to
  the specimen and the counts 292, 294, 308, 310, 319, 326, 91, 61, 74, 80, 85, 104 all recovered exactly, and
  the easy route still holds the change: the point estimate of the increase is identical under both
  estimators, and only its standard error differs (0.0138 against 0.0303 at 0.030).
- **Not rule application:** KVAL-07 4.1(a) names the quantity (the increase and a 95 per cent interval above
  zero) and never names an estimator for it; no filed sentence, column, dictionary entry or document performs
  the step, so a solver who executes every stated rule still has to choose how the interval is built.
- **Analyst test:** the easy route holds the change and continues the parallel run: it reads 4.1(a) by giving
  each screen's detection rate its own 95 per cent interval and finds them overlapping at every compliant
  cutoff. Executed in `generator/checks.py` on the clean truth (R3a) with every filed rule applied.
- **Estimand:** KVAL-07 3.1 to 3.5 file it: the population (specimens received on or after 1 March and on or
  before 31 May 2027 under the cohort service's own project codes, with an accepted read, an accepted read
  set with an estimate, and a verdict of MIXED or CONCORDANT reported on or before 21 June 2027), the outcome
  (a flag on a specimen whose verdict is MIXED), the window (the parallel run), the unit (one specimen) and
  the comparison (each listed cutoff of the candidate screen against the screen in service on those
  specimens). The decisive step settles none of these five: both estimators read the same rows at the same
  grain and return the same point estimate.
- **No decoy:** nothing is planted. No block is copied or backfilled, no rule is withheld, no memo, draft or
  stakeholder figure argues a cutoff or the hold, and no shipped document ranks the cutoffs. Every figure in
  the pack is correct, and deleting every document leaves the task as hard.
- **No certified replay:** there is no closed corpus of past determinations and no published figure to
  reproduce. The parallel run is the evidence the protocol names, not a corpus that selects a method, and the
  model card reports the estimator's output distribution only.
- **Lesson:** when two methods are read on the same units, the evidence about their difference is the
  disagreement between them, and judging the difference by the overlap of two separately computed intervals
  throws away the design that was paid for. No build on file teaches it: the corpus holds reference
  distributions for selected extremes (task191), empirical nulls for shared cycles (task186) and variance at
  the clustering unit (task228), all of which widen an interval; this one narrows it, and the narrowing is
  what the design entitles.

## The WHAT screen (`stumping` 1.2)

The decisive step is "estimate the increase's uncertainty from the specimens the two screens disagree on".
Which part of the estimand does it settle? None, and here is the filed sentence for each part.

| Estimand part | Filed by | Does the decisive step settle it? |
|---|---|---|
| Population | KVAL-07 3.1 ("received on or after 1 March 2027 and on or before 31 May 2027 under a cohort service project code"; contract receipts out of scope) and 3.2 (accepted read, accepted read set with an estimate, verdict MIXED or CONCORDANT reported on or before 21 June 2027) | No. Both estimators run on the same 5,839 specimens and the same 393 events; `checks.py` asserts the row and entity counts are identical on both routes. |
| Outcome | KVAL-07 3.3 ("a confirmed contamination event is a specimen whose verdict is MIXED") and 3.4 ("a screen detects a confirmed contamination event when it flags that specimen") | No. The flag and the verdict are read the same way on both routes; the detection counts 292 and 294 to 326 are identical. |
| Window | KVAL-07 3.1, the receipt window, with 3.2's verdict as-of date | No. Neither estimator moves a date. |
| Unit | KVAL-07 3.4 ("detection is counted per specimen") | No. Both estimators are at specimen grain; the paired route adds no unit, it uses the one already filed. |
| Comparison | KVAL-07 4.1 ("over the screen in service", each listed cutoff of Table 2) | No. The comparison set and the comparator are the same on both routes, and the point estimate of the increase is identical (16 specimens at 0.030 either way). |

So the estimand is beyond argument and two estimators of its uncertainty still stand: the marginal route
(each screen's own interval, or the two-sample difference) and the paired route (the discordant specimens).
The data's own structure rules the marginal one out, because the two calls are computed from one specimen's
own read sets and agree on 5,678 of the 5,839 specimens. That is the shape the screen asks for: not a part of the
estimand, but a choice of estimator for one filed quantity, with the records separating the candidates.
Three builds in this wave died on the other side of the screen (task190 settled whether members not yet
observed are in the population, task192 the unit of the count, task193 the comparison population); this one
settles no part of it.

## Survivor anatomy

Actor: the deciding property, each confirmed event's discordance between the two screens (flagged by one and cleared
by the other on the same specimen), has no column: each export carries one screen's call, and the pairing exists only
across files on the same specimen.

Link: the signal is read by setting the screen in service's call beside the candidate's flag on the same specimen and
counting the specimens the two disagree on, a paired comparison the two-interval reading never asks for; no sentence
invites it.

Reflex: the field's reflex for an increase with a 95 per cent interval, each screen's own detection rate with its own
Wilson interval read for overlap, is the default path and holds the change.

Back-test: not applicable: a parallel-run validation has no history to test on; the textbook route's own figures (each
screen's rate and its interval) recompute exactly, so nothing in the pack contradicts it.

Second use: every file the decisive step reads sits in the pack for its own reason: the two quality-control exports,
the re-run estimates and the panel register are the parallel run's own records, which the protocol's detection and
false-call counts need whatever the comparison.

Shock: the movement the step recovers is ordinary: the increase (16 specimens, 4.07 points at 0.030) is the same count
the default path computes; only its interval changes, so no specimen or cutoff stands out.

Pins: KVAL-07 4.1 files the WHAT (an increase in detected events that the parallel run establishes at 95 per cent, false
calls within the bound); no filed sentence names pairing, discordant specimens or a paired test.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 sign and ceiling only, answer 0.050 | 4.1 states both conditions, so the sign read is incomplete on its face | the counts are a group-by | the opponent's reflex is to interval the figure | nothing scores it | battery silent | one subtraction | readable |
| 1 each screen's own interval, answer hold | 4.1(a) says "established with a 95 per cent interval above zero" and nothing more | two rate columns a solver builds | comparing two intervals is the first reflex | nothing scores it | battery silent | two Wilson intervals | readable |
| 2 two-sample difference interval, answer 0.015 | no sentence names a standard error | nothing in the schema | the textbook correction a careful solver reaches for | nothing scores it | battery silent | one formula | readable |
| 3 (decisive) the paired difference on the discordant specimens, answer 0.030 | no filed sentence names the pairing, the discordance, the estimator or the design; 4.1(a) names the quantity only | no column, key or marker holds concordance, discordance or a pair id; the pairing is a property of the join the population sentence already forces | not an opponent default: 79 rounds show the battery, the event study and the interval reflex, never a within-unit variance | no control, corpus or published figure confirms it, and none ties only under it | key uniqueness, duplicates, fan-out and count ties all pass on both routes | not a subtraction, a ratio or half a reported figure: it changes a standard error from 0.0303 to 0.0138 | silent |

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the comparison's specimens | KVAL-07 3.1 and 3.2, 5,839 specimens | the scope clause dropped, so contract receipts are in | `same call` | 3.1 states the scope, and the re-run's archive path holds the cohort service projects only, so no contract receipt carries an estimate and no reading of 3.1 can add one (asserted, C1) |
| SF2 | confirmed contamination event | verdict MIXED, 393 specimens | MIXED or INCONCLUSIVE | 0.030 | 3.3 names MIXED; 3.2 keeps INCONCLUSIVE out of the population; `same call` asserted |
| SF3 | detection | a flag on the specimen, counted once per specimen | counted per read or per read set | 0.030 | 3.4 "counted per specimen"; one accepted read and one accepted read set per specimen asserted; `same call` |
| SF4 | "established with a 95 per cent interval above zero" | the two-sided 95 per cent interval excludes zero | a one-sided 95 per cent lower bound above zero | 0.030 | convergence: the qualifying set is identical under both readings at every cutoff (asserted, C1) |
| SF5 | false-call rate | flags among the comparison's CONCORDANT specimens, 5,446 | flags among all 5,839 comparison specimens | 0.030 | 3.5 names the CONCORDANT specimens; `same call` asserted on both denominators |
| SF6 | "the highest cutoff value listed in Table 2" | the largest mixture-fraction value, 0.050 first | the cutoff flagging most specimens, so the list is walked the other way | 0.015 | 4.1 says "the highest cutoff value listed in Table 2" and Table 2 lists values, not flag counts; `checks.py` asserts both the ordering and the other walk's answer |
| SF7 | a flag at a cutoff | estimate at or above the cutoff | estimate strictly above the cutoff | 0.030 | 3.4 "at or above"; no estimate equals a listed cutoff (asserted, C1) |
| SF8 | the screen in service's call | the flag the quality-control export records, reviewed calls included | the flag re-derived from the het-excess value and the control threshold the run log records | `same call` | 3.4 "when the quality-control export records the flag"; the two converge inside the comparison, 292 detections and 91 false calls either way, because the 15 calls the laboratory overturned at review sit on receipts the comparison does not hold, asserted |
| SF9 | the window | receipt date on or after 1 March and on or before 31 May 2027 | a processing or release date | `same call` | 3.1 names the receipt date, and the quality-control export carries no other date for a specimen, so the readings converge on the same rows (asserted) |
| SF10 | the increase | the difference between the two detection counts on the filed population | the ratio of the two detection rates | 0.030 | 4.1(a) says "the increase in confirmed contamination events detected"; `same call` asserted on the paired log-ratio interval |
| SF11 | accepted read | `read_accepted` is Y in the quality-control export | the latest read whatever its status | 0.030 | 3.2 "an accepted read"; the export's own `read_accepted` column carries Y or N and a voided read carries no call, so no reading can count one; `same call` asserted |
| SF12 | the estimate for a specimen with two read sets | the accepted read set's estimate | the later read set, or the mean of the two | 0.030 | 3.4's accepted read set; both alternatives asserted to leave every cutoff's counts unchanged |
| SF13 | rounding path | from unrounded counts, percentage points to two decimals | rounding each rate first | 0.030 | the prompt's last sentence; every graded figure's distance to its bin edge asserted at 0.0036 points or more |
| SF14 | the interval's population | the comparison's own specimens | the comparison's specimens weighted for the specimens whose verdict was still pending | 0.030 | 3.2 excludes pending verdicts; the pending set's flag distribution and the verification-weighted answer are asserted to leave the call where it is |

## Ladder

Four rungs, four answers, each a complete pipeline that reproduces from the bundle. Measured by
`generator/checks.py` on the cut pack; every figure below is a measurement, not an intention.

| Rung | The analysis | Answer | Dies to |
|---|---|---|---|
| 0 | detections, the sign of the increase and 4.1(b) only | 0.050 (increase +2 specimens, 0.51 points, false calls 1.12 per cent) | 4.1(a): the increase at 0.050 is established by no estimator (paired z 0.392, exact McNemar p 0.845) |
| 1 | each screen's own detection rate with its own 95 per cent interval, read for overlap | hold the change | the overlap of two intervals is not the interval of their difference; the same specimens carry both calls |
| 2 | the increase with a two-sample (independent proportions) interval | 0.015 (increase +27, 6.87 points, z 2.323) | the two screens are not two samples: 5,678 of 5,839 specimens are called the same way by both at the deciding cutoff |
| 3 (decisive) | the increase with the interval carried by the specimens the screens call differently | **0.030** (increase +16, 4.07 points, paired z 2.953, interval 1.37 to 6.77 points) | nothing in the pack; this is the golden |

**Arithmetic, measured.**
- Position: on rung 0 the golden cutoff is the second row of Table 2, never named on rungs 1 or 2; the golden
  is named by no rung below 3.
- Decisive margin: paired z 2.953 against the 1.96 bar, 50.7 per cent clear; the same figure on the
  two-sample route is 1.344, 31.4 per cent short. Ratio of the two standard errors 2.197x.
- Robustness of the golden (every variant asserted): paired Wald, continuity-corrected McNemar chi-square
  (7.500), exact McNemar (p 0.00522), the one-sided reading, a Bonferroni bar over the five cutoffs (2.576,
  cleared by 14.6 per cent), the paired log-ratio interval, a plate-clustered paired interval, the
  all-specimens false-call denominator and verification weighting for the pending verdicts all name 0.030.
- Robustness of each wrong rung: the two-sample route names 0.015 under the two-sided and the one-sided
  reading and under Wilson-based (Newcombe) intervals; with a Bonferroni bar it names the hold, which is
  rung 1's answer, so no variant of a wrong rung reaches 0.030.
- Separation: the four answers are 0.050, hold, 0.015 and 0.030; no two rungs share one.
- Dominance: at 0.030 the paired route clears the bar by 0.993 z units while the nearest wrong cutoff
  (0.020, which also qualifies on the paired route) is excluded by 4.1's "highest cutoff" clause, not by a
  margin; the cutoff above it (0.050) fails 4.1(a) by 1.568 z units on every estimator.
- The grid: estimator (marginal overlap, two-sample, paired) x interval reading (two-sided, one-sided) x
  false-call denominator (CONCORDANT, all) x verdict scope (MIXED, MIXED or INCONCLUSIVE) is computed cell by
  cell in `checks.py`; every cell is 0.050, hold, 0.015 or 0.030, and every cell that is not the golden
  violates a quoted sentence of KVAL-07 or uses an estimator the pairing rules out.
- One live degree of freedom? No: the cutoff set is closed at five listed values and the graded quantity is
  a count difference, so there is no parameter to tune.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which specimens are in the comparison | KVAL-07 3.1 and 3.2 file it literally; 5,839 specimens asserted, and the pending and inconclusive sets named as excluded |
| 2 | Unit of account | specimen, read, read set, aliquot | 3.4 "counted per specimen"; one accepted read and one accepted read set per specimen asserted |
| 3 | Attribution window | which receipts fall in the run | 3.1 "on or after 1 March 2027 and on or before 31 May 2027"; receipt dates are whole days, no timestamp on the boundary |
| 4 | As-of dating | which verdicts count | 3.2's "reported on or before 21 June 2027"; the extract date is 21 June 2027 |
| 5 | Version basis | which pipeline version's estimate | 3.2 and the run config name v3.4; one estimate per accepted read set |
| 6 | Denominator | detection over what, false calls over what | 3.3 and 3.5; SF5 asserts the all-specimens denominator gives the same call |
| 7 | Weighting | specimens equal, or plates | 3.4 per specimen; a plate-clustered paired interval asserted to leave the call where it is |
| 8 | Window length | how much history | the parallel run is the filed window; no rolling rate on the call's path |
| 9 | Boundary inclusivity | at or above the cutoff | 3.4 "at or above"; no estimate equal to a listed cutoff (asserted) |
| 10 | Rounding path | once at the end or per line | the prompt's last sentence; every graded figure asserted at least 0.0036 points from its bin edge |
| 11 | Tie-break | two cutoffs equally placed | 4.1 takes the highest qualifying cutoff; the qualifying set is a contiguous run of Table 2 and no two cutoffs tie |
| 12 | Maturity and censoring | verdicts still pending | 3.2 excludes them; the pending set's flag rates and a verification-weighted answer asserted to leave the call where it is |
| 13 | Order of operations | which 4.1 condition first | both are filters on one closed cutoff set; the answer is asserted identical in either order |
| 14 | Row order | file order | every figure is a count over a set; asserted invariant under a permuted read of all three call files |
| 15 | Duplicate resolution | voided reads, second read sets, re-sent verdict rows | 3.2 and 3.4 file the accepted read and read set; one verdict per comparison specimen asserted; re-sent rows sit outside the comparison |
| 16 | Identity normalisation | specimen across three systems | the call joins `specimen_id`, which all three call files carry; the request crosswalk is not on the call's path; the join asserted one to one |
| 17 | Netting against gross | may misses offset extra detections | 4.1(a) is the net increase on one population, which is what the paired difference is; asserted equal to the difference of counts |
| 18 | Dimensional units | fraction or per cent | the re-run configuration's `output_scale` ("fraction of the specimen's reads") and the model card ("as a fraction") state it; per cent appears only as a label on the dilution panel's levels, a file the call does not read |
| 19 | Code and status semantics | verdict, read status, project and agreement codes | KVAL-07 3.1 to 3.5 name every code the call reads (a verdict of MIXED or CONCORDANT, a FLAG call, a cohort service project code, a contract agreement), the exports carry them under those names and the re-run configuration lists the project codes; never the stump |
| 20 | Integerisation | counts | whole specimens by construction; no allocation or apportionment |
| 21 | Clause scope | which cutoffs 4.1 applies to | 4.1 names Table 2's listed values; the set is closed at five |
| 22 | Forward window contents | what the committed quarter holds | the rule runs on the closed parallel run and commits the quarter from 1 July 2027; no forward driver file is needed, and the design note records the retrospective evidence with a forward commitment |

## Literal reader

Executed word for word, KVAL-07 3.1 to 3.5 select 5,839 specimens and 393 confirmed events, 4.1(b) removes
the 0.010 cutoff, and 4.1(a) leaves one thing open, how the 95 per cent interval on the increase is built;
every reading of every other term returns the same rows and the same counts (SF1 to SF14 asserted in
`checks.py` and again in `verify.py`), and of the estimators the data admits, the one the design entitles
returns 0.030 under the two-sided, one-sided, exact, continuity-corrected, log-ratio, Bonferroni and
plate-clustered variants alike.

## Oracles

| Control or published figure | What it confirms | On the wrong path |
|---|---|---|
| MG-2025-14, the 2025 extraction platform validation (PDF) | the 2026 method table's codes, and each method's median yield on the verification specimens | read beside the extract's names it contradicts them for every 2026 code, and the battery takes the name on the record; it states no figure the ask grades and arbitrates which method a code meant without handing over a count |
| `release_volumes_monthly_2026-03_2027-02.csv` | the release rows booked at each month's close, before the release desk's amendments | invariant under the device: the re-coding moves no release between months, so every reading of the methods ties to it alike |
| The model card's estimate distribution | the re-run's output distribution over the 2027 archive | reproduces identically on every route; carries no verdict, so it confirms nothing about detection |
| Nothing else | no file states a detection count, an increase, an interval, a cutoff recommendation or a figure per method | no oracle ties only under the golden |

## Ask sheet

One ask, 16 graded figures, on the screen in service's twelve reporting months before the parallel run, the
record KVAL-07 5.1 puts in the validation file; it is keyed to neither the call nor its construction, and none of
its rows is a comparison specimen. Rebuilt at the reship of 11-03: the identity-merge layer (the weekly reports'
specimens through the biobank's vial reference, the monthly baseline through the extraction id) went SEND_BACK at
judge pass 3, and no identity reconstruction or counting convention is drafted again (`## Tried and rejected`).
The per-cutoff table and the chart are the call's own construction and are scored with it.

| Ask | Figures | H18 home | Use | Silent primary | Path (files, columns) | Stops and lazy delta | Realism |
|---|---|---|---|---|---|---|---|
| A, the screen in service by extraction method | 4 methods x (specimens released in the twelve months to February 2027, those the duty bioinformatician reviewed, those the screen in service flagged with reviewed ones by their review outcome, flags per thousand released) = 16 | a measure the screen in service carries that the call does not turn on: KVAL-07 5.1's record of the screen in service over the twelve reporting months before the parallel run | the quality review reads where the screen in service's flags fall before the screen changes: a hand-held column and a low input carry a second contributor's DNA through more often | D2 with D7, a label at the wrong vintage on a code whose meaning changed. On 2 November 2026 the second extraction robot came into service with its low-input program, and the method group re-coded the LIMS method table so the codes follow the robots' program numbers: 1 the low-input program, 2 the standard magnetic bead, then the bench methods, 3 silica column and 4 salting out. An extraction keeps the code it was booked under, and the warehouse names every code by the table at the pull (the extract's footer: "Code descriptions are those of the LIMS reference tables at the pull"), so every extraction before the go-live carries a 2026 code (1 magnetic bead, 2 silica column, 3 salting out, as MG-2025-14 prints them) under the name of the method holding that code now. Nothing dates the re-coding; the first extraction booked under code 4 and every code's DNA concentration show it | `qc_screen_history_2026-02-15_2027-02-28.csv` (specimen_id, extracted_date, extraction_method_code, extraction_method, dna_ng_ul, call_source, hetx_call, review_outcome, release_status, released_date), `release_amendments_2027-04_2027-06.csv` (field, value_after), `extraction_platform_validation_2025.pdf` (the 2026 codes): 3 files, 13 columns | the names as the record gives them, amendments applied (the cracker): every figure off; the names without the amendments (the mirror): every figure off; the 2025 codes on every record: every figure off; the 2026 table on the 2026 records and the names on the 2027 ones: every figure off; the re-coding found but split on the receipt date: every released count off, 10 of 16 kept; the answer | a LIMS reference table re-coded in place when new equipment is set up, with a warehouse that joins old records to the table as it stands, is the commonest way a re-coded dimension mislabels history; low-input and hand-held extractions carrying more contamination through is what a genomics core sees |

**Forcing, asserted on the shipped rows.** Read by the names, every 2026 code's median DNA concentration jumps at 2
November 2026 (code 1 from 63.2 to 21.8 ng/ul, code 2 from 47.5 to 63.3, code 3 from 83.0 to 47.0, each 1.3 times
or more); read on the table in force when the DNA was extracted, each method's concentration moves by 1.1 per
cent or less across the go-live (the assertion's bar is 4). Before 2 November only codes 1 to 3 are booked, from it all four. Read the golden way,
magnetic bead is the largest method all year (15,852 of the 28,401 specimens released); read by the names, the
low-input program would hold 13,204 of them from March 2026, eight months before the robot that runs it arrived.

**The pin test, answered.** The asking sentence pins the method, the window (released in the twelve months to
February 2027), the count (each specimen once), the call of record (a reviewed specimen by its review outcome) and
the rate's unit (per thousand released); the extract's footer files what its description column is, and the
amendment log's footer files that the amended value stands. The device sits in which method a code meant on the day
the DNA was extracted, which no pin names and no filed sentence adjudicates; written fully defined (the method the
extraction was booked under, on the table in force that day), the device still bites, because nothing says when the
table changed or that it changed.

**Main population zero counts, asserted and counted in one place.** The warehouse extract's receipts end 28 February
2027, so it shares no specimen with the comparison; no amendment names a comparison specimen; the call reads none of
the ask's three files and the ask reads none of the call's. `qc_screen_calls_gsqa`, `qc_screen_calls_gsqb` and
`mixture_fraction_rerun_v34` are byte-identical to the 10-17 cut by sha256. Three files the call reads or cites
changed for realism only, at the 11-01 reader's word, each on rows or sentences the call never executes: the
register's request numbers on the 912 results for receipts before the run window (the biobank's counter skips),
KVAL-07 6.2's sentence on an export manifest the pack no longer ships, and the model card's addendum sentence.
`checks.py` regenerates each with the change undone and asserts the shipped bytes back exactly, and asserts the
register's comparison rows byte-identical; KVAL-07 3.1 to 3.5 and 4.1 are word for word as approved. Delete the
ask's files and the call is unchanged.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| the release desk's 383 amendments, raised after the extract was pulled; the log's footer files that the amended record carries value_after | A | left out, the flagged counts and rates move in every method (the mirror's row) |
| a correction released again under the same accession | A | each release row counted, every method's released count moves |
| withheld and superseded release rows | A | kept, every method's released count moves |
| the reviewer's outcome over the automatic call | A | the automatic call alone moves every method's flagged count |

**Referee.** MG-2025-14's own medians (yield 6.4, 4.9 and 8.1 ug for magnetic bead, silica column and salting out)
order the 2026 codes' concentrations read on the 2026 table, and order nothing read by the names; the report states
no count, rate or figure the ask grades. The reporting pack's monthly release counts tie under every reading.

| Ask | Cracker (lands the call, runs the hygiene battery, executes every filed rule) | Figures | Kept | Verdict |
|---|---|---|---|---|
| A, by extraction method | applies the release desk's amendments as the log's footer files them, takes a reviewed specimen by its review outcome, counts each specimen once (the correction released again repeats its accession), keeps the releases dated March 2026 to February 2027 and reads each record's method from the record; where MG-2025-14's codes contradict the record's name, the battery re-derives from the finer key, the name: magnetic bead 10,546 released and 18.8 per thousand against 15,852 and 13.0, the low-input program 13,204 against 1,758, silica column 3,527 against 6,802, salting out 1,124 against 3,989 | 16 | 0 of 16 | miss |
| A, the mirror (the best response off the call) | the same path without the amendments | 16 | 0 of 16 | miss |

Stress rows, printed by `ceiling.py` and not the gate: the 2025 codes on every record keeps 0 of 16; the 2026 table
on the 2026 records 0 of 16; the response that finds the re-coding but splits on the receipt date keeps 10 of 16
and misses every released count, by the extractions of the last receipts before the go-live; the full includer,
who reads each code on the table in force on the day its DNA was extracted, keeps 16 of 16, which with the call
landed and a second includer off the call puts the pair at 83.5. The layer stands on one primary, the residual
risk recorded here: the includer has to see that the extract names every code by today's table while the codes on
its older records were booked under another, a judgment the battery does not make.

Measured by: generator/ceiling.py on the cut pack (target.zip 18d896f6), standard library and pypdf only, no generator code.

Pair ceiling: 36.8 measured, with the chart's four criteria counted inside the ask weight (the cracker 38 + 7 + 55 x 4/20 = 56.0; the mirror 5 + 7 + 55 x 2/20 = 17.5); 28.5 on the sixteen ask figures alone.

Mirror leakage: 10.0 per cent of ask weight (the mirror's chart keeps its increases and its zero line).

Each primary is a key question no shipped sentence adjudicates (ban 1): the extract's footer files what the
description column is and never that a code changed meaning. No marker isolates the device rows (ban 2: every
record carries a code and a name, the instrument column's names are the benign twin under the same footer, and no
flag, status or comment marks a pre-go-live extraction). No oracle ties only under the golden (ban 3: MG-2025-14
states no graded figure; the reporting pack ties under every reading). The ask turns on nothing the call turns on
(ban 4).

## Pre-ship check

**Reship of 11-03, rubric scope, the call frozen: free gates, all green on the candidate cut
(target.zip sha256 18d896f6085e6f32).** `generator/checks.py` 212 assertions, the separation line, the
device's facts and forcing, every stop and hazard, and the undo proofs for the three call files that
changed among them; `generator/verify.py` 70 independent checks from the bundle and `figures.json` alone,
the per-method ask recomputed with its own parser and the 2026 codes read from the platform validation's
own table; two rebuilds byte-identical (target, golden, `figures.json`, `metadata.json`) and the zip cut
twice byte-identical by `generator/cut_zip.py`; input gates 17 files in 5 formats (csv, tsv, json, xlsx,
pdf), the warehouse extract at 32,644 rows, 6 distractors declared and named in no file
name; `figures_check.py` 107 figures, 0 absent; `precut.py` 61 checks, 0 FAIL, 0 WARN; `voice-check.py`
PASS at 814 characters; `leak.py --asof 2027-06-21` REVIEW on the same three lines as every earlier pass
(KVAL-07 carries 8 of the call's 10 distinctive words because it is the protocol the call executes and
names no cutoff, count or interval method; KVAL-07 and the model card share 10 and 5 of the stump
paragraph's terms because they are the laboratory's own documents on this assay and neither names the
paired reading), each ruled harmless; containers clean in `target/` and `golden/`; `freeze.py check
--mode rubric` PASS with `--allow` for the nine `panel_weeks` week-ending keys (`## Tried and rejected`);
`guard.py heart` WARN (repeat.gate_g against task233 v2, overuse.gate_g, repeat.deliverables against
task263, test.same_driver_older a NOTE differentiated against task228 and task478 v7), no BLOCK;
`guard.py surface` exit 0 with one promoted pair, task478 at 0.084 on the cards' gap, pattern and Gate G
mechanism, the frozen main call's driver and not the ask, flagged to the author and not relabelled;
`guard.py validate` 0 invalid.

**The 10/10 rules re-read against the built pack.** The decisive step is untouched and still analytical:
the call's three data files are byte-identical to the 10-17 cut and its clauses word for word, so the four
rungs answer 0.050, the hold, 0.015 and 0.030 exactly as before. The ask's device is Layer 1 of the
organisation's own making (a reference table re-coded in place, a warehouse naming old records by today's
table); it is an ask device, which rule 3 does not bind, and nothing in it is planted: every code is the one
in force on its extraction day and every name is the table's.

**Stage 4.** This session has no agent-spawning tool, so the two isolated reads are briefed for the parent
to run on the candidate cut: the leak reader (prompt and pack only) and the determinism judge (the system
prompt verbatim and the graded blocks). Their verdicts, and every finding fixed in one generator pass,
close this block before `RESHIPPED`.

**Earlier passes, kept as the record.**

**Free gates, all green on the final rebuild.** `generator/checks.py` 279 assertions; `generator/verify.py`
125 independent checks from the bundle and `figures.json` alone; two fresh rebuilds byte-identical to the
shipped `target/` (sha256 9357a0231529090d over all 19 files) and to `golden/`; input gates 19 files, 5
formats (csv, tsv, json, xlsx, pdf), a 32,647-row file, 4 distractors declared in `metadata.json` and named
in no file name; `figures_check.py` 111 figures, 0 absent; `precut.py` 49 checks, 0 FAIL, 0 WARN;
`freeze.py check --mode rubric` down to the two items the repair passes were ordered to move, filed below;
`leak.py --asof 2027-06-21` REVIEW, four lines, each answered: the protocol carries 8 of the call's 10
distinctive words because it is the protocol the call executes and it names no cutoff, no detection count
and no interval method; the protocol, the model card and the platform validation share 3 to 9 of the stump
paragraph's terms because they are the laboratory's own documents on this assay, and none names the paired
reading or the move; the container audit reports no writer signature, which is the clean result;
`guard.py surface` 0 promoted pairs; `guard.py heart` WARN, nearest 0.08 (task185's ledger row), no BLOCK;
containers audited clean by `scrub_producer_metadata.py` for both `target/` and `golden/`.

**The 10/10 rules re-read against the built pack, at ship.** The decisive step is still analytical: the
pack ships the two screens' per specimen calls and the panel's verdicts, and the increase's uncertainty is
the only thing no filed sentence settles. Four passes of repair have moved the ask layer twice and the
realism of every file once, and none of them touched it: the comparison is the same 5,839 specimens with
393 confirmed events, the screen in service flags the same 292 and 91, the four rungs answer 0.050, the
hold, 0.015 and 0.030, and every paired estimator still establishes the 0.030 increase while no unpaired
one does. Every mess item is Layer 1 and asserted neutral (R2); R3a files the hold on
the clean truth and R3b files 0.030 when only the estimator changes. Nothing is planted: no document
recommends a cutoff, states a detection count or argues a basis, and the difficulty survives deleting every
document, because the ladder lives in the records.

**The judge's gates, the author's own read before the isolated thread runs.** A: every write-up figure
recomputes, `verify.py` on its own code path. B: KVAL-07 3.1 to 3.5 and 4.1 ship the population, the
outcome, the unit, the comparison and the decision rule, and every distinctive term of the recommendation
is in the protocol. C: the estimand is filed and only the estimator of the increase's uncertainty stays
open, which the design closes, because both calls are computed from one specimen's own read sets and the
two screens agree on 5,678 of the 5,839 specimens; every paired variant returns 0.030, asserted. D: no term
on the main call reads two ways (SF1 to SF14, all asserted). E: the prompt pins the decision and no method,
and rounding sits once at the close. F: the default path ends on the hold, the obvious correction on 0.015
and the sign-only read on 0.050. G: no shipped number is wrong, so the difficulty survives deleting every
wrong number; the mechanism is method selection. H: the domain's own paired comparison decides, both layers
are present, and the decisive step is analytical.

**Stage 4, the determinism judge.** DETERMINISTIC, APPROVE, no fix. Gate G `statistical_rigor` /
`analytical_non_defect`, surface-read dependency no, sole data defect no. Gate H domain pass, layers pass,
decisive_step analytical. It built the paired Wald, Newcombe paired, exact conditional, specimen bootstrap,
plate-cluster bootstrap, continuity-corrected, one-sided and Bonferroni intervals and found every one of
them leaves 0.050 unestablished and 0.030 established, ruled the unpaired interval wrong rather than a rival
reading (the two screens' calls come from one specimen, joined on `specimen_id`, and correlate at phi 0.79),
and read "highest" as unambiguous. It expects solvers to build the unpaired interval and file 0.015 or the
hold. Verdict at `<scratch>/t195/judge/verdict.md`.

**Stage 4, the leak reader.** Nothing in the pack names the decisive step (it quoted KVAL-07 4.1 and noted
that no document says how the interval is built), no file ranks the cutoffs, and no figure reads as the
answer. It landed the call at 0.030 by taking the paired interval at once, because the data are paired, and
its unpaired reading gives 0.015. Its question 6 answered "mostly rule application, plus one analytical
choice", counting the population rebuild across four sources as the bulk of the work. Its two substantive
findings are answered in the fix pass below; its answers are at `<scratch>/t195/reader/reader_answers.md`.

**The first fix pass, with every graded figure frozen.** `generator/figures.json` came out byte-identical
to the version the judge approved (sha256 69a0d352fb63b1eb...), asserted by comparison, so the call, the
five cutoff rows and every ask figure stood where they were.

- The re-run's estimate and the identity panel's second-contributor share now measure the same mixture: the
  panel's share is drawn as a noisy function of the specimen's own estimate (a floor the targeted markers
  hold plus a proportional term, with lognormal measurement noise), so the two track at Pearson 0.89 and
  Spearman 0.92 against 0.04 before, asserted at 0.75 or better. No estimate moved, so no cell of any
  paired table moved.
- The register's turnaround clock, the population and every ask input are unchanged: the one draw the
  register used for its old request sequence is still taken, so every report date is the approved one.
- The laboratory is closed on Norwegian holidays, so nothing is received on them (14 days across the two
  windows), the receipt day's own size varies from 89 to 155, the control threshold is set per batch and
  held, accessions step irregularly, intake hours follow a working day, heterozygosity carries a plate
  effect and a right tail, the estimate has no floor spike, the panel's typing record varies and an
  INCONCLUSIVE result is one the panel could not type enough markers for, the register's request is the
  biobank's request, a request covers one specimen or a family group, the biobank reference is well formed,
  the dilution panel's casing is an operator's and each level was sequenced on its own.
- Three date-coherence defects closed: the weekly report file is pulled at the extract date and covers 5
  March to 18 June, no estimate is completed after the re-run's own pull date (the re-run ran in batches
  from 9 to 17 June), and the validation request in Annex A predates the protocol's issue.
- `rerun_pipeline_config_v34.json` has a user inside the fiction: the model card cites it for the run's
  scope, reference build, marker panel and depth floor.
- Three asking sentences pinned to the golden's own reading, no figure moved: any verdict counts for the
  weekly comparison and the reports are those issued in April and May; a reviewed specimen counts by its
  review outcome and the month is the release month; the dilution replicates are counted of the results
  reported.

**The second pass, the ask re-cut, with the call frozen.** The first pass closed the two readings the
pins opened and spent all three ask devices with them: the measured cracker sheet put the pair ceiling at
83.5 and mirror leakage at 100 per cent, which fails the bar. The three ask paths are re-cut on silent
primaries that live outside the call's row population, and the pins survive word for word.

- The call does not move, proved four ways. The four files the call reads
  (`qc_screen_calls_gsqa_2027-03_2027-05.csv`, `qc_screen_calls_gsqb_2027-03_2027-05.csv`,
  `mixture_fraction_rerun_v34.csv`, `method_validation_protocol_kval07.pdf`) are byte-identical to the
  judge-approved pack by sha256. The fifth file the call reads, `identity_panel_register_2027.csv`, is
  byte-identical on all 5,839 of the comparison's rows, and 0 of the 214 added rows touches a comparison
  specimen. `figures.json` moved on 43 keys, all of them under `panel_weeks` and `dilution`; the cutoff
  table, the increase, the interval, the false-call rates, the ladder's four rung values and A2's twelve
  monthly figures are unchanged. `freeze.py check --mode rubric` passes.
- A1's primary is the key. The register's `specimen_id` is an accession number: the laboratory
  re-accessions the biobank's second vial when a typing is borderline, so 214 specimens in April and May
  carry two accessions and the register holds both rows. The specimen's one identifier is `biobank_ref` in
  `specimen_request_crosswalk.tsv`, and nothing in the register points at it. The cracker's path misses all
  18 figures.
- A2's primary is the vintage. The warehouse extract was pulled before the release desk posted its
  corrections, so it holds the value before each of 367 amendments, which ship as their own log naming the
  column of record for each specimen. The reporting pack's release counts tie to the stale view, so the one
  control a careful solver reaches for confirms the wrong read. The cracker's path misses all 12 months by
  2.0 to 5.9 per thousand.
- A3's primary is the scope. The dilution workbook is the method group's standing panel workbook, so its
  prepared-levels sheet keeps the series of both stocks the group made up at the same three level names.
  The quarter's replicates all ran from NS-27-04; NS-27-07 is listed first and is 3.7 per cent lower. The
  cracker's path misses all three medians and coincides on the three within-a-fifth counts.
- Measured, not asserted: `generator/cracker.py` runs the cracker's path on the cut pack and scores it
  against the golden within half a unit of the stated rounding. 3 of 36 figures kept, pair ceiling 33.1,
  mirror leakage 8.3 per cent, all three assertions in `checks.py`. The three pinned asking sentences are
  unchanged word for word, with their figures, units and rounding.
- One coherence defect found and closed on the way: the amendment log's file name has to bracket the
  amendment dates it holds, so it is `release_amendments_2026-03_2027-05.csv` and `checks.py` asserts the
  bracket and that no amendment predates the release it corrects.

**The third pass, the judge's FIX_NOW on the two asks, with the call frozen.** The stage-4 judge
returned NOT_DETERMINISTIC, FIX_NOW, `competing_defensible_answer`, on supplementary answers 3 and 4 and
not on the main call: it recorded every paired estimator at 0.030 (lower bounds 1.36 to 1.53 across Wald,
Newcombe, Tango, paired bootstrap and exact McNemar), every unpaired one at 0.015, independence of the two
screens' calls rejected at chi-square 248 on one degree of freedom, 30 discordant specimens against 142
expected, the unpaired variance 2.2 times the real one, Gate G `statistical_rigor` / `analytical_non_defect`
and Gate H passing with the decisive step analytical. The repair is in the asking sentences, not in the
pack's documents.

- **The ambiguity was never the device; the work is.** The judge's first two fixes would have pinned the
  "specimen" identity and the monthly-rate basis in `validation_extract_dictionary.csv`, which is what A1's
  and A2's devices ride on. Declined. Each ask's own sentence now names its observables, which `supplemental
  stumping` Part 5 licenses, and the work is untouched: a solver still has to find that the register's
  identifier is an accession and that the vial's reference lives in a file the register never names, and
  still has to notice that the extract predates the corrections while the reporting pack ties to the stale
  view.
- **Ask 3 now asks for its two observables by name:** per weekly report issued in April or May, the
  distinct vials its results came from and the excess of results issued over them, with the sign of the gap
  in the sentence. The golden stays on the vial basis. Two further holes closed with it: the dictionary said
  the accession was "one per specimen received", which was simply false, and now says it is assigned when a
  vial is booked in; and the biobank's register now carries a row for every one of the 7,838 accessions the
  panel register holds (7,987 rows), so the vial is never guessed from the accession and `golden.py` asserts
  the coverage instead of falling back. The second sentence of the old `biobank_ref` entry, which told the
  reader that accessions duplicate, is gone: that was a marker, and the asking sentence does the work it was
  doing.
- **Ask 4 now names its population and its unit:** flagged specimens per thousand specimens released in the
  month, each counted once. That settles the numerator and denominator grain, the 1,449 specimens sitting on
  two released rows, and whether an automatic call or a review outcome governs. It says nothing about
  corrections existing or a log being applied. The reporting pack gains one line of its own as-of, "counts
  are the results booked as released at the close of each month", which states the vintage and adjudicates
  nothing: the solver still has to find the amendment log, notice it postdates the booking and decide to
  apply it.
- **The declined third fix.** The judge also suggested filing in the dictionary or protocol that detection
  and false-call are per-specimen indicators on the same specimens. Not added. Its own probe 1 shows the
  pairing already closes through KVAL-07 3.1, 3.2 and 3.4, so the sentence buys no determinism, and it would
  make the pairing more obvious on a build whose Gate F is moderate. KVAL-07 3.4 is exactly as it was.
- **Two figure problems closed.** The write-up stated the paired Wald endpoints, 1.37 to 6.77, where the
  paired estimators run 1.36 to 1.53 and 6.77 to 7.08; block 1, step 5 and the workbook's decision sheet now
  state only what every paired estimator agrees on, that the interval is clear of zero, and 4.1(a) asks for
  nothing more. And L1's within-a-fifth count sat on the line, one replicate 19.51 per cent from its
  prepared level against a 20 per cent test; the generator now steps each level until every replicate is at
  least 2 points of the level clear of that line, measured at 2.93, 3.44 and 2.58 points, asserted. L1's
  count moved 6 to 7 with the clearance.
- **Four realism tells closed.** The accession counter is shared with the laboratory's other work, so no
  stride dominates (the commonest is 26 per cent of 7,986 gaps across 8 or more distinct strides, against
  55 per cent at exactly 4); GSQ-A is the older sequencer and carries the higher het-excess background, so
  the two instruments flag at 7.28 and 4.30 per cent rather than 5.75 and 5.76; and the booking clock
  records the second and bunches its minutes after a courier drop (commonest minute 3.2 per cent against a
  flat 1.7). The constant `extract_date` is right for a single pull and was left alone. The reader's fifth
  item, the volume file tying to the history's row counts while the amendments move months, is A2's device
  working as designed and was left alone.
- **Three files no longer read as built for the analyst.** The dictionary carries an owner and a review
  date per entry and its own issue history; the manifest carries a licence beside the source and the pull
  date for all 19 files, with a compiler and an approver; and the model card is version 3.4.1 issued
  2027-05-14, before the re-run's first batch completed, with its archive distribution in an addendum of
  19 June, after the last batch, a revision history of four versions, and no sentence disclaiming the
  distribution it reports.
- **What the call side did, exactly.** No call figure moved: `figures.json` differs from the judge-approved
  set on 45 keys, 27 under `panel_weeks` and 18 under `dilution`, and on nothing else. The cutoff table, the
  increase, the false-call rates, the ladder's four rung values and A2's twelve monthly figures are
  identical. The specimen identifiers in the call's own files did change, because the stride-4 pattern was a
  realism defect in the identifier generator and nothing else; roles are assigned by index, so every count,
  every rung and the answer are untouched, which `checks.py` and `verify.py` both re-establish from the
  rebuilt pack.
- **The cracker sheet, re-measured on the new pack**, not carried forward: A1 keeps 0 of 18, A2 0 of 12,
  A3 3 of 6, so 3 of 36, pair ceiling 33.1 and mirror leakage 8.3 per cent. The three ask devices survived
  the re-wording, which is the test that mattered.

**The fourth pass, realism on an approved build, with the call frozen.** The second judge pass returned
DETERMINISTIC, APPROVE, no fix and no rerun: every figure in blocks 1 to 4 reproduced from the bundle,
Gate G `method_selection` / `statistical_method_choice` with no surface-read dependency and no sole data
defect, Gate H passing with the decisive step analytical, and all four asks forced. Ask 3's re-wording
closed through the weekly report's own footer on re-sent results, and ask 4 through the dictionary's
value-after-amendment entry and the manifest's amendments line. This pass is realism in the data, one
date correction and one write-up qualifier; no graded figure of the call moved and `figures.json` differs
from the judge-approved set on 45 keys, 27 under `panel_weeks` and 18 under `dilution`, and nothing else.

- **Three date anachronisms closed, and the pattern is now a gate.** The warehouse extract is pulled
  2027-04-09, after the last release it carries (2027-03-31), and every one of its 390 amendments is
  raised on the spring reconciliation that followed, 2027-04-12 to 2027-06-11, so the extract cannot hold
  a value the log postdates. The protocol is issue 4 approved 2027-02-19 and its revision table states
  that the issue pre-specifies the run's window, its data cut and the decision rule and is approved
  before a run opens, so no clause describes an event that had not happened. The dictionary is issue 5 of
  2027-06-18 with an issue history behind it, and no entry is reviewed before the data it describes
  begins. `checks.py` now runs the general check after the metadata is written: every delimited file's
  latest date is at or before its own pull date in the manifest, the extract's pull follows its last
  release, every amendment follows the pull, and every dictionary entry follows its data's start.
- **The protocol is no longer an extract.** The line saying sections 1, 2, 6 and 7 were "not reproduced
  in this extract" is gone and those sections are in the document: purpose and scope with the two files
  it does not cover, responsibilities with the separation of the run from the decision, deviations and
  records with the fifteen-year retention and the manifest requirement, and references with the four-issue
  revision table. The clauses the call executes, 3.1 to 3.5 and 4.1, are byte-identical.
- **Six measurement shapes, none of which touches a call.** DNA input is an extraction yield, right
  skewed, quartiles 43.1, 62.1 and 88.4 against a flat 54, 96 and 140; the depth a run reaches follows the
  input it was given with a left tail, quartiles 40.1, 47.0 and 53.7, and the read sets the pipeline
  could not estimate on now sit below the depth floor, from 5.4, which is why they have no estimate; the
  typed-marker count thins out, 4,236 panels at the full 96 then 1,582, 878, 489, 270, 154, 90, 61 and 14,
  against four near-equal bins; the read-set counter steps irregularly, commonest stride 25 per cent of
  6,105 gaps across 7 strides, as does the dilution workbook's; and the warehouse extract's depth is a
  measurement rather than a flat spread.
- **The dilution panel's lowest level no longer turns on a rounding step.** The judge measured L1's
  within-a-fifth count as the tightest margin in the pack: its nearest replicate sat 0.00012 from the
  one-fifth line, 1.2 steps of the stored four decimals. The cause was the level, not the draw: at a
  prepared level of 0.0041 a result stored to four decimals carries two significant figures, so the
  window the count tests is only sixteen steps wide and no believable recovery clears it. The panel's
  lowest level is now 0.8 per cent, prepared at 0.0081, which is where the estimator's stated limit of
  detection sits and therefore where a sensitivity panel belongs. Measured clearances, asserted per
  level: L1 0.00042 (4.2 stored steps), L2 0.00056 (5.6), L3 0.00162 (16.2). The flip condition is that
  number: one replicate would have to move by more than four stored steps for L1's count to change, where
  the stated rounding's half-unit is half a step. L1's count is the 7 the judge approved; its median
  recovery moves from 0.878 to 0.963 with the level, and the generator now also refuses a median recovery
  that lands on a round two-decimal value.
- **The empty guard band around the threshold is gone.** The screen in service's het-excess value now sits
  against the one control threshold the run log records for every batch, 36.60, with 28 values within 0.02
  of it and none inside: a 2-decimal measurement against a threshold, which is what the data should look
  like. The laboratory overturned 15 borderline calls at review, each of them on a receipt the comparison
  does not hold, so the override cannot move the screen in service's 292 detections or its 91 false calls,
  and both counts are re-asserted. SF8's closure is stronger for it: re-deriving the call from the run
  log's threshold reproduces every call inside the comparison, so the fork converges rather than merely
  landing the same way.
- **The reconciliations are no longer exact everywhere.** The nine weekly reports the validation file
  reports still tie to the register exactly, which is what ask 3's referee needs, and the volumes file
  still ties to the pre-amendment row counts, which is what A2's device needs. Three reports outside April
  and May do not tie, each stating why: results returned on receipt for re-typing and re-issued in a later
  week. The model card's addendum states that it was prepared on the read sets completed by 16 June while
  the file as filed carries the batches of 17 June, so recomputing from the file moves its figures a
  little, which is asserted rather than hidden.
- **One write-up qualifier, taken from the judge.** Block 1 now reads "which clear both tests on the
  paired interval", because 0.020 and 0.015 clear both tests in the paired family only; the unpaired 0.020
  fails at a lower bound of -1.33. No figure moved with it.
- **What `freeze.py` reports, and why.** Two items, both ordered. Final Recommendation loses exactly
  `1.37` and `6.77`, the paired Wald endpoints; Critical Components loses exactly `1`, `2`, `3`, `4`, the
  list markers that `freeze.py` now strips and this build's pre-fix snapshot still holds. Measured against
  the snapshot directly: zero main-call figures moved, and the stump, the card's driver, the prompt's call
  sentence, the ladder section and the default-path section are byte-identical.
- **The cracker sheet, re-measured again on the rebuilt pack**, because the realism changes touch the ask
  files: A1 keeps 0 of 18, A2 0 of 12, A3 3 of 6, so 3 of 36, pair ceiling 33.1, mirror leakage 8.3 per
  cent. Both clear the bar.

## Tried and rejected

- Seed AD18's own architecture (the parallel run was a statement about another season, so the switch is held
  on transportability): dropped at the draw, a spent argument on this objective and a Layer 1 answer.
- `gate_g: signal_vs_noise_or_hold` as drawn: re-drawn to `method_or_model_selection` at stage 2 because
  task191 and task193 carry it in the same batch and task191's decisive step also judges a figure against a
  reference distribution. The mechanism is honest either way; the batch cannot read as one strategy three
  times.
- A rule reading "the cutoff with the greatest increase among the qualifying cutoffs": dropped, because the
  qualifying set under the two-sample route and under the paired route then share their loosest member and
  both routes answer 0.015, which spends the stump.
- A rule with 0.050 at a negative increase: dropped, because then the sign-only route also holds the change
  and rung 0 duplicates rung 1's answer; a small positive increase at 0.050 gives rung 0 its own answer and
  punishes the route that skips 4.1(a) altogether.
- A bridge from the run log's receipts to the comparison as an ask: dropped under
  `supplemental-stumping` ban 4, it is the ladder's population walk and the cracker holds it by landing the
  call.
- A prior-year method comparison PDF as a distractor: dropped, it would teach the paired reading by example.
- A bridge from the identity panel's weekly reports to the comparison's population as a fourth ask: dropped
  with the receipts bridge, same reason, and the three remaining asks carried 42 graded figures between them
  at the time, 36 after the re-cut.
- `world.org_family: university_or_school`: dropped at the duplicate check when task233 was filed against
  it; the laboratory became a research institute's genomics core, which moved no figure and no rung.
- Permuting the re-run's estimates within strata of the screen in service's call, to make them track the
  panel's share: not needed, because deriving the panel's share from the estimate gives the same tracking
  and cannot move a cell at all; `figures.json` came out byte-identical either way the check was run.
- Redrawing the low band of the estimate to kill its floor spike was done inside the band, one draw for
  one draw, so no specimen crossed a cutoff and the register's turnaround clock did not move.
- A fourth ask, to dilute the weight of the two asks the pins opened: dropped, the prompt is at 997 of
  1,000 characters and a fourth ask would have to take figures from the three the judge approved.
- The paper cracker sheet (three asks missed, pair ceiling 35.1): contradicted by the stage-4 reader, which
  reached all 42 ask figures. The sheet now carries the measurement, `precut.py` fails on it, and the ask
  layer needs new silent primaries rather than another pin.
- Merging A1's weekly reports, so the solver had to decide which issue of a report counts: dropped, the
  asking sentence pins "each weekly report issued in April and May" and the pin may not move, so the
  primary had to sit in the register's own key instead.
- A1's silent primary inside the register itself (a second `result_seq` or a second `aliquot_id` carrying
  the specimen): dropped, both are visible in the register's own columns, which makes them a marker
  (`supplemental-stumping` ban 2); the specimen's one identifier had to live in another file, so it is the
  biobank reference in the crosswalk and the register never points at it.
- Re-cutting A1 on the request register rather than the crosswalk: dropped, the register's request
  sequence is a frozen draw the call's report dates depend on, so the key had to come from a file the
  comparison does not read.
- A2's amendment log naming `hetx_call` for every specimen: dropped, a reviewed specimen's call of record
  is `review_outcome`, so one amendment row would have moved two columns and a solver applying the log
  literally would have landed a different figure from one propagating it. The log now names the column of
  record for each specimen, which closes the fork and is what a release desk would write.
- A2's amendment log at 430 rows with 45 per cent of them call corrections: cut to 367 rows and 122 call
  corrections, because a desk correcting two fifths of the extract's flags is not credible and the measured
  delta of 2.0 to 5.9 per thousand already misses every month at the stated rounding.
- A six-level dilution panel: cut to three levels, because the pair arithmetic counts figures and six
  levels put 12 of the 36 ask figures in the ask whose primary the cracker partly survives.
- `release_amendments_2026-07_2027-03.csv`: renamed twice, to `2026-03_2027-05`, because the name has to
  bracket the amendment dates the file actually holds; `checks.py` now asserts the bracket, so the name
  cannot drift away from the data again.
- A fourth primary on A2, a second pull of the same extract: dropped, one vintage device per ask is the
  ceiling and a second pull would have given the solver the diff for free.
- `freeze.py check task195 --mode rubric` without `--allow`: it reports three main-call figures moved,
  `panel_weeks.BA-2027-W13.difference`, `panel_weeks.BA-2027-W16.difference` and
  `panel_weeks.BA-2027-W18.difference`. They are A1 ask figures, not main-call figures: freeze classifies a
  `figures.json` value as main-call when it equals a number scraped from blocks 1 and 2, and those three
  differences were 4, 3 and 4 before the re-cut, which are the "3." and "4." list markers in Critical
  Components. The three keys are named in `--allow` for that reason. A key-by-key diff against the
  judge-approved `figures.json` is the real evidence: 43 keys moved, 26 under `panel_weeks` and 17 under
  `dilution`, and nothing else; the cutoff table, the interval, the ladder's four rung values and A2's
  twelve monthly figures are byte-identical. The pack's own proof is stronger still: the four files the
  call reads are byte-identical to the approved pack by sha256, and the fifth, the panel register, is
  byte-identical on all 5,839 of the comparison's rows, with 0 of the 214 added rows touching one.
- Pinning the specimen identity and the monthly-rate basis in `validation_extract_dictionary.csv`, which is
  what the stage-4 judge's first two fixes asked for: declined, because those two readings are exactly what
  A1's and A2's devices ride on, and the build has already been through that once, when pins ordered after
  the first judge pass closed the readings the devices rode on and the measured pair ceiling came back 83.5
  against 35.1 on paper with leakage at 100 per cent. The ambiguity moved into the asking sentence instead,
  where a pin says what to compute without making it easy to compute.
- Filing in the dictionary or the protocol that detection and false-call are per-specimen indicators on the
  same specimens, the judge's optional third fix: declined. The pairing already closes through KVAL-07 3.1,
  3.2 and 3.4, so the sentence buys no determinism, and it would advertise the pairing on a build whose
  Gate F is moderate and whose stage-4 reader landed the call off 3.4 alone.
- Keeping the paired Wald endpoints in block 1 and naming the estimator beside them: dropped, because
  naming the estimator in the write-up files the HOW of a figure the protocol leaves open, and 4.1(a) needs
  only a lower bound clear of zero. The write-up now states what every paired estimator agrees on.
- Asking for the results each report issued as a third graded figure on A1, which the re-wording invites:
  dropped, because the row count per report is the one A1 figure the cracker's path gets right, and grading
  nine of them would have taken the measured mirror leakage from 8.3 to 26.7 per cent and the pair ceiling
  from 33.1 to 43.2, over the bar. The sentence names the results issued as the thing the excess is measured
  against and grades the two figures that carry the device.
- Changing the register's own columns to carry the vial reference: dropped, it would put the device's answer
  in the file the device is in. The crosswalk instead gained the 912 earlier accessions it was missing, so
  the vial is determinate for every row of the ask's window without the register pointing at anything.
- `freeze.py check task195 --mode rubric` now reports two moved items, and both are the third pass's own
  orders. Final Recommendation numbers: the list loses exactly `1.37` and `6.77`, the paired Wald endpoints
  the judge ruled estimator-specific, and nothing else. Critical Components numbers: the list loses exactly
  `1`, `2`, `3`, `4`, which are the ordered-list markers of its four items; `freeze.py` was fixed after this
  build's snapshot was taken so that it strips markers, and the snapshot still holds the unstripped lists,
  so the delta is the script's own repair and not a figure. Measured against the snapshot directly: zero
  main-call figures moved, the stump, the card's driver, the prompt's call sentence, the ladder section and
  the default-path section are all byte-identical, and the three `panel_weeks` difference keys still need
  `--allow` because the stale snapshot classified them as main-call for the same marker reason.
- Adding "after the release desk's amendments" to ask 4, the judge's second optional tightening:
  declined. That clause tells the solver the amendments exist and to apply them, which is the whole of
  A2's work. The judge marks it optional and has already ruled the ask forced, so there is nothing to buy
  and a device to lose, and this build has already spent its devices on pins once, at a measured pair
  ceiling of 83.5 with 100 per cent leakage.
- Adding "within a fifth of that level" to ask 5, the judge's third optional tightening: declined. The
  judge ruled the ask forced and found the alternative reading fails on units, because the replicate
  results are fractions near 0.004 to 0.06 while a median recovery is a share near 1. The prompt sits at
  996 of 1,000 characters, so the eight characters would have to come out of a load-bearing clause.
- A single global het threshold of 36.50 in `checks.py`'s SF8 probe: dropped with the two-threshold run
  log that justified it. The run log now records one validated threshold, 36.60, held for every batch of
  the quarter, so re-deriving the call from the run log converges on the recorded call exactly and SF8
  closes by convergence. A threshold that moved mid-quarter made a sloppy single-threshold re-derivation
  land on a different cutoff, which is a fork the build does not need.
- Giving the April and May weekly reports a reconciliation residue along with the rest: dropped. Those
  nine are ask 3's referee and the judge credited the report footer with ruling out the specimen-and-aliquot
  handling, so a residue there would reopen what "results issued" means. The residue sits on three reports
  outside the ask's window, each with its reason stated in the report.
- Keeping the warehouse extract's 2027-03-04 pull date and truncating its releases instead: dropped,
  because the releases run to 2027-03-31 by the extract's own four-to-twenty-six-day lag and truncating
  them would move A2's twelve monthly figures, which the judge has approved twice.
- Leaving the dilution panel's lowest level at 0.4 per cent and tightening only the draw, so that the
  judge's approved Ask 5 row would stand untouched: dropped. Four hundred draws at that level were
  searched and only two cleared the one-fifth line by three stored steps, both at a median recovery of
  1.098, outside the band a sensitivity panel reports. The quantisation, not the draw, was the cause, so
  the level moved. The consequence is on the record: the shipped L1 row reads 0.963/7 against the 0.878/7
  in `determinism_check_report.md`, which is the judge's own artifact and is not edited. The count the
  judge graded is unchanged, the clearance is 4.2 stored steps instead of 1.2, and the level now sits at
  the estimator's stated limit of detection, where a sensitivity panel belongs.
- Deleting clause 3.4's first sentence ("Detection is counted per specimen") so the records alone force the
  pairing, which is the repair the Gate F failure was handed over with: measured inert. The deletion is
  legal, because the unit fork closes by convergence (counting detection per read set returns the same
  294, 308, 310, 319, 326 detections, the same +2, +16, +18, +27, +34 increases and the same false-call
  rates, so axis 2 and SF3 close by C1 rather than by the sentence), but it moves no route: the reflex
  sweep run on the shipped pack scores 6 of 12 enumerated routes landing the golden 0.030 and not one of
  them reads a clause.
- Rewording 3.4 so it files the unit without signalling the pairing: dropped, the pairing is a consequence
  of two filings the spec makes mandatory. 3.2 files the population at specimen grain and 4.1 files the
  comparison of the two screens on that population, so one specimen carrying both calls follows from the
  estimand, and `determinism-check` section 1 requires the estimand filed literally. There is no wording
  of a parallel run in which the two screens are not read on the same material.
- The whole paired-variance architecture (`own:paired-difference-against-marginal-intervals`): spent, on
  measurement rather than on the clause. The decisive step moves no point estimate (the increase is
  +0.040712 at 0.030 under both estimators, identical to 1e-12 at all five cutoffs), so the call is a
  binary estimator-family selection, and the family is internally unanimous on each side (every paired
  member's lower bound 1.34 to 1.53 points, spread 0.187 points, all clear of zero; every unpaired member
  at 0.015 or the hold). A nonparametric bootstrap over the specimen rows and a regression of detection on
  screen with specimen-clustered standard errors both file 0.030, and both are one line on the table the
  population rebuild necessarily produces. `stumping` Part 6: a reflex reaching the golden spends the stump.
- The reference standard's own misses as the decisive step (the identity panel's sensitivity falling with
  the markers it typed): dropped, unidentified in this pack. Inside the comparison the panel typed 84 to
  107 markers, 5,772 of 5,839 specimens at 90 or more and none under 40, so the records measure no
  sensitivity gradient about themselves and the candidate is `stumping` 1.2b case three. Building it needs
  a different reference-standard design, which is a draw and not a ladder.
- Plate clustering as the decisive step: dropped twice over. The measured plate design effect on the
  increase is 0.725 to 0.863, below 1, so clustering narrows rather than widens and separates nothing
  (established at 0.030 and unestablished at 0.050 either way), and a widening correction fails the
  variance-only screen anyway, because then every conservative reflex files the hold with no analysis.
- In-sample selection over the five listed cutoffs as the decisive step: dropped, no lever. Unadjusted,
  Bonferroni, Sidak and one-sided Bonferroni over the five cutoffs all establish 0.030, 0.020 and 0.015
  and all recommend 0.030, so no multiplicity reading moves the call.
- Moving the decisive step anywhere else inside KVAL-07 4.1: dropped, the rule leaves nowhere to move it
  to. Four of the five per-cutoff graded figures are recorded statistics the pack fixes exactly (the
  detections, the increase in specimens and points, the false-call rate, all reproduced from the shipped
  files), so by `stumping` 1.2 nothing there is left to estimate and the interval is the only residue.
  Changing that means changing the decision rule, which is the world's own governing document, which is a
  stage-1 draw.

- Resuming this architecture at all: refused by the free guard, which has moved since the ship.
  `guard.py heart` now returns BLOCK on `test.same_driver_older`, because the decisive gap, the decisive
  pattern and the Gate G mechanism all repeat task190 architecture 6 and this card carries no
  differentiation against it (the Draw section answers that test against task228's lineage, which was the
  only collision on file when the draw was fixed). The collision is not cosmetic: task190 architecture 6
  filed a 95 per cent level in an authority memo over a quantity whose variance was then the standard
  formula, screened its decisive rung silent, and its isolated reader landed the call and all 38 ask
  figures. This build filed a 95 per cent level in a protocol clause over a quantity whose variance is then
  the paired formula, screened its decisive rung silent, and its isolated reader landed the call and 26 of
  30 ask figures. Same gap, same pattern, same mechanism, same measured death twice, so the architecture is
  spent at corpus level and not only in this folder. `guard.py surface` is clean (exit 0) on the same pack.

### The thirteen rule lines for the deleted-clause candidate, with the failures named

Written for the repair as handed over (3.4's first sentence gone, the records forcing the pairing), not
written to pass. Nine lines hold, three fail, and the client's own test is answered no.

- **Task type:** genomics-gwas-high-dimensional-association, the anomaly-detection flavour, unchanged: a
  sample-level anomaly called from a high-dimensional marker signal. Holds.
- **Domain test:** the deciding quantity is still the increase in confirmed contamination events the same
  archived read sets yield under a second caller, which a laboratory validation judges on the discordant
  specimens. Holds.
- **Swap:** unchanged and still bites: two inspection rigs reading different units have nothing to pair.
  Holds.
- **Layer 1:** unchanged, every mess item the laboratory's own systems write, each asserted neutral. Holds.
- **Layer 2:** `field_method`, the uncertainty of a paired difference. Holds as a family, and is not what
  fails.
- **Decisive step:** take the increase's 95 per cent interval from the specimens the two screens call
  differently, with the pairing read off the records rather than off a clause. Stated, and it is this step
  that the two failing lines below are about.
- **Not semantics:** holds. Every field, code, unit and definition can be read correctly, the comparison
  reconciled to 5,839 specimens and 393 events and every count recovered exactly, and the easy route still
  files the hold, because the point estimate is identical under both estimators (+0.040712 at 0.030 either
  way) and only the standard error differs (0.01378 against 0.03029, z 2.953 against 1.344).
- **Not rule application:** holds in the letter and does not save the build. With the sentence deleted no
  filed clause performs the step, and executing 3.1 to 3.5 and 4.1 word for word still leaves the estimator
  unchosen. What the build fails is the analyst test below, not this line.
- **Analyst test:** **fails, measured.** The easy route is supposed to file the hold. Run as code on the
  shipped pack, 6 of 12 enumerated routes file the golden 0.030: paired Wald, continuity-corrected
  McNemar, exact McNemar, a nonparametric bootstrap over the specimen rows, a permutation of the screen
  label within specimen, and a regression of detection on screen with specimen-clustered standard errors.
  The bootstrap and the clustered regression read no clause and need no insight into the design: the
  population rebuild 3.2 forces produces one row per specimen, and resampling those rows is paired for
  free. The client's test, could a strong analyst who cleaned the data and read every rule correctly still
  get the answer wrong by doing the analysis the easy way, is therefore answered **no** on measurement.
- **Estimand:** holds. KVAL-07 3.1 to 3.5 file the population, outcome, window, unit and comparison, and
  with 3.4's first sentence gone the unit closes by convergence instead (measured above). The decisive step
  settles none of the five parts, which is why the WHAT screen passed and the build still died.
- **No decoy:** holds. Nothing is planted, no document ranks the cutoffs or argues a basis, and the
  difficulty survives deleting every document.
- **No certified replay:** holds. No closed corpus of past determinations and no published figure to
  reproduce.
- **Lesson:** **fails to be a lesson.** What a model learns by getting this right is to use McNemar on a
  paired comparison of two classifiers, which is the textbook first move on that 2 x 2 rather than a
  judgment the data settle. The library test fires: the golden is a card's method applied as the card
  states it, and the blind reader landed it in one pass at about 70 per cent confidence.
- **(2026-10-25, measured) Re-measured with the scorer, and the architecture is confirmed spent from the other side.** `score_reader.py` on the stored reader answers: the reader **landed the call, 1 of 1** (0.030), and took **26 of 30 ask figures (86.7 per cent)**. Both halves fail at once, so neither hardening the ladder nor re-siting the devices reaches it; the number needs a re-root, which is what the stage-2 measurement already concluded on the family spread.
- 2026-10-31, reship under the 10-30 gates: the export manifest and the validation extract dictionary were describing
  files (leak.py sweep 1); both removed, their facts already carried by the exports' own columns, the KVAL-07 protocol
  and the model card; every graded figure unchanged.
- Reship of 10-31 without the extract dictionary: closing judge pass 2's FIX_NOW (the vial identity, the amendment rule) in KVAL-07 restores determinism but leaves A1 and A2 executable from a filed sentence; a careful cracker keeps 33 of 36 ask figures (pair 78.9), so the asks' devices are redesigned before the reship ships, never shipped on the lazy cracker the sheet measured.
- Reship of 11-01, measured before any document work with the honest careful path (`generator/cracker.py`):
  with the vial reference and the amended value filed, that path keeps 36 of 36 ask figures on the shipped
  cut, pair 83.5, not the 33 of 36 the resume line carried. The difference is the dilution ask: its
  replicate sheet names the stock each replicate ran from, so a join of the replicates to the prepared
  levels on stock and level, which a fan-out on the level name alone forces, keeps all six; the 3 of 6 on
  file came from a path that ignored that column.
- A1's device as shipped, a vial booked in twice under two accessions with the vial's reference in the
  biobank's register: a work order once the reference is filed, because the asking sentence counted
  vials and the footer names the vial's key. Re-sited onto task236's shape: the sentence counts specimens,
  the register's accession is the specimen's key at face value, and the vial reference is what joins two
  accessions into one specimen. Every A1 figure is unchanged.
- A1's device on a per-collection reference (the biobank numbering each project's vials apart, so one
  number recurring across projects): dropped. A weekly report's vials are booked within days of each other,
  so two collections' numbers meet inside one report only by coincidence and the device has no mass, and
  the judge's literal reading of "the biobank's own reference for the vial" would have stood against the
  golden.
- A1 on a re-booking that scans the laboratory's own freezer label as the source barcode, or on a
  re-labelled vial: dropped, each is a prior-id chain the battery walks once the odd format is seen, or a
  link family members share.
- A2's device as shipped, the warehouse extract predating the release desk's amendments: a work order once
  the log's footer files that the amended record carries value_after, which pass 2's FIX_NOW required. Kept
  as a hazard (2.7 to 7.2 per thousand in every month for the response that skips it); the primary moved to
  a depth top-up booked under an accession of its own, linked to its specimen only by the extraction.
  Every A2 figure is unchanged, because the top-up adds a second accession to a specimen the truth already
  counts once.
- A2's top-ups at a flagged rate of 0.10: October's accession path sat 0.2 per thousand from the golden,
  two bins on one top-up flag. Raised to 0.16, every month now misses by 0.3 to 2.5.
- A2 on recalled releases (a result withdrawn after the month closed, counting in its month as booked):
  dropped, "released in the month" reads both ways for a recall and the closing sentence would have named
  the device.
- A2 on release dates written as the nightly load's date, or on accessions reissued after a LIMS restore:
  dropped, the first is a clock a weekday profile finds and the second gives one or two months of mass.
- A second device of another family on each ask, so the full includer misses a block: none drafted held.
  A report set by issue date moves two of nine reports and the PDF states the issue date; a reporting month
  closing off month end is filed or unfair; a receipt second as the top-up's link is not an identity, and
  the seven receipt seconds two specimens of one project share move no month at the stated rounding. The
  full includer's keep is measured and stated on the sheet instead.
- The dilution ask (median recovery and the replicates within a fifth, by level): dropped, not re-sited.
  The stock join is a battery item; a stock inferred from the run date is found by a careful solver once
  two stocks are listed; a prepared level rebuilt from DNA masses is computed right by the same solver; a
  replicate sheet without its stock column, or a level label used twice, is a fork. The workbook stays in
  the pack as a distractor, relevant to the estimator's sensitivity near the cutoffs and unused by the
  solution.
- Filing the vial reference and the amended value in KVAL-07 5.3 and 6.3, the route the resume line named:
  dropped. KVAL-07 is a document the call reads, and an ask's organ there breaks the separation line; each
  fact went into its producing file's own footer (the biobank's register, the release desk's log), and
  KVAL-07 changed only in 6.2, where the sentence on an export manifest the pack no longer ships came out.
- The weekly reports' footer "a result is issued per specimen and aliquot typed": reworded to "for each
  aliquot typed", because a literal reader could take the partner's "specimen" as the specimen A1 counts.
- Reship redesign of 11-01, judged pass 3 (`determinism_check_report_pass3.md`): the main call reproduced and
  forced, decisive step analytical, Gate G method selection; SEND_BACK on both asks, because the judge holds
  that "specimen" reads as `specimen_id` in every file and that merging accessions through the vial (A1) or the
  extraction (A2) is an unstated identity rule. Filing either identity, as its fix asks, hands the device to
  the careful path (36 of 36 measured on the shipped cut with the facts filed, pair 83.5), so the
  task236-shaped identity devices are dead in this world under this judge; no device drafted survives the
  filing (the lines above). Blocked: the ask layer needs devices that are not identity reconstructions, or the
  asks are cut back to what the records force and the pair is priced on the call alone.
- Reship of 11-03, the identity layer replaced. A1 (each April and May weekly report's specimens counted
  through the biobank's vial reference) and A2 (the twelve-month baseline counted once per extraction id)
  are dropped: judge pass 3 held both merges unfiled, and with them filed the careful path keeps 36 of 36
  (pair 83.5). No identity reconstruction or counting convention is drafted again. The ask moves onto the
  screen in service's twelve reporting months by extraction method, on the LIMS method table's re-coding at
  the second extraction robot's go-live on 2 November 2026 (`## Ask sheet`); ceiling.py on the cut pack:
  the cracker and the mirror keep 0 of 16, pair 36.8 with the chart inside the ask weight.
- Keeping the monthly per-thousand series beside the method ask: dropped. With the extraction-id device
  gone every month is reachable by the battery (the amendments applied, the review outcome taken, the
  correction released again folded on its accession), and twelve kept figures would put the pair at
  52.1 on the ask figures alone, 54.3 with the chart.
- A depth basis that changes at a pipeline version (depth over all reads before it, after duplicate
  removal from it) under a below-the-estimator's-floor count: dropped. Unfiled, the earlier basis is a
  fork; filed, the cracker converts; and either uniform reading keeps one side's months.
- A control threshold re-validated mid-year under a count of the reviews that reversed the screen's own
  call: dropped. The cracker re-derives the automatic call at the threshold the run log files, and the
  recorded automatic calls show the earlier threshold the moment it checks its rule against them.
- The review overwritten into hetx_call by an earlier LIMS: dropped. The battery's re-derivation of a call
  its het excess contradicts recovers the screen's own call, so the flags reach the cracker.
- Swapping what the two call columns hold on the earlier records: dropped. "Reviewed ones by their review
  outcome" then reads literally to the cracker's answer, and a column swap is a planted defect.
- A partial re-coding that left magnetic bead on code 1: dropped. The largest method's four figures would
  have reached the cracker; the re-coding passes every 2026 code to another method.
- Holding the receipt-date split outside the bin on every figure: not forced. It is the response that has
  found the re-coding and splits on the wrong date, so it keeps 10 of 16 and misses every released count
  by the extractions of the last receipts before the go-live; recorded as a stress row, not a stop.
- A month-by-method grid, or the method figures by quarter: dropped. The quarter after the go-live is read
  right on the names, so the grid hands the cracker its post-go-live cells; the twelve-month figures carry
  the device in every cell.
- Reverting the panel register, KVAL-07 and the model card to the 10-17 bytes: declined. The 11-01
  reader's realism tells (request numbers stepping by one on the 912 earlier receipts, a protocol sentence
  pointing at an export manifest the pack no longer ships, an addendum addressing a reader who recomputes)
  were fixed there; each change touches no comparison row and no clause the call executes, and checks.py
  regenerates each file with the change undone and asserts the shipped sha256 back (flagged to the author).
- `freeze.py check task195 --mode rubric` without `--allow`: nine items, `panel_weeks.BA-2027-W13` to
  `W21` `.week_ending`, A1's report dates, classified main-call because block 1 states 2027; they left with
  A1. Named in `--allow`; with them the check passes, and the Final Recommendation and Critical Components
  numbers, every main-call figure, the stump, the card's driver, the ladder, the default path and the
  prompt's call sentence are unchanged.
