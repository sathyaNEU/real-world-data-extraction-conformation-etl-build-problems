# task398 design note

Architecture 1, drawn 2026-11-03. The number was handed out against seed RC04 (a commuter line's five delay causes and
its one winter fix). The rail world has no Root-Cause task type in the client taxonomy, so the build keeps the seed's
decision shape (which one of five causes gets the one fix, priced as the shortfall the fix would have removed, with the
runner-up) and moves to another client domain, world and dataset under the same objective and number (`CLAUDE.md`, a
stuck build is unblocked, never parked). Thornbury Fund Managers runs the Thornbury Managed Risk UK Equity Fund, a UK
open-ended fund whose two equity sleeves are run by external sub-advisers and whose equity exposure a futures overlay
cuts to 40 per cent when the fund's own price falls more than 8 per cent below its recent high. In the accounting year
to 30 September 2026 the fund trailed its benchmark; its board makes one change for 2026-27 in the annual assessment of
value.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task398.json`, architecture v1, drawn and registered 2026-11-03.
  `guard.py check` on the draft returned PASS after one persona was redrawn (a first-name WARN); nearest drivers 0.06
  (task193 v2, task65 v1 lineage, task36 lineage, task50 v4), none the same insight.
- **Pairing:** Quantitative Finance (client domain) / `factor-return-attribution` / Root-Cause Analysis. The task type
  serves Root-Cause only; `quantitative-finance x root-cause` has never been built (`guard.py coverage`, 2026-11-03).
  The four quant-finance cards on file (task135, task178, task271, task306) are forecasting, descriptive and
  opportunity-sizing builds; none attributes a fund's shortfall.
- **Objective and call:** which one of five changes the board makes for 2026-27, decided by attributing the 2025-26
  shortfall against the benchmark to its causes and pricing each change at the shortfall it would have removed. The
  decision faces forward (the change runs from the 2026-27 accounting year); the pricing is retrospective because the
  board's assessment-of-value terms price every candidate change on the closed accounting year, the only year whose
  record exists. The tag stays Root-Cause Analysis: the work is naming what caused the shortfall, rivals ruled out on
  the replayed year; nothing is forecast.
- **Shape:** 01, a ranked list under a cap of one: each of the five changes with the shortfall it would have removed,
  the call, the runner-up and the gap, plus the asks (`## Ask sheet`, stage 2).
