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
- **Layer 1:** programme and commitment files in local market time against a UTC archive and UTC frequency extracts; one settlement meter reporting kWh with its unit column; a metering point replaced mid-window; an October settlement statement issued preliminary and then amended; frequency at two resolutions, a minute summary for locating and one-second extracts for measuring, which disagree for the minutes the summariser ran on the SCADA chain's own average; deviation away from the period boundaries that crosses the operator's extract trigger and never qualifies, some of it carrying a transient that reaches the threshold for too few seconds and some of it too shallow for an extract to be published at all; a settlement meter file indexed by the interval it closes; two clocks in the control platform's event log; three logged withdrawals a later correction row cancels; estimated-quality seconds in the archive; a fortnight's retention on the platform's rate-of-change captures, a capture queue that misses eligible steps and a buffer that wraps; an archive recording restored twice after a storage fault. Each is produced by the systems named in the event log and the dictionary; none carries the decisive step.
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
| 0 | response from the undisturbed level, the site's recorded power at the last second before the episode at which the published frequency was still inside the dead band, which the archive carries for all 935 obliged pairs | VKF-ZWT | 77 | the archive's own boundary records, which show the programme moving through the episode |
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
| 5 Version basis | the settlement statements are the operator's record and carry two October issues; nothing graded reads them | clause 5 names them as the monthly reconciliation and grades nothing from them; the ask side reads the desk's own meter file |
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

Three asks, 50 graded figures. Each is a component of the determination's own case, each is computed
over rows the main call never reads, and each carries one primary device the cracker misses: an
internal inconsistency nothing in the pack invites, found only by a cross-file or cross-grain cut,
with its forcing stated as a number measured on the cut pack.

| Ask | Figures | H18 home | Population the call does not read | Primary device | Hazards |
|---|---|---|---|---|---|
| A down regulation | 9 gains, 9 episode counts | the other half of the same contract: the desk owes the operator a view of both directions, and the down product is reviewed on the same characteristic | qualifying over-frequency episodes (f at or above 50.080 Hz), which the call's population excludes by sign | **D9 self-validation.** For 32 minutes the operator's summary ran on the SCADA chain's own one-minute average, so those rows carry that single value in all three columns and the published extract reaches above the summary's own stated maximum for the same minute. A response that locates episodes from the summary, which is the pack's index to a 97,730 row extract file and the route the under-frequency call rewards, never opens them. | the clock device below (shared), the restored recording, the kWh feed, UTC against local market time |
| B capacity held available | 6 held-available, 6 shortfall | capacity settlement: the desk is paid on the capacity it holds available and reports the shortfall per block | the control platform's reserve-withdrawal rows, every one placed clear of every qualifying under-frequency episode of the call's population | **D8 clocks.** The alarm handler stamps `start_local` from the local clock; the operator interface stamps the same field from the UTC clock and the export appends the house offset either way, so nine rows read two hours early. Nothing says so. The file's own `logged_utc` is 90 seconds after the window opens on every row the platform wrote, which is a convention no document states and only a column-against-column cut shows. | the three correction rows, the block grain against the minute grain |
| C imbalance exposure | 9 above programme, 9 below programme, 2 portfolio totals | clause 5: outside the blocks it is committed to, the whole gap between what a site delivers and what its programme sets falls to the desk's imbalance position, and upward and downward exposure are priced apart | the settlement periods the site held no delivery-block commitment for, the complement of the call's own population, read off a meter file the call never opens | **D6 grain.** The meter data platform stamps each interval with the instant it closes and derives the period index from that instant, so every row carries the interval before the one it names. The column is named for the timestamp the platform writes, not for a convention, so nothing in the pack asserts either reading, and the only evidence is the programme the rows are paired against. | the replaced metering point, the kWh meter, the preliminary against the amended October statement |

**The separation line, asserted by count in `checks.py`.** Zero device and hazard rows in the main
call's declared row population:

