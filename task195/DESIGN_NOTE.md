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
| Spine | `qc_screen_history_2026-03_2027-02.csv`, one row per specimen's quality-control screen record |
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
| SF8 | the screen in service's call | the flag the quality-control export records, reviewed calls included | the flag re-derived from the het-excess value and the batch control threshold | `same call` | 3.4 "when the quality-control export records the flag"; the re-derived route moves the counts to 283 detections and 93 false calls and still answers 0.030, asserted |
| SF9 | the window | receipt date on or after 1 March and on or before 31 May 2027 | a processing or release date | `same call` | 3.1 names the receipt date, and the quality-control export carries no other date for a specimen, so the readings converge on the same rows (asserted) |
| SF10 | the increase | the difference between the two detection counts on the filed population | the ratio of the two detection rates | 0.030 | 4.1(a) says "the increase in confirmed contamination events detected"; `same call` asserted on the paired log-ratio interval |
| SF11 | accepted read | `read_accepted` is Y in the quality-control export | the latest read whatever its status | 0.030 | 3.2 "an accepted read"; the dictionary defines `read_accepted`; voided reads carry no call, `same call` asserted |
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
| 18 | Dimensional units | fraction or per cent | the dictionary states the estimate is a fraction; per cent appears only as a label on the dilution panel's levels |
| 19 | Code and status semantics | verdict, read status, project and agreement codes | dictionary semantics for every call-path column; never the stump |
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
| The partner laboratory's weekly report totals (PDF) | the panel results issued each week, the ask-1 control total | ties only with the register's re-sent and repeat rows resolved; says nothing about any detection count |
| `release_volumes_monthly_2026-03_2027-02.csv` | the specimens released each month, the ask-2 control total | ties only on the release month; carries no flag, verdict or cutoff |
| The model card's estimate distribution | the re-run's output distribution over the whole archive | reproduces identically on every route; carries no verdict, so it confirms nothing about detection |
| The dilution panel's summary row | the panel's own replicate count per level | ties under every unit handling; the recovery figures are the ask's, not the call's |
| Nothing else | no file states a detection count, an increase, an interval or a cutoff recommendation | no oracle ties only under the golden |

## Ask sheet

