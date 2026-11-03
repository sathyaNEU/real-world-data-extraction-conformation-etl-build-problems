# task276 design note

## Draw

Architecture 2 of the reopened slot, re-rooted at the draw on 2026-11-03 into a fresh world and domain (the DA26
developer-community world, the exposure-response draw and architecture 1's twenty-two screens stay dead, `## Tried and
rejected`). Pairing: `urban-regional-science` / `network-analysis` (Descriptive & Distribution Analysis), shape 01
(ranked list, each shortlisted crossing a row). Niche: the Shires Transport Board, a sub-national transport body for
four shire counties (Northshire, Southshire, Eastshire, Westshire), chooses which crossing on its level crossing
replacement shortlist the 2027 scheme replaces; the programme brief files the choice as the crossing whose barrier
closures cost road users the most delay on school-day mornings, 07:00 to 10:00, over the 2025/26 school year.

Abstraction: a stoppage holds a queue, and the cost of the stoppage is the time the queue takes to drain; the field's
model drains it at the road's own capacity, and the step is seeing that at one site the drain runs through a second
control whose open periods and short storage set the pace, so the cost has to be rebuilt through that control's timed
greens. Nearest drivers on file (guard.py check): task472 v1 lineage at 0.08 (a job finished only when its slowest
parallel stream finishes), task109 v1 lineage at 0.06, task173 v4 at 0.05; none is a queue paced by a downstream
control. `slots` on the mechanism words (spillback, blocking back, storage, shuttle signals, downstream signal,
saturation flow) and on the setting words (level crossing, barrier, closure delay, school run) returned no screen.

The committed quantity is retrospective on purpose: the programme's appraisal reads the last full school year's
record to choose the next year's scheme (the timetable and the road network are unchanged into 2027, the brief
says so), so the call faces forward and the measured year is closed.

Guard answers: WARN overuse.org_family (government_agency in 40 builds) is the honest label, a public transport
body; WARN repeat.deliverables (docx and xlsx against task200) is answered at the role level, a crossing workbook and
a panel paper, with the shell drawn as a "what" question ("which" sits over its corpus quota) with a "Build" opener. Personas from
`guard.py names --geo uk --seed 276`: Andrew Stevens (network planning lead), Gareth Davis (programme manager); neither
appears in the prompt.

Data-native sentence: Mill Lane's crossing sits 42 metres from the stop line of a single-track river bridge worked by
fixed-time shuttle signals, so every queue a closure builds there can only leave in the bridge's greens for its own
direction, and that fact lives only in the network links, the node coordinates and the highway authority's signal
timing register, none of which the closure model reads.

## Default path

1. Read `rail/barrier_events_2025_26.csv` (UTC), drop the sensor-bounce repeats, pair each lowering with the next
   raising and convert to UK local time.
2. Take school days from `schools/term_dates_2025_26.xlsx` for each crossing's county (the county from
   `rail/crossing_register_2025.pdf`), bank holidays out, as the programme brief files.
3. Map the approach count sites to crossings through `highways/network_register_2026.xlsx` and spread each
   quarter-hour's count in `highways/approach_counts_2025_26.csv` evenly across its quarter hour (the appraisal
   method's convention).
4. The field's closure model: each vehicle reaching the barriers while they are down waits for the raising, and
   the held queue discharges at the saturation flow, 1,800 vehicles an hour per lane (lanes from
   `highways/network_links.csv`), from the moment the barriers rise; delay is each vehicle's extra time against the
   same morning with no closures.
5. Sum over vehicles counted 07:00 to 10:00 on school days, by crossing, in vehicle-hours; validate the arrivals
   against the 2026 queue survey's queues at barrier rise, which agree at every crossing; rank.

The closure model files Station Road at 7,000 vehicle-hours with Mill Lane second at 5,000 (6,998 against 4,832
unrounded); the golden files Mill Lane at 10,000 against Station Road's 7,000 (10,026 against 6,998), a gap of 3,000.

Ends on: Station Road.

Golden: Mill Lane.

## Stump sentence

A competent analyst replays every closure through the field's closure model, the held queue leaving at 1,800 vehicles
an hour once the barriers rise, and names Station Road (7,000 vehicle-hours against Mill Lane's 5,000); the step
that lands it there is releasing Mill Lane's queues at the road's own rate, when the river bridge's shuttle signals 42
metres beyond the crossing pass each direction only in its own green and hold seven vehicles of storage between them,
so Mill Lane's closures cost 10,000 vehicle-hours and lead.

## Three rules

Task type: network-analysis in urban-regional-science, the delay a network element imposes on the flows through it,
which serves Descriptive & Distribution Analysis in the taxonomy (how the road-user delay of the programme's
crossings is distributed across them).
Domain test: the deciding quantity is the road-user delay each crossing's closures cause, which transport network
analysis estimates with deterministic queueing at the network's controls (the closure model at the saturation flow,
and at any control the released queue reaches, that control's capacity in its own green).
Swap: with "hospital" for "crossing" and "patients" for "vehicles" the sentence loses its meaning: there is no barrier
log, no saturation flow, no shuttle green and no storage in metres between two stop lines to pace a released queue.
Layer 1: the rail infrastructure manager's barrier log in UTC with sensor-bounce repeats; the highway authority's
quarter-hour counts in UK local time across both clock changes, with dropouts outside the peak; the crossing register
as a scanned PDF under the railway's references; the network under the highway authority's node numbers; four county
term calendars with different half terms; a fault work-order export and a signaller's occurrence book, each in its own
keys; two counter models that write the heavy-vehicle column differently.
Layer 2: allocation_constraints, a queue's discharge bounded by the tightest capacity downstream within the queue's
reach, here a fixed-time shuttle signal with seven vehicles of storage between it and the barrier.
Decisive step: recognising that Mill Lane's released queues, westbound and eastbound, are paced by the river bridge's
signals 42 metres away and rebuilding the closures' delay through the bridge's timed greens and the storage between
the two stop lines, rather than through the barrier alone.
Not semantics: every field, code, unit and clock read correctly still leaves the closure model naming Station Road,
because no field says that a control sits within the queue's reach; the bridge is a node 42 metres along a link, and a
site in a timing register keyed by node number.
Not rule application: no filed rule or procedure says where a released queue goes; the brief files the outcome (extra
time to reach the far count site against the same morning without closures), the population, the window and the unit,
and the method files only network constants; the enumerated family (closure count, closure minutes, vehicles held,
the closure model at 1,800, the closure model with the bridge for one direction, the replay through every control in
the section) spreads Mill Lane from 4,832 to 10,026 vehicle-hours and the call between Common Road, Station Road
and Mill Lane; the standing family (the closure model at 1,800 and the replay through the section's controls, both
literal readings of "extra time to reach the far count site" to a reader who has not looked at the section) spreads
Mill Lane from 4,832 to 10,026 and the call from Station Road to Mill Lane; nothing loud rules either out, since no
sentence, column or flag names the bridge's effect.
Analyst test: a strong analyst who pairs the barrier events, reads each closure's arrivals off the approach counts and
releases every held queue at 1,800 vehicles an hour per lane once the barriers rise, the closure model the queue survey
validates at every crossing, names Station Road, when at Mill Lane both directions' queues can only leave in the
bridge's greens and its closures cost the most road time.
Estimand: the programme brief (`programme/crossing_programme_2027.docx`, section 3) files the delay a crossing causes
as the extra time vehicles counted on its approaches between 07:00 and 10:00 on school days take to reach the count
site on the far side of the crossing because the barriers were lowered, against the same morning with the barriers
left raised, summed in vehicle-hours over the 2025/26 school year; the appraisal method files the network constants.
No decoy: nothing is planted: no copied block, hidden rule, memo, draft, briefing or stakeholder figure carries the
wrong answer; the queue survey is the programme's own calibration of arrivals and is true at every crossing, and the
register's risk score is the rail manager's own measure for another purpose.
No certified replay: no certified or published delay figure exists in the pack, so the method cannot be recovered by
reproducing one; the survey records queues at barrier rise, which every route reproduces.
Lesson: a model that gets it right learns that a stoppage's cost is set by the tightest capacity its released queue
meets, so a delay estimate has to walk the network beyond the stoppage; no build on file teaches a queue paced by a
second control within its storage reach.

## Survivor anatomy

Actor: the deciding property, that Mill Lane's released queues meet a second control within seven vehicles of
storage, is a relation between the crossing's node, a 42-metre link and a timing-register row; no file has a column
for it, and no file names both the crossing and the bridge.
Link: the crossing register gives the railway's reference and an OS grid reference, the network gives node numbers
with coordinates, and the timing register gives a site, a node and its greens; the bridge is reached only by matching
the crossing to its node by coordinates and walking the links to the next node, a join no shared key offers.
Reflex: the field's closure model (deterministic queueing at the saturation flow once the barriers rise) is rung 3 and
names Station Road.
Back-test: the 2026 queue survey's vehicles in queue at barrier rise agree with the closure model's arrivals at every
crossing, Mill Lane's two approaches included, because a queue at the rise does not depend on how it leaves.
Second use: the network links file carries each approach's lane count, which the closure model needs (Common Road's
two lanes a direction), and the timing register shares its workbook with the count-site sheet the default path
reads to map counts to crossings; every file the decisive step reads ships for the default path too.
Shock: Mill Lane leads no shipped statistic: second in closure minutes, fifth in closures per morning, sixth in
approach traffic and last of the six on the register's risk ranking; its delay rises only once its queues are walked
to the bridge, and nothing in the record moves at Mill Lane in the year.
Pins: the brief files population, outcome, window, unit and comparison, and the method files saturation flow, vehicle
length and the count spreading; no sentence names the bridge, a signal, a storage or a queue's route, and deleting any
filed sentence leaves the call where it is.

## Readability screen

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 closures per morning (Common Road) | no | no | no | no | no | yes | no | readable |
| R1 closure minutes (Station Road) | no | no | no | no | no | yes | no | readable |
| R2 vehicles held (Station Road) | no | no | no | no | no | yes | no | readable |
| R3 closure model at 1,800 (Station Road) | no | no | yes | no | no | no | no | readable |
| R4 the bridge for the westbound queue only (Mill Lane) | no | no | no | no | no | no | no | silent |
| R5 replay through every control in the section (decisive) | no | no | no | no | no | no | no | silent |

Test 1: no clause names a downstream control, a storage or a queue's route. Test 2: no column or flag marks the bridge
as Mill Lane's; the timing register is keyed by node. Test 3: the reflex is the closure model (R3), which names Station
Road. Test 4: the survey agrees with every route. Test 5: the battery (bounces, clocks, calendars) moves no rank.
Test 6: the gated delay is a replay through two controls with storage, not one subtraction. Test 7: every file R5 reads
ships for R3 as well (Second use).

## Semantic fork table

| ID | Term or convention | Alternatives | Ruled out by |
|---|---|---|---|
| SF1 | a closure | lowering to raising as logged; lights to raising | the method files lowering to raising; the log has only those events |
| SF2 | the barrier log's clock | UTC; local | the column is `event_time_utc`; the counts' local clock shows in both clock changes |
| SF3 | school days | term weekdays of the crossing's county; any county's; all weekdays | the brief files the crossing's own county's term dates with bank holidays out |
| SF4 | the vehicles counted | counted 07:00 to 10:00; held in the window | the brief files vehicles counted at the approach sites 07:00 to 10:00; same call |
| SF5 | delay | extra time to the far count site against no closures; time at the barrier | the brief's sentence; Station Road and every non-Mill crossing identical either way |
| SF6 | saturation flow | 1,800 per lane; per approach | the method files 1,800 an hour per lane; lanes in the links file |
| SF7 | arrivals within a quarter hour | evenly spread; at the start; random | the method files evenly spread; the start reading moves no figure out of its bin |
| SF8 | storage between the stop lines | 42 m at 5.75 m a vehicle, seven; six; eight | the method files 5.75 m; floor and nearest agree on seven; six and eight keep every bin |
| SF9 | effective green | the displayed green; less a lost time | the timing register's note: effective green is taken as the displayed green |
| SF10 | travel inside the section | point queues; a few seconds stop line to stop line | same call; up to five seconds keeps Mill Lane's bin |
| SF11 | sensor-bounce repeats | dropped; kept | a repeat of the same event within three seconds; kept, a lowering pairs with the next raising either way; same call |
| SF12 | vehicles counted before 07:00 | out of the sum, in the replay; out of both | the brief counts vehicles from 07:00 and the replay starts at 06:00; starting at 07:00 keeps every bin |
| SF13 | delay running past 10:00 | counted in full; cut at 10:00 | the brief sums each counted vehicle's extra time; same call |
| SF14 | the gap | from unrounded figures; from rounded | the prompt rounds the figures and the gap; both give 3,000 |
| SF15 | closures per morning | closures begun 07:00 to 10:00 per school morning | the asking sentence |
| SF16 | a closure a fault held down | a closure during which a road-closing fault was reported or reset | the asking sentence's words and both fault records |
| SF17 | the heavy goods vehicle share | both approaches' vehicles counted 07:00 to 10:00 on school days | the asking sentence |
| SF18 | the fault window | 1 September 2025 to 31 August 2026, every hour the log covers | the asking sentence |
| SF19 | count dropouts | none in the window | asserted: no school-day site misses a quarter hour from 06:00 to 11:00 |
| SF20 | Common Road's lanes | two a direction | the links file; the closure model and the replay agree |

## Ladder

| Rung | Route | Names | Margin over the next |
|---|---|---|---|
| R0 | closures begun per school morning | Common Road | 1.20 over Church Lane |
| R1 | barrier-down minutes per school morning | Station Road | 1.18 over Mill Lane |
| R2 | vehicles arriving while the barriers are down | Station Road | 1.20 over Mill Lane |
| R3 | the closure model at 1,800 an hour per lane (the field's reflex) | Station Road | 1.45 over Mill Lane |
| R4 | the bridge for the westbound queue only | Mill Lane | 1.37 over Station Road |
| R5 | the replay through every control in the section (golden) | Mill Lane | 1.43 over Station Road |

Every rung's margin is asserted in `checks.py` on the cut pack at 1.15 or more; the cheap routes that reach Mill Lane
are R4 and R5, both through the bridge. Mill Lane's figure under every reasonable convention (storage six or eight,
two or five seconds between stop lines, counts at the start of their quarter hour, the replay begun at 07:00) runs
9,675 to 10,439 and the gap 2,677 to 3,441, each inside its thousand, asserted.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | vehicles counted on each shortlisted crossing's approaches 07:00 to 10:00 on its county's school days | filed in the brief; C1 |
| 2 Unit of account | the vehicle | filed; C1 |
| 3 Attribution window | the 2025/26 school year, 3 September 2025 to 22 July 2026 as each county's terms run | filed; C1 |
| 4 As-of dating | the record as exported in September 2026 | C1 |
| 5 Version basis | one export of each file | C1 |
| 6 Denominator | none (a sum) | C1 |
| 7 Weighting | none, each vehicle once | filed; C1 |
| 8 Window length | the three-hour morning | filed; C1 |
| 9 Boundary inclusivity | counted from 07:00 up to 10:00 | filed by quarter hours; C1 |
| 10 Rounding path | vehicle-hours summed, rounded once to the nearest thousand | the prompt; asserted mid-bin |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | the year is closed | C1 |
| 13 Order of operations | pair, convert, select days, replay, sum | C1 |
| 14 Row order | file order | asserted over shuffles |
| 15 Duplicate resolution | bounce repeats dropped | SF11; same call |
| 16 Identity normalisation | crossing to node by coordinates, count site to node by register | C4, asserted |
| 17 Netting against gross | the no-closure morning netted from the closure morning | filed (SF5) |
| 18 Dimensional units | seconds, vehicles, metres, vehicle-hours | filed |
| 19 Code and status semantics | LOWERED and RAISED | C1 |
| 20 Integerisation | storage seven vehicles | SF8 |
| 21 Clause scope | saturation flow per lane at every stop line | filed (SF6, SF9) |
| 22 Forward window contents | the 2027 scheme replaces one shortlisted crossing | filed in the brief |

## Literal reader

Executed on paper word for word: the brief's sentence fixes the population (vehicles counted 07:00 to 10:00 on the
crossing's county's school days), the outcome (the extra time to reach the far count site because the barriers were
lowered), the comparison (the same morning with the barriers left raised), the window and the unit; the method fixes
the saturation flow, the vehicle length and the spreading of counts; the timing register fixes each signal site's
greens. Executing it at Mill Lane means replaying the section between its two count sites, which holds the crossing
and the bridge; the literal execution is the golden, and the closure model is its execution at a crossing with no
control in its section.

## Oracles

None: no shipped figure ranks the crossings on delay; the queue survey agrees with every route; the risk score is the
rail manager's own measure and is named a distractor in `metadata.json`.

## Ask sheet

Two asks per crossing, each a reconstruction across two systems or grains that no sentence states, sited on rows and
columns the main call never reads (fault closures outside the school-day mornings; the heavy-vehicle column), each with
two primaries from different families on disjoint figure blocks.

**Ask A, fault-held closure hours.** Each crossing's hours of barrier closure, 1 September 2025 to 31 August 2026, in
closures a fault held down. Use: the panel's reliability case (a replaced crossing has no barrier faults). H18 home: a
measure every candidate carries that the call does not turn on. Primary F1 (D4, absence evidenced in a file no habitual
join reaches): a fault the signaller cleared by resetting the crossing from the box raises no work order and lives only
in the signaller's occurrence book, written after the reset, so its time falls after the closure it held. Primary F2
(D9, a record true only in its scope): a work order runs from the fault report to the technician's sign-off, which is
not the closure; the closure is the barrier log's lowering to raising. Primary F3 (D7, the true key elsewhere): Long
Drove's barrier machine was renewed in February 2026 and its new asset number is in no register, so its later work
orders join to no crossing until their times are matched to the barrier log. Hazard: the UTC log against local
work orders (H1). F1 moves Station Road, Common Road and Church Lane; F3 moves Long Drove; Mill Lane's and
Moor Road's fault hours carry no device. Files: `rail/barrier_events_2025_26.csv`,
`rail/fault_work_orders_2025_26.csv`, `rail/signaller_occurrences_2025_26.xlsx`, `rail/crossing_register_2025.pdf`;
9 columns on the path. Stops: work-order spans by asset (the lazy read); barrier closures matched to work orders (the
careful route); plus the occurrence book's faults matched to the closure before their entry (the full includer short
of F3); every fault's closure, Long Drove's renewed machine matched by time (golden). Pin test: the sentence carries
the window, the unit and "a fault held down"; the devices sit in which records are faults, which closure each one
held and which crossing an unregistered machine serves, none of which the pins name.

**Ask B, heavy goods vehicle share.** Each crossing's heavy goods vehicles as a share of the vehicles counted on its
approaches 07:00 to 10:00 on school days. Use: the business case values goods-vehicle time above car time. Primary F4
(D3, units set per source): the older counter model writes the heavy-vehicle column as a whole-number percentage of
the quarter hour's vehicles, which reads as a count without an error; the evidence is internal (at those sites the
column does not rise with the flow). Primary F5 (D2, a label stored before a silent switch): two sites changed from
the older model to the newer on 8 April 2026, and the register shows each site's current counter with its install
date only, so a model join by site reads their autumn rows as counts. Hazard: county term dates (H3). F4 moves Common
Road, Long Drove and Moor Road; F5 moves Common Road and Church Lane. Files:
`highways/approach_counts_2025_26.csv`, `highways/network_register_2026.xlsx`, `schools/term_dates_2025_26.xlsx`,
`rail/crossing_register_2025.pdf`; 8 columns on the path. Stops: the column read as counts everywhere (the lazy read
and the careful route); the register's older-model sites converted (the full includer short of F5); every row of the
older model converted by its own dates (golden). Pin test: the sentence carries the population, window, unit and
rounding; the devices sit in which rows' heavy column is a share, which no pin names.

Main population zero-counts (asserted in `checks.py` from the shipped rows): no fault work order, occurrence entry or
long closure falls on a school day between 06:00 and 11:00 local; no count site misses a quarter hour on a school day
between 06:00 and 11:00; deleting every ask device leaves every delay figure identical.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| H1 UTC log against local work orders and occurrences | A | every crossing's fault hours move when unconverted (matches lost in summer time) |
| H3 county term dates | B, main | the share moves at the second decimal; the delay bins hold |

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | barrier-log closures matched to the work orders through the register's asset numbers, clocks converted, bounce repeats dropped | miss |
| B | heavy column summed over vehicles counted 07:00 to 10:00 on school days, read as the counts its header says | miss |

Mirror leakage: 33.3 per cent of ask weight, the best miss (the closure model, Station Road) taking the same careful
routes on both asks and keeping the four figures no device reaches (Mill Lane's and Moor Road's fault hours, Station
Road's and Mill Lane's heavy shares, whose counters were never the older model).
Pair ceiling: 46.8 on the cracker (63.3) and mirror (30.3) rows; 58.3 with the full includer on the call (86.2,
every finding but F3 and F5), recomputed by the script on the cut pack.
Measured by: `generator/ceiling.py` on the cut pack, with every route's figure-by-figure miss asserted in
`generator/checks.py`; the single-finding lifts are F1 25.0, F3 8.3, F4 16.7 and F5 16.7 per cent of ask weight,
none over a third.
`generator/checks.py`, and no single finding keeping over a third of the ask weight.

## Leak sweep answers

`leak.py --asof 2026-09-14` on the final cut: REVIEW, no LEAK. One line per REVIEW:
- Brief, figure 3.3: the paper's own paragraph number (3.3 School days), not the fault-hours figure it equals.
- Brief, Church Lane beside decision words: the shortlist table names every crossing with its railway reference and
  county; no figure ranks them.
- Brief, stump terms (closure, bridge, network, station): barrier closures are the decision quantity, the bridge is the
  replacement scheme's own type (a road bridge or a realignment), the network clause says the roads are unchanged into
  2027, and Station is a crossing's name; nothing names a queue's route or a control.
- Appraisal conventions, stump terms (register, control, survey, counts, saturation, signal): the Board's general
  conventions for every delay estimate its programmes make; the signal item is one of six and names no crossing, no
  storage and no queue route. This is the pack's sharpest REVIEW and the leak reader's question 1 is asked of it.
- Crossing register, stump terms (register, control, station) and candidates beside numbers: the rail manager's own
  register with census figures and risk rankings; it does not rank on delay, and its risk ranking puts Common Road and
  Church Lane highest and Mill Lane last, a safety measure for another purpose.
- Network register, queue survey, occurrence book, candidates beside numbers: count sites and signal sites keyed by node,
  queues at barrier rise, and occurrence entries; none ranks the crossings on delay, and the survey agrees with every
  route at every crossing (`checks.py` T1).
- Sweep 13 was LEAK on the first cut (metadata's prompt shape used the word closure, and a stated-inputs list carried
  1,800): reworded, the list dropped and the saturation flow taken out of block 1, so the figure sits only in the
  filed conventions and in block 3's steps.
- Sweep 12 was LEAK on the first cut (the brief named nine column names verbatim): the data files' columns were renamed
  to their systems' own forms (`lx_ref`, `veh_total`, `asset_no`, `reported_at`) and the sweep is clean.

## House fixes

- H21: the counter brand (a Norwegian town's name), two signal box names (real Yorkshire and Lincolnshire places), and
  A and B road numbers that exist on the national network were renamed in the generator (RX-5, Westshire line panel,
  Eastshire line box, local C numbers); no graded figure moved.
- H1: every docx, xlsx and pdf, goldens included, scrubbed after save and laid out as Office saves it (sweep 10 clean).
- H4, H7: target.zip holds the files under `target/` only, cut from the second of two byte-identical builds.
- H8, H23: the write-up's citations resolve (brief 3.2 and 3.3, conventions 3); every ask reads with none as an answer.

## Duplicate check

`guard.py heart task276`: WARN, no BLOCK (government_agency overuse; the docx and xlsx set against task200), nearest
driver task472 v1 lineage at 0.08, nearest stump task254 v3 at 0.07. `guard.py surface task276` promoted two pairs on card
structure alone, task159 (surface 0.025) and task147 (0.020): the same gap, pattern G8, Gate G and calibration form,
which the card's differentiation lines answer (no service with room and no request taken whole; a continuous road
queue paced through a downstream signal, read on the timed greens). The surface text is in the corpus's fourteenth to
sixteenth percentile; the adjudicated read is the author's `/clone-check`.

## Tried and rejected

- Overlap and saturation alone (`binding_constraint`, G8): the first-order correction a careful analyst makes by reflex (collaborators already seeded cannot be invited) lands the call, and overlap among invitees is a second-order effect at launch densities that stay plausible.
- Acceptance delay completed community by community (`maturity_censoring`): the nowcast by unit-specific delay is task181's and task451's driver.
- A dated platform campaign inflating some pilots (`decomposition_attribution`): a cause with a cutover date is adjusted by reflex (the strategy record, F8).
- The pilots' evidence judged at the pilot rather than the invitation (`uncertainty_hold`): the client's record has interval stumps landing on the natural computation.
- Exposure-response at launch density (`composition_mix`, pattern E, 2026-10-24): a developer's chance of accepting rises steeply with how many seeded collaborators invite, read at each member's own invitation count at launch density, is task175's driver (a unit's chance of being taken rises steeply with how many units on its own run are already taken, read at its own run's fill and carried run by run) with the count created by the seeding instead of found on the street; `guard.py check` scored it 0.06 against task175 and passed it with WARNs only, so the repeat was found by the abstraction test, not the guard.
- A1.1 Year-one retention by market against the month's sign-ups, when members who leave erase their accounts (in-app deletion under App Store guideline 5.1.1(v) and GDPR Article 17) and the accounts table and the analytics export hold only accounts not erased (Product Analytics, metric-definition-measurement-science, `population_selection`, G9): the strongest; honest, prototyped, and the routes separate, but `guard.py check` BLOCKs `test.same_driver` inside the twelve-build window (population, G9, method_or_model_selection against task270's v1 and v6 lineage), the G12 reading of the same step BLOCKs against task268 v2 and task273 v1 lineage, and no honest redraw of the gap or the pattern keeps the mechanism, so it cannot register. Written in full below.
- A1.2 The share of checkout requests over a latency line from traces weighted by their recorded sample rate, when the collector's rate limit drops traces at peak minutes without changing the recorded rate (Product Analytics, metric-definition-measurement-science): the swap fails (a laboratory audit desk with a daily cap reads the same; inclusion probabilities under a capacity cap are generic survey sampling), so the domain is a backdrop. Written in full below.
- A1.3 Block parking occupancy for a demand-responsive rate change, from paid space-hours that miss free placard parkers, completed from enforcement licence-plate sweeps matched to pay-by-plate sessions (General Statistics, missing-data-censoring-measurement-error): all seven anatomy lines hold on paper, but the abstraction sentence (the part a measuring channel misses is completed from a second channel's sample cell by cell and added) is task275's, approved. Written in full below.
- A1.4 A release's store rating read from reviews posted during a phased release (Product Analytics): regressing each day's ratings on the day's version mix from the analytics is task263's driver (each source's own level measured only in mixtures whose proportions change), spent. Written in full below.
- A1.5 A free plan's monthly limit set from a usage distribution held down by the current rolling-window cap (Product Analytics, metric-definition): the capped rows hand over the signal (stumping Part 3, step 7), and the uncensored demand above the cap needs a fitted model with a free parameter (Gate C).
- A1.6 Checkout funnel losses at a payment step that hands the buyer to a bank app and returns them under a new browser identity (Product Analytics, funnel-journey-analysis): identity resolution carried by Layer 1; once the join is cleaned the call is easy.
- A1.7 Multi-visit web funnels fragmented by WebKit's seven-day cap on script-set cookies (Product Analytics, funnel-journey-analysis): a reflex for web analysts and a reading of a platform behaviour (data semantics).
- A1.8 A candidate primary metric scored for sensitivity on an experiment corpus whose experiments were stopped early on the old primary metric (Product Analytics, metric-definition): the swap fails (a hospital's trials stopped on the old endpoint read the same) and each experiment's planned horizon is a registry column (the schema test).
- A1.9 Push deliveries under APNs store-and-forward coalescing once the 2027 schedule sends more alerts (Product Analytics, metric-definition): devices' offline spells are unobservable at the new schedule's resolution, a free-parameter model (Gate C), and the effect is small outside a few segments.
- A1.10 New items' first-week views held down until the next recommendation-model retrain, carried to a daily cadence (Product Analytics, feature-adoption-diffusion-modeling): task258's abstraction (an effect that reaches only the units a step's condition lets it reach), and the step rides on an as-of time join (time semantics risk).
- A1.11 A legacy feature's distinct users over 2027 read from an event log retained for six months (Product Analytics, feature-adoption): the off-window seasonal users are absent (Gate B) and any projection is a fitted reach model, the field's method as the golden or a fork.
- A1.12 Email-verification losses from deliveries deferred at corporate mail gateways (Product Analytics, funnel-journey-analysis): a root-cause question; the losses are real losses at the step, so the descriptive answer does not move.
- A1.13 A new version's crash rate during a phased release with self-selected manual updaters mixed into the random slice (Product Analytics, metric-definition): a comparison-group question, `causal_design` (banned against task157) and Experiment and Causal Analysis ground.
- A1.14 Durable usage inflated by in-product prompts (Product Analytics, feature-adoption): already dead in this slot (a dated campaign adjusted by reflex).
- A1.15 Search requests' tail latency once the index is split across more shards and every request waits for its slowest shard (Product Analytics, metric-definition): the swap fails (a discharge that waits on every laboratory result reads the same).
- A1.16 Life expectancy of a group under-recorded on death certificates, corrected locally through a linkage to an enrolment register (Sociology, fertility-mortality-life-table-estimation): misclassification among decedents outside the register is absent (Gate B), and carrying the linked rate within a place is task124's abstraction.
- A1.17 Ward peak occupancy against the midnight census (Healthcare, provider-quality-risk-adjustment): the estimand's clock (midnight against hourly) is the step, a WHAT fork (stumping 1.2).
- A1.18 Claims-based disease prevalence by area with practice-dependent coding intensity (Healthcare, provider-quality-risk-adjustment): task271 v1's driver (a risk property recorded at other units), and the honest label `composition_mix` is banned against task166.
- A1.19 Small-area support for a ballot measure by MRP with engagement-driven nonresponse corrected through voter-file turnout (Political Science, small-area-public-opinion-estimation-mrp): several defensible model specifications split the districts near the line (Gate C).
- A1.20 Brand duplication inflated by shared store access (Marketing, segmentation-market-structure): the honest label `composition_mix` is banned against task166 and partitioning by distribution is a known correction in the duplication-of-purchase literature (reflex).
- A1.21 A port passenger survey whose interviewers fall behind at peak hours, so realised sampling rates fall under the designed interval (Survey Research, sample-design-allocation-weighting): post-stratifying by hour is a grouping (stumping 1.1c), which the data separate by reflex.
- A1.22 Plan-limit and pricing replays (seat licences, AI token costs under a new cache rule, per-organisation rate limits) over the 2026 history (Product Analytics, metric-definition): executing a filed plan rule over the history is rule application.
- The four strongest written in full, as the orchestrating session asked. A1.1: default path, each matured monthly cohort (November 2024 to October 2025) built from the accounts table's sign-up date and country, a member retained when the analytics export shows a session in the twelfth month after the sign-up month, pooled by market (or cohort rates averaged, or a Kaplan-Meier on the last active month), the market with the highest rate named; the analytics vendor's own retention dashboard agrees because the vendor honours the same erasures; ends on the market whose leavers erase most (the prototype: Germany, 0.268, against Spain 0.210). Golden: retention over the month's sign-ups, the erased members placed in their cohorts by the account id's order among surviving ids and their country from the request register's residence field, counted not retained unless the erasure came after their twelfth month, those few bounded both ways: Spain, 0.192, bounds 0.190 to 0.195, Portugal next at 0.181. Swap: holds (a hospital cannot erase a patient's record under records-retention law and a utility keeps a leaver's account for years, so the route that removes leavers does not exist there). Anatomy: Actor holds (whether a sign-up later erased their account has no column; the erased are absent), Link holds (the register keys requests by an account id the accounts table no longer holds; the cohort comes from the id order), Reflex holds (the cohort retention table files the wrong market), Back-test holds (the vendor dashboard agrees with the survivors), Second use holds (the register sits for a GDPR one-month completion ask), Shock open (the high-erasure markets lead the survivors' ranking by a visible margin), Pins hold (the plan files retention over the month's sign-ups and no sentence names erasure). Bin: margins 1.08 on the survivors and 1.06 on the sign-ups, both under the 1.15 floor, with erasure shares of 9 to 37 per cent of sign-ups; realistic shares of 10 to 25 per cent bound the swing. Prototype: a seeded replay of ten markets' sign-ups, monthly activity and erasure behaviour (leavers erase at a market-specific rate, stayers rarely, a delay after the last session), run in the session scratchpad and not kept in the pack. Guard: BLOCK as A1.1 states. A1.2: default path, each request's latency weighted by its trace's recorded sample rate, the share over one second, which reconciles with the load balancer's per-minute counts within 2 per cent on monthly volume and understates the peak-minute tail; swap fails; Actor, Link (kept traces per second against the load balancer's counts), Reflex, Back-test, Second use, Shock and Pins hold on paper; bin not reached; dead on the swap. A1.3: default path, paid space-hours over available space-hours by block and rate period, validated on the 2019 sensor pilot's low-placard blocks; golden adds the unpaid occupancy the sweeps read cell by cell; swap holds; all seven anatomy lines hold; bin a ratio estimator with a corridor; dead on task275's abstraction. A1.4: default path, the rating before and after the release date; golden the daily rating regressed on the day's version mix; swap holds; Link holds (the store's reviews carry no version, the mix comes from the analytics); Shock open; dead on task263's driver.
- A2.0 (2026-11-03, architecture 2's draw): the count of vehicles held over five minutes as the deciding quantity. Died
  on the prototype: with the bridge near its capacity the count above five minutes moved by a factor of four between
  neighbouring storage settings, so the graded figure had no stable bin; the deciding quantity moved to the closures'
  vehicle-hours, whose spread across every reasonable convention is about three per cent.
- A2.1: the first card check BLOCKed on `ban.pattern` (C against task241) and on the older same-puzzle and same-driver
  tests against task147 and task159 with G7 decisive; G7 with pick_one_of_n hard-blocks against task307 inside the
  twelve. Redrawn to pattern none with G8 decisive and differentiation lines against task147 and task159.
- A2.2: a downstream signal 400 metres beyond the crossing. Rejected: the estimand's section would have to reach it at
  every crossing, and a far count site that counts departures records the slow discharge directly, a back-test that
  refutes the closure model at the stump crossing in plain sight.
- A2.3: approach counters that count both directions. Rejected for the same reason: the departure lane is a Newell
  input-output measurement of the paced discharge, a second route to the golden that needs no network walk.
- A2.4: vehicle-actuated bridge signals with logged greens. Rejected: the greens on a morning without closures are
  unknowable, so the comparison the brief files has two readings (Gate C); fixed-time shuttle working in the
  morning plan closes it.
- A2.5: a signal lost-time convention left open. Rejected after measuring it: two seconds of lost time a green moved
  Mill Lane's figure by 31 per cent, far outside any bin; the timing register's own note files effective green as the
  displayed green.
- A2.6: crossing, county and bridge names drawn as invented place names (Sallowby, Tewsley, Hawsby). Renamed to
  descriptive road names under H21: two of them sat within two letters of real villages.
