# task127 design note

Architecture 3, drawn 2026-10-14 at the author's request. Figures marked "about" are the prototype's
(`proto_ye.py`, 1,500 claimant features a quarter, represented claims settling at 0.82 of their former pace
from the cutover); the generator's `figures.json` replaces every one at stage 3.

## Draw

**Card.** task127 v3, registered 2026-10-14, guard PASS (NOTEs only: test.same_puzzle_older and
test.same_driver_older, differentiated against task138 and task446 v2). Actuarial Science & Insurance (client
domain), task type `reserving-development-triangles` (serves Forecasting in the client taxonomy), objective
Forecasting & Predictive Modeling; shape 02; decision `quantity_figure` in dollars, question form how-much; gap
time; pattern none, generators G16 then G14; Gate G forecasting; strategy `forecast_method_backtest` (F6);
Layer 2 family `field_method`; forum the executive team, forcing event the year-end close (`period_close`),
organisation a mutual insurer (`financial_institution`), role the chief financial officer (`finance_controller`),
context artifact the preliminary year-end reserve register; calibration none. People from `guard.py names --geo
"United States" --seed 127`: Brian Robbins (chief actuary, signs the reserving basis), Ricky Evans (claims
systems, signs the conversion notes), Kyle Bean (controller, signs the ledger extract notes); Bradley, Elizabeth,
Sandra, Larry, Stephanie and William drew people.first WARNs and were passed over.

**The author's override.** On 2026-10-14 the author asked for "a full refresh of data, domain, objective
everything and ... a tougher one this time" while architecture 2 (discharge-to-assess packages, Opportunity
Sizing, shipped 59aaaba) was pending review. build-pipeline re-roots in the same objective; the move to
Forecasting is the author's instruction, recorded in `pipeline.json` (`author_override`).

**The world.** Ninebark Mutual Insurance Company, a mutual property and casualty insurer writing private
passenger auto in Iowa, Nebraska and South Dakota (no real insurer carries the name). Bodily injury liability is
counted per claimant feature. Claims ran on an in-house legacy system until the cutover weekend of 29 and 30
June 2024, when the features open at the time were converted to a vendor claims platform; features reported
from 1 July 2024 open on the platform. Since the cutover the represented claims (attorney-represented injuries,
which carry most of the dollars) have settled at about 0.82 of their former pace. Nothing in the pack says so:
the claims and payments show it only as closings and payments arriving later than they used to. Valuation 31
December 2026, Central time; the extracts ran on 6 January 2027; finance has booked a preliminary $295 million
for unpaid bodily injury loss in its year-end close, and the statutory annual statement is due 1 March 2027.

**The decision.** How much to carry for unpaid bodily injury loss at 31 December 2026 against the preliminary
$295 million: a forward quantity (the payments still to come on accidents already incurred), committed in the
year-end close.

**Shape 02 arithmetic.** The unpaid for each accident year 2017 to 2026 (10 criteria) committed as one carried
figure (1), the booked figure and the gap (2), the chart's parts (a bar per accident year, the paid and unpaid
split, the booked total marked: about 5), Ask A's claimant features by accident year (30), Ask B's ledger
quarters (8) and the three files: well over 25, each a separate figure.

**Data-native sentence.** Bodily injury claims pay almost everything at settlement, so this book's paid
development is its claims closing, seen in dollars; the cutover slowed the closing of the represented claims that
carry most of the dollars, and the paid triangle records that as smaller payments at every age in the quarters
since, which a history of development factors reads as smaller ultimates rather than later ones.

**Sources, one line each (what it teaches, how this build differs).**
- Friedland, *Estimating Unpaid Claims Using Basic Techniques* (Casualty Actuarial Society, 2010), chapter 13:
  the Berquist-Sherman adjustment of paid development to the latest diagonal's disposal rates. Here the textbook
  move is the decisive step and nothing shipped names it.
- Berquist and Sherman, "Loss Reserve Adequacy Testing: A Comprehensive, Systematic Approach", Proceedings of the
  CAS (1977): the original adjustment; the restatement here uses ultimate claimant features as its base.
- Actuarial Standard of Practice 43 (property and casualty unpaid claim estimates): the actuary considers
  changes in claim settlement. Not shipped and not needed: the data carries the change.
- `stumping/references/strategies.md` F6 (task46 held: a rate law stationary only in cumulative service
  exposure rebuilt from a movement log): the proven device; here the constructed exposure is the share of
  claimant features closed and the restatement acts on a whole triangle's history, not on each unit's state.