- **Strategy and Gate G:** `decomposition_attribution`, Gate G `decomposition_attribution`: every reported figure in the
  pack is correct; the call turns on assigning the year's shortfall to the cause that produced it when one component's
  loss and the fund's own exposure rule interact. Gap objective (the attribution's effects are correct and are not what
  the decision is scored on, the shortfall a change would have removed) then time (the rule acts on the price path);
  pattern none; generators G4 (attribution at the transition into the defensive allocation), G3 (the recorded exposure
  against the rule's operation).
- **Furniture:** forum `board_of_directors` (the authorised fund manager's board approves the assessment of value and
  its actions), forcing event `statutory_or_regulatory_filing` (the annual assessment of value the authorised fund
  manager must publish), org family `financial_institution`, role family `research_desk` (the authorised fund manager's
  investment oversight analyst), context artifact `filed_standard` (the prospectus and the board's assessment-of-value
  terms), calibration none. None is held by the last three live cards (task483, task274, task277).
- **People** (`guard.py names --geo "United Kingdom" --seed 398`): Carol Rowe (head of investment oversight, owner of the
  review terms), Julia Parry (the overlay manager's client portfolio manager), Naomi Collins (fund accounting at the
  administrator). None appears in the prompt.
- **Data-native sentence:** the fund's equity exposure is not a choice anyone recorded but the output of a rule run every
  dealing day on the fund's own accumulation share price, so the year's records hold the exposure the rule chose for the
  fund that existed, with Penrose Bank's collapse in its price, and any change that moves the March price path moves
  the exposure the rule would have chosen.
- **The abstraction sentence** (what a reviewer holding this build beside its nearest approved build would call the same):
  "a component's loss that carries a whole across the line of a filed rule keyed to the whole's own path owns the rule's
  response, and holding the recorded response fixed books it to the rule." Written against every approved and delivered
  driver on Root-Cause and Quantitative Finance (`guard.py mechanisms --objective root-cause`, the four quant cards):
  task202 routes an input to a layer by physics, task129 places a rise outside a provider's zone, task111 asks which
  cause still operates forward, task303 removes a shared supply loss logged under each feeder, task178 removes an
  absorbing agent from a forward dispersion; none is a rule keyed to the whole's own path re-run in a counterfactual.
  It cannot be written against any of them.
- **Same-puzzle and same-driver tests:** gap objective, decisive generator G4 and pick_one_of_n repeat no card in the last
  twelve; `guard.py check` PASS.
- **Library test:** the golden is not a named correction. The field's method for the deciding quantity, return
  attribution (by sleeve, overlay and cash, linked over the year), sits at rung 1; the decisive step is recognising that
  this fund's exposure was set by a rule on its own price, so a change's counterfactual has to run the rule again.
- **Sources** (every file synthetic, generated by `generator/` from seed 398, invented world, no real organisation or
  index; licence CC BY 4.0, recorded in `metadata.json` at stage 3): custody holdings from two custodians either side of
  the 1 April 2026 depositary change (the spine), the administrator's daily share prices and fund flows, the overlay
  manager's daily exposure report and futures blotter, the index provider's daily levels for the benchmark and the two
  style indices, the two sub-advisers' monthly reports, the prospectus extract, the board's assessment-of-value terms, the
  corporate actions file, and distractors named in `metadata.json`.

## Default path

The route a competent analyst builds without thinking, from the prompt's words and the files' grain, with the field's
method for the deciding quantity in it:

1. Conform the two custodians' holdings (SEDOL against ISIN, pence against pounds), the administrator's accumulation
   share price and the index provider's total return levels for the accounting year.
2. Compute the fund's shortfall against the benchmark over the year and attribute it the way performance analysis does:
   each sleeve's selection effect against the benchmark, the overlay's effect (the fund's equity exposure against full
   exposure, times the benchmark's return, day by day), the cash buffer's drag, linked over the year.
3. Price each candidate change at the effect its cause carries: indexing the value sleeve removes the value sleeve's
   selection effect, indexing the growth sleeve the growth sleeve's, raising the drawdown trigger to 12 per cent the
   overlay's effect, restoring full exposure at 6 per cent the part of the overlay's effect after the fund came back
   within 6 per cent, equitizing the cash its drag; or replay each change on the year holding the overlay's recorded
   daily exposure, which gives the same ranking.
4. Rank the changes and name the largest.

Ends on: raising the drawdown trigger to 12 per cent, about 600 basis points of the shortfall removed, against about 240
for indexing the value sleeve (design targets; the measured figures replace them at stage 3).

Golden: indexing the value sleeve, about 820 basis points removed, against about 600 for raising the drawdown trigger
(design targets): with the rule run on the changed fund's own price, the fund without the Penrose position never falls
8 per cent below its high in March, so it stays fully invested through the April-to-June rebound.

## Stump sentence

A competent solver attributes the 2025-26 shortfall by sleeve, overlay and cash, books the April-to-June rebound the
defensive allocation missed to the drawdown overlay and files raising the trigger to 12 per cent (the `Ends on:`, about
600 basis points against about 240 for indexing the value sleeve); the step that lands it there is holding the overlay's
recorded exposure fixed in each change's counterfactual, when the rule sets that exposure from the fund's own price and
Penrose Bank's collapse in the value sleeve is what carried the March drawdown past 8 per cent.

## Three rules

Task type: `factor-return-attribution`, Quantitative Finance, which the taxonomy serves with Root-Cause Analysis only:
attributing a fund's return against its benchmark to the decisions and components that produced it.
Domain test: the deciding quantity is the shortfall against the benchmark each candidate change would have removed in
the accounting year, which performance analysis prices by return attribution (selection by sleeve, the overlay's
exposure effect, cash), linked over the year; the attribution is the default path's method and sits at rung 1.
Swap: "which one of five changes the hospital makes, priced at the waiting-list shortfall each would have removed" keeps
the sentence and loses the analysis: no ward carries an exposure that its own waiting list sets through a filed line,
and no benchmark measures the ward, so there is nothing to attribute and no rule to run again.
Layer 1: the depositary and custody change on 1 April 2026 (the old custodian keys holdings by SEDOL and prices them in
pence, the new one by ISIN in pounds); the accumulation and income share classes (the income price drops at each
ex-dividend date, the review runs on accumulation); the overlay manager's blotter in UTC across the 29 March clock change
with quarterly futures rolls; the fund's noon valuation point against the index's close; Penrose Bank's suspension
(no price after 13 March) and its resolution value of zero; one sub-adviser's monthly workbook with a header block and
the other's PDF table. Each comes from the system named and none is placed to be caught or carries the call.
Layer 2: `estimand_identification`, the right counterfactual: what the fund would have returned had a change applied,
when the fund's equity exposure is the output of a rule on the fund's own price.
Decisive step: replay the accounting year for each change with the drawdown rule run on that changed fund's own
accumulation price, so the replay for indexing the value sleeve, whose price never falls 8 per cent below its 63-day high
without the Penrose position, stays fully invested from 23 March to the end of June.
Not semantics: every field, unit, code, share class and clock read correctly still yields a correct attribution that
books the defensive allocation's cost to the overlay; no field says what the exposure would have been for another fund.
Not rule application: no filed rule or procedure says which change would have kept the March drawdown inside the rule's
line; the prospectus states how the overlay sets exposure from the fund's price and the review terms price each change
on the year, and executing both on the attribution's effects, or on a replay that keeps the recorded exposure, files
the trigger change. Enumerated family (target values, measured at stage 3): the linked attribution and the
exposure-held replay file the 12 per cent trigger; the manager scorecard against each sleeve's style index files
indexing the growth sleeve; the replay with the rule re-run files indexing the value sleeve. Standing family: the
replays that run the rule on each changed fund's price under every licensed convention the prospectus leaves open (the
63-day window including or excluding the day, the dealing day the cut takes effect), spread on the graded call zero;
the ruling-out is the March drawdown path rebuilt without the position, which the attribution never asks for.
Analyst test: a strong analyst who conforms every file and reads the prospectus correctly prices each change on the
year's attribution, or replays it holding the recorded exposure, and files raising the drawdown trigger to 12 per cent,
the default path's `Ends on:`, because it treats the overlay's March cut as the overlay's own decision rather than the
rule's response to the fund's price.
Estimand: the board's assessment-of-value terms (`review_terms` in the pack, the authorised fund manager's own genre):
the one change that removes the most of the accounting year's shortfall against the benchmark; population, the fund's
B Accumulation shares; outcome, the shortfall removed; window, 1 October 2025 to 30 September 2026; unit, basis points of
the year's return; comparison, the year with the change in place from 1 October 2025 against the year as it ran.
No decoy: nothing is planted to be caught; no memo, briefing, draft or stakeholder figure argues for the trigger change;
every price, holding, exposure and attribution figure is correct and no shipped artifact ranks the changes.
No certified replay: no certified or published figure is reproduced to recover a method; the decisive step is a replay
of the fund's own rule on a rebuilt price path, not a rule recovered from closed cases.
Lesson: a model learns that when a portfolio's exposure is set by a rule keyed to the portfolio's own path, a holding's
loss can carry the path across the rule's line, and the cost of the rule's response belongs to that holding's
counterfactual; attribution that holds the recorded exposure books it to the rule. No build on file teaches a
counterfactual through a rule keyed to the unit's own path (`guard.py slots` on overlay, drawdown, de-risk, managed
volatility, target volatility and risk control returned no mechanism, 2026-11-03).

