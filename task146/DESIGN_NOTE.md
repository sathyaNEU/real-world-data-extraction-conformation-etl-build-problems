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

Ends on: about 14,000 initial claims for the week ended 10 October 2026 (the exact value is measured on the built
pack at stage 3).
Golden: about 16,000 initial claims for the week ended 10 October 2026.

## Stump sentence

Carrying the step the first claims week of a quarter takes on average onto the level of the last four weeks calls
about 14,000 initial claims for the week ended 10 October 2026 (Ends on); the step that lands it there is treating the
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
  its 2023 revision, the notices portals (legacy and current), amended, withdrawn and multi-site notices, and the
  page-view dumps by UTC hour. Each is what these systems write; none decides the call (asserted at stage 3).
- **Layer 2:** `field_method`: an administrative calendar effect in an official weekly series is modelled as a
  regression effect with its driver rather than absorbed into the seasonal factor; the shortcut carries the
  quarter-start step as a seasonal share of the level (or a year-on-year ratio, a quarter-start term, or a step scaled
  on the closing quarter's claims), and the expert sizes it from the closing quarter's monetarily ineligible
  determinations at the rate past quarter turns show.
- **Decisive step:** the first claims week of the fourth quarter built as its seasonal baseline (the recent level
  carried through the week's usual movement) plus the claims filed again by claimants found monetarily ineligible in
  July to September, at the share of each closing quarter's ineligible determinations that past quarter turns sent
  back in their first claims week; this moves the week from about 14,000 to about 16,000.
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
  which rejects the seasonal-share step by a visible margin (the turns after the high-ineligibility quarters, the
  margin measured and asserted at stage 3).
- **Analyst test:** a strong analyst who reads every field, the technical notes and the program statistics correctly
  forecasts the week ended 10 October 2026 from seasonal factors for the first claims week of each quarter carried on
  the level of the last four weeks and calls about 14,000 (Ends on); the year-on-year ratio, a regression with a
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

Stage 2.

## Semantic fork table

Stage 2.

## Ladder

Stage 2.

## Closure table

Stage 2.

## Literal reader

Stage 2.

## Oracles

Stage 2.

## Ask sheet

Stage 2.

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