| Assertion | Measured |
|---|---|
| withdrawal windows touching a qualifying under-frequency episode at their true place | 0 |
| withdrawal windows touching one at the place their own `start_local` field reads | 0 |
| held summary minutes holding a second at or below 49.920 Hz | 0 of 32 |
| held summary rows moving a minute into or out of the set the call locates | 0 of 32 |
| main-call gains that move when the withdrawal scope is opened | 0 of 9 |
| reads of the settlement meter series on the call's path | 0 |
| deviation windows the archive's added captures change | 0 of 1,652 |
| added captures covering a qualifying episode's extreme second | 0 |

The last two are the ones that matter. The clock device sits on rows the call reads (it drops
withdrawn block parts), so the assertion is run on the call's figures and not on the file: with the
withdrawal scope opened entirely, every under-frequency gain prints the same whole per cent. The
interval-index device sits in a file the call never opens, and that is asserted by counting the
reads of the metered series while the under-frequency table is built, rather than by reasoning
about it.

**Forcing, measured on the cut pack.** `generator/ceiling.py` recomputes each figure from the
shipped bytes under both readings and `checks.py` asserts each line.

| Device | The arithmetic that makes the wrong reading wrong | Natural read | Golden | Against a stated rounding of |
|---|---|---|---|---|
| B, the logged clock | `logged_utc` less `start_local` is 90 s on 21 withdrawal rows and 7,290 s on 9 of them; 7,290 s is not a local offset of a 90 second lag | shortfall per block misplaced by 1.3 to 7.7 MWh, every one of the six blocks moved | 18.0, 17.0, 20.9, 7.1, 26.5, 7.8 MWh | 0.1 MWh |
| C, the interval index | over 13,873 scored periods the mean absolute deviation from programme is 0.0255 MWh when a row is paired with the interval it closes and 0.1437 MWh when it is paired with the period its own index names, a factor of 5.6; of the 2,874 periods whose setpoint steps by more than 1 MW, the row carrying that index sits nearer the previous setpoint in 2,872 and nearer its own in 2. Smallest per-site gap 39.7 MWh, largest 214.9 | 940.9 above and 1,055.1 below | 114.4 above and 242.6 below | 0.1 MWh |
| A, the held summary rows | the published extract reaches above the summary's own stated maximum in the held minutes, and 5 qualifying over-frequency episodes sit inside them | 8 of 9 episode counts move on a summary-first route | 20, 152, 20, none, 72, 15, 22, 71, 71 | 1 episode |
| A and B, the clock hazard | the same 9 rows withdraw 5 over-frequency obligations the face-value reading leaves in | 5 of 9 counts and 5 of 9 gains move on either route | as above | 1 episode, 1 per cent |
| hazard, the correction rows | three logged withdrawals a later row cancels | 12.3 MWh of shortfall counted twice | excluded | 0.1 MWh |
| hazard, the restored recording | one over-frequency capture replayed under a fresh id after the storage fault | a per-recording average counts that date twice | per-episode, per clause 2 | 1 episode |

**The cracker sheet.** The cracker is the response that landed the call, so it has the traverse
construction; it ran the hygiene battery (key uniqueness, exact duplicates, unmatched joins,
fan-out, count ties) and executed every filed sentence it points at: clause 2's scope, clause 4's
availability, clause 5's exposure, the unit column on the kWh meter, the replaced metering point the
event log records, the amended October statement and the three correction rows. Device A is the only
one whose bite depends on the route a response takes, so the cracker is scored twice and the gated
figure is the worse of the two, the cracker that scans the extracts directly and so beats device A.

| Ask (cracker, extract-scanning: the gated reading) | What it keeps | Verdict |
|---|---|---|
| A down regulation, 18 figures | 8 of 18: the four gains and four counts the clock device does not reach, plus Meppelerdiep's pair, which has no qualifying over-frequency episode in the window | miss |
| B capacity held available, 12 figures | 0 of 12 | miss |
| C imbalance exposure, 20 figures | 0 of 20 | miss |

