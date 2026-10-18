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
3. Niche: a Pittsburgh regional bank holding company (about $38 billion of assets) designating its one $1.2 billion
   four-year pay-fixed swap overlay, traded on 15 December 2026 and starting on 4 January 2027, against the
   fixed-rate pool whose +200 bp economic value loss averaged over calendar 2027 is largest, when the 2023-24
   portfolio jumbo mortgages carry rates the planning path's 6.25 per cent now beats and about $3.2 billion of
   fixed-rate CRE balloons, nearly all written in the bank's push of December 2021 to April 2022 (sized on pro forma
   rents at the credit box's full proceeds, half of them interest only), fall due from December 2026 through 2027.
4. Call and shape: the pool the overlay is designated against (`pick_one_of_n`, a named pool, question form which) and
   its +200 bp loss averaged over the twelve month-ends of 2027, in $ millions to the nearest $10 million (the
   precision every out-of-sample-valid construction shares within a quarter of the bin, measured below). Shape `other`: the call with its critical
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
bank's push of December 2021 to April 2022, at the credit box's full proceeds on pro forma rents and half of them
interest only, and their properties' income has slipped since, so at the planning cycle's 6.95 per cent most of them
cannot carry a new loan of their balloon on the bank's 25-year amortization and will take the bank's one extension
(36 months, a tenth paid down, the rest at the posted rate), as the maturity log shows for nearly every loan that fell
due below a cover of about 1.08 since 2015, while the maturities of 2023 to 2026, written in the pandemic years' tighter
box, mostly refinanced and leave the recent extension share near an eighth.

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
   on 30 November 2026, averaged over the twelve month-ends of the overlay's first year (it starts on 4 January 2027);
   every pool holds more than $1.2 billion and is eligible.
2. Treasury ladder: contractual coupons and principal from the custody statement ($67.0 million).
3. Agency MBS (the 2020-21 purchases): each pool's prepayment rate over the last twelve factor months carried forward
   ($110.5 million).
4. 2023-24 mortgages: stack the two servicing extracts through the conversion xref and fit the prepayment curve on the
   incentive against the posted jumbo rate a month earlier, the strong analyst's reflex; at the planning cycle's 6.25
   per cent the pool prepays about 30 per cent a year ($85.2 million).
5. Indirect auto: the roll's monthly prepayment rate over the last twelve months ($30.7 million).
6. Fixed-rate CRE: the term loans' payments to maturity, each balloon taken out on the bank's extension at the share
   the maturity log shows for the last twelve months (0.119), or repaid when due ($38.1 million; $19.6 million).
7. Rank and designate the largest.

Ends on: Agency MBS, $110 million (110.5 to the nearest $10 million)
Golden: Fixed-rate commercial real estate, $150 million (149.99 to the nearest $10 million)

## Stump sentence
Projecting the 2023-24 mortgages on a prepayment curve at the planning rate and the commercial real estate balloons at
the extension share the maturity log shows lately files Agency MBS, $110 million; the step that lands it there is
carrying the recent share of due balloons that extended as a constant, when each balloon extends according to
whether its property's income can carry a new loan of its balance at the planning cycle's 6.95 per cent, and the
$3.2 billion due from December 2026 through 2027, nearly all written in the early-2022 push on pro forma rents, mostly
cannot: an extension model conditioned on refinance cover, fitted on every maturity since 2015 and chosen on the
2025-26 maturities held out, puts about nine-tenths of that principal on the bank's 36-month extension and the pool's
averaged loss at $150 million.

## Three rules