- `stumping/references/client/two-layer-task-design.md` (`field_method`, development triangles): the family.
  The actuarial domain has no rigor patterns of its own; the nearest (payment and claims analytics: complete
  recent claims with lag-triangle factors) is the move this build's default path already makes.
- `guard.py mechanisms --objective forecasting`: no driver on file restates a development history at a
  resolution share; task46 (service exposure), task138 (each unit's own store) and task446 v2 (a base rate backed
  out through error rates) are the nearest and are differentiated on the card.

## Default path

1. Stitch the legacy payment ledger (to 30 June 2024) and the platform's payments (from 1 July 2024): legacy
   dollars and platform cents, US dates and UTC timestamps put on Central dates, voids netted, each payment's
   accident quarter from its feature's accident date.
2. Build the cumulative paid triangle by accident quarter (2017 Q1 to 2026 Q4) at quarter-end ages 1 to 40.
3. Take volume-weighted age-to-age factors over all accident quarters, with no development past 40 quarters
   (the reserving basis).
4. Project each accident quarter's paid to ultimate; the unpaid is ultimate less paid, about $270 million in all.
5. Set it against the $295 million booked: a release of about $25 million.

Ends on: carry $270 million, a release of $25 million against the $295 million booked
Golden: carry $330 million, a strengthening of $35 million

## Stump sentence

The default path develops the stitched quarterly paid triangle with all-quarter volume-weighted factors and
carries $270 million, releasing $25 million of the $295 million booked; the step that lands it there is carrying
the history's development factors onto accident quarters whose represented claims have settled more slowly since
the July 2024 platform cutover, so the recent quarters have paid less of their ultimate at every age than the
history did, and only restating the history at the closure ratios the latest diagonal shows gives $330 million, a
$35 million strengthening.

## Three rules

