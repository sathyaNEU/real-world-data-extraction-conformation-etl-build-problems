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
  `balancing_area_codes.csv`; `corvane_electricity_invoice_lines_fy2025.csv` (the accounts-payable export of every
  electricity invoice line for the eight stores, the asks' file); `solar_pilot_siting_charter_2027.pdf` (the decision,
  the measure and the timetable); `pilot_siting_data_dictionary.xlsx`; `pilot_siting_extract_manifest.csv`; distractors
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
  charge lines, Tennaford's declining blocks, two cycles billed on an estimate and again on the actual read, Halvane's
  gas service on its electric bill, two garden-centre meters, and the supplier's quantities at the wholesale delivery
  point (the meters' kWh times the territory's loss factor). Each is what the system that writes the file produces; none
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
  respond, in which hours, or how to estimate the response (the charter, the publication's notes and the dictionary are
  scanned for a basis or an estimator and carry none), so executing every filed rule leaves the estimator to the analyst,
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
  email or stakeholder figure ships (the folder is the 13 declared files); the charter names no rate, basis or method;
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
| 4 | As-of dating | the agency's data as pulled 20 October 2026, the 2025 release of 8 September 2026 | the manifest; one vintage of each file |
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
| 18 | Dimensional units | MW over an hour as MWh; kW AC; pounds per MWh and short tons to metric tonnes | the dictionary and the publication's headers; charter 3.4 |
| 19 | Code and status semantics | fuel and prime-mover codes; the imputed-demand flag | the dictionary; same call |
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
  carries that the call does not turn on (the finance team's valuation of the array's output, charter 4.2). Path: the
  invoice export, the store sites, the dictionary and the manifest (four files, eight columns). Primary device: D6, an
  event's quantity on every line it covers: each delivery utility repeats the cycle's kWh on its distribution, its
  transmission and (at three utilities) its kWh-tax lines, while Tennaford bills distribution energy in declining
  blocks (partial quantities that sum) and transmission on demand; a sum of every kWh line runs three to five times high
  and one kWh line per invoice misses Tennaford's blocks. Hazards: H1 the supplier bills the same consumption by
  calendar month at the wholesale delivery point (the meters' kWh times a loss factor of 1.037 to 1.062), so adding it
  doubles the figure and taking it alone runs 3.6 to 6.2 per cent high (D3, scale set per source; the dictionary files the supplier's billing at the wholesale delivery point); H2 two cycles
  (Quillbury in January, Ostlemere in July) billed on an estimate and again on the actual read, both in an export that
  carries invoices only (D2; the dictionary files the later invoice as the bill of record); H3 the garden-centre meters at Quillbury and Kestrel Point; H4 cycles straddling the year,
  counted by days (the prompt's convention). Stops (built, every figure outside its bin, asserted): every kWh line
  (Brackwell 12,102 against 2,381); the largest kWh line per invoice across both vendors (Brackwell 4,861); the supplier
  alone (Brackwell 2,479, every store 3.6 to 6.2 per cent high); both vendors' energy lines (twice the golden); the
  estimated bills kept (Quillbury 2,614, Ostlemere 3,119); invoices dated in 2025 (all eight miss, Brackwell 2,364); one
  meter per store (Quillbury and Kestrel Point); the golden. Realism: line-item bill exports repeat the billed quantity
  on every volumetric charge, and retail suppliers bill at the wholesale point.
- **Ask B, the share of each store's 2025 use its array would have supplied (eight figures, one decimal).** H18 home: a
  qualifier of the array against the store's load (charter 3.3 and 4.2). Construction: the array's 2025 output over
  Ask A's use; inherits Ask A's device and hazards (a doubled use halves the share; the estimated bills kept take
  Quillbury to 20.6 and Ostlemere to 27.7).
- **Ask C, what Corvane paid per MWh for each store's electricity in 2025 (eight figures, whole dollars).** H18 home: the
  price the finance team values the array's output at (charter 4.2). Construction: every electricity charge on both
  vendors' current invoices, counted by days in 2025, over Ask A's use. Primary device: D5, a category crossed by
  label: Halvane Gas & Electric bills the store's gas on the same invoice (gas customer, distribution, supply and tax
  lines), which an invoice-level sum counts as electricity (Halvane $150 against $142). Hazards: H1 inverted (a response
  that drops the supplier to stop double counting kWh also drops the energy charges: every store $54 to $113); H2 (the
  estimated bills' dollars kept: Quillbury $208, Ostlemere $193); Ask A's use as the denominator.
- **The chart:** each store's 2025 monthly metered use against its array's monthly modelled output; its use bars carry
  Ask A's device.
- **The hourly file:** one row per store and local standard hour of 2025 with the array's output, the hour's marginal
  rate and the CO2 avoided; it carries the main construction.
- **Main population zero-counts (asserted):** the main call reads no invoice row (the call and every rung computed
  with the invoice export deleted are identical); the asks read no operating-data row (zeroed, every ask figure is
  unchanged) and only the model's annual output for Ask B.
- **Hazard table (built):** H1 moves every Ask A, B and C figure for a response adding or substituting the supplier's
  quantities; H2 moves Quillbury's and Ostlemere's A, B and C figures; H3 moves Quillbury's and Kestrel Point's for a
  response taking one meter per store; H4 moves every A figure for a response counting by invoice date.
- **Rounding edges (asserted):** every use at least 0.15 MWh, every share 0.03 points and every price $0.15 from its
  rounding edge.
- **Referee:** none needed; no control ties only under the golden.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, 2025 metered use | sums the kWh the invoices bill for 2025 by days, or the supplier's calendar months that need no proration: every store high (the repeated lines, or the supplier's loss-adjusted quantities) | miss |
| B, share supplied | the array's output over A's use: every share low | miss |
| C, price per MWh | the dollars over A's use: every price low | miss |
| Chart | the use bars are A's figures | miss |

- Mirror leakage: about 11 per cent of ask weight (a response on R1 keeps Faraview's rate, 0.39 under both, the hourly
  file's layout and the chart's array bars).
- Pair ceiling: 39.8 (cracker 38 + 7 + 55 x 0.30 = 61.5, keeping the eight construction rates, the hourly file and the
  chart's array bars; the mirror on R1, 5 + 7 + 55 x 0.11 = 18.1; average 39.8), rerun from the generated rubric at build.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| UTC hour ending with a local column; the model's local standard hour beginning | the agency's data system; the engineering firm's model | hourly operating data; array model | the model's start read against the operating data's end, an hour either way | the call, the first store left out, the gap and components 1 to 3 unchanged; Brackwell and Tennaford move by up to 0.03 |
| the same clocks joined with the offset ignored (the model's local hour matched to the operating data's UTC label) | the solver, not a system | hourly operating data; array model | a gross error, not a reading: every operating-data row states its local time and offset beside UTC, and the dictionary names both clocks | the call moves to Tennaford (the margin is a matter of the hour); closed by the files, asserted (SF9) |
| Kestrel Point's former code KPLP to 30 June 2025 | the operator's renaming | hourly operating data; codes | a filter on KSTP drops January to June | the call unchanged; Kestrel Point's rate moves 0.003 and keeps its two-decimal figure |
| imputed demand hours, filed from the hour's balance | the operator | hourly operating data | dropped or kept | the eight rates unchanged to two decimals |
| solar station service as small negative MW at night | the operator's net metering | hourly operating data | clipped to zero | no CO2 effect, no figure moves |
| short tons, pounds per MWh, kW | the register, the publication, the model | register; publication; model | not converted | a factor on every rate: the order unchanged |
| run-of-river hydro and nuclear output wandering hour to hour; old coal units at the winter evening peak; peaking units' monthly readiness tests (9 to 11 pm); units at full output a little below nameplate | the plants' operation | hourly operating data | none needed | part of the record every path reads |
| repeated kWh lines, blocks, two vendors, re-bills, gas lines, the supplier's loss factor | the utilities' and supplier's billing systems; the AP export | invoice export | see the ask sheet | asks only; zero main-call rows |

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the emissions inventory's own avoided-emissions factor for
  a grid-connected project, the operating margin in the project's hours, estimated from the hour-to-hour changes in the
  area's fossil CO2 and weighted by the project's output (the swap in the Three rules section stops reading). Two
  layers: the Layer 1 inventory above, each item asserted neutral to the call and to components 1 to 3 or confined to
  an ask; Layer 2 the margin in the array's hours. The decisive step is none of the three banned kinds, each executed
  in `checks.py`: not a plant (R3c: no copied or flat day in any hourly series or array, the publication recomputes
  from the register, the charter, the publication's notes and the dictionary name no basis or estimator, no memo or
  stakeholder figure ships, the supplier's label ranks nothing); not data semantics (R2: the clock an hour either way,
  KPLP dropped, imputed hours dropped, station service clipped and units unconverted each leave the call and
  components 1 to 3, and every field read correctly still leaves four easy estimators on wrong stores); not rule
  application (R3a: with every filed rule executed, the easy routes on the clean truth file Brackwell, Quillbury,
  Tennaford and Brackwell; R3b: only the margin by season and hour weighted by output files Gorsefield, and it matches
  the generators the dispatch moved).
- **Gates.** 13 files in 3 formats (csv, pdf, xlsx); the hourly operating data and the array model at 70,080 rows each;
  two distractors (the 2024 edition and the supplier's label) the solution never reads; 108 checks; `verify.py` from
  the bundle alone; two builds byte-identical; `figures_check.py`, `precut.py` and `voice-check.py` exit 0; `leak.py`
  REVIEW (no LEAK); guard heart WARN; surface promoting task458 (the prompt's opening, reworded as a where question),
  task459 (the same pairing back to back), task135 and task451 (the same gap, pattern and Gate G, differentiated on the
  card) for the author's read; the containers carry the fiction's people and dates.

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

## Determinism judge

- First pass (2026-10-15, `determinism_check_report.md`): DETERMINISTIC, FIX_NOW (optional). Gate G
  method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain
  pass, layers pass, decisive_step analytical. Every figure reproduced under every estimator the thread tried. The
  findings, all on the asks, fixed in one generator pass: the dictionary now files the supplier's billing at the
  wholesale delivery point against the utilities' meter readings, the later invoice as the bill of record, and tax
  lines as charges; the 2025 rates release moved before the charter's approval (8 September 2026). Left as they are:
  the hour-matched average (the charter's counterfactual and the hourly records rule it out; filing the word marginal
  would file the method) and the chart's monthly basis (loosely gradable by design).

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