Three asks, 42 graded figures, none keyed to the call or its construction and none on the comparison's rows.

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops and lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 the panel register against the partner laboratory's weekly reports | 9 reports x (specimens the report covers, difference against the report's own total) = 18 | the audit trail of an input the call consumes, to another system's control total | KVAL-07 5.1 puts the identity panel's delivery record in the validation file | D1 duplication: 27 results issued again under a second sequence number and 18 panels repeated on a second aliquot, 45 extra rows spread over all nine reports, every one of them on a specimen the comparison does not hold | a report issued two working days late, noted in the report itself; verdicts for receipts before the run window; the second aliquot's verdict is not always the first one's | `identity_panel_register_2027.csv` (7,624 rows; specimen_id, aliquot_id, report_ref, report_date, result_seq, verdict), `identity_panel_weekly_reports_2027.pdf` (the report's own total), 9 columns | row count per report (every difference reads 0), distinct specimens after dropping the second aliquot rows only, distinct specimens after dropping the second sequence rows only, the answer; lazy delta 45 results over the nine reports | a partner laboratory re-sends results its courier returned to the depot and types a second aliquot when the first is borderline |
| A2 the screen in service's twelve-month record | 12 months x flagged specimens per thousand released = 12 | a measure the screen in service carries that the call does not turn on: KVAL-07 5.1's record of the screen over the twelve reporting months before the parallel run | the quality review reads the baseline before it reads the parallel run | D4 absence: the warehouse's nightly load writes the automatic call in `screen_flag` and leaves it empty for the 3 per cent of specimens the duty bioinformatician reviewed, whose outcome sits in `review_outcome` | the extract carries a receipt date, a receipt time in UTC and a release date, and the reporting month is the release month; 4.6 per cent of rows are withheld or superseded and never released; the October daylight-saving overlap; the reporting pack writes thousands with a space | `qc_screen_history_2026-02-15_2027-02-28.csv` (31,200 rows, 14 columns), `release_volumes_monthly_2026-03_2027-02.csv`, `validation_extract_dictionary.csv` | automatic call only (1.6 to 6.6 per thousand low in every month), receipt month (3.0 low to 2.7 high), all specimens as the denominator, the answer; lazy delta 2.0 to 6.9 per thousand | a warehouse extract carries three dates and two call columns, and a reporting pack counts releases |
| A3 the quarter's dilution panel | 6 levels x (median recovery of the prepared level, replicates within a fifth of it) = 12 | a component of the case: KVAL-07 5.1's analytical sensitivity panel for the quarter | the review asks what the estimator recovers at the levels the listed cutoffs sit near | D3 units and meaning: the panel labels its levels as the second contributor's share in per cent and records the prepared level as a gravimetric fraction, and the replicate results are fractions | a replicate voided on a control failure and carried with no result; the two sheets write the level key in different case; the panel notes state the replicates reported | `dilution_panel_2027q1.xlsx` (sheets "Prepared levels", "Replicate results", "Panel notes", 9 columns), `mixture_estimator_model_card_v34.pdf`, `rerun_pipeline_config_v34.json` | the per cent label as the level (every recovery reads about 0.010, two orders out), the voided replicate counted as zero, the mean rather than the median, the answer; lazy delta two orders of magnitude | a laboratory prepares a dilution series each quarter and labels the levels in per cent |

**Main population zero counts (asserted).** Device and hazard rows inside the comparison's 5,839 specimens:
A1 0, A2 0, A3 0. The 45 re-sent and repeat rows cover no comparison specimen (asserted by name), the
twelve-month warehouse extract covers receipts to 28 February 2027 and shares no specimen with the
comparison (asserted on the id sets), and the dilution panel holds prepared control mixtures. Delete every
device and the call is unchanged, asserted.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| a report issued two working days late | A1 | none on the figures: the register's rows carry the report reference, so the note is texture |
| the second aliquot's verdict differs from the first's | A1 | 5 of the 18 repeat panels carry the other verdict, so a verdict-level dedup misses them too |
| withheld and superseded releases | A2 | the denominator moves by 4.6 per cent in every month |
| the UTC receipt stamp and the October daylight-saving overlap | A2 | the receipt-month read moves every month, 3.0 per thousand low to 2.7 high |
| a dilution replicate voided on a control failure | A3 | L3's median moves one position when the void is read as a zero |

**Referee.** The partner laboratory's weekly report totals are the one byte-clean referee: they state the
results each report issued and arbitrate A1 without stating a specimen count, and they tie under no other
handling. There is no referee for the call, and no control ties only under the golden.

| Ask | The cracker (landed the call, ran the hygiene battery, executed every filed rule, matched every control) | Verdict |
|---|---|---|
| A1 | counts register rows per report, which is what the report's own total counts, so all nine differences read 0 and all nine specimen counts are 3 to 7 too high | miss |
| A2 | sums `screen_flag` and groups the warehouse extract by its first date column; every one of the twelve months lands 1.6 to 6.6 per thousand low, each of them several bins outside | miss |
| A3 | reads the level label's per cent as the prepared level; all 12 figures land two orders of magnitude out | miss |

**Pair ceiling:** 35.1 (the cracker banks 38 + 7 + 55 x 0.12 = 51.6; the best response off the call banks
5 + 7 + 55 x 0.12 = 18.6; the pair averages 35.1).
**Mirror leakage:** 12.0 per cent of ask weight (the mirror stops at rung 2, takes the same three ask paths
as the cracker and keeps only the figures no device moves).

## Leak review

`leak.py task195 --asof 2027-06-21` is REVIEW, with five lines, each answered here.

- Sweep 3, the protocol carries 8 of the 10 distinctive words of the committed call: the call is written in
  the protocol's own nouns (the screen in service, the candidate screen, the cutoff, the quarter), which
  `reduce-house-fixes` H20 requires the pack to carry. KVAL-07 states no cutoff, no detection count, no
  increase and no interval, and the swept words carry no figure.
- Sweep 4, the protocol, the model card and the 2025 platform validation carry stump-paragraph terms: the
  terms are the field's ordinary nouns (specimen, verdict, estimator, cutoff, method, laboratory). The
  decisive vocabulary is absent from every document, asserted by a grep of the extracted text for paired,
  pair, discordant, McNemar, two-sample, standard error, uncertainty, overlap, same specimens, marginal.
- Sweep 4, the prompt sentence carrying two stump terms: the terms are specimen and comparison, the words
  the asks are written in; the sentence states the question and the figures wanted and no method.
- Sweep 10, container metadata: the audit found no writer signature; every container carries the
  laboratory's own producer and an in-fiction stamp.
- Sweep 8 cleared after the quality-control export's call column was given the screen's own name
  (`hetx_call`, values FLAG and CLEAR) in place of a generator's `screen_flag`.

## Pre-ship check

**Free gates, all green on the final rebuild.** `generator/checks.py` 153 assertions; `generator/verify.py`
134 independent checks from the bundle and `figures.json` alone; two byte-identical rebuilds of `target/`
and `golden/`; input gates 18 files, 5 formats (csv, tsv, json, xlsx, pdf), a 31,200-row file, 4 distractors
declared in `metadata.json` and named in no file name; `figures_check.py` 117 figures, 0 absent;
`precut.py` 49 checks, 0 FAIL, 0 WARN; `leak.py --asof 2027-06-21` REVIEW with every line answered above;
`guard.py surface` 0 promoted pairs; `guard.py heart` WARN, nearest 0.08 (task185's ledger row), no BLOCK;
containers audited clean by `scrub_producer_metadata.py` for both `target/` and `golden/`.

**The 10/10 rules re-read against the built pack.** The decisive step is still analytical: the pack ships
the two screens' per specimen calls and the panel's verdicts, and the increase's uncertainty is the only
thing no filed sentence settles. Every mess item is Layer 1 and asserted neutral (R2); R3a files the hold on
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

**Stage 4 status.** The leak reader and the determinism judge are staged as two isolated working
directories for the orchestrating session to spawn, because this build session has no agent tool.
`<scratch>/t195/judge` holds `judge_brief.md` (the isolation rules naming the forbidden files, the
literal-reading-first method, the recompute-everything requirement, three probes on this build's interval,
population and rule direction, a request for the Gate G and Gate H lines in full, and the judge's system
prompt inlined verbatim), `prompt.txt`, `submission_blocks.md` and a fresh unzip of `target.zip` into
`target/`; its verdict goes to `verdict.md`. `<scratch>/t195/reader` holds `reader_brief.md` (the six
solver's-eye questions and three working-analyst questions: what the reader reaches and which choices the
documents did not make, realism named column by column, and whether each supplementary ask is forced),
`prompt.txt` and a fresh unzip into `bundle/`; its answers go to `reader_answers.md`. Every finding from
both is fixed in the generator in one pass, the free gates re-run, the judge re-run once on FIX_NOW and the
reader only if a document or the prompt changed.

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
  with the receipts bridge, same reason, and the three remaining asks carry 42 graded figures between them.
- `world.org_family: university_or_school`: dropped at the duplicate check when task233 was filed against
  it; the laboratory became a research institute's genomics core, which moved no figure and no rung.
