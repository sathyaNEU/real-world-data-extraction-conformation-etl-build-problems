# task178 design note

**Status: PAUSED (2026-10-23). Architecture 3 spent at stage 4, Gate F (zip 6a710f5b): blind reader B landed the call by instrumenting the Bank's endogenous trades (`## Tried and rejected`). The next cell comes from the main session.** The number was RETIRED on 2026-10-21 and reopened under the author's
rule that no number stays retired (`## Rebuild (2026-10-23)`). Architecture 1 (the harbour trestle deck) and
architecture 2 (the floodplain segment of a stage-discharge rating) were spent at Gate F; the conjoint and
population-pharmacokinetics cells registered no card. Cell allocated by the main session for this draw:
quantitative-finance / volatility-derivatives-pricing, Forecasting, with a fictional country, central bank, currency
and dealers. Prototypes in the session scratchpad (b178q/proto: c1_fx.py, c1b.py, c1h.py, c1n.py, c1f.py, c1t.py).

## Draw

- **Pairing:** Quantitative Finance, task type `volatility-derivatives-pricing` (F). The deciding quantity is the
  realised volatility a freely floating exchange rate will show in 2027, the number an FX options desk prices its
  one-year options at.
- **World (fictional):** the Republic of Tamarquia, a small Andean economy whose currency, the tamarquian peso, trades
  against the dollar on an interbank platform from 08:00 to 16:00 local time. From January 2024 to December 2026 its
  central bank, the Banco Central de Tamarquia, sold or bought dollars with the dealers in the hours the peso came
  under the most pressure; in October 2026 it announced that its spot operations end on 4 January 2027 and released,
  with the announcement, the hourly record of its operations and of the reporting dealers' net customer purchases for
  2024 to 2026. A domestic bank's FX options desk launches the country's first one-year dollar options to corporate
  clients in January 2027 and must set the volatility it prices them at; its pricing policy prices at the volatility
  the reference rate is expected to realise over the option's life, rounded up to the next whole per cent, and it
  delegates the figure to the head of the desk, who sets it before launch (forum: the desk itself).
- **The call:** the 2027 pricing volatility, a dial on the desk's whole-per-cent grid. Golden (prototype, the hourly
  instrument family on the record's three years): a free-float volatility near 11.5 per cent, priced at 12. Default
  path: the reference rate's realised volatility over 2024 to 2026, near 7.2, priced at 8.
- **Shape:** 04, setting one dial: the grid's settings, each covering or failing the 2027 expected volatility, the
  committed setting and the one below; asks A and B supply the rest (stage 2, `## Ask sheet`).
- **Strategy:** `causal_design` (simultaneity: the central bank's trades respond to the same hour's move, so the
  comparison the design implies is the customers' own flow, not the net flow), gap time (the record was produced
  under the smoothing operations, the decision bets on the float), G5 then G16 and G17, Gate G
  method_or_model_selection, layer2_family estimand_identification, layer2_pattern
  own:price-impact-of-customer-flow-under-leaning-intervention.
- **Data-native sentence:** the central bank sold dollars in the hours the peso fell hardest and bought in the hours it
  rose hardest, so in the record its trades are largest exactly when the hour's own news was largest; the customers'
  flow is the only flow in the record that did not answer the hour's move, and the market's depth is read on it, net
  of the share of it the bank took off the market.
- **Sources (one line each):** the client's derivative-pricing, market-data and counterparty cards (calibrated model,
  discrete monitoring, early exercise, total-variance arbitrage, curve repricing, netting) are pricing methods that
  take the volatility as given, so none supplies this pitfall; the field's textbook routes for the forecast (the
  record's realised volatility, a GARCH or HAR fit to it, the latest quarter) are the default path; FX microstructure's
  textbook calibration (the rate's move regressed on order flow) is the first rung, and the simultaneity it ignores
  under a leaning central bank is the stump. task177's unregistered candidate G (dealer gamma damping index moves,
  the programme winding up) is the nearest screen on file and died on lever and family spread at plausible strength;
  task135 (nonsynchronous unit prices under a volatility cap) is the cell's shipped card and shares no driver.
- **Measured lever (prototype, 10 to 20 worlds a configuration, hourly grain over 756 days):** with the bank absorbing
  part of every hour's pressure beyond about 0.1 per cent, the record's volatility sits at 0.58 to 0.75 of the
  free-float truth; the impact read on the net flow puts the bank back at 0.56 to 0.85; the two-regressor fit, whose
  bank coefficient has the wrong sign, 0.35 to 0.63; customer flow alone (the reduced form) 0.75 to 0.89; customer
  flow in the hours the bank stayed out 0.60 to 0.81; scaling the record by the net flow's variance ratio 0.72 to
  0.94; the bank-hours volatility 0.70 to 0.94. The instrument family (the customer flow as the instrument hourly and
  daily, its sign, year by year, the reduced form over one less the absorbed share, the structural sum) lands 0.90 to
  1.09 of the truth, median spread 3.6 to 4.4 per cent within a world, the hourly members 1 to 2 per cent of each
  other; the whole-per-cent grid with the expected volatility mid-bin holds every member on one setting.
- **Guard (`check` on the draft):** WARN only, overuse.objective (the lane is Forecasting) and overuse.gate_g
  (method_or_model_selection is the honest label: two defensible estimators of the market's price impact, the data's
  structure pinning one). Earlier drafts BLOCKed and were redrawn honestly before filing: decisive G16 repeated
  task478's pattern (ban.pattern) and decisive G3 repeated task169's signature (test.same_driver on time, G3 and
  forecasting), so the decisive generator is G5 (the customers' dollar need was partly met by the central bank, so the
  record's prices never absorbed it), which is what the record shows; Gate G forecasting with G5 matched task111 and
  task86, and the identification is the mechanism, so method_or_model_selection is the label the design earns.
  Personas drawn with `guard.py names --locale es_CO --seed 178`; Rosa, Eduardo and Alexander replaced on
  people.first. Under the serial lock the window had moved: ban.forum committee_or_panel against task482, so the
  figure is the desk head's own under the pricing policy (operations_desk, which is how a trading desk sets a
  pricing parameter), and the deliverable pair became a workbook and a PNG chart (svg plus xlsx repeated task482;
  png plus xlsx is a WARN against task175, answered: the chart is the desk's grid against the forecast, nothing
  like task175's).

## Default path

The pipeline a strong analyst builds from the prompt's words, the policy and the files' grain, with every field read
and every filed rule applied:

1. Reads the pricing policy (section 2): the 2027 expected volatility is the closing rate's volatility over the 2024 to
   2026 sessions had the Banco Central not operated, as the annualised root mean square of daily log changes at 252
   sessions, rounded up to the next whole per cent.
2. Builds the customers' net dollar purchases each hour from the reports of record in
   `dealer_customer_flows_hourly_2024-2026.csv` (the last report received per dealer and hour, Financiera Tres Valles'
   July 2025 reports dropped per the dealer register), and the Bank's net dollar sales each hour from
   `bct_spot_operations_2024-2026.csv` (ANULADA rows dropped, VENTA less COMPRA).
3. Takes each hour's log change of the platform mid, joining an hour to the next where a mark is missing, and regresses
   it on the order flow the dealers absorbed, the customers' purchases less the Bank's sales (FX microstructure's
   textbook calibration of price impact): 0.07 per cent of the rate per 100 million dollars.
4. Puts each session's Bank net sales back into the closing rate's daily log change at that impact and takes the
   policy's root mean square at 252 sessions: 7.4 per cent.
5. Rounds up: 8 per cent.

- **Ends on:** 8 per cent
- **Golden:** 12 per cent

The neighbouring routes, each measured on the cut pack (`checks.py`, `cracker.py`): the record itself, 6.9 (7); the
impact read on customer flow alone, 8.9 (9); on customer flow in the hours the Bank stayed out, 8.4 (9); the
two-regressor fit taking the Bank's coefficient as the impact, 6.1 (7), or the customers' coefficient, 8.1 (9);
the record scaled by the customers' flow variance against the net flow's, 8.2 (9); the sessions the Bank did not deal
in, 4.2 (5).

## Stump sentence

A competent solver who calibrates the market's price impact the textbook way, the hour's move regressed on the order
flow the dealers absorbed (customers less the Bank), puts the Bank's trades back at that impact and prices at 8 per
cent (7.4); the step that lands it there is the regression itself, because the Bank sold in the hours the peso was
falling hardest and bought in the hours it was rising hardest, so its trades answer the same hour's news and the
customers' flow, the one flow that did not answer the move, read as the instrument (the reduced-form impact scaled by
the share of it the Bank left to the market) gives the depth the float exposes, a 2024 to 2026 volatility between 11
and 12 per cent and a price of 12.

