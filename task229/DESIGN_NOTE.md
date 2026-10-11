# task229 design note

Seed DQ02 (whether the release-health alert fires on this week's build, when the metric is the
average user's rate). The seed's pairing was product-analytics; task228 is being built the same day
in the same objective inside the product-analytics experiment-platform world, so this build keeps the
seed's objective and moves the world to a smart-meter metering data provider, where the object under
analysis (interval data delivery) is the health of the data itself.

**Where the build stands.** Architecture 1, hardening loop 1. Round 1 had both solvers execute the
filed mean and the filed installation-level error and land the call (`## Tried and rejected`). The
loop keeps the world, the call shape and the ask devices and moves the decisive rung to the one step
no clause can carry: the unit the build's standard error is built over. The standard now files the
measure and "three standard errors" and says nothing about that unit; the head-end export carries each
meter's comms parent because head-ends do; the data decides.

## DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | Energy Systems & Utilities / other (smart-meter interval data delivery quality, the metering data provider's read performance; the client list carries no energy task type that serves Data Quality Monitoring) |
| Objective | Data Quality Monitoring & Alerting |
| Niche | a smart-meter data provider's read-health gate on the communications-module firmware builds live in its fleet, deciding which builds the read-health alert fires on before the next rollout wave |
| Shape | 10 scorecard against thresholds: eight builds, each with read health, its standard error, lower limit and fire or hold, plus the Wave 8 moves under the call and the week's upgrade-night cost |
| Decision type / unit | designation_set (which builds the alert fires on) / set_of_items |
| Gap / pattern / generators | population (decisive: the unit the noise lives in is the comms node the installations share, not the installation; the file grain is the register-day delivery), time (the delivery cut-off as of which a read counts); pattern D (two grains, both flawless: installation and node); G2 grain mismatch, G7 operating window, G12, G17 statistical rigor |
| Gate G mechanism | signal_vs_noise_or_hold (which builds sit below the reference by more than their own noise; five of eight hold, two of them on the noise their shared nodes carry) |
| Stump strategy | grain_or_unit; decisive rule filed (the standard defines the measure, the reference and the three-standard-error limit); the step that turns the rule into the answer (the unit the error is built over) is in no sentence; no official decoy; no validated decoy; no calibration organ |
| Layer 2 | estimation_fit, `survey-research-official-statistics/complex-survey-estimation-variance/1` (variance must reflect the primary units; a simple-random-sample formula on the respondent count understates it severalfold for clustered items), made this build's own: the primary unit is the mesh collector or access point, because a node that misses a night's collection takes that day from most of the installations behind it at once, and firmware waves are pushed node by node, so a build's installations are concentrated behind few nodes |
| Layer 1 | interval reads with quality codes at mixed 5, 15 and 30 minute resolution; register-days re-delivered when a later retrieval completes them, and days the MDM held nothing for until its estimation run; receipts in UTC, market time in AEST, field times in AEDT, against a filed cut-off; firmware build codes spelled three ways; effective-dated meter-to-installation assignments with mid-week exchanges; head-end events replayed after a failover and failed activations rolled back; each meter's comms parent in the head-end record with the date it joined |
| Calibration form | none, because the strategy is a stated rule whose construction is the work; no closed corpus is needed or shipped |
| Context artifact | filed_standard (the read-health standard MDS-STD-114 the gate runs on; redrawn from monitoring_export once task228, drawn earlier the same day, took that type) |
| Stakeholder | metering data services lead, who owns the read-health alert the rollout desk gates each wave on |
| Forum / forcing event / org family | operations_desk (the rollout desk holds the wave for any build the alert fires on) / cutover_or_migration (Wave 8 of the firmware migration goes out on Tuesday night) / utility_or_infrastructure |
| World | Halvane Metering, an accredited metering provider and metering data provider in the National Electricity Market, New South Wales, AUD; personas drawn with `guard.py names --locale en_AU --seed 229` |
| Deliverables | `wave8_read_health_alerts.json` (the alert payload the routing system ingests: commits), `read_health_by_build_wk41.png` (reads at a glance) |
| Guard | heart WARN on repeat.gate_g against task228 (answered below); NOTE same_puzzle_older against task98 v3, differentiated on the card; nearest driver 0.06 (task87 v3), nearest heart text 0.04 (task114) |

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
EM3.12.1, EM3.12.2 and PX5.2.7, and Wave 8's 1,274 moves onto EM3.12.2 stop. The step that carries the
stump is the unit of the error. The EM3.12.2 installations the standard assesses were piloted on seven
collectors, and on Thursday 8 October one of them (EMC-8631) missed the night's collection and its
backlog reached the MDM after 10:16 the next morning, so 20 of its 23 EM3.12.2 installations held
nothing for that day at the cut-off, together; two collectors in the newer suburbs did the same to 121
EM3.12.0 installations on the Monday and the Sunday. A build's read health therefore moves with its
nodes, not with its installations: built over the collectors and access points the installations
report through, EM3.12.2's standard error is 1.90 (not 0.41) and EM3.12.0's is 0.56 (not 0.09), both
hold, and the alert fires on PX5.2.7, EM3.12.1 and EM3.10.9 only, whose shortfalls are spread across
their nodes and fire on either error.

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
  is decided by the data's own dependence (the node-night split below), which is estimation, not a
  definition.
- **Forward framing.** The measure is of the week just closed, which is what the standard scores;
  the decision is forward (Wave 8 moves nothing onto a build the alert fires on). A Data Quality
  Monitoring call is a gate on the next action, and its evidence is the last complete window by
  design.

## The decisive move, and why it survives the opponent

1. **Written in no sentence.** The standard defines the installation's read health, the build's read
   health as their mean, the reference, and the limit as three standard errors of the build's read
   health, computed from the build's assessed installations, with sample (n minus 1) spreads. Nothing
   says what unit the error is built over, that installations behind one node fail together, or that
   waves go node by node. The field reference describes `comms_parent` as the node that collects the
   meter's reads, which is what the head-end field is. The round-1 sentence the solvers executed
   ("treats the week's assessed installations as a sample") is gone, because a standard written by
   anyone who knew the network would not file it and the golden would contradict it.
2. **No sweepable corpus.** There is no prior read-health report, no published error, no closed
   corpus; nothing nominates a method.
3. **No arithmetic symptom.** The installation-level error is complete, plausible and internally
   consistent; read health is identical under both errors (only the error moves); every
   reconciliation ties. The node failures are counted the same way on either path.
4. **Not a per-row predicate.** It needs a group (each build's installations by node), the deviations
   summed within the group, and a spread across groups.
5. **Enumeration is arithmetic.** The node is a stored attribute; the move is not a filter on it but
   the decision that the error lives at that grain, which the data forces (below) and no clause states.
6. **No cutover date, and the dated events sit on the wrong side.** The node failures are four
   nights on four nodes; an event study on EM3.12.2's daily read health finds Thursday's dip, which is
   real and counted, and which is exactly what makes the installation-level error fire. The step that
   matters is how much a dip of that shape says about the build.
7. **Survives the deletion** (above).

**First-moves test.** The opponent's first moves (execute the standard; give a mean its textbook
error) land on R4: five fires and Wave 8 stopped onto EM3.12.2. Round 1's plain solver wrote exactly
that error ("99.50 minus 3 x (sample standard deviation / square root of n)").

**The data's own structure (O2, asserted).** Across every node and night, a node-night either loses
the day at the cut-off for 80 to 95 per cent of the installations behind it (four node-nights:
EMC-8306 on 5 October, EMC-8631 on 8 October, EMC-2773 and EMC-7873 on 11 October) or for at most a
few per cent of them; nothing lies between. That hole is what makes the node, and no coarser or finer
grouping, the unit: installations share nights through their node, and nodes fail independently.

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

Answer: fire on {PX5.2.7, EM3.12.1, EM3.10.9}, hold on the other five.

| Rung | Reading | Fires on | Killed by |
|---|---|---|---|
| R0 natural pipeline | latest delivery per register-day, every installation on its end-of-week build, pooled reads, binomial error on reads | EM3.10.9, EM3.12.2, PX5.3.0, PX5.3.1 | 3.5 (read held at cut-off) with 3.3 (every expected interval) |
| R1 | + reads held at the 06:00 cut-off against every interval of every stream (a register-day held nowhere counts zero) | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.0, PX5.3.1 | 3.6 and 3.7 (assessed installation) |
| R2 | + only installations that ran the build all week | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.0 | 4.2 (the mean of installations) |
| R3 | + the mean of installation read health | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7, PX5.3.1 | 5.2 (standard error of the build's read health: reads are not independent draws) |
| R4 | + the error with each installation its own unit (sample SD over root n) | EM3.10.9, EM3.12.0, EM3.12.1, EM3.12.2, PX5.2.7 | the node-night split: installations behind one node fail together |
| R5 | + the error built over the nodes the installations report through | **PX5.2.7, EM3.12.1, EM3.10.9** | answer |

- **How the round-1 brief is answered.** Round 1's landing step was R4 executed as a filed formula.
  R4 is now the step a competent solver supplies by habit, it completes, and it returns five fires and
  a stopped wave; R5 is built so that exactly that step is the wrong one, from the data's structure
  and not from a clause.
- **Partial applications.** Dividing by the register-days the MDM held at the cut-off (instead of the
  register's expected reads) makes the node failures vanish altogether (EM3.12.2 99.77) and holds
  PX5.2.7, so it files EM3.10.9 and EM3.12.1 only; the cut-off applied to rows alone in the natural
  pipeline holds PX5.2.7 and fires six others (asserted).
- **Satisfying to stop at.** R0 is the dashboard number every MDP reports; R1 is what a careful analyst
  who read the cut-off and expected-reads clauses files; R2 is the clause-by-clause population; R3 is a
  correct mean with the error a proportion invites; R4 is the correct mean with the error every
  textbook gives a mean, which round 1 shows the strongest solver writes unprompted.
- **Position.** Calls right per rung (of eight): R0 3, R1 4, R2 5, R3 5, R4 6, R5 8. No intermediate
  rung lands the call.
- **Discriminator dominance.** EM3.12.2: 97.92 against 98.27 on the installation-level error (fires
  by 0.35), against 93.79 on the node-level error (holds by 4.13). EM3.12.0: 98.39 against 99.24 (fires
  by 0.85) or 97.81 (holds by 0.58). The three builds that fire do so on either error by at least 0.33,
  because their shortfalls are spread across their nodes (EM3.12.1's 695 installations over eleven
  collectors in the older suburbs, none of which failed).
- **Convergence (asserted).** The call is the same under the k/(k minus 1) small-sample factor, without
  it, and under the delete-one-node jackknife; the installation-level error fires EM3.12.0 and EM3.12.2
  under either divisor. No build's node-level error undercuts its installation-level error by more
  than 15 per cent (tuned), so the node grain only ever widens the noise where nodes failed.
- **Grid (asserted cell by cell).** 3 versions (cut-off, latest, first) x 3 populations (whole week,
  start-of-week build, end-of-week build) x 4 units (installation mean, pooled reads, register-day
  rows, data streams) x 6 errors (nodes with and without the small-sample factor, installations,
  binomial on reads, binomial on installations, none) x 2 denominators = 432 cells. Every cell that
  lands the call builds its error over the nodes; the ones other than the standard's reading take the
  first delivery of each register-day, which moves at least four builds' graded figures.
- **Sign discipline, margins.** Every build sits at least 0.05 percentage points from its limit, the
  distances to the limits are at least 0.04 apart (the payload's order is not a near tie), and every
  two-decimal read health, standard error and limit sits at least 0.0015 from its rounding edge.

## Closure table (determinism-check, the 22 axes)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | installations whose meter ran the build all week | filed (3.7, 3.6); readings by start or end build are grid cells |
| 2 | Unit of account | the installation | filed (4.1, 4.2); rows, streams and reads are grid cells |
| 3 | Attribution window | market days 5 to 11 October | filed (3.2); the receipts carry only those read dates |
| 4 | As-of dating | the meter's build at the week start, no activation inside the week | filed (3.6, 3.7) |
| 5 | Version basis | latest delivery received before the cut-off | filed (3.5); first and latest are grid cells |
| 6 | Denominator | every interval of every data stream the register lists, every day | filed (3.3); the rows held at the cut-off are a grid cell |
| 7 | Weighting | equal per installation | filed (4.2) |
| 8 | Window length | one week | filed (3.2) |
| 9 | Boundary inclusivity | received before 06:00; fire when strictly below | C1: no delivery lands within 8 minutes of a cut-off; no build within 0.05 of its limit |
| 10 | Rounding path | compute unrounded, report two decimals | filed (7); every figure clear of its edge |
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
| 21 | Scope of a clause | the standard governs the alert; the Wave 7 and Wave 8 asks are defined in the prompt | prompt wording |
| 22 | Forward window contents | Wave 8 moves under this week's call, on the schedule as cut | prompt wording ("once this call is applied") and 6.1 |
| + | Unit the error is built over | the node (collector or access point) each installation reports through | the data's structure: the node-night split (asserted); every assessed installation has one node and no assessed meter changed node during the week (asserted) |
| + | Small-sample convention | k/(k minus 1) over the nodes' summed deviations | filed (7: sample spreads, standard errors built from them); the call is the same without it and under the jackknife (asserted) |
| + | Domain or full design | the build's own installations | filed (4.3: computed from that build's assessed installations alone) |

## Ask sheet (supplemental-stumping)

Main row population: the receipts of the 6,729 assessed installations on read dates 5 to 11 October,
their meters' head-end histories up to the week start and comms parents, and their register rows.
Zero mover, exchange or schedule rows inside it (asserted).

| Ask | What it is in the decision | Primary device | Stops (asserted) | Named use |
|---|---|---|---|---|
| A. Wave 8 moves onto EM3.12.2 and PX5.3.1 once the call is applied | the exposure each go/no-go releases, as the desk will run it on the night | D2 a schedule cut on 1 October before 37 + 9 meters went in Wave 7 and 22 were exchanged out; D7 serials that lost their leading zeros on batch A; D1 rows re-batched onto B and left on A (16 + 5), with blank NMIs on a third of batch A punishing a dedup on NMI; and the call itself (none onto a build that fires) | rows, distinct rows and one per NMI cell all miss (asserted, logged by `checks.py`); the installation-level call 0 / 109; answer **1,274 / 109** | the desk sizes field support and Settlement's substitution load for the night |
| B. Wave 7 moves this week: installations moved onto EM3.12.2 and PX5.3.1 and the interval reads they were missing at the cut-off on the market day they moved | the audit trail of what a wave costs, which the desk weighs beside the alert | D8 the move day in market time (UTC stamps, AEDT local nights from 23:30); D1 events re-stored after the 7 October failover; D5 41 meters that failed on Tuesday, rolled back and moved on Wednesday, and 29 exchanged meters commissioned on EM3.12.2 that no wave moved | UTC day, AEDT day and latest deliveries all miss (asserted, logged); answer **1,109 installations, 16,907 reads / 63, 1,101** | Settlement Operations carries the substitutions |

**Ask A carries the call on purpose.** Round 1 measured the schedule devices at full leakage for both
solvers (each filed 1,274 and 109). A Wave 8 figure "if it goes ahead" therefore paid a response that
missed the call as much as one that landed it; the figure the desk actually runs on Tuesday is the
schedule under this week's call, so the ask now owes that, and a response that fires on EM3.12.2 files
0 for it. The devices still bind a response that lands the call.

**Pair arithmetic.** A response that lands the call keeps the scorecard (24 figures), the chart and
whatever the devices leave of the six ask figures. A response that misses the call on the error keeps
the eight read-health figures, PX5.3.1's Wave 8 figure and the Wave 7 figures it gets through the
devices: about two-fifths of the ask weight, and it loses every standard error and every limit (all
eight builds' errors differ at two decimals between the two grains), the order, both lists, EM3.12.2's
Wave 8 figure and the chart's title and ticks. The build leans on the main call staying missed by both
top responses; the worth-it gate tests that.

## Shape and criteria

Shape 10: eight builds x (read health, standard error, lower limit, fire or hold) = 32, plus the fire
and hold lists, the order, Wave 8 (2), Wave 7 (4) and the chart parts (5): about 45.

## Realism debts

- Four node-nights failing in one week across 72 nodes is a bad week for a mesh, not an impossible
  one: a backhaul SIM or a pole-top power supply takes a collector out overnight, and the backlog
  arrives after the morning cut-off.
- 2,242 installations on one build and 37 on the pilot is the shape of a real fleet mid-migration; a
  pilot spread over seven collectors at about twenty meters each is how a careful desk pilots a mesh
  firmware.
- EM3.12.1's eleven collectors are the older suburbs where the hotfix list sits; none failed this
  week, and its spread-out shortfall fires on either error.

## Stopping rule

At ceiling if the portal's top two land the call; licensed one repair if the top two miss the call
but the asks leak above a fifth each. In-house: if round 2 has a solver build the error over the nodes
from the data alone, the architecture has no unstated step left that the data forces, and the next
move is the second hardening loop or a re-root, decided on that solver's path sentence.

## Build record

- Generator: `generator/make.py` builds the pack (`build.py`), the goldens from the shipped bundle
  alone (`deliver.py` over `golden.py`), `metadata.json`, runs `checks.py` (the six rungs by name, the
  432-cell grid, the convergences, the node-night split, the deciding contrasts in both directions, both
  asks' stops, chronology, separation, the gates, single statement of the reference and the cut-off,
  the write-up against the golden) and the independent `verify.py` (standard library and openpyxl, no
  shared code, the node-level error recomputed), builds a second time into scratch and requires
  byte-identical target and golden files, then cuts `target.zip` (flat, ten members).
- Network: two RF meshes (56 EM3 collectors in pilot, Wave 7, Wave 8, older-suburb and newer-suburb
  groups; 16 PX5 access points), installations placed by the wave history, node failures drawn per
  node per night (`world.EVENT_P`), a failure taking the day from each meter behind the node with the
  event's share as its chance and the backlog arriving between 07:05 and 12:55 AEST. Texture salts
  per build and the network salt were chosen by `tune.py` against the design's margins and edges; the
  design parameters did not move.
- Surface screen (`guard.py surface task229`, hardened cut): 0 promoted pairs, nearest surface 0.10;
  no persona of another build in the cut pack. task228's pack sits on another checkout and is
  screened against this one before ship.
- Input gates: 10 files; csv, json, md, pdf, xlsx; the MDM receipts carry 94,912 rows; distractors
  `hes_firmware_census_20261012.csv` (the head-end's inventory by image and status) and
  `dnsp_planned_interruptions_oct2026.xlsx` (the distributors' planned supply interruption
  notifications; the meters keep their interval data through daytime works, so the reads are
  unaffected while the day totals dip), both named in `metadata.json` and asserted unused by the golden.

## House fixes and realism (reduce-house-fixes, golden-realism)

- H1: the standard's PDF is written invariant and stamped 24/06/2026 with the owner as producer;
  `scrub_producer_metadata.py` audits the target clean; workbooks carry their owners and in-fiction
  dates. Goldens are script output (matplotlib, json) and are left as such.
- H2, H3: every figure in `submission.md` is printed by `golden.py` and re-derived by `verify.py`;
  the steps cite clauses rather than restating figures.
- H4: `target.zip` members equal the ten declared files, no enclosing folder; the chart was opened
  and read after rendering (EM3.12.2's limit drawn off scale at the left edge with its value).
- H12: one convention sentence (percentages to two decimals, counts whole) carries every figure.
- H13: the call is the last sentence of the context; each later paragraph ties back to it.
- H16: no meter runs an image before its release date, no event postdates the extract, and no meter
  joins a node before it was installed (asserted); the standard (effective 01/07/2026) predates every
  document that cites it.
- H18: Wave 8's moves are the exposure each go/no-go releases, now as the desk will run them under the
  call; Wave 7's move-night cost is what a hold costs Settlement Operations if the wave proceeds. Both
  sit on rows the main call never reads.
- H20: the prompt names the comms firmware rollout, interval reads, installations and the market
  day, which place the request with a metering data provider.
- H21: the invented organisation is Halvane Metering; distributor names (Ausgrid, Endeavour Energy) are
  the real NSW networks matching each NMI's prefix, used as texture; the register withholds address
  fields as an analytics extract does.
- golden-realism: payload carries an alert id, the week, the routing list, a note on the error's
  unit, notes sourced from the standard's own clauses, two-decimal percentages; the chart uses the
  validated categorical blue for holds and the reserved critical red for fires, with a FIRE label
  beside every red mark, ink-coloured text, a title stating the call and the reference line labelled.

## Leak check (stage 4, mechanical half)

`leak.py --asof 2026-10-12` on the hardened cut: REVIEW, three lines, no LEAK. The first run was LEAK
twice and both were fixed in the generator: block 4 named the reference value on the chart line
(the standard files it, so the write-up now says "labelled with the standard's reference read
health"), and the standard's revision history gave the old reference as 99.30, which is now
EM3.12.1's lower limit to the digit (the history now reads 99.20). Each REVIEW line:

- The standard "carries 6 of 6 distinctive words of the committed call": the words are read-health,
  alert, fire, hold and the like, which the standard defines; it names no build; harmless.
- The standard carries three stump terms (measure, provider, installation) and the field reference
  five (quality, carries, head-end, installation, access): the documents' own subject matter, and
  "access" is the access point in the `comms_parent` row, which describes the field and says nothing
  about errors, independence or which grouping matters; harmless.

The solver's-eye reader runs again on this cut (every document under `target/` and the prompt
changed), staged with the round.

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
