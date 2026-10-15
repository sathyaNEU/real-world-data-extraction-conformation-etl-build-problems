# task460 design note

Architecture 1, drawn 2026-10-15 from seed ET17 (the world and the decision; the pitfall re-found from the data).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task460.json`, registered 2026-10-15. Guard WARN only: overuse.shape
  (01 in three of the last twelve: a pick among eight stores is a ranked list under a cap of one, and the criteria come
  from each store's three figures) and repeat.question_form (where, after task145: a siting call asks where). The older
  same-puzzle and same-driver matches (task105 v1, task135 v2, task451 v2) are differentiated on the card.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL, own pattern
  operating-margin-weighted-by-project-output. The seed's energy-procurement world has no ETL task type in Energy
  Systems & Utilities; emissions accounting does, and it owns the quantity a sustainability team sites a project on:
  the grid carbon dioxide a megawatt-hour of new zero-emission output avoids. Emissions accounting estimates it for a
  grid-connected project from the operating margin, the generators that would otherwise have run in the hours the
  project generates, not from the grid's average output rate.
- **Why this task type:** the six ETL-serving task types are all in recent use; emissions-inventory was last drawn by
  task459 (a plant's CO2 per net MWh at its contract output) and task452 (a forest program's deforested area), neither
  about which generators a change in load moves.
- **Shape:** 01, a ranked list under a cap of one. Arithmetic: the store picked, the first store left out and its gap
  (3); each of the eight stores' avoided carbon dioxide per megawatt-hour, the array's annual output and the tonnes it
  would avoid in a year like 2025 (24); a chart of the pick's marginal rate by hour of day and season against its array's
  output (about 4); the hourly conformed file (1): 32 before the asks.
- **Strategy:** decomposition_attribution (the change in a system's emissions attributed to the change in its load,
  hour by hour) on the time gap (the evidence covers every hour; the decision bets on the hours the array generates)
  with the population gap behind it (the average covers every generator; the change moves only the marginal ones).
  Generators G7 (operating window) decisive, G6 (composition shift) and G2 (grain mismatch) behind.
- **World:** Corvane Home & Garden, a national home and garden retailer (invented) in an unnamed country, with one
  candidate store in each of eight balancing areas: Brackwell, Quillbury, Tennaford, Gorsefield, Faraview, Ostlemere,
  Kestrel Point and Halvane. Its capital committee funds one on-site solar pilot in the 2027 capital plan, at the store
  whose array would avoid the most grid carbon dioxide per megawatt-hour it generates.
- **Files (planned):** `balancing_area_hourly_generation_2025.csv` (the spine: each balancing area's hourly demand,
  net generation by fuel and scheduled interchange, UTC hour ending with a local-time column, about 70,000 rows);
  `unit_hourly_emissions_2025.csv` (the emissions monitoring system's hourly records for every fossil unit: operating
  time, gross load, CO2 in short tons, local standard time); `generating_plant_register_2025.csv` (plants and units,
  balancing area, fuel, prime mover, capacity, annual net generation); `grid_emission_rates_annual_2025.xlsx` (the
  national agency's published annual average and non-baseload output rates by balancing area); `pilot_array_output_model.csv`
  (each store's modelled hourly AC output for its planned array, local standard time hour beginning);
  `corvane_store_sites.csv`; `solar_pilot_charter_2027.pdf` (the committee's charter: the decision, its measure and its
  timetable); `balancing_area_codes.csv`; a data dictionary; a manifest; distractors (the stores' 2025 electricity
  bills, the suppliers' power content labels).
- **Forcing fact:** the capital committee approves the 2027 capital plan on 4 December 2026; the pilot's site is named
  in the plan. The measure is the latest full calendar year of grid records (2025); the call (where the array goes)
  faces forward.
- **Forum and forcing event:** committee_or_panel (the capital committee), budget_or_appropriation (the 2027 capital
  plan). Organisation retailer_or_ecommerce; role procurement_lead (the director of energy and sustainability).
  Personas from `guard.py names --geo "United States" --seed 460`: Barbara Rangel (director of energy and
  sustainability), Joel Russo (energy analyst).
- **Data-native sentence:** in a dispatched grid the generators that answer a change in load are the next ones in the
  merit order, not the average fleet, and which ones they are moves with the hour as load, wind and solar shift the
  order; the hourly records show the response only in the hour-to-hour changes, and a store's array changes its area's
  load only in daylight.
- **Sources, one line each:**
  - `stumping/references/client/measured-drivers.md`, the held group: the decisive step defines the quantity upstream of
    every graded figure (here which generators a megawatt-hour displaces), and the easy routes are published figures a
    solver trusts.
  - `stumping/references/client/two-layer-task-design.md`, field_method and estimand identification: emissions
    accounting's operating margin for a grid-connected project against the inventory's average rate.
  - `dataset-generation/references/layer1-messiness.md`: clocks (UTC against local standard time, hour ending against
    hour beginning), units (pounds against tonnes), operator imputation and renamed areas; none on the decisive step.
- **Same-puzzle and abstraction:** gap time, generator G7, Gate G method_or_model_selection, decision pick_one_of_n.
  Nearest drivers on file 0.07 to 0.08 (task94 lineage, task123, task135, task459); none sets a new source's effect by
  the margin in its own operating intervals.

## Tried and rejected

- 2026-10-15, draw: the seed's own quantity, the all-in price a kWh saves under two bills (delivery and supply) counted
  once. Rejected: counting the delivery-only rows' kilowatt-hours once is reading a part code (data semantics), and the
  price an array saves (the avoidable volumetric rate) is tariff analysis, a task type with no ETL objective.
