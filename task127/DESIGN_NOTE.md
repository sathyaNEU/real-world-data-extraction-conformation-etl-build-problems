# task127 design note

Architecture 3, drawn 2026-10-14 at the author's request. Every figure below is the generator's
(`generator/figures.json`, asserted in `generator/checks.py` and recomputed by `generator/verify.py`).

## Stage 3 build

- `python3 task127/generator/build.py`: the pack (15 files), the goldens, `metadata.json` and `figures.json`; 219
  checks; the independent verifier (target/ only) recomputes the carried $400 million, the 20 count cells and the 8
  ledger cells; two builds byte-identical; `target.zip` cut from the final build.
- Gates: `figures_check.py` PASS (69 figures); `voice-check.py` PASS; `leak.py` REVIEW, no LEAK (two lines, read in
  `leak_check_report.md`); `guard.py heart` WARN (repeat.question_form against task453 v2, answered under Draw);
  `guard.py surface` promotes task125, task138 and task446 on card axes only (gap time and quantity_figure; G16 with
  task138 and task446), each differentiated on the card and put to the author-requested adjudicated clone check.

## Draw

**Card.** task127 v3, registered 2026-10-14, guard PASS at the draw (NOTEs only: test.same_puzzle_older and
test.same_driver_older, differentiated against task138 and task446 v2). Actuarial Science & Insurance (client
domain), task type `reserving-development-triangles` (serves Forecasting in the client taxonomy), objective
Forecasting & Predictive Modeling; shape 14 (the asks' cuts per accident year and per quarter carry the criteria;
drawn as 02 and moved when the accident-year unpaid left the graded set, see Tried and rejected); decision
`quantity_figure` in dollars, question form how-much; gap time; pattern none, generators G16 then G14; Gate G
forecasting; strategy `forecast_method_backtest` (F6); Layer 2 family `field_method`; forum the executive team,
forcing event the year-end close (`period_close`), organisation a mutual insurer (`financial_institution`), role the
chief financial officer (`finance_controller`), context artifact the preliminary year-end reserve register;
calibration none. People from `guard.py names --geo "United States" --seed 127`: Brian Robbins (chief actuary, signs
the reserving basis), Ricky Evans (claims systems, signs the platform and conversion notes), Kyle Bean (controller,
signs the ledger notes and the register); Bradley, Elizabeth, Sandra, Larry, Stephanie and William drew
people.first WARNs and were passed over. The heart's repeat.question_form WARN (how-much beside task453 v2, drawn
after this card) is answered by the decision: an amount to book asks how much.

**The author's override.** On 2026-10-14 the author asked for "a full refresh of data, domain, objective
everything and ... a tougher one this time" while architecture 2 (discharge-to-assess packages, Opportunity
Sizing, shipped 59aaaba) was pending review. build-pipeline re-roots in the same objective; the move to
Forecasting is the author's instruction, recorded in `pipeline.json` (`author_override`).

**The world.** Ninebark Mutual Insurance Company, a mutual property and casualty insurer writing private
passenger auto in Iowa, Nebraska and South Dakota (no real insurer carries the name). Bodily injury liability is
counted per claimant feature; an accident carries one to three. Claims ran on an in-house legacy system until the
conversion weekend of 29 and 30 June 2024, when the features open at the time moved to a vendor claims platform;
features reported from 1 July 2024 open there. Since the platform went live the represented claims (the
attorney-represented injuries that carry most of the dollars) have settled at 0.75 of their former pace. Nothing in
the pack says so: the claims and payments show it only as closings and payments arriving later than they used to.
Valuation 31 December 2026, Central time; the extracts ran at 06:10 on 6 January 2027; finance's register carries a
preliminary $344.6 million for bodily injury loss.

**The decision.** How much to carry for unpaid bodily injury loss at 31 December 2026 against the preliminary
$344.6 million: a forward quantity (the payments still to come on accidents already incurred), committed in the
year-end close.

**Shape arithmetic.** The carried figure, the booked figure and the gap (3), the closure evidence and the paid to
date (3), Ask A's claimant features closed with and without a loss payment for each accident year 2017 to 2026
(20), Ask B's two figures for each quarter of 2026 (8), the chart's parts (about 4) and the three files: over 35
criteria, each a separate figure or part.

