# task146: Rothwell Bank's initial claims call for the week ended 10 October 2026 (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC17. The seed (a bank economics desk's nowcast of the
week's national unadjusted initial claims, published to clients before the official Thursday release) was read at its
header and Situation only. Its world, decision and quantity are kept. Its mechanism (an employer-filed block an
attention signal cannot see) is a hidden bulk filing and is not kept. The pitfall is re-found from how unemployment
insurance claims come to exist: a claim takes effect on the Sunday of the week it is filed, its base period is fixed
by the quarter of that Sunday, a claimant refused for want of base-period earnings can be admitted once the quarter
turns, and how many of the refused come back is a property of the region's labour market and of how long ago they were
refused. Deepened at the stage 2 resume (2026-10-16): the refiling itself is inferable from the base-period definition,
so the decisive step became the refiling share's regional structure. Repaired the same day after the strict rule 3
audit (AT_RISK, data semantics): the refiling is filed in the technical notes as the board's own rule. Strengthened the
same day after the rule 3 re-audit (PASS) found the stump too weak (both top responses land regional sizing about half to
three quarters of the time): in this world a refused claimant's chance of filing again at the turn also falls steeply
with the weeks since the refusal, the third quarter's refusals in the three regions that come back fell late (55.3 per
cent in September), and the call turns on sizing the refiling region by region and month by month of refusal; regional
sizing on the quarter taken whole files two bins low (`## Build record`). Every measured figure below is the shipped
pack's, recomputed by `generator/checks.py` and `verify.py`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task146.json`, architecture v1, registered 2026-10-15, edited in place at the stage 2 resume (2026-10-16) for the deepened decisive step, at stage 3 (answer, spine rows, Layer 1 as built) and at the strengthening (answer, driver, stump, analyst and domain tests, Layer 2 pattern, the task134 differentiation); `guard.py heart` WARN (repeat.gate_g, overuse.gate_g, answered below), no BLOCK; nearest drivers 0.07 and under; same-puzzle and same-driver matches against older builds (task134 v3, task54) and the composition drivers (task95, task137, task448) differentiated on the card; `guard.py validate` clean |
| Domain / task type | `survey-research-official-statistics` (client domain), task type `seasonal-adjustment-official-time-series-production` (forecasting): the call is the next value of an official weekly series in a week that carries an administrative calendar effect, which official time-series practice models as a regression effect with its own driver beside the seasonal component, on the components where their effects differ and their mix moves, and with the driver measured at the grain the effect works on (here the month of the refusal). The seed's home, `economics-econometrics` with forecasting, is banned against task145 (the pairing in the last three builds) |
| Objective | Forecasting & Predictive Modeling: the national initial claims of the claims week Sunday 4 to Saturday 10 October 2026, in progress at the decision (Thursday 8 October 2026, after the board's 08:30 release of the week ended 3 October) and first published on Thursday 15 October 2026 |
| Shape | `single-figure`: one committed count, its critical components, a chart and two ask tables supplying the criteria (the call and its components 6, the chart's parts 5, Ask A 24, Ask B 14, the files 2, instructions about 3: about 54) |
| Decision | `quantity_figure`, answer unit `count` (the desk's call for the week, to the nearest thousand) |
| Mechanism | gap population (decisive: the claims that make the quarter-start step are filed by the claimants the closing quarter refused, in each region at that region's own shares by the month of the refusal) and time (the step comes in the first week whose Sunday opens the quarter, and the weeks from a refusal to that week set how many of the refused are still out of work); pattern none; generators G14 (the first week's yield conditioned on the region and the month of refusal), G6 (the refused pool's regional and monthly mix moved far from the usual), G11 (the pool is the claims that failed the monetary eligibility test), G13 (the week the turn falls in); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `field_method` (an administrative calendar effect in an official series modelled as a regression effect with its driver, on the components); `own:quarter-start-refiling-effect-sized-by-region-and-month-of-refusal-on-the-closing-quarter-ineligible-determinations` (nearest library line: survey-research-official-statistics/seasonal-adjustment-official-time-series-production/1, model the regression effects before the seasonal filter; this build's effect is a recurring calendar step with a measurable driver whose yield differs by component and by the driver's timing inside the closing quarter) |
| Furniture | forum `customer_or_counterparty` (the bank's clients receive the preview), forcing event `other` (the board's Thursday 08:30 release), organisation family `financial_institution` (a bank's economics desk), role family `research_desk`, context artifact `other` (the board's releases, statistics and technical notes; no stakeholder memo or model ships), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `ic_open_data_by_industry_2023-2026.csv`, the board's open-data cube of claims by claims week, region, industry division of the last employer and claim type from the claims week of 1 January 2023 (constructed, 189,903 rows), on Ask B's path; the call reads the board's weekly series by region and the monthly program statistics. The pack is 16 files in four formats (csv, json, pdf, xlsx) |
| Deliverables | `ic_preview_2026-10-10.docx` (the one-page preview: the call and a chart of the weekly series with it), `ic_preview_2026-10-10.xlsx` (the call and the two ask tables) |
| People | drawn with `guard.py names --geo "New Zealand" --seed 146`: Stacey Baxter (senior economist, Rothwell Bank, writes the preview), Tia Hewitt (economist on the desk, keeps the desk's files and data log), Nicola Pedersen (the board's manager of labour market statistics, the technical notes' author and contact), Timothy Laing (the board's employer services lead, the register's last save); Employer Services officers appear by initials only in their case notes and register; none appears in the prompt |

**Guard.** `guard.py heart` on the edited card at the strengthening: WARN `repeat.gate_g` (forecasting beside task145)
and WARN `overuse.gate_g` (5 of the last 12), no BLOCK; nearest drivers 0.07 (task446 v2) and under. Answered: the
objective is Forecasting and the honest mechanism for a forecast the correctly read past does not pin is
`forecasting`; task145's is a forward count re-routed at plan exchange rates and shares nothing else on the card. The
structural tests matched older builds on (population, G14, quantity_figure) and (population, G14, forecasting):
task134 v3 and task54, each differentiated on the card in one line. A scratch card carrying the recency driver, checked
as a new draw before the world was rebuilt, blocked only against this slot's own registration (test.own_lineage and
driver 0.61, the same build); its nearest other drivers were 0.06 (task1, task127 lineage) and 0.05 (task85, task123).

**Same-puzzle and same-driver tests.** Gap population, decisive G14, decision `quantity_figure`, Gate G `forecasting`:
no build in the last twelve carries gap population with decisive G14 (task143's decisive is G17, task141's G9,
task142's G2, task144's G6). Older matches are task134 v3 and task54, differentiated.

**Abstraction test.** Stripped of nouns, the driver is: a step a weekly count takes each time a calendar period turns is
released by the turn from a pool the closing period built (units refused at their first attempt because their
qualifying record lagged); the share of the pool that comes back differs several-fold between the pool's segments and,
within the segments that come back at all, falls steeply with the time from the refusal to the turn, steady within each
across past turns; when the closing period's refusals in the segments that come back most fell late in the period, the
segment pools taken whole at their average rates, the pool taken whole at the pooled rate and the seasonal forecast all
understate the step. The nearest drivers (`guard.py`, 0.07 and under): task446 v2 (a screen's yield against a moving
base rate), task123 v2 (a total split onto calendar periods by how fast it ran), task85 v2.5 (each unit's own
observation window), task133 v2 (units held only if still present at a takeover); none shares the latent structure.
Read by mechanism rather than score: the composition drivers are the nearest. task95's rate is a weighted average over
two latent classes rebuilt per unit by differencing two dated events across two registers; task137 splits a repricing's
share between two kinds of unit; task448 completes a register by a capture rate that differs by filing route. Here
nothing is latent per unit or completed: a calendar turn releases a closing quarter's refused claims all at once into one
week of an official series, and the step is a regression effect whose yield is measured region by region and month by
month at 50 past turns. task134's lineage v2 converted a pool continuously on a hazard by time since entry; here no
survival curve is fitted and nothing converts by age: the turn is a single release, and the month of the quarter a claim
was refused in enters as three monthly determinations the board publishes, each with its own share. The stage 2 resume
had rejected the month of refusal for nearness to that lineage and for three collinear monthly pools (`## Tried and
rejected`); at the strengthening the guard puts no driver nearer than 0.07, and the world's month-to-month swings and
timed layoff episodes separate the three months (F 219 to 529 a region against the quarter taken whole).

**Data-native sentence.** The board's rules let a claimant refused for want of base-period earnings file again once a
later quarter moves the base period, but how many do depends on the region and on how long before the turn they were
refused: in the tourism and building regions the refused are mostly short-tenure seasonal workers whose last season now
counts, and between two thirds and nine tenths of those refused in a quarter's last month come back in the first week,
while those refused in its first two months have mostly found other work and under one in five come back; elsewhere few
come back at any month; this year's third quarter refused about 1.4 times a usual quarter's number, 40 per cent of them
in the three regions where claimants come back, and 55 per cent of those three regions' refusals came in September,
against about a third in a quarter's last month at a usual turn.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: conditional survival (133), a hazard by
time since entry and a surge filling the pool (134 v2), an intervention's increment on own pace (136), a mixture of unit
kinds at repricing (137), a start state at the forecast date (138), a randomised intervention per assigned unit (139), a
dependent reservation (140), selective labels (141), a period total built from its generating units (142), a correlated
group effect (143), a seeded cascade (144), a nominal line re-applied at plan exchange rates (145); none releases a pool
into an official weekly series at a calendar turn. `layer2-rigor-patterns.md`: the seasonal-adjustment line 1
(regression effects modelled before the seasonal filter) is the client's nearest line. `two-layer-task-design.md`:
"handling the data's real structure" is the client's family for the step. `exemplars.md` (Economics, labour market
seasonality): the depth of a calendar built from a labour series, not its withheld window. The seed's header and
Situation (FC17) for the world, decision and quantity only.

**World.** A fictional English-speaking country of about 9.1 million people in eight regions. Unemployment insurance
is run by the Unemployment Insurance Board. Claims weeks run Sunday to Saturday; a claim takes effect on the Sunday of
the week it is filed; its base period is the first four of the last five completed calendar quarters before the
quarter of that Sunday, and a claimant whose base-period earnings fall below the minimum is found monetarily
ineligible. Every Thursday at 08:30 the board publishes the advance count of initial claims for the claims week ended
the previous Saturday, nationally and by region, with the week before revised; a month's program statistics (claims,
determinations, first payments, weeks claimed, benefits, by region) come out with the weekly release on the Thursday
after the month's last claims week ends, that week at its advance count. Rothwell Bank's economics desk sends its
clients a short initial claims preview each Thursday afternoon with its call for the following Thursday's figure. The
as-of is Thursday 8 October 2026, after the release of the week ended 3 October, which carried the September program
statistics. The desk holds Employer Services' notice register, portal export and case notes from an information
request answered on 7 October. Through 2025 and early 2026 building and tourism boomed in the Western, Coastal and
Island regions and their refused claimants were few; layoffs there come in lumps, as a season ends or a project
finishes, so their refusals move together from month to month and some quarters' fall late and others' early. In the
third quarter of 2026 their claims rose from June, their refusals stayed near the usual level in July and August, and in
September, as the winter season ended and building contractors and hotels shed staff taken on in the boom, more than
half of their new claims were found monetarily ineligible; elsewhere refusals stayed near their usual level. Employer
Services took layoff notices by email until 30 June 2026 and on the Employer Portal from 1 July 2026. The board's open-data cube of claims by industry was rebuilt for the 2023 industry
classification from the claims week of 4 January 2026.

## Default path

1. Read the board's weekly initial claims by region in both claims-system layouts into one series per region by claims
   week to the advance count of the week ended 3 October 2026 (11,814 nationally).
2. Sum each region's monetarily ineligible determinations of each calendar quarter from the program statistics
   (insufficient in the sheets to June 2021): the claimants technical notes 2.3 allow to file again once the base period
   has moved.
3. At each of the 50 first claims weeks of a quarter from April 2014 to July 2026, regress each region's change from the
   week before on that region's ineligible determinations in the quarter just closed, with one intercept per quarter of
   the year (Western about 0.33, Coastal and Island about 0.26, every other region under 0.1).
4. Add to each region's week ended 3 October its fourth-quarter intercept and its share of its July to September
   determinations, and sum the eight regions: about 3,500 claims filed again on about 11,350 for the rest of the week.

Ends on: about 15,000 initial claims for the week ended 10 October 2026 (14,849 on the built pack and on the clean
truth, asserted R3a; every region-aware timing-blind construction 13,767 to 15,807, a full bin or more off).
Golden: about 17,000 initial claims for the week ended 10 October 2026 (16,895 on the built pack, 0.40 of a bin from
the edge; the world's own expected advance count 17,045).

## Stump sentence

Sizing the claims filed again in the first claims week of the fourth quarter region by region, each region's third
quarter ineligible determinations taken whole at the share its own past quarter turns show, calls about 15,000 initial
claims for the week ended 10 October 2026 (Ends on); the step that lands it there is weighing every refusal of the
quarter alike, when past turns show that in Western, Coastal and Island between two thirds and nine tenths of those
refused in a quarter's last month file again in the first week against under one in five of those refused in its first
two months, and this quarter's refusals there came 55.3 per cent in September against about a third in a quarter's last
month at a usual turn, so the week is about 17,000; the national determinations at the national rate and the seasonal
step of past first claims weeks call about 13,000.

## Three rules

- **Task type:** survey-research-official-statistics, seasonal-adjustment-official-time-series-production (serves
  Forecasting): the national initial claims of the first claims week of the fourth quarter, forecast as the official
  weekly series' baseline movement plus the quarter-start refiling effect, a regression effect with its own driver,
  sized on the regional components with the driver read month by month.
- **Domain test:** the deciding quantity is how many of a closing quarter's refused claimants file again in the first
  claims week of the next quarter, an administrative effect that official time-series practice models as a regression
  effect with its own driver beside the seasonal component, on the components where their effects differ and their mix
  moves, and with the driver at the grain the effect works on: each region's monetarily ineligible determinations of
  each month of the closing quarter at that region's own shares, which fall from the quarter's last month to its first,
  measured on 50 past quarter turns.
- **Swap:** "how many hospital admissions will the first week of the quarter bring" keeps a weekly count, regions, months
  and a quarter turn, but a base period that moves at the turn, a monetary determination and refused claimants who file
  again once it moves, fewer the longer ago they were refused, have no counterpart there, so what sizes the quarter-start
  step, and with it the call, stops making sense.
- **Layer 1:** the board's weekly series in two claims-system layouts (upper-case against lower-case column names,
  day-first against ISO dates, region codes against names, both keyed by the claims week's Sunday); the latest week at
  its advance count beside revised counts and a first-reported column; the program statistics workbook organised by
  fiscal year (July to June) in two layouts (the legacy report blocks headed sufficient and insufficient, the current long
  table headed monetarily eligible and ineligible), its months assigned by the claims week's Sunday, September 2026
  provisional with its last week at the advance count, determinations in units beside benefits in thousands of dollars,
  a few claims withdrawn before they are determined; public holidays, the summer shutdown and the fiscal year's end
  moving claims between weeks; on the ask paths the layoff notices in Employer Services' register to 30 June 2026 and on
  the Employer Portal after it, the portal's UTC lodgement stamps, amended and withdrawn notices, typed register dates and
  employer names, case-note references typed in several forms, the open-data cube's rebuild for the 2023 classification,
  transitional claims beside initial claims; the desk's data log. Each is what these systems write; none moves the call
  (R2 asserted per item in `checks.py`: the day-first dates read month first fail in 2,976 of 3,128 legacy rows, the
  codes map one to one and the national series is the same under any mapping, first-reported history 16,883, the current
  layout's turns 17,045, holiday-touched turns dropped 17,045, January turns dropped 16,957, July turns dropped 16,724,
  September's last week at its revised count 16,898, every legacy month heading carries its year, the junction neither
  gaps nor overlaps).
- **Layer 2:** `field_method`: an administrative calendar effect in an official weekly series is modelled as a
  regression effect with its driver, on the components where the components' effects differ and their mix moves, with
  the driver at the grain the effect works on; the shortcut, once the filed refiling is read and the regions are
  separated, takes each region's closing quarter whole at its average share, and the expert reads the published months
  apart after the past turns show that the quarter whole fails in and out of sample and that the share falls from the
  quarter's last month to its first.
- **Decisive step:** the claims filed again in the first claims week of the fourth quarter sized region by region and
  month by month, each region's July, August and September monetarily ineligible determinations at the shares its own
  past quarter turns sent back from each month of a quarter; this moves the week from about 15,000 (each region's
  quarter taken whole) to about 17,000.
- **Not semantics:** the refiling is filed (technical notes 2.3: "A claimant found monetarily ineligible may file again
  in a later quarter, once the base period has moved."), so no reader misses it and no reading of a field, code, unit or
  definition decides the call; what no field, code, unit or definition says is how many come back, that the share differs
  by region, or that it depends on when within the quarter the claimant was refused (asserted: no shipped sentence that
  speaks of refusal or filing again names recency, timing or region); an analyst who reads every definition correctly and
  sizes the filed refiling region by region on the quarter taken whole calls about 15,000, two bins low.
- **Not rule application:** the strict rule 3 test, on every shipped sentence that bears on how the figure is computed:
  the prompt's question (the national count the board will first report for the claims week ended Saturday 10 October
  2026), the technical notes' 24 sentences on the claims week and its effective date, the month a week belongs to, an
  initial claim, the monetary determination and its base period, refiling once the base period has moved, the region of
  a claim, the advance and revised counts, a month's program statistics and the two claims systems (sections 2.1 to 2.4,
  3.1, 3.2 and 3.3), and the release's three sentences on the count. Executed word for word on the clean truth, together,
  they fix the target week, the series and who may file again when, and give no figure of their own: they carry no count,
  rate or share (their only figures are the $6,800 minimum, 08:30, dates and years), say nothing of how many file again,
  of a share by region or of a share by how long ago the claimant was refused, and name no seasonal factor or regression;
  the estimators they admit file 15,000 (the filed refiling region by region on the quarter whole), 13,000 (the filed
  refiling at the national rate, or the seasonal step) or 38,000 (every refused claimant filing again in the week), never
  17,000. The behaviour the decisive step turns on, each region's shares by month of refusal, is inferred from the 50 past
  quarter turns, and the data rejects the rival assumptions by visible margins: one slope on the quarter whole in each
  region at F 77.3 on 16 and 344 degrees of freedom (Western, Coastal and Island 219, 529 and 387 on 2 and 43; per region
  and turn 156 claims against 76), one month profile for every region at F 108.3 on 21 and 344; leave one turn out, the
  national step misses by 303 claims under the golden against 635 for the regions on the quarter whole, 758 for the
  national months, 880 for the national pool, 873 for one share in every region, 1,015 for the closing quarter's claims
  and 1,041 for a quarter-start term. Asserted in `checks.py` (the R3 strict block: the sentences ship word for word, the
  refiling once with no size, rate, share, timing or region, no method vocabulary, no sentence of refusal naming recency,
  timing or region, and executed they give no 17,000; and R3a, R3b on the clean truth and the pack).
- **Analyst test:** a strong analyst who reads every field, the technical notes (the refiling filed in 2.3) and the
  program statistics correctly, and sizes the refiling region by region, each region's third-quarter ineligible
  determinations taken whole at the share its own past quarter turns show, calls about 15,000 (Ends on: 14,849; every
  region-aware timing-blind construction 13,767 to 15,807); the national determinations at the national rate (13,340), the
  seasonal step, the year-on-year ratio, a quarter-start term and a step scaled on the third quarter's claims call 12,000
  to 14,000; only the step built region by region and month by month, each region's July, August and September
  determinations at the shares its own past turns sent back from each month of a quarter, calls about 17,000 (executed in
  `checks.py` on the clean truth and on the pack: 14,849 and 16,895 on both).
- **Estimand:** the prompt: the national number of initial claims the board will first report for the claims week
  ended Saturday 10 October 2026, in its release of Thursday 15 October 2026 (the release of 8 October names it); the
  technical notes define the claims week (Sunday to Saturday, section 2.1), an initial claim (a new or additional
  claim, 2.2) and the advance count (3.1); every claim of that week is in the population, none of them filed when the
  desk calls it. The population, outcome, window and unit are filed; the estimator of the week's count is not.
- **No decoy:** no memo, briefing, earlier preview, consensus figure or stakeholder estimate states or argues a figure,
  a step or a method; the board's releases and statistics carry counts only; the desk's earlier previews are not
  shipped; the distractors (the labour force survey's regional unemployment rates and the online job advertisements
  index) rank nothing.
- **No certified replay:** no certified or published forecast ships and nothing graded is reproduced; the refiling
  shares by region and month are not recovered by reproducing certified figures but estimated from the raw weekly counts
  and monthly determinations of past quarter turns.
- **Lesson:** a recurring step at a calendar turn in an official weekly series can be an administrative effect with a
  driver (here the closing quarter's refused claims, free to file again when the base period moves) whose yield differs
  by component and by the driver's timing inside the period (a refusal near the turn is still out of work at it, an early
  one has moved on), and must be modelled from that driver on the components at the grain the publisher already gives,
  not carried as a seasonal share of the level, as the aggregate pool at the aggregate rate, nor as each component's
  period total at its average rate; no build on file teaches a calendar-released pool in an official series weighed by
  when it was built (task102 moves payments across a weekend year end, task134 converts a pool by time since entry,
  task95 recovers a latent class weight).

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear. Values
measured on the shipped pack (`generator/calc.py`).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 seasonal factors for the first claims week of each quarter (2022 to 2025) on the level of the last four weeks | no | no | yes: the textbook seasonal-factor forecast | no | no | yes: one factor times a level | readable |
| R1 last year's first claims week of the fourth quarter times the year-on-year growth of the last eight weeks | no | no | yes: the year-on-year reflex | no | no | yes: one ratio | readable |
| R2 the step from the week before, one intercept per quarter of the year (a quarter-start term) | no | no | yes: a calendar dummy | no | no | yes: one mean | readable |
| R3 the step scaled on the closing quarter's claims | no | no | yes: the obvious covariate | no | no | yes: one slope | readable |
| R4 the step on the closing quarter's national ineligible determinations at the national rate | yes: technical notes 2.3 files the refiling, which sends every reader to the refused claims | no | yes: the national determinations are the obvious covariate | no | no | yes: one slope | readable |
| R5 (the default path) each region's step on its closing quarter's determinations taken whole | yes: 2.3 sends the reader to the refused claims | yes: every file is by region, the workbook's ineligible determinations by region and month | yes: the regions are the series' own dimension, the quarter the refiling's own period | no | no | yes: one slope a region | readable |
| R6 (decisive) each region's step on its closing quarter's three monthly determinations, each month at its own share | no: no sentence says how many refused claimants come back, that the share differs by region, or that it depends on when within the quarter they were refused | no: no column holds a share, a weight or a refiled claim; the months are the workbook's grain, summed by every quarterly route | no: once the refiling is filed the quarter is its natural unit; only the regional fits' misfit (R squared 0.55 to 0.76 in the three regions against 0.98 by month) and their out-of-sample record (leave-one-turn-out 635 against 303) show that a refusal's month matters, and a solver must go and look | no: no published forecast, certified figure or past call ships | no: nothing in the files is wrong | no: eight regressions of a step built against the week before at 50 turns on three monthly pools a region read from a second file's regional table across fiscal-year sheets in two layouts | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py` at stage 3.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "initial claims" | new and additional claims taken in the claims week, as the board counts them | new claims only; transitional claims added; continued weeks | another quantity, not the series the board publishes | technical notes 2.2 (an initial claim) |
| SF2 | "the claims week ended Saturday 10 October 2026" | Sunday 4 to Saturday 10 October 2026 | the week containing 1 October | the week ended 3 October is published; same target week | technical notes 2.1 (the claims week); the prompt |
| SF3 | "first report" | the advance count in the release of Thursday 15 October 2026 | the count as revised a week later | same call (asserted: national revisions at most about 1 per cent, the largest 1.03; the advance target files 16,951 and every construction keeps its bin) | the prompt; technical notes 3.1 (advance and revised counts) |
| SF4 | "nationally" | the eight regions together | one region | not the national figure | the prompt; the release's national row |
| SF5 | the as-of | the release of 8 October (week ended 3 October, advance) and the September program statistics it carried | the release of 15 October | not available at the as-of | each file's own date |
| SF6 | the months of the program statistics | claims-week months, each week in the month of its Sunday, so a quarter's three months are its weeks' | calendar months | same call (the workbook's months are the board's; no calendar-month figures ship; asserted C1, every region-month's new claims equal its weeks') | technical notes 2.1 and 3.2; the workbook's notes |
| SF7 | history on advance or revised counts | either | the other | same call (asserted: first-reported history 16,883) | none needed |
| SF8 | the turns the shares are measured on | all 50 since 2014 | since 2017, since 2019, the current system's, the last five or three years, without 2020 and 2021, fourth-quarter turns only, third and fourth only, without January turns, holiday-touched turns dropped | same call (asserted: every window inside the 17,000 bin, 16,865 to 17,075) | none needed |
| SF9 | the base week | the advance count of the week ended 3 October | the mean of the last three weeks | same call (asserted: 17,088) | none needed |
| SF10 | the rounding | the call to the nearest thousand from unrounded components, once | per region or per component | asserted one arithmetic | the prompt's last sentence |
| SF11 | "how many" | the mean expected count | the median | same call (asserted) | the prompt |
| SF12 | holidays in the target week | none (Labour Day is 26 October) | n/a | same call | the public holidays file |
| SF13 | the legacy and current layouts' junction | the legacy file to the week ended 26 June 2021, the current from the week beginning 27 June 2021, no gap or overlap | a duplicated or dropped week at the junction | same call (asserted) | the two files' own ranges |
| SF14 | the regions | the eight regions, legacy codes mapped to names through the regions file, the same boundaries throughout | codes read as other regions | same call once mapped (asserted: one code per name) | the regions file |
| SF15 | "charts the weekly national count from April 2026" | from the claims week of Sunday 5 April 2026 (ended 11 April) | from the week ended 4 April 2026 | the chart only, not the call | technical notes 2.1: the week ended 4 April begins on Sunday 29 March and belongs to March (asserted) |
| SF16 | the month terms' form | each month of the closing quarter its own share | the last month and the rest; the last month alone; the first month left out; one month profile for every region with each region's scale | same call (asserted: 16,895, 16,970, 16,954, 16,930) | none needed |
| SF17 | September 2026 in the workbook | provisional, its last week (ended 3 October) at the advance count | the week's revised determinations | same call (asserted: 16,898) | technical notes 3.2; the workbook's note "September 2026 is provisional." |

## Ladder

Measured on the shipped pack by `generator/calc.py` on the published view only: revised counts by region to the week
ended 26 September, the advance count of the week ended 3 October, monetarily ineligible determinations by region and
claims-week month. The same code on the clean truth gives the same rungs (R3a, R3b in `checks.py`).

| Rung | Construction | Call | Bin | Dies to |
|---|---|---|---|---|
| R0b | ISO-week seasonal factors on the level of the last four weeks | 12,340 | 12,000 | ISO week 41 is the fourth quarter's first claims week in 2024 and 2025 only (the second in 2022 and 2023) |
| R1 | last year's first claims week of the fourth quarter times the last eight weeks' growth on the year | 12,665 | 13,000 | last October's step (860) carried a third-quarter pool of 16,767 determinations, 14.5 per cent in Western, Coastal and Island and 28 per cent of theirs in September; this year's is 26,035 at 40.1 per cent, 55.3 of theirs in September |
| R2 | the step from the week before with one intercept per quarter of the year | 13,084 | 13,000 | the first week's step varies with the closing quarter's refused claims, not the calendar (leave-one-out 1,041 claims against 303) |
| R0 | factors for the first claims week of each quarter, 2022 to 2025, on the level of the last four weeks (the seasonal route) | 13,241 | 13,000 | as R2 |
| R3, R3r | the step scaled on the closing quarter's claims; the same region by region | 13,253; 13,562 | 13,000; 14,000 | the third quarter's claims are 1.11 times the median third quarter's (leave-one-out 1,015) |
| R2r, R2g | a quarter-start ratio; quarter-start terms region by region | 13,184; 13,084 | 13,000 | as R2 |
| R4 | the filed refiling sized on the national determinations at the national rate (all turns; sixteen variants and the one-share panel 13,171 to 13,916) | 13,340 | 13,000 | one share for every region is rejected by the regions' own steps (F 108.3 on 21 and 344 by month) and fails out of sample (leave-one-turn-out 880, the one-share panel 873); the national fit's R squared is 0.40 |
| R4m | the national determinations month by month (twelve variants 13,592 to 15,346) | 14,516 | 15,000 | region-blind: the national months mix the three regions' steep monthly shares with the rest's flat ones (leave-one-out 758) |
| L | latest-period rates: last October's step per refused claim, the last four turns', the last turn's | 13,149; 14,727; 16,097 | 13,000 to 16,000 | the boom quarters' refusals sat in the low-share regions; the July turn's step rode its own late refusals (0.60 of the three regions' in June) on a pool of another mix |
| V | the step on the closing quarter's change in the job advertisements index (a distractor, 29 turns) | 13,171 | 13,000 | the index does not drive the step |
| R5 (default) | the filed refiling region by region, each region's quarter taken whole at its share (all turns; 24 constructions 13,767 to 15,807) | 14,849 | 15,000 | the share falls steeply from a quarter's last month to its first (Western, Coastal and Island F 219, 529 and 387 on 2 and 43 against the quarter whole; R squared 0.76, 0.61 and 0.55 against 0.98 by month); out of sample 635 against 303; this quarter's refusals in the three regions sit 55.3 per cent in September against 32.4 at the median turn |
| golden | each region's step on its closing quarter's three monthly determinations, one intercept per quarter of the year, all 50 turns, on the advance count of the week ended 3 October | 16,895 | 17,000 | (the golden) |

- **Every construction of the golden** (24, asserted, each clear of 16,500 and 17,500 by more than one sigma): all turns
  16,895; fourth-quarter turns only 17,071 (one intercept 17,071); third and fourth 17,075; without 2020 and 2021 16,910;
  since 2019 16,949; since 2017 16,916; without January turns 16,957; the current system's turns 17,045; the last five
  years 17,051; the last three years 16,865; holiday-touched turns dropped 17,045; Huber 16,942; ratio form 16,844;
  log-ratio form 17,225; the mean of the last three weeks as base 17,088; the advance count as the target (current
  system) 16,951; each region with one intercept 17,047; the last month and the rest of the quarter 16,895; the last
  month alone 16,970; the last two months with the first left out 16,954; one month profile for every region with each
  region's own scale 16,930; the national step on the three regions' and the rest's months 16,899; one intercept per
  quarter of the year common to every region 17,067. Span 16,844 to 17,225;
  the nearest edge 275 claims away, 3.3 sigma. Without the July turns (the June fiscal year's end) 16,724. The national
  step on the 24 regional monthly determinations in one equation lands the bin too: 16,854, standard error 262 (3.1 times
  the golden's), out of sample 398. The middle month lumped with the last (one share for August and September) files
  16,504, four claims over the edge, and the data rejects it (F 96, 238 and 255 on 1 and 43 in the three regions; out of
  sample 403).
- **The multiplicative form** (each region's log ratio of the first week to the week before on its months over the base
  week) lands the same bin, 17,225, and predicts past turns worse (leave-one-out 369 against 303); it is a variant of the
  golden, not a rival.
- **Rate evidence.** The three regions' first-week shares by month of refusal (all turns): Western 0.011, 0.155 and
  0.696 for a quarter's first, middle and last month; Coastal -0.005, 0.147 and 0.852; Island 0.063, 0.085 and 0.823
  (standard errors 0.016 to 0.038); every other region's under 0.1 in every month. Under every construction with its
  months identified the last month stays between two thirds and nine tenths (0.678 to 0.880) and the first two under one
  in five (asserted); on the quarter taken whole the same regions show 0.33, 0.26 and 0.26. One sigma on the golden
  (slopes and fourth-quarter intercepts, delta method) is 83 claims: 16,812 to 16,979; the flip to 16,000 needs the
  estimate 395 claims lower (4.7 sigma), to 18,000 605 higher (7.3).
- **The components at the precision every construction shares** (asserted): the claims filed again 5,308 (5,243 to
  5,527 across constructions, one sigma 86) state as 5,000 to 6,000; the rest of the week 11,588 (11,503 to 11,803, one
  sigma 84) as 11,000 to 12,000; Western, Coastal and Island's part of the refiled claims 0.916 (0.901 to 0.929, one
  sigma 0.009) as about nine tenths.
- **The data rejects the quarter taken whole.** Leave one turn out, the national step misses by 303 claims under the
  golden, 314 for the last month and the rest, 342 for the last month alone, 635 under each region's quarter taken
  whole, 758 under the national months, 880 under the national pool at the national rate, 873 under one share for every
  region, 1,015 under the closing quarter's claims and 1,041 under a quarter-start term. Region by region and turn by
  turn, the quarter whole misses by 156 claims and one month profile for every region by 198, against 76 for each
  region's own months; F 77.3 on 16 and 344 (the quarter whole) and 108.3 on 21 and 344 (one profile). The three regions'
  last-month part of their quarter's refusals runs from 0.08 to 0.60 across the 50 turns (median 0.32), so the timing
  shows in the history, and this quarter's 0.553 is inside it.
- **Twin pairs.** Timing: the July 2026 and July 2019 turns, Western, Coastal and Island determinations 6,207 and 5,729
  (national 18,490 and 16,964), the last month's part 0.60 and 0.15, steps 3,042 and 836 (asserted). Regions: the
  October 2016 and October 2022 turns, national pools 17,681 and 17,518, the three regions' part 0.380 and 0.109, steps
  2,084 and 545 (asserted).
- **Position and dominance.** The golden is the extreme cell; every correction from R0 to R5 walks up and stops at or
  below 16,000: the timing-blind constructions reach 15,807 and the latest-period rate on the July turn alone 16,097,
  each a full bin below. The month weighting raises the claims filed again from the quarter-whole build's 3,498 to 5,308.
- **Bins.** The default path two bins below the golden (its nearest variant 1,088 claims below), the national rate and
  the seasonal route four.
- **Worth.** Graded: the call and its critical components (the third quarter's ineligible determinations, 26,035 exact
  from the workbook, 40.1 per cent of them in the three regions and 55.3 per cent of those three regions' in September;
  the month shares in words; the claims filed again, 5,000 to 6,000, about nine tenths of them in Western, Coastal and
  Island; the rest of the week, 11,000 to 12,000), never an intermediate.

## Closure table

Each row's assertion is written in `checks.py` at stage 3.

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every initial claim the board takes in the claims week ended 10 October 2026, none filed at the as-of | filed (the prompt; technical notes 2.2); SF1 |
| 2 | Unit of account | initial claims (new and additional) | filed (2.2) |
| 3 | Attribution window | Sunday 4 to Saturday 10 October 2026 | filed (2.1); SF2 |
| 4 | As-of dating | the release of 8 October and the September program statistics published with it | each file's date; SF5, SF17 |
| 5 | Version basis | the advance count is the target; history revised or advance | SF3, SF7 asserted |
| 6 | Denominator | none in the call; each share is a region's claims filed again per ineligible determination of a month of the closing quarter | design; asserted convergent across constructions |
| 7 | Weighting | each past turn once per region | C1 across OLS and Huber (asserted) |
| 8 | Window length | the turns since 2014 | C1 across eleven windows (SF8) |
| 9 | Boundary inclusivity | a week belongs to the month, so the quarter, of its Sunday | filed (technical notes 2.1 and 3.2); no claims week straddles the target's edges; SF6 |
| 10 | Rounding path | the call rounded once to the nearest thousand | the prompt; SF10 |
| 11 | Tie-break | none arises | the golden a bin or more from every rival |
| 12 | Maturity and censoring | the September determinations complete at 8 October (determined when the claim is taken), the month's last week at its advance count | technical notes 2.3 and 3.2; SF17 asserted |
| 13 | Order of operations | each region's step estimated on its three months, then added to its base week, then summed | not a convention: the components and the months are the decisive step, forced by the data (F 77.3 against the quarter whole, 108.3 against one profile; leave-one-turn-out 303 against 635 and 880); the national step fitted on the 24 regional months at once lands the same bin (16,854, standard error 262) |
| 14 | Row order | none matters | C1, asserted: the weekly files and the program statistics' rows read in reverse give the same call |
| 15 | Duplicate resolution | the junction week once | SF13 |
| 16 | Identity normalisation | regions by legacy code and by name | the regions file; SF14 |
| 17 | Netting against gross | gross initial claims | filed (2.2) |
| 18 | Dimensional units | claims and determinations are counts; benefits in thousands of dollars (unused) | the workbook's headers |
| 19 | Code and status semantics | new and additional claim types; the advance and revised status | technical notes 2.2 and 3.1; never the stump |
| 20 | Integerisation | none before the final rounding | design |
| 21 | Clause scope | the technical notes cover the weekly series, the program statistics and the open-data cube | filed |
| 22 | Forward window contents | the week of 4 to 10 October: no holiday, the first claims week of the fourth quarter | the public holidays file; the calendar |

## Literal reader

Executing the prompt and the technical notes word for word fixes the target (the national initial claims first reported
for the claims week Sunday 4 to Saturday 10 October 2026) and every term but the estimator of the week's count; every
reading converges on the golden's bin or violates a quoted line (SF1 to SF17), and the easy answers come from easy
estimators on the same literal target (the filed refiling region by region on the quarter taken whole, the national
refused pool at the national rate, or a seasonal share of the level), never from another reading. Re-run on the
finished pack: the 24 technical-notes sentences (the filed refiling among them), the release's three and the prompt's
question ship word for word and carry no count, rate or share, and no sentence that speaks of refusal or filing again
names recency, timing or region; every SF row is asserted (SF1 to SF17 in `checks.py`), and the literal estimators file
15,000, 13,000 or 38,000, never the golden's 17,000.

## Oracles

- The board's weekly series by region: raw counts; the history's quarter turns are what any construction must explain;
  no forecast, seasonal factor or certified figure ships with it.
- The program statistics workbook: the monthly monetary determinations the golden reads, one regional table among
  several (claims by type, determinations, first payments, weeks claimed by region); no table ties only under the golden.
- The labour force survey's regional unemployment rates and the online job advertisements index (distractors): rank
  nothing; the step on the job advertisements index files 13,171 (rung V), and the survey's July to September quarter
  is not out until November. Each deleted leaves the call and both asks unchanged (asserted).
- The desk's data log: where each file came from and when; it states no figure, method or device (asserted).
- Nothing ties only under the golden: no published forecast, consensus or past call for the week ships.

## Ask sheet

**Main call's declared row population:** the board's two weekly series files and its release of 8 October, the program
statistics workbook, the technical notes, the regions file and the public holidays file. Device and hazard rows in it:
0 (asserted: the call opens no notices file and no cube file; computed from the two weekly files, the program
statistics and the regions file alone it is the golden; the asks computed with every main-call file but the technical
notes and the regions file removed are the asks).
Neither ask is keyed to the call, its construction or its figures; they share no primary device.

**Ask A. Layoffs notified for the fourth quarter** (24 figures): for each region, the workers to be laid off under
layoff notices given to the board whose first layoff falls from 11 to 31 October, in November and in December 2026,
exact.
- H18 home: the forward layoffs behind the coming weeks' claims, a context table the desk's preview carries beside the
  call; a measure every region carries that the call does not turn on. Use: the workbook's first table, in the desk's
  words ("workers to be laid off under notices").
- Construction: every layoff notice given to the board (Employer Services' register to 30 June 2026, the Employer Portal
  from 1 July 2026), each notice once, an amended notice in place of the one it replaces, withdrawn notices out, each
  site's workers in the region of the site, the period by the notice's first layoff.
- Primary device A1 (D7, the true key elsewhere): the portal's first release takes each notice's header from the
  business register and prints it on every site line of its notices report, so the report's region column is the
  employer's registered region; the site's region comes from its town through the regions file. National employers
  give most of the notices that cross regions, and every region carries, in every period, sites of an employer
  registered elsewhere (asserted).
- Second device A2 (D1, the same records under two key schemes): Employer Services re-keyed the register's open notices
  onto the portal under new portal numbers, those with first layoffs before October in the go-live weeks and the later
  ones in batches from mid-September as their dates came near; no field links the two copies, which match on business
  number, first layoff and sites; stacking both channels counts the re-keyed notices twice, the portal alone misses the
  ones not yet re-keyed.
- Third device A3 (D4, absence evidenced in a file no habitual join reaches): the portal has no withdrawal function, so
  a withdrawal is only in Employer Services' case notes, the notice number typed by hand in several forms; two notes
  record a withdrawal under consideration that never came.
- Hazards: HA1 legacy region codes in the register; HA2 register dates typed by hand, some as day-first text; HA3
  reduced-hours notices beside layoff notices; HA4 amended notices (superseded, with the replacing notice named); HA5
  the portal's lodgement stamps in UTC.
- Stops (computed from the shipped rows and asserted; the nearest moved cell to the golden): S1 the portal's region,
  24 of 24 cells off, nearest 12 workers; S2 both channels stacked, 10 cells off, nearest 14; S3 the portal alone, 8
  cells off, nearest 20; S4 withdrawals ignored, 12 cells off, nearest 10; S5 the cracker (S1 and S2), 24 of 24 off,
  nearest 8; S6 the over-clean (every portal notice of an employer with an open register notice dropped), 20 cells off,
  nearest 11; HA3 reduced-hours notices kept, 12 cells; HA4 superseded notices kept, 4 cells. The golden equals the
  truth table in all 24 cells; 77 register notices re-keyed, 34 withdrawal references in the case notes.
- Span: the portal export, the register workbook, the case notes, the regions file and the technical notes (5 files);
  notice number, lodged, business number, employer, region, type, first layoff, site town, workers, status, replaces;
  ES reference, town, region code, workers, first layoff, type, status; reference, note.
- Realism: a portal's first release pre-fills the notice header from the business register, a migration re-keys open
  cases as they come due, and withdrawals by email land in case notes.

**Ask B. The industries behind the third quarter** (14 figures): for each industry group, the change in initial claims
from July to September 2025 to July to September 2026, in per cent to one decimal.
- H18 home: where the third quarter's claims came from, the preview's second table; a measure every group carries that
  the call does not turn on. Use: the workbook's second table.
- Construction: the cube's new and additional claims (transitional claims are not initial claims), each claims week in
  the quarter of its Sunday, the weeks before the rebuild mapped from their 2006 division codes through the
  concordance to the 2023 divisions and the board's groups.
- Primary device B1 (D7, codes reissued to other entities): the 2023 classification re-blocked the division codes and
  gave thirteen 2006 numbers to divisions of other groups, so reading the 2025 weeks through the current code list
  misassigns them while every total ties and no code goes unmatched; the switch shows only in the fifteen codes the
  revision created, which first appear in the claims week of 4 January 2026, read against the concordance. Every group
  gives or receives a reissued code (asserted).
- Second device B2 (D2, a label stored before a silent switch): the rebuild also changed the cube's week label, from the
  claims week's last day (a Saturday) to its first (the Sunday); no sentence says so, and the weekdays change at the
  rebuild; reading every label as a week's end (the open-data convention) drops the first week of July 2026, reading
  every label as a start shifts the 2025 quarter a week early.
- Hazards: HB1 transitional claims in the cube (technical notes 2.2); HB2 the quarter of the Sunday against a label's
  own month (technical notes 2.1); HB3 the two 2006 divisions feeding one 2023 division (accommodation, education).
- Stops (computed from the cube as shipped and asserted; the nearest moved group to the golden): S1 the current list
  on both years, 14 of 14 groups off, nearest 5.0 points; S2 every label read as a Saturday, 14 off, nearest 7.9; S3
  every label read as a Sunday, 14 off, nearest 0.4; S4 transitional claims kept, 11 off, nearest 0.1; S5 the cracker
  (S1 with labels read as Saturdays), 14 off, nearest 3.1; S6 S1 with labels read as Sundays, 14 off, nearest 5.6.
  Every golden figure sits 0.281 of a bin or more from its rounding edge (asserted at 0.23: the smallest group's change
  moves about half a bin a claim); the golden equals the truth in all 14 groups. The cube's latest week is at its
  advance count, as the release's.
- Span: the cube, the board's industry code list, the Statistics Office's concordance and the technical notes (4
  files); week, region, division, claim type, claims; code, title, group; 2006 code, 2023 code, correspondence.
- Realism: a statistical cube rebuilt for a new classification keeps its history as published, and a rebuild changes a
  label convention along with the codes.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 legacy region codes | the register's own coding | Ask A, register rows | none when mapped |
| HA2 typed dates | clerks keying email notices | Ask A, register rows | a day-first date misread moves a notice's period |
| HA3 reduced-hours notices | the notice form's two types | Ask A | 12 cells up when kept |
| HA4 amended notices | the portal's amendment by replacement | Ask A | 4 cells when the superseded notice is kept |
| HA5 UTC stamps | the portal's database | Ask A, the channel split by date | none when converted |
| HB1 transitional claims | the cube's claim types | Ask B | 11 groups when kept |
| HB2 the label's month | the cube's labels | Ask B | every group under the label month and the Saturday reading |
| HB3 two sources into one division | the concordance's merges | Ask B | none at the group grain |

**Referee.** For Ask A the regions file's towns give each site's region and the register's business numbers give each
re-keyed notice's twin; for Ask B the concordance gives each 2006 code's 2023 division, and the weekdays of the labels
give the rebuild. Each is a source the golden reads, not a control: no file ties only under the golden, and no filed
sentence says what the portal's region column holds, that open notices were re-keyed, or when the cube was rebuilt
(asserted).

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A workers by region and period (24) | both channels stacked, case-note withdrawals applied, amendments and types handled, the portal's region column | every cell off, nearest 8 workers | miss |
| B change by industry group (14) | transitional claims out, the quarter of the Sunday with every label read as a week's end, the current code list on both years | every group off, nearest 3.1 points | miss |
| the preview's chart | the cracker's weekly series drawn as the golden draws it | its call point carries the cracker's call only when the call lands | outside |

Mirror leakage: 9 per cent of the ask weight. The mirror is the most attractive wrong rung, R5 (the filed refiling
region by region on each region's quarter taken whole, 15,000); it runs the same ask paths as the cracker, so it misses
every Ask A and Ask B figure and keeps only the chart's form (four of its five parts).
Pair ceiling: 35 (the cracker about 49 with the call, its components, the instructions and the chart; the mirror about
21 with the instructions, the chart's form and the components it shares: the third quarter's determinations with their
three-region part and the rest of the week without the refiling; it misses the call, the month shares and the
refiling's size). With the
cracker also cracking the most obvious device (A3, the case-note withdrawals) it keeps no further figure, since A1 holds
every Ask A cell: 35. With both top responses on the call: about 49.

## Build record

**Stage 2 resumed 2026-10-16** (this session): the golden re-centred on 16,000 through the late-2026 level (one sigma
86 claims inside the bin); the decisive step deepened from the refiling to its regional structure under the strict
reading of rule 3; the ask worlds built and measured (`generator/notices.py`, `generator/industry.py`); the prompt
written; `precut.py` next, then stage 3.

**Stage 3, 2026-10-16** (resumed after a container restart from the stage 2 result: `precut.py` re-run exit 0 with 49
checks; stash, `git pull --rebase origin main` up to date, pop).
- Generator: `world.py` gains the advance split of new and additional claims and the latest week's advance
  determinations on their own streams (no earlier draw moved); `records.py` the file names and every shipped table,
  the desk's data log among them; `docs.py` the technical notes and the release (PDF), the program statistics, the
  register and the concordance (xlsx) and the job advertisements (JSON); `calc.py` the ladder from the shipped files
  and, through the same code, from the clean truth, and both asks from their rows (`ladder_proto.py` folded in and
  removed); `deliver.py` the goldens and `figures.json`; `checks.py` 150 assertions; `verify.py` independent (csv,
  openpyxl, numpy least squares, its own Ask A matching and Ask B mapping); `metadata.py`; `build.py`. `industry.py`
  puts the cube's latest week at its advance count; `notices.py` fixes case-note wording (no truth moved).
- Pack: 16 files in four formats, the cube 189,848 rows, two distractors (the survey's regional unemployment and the
  job advertisements index), the desk's data log as the provenance record.
- Gates: checks 150, 0 failed; verify agrees (call 15,993, one sigma 86, refiled 4,609, the rest 11,384, the default
  13,415, the national rate 14,670, Ask A's 24 cells, Ask B's 14 groups); two builds byte-identical (target, golden,
  metadata.json, figures.json, target.zip); `figures_check.py` 65 figures, 0 absent; the realism sweep in `checks.py`;
  `golden-realism` (the chart's palette validated, annotations in ink, a finding as its title; the workbook's notes
  sheet, frozen headers and print titles); `reduce-house-fixes` (H1 audit clean on target and golden; H9 the data log
  names every other file, asserted; H3 the preview's sentences asserted against the figures); `leak.py` REVIEW,
  answered below; `guard.py surface` exit 0 (task134 and task54 promoted on the card signature, the draw's
  differentiated matches, for the author's clone-check); `guard.py heart` WARN (repeat.gate_g, overuse.gate_g,
  answered at the draw; nearest driver 0.07); `guard.py validate` 186 cards, 0 invalid; `precut.py` exit 0 on this note.
- Deliverables: `ic_preview_2026-10-10.docx` (one page, the call in the opening line, one chart of the weekly series
  from the week ended 11 April with the call marked), `ic_preview_2026-10-10.xlsx` (the call with its workings, the
  notified layoffs by region and period, the industry changes, a notes sheet).

**Rule 3 repair, 2026-10-16**, after the strict rule 3 audit (AT_RISK on data semantics) and the determinism judge's
APPROVE on the pre-repair cut (22f06ed9, Gate H analytical).
- The audit: technical notes 2.1 and 2.3 let a strong analyst read the refiling off the definitions, and quarter-change
  refiling is standard knowledge in the field, so the 13,000 leg, where most misses fell, was a semantics miss; the
  analytical leg was one bin (the national rate 14,670) behind a clean-looking national fit (R squared 0.82,
  leave-one-out 414 against 400); two region-aware variants cleared 15,500 by 71 and 105 claims; the eight-pool equation
  gave 15,306.
- Filed: technical notes 2.3 now says "A claimant found monetarily ineligible may file again in a later quarter, once
  the base period has moved." It gives no size, rate, timing or region.
- World rebuilt (`world.py`): the first-week shares widened (Western 0.265, Coastal 0.295, Island 0.318; the other five
  0.016 to 0.058). The three tourism and building regions' refusals now move together quarter by quarter (a common
  factor, standard deviation 0.55, on its own stream), so their part of the pool runs from 0.09 to 0.61 across the turns
  and pooling shows in the history. The third quarter of 2026's refusals rise in those three regions only (monthly rates
  0.32 to 0.51) and stay near their usual level elsewhere (0.13 to 0.19): a pool of 30,182, 48.5 per cent of it in the
  three regions.
- Measured on the pack (asserted): the golden 16,038 (one sigma 77); the 22 region-aware constructions run 15,720 to
  16,296, each clear of both edges by more than one sigma (the nearest edge 204 claims away, 2.6 sigma), the last three
  years 16,169; the national rate 13,727 (14,000), every variant 13,556 to 14,158; the seasonal route 13,273; the
  eight-pool equation 15,781 (inside the bin, standard error 351); leave one turn out 374 against 583 (national pool),
  591 (one share), 823 and 914; panel F 189.8.
- The judge's points: SF15 for the chart's start (asserted); the leave-one-out separation is now 583 against 374
  (was 414 against 400); the last three years sit 331 claims from 16,500. Write-up step 6 states the SIC 2006 to 2023
  and label cutover, which the pack still leaves to the data (Ask B's device). Components 3 and 4 stay ranges. The case
  notes and employer names are de-templated with no figure moved: legal names come from the business register on their
  own stream, the email register carries the clerk's shorter typing, and the case notes use officer voices from their own
  text stream. Ask A's 24 cells are identical.
- Ask B re-measured on the rebuilt world (its cube follows the world's claims): 14 changes, clearance 0.244; the stops
  hold in kind. Ask A unchanged.
- Gates: checks 163, 0 failed; verify agrees; two builds byte-identical; `figures_check.py` 65 of 65; `precut.py`,
  `voice-check`, `leak.py`, `guard.py surface` and `heart` re-run (results in the commit and `pipeline.json`).

**Strengthening, 2026-10-16**, after stage 4 on the repaired cut (a040f6c1): the judge DETERMINISTIC / APPROVE (one
residual fork, a multiplicative region build at 16,719); the rule 3 re-audit PASS but the stump too weak (both top
responses land regional sizing about half to three quarters of the time); the leak reader clean, noting repeated
withdrawal phrases in the case notes.
- The second layer: a refused claimant's chance of filing again at the turn falls with the weeks from the refusal to
  the quarter's last week (each refusal weighs exp(-d / 2.5) by its weeks d, averaging one over a quarter), so those
  refused in a quarter's last month come back several times as often as those refused in its first. The world gives the
  history the timing variation that identifies it: each region's refused share moves month to month (standard deviation
  0.28, the three tourism and building regions together 0.50 on a stream of their own), and twelve of the regional
  layoff episodes fall late or early in their quarter. The claims filed again and their determinations moved to streams
  of their own, so the base claims no longer move with the refiling. The third quarter of 2026 in the three regions:
  refusals near the usual level in July and August (about 0.14 and 0.19 of new claims) and more than half in September
  (0.545 to 0.56). The three regions' first-week shares at an even spread of refusals over a quarter rose by 8 per cent
  (Western 0.286, Coastal 0.319, Island 0.343).
- Searched and chosen (scratch harness, clean truth): the decay (2.5 and 3 weeks against 4), the month swings, the
  timed episodes, the September profile and the realisation of the month swings' two streams (forty draws; `MONTH_DRAW`
  "s24" is the one where every construction of the golden, the two-group month equation and the 24-month equation
  agree within 310 claims and the timing-blind constructions sit 1,050 claims or more below). The late-claim share's
  range moved from 0.0025-0.0095 to 0.0023-0.0095 so the week ended 3 October's advance count is not a round 11,800 and
  Ask B's nearest change sits 0.281 of a bin from its edge.
- Measured on the pack (asserted): the golden 16,895 (one sigma 83, 0.40 of a bin from the edge; 24 constructions 16,844
  to 17,225, the nearest edge 275 claims away, 3.3 sigma; the 24-month equation 16,854); the multiplicative form lands the
  bin (17,225, leave-one-out 369 against 303); the default path, each region's quarter whole, 14,849 (24 constructions
  13,767 to 15,807, the nearest 1,088 claims below); the national rate 13,340; the national months 14,516; the seasonal
  route 13,241; leave one turn out 303 against 635 (the quarter whole), 758, 880, 873, 1,015 and 1,041; F 77.3 on 16 and
  344 against the quarter whole and 108.3 on 21 and 344 against one month profile; the timing twin July 2026 against July
  2019 (last-month part 0.60 and 0.15 on pools within 8 per cent, steps 3,042 and 836).
- Records: the stump sentence, the analyst test (now the region-aware timing-blind route), the Three rules lines, the
  ladder, the fork table (SF16 the month terms' form, SF17 September's provisional last week), the card (answer, driver,
  stump, analyst and domain tests, Layer 2 pattern, the task134 line), the ledger row and the submission rewritten; the
  preview and the workbook carry 17,000, the September part and the month shares in words; the workbook's note on the
  refiled claims' regional part now matches the preview (about nine tenths). The checks now assert that no shipped
  sentence that speaks of refusal or filing again names recency, timing or region.
- Case notes: the withdrawal reasons are drawn with their own particulars (the month, the year, the plant, the number
  of staff on reduced hours), so no reason phrase repeats verbatim across notices; Ask A's 24 cells are unchanged.
- Gates: checks 179, 0 failed; verify agrees (call 16,895, one sigma 83, refiled 5,308, the rest 11,588, the timing-blind
  route 14,849, the seasonal default 13,241, the national rate 13,340, Ask A's 24 cells, Ask B's 14 groups); two builds
  byte-identical; `figures_check.py` 69 figures, 0 absent; `precut.py` 49 checks, 0 FAIL, 0 WARN, with `voice-check`;
  `leak.py` REVIEW, answered below; the producer-metadata audit clean on target and golden; `guard.py validate` 186 cards,
  0 invalid; `surface` exit 0 (task134 and task54 promoted on the card signature, as before); `heart` WARN
  (repeat.gate_g, overuse.gate_g, answered at the draw; nearest driver 0.07).

**Case-note coherence fix, 2026-10-16**, after stage 4 on the strengthened cut (f0b43f3f): the judge DETERMINISTIC /
APPROVE with Gate H analytical (the call reproduced at 16,895, all 24 Ask A cells and all 14 Ask B changes); the third
rule 3 audit PASS, strong (0.5 to 0.9 landers expected in the top two; eleven further constructions all land 17,000);
the leak reader clean, Q6 analytical, never surfacing the recency layer, with the desk's data log reading tidy.
- Fixed: CN051136, dated 10 July, gave "busy again since the start of October" as a withdrawal reason; two information
  sessions were dated before the notes that booked them (CN051364, CN051376). Every date a case note names is now drawn
  from the note's own date: a month given as past ("since ...") is before it, a session, briefing, expo or visit falls 3
  to 23 days after it, a deferral or extension names a month after it, and a first layoff already past is spoken of in
  the past. Asserted: no case note refers to a month or day after its own date as already past, speaks of a day before
  it as still ahead, or carries a date stamp other than its own (forward references to a first layoff or a deferral are
  the notice's own future). The assertion flags all three notes of the earlier cut.
- Varied: the officers' wording, so no sentence template (contacts, towns, numbers, months and the bracketed reason set
  aside) recurs more than twice (152 templates in 177 notes; asserted); each officer writes withdrawals six to eight
  ways and every other kind of note three to five, used in turn before any repeats, on a wording stream of their own. The
  notes' ids, dates, officers and typed references are unchanged, every withdrawal is still read as one by both
  detectors, and Ask A's 24 cells are asserted identical to the strengthened cut's. "Work and Income" (a real agency's
  name) became the board's regional employment office.
- The desk's data log reads as a working log: terse notes, the keeper's initials and times, an entry left bare.
- Gates: checks 183, 0 failed; verify agrees (call 16,895); two builds byte-identical; `freeze.py check --mode
  determinism` PASS (the main call, the stump and every graded figure unchanged; the goldens and figures.json
  untouched); `figures_check.py` 69 of 69; `precut.py` 49 checks, 0 FAIL, 0 WARN; `leak.py` REVIEW, the same lines as
  answered below; the producer-metadata audit clean on target and golden; `guard.py validate` 187 cards, 0 invalid,
  `surface` exit 0, `heart` WARN as before.

**Case-note realism pass, 2026-10-16**, after the targeted re-read of cut a502ea69 (no leak, Q6 analytical; realism
tells in the two changed files). Nothing graded moved (`freeze.py --mode determinism` PASS, nothing allowed).
- Each note now carries its own particulars: the employer's name, the site town, the contact, the time, the counts and,
  for a withdrawal, a reason drawn for the employer's industry with its own counterparty, place and month (a consent
  granted on a past date, a client renewed to a named year, a buyer by name). Reason families and each officer's
  phrasings are spread across the log, least used first, so no cause or form clusters. Asserted: no clause of six words
  or more appears in more than one note, every note is distinct, and no template recurs more than twice or twice for
  the same officer.
- The rule-restating filler is gone: the notes record the call or the job done ("Rang re notice period, went through it
  with the operations manager", "sent the amendment form", "4 left on VR at Pikes Landing per the operations manager")
  and never tell a reader what counts, what stands or what an amendment needs (asserted). The facts the asks rest on
  stay: the 34 withdrawals, the two withdrawals under consideration, the possible reductions with no amendment lodged,
  the first layoff dates.
- Every withdrawal note says the whole notice is withdrawn in the officer's own words ("in full", "outright", "for both
  sites", "across all 4 sites") and any count it gives is the notice's own total; asserted for all 34, and CN051234 now
  reads "withdrawal email from owner: ... Whole notice, all 20 staying."
- The officers' workload is uneven (JW 55, CH 35, RB 32, SB 30, DL 15, TL 10; asserted three to one or more), drawn on a
  stream of its own so the log's ids, dates and typed references are unchanged; Ask A's 24 cells asserted identical.
- The desk's data log is plainer: time stamps only where the desk kept one, the job-advertisements entry untagged.
- Gates: checks 187, 0 failed; verify agrees; two builds byte-identical; `figures_check.py` 69 of 69; `precut.py` 49, 0
  FAIL, 0 WARN; `leak.py` REVIEW, the same eight lines as answered below; the producer-metadata audit clean on target and
  golden; `guard.py validate` 187 cards, 0 invalid, `surface` exit 0, `heart` WARN as before.

**Ship, 2026-10-16**, on the realism pass's cut (commit 0a888d3, target.zip sha256 e5e9d268b7bd6c16; the final rebuild
cut it again byte for byte). The final targeted re-read of that cut was clean: no leak, nothing ranks or states a
figure, Q6 an analytical choice.
- The judge: `determinism_check_report.md` is the third round's verdict, on the strengthened cut f0b43f3f:
  DETERMINISTIC / APPROVE, Gate H analytical, the call reproduced at 16,895 (bootstrap 16,656 to 17,137 on the revised
  basis), all 24 Ask A cells and all 14 Ask B changes. The first two rounds, on the designs before the strengthening
  (22f06ed9 and a040f6c1, the call then 16,000), are kept as history in `determinism_check_report_round1.md` and
  `determinism_check_report_round2.md`. The two cuts after f0b43f3f (a502ea69 and e5e9d268) changed only the case notes
  and the desk's data log: no graded figure moved, `freeze.py check --mode determinism` passed with nothing allowed at
  each, and 14 of the 16 pack files are byte-identical to the judged pack.
- The rule 3 audits, three, each an isolated strict read:
  - `rule3/task146.md` (f71f5a0, cut 22f06ed9): AT_RISK on data semantics, the refiling read off the base-period
    definition carrying most of the stump's power. Fixed by the rule 3 repair: the refiling filed in technical notes
    2.3 with no size, timing or region, and the decisive step moved to its regional sizing.
  - `rule3/task146_r2.md` (67e305d, cut a040f6c1): PASS, but the stump too weak (both top responses land regional
    sizing about half to three quarters of the time). Strengthened: the month of the refusal.
  - `rule3/task146_r3.md` (0f4de4d, cut f0b43f3f): PASS and strong (0.1 to 0.25 of a strong field landing 17,000,
    0.5 to 0.9 landers expected in the top two; eleven constructions outside the asserted 24 all land 17,000).
- Accepted risks:
  - The judge's stump-power note, a partial landing route: applying July 2026's refiling ratio (the turn after June's
    refusal spike, a step of 3,042) to September's 5,767 refusals in Western, Coastal and Island gives about 4,900
    claims filed again and about 17,000 (16,800 to 17,000) without the region-by-month build. The judge rates the stump
    moderate and expects partial failures rather than a wall. Accepted as it stands.
  - The case notes' remaining regularity (a reason on most withdrawals, the whole-notice wording varied by officer,
    regular routine entries, the reference spellings), from the final re-read: accepted as a residual realism risk; no
    count turns on it.
- The leak readers' rounds and rulings are in `leak_check_report.md` (`## Solver's-eye read`) and in `## Leak review`.

## Leak review

`leak.py --asof 2026-10-08` on the strengthened build: REVIEW, no LEAK. Each line is harmless:
- Sweep 3, "2.3" in the technical notes: the section number of the monetary determination, matching Ask B's 2.3 for
  administrative and support services by coincidence of digits.
- Sweep 3, the call's words in the technical notes and the release: the field's own vocabulary (board, report, initial
  claims, nationally, claims week); no figure of the call.
- Sweep 4, stump terms in the technical notes (9 of 25: quarter, effect, determinations, period, technical, advance) and
  the release (5 of 25: technical, advance, regions, seasonal, statistics): the claims-week, base-period and publication
  definitions, the filed refiling rule of 2.3 (the WHAT, filed on purpose by the rule 3 repair) and "Counts are not
  seasonally adjusted."; neither document says how many refused claimants come back, that the share differs by region,
  or that it depends on when within the quarter they were refused (asserted R3 strict: no sentence that speaks of refusal
  or filing again names recency, timing or region).
- Sweep 9, dates after 8 October: the notices' first layoffs (portal and register) and the holiday list, forward by
  nature.

The last `leak.py` run, on the shipped cut, gives the same eight lines, no LEAK. The isolated readers, five rounds
(`leak_check_report.md`): rounds 1 to 3 on the stage 3, repaired and strengthened cuts each found no decisive-step
sentence, no file ranking the candidates or stating an asked figure, no helping file and no answer-shaped figure, with
Q6 an analytical choice, and round 3 never surfaced the month of the refusal; the two targeted re-reads of the case
notes and the desk's data log found no leak, and the first one's realism tells were fixed in the realism pass. Rulings
on the final re-read's points:
- The VR notes and the "amendment form emailed" notes do not change any count: technical notes section 5 counts a
  change only through an amended notice, and the judge reproduced all 24 Ask A cells on that reading.
- The chart's question for past weeks (revised or first reported) is ungraded and low risk.
- The technical notes' completeness is the board's own methodology document, so it is not steering.
- The remaining regularity in the case notes is accepted as a residual realism risk (`## Build record`, Ship).

## Gates at ship

- Generator checks: 187 passed, 0 failed, among them the R3 strict block (the HOW-bearing sentences ship word for word
  and executed give no 17,000), R3a and R3b (the analyst test on the clean truth and the pack: 14,849 and 16,895 on
  both), every fork row SF1 to SF17, the rivals and the margins by which the data rejects them, Ask A's 24 cells held
  identical across the cuts, and the case notes' realism and coherence checks.
- `verify.py` agrees on its own code path (the call 16,895, 17,000; one sigma 83; claims filed again 5,308, the rest
  11,588; the timing-blind route 14,849, the seasonal default 13,241, the national rate 13,340; Ask A's 24 cells and Ask
  B's 14 groups; the goldens agree).
- Each build run compares two builds byte for byte; the final rebuild cut the shipped target.zip again (sha256
  e5e9d268b7bd6c16).
- `figures_check.py`: 69 figures, none absent. precut: 49 checks, 0 FAIL, 0 WARN, with voice-check (the prompt
  unchanged).
- The container audit is clean (target and golden). `guard.py validate`: 187 cards, 0 invalid.
- `leak.py`: REVIEW, the eight lines answered above, no LEAK.
- `guard.py heart`: WARN (repeat.gate_g, overuse.gate_g, answered at the draw). `guard.py surface`: exit 0, task134 and
  task54 promoted on the card signature for the author's `/clone-check`.
- `freeze.py check --mode determinism`: PASS with nothing allowed (the main call, the stump and every graded figure
  unchanged through the case-note cuts).

## Pre-ship check

The 10/10 rules re-read against the built pack:
- **The domain:** the call turns on how many of the third quarter's refused claimants file again in the first claims
  week of the fourth quarter, the administrative calendar effect an official statistics unit models as a regression
  effect with its own driver: each region's monetarily ineligible determinations month by month, at that region's own
  shares by month of refusal. Swapping in hospital admissions leaves no base period, no monetary determination and no
  refused claimant to come back.
- **Two layers:** every mess item is the board's, Employer Services' or the desk's own and asserted neutral for the
  call (the two claims-system layouts, the advance count beside revised counts, the fiscal-year workbook in two layouts
  with September provisional, the holiday and shutdown weeks; on the ask paths the register and the portal, UTC stamps,
  amended and withdrawn notices, typed references, the cube's 2023 rebuild). The decisive step is analytical:
  - the easy routes, executed on the clean truth with every filed rule applied, file 14,849 (each region's quarter
    taken whole), 13,340 (the national rate) and 13,241 (the seasonal step);
  - changing only the decisive step, each month of the closing quarter at its own share region by region, files
    16,895;
  - nothing in the pack is planted to be caught, and no file, column or sentence gives a share by region or by month of
    refusal.
- **Rule 3, read literally:** technical notes 2.1 to 2.4 and 3.1 to 3.3, the release's three sentences on the count and
  the prompt's question, executed word for word, fix the week, the series and who may file again when, and give no
  figure; the estimators they admit file 15,000, 13,000 or 38,000, never 17,000. The three isolated audits: AT_RISK
  (fixed), PASS (strengthened), PASS and strong.
- **Determinism:** the fresh judge on the strengthened cut reproduced the call, all 24 Ask A cells and all 14 Ask B
  changes, Gate H analytical; the two later cuts moved no graded figure.
- **Robustness:** one sigma is 83 claims and the golden sits 0.40 of a bin from the edge; the 24 asserted constructions
  run 16,844 to 17,225 (the nearest edge 275 claims away, 3.3 sigma); every fork row is closed by a filed sentence or
  keeps the call, asserted.
- **Accepted risks:** the judge's partial landing route (July 2026's refiling ratio on September's refusals, about
  17,000) and the case notes' residual regularity (`## Build record`, Ship).
- **The asks:** unchanged since the strengthening; the readers' ask readings are the asks' bases, closed by filed
  sentences, or their devices.

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
  the battery; dropped.
- An insured unemployment rate ask (continued weeks over covered employment): every device found (fortnightly
  certifications, provisional quarters, an office restructure) is adjudicated by the definition a careful solver
  executes, so none holds the cracker.
- A first-payments ask (payments reissued under fresh ids): the battery's claim-and-week dedupe repairs it.
- The industry classification as a full renumbering: a raw join then gives implausible changes that invite the check;
  kept as partial code reuse with every total tying.
- The refiling at one national rate as the decisive step (the design paused on 2026-10-15): under the strict reading of
  rule 3 the base-period definition, read against the quarter turn, lets a careful reader infer that refused claimants
  can file again, and once inferred the natural sizing (the national determinations at the rate past turns show) is the
  golden, so the decisive step leaned on reading a definition; deepened so the share differs by region and the national
  rate on the national pool files a bin low (2026-10-16).
- A refiling share by the month of refusal (claimants refused late in the quarter come back more): a duration-dependent
  pool too near task134 v2's hazard by time since entry, and three monthly pools too collinear to separate three shares
  from 50 turns.
- A refiling share by the reason for monetary ineligibility: which reasons a base-period move cures can be read off the
  reasons' definitions, the same semantics lean one level down.
- A quarter-end separation bump in every quarter's last claims week (tried so that no-intercept rates miss): it gave the
  October turn a negative step of its own that crude ratios ignore, which carried a crude last-four-turns rate onto the
  golden; replaced by the fiscal year's end in June alone and a summer shutdown spanning the first January week.
- The 2025 boom quarters at the usual regional mix: the last four turns' national rate then sat near the golden; in
  this world the boom regions refused few claimants through 2025 and early 2026, and the latest-period rates read low.
- The national refiling at a steeper level only (re-centring the golden by the rate): the national-pool rival rose with
  it; the golden was re-centred through the late-2026 level, which moves every construction alike.
- Ask A's first-layoff dates stored as UTC stamps of local midnight (the device drafted at the pause): the hygiene
  battery executes UTC conversions (measured in-house), so it would not hold the cracker; the portal's lodgement stamps
  stay in UTC as texture.
- Ask B's week labels against the quarter-of-the-Sunday rule as a device: a filed rule adjudicates it; kept only as the
  cube's label switch at its rebuild, which no sentence states.
- The portal going live on 1 June 2026: the register then held few notices with first layoffs in October to December,
  so the re-keying touched three cells; moved to 1 July 2026, the fiscal year's start.
- Random coverage of the regions' cross-region sites: two cells carried only in-region employers in one draw, so the
  cracker hit them; every region and period now carries a site of an employer registered elsewhere by construction.
- The legacy weekly file's weeks labelled by their Saturday (the drawn Layer 1 item): read at face value for the
  quarter, the label moves the 29 legacy turns a week early and the call from 15,994 to 12,491 on the world, so a mess
  item could flip the call; both claims-system layouts key the week by its Sunday, and the Saturday-to-Sunday switch
  stays only in the cube, as Ask B's ledgered device (2026-10-16).
- The refiled claims and the rest of the week stated to the nearest 500 (4,500 and 11,500): the ratio form puts the
  refiling at 4,889 and the mean of three weeks as base puts the rest at 11,784, so no rounding is shared by every
  construction; stated as 4,000 to 5,000 and 11,000 to 12,000, which every construction and a one-sigma move keep.
- The regional first-week shares stated in whole per cent (about 2 in the Capital, 21 to 27 in Western, Coastal and
  Island): one sigma moves the Capital's 2.1 across 1.3 to 2.9; stated in words (one in five, one in four, fewer than
  one in ten), which every construction and a one-sigma move keep.
- The program statistics published on the fifth working day (7 October), before the weekly release of the month's last
  claims week: the month would make that week public before its advance count; published with the Thursday release,
  the last week at its advance count.
- A bank desk holding Employer Services' register and case notes with no record of how: the desk's data log records
  them as released on its information request, beside where every other file came from.
- "Most of the rise" for construction and accommodation in the preview: they rose 15,963 against a total rise of
  12,604; the sentence now says more than the whole rise, nine of the other twelve groups lower (asserted).
- base-period refiling left to the definitions: data semantics, per the rule 3 audit
- The three tourism and building regions' refusals moving independently of one another (the stage 3 world): their part
  of the pool hardly varied across turns (standard deviation 0.051), so pooling cost the national fit nothing visible
  (leave-one-out 414 against 400) and the national rate sat one bin low; a common quarterly factor for the three regions
  now shows the misfit in the history (2026-10-16).
- Ask B's rounding floor raised to 0.27 of a bin: unreachable for the smallest group, whose change moves about half a
  bin with each claim; kept at the design's 0.23.
- regional sizing alone: both top responses land it once the refiling is filed, per the rule 3 re-audit
- A refusal's weight decaying over four weeks with month swings of 0.22 (the first strengthening world): the month
  model predicted past turns no better than each region's quarter taken whole (leave-one-out 322 against 319), the
  April 2020 turn's pandemic fall swamping the timing; a 2.5-week decay with larger month swings, common to the three
  regions, and timed episodes separates them (303 against 635).
- The September wave on the history as it stood (no late waves): the 2026 last-month refusals over the base week sat
  beyond every past turn and the multiplicative form overshot to about 17,600 (18,000); with late waves in the history
  and September's refused share at 0.55, the multiplicative form lands the golden's bin (17,225).
- Late layoff waves in the recent quarters (Western 2022, Coastal 2024): they lifted the timing-blind constructions on
  the recent windows to about 16,600, inside a bin of the golden; made early waves (2026-10-16).
- The first draw of the month swings' streams: the national step on the three regions' months and the rest's filed
  16,437 (16,000), 460 claims under the golden on a standard error of 220; among forty draws, the one kept holds every
  construction of the golden within 310 claims.
- The week ended 3 October at a round 11,800 (the late-claim share's first range): a round headline count reads as
  made up; the range moved to 0.0023-0.0095 (11,814), which also keeps Ask B's nearest change 0.281 of a bin from its edge.
