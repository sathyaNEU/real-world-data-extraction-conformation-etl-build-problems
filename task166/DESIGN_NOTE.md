# task166 design note

Architecture 1, drawn 2026-10-18 (wave 7, the first of the wave, Forecasting lane, sathya8571), numbered from seed
FC37. The seed (a regional bank's ALCO designating one $1.2 billion, four-year pay-fixed swap overlay against one of
five fixed-rate pools, ranked by the hedge policy on the +200 bp loss in economic value averaged over the swap's first
twelve months, with the September planning cycle's base-case mortgage rate at 6.25 per cent) was read at its header
and Situation only. Its world, decision and quantity are kept. Its two decoy-era devices are not shipped: no policy
clause makes a forward-loss method conditional on reproducing a model validation control set, and no ALM report ranks
the pools on their trailing-year loss. The pitfall is re-found from how each pool's balance will run off under the
planning cycle's base case.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task166.json`, architecture v1, registered 2026-10-18. `guard.py check`
   WARN, answered below.
2. Pairing: Banking, Credit & Financial Risk (client domain) / `stress-testing-capital` / Forecasting & Predictive
   Modeling. The seed's house label was Economics (bank balance-sheet risk management); the domains README files
   lending and bank risk under Banking, never Economics ("Economics is macro, labour, trade and fiscal reads, never
   corporate finance, markets trading or lending"). The deciding quantity is a +200 bp economic value of equity (EVE)
   stress on each pool's expected cash flows through a forward year, which is interest-rate risk in the banking book,
   the rate-stress part of `stress-testing-capital`; the task type serves forecasting, and the forecast that decides
   is each pool's behavioural balance path under the planning cycle's base case.
3. Niche: a Pittsburgh regional bank holding company (about $31 billion of assets) designating its one $1.2 billion
   four-year pay-fixed swap overlay, traded on 15 December 2026 and effective 4 January 2027, against the fixed-rate
   pool whose +200 bp economic value loss averaged over calendar 2027 is largest, when the 2023-24 portfolio jumbo
   mortgages carry rates the planning path's 6.25 per cent now beats and about $3.0 billion of fixed-rate CRE balloons,
   mostly written in the bank's push of December 2021 to April 2022 at peak values and sized to its minimum cover, fall
   due from December 2026 through 2027.
4. Call and shape: the pool the overlay is designated against (`pick_one_of_n`, a named pool, question form which) and
   its +200 bp loss averaged over the twelve month-ends of 2027, in $ millions to the nearest $25 million (the
   precision every defensible construction shares, measured below). Shape `other`: the call with its critical
   components and a decoupled ask table in a workbook, and a two-slide ALCO deck; the criteria are counted in
   `## Ask sheet`.
5. Mechanism keys: gap time (the maturity record is a statement about due dates whose loans could carry a new loan;
   the decision bets on a wall whose loans mostly cannot) with population (which loans are still in each pool through
   the year); decisive pattern E (the share of due balloons that stays, conditioned on each loan's refinance cover, an
   absolute split no column names), then G13 (the year holds the wall) and G6 (the wall's mix on cover differs from
   every closed year's); Gate G `forecasting`; strategy `composition_mix` (a recent or pooled extension share does not
   apply to a wall whose mix on refinance cover differs from the measurement corpus).
6. Layer 2: `forecast_uncertainty` (the conditioning chosen on held-out maturities), pattern
   `own:balloon-maturities-extended-by-refinance-cover`. Banking has no library patterns
   (`layer2-rigor-patterns.md`); the pattern is built from the client's family (model choice on out-of-sample error)
   and the field's own refinance test.
7. Furniture: forum `committee_or_panel` (ALCO approved the overlay at its November meeting; the designation memo goes
   to ALCO's chair before the trade); forcing event `purchase_order_or_contract` (hedge designation must be documented
   at the swap's inception, so the memo is due on Monday 14 December, the day before the trade); organisation family
   `financial_institution`; role family `portfolio_manager` (the head of balance sheet management, who runs the bank's
   interest-rate risk position and its hedge programme); context artifact `close_out_summary` (the third-quarter ALM
   report: the bank's quarter-end EVE and earnings-at-risk position at balance-sheet level, which ranks no pool);
   calibration `existing_book_actuals` (the bank's own loan-level prepayment history and its CRE maturity log with
   every outcome since 2015).
8. Spine: the servicing system's monthly loan-level extract for the 2023-24 portfolio mortgages (loan by month,
   January 2023 to November 2026, about 160,000 rows, two layouts across the 2024 servicing platform conversion);
   constructed in the layout of a mortgage servicing system's monthly extract. Other files are listed at stage 3.
9. Deliverables: `overlay_designation_2027.xlsx` (the call, its components and the ask tables) and
   `overlay_designation_alco.pptx` (two slides for ALCO); the format set xlsx and pptx is in none of the last three
   builds.
10. People, drawn with `guard.py names --geo "United States" --seed 166`: Guy Morrison, Sheri Roberts, Cody Li, Jeff
    Guzman, Joshua Boyd (roles assigned at stage 3; no persona in the prompt). Invented names: Carrick Valley Bancorp
    and Carrick Valley Bank (a web search found no bank or bancorp of that name; Carrick is a Pittsburgh
    neighbourhood); counterparty and system names are left generic or checked the same way when the pack is cut.

**Data-native sentence.** Carrick Valley's records show every pool's monthly balance and every CRE maturity's outcome,
so nothing is hidden: but the fixed-rate CRE pool's balloons due from December 2026 through 2027 were written in the
bank's push of December 2021 to April 2022 at peak values, sized on pro forma rents to its 1.25 cover minimum, and
their properties' income has slipped since, so at the planning cycle's 6.95 per cent most of them cannot carry a new
loan of their balloon balance on the bank's 25-year amortization and will be extended for 36 months at their note
rates, as the maturity log shows for every loan that fell due at that cover since 2015 (27 of 27 below a cover of
1.0), while the maturities of 2023 to 2026, written with cover to spare, mostly refinanced and leave the recent
extension share at a quarter.

**Guard and similarity.** `guard.py check` WARN at registration, one line: `repeat.question_form` (which, against
task245 and task471): the decision is a pick of one pool, so the form is the decision's own. The structural
signatures (gap time, pattern E, Gate G forecasting; and with `pick_one_of_n`) repeat older builds only and carry a
differentiation line each on the card (task37 v2, task44 v2, task97 v5, task117, task137 v1 and its round-1
lineage, task155, task197). The ban window at registration held task163, task245 and task471; nothing on the card
repeats an axis of theirs.

**Abstraction test.** Stripped of nouns: two parts of a stock answer the same forward terms in opposite directions,
one leaving faster than its own past because its units' rates are beaten by the terms, the other keeping every due
unit whose own earnings no longer cover the terms it would roll onto; the part with the most exposure over the
window is found only when both answers are projected. Read against the nearest by structure:
- task137 v1 conditions a renewal share at maturity on the gap between the locked rate and the card; that is this
  build's lower rung for the mortgages (prepayment by incentive, the field's textbook curve, a reused device), and it
  is the losing rival for the CRE wall: the 2027 balloons' rate gaps are no wider than those of the 2026 maturities
  that refinanced, and what keeps them is each property's income against a new loan's debt service at the planning
  rate, joined from the operating statements. task137's current architecture rebuilds a class from entry data; no
  class is rebuilt here.
- task155 and task97 condition a take-up or repeat rate on a covariate the history carries in another form; here the
  conditioned share decides a value-sensitivity ranking only together with another pool's opposite run-off.
- task134 v2 (a hazard by time since entry) and task157 (a returning wave's leading edge) share no structure: no age
  clock and no leading edge decide.
None shares the latent structure, the default path and the correction together.

**Sources, one line each.**
- Seed FC37 header and Situation (`status.py task166`): the world, the five pools, the overlay, the policy measure and
  the 6.25 per cent planning rate; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting` (76 builds): behaviour at a maturity conditioned on a rate gap
  (task137 v1) and on a class of money (task137), hazards by time since entry (task134 v2), leading edges (task157),
  stepped payouts from a resampled distribution (task151), delayed entry (task133), a conversion yield read against
  untreated states (task163); none projects a balance sheet's pools through a forward year on their own behaviour.
- `stumping/references/client/two-layer-task-design.md`: the client's example of validating a forecast on data it was
  not built on (the extension model chosen on held-out maturities, the rivals rejected there).
- `stumping/references/strategies.md` F5 (the conditioning property rebuilt from a history, one band moving against
  the rest) and F6 (the natural fit fails forward because the rate is stationary only in a constructed quantity).
- `dataset-generation/references/layer1-messiness.md`, Banking 1 (monthly loan tapes with status transitions) and 8
  (rates on different bases and day counts), with the universal techniques for the servicing conversion and the
  custodian's securities layout.

## Default path
1. Read the hedging policy (section 3): each Schedule A pool's loss in economic value under a 200 bp parallel rise of
   the planning cycle's base-case zero curve, on the base-case expected cash flows of the positions held at the close
   on 30 November 2026, averaged over the twelve month-ends of 2027; every pool holds more than $1.2 billion and is
   eligible.
2. Treasury ladder: contractual coupons and principal from the custody statement ($67.0 million).
3. Agency MBS (the 2020-21 purchases): each pool's prepayment rate over the last twelve factor months carried forward
   ($110.5 million).
4. 2023-24 mortgages: stack the two servicing extracts through the conversion xref and fit the prepayment curve on the
   incentive against the posted jumbo rate a month earlier, the strong analyst's reflex; at the planning cycle's 6.25
   per cent the pool prepays about 30 per cent a year ($85.2 million).
5. Indirect auto: the roll's monthly prepayment rate over the last twelve months ($30.7 million).
6. Fixed-rate CRE: the term loans' payments to maturity, each balloon taken out at the extension share the maturity log
   shows for the last twelve months (0.256), or repaid when due ($68.9 million; $27.3 million).
7. Rank and designate the largest.

Ends on: Agency MBS, $100 million (110.5 to the nearest $25 million)
Golden: Fixed-rate commercial real estate, $150 million (150.9 to the nearest $25 million)

## Stump sentence
Projecting the 2023-24 mortgages on a prepayment curve at the planning rate and the commercial real estate balloons at
the extension share the maturity log shows lately files Agency MBS, $100 million; the step that lands it there is
carrying the recent share of due balloons that extended as a constant, when each balloon extends according to
whether its property's income can carry a new loan of its balance at the planning cycle's 6.95 per cent, and the $3.0
billion due from December 2026 through 2027, written in the early-2022 push at peak values and full leverage, mostly
cannot: an extension model conditioned on refinance cover, fitted on every maturity since 2015 and chosen on the
2025-26 maturities held out, puts about four-fifths of that principal on 36-month extensions and the pool's averaged
loss at $150 million.

## Three rules

Task type: stress-testing-capital (Banking, Credit & Financial Risk: interest-rate risk in the banking book, the +200 bp economic value stress), which serves Forecasting & Predictive Modeling in the taxonomy; the decisive forecast is each fixed-rate pool's behavioural run-off through 2027 under the planning cycle's base case.
Domain test: the deciding quantity is each pool's +200 bp loss in economic value averaged over the overlay's first year, the IRRBB stress a bank's ALM function computes on behavioural cash flows, and it turns on the field's two run-off forecasts: residential prepayment on the refinancing incentive at the planning rate, and commercial real estate balloon extension conditioned on refinance cover (the property's income against a new loan's debt service at the refinance rate), the credit test that decides whether a balloon can be taken out at maturity.
Swap: "which plant gets the one spare turbine, ranked on the megawatt-hours each would lose under a 20 per cent demand surge averaged over next year" keeps a ranking of five assets on a stressed loss, but loses discounted cash flows re-priced under a rate shock, and above all a borrower's refinance cover at a planning rate deciding whether a balloon leaves at maturity or stays for three years: with turbines nothing refinances, so the quantity the call turns on stops making sense.
Layer 1: the servicing platform conversion (legacy extract to the August 2024 cycle with uppercase codes, MMDDYYYY dates, rates in per cent, curtailments and payoffs apart and a trailer row; the new platform with decimals, combined unscheduled principal and zero-balance codes; the xref), loans held for sale in both extracts, the rate sheet archive (weekly sheets, mid-week re-prices, codes renamed with the pricing engine on 1 January 2024), the CRE file's floating loans and extended loans' current against original maturities, ACT/360 interest, the maturity log's two sheet layouts and its obligation and property numbers in credit administration's formats, operating statements by the borrower's own fiscal year with their review dates, the custodian's thousands, pool factors and the rest of the AFS account, the agency payment delay, and the auto portfolio's dynamic roll; each is how its system writes, none carries the call (each asserted neutral in checks.py, R2).
Layer 2: forecast_uncertainty (the conditioning of a behavioural share chosen on held-out outcomes): the choice that flips the call is forecasting each balloon's extension from its own refinance cover at the planning rate, chosen against the recent share, the rate gap and the note-rate DSCR on the 2025-26 maturities held out, not carrying the share recent maturities showed onto a wall whose cover mix the history never saw at that weight.
Decisive step: model the probability that a commercial real estate balloon is extended at maturity as a function of its refinance cover (the latest reviewed net operating income over a new loan of the balloon at the posted five-year rate on the bank's 25-year amortization), fit it on every maturity since 2015, validate it on the maturities held out, and apply it at the planning cycle's 6.95 per cent to every loan not yet extended.
Not semantics: every field is read correctly on the default path (the outcome codes, the extended maturities, the statements, the rates, the policy's measure); the maturity log's recent extension share is correctly read as a quarter of the due balloons and is still the wrong forecast for a wall whose loans mostly sit below a cover of 1.05, a mix no recent year had.
Not rule application: the policy files the measure (shock, curve, window, cash flows before credit losses, the pool at the as-of, eligibility) and says nothing about how any pool behaves; no filed rule forecasts extension, and executing every filed rule with balloons repaid when due or extended at the recent share files Agency MBS.
Analyst test: a strong analyst who stitches the servicing extracts, reads every code, fits the mortgage prepayment curve at 6.25 per cent and takes the commercial real estate balloons out at the log's recent extension share (or when due) files Agency MBS, $100 million; only conditioning each balloon's extension on its refinance cover at 6.95 per cent files Fixed-rate commercial real estate at $150 million (executed in checks.py on the generator's clean truth: R3a, R3b, every single lower correction wrong).
Estimand: the hedging policy (section 3, balance_sheet_hedging_policy.pdf) files the population (the positions in each Schedule A pool at the close on the memo's as-of date, positions added after it excluded), the outcome (present value of the pool's base-case expected cash flows after each month-end on the planning cycle's base-case zero curve, the same rates at every month-end, less the same at +200 bp), the window (the month-ends of the overlay's first twelve months), the unit ($ millions) and the comparison (the largest among the eligible pools); the prompt adds the rounding.
No decoy: no memo, draft, ranking, model output, stakeholder figure or prior designation argues for any pool or any behaviour; the third-quarter ALM report states the bank's position against its limits and ranks no pool; nothing is copied, backfilled or withheld, and the planning workbook carries rates only.
No certified replay: no shipped figure is to be reproduced to recover a method; the maturity log's outcomes and the servicing history are closed outcomes every route reads alike, and the 2025-26 hold-out is the analyst's own validation, not a published control set.
Lesson: a model learns that a balloon book's run-off at a maturity wall is set by whether each loan can be refinanced at the forward rate, its income against new debt service, so a share of recent maturities that extended does not transfer to a wall written at a different leverage and rate; no build on file conditions a balloon's extension on refinance cover.

## Readability screen
Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Figures are built (generator/calc.py routes, asserted in checks.py).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every pool at its own last twelve months, balloons repaid when due (2023-24 mortgages, $129.1 million) | the policy names the measure, which invites each pool's recent behaviour | the servicing extracts and the factors carry the last year | yes, the default | none ships; the analyst's own back-test of last year's speed on the 2024 and 2025 dips misses | no | yes, one rate | readable |
| R1 the mortgages on a fitted prepayment curve at the planning cycle's 6.25 per cent (Agency MBS, $110.5 million against $85.2 million) | the planning workbook files 6.25 per cent | the extracts' note rate and the rate sheet | yes, the ALM reflex | none | no | no | readable |
| R2a the balloons at the log's last-twelve-month extension share, 0.256 (Agency MBS; CRE $68.9 million) | no | the log's outcome column | yes, a historical share | none | no | yes | readable |
| R2b extension on the rate gap, the posted rate at maturity less the note rate (Agency MBS; CRE $65.5 million) | no | the log's note rate and the rate sheet | yes, the rate-sensitive reflex | its own hold-out (Brier 0.186) | no | no | readable |
| R2c extension on the debt service coverage at the note rate, the credit file's metric (Agency MBS; CRE $91.6 million) | no | the risk grade and the statements | yes, the credit reflex | its own hold-out (Brier 0.139) | no | no | readable |
| R3 (decisive) extension on refinance cover at the planning rate, every future maturity (CRE $150.9 million) | no sentence names cover, refinancing, a debt constant or what drives an extension; the log defines an extension's terms only | no column carries net operating income, cover or a probability on the loan file; the statements sit in their own file keyed in another format | no: the reflexes are a share, a rate gap, a note-rate DSCR | none ships: the log's outcomes are read alike by every route; only the analyst's own hold-out separates them | no: keys normalise and every join matches | no: a fitted conditional share applied loan by loan, then the cash flows re-discounted month by month | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs, and the ask's terms. Every id is
asserted in `generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "our five fixed-rate pools" | the five pools of the policy's Schedule A | every fixed-rate book the bank holds | same five candidates (no other book is named) | the policy ("the eligible pool in Schedule A") |
| SF2 | "designated against" | ALCO's designation of the overlay under the policy, section 3 | a hedge accounting designation with its own tests | same call | the policy section 3 and section 4 (the memo names the pool) |
| SF3 | "averaged loss under the hedging policy's +200 basis point test" | the mean over the overlay's first twelve month-ends | the loss at the as-of alone | CRE, $200 million (190.4) | the policy ("averaged over the month-ends of the overlay's first twelve months") |
| SF4 | the month-ends of the first twelve months | 31 January to 31 December 2027 (effective 4 January 2027) | December 2026 to November 2027; thirteen month-ends to January 2028 | same call (156.0; 148.4, both $150 million) | the prompt's dates and the policy; same call, asserted |
| SF5 | the curve at each month-end | the base-case zero rates applied from each month-end | forwards implied for each month-end | same call (151.1) | the policy ("the same zero rates at every month-end"); same call, asserted |
| SF6 | time and placement | months over twelve, each cash flow at its payment month's end | day fractions | same call | the policy ("a month counting as a twelfth of a year") |
| SF7 | expected cash flows | base-case behaviour, before credit losses | net of charge-offs | same call | the policy ("before credit losses") |
| SF8 | the pool | the positions at the close on 30 November 2026 | the pool with the plan's new business | same call | the policy ("positions added after it are not part of it") |
| SF9 | eligible | principal at the as-of at least $1.2 billion: all five | principal expected to stay above $1.2 billion to the swap's maturity | no pool designated | the policy ("its principal outstanding at the close on the as-of date") |
| SF10 | the base case | ALCO's September 2026 planning cycle: the zero curve and product rates, held after December 2027 | today's market | same call | the policy ("ALCO's most recent planning cycle") and the workbook's cycle sheet |
| SF11 | fixed-rate commercial real estate | term loans with a fixed note rate, the extended ones included | the extended loans left out | same call (144.3, $150 million) | Schedule A ("Commercial real estate term loans with a fixed note rate"); same call, asserted |
| SF12 | agency MBS | the pass-throughs bought in 2020 and 2021 | every agency pool in the account | same call | Schedule A ("bought in 2020 and 2021"); same call, asserted |
| SF13 | 2023-24 residential mortgages | held for investment, originated 2023 and 2024 | the loans held for sale too | same call (none is left at the as-of) | Schedule A ("held for investment"); same call, asserted |
| SF14 | the rounding | the averaged loss to the nearest $25 million | a finer unit | same call, the bin holding every construction | the prompt |
| SF15 | the hedge programme | the treasury system's ALM book | every swap, the customer programme included | Ask A only | the policy ("Swaps the bank writes for its customers, and the swaps that offset them, are not part of the programme") |
| SF16 | in effect at a quarter-end | effective on or before it, maturity after it | maturity on or after it | same figures (no maturity falls on a 2027 quarter-end) | the policy; same figures, asserted |
| SF17 | overlays, funding hedges, loan hedges | by what each swap is designated against | by the register's strategy code | Ask A only (overlays and funding hedges move by $275.0 million) | the policy ("Overlays are pay-fixed swaps designated against a fixed-rate asset pool") |
| SF18 | the new one included | $1.2 billion in overlays at every 2027 quarter-end | left out | Ask A only | the prompt |
| SF19 | notional | the notional of the calculation period in effect | the register's current notional held flat | Ask A only | the register ("an amortizing swap's current period") and the schedules |

## Ladder
Built figures from `generator/calc.py` (`golden`, `routes`), every row asserted in `generator/checks.py` (LADDER, FAM,
OOS, R3b). Each pool's averaged loss in $ millions.

| Rung | Construction | Treasury | Agency MBS | 2023-24 mortgages | Auto | Fixed-rate CRE | Names | Margin |
|---|---|---|---|---|---|---|---|---|
| R0 | every pool's last twelve months, balloons repaid when due | 67.0 | 110.5 | 129.1 | 30.7 | 27.3 | 2023-24 mortgages | 1.17 over Agency MBS; CRE 5th |
| R1 default | the mortgages on the fitted prepayment curve at 6.25 per cent | 67.0 | 110.5 | 85.2 | 30.7 | 27.3 | Agency MBS | 1.30 |
| R2a | R1, balloons at the log's last-year share (0.256) | | | | | 68.9 | Agency MBS | 1.30 over the mortgages; CRE 3rd |
| R2b | R1, extension on the rate gap | | | | | 65.5 | Agency MBS | 1.30 |
| R2c | R1, extension on the note-rate DSCR | | | | | 91.6 | Agency MBS | 1.21 over CRE, CRE 2nd |
| R3 decisive | R1, extension on refinance cover at 6.95 per cent, every future maturity | | | | | 150.9 | Fixed-rate CRE | 1.37 over Agency MBS |

**Position and separation.** The golden is 5th on R0 and on R1, never first on an intermediate rung, 2nd only on R2c
(Agency MBS 1.21x ahead); no rung margin is under 1.15x; the final margin is 1.37x. **Dominance:** the decisive axis
moves the pool 123.6 (27.3 to 150.9) against Agency MBS's carried lead of 83.2 on R1, 1.49x. **Grid:** the cover step
alone, with the mortgages at last year's speed, still names the pool (150.9 against 129.1, 1.17x); the mortgages'
scheduled amortization alone names the mortgages (386.9); a debt yield fitted on every maturity names the pool by
1.03x at $114.1 million (the $125 million bin), a note-rate DSCR fitted on 2023 onward at $126.5 million (the $125
million bin); every balloon extended names the pool at $189.9 million (the $200 million bin).

**The golden family (C3, asserted).** Nine constructions of the decisive step run 147.0 to 153.1, every one $150
million: the cover logit on every maturity since 2015 (150.9) or on 2023 onward (151.2); log cover (151.1); empirical
bands of 0.05 (147.0); the refinance rate a month before maturity (150.7); the statement by fiscal year end rather than
review date (147.5); cover with the rate gap (152.2); income trended at minus 2 per cent a year (153.1); interest on
30/360 (150.5). Applying the cover model to the 2027 balloons only gives 145.0, also $150 million. The bootstrap of the
629 maturities (200 resamples, seeded) puts one sigma of the golden at 3.27; the golden is 13.4 above the bin's lower
edge and 11.6 below its upper edge, and every construction plus or minus one sigma (143.7 to 156.4) stays inside it. The 30-year and 20-year debt constants
(152.0, 149.1) are ruled out by the rate sheet's product line ("25-year amortization") and also file $150 million.

**Out of sample.** Fitted on the 481 maturities to December 2024 and scored on the 148 of 2025 and 2026, cover's Brier
score is 0.037 against 0.103 for the debt yield, 0.139 for the note-rate DSCR, 0.178 for the last year's share, 0.186
for the rate gap and 0.200 for the pooled share.

**Worth on the graded quantity.** The mortgage prepayment curve moves the mortgages' loss from 129.1 to 85.2 and the
designation from the mortgages to Agency MBS; the cover step moves the pool's loss from 27.3 (or 68.9 at the recent
share) to 150.9 and the designation to the pool.

**Strength.** P(one strong solver lands the pool and the $150 million bin) about 0.15: it must see that the balloons
due through 2027 decide the ranking, that their extension cannot be read from the recent share or the rate gap, and
that each loan's income against a new loan's debt service at 6.95 per cent decides it, joined from the statements in
another key format and validated against the alternatives. P(both top responses land) about 0.03 if independent, under
0.06 with plausible correlation. The seed was fixed by rule (the task number, then the memo's month and day: 1661214)
before any data was generated and is never searched; the pool sizes (the mortgages' loan size, the agency pools' face,
the push loans' scale) were set by rule to hold the margins and to put the golden mid-bin, never by redrawing.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the positions in each Schedule A pool at the close on 30 November 2026 | filed (policy section 3, Schedule A); SF1, SF8, SF11 to SF13 |
| 2 | Unit of account | each pool's averaged loss in dollars, reported in $ millions | filed (policy, prompt); SF14 |
| 3 | Attribution window | the month-ends of the overlay's first twelve months: January to December 2027 | filed (policy); SF4 same call asserted |
| 4 | As-of dating | positions at 30 November 2026, files pulled 3 December 2026 | filed (prompt, extract notes); statements to 30 November or 3 December the same figure (asserted) |
| 5 | Version basis | ALCO's September 2026 planning cycle | filed (policy: the most recent cycle); SF10 |
| 6 | Denominator | none: a loss in dollars | n/a |
| 7 | Weighting | the mean of twelve month-end losses, equal weights | filed (policy "averaged") |
| 8 | Window length | the extension history the model is fitted on | C3: every maturity since 2015 or since 2023 the same bin (asserted) |
| 9 | Boundary inclusivity | cash flows after each month-end; eligibility at least the notional | filed (policy) |
| 10 | Rounding path | the unrounded average to the nearest $25 million | filed (prompt); SF14 |
| 11 | Tie-break | none: the margin is 1.37x | n/a |
| 12 | Maturity and censoring | the balloons due after the as-of are unresolved; their extension is the forecast | the decisive step itself (open, forced by the hold-out) |
| 13 | Order of operations | each pool's cash flows, the measure per month-end, the mean | filed (policy) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | the loans converted in August 2024 appear in both servicing extracts on their own cycles only | C1: the xref joins them; no cycle is in both extracts (asserted) |
| 16 | Identity normalisation | legacy loan numbers to loan ids; obligation and property numbers to the loan file's | the xref and the formats in the extract notes; C1 (every log row joins its statements, asserted) |
| 17 | Netting against gross | none on the call | n/a |
| 18 | Dimensional units | the custodian's thousands; rates in per cent and decimals | the extract notes; R2 asserted |
| 19 | Code and status semantics | outcome codes in two layouts; servicing status and zero-balance codes | the extract notes; R2 asserted |
| 20 | Integerisation | none before the rounding | the golden mid-bin with one sigma (asserted) |
| 21 | Clause scope | the policy's measure applies to every Schedule A pool | filed |
| 22 | Forward window contents | each pool's behaviour through 2027 and beyond under the base case | forecast from the records (the decisive step and its rungs) |

## Literal reader
Executing the prompt and the hedging policy word for word gives each Schedule A pool's loss in economic value under a
200 bp parallel rise of the September 2026 planning cycle's base-case zero curve, the same zero rates at every
month-end, on the base-case expected cash flows before credit losses of the positions held at the close on 30 November
2026, averaged over the month-ends of 31 January to 31 December 2027, the largest designated and its figure given to
the nearest $25 million; no shipped sentence says how any pool's payments, prepayments or maturities behave, so a
literal reader must forecast them; the easy method on the same literal estimand (the mortgages on a prepayment curve
at 6.25 per cent, the balloons at the log's recent extension share) files Agency MBS at $100 million, and the fork
table leaves no reading under which a lower rung is the golden.

## Oracles

- The maturity log's outcomes (2015 to 2026): closed outcomes every route reads alike; on the wrong path they supply
  the recent share; only the analyst's own hold-out separates the conditionings, and no shipped figure scores them.
- The servicing history and the agency factors: read alike by every route.
- The third-quarter ALM report: the bank's EVE and NII against limits at 30 September, consistent with every route; it
  carries no pool and no programme figure.
- The custody statement's prices and the operating statements' revenue lines: read by no route.
- Ask A: the clearing statement ties every cleared trade's clearing ref under every handling; no control total ties
  only under the golden.

## Ask sheet

**Main call's declared row population:** the servicing extracts' 2023-24 held-for-investment loan-months and the xref,
the rate sheet archive, the CRE term loan file's fixed-rate loans, the maturity log, the operating statements, the
custody statement's Treasury notes and 2020-21 agency pools with their factors, the auto tape and roll, the planning
workbook and the policy. Device and hazard rows in it: 0 (asserted, DEVICE: the call's figures are unchanged with the
register, the schedules and the clearing statement deleted, and the call reads no swap file).

**Ask A. The hedge programme's notional in effect at each quarter-end of 2027 for its overlays (the new one included),
its funding hedges and its loan hedges** (12 figures, $ millions to one decimal).
- H18 home: a component of the designation memo the policy files (section 4: the memo "states the programme's notional
  in effect at each quarter-end of the overlay's first year"), on rows the call never reads.
- Use: the workbook's programme sheet and the deck's second slide (the 15 per cent pay-fixed limit is read from it).
- Golden: overlays 3,127.8, 3,114.3, 3,101.2, 3,088.4; funding hedges 437.5, 437.5, 537.5, 537.5; loan hedges 2,047.5,
  1,647.5, 1,313.2, 1,313.2 (31 March, 30 June, 30 September, 31 December 2027).
- Primary A1 (D1, the same records under two key schemes): four of the programme's uncleared trades with one dealer
  (an overlay, a funding hedge and two loan hedges) were backloaded into clearing on 18 September 2026; the treasury
  system booked the cleared trades and still carries the bilateral originals as live. The only evidence is the
  clearing statement's client_trade_ref, which holds each bilateral trade's number as the reference of its cleared
  trade (the trades cleared at execution carry the execution platform's id). Fair: the statement names the bilateral
  trade each cleared trade replaced. Silent: every trade number is unique, no row is an exact duplicate, every cleared
  trade's clearing ref is on the statement and every statement row is in the register, and no shipped sentence
  mentions a backload (asserted).
- Over-cleaning half: two genuine pairs, each one leg bilateral with a dealer and one leg cleared, carry identical terms
  (an overlay pair and a loan hedge pair), so dropping every trade whose terms repeat another's loses real swaps.
- Second device A2 (D2, a label stored before a silent switch, adjudicated by the policy): a pay-fixed swap entered as
  a funding hedge was designated against the 2019-22 mortgages in April 2026; the register's strategy code still reads
  FUNDING while its hedged item reads the mortgage pool. A mirror device: the policy's definition of the parts settles
  it.
- Hazards: the amortizing overlay and loan hedge (their schedules), the forward-starting funding hedge (1 July 2027),
  maturities inside 2027 (17 March, 14 April, 17 August, 15 September), a terminated trade, the customer programme in
  the same register, the new overlay from 4 January 2027.
- Stops (built and asserted, cracker.py): the battery's read with the parts by hedged item (the cracker): all 12 miss
  (overlays 3,440.3, 3,426.8, 3,413.7, 3,400.9; funding 625.0, 625.0, 725.0, 725.0; loans 2,622.5, 2,222.5, 1,888.2,
  1,888.2); by strategy code: all 12 miss; the backload read but parts by strategy code: the 8 overlay and funding
  figures miss; every repeated set of terms dropped: the 8 overlay and loan figures miss; the golden.
- Span: the register (book, strategy, hedged item, cleared, clearing ref, bank pays, notional, dates, status), the
  schedules, the clearing statement (client_trade_ref, ccp_trade_id), the policy, the extract notes (5 files).
- Realism: backloading moves a bilateral trade into clearing under a new trade id while the original waits on the
  dealer's termination confirmation; split executions with two dealers on the same terms are ordinary.

**The chart** (`overlay_designation_alco.pptx`, slide 2): one stacked bar per 2027 quarter-end, the three parts
stacked, each segment labelled with its value; graded on its parts and on its values (Ask A's).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| Amortizing schedules (an overlay quarterly, a loan hedge semi-annually) | A | overlays and loans held at today's notional: every figure |
| The forward-starting funding hedge | A | funding at 31 March and 30 June by $350.0 million |
| The customer programme in the register | A | every figure, if not filtered |

**Referee.** The clearing statement for A1; it hands over no level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and definition):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, overlays at four quarter-ends | the register's live ALM trades by hedged item, the schedules, the new overlay added | A1, the backloaded overlay counted twice | miss |
| A, funding hedges at four quarter-ends | the same | A1, the backloaded funding hedge counted twice | miss |
| A, loan hedges at four quarter-ends | the same | A1, the two backloaded loan hedges counted twice | miss |
| Deck slide 2, the labels' values | the same figures charted | A1 | miss |

**Mirror sheet.** The mirror stops at R1 (Agency MBS) on the call and reads the ask the same way: it keeps the chart's
three structural parts and no figure.

Pair ceiling: 38.8 (cracker 38 + 7 + 55 x 3/16 = 55.3; mirror 5 + 7 + 55 x 3/16 = 22.3)

Mirror leakage: 18.8 per cent of ask weight (the chart's three structural parts of 16 ask criteria)

Measured by: generator/cracker.py (run on a fresh unzip of target.zip)

## Residual

What stage 3 leaves standing, as measured (every figure asserted in checks.py):
- The income routes. The note-rate DSCR fitted on every maturity names Agency MBS by 1.21x (CRE 91.6); fitted on 2023
  onward it names the pool at $126.5 million, the $125 million bin. The debt yield fitted on every maturity names the
  pool by 1.03x at $114.1 million (the $125 million bin); fitted on 2023 onward it files $147.8 million, the golden's
  bin: on the 2023 to 2026 maturities the refinance rates sit at the planning rate's level, so the debt yield there is
  the cover up to a constant. An income-based extension model is the decisive insight in either form; the rate
  adjustment separates the two only on the full history.
- The mortgages' own loss moves with the prepayment construction (80.6 to 85.6 over the curve's variants) and is never
  above Agency MBS; the call never rests on it (the cover step with last year's mortgage speed still names the pool,
  1.17x).
- Rung 0's margin is 1.17x (the mortgages at last year's speed against Agency MBS); last six months' speed names the
  mortgages by 1.06x. Either way a wrong answer.
- The reporting unit. Nine constructions of the decisive step run 147.0 to 153.1 with a bootstrap sigma of 3.27, so the
  figure is graded to the nearest $25 million; at $10 million the bands variant (147.0) and the trended-income variant
  (153.1) would print different figures.
- Every agency pool in the account read as the MBS pool: 124.8, still 1.21x under the golden.
- The fingerprint heart gate: BLOCK on `ban.forum` against task198 (v2), whose card was registered at 05:25:01Z, one
  minute before this card (05:26:01Z), and reached main after this build's DRAWN commit, so the draw's ban window did
  not show it. The forum is honest (ALCO designates the overlay under the policy and receives the memo); the card is
  not relabelled and its stamps are untouched. The main session decides: hold the draw as registered, or redraw the
  forum (for example a designation the Treasurer makes under delegated authority and reports to ALCO), which moves
  the policy's section 3 and section 4 sentences, the deck's audience and the card's forum key, and no figure.

## Leak sweep

`leak.py task166 --asof 2026-12-03` returns REVIEW (no LEAK); every line answered:
- Sweep 2, `ladder` in the policy: the Treasury ladder is the pool's own name, declared under `field_terms`.
- Sweep 3, the call's words in the policy, the extract notes and the ALM report (overlay, fixed-rate, commercial real
  estate, pool): the policy names the pools it governs and the notes the files; none states a loss, ranks a pool or
  names the designation.
- Sweep 4, design-note vocabulary in the policy (maturity, agency, planning, mortgages, recent, credit), the notes
  (maturity, agency, planning, servicing, extended, credit) and the ALM report (mortgages, balance, twelve, income):
  the files' own subjects; none names refinance cover, a debt constant, a debt yield or what drives an extension
  (asserted in checks.py, R3c).
- Sweep 9, dates after the pull: records that carry future dates by nature (loan and swap maturities, next due dates,
  rate-lock expirations, the plan's months, amortization periods, the log's extended-to dates).

## Surface screen

`guard.py surface task166` exits 0 and promotes pairs for the author's adjudicated `/clone-check`. Before the final cut
it promoted task133 on a prompt construction the two prompts shared ("i also need two slides for"); the deck sentence
was rewritten and the pair dropped out. The six left (task155, task37, task117, task137, task44, task97) are the
card-level signatures differentiated at the draw (decisive gap time and pattern E with Gate G forecasting), none
sharing a file name, schema, same-seed table or invented name.

## Build record

Stage 3, 2026-10-18. `build.py`: checks 84 run, 0 failed (the three-rules block R1 to R3c on the generator's clean
truth, every SF row SF1 to SF19, the ladder and its grid, the golden family and its bootstrap, the out-of-sample
choice, the ask's devices, the separation line, the distractors' deletion, the input gates and the realism sweep);
`verify.py` (pandas, no generator import, every format read with a positive control) 14 passed, 0 failed; two
consecutive builds byte-identical (target, golden, figures.json); `figures_check.py` 44 figures, 0 absent;
`precut.py` PASS; `voice-check.py` PASS (907 characters); H1 audit clean on the pack and the goldens; `leak.py`
REVIEW, no LEAK; `guard.py validate` clean, `surface` exit 0, `heart` BLOCK (Residual); `cracker.py` on a fresh unzip
of target.zip: pair ceiling 38.8, mirror leakage 18.8 per cent. 20 files in 4 formats, the largest the servicing
extract at 116,277 rows; distractors `deposit_decay_study_2026.xlsx` and `mortgage_lock_pipeline_20261130.csv`.
Invented names searched: Carrick Valley Bancorp and Carrick Valley Bank (no bank of that name), the dealers
Halvorsen Markets, Pemberly Securities, Corvane Bank NA, Ostrander Securities and Larkmoor Capital Markets (no firm of
those names; Redfern Capital Markets was renamed, a letter from a real Florida real estate investor); personas from
`guard.py names`.

## Tried and rejected

- The mortgages' prepayment by refinancing incentive as the decisive step (the brief's first idea), worked at the
  draw: an incentive curve fitted to the bank's own loan history is the field's textbook construction and the strong
  solver's reflex, and as a decisive step it is task137 v1's driver (a behavioural share stable only per unit of the
  rate gap) in mortgage nouns; kept as the default path's own correction, the rung that moves the mortgages off the
  call, never as the step that lands it.
- The +200 bp loss with behaviour re-projected under the shock (negative convexity) as the decisive step, prototyped:
  with the policy's swap-curve discounting the in-the-money mortgages' extension under the shock adds value (their
  coupons sit above the shocked curve), so the re-projected loss came out at half the static one (3.1 against 6.2 per
  cent of balance), and with product-rate discounting the scheduled-only and flat-hold routes land on the same pool as
  the golden; the policy files the base-case cash flows, re-discounted.
- Burnout (a pool's response falling with its time already in the money) as the decisive step: the 2023-24 vintage
  has already been through the 2024 and 2025 rate dips, so burnout slows it, which puts the golden on the pool every
  flat-hold route picks; and the latent-depletion structure sits in task137's family.
- Seasoning (a hazard by loan age) as the decisive step: task134 v2's driver, and an age covariate any full model
  carries.
- Eligibility as a forecast (a pool eligible only if its base-case balance stays above the notional to the swap's
  maturity, the portfolio layer method's own test): an eligibility check deciding the call is a backdrop and a
  threshold on a forecast; eligibility is filed as a plain fact on the designation-date balance.
- A first card with the honest keys gap time and pattern E blocked on the older same-puzzle and same-driver
  signatures; the keys were kept (pattern C was the other candidate and does not describe a conditioned share) and
  each older build got a differentiation line on the card.
- Redfern Capital Markets as a dealer's name, at stage 3: a letter from a real Florida real estate investor (H21); renamed
  Larkmoor Capital Markets, no figure moved.
