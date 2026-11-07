# task306 design note

## Draw

1. Card: `.claude/skills/fingerprint/cards/task306.json`, architecture 4, registered 2026-10-31 after a pull; the
   three earlier architectures sit in the card's lineage as spent.
2. Pairing: Quantitative Finance, task type portfolio-construction-risk, objective Opportunity Sizing & Decision
   Support (the headline is the alpha a year each strategy keeps at the size it would be given, pool to realisable,
   and the larger keeps the money); shape other (three candidates each with a gross alpha, a cost at size and a net,
   the call, the runner-up and the gap, a chart, and two asks on the desk's own 2026 trading).
3. World: Wealdmoor Investment Management, a London asset manager whose systematic equity desk runs four live UK
   strategies and has three more backtested; its brokers Orchard Lane Securities, Calder Row Brokers, Brightwater
   Execution and Hythe Street Markets. People from `guard.py names --geo "United Kingdom" --seed 306`: Howard Simpson
   (chief investment officer, chairs the investment committee and sends the request), Carole Shaw (head of
   systematic equities), Sarah Ford (head of trading, owns transaction cost analysis).
4. Quantity: for each backtested strategy, its expected alpha a year in pounds at GBP 400 million, the backtest's
   gross alpha less the cost its 2026 rebalances would pay traded at that size; the call is which strategy takes the
   money from 4 January 2027.
5. Default path: each strategy's 2026 turnover priced at what the desk's own orders paid per traded pound in stocks of
   the same size (or a flat research cost), the field's back-of-envelope capacity check, which leaves small-cap
   momentum first on its gross lead.
6. Data-native sentence: the desk's orders carry each order's size and the stock's daily traded value, so the cost of
   an order rises with its share of that value along a curve the executions trace; the desk's small-cap and mid-cap
   pounds traded sat at about one per cent of a stock's day at the median, their larger shares coming in thin names
   where an ordinary order is much of the day, while at GBP 400 million momentum's month-end trades take about 30 per cent of each liquid
   small cap's day at the median pound, a scale the desk's average cost never weighted.
7. Against task310 (an added store's yield behind a site's send-out limit), task106 (candidates sharing one pool of
   spare capacity), task309 (one effect ratio carried across an intensity range) and task83 (a capped budget ranked by
   a randomized holdout's effect): here one candidate is funded whole and the carried quantity is a cost per traded
   pound that rises smoothly with the trade's share of the stock's day, fitted on the desk's own executions (the
   card's differentiation lines).
8. Furniture: forum committee_or_panel (the investment committee), forcing launch_or_rollout (the strategy goes live
   on 4 January 2027), org financial_institution, role portfolio_manager; none is banned against the last three
   builds (task181, task474, task125).
9. Prompt shell: a which question (what alpha each keeps, and which should take it), the second sentence opening
   "The", the rounding sentence opening "Alpha"; the dead architecture's how-much shell is not kept;
   deliverables pptx and xlsx.
10. Guard WARN people.first answered: Carole and Sarah each appear in one older build (task105, task108); both are the
   drawn personas for this seed and no other persona in the pack shares their names.

## Default path

1. Read IC-07: alpha at a size is the backtest's annualised gross alpha less the shortfall the twelve months of
   rebalances would pay at that size, estimated from the desk's own executions.
2. Conform the desk's orders (each execution id once, pounds fills as pence, the failover orders merged, shortfall
   from arrival, cost positive) and read what they paid in the band each candidate trades, as IC-07 files it: the
   value-weighted shortfall per band, about 33 basis points for the large caps, 37 for the FTSE 250 and 61 for the
   small caps.
3. Scale each candidate's traded weights to GBP 400 million and price every pound traded at its band's average, the
   field's capacity check done on the desk's record.
4. Net it from gross alpha: UK Smaller Companies Momentum keeps about GBP 13 million, UK Mid Cap Value 10, UK Large Cap
   Quality 6.

Ends on: UK Smaller Companies Momentum
Golden: UK Mid Cap Value

## Stump sentence

The default path prices each candidate's twelve months of rebalances at GBP 400 million at what the desk's own orders
paid per traded pound in the same band and gives the money to UK Smaller Companies Momentum; the step that lands it
there is carrying the desk's average cost to trades of a new size, when the executions show shortfall rising with the
square root of each order's share of the stock's daily traded value and at GBP 400 million momentum's month-end swaps
take a fifth to two fifths of each small cap's day, so it keeps about GBP 5 million against UK Mid Cap Value's 8.

## Three rules

Task type: portfolio-construction-risk (Quantitative Finance), which serves Opportunity Sizing & Decision Support: the headline is the alpha a year each candidate keeps at the capital it would be given, the pool its gross alpha and the realisable part what survives its own trading.
Domain test: the quantity that decides is each candidate's alpha net of the market impact its rebalances pay at GBP 400 million, which systematic equity estimates from the desk's transaction cost analysis, cost per order rising with its share of the stock's daily volume; with another field's nouns there is no participation, no arrival-mid shortfall and nothing that makes a trade dearer per pound as it grows.
Swap: "Which charity should receive the bequest, sized by the beneficiaries it reaches?" reads differently, because a grant's cost per beneficiary does not rise with the size of the cheque against what a market absorbs in a day; put megawatt-hours in and there is no stock whose daily traded value prices the trade.
Layer 1: the OMS export as the desk's systems write it: fills re-sent after the 9 June outage under the same execution ids, one broker reporting pounds where the rest report pence, orders the backup re-created after each failover under new ids, block orders on the desk's block account with a separate allocation export, cancelled orders with unfilled remainders, UTC stamps against London trade dates, a reused account code, SEDOL in the market data against ISIN in the backtest log, share consolidations in the market data; each is produced by the system that records it and none is placed to be caught.
Layer 2: estimation_fit, the shortfall curve in trade size: the desk's executions trace cost against each order's share of the stock's day, and the comparison is decided by reading that curve at the participation each candidate's rebalances would have at GBP 400 million.
Decisive step: pricing each rebalance trade at the cost the executions show for an order of its own share of the stock's day, rather than at what the desk paid on average for its own, far smaller orders.
Not semantics: every field read right (participation, arrival mid, shortfall sign, the bands) still leaves the band averages, which are correct figures for the desk's own orders and say nothing about orders ten to forty times larger; no column holds a trade's cost at a size the desk never traded.
Not rule application: IC-07 files the estimand and the TCA standard the measures, and neither says how cost depends on size; executing every filed rule with each band's average cost files momentum, and only the shape of cost against participation in the executions, which no sentence states, moves the money.
Analyst test: a strong analyst conforms every fill, reads IC-07 and the TCA standard correctly, prices each candidate's rebalances at GBP 400 million at the desk's value-weighted shortfall for that band and gives the money to UK Smaller Companies Momentum at about GBP 13 million kept; every field is read and every rule executed, and the call is wrong because momentum's trades at that size sit far up a cost curve the desk's average never reached.
Estimand: ic_capital_allocation_policy_2026.pdf section 2 with tca_standard_rev4.pdf sections 1 to 3: population, the candidates in Research's workbook; outcome, alpha a year at GBP 400 million, the annualised gross alpha 2015 to 2026 less the implementation shortfall of the rebalances of the twelve months to 30 November 2026 scaled to GBP 400 million and traded in full on each rebalance day; unit, pounds a year; comparison, the largest.
No decoy: nothing is planted to be caught; no memo, research note or broker estimate argues the band average, the commission schedule and the ESG list are context, and the backtest workbook carries gross alpha only.
No certified replay: no certified or published figure reproduces the method; no file carries a cost estimate for any candidate, a capacity figure or a ranking.
Lesson: what a strategy keeps depends on the size it runs at, because a trade's cost rises with its share of the stock's daily volume; a model that learns to read the desk's own cost curve at the size being decided, not at the size it has traded, sizes capacity the way the field does, which no build on file teaches.

## Survivor anatomy

Actor: the deciding property, what a trade of a given size would cost, has no column; the orders carry their own participation and shortfall, the candidates' trades carry only a weight, and the property is the relation between the two that the executions trace and the candidates' trades sit far beyond on average.
Link: no key ties a candidate's trade to any execution; the comparison that prices it (the desk's orders binned or fitted on participation, read at the trade's own participation on the rebalance date) is one the band-average capacity check never asks for, and no sentence invites it.
Reflex: the field's back-of-envelope capacity check, turnover times the desk's average realised cost, is rung 0 and files UK Smaller Companies Momentum.
Back-test: the textbook route validates: on the desk's own orders the band average reproduces each book's realised 2026 shortfall almost exactly, because those orders sit where the average was measured.
Second use: every file the decisive step reads has its own reason to be in the pack: the fills and orders carry the year's TCA report (both asks), the market data the participation the standard defines, the trade log the candidates' rebalances.
Shock: momentum's gross alpha is the largest by GBP 8 million and its trades are the desk's most familiar kind; the golden is not an interval of any sort of the candidates by gross alpha, turnover, band or holdings, asserted in checks.py (C2 and R0).
Pins: the WHAT sits in IC-07 (gross alpha, the twelve months of rebalances, the size, traded in full on the day, the desk's executions in the candidate's index band as the population a cost is estimated from, commissions and the launch build outside) and the TCA standard (shortfall, value, participation, volatility, the consolidation day that gives no return, the 60 sessions of history); no filed sentence names how cost grows with size, a square root, impact or capacity (R1).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 turnover at a flat research cost | none | the trade log's weights | the backtest habit | none | none | one product | yes | readable |
| R1 turnover at the desk's average shortfall per band | IC-07 names the desk's executions | the TCA columns | the field's capacity check | the desk's own books reproduce it | the battery cleans the fills | one product | yes | readable |
| R2 R1 with the orders' average per order, not per pound | none | the TCA columns | a TCA summary | none | none | one product | yes | readable |
| R3 (decisive) each trade priced at its own participation on the executions' cost curve | none names size, a curve, impact or a square root | no column holds a trade's cost at a new size | not the capacity reflex | no file prices any candidate | the battery stops at clean orders | not affine in any shipped column | the files carry the asks | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | participation's daily traded value | 20 sessions before the trade date | 60 sessions | same call and rounded figures (asserted) | TCA standard section 3 |
| SF2 | daily volatility | 60 sessions before | 250 sessions | same call and rounded figures (asserted) | TCA standard section 3 |
| SF3 | the cost curve's form and weighting | least squares, band by band, on daily volatility times the square root of participation | participation to the 0.4 to 0.7, without the volatility term, value-weighted, the exponent fitted per band, binned | same call, runner-up, gap and rounded figures under every member (asserted, C2, C3 and C7); band by band each alpha stays at least 0.25 inside its million (C8); a fit through the origin keeps the call, runner-up and gap and moves momentum's kept alpha to 4 (the re-judge's one open member, rejected by the fit) | convergence: the desk's small-cap and mid-cap orders reach a fifth to two thirds of a thin name's day, so the executions trace the curve across the participation the candidates trade at |
| SF4 | the failover orders in the fit | merged into their originals | left as separate orders | same call and rounded figures (asserted) | TCA standard section 1 |
| SF5 | re-sent fills in the fit | each execution id once | kept twice | same call and rounded figures (asserted) | TCA standard section 1 |
| SF6 | a pounds fill | times 100 into pence | read as pence | shortfalls of minus 10,000 bps show at once (asserted) | the fill's price unit and TCA standard section 1 |
| SF7 | expected gross alpha | the Summary's annualised figure | the annual alphas compounded or averaged | the annual alphas compound to it (asserted) | IC-07 section 2 |
| SF8 | the rebalances priced | the twelve months to 30 November 2026: twelve monthly, four quarterly | calendar 2026 or the whole log | not the filed window (asserted twelve and four) | IC-07 section 2 |
| SF9 | what the cost of trading excludes | commissions and the launch build | either included | not the filed estimand | IC-07 section 2 (asserted) |
| SF10 | shortfall, value, a block's owners and a portfolio's orders | arrival mid, filled quantity at arrival, the allocation export, the dated register | fill value, order quantity, the blotter's account | moves the asks only | TCA standard sections 1, 2 and 4 (asserted) |
| SF11 | the executions a candidate's cost is estimated from | the desk's executions in stocks of the candidate's index band | one curve pooled over the bands | with an intercept per band, same call and rounded figures (asserted, C7); with one intercept for all bands the figures move, since the half-spread differs by band | IC-07 section 2 (asserted, SF9) |
| SF12 | the consolidation day in the volatility | no return | the history before it adjusted, or the tenfold change left as a return | same call and rounded figures under both (asserted, C7): only the least liquid small caps, which no book or candidate trades, consolidate | TCA standard section 3 (asserted, SF10) |
| SF13 | an order without 60 sessions of history | measured only once 60 sessions exist | measured on fewer | none exists: the books' orders begin on 1 April 2025, the 64th session (asserted) | TCA standard section 3 (asserted, SF10) |
| SF14 | the ESG list against the rebalance log | inert: every exclusion took effect before the log and the orders begin | the excluded names dropped from the rebalances | no rebalance trade is in an excluded name (asserted), so dropping changes nothing (C7) | the list's own effective dates |
| SF15 | the Severnvale transition's and the block account's orders in the fit | kept: the desk's own executions | dropped | same call and rounded figures (asserted, C7) | IC-07 section 2 |
| SF16 | orders cancelled part filled, in the fit | kept for the quantity they filled | dropped | same call and rounded figures (asserted, C7) | TCA standard section 2 |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | gross alpha less turnover at a flat 10 basis points | UK Smaller Companies Momentum (GBP 19 million kept) | IC-07 sends the cost to the desk's executions |
| 1 | gross alpha less turnover at the desk's value-weighted shortfall per band | UK Smaller Companies Momentum (about 13, against 10 and 6) | the desk's pounds sat where the average was measured; at GBP 400 million momentum's swaps take a fifth to two fifths of each small cap's day |
| 2 | rung 1 with the per-order average | UK Smaller Companies Momentum (13, against 11 and 7) | the same fact: the desk's orders are mostly small |
| 3 (decisive) | each trade at the cost the executions show for its own participation | UK Mid Cap Value (8), UK Large Cap Quality (6), momentum (5) | the golden |

- **Margins on the cut pack** (asserted in checks.py): the golden keeps 4.90 (momentum), 7.99 (UK Mid Cap Value) and
  5.90 (UK Large Cap Quality), a gap of 2.08. Across the 31-member fit family (C7: participation to the 0.4 to 0.7,
  with and without the volatility term, band by band and pooled with an intercept per band, unweighted and
  value-weighted, without the transition, the block account or the cancelled orders, either consolidation reading,
  the ESG names dropped) band by band momentum keeps 4.79 to 5.24, UK Mid Cap Value 7.97 to 8.07 and UK Large Cap
  Quality 5.85 to 6.03, each at least 0.25 inside its whole million (C8); the pooled fits widen that to 4.74 and 6.14,
  still 0.2 inside. The fitted power, the binned reading, 60-session participation, 250-session volatility and the
  fit without the failover merge or with the re-sent fills round to the same figures (C3, SF1 to SF5). The size-blind
  routes file momentum by 2.4 to 7.4 million (R0). The one member outside the family, recorded at the re-judge: a
  curve fitted through the origin (no half-spread) keeps the call, the runner-up and the gap but puts momentum at
  3.64, so its kept alpha rounds to 4 against the golden's 5; the executions reject it (the small-cap band's fit
  explains 0.77 of the shortfall's variance with the intercept against 0.68 without), and naming the curve's form
  would file the method.
- **Pricing sequence.** (1) The residue the filed WHAT leaves is how cost depends on size, a method, not a knob. (2)
  Momentum has to fall from about 13 kept to under 6; at GBP 400 million its pounds trade at a fifth to two fifths of
  the day, where the executions price them at about twice the band average (126 basis points against 61). (3) The one-group-by route (cost by
  band) ranks the books' realised costs correctly and misprices the candidates; no route is affine in a shipped
  column. (4) Across the fit family momentum spreads 4.74 to 5.24, mid caps 7.97 to 8.07; the gap of 2 million to
  the runner-up holds under every member (raw 1.86 to 2.22). (5) and (6) No variance is corrected. (7) No subset of rows prints a
  candidate's cost. (8) The reflex sweep runs as code (checks.py R0, C2 and C3).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the candidates in Research's workbook; each one's cost estimated from the desk's executions in its index band | filed (IC-07 sections 1 and 2); SF11 |
| 2 Unit of account | pounds of alpha a year at GBP 400 million | filed (IC-07 section 2) |
| 3 Attribution window | the rebalances of 1 December 2025 to 30 November 2026 | filed (IC-07 section 2); SF8 |
| 4 As-of dating | each trade's participation and volatility on its rebalance date, the consolidation day giving no return, 60 sessions of history | filed (TCA standard section 3); SF1, SF2, SF12, SF13 |
| 5 Version basis | the trade log as Research cut it; the OMS export of 1 December 2026 | one version shipped |
| 6 Denominator | the GBP 400 million for alpha; arrival value for shortfall | filed |
| 7 Weighting | shortfall value-weighted at arrival; the curve's own weighting left open and converging | filed (TCA standard section 2); SF3 (C7) |
| 8 Window length | twelve months of rebalances | filed |
| 9 Boundary inclusivity | 1 December 2025 and 30 November 2026 both inside | filed; no rebalance near either edge |
| 10 Rounding path | each figure rounded once from unrounded pounds; the gap from the rounded figures | C1; mid-bin asserted (C4) |
| 11 Tie-break | none needed: the margins exceed 1.2 million | C2 |
| 12 Maturity and censoring | none: the orders are complete fills to the export | C1 |
| 13 Order of operations | conform, size, fit, price, net | C1 (SF4, SF5) |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | each execution id once | filed (TCA standard section 1); SF5 |
| 16 Identity normalisation | ISIN to SEDOL through the security master | the systems' own keys |
| 17 Netting against gross | buys and sells both cost, signed so a cost is positive | filed (TCA standard section 2) |
| 18 Dimensional units | pence in the market data and fills, pounds where a fill says so | filed; SF6 |
| 19 Code and status semantics | TERMINATED, BACKUP-RECOVERY, CANCELLED, the block account | filed (TCA standard section 1) |
| 20 Integerisation | none: pounds | C1 |
| 21 Clause scope | IC-07's commissions and launch exclusions bind the call only | filed scope |
| 22 Forward window contents | the twelve months of 2026 rebalances stand for a year of trading from 4 January 2027 | filed (IC-07 section 2) |

## Literal reader

Executed word for word, IC-07 takes each candidate's annualised gross alpha from the workbook, scales the trade log's
weights for the twelve months to 30 November 2026 to GBP 400 million and asks what implementation shortfall those
trades would pay, traded in full on each rebalance day, estimated from the desk's executions in the candidate's index
band; the TCA standard defines shortfall, value, participation and volatility, the consolidation day and the history
it is measured on. A literal reader fitting cost on participation, the standard's own measure, files
the golden; the band average is a reading of the executions that ignores the measure the standard defines.

## Oracles

None on the main call: no file carries a cost estimate, capacity figure or ranking for any candidate. The verifier
(generator/verify.py) recomputes the call, every figure and both asks with pandas from target/ alone.

## Ask sheet

Two asks on the desk's own 2026 trading, both from the OMS export the call reads for its curve, neither carrying the
call's decisive step.

**Ask A, each live strategy's implementation shortfall in each quarter of 2026 (16 figures, bps to one decimal).**
- Devices: the orders the backup re-created after each failover are the originals (TCA standard section 1), and
  nothing keys them; a block order belongs to its books by the allocation export.
- Hazards: re-sent fills, pounds fills, cancelled remainders, the dated register.

**Ask B, the value each live strategy traded in each half of 2026 (8 figures, whole GBP million).**
- Device: the block orders sit on the desk's block account in the blotter and reach each book only through the
  post-trade allocation export.
- Hazards: the same battery; the reused account code.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| A, 16 quarter shortfalls | measures each re-created order from its own arrival and leaves the blocks on the block account | miss |
| B, 8 half-year traded values | leaves the blocks on the block account | miss |

Pair ceiling: 28.5 ((38 + 7 + 55 x 0) and (5 + 7 + 55 x 0), averaged)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack, target.zip 7f2aba02)

## Leak review

`leak.py task306 --asof 2026-12-01` on target.zip 7f2aba02: REVIEW, no LEAK; each line ruled.
- Sweep 1, the backtest workbook's Notes sheet: harmless; it defines gross alpha, says the ESG list is applied and
  names its preparer, and describes no file or column.
- Sweep 4 on IC-07 (executions, candidate, rebalances, standard, outside) and on the TCA standard (orders, average,
  participation, standard, register): harmless; they are each document's own nouns for its estimand and measures, and
  neither says how cost depends on size (R1). IC-07's population sentence (the desk's executions in the candidate's
  index band) is the grouping the band average itself uses, and the TCA standard's consolidation and history sentences
  are measurement conventions; none names a curve, a square root or impact.
