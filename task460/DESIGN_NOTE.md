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
  (3); each of the eight stores' avoided carbon dioxide per megawatt-hour, 2025 metered use, share supplied and price
  paid (32); a chart of each store's monthly use against its array's monthly output (about 4); the hourly conformed
  file (1): 40.
- **Strategy:** decomposition_attribution (the change in a system's emissions attributed to the change in its load,
  hour by hour) on the time gap (the evidence covers every hour; the decision bets on the hours the array generates)
  with the population gap behind it (the average covers every generator; the change moves only the marginal ones).
  Generators G7 (operating window) decisive, G6 (composition shift) and G2 (grain mismatch) behind.
- **World:** Corvane Home & Garden, a national home and garden retailer (invented) in an unnamed country, with one
  candidate store in each of eight balancing areas: Brackwell, Quillbury, Tennaford, Gorsefield, Faraview, Ostlemere,
  Kestrel Point and Halvane. Its capital committee funds one on-site solar pilot in the 2027 capital plan, at the store
  whose array would avoid the most grid carbon dioxide per megawatt-hour it generates.
- **Files:** `balancing_area_hourly_operating_data_2025.csv` (the spine, 70,080 rows: each area's hourly demand, net
  generation by fuel and interchange, the hour named by its end in UTC with a local-time column);
  `pilot_array_output_model_2025.csv` (70,080 rows: each store's modelled AC output on 2025 weather, local standard time,
  hour beginning); `generating_plant_register_2025.csv` (plants, fuel, prime mover, capacity, 2025 net generation, CO2 in
  short tons); `edc_generation_emission_rates_2025.xlsx` (the agency's published average, fossil, fuel and non-baseload
  output rates by area, the context artifact); `corvane_pilot_store_sites.csv`; `utility_balancing_area_map.csv`;
  `balancing_area_codes.csv`; `corvane_electricity_invoice_lines_fy2025.csv` (the accounts-payable export of the eight
  stores' electricity invoice lines, December 2024 to February 2026, from the delivery utilities, the retail supplier and,
  from each store's move in the spring of 2025, the bill-payment service; the asks' file); `solar_pilot_siting_charter_2027.pdf` (the decision,
  the measure and the timetable); distractors
  `edc_generation_emission_rates_2024.xlsx` (the prior edition) and `ardley_power_content_label_2025.pdf` (the supplier's
  product mix and intensity, one figure for every store).
- **Forcing fact:** the capital committee approves the 2027 capital plan on 4 December 2026; the pilot's site is named
  in the plan. The measure is the latest full calendar year of grid records (2025); the call (where the array goes)
  faces forward.
- **Forum and forcing event:** committee_or_panel (the capital committee), budget_or_appropriation (the 2027 capital
  plan). Organisation retailer_or_ecommerce; role procurement_lead (the director of energy and sustainability).
  Personas from `guard.py names --geo "United States" --seed 460`: Barbara Rangel (director of energy and
  sustainability), Russell Scott (energy analyst).
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

## Survivor anatomy

- **Actor:** which of an area's generators answer a change in its load in the hours one store's array generates has no
  column in any file: the operating data hold each hour's demand, net generation and generation by fuel, the register
  each plant's annual totals, the publication each area's annual rates; the margin is a relation between consecutive
  hours of one area (the change in its fossil CO2 against the change in its generation) grouped by season and hour, and
  it decides only once weighted by another file's hourly profile. No column is one join away from a marginal rate.
- **Link:** the signal is read through a comparison no shipped figure makes, the area's response in the hours one
  store's array generates: the engineering firm's model (hour beginning, local standard time) joined hour by hour to the
  operator's records (hour ending, UTC) through each area's offset, the store reaching its area only through its
  delivery utility; no key, shared code or clause names the array's hours against the area's margin (charter 3.1 to
  3.4 define the counterfactual, never the hours).
- **Reflex:** the field's named figures for what a grid-connected project avoids sit at rungs 0 and 1 and file wrong
  stores: the agency's published average output emission rate (Brackwell 0.85, where `## Default path` ends) and its
  non-baseload output rate, the usual avoided-emissions proxy (Quillbury 1.11).
- **Back-test:** the textbook route validates: the publication's average, fuel and non-baseload rates recompute from the
  plant register to 0.06 lb/MWh, every area's annual net generation ties to its hourly fuel columns, and the supplier's
  label is one intensity for every store; every control a solver checks the average rate against passes (checks R3c).
- **Second use:** every file the decisive step reads sits in the pack for its own reason: the hourly operating data are
  the publication's source and every rung's input; the array model gives each store's 2025 output for the share supplied
  and the chart; the publication's fuel rates price every rung's fossil CO2; the code list, utility map and store sites
  place each store in its area. Deleting the decisive step drops no file.
- **Shock:** the movement the step recovers is ordinary dispatch, Gorsefield's coal following the load from 5 am to 6 pm
  while gas carries the nights; Gorsefield leads no shipped statistic a route reads (5th on the published average, 2nd on
  non-baseload, 3rd on one all-hours marginal rate, 2nd on array size, use and share behind Ostlemere), so the golden is
  first only on the charter's measure.
- **Pins:** the WHAT is filed in the Capital Committee's own charter (3.1 to 3.4: the counterfactual inside the store's
  balancing area, per MWh of the model's 2025 output, interchange fixed, metric tonnes); no filed sentence names the
  hours, the season grouping, a margin, an estimator or a rate, and no sentence's deletion unforces the call (both judge
  passes executed 3.2 and 3.3 word for word and reached the margin in the array's hours).

