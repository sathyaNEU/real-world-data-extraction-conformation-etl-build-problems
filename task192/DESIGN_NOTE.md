# task192 design note

Counting how many coordinated operations stand behind overlapping bursts of recorded events.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task192.json`, filed and committed with this note |
| Domain, task type | political-science-public-policy, `conflict-protest-event-data-analysis` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 17, periods around a change point |
| Decision | quantity_figure, a count |
| Gate G | `decomposition_attribution`; decisive generator G10, G6 |
| Strategy | `other`, the count of processes behind a superposition |
| Layer 2 | `estimand_identification`, own pattern `own:count-of-processes-behind-a-superposition` |
| World | Portugal, a conflict monitoring institute, EUR |
| As-of date | 2026-11-06 |
| Guard | registered at PASS |

**Data-native sentence.** Every operation in this record runs to its own calendar, one action every
few days from a fixed start, and because the operations share locations, two of them land on the same
place on the same day often enough that contiguous runs of flagged location-days merge them, while an
operation whose interval skips a beat is split in two. The only thing in the record that belongs to
one operation and not to its neighbours is the interval between its own actions.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD15: the decision shape only, a count of coordinated
  operations committed to a standing body. Its own architecture turns on a stated definition of a
  campaign plus a verification subsample that blesses one reading, which is rule application with a
  certified replay, so the card re-roots on the field's own estimate of how many processes generated
  the bursts.
- `guard.py mechanisms --objective anomaly-detection`: the spent drivers are detection delay by
  route, a count read before its records arrive, a check that sees a unit before it resets, a yield
  carried onto another base rate, and now a stock read as a flow. None of them decomposes a
  superposition.
- `guard.py nearest` on the driver: the card's own differentiation line against task98 v7, whose
  decisive move is a double removal across two dated lists. Nothing on file counts generating
  processes.

## Default path

1. Read `event_reports_minute.csv`, one row per recorded event at one location in one minute, and
   `coordination_flags.csv`, the institute's own per location-day flag.
2. Resolve the two language feeds and the re-imported month so each event is counted once, and read
   the timestamps in local time across the 25 October clock change.
3. Keep the flagged location-days inside the reporting window.
4. Group the flagged location-days that touch in time and place, treating a group as one operation.
5. Count the groups and file that number.

**Ends on:** 23 operations.
**Golden:** 9 operations.

## Stump sentence

A competent solver cleans the feeds, groups the flagged location-days that touch in time and place,
counts the groups and files **23 operations**, which counts where the operations overlap and where
their own intervals skip rather than the operations themselves, because two operations hit the same
location on the same day often enough to merge and every operation's interval leaves gaps that split
it.

## Three rules

- **Task type:** `conflict-protest-event-data-analysis`, the task type in Political Science & Public
  Policy that serves Anomaly Detection: separating a real coordinated process in an event record from
  the artifacts of how the record was assembled.
- **Domain test:** the deciding quantity is how many point processes generated an observed
  superposition, which event-data analysis recovers from the tempo each process imposes, the interval
  between one operation's own actions, rather than from the shape of the merged series. Swap the
  coordinated operations for shops counted once each and there is no superposition to decompose and
  no tempo to read, so the count is a row count and the task is gone.
- **Swap:** "how many shops in the district took part in the strike" counts rows in a register, since
  each shop appears once and nothing overlaps. What breaks is that one operation produces many rows at
  many places, two operations produce rows at the same place on the same day, and the count the
  decision needs is of neither rows nor runs.
- **Layer 1:** the institute's own pipeline produces all of it. Events arrive at minute grain from
  two access routes, a media monitor and a partner network, and the two language feeds overlap so the
  same action is reported twice in different words; the coordination flag file sits at location-day
  grain while the events sit at location-minute; the timestamps are local and the clocks go back an
  hour on 25 October 2026 inside the window, so one hour repeats; one month was re-imported and is
  present twice; the partner network's own tables arrive inside PDFs. None of it is placed to be
  caught and none of it decides the count.
- **Layer 2:** `estimand_identification`. The methodological choice is what the count is of: the runs
  the record shows, or the processes that generated them.
- **Decisive step:** recover the number of distinct generating processes from the intervals between
  actions, because each operation repeats on its own interval from its own start and the locations it
  alone touches show that interval unmixed.
- **Not semantics:** every field, code, unit and timestamp read correctly still leaves the flagged
  location-days, which are correct, and the runs they form, which are also correct. The dictionary
  gives every field, the protocol defines the flag, and the calendar note gives the clock change.
  Reading all of it right is what produces the 23 runs, which is the wrong answer's input.
- **Not rule application:** the protocol defines an operation as a series of actions carried out by
  one coordinating group to one plan, and files the window and what counts as an action. No shipped
  sentence says how the operations are told apart or counted, nothing names an interval, a tempo, a
  period or a run, and a word sweep over every shipped file asserts it.
- **Analyst test:** a strong analyst who resolves both feeds, drops the re-imported month, reads the
  clocks correctly and applies the protocol's definition of an action groups the flagged
  location-days by contiguity in time and place and files 23 operations, the default path's
  `Ends on:`, where 9 operations generated the record.
- **Estimand:** the monitoring protocol's paragraph 3.1: "The bulletin reports the number of distinct
  operations that carried out at least one action in the reporting period, an operation being a series
  of actions carried out by one coordinating group to one plan." The population, the outcome, the
  window and the unit are there; how one operation is told from another is not.
- **No decoy:** nothing is planted to be caught. No block of events is copied, no memo argues a
  count, no stakeholder figure carries one, and the institute's own flag file flags location-days
  without grouping or counting them. The re-imported month is an ordinary pipeline fact and is
  visible in the import log.
- **No certified replay:** no published count ships. The institute's previous bulletins report action
  counts and locations touched, never operations, so no method can be recovered by reproducing one.
- **Lesson:** when many periodic processes share a stage, the count of processes is not the count of
  runs: runs merge where processes coincide and split where a process skips, and only each process's
  own tempo survives the superposition. No build on file teaches it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 contiguous runs of flagged location-days | the protocol defines an action and an operation, never a run | the flag file's own grain invites the grouping | yes, the first grouping anyone writes | none | the battery finds the duplicate feeds, not the grouping | one pass over sorted dates | readable |
| 1 runs with the singletons dropped | no | no | yes, the minimum-size reflex | none | no | one filter | readable |
| 2 a spatiotemporal clustering with a tuned radius | no | the location coordinates are there | yes, the clustering reflex | none | no | no | readable |
| 3 the distinct intervals between one operation's own actions (decisive) | no sentence names an interval, a tempo, a period, a cycle or a run, asserted by a word sweep over every shipped file | no column holds an interval; the dates are ordinary event fields the whole ladder reads | no reflex computes a tempo: the three groupings each file a different count and none of them looks at spacing | nothing scores a count; the earlier bulletins report actions and locations, never operations | the battery finds the two feeds and the re-import and leaves the count open | no: it is the number of distinct arithmetic progressions in a union of them | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | operation | a series of actions by one coordinating group to one plan, paragraph 3.1 | a run of flagged location-days, or a location | the count changes | paragraph 3.1, quoted; asserted |
| SF2 | action | one event the protocol counts, at one location on one day | one recorded report, so a double-reported action counts twice | the count of actions changes and the intervals break | paragraph 2.2's definition of an action and the dictionary's report identifier; asserted |
| SF3 | the reporting period | 1 May to 30 October 2026 | the calendar half year, or to the extract date | the count changes | paragraph 3.2, quoted, and the prompt's period close |
| SF4 | the clock | local time, with the hour that repeats on 25 October resolved by the report identifier's sequence | UTC, or the repeated hour collapsed | two actions move between days | the dictionary's local time sentence and the calendar note, both quoted; asserted that no action's day changes |
| SF5 | at least one action in the period | an operation with an action inside the window | an operation whose plan was running, whether or not it acted | `same call`, asserted: every operation in the record acted at least three times inside the window |
| SF6 | distinct operations | distinct by their own interval and start | distinct by the set of locations they touch | `same call`, asserted: the two readings give the same nine |
| SF7 | the re-imported month | the events of the re-imported month counted once | counted twice, or the month dropped | the count of actions changes, not the count of operations | the import log's own two entries for one month and the report identifiers, which repeat exactly; asserted both ways |
| SF8 | the two language feeds | one action however many feeds report it | one action per feed | the count of actions changes and the intervals break | the dictionary's report identifier sentence; asserted |
| SF9 | a location | the gazetteer's own settlement, with the two renamed ones resolved | the free-text place name as reported | the locations split and the intervals break | the gazetteer and its superseded names; asserted |
| SF10 | rounding | none: the answer is a count | the count of actions rounded to a round number | `same call`, no figure in the main call is rounded |
| SF11 | ties | none: the nine intervals are distinct and none is a multiple of another | two operations on one interval, which could not be separated | `same call`, asserted: all nine intervals distinct and pairwise non-dividing |
| SF12 | the flag | the institute's own suspicion flag, which the count does not rest on | the flag as the definition of an operation | the count changes | paragraph 3.1 defines an operation and paragraph 4.3 says the flag is a working aid; asserted that the answer holds with the flag file deleted |
| SF13 | the change point | the fortnight the partner network's reports begin | a change in activity | `same call`, asserted: the operations' own intervals are unchanged across it |
| SF14 | one action per location per day | an operation acting twice at one location on one day is one action there | two actions | the count of actions changes, not the operations | paragraph 2.2, quoted; asserted |

## Ladder

| Rung | The analysis | The count |
|---|---|---|
| 0 | contiguous runs of flagged location-days | **23** |
| 1 | the same with the single-day runs dropped | 17 |
| 2 | a spatiotemporal clustering of the flagged location-days | 12 |
| 3 | **answer:** the distinct intervals the actions repeat on | **9** |

**Separation.** 23, 17, 12 and 9 are four distinct counts, each more than 6 per cent from the next
(23 to 17 is 35 per cent, 17 to 12 is 42 per cent, 12 to 9 is 33 per cent), and each is the complete
output of a competent pipeline. The answer is the extreme of the four, so a solver cannot land it by
stopping early.

**The grid.** Two axes, feed resolution and what is counted:

| | runs | runs without singletons | clustered | distinct intervals |
|---|---|---|---|---|
| feeds and re-import resolved | 23 | 17 | 12 | **9** |
| feeds doubled or the month twice | 31 | 21 | 14 | 9 |

Every cell is a named count. The decisive step is the only one that reverses: the intervals survive
the duplication, because a doubled report does not change the day an action happened, so the cleaning
is worth the ask criteria and the count is worth the call. That is also the fairness the ladder needs:
a solver who misses the duplicate feeds still gets the count right if they find the tempo.

**Dominance.** The operation the ladder turns on is the one on the shortest interval: it acts often
enough to collide with three others, so contiguity merges it into their runs and clustering buries it,
while its own sole-hit locations show its interval unmixed.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which events are in the record | paragraph 3.2 files the window; the gazetteer files the locations; asserted |
| 2 | Unit of account | the action, the report, the location-day | paragraph 2.2 files the action as one location on one day; asserted |
| 3 | Attribution window | which day an event falls in | the local calendar day; no action within 70 minutes of midnight, asserted |
| 4 | As-of dating | the record at the extract | the extract date is filed; the window closed a week before it, asserted |
| 5 | Version basis | the re-imported month and the superseded place names | the import log and the gazetteer; C1, asserted |
| 6 | Denominator | none: the answer is a count | nothing to close, stated |
| 7 | Weighting | none: operations are counted, not weighted | stated |
| 8 | Window length | the reporting period | paragraph 3.2; asserted that every operation acts at least three times inside it |
| 9 | Boundary inclusivity | 1 May and 30 October | paragraph 3.2 states both inclusive; no action on either day, asserted |
| 10 | Rounding path | none in the call | stated; the asks round once |
| 11 | Tie-break | two operations on one interval | none: the nine intervals are distinct and pairwise non-dividing, asserted |
| 12 | Maturity and censoring | reports still arriving | the import log's own completion dates; the window closed a week before the extract, asserted |
| 13 | Order of operations | resolve feeds then flag, or flag then resolve | C1: the flag file is at location-day grain, so either order flags the same days, asserted |
| 14 | Row order | the minute file's order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the two feeds and the re-imported month | C1: a duplicate report carries the same report identifier and the same minute, so any resolution keeps one action, asserted |
| 16 | Identity normalisation | place names across the feeds and the gazetteer | the gazetteer's superseded names; asserted that every reported name resolves to one settlement |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | counts of events, of reports and of actions | the dictionary names each; the call reads actions only, asserted |
| 19 | Code and status semantics | the route codes and the flag codes | the dictionary; never the decisive step |
| 20 | Integerisation | the count is an integer by construction | stated |
| 21 | Clause scope | paragraph 2.2 per location per day | the paragraph states both; asserted |
| 22 | Forward window contents | the next period the institute will monitor | the call is a count for the closed period, with its reason: the bulletin reports the period that closed, and the trustees' vote is on the desk the count sizes |

## Literal reader

Executing the prompt, the protocol's paragraphs 2.2, 3.1, 3.2 and 4.3, the dictionary and the
gazetteer word for word selects the actions at the gazetteer's settlements between 1 May and 30
October 2026, one action per location per day, and asks how many distinct operations carried out at
least one of them, an operation being a series of actions by one coordinating group to one plan. The
text is silent on how one operation is told from another, so every option was computed: contiguous
runs of the flagged location-days give 23, runs without singletons 17, a spatiotemporal clustering 12,
and the distinct intervals the actions repeat on give 9, which the locations each operation alone
touches show unmixed. The easy ones are easy methods on the same literal estimand, not other readings
of it, and every other term and convention has an SF row ruled out by a quoted sentence or asserted
to give the same count.

## Oracles

- `coordination_flags.csv`, the institute's own suspicion flag at location-day grain, confirms which
  days its analysts thought something was coordinated. It groups nothing and counts nothing, and the
  answer holds with the file deleted, asserted.
- The earlier bulletins report actions recorded and locations touched by period and never operations,
  so they tie under every rung.
- `import_log.csv` confirms which month was loaded twice and when each load completed; it ties under
  every rung.
- The gazetteer confirms the settlements and their superseded names; it ties under every rung.
- No control, published figure or corpus states a count of operations, and no earlier count ships.
  There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per fortnight, the actions recorded, the locations touched and the share of actions the partner network reported | 3 per fortnight | the construction's own output on the segment the trustees want anyway | the bulletin's standing table | the construction layer: a wrong action unit, a doubled feed or the re-imported month fails every cell | D8 the repeated hour; D5 the partner network's late start | minute file, import log, gazetteer, routes, dictionary, protocol, manifest, partner tables; 12 columns | 4 stops, lazy delta 8 of 13 fortnights | the bulletin's own table |
| A2 per access route, the reports received, those the institute could not place, and the median minutes from event to report | 3 per route | the audit trail from an input the call consumes, through rows it never reads, to the route's own control total | the pipeline review the institute runs each period | D4 absence as the signal: the reports the institute could not place are held in a separate exceptions file no habitual join reaches | D6 the exceptions file is per report, the route totals per day; D8 the report clock is the publisher's, not the institute's | exceptions file, route totals, minute file, dictionary, manifest; 11 columns | 4 stops, lazy delta 2 of 3 routes | an ingest pipeline's own period review |
| A3 per partner organisation, the reports it filed, those filed after the period closed and the euros paid under its data agreement | 3 per partner | an input reconciled to another system's total, the gap made of devices | the finance office settles the data agreements | D2 version: one partner's agreement was amended mid-period and the rate paid is the amended one, which the superseded schedule does not carry | D3 a rate per report against a rate per month; D7 one partner filed under two organisation codes after a merger | partner tables in PDF, agreement schedule, amendment, route totals, manifest, dictionary; 13 columns | 5 stops, lazy delta 3 of 7 partners | the finance office's quarterly settlement |

**The main population's zero counts.** Zero device rows and zero hazard rows in the actions the count
rests on: the devices sit in the exceptions file, the agreement schedule and the partner tables, none
of which carries an event. Deleting every device leaves the count exactly as hard, asserted.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D8 the repeated hour | A1, A2 | A1 one fortnight, A2 one route's median |
| D6 grain | A2, A3 | A2 one route, A3 two partners |
| D5 the partner network's late start | A1, A3 | A1 the share in five fortnights, A3 one partner |

**The referee.** `extract_manifest.csv` states each file's rows and range and settles the one designed
disagreement, the exceptions file's extent, without naming a level.

**The cracker sheet.** The cracker counted nine operations, ran the hygiene battery, executed every
filed paragraph and matched every control.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 share the partner network reported, fortnight 7 | counts reports, not actions | too high | to be measured at build | miss |
| A2 reports the institute could not place, media monitor | the minute file alone, which holds only placed reports | 0 | to be measured at build | miss |
| A2 median minutes to report, partner network | the publisher's clock | too low | to be measured at build | miss |
| A3 euros paid, the amended partner | the superseded schedule's rate | too low | to be measured at build | miss |
| A3 reports filed, the merged partner | one organisation code | too low | to be measured at build | miss |

**Pair ceiling:** 39.5
**Mirror leakage:** 20.0

## Tried and rejected

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
