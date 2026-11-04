# task192 design note

Architecture 4, drawn 2026-11-04. The slot keeps its number and its objective (Anomaly Detection &
Diagnostics) and leaves the Portuguese protest register for good: architecture 3 (a classifier corrected by
hand-coded audits) is spent, its shipped pack (060f8959) stays at the portal, pending, and its design is in the
git history of this file (commit 826dc6b and earlier). New client domain, world, dataset, generator and prompt
shell; no seed mechanism used. The 55 screens that preceded this draw are in `## Tried and rejected` (A4.1 to
A4.55).

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task192.json`, architecture v4, registered 2026-11-04T04:24:23Z at WARN |
| Client domain / task type | Energy Systems & Utilities (`energy-systems-utilities`), `grid-reliability-outage-analysis` (serves RC and AD): finding the component that is breaking down on a distribution feeder is the network's reliability analysis of its own protective-device records |
| Objective | Anomaly Detection & Diagnostics: a real event (one insulator breaking down) separated from the ordinary momentary interruptions that raise the same counts (lightning, wind and tree contacts, squirrels, the exposure of long rural lines) |
| Decision | which feeder Kestrel Falls Municipal Utilities' one overhead line patrol crew works in the week of 9 November 2026 (week 46), or none; pick one of the city's feeders (`pick_one_of_n`), forward facing (the crew's coming week, before the component fails outright and causes a sustained outage) |
| Shape | 07, a grid of cells: every feeder by its momentary events and its 2026 reliability indices (the asks), plus the call, the poles to walk, the runner-up and what separates them |
| Gap / pattern / generators | `objective` (the momentary counts are correct and are not what the patrol is scored on); pattern `none`; `G2` decisive (the record's unit is a protective operation, the decision's a failing point on a feeder), `G10` second (one point's failures counted as several events) |
| Gate G | `decomposition_attribution`: each feeder's momentary events attributed to storms, wind and trees, animals, exposure and one repeating point |
| Strategy | `grain_or_unit` (operations grouped into the points they came from); Layer 2 family `field_method`; pattern `own:repeat-faults-located-by-their-recorded-fault-current` |
| Forum, forcing event, org family | `operations_desk` (the distribution operations desk dispatches the crew Monday morning), `shift_or_daily_cycle` (the weekly crew assignment), `local_government` (a city department, the electric division of a municipal utility) |
| Role | the utility's distribution reliability engineer (`other`) |
| Context artifact | `filed_standard`: the utility's Distribution Reliability Procedure (the patrol's purpose, the index definitions, the major event day rule, the storm-day screen) |
| Calibration | none |
| Personas | Kelsey Sanford, Shawn Hartman (`guard.py names --geo us --seed 192`) |
| WARNs answered | `three_rules.strategy_risk` (grain_or_unit): the analyst test below files a storm, squirrel or exposure feeder with every field and rule read correctly, so the step is analytical; `overuse.objective`: the number's objective is fixed by START_HERE.md; `repeat.deliverables` (svg+xlsx, against task193 v3): a strip chart of fault currents is the species that makes a repeated current read at a glance, and the prompt's other shell classes are under their quotas |

**Data-native sentence.** A feeder head relay records, for every fault it trips on, the faulted phase and the
current the fault drew, and on a radial overhead feeder that current falls with the fault's distance from the
substation through the line's impedance; one cracked insulator that flashes over on damp mornings and recovers
when it dries draws the same current on the same phase every time, so its flashovers are several momentary
events sharing one signature, which no count of events, no storm screen and no per-mile rate can tell from the
squirrels, trees and lightning that make up the rest of the record.

**Abstraction sentence (written to be refused).** "The decisive quantity is where a unit's repeated failures
come from, recovered by grouping its events on a recorded signature that stands for position along the unit."
No approved or delivered build carries it: task183 forecasts cable failures from each identified section's own
failure history (the parts are known by id and the call is a forward count), task303 removes the tickets every
feeder opened in the same minute as one upstream loss (a shared cause across units), task194 nets one area's rise
against a neighbour's simultaneous fall (supply passed between units), task200 re-measures detection on first
meetings with an image (a history-defined subset). Nearest driver on file 0.07 (task132).

**Sources.** Fully constructed operating layer for a fictional municipal electric utility in Missouri: the
feeder head relays' fault records, the mid-line reclosers' event logs, the SCADA sequence-of-events log, the
outage management system's tickets, the device register, the feeder register and impedance model, the
lightning detection network's strokes, the airport weather station's hourly observations, the vegetation
management log, customer contacts, and the Distribution Reliability Procedure. Provenance in `metadata.json`.

## Default path

1. Read the Distribution Reliability Procedure: the patrol goes to the feeder where a component is failing;
   momentary interruption events are counted the IEEE 1366 way (reclosing operations within five minutes are one
   event); storm days are the calendar days the procedure's storm screen marks.
2. Join the feeder head relay records to the SCADA operations and the mid-line recloser logs, convert UTC to
   Central time, keep the momentary operations (the breaker closed back in and held), and group them into
   momentary interruption events per feeder for August to October 2026.
3. Set aside the storm days (lightning within the screen's distance of the feeder's substation, or gusts at or
   over the screen's speed at the airport station).
4. Normalise each feeder's non-storm momentary events by its overhead miles, and set the result against August
   to October 2025 to see which feeder's blinking is new.
5. Send the crew to the feeder whose non-storm momentary rate rose most.

Ends on: the squirrel feeder (fixed by the generator's design point; written in at stage 2)
Golden: the feeder whose momentary faults repeat at one recorded current on one phase

## Stump sentence

A competent solver who groups every feeder's reclosing operations into momentary interruption events, sets aside
the storm days, normalises by overhead miles and compares August to October 2026 with 2025 sends the patrol to a
feeder whose new blinking is squirrels, when the feeder whose faults keep returning at one recorded current on
one phase has an insulator breaking down.

## Three rules

Task type: `grid-reliability-outage-analysis` in `energy-systems-utilities`, which serves anomaly detection; locating the component that is breaking down on a distribution feeder from its protective devices' fault records is the utility's reliability analysis of its own network.
Domain test: the deciding quantity is where on the network a component is failing, which distribution protection reads from the fault current each operation records, because a fault's current falls with its distance from the substation through the feeder's impedance, so one insulator flashing over again and again records one current on one phase; the field's estimator for where a fault is is the impedance-based distance to fault.
Swap: "send the inspector to the ward where a device is failing, read from the alarms each bed raised" keeps none of it: there is no feeder impedance, no fault current that falls with distance, no flashover that clears when the breaker recloses and no momentary interruption to count.
Layer 1: relay records in UTC against the SCADA log in Central time with the same operation in both (the relays and SCADA); reclosing shots grouped into five-minute events (the protection scheme); mid-line reclosers in kiloamps against relays in amps, and phase labels in two conventions (two device vendors); outage tickets in two layouts across the 2026 system upgrade, partial restorations as child tickets (the outage management system); customers downstream of each device from the device register, feeders renumbered at the Cotter Road rebuild (the asset register); none placed to be caught.
Layer 2: `field_method` / grain: the feeder's operations are grouped into the points they came from; the methodological choice that flips the call is reading each momentary operation's recorded phase and fault current as a position on the feeder and looking for the position that keeps failing, instead of counting, screening and normalising the operations.
Decisive step: recognising that a breaking-down component announces itself as repeated self-clearing faults at one place, and finding that place by grouping each feeder's momentary operations on the faulted phase and the fault current the head relay recorded (equivalently, the impedance-based distance to fault each current implies).
Not semantics: every field, unit, clock and code read correctly (the relays' amps, the reclosers' kiloamps, UTC and Central time, the phase conventions, the five-minute event rule, the storm screen) still leaves the counts, the storm-screened counts, the per-mile rates and the change on 2025 on a storm, squirrel or exposure feeder; no column holds a location or a repeat.
Not rule application: the procedure files the patrol's purpose, the event rule and the storm screen and nothing about where faults come from, so executing every filed rule files the squirrel feeder; the enumerated family (momentary events, events per customer, storm-screened events, per overhead mile, the change on 2025, the phase-skew test, damp-weather events) spreads over several feeders and never names the failing one, and the standing family once the faults are placed by their current is one member, the ruling-out done by a group of same-phase, same-current operations that no other feeder carries.
Analyst test: a strong analyst who joins the relays to SCADA, groups the reclosing operations into momentary events, sets aside storm days, normalises by overhead miles and compares with 2025 files the default path's feeder, the squirrel feeder, and never asks where on each feeder the faults were.
Estimand: Distribution Reliability Procedure section 5: the weekly patrol goes to the feeder where a component on the overhead line is breaking down, so that it is found and replaced before it fails outright; storm damage, animal contacts and tree contacts are left to the storm, animal-guard and line-clearance programmes; filed in `procedures/DRP-04_distribution_reliability_procedure.pdf`.
No decoy: nothing is planted to be caught: no memo, draft, briefing or stakeholder figure names a feeder; the failing insulator is an ordinary component failure whose only trace is its own flashovers in the relay records.
No certified replay: the method is not recovered by reproducing certified or published figures; no shipped figure is a fault location or a repeat count.
Lesson: a feeder's momentary interruptions are a mixture of independent events and one repeating source, and the repeating source is found only by placing each fault on the line through the current it drew; no build on file teaches locating a failing component from repeated fault-current signatures.

## Survivor anatomy

Actor: the deciding property (one point on a feeder failing again and again) has no column in any file; it is a relation between a feeder's own momentary operations, the same phase and the same recorded current on different days.
Link: the signal is read through a comparison the field's momentary-interruption method never asks for, each operation's fault current against the other operations' currents on the same feeder and phase; the impedance model turns a current into a distance, but no key joins an operation to a pole.
Reflex: the field's named method for targeting patrols (momentary interruption events, IEEE 1366, storm days set aside, per overhead mile, against last year) sits at rungs 0 to 3 and files a storm, squirrel or exposure feeder.
Back-test: the textbook route validates: the storm-screened, per-mile momentary rate tracks the animal and tree contacts the outage tickets confirm on the other feeders, and last spring's line clearance on the failing feeder lowered its counts exactly as the clearance programme expects.
Second use: the relay records carry every rung and the asks' momentary events; the SCADA log is the operations record the relays are reconciled to; the impedance model is the protection study's model; the weather and lightning files carry the storm screen; deleting the decisive step removes no file.
Shock: the failing feeder's August to October count is ordinary, its rise on 2025 near zero (spring line clearance took out its tree contacts), its phase mix unremarkable; it is no sort's extreme.
Pins: the procedure files the patrol's purpose, the event rule, the storm screen and the major event day rule; no filed sentence names fault currents, positions, repeats or phases.

## Tried and rejected
- The loop-4 reader, cold on the re-drawn record, **missed the call**: it filed 550 at 50 per cent
  with 600 at 20, 500 at 12, the stored-code count's 300 at 8 and the golden's 450 at **6**. That is
  the first cold thread in this wave to go wrong on a call, and it matters for more than Gate F: the
  pair ceiling assumes a ladder that keeps all but one response off the call, and until a cold thread
  misses it the measured pair is an assumption rather than evidence. task190 was retired today on
  exactly that premise failing. Here it holds, so this build's ask arithmetic means what it says.
  The reader's route is the predictive-value family again, now with an extra step: it treated the
  partner and line codes as ground truth because they agree on 205 of 205 overlapping actions, and
  corrected only the monitor-only actions. Without that step it lands on 605, the 600 cell.
- The realism list from that read, held until the judge reports. **The worst of it is that a realism
  defect is generating a wrong route:** the partner and line codes agreeing on 205 of 205 overlaps is,
  in the reader's words, the most generated-looking statistic in the pack, because independent
  reporters never agree perfectly, and that perfect agreement is what licensed it to treat those codes
  as truth. Breaking the agreement moves the filer-confrontational count, so it is a figure-moving fix.
  Next: the audit covers 54 per cent of accepted May to August reports, 91 per cent in May falling to
  22 in August, and a desk double-coding half of everything is a validation exercise rather than a
  sample. That one is answered by framing rather than data, since the protocol can say what the
  exercise was, and no figure moves. The classifier reads as a relabeller instead of an instrument,
  its errors concentrated in three labels while two stay almost clean. Identifiers are gap-free across
  three files. The exception file reuses identifiers, about two rows per identifier across 308 rows,
  which is a key-uniqueness defect the hygiene battery would flag and which nothing declares. The
  tension index contradicts itself, labelling a rise from 56.3 to 67.2 as falling. The media coverage
  file is a literal expansion of the monitor's own config weights. And the report lags have no long
  tail at all, the press maximum sitting at 20 hours.
- Credit where the pass earned it: the surge now touches new ground, 66 municipalities to 112 and 214
  localities to 421, which was the reader's complaint last round and is no longer one.
- **(architecture 3, the realism pass of 2026-10-17) A hand-coding worksheet drawn as a fixed half of each round's window.** Two cold readers read the file as built rather than kept: exactly 1,000 rows split 420 and 580, exactly 50.0 per cent of each round's pool, rows in identifier order with the coding dates running monotonically down the page, daily loads repeating, 47 notes from six stock phrases with ten of them on rows no second coder had seen, eleven of eighteen changed decisions ending on the classifier's own code, agreement flat at 74 to 79 per cent across all four coders, and not one report the desk could not code. The desk now has its own random stream (`SEED_DESK`), its own calendar and its own capacity: the lot is the sum of what its coders got through on the days they sat, which is 1,064 rows, 68.4 per cent of round one's pool and 43.5 per cent of round two's; the file is written as the desk's journal, by round, coding day and coder, so consecutive rows run up the identifier half the time (0.505); the daily load runs 5 to 45 over 58 coding days; a note sits only on a row a second coder read or a row nobody could code, composed from two pools into 35 distinct texts on 63 rows; a second coder reads a row far more often when the report is one the classifier also got wrong, so 15 of the 19 changed decisions end on a code the classifier did not give; each coder reads an ambiguous report as a neighbouring code of the same kind at their own rate, so exact agreement runs 0.614 to 0.737 across the four; and eight rows carry no manual code at all, with the dictionary and protocol 4.5 saying what an empty code means and SF27 asserting that reading those rows as ordinary codings gives the same call. **What it cost:** the audit's four cells, and therefore the committed count and every figure downstream of them, had to be re-tuned (see the entry on the design point below); the protocol's 4.5 now says the file carries the manual code "onde a mesa o conseguiu fixar".
- **(architecture 3, the realism pass) The six weeks with no coding in them.** `desk_calendar` worked each lot in the fixed 34 days before its own close, so round one coded 17 May to 19 June, round two 7 August to 9 September, and the 48 days between them were empty although round two's lot held reports dated from 20 June: either the desk worked that stretch or the round's dates were wrong. Each round now opens its lot the working day after the previous round closed and works it to its own close, with the association's holiday month thinner rather than empty and the odd catch-up Saturday. Coding now runs 4 May to 8 September with no gap longer than seven days and coding days in every month from May to September, asserted (`real.coding_calendar_has_no_hole`, `real.coding_covers_every_month`, `real.round_opens_on_the_previous_close.R2`). **What it cost:** the desk draws from the reports that had arrived by each coding day, so the lot is weighted towards the early part of each window: May gives 458 of the audit's rows and August 107. That is the stated process working, it strengthens rather than weakens the engine (the audit's prevalence sits 1.56 times the record's), and it moved every audit cell.
- **(architecture 3, the realism pass) The reposted August load keeping its original delivery stamps.** The second load of the August partner file carried the same `carimbo_entrega_utc` as the first while the import log said it arrived on 14 September and the ingest counter counted it there, so the only thing that marked the reload was the load id. The portal now stamps the second load's rows on the day the log says they arrived, spread across that morning, which is what actually double-counts a month. **What it cost:** the two stamps a reposted report now carries open a reading the pack had not had, so the dictionary's `carimbo_entrega_utc` line makes the delivery moment the first load's, SF28 carries the row, and the alternative is asserted to move the partner route's median from 1,385 to 1,450 minutes. The device is stronger for it: D1 now moves the A2 median as well as the counts.
- **(architecture 3, the realism pass) One clock profile across the three routes.** All three routes drew the action's start hour from one shared distribution, so the press monitor, the partner network and the public line filed on actions with the same mean hour of 14.0 to 14.2, the same standard deviation of 3.6, the same 07:00 floor and the same 21:55 cap. Each route now has its own hours and its own shape: the monitor's titles cover the set-piece daytime actions (mean 13.55, 07:00 to 21:59), a partner organisation writes up what its own people were at during their working day (11.76, 08:00 to 20:59) and the public line is where the evening and night-time blockades arrive (15.68, 05:00 to 23:59), asserted pairwise (`real.route_clocks_differ.*`, `real.route_clock_ranges_differ`). **What it cost:** the start hours move every receipt stamp, so the three route medians and the two partner columns moved with them.
- **(architecture 3, the realism pass) Start minutes on a quarter-hour lattice.** 52 per cent of start minutes were exactly a quarter hour, 26 per cent were one of eight other five-minute marks and the rest were uniform, which a reader read off as a lattice with a small second group ending 05, 10, 25 and 55. The minute is now drawn from a distribution with a quarter-hour mode and a shoulder around it: 44 per cent on a quarter hour, 22 per cent on another five-minute mark, 22 per cent within four minutes of a quarter hour and 12 per cent anywhere, which puts 45 per cent on the quarter hours, every one of the 60 minute values in the file and 29 per cent off a multiple of five, asserted (`real.minute_mode_is_the_quarter_hour`, `real.minute_lattice_broken`). **What it cost:** nothing beyond the stream: no graded figure reads a start minute, and the medians move only through the stamps.
- **(architecture 3, the realism pass) A surge that doubled the volume without touching new ground.** Monthly actions roughly doubled from September while the municipalities touched moved only between 117 and 119, because every action drew its municipality uniformly from the gazetteer's 119. The geography is now the register's own: each municipality carries a share of its district's standing contention (the district capital and the two island capitals most, a long tail of small ones), each dispute theme falls on the territory it belongs to, and the two themes the autumn brings, the transmission network and the fire season, run the municipality size the other way, because the lines and the burnt ground are where the people are not. The spring and summer months now touch 82, 83, 86 and 88 municipalities and the two autumn months 117, thirteen municipalities have no action in the register before 5 September, the interior districts' share rises by 37 per cent while the metro districts' falls, and Beja doubles, all asserted (`real.geography_moves_with_the_volume`, `real.register_does_not_start_saturated`, `real.surge_reaches_new_ground`, `real.surge_concentrates_in_districts`). **What it cost:** the fortnight municipality counts, the graded column of the A1 table, fell from 100 to 119 to 63 to 112, and the protocol's dispute-theme list went from fourteen themes to ten so that a theme-stratified correction has strata big enough to be worth computing (see the design point below). The earlier bulletins' three figure collisions with graded fortnight rows went with it.
- **(architecture 3, the realism pass) Re-tuning the design point on the coding desk's stream alone.** The first attempt searched `SEED_DESK` for a draw in which either round's cells alone land in the call's cell: 7,200 desk seeds gave one hit and none with both rounds inside the band. Measured, the reason is structural: the desk draws more than half of each round's pool, so a round's estimate is pinned by that window's own realised rates and the desk's draw only jitters it by about 30 actions. The two rounds' anchors are a property of the action layer, so the search moved there: 12,000 action seeds were screened on the pooled call, the two round anchors, the stratified family's anchors at seven reference desk draws, the seven wrong routes' cells, the record's dispersion in both regimes, the three medians and the fortnight ties, which gave twelve candidates, and the desk's own stream was then searched on the best of them. The shipped point is action seed 10461 with desk seed 4. **What it cost:** the two sub-routes of rung 1 now share the 250 cell while rung 0 sits at 300 and the audited prevalence at 700, so the ladder is six cells rather than the five it was, and rung 4a (the coded count scaled by the recall, 615.64) shares the default path's 600 cell, 1.1 actions from it, which is the one place the ladder is worth less than a cell. Against that, every route in the right family is now at least 7.7 actions from its cell edge where two of them used to sit 0.8 and 4.6 from one, and the family gap is 3.3 sigma where it was 2.7.
- **(architecture 3, the realism pass) The classifier's nominal rates at 0.46 and 0.0295 with a fourfold fall in the confrontational share.** The re-centring measured the candidates' positions as functions of the nominal recall, the nominal false-mark rate, the level of the confrontational share and its fall across the period, and the combination the ladder needs is a recall near one half, a false-mark rate near one in fifty, an audit prevalence near 15 per cent and a record prevalence near 10 per cent. The shipped values are 0.46 and 0.023 nominal, measured at 0.4783 and 0.0201 on the shipped worksheet, with the confrontational share falling by a factor of 2.6 rather than 4.2 so that the audit's prevalence stays inside the cell the audited-prevalence route needs. **What it cost:** nothing in the record's story, which still has a confrontational spring and summer and a peaceful autumn mobilisation; the marked rate still halves across the cut (8.8 against 4.3 per cent, p = 3.0e-09).
- **(architecture 3, the realism pass) The monitor and the public line stamping receipts at any hour.** With the start hours re-drawn, one press report landed at 23:21 on 30 October, 38 minutes from the period's edge, and the route table's zone-invariance assertion caught it: a solver who read the receipt stamps an hour out would have counted a different triple. The association's own intake hours, 06:00 to 23:00, are now in the monitor's configuration, and whatever lands outside them is written at the next collection, so no receipt stamp sits within an hour of either edge and the triple survives every zone in the pack by construction rather than by luck (`SF26.route_window_zone_invariant`). **What it cost:** the night's arrivals pile into the morning, which is what a real intake does, and the three medians moved with it.
- Loop 3, the route table shipped with no window. The loop-2 judge computed three windows off the same sentence (received in the period 4,346 / 1,204 / 945, received to the 6 November extract 4,658 / 1,313 / 988, reports of actions dated in the period 4,348 / 1,215 / 945, with the partner median moving 1,327.0 / 1,312.0 / 1,331.0), so the ask was an open fork. Closed with one `convencoes` row fixing the basis, scoped to the route figures: the partner table's own row beside it stays action-dated, so the two conventions read as the two different things they are. The row is load-bearing, not a giveaway: delete it and the three windows compute again, and it says nothing about the repost, the placement or the medians. Measured zone-robust before it was written, the nearest receipt stamp sitting 1.25 hours from a window edge.
- Loop 3, five figures graded that the prompt never asked for. The decomposition (4,200 / 427 / 302 / 30 / 1,000) and the per-fortnight shaded series left block 4; the decomposition stays in Critical Components, where it is a component of the call rather than an answer the rubric owes, and the shading stays in the bulletin as the house's own context, described but not graded.

- The seed's own architecture, a filed definition of a campaign plus a verification subsample that
  blesses one reading of it: the definition makes the count rule application and the subsample is a
  certified replay, both of which the client's rules ban as the decisive step. Re-rooted at the draw.
- Recovering the number of operations from a periodogram of the daily action counts: the number of
  peaks depends on the window, the detrending and the significance threshold, so the count would not
  be determinate. Replaced by the intervals read off the locations each operation alone touches, which
  needs no threshold.
- Letting the institute's flag file group the location-days into episodes: that ships an artifact that
  answers the decision question wrongly, which Gate G forbids. The flag file flags days and groups
  nothing.
- (architecture 2) A confrontation risk filed with an eight-week horizon from each episode's opening,
  the cohort the episodes opened in a window that ends a week before the extract: measured on the
  model, the complete-case share over the episodes with a full eight weeks of follow-up is an unbiased
  estimate of the same quantity and lands within a point of the golden, so the easy route reaches the
  answer. Replaced by the whole-life estimand.
- (architecture 2) Grading the share to one decimal: the weekly and fortnightly readings of the
  decisive estimate give 17.05 and 16.99 against the daily 17.03, which a one-decimal figure splits.
- (architecture 2) A ranked watch list of the live episodes by remaining confrontation risk: the
  remaining risk is a monotone function of an episode's age alone, so the ranking degenerates.
- (architecture 2) The whole competing-exit architecture, designed, built and gated: on the remote
  merge of 2026-10-17 task266 arrived with the same mechanism in other nouns, and task157 arrived with
  the same gap, decisive pattern and decision type while task190 v2 took the stakeholder role.
  Re-rooted at the draw rather than shipped into a clone finding.
- (architecture 3) Correcting the count by the classifier's precision alone, or by its recall alone:
  each carries one of the two measured error rates and lands two cells away, which is why both are
  rungs rather than the answer.
- (architecture 3) A double-coding sample that verifies every classifier positive and a sample of its
  negatives, which is what a real quality desk draws: it makes the predictive values the design-exact
  quantities and the sensitivity the derived one, which inverts the decisive step and leaves the
  weighting of the two strata arguable, so each round draws at random from the reports entered since
  the previous close and 4.5 says so.
- Dating the desk's hand coding forward from each round, the round day plus nought to eight days: the
  November round then codes reports after the 6 November extract, which the leak sweep caught.
  Replaced by the desk's own working calendar before each round's close, with the batch worked in the
  order the reports arrived.
- Partner rates of 5.25 and 6.15 euros for the amended agreement: the paid reports came to exactly
  892.50 euros, so a solver rounding half up and one rounding half to even would file different euros.
  Replaced by rates that land every total at least a quarter of a euro from its edge.
- **(architecture 3, the stage-4 determinism finding of 2026-10-17) A correction forced by nothing but
  the shape of the record, with a flat confrontational rate and a validation sample spread over the
  whole period.** The judge found eight routes standing between 226 and 237 on a golden of 234: a
  pooled predictive-value correction, its month-, theme- and round-stratified variants, the sample
  prevalence, a continuity adjustment, the hand-code-where-sampled route and the pooled Rogan-Gladen
  the golden used. Measured, the two families differ by less than their own sampling error (the gap's
  mean was 7 against a standard deviation of 24) because the two are algebraically the same quantity
  when the validation sample is representative of the population it corrects, and that sample's
  coverage varied while its prevalence did not (p = 0.81 across months). Nothing in the record could
  pick one. Re-rooted inside the architecture, not away from it: the audit's window now stops before
  the autumn surge, the confrontational share falls fourfold across the period, and the two families
  are 30.8 per cent apart at 2.78 standard deviations of the gap's own sampling error.
- **(architecture 3) Keeping the validation sample at 2,600 rows over 59.7 per cent of the period's
  accepted reports.** The reader's verdict was that no desk produces that file in that shape, and the
  arithmetic agrees: at the audited batch's size the stratified variants of the right family sit
  within a per cent of the pooled one, so they cannot be told from it, and the hand-code-where-sampled
  route closes to within 6 per cent of the answer. Measured over the repaired design, the audit has to
  sit between about 900 and about 1,350 rows: below 900 the theme-stratified route with a pooled
  fallback leaves the answer's cell, above about 1,400 the hand-code-where-audited route comes inside
  6 per cent of it. Built at 1,000 rows in two rounds, 23.8 per cent of the period's accepted press
  reports and about 500 a round, which is what the reader put a real desk's own output at.
- **(architecture 3) Grading the count as a whole number.** The audit's four cells carry a sampling
  standard deviation of 57.4 actions on the answer, so a whole number claims 0.2 per cent precision on
  a figure whose own standard error is 12.7 per cent, which is the arithmetic task190 paid for.
  Replaced by the nearest fifty actions, 0.87 of that standard deviation, with every candidate route's
  cell asserted.
- **(architecture 3) Cutting the audit to a few per cent of the record.** Measured rather than argued:
  the answer's relative sampling error is about 1.5 over the square root of the hand-coded
  confrontational reports, and that count is the audit's row count times the audited prevalence, so an
  audit of a few per cent of 4,200 press-reported actions would hold about a dozen such rows and carry
  a standard error near 30 per cent, at which no granularity separates the two families and no cell
  holds the right one. The record's volume cannot be raised to buy the coverage back without putting
  more than fifty contentious actions a day into a country of ten million. The audit is therefore
  sized by what it has to measure, 1,000 rows, and the coverage that follows, 23.8 per cent, is
  reported rather than disguised.
- (architecture 3) A single nine-day burst per round with four coders at equal loads and no second
  codings: the reader read it as a file built to be read by an analyst. Replaced by the desk's own
  working calendar, 65 coding days at loads from 1 to 41, unequal coder loads of 345, 290, 212 and
  153, 78 rows sent to a second coder with the desk's decision recorded on each, and 49 coding notes.
- (architecture 3) A classifier that relabels at random: the reader measured its agreement with the
  hand code at 21.8 per cent against 19.8 expected by chance, which reads as noise rather than an
  instrument. Replaced by a confusion matrix over the protocol's eight codes with a strong diagonal
  and neighbour confusion, which agrees with the hand code on 64.2 per cent of the worksheet's rows
  and confuses a code with a neighbour more often than with a distant one, both asserted.
- (architecture 3) Action start times on the quarter hour between 08:00 and 19:59 with nothing over
  lunch, no weekday to weekend difference, partner deliveries flat across the 24 hours and line lags
  bounded at 42 to 206 minutes: every one of them a tell the reader read off the pack in one pass.
  Replaced by start times from 07:00 to 21:59 with 82 per cent of minutes on a multiple of five, a
  working week in the daily counts, partner deliveries inside each organisation's working day, and
  lognormal lags, all asserted.
- **(architecture 3) The earlier bulletins' note that two dispute themes entered the register with
  the autumn mobilisation.** "O boletim de setembro registou a entrada de dois temas de disputa que o
  registo ainda nao tinha visto, energia e redes e florestas e fogos, com a mobilizacao do outono."
  Two independent cold readers named it, in the same company as 3.3, 4.5 and the classifier's
  stability line, as part of what lets a solver see that the autumn is unmeasured by the audit. Cut.
  It was the only optional member of that company and the pack loses nothing by it: the surge is
  visible in the monthly action counts, and the two themes are visible as codes that appear in the
  record only from September. The protocol's thematic table keeps both codes, because a code list is a
  code list and says nothing about when either theme entered the register. **Why the other three stay,
  so nobody cuts them later:** 3.3 files the estimand, so it is the WHAT; 4.5 with the dictionary's
  round definition files the sampling frame, which is also the WHAT and which `determinism-check` §1
  requires; and `config_monitor.json`'s "alteracoes_no_periodo: nenhuma" is a decisive fact Gate B
  requires shipped, because without it the classifier's error rates would not transport either and the
  problem would have no answer at all. Cutting the sentence moved no figure: `figures.json` is
  byte-identical across the rebuild and only the bulletins PDF's own bytes changed.
- **(architecture 3) Grading the fortnight's partner column as a share of the fortnight's actions.**
  The share put a one-decimal percentage in thirteen graded cells, and `determinism-check` §3 says
  never grade a percentage near a one-decimal edge, flatly, without an exception for a filed rounding
  path. Filing the path closed the one route that misprinted Q11, but managing one instance of a hazard
  class is not removing the class, and a judge reading the rule as written costs a determinism return.
  The column is now a count of the fortnight's actions the network reported. No data moved, so the
  call, the candidate table, the 2.8-sigma family gap and the audit's own draw are untouched; thirteen
  cells stay thirteen cells; and the difficulty is unchanged, because the count still turns on the
  action grain, the reposted load, the delivery lag against the action's own day and the gazetteer,
  measured at three misses on the cracker sheet. Exactly fourteen graded figures moved, the thirteen
  converted cells and P07's euro total, confirmed by diffing `figures.json`.
- **(architecture 3) A cracker sheet measured by hand.** Two builds in this wave shipped a sheet whose
  figure was the complement or the mirror of the truth, and the gate that reads the sheet cannot tell.
  The sheet is now the printed output of `generator/cracker.py`, which runs each named wrong path
  through `golden.py`'s own readers on the shipped bundle and exits non-zero if any row's cracker
  figure equals the golden.
- **(architecture 3, the author's pre-ship pass of 2026-10-17) Measuring a share's distance to its
  rounding edge as the distance to its printed value.** `checks.py` computed `abs(t - round(t))` on the
  share in tenths of a point, which is the distance to the middle of the printed cell and not to its
  edge, so it named Q9 at 0.0129 as the tightest when the real tightest is Q11 at 0.0013 and Q9 is
  comfortably clear at 0.0371. The judge found it. The check now computes `(0.5 - abs(t - round(t)))/10`
  and reports every one of the thirteen, and the seed hunt that had optimised the wrong quantity is
  superseded by filing the rounding path instead (axis 10). A bar of 0.010 points on all thirteen is
  reachable, 27 of 360 pack seeds clear it with no two-step drift, but reaching it means a different
  `SEED_PACK`, which re-draws all 69 graded ask cells, the audit's own draw and therefore the call, and
  voids the judge's reproduction table; held for the author's call rather than taken.
- (architecture 3) P07's rate at 6.15, which put its euro total at 731.85, 0.35 of a euro from its
  edge and the tightest of the seven: moved to 6.10, which lands 725.90 and 0.40, the clearance the
  other six have. Only that one graded figure moved, confirmed by diffing `figures.json` across the
  rebuild.
- (architecture 3) Leaving "the euros paid under its data agreement" to clause 6.2. Two independent
  threads reached two values on the same reading, 7,337.90 against 7,410.85 and P02 at 2,493.05
  against 2,504.95, because 6.2 pays a late delivery with the period it was delivered in and whether
  that excludes it here is one inferential step. Closed in the asking sentence rather than in 6.2,
  which sits next to the device: the ask now names the observable, the euros the agreement pays for the
  reports filed by the close. No golden figure moved, because the golden already computed exactly that.
- (architecture 3) Paragraph 4.5 saying each round draws from the reports entered since the previous
  round closed, while round two closed on 10 September and its batch stops at 31 August: the 305 press
  reports of 1 to 10 September were in neither reading and a close reader was left holding a
  contradiction, although the figure never moved because the dictionary's range is what controls. 4.5
  now gives each round a cut and a close, the batch runs from the previous cut to its own cut, and the
  round closes when the desk signs the batch off; the dictionary's `ronda` column states both dates for
  both rounds. Text only, no figure moved.
- (architecture 3) The dictionary saying the desk works the batch on working days while 56 of the
  1,000 rows carry a weekend coding date: the generator's own calendar already models the occasional
  catch-up Saturday, so the dictionary now admits it rather than the rows being moved. Text only.
- (architecture 3) Leaving each partner's own monthly return to be read as the delivered rows. The
  returns count a report by the month of its action and the portal stamps the delivery, so at a month
  boundary the two differ, P01's May reading 18 against 17 delivered. That is the pack's own basis
  difference and it is now a declared device in the ask sheet (D3) with the basis filed in the
  dictionary's description of the returns, rather than an accident a reader has to guess at.
- (architecture 3) Paragraph 4.5 closing on the desk's schedule, that the round the calendar puts in
  the autumn is done in the next reporting period: of the whole pack it was the one line nearest the
  signpost boundary, because its only function was to tell a reader that the autumn holds no audited
  report. Cut. The frame stays, which is the sentence saying what each round drew its batch from and
  over which period, and that is the WHAT the estimand owes; the coverage gap is visible in the
  worksheet's own dates and the uncomputability of every stratified route is asserted on the data
  rather than on that line. Dropping it moved no figure: `figures.json` is byte-identical across the
  rebuild and only the protocol's own bytes changed.
- (architecture 3) Three Azores municipalities in the gazetteer's "Ilhas" district beside the Madeira
  ones, with the clock offsets in no shipped file: a geography error of the pack's own making that
  left the medians open four ways. The gazetteer now carries "Acores" and "Madeira" as separate
  districts and the monitor's configuration states each one's offset and the 25 October change, which
  closes the medians and leaves the Azores hour as a device in A2 rather than an accident.
- **(architecture 3, the stage-2 re-measurement of 2026-10-21) The magnitude fix itself: widening the
  composition drop so the easy family sits further from the call.** Dead on the floor it spends. The
  drop and the margin on the nearest wrong rung are one quantity with two signs: sweeping
  `CONF_RATE_LO = CONF_RATE_HI / k` over k = 1.0 to 8.0 at the shipped surge, the reach `PV - RG` rises
  36.95, 89.56, 114.37, 139.19, **159.62 (shipped, k = 2.6)**, 180.05, 190.27, 197.57, 206.33 actions
  while the gap to rung 2 falls 180.10, 125.68, 105.57, 85.47, **68.91**, 52.35, 44.07, 38.16, 31.06
  and its ratio falls 1.3588, 1.2824, 1.2496, 1.2126, **1.1785**, 1.1423, 1.1245, 1.1103, 1.0919. The
  1.15x floor is crossed between k = 2.6 and k = 3.2, the gap falls under one printed cell by
  k = 4.0 (0.88 cells) and rung 2 shares the call's own printed cell at k = 8.0 (369.064 against
  338.000, both printing 350). Over twenty action seeds a setting, the floor passes falls from 20
  of 20 at k = 1.0 to 13 of 20 at the shipped point and 8 of 20 at k = 4.0. The shipped point is
  therefore already at or past the widest setting the floor allows, and the realism pass of
  2026-10-17 had already walked this dial down from a fall of 4.2 to 2.6 to keep a wrong route
  inside its own printed cell (its own entry above), which is this same trade read from the other
  side. `corr(reach, gap to the nearest rung)` = -0.5791 over the sweep.
- **(architecture 3, the stage-2 re-measurement) Widening on the volume axis instead, where the two
  separations do not trade off.** `ACTIONS_SURGE` 1.0 to 6.0 at the shipped drop raises the reach
  65.23, 82.77, **159.62**, 207.10, 250.98 actions with the floor holding (ratios 1.2027, 1.2306,
  **1.1785**, 1.1896, 1.2190), so it is the one axis that buys reach without spending the floor, and
  it is dead on Gate C: over 120 draws on that axis the licensed error-rate family is unanimous on
  one printed call in 5, going 2, 1, 2, 0, 0, 0 of 20 seeds at surges 1.0, 1.6, 2.45, 3.4, 4.5 and
  6.0. The axis that keeps the ladder splits the call.
- **(architecture 3, the stage-2 re-measurement) The architecture, on the identity behind both of
  those.** `PV - RG = N (p - p_a) [(PPV - (1 - NPV)) - 1/(r - f)]` holds to 1.3e-13 at every seed, so
  the reach the ladder stands on **is** the difference between the record's own marked rate and the
  worksheet's own marked rate, times a constant of the four cells. Both are one group-by on a shipped
  column (`codigo_acao` on the item log, `codigo_monitor` against a non-empty `codigo_manual` on the
  worksheet), so the exchange rate is fixed by arithmetic rather than by tuning: 26.90 actions of
  reach per sigma of the window comparison at the shipped point, 25.29 to 48.00 across the drop axis.
  Counted over the two axes at twenty action seeds a setting, 245 of 300 draws give a printed
  cell of reach or more and 66 leave the window comparison insignificant, 22 do both, and **0**
  of those 22 have the licensed family unanimous; the family is unanimous in 9 of the 300 and all
  nine sit where the comparison is significant below 0.05. **0** of 320 draws give reach, a
  unanimous family, the 1.15x floor and a mid-bin call together, and the three that give the
  first three are the shipped setting and two at surge 1.0. So every draw with reach and a quiet
  record forks the call and every draw that files one call announces the step: the dial's two
  ends are the same end, the failure is not magnitude and no magnitude fix exists. Re-root or
  retire, the author's call: this is architecture 3.
- **(architecture 3, the stage-2 re-measurement) Re-shipping this pack as it stands, independently
  of the screens.** `guard.py heart task192` now returns **BLOCK** where on 2026-10-17 it returned
  WARN with no BLOCK, because the corpus moved under it: `ban.role` on the `research_desk`
  stakeholder family, `ban.forum` on `trustees_or_governors` and `ban.forcing_event` on
  `vote_or_meeting` all against task266 (v1), now delivered or approved, and
  `test.same_driver_older` because the decisive gap, the decisive pattern and the Gate G mechanism
  all repeat task270 (v2, lineage) with no differentiation line on the card. The driver text is not
  the problem, its nearest neighbour on file sits at 0.06; the axes are. So the role, the forum and
  the forcing event have to be redrawn whatever is decided about the magnitudes, which is a second
  reason the number wants a re-root rather than a resumption. `guard.py validate` is clean (277
  cards, 0 invalid) and the pack itself is untouched: `verify.py` passes all 138 independent checks
  and `target/`, `golden/` and `target.zip` hash to what the ship recorded.
  `guard.py surface` is exit 0 with no BLOCK lines and no personas in the cut pack, and it now
  promotes **three** pairs for adjudication with task192 in all three, each at exclusion level
  with both sides delivered: task191 vs task192 at 0.101 (corpus pct 99, back to back, same
  decisive gap and same context-artifact type on the cards), task192 vs task193 at 0.100 (pct 98,
  back to back, same decisive gap) and task189 vs task192 at 0.101 (pct 99, same decision type).
  On 2026-10-17 only the task191 pair was promoted, so two have appeared since. These are B-track
  card-axis matches rather than driver text, and they point the same way as the heart BLOCK.
- **(architecture 3, the stage-2 re-measurement) A seventh cell nothing in the pack rules out, found
  on the way.** A calibration model fitted on the worksheet with the classifier's label and a month
  term, extrapolated over the two months the audit never reached, files 504.483 and prints **500**,
  which is neither the call nor the default path and has no row in the candidate table and no `cand.*`
  assertion. Without the month term the same model reproduces the default path exactly (614.530). It
  is a construction a competent analyst would use and it is an open Gate C candidate on the shipped
  pack, which the loop-4 judge never tested; recorded here because it would have to be closed by any
  repair and cannot be closed by a magnitude.
- **(2026-11-04) Architecture 3 spent, confirmed; the re-root to architecture 4 opened at stage 1 and no
  candidate cleared, so nothing was carded.** Architecture 3 (confrontational actions in an event record, a
  classifier corrected by hand-coded audits) was confirmed spent at the 2026-11-01 re-check (commit 91cee50):
  its seventh cell (a logistic fit of hand code on the classifier mark plus a month index, extrapolated over
  September and October) files 504 and prints 500 against the golden 450, and the sentence that would close it
  names what the decisive step recognises, so the fork is the stump (`stumping` 1.2). Its shipped pack
  (060f8959) stays at the portal, pending, and its card is marked `architecture_spent`. The architecture 4 draw
  screened 55 candidates across 13 task types (A4.1 to A4.55 below) on 2026-11-04, each against
  `guard.py mechanisms --objective anomaly-detection`, `guard.py slots` on the mechanism and the setting nouns,
  the default path, the swap, the survivor anatomy and the bin. The window moved during the pass: task461 v2 and
  task193 v3 registered at 03:18 and 03:21 UTC, which closed physical-environmental-sciences x
  anomaly-detection and environmental-monitoring-exceedance and opened energy-systems-utilities and
  human-factors-ergonomics (task194 v17 and task200 v6 left the last three). The three strongest are written in
  full first.
  - **A4.5, the storm overflow capacity fault (physical-environmental-sciences / environmental-monitoring-exceedance;
    prototyped, then banned against task193 v3).** Draw: a regulator's area team sends its one winter compliance
    investigation to the storm overflow whose own pass-forward capacity fell (a partly blocked throttle), read
    from event duration monitoring against the rain gauge network. Default path: each overflow's 2026 spills by
    the 12/24 count against its 2021 to 2025 counts, adjusted for its gauge's 2026 rainfall, dry-day spills
    screened, files the overflow whose rain-adjusted count rose most. Golden: the overflow whose spills now begin
    after far less rain (the rain before each spill's onset, 2026 against 2021 to 2025). Swap holds (rainfall
    runoff on dry-weather flow, a setting a blockage lowers, a tipping-bucket gauge, 12/24 counting). Anatomy
    answered on paper (no column holds the setting; the onset rain is a relation between the spill log and the
    gauge record; the count is the field's method; the published returns reconcile with it). Measured on the
    clean truth (scratchpad `cso/proto3.py`, 16 overflows on 6 gauges at 15 minutes, 2021 to 2026, six seeds):
    the onset family (rain in the 3, 6, 12 and 24 hours before onset, event depth to onset, its lower quartile)
    names the faulty overflow in 5 of 6 seeds at onset ratios of 0.44 to 0.51 against 0.73 to 1.71 elsewhere,
    but the rain-adjusted 12/24 count names it in 3 of 6, spill hours per unit rain in 4 of 6 and spill events per
    unit rain in 3 of 6. The easy route is a crude member of the same capacity family (`stumping` 1.1, convergence
    and reach are one dial), and the confounds strong enough to move it off the fault (a showery year, long winter
    spells counted in 24-hour blocks, a catchment that grew) move the onset family with it, because intense
    storms and wet antecedents also lower the rain an unchanged overflow needs to spill. Dead on the dial.
  - **A4.48, a PV fleet's hardware fault against soiling (energy-systems-utilities / grid-reliability-outage-analysis).**
    Draw: the O&M company's one repair crew to the site whose arrays lost output to a fault it can fix, when a
    new dust source soils another site. Default path: the IEC 61724 temperature-corrected performance ratio over
    the last 60 days, curtailment and outages netted, against the same weeks of 2025, files the soiled site.
    Golden: the ratio on the days just after the latest cleaning rain. Swap holds. Dead on `stumping` 1.1b:
    soiling read from the recovery after rain (the soiling ratio, RdTools' stochastic rate and recovery) is the
    field's own method for a site-wide loss in a dry spell, so the golden is the opponent's first move; the
    upper-quantile, recency and trend routes also read the clean state, so the dial fails as well.
  - **A4.44, wrong blood in tube against detection opportunity (human-factors-ergonomics / safety-incident-error-analysis).**
    Draw: which clinical area gets the 2027 electronic bedside labelling first, by how often its samples are taken
    from a patient other than the one on the tube, when a mislabel is caught only where the sample can be
    compared with an earlier, independently taken group of the same patient. Default path: detected WBIT per
    1,000 samples (the haemovigilance metric) files the area with the most repeat patients. Golden: detected WBIT
    per comparable sample, the emergency department. Swap holds (ABO and D groups, historical group checks, the
    two-sample rule). Dead twice: on the bin (about one WBIT in 2,000 samples leaves 10 to 25 detected events per
    area over two years, so the area ranking is seed-hostage at any plausible volume) and on the abstraction test
    against task200 v6 in the same task type (a safety rate re-measured on the subset of records each person's own
    history makes valid).
  - Environmental monitoring: A4.1 river phosphorus concentration-discharge hysteresis, spent (task249 v5's
    driver, task279's screen, landed by the field's hysteresis reflex); A4.2 reservoir manganese aligned to the
    turnover date from a thermistor chain, spent (the phase of a recurring cycle read from a continuous record);
    A4.3 autosampler carryover after high samples and A4.4 cross-contamination by non-dedicated purge pumps on a
    fixed route, Layer 1 carrying the stump (data validation, planted in effect); A4.6 roadside remote-sensing NOx
    with a thermal-window defeat strategy, task273 v2's re-weighting to the year's conditions by stratum, and the
    "same conditions" fork closes only by naming temperature; A4.7 accelerated monitoring after an exceedance
    inflating a sample mean, the fork (sample mean against time-weighted) closes only by naming the weighting;
    A4.8 ozone titration near roads, not an artifact; A4.9 fenceline benzene with a near-field source, the
    method's own correction and task201's wind-sector screen; A4.10 landfill gas probes under barometric pumping,
    task279's screen.
  - General statistics: A4.11 central statistical monitoring, low within-patient variability at a fabricating
    trial site, the client's own planted-defect example (copied readings); A4.12 Benford tests on expense claims
    with fixed-rate allowances, swap and task185's heaping; A4.13 Mahalanobis against univariate outliers, the
    library test.
  - Payment claims: A4.14 ambulance trips with no claim at the destination, swap (billed against actual distance
    reads the same for taxis) and the OIG's own audit; A4.15 capitated groups' encounters against their pharmacy
    and laboratory claims, task188 v2's driver; A4.16 coding intensity from diagnoses with no treatment evidence,
    a filed crosswalk executed (rule application, code semantics); A4.17 completion factors with one provider's
    faster submission, the grouping dichotomy (1.1c); A4.18 multiple-provider episodes counted by prescriber or
    by practice, the unit (WHAT screen); A4.19 provider-based billing after an acquisition, the outcome
    definition (WHAT screen).
  - Disease surveillance: A4.20 wastewater at a sewershed holding the regional hospital, task182's approved driver
    (a unit's level less its response to an external series) and the resident population is the WHAT; A4.21
    positivity with negatives reported in weekly batches, task181 v2's nowcast family; A4.22 a community cancer
    cluster drawn around its cases, task191's extremum against a null extremum; A4.23 community urine resistance
    under selective testing, task273 v2's re-weighting; A4.24 imported cases in a reproduction number, the field's
    reflex; A4.25 PMMoV normalisation at a works taking a pepper processor's effluent, planted in effect and an
    estimator choice.
  - Survey research: A4.26 chain drift in a scanner-data index, task463; A4.27 interviewer falsification from
    impossible travel between interviews, swap; A4.28 a stratum jumper's weighted impact, the surprise-stratum
    reflex; A4.29 a hot-deck donor reused across recipients, the imputation flag is a column; A4.30 mirror-trade
    asymmetry from goods in transit at the year end, time semantics and task68's world; A4.31 head-office
    allocation in regional statistics, task194's driver.
  - Banking fraud and AML: A4.32 bid rotation in a procurement ring, AD25 (task202's seed); A4.33 AIS dark gaps on
    financed voyages, swap; A4.34 mule deposits in bursts at one deposit machine, the aggregation reflex (fraud
    card 4); A4.35 cheque kiting across two banks, no float left to exploit in 2026.
  - Safety signals: A4.36 the Weber effect against older comparators, swap and reflex; A4.37 nocebo reports after
    a forced biosimilar switch, the stratify-by-switch reflex; A4.38 hot vaccine lots, age and week
    standardisation (reflex); A4.39 febrile seizures after co-administration, the co-prescribed-cause family.
  - Provider quality: A4.40 breast screening readers whose women's prior images were missing, the "same reading
    conditions" fork names the step; A4.41 surgeons' early learning-curve cases, task200's driver and the swap;
    A4.42 cardiac arrest calls and resuscitation decisions, the population of arrests (WHAT screen); A4.43 complex
    cases allocated to a senior surgeon by a multidisciplinary meeting, the meeting log one join from a column.
  - Human factors (open from 03:21 UTC): A4.45 drug diversion read within patient across nurses, swap and an
    individual accusation; A4.46 dispensing-cabinet overrides against the pharmacist's verification time, the
    population of inappropriate overrides (WHAT screen); A4.47 takeoff performance entered for the wrong weight or
    intersection, a column comparison (FMS weight against the load sheet) and a filed SOP (rule application).
  - Energy systems (open from 03:21 UTC): A4.49 a recloser's repeated self-clearing faults at one location,
    task183's driver; A4.50 a service reservoir's structural leak against an outlet meter's low-flow error,
    separable only by a fitted two-driver regression (Gate C), and the natural drop test is the field's named
    method; A4.51 a failing service connection from its own voltage against its own load, Ohm's law the reflex
    and the sibling-netted form task303's driver; A4.52 a peaking unit's failed starts against standby time,
    small numbers and the swap; A4.53 FLISR commissioning hiding sustained interruptions, a dated cutover in the
    register; A4.54 a reconfiguration moving customers behind a fault-prone spur, task194's driver; A4.55
    sympathetic trips on DER-rich feeders, task303's driver.
  - What the pass leaves: on every cell this objective holds, each decisive step screened here was the field's
    method, a WHAT (population, unit, comparison), a grouping, a crude member of its own estimator family (the
    dial), or a driver already on file (task182, task188, task191, task194, task200, task273 v2, task303). The two
    cells that opened during the pass (energy-systems-utilities and human-factors-ergonomics) were screened last;
    the next draw starts there, from what a file the question gives no reason to open pins (`stumping` Part 6),
    with the cheapest licensed member priced before the anatomy is written.

- **(2026-11-04, architecture 4 draw) The recloser repeat-fault design priced on the clean truth before carding**
  (scratchpad `rc/proto.py` to `rc/proto3.py`, 16 seeds). With the failing insulator firing 20 or more times a quarter,
  every count found it (the dial again). At six flashovers among realistic background rates (10 to 60 momentary
  operations a feeder a quarter) the same-phase, same-current group named it in 16 of 16 seeds (6 against at most 5
  elsewhere at plus or minus 2 per cent), but the change on 2025 named it in 10 of 16, the non-storm change in 9 and
  the phase-skew test in 2. The generator therefore carries the offsets real feeders carry (spring 2026 line
  clearance on the failing feeder, a 2026 squirrel year on another, single-phase laterals that concentrate faults on
  one phase, a short urban feeder) and the relays' stated 1 per cent current accuracy, and `checks.py` asserts every
  cheap route off the call.

## Architecture 2, blocked at the draw by the remote merge

Architecture 2 asked what share of the register's dispute episodes would have recorded a
confrontational action by the time they closed, with a quiet close treated as the other way an episode
ends rather than as an observation that stopped. It was drawn, designed, built and gated: 635 episodes
in the cohort, 89 with a confrontational action at the extract, 312 closed quietly, 234 still open,
and 108 episodes, 17 per cent, on the decisive estimate, against 89 on the recorded count, 141 on the
known outcomes and 178 on a product-limit survival. The pack carried 17 files in four formats and a
25,688-row item log, with 108 generator assertions, 99 independent checks in a verifier that read only
the bundle, two byte-identical rebuilds, `figures_check.py` exit 0 and `precut.py` at 0 FAIL and 0
WARN.

It is spent for one reason outside the build. The remote merge of 2026-10-17 brought in task266,
drawn the same day in sociology-demography, whose driver is that mechanism in other nouns, and the
clone check reads mechanisms rather than nouns; the same merge brought in task157, which took the
structural triple, and task190 v2, which took the stakeholder role. Competing risks against censoring
is therefore on this slot's banned list with the rest.

What architecture 3 keeps: the world, the three access routes, the settlement gazetteer, the partner
organisations and their agreements, the ask layer with its devices, and every pack writer that is not
about the decisive quantity. What it discards: the episode construction and its peace interval, the
whole-life cohort estimand, the four survival estimators, the ladder, the prompt, the goldens and the
submission. Its pack, zip, goldens, submission and metadata were removed from the task tree when the
draw was blocked, so that nothing a consumer discovers by name can be graded as this build's
(`reduce-house-fixes` H11); the architecture is on the slot's banned list and will not be rebuilt.

## Architecture 1, spent at stage 3 on measurement

The generator was written far enough to measure the ladder on the record itself, before any file was
cut. Two findings kill the architecture, and neither is a tuning problem.

**1. The default path has no parameter-free answer, and its parameter range covers the golden.**
"Group the flagged location-days that touch in time and place" is a single-linkage clustering, and its
one free parameter is the gap in days it tolerates. Measured on the record (748 location-days, nine
operations, reach 0.70):

| Gap tolerated | Components, no same-day link | Components, same-day link |
|---|---|---|
| 1 day | 673 | 65 |
| 2 days | 598 | 22 |
| 3 days | 562 | **9** |
| 5 days | 310 | 1 |

The count falls monotonically from 673 to 1 and passes through 9, so a solver who tunes the gap to a
sensible-looking cluster count can land the answer without the insight, and no parameter-free reading
of "contiguous" lands on a plausible count: the two parameter-free readings give 65 and 673, which
nobody files as a count of coordinated operations. The design note's 23 was never reproducible. A
ladder whose rung 0 is one live degree of freedom in the graded quantity holds nothing
(`stumping` Part 3), and the sweep over flag rules (seven variants, 196 to 602 flagged cells) moved
the component counts by two or three and never separated them from 9.

**2. The decisive quantity is not one the field estimates, so rule 1 fails on measurement.** The step
is recovering the number of arithmetic progressions in a union of them: per-settlement gcds of the
observed gaps return exactly `[4, 5, 6, 9, 11, 13, 17, 23, 29]` on the 20 settlements one operation
reaches, and nine distinct interval-and-phase pairs. That is signal processing, not conflict event
analysis: no monitoring institute estimates how many periodic processes generated its record, and the
swap reads unchanged with machines on fixed maintenance cycles in place of coordinated operations.
Exact lattices over six months is also the kind of structure a realism read calls constructed.

The architecture is spent. Re-root at stage 1 in the same number and objective. The world (a
Portuguese conflict monitoring institute, three access routes, a settlement gazetteer, partner
organisations under data agreements) is sound and can be kept; the decisive step cannot.

**Ruled out for the re-root, with the reason, so the new draw does not walk into one:**
- capture of one list measured on the overlap with another: task448's driver, spent;
- the selected extreme judged against the record of extremes at the same reach: task191, one build ago;
- a shared external driver with unit-specific lagged response: task182;
- composition against rate: task183, task125, task188;
- a count read before its records have arrived: task190, task457;
- an event entering the record only above a detection threshold that moves on a cycle: task180.

**How architecture 3 clears each of them.** The decisive step is none of the six: nothing is captured
from an overlap (the duplicate reports collapse to one action and the count is invariant to them,
asserted); nothing extreme is selected and no null of extremes is built; no external driver and no lag
appear; the count is a count with no composition against any rate, and although the record's own
composition moves across the period that movement is what rules a method out rather than the quantity
being compared; every report has arrived, the import log closes the one month that arrived twice, and
the gap is in what the classifier made of the reports rather than in the recording; and no detection
threshold exists, the action grain being filed and every accepted item carried.
- **(2026-10-25, measured) A blind reader landed the call exactly, took 92.5 per cent of the ask figures, and reproduced this note's whole ladder as its own list of rejected methods.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **450 confrontational actions** against the golden 450 (its exact 455 against the generator's 454.91), on 4,656 actions built as tema plus gazetteer locality plus occurrence day, and hit **98 of 106 ask figures**. It took the decisive step and said why: because the mix changed after the audited months it corrected the 271 press marks with recall and the false-mark rate only, `true = (marks - FPR x N) / (recall - FPR)`, "that correction does not depend on how common confrontation is, so it carries to the unaudited months". Then it listed, by figure, every rung this note designed: naive 320, recall only 616, times precision 269, audit prevalence 694, hand codes where audited 386. A theme-stratified cross-check gave 466, still rounding to 450.
- **(2026-10-25, measured) The seventh cell is CONFIRMED open by an independent reader.** Asked to fit the calibration model (hand code on classifier mark plus a month index, extrapolated over the two unaudited months) and to say whether anything in the bundle rules it in or out, the reader returned **504, reported as 500**, a different fifty-bucket from the call, and answered: **"Nothing in the bundle rules it in."** It argued against it on three grounds of its own (the audit stops in August, two themes appear only in September so no month or theme term can be fitted for them, and the month term is not significant at p = 0.088), but those are judgements a competent analyst could decide the other way, not a shipped fact. So the Gate C finding recorded above is not a paper worry: it is a reachable candidate on the shipped pack, it has no row in the candidate table and no `cand.*` assertion, and any repair of this number owes its closure.
- **(2026-11-01, the re-check under the new gates) Architecture 3 confirmed spent on the shipped cut; not repaired, not re-rooted.** The rebuild (`python3 task192/generator/build.py`, matplotlib installed into the container) reproduced the shipped target.zip byte for byte (060f8959) with 310 generator assertions and 138 independent checks green. The shipped cut fails three free gates: `leak.py` LEAK on sweep 12 (`protocolo_vigilancia_v4.pdf` names 11 of the data files' columns) and sweep 13 (`metadata.json` committed_answer carries 450); `precut.py` FAIL on SF27 (asserted in `checks.py`, absent from the fork table) with 8 survivor-anatomy WARNs; `guard.py heart` BLOCK on the inherited bans against task266 v1 and task270 v2 recorded on 10-21. voice-check PASS (WARN only on the corpus how-many quota), figures_check 111 of 111. The seventh cell was refitted on the shipped target with the pack's own loader: a logistic calibration of the hand code on the classifier mark alone files 614.530 (the default path), and with a month index added files 504.483 and prints 500 against the golden 450. Closing it needs a filed sentence separating a correction free of how common the class was in the audited months from one that is not, which is the property the decisive step recognises (stumping 1.2, the fork-is-the-stump test), so no closure is available inside this architecture and the leak repairs were not cut on a build the main call cannot ship from.
