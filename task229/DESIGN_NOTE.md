# task229 design note

Seed DQ02 (whether the release-health alert fires on this week's build, when the metric is the
average user's rate). The seed's pairing was product-analytics; task228 is being built the same day
in the same objective inside the product-analytics experiment-platform world, so this build keeps the
seed's objective and moves the world to a smart-meter metering data provider, where the object under
analysis (interval data delivery) is the health of the data itself.

**Where the build stands.** Shipped (stage 8) on architecture 1, hardening loop 2. Round 3 passed the
worth-it gate (recorded as a pass under the single-solver rule of PR #17: no solver committed to the
main call), and the determinism judge's first pass on the loop-2 cut returned DETERMINISTIC with
APPROVE (`## Determinism check (stage 7)`). Round 1 had both solvers execute the filed mean and
the filed installation-level error and land the call. Loop 1 moved the decisive rung to the unit the
build's standard error is built over, which no clause can carry: round 2 had both solvers miss the
call at exactly that step, and the ask layer leaked. Loop 2 hardened the ask layer and closed an
outage carve-out route the leak reader found; round 3 had both solvers, and the leak reader solving
on its own, miss the call at the same step (`## Solver rounds`).

## DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | Energy Systems & Utilities / other (smart-meter interval data delivery quality, the metering data provider's read performance; the client list carries no energy task type that serves Data Quality Monitoring) |
| Objective | Data Quality Monitoring & Alerting |
| Niche | a smart-meter data provider's read-health gate on the communications-module firmware builds live in its fleet, deciding which builds the read-health alert fires on before the next rollout wave |
| Shape | 10 scorecard against thresholds: eight builds, each with read health, its standard error, lower limit, distance from the limit and fire or hold, plus the Wave 8 moves and the Settlement substitution load under the call |
| Decision type / unit | designation_set (which builds the alert fires on) / set_of_items |
| Gap / pattern / generators | population (decisive: the unit the noise lives in is the comms node the installations share, not the installation; the file grain is the register-day delivery), time (the delivery cut-off as of which a read counts); pattern D (two grains, both flawless: installation and node); G2 grain mismatch, G7 operating window, G12, G17 statistical rigor |
| Gate G mechanism | signal_vs_noise_or_hold (which builds sit below the reference by more than their own noise; five of eight hold, two of them on the noise their shared nodes carry) |
| Stump strategy | grain_or_unit; decisive rule filed (the standard defines the measure, the reference and the three-standard-error limit); the step that turns the rule into the answer (the unit the error is built over) is in no sentence, and no sentence states or implies a rival unit; no official decoy; no validated decoy; no calibration organ |
| Layer 2 | estimation_fit, `survey-research-official-statistics/complex-survey-estimation-variance/1` (variance must reflect the primary units; a simple-random-sample formula on the respondent count understates it severalfold for clustered items), made this build's own: the primary unit is the mesh collector or access point, because a node that misses a night's collection takes that day from most of the installations behind it at once, and firmware waves are pushed node by node, so a build's installations are concentrated behind few nodes |
| Layer 1 | interval reads with quality codes at mixed 5, 15 and 30 minute resolution; register-days re-delivered when a later retrieval completes them, and days the MDM held nothing for until its estimation run; receipts in UTC, market time in AEST, field times in AEDT, against a filed cut-off; firmware build codes spelled three ways; effective-dated meter-to-installation assignments with mid-week exchanges; head-end events replayed after a failover and failed activations rolled back; each meter's comms parent in the head-end record with the date it joined |
| Calibration form | none, because the strategy is a stated rule whose construction is the work; no closed corpus is needed or shipped |
| Context artifact | filed_standard (the read-health standard MDS-STD-114 the gate runs on; redrawn from monitoring_export once task228, drawn earlier the same day, took that type) |
| Stakeholder | metering data services lead, who owns the read-health alert the rollout desk gates each wave on |
| Forum / forcing event / org family | operations_desk (the rollout desk holds the wave for any build the alert fires on) / cutover_or_migration (Wave 8 of the firmware migration goes out on Tuesday night) / utility_or_infrastructure |
| World | Halvane Metering, an accredited metering provider and metering data provider in the National Electricity Market, New South Wales, AUD; personas drawn with `guard.py names --locale en_AU --seed 229` |
| Deliverables | `wave8_read_health_alerts.json` (the alert payload the routing system ingests: commits), `read_health_by_build_wk41.png` (reads at a glance) |
| Guard | heart WARN on repeat.gate_g against task228 (answered below); NOTE same_puzzle_older against task98 v3, differentiated on the card; nearest driver 0.06 (task87 v3), nearest heart text 0.04 (task114); adjudicated pre-flight on the loop-1 driver CLEAN (`clone_check_report.md`) |

**WARN repeat.gate_g (task228), answered.** Both builds label their Gate G mechanism
signal_vs_noise_or_hold because both are alerting calls; task228 picks which metric an alert should
watch from a replay of past check nights (one of N), task229 constructs one stated measure and the
error that measure carries on a network whose nodes fail together, and designates the builds that
breach. The decisive constructions share nothing.

**Coordination with task228.** Drawn the same day in the same objective. task228 holds the
product-analytics experiment-platform guardrail world; this build differs in domain (energy
utilities), organisation (a metering data provider), forum (the rollout desk), forcing event (a
firmware migration wave), geography (New South Wales), personas (en_AU draw), data structure
(register-day deliveries of interval counts by quality flag, an activation history and a two-mesh
topology), stump strategy (grain_or_unit on the unit of the error) and context-artifact type.
task228's card is copied into this build's cards folder so the guard sees both. The prompt avoids the
six idioms the corpus over-uses (a named colleague's belief about the naive pick, a closing role line,
"what I need is", a chart title asked for last, the pick marked on the chart, the runner-up beside the
pick).

**Data-native sentence.** An AMI mesh collects every meter's day through a collector or access point,
and when a node's backhaul or power fails overnight the day of most of the meters behind it misses the
MDM's cut-off together; firmware waves are pushed node by node, so a build's installations sit behind
few nodes, and on this fleet a build's weekly read health is a draw of its nodes' nights, not of
independent installations, which is exactly the independence a capable analyst assumes when the
standard says "standard error" and the population is a list of installations.

**Why every element is real.** NEM metering data providers deliver interval data with quality flags
(actual, substituted, estimated) by register and day, re-deliver a day when a later retrieval
recovers the reads, and work in market time (AEST) while field crews and the head-end log local or
UTC time; RF mesh head-ends record each meter's parent node, collect the day overnight and backfill a
node's meters when it comes back; firmware is downloaded through the node, so waves go node by node,
with a go/no-go per build.

## Stump sentence

A competent solver executes MDS-STD-114 to the letter (installations whose meter ran a build all week,
reads held at the 06:00 AEST cut-off against every expected interval of every stream, the mean of the
installations' read health) and gives that mean the textbook standard error, the sample standard
deviation over the square root of the installation count: the alert fires on EM3.10.9, EM3.12.0,
EM3.12.1, EM3.12.2 and PX5.2.7, Wave 8's 1,274 moves onto EM3.12.2 stop, and Settlement Operations is
warned of 5,379 installations. The step that carries the stump is the unit of the error. The EM3.12.2
installations the standard assesses were piloted on seven collectors, and on Thursday 8 October one of
them (EMC-8631) missed the night's collection and its backlog reached the MDM after 10:16 the next
morning, so 20 of its 23 EM3.12.2 installations held nothing for that day at the cut-off, together; two
collectors in the newer suburbs did the same to 121 EM3.12.0 installations on the Monday and the
Sunday. A build's read health therefore moves with its nodes, not with its installations: built over
the collectors and access points the installations report through, EM3.12.2's standard error is 1.83
(not 0.40) and EM3.12.0's is 0.57 (not 0.09), both hold, and the alert fires on EM3.12.1, EM3.10.9 and
PX5.2.7 only, whose shortfalls are spread across their nodes and fire on either error.

## Gate G

- **Litmus.** No reported number or stakeholder conclusion is overturned. The pack carries no
  read-health report, no scorecard and no ranking of the builds; the MDM receipts, the head-end
  history and the register are correct records of what happened, the node failures included (they
  are real reads that were not held, and the standard counts them on purpose). The prompt carries no
  stakeholder belief. The difficulty is constructing the measure and the error the standard defines:
  the unit, the population, the version, the expected reads the deliveries do not carry, and the unit
  the error is built over. Answer: no.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Primary mechanism:** signal_vs_noise_or_hold (which builds sit below the reference by more than
  their own noise), with `statistical_rigor` support (the error built over the units that fail
  independently). The unit itself is Pattern D, two grains both flawless: the installation and the
  node.
- **Deletion test.** Nothing in the pack is wrong; there is nothing to delete. Still hard because the
  installation-level error and the node-level error are both arithmetically perfect and disagree on
  two builds.
- **Clean-data test (asserted).** Repair the Layer 1 mess on the main path (replayed head-end events
  removed, the first-delivery and latest-delivery versions set aside for the cut-off version, every
  register-day given its expected intervals): the answer does not move and the installation-level
  answer does not move, and they differ. The node failures are not a defect to repair: they are reads
  that did not reach the MDM by the cut-off, the standard's own measure; an instrument that dropped
  them would be measuring something the standard does not score.
- **Lens-swap test.** The naive reading and the answer are not one population at one moment: the
  natural pipeline takes 7,930 installations on their end-of-week build with the latest deliveries,
  pooled; the answer takes the 6,729 that ran one build all week, the deliveries held at each day's
  cut-off against every expected interval, the mean, and an error built over 3 to 53 nodes per build.
  The last rung is not a re-reading of a stated figure: no figure is stated, and the unit of the error
  is decided by the data's own dependence (below), which is estimation, not a definition.
- **Forward framing.** The measure is of the week just closed, which is what the standard scores;
  the decision is forward (Wave 8 moves nothing onto a build the alert fires on). A Data Quality
  Monitoring call is a gate on the next action, and its evidence is the last complete window by
  design.

## Stump or fork

Both round-2 solvers missed the call at R4, and both said why they never used the node field: "the
planned-interruption and comms_parent data were not used because the standard sets no exclusions for
them". They read the node as a candidate exclusion, which the standard rightly gives them no licence
for, and never as the unit their error rests on. The miss is a stump and not a fork, because the
pack's own structure refutes the one premise R4 needs and every reading that respects that structure
lands the golden call (all asserted in `checks.py`):

- **The premise is refuted by the files.** R4's sample SD over root n is the standard error of a mean
  only when the installations vary independently. Outside the four node failures, an installation
  loses a whole day at the cut-off on about 0.14 per cent of node-nights' installation-days; on the
  four failed node-nights 80 to 95 per cent of the installations behind the node lost that day
  together, with binomial tails under independence of 10^-159 to 10^-209. No other node-night loses
  the day for more than 3.3 per cent of its installations.
- **Every dependence-respecting reading lands the call.** Grouping the installation-day panel by node,
  by node-day, by day, or two ways by node and day all fire EM3.12.1, EM3.10.9 and PX5.2.7 and hold
  the other five, as do the node error without the small-sample factor and the delete-one-node
  jackknife. Only the readings that treat installations (or reads) as independent fire EM3.12.0 and
  EM3.12.2. The figures are those of the node grouping on the installation-week shares, which is the
  unit 4.1 defines and the grain that nests every dependence the data show (an installation's own
  days, and the installations behind one node).
- **The size of the error the premise costs.** The node-level standard error is 4.6 times the
  installation-level one for EM3.12.2 (1.83 against 0.40) and 6.1 times for EM3.12.0 (0.57 against
  0.09); for the builds whose nodes did not fail the two agree within 15 per cent.
- **The judge's residual is not a second answer.** The judge found one estimator that moves a build:
  the standard's simple mean paired with a random-intercept variance, (σu² Σm² + σe² n) / n², gives
  EM3.10.9 a standard error of 0.65 against the 0.48 it needs to hold. It did not count it as
  licensed, and the data say why. The model gives every node one common spread of node effects,
  estimated from EM3.10.9's many small nodes (most hold one to six installations, and their means
  scatter widely, the failed EMC-8631 among them). It then charges that spread to the few large nodes
  by size squared, though their means sit close to the build's 98.06 (the ten largest, 22 to 36
  installations each, at 97.67 to 99.58). The full random-intercept fit applies the same model to the
  mean as well: it gives 97.44 with a standard error of 0.46 and fires EM3.10.9, as does every
  design-based estimator. The figures are asserted or printed by `checks.py` with a moment estimator,
  which reproduces the judge's.

