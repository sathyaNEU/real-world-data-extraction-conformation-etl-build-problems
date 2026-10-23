# task173: Hollis Bend Water Utilities' 2027 utility-side service leak repairs, the year its AMI contractor exchanges two thirds of the city's meters (architecture 3)

**Status (2026-10-23).** Reopened by the author for a from-scratch rebuild (`## Retired`, `## Rebuild (2026-10-23)`).
Architecture 2 (load forecasting) is spent at Gate F and the psychology and human-reliability cells died at stage 1;
every world, cell and mechanism in `## Tried and rejected` is spent and is not re-screened. Architecture 3 is drawn in
`energy-systems-utilities` / `asset-condition-maintenance` (Forecasting), chosen shape first (below).

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v3 (v1 and v2 in `lineage`, v2 marked spent) |
| Domain / task type | `energy-systems-utilities`, task type `asset-condition-maintenance` (serves Forecasting): the deciding quantity is the count of buried service failures a water utility's crews will repair in 2027, a failure hazard per service carried to a year in which most services are worked on |
| Objective | Forecasting & Predictive Modeling: utility-side service leak repairs completed in calendar 2027, a window not yet open; records run to 30 September 2026 |
| Shape | `02`, a forecast with its history: the call (the 2027 count) and the asks' grids over the record (criteria in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `count`: the estimated quantity of service leak repairs in the 2027 service repair and restoration term contract |
| Mechanism | gap time (decisive: the record spreads meter exchanges thinly, about one meter in twenty a year, and the forward year exchanges about two in three within six months), with population (the 2027 service-months sit mostly inside the weeks after an exchange, where the record has few); pattern none; generators G2 (decisive: the unit the failure rate is read on is each service's own exchange visit and the weeks after it, not the service-year, its route or its street), G7 (when the induced failures can happen is pinned by an operations file, the AMI deployment schedule), G6 (the forward year's service-months move to the post-exchange state); Gate G `forecasting`; strategy `causal_design` (a transient risk window after a discrete visit, identified on each service against its own baseline) |
| Layer 2 family / pattern | `estimand_identification` (which exposure the failure rate is read on); `own:work-induced-failure-risk-window-carried-to-a-mass-meter-exchange` (Energy carries no client cards; the five families and the nearest domains' cards are the seeds) |
| Furniture | forum `council_or_assembly` (the City Council awards term contracts above the purchasing threshold on the estimated quantities), forcing event `purchase_order_or_contract` (the 2027 service repair and restoration term contract goes to bid with estimated quantities), organisation `local_government` (the utility is a department of the City), role `operations_director`, context artifact `other` (the bid schedule of estimated quantities), calibration `none` |
| World | Hollis Bend, a fictional Texas city of about 380,000 on shrink-swell clay; Hollis Bend Water Utilities, a city department, about 140,000 metered services with meters in curb boxes on setters with angle valves; meters exchanged at end of life by the utility's meter shop (and in 2022 by a contractor clearing stopped meters); a 2026 AMI contract exchanges every pre-2019 meter February to July 2027 and fits radio endpoints to the rest. All fictional; the field's method is real |
| People | `guard.py names --geo us --seed 173`: Mario Barnett, Heidi Snyder (Michelle Russell dropped on a people.first WARN) |

**Why this cell, shape first.** The shape that held this round is a forward population sitting at one end of an
exposure the record measures at a finer grain than the textbook model uses, the right exposure chosen by fit (task175),
or a structural estimand choice the textbook route does not make (task169). In buried-asset failure forecasting the
textbook route is a failure rate per asset-year by material, age and environment carried to the forward inventory;
the judgment it takes for granted is what exposure the failures are read on. Here the forward year is the end of an
exposure (work on the service) that the record holds only thinly, and the exposure is visible only by linking each
service's leaks to its own meter history.

**Data-native sentence.** In Hollis Bend a meter exchange means closing and reopening a decades-old angle valve and
breaking and remaking the setter's couplings in a clay-filled box, and about one exchange in a hundred leaks within
weeks, while the record's routine exchanges touch only about one meter in twenty a year, so the leaks per service-year
the record shows carry almost none of what the 2027 exchange of two thirds of the meters sets off; the induced chance
is readable only on each service's own record, its leaks in the weeks after its own past exchanges against its own
baseline.

**Screen measured before the card** (`scratchpad/b173s/proto/s1b.py` to `s1d.py`, 140,000 services, 2012 to 2026,
about 60,000 routine exchanges and 16,000 leaks, four seeds): the default (leaks per service-year of the last two
years) files 0.53 to 0.57 of the 2027 expected truth; the golden family (the per-exchange excess over each service's
own base inside a 120, 180 or 365 day window, with the delay profile applied to the 2027 schedule) sits at 0.98 to 1.05
of the truth across seeds and within 1 to 3 per cent of itself within a seed; windows of 60 to 90 days without the
delay tail file 0.89 to 0.96. Final magnitudes are set on the generator (`## Ladder`).

## Guard

`guard.py check`: WARN only (`overuse.objective`, `overuse.gate_g`: the lane's objective and its Gate G;
`repeat.decision` quantity_figure and `repeat.question_form` how-many against task176: a count of repairs is a
quantity and asks how many; `repeat.deliverables` xlsx and png against task175: a forecast workbook and its chart).
Axes redrawn at the probe and under the registration lock, each on the axis the guard named: forum
`council_or_assembly` first blocked against task274 and `board_of_directors` against task177, then `executive_team`
blocked against task175 once task274's card was spent; the City Council awards term contracts above the purchasing
threshold, and with task274 spent that forum is open again, so `council_or_assembly`. Organisation
`utility_or_infrastructure` blocked against task175: the utility is a department of the City, `local_government`.
Pattern G6 blocked against task175 and G14 against task176: the decisive rung is the unit the rate is read on (each
service's own visit and the weeks after it), G2, with G7 and G6 kept beside it. Context artifact `planning_thread`
blocked against task171, so `other` (the bid schedule). Same-puzzle and same-driver signatures differentiated on the
card against task125, task150 and task501 v3, with lines against task132, task149, task177 v3, task183 and task480 v1.

**Abstraction test.** Nearest drivers task149 (hazard per unit of working time against the pace of work, 0.10),
task183 (a part's own failure history as a frailty, 0.10), task111 v1 (a failure's originating delay in earlier work,
0.07), task132 (a wear curve reset by replacement, 0.07). None raises a unit's hazard for weeks after a discrete visit
of work to that unit and carries the visit count of a forward window; task480 v1 read old meters' under-registration at
their exchange, which is what the meter recorded, not what the visit set off.

## Default path

1. Stitch the legacy work orders (to May 2021, by street address) and the new CMMS (from May 2021, by GIS service
   ID), keep utility-side service leak repairs, one per leak (its repair work order, not its investigation or
   restoration orders).
2. Count completed repairs per year; take the last two full years to 30 September 2026 (or fit a model of each
   service's leaks per service-year on material, install era and pressure zone).
3. Carry the rate to the 2027 inventory, net of the services the 2027 capital program renews.

Ends on: about 1,100 repairs (prototype; set on the generator)

Golden: about 1,950 repairs (prototype; set on the generator)

## Stump sentence

A competent solver carries the service leaks per service-year of the record, or a model of them on each service's
material, age and pressure zone, to the 2027 inventory and files about 1,100 repairs, because it never reads a
service's failures on its own exchange visits: an exchange operates the old angle valve and remakes the setter's
couplings and leaks within weeks about once in a hundred visits, the record's routine exchanges touch one meter in
twenty a year, and the 2027 AMI contract exchanges two meters in three in six months, which puts the year at about
1,950.

## Tried and rejected

- Lazy abandonment in the 2026 simulation (a customer's patience checked only when an expert came free): it pushed a
  retry before the clock and one expert served two customers at once; abandonment and the queue's close are now events
  in time order, asserted (no event out of order, no overlapping interactions).
- Demand at the 2026 scale of 1.03: the 2026 fortnight served more new cases than the 2027 plan, an implausible fall; the
  2026 scale is 1.00 and the plan grows 3.4 per cent on the CRM's count.
- A graded figure for the fortnight's forecast contacts to the nearest thousand: its constructions spread 400 contacts
  and the golden sat within 100 of a cell edge at every placement the booking allowed; dropped from the prompt, kept in
  the workbook as working.
- Shrinkage at 11 per cent with a handle-time ramp of 0.47: the nearest flat-haircut rival landed the block; the ramp is
  0.455 and shrinkage 12 per cent, every canonical haircut now orders another block.
- Ask B as counts of customers answered after more than three minutes by day: the connect time flips too few customers
  on the quiet days after the deadline, so the cracker landed 2 and 3 May; the daily average wait moves every day by 9
  seconds.
- Crashes drawn per agent-day at a flat rate: some days had none, so the cracker landed them; each day now has at least
  three planned and a blocked one retries later in the shift.
- Hillsborough's Sunday shifts ending at 22:00: one contact ran past 23:00 Eastern, Atlantic midnight, and the invoice
  weeks read in Atlantic and Eastern time split by 0.08 h; Sunday shifts now end by 20:30.
- Frozen sessions all lasting exactly the 90-minute timeout: a uniform organ; team leads now force some out after 10 to
  75 minutes, and the timeout carries the heartbeat's 30 seconds.
- Personal Not Ready of 3 to 8 minutes: put 25 April's billable time on an exact rounding tie (209.05 h); 2 to 9
  minutes, every Ask A figure now clears its tie.
- An invoice header with a street address and an HST registration number: invented details that could match a real
  business; dropped.
- Registering after task165's DRAWN (23bd05a): `guard.py check` on 18 October blocks on the last-three bans on G14,
  `composition_mix` (task165), forum `executive_team` and forcing event `vote_or_meeting` (task247), and beyond them on
  `test.same_puzzle` and `test.same_driver` against task165 in the twelve-build window. Putting G6 first would clear the
  two tests and was rejected as a relabel of a real kinship (both builds carry a conditioned yield to a new mix); stage
  3 is built in scratch and committed without a card, which registers when task165 has left the window.
- Architecture 1 (Ashdale Tax Live's deadline-fortnight outsourcer booking, comebacks set by whoever opened each case) abandoned unregistered on 22 October: the guard's window blocked it for three days on `composition_mix`, G14, `filed_standard`, `executive_team` and `vote_or_meeting` while other lanes kept drawing those axes, and the author chose a fresh draw in a new world rather than wait; nothing of its world, mechanism or blocked axes is carried.
- Redraw cell 1, candidate A (a hospital's ALC census, its patients awaiting long-term care leaving at a fixed weekly placement count set by the region's vacancies, cut after a home closed, while other ALC exits leave in proportion to the stock; default path Little's law on the 12-month ALC stay): measured on the clean truth over 4 seeds (`proto_a2.py`), the textbook rivals bracket the golden instead of missing it on one side (Little on 12-month stays 98 to 128, Little on 13-week stays 150 to 209, occupancy over arrivals 103 to 197, Holt-Winters on the weekly census 112 to 156, against golden 120 to 171), and the golden's own spread from the post-closure placement rate alone is plus or minus 3.5 per cent at one standard error; the closure recency that separates Little's law from the count model is the same dial that starves the post-closure rate, and a census time series is a random walk with drift exactly where the placements are a count. Dead.
- Candidate B (the same placements shared at random across five hospitals' waiting lists, so another hospital's filed rise in designations lengthens every hospital's wait): measured over 3 seeds and two shock sizes (`proto_b.py`), Little on the hospital's own 12-month hazard lands at 32 to 54 against golden 35 to 53, again on both sides, with the golden plus or minus 3 per cent on the pooled placement rate; the spillover moves the level by about 15 per cent, under the 30 per cent the bar needs. Dead.
- Paper screens on the same cell, each killed before a harness: the holiday discharge backlog (the 2026-27 Christmas and New Year run of no-discharge days matches 2025-26 and 2023-24 within a day, so the seasonal naive on aligned dates carries it; `time_semantics` besides); length of stay that shortens with occupancy (the slope's estimator family is open and confounded with season); ED diversion by geography after a neighbour closes (nearest-hospital allocation is the cheap twin of the choice model, one dial); a census capped at staffed beds (the latent demand is either the boarders' count, a population reading, or arrivals times stay, which is the default path itself); new Saturday operating lists (no Saturday surgery in the record, so the weekday discharge model is extrapolated and the family forks); nursing workload from turnover (lever under 10 per cent); float-pool pooling and sickness moving with demand (the empirical daily percentile reaches the golden); a discharge-count cap first binding in the forward peak (the driver of task156, task159 and task172); a transitional unit's 60-day stay limit returning patients (task172's deadline); follow-up echoes of a new-patient surge (task157 and architecture 1's comebacks); nurse retirement at a pension eligibility date (a teachers' plan reads the same, rule 1 fails).
- Redraw cell 2, candidate C1 (a discrete cohort mortality step, the cohorts born 1944 to 1947 carrying 25 per cent excess mortality at every adult age, against Lee-Carter fitted on 1995 to 2025 and a fixed 1.5 per cent improvement; `proto_c.py`, expected values, a fictional country of about 20 million): on the deaths at 75 to 89 in 2027 to 2031, the planning quantity, Lee-Carter files 0.990 of the truth and the fixed improvement 1.012, a one per cent lever, because the step sits on four cohorts among fifteen; it reaches 20 per cent only on the cohort's own ages (83 to 86 in 2030), a quantity no decision funds, and grading it needs the cohort effect separated from age and period, the APC identification fork. Dead on lever.
- Cell 2 paper screens, each dead before code: oldest-old register over-coverage rebuilt by extinct cohorts (already dead twice, task228 candidate 2 and task271's re-root screens, not re-screened); mortality displacement after a severe 2025 winter (one to two per cent of a year's deaths, sized from a handful of past shocks); tempo and recuperation in period fertility, and second births echoing a first-birth surge (task176's paper deaths, not re-screened); depletion of the childless pool after a pulled-forward first-birth wave (about 4 per cent of a year's births, and the time-since-entry family); select mortality in a recently enrolled group (a hazard by time since entry, task468 and task134 v2); exposure bias where adjacent birth cohorts differ sharply in size (a local, sub-per-cent move on any planning total); late registration of inquest deaths at young adult ages (the standard truncation correction, lesson 1 of this round); incomplete death registration estimated by the death distribution methods (a coverage defect, the judge's planted-defect list, as task228 found); the first year deaths exceed births (the difference amplifies the golden family's spread as much as the lever); Lee-Carter's rotation, jump-off and fitting window, and cause-specific forecasting (method forks); a disability-free life table by Sullivan against a multistate projection (prevalence as incidence times duration, cell 1's bracketing death in other nouns); a once-in-sixty-years zodiac dip in births (a single past event).
- Rebuild (2026-10-23), cell `energy-systems-utilities` / `load-forecasting`, paper screens killed before a harness:
  large customers chasing a coincident-peak charge that a 2027 tariff removes (the add-back is the field's known 4CP
  correction and a null region publishes it: the non-alert days are the uncurtailed load); heat build-up over a
  heat wave's days (a lever of 3 to 6 per cent of a peak, and the lag family forks); dual-fuel heat pumps losing gas
  when a gas network is decommissioned (the pre-emption shows in the hybrids' own cold-day load, and the all-electric
  homes publish the answer); rooftop PV export limits raised under a minimum-demand forecast (task136's PV world in the
  same cell, and unclipping a known limit is the reflex); suppressed demand after rotating outages end (the restoration
  rebound is task131's driver); a direct load control programme ending (task131 again, and the non-event days are a
  null region); a district cooling plant with ice storage closing (contrived, one plant); data-centre cooling load by
  design (a visible attribute, stratified by reflex); prepaid metering conversion (stratify by payment type);
  efficiency savings embedded in the trend (about one per cent a year).
- Candidate P1 on code (`proto_p.py`, `proto_p2.py`, 12 seeds): senior plants with separate well and river-lift meters.
  The lever held (the bench wells' fitted energy per curtailed acre-foot carried over filed 1.44 to 2.31 times the
  golden), but each senior well's energy per acre-foot was then one divide of two shipped files (its bills over its
  metered extraction), a single-purpose route to the golden; the wells were moved onto the river lifts' meters, as the
  bottomland plants are built, so the pair has to be fitted (`proto_p3.py`: per-plant fit, pooled fit and the
  separate-plant average within 0.25 GWh of the truth over 16 seeds).
- The decreed allotment against the water actually diverted (the cut is the diversion above a quarter of the
  allotment, not three quarters of the allotment): kept only as a lower rung, because the order files the limit and
  applying it to each right's statements is rule application.
- Architecture 2 (Varner Valley PUD's 2027 Apr-Sep irrigation pumping under the first senior curtailment, bottomland plants a river lift and a well on one meter) spent 2026-10-23 at stage 4 on zip be677673 (Gate F): blind reader A filed 155,000 MWh, the golden, by the path "345 river lift plus well services: energy = a x diverted AF + b x well AF per service (fit 2017-2026) ... Diversion capped at 25 percent of allotment, balance pumped from the service's own well"; reader B filed 130,000 (it read the cap as leaving the land unirrigated). Both readers hit all 56 ask figures: the check meter repeating each revenue meter one interval early was dropped as a duplicate, and the meter clock's missing DST gap gave its standard time away. The judge returned DETERMINISTIC with one FIX_NOW (which meter in each pair is the revenue meter) and warned that the plant strings "RIVER LIFT + WELL" invite the two-source fit. Lessons: a plant description that names both pumps makes the per-service two-regressor fit a reflex, so the decisive quantity was named in the pack; a duplicated series and a clock with a tell-tale gap are visible hygiene and keep nothing.
- Third cell, chosen by this build after architecture 2's Gate F death: `psychology-behavioral-science` / `decision-making-computational-behavioral-modeling` (Forecasting), task177 v1's driver (imposed experiences in a learner) avoided. Why the cell: the field's own quantity, a reference-dependent stopping rule, is read from within-shift choices, no field or string names it, and a pay standard moves every worker's stopping point in a way no shift in the record ran. `guard.py check` on a probe card passes the pairing (its BLOCKs were the probe's own axes, G3 and `capacity_planner` against task169, and the older same-puzzle tests without a differentiation line). Candidate Q1 on code (`proto3/q1.py`, `q1b.py`, scratchpad b173n, 3 and 2 seeds): a food-delivery platform's 19:00 to 23:00 courier-hours after a per-order base fee rise, targeters stopping at the first drop-off past their own day's amount, clock couriers at their planned end. With the base fee from 4.10 to 5.00 (earnings per order up about 11 per cent) and 55 per cent targeters, the late hours fall 8 per cent and the courier-FE elasticity route (minus 0.30, division bias included) files 1.05 times the truth; the lever reaches 32 per cent only with the fee nearly doubled and three quarters of couriers targeting, and the record-only reconstruction of each courier's rule then sits 2 to 3 per cent off the truth. The lever is bounded by the size of the pay change, and the textbook elasticity already moves the right way. Dead.
- Third-cell paper screens and the untouched Forecasting cells beside it, each dead before code: an infectious disease's post-campaign season by the final-size relation (the nonlinearity that makes the lever is the sensitivity: near an effective R of 1.2 a 1 per cent error in R moves the season about 5 per cent, and R and the season-start susceptible share are separately identified only from season-to-season variation, so the golden family spreads past any bin); vaccine effectiveness waning under an earlier campaign (a test-negative record's per-bin effectiveness carries 2 to 3 points of sigma, and campaign timing against waning is the field's open debate a reader raises unprompted); household prophylaxis courses counted per index household (counting households with a case by address is the natural route); stress-test losses convex in unemployment (the logit or probit transform forks, and either is the satellite model's textbook); a percentile of a summed demand under cross-site dependence (resampling whole dates is the natural route); a housing-led small-area projection (net migration regressed on completions, the obvious covariate); a redistricting stripped of incumbents' personal votes (election-polling, excluded by task179's `## Rebuild`); monthly subscribers forced onto annual billing (the per-decision churn hazard does not transfer identified). Infectious disease's two earlier drivers (task179's truncated serial interval, task501's next-generation matrix) were not re-screened.

- Fourth cell, assigned 2026-10-23: `human-factors-ergonomics` / `human-reliability-assessment` (Forecasting), read against task149, task171, task175 and task176's deaths in this task type and task230 v2's driver (detection falling with a shared pool's prevalence), all avoided. Candidate R1 on code (`proto/r1.py`, scratchpad b173h, one seed, 580,000 runs and 15,300 events): a train operator's overspeed events per run rising with the days since the driver last drove that route (route-knowledge decay, truth g = 0.95 + 0.30 ln(1 + days/4)), the December timetable merging two depots' links so every driver signs twelve routes instead of seven. The lever is bounded by the merge: a driver's gap on a route goes from about 6 to about 10 days and about half of all runs are a second or third run of the day at zero recency, so the route-rate default files 0.971 of the truth and the pooled rate 0.981, against a golden family (route by recency bins at three binnings, log-recency fits) at 1.007 to 1.023; the HEART-style binary unfamiliarity split at 14 days lands 1.000. Even a tripled route set with a steep decay moves first runs about 40 per cent and all runs about 20. Dead on the lever, which the size of the roster change caps.
- Candidate R2 on code (`proto/r2.py`, `proto/r2b.py`, three seeds, 596,000 to 599,000 runs): a ten-week blockade of the main line diverting its services over a diversionary route the drivers keep signed but drive only on engineering weekends (every three weeks), the diversion's own base 1.8 times the main line's, truth amplitude 1.2 and decay 25 days; graded the overspeed events on the diverted services (truth 190 to 327). The default (the diversion's historical rate per run) files 1.28 to 1.38 of the truth and the main line's rate 0.53 to 0.58, but the golden family (route by recency bins, three binnings and a coarse one) sits at 1.013 to 1.149 of the truth across seeds (the diversion's base is read from 350 to 680 events, all at long recency, so its own scatter is about 5 per cent), leaving the default only 23 to 26 per cent above the golden; the parametric decay forms spread 0.98 to 1.25 with the likelihood picking the true decay; and the attaining subset, the diversion's own runs at 7 days or less (the second day of a weekend, the return run), files 0.92 to 1.09 of the truth, 4 to 10 per cent from the golden, a filter and a divide once the recency is built. With a three-week analogue closure in the history its rate by week of closure carried the call besides. Dead on the subset screen and the lever.
- Candidate R3 on code (`proto/r3.py`, three seeds, 8,760 shift records and about 1,300 errors in three years): a gas control centre's operator errors as slips per switching operation plus monitoring lapses per console-hour, the forward roster moving four desks on 12-hour shifts to three consolidated desks on 8-hour shifts, the duty cycle unlike the history's. The two single-exposure routes bracket the truth at 1.10 to 1.17 (per operation) and 0.81 to 0.87 (per hour), levers of 13 to 17 per cent, under the 30 the bar needs; with every history shift at 12 hours, a regression on operations leaves its intercept readable per shift (1.13 to 1.21) or per hour (0.93 to 1.05), a form the data cannot settle; with relief shifts of 8 hours in the history the two-exposure fit lands within 4 to 6 per cent, which is the two-regressor fit a medium reader took on architecture 2, and the golden's own scatter is about 4 per cent on that error count. This field's reflex (a human error probability per opportunity) does not split the two, but the data either split them for any regression or not at all. Dead three ways.
- Fourth-cell paper screens, each dead before code: errors by hour of day under a timetable moving work into the night (a stratification on the timestamp, the reflex); handover-related errors under the 12-hour to 8-hour change (the time-on-shift curve inside its observed range, task171's shift death); a workload U-curve at a consolidated desk (the forward load sits outside the record, a form fork); an error taxonomy that types slips and lapses (the split is one group-by, then each type on its natural exposure); a plant-specific HEP updated from a generic prior (a level at a selected unit, the shrinkage law); latent pre-initiator miscalibrations under a surveillance-interval extension (a regression on the interval since the last test, the obvious covariate, and equipment reliability more than human); simulator-derived HEPs for a PSA human failure event (which runs are demands is the estimand's population, the WHAT screen); steps of a procedure lengthened under a new work plan (task176's paper death, the condition in the record or its curve extrapolated). The cell's recurring death: in human reliability the forward condition either moves a performance-shaping factor the record already spans (the attaining subset, or the reflex stratification once the factor is built) or moves it outside the record (a form fork), and the roster or plan changes that are realistic move the factor too little for a 30 per cent lever.

- Rebuild cell 5, chosen by this build shape first on 2026-10-23 (`energy-systems-utilities` /
  `asset-condition-maintenance`), after these directions died on paper in the search: sewer blockages from food
  establishments upstream under a 2027 bypass (grease from restaurants is the field's best-known cause of blockages,
  and the bypass names it); deposit runoff by salary-credit primacy (the field's stable-deposit definition names
  primacy); lapse at the end of a level-term period by premium jump (the post-level-term studies tabulate it); rent
  index lag through the lease stock (the new-tenant rent index is the field's known lead); retirements at unreduced
  eligibility (experience studies tabulate rates by eligibility, and the plan rule is filed); water main breaks after a
  worst-first replacement (a level at selected units, the shrinkage law); fibre take-up by competitor presence (the
  forward areas' defining feature names the covariate); involuntary lapse at card expiry (a calendar-locked trigger,
  task162 by abstraction).

## Retired

**RETIRED 2026-10-22 under this round's rule that a number which dies in its second new cell is retired.** Three
worlds were screened at stage 1 and none held:
- the seed's world (Ashdale Tax Live), architecture 1, built in scratch but never registered, abandoned for a fresh draw
  after three days blocked by the guard's window;
- redraw cell 1, healthcare delivery patient flow (Forecasting): candidates A and B on code, twelve on paper; a
  count-limited exit lands between the textbook routes, not outside them;
- redraw cell 2, sociology and demography life tables (Forecasting): C1 on code, fourteen on paper; national vital
  counts give sigma near one per cent, but every structural judgment the textbook routes take for granted moves a
  planning total by a few per cent, or is a coverage defect, a future-rate assumption or a spent driver.

No card was ever registered, so no guard axis is held. The screens above are the number's record for `guard.py slots`.

## Rebuild (2026-10-23)

Reopened by the author for a from-scratch rebuild under the rule that no number stays retired; architecture 2 drawn
in `energy-systems-utilities` / `load-forecasting` (Forecasting), card v2 registered, `pipeline.json` architecture 2.

Architecture 2 spent at Gate F on be677673 (`## Tried and rejected`). The coordinator then left the next cell to this build under four conditions (a forward window that changes the process in a way not on file, no field or plant string naming the decisive quantity, no ask device that is visible hygiene, every listed cell excluded). Chosen: psychology-behavioral-science / decision-making-computational-behavioral-modeling, for the reason in `## Tried and rejected`; Q1 measured dead on code and eight more directions dead on paper. No card registered for it; v2 stays the card's identity, marked spent. PAUSED at stage 1 for another cell.

Fourth cell (assigned by the main session): human-factors-ergonomics / human-reliability-assessment (Forecasting). R1 (route-knowledge decay under a depot merger), R2 (a blockade's diversion over a route driven only at long recency) and R3 (operator errors per operation against per console-hour under a new duty cycle) measured dead on code, eight more on paper (`## Tried and rejected`). No card registered; v2 stays the card's identity, marked spent. PAUSED at stage 1 for another cell.

Fifth cell (chosen by this build, 2026-10-23): energy-systems-utilities / asset-condition-maintenance (Forecasting),
architecture 3, card v3 registered with v2 moved into `lineage` as spent, `pipeline.json` architecture 3.
