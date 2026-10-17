# task234 design note

Architecture 1 (drawn 2026-10-16), wave 2, seed DQ07 (which laboratory feeds get a volume-drop alert against the seasonal
baseline): the seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10 rules.
Epidemiology & Public Health, disease surveillance and outbreak anomaly detection, Data Quality Monitoring & Alerting. A
county health department's epidemiology unit receives electronic laboratory results for influenza, RSV and SARS-CoV-2
from ten laboratories; every Monday its surveillance data manager sets which result streams the laboratory liaison
escalates under the feed completeness protocol, judged on each stream's completeness for the week just closed: the
results received over the tests the laboratory's weekly aggregate report will count when it arrives on Wednesday.

## Draw

Card `cards/task234.json` (registered 2026-10-16). Guard verdict WARN, one line each: `repeat.gate_g` against task263
(decomposition_attribution, which splits emissions among sources measured only in mixtures) is accepted because the
mechanism, the domain and the object differ; `repeat.decision` against task233 (designation_set) is accepted because the
domain, the object (result streams, not published statistics) and the mechanism differ; `test.same_puzzle_older`
(task231, task445 v1 loop 0) is differentiated on the card.

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, serving Data Quality
  Monitoring & Alerting (the domain index lists this task type under AD and DQ).
- **Niche.** The county's surveillance platform takes each laboratory's result messages through an interface; each
  laboratory also files a weekly aggregate report of the tests it ran and the positives it found for each virus, due
  the Wednesday after the week. The feed completeness protocol has the liaison chase any stream whose results fall
  below 80 per cent of the tests the aggregate report counts. The check runs on Monday, before the reports arrive, so
  each stream's tests for the week have to be estimated.
