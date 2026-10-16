# task234 design note

Architecture 1 (drawn 2026-10-16), wave 2, seed DQ07 (which laboratory feeds get a volume-drop alert against the seasonal
baseline): the seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10 rules.
Epidemiology & Public Health, disease surveillance and outbreak anomaly detection, Data Quality Monitoring & Alerting. A
county health department's epidemiology unit receives electronic laboratory results for influenza, RSV and SARS-CoV-2
from eleven laboratories; every Monday its surveillance data manager sets which result streams the laboratory liaison
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
- **The call.** For each of the 32 result streams (eleven laboratories, three viruses each except the long-term-care
  laboratory's two), escalate or not for MMWR week 3 of 2027 (17 to 23 January).
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
  own patients, and this winter RSV peaked among the children's hospital's patients in November while influenza is still
  climbing among adults in January; a message lost between a laboratory and the county drops a positive result and a
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

1. Read the feed completeness protocol: a stream's completeness for a week is the results received by Monday 08:00 for
   tests resulted in that MMWR week, over the tests the laboratory's weekly aggregate report counts for that virus and
   week; the liaison escalates a stream below 80 per cent.
2. Collapse the result messages to tests for each stream (one test per accession and virus, influenza A and B rows as
   one influenza test, a corrected result once, cancelled tests out, the week by the county's local result date, the
   merged laboratory's two facility identifiers as one).
3. Take each stream's tests for week 3 from the latest aggregate report, week 2's.
4. Completeness is the week's results over those tests; escalate below 80 per cent.

Ends on: the design's wrong grid (the generator fixes the cells): the influenza streams of the two laboratories losing
results stay unescalated (influenza tests rose by about a third in the week) and healthy streams whose epidemic is
falling are escalated.

Golden (design): every stream of the two laboratories whose interfaces lost results mid-week, and no other.

## Stump sentence

A competent solver divides each stream's week-3 results by the tests in last week's aggregate report and files a wrong
grid (Ends on: the losing laboratories' influenza streams left alone, healthy falling streams escalated); the step that
lands it there is taking the week's tests from the past instead of from the stream's own positivity, which moves with
its patients' epidemic and not with a lost message.

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
- **Layer 1:** result messages at the target level from some laboratories (influenza A and B as separate rows) and at
  the test level from others, corrected results resent under the same accession, cancelled tests, result times in UTC
  against MMWR weeks counted on the county's local date, one laboratory sending under two facility identifiers after a
  merger, and aggregate reports revised after first filing, each as the laboratories' and the platform's systems
  produce them; nothing is placed to be caught, and on the clean truth the default path and the golden are unchanged.
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
  stream's tests from last week's aggregate report and files the default path's Ends on; the seasonal baseline of the
  same weeks in earlier winters files another wrong grid; `checks.py` runs both on the generator's clean truth and
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

## Tried and rejected

- One stream per laboratory, every virus pooled (prototype 2026-10-16): the pooled positivity mixes the children's
  hospital's RSV and influenza clocks, and the county's indicators and the aggregate reports are per virus; rejected for
  the laboratory-by-virus grid.