| Ask (cracker, summary-first) | What it keeps | Verdict |
|---|---|---|
| A down regulation, 18 figures | 5 of 18 | miss |
| B capacity held available, 12 figures | 0 of 12 | miss |
| C imbalance exposure, 20 figures | 0 of 20 | miss |

| Ask (mirror, stopped at rung 0 and named VKF-ZWT) | What it keeps | Verdict |
|---|---|---|
| A down regulation, 18 figures | 3 of 18: every gain is on the undisturbed-level baseline and wrong | miss |
| B capacity held available, 12 figures | 0 of 12 | miss |
| C imbalance exposure, 20 figures | 0 of 20 | miss |

Asks B and C consume nothing the call's construction produces, so the two columns agree there by
construction; the separation assertions above are what prove the decoupling, not the agreement of
two rows in a script. The columns part on ask A, which is the construction layer and is meant to.

Mirror leakage: 6.0
Pair ceiling: 34.5
Measured by: generator/ceiling.py

**Why the pair sits below the 40 target rather than on it.** The three primaries are one per ask and
nothing is stacked. The clock device turned out to reach two figure families in ask A rather than one,
because a withdrawn over-frequency obligation leaves a near-zero response in the average as well as
a missing episode in the count, so five gains move as well as five counts. That was measured, not
designed, and the honest number is the measured one. The free figures the gated cracker still banks
are eight, and the sweep in `ceiling.py` puts the 40 line at eighteen, so the margin is real rather
than a rounding of it. Raising the pair would mean adding figures no device reaches, which Part 6 of
`supplemental-stumping` says to cut rather than add.

## Tried and rejected` is a period-label convention change in the settlement meter
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

