# task459 design note

Architecture 1, drawn 2026-10-14 (wave 3, oviya1301), from seed ET16 (a planning team's list of the most efficient gas plants from the generation survey). Kept: the world (gas-fired plants in one footprint, a planning team building a list of them), the decision (which plants make the list) and the quantity (efficiency, read here as carbon dioxide per net megawatt-hour). Not kept: the seed's mechanisms (combined-cycle steam turbines carrying generation and no fuel, CHP fuel, generator fan-out), which are data semantics; they survive only as Layer 1. task456 and task457 wait: no ETL task type is free for their worlds while task453 and task454 hold the last three draws.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task459.json`, architecture v1, registered 2026-10-14. `guard.py check` returns WARN only. Each WARN is answered here.
  - `overuse.objective` (ETL, 5 of the last 12): the lane's objective.
  - `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection): the honest label for a rate the data must be read at the right operating level for; the mechanism (a unit's emission rate as a function of its output, read at the level a commitment fixes) is on no other card.
  - `test.same_puzzle_older` and `test.same_driver_older` against task230 v2, task114 and task33 are differentiated on the card; so is task452 (a curve through sparse samples, the nearest insight in the lane).
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). Each offered plant's carbon dioxide per net megawatt-hour is put together from the hourly emissions monitoring records (per combustion-turbine stack), the balancing authority's revenue meters (per plant), the generation and fuel survey, the generator inventory and the unit-to-generator crosswalk. Building a generating unit's emission rate from hourly heat input, CO2 mass and net generation is the emissions inventory's own work for the power sector.
- **Objective:** ETL. The conformed dataset is each offered plant's 2025 emissions and generation record on the standard's basis (CO2 in pounds, net MWh at the plant's meter), with the determination beside it.
  - Forward facing: the commitment runs 2027 to 2036; the rate that decides is the one the plant will emit at while delivering its contract capacity, estimated from its 2024 and 2025 records.
  - Not retaggable as Forecasting: no series is projected. The open part is the plant's emission rate at an operating level its records hold only in some hours.
- **Shape:** 10, a scorecard against one threshold: each offered plant's CO2 per net MWh against 925 pounds. Criteria arithmetic (planned; the ask sheet fixes it at design):
  - the call, the megawatts the district can sign and the plants, 2;
  - each of the ten offered plants' rate under the commitment with its verdict, 10;
  - the chart of the ten rates against the 925 line, 3;
  - two or three asks on measures the call does not use, about 15;
  - the two files, 2.
  - About 32 in all.
- **Strategy:** forecast_method_backtest (F6: the invariant is the plant's heat input as a function of its output, recorded hour by hour; the closed period's average is not invariant to how the plant was dispatched). The decisive move is the operating level the rate is read at.
- **Mechanism:**
  - Gap: time (decisive: the records describe the plants as they were dispatched in 2024 and 2025, cycling, part-loaded and peaking on their duct burners; the commitment holds each plant at its contract capacity in every hour), with population supporting (which hours represent the commitment).
  - Generators: G13 decisive (the decision covers an operating regime the closed window did not run), G7 (the operating level the commitment fixes), G17 (the margins, asserted).
  - Gate G: method_or_model_selection. Layer 2: estimation_fit, `own:emission-rate-at-committed-operating-level`. Pattern A (the past average against the committed future rate; a filed contract fact pins the horizon's operation; no past ranking ships).
- **World:** Calder County Public Utility District No. 1, a public power utility in Washington. Its 2026 baseload request for offers seeks capacity for 2027 to 2036 under ten-year tolling agreements. Ten gas-fired plants in the balancing authority's footprint were offered. The state's emissions performance standard bars a utility from a long-term baseload commitment with a plant that emits more than 925 pounds of CO2 per net MWh, and the district's procurement procedure determines the rate from the plant's own monitoring and meter records; sellers' guaranteed heat rates are not accepted. The board of commissioners approves the commitments.
- **As-of:** the monitoring records for 2024 and 2025 (EPA's quarterly reports, final for 2025 in spring 2026); the balancing authority's revenue-meter data for the same years; offers received 30 September 2026; the determination for the board's November 2026 meeting.
- **Furniture:**
  - Forum board_of_directors (the district's board of commissioners); forcing event purchase_order_or_contract (the ten-year tolling agreements); organisation utility_or_infrastructure (a public utility district).
  - Role capacity_planner (the district's manager of resource planning; the prompt names no one); context artifact capacity_report (the balancing authority's seasonal capability test results); calibration none.
- **People:** drawn with `guard.py names --geo "United States" --seed 459`, on the card: Victor Carr (the district's general manager), Adrian Dunn (manager of resource planning), Julie Jackson (the district's environmental compliance specialist). Christine Burke and Lisa Howell were drawn and set aside (first names on older builds).
- **Data-native sentence:** a gas combined cycle burns more fuel per megawatt-hour at part load and in the hours after a start, and its duct burners add output at a far higher heat rate than the turbines; plants that cycled through 2024 and 2025 carry those hours in their annual averages, while the baseload commitment holds each plant at its contract capacity in every hour, a level the cycling plants held only on their best hours and one Tamarack Landing reaches only with its duct burners firing.
- **Sources, one line each:**
  - `two-layer-task-design.md`, estimation_fit (the data's real structure; ratio of totals): the rate is a ratio of totals over hours whose operating levels the commitment changes.
  - `strategies.md` F6 and "the field's estimator meets the data's process": the invariant is the unit's input-output relation, recorded hourly; the generic move carries the period average.
  - `layer1-messiness.md`, Physical & Environmental Sciences and Energy (instrument records with method codes, standard against prevailing time, gross against net, prime-mover grain): Layer 1, none of it on the decisive step.
  - task452 (a concentration-discharge curve through sparse samples): the nearest insight in the lane; here every hour is recorded and the error is the operating level, not the sampling.
- **Prototype** (scratch, nine simulated plants on one seed): the rate read in the hours near each offer's output matched the plant's true rate under the commitment within 6 pounds; the annual average sat 5 to 11 per cent above it for the cycling plants and within 1 per cent for the base-loaded ones; the duct-fired offer needs firing in most hours to move far enough, so the generator sets its contract capacity above its winter unfired capability.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the request for offers and the procurement procedure: a baseload commitment may be signed only with a plant whose CO2 per net MWh is at or below 925 pounds; each offer names a plant and a contract capacity.
2. Conform the hourly emissions records: each monitored stack to its plant through the crosswalk, CO2 short tons to pounds, every reported hour kept.
3. Net generation: the balancing authority's meter per plant per hour (or the survey's monthly net generation), 2025.
4. Rate: the plant's 2025 CO2 over its 2025 net generation.
5. Sign the plants at or below 925 and add their contract capacities.

**Ends on:** sign Tamarack Landing, Ochre Flat, Juniper Draw, Lindgren Hill and Moraine Point; turn down Sorrel Butte, Kessling Creek, Ashby Gulch, Pelton Mill and Coldbrook (as designed; the generator places each plant so the built ladder lands it, asserted in `checks.py`).

**Golden:** sign Sorrel Butte, Kessling Creek, Ochre Flat, Juniper Draw, Lindgren Hill, Ashby Gulch and Moraine Point; turn down Tamarack Landing, Pelton Mill and Coldbrook, each plant's rate read at its offered contract capacity from the hours it ran at that output.

## Stump sentence

The default path turns down Sorrel Butte, Kessling Creek and Ashby Gulch and signs Tamarack Landing because it rates each plant on its 2025 annual CO2 per net MWh, which carries the cycling plants' starts and part-load hours and Tamarack Landing's mostly unfired base operation into a commitment that holds every plant at its contract capacity in every hour; read at that output, the three cycling plants sit well under 925 pounds and Tamarack Landing, firing its duct burners in every hour to reach its contract capacity, sits above it.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory (serves ETL in the client taxonomy): a plant-level CO2 inventory built from hourly monitoring records, revenue meters and the generation survey.
Domain test: the quantity that decides is each plant's CO2 per net MWh at its committed output; emissions accounting for generating units estimates it from hourly heat input and CO2 mass against metered net generation, read at the operating level, because a gas unit's heat rate falls with load, carries start-up fuel and rises once duct burners fire.
Swap: "sign the hospitals whose cost per discharge at the contracted volume is at or below the cap" has no heat input, no part-load heat rate, no start-up fuel, no duct burner and no station service drawn while idle; the hourly records the rate is read from have no counterpart, so the task stops reading.
Layer 1: hourly monitoring per turbine stack in standard time with method-coded substitute hours (the operator's data acquisition system); stacks to generators through the EPA-EIA crosswalk (many-to-many for combined cycles); revenue meters per plant in prevailing time, negative while idle (the balancing authority's settlement system); survey net generation by prime mover with no fuel on steam turbines (the survey's design); offers under trade names (the sellers); a stack renumbered at a monitor replacement (the monitoring plan); seasonal capability tests (the balancing authority).
Layer 2: estimation_fit. A plant's emission rate is a function of its output level; the commitment fixes the level, so the rate must be read at it, not carried from the closed period's average.
Decisive step: estimate each plant's CO2 per net MWh at its offered contract capacity from the hours its records hold at that output (its heat-rate curve), instead of its 2025 annual average.
Not semantics: with every field read right (gross against net, short tons, standard against prevailing time, the steam turbine's missing fuel, the crosswalk, the substitute hours), the annual average is still the easy route and still files the wrong plants.
Not rule application: the procedure files the estimand (CO2 per net MWh delivered under the commitment) and the threshold, and no filed rule says how a rate at a committed output is estimated; executing every filed rule on the annual average turns down Sorrel Butte, Kessling Creek and Ashby Gulch and signs Tamarack Landing.
Analyst test: a strong analyst who conforms the records, aligns them with the meters and rates each plant on its 2025 CO2 per net MWh signs Tamarack Landing, Ochre Flat, Juniper Draw, Lindgren Hill and Moraine Point and turns down Sorrel Butte, Kessling Creek and Ashby Gulch (the default path's Ends on).
Estimand: CO2 per net MWh delivered under the commitment (the plant at its contract capacity in every hour of the term outside planned outages), against 925 pounds, per offered plant; filed in the district's procurement procedure (the emissions performance section) and the request for offers (the delivery terms).
No decoy: nothing is planted. No memo, draft, seller attestation or published rate argues for the annual average; sellers' guaranteed heat rates are filed as not accepted and do not ship.
No certified replay: no certified, published or prior determination of any plant's rate ships, and the method is not recovered by reproducing one.
Lesson: a generating unit's emission rate belongs to the operating level it was measured at; when a commitment fixes the level, the rate is read at that level (part load, starts and supplementary firing all move it), which no build on file teaches.

## Tried and rejected

- 2026-10-14, draw: task456 (ET13, regional hospital surge trigger) first, as `status.py next` names it. Rejected for now: hospital capacity sits in Healthcare Delivery's patient-flow task type, which serves no ETL objective, and the ETL task types free of the last three draws (payment claims, emissions inventory, test equating) do not hold it.
- 2026-10-14, draw: the ambient-temperature correction of full-load heat rate as the decisive step. Rejected: a combined cycle's full-load heat rate moves 1 to 2 per cent across the seasons, too little against the margins determinism needs; it stays inside the golden method.