## Default path

1. Map each store to its balancing area through its delivery utility (`corvane_pilot_store_sites.csv`,
   `utility_balancing_area_map.csv`).
2. Read each area's 2025 CO2 output emission rate from the agency's publication (`edc_generation_emission_rates_2025.xlsx`,
   sheet BA25) and convert pounds per MWh to tonnes.
3. Take that rate as the grid carbon dioxide each store's array avoids per MWh and rank the stores.

- **Ends on:** Brackwell, 0.85 t/MWh (the area's 2025 average output emission rate), Tennaford second at 0.64.
- **Golden:** Gorsefield, 0.89 t/MWh avoided per MWh of its array's 2025 output, Halvane first left out at 0.58.

## Stump sentence

The default path takes each store's balancing-area average output emission rate as the carbon dioxide its array avoids
and pilots at Brackwell (0.85 t/MWh), where coal runs at full output through the day and gas follows the load; an array
removes the generation at the margin in the hours it generates, gas at Brackwell (0.40 t/MWh) and coal at Gorsefield
(0.89), where gas carries the nights and the coal fleet follows the load from 5 am to 6 pm.

## Three rules

- **Task type:** emissions inventory (emissions-inventory), here the grid emission factor a sustainability team uses
  to credit a project, built by conforming the agency's hourly operating data, its plant register and published rates,
  the engineering firm's array model and the accounts-payable invoices to one clock, unit and store key: the ETL
  objective's conformed store-by-hour dataset is the deliverable the call is read from.
- **Domain test:** the deciding quantity is the avoided-emissions factor of a grid-connected project: the CO2 rate of
  the generators that respond at the margin in the hours the project generates, estimated the way emissions accounting
  estimates marginal emission factors (the hour-to-hour change in the area's fossil CO2 regressed on the change in its
  generation, by season and hour of day) and weighted by the project's own output profile.
- **Swap:** "the clinic whose new evening shift cuts the most waiting per hour staffed" keeps the sentence and loses the
  task: there is no merit order deciding which providers stop working when demand falls in each hour, no published
  average or non-baseload rate that differs from the response, and no hourly operating record whose changes reveal it.
- **Layer 1:** the agency's operating data name each hour by its end in UTC with the area's local time beside it, the
  engineering firm's model names the hour by its start in local standard time (the two systems' conventions); the
  register reports CO2 in short tons and the publication in pounds per MWh, the charter wants metric tonnes; Kestrel
  Point's area filed under its former code KPLP until 30 June 2025 (the operator's renaming); the operator filled a
  few hours of lost demand telemetry from the hour's balance (flagged); solar plants' station service shows as a few
  negative MW at night; the invoice export carries each delivery utility's own line wording, the same kWh on several
  charge lines, Tennaford's declining blocks, Halvane's gas service on its electric bill, two garden-centre meters, the
  supplier's first-term quantities at the wholesale delivery point and its second term at the meter, the bill-payment
  service's dollar-only lines from each store's move and the bills paid twice at the moves. Each is what the system that writes the file produces; none
  carries the call (checks R2: each mishandled, the call, the first store left out, the gap and components 1 to 3 hold).
- **Layer 2:** estimand identification: the counterfactual the charter defines is the response of the area's
  generators to the array's output, which is the operating margin in the hours the array generates, not the area's
  average or non-baseload rate and not one margin fitted over all hours of the year.
- **Decisive step:** estimate each area's marginal emission rate by season and hour of day from the hour-to-hour
  changes in its fossil CO2 against the changes in its generation, and weight it by the store's modelled hourly output.
- **Not semantics:** every field, unit, code and definition read correctly still leaves the published average output
  rate (Brackwell), the published non-baseload rate, the usual proxy for a margin (Quillbury), one marginal rate fitted
  over every hour of 2025 (Tennaford) and the average intensity in the array's hours (Brackwell) on the table; each is a
  correct number for another question, and only the hourly analysis shows they rank the stores differently from the
  margin in the array's hours. No reading flips the call: each Layer 1 item mishandled (the clock an hour either way,
  KPLP's rows dropped, the imputed hours dropped, station service clipped, units left unconverted) leaves the call and
  the critical components where they are (checks R2).
- **Not rule application:** the charter files the estimand (what is avoided, by whose generators, per MWh of which
  output, interchange fixed, in metric tonnes) and the publication files its definitions; no file says which generators
  respond, in which hours, or how to estimate the response (the charter and the publication's notes are scanned for a basis
  or an estimator and carry none, and no describing file ships), so executing every filed rule leaves the estimator to the analyst,
  and on the clean truth the easy ones file Brackwell, Quillbury and Tennaford (checks R3a); only the decisive step files
  Gorsefield (R3b), and it agrees with the generators the dispatch actually moved (0.887 against the estimate's 0.89).
- **Analyst test:** a strong analyst who reads every file correctly and applies every filed rule ranks the stores on
  the published 2025 average output emission rate and pilots at Brackwell (0.85 t/MWh), or on the published
  non-baseload rate and pilots at Quillbury (1.11), or fits one marginal rate per area over all hours of 2025 and pilots
  at Tennaford (0.83), or time-matches the average to the array's hours and pilots at Brackwell (0.82); none files
  Gorsefield. Executed on the generator's clean truth in `checks.py` (R3a), with the decisive step alone filing
  Gorsefield (R3b).
- **Estimand:** charter 3.1 to 3.4: the carbon dioxide that the generators of the store's balancing area would not have
  emitted in 2025 had the array been supplying the store, per megawatt-hour the array generated in 2025 (its modelled
  output), each array megawatt-hour one megawatt-hour less from the area's generators, interchange unchanged, in metric
  tonnes (`solar_pilot_siting_charter_2027.pdf`).
- **No decoy:** nothing is planted to be caught: the published rates are the agency's inventory figures, recomputed
  from the register to 0.05 lb/MWh, and its notes define them without a word on what a project avoids; no memo, draft,
  email or stakeholder figure ships (the folder is the 11 declared files); the charter names no rate, basis or method;
  the supplier's label is one figure for every store and ranks none; no block of records is copied or flat (every
  hourly series and array output scanned, checks R3c).
