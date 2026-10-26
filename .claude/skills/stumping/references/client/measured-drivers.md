# The measured tasks, one driver each, read against our bar

> The client measured its Batch 14 accepted tasks with four runs of the current model each and recorded the mean. We are graded on the top two responses averaging under 70 per cent with at least one of them stumped on the call, built to 60. The two measures disagree on more than half the corpus: a task the client lists at a mean of 0.45 can sit at a top two of 0.655 because one run cracked it. This file reads each of the 49 recorded tasks against our bar and writes one driver per task, the decisive move with the domain nouns stripped, in the form the fingerprint card uses. The compact records of the same tasks are in `../../../guide-to-prompt/references/exemplars.md` and the full ones in `exemplars/` beside it; the trap types and their counts are `../strategies.md` Part 5, numbered the same. Read this file at the draw, after Part 5, so the rung being drawn comes from a task whose call held and not only one whose asks carried it under the bar.

**How the verdict is computed.** Top two is the mean of the two highest of the client's recorded runs, which the exemplars carry beside every task. Three tasks have three runs and one has two; their top two is marked with an asterisk. Two tasks have one run and get no verdict. A task **held** when its top two is under 0.50, which in these runs meant the call itself stumped; a coin flip can still clear the bar of 0.70 when its asks hold, but only a hold is evidence for the rung. The 29 that gave way fall into three signatures, and the signature is what a build is designed against.

| Signature | Count | Shape of the runs | What it means for a build |
|---|---|---|---|
| **held** | 18 | every run low; spread 0.21 or less on four runs (the one two-run task spreads 0.40) | the construction is compound or outside the solver's hypothesis space |
| **coin flip** | 13 | one or two runs at 0.57 to 0.99, the rest at 0.09 to 0.56; spread 0.38 or more | one decisive insight a run either has or does not; a stump under the mean, a fail under the top two |
| **leaked** | 13 | the wrong committed figure recorded, and the top two still 0.51 to 0.79 | the asks were collected around the wrong call because the decisive step sat downstream of most graded figures |
| **landed** | 3 | the call right in most runs, top two 0.63 to 0.75 | the difficulty sat in a margin or an interval; the call was the natural computation |
| **one run** | 2 | a single run at 0.35 and 0.44 | no verdict |

Each entry below gives the client's short name for the task, its top two, the runs, the trap numbers in `../strategies.md` Part 5 it feeds, the driver, and one line on why it held or gave way. Entries are sorted by top two inside each group. Where the client's note gives a run count ("4/4", "three of four") the entry quotes it; where the note describes the miss without one, the run pattern is the evidence, and the entry says so where it matters.

## Part 1. The 49 tasks

### Held (18)

**Winter relief eligible units** · 0.18 · runs 0.16, 0.18, 0.18, 0.18 · trap 2
Driver: The eligible unit is composed from person records by relationship, age and subfamily codes, with unit income the members' adjusted person income, and only that composition reproduces six published allocations to the dollar; one unit per housing record with household income reproduces one share and no allocation.
Why it held: a multi-rule composition the solver declined to build, upstream of every graded figure, with six dollar-exact controls; the solver reported the failed replication as a caveat and kept its unit.

**Field-support cycle by division and class** · 0.205 · runs 0.21, 0.20, 0.19, 0.16 · trap 14
Driver: The scored cell is a region crossed with each fine class code rather than the coarse two-way split, and the rate is total net movement over total residents rather than a mean of unit rates; each shortcut on its own sends the decision to a different cell.
Why it held: two independent moves, grain and weighting; the solver took the weighting and coarsened the grain because the coarse shorthand is the familiar one, and the four scores sit within 0.05 of each other.

**Replenishment cover schedule** · 0.21 · runs 0.21, 0.21, 0.00, 0.21 · traps 1, 8
Driver: Published yearly means reproduce only when the observation is regrouped from order lines to arrivals timed from the earliest order carried and a population is excluded through a date-window join to a register with no flag column; either move alone reproduces fewer means than neither.
Why it held: a conjunction whose partial application scores worse than nothing, so no hill-climb reaches it; 24 exact controls and a clause making reproduction the gate; the solver saw 19 of 24 and shipped.

