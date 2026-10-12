# task501 design note

Private, never ships. Architecture 3 of the slot, redesigned at stage 2 on 2026-10-12 after the v2 portal result
(both responses landed CHF 250 million by executing the walk-forward the directive filed in full). The first
v3 design kept that walk-forward as a filed execution layer and moved the decisive step to the buffer's
estimand, which the directive also filed ("at any point in a horizon"); under the readability screen both
steps are rule application and the buffer rung is readable, so this redesign replaces the decisive step,
the directive and the asks, and keeps the world (the programme, its managers and funds, the lender and the
facility decision). The replaced design is in git history and in `## Tried and rejected`.

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
| World | Pensionskasse Werdinsel, Zurich, CHF; commitments in USD, EUR and CHF to about 50 funds of 20 managers, vintages 2015 to 2026; Privatbank Lindenhof AG offers the facility. People drawn with `guard.py names --geo Switzerland --seed 501`: Domenica Hürlimann (Treasury & Liquidity), Torsten Sigrist (Portfolio Management), Noémie Hess (Rechnungswesen), Jeremias Ritter (president of the Stiftungsrat), Lazar Marti (the bank). None appears in the prompt |
| As-of | records to 31 December 2026 (the plan date); the extract runs Tuesday 5 January 2027; the lender needs the election by 15 January 2027; the facility year is calendar 2027 |

