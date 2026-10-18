# task179 design note

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** New, Forecasting, seed FC50. The world was
moved honestly off `local_government`: a private ambulance company holds a city's 911 ambulance contract (the city
stays as the contract's counterparty) and decides its own summer surge pool, ten medic units for the weekend
20:00 to 24:00 block from June to August, any it does not need offered to the county's mutual-aid roster for the
summer; the contract's deployment standard staffs so that on nine weekend evenings in ten the units can answer every
call in the block at 1.2 unit-hours a call, and from June dispatch sends any unit in a district to any call in it,
North (planning areas 1 and 2), Central (3 and 4) and South (5). The world, the decision and the quantity were kept.
The seed's own mechanisms (a filed staffing formula executed literally, the public dataset's suppression of one-
and two-call cells, a sentence telling the solver to pool the areas) were never candidates. Two decisive steps were
screened on code, each one of the brief's ideas in its strongest form, over three seeds each plus sweeps, and
neither held. No architecture is live. This note holds the screen record only; it carries none of the `precut.py`
sections, because no design exists. The prototypes stay in the session scratchpad (b179/screen:
`c1_pool.py`, `c1_summary.py`, `c1_station.py`, `c1_total.py`, `c2_level.py`, `c2_sigma.py` and `screen179.py`,
whose output `screen179.out` is byte-identical with `screen179_run2.out` over two runs).

**The structural sentence, and the first thing to read.** The quantity cannot carry a graded whole-unit call under
the bar, whatever the decisive step. A district's units at the 9-in-10 standard are the ceiling of 0.3 times the
90th percentile of its block calls over one summer's 39 or 40 Friday, Saturday and Sunday evenings, and the record that
estimates that percentile is at most nine or ten summers of those evenings: the golden's own bootstrap sigma is
0.40 to 0.91 units in every realistic world measured (1.51 at twice the size), against the 0.25 units a whole-unit
bin leaves once its quarter-bin margin is taken, and on one pack the defensible estimators of that percentile
spread 0.44 to 1.19 units; only small Poisson-dominated districts reach 0.24 and 0.22, where every lever on file
(pooling, co-movement, a trend, a break, a one-off) moves the call by at most one unit and the cheap routes land.
The total of the three districts is worse: its sigma is 1.09 to 1.19 units at the base world (`c1_total.py`).
And the one forward change this world really carries, district dispatch, is the estimand's unit: once the standard
names the district's block as what its units must answer, the district's own evening totals in the record,
filtered, summed and quantiled with a trend, are the golden family, which is the first thing a strong analyst
builds. A draw on this quantity needs a graded figure resting on many more events than one evening's percentile (a
season's unit-hours, say, which changes the seed's quantity), or another world.