**Level-mix referral** · 0.26 · runs 0.26, 0.26, 0.22, 0.26 · trap 19
Driver: A saturated share ties 111 entities at the maximum, and the standard's lowest-value-consistent-with-all-files rule, applied by reconciling a summary file's totals to a detail file's rows, leaves one entity settled there while the documented tie-break names another.
Why it held: the rule is a cross-file reconciliation rather than a column operation, and the written tie-break is the lure; the solver read the rule and dismissed it as inapplicable.

**Stalls traded** · 0.26 · runs 0.26, 0.22, 0.26, 0.26 · traps 2, 8
Driver: The counted unit is defined nowhere in the standard and is built by joining neighbouring rows under each site's own numbering scheme on a three-attribute adjacency convention recoverable only from last year's printed bands; one unit per row and one per licence both fail the seventeen printed figures.
Why it held: a unit built by adjacency is outside the solver's hypothesis space; the solver saw 91 capped sites against the printed 79 and hard-coded the bands rather than change the unit.

**Journey-time cause** · 0.265 · runs 0.27, 0.26, 0.26, 0.26 · trap 1
Driver: The published measure is a mean across respondents of each respondent's diary-week mean, counting only journeys ending in the usual workplace zone or a neighbouring zone; the journey-level mean over all work journeys returns 24 of 32 published means and names a different cause.
Why it held: two moves, aggregation grain and a destination filter through a neighbour list, and the wrong tabulation produces a complete and internally consistent wrong grid; the solver shipped 24 of 32 and the wrong response.

**Cost-pressure reserve** · 0.29* · runs 0.30, 0.28, 0.21 · trap 1
Driver: An undocumented peer-analog forecast (five predictors, median fill, robust scaling, same-quartile peers, five nearest by distance, inverse-distance weights, a leave-one-out residual by quartile, an enrolment-weighted upper percentile) must reproduce eight signed values to six decimals before it is carried forward; a circulating persistence note points elsewhere and does not control.
Why it held: about eight coupled choices pinned by eight six-decimal controls; each run landed a different wrong winner because each kept a different non-reproducing treatment.

**Team plan allowance** · 0.32 · runs 0.27, 0.32, 0.32, 0.32 · traps 8, 18
Driver: The published per-seat series reproduces only when the denominator is rebuilt from status spells as billable days and a population is excluded through a three-hop hierarchy join to an agreements register; either move alone matches none of 36 published months and the obvious series matches 27.
Why it held: a conjunction whose halves score zero alone; the standard bars a series missing any month; the solver saw 27 of 36 and one run pasted the published values over its own.

**Crossing cycle certification** · 0.32 · runs 0.35, 0.27, 0.22, 0.29 · trap 1
Driver: An unprinted factor table is recovered from fourteen certified cells; the obvious single key reproduces ten with opposite-sign misses, and only a second key that is a property of a different entity reporting at the same site closes all fourteen and drops the cycle a tier.
Why it held: the missing dimension lives on another entity, not on the project list, so no refinement of the single key reaches it; the solver accepted 10 of 14 and certified a tier up.

**Stabilisation award** · 0.33 · runs 0.29, 0.27, 0.37, 0.29 · trap 1
Driver: A matched-reference construction (period-length screens, windows aligned to each state's own effective date, pool eligibility read at each pool member's own span end, profiles scaled by pool standard deviation, a greedy group build run jointly over all designees with a two-use cap) must return two prior certifications; running states separately, dropping the scaling or narrowing admission each moves the award.
Why it held: many coupled steps and controls from two closed cycles; the solver rejected the staff decoy, failed the controls, said so, and still named a winner.

**Endowment settlement** · 0.335 · runs 0.35, 0.32, 0.29, 0.32 · traps 4, 17
Driver: Unlabelled movements between two accounts are attributed by exact-amount pairing with an over-sized movement priced against the one outstanding advance, a procedure chosen only because it reproduces a closed sibling settlement; the aggregate comparison that suggests nothing is owed cannot see the outflows.
Why it held: one settled case is enough because the fix is a procedure, not a parameter; the solver never opened the sibling case and returned 0, 2,421 or 706,139.

**Continuity reserve** · 0.34* · runs 0.34, 0.32, 0.34 · traps 11, 1
Driver: After the observed-growth snapshot is rejected, the production forecast is a peer-analog treatment with a seed depth, a clustering coherence control, a per-state cap and inverse-distance weights, pinned by five certified references on both peer count and rate.
Why it held: the decoy was beaten by every run and carried no difficulty; the treatment's ten checkpoints were disclosed as 3 of 5 met and shipped anyway.

