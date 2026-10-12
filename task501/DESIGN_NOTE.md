# task501 design note

Private, never ships. Architecture 3 of the slot, redesigned at stage 2 on 2026-10-12 after the v2 portal result
(both responses landed CHF 250 million by executing the walk-forward the directive filed in full). The first
v3 design kept that walk-forward as a filed execution layer and moved the decisive step to the buffer's
estimand, which the directive also filed ("at any point in a horizon"); under the readability screen both
steps are rule application and the buffer rung is readable, so this redesign replaces the decisive step,
the directive and the asks, and keeps the world (the programme, its managers and funds, the lender and the
facility decision). The replaced design is in git history and in `## Tried and rejected`. Stage 4 (2026-10-12): the
determinism judge found the golden 2.6 per cent above its bin's floor with the fit window unfiled; the repair filed the
estimation period in RL-PM-05 s.5.2 (the programme's whole history since 2015, a period and no method) and tightened the
world (the four funds' pacing, the spread of the drawn share at a period end) so that every member of the golden family
sits at least 2 per cent inside the bin; the figures below are the repaired build's.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task501.json`, architecture v3 with lineage v1, v2 and the v3 first decisive step; `guard.py check` WARN on one finding (repeat.gate_g against task181, answered below), registered 2026-10-12 |
| Domain / task type | quantitative-finance / liquidity-funding-balance-sheet (the author's declared task type inside the client's Quantitative Finance domain): a private-markets programme's liquidity for unfunded commitments |
| Objective | Forecasting & Predictive Modeling: the expected capital calls of calendar 2027, which size the facility |
| Shape | 07, a grid of cells: the call (one facility amount) with the year's fees at it and at the next amount down, and the cash received from distributions in 2026 by strategy and quarter (16 cells and 4 year totals) with the chart's bar labels and title |
| Gate G mechanism | forecasting |
| Gap, pattern, generators | time, then population; pattern none; G6 decisive (composition shift: the funds whose investment periods end inside 2027 are far behind schedule, a mix the record's closed funds never had at their deadlines), G13 (horizon: the deadlines fall inside the forward window), G7 (operating window: the investment period closes the undrawn balance to new investments) |
| Stump strategy / class | composition_mix / analytical |
| Layer 2 family / pattern | field_method / `own:investment-period-deadline-drawdown` |
| Decisive rule filed, official decoy, validated decoy | no, no, no |
| Decision / unit | dial_setting: the facility amount from the lender's menu, CHF 50 to 400 million in steps of 25 million |
| Calibration / context artifact | existing_book_actuals (the programme's own funds whose investment periods have ended, read from the ledger) / register (the programme register, static contract terms) |
| Stakeholder / forum / event / organisation | the head of treasury and liquidity (finance_controller) / the Stiftungsrat (trustees_or_governors) / the lender's facility election (purchase_order_or_contract) / foundation_or_funder: a Swiss Pensionskasse is a pension foundation (Stiftung) governed by its Stiftungsrat and supervised as a foundation, not a FINMA financial institution, and financial_institution also repeats task446 |
| World | Pensionskasse Werdinsel, Zurich, CHF; commitments in USD, EUR and CHF to 51 funds of 20 managers, vintages 2015 to 2026; Privatbank Lindenhof AG offers the facility. People drawn with `guard.py names --geo Switzerland --seed 501`: Domenica Hürlimann (Treasury & Liquidity), Torsten Sigrist (Portfolio Management), Noémie Hess (Rechnungswesen), Jeremias Ritter (president of the Stiftungsrat), Lazar Marti (the bank). None appears in the prompt |
| As-of | records to 31 December 2026 (the plan date); the extract runs Tuesday 5 January 2027 and the pack is assembled after the last message of 6 January (the files' time); the lender needs the election by 15 January 2027; the golden paper is dated 8 January 2027; the facility year is calendar 2027 |

**Data-native sentence.** A fund may draw its commitment for new investments only until its investment period ends,
and in the programme's record every fund whose period has ended had drawn 92.2 to 93.3 per cent of its commitment by
then (92.6 on average), including the five slow starters that were 49.6 to 69.6 per cent drawn a year before their
deadlines; the four funds committed in late 2022 and late 2023 (Loschwitz Equity III, Juneau Infrastructure Partners
II, Rosenthal Buyout Partners II, Tessin Private Credit I) did most of their first years in the 2023-24 deal drought,
are 45.6 to 61.8 per cent drawn on 31 December 2026 and reach the end of their investment periods between 20 September
and 18 December 2027, so their 2027 calls are set by the balance they still have to draw before their deadlines, which
no age curve fitted on funds that kept to schedule can see.

**The pairing and the swap test.** The deciding quantity is a commitment-pacing forecast, the capital calls a
private-markets programme will receive, the core liquidity estimate a pension fund treasury makes for unfunded
commitments (Takahashi and Alexander's model is the field's textbook form: calls as a rate on the undrawn
commitment by fund age). With another field's nouns there is no commitment drawn by a manager, no investment period
that closes the undrawn balance to new deals, no fee charged on commitment during that period and no follow-on
regime after it, so the task stops reading the same.

**Sources read, and how this build differs** (`stumping` Part 1.3).

- `layer2-rigor-patterns.md` lists no Quantitative Finance patterns; `two-layer-task-design.md`'s field_method family
  (exposure windows, the field's own method done right) is the nearest. Here the exposure is the commitment still
  drawable before a contractual deadline, and the field's pacing model done right conditions on it.
- `strategies.md` F5 (composition: a correct pooled rate does not fit this pool on a property no column names) is
  the family; F1's current form (a clock process already in the data, estimated from every unit that went
  through it) is the footing: every closed fund went through its deadline in the record.
- Exemplar "Treasury Cash Flow Forecasting" (economics, 0.41) and "Capital Grant Drawdown Forecasting" (nonprofit,
  0.34): the depth a cash-forecasting task carries; their traps (a loss function, a schedule anchor) are not used.
- `measured-drivers.md`, held group: "Capital fund drawdown" (0.40) held because the back-test passes by
  construction and the forward population differs on an axis only a case log shows. This build's default
  back-tests within 4.6 and 0.9 per cent on 2025 and 2026 for an honest reason (no fund reached its deadline behind
  schedule in those years), and the forward group differs on its position against a deadline the register states.
- `examples.md` 1 (task133): the textbook rate applied without conditioning on where each unit stands; task133
  conditions a credit curve on survival, this build conditions a pacing rate on the drawable balance and a deadline.
- The portal record of this slot: v2 landed because the method was filed; nothing about the method is filed now.

**Abstraction and same-puzzle tests.** Stripped of nouns: a unit's forward draw on what remains of its allotment
is set by how much it must still place before a hard deadline, because every unit whose deadline has passed had
placed all but a small reserve by it; a draw rate pooled by age over units that kept to schedule gives a group
that fell behind the same modest share. The nearest drivers (`guard.py check`): task59 v2 at 0.08 (new episodes
capped at the weeks they can draw before a window closes: a cap on new entrants, not a deadline that forces a
balance out), this slot's v1 at 0.08 (an age rate capped at a balance restored by a hidden term: dead, and nothing
is hidden here), task133 at 0.06 (a curve conditioned on survival to date: a different latent state and
correction), task120 v3 at 0.05. Gap, pattern and Gate G (time, G6, forecasting) and gap, pattern and decision type
(time, G6, dial_setting) repeat no build in the last twelve; earlier codings with pattern E or G14 decisive collided
with spent signatures (task117, task37, task44, task97; task124) and were not used. WARN repeat.gate_g against
task181 answered: task181's forecast is a delayed-reporting nowcast by laboratory route; this one is a pacing
forecast under a contract deadline, and forecasting is the honest Gate G mechanism for both.

**Prompt shape and criteria arithmetic.** The call (1) and its critical components (the deadline group named, its
undrawn commitment, the closed funds' drawn share, the fees at the amount and at the next amount down: 5); the
distributions received in 2026, four strategies by four quarters (16) and the four year totals (4); the chart's
four bar labels and its title (5); the two files and the chart's form (3). 34 criteria from the structure of the
answer, none stacked.

## Default path

The pipeline the measured opponent builds unsteered from the prompt's words and the files' grain: the field's
textbook pacing model, done well. Figures measured on the built pack (`generator/figures.json`, `checks.py`).

1. Read the notice ledger, keep the issued capital-call lines (investments, management fees, partnership expenses;
   withdrawn notices out), date each by its value date, translate at the plan-date reference rate, and build each
   fund's monthly calls and its unfunded commitment (commitment less calls) at 31 December 2026, every fund in the
   register included.
2. Estimate the programme's monthly call rate on unfunded commitment by fund age, twelve-month bands counted from
   each fund's first call, as the ratio of summed calls to summed unfunded commitment over the record.
3. Schedule 2027 month by month: each fund's band rate times its unfunded commitment, capped at what is undrawn,
   the unfunded commitment reduced after each month.
4. Sum: CHF 236.1 million of expected calls in 2027. Check it: the same model run from the end of 2024 and of 2025
   forecasts the next year's calls within 4.6 and 0.9 per cent (from the end of 2023 it over-forecasts the drought
   year 2024 by 20.6 per cent, which reads as the market, not the model).
5. Apply the directive: expected calls plus a tenth, less the CHF 150 million reserve, CHF 109.7 million, and the
   smallest amount on the lender's menu that covers it.

**Ends on:** CHF 125 million (CHF 236.1 million of expected calls, a requirement of CHF 109.7 million).

**Golden:** CHF 225 million (CHF 329.3 million of expected calls, a requirement of CHF 212.2 million, 12.2 million above
the bin's lower edge and 12.8 million below its upper; in expected calls the bin runs from 318.2 to 340.9 and the golden
sits 3.5 per cent above the floor and 3.4 per cent below the ceiling).

The other natural routes also land short: the age bands split by whether the fund is still in its investment
period (R1b) 107.8 and CHF 125 million; rates by months to the investment-period end (R2) 127.3 to 147.4 and CHF 150
million; the strategy-by-age table (R1s) 128.8 and CHF 150 million; each fund's own 2026 rate (R3own) 85.8 and CHF
100 million. The programme's 2026 calls carried forward (R0, CHF 310.0 million at the plan-date rates with the franc
commitments at par, 310.6 at value-date rates) give 191.0 and CHF 200 million: 2026 had no fund reaching its deadline
behind schedule.

## Stump sentence

A competent solver forecasts 2027 calls fund by fund with the programme's age-band call rates on unfunded
commitment, files CHF 236.1 million of expected calls and elects CHF 125 million; the step that lands it there is
giving Loschwitz Equity III, Juneau Infrastructure Partners II, Rosenthal Buyout Partners II and Tessin Private
Credit I, which deployed slowly through 2023-24 and whose investment periods end between September and December 2027
with 45.6 to 61.8 per cent of their commitments drawn, the call rate of funds their age, when every fund whose
investment period has ended in the record had drawn 92.2 to 93.3 per cent of its commitment by then, so those four
call about CHF 170 million in 2027 rather than CHF 80 million and the facility is CHF 225 million.

## Three rules

**Domain test:** the deciding quantity is a private-markets commitment-pacing forecast, the capital calls each fund
will make from its undrawn commitment, governed by the investment period its limited partnership agreement allows
for new investments; the field's model (calls as a rate on undrawn commitment by fund age) done right conditions on
how much a fund must still draw before that period closes. With another field's nouns there is no commitment drawn
by a manager, no investment period, no fee on commitment and no follow-on regime, and the task stops reading the same.

**Analyst test:** a strong analyst who reads every term right (calls by value date with fees and expenses, every
commitment in the register, the plan-date rate, the reserve and the tenth, distributions not credited, withdrawn
notices out) and fits the field's standard pacing model, age-band call rates on unfunded commitment, files CHF 236.1 million of expected calls and elects CHF 125 million against CHF 225 million, because the model gives the four
funds whose investment periods end in late 2027 the call rate of funds their age instead of the balance they must
draw before their deadlines. The easy way gets it wrong, so the stump is analytical.

**Layer 1:** call and distribution notices withdrawn by the manager and reissued under a new number; notices of
several lines (investments, management fees, partnership expenses; returns of capital, gains, income); currency
codes in mixed case and descriptions with stray spaces as the clerks keyed them; from January 2026 the custodian's
feed loads distribution advices as single lines beside the clerks' line-by-line keying of the same notices, which
ran in parallel until the end of September; custodian credits arriving a few days after the payment date the notice
states, and some booked the day after their value date; distributions in specie of listed shares; manager
statements received months after the period end, seven third-quarter statements still outstanding; audited
capital accounts at fund and year-end grain beside the line-level ledger; quarterly look-through holdings with
NACE codes from the managers' reports; a reference-rate table in long form for every currency the custodian
quotes, some per 100 units, without holidays; final closes still to come left blank in the register; German and
English labels across the systems. Each is what these systems produce, and none decides the call.

**Layer 2:** the tempting shortcut is the textbook pacing model, a pooled call rate on unfunded commitment by fund
age, which back-tests well on 2025 and 2026. An expert refuses it for the funds whose investment periods end inside
the forecast year, because a fund may draw for new investments only until that date and the record shows every fund draws to 92.2 to 93.3 per cent of commitment by it, however far behind it was; the pooled age rate averages them
with funds that kept to schedule. The rigorous method forecasts those funds from the balance to the closed funds'
drawn share by their deadlines and the rest from the pacing model.

**Gate G.** Litmus: no reported number is wrong and no conclusion is overturned; the ledger, the register, the
audited accounts and the age-band rates are all correct, and the age-band model is a fair description of the
record. Mechanism forecasting; surface_read_dependency no; sole_data_defect no. Clean-data test: with every Layer 1
item repaired in the generator, the default still lands at CHF 125 million and the golden at CHF 225 million
(asserted). Deletion test: no shipped artifact forecasts calls or ranks facility amounts; deleting every
distractor and every Layer 1 item moves neither answer. Lens swap: the default and the golden forecast the same
population's calls over the same year at the same rate; they differ in how four funds' calls are generated.
Identity test: 2027 calls are not an identity over shipped quantities (the four funds' undrawn commitments are
shipped; how much of them is called in 2027 is not). Corpus direction: the closed funds confirm the deadline
drawdown and nothing in the pack files the age-band model as policy.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 battery | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the programme's 2026 calls carried to 2027 | no | no | fires: the run rate is every treasurer's first number | no | no | fires: one reported total | readable |
| R1 age-band call rates on unfunded commitment (the default) | no | no | fires: the textbook pacing model | no | no | no | readable |
| R1b age bands split by whether the fund is still in its investment period | no | fires: the register's investment_period_end column | fires: holding the pool to a visible attribute | no | no | no | readable |
| R2 rates by months to the investment-period end | no | fires: the same column, made into a clock | fires: a visible attribute turned into bands | no | no | no | readable |
| (decisive) R3 the funds whose investment periods end in 2027 draw the balance to the closed funds' drawn share by their deadlines | no: the register states each fund's investment-period end and the agreements' standard limit on calls after it; no sentence names a target share, a balance, a catch-up or the pace of slow funds | no: no column, code or flag marks a fund as behind schedule or carries a drawn share at a deadline; the drawn share is a construction from the ledger and the register | no: it is not pooling, stratifying on a visible attribute, trending, reweighting, shrinking or building an analog on visible attributes; the reflexes with the deadline (R1b, R2) land short | no: the age-band model back-tests within 4.6 and 0.9 per cent on 2025 and 2026, and no control total, statement or published figure carries a forecast | no: every join resolves, no duplicate or fan-out points at the four funds | no: the balance is a commitment times a share no file reports, applied only to funds selected by a deadline inside the window | silent |
| Over-correction: every undrawn franc of the four funds called by the deadline | no | no | no | no | no | fires: the unfunded commitment as reported | readable |

The decisive rung's quantity is named by no sentence and no column, it is not a reflex, no control sees it, the
battery comes back clean on the wrong path and it is not linear in a reported figure. Both shapes the record says
hold are present: a quantity the solver believes needs no construction beyond the textbook model (the forward calls
of four ordinary funds), and the maturity attack's form (the four funds' drawdown happens after the extract, the
closed years tie under the default because no fund met its deadline behind schedule in them, and the evidence sits in
the closed funds' paths the default never examines).

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. Section numbers are those of the
directive (`richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx`); every quoted sentence is asserted verbatim in the
shipped text by `checks.py`, which also computes and asserts the call under each alternative.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | facility amount | one of the lender's amounts, CHF 50 to 400 million in steps of 25 million | any amount equal to the requirement | CHF 212.2 million, not an amount the lender offers | term sheet ("One of CHF 50, 75, 100, ... 375 or 400 million") and s.4 ("the smallest facility amount offered by the lender") |
| SF2 | for 2027 | the facility year, 1 January to 31 December 2027 | the twelve months from the election date | same call (the four deadlines fall inside 2027 either way; asserted) | s.2.6 ("Facility year: the calendar year for which the facility is elected") |
| SF3 | expected capital calls | the expected (mean) total of the year's calls | a prudent or stressed figure | higher, a cushion on top of the filed one | s.4 (the margin is the stated prudence: "expected capital calls of the facility year plus one tenth of them") |
| SF4 | capital calls | every amount a manager calls against the commitment: investments, management fees and partnership expenses | investments only | CHF 200 million (asserted) | s.2.2 ("for investments, management fees or partnership expenses") |
| SF5 | calls of the facility year | calls with a value date in 2027 | calls noticed in 2027 | same call: no notice issued by 31 December 2026 is due in 2027 (asserted) | s.5.1 ("A call is in the facility year when its value date is, whenever it was noticed") |
| SF6 | which commitments | every commitment in the register at the plan date | active funds only, or commitments signed after the plan date too | same call for the first (every registered fund has called by the plan date; asserted); the second has no filed size and is excluded | s.5.1 ("on every commitment in the programme register at the plan date"; "Commitments signed after the plan date are funded from the commitment budget and are not in the plan") |
| SF7 | currency | every amount at the reference rate of the plan date | each month's rate or a forward | not computable: the rate file ends on the plan date (asserted) | s.4 ("translated at the reference rate of the plan date") |
| SF8 | the reserve | CHF 150 million deducted | no reserve deducted | CHF 375 million (asserted) | s.3 ("a reserve of CHF 150 million") and s.4 |
| SF9 | the margin | one tenth of the expected calls | none | CHF 200 million (asserted) | s.4 ("expected capital calls of the facility year plus one tenth of them") |
| SF10 | distributions | not credited against calls | 2026's distributions netted against the calls | a lower amount (asserted) | s.4 ("they are not credited against calls") |
| SF11 | withdrawn notices | no cash effect; the reissue carries the call | counted as well | same call (asserted) | field notes ("A withdrawn notice has no cash effect; the manager reissues it under a new number") |
| SF12 | the plan date and the extract | 31 December 2026, the extract's close | the extract's run date, 5 January 2027 | same call (no notice dated after 31 December 2026 is in the extract; asserted) | s.2.5 ("Plan date: 31 December of the year before the facility year") and the extract log |
| SF13 | unfunded commitment | commitment less calls with a value date to that day | less calls noticed to that day | same call (asserted) | s.2.4 ("Unfunded commitment: the commitment less the capital calls with a value date on or before that day") |
| SF14 | rounding path | the requirement unrounded, the amount the menu's | expected calls rounded to the million first | same call (asserted) | s.4 and the term sheet |
| SF15 | a fund's investment period | the dates in the register | the period counted from the final close | CHF 125 million (asserted): the four deadlines move into 2028 | the register (sheet Fonds, investment_period_end; sheet Hinweise: "as stated in the limited partnership agreement; no extension has been requested") |
| SF16 | the year's fees | 0.30 per cent of the amount for the availability period and 0.15 per cent flat | a day count on a per annum rate, or January at another amount until the election | not open: the fee is a share for the period and the amount runs for the whole period (asserted) | term sheet ("0.30 per cent of the facility amount for the availability period"; "available in that amount for the whole availability period") |
| SF17 | the estimation period (the records a rate or a drawn share is measured on) | the programme's whole history, 2015 to the plan date | a recent window: fits from 2019, 2021, 2022, 2023, 2024 or 2025 onward | CHF 225 million from 2019, 2021, 2022, 2023 and 2025; CHF 200 million from 2024 (asserted, figures.json `window_variants`) | s.5.2 ("from the programme's own records as they stand at the plan date, over the programme's whole history since its first commitment in 2015"); the ledger and the register start in 2015 (asserted) |
| SF18 | the term sheet's covenants (NAV at least CHF 900 million; the facility not above 25 per cent of NAV) | conditions the elected amount meets | a cap on the amount computed from the programme NAV | same call: the NAV is CHF 1,231 to 1,418 million on every reading of the NAV register (30 June or 30 September 2026 as received, or each fund's latest statement; booked francs or the plan-date rate), so a quarter of it is above CHF 250 million (asserted) | term sheet ("Covenants") read with the NAV register; the readings converge (C1) |

The stump is none of these readings: the default and the golden read every term the same way and differ only in
how four funds' 2027 calls are forecast (the lens-swap assertion: the four carry over 90 per cent of the difference).

## Ladder

Requirement = expected 2027 calls plus one tenth, less the CHF 150 million reserve; the facility is the smallest menu
amount at or above it. Measured on the built pack and asserted in `checks.py`: every rung's amount, and every wrong
rung at least 7 million outside the golden bin (CHF 200 to 225 million).

| Rung | Construction | Expected calls | Requirement | Amount | Killed by |
|---|---|---|---|---|---|
| R0 | the programme's 2026 calls carried forward (plan-date rates, franc commitments at par) | 310.0 | 191.0 | 200 | 2026 had no fund reaching its deadline behind schedule; the run rate misses the four funds' balances |
| R1 (default) | age-band call rates on unfunded commitment, pooled, 12-month bands from the first call | 236.1 | 109.7 | 125 | the four funds behind schedule draw their balance before deadlines inside 2027 |
| R1-6, R1fc, R1m | the same with 6-month bands, age from the first close, or the mean of fund-month rates | 230.9 to 245.1 | 103.9 to 119.6 | 125 | as R1 |
| R1b | age bands split by in or after the investment period | 234.4 | 107.8 | 125 | as R1; the split lowers the four funds' last months further |
| R1s | the same by strategy and age band | 253.5 | 128.8 | 150 | as R1 |
| R2 | rates by months to the investment-period end, 3-, 6- or 12-month bands, pooled or by strategy | 252.1 to 270.3 | 127.3 to 147.4 | 150 | the deadline band's rate pools funds that kept to schedule (small balances) with the few that did not |
| R3own | each fund's own 2026 call rate on its unfunded commitment | 214.3 | 85.8 | 100 | a fund's own last year says nothing of the deadline ahead |
| R3 (golden) | the funds whose investment periods end in 2027 draw the balance to the closed funds' mean drawn share by their deadlines, then the band rate on the rest; every other fund on R1 | 329.3 | 212.2 | 225 | |
| X1 | every undrawn franc of the four funds called by the deadline | 377.4 | 265.1 | 275 | every closed fund kept 6.7 to 7.8 per cent of commitment undrawn at its deadline |
| X2 | the balance to the drawn share spread evenly to every in-period fund's own deadline | 291.1 | 170.2 | 175 | funds with deadlines after 2027 deploy ahead of an even spread in the record |

**Arithmetic.** Position: the default is four amounts below the golden; R2, the nearest reflex, three below; X1 two
above. Every correction a solver adds to R1 (strategy, the in-period split, months to deadline) walks the
requirement up by at most 37.7 million and none reaches the golden; only the deadline balance on the four funds moves
it into the golden's bin (the decisive move is 102.5 million, 2.7 times the largest reflex, asserted over 1.5). The
golden is bracketed: every under-construction lands below, every over-construction above. Dominance: the four funds'
balance to the drawn share (CHF 168.3 million) against what the default gives them (CHF 79.7 million) is 2.1 times
(asserted over 1.8). R0 sits 9.0 million below the golden bin's floor, the nearest wrong rung.

**The golden family (C3), measured on the filed estimation period.** RL-PM-05 s.5.2 now files the period the plan is
estimated on, the programme's whole history since its first commitment in 2015; the method stays open. Every choice a
careful solver could make on that record, one at a time, lands on CHF 225 million at least 2 per cent of expected calls
inside both edges of the bin (318.2 to 340.9; asserted in `checks.py`, the five corridor cases again in `verify.py`):

| Member | Expected calls | Requirement | Margin to the nearer edge |
|---|---|---|---|
| canonical (12-month age bands from the first call, pooled, the closed funds' mean drawn share) | 329.3 | 212.2 | 3.41% |
| 6-month or 24-month age bands | 329.3, 327.6 | 212.3, 210.4 | 3.39%, 2.96% |
| age from the first close | 332.1 | 215.3 | 2.58% |
| age bands by strategy, 12 or 6 months | 329.6, 328.7 | 212.5, 211.6 | 3.32%, 3.31% |
| target the median, the strategy's mean, the lowest or the highest drawn share of the 27 closed funds | 329.1, 329.2, 326.5, 333.3 | 212.0, 212.2, 209.2, 216.6 | 3.44%, 3.42%, 2.62%, 2.23% |
| the balance for the four funds behind schedule only, the six on the band rates | 326.5 | 209.2 | 2.63% |
| the post-period rate (age band, after the period end) on what remains after a deadline | 326.1 | 208.7 | 2.49% |
| the band rate up to the deadline and a top-up to the target in the deadline month (the judge's form) | 329.4 | 212.3 | 3.39% |
| each fund's first month left out of the rates | 328.2 | 211.0 | 3.15% |

Every one of the 384 combinations of those choices (bands, anchor, pooling, target, catch-up set, post-period rate,
style) lands on CHF 225 million (320.1 to 336.8). Two weaker estimators also land on it with less room: the mean of
fund-month rates (336.8, 1.20 per cent below the ceiling; applied to the record's own fund-months it gives 6.3 per
cent more calls than the record holds, where the ratio of sums reproduces them exactly) and nothing called after a
deadline (321.6, 1.07 per cent above the floor; the register's notes and the record both show calls for follow-ons
after a period ends). With those two added, 52 of 1,152 combinations leave the bin, each one at least three departures
from the canonical, one of them a weaker estimator. A recent fit window is ruled out by s.5.2 (SF17) and
is not a family member; measured for the record, rates fitted from 2019, 2021, 2022, 2023 or 2025 still give CHF 225
million (332.6, 337.0, 325.3, 320.0, 324.8) and from 2024 CHF 200 million (317.1).

## Closure table

| # | Axis | Reading | Closed by |
|---|---|---|---|
| 1 | Population | every commitment in the register at 31 December 2026, each fund with calls by then; commitments signed later are out | s.5.1 filed; every registered fund called by the plan date (asserted, C1) |
| 2 | Unit of account | the fund commitment, in fund currency, translated at the plan-date rate | s.2, s.4 filed |
| 3 | Attribution window | a call belongs to the year of its value date | s.5.1 filed; no notice issued by 31 December 2026 is due in 2027 (asserted, C1) |
| 4 | As-of dating | the ledger as it stood at the 31 December 2026 close | s.2 filed; no notice dated after it in the extract (asserted) |
| 5 | Version basis | issued notices; a withdrawn notice replaced by its reissue | field notes; C1 (asserted) |
| 6 | Denominator | the call rate's base is the unfunded commitment; the drawn share's base is the commitment | s.2 definitions of both quantities; the method's bases are the field's own, and the golden family includes commitment-based post-period rates (C3) |
| 7 | Weighting | ratio of summed calls to summed exposure in a band | C3: the mean of fund-month rates lands on the golden 1.20 per cent inside the bin, and every combination of the careful choices inside it (asserted) |
| 8 | Window length | the programme's whole history, 2015 to the plan date | filed at authority in s.5.2 (SF17); the recent windows computed and recorded in figures.json |
| 9 | Boundary inclusivity | the investment-period end month is inside the period | C1: no call is noticed before and due after an investment-period end (asserted) |
| 10 | Rounding path | figures unrounded to the requirement; amounts from the menu; fees exact | s.4 and the term sheet; the golden requirement mid-bin (asserted) |
| 11 | Tie-break | not used: the requirement never equals a menu amount | asserted: every careful-solver member at least 2 per cent of expected calls from both edges |
| 12 | Maturity and censoring | the closed funds are those whose investment periods ended by 31 December 2026 | C1: no investment period ends between 1 December 2026 and the extract run, so the set is the same at either date (asserted) |
| 13 | Order of operations | each fund's month capped at its unfunded commitment, then reduced | C1: every band rate is under one, so the cap never binds (asserted) |
| 14 | Row order | the ledger's row order does not enter | C1 (asserted over a shuffle) |
| 15 | Duplicate resolution | withdrawn and reissued call notices; the custodian feed loads no call | field notes; the feed's rows are distribution advices only (asserted zero call rows) |
| 16 | Identity normalisation | currency codes folded to upper case | field notes ("the clerks are not consistent about case") |
| 17 | Netting against gross | calls gross; distributions not credited | s.4 filed |
| 18 | Dimensional units | fund currency translated once, at the plan-date rate | s.4 filed |
| 19 | Code and status semantics | line types and statuses per the field notes | field notes; never the stump |
| 20 | Integerisation | none in the call | n/a, asserted that no figure is integerised before the requirement |
| 21 | Clause scope | s.4 sizes the facility; s.5 defines the plan; s.6 the annual report | filed; s.6 states no method |
| 22 | Forward window contents | calendar 2027: the twelve months after the plan date, every registered commitment, no new commitment | s.2 and s.5.1 filed |

## Literal reader

Executing the prompt and the directive word for word: the amount is the smallest of the lender's amounts that, with
the CHF 150 million reserve, covers the expected 2027 calls (by value date, fees and expenses included, every fund in
the register, plan-date rate) plus a tenth, estimated on the programme's whole history since 2015 (s.5.2); every
term has one reading under its SF row, and the readings that differ (SF1, SF3, SF4, SF7 to SF10, SF17) each violate a
quoted sentence. The text files the estimand and the period it is estimated on, not a method, so a literal reader must
forecast; the default's forecast and the golden's are the same estimand on the same population and the same record,
and they differ by method alone. The method is forced by the data's structure: every fund in the record whose
investment period has ended drew to between 92.2 and 93.3 per cent of commitment by its end, slow starters included,
so a forecast that leaves the four funds about half drawn at their deadlines contradicts every closed case, while every
member of the golden family, whatever its pacing details for the other funds, lands in the same amount at least 2 per
cent of expected calls inside the bin (asserted). The write-up's steps pass the same test; step 2 measures each closed
fund's drawn share at the end of its own investment period, and the R0 figure states its rate basis.

**The leak reader's readings (stage 4), answered.**

- *The custodian's franc credit at its dealing rate against the notice at the reference rate of the value date (ask).*
  The prompt asks for the distributions "at the reference rate of the day the cash arrived", RL-PM-05 2.7 defines the
  reference rate as the custodian's 16:00 rate, and the field notes say the statement converts "at its dealing rate":
  the dealing-rate francs are another quantity, stop s4 (every figure off by at least CHF 18.9 thousand, asserted).
- *Quarter by booking date or by value date (ask).* The field notes define Buchungsdatum as the day the custodian booked
  the posting and Valuta as "the day the amount was credited to or debited from the account", which is the day the
  cash arrived; booking dates move five of the 186 credits of 2026 across a quarter end, three of them into 2027, and
  change nine of the 24 figures while the title stays Buyout (measured). The golden quarters by Valuta; no sentence
  supports the booking date.
- *The NAV covenant as a cap on the call.* The term sheet's covenants (NAV at least CHF 900 million, the facility not
  above 25 per cent of NAV) never bind: the programme NAV is CHF 1,231 to 1,418 million on every reading of the NAV
  register, so a quarter of it is CHF 307.8 million or more, above the golden amount and the next amount up (SF18,
  asserted). The NAV register stays a declared distractor: the call is unchanged with it deleted (asserted), and the
  write-up's step 6 says the amount sits within the covenants without a figure of its own.
- *The withdrawn and in-specie lines (ask).* Filed in the field notes (a withdrawn notice has no cash effect; IN_KIND
  settles in securities); neither has a custodian credit, so the credit-matched golden cannot count them.

## Oracles

None. The audited capital accounts agree with the ledger's calls fund by fund under every construction and carry
no forecast; the manager statements carry net asset values and quarterly flows, no forecast; the H1 2025
programme report bridges a closed half-year and shares no figure with the call or the ask; the term sheet lists the
menu and the fees and ranks nothing. The custodian's account statement is the ask's referee (below): it confirms
which distribution notices were paid and when the cash arrived, in francs at the custodian's dealing rates, so it
arbitrates the ask's devices without handing over any graded level, and the call never reads it.

## Ask sheet

**The main call's declared population.** The cells the call reads: the notice ledger's capital-call rows (notice
date, value date, status, line type, amount, currency, fund); the register's fund identifier, currency,
commitment, first close and investment-period end; the reference rates of 31 December 2026; the directive and the
term sheet. The ask reads the ledger's distribution rows, the custodian's account statement, the register's strategy
column and the reference rates of the days distributions arrived in 2026. Device rows inside the call's population: 0
(the custodian feed loaded distribution advices only, asserted zero capital-call rows from the feed). Hazard rows
inside it: 0. `checks.py` asserts the separation by recomputing the call with every distribution row, the custodian
statement and the register's strategy column scrambled: unchanged at full precision.

### Ask A: the cash the programme account received from distributions in 2026 (sheet in `distributions_received_2026.xlsx`, the chart and table in `facility_election_2027.docx`)

| Field | Entry |
|---|---|
| What it asks | For each strategy (Buyout, Growth, Private credit, Infrastructure), the cash the programme account received from fund distributions in each quarter of 2026 and in the year, CHF thousand at the reference rate of the day the cash arrived (20 figures). The chart: one stacked bar per quarter with a segment per strategy, each bar labelled with its total, the title naming the strategy that returned the most over the year |
| Named use | The directive's annual programme liquidity report to the Stiftungsrat (s.6) shows what the programme returned to the general portfolio, quarter by quarter, beside the facility proposal: the board weighs the facility against the cash distributions bring back, which the directive does not credit. H18 home: the component of the facility case that explains why distributions are not credited (their size and timing), from rows and columns the call never reads |
| Primary device | P1, D1 (the same records under two key schemes and grains): from 1 January 2026 the custodian's CF-PM feed loads the distribution advices of the eight managers on its portal into the ledger, one line per advice (the cash amount under the custodian's category, its own reference as the notice number, the custodian's credit value date), while Rechnungswesen kept keying those managers' PDF notices line by line (return of capital, gain, income; the manager's notice number; the payment date the notice states) until the parallel run ended on 30 September (Kalmar's advices from April; the clerks stopped keying Ebersol and Dunmore in July). 52 of the 186 credits of 2026 are in the ledger twice, both issued. Every one of those notices from January to September is in the ledger twice, both issued, in all four strategies. Silent under the battery: no duplicate rows (different identifiers, line counts, descriptions and entry times), keys unique, every join resolves. Visible only at a cross-file cut nothing invites: the custodian statement shows one credit per notice |
| Hazards | h1 (D8, clock): the notice states a payment date and the custodian credits the cash one to four business days later for about one distribution in six (cross-border, USD and EUR); at the four 2026 quarter ends and at both year ends some cross into the next quarter or year, in every strategy, and every late credit is translated at a different day's rate. h2 (D5): one distribution in specie of listed shares (Growth, third quarter) is not cash. h3 (D2): one Private credit distribution notice withdrawn and reissued in the second quarter. h4 (D3): the custodian statement carries francs at its dealing rates, not the reference rate |
| Stops (each a complete pipeline; targets asserted) | s1 the cracker's path: ledger distribution rows, issued, cash only, by the ledger's value date and that day's reference rate: every one of the 20 figures off, by at least CHF 3,608.6 thousand in Q1 to Q3, CHF 720.8 thousand in Q4, CHF 14,168.3 thousand in the year totals and CHF 1,041.2 thousand in the quarter totals, the title naming Infrastructure. s2 ledger rows deduplicated at notice level on fund, total and stated date (the over-cleaner's first move), keeping the clerk's row: the Q1 to Q4 boundary cells off. s3 deduplicated keeping the feed's row: the boundary cells of non-feed managers off. s4 the custodian statement's credits summed in francs (the dealing rates): every figure off by at least CHF 18.9 thousand. s5 lazy (in specie and the withdrawn notice kept): every figure off. Measured smallest misses over the 24 figures: s2 97.6, s3 26.6 (CHF thousand) |
| Golden | each distribution notice once, matched to its custodian credit, cash lines only, in the quarter of the credit's value date, its fund-currency amount translated at the reference rate of that date, grouped by the register's strategy |
| Chart | labels are the four quarter totals of the golden; the title names the strategy with the largest year total. The builder places the golden's top two strategies so that s1 names the other one in the title |
| Span (6 files, 13 columns, causal) | ledger (fund, notice id, type, status, line type, value date, amount, currency); custodian statement (Valuta, Betrag CHF, Referenz, Transaktionsreferenz); register (strategy); reference rates (rate_date, currency, unit, rate_chf); field notes (status, line-type and Valuta semantics); extract log (the statement's coverage). Short of the eight-file floor: the quantity's whole causal path runs through these six systems, and adding a seventh would mean a file built to carry the ask |
| Necessity matrix (target) | one file misread, the rest right: ledger value date taken as arrival, every Q1 and Q4 cell; custodian statement unread, every Q1 to Q3 cell; register strategy unread, n/a (no other strategy source); reference rates unread (dealing rates), every cell; field notes unread (in specie kept), the Growth Q3 and year cells |
| Realism | A custodian feed run in parallel with manual keying for the first three quarters of its life, nobody reconciling the two until the year-end close, is what a migration produces; cross-border credits arriving days after a notice's stated payment date are routine for USD and EUR distributions |
| Referee | the custodian statement: one credit per paid notice, the arrival date, francs at dealing rates; it hands over no graded level |

**Hazard table.** h1 moves every Q1 and Q4 cell (each strategy has a late credit across 31 December 2025 and across
31 December 2026; asserted through s2 and s3) and the Q2 and Q3 cells it crosses; h2 the Growth Q3 and year cells on
the ledger's path; h3 the Private credit Q2 and year cells on the ledger's path; h4 every cell on the custodian-only
path. Composed mishandlings, every subset of {P1, h1, h2, h3, h4} computed over the 25 ask items (20 figures, 4
labels, the title): any subset with h1 keeps at most the title; P1 without h1 keeps at most one item, the Buyout Q4
cell (September notices of the feed managers whose cash arrived in October are in the fourth quarter twice), and loses
the title; h4 keeps the title only; h2 and h3 are inert
on the credit path (neither has a credit) and matter only on the ledger's dates, where h1 already misses everything.

**Cracker sheet.** The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates,
unmatched joins, fan-out, counts that tie), executes every filed sentence and excludes the in-specie line and the
withdrawn notice; on the ask it sums the ledger's issued cash distribution lines by the ledger's value date at that
day's reference rate, which is stop s1.

| Ask row | The cracker's computation | What moves it | Cracker verdict |
|---|---|---|---|
| Q1 2026, four strategies | s1 | P1 (the eight feed managers' notices twice) and h1 (late credits across both Q1 edges) | miss |
| Q2 2026, four strategies | s1 | P1 and h1 | miss |
| Q3 2026, four strategies | s1 | P1 and h1 | miss |
| Q4 2026, four strategies | s1 | h1 (late credits across 30 September and 31 December, other days' rates) | miss |
| Year totals, four strategies | s1 | P1 and h1 | miss |
| Chart bar labels, four quarters | s1's quarter totals | P1 and h1 | miss |
| Chart title | s1's largest strategy | P1 (the builder sets the golden's top two so s1 names the other) | miss |

**Mirror sheet.** The same response at R1, the default path: identical on every ask row (the ask is decoupled), so
the two sheets differ only in the call's criteria.

**Mirror leakage:** 0 per cent of the ask's graded figures on paper (the mirror takes stop s1 like the cracker and
misses all 20 figures, the four labels and the title); the chart's form, which both keep, is graded under the files
and form criteria.

**Pair ceiling:** 29.5 on paper (planning weights 38 / 7 / 55 over 34 criteria: the cracker keeps the call, its five
components and the files, 45.0, and none of the 25 ask criteria; the mirror misses the call and its components but
for the fee arithmetic at its own amount, about 7 of the 38, keeps the files and form, 7.0, and no ask criterion,
14.0; the pair is 29.5, and 32.3 if each keeps a twentieth of the ask weight). The nearest partial path, a response
that dates by the custodian's credits but keeps both records, keeps 1 of the 25 ask items: with the call it scores
about 47, and the pair with the mirror about 31.

**What the pass rests on.** The parallel run. A top response that matches every ledger distribution to its custodian
credit, counts each notice once, dates it by the credit and translates at the credit day's reference rate lands all
20 figures; if that response also lands the call, the pair still clears the bar (about 47 and 14). The ask holds
only while no top response reconciles the ledger's distributions to the custodian statement notice by notice.

## Prompt

`prompt.txt`, one paragraph, question first, two files named, rounding once at the close; `voice-check.py task501`
PASS at 867 characters. It names no person, title, meeting or reader, no input file, no method and no trap word. The
forcing fact is the 31 December 2026 extract. The programme account is qualified as the private-markets programme's
(house fix H20: the domain's institutional noun in the prompt). The ask is worded so that "none" is never needed
(every strategy received distributions in every quarter of 2026, a fact the requester knows).

## Build record

The generator is rebuilt for this design (the first v3 generator is replaced in the same commit as the pack). Run
order: `build.py`, `checks.py`, `verify.py`, `golden.py`, `writeup.py`.

- `world.py`: managers, funds, investment periods, fee terms, the reference-rate anchors, people, dates, the spread
  of each fund's drawn share around the managers' aim at a period end (`IOTA_SD`), the account's operating minimum
  (`MIN_BALANCE`) and `DIST_STREAM`, the random stream of the 2025-26 distribution timings (360, the strongest of the
  four streams of 2,000 that pass every assertion: an in-memory screen of the rounding paths, then the full checks).
- `sim.py`: monthly calls per fund from the first call, a pacing hazard on the remaining investable commitment with a
  market factor (2020 pause, 2021 boom, 2023-24 drought), the deadline drawdown in each fund's last six months, the
  post-period follow-ons; distributions, NAV, holdings.
- `observe.py`: what the systems recorded: arrival lags (the 2025-26 distributions' drawn on the timing stream), the
  quarter-edge credits, the withdrawn notices, the in-specie distribution, the custodian feed's advices beside the
  clerks' keying, and the custodian's statement of the account, where the facility is drawn when a call would take the
  balance under the operating minimum.
- `pack.py`, `docs.py`: the files and documents (container times and PDF information set to each document's own
  dates after the house scrub); `build.py` also writes `metadata.json`.
- `solve.py`: every graded figure from `target/` alone (pandas): the call, the ladder, the golden family (one at a
  time, the weaker estimators, every combination, the recent windows), the back-tests, the ask, its stops and its
  composed mishandlings. `verify.py` recomputes the call, the fees, the corridor's five cases and the 24 ask figures
  with the standard library and openpyxl only. `checks.py` asserts and writes `figures.json`;
  `writeup.py` renders `submission.md` from it; `golden.py` writes the two goldens. `tune.py` is the in-memory
  harness that steered the world; nothing shipped depends on it.

**As built (2026-10-12, after the stage-4 repair).** 14 files in 7 formats (csv, xlsx, docx, pdf, md, txt, json);
the notice ledger 11,223 rows, the reference rates 33,968 rows (the 25,000-row file, used by the call and the ask), the
look-through holdings 27,737 (a distractor). Distractors in `metadata.json`: the audited capital accounts, the NAV
register and the look-through holdings; the call and every ask figure unchanged with all three deleted (asserted).
Free gates: `checks.py` 250 assertions, 0 failed; `verify.py` 0 differences; two consecutive builds byte-identical
(target, goldens, `figures.json`, `submission.md`, `metadata.json`: 19 files); `figures_check.py` 99 figures, 0
absent; container audit clean on the pack and the goldens; `leak.py --asof 2027-01-06` REVIEW, no LEAK (lines below);
`guard.py surface` 0 pairs promoted; `guard.py heart` WARN (answered below); `precut.py` 38 checks, 0 FAIL, 0 WARN; `voice-check.py`
PASS. The repair changed two documents: RL-PM-05 s.5.2 (the estimation period) and the minutes' item 6.1 (the
facility "is repaid from the October transfer": the 24 September sitting could not report a repayment on 2 October).

**leak.py REVIEW lines.** Sweep 3: the directive, the minutes and the term sheet carry the words of the call
(elect, standby, facility, 2027) because they govern it; the reserve and the lender's menu are listed as stated
inputs. Sweep 4: the field notes, the H1 2025 report, the mail, the directive and the term sheet share generic nouns with the stump paragraph (investment, balance, register, notice, reserve, unfunded, period, January, lender, audited, and in s.5.2 history); none names a deadline, a balance to draw, a
drawn share at a period end or the pace of a fund (asserted by the decisive-words sweep in `checks.py`). Sweep 6: the
register and the custodian statement carry the strategy names inside fund names and the register's strategy column;
neither totals or ranks strategies. Sweep 9: the register's investment-period and term ends after 6 January 2027 are
contract dates (forward-looking by nature, on the allow-list); final closes still to come are left blank.

**guard.py.** Heart WARN repeat.gate_g against task181, answered at the draw (an earlier run also warned
overuse.shape, shape 07 in 3 of the last 12: the grid is the ask's own structure, four strategies by four quarters
with the year, not a borrowed skeleton). Surface lists "Kalmar Mezzanine" as a persona: it is a fund manager's name, not a person.

## Portal log

- P1 (v2, 2026-10-11): two of two responses landed CHF 250 million by executing the walk-forward filed in s.5.3.
  Redesigned at stage 2 on 2026-10-12 (this note).

## Stopping rule

Two consecutive portal landings on the golden amount by the deadline route re-root the slot; a landing by another
route, or the asks collected around a landed call, licenses one repair of that layer. A miss licenses nothing.

## Tried and rejected

- v2 architecture (2026-10-11): the walk-forward selection with its mechanics filed in s.5.3 and the buffer as the largest end-of-horizon shortfall; both portal responses executed the filed test and landed CHF 250 million. Retired the same day: a validation whose mechanics are filed is a computation to a strong solver. v3 keeps the test and moves the deciding quantity to the buffer's estimand.
- Candidate set including a trailing twelve-month basis at v3: persistence won the honest test whenever recent vintages paced faster than history; left out.
- Seasonality at 1.35 to 0.65 (first half to second half): the path and end-of-horizon buffers sat 5 to 20 million apart, inside one tranche; set at about 70:30, which puts them 35 million apart.
- Seed sweep 118 to 149 under the sharper seasonality: nine seeds meet the honest margin, the leaky margin and the path separation; 118 kept (the persona draw's seed).
- Reserve at 50, 60 and 70 million with the 25-million menu: the fit-once path-buffer cell or the end-of-horizon cell sat within three million of the answer bin's edges; 75 million puts the answer 12 from both edges and every single-error cell at least 4 from them.
- v1 architecture (2026-10-10): the unfunded commitment restored by recallable proceeds under a term no document stated, pinned by reproducing 180 audited cells; retired 2026-10-11 under the client's 10/10 rules as data semantics and a hidden rule deciding the call (rule 3), and as a backdrop domain under the noun-swap (rule 1). The world, the pack and asks B and C were kept; the recycling term is now filed in the register and the stump moved into the validation.
- Candidate set with a trailing twelve-month basis: persistence won the honest test whenever the recent vintages paced faster than history and landed on the answer tranche; dropped, the three bases are band, strategy and band, manager's own.
- Strategy-coherent pacing shifts in the recent vintages: the strategy-and-band basis then won honestly by 11 per cent and the full-window fit tied the pooled bases, so the leak crowned nothing; replaced by manager-level and fund-year noise, under which the manager's-own basis memorises the past (full window 2.9 per cent against 6.0) and loses forward (17.2 against 9.1).
- Buffer as the second-largest shortfall: the truth and the leaky cell sat within three million of tranche edges at every reserve from 55 to 80; the largest shortfall with a CHF 60 million reserve puts the truth 10.8 and 39 from its edges and every wrong cell at least 4 from its own.
- Pooled rates as the mean of per-fund-month ratios: a fund in run-off with a small audited NAV and one large exit produced ratios above one and dominated the band; replaced by the ratio of sums at the plan-date rate (RL-PM-04 s.5.2, 5.3), which is also what a treasury would write.
- Estimator as rate on unfunded commitment (the Takahashi-Alexander form): the naive and true rates partly cancel because the naive denominator is smaller by the same recallables, and the Gate G label would have moved off binding_constraint; kept the cap form, where the construction is inert unless the cap bites, and built heterogeneous pacing so the recycling funds are the fast deployers whose cap bites.
- Uniform fast pacing: every fund fully drawn by month 24, the later age bands carried no history and the cap never bit under any construction (all constructions on one tranche); replaced by per-manager pacing (fast credit deployers, slower buyout and infrastructure).
- Distributions credited at one half: the programme's run-off distributions swamped the calls and the required facility sat at one tranche for every construction; the directive credits one quarter.
- Age bands 37 to 48 and 49 to 72: the recycling funds straddled the thin fourth band in 2027 and the band rate was too small for the restored commitment to matter; bands set to 37 to 54 and 55 to 78.
- The 2026 prepayment wave drawn from loans funded from January 2024: a third of the wave exited in 2025 and sat inside the audited cells, so the audited roll-forward reproduced most of the answer; the wave is drawn from loans funded in 2025 and exits in 2026 only.
- Short holds from the ordinary hold distribution: the normal draws put exits under eighteen months in half the funds, so commitment less calls missed 96 of 178 audited cells and was not the empirically excellent basis L7 requires; ordinary holds now start above the convergence gap and only the designed quick exits, the two historical flippers and the 2026 wave are short.
- Recallable proceeds attributed to the audited year by realisation date: an exit on 28 December with a January notice put the proceeds in different years under the two readings (one cell unreproduced); attributed by notice date, and no realisation now falls after the 15th of December.
- Reserve at CHF 30, 45 and 55 million: the truth or a wrong construction sat within five million of a tranche edge; CHF 65 million puts the truth 11.1 and 13.9 from its edges and the three wrong bases 8 to 15 from theirs.
- Producer string "Treasury & Liquidity" on the board paper's container: the raw ampersand broke the core-properties XML and the file no longer opened; the deliverables are stamped with the organisation's name.
- Context artifact as the H2 2025 semi-annual report (30 June to 31 December 2025): its closing NAV column is the opening column of ask B, five golden figures in a shipped document (leak.py LEAK); replaced by the H1 2025 report, which shares no figure with any ask.

- Signature rule / B / method_or_model_selection (any decision type): guard BLOCK, spent in 12 earlier builds (test.same_driver_older) and task71 (test.same_puzzle_older). Relabelled honestly: the forward regime is the decisive gap (time first) and the cap at remaining commitment is the Gate G mechanism (binding_constraint).
- Driver variant "late-close equalisation" (a midway entrant's first draw equals the process's draw-to-date on its own size): nearest driver task107 at 0.09, kept out because the catch-up is stated on every real notice and the rule reduces to a readable term.
- Driver variant "notices netted by some counterparties": kept out because the gross lines exist on the notice file and the move collapses to a file choice.
- v3 first decisive step (2026-10-11 to 10-12): the walk-forward kept as a filed execution layer and the buffer read on the month-end path ("at any point in a horizon", s.5.6) instead of the horizon totals; replaced on paper at the 2026-10-12 redesign before any portal test: s.5.3 filed the whole method (rule application, the step v2's responses executed) and s.5.6 named the decisive quantity (readability test 1), and the v3 world also carried a CIO and a portfolio manager each arguing a wrong basis (licensed voices). The redesign files the estimand only.
- Decisive step candidates weighed at the redesign (2026-10-12): a subscription-line overhang (investments closed but not yet called) died on the battery (an unmatched join between holdings and calls is a work order); a quantile of the year's calls with cross-fund dependence died on determinism (a quantile from eleven years of programme history straddles bins under reasonable estimators); a curve conditioned on each fund's position died as task133's driver; seasonality of calls inside the year died as task32's and the first v3's. The deadline drawdown kept: silent, analytical, and forced by every closed fund's path.
- Prototype with the deadline group's investment periods ending April to August 2027 (scratch proto2): the group started drawing down inside 2026, so the default's 2026 back-test missed by 17 per cent on some seeds and a fund's own recent rate reached half the drawdown; the group's deadlines moved to September to December 2027 and the six-month drawdown now starts inside the facility year.
- Card codings with pattern E (time, E, forecasting) and with G14 or G7 decisive: guard BLOCK (spent in task117, task37, task44, task97; G14 in task124; G7 in task229); coded G6 (the composition shift on the deadline position), which the strategy (composition_mix) names.
- Commitment wave of 2024-26 vintages at up to CHF 170 million each (prototype 3): the programme's 2026 calls ran so far above 2027's that the run rate landed inside the golden's bin on one seed in two; the later vintages were cut to a steady CHF 60 to 120 million a year.
- An expected-calls figure, or the next amount down's uncovered amount, as a graded ask: both are method figures that move by several million across the golden family; the prompt asks for the fees at the two amounts, which are exact.
- The look-through holdings as the pack's only 25,000-row file (stage 3): it is a distractor, so the bulk file did no work for the solution; the reference rates now ship in the custodian's long form for every currency it quotes (33,968 rows), which the call and the ask both read.
- Composed-mishandling target "nothing that includes P1 keeps a figure": the parallel run ended in September, so a response that dates by the custodian's credits but keeps both records is right in the five Q4 items; extending the parallel run into the fourth quarter would need a portal manager's fourth-quarter notice in every strategy, which the quarterly income pattern does not give; accepted at 5 of 25 ask items and priced into the pair ceiling.
- One random stream for every observation draw: the year totals of the ask then disagreed with the sums of their rounded quarters (Buyout 95,971 against 95,972), a rounding-path fork; the 2025-26 distribution timings got a stream of their own and streams 0 to 39 were scanned with every assertion plus the one-rounding-path test; 11, 12 and 23 pass, 12 kept (largest stop misses).
- Term sheet with the commitment fee "per annum ... quarterly in arrears" and the 2026 amount running until the election: a day count and a pro-rata January each gave another year's fee; the fee is now a share of the amount for the availability period and the elected amount runs for the whole period.
- The custodian statement's columns glossed only as "booking date" and "value date": reading the day the cash arrived as the booking date moved 19 of the 24 ask figures (credits booked a business day late, six across quarter or year ends); the field notes now say what Valuta is.
- Names within a word of real organisations (a growth manager named after a real biotech's brand, an infrastructure manager sharing a common corporate name, a real fund administrator as a paying agent): renamed Gosford Growth Partners, Juneau Infrastructure Partners and Corvisart Equity Gestion SAS; no figure moved.
- Container times left to the writer and the house scrub: openpyxl stamps the build clock, which sits inside the fiction's band and changed every build (two builds were not byte-identical), and every PDF carried the extract's date and reportlab's "(unspecified)" creator; each document now carries its own created and modified times.
- The v3 world as first built (stage-4 judge, 2026-10-12, NOT_DETERMINISTIC on margin_or_boundary_fragility): the golden's CHF 326.6 million of expected calls sat 8.4 million (2.6 per cent) above the floor of the CHF 225 million bin while RL-PM-05 left the estimation period unfiled, so rates fitted from 2024 gave the judge CHF 312.3 million and CHF 200 million, and the closed funds' drawn-share range (91.8 to 93.8 per cent) alone moved the total 13 million. Repaired by filing the period in s.5.2 (the programme's whole history since 2015) and tightening the world: each fund's spread around the managers' aim at a period end from 0.45 to 0.15 points of commitment, the four funds' pace from 0.38 to 0.36 (Tessin 0.35), which centres the golden at CHF 329.3 million against a bin midpoint of 329.5.
- Closing the fit windows by the world alone (no filed period): the 2024-onward fit stayed under the bin's floor in every world tried, because from 2024 the four slow funds carry 45 to 61 per cent of the unfunded commitment in the age bands of one to three years; milder 2023-24 market factors (0.85 and 0.90) moved it by under a million and pushed the 2026 back-test past 5 per cent. The period is filed instead; the recent windows are recorded, not family members.
- The six on-schedule funds moved out of 2027 (vintages a year earlier, closed by the plan date): the post-deadline and catch-up-set spreads fell under 2 million, but the 2025 back-test of the default went to +11 per cent and the golden fell to 323.9; the six were kept. Shrinking them to 0.5 or 0.7 of their commitments, or moving their deadlines to May to August 2027, lowered the golden 5 to 9 million or took the 2025 back-test past 7 per cent; kept as they were.
- The four funds' paces swept from 0.33 to 0.38 with Tessin's commitment at 170, 174 and 178: 0.34 and lower pushed the 2026 calls (R0) above CHF 317 million, inside 7 million of the golden bin; 0.36 with Tessin at 0.35 keeps R0 9.0 million below the floor and the family's narrowest careful member 2.23 per cent inside.
- The post-period rate as the canonical treatment after a deadline: kept as a family member (2.49 per cent inside), because as the canonical it would leave the lowest drawn share and the 24-month bands 1.6 and 1.5 per cent above the floor.
- Restoring the September 2026 facility draw (the new world's calls left the account CHF 3.3 million above zero) by cutting the pre-October reserve level from CHF 35 to 30 million: it changes a figure the minutes state; replaced by an operating minimum of CHF 5 million below which the treasury draws the facility (drawn CHF 6 million on 18 September). The minutes no longer report the October repayment, which the 24 September sitting could not know.
- The timing-stream rescan on the old arrival draws (streams 0 to 39 with the full checks): the Growth Q2 cell sat 12 francs from a rounding edge in 16 of the 18 streams run because the stream never touched its credits, and none passed. The 2025-26 distributions' arrivals are now drawn on the timing stream; 2,000 streams were screened in memory for the one-rounding-path constraints, six passed, four of them the full checks, and 360 was kept for the largest stop misses (s2 97.6, s3 26.6).
- Architecture after the portal landed v2 (facility election from expected 2027 calls; period-end completion for the four slow funds): spent at stage 4. Pass 1 found margin fragility (a 2024-onward fit window gave 200); the repair filed the whole-history period and tightened the world. Pass 2 found a fork under the call that the period does not close: once the ten funds complete to 92.6 per cent at period end, the remaining funds' base (call rate on unfunded, 329, 225; on commitment, 349, 250) is not separated by the filed records or by back-tests. Two judge passes failed, so the architecture is spent.
