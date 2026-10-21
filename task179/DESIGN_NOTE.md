# task179 design note

**Status: architecture v2 drawn 2026-10-21 in the round's second new cell, Epidemiology & Public Health,
`infectious-disease-transmission-modeling`, Forecasting.** The first cell (the ambulance surge pool, never carded)
and the redraw cell in Economics & Econometrics (`time-series-macro-econometrics`, never carded) are spent; their
records sit under `## First-cell record` and in `## Tried and rejected`. Re-screen nothing there.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task179.json`, architecture v2 (no earlier card exists; v1 is the
   uncarded first cell). `guard.py check` WARN only: `repeat.gate_g` against task479 (answered in item 5);
   `test.same_puzzle_older` and `test.same_driver_older` against task126, task138 and task82, differentiated on
   the card (a succession link split, a store rebuilt from inputs, records attributed through a second ledger;
   none reads a delay distribution from linked pairs). Redrawn under the registration lock after task178 entered
   the window: the decisive generator G13 became G3 and the context artifact `published_series` became
   `capacity_report` (item 5 and item 7). Nearest drivers 0.07 (task251 v4) and 0.06 (task192 v1,
   task452 v1, task199).
2. Pairing: Epidemiology & Public Health (client domain) / `infectious-disease-transmission-modeling` /
   Forecasting & Predictive Modeling. The one build on file in this task type is task501 (a next-generation
   matrix built from contact diaries of the season's own regime); nothing here touches a contact matrix, a regime
   of observation days or an eigenvalue.
3. Niche: Action Sante Lulonga (invented; no organisation of that name found), a medical humanitarian
   organisation running two Ebola treatment centres in Equateur province, projecting the cases its centres must
   plan for in epidemiological weeks 49 to 52 (30 November to 27 December 2026) under the provincial response
   plan's central scenario, from the province's line list and the response's contact-tracing chain register.
4. Call and shape: the number of new cases (confirmed and probable, by date of symptom onset) in weeks 49 to 52
   under the central scenario, to the precision the measured family supports (`quantity_figure`, `count`,
   question form how-many), with the four weekly figures and the current reproduction number as components. Shape
   `single-figure` (the call, its components and the ask tables; criteria counted in `## Ask sheet`); `other`
   and `10` are in the last two builds.
5. Mechanism keys: gap population (the chain register is not the population of transmission intervals, it is
   the subset whose case has already fallen ill) then time (the projection bets on the interval the chains run
   on, the register measures the intervals finished by its cut-off); generators G3 (record versus operation: the
   register's intervals against the interval the transmission process runs on) then G13 (each pair is observed
   only inside the horizon its source has to the extract). G13 led the first draft and task178 now holds it in the
   window; G3 is an equally honest reading of the step, and G12 (absence of a record) would also read. Gate G `forecasting`
   (a forecast the correctly read past does not pin): the WARN `repeat.gate_g` against task479 is answered by
   the honest key, `method_or_model_selection` would claim two methods pinned by a validation or a standard and
   here no validation or standard pins anything, the data's own truncation does. Strategy `maturity_censoring`
   (right truncation of a delay at the extract), free in the window (task486 other, task480
   decomposition_attribution, task479 other).
6. Layer 2: `estimation_fit` (censoring and truncation), pattern
   `epidemiology-public-health/infectious-disease-transmission-modeling/1` (Rt needs onset timing and the
   generation interval). The card is the textbook route and the default path takes it whole; the stump is the
   judgment it takes for granted, that the serial interval read from the outbreak's own pairs is the interval the
   renewal equation needs.
