# task164: Calloway Valley Power's 2027 proactive transformer replacements by district (architecture 1)

Private, never ships. A new build (wave 6), numbered from seed FC35. The seed was read at its header and Situation only
(`status.py task164`). Its world (a California utility allocating 400 proactive service-transformer replacements across
twelve districts in 2027), its decision (each district's replacements, summing to 400, Foothill's on its own) and its
quantity (each district's forecast count of transformers at risk of summer overload, a forecast 4 to 9 pm peak above
1.2 times nameplate) are kept. The seed's mechanism (a pilot log whose filed determinations reproduce only under one
charging-start method) is not used in any form: there is no reproduction requirement, no certified record and no
withheld rule. The pitfall is re-found from how a service transformer's summer peak is set: the peak is the highest
quarter hour of the summer, it falls on an evening when the transformer's own load is highest, and on a small
transformer serving few vehicles that is an evening when a vehicle charges, so a vehicle adds most of its charger's draw
to the peak while its average evening demand is a fraction of a kilowatt.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task164.json`, architecture v1, registered 2026-10-18T01:34:28Z; `guard.py check` WARN only (answered below); nearest driver 0.07 (task86 v1) |
| Domain / task type | `energy-systems-utilities`, task type `load-forecasting` (serves Forecasting): the deciding quantity is each service transformer's summer 2027 4 to 9 pm peak, a window not yet open, forecast from its own recorded summer peaks and the vehicles registered at the record date |
| Objective | Forecasting & Predictive Modeling: the forecast summer is June to September 2027; the record date is Wednesday 31 March 2027, the extracts are pulled Monday 5 April 2027 and the compliance filing is due Friday 30 April 2027 |
| Shape | `05` allocation to a fixed total: each district's replacements (12) and its forecast at-risk count (12), Foothill's figure on its own (1), then two decoupled asks (the 2025-26 pilot close-out in its three districts: transformers replaced, kVA added, cost per replacement; and each district's summer 2026 transformer-failure customer-hours and customers out more than eight hours) and a chart of the customer-hours. Criteria on paper: 12 + 12 + 1 + 9 + 24 + 3 (chart) + 2 (files) = 63 |
| Decision | `allocation_to_total`, answer unit `count` (replacements per district, summing to 400 by the Commission's largest-remainder rule) |
| Mechanism | gap time (decisive: the evidence a solver reaches first is a vehicle's average draw over the 4 to 9 pm window, the decision bets on the transformer's highest quarter hour of the coming summer) with population (the effect belongs to the transformer's recorded maximum, which a vehicle on its schedule moves by most of its draw, not to the vehicle's own average draw); pattern D (two flawless grains: the per-vehicle window average is right at the system's grain, the coincident increment at the transformer's; the decision funds transformers); generators G2 (what one unit of the decided thing is), G14 (the increment conditioned on the premise's rate and the transformer's size), G7 (the 4 to 9 pm window against the hours EV-rate premises charge in); Gate G `method_or_model_selection`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `field_method` (diversified demand on a service transformer, the field's own construction); `own:coincident-peak-increment-by-rate-schedule` |
| Calibration | `none`: the 2024 to 2026 recorded peaks are the transformers' own history, the series a forecaster fits and holds out, never a certified record |
| Furniture | forum `regulator_or_inspector` (the Commission receives the compliance filing), forcing event `statutory_or_regulatory_filing` (the filing is due 30 April 2027), organisation family `utility_or_infrastructure`, role family `programme_officer` (the manager of the proactive replacement program files the allocation), context artifact `register` (the GIS service-transformer register the call reads for nameplate), opening `question-first`, question form `how-many` |
| Spine | the transformer load management extract, one row per transformer location and summer (2024, 2025, 2026: recorded 4 to 9 pm peak in kVA, its date and quarter hour, premises summed and AMI completeness), three season runs of 51,815 rows (155,445); constructed in the layout of a utility TLM extract |
| Deliverables | `ptr_2027_district_allocation.xlsx` (the allocation table, the at-risk counts and the ask tables) and `summer_2026_transformer_failures.png` (the failures ask charted, never the decision quantity) |
| People | drawn with `guard.py names --geo "United States" --seed 164`: Megan Stewart (distribution planning, owner of the TLM extract), Christopher Richardson (load research), Katelyn Duarte (regulatory compliance), Antonio Morgan (the pilot's construction lead); the requester is in no file and not in the prompt |
| World | Calloway Valley Power Company (searched: no utility or company of the name), a fictional investor-owned electric utility in California's Central Valley and Sierra foothills, twelve operating districts (Foothill, Railyard, Canal, Mission, West Bluff, Crestview, Lakeside, Sunrise, Sandhill, Kingsley, Highland, Brookside; each screened against every card's invented names, Old Town, Orchard, Delta and Northgate dropped for colliding); towns Calloway, Cedar Gap, Pine Hollow, Loma Pardo, Tule Bend, Cottrell, Lake Vardon, Juniper Springs, Garnet Wells, Copper Flat and Kingsley, screened against every card (Dunmore, Ostrander, Hartwell and Marlow dropped as other builds' nouns; Ridgeport, Elkhorn Springs and Gold Run Heights dropped as a letter or a word from real California places) |

**Data-native sentence.** A transformer's recorded summer peak is the single highest quarter hour of its summed
premises' load, so it is set on the evening its load happens to be highest; on a small pole-top serving one to five
homes that is an evening a vehicle at a default-rate premise charges, which makes the vehicle's contribution to the peak
most of its charger's draw, while the load research sample, read as averages, says the same vehicle draws 0.6 kVA between
4 and 9 pm.

**WARNs answered.**
- `three_rules.strategy_risk` (`grain_or_unit`): the analyst test runs on the clean truth with every field and rule read
  correctly (registrations matched, the decision, tariffs and extract read right) and still files the wrong split by
  adding each new vehicle's average window draw; the grain here is not a field to read, it is the level at which a
  vehicle's draw is coincident with a peak, which no column carries.
- `repeat.gate_g` and `overuse.gate_g` (`method_or_model_selection`, task161 and six of twelve): the label repeats, the
  driver does not (task161 draws a pre-tariff stock down at its holders' own use shares); no other key is honest, since
  the stump is a choice between two estimators of one filed quantity, settled by the transformers' own recorded peaks.
- `repeat.deliverables` (`png` and `xlsx`, task160): a filing workbook and a chart of an ask are what a planning engineer
  hands over; the chart carries the failures, not the call.
- `repeat.question_form` (`how-many`, task160 and task161): the call is a count per district, and a count asks how many.
- `people.first` (Christopher, one older build): kept, one older build only; the other three names are clear.

**Same-puzzle and same-driver tests.** Gap time, pattern D, `allocation_to_total`: no build in the last twelve or older
carries the triple (`guard.py check`). Gap time, pattern D, Gate G `method_or_model_selection`: none either. Gap
population, pattern D, Gate G `method_or_model_selection` was spent in eight older builds, so the card files the honest
decisive gap first, time: the window average against the peak quarter hour is the gap the default path falls into.

**Abstraction test.** Stripped of nouns: the rise in a shared asset's seasonal peak from one more intermittent load is
that load's draw at the moments the peak is set, and because a peak sits where the asset's load is highest, a load
joining an asset few others share adds most of its full draw, less on a large asset and less for each further load,
while its average draw over the peak window is a small fraction of that. Against `guard.py nearest`: task86 v1 (a priced
buyer-side position persisting across a supplier's substitutions), task120 v3 (a peak draw as inflow less storage
change), task131 v2 (a randomised tariff moving load out of a window and the rebound surge moving the maximum), task198
(an outcome falling with the number of parallel servers): none maps onto it. task131 is the nearest world (the maximum
of a summed curve on an energy system) and differs in the move: there the treatment shifts every household's load in
time and the rebound sets the new maximum; here nothing shifts, and the question is how much of one intermittent load
coincides with a small asset's maximum against its average.

**Kinship, answered (the builds the brief names, and every energy, utility or EV card).**
- task152 (a solar plant's forward sale after a module swap, the wear the swap restores read at just-reset states): a
  decline decomposition; nothing here decomposes a decline or reads a reset.
- task158 (GPU capacity priced at the rates of traffic with no cached input): a per-call rate that depends on what the
  call re-sends; here the rate per vehicle is fixed and what changes is how much of it coincides with a peak.
- task155 (crew hours taken when a call-in carries on from rostered work): a take-up probability conditioned on
  adjacency; no probability of acceptance enters here.
- task117 (a garage service's demand ratchet replayed over sessions whose start times follow the session ahead): a
  peak of summed load too, but there the decisive move re-times follow-on sessions behind faster chargers on one
  metered service; here no session is re-timed, the transformers' own recorded peaks give the increment, and the unit
  is a transformer shared by a few homes.
- task136 (rooftop PV enrolments that would have happened anyway): adoption counted against a counterfactual; here the
  vehicles are registered facts and the forecast is their load at the peak.
- task124 v1 to v3 (newcomers' share of a capped peak priced from dispatched analogs): retired architectures on a
  demand-response cap; nothing here is dispatched or capped.
- task183 (cable sections whose failures recur), task132 (a last-time buy of relay modules), task129 (vegetation
  outages), task197 (reserve droop against a ramp), task187 (wind turbines in a wake), task120 (a campus water peak):
  asset failure, spares, outage causes, droop, wake and storage; none forecasts a coincident peak increment.

**Sources read at the draw.** `stumping/references/client/two-layer-task-design.md` (energy has no Layer 2 patterns, so
the pitfall is built in `field_method`: diversified demand is the field's own construction for a service
transformer's peak); `strategies.md` F2 (grain: the unit is built, never read, and dies when a key column bridges the
grains; here no column holds a coincident increment and the TLM extract and the load research sample sit at different
grains); F6 and F5 (a pooled rate carried to a pool it does not fit; here the pooled increment fails because the
increment is the transformer's, not the vehicle's); the dead list (a quantity named by a filed sentence, a move visible
in the schema, a control that nominates; the decision files the at-risk test and the record date and nothing about how
a vehicle adds to a peak); `dataset-generation/references/layer1-messiness.md` energy items 1, 2, 6 and 8.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, every field and rule read right:

1. Read the decision excerpt: a transformer is at risk if its forecast 2027 summer peak exceeds 120 percent of its
   nameplate; the forecast is its recorded 2026 summer peak adjusted for the vehicles at its service addresses on the
   record date against those on its 2026 peak day, each at the schedule then in effect and each taken at the expected
   effect of one vehicle on a recorded peak, one figure for R-EV2 and one for every other schedule; 400 split by
   largest remainder.
2. Join the three TLM runs to the GIS register (the T prefix and the 2024 run's zeros), the service points to their
   transformers, and the DMV notifications to their service points through `matched_sp_id`.
3. Count each transformer's vehicles on its 2026 peak day and on 31 March 2027, each on its premise's schedule from the
   R-EV2 effective dates.
4. Take each schedule's figure from the EV charging load study, the average EVSE demand over the quarter hours
   ending 16:15 to 21:00 (kWh times four, over 0.95): 0.61 kVA a default-rate vehicle, 0.008 kVA an R-EV2 one.
5. Forecast each transformer as its 2026 TLM peak plus that figure for every vehicle added since its peak day, less it
   for every vehicle gone, with the difference for every premise moved to R-EV2.
6. Count the transformers above 1.2 times the register's kVA by district (1,591) and split the 400 by largest
   remainder.

Ends on: Foothill 59 replacements (1,591 transformers at risk; all twelve districts off the golden)
Golden: Foothill 79 replacements (1,824 transformers at risk)

## Stump sentence

Adding each vehicle's average 4 to 9 pm charging demand from the load study (0.61 kVA on the default rate) to its
transformer's recorded 2026 peak files Foothill 59 of the 400, because a service transformer's recorded peak is its single
highest quarter hour of the summer, set on an evening its own load is highest, and on a pole-top serving two or three
homes that is an evening a default-rate vehicle is charging: the transformers that gained one such vehicle between the
2024, 2025 and 2026 summers show their recorded peak rising by about 4.9 kVA, which files Foothill 79.

## Three rules

- Task type: `load-forecasting` in Energy Systems & Utilities, serving Forecasting & Predictive Modeling: each
  transformer's summer 2027 4 to 9 pm peak, a window not yet open, forecast from its own recorded summer peaks.
- Domain test: the deciding quantity is the expected rise in a service transformer's recorded summer peak when a plug-in
  vehicle joins it, one figure per rate schedule, estimated the distribution planner's way from the transformers' own
  recorded peaks before and after they gained a vehicle (coincident demand at the transformer), not from the vehicle's
  average demand.
- Swap: "each school district's share of 400 new classrooms in proportion to its schools whose 2027 peak-day enrolment
  exceeds 120 percent of capacity, from each new pupil's average attendance" reads the same and loses the stump: a
  pupil's attendance adds steadily, while here the quantity is the maximum quarter hour of a few homes' summed load on a
  small asset, the added load is intermittent, and a tariff moves it out of the window; with the nouns swapped the
  maximum of a small sum and the rate schedule vanish.
- Layer 1: the 2024 run in the TLM 4.2 layout (interval beginnings, zero-padded location numbers, upper-case districts;
  the TLM upgrade), location numbers with and without the GIS T prefix (TLM keys on the integer), DMV addresses in DMV's
  own abbreviations with 3.1 percent left blank by the utility's matcher (a unit left off, a misspelt street),
  notifications at addresses on no residential single-phase service, registrations of 1 to 4 April 2027 in the 5 April
  feed, AMI read shares under 100 percent, the GIS install-date sentinel, rate changes carrying a request and an
  effective date (the tariff's next-meter-read rule), the load study's kWh intervals with head-end gaps; each system is
  named in `## Draw` and each item is neutral (checks R2).