**Data-native sentence.** A fund may draw its commitment for new investments only until its investment period ends,
and in the programme's record every fund whose period has ended had drawn about 92 per cent of its commitment by
then, including the slow starters the 2020 pause left behind; the four funds committed in late 2022 and late 2023
(Loschwitz III, Juno II, Rosenthal II, Tessin I) did most of their first years in the 2023-24 deal drought, are about
half drawn on 31 December 2026 and reach the end of their investment periods between September and December 2027,
so their 2027 calls are set by the balance they still have to draw before their deadlines, which no age curve
fitted on funds that kept to schedule can see.

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
  back-tests within about 3 per cent on 2025 and 2026 for an honest reason (no fund reached its deadline behind
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
textbook pacing model, done well. Prototype figures (scratch `w501/proto/proto4.py`, seed 501); the build replaces
them with measured ones.

1. Read the notice ledger, keep the issued capital-call lines (investments, management fees, partnership expenses;
   withdrawn notices out), date each by its value date, translate at the plan-date reference rate, and build each
   fund's monthly calls and its unfunded commitment (commitment less calls) at 31 December 2026, every fund in the
   register included.
2. Estimate the programme's monthly call rate on unfunded commitment by fund age, twelve-month bands counted from
   each fund's first call, as the ratio of summed calls to summed unfunded commitment over the record.
3. Schedule 2027 month by month: each fund's band rate times its unfunded commitment, capped at what is undrawn,
   the unfunded commitment reduced after each month.
4. Sum: about CHF 246 million of expected calls in 2027. Check it: 2026's realised calls were higher only because
   more young funds were in their first year, and the same model run from the end of 2024 and of 2025 forecasts the
   next year's calls within 3.3 and 1.5 per cent.
5. Apply the directive: expected calls plus a tenth, less the CHF 150 million reserve, about CHF 120 million, and the
   smallest amount on the lender's menu that covers it.

**Ends on:** CHF 125 million (about CHF 246 million of expected calls, a requirement of about CHF 120 million).

**Golden:** CHF 225 million (about CHF 323 million of expected calls, a requirement of about CHF 205 million in the
prototype; the build places the requirement mid-bin between 200 and 225).

The other natural routes also land short: the age bands split by whether the fund is still in its investment
period (R1b) 120 and CHF 125 million; rates by months to the investment-period end (R2) 141 to 154 and CHF 150 or 175
million; the strategy-by-age table 138 and CHF 150 million. The programme's 2026 calls carried forward (R0) land
high, 238 and CHF 250 million, because 2026 carried more first-year funds than 2027 will.

## Stump sentence

A competent solver forecasts 2027 calls fund by fund with the programme's age-band call rates on unfunded
commitment, files about CHF 246 million of expected calls and elects CHF 125 million; the step that lands it there
is giving Loschwitz III, Juno II, Rosenthal II and Tessin I, which deployed slowly through 2023-24 and whose
investment periods end between September and December 2027 with about half their commitments drawn, the call rate
of funds their age, when every fund whose investment period has ended in the record had drawn about 92 per cent of
its commitment by then, so those four call about CHF 150 million in 2027 rather than about CHF 75 million and the
facility is CHF 225 million.

## Three rules

**Domain test:** the deciding quantity is a private-markets commitment-pacing forecast, the capital calls each fund
will make from its undrawn commitment, governed by the investment period its limited partnership agreement allows
for new investments; the field's model (calls as a rate on undrawn commitment by fund age) done right conditions on
how much a fund must still draw before that period closes. With another field's nouns there is no commitment drawn
by a manager, no investment period, no fee on commitment and no follow-on regime, and the task stops reading the same.

**Analyst test:** a strong analyst who reads every term right (calls by value date with fees and expenses, every
commitment in the register, the plan-date rate, the reserve and the tenth, distributions not credited, withdrawn
notices out) and fits the field's standard pacing model, age-band call rates on unfunded commitment, files about CHF
246 million of expected calls and elects CHF 125 million against CHF 225 million, because the model gives the four
funds whose investment periods end in late 2027 the call rate of funds their age instead of the balance they must
draw before their deadlines. The easy way gets it wrong, so the stump is analytical.

**Layer 1:** call and distribution notices withdrawn by the manager and reissued under a new number; notices of
several lines (investments, management fees, partnership expenses; returns of capital, gains, income); December
notices due in January; currency codes in mixed case and descriptions with stray spaces as the clerks keyed them;
from January 2026 the custodian's feed loads distribution advices as single lines beside the clerks' line-by-line
keying of the same notices, which ran in parallel until the end of September; custodian credits arriving a few days
after the payment date the notice states; distributions in specie of listed shares; manager statements received
months after the period end, some still outstanding; audited capital accounts at fund and year-end grain beside the
line-level ledger; quarterly look-through holdings with NACE codes from the managers' reports; a reference-rate file
without holidays; German and English labels across the systems. Each is what these systems produce, and none decides
the call.

**Layer 2:** the tempting shortcut is the textbook pacing model, a pooled call rate on unfunded commitment by fund
age, which back-tests well on 2025 and 2026. An expert refuses it for the funds whose investment periods end inside
the forecast year, because a fund may draw for new investments only until that date and the record shows every
fund draws to about 92 per cent of commitment by it, however far behind it was; the pooled age rate averages them
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
| (decisive) R3 the funds whose investment periods end in 2027 draw the balance to the closed funds' drawn share by their deadlines | no: the register states each fund's investment-period end and the agreements' standard limit on calls after it; no sentence names a target share, a balance, a catch-up or the pace of slow funds | no: no column, code or flag marks a fund as behind schedule or carries a drawn share at a deadline; the drawn share is a construction from the ledger and the register | no: it is not pooling, stratifying on a visible attribute, trending, reweighting, shrinking or building an analog on visible attributes; the reflexes with the deadline (R1b, R2) land short | no: the age-band model back-tests within about 3 per cent on 2025 and 2026, and no control total, statement or published figure carries a forecast | no: every join resolves, no duplicate or fan-out points at the four funds | no: the balance is a commitment times a share no file reports, applied only to funds selected by a deadline inside the window | silent |
| Over-correction: every undrawn franc of the four funds called by the deadline | no | no | no | no | no | fires: the unfunded commitment as reported | readable |

The decisive rung's quantity is named by no sentence and no column, it is not a reflex, no control sees it, the
battery comes back clean on the wrong path and it is not linear in a reported figure. Both shapes the record says
hold are present: a quantity the solver believes needs no construction beyond the textbook model (the forward calls
of four ordinary funds), and the maturity attack's form (the four funds' drawdown happens after the extract, the
closed years tie under the default because no fund met its deadline behind schedule in them, and the evidence sits in
the closed funds' paths the default never examines).

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. Section numbers are those of the
directive (`richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx`, text in `## Build record`). Calls under the
alternative are prototype estimates; `checks.py` computes and asserts each row.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | facility amount | one of the lender's amounts, CHF 50 to 400 million in steps of 25 million | any amount equal to the requirement | about CHF 205 million, not an amount the lender offers | term sheet ("one of CHF 50, 75, ... 400 million") and s.4 ("the smallest amount offered by the lender") |
| SF2 | for 2027 | the facility year, 1 January to 31 December 2027 | the twelve months from the election date | same call (the January 2027 calls are inside both; asserted) | s.2 ("Facility year: the calendar year for which the facility is elected") |
| SF3 | expected capital calls | the expected (mean) total of the year's calls | a prudent or stressed figure | about CHF 250 to 275 million with an added cushion | s.4 (the margin is the stated prudence: "the expected capital calls ... plus one tenth of them") |
| SF4 | capital calls | every amount a manager calls against the commitment: investments, management fees and partnership expenses | investments only | about CHF 200 million (fees about CHF 30 million) | s.2 ("Capital call: ... for investments, management fees or partnership expenses") |
| SF5 | calls of the facility year | calls with a value date in 2027, a notice issued in 2026 and due in 2027 included | calls noticed in 2027 | same call (the December notices due in January are about CHF 9 million; asserted outside the bin edge either way) | s.5.1 ("a call is in the facility year when its value date is, whenever it was noticed") |
| SF6 | which commitments | every commitment in the register at the plan date | active funds only, or commitments to be signed in 2027 too | same call for the first (every registered fund has called by the plan date; asserted); the second has no filed size and is excluded | s.5.1 ("every commitment in the programme register at the plan date. Commitments signed after the plan date are funded from the commitment budget and are not in the plan") |
| SF7 | currency | every amount at the reference rate of the plan date | each month's rate or a forward | not computable from the pack for the forward months; the 2027 rates do not exist | s.4 ("translated at the reference rate of the plan date") |
| SF8 | the reserve | CHF 150 million deducted | no reserve deducted | CHF 375 million | s.3 and s.4 |
| SF9 | the margin | one tenth of the expected calls | one tenth of the facility amount, or none | CHF 200 million (none) | s.4 ("plus one tenth of them") |
| SF10 | distributions | not credited against calls | expected distributions netted | about CHF 100 million lower | s.4 ("Distributions are paid to the general portfolio and are not credited against calls") |
| SF11 | withdrawn notices | no cash effect; the reissue carries the call | counted twice | about plus CHF 2 million in history, same call (asserted) | field notes ("A withdrawn notice has no cash effect; the manager reissues it under a new number") |
| SF12 | the plan date and the extract | 31 December 2026, the extract's close | the extract's run date, 5 January 2027 | same call (no notice dated after 31 December 2026 is in the extract; asserted) | s.2 ("Plan date: 31 December of the year before the facility year") and the manifest |
| SF13 | unfunded commitment | commitment less calls with a value date to that day | less calls noticed to that day | same call (asserted) | s.2 ("Unfunded commitment: the commitment less the capital calls with a value date on or before that day") |
| SF14 | rounding path | the requirement unrounded, the amount the menu's | rounding the expected calls to the million first | same call (the golden requirement at least 7 million inside its bin; asserted) | s.4 and the term sheet |
| SF15 | a fund's investment period | the dates in the register | the period counted from the final close or extended by a year | same call for the final close (every fund's register date is from its first close as its agreement states; asserted for the four, whose final closes are inside 2022 or 2023) and no extension is recorded | the register (sheet Fonds, investment_period_end, and sheet Hinweise: "as stated in the limited partnership agreement; no extension has been requested") |

