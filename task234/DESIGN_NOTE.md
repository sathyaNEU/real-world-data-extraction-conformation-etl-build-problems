# task234 design note

Architecture 2 (re-rooted 2026-10-17 after the determinism judge's round-2 SEND_BACK of architecture 1, which left the
estimator of the week's tests to the data), wave 2, seed DQ07 (which laboratory feeds get a volume-drop alert against
the seasonal baseline): the seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10
rules. Architecture 2 keeps the world and the decisive step and files the protocol's week-by-week check, which the
judge found missing.
Epidemiology & Public Health, disease surveillance and outbreak anomaly detection, Data Quality Monitoring & Alerting. A
county health department's epidemiology unit receives electronic laboratory results for influenza, RSV and SARS-CoV-2
from ten laboratories; every Monday its surveillance data manager sets which result streams the laboratory liaison
escalates under the feed completeness protocol, judged on each stream's completeness for the week just closed: the
results received over the tests the laboratory's weekly aggregate report will count when it arrives on Wednesday.

## Draw

Card `cards/task234.json` (architecture 2, registered 2026-10-17; architecture 1 in its lineage). Guard verdict WARN,
one line: `repeat.question_form` against task193 and task194 (which) is the decision's own form, a set of streams.
`test.own_lineage` is cleared by the card's differentiation line (architecture 1 left the estimator open; architecture 2
files the check and gives week 2 an interface outage, the decisive step unchanged and unfiled); `test.same_puzzle_older`
(task231, task445 v1 loop 0) stays differentiated. Furniture redrawn against the builds filed since architecture 1:
calibration prior_period_close_out (task195 took parallel_run_overlap), forum other (task193 took operations_desk),
forcing event period_close (task195 took season_or_peak), strategy decomposition_attribution (task464 took
forecast_method_backtest).

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
- **Strategy.** decomposition_attribution with G12 decisive (a stream's missing results told apart from tests its
  laboratory never ran) and G6 supporting (each laboratory's patient mix sets its own epidemic clock); Gate G
  decomposition_attribution (a correctly reported change in a stream's volume assigned to its driver, the epidemic or a
  lost message); calibration prior_period_close_out (FCP-2 s.5's check: the estimates that could have been made for
  week 2 at its Monday cutoff set beside the week-2 reports that have since closed it); context artifact filed_standard;
  layer 2 family forecast_uncertainty, pattern epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/3.
- **The check (architecture 2).** FCP-2 s.5 files how the way of estimating a week's tests is chosen, in general terms:
  set beside the last closed week's reports, the way whose largest miss across the streams was smallest. Week 2 was a
  week in which Brandmoor's interface lost every result it released from Tuesday morning to Friday morning (about half
  its week) and never resent them; the platform held half of Brandmoor's week at the 18 January cutoff and holds no more
  now. No sentence names a way, a predictor or what the week's results contribute.
- **Forum, event, organisation.** other (the surveillance data manager sets the list for the laboratory liaison; no
  committee), period_close (the close of MMWR week 3 forces the Monday call), local_government (a county health
  department).
- **People** (`guard.py names --geo "United States" --seed 234`): Michaela Mclean, surveillance data manager, who sets
  the escalations; Travis Humphrey, laboratory liaison; Kaitlyn Sanchez, respiratory epidemiologist, who keeps the
  protocol.