Task type: stress-testing-capital (Banking, Credit & Financial Risk: interest-rate risk in the banking book, the +200 bp economic value stress), which serves Forecasting & Predictive Modeling in the taxonomy; the decisive forecast is each fixed-rate pool's behavioural run-off through 2027 under the planning cycle's base case.
Domain test: the deciding quantity is each pool's +200 bp loss in economic value averaged over the overlay's first year, the IRRBB stress a bank's ALM function computes on behavioural cash flows, and it turns on the field's two run-off forecasts: residential prepayment on the refinancing incentive at the planning rate, and commercial real estate balloon extension conditioned on refinance cover (the property's income against a new loan's debt service at the refinance rate), the credit test that decides whether a balloon can be taken out at maturity.
Swap: "which plant gets the one spare turbine, ranked on the megawatt-hours each would lose under a 20 per cent demand surge averaged over next year" keeps a ranking of five assets on a stressed loss, but loses discounted cash flows re-priced under a rate shock, and above all a borrower's refinance cover at a planning rate deciding whether a balloon leaves at maturity or stays for three years: with turbines nothing refinances, so the quantity the call turns on stops making sense.
Layer 1: the servicing platform conversion (legacy extract to the August 2024 cycle with uppercase codes, MMDDYYYY dates, rates in per cent, curtailments and payoffs apart and a trailer row; the new platform with decimals, combined unscheduled principal and zero-balance codes; the xref), loans held for sale in both extracts, the rate sheet archive (weekly sheets, mid-week re-prices, codes renamed with the pricing engine on 1 January 2024), the CRE file's floating loans, extended loans' current terms against their original maturities and interest-only loans beside amortizing ones, ACT/360 interest, the maturity log's two sheet layouts, its five outcome codes and its obligation and property numbers in credit administration's formats, operating statements by the borrower's own fiscal year with their review dates and the underwriting row, the custodian's thousands, pool factors and the rest of the AFS account, the agency payment delay, and the auto portfolio's dynamic roll; each is how its system writes, none carries the call (each asserted neutral in checks.py, R2).
Layer 2: forecast_uncertainty (the conditioning of a behavioural share chosen on held-out outcomes): the choice that flips the call is forecasting each balloon's extension from its own refinance cover at the planning rate, chosen against the recent share, the rate gap and the note-rate DSCR on the 2025-26 maturities held out, not carrying the share recent maturities showed onto a wall whose cover mix the history never saw at that weight.
Decisive step: model the probability that a commercial real estate balloon is extended at maturity as a function of its refinance cover (the latest reviewed net operating income over a new loan of the balloon at the posted five-year rate on the bank's 25-year amortization), fit it on every original maturity since 2015, validate it on the maturities held out, and apply it at the planning cycle's 6.95 per cent to every loan not yet extended, an extension running on the bank's filed terms.
Not semantics: every field is read correctly on the default path (the outcome codes, the extended maturities, the statements, the rates, the policy's measure); the maturity log's recent extension share is correctly read as about an eighth of the due balloons and is still the wrong forecast for a wall nine-tenths of whose principal sits below a cover of 1.05, a mix no recent year had.
Not rule application: the policy files the measure (shock, curve, window, cash flows before credit losses, the pool at the as-of, eligibility) and says nothing about how any pool behaves; no filed rule forecasts extension, and executing every filed rule with balloons repaid when due or extended at the recent share files Agency MBS.
Analyst test: a strong analyst who stitches the servicing extracts, reads every code, fits the mortgage prepayment curve at 6.25 per cent and takes the commercial real estate balloons out at the log's recent extension share (or when due) files Agency MBS, $110 million; only conditioning each balloon's extension on its refinance cover at 6.95 per cent files Fixed-rate commercial real estate at $150 million (executed in checks.py on the generator's clean truth: R3a, R3b, every single lower correction wrong).
Estimand: the hedging policy (section 3, balance_sheet_hedging_policy.pdf) files the population (the positions in each Schedule A pool at the close on the memo's as-of date, positions added after it excluded), the outcome (present value of the pool's base-case expected cash flows after each month-end on the planning cycle's base-case zero curve, the same rates at every month-end, less the same at +200 bp), the window (the month-ends of the overlay's first twelve months), the unit ($ millions) and the comparison (the largest among the eligible pools); the prompt adds the overlay's start (4 January, which fixes the twelve month-ends as January to December 2027) and the rounding.
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
| R2a the balloons at the log's last-twelve-month extension share, 0.119 (Agency MBS; CRE $38.1 million) | no | the log's outcome column | yes, a historical share | none | no | yes | readable |
| R2b extension on the rate gap, the posted rate at maturity less the note rate (Agency MBS; CRE $32.1 million) | no | the log's note rate and the rate sheet | yes, the rate-sensitive reflex | its own hold-out (Brier 0.099) | no | no | readable |
| R2c extension on the debt service coverage at the note rate, the credit file's metric (Agency MBS; CRE $52.4 million) | no | the risk grade and the statements | yes, the credit reflex | its own hold-out (Brier 0.065) | no | no | readable |
| R3 (decisive) extension on refinance cover at the planning rate, every future maturity (CRE $150.0 million) | no sentence names cover, refinancing, a debt constant or what drives an extension; the log defines an extension's terms only | no column carries net operating income, cover or a probability on the loan file; the statements sit in their own file keyed in another format | no: the reflexes are a share, a rate gap, a note-rate DSCR | none ships: the log's outcomes are read alike by every route; only the analyst's own hold-out separates them | no: keys normalise and every join matches | no: a fitted conditional share applied loan by loan, then the cash flows re-discounted month by month | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs, and the ask's terms. Every id is
asserted in `generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "our five fixed-rate pools" | the five pools of the policy's Schedule A | every fixed-rate book the bank holds | same five candidates (no other book is named) | the policy ("the eligible pool in Schedule A") |
| SF2 | "designated against" | ALCO's designation of the overlay under the policy, section 3 | a hedge accounting designation with its own tests | same call | the policy section 3 and section 4 (the memo names the pool) |
| SF3 | "averaged loss under the hedging policy's +200 basis point test" | the mean over the overlay's first twelve month-ends | the loss at the as-of alone | CRE, $190 million (189.3) | the policy ("averaged over the month-ends of the overlay's first twelve months") |
| SF4 | the month-ends of the first twelve months | 31 January to 31 December 2027: the overlay starts on 4 January | a spot start on 17 December, December 2026 to November 2027; thirteen month-ends to January 2028 | CRE, $160 million (155.0); CRE, $150 million (147.6) | the prompt ("starts on Monday 4 January") and the policy ("the month-ends of the overlay's first twelve months"), asserted |
| SF5 | the curve at each month-end | the base-case zero rates applied from each month-end | forwards implied for each month-end | same call (150.2) | the policy ("the same zero rates at every month-end"); same call, asserted |
| SF6 | time and placement | months over twelve, each cash flow at its payment month's end | day fractions | same call | the policy ("a month counting as a twelfth of a year") |
| SF7 | expected cash flows | base-case behaviour, before credit losses | net of charge-offs | same call | the policy ("before credit losses") |
| SF8 | the pool | the positions at the close on 30 November 2026 | the pool with the plan's new business | same call | the policy ("positions added after it are not part of it") |
| SF9 | eligible | principal at the as-of at least $1.2 billion: all five | principal expected to stay above $1.2 billion to the swap's maturity | no pool designated | the policy ("its principal outstanding at the close on the as-of date") |
| SF10 | the base case | ALCO's September 2026 planning cycle: the zero curve and product rates, held after December 2027 | today's market | same call | the policy ("ALCO's most recent planning cycle") and the workbook's cycle sheet |
| SF11 | fixed-rate commercial real estate | term loans with a fixed note rate, the extended ones included | the extended loans left out | CRE, $140 million (144.5) | Schedule A ("Commercial real estate term loans with a fixed note rate"); asserted |
| SF12 | agency MBS | the pass-throughs bought in 2020 and 2021 | every agency pool in the account | same call | Schedule A ("bought in 2020 and 2021"); same call, asserted |
| SF13 | 2023-24 residential mortgages | held for investment, originated 2023 and 2024 | the loans held for sale too | same call (none is left at the as-of) | Schedule A ("held for investment"); same call, asserted |
| SF14 | the rounding | the averaged loss to the nearest $10 million | a finer unit | same call; every out-of-sample-valid construction sits in the bin's middle half | the prompt |
| SF15 | the hedge programme | the treasury system's ALM book | every swap, the customer programme included | Ask A only | the policy ("Swaps the bank writes for its customers, and the swaps that offset them, are not part of the programme") |
| SF16 | in effect at a quarter-end | effective on or before it, maturity after it | maturity on or after it | same figures (no maturity falls on a 2027 quarter-end) | the policy; same figures, asserted |
| SF17 | overlays, funding hedges, loan hedges | by what each swap is designated against | by the register's strategy code | Ask A only (overlays and funding hedges move by $275.0 million) | the policy ("Overlays are pay-fixed swaps designated against a fixed-rate asset pool") |
| SF18 | the new one included | $1.2 billion in overlays at every 2027 quarter-end | left out | Ask A only | the prompt |
| SF19 | notional | the notional of the calculation period in effect | the register's current notional held flat | Ask A only | the register ("an amortizing swap's current period") and the schedules |
| SF20 | a loan already extended | repays at its extended date | extended again on cover (the 32 extended loans) | same call (152.7) | the extract notes ("An extended loan is not extended again: at its extended maturity it is paid or goes to special assets"), asserted |
| SF21 | the extension's terms | a tenth of the principal due paid down, the rest at the posted five-year rate on the maturity date (the plan's 6.95 per cent in 2027) amortizing over 25 years, 36 months | the note's rate and payment held, nothing paid down; November's posted rate | CRE, $160 million (159.9); same call (149.6) | the extract notes ("one extension, of 36 months, on a paydown of 10 per cent of the principal due, at the bank's posted five-year fixed rate on the maturity date, the payment amortizing the rest over 25 years"), asserted |
| SF22 | EXT-S | six months on the note's terms for a sale under contract, read as the repayment it precedes | dropped from the fit; carried forward at its share; read as the 36-month extension | same call (150.0; 149.4); CRE, $130 million (130.1) | the extract notes ("EXT-S, extended six months on the note's terms for a sale under contract"), asserted |

## Ladder
Built figures from `generator/calc.py` (`golden`, `routes`), every row asserted in `generator/checks.py` (LADDER, FAM,
OUT, BYPASS, OOS, R3b). Each pool's averaged loss in $ millions.

| Rung | Construction | Treasury | Agency MBS | 2023-24 mortgages | Auto | Fixed-rate CRE | Names | Margin |
|---|---|---|---|---|---|---|---|---|
| R0 | every pool's last twelve months, balloons repaid when due | 67.0 | 110.5 | 129.1 | 30.7 | 19.6 | 2023-24 mortgages | 1.17 over Agency MBS; CRE 5th |
| R1 default | the mortgages on the fitted prepayment curve at 6.25 per cent | 67.0 | 110.5 | 85.2 | 30.7 | 19.6 | Agency MBS | 1.30 |
| R2a | R1, balloons at the log's last-year share (0.119) | | | | | 38.1 | Agency MBS | 1.30 over the mortgages; CRE 4th |
| R2b | R1, extension on the rate gap | | | | | 32.1 | Agency MBS | 1.30; CRE 4th |
| R2c | R1, extension on the note-rate DSCR | | | | | 52.4 | Agency MBS | 1.30; CRE 4th |
| R3 decisive | R1, extension on refinance cover at 6.95 per cent, every future maturity | | | | | 150.0 | Fixed-rate CRE | 1.36 over Agency MBS |

**Position and separation.** The golden is 5th on R0 and on R1 and 4th on every R2 rung, never first on an intermediate
rung; no rung margin is under 1.15x; the final margin is 1.36x. **Dominance:** the decisive axis moves the pool 130.4
(19.6 to 150.0) against Agency MBS's carried lead of 90.9 on R1, 1.43x. **Grid:** the cover step alone, with the
mortgages at last year's speed, still names the pool (150.0 against 129.1, 1.16x); the mortgages' scheduled
amortization alone names the mortgages (386.9); a debt yield fitted on every maturity names the pool by 1.23x at $136.0
million (the $140 million bin), a note-rate DSCR fitted on 2023 onward files $65.5 million; every balloon extended
names the pool at $174.6 million (the $170 million bin).

**The golden family (C3, asserted: FAM).** Every out-of-sample-valid construction of the decisive step, with its
hold-out Brier score (refitted on the 510 maturities to December 2024, scored on the 274 of 2025 and 2026), files
$150 million, and each plus or minus one sigma sits inside 147.5 to 152.5:

| Construction | Figure | Hold-out Brier |
|---|---|---|
| cover logit, every maturity since 2015 (the golden) | 149.99 | 0.0126 |
| cover logit, maturities since 2023 | 150.39 | 0.0115 |
| log cover | 150.08 | 0.0126 |
| cover bands of 0.05 (edges at 0.70, 0.75, ...) | 149.68 | 0.0143 |
| cover bands of 0.05, offset (0.725, 0.775, ...) | 150.09 | 0.0160 |
| cover bands of 0.10 (0.70, 0.80, ...) | 149.09 | 0.0139 |
| cover bands of 0.10, offset (0.75, 0.85, ...) | 149.52 | 0.0205 |
| hard cut at 1.09 (the data's choice) | 149.98 | 0.0109 |
| debt yield logit, maturities since 2023 | 149.17 | 0.0123 |
| debt yield and the refinance rate | 150.24 | 0.0122 |
| cover logit, the 2027 balloons only (later ones repaid when due) | 149.35 | 0.0126 |
| refinance rate a month before maturity | 149.85 | 0.0130 |
| statement by fiscal year end rather than review date | 149.82 | 0.0137 |
| cover and rate gap | 150.11 | 0.0115 |
| income trended at minus 2 per cent a year | 150.61 | 0.0126 |
| sale-pending outcomes dropped from the fit | 150.04 | 0.0125 |
| sale-pending six months carried forward at their share | 149.40 | 0.0126 |
| interest on 30/360 | 149.50 | 0.0126 |

The data-chosen cut is 1.09 (hold-out 0.0109, the best; in-sample also the best); every cut that scores within 1.25
times the best lands in the middle half, and cuts from 1.12 up score 0.018 or worse and file 152.4 to 157.7. Cover with
property type files 150.3 (H14). The bootstrap of the 784 maturities (200 resamples, seeded) puts one sigma of the
golden at 0.77; the constructions run 149.09 to 150.61, 148.33 to 151.38 with one sigma. Reading the sale-pending six
months as the 36-month extension misreads a filed code and files 130.1 (hold-out 0.0445).

**The routes kept outside (asserted: OUT, RIVALS).**

| Construction | Figure | Hold-out Brier | Against the bin |
|---|---|---|---|
| the 1.25 cover convention (a balloon extends below 1.25) | 157.73 | 0.2007 | 2.7 above |
| the 1.00 cover rule | 141.53 | 0.0401 | 3.5 below |
| note-rate DSCR logit, every maturity | 52.40 | 0.0654 | 92.6 below |
| note-rate DSCR logit, maturities since 2023 | 65.50 | 0.0540 | 79.5 below |
| debt yield logit, every maturity | 136.02 | 0.0389 | 9.0 below |
| the 2027 balloons' model share carried to every balloon | 160.46 | as the golden's | 5.5 above |
| every balloon extended | 174.58 | 0.9088 | 19.6 above |
| every 2027 balloon extended | 162.92 | | 7.9 above |
| in-place cover (on the current payment) below 1.20 | 75.28 | | 74.7 under the golden |
| in-place cover below 1.25 | 77.66 | | 72.3 under the golden |
| the watch list (grade 6 or worse) extending | 32.93 | | 117.1 under the golden |
| rate gap logit, every maturity; since 2023 | 32.11; 33.63 | 0.0989; 0.0848 | below |
| the last twelve months' share; since 2023; pooled | 38.10; 33.68; 27.70 | 0.0829; 0.0829; 0.0865 | below |
| property type shares since 2023; repaid when due | 33.90; 19.59 | | below |

The in-place and watch-list routes miss by more than a bin because in-place cover and grade are set by the current
payment and refinance cover by the balloon at the planning rate: the push's interest-only loans (128 of the pool's
360) carry in-place cover near 1.8 on their interest-only payment and refinance cover near 0.8 on their whole balance,
while the later high-coupon loans carry in-place cover near 1.2 and refinance cover above 1.3.

**The constant-share bypass (asserted: BYPASS).** A single extension share on every balloon not yet extended lands only
between 0.809 and 0.874: 0.85 lands (151.3); one half files 97.1, three-fifths 112.6, two-thirds 122.9, 0.7 128.1,
three-quarters 135.8, four-fifths 143.6, nine-tenths 159.1, all 174.6. On the 2027 balloons alone, later ones repaid
when due, it lands between 0.875 and 0.945: nine-tenths lands (148.6, the wall's own model share being 0.909), and one
half 91.3, two-thirds 115.1, 0.7 119.9, three-quarters 127.1, four-fifths 134.3, 0.85 141.4 and all 162.9 miss.

**Out of sample.** Cover's Brier score is 0.013 against 0.039 for the debt yield, 0.065 for the note-rate DSCR, 0.083
for the last year's share, 0.0865 for the pooled share and 0.099 for the rate gap (asserted: cover beats every rival by
half). The history carries the exceptions a book has: 2 payoffs below the fitted break (1.087) and 6 extensions above
it, 4 six-month extensions for a sale and 2 loans sent to special assets at their extended maturity (REAL).

**Worth on the graded quantity.** The mortgage prepayment curve moves the mortgages' loss from 129.1 to 85.2 and the
designation from the mortgages to Agency MBS; the cover step moves the pool's loss from 19.6 (or 38.1 at the recent
share) to 150.0 and the designation to the pool.

**Strength.** P(one strong solver lands the pool and the $150 million bin) about 0.14: it must see that the balloons
due through 2027 decide the ranking (about 0.6), condition each balloon's extension on its refinance cover from the
history rather than on the 1.25 convention, the 1.00 rule, a share, the rate gap, the note-rate DSCR, the in-place
cover, the grade or a debt yield on the full history (about 0.3), and execute the cash flows on the bank's extension
terms and the average within $5 million (about 0.75); the guess routes that land (0.85 on every balloon, nine-tenths on
the 2027 balloons alone) add about 0.01. P(both top responses land) about 0.02 if independent, about 0.04 with a
correlation of 0.2, under 0.08 with margin. The seed was fixed by rule (the task number, then the memo's month and day:
1661214) before any data was generated and is never searched; the world's extension response, the book's origination
profile, the push's sizing and its interest-only share were chosen against criteria fixed before the search (every
construction above plus or minus one sigma in the bin's middle half, the named routes and every rival outside the bin,
the in-place and watch-list routes a full bin away, no listed share in either constant-share band, the ladder held),
and the golden was then re-centred by one rule written before any route was measured: the push loans' income scale is
solved so the file-built golden sits within $0.5 million of $150 million (1.491; the build gives 149.99).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the positions in each Schedule A pool at the close on 30 November 2026 | filed (policy section 3, Schedule A); SF1, SF8, SF11 to SF13 |
| 2 | Unit of account | each pool's averaged loss in dollars, reported in $ millions | filed (policy, prompt); SF14 |
| 3 | Attribution window | the month-ends of the overlay's first twelve months: January to December 2027 | filed (the prompt's start, 4 January, and the policy); SF4 asserted |
| 4 | As-of dating | positions at 30 November 2026, files pulled 3 December 2026 | filed (prompt, extract notes); statements to 30 November or 3 December the same figure (asserted) |
| 5 | Version basis | ALCO's September 2026 planning cycle | filed (policy: the most recent cycle); SF10 |
| 6 | Denominator | none: a loss in dollars | n/a |
| 7 | Weighting | the mean of twelve month-end losses, equal weights | filed (policy "averaged") |
| 8 | Window length | the extension history the model is fitted on | C3: every maturity since 2015 or since 2023 the same bin (asserted) |
| 9 | Boundary inclusivity | cash flows after each month-end; eligibility at least the notional | filed (policy) |
| 10 | Rounding path | the unrounded average to the nearest $10 million | filed (prompt); SF14 |
| 11 | Tie-break | none: the margin is 1.36x | n/a |
| 12 | Maturity and censoring | the balloons due after the as-of are unresolved; their extension is the forecast; a loan already extended is not extended again | the decisive step itself (open, forced by the hold-out); SF20 filed |
| 13 | Order of operations | each pool's cash flows, the measure per month-end, the mean | filed (policy) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | the loans converted in August 2024 appear in both servicing extracts on their own cycles only | C1: the xref joins them; no cycle is in both extracts (asserted) |
| 16 | Identity normalisation | legacy loan numbers to loan ids; obligation and property numbers to the loan file's | the xref and the formats in the extract notes; C1 (every log row joins its statements, asserted) |
| 17 | Netting against gross | none on the call | n/a |
| 18 | Dimensional units | the custodian's thousands; rates in per cent and decimals | the extract notes; R2 asserted |
| 19 | Code and status semantics | five outcome codes in two layouts (PO, EXT, EXT-S, PO-EXT, SA); servicing status and zero-balance codes | the extract notes; SF22 and R2 asserted |
| 20 | Integerisation | none before the rounding | the golden within $0.5 million of the bin's centre, every construction in the middle half with one sigma (asserted) |
| 21 | Clause scope | the policy's measure applies to every Schedule A pool | filed |
| 22 | Forward window contents | each pool's behaviour through 2027 and beyond under the base case | forecast from the records (the decisive step and its rungs) |

## Literal reader
Executing the prompt and the hedging policy word for word gives each Schedule A pool's loss in economic value under a
200 bp parallel rise of the September 2026 planning cycle's base-case zero curve, the same zero rates at every
month-end, on the base-case expected cash flows before credit losses of the positions held at the close on 30 November
2026, averaged over the month-ends of the overlay's first twelve months, 31 January to 31 December 2027 (it starts on
4 January), the largest designated and its figure given to the nearest $10 million; no shipped sentence says how fast
any pool prepays or which balloons extend (the extract notes file the terms of the bank's one extension, never when a
loan takes it), so a literal reader must forecast them; the easy method on the same
literal estimand (the mortgages on a prepayment curve at 6.25 per cent, the balloons at the log's recent extension
share) files Agency MBS at $110 million, and the fork table leaves no reading under which a lower rung is the golden.

## Oracles

- The maturity log's outcomes (2015 to 2026): closed outcomes every route reads alike; on the wrong path they supply
  the recent share; only the analyst's own hold-out separates the conditionings, and no shipped figure scores them.
- The servicing history and the agency factors: read alike by every route.
- The third-quarter ALM report: the bank's EVE and NII against limits at 30 September, consistent with every route; it
  carries no pool and no programme figure, and its credit quality line (the CRE book's watch-list share, 7.4 per cent)
  is the loan file's grades summed, which the watch-list route reads and misses with (32.9).
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
What stage 4 round 2 leaves standing, as measured (every figure asserted in checks.py):
- The nearest routes outside the bin: the 1.25 cover convention files 157.7 (2.7 above the bin's top) and the 1.00
  rule 141.5 (3.5 below its foot); with one sigma at 0.77 both stay out, and both score worse on the hold-out than the
  cover logit (Brier 0.2007 and 0.0401 against 0.0126), so a solver who validates drops them.
- The income routes. The debt yield fitted on every maturity names the pool at $136.0 million (the $140 million bin,
  hold-out 0.0389); fitted on 2023 onward it files $149.2 million, the golden's bin and a family member: on the 2023 to
  2026 maturities the refinance rates sit near the planning rate's level, so the debt yield there is the cover up to a
  constant. An income-based extension model is the decisive insight in either form; the rate adjustment separates the
  two only on the full history. The note-rate DSCR names Agency MBS fitted either way (52.4 and 65.5).
- The in-place and watch-list routes. In-place cover and the risk grade run on the current payment, refinance cover on
  the balloon at the planning rate: the push's interest-only loans (128 of the pool's 360, $1.85 billion) carry
  in-place cover near 1.8 and refinance cover near 0.8, the later high-coupon loans in-place cover near 1.2 and
  refinance cover above 1.3. Extending below an in-place cover of 1.20 or 1.25 files 75.3 and 77.7 and the watch list
  (grade 6 or worse) 32.9, each naming Agency MBS.
- Two natural shares land: 0.85 on every balloon not yet extended (151.3), and nine-tenths on the 2027 balloons alone
  (148.6, the wall's own model share being 0.909), because the extension effect per balloon dollar is near uniform, so
  a guess that falls on the wall's share lands; every other listed share misses either way (BYPASS).
- The extended loans: 32 loans ($169.4 million) are on their one extension; extended again on cover they would file
  152.7, the same bin, and the extract notes file that they are not (SF20).
- The mortgages' own loss moves with the stitching (85.7 on the new platform's months alone, 65.2 with the
  held-for-sale deliveries counted as payoffs) and is never above Agency MBS; the call never rests on it (the cover
  step with last year's mortgage speed still names the pool, 1.16x).
- Rung 0's margin is 1.17x (the mortgages at last year's speed against Agency MBS). A wrong answer either way.
- Every agency pool in the account read as the MBS pool: 124.8, still 1.20x under the golden.
- The book: fixed-rate originations run 40 to 53 a year to 2017, 73 in 2018, 107 in 2019, 70 in 2020, 234 in 2021 and
  229 in 2022 (nearly all before May), then 7, 11, 4 and 5 a year as new lending moved to floating rate (68, 62, 67 and
  75 floating loans a year). The push of December 2021 to April 2022 is $3.04 billion of the $3.64 billion fixed-rate
  pool (243 of 360 loans), half of it interest only; $3.21 billion of balloons not yet extended fall due by December
  2027 (277 loans), 8.4 per cent of total assets of $38.06 billion. The ALM report's commercial real estate line
  carries $5.28 billion with the floating-rate book, and its credit quality line puts grades 6 to 8 at 7.4 per cent of
  that book and grades 7 and 8 at 3.0 per cent, the loan file's own grades.
- The history's exceptions: 739 payoffs, 41 extensions, 4 six-month extensions for a sale, 11 payoffs at an extended
  maturity and 2 loans sent to special assets there; 2 loans paid below the fitted break (cover 1.03 and 1.08) and 6
  extended above it; every loan below a cover of 1.0 extended (23 of 23) and 3 of 92 between 1.12 and 1.25 (REAL).
- The fingerprint heart gate: WARN (`repeat.question_form`, answered at the draw); the ban window is task163, task245
  and task471. `guard.py surface` now promotes task167 back to back (decisive pattern E and the close_out_summary
  context artifact on both cards): task167's v2 card was registered at 06:59:01Z, after this card (05:26:01Z), so the
  repeat sits in the later draw's window, and nothing on this card moved for it.

## Leak sweep
`leak.py task166 --asof 2026-12-03` returns REVIEW (no LEAK); every line answered:
- Sweep 2, `ladder` in the policy: the Treasury ladder is the pool's own name, declared under `field_terms`.
- Sweep 3, the call's words in the policy, the extract notes and the ALM report (overlay, fixed-rate, commercial real
  estate, pool): the policy names the pools it governs and the notes the files; none states a loss, ranks a pool or
  names the designation.
- Sweep 4, design-note vocabulary in the policy (maturity, agency, mortgages, planning, recent, credit), the notes
  (extension, maturity, agency, planning, extended, servicing) and the ALM report (mortgages, credit, twelve, balance,
  estate): the files' own subjects. The notes file the bank's extension terms (one extension, 36 months, a tenth paid
  down, the posted rate, 25-year amortization) as the credit file's practice; no file names refinance cover, a debt
  constant, a debt yield or what decides whether a loan is extended (asserted in checks.py, R3c).
- Sweep 9, dates after the pull: records that carry future dates by nature (loan and swap maturities, next due dates,
  rate-lock expirations, the plan's months, amortization periods, the log's extended-to dates).
- Sweep 10: INFO only (the audit reports no writer signature).

## Surface screen
`guard.py surface task166` exits 0 and promotes eight pairs for the author's adjudicated `/clone-check`: task167 back to
back (decisive pattern E and the close_out_summary context artifact; task167's v2 card registered after this one, its
gap population, decision a quantity figure, domain grant making, no file name, schema or invented name shared), and
task155, task37, task117, task137, task44, task97 and task197, every one the card-level signature differentiated at
the draw (decisive gap time and pattern E with Gate G forecasting, or the decision family), none sharing a file name,
schema, same-seed table or invented name. Before the first cut it promoted task133 on a prompt construction the two
prompts shared ("i also need two slides for"); the deck sentence was rewritten and the pair dropped out.

## Build record
Stage 3, 2026-10-18; rebuilt after stage 4 round 1 and again after round 2 the same day. `build.py`: checks 110 run, 0
failed (the three-rules block R1 to R3c on the generator's clean truth, every SF row SF1 to SF22, the ladder and its
grid, the golden family of 18 constructions with their hold-out scores and the bootstrap, the data-chosen cuts, the
misread code, the routes kept outside with the in-place and watch-list routes a full bin away, the constant-share
bands, the out-of-sample choice, the history's exceptions, the ask's devices, the separation line, the distractors'
deletion, the input gates and the realism sweep); `verify.py` (pandas, no generator import, every format read with a
positive control, the extension terms recomputed) 14 passed, 0 failed; two consecutive builds byte-identical (target,
golden, figures.json); `figures_check.py` 51 figures, 0 absent; `precut.py` PASS; `voice-check.py` PASS (938
characters); H1 audit clean on the pack and the goldens; `leak.py` REVIEW, no LEAK; `guard.py validate` clean,
`surface` exit 0, `heart` WARN (Residual); `cracker.py` on a fresh unzip of target.zip: pair ceiling 38.8, mirror
leakage 18.8 per cent. 20 files in 4 formats, the largest the servicing extract at 116,277 rows; distractors
`deposit_decay_study_2026.xlsx` and `mortgage_lock_pipeline_20261130.csv`. Invented names searched: Carrick Valley
Bancorp and Carrick Valley Bank (no bank of that name), the dealers Halvorsen Markets, Pemberly Securities, Corvane
Bank NA, Ostrander Securities and Larkmoor Capital Markets (no firm of those names; Redfern Capital Markets was
renamed, a letter from a real Florida real estate investor); personas from `guard.py names`.

Round 1 rework (the judge DETERMINISTIC, APPROVE; the reader no leak; the rule 3 audit PASS but tighter): the
extension response sharpened, the push written half as cash-out deals at full proceeds on pro forma rents and half as
lower-leverage refinances, the bin cut to $10 million, the overlay's start filed in the prompt, the ALM report's CRE
line moved with the book; the extract notes now say Hedged item is what the swap is designated against and
client_trade_ref is the trade number the bank gave the broker when it submitted the trade for clearing (the two facts
that settle Ask A's devices); the goldens' and the write-up's dates are the prompt's.

Round 2 rework (110523a5: the judge DETERMINISTIC, APPROVE, reproducing CRE 150.7 and MBS 110.5; the reader no leak;
the rule 3 recheck PASS with P(one) 0.13 to 0.15; realism AT_RISK and one fork unfiled), in one rebuild: the bank's one
extension filed as a plain fact in the extract notes with its terms (36 months, a tenth of the principal due paid
down, the posted five-year rate on the maturity date, 25-year amortization) and the cash flows recomputed on them (SF20,
SF21); six-month sale extensions (EXT-S) and transfers to special assets (SA) added to the log's codes with payoffs
below the break and extensions above it (SF22, REAL); the origination history ramped through 2020 to 2022 with fixed-
rate lending slowing to a handful a year after April 2022 and the floating-rate book growing; total assets raised to
$38.06 billion so the wall is 8.4 per cent of them; half the push written interest only for its whole term and grades
set on in-place cover with the officer's adjustment, so in-place cover and grade part from refinance cover (the in-place
and watch-list routes now a full bin away, OUT); the watch-list share brought to 7.4 per cent and given a line in the
ALM report; the golden re-centred by the rule (149.99); every construction plus or minus one sigma inside 147.5 to
152.5 at $10 million, no loosening needed.

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
- A soft extension response (a logistic scale of 0.05 in cover) with the push's balloons spread across the break, at
  stage 4 round 1: a data-chosen hard cut at 1.18 to 1.20 scored the best hold-out Brier and filed 160 to 161, and a
  constant share of 0.68 to 0.83 on every balloon landed the $150 million bin (0.75 gave 149.3); the $25 million bin
  could not narrow that band. Rebuilt with a sharp break near a cover of 1.10, half the push written as lower-leverage
  refinances, the bin cut to $10 million and the overlay's start filed in the prompt (a spot start would move the
  twelve month-ends and the figure to $160 million).
- Keeping the wall's extension share near four-fifths with a finer bin: the every-balloon guess band still held
  three-quarters, and the later balloons needed to separate the two bands raised the contractual loss and the
  note-rate DSCR rival past R2c's 1.2x margin.
- A $5 million bin: every construction would have to agree within $1.25 million, which no cover mix of the wall held
  against the bands and the debt yield since 2023.
- More seven-year 2021 loans to widen the gap between the two constant-share bands: the note-rate DSCR fitted on 2023
  onward moved into the bin (145 to 148) and R2c past 1.2x.
- Repaying the already-extended loans at their extended date with the practice stated only in the write-up, at stage 4
  round 2: the cover model run on their current maturities gave 156.1 on that pack, so the reading was an open fork;
  the bank's one extension is now filed in the extract notes with its terms, and the second extension (152.7 on this
  book) is asserted as the alternative.
- An extension on the note's rate and payment with nothing paid down (round 1's terms), at stage 4 round 2: no bank
  extends a five-year balloon three years on unchanged terms; the filed terms are a tenth paid down, the posted
  five-year rate on the maturity date and 25-year amortization, and on this book the old terms would file 159.9 (SF21).
- A break at a cover of 1.05: the 1.00 rule came within $7 million of the golden in half the lab draws and the
  bootstrap sigma ran 1.4 to 1.9 in the median draw; at 1.12 the 1.25 convention came within $7 million in most draws;
  the break was set at 1.08.
- A softer extension response (a logistic scale of 0.03 in cover, for a more gradual book): the 1.25 convention moved
  to within $5 million of the golden and, with the break at 1.10, the sigma rose to 1.4; kept at 0.025.
- Interest-only on a third of the push: the bootstrap sigma rose to 1.8 in the median lab draw, the family's plus or
  minus one sigma out of the middle half; interest only for the first 24 months and amortizing after left in-place
  cover too close to refinance cover; half the push interest only for its whole term puts the in-place and watch-list
  routes 72 to 117 below the golden.
- A larger later fixed-rate book (1.5 then 1.0 loans a month after 2022, or a quarter to a third of it on seven- and
  ten-year terms): the balloons-repaid loss rose to $42 to $44 million and the sigma to 1.5 to 1.9 in the median draw,
  the later balloons' extension adding model spread outside the wall; the later book was cut to a handful of five-year
  loans a year, new lending moved to floating rate.
- Total assets held at $31.15 billion: the 2027 wall would be 10.3 per cent of the balance sheet falling due in one
  year; raised to $38.06 billion (8.4 per cent), C&I taking up the rest, the EVE figures unchanged.