## Why the standard files three standard errors and not their unit

- **What MDS-STD-114 files** is what an organisation decides: the population (3.7), the measure and
  its window (3.2 to 4.2), the reference (5.1), the decision rule (5.2, 5.3: fire below the reference
  less three standard errors of the build's read health), the routing (6) and the reporting
  convention (7, sample spreads with the n minus 1 divisor). A standard error is not an organisational
  choice: it is the standard deviation of that estimate under the process that produces the week's
  reads, a defined statistical quantity, so the rule is complete as filed.
- **Why a real standard stops there.** The estimator depends on how the week's reads were produced,
  and on this network that changes every wave: a wave re-homes builds node by node, so which nodes a
  build sits behind, and how many, is a fact of the week, not of the standard. Control-limit standards
  work the same way (a Shewhart chart is specified as three-sigma limits and the analyst chooses the
  rational subgroups from the process; a release canary gate names the confidence level and leaves the
  test to the analytics team). MDS's own revision history shows what this organisation revises the
  standard for: the reference and the cut-off.
- **What was taken out, and why it was not a rule.** Revision 3 in round 1 carried "The standard error
  treats the week's assessed installations as a sample of how the build behaves in the field". It
  named no unit and no independence, but on this network it reads as an instruction to treat
  installations as independent draws, which would make it a filed sentence pointing at the wrong
  answer: the official decoy the guard bans, and with the unit unstated, the withheld-rule-with-decoy
  shape. Removing it leaves no stated rule that conflicts with the golden. Nothing is recovered from
  certified or published figures (there are none), and the method follows from the definition of a
  standard error and the dependence the files show, not from a sentence the pack hides.
- **The card says so.** `decisive_rule_filed: true` (the rule that decides is in 5.2 and 5.3);
  `official_decoy: false` (no sentence states or implies installation-level independence); the
  card's notes record that the unit of the error is a construction the data force.

## The outage carve-out route (leak reader, round 2)

The reader found that setting the four node failures aside and keeping the installation-level error
landed the committed fire list, with EM3.12.0 within 0.006 of its limit. Two closures, both now in
place:

- **The pack rules the route out.** 3.3 counts every interval of every data stream metered in the
  week, and no clause excuses any cause; 3.5 says only reads held at the cut-off count. Both round-2
  solvers declined to exclude anything on exactly that reading, and the reader itself notes that no
  document states the carve-out. It is a reading that violates a filed clause, not a fork.
- **The route no longer lands by luck.** EM3.12.0's own firmware gap and outage rates were raised
  (0.074 and 0.029 to 0.085 and 0.035 a day and a week), so its shortfall without the node failures
  sits clearly under its installation-level limit: every carve-out variant (failed node-days dropped,
  the node backlog counted as held, installations behind failed nodes dropped) fires EM3.12.0 by 0.15
  and files a wrong set (asserted). The golden still holds EM3.12.0 by 0.41.

## Solver rounds

| Round | Cut | Plain | Skeptic | Decision |
|---|---|---|---|---|
| 1 | architecture 1 as first built | landed, 91.3 | landed, 87.4 | harden: the decisive step was a filed formula |
| 2 | loop 1 | missed at R4, 54.5 | missed at R4, 54.5 | harden the asks: read for the facts each kept about 37, no margin under 40 |
| 3 | loop 2 | missed at R4, 47.0 | missed at R4, 43.4 | pass (recorded under the PR #17 single-solver rule: the main call missed; proxy recorded) |

Rounds 1 to 3 ran under the two-solver rule (plain and skeptic, mean proxy at most 40). PR #17 replaced
it while the judge was reading the loop-2 cut: a round is one isolated solver in a sandbox, it passes
when the solver does not commit to the main call, the proxy is recorded and does not gate, and
whether a different answer is a stump or a fork is the determinism judge's question at stage 7.
Round 3 is recorded as a pass under that rule: neither solver, and not the leak reader solving on its
own, committed to the golden fire set. No hardening loop 3 ran for the proxy. The record below is the
round as graded under the old rule, kept for the judge and the portal.

1. **Both solvers miss the main call.** Both filed fire on EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1 and
   PX5.2.7 with "SE = sample SD (n-1)/sqrt(n)" and no use of `comms_parent`, and both stopped Wave 8
   onto EM3.12.2. The round-3 leak reader, solving on its own, filed the same five fires and tried a
   cut-off sweep, AEDT, a pooled error, the build at the week start, dropping missing or estimated days
   and excluding the four failed collectors (EM3.12.0 still fires there, at minus 0.15), and never an
   error over the nodes.
2. **The proxy (recorded, no longer gating): the pair stays under 40 on the facts.** Read for what each solver filed, each kept 17 of 51 ask
   criteria (the read-health figures, six of the eight per-build alerts, PX5.3.1's Wave 8 figure and
   the chart's points and reference line) and lost every standard error, limit and distance, both
   lists, the order, EM3.12.2's Wave 8 figure, the substitution load and the chart's title, order and
   ticks: about 31 each. By grade.py's own cracked-item count (one of four items each) the pair
   arithmetic gives about 27. grade.py's decimal (47.0 and 43.4) is inflated by its matcher, which is
   the reason the skill reads the facts rather than the decimal: it accepts a number within 0.5 per
   cent of the golden (about 0.49 points on percentages near 99, so 98.89 passes for 98.40), matches
   numbers anywhere in an answer rather than on their build, credits the eligible 1,274 the solvers
   quoted beside their committed 0, and scores a capitalised word in the load item. With the
   tolerance at the prompt's rounding the decimals are 44.5 and 40.8 (`solver_rounds/round-3-*.md`).
3. **Every miss is a stump on the main thread's read** (`## Stump or fork`; the judge rules on it): the
   files refute the independence R4 assumes, and every dependence-respecting grouping lands the golden
   call. The judge agreed (`## Determinism check (stage 7)`).

## Determinism check (stage 7)

Pass 1, an isolated judge on the loop-2 cut (`determinism_check_report.md`): **DETERMINISTIC, APPROVE**,
Gate G passes (`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`). It rebuilt the chain from the ten files and
reproduced every figure in the four graded blocks to two decimals. It found the four collector-nights
(77 to 100 per cent of the installations behind one collector losing the day, at most 3 installations
elsewhere), and all nine collector-aware estimators it tried, design-based and model-based, landed the
golden call. It judged the independent-installation error an analytical error, not a licensed
reading. Its notes, and what was done:

- **Grading tolerance.** A limit or distance worked from the two-decimal standard error moves by 0.01
  for EM3.12.1, EM3.10.9, PX5.3.0 and EM3.12.0. Step 6 of the write-up now says the limits and
  distances come from the unrounded error and names the four that move by 0.01 with no call changing.
- **Wording.** The recommendation called EM3.12.0 a deciding margin; the thinnest margins are PX5.2.7
  (0.23 below) and PX5.3.0 (0.13 above), and the recommendation now names those.
- **Container nits, fixed in the generator.** The standard's PDF named Microsoft Word as its creator
  over a ReportLab structure; it now names the records system that renders it (HVM Records, already
  its producer). The three workbooks carried openpyxl's layout (inline strings, calc id 124519, a
  two-field app.xml, explicit defaults) and one shared modified stamp. They are now laid out the way
  Excel saves a workbook (shared strings, calc id 191029, full extended properties, Excel's entry order
  and 1980 entry stamps), each with its own created and last-saved stamps in UTC, matching the extract
  log's local times. The golden's Wave 8 note said the schedule was cut on 1 October; batch B was
  rebuilt on 9 October, and the note now says so.
- **Nothing graded or read moved.** The rebuilt pack was compared with the judged cut:
  - the seven text files are byte-identical;
  - the PDF's extracted text is identical page for page and parses with no error logged;
  - every workbook cell value, type, number format, bold header and frozen pane is identical. The 239
    empty Wave 8 NMI cells that openpyxl stored as empty strings are now unstored, as Excel stores
    them, and still read as empty;
  - LibreOffice opens all three workbooks;
  - the goldens' figures, the 120 assertions and the verifier are unchanged, and two builds are
    byte-identical.

  No fresh round and no second pass are owed, since no graded figure, rung or document text a solver
  reads moved.
- **The judge's cross-batch duplicate check did not run** (its allow-list barred the batch folders).
  The duplicate check stands on stage 5 (heart and adjudicated pre-flight) and on the surface screen
  against task228 (`## Build record`).

**Reconciliation (main thread, after the verdict).**

- **Gate G.** The judge's three flags match this note's `## Gate G` exactly. Its mechanism label
  (method or model selection) is the judge's vocabulary for the move this note files as
  signal_vs_noise_or_hold with statistical_rigor support: choosing the unit of the error on honest
  data. Its stump-power paragraph calls it a signal-versus-noise call. There is no mismatch, and the
  judge names no distractor as the surface read.
- **Spec gates.** All pass:
  - 10 files in 5 formats, the largest at 95,140 rows;
  - two declared distractors, unused by the golden and named for nothing;
  - two deliverables;
  - every ask with its unit and rounding;
  - shape 10, at about 51 criteria.

## The decisive move, and why it survives the opponent

1. **Written in no sentence.** The standard defines the installation's read health, the build's read
   health as their mean, the reference, and the limit as three standard errors of the build's read
   health, with only the build's own assessed installations entering it, and sample (n minus 1)
   spreads. Nothing says what unit the error is built over, that installations behind one node fail
   together, or that waves go node by node. The field reference describes `comms_parent` as the node
   that collects the meter's reads, which is what the head-end field is.
2. **No sweepable corpus.** There is no prior read-health report, no published error, no closed
   corpus; nothing nominates a method.
3. **No arithmetic symptom.** The installation-level error is complete, plausible and internally
   consistent; read health is identical under both errors (only the error moves); every
   reconciliation ties. The node failures are counted the same way on either path.
4. **Not a per-row predicate.** It needs a group (each build's installations by node), the deviations
   summed within the group, and a spread across groups.
5. **Enumeration is arithmetic.** The node is a stored attribute; the move is not a filter on it but
   the decision that the error lives at that grain, which the data force and no clause states. Round 2
   shows the attribute alone does not hand it over: both solvers saw it and considered it only as an
   exclusion.
6. **No cutover date, and the dated events sit on the wrong side.** The node failures are four
   nights on four nodes; an event study on EM3.12.2's daily read health finds Thursday's dip, which is
   real and counted, and which is exactly what makes the installation-level error fire.
7. **Survives the deletion** (above).

**First-moves test.** The opponent's first moves (execute the standard; give a mean its textbook
error) land on R4: five fires and Wave 8 stopped onto EM3.12.2. Round 1's plain solver wrote exactly
that error, and both round-2 solvers filed it.

## Layers

- **Layer 1 (the realistic mess and the system that produces it).** MDM interval receipts at
  register-day by delivery grain with A, S, F and E quality counts at 5, 15 and 30 minute resolution;
  a later delivery replaces the register-day; a day the head-end collected nothing for has no version
  until the MDM's 06:30 estimation run and arrives when the node's backlog clears; UTC receipt stamps
  against a market-time (AEST) cut-off, while the register and the schedule are in local time (AEDT
  since 4 October); the head-end history as nested JSON with staging, failed activations, rollbacks,
  decommissioning, events re-stored after a failover, and each meter's comms parent with the date it
  joined; HES image ids that the catalogue maps to release names and the schedule spells a third way;
  NMIs with and without the checksum character; serials that lost their leading zeros in the register.
- **Layer 2 (the analytical shortcut).** Treating the assessed installations as independent draws
  when the standard asks for the standard error of their mean. An expert in survey or cluster
  inference recognises it: the primary units are the nodes, the effective sample of a build piloted on
  seven collectors is seven, and an error on the installation count understates the noise severalfold.
  Beneath it, the round-1 ladder stays as the lower rungs: the cut-off version, the register's expected
  reads (absence of a record is not a record of absence), the full-week population, and the mean of
  installations rather than pooled reads.

## Ladder (asserted by name in `generator/checks.py`)

Answer: fire on {EM3.12.1, EM3.10.9, PX5.2.7}, hold on the other five.

| Rung | Reading | Fires on | Killed by |
|---|---|---|---|
| R0 natural pipeline | latest delivery per register-day, every installation on its end-of-week build, pooled reads, binomial error on reads | EM3.10.9, EM3.12.0, EM3.12.2, PX5.3.0, PX5.3.1 | 3.5 (read held at cut-off) with 3.3 (every expected interval) |
| R1 | + reads held at the 06:00 cut-off against every interval of every stream (a register-day held nowhere counts zero) | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.0, PX5.3.1 | 3.6 and 3.7 (assessed installation) |
| R2 | + only installations that ran the build all week | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.0 | 4.2 (the mean of installations) |
| R3 | + the mean of installation read health | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.1 | 5.2 (standard error of the build's read health: reads are not independent draws) |
| R4 | + the error with each installation its own unit (sample SD over root n) | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7 | the node-night split: installations behind one node fail together |
| R5 | + the error built over the nodes the installations report through | **EM3.12.1, EM3.10.9, PX5.2.7** | answer |

- **How the round-1 brief is answered.** Round 1's landing step was R4 executed as a filed formula.
  R4 is now the step a competent solver supplies by habit, it completes, and it returns five fires and
  a stopped wave; R5 is built so that exactly that step is the wrong one, from the data's structure
  and not from a clause. Round 2 measured it: both solvers filed R4.
- **Partial applications.** Dividing by the register-days the MDM held at the cut-off (instead of the
  register's expected reads) makes the node failures vanish altogether (EM3.12.2 99.83) and holds
  PX5.2.7; the cut-off applied to rows alone in the natural pipeline holds PX5.2.7 and fires six
  others; every outage carve-out fires EM3.12.0 (asserted).
- **Satisfying to stop at.** R0 is the dashboard number every MDP reports; R1 is what a careful analyst
  who read the cut-off and expected-reads clauses files; R2 is the clause-by-clause population; R3 is a
  correct mean with the error a proportion invites; R4 is the correct mean with the error every
  textbook gives a mean, which both round-2 solvers filed.
- **Position.** Calls right per rung (of eight): R0 2, R1 4, R2 5, R3 5, R4 6, R5 8. No intermediate
  rung lands the call.
- **Discriminator dominance.** EM3.12.2: 97.87 against 98.30 on the installation-level error (fires
  by 0.43), against 94.01 on the node-level error (holds by 3.86). EM3.12.0: 98.21 against 99.22 (fires
  by 1.01) or 97.80 (holds by 0.41). The three builds that fire do so on either error by at least
  0.23, because their shortfalls are spread across their nodes (EM3.12.1's 695 installations over
  eleven collectors in the older suburbs, none of which failed).
- **Convergence (asserted).** The call is the same under the k/(k minus 1) small-sample factor, without
  it, under the delete-one-node jackknife, and for the node-day, day and two-way groupings of the
  installation-day panel; the installation-level error fires EM3.12.0 and EM3.12.2 under either
  divisor. No build's node-level error undercuts its installation-level error by more than 15 per cent
  (tuned), so the node grain only ever widens the noise where nodes failed.
- **Grid (asserted cell by cell).** 3 versions (cut-off, latest, first) x 3 populations (whole week,
  start-of-week build, end-of-week build) x 4 units (installation mean, pooled reads, register-day
  rows, data streams) x 6 errors (nodes with and without the small-sample factor, installations,
  binomial on reads, binomial on installations, none) x 2 denominators = 432 cells. Every cell that
  lands the call builds its error over the nodes; the ones other than the standard's reading take the
  first delivery of each register-day, which moves at least four builds' graded figures.
- **Sign discipline, margins.** Every build sits at least 0.05 percentage points from its limit, the
  distances to the limits are at least 0.04 apart (the payload's order is not a near tie), every
  two-decimal read health, standard error, limit and distance sits at least 0.0015 from its rounding
  edge, and each distance reads the same from the rounded figures as from the unrounded ones.

## Closure table (determinism-check, the 22 axes)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | installations whose meter ran the build all week | filed (3.7, 3.6); readings by start or end build are grid cells |
| 2 | Unit of account | the installation | filed (4.1, 4.2); rows, streams and reads are grid cells |
| 3 | Attribution window | market days 5 to 11 October | filed (3.2); the receipts carry only those read dates |
| 4 | As-of dating | the meter's build at the week start, no activation inside the week | filed (3.6, 3.7) |
| 5 | Version basis | latest delivery received before the cut-off | filed (3.5); first and latest are grid cells |
| 6 | Denominator | every interval of every data stream the register lists, every day | filed (3.3); the rows held at the cut-off are a grid cell; no clause excuses any interval, so an outage carve-out violates 3.3 (and files a wrong set, asserted) |
| 7 | Weighting | equal per installation | filed (4.2) |
| 8 | Window length | one week | filed (3.2) |
| 9 | Boundary inclusivity | received before 06:00; fire when strictly below | C1: no delivery lands within 8 minutes of a cut-off; no build within 0.05 of its limit |
| 10 | Rounding path | compute unrounded, report two decimals | filed (7); every figure clear of its edge; distances agree from rounded and unrounded figures |
| 11 | Tie-break | none needed | C1: no ties in the order (distances 0.04 apart) |
| 12 | Maturity | the week is closed and every cut-off has passed | C1: the extract is after Sunday's cut-off |
| 13 | Order of operations | share per installation, then mean, then the error | filed (4.1, 4.2, 5.2) |
| 14 | Row order | any | C1 |
| 15 | Duplicate resolution | head-end events by event id; deliveries by the cut-off rule | C1 for the population (replays change no assessed installation, asserted); filed for deliveries |
| 16 | Identity | NMI to 10 characters, serials to 8 digits | C1: the joins have one answer once normalised |
| 17 | Netting | not applicable | none |
| 18 | Dimensional units | interval counts only | C1: kWh totals are never used |
| 19 | Code semantics | A is a read; S, F and E are not; a rolled-back activation is not a move | filed (3.5, 3.6) and the field reference |
| 20 | Integerisation | counts are counts | C1 |
| 21 | Scope of a clause | the standard governs the alert; the Wave 8 ask and the substitution load are defined in the prompt and 6.1 | prompt wording and 6.1 |
| 22 | Forward window contents | Wave 8 moves under this week's call, on the schedule as cut | prompt wording ("once this call is applied") and 6.1 |
| + | Unit the error is built over | the node (collector or access point) each installation reports through | the data's structure: the independence test and the node-night split (asserted); every dependence-respecting grouping gives the same call (asserted); every assessed installation has one node and no assessed meter changed node during the week (asserted) |
| + | Small-sample convention | k/(k minus 1) over the nodes' summed deviations | filed (7: sample spreads, standard errors built from them); the call is the same without it and under the jackknife (asserted) |
| + | Domain or full design | the build's own installations | filed (4.3: only the build's own assessed installations enter its read health and its standard error) |
| + | As-of for "run a build" | the build each in-service meter runs at the extract | C1: identical at the week's end and at the extract (asserted) |

## Ask sheet (supplemental-stumping)

Main row population: the receipts of the 6,729 assessed installations on read dates 5 to 11 October,
their meters' head-end histories up to the week start and comms parents, and their register rows.
Zero mover, exchange or schedule rows inside it (asserted).

| Ask | What it is in the decision | Device | Stops (asserted) | Named use |
|---|---|---|---|---|
| A. The scorecard: each build's read health, standard error, lower limit and distance from the limit, in order | the evidence the router files beside each fire or hold | the construction itself: the error's unit moves 24 of its 32 figures and the order | the installation-level error is wrong on every standard error, limit and distance (asserted) | the vendor desk and the rollout desk read the margins |
| B. Wave 8 moves onto EM3.12.2 and PX5.3.1 once the call is applied | the exposure each go/no-go releases, as the desk will run it on the night | D2 a schedule cut on 1 October before 37 + 9 meters went in Wave 7 and 22 were exchanged out; D7 serials that lost their leading zeros on batch A; D1 rows re-batched onto B and left on A (16 + 5), with blank NMIs on a third of batch A punishing a dedup on NMI; and the call itself (none onto a build that fires) | rows, distinct rows and one per NMI cell all miss (asserted, logged); the installation-level call 0 / 109; answer **1,274 / 109** | the desk sizes field support for the night |
| C. The substitution load: installations running a build the alert fires on | the warning 6.1 sends Settlement Operations | the call, and the build each installation runs now (movers, exchanges and bench meters on the targets for any call that fires them) | the installation-level call 5,379; answer **1,846** | Settlement Operations plans its substitutions |

**Loop 2 changes, and why.** The Wave 7 ask (moves and move-night losses) was cracked in full by all
four solvers across rounds 1 and 2: its devices (UTC and AEDT nights against market days, replays,
rollback retries) are ones these solvers handle by reflex, so it paid a response that missed the call
as much as one that landed it, and it is gone. The distance from the limit (an output of the decisive
construction for every build) and the substitution load (6.1's own routing figure, which follows the
call) replace it. Ask B carries the call on purpose: the figure the desk runs on Tuesday is the
schedule under this week's call.

**Pair arithmetic.** A response that lands the call keeps the scorecard, the chart, the substitution
load and whatever the schedule's devices leave of Wave 8. A response that misses the call on the error
keeps the eight read-health figures, six of the eight per-build alerts, PX5.3.1's Wave 8 figure and
the chart's points and reference line: about a third of the ask criteria (roughly 17 of 51), and it
loses every standard error, limit and distance, the order, both lists, EM3.12.2's Wave 8 figure, the
substitution load and the chart's title, order and ticks. The build still leans on the main call
staying missed by both top responses; the worth-it gate tests that.

## Shape and criteria

Shape 10: eight builds x (read health, standard error, lower limit, distance, fire or hold) = 40, plus
the fire and hold lists, the order, Wave 8 (2), the substitution load and the chart parts (5): about 51.

## Realism debts

- Four node-nights failing in one week across 72 nodes is a bad week for a mesh, not an impossible
  one: a backhaul SIM or a pole-top power supply takes a collector out overnight, and the backlog
  arrives after the morning cut-off.
- 2,242 installations on one build and 37 on the pilot is the shape of a real fleet mid-migration; a
  pilot spread over seven collectors at about twenty meters each is how a careful desk pilots a mesh
  firmware.
- EM3.12.1's eleven collectors are the older suburbs where the hotfix list sits; none failed this
  week, and its spread-out shortfall fires on either error.
- EM3.12.0 runs a little worse than EM3.11.4 on its own (gap and outage rates of 0.085 and 0.035),
  which is why its shortfall would fire on an installation-level error even without the node failures;
  the node failures are what make the week's evidence too noisy to fire on.

## The client's six-point check (stage 8)

1. **The inputs take real work, and none of it is a planted defect.** Ten files in five formats:
   register-day deliveries replaced by later deliveries, a cut-off in market time against UTC stamps
   and AEDT field times, an activation history with replays, failed activations and rollbacks, serials
   that lost their zeros in a CIS migration, NMIs with and without the checksum, a schedule re-batched
   by a depot. Each is what these systems export; nothing exists to be caught.
2. **The step that flips the call is a methodological choice.** The unit the standard error of a mean
   is built over: independent installations, or the comms nodes the installations share. Nothing is
   planted; the node failures are real reads the standard counts.
3. **The standard defines what to measure precisely enough that one method is defensible.** MDS-STD-114
   files the population, the measure, the window, the cut-off, the reference and the rule; a standard
   error is a defined quantity; the files refute the independence the installation-level error needs;
   every dependence-respecting estimator lands the same call; 4.3 and 7 pin the domain and the
   small-sample convention for the figures.
4. **No decoy memo, staff draft or briefing.** The pack carries no memo, no ranking, no prior read-health
   report and no stakeholder belief, and no sentence states or implies installation-level independence.
5. **The method is not hidden and recovered from certified figures.** There are no certified or
   published figures to reproduce and no corpus to back-test; the method follows from the definition of
   a standard error and the dependence the files show.
6. **The lesson is new.** An operational alert's standard error built over the units that fail together
   (clustered errors on a monitoring gate). The adjudicated pre-flight found no Track A or Track B
   finding at any tier; the nearest mechanism neighbour (task131) is clean.

## Stopping rule

At ceiling if the portal's top two land the call; licensed one repair if the top two miss the call
but the asks leak above a fifth each. In-house: if a round has a solver build the error over the nodes
from the data alone, the architecture has no unstated step left that the data force, and the next move
is the third hardening loop or a re-root, decided on that solver's path sentence.

## Build record

- Generator: `generator/make.py` builds the pack (`build.py`), the goldens from the shipped bundle
  alone (`deliver.py` over `golden.py`), `metadata.json`, runs `checks.py` (the six rungs by name, the
  432-cell grid, the convergences, the independence test, the dependence-respecting groupings, the
  carve-out routes, the node-night split, the deciding contrasts in both directions, the judge's
  random-intercept residual, both asks' stops,
  chronology, separation, the gates, single statement of the reference and the cut-off, the write-up
  against the golden) and the independent `verify.py` (standard library and openpyxl, no shared code,
  the node-level error, the distances and the substitution load recomputed), builds a second time into
  scratch and requires byte-identical target and golden files, then cuts `target.zip` (flat, ten
  members).
- Network: two RF meshes (56 EM3 collectors in pilot, Wave 7, Wave 8, older-suburb and newer-suburb
  groups; 16 PX5 access points), installations placed by the wave history, node failures drawn per
  node per night (`world.EVENT_P`), a failure taking the day from each meter behind the node with the
  event's share as its chance and the backlog arriving between 07:05 and 12:55 AEST. Texture salts
  per build and the network salt were chosen by `tune.py` against the design's margins, edges and the
  carve-out routes.
- Surface screen (`guard.py surface task229`, loop-1 cut): 0 promoted pairs, nearest surface 0.10;
  no persona of another build in the cut pack. Against task228's pack (stage 8, final cut): the run
  was a scratch worktree holding both branches, with task228 at 6b19d41 built from its generator, and
  the worktree was removed afterwards.
  - **Result:** 0 promoted pairs, and no persona in the cut pack.
  - **Track A (task228 against task229): 0.08.** They share no file name, schema, seeded table, prompt
    or write-up wording, entity or deliverable species; both are flat, with one shared format.
  - **Track B:** they share only the population gap label (pattern, decision family and mechanism
    0), so the pair is not promoted.
- Input gates: 10 files; csv, json, md, pdf, xlsx; the MDM receipts carry 95,140 rows; distractors
  `extract_log_20261012.csv` (the pull's provenance: sources, times, coverage, record counts) and
  `dnsp_planned_interruptions_oct2026.xlsx` (the distributors' planned supply interruption
  notifications; the meters keep their interval data through daytime works, so the reads are
  unaffected while the day totals dip), both named in `metadata.json` and asserted unused by the
  golden. `hes_firmware_census_20261012.csv` (the head-end's inventory by image and status) is a
  supporting cross-check, not a distractor: solvers use it to confirm each meter's build, and once the
  fire set is known its in-service counts sum to the substitution load.

## House fixes and realism (reduce-house-fixes, golden-realism)

- H1: the standard's PDF is written invariant and stamped 24/06/2026 with the owner's records system
  as creator and producer; `scrub_producer_metadata.py` audits the target clean; workbooks carry their
  owners and their own created and last-saved stamps (UTC, matching the extract log), laid out the
  way Excel saves them (`postprocess.normalize_zip`). Goldens are script output (matplotlib, json) and
  are left as such.
- H2, H3: every figure in `submission.md` is printed by `golden.py` and re-derived by `verify.py`;
  the steps cite clauses rather than restating figures.
- H4: `target.zip` members equal the ten declared files, no enclosing folder; the chart was opened
  and read after rendering (EM3.12.2's limit drawn off scale at the left edge with its value).
- H12: one convention sentence (per cent to two decimals, counts whole) carries every figure.
- H13: the call is the last sentence of the context; each later paragraph ties back to it.
- H16: no meter runs an image before its release date, no event postdates the extract, and no meter
  joins a node before it was installed (asserted); the standard (effective 01/07/2026) predates every
  document that cites it.
- H18: Wave 8's moves are the exposure each go/no-go releases, as the desk will run them under the
  call; the substitution load is 6.1's own warning to Settlement Operations; the distances are the
  margins the vendor desk reads.
- H20: the prompt names the comms firmware rollout, installations, the market and Settlement
  Operations, which place the request with a metering data provider.
- H21: the invented organisation is Halvane Metering; distributor names (Ausgrid, Endeavour Energy) are
  the real NSW networks matching each NMI's prefix, used as texture; the register withholds address
  fields as an analytics extract does.
- golden-realism: payload carries an alert id, the week, the routing list, a note on the error's
  unit, notes sourced from the standard's own clauses, two-decimal percentages with signed distances;
  the chart uses the validated categorical blue for holds and the reserved critical red for fires,
  with a FIRE label beside every red mark, ink-coloured text, a title stating the call and the
  reference line labelled.

## Leak check (stage 4, mechanical half)

`leak.py --asof 2026-10-12` on the loop-2 cut, and again on the stage 8 rebuild: REVIEW, the same
three lines, no LEAK. The stage 8 rebuild changed containers only. No text under `target/` changed and
the prompt did not change, so round 3's reader pass stands (the equivalence is in `## Determinism check
(stage 7)`). (Loop 1's first run was
LEAK twice, fixed in the generator: block 4 named the reference value on the chart line, and the
standard's revision history gave the old reference as 99.30, which had become a lower limit to the
digit; the history now reads 99.20.) Each REVIEW line:

- The standard "carries 6 of 6 distinctive words of the committed call": the words are read-health,
  alert, fire, hold and the like, which the standard defines; it names no build; harmless.
- The standard carries six stump terms (cut-off, provider, measure, interval, delivery, installation)
  and the field reference five (quality, interval, delivery, carries, installation): the documents'
  own subject matter; neither mentions errors, independence, outages, carve-outs or which grouping
  matters; harmless.

Round 2's solver's-eye reader (on the loop-1 cut) quoted nothing for any question and called every
REVIEW line harmless; its solvability point is answered in `## The outage carve-out route`. Round 3's
reader (on the loop-2 cut, after the prompt changed) again quoted nothing for any question and called
every REVIEW line harmless. Two points from it:

- It names `dnsp_planned_interruptions_oct2026.xlsx` as a distractor that does not help ("none of the
  NMIs it lists in the assessment week lost reads on the notified day"), as designed.
- For question 4 it notes that once the fire set is known, the census's in-service counts sum to the
  substitution load (695 + 423 + 728 = 1,846): a second route to the same figure, which is
  convergence, not a fork, but it means the census answers a graded quantity, so it cannot stay a
  declared distractor. `metadata.json` now declares the extract log and the planned-interruption
  notifications as the two distractors and the census as a supporting cross-check (the change touches
  no shipped byte, no graded figure and no document a solver reads).

## Tried and rejected

- Keeping the seed's product-analytics crash-rate world: a per-user crash rate is a product health
  metric, not the health of data or of a pipeline, so the build would retag as Anomaly Detection
  without changing a word; and task228 holds product-analytics in this objective on the same day,
  so the pairing would block on `ban.pairing` at the heart check.
- First cut of PX5.2.7's late data as partial-day misses (16:00 to 24:00) that the overnight delivery
  already carried as substituted reads: a solver who applied the cut-off clause to the rows it held
  reached PX5.2.7's fire with no further thought. Replaced before any round with whole-day misses that
  leave the MDM no version of the register-day until its 06:30 estimate.
- First rounding-edge assertion measured distance to the bin centre instead of to the x.xx5 edge;
  caught on review, fixed in `tune.py` and `checks.py`, salts re-chosen.
- Architecture 1, round 1 (2026-10-11): both solvers landed the call and every scorecard figure
  (plain 91.3, skeptic 87.4). Plain path: "a build's read health is the mean of its installations'
  read health; its lower limit is 99.50 minus 3 x (sample standard deviation / square root of n)",
  read straight off section 4.2 and 5.2, with the cut-off, the register denominators and the full-week
  population executed as written. Every decisive step was a filed formula, which is the dead shape
  "a committed figure that is the output of a filed formula". Brief: keep the world and the call shape,
  and move the decisive step into the error the measure needs when outages are shared by the meters
  behind one comms node, which no formula in the pack spells out.
- Hardening loop 1, first draft (pooled share with a node-level error, never shipped): making the
  stated measure the pooled share of reads, as the brief first proposed, put the 5-minute
  three-register installations in charge of the installation-level ratio error, which then held
  EM3.12.2 on its own, and split the natural route between a binomial read count and a ratio error,
  so the decisive rung stopped being the one step every solver takes. The filed mean stays, and the
  natural error stays the one round 1 wrote.
- Hardening loop 1, node failures on the access points carrying PX5.2.7 and PX5.3.0, and on the
  older-suburb collectors carrying EM3.12.1: with fourteen and eleven nodes, one failure there widens
  a genuinely degraded build's error until it holds, which buries the signal the alert exists for.
  The tuned week keeps those nodes clean, so the builds that fire do so on a spread-out shortfall and
  the node grain only bites where nodes failed.
- Architecture 1, loop 1, round 2 (2026-10-11): both solvers missed the call at R4 (the stump held).
  Plain path: "Assessed = IN_SERVICE meter, NMI with no meter change, no activation inside the week ->
  6729 installations; mean, sample SD, SE, LL per build; fire if mean < LL -> 5 fire, 3 hold"; both
  filed fire on EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1 and EM3.12.2 and set Wave 8 onto EM3.12.2 to 0,
  and both set the node field aside "because the standard sets no exclusions for them". The asks
  leaked: `grade.py` scored each 54.5 (the fire-and-hold item's only gradable tokens are its two verbs,
  so any list scores it, and a Wave 8 answer that quoted the eligible 1,274 beside its 0 scored that
  item too); read honestly, each kept the read-health figures, PX5.3.1's Wave 8 figure and the whole
  Wave 7 ask, about 37 points, under 40 but with no margin. Decision: harden the ask layer (loop 2):
  drop Wave 7, add the distance from the limit and 6.1's substitution load, and merge the lists into
  the scorecard item.
- Loop 1's leak reader (round 2) found the outage carve-out route: setting the four node failures aside
  with the installation-level error landed the committed list with EM3.12.0 within 0.006 of its limit.
  Closed in loop 2 by raising EM3.12.0's own gap and outage rates so every carve-out fires EM3.12.0 by
  0.15 (`## The outage carve-out route`).