- **Deliverables.** `respiratory_feed_escalations_2027-W03.xlsx` (the grid, with each stream's estimated tests and
  completeness) and `respiratory_feed_completeness_2027-W03.svg` (each stream's completeness against the 80 per cent
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

## Survivor anatomy

Actor: which streams lost results in transit rather than saw their epidemic fall has no column; it is a relation between each stream's received week of results, its received positivity, and its own testing response to positivity fitted on the weeks its aggregate reports already cover, which nothing stores.
Link: the week's received results, collapsed to tests, are set against the stream's fitted relation of tests to positivity from its reports, a comparison across the feed and the reports that no key offers and no sentence invites (FCP-2 s.5 files a check, never a predictor).
Reflex: the field's own completeness baselines, last week's count or a seasonal (Farrington-type) baseline, run through the protocol's week-2 check, sit at rungs 0 and 1 and escalate fifteen streams, nine of them complete (`Ends on:`), not the golden six.
Back-test: the protocol's own week-2 check certifies last week's count as the way that missed least among the textbook baselines, so the easy route passes the filed validation against every alternative it is shown.
Second use: every file the step reads is in the pack for the protocol's routine: the extract for every completeness, the aggregate reports as the denominator of record, the register for the streams and the codes for the viruses; both asks read the same extract and reports.
Shock: the two laboratories' losses and the complete streams' falls read as ordinary week-to-week movement in a winter season, their received counts dropping by similar shares, so no shipped statistic sorts the six lossy streams to the top.
Pins: FCP-2 files the ratio, the denominator (the report of record), the week by county date, the 80 per cent line and the check that chooses the way of estimating the week's tests (s.5); no sentence names a predictor, positivity, or that a lost message drops a positive and a negative alike.

## Default path

1. Read the feed completeness protocol (FCP-2): a stream's completeness for a week is the tests resulted in that MMWR
   week whose results reached the platform by 08:00 on the Monday after it, over the tests the laboratory's weekly
   aggregate report counts for that virus and week; the liaison escalates every stream below 80 per cent; the week's
   escalations are set on the Monday, before the reports are due on the Wednesday.
2. Collapse the week-3 result messages to tests for each stream (one test per accession and virus, influenza A and B
   rows as one influenza test, a corrected result once, cancelled tests out, the week by the county's local result
   date, the merged hospital's two facility identifiers as one laboratory).
3. Run FCP-2 s.5's check over the ways a forecaster reaches for first, each from the stream's own reports (last
   week's count, last week's growth, the mean of the last three weeks, the seasonal baseline of earlier winters): set
   beside the week-2 reports, last week's count missed some stream by 54.0 per cent at most, the seasonal baseline by
   56.7, the mean by 80.4 and the growth by 111.7, so keep last week's count.
4. Take each stream's tests for week 3 from the latest aggregate report, week 2's.
5. Completeness is the week's results over those tests; escalate below 80 per cent.

Ends on: 15 streams escalated, 9 of the 29 cells wrong: the SARS-CoV-2 streams of Ellery, Corrigan Valley, Brandmoor,
the three urgent-care networks and Arbor Point and the children's hospital's influenza and RSV streams are escalated
though they are complete (their epidemics fell by a quarter to a half in the week; last week's count puts them at 55 to
74 per cent), beside the six streams of Wexmoor and Westmarch; every stream sits at least 0.042 from the line.

Golden: escalate the influenza, RSV and SARS-CoV-2 streams of Wexmoor Regional Medical Center and of Westmarch
Reference Laboratory, and no other stream.

## Stump sentence

A competent solver runs the protocol's week-2 check over the textbook baselines, keeps last week's aggregate report as
the way that missed least, divides each stream's week-3 results by it and files 9 of the 29 cells wrong (Ends on: 15
streams escalated, nine of them complete streams whose epidemic fell in the week); the step that lands it there is
taking the week's tests from the past instead of from the stream's own positivity, which moves with its patients'
epidemic and not with a lost message.

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
- **Not rule application:** the protocol files the ratio, its denominator (the aggregate report's count), the week, the
  80 per cent line and the check that chooses the way of estimating the week's tests (s.5); it names no way and no
  predictor, so executing every stated rule over the ways a forecaster reaches for first keeps last week's count (or,
  with the other laboratories' change among them, that) and still files a wrong grid; only the analyst's own choice
  of what in the week's results can estimate its tests reaches the golden.
- **Analyst test:** a strong analyst who collapses the messages to tests correctly, reads the protocol and runs its
  week-2 check over the textbook baselines keeps last week's aggregate report and files the default path's Ends on (9
  of 29 cells wrong); with the other laboratories' change among the ways the check keeps that and files 3 cells wrong;
  `checks.py` runs both on the generator's clean truth and asserts them, then changes only where the week's tests come
  from and asserts the golden.
- **Estimand:** the feed completeness protocol (in the pack) fixes the population (every result stream the protocol
  lists), the outcome (results received by Monday 08:00 for tests resulted in the week), the denominator (the tests the
  laboratory's weekly aggregate report counts for that virus and week, still to arrive, estimated in the way s.5's
  check keeps), the window (MMWR week 3 of 2027 by local result date) and the line (80 per cent).
- **No decoy:** nothing is planted: no memo, draft, alert export or stakeholder figure states a completeness, a
  baseline, an estimate or an escalation; the interface outages (Brandmoor's in week 2, Wexmoor's and Westmarch's in
  week 3) are the events the protocol exists to catch, recorded only as their effect on the messages; no rule is
  withheld and no block is copied.
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
| 0 (default) last week's aggregate tests as the week's, the way the s.5 check keeps among the textbook baselines (largest week-2 miss 54.0 per cent): 9 wrong | FCP-2 s.3 names the aggregate report as the denominator and s.5's check, run over the baselines, keeps the latest one | the report sits beside the results by laboratory and virus | yes, carry the last observation | the week-2 check: it misses some stream by 54.0 per cent | no | one division | readable |
| 1 last week's tests at last week's growth, or the recent mean: 8 and 10 wrong | none | the weekly series | yes, a trend nowcast | the week-2 check: 111.7 and 80.4 per cent | no | one ratio | readable |
| 2 the seasonal baseline (the same weeks of earlier winters, trend-adjusted, Farrington's construction): 9 wrong | none | the reports go back to 2022 | yes, the surveillance textbook | the week-2 check: 56.7 per cent | no | a group-by | readable |
| 2 the other laboratories' change this week applied to each stream: 3 wrong | none | the other streams' results this week | yes, compare with peers | the week-2 check: 44.5 per cent (Brandmoor's lost half pulls its peers' change) | no | one ratio | readable |
| 2 the week's results taken as its tests, or its positives over last week's positivity: none escalated; 4 wrong | none | the result values | yes, the feed as its own count; scale by positives | the week-2 check: 52.6 and 63.1 per cent (Brandmoor's lost half) | no | one division | readable |
| 3 (decisive) each stream's tests from its own positivity this week, through the laboratory's testing response fitted on its reports, because a lost message drops a positive and a negative alike | s.5 asks for the way that missed week 2 least and names none; no sentence names positivity, a model or a predictor | no column holds an expected count; the reports hold tests and positives only | no: the reflexes carry the past, scale by peers, use the feed's own count or its positives | the week-2 check scores it (largest miss 7.8 per cent) only for a solver who brings it; the check names no candidate | no | not linear: the response is fitted per stream and read at the week's positivity | silent |

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
| SF8 | the aggregate report of record | the latest submission for the laboratory, virus and week | the first | same call | FCP-2 s.3 (the latest submission is the report of record); same call (asserted) |
| SF9 | "below 80 per cent" | strictly below | at or below | same call (no stream within 2 points of the line under any positivity model) | FCP-2 s.4; same call (asserted) |
| SF10 | a hospital sending under two facility identifiers | one laboratory (the register maps both) | two, or the second left unmapped | the second identifier carries under 2 per cent of the extract, same call | stream register; same call (asserted) |
| SF11 | an inconclusive result | a test, neither positive nor negative | dropped | same call | FCP-2 s.2; same call (asserted) |
| SF12 | population of the week's tests | every test the laboratory resulted in the week, whatever the patient's residence | county residents only | the aggregate reports count every test | FCP-2 s.3 (the report's count) |
| SF13 | the check's "largest miss across the streams" | each way's largest miss over the 29 streams, as a share of the week's reported tests | the average miss | same call: the Poisson fit on positivity misses by 3.2 per cent on average, every other way by 9.0 or more (asserted) | FCP-2 s.5; same call (asserted) |
| SF14 | estimates "that could have been made at that Monday's cutoff" | from the reports to week 1 and the week-2 results the platform held at 08:00 on 18 January | every week-2 result in the extract | same call: Brandmoor's lost half was never resent, so the week's received results still miss by 49.5 per cent and the positivity fit by 7.6 (asserted) | FCP-2 s.5; same call (asserted) |
| SF15 | the receipt clock for what the platform held at the cutoff | county time before the broker migration | UTC throughout (the weekend batch counted as held) | same call: the positivity fit misses by 7.6 per cent at most, every other way by 49.5 or more (asserted) | same call (asserted) |

## Ladder

Four rungs, each a defensible way of estimating the week's tests, each dying to one shipped fact, the s.5 check on week
2 first among them (counts in tests; the line at 80 per cent; figures measured on the shipped pack, asserted in
`checks.py`; week-2 largest misses at the 18 January cutoff).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | last week's aggregate tests, the way the check keeps among the textbook baselines (largest miss 54.0 per cent, the seasonal baseline 56.7) | 15 escalated, 9 wrong (nine complete streams escalated); nearest stream 0.042 from the line | the check: a way built on the positivity misses week 2 by 7.8 per cent at most |
| 1 | last week's tests at last week's growth; the mean of the last three weeks | 14 escalated, 8 wrong (seven healthy influenza streams just past their turn, Arbor Point's SARS-CoV-2); 14 escalated, 10 wrong | the check: 111.7 and 80.4 per cent |
| 2 | the seasonal baseline; the other laboratories' change (pooled or median); the week's received results taken as its tests; positives over last week's positivity | 13 escalated, 9 wrong; 5 escalated, 3 wrong (the children's influenza escalated, Westmarch's influenza and SARS-CoV-2 missed), median 7 escalated, 3 wrong; none escalated, 6 wrong; 2 escalated, 4 wrong | the check: 56.7; 44.5 and 49.1; 52.6; 63.1 per cent (Brandmoor's lost half in week 2 moves every count-based way) |
| 3 (golden) | each stream's tests predicted from its own positivity through its testing response (a Poisson fit on positivity and a linear trend over every report of record, holiday weeks out) | 6 escalated, the golden; nearest stream 0.074 from the line (Bluestem's RSV at 87.4 per cent) | |

- **Margins.** Every positivity model in the asserted family (log-linear, log-linear with trend, Poisson, quadratic in
  the log, anchored on last week's report, with last week's tests as a covariate, linear and linear with trend; on the
  current season, the last sixty weeks or every report; holiday weeks in or out) escalates exactly the golden six, the
  nearest stream at least 0.069 from the line under the log models and 0.031 under the linear ones; no fit on 13 weeks
  of reports or more, in any of those forms, changes a stream (asserted). On the truth (the tests the week-3 reports
  will count) the six are 52 to 58 per cent complete and every other stream 93.5 per cent or more.
- **The check.** Of the ways tried, the golden's Poisson fit has the smallest largest week-2 miss (7.8 per cent); every
  other positivity fit that clears 30 per cent gives the golden six; every way not built on the positivity misses by
  44.5 per cent or more, under either receipt clock and with every week-2 result in the extract (asserted).
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
| 4 | As-of dating | the platform extract of Monday 25 January 2027 | the extract's own date; C1 (SF6: no week-3 row after 08:00 in either clock reading) |
| 5 | Version basis | the latest aggregate submission for each laboratory, virus and week | FCP-2 s.3 (SF8) |
| 6 | Denominator | the tests the week-3 aggregate report will count | FCP-2 s.3 (SF7) |
| 7 | Weighting | none: a ratio of counts per stream | FCP-2 s.3 |
| 8 | Window length | one MMWR week | FCP-2 s.3 |
| 9 | Boundary inclusivity | escalate below 80 per cent, 80 itself not escalated | FCP-2 s.4 (SF9) |
| 10 | Rounding path | completeness unrounded against the line; shown to one decimal | FCP-2 s.4 |
| 11 | Tie-break | none: each stream on its own | FCP-2 s.4 |
| 12 | Maturity and censoring | week-3 reports not yet filed; the tests are estimated in the way FCP-2 s.5's check keeps | FCP-2 s.4 and s.5; C2 (the check on week 2 keeps a positivity way: 7.8 per cent against 44.5 or more) |
| 13 | Order of operations | collapse to tests, count by stream, divide, compare | FCP-2 s.2 to s.4 |
| 14 | Row order | irrelevant to counts | C1 |
| 15 | Duplicate resolution | a corrected result once; influenza A and B one test | FCP-2 s.2 (SF2, SF3) |
| 16 | Identity normalisation | the merged hospital's two facility identifiers to one laboratory | stream register (SF10) |
| 17 | Netting against gross | none | FCP-2 s.3 |
| 18 | Dimensional units | counts; completeness in per cent | FCP-2 s.3 |
| 19 | Code and status semantics | test codes to viruses by the test code list; status F, C, X | test code list; FCP-2 s.2 |
| 20 | Integerisation | none | counts are integers |
| 21 | Clause scope | FCP-2 applies to the register's streams from 1 October 2026 | FCP-2 s.1 |
| 22 | Forward window contents | the week-3 tests the aggregate reports will count on the Wednesday | FCP-2 s.3 to s.5 (SF13 to SF15) |

## Literal reader

Executed word for word, FCP-2 and the prompt fix the streams (the register's 29), the test (accession and virus, with
the collapse rules), the week (MMWR week 3 by local release date), the numerator (the extract's results), the
denominator (the tests the week-3 aggregate report will count), the line, the time of the call (the Monday, before
the reports) and the way of estimating the week's tests: the way whose largest miss across the streams was smallest
when the estimates that could have been made at week 2's cutoff were set beside week 2's reports (s.5). Executed, the
check scores every way a reader brings: last week's report misses some stream by 54.0 per cent, the seasonal baseline
by 56.7, the recent mean by 80.4, last week's growth by 111.7, the other laboratories' change by 44.5, the week's
received results by 52.6 and positives over last week's positivity by 63.1 (Brandmoor's interface lost half its week
and the platform held only the rest), while each stream's tests read from its own positivity through the testing
response fitted on its reports miss by 7.8 per cent at most. No sentence names that way; the check keeps it once a
reader brings it, and every positivity way the check could keep escalates the golden six. Over the 5,046 closed
stream-weeks since March 2023 the same fit misses by 15 per cent or more once, last week's count 177 times (asserted).
A lost message drops a positive and a negative alike, so the week's received positivity is the laboratory's.

## Oracles

- FCP-2 s.5's check on week 2 (the week-2 reports beside the week-2 results the platform held at the cutoff): a filed
  selection criterion (C2), not an oracle; it scores only the ways a reader brings and names none, and it keeps the
  golden's way only for a reader who brings the stream's own positivity.
- The aggregate reports from October 2022: the history the testing response is fitted on; they hold no week-3 count.
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
| A: each stream's completeness for week 2, now that the week-2 aggregate reports are in | 29 | a reconciliation of the feed against the laboratories' own counts for the last closed week | the liaison's note to each laboratory quotes last week's completeness beside this week's call | D8, a clock against a filed cutoff: until the state hub's broker migration on Tuesday 19 January the platform wrote receipt times in local time; the receipt column carries the broker's stamp with no zone in its name, while the extract's other two times are named _utc, and before the migration receipts precede their releases by about six hours, which no UTC stamp could; the change log dates the migration; every laboratory's interface holds the results it releases from Saturday evening and sends them on Monday morning, so the week-2 batch sent on Monday 18 January (after the 08:00 cutoff) reads as arriving before it | the influenza A and B rows; corrected and cancelled results; the merged hospital's two identifiers; UTC release times against the local week | results (facility, accession, test code, target, status, released, received), aggregate reports (tests by laboratory, virus and week), stream register (facility to laboratory), test code list, FCP-2 (s.2, s.3, s.5), platform change log (the migration), dictionary: 7 files, 12 columns | every receipt time read as UTC (every stream high: 99.2 to 99.7 against the answer's 93.9 to 98.0 outside Brandmoor, whose three read 50.5 to 51.6 against 47.4 to 48.3); only rows received before their release shifted (every stream 0.4 points or more high); every pre-migration row shifted and week-3 rows too (the answer for week 2, harmless to week 3); rows with a negative lag dropped (every stream 5 points or more low); the answer, every figure at least 0.0099 points from a rounding edge (Brandmoor's three at about 48 per cent, its interface's lost half never resent) |
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

- **Cracker keeps:** 1 of the 40 ask criteria (the chart's structure), measured on the cut pack.
- Mirror leakage: 2.5 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the call's
  construction).
- Pair ceiling: 29.9 (cracker 46.4 with the call and 1 of 40 ask criteria; mirror 13.4).
Measured by: generator/ceiling.py on the cut pack (target.zip d84a1971): each response's ask figures recomputed from
target/ with its handling (every receipt time read as UTC, specimens by accession) and scored against the golden
handling on the same files; the full includer keeps 40 of 40.

## Pre-ship check

1. Domain: the call stands on each stream's week-3 tests predicted from its own test positivity, the surveillance
   field's measure of activity that a lost message cannot move, through the laboratory's testing response (a Poisson
   fit on positivity and trend over its aggregate reports); FCP-2 s.5's week-2 check keeps that way (largest miss 7.8
   per cent; last week's report 54.0, the held results 52.6, the other laboratories' change 44.5). With last week's
   count in its place 9 cells change, with the seasonal baseline 9, with the other laboratories' change 3. With meters
   or tills for laboratories there is no positivity to read.
2. Two layers: Layer 1 (influenza A and B rows at three laboratories, corrected results, cancelled orders, UTC release
   times against county weeks, the merged campus's second identifier, resubmitted reports, the broker's receipt clock)
   is neutral on the call, each item asserted (R2, SF rows); Layer 2 is the positivity-driven estimate of the week's
   tests, asserted alone to move the default path to the golden (R3b) and kept by the s.5 check under either receipt
   clock and either vintage of its inputs (SF13 to SF15, C1).
3. No banned stump decides: nothing is planted (Brandmoor's week-2 outage and the week-3 losses are recorded only as
   their effect on the messages; no memo, alert or draft); not semantics (the default path reads every field and code
   right, runs the check over the textbook baselines and files 9 wrong cells, asserted on the clean truth, R3a); not
   rule application (FCP-2 files the ratio, its denominator, the line and the check's criterion in general terms and
   names no way, predictor or input for the week's tests, asserted on the protocol's text).
4. Gate G: no shipped artifact estimates, flags or ranks a stream; the four distractors count no laboratory's tests.
5. Determinism: every asserted positivity model escalates the golden six (nearest stream 0.069 from the line under
   the log models, 0.031 under the linear ones, 0.074 under the golden fit), and every positivity way that beats every
   other way in the check escalates them; the check's inputs read the same as they stood at the cutoff (every earlier
   report filed by 13 January; the held tests and their results unchanged since); every receipt reading puts every
   week-3 result before its cutoff (SF6); every week-2 figure sits at least 0.0099 points from a rounding edge;
   specimen counts are integers. Judge (architecture 2, round 1): DETERMINISTIC, APPROVE; Gate G method_or_model_selection,
   analytical_non_defect, no surface read; Gate H domain pass, layers pass, decisive step analytical. The judged bundle
   and the shipped one differ only in seeded noise (the cancelled-order fix moved the records generator's later draws:
   first submissions, submission dates, message ids and the three distractors); every report of record and every
   graded figure is identical, and the judge's agent recomputed every figure on the shipped zip.
6. Asks: A (29 figures) is moved in every figure by the receipt clock (the UTC reading gives 99.2 to 99.7 against
   93.9 to 98.0 outside Brandmoor, 50.5 to 51.6 against 47.4 to 48.3 at Brandmoor), B (10) in every figure by the
   accession key (2,976 to 12,863 against 2,835 to 9,204); the call reads neither column (asserted by shifting every
   receipt time and by scrambling patients and collection times).
7. Input gates: 10 files in three formats (csv, xlsx, pdf), the result extract at 211,361 rows, four distractors
   named in metadata.json (the vaccination coverage file added at the 10-31 repair); 487 generator checks with the realism sweep; the verifier (its own Poisson fit) green; two builds
   byte-identical; figures_check 103 of 103; containers clean.
8. Duplicate guard: `guard.py heart` WARN (repeat.question_form against task194, the decision's own form for a set of
   streams; same_puzzle_older differentiated against task231 and task445; the driver near only its own lineage);
   `guard.py surface` promoted six pairs for the author's adjudicated read, none a shared mechanism: task233 (a README
   and a designation set), task232 (the same pairing two builds apart: SLA thresholds behind enteric transmission, not
   completeness), task81, task95 and task73 (surface in the corpus top 1 per cent, other mechanisms), task231 (the time
   gap and G12, differentiated on the card).

## Leak check

leak.py REVIEW, no LEAK (--asof 2027-01-25; three design-note vocabulary lines, all harmless). Reader (architecture 2):
Q1 none names the step (the nearest, FCP-2 s.5's criterion, names the check and no candidate; s.4 fixes when the call is
made); Q2 to Q4 none; Q5 s.3 and s.4 execute to the week-2 figures and leave week 3's denominator to be estimated,
s.5 choosing the way; Q6 an analytical choice (estimating the week-3 denominators and choosing by the s.5 check).
Realism: the pre-migration receipt clock is the Ask A device (CHG-2027-0019 records the migration and names no clock);
cancelled orders received on Sundays while the interfaces held every result, numbered in a block above each
laboratory's accessions, were fixed in the generator (held and lost with the results, numbered in sequence; goldens,
figures.json and the write-up byte-identical); the register's "visible" sheet names are the reader's printout of the
sheet state. The reader's question whether the clock could decide a week-3 stream near the line: no receipt is stored
after 08:00 on 25 January, so every reading puts every week-3 result before the cutoff (SF6, asserted).

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
- Architecture 1 (drawn 2026-10-16, built and judged 2026-10-17): the week's tests estimated from each stream's own
  positivity with no filed text directing how the week's tests are estimated; judge round 1 DETERMINISTIC, FIX_NOW (the
  dictionary's UTC receipt time, fixed), round 2 NOT_DETERMINISTIC, SEND_BACK, underspecified_objective (the data favoured
  the positivity fit, 2.9 against 5.7 per cent, but nothing directed a solver to compare ways). Spent; re-rooted as
  architecture 2 with the protocol's week-by-week check filed and week 2 given an interface outage.
