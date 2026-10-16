# task149: Ostrander Logistics' fiscal 2027 recordable injuries at its twenty ergonomics programme DCs (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC20. The seed (a logistics operator's ergonomics
programme at twenty growth sites, priced by the vendor per forecast recordable injury) was read at its header and
Situation only. Its world, decision and quantity are kept. Its mechanism, new hires not yet in the tenure window where
harm surfaces, is not kept: a hazard by time since hire is a clock read against a window, close kin to task133's delayed
entry and task130's report lag. The pitfall is re-found from how a contract distribution centre's hours come to exist:
the labour plan does not schedule hours, it divides the cases a DC must move by the engineered labour standards and by
the pace the planners assume, and the recordable rate per hour worked is not a property of the DC but of how fast those
hours are worked against the standards. The FY2027 operating plan gives the twenty DCs their new accounts' cases at
labour hours that imply each crew working about 9 per cent faster against standard than it does today.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task149.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (repeat.decision, answered below), no BLOCK; the older same-puzzle and same-driver signatures (time, G14) against task134's round-1 lineage and task452's v1 lineage differentiated on the card; nearest drivers 0.07 (task89 lineage, task54) and under |
| Domain / task type | `epidemiology-public-health` (client domain), task type `health-burden-impact-modeling` (serves Forecasting): the call is the burden of occupational injury a working population will carry under a planned change in its exposure, built the impact-modelling way, the burden under the shifted exposure distribution through the exposure-response, not today's burden scaled. Occupational injury epidemiology is the field that owns a recordable-injury forecast on person-time; Human Factors & Ergonomics has no task type serving Forecasting that fits (its one, human-reliability assessment, prices error probabilities in safety-critical control tasks), and the seed's Supply Chain label is a house domain whose pairing with Forecasting repeats task147 |
| Objective | Forecasting & Predictive Modeling: the recordable cases the twenty DCs will log in fiscal 2027 (27 December 2026 to 25 December 2027), a window not open at the decision (the vendor agreement is signed in November 2026 on the forecast) |
| Shape | `single-figure`: one committed fiscal 2027 total, its critical components (the plan's pace against standard, the rate's response to it), a one-slide chart and two ask tables on fiscal 2025 and 2026 records supplying the criteria (counted in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `count` (recordable cases, to the nearest hundred) |
| Mechanism | gap time (decisive: the history describes each DC's rate per hour at the pace its crews worked; the decision bets on hours worked at the pace the plan sets) with population (the plan's hours are a different population of hours, worked faster); pattern none; generators G14 (the historical rate per hour does not apply to the plan's hours), G6 (the pace mix of the hours shifts under the rate), G13 (the window the plan covers); Gate G `method_or_model_selection`; strategy `forecast_method_backtest` (the rate is stationary only once conditioned on pace against standard, a constructed exposure, and every natural fit fails out of sample where pace moved) |
| Layer 2 family / pattern | `field_method`; `epidemiology-public-health/health-burden-impact-modeling/2` (the potential impact fraction is not a scaled attributable fraction: compare the shifted exposure distribution through the exposure-response). Here the exposure is work pace against the engineered standard, its response is estimated within each DC from the history, and the shift is the plan's |
| Furniture | forum `executive_team` (the agreement is approved with the FY2027 plan), forcing event `purchase_order_or_contract` (Lindqvist's per-case price is applied to the forecast at signing), organisation family `logistics_or_3pl`, role family `operations_director` (the director of environmental health and safety owns the forecast), context artifact `capacity_report` (the FY2027 operating plan), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `wfm_hours_by_dept_week_fy21_fy26.csv`, the workforce-management system's weekly labour hours, one row per DC, fiscal week and labour department with hours by pay code (constructed, 146,400 rows) |
| Deliverables | `ergonomics_forecast_fy2027.xlsx` (the forecast, its components, the two ask tables), `ergonomics_forecast_fy2027.pptx` (one slide: the forecast and the chart of the twenty DCs' recordables by fiscal year) |
| People | drawn with `guard.py names --geo "United States" --seed 149`: Sherri Newton (director of environmental health and safety, the requester; not in the prompt), Jesse Delgado (safety analytics manager, the EHS exports), Kurt Gilbert (industrial engineering manager, owner of the engineered labour standards), Nichole Sandoval (operations planning manager, FP&A, owner of the FY2027 operating plan), Tracy Curtis (Lindqvist Ergonomics Group's account director) |

**Guard.** `guard.py check` on the registered card: WARN `repeat.decision` (quantity_figure beside task148). Answered:
the call is a forecast count the vendor's price multiplies, so a quantity is the honest decision type; task148 is a
credit-loss allowance in dollars on a loan servicing history and shares nothing else on the card. The first check
blocked on `test.same_puzzle_older` and `test.same_driver_older` (gap time, G14) against task134's round-1 lineage and
task452's v1 lineage; the card carries both differentiation lines: task134's round 1 timed a conversion hazard by each
member's time since entry (no clock here, no entry date); task452's v1 filled a sparsely sampled factor that rises with a
recorded one (here the rate is recorded every week at every DC and the step is its response to pace against the
engineered content of the work, carried to a plan faster than the history ran).

**Same-puzzle and same-driver tests.** Gap time, decisive G14, decision `quantity_figure`, Gate G
`method_or_model_selection`: no build in the last twelve (task261 to task148) carries the triple (task146 is population
and G14; task461 is time and G13; task145 is time and G16). The older matches are differentiated above.

**Abstraction test.** Stripped of nouns: the hazard per unit of working time rises steeply with how fast a fixed content
of work is done, measured against that work's engineered content and read within each unit, and a forward plan that fits
more work into each hour concentrates it; carrying today's rate per hour, per item or per unit of engineered work onto the
plan, reading the speed off raw item counts, or reading it across units rather than within each, under-counts where the
plan raises the speed. Read by mechanism rather than score, the nearest drivers are: task46 (a rate stationary in
cumulative service exposure rebuilt from a movement log: a cumulative clock, here an intensity with no memory); task47
(per-order yields where per-unit rates mislead as basket size moves: an exposure base, here every base the history offers
is wrong and the rate's response to intensity decides); task79 (a conversion that falls once a capacity binds: a hard
kink at a capacity, here no capacity binds and the response is smooth); task181 (losses of separation follow vertical
crossings: an encounter count between units, here no unit meets another); task229 (a convex rating applied to a day's
mean: the grain of a measurement, here the plan's pace is read at the plan's own grain); task134 round 1 (a hazard by
time since entry); task130's lineage (regression to the mean of a group chosen on a noisy outcome: the programme DCs are
chosen on planned growth, and their rates are measured on every week since FY2021). None shares the latent structure.

**Data-native sentence.** Ostrander's contract DCs are planned in standard hours: the FY2027 operating plan takes each
DC's forecast cases by product category, multiplies them by the industrial engineering team's engineered minutes per
case, and divides by the pace the planners assume, while the DCs' own crews have averaged between 83 and 102 per cent
of standard since FY2021; the twenty programme DCs take on two retail clients' heavier freight in FY2027 at planned
hours that imply each crew working about 9 per cent faster against standard, and in every DC's own history the weeks worked faster
against standard carried more recordables per hour than its slower weeks, by far more than in proportion.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (60 builds): no driver on file makes the
rate per hour a function of work pace against an engineered standard (the nearest structures are an exposure base,
task47, a cumulative-exposure rate law, task46, and a capacity kink, task79). `layer2-rigor-patterns.md`: epidemiology,
health-burden line 2 (the potential impact fraction under a shifted exposure distribution) is the client's line for the
step; general statistics, regression diagnostics line 2 (leave-out misfit) is the neighbouring idea the back-test uses.
`two-layer-task-design.md`: "a forecast validated out of sample" and "the field's own method done right" are the
families. `strategies.md` F6 (a rate stationary only in a constructed exposure; every natural fit fails forward) is the
family record. The seed's header and Situation (FC20) for the world, decision and quantity only.

**World.** Ostrander Logistics, a privately held third-party logistics operator based in Columbus, Ohio, runs sixty
dedicated contract distribution centres for grocery and consumer-goods retailers in eleven states. Each DC receives,
puts away, replenishes, selects and loads cases for one or two retail clients; every direct labour function works to the
industrial engineering team's engineered labour standards (minutes per case by product category and function, with a
layout factor per DC), and selectors are paid an incentive above 100 per cent of standard. For fiscal 2027 (the 52 weeks
from Sunday 27 December 2026 to Saturday 25 December 2027, 4-4-5 periods) Ostrander has engaged Lindqvist Ergonomics
Group to run an ergonomics programme (lift assists at the heavy slots, job rotation, coaching) at the twenty DCs with
the largest planned growth, which take on two new retail accounts' freight (a warehouse club's and a regional grocer's,
heavy on beverages, pet food and bulk paper). Lindqvist prices the programme per forecast OSHA recordable case at the
programme DCs in fiscal 2027 on the FY2027 operating plan, and the agreement is signed on Monday 16 November 2026 on
Ostrander's forecast. The FY2027 operating plan (version 3) was approved by the executive team on Friday 23 October 2026.
The EHS team's exports, the workforce-management hours and the WMS throughput were pulled on Monday 2 November 2026
through fiscal 2026 week 44 (the week ending Saturday 31 October 2026).

## Default path

1. From the two EHS case exports (the legacy database to 30 June 2024, the EHS platform from 1 July 2024), keep each
   programme DC's recordable cases (first-aid cases and cases removed as not work-related out, each open case migrated
   across in 2024 counted once), by date of injury.
2. From the workforce-management hours, sum each DC's hours worked (every department and pay code, agency associates
   included) over the latest twelve months, fiscal 2025 week 45 to fiscal 2026 week 44.