- The ask layer as first built: every device was adjudicated by a sentence the work reads anyway. Clause 4 said an event a later correction cancels is not a withdrawal, clause 5 said to take the latest statement issued and to read that site's metering points, and the unit column named the kWh meter. A cracker that executes filed sentences handled all four, so it kept 49 of 59 ask figures and the measured pair was 65.8 with mirror leakage at 52.5. The whole layer was documented mess. Rebuilt against supplemental-stumping Part 6: clauses 4 and 5 now file the quantity and adjudicate nothing, and each ask carries one undocumented inconsistency instead. Clauses 1, 2 and 3, which the call reads, are byte-identical.
- The settlement reconciliation as an ask: cut, not repaired. A window total over 21 delivery dates is immune to every shift, label and clock device, because the edge effects cancel, and the only devices it can carry are mapping devices that reach two sites. Four candidates were drafted (a crossed EAN registration, an hourly operator read cycle, a UTC delivery date, a delta-only amended statement) and each either moved two figures or was loud on the ask's own difference column, which is its own control. The quantity was replaced by programme exposure over the periods the site holds no commitment, which is the complement of the call's population and sits on a 18,144 row meter file the call never opens.
- The down-regulation gains as a device target: measured and abandoned as a population device. The per-episode ratio has a standard deviation of 0.8 to 1.9 percentage points within a site, so removing episodes from a site with 16 to 153 of them moves its mean by less than a fifth of a point. A device that changes which episodes are in the population therefore moves the counts and not the gains. What does move the gains is a withdrawal that leaves a near-zero response in the average, which is how the clock device came to reach both figure families.
- Hiding over-frequency episodes by lowering the minute summary's stated maximum: rejected on arithmetic. Any 15 second run at or above 50.080 Hz contains at least one instant of a 10 second sampler, so a coarser sampling chain cannot read below the threshold, and a calibration offset would move the minima the call locates on. The fallback to the SCADA chain's own one-minute average in all three columns is the form that is both arithmetically consistent and confined to minutes holding no qualifying under-frequency second.
- A device on the commitment file: cut at the draw. The call joins it by delivery date and block to scope every episode, so a row covering two blocks or over-stating a committed volume changes the call's own population. Held in this note rather than built, which is the right order.
- A referee per device: dropped to one. The group availability statement was drafted as an arbiter for the capacity-hours ask and cut, because a control that ties only under an ask's golden is a death on file. Device B is settled by two columns of the same row, device C by the programme the rows are paired against, and device A by the extract against the summary that summarises it; none of the three hands over a level.
- Three sites withdrawn in the same minutes: the first placement put the block 3 over-frequency drops for Zwartewater, Terborgh and Nieuwveen on one date and the block 5 drops for Kampvliet, Dollardkust and Reiderland on another, because the under-frequency exclusion left one feasible window each. Shortened to fifteen and thirty minute windows, which opened enough dates to separate them; Nieuwveen, Dollardkust and Reiderland keep their counts rather than share a date, and those three figures are free to the cracker.
- The mid-bin floor applied to the capacity and exposure figures: first replaced by an exactness argument, then met properly. A single global seed cannot drive twenty arbitrary sums mid-bin (the best of forty draws left the tightest at 0.13 of a unit), but a seed per meter can: each site has two figures, so the search is nine independent searches of about six draws each, with one site re-drawn to bring the two portfolio totals in as well. Every one of the twenty exposure figures now sits at least 0.3 of its printed tenth of a megawatt hour from a bin edge, tightest Reiderland above at 0.0303 MWh, against 0.0040 MWh before. A gain is recovered through the traverse span, which a solver lands within a second or two of, so it carries path spread and keeps the 0.3 floor. A block's capacity hours and a site's exposure are exact sums over shipped rows on a population the commitment file fixes, with the rounding path pinned, so nothing on the solver's side can move them; those are asserted for exactness, with a floor that keeps no figure on a printed boundary. Every withdrawal duration was then chosen per site capacity so that capacity times hours lands on an exact tenth of a megawatt hour, which puts all twelve capacity figures on a bin centre by construction rather than by luck.
- Gains carried at one decimal place in figures.json while the asking sentence says whole per cent: caught by the verifier, which reproduced 95.87 for Oosterhout against a golden of 95.9 and failed. The figure is now carried and printed at the precision the asking sentence states, and checks.py reads submission.md's own graded block to assert it, which figures_check.py cannot do.
- `freeze.py check --mode rubric` flags `down.7.episodes` and `down.8.episodes`, Terborgh's and Zwartewater's qualifying over-frequency episode counts, which moved from 72 to 71 because the clock hazard withdraws one over-frequency obligation at each. Both are ask A figures and the mode expects the ask side to move; they are flagged only because 72 is also the call's gain in percentage points, so the tool's numeric match pulls them into the main-call set. Allowed with `--allow down.7.episodes,down.8.episodes`. Every figure that is genuinely on the main call is identical to the snapshot: the nine under-frequency gains to six decimal places, all four ladder rungs for all nine sites, the scorecard, the call at 72 per cent, the runner-up at 83, the gap of 11 points, the 137 episodes behind the call, the nine traverse spans, the 935 obliged site-episode pairs and the three sites outside tolerance.
- The archive announced the decisive step by its shape, not by a sentence. The isolated reader landed the call at about 80 per cent confidence and named the reason: 695 captures with trigger `programme_transition`, every one 241 seconds long and every one starting 30 seconds before a quarter-hour boundary, carrying nothing but the ramp. Measured on the shipped pack the contrast was inside the same file: one distinct length and one distinct offset against 39 lengths and 27 offsets for the operator's deviation windows. An organ's realism is its variance, not its genre, and 695 rows identical on every dimension but their timestamps is a training set with a filename. The archive now holds five kinds of capture (the operator's deviation windows, the platform's rate-of-change captures, captures around logged alarms and withdrawals, captures around mode changes and overrides, and a desk engineer's own captures) across 2,717 recordings with 222 distinct lengths from 67 to 825 seconds and 97 distinct quarter-hour offsets; the rate-of-change captures are 37.3 per cent of the file with 179 distinct lengths and 36 distinct offsets, a capture queue that misses 38 per cent of eligible steps and a buffer that wraps on 8 per cent of the rest, and captures of some other kind fall on all 21 delivery dates rather than only the last six. The trigger values are the platform's own codes rather than a description of what the analyst wants from them.
- A capture length that would have carried the answer: rejected at the design stage. The first draft tied the settle window to the site's own ramp, which is physically tempting and would have let a solver read the traverse span off the recording lengths. The settle window is now drawn from one distribution for every site, asserted at a per-site median spread of 14 seconds, and the only site attribute in a capture's geometry is its ring buffer, whose assignment is held at rank correlation 0.000 against the traverse spans by choosing the configuration salt and asserting the correlation. The first salt tried gave 0.517, which is why the assertion exists rather than the intention.
- Variance that broke the organ: the first spread left Kampvliet with no boundary a solver could fit its traverse over, because five of the nine sites rested on a single usable boundary even in the shipped pack and a 14 per cent miss rate removed it. The retention was widened from six days to a fortnight, which is stated in no shipped file, and the three boundaries per site that a solver can actually fit over are never missed and never truncated, with a short window kept where the jittered one would have run into a capture already held. Every site now keeps between two and five fitting boundaries captured in full, and the verifier recovers all nine spans exactly by least squares.
- The mis-stamped clock as a share of its file: nine of twenty-two withdrawal rows read as designed whatever the mechanism, so eight further alarm-handler rows were added and the share is nine of thirty, 30 per cent. The device's own forcing is unchanged by this, because both readings place a correctly stamped row identically, so the per-block gaps stay at 1.3 to 7.7 MWh; only the levels moved. Every added row's shortfall is an exact tenth of a megawatt hour by the per-capacity duration rule.
- The standard's version note: "Replaces version 3 (2025-09-01), which assessed response on block averages" named the method the easy route uses and marked it superseded, which is a signpost at rung 0 rather than a version note. The characterisation is cut and the replacement and its date stay; the verifier asserts "block average" never returns to the document.
- Clause 5 of the technical conditions, that nothing in a unit's programme reduces the response owed: kept. The test is whether the sentence would exist without the trap, and a technical-conditions document saying a unit's own schedule does not reduce its obligation is what such a document says. It states an obligation, not a method, and it does not say how to rebuild the counterfactual output.
- The three recomputations the exposure figures were tested against, each reported on Terborgh below, Reiderland above and Dollardkust below. The grid-loss factor: Terborgh and Reiderland do not move at all, being 20 kV connections the adjustment never reaches, and Dollardkust below moves 4.3488 MWh applied per interval and 0.2131 MWh applied once to the sum, which is a real fork on the two connections above 110 kV and is why clause 5 now says the delivered energy is the volume the site's own meters register before any adjustment the operator applies at settlement. The rounding path: rounding each interval to the printed tenth moves Terborgh below by 16.6460 MWh, which no printed precision could survive and which clause 5 closes in words ("summed over those periods and rounded once at the end"); rounding each interval to the file's own four decimal places, which is what a careful recomputation does, moves the three figures by 0.0002 to 0.0020 MWh. The restored duplicate: zero on every energy figure, because the exposure reads the meter file and the programme file and the restored recording is an archive row, which the read-count assertion proves. Summation order, the one genuinely free choice, drifts 3.6e-15 MWh over 200 random orders. The margin was 0.0040 MWh and the worst competent drift 0.0020, so rather than ship a figure that spends half its margin on an arithmetic variant, the margin was widened to 0.0303 MWh in the data.
- Clause 3's general rule said the window ends with the last delivery date before the determination, which for a determination dated 13 October is 12 October while the clause names 11 October. The explicit dates settled it and the judge passed on it, but a clause that needs settling is a clause another judge may settle differently, so the rule now reads "the delivery date two days before the desk's determination", which the stated dates satisfy exactly.
- The three governing PDFs carried a zeroed 2000-01-01 control date and an empty producer against a 2026 fiction. reportlab's invariant mode writes that date so the rebuild is byte-identical, so each document's date is now substituted afterwards at equal byte length, the standard at 2026-06-24 against its 2026-07-01 effective date, the technical conditions at 2026-01-05 and the availability statement at 2026-10-07, which is the fifth working day of the month after the one it reports. The producer is the issuing organisation's own document control.
- The scorecard's tolerance column read "whether it is under the standard's tolerance", which can be read inverted and put nine graded boolean cells at risk for one word. It now reads "whether it falls below the standard's 90 per cent tolerance". The prompt stayed inside the thousand-character gate at 991 by shortening the chart clause, which the stated 90 per cent now makes determinate on its own, and the call sentence is byte-identical.
- Rung 0's figures were printed against an unpinned basis. The write-up said "the undisturbed level before each episode" and priced it at Zwartewater 77 per cent and Kampvliet 94, and the re-judge could not reproduce that pair under any construction it tried: 72 and 98 at the recording's first second, 73 and 97 at a ten-second mean, 74 and 96 at fifteen, 75 and 95 at twenty. The generator's basis is a fifth construction, the site's recorded power at the last second before the episode at which the published frequency was still inside the dead band, which sits fifteen seconds after the extract's first row because the extract pads back past the dead-band crossing. Measured, that basis is defined for all 935 obliged site-episode pairs with none missing, gives Zwartewater 76.82 and Kampvliet 93.55, and prints 77 and 94. So the figures were right and the sentence was short: the basis is now stated in the Final Recommendation, in step 6 and in the determination memo, and both checks.py and the verifier assert the figures recompute on it. Zwartewater is lowest under every one of the five constructions, so the rejection never depended on the choice.
- The portfolio exposure total of 114.4 against nine printed rows summing to 114.3: correct and left alone. Clause 5 requires the sum over the unrounded period values rounded once, and rounding the rows first is the path the clause closes. A reader will still doubt it, so the workbook carries a one-line note under the table, its notes sheet carries the convention, and the write-up's portfolio line says it. Nothing moves.
- The frequency record read as built because its deviation was a boundary law with three exceptions: 512 of 515 qualifying episodes with their extreme second 67 to 90 seconds after a period start, and 7 of 607 published deviation windows opening anywhere but at a boundary. The concentration itself is real physics and is the mechanism, so the episodes were not scattered. What the record gained is the deviation a real one carries besides them, placed away from the boundaries and at least 460 seconds clear of every published window: sustained excursions that cross the operator's 75 mHz extract trigger and peak below the 80 mHz qualifying threshold, sustained ones carrying a short transient that does reach the threshold for fewer than fifteen consecutive seconds, and shallow ones no extract is published for. Published deviation windows went from 607 to 657 and those opening 2 to 13 minutes into a period from 7 to 53, 8.1 per cent of the file. The placement verifies itself: an added excursion whose span would carry a fifteen-second run at the threshold is not added, so the qualifying set cannot move, and checks.py recomputes the whole window both ways and asserts 515 episodes against 515 on every one of the 21 dates.
- Why none of that touches a graded figure, which is the part worth writing down. A site outside the delivery blocks it is committed to has its response gated to zero, so its recorded power does not depend on the frequency at all; and a site inside a committed block is scored by ask C only on the periods it holds no commitment for. Either way the exposure figures cannot move, and they did not: all eighteen site figures and both portfolio totals are identical and the tightest bin clearance is still 0.0303 MWh. The call is protected by the 460-second clearance, which exceeds the response lag's 400-second warm start, so the power inside every published deviation window is unchanged: all nine under-frequency gains match to six decimal places.