The stump is none of these readings: the default and the golden read every term the same way and differ only in
how four funds' 2027 calls are forecast.

## Ladder

Requirement = expected 2027 calls plus one tenth, less the CHF 150 million reserve; the facility is the smallest menu
amount at or above it. Prototype (seed 501); the build measures and asserts every row, places the golden's
requirement mid-bin and keeps every wrong rung at least 7 million from the golden bin's edges.

| Rung | Construction | Expected calls | Requirement | Amount | Killed by |
|---|---|---|---|---|---|
| R0 | the programme's 2026 calls carried forward | 352.8 | 238.1 | 250 | 2026 carried first-year calls of the 2025-26 vintages that 2027 will not repeat, and it ignores the four funds' deadlines |
| R1 (default) | age-band call rates on unfunded commitment, pooled, 12-month bands from the first call | 245.5 | 120.1 | 125 | the four funds behind schedule draw their balance before deadlines inside 2027 |
| R1s | the same by strategy and age band | 261.6 | 137.8 | 150 | as R1 |
| R1b | age bands split by in or after the investment period | 245.7 | 120.3 | 125 | as R1; the split lowers the four funds' last months further |
| R2 | rates by months to the investment-period end, 6- or 12-month bands | 264.6 to 276.6 | 141.1 to 154.3 | 150 to 175 | the deadline band's rate pools funds that kept to schedule (small balances) with the few that did not |
| R3 (golden) | the funds whose investment periods end in 2027 draw the balance to the closed funds' mean drawn share by their deadlines, then the post-period rate; every other fund on R1 | 323.0 | 205.3 | 225 | |
| X1 | every undrawn franc of the four funds called by the deadline | 378.7 | 266.5 | 275 | every closed fund kept 6 to 11 per cent of commitment undrawn at its deadline (follow-on and fee reserves) |
| X2 | the deadline balance spread evenly to every fund's own deadline | 271.1 | 148.2 | 150 | funds with deadlines after 2027 deploy front-loaded in the record, not evenly |
| X3 | the target taken as the lowest closed share | 306.0 | 186.6 | 200 | the estimand is the expected call; the lowest share is a bound |

