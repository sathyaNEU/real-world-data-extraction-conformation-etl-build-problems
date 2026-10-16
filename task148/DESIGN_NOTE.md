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
| Spine | the servicing system's monthly loan history, one row per 7(a) loan per month from October 2009 to September 2026 (constructed, about 2.5 million rows, parquet) |
| Deliverables | `sba_allowance_fy2026.xlsx` (the allowance and its components, the ask tables), `allowance_note_fy2026.docx` (the board's one-page note with a chart) |
| People | drawn with `guard.py names --geo "United States" --seed 148`: Erin Spence (controller, books the allowance), Richard Fields (chief credit officer, SBA Lending, owns the allowance policy), Johnny Nicholson (SBA servicing manager, the servicing extracts), Donna Graves (special assets, workouts and charge-offs), Tara Williams (loan operations, SBA reporting); none appears in the prompt |

**Guard.** `guard.py check` at the draw: WARN `three_rules.strategy_risk` (grain_or_unit), no BLOCK. Answered: the
analyst test below runs the easy route with every field read and every filed sentence executed, the guarantee
register included, and it still files the wrong allowance, because reading who guarantees which loan is not the step;
the step is pricing each loan at the hazard of the group it fails with. The first check blocked on
`test.same_driver_older` against task142 (gap population, G2, Gate G forecasting): task142 builds an upper percentile of
a period's total from arrivals and durations; the card carries that differentiation line, and the ones against task133,
task143 and task132.

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
   loan's remaining contractual life on the loans in the relief-era pool at 30 September 2026, prime held at its level
   on that date; a loan is in default at the first month-end it is 90 or more days past due or accelerated.
2. Read the servicing history into loan-months from each loan's first payment, leaving the months SBA paid under
   Section 1112 out of the loans at risk.
3. Estimate monthly default and payoff hazards by months on book and term over every loan approved since FY2010, each
   loan at risk until its own default, payoff or maturity.
4. Roll each active pool loan forward from its months on book at 30 September 2026, conditioned on its survival to
   date, the default hazard against payoff and maturity; multiply each month's default probability by the loan's
   unguaranteed principal on its amortization schedule at the reserve-date rate, times the share of defaults the record
   shows ending in a charge-off; loans already in default at their charge-off share.

Ends on: about $7 million (paper value from the prototype, about 24 per cent under the golden; set on the built pack).
Golden: about $10 million (paper value; set on the built pack).

## Stump sentence

Building monthly default and payoff rates by months on book and term from every loan since FY2010 and rolling each
active relief-era loan forward on its own months on book books about $7 million (Ends on) at 30 September 2026; the step
that lands it there is pricing each loan as if it stood alone, when a loan whose operator guarantees other businesses
under the bank's cross-default fails whenever any of them fails, so its hazard is the sum of the group's businesses'
hazards at their own ages, and many of those businesses, financed outside the pool in FY2022 to FY2026, are young; the
allowance is about $10 million.

## Three rules

Written at the draw; every figure is the prototype's and is replaced by the built pack's at stage 3.

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
- **Layer 1:** the servicing history in the layout of a lender's monthly extract (status codes, days past due at the
  month-end, payment source codes, the SBA-paid Section 1112 months among them); the guarantee register's names written
  differently across an operator's loans (middle initials, suffixes) with the last four digits of the guarantor's tax
  number; SBA loan numbers in SBA's files against the bank's note numbers in its own; the Form 1502 report in SBA's
  layout; fiscal years ending 30 September against calendar dates; amounts in dollars and cents in one ledger and whole
  dollars in another. Each is what these systems write; none carries the stump (asserted at stage 3).
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
  depends on its group's other businesses' ages; the default path reads every one of them and still files about $7
  million.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the prompt's question, the
  allowance policy's estimand, default, charge-off and rate sentences, the loan authorization's cross-default clause) are
  executed word for word on the clean truth at stage 3 and give no figure of their own: they say what is counted and
  when a loan is in default, never a hazard, a group's hazard or how a loan's default probability is built; the
  estimators they admit (loan-level rates pooled, recent or by covariate) file about $7 million.
- **Analyst test:** a strong analyst who stages the pool cleanly, keeps the SBA-paid months out of the risk sets, reads
  the policy, the register and the loan authorization correctly and builds the textbook lifetime PD from monthly default
  and payoff rates by months on book and term over every loan since FY2010 books about $7 million (Ends on), because a
  loan whose operator carries other businesses fails when any of them fails and its own months on book say little about
  that; the last year's rates file about $7 million too, and a count of the group's loans at the loan's own rate about
  $9 million.
- **Estimand:** the allowance policy (section 2, to be written at stage 2): the unguaranteed principal the bank expects to
  charge off, over each loan's remaining contractual life, on every loan in the relief-era pool (7(a) loans approved in
  SBA fiscal years 2019 to 2021) on the books at 30 September 2026, loans in default not yet charged off included,
  recoveries not netted, prime held at its 30 September 2026 level; the population, outcome, window and unit are filed,
  the estimator is not.
- **No decoy:** no memo, prior-year allowance, model output, stakeholder figure or certified table states or argues a
  figure or a method; the loan authorization is the bank's standard template, read for its clauses, and argues nothing.
- **No certified replay:** no certified or published allowance ships and nothing graded is reproduced; the business
  hazards are estimated from the raw servicing history.
- **Lesson:** a loan's default is its guarantors' default: when one operator stands behind several businesses under
  cross-default, each loan fails when any of them fails, so its hazard is built on the group (every business the
  guarantors back, at its own age, inside the pool or not), and a loan rate pooled or recent, which averages the
  history's cross-defaults at the history's mix, misprices a pool whose groups are larger and younger; no build on file
  teaches a unit of default that spans several records behind one backer.

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