- **No certified replay:** no certified or published figure reproduces the margin, and the method is not recovered by
  matching one; the publication's figures tie on every path because they answer other questions.
- **Lesson:** what a new zero-emission source avoids is set by the generators that respond in the hours it runs; an
  area's average, its non-baseload proxy and a year-round margin rank sites differently from the margin in the
  project's own hours, and the hourly records reveal it only through their changes. No build on file teaches it:
  task459 measured a plant's own rate against a standard, task135 a variance of a weighted sum, task105 a new
  outlet's take.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 published average output rate (Brackwell) | the publication defines it | a column | yes | no | no | a lookup | readable |
| R1 published non-baseload rate (Quillbury) | the publication defines it | a column | yes, the usual avoided-emissions proxy | no | no | a lookup | readable |
| R2 one marginal rate fitted over all hours (Tennaford) | no | no | yes, an annual marginal factor | no | no | one regression per area | readable |
| R3 margin weighted by the array's output (decisive) | no: the charter defines the counterfactual, never hours or margins | no column holds a margin | no: every reflex above lands elsewhere, and so does the hourly average intensity in the array's hours (Brackwell) | no | no | regressions by season and hour, then a weighting | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | avoided | the CO2 the area's generators would not have emitted had the array been supplying the store | the area's inventory (average) emissions per MWh | Brackwell | charter 3.2 defines avoided as the counterfactual |
| SF2 | grid | the generators of the store's balancing area | the interconnected grid, or the supplier's product mix | Gorsefield, or no ranking (one supplier figure for all) | charter 3.2 (the store's balancing area) and 3.3 (interchange unchanged) |
| SF3 | per MWh of the array's 2025 output | the modelled 2025 output | an annual energy estimate of another year | same call | charter 2.2 (the model's output is the array's 2025 output) |
| SF4 | losses | one array MWh is one MWh less from the area's generators | grossed up for delivery losses | same call | charter 3.3 |
| SF5 | export | all output used in the store | part exported | same call | charter 3.3 (sized below daytime load) |
| SF6 | tonnes | metric tonnes | short tons | same call | charter 3.4 |
| SF7 | 2025 | the store's local standard calendar year | the UTC year | same call and figures | the output in the local hours past the UTC year is under 0.01 per cent of any array's, asserted |
| SF8 | the margin's estimator | season by hour of the change in fossil CO2 on the change in net generation, publication's fuel rates | month by hour, hour of day alone, UTC hour, change in demand or fossil generation (and their pairings), register-derived fuel rates, imputed hours dropped | same call and the same eight figures to two decimals, each at least 0.0009 from a rounding edge | asserted (C1) |
| SF9 | the clock join | UTC hour from each file's own convention | an hour's end read as its beginning, either way | same call, first store left out, gap and components 1 to 3 | asserted (C1 on the call and components) |
| SF10 | Kestrel Point's former code | KPLP rows belong to KSTP | KPLP rows dropped | same call | `balancing_area_codes.csv` (former code and its end date) |
| SF11 | first store left out | the second-highest measure | none | same call | the prompt |
| SF12 | the gap | the pick's measure less the first store left out's, from unrounded figures | from rounded figures | same figure | the prompt's rounding sentence; asserted mid-bin under every estimator |

## Ladder

| Rung | Construction | Winner | Margin over second | Gorsefield's place |
|---|---|---|---|---|
| R0 | the published 2025 average output emission rate | Brackwell 0.851 | 1.34 (Tennaford 0.637) | 5th (0.313) |
| R1 | the published 2025 non-baseload output rate | Quillbury 1.113 | 1.39 (Gorsefield 0.798) | 2nd |
| R2 | one marginal rate per area fitted over all 2025 hours (the change in fossil CO2 on the change in demand) | Tennaford 0.834 | 1.21 (Brackwell 0.687) | 3rd (0.608) |
| R3 | the marginal rate by season and hour, weighted by the array's output (golden) | Gorsefield 0.891 | 1.54 (Halvane 0.579) | 1st |

- **Other reflexes, each landing elsewhere:** R2 fitted on net generation instead of demand, Tennaford 0.834 by 1.21;
  the season-by-hour margins averaged over every hour without the array's weights, Tennaford 0.784 over Gorsefield
  0.679; the hourly average intensity in the array's hours (24/7 matching), Brackwell 0.824 over Tennaford 0.674
  (Gorsefield 4th at 0.352); the published fossil output rate, Tennaford 1.068 over Brackwell 0.877 (Gorsefield 3rd).
- **Position:** Gorsefield is 5th on R0, 2nd once (R1, at 1.39 below the winner) and 3rd on R2.
- **Dominance:** on the golden measure Gorsefield beats every rung's winner by 2.18 times or more (Brackwell 0.402,
  Quillbury 0.390, Tennaford 0.408).
