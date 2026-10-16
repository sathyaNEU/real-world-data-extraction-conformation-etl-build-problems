# task149: Ostrander Logistics' fiscal 2027 recordable injuries at its twenty ergonomics programme DCs (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC20. The seed (a logistics operator's ergonomics
programme at twenty growth sites, priced by the vendor per forecast recordable injury) was read at its header and
Situation only. Its world, decision and quantity are kept. Its mechanism, new hires not yet in the tenure window where
harm surfaces, is not kept: a hazard by time since hire is a clock read against a window, close kin to task133's delayed
entry and task130's report lag. The pitfall is re-found from how a contract distribution centre's hours come to exist:
the labour plan does not schedule hours, it divides the cases a DC must move by the engineered labour standards and by
the pace the planners assume, and the recordable rate per hour worked is not a property of the DC but of how fast those
hours are worked against the standards. The FY2027 operating plan gives the twenty DCs their new accounts' cases at
labour hours that imply each crew working about a tenth faster against standard than it does today.

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
| Spine | `wfm_hours_by_dept_week_fy21_fy26.csv`, the workforce-management system's weekly labour hours, one row per DC, fiscal week and labour department with hours by pay code (constructed, about 110,000 rows) |
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
case, and divides by the pace the planners assume, while the DCs' own crews have run between 86 and 99 per cent of
standard since FY2021; the twenty programme DCs take on two retail clients' heavier freight in FY2027 at planned hours
that imply each crew working about a tenth faster against standard, and in every DC's own history the weeks worked faster
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

1. From the two EHS case exports (the legacy system to 30 June 2024, the EHS platform from 1 July 2024), keep each
   programme DC's OSHA recordable cases (first-aid cases and cases removed as not work-related out, each case migrated
   across in 2024 counted once), by date of injury.
2. From the workforce-management hours, sum each DC's hours worked (every department and pay code, agency associates
   included) over the latest twelve months, fiscal 2025 week 45 to fiscal 2026 week 44.
3. Each DC's recordable rate is its cases over those hours (per 200,000 hours worked).
4. Multiply each DC's rate by its FY2027 planned labour hours (direct and indirect, the twelve periods summed) and add
   the twenty DCs.

Ends on: about 800 recordable cases in fiscal 2027 (set on the pack at stage 3).
Golden: about 1,000 recordable cases in fiscal 2027 (set on the pack at stage 3).

## Stump sentence

Carrying each programme DC's recordable rate per hour worked from the latest twelve months onto its FY2027 planned hours
files about 800 recordable cases for fiscal 2027 (Ends on); the step that lands it there is pricing every planned hour at
today's rate, when the plan moves the new accounts' cases through hours that imply each crew working about a tenth faster
against the engineered standards, and within each DC the rate per hour rises steeply with pace against standard, so the
twenty DCs come to about 1,000.

## Three rules

Drafted at the draw; completed in stage 2.

- **Task type:** epidemiology-public-health, health-burden-impact-modeling (serves Forecasting): the injury burden a
  working population will carry under a planned shift in its exposure, through an exposure-response estimated on
  person-time.
- **Domain test:** the deciding quantity is each DC's recordable rate per 200,000 hours as a function of its crews' work
  pace against the engineered labour standards, the work-intensity exposure-response occupational epidemiology fits on
  person-time, applied to the pace the operating plan implies.
- **Analyst test:** a strong analyst who reads every field and rule correctly and forecasts each DC as its recordable
  rate per hour worked times its FY2027 planned hours files about 800 (Ends on); every exposure base the history offers
  (hours, cases, standard hours) and every fit on its visible columns files below the golden.

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