3. Each DC's recordable rate is its cases over those hours (per 200,000 hours worked).
4. Multiply each DC's rate by its FY2027 planned labour hours (direct and indirect, the twelve periods summed) and add
   the twenty DCs.

Ends on: about 800 recordable cases in fiscal 2027 (816.7 from the shipped files, the same on the clean truth).
Golden: about 1,000 recordable cases in fiscal 2027 (1,001.8 from the shipped files, one standard error 26).

## Stump sentence

Carrying each programme DC's recordable rate per hour worked from the latest twelve months onto its FY2027 planned hours
files about 800 recordable cases for fiscal 2027 (Ends on); the step that lands it there is pricing every planned hour at
today's rate, when the plan moves the new accounts' cases through hours that imply each crew working about 9 per cent
faster against the engineered standards, and within each DC the rate per hour rises steeply with pace against standard,
so the twenty DCs come to about 1,000.

## Three rules

- **Task type:** epidemiology-public-health, health-burden-impact-modeling (serves Forecasting): the burden of
  occupational injury a working population will carry under a planned shift in its exposure, built the impact-modelling
  way, through an exposure-response estimated on person-time, the shifted exposure carried through it rather than today's
  burden scaled by the hours.
- **Domain test:** the deciding quantity is each DC's recordable case rate per 200,000 hours worked as a function of its
  crews' work pace against the engineered labour standards (the work-intensity exposure-response occupational
  epidemiology fits on person-time, a Poisson rate model with each DC its own baseline), carried to the pace the FY2027
  plan's cases and labour hours imply: the potential impact of a shifted exposure distribution, not the attributable
  burden scaled.