- **Grid:** the two analytical choices (average, non-baseload or marginal; all hours or the array's hours) give five
  cells, each naming a store: average over all hours Brackwell, average in the array's hours Brackwell, non-baseload
  Quillbury, marginal over all hours Tennaford, marginal in the array's hours Gorsefield. Every partial step lands on a
  wrong store; only the margin in the array's hours reaches Gorsefield (asserted).
- **Worth:** on the graded figures every rung's winner avoids far less than its rung says: Brackwell 0.851 against
  0.402, Quillbury 1.113 against 0.390, Tennaford 0.834 against 0.408; Gorsefield 0.31 (R0), 0.80 (R1), 0.61 (R2)
  against 0.89.
- **Data-native structure:** in Gorsefield gas carries the nights and the coal fleet follows the load from 5 am to
  6 pm; in Tennaford coal follows the load through the night and gas the business day from 7 am to 6 pm; in Brackwell
  coal follows the nights and runs at full output by day while gas follows the load; Halvane's coal and gas share the
  daytime margin; the gas-only areas sit near 0.39. The generators the dispatch actually moved, weighted by each
  array's output, give Gorsefield 0.887 and Halvane 0.580 against the estimates' 0.89 and 0.58.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the eight candidate stores, each in one balancing area; the area's generators | charter 2.1 and 3.2; the utility map gives one area per store (asserted) |
| 2 | Unit of account | the store's array; the area's generators as a system | charter 3.1 |
| 3 | Attribution window | the hours of 2025 on the store's local standard clock | charter 3.1; SF7 asserted |
| 4 | As-of dating | the agency's 2025 data, the rates' release 1.0 of 8 September 2026 | the publication's own title line; one vintage of each file |
| 5 | Version basis | the operating data as filed, imputed demand hours as the operator filed them | SF8 converges with imputed hours dropped or demand as the regressor |
| 6 | Denominator | the array's modelled 2025 output | charter 2.2 and 3.1 |
| 7 | Weighting | each hour's marginal rate weighted by the array's output in that hour | charter 3.1 to 3.3 (the counterfactual per MWh generated) |
| 8 | Window length | the full year 2025 | charter 3.1 |
| 9 | Boundary inclusivity | the hour as each file names it | SF9 |
| 10 | Rounding path | rates from unrounded estimates, shown to two decimals; the gap from unrounded rates | the prompt's rounding sentence; every graded rate at least 0.0009 from a rounding edge under every estimator (asserted) |
| 11 | Tie-break | none needed | no tie (asserted) |
| 12 | Maturity and censoring | none: a closed year | the data cover all 8,760 hours (asserted) |
| 13 | Order of operations | conform clocks and codes, convert units, estimate the margin, weight | C1 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | one row per area and hour in the operating data; one row per store and hour in the model | asserted |
| 16 | Identity normalisation | the store to its area through its delivery utility; the former area code to the current | `utility_balancing_area_map.csv`, `balancing_area_codes.csv` (SF10) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | MW over an hour as MWh; kW AC; pounds per MWh and short tons to metric tonnes | the files' own headers (demand_mw, ac_output_kw, co2_2025_short_tons, the publication's lb/MWh); charter 3.4 |
| 19 | Code and status semantics | fuel and prime-mover codes; the imputed-demand flag | the files' own codes as filed; same call (SF8 with imputed hours dropped) |
| 20 | Integerisation | none on the main call | n/a |
| 21 | Clause scope | the charter's measure applies to every candidate alike | charter 3.1 |
| 22 | Forward window contents | none: the measure reads the closed year 2025 | retrospective by the charter's rule (the latest calendar year of complete grid records); the call (where the 2027 array goes) faces forward |

## Literal reader

Executed word for word, the charter's 3.1 to 3.4 define the comparison between 2025 as it ran and 2025 with each array
supplying its store, per MWh of the model's 2025 output, inside the store's balancing area with interchange fixed; the
literal reader must find which of the area's generators produce less in each hour the array generates, which the
operating data show only through their hour-to-hour changes, and every estimator of that response by season and hour
(month by hour, hour alone, UTC hour, demand, fossil or net-generation changes, the register's or the publication's
fuel rates) gives Gorsefield 0.89 and Halvane 0.58; no filed sentence defines an average or non-baseload rate as what
an array avoids.

## Oracles

The publication's average, fossil, fuel and non-baseload rates confirm nothing about the margin and tie on every path;
its fuel output rates are an input every path shares (the register recomputes them to 0.05 lb/MWh). The register's
annual net generation ties to the hourly fuel columns on every path. The supplier's label gives one figure for every
store and ranks nothing. No control ties only under the golden.

## Ask sheet

- **Ask A, each store's 2025 metered electricity use (eight figures, whole MWh).** H18 home: a measure every candidate
  carries that the call does not turn on (the finance team's valuation of the array's output, charter 4.2). Use: the
  valuation's volume line. Path: the invoice export (vendor, invoice number and date, store, account, meter, service
  period, description, quantity, unit, amount: eleven of its fourteen columns) and the store sites (two files).