## Survivor anatomy

Actor: each dealing day has rows (holdings, prices, the overlay's exposure), and the deciding property, whether the
changed fund's price would have crossed the 8 per cent line on 20 March, has no column in any file: it is the drawdown of
a price path that never existed, rebuilt from the sleeves' daily returns.
Link: read across the custody holdings, the administrator's prices and the overlay manager's exposure report with no key
between a holding's loss and the overlay's cut; the attribution never asks what the exposure would have been.
Reflex: the field's return attribution (selection by sleeve, the overlay's exposure effect, cash, linked) sits at rung 1
and files the trigger change, the `Ends on:`.
Back-test: the textbook route validates: the attribution's effects add exactly to the year's shortfall under the linking,
and every sleeve's attributed return reconciles to the sub-advisers' own reports and the administrator's prices, so
every check an analyst runs on the attribution confirms it (asserted at stage 3).
Second use: the custody holdings carry every sleeve figure the asks grade; the overlay report carries the exposure and the
futures the roll-cost ask reads; the administrator's prices carry the share-class asks; none is in the pack only for the
decisive step.
Shock: the March cut reads as the overlay doing its job in a falling market, two dealing days after an index fall; it is
not the only cut on any sort of the shipped figures, and the value sleeve is not the top of any shipped statistic.
Pins: the WHAT sits in the board's assessment-of-value terms in the authorised fund manager's own genre (the shortfall
against the benchmark, the accounting year, each change in place from the year's start); no filed sentence names the
March drawdown, the Penrose position's part in it, or a replay of the rule.

## Tried and rejected

- 2026-11-03, the seed's own world (a commuter line's five delay causes): refused before any harness. No task type in the
  taxonomy serves Root-Cause for transport: `supply-chain-logistics` maps to `urban-regional-science`, which serves no
  Root-Cause task type (`guard.py check` BLOCK `three_rules.task_type` on a probe card), and to
  `general-statistics-data-science`, whose only Root-Cause task type is `interpretability`, which the author ruled a
  backdrop for an operations world at task129 v1. The seed's own stump (lost time recovered before the terminal) is also
  task202's abstraction (how much of each input reaches the place the outcome is measured), which the brief bars.