- Sweep 6, the backtest workbook names the candidates beside numbers: harmless; it ranks them by gross alpha, the input
  IC-07 names, not by the alpha each keeps.
- INFO, the account register names the live books: their codes and dates, no figure.
- Sweep 11, the prompt gate's shell quota (WARN in voice-check.py, which passes): the corpus now holds the 'which'
  question form at 37 per cent of 196 prompts against a cap of 30, a quota other builds moved since this prompt was
  written; the prompt is left as built for the main thread to reword at the role level if it chooses.

## Pre-ship check

1. The three rules re-read against the built pack: the decisive step is the cost curve read at the candidates'
   participation, analytical; the mess is Layer 1 only and each piece is asserted not to move the call (SF4 to SF6).
2. Determinism: the WHAT filed in IC-07 (the band's executions) and the TCA standard (the consolidation day, the
   60-session history); every member of the 31-member fit family converges on the golden's call, runner-up, gap and
   whole millions (C7), band by band at least 0.25 inside each million (C8), and the distractors are inert (SF14).
3. Gates on the final cut: generator checks, the verifier, two byte-identical builds, figures_check.py, precut.py,
   voice-check.py, leak.py, guard.py surface and heart.

## Tried and rejected

- Pack 1 of the prototype (2026-10-24, seed 3061) hid each imported car's pack history before its Dutch registration (the log started at the Dutch registration), so a solver could not know an import's pack state and both probes repaired it differently (sonnet calibrated the imports down by 0.74, opus modelled the abroad replacements in expectation): a fork, not the stump. The log is now the OEMs' EU-wide record plus Voltwerk's own, and a car whose pack failed outside warranty abroad is scrapped there and never imported.
- The prototype's truth carried a scrappage and export rate that no file shows; the forecast now takes a car in use to stay in use through 2027, filed in the tooling plan.
- The first cut's imports arrived about six years old, inside the eight-year warranty, and moved the call by three per cent and one lot; the Mira city car is now the platform kept alive by old imports from abroad, as old cheap EVs are.
- A refurbished pack failing inside Voltwerk's two years was logged as an OEM warranty fit in the prototype (99 rows): fixed, a Voltwerk-warranty failure takes another refurbished pack under Voltwerk's cover.
- The first stage-2 world kept the Mira city car launched in 2014 with 520 imports a month and an eight-year warranty: its arrival stream still ramped through the replay windows, so the 6- and 24-month windows spread the Mira's forecast by 51 and the total straddled a hundred bin. The Mira is now launched in 2013 with a five-year warranty and a steeper wear-out, its stream flat over the last 36 months and its imports arriving as survivors on their original packs.
- An estimand counting only failures outside both warranties left out the packs Voltwerk itself replaces under its two-year warranty, which the line supplies too; the plan now counts every failure outside the OEM warranty.
- Grading each platform's forecast paid the wrong route: the register-only route files four of the five platforms' forecasts at the nearest hundred (only the Mira moves); the prompt grades the slots and the total.
- Ask B's re-keying first moved the naive share by under 0.1 point on the Volta hatch, the new ids passing at about the platform's own rate; the BMS is now replaced in seven reworks in ten and the line seed (31062, from 750 swept) keeps every platform's natural read and over-repair outside its bin on all three asks, worst golden edge 0.155 of a bin.
- The dealer rows of the replacement log first carried plates typed with dashes; a solver who joined without normalising them filed Mira 1,350 and Volta 1,000, so that mess could move the call (dataset-generation R2) and was cut: both sources now carry the register's own plate format.
- Ask C's first device, dock 2 setting its rejects aside without scanning them (absent from the intake export, present at the recycler without a core code), was landed 5 of 5 by the stage 4 reader: dock 2's zero rejects and the blank core codes sit on the path of anyone counting rejects, and the judge found the dock's practice stated in no file. Re-sited onto the grade's date (D2): the intake export carries each core's grade on 1 July 2026, so a core the line built on and scrapped reads AFGEKEURD, and only its work order in the MES shows it passed intake; every ask C figure is unchanged.
- The plan's "a car in use in the Netherlands is taken to stay in use through 2027" read to the stage 4 reader, and to the judge as its one soft spot, as freezing the register of 30 June 2026; the sentence now places the car in 2027 ("a car in use in the Netherlands in 2027 is taken to stay in use for the rest of the year"), the population the estimand already files, and names no import.
- The portal returned the build on determinism (both judges: Gates C, D and E, underspecified_objective, A, B and G passing): the plan as shipped named the register as its only source and its only dynamics clause was about exits, so both judges forecast the register of 30 June 2026 alone (3,448, 3,500 with a judge's renewals), and a judge also summed ask A's batch lines as written. Pinning the population to the register was refused (it makes the judges' answer the golden and spends the stump), and filing the projection (a twelfth a month at the trailing rate, mix and age) was refused (rule application, CLAUDE.md rule 3). Closed instead by the WHAT at authority: plan section 3 files the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027 (SF25) and one pack per car (SF26), the projection left open and forced by C1 over 144 projections, and the line notes file the lot stock rule for ask A (SF27); no graded or stated figure moved (freeze.py). The cost: that the later registrations are in the fleet is now readable, so the decisive rung keeps only what no sentence says, which of them fall due; the default path's answer is now the easy route's on the literal estimand (the later registrations carried as new cars).
- 2026-10-31, architecture 1 spent at the batch 1 triage: shipped 10-24 and reshipped 10-26 after the portal's determinism block, its isolated cold reader reproduced the call cell for cell (Volta 900, Kestrel 250, Plover 350, Mira 1,450, Tern 50, 3,800) and named the decisive step a procedure, since the repair's population sentence and the plan's pack-age sentence read together as the method; the surviving risk the note recorded was that conditioning a survival curve on survival to the as-of date is reflex reachable. Re-rooted in a new world rather than hardened.
- 2026-10-31, re-root screen before this draw: an actuarial reinsurance-capital draw (a county mutual's 2027 windstorm programme, the vendor's year loss table loaded storm by storm for demand surge read off the market's index loss) cleared `guard.py check` and was set aside unregistered, because task309 (FORTIFIED roofs, one cut ratio across storms that varies with gust intensity, carried through a vendor event set) is the same insight in the same domain; regression to the mean in a health-services pilot and a healthy-adopter uptake were set aside as general statistical mechanisms readers name unprompted (task308's screen of six); stale-priced returns in a portfolio's risk budget were set aside as task135's cross-day covariance.
- 2026-10-31, architecture 2 (the development corporation's 2027 inward investment award between a logistics hub on the city region's boundary and an inland food plant, the induced round read where each project's staff live) drawn, registered and spent at stage 2 before any data was cut: the survivor anatomy's Actor test failed on paper, since where the hub's staff live is one join from a column (a roster postcode against the postcode directory's local authority), and every honest way to ship it (a roster, a travel plan's postcode survey, a commuting flow for the depot's zone) is a column or a sentence that sends a solver to it; the IO world offered no relation between rows that carries the induced round's leak.
- 2026-10-31, architecture 3 first cut (an occurrence cover against an annual aggregate cover): the two covers' releases separated by about 1.12 times under every loading of the storms, so no costing of the record moved the call; redesigned at stage 2 into the second-event cover, buy or not, on the occurrence cover's retained band.
- 2026-10-31, the second-event cover on the 50th worst year alone, an upper layer above the occurrence cover and a tall tower from 12 to 60 million were each priced: the single year was noisy enough to flip on the seed, the upper layer's release was small and noisy, and the tower closed the gap between the cheap routes and the golden; the capital policy's average of the 50 worst years and the 7.5 million xs 4 million band were kept.
- 2026-10-31, the first record draw (seed 498): the ratio of totals over the later storms of each season landed the call (worth plus 0.13 million) with the golden's release, and the mean of ratios over the later storms of each year landed it too; a stormier physics with more trains a season made the rank routes buy harder, and shifting a year's first train to clear the year end left nine gaps of exactly 70 days and one inside the window corridor. The record is now drawn with trains kept apart across the year end and searched over 7,500 seeds for one where every rank, year, season, size and pooled route under every estimator files the wrong call (seed 2703, worst route minus 0.06 million).
- 2026-10-31, an exposure ask on the home book (sums insured in force by county) was set aside: in-force by date, renewal terms under new numbers and lapses are rule application a careful solver executes, with no reconstruction left after noticing; the home extract ships as a distractor and the farm book carries the exposure ask.
- 2026-10-31, a reopened claim's further damage first came to some claims before they had been notified, which no claims system allows and which left the pairing of lines and instructions unrecoverable for those claims; further damage now comes only to a claim already open with its adjuster instructed.
- 2026-10-31, architecture 3 (Penwarden's second-event windstorm cover for the county mutual) spent at stage 4: the FIX_NOW failed its second pass. Pass 1 (DETERMINISTIC, FIX_NOW) found "worth" in two senses, cover B's one reinstatement missing from the working and the coinsurance share unpinned, all fixed; pass 2 (DETERMINISTIC, FIX_NOW) found the 2026 storms asks open, since 379 reopened /R1 claim lines with no instruction of their own took their original claim's instructed damage day in the golden, a rule filed nowhere, and the lines' own loss_date filed a recovery of 11,881,000 against 12,015,000. The main call (follow-on storms costing 1.62 times the model) held throughout. The lesson carried forward: a reopened, re-sent or amended record's date or owner is filed or unmistakable before any ask counts it. Reports kept as determinism_check_report_arch3.md and determinism_check_report_arch3_pass2.md.
- 2026-10-31, architecture 4 at its stage 4 judge (NOT_DETERMINISTIC, reconciled FIX_NOW): the call held in every variant, but the runner-up, the gap and the kept alpha moved with the curve's exponent (momentum 3.91 to 5.88 between 0.7 and 0.4), its weighting, a common intercept across the bands, the consolidation day left as a return and the ESG names dropped, because the desk's orders sat almost all under 3 per cent of a stock's day (1.2 per cent were event trades) and the data did not separate the forms (R2 0.4655 against 0.4630); the ESG list also took effect inside the log (15 January 2026) while 101 rebalance rows still traded listed names. Repaired in the generator, the call and the decisive step unchanged; the judge's verdict kept as determinism_check_report_arch4.md.
- 2026-10-31, the first repair raised liquid event trades to a tenth of the desk's orders (4 to 60 per cent of the day): the family converged, but those orders carried most of the desk's traded pounds, so the value-weighted band averages (57, 75 and 115 bps) converged on the curve and filed UK Mid Cap Value, and the default path no longer ended wrong. Rejected.
- 2026-10-31, kept: participation comes from thin names, as it does on a desk. Each lower band carries a tail of thinly traded names (52 in the FTSE 250, 100 in the SmallCap), where the books' ordinary orders, sized in pounds and scaled only mildly with liquidity, take a fifth to two thirds of the day; the desk's pounds stay in liquid names at about one per cent, so the band averages still file momentum (by 2.7 million) while about 1,550 small-cap orders above a tenth of the day pin the curve where momentum trades. The 12 least liquid small caps, which no book or candidate trades, carry the consolidations; the ESG list predates the log and no book or candidate trades a listed name; the books' orders begin on 1 April 2025 with 60 sessions of history; the Severnvale transition trades large and mid caps only, at five orders a day.
- 2026-10-31, a tail of 130 thin small caps was dropped: it left momentum's investable pool (5 million a day or more) too small to swap 18 names a month, and its kept alpha fell to under 1 million.
- 2026-10-31, a common intercept across the bands was not chased: the half-spread differs by band (3, 8.5 and 25 bps), so one intercept misprices each band's trades by 0.5 to 2.2 million, which no rounding bin absorbs; IC-07 now files the population a cost is estimated from (the desk's executions in the candidate's index band), the WHAT, and the golden fits band by band. A lower shortfall noise and a narrower or wider spread of order sizes were screened and left the family's width unchanged (it is form error, set by where the desk's orders sit), so the order sizes' spread was set at 0.6 for the wider stump margin.