**Arithmetic.** Position: the default is four amounts below the golden; R2, the nearest reflex, one to two amounts
below; X1 two above. Every correction a solver adds to R1 (strategy, the in-period split, months to deadline) walks
the requirement up by less than one and a half amounts and none reaches the golden; only the deadline balance on the
four funds moves it to the golden's bin (the decisive move is the largest move on the ladder, 85 million against 17
to 34 for the reflexes). The golden is bracketed: every under-construction lands below, every over-construction
above. Dominance: the four funds' balance to the drawn share (about CHF 152 million) against what the default gives
them (about CHF 75 million) is a 2.0x edge; the strategy split's carried advantage on the other funds is 16 million.

**The golden family** (prototype, all inside CHF 200 to 225 million): age bands of 6 or 12 months; pooled or by
strategy; age from the first call or the first close; estimation windows from 2015, 2019 or 2021; the target share
as the mean, the median or the strategy's mean of the closed funds; the post-period rate on commitment or on what
is undrawn. Spread 200.8 to 215.0 in the prototype, too wide for a centred bin; the build closes it by pricing the
four funds' few post-period months with the same age-band rate as every fund (the prototype's separate post-period
rate is the widest member), and asserts every member at least 3 million inside the bin.

## Closure table

| # | Axis | Reading | Closed by |
|---|---|---|---|
| 1 | Population | every commitment in the register at 31 December 2026, each fund with calls by then; commitments signed later are out | s.5.1 filed; every registered fund called by the plan date (asserted, C1) |
| 2 | Unit of account | the fund commitment, in fund currency, translated at the plan-date rate | s.2, s.4 filed |
| 3 | Attribution window | a call belongs to the year of its value date | s.5.1 filed; the December notices due in January asserted on both sides of the bin (C1) |
| 4 | As-of dating | the ledger as it stood at the 31 December 2026 close | s.2 filed; no notice dated after it in the extract (asserted) |
| 5 | Version basis | issued notices; a withdrawn notice replaced by its reissue | field notes; C1 (asserted) |
| 6 | Denominator | the call rate's base is the unfunded commitment; the drawn share's base is the commitment | s.2 definitions of both quantities; the method's bases are the field's own, and the golden family includes commitment-based post-period rates (C3) |
| 7 | Weighting | ratio of summed calls to summed exposure in a band | C3: unweighted means of fund rates inside the golden family's bin (asserted) |
| 8 | Window length | the whole record from 2015, 2019 or 2021 | C3 across the three windows (asserted) |
| 9 | Boundary inclusivity | the investment-period end month is inside the period | C1: no call is noticed before and due after an investment-period end (asserted) |
| 10 | Rounding path | figures unrounded to the requirement; amounts from the menu; fees exact | s.4 and the term sheet; the golden requirement mid-bin (asserted) |
| 11 | Tie-break | not used: the requirement never equals a menu amount | asserted at least 3 million from every edge |
| 12 | Maturity and censoring | the closed funds are those whose investment periods ended by 31 December 2026 | C1: no fund's investment period ends in December 2026, so the set is the same at either edge (asserted) |
| 13 | Order of operations | each fund's month capped at its unfunded commitment, then reduced | C3 (the cap never binds in the golden; asserted) |
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
the register, plan-date rate) plus a tenth; every term has one reading under its SF row, and the readings that
differ (SF1, SF3, SF4, SF7 to SF10) each violate a quoted sentence. The text files the estimand, not a method, so
a literal reader must forecast; the default's forecast and the golden's are the same estimand on the same
population, and they differ by method alone. The method is forced by the data's structure: every fund in the record
whose investment period has ended drew to between about 89 and 94 per cent of commitment by its end, slow starters
included, so a forecast that leaves the four funds about half drawn at their deadlines contradicts every closed case,
while every member of the golden family, whatever its pacing details for the other funds, lands in the same amount
(asserted). The write-up's steps pass the same test.

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
| Primary device | P1, D1 (the same records under two key schemes and grains): from 1 January 2026 the custodian's CF-PM feed loads the distribution advices of the eight managers on its portal into the ledger, one line per advice (the cash amount under the custodian's category, its own reference as the notice number, the custodian's credit value date), while Rechnungswesen kept keying those managers' PDF notices line by line (return of capital, gain, income; the manager's notice number; the payment date the notice states) until the parallel run ended on 30 September. Every one of those notices from January to September is in the ledger twice, both issued, in all four strategies. Silent under the battery: no duplicate rows (different identifiers, line counts, descriptions and entry times), keys unique, every join resolves. Visible only at a cross-file cut nothing invites: the custodian statement shows one credit per notice |
| Hazards | h1 (D8, clock): the notice states a payment date and the custodian credits the cash one to four business days later for about one distribution in six (cross-border, USD and EUR); at the four 2026 quarter ends and at both year ends some cross into the next quarter or year, in every strategy, and every late credit is translated at a different day's rate. h2 (D5): one distribution in specie of listed shares (Growth, third quarter) is not cash. h3 (D2): one Private credit distribution notice withdrawn and reissued in the second quarter. h4 (D3): the custodian statement carries francs at its dealing rates, not the reference rate |
| Stops (each a complete pipeline; targets asserted) | s1 the cracker's path: ledger distribution rows, issued, cash only, by the ledger's value date and that day's reference rate: every one of the 20 figures off, each by at least CHF 1,000 thousand in Q1 to Q3 and at least CHF 20 thousand in Q4. s2 ledger rows deduplicated at notice level on fund, total and stated date (the over-cleaner's first move), keeping the clerk's row: the Q1 to Q4 boundary cells off. s3 deduplicated keeping the feed's row: the boundary cells of non-feed managers off. s4 the custodian statement's credits summed in francs (the dealing rates): every figure off by at least CHF 2 thousand. s5 lazy (in specie and the withdrawn notice kept): every figure off |
| Golden | each distribution notice once, matched to its custodian credit, cash lines only, in the quarter of the credit's value date, its fund-currency amount translated at the reference rate of that date, grouped by the register's strategy |
| Chart | labels are the four quarter totals of the golden; the title names the strategy with the largest year total. The builder places the golden's top two strategies so that s1 names the other one in the title |
| Span (6 files, 13 columns, causal) | ledger (fund, notice id, type, status, line type, value date, amount, currency); custodian statement (value date, amount CHF, reference text); register (strategy); reference rates (date, USDCHF, EURCHF); field notes (status and line-type semantics); export manifest (the statement's coverage). Short of the eight-file floor: the quantity's whole causal path runs through these six systems, and adding a seventh would mean a file built to carry the ask |
| Necessity matrix (target) | one file misread, the rest right: ledger value date taken as arrival, every Q1 and Q4 cell; custodian statement unread, every Q1 to Q3 cell; register strategy unread, n/a (no other strategy source); reference rates unread (dealing rates), every cell; field notes unread (in specie kept), the Growth Q3 and year cells |
| Realism | A custodian feed run in parallel with manual keying for the first three quarters of its life, nobody reconciling the two until the year-end close, is what a migration produces; cross-border credits arriving days after a notice's stated payment date are routine for USD and EUR distributions |
| Referee | the custodian statement: one credit per paid notice, the arrival date, francs at dealing rates; it hands over no graded level |

**Hazard table.** h1 moves every Q1 and Q4 cell (each strategy has at least one late credit across 31 December 2025
or 31 March 2026, and across 30 September or 31 December 2026; asserted) and the Q2 and Q3 cells it crosses; h2 the
Growth Q3 and year cells on the lazy path; h3 the Private credit Q2 and year cells on the lazy path; h4 every cell on
the custodian-only path. Composed mishandlings: every subset of {P1, h1, h2, h3, h4} computed; none keeps more than
2 of the 20 figures, and none that includes P1 or h1 keeps any.

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
14.0; the pair is 29.5, and 32.3 if each keeps a twentieth of the ask weight).