- **Swap:** "how many outages will our twenty substations have in fiscal 2027 under the load plan" keeps a rate times an
  exposure, but a substation's load has no engineered standard for a fixed content of work, no recordable case defined on
  person-time and no crew whose pace the plan sets, so the quantity that decides this call (pace against standard within
  each DC, read on hours worked) has nothing to attach to there.
- **Layer 1:** the EHS migration on 1 July 2024 (two exports in two layouts, the 113 cases open at go-live carried across
  under platform numbers with the legacy number kept, the platform's times in UTC against the legacy database's local
  dates and times); cases removed as not work-related kept in the platform with that status; the workforce-management
  system's DC numbers against the WMS's location codes and the EHS establishment names, Rockford re-numbered and re-coded
  at fiscal 2025 week 14 when its client changed; the WMS item hierarchy re-coded at fiscal 2023 week 27; the engineered
  standards versioned by effective date (Lebanon TN re-studied in fiscal 2024); a 53-week fiscal 2022; the plan in 4-4-5
  periods against fiscal weeks in the history; the ITA Form 300A submissions on calendar years with salaried hours in
  their totals. Each is what these systems write; none moves the call (R2.1 to R2.9 in `checks.py`: 1,010.7, 1,012.5,
  1,000.9, Rockford, 997.0, Lebanon TN, 1,003.8, all in the 1,000 bin; the ITA ties to the cleaned cases by calendar year).
- **Layer 2:** `field_method`, impact modelling under a shifted exposure: the rate per hour is a function of pace against
  the engineered standard, estimated within each DC (across DCs the faster ones are the better laid out and safer, so the
  pooled response nearly vanishes, 0.2 against 2.7 within), and the plan's cases and hours set a pace about 9 per cent
  above the latest twelve months' while its cases per direct hour move 3 per cent (the new freight is heavier); the easy
  route carries today's rate per hour onto the planned hours and files about 800.
- **Decisive step:** measuring each DC-week's pace as its engineered standard hours (cases shipped by category times the
  standard minutes in force) over its direct hours worked, fitting the recordable rate per hour on that pace with each DC
  its own baseline, and carrying it to the pace each programme DC's FY2027 cases and hours imply: 1.03 of standard
  against 0.95 in the latest twelve months, which raises the rate per hour by about a quarter and the twenty DCs' fiscal
  2027 cases from about 800 to about 1,000.
- **Not semantics:** no field, code, unit or definition says how fast the plan's hours are worked or how the rate per
  hour responds to it; the case classes, the migrated duplicates, the removed cases, the hours' pay codes, the WMS codes
  and the standards' versions are read correctly on the easy route too, and an analyst who reads every one of them
  correctly and carries today's rate per hour (or per case, or per standard hour) onto the plan files 780 to 890.
- **Not rule application:** the strict rule 3 test on every shipped sentence that bears on how the figure is computed:
  the prompt's question; the agreement's Schedule A (the twenty DCs) and Schedule B 2.1 to 2.3 (the forecast recordable
  cases, by date of injury in fiscal 2027, on the plan's volumes and labour hours; expected, not a high case); EHS-RK-01
  sections 3 to 8 (what is recorded, on whose log, by date of injury, privacy cases, removed cases, the migration, the
  rate's denominator); the export notes' field definitions; the plan's read-me (what each sheet holds, the hours
  Ostrander's and agency associates' together); the standards' notes (minutes per case shipped, by function and category,
  a site factor for putaway and selection, standard hours for a week). Executed word for word they fix the target and
  give no forecast: none carries a pace, a response or a method, none says the plan's hours are worked faster or that a
  faster hour carries more risk, and the literal combinations they admit (section 8's rate over the latest twelve months,
  fiscal 2025, fiscal 2026 to date or every year, or the 2025 Form 300A, times the plan's hours; the standards' standard
  hours times a rate per standard hour) file 778 to 888 (`R3s` in `checks.py`). The behaviour the decisive step turns on
  is inferred from the data, and the data rejects the rivals by a visible margin out of sample (Ladder).
- **Analyst test:** a strong analyst who reads every field, code and filed sentence correctly, cleans both EHS exports,
  sums the hours and forecasts each programme DC as its recordable rate per hour worked from the latest twelve months
  times its FY2027 planned hours files about 800 (Ends on: 816.7); the multi-year and seasonal rates, a rate per case or
  per standard hour, an hours elasticity, a fit on cases per hour or on the heavy-freight share within each DC, or on
  pace pooled across DCs all file 770 to 890; only the rate per hour carried to the plan's pace against standard within
  each DC files about 1,000 (executed in `checks.py` on the clean truth and on the pack).
- **Estimand:** the agreement's Schedule B 2.1 with the prompt: the number of recordable cases the twenty Schedule A DCs
  are expected to enter on their OSHA 300 Logs with a date of injury or illness in fiscal 2027 (Sunday 27 December 2026 to
  Saturday 25 December 2027), every associate on those logs included, on the FY2027 operating plan's volumes and labour
  hours for those DCs, in `target/lindqvist_program_agreement_fy2027_draft.pdf`. Population (members not yet observed:
  every fiscal 2027 case), outcome, window, unit and comparison are filed; the forecast's method is not.