- A filed back-test over the season's closed weeks (architecture 2 draft): with no losses in those weeks the week's own
  received count would score best and escalate nothing, and with the holiday weeks in, the other laboratories' change
  scores level with a positivity fit (6.0 against 6.4 per cent on average); the check on the last closed week, when
  Brandmoor lost half its results, separates the ways under every reading.
- Brandmoor resending its lost week-2 results on 20 January (architecture 2 draft): read with every week-2 result in
  the extract, the week's received results then missed by 0.8 per cent at most and would have kept themselves; the
  lost results are not resent by the extract, so that reading also keeps the positivity fit.
- The log-linear fit with trend as the golden model under the check: a Poisson fit on the same terms missed week 2 by
  7.8 per cent at most against its 8.0, so the golden is the Poisson fit, the closest of the ways tried; the call is
  the same under either.
- Cancelled orders sent through on Sundays while the interfaces held every result, on accessions numbered in a block 45,000
  above each laboratory's tests (the leak reader's realism note, architecture 2): they now pass through the interface like
  results (held over the weekend, lost in an outage) on accessions numbered in sequence; no figure moved.
- 2026-10-31, the README and the data dictionary: withdrawn at the batch 1 repair (files describing the data; the
  dictionary listed every column of the results extract). The report of record and the status codes are FCP-2's
  (s.2, s.3), the week's county date is FCP-2 s.2, and the extract now names its two UTC columns (released_utc,
  specimen_collected_utc) while the receipt column keeps the broker's stamp with no zone, as the extract had it.
- 2026-10-31, the prompt in the which form with a PNG beside the workbook (both over their corpus caps): the question
  asked in the whether form and the chart an SVG; the card answers task482 v14 with a differentiation line.