**What the pass rests on.** The parallel run. A top response that matches every ledger distribution to its custodian
credit, counts each notice once, dates it by the credit and translates at the credit day's reference rate lands all
20 figures; if that response also lands the call, the pair still clears the bar (about 47 and 14). The ask holds
only while no top response reconciles the ledger's distributions to the custodian statement notice by notice.

## Prompt

`prompt.txt`, one paragraph, question first, two files named, rounding once at the close; `voice-check.py --task
task501` PASS at 851 characters on the draft. It names no person, title, meeting or reader, no input file, no
method and no trap word. The forcing fact is the 31 December 2026 extract. The ask is worded so that "none" is
never needed (every strategy received distributions in every quarter of 2026, a fact the requester knows).

## Build record

The generator is rebuilt for this design (the first v3 generator is replaced in the same commit as the pack):

- `world.py`: managers, funds, investment periods, fee terms, the reference-rate path, people, dates.
- `sim.py`: monthly calls per fund from the first call, a pacing hazard on the remaining investable commitment with a
  market factor (2020 pause, 2021 boom, 2023-24 drought), the deadline drawdown in each fund's last six months, the
  post-period follow-ons and fees; distributions, NAV, holdings; the 2026 custodian credits with arrival lags.
- `pack.py`, `docs.py`: the files and documents; `golden.py`: the two deliverables; `checks.py`; `verify.py`
  (reads only `target/`); `figures.json`.

As built: to be filled at stage 3 with the measured ladder, the family and every gate.

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