- **Primary 1 (D4 absence with D2 a label stored before a silent switch): the meter's kilowatt-hours after each store's
  move.** In the spring of 2025 Corvane moved its stores' main utility accounts to Halworth Utility Payment Services in
  three waves (1 March, 24 March, 14 April); from a store's move the utility's bills go to the service, which pays them
  and invoices Corvane weekly with one dollar-only line per bill, so the meter's kilowatt-hours stop reaching accounts
  payable (every main account's own invoices end with the cycle billed at the move, by 4 May). The garden-centre
  accounts at Quillbury and Kestrel Point stayed on direct payment. The only kilowatt-hours left for the rest of the
  year are Ardley Retail Energy's, which bills every meter on the utility's read cycles: under its first term at the
  wholesale delivery point (the meter's kWh times the territory's loss factor, its renewable portfolio standard line on
  the same quantity), and from the first read on or after 1 July 2025, its second term, at the meter with the standard's
  cost in the price (no standard line). The battery's cross-system match (one meter's consumption on two vendors' bills,
  keep one, reconcile the other to it) learns each meter's factor where both bill and divides every later Ardley bill
  by it: right through June, 1.7 to 2.5 per cent under every store from July. Filling the gap as billed is right from
  July and 0.9 to 1.9 per cent over through June. Only the term read from the bills' own structure (the standard line
  gone, the price reset) and confirmed at the two garden-centre meters, which the utility still bills and where Ardley's
  second-term quantity is the meter's kWh exactly, recovers every store. Nothing dates or names the switch.
- **Forcing (asserted on the shipped rows):** in all 80 first-term bills the energy and standard lines carry one
  quantity, 1.0365 to 1.0623 times the meter's kWh to the kWh in every cycle both vendors bill; in the 69 second-term
  bills the garden-centre meters' quantity equals the utility's reading exactly; the golden route recovers every store's
  metered use to 0.002 MWh and its monthly use to 0.001 MWh from the shipped rows; the 101 service lines carry no
  quantity.