- **The call.** For each of the 29 result streams (ten laboratories, three viruses each except the long-term-care
  laboratory's two), escalate or not for MMWR week 3 of 2027 (17 to 23 January). The laboratories serve different
  patients: a children's hospital, four adult hospitals (one with mostly older patients), three urgent-care networks,
  a laboratory testing the county's long-term-care homes and a reference laboratory taking specimens from the rural
  clinics in the county's north.
- **Shape.** 07, a grid of cells (laboratories by virus), each cell graded. Decision designation_set, answer
  set_of_items, question form which.
- **Strategy.** forecast_method_backtest with G12 decisive (a stream's missing results told apart from tests its
  laboratory never ran) and G6 supporting (each laboratory's patient mix sets its own epidemic clock); Gate G
  decomposition_attribution (a correctly reported change in a stream's volume assigned to its driver, the epidemic or a
  lost message); calibration parallel_run_overlap (the aggregate reports beside the result feed over the same weeks);
  context artifact filed_standard; layer 2 family forecast_uncertainty, pattern
  epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/3.
- **Forum, event, organisation.** operations_desk (the laboratory liaison acts on the list), season_or_peak (influenza
  is climbing: a stream losing results now blinds the county's indicators at the peak), local_government (a county
  health department).
- **People** (`guard.py names --geo "United States" --seed 234`): Michaela Mclean, surveillance data manager, who sets
  the escalations; Travis Humphrey, laboratory liaison; Kaitlyn Sanchez, respiratory epidemiologist, who keeps the
  protocol.
- **Deliverables.** `respiratory_feed_escalations_2027-W03.xlsx` (the grid, with each stream's estimated tests and
  completeness) and `respiratory_feed_completeness_2027-W03.png` (each stream's completeness against the 80 per cent
  line).
- **Data-native sentence.** Each laboratory's weekly respiratory test count rises and falls with the epidemic among its
  own patients, and in week 3 those epidemics are on different clocks: children's influenza and RSV and the city's
  holiday COVID wave are falling, adult influenza has just turned, the long-term-care homes' outbreaks are ending and
  the rural clinics' epidemics are still rising; a message lost between a laboratory and the county drops a positive result and a
  negative one alike, so each stream's own positivity, which no lost message moves, tells how many tests its laboratory
  ran, while the calendar, last week and the other laboratories each tell it wrong for some streams.

Sources, one line each (what it teaches; how this build differs):
- Client pattern disease-surveillance-outbreak-anomaly-detection/3 (testing volume changes the count: positivity or
  test-adjusted rates; shortcut: more confirmed cases means more infection): turned round here, positivity reads the
  epidemic that drives the testing volume, and a lost message moves neither the positivity nor the tests.
- Pattern /1 (the seasonal baseline: Farrington, Serfling) is this build's rung 2: the textbook baseline, wrong this
  winter because RSV and influenza run on other clocks than in any earlier season.
- Seed DQ07: the world, the decision and the quantity only; its decoy architecture is not used.
- Farrington et al. (1996) and Noufaily et al. (2013), the seasonal baseline; weekly aggregate reporting of tests and
  positives by virus as respiratory laboratory networks file it; completeness of electronic laboratory reporting judged
  against an independent count. No card or ledger row on file uses positivity.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomised unit), task229
  (a daily mean through a convex rating), task230 (net coding bias of a late channel), task231 (the closed share of
  silent units from rounds the register caught up with), task232 (transmission from delayed, mixed outcomes), task233
  (a missing-not-at-random departure on the odds scale). None reads a loss-invariant ratio to tell missing records from
  fewer events.
- task232 (same pairing, laboratory result feeds): prices lateness by childcare transmission; this build has no
  lateness and no transmission: each stream's completeness is judged against tests predicted from its positivity.

## Default path

1. Read the feed completeness protocol (FCP-2): a stream's completeness for a week is the tests resulted in that MMWR
   week whose results reached the platform by 08:00 on the Monday after it, over the tests the laboratory's weekly
   aggregate report counts for that virus and week; the liaison escalates every stream below 80 per cent; the week's
   escalations are set on the Monday, before the reports are due on the Wednesday.
2. Collapse the week-3 result messages to tests for each stream (one test per accession and virus, influenza A and B
   rows as one influenza test, a corrected result once, cancelled tests out, the week by the county's local result
   date, the merged hospital's two facility identifiers as one laboratory).
3. Take each stream's tests for week 3 from the latest aggregate report, week 2's.
4. Completeness is the week's results over those tests; escalate below 80 per cent.

Ends on: 15 streams escalated, 9 of the 29 cells wrong: the SARS-CoV-2 streams of Ellery, Corrigan Valley, Brandmoor,
the three urgent-care networks and Arbor Point and the children's hospital's influenza and RSV streams are escalated
though they are complete (their epidemics fell by a quarter to a half in the week; last week's count puts them at 55 to
74 per cent), beside the six streams of Wexmoor and Westmarch; every stream sits at least 0.042 from the line.

Golden: escalate the influenza, RSV and SARS-CoV-2 streams of Wexmoor Regional Medical Center and of Westmarch
Reference Laboratory, and no other stream.

## Stump sentence

A competent solver divides each stream's week-3 results by the tests in last week's aggregate report and files 9 of
the 29 cells wrong (Ends on: 15 streams escalated, nine of them complete streams whose epidemic fell in the week);
the step that lands it there is taking the week's tests from the past instead of from the stream's own positivity,
which moves with its patients' epidemic and not with a lost message.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting: the completeness of each laboratory's result stream judged against the tests it ran,
  the week's tests read from the epidemic the stream's own positivity shows.
- **Domain test:** the quantity that decides is each stream's tests for the week predicted from its own test
  positivity, the surveillance field's measure of epidemic activity that is independent of testing volume and that a
  lost message cannot move; a seasonal (Farrington-type) baseline, last week's count or the other laboratories' change
  in its place changes the escalations.
- **Swap:** with meters, tills or app events for laboratories there is no positivity and no epidemic among a source's
  own patients driving its count, so the decisive step has nothing to read; the task stands on the laboratories'
  testing and the viruses' epidemics, not on the word "feed".
- **Layer 1:** result messages at the target level from three laboratories (influenza A and B as separate rows) and at
  the test level from the others, corrected results resent under the same accession, cancelled orders, result times in
  UTC against MMWR weeks counted on the county's local date, a merged campus laboratory sending under a second facility
  identifier, and aggregate reports resubmitted after first filing, each as the laboratories' and the platform's systems
  produce them; nothing is placed to be caught, each mishandled leaves the call where it is (asserted, R2), and on the
  clean truth the default path and the golden are unchanged (asserted, R3a and R3b).
- **Layer 2:** forecast_uncertainty, pattern /3 turned round: each stream's tests for the week predicted on honest
  history from its own positivity, the one predictor this week's losses cannot touch, not from the calendar, last week
  or the other laboratories, each of which the season's history refutes for some streams.
- **Decisive step:** estimating each stream's tests for the week from its own positivity (the laboratory's testing
  response to its patients' epidemic, fitted on the weeks its aggregate reports already cover), because a message lost
  on the way drops a positive and a negative alike, so the received positivity is the laboratory's positivity even
  when a third of its results are missing.
- **Not semantics:** the default path reads every field, code and definition right (tests collapsed per accession and
  virus, the week by local result date, the protocol's ratio and line) and still files the wrong grid; the wrong cells
  come from where the week's tests are taken from, which no field, code or definition names.
- **Not rule application:** the protocol files the ratio, its denominator (the aggregate report's count), the week and
  the 80 per cent line; no filed sentence says how the week's tests are estimated before the report arrives, so
  executing every stated rule with last week's count or the seasonal baseline still files the wrong grid.
- **Analyst test:** a strong analyst who collapses the messages to tests correctly and reads the protocol takes each
  stream's tests from last week's aggregate report and files the default path's Ends on (9 of 29 cells wrong); the
  seasonal baseline of the same weeks in earlier winters files another wrong grid (9 wrong); `checks.py` runs both on the generator's clean truth and
  asserts them, then changes only where the week's tests come from and asserts the golden.
- **Estimand:** the feed completeness protocol (in the pack) fixes the population (every result stream the protocol
  lists), the outcome (results received by Monday 08:00 for tests resulted in the week), the denominator (the tests the
  laboratory's weekly aggregate report counts for that virus and week, still to arrive), the window (MMWR week 3 of 2027
  by local result date) and the line (80 per cent).
- **No decoy:** nothing is planted: no memo, draft, alert export or stakeholder figure states a completeness, a
  baseline or an escalation; the interface outages are the events the protocol exists to catch, recorded only as their
  effect on the messages; no rule is withheld and no block is copied.
- **No certified replay:** no certified or published figure exists for the method to reproduce; the aggregate reports
  are the laboratories' own counts of past weeks, and the testing response is read from how those counts move with
  positivity, not recovered by matching a stated number.
- **Lesson:** a drop in a stream's records is either records lost or events that never happened, and a ratio the loss
  cannot move (here the share of tests positive, which tracks the epidemic that drives testing) tells them apart when
  the true count is not yet in; the calendar, the last period and the peers each confuse an epidemic's turn with a
  failing feed. No build on file teaches a loss-invariant ratio as the reference for completeness.

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) last week's aggregate tests as the week's: 9 wrong | FCP-2 s.3 names the aggregate report as the denominator, so the latest one is the natural stand-in | the report sits beside the results by laboratory and virus | yes, carry the last observation | the season's own reports show weekly swings of a quarter | no | one division | readable |
| 1 last week's tests carried forward at last week's growth, or the recent mean: 8 and 10 wrong | none | the weekly series | yes, a trend nowcast | the reports show the growth turning in several streams | no | one ratio | readable |
| 2 the seasonal baseline (the same weeks of earlier winters, trend-adjusted, Farrington's construction): 9 wrong | none | the reports go back to 2022 | yes, the surveillance textbook | the season's reports show RSV, COVID and influenza off their usual weeks | no | a group-by | readable |
| 2 the other laboratories' change this week applied to each stream: 3 wrong | none | the other streams' results this week | yes, compare with peers | the reports show the laboratories' patients on different clocks | no | one ratio | readable |
| 2 the week's tests from its positives and last week's positivity: 4 wrong | none | the result values | yes, scale by positives | none, it fails only where results are lost | no | one division | readable |
| 3 (decisive) each stream's tests from its own positivity this week, through the laboratory's testing response fitted on its reports, because a lost message drops a positive and a negative alike | no sentence names positivity, a model or a predictor; FCP-2 files only the ratio and its denominator | no column holds an expected count; the reports hold tests and positives only | no: the reflexes carry the past, scale by peers or use positives | only the reports' own weeks, which show tests following positivity to a solver who asks what drives a laboratory's testing | no | not linear: the response is fitted per stream and read at the week's positivity | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "stream" | one laboratory's results for one of influenza, RSV, SARS-CoV-2, as the stream register lists them (29) | every laboratory and virus pair seen in the results | the register lists every pair that appears | C1 (asserted: the pairs in the results equal the register's 29) |
| SF2 | "test" | one accession and one virus; influenza A and B on one accession one influenza test | each result row | the three target-level laboratories' influenza streams double, same call | FCP-2 s.2; same call (asserted) |
| SF3 | a corrected result | replaces the result it corrects (one test) | counted again | counts rise by under 1 per cent, same call | FCP-2 s.2; same call (asserted) |
| SF4 | a cancelled test | not a test | counted | same call | FCP-2 s.2; same call (asserted) |
| SF5 | the week of a result | MMWR week of the local (America/Chicago) release date | the UTC date | counts move by under 15 per cent (week 2's Saturday evening joins week 3), same call | FCP-2 s.2; same call (asserted) |
| SF6 | "received by 08:00 on the Monday" | every week-3 result in the extract (cut at 08:00 on 25 January) | none | one extract | C1 (asserted: no week-3 row after the cutoff in either clock reading) |
| SF7 | the denominator | the tests the laboratory's week-3 aggregate report will count for that virus | last week's report | the default path | FCP-2 s.3 and s.4 (the report for the week, due on the Wednesday after it; the escalations set before it arrives) |
| SF8 | the aggregate report of record | the latest submission for the laboratory, virus and week | the first | same call | data dictionary; same call (asserted) |
| SF9 | "below 80 per cent" | strictly below | at or below | same call (no stream within 2 points of the line under any positivity model) | FCP-2 s.4; same call (asserted) |
| SF10 | a hospital sending under two facility identifiers | one laboratory (the register maps both) | two, or the second left unmapped | the second identifier carries under 2 per cent of the extract, same call | stream register; same call (asserted) |
| SF11 | an inconclusive result | a test, neither positive nor negative | dropped | same call | FCP-2 s.2; same call (asserted) |
| SF12 | population of the week's tests | every test the laboratory resulted in the week, whatever the patient's residence | county residents only | the aggregate reports count every test | FCP-2 s.3 (the report's count); data dictionary |

## Ladder

Four rungs, each a defensible estimate of the week's tests, each dying to one shipped fact (counts in tests; the line at
80 per cent; figures measured on the shipped pack, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | last week's aggregate tests | 15 escalated, 9 wrong (nine complete streams escalated); nearest stream 0.042 from the line | the season's reports: where a stream's positivity moved 3 points or more, last week's count misses the week by 15.5 per cent at the median |
| 1 | last week's tests at last week's growth; the mean of the last three weeks | 14 escalated, 8 wrong (seven healthy influenza streams just past their turn, Arbor Point's SARS-CoV-2); 14 escalated, 10 wrong | the reports: last week's growth reversed in those streams; the holiday weeks pull the mean down |
| 2 | the seasonal baseline; the peers' change (pooled or median); positives over last week's positivity | 13 escalated, 9 wrong (the SARS-CoV-2 streams of seven laboratories and the children's RSV escalated, Wexmoor's influenza missed); 5 escalated, 3 wrong (the children's influenza escalated, Westmarch's influenza and SARS-CoV-2 missed), median 7 escalated, 3 wrong; 2 escalated, 4 wrong (Wexmoor's three streams and Westmarch's SARS-CoV-2 missed) | the reports: this winter's influenza peaks later and higher than any earlier one; the laboratories' patients are on different clocks; positives are lost with the rest |
| 3 (golden) | each stream's tests predicted from its own positivity through its testing response | 6 escalated, the golden; nearest stream 0.073 from the line (Bluestem's RSV at 87 per cent) | |

- **Margins.** Every positivity model in the asserted family (log-linear, log-linear with trend, Poisson, quadratic in
  the log, anchored on last week's report, with last week's tests as a covariate, linear and linear with trend; on the
  current season, the last sixty weeks or every report; holiday weeks in or out) escalates exactly the golden six, the
  nearest stream at least 0.069 from the line under the log models (0.099 log-linear, 0.069 with trend, 0.074 Poisson,
  0.076 quadratic, 0.077 anchored, 0.099 lagged) and 0.031 under the linear ones; no fit on 13 weeks of reports or more,
  in any of those forms, changes a stream (asserted). On the truth (the tests the week-3 reports will count) the six are
  52 to 58 per cent complete and every other stream 93.5 per cent or more.
- **Position and dominance.** Every reflex lands on its own wrong grid; only the decisive construction reaches the
  golden; the default path's nine wrong cells are all 0.04 or more from the line.
- **Grid.** The default moves 9 of 29 cells, the rungs 3 to 10.
- **Worth.** Worth is counted on the cells, never on an intermediate.

## Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | the 29 streams of the stream register | FCP-2 s.1; C1 (SF1) |
| 2 | Unit of account | the test (accession and virus) | FCP-2 s.2 (SF2) |
| 3 | Attribution window | MMWR week 3 of 2027 (17 to 23 January) by local release date | FCP-2 s.2 (SF5) |
| 4 | As-of dating | the platform extract of 08:00 on Monday 25 January 2027 | dictionary and README; C1 (SF6) |
| 5 | Version basis | the latest aggregate submission for each laboratory, virus and week | dictionary (SF8) |
| 6 | Denominator | the tests the week-3 aggregate report will count | FCP-2 s.3 (SF7) |
| 7 | Weighting | none: a ratio of counts per stream | FCP-2 s.3 |
| 8 | Window length | one MMWR week | FCP-2 s.3 |
| 9 | Boundary inclusivity | escalate below 80 per cent, 80 itself not escalated | FCP-2 s.4 (SF9) |
| 10 | Rounding path | completeness unrounded against the line; shown to one decimal | FCP-2 s.4 |
| 11 | Tie-break | none: each stream on its own | FCP-2 s.4 |
| 12 | Maturity and censoring | week-3 reports not yet filed; the tests are estimated | FCP-2 s.4 (set on the Monday) |
| 13 | Order of operations | collapse to tests, count by stream, divide, compare | FCP-2 s.2 to s.4 |
| 14 | Row order | irrelevant to counts | C1 |
| 15 | Duplicate resolution | a corrected result once; influenza A and B one test | FCP-2 s.2 (SF2, SF3) |
| 16 | Identity normalisation | the merged hospital's two facility identifiers to one laboratory | stream register (SF10) |
| 17 | Netting against gross | none | FCP-2 s.3 |
| 18 | Dimensional units | counts; completeness in per cent | FCP-2 s.3 |
| 19 | Code and status semantics | test codes to viruses by the test code list; status F, C, X | test code list; FCP-2 s.2 |
| 20 | Integerisation | none | counts are integers |
| 21 | Clause scope | FCP-2 applies to the register's streams from 1 October 2026 | FCP-2 s.1 |
| 22 | Forward window contents | the week-3 tests the aggregate reports will count on the Wednesday | FCP-2 s.3 and s.4 |

## Literal reader

Executed word for word, FCP-2 and the prompt fix the streams (the register's 29), the test (accession and virus, with
the collapse rules), the week (MMWR week 3 by local release date), the numerator (the extract's results), the
denominator (the tests the week-3 aggregate report will count), the line and the time of the call (the Monday, before
the reports). No sentence fixes how the week's tests are estimated before the reports arrive; the reports do. They run
from October 2022, and in every stream the weekly tests follow the stream's own positivity (the laboratory tests more
patients as the share testing positive rises). Back-tested one week ahead over the 5,046 closed stream-weeks since
March 2023, a fit of each stream's log tests on its positivity misses by 15 per cent or more once, last week's count 177
times and last week's growth 271 times; in the 210 stream-weeks where positivity moved by 3 points or more, the fit misses
by 2.6 per cent at the median, last week's count by 15.5 and last week's growth by 4.5 (asserted). A lost message drops
a positive and a negative alike, so the week's received positivity is the laboratory's. Every model of the response
that fits the reports gives the golden six; the default path reads every term the same way and differs only in where
the week's tests come from.

## Oracles

- The aggregate reports from October 2022: the bench the decisive construction is fitted and checked on; they tie
  every route's past weeks equally (they hold no week-3 count) and show the positivity relation only to a solver who
  asks what drives a laboratory's testing.
- The state's regional positivity table, the county's syndromic ILI series and the county's respiratory admissions
  (distractors, named in `metadata.json`): none counts a laboratory's tests or flags a stream; the state table and the
  admissions end at week 2, and the ILI series covers the county's emergency departments, not the rural clinics or a
  laboratory's own patients.
- No shipped artifact estimates, flags or ranks a stream.

## Ask sheet

Two asks, 39 figures, decoupled from the call: the call reads the week-3 results' laboratory, virus, accession, status,
result value and release time and the aggregate reports' tests and positives; the asks read the week-2 results'
receipt times and the week-3 results' patient and collection time, columns and rows the call never reads.

**Main population (zero device rows, asserted):** the week-3 results' counted columns and the aggregate reports. The
week-2 receipt-time convention and the week-3 patient and collection-time fields move no escalation (asserted:
every escalation unchanged when every receipt time is shifted by any amount, and when patient and collection fields are
scrambled).

| Ask | Figures | H18 home | Use | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: each stream's completeness for week 2, now that the week-2 aggregate reports are in | 29 | a reconciliation of the feed against the laboratories' own counts for the last closed week | the liaison's note to each laboratory quotes last week's completeness beside this week's call | D8, a clock against a filed cutoff: until the state hub's broker migration on Tuesday 19 January the platform wrote receipt times in local time; the dictionary names the hub's broker as the stamp's writer and states no zone, while the extract's other times are UTC; every laboratory's interface holds the results it releases from Saturday evening and sends them on Monday morning, so the week-2 batch sent on Monday 18 January (after the 08:00 cutoff) reads as arriving before it | the influenza A and B rows; corrected and cancelled results; the merged hospital's two identifiers; UTC release times against the local week | results (facility, accession, test code, target, status, released, received), aggregate reports (tests by laboratory, virus and week), stream register (facility to laboratory), test code list, FCP-2 (s.2, s.3, s.5), platform change log (the migration), dictionary: 7 files, 12 columns | every receipt time read as UTC (every stream high: 99.1 to 99.7 against the answer's 93.8 to 98.0); only rows received before their release shifted (every stream 0.4 points or more high); every pre-migration row shifted and week-3 rows too (the answer for week 2, harmless to week 3); rows with a negative lag dropped (every stream 5 points or more low); the answer, every figure at least 0.012 points from a rounding edge |
| B: the specimens each laboratory tested in week 3 that have results on the platform | 10 | a measure every laboratory carries that the call does not turn on | the liaison opens each call with the laboratory's specimen volume | D7, the true key elsewhere: most laboratories issue an accession per test ordered, so one swab tested for influenza, RSV and SARS-CoV-2 carries up to three accessions, and the panel laboratories add tests to a swab under new accessions; a specimen is one collection from one patient (FCP-2 s.6) | patients swabbed twice in the week; the influenza A and B rows | results (facility, accession, patient number, collected, target), stream register, FCP-2 s.6, dictionary: 4 files, 5 columns | distinct accessions (every laboratory high: 2,976 to 12,863 against the answer's 2,835 to 9,204); distinct patients (every laboratory low: 2,715 to 8,792, repeat swabs); the answer, distinct patient and collection time (patient and collection date counts the same, a patient's collections a day or more apart, asserted) |

- **Span:** nine files and 17 column uses across the asks; no shared primary or path (A reads receipt and release
  times of week 2, B patient and collection fields of week 3).
- **Shared hazards:** the influenza A and B rows move both counts if mishandled.
- **Realism:** a broker writing naive local timestamps until a migration, laboratories releasing a weekend queue on
  Monday morning, and laboratories numbering accessions per test ordered are records the systems make with no task in
  mind.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A completeness, every stream (29) | reads every receipt time as UTC like the extract's other times; the Monday batch counts as received before the cutoff | misses the same way | miss |
| B specimens, every laboratory (10) | counts distinct accessions, the protocol's key for a test | misses the same way | miss |

- **Cracker keeps:** under 0.05 of the ask weight (no figure is free of a device).
- Mirror leakage: 5 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the call's
  construction).
- Pair ceiling: 31.6 (C = 38 + 7 + 55 x 0.05 = 47.8; S = 5 + 7 + 55 x 0.05 = 14.8; mean 31.3, 31.6 with the chart's
  criteria split).

## Pre-ship check

1. Domain: the call stands on each stream's week-3 tests predicted from its own test positivity, the surveillance
   field's measure of activity that a lost message cannot move, through the laboratory's testing response fitted on
   its aggregate reports; with last week's count in its place 9 cells change, with the seasonal baseline 9, with the
   other laboratories' change 3. With meters or tills for laboratories there is no positivity to read.
2. Two layers: Layer 1 (influenza A and B rows at three laboratories, corrected results, cancelled orders, UTC release
   times against county weeks, the merged campus's second identifier, resubmitted reports) is neutral on the call,
   each item asserted (R2); Layer 2 is the positivity-driven estimate of the week's tests, asserted alone to move the
   default path to the golden (R3b).
3. No banned stump decides: nothing is planted (the interface losses are recorded only as their effect on the
   messages; no memo, alert or draft); not semantics (the default path reads every field and code right and files 9
   wrong cells, asserted on the clean truth, R3a); not rule application (FCP-2 files the ratio, its denominator and
   the line and names no method for the week's tests, asserted on the protocol's text).
4. Gate G: no shipped artifact estimates, flags or ranks a stream; the three distractors count no laboratory's tests.
5. Determinism: every asserted positivity model escalates the golden six (nearest stream 0.069 from the line under
   the log models, 0.031 under the linear ones) and no fit on 13 weeks of reports or more changes a stream; on the
   truth the six sit at 52 to 58 per cent and every other stream at 93.5 or more; the bench separates the routes;
   every week-2 figure sits at least 0.012 points from a rounding edge; specimen counts are integers.
6. Asks: A (29 figures) is moved in every figure by the receipt clock (the UTC reading gives 99.1 to 99.7 against
   93.8 to 98.0), B (10) in every figure by the accession key; the call reads neither column (asserted by shifting
   every receipt time and by scrambling patients and collection times).
7. Input gates: 11 files in four formats, the result extract at 217,357 rows, three distractors named in
   metadata.json; two builds byte-identical; figures_check 98 of 98.

## Leak check

leak.py REVIEW, no LEAK (--asof 2027-01-25; the code list renamed from a name the scan reads as authoring vocabulary).
Reader pass 1: Q1 the protocol's timing sentence (s.4, the escalations set before the reports are due), which fixes
when the call is made and names no method; Q2 to Q4 none; Q5 FCP-2 s.3, executing to the week-2 figures and leaving
week 3's denominator to be estimated; Q6 an analytical choice; the four REVIEW lines harmless. Its realism notes: the
receipt-before-release rows are the pre-migration county clock (the week-2 device); the register's sheet names were
the reader's printout of the sheet state; the sparse change log and the register's identical start dates were fixed in
the generator (a fuller log, each stream's test codes). Reader pass 2, on the rebuilt pack after the judge's round-1
fix: Q1 none (s.3 and s.4 the nearest, naming no denominator for week 3), Q2 and Q4 none, Q3 the dictionary, readme and
code list, Q5 the same, Q6 an analytical choice; the three REVIEW lines harmless; realism notes mild (the migration
entries, the six-hour receipt inversion before the migration, both the week-2 device's evidence).

## Tried and rejected

- One stream per laboratory, every virus pooled (prototype 2026-10-16): the pooled positivity mixes the children's
  hospital's RSV and influenza clocks, and the county's indicators and the aggregate reports are per virus; rejected for
  the laboratory-by-virus grid.
- Week-3 completeness rounded to one decimal place under the prompt's closing sentence (draft prompt, 2026-10-17): the
  figures are model estimates that move by a point between fits of the response; the rounding sentence now names the
  week-2 completeness only, and the workbook and chart give week-3 completeness in whole per cent.
- Linear response models fitted without the holiday weeks came within 0.01 of the line on the children's hospital's
  influenza stream (an exponential response over a fivefold range of tests; build 2026-10-17): the simulator was retuned
  (adult influenza peaking a week later, the rural epidemics still rising, losses of 0.45 and 0.40, RSV volumes up by a
  sixth) and the seeds searched until every asserted model clears 0.03.
- The golden fit with the holiday weeks in: the weeks of Christmas and New Year fall on the influenza peaks and flatten
  the response, so healthy influenza streams read up to 111 per cent; the golden leaves the weeks of Thanksgiving,
  Christmas Day and New Year's Day out.
- Corrections that flipped a true result (first message right, correction wrong) pushed the received positives 2 to 3
  per cent above the reports' count; a correction now carries the true result and the first message the wrong one.
- Wexmoor and Westmarch reporting influenza A and B as separate rows made counting rows as tests move the call (an R2
  failure); both now report one influenza result per test, and the three target-level laboratories are healthy.
- Corrigan Valley's merged campus sending a third of its results made an unmapped second identifier escalate the
  hospital (an R2 failure); the campus sends one result in twelve.
- Accession numbers drawn at random per laboratory and week collided between weeks 2 and 3 and merged tests across the
  weeks (Arbor Point's SARS-CoV-2 read 88 per cent complete on the truth): each laboratory now numbers in one sequence,
  each week's orders in their own run, in collection order, and `checks.py` asserts no accession spans two weeks and the
  extract collapses to the truth exactly.
- A week-3 seed giving two urgent-care networks the same specimen count: the seed was dropped.
- The dictionary calling the receipt time UTC for the whole column (judge round 1, FIX_NOW): read literally it gives
  every stream's week-2 completeness at 99.1 to 99.7, against the county-time receipts of the rows before the hub's
  broker migration; the row now names the broker as the stamp's writer and states no zone, so the records alone
  carry the clock (receipts that would precede their results' release by about six hours, a gap at the migration).
- A patient's two collections on one day (judge round 1, minor): patient and collection date counted two specimens
  as one; a patient's collections in the week now fall a day or more apart, so the date and time keys converge
  (asserted in county time and in UTC).