- Layer 2: `field_method`, diversified demand on a service transformer: the per-vehicle figure the forecast adds must be
  the vehicle's expected effect on the transformer's recorded maximum, which for one vehicle on a small transformer is
  most of its charger's draw; the methodological choice is that estimator, taken from the recorded-peak panel, against
  the load study's per-vehicle window average, and the data separates them out of sample.
- Decisive step: estimating a vehicle's contribution to a service transformer's summer peak as the coincident increment
  the recorded peaks show (the weather-adjusted rise in recorded peak of transformers that gained one vehicle between
  summers, by the premise's schedule), and rejecting the load study's window average because it leaves 4.2 kVA of each
  such transformer's 2026 peak unforecast when 2026 is forecast from 2025 (a 4.83 kVA mean rise against 0.61).
- Not semantics: every field read correctly (the TLM peak is kVA of the summed service points, the load study is kWh a
  quarter hour at the EVSE, the schedules' periods, the record date, the matched service points) still leaves the easy
  route adding 0.61 kVA a default-rate vehicle, a correct reading of the load study and a wrong estimate of the effect
  on a maximum.
- Not rule application: OP 4 files the quantity (the expected effect of one vehicle on a service transformer's recorded
  summer peak, one figure per schedule) and no rule, document or column says how it is measured; executing every filed
  rule (the record date, the peak day, the schedules in effect, one figure per schedule, 120 percent, the largest
  remainder) with the load study's figures files Foothill 59.
- Analyst test: a strong analyst who matched every registration, read every rate change and applied OP 2 to OP 5 to the
  letter but took each schedule's figure as the load study's average 4 to 9 pm demand files Foothill 59 (1,591 at risk),
  asserted on the clean truth and on the pack (checks R3a, R3a-pack).
- Estimand: OP 3 to OP 5 of decision_26-11-019_excerpt.pdf with Finding 5: every single-phase residential service
  transformer in service on 31 March 2027, its recorded 2026 summer peak adjusted for the difference between the
  vehicles registered at its service addresses on its 2026 peak day and on the record date, each at the schedule in
  effect on the date concerned and each taken at the expected effect of one vehicle on a service transformer's recorded
  summer peak, one figure for every vehicle on R-EV2 and one for every vehicle on any other schedule; at risk when that
  exceeds 120 percent of the nameplate of the unit installed on the record date, counted in its district; 400 split by
  largest remainder (OP 2).
- No decoy: the load study measures what it measures and draws no conclusion; no memo, draft, briefing, staff figure or
  stakeholder argues a per-vehicle figure or a ranking of districts; the IEPR forecast and the feeder peaks are declared
  distractors that rank nothing on the decision; no block is copied and no rule withheld.
- No certified replay: nothing certified or published is reproduced to recover a method; the TLM peaks are the
  transformers' own history, and the 2025-26 pilot's records feed only the close-out ask.
- Lesson: a peak is a maximum, so an intermittent load's effect on a small asset's recorded maximum is close to its full
  draw when it runs on the asset's peak evenings, and a forecast of a peak needs the coincident increment the asset's own
  peaks show, never the load's window average; no build on file teaches a maximum-of-a-small-sum increment (task131
  shifts a population's load in time, task117 re-times sessions behind a demand ratchet).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the load study's 4 to 9 pm average per vehicle, by schedule (Foothill 59) | OP 4 asks for each schedule's expected effect on a recorded peak and the study answers in the window's terms | the participants file names the schedule | yes, the reflex | none | none | one mean a schedule | readable |
| 1 the window's busiest quarter hour (Foothill 60), or the charging rate on the default schedule and nil on R-EV2 (Foothill 82) | none | charging_kw is a column | a coincident-demand reflex | none | none | one max or one mean | readable |
| 2 one recorded-peak rise for every vehicle whatever its schedule (Foothill 66), or the default-rate rise with R-EV2 nil (Foothill 80) | OP 4 asks for one figure per schedule | the schedule split sits in the rate log | pooling is the reflex once the panel is built | none | none | one mean | readable |
| 3 each schedule's expected effect measured on the 2024 to 2026 recorded-peak panel (decisive) | none: OP 4 files the quantity, one figure per schedule, and never how it is measured | no column carries a rise or an effect; the panel needs DMV states at three peak days joined through service points | no: the reflex for a vehicle's load at peak is the load study | none: nothing published or certified ties under any basis | none | a panel of transitions, weather-adjusted by district, one mean a schedule | silent |
| filed changes: new vehicles only (Foothill 71), schedules frozen at the peak (70), departures ignored (80) | OP 4: the difference between the two days, each at its schedule | DMV status, rate log | no | none | none | rule | readable |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | at risk | forecast exceeds 1.2 times nameplate | reaches it | same call | OP 3 "exceeds"; no changed transformer within 0.2 kVA of the line (HOLES) |
| SF2 | the base | recorded 2026 summer peak | a three-summer average of projected peaks | Foothill 84, eleven districts off | OP 4 "its recorded 2026 summer peak" |
| SF3 | nameplate | unit installed on the record date (register) | the 2026 TLM run's kVA | same call | OP 5; the two agree at every location |
| SF4 | vehicles registered at its service addresses | matched notifications | matched plus the matcher's misses placed by address | same call | records converge (R2-unmatched) |
| SF5 | when the 2026 state is taken | the day of the recorded 2026 peak | 30 September or 1 June 2026 | two and four districts off | OP 4 "on the day of its recorded 2026 peak" |
| SF6 | schedule in effect | effective_date | request_date | allocation unchanged, one at-risk count | OP 4 "in effect"; tariff special condition; dictionary effective_date |
| SF7 | no vehicle after the record date | registrations to 31 March 2027 | the 5 April feed | same call | OP 4; records converge (R2-april) |
| SF8 | district | the register's district on the record date | the TLM district code | same call | OP 3; the two agree everywhere |
| SF9 | expected effect | mean rise | median rise | Foothill 82, eight districts off | OP 4 "expected effect" |
| SF10 | the split | largest remainder | plain rounding | same call | OP 2; every share 0.29 or more from a half |
| SF11 | summer | 1 June to 30 September | calendar year | same call | Finding 5; every peak dated inside |
| SF12 | 4 to 9 pm | quarter hours ending 16:15 to 21:00 | the 2024 run's beginnings 16:00 to 20:45 | same call | dictionary; the same intervals labelled by their start |
| SF13 | units | kVA (TLM at 0.95) | kW | same call | dictionary; the golden adds kVA to kVA |
| SF14 | in service on the record date | the register at the pull | locations changed after it | same call | no location added or removed between the record date and the pull |
| SF15 | registered on the record date | present on 31 March 2027 | a status ending that day | same call | no registration ends on 31 March 2027 |
| SF16 | forecast 2027 summer peak | OP 4's definition | a weather-normalised or trended peak | not the decision's quantity | OP 4 defines it; OP 4 "no other change in load" |
| SF17 | the granularity of the effect | one figure for R-EV2, one for every other schedule | by fuel type (BEV 5.64, PHEV 1.94), by district, by transformer size, by size and position | Foothill 78 six off, 80 seven off, 79 none off (three counts), 80 two off | OP 4 "one figure applying to every vehicle on Schedule R-EV2 and one to every vehicle on any other residential schedule" |
| SF18 | the R-EV2 figure | the expected effect measured like the other schedule's (0.88) | nil or 0.2 because R-EV2 charges after midnight | Foothill 80 with eight and with four districts off | OP 4 asks for an expected effect for R-EV2; the panel's R-EV2 transitions average 0.88 kVA (REV2) |

## Ladder

Rungs from the pack (`calc.ladder`), each a complete pipeline, the allocation's districts off the golden and Foothill:

| Rung | Construction | At risk | Foothill | Districts off | Dies to |
|---|---|---|---|---|---|
| 0 (default) | load study window average by schedule, every change | 1,591 | 59 | 12 | the 2025 to 2026 back-test (4.23 kVA unforecast per added default-rate vehicle; BACKTEST) |
| 1a | the window's busiest quarter hour by schedule | 1,570 | 60 | 12 | the same back-test |
| 1b | charging rate (6.3 kVA) on the default schedule, nil on R-EV2 | 2,006 | 82 | 7 | the panel: a default-rate vehicle raises a recorded peak 4.9 kVA on average, an R-EV2 one 0.9 |
| 2a | one recorded-peak rise for any vehicle, whatever its schedule | 2,022 | 66 | 9 | OP 4's one figure per schedule; the panel's R-EV2 transitions rise 0.9, the default-rate ones 4.9 |
| 2b | default-rate rise, R-EV2 nil | 1,794 | 80 | 8 | the panel's R-EV2 transitions (0.88) |
| 3 (decisive) | each schedule's expected effect from the recorded-peak panel | 1,824 | 79 | 0 | (golden) |

Filed-rule rungs (OP 4): new vehicles only 2,174 at risk, Foothill 71; schedules frozen at the peak 2,080, 70;
departures ignored 1,912, 80 with four districts off. Every one of the eleven per-schedule estimators the pack supports
gives the same twelve counts (FAMILY-pack; FAMILY-spread lists them): the one-vehicle means on both transition years,
on 2024 to 2025 alone (5.01 and 0.79 kVA) or 2025 to 2026 alone (4.83 and 0.98), with the district's median ratio,
its mean difference or no weather adjustment; the per-vehicle mean over one or two vehicles added; least squares of
the change on the vehicles added, weather-adjusted, with district-and-year or year effects, or over every change
(4.69 to 4.71 and 0.64 to 0.73); and the 2026 cross-section within district, rating and service points (4.46 and
0.83). The 2027 additions' fuel mix (79.2 percent battery electric) matches the history's one-vehicle transitions
(80.5 percent), and the default-rate figure reweighted to it files the same allocation (FUELMIX). Worth: the decisive
move takes Foothill from 59 to 79 and the at-risk total from 1,591 to 1,824; every correction below it moves one way and
leaves at least seven districts off.

**Natural routes, measured on the cut pack** (`checks.py` CORRIDOR, ROUTES, ROUTES-cf). Constant per-vehicle figures
land the golden allocation for a default-rate figure of 4.2 to 5.2 kVA with an R-EV2 figure of 0.1 to 1.5 kVA: a
coincidence factor of 0.66 to 0.82 on the load study's mean charging rate of 6.34 kVA with a small R-EV2 factor, the
planner's own knowledge that a lone vehicle on a small transformer is mostly coincident with its peak; with R-EV2 nil
no factor from 0.50 to 1.00 lands. Every load-study figure (0.61 average, 0.94 busiest quarter hour) and the charging
rate itself lie outside the corridor. The rest miss the allocation in eleven or twelve districts (ROUTES): the IEPR
2027 vehicle forecast (Foothill 17), the vehicles registered on the record date (25), the default-rate vehicles alone
(51), the vehicles added since the peak (32), the 2026 overloads alone (58), the 2026 peaks over 1.15 (46), each
transformer's 2025 to 2026 rise repeated (53) or 2024 to 2026 trend (57), the summer 2026 failures (43), the
transformer counts (40); each participant's mean 4 to 9 pm maximum (5.88 and 3.02 kVA) gives Foothill 78 with ten
districts off. Paper estimate, with the stage 4 audit: a top response lands the call through the panel, or a
coincidence factor in that band with a small R-EV2 factor, about one time in eight; both top responses about one time
in thirty.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | single-phase residential transformers in service on the record date | OP 3; register and every TLM run hold the same 51,815 locations (C1) |
| 2 | Unit of account | the transformer, counted by district | OP 2 and OP 3 |
| 3 | Attribution window | summer 1 June to 30 September | Finding 5; every peak dated inside (SF11) |
| 4 | As-of dating | the record date, 31 March 2027 | OP 5; no registration ends on it, April registrations converge (SF7, SF15) |
| 5 | Version basis | the 2026 TLM run against the pull's register | identical kVA at every location (SF3) |
| 6 | Denominator | the system's at-risk total | OP 2 |
| 7 | Weighting | each one-vehicle transition once in the per-schedule mean | OP 4 "expected effect"; least squares and the cross-section weight otherwise and agree (FAMILY-pack) |
| 8 | Window length | the panel's summers | either transition year alone gives the same counts (FAMILY) |
| 9 | Boundary inclusivity | exceeds | OP 3; holes of 0.2 kVA around the line for every changed transformer (HOLES) |
| 10 | Rounding path | whole replacements | OP 2; plain rounding agrees (SF10) |
| 11 | Tie-break | equal remainders | none: every share 0.30 or more from a half and twelve distinct counts |
| 12 | Maturity and censoring | vehicles not yet registered | OP 4 excludes them; the IEPR forecast is a distractor |
| 13 | Order of operations | forecast, threshold, count, split | OP 2 to OP 4 in one order |
| 14 | Row order | none | no step depends on file order |
| 15 | Duplicate resolution | one notification per vehicle and address | dictionary grain statement; no vehicle twice at one address |
| 16 | Identity normalisation | T prefix, zero padding, DMV addresses | R2-keys, SF4 |
| 17 | Netting against gross | departures and moves against registrations | OP 4 "the difference" |
| 18 | Dimensional units | kVA | dictionary; load study kWh to kVA at 0.95 only on the default path (SF13) |
| 19 | Code and status semantics | R-EV2 against R-TOU4 and R-1; CARE is a flag | tariff excerpt; dictionary |
| 20 | Integerisation | largest remainder | OP 2, C1 with plain rounding |
| 21 | Clause scope | each vehicle's schedule on each of the two dates; one figure per schedule for every vehicle | OP 4 "on the date concerned", "one figure applying to every vehicle" |
| 22 | Forward window contents | the vehicles registered on the record date | OP 4; no other change in load |

## Literal reader

Executed word for word, Finding 5 and OP 2 to OP 5 fix the population (the register on the record date), the outcome
(the recorded 2026 peak adjusted for the difference between the vehicles on the peak day and on the record date, each at
its schedule then), the granularity and the functional (each vehicle at the expected effect of one vehicle on a recorded
peak, one figure for R-EV2 and one for every other schedule), the threshold (exceeds 120 percent of the record-date
nameplate), the unit (district counts) and the split (largest remainder); the one open element, how each schedule's
effect is measured, is settled by the TLM history: all eleven per-schedule estimators on the 2024 to 2026 panel give the
same twelve counts, and the load study's window average fails the 2025 to 2026 back-test by 4.23 kVA a vehicle.

## Oracles

- TLM peaks: the history the forecast is fitted on; no published or certified figure ties under any basis.
- Load study: an EVSE measurement in its own terms; nothing reconciles to it.
- The decision's "about 51,800" transformers: a rounded count that confirms nothing.
- IEPR 2027 vehicle forecast (distractor): a different population at a different date; ties to nothing.
- Feeder-head peaks (distractor): MW at the feeder; no transformer figure reconciles to them.
- None ties only under the golden.

## Ask sheet

**Main call's declared population:** the three TLM runs, the GIS register, the service points, the rate change log
and the DMV notifications (with the decision and the tariffs). Device and hazard rows in it: 0 (SEP, SEP-corr: the
golden reads none of the work orders, cost lines, change log or OMS lines, and the register carries the true rating at
every pilot record correction). Neither ask is keyed to the call, its construction or its figures; they share no
primary device.

**Ask A. The 2025-26 pilot close-out in Railyard, Canal and Brookside** (9 figures: transformers replaced, nameplate kVA
added, cost per transformer replaced). H18 home: the program's own close-out, the cost basis and the stock it already
renewed, a measure the call does not turn on. Golden: Railyard 94, 1,812.5 kVA, $6,799; Canal 81, 1,532.5 kVA, $7,049;
Brookside 88, 1,615.0 kVA, $7,008.
- Primary (D9 with D2, silent): the units the screen ranked first because GIS recorded them a size small were found
  larger on the pole, left in place and their record corrected under the pilot's own orders: the change log shows a
  PTR change with the serial unchanged (4, 8 and 4). The GIS PTR rows count them as replacements and add their kVA;
  only the unchanged serial, and the orders' labor-only charges, show it.
- Pin (stage 4): the asking sentence files the cost basis as "the lines on its work orders in that district, net of
  reversals, over the transformers it replaced", so cancelled and no-work orders' lines count and the -R and -C pairs
  net; the judge read the earlier "everything charged" as supporting the golden and asked for one reading.
- Hazards: second units taken under one order carry a PTR change with no work order (an unmatched join that the reason
  code resolves); substitutions (planned 50, set 37.5); cancelled orders' survey charges; lines posted to the wrong
  order and moved (-R, -C); contract accruals reversed the next day.

**Ask B. Summer 2026 transformer failures by district** (24 figures: customer-hours and customers out more than eight
hours). H18 home: the reliability case for the program, in the reliability report's words. Golden (customer-hours,
customers over eight hours): Foothill 1,010 and 50, Railyard 1,676 and 80, Canal 1,185 and 54, Mission 1,231 and 52,
West Bluff 810 and 42, Crestview 717 and 39, Lakeside 540 and 21, Sunrise 1,181 and 41, Sandhill 1,527 and 87, Kingsley
1,063 and 35, Highland 764 and 18, Brookside 652 and 35.
- Primary (D6, silent, the proven shape): an outage event's customers out is the event's total, repeated on each of its
  transformer lines; on a failure that took a tap or loop fuse every line carries the whole event's customers, so the
  per-line product counts them once a line. Only the line's own service points (another file) show it; every district
  has such events.
- Pin (stage 4): the dictionary's dispatch_district definition files that outage reporting counts each line in the
  operating district of the transformer it de-energised; on dispatch_district ten districts' customer-hours move
  (Canal 734 against 1,185; ASK-district).
- Hazards: the OMS clock in UTC (documented; failures on the evenings of 31 May and 30 September cross the window),
  the dispatch district (filed), the overload operations OL-XFMR beside the failures EQ-XFMR (the cause list), the
  staged restoration (each line its own restoration).

Pair ceiling: 31.6 (cracker 48.1, mirror 15.1)
Mirror leakage: 5.6 per cent of ask weight (the mirror reads completed work orders and their planned sizes, and the
OMS lines as exported)
Measured by: generator/cracker.py

| Ask | Figures | Cracker path | Cracker value against golden | Cracker |
|---|---|---|---|---|
| A transformers replaced | 3 | GIS PTR changes in the pilot window | 98, 89, 92 against 94, 81, 88 | miss |
| A kVA added | 3 | the same rows' kVA | 1,852.5, 1,615.0, 1,655.0 against 1,812.5, 1,532.5, 1,615.0 | miss |
| A cost per replacement | 3 | every pilot charge over those rows | $6,522, $6,415, $6,703 against $6,799, $7,049, $7,008 | miss |
| B customer-hours | 12 | customers_out times each line's hours, local window, register district | every district above the golden (Railyard 6,391 against 1,676) | miss |
| B customers over eight hours | 12 | customers_out on lines over eight hours | every district above the golden | miss |


## Leak sweep (stage 3)

`leak.py task164 --asof 2027-04-05`: REVIEW, no LEAK. Each line answered:
- Sweep 3, the decision carries 120: the filed threshold of OP 3, stated by the Commission and asked of nobody.
- Sweep 3, the decision carries the call's words: Finding 4 names the twelve districts and OP 1 the 400, the decision's
  own furniture; no district figure appears in any document.
- Sweep 4, the decision's stump terms (schedule, vehicle, recorded, effect, record): OP 4 files the outcome, the
  comparison and the granularity (the recorded peak, the vehicles on two dates at their schedules, one expected effect
  per schedule); it names no per-vehicle figure, no estimator and no window average, which is the decisive step.
- Sweep 4, the tariff's terms (schedule, vehicle, effect, quantity, percent, registered): R-EV2's applicability, the
  tiers and the change-of-schedule rule in a utility's own tariff words.
- Sweep 8, `qc_flag`, `device_id`, `internal_order`: a weather network's quality flag, an OMS device field and the
  ledger's internal order, each the system's own column name.

## Tried and rejected

- The seed's pilot reproduction (a filed set of pilot determinations that only one charging-start method reproduces):
  rejected at the draw, a withheld rule recovered from a certified record; the 2025-26 pilot survives only as the
  close-out ask's records.
- Adoption clustering as the decisive step (new vehicles land where vehicles already are): rejected at the draw; the
  forecast's vehicles would have to be placed stochastically, so the at-risk count is an expectation over placements and
  no figure is determinate; the estimand files the vehicles registered at the record date instead.
- Rate-plan shifting as the decisive step (which charging leaves the window on each rate): kept only as a lower rung;
  a solver who reads the load research sample by rate sees it in one group-by, so it cannot carry the stump.
- Gap population first with pattern D and Gate G `method_or_model_selection`: blocked by `test.same_driver_older`
  (eight older builds); the honest decisive gap is time (the window average against the peak quarter hour), filed first.
- A least-squares fit on vehicles added and the 2026 cross-section as family members under strong adoption clustering:
  their R-EV2 coefficients absorbed the clustering and widened the holes past what the forward fleet could clear;
  clustering cut to the districts' own rates and the cross-section taken within district, size and premises, after
  which both give the golden counts.
- Greedy steering of the district counts, then a seeded random search over three districts: both left a district on a
  half (Sunrise at 4.995) or failed on a district that cannot lose a transformer (Lakeside); replaced by a knapsack over
  all twelve districts with every share at least 0.26 from a half and the twelve counts distinct.
- A forecast base averaged over the three summers' projected peaks: a forecaster's honest move that moves ten
  districts (each transformer's maximum regresses to its mean); closed by filing the recorded 2026 peak as the base in
  OP 4, the Commission's own definition of the forecast, which leaves the per-vehicle effect open.
- Median recorded-peak rises as a robust estimator: Foothill 79 with ten districts off, because an R-EV2 vehicle's
  rise is usually nil and occasionally a full charger; closed by OP 4's "expected effect".
- Unrounded world counts: the first draws gave every district a round transformer count and three districts 19
  transformers at risk; the districts now hold 51,815 locations in unround counts and the planner keeps the at-risk
  counts distinct.
- Failure counts by district as an ask: the cracker banks them by counting distinct failed units; replaced by the
  customers out more than eight hours, which the OMS event-level customers figure moves.
- A failed unit restored with its tap: left Crestview's and Kingsley's over-eight-hour figures unmoved by the device;
  the failed unit now waits for a line truck after the tap or loop is re-closed, as crews work, and every district's
  figure moves.
- Rate requests drawn freely before their effective dates: dated at the request, three districts' at-risk counts moved;
  a request for a change taking effect after the transformer's 2026 peak now comes after that peak where the calendar
  allows, leaving one count and no allocation on the reading the tariff rules out.
- OP 4 as first filed ("adjusted by the expected effect on that peak of the difference between the plug-in electric
  vehicles"), with a size-by-position table as the golden: the stage 4 judge found the effect's granularity unfiled
  (NOT_DETERMINISTIC, SEND_BACK, Gates C and E), estimators by fuel type, district, size, a pooled median and an R-EV2
  nil filing Foothill 74 to 79; filing the panel method was refused as rule application. OP 4 now files the WHAT only:
  each vehicle at the expected effect of one vehicle on a recorded peak, one figure for R-EV2 and one for every other
  schedule. The hole family was rebuilt on the eleven per-schedule estimators (one-vehicle means by transition year and
  weather adjustment, least squares with district and year effects, the cross-section), and the golden moved from the
  size-by-position table (Foothill 77) to the per-schedule means (Foothill 79).