- **Hazards:** H1 the same kilowatt-hours on a bill's distribution, transmission and tax lines (every kWh line summed:
  Brackwell 4,866 against 2,373); H2 Tennaford's declining blocks (summed); H3 the garden-centre meters (one meter per
  store moves Quillbury and Kestrel Point only); H4 the cycles straddling the year (counted by days, the prompt's rule).
- **Stops (built, every figure outside its bin, asserted):** the cracker's reconciled fill (Brackwell 2,327); the fill as
  billed (2,406); Ardley's energy as billed for the whole year (2,423); Ardley over the factor for the whole year
  (2,327); the utilities' own invoices alone (395); every kWh line summed (4,866); the golden 2,373.
- **Pin test:** the asking sentence pins the store, the year, metered use and each bill's days pro rata; the device
  sits in which bills carry the meter's kWh after the move and on what basis each Ardley bill states it, which no pin
  names and no filed sentence states (the charter's 4.2 names the figure, the prompt the proration).
- **Realism:** bill-payment outsourcing in waves, with the payment agent's lines carrying amounts only, is how a
  retailer's accounts payable sees its utility bills after the move; retail suppliers bill at the wholesale delivery
  point and reprice at a new term with losses in the price.
- **Ask B, the share of each store's 2025 use its array would have supplied (eight figures, one decimal).** H18 home: a
  qualifier of the array against the store's load (charter 3.3 and 4.2). Construction: the array's 2025 output over Ask
  A's use; inherits primary 1 (the reconciled fill puts every share 0.47 to 0.75 points high, the fill as billed 0.25
  to 0.51 low).
- **Ask C, what Corvane paid per MWh for each store's electricity in 2025 (eight figures, whole dollars).** H18 home: the
  price the finance team values the array's output at (charter 4.2). Construction: every payment for the store's
  electricity for 2025 service (the utilities' invoices, the service's lines, Ardley's invoices), each counted by its
  days in 2025, over Ask A's use; inherits primary 1.
- **Primary 2 (D1 duplication, the over-correction): the bill paid twice at the move.** At seven stores the first bill
  after the move had already reached Corvane and accounts payable paid it while the service paid it too (the service's
  line names the same bill number as the utility's invoice). The utility carried the overpayment as a credit, so the
  service paid that much less on the next bills (Tennaford's and Faraview's next bills at nothing). The battery removes
  the duplicate payment (records matched across two systems, keep one) and leaves each of the seven a bill short; only
  counting every payment as made, which the credits net back to the charges, is right. Forcing (asserted): counting the
  second payment once leaves each store short by exactly the credit the next payments absorbed, and the golden equals
  every store's 2025 charges to the cent. Mass: with every use right, the duplicate removed misses 7 of 8 prices (Halvane,
  whose bills reached the service directly, is the eighth). Pin test: "what we paid" names payments, which the device
  turns on, never how a duplicate and a credit net.
- **Hazards on C:** Halvane Gas & Electric's gas charges (on its own invoices before the move and as the service's
  gas-service lines after it; kept, they move Halvane's price only); the service's lines left out (every price misses).
- **The chart:** each store's 2025 monthly metered use against its array's monthly modelled output; its use bars carry
  primary 1 (the cracker's months from July run 3.5 to 5.9 per cent low).
- **The hourly file:** one row per store and local standard hour of 2025 with the array's output, the hour's marginal
  rate and the CO2 avoided; it carries the main construction.
- **Main population zero-counts (asserted):** the main call reads no invoice row; the asks read no operating-data row
  (zeroed, every ask figure is unchanged) and only the model's annual and monthly output for Ask B and the chart; the
  call's ten files are byte-identical to the 10-15 build (sha256 asserted in checks.py).
- **Hazard table (built):** H1 moves every A, B and C figure for a response summing kWh lines; H3 moves Quillbury's and
  Kestrel Point's for a response taking one meter; the gas lines move Halvane's C only; the service's lines left out
  move every C.
- **Rounding edges (asserted):** every use at least 0.20 MWh, every share 0.036 points and every price $0.26 from its
  rounding edge.
- **Referee:** the two garden-centre meters, which the utility bills directly all year, arbitrate which Ardley line
  changed basis in July without handing over any main meter's level; every other control ties under every handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, 2025 metered use | the utilities' own invoices, then Ardley's energy over the factor learnt where both bill: every store 1.7 to 2.5 per cent low | miss |
| B, share supplied | the array's output over A's use: every share 0.47 to 0.75 points high | miss |
| C, price per MWh | every payment pro rata with the bill paid twice counted once, over A's use: every price 2 to 3 dollars off | miss |
| Chart | the use bars are the cracker's months, July to December low | miss |
| Full includer (reads the July term, counts the bill paid twice once) | keeps the sixteen uses and shares, misses 7 of 8 prices | miss |

- Measured by: generator/ceiling.py on the cut pack (target.zip b0a46e28; standard library only, no generator code):
  the cracker keeps 0 of the 24 use, share and price figures, the eight construction rates, the hourly file and three of
  the chart's four criteria (12 of 37); the mirror on R1 keeps Faraview's rate and the same three chart criteria (4 of 37).
- Pair ceiling: 40.4 (the cracker 38 + 7 + 55 x 12/37 = 62.8; the mirror on R1, 5 + 7 + 55 x 4/37 = 17.9).
- Mirror leakage: 10.8 per cent of ask weight.
- Stress rows (ceiling.py prints them, not the gate): the fill as billed keeps 0 of 24 with or without the duplicate
  removed; the full includer who reads the July term and removes the duplicate keeps 17 of 24 (pair 67.1 with a second
  full includer off the call); the one who also counts every payment as made keeps 24 of 24 (pair 77.6), the residual
  risk recorded here: that response has to see both the term change and the credit.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| UTC hour ending with a local column; the model's local standard hour beginning | the agency's data system; the engineering firm's model | hourly operating data; array model | the model's start read against the operating data's end, an hour either way | the call, the first store left out, the gap and components 1 to 3 unchanged; Brackwell and Tennaford move by up to 0.03 |
| the same clocks joined with the offset ignored (the model's local hour matched to the operating data's UTC label) | the solver, not a system | hourly operating data; array model | a gross error, not a reading: every operating-data row states its local time and offset beside UTC, and both files' headers name their clocks | the call moves to Tennaford (the margin is a matter of the hour); closed by the files, asserted (SF9) |
| Kestrel Point's former code KPLP to 30 June 2025 | the operator's renaming | hourly operating data; codes | a filter on KSTP drops January to June | the call unchanged; Kestrel Point's rate moves 0.003 and keeps its two-decimal figure |
| imputed demand hours, filed from the hour's balance | the operator | hourly operating data | dropped or kept | the eight rates unchanged to two decimals |
| solar station service as small negative MW at night | the operator's net metering | hourly operating data | clipped to zero | no CO2 effect, no figure moves |
| short tons, pounds per MWh, kW | the register, the publication, the model | register; publication; model | not converted | a factor on every rate: the order unchanged |
| run-of-river hydro and nuclear output wandering hour to hour; old coal units at the winter evening peak; peaking units' monthly readiness tests (9 to 11 pm); units at full output a little below nameplate | the plants' operation | hourly operating data | none needed | part of the record every path reads |
| repeated kWh lines, blocks, two vendors for one meter, gas lines, the supplier's loss factor and its July term, the payment service's dollar-only lines, the bills paid twice and their credits | the utilities', the supplier's and the payment service's billing systems; the AP export | invoice export | see the ask sheet | asks only; zero main-call rows |

## Pre-ship check

- **The rubric reship of 2026-11-01 (ask layer only, the call frozen).** The 10-15 version was not returned by the
  portal; it failed the 10-30 gates (leak.py LEAK on the data dictionary and the extract manifest, the prompt's
  rounding opener over its quota, no survivor anatomy, no ceiling script). Scope proved by `freeze.py check task460
  --mode rubric`: every Final Recommendation and Critical Components number, every main-call figures.json value, the
  stump sentence, the card's stump and driver, the ladder and the default path unchanged; 48 ask figures moved; one
  frozen item moved, the prompt's call sentence ("among our eight candidate stores" became "among our candidate
  stores" under the count rule), which `--allow` cannot reach, recorded here and in `## Tried and rejected` rather than
  cleared by editing the gate or retaking the snapshot.
- **Three rules, re-read against the built pack.** The call's ten files are byte-identical to the 10-15 build
  (sha256 asserted in checks.py), so the decisive step, the ladder and every rung stand as the two judge passes read
  them: domain, the emissions inventory's own avoided-emissions factor for a grid-connected project; Layer 2 the margin
  in the array's hours; not a plant, not data semantics, not rule application (checks R2, R3a to R3c re-run green).
  The describing files are gone; SF7, SF9 and SF10 are asserted on the files' own headers and code list. Layer 1 on the
  invoice side is ask-only (zero main-call rows).
- **Gates.** 11 files in 3 formats (csv, pdf, xlsx); the hourly operating data and the array model at 70,080 rows
  each; two distractors (the 2024 edition and the supplier's label); generator checks 115 of 115; `verify.py` from the
  bundle alone on its own route; two builds byte-identical; `figures_check.py` 60 of 60; `precut.py` 61 checks, 0 FAIL,
  0 WARN; `voice-check.py` PASS (no count, every shell class under its quota); `leak.py` REVIEW, no LEAK; container
  clean (H1 audit on target and golden); `guard.py validate` clean; heart BLOCK on four axis bans held by builds
  registered before this one on 10-15 (ban.artifact and ban.forum against task261, 06:16 UTC; ban.shape and
  ban.forcing_event against task455 v2, 07:33 UTC; this card 10:49 UTC), flagged, not relabelled; the same-driver test a
  NOTE (task135, task161, task451 differentiated on the card, task161 added); surface promoted 12 pairs for the
  author's adjudicated read.
- **The ask layer, measured.** `generator/ceiling.py` on target.zip b0a46e28: the cracker keeps 0 of the 24 use,
  share and price figures; pair ceiling 40.4; mirror leakage 10.8 per cent; the full includer's pair 67.1 and the
  residual 77.6 recorded in the ask sheet.

## Leak check

- `leak.py`: REVIEW, no LEAK. Each REVIEW line is harmless: the supplier label's "generator" is an electricity
  generator; the dictionary's 70,080 is the hourly file's own row count; the charter carries the pilot's vocabulary
  (Corvane, site, 2027, solar, pilot, store) and the counterfactual's words without naming a rate, a margin or an hour.
- Reader, first pass (2026-10-15): questions 1 to 4 none (no sentence names the step, no file ranks the stores on the
  question, the dictionary and manifest read as the organisation's own, no figure reads as the answer); question 5
  executed charter 3.2 and 3.3 as displaced generation and reached Gorsefield 0.89, Halvane about 0.59; question 6 an
  analytical choice, the easy route the published average (Brackwell 0.85), the fossil rate (Tennaford) or the
  non-baseload rate (Quillbury 1.12). It flagged average against marginal as the main determinism risk (the judge,
  executing the charter literally, reached the margin; nothing filed) and four realism tells, fixed in the generator:
  peakers with no 2025 output (each now runs its monthly readiness test, 9 to 11 pm on the first Wednesday), units at
  full output sitting on their nameplate for hours (now a little below it, as ambient conditions move it), every array
  facing due south with the roof area scaled from the array (each store's own roof and orientation now); the dates
  against today's date are the fiction's own timeline, internally consistent.
- Reader, second pass on the repaired pack (2026-10-15): questions 1 to 4 none; question 6 an analytical choice (the
  margin in the array's hours against the published average, Brackwell 0.85, or one all-hours marginal rate,
  Tennaford). Question 5 found no filed sentence fixing the method or the hours and named the area average as the
  nearest literal execution: the easy method on the filed estimand, which both judge passes, executing charter 3.2
  and 3.3 word for word, found closed as the response of the area's generators (the hourly records show which ones
  move); filing the method would make the step rule application, so nothing was added. Realism: two peakers of one size
  reporting the same annual output fixed in the generator (each operator's own test level, each unit's own share of
  its block's starts); round nameplates, the old coal units' small 2025 output and extract dates after the charter
  (the charter commissions the analysis) left as they are. The dictionary's station-service, former-code, wholesale
  delivery point and bill-of-record lines stay: the first two are the agency's own notes and the last two the judge's
  determinism pins.

- First pass (2026-10-15, `determinism_check_report.md`): DETERMINISTIC, FIX_NOW (optional). Gate G
  method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain
  pass, layers pass, decisive_step analytical. Every figure reproduced under every estimator the thread tried. The
  findings, all on the asks, fixed in one generator pass: the dictionary now files the supplier's billing at the
  wholesale delivery point against the utilities' meter readings, the later invoice as the bill of record, and tax
  lines as charges; the 2025 rates release moved before the charter's approval (8 September 2026). Left as they are:
  the hour-matched average (the charter's counterfactual and the hourly records rule it out; filing the word marginal
  would file the method) and the chart's monthly basis (loosely gradable by design).
- Re-judge after FIX_NOW (2026-10-15, `determinism_check_report_pass2.md`): DETERMINISTIC, APPROVE. Gate G
  method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain
  pass, layers pass, decisive_step analytical; every figure reproduced under season by hour, hour alone and month by
  hour; the asks reproduce with the dictionary's pins; stump power moderate to good. Its three weak forks move no
  call: the single fossil output rate (Tennaford, against the publication's fuel-specific rates), a regression on
  levels rather than changes (seasonally confounded, not the counterfactual), a slope without an intercept (gap 0.29).
  If a portal finding names one, the repair files the WHAT (fuel-specific CO2, change on change), never the grouping.

- `leak.py` on the reship (2026-11-01, --asof 2026-11-13, pack b0a46e28): REVIEW, no LEAK; the dictionary and
  manifest LEAKs are gone with the files and the metadata title and subdomain lines reworded. Each REVIEW line ruled
  here: the agency's Notes sheets in both editions are its own methodology for its own table (coverage, net generation,
  each rate's definition), harmless; the label's "generator" is a power plant in disclosure boilerplate, harmless; the
  charter's pilot vocabulary (the answer-figure sweep) names the measure, the records and the memo, never a store,
  harmless; the stump-vocabulary sweep's 11 of 25 terms in the charter are its counterfactual's own words (3.2 the
  generators of the store's balancing area, 3.3 does not change with the array's output, 5.1 the hourly operating data
  and the published rates), naming no rate, margin, hour or estimator, harmless (the reader's question 1 found nothing
  cold).
- Reader on the reship (2026-11-01, `leak_check_report.md`): questions 1 to 4 none; question 5 executed charter 3.2 to
  3.4 as the carbon dioxide the area's generators avoid hour by hour from the array's output, leaving which generators
  respond and which rate open (the same reading the two judge passes closed as the response of the area's generators);
  question 6 an analytical choice; REVIEW items a to c harmless; no narration. Realism: the supplier's store-keyed
  account and invoice numbers fixed in the generator (random accounts, one running invoice sequence with gaps, its own
  random stream so no other draw moved; ceiling unchanged at 40.4); the store-keyed feasibility-study and model-run
  identifiers, the near-constant tilt and DC-to-AC ratio, the inverter clipping and the all-operating register are in
  the call's files, byte-identical to the 10-15 build two readers accepted, and stay. The reader does not re-run: the fix
  is data only (`leak.py` re-run, REVIEW unchanged).

- Judge pass 3 on the reship (2026-11-01, `determinism_check_report_pass3.md`, pack b0a46e28): DETERMINISTIC, APPROVE.
  Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H
  domain pass, layers pass, decisive_step analytical. Every call figure and all 24 use, share and price figures
  reproduced from the bundle (use with the supplier's first-term bills over the loss factor and its second-term bills
  as billed). Surviving fork: the levels regression pass 2 already named (same call and first store left out, gap
  0.32), left as pass 2 ruled (filing change-on-change would file the method). Rejected readings it named: the loss
  factor applied to the second term (every use about 2 per cent low; the data support as billed), the duplicate
  dropped without its credit (prices 4 to 9 dollars off), invoice-date years (breaks the pro rata rule).

## Tried and rejected

- 2026-10-15, draw: the seed's own quantity, the all-in price a kWh saves under two bills (delivery and supply) counted
  once. Rejected: counting the delivery-only rows' kilowatt-hours once is reading a part code (data semantics), and the
  price an array saves (the avoidable volumetric rate) is tariff analysis, a task type with no ETL objective.
- 2026-10-15, build: the first cut's realism pass (nuclear, interchange and loaded units given their hour-to-hour drift)
  put Gorsefield's figure at 0.8953, on the 0.895 rounding edge, and split Tennaford's between 0.41 and 0.42 across
  estimators, while the morning flip at 6 am moved Gorsefield's figure with the clock. Rejected that calibration: the
  coal fleet now follows Gorsefield's load from 5 am, Tennaford's business day runs to 6 pm, the coal and gas rates are
  set so every figure sits mid-bin under every estimator, R2 is the one annual marginal rate an analyst fits (Gorsefield
  2nd on the hour-bin average, which is a reflex), and component 3 is Quillbury's, which no clock reading moves.
- 2026-11-01, measured before any document work: the 10-15 ask layer's honest ceiling on its own cut pack (target.zip
  04008e07, a standalone cracker in the session scratchpad: the utility's distribution quantity once per meter and
  cycle, the latest invoice per meter and period, the supplier's wholesale-point quantities left out as the dictionary
  filed, the gas lines dropped, every bill prorated) kept 24 of 24 use, share and price figures: pair 77.6 (cracker
  100, mirror 55.1). Every device was a battery step or a dictionary fact: D6 the kWh on every charge line (taken
  once), D3 the supplier at the wholesale delivery point and D2 the later invoice as the bill of record (both filed in
  the dictionary), D5 Halvane's gas lines (labelled Gas). Replaced by primaries 1 and 2 (the ask sheet).
- 2026-11-01, the data dictionary and the extract manifest removed (leak.py LEAK on both under the 10-30 gates); the
  main call's forks they closed (SF7, SF9, SF10) are asserted on the files' own headers and code list.
- 2026-11-01, the estimated-then-actual re-bills (the old H2) cut: without the dictionary's bill-of-record line the
  later invoice's standing would rest on an unstated rule (task189 and task195 failed the judge on such conventions),
  and no device in the new layer needs them.
- 2026-11-01, the supplier on calendar months (the 10-15 layout) replaced by billing on the utility's read cycles: with
  the supplier the only kilowatt-hours after a store's move, a calendar month straddling the meter's last own cycle,
  split by days, lands 1 to 4 MWh off the meters (the verifier's first run on the new layer), an open reading; billed
  on the same cycles, the two vendors match bill for bill.
- 2026-11-01, the prompt: the rounding sentence reworded at the role level ("give" opened it, 38 per cent of the
  corpus); the call sentence's "eight candidate stores" became "candidate stores" (the count rule; voice-check's
  pattern misses an adjective between the number and its noun). `freeze.py --mode rubric` reports the call sentence
  moved and its `--allow` reaches figures.json keys only, so the FAIL is recorded with its one item and the gate left
  as it is.
