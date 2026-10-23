# task173: the Varner Valley Public Utility District's April to September 2027 irrigation pumping forecast for Tri-Basin, the first season the Varner River watermaster holds the riparian and pre-1914 rights to a quarter of their allotments (architecture 2)

**Status (2026-10-23).** The number was marked RETIRED on 2026-10-22 (`## Retired`) and the author reopened it for a
from-scratch rebuild in a new cell, `energy-systems-utilities` / `load-forecasting`, Forecasting. Architecture 1
(Ashdale Tax Live) and the two redraw cells of 22 October are spent and are not re-screened; their deaths stay in
`## Tried and rejected`. Architecture 2 below is new in world, decision, quantity and mechanism. No seed is used: the
cell was allocated by the main session and the organisation, decision, quantity and mechanism were searched here.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v2 (the first card this number has carried; architecture 1 sits in `lineage` as abandoned unregistered) |
| Domain / task type | `energy-systems-utilities`, task type `load-forecasting` (serves Forecasting): the deciding quantity is a utility rate class's season energy under a change in its water supply, built the way an irrigation load forecaster builds it, acre-feet each pumping plant must move times that plant's energy per acre-foot |
| Objective | Forecasting & Predictive Modeling: the energy Schedule IP services will draw from 1 April to 30 September 2027, a season not yet open; every file was pulled by 16 October 2026 and the member forecast is due to Tri-Basin on 1 December 2026 |
| Shape | `single-figure`: the call (the class's season energy in MWh, nearest 5,000) and the three base-year tables Tri-Basin's form asks beside it, delivery-point energy by billing month (24 figures), delivery-point demand in each monthly system peak hour (24), and the irrigation services and billed energy each delivery point supplied (8); 56 ask figures, criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (MWh) |
| Mechanism | gap population (decisive: one bottomland billing row is two pumps, a river lift and a well, whose energy per acre-foot differ about fivefold, and the 2027 order moves water from the one to the other), with time (the order rewires where the bottomland plants' water comes from for the first time, and the record's only curtailment response is the bench wells'); pattern none; generators G2 (the bill's grain is the plant's meter, the decision's is each pump on it), G5 (the bottomland need was met by the river lifts until now), G14 (the bench wells' energy per withheld acre-foot does not apply to this pool), G6 (the curtailed population moves from one band of the record to the other); Gate G `forecasting`; strategy `decomposition_attribution` |
| Layer 2 family / pattern | `field_method` (pumping energy as water moved times each plant's own energy per acre-foot, the combined plant's river lift and well separated by fitting its metered energy to its own two metered volumes); `own:replacement-water-priced-at-each-combined-plants-own-well-and-lift` |
| Layer 1 | the January 2020 CIS conversion (legacy account numbers before it), meter exchanges as two read lines, estimated reads trued up on the next read, cancelled and re-issued bills with reversals, register reads with multipliers, the agency's two report layouts and a water year still coming in, the service number written three ways, station days filled from neighbours; on the asks' rows only, feeders moved between substations with the GIS label left as mapped, the delivery-point meters' own clock, a check meter stamping interval starts and a second bank's meter energised mid-season (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `customer_or_counterparty` (the forecast is filed with Tri-Basin Power Authority, the joint power authority that supplies the PUD and sets its 2027 energy blocks from it), forcing event `season_or_peak` (the order fixes the 2027 season's surface supply now, ahead of Tri-Basin's 1 December deadline), organisation family `local_government` (a public utility district, a publicly owned electric distributor), role family `procurement_lead` (the power supply manager who buys the PUD's power), context artifact `filed_standard` (Tri-Basin's member load forecast instructions, the standard the forecast is filed against), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | `vvec_ip_billing_2015-2026.csv`, one row per meter read line on a Schedule IP bill, January 2015 to September 2026, 96,153 rows; constructed in the layout of a public utility's CIS billing extract across a system conversion |
| Deliverables | `irrigation_forecast_2027.xlsx` (the forecast and its working, the three base-year tables) |
| People | drawn with `guard.py names --geo "United States" --seed 173`: Mario Barnett (the PUD's power supply manager, the requester; in no file), Kimberly Ball (Varner River Watermaster, signs Order No. 2026-14), Tammy Gibson (Tri-Basin load forecasting; named on the instructions). Adam Rojas dropped on a people.first WARN |
| World | the Varner Valley Public Utility District serves the Varner River bottomlands and the Lone Bench above them; Tri-Basin Power Authority, a joint power authority of public utilities, is its supplier; the Varner River Decree (1934) is administered by a court-appointed watermaster; Lone Bench Irrigation District holds a post-1914 right; the Varner Subbasin Groundwater Agency takes metered extraction reports; Kestrel County. All fictional, as are the people, systems and data; the field's method is real |

**Data-native sentence.** In this valley the only seasons the record shows water being cut are the Lone Bench
district's, and the bench wells lift from 300 to 400 feet down, while the bottomland plants the 2027 order cuts lift
from shallow alluvium a few dozen feet down and their river lifts and wells share one meter, so the energy a cut
acre-foot costs is a property of whose wells replace it, readable only by fitting each bottomland plant's metered
energy to its own diversion statements and its own metered well extraction.

**Sources read, and how this differs.**
- `two-layer-task-design.md` families (Energy carries no client rigor cards): `field_method` (the field's own
  energy-water identity), with `estimation_fit` for the per-plant two-volume fit. The textbook routes for an irrigation
  class forecast (an econometric model of class energy on curtailed water and evapotranspiration, an analogue season,
  per-account models on own history) are the default path and its rivals, never the stump.
- Nearest domains' cards: Economics `forecasting-forecast-evaluation` and `elasticity-welfare-policy-impact-estimation`
  2 (a response measured under one regime carried to another) and Healthcare `utilization-access-demand-forecasting` 1
  (capped demand); Urban `forecasting` 1. Each is a lower rung or the default path here; the golden is none of them
  applied as stated: the judgment is which quantity transports (the water, not the energy) and whose lift prices it.
- Cell builds: task136 (rooftop PV bulk-buy uplift, adoption) and task164 (coincident transformer peak from new EV load)
  spend adoption and coincidence; nothing here adopts or coincides. task131 (tariff rebound), task120 (storage drawdown),
  task152 (module wear), task132 (spares renewal) spend their own drivers; none prices water by lift.
- Shapes that held this round (task169 re-routing, task177 v2 exposure at one end): the shape here is our own, a supply
  rule rewiring where a group's water comes from, priced by a physical intensity the record shows only per plant.
- `guard.py slots` on the mechanism's words (energy per acre-foot, same meter, two volumes, combined plant, river lift)
  and the setting's (irrigation, groundwater, watermaster, pumping): task138's irrigation district season order, task152's
  plant wash well, task478's unmetered pumping screen (energy to water through a lift factor, rejected there as no ETL
  task type serving hydrology) and task134's dry-year battery seed share vocabulary only.

## Guard

**The draw was redrawn twice before it was filed, each time on the axis the guard named, and the record of it is the
point of this section.**
1. At the probe the decisive pattern was labelled G14 (the bench wells' rate does not fit this pool), which sat behind
   task273's `ban.pattern`; it was carried as G6 (the curtailed population moves from one band of the record to the
   other), with `composition_mix` and the decree's schedule as the context artifact.
2. Under the registration lock the window moved: task175, registered minutes earlier, took G6, `composition_mix` and
   `register`, and with it the same-puzzle and same-driver signatures inside the batch, and task171 took
   `cooperative_or_member_body`. The decisive rung was re-read rather than relabelled: the silent rung is splitting each
   bottomland meter into its river lift and its well (the readable rung beneath it is carrying water rather than
   energy), so the card leads with G2 (the bill's grain is the plant's meter, the decision's is each pump on it) and
   `decomposition_attribution`, with G5, G14 and G6 kept beside it, and the context artifact is Tri-Basin's filed
   forecast standard, the stakeholder's own file. The ladder, the golden and every figure were unchanged by it.
3. The organisation was then a rural electric cooperative and both of its honest families were banned
   (`cooperative_or_member_body` against task171, `utility_or_infrastructure` against task175). The world was redrawn on
   that axis: the distributor is a public utility district (`local_government`), the publicly owned kind that serves
   irrigation pumping in western valleys, and its supplier a joint power authority. Names and voices moved; the data,
   the decision and the mechanism did not.

`guard.py check` on the filed card: WARN only. `overuse.objective` and `overuse.gate_g` (forecasting in 6 of 12): the
lane's objective. `repeat.gate_g` (task171, task170) and `repeat.decision` (quantity_figure against task170): the
objective's own Gate G and a season energy is a quantity. `test.same_puzzle_older` and `test.same_driver_older`
(population, G2, quantity_figure / forecasting) carry differentiation lines against task142 and task148 v1, and the
card keeps its lines against task98 v1, task124 v6, task132, task144, task163, task465 v1 and task175.

**Abstraction test.** The nearest drivers (task181 v1 at 0.09, task237 at 0.08, task465 v2 at 0.08): two victim
sources pooled at a common point, a composite's variance share, two traits no source records together. None splits
one metered total into two sources by fitting it to each source's own recorded volume, and none prices a carried
volume at each unit's own cost per unit. task175 (the batch's nearest by structure) reads take-up at each run's own
fill; nothing here takes up, and every bottomland plant replaces every acre-foot it can.

## Tried and rejected`. Architecture 2 below is new in world, decision, quantity and mechanism. No seed is used: the
cell was allocated by the main session and the organisation, decision, quantity and mechanism were searched here.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v2 (the first card this number has carried; architecture 1 sits in `lineage` as abandoned unregistered) |
| Domain / task type | `energy-systems-utilities`, task type `load-forecasting` (serves Forecasting): the deciding quantity is a utility rate class's season energy under a change in its water supply, built the way an irrigation load forecaster builds it, acre-feet each pumping plant must move times that plant's energy per acre-foot |
| Objective | Forecasting & Predictive Modeling: the energy Schedule IP services will draw from 1 April to 30 September 2027, a season not yet open; every file was pulled by 16 October 2026 and the member forecast is due to Tri-Basin on 1 December 2026 |
| Shape | `single-figure`: the call (the class's season energy in MWh, nearest 5,000) and the three base-year tables Tri-Basin's form asks beside it, delivery-point energy by billing month (24 figures), delivery-point demand in each monthly system peak hour (24), and the irrigation services and billed energy each delivery point supplied (8); 56 ask figures, criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (MWh) |
| Mechanism | gap population (decisive: one bottomland billing row is two pumps, a river lift and a well, whose energy per acre-foot differ about fivefold, and the 2027 order moves water from the one to the other), with time (the order rewires where the bottomland plants' water comes from for the first time, and the record's only curtailment response is the bench wells'); pattern none; generators G2 (the bill's grain is the plant's meter, the decision's is each pump on it), G5 (the bottomland need was met by the river lifts until now), G14 (the bench wells' energy per withheld acre-foot does not apply to this pool), G6 (the curtailed population moves from one band of the record to the other); Gate G `forecasting`; strategy `decomposition_attribution` |
| Layer 2 family / pattern | `field_method` (pumping energy as water moved times each plant's own energy per acre-foot, the combined plant's river lift and well separated by fitting its metered energy to its own two metered volumes); `own:replacement-water-priced-at-each-combined-plants-own-well-and-lift` |
| Layer 1 | the January 2020 CIS conversion (legacy account numbers before it), meter exchanges as two read lines, estimated reads trued up on the next read, cancelled and re-issued bills with reversals, register reads with multipliers, the agency's two report layouts and a water year still coming in, the service number written three ways, station days filled from neighbours; on the asks' rows only, feeders moved between substations with the GIS label left as mapped, the delivery-point meters' own clock, a check meter stamping interval starts and a second bank's meter energised mid-season (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `customer_or_counterparty` (the forecast is filed with Tri-Basin Power Authority, the joint power authority that supplies the PUD and sets its 2027 energy blocks from it), forcing event `season_or_peak` (the order fixes the 2027 season's surface supply now, ahead of Tri-Basin's 1 December deadline), organisation family `local_government` (a public utility district, a publicly owned electric distributor), role family `procurement_lead` (the power supply manager who buys the PUD's power), context artifact `filed_standard` (Tri-Basin's member load forecast instructions, the standard the forecast is filed against), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | `vvec_ip_billing_2015-2026.csv`, one row per meter read line on a Schedule IP bill, January 2015 to September 2026, 96,153 rows; constructed in the layout of a public utility's CIS billing extract across a system conversion |
| Deliverables | `irrigation_forecast_2027.xlsx` (the forecast and its working, the three base-year tables) |
| People | drawn with `guard.py names --geo "United States" --seed 173`: Mario Barnett (the PUD's power supply manager, the requester; in no file), Kimberly Ball (Varner River Watermaster, signs Order No. 2026-14), Tammy Gibson (Tri-Basin load forecasting; named on the instructions). Adam Rojas dropped on a people.first WARN |
| World | the Varner Valley Public Utility District serves the Varner River bottomlands and the Lone Bench above them; Tri-Basin Power Authority, a joint power authority of public utilities, is its supplier; the Varner River Decree (1934) is administered by a court-appointed watermaster; Lone Bench Irrigation District holds a post-1914 right; the Varner Subbasin Groundwater Agency takes metered extraction reports; Kestrel County. All fictional, as are the people, systems and data; the field's method is real |

**Data-native sentence.** In this valley the only seasons the record shows water being cut are the Lone Bench
district's, and the bench wells lift from 300 to 400 feet down, while the bottomland plants the 2027 order cuts lift
from shallow alluvium a few dozen feet down and their river lifts and wells share one meter, so the energy a cut
acre-foot costs is a property of whose wells replace it, readable only by fitting each bottomland plant's metered
energy to its own diversion statements and its own metered well extraction.

**Sources read, and how this differs.**
- `two-layer-task-design.md` families (Energy carries no client rigor cards): `field_method` (the field's own
  energy-water identity), with `estimation_fit` for the per-plant two-volume fit. The textbook routes for an irrigation
  class forecast (an econometric model of class energy on curtailed water and evapotranspiration, an analogue season,
  per-account models on own history) are the default path and its rivals, never the stump.
- Nearest domains' cards: Economics `forecasting-forecast-evaluation` and `elasticity-welfare-policy-impact-estimation`
  2 (a response measured under one regime carried to another) and Healthcare `utilization-access-demand-forecasting` 1
  (capped demand); Urban `forecasting` 1. Each is a lower rung or the default path here; the golden is none of them
  applied as stated: the judgment is which quantity transports (the water, not the energy) and whose lift prices it.
- Cell builds: task136 (rooftop PV bulk-buy uplift, adoption) and task164 (coincident transformer peak from new EV load)
  spend adoption and coincidence; nothing here adopts or coincides. task131 (tariff rebound), task120 (storage drawdown),
  task152 (module wear), task132 (spares renewal) spend their own drivers; none prices water by lift.
- Shapes that held this round (task169 re-routing, task177 v2 exposure at one end): the shape here is our own, a supply
  rule rewiring where a group's water comes from, priced by a physical intensity the record shows only per plant.
- `guard.py slots` on the mechanism's words (energy per acre-foot, same meter, two volumes, combined plant, river lift)
  and the setting's (irrigation, groundwater, watermaster, pumping): task138's irrigation district season order, task152's
  plant wash well, task478's unmetered pumping screen (energy to water through a lift factor, rejected there as no ETL
  task type serving hydrology) and task134's dry-year battery seed share vocabulary only.

## Guard

`guard.py check` on the card: WARN only. `repeat.gate_g` (forecasting against task169): forecasting is the objective's
own Gate G and the mechanism differs. `repeat.deliverables` (xlsx against task169): a workbook is what Tri-Basin's form
takes. `test.same_puzzle_older` and `test.same_driver_older` (population, G6, quantity_figure / forecasting) carry
differentiation lines on the card against task98 v1, task124 v6, task132, task144, task163 and task465 v1. The
decisive pattern was first labelled G14, which sat behind task273's `ban.pattern` at the probe; G6 is the honest first
key because the decisive fact is the curtailed population moving from one band of the record to the other, G14 and G5
stay beside it, and nothing in the design moved with the label (card `notes`).

**Abstraction test.** The three nearest drivers (task464 v1 at 0.06, task482 v1 at 0.06, task501 v3 at 0.06): a
standard-year output on the current regime, a combined return split by head count, a forward draw on an allotment
before a deadline. None prices a carried volume at each unit's own intensity behind a shared meter. **Same-puzzle
test:** gap population, G6, quantity_figure repeats task163 outside the twelve; differentiated (task163 discounts
marginal entrants; here every unit replaces its whole shortfall and only the energy per unit volume differs).

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