## Three rules

- **Task type:** volatility-derivatives-pricing (Quantitative Finance), a task type the taxonomy serves with
  Forecasting; the call is the volatility one-year options are priced at for a window not yet open.
- **Domain test:** the deciding quantity is the realised volatility the peso's closing rate would show without the
  central bank, which FX microstructure reaches through the price impact of customer order flow (the market's depth)
  and an options desk prices at; with another field's nouns there is no order flow, no dealer depth and no central
  bank trading against the same hour's move, and nothing in the call computes.
- **Swap:** "Price the 2027 one-year dollar options at 12 per cent" becomes "staff the 2027 wards at 12 nurses a shift":
  a hospital has no order flow that a central bank absorbs and no price that moves per dollar traded, so the sentence
  stops making sense, and the reduced form scaled by the absorbed share has nothing to scale.
- **Layer 1:** the Bank's dealing-system export with ANULADA rows for deals entered in error (its dealing desk); dealer
  reports filed by 18:00 and refiled to correct, every receipt kept (the Bank's reporting portal); Financiera
  Tres Valles' legacy feed still filing its former customers for July 2025 after the merger into Banco del Salitral
  (the systems migration); hour marks missing after platform feed failures (the price feed); two holiday calendars
  closing the platform; platform confirmations in UTC with CANCELLED executions (the platform); euro forwards, cancelled
  deals and the Treasury desks' own deals in the deal-system export, window forwards kept at contract notional with
  their drawdowns booked as outrights (the deal system's booking). Nothing placed to be caught; each item mishandled
  leaves the call at 12 (`checks.py` R2).
- **Layer 2:** estimand_identification. The counterfactual volatility needs the market's price impact, and the
  Bank's reaction to each hour's own move makes every regression that puts the Bank's trades on the right-hand side
  inconsistent; the customers' flow is the instrument.
- **Decisive step:** identifying the market's price impact with the customers' own flow as the instrument for the
  flow the dealers absorbed, equivalently the reduced-form impact divided by one less the share of customer flow the
  Bank absorbed, because the Bank's trades answer the hour's own news.
- **Not semantics:** every field read correctly (the report of record, ANULADA, the merger, the 16:00 close, 252
  sessions, rounding up) still leaves the textbook regression of the hour's move on the net flow, which files 8;
  nothing in any definition says how the impact is estimated, and the Bank's files say what a row is and nothing
  about how its trades relate to the hour's move.
- **Not rule application:** no filed rule estimates the impact or builds the counterfactual; the policy files only the
  WHAT (the closing rate over the 2024 to 2026 sessions had the Bank not operated, customers' trading as it was).
  Enumerated family, 14 constructions (record, net-flow OLS, customer-flow OLS, customer flow in Bank-free hours, the
  two-regressor fit read two ways, the variance ratio, Bank-free sessions, and the six instrument constructions):
  4.2 to 11.6 per cent, settings 5 to 12. Standing family, the six constructions consistent under the Bank's
  same-hour reaction (customer flow as the instrument hourly, daily, by year and by its sign, the reduced form over one
  less the absorbed share, the structural sum): 11.32 to 11.60 per cent, one setting, 12. The ruling-out is the
  Bank's own purpose in its press release (moderating disorderly movements during the session) and the two-regressor
  fit's wrong-signed Bank coefficient (minus 0.20 per cent per 100 million dollars: a Bank sale moving the rate up),
  not a filed clause.
- **Analyst test:** a strong analyst who takes the reports of record, drops the ANULADA deals and Financiera
  Tres Valles' July 2025 reports, joins the hours with a missing mark and reads the policy's closing-rate, 252-session
  and round-up conventions, then puts the Bank's trades back at the impact read from the hour's move regressed on the
  market's net flow, prices at 8 per cent (7.4), or at 9 with customer flow alone (8.9).
- **Estimand:** `cordillera_fx_options_pricing_policy_2027.pdf`, section 2: "For the 2027 launch the expected
  volatility is the volatility the closing rate would have shown over the sessions of 2024 to 2026 had the Banco
  Central not operated in the spot market, with customers' dollar trading and the news the market received as they
  were." Population: the daily changes of the 16:00 closing rate between the release's sessions, 2 January 2024 to 29
  December 2026 (727 changes); outcome: the annualised root mean square at 252 sessions; window: those sessions;
  unit: per cent, rounded up to the whole per cent; comparison: none (a dial against the grid).
- **No decoy:** nothing is planted to be caught: no memo, draft, staff estimate or Bank statement of its own effect on
  volatility ships, no figure in the pack ranks the grid's settings, and the two distractors answer other questions
  (the TRM is not the settlement rate; the monthly statistics are by value date).
- **No certified replay:** no certified or published figure is reproduced to recover the method; the monthly
  statistics sum the Bank's sales by value month and cannot identify an hourly impact, and nothing in the pack
  states a volatility the method must match.
- **Lesson:** a regression of price on order flow measures depth only where the flow is not answering the price;
  under an agent that trades against the outcome it is regressed on, the record's damped market is undamped at the
  depth the exogenous flow reveals. No build on file teaches it: task177's candidate G (dealer gamma) died before a
  card on lever and spread, and task135's driver is nonsynchronous pricing.

## Readability screen

| Rung | Its handle in the pack | Verdict |
|---|---|---|
| R0 the record's realised volatility, 6.9 (7) | the 16:00 marks in the hourly mid file | readable |
| R1 the Bank put back at the net-flow regression's impact, 7.4 (8) | the flows and operations files side by side | readable |
| R2 the impact on customer flow alone, 8.9 (9) | the flows file | readable |
| R3 the impact on customer flow in the hours the Bank stayed out, 8.4 (9) | the operations file's empty hours | readable |
| R4 (decisive) customer flow as the instrument, 11.3 to 11.6 (12) | nothing names it: no file, column or sentence says the Bank's trades answer the hour's own move, names an instrument or an absorbed share; the press release says only that the Bank moderated disorderly movements during the session | silent |

## Semantic fork table

| ID | Term | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "volatility" | annualised root mean square of daily log changes at 252 | demeaned standard deviation; simple changes; hourly realised variance plus the overnight | 12 each (asserted) | same call |
| SF2 | "2024 to 2026" | the release's sessions, 2 January 2024 to 29 December 2026 | calendar years with the release's last days | 12 | same call (the release ends 29 December) |
| SF3 | "had the Banco Central not operated" | the Bank's trades taken off the market, customers and news as they were | customers trading differently under a float | not computable | policy section 2 ("customers' dollar trading and the news the market received as they were") |
| SF4 | "customers" | counterparties other than reporting dealers and the Bank | interbank or Bank trades included | the release note | release note section 2 |
| SF5 | the Bank's operations | VIGENTE rows | ANULADA rows kept | 12 (11.68) | release note section 1, and same call |
| SF6 | the hour of an operation | the dealing system's local time | UTC | the note | release note section 1 ("local time") |
| SF7 | a dealer's report for an hour | the last received | the first received, or every receipt summed | 12 each (11.47, 11.49) | release note section 2, and same call |
| SF8 | Financiera Tres Valles' July 2025 reports | not of record (to 30 June 2025) | kept | 12 (11.47) | the dealer register, and same call |
| SF9 | an hour whose closing mark is missing | joined to the next hour | the pair of hours dropped | 12 | same call (asserted) |
| SF10 | the grid | rounded up to the next whole per cent | nearest whole per cent | 11 or 12 at a 11.5 golden | policy section 2 ("rounded up to the next whole per cent") |
| SF11 | "the closing rate" | the platform's 16:00 mark | the 08:00 open, the TRM | the policy | release note section 3, policy section 1 |
| SF12 | the settlement series | the 16:00 closing rate | the TRM (its recorded changes run under the close's) | the policy | policy section 1 ("cash settled against the platform's 16:00 closing rate") |

## Ladder

| Rung | Route | Figure | Setting |
|---|---|---|---|
| R0 | the closing rate's recorded volatility | 6.9 | 7 |
| R1 (default) | the Bank's trades put back at the hour's move regressed on the net flow | 7.4 | 8 |
| R2 | the impact on customer flow alone (the reduced form) | 8.9 | 9 |
| R3 | the impact on customer flow in the Bank-free hours (selected on small moves) | 8.4 | 9 |
| R4 (decisive) | customer flow as the instrument for the absorbed flow | 11.32 to 11.60 | 12 |

Separation: every rung below R4 files 9 or less, three settings or more under the call; the nearest rival sits 2.6
points under the golden (11.50 against 8.92). The golden's own sigma over 80 hour bootstraps keeps 12 at two sigma
(`checks.py`). The generator's free-float truth is 11.52.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the daily closing changes between the release's sessions | filed (policy section 2), C1 against the calendar years |
| 2 Unit of account | a session's closing change; an hour for the impact | the policy files the daily change; the hour is the record's grain |
| 3 Attribution window | an operation belongs to the hour of its local time stamp | release note sections 1 and 2, one clock |
| 4 As-of dating | the release of 30 December 2026 | filed in the release note |
| 5 Version basis | the last report received for a dealer and hour | release note section 2; C1 (first or summed, same setting) |
| 6 Denominator | 252 sessions a year | policy section 2 |
| 7 Weighting | every session equally in the mean square | the definition (a root mean square of daily changes) |
| 8 Window length | the three years | filed |
| 9 Boundary inclusivity | a figure on an integer stays there under rounding up | C1, the golden 0.5 inside its bin |
| 10 Rounding path | rounded once, up, at the end | policy section 2 |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | none: the record is complete to its last session | C1 |
| 13 Order of operations | the impact first, the daily changes after | C1 (the hourly and daily routes agree) |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | ANULADA deals out; refiled reports by receipt time | release note sections 1 and 2; C1 |
| 16 Identity normalisation | the merged dealer's codes | the dealer register |
| 17 Netting against gross | VENTA less COMPRA within the hour | release note section 1 |
| 18 Dimensional units | both flows in thousands of dollars | the column names and the note |
| 19 Code and status semantics | VENTA, COMPRA, ANULADA | release note section 1 |
| 20 Integerisation | the grid's whole per cents | policy section 2 |
| 21 Clause scope | the 2027 sentence governs the launch only | policy section 2 |
| 22 Forward window contents | 2027 taken at the base years' customers and news | policy section 2 (the counterfactual) |

## Literal reader

Executing the prompt and every filed sentence word for word: the policy names the series (the 16:00 close), the
measure (root mean square of daily log changes at 252), the window (the 2024 to 2026 sessions), the counterfactual
(the Bank's operations taken off the market, customers' trading and news as they were) and the rounding (up to the
next whole per cent); the release note defines every row the counterfactual needs. Nothing filed estimates the
market's response to the trades removed, so the literal reader must estimate it, and the readings of every term
converge on 12 (`## Semantic fork table`, each row asserted in `checks.py`); the easy answer, 8, comes from an easy
estimator on the same literal estimand, never from another reading.

## Oracles

- The generator's free-float truth (the hourly path with the Bank's trades never applied): 11.52, against a golden of
  11.50 read from the shipped files.
- The independent verifier (`generator/verify.py`): pandas joins and a two-stage least squares on its own code path,
  the impact 0.5 to 0.6 per cent per 100 million dollars and the volatility inside (11, 12].
- The asks: the generator's own order and drawdown structure against the shipped files' grouping (`checks.py` ask A
  and ask B blocks).

## Ask sheet

**Ask A, the desk's 2026 hedging cost.** Figures: 16 (four 2026 quarters times four order size bands), pesos per
dollar to one decimal, dollar-weighted against the platform mid at each order's arrival. H18 home: a component of
the option's price (the policy's hedging charge, section 3). Use: the charge the desk adds to the premium. File:
`platform_confirmations_cordillera_2026.csv`, 10 columns, 3,000 rows. Primary device (D6, which records are one
event): an order that takes several resting quotes is confirmed as one execution per quote, each carrying the
order's millisecond stamp, trader, side and arrival bid and ask; nothing names the order. Read as orders, the
executions put the large orders' deep fills into the small bands and leave the 10 million band empty in every
quarter. Hazard: CANCELLED executions and their re-booked twins (moves 9 of 16 cells when kept); confirmations in UTC
(no quarter boundary moves, texture). Benign twins: other traders' orders in the same second. Stops: executions as
orders (every cell misses, the top band empty); CANCELLED kept (9 cells move); orders by second rather than by
trader (benign twins, one cell). Realism: platform confirmations are per execution; the desk's order book export did
not exist before 2026, so Treasury Operations costs orders from the confirmations.

**Ask B, client dollar forwards falling due in 2027.** Figures: 8 (four 2027 quarters times exporters' sales and
importers' purchases), millions of dollars to one decimal. H18 home: the policy's launch limit (section 4). Use: the
vega limit quarter by quarter. Files: `cordillera_fx_forward_deals_2025-2026.xlsx` (11 columns, 949 rows) and
`cordillera_corporate_client_register.csv` (5 columns). Primary device (D1 and D6, which records are one event): a
window forward keeps its contract notional while each drawdown against it is booked as a separate outright at the
window's rate, same client and side, maturing inside the window; nothing links them. Summed gross, every quarter's
two figures run 4.0 to 25.0 million high. Hazards: euro forwards (7 figures move), cancelled deals, the Treasury
desks' deals (segment TESORERIA). Stops: windows gross (every figure misses); windows dropped (misses the remainders);
euros kept. Realism: deal systems book a window's drawdowns as new tickets and net them in the risk engine.

**Main population zero-counts:** neither ask's files are read by the call (the call reads the flows, operations,
mids, dealer register and calendar); no ask device row sits in a file the call reads (asserted by file in
`checks.py`). Delete every ask device and the call is unchanged; delete the call's analysis and the asks are
unchanged.

**Hazard table:** CANCELLED executions (ask A, 9 cells); euro forwards (ask B, 7 figures); cancelled deals (ask B, 3
figures). **Referee:** none needed; each device's evidence is an identity inside its own file.

| Ask row | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, 16 cells | executions read as orders, CANCELLED dropped: 0 of 16 within the bin | miss |
| B, 8 figures | live deals summed gross, euro, Treasury and cancelled deals dropped: 0 of 8 | miss |

- **Measured by:** `generator/cracker.py` on the cut pack (scores every figure against `figures.json`).
- **Mirror leakage:** 0.0 per cent of ask weight (the mirror, priced at 8, takes the same ask path: 0 of 24).
- **Pair ceiling:** 28.5 (cracker 45.0 on 38, 7 and 55; mirror 12.0).

## Leak sweep

`leak.py task178 --asof 2026-12-30`: REVIEW, no LEAK. Answered line by line:
- Sweep 3, answer figures: 1.0 and 2.1 are the pricing policy's version numbers in its revision table and footer, not
  ask figures; the policy carries the call's words (one-year, dollar, options) because it is the product's own policy,
  and it names no volatility, setting or grid outcome.
- Sweep 4, design-note vocabulary: the release note, the press release and the policy share generic words with the stump
  paragraph (record, customer, market, trades, hourly, measured); none says the Bank's trades answer the hour's move,
  names an instrument, a regression, an impact or an absorbed share (asserted in `checks.py`: no document carries
  instrument, endogen, simultane, price impact, regress, lean, drawdown, sweep or "execution per").
- Sweep 9, dates after the setting: the forward deals' 2027 maturities (the ask's own subject) and the calendar's 31
  December 2026 row (a calendar lists the year's remaining days).
- Container metadata: `scrub_producer_metadata.py` reports target and golden clean.

## Guard

- `check` on the registered card: WARN only (overuse.objective and overuse.gate_g, the lane; repeat.gate_g against
  task482, whose method selection is a hedonic index, nothing shared; repeat.deliverables png plus xlsx against task175,
  answered at the draw).
- `surface task178`: exit 0; the highest surface similarity is 0.10 (task179, task461, task458, about the corpus 98th to 99th percentile, no shared gap, pattern or decision family); personas in the cut pack are the card's.
- `heart task178`: WARN, the nearest driver or stump on file at 0.06 (task446's group pricing, task253, task482); no
  driver within the WARN floor's reach of an absorbing-agent identification.
- Names (H21): the first cut named the country after a real Colombian department and three dealers after real banks
  (Scotiabank, CorpBanca, Banco Agrario); every institution, the country, its capital and a branch were renamed before
  any reader saw the pack.

## Retired

Retired on 2026-10-21 under the author's rule for this round (a number that dies in its second new cell is
retired). The seed's own world (FC49, product-security triage) died at stage 1. The first redraw cell
(physical-environmental-sciences / climate-weather-extremes) carried architecture 1, the April-May 2027 trestle deck
set against the window's own predicted tides; it was built to stage 3 green and spent at Gate F when a scored
reader conditioned on the 2027 tide table and landed every call figure. The second cell
(marketing-consumer-research / conjoint-choice-willingness-to-pay-analysis, Forecasting) yielded nothing that holds
on measurement or on the screens (`## Tried and rejected`, the conjoint lines): the judgments the textbook
simulators (a logit share simulator, an aggregate MNL, an HB simulator, the first-choice rule) take for granted
either move the forecast less than their own estimator family spreads it (price non-attendance under a normal-prior
HB; a brand-by-tier interaction), or rest on a linked file whose filter or calibration is the reader's first move
(a pilot's revealed uptake, the in-market population by contract timing or footprint), or are banned as hidden
rules (a competitor's matching reaction). No card was registered in the second cell. The card for architecture 1
stays filed with `architecture_spent` set.

## Rebuild (2026-10-23)

Reopened by the author's rule that no number stays retired and rebuilt from scratch in
physical-environmental-sciences / hydrology-flood-frequency (Forecasting), the cell the main session allocated,
worktree `b_178n`. Architecture 1 (the harbour trestle deck) and the conjoint cell stay spent; the card's identity
for architecture 1 moved into `lineage`. Architecture 2, the floodplain segment of the stage-discharge rating under
the annual peak series, was registered and committed DRAWN on 2026-10-23 (9bb65027) and built the same day to stage 3
green (checks 151 of 151, verifier 26 of 26, two byte-identical builds, precut and figures_check exit 0, leak.py
REVIEW answered, guard surface exit 0 and heart WARN); it waits at stage 4 for the main session's two scored readers
and the judge. The cell's other candidates are lines at the foot of `## Tried and rejected`. Stage 4 (pack cc9cb2f1):
the judge approved, both readers landed the call, and architecture 2 is spent at Gate F; the card's re-registration
(d4521939) is moot with the architecture spent, and the card is left as filed with `architecture_spent` set.

The main session then assigned pharmacology-pharmacoepidemiology-safety / population-pharmacokinetics-exposure-response
(Forecasting), worktree `b_178n` at 682b11dd, with fictional drug, sponsor and country. The task type's earlier screens
were read first and kept spent (task179's target-mediated elimination and eleven on paper, task170 architecture 2's
twenty). Two new candidates were measured dead on code and sixteen directions on paper (the cell's lines at the foot
of `## Tried and rejected`). No card was registered, so architecture 2 stays the card's current identity, nothing moved
into `lineage` and nothing was cut. PAUSED at stage 1 for the main session to assign another cell.

Third rebuild cell the same day, assigned by the main session: quantitative-finance / volatility-derivatives-pricing
(Forecasting), worktree `b_178n` at d020f687, fictional settings. task177's screen of the same cell (candidate G and
seventeen paper deaths, with its finding that a volatility level carries a 5 to 14 per cent model spread) and task135's
card were read first and kept spent. Fifteen directions died on paper and one candidate measured on code held at the
screen (the cell's lines at the foot of `## Tried and rejected`): architecture 3, a central bank's leaning spot
operations ending, registered on 2026-10-23 with architecture 2's identity moved into the card's `lineage`.
Built the same day to stage 3 green (checks 91 of 91, verifier 33 of 33, two byte-identical builds, precut and
figures_check exit 0, leak.py REVIEW answered, guard surface exit 0 and heart WARN); it waits at stage 4 for the main
session's two scored readers and the judge.

## FC49 screen record (world spent, kept for the record)

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** New, Forecasting, seed FC49: a
network-equipment vendor's product-security team has one extra triage analyst for the first quarter of 2027,
who goes to the product line with the most critical triages forecast for the quarter (one triage per CVE per
affected product line, done as part of that line's advisory) if its lead over the runner-up is larger than
the forecast's own error one quarter ahead, and otherwise stays in the shared pool; the staffing note is due
on 10 December 2026. The world, the decision and the quantity were kept. The seed's own mechanisms (the
policy's four-quarter mean and eight-quarter lead deviation as a filed HOW, the vendor's severity score as
the decider, the dashboard as an official decoy, the release-train swing inflating the lead's deviation into
a hold) were never candidates. Two decisive steps were screened on code, each one of the brief's ideas in
its strongest form, over three seeds each, and neither held. No architecture is live. This note holds the
screen record only; it carries none of the `precut.py` sections, because no design exists. The prototypes
stay in the session scratchpad (b178/proto: `protoA.py`, `protoB.py`, `screen178.py`, whose output
`screen178.out` is byte-identical with `screen178_run2.out` over two runs).

**The structural sentence, and the first thing to read.** A line's coming quarter differs from its own
record only where work reaches its advisories through a channel or a train slower than the quarter: reports
waiting under embargo in the coordination centre's queue, a component refresh that triages every
third-party critical accumulated since the line's last one, a supplier's pre-notified bulletins. Every
reading of that difference that holds is a count not yet arrived, completed for the slow unit, which is
task181 v2's driver ("the units whose records arrive slowest look quiet exactly while they are surging, so
the comparison has to be made on the complete count each unit's own arrival history implies"), landed on
the portal once its estimand was filed literally, and honestly `maturity_censoring`, which task201 holds in
the ban window. The readings that are not that driver either hand the call to the cheapest route (the queue
read at face value, a rule of thumb for a long-delayed refresh) or move the decisive step into composition
(conversion or slip by case type or by line, `composition_mix` held by task165) or into semantics (which
other lines a queued report's code also ships on). The quantity is also thin where it is not pipeline: a
real vendor's own-code criticals run one to five per line per quarter, so a lead that is real against the
forecast's own error needs the counts third-party CVEs supply, and third-party CVEs reach a line only
through its refresh train. A draw on this quantity needs a difference between the coming quarter and the
record that no recorded channel already carries and no slow channel is completing; none was found here.

**The registration finding.** The honest strategies were `maturity_censoring` (candidate 1, and every
per-line reading of the queue), held by task201 (registered 13:39), and `composition_mix` (candidate 2c),
held by task165 (14:10). The window on main at 5c5631d is task201 (`operations_desk`, `season_or_peak`,
`utility_or_infrastructure`, `field_unit_lead`, `published_series`), task247 (`executive_team`,
`vote_or_meeting`, `university_or_school`, `research_desk`, `operations_log`) and task165
(`council_or_assembly`, `purchase_order_or_contract`, `local_government`, `operations_director`,
`register`). The keys this world offers honestly outside them, had a design held: organisation
`manufacturer`, forum `committee_or_panel`, forcing event `budget_or_appropriation`, role
`capacity_planner`, calibration `none`. Nothing was registered and no axis of the window was spent.

**The taxonomy finding.** A product-security team's triage workload has no client task type of its own.
Product Analytics serves Forecasting through retention, churn and feature adoption only (task162's browser
reports sat in feature adoption because version adoption decided them), and none of them is a line's
critical CVE count. The honest home is General Statistics & Data Science,
`regression-classification-model-diagnostics` (the forecast model and its out-of-sample one-quarter error),
or the house domain `business-operations-analytics` (`workforce-labour-planning`) that maps there.

**The repeat screen.** `guard.py recent`, `coverage`, `mechanisms --objective forecasting` (82 builds) and
`slots` ran before any card, `slots` on embargo, advisory, triage, refresh, roll-up, freeze, deferred,
backlog, accumulated, Hawkes, self-exciting, excitation, follow-on, variant, code age, new code, churn,
lifetime, honeymoon, spillover, embedded, sibling, shared code, fan-out and observation effort: no slot or
card spent a refresh-accumulation or forward-batch mechanism in a product-security world, and the binding
matches are by the abstraction test (task181 v2 and v3, task174's vintage screen, task136, task163,
task132, task75 v1, task199). The brief's near drivers were read in full on their cards: task162 (restart
bursts after Patch Tuesday), task148 (abandonment in a 911 queue), task159 (backlog behind full trains);
none is touched by either candidate.

## Tried and rejected

- **Candidate 1: the deferred component refresh** (the brief's release-train idea in its strongest form;
  `protoA.py`, seeds 11, 12 and 13 fixed before outcomes). Driver as drafted: a line's kernel and crypto
  updates wait for its platform release, so its recent quarters record only the rest of its third-party
  flow, the held criticals keep arriving upstream at the rate its earlier refreshes and its siblings' current
  ones show, and they land in one roll-up with the release inside the quarter. Killed at stage 1 on
  measurement (a rule of thumb lands) and on the draw screens (it is task181 v2's driver, honestly
  `maturity_censoring`).
  - The world: eight upstream component groups (kernel 4.0, crypto 2.2, SSH 0.8, web 3.0, DNS and DHCP
    1.2, routing 1.5, management 1.0, libraries 5.0 critical CVEs a month), five lines with group-specific
    affected shares, refreshes monthly (DATACENTRE), quarterly (CAMPUS), half-yearly (BRANCH in April and
    October, WIRELESS in May and November) and every four months (GATEWAY in April, August and December),
    8 per cent of upstream criticals exploited and patched out of band within three weeks, own-code
    criticals 0.8 to 2.2 a month a line, chipset bulletins 2.5 a month for WIRELESS. GATEWAY's kernel and
    crypto groups were held after its 16 September 2025 refresh until the GATEWAY 10 platform release on
    10 February 2027: seventeen months at about 4.9 affected criticals a month. As-of 10 December 2026.
  - The golden family (GATEWAY's first-quarter critical triages): its own pre-freeze group rates over each
    group's months since its last update, the same on its last 24 pre-freeze months, and the held groups
    priced at the sibling lines' post-freeze rates scaled by GATEWAY's earlier ratio to them: 104.2, 109.4
    and 91.8; 111.2, 108.8 and 105.2; 105.5, 101.9 and 118.1 (a spread of 5.5 to 16.9 per cent of the
    median, so GATEWAY's figure needs a bin of 25 or more). Realised first-quarter truth 72, 82 and 96.
  - The routes as first drawn (the runner-up 43.7 to 48.1): the trailing four quarters BRANCH, DATACENTRE,
    BRANCH; eight quarters BRANCH, DATACENTRE, DATACENTRE; the same quarter last year DATACENTRE,
    DATACENTRE, CAMPUS; the latest complete quarter and an eight-quarter trend DATACENTRE in all three; the
    average roll-up per release GATEWAY in seeds 11 and 13 (46.2 against 45.0, 46.0 against 38) and
    DATACENTRE in 12; a factor of 1.5 to 3.0 on GATEWAY's recent roll-up GATEWAY in all three.
  - With DATACENTRE's own-code criticals raised to 9 a month (the naive leader at about 70 to 80, the
    runner-up 67.2 to 74.1): every time-series and per-release route files DATACENTRE; a factor of 1.5
    misses in all three seeds, 2.0 lands in seeds 11 and 13, 2.5 and 3.0 land in all three. The factor at
    which GATEWAY overtakes is 1.55, 2.03 and 1.52 against the golden's 2.20 to 2.51, and the 2.5 and 3.0
    factors (91 to 123) sit inside the family's own 94 to 117, so a rule of thumb for "a long-delayed
    refresh is two or three times a normal one" lands the line and the figure's bin.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply (a count, no
    suppressing threshold); variance-only passes (the step moves GATEWAY's point 2.20 to 2.51 times); the
    common-exposure subset fires in its once-thought-of form, since the golden is GATEWAY's own pre-freeze
    kernel and crypto months filtered and divided, times the seventeen-month gap (equal to the family's
    median in four of six runs), and no earlier refresh closes a gap like it (the longest is four months),
    so the step's whole difficulty is recognising the held groups.
  - Why it is dead whatever the tuning: the held criticals are incurred and not yet triaged, and the
    forecast completes them for one slow unit, which is task181 v2's driver by the abstraction test (latent
    structure: records that arrive late for one unit; default: what has arrived; correction: the complete
    count the unit's own history implies) and `maturity_censoring` honestly; relabelling it time or
    decomposition to pass the window would be a lie in the card.
- **Candidate 2: the coordinated batch in the coordination centre's acknowledgement queue** (the brief's
  known-forward-workload idea, read through the queue's own slip and conversion history; `protoB.py`, seeds
  21, 22 and 23 fixed before outcomes). Killed at stage 1 on measurement in all three configurations.
  - The world: own reports that become critical advisories 2.5 to 5.5 a month a line, each acknowledged
    with a planned disclosure 45 to 120 days on and a slip drawn per case; third-party criticals 4 to 12.5
    a month a line; five earlier coordinated batches of 9 to 18 (2023 to 2025, one a year somewhere) so the
    queue's history has precedents; at the as-of a coordinated multi-vendor batch of 34 criticals listed
    against GATEWAY.
  - 2a, the batch planned for 2 February 2027 and multi-party cases slipping as single-vendor ones do: the
    face-value reading (every open case planned in the quarter, on its listed line, at full size), the
    pooled-slip reading and the golden (slip by case type) all file GATEWAY in all three seeds, so the
    cheapest queue route lands; the golden's lead over DATACENTRE is 1.7, 12.6 and 11.7 against a model
    error of 11.1 to 11.4 (ratio 0.15 to 1.10), so even the golden's pick is not robustly real.
  - 2b, the brief's slip check (the batch planned for 2 March 2027, multi-party cases slipping by a gamma
    with a mean of 48 days): the batch lands inside the quarter with probability 0.35 to 0.36, its landing
    variance takes the error to 19.0 to 19.3 against leads of 10.1 to 17.7 (ratio 0.52 to 0.92), and the
    golden (DATACENTRE) is the trailing route's and the seasonal route's answer in all three seeds while the
    face value files GATEWAY: the slip noise swamps the lead exactly as it did task174's.
  - 2c, the batch listing GATEWAY and BRANCH, which ship the same VPN stack, BRANCH affected by about 30 per
    cent of the stack's earlier coordinated cases: the face value lands GATEWAY in all three seeds and the
    pooled conversion files GATEWAY, GATEWAY and BRANCH; the step that separates (conversion read per
    listed line from the stack's earlier cases) is `composition_mix`, held by task165, and reads the
    vendor's own affected determinations, which the brief names as semantics.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply; variance-only fires in
    2b (the step lowers GATEWAY's point and raises its error, so the golden sits near the hold); the
    common-exposure subset fires in 2a and 2c (the face value is a filter and a count, and it lands).
- **Paper screens, not coded.**
  - The queue read per line at the same lead (the share of each line's quarter already acknowledged three
    weeks before it starts, from the acknowledgements as they stood, including a line whose pre-notified
    supplier bulletins are light this quarter): task181 v2's driver exactly, and `maturity_censoring`.
  - Follow-on research after a high-profile disclosure (variant hunting): task181 v3's self-exciting runs
    in the opposite direction, and critical follow-ons per trigger are a handful, too few for a real lead.
  - Code age (criticals concentrated in code shipped in the last two years, a new release yielding a wave a
    few quarters on): own-code criticals are too thin for a real lead, and a component upgrade restarting
    the curve is task132's renewal.
  - A shared-code fan-out (a batch listed against the line it was found on also lands on the line that
    embeds the same daemon): the call flips at any fan-out, so the decisive step reduces to the triage
    standard executed on an affected set inferred from co-listing, rule application on a read of the
    acknowledgement's product field.
  - The open queue as survivors (old open reports rarely become critical advisories, so the pooled
    conversion overstates the line with the stalest queue): task75 v1's open cases against completed
    durations, censoring by its honest label, and own-code counts too thin.
  - A component refresh closing an ordinary interval (the release train alone): a read of the calendar, and
    the same quarter last year lands it.
  - An upstream group's flow stepping up, or a transient upstream wave ending: with prompt triage the latest
    quarter shows it and lands; with a lagged refresh it becomes candidate 1's held backlog.
  - A staggered programme (a reachability or VEX workflow, a memory-safe rewrite) read against lines not
    yet on it: task136's and task163's common rise between the before and after windows.
  - The queue's planned dates as they stood at each origin (a real-time back-test against the overwritten
    planned-date field): task174's vintage screen on a schedule's slips, and the overwritten field makes the
    step a reading.
  - The internal testing effort read against its findings: task199's observation-effort organ, and the
    testing plan names the step.
  - The lead's error narrowed by the CVEs the top two lines share: the seed's own uncertainty-hold
    architecture, banned as a near driver, and the Poisson reflex lands any narrowing.
- **Redraw cell, climate-weather-extremes: candidates screened (2026-10-19 to 21).**
  - Mixed populations in annual maxima (tropical against extratropical): paper; the tropical population rests on
    a few dozen events, the mixture fit's spread exceeds any lever, and the storm-track file needed to split
    them is single-purpose.
  - A summer hot-day count conditioned on spring soil-moisture deficit: paper; a regression on the obvious
    covariate (the textbook route the blind readers take) with skill near r 0.4, lever under the noise.
  - Fixed-interval against sliding-window rainfall maxima (Hershfield-Weiss factor from an hourly overlap):
    paper; lever 5 to 13 per cent and the textbook 1.13 lands.
  - A declustered heat-event count (extremal index): paper; the run-length is a knob, the dispersion screen
    fires.
  - Areal against point rainfall return levels: paper; the areal-mean series fitted directly is the golden.
  - A nonstationary GEV on a warming covariate: the textbook itself.
  - Frost after bloom (phenology-conditioned frost risk): paper; the bloom model's base temperature and stage
    thresholds are open knobs, determinacy fails.
  - Joint exceedance across a network (tail dependence): paper; the estimator family's spread is wide.
  - A saturating gauge or a recorder lost in its largest events: task172's cap and task245's driver.
  - The forward astronomical tide (this draw), first form: a winter (November to February 2026-27) closure
    count at a mesotidal semidiurnal site; killed on measurement (p1, p2): the window's tidal index sits at
    0.83 to 1.0 of the long-run mean, so the climatology lands within 17 per cent.
  - Second form: March to April 2027; killed on measurement (p6, p11): the last season (2026, also weak
    springs) lands (13 against a golden 12.4 to 15.2 at one threshold, 7 against 6.2 at another).
  - Hourly non-tidal residual against skew surge as the decisive rung: killed on measurement (p6, p9): with the
    timing interaction at 0.5 to 0.8 h per metre of surge the all-hours residual and the residual at predicted
    high water both land the golden; only the cycle-maximum residual overstates (x1.5), so it is at most a lower
    rung.
  - A macrotidal estuary site: rejected on paper (p3): the tide is so dominant that every reader opens the tide
    table first.
- **Ask B, first form: a dispatcher's call record beside each crew closure from 2022** (D1). Dropped on paper: the
  source column names the dispatcher, so a careful reader drops those rows by reading it; and the new system's
  years carried no second device, so 2019 to 2026 left five years' cells to the careful path. The ask moved to
  2017 to 2022, all on the legacy system, where the reset work orders and the UTC clock move every cell.
- **Ask A, first form: a storm-peak outage on the primary, the peak on the harbormaster's tide board** (D4).
  Dropped on paper: whether the board's reading is "at the gauge" is a fork the survival definition cannot close
  without naming the board, which announces the device. The outage was removed; the board ships as a distractor.
- **Names near a real waterfront.** The first cut used a Commercial Street, a Union Wharf, a Marginal Way and a
  Custom House on a Maine harbour (Portland's own) and a city name shared with a real village; renamed before any
  reader saw the pack (`reduce-house-fixes` H21).
- **Architecture 1, the April-May 2027 trestle deck set against the window's own predicted tides: spent at stage 4,
  Gate F (2026-10-21, pack d64099d2), the judge stopped since the readers decided it.** Scored reader A landed the
  call exactly (11.60 ft, 0.4 and 2.3): "the 2027 predicted highs for 1 April to 31 May were combined with
  observed-minus-predicted peak residuals from April and May of 1995 to 2026, each year shifted to 5.40". Reader B
  filed the default path, 12.35 ft. With the tide table in the pack the decisive step is a reflex for any reader who
  thinks of it, and hiding the table would be a plant, so the architecture is spent rather than hardened. Asks: A
  kept 15 of 22 and B 16 of 22; the sensor bracket offset fell (reader A: "the sensor read 0.08 ft low from the
  2017-10-30 storm until the 2018-03-12 reset; checked against the harbormaster board") and the reset work orders
  fell to a time-gap merge ("counts did not change for cutoffs from 6.5 to 9 hours"); the legacy system's unstated
  UTC clock held for both readers (both filed 18, 22, 22, 18, 17, 10 against 24, 36, 33, 30, 20, 18). Why it held: its
  only evidence is an alignment between two files that no document invites anyone to make, while the two that fell
  each had a document naming the event (a log line, a levelling row) or a gap a reflexive dedup closes.
- **Second cell, conjoint choice and willingness to pay (Forecasting), screened 2026-10-21; nothing held, no card.**
  - Price non-attendance hidden by a normal-prior HB (`cj/ana.py`, 700 respondents, 12 tasks, three alternatives
    and none, 30 per cent ignoring price): the vendor-style HB pulls the ignorers' price coefficient to -0.33
    against a true -0.04, but the simulated shares move only 0.151 against 0.176 at the top price, every route
    (truth, HB means, aggregate MNL, latent class with one to three classes) picks the same revenue price, and the
    latent-class forms recover the truth no better than HB. Dead on lever.
  - A stated-to-revealed calibration from a two-arm price pilot of the same respondents (`cj/sprp.py`, three
    seeds): the raw simulator (0.28) already sits within the full calibration's own spread (0.26 to 0.29, around
    a truth of 0.24), because the scale and the constant offset each other at the launch price. The calibration
    regressed on noisy HB utilities also attenuates (lambda 0.45 to 0.52 against 0.55), which leaves a
    measurement-error correction as an open knob, and the pilot arms' linear extrapolation lands in one seed. Dead
    on lever and determinacy.
  - A brand-by-tier interaction the main-effects simulator cannot carry (`cj/inter.py`, two seeds): it moves the
    premium configuration's revenue 20 to 45 per cent, but the interaction family itself spreads 40 per cent
    (aggregate against HB with the interaction). Forcing it needs a holdout or model-selection criterion, which is
    the window's G16 and backtest ground, and the pick flips only when tuned near the boundary. Dead on paper.
  - The in-market population (contract end or fibre footprint correlated with preference): a join and a filter
    give the golden. That is the common-exposure subset screen, and arch 1's measured reflex on any linked forward
    input. Dead on paper.
  - Within-respondent IIA for a near-clone: the correcting rule (randomized first choice) carries an error-scale
    knob and the first-choice rule (a textbook route) lands. Dead on paper.
  - Competitor price matching read off the price history: a reaction rule recovered from records, the banned
    hidden-rule family. Dead on paper.
  - The client's four conjoint cards (IIA clone, WTP as a ratio, preference against market share with the none
    option, no out-of-range prices) are themselves the textbook routes the readers take.
- **Rebuild cell, hydrology-flood-frequency (Forecasting), screened 2026-10-23 before the draw; the field's
  textbook routes (log-Pearson Type III or GEV on the annual maximum series, a regional skew, a trend term on the
  obvious covariate) taken as the default path.** The siblings' findings read first (task174 and task176 on main:
  forward conditions die to the attaining subset, an unidentified behaviour or a filed mechanic; a finer per-case
  file replays or reduces to one group-by), so the search went to a measurement or reconstruction step the
  textbook route takes for granted. Dead on paper, each at the draw:
  - daily-mean maxima against instantaneous peaks for pre-recorder years (a peak-to-daily ratio fitted on the
    overlap, Sangal's neighbouring-day form): the ratio touches only the early years and moves the 1 per cent flood
    10 to 15 per cent at most, a constant overlap ratio lands within a bin, and a ratio by season is one group-by;
  - the loop rating at the peak (Jones's correction): at the stage crest the rate of rise is zero, so the peak's
    rated discharge moves a few per cent at most on a flashy river, under any bin;
  - a fall rating against backwater from a downstream confluence: the default's error changes sign with
    coincidence (free-flow peaks under-rated, backwater peaks over-rated) and nets small and unforced;
  - naturalising a regulated record (inflow from outflow plus the storage change): an identity once the
    elevation-storage table is read, a replay;
  - a burned catchment's next floods: the neighbouring burned basins are the attaining subset and the response
    curve past their range forks;
  - urbanisation through a continuous simulation of each storm at the future impervious share: the trend term on
    the covariate is the default, the loss model's form forks, and the future share lies past the record's range;
  - stage-frequency under a channel aggrading at the gauge: the forward shift is an extrapolated trend whose form
    forks;
  - two gauged tributaries routed to an ungauged confluence: the routed combination is a replay once the lag is
    fitted, and the short downstream record's own fit differs from the long reconstruction only by sample;
  - a crest-stage era read as censored years (EMA with perception thresholds): task466's driver, spent;
  - mixed rain and snowmelt populations: the climate cell's mixed-population death (few events, the mixture fit's
    spread over any lever);
  - a construction-season maximum (the in-water work window): a reading of the window, ask material only.
  - Held and drawn: the rating's floodplain segment (`## Draw`), measured on code (p1 to p4) before the card.
- **Architecture 2, the floodplain segment of the stage-discharge rating under the annual peak series: spent at stage 4,
  Gate F (2026-10-23, pack cc9cb2f1).** The judge returned DETERMINISTIC / APPROVE with no fix, but both scored readers
  landed the call. Reader C filed Alternative D and 14,000 cfs and kept 32 of 32 ask figures. Reader D also filed D and
  14,000 cfs: "in-bank power law with a steeper overbank term above about 10.3 ft. It is stable across eras and fits within
  about 5 percent". For the asks it found the purge spikes, the 0.47 ft offset and the stale radar face ("the sensor face
  was surveyed at 199.84 ft in May 2023"). Why it died: a rating segmented at the bankfull break is the field's own
  standard practice (a control change read off the gaugings), and with 79 gaugings above 10.3 ft the break shows plainly,
  so a careful reader fits it by default; measurement 1 of the brief (a correction the field teaches as standard is the
  default path) applies to hydrometry as it did to the tide table. The ask devices (a visit-log clock, a logged controller
  offset, a resurveyed sensor face) are all 1.1e hygiene that careful readers execute. The card's re-registration
  (d4521939) is moot now; the card is left as filed, marked spent.
- **Third rebuild cell, pharmacology-pharmacoepidemiology-safety / population-pharmacokinetics-exposure-response
  (Forecasting), screened 2026-10-23; nothing held, no card.** The cell's four library cards (covariates inside the
  mixed model, allometric centring, exposure-response confounded by clearance, BLQ as censored) and the field's
  forecast (a population model on the monitoring levels, each patient read at its own levels, the new regimen
  simulated) were taken as the default path. Two candidates measured on code (scratchpad `b178p/proto`: `titr.py`,
  `ddi1.py` to `ddi3.py`; `pk_screen.out` byte-identical with `pk_screen_run2.out`), sixteen on paper.
  - **Measured: a titration-to-goal phase 2 carried to a fixed-dose phase 3 arm** (600 patients, 10, 20 and 40 mg,
    uptitrated at weeks 4 and 8 when the week's response missed goal, Emax on concentration, between and within SD 8,
    EC50 CV 0 and 0.5, three seeds each; graded figure the 20 mg arm's mean week-12 response). The final-dose group,
    a cross-sectional dose regression and the uptitrated patients' paired change (which carries regression to the mean
    from selection on a noisy week) miss the truth (13.0 to 14.6) by 11 to 28 per cent, but the random-intercept mixed
    model on every visit with the dose as a fixed effect, the reflex for repeated measures, lands it within 0.0 to 0.4
    units in all six runs, because an uptitration made on the observed response is missing at random. Dead: the
    golden is the reflex.
  - **Measured: a strong CYP3A inhibitor's healthy-volunteer AUC ratio carried to renal-function bands** (dual
    impairment: a drug about 45 per cent renally cleared, the inhibitor taking the non-renal pathway to about 0.3, a
    triazole prophylaxis switch putting every 2027 patient on it; graded figure the dose per label band matching each
    band's own exposure). The uniform ratio (1.53 to 1.70) overstates the dose by 22 to 29 per cent in the 30 to 59
    mL/min band and 42 to 50 per cent in the 15 to 29 band, but the golden family (the two-pathway split by plain or
    log-weighted fit of the patients' clearances, by the volunteers' urinary fraction or by their urine clearances,
    times the inhibited remainder by the urine geometric mean, the ratio of means or the plasma ratio with the
    urinary fraction) spreads 3.6 to 14.8 per cent of the dose in every band over eight seeds, because the inhibited
    remainder is a difference of two measured clearances; and the fraction-weighted static interaction model is the
    field's taught correction, which this round's lesson 1 places on the default path. Dead on measurement.
  - Paper: the response read at the trough of a monthly regimen from draws spread over the dosing cycle (a phase 3
    end point drawn before the week-24 injection): time-matched PK-PD is the field's route, and stripped of nouns it is
    task177 v2's driver, an effect averaged over a recurring cycle carried to one point of it.
  - Paper: QTc under a drug that raises heart rate (Fridericia against an individual correction): the correction is
    the outcome's definition, so filing it is rule application and leaving the guidance's QTcF is a fork.
  - Paper: toxicity read on the peak under a twice-daily to once-daily switch, and a hazard varying within the dosing
    interval under an interval extension: the switch itself prompts the exposure-metric comparison every
    exposure-response reader runs, and the extension's troughs sit below the record's, informed only by delayed
    doses (the attaining subset, task179's death).
  - Paper: regression dilution of an exposure-response slope fitted on sparse exposure estimates: the dose arms'
    means are the reflex, and task501 killed it as a magnitude.
  - Paper: flare-triggered monitoring samples biasing clearance upward: the inflammation markers the field already
    puts on clearance absorb it, and without them it is unidentified.
  - Paper: dose reductions after grade 2 toxicity that intercepted grade 3, carried to a fixed-dose combination with
    no lower strength: identified only by the few patients not reduced, through a multistate fit whose form forks.
  - Paper: an active metabolite carrying the effect under a forward CYP2D6 inhibitor: the poor metabolisers are the
    attaining subset and the metabolite's potency is a dossier fact.
  - Paper: prevalent against new users in a monitoring register (depletion of the susceptible): the new-user filter is
    the sister task type's first card; monitored courses as the population for a hospital-wide dose table: reweighting
    on the covariates that drive monitoring is a reflex, otherwise unidentified.
  - Paper: lung epithelial lining fluid against plasma target attainment for a pneumonia dose: textbook, and the
    bronchoscopy study is a single-purpose file; first-isolate de-duplication of the MIC distribution: hygiene a
    medium reader runs; healthy-volunteer against patient clearance in a subcutaneous bridge: the standard bridge
    transports absorption only.
  - Paper: a time-dependent inhibitor or an inducer short of its new enzyme steady state in the interaction study:
    the turnover model's form and degradation constant fork or are a literature constant; smoking cessation on
    admission under a smoke-free policy de-inducing CYP1A2: the smoking covariate is textbook and cigarettes per day a
    composition.
  - Paper: degradation in late-processed specimens and immunoassay metabolite cross-reactivity: Layer 1 carrying the
    stump.
  - The cell finding, now on three builds (task170, task179, task178): the field's forecast already conditions each
    patient on its own concentrations and names every elimination pathway, so what it misses is an extrapolation past
    the record informed by an attaining minority, a correction the field teaches (fraction-weighted interactions,
    time-matched PK-PD, a mixed model over a titration), or a difference of measured clearances whose estimator family
    spreads as wide as its lever. The cell is spent for this round.
- **Third rebuild cell, quantitative-finance / volatility-derivatives-pricing (Forecasting), screened 2026-10-23.**
  task177's screen of the same cell read first (candidate G, dealer gamma, measured dead; seventeen on paper; a
  volatility level carries a 5 to 14 per cent model spread), with the field's routes (the record's realised volatility,
  GARCH or HAR on it, implied volatility, event-volatility stripping, the term structure) taken as the default path.
  Dead on paper, one line each:
  - a results day carrying a preliminary trading statement's news once statements are abolished: one step once the
    rule change is read (add the statement day's variance);
  - semiannual reporting doubling each report's accumulated news: one step once read, and the semiannual reporters
    already on file are the attaining subset;
  - limit-lock runs merged into latent moves under a widened daily price limit: for the variance the multi-day return
    lands (task135's estimator), for the tail the censored-t fit is the taught correction, and the new limit replayed
    on latent moves is rule application;
  - a narrowed limit splitting moves for a variance swap on daily settlements: the filed limit rule executed on the
    record's moves is rule application;
  - employee stock options' expected term read on moneyness: the exercise-multiple lattice is the field's taught method
    and the simplified-method term sits near the golden;
  - a currency near the edge of a credible band: the reflected terminal distribution follows from the filed band
    (rule application) and the compression is a fitted nonlinearity;
  - commodity option volatility on hub-level days of cover: a regression on the obvious covariate (the brief's measured
    death), with past low-stock days the attaining subset;
  - rate volatility on a normal-against-CEV backbone with the forward level outside the record: a fitted nonlinearity
    extrapolated, forking on the exponent;
  - a calendar strip or average-price option: the averaging formula is textbook and the strip's own price series is the
    attaining subset;
  - same-day and morning-settled options: the record measures each window directly, or the settlement time is a
    contract reading (semantics);
  - an exporter's surrender requirement routing its dollars through the market: task169's driver in FX nouns (a
    closed route's events through the remaining route's conversion), and the signature BLOCKs against task169;
  - the results season's single-stock jumps on each name's own baseline: event-volatility stripping is textbook and the
    lever is under 10 per cent of the volatility;
  - a central bank answering the customer flow it sees rather than the move: the net-flow regression is consistent and
    the reflex lands;
  - leveraged-fund rebalancing amplifying closes, the fund closing: candidate G's twin with the sign reversed, a
    regression on a shipped covariate;
  - pre-announced intervention auctions as the instrument: the impact of an anticipated flow differs from a surprise
    one, so it is unidentified.
  - Held and drawn: the central bank's leaning spot operations ending (`## Draw`), measured on code (c1_fx.py to
    c1t.py) before the card.
- **Architecture 3 at stage 3, tried and dropped while building (2026-10-23).** A clients-due count per quarter in ask
  B: the window device moved it in only two of four quarters in every realisation scanned, so the count was cut and
  ask B carries the eight notionals. The central bank's operations log in UTC and in millions beside the dealers'
  local hours and thousands: mishandled, either conversion collapses the instrument route to the record's own
  neighbourhood (8), so Layer 1 would have carried part of the call (R2 failed); both now share one clock and one
  unit. Dealer refilings whose first report was a thousandfold keying error: summing receipts then broke the
  instrument route (R2 failed); the first reports are now a sign error, the previous hour's figure or a partial
  figure, and every handling of refilings keeps 12. A desk-orders realisation whose ask A cells sat within 0.002 of a
  rounding edge: re-drawn (stream desk_orders/15, every cell 0.009 or more inside its bin).
- **Architecture 3, the central bank's leaning spot operations ending: spent at stage 4, Gate F (2026-10-23, zip
  6a710f5b).** Blind reader B landed the call, 7 of 7 call figures (12 per cent, settings 12 and 13 covering): "Hourly log
  mid change regressed on customer net dollar flow and BCT net sales; BCT trades when the hourly move exceeds ~5 pesos so it
  is endogenous, so estimated by 2SLS with hinge terms of customer flow as instruments ... counterfactual about 11.4 per
  cent (11.0-11.6 over the kappa range), rounded up to 12". The paper risk named at the draw came true: an agent that leans
  against each hour's move is an endogeneity a medium reader spots in the operations file and instruments by itself, so
  the decisive step was a taught correction (lesson 1). Asks leaked 16 of 24 (66.7 per cent): ask A's sweep device was
  absent from the reader's path (it grouped fills by UTC time, trader and side and kept only confirmed rows); ask B held
  (window forwards kept by maturity date). Reader A and the judge were stopped; the card is marked spent.