7. Furniture: forum `operations_desk` (the organisation's emergency desk commissions beds and staff directly on
   the planning lead's projection); forcing event `incident_or_complaint` (the outbreak, with the response plan's
   phase 3 starting 2 November); organisation family `hospital_or_health_provider` (a non-governmental operator
   whose role here is running treatment centres; `nonprofit_or_charity` would also read and is in the window,
   task486, said in the card's notes); role family `capacity_planner` (the medical planning lead); context
   artifact `capacity_report` (the treatment centres' weekly bed-capacity report the planning lead works from; the
   provincial weekly situation report also ships); calibration `none`. Free against
   task486, task480 and task479 on every axis.
8. Spine: the provincial line list as extracted on Sunday 18 October 2026 (one row per notified suspect,
   probable or confirmed case), constructed in the layout of a provincial surveillance export; the 25,000-row file
   is the contact follow-up log (contact by follow-up day).
9. Deliverables: `projection_mve_s49_s52.xlsx` (the projection, its components and the ask tables) and
   `courbe_projection_mve.svg` (observed and projected weekly cases with the scenario's start marked; SVG, since
   xlsx with png repeats task178's set).
10. World: Ebola virus disease (Zaire ebolavirus) in Equateur province, Democratic Republic of the Congo, first
    known onset 4 May 2026, declared in July, growing steadily since (doubling about every two weeks) to several
    thousand cases by mid-October across the Mbandaka, Wangata, Bolenge, Bikoro, Iboko, Ingende and Lotumbe health
    zones. The response plan's phase 3 (ring vaccination widened, a third treatment centre, safe burials scaled)
    starts Monday 2 November; its central planning scenario is that each case with onset from 2 November causes 40
    per cent fewer cases than cases did over the six weeks to 11 October. Personas from `guard.py names --geo
    "Democratic Republic of the Congo" --locale fr_FR --seed 179` (no locale is mapped for the country; the
    organisation's international staff carry French names): Valerie Francois (response epidemiologist, owner of the
    planning note), Thibaut Hebert (emergency coordinator), Colette Chauveau (treatment-centre medical lead).
11. As-of: the line list and chain register extracted Sunday 18 October 2026 at 23:59 (Kinshasa time, UTC+1);
    the provincial protocol closes notification within seven days of onset, so onsets to Sunday 11 October are
    complete; the projection is for weeks 49 to 52.
12. Sources read for the domain (stumping 1.3): the cell's two library cards (renewal-equation Rt with onset timing
    and the generation interval; the next-generation matrix's eigenvalue); task501 (a contact matrix pooled over
    two regimes; here no matrix); task232 (a transmission rate per exposure from closed episodes whose outcomes
    surface after a delay window; here the delay itself is the estimated quantity and the episodes are open);
    task181's lineage (a count read before its records finish arriving, units completed from their own arrival
    history; here the counts are complete and the intervals between linked records are what the cut-off bends);
    task133 (left truncation in a loan record; here truncation is on the right and by the later event); task91
    (young units that look dormant; here no unit's age conditions its outcome).
13. Data-native sentence: a source-to-case link is entered in the chain register only when the infected contact
    falls ill and is notified, and the outbreak doubles about every two weeks, so at the extract most sources are
    recent and are listed only with the cases they infected within the few weeks they have had, which bends the
    register's intervals short in exactly the cohort the renewal equation's growth window reads.

## Screens (stumping 1.2, as code)

Prototypes in the session scratchpad, b179e/screen (`a1.py` to `a4.py`, `e1.py`; seeds fixed before outcomes,
the outbreaks that died out before 2,500 cases skipped). The world screened is a discrete-day onset process,
offspring negative binomial (R 1.7, k 0.4), serial interval a discretised gamma (mean 12.6, sd 7.4 days), 62 per
cent of cases linked to a source, extract at day 165; eight outbreaks of 6,979 to 18,354 cases with 4,364 to
11,356 pairs. Figures are the projected cases in a four-week window starting five weeks after a 40 per cent cut,
each route against the golden (truncated maximum likelihood, gamma) on the same pack.

- The default family lands about a quarter low and tightly: every pair fitted (empirical or gamma) -27.2 per cent
  (sd 0.8), the same with the renewal-ratio R -27.0 (2.5), dropping pairs whose case fell ill in the last 21 or 42
  days (the hygiene reflex, on the case's clock) -27.9 and -26.9.
- The golden family converges where the data close it: truncated gamma 0.0, truncated Weibull +0.5 (0.1), the
  reverse-time nonparametric estimator 0.0, sources whose onset is 50 or 70 days before the cut-off (the
  complete-cohort subset, on the source's clock) +0.9 (3.0) and +0.3 (4.9). The lognormal reads +4.0 and the data
  reject it (negative log-likelihood 64 to 183 units worse than the gamma on every pack).
- The open residue is the current reproduction number's window and estimator: from the growth rate over 42 days
  it is the golden, over 28 days -0.1 with sd 7.4, the renewal ratio over the same 42 days +0.6 with sd 3.0. That
  is a knob, not the stump, so the window is filed (the six weeks to 11 October, weeks 36 to 41) and the spread of
  the two estimators on that window is measured on the cut pack before the rounding is set.
- Dispersion: the decisive quantity is a delay distribution's location; the parametric forms the data do not
  reject agree within 0.5 per cent and the nonparametric estimator within 0.1.
- Variance-only: the step moves the point (a quarter of the figure), it does not widen an interval.
- Common-exposure subset: the subset already complete, sources old enough that every case they caused has fallen
  ill, lands within its own sampling noise; choosing it means filtering on the source's onset, which is the
  decisive step itself. On the case's clock (the reflex) it lands the default.
- Truncation direction: the cut-off hides the top of the interval distribution (the long intervals), which is the
  case the screen keeps alive.
- Literature reflex: plugging in the West African 2014 serial interval (15.3 days, sd 9.3) lands +30 per cent;
  the planning note files that the projection rests on this outbreak's own chains.
- `guard.py slots --driver`: vocabulary hits only (task194, task190, task253, task117, task501); no slot records
  a truncated delay distribution or a serial interval dying.

## Default path

1. Daily onsets of confirmed and probable cases from the line list (suspects discarded after testing left out, a
   case notified twice kept once), complete to 11 October.
2. The serial interval from every source-to-case pair in the chain register: onset of case less onset of source,
   gamma fitted (mean about 11.5 days).
3. The current reproduction number from the growth of onsets over weeks 36 to 41 through that interval (about 1.6).
4. The renewal equation forward from 12 October, the reproduction number cut by 40 per cent for cases with onset
   from 2 November, cases summed over weeks 49 to 52.

Ends on: to be measured on the cut pack (about a quarter under the golden in every screened outbreak)
Golden: to be measured on the cut pack

## Stump sentence

A competent analyst fits the serial interval to every source-to-case pair in the chain register, takes the
reproduction number from the growth of onsets over weeks 36 to 41, cuts it by 40 per cent from 2 November and
projects about a quarter too few cases for weeks 49 to 52, because the register holds a pair only once its case has
fallen ill, so September's and October's sources appear only with the cases they infected quickly; read against
the time each source had to the cut-off, the pairs give the longer interval the chains run on, a higher
reproduction number and a December that holds instead of falling away.

## First-cell record

**First cell (2026-10-18).** New, Forecasting, seed FC50. The world was
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

- **Redraw cell, 2026-10-19: Economics & Econometrics, `time-series-macro-econometrics`, Forecasting.** The cell's
  three library cards (cointegration critical values, the Johansen rank's deterministic terms, shock identification)
  were read first; `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` (pass-through,
  asymmetric, invoicing, indexation, cointegration, error correction, recovery, seasonal, mortgage, lock-in, rent,
  catch-up, settlement, Phillips, kink, capacity utilisation) ran before any candidate. No build on file sits in this
  task type. The live window at a932f79 is task249, task177 and task270 (strategies `causal_design`,
  `forecast_method_backtest`, `population_selection`; patterns G14, G16, G12; task269 is spent and skipped). Prototypes
  in the session scratchpad, b179r/screen: `s1_cp.py`, `lm1.py`, `d1.py`, `w1.py`, `w2.py`, and `screen179r.py`, whose
  output `screen179r.out` is byte-identical with `screen179r_run2.out` (as `lm1.out` is with `lm1_run2.out`). Seeds
  were fixed before outcomes. No card was drafted, because nothing passed the measurement.
  - **Measured: a business survey's up, same and down shares against the quarter's mean output move** (the balance
    bridge against a quantification that scales the shares by the firms' spread, Carlson-Parkin; `s1_cp.py`, 20
    world draws a scenario, 1,500 firms a quarter, 127 quarters, t(5) firm growth). At ordinary spread the balance
    bridge lands (truth -1.0: balance -0.86, golden -0.98); only a deep fall at an unprecedented spread separates it
    (truth -3.0 at spread 12: balance -1.80, the up-and-down two-share regression -2.55, golden -2.89 with a sd of
    0.35, 12 per cent of the figure). The nearest reflex sits about one golden sigma away, the golden's own sigma is
    an order above the bar, and the separating world needs a recession no record has seen.
  - **Measured: long memory, a fractionally integrated series against the AR chosen by AIC and the KPSS-chosen unit
    root** (`lm1.py`, 40 draws, d 0.4, 480 months, the mean of months 25 to 36). The AR by AIC, the AR(1) and the
    estimated-d forecast agree (mean absolute errors 0.605, 0.593 and 0.599 sd units, the random walk 0.936), and all
    three miss the truth through the sample mean's own long-memory error (correlation -0.89 to -0.93 with it). No
    lever between the textbook route and the golden: the residue is the mean, not the method.
  - **Measured: national excess unemployment twelve months on when the shock sits in the slowest regions** (bottom-up
    regional persistence against the national AR; `d1.py`, 30 seeds, eight regions at monthly persistence 0.90 to
    0.985). The national AR understates the remaining excess by 0.108 (24 per cent of 0.459); the bottom-up AR(1)
    overshoots by 0.087 with a sd of 0.085, so the golden's own error is the size of the lever, because forty years
    of monthly data pin a near-unit-root persistence too loosely. By abstraction it is also composition weights that
    moved (task95, task446).
  - **Measured: new collective agreements' annualised increase once a long pre-surge wave expires** (the catch-up of
    real pay lost since each agreement's own last settlement; `w1.py`, `w2.py`, seeds 1 to 5, about 13,600
    agreements over 2000 to 2027). On the 2027 approvals the trailing-inflation regression lands within 0.15 to 0.50
    points (2.50 against truths of 2.64 to 3.00, 5 to 17 per cent); the symmetric catch-up regression misses as
    badly (2.20 to 2.57) and only an asymmetric catch-up lands (2.61 to 2.95), so the decisive step became the
    asymmetry, a 0.4-point split inside the golden family against the lever. Catch-up since the last settlement is
    also the first thing a labour economist checks after a surge, a cousin of task165's gain conditioned on each
    unit's own baseline, and the settlement regression is panel estimation rather than this task type.
  - Paper: invoicing-currency (dominant-currency) pass-through into import prices is task145's driver (units differ
    in which currency they hold fixed), and task153 rejected its pass-through cousins.
  - Paper: asymmetric error correction in a retail price (rockets and feathers) is the adjustment-speed cousin
    task153 rejected.
  - Paper: phase-asymmetric unemployment (steep rises, recoveries at a steady log pace) against a linear AR: a gap
    closing at a fixed pace rather than in proportion is task161's driver (own-use burn against a half-life), its
    honest strategy `forecast_method_backtest` (a regime) is in the window (task177), and the pace of past
    recoveries, the natural analogue, is the golden.
  - Paper: a rent index under a cap on sitting-tenant increases with vacancy decontrol (a backlog drawn down at the
    cap, a nonlinear error correction): fixed-rate drawdown is task161's driver and the saturation task79's, and once
    the cap is filed the sitting tenancies' path executes it.
  - Paper: a convex price response to capacity utilisation read from an industry panel is task79's kink (task149
    rejected the same).
  - Paper: mortgage-rate lock-in holding down housing transactions and transfer-tax receipts is task166's driver
    (units whose own rate the terms beat).
  - Paper: a moving lunar holiday (Ramadan and Eid) in a monthly flow or in banknote demand is task162's
    calendar-locked alignment, and a strong reader models it.
  - Paper: a reset-month step in a price index sized by trailing inflation (state-dependent seasonality from annual
    indexation), and year-end appropriation spending sized by the unspent balance: both task146's driver (a step at a
    calendar turn is not a fixed seasonal share).
  - Paper: downward nominal wage rigidity bending aggregate wage growth: at plausible desired growth for 2027 (1 to 3
    per cent, a worker sd of 3) the floor moves aggregate growth 0.09 points from a linear extrapolation, and
    aggregation over a per-unit floor is task16's driver.
  - Paper: cointegration and error correction against a VAR in differences or ARIMA, including the partner that
    reveals a shock's permanence and a trend in the cointegrating relation: the cell's own cards 1 and 2 applied as
    stated, which the library test says a blind reader lands; where the golden is no reversion, ARIMA lands it; and
    `coint` applies MacKinnon's critical values by default.
  - Paper: signal extraction from a sampled series: IMA(1,1) is the optimal filter for a random walk plus noise and
    lands, and autocorrelated sampling error needs the filed design variance (rule application).
  - Paper: a minimum wage's effect through its bite is task165's untreated part; the shadow rate at the lower bound
    is markets and lending ground, with a rule fitted on off-floor quarters both the default and the golden; an
    uncertainty hold on a trend-growth revision (HAC against iid) fails the variance-only screen; inventory payback,
    the accelerator and the carry-over are accounting a strong reader states; tariff diversion to untariffed origins
    is a product-panel elasticity outside this task type and close to task88's displacement.
  - The cell finding: the field's textbook routes (ARIMA, VAR, VECM, bridge, X-13) are routes a blind reader takes,
    and every structural judgment beyond them that this search found is either a driver on file by abstraction
    (fixed-pace drawdown, a kink, a calendar turn's step, a conditioned gain, a moved mix, a lock-in, pass-through)
    or, where it is new, carries a golden whose own sigma (12 per cent, 18 per cent of the figure) or family split
    is the size of its lever, because macro aggregates rest on too few independent events. Micro registers give the
    precision and move the work out of this task type.

## Resume

Architecture v2 drawn 2026-10-21. Next: the generator's world and pack, the measured default and golden on the cut
pack, the asks and their devices, then the stage 2 sections (three rules, readability screen, fork table, ladder,
closure table, literal reader, oracles, ask sheet) and `precut.py`.
