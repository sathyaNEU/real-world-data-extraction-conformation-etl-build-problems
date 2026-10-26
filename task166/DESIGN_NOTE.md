# task166 design note

Architecture 2, drawn 2026-10-25 (wave 7 slot, Forecasting lane, sathya8571), a re-root after portal round 1. Architecture 1
(a regional bank's ALCO designating a swap overlay against one of five fixed-rate pools, seed FC37) was landed by both
portal responses on its golden: conditioning each commercial real estate balloon's extension on refinance cover at the
planning rate is a reflex for the portal's models, and both responses also fitted the mortgages' prepayment on their own
rate incentive, the textbook curve. Its identity is in the card's lineage and its dead ends below. Nothing of the seed or of
architecture 1's world is kept: this draw is a credit union's fixed-rate home equity book.

The decisive step was redesigned at stage 2, before any data was cut, against the portal's evidence. The draw's first
decisive step, reading each second lien's payoff off the first mortgage's own refinancing incentive, is the lock-in, the most
discussed housing story of 2023 to 2026, and a 2026 model that sees a credit report's first-mortgage tradeline takes it by
reflex; the prototype measured it as one cheap route (the book behind first mortgages above the 2027 rate, one group-by)
to its answer. It is now rung 2 and names the Lakeshore. The decisive step is the whole stack: a member pays the second off
by refinancing the debt on the house, and the stack's blended rate (the first and the second at their balances) against
the posted 30-year rate decides it. That names Muskegon and the North.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task166.json`, architecture v2, registered 2026-10-25T17:31:36Z, v1 in its
   lineage, edited in place at the stage 2 redesign (stump, driver, analyst and domain tests, Layer 2 pattern, Layer 1,
   spine, deliverables) and re-checked: `guard.py check` WARN, `repeat.decision` and `repeat.question_form` (pick, which,
   against task301 v2), answered below; nearest driver 0.05 (task154).
2. Pairing: Banking, Credit & Financial Risk (client domain) / `deposit-liquidity-behaviour` / Forecasting & Predictive
   Modeling. The client taxonomy files prepayment behaviour with deposit behaviour under this task type (its rigor group
   is deposit-prepayment-interest-rate-behavior, whose fourth card is a prepayment S-curve fitted pooled), and the task type
   serves forecasting. The deciding quantity is each region's 2027 home equity payoffs under the planning cycle's base case.
3. Niche: Hollowell Community Credit Union, a state-chartered credit union in West Michigan (about $4.1 billion of assets;
   regional lending centers in Grand Rapids, the Lakeshore, Kalamazoo and Battle Creek, and Muskegon and the North), whose
   Management Lending Committee opens a payoff-retention pilot (a dedicated mortgage loan officer who reaches home equity
   members before they pay off) in one region on Monday 4 January 2027: the region whose members will pay off the most
   fixed-rate home equity principal in 2027 (Lending Policy 7.4.2). The book grew fastest in the 2024 to 2026 equity-tap
   boom. Grand Rapids' taps sit behind large first mortgages, refinanced in 2020 and 2021 or written from 2012 to 2016; the
   Lakeshore's newer suburbs carry purchase seconds behind 2024 to 2026 first mortgages at 6.2 to 7.2 per cent; Kalamazoo
   and Battle Creek's 2023 purchase seconds sat behind first mortgages at the 2023 peak and have mostly paid off; Muskegon
   and the North's 2024 to 2026 taps are large ($70,000 to $112,000) and sit behind small, seasoned first mortgages opened
   from 2010 to 2015 at 3.5 to 4.75 per cent.
4. Call and shape: the region (`pick_one_of_n`, four regions, question form which), the principal its members will pay off
   in 2027 (payoffs and curtailments, $ millions to the nearest 10), and the region second. Shape `other`: the call with
   its components and one decoupled ask of 32 counts (two per region and quarter) with a chart.
5. Mechanism keys: gap population (what drives one loan's exit), decisive pattern E (each loan's payoff conditioned on the
   whole stack's refinancing incentive, an absolute split no column names) with G14 and G6 (the forward book's stacks
   differ from every closed year's: the record's large seconds sat on stacks whose blend met the market in 2019 to 2022,
   Muskegon and the North's new taps sit on stacks the 2024 to 2026 market never reached); Gate G
   `method_or_model_selection` (the record selects the stack's blended incentive over the own-rate, the first-alone, the
   two-incentive and the lien-by-lien models); strategy `composition_mix`.
6. Layer 2: `field_method`, pattern `own:junior-lien-payoffs-set-by-the-whole-stacks-blended-refinance-incentive`. The
   client's banking rigor card 4 carries the own-rate S-curve as the textbook route; the field's method for a closed-end
   second is to model its exits on the refinancing economics of the debt on the house, the first and the second together.
7. Furniture: forum `committee_or_panel` (the Management Lending Committee chooses the region at its meeting of 9 December
   2026); forcing event `launch_or_rollout` (the pilot opens on 4 January 2027); organisation family `financial_institution`;
   role family `finance_controller` (the lending analytics manager); context artifact `close_out_summary` (the third-quarter
   ALM report: balance sheet, net economic value and the home equity book's size, ranking no region); calibration
   `existing_book_actuals` (the credit union's own payoff history since 2019).
8. Spine: the new core's monthly trial balance of fixed-rate home equity loans (loan by month-end, September 2024 to
   November 2026, 197,078 rows) beside the legacy core's loan master for January 2019 to August 2024. The forcing file is
   the lending system's funded-loan file: each application's senior lien as the underwriter took it from the credit report
   (creditor, opened month, original amount, term where reported, balance at its reported month, payment as reported), and
   for a second funded with the purchase the first's terms from the purchase file. Credit reports carry no rate, so each
   first mortgage's rate comes from the amortization identity on its original amount, term and reported balance.
9. Deliverables: `he_payoff_pilot_2027.xlsx` (the call, its components and the ask's 32 counts) and
   `payoff_quotes_by_center.png` (the ask's quoted counts, one bar per quarter split by center); task303 v2 shipped a memo
   and a workbook and task485 v3 a workbook and a chart, so the pair is no template.
10. People, drawn with `guard.py names --geo "United States" --seed 166`: Sherri Bautista (lending analytics manager),
    Brandon Coffey (chief lending officer, owner of Lending Policy 7.4), Joel Singh (ALM and finance manager, the ALM report
    and the planning rates), Cody Li (loan servicing supervisor, the payoff desk). No persona is in the prompt. The credit
    union's name was checked against real credit unions (H21): no "Hollowell" credit union was found (Thornbrook was
    dropped, too near Thornapple Credit Union of Hastings, in the Grand Rapids region's own county list).

**Data-native sentence.** A closed-end second is paid off at the closing of a sale or of a refinance of the debt on the
house, and a member refinances that debt when the blend of the first mortgage and the second, each at its balance, sits
above a new first mortgage at the posted 30-year rate; Muskegon and the North's 2024 to 2026 taps are as large as the
seasoned first mortgages ahead of them, so a 4 per cent first locks nothing and those stacks blend near 6.5 per cent, a
level the posted 30-year rate never fell under in 2024 to 2026 and the planning path falls under from February 2027,
while the record's own payoffs never show such a stack in the money.

**Guard and similarity.** `guard.py check` on the edited card: WARN, two lines, no BLOCK. `repeat.decision`
(`pick_one_of_n`) and `repeat.question_form` (which) against task301 v2: the decision is a pick of one region, so the type
and form are the decision's own. The structural signatures (gap population, pattern E, `pick_one_of_n`; with
`method_or_model_selection`) repeat older builds only and carry a differentiation line each on the card. Nearest driver
0.05 (task154), 0.04 (task137 v1).

**Abstraction test.** Stripped of nouns: a junior unit leaves when the whole stack it sits in is replaced, and the holder
replaces the stack when its blended price at each layer's size rises above one new senior unit; the junior's own price and
the senior's own price, each a reflex's covariate, met the blend in the record and part from it in the forward book, where
the largest juniors sit on small cheap seniors. Read against the nearest by structure:
- task137 v1 conditions a renewal share at maturity on a unit's own rate gap; here a unit's own rate gap is rung 0.
- task500 v2 (lineage) reads a spillover on untouched units through another entity's register; here no spillover is
  estimated, a junior lien is retired with the stack it sits in.
- task28 v1 and task32 v1 (lineage) condition a volume or a yield on a property recovered through a join; here the
  property is a weighted blend of two rates, one recovered from a third party's summary of another lender's account by an
  amortization solve, at balances that move every month.
- Architecture 1 of this slot conditioned a maturity's extension on refinance cover; no maturity or cover decides here.
None shares the latent structure, the default path and the correction together.

**Sources, one line each.**
- `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` on the mechanism's nouns (second lien,
  first lien, blended rate, cash-out, tradeline, home equity, refinance): no card spends a junior lien's exit on the stack's
  blended rate.
- `stumping/references/client/layer2-rigor-patterns.md`, deposit-prepayment-interest-rate-behavior card 4: the textbook
  route is one incentive S-curve on the loan's own rate.
- `stumping/SKILL.md` 1.1b (the field's method at rung 0, the decisive step where the data violate its precondition) and
  Part 6 (the forcing file first: the lending system's senior lien is the only file that sees the first mortgage).
- `dataset-generation/references/layer1-messiness.md`, Banking 1 (monthly loan tapes with status transitions) and the
  universal techniques for a core conversion.

## Three rules

Task type: deposit-liquidity-behaviour (Banking, Credit & Financial Risk: prepayment behaviour, the client's rigor group deposit-prepayment-interest-rate-behavior), which serves Forecasting & Predictive Modeling; the decisive forecast is each region's 2027 home equity payoffs under the planning cycle's base case.
Domain test: the deciding quantity is each region's 2027 home equity payoffs, which prepayment modeling forecasts from the refinancing incentive of the whole mortgage debt on the house (the first mortgage and the closed-end second at their balances, their blended rate against a new first mortgage at the posted 30-year rate), because a member pays the second off at the closing of a sale or of a refinance of that debt; the first mortgage's rate is recovered from the credit report's tradeline by the amortization identity.
Swap: "which district opens the retention pilot, by the follow-up visits its patients will cancel next year" keeps a regional pick on a forecast count of exits, but loses a stack of liens retired together, a blended rate weighted by two balances, and a new first mortgage whose rate the blend is set against: with clinic visits nothing sits on anything, so the quantity the call turns on stops making sense.
Layer 1: the core conversion (the legacy master to August 2024, the new core's trial balance after it, loan numbers through the cross-reference), the legacy master's 2018 year-end balances in place of monthly ones, the lending system keeping the loan number assigned at funding, the senior lien as the credit report gave it (a reported month, a payment some servicers report with escrow, a term sometimes blank, purchase seconds with the first's terms from the purchase file), weekly rate sheets with mid-week reprices, close codes for maturity and charge-off, region from the collateral county, and on the ask's path the statement log's shared home equity product code, legacy numbers on title agencies' requests, updated and voided requests and UTC issue times; each is how its system writes and each is asserted neutral on the call in checks.py.
Layer 2: field_method (a closed-end second's prepayment modeled on the debt it sits in): the choice that flips the call is forecasting each loan's payoff from the whole stack's blended rate at the two balances against the posted 30-year rate, selected by the record over the loan's own rate, the first mortgage's rate alone, the two incentives side by side and each lien against its own posted rate, not from either loan's own rate.
Decisive step: recover each first mortgage's rate and its balance path from the senior lien the lending system took from the credit report, form each month's blended rate of the stack (first and second at their balances) less the posted 30-year rate a month earlier, fit the home equity loans' monthly payoff probability on it over every loan-month since 2019, and run the loans on the books at 30 November 2026 through 2027 on the planning cycle's base case, summed by region.
Not semantics: every field is read correctly on the default path and on rung 2 (the conversion, the codes, the payoffs, the posted rates, the senior lien's rate recovered exactly); a prepayment curve on the loan's own rate is the textbook construction and the lock-in on the first's own rate is the reflex refinement, both fit the 2019 to 2026 payoffs, and both are the wrong forecast for a book whose largest new seconds sit on small seasoned firsts.
Not rule application: no filed rule forecasts a payoff; Lending Policy 7.4.3 files the estimand (the loans on the books at the close of 30 November 2026, principal paid ahead of schedule, calendar 2027, the region of the collateral county, the base case, $ millions) and nothing about behaviour, and executing every filed sentence with an own-rate model names Grand Rapids and with the first mortgage's own incentive the Lakeshore. Enumerated family (own rate, first alone, the two side by side, each lien against its own posted rate, the blended stack, each with and without region effects, trailing payoffs): the pick spans all four regions and Muskegon and the North's figure 9.4 to 43.9. Standing family (the blended stack under every form and convention the record leaves defensible: logistic and complementary log-log, knots, seasonality, the purchase marker, region effects, rates as day-weighted or simple monthly averages, lag 0 to 2 months, payoffs with and without December 2026): one pick, Muskegon and the North, at 36.5 to 41.3, every value in the $40 million bin. Loudness of the ruling-out: a likelihood comparison the analyst has to run, deviance 48,888 for the blend against 49,295 lien by lien, 49,431 two incentives, 49,476 first alone and 52,395 own rate, on 5,264 payoffs; no clause and no one-group-by comparison eliminates the rivals.
Analyst test: a strong analyst who joins the two cores, reads every field and fits the home equity payoffs on each loan's own note rate against the posted home equity rate, validated on the 2019 to 2026 payoffs, names Grand Rapids at about $60 million; one who reads the lock-in off each first mortgage's own rate names the Lakeshore; a trailing payoff rate names Kalamazoo and Battle Creek; only the stack's blended rate names Muskegon and the North at about $40 million (executed in checks.py on the generator's clean truth).
Estimand: Lending Policy 7.4.3 (a shipped PDF) files the population (the fixed-rate closed-end home equity loans on the books at the close of business on 30 November 2026, loans funded after it and home equity lines excluded), the outcome (principal paid ahead of schedule: payoffs before maturity and curtailments; scheduled principal, a final scheduled payment and charge-offs excluded; a loan the credit union refinances itself is paid in full), the window (payments posted 1 January to 31 December 2027), the region (the county of the collateral through the county map), the rates (the planning cycle's base case, monthly averages of posted rates) and the unit ($ millions); 7.4.2 files the decision rule; the prompt adds the pilot's start and the rounding.
No decoy: no memo, draft, ranking, vendor speed table, model output or stakeholder figure argues for any region or any behaviour; the ALM report states the book's size and ranks no region; nothing is copied, backfilled or withheld.
No certified replay: no shipped figure is to be reproduced to recover a method; the payoff record and the credit reports are closed outcomes every route reads alike.
Lesson: a model learns that a second lien's run-off is set by the refinancing economics of the whole debt on the house, the first and the second at their balances against one new first mortgage, so neither the loan's own rate nor the first's rate alone puts a refinance wave's exits on the right loans once large seconds sit on small cheap firsts; no build on file conditions one claim's exit on a blend of its own and another claim's rate.

## Default path
1. Read Lending Policy 7.4: the fixed-rate home equity loans on the books at 30 November 2026, their 2027 principal paid
   ahead of schedule under the planning cycle's base case, by the region of the collateral county.
2. Stack the legacy master and the new core's trial balance through the conversion cross-reference into one loan-month
   history, January 2019 to November 2026, with each loan's balance, note rate, payoffs, maturities and charge-offs; join
   the region from the lending system's collateral county.
3. Fit the textbook prepayment curve: each loan-month's payoff probability on the loan's own incentive (its note rate less
   the posted fixed home equity rate for its term a month earlier), with seasonality, validated on the 2019 to 2026 payoffs
   (the strong analyst's reflex, and the one both portal responses took on architecture 1's mortgages).
4. Run each loan on the books through 2027 on the base case, whose posted home equity rate falls under the 2024 to 2026
   notes from the first quarter; add curtailments at the core's recent rate.
5. Sum by region and pick the largest.

Ends on: Grand Rapids ($60 million)
Golden: Muskegon and the North ($40 million)

## Stump sentence
Fitting the home equity payoffs on each loan's own note rate against the posted home equity rate names Grand Rapids at
about $60 million, and reading the lock-in off each first mortgage's own rate names the Lakeshore; the step that lands it
there is reading a second lien's payoff off one of the two loans, when a member pays the second off by refinancing the
whole debt on the house, which the stack's blended rate at the two balances against the posted 30-year rate decides:
Muskegon and the North's large 2024 to 2026 taps sit behind small seasoned first mortgages at 3.5 to 4.75 per cent, so
those stacks blend near 6.5 per cent, come into the money as the planning path falls, and pay off about $40 million.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| Rung 0, own-rate S-curve (Grand Rapids) | the policy names the outcome, not a model | note rate and posted home equity rates are columns | the textbook prepayment curve, the default | none | none | no | no organ | readable |
| Rung 1, trailing payoffs (Kalamazoo and Battle Creek) | none | payoff codes and balances are columns | a run-rate carry, a common shortcut | none | none | one group-by | no organ | readable |
| Rung 2, the first mortgage's own incentive (the Lakeshore) | none | the senior lien fields name the first mortgage; its rate is recovered | the lock-in, the 2023 to 2026 housing story | none | none | no | the lending file carries the senior lien for underwriting (combined loan-to-value, debt-to-income) | readable |
| Rung 3, the stack's blended rate at the two balances (decisive) | no sentence names a blend, a stack, a cash-out or a consolidation | no column holds the blend or the share of the stack; the first's balance path comes from the amortization identity | the reflex stops at the first's own rate | no control reproduces under the blend alone | no battery step touches it | a weighted blend of two recovered rates at two moving balances, against the market | the senior lien ships for underwriting; deleting the step leaves every file in the pack | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "on the books at 30 November 2026" | the trial balance's 2026-11-30 rows with status ACTIVE | add the rows closed in November (status PIF on 2026-11-30) | same call (their balance is nil) | same call; 7.4.3 "on the books at the close of business on 30 November 2026" |
| SF2 | "pay off" (the outcome) | payoffs at the balance retired plus curtailments | payoffs only | same call (MN 37.0, LS 22.6) | 7.4.3 "any principal paid in a month above that month's scheduled principal" |
| SF3 | "in 2027" | payments posted 1 January to 31 December 2027 | December 2026 counted too | same call (MN 40.0) | 7.4.3 "payments posted from 1 January 2027 to 31 December 2027" |
| SF4 | "region" | the collateral county's center through the county map | a member's branch or address | same call (no other region field ships) | 7.4.3 "the county where the collateral property sits, as the county map assigns it" |
| SF5 | "fixed-rate home equity" | closed-end fixed-rate loans in both cores | lines of credit added | same call (lines are a separate extract) | 7.4.3 "home equity lines of credit are a separate product and are not in it" |
| SF6 | the rate path | the planning workbook's base case | an alternative scenario | not computed | 7.4.3 "the planning cycle's base case" |
| SF7 | a month's posted 30-year rate | the day-weighted average of the sheets in effect | the simple average of the month's sheets | same call (MN 39.1) | same call |
| SF8 | the rate's lag | the month before | the same month, two months before | same call (MN 41.3, 36.5) | same call |
| SF9 | maturities | a final scheduled payment is not ahead of schedule | count maturities as payoffs | same call | 7.4.3 "including the final scheduled payment of a loan that reaches maturity" |
| SF10 | charge-offs | not principal paid | count them | same call | 7.4.3 "a balance charged off is not principal paid" |
| SF11 | the credit union's own refinances | paid in full | excluded | same call (the cores code them PIF) | 7.4.3 "A loan the credit union refinances itself is paid in full" |
| SF12 | a blank senior-lien term | the term whose payment the reported payment carries | 360 months always | same call | same call |
| SF13 | payments made by the reported month | months from opening to the reported month | one fewer | same call | same call |
| SF14 | legacy balances | scheduled from the 2018 year-end balance or the funding | the original amount throughout | same call | same call |
| SF15 | "to the nearest 10" (millions) | 39.2 prints 40 | 35 or 45 | same call | the prompt's rounding sentence |
| SF16 | "which center comes second" | the Lakeshore (23.9 against Grand Rapids 18.5) | none | same call | same call |
| SF17 | "quoted a payoff for" (ask) | an issued or updated statement whose amount paid the loan off, the log's, a first-mortgage statement that also paid the loan, or the outage log's | statements naming the loan only | asks only | the prompt's "quoted a payoff for" |
| SF18 | "counted once in a quarter" (ask) | distinct loans per quarter | statements | asks only | the prompt's "a loan counted once in a quarter however many quotes it had" |
| SF19 | a quote's quarter (ask) | the Eastern calendar date it was issued | the UTC date | same counts (issue times 8 a.m. to 6 p.m. Eastern) | same call |
| SF20 | "paid in full by 30 November 2026" (ask) | core status PIF with a close date on or before 2026-11-30 | maturities or charge-offs counted | asks only | the prompt's "paid in full" and the core's codes |
| SF21 | voided requests (ask) | not a quote | counted | asks only | the log's VOID: "requests voided before a statement was issued" |

## Ladder

Every route runs on the shipped files (`generator/calc.py`, `routes`), 2027 principal paid ahead of schedule, $ millions.

| Rung | Construction | Grand Rapids | the Lakeshore | Kalamazoo and Battle Creek | Muskegon and the North | Names | Margin |
|---|---|---|---|---|---|---|---|
| 0, default path | own-rate S-curve (note rate less the posted home equity rate for the term) | 58.7 | 25.5 | 14.5 | 43.9 | Grand Rapids | 1.34 |
| 1 | trailing payoffs, December 2025 to November 2026, carried forward | 10.6 | 8.1 | 14.6 | 9.4 | Kalamazoo and Battle Creek | 1.38 |
| 2 | the first mortgage's own incentive (the lock-in) | 17.4 | 23.0 | 13.1 | 12.5 | the Lakeshore | 1.32 |
| 3, decisive | the stack's blended rate at the two balances | 18.5 | 23.9 | 13.5 | 39.2 | Muskegon and the North | 1.64 |

- Each rung dies to one shipped fact or construction: rung 0 to the record's 2024 to 2026 taps behind locked stacks, whose
  own rate was in the money and which did not pay off (deviance 52,395 against the blend's 48,888); rung 1 to the planning
  path (the trailing year is the 2023 cohort's wave, mostly already paid off); rung 2 to the record's seasoned stacks,
  whose firsts were out of the money and which paid off as their blend crossed the market (deviance 49,476).
- The rivals between the rungs: the two incentives side by side name the Lakeshore (1.21); each lien against its own
  posted rate names the Lakeshore (22.9 against Muskegon and the North 22.0, 1.04, deviance 49,295); the own rate with
  region effects names Grand Rapids (1.31); the first alone with region effects the Lakeshore (1.27); the own and first
  curves fitted on 2023 to 2026 alone name Grand Rapids (1.36) and the Lakeshore (1.22); gradient-boosted trees on the home
  equity loans' own fields, with or without the region, name Grand Rapids in four of four runs (`generator/rivals.py`).
- Position of the golden: second on rung 0 (Grand Rapids leads by 1.34), third on rung 1, fourth on rung 2.
- Separation: every rung names a different region; the golden is named by the decisive rung and its forms only.
- Dominance: Muskegon and the North's stacks gain 1.2 to 1.6 points of incentive between November 2026 and the second
  quarter of 2027 (from about -0.3 to above 1.0), against the Lakeshore's purchase stacks, already partly in the money at
  the as-of; the region's lead is its seconds' size in the stack, carried by no rung below.
- Grid: every correction walks the same way until the stack (own rate to the first's rate moves the pick from Grand Rapids
  to the Lakeshore; adding region effects or a second incentive keeps it there); only the blend at the two balances
  reverses to Muskegon and the North, and its forms agree on the pick in every member of the standing family.
- Residual risk, measured (`generator/rivals.py`): gradient-boosted trees given the stack's own fields (both rates, both
  balances) name Muskegon and the North in four of four runs (its figure 15.9 to 41.6; the two runs without the
  incentives by a hair, 16.1 and 15.9 against Grand Rapids' 15.6), and a screen of the book whose stack blends above the
  2027 planning average names it too (112.3 million of balance, 2.0 over the Lakeshore) while carrying no 2027 figure;
  each has taken the decisive step's construction, the first mortgage recovered from the senior lien and set beside the
  second at the two balances. The same screen on the first mortgage alone names the Lakeshore (52.3, 2.0).
- Figure and bin: the standing family's Muskegon and the North spans 36.5 to 41.3 (golden 39.19), every value in the $40
  million bin [35, 45); the nearest member to an edge is the two-month lag at 36.5, 1.5 inside.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the loans on the books at the close of 30 November 2026 | filed, 7.4.3; SF1 |
| 2 | Unit of account | a loan; principal in dollars | filed, 7.4.3 ("Unit: dollars of principal") |
| 3 | Attribution window | payments posted in calendar 2027 | filed, 7.4.3; SF3 (December 2026 counted too gives the same call and bin) |
| 4 | As-of dating | the book at the 30 November 2026 close; rates a month earlier | filed as-of; SF8 lag converges |
| 5 | Version basis | the cores as pulled on 3 December 2026 | one pull; C1 |
| 6 | Denominator | none in the call (a dollar total) | n/a, same call |
| 7 | Weighting | each loan at its own balance | the outcome is a dollar total; C1 |
| 8 | Window length | the hazard fitted on every loan-month since January 2019 | C1: fits on 2023 to 2026 alone keep the pick (blend 41.2) |
| 9 | Boundary inclusivity | payments posted 1 January to 31 December 2027 inclusive | filed, 7.4.3 |
| 10 | Rounding path | the regional total rounded once, to the nearest 10 million | the prompt's rounding sentence; SF15 |
| 11 | Tie-break | none (margin 1.64) | C1 |
| 12 | Maturity and censoring | maturities and charge-offs leave the risk set and are not payoffs; the record runs to November 2026 | filed, 7.4.3; SF9, SF10 |
| 13 | Order of operations | survival through each month before the month's payoff | standard; C1 |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per loan per month in each core; the conversion month from the legacy balance | C1 |
| 16 | Identity normalisation | legacy numbers to new through the cross-reference; the lending file's funding number mapped the same way | dictionary semantics; C1 |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | dollars and per cent in both cores (the new core's rate a decimal fraction) | dictionary semantics |
| 19 | Code and status semantics | PIF a payoff; MAT, CO and CHGOFF not | dictionary semantics; SF9, SF10; never the stump |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | 7.4.3 governs the forecast; 7.4.2 the decision | filed |
| 22 | Forward window contents | the planning cycle's base case, December 2026 to December 2027 | the shipped planning workbook; SF6 |

## Literal reader

Executed word for word, Lending Policy 7.4 and the prompt fix the population, outcome, window, region, rates, unit and
rounding; every convention left open (SF7 rates, SF8 lag, SF12 term, SF13 payments counted, SF14 legacy balances, SF2 and
SF3 read the other way) keeps Muskegon and the North and the $40 million bin, and the easy routes differ from the golden by
method on the same literal estimand (the own rate or the first's rate in place of the stack), never by a reading.

## Oracles

- The third-quarter ALM report: the book's size and weighted note rate at 30 September 2026, reproduced from the trial
  balance; it ranks no region and carries no speed.
- The payoff statement log: it ties to the cores' payoffs where a statement was issued, under every reading; it is the
  ask's file and the call never reads it.
- The county map and the conversion cross-reference: lookups, the same under every route.
- No control reproduces only under the golden or only under a wrong route.

## Ask sheet

One ask, 32 counts, on rows the call never reads (asserted in checks.py: the statement log, the outage log and the first-
mortgage servicing file are not opened by the golden's computation, and deleting them leaves the call byte for byte).

- **The ask: for each regional lending center and each quarter from October 2025 through September 2026, how many fixed-
  rate home equity loans the credit union quoted a payoff for, a loan counted once in a quarter however many quotes it had,
  and how many of those loans had been paid in full by 30 November 2026 (16 cells, two counts each).** Use and H18 home:
  the pilot's mortgage loan officer works from payoff quote requests, the earliest notice a member is about to pay off;
  the committee sizes the officer's load and the quote-to-payoff share by center. Files: the payoff statement log, the
  outage log (`payoff_statements_manual_2026-03.xlsx`), the first-mortgage servicing file, the trial balance (payoff
  status), the conversion cross-reference and the lending file (collateral county and address): six files, 14 columns on
  the path.
- **Primary 1, a first-mortgage statement that also quotes the home equity loan (D6 and D7, silent, a reconstruction).**
  When the credit union holds a member's first mortgage, the title agency asks for every lien it holds and the desk
  issues one statement on the mortgage's number for both: the log shows product MTG and the mortgage number, and only its
  amount, the mortgage's payoff plus the home equity loan's, shows the second loan was quoted (238 loan-quotes, every
  cell). The log's other first-mortgage statements quote the mortgage alone: the credit union's 2,362 first mortgages with
  no home equity loan behind them (their payoffs since 2025 and requests that fell through), members with a home equity
  loan behind the credit union's first who asked for the first's payoff alone (a refinance of the first shopped, a payoff
  from savings considered), and closings whose first request named the first mortgage before the title search found the
  second lien (485 of the 724 issued or updated MTG statements). So noticing the MTG rows does not settle the ask: the
  reader rebuilds each mortgage's scheduled balance at the prior month-end from the servicing file, reconciles the amount
  against it and the home equity loan's balance at the same property (asserted to the cent, A5; a coarser reconciliation
  converges, A11), and a reader who counts every MTG statement at a booked loan's address misses all 16 quote counts and
  7 of the paid counts (A12). Fair: each amount equals one payoff or the two at the good-through date. Silent: no column of
  the system's log marks it; the battery's unmatched-join sweep sees a mortgage statement matched to a mortgage.
- **Primary 2, the outage fortnight (D4, absence evidenced in a file no habitual join reaches).** The statement system was
  down from 9 to 20 March 2026 (the dictionary says so, as a system's documentation would) and the desk kept a workbook of
  hand-prepared statements with the borrower's name, the property address, the liens quoted and no loan number (53
  loan-quotes, the four first-quarter cells). Fair: each home equity row's address matches one lending-file collateral
  address after case and punctuation are normalised; its liens column carries "1st mortgage" rows too, not quotes of the
  second loan.
- **Hazards (seen, repaired right, texture):** legacy loan numbers on requests from title agencies holding pre-conversion
  statements (through the cross-reference); product HE covering home equity lines (not in either core's fixed-rate
  book); updated statements and voided requests; a loan quoted in the month it was funded (the amount funded, no prior
  month-end); issue times in UTC (inert for the quarter: every issue falls 8 a.m. to 6 p.m. Eastern).
- Screened against 1.1e: no column, code or comment of the statement system's log marks a statement covering two liens or
  a hand-kept quote; the second loan shows only in an amount reconciled against two systems' balances, and the outage only
  as missing days and the dictionary's note of the upgrade. The hand log's liens column states what each hand statement
  quoted, as a desk's log does; it can tell a reader that one statement may quote two liens, and the reconciliation is
  still the work.

| Ask cells | Figures | Cracker and mirror routes (`generator/ceiling.py`) | Verdict |
|---|---|---|---|
| Loans quoted, four centers by four quarters | 16 | quotes naming the loan (new or legacy number), updates and voids handled, lines excluded; with or without the outage log; every MTG statement at a booked loan's address counted unreconciled | miss |
| Of those, paid in full by 30 November 2026 | 16 | the same routes, payoffs from the core (the unreconciled MTG route keeps 9 of these 16) | miss |

Pair ceiling: 31.6 (cracker 48.1 with the call landed and 0 of 32 counts, the chart's two structural criteria kept; mirror 15.1; generated-rubric weights 38, 7, 55; a reader who reconciles the mortgage statements but skips the outage workbook keeps 24 of 32, one who counts every MTG statement unreconciled with the outage workbook 9 of 32)

Mirror leakage: 5.7 per cent of ask weight (the chart's structure only; 0 of 32 counts)

Measured by: generator/ceiling.py

## Prompt

`prompt.txt`, one paragraph, question first: which center opens the pilot, how much principal its members will pay off in
2027 and which center comes second; the workbook with the 32 counts; the chart; the rounding once at the end. Gated by
`voice-check.py`.

## Build record

Stage 3, 2026-10-25, worktree build on main at 876c00de (pulled with the work autostashed before the corpus gates).

- Generator (`task166/generator/`): `common.py` (constants, people, dates), `world.py` (the clean truth: posted rates,
  the stacks by region, the monthly payoff hazard on the stack's blend, curtailments, maturities and charge-offs),
  `records.py` (both cores, the cross-reference, the lending file, the servicing file, the county map, the rate sheets,
  the lines, the house price index), `asks.py` (the statement log and the outage workbook), `docs.py` (Lending Policy
  7.4, the ALM report, the planning workbook, the dictionary, the manifest), `postprocess.py` (containers), `calc.py`
  (the golden and every route, from the shipped files only), `deliver.py` (the workbook, the chart, `figures.json`,
  `submission.md`), `metadata.py`, `checks.py` (85 assertions), `verify.py` (25 checks on its own code path: the csv
  module, numpy, openpyxl, pypdf, pdfminer and zoneinfo, no generator module), `ceiling.py` (the ask routes),
  `rivals.py` (the rivals beyond the ladder), `build.py`.
- Pack: 16 files in 4 formats (csv, pdf, txt, xlsx); the new core's trial balance holds 197,078 rows; distractors
  `heloc_lines_2026-11.csv` and `county_house_price_index_2019q1_2026q3.csv` (S2: the call and the asks unchanged with
  both deleted).
- Gates: `checks.py` 85 of 85 (G, C, L, F, SF1 to SF21, A1 to A12, S, M, R1 to R3c, D, Q); `verify.py` 25 of 25 (the
  call recomputed at Muskegon and the North 39.19, the Lakeshore 23.90, Grand Rapids 18.47, Kalamazoo and Battle Creek
  13.52; rungs 0 to 2 by name; all 32 counts; every format read back, the policy through a strict reader and pdfminer);
  two builds byte-identical (target, golden, figures); `figures_check.py` 70 figures, 0 absent; `precut.py` 51 checks,
  0 FAIL, 0 WARN; `voice-check.py` PASS; `scrub_producer_metadata.py` clean on `target/` (band 2026-03-01 to 2026-12-08)
  and `golden/` (2026-12-03 to 2026-12-09), the PNG with no text chunk; `ceiling.py` pair 31.6, mirror leakage 5.7 per
  cent.
- `leak.py --asof 2026-12-03`: REVIEW, no LEAK, seven REVIEW lines, each read and harmless:
  - sweep 4, `lending_policy_7-4_he_payoff_forecast.pdf`: the domain's own words (region, million, mortgage, credit,
    posted, balance) in the estimand's sentences; it names no move, no stack, blend, lock-in or model;
  - sweep 4, `alm_report_2026_q3.pdf`: the same words in a balance sheet and rate-shock tables; it names no move and
    ranks no region;
  - sweep 4, `data_dictionary.txt`: the words in field descriptions that say what a row is; it names no move;
  - sweep 9, `first_mortgage_servicing_2026-11.csv`: the dates after the pull are active mortgages' maturity dates, a
    forward-dated field;
  - sweep 9, `heloc_lines_2026-11.csv`: the dates after the pull are open lines' draw-period ends, a forward-dated field;
  - sweep 9, `payoff_statement_log_2025-10_2026-11.csv`: the dates after the pull are good-through dates on statements
    issued in late November 2026, every issue time on or before 30 November;
  - sweep 9, `planning_cycle_2027_rates.xlsx`: the dates after the pull are the plan's month labels, December 2026 to
    December 2027.
- Reader B's ALM "mismatch" (8,567 loans in the report against 8,662 rows in the trial balance at 30 September 2026) is
  not a defect: the report's 8,567 loans and USD 424.2 million match the trial balance's ACTIVE rows at 30 September 2026
  exactly (verify V5), and the other 95 rows are loans that closed that month, which the dictionary says the trial
  balance carries ("including the month a loan closed").
- `guard.py heart`: WARN, no BLOCK (`repeat.decision` and `repeat.question_form` against task301 v2, answered at the
  draw; `test.same_puzzle_older` and `test.same_driver_older` differentiated on the card, every line rewritten for the
  stage 2 step); nearest driver 0.05 (task154), nearest stump 0.06 (task133). `guard.py surface`: exit 0, task167 back to
  back on the cards' gap, pattern, Gate G mechanism and context artifact (task167 v2 registered 2026-10-18, a week before
  this card's re-registration; its differentiation line: a fund's draw schedule read from funds financed like it, a
  class read from entry data, against a blend of two liens at their balances) and fifteen card-level pairs at surface
  0.101 to 0.104, left to the author's optional `/clone-check`.
- `target.zip` sha256 f022d2a94b534aad60cf312d47530b6b1cb007572ec9d90e47adf0788f48bdf2 (16 members, each equal to
  `target/`).
- Stage 5, 2026-10-25: the judge's finding 1 fixed in `deliver.py` (write-up step 2's loan-month count, 362,831 against
  the judge's 368,405 on a construction that keeps closing months, is dropped from step 2 and `figures.json`; it was
  incidental); the final rebuild leaves `target/` byte-identical and `target.zip` at f022d2a9.

## Pre-ship check

1. Domain: the call is a prepayment forecast of closed-end second liens, each loan's monthly payoff read off the
   refinancing economics of the whole debt on the house (the first mortgage recovered from the senior lien by the
   amortization identity, blended with the second at their balances, against the posted 30-year rate); with another
   field's nouns there is no stack of liens a new first mortgage replaces, and the quantity that decides the call stops
   existing.
2. Layer 1: the core conversion with its cross-reference, the legacy master's 2018 balances, legacy loan numbers in the
   lending file, the senior lien as a credit report gives it (escrow in one servicer's payments, blank terms, purchase
   seconds' terms from the purchase file), weekly rate sheets, the close codes, the county map, and on the ask's path the
   shared product code, legacy references, updates, voids and UTC times; each is how its system writes, none is planted,
   and each mishandled keeps the call (R2, M1 to M6).
3. The step that flips the call is a model choice the record makes, the covariate a second lien's payoff hazard reads
   (the stack's blend against the own rate, the first's own rate, both side by side or each lien against its own posted
   rate), selected by likelihood on 5,264 payoffs; no field, code or stated rule decides it.
4. Analyst test (R3a, R3b, on the clean truth): reading every field right and executing 7.4.3 with the textbook own-rate
   curve names Grand Rapids at about $60 million, the lock-in on the first's own rate the Lakeshore, the trailing year
   Kalamazoo and Battle Creek; only the stack names Muskegon and the North at about $40 million.
5. The estimand is filed: Lending Policy 7.4.3 gives the population, outcome, window, region, rates and unit, and the
   prompt the rounding; the method stays open and the record forces it (deviance 48,888 against 49,295 to 52,395), the
   standing family inside the $40 million bin (36.5 to 41.3).
6. No decoy: no memo, draft, ranking or model output argues for a region or a behaviour; the ALM report states the
   book's size and rate and ranks nothing.
7. No certified-figure pin: no shipped figure ties only under the golden or only under a wrong route.
8. The lesson (a second lien runs off with the whole stack's refinancing incentive, so its own rate and its first's rate
   alone put a refinance wave's exits on the wrong loans once large seconds sit on small cheap firsts) is taught by no
   earlier build: nearest driver 0.05, nearest stump 0.06.
- Asks: one ask of 32 counts on rows the call never reads (S1, S3), primary 1 a reconstruction (first-mortgage
  statements reconciled against two systems' balances, 238 loan-quotes beside 485 statements quoting the first alone),
  primary 2 the outage workbook (53 loan-quotes); the cracker keeps 0 of 32, an unreconciled count 9 of 32; pair ceiling
  31.6.
- Input gates: 16 files, 4 formats, a 197,078-row trial balance, two distractors, every file's source, date and licence
  in `metadata.json`.
- Stage 4 on f022d2a9: the determinism judge DETERMINISTIC, APPROVE (Gate G method_or_model_selection,
  analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain, layers and decisive step pass;
  every graded figure reproduced, its finding 1 fixed above, its caution 3 on the mortgage statements' balance date
  answered by the servicing file's note terms, which decide each statement). Leak reader A (Sonnet, medium) missed the
  call: the Lakeshore at $20 million on the first mortgage alone, Grand Rapids second, asks 0 of 36 (`score_reader`
  PASS). Leak reader B (Opus, medium) landed it: Muskegon and the North at $40 million (36.4) with the Lakeshore
  second, by fitting the own-rate, first-only and blended-stack incentives and keeping the blend on full-history fit
  and on a 2019 to 2022 fit tested on 2023 to 2026; asks 0 of 36 (`score_reader` exit 1, call 3 of 3). Neither reader
  found a decisive-step sentence, a helping file or a main-call fork.
- Shipped 2026-10-25 under the author's ruling ('yea ship') with the Opus reader landing the call; Gate F risk
  accepted; if the portal lands it, re-root to architecture 3 off the enumerate-and-back-test chain (grain, population
  or censoring).

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
- Convenience extensions at high cover (about 1 per cent at any cover, the round 3 recheck's suggestion), at stage 4
  round 4: a logistic has no floor, so a few extensions at covers of 1.5 to 2.5 flattened the fitted scale from 0.023
  to 0.09 and split the family by 15 to 34 million in the lab; dropped, the response has none above a cover of 1.25.
- Softening the shoulder instead (3 per cent of maturities at covers of 1.10 to 1.35 taking the extension): the family
  held in the lab, but in the file-built golden the near-best hard cut at 1.12 left the middle half with one sigma
  (152.0 plus 0.6); dropped.
- Trailing twelve-month statements for the hotels and retail centres maturing in 2020 and 2021, so their decisions read
  the pandemic: a solver who reads only the fiscal-year statements sees those loans extend at covers of 1.5 to 2.3 and
  files 141.1 in the lab; dropped. The pandemic reaches the record through the 2020 statements, so its extensions run
  from 2021, and the 2020 maturities read 2019 statements (52 of 54 repaid).
- Sale extensions whatever the cover (round 2's 1.2 per cent): on the keyed world a sale-pending six months at a cover
  of 0.81 put a non-extension in the wall's densest band and moved the band constructions by 2.5 to 3.1; a sale repays
  the loan only from a property with equity, so a sale extension now needs a cover of 1.0 or more.
- Statements reviewed after a loan's payoff left in the operating statement file: the fiscal-year reading then picked up
  a hotel's collapsed 2020 statement for a loan paid in February 2021 and moved 4.6; the file now closes with the loan's
  credit file at its payoff.
- Keeping the round 2 realization: with one stream through the book, adding hotels or the ramp moved every later loan's
  draws. Each loan now draws from streams keyed by its origination month and place; on that world the round 2
  settings alone fail the middle half (lab spread plus sigma 5.7), and the ramp, the equity rule and the break at 1.10
  together hold it (2.2).
- The break kept at a cover of 1.08 on the keyed world: the 1.00 rule landed (inside the bin by 0.1); moved to 1.10.
- Loans below a cover of 1.0 sent to special assets at their original maturity (the recheck's coherence exceptions): the
  plateau the wall sits on would fall by about 0.07 and the figure by about $5 million, with a fork on how a transfer
  is read; dropped, and the support agreement and interest reserve that make the plateau real are filed instead.
- A deeper push (pro forma rents 19 to 21 per cent over actual) for a tighter family: the spread fell (lab 2.0) but the
  1.00 rule and every 2027 balloon extended landed; kept at 15 per cent.
- More lending after the push (14 to 18 loans a month from May 2022) to lift every 2027 balloon extended further above
  the bin: the near-best cut at 1.12 left the middle half (lab 2.8 to 3.0); kept at 10.
- The support agreement filed with an income condition ("Where the property's net operating income falls short of the
  extension's payments, the extension is granted on the guarantor's support agreement..."), at stage 4 round 4: the
  reader read it as a mild-to-moderate hint and the recheck as the first filed sentence setting income against forward
  debt service, one step from the cover metric; reworded as a blanket practice on every extension, the pin that the
  payments are made as scheduled kept, no figure moved.
- Portal round 1 (2026-10-25): both responses landed the call, Fixed-rate commercial real estate at $150 million, so conditioning each balloon's extension on refinance cover at the planning rate is a reflex for the portal's models, not a decisive step; the stump sentence's step is spent and the build returns to stage 2.
- Architecture 1 re-rooted at the draw of 2026-10-25, its card's identity moved to the v2 card's lineage: the portal's
  models executed every correction the ladder held (the servicing stitch, an incentive curve on the mortgages' own rates,
  the cover-conditioned extension chosen on held-out maturities), so a redesign inside the overlay world would only add a
  rung above a spent one; the new draw makes the own-rate prepayment curve, the reflex both responses showed, the wrong
  route.
- A plain 2027 run-off figure for the plan (the home equity production that would hold the book flat) as architecture 2's
  call, at the draw: `quantity_figure` with gap population and pattern E repeats task170 v5's structural signature inside
  the batch (`guard.py` test.same_puzzle), and the payoff forecast's own decision is where the retention pilot opens, so
  the call is the pilot's region with its payoff figure.
- The first mortgage's own refinancing incentive (the lock-in) as the decisive step, the draw's first design, at stage 2
  before any data was cut: the lock-in is the most discussed housing story of 2023 to 2026, a 2026 model that sees a
  first-mortgage tradeline takes it by reflex, and the prototype found one cheap route to its answer (the book behind
  first mortgages above the 2027 rate, one group-by, 1.95 over the next region). Kept as rung 2, where it names the
  Lakeshore; the decisive step became the whole stack's blended rate at the two balances, which names Muskegon and the
  North and which no column or one-group-by reaches.
- A semiannual bureau refresh as the forcing file (the draw's plan): it would carry every member's tradelines twice a
  year for eight years, a file several times the size of the cores, to give what the lending system already holds from
  the application's credit report; the senior lien as the underwriter took it is the forcing file, and the first's balance
  path follows from the amortization identity.
- Purchase seconds' first mortgages from a credit report, at the first build: a first opened in the month the second was
  funded is not yet on the report, so its balance reads the original amount and no rate solves; the lending file takes a
  simultaneous second's first-mortgage terms, its rate included, from the purchase file, as an underwriter does.
- Muskegon and the North's seasoned stacks above a blend of 7 per cent (the prototype's first world): they refinanced in
  the record's 2025 and 2026 dips, so the trailing payoffs and a boosted tree on the home equity loans' own fields named the
  golden; the stacks were sized to blend near 6.5 per cent, quiet while the posted 30-year rate held at 6.6 to 7.3 per cent,
  and the record's 2024 to 2026 rates were set so no month reaches them.
- A small 2019 to 2022 book in Muskegon and the North, made of old seasoned stacks: trees on the home equity loans' own
  fields with a region marker carried its 2022 payoff rate (0.16 a year at mid rates, against 0.07 elsewhere) onto 2027 and
  named the golden at implausible levels (41 to 87); the region's history was given the same mix of purchase seconds and
  taps as the others, and the trees now name Grand Rapids in four of four runs.
- A $5 million bin on the pick's figure: region effects in the blended model, significant at 2 per cent on the record
  (deviance 10 on 3 degrees of freedom), move Muskegon and the North by 1.5 to 2.0 and the two-month lag by 2.7, so the
  standing family spans two $5 million bins; at the nearest $10 million it spans one, [35, 45), with the golden at 39.19.
- Grading every center's 2027 figure: at the nearest $10 million the first-alone route matches three of the four (Grand
  Rapids 20, the Lakeshore 20, Kalamazoo and Battle Creek 10) and the own-rate route matches the golden's Muskegon and the
  North figure (43.9, 40); only the pick's figure and the second center are graded.
- Each lien against its own posted rate, weighted by balance (a stack-aware rival): it names the Lakeshore at 22.9 against
  Muskegon and the North 22.0 and the record rejects it (deviance 49,297 against 48,893); left as an enumerated rival, its
  figure outside the bin either way.

- Every first-mortgage statement in the log quoting both liens (primary 1's first cut, at stage 3): every MTG row sat on
  a stacked mortgage, so noticing the MTG rows was the remedy (count each one at a booked loan's address, 32 of 32 with
  the outage workbook), a device whose discovery and remedy were one act; the credit union's other first mortgages,
  members' quotes on the first alone and closings whose first request named the first mortgage before the title search
  found the second lien now share the log, and only the amount tells which statements paid the second loan too (counting
  every MTG statement unreconciled keeps 9 of 32).
- The ALM report's clause on why the home equity book grew ("as members borrowed against their equity rather than
  refinance their first mortgages"), at stage 3: a narrative of the lock-in in the context artifact, pointing a reader at
  rung 2, and a claim about the record no check reproduced; cut to the book's size, count and rate.
- Creditor and title agency names near real firms (H21), at stage 3: Arcadia Home Loans (a mortgage lender once licensed
  from Grandville, Michigan), Cross River, Horizon First (First Horizon reversed), Meridian Trust (a federal credit union),
  Pinehurst Mortgage, Trillium Mortgage, Summit, Meridian National (a trade name of Meridian Title, which has offices in
  Indiana and Michigan) and Tallgrass Title (a Kansas agency); renamed Marlstone, Fernwick, Dunmere, Corraven, Vellacott,
  Eldermoor, Tollmere, Ashgrove National and Larchwick, each searched without a hit; no figure moved.
- A statement on a loan funded earlier in its month, at stage 3: the generator quoted the loan's exit balance, a balance it
  did not yet have, and one first-mortgage statement failed to tie; the desk now quotes the amount funded for a loan
  funded in the statement's month, and no statement predates its loan's funding.
- Portal round 1 on architecture 2 (2026-10-26): both responses landed the call, Muskegon and the North at about $40 million with the Lakeshore second, the golden; reading each stack's payoff off its blended first-plus-home-equity rate, chosen over the own-rate and first-only curves on fit and back-test, is a reflex for the portal's models, as stage 4's Opus reader showed, so architecture 2 is spent and the build re-roots off the enumerate-and-back-test chain.
- Architecture 3 candidate 1, a homeowners late-reported claim count by territory completed by occupancy (seasonal
  homes found at the next visit, a seasonal book grown since July 2025), probed 2026-10-26 (p166b): the Opus call-only
  probe found the seasonal-residence endorsement at once, built lag curves by that flag and the loss season on the
  developed 2021 to 2023 losses, used Bornhuetter-Ferguson for the young seasonal book and landed the territory and
  the runner-up (Lakes about 80, Ridge second); an occupancy lag read off an endorsement column is a move visible in
  the schema. Its pack also read as built (no policies written 2021 to 2024, every 2025-26 policy a seasonal home, no
  cancellations, one form).
- Architecture 3 candidate 2, the same count with the lag driver rebuilt from a record kept for billing (homes standing
  empty at the loss date: seasonal cottages, and primary homes whose owners winter away, seen only as winter mailing
  addresses; a June to November 2026 book transfer into Ridge with no winter on the books), probed 2026-10-26 (p166d):
  the Opus call-only probe matched every claim to the term, the endorsement and the mailing address in force at the
  loss date, built four occupancy states, ran Bornhuetter-Ferguson on policy-days by territory, state and month and
  landed Ridge at about 70 with Lakes second; an attribute of the frame's own units, however it is recorded, is joined
  at the event date and modelled. The pack also carried rows dated after the pull and transfer policies whose original
  inception equalled the transfer date.
- Architecture 3 candidate 3, homeowners claims first reported in 2027 by territory with an exiting carrier's book
  rolling into Ridge at its renewal dates through May 2027, listed in the transfer desk's roster, probed 2026-10-26
  (p166f): the Opus call-only probe counted every policy in force in 2027, carried the roster's offered and
  not-yet-mailed rows at the decided acceptance, modelled them on the 2022 transfer block's first-months curve and
  landed Ridge first and Metro second at about 2,350; a roster listing the incoming units is read as future book
  growth. It also noticed every term ran exactly 365 days.
- Architecture 3 candidate 4, the same 2027 count with no roster, the transfer's continuation left to the record's own
  arrival flow (1,600 a month into Ridge from September 2026) and the 2022 block's twelve-month cycle, probed
  2026-10-26 (p166g): the Opus call-only probe fitted claims by territory, month and months since transfer on the
  2022 block, inferred one renewal cycle from the source's definition and the analogue, projected 1,595 a month to
  August and landed Ridge at about 2,550 with Metro second; an arrival flow that jumps a territory's book by 8 per cent
  a month, with an analogue block beside it, is salient however unlisted. Pack tells: dates on days 1 to 28 only, a
  pile of 1979 inceptions.
- Architecture 3 candidate 5, a self-insured manufacturer's 2027 workers' compensation claims by the claimant's last
  plant, a laid-off forge cohort turning 62 and filing hearing-loss claims from the HR master's separated rows,
  probed 2026-10-26 (p166i): the Opus call-only probe sliced the hearing-loss claimants by status (613 of 730 former),
  fitted a hazard by age, department and length of service on former workers, found the 2014 forge layoff and its
  1965 births and landed Kessler at about 340 with Harlow second; a separated population in the frame's own file is
  read once the claimants are sliced by status. It ignored the noise survey, taking department and tenure as the
  exposure, and flagged the single-date layoff and the birth bunching.
- Architecture 3 candidate 6, first form (measured 2026-10-26, never probed): the 1988-90 forge cohort crossing 62
  with a realistic birth spread, the golden on cumulative dose from the noise survey. With births spread over 1962
  to 1972 the cohort's first crossers fall in 2023-26, so the back-test p166j ran (fit 2016-22, test 2023-26) showed
  the department-and-tenure hazard over-predicting Kessler's hearing-loss filings by 40 to 70 per cent, and a
  per-plant recalibration of that hazard lands the golden; the cohort's separation moved to a November 2026 forge
  closure and the filing hazard onto years since leaving.
- Architecture 3 candidate 6, a November 2026 forge closure whose 1988-90 hires worked almost entirely under the
  1991 enclosure, the filing hazard by years since leaving and dB-years from the noise survey, probed 2026-10-26
  (p166k): the Opus call-only probe split acute injury from hearing loss, put acute claims on the 30 November roster
  by plant and department (the forge empty, Ellery's 1,625 hires counted), fitted the closure group's propensity by
  plant, department and hire era, measured the cohort's own low claim rate beside the noise drop, rejected the flat
  layoff precedent and landed Ellery at about 260 with Harlow second; a cohort the action concentrates on is dug
  into through every related file, the noise survey included.
- Architecture 3 candidate 7, a self-insured manufacturer's 2027 carpal tunnel claims by plant, a mid-2026 line
  speed-up at Ellery hidden by the disorder's onset lag, the ergonomics file carrying each job's Strain Index inputs,
  probed 2026-10-26 (p166m, p166n): both Opus call-only probes scored the Strain Index from the assessment rows,
  fitted log rate = -6.76 + 1.54 ln(SI) across the 56 job areas, confirmed it on the one area already changed, applied
  the speed-up's doubling with an onset ramp and landed Ellery at about 290 to 300 with Harlow second; an exposure
  field the solver recognises is scored and calibrated across the units.
- Architecture 3 candidate 8, a new acute hospital's first-year critical care admissions under a practice-allocation
  model, two independent-sector hospitals beside the new site sending their deteriorating patients to the nearest NHS
  unit (Ravensholt General today) whatever the patient's practice, probed 2026-10-26 (p166o): the Opus call-only probe
  ran the practice model (543, back-tested at 505 against 511), tabulated transferring sites in the admissions file,
  found the two Hindmarsh sites' transfers taken at Ravensholt whatever the practice, reassigned them by site (55 in
  2025-26, trended to 52.5) and landed 600 (595.4), rejecting the literal model as missing the flow; an outside body
  carried in the model's own records is tabulated, however small its share.
- Architecture 3 candidate 9, a new secondary academy's first Year 7 intake under the council's place-planning
  model (its area's demand less the existing schools' admission numbers, 130), a neighbouring area's oversubscribed
  schools turning away about 55 applicants a year whom the coordinated scheme's clause 8.1 offers the nearest school
  with a place (until 2027 one in another authority, from 2027 the new academy, filling it to its 180), built
  2026-10-26 as probe9 and never probed: it has the anatomy of task137 v3's stage-4 SEND_BACK, a filed clause that
  decides membership and a cap that makes the body's size immaterial (every golden reading exactly 180), so the
  decisive step reads as data semantics and rule application to the judge and to any reader of the scheme.
- The outside-population family as a whole (candidates 5 to 9 here, task137 v3): the decisive step cannot satisfy
  the three rules. Filed for determinacy, the institutional fact makes the step a presence flip read off a document
  (Gate H data semantics, task137 stage 4); withheld, the golden rests on a hidden rule; left measurable in the data,
  the body is tabulated or calibrated and landed (candidates 5 to 8); and a body large enough to move the bin
  robustly makes its own size immaterial, while a small one leaves the call on the rounding edge.