- 2026-11-03, rail under `human-factors-ergonomics` (signals passed at danger, platform overruns, signaller workload):
  the incident counts on one line are too thin to grade, red-signal approaches as exposure was screened at task175, and
  workload exposure built from the activity log is task121's abstraction.
- 2026-11-03, grid reliability screens, each dead on paper: concurrent upstream unavailability (task201's measured death,
  storm collinearity); a transformer out for months leaving a substation on one supply, its loss-of-supply events
  credited to the failure's cause (reads as task303's substation supply losses and programme credit, same shape and
  shell family); crew-queue knock-on (task111 measured same-resource knock-on as a reflex, and the counterfactual
  dispatch forks); restoration staging (task201's restoration accounting and the seed's absorption); protection
  miscoordination and fuse-saving zones (an odd-one-out candidate sized by one filter); customers over an interruption
  count (the metric's definition executed); cold load pickup (inside the cause's own records); joint infant mortality
  after replacement (task183's repeat failures); a reliability metric's major-event-day reclassification (the standard
  executed, and task129's ground).
- 2026-11-03, pollution source attribution screens: exceedance days against given daily contributions (task202's screen:
  the estimand executed), a contaminated upwind background (the background choice forks), inversion amplification
  (reach, and dispersion parameters fork), secondary nitrate (chemistry parameters fork).
- 2026-11-03, a volatility-target overlay keyed to the fund's own volatility: a single holding's crash moves the
  volatility by the square of its weight while its direct loss moves with the weight, so the overlay's response never
  outweighs the direct loss and the attribution already ranks the holding first (prototype `proto2.py`, scratch, 20
  seeds). The drawdown rule keeps the mechanism and makes the response first-order in the weight (`proto3.py`).
