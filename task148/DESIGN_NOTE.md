# task148: Fenmore Savings Bank's 30 September 2026 allowance on the relief-era SBA pool (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC19. The seed (a bank's year-end loss reserve on the
unguaranteed portions of its FY2019 to FY2021 SBA 7(a) loans, when a payment holiday paused some loans' clocks) was
read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism, a repayment clock that
stopped during a payment holiday, is not kept: it re-aligns the loan-age axis, which is close kin to task133's delayed
entry (loans taken over at a go-live counted only from that date). The pitfall is re-found from how a multi-unit
operator's loans come to default: each business has its own 7(a) loan to its own company, the operator personally
guarantees every one of them, the bank's loan authorization cross-defaults them, and when any one business fails the
bank accelerates every loan the operator stands behind. The records hold one row per loan; the default happens to the
operator.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task148.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (three_rules.strategy_risk, answered below), no BLOCK; the older same-driver signature (population, G2, forecasting) against task142 differentiated on the card; nearest drivers 0.09 (task127 v3 lineage) and under |
| Domain / task type | `banking-credit-financial-risk` (client domain), task type `expected-credit-loss-provisioning` (serves Forecasting): the call is a CECL allowance, the expected lifetime charge-offs of a pool's unguaranteed principal, built the ECL way from default and payoff hazards by months on book conditioned on each loan's survival to the reserve date. The seed's own label (Economics) is not a client domain for lending (`guide-to-prompt/references/domains/README.md`: Economics is never lending) |
| Objective | Forecasting & Predictive Modeling: the charge-offs the pool will take over the loans' remaining lives, a window open at the decision (the fiscal year-end close of 30 September 2026, booked in October) |
| Shape | `single-figure`: one committed allowance, its components by approval fiscal year, a chart and the ask tables supplying the criteria (counted at stage 2 in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `currency` (the allowance to book, to the nearest million dollars on paper; set at stage 3 against the built pack) |
| Mechanism | gap population (decisive: the unit that defaults is the guarantor's cross-defaulted group of businesses, not the loan) and time (the groups' newest businesses, financed in 2025 and 2026, are only now entering the years when businesses fail most); pattern none; generators G2 (what one defaulting unit is), G14 (the pooled loan rate does not fit a pool whose groups differ from the history's), G13 (the window the newest members' peak falls in); Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `estimand_identification` (the right unit of the event: a loan's default is its guarantor group's default); `own:guarantor-group-default-unit` (nearest library lines: event-history 3, repeated spells need their own risk sets, and survival 1, competing exits are not censoring; neither carries a unit of default that spans several records) |
| Furniture | forum `board_of_directors` (the board approves the year-end allowance), forcing event `period_close` (the 30 September 2026 fiscal year-end), organisation family `financial_institution`, role family `finance_controller` (the controller books it), context artifact `register` (the servicing system's loan and guarantor records), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the servicing systems' monthly loan history, one row per 7(a) loan per month-end: the current system from October 2017 (1,627,120 rows, parquet) and the legacy core to October 2017 (499,113 rows, parquet), constructed |
| Deliverables | `sba_allowance_fy2026.xlsx` (the allowance and its components, the ask tables), `allowance_note_fy2026.docx` (the board's one-page note with a chart) |
| People | drawn with `guard.py names --geo "United States" --seed 148`: Erin Spence (controller, books the allowance), Richard Fields (chief credit officer, SBA Lending, owns the allowance policy), Johnny Nicholson (SBA servicing manager, the servicing extracts), Donna Graves (special assets, workouts and charge-offs), Tara Williams (loan operations, SBA reporting); none appears in the prompt |

**Guard.** `guard.py check` at the draw: WARN `three_rules.strategy_risk` (grain_or_unit), no BLOCK. Answered: the
analyst test below runs the easy route with every field read and every filed sentence executed, the guarantee
register included, and it still files the wrong allowance, because reading who guarantees which loan is not the step;
the step is pricing each loan at the hazard of the group it fails with. The first check blocked on
`test.same_driver_older` against task142 (gap population, G2, Gate G forecasting): task142 builds an upper percentile of
a period's total from arrivals and durations; the card carries that differentiation line, and the ones against task133,
task143 and task132. `guard.py heart` at stage 3: WARN, no BLOCK; the nearest text is task133's v2 stump at 0.22, and the
words they share are the textbook route both default paths take (monthly default and payoff rates by months on book from
the loan history); task133's step is delayed entry on an earlier platform's loans, this build's is the guarantor group's
union over businesses at their own ages, and the card's differentiation line against task133 says so. `guard.py surface`
at stage 3: exit 0, no file, schema, wording or name promoted; two pairs promoted on the cards' mechanism axes for the
author's adjudication: task146 (two apart, the same decisive gap and decision type; its step weighs a pool released at a
calendar turn by when each refusal fell, differentiated on the card) and task142 (the older same-driver signature,
differentiated at the draw). Personas found in the cut pack: Erin Spence and Richard Fields, both on the card.

**Same-puzzle and same-driver tests.** Gap population, decisive G2, decision `quantity_figure`, Gate G `forecasting`:
no build in the last twelve carries that triple (task228 is population and G2 but a monitoring hold; task143's decisive
is G17; task146's G14). The older same-driver match is task142, differentiated.

**Abstraction test.** Stripped of nouns, the driver is: a unit's failure takes down every other unit its backer carries,
so the hazard each unit faces is the sum of the hazards of all the units behind the same backer, each at its own age,
including units outside the population being priced and units added recently at the steepest part of the curve; a rate
built on each unit alone at its own age, pooled over the history or taken from the latest period, prices every unit as
if it stood alone. Read by mechanism rather than score, the nearest drivers are: task132 (a failed item renewed at age
zero in the same position: here nothing failed is replaced, the backer adds units by choice, and the first member's
failure ends the group); task143 (the weakest of a few members of a new group against a threshold, with a group effect in
the predictor's error: here members fail independently and the group's failure is their union, so the hazard adds over
members); task133 (delayed entry: here every loan is watched from its first payment and its own age axis is right);
task77, task60 and task103 (a person behind several records, collapsed for a count: here the person is the unit an event
happens to, and the records' ages, not their number, carry the hazard). None shares the latent structure.

**Data-native sentence.** Fenmore's SBA Lending finances owner-operators who run several franchise units or acquired
businesses, each business on its own 7(a) loan to its own company, every loan personally guaranteed by the operator and
cross-defaulted under the bank's loan authorization, so the servicing system holds one row per loan while a default
happens to the operator; the operators kept adding businesses after FY2021, most of all as rates came down in 2025 and
2026, so the relief-era pool's loans now sit in groups whose newest businesses, outside the pool, are just entering the
years when a new business fails most.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (59 builds): conditional survival and
delayed entry (133), conversion hazards with competing deaths (134), replacement renewal (132), selective labels (141),
a correlated group effect (143), a pool released at calendar turns (146) and the rest of the lane's drivers; none makes a
unit's event the union of several records' events behind one backer. `layer2-rigor-patterns.md`: event-history 3
(repeated spells, risk sets by person) and survival 1 (competing exits) are the nearest lines; both are already the
default path's reflexes here. `two-layer-task-design.md`: "the right comparison group" and "the data's real structure"
are the client's families for the step. task133's card, design note and `## Tried and rejected` (the lane's loan-book
allowance): its delayed entry, survival conditioning and competing repayment are all ground this build stands on, never
its step. The seed's header and Situation (FC19) for the world, decision and quantity only.

**World.** Fenmore Savings Bank (holding company Fenmore Financial Corporation) is a savings bank whose fiscal year ends
on 30 September. Its SBA Lending division opened in October 2009 and makes 7(a) loans across the country under the
Preferred Lenders Program; it sells the guaranteed portions on the secondary market, keeps the unguaranteed portions and
services every loan. Most borrowers are single businesses; a large share are companies owned by operators who run
several franchise units or have bought several small businesses, each financed with its own 7(a) loan. The bank's SBA
loan authorization makes every loan to an operator's companies guaranteed by the same individuals cross-defaulted and
cross-collateralized, and the bank's practice is to accelerate every such loan when any one of them goes into default.
The allowance policy pools the loans approved in fiscal years 2019 to 2021 separately (the relief-era pool: Section 1112
payments, the Economic Aid Act's 90 per cent guaranty and waived fees) and books its allowance at each 30 September. The
controller books the allowance at 30 September 2026; the board approves it in October.

## Default path

1. Read the allowance policy: the allowance is the unguaranteed principal the bank expects to charge off over each
   loan's remaining contractual term, adjusted for expected prepayments, on the relief-era loans on the books at
   30 September 2026, at the note rate in effect that day; a loan is in default at the first month-end it is 90 or more
   days past due or accelerated.
2. Read the two servicing extracts into loan-months from each loan's disbursement, the legacy layout's codes and cents
   mapped to the current system's, and the loan master for each loan's approval date, term and guaranty share.
3. Estimate monthly default and payoff hazards by months on book (and term) over every loan since October 2009, each loan
   at risk until its own default, payoff or maturity.
4. Roll each performing pool loan forward from its months on book at 30 September 2026, conditioned on its survival to
   date, the default hazard against payoff and maturity; multiply each month's default probability by the loan's
   unguaranteed principal scheduled for that month-end at the reserve-date rate, times the share of resolved defaults
   the record shows ending in a charge-off; loans already in default at that share of their unguaranteed principal.

Ends on: about $4 million (3.89 on the built pack, 61 per cent under the golden; by term 3.84).
Golden: about $10 million (9.94 on the built pack; split 2.0, 3.0 and 5.0 by approval fiscal year, from 1.99, 3.00 and
4.95).

## Stump sentence

Building monthly default and payoff rates by months on book from every loan since October 2009 and rolling each
performing relief-era loan forward on its own months on book books about $4 million (Ends on) at 30 September 2026; the
step that lands it there is pricing each loan as if it stood alone, when a loan whose operator guarantees other
businesses under the bank's cross-default fails whenever any of them fails, so its hazard is the union of the group's
businesses' hazards at their own ages, and most of those businesses, financed outside the pool in fiscal 2026, are only
now entering the years when a business fails most; the allowance is about $10 million.

## Three rules

Written at the draw; the figures are the built pack's (stage 3).

- **Task type:** banking-credit-financial-risk, expected-credit-loss-provisioning (serves Forecasting): the relief-era
  pool's CECL allowance, the expected charge-offs of its unguaranteed principal over the loans' remaining lives, built
  from default and payoff hazards by months on book conditioned on survival to the reserve date.
- **Domain test:** the deciding quantity is each loan's lifetime probability of charge-off under personal guarantees and
  cross-default: the unit that defaults is the operator's group of businesses, so a loan's default hazard is the sum of
  the default hazards of every business its guarantors stand behind, each at its own months on book, and the loan is
  charged off when the group defaults while the loan is still on the books.
- **Swap:** "how many hospital patients will be readmitted" keeps records, ages and a hazard, but a personal guarantee
  that ties several companies' loans to one person, a loan authorization that cross-defaults them and a bank that
  accelerates them together have no counterpart, so what sets each record's hazard, and with it the call, stops making
  sense.
- **Layer 1:** the servicing history in two layouts (the legacy core's codes, cents and loan numbers to October 2017, the
  current system's from its parallel run in October 2017, the month in both); the guarantee register's names written
  differently across an operator's loans (middle initials, suffixes, capitals) beside the documentation system's party
  number and the last four digits of the guarantor's tax number, and different people sharing a name; SBA loan numbers in SBA's files against the bank's note
  numbers in its own; the Form 1502 report in SBA's layout; fiscal years ending 30 September against calendar dates;
  transient delinquencies that cure. Each is what these systems write; none carries the stump (asserted at stage 3).
- **Layer 2:** `estimand_identification`: the unit of the event is the guarantor's group, so the hazard each loan faces
  is the union of the group's businesses' hazards at their own ages; the shortcut prices each loan on its own months on
  book from rates pooled over loans (or taken from the latest year), which already average the history's cross-defaults
  at the history's group mix and its members' ages, and the pool's groups are larger and younger than that.
- **Decisive step:** each relief-era loan priced at the default hazard of its guarantor group: the sum, month by month,
  of the business default hazards of every active loan its guarantors stand behind (estimated on the businesses that
  start a group's default, or on single-business guarantors), each at its own months on book and with its own payoff and
  maturity, the businesses financed in FY2022 to FY2026 outside the pool included.
- **Not semantics:** the guarantee register, the loan authorization's cross-default clause and the servicing statuses
  are read correctly by the easy route too; no field, code, unit or definition says what a loan's hazard is or that it
  depends on its group's other businesses' ages; the default path reads every one of them and still files about $4
  million.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the prompt's question, the
  allowance policy's estimand, default, charge-off and rate sentences, the loan authorization's cross-default clause) are
  executed word for word on the clean truth at stage 3 and give no figure of their own: they say what is counted and
  when a loan is in default, never a hazard, a group's hazard or how a loan's default probability is built; the
  estimators they admit (loan-level rates pooled, recent or by covariate) file about $4 million.
- **Analyst test:** a strong analyst who stages the pool cleanly, maps the legacy layout, reads the policy, the register
  and the loan authorization correctly and builds the textbook lifetime PD from monthly default and payoff rates by months
  on book and term over every loan since October 2009 books about $4 million (Ends on), because a loan whose operator
  carries other businesses fails when any of them fails and its own months on book say little about that; the last
  year's rates file about $4.6 million, the group's size as a covariate or a count of the group's loans at a per-loan
  rate $5.2 to $7.4 million, and the group priced with the per-loan rates $11.9 to $13.0 million (built pack).
- **Estimand:** the allowance policy (`allowance_policy_sba_7a.pdf`, 1.2, 2.1, 3.1 and 5.1): the unguaranteed principal
  the bank expects to charge off, over each loan's remaining contractual term adjusted for expected prepayments, on every
  relief-era loan (7(a) loans approved by SBA from 1 October 2018 to 30 September 2021) on the books at 30 September
  2026, loans in default not yet charged off included, expected recoveries not included, each loan's exposure at its
  note rate in effect that day, loans made after the date not projected; the population, outcome, window and unit are
  filed, the estimator is not.
- **No decoy:** no memo, prior-year allowance, model output, stakeholder figure or certified table states or argues a
  figure or a method; the loan authorization is the bank's standard template, read for its clauses, and argues nothing.
- **No certified replay:** no certified or published allowance ships and nothing graded is reproduced; the business
  hazards are estimated from the raw servicing history.
- **Lesson:** a loan's default is its guarantors' default: when one operator stands behind several businesses under
  cross-default, each loan fails when any of them fails, so its hazard is built on the group (every business the
  guarantors back, at its own age, inside the pool or not), and a loan rate pooled or recent, which averages the
  history's cross-defaults at the history's mix, misprices a pool whose groups are larger and younger; no build on file
  teaches a unit of default that spans several records behind one backer.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Values are the built pack's ($ million).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the default path: loan-level default and payoff rates by months on book (and term) since October 2009, each loan on its own age (3.89) | no | no | yes | no | no | no | readable |
| R1 the obvious corrections: covariates (size, industry, term) or the latest 12, 24 or 36 months' rates (3.84 to 4.56) | no | no | yes | no | no | no | readable |
| R2 the group's size: a multi-unit flag or the group's loan count as a covariate, or a per-loan rate times the count (5.18 to 7.41) | yes (the cross-default clause sends the solver to the register) | yes (the party number, one join) | yes | no | no | yes | readable |
| R3 the group's union over the pool's own loans (4.45 to 4.85) | yes | yes | no | no | no | no | readable |
| R4 the group's union at the per-loan rates (11.86 to 12.98; the rates already hold the history's cross-defaults) | yes | yes | yes | no | no | no | readable |
| R5 (decisive) each loan at its group's default: the union, month by month, of the failure hazards of every performing loan its guarantors stand behind, each at its own months on book with its own payoff and maturity, the fiscal 2026 units outside the pool included, the failure hazard measured on loans standing alone (9.94) | no (the clause says a default under any of those loans is a default under this one; nothing says what a loan's hazard is, that the other loans' ages carry it, or which rate is a business's) | no (no column holds a group, a group's hazard, a member's age or the business that failed: a fast failure accelerates every loan of the group the same month under 90 days past due) | no (the reflexes are pooling, stratifying on size, the latest rates, a count) | no (no allowance, model output or corpus ships) | no (the battery is clean on it) | no (a per-group survival product over each member's own hazard curve) | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "allowance for credit losses" | the lifetime expected charge-offs on the pool at the reserve date | twelve months or incurred losses; the year's provision | lower; a change, not a balance | policy 2.1 ("over each loan's remaining contractual term"); the prompt's "as the allowance" |
| SF2 | "unguaranteed portions" | (1 minus the guaranty share) of each loan's principal | the whole loan; the guaranteed portion | four to ten times higher | the prompt; policy 1.1 |
| SF3 | "approved in fiscal years 2019 to 2021" | SBA approval date 1 October 2018 to 30 September 2021 (the master's approval date) | note date, disbursement date, calendar years | another set of loans | policy 1.2 (approved by SBA, 1 October 2018 to 30 September 2021) |
| SF4 | "at 30 September 2026" | the loans on the books at the September 2026 month-end | loans closed in September included | fewer or more loans | policy 2.1 ("on the books at that date"); the servicing month-end rows |
| SF5 | loans in default | included at the charge-off share of their unguaranteed principal | excluded; at their whole unguaranteed principal | lower or higher | policy 2.1 and 2.3 |
| SF6 | recoveries | not netted | expected recoveries netted | lower | policy 2.1 ("Expected recoveries are not included") |
| SF7 | the rate on the schedule | each loan's note rate in effect at 30 September 2026, held | a forward prime path | about 1 per cent | policy 3.1 |
| SF8 | conditions | the bank's own experience from October 2009, no forecast adjustment | a macro overlay | another figure | policy 4.1 |
| SF9 | the loss on a default | the unguaranteed share of the principal scheduled to be outstanding at the month-end of default | the principal before that month's instalment; net of collateral | 10.24 (same call); lower | policy 3.1 and 2.1; the earlier-instalment reading is same call (asserted) |
| SF10 | default | the first month-end at 90 or more days past due or accelerated | the charge-off as the event; 120 days | timing only | policy 2.2 |
| SF11 | remaining life | to contractual maturity, adjusted for expected prepayments | no prepayments; extensions | higher | policy 2.1 (ASC 326-20-30-6's term) |
| SF12 | loans made later | not projected | future add-on units projected | higher | policy 5.1 |
| SF13 | Section 1112 months | no break in the risk sets (the servicing history carries no paid-month flag; a loan SBA paid is current) | the paid months taken out by the agent's instalment months | same call (9.99) | asserted in checks.py (C3) |
| SF14 | "book" | the allowance balance at 30 September 2026 | the fiscal 2026 provision expense | another quantity | the prompt ("book at 30 September 2026 as the allowance") |
| SF15 | rounding | once: the allowance to the nearest $1 million, each part of the split to the nearest $0.5 million | the parts rounded and then summed | same call (the rounded split sums to the rounded allowance, asserted) | the prompt's last sentence |
| SF16 | the same guarantor | the register's party number | the surname with the TIN's last four; the name without initials or suffix with the TIN; the exact name as typed | the same 30,791 groups for the first two | C1 (asserted); the exact typed name is a Layer 1 slip, not a reading of a term |
| SF17 | the cross-default's reach | every loan guaranteed by a guarantor of the loan (authorization 6.1) | the connected chain of guarantors | same call | C1 (asserted: no guarantor bridges two groups) |
| SF18 | the charge-off share | resolved defaults by loans: charged off over charged off, cured and paid in liquidation | by dollars; by groups; open defaults counted as not charged off | same call (9.93 to 9.98); 9.20 | asserted within the bin (C3); the open-defaults reading is ruled out by policy 2.3 (a loan in liquidation is not brought current or paid) |
| SF19 | the split's fiscal year | SBA's fiscal year of approval | the bank's fiscal year | same call | both run 1 October to 30 September (policy 1.2) |
| SF20 | "the unguaranteed principal" on the chart | the unguaranteed share of principal on the books at 30 September 2026, loans in default included | performing loans only | a smaller bar | policy 2.1's population ("loans in default not yet charged off included") |

The stump is none of these rows: every reading above files the same rounded allowance once the decisive step is taken,
and the default path files about $4 million under every one of them.

## Ladder

Built pack, $ million (checks.py prints every value).

| Rung | Construction | Allowance | Dies to |
|---|---|---|---|
| 0 | loan-level rates by months on book since October 2009, each loan on its own age (by term 3.84) | 3.89 | the clause and the register (a loan fails with its group); out of sample (rates to September 2024, fiscal 2025 and 2026 one month ahead, whole book) the per-loan rates expect 724 defaults where loans standing alone had 605, and 164 where loans in groups had 369 |
| 1 | the latest 12, 24 or 36 months' rates; covariates (size and industry) | 3.91 to 4.56 | the same; the latest rates still hold today's members at today's ages |
| 2 | the group's size as a covariate or a multi-unit flag (all history, latest 24 or 60 months), or a per-loan rate times the count of the group's loans | 5.18 to 7.41 | the members' ages: the history's groups were bought as blocks of one age, while the pool's groups gained 1,403 units in fiscal 2026 that have not reached their failing years |
| 3 | the group's union over the pool's own loans | 4.45 to 4.85 | the clause reaches every loan the guarantors stand behind; the register lists the fiscal 2022 to 2026 units |
| 4 (decisive) | the union over every performing member at its own months on book, the failure hazard on loans standing alone | 9.94 (1.99, 3.00, 4.95) | the golden; out of sample it expects 548 and 392 against 605 and 369 |
| over | the union at the per-loan rates (cross-defaults counted twice), all history or the latest 12 to 36 months | 11.86 to 12.98 | the per-loan rates already hold the history's cross-defaults |

Grid, rate basis by unit of pricing ($ million, built pack):

| Rate basis | Each loan alone | Times the count | The pool's union | The full union |
|---|---|---|---|---|
| per-loan rates since October 2009 | 3.89 | 5.97 | 4.85 | 11.86 |
| per-loan rates, latest 12 months | 4.56 | 7.41 | not run | 12.98 |
| per-loan rates, latest 24 months | 4.29 | 6.85 | not run | 12.43 |
| loans standing alone | 3.79 (prototype) | 5.41 | 4.45 | 9.94 (golden) |

Position and margin: the golden is the one cell of the grid inside its bin; the nearest cell below is 7.41, a ratio of
1.34, and the nearest above 11.86, a ratio of 1.19; every cell is at least 1.9 from the golden, more than one $1 million
bin. Dominance: corrections on rungs 1 to 3 move the figure by 3.5 at most; the decisive step moves it by 2.5 to 6.1
from any rung below, and the one family above it is the double count. Worth: the decisive step carries 6.0 of the 9.94.
Every reflex lands outside: pooling, the latest rates, a size covariate, a count, the pool's own union and the double
count.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the relief-era loans (SBA approval 1 October 2018 to 30 September 2021) on the books at 30 September 2026, loans in default not yet charged off included; no loan joins the pool after the date and loans made later are not projected | filed (policy 1.2, 2.1, 5.1); C1 on the master's approval dates (none within a day of either edge undecided) |
| 2 | Unit of account | the loan is the unit of loss and of the split; the unit that defaults is left to the analysis | filed (2.1, 2.2); the default unit is HOW, forced by the clause and the data |
| 3 | Attribution window | each loan's remaining contractual term from October 2026 to its maturity month | filed (2.1); the master's maturity dates |
| 4 | As-of dating | the September 2026 month-end rows | filed (2.1); the servicing extract ends there |
| 5 | Version basis | the servicing month-end rows as recorded; the legacy layout to October 2017, the current system from October 2017 | C1: the parallel-run month is identical in both (asserted) |
| 6 | Denominator | the charge-off share over resolved defaults | C3 over the bases (asserted); open defaults counted as not charged off is ruled out by policy 2.3 (SF18) |
| 7 | Weighting | the charge-off share by loans, dollars or groups | C3: same call (asserted) |
| 8 | Window length | the experience from October 2009 | filed (4.1); shorter windows are rungs the data rejects |
| 9 | Boundary inclusivity | approval dates 1 October 2018 and 30 September 2021 inside | filed (1.2, "1 October 2018 to 30 September 2021"); C1 |
| 10 | Rounding path | once, at the end: the allowance to $1 million, each part of the split to $0.5 million | the prompt; the rounded parts sum to the rounded allowance (asserted) |
| 11 | Tie-break | none: one figure | not applicable, asserted single |
| 12 | Maturity and censoring | loans followed to September 2026; open defaults out of the share | C3 (row 6); every loan observed from disbursement (the division opened October 2009) |
| 13 | Order of operations | hazard, exposure and the charge-off share multiply | C1: they commute; the share applied once (asserted) |
| 14 | Row order | the servicing rows' order | C1: asserted over a shuffled read |
| 15 | Duplicate resolution | the October 2017 month in both layouts | C1: identical rows, either copy (asserted) |
| 16 | Identity normalisation | a guarantor across loans by the register's party number (surname with the TIN gives the same groups); loans across systems through the master's crosswalk | C1 (SF16, asserted); the master carries legacy, note and SBA numbers |
| 17 | Netting against gross | recoveries not netted | filed (2.1) |
| 18 | Dimensional units | legacy amounts in cents, current in dollars | the README's field notes; C4 (a cents misread moves no hazard, the exposure reads the current system) |
| 19 | Code and status semantics | the legacy codes against the current; default at 90 days or accelerated | the README's code lists; filed (2.2); never the stump |
| 20 | Integerisation | none | not applicable |
| 21 | Clause scope | the cross-default reaches every loan guaranteed by a guarantor of the loan, every vintage | filed (authorization 6.1); C1 (SF17, no guarantor bridges two groups) |
| 22 | Forward window contents | the current members' remaining terms at the reserve-date rates; no new loans | filed (3.1, 5.1) |

## Literal reader

Executing the prompt and every filed sentence word for word fixes the population (1.2, 2.1), the outcome (2.1, 2.3), the
window (2.1), the exposure and its rate (3.1), the experience (4.1), the run-off (5.1) and the event (2.2), and each
term has one reading or readings that file the same figure (the fork table); no sentence says how a loan's default
probability is estimated, what a business's failure rate is or which loans' ages carry a loan's risk. Every estimator
the sentences admit is a HOW; the data's structure forces it (accelerations co-timed across loans sharing guarantors,
the clause, one failure curve by a business's own age, the fiscal 2026 units), and out of sample the data separates the
candidates: the per-loan rates expect 0.45 of the defaults loans in groups had (164 against 369) while the union
expects 1.06 of them (392), and 1.20 of the standing-alone loans' defaults against the union's 0.91. The easy answer is
an easy method on the same literal estimand, never another reading; the literal estimator (the bank's loan-level
experience) files 3.89 (asserted).

## Oracles

- The Form 1502 report for September 2026 (a distractor): guaranteed balances and SBA status codes by loan; it carries no
  allowance, no guarantor and no rate, and ties to the servicing history under every basis.
- The special assets ledger, the payments to SBA and the settlement account credits: the asks' files; the call reads
  none of them, and the charge-off share the call takes from the servicing statuses equals the ledger's charge-off count
  under every basis (asserted), so nothing there scores the allowance.
- No allowance, prior-year allowance, model output, peer rate or published loss rate ships: none for the call.

## Ask sheet

**Main call's declared row population:** the two servicing extracts, the loan master, the guarantee register, the
allowance policy, the loan authorization's standard terms and the README. Device and hazard rows in it: 0 (asserted: the
call computed with the FTA files, the settlement account credits, the special assets ledger and the payments to SBA
removed is the golden; the asks computed with the guarantee register and both servicing extracts removed are the asks).
The loan master is shared and carries no device. Neither ask is keyed to the call, its construction or its figures;
they share no primary device and neither reads the guarantee register.

**Ask A. Section 1112 payments on the relief-era loans by fiscal quarter of the instalment** (7 figures, April to June
2020 through October to December 2021, to the nearest $1,000).
- Golden (built): FY2020 Q3 $76,581,000; FY2020 Q4 $88,571,000; FY2021 Q1 $22,362,000; FY2021 Q2 $56,835,000; FY2021
  Q3 $60,582,000; FY2021 Q4 $58,183,000; FY2022 Q1 $24,141,000. Equal to the world's payments in every quarter
  (asserted) and recomputed by the verifier.
- H18 home: an audit trail of the relief that sets the pool apart, the workbook's second table, a measure the call does
  not turn on; in the controller's words ("Section 1112 payments", "instalments due").
- Construction: every remittance line SBA's fiscal transfer agent sent for a pool loan (SBA loan number to the master),
  each instalment once at the amount SBA paid on it, by the fiscal quarter of the instalment's due date; the Economic
  Aid Act layout's cents converted and its hyphens dropped from the SBA loan number.
- Primary device A1 (D6, an event's quantity on every line it covers, grain unstated): the agent's detail export prints a
  disbursement's amount on every instalment line it covers. A catch-up disbursement (a loan whose data reached the agent
  late, a new loan's first payment covering two to four instalments, the first Economic Aid Act payment covering February
  and March 2021) pays each instalment at the first instalment's amount and carries its total on each of its lines, so
  summing the lines counts the total once per instalment. Catch-up lines in every quarter (built: 3,004, 943, 728, 6,359,
  3,617, 1,689 and 1,394, asserted). Nothing in either file marks them: a catch-up line looks like a monthly one. The
  tell is across files: the settlement account's ACH credit for a trace is the sum of its disbursements, each once, and
  an Economic Aid Act line above the $9,000 monthly cap cannot be one instalment.
- Hazards: HA1 the Economic Aid Act layout's amounts in cents and hyphenated SBA loan numbers; HA2 two dates on a line
  (remitted and instalment due); HA3 the agent's files cover the whole 7(a) book, every vintage.
- Stops (built, each a complete pipeline): S1 the cracker, lines summed by the instalment's quarter with every hazard
  handled, 7 of 7 off, nearest $9,939,453; S2 lines summed by the remittance quarter, 7 of 7 off, nearest $7,689,196; S3
  each disbursement kept once at its first instalment's quarter, 7 of 7 off, nearest $185,147; S4 the cents unconverted
  with A1 resolved, 4 of 7 off (the Economic Aid Act quarters). Lazy delta: S1 against the golden, every quarter.
- Span: the CARES Act detail, the Economic Aid Act detail, the settlement account credits, the loan master and the
  README (5 files); remitted, trace, SBA loan number, borrower, instalment due, amount in each layout; settlement date,
  trace, description, amount; approval date, SBA loan number (12 columns).
- Realism: an agent's flat export repeats a disbursement amount on each detail row; catch-ups are how late data and new
  loans' first payments were paid.

**Ask B. Net charge-offs on the relief-era loans by fiscal year and approval fiscal year** (12 figures, fiscal 2023 to
2026 by fiscal 2019, 2020 and 2021 approvals, to the nearest $1,000).
- Golden (built): FY2023 $12,518,000, $19,933,000 and $13,333,000; FY2024 $882,000, $6,821,000 and $11,699,000; FY2025
  $1,487,000, $2,189,000 and $4,133,000; FY2026 $1,161,000, $460,000 and $2,107,000 (FY2019, FY2020 and FY2021
  approvals). Equal to the world's net charge-offs in every cell (asserted) and recomputed by the verifier.
- H18 home: the pool's loss history by vintage, the workbook's third table, the record the allowance is read against; a
  measure the call does not turn on.
- Construction: the unguaranteed principal the special assets ledger charges off on a pool loan (note number to the
  master), by the posting date's fiscal year, less the recoveries the bank kept: its share of each receipt in the ledger
  and the lender's shares of Treasury offset collections SBA remits to the settlement account.
- Primary device B1 (D3, a per-row convention that passes the identity check): Special Assets moved to a new workout
  module on 3 April 2023, and a case keeps the module it was opened in. The old module records a liquidation receipt at
  the bank's share; the new one records the gross receipt. SBA's share of every receipt is paid from the liquidation
  account and appears in the payments to SBA. Reading every receipt as the bank's share overstates the recoveries on
  cases opened from April 2023; netting SBA's payment from every receipt understates those on older cases; switching by
  the posting date gets the older cases' later receipts wrong. Receipts from both modules in every cell (built: 5 to 232
  old-module and 5 to 266 new-module receipts a cell, asserted). Nothing names the module: the convention shows only in
  the ratio of SBA's payment to the receipt it follows (the guaranteed share over the unguaranteed share when the receipt
  is the bank's share, the guaranteed share when it is gross; built: 2,532 receipts on older cases and 1,767 on newer
  ones, every one on its own ratio).
- Second device B2 (D4, absence evidenced in a file no habitual join reaches): Treasury offset collections reach the
  bank as SBA's remittance of the lender's share to the settlement account, never in the special assets ledger; 8 to 154
  a cell (asserted).
- Hazards: HB1 a charge-off posted to the wrong note and reversed within days; HB2 guaranty purchase proceeds on held
  guaranteed portions among the settlement credits (not recoveries); HB3 the ledger keys note numbers, SBA's files SBA
  loan numbers.
- Stops (built, each a complete pipeline): S1 the ledger as kept, 12 of 12 off, nearest $72,551; S2 SBA's payment netted
  from every receipt, Treasury shares added, 12 of 12 off, nearest $218,937; S3 the cracker, B1 resolved and B2 missed,
  12 of 12 off, nearest $8,835; S4 the switch by posting date, Treasury shares added, 12 of 12 off, nearest $315,677.
  Lazy delta: S1 against the golden, every cell.
- Span: the special assets ledger, the payments to SBA, the settlement account credits, the loan master and the README
  (5 files); posted, case, note number, code, amount; paid, SBA loan number, purpose, amount; settlement date,
  description, addenda, amount; note number, approval date, guaranty share (16 columns).
- Realism: a module change switches what a receipt line holds without changing its columns; Treasury offset shares
  arrive as SBA cash, not as a workout receipt.

**Hazard table** (built deltas, $ thousand)

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 cents in the Economic Aid Act layout | the agent's 2021 layout | A | the four 2021 quarters 100 times |
| HA1 hyphenated SBA loan numbers | the agent's 2021 layout | A | 4 of 7 quarters low, by 24,141 to 59,206 |
| HA2 two dates on a line | the remittance follows the instalment | A | 7 of 7 quarters off (S2) |
| HA3 the whole book | one agent for every vintage | A | 5 of 7 quarters high, by 47,859 to 203,251 |
| HB1 a reversed mis-posting | a keying slip | B | 2 cells high by 49 and 43 if the reversal alone is dropped |
| HB2 purchase proceeds as recoveries | one settlement account for every flow | B | 12 of 12 cells low, by 41 to 1,940 |
| HB3 note numbers against SBA loan numbers | the bank's ledger against SBA's files | B | the join through the master; unjoined, every cell is lost |

**Referee:** the settlement account credits settle A1 (each disbursement once in its trace) and carry B2's shares; the
payments to SBA settle B1. Neither hands over a quarter's or a cell's figure.

**Cracker sheet**

| Ask row | Figures | Cracker (landed the call, ran the battery, executed every filed rule) |
|---|---|---|
| Ask A, Section 1112 payments by quarter | 7 | miss |
| Ask B, net charge-offs by fiscal year and vintage | 12 | miss |
| the chart's unguaranteed principal by vintage | 3 | outside |
| the allowance's split on the chart | 3 | outside |

Mirror leakage: 14 per cent of the ask weight (the chart's unguaranteed principal bars and its form; the mirror, off the
call, misses both asks and the allowance bars).

Pair ceiling: 37 (C = 38 + 7 + 55 x 0.17 = 54.4 with the cracker keeping the chart; S = 5 + 7 + 55 x 0.14 = 19.7;
rerun from the generated rubric once the portal returns it).

## Build record

Stage 3, 2026-10-16. `generator/build.py`: the world (`world.py`, every draw keyed by group, unit, month and purpose;
37,586 loans approved from October 2009 and disbursed by 30 September 2026 in 30,791 guarantor groups), the servicing
extracts, master, register, Form 1502 and secondary market files (`records.py`, `cast.py`), the Section 1112, settlement
account, special assets and payments-to-SBA files (`asks.py`), the policy, the loan authorization's terms and the README
(`docs.py`), the goldens and `figures.json` (`deliver.py`), `metadata.json` (`metadata.py`); then `checks.py` (173
assertions, 0 failed: the input gates, the realism sweep, R1 to R3c on the clean truth, the rule 3 sentence audit, SF1 to
SF20, every rival's separation, the back-test, thirteen constructions and one sigma, the asks' goldens, devices, stops
and coverage, the separation line both ways, the distractors' deletion), `verify.py` (its own code path: connected
components on loans and parties, its own union algebra, each receipt's module from its ratio to SBA's share; the call
9.94 and all 26 graded figures agreeing), a second full build compared byte for byte (16 target files, 2 goldens,
metadata.json, figures.json, target.zip identical, target.zip sha256 991dd3ef) and target.zip. Gates: `figures_check.py`
53 of 53; `precut.py` exit 0 (49 checks); `voice-check.py` PASS (846 characters); `scrub_producer_metadata.py` clean on
target and golden (band 1 January 2018 to 9 October 2026; the policy's and the form's own dates in their containers);
`leak.py --asof 2026-10-05` REVIEW (no LEAK, six lines answered below); `guard.py surface` exit 0 and `heart` WARN, both
answered in `## Draw`; `validate` clean.

House fixes in this pass: H3, the critical component's count says whose guarantors stand behind another performing loan
(2,036 relief-era loans; no loan in default has a performing loan beside it); LEAK fixed, an operator's monogram spelt a
toolchain word in one borrower's name (`cast.py` monograms now skip it); the persona scan's two false names (a department
and the form's name read as people) removed by writing both in lower case in the README and the form's heading in
capitals;
H21, the bank's invented name read against real names a letter or two off (Fenimore, Fennimore, Kenmore), none a lender
known to us, kept.

## Leak review

- Sweep 3, `README.txt` carries 11 of the committed call's 12 distinctive words: its title and file notes use the
  policy's own vocabulary (the allowance for credit losses, the SBA 7(a) unguaranteed portions, 30 September 2026, the
  fiscal years); no allowance, rate or model figure ships anywhere (R3c asserted). Harmless.
- Sweep 3, `allowance_policy_sba_7a.pdf` carries 10 of the 12: the policy defines the allowance in the call's words and
  states no figure. Harmless.
- Sweep 4, `README.txt` shares seven stump-paragraph terms (october, history, servicing, guarantor, carries, register):
  its field notes describe the extracts and the guarantee register; none names a hazard, a group's union or a member's
  age (the rule 3 word screen asserts it). Harmless.
- Sweep 4, `allowance_policy_sba_7a.pdf` shares three (default, october, policy): its definitions of default, the
  pool and the experience window. Harmless.
- Sweep 4, `sba_loan_authorization_standard_terms.pdf` shares five (default, october, guarantor, business, guarantors):
  the guaranty and cross-default clauses every route reads (`Not semantics:`); they say when loans default together,
  never how a loan's default probability is built. Harmless.
- Sweep 9, `sba_loan_master.csv` carries 25,854 ISO dates after 5 October 2026: 25,448 maturity dates and 406 first
  payment dates of loans disbursed in September 2026, contractual schedule dates on the forward-looking allow-list
  (H16); no record was made after the export. Harmless.

## Tried and rejected

- The seed's paused repayment clock (a payment holiday stopping the seasoning clock for some loans): not built; it
  re-aligns the loan-age axis, close kin to task133's delayed entry.
- The payment burden of variable-rate loans as the decisive step (each loan's hazard on its scheduled payment against
  the payment it was underwritten on, prime re-amortised at quarterly resets): prototyped on 2026-10-16. With prime held
  at its reserve-date level the textbook pooled rate missed by 6 to 14 per cent and the latest year's rates by 4 to 10,
  because the history already carries the 2023 to 2026 burden at the same months on book and a 10-year loan's payment
  moves little late in life; burden models with and without calendar or vintage effects scattered 3.5 to 4.8 against a
  truth of 4.5; 25-year loans made the textbook land within 1 per cent; a filed rising-rate outlook would have been a
  signpost and a stress test a change of decision.
- The guarantor-group world with large blocks and steady add-ons (prototypes 6 and 7, 2026-10-16): the group's size as a
  covariate and the latest year's rate times the count landed within a bin of the golden, because the history already
  held groups whose loans were the pool loan's age; rebuilt with blocks of one to four units and add-ons only after
  rates fell in fiscal 2026.
- Add-ons by single-unit operators at the same rate as multi-unit operators: the business rate taken from guarantors
  with one loan ever came out 5 per cent above the golden (the operators who survived went on to expand), outside one
  sigma; add-on rates now follow the operator's units in service.
- Section 1112 months flagged in the servicing history: the flag would have referred Ask A's amounts to a main-call file;
  the paid months stay unflagged and a business that failed while SBA paid shows it when the payments stop.
- Failures deferred while SBA paid (a business that failed during its Section 1112 months shown only when the payments
  stopped): taking those months out of the risk sets (SF13) landed at the bin edge; failures during paid months now
  close within the month like any other.
- The module switch by posting date (every receipt posted from 3 April 2023 gross): netting SBA's share from every
  receipt and adding the Treasury offset shares landed 9 of the 12 Ask B cells; the convention now follows the case,
  so every stop misses every cell.
- More single-loan borrowers to steady the standing-alone rate: the double count the union at per-loan rates carries
  fell to 9 per cent, inside a bin of the golden; singles and operators now scale together and relief-era blocks run
  to five units.
- Two entity guarantors sharing a base name and the last four of their EIN: the guarantor-by-name-and-TIN reading
  (SF16) merged groups the Party No keeps apart; an entity's TIN digits are now unique to its base name.
- A world drawn from streams whose shape followed the parameters: one parameter change re-drew every loan and moved
  the margins between builds; every draw is now keyed by group, unit, month and purpose.
- The earlier, more frequent transient delinquency: the roll-rate reading of delinquency at the reserve date moved
  the allowance 4.7 per cent, outside one sigma; transient delinquency is rarer and failures close faster.
- Open defaults counted as not charged off in the charge-off share: a construction no longer, ruled out as SF18 by
  policy 2.3 (a default still in liquidation is not resolved).