**The registration finding.** Nothing was registered and no axis of the window was spent. The window moved during
the screen: at fa74407 it was task201, task247 and task165; at 2689b12 it is task165 (`council_or_assembly`,
`purchase_order_or_contract`, `local_government`, `operations_director`, `register`, `single-figure`,
`composition_mix`), task268 (`board_of_directors`, `launch_or_rollout`, `retailer_or_ecommerce`,
`operations_director`, `operations_log`, `14`, `composition_mix`) and task248 (`line_manager_or_team`,
`cutover_or_migration`, `government_agency`, `capacity_planner`, `monitoring_export`, `03`, `other`). The keys this
world offers honestly outside it, had a design held: organisation `hospital_or_health_provider` (a licensed
ambulance service), forum `customer_or_counterparty` (the city's EMS contract office receives the summer deployment
plan), forcing event `other` (the county's mutual-aid roster closing in May), context artifact `filed_standard`
(the contract's deployment standard), calibration `prior_period_close_out` (the summers' close-outs), shape `05`
(ten units across three districts, the rest released). The honest role is `capacity_planner` (the contractor's
deployment planner), which task248 now holds, and the honest strategies are `grain_or_unit` for candidate 1's
pooling reading and `forecast_method_backtest` for candidate 2, both free.

**The taxonomy finding.** The honest home is Healthcare Delivery & Health Economics,
`utilization-access-demand-forecasting` (ambulance demand forecasting; the client library's pattern 4 there, plan
capacity to an overdispersed quantile against a mean plus a Poisson margin, is this quantity exactly), or
`patient-flow-beds-workforce-optimization` (staffing to the standard). The urban-regional municipal-service cell is
held by task165's subdomain in the window.

**The repeat screen.** `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` ran before
any card, `slots` on the pooled-percentile driver, the level driver and the terms pooling, percentile, surge,
ambulance, medic and dispatch: no slot or card spent a pooled-percentile or a surge-pool level mechanism. The binding
matches are by the abstraction test: candidate 1's co-movement reading is task143's driver (a joint tail of a few
members whose error is mostly a component they share, the members treated as independent misstating it, the shared
component carried into the joint quantity), and its percentile-of-a-total reading sits beside task142 (an upper
percentile of a period's total built from the units that generate it). The brief's near drivers were read in full
on their cards: task148 (Erlang A with reneging in a 911 queue), task159 (platform backlog behind full trains),
task160 (regional waves timed by their lag) and task162 (version uptake set by the monthly restart burst); neither
candidate touches them.

## Tried and rejected

- **Candidate 1: the district's requirement read from the areas' joint evenings, against the closed summers'
  area-by-area staffing, the areas treated as independent, a square-root pooling law and a pooling discount** (the
  brief's first and second ideas; `c1_pool.py`, `c1_summary.py`, `c1_station.py`, `c1_total.py`, seeds 1, 2 and 3
  fixed before outcomes).
  Killed at stage 1 on measurement and on the estimand screen.
  - The world: five planning areas whose block calls are Poisson around a lognormal intensity carrying a city-wide
    evening factor (weather, events), a district factor and an area factor, Friday 0.95, Saturday 1.15 and Sunday
    0.88, 3 per cent a year; 2026 means 14, 12, 18, 10 and 15 calls a block; summers 2021 to 2026 (236 evenings),
    the truth simulated on 200,000 evenings of 2027.
  - The golden family on one pack (the district's evening totals rescaled to 2027 by their own log-linear trend and
    quantiled: type 7, type 1, Harrell-Davis, last three summers, area trends summed, additive rescaling, a negative
    binomial by weekday mixed): at the base world (city factor 0.15, district 0.05, area 0.10) North 10.92 to 11.22
    continuous units, Central 11.43 to 13.37, South 6.40 to 7.03 for the type 7 member, the family spanning two
    whole numbers in 6 of 9 district-seeds, a bootstrap sigma of 0.47 to 0.58 (North), 0.53 to 0.69 (Central) and
    0.38 to 0.44 (South).
  - The sweep, North and Central over three seeds (sigma, family spread on one pack, the area-by-area default's
    units above the golden, and how often independence and the square-root law land the golden's whole number):

    | World | Sigma | Family spread | Area-by-area | Independence lands | Square-root law lands |
    |---|---|---|---|---|---|
    | city factor 0.05 | 0.43 | 0.44 | +1.50 | 6 of 6 | 6 of 6 |
    | city factor 0.15 (base) | 0.58 | 0.62 | +1.17 | 3 of 6 | 4 of 6 |
    | city factor 0.25 | 0.71 | 0.88 | +1.33 | 5 of 6 | 5 of 6 |
    | city factor 0.35, area 0.15 | 0.91 | 1.02 | +1.00 | 0 of 6 | 0 of 6 |
    | nine summers (2017 to 2026 less 2020) | 0.40 | 0.61 | +1.50 | 5 of 6 | 5 of 6 |
    | twice the size | 1.51 | 1.19 | +1.67 | 0 of 6 | 0 of 6 |
    | small Poisson districts (means 4 to 6 an area) | 0.24 | 0.22 | +1.00 | 6 of 6 | 6 of 6 |

  - The lever at the truth: area-by-area staffing needs one unit more than the district in North and Central (13
    against 12, 8 per cent of the units a district needs), one or two at twice the size, none in South, against the
    brief's 30 per cent. Staffing station by station in the closed summers (three station areas a planning area)
    raises it to 29 to 33 per cent (16 against 12, 9 against 7) and changes nothing else below.
  - One dial: the independence and square-root routes miss only where the city factor is strong enough to make the
    golden's own sigma 0.91 units or more and the family spread a unit; where sigma falls toward 0.24 they land in
    every district-seed. No world puts both rivals a bin away while the golden holds a quarter-bin and one sigma.
  - The eda6c8c screens, as code (`screen179.py`): dispersion fires (the co-movement is estimated, and on one pack
    the family spreads 0.49 to 0.78 units); variance-only passes (area-by-area +0 to +2, independence -1 to +0, the
    point moves); the common-exposure subset fires in 6 of 6 district-seeds, since the district's own evening totals
    filtered, summed and quantiled are the golden, a filter and a sum with no model; truncation direction: blanking
    station cells of one or two calls (13 to 21 per cent of evenings carry one) leaves every district's units
    unchanged at an imputation of 0, 1, 1.5 or 2, so the suppression hides the bottom and is Layer 1 at most.
  - Why it is dead whatever the tuning: pooling is the estimand's unit (the district's block, which the standard
    has to file), so filing it makes the computation follow and the strong analyst's first build, the district's
    own totals, is the golden (rule 3, rule application); the co-movement reading is task143's driver; and the
    sigma floor above holds at every size.
- **Candidate 2: next summer's level against the record's, a trend, an accelerating district, a break and a
  one-off, each route priced in whole units and the route chosen on the 2025 and 2026 summers held out** (the
  brief's third and fourth ideas; `c2_level.py`, `c2_sigma.py`, seeds 1, 2 and 3 fixed before outcomes, then 101
  to 120 for the routes' own sigma). Killed at stage 1 on measurement. Built on small Poisson districts (2026 means
  North 16, Central 20 and South 11 calls a block, city factor 0.06) so that the percentile's noise is the smallest
  the world allows; summers 2018, 2019 and 2021 to 2026, spring weekends through April 2027.
  - The routes: the last summer flat; the last summer times the record's trend; every summer detrended; the last
    three summers on their own trend; the last summer times spring 2027 over spring 2026; a quadratic trend; the
    plain mean of the summers.
  - A, 3 per cent a year everywhere: Central's truth 9 units (8.10 continuous); the routes' means over 20 seeds
    7.36 to 8.42, their own sigma 0.19 to 0.45; on seeds 1 to 3, 5, 3 and 5 of the 7 routes land the truth's whole
    number; the back-test lands the truth in 13 of 20 and picks six different routes across them (every summer
    detrended 9 times, the last summer flat 4, the last three 4).
  - B, North's growth accelerating from 4 to 9 per cent a year from 2022: truth 8 (7.20); routes 5.40 to 8.31 on
    seeds 1 to 3, 2, 1 and 3 of them landing; the back-test right in 1 of 3.
  - C, Central 18 per cent lower from January 2025 (a diversion programme): truth 7 (6.90); routes' means 5.95 to
    7.17, sigma 0.15 to 0.48; on seeds 1 to 3, 4, 3 and 7 of 7 routes land; the back-test lands the truth in 17 of
    20, picking the plain mean of the summers in 8 of them (and on seeds 1 to 3 every time), which lands by
    cancellation (the break against the trend, mean 6.94).
  - D, South 20 per cent higher in summer 2026 only: truth 5 (4.80); only the plain mean lands (4.49, sigma 0.10),
    the flat hold once; the back-test lands the truth in 2 of 20 and never picks the plain mean.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply (a level, no suppressing
    threshold on the path); variance-only passes (on seeds 1 to 3 each scenario's routes spread 0.58 to 2.91
    continuous units); the common-exposure subset fires, since the summers already at the coming level, filtered
    and quantiled (the last summer, the last three on their own trend), land the truth in 8 of 12 scenario-seeds
    (all three of A and C, one of B and of D).
  - Why it is dead: the levers a trend, an 18 per cent break, a 20 per cent one-off and an accelerating district
    can buy are a unit or less on districts this small, against routes whose own sigma is 0.10 to 0.48 units (0.26
    to 0.48 for every route that carries a trend), so the flat hold, the plain mean and the last summer land, two
    wrong steps cancel (scenario C), and two held-out summers of 39 or 40 evenings cannot select the route (it lands the
    truth in 2 to 17 of 20 depending on the scenario). On larger districts the levers grow with the noise, as
    candidate 1's sweep shows.
- **Paper screens, not coded.**
  - Heat normalised over a long weather record: the lever is the record's weather sample against climatology,
    whose sign the draw sets, and the recent summers are the better guide to a warming climate, so the reading is
    contested.
  - A new venue's or team's weekend evenings on a filed event calendar: `composition_mix` (held by task165 and
    task268), the coming window's cells unfilled, and the venue's own event evenings filtered and divided hand it
    over.
  - A new development's occupancy: its occupied dwellings' rate times the forward occupancy is two filters and a
    divide.
  - An alternative-response or sobering-centre pilot going city-wide: a filed forward condition, the pilot
    district's own post-period evenings at the coming exposure, and a lever of a few per cent of block calls.
  - A frequent-caller programme and its regression to the mean: a lever of a few per cent.
  - Calls passed to county mutual aid or held when an area's units were all committed (capacity-censored demand):
    task168's driver, and a mutual-aid log that records every overflow call makes it a join.
  - The county's own units cut, so more of its calls overflow to the contractor (a loss model): task156's driver
    (work reaches a second tier only when the first falls short).
  - Hospital offload delays or cross-area travel lengthening each call under district dispatch: the 1.2 unit-hours
    a call is part of the filed estimand, and leaving it open makes the quantity a duration times a count,
    task142's driver.
  - Peak concurrency inside the block: task142's and task148's drivers, and the filed unit-hour standard does not
    ask for it.
  - Summing the block's hourly 90th fractiles (the demand-pattern reflex) or the stations' requirements: the
    estimand's unit again, which a strong analyst reads off the standard.
  - The predictive spread widened by next summer's own level shock: variance-only, the golden always above the
    plug-in, so a padding reflex lands it.
  - A summer-specific growth against all-year growth: a lever of a few per cent a year.
  - One 9-in-10 condition across the three districts jointly: the estimand again, and once filed the joint
    record's evenings answer it by a count.

## Resume

Do not re-screen anything above in this world. The binding finding is the sigma floor, which no decisive step
moves: a district's whole units at the 9-in-10 percentile of one weekend evening's block, read from nine or ten
summers, carry 0.40 to 0.91 units of the golden's own sigma in every realistic world, and the small districts that
get under the 0.25 budget leave every lever at a unit or less. The pooling the seed turns on is the estimand's
unit, and the district's own totals hand it over. The coordinator or the author decides whether the number is
redrawn on another quantity in this world (one that rests on many more events, a season's unit-hours rather than
one evening's percentile, which changes the seed's quantity), moved to another seed in the lane, or retired.