- **No decoy:** no memo, earlier forecast, vendor figure, benchmark or stakeholder number states or argues a fiscal 2027
  count, a rate or a method; the plan's read-me and the standards' notes say what their sheets hold; the ITA submissions
  are records of past calendar years; the distractors (the workers' compensation loss run and the behaviour-based safety
  observations) rank nothing and forecast nothing.
- **No certified replay:** nothing certified or published is reproduced to recover a method; the response to pace is
  estimated from the raw weekly records, and the ITA submissions only confirm past counts under every method.
- **Lesson:** a recordable rate per hour worked is a property of how hard each hour is worked, so a plan that moves a
  fixed content of work through fewer hours raises the rate per hour, and the forecast has to carry the exposure-response
  to the pace the plan implies, read within each site because the sites that work fastest are the safest, and read
  against the engineered content of the work because cases per hour move with the freight; no build on file teaches pace
  against an engineered standard as the exposure (task47's exposure base, task46's cumulative-exposure rate law and
  task79's capacity kink are other structures).

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear. Values
from the shipped files.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (the default path) each DC's rate per hour worked, latest twelve months, times its planned hours | no | no | yes: the recordable rate times hours | no | no | yes: one ratio | readable |
| R0a the rate over every year since fiscal 2021 | no | no | yes: the long-run rate | no | no | yes | readable |
| R0s each DC's rate by fiscal period times the planned period hours | no | no | yes: seasonality | no | no | yes | readable |
| R1c each DC's rate per case shipped times the plan's cases | no | no | yes: a volume base | no | no | yes | readable |
| R1e each DC's rate per engineered standard hour times the plan's standard hours | yes: the standards' notes define a week's standard hours | yes: the standards table joins to the cases | yes: a work-content base | no | no | yes | readable |
| R2h a Poisson fit with DC effects and the log of hours (an hours elasticity) | no | no | yes: the obvious covariate | no | no | no | readable |
| R2u a Poisson fit with DC effects and cases per hour worked | no | yes: two columns, one division | yes: productivity as cases per hour | no | no | no | readable |
| R2p the rate per hour fitted on pace against standard pooled across DCs | no | no | no | no | no | no: pace built from three systems | silent |
| R3 (decisive) the rate per hour fitted on pace against standard within each DC, carried to the pace the plan's cases and hours imply | no: no sentence says the plan's hours are worked faster, names a pace or says a faster hour carries more risk | no: no column holds pace; it is built from the WMS cases by category, the standards in force and the direct hours | no: rate times hours is the reflex, and the plan's cases per direct hour barely move (1.03) while its pace against standard rises 9 per cent | no: no forecast, scorecard or certified figure ships | no: nothing in the files is wrong | no: a weekly join of three systems through two crosswalks, a fit with sixty DC effects, then the plan's own standard hours | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py`.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "recordable cases" | cases entered on the DCs' OSHA 300 Logs, injuries and illnesses | injuries only; every reported case | illnesses out: same call (asserted); every reported case: not the log (first aid is not recorded) | Schedule B 2.1 ("entered on the Program Sites' OSHA 300 Logs"); EHS-RK-01 3.1 |
| SF2 | "our twenty ergonomics programme DCs" | the twenty Schedule A DCs | any other twenty | not the agreement's sites | Schedule A; the site register's program column, the same twenty (asserted) |
| SF3 | "fiscal 2027" | 27 December 2026 to 25 December 2027, 52 weeks | calendar 2027 | not the agreement's window (the plan is fiscal) | Schedule B 2.1; agreement section 2 |
| SF4 | "under the FY2027 operating plan" | the plan's cases and labour hours for each DC and period, as approved | the plan's cases with hours re-derived at the DCs' current productivity | not the agreement's basis (that basis files the per-standard-hour rung, 888) | Schedule B 2.2 ("on the plan's volumes and labor hours") |
| SF5 | "log in fiscal 2027" | by date of injury or onset | by date entered | same call (asserted: no case is entered more than seven days after the injury) | EHS-RK-01 4.2 |
| SF6 | agency associates | on Ostrander's logs, counted; their hours in the history's and the plan's hours | Ostrander employees only | not the log | EHS-RK-01 3.3 (supervised day to day) and 8; the plan's read-me (the hours together) |
| SF7 | privacy cases | counted | left out | not the log | EHS-RK-01 5 |
| SF8 | cases migrated in 2024 | once | twice (both exports) | same call (asserted: 1,010.7) | EHS-RK-01 7; the platform's legacy reference |
| SF9 | cases removed as not work-related | out | in | same call (asserted: 1,012.5) | EHS-RK-01 6 |
| SF10 | "forecast" | the expected count | a high case | the golden matches the world's own expectation (990.7) | Schedule B 2.3 ("expected value") |
| SF11 | rounding | each DC-period unrounded, summed, rounded once to the nearest hundred | per DC | asserted one arithmetic | the prompt's last sentence |
| SF12 | hours worked | every department and pay code (direct, indirect, agency) | direct only | same call (asserted: the direct-hours offset files 1,001.8) | EHS-RK-01 8 (the rate's denominator); the plan's two hour columns |
| SF13 | the history read | fiscal 2021 week 1 to fiscal 2026 week 44 | from fiscal 2022, 2023 or 2024 | same call, same bin (asserted: 1,005.0, 1,005.0, 995.5) | none needed |
| SF14 | the plan's version | v3, approved 23 October 2026 | none ships | same | the plan's read-me |

## Ladder

Measured on the shipped files by `generator/calc.py` (the clean truth gives the same default, 816.7, and the same
golden fit, 1,001.8); every figure is the twenty programme DCs' fiscal 2027 recordable cases.

| Rung | Construction | Figure | Rounded | Dies to |
|---|---|---|---|---|
| R0 (default) | latest twelve months' rate per hour times planned hours | 817 | 800 | pace: the plan's hours are worked about 9 per cent faster against standard and the rate per hour rises with pace within each DC (out of sample 20.6 per cent a DC against the pace model's 11.1) |
| R0a | every year's rate per hour since fiscal 2021 | 779 | 800 | as R0 (16.3 out of sample) |
| R0s | each DC's rate by fiscal period times planned period hours | 780 | 800 | as R0 (16.1); the history's peak periods carry the peaks' own pace, which the plan does not |
| R1c | rate per case shipped times the plan's cases | 841 | 800 | the plan's heavier freight takes more work a case, and pace (19.0) |
| R1e | rate per standard hour times the plan's standard hours | 888 | 900 | pace: the rate per standard hour rises with pace too, the same work done faster (18.7) |
| R2h | Poisson, DC effects, log hours (elasticity 0.95) | 770 | 800 | the history's hours swing with volume at near-constant pace; the plan's do not (16.2) |
| R2u | Poisson, DC effects, cases per direct hour | 841 | 800 | cases per hour moves with the freight: the history's account wins and losses moved it at 30 DCs with no move in the rate per hour (in sample 60 deviance points worse than pace; with both in the model pace 3.0 (se 0.38), cases per hour -0.3 (0.32); out of sample 14.7 against 11.1, and 19.6 against 8.8 at the 7 DCs whose work content per case moved more than 3 per cent), and the plan's heavier freight holds it at 1.03 while pace rises 9 per cent |
| R2c | Poisson, DC effects, free log hours and log cases | 869 | 900 | as R2u (14.3 out of sample) |
| R2p | pace pooled across DCs | 783 | 800 | the faster DCs are the better laid out and safer, so pooled the response nearly vanishes (0.2) (43.3 out of sample) |
| R2s | Poisson, DC effects, heavy-freight share | 784 | 800 | the heavy share moves no rate at constant pace (16.2) |
| golden (R3) | pace against standard within each DC (response 2.7, se 0.2, Poisson on DC-periods, offset log hours), at each DC's FY2027 pace | 1,001.8 | 1,000 | (the golden) |

- **Every construction of the golden** (C1): weekly fit 990.2; period fit 1,001.8; negative binomial 1,002.8;
  direct-hours offset 1,001.8; with fiscal-period effects 1,007.9; with fiscal-year effects at fiscal 2026's level 989.3;
  free log hours and log standard hours 1,006.1; exponential in pace 1,013.6; fitted from fiscal 2022 1,005.0, 2023
  1,005.0, 2024 995.5; the programme DCs alone 981.7; the latest twelve months' rate times the fitted pace uplift 1,027.9.
  Span 981.7 to 1,027.9, every one in the 1,000 bin (the lowest 31.7 above 950, the highest 22.1 below 1,050). The
  world's own expectation (the plan's pace with the history's weekly swings around it) 990.7.
- **One sigma.** The golden's standard error from the fit (400 parametric draws of the DC effects and the response) 26.2;
  the 1,000 bin holds the golden plus or minus 51.8 and 48.2.
- **The data rejects the default and every rival.** Fitted on fiscal 2021 to 2024 and asked for fiscal 2025 and 2026 to
  date at each DC's actual hours: today's rate per hour misses by 20.6 per cent a DC (22.6 at the 24 DCs whose pace moved
  more than 4 per cent, errors correlated -0.42 with the pace change), the long-run rate 16.3, the seasonal rate 16.1, the
  rate per case 19.0, the rate per standard hour 18.7, the hours elasticity 16.2, cases per hour 14.7, free hours and cases
  14.3, the heavy share 16.2, pooled pace 43.3; the pace model 11.1 (9.9, -0.12), every rival 3.2 points or more above it
  (B1 to B7 in `checks.py`).
- **Position and dominance.** On the default the decisive move adds about 185 cases (816.7 to 1,001.8); every lower
  correction stays under 890. The nearest rival (R1e, 888) is 114 below the golden, a full bin.
- **Bins.** The default 816.7 (800 bin), the golden 1,001.8 (1,000 bin): two bins apart; no rival in the 1,000 bin.
- **Worth.** Graded: the call; the components the write-up states (the plan's pace against standard about 9 per cent
  above the latest twelve months', the rate per hour about a quarter higher at it), never an intermediate a valid method
  could skip.

## Closure table

Each row's assertion is in `checks.py` (C1 to C22).

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every case the twenty DCs enter on their OSHA 300 Logs with a date of injury in fiscal 2027, agency associates' and privacy cases included, none observed yet | filed (Schedule A, Schedule B 2.1, EHS-RK-01 3 and 5); SF1, SF2, SF6, SF7 |
| 2 | Unit of account | a recordable case | filed (Schedule B 2.1) |
| 3 | Attribution window | a case belongs to the fiscal year of its date of injury | filed (EHS-RK-01 4.2); SF5 |
| 4 | As-of dating | the plan v3 of 23 October 2026; history through fiscal 2026 week 44, pulled 2 November 2026 | the plan's read-me; the export manifest |
| 5 | Version basis | the plan v3 (only version shipped); the standards in force each week | asserted (Lebanon TN's re-study read either way, same bin) |
| 6 | Denominator | hours worked, every department and pay code | EHS-RK-01 8; SF12 |
| 7 | Weighting | each DC-period by its hours (Poisson) | C1 (weekly, period, negative binomial) |
| 8 | Window length | fiscal 2021 to 2026 week 44 | C1 (from 2022, 2023, 2024); SF13 |
| 9 | Boundary inclusivity | fiscal weeks Sunday to Saturday; the platform's UTC timestamps read in each DC's local time | asserted neutral (UTC dates read as dates: 1,000.9) |
| 10 | Rounding path | unrounded DC-period forecasts summed, rounded once to the nearest hundred | the prompt; SF11 |
| 11 | Tie-break | none arises | asserted (the golden is off every rounding edge) |
| 12 | Maturity and censoring | every case through week 44 entered by the pull | asserted (the last week's count in line with the weeks before) |
| 13 | Order of operations | cases, hours, standard hours, pace, fit, the plan's pace, forecast, sum, round | design; the decisive step is forced by the data (the back-test and the in-sample separation) |
| 14 | Row order | none matters | asserted (the exports read in reverse give the same figures) |
| 15 | Duplicate resolution | a migrated case once (the platform keeps the legacy number) | EHS-RK-01 7; SF8 asserted |
| 16 | Identity normalisation | DC numbers, WMS codes and EHS establishment names through the site register; Rockford's two numbers and codes | the register's crosswalk; asserted |
| 17 | Netting against gross | first-aid and removed cases out | EHS-RK-01 3.1 and 6; SF9 |
| 18 | Dimensional units | hours; cases; standard minutes per case shipped | the standards' notes; the plan's read-me |
| 19 | Code and status semantics | classification, OSHA case type, status; WMS category codes before and after fiscal 2023 week 27 | the export notes and the standards' notes; never the stump |
| 20 | Integerisation | none before the final rounding | design |
| 21 | Clause scope | EHS-RK-01 covers every Ostrander DC | filed |
| 22 | Forward window contents | the plan's twelve periods (52 weeks), the new accounts from period 1 | the plan |

## Literal reader

Executing the prompt, the agreement's Schedules A and B, EHS-RK-01, the export notes, the plan's read-me and the
standards' notes word for word fixes the target (the twenty Schedule A DCs' OSHA 300 Log cases with a date of injury in
fiscal 2027, expected, on the plan's volumes and labour hours) and every convention but the forecast's method; every
reading converges on the golden's bin or violates a quoted line (SF1 to SF14); the easy answers come from easy methods
on the same literal target (today's rate per hour, per case or per standard hour; seasonal, elastic or pooled fits),
never from another reading. The one reading that would change the basis, re-deriving the plan's hours at the DCs' current
productivity, is ruled out by Schedule B 2.2.

## Oracles

- The ITA Form 300A submissions (calendar 2021 to 2025, every DC): each establishment-year's recordable cases and total
  hours worked (salaried hours in); equal to the cleaned EHS cases by calendar year (asserted) and blind to the decisive
  step (no pace, no plan). They confirm the counts under every method.
- The site register: keys, clients and the program flag, no figure that ranks or forecasts.
- The distractors (the workers' compensation loss run, the behaviour-based safety observations): rank nothing; the call
  and both asks unchanged with both deleted (asserted, SEP1).
- Nothing ties only under the golden: no forecast, scorecard or certified figure of fiscal 2027 ships.

## Ask sheet

**Main call's declared row population:** the two EHS case exports' case, classification, status, date and DC fields;
the workforce-management hours; the WMS cases by category; the engineered standards; the FY2027 plan; the site register;
EHS-RK-01 and the agreement. Device and hazard rows in it: 0 (asserted, SEP1 to SEP3: the forecast computed from the main
files alone, without the work-status log, the item master, its history, the SKU picks or the distractors, is the golden;
the platform's day-count fields are read only by Ask A's code). Neither ask is keyed to the call, its construction or its
figures; they share no primary device.

**Ask A. Fiscal 2026 to date, each programme DC: the days away from work and of job transfer or restriction, added
together, that its recordable cases have carried to 31 October 2026** (20 figures).
- H18 home: the programme's severity baseline (Lindqvist's coaching and return-to-work support are sized on DART days,
  the agreement's section 4), a measure every programme DC carries that the call does not turn on; in the safety team's
  words ("days away", "job transfer or restriction").
- Construction: the fiscal 2026 recordable cases at each DC (EHS platform, removed cases out), each case's days from the
  return-to-work work-status log (calendar days from the day after the injury, away and restricted or transferred spells,
  to full duty, separation or 31 October 2026, 180 days at most in total, EHS-RK-01 9), attributed to the DC whose log
  holds the case.
- Golden: `figures.json` `ask_a_dart_days` (140 to 954 days a DC, 10,146 in all), equal to the world's day counts at every
  DC (AA1).
- Primary device A1 (D2, a value as of an earlier date that looks final): the platform's day-count fields are the site
  coordinators' counts as of each case's last update; for cases still away or restricted at that update the counts stop
  there, and the platform holds no flag beyond the update date; only the work-status log's spells, by a cross-file cut,
  show the days since.
- Second device A2 (D7, a prior-id chain): when an associate on restricted duty works the restriction at a sister DC
  (transitional duty: the home DC has no modified work), the sending DC's case manager closes her file as a transfer out
  and the receiving DC opens a continuation file under a new return-to-work id that carries the associate number and no
  EHS case number, and the system overwrites the associate's home DC on the first file; a join on the EHS case number
  drops the continuation's days, a sum by the log's home DC credits the whole case to the receiving DC. Every programme
  DC placed at least one associate (AA4).
- Hazards: HA1 the 180-day cap; HA2 a removed case's spells still in the log; HA3 separations end the count; HA4 cases
  open at the extract counted to 31 October.
- Stops (measured, `calc.ask_a`): the platform's fields as they stand (misses at 20 of 20 DCs); the log joined by EHS case
  number only, continuations dropped (20 of 20); the log summed by its own home DC (20 of 20); the over-correction, each
  continuation credited to the receiving DC (20 of 20).
- Span: the EHS platform export, the work-status log, the site register, EHS-RK-01 (4 files); 12 columns.
- Realism: coordinators update a case's days when they next touch it; a case manager at the receiving DC opens her own
  file for a transferred associate, and a case management system keeps one home DC per associate.

**Ask B. Fiscal 2026 weeks 1 to 44, each programme DC: the cases picked that weighed more than 50 pounds** (20 figures).
- H18 home: Lindqvist's lift-assist sizing (the assists go on the heavy slots, the agreement's section 1), a measure every
  programme DC carries that the call does not turn on; in the vendor's words ("cases over 50 pounds").
- Construction: the WMS SKU pick summary (cases picked by DC, SKU and fiscal period) joined to the case weight of the item
  version in effect during the period picked (item master history), each weight in pounds; cases strictly over 50 pounds.
- Golden: `figures.json` `ask_b_cases_over_50_lb` (437,458 to 2,041,509 a DC), equal to the world's heavy cases at every DC
  (AB1).
- Primary device B1 (D3, units set per source): case weights for items set up through the vendor portal since its March
  2025 launch are kilograms (the portal's field), every other weight pounds; the item master carries the weight source and
  no unit; only the weight-to-cube density by source and the pounds in bag descriptions show it. No portal item sits
  within half a pound of 50 (AB3).
- Second device B2 (D7, a code reissued): the WMS re-uses a discontinued SKU's number for a new item; the item master
  shows the current item only and its history file carries the earlier item's weight and dates, so picks of the old item
  before the change are weighed as the new one.
- Hazards: HB1 SKUs picked but missing from the master (items purged after discontinuation, in the history file, 4,326
  pick rows); HB2 cases at exactly 50.0 pounds (not over); HB3 Rockford's two codes (its picks under RKF2 only).
- Stops (measured, `calc.ask_b`): the master's weight read as pounds throughout (misses at 20 of 20); the current master
  only, kilograms converted (20 of 20); the cracker, current master and pounds (20 of 20); the over-correction, every
  weight set up since the portal launch converted (20 of 20); 50 pounds and over (20 of 20).
- Span: the SKU pick summary, the item master, the item master history, the site register (4 files); 10 columns.
- Realism: a vendor portal defaults to metric for imported items; WMS SKU numbers are recycled.

**The slide's chart** (about 5 criteria): the twenty DCs' recordable cases in each fiscal year from 2021 to 2025 (609,
623, 637, 588, 661 from the cleaned EHS exports, fiscal 2022 on 53 weeks) beside the fiscal 2027 forecast; its parts are
the five yearly bars, the forecast bar and its label.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 the 180-day cap | EHS-RK-01 9 | Ask A, 1 DC | measured (`stop_no_cap`) |
| HA2 removed cases in the log | the case manager keeps the spells | Ask A, 2 DCs | measured (`stop_with_removed`) |
| HA3 separations | the log's SEPARATED status | Ask A, 5 DCs | measured (`stop_sep_ignored`) |
| HB1 purged SKUs | the master purges discontinued items | Ask B, every DC | inside `stop_current` |
| HB2 exactly 50 pounds | a common bag weight | Ask B, every DC | measured (`stop_at_50`) |

**Referee.** For Ask A, the work-status log's continuation files (associate number and dates) and the EHS case's DC;
for Ask B, the item master's weight source against its cube and the history file's dates. Each is a source the golden
reads, not a control: no file ties only under the golden.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A days by DC (20) | the log joined to the platform by EHS case number, every filed rule (calendar days, 180 cap, separations) applied | the transferred associates' continuation days dropped: every DC low | miss |
| B heavy cases by DC (20) | the picks joined to the current item master, weights read as pounds | the portal items' kilograms read as pounds: every DC off | miss |
| the slide's chart | the cracker's forecast drawn as the golden draws it | the five yearly bars and the forecast | outside |

Mirror leakage: about 10 per cent of the ask weight (the mirror runs the same ask paths as the cracker and keeps the
chart's five yearly bars and its axis, not the forecast).
Pair ceiling: 36 (the cracker about 50 with the call, its components, the instructions and the chart; the mirror about 22
with the instructions, the chart's history and the asks' shared misses; 40 ask figures).

## Tried and rejected

- The seed's mechanism (new hires not yet in the tenure window where harm surfaces): rejected at the draw, a hazard by
  time since hire is close kin to task133's delayed entry and task130's report lag.
- Regression to the mean of sites chosen for a high recent rate: rejected at the draw, task130's lineage spent it
  (a group chosen on a noisy outcome, forecast by its own chosen-period value).
- Contact injuries scaling with how many associates share the floor at once (density per operating hour, a new shift
  spreading the crew thin): rejected at the draw, task181's driver (events follow encounters between units present at
  the same time, not the time units spend) in other nouns.
- Injuries per hour rising past a utilisation threshold of the building's capacity: rejected at the draw, task79's
  driver (a conversion that changes once a capacity binds, the forward window past it).
- Heavier freight read through a convex dose in case weight (fatigue-failure damage): rejected at the draw, a weight
  column in the item master makes it a stratification on a visible attribute, and the convexity is task229's driver.
- A first cut of the world where cases per hour back-tested as well as pace (MAPE 10.1 against 10.2 per cent, deviance
  1.3 apart): the history's freight mix was stable inside each DC, so the two exposures moved together and a fit on cases
  per hour (842, the 800 bin) was a defensible construction the data could not rule out. Rejected for an open method;
  repaired by the history's real account wins and losses (heavy and light accounts on and off at 30 DCs, staffed at the
  standards) and by two to four lasting pace changes at every DC, which separate the two (60 deviance points; 14.7
  against 11.1 out of sample).
- Ask A as two figures per DC (days away, days restricted): the cracker's log-based path gets every days-away figure
  right, since the continuation files hold restricted days only. Rejected; the ask asks the two added together, and every
  programme DC places at least one associate on transitional duty.
- A rival exposure read as agency hours left out of direct hours: the plan's hours did not say whether agency
  associates' hours were in them, so a reader could build the plan's pace on another basis than the history's. Closed by
  the plan's read-me (the hours Ostrander's and agency associates' together, as the WFM system records them), a WHAT.

## Build record

Stage 3, built 2026-10-16 from `task149/generator/build.py` (seed 1492027).

- Pack: 18 files, 6 formats (csv, json, parquet, pdf, txt, xlsx); the largest 1,051,088 rows (the SKU picks), the spine
  146,400 rows; distractors `wc_loss_run_valued_2026-09-30.xlsx` and `bbs_observations_fy2025_fy2026.csv` (metadata.json).
- Main call from the shipped files: 1,001.8 (about 1,000; one standard error 26.2); the default 816.7 (about 800);
  response 2.73 (se 0.20) within DCs, 0.17 pooled; the plan's pace 1.029 against 0.946 in the latest twelve months (8.8
  per cent), its cases per direct hour 3.1 per cent above, its hours 20.5 per cent; the rate per hour 26 per cent higher at
  the plan's pace. Every construction 981.7 to 1,027.9.
- Clean truth: the default 816.7, the golden's model 1,001.8, the world's expectation 990.7 (986.5 at a flat pace).
- Mess variants (R2): migrated twice 1,010.7; removed kept 1,012.5; UTC dates 1,000.9; Rockford as two DCs 1,004.4; old
  WMS codes unmapped 997.0; Lebanon TN's current factor throughout 1,001.2; week 53 dropped 1,003.8; illnesses out 989.0;
  the main files alone 1,001.8.
- Gates: `checks.py` 154 assertions, 0 failed (the measured lines above printed by it); `verify.py` agrees on its own code
  path (forecast 1,001.8, response 2.734, default 816.7, the chart and all 40 ask figures, the workbook and the slide); two
  byte-identical builds (target, goldens, metadata.json, figures.json, target.zip sha256 bc83c300f3ef8ed2); container
  audit clean on the pack and the goldens; `figures_check.py` 73 figures, 0 absent; `precut.py` 49 checks, 0 FAIL;
  `voice-check.py` PASS (772 characters); `leak.py` REVIEW, no LEAK (answered below); `guard.py heart` WARN
  (repeat.decision, answered under Draw), `surface` 0 promoted (nearest task71 at 0.100), `validate` clean.
- Golden realism and house fixes: the workbook's title states the finding, number formats per column, frozen headers,
  a provenance line from the pack; the slide's title states the forecast, its forecast bar distinguished and labelled,
  axis titled, a source strip; invented names a letter or a word from real organisations renamed in the generator (a
  health system, a grocery chain, a golf brand, three staffing brands); the folder index and the export notes'
  keys checked against the shipped set (H9) and the write-up's citations against the pack (H8).

## Leak review

`leak.py --asof 2026-11-02` on the cut: REVIEW, no LEAK. One line per REVIEW line.

- Sweep 3, the agreement's "USD 2,140": Katy DC's 140 DART days match inside the fee; a coincidence of digits, harmless.
- Sweep 3, the export notes carry 5 of 8 words of the call: the folder's title (the FY2027 ergonomics program forecast)
  names the subject and no figure; harmless.
- Sweep 3, the agreement carries 7 of 8 words of the call: Schedule B 2.1 defines the forecast the call fills, its
  B2.3 blank ("Forecast Recordable Cases ____"); the estimand, filed by design.
- Sweep 4, EHS-RK-01 (worked, injury, history, schedule, the procedure's own number): recordkeeping words; it names no
  pace, response or method (R3s asserted); harmless.
- Sweep 4, the agreement (twelve, injury, schedule): twelve installments, injury or illness, Schedules A and B; harmless.
- Sweep 6, the case exports, the plan, the standards, the agreement and the loss run name the twenty DCs beside numbers:
  records by DC (cases, hours, plan volumes, site factors, Schedule A, claims), none ranks the DCs on fiscal 2027 cases;
  the loss run is a declared distractor; harmless.
- Sweep 9, the plan's FY2027 period dates after the as-of: a forward plan by design (the allow-list is the plan alone).
- `guard.py surface` reads "Pleasant Prairie" as a persona: it is the Wisconsin village where DC 1104 stands, not a
  person; no change.