Task type: reserving-development-triangles (Actuarial Science & Insurance), which serves Forecasting in the client taxonomy.
Domain test: The deciding quantity is unpaid loss estimated from a development triangle, the reserving actuary's core forecast, and what decides it is the field's own response to a change in settlement speed, Berquist and Sherman's restatement of paid development at the current disposal rate.
Swap: "How much should the utility carry for unbilled energy at year end" keeps "unpaid" and "development" but loses the claim that closes, the closure ratio a history is restated at and the reserve that is booked, so the restatement has nothing to act on and the task no longer reads the same.
Layer 1: Two claims systems for one book (the legacy ledger and archive in US dates and dollars, the platform in UTC timestamps and cents, joined through a legacy reference), converted features closed in the legacy archive with a conversion code, extracts run six days after the valuation date, voided and reissued checks, features opened in error and closed as duplicates, and a ledger booking a nightly payment feed and a monthly wire journal by posting date; each is what these systems produce and none is placed to be caught.
Layer 2: field_method, the development triangle done right: the paid history is restated at the latest diagonal's closure ratios before factors are taken, because settlement slowed inside the record.
Decisive step: Restating the paid development history at the share of ultimate claimant features closed that the latest diagonal shows at each age (the Berquist-Sherman paid adjustment), then taking volume-weighted factors from the restated triangle.
Not semantics: Every field read correctly (dates, clocks, units, voids, codes, the conversion) gives the right paid triangle and the right closure counts, and the paid chain ladder on that triangle still carries $270 million.
Not rule application: The reserving basis files the estimand, the grain, the tail and the count unit and no method; no filed rule restates development, so executing every stated rule still files the chain ladder's $270 million.
Analyst test: A strong analyst who reads every field and rule correctly builds the quarterly paid triangle, develops it with all-quarter volume-weighted factors (or the latest diagonals' factors, lower still) and carries $270 million, a $25 million release against the $295 million booked.
Estimand: Unpaid loss on motor bodily injury claimant features from accidents on or before 31 December 2026, reported or not, excluding adjusting expenses, gross of reinsurance, undiscounted, with no development past 40 quarters, valued at 31 December 2026 Central time (ninebark_reserving_basis_2026.pdf, section 2).
No decoy: Nothing is planted: no prior indication, memo, staff draft or certified triangle ships, the booked $295 million is finance's roll-forward with no method stated beside it, and no record is copied, withheld or written to carry the wrong answer.
No certified replay: No certified or published figure exists for a method to reproduce; the method is forced by the closure counts in the claims data.
Lesson: When settlement speed changes, paid development is stationary in the share of claims closed rather than in age, so the analyst measures closure ratios down each diagonal before trusting factors; no build on file restates a development history at a resolution share.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 the latest diagonals' factors | none | no | yes: the recent factors visibly differ, the opponent's first correction | no | no | no | readable |
| R2 frequency-severity | none | the claimant counts and closings are in the files | yes: a standard second method | no | no | no | readable |
| R3 (decisive) the history restated at the latest closure ratios | none: the basis files the estimand, grain, tail and count unit, never settlement, closings or a restatement | close dates exist for every feature, but no column, code or flag marks a settlement speed or the cutover's effect on it | no: the default is the chain ladder, and closure ratios down the diagonals are an expert's diagnostic | no control, prior indication or published figure; the latest year's payments against the chain ladder's expectation read about 0.98, favourable if anything | the battery (keys, duplicates, unmatched joins, voids) never measures settlement speed | a restatement of every historical cell by interpolation and a re-projection, no single ratio | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "unpaid ... losses" | loss only | loss and adjusting expense | same call: the pack carries no expense payment | basis section 2: "excluding adjusting expenses" |
| SF2 | which claims | every bodily injury claimant feature from accidents to 31 December 2026, reported or not | reported features only | same call: unreported features are under 1 per cent of the unpaid (asserted) | basis section 2: "including claims not yet reported" |
| SF3 | gross or net | gross of reinsurance | net of the excess treaty | same call: the pack carries no ceded data | basis section 2 |
| SF4 | discounting | undiscounted | discounted | same call: the pack files no rate | basis section 2 |
| SF5 | the valuation clock | 31 December 2026, Central time | the UTC date of platform timestamps | same call: a few late-evening events move (asserted) | basis section 3 and the platform extract notes (timestamps in UTC) |
| SF6 | development grain | accident quarters at quarter-end ages | accident years at 12-month ages | same call (asserted: the annual restatement also rounds to the golden's ten million) | basis section 3 |
| SF7 | the tail | no development past 40 quarters | a fitted tail factor | same call: every feature settles inside ten years by construction | basis section 3 |
| SF8 | the count unit | claimant features | claims (accidents) | same call: the closure ratios restate the same (asserted) | basis section 3, the archive and register notes |
| SF9 | voids and reissues | net, a void on its own date | gross | same call (asserted) | both ledgers' notes |
| SF10 | "booked" | the register's preliminary year-end bodily injury loss line, $295 million | the loss and expense line, or the September review | same call: the register labels each line | the register's own labels |
| SF11 | converted features in the legacy archive | closed in the archive by the conversion (code CV), alive on the platform | closed claimant features | same call for the main figure (asserted); Ask A turns on it | the archive's code list |
| SF12 | reopened features | open from the reopening until the next closing | closed at the first closing | same call (asserted) | the platform register notes and the events file |
| SF13 | rounding of the carried figure | the indicated unpaid rounded once to the nearest $10 million | a sum of rounded accident years | same call (asserted) | the prompt |

## Ladder

| Rung | Construction | Unpaid (about) | Call | Dies to |
|---|---|---|---|---|
| R0 (default) | stitched quarterly paid triangle, all-quarter volume-weighted factors | $270 million | release $25 million | the closure counts: since the cutover each diagonal has closed a smaller share of its ultimate features at every age from three quarters |
| R1 | the latest four, eight or twelve diagonals' factors | $235 to 280 million | release | the same counts: the latest diagonals mix pre-cutover quarters' slowed tails with post-cutover quarters' slow starts, so their factors carry neither pace |
| R1a | the latest year's payments against the chain ladder's expectation | about 0.98 of expected | release, read as favourable | the same counts: lower payments here mean later closings, not cheaper claims |
| R2 | frequency-severity: open features at the average closed severity, or ultimate features at a severity trended from 2017 to 2019 | $80 million; $220 to 330 million (asserted on the shipped data) | release, or no clear call | the closed features are the quick, small ones; a seven-year extrapolation of a twelve-quarter trend is not a forecast the data supports |
| R3 (decisive) | the history restated at the latest diagonal's closure ratios (closed over ultimate features, linear between evaluations), then volume-weighted factors | $330 million | strengthen $35 million | the golden |

- **Position and margin.** The booked $295 million sits between every rung: R0 and R1 at least 1.08 below it, R3
  at least 1.08 above (planning; asserted on the shipped data with the floor at 1.06).
- **Every correction walks one way.** R1, R1a and R2 each land at or below R0; only the restatement reverses.
- **Convergence of the decisive rung (C1).** Linear or exponential interpolation, closed over ultimate or over
  reported features, quarterly or annual development: every settlement-aware variant rounds to the golden's
  nearest ten million (asserted), so the method is open but the figure is not.
- **Worth.** The decisive rung moves the figure from about $270 million to about $330 million (22 per cent) and
  the call from a release to a strengthening; the accident-year unpaid moves in every year from 2022 on.
- **Grid.** Two binary moves (restate or not; all or latest diagonals): four cells, the restated pair converging
  on the golden and the unrestated pair on R0 and R1, each a named wrong answer below the booked figure.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | bodily injury claimant features from accidents to 31 December 2026, reported or not | filed (basis section 2); C1 on unreported features |
| 2 | Unit of account | the claimant feature for counts, the dollar for the reserve | filed (basis section 3) |
| 3 | Attribution window | accident date to accident quarter and year | the accident date field, a calendar date; C1 at quarter boundaries (asserted) |
| 4 | As-of dating | 31 December 2026, Central time; the extracts ran 6 January 2027 | filed (basis section 3, extract notes); the events file holds the state at the valuation date |
| 5 | Version basis | the payment as issued, a void on its own date | the ledgers' notes; C1 |
| 6 | Denominator | ultimate claimant features under the closure ratio | method-level, C1 across closed over ultimate and closed over reported (asserted) |
| 7 | Weighting | volume-weighted factors over all accident quarters | method-level; the restated triangle's simple and weighted averages round the same (asserted) |
| 8 | Window length | all accident quarters after restatement | C1 against the latest twelve diagonals' restated factors (asserted) |
| 9 | Boundary inclusivity | an event at 23:59 on 31 December is in | C1, asserted on the late-evening events |
| 10 | Rounding path | the indicated unpaid rounded once to $10 million; accident years once to $1 million | filed in the prompt |
| 11 | Tie-break | none: one figure | not applicable, nothing ties |
| 12 | Maturity and censoring | every accident quarter, the latest at one quarter old | the estimand includes them; no tail past 40 quarters (filed) |
| 13 | Order of operations | restate, then take factors, then project the actual latest diagonal | method-level; the golden's steps |
| 14 | Row order | none matters | C1, asserted over a shuffled pack |
| 15 | Duplicate resolution | features opened in error (DUPLICATE) are not claimant features; a reissue replaces its voided check | filed (register notes); C1 on the reserve |
| 16 | Identity normalisation | legacy claim and feature number to the platform's feature through the legacy reference | filed (conversion notes) |
| 17 | Netting against gross | voids net against payments | filed (ledger notes) |
| 18 | Dimensional units | legacy dollars, platform cents, ledger dollars | filed in each file's notes |
| 19 | Code and status semantics | conversion, disposition and status codes | filed code lists; never the stump |
| 20 | Integerisation | none on the reserve; counts are whole features | by construction |
| 21 | Clause scope | the basis applies to motor bodily injury only | filed (basis section 1) |
| 22 | Forward window contents | every payment still to come on incurred accidents | the estimand; no forward driver file needed |

## Literal reader

Executed word for word, the prompt and the reserving basis fix the estimand (unpaid loss on bodily injury
claimant features from accidents to 31 December 2026, reported or not, gross, undiscounted, no development past 40
quarters, Central time) and leave the method open; the data forces it, since every diagonal since the cutover
closes a smaller share of its ultimate features at each age from three quarters than the history did (asserted),
and every settlement-aware variant of the restatement rounds to the golden's carried figure (asserted, C1), while
the unrestated developments land on named wrong answers below the booked figure.

## Oracles

None on the main call: no prior indication, certified triangle, published reserve or consultant's figure ships.
The booked $295 million is a figure with no method beside it, below the golden and above every unrestated rung, so
it confirms nothing on either path. The ledger (Ask B) ties to the claims payments on every basis and carries no
reserve.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each accident year 2017 to 2026, the claimant features closed with a loss payment, closed without one and open at 31 December 2026 | 30 | the audit trail of the claimant counts the reserve stands on, the inventory its unpaid covers | the annual statement's claim count exhibit beside the reserve | D9 split evidence: "closed with a loss payment" is a fact of the two payment ledgers, not of the disposition code; a converted feature's advance sits in the legacy ledger under its legacy claim and feature number while its withdrawn or denied closing is on the platform, and a settled feature whose only check was voided and never reissued closed without one | D1 (legacy features closed before the cutover and reopened after it were re-created on the platform under new ids with the legacy reference, while the archive keeps their closed rows, not coded CV); D2 (the register's status and dates stand at the 6 January run, the events file at any date); D2 (features re-coded from medical payments to bodily injury after the year end were not bodily injury features at it); D8 (UTC timestamps against the Central year end); D5 (features opened in error, filed) | legacy_bi_claims_archive.csv (claim_no, feature_no, accident_date, close_date, disposition), platform_bi_features_2027-01-06.csv (feature_id, legacy_ref, accident_date, coverage, status, closed_at, reopened_at, disposition), platform_feature_events.csv (feature_id, event, event_at, coverage), legacy_bi_payments_2017-2024.csv (claim_no, feature_no, amount, trans_code), platform_bi_payments_2024-2027.csv (feature_id, amount_cents, status, voided_at), legacy_disposition_codes.txt, platform_extract_notes.md; 7 files, 18 columns | by the register's status: every year's open and closed off; union without the legacy reference: 2017 to 2024 up by the re-created features; disposition for payment: closed with and without off in every year; platform payments only: 2019 to 2024 off; the answer | a conversion that keeps the legacy archive whole; a check voided after a settlement fell through; reopenings re-created rather than reopened on a new system |
| B, for each quarter of 2026, how much of the bodily injury loss the ledger booked is payment timing and how much is anything else | 8 | an input reconciled to another system's total, the gap made of devices: the paid losses the reserve rests on tied to the statements | the controller's sign-off that the paid triangle is the books' paid | D4: wire settlements never pass through the nightly check feed; Treasury books each month's wires by one manual journal posted when the bank statement closes, in the first week of the next month, so a quarter's ledger carries the previous quarter's last month of wires and not its own | D1 (the feed re-sent one night's batch under a fresh batch id, reversed by journal in the next quarter); D8 (the feed posts the previous Central day's checks; platform timestamps in UTC); D2 (voids post on the void date); D3 (platform cents, ledger dollars) | gl_bi_paid_loss_2026.csv (posting_date, period, source, batch_id, description, amount), platform_bi_payments_2024-2027.csv (issued_at, method, amount_cents, status, voided_at), ninebark_ledger_extract_notes.md, finance_close_calendar_2026.xlsx (business days); 4 files, 11 columns | next-day feed only: every quarter's timing off by a month of wires, the wires read as other; UTC days: Q1 and Q4 off by the year-end evening checks; the replay read as timing: Q3 and Q4 off; the answer | a Treasury wire journal and a feed replay are what a ledger tie-out normally finds |
| C, the unpaid for each accident year and the chart | 10 and the chart's parts | the construction | the call's own table | none | none | the golden's restatement | R0 to R3 values | the reserving team's own exhibit |

- **Main population zero-counts.** No ask device moves the carried figure or any accident year's unpaid
  (asserted: the call recomputes identically under each device's mishandling: CV rows kept, re-created features
  doubled, the register's status read at the run date, re-coded features counted, UTC clocks); the ledger and its
  notes are read by no step of the call; deleting every ask file leaves the call and Ask C unchanged.
- **Hazard table.** D9 (A) moves closed with and without payment in every year with advances or voided
  settlements; D1 (A) moves 2017 to 2024; D2 (A, run date) moves open and closed in every year with January
  events; D2 (A, re-coding) moves 2025 and 2026 open; D8 moves a few features at the year end; D4 (B) moves every
  quarter's timing and other; D1 (B) moves Q3 and Q4; D8 (B) moves Q1 and Q4.
- **Referee.** None for the primaries; the ledger notes define the feed and the extract notes the clocks, the
  WHAT only; no filed sentence says that wires leave the feed, which features were re-created or which payment
  ledger holds a converted feature's advance.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A closed with a loss payment (10) | the disposition code, read at 31 December from the dated fields, legacy CV rows dropped | advances on withdrawn and denied features and voided settlements misfiled: every year off | miss |
| A closed without one (10) | the same | every year off by the same features | miss |
| A open at 31 December (10) | dated fields, CV dropped, re-created features kept twice and re-coded features counted | 2017 to 2024 off by the re-creations, 2025 and 2026 off by the re-codings | miss |
| B timing (4) | the nightly feed's next-day posting on Central days | every quarter off by a month of wires | miss |
| B anything else (4) | the ledger less the feed-timed payments | the wire journals read as other: every quarter off | miss |
| C unpaid by accident year (10) and the chart | the golden's restatement | right | outside |

Mirror leakage: 0 per cent of the device asks beyond what the cracker keeps (the asks never read the reserve), and
the chain-ladder mirror keeps none of Ask C and none of the chart's unpaid segments; on the device asks it does
what the cracker does.
Pair ceiling: 40 (the cracker about 58 with the call, Ask C and the chart; the chain-ladder mirror about 21).

## Tried and rejected


- The note's decisive rung, per feeder the smaller of expected buyers and hosting slots: a stated connection standard, a per-feeder hosting map and a neighbourhood-to-feeder join whose keys line up hand it to any solver who reads them, its driver sits nearest task106's, and as labelled it BLOCKs on ban.pattern C (task119), ban.calibration pilot_log (task122) and test.same_driver_older (a signature spent in nine builds); kept as rung 2.
- Resistance-to-heat-pump netting (each resistance conversion frees feeder headroom for oil or propane conversions): the connection standard either states a per-heat-pump assessment, which contradicts the netting and is a counter-pin, or states a net-change rule, which hands it over; a corpus of past approvals would refute the stop rung, which L1 forbids.
- Heat pumps per home (large ducted homes taking two outdoor units, so two feeder draws per slot): visible at heat-pump grain in any connection or rebate record, and found by any solver who counts rebates per buyer; moves only the saturated feeders, too little to change a leader.
- Survey staleness (homes converted since fieldwork leave the pool): a dated register keyed on neighbourhood is a schema-visible pool deduction a careful solver makes unprompted.
- Competing claims on feeder headroom (the utility's deferred queue, committed loads, a state income-qualified programme): each needs a first-come-first-served clause the solver executes, and the effect sits only on saturated feeders.
- Seasonal against winter hosting capacity on summer-peaking feeders: needs a filed "winter" assessment that sends the solver straight to the feeder load history.
- A feeder map naming each neighbourhood's primary feeder while boundary streets sit on the next one: reads as a coarse instrument (sole_data_defect yes under the instrument repair), and a solver who reads "primary" looks for the street-level join.
- The expected minimum against the minimum of the expectation at feeders where buyers and slots balance: under 10 per cent on any feeder and inside the nearest ten on co-op totals.
- The year-end lapse on Year 1's lag alone (late autumn purchases missing 31 December): a stated deadline the solver replays at the finest grain on offer; kept as the check that passes at rung 2.
- A utility service-upgrade queue for old 100 A homes as the decisive rung: the upgrade requirement has to be stated for determinism, which sends the solver to upgrade lead times, and old homes sit mostly on saturated feeders, where the feeder cap already binds.
- Relabelling the note's pilot log as realised_outcome_roster to clear ban.calibration: a relabel that does not name the decisive move, so the organ itself was redrawn as Year 1's install book.
- A Nova Scotia setting with a fictional utility (oil and electric heat): the province's distribution is one large utility, so a co-op that sets its own heat-pump rate meters reads as invented; moved to Minnesota co-op territory.
- A field operations voice saying the 2025 meter-exchange backlog is behind us: true, but it names the backlog and sends a reader to the weeks the crews ran at their ceiling; dropped.
- A filed field-procedure line on the order of work (standing orders first, then orders in date order): read beside the programme's volume it gives a solver a reason to ask whether the crews keep up; the order is to be pinned by the 2025 record instead, and the line stays out unless the determinism check needs it.
- Keeping one co-op as the requester at registration, relabelled cooperative_or_member_body to clear ban.org_family: the key is honest for a member-owned co-op, but two United States power-company allocation builds would then sit side by side with task124, the calibration and artifact bans would still need redrawing, and the business-operations-analytics x opportunity-sizing-decision pairing would still block task128; the requester moved to the fund instead.
- The draw's per-co-op ask figures (meters still unset on 31 December, qualifying buyers the feeders turn away) and its chart parts (the stacked series, the year-end queue annotated): each names rung 3 or rung 4 in the prompt, which outranks every file, so a solver is told the queue and the feeder cap exist before opening anything; replaced by two device-carried pilot audits and a 2027-against-2026 chart.
- Spare capacity of about six sets a week at Lakes: the autumn queue bites harder, but each crew's annual spare (about 300) then falls below Lakes' 420 placeable meters, so a crude annual check hands Riverbend the lead without the queue; spare set back to about ten (annual about 500).
- Lakes and Uplands crews on a Monday-to-Friday week: the 2027 Friday holidays (Christmas observed 24 December, New Year observed 31 December) and Thanksgiving Friday open a holiday-handling fork worth up to a full ten on Lakes' slots; moved both crews to four ten-hour days, Monday to Thursday, with the 2026 record showing they worked the Thursdays before Friday holidays.
- Grading the year's rebated installs as the unrounded co-op sets rounded once to the nearest ten: the two binding co-ops' convention spreads (about 5 and 3.5 sets) add across a ten on the total; the graded total is the sum of the co-ops' slots, with the unallocated figure its complement.
- A spring queue left to run continuously into the autumn at the binding crews: year-end sets then depend on the spring start week and every holiday from Memorial Day on, a spread of more than ten; spring volumes sized so both crews clear by August.
- Pilot spring shares that differ by neighbourhood: per-co-op and pooled readings of the forward calendar then differ by 4.2 sets a point at Lakes; set to exactly 25 per cent in every pilot neighbourhood.
- A 2027 slot-release rule (a quarter of each co-op's slots in the spring window): it makes arrivals depend on the allocation itself and its fixed point (Lakes about 183) disagrees with the one-pass queue (about 240), a fork created by a filed sentence; no release rule, so both readings give 240.
- A per-co-op ask on the pilot's days from claim to payment: a staffing decision that the split never reads, so it fails H18; re-cut to the rebate dollars paid in 2026 and the installs they cover, the audit trail of the pilot the rates are built on.
- A pilot close-out stating the total rebates paid: an oracle that verifies ask B's handling for free; the pack states no paid, cost or cleared total.
- Field-order volumes at the draw's 70,000 rows: six crews' standing work over 104 weeks is about 31,000 orders at realistic crew sizes, and padding the file to 70,000 would need order types nothing reads; 31,000 clears the gate.
- Ask B's clock device on the 31 December 2026 evening payment run: the pack's as-of date is 11 December and the trustees meet on 17 December, so no December run exists to cross the year; the cutoff moved to the fund's November month end (the 30 November run clears on 1 December UTC) and the prompt asks for rebate dollars paid through the end of November.
- Anthony Bentley as the outreach director: the name is not in the seed-127 draw (`guard.py names --geo "United States, Minnesota" --seed 127 --n 200`); Anne Garcia from the draw then took BLOCK people.first against task125; Sara Duncan from the same draw is clear.
- The outreach director's belief that Uplands has more propane and electric homes than any other co-op: Table H1 puts Valley first on propane and electricity, so the belief would be a stakeholder read the pack refutes; reworded to more qualifying homes, which the survey's joint counts make true (rung 1's leader).
- The rung 3 twins with each neighbourhood's buyers split across two feeders: the map puts each neighbourhood on exactly one feeder, so Elm Park and Birch Hollow are identical on the survey and sit on a full and a roomy feeder respectively.
- A Lakes ceiling cycle averaging 10.45 a day over twenty days: the plateau's 50 days start mid-cycle and recover 10.57, which moves Lakes across a ten; the ceiling is a four-day 11, 10, 11, 10 pattern (42 a week) and standing work a twenty-day block averaging 8.05, so spare is 2.44 a day in any window.
- Pilot install rates with neighbourhood-level noise: rates by system and income band, or each co-op's own pilot rates, would each give a different forward figure (H14); every pilot neighbourhood is built from unit blocks (38 ducted-propane households to 3 installs, 32 electric to 1, 95 hydronic to 1), so every finer grain returns the system rates exactly.
- Pilot purchase dates spread evenly with a random installer lead time: autumn installs clustered to six orders a week at Uplands (0.86 of its spare); installs are spread evenly over each season's install span instead, peak four a week at Lakes and three at Uplands.
- The rebate amount as a pilot-log column: it would let a per-rebate reconciliation of the ledger find every returned payment for free; the amounts live in Schedule B of the participation terms instead (still a reconciliation route, recorded as HZ2's leakage).
- The rules file named `clean_heat_programme_rules_2027.pdf` after the fund: leak.py's file-name sweep reads `clean_` as the author's cleaned-data noun (LEAK); renamed `heat_pump_programme_rules_2027.pdf` in the generator.
- A "Decision sought" closing section and totals for expected installs, feeder room and meter sets in the note's line-by-line table: the section restated the split on an orphaned page, and a meter-set total of 1,174 beside 1,170 placed is a second statement of the year's installs by another rounding path (H3); both cut.
- 2026-10-10: the crew meter-set queue as decisive rung under a hosting-slot cap; the determinism judge returned SEND_BACK and the build was retired, not submitted.
- 2026-10-12, re-root (architecture 2): the author re-queued the number in wave 1 as "re-root, Opportunity Sizing". Candidates weighed at the draw and rejected: a charged-off card portfolio's sale against keeping it (the warehouse's payers are a visible attribute every solver conditions on, and the composition-mix strategy is banned against task501); a diabetic eye screening van placed by first-round against repeat-round yield (the prevalence-round effect is textbook to a strong solver); acoustic leak-detection crews placed by main material (material is a GIS column the reflex stratifies on, and a conditioned yield transferred across mixes is composition mix); a health plan's navigations split by procedure group where members follow their surgeon (the payment-claims task type serves ETL and Anomaly Detection, not Opportunity Sizing); an overdraft fee cap's revenue at risk sequenced after the banks' own changes (lending sits outside Economics in the client taxonomy, and no banking task type serving Opportunity Sizing fits a rule's revenue impact).
- 2026-10-12, architecture 2 at stage 2: a brokerage "package available from" date beside the start date (care ready before the patient left): it shows the care wait apart from the delay for every patient held by equipment, so a solver reconciling the two sees a third of Ashby Vale's patients leaving days after their care was ready and goes looking; the brokerage records care starting on the day the patient went home, and the restart patients carry the counterfactual instead.
- Restart patients needing discharge equipment at the same rate as new-package patients: subtracting their average nights (the control reflex) filed the golden split exactly; restart patients mostly have their equipment at home already (0.15 of the rate), and the control now files Ashby Vale first.
- Wendlebury's equipment need at 0.27 of covered patients: counting equipment patients at nought (R2) then filed the golden split; at 0.62, with the North depot's quick deliveries, R2 fills Cleeve Park and leaves Wendlebury short while the golden barely moves.
- The national weekly return by site: its nights per discharge rank the hospitals on the delay, an artifact on rung 0; it ships by trust, a distractor.
- A boundary change moving two wards from Ashby to Marchford district in April 2026 as an Ask B device: the ask's "district" would read two ways (as then or as now); the districts are stable and the county-line postcode district carries the district hazard.
- The winter's delayed bed-days total in the chart's title: within-trust moves leave the five-hospital total unchanged, so the cracker banks it; the title states what the chart shows, and the ask adds each hospital's delayed patients.
- Re-brokered and re-sent referrals as Ask B devices: whether a re-sent referral is a second referral the brokerage took reads two ways; cut.
- The part-filled hospital's bed-days at 967.45: rounding the value to two places first gives 968; the clearance brings one Cleeve Park delivery forward a day, so 968.23 rounds to 968 on every path.
- 2026-10-14, second-layer attempt after shipping (built to stage 4, not shipped): the patients the wait for home care itself sent to a rehabilitation bed or a care home (re-assessed while waiting, so the warehouse records them on pathway 2 or 3 and the default cohort conditions on the wait's own outcome), found from the brokerage's withdrawn hospital referrals, with the note's section 3 moved to "medically optimised for discharge home on pathway 1". Every free gate was green (27,838 checks, the verifier, a byte-identical rebuild, precut, leak.py), but the judge returned NOT_DETERMINISTIC and SEND_BACK on that pack (determinism_check_report_loop1.md, which covers the rejected prototype and not the shipped pack): no shipped sentence says a withdrawn hospital referral marks a patient optimised for home, and that reading alone moves Ashby Vale from 10 packages to none. Filing the population as "whatever pathway they left on" would hand over the post-treatment insight and leave only a record linkage a solver executes once told, so the call would turn on a filed rule; the leak reader also opened a fork on the package's "up to four weeks" (the re-assessed patients waited 23 to 26 nights on average). Reverted to the shipped pack, which the generator rebuilds byte-identical (27,095 checks); the shipped build's longest saving is 14 nights, so the four-week fork does not reach it.
- 2026-10-14, re-root (architecture 3) at the author's request: architecture 2 (discharge-to-assess packages, shipped 59aaaba, pending review) replaced by a full refresh of data, domain and objective; drawn instead: a motor bodily injury reserve under Forecasting.
- A settlement speed-up after the cutover instead of a slowdown: the paid chain ladder overstates while frequency-severity on closed claims understates, so the reflexes walk both ways and no booked figure separates them from the restatement.
- A quarter of each claim paid in instalments over its life, with severity tied to settlement time at power 0.9: the restatement's variants fell 6 to 15 per cent below the simulated truth and 2 to 4 per cent apart; bodily injury pays at settlement (the claimant's own medical cover carries the bills), so the build pays at closing with a few advances.
- Restating each handling unit's triangle on its own (represented claims alone): that triangle's early paid is a handful of advances, its restated early factors explode and the indication nearly doubles; no handling-unit column ships, and the restatement runs on the whole line, where every variant converges.
- Annual development at 12-month ages: the linear and exponential restatements 4 per cent apart and closed over reported against closed over ultimate 6 per cent apart; the basis files accident quarters at quarter-end ages, where the variants converge.
- Frequency-severity with severity trended from the mature quarters as a converging second method: a twelve-quarter trend carried seven years swings 0.6 to 1.4 of the restated indication across seeds; it is a rung (R2), asserted on the shipped data, never the golden.
- Report lags with a long tail (2 per cent of features reported after six months): the two count bases of the restatement drift 4 to 5 per cent apart; lags now average five days with a thin tail, so both bases converge.