**Transload siting** · 0.38* · runs 0.18, 0.58 · traps 3, 1
Driver: A lost index is a six-rule composition (producing sector, a distance floor, weighting, a lane tonnage floor, a cell sample floor, a per-vintage mode-code map in which one code means a different mode in each survey year) applied in one order; only that composition returns nine retained values, and the memo's first-order share is barred by clause.
Why it held, with a flag: high-dimensional and order-dependent, but one of two runs reached 0.58, so the flip risk is real; the per-vintage recode is the move the near miss lacked.

**Custody restatement** · 0.38 · runs 0.41, 0.35, 0.35, 0.35 · trap 11
Driver: After two visible decoys (ranking on level instead of position, an allocation the standard bars) are beaten, the corrections themselves must be decoded from register entry values by the one fixed step that reproduces two prover controls.
Why it held: the quiet step sits behind the loud ones and has its own controls; every run beat both decoys and failed the decode the same way.

**Capital fund drawdown** · 0.40 · runs 0.40, 0.40, 0.38, 0.40 · trap 13
Driver: A scheduled-date field reproduces every paid certificate and every closed year because the office re-aligns a schedule once an award starts drawing, and is stale for the awards that have not; commencement is the later of two case items and programme months are constant by type, which moves the exhaustion year.
Why it held: the back-test passes by construction, so there is no arithmetic symptom; the forward population differs from the validated one on an axis the pack shows only in the case log.

**Capacity watch** · 0.44 · runs 0.44, 0.41, 0.39, 0.44 · trap 4
Driver: A words-only index is rebuilt as support held per registered grantee (awards live in any part of the year, valued at obligations to date, an exclusion applied on the base transaction) standardised against the entity's own prior cycles and against the field, pinned by 200 filed cells; booked-year, own-term and per-row variants reproduce 147 to 155.
Why it held: three coupled choices and a large control set; partial variants score high but not full, and the solver never tested its reading at all.

**Award extension residual** · 0.44 · runs 0.44, 0.31, 0.44, 0.42 · trap 13
Driver: Expenditure is cash posted rather than notes designated, and remaining draws post with a lag that differs by product type; the longer lag is recoverable only from a separate award's quarterly cells, and every supported lag pair returns the same residual.
Why it held: the second lag's evidence sits in a file about a different award, so a clean back-test on the visible product type feels like proof.

**Sector revenue outlook** · 0.455* · runs 0.37, 0.47, 0.44 · trap 3
Driver: The certified growth rate reproduces only on a core-revenue basis over a continuing panel above a size floor, and is then applied to the full-sector base rather than the panel's; the near-miss basis without the floor leaves residual differences against all eight subsector rates, and the raw extrapolation reproduces none.
Why it held, with a flag: two moves plus a base rule, but three runs only and the top run at 0.47 sits close to the bar.

### One run (2)

