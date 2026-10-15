# task146: Rothwell Bank's initial claims call for the week ended 10 October 2026 (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC17. The seed (a bank economics desk's nowcast of the
week's national unadjusted initial claims, published to clients before the official Thursday release) was read at its
header and Situation only. Its world, decision and quantity are kept. Its mechanism (an employer-filed block an
attention signal cannot see) is a hidden bulk filing and is not kept. The pitfall is re-found from how unemployment
insurance claims come to exist: a claim takes effect on the Sunday of the week it is filed, its base period is fixed
by the quarter of that Sunday, and a claimant refused for want of base-period earnings can be admitted once the
quarter turns.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task146.json`, architecture v1, registered 2026-10-15 after `git pull` (task145 at stage 3, task460 drawn); `guard.py check` WARN (repeat.gate_g, overuse.gate_g, answered below), no BLOCK; same-puzzle and same-driver matches against older builds (task134 v3, task54) differentiated on the card; `guard.py validate` clean |
| Domain / task type | `survey-research-official-statistics` (client domain), task type `seasonal-adjustment-official-time-series-production` (forecasting): the call is the next value of an official weekly series in a week that carries a calendar-administrative effect, which official time-series practice models as a regression effect with its own driver beside the seasonal component. The seed's home, `economics-econometrics` with forecasting, is banned against task145 (the pairing in the last three builds); the claims nowcast's deciding analysis is the official series' seasonal and calendar structure, which is this task type's work |
| Objective | Forecasting & Predictive Modeling: the national unadjusted initial claims of the claims week Sunday 4 to Saturday 10 October 2026, in progress at the decision (Thursday 8 October 2026, after the board's 08:30 release of the week ended 3 October) and first published on Thursday 15 October 2026 |
| Shape | `single-figure`: one committed count, the call's critical components, a chart and two ask tables supplying the criteria (the call and its components about 4, the chart's parts 5, the two ask tables about 30 figures, the files 2: about 40), arithmetic in the ask sheet |
| Decision | `quantity_figure`, answer unit `count` (the desk's call for the week, to the nearest thousand) |
| Mechanism | gap population (decisive: the claims that make the quarter-start step are filed by a population the closing quarter built, the claimants it refused for want of base-period earnings, not by this week's labour market) and time (the step comes in the first week whose Sunday opens the quarter); pattern none; generators G14 (the first week's step conditioned on the closing quarter's refused claims), G11 (the pool is the claims that failed the monetary eligibility test), G13 (the week the turn falls in); Gate G `forecasting`; strategy `composition_mix` (the step is carried as a pooled seasonal share while its size is set by the share of the closing quarter's claims found ineligible) |
| Layer 2 family / pattern | `field_method` (an administrative calendar effect in an official series modelled as a regression effect with its driver); `own:quarter-start-refiling-surge-driven-by-the-closing-quarter-ineligible-determinations` (nearest library line: survey-research-official-statistics/seasonal-adjustment-official-time-series-production/1, model the regression effects before the seasonal filter; this build's effect is not an outlier or a level shift but a recurring calendar step whose size has a measurable driver) |
| Furniture | forum `customer_or_counterparty` (the bank's clients receive the preview), forcing event `other` (the board's Thursday 08:30 release), organisation family `financial_institution` (a bank's economics desk), role family `research_desk`, context artifact `other` (the board's open-data extracts and technical notes; no stakeholder memo or model ships), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | the board's open-data initial claims by claims week, region, industry division of the last employer and claim type from January 2023 (constructed; rows set at stage 3), on an ask's path; the call reads the board's weekly series by region and the monthly program statistics |
| Deliverables | `ic_preview_2026-10-10.docx` (the one-page preview: the call and a chart of the weekly series with it), `ic_preview_2026-10-10.xlsx` (the call and the two ask tables) |
| People | drawn with `guard.py names --geo "New Zealand" --seed 146`: Stacey Baxter (senior economist, Rothwell Bank, writes the preview and asks for it), Tia Hewitt (economist on the desk, keeps the layoff-notice tracker and the desk's attention pages), Nicola Pedersen (the board's manager of labour market statistics, named as the contact in the technical notes), Timothy Laing (the board's employer services lead, signs the notices portal notice); none appears in the prompt |

**Guard.** `guard.py check` on the registered card: WARN `repeat.gate_g` (forecasting beside task145) and WARN
`overuse.gate_g` (5 of the last 12), no BLOCK. Answered: the objective is Forecasting and the honest mechanism for a
forecast the correctly read past does not pin is `forecasting`; task145's is a forward count re-routed at plan
exchange rates and shares nothing else on the card. The structural tests matched older builds on (population, G14,
quantity_figure) and (population, G14, forecasting): task134 v3 (a raised zoning allowance's rebuild yield) and task54
(a per-event loss over a re-sequenced plan), each differentiated on the card in one line.

**Same-puzzle and same-driver tests.** Gap population, decisive G14, decision `quantity_figure`, Gate G `forecasting`:
no build in the last twelve carries gap population with decisive G14 (task143's decisive is G17, task141's G9,
task142's G2, task144's G6). Older matches are task134 v3 and task54, differentiated.

**Abstraction test.** Stripped of nouns, the driver is: a step a weekly count takes each time a calendar period turns
is released by the turn from a pool the closing period built (units refused at their first attempt because their
qualifying record lagged), so its size is that pool times the rate past turns show, and when the closing period
refused far more units than usual every seasonal, year-on-year or level-driven forecast of the first week understates
it. The three nearest drivers (`guard.py`, 0.06 and under): task446 v2 (a screen's yield against a moving base rate),
task127 v1 lineage (a fixed team's finishes before a period closes), task123 v2 (reading intervals split onto calendar
months); none shares the latent structure. Read by mechanism rather than score: task134's lineage v2 (an inflow a pool
sends on a conversion hazard by time since entry) is the nearest: here there is no duration clock or hazard, the pool
is released all at once by a calendar turn, and its size is a count the closing quarter recorded. task102 (payments
due on a weekend released into the next fiscal year) moves a closed count across a period line; here the count is not
moved, it is generated by the pool. task89 (a stock's net movement differenced against a known inflow schedule) has a
filed inflow; here the inflow is inferred from past turns.

**Data-native sentence.** A claim takes effect on the Sunday of the week it is filed and its base period is fixed by
the quarter of that Sunday, so a claimant refused in July to September because their recent earnings sat in the
quarter just after the base period can be admitted from the first claims week whose Sunday falls in October: that
week's rise is the third quarter's refused claims coming back, and this year the third quarter refused more than
twice as many claims as a usual quarter.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: conditional survival (133), a hazard
by time since entry and a surge filling the pool (134 v2), an intervention's increment on own pace (136), a mixture of
unit kinds at repricing (137), a start state at the forecast date (138), a randomised intervention per assigned unit
(139), a dependent reservation (140), selective labels (141), a period total built from its generating units (142), a
correlated group effect (143), a seeded cascade (144), a nominal line re-applied at plan exchange rates (145); none
releases a pool into an official weekly series at a calendar turn. `layer2-rigor-patterns.md`: the seasonal-adjustment
line 1 (regression effects modelled before the seasonal filter) is the client's nearest line. `two-layer-task-design.md`:
"handling the data's real structure" is the client's family for the step. `exemplars.md` (Economics, labour market
seasonality): the depth of a calendar built from a labour series, not its withheld window. The seed's header and
Situation (FC17) for the world, decision and quantity only.

**World.** A fictional English-speaking country of about 9.1 million people in eight regions. Unemployment insurance
is run by the Unemployment Insurance Board. Claims weeks run Sunday to Saturday; a claim takes effect on the Sunday of
the week it is filed; its base period is the first four of the last five completed calendar quarters before the
quarter of that Sunday, and a claimant whose base-period earnings fall below the minimum is found monetarily
ineligible. Every Thursday at 08:30 the board publishes the advance count of initial claims for the claims week ended
the previous Saturday, nationally and by region, with the week before revised; on the fifth working day of each month
it publishes its program statistics for the month before (initial claims by type, monetary determinations, first
payments, weeks claimed, exhaustions, benefits paid). Rothwell Bank's economics desk sends its clients a short initial
claims preview each Thursday afternoon with its call for the following Thursday's figure. The as-of is Thursday 8
October 2026, after the release of the week ended 3 October and the September program statistics (published 7
October). Claims rose through the third quarter of 2026 as building contractors and hotels shed staff taken on in
2025 and early 2026, and the share of new claims found monetarily ineligible rose with them.

## Default path

1. Read the board's weekly initial claims by region in both claims-system layouts into one national series by claims
   week to the advance count of the week ended 3 October 2026.
2. Estimate a seasonal factor for each claims week of the year from 2022 to 2025 (each week's claims over its centred
   52-week mean, averaged across the four years), the weeks aligned on the first claims week of each quarter.
3. Seasonally adjust the last four weeks (claims weeks ended 12 September to 3 October 2026) and average them as the
   level.
4. Multiply the level by the factor of the first claims week of the fourth quarter.

Ends on: about 13,000 initial claims for the week ended 10 October 2026 (13,385 on the world prototype; the exact
value is measured on the built pack at stage 3).
Golden: about 16,000 initial claims for the week ended 10 October 2026 (15,785 on the world prototype).

## Stump sentence

Carrying the step the first claims week of a quarter takes on average onto the level of the last four weeks calls
about 13,000 initial claims for the week ended 10 October 2026 (Ends on); the step that lands it there is treating the
quarter-start rise as seasonal when it is claimants found monetarily ineligible in the third quarter filing again once
the fourth quarter moves their base period, and the third quarter's ineligible determinations, more than twice a
usual quarter's, put the week at about 16,000.

## Three rules

- **Task type:** survey-research-official-statistics, seasonal-adjustment-official-time-series-production (serves
  Forecasting): the national unadjusted initial claims of the first claims week of the fourth quarter, forecast as the
  official weekly series' seasonal baseline plus the quarter-start surge modelled as a regression effect with its own
  driver.
- **Domain test:** the deciding quantity is the surge an official weekly claims series takes in the first claims week
  of a quarter, which official time-series practice models as a regression effect with its own driver beside the
  seasonal component (here the closing quarter's monetarily ineligible determinations, which file again once the base
  period moves) rather than leaving it in the seasonal factor; the field's estimator is the seasonal baseline plus
  that effect, sized from past quarter turns.
- **Swap:** "how many hospital admissions will the first week of the quarter bring" keeps a weekly count and a quarter
  turn, but a base period that moves at the turn, a monetary determination and claimants refused at their first
  attempt who file again have no counterpart there, so what sizes the quarter-start step, and with it the call, stops
  making sense.
- **Layer 1:** the board's weekly series in two claims-system layouts (column names, date formats, weeks labelled by
  their Saturday in the legacy file and their Sunday in the current one, region codes against names); advance counts
  beside revised ones; the program statistics workbook organised by fiscal year (July to June) in two layouts, its
  months assigned by the claim week's Sunday, determinations in units beside benefits in thousands of dollars; public
  holidays moving claims between weeks; on the ask paths the industry division coded on the 2006 classification and
  its 2023 revision, the layoff notices in Employer Services' register before 1 June 2026 and on the Employer Portal
  after it, the portal's UTC timestamps, withdrawals kept in Employer Services' case notes, multi-site notices. Each is
  what these systems write; none decides the call (asserted at stage 3).
- **Layer 2:** `field_method`: an administrative calendar effect in an official weekly series is modelled as a
  regression effect with its driver rather than absorbed into the seasonal factor; the shortcut carries the
  quarter-start step as a seasonal share of the level (or a year-on-year ratio, a quarter-start term, or a step scaled
  on the closing quarter's claims), and the expert sizes it from the closing quarter's monetarily ineligible
  determinations at the rate past quarter turns show.
- **Decisive step:** the first claims week of the fourth quarter built as its seasonal baseline (the recent level
  carried through the week's usual movement) plus the claims filed again by claimants found monetarily ineligible in
  July to September, at the share of each closing quarter's ineligible determinations that past quarter turns sent
  back in their first claims week; this moves the week from about 13,000 to about 16,000.
- **Not semantics:** every field, code, unit and definition can be read correctly (the claims week, the effective
  date, new and additional claims, the monetary determination and its base period, the fiscal-year sheets, the
  advance count) and the default path reads them all correctly and still calls about 14,000; the week the surge
  lands in is shown by every past quarter turn in the counts themselves; nothing flips on what a field, code, unit or
  time zone means, only on how the quarter-start step is estimated.
- **Not rule application:** the shipped sentences that bear on how the figure is computed are the prompt's question
  (the national count the board will first publish for the claims week ended 10 October 2026) and the technical
  notes' definitions of a claims week, an initial claim, the effective date and the monetary determination with its
  base period; executed word for word on clean data they fix the target week and say who could be eligible when, but
  give no count and say nothing of anyone filing again, so no sentence or pair of sentences spells the method; the
  refiling and its rate per ineligible determination are left to be inferred from the history of past quarter turns,
  which rejects the seasonal-share step by a visible margin: on the world prototype the step fitted on the closing
  quarter's ineligible determinations misses past turns by 437 claims (leave-one-out root mean square, 50 turns)
  against 1,086 for a quarter-start term alone and 812 for a step scaled on the closing quarter's claims, and 245
  against 1,392 and 752 at the ten turns after the largest pools (re-measured and asserted on the pack at stage 3).
- **Analyst test:** a strong analyst who reads every field, the technical notes and the program statistics correctly
  forecasts the week ended 10 October 2026 from seasonal factors for the first claims week of each quarter carried on
  the level of the last four weeks and calls about 13,000 (Ends on); the year-on-year ratio, a regression with a
  quarter-start term and the level, and a quarter-start step scaled on the third quarter's claims all call 13,000 to
  14,000, and only the quarter-start step rebuilt as the third quarter's monetarily ineligible determinations times
  the share of them past quarter turns sent back in the first week calls about 16,000 (executed on the clean truth in
  `checks.py` at stage 3).
- **Estimand:** the prompt: the national number of initial claims the board will first publish for the claims week
  ended Saturday 10 October 2026, in its release of Thursday 15 October 2026; the technical notes (section 2) define
  the claims week (Sunday to Saturday), an initial claim (a new or additional claim taken in the claims week) and the
  advance count; every claim of that week is in the population, none of them filed when the desk calls it. The
  population, outcome, window and unit are filed; the estimator of the week's count is not.
- **No decoy:** no memo, briefing, earlier preview, consensus figure or stakeholder estimate states or argues a
  figure, a step or a method; the board's releases and statistics carry counts only; the desk's earlier previews are
  not shipped; the distractors (the labour force survey's regional unemployment rates and the online vacancy index)
  rank nothing.
- **No certified replay:** no certified or published forecast ships and nothing graded is reproduced; the refiling rate
  is not recovered by reproducing certified figures but estimated from the raw weekly counts and monthly
  determinations of past quarter turns.
- **Lesson:** a recurring step at a calendar turn in an official weekly series can be an administrative effect with a
  driver (here the closing quarter's refused claims, re-admitted when the base period moves) and must be modelled from
  that driver, not carried as a seasonal share of the level; no build on file teaches a calendar-released pool in an
  official series (task102 moves payments across a weekend year end, task134 converts a pool by time since entry,
  task123 calendarises reading intervals).

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear. Values
from the world prototype (`generator/ladder_proto.py`); re-measured on the pack at stage 3.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 seasonal factors for the first claims week of each quarter (2022 to 2025) on the level of the last four weeks (the default path) | no | no | yes: the textbook seasonal-factor forecast | no | no | yes: one factor times a level | readable |
| R1 last year's first claims week of the fourth quarter times the year-on-year growth of the last eight weeks | no | no | yes: the year-on-year reflex | no | no | yes: one ratio | readable |
| R2 the step from the week before, one intercept per quarter of the year (a quarter-start term) | no | no | yes: a calendar dummy | no | no | yes: one mean | readable |
| R3 the step scaled on the closing quarter's claims | no | no | yes: the obvious covariate | no | no | yes: one slope | readable |
| R4 (decisive) the step from the closing quarter's monetarily ineligible determinations at the rate past quarter turns show | no: no sentence names refiling, a quarter-start effect or its driver; the technical notes define the claims week, an initial claim, the effective date and the base period, and say nothing of anyone filing again | no: no column holds refiled claims or flags a quarter's first claims week; the determinations are one table of several in the board's monthly program statistics | no: seasonal factors, year-on-year, quarter dummies, level-driven steps and the search-interest regression all file 12,000 to 14,000 | no: no published forecast, certified figure or past call ships; the history's turns are raw counts | no: nothing in the files is wrong | no: the step is built against the week before at each of 50 past turns and regressed on a pool summed by quarter from a second file's monthly table, read across fiscal-year sheets in two layouts | silent |

## Semantic fork table

Draft at the pause; every row is asserted in `generator/checks.py` at stage 3 and re-read before precut.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "initial claims" | new and additional claims taken in the claims week, as the board counts them | new claims only; continued weeks | another quantity, not the series the board publishes | technical notes 2.2 (an initial claim) |
| SF2 | "the claims week ended Saturday 10 October 2026" | Sunday 4 to Saturday 10 October 2026 | the week containing 1 October | the week ended 3 October is published; same target week | technical notes 2.1 (the claims week); the prompt |
| SF3 | "first report" | the advance count in the release of Thursday 15 October 2026 | the count as revised a week later | same call (asserted: the revision is under 1 per cent and every construction keeps its bin) | the prompt; technical notes 3.1 (advance and revised counts) |
| SF4 | "nationally" | the eight regions together | one region | not the national figure | the release's national row |
| SF5 | the as-of | the release of 8 October (week ended 3 October, advance), the September program statistics of 7 October, the open-data extract of 7 October | the release of 15 October | not available at the as-of | each file's own date |
| SF6 | the months of the program statistics | claims-week months, each week in the month of its Sunday | calendar months | same call (the workbook's months are the board's; no calendar-month figures ship) | the workbook's notes |
| SF7 | history on advance or revised counts | either | the other | same call (asserted) | none needed |
| SF8 | the turns the rate is measured on | all 50 since 2014 | since 2019, since 2022, without 2020 and 2021, fourth-quarter turns only, without January turns | same call (asserted: ten constructions inside the 16,000 bin) | none needed |
| SF9 | the base week | the advance count of the week ended 3 October | the mean of the last three weeks; an interpolated base | same call (asserted) | none needed |
| SF10 | the rounding | the call to the nearest thousand from unrounded components, once | per component | asserted one arithmetic | the prompt's last sentence |
| SF11 | "how many" | the mean expected count | the median | same call (asserted) | the prompt |
| SF12 | holidays in the target week | none (Labour Day is 26 October) | n/a | same call | the public holidays file |
| SF13 | national against regional modelling | the national series | the eight regions modelled and summed | same call (to assert on the pack) | none needed |
| SF14 | the legacy and current layouts' junction | the legacy file to the week ended 26 June 2021, the current from the week beginning 27 June 2021, no gap or overlap | a duplicated or dropped week at the junction | same call (asserted) | the two files' own ranges |

## Ladder

Measured on the world prototype (`generator/ladder_proto.py`, world seed 1462028), the published view only: revised
counts to the week ended 26 September, the advance count of the week ended 3 October, monetary determinations by
claims-week month. Re-measured from the shipped files at stage 3.

| Rung | Construction | Call | Bin | Dies to |
|---|---|---|---|---|
| R0b | ISO-week seasonal factors on the level of the last four weeks | 12,383 | 12,000 | ISO week 41 is not the quarter's first claims week in years whose 1 October is a Sunday |
| R0 (default) | factors for the first claims week of each quarter, 2022 to 2025, on the level of the last four weeks | 13,385 | 13,000 | the first week's step varies with the closing quarter's ineligible determinations, not the level (R squared 0.258 for a quarter term against 0.881) |
| R1 | last year's first claims week of the fourth quarter times the last eight weeks' growth on the year | 13,171 | 13,000 | last year's step carried a third-quarter pool of about 16,000 determinations, this year's 43,608 |
| R2 | the step from the week before with one intercept per quarter of the year | 13,518 | 14,000 | as R0; clearance 0.02 on the prototype, re-centred at stage 3 |
| R3 | the step scaled on the closing quarter's claims | 13,751 | 14,000 | the third quarter's claims are 1.15 times a usual quarter's, its ineligible determinations 2.7 times (twin pairs below) |
| R4 | R2 in ratio form | 13,619 | 14,000 | as R2 |
| golden | the step on the closing quarter's monetarily ineligible determinations, all 50 turns, one intercept per quarter of the year, on the advance count of the week ended 3 October | 15,785 | 16,000 | (the golden) |

- **The golden's constructions** (ten): all turns 15,785; fourth-quarter turns only 15,916; the mean of the last three
  weeks as base 15,686; ratio form 15,886; without January turns 15,742; without 2020 and 2021 15,856; since 2019
  15,764; since 2022 15,695; advance counts throughout 15,657; Huber 15,777: spread 259, all in the 16,000 bin, the
  nearest 0.16 of a bin from an edge. An interpolated base (the week before and the fourth week) gives 16,293.
- **Rate evidence.** 0.0965 claims in the first claims week per monetarily ineligible determination of the closing
  quarter (the world's 0.0912), standard error 0.0063 over 50 turns; residual 421 claims. One sigma on the rate moves
  the call by 274: at 15,785 the low side is 15,511, inside the bin by 11 claims, so stage 3 re-centres the golden
  near 16,000 (the level or the rate) before the figures are cut, and asserts one sigma inside the bin.
- **Rejection margin.** Leave-one-out root mean square over the 50 turns: the pool-driven step 437, a quarter term alone
  1,086, the level-driven step 812; at the ten turns after the largest pools 245, 1,392 and 752.
- **Twin pairs.** The second-quarter turns of 2017 and 2019: closing-quarter claims 138,201 and 138,951 (0.5 per cent
  apart), ineligible determinations 12,657 and 27,197, steps 715 and 2,250. The third-quarter turns of 2023 and 2024:
  claims 141,219 and 145,500, determinations 10,562 and 27,613, steps 1,078 and 2,534.
- **Position and dominance.** The golden is the extreme cell; every correction from R0 to R4 walks up and stops at or
  below 14,000. The pool is 2.7 times a median quarter's while the quarter's claims are 1.15 times, so the pool-driven
  step is about 2.4 times what the level-driven step carries.
- **Bins.** Every rival two or more bins below the golden; the default path 2.4 bins.
- **Worth.** Graded: the call and its critical components (the third quarter's ineligible determinations, exact from
  the workbook; the claims expected to be filed again, about 4,000; the week's baseline, about 12,000), never an
  intermediate.

## Closure table

Draft at the pause; each row's assertion is written at stage 3.

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every initial claim the board takes in the claims week ended 10 October 2026, none filed at the as-of | filed (the prompt; technical notes 2.2); SF1 |
| 2 | Unit of account | initial claims (new and additional) | filed (2.2) |
| 3 | Attribution window | Sunday 4 to Saturday 10 October 2026 | filed (2.1); SF2 |
| 4 | As-of dating | the release of 8 October, the program statistics of 7 October, the extracts of 7 October | each file's date; SF5 |
| 5 | Version basis | the advance count is the target; history revised or advance | SF3, SF7 asserted |
| 6 | Denominator | none in the call; the rate is claims per ineligible determination | design; asserted convergent across constructions |
| 7 | Weighting | each past turn once | C1 across OLS and Huber (asserted) |
| 8 | Window length | the turns since 2014 | C1 across seven windows (SF8) |
| 9 | Boundary inclusivity | a week belongs to the quarter of its Sunday | filed (technical notes 2.1, the workbook's notes); no claims week straddles the target's edges |
| 10 | Rounding path | the call rounded once to the nearest thousand | the prompt; SF10 |
| 11 | Tie-break | none arises | the golden two or more bins from every rival |
| 12 | Maturity and censoring | the September determinations complete at 7 October (determined at filing); the week ended 3 October advance | the workbook's notes; asserted |
| 13 | Order of operations | the step estimated, then added to the base week | design; C1 with the interpolated base |
| 14 | Row order | none matters | C1, asserted over shuffled rows |
| 15 | Duplicate resolution | the junction week once | SF14 |
| 16 | Identity normalisation | regions by legacy code and by name | the region codes file |
| 17 | Netting against gross | gross initial claims | filed (2.2) |
| 18 | Dimensional units | claims and determinations are counts; benefits in thousands of dollars (unused) | the workbook's headers |
| 19 | Code and status semantics | new and additional claim types | technical notes 2.2; never the stump |
| 20 | Integerisation | none before the final rounding | design |
| 21 | Clause scope | the technical notes cover the weekly series and the program statistics | filed |
| 22 | Forward window contents | the week of 4 to 10 October: no holiday, the first claims week of the fourth quarter | the public holidays file; the calendar |

## Literal reader

Executing the prompt and the technical notes word for word fixes the target (the national initial claims first
published for the claims week Sunday 4 to Saturday 10 October 2026) and every term but the estimator of the week's
count; every reading converges on the golden's bin or violates a quoted line (SF1 to SF14), and the easy answer comes
from an easy estimator of the quarter-start step on the same literal target (a seasonal share of the level), never
from another reading. Re-run on the finished pack at stage 3.

## Oracles

- The board's weekly series: raw counts; the history's quarter turns are what any construction must explain; no
  forecast, seasonal factor or certified figure ships with it.
- The program statistics workbook: the monetary determinations the golden reads, one table of several (claims by
  type, first payments, weeks claimed, exhaustions, benefits paid); no table ties only under the golden.
- The search-interest index and the labour force survey's regional unemployment rates (distractors): rank nothing; the
  search-interest regression is a measured rival at stage 3.
- Nothing ties only under the golden: no published forecast, consensus or past call for the week ships.

## Ask sheet

Designed at the pause, not yet measured; stage 3 computes every stop, the cracker's and the mirror's values, and the
pair ceiling from the generated rubric. Both asks read files the call never opens.

**Ask A. Layoffs announced for the fourth quarter** (24 figures): for each region, the workers to be laid off under
layoff notices given to the board whose first layoff falls from 11 to 31 October, in November and in December 2026,
exact.
- H18 home: the forward layoffs behind the coming weeks' claims, a context table the desk's preview carries.
- Sources: the Employer Portal export of 7 October 2026 (notices from 1 June 2026, one row per notice site, timestamps
  in UTC), Employer Services' register of notices received by email before 1 June 2026 (one row per notice site,
  local dates, legacy region codes, a status column), Employer Services' case notes (June to October 2026), the region
  codes, the technical notes' time zone line.
- Primary device A1 (D8, a clock against a filed cutoff): the portal stores each first layoff date as the UTC stamp of
  local midnight (UTC+13 from 27 September), so a 1 November or 1 December first layoff reads as 31 October or 30
  November when the stamp's date is taken; every region carries notices first laying off on 1 November and 1 December.
- Second device A2 (D4, absence evidenced in a file no habitual join reaches): the portal export keeps a withdrawn
  notice as lodged; the withdrawal is only in Employer Services' case notes, the notice number typed by hand.
- Third device A3 (D4, a channel absent): notices received before 1 June 2026 with first layoffs in the window are only
  in the email register.
- Hazards: legacy region codes; case-note references typed several ways; multi-site notices (one row per site in both).

**Ask B. The industries behind the third quarter** (14 figures): for each industry group, the change in initial claims
from July to September 2025 to July to September 2026, in per cent to one decimal.
- H18 home: where the third quarter's claims came from, the preview's second table.
- Sources: the board's open-data initial claims by claims week, region, industry subdivision and claim type (the
  spine), the board's current industry code list, the Statistics Office's concordance between its 2006 and 2023
  classifications, the technical notes (claims weeks belong to the quarter of their Sunday).
- Primary device B1 (D7, codes reissued to other entities): the board codes industry on the 2023 classification from
  the claims week of 4 January 2026; several 2006 subdivision codes were reused in 2023 for subdivisions in other
  groups, so the third quarter of 2025 read through the current code list puts claims in the wrong groups while every
  total ties; no code goes unmatched.
- Second device B2 (D8, periods off month end): the extract labels each week by its Saturday; the quarter is the quarter
  of the week's Sunday, so the weeks ended 4 July and 3 October 2026 (and 5 July and 4 October 2025) change quarter
  under the label.
- Third device B3 (D5, a repair right for one population only): claims not yet coded at the extract (code 99) sit
  mostly in the latest weeks; allocating them across groups moves every 2026 figure.
- Hazards: claim types, regions.

**Criteria.** Call and components (about 4), the chart's parts (5), Ask A (24), Ask B (14), files (2): about 49.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A workers by region and month (24) | both registers stacked, case-note withdrawals applied, first layoff dates taken from the stamps' dates | every region's October, November and December off (measured at stage 3) | miss |
| B change by industry group (14) | the extract by its week label, the current code list on both years | every group off (measured at stage 3) | miss |

Mirror leakage: 10 per cent of ask weight (design estimate, measured at stage 3).
Pair ceiling: 30 (design estimate: the cracker about 48 with the call, components and the chart's form; the mirror
about 12; re-computed at stage 3 from the generated rubric).

## State at pause

Paused 2026-10-15 at stage 2 (design) for the author's priority reworks; nothing cut, no prompt yet.
- Done: the draw (card registered, `DRAWN` 3994282), the three rules, the default path and stump sentence, the world
  (`generator/world.py`, seed 1462028 in `generator/common.py`) and the ladder measured on its published view
  (`generator/ladder_proto.py`), the readability screen, drafts of the fork and closure tables, the literal reader,
  the oracles and the ask design.
- Resume at stage 2: (1) re-centre the golden near 16,000 so a one-sigma move in the rate stays inside the bin (raise
  the 2026 level knot or the first-week rate slightly) and re-run `ladder_proto.py` until every construction keeps
  0.15 of a bin and every rival stays two bins off; (2) build the ask worlds on paper (`notices.py`, `industry.py`) and
  measure each stop, the cracker and the mirror, then write the pair ceiling and mirror leakage from them; (3) write
  `prompt.txt` (question first, one paragraph, under 1,000 characters, `voice-check.py`) and run `precut.py task146`
  to exit 0; then stage 3 (pack, goldens, submission, gates) as `build-pipeline` sets out.
- Draft prompt: How many initial claims will the Unemployment Insurance Board first report for the claims week ended
  Saturday 10 October 2026? Put the call in ic_preview_2026-10-10.docx, a one-page preview that opens with it and charts
  the weekly national count from April 2026 with the call, and in ic_preview_2026-10-10.xlsx with two tables: for each
  region, the workers to be laid off under layoff notices given to the board whose first layoff falls from 11 to 31
  October, in November and in December 2026; and for each industry group, the change in initial claims from July to
  September 2025 to July to September 2026. Give the call to the nearest thousand, workers exactly and changes in per
  cent to one decimal.

## Tried and rejected

- The seed's mechanism (an employer-filed block of claims for idled workers that the attention signal cannot see,
  with a model-risk standard certifying the house method on 52 past nowcasts): a hidden bulk filing and a certified
  record built to bless the wrong method, both banned as the decisive step (10/10 rules 3, and the validated decoy).
- The seed's home domain (`economics-econometrics`, forecasting): banned against task145 (the pairing in the last three
  builds); the house alias `economics` would pass the guard by name only and was not used.
- Additive against multiplicative seasonality under a non-seasonal level rise (the seasonal swing fixed in claims while
  a shock lifts the level): rejected at the draw because the solvers' own defaults split both ways (statsmodels'
  `seasonal_decompose` and STL are additive, ratios and year-on-year growth multiplicative), so the stump would be a
  coin flip on a library default, not an analysis a capable analyst skips.
- An attention-signal nowcast fitted on pages chosen by in-sample correlation, validated out of sample: the client's
  own example, but `forecast_method_backtest` is task145's strategy (banned in the last three) and the decisive step
  would need a filed back-test organ two builds running.
- A Labor Day or Christmas holiday misalignment in 52-week ratios: rejected as a calendar reading (time semantics)
  that a capable analyst checks by reflex, and as task102's family.
- A benefit-year anniversary echo of last year's surge (claims filed again 52 weeks on): rejected as too near task134
  v2's driver (an inflow a pool sends a year after entry) and too small at realistic re-employment.
- The national figure at a US scale (about 220,000 a week) or at 40,000: prototyped on 2026-10-15; the golden's
  defensible variants (the estimation sample, the base week, the step's form) spread 2 to 3 per cent, wider than a
  thousand-claim bin; a country of about 9 million (about 12,000 claims a week, the first week about 16,000) keeps
  every variant inside one bin with the rivals two or more bins off (prototype, eight seeds).
- The world prototype's first settings (2026-10-15): a pandemic surge of 4.3 times and holiday weeks at 8.5 per cent a
  day lost biased the rate (0.070 against the world's 0.084) and spread the golden's constructions over 827 claims;
  the surge was softened to 2.35 times and the holiday effects to 3 per cent a day.
- High-ineligibility quarters placed mostly in the third quarter: they lifted the fourth-quarter intercept every rival
  carries and put the level-driven and ratio rivals in the 15,000 bin, one bin from the golden; spread across the year.
- The episodes of 2022 to 2026 as first set: the high pools all fed the April turns and the January turns with the
  largest calendar moves followed the low pools, so the post-2022 construction came out about 650 claims low in every
  world seed; rebalanced, and the January return and shutdown softened, after which it is noise around the others.
- An attention-signal ask (the seed's encyclopedia page views, or search-interest exports each scaled to its own peak):
  its index needs a filed construction a careful solver executes, and its UTC-hour and rename devices are found by
  the battery; the search-interest index ships as a distractor instead.
- An insured unemployment rate ask (continued weeks over covered employment): every device found (fortnightly
  certifications, provisional quarters, an office restructure) is adjudicated by the definition a careful solver
  executes, so none holds the cracker.
- A first-payments ask (payments reissued under fresh ids): the battery's claim-and-week dedupe repairs it.
- The industry classification as a full renumbering: a raw join then gives implausible changes that invite the check;
  kept as partial code reuse with every total tying.
