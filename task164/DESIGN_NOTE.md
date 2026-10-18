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
| Shape | `05` allocation to a fixed total: each district's replacements (12) and its forecast at-risk count (12), Foothill's figure on its own and the system at-risk total (2), then two decoupled asks (the 2025-26 pilot close-out in its three districts, and each district's summer 2026 transformer failures with the customer-hours they cost) and a chart of the failures. Criteria on paper: 12 + 12 + 2 + 9 + 24 + 4 (chart) + 2 (files) = 65 |
| Decision | `allocation_to_total`, answer unit `count` (replacements per district, summing to 400 by the Commission's largest-remainder rule) |
| Mechanism | gap time (decisive: the evidence a solver reaches first is a vehicle's average draw over the 4 to 9 pm window, the decision bets on the transformer's highest quarter hour of the coming summer) with population (the increment is a property of the transformer the vehicle joins, its size and the default-rate vehicles it already serves, not of the vehicle); pattern D (two flawless grains: the per-vehicle window average is right at the system's grain, the coincident increment at the transformer's; the decision funds transformers); generators G2 (what one unit of the decided thing is), G14 (the increment conditioned on the premise's rate and the transformer's size), G7 (the 4 to 9 pm window against the hours EV-rate premises charge in); Gate G `method_or_model_selection`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `field_method` (diversified demand on a service transformer, the field's own construction); `own:coincident-peak-increment-by-transformer-size-and-rate` |
| Calibration | `none`: the 2024 to 2026 recorded peaks are the transformers' own history, the series a forecaster fits and holds out, never a certified record |
| Furniture | forum `regulator_or_inspector` (the Commission receives the compliance filing), forcing event `statutory_or_regulatory_filing` (the filing is due 30 April 2027), organisation family `utility_or_infrastructure`, role family `programme_officer` (the manager of the proactive replacement program files the allocation), context artifact `register` (the GIS service-transformer register the call reads for nameplate), opening `question-first`, question form `how-many` |
| Spine | the transformer load management extract, one row per transformer location and summer (2024, 2025, 2026: recorded 4 to 9 pm peak in kVA, its date and quarter hour, premises summed and AMI completeness), about 150,000 rows; constructed in the layout of a utility TLM extract |
| Deliverables | `ptr_2027_district_allocation.xlsx` (the allocation table, the at-risk counts and the ask tables) and `summer_2026_transformer_failures.png` (the failures ask charted, never the decision quantity) |
| People | drawn with `guard.py names --geo "United States" --seed 164`: Megan Stewart (distribution planning, owner of the TLM extract), Christopher Richardson (load research), Katelyn Duarte (regulatory compliance), Antonio Morgan (the pilot's construction lead); the requester is in no file and not in the prompt |
| World | Calloway Valley Power Company (searched: no utility or company of the name), a fictional investor-owned electric utility in California's Central Valley and Sierra foothills, twelve operating districts (Foothill, Railyard, Canal, Mission, West Bluff, Crestview, Lakeside, Sunrise, Sandhill, Kingsley, Highland, Brookside; each screened against every card's invented names, Old Town, Orchard, Delta and Northgate dropped for colliding) |

**Data-native sentence.** A transformer's recorded summer peak is the single highest quarter hour of its summed
premises' load, so it is set on the evening its load happens to be highest; on a small pole-top serving one to five
homes that is an evening a vehicle at a default-rate premise charges, which makes the vehicle's contribution to the peak
most of its charger's draw, while the load research sample, read as averages, says the same vehicle draws 0.7 kVA between
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