**Employment programme continuation** · 0.35 · one run · trap 1
Driver: An undisclosed comparison-group construction (parts drawn from a service model, a counting floor, a nearest-areas share, alternating application until stable, the comparison rate standardised to the site's base composition) must return 23 certified figures; a single-pass construction returns one and names a different site.

**Fiscal diagnostic selection** · 0.44 · one run · trap 3
Driver: An undocumented peer-benchmarked measure is a six-rule stack (a size floor, a same-state size band, widening below ten members, iterative set-aside of movers above the running median, a median benchmark) that must return sixteen transmitted entries, with a vintage fork that applies errata to the new cycle only.

### Coin flip (13)

**Match fund certification** · 0.54 · runs 0.74, 0.32, 0.34, 0.34 · trap 2
Driver: The certified unit is a funded budget period, present in no field and recovered by decomposing installment postings into runs matched to the one federal action whose amount times the rate equals the run total; award grain undercounts and action grain overcounts.
Why it gave way: one run found the population (then collapsed multi-period awards); the unit is a single reconstruction a run either attempts or does not.

**Hours screen retarget** · 0.59 · runs 0.17, 0.19, 0.17, 0.99 · trap 9
Driver: Every offered option fails (adopting funds the declining group, refusing is barred) and the repair is to flip the side of the posted cutoff, which the rule permits while barring a second cutoff; the briefing's pooled lift is the claimed and not the identified effect.
Why it gave way: one decision branch; three runs refused and one took the repair at 0.99.

**Outbound volume commitment** · 0.595 · runs 0.73, 0.46, 0.44, 0.25 · traps 7, 1
Driver: Three unstated conventions (scoring window, outbound basis, allowance form) are each pinned by reproducing a different filed figure, and the archived scorecard winner ranks last once the convention runs on the current window.
Why it gave way: the profile was reachable and the allowance window was one parameter; the top run got everything but it.

**Margin review flag** · 0.625 · runs 0.99, 0.26, 0.26, 0.25 · trap 12
Driver: The review-value formula is unwritten and recoverable only as the highest of six exposure-by-anchor views, pinned by coarse archive counts that the salient forty-case replay does not discriminate.
Why it gave way: several constructions pass the salient control, so the fix is one extra search step; one run took it and scored 0.99 on a 0.25-point margin.

**Average-grant fall** · 0.625 · runs 0.57, 0.13, 0.09, 0.68 · trap 5
Driver: A grant is one grantee's support per programme per year with decisions aggregated and the organisation's own sponsored payees excluded; only that basis reproduces 24 published figures, and it moves the drill leaf.
Why it gave way: the basis is findable by testing against the published series; two runs scored 0.57 and 0.68 against 0.13 and 0.09.

**Withdrawal feed selection** · 0.655 · runs 0.34, 0.97, 0.34, 0.31 · trap 7
Driver: A polished scorecard favours one feed on measures that reset each date; the governing loss is cumulative within period and asymmetric, pinned by six historical certified periods, and it flips the selection.
Why it gave way: a single definition from a short list of standard loss forms; one run tried it.

**Extended-hours calendar** · 0.655 · runs 0.95, 0.32, 0.35, 0.36 · trap 4
Driver: An unstated averaging window is recovered by replaying two past calendars month for month; the natural trailing and calendar windows reproduce neither.
Why it gave way: a window is one scannable parameter, the dead shape in `../strategies.md` (Parts 1 and 6, our own measured builds) Part 4; the run that replayed scored 0.95.

**Loading-constrained year** · 0.665 · runs 0.45, 0.38, 0.88, 0.37 · traps 8, 9
Driver: Three natural shortcuts (month assignment, carriage basis, footing timing) and an unassigned pair of set figures jointly reproduce none of eight lifted readings; the prompt's withhold option is the trap because a reproducing method exists.
Why it gave way: the escape hatch sat in the prompt and the note records the withheld call; one run at 0.88 searched to completion.

**Distributor allocation** · 0.68 · runs 0.80, 0.56, 0.49, 0.41 · trap 15
Driver: The written schedule counts shipments less returns with no inventory adjustment, so the requester's doubt about a stock build is context and the attainment holds as written; netting it out drops a tier.
Why it gave way: the correct answer is the natural computation and the difficulty is resisting a framing, a confirm-the-number shape one run took at 0.80 and one our Gate G reads with suspicion.

**Suppressed-rate headline** · 0.685 · runs 0.53, 0.48, 0.84, 0.46 · trap 24
Driver: Suppressed cells are bounded from a published aggregate and its other component because the aggregate lies between its parts, which overturns two draft lines and selects the headline.
Why it gave way: one bounding insight; the run that had it scored 0.84.

**Included allowance** · 0.705 · runs 0.53, 0.88, 0.47, 0.53 · trap 9
Driver: Every slate option fails one of three conditions and the policy admits any whole thousand; revenue is non-monotone in the allowance because of a rate-card band edge, so the only admissible value is off-slate between two failing candidates.
Why it gave way: one run searched off the slate; the others chose the least-bad candidate.

**Pilot state and category** · 0.715 · runs 0.44, 0.47, 0.94, 0.49 · trap 16
Driver: A 0.15-point margin is smaller than the shift from any of three documented processing shortcuts (leaf coverage across two files, reference-month window, quintile assignment rule), so one shortcut flips the winner.
Why it gave way: a thin margin makes the stump a coin flip on processing discipline and a determinism risk; the exact run scored 0.94.

**Leading origin** · 0.955 · runs 0.98, 0.18, 0.93, 0.15 · no catalogue entry
Driver: Persons are attributed to the district a register places them in at the reference date rather than the from-address on the relocation return, and a reliability threshold then excludes the largest mover.
Why it gave way: one attribution choice between two files; two runs made it, and the top two sits near 1.

### Leaked (13)

**Cross-dock award** · 0.51 · runs 0.51, 0.42, 0.51, 0.49 · trap 10
Driver: The throughput leader breaches a sortation ceiling derivable only as the lowest overcapacity-coded volume in an incident log, which disqualifies it and changes the runner-up.
Why it leaked: the ceiling is one clause applied last, after a ranking table and a chart that bank credit with the wrong winner.

**Allocation-treatment package** · 0.515 · runs 0.47, 0.53, 0.47, 0.50 · traps 12, 15, 20
Driver: The settled replay is reproduced by both candidate treatments and cannot pick one; a dated ratified register row resolves the active window, and ranking the driver needs an isolated counterfactual the component tables never state.
Why it leaked: the treatment in force was identified, which earned credit, and the actionable funding package was chosen; a page with many certifiable items banked half without the driver call.

**Recovery schedule yield** · 0.52 · runs 0.52, 0.52, 0.52, 0.52 · trap 10
Driver: Recoverability is a timetable constraint (one place per period) run as a filed offer walk over every short student, including the unhelpable ones who still consume places; area-by-area counting overstates it.
Why it leaked: the wrong headline (121 against 102) with four identical scores, and an eight-sheet workbook whose historical, outside-credit and registrar sheets are independent of the walk.

**Administration charge** · 0.54 · runs 0.54, 0.54, 0.53, 0.54 · trap 22
Driver: A charge that counts as part of the base it is charged on needs a fixed-point solve with a ceiling; one pass puts nobody at the ceiling and shifts the pool onto the wrong participants.
Why it leaked: the decisive step is the last step of an otherwise correct chain (learner base, tiers, floor, replay), so the wrong headline still carried 0.54.

**Productivity indicator** · 0.54 · runs 0.53, 0.53, 0.55, 0.52 · trap 21
Driver: Eligibility is re-tested on a restated output basis while completeness screens stay fixed; a cautious extra screen holds four qualifying blocks and moves every published ratio.
Why it leaked: the committed figure and block count were wrong (17 blocks against 21, which moves every ratio and coverage figure) while the decision word and the population accounts that tie banked the credit; over-exclusion on a gate is a judgment the rubric half forgave.

**New-vertical pod** · 0.56 · runs 0.44, 0.60, 0.52, 0.42 · traps 5, 23
Driver: The serviceable market includes a class of agencies a docket's officer-count filter drops, and whether that class is sellable is settled by following billing across a product closure to its successor.
Why it leaked: the solver found the dropped class and argued it away, and the sizing of the other two verticals banked credit with the wrong pick.

**Lifecycle campaign** · 0.565 · runs 0.54, 0.58, 0.54, 0.55 · trap 11
Driver: After the visible decoy (a dormant list that is an artefact of missing log coverage) is killed, the winning audience is recoverable only by unioning two log deliveries, excluding a mirror collector and repairing malformed rows through a session table.
Why it leaked: the wrong campaign funded (one of two rivals, across runs), yet killing the decoy and the supporting numbers earned most of the memo's credit.

**Activation stall** · 0.585 · runs 0.49, 0.68, 0.48, 0.49 · trap 6
Driver: The remedy splits one uniformly labelled segment three ways on attributes reachable only through a provider bulletin, a grant audit and a security clause, and leaving the residual part untreated lowers the committed landing.
Why it leaked: the cause, the composition effect and two of three parts were found, so a mostly right shaped call banked most of the credit.

**Welcome-kit order** · 0.62 · runs 0.62, 0.59, 0.58, 0.62 · trap 18
Driver: Status grades on merchandise value rather than paid amount, and a material share of qualifying orders sits under one-off guest records linked to members only by a phone-credited ledger posting.
Why it leaked: the wrong kit count recorded (1,143 against 1,298), while tier counts, migration figures and the winback list banked 0.58 to 0.62 on their own.

**Investigation workstream** · 0.63 · runs 0.54, 0.54, 0.55, 0.71 · traps 7, 14
Driver: The coarse funnel stage the data offers points at a decision gate; splitting it at an interior review event shows the loss is entry into review rather than the decision, which changes the funded workstream.
Why it leaked: the wrong gate funded, and a one-deliverable note shape gave credit for the diagnosis around it.

**Seat plan** (our task62) · 0.68 · runs 0.68, 0.68, 0.68, 0.44 · trap 6
Driver: Expiring channel seats land on their accounts' own open lines and not on lapsed ones, so the committed base adds only the open-line share; the recorded commit was the base plus the signed book.
Why it leaked: the wrong call at 43,960 still banked 0.68 in three runs (the note gives no run split; three identical scores are consistent with the same commit), because the closing base, the contract book and nine printed checks were correct and collected without it.

**Contraction attribution** · 0.735 · runs 0.60, 0.71, 0.76, 0.66 · traps 7, 20
Driver: Component growth rates mislead until weighted by size with imports signed negative, and the deciding comparison (domestic demand total against net trade total) is never stated by a response that reports components row by row.
Why it leaked: the wrong country named and 0.60 to 0.76 banked, because the screen, the contributions and the audit workbook were right.

**Block-contract capacity** · 0.79 · runs 0.79, 0.79, 0.73, 0.23 · trap 10
Driver: The demand model is correct and the answer is the lower of demand and the beds that will still be registered after dated deregistrations, because the brief forbids contracting beds that will not exist.
Why it leaked: the uncapped figure committed (946 against 899, one run seeing the cap and declining to apply it) and 0.79 banked twice and 0.73 once, because the per-year series, the four circulating figures priced and the settled-versus-forecast split were independent of the cap.

### Landed (3)

**Helene anchor county** · 0.63 · runs 0.70, 0.56, 0.44, 0.50 · trap 3
Driver: The terms admit several readings and only the one with a pre-storm comparator screen and a cross-state adjacency ring returns all eight restated rates; the winner survives most readings and the gap halves.
Why it landed: the decisive rule moved only the runner-up and the margin, so the call was reachable on relaxed readings in three of four runs.

**Campaign merge** · 0.715 · runs 0.71, 0.72, 0.55, 0.45 · trap 25
Driver: The dated change everyone can see explains a minority of the rise once the unswitched trend is netted; the driver is duplicate targeting sets found by grouping on four attributes rather than by name, priced from the account's own past merges in the change log.
Why it landed: the bid-revert decoy was rejected in every run and the merge call made in most; only the premium's size and the set count were lost.

**Opening allocation hold** · 0.75 · runs 0.81, 0.60, 0.68, 0.69 · trap 26
Driver: The comparable window starts after a documented confounder ends, which turns a decisive-looking interval into one spanning zero; the hold survives either window.
Why it landed: the call follows from materiality regardless of the window, so the window only changes an interval that is never graded alone.

## Part 2. What separates the 18 from the 29

**The mean hides the verdict.** The client's mean of 0.45 for the extended-hours calendar and 0.54 for the leading origin both read as stumps. Their top two are 0.655 and 0.955. Any rung drawn from `../strategies.md` Part 5 has to be checked here first, because the catalogue counts a trap as decisive when it cost the mean. Only eleven of its twenty-six traps (1, 2, 3, 4, 8, 11, 13, 14, 17, 18 and 19) have a held task behind them; the other fifteen are carried, among the 49 recorded, only by tasks that gave way.

**Held tasks are compound, or outside the hypothesis space.** The eighteen take six forms. A conjunction of two independent corrections where a partial fix scores no better or worse (cover schedule, team plan allowance, field-support cycle, journey-time cause, sector outlook, capacity watch). A dimension that lives on a different entity or in a different file (the crossing cycle's second key, the drawdown's case items, the extension residual's quarterly cells, the level-mix summary file). A unit composed from finer rows by a rule the grain hides (stalls by adjacency, eligible units by person composition, arrivals from order lines). A procedure chosen against a settled sibling case (the endowment pairing). A treatment with four to eight coupled choices pinned by many exact controls (cost-pressure, stabilisation, continuity, transload, and both one-run tasks). A quiet decode behind beaten decoys with its own controls (custody restatement). What they share is that the solver cannot enumerate the fix. It recognises the mismatch, reports it as a caveat, and ships, because the next hypothesis is not on its list.

**Coin flips are one choice the solver does enumerate.** A window (extended hours), a scoring window (outbound volume), a loss definition (withdrawal feed), which side of a cutoff (hours screen), an off-slate search (included allowance), a bounding argument (suppressed rate), which of two files to attribute by (leading origin), a counting basis testable against a published series (average grant), a reconstruction a run either attempts or not (match fund), one search step past a salient control (margin review), persistence past an escape hatch (loading year), resisting a framing (distributor), processing discipline on a thin margin (pilot). Controls do not save them: the withdrawal feed had six certified periods, the average grant 24 published figures, the extended-hours calendar two full past calendars. The dimensionality of the fix decides, not the size of the control set. This is the measured form of the dead shape in `../strategies.md` (Parts 1 and 6, our own measured builds) Part 4, a recovered rule that is one scannable parameter.

**Leaked tasks put the decisive step last.** In every leaked task the client's note records the wrong committed figure (in every run, where it counts them) and the top two still banked 0.51 to 0.79, because the decisive step (a cap, a fixed point, a timetable walk, a three-way split, a phone-credited link, a stated comparison) sits downstream of most graded figures, which were right. In the held tasks the decisive step is the definition of the unit, the population or the measure, upstream of everything, so every downstream figure inherits the wrong unit. Our own task62 and task78 sit in this group (Part 4).

**Landed tasks had their difficulty in a margin or an interval.** A rung that moves only the runner-up, the gap or the confidence interval leaves the call reachable, and a reachable call banks about 45 before any ask is answered (`../../../supplemental-stumping/SKILL.md` Part 0).

**Decoy artefacts carried nothing.** Every held task that shipped a staff first look, a snapshot, an indicative schedule or a circulating note saw the solver beat the decoy (stabilisation, continuity and custody in every run the note counts; cost-pressure in all but one) and lose on the construction. This is the measured form of Gate G: refuting a surface read is spent difficulty, and a build whose stump is the decoy has no stump.

**The run spread is the diagnostic.** Held tasks with four runs spread 0.21 or less; coin flips spread 0.38 or more. In-house, a round where one solver lands the call and the others do not is the coin-flip signature, and it reads as a fail under the top two, not as a near pass under the mean.

## Part 3. What this adds to the draw

1. **Draw the decisive rung from a trap with a held task behind it** (1, 2, 3, 4, 8, 11, 13, 14, 17, 18, 19). The other fifteen traps in `../strategies.md` Part 5 cost the client's model its mean and never held under our bar in any recorded task, so a rung drawn from one of them is a bet and the design note says why in one line.
2. **Write the partial-fix match counts into the design note before the pack is cut**: the obvious construction, each correction alone, and the conjunction, each against the control set. The cover schedule reads 19 of 24, fewer, fewer, 24 of 24; the team plan reads 27 of 36, 0, 0, 36. If a single correction improves the match, the landscape is climbable and the build is a coin flip.
2. **The decisive move must be one the solver does not enumerate**: a key on another entity, a unit composed by a rule the grain hides, a procedure learned from a settled sibling case, a conjunction of two corrections. A window, a lag, a threshold, a standard definition, a cutoff side or a choice between two files is enumerable and is a coin flip however many controls pin it.
3. **Put the decisive move upstream of every graded figure.** List the graded figures and mark which change when the decisive move is undone; every one should. If the move is a cap or a last-step solve, the asks leak around a wrong call, which is the shape of every leaked task and of our own task62 and task78.
4. **A control set makes the stump fair, not hard.** The held tasks carry 14 to 36 exact cells, or 200, and that size is what makes "most of them" visible and inexcusable. One settled sibling case held (the endowment) because the fix was a procedure; 24 published figures gave way (the average grant) because the fix was a basis.
5. **A decoy artefact is furniture.** Ship it when the world would have one, never as a rung, and never let it be the only wrong thing in the pack.
6. **Margins under about half a point of the graded quantity turn the stump into a processing coin flip and a determinism risk** (the pilot at 0.15 points, the anchor county at 0.36, the margin review at 0.25). Widen the gap or move the decision to a quantity where the construction's effect is large.
7. **Read the in-house rounds for spread, not for the mean.**

## Part 4. Two of these tasks are ours

The client's 64 measured tasks include two of this repo's shipped builds. task62 is the seat plan at 51,220 seats, listed in the client's Economics file with runs 0.68, 0.68, 0.68 and 0.44; the note records the committed figure as 43,960 with the feed lure resisted in all four runs and gives no run split, and the three identical scores are consistent with the same commit. task78 is the 3,642 planned maintenance visits, listed under trap 4 in `../strategies.md` Part 5 at a mean of 0.59 with the model committing 3,327; its run list was not recorded. Both read as leaked: the wrong committed figure recorded, and most of the score banked around it. The shipped ledger carries no portal row for either, and none is written from this file, because a ledger row records what the author reports from the portal; but the client's measurement is the portal measuring both.