**Data-native sentence.** Bodily injury claims pay almost everything at settlement, so this book's paid
development is its claims closing, seen in dollars; the platform slowed the closing of the represented claims that
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

1. Stitch the legacy payment ledger (to 28 June 2024) and the platform's payments (from 1 July 2024): legacy
   dollars and platform cents, US dates and UTC timestamps put on Central dates, voids netted on their own dates,
   each payment on its feature's accident quarter.
2. Build the cumulative paid triangle by accident quarter (2017 Q1 to 2026 Q4) at quarter-end ages 1 to 40.
3. Take volume-weighted age-to-age factors over all accident quarters, with no development past 40 quarters
   (the reserving basis).
4. Project each accident quarter's paid to ultimate: $316.8 million unpaid in all.
5. Round to the nearest $25 million and set it against the $344.6 million booked: carry $325 million, a release.

Ends on: carry $325 million (the chain ladder's $316.8 million), a release of $19.6 million against the $344.6 million booked
Golden: carry $400 million (the restated development's $399.8 million), a strengthening of $55.4 million

## Stump sentence

The default path develops the stitched quarterly paid triangle with all-quarter volume-weighted factors to $316.8
million and would carry $325 million, a release of $19.6 million against the $344.6 million booked; the step that
lands it there is carrying the history's development factors onto accident quarters whose represented claims have
settled more slowly since the platform went live in July 2024, so the recent quarters have paid less of their
ultimate at every age than the history did, and only restating the history at the closed shares the latest
diagonal shows gives $399.8 million and a carried $400 million, a strengthening of $55.4 million.

## Three rules

Task type: reserving-development-triangles (Actuarial Science & Insurance), which serves Forecasting in the client taxonomy.
Domain test: The deciding quantity is unpaid loss estimated from a development triangle, the reserving actuary's core forecast, and what decides it is the field's own response to a change in settlement speed, Berquist and Sherman's restatement of paid development at the current disposal rate.
Swap: "How much should the utility carry for unbilled energy at year end" keeps "unpaid" and "development" but loses the claim that closes, the closure ratio a history is restated at and the reserve that is booked, so the restatement has nothing to act on and the task no longer reads the same.
Layer 1: Two claims systems for one book (the legacy ledger and archive in US dates and dollars, the platform in UTC timestamps and cents, joined through a legacy reference), converted features closed in the legacy archive with a conversion code, legacy features reopened after the conversion and re-entered on the platform, extracts run six days after the valuation date, voided, reissued and returned checks, features opened in error (some carrying a payment) and a ledger booking a nightly check feed, monthly Treasury wire journals by bank value date and Finance's journals; each is what these systems produce and none is placed to be caught.
Layer 2: field_method, the development triangle done right: the paid history is restated at the latest diagonal's closed shares before factors are taken, because settlement slowed inside the record.
Decisive step: Restating the paid development history at the share of ultimate claimant features closed that the latest diagonal shows at each age (the Berquist-Sherman paid adjustment), then taking volume-weighted factors from the restated triangle.
Not semantics: Every field read correctly (dates, clocks, units, voids, codes, the conversion) gives the right paid triangle and the right closure counts, and the paid chain ladder on that triangle still gives $316.8 million and carries $325 million.
Not rule application: The reserving basis files the estimand, the grain, the tail and the count unit and leaves the method to the actuary; no filed rule restates development, so executing every stated rule still files the chain ladder's $325 million.
Analyst test: A strong analyst who reads every field and rule correctly builds the quarterly paid triangle, develops it with all-quarter volume-weighted factors (or the latest diagonals' factors, lower still) and would carry $325 million, a $19.6 million release against the $344.6 million booked (executed on the clean truth in checks.py).
Estimand: Unpaid loss on motor bodily injury claimant features from accidents on or before 31 December 2026, reported or not, excluding adjusting expenses, gross of reinsurance, undiscounted, with no development past 40 quarters, valued at 31 December 2026 Central time (ninebark_reserving_basis_2026.pdf, sections 2 and 3).
No decoy: Nothing is planted: no prior indication, memo, staff draft or certified triangle ships, the booked $344.6 million is finance's roll-forward with no method beside it, and no record is copied, withheld or written to carry the wrong answer.
No certified replay: No certified or published figure exists for a method to reproduce; the method is forced by the closure counts in the claims data.
Lesson: When settlement speed changes, paid development is stationary in the share of claims closed rather than in age, so the analyst measures closed shares down each diagonal before trusting factors; no build on file restates a development history at a resolution share.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 the latest diagonals' factors | none | no | yes: the recent factors visibly differ, the opponent's first correction | no | no | no | readable |
| R2 frequency-severity | none | claimant counts and closings are in the files | yes: a standard second method | no | no | no | readable |
| R3 (decisive) the history restated at the latest closed shares | none: the basis files the estimand, grain, tail and count unit and leaves methods to the actuary; nothing names settlement speed, closings by age or a restatement | close dates exist for every feature, but no column, code or flag marks a settlement speed, a handling unit or the platform's effect | no: the default is the chain ladder, and closed shares down the diagonals are an expert's diagnostic | no control, prior indication or published figure; the latest year's payments come in at 0.968 of the chain ladder's expectation, read as favourable | the battery (keys, duplicates, unmatched joins, voids) never measures settlement speed | a restatement of every historical cell by interpolation and a re-projection, no single ratio | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "unpaid ... losses" | loss only | loss and adjusting expense | same call: the pack carries no expense payment (asserted) | basis 2.2: "excludes adjusting expenses" |
| SF2 | which claims | every bodily injury claimant feature from accidents to 31 December 2026, reported or not | reported features only | same call: unreported features carry under 1 per cent of the unpaid (asserted) | basis 2.1: "including claims not yet reported" |
| SF3 | gross or net | gross of reinsurance | net | same call: the pack carries no ceded data (asserted) | basis 2.2 |
| SF4 | discounting | undiscounted | discounted | same call: the pack files no rate (asserted) | basis 2.2 |
| SF5 | the valuation clock | 31 December 2026, Central time | platform timestamps read on their UTC dates | same call: carries $400 million (asserted) | basis 3.4 and the platform notes (timestamps in UTC) |
| SF6 | development grain | accident quarters at quarter-end ages | accident years at 12-month ages | the annual restatement lands at $387.5 million, on the $25 million edge | basis 3.2: development is measured at quarter ends |
| SF7 | the tail | no development past 40 quarters | a fitted tail factor | same call: every feature settles by age 40 (asserted) | basis 3.5 |
| SF8 | the count unit | claimant features | claims (accidents) | same call: carries $400 million (asserted) | basis 3.1 |
| SF9 | voids | net, each void on its own date | gross | same call: carries $400 million (asserted) | basis 3.3 |
| SF10 | "booked" | the register's preliminary bodily injury loss line, $344.6 million | the defence or adjusting lines | the register labels each line (asserted) | the register's labels |
| SF11 | converted features in the legacy archive | closed in the archive by the conversion (CV), alive on the platform | closed claimant features | the closings at 29 June 2024 would move the restatement | the code list ("feature continues on platform") and the conversion notes |
| SF12 | reopened features | open from a reopening until the next closing | closed from the latest closing alone | same call: carries $400 million (asserted) | the platform notes and the events file |
| SF13 | rounding of the carried figure | the indicated unpaid rounded once to the nearest $25 million | the accident quarters' rounded figures summed | same call (asserted) | the prompt |

## Ladder

| Rung | Construction | Unpaid | Carried | Dies to |
|---|---|---|---|---|
| R0 (default) | stitched quarterly paid triangle, all-quarter volume-weighted factors | $316.8 million | $325 million, a $19.6 million release | the closure counts: since the platform went live each diagonal has closed a smaller share of its ultimate features at every age from seven quarters (asserted at each age 7 to 23) |
| R1 | the latest 4, 8 or 12 diagonals' factors | $314.1, $283.6 and $289.3 million | $300 to $325 million, a release | the same counts: the latest diagonals mix older quarters' slowed tails with newer quarters' slow starts and carry neither pace |
| R1a | the latest year's payments against the chain ladder's expectation | 0.968 of expected | a release, read as favourable | the same counts: lower payments mean later closings, not cheaper claims |
| R2 | frequency-severity: open features at the average closed severity, or ultimate features at a severity trended from 2017 to 2019 | $96.9 million; $356.5 million | $100 million; $350 million | the closed features are the quick, small ones; a twelve-quarter severity trend (4.1 per cent a year) carried seven years |
| R3 (decisive) | the history restated at the latest diagonal's closed share of ultimate features for each age (linear between quarter ends), volume-weighted factors from the restated triangle | $399.8 million | $400 million, a $55.4 million strengthening | the golden |

- **Position and margin.** The booked $344.6 million sits 1.088 above the chain ladder and 1.098 above the best
  latest-diagonal reading; every restated variant sits at least 1.151 above it (asserted at 1.06).
- **Every correction walks one way.** R1 and R1a land at or below R0; R2's trended reading lands short of the
  golden's carried figure by $50 million; only the restatement reaches it.
- **Convergence of the decisive rung (C1).** Linear or exponential interpolation, closed over ultimate or over
  reported features, volume-weighted or simple factors, all quarters or the latest twelve diagonals after
  restatement: $396.5 million to $404.9 million, all carried at $400 million (asserted; the golden $11.6 million
  from the nearest $25 million edge).
- **The evidence is in the counts.** Closed share of ultimate features at eight quarters 74.4 per cent across the
  2018 to 2020 accident quarters against 71.9 per cent for 2025 Q1; at twelve quarters 84.7 against 80.6 per cent
  for 2024 Q1; post-cutover means below the history at every age from 7 to 23, most post-cutover cells below the
  history's lowest (asserted).
- **Clean truth.** On the world's own records (no Layer 1) the chain ladder still files a release and the
  restatement still carries $400 million; the book's true unpaid is a strengthening and sits nearer the golden
  than the chain ladder (asserted).
- **Grid.** Two binary moves (restate or not; all or latest diagonals): the restated pair converges on the golden,
  the unrestated pair on R0 and R1, each a named release below the booked figure.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | bodily injury claimant features from accidents to 31 December 2026, reported or not | filed (basis 2.1); C1 on unreported features |
| 2 | Unit of account | the claimant feature for counts, the dollar for the reserve | filed (basis 3.1); C1 on claims (SF8) |
| 3 | Attribution window | accident date to accident quarter and year | the accident date field, a calendar date |
| 4 | As-of dating | 31 December 2026, Central time; the extracts ran 6 January 2027 | filed (basis 3.4, platform notes); the events file holds the state at the valuation date |
| 5 | Version basis | the payment as issued, a void on its own date | filed (basis 3.3, both ledgers' notes); C1 (SF9) |
| 6 | Denominator | ultimate claimant features under the closed share | method-level, C1 across closed over ultimate and closed over reported (asserted) |
| 7 | Weighting | volume-weighted factors over all accident quarters | method-level; simple averages carry the same (asserted) |
| 8 | Window length | all accident quarters after restatement | C1 against the latest twelve diagonals' restated factors (asserted) |
| 9 | Boundary inclusivity | an event at 23:59 on 31 December is in | C1, asserted on the UTC reading (SF5) |
| 10 | Rounding path | the indicated unpaid rounded once to $25 million; ledger amounts to the cent | filed in the prompt; C1 on summed quarters (SF13) |
| 11 | Tie-break | none: one figure | not applicable, nothing ties |
| 12 | Maturity and censoring | every accident quarter, the latest at one quarter old | the estimand includes them; no tail past 40 quarters (filed) |
| 13 | Order of operations | restate, then take factors, then project the actual latest diagonal | method-level; the golden's steps |
| 14 | Row order | none matters | C1: every computation groups and sums |
| 15 | Duplicate resolution | features opened in error (DUPLICATE, XD) are not claimant features; a reissue replaces its voided check | filed (platform notes, code list); C1 on the reserve (asserted) |
| 16 | Identity normalisation | legacy claim and feature number to the platform's feature through the legacy reference | filed (conversion notes, platform notes) |
| 17 | Netting against gross | voids net against payments | filed (basis 3.3) |
| 18 | Dimensional units | legacy dollars, platform cents, ledger dollars, register thousands | filed in each file's notes and headers |
| 19 | Code and status semantics | conversion, disposition and status codes | filed code lists; never the stump |
| 20 | Integerisation | none on the reserve; counts are whole features | by construction |
| 21 | Clause scope | the basis applies to motor bodily injury only | filed (basis 1.1) |
| 22 | Forward window contents | every payment still to come on incurred accidents | the estimand; no forward driver file needed |

## Literal reader

Executed word for word, the prompt and the reserving basis fix the estimand (unpaid loss on bodily injury
claimant features from accidents to 31 December 2026, reported or not, gross, undiscounted, quarter-end development
to age 40, Central time) and leave the method to the actuary; the data forces it, since the diagonals since the
platform went live close a smaller share of their ultimate features at every age from seven quarters (asserted),
and every settlement-aware variant of the restatement carries the golden's $400 million (asserted, C1), while the
unrestated developments land on named releases below the booked figure.

## Oracles

None on the main call: no prior indication, certified triangle, published reserve or consultant's figure ships.
The booked $344.6 million is a figure with no method beside it, below the golden and above every unrestated rung, so
it confirms nothing on either path. The ledger (Ask B) ties to the claims payments on every basis and carries no
reserve; the earned car-years and the property damage triangle (distractors) bear on neither.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each accident year 2017 to 2026, the claimant features closed at 31 December with a loss payment and those closed without one | 20 | the audit trail of the claimant counts the reserve stands on | the annual statement's claim count exhibit beside the reserve | D9 split evidence: a loss payment is a fact of the two payment ledgers, not of the disposition code; a converted feature's advance sits in the legacy ledger under its legacy number, a withdrawn or denied feature may have been paid an advance, a settled feature may have been settled on the vehicle claim, and a settlement may sit on the claim's duplicate feature (legacy XD or platform DUPLICATE) | D1 (legacy features closed before the conversion and reopened after it were re-entered on the platform under new numbers with the legacy reference, while the archive keeps their closed rows, not coded CV); D2 (checks returned in the first week of January voided after the valuation); D2 (the register's status at the 6 January run); D8 (UTC timestamps against the Central year end); D5 (features opened in error, filed) | legacy_bi_claims_archive.csv (CLM_NO, FEAT_NO, LOSS_DT, RPT_DT, CLS_DT, DISP), platform_bi_features_2027-01-06.csv (feature_id, claim_number, legacy_ref, accident_date, reported_date, disposition), platform_feature_events_2027-01-06.csv (feature_id, event, event_at), legacy_bi_payments_2017-2024.csv (CLM_NO, FEAT_NO, TRANS_CD, AMOUNT), platform_bi_payments_2024-2027.csv (feature_id, amount_cents, status, voided_at), legacy_disposition_codes.txt, claims_conversion_notes_2024.md, platform_extract_notes.md; 8 files, 20 columns | the disposition read as the payment: every year off; one ledger per system: 2017 to 2024 off; every voided check netted: 2023 to 2026 off; re-entered features counted twice: 2017 to 2024 off; duplicates' payments dropped: every year off; the answer | a conversion that keeps the legacy archive whole; old claims reopened over a lien; a check returned at year end; a settlement keyed to a duplicate feature |
| B, for each quarter of 2026, how much of the bodily injury loss the ledger booked was claims payments issued in an earlier quarter and how much was not claims payments at all | 8 | an input reconciled to another system's total, the gap made of devices: the paid losses the reserve rests on tied to the statements | the controller's sign-off that the paid triangle is the books' paid | D4: wire settlements never pass through the nightly check feed; Treasury books each month's wires by bank value date (a wire released after 15:00 values the next business day) in one journal per state early in the next month, so a quarter's last-day late wires sit in the next quarter's second journal | D1 (the feed re-sent the 13 August batch on 15 August beside a genuine catch-up pair after the 19 May outage, reversed in October); D2 (a December 2025 vehicle-damage wire inside Treasury's journal, reclassed in April); D2 (two feed lines rejected for a missing state segment and reposted by Finance's manual journal: claims payments under the MANUAL source); D8 (the feed posts the previous Central day's checks; platform timestamps in UTC); D3 (platform cents, ledger dollars) | gl_5311_bi_paid_loss_2026.csv (posting_date, source, batch_ref, state, description, amount), platform_bi_payments_2024-2027.csv (issued_at, method, amount_cents, status, voided_at), platform_bi_features_2027-01-06.csv (state), ledger_extract_notes_2026.md, finance_close_calendar_2026.xlsx (business days); 5 files, 12 columns | each Treasury journal as the previous month's wires and every manual line as other: all 8 off; wires by issue month: every quarter's earlier off; the repeat read as payments: Q3 and Q4 off; the answer | a Treasury wire journal booked on value dates, a replayed feed batch and a reposted rejected line are what a ledger tie-out finds |
| C, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's restatement by accident year | R0 to R3 values | the reserving team's own exhibit |

- **Main population zero-counts.** No ask device moves the carried figure (asserted: the call recomputes at $400
  million with the duplicates' payments dropped, the re-entered features counted twice and the January voids
  netted at the year end); the ledger, its notes and the close calendar are read by no step of the call; deleting
  every ask file leaves the call and Ask C unchanged.
- **Hazard table.** D9 (A) moves closed with and without payment in every year with advances, vehicle-claim
  settlements or duplicate-keyed payments; D1 (A) moves 2017 to 2024; D2 (A, returns) moves 2023 to 2026; D4 (B)
  moves every quarter's earlier-quarter figure; D1 (B) moves Q3 and Q4; the reposts move Q2's and Q4's two figures
  for a reader filing every manual line as other.
- **Referee.** None for the primaries; the ledger notes define the feed and the extract notes the clocks, the
  WHAT only; no filed sentence says that wires leave the feed or value-date, which features were re-entered, which
  payment ledger holds a converted feature's advance or that a duplicate can carry a payment.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A closed with a loss payment (10) | payments from both ledgers with each converted feature linked through its legacy reference, voids netted at 31 December, CV, XD and DUPLICATE rows dropped with their payments, re-entered features' archive rows kept | duplicate-keyed settlements lost and re-entered features doubled: every year off (asserted, 20 of 20 cells) | miss |
| A closed without one (10) | the same | every year off by the same features | miss |
| B earlier-quarter payments (4) | each Treasury journal read as the previous month's wires by issue date, every manual line as other | the quarter-end late wires and the reposted feed lines misfiled: every quarter off (asserted, 8 of 8 cells) | miss |
| B not claims payments (4) | the same | the reposts filed as other and the vehicle-damage wire and repeat batch filed as payments: every quarter off | miss |
| C the chart | the golden's restatement | right | outside |

Mirror leakage: 6 per cent of the ask weight on the most attractive wrong rung (the chain ladder): it misses every
Ask A and Ask B cell exactly as the cracker does, and of the chart it keeps only the bar per accident year and the
booked total, its unpaid bars and carried total being the chain ladder's.
Pair ceiling: 34 (the cracker about 52 with the call, its components and the chart; the chain-ladder mirror about
16).

## Pre-ship check

- **Rule 1, the domain:** the deciding quantity is the unpaid loss on a motor bodily injury book, estimated from a
  paid development triangle, the reserving actuary's forecast; what decides it is the field's response to a change
  in settlement speed: the closed share of ultimate claimant features, read down the diagonals, falls at every age
  from seven quarters once the claims platform goes live, and the Berquist-Sherman paid adjustment restates the
  history at the latest diagonal's closed shares before factors are taken. Swapped into unbilled energy or a
  hospital's receivables, there is no claimant feature that closes and no closed share to restate a history at, so
  the $83.0 million between the chain ladder's $316.8 million and the restated $399.8 million stands for nothing.
- **Rule 2, two layers:** Layer 1 is the two claims systems for one book: the legacy ledger and archive (US dates,
  dollars, CV and XD rows), the platform's register, events and payments (UTC timestamps, cents, DUPLICATE rows),
  the conversion and the legacy features re-entered on the platform, voids, reissues and returned checks, the
  extracts run six days after the valuation, and a ledger fed by a nightly check feed, monthly Treasury wire
  journals by bank value date and Finance's journals. Mishandled, these move the asks: the cracker path misses 20 of
  20 count cells and the face-value read misses 8 of 8 ledger cells (asserted). They do not move the call. Layer 2 is
  the development done right: the chain ladder files $316.8 million ($325 million, a release), the latest
  diagonals $283.6 to $314.1 million, the trended frequency-severity $356.5 million, and the restatement $399.8
  million ($400 million), all executed on the clean truth.
- **Rule 3, the decisive step:** the decisive step is an analytical choice: restate paid development at the latest
  closed shares before projecting. No field, code, unit or definition says it, and no filed rule performs it (the
  basis files the estimand and conventions and leaves the method to the actuary). Nothing is planted: no prior
  indication, memo, certified triangle or stakeholder figure. The leak reader's question 6 reads it as an
  analytical choice about how the paid development is projected, with nothing planted or announced.
- **Gate G:** no shipped artifact states a carried figure or ranks methods. The register's booked $344.6 million is
  the comparison the prompt asks for, with no method beside it. Deleting every wrong number leaves the difficulty
  intact, because the wrong answers come from methods, not from figures in the pack. The motor PD triangle and the
  earned car years are named distractors that argue no BI figure.
- **Determinism:** the estimand is filed in basis 2.1 and 2.2 and the conventions in 3.1 to 3.6. Every restatement
  variant (linear or exponential, closed over ultimate or over reported, volume-weighted or simple, all quarters or
  the latest twelve restated diagonals) lands at $396.5 to $404.9 million, carried at $400 million. Annual
  development is ruled out by 3.2's quarter-end ages (asserted). The asks' WHAT is in the prompt and the notes: the
  feed's previous day, the wires' 15:00 release and value date, and a closed feature's net loss payments to the
  valuation.

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
- 2026-10-14, at stage 3: the unpaid for each accident year as graded figures: the latest years differ by 2 to 3 per cent across the restatement's variants (2026 between $136 million and $144 million), so neither a $1 million nor a $5 million rounding holds; the prompt asks for the carried total and the chart shows the years.
- A carried figure rounded to $10 million: the quarterly variants spread about $8 million and straddle a $10 million edge; at $25 million the golden sits $11.6 million from an edge with every variant inside.
- Represented claims at 0.82 of their pace: the closed shares fell 1.4 points on average after the cutover and about half the post-cutover cells stayed inside the history's range, too thin for a judge to call the restatement forced; 0.75 gives about 2 points with most cells below the history's lowest.
- Ask A's "reported" and "open at 31 December" columns: a solver reading the register's dated fields gets them right; the ask counts closed features with and without a loss payment.
- Ledger amounts to the nearest dollar: Q4's earlier-quarter payments came to exactly $3,821,032.50, a half-up against half-even fork; asked to the cent.
- Ledger quarters whose only other entries were manual journals: a reader filing every manual line as other hit Q2 and Q4; two feed lines rejected for a missing state segment and reposted by manual journal (claims payments) now sit beside them.
- An annual-development convergence assertion: the annual restatement fell at $387.5 million, on the $25 million edge; annual development is ruled out by the basis's quarter-end ages (SF6) instead.
- Initial medical payments on every represented claim and a handling-unit column: restating the represented claims' own triangle explodes its early factors; bodily injury pays at settlement and no unit column ships.
- Architecture 3 at stage 4 (10-14): judge NOT_DETERMINISTIC, SEND_BACK. The basis leaves the method to the actuary (2.3), and nothing shipped selects the closure restatement over a frequency-severity method on paid per closed feature developed with volume-weighted severity factors ($343.8 million, carried $350 million) or severity trended from 2017 to 2019 ($356.5 million, $350 million); the judge's one-year emergence back-test at the 2024 Q3 to 2025 Q4 valuations favours the latest diagonals' factors, not the restatement. Filing the method makes the decisive step rule application, and no selection criterion the data decides favours the restatement (the world's true unpaid is $427.9 million, above every method, because the slowdown falls on the represented claims, which cost the most, so paid does not track closed share either). The asks reproduced to the cent. Architecture spent.
