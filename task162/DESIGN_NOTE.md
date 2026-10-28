# task162 design note

Architecture 2, drawn 2026-10-28 (the Forecasting slot's re-root at the author's word, the same day architecture 1 was
spent on determinism). The world, the decision, the dataset and the generator are all new; architecture 1's record is
kept in its own section below, its card identity in the card's lineage and its ledger line under Earlier architectures.

## Draw

1. **Pairing.** energy-systems-utilities / asset-condition-maintenance, which serves Forecasting (`guard.py check`
   raises no task-type BLOCK). A water network's leakage is the standing condition of its mains and service pipes, and
   pressure management is the intervention whose effect the field forecasts by FAVAD (leakage rising with pressure to a
   district's N1). Client domain energy-systems-utilities; no house domain.
2. **World.** Lynmere Water, an English water company (invented), supplies its Northern zone from Thornholme service
   reservoir down the Thornholme to Brackenby trunk main. Coldbeck Network Partners (invented) is its pressure management
   and leakage delivery partner on an outcome contract: paid per megalitre a day of sustained reduction as Lynmere's own
   annual district leakage assessment measures it, with a reduction target per phase. Phase 3 is the 22 district metered
   areas at the trunk main's far end, each getting a fixed-outlet pressure reducing valve at its inlet, commissioned
   January to March 2027. Brackenby Paper Mill draws two weekday shifts' worth of water off its own off-take on the same
   main. The contract measures the phase against the 2025-26 assessment year, in the 2027-28 one.
3. **The call (forward, a window not yet open).** Will Phase 3's valves take the districts' leakage down by the
   contracted 0.48 Ml/d in the 2027-28 assessment, and if not, how many find-and-fix gang-years (0.05 Ml/d each,
   rounded up) must be added? A go/hold for the 2027-28 delivery plan with the shortfall and the gang-years; shape 07,
   the criteria from the zone check on the call's 2025-26 baseline, a reconciliation inside the decision: the 2025-26
   assessed leakage of the zone's twelve other districts and the zone's top-down balance, against which the districts'
   bottom-up leakage is read (the call's own district figures are charted, not graded: they sit on the call's
   population, which carries no device).
4. **The decisive step (Layer 2, G7 operating window).** A fixed-outlet valve holds its outlet at its setting only
   while its inlet pressure is above the setting and stands fully open otherwise. At the far end of the main the mill's
   weekday shifts (06:00 to 22:00) pull the district inlets down by 7 to 11 metres on average through the working day,
   more at the demand peaks, against settings 8 to 15 metres under the night inlet pressure, so on the pack the valves
   stand open in 20 to 37 per cent of the hours in 14 districts and 3 to 15 per cent in the other 8, all but a tenth of
   a per cent of those hours on weekdays from 06:00 to 22:00 (D1 to D3 in `checks.py`). The leakage the
   2027-28 assessment will measure (net night flow times a night-day factor built from the hourly average zone
   pressures) comes from replaying each day's recorded inlet and zone pressures through the setting, hour by hour, and
   rebuilding both the night flow and the night-day factor. The easy route carries the valve's night pressure ratio
   through every hour.
5. **Card.** shape 07; decision go_hold_or_stop; answer unit rate_or_share (megalitres a day); gap time then
   population; pattern none; generators G7 (decisive) and G13; Gate G forecasting; strategy other (an intervention's
   effect replayed at the hour a device acts on recorded upstream values, rather than carried from the hour it acts
   hardest); calibration none; context artifact close_out_summary (Lynmere's 2025-26 district leakage assessment, the
   closed year's figures, correct for the question it answers); Layer 2 field_method,
   `own:fixed-outlet-valve-diurnal-bite`; forum customer_or_counterparty (the plan goes to Lynmere's contract manager);
   forcing event purchase_order_or_contract (the contract's 2027-28 delivery plan instructs the gangs before the
   assessment year opens); org professional_services (the partner carries the contracted reduction); role
   field_unit_lead (the partner's Northern zone delivery lead, who runs the find-and-fix gangs). Axes redrawn at stage 2
   when the window moved under the registered card (task304 and task177 v4 were filed minutes before it and reached this
   checkout only with the DRAWN pull): strategy binding_constraint to other (task177 v4 holds it, and the step is no
   limit deciding feasibility), forcing event launch_or_rollout to purchase_order_or_contract (task304 holds it; task179
   has left the window), role operations_director to field_unit_lead (task304), context artifact monitoring_export to
   close_out_summary (task177 v4). `check` on the edited card: WARN only.
6. **People** (`guard.py names --geo "United Kingdom" --seed 162`, on the card): Emily Fitzgerald (Coldbeck's Northern
   zone delivery lead, the requester, not in the prompt), Annette Patel (Coldbeck's network modeller, the valve
   schedule), Clive Heath (Lynmere's contract manager), Louis Lee (Lynmere's leakage analyst, the assessment export),
   Mandy Austin (Coldbeck's commercial manager).
7. **Guard.** `check` before and after `register` (2026-10-28T04:48:39Z): WARN only. repeat.gate_g and overuse.gate_g
   answered on the card (forecasting carries this stump, a forward assessment of an intervention not yet installed,
   and the fine mechanism is no forecasting card's: nearest driver 0.07, task303). test.same_driver_older is
   differentiated on the card against task105 v1 (an outlet's season-ahead agreement window), task170 v1 (a first
   passage of scattered measurements over a level), task229 v3 (a daily mean passed through a convex rating, Jensen's
   gap inside the day, where averaging the replayed readings here is harmless) and task303 (shared upstream losses).
   The forcing event was redrawn from purchase_order_or_contract (task179 held it) and the organisation from
   utility_or_infrastructure and the role from capacity_planner (task281 holds both); the partner's seat is the honest
   one, since the contracted reduction is the partner's to deliver.
8. **slots.** On the driver's words and on the setting's (valve setting, outlet, inlet pressure, trunk main): no slot
   note touches a valve, its setting or an inlet pressure. "water company" finds task182's arsenic results, task248's
   treatment plants and task303's feeders, none of them this mechanism; task120 (a campus water utility's well capacity
   read through its tank levels, in review) shares the water setting and nothing else.
9. **Prototype** (scratchpad `t162v2/proto/prv3.py`, before the generator): on settings that bite in every reading the
   night-ratio route lands within 3 to 8 per cent of the replay, so the generator places the phase where the far end of
   a main with a heavy daytime off-take really sits: the settings held for a 20 m critical-point design condition at the
   2035 peak with a fire flow, the inlet falling under them through the working day.
10. **Screens on paper.** Estimand: the 2027-28 assessed leakage and its reduction are filed by the contract and the
   assessment method, and the decisive step is none of the five parts. Variance only: the step moves the point
   estimate. Common exposure and partial coverage: there is no attaining subset (Phase 3 is the partner's first scheme
   in the zone, no valve in the zone has run before) and the correction acts on every district's day, one per
   district, never one number. Designation: the call is a total against a contracted figure, no slate. 1.2c: the
   assessment is the filed measurement and the decisive construction is the valve's physics, no model of the
   measurement; N1 is filed per district, so nothing is fitted per group (1.1j) and no grouping decides (1.1c). Fourth
   clause: no file summarises the replay (the export's average zone night pressure and night-day factor are the
   pre-valve facts the easy route reads). Swap: patients and wards have no valve whose effect turns on an upstream
   pressure, no N1 and no night-day factor. Library: the field's shortcut for a scheme's benefit is the night pressure
   ratio raised to N1, which is the default path.
11. **Layer 1** (from Lynmere's own systems, none carrying the stump; the inventory with each item's mishandling is
   `## Layer 1 inventory`): telemetry stamped in GMT; logger swaps with new serials; two logger makes, one reporting
   bar; battery gaps and re-transmitted blocks; the export's own monthly and yearly layout; a retired district code
   still in the logger register and the property system; a district fed through its neighbour for nine days; new
   builds under plot and address records; flats on shared supplies; a billing extract by supply point and bill period
   across the year's edges; the reservoir outlet meter's calibration.

## Default path
1. Read the outcome contract's Schedule 4 (Phase 3's target: the Phase 3 districts' leakage down by 0.48 Ml/d in the
   2027-28 assessment against the 2025-26 one, both by Lynmere's method LW-LA-04, the year's figure the mean of its
   twelve months, a shortfall made up by find-and-fix at 0.05 Ml/d a gang-year rounded up), Lynmere's planning note
   (2027-28 demand and pressures as recorded in the same months of 2025-26, the valves in service all year), the method
   (net night flow at 03:00 to 04:00 GMT less the night use allowance, times a night-day factor from that day's hourly
   average zone pressures to the district's N1) and Coldbeck's valve schedule (each valve's outlet setting and its
   average zone night pressure before and after commissioning).
2. Take each district's 2025-26 monthly assessed leakage and average zone night pressure from Lynmere's export and the
   night inlet pressures from the loggers; the valve lowers the night inlet to its setting, so the average zone night
   pressure falls by the night inlet's excess over the setting (the schedule's after-commissioning column).
3. Scale each month's leakage by the average zone night pressure after over before, raised to the district's N1 (the
   field's benefit calculation for a pressure scheme), and sum the 22 districts.
4. The phase's 2027-28 leakage comes to 2.59 Ml/d against 3.22, a reduction of 0.63 Ml/d: over the 0.48 Ml/d target,
   so no find-and-fix.

Ends on: the phase meets its contracted 0.48 Ml/d with a 0.63 Ml/d reduction, no find-and-fix gang-years.
Golden: the phase falls 0.07 Ml/d short with a 0.41 Ml/d reduction, 2 find-and-fix gang-years.

## Stump sentence
Scaling each Phase 3 district's 2025-26 assessed leakage by its valve's night pressure ratio raised to the district's
N1 files the phase as meeting its contracted 0.48 Ml/d with a 0.63 Ml/d reduction and no find-and-fix; the step that
lands it there is carrying the night reduction through every hour, when on weekday daytimes the paper mill's draw on
the trunk main pulls the far districts' inlets below their valves' settings and the valves stand fully open, so the
2027-28 assessment, rebuilt hour by hour through the settings, measures a 0.41 Ml/d reduction, 0.07 Ml/d short, and the
phase needs 2 find-and-fix gang-years. The data-native sentence: the inlet loggers already record every weekday's
daytime inlet sitting under each far district's setting, so the valve's bite is a property of the recorded pressures,
not of the valve.

## Three rules

Task type: asset-condition-maintenance (Energy Systems & Utilities), which serves Forecasting & Predictive Modeling in the taxonomy; a water network's leakage is the standing condition of its mains, and a pressure scheme's 2027-28 effect on it is forecast before the valves exist.
Domain test: the deciding quantity is the leakage Lynmere's FAVAD assessment will measure in 2027-28 once fixed-outlet pressure reducing valves hold each district's inlet, which a water loss engineer forecasts from the district's recorded inlet and average zone pressures, its N1 and the assessment's night-day factor; nothing like it exists once the nouns are swapped.
Swap: "how many fewer patients a ward will hold in 2027 once a new discharge lounge opens" keeps a planned intervention and a forecast against a target but loses the valve whose effect depends on an upstream pressure, the N1 power and the night-day factor, so the quantity the call turns on stops existing.
Layer 1: Lynmere's telemetry export (inlet loggers with flow and pressure, zone loggers with pressure, hourly means in GMT, one logger make in bar and the other in metres head, swaps with new serials, battery gaps, re-transmitted blocks), the assessment export in its own monthly layout, the property extract with plot and address records and shared supplies, the billing extract's read cycles and the outlet meter's daily volumes; none of it decides the call (`## Layer 1 inventory`, asserted item by item).
Layer 2: field_method, a pressure scheme's benefit rebuilt the way the assessment will measure it: each fixed-outlet valve lowers its district's pressure only in the hours its inlet sits above the setting, so the night flow and the night-day factor are rebuilt from the recorded hourly pressures through the setting rather than the night pressure ratio carried to every hour; the choice flips the call.
Decisive step: replay each Phase 3 district's 2025-26 hourly inlet and average zone pressures through its valve's outlet setting (the outlet the lower of the inlet and the setting, the zone pressure lowered by the same amount), rebuild each day's net night flow by FAVAD and its night-day factor from the replayed zone pressures, and take the months, the year and the reduction against 2025-26 as the method and the schedule define them.
Not semantics: every field is read correctly on the default path (each district's export rows, the night hour, the allowance, N1, the settings in metres at the outlet, the loggers' units once converted); the miss comes from carrying a night ratio through the day, not from reading anything differently, and every reading difference in the fork table prints the same call.
Not rule application: the method files how leakage is measured and the contract files the target and the yield, while no shipped sentence says when a valve lowers the pressure or how a scheme's benefit is to be forecast; executing every filed rule with the night ratio carried through the day files the 0.63 Ml/d reduction and the target met (R3a, asserted on the generator's clean truth).
Analyst test: a strong analyst who conforms the loggers, reads the method, the contract, the planning note and the valve schedule correctly and applies the field's benefit calculation (the 2025-26 assessed leakage times the average zone night pressure ratio to N1) files the 0.48 Ml/d target met with a 0.63 Ml/d reduction and no find-and-fix gang-years, because the night ratio holds only while each valve bites and on weekday daytimes it stands open.
Estimand: the contract's Schedule 4 and the method file the population (the 22 Phase 3 districts), the outcome (the leakage LW-LA-04 assesses), the window (the 2027-28 assessment year, April 2027 to March 2028, its figure the mean of its months), the comparison (against the 2025-26 assessment in Lynmere's export of 14 May 2026) and the shortfall's conversion (0.05 Ml/d a gang-year, rounded up); the planning note files the forward conditions (each month's demand and pressures as recorded in the same month of 2025-26, no growth, the valves in service all year at rev C); the prompt asks the question.
No decoy: nothing is planted: the paper mill is an ordinary customer whose draw shows in the inlet pressures and in its own meter, the valve schedule gives settings, a design basis and a true night pressure after commissioning and states no benefit, the assessment export answers 2025-26 correctly, and no memo, plan or earlier forecast states a 2027-28 figure or argues a method; the distractors are named in `metadata.json`.
No certified replay: no shipped figure is reproduced to recover a method: the baseline is the export's own 2025-26 assessment, and the forecast is the method executed on the replayed readings.
Lesson: a model learns that a fixed-outlet valve can only lower the pressure while its inlet stands above the setting, so a pressure scheme's benefit has to be rebuilt hour by hour from the recorded inlet pressures before the leakage assessment's night flow and night-day factor are applied; at the end of a long trunk main a heavy daytime draw upstream keeps the valves open through the working day.

## Readability screen
Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Figures from the cut pack, asserted in `checks.py`.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 no change: the 2025-26 assessment carried (0.00 reduction, 10 gang-years) | the contract names the valves as the phase's measure | the export's leakage column | no | no | no | no | readable |
| R1 (default) the night pressure ratio to N1 on each month's assessed leakage (0.63, target met) | the method's N1 and the schedule's settings | the schedule's AZNP columns | yes, the field's benefit calculation | no shipped figure scores it | no | one ratio per district | readable |
| R2a the night flow change times 24 hours (0.70, met) | no | the export's net night flow | yes, a night-flow reflex | no | no | one subtraction | readable |
| R2b the night drop applied to every hour's zone pressure, the night-day factor rebuilt (0.68, met) | no | the zone loggers | a half-step: a profile without the valve's physics | no | no | no | readable |
| R3 a typical day per month replayed through the setting (0.39, 2 gang-years: the insight, every figure missed) | no | the loggers | a half-step: the physics on averaged days, against the method's per-day factor | no | no | no | readable |
| R4 (decisive) each day's hourly readings replayed through each setting, net night flow by FAVAD and the night-day factor rebuilt per day (0.41, 2 gang-years) | no sentence says when a valve bites or how a scheme's benefit is forecast | the inlet logger's pressure against the schedule's setting is a cross-file comparison nothing invites | no: the field's reflex is the night ratio | no control scores it | no | no: it needs the hourly replay | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py` on the built pack.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "cut the leakage by 0.48 Ml/d in the 2027-28 assessment" | the 2025-26 assessed leakage of the 22 districts less the 2027-28 one, each year the mean of its twelve monthly figures | a reduction in night flow carried over 24 hours | the night-flow reading files 0.70 and the target met | Schedule 4.2 (each year assessed by LW-LA-04 issue 6) |
| SF2 | the forward conditions | each 2027-28 month as recorded in the same month of 2025-26, no growth, valves in service all year at rev C | trended demand or pressures | not open | the planning note |
| SF3 | the year's figure | the mean of the twelve monthly figures | the mean of all valid days | same call (0.41, 2 gang-years) | LW-LA-04 section 6 |
| SF4 | the night hour | 03:00 to 04:00 GMT, the loggers' clock | 03:00 to 04:00 local time | same call, same printed figures | LW-LA-04 section 3 |
| SF5 | the night use allowance | 1.7 litres an hour for each dwelling connected that day | each property record or each supply point | same call (Phase 3's counts agree under every reading) | LW-LA-04 section 4 |
| SF6 | N1 | each district's own, from LW-LA-04 Table C2 | one company value | 1.15 for every district files 4 gang-years | LW-LA-04 Table C2 |
| SF7 | the outlet setting | metres head at the valve outlet, the inlet logger's own point | metres at the average zone point | same call, same printed figures | the valve schedule's design basis |
| SF8 | a valid day | 24 hourly readings on the inlet and zone loggers, the district closed | partial or gap-filled days kept | same call, same printed figures | LW-LA-04 section 5 |
| SF9 | gang-years | the shortfall over 0.05 Ml/d a gang-year, rounded up | rounded to the nearest | 1 gang-year (1.4 to the nearest) | Schedule 4.4 ("rounded up to whole gang-years") |
| SF10 | the valve's head loss when open | none at district flows | up to 0.1 m whenever the valve is open | same call, same printed figures | the valve schedule's sizing line |
| SF11 | the 2025-26 baseline | the export of 14 May 2026, as Schedule 4.2 names it | the method rerun on the loggers | same call, same printed figures | Schedule 4.2 |
| SF12 | the zone pressure after the valve | the recorded zone pressure lowered by what the valve takes off the inlet, flows as recorded | the district's head loss refitted to its lower inflow | same call, same printed figures | the planning note (pressures as recorded) |
| SF13 | the change in leakage with pressure | N1 on the net night flow, the minimum night flow less the night use allowance | N1 on the whole minimum night flow, night use included, the allowance taken off after | 0.70 and the target met | LW-LA-04 section 7 (N1 applies "to any change in a district's leakage with its pressure") and section 4 (the net night flow is the minimum night flow less the allowance) |

## Ladder
Figures from the cut pack (`generator/checks.py`, section L; `generator/calc.py` modes).

| Rung | Construction | Reduction (Ml/d) | Gang-years | Dies to |
|---|---|---|---|---|
| R0 | the 2025-26 assessment carried | 0.00 | 10 | the contract's measure is the valves' effect |
| R1 default | each month's assessed leakage times the night pressure ratio to N1 | 0.63 | 0 (target met) | on weekday daytimes the far districts' inlets sit under their settings and the valves stand open |
| R2a | the night flow change times 24 hours | 0.70 | 0 | the method's night-day factor |
| R2b | the night drop on every hour's zone pressure, the factor rebuilt | 0.68 | 0 | a fixed-outlet valve cannot lower a pressure already under its setting |
| R3 | a typical day per month replayed | 0.39 | 2 (the call, every figure missed) | the method's factor is per day; the averaged day shaves the valves' hours at the margin |
| R4 decisive | each day's readings replayed through each setting, the night flow and the factor rebuilt per day | 0.41 | 2 | (golden) |

**Position and margins.** The default path sits 0.15 Ml/d over the target and the golden 0.07 under it; the golden's
shortfall over the yield is 1.4, 0.4 of a gang-year from each whole-number boundary. Every printed call figure sits
well inside its cell (clearances 0.38 to 0.49 of a step), and the corridor members (the open valve's 0.1 m, the
head loss refitted to the lower inflow, the setting read at the zone point, the night hour in local time, gap-filled
days) print the same figures.

**Worth on the graded quantity.** Seeing that the valves stand open on weekday daytimes is worth 0.22 Ml/d of the
reduction and the whole find-and-fix call.

## Layer 1 inventory

Each item, the system that writes it, its file, and its natural mishandling; R2 in `checks.py` runs the golden method
with each Phase 3 item mishandled and asserts the call and its printed figures unmoved. Items outside Phase 3 are ask
devices or hazards (`## Ask sheet`).

| Item | System and file | Natural mishandling | Effect |
|---|---|---|---|
| Hourly means stamped in GMT, the loggers' clock | telemetry archive; both logger files | the stamps read as local time, the night hour taken at 03:00 BST | none on the call (asserted) |
| A logger swapped with a new serial (NZ20's inlet, 14 April 2025) | logger register; inlet file | the old serial left unmapped | none on the call (asserted) |
| Battery gaps (NZ27's zone point, NZ15's inlet; NZ11 and NZ05 near) | inlet and zone files | gaps interpolated and the days kept | none on the call (asserted) |
| Re-transmitted blocks (NZ22's inlet, NZ30's zone point; NZ08 near) | inlet and zone files | duplicate rows summed | none on the call (asserted) |
| Two logger makes, one reporting bar (NZ02 and NZ08 inlets, NZ06 and NZ11 zone points, NZ03's after its swap) | logger register | bar left unconverted | none on any graded figure (ratios; asserted) |
| The export's monthly and yearly sheets, a SUM row | assessment export | the SUM cell read as a value | none |
| A retired code still in use (NZ04A) | logger register, property extract, code history | the code left unmapped | Ask A (NZ04) and Ask B only |
| A district fed through its neighbour (NZ09 through NZ10, 12 to 20 January 2026) | inlet file, district register | the days kept | Ask A (NZ09, NZ10) only |
| Plot and address records on one supply point; flats on a shared supply | property extract | records or supply points counted | Ask A only (Phase 3 has none, asserted) |
| Identical assessed lines (flats on a shared supply) | billing extract | identical lines dropped | Ask B only |
| Bills across the year's edges; the outlet meter's calibration; NZ-TM | billing extract, outlet file, certificate | bills counted whole, readings uncorrected, the mill left out | Ask B only |

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 22 Phase 3 districts in Schedule 4's table | filed (Schedule 4) |
| 2 | Unit of account | the district's assessed leakage, Ml/d; the phase the sum | filed (LW-LA-04 section 6) |
| 3 | Attribution window | the 2027-28 assessment year, April 2027 to March 2028 (GMT days) | filed (Schedule 4.2, LW-LA-04); SF3 |
| 4 | As-of dating | the files taken on 2 November 2026; the telemetry to 31 March 2026 | the extracts' own dates; no figure after the as-of is used (Z7 asserted) |
| 5 | Version basis | the 2025-26 assessment as exported on 14 May 2026 | filed (Schedule 4.2); SF11 |
| 6 | Denominator | none (levels, not rates) | n/a |
| 7 | Weighting | none (a sum of districts, a mean of months) | filed; SF3 |
| 8 | Window length | the twelve months of 2025-26 as the forward conditions | filed (planning note); SF2 |
| 9 | Boundary inclusivity | a GMT day from 00:00 to 24:00; the night hour 03:00 to 04:00 | filed (LW-LA-04); SF4 |
| 10 | Rounding path | unrounded months, the mean, the reduction, then two decimals; gang-years up | filed (Schedule 4.4); SF9 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | none (the record is complete for 2025-26) | n/a |
| 13 | Order of operations | replay, then the day's net night flow and factor, then the day's leakage, then the month's mean | filed (LW-LA-04's day-then-month order); SF3 asserted |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | re-transmitted logger rows are exact duplicates | C1 (R2 asserted: summing them leaves every printed figure) |
| 16 | Identity normalisation | logger serials to districts through the logger register, swaps dated | the register's own dates (R2 asserted) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | metres head throughout Phase 3; bar only on near-district loggers, where only ratios and flows are read | filed (LW-LA-04 section 2, 1 bar is 10.197 m); R2 asserted |
| 19 | Code and status semantics | none on the call (no retired code in Phase 3) | A11 asserted |
| 20 | Integerisation | gang-years rounded up | filed (Schedule 4.4); 1.6 clear of 1 and 2 by 0.4 (C3b asserted) |
| 21 | Clause scope | the target applies to the phase's sum, not to each district | filed (Schedule 4.2) |
| 22 | Forward window contents | the valves in service from 1 April 2027 at rev C settings | filed (planning note, valve schedule) |

## Literal reader
Executed word for word, the prompt, Schedule 4, LW-LA-04, the planning note and the valve schedule fix every part of
the estimand: the 22 districts, the assessed leakage, the 2027-28 year as twelve months each as recorded in 2025-26,
the reduction against the export's 2025-26 figure, the conversion to gang-years rounded up. What the text leaves open
is how a valve that does not yet exist changes the hourly pressures the method reads, and the literal reader must
forecast it: the outlet of a fixed-outlet valve is the lower of its inlet and its setting (the schedule's own sizing
line makes the open valve's loss negligible, and the corridor asserts it moves nothing), so replaying the recorded
readings is the only execution that uses the method as written. The night ratio carried to every hour is not a
reading of any sentence: it assumes the night's reduction holds when the recorded inlet sits under the setting. Every
fork row above closes on a quoted sentence or prints the same call.

## Oracles
None on the main call: no shipped file states a 2027-28 figure, a benefit for any valve, an earlier forecast or a
scheme's realised saving, and the zone has no valve in service whose record could be read across. The assessment export
answers 2025-26 and is the baseline the contract names. The valve schedule's AZNP after commissioning is the true
night figure (asserted against the pack's own replay at 03:00) and is the default path's input, not a verdict. The
mill's AMR shows its two-shift weekday draw and is not needed: the inlet pressures already carry its effect.

## Ask sheet

The call's population is the 22 Phase 3 districts' 2025-26 hourly inlet and zone readings, their export rows, their
valve settings and their N1. Every ask reads other rows: the zone check on the baseline reads the twelve districts
nearer Thornholme (the method executed on their raw loggers, the export covering only the contract's districts) and
the zone's bulk and billing records, the top-down balance the districts' bottom-up leakage sits under. Zero device or hazard rows sit in the call's population (A9 and A11 asserted: Phase 3 has no plot
record, shared supply, retired code, dated connection, open boundary or bar logger).

**Ask A, the zone's twelve other districts' 2025-26 assessed leakage (12 figures, Ml/d to three decimals).** The method
executed on raw loggers. Construction: LW-LA-04's day-by-day net night flow and night-day factor. Primary (all twelve):
the allowance counts each dwelling connected that day, and the property extract carries two kinds of shared supply
point: a new build connected under the developer's plot record (no UPRN) and given its address record on the same
supply point 45 to 150 days later, the plot record closed then about one time in seven (2,290 new builds), and flats on
a shared supply, two to six dwellings with their own UPRNs on one supply point (779 supply points). Counting property
records double-counts the new builds once addressed, counting supply points loses the flats, counting UPRNs drops each
new build until it is addressed: each misses all twelve figures (by 1 to 7 bins, A2b). Only the dwelling count lands, a
reconstruction per supply point. Hazards: NZ04's second inlet still logged under the retired code NZ04A and 37 per cent
of its properties coded NZ04A (the code history maps it; leaving either out misses NZ04); NZ09 fed through NZ10 for 12 to
20 January 2026 (its inlet dry, NZ10's carrying both; section 5's closed-district rule, which no file narrates, takes
both districts' days out; keeping them misses both).

**Ask B, the Northern zone's 2025-26 top-down balance (3 figures, Ml/d to two decimals): system input, billed unmetered
consumption, real losses.** Construction: section 8 executed on the outlet meter's daily volumes and the billing
extract. Primary: flats on a shared supply each carry their own assessed bill on the shared supply point, so the
extract holds identical lines (779 sets); the hygiene battery's exact-duplicate reflex drops them, taking billed
unmetered 0.25 Ml/d low and real losses as much high. Hazards: the outlet meter's certificate (readings before 12
November 2025 divided by 0.986; uncorrected misses system input and real losses); NZ04A's properties (unmapped misses
billed unmetered and real losses); bills apportioned by days (counted whole, real losses miss); the trunk main's direct
supplies, NZ-TM (left out, real losses miss). Corridor: the certificate applied by multiplying (1.014) rather than
dividing, and bill_to read as exclusive, print every balance figure alike (B2 asserted).

Pair ceiling: 32.2 (one response on the call and one off it, both handling the asks the cracker's way); 48.7 with both on the call.
Mirror leakage: 6.7 per cent of ask weight (the mirror keeps Ask B's system input only).
Measured by: generator/cracker.py (on the cut pack: the cracker counts supply points once and drops identical bill lines, the mirror counts property records and drops them too).

| Ask | Figures | Cracker path (lands the call, runs the battery, executes every filed rule) | Cracker keeps | Verdict |
|---|---|---|---|---|
| A, the twelve near districts' leakage | 12 | conforms the loggers, maps NZ04A, drops NZ09's and NZ10's open days, sees the repeated supply point references and counts each supply point once | 0 of 12 | miss |
| B, the zone's balance | 3 | the outlet's daily volumes with the certificate's correction (system input kept), bills to the zone's customers apportioned by days, identical lines dropped (billed unmetered and real losses missed) | 1 of 3 | miss |

| Ask | Mirror (stops at the default rung) | Mirror keeps |
|---|---|---|
| A | counts property records | 0 of 12 |
| B | as the cracker | 1 of 3 |

**Arithmetic.** Ask weight 55 over 15 ask figures; the cracker keeps 1 of 15 (Lc 0.067): C = 38 + 7 + 55 x 0.067 =
48.7; the mirror keeps 1 of 15 with about 5 of the recommendation: S = 5 + 7 + 3.7 = 15.7; the pair (48.7 + 15.7) / 2 =
32.2. The layer leans on the dwelling count: a response that resolves both kinds of shared supply keeps 12 of 12 on Ask
A, and if both top responses did so the pair would reach (92.7 + 59.7) / 2 = 76.2 on the same footing; the device is a
reconstruction with three wrong reflexes and one right handling, which is why it carries the layer.

## Pre-ship check

Written at stage 4 and re-read against the pack after the leak reader's fix pass (target.zip a8146587: Phase 3's infill
and demolitions, the winter leakage and smaller bursts, the commissioning route, the certificate's test points).

1. Domain: a water company's pressure management partner deciding whether a phase of fixed-outlet pressure reducing
   valves meets its contracted leakage reduction; the quantity that decides is the leakage the company's FAVAD
   assessment will measure in 2027-28 (net night flow times a night-day factor from the hourly zone pressures) once the
   valves act on the recorded pressures, and another field's nouns break it.
2. Real work, nothing planted: a telemetry archive stamped in GMT with swaps, two logger makes, battery gaps and re-sent
   blocks, the company's own assessment export, a property extract with plot and address records and flats on shared
   supplies, a billing extract by supply point across the year's edges, a reservoir outlet meter with its certificate;
   each from the organisation's own systems, none deciding the call (R2 asserted item by item).
3. The flip is an analytical choice: whether the night's pressure reduction holds through the day, which the recorded
   inlet pressures settle; every filed rule is read the same on both paths (R3a and R3b on the generator's clean truth).
4. The analyst test holds: the night ratio files 0.63 Ml/d and the target met, the schedule's after-commissioning AZNP
   0.63, the night flow over 24 hours 0.70, the night drop on every hour 0.68; only the hourly replay files 0.41 and 2
   gang-years, and a typical day replayed per month 0.39 (the call reached on the insight, every figure missed).
5. One defensible answer: SF1 to SF12 asserted; the corridor (an open valve's 0.1 m, the head loss refitted to the
   lower inflow, the setting read at the zone point, the night hour in local time, gap-filled days, the export against
   a recomputed baseline) prints the same figures, and every call figure sits at the centre of its cell.
6. No decoy: no file states a 2027-28 figure or a benefit; the valve schedule's after-commissioning AZNP is a true night
   figure (asserted); the contact log and the mill's AMR are declared distractors, read by neither the golden nor an ask.
7. Nothing hidden and recovered: no certified figure pins the method; the baseline is the export Schedule 4 names.
8. A new lesson: a fixed-outlet valve can only take off what its inlet stands above the setting, so a scheme's benefit
   at the end of a trunk main with a heavy daytime off-take has to be replayed hour by hour; no build on file uses a
   device whose effect is bounded by an upstream reading.

- **leak.py REVIEW lines, answered (--asof 2026-11-02):** sweep 3, Table C2 in LW-LA-04 lists districts beside their N1,
  exponents the method files, not answers: harmless. Sweep 4, the method and Schedule 4 carry the stump paragraph's
  generic words (method, factor, contract, export, target, schedule) and name no move; S2 asserts no shipped sentence
  says when a valve acts or how a scheme's effect is forecast: harmless. The prompt's first sentence carries the
  decision's own terms: harmless. Sweep 6, Table C2 and district_register.csv list every district beside its N1 or its
  register fields and rank nothing on the question: harmless.

## Stage 4 (2026-10-28)

- Leak reader (one isolated read of prompt.txt and target/, Sonnet, medium, on target.zip 828ecbc5): no sentence or file
  states the decisive step, nothing ranks the districts or states a 2027-28 figure, no file exists only to help the
  analyst, nothing reads as the answer; question 6 read the decisive step as an analytical choice. Its realism tells
  (flat Phase 3 household counts, flat night flows, the commissioning weeks in code order) and its reading of the
  certificate's test points were fixed in the generator in one pass; no sentence under target/ changed
  (`leak_check_report.md`, Solver's-eye read).
- Determinism judge (one isolated thread on a fresh unzip of target.zip a8146587, run r2): DETERMINISTIC, APPROVE. Every
  main figure, the twelve districts and the balance reproduced; the night ratio carried through the day filed 0.63 and
  the target met, the replay 0.41 and 2 gang-years; Gate G forecasting, analytical_non_defect, no surface read, no sole
  data defect; Gate H domain pass, layers pass, decisive step analytical; stump power moderate, the schedule's
  after-commissioning AZNP read as true but incomplete (`determinism_check_report.md`).
- The judge's two optional pins, declined: a sentence that a dwelling counts once would adjudicate Ask A's primary
  (supplemental-stumping ban 1), and the judge found the reading pinned by the files themselves (plot records without a
  UPRN, bills starting at the plot connection, the handover dates, k flats with k bills); the NZ09 and NZ10 exclusion's
  evidence (NZ09's dry inlet, the shared BV-0910) is already in the write-up's step 6.
- Main thread, while the judge ran: N1 applied to the whole minimum night flow (night use included) files 0.70 and the
  target met; closed by LW-LA-04 sections 4 and 7 and added as SF13 (asserted).

## Architecture 1 record (spent 2026-10-28)

Drawn 2026-10-18 from seed FC33 in product-analytics / feature-adoption-diffusion-modeling: Usva Software's Tampere
bug-triage team filing its first-quarter 2027 triage headcount, staffed for the busiest week at 120 triage items per
triager-week, in its first quarter on a new tracker. The decisive step built each release's adoption from ordinary
restarts plus the Windows restart burst in the two days after Patch Tuesday, which falls inside every first-quarter
release week and never did in the record: 8 triagers, the busiest week near 900 items, against the default path's 6.
Shipped 10-18, repaired for determinism 10-27 (Ask B's "arrived in its components"), returned 10-28 on the portal's
second determinism round (a validated release-phase model filing 6). The re-cut of 10-28 (the autumn train moved
around the restart cycle, the staffing thread's forecast test filed) was judged three times, and each pass found a
competing defensible answer: the decisive configuration was out of sample, so no back-test over the record forced the
restart model, and the restart family's own spread (848 to 977) was wider than the 120-item band. Lessons carried into
architecture 2: the configuration that decides must be in the record; the golden family's spread must sit well inside
the band; no filed back-test (the consecutive-builds rule); the construction should close on arithmetic the records
supply rather than on a fitted behavioural model. The returned reship's pack is commit 6c612d30; the re-cut was never
committed and its measurements are the lines dated 10-28 under Tried and rejected.

## Tried and rejected
- 2026-10-18 draw: the seed's own route made analytical, a new-to-old conversion whose duplicate share rises with the
  spike, so the quiet parallel-run ratio fails in release weeks; its honest key is composition (task470 held it in the ban
  window), and with the counting basis filed and the old export holding every duplicate, rebuilding the new basis from
  the export bypasses the conversion and lands on any typical-quarter golden.
- 2026-10-18 draw: the December release's open regressions drawing duplicates until their fixes ship with the January
  release; carrying the December excess forward lands within a quarter bin of the golden, so persistence is a bypass.
- 2026-10-18 draw: the January release's beta-channel reports scaled to the release wave by the ratio earlier versions
  showed at the same beta age; it is task157's driver (the part already in times a ratio earlier waves kept) in other
  nouns, and the as-of leaves only days of beta.
- 2026-10-18 draw: each release's wave sized by the fixes it carries; one ratio (linear), a covariate reflex, and only the
  January version's size is known at the as-of.
- 2026-10-18 build: ask device A1 of the design stage (the bridge's history entries under the migration lead's account
  while she was on the rota): no literal rule separates her bridge entries from her own triage without a fork; the
  bridge runs under its service account and she is off the rota.
- 2026-10-18 build: Ask A's second figure as the items still untriaged when the run ended: zero in three of the four
  weeks, so the all-nil response kept them; replaced by the items closed by the run's end.
- 2026-10-18 build: the design stage's Ask B (closed items and closed duplicates by group): a careful replay of the
  changelog under the agreement's definitions cracks the Close transition and the moved reports.
- 2026-10-18 build: Ask B as the items in each group's components at the run's end: once the reports the bridge had not
  yet written at the run's end sit in no group, every cracker path kept 5 to 7 of 8 (pair 46.8 to 51.4).
- 2026-10-18 build: Ask B as the reports moved to the web-compatibility team by group: the created path kept 6 of 8.
- 2026-10-18 build: the bridge writing the old number into Legacy bug on every issue: a cracker joining the old export
  on it landed every ask figure (pair 59.1); a real bridge's catch-up writes through a short payload, now modelled.
- 2026-10-18 build: the portal's shares by exact version, point releases as their own rows: reading each point release
  as a new version moved the call to 6, a messy choice flipping the answer; the portal publishes major versions.
- 2026-10-18 build: a parallel-run report PDF with the weekly side-by-side of both trackers: its weekly items by filing
  week would tie only under the old tracker's filing times, an oracle for Ask A; not built.
- 2026-10-27 determinism repair: Ask B's "arrived in its components" read three ways by a portal judge (the component an
  item came in with, its components at the run's end, every component it held), closed by one agreement sentence on the
  WHAT (each report once, in the group of the component it comes in with) rather than by rewording the prompt; the
  judge's optional note that the write-up name the re-sent copies' exclusion declined, since the old bug number already
  excludes them and the write-up states no figure for them.
- 2026-10-28 portal round 2: a filed forecast test on the old record (two releases two weeks before Patch Tuesday) as
  the whole repair: the restart model led a release-phase model with a Patch Tuesday step by 13 per cent on the weeks to
  the next release, tied it with the next release's own week judged (4,204 against 4,223) and lost with the installs
  carried on from the week before (4,818 against 4,832), so the test needed a record that separates the families; the
  train was re-based instead (three releases three weeks before Patch Tuesday, every reading separated by at least 4 per
  cent and the plain one by 24).
- 2026-10-28 re-cut, first version: the train re-based on a fixed four-week cycle from 46.0 (three releases three weeks
  before Patch Tuesday in a row). The licensed judge (pass 2 on 92f9a766, NOT_DETERMINISTIC, SEND_BACK) found two holes:
  a profile carried from the last release fits a run of releases in the same place in the cycle, so the thread's test
  barely separated it from its own restart build; and holding active installs flat from December, against a seasonal
  swing of seven per cent, dropped the busiest week to 825 (7 triagers). Fixed by the autumn that moves at every
  release, the two per cent swing and the first-use share, every rival and every installs projection asserted.
- 2026-10-28, second re-cut: the forecast left at 920 with the e-mail's over-or-under clause alone: the pass-3 thread's
  own restart model fitted on the autumn files 972 to 976 (9 triagers) and on its August and September windows 953 to
  959 (1,000), and the test prefers the whole record to a 17-week window by under 2 per cent, too thin to rule those out.
- 2026-10-28, second re-cut: the first-use rate lowered directly (912 to 890 and 880) to centre the forecast: every
  day's Poisson draws are redrawn, and the pass-3 thread's autumn fit rose to 981 at 890 (9 triagers); the level is set
  by thinning on its own stream instead, which keeps the record as drawn.
- 2026-10-28, second re-cut: the per-release noise in the first-use rate lowered (0.05 to 0.03 and 0.02) so the
  autumn's excess shrinks: the short-window fits did not narrow (965 to 977 at the top), because the autumn fit's weak
  split between baseline and first-use reports carries as much as the draws do.
- 2026-10-28, judge pass 4 on 60e4764a: the thread left the old tracker's Web Compatibility product out of the triage
  items, reading it as the site tool's reports, and filed 7 (783); the runbook already kept moved reports, but the
  product sharing its name with the site tool's project carried a careful reader past it, and at the band's centre that
  misreading costs a triager; the runbook's counting sentence now names the Web Compatibility and Archive products.
- 2026-10-28, judge pass 5 on c898f73f: NOT_DETERMINISTIC, SEND_BACK. With the test pinned to weekly misses, its thread's
  count-based weekly phase model with a Patch Tuesday term fitted on the last 13 weeks missed fewest (1,121 against its
  restart model's 1,305 to 1,395), and its restart family spread 848 to 977. Measured in the generator: the count-based
  phase model with a Patch Tuesday term on the last 13 weeks misses 1,185, against the restart model's 1,434 with the
  installs carried from the week before; the restart model's 850 needs the judged weeks' own installs, which a forecast
  made the day before a release does not have.
- 2026-10-28, architecture 1 spent (each first-quarter release's adoption built from ordinary restarts plus the Windows
  restart wave after Patch Tuesday, 8 triagers against the default path's 6): the decisive configuration, a release
  shipped on Patch Tuesday, never occurs in the record, so no back-test over the record forces the restart model over a
  model that fits the record's releases as well, and the restart family's own spread across defensible builds (848 to
  977 over fit windows, installs projections and lag forms) is wider than the 120-item band the call sits in; each
  repair met a new competing answer at the next judge (the netted test, the autumn fit window, the moved reports'
  product, the count-based model under an honest installs projection). Re-rooted at the author's word: a forecast whose
  deciding configuration is out of sample can be forced only by naming the method, which files the HOW.
- 2026-10-28, architecture 2 draw: a battery fleet's 2027 fade under a move from frequency response to arbitrage, read
  by cycle depth (prototypes bess.py and bess2.py): throughput and equivalent-full-cycle routes landed within 0.3
  points of the truth on average, and the depth family's fitted exponent came out 1.0 to 1.3 against a true 2.0 on
  half-yearly capacity tests, so neither strength nor determinism.
- 2026-10-28, architecture 2 draw, paper: area burnt in 2027 by time since fire (the unburnt land is a filter and a
  divide, the partial-coverage screen, and megafire years spread the per-class rates); pipeline fatigue crack growth
  (a Paris exponent fitted on in-line inspection sizing noise is a fitted family); trial event projection,
  amounts-weighted pensioner mortality, competing exits, delayed entry, deposit betas and burnout, media reach
  (screened to death in task171, task133, task141, task170 and task174); an Erlang loss on beds, reservoir routing,
  tidal flood days, a dairy calving shift and airport show-up curves (task139, task148, task138, task137 and task178's
  drivers, or a calendar-locked schedule like architecture 1's).
- 2026-10-28, architecture 2 build: the replay with the zone pressure lowered by the inlet reduction and nothing else;
  a reader refitting each district's head loss to its lower inflow moved the reduction 0.008 Ml/d, across the 0.40
  cell, while leakage was two fifths of the inflow; household use raised to a realistic 300 to 360 litres a day and the
  in-district head loss halved, so the refit moves it under 0.002 and the corridor is asserted.
- 2026-10-28, architecture 2 build: an open valve's loss filed as under 0.3 m; read as a flat 0.3 m it moved the forecast
  to the edge of its cell; the sizing line now says under 0.1 m and the corridor holds.
- 2026-10-28, architecture 2 build: the outlet meter as found 1.8 per cent low; dividing out the error against adding
  it differed by 0.006 Ml/d on system input, wider than half a cell; 1.4 per cent, and the balance calibrated so both
  readings print alike.
- 2026-10-28, architecture 2 build: Ask B as system input, billed metered and real losses with every step filed in
  section 8; a careful solver executing the section keeps all three, so billed unmetered replaced billed metered and the
  primary became the flats' identical assessed lines.
- 2026-10-28, architecture 2 build: Ask A's primary as new builds under plot and address records alone; dropping the
  plot records landed within half a bin while the address lagged 10 to 45 days, and "household" left room to count
  records; flats on shared supplies added (so counting supply points also misses), the lag set at 45 to 150 days, and
  section 4 counts dwellings.
- 2026-10-28, architecture 2 build: three Phase 3 inlet loggers of the bar make; left unconverted they moved the call, a
  unit reading deciding it, so the bar make moved to near-district loggers where only flows and ratios are read.
- 2026-10-28, architecture 2 build: household night use applied only at 03:00 GMT, a notch rather than a trough; read
  in local time it moved the forecast by 1.2 Ml/d, and the notch is a generator's tell; household use is now a
  local-time profile whose small hours sit at the night use.
- 2026-10-28, architecture 2 build: each Phase 3 district's own forecast printed in the goldens; several sit within
  0.0005 of a two-decimal edge, so the chart draws them without labels and the workbook prints only the asked figures.
- 2026-10-28, stage 4 leak reader: Phase 3's household counts flat all year and the monthly night flows flat but for a
  few bursts read as generated; single infill houses and demolitions added (single records every count reads alike),
  background leakage given a winter rise and the bursts made smaller and more frequent; the call's figures moved to
  3.22, 2.81, 0.41 and 0.07, still 2 gang-years, and R3 (a typical day replayed) now reaches the call while missing
  every figure.
- 2026-10-28, stage 4 leak reader: the valve schedule's commissioning weeks ran two districts a week in code order; now
  the crews' route, one to three valves a week with the half-term week empty.
- 2026-10-28, stage 4 leak reader: the certificate's test-point errors (-1.42 to -1.39 per cent) could be applied in
  place of its stated 1.4; now -1.41 to -1.39, every such reading inside the balance's corridor.
- 2026-10-28, stage 4 fix pass: dropping NZ20's old logger serial lost five months of a district whose leakage now rises
  in winter and moved the forecast a bin; the swap moved to 14 April 2025, so the mishandling costs two weeks.
