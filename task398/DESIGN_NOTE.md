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

Ends on: raising the drawdown trigger to 12 per cent, 520 basis points of the shortfall removed, against 310 for running
the value sleeve as a tracker (measured on the shipped pack: the linked attribution 547 against 306, the exposure-held
replay 519 against 313).

Golden: running the value sleeve as a tracker, 830 basis points removed, against 520 for raising the drawdown trigger:
with the rule run on the changed fund's own price, the fund without the Penrose position falls no more than 6.24 per cent
below its 63-day high, so it stays fully invested through the April-to-June rebound.

## Stump sentence

A competent solver attributes the 2025-26 shortfall by sleeve, overlay and cash, books the April-to-June rebound the
defensive allocation missed to the drawdown overlay and files raising the trigger to 12 per cent (the `Ends on:`, 520
basis points against 310 for running the value sleeve as a tracker); the step that lands it there is holding the overlay's
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
with the contracts' quarterly expiries; the fund's noon valuation point against the index's close; Penrose Bank's suspension
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
the trigger change. Enumerated family (measured on the shipped pack): the managers' own reports (the overlay's futures
loss 498, Fennick 310 behind its growth index, the cash drag 50, Ashcombe ahead of its value index) file the trigger; the
linked attribution (547 against 306) and the exposure-held replay (519 against 313) file the trigger; the replay with the
rule re-run on each changed fund's own price files the value tracker, 831 against 519. Standing family: that replay under
every reading the prospectus and the terms leave (63 points with or without the day, dealing in units or in pounds,
futures commission in or out) prints 830 to 831 for the tracker and the same call, and a solver's pool approximation on
index returns with fixed or drifting weights prints 812 to 848 and the same call at 1.61 to 1.63x: spread on the graded
call zero, on the tracker's figure one bin under the filed mechanics. The ruling-out is the March price path rebuilt
without the position, which the attribution never asks for.
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
Back-test: the textbook route validates: the attribution's effects add to the year's shortfall under the linking, and
the exposure-held replay with no change reproduces the published B Accumulation price at every valuation point to the
penny (asserted), so every check an analyst runs on the easy route confirms it.
Second use: the administrator's valuation and the overlay monitor carry the attribution every route runs; the index
levels carry the benchmark the shortfall is measured on; the custody records and the corporate actions feed carry the
three asks; none is in the pack only for the decisive step.
Shock: the March cut reads as the overlay doing its job in a falling market, two dealing days after an index fall; it is
not the only cut on any sort of the shipped figures, and the value sleeve is not the top of any shipped statistic.
Pins: the WHAT sits in the board's assessment-of-value terms in the authorised fund manager's own genre (the shortfall
against the benchmark, the accounting year, each change in place from the year's start); no filed sentence names the
March drawdown, the Penrose position's part in it, or a replay of the rule.

## Readability screen

The seven tests per rung (stumping 2.1), the reflex row enumerated from the field's vocabulary for the deciding quantity
(what a change to one component would have done to a fund's return): Brinson attribution by sleeve, the overlay's
exposure effect, contribution to return, the overlay manager's futures result, tracking error decomposition, a
what-if on the recorded weights.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| Rung 0, the managers' own reports (higher trigger) | none needed | the overlay monitor's futures, the sub-advisers' relative returns | contribution read from reports | none | none | yes | none | readable |
| Rung 1, the linked attribution or the exposure-held replay (higher trigger) | the terms file the shortfall removed, the prospectus files the rule | sleeve valuations, the benchmark at 12:00, the monitor's exposure | Brinson by sleeve with the overlay's effect, the field's method | the effects add to the shortfall; the held replay reproduces the published price | none | yes | none | readable |
| Decisive, the rule run on each changed fund's own price (value tracker) (decisive) | the terms file the WHAT (the year with the change in force from 30 September 2025, the fund otherwise run as its prospectus requires) and the prospectus how the overlay sets exposure; no sentence says the exposure would differ under a change, names the March fall or Penrose's part in it | no column holds a changed fund's price or exposure | attribution and the held replay sit at rung 1 and neither re-runs the rule | the back-test confirms the easy route; nothing scores the changes | no battery step re-derives an exposure | no: a path-dependent replay over 251 valuation points with a rolling 63-point high and a one-day lag | the monitor, the valuation summary and the index levels are standing records the attribution and the shortfall read | silent |

The residual risk is the terms' clause 2.3, "the fund is otherwise run as its prospectus requires", which a reader may
take as a pointer to the overlay. It is the WHAT the estimand needs (without it the counterfactual's exposure is a fork,
SF4) and it names neither the overlay nor a replay. Recorded for the leak reader's question 6 and the judge's Gate H.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternatives, and the call under each | Ruled out by |
|---|---|---|---|---|
| SF1 | against its benchmark | the Larkspur UK All-Share total return at 12:00 | the close or the price index: the shortfall moves, no change's figure reads the benchmark's level; a tracker on close-to-close returns keeps the call | terms 2.2 (total return at the valuation point); same call (asserted) |
| SF2 | 2025-26 | 12:00 on 30 September 2025 to 12:00 on 30 September 2026 | the calendar year, or 1 October onward | terms 2.2 |
| SF3 | the fund's return | B Accumulation | another class: the rule reads B Accumulation, every class moves with the same gross return | terms 2.1 |
| SF4 | the change in force | the fund run under its prospectus with the change, the rule run on its own price | the recorded futures held: a different fund from the one the prospectus runs once the price path moves | terms 2.3 and prospectus 4.3 (asserted: the replayed states differ from the recorded ones) |
| SF5 | removed | the replayed B Acc return less the return as it ran, in basis points | a share of the shortfall | terms 2.1 and the prompt's unit |
| SF6 | from 30 September 2025 | the change in force from the base valuation point, no reduction pending | none | asserted: FULL at the base, drawdown under 8 per cent |
| SF7 | the 63 valuation points | ending with the day in question | ending the day before: same states, same figures | prospectus 4.3; same call (asserted) |
| SF8 | from the next dealing day | the futures traded at the next valuation point | the same day, or two days on: the call holds, B, D and E move | prospectus 4.3 and 4.4 (asserted) |
| SF9 | within 4 per cent | at or under 4.00 per cent | strictly under: no reduced valuation point sits on the line | same states (asserted) |
| SF10 | more than 8 per cent | strictly over 8.00 per cent | at or over: no fully invested valuation point sits on the line | same states (asserted) |
| SF11 | a tracker of the benchmark | the benchmark's total return between valuation points | close to close: same call | terms 3; same call (asserted) |
| SF12 | dealing as it was | each class's units dealt in proportion to its units in issue | pounds dealt as recorded: same figures; dealing left out: same call | terms 2.3; same call (asserted) |
| SF13 | futures commission | the blotter's rate per contract on every contract traded | left out: same figures | same call (asserted) |
| SF14 | the futures' return | the contract's 12:00 mark | the Larkspur 100's 12:00 level, fixed or drifting weights: same call | prospectus 4.1; same call (asserted) |
| SF15 | the price the rule reads | the published price in pence to two decimals | the unrounded price: no valuation point within a rounding unit of a line | same states (asserted with SF9 and SF10) |
| SF16 | equitised liquidity sleeve | futures as near as possible to the liquidity sleeve's value, set at each valuation point while not reduced | at a quarter-end, SF31 | terms 3 |
| SF17 | earlier restoration | within 6 per cent closes a reduction | none | terms 3 |
| SF18 | higher trigger | more than 12 per cent opens a reduction | none | terms 3 |
| SF19 | transition costs | none | none | terms 2.3 |
| SF20 | charges under a change | unchanged: the authorised fund manager pays the sub-advisers from its charge | a tracker's lower fee | prospectus 5.1 |
| SF21 | the gap | the call's figure less the runner-up's | from printed figures: the same 310 | asserted |
| SF22 | dividend income | gross, no tax withheld on a UK dividend | none | same figures |
| SF23 | paid or still to be paid | Penrose's March final out: its shares were cancelled on 23 March and no payment reached Northcote by 16 October, six months after its pay date | in, as Holloway's due line: V Jan-Mar 3,093,000 against 3,032,000 | the prompt's clause; asserted |
| SF24 | in cash or in new shares | a scrip election counted at the cash dividend | at the new shares' value: the fraction lapses, a few pounds | the prompt's clause |
| SF25 | each quarter of the accounting year | October to December, January to March, April to June, July to September | calendar quarters: the same months | the prompt |
| SF26 | commission and stamp duty | the sleeves' broker commission and stamp duty reserve tax | futures commission added: not a sleeve's dealing | the prompt ("each sleeve's") |
| SF27 | the date of the trade | the trade date | the settlement date: every cell moves | the prompt |
| SF28 | holdings at the custodian, at its prices | settled holdings at the custodian's close prices | trade-date holdings: the prompt names the custodian | the prompt |
| SF29 | each quarter-end | the last valuation point of each quarter, every one a dealing day | none | asserted |
| SF30 | the holding a dividend is paid on | the settled holding on the record date | the holding on the ex-date: the same on every dividend of the year | asserted |
| SF31 | the liquidity sleeve's value that sizes the equitised futures at a quarter-end | after the cash moved between the sleeves at that valuation point (-50 bp, -50.1 unrounded) | before the transfer, the valuation summary's value at the valuation point: -57.8, filed -60 (the judge's pass 1 finding) | terms 3 ("at the last valuation point of a calendar quarter the liquidity sleeve's value is taken after the cash moved between the sleeves at that valuation point"); asserted |

## Ladder

Measured on the shipped pack, each change's basis points of the year's B Accumulation return:

| Rung | What it computes | A value tracker | B growth tracker | C higher trigger | D earlier restoration | E equitised | Files | Margin |
|---|---|---|---|---|---|---|---|---|
| 0 | the managers' own reports: the overlay's futures loss, each sub-adviser against its style index, the cash drag | -47 | 310 | 498 | 0 | 50 | C | 1.61x |
| 1 | the linked attribution, each change at its component's effect (the default path) | 306 | 11 | 547 | 118 | 17 | C | 1.78x |
| 1b | the exposure-held replay (each change applied, the overlay's recorded futures kept) | 313 | 11 | 519 | 82 | -10 | C | 1.66x |
| decisive | the replay with the rule run on each changed fund's own B Acc price | 831 | -29 | 519 | 82 | -50 | A | 1.60x |

The golden is last on rung 0, second on rung 1 by 1.78x and 1.66x and first only on the decisive rung (asserted). One
cheap route reaches the call: the replay. Dominance: the tracker's edge on the decisive rung, 312, is 1.30 times the
trigger's advantage on rung 1, 240 (asserted). The configuration that decides is in the record: as it ran, the price
closed 8.7 per cent below its high on 20 March 2026 and exposure was cut from 23 March to 8 June; replayed with the value
sleeve as a tracker its deepest fall is 6.24 per cent below its high (2 April) and it is never cut; as it ran it never fell 11 per cent
below its high, so the higher trigger never fires.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the B Accumulation shares; the changes on the terms' list | terms 2.1 and 3 |
| 2 | Unit of account | basis points of the year's B Accumulation return | terms 2.1 |
| 3 | Attribution window | 12:00 on 30 September 2025 to 12:00 on 30 September 2026 | terms 2.2 (SF2) |
| 4 | As-of dating | each valuation point's published price; each change in force from the base point | terms 2.1, prospectus 4.3 (SF6) |
| 5 | Version basis | one release of every series, nothing revised | C1 |
| 6 | Denominator | none: a difference of returns | terms 2.1 |
| 7 | Weighting | the fund's own sleeve values at each valuation point, rebalanced at quarter-ends | prospectus 3.2; C1 across pool weightings (SF14) |
| 8 | Window length | 63 valuation points | prospectus 4.3; C1 with or without the day (SF7) |
| 9 | Boundary inclusivity | more than 8, within 4 | prospectus 4.3 and 4.4; C1, nothing on a line (SF9, SF10) |
| 10 | Rounding path | carried unrounded, rounded once at the stated unit | C1 (SF21); every graded figure at least 0.07 of a bin from its edge, the tightest the AIM share at 31 December 2025 at 0.081 (asserted) |
| 11 | Tie-break | none | 831 against 519 |
| 12 | Maturity and censoring | a closed year | terms 1.1 |
| 13 | Order of operations | valuation, dealing and charges, quarter-end rebalance, the overlay at the next valuation point | prospectus 2.1, 3.2, 4.3; C3 on the lag (SF8) |
| 14 | Row order | none: a time series | C1 |
| 15 | Duplicate resolution | none on the call; the asks' open trades counted once | asserted in verify |
| 16 | Identity normalisation | SEDOL to ISIN through the security master (asks only) | the master's two keys |
| 17 | Netting against gross | units created and cancelled net per class | C1 (SF12) |
| 18 | Dimensional units | prices in pence, values in pounds, futures in points at GBP 10 | prospectus 4.1 and the files' headers |
| 19 | Code and status semantics | the monitor's state column describes the fund as it ran and is not read by the replay | C1 |
| 20 | Integerisation | whole contracts | prospectus 4.1; C1 (SF13, SF14) |
| 21 | Clause scope | the rule at every valuation point, every change from the year's start | prospectus 4.3, terms 2.1 |
| 22 | Forward window contents | none needed: the forward decision is priced on the closed year | terms 1.1 |

## Literal reader

Executed word for word on the shipped text: the prompt asks how big the 2025-26 shortfall was, which change on the
board's list would have removed most of it and how much each would have removed. The review terms file the measure: the
B Accumulation return over the accounting year had the change been in force from the 12:00 valuation point on 30
September 2025, less the return as it ran, in basis points, the market and dealing taken as they were, a sleeve left with
its sub-adviser keeping that sub-adviser's holdings, and the fund otherwise run as its prospectus requires. A literal
reader builds the fund the prospectus describes (the sleeves, the liquidity sleeve's dealing, charges and margin, the
quarter-end rebalance, the overlay's rule at 8 and 4 per cent on 63 valuation points with the next dealing day's
futures), changes what each change changes and runs the year: the value tracker 831, the higher trigger 519, the earlier
restoration 82, the growth tracker -29, the equitised sleeve -50. Where the text is silent the readings converge (SF1 to
SF21), and the one reading the record did not settle, which value of the liquidity sleeve sizes the equitised futures at a
quarter-end, is filed in the terms' own definition of that change (SF31). The easy answer comes from the same literal estimand executed with an easy method (the attribution, or a replay
that keeps the recorded futures), never from another reading of a term. The asks' readings are closed the same way
(SF22 to SF30); each device's wrong handling reads a record for something it is not (Holloway's due line for a dividend
that will be paid, Holloway's report for every dividend, a settlement date two weekdays back for the trade date across a
bank holiday, today's market segment for the segment at a quarter-end), each refuted by a cross-file tie a grader can
confirm.

## Oracles

- The overlay monitor's drawdown column: the fund as it ran, 8.7 per cent on 20 March. It ties to the published price
  and confirms the rule's operation for whoever reads it; it holds nothing about a changed fund.
- The sub-advisers' reports (Ashcombe's workbook, Fennick's PDF): each manager against its style index, a different
  question answered correctly; they put Fennick furthest behind its mandate, which rung 0 reads.
- The exposure-held replay reproduces the published B Accumulation price exactly when nothing changes: a second source
  agreeing with the wrong path, the shape that held.
- The corporate actions feed: the asks' referee for ex-dates, record dates and listing transfers; it ranks nothing.
- Holloway's open-trades list: the trade dates of the trades in flight at the change of custodian; it ties to
  Northcote's settlements of 7 and 8 April by security, quantity and consideration.
- No published figure, certified total or reconciliation column ties only under the golden. The prior year's published
  assessment and the Larkspur 100 factsheet (the distractors) tie to nothing.

## Ask sheet

**Shape 01, the criteria.** The call side: the call, the runner-up, the gap, the shortfall and each change's figure (9).
The chart: a bar for every change, labelled in basis points, a title naming the measure (3). The files: 2. The asks: 24
figures. 38 criteria. Weights 38 on the call side and chart, 7 on instruction-following, 55 on the asks.

- **Ask A1, each sleeve's dividend income by quarter of the accounting year, by ex-dividend date, paid or still to be
  paid (eight figures, nearest GBP 1,000).** H18 home: the income the income classes distribute and the assessment's
  income line, a measure every change carries that the call does not turn on. Path: Holloway's entitlement report,
  Northcote's statement, the corporate actions feed, both custodians' positions, the security master (five files).
  Primary 1 (D4/D5, an absence no habitual join reaches): Holloway's entitlement report carries only the dividends its
  income system processed; the issuers that offer a scrip alternative ran through its elective events desk and are
  absent even where the fund took cash, so January to March and October to December miss them; only the positions
  against the feed show it. Primary 2 (D2, a due line no later record honours): Penrose Bank's March final sits in
  Holloway's report as due; its shares were cancelled on 23 March and nothing reached Northcote by 16 October. The
  report-led route files V 4,837,000 and 3,093,000, G 2,044,000 and 1,975,000 for the first two quarters. Hazards: the
  overlap of Holloway's due lines with Northcote's receipts; the scrip elections in April to June; the dividends still
  unpaid at the extract.
- **Ask A2, each sleeve's commission and stamp duty by quarter of trade (eight figures, nearest GBP 100).** H18 home: the
  assessment's transaction costs. Path: both custodians' settled statements, Holloway's open-trades list, the security
  master (four files). Primary 3 (D8, a settlement date for the event date): both custodians' statements carry the
  settlement date only; each quarter-end's rebalancing trades settle in the next quarter, and the 31 December trades
  settled on 5 January across the New Year bank holiday, so a trade date taken two weekdays back lands on 1 January.
  Settlement dates as trade dates miss all eight; two weekdays back files V 243,900 and 332,900, G 357,200 and 408,900
  for the first two quarters. Hazard: the trades open at the change of custodian, settled at Northcote on 7 and 8 April
  and listed with their trade dates by Holloway.
- **Ask A3, the growth sleeve's AIM holdings at each quarter-end: how many and their share (eight figures, per cent to
  one decimal).** H18 home: the assessment's liquidity view of the growth sleeve. Path: both custodians' positions, the
  security master, the corporate actions feed (four files). Primary 4 (D2, a label stored after a silent switch): the
  security master carries each company's market as at 16 October 2026; two holdings moved from AIM to the Main Market on
  18 May and 7 September 2026, recorded only as listing transfers in the feed. Today's segment files 8 holdings at 8.1,
  8.6, 8.0 and 7.5 per cent against 10 at 11.9, 10 at 12.3, 9 at 9.2 and 8 at 7.5.
- **Separation (asserted):** the call reads the administrator's valuation and class prices, the index levels, the
  liquidity fund, the overlay monitor, the blotter, the prospectus and the terms; the asks read the custody records,
  the feed and the master; no file is in both sets. Delete every device and the call is as hard.
- **Rounding edges (asserted):** every graded figure sits at least 0.07 of a bin from its rounding edge, measured as
  u/2 - |v - round(v/u)u| over 31 figures (the AIM counts are whole numbers); the tightest is the AIM share at 31
  December 2025, 11.942 per cent, 0.081 of its bin. Two figures sat on an edge at the first cut and were moved in the
  generator: Wath Energy's November 2025 dividend is declared at 15.80p (value income October to December 4,951,011,
  was 4,951,499), and Fennick's broker rate is 6.2 bp (growth dealing costs October to December 360,329, was 357,849).

| Ask | Cracker (lands the call, runs the battery, executes every filed statement) | Verdict |
|---|---|---|
| A1 dividend income | Holloway's report for its months, Northcote's receipts and scrip by ex-date, the unpaid dividends on the ex-date holding: four of eight (V 4,837,000 and 3,093,000, G 2,044,000 and 1,975,000 off) | miss |
| A2 dealing costs | trade dates two weekdays before settlement, the open trades matched: four of eight (V 243,900 and 332,900, G 357,200 and 408,900 off) | miss |
| A3 AIM holdings | the master's segment at every quarter-end: two of eight (8 holdings at 8.1, 8.6 and 8.0 per cent off) | miss |

Measured by: generator/ceiling.py on the cut pack (target.zip 6749a0ae; standard library and openpyxl, no generator code): the cracker keeps
10 of the 24 ask figures; the mirror on rung 1 keeps the same 10 and 5 of 12 on the call side (the shortfall, the
trigger's 520 and the chart).
Pair ceiling: 56.8 (the cracker 38 + 7 + 22.9 = 67.9; the mirror 15.8 + 7 + 22.9 = 45.8).
Mirror leakage: 41.7 per cent of ask weight.
Stress rows: the full includer (every dividend from the record-date holding against the feed, a UK holiday calendar for
settlement, each segment dated by the feed's transfers) keeps 24 of 24, the residual risk recorded here.

## Layer 1 inventory

Each item and the system that produces it; none decides the call:
- Holloway Trustee keys holdings by SEDOL with prices in pence and dates as DD/MM/YYYY; Northcote Depositary keys by ISIN
  with prices in pounds and ISO dates, from 1 April 2026, with a receive-free line for every transferred position;
- both custodians report settled holdings and settled transactions; the trades of 30 and 31 March 2026 settled late at
  Northcote after Easter;
- the overlay manager's blotter is stamped in UTC across the 29 March clock change, the fund's valuation point is 12:00
  UK time, the index provider publishes 12:00 and close levels and a price index beside the total return;
- the share classes: income classes drop at 1 October and 1 April by their distributions, accumulation classes do not;
- Penrose Bank's suspension on 16 March (the administrator values it at nil, Holloway carries its last price until the
  cancellation on 23 March);
- the sub-advisers' reports run close to close against their own style indices, one a workbook with a header block,
  the other a PDF table;
- a few issuers are incorporated in Jersey or Guernsey, so their ISINs are not GB00 plus the SEDOL.

## Leak check

- `leak.py --asof 2026-11-03`: REVIEW, no LEAK. Sweeps 1, 2, 3, 5, 6, 7, 8 and 11 clean; container metadata INFO.
- Stump-vocabulary sweep (sweep 4), ruled here and never handed to the reader: the prospectus extract, the review terms
  and the prior year's published assessment carry the fund's own words (its overlay, its exposure, its trigger, its
  managers, its accumulation shares) because they are the fund's constitution, the board's list of changes and last
  year's published conclusions; none names the March fall, the Penrose position's part in it, a counterfactual or a
  replay, and none relates one component's loss to the overlay's response. Harmless, each a fact about the world.
- Dates after the setting (sweep 9): the corporate actions feed as at 16 October 2026 carries the payment dates of
  dividends already declared, some in November and December 2026; a feed of announced events always runs ahead of its
  extract date. Handed to the reader for a ruling.
- Reader pass 1 (isolated, sonnet, medium; the pack only, target.zip 896bc527): question 1 none (the nearest sentence
  is the terms' 2.1, which defines the estimand and does not say how to reach it); questions 2 to 4 none (the
  sub-advisers' reports measure each sleeve against its own style index, a different quantity); question 5 the terms'
  2.1 and 2.2, read literally as the counterfactual B Accumulation return less the actual, the golden's estimand;
  question 6 an analytical choice; realism none, no describing file, nothing saying the world is invented; the feed's
  future payment dates ruled harmless (ordinary forward payment dates on declared dividends).
- Reader pass 2 (same brief, target.zip 6749a0ae, after the terms gained SF31's clause): question 1 none (2.1 and 2.3
  file the estimand and the counterfactual, not a step), questions 2 to 4 none, question 6 an analytical choice,
  questions 8 and 9 none, the feed's future dates harmless (payment dates on confirmed dividends whose ex and record
  dates fall on or before the feed's date). Its question 7 found the writing library's default-template properties in
  the review terms (Words 0 and Pages 1 in docProps/app.xml, a stylesWithEffects part, a blank thumbnail): the
  generator now scrubs every Office file's properties, inputs and goldens (app.xml from each file's own text, slides
  and sheets; a thumbnail of its first page or slide; the Word 2010 styles part dropped with its relationship and its
  content-types override; the deck's chart workbooks given the deck's author and dates in place of the build clock),
  asserted in checks.py, and the goldens now rebuild to the byte as well. The shipped cut, target.zip 4d9a7a57, keeps
  word/document.xml byte-identical to 6749a0ae's and changes nothing else outside those properties, so no third pass is
  owed.

## Determinism judge

- Pass 1, one isolated thread (sonnet, medium) on target.zip 896bc527: DETERMINISTIC, APPROVE. Every committed figure
  reproduced from the bundle (the value tracker 830.1, the higher trigger 519.0, the gap 311.1, the shortfall 971.7; the
  asks to the pound and the tenth). Gate G: counterfactual replay, analytical_non_defect, surface_read_dependency no,
  sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical, matching the leak reader's question
  6, so there is no split to settle. Its caveat (terms 2.3 and prospectus 4.3 state the rule, so a sceptic could call
  the replay rule application) it ruled analytical: the dynamic against static estimand and the faithful rebuild
  separate the answers, not the reading of a rule.
- Its residual points, both fixed in one generator pass with the main call, the ladder and every main-call figure in
  their bins: the equitised change's quarter-end sizing (SF31, filed in the terms' definition of that change) and two
  ask figures on a rounding edge (moved mid-bin; every graded figure's edge now asserted at 0.07 of a bin or more).
  No re-judge is owed: the fixes close the judge's own points and change no committed figure (value income October to
  December and growth dealing costs move inside the pack; growth dealing costs file 360,300, 405,800, 211,200 and
  325,700 at the new broker rate).

## Pre-ship check

- 2026-11-03, stage 4 pass 1 on target.zip 896bc527: leak reader clean (above); judge DETERMINISTIC, APPROVE (above).
- The repair pass: the terms' clause for the equitised change (SF31), Wath Energy's declared rate and Fennick's broker
  rate, on target.zip 6749a0ae; reader pass 2 clean apart from the properties scrub above.
- The ship cut, target.zip 4d9a7a57 (md5 4d9a7a579a1109be9ef577bae53d9192), every gate re-run on it after merging
  claude/jolly-hypatia-06c61h at fe35f42 (task399's architecture 3 card on file, its spent architectures in its
  lineage): checks 70 assertions 0 FAIL, verify PASS, two byte-identical builds and byte-identical goldens,
  figures_check PASS (58 figures), precut 0 FAIL, voice-check PASS, leak.py REVIEW (no LEAK), guard.py heart PASS and
  surface 0 promoted. Every graded figure is unchanged from 6749a0ae (figures.json and submission.md identical). The
  ceiling: pair 56.8, mirror leakage 41.7.
- The 10/10 rules re-read against the built pack: the decisive step is replaying the year with the overlay's rule run on
  each changed fund's own price, which the attribution and the exposure-held replay do not do; the two custodians,
  the settlement dating, the clock, the share classes and Penrose's suspension stay Layer 1 and decide no main figure.

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
