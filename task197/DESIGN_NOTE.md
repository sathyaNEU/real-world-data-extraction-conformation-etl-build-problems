# task197 design note

A flexibility aggregator's reserve portfolio desk decides which one of its nine contracted frequency
containment reserve sites comes out of the portfolio for the November delivery month and takes the system
operator's single monthly re-prequalification slot.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | energy-systems-utilities / grid-reliability-outage-analysis (serves anomaly-detection) |
| Objective | anomaly-detection |
| Shape | 10, scorecard against thresholds: nine sites by three figures, plus the call, the runner-up, the gap and a chart |
| Decision type / answer unit | pick_one_of_n / named_option |
| Gap | time, population |
| Guard WARNs answered | `repeat.gate_g` and `overuse.gate_g`: method selection is the corpus's commonest mechanism, and this build's selection is of a counterfactual construction the data settles rather than of a model family, so the collision is in the label and not in the move. `repeat.question_form`: the decision is a pick, so the question asks which; any other form would misstate the call. `ban.artifact` moved twice while this build was in flight (operations_log and published_series both went to a shipped neighbour), so the card names the asset register, which this pack also ships. |
| Pattern / generators | E (conditioned yield) / G14, G4 |
| Gate G mechanism | method_or_model_selection (which construction of the counterfactual output the analyst selects) |
| Stump strategy / Layer 2 | causal_design / estimand_identification, own:droop-response-confounded-by-own-block-ramp |
| Calibration organ | none |
| Context artifact | register (the desk's asset register of its reserve-providing units) |
| Forum / forcing event / org family | other (no committee; the desk signs) / statutory_or_regulatory_filing / other (an asset-light flexibility aggregator) |
| Stakeholder role | the reserve portfolio desk (capacity_planner) |
| Spine | target/platform/vkf_highres_archive.sqlite, one row per second of recorded net active power per site |
| World | Netherlands, EUR, Veerkracht Flex (aggregator), Rijksnet (system operator), people drawn with guard.py names |
| Deliverables | response_determination.md, site_response_scorecard.xlsx |

**Assigned ground, and why this is not it.** The wave assignment named quantitative-finance /
market-microstructure-execution-cost. No quantitative-finance task type serves anomaly-detection in the
client taxonomy, so `guard.py check` blocks that pairing outright on `three_rules.task_type`; the
coordinator confirmed the assignment was drawn off a coverage grid without the objective map. The finance
group's only anomaly-detection task type (banking-credit-financial-risk / fraud-aml-detection) was
registered by task196 while this draw was being written. This ground was taken from the coordinator's
fallback list because the architecture's confounder, a unit's own scheduled traverse running in the same
seconds its response to a shared signal is measured, is native to a synchronous power system and to
nothing else on that list.

**Data-native sentence.** Deterministic frequency deviations in this system fall in the first minutes of a
settlement period, which are exactly the seconds in which every site is traversing between programme
setpoints, so each site's recorded power at the second its response is read carries both its droop response
and its own programme movement, and the archive gives the traverse only as the endpoints the programme file
holds.

**Sources read.** `stumping` Part 1.2 (the WHAT screen: the decisive step settles none of the five parts,
because the baseline is a nuisance quantity in estimating a filed gain rather than the comparison);
`determinism-check` section 1 (the comparison is filed as the site's own contracted characteristic);
`supplemental-stumping` Parts 1 to 3 (the ask layer and its devices); `dataset-generation` sections 6 to 8
(rung exactness, Layer 1 mess, provenance); `two-layer-task-design.md` (the five Layer 2 families; energy
carries no Layer 2 pattern library, so the pattern is `own:`).

## Default path

1. Read `operator/system_frequency_minute_summary.csv`, find every minute whose minimum is at or below
   49.920 Hz, and pull those windows from `operator/system_frequency_1s_extracts.csv`.
2. Keep the runs at or below 49.920 Hz lasting 15 seconds or more; take each run's lowest second as its
   extreme second, reading the deviation beyond the 10 mHz dead band from the published frequency.
3. Join `platform/fcr_block_commitments.csv` by delivery date and block to get the sites contracted for
   each episode, and drop the parts of blocks the event log shows withdrawn from reserve.
4. For each site and episode, pull the second-by-second power from `platform/vkf_highres_archive.sqlite`
   and take the site's response as its power at the extreme second minus its power at the last undisturbed
   second before the episode, the natural reading of "the output it would have produced had the frequency
   stayed inside the dead band".
5. Divide by the deviation beyond the dead band and by the contracted gain (contracted FCR capacity divided
   by 0.190 Hz) from `register/asset_register.xlsx`, average the ratios with equal weight across the site's
   episodes, express as a percentage and rank the nine sites.
6. Take the site furthest below contract, check it against the 90.0 per cent tolerance in the performance
   standard, and write the determination.

Ends on: Zwartewater (VKF-ZWT) at 77 per cent of contracted gain
Golden: Kampvliet (VKF-KPV) at 72 per cent of contracted gain

## Stump sentence

Measuring each site's response from its undisturbed level before the episode, rather than from the
programme traverse its own controller was running through those same seconds, credits every site with
whatever its programme did during the deviation and files Zwartewater (VKF-ZWT) at 77 per cent, because
Zwartewater's qualifying episodes fall in the quarter-hours in which it is unwinding a 13 MW morning
discharge in 1.5 MW steps, while Kampvliet, whose droop gain is genuinely at three-quarters of contract,
is lifted to 94 per cent by the evening traverse running up underneath it.

## Three rules

- **Task type:** grid-reliability-outage-analysis in energy-systems-utilities, which serves anomaly-detection: the post-event analysis of what each reserve-providing unit delivered into a system frequency disturbance.
- **Domain test:** the deciding quantity is a unit's realised droop gain, megawatts of primary frequency response per hertz of deviation beyond the dead band, which a power system measures against the unit's own scheduled trajectory because deterministic frequency deviations coincide with market-block traverses.
- **Swap:** "which ward comes off the roster, measured on the beds it staffed per hour of demand beyond the planning band" reads as an ordinary rate comparison: there is no shared signal every unit answers to in the same second, no dead band, no droop, and no traverse between half-hourly setpoints, so nothing in the swapped sentence makes the measured response ambiguous.
- **Layer 1:** programme and commitment files in local market time against a UTC archive and UTC frequency extracts; one settlement meter reporting kWh with its unit column; a metering point replaced mid-window; an October settlement statement issued preliminary and then amended; frequency at two resolutions, a minute summary for locating and one-second extracts for measuring; estimated-quality seconds in the archive; a six-day retention limit on programme-transition recordings; an archive recording restored twice after a storage fault. Each is produced by the systems named in the event log and the dictionary; none carries the decisive step.
- **Layer 2:** estimand_identification. The response credited to a site at a given second depends on what its own programme was doing at that second, and the programme's path between setpoints is in no document, so the gain is identified only against the traverse the site's own archive shows at boundaries where no episode ran.
- **Decisive step:** build each site's programme traverse from its own recorded boundaries, the span its controller takes between settlement-period setpoints, and measure the delivered response against that moving baseline rather than against a level, a setpoint or a period average.
- **Not semantics:** every field, code, unit, time zone and definition can be read correctly and the easy route still files Zwartewater, because the error is in what the undisturbed level stands for, not in what any field means; the programme file's setpoints are read correctly and are simply not the power the site was being taken to at the second the response is read.
- **Not rule application:** no shipped sentence states the shape, span or start of a programme traverse, and none says how to reconstruct it. The technical conditions say only that the response owed is additional to the output the unit would deliver under its programme; the performance standard files the quantity and leaves its construction to the desk.
- **Analyst test:** an analyst who resolves the time zones, the units, the commitments and the withdrawn block parts, and who reads the standard's definition correctly, takes the undisturbed level before each episode as the counterfactual and files Zwartewater (VKF-ZWT) at 77 per cent.
- **Estimand:** clause 2 of `standards/reserve_performance_standard_v4.pdf` files population (qualifying episodes in settlement periods the site was contracted for, withdrawn block parts out of scope), outcome (power in excess of the output the site would have produced had the frequency stayed inside the dead band, per hertz beyond the dead band, at the extreme second), window (21 September to 11 October 2026), unit (percentage of the site's own contracted gain, equal-weighted mean across episodes, to the nearest whole per cent) and comparison (the gain the site's own contract requires, capacity divided by 0.190 Hz).
- **No decoy:** nothing is planted to be caught. No memo argues a site, no block of readings is copied, no rule is withheld against a stated one, and no document ranks the sites. The system operator's statements are at group level by design, as the conditions say.
- **No certified replay:** the prequalification records carry each site's commissioning step test and the controller-change declarations; no certified figure reproduces under the wrong baseline, and no corpus of closed determinations ships.
- **Lesson:** when a unit's response to a shared signal is measured at a second in which the unit is also moving along a schedule, the counterfactual is the schedule's path and not any level, and the path has to come from the unit's own record. No build on file teaches it: the corpus's own-contribution builds separate a source from a background (task182) or attribute a signal to a neighbouring compartment (task180 v2), neither of which has a scheduled trajectory running through the measurement second.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 undisturbed level | the standard's counterfactual invites it | power and frequency columns only | yes, the first reflex | none | battery passes | one subtraction | readable |
| 1 period setpoint | the programme file names the setpoint | a column holds it | yes, the document reflex | none | passes | one subtraction | readable |
| 2 linear traverse across the period, or the period's metered average | no sentence states a traverse | nothing names a span | partly, a smoothing reflex | none | passes | two subtractions | readable |
| 3 the site's own traverse from its episode-free boundaries (decisive) | no sentence states shape, span or start | no column, no flag, no marker | no: no reflex measures a baseline against the unit's own boundary records | nothing ties only under it | no sweep looks at boundary traverses | neither a ratio nor a half of a reported figure | silent |

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | realised response gain | clause 2: per-episode ratio, equal-weighted mean, one decimal | energy ratio over the episode, or ratio of sums | Kampvliet either way at this window | clause 2 words "taken at the extreme second of each qualifying episode ... averaged with equal weight"; `checks.py` asserts the call under both |
| SF2 | qualifying under-frequency episode | at or below 49.920 Hz for 15 or more consecutive seconds | 49.900 Hz, or 20 seconds | same call | clause 2 of the standard states both numbers; asserted across both variants |
| SF3 | the output it would have produced had the frequency stayed inside the dead band | the power the site's own programme was taking it to at that second | the settlement period's programme setpoint | Reiderland | the archive at boundaries where no episode ran: with no response owed, recorded power still sits more than a megawatt off the period setpoint at the measured second, so the setpoint is not what the site would have produced; `checks.py` measures the largest such offset |
| SF4 | contracted gain | contracted FCR capacity divided by 0.190 Hz | capacity divided by 0.200 Hz | same call, every figure scales by 5.3 per cent | clause 2 of the technical conditions, dead band 10 mHz and full activation at 200 mHz |
| SF5 | settlement period the site was contracted for | the commitment file by delivery date and block | the register's usual blocks column | same call, Terborgh and Meppelerdiep move | the register's own note says the column is indicative and the platform writes the commitment file daily |
| SF6 | extreme second | lowest published second, earliest on a tie | last on a tie | same call | clause 2's tie-break; asserted, no tie changes a printed figure |
| SF7 | under the tolerance | below 90 per cent of contracted gain | at or below | same set of three sites | clause 3 of the standard; no figure within 1 pp of 90 |
| SF8 | comes out of the portfolio | the one site furthest below contract | every site under tolerance | the determination still names Kampvliet first | clause 3, one site and the operator's single test slot |
| SF9 | episode count | qualifying episodes in contracted periods, withdrawn parts excluded | all qualifying episodes in the window | same call | clause 2's scope sentence; asserted per site |
| SF10 | time base | archive and frequency in UTC, programme and commitments in local market time | local throughout | no episode changes period | the dictionary states each file's base, offset is +02:00 for the whole window; asserted |

## Ladder

| Rung | Analysis | Names | Figure | Dies to |
|---|---|---|---|---|
| 0 | response from the undisturbed level before the episode | VKF-ZWT | 77 | the archive's own boundary records, which show the programme moving through the episode |
| 1 | response from the settlement period's programme setpoint | VKF-RDL | 58 | the same records: at an episode-free boundary the recorded power is not at the setpoint |
| 2 | the programme read as traversing linearly across the whole settlement period, or the period's metered average as the baseline | VKF-ZWT / VKF-RDL | 74 / 58 | the traverse spans 80 to 300 seconds by site, not 900 |
| 3 | the site's own traverse, its span read from the boundaries where no episode ran and the frequency sat inside the dead band (decisive, silent) | VKF-KPV | 72 | nothing: this is the golden |

Golden ranking: KPV 72, RDL 83, HGZ 88, NWV 91, DLK 93, OOS 95, MPD 97, ZWT 99, TRB 101.
Margin to the runner-up 11 pp, which is 11 printed units. The golden sits 4th on rung 0 (94) and 2nd on
rung 1 (69), so no naive route puts it first. Rung 0's own margin over its runner-up is 6.6 pp, so the
default path commits. Every rung reproduces from the raw files, every rung names a site that is not the
golden, and each rung is a finished-looking analysis: two of the four land on Zwartewater and two on
Reiderland, which is the permitted "two fall to one correction". Partial applications were swept: correcting
the traverse for some sites and not others moves the ranking only through the sites corrected, and every
single-correction cell lands on ZWT, RDL or KPV, each a named answer. Dominance: the decisive move changes
all nine figures, by 11.5 pp on average against the undisturbed level, 9.9 pp against the setpoint and 12.2 pp
against the linear reading, so it is not the smallest move on the graded quantity, and it is the only one that
reverses the ranking.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | qualifying episodes in contracted periods, withdrawn block parts out | filed in clause 2; commitment file is the record; counts asserted |
| 2 Unit of account | the reserve-providing unit (site) | the question names the site; the register is one row per unit |
| 3 Attribution window | the episode falls in the period holding its extreme second | asserted: no extreme second within 5 s of a period boundary |
| 4 As-of dating | determination dated 2026-10-13, window closed 2026-10-11 | filed in clause 3 |
| 5 Version basis | the latest settlement statement issued per month | filed in clause 5 (ask side only) |
| 6 Denominator | deviation beyond the dead band, times contracted gain | filed in clause 2 of both documents |
| 7 Weighting | equal weight per episode | filed in clause 2; asserted against the ratio-of-sums variant |
| 8 Window length | 21 delivery dates | filed in clause 3 |
| 9 Boundary inclusivity | at or below 49.920, 15 or more seconds | asserted: no published second equals 49.9200, no 15-second run is decisive |
| 10 Rounding path | ratios unrounded, the mean rounded once to the nearest whole per cent | filed in clause 2; asserted |
| 11 Tie-break | earliest second on a tied extreme | filed in clause 2; asserted no tie moves a figure |
| 12 Maturity and censoring | the window is closed; every extract is complete to 2026-10-11 | asserted: every qualifying episode has a recording covering its extreme and undisturbed seconds |
| 13 Order of operations | ratio per episode then mean, never sum over sum | filed in clause 2; both computed and asserted |
| 14 Row order | archive rows keyed by recording and second | asserted invariant under permutation |
| 15 Duplicate resolution | one recording per site per window; the restored duplicate sits only on over-frequency extracts | asserted: zero duplicated site-seconds inside the under-frequency populations |
| 16 Identity normalisation | site_id throughout; metering points change on the settlement side | asserted: site_id joins are one to one |
| 17 Netting against gross | response signed against the deviation; up and down never averaged | filed in clause 2 |
| 18 Dimensional units | MW in archive and programme, MWh or kWh with a unit column in metering, Hz to four decimals | dictionary; asserted on the shipped bytes |
| 19 Code and status semantics | quality M or E, event types and codes | dictionary; never the stump |
| 20 Integerisation | episode counts whole, gains not integerised | the asking sentence |
| 21 Clause scope | standard clause 2 the measure, clause 3 the decision, conditions clause 2 the characteristic | each clause names its scope |
| 22 Forward window contents | the call applies to November; nothing about November is needed | the window to date is the whole evidence, filed in clause 3 |

## Literal reader

Executed word for word, clause 2 of the performance standard asks for the power a site delivered in excess
of the output it would have produced at that second had the frequency stayed inside the dead band. The pack
answers what that output was: at every boundary where no qualifying episode ran, the site's recorded power
traverses between the two setpoints over a span its controller fixes and holds, identical at every such
boundary to within the archive's noise, so the counterfactual at any second inside a traverse is
determinate from the shipped bytes. The setpoint reading of the same clause is contradicted by those same
records, since it would have each site deviating from programme by megawatts for minutes at a time with no
response owed. Every other licensed reading in the fork table either gives the same call or is ruled out by
a quoted sentence, and the easy answer comes from an easy method on the same literal estimand, not from a
second reading of it.

## Oracles

None ties only under the golden. The system operator's group availability statement is at group level and
carries no per-site figure, as clause 4 of the technical conditions says. The prequalification records
carry commissioning tests from 2017 to 2025 and two controller-change declarations, and reproduce under
every baseline because they are step tests at a fixed deviation, not window measurements. The settlement
statements reconcile to the metered volumes on the ask path and say nothing about response. The auction
results and imbalance prices are the two declared distractors and touch no graded figure.

## Ask sheet

Three asks, each a component of the determination's own case, each computed over rows the main call
never reads.

| Ask | Figures | H18 home | Use | Population the call does not read | Primary device | Hazards |
|---|---|---|---|---|---|---|
| A down regulation | 9 gains, 9 episode counts | the other half of the same contract: the desk owes the operator a view of both directions | the down-regulation product is contracted and reviewed on the same characteristic | qualifying over-frequency episodes (f at or above 50.080 Hz), which the call's population excludes by sign | D1 replay: one delivery date's recordings for one site were restored twice after the storage fault the event log carries, so a response averaging per recording rather than per episode double counts that date | the kWh meter, the UTC against local market time join |
| B block availability | 6 blocks by committed, held available and shortfall, plus 3 portfolio totals | capacity settlement: the desk is paid on capacity held available | the operator settles capacity per block and the desk reports the shortfall | the control platform's reserve-withdrawal events and their corrections, placed clear of every measured episode | D2 version: three withdrawal events a later correction row cancels, which a naive sum of outage minutes counts twice | the block grain against the minute grain of the event log |
| C settlement reconciliation | 9 metered volumes, 9 differences, 2 portfolio totals | clause 5 of the standard: the desk reconciles its own meters to the operator's statements | the difference drives the imbalance position the desk carries | the settlement meter file and the operator's daily statements | D7 keys: one site's metering point was replaced mid-window, so its September volumes sit under a code the register no longer carries | D2 the preliminary against the amended October statement, D3 one meter reporting kWh |

**Separation line.** Zero device rows inside the main call's population, asserted by count in
`checks.py`: every reserve-withdrawal window is placed in seconds holding no qualifying episode of either
sign for that site, and the restored recording holds no qualifying under-frequency episode. Deleting every
device leaves the call exactly as hard, because the call reads the archive, the frequency extracts, the
programme, the commitments and the two governing documents, and no ask device sits in any of them.

**Forcing, measured on the cut pack** (`generator/ceiling.py` prints each one):

| Device | Natural read | Golden | Gap against the asking sentence's rounding |
|---|---|---|---|
| B superseded corrections | shortfall summed over every logged withdrawal, 43.7 MWh | shortfall over the withdrawals no correction cancels, 31.4 MWh | 12.3 MWh against a stated 0.1 MWh |
| C replaced metering point | window volume joined on the register's current code | both codes, as clause 5's "that site's metering points" requires | 38.2 MWh against a stated 0.1 MWh |
| C preliminary statement | the preliminary October issue | the amended issue, per clause 5's "latest statement issued" | 4.4 MWh against a stated 0.1 MWh |
| A restored recording | per-recording average, which counts one site's restored date twice | per-episode average | moves two of ask A's eighteen figures, measured by ceiling.py |

Pair ceiling: 65.8
Mirror leakage: 52.5
Measured by: generator/ceiling.py

| Ask (cracker, the response that landed the call and ran the battery) | Verdict |
|---|---|
| A down regulation, 18 figures | cracker keeps 16, mirror keeps 16 |
| B block availability, 21 figures | cracker keeps 13, mirror keeps 7 |
| C settlement reconciliation, 20 figures | cracker keeps 20, mirror keeps 8 |

**The ask layer does not yet clear the bar, and the measurement says why.** Every device above is mess the
pack documents: a correction row with its own `supersedes_event_id`, a metering change in the event log, a
unit column, two statement issues. A cracker that landed the call runs the hygiene battery and executes
every filed sentence, so it handles all four and keeps most of the ask weight; the measured pair sits above
40 and the honest figure is in the gated field. The fix `supplemental-stumping` prescribes is a cracker-grade
primary per ask, an inconsistency nothing in the pack invites, which in practice is a grain or
self-validation shape: a figure for each ask whose every row moves on one cross-grain reconciliation. The
candidate carried into `## Tried and rejected` is a period-label convention change in the settlement meter
file, which moves every row of an ask computed on programme deviation and touches no file the call reads.

## Tried and rejected

- Market microstructure and execution cost (the assigned ground), closing-auction own-impact against responsive liquidity: fully designed, then abandoned at the draw because no quantitative-finance task type serves anomaly-detection and the finance group's only anomaly-detection task type was registered by task196 mid-draw.
- Stale closing prices in a thinly traded market as the decisive step: rejected because the literal reading of "the return over the window" is the file's own closes, so the naive answer would have been the golden.
- The register's declared maximum ramp rate as the source of the traverse: dropped, because a document that files a ramp rate turns the decisive step into executing it.
- The portfolio's aggregate response reconciled to the sum of the sites as a control: dropped as an oracle, since it ties only under the correct per-site baseline.
- Reserve performance assessed as the integral of the shortfall against the integral of the obligation: rejected, because filing the functional makes the step rule application and leaving it open is a fork.
- A clock-offset rung on two sites' telemetry: dropped as unnecessary texture once four baselines each landed on a named wrong site.
- A metered-file period-label convention change (period-start against period-ending for one delivery month) as a cracker-grade primary: designed and held, not built, because it needs the metered file re-cut and the ask re-worded; it moves every row of a programme-deviation ask and sits in no file the call reads.
- Graded gains printed to one decimal place: dropped at the build stage. The verifier showed that a solver recovering each site's traverse span from the pack lands within one or two seconds of it, which moves a gain by about 0.2 pp, so a tenth of a point was finer than the data carries. The asking sentence, the standard's clause 2 and every golden now print whole per cent, and the nine gains are calibrated onto bin centres two or more points apart.
- Recovering the traverse span from the half-point of a big programme step: rejected, because at a boundary with a small deviation the site's own response moves its output alongside its programme and biases the span low by up to fifteen seconds. The span is recovered by fitting the traverse over the boundaries the minute summary shows inside the dead band, which lands every site exactly.
- Episodes detected on the generator's own full-day frequency array: replaced by detection inside the published extract windows, so the golden population and a solver's are the same set by construction; it had left three sites one episode apart.
- The register's declared maximum ramp rate as a rung: cut from the pack entirely, because a document that files a ramp rate turns the decisive step into executing it.
- An outage window placed by hand in the event log: replaced by a placement that searches each delivery date for seconds holding no qualifying episode of either sign, after three hand-placed windows landed inside the measured population and moved three graded figures.

