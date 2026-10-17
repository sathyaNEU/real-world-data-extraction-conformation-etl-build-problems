# task464 design note: Wendlemere accelerator advisor slate (architecture 1)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task464.json`, registered 2026-10-17, guard PASS. The first keying (gap
  time, pattern A, Gate G forecasting) blocked on `test.same_driver_older` against seven older builds; keyed again on
  the skill's own definitions (below), which also reads truer to the mechanism. Personas re-drawn from the same
  `guard.py names` list after a first-name WARN.
- **Seed:** ET21 (`analytical_tasks/07_data_extraction_conformation`), world, decision and quantity only: a city-funded
  building decarbonization accelerator assigns its advisors to the covered buildings in one community district with the
  largest expected penalty under a building emissions limits law. The seed's own mechanism (a benchmarking file's
  greenhouse gas column against the law's coefficients, the largest use type's limit for a mixed-use building, campus
  rows) is data semantics and rule application; it survives only as Layer 1, lower rungs and ask hazards.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL, own pattern weather-normalized emissions on
  the current operating regime. A building-level emissions inventory for a city's covered buildings, conformed from the
  utility's whole-building bills, the steam utility's statements and two oil dealers' tickets into one energy record and
  turned into each building's emissions by the law's coefficients, is emissions inventory work; weather normalization
  of building emissions is part of the field's inventory practice (temperature-adjusted series, like-for-like portfolio
  inventories). The last three draws are genomics, safety signals and provider quality (all anomaly detection); this
  task type last carried task263, nine builds back, and before it my lane's task462 and task460 (which share none of
  this mechanism).
- **Why this task type and mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457),
  capture and coverage of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450),
  a rotating panel's measurement change (453), a stratified sample on a revised map (452), latent classes (456),
  partial observation selected on the trait (458), an operating level (459), a dispatch margin (460), a record extended
  through an auxiliary series (461), detection-weighted snapshots (462) and a drift-free price index (463); none
  normalizes a unit's output to a standard year of an external driver, and none has to find, inside each unit's own
  record, the point from which the record describes the unit being decided.
- **Shape:** 01, a ranked list under a cap (twelve advisor places): the twelve (each one's 2027 penalty), the first
  property left out, its gap to the twelfth and a chart of the thirteen; the asks and the conformed record add 19.
- **Strategy:** forecast_method_backtest (a regime change inside each building's own record makes the natural fit, over
  the whole record or the latest twelve months, wrong out of sample on its own latest bills), on the population gap (a
  building's bills from before its last change in how it runs describe a building that is no longer the one decided)
  with the time gap behind it (the record's weather against the normal year). Generators G4 (each record split at its
  own change), G13 (the record's horizon against the normal year as run now) and G16 (a degree-day model over a ratio
  of degree days). Gate G forecasting.
- **World:** Wendlemere, an invented city in the northeastern United States. Its Local Law 18 of 2022 sets annual
  emissions limits on covered properties (over 25,000 square feet) by occupancy group for 2024 to 2029, converts each
  fuel to tonnes of CO2e by a schedule of coefficients and charges $275 a tonne over the limit. The Wendlemere Building
  Decarbonization Accelerator, run under a city contract by the nonprofit Wendlemere Building Futures, gives covered
  properties a year of free technical advisors; its 2027 cycle has twelve advisor places in Community District 4, 158
  covered properties (multifamily heated by oil, gas, district steam or packaged heat pumps, mixed-use blocks, a few
  hotels and offices). Data: Wendlemere Electric & Gas's whole-building billing export (electricity and gas, December
  2022 to September 2026), Wendlemere Thermal's steam statements, Dunmarrow Fuel Oil's and Velsby Brothers Petroleum's
  delivery tickets, the utility account crosswalk, the covered buildings register, the Lindqvist Field airport's daily
  weather record from 1991 and its 1991 to 2020 normals; for the asks, the benchmarking filings for 2023 to 2025, the
  Department of Finance's penalty ledger and its tax lot changes.
- **Forcing fact:** the 2027 cycle runs January to December 2027 and the slate goes to the city's Office of Climate and
  Environment for sign-off by 20 November 2026; the call faces forward (the penalty each property would owe for 2027)
  on a record that closes at the end of September 2026.
- **Forum and forcing event:** funder_or_donor (the city's Office of Climate and Environment funds the advisors and
  signs off the slate), launch_or_rollout (the 2027 advisory cycle). Organisation nonprofit_or_charity; role
  field_unit_lead. Personas from `guard.py names --geo "United States" --seed 464`: Kelli Pierce (the accelerator's
  district lead for Community District 4, who issues the cycle rules), Nicholas Clay (an advisor).
- **Data-native sentence:** Wendlemere's covered buildings are partway through their own decarbonization, so three and
  a half years of a building's bills often hold two buildings, the one before a boiler was replaced, heat pumps went in,
  a hot water plant was converted or a tenant fitted out and the one after, on a date no file records; nineteen of the
  district's 158 buildings made such a change between December 2025 and February 2026, inside the latest twelve months,
  so their records are mostly the building that no longer exists.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, forecasting and uncertainty: model choice on out-of-sample
    error; here a degree-day model fitted across a building's change in how it runs fails on its own latest bills.
  - `stumping/references/client/two-layer-task-design.md`, the field's own method: building energy analysts estimate a
    building's normal-year use with inverse degree-day models over a baseline period that represents current
    operation (the measurement and verification practice); this build makes the baseline period the decisive choice.
  - `dataset-generation/references/layer1-messiness.md`: several feeds for one picture, billing periods off the
    calendar, estimated reads trued up later, delivered fuel as tank fills, units per fuel, imperfect keys, a weather
    record in tenths of a degree Celsius; none on the decisive step.
- **Same-puzzle and abstraction:** gap population, G4, Gate G forecasting, decision ranked_slate_under_cap: guard PASS.
  Nearest drivers 0.06 to 0.10 (task182, task51 lineage, task460, task445 v1, task32 v2 lineage). task182 measures an
  effect as the gap between a level and each unit's driver-only path fitted before a known start; here no effect is
  measured, the change in each building is undated and is found from its own series, and the quantity is a forward
  normal year on the regime that holds now. task32 v2 fitted a conversion rate jointly across one dated regime break;
  here each of many units carries its own undated change, or none.

## Default path

1. Read the accelerator's 2027 cycle rules: the twelve places go to the covered properties in the district that would
   owe the largest penalties under Local Law 18 for calendar year 2027, with the year's weather at the 1991 to 2020
   normal at Lindqvist Field, each estimated from the property's own bills, statements and delivery tickets through 30
   September 2026.
2. Read the law's schedule: each fuel's coefficient and energy per unit (Table 1), each occupancy group's limit for 2024
   to 2029 (Table 2), the limit as the sum over the register's occupancy areas, $275 a tonne over it.
3. Conform the records: Wendlemere Electric & Gas's bills (gas in CCF times each period's therm factor), Wendlemere
   Thermal's statements (the 2025 and 2026 sheets in pounds), the two dealers' tickets (gross gallons, fill to fill),
   each account to its property through the crosswalk for the dates it served it; Lindqvist Field's daily mean
   temperature from TMAX and TMIN, heating and cooling degree days at base 65 F.
4. Fit each fuel's degree-day model (use per day on heating and cooling degree days per day, each span weighted by its
   days) over the property's whole record and evaluate it at the normals (4,735 heating and 1,048 cooling degree days).
5. Price each property's 2027 emissions over its limit at $275 a tonne and take the twelve largest.

- **Ends on:** the whole-record slate, with 429 Quillen Avenue ($154,452), 461 Tallman Street ($143,441) and 173 Orrin
  Place ($140,659) in place of 758 Fenwright Avenue, 843 Merrow Street and 137 Ashlar Street (13th, 18th and 16th on it).
- **Golden:** 808 Thornwick Avenue, 686 Fenwright Avenue, 76 Thornwick Avenue, 34 Thornwick Avenue, 62 Merrow Street, 157
  Lattermore Place, 185 Brennick Avenue, 758 Fenwright Avenue, 151 Orrin Place, 843 Merrow Street, 937 Haddon Street and
  137 Ashlar Street, from each fuel's degree-day model fitted on the spans since the property last changed how that
  fuel's use responds (found in its own record) and evaluated at the normals.

## Stump sentence

The default path fits each fuel's degree-day model over the property's whole record and files a slate with 429 Quillen
Avenue, 461 Tallman Street and 173 Orrin Place in place of 758 Fenwright Avenue, 843 Merrow Street and 137 Ashlar Street,
because those three replaced a boiler or put in heat pumps between 29 December 2025 and 3 February 2026 and three
years of their bills still describe the plant they had (their heating fuel's bills since then run 10 to 20 per cent
under the whole-record model at the same weather); the obvious correction, the latest twelve months, still straddles
those changes and keeps 461 Tallman Street and 173 Orrin Place in.

## Three rules

- **Task type:** physical-environmental-sciences/emissions-inventory (serves ETL): a building-level emissions inventory
  of a city district's covered properties, conformed from a utility's, a steam company's and two oil dealers' records
  into one energy record and converted to emissions by the law's coefficients.
- **Domain test:** the deciding quantity is each property's emissions in a year of normal weather as it now runs,
  estimated the way building energy analysts estimate it: inverse degree-day models of each fuel over its billing
  periods or fill intervals, a baseline period that represents the building's current operation, and the station's
  1991 to 2020 normals, priced against the law's limit.
- **Swap:** "which twelve buildings would owe the largest penalty in a year of normal weather as they now run" with a
  clinic's nouns ("which twelve clinics would see the most visits in a normal flu season as they now operate") loses
  what decides it: a heating plant's response to degree days, a hot water and cooking load the weather does not drive,
  a cooling response in the summer bills, and a retrofit that changes the response partway through the bills.
- **Layer 1:** Wendlemere Electric & Gas's export (billing periods off the calendar, estimated reads trued up at the next
  actual read, gas in CCF with a heat factor per period, accounts replaced after service upgrades), Wendlemere
  Thermal's statements (thousands of pounds, then pounds and a text period from its 2025 billing system), two oil
  dealers' tickets in their own layouts (a Y/N fill flag against FILL and PARTIAL, gross and net gallons, two grades
  under three product names, partial deliveries in the 2022 to 2023 season), the airport's daily record in tenths of a
  degree Celsius with missing days and flagged values, and for the asks lots with and without separators and the
  portal's own greenhouse gas column. Each comes from the system that writes it; nothing is placed to be caught, and
  each mishandled leaves the call and every graded 2027 figure where they are (`## Layer 1 inventory`, asserted).
- **Layer 2:** field_method (and forecasting and uncertainty behind it): the choice that flips the call is the baseline
  period each property's degree-day models are fitted on, the stretch of its own record since it last changed how it
  runs, found from the record itself.
- **Decisive step:** a property whose response to the weather, or whose fixed draw, stepped partway through the record
  has two models in its bills; its 2027 at normal weather comes from the bills after the step, found by the fit that
  breaks there, while a model over the whole record, or over the latest twelve months when the step falls inside them,
  describes a building that no longer exists.
- **Not semantics:** every field read correctly (billing periods, read types, heat factors, steam pounds, gallons, grades
  and fill flags, the weather record's units and flags, the register's occupancy areas, the law's coefficients) still
  leaves a model fitted over the whole record, or the latest twelve months, on the wrong slate; no field, code, flag or
  account records a property's change in how it runs.
- **Not rule application:** the law turns energy into tonnes and tonnes over the limit into dollars, and the cycle rules
  fix the quantity (the penalty for calendar year 2027 at the normal weather, from the property's own records through
  30 September 2026); nothing states how a property's 2027 is estimated from its records or which of them describe how
  it runs now, so executing every stated rule on a fit over the whole record files the wrong slate.
- **Analyst test:** a strong analyst who conforms every bill, statement and fill correctly, reads the law and the cycle
  rules and fits each fuel's degree-day model the usual way, over the whole record (the default path) or over the
  latest twelve months, evaluated at the normals, files a slate with 461 Tallman Street and 173 Orrin Place in (and on
  the whole record 429 Quillen Avenue), in place of 843 Merrow Street and 137 Ashlar Street (and 758 Fenwright Avenue).
- **Estimand:** the cycle rules 2.1: the twelve covered properties in the district that would owe the largest penalties
  under Local Law 18 for calendar year 2027, with the year's weather at the 1991 to 2020 normal at Lindqvist Field, each
  estimated from the property's own records through 30 September 2026 (the bills, the statements and the tickets);
  every one of the register's 158 properties is a candidate, and the law's schedule converts and prices.
- **No decoy:** no document gives a 2027 figure, a normal-year figure, a penalty estimate or a ranking; nothing records a
  retrofit, conversion or fit-out, and no document describes or endorses a normalization or argues for a slate; the
  owners' filings and the city's ledger, read only by the asks, describe 2025 as filed and billed.
- **No certified replay:** no published or certified figure is reproduced by the golden method and missed by another;
  the 2025 filings and billing are not a control any 2027 method must replay.
- **Lesson:** a building's expected compliance exposure is a weather-normalized year on the regime it runs in now: a
  model fitted across a retrofit describes neither building, and a recent window that straddles the retrofit does too.
  No build on file normalizes an output to a standard year of its driver or locates each unit's own regime.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| The owners' 2025 filings as reported (three swaps) | the cycle rules 2.1 name the bills, statements and tickets and the 2027 normal weather | the filings carry each fuel for 2025 | yes: take the latest reported year | no | no | one product per property | readable |
| The 2025 filings with the heating fuels scaled by 4,735 over 4,142 degree days (three swaps) | 2.1 as above | as above | yes: a degree-day ratio | no | no | one ratio | readable |
| Each fuel's degree-day model over the whole record (the default path, three swaps) | 2.1 "estimated from the property's own records through 30 September 2026" reads as all of them | bills, statements and tickets for every property | yes: fit everything | no | no | one regression per fuel | readable |
| The same model over the latest twelve months (two swaps) | 2.1 asks for 2027, the year ahead | the records end 30 September 2026 | yes: recent data for current operation | no | no | one regression per fuel | readable |
| The whole record with a linear time trend to mid-2027 (two swaps) | none | none | yes: a trend for drift | no | no | one regression per fuel | readable |
| Each fuel's model fitted on the spans since the property last changed how that fuel's use responds, the change found in its own record (decisive) | no: the rules fix the quantity and the records, and no sentence names a change, a baseline period, a break or a regime | no column, flag, note or account marks a retrofit; the account replacements fall on dates unrelated to any change near the cut (asserted) | no: every reflex (all records, the latest year, a trend, a ratio, a heating-only model) files a wrong slate | no: nothing reports 2027 or a normal year; the 2025 filings and ledger describe 2025 | no: every bill and ticket is valid and the battery finds nothing | no: a break search on each stream of each property | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | covered property | the register's covered property ID, its accounts through the crosswalk | a tax lot or a building | same call (no property near the cut shares an account or a lot) | the law's 103-01(a); asserted |
| SF2 | in the district | the register's 158 properties, all in Community District 4 | none in the files | same call | the register (DISTRICT 4 on every row); asserted |
| SF3 | penalty under Local Law 18 for calendar year 2027 | $275 a tonne over the limit, Table 1 and Table 2 for 2024 to 2029, nothing below zero | the 2030 limits | not 2027 | Table 2's caption; 103-04(b) |
| SF4 | the limit | the sum over the register's occupancy areas of area times the group's limit | the largest group's limit on the whole floor area | a different slate (four swaps) | the law's 103-03(a) |
| SF5 | the year's weather at the 1991 to 2020 normal | 4,735 heating and 1,048 cooling degree days, the sums of the normals file's monthly normals, base 65 F | the annual means of the daily record for 1991 to 2020 | same call, every graded figure in its bin | the cycle rules 2.1 and the dictionary (the normals file); asserted |
| SF6 | weather terms in the model | heating and cooling degree days | heating degree days alone | same slate; the order of 151 Orrin Place and 843 Merrow Street and the gap move | the bills: every slate property's electricity carries a cooling response (t of 36 or more) and a heating-only fit leaves 67 to 1,250 times the residual; asserted |
| SF7 | the property's own records | its bills, statements and tickets, each account while the crosswalk has it serving the property | the owners' 2025 benchmarking filings | a different slate (three swaps) | the cycle rules 2.1 list the records |
| SF8 | through 30 September 2026 | bills whose period ends by then, deliveries dated by then | bills that start by then | same call: no bill or ticket in the pack runs past 30 September 2026 | the cycle rules 2.1 and 3.1; asserted |
| SF9 | an account's dates | the crosswalk's VALID_FROM and VALID_TO | the account alone, dates ignored | same call | the crosswalk; asserted |
| SF10 | gas quantity | CCF times the period's THERM_FACTOR, in therms | one average factor; CCF read as therms | one factor: same call; CCF as therms is not a reading of the export | the dictionary (UOM CCF, THERM_FACTOR therms per CCF) and Table 1 (therm); asserted |
| SF11 | steam quantity | thousands of pounds, the 2025 and 2026 sheets' pounds over 1,000 | pounds read as thousands | not a reading: the 2025 header says pounds and only the conversion joins the 2024 and 2025 sheets | the dictionary; asserted |
| SF12 | oil quantity | gross gallons as metered at the truck | Velsby's net gallons at 60 F | same call | the law's 103-02(b); asserted |
| SF13 | an estimated read | the period it closes measured with the next actual read | each estimated bill as read | same call | the dictionary (READ_TYPE); asserted |
| SF14 | a partial delivery | the tank measured fill to fill, a partial adding to the next fill | every delivery taken as a fill | same call | the dictionary (TANK_FILLED, FILL or PARTIAL); asserted |
| SF15 | the twelve largest | ranked on the unrounded 2027 penalties | ranked on the rounded penalties | same call: the 12th ($75,180) and 13th ($68,388) round apart | the cycle rules 2.1; asserted |
| SF16 | the gap | the twelfth's unrounded penalty less the thirteenth's, then rounded to $1,000 | the difference of the rounded penalties | $5,000 against $7,000 | the prompt rounds the gap to $1,000, which a difference of $5,000-rounded penalties could never need |
| SF17 | the first property left out | the thirteenth on the same estimate | the thirteenth after removing 2026 advisees | same call | the cycle rules 2.2 (a 2026 advisee may take a place) |
| SF18 | calendar year 2027 | 365 days at the normal year's degree days | none | same call | the cycle rules 1.1 and 2.1 |

## Ladder

| Rung | Construction | Departs from the golden | Nearest the line |
|---|---|---|---|
| below 0 | the owners' 2025 filings as reported, the law applied | 429 Quillen Avenue ($137,528), 461 Tallman Street ($124,851), 173 Orrin Place ($106,959) in; 157 Lattermore Place, 843 Merrow Street, 137 Ashlar Street out (13th, 14th, 16th) | 12th 758 Fenwright Avenue $92,770; 13th 157 Lattermore Place $85,225 |
| below 0 | the 2025 filings, heating fuels times 4,735 over 4,142 | the same three in ($205,273, $204,399, $190,923); 758 Fenwright Avenue, 843 Merrow Street, 137 Ashlar Street out (13th, 14th, 16th) | 12th 157 Lattermore Place $139,190; 13th 758 Fenwright Avenue $127,512 |
| 0, the default path | each fuel's degree-day model over the whole record | 429 Quillen Avenue ($154,452), 461 Tallman Street ($143,441), 173 Orrin Place ($140,659) in; 758 Fenwright Avenue, 843 Merrow Street, 137 Ashlar Street out (13th, 18th, 16th) | 12th 173 Orrin Place $140,659; 13th 758 Fenwright Avenue $128,313 |
| 1, the obvious correction | the same over the latest twelve months (spans from 1 October 2025) | 461 Tallman Street ($111,369), 173 Orrin Place ($99,403) in; 843 Merrow Street, 137 Ashlar Street out (13th, 15th) | 12th 937 Haddon Street $92,651; 13th 843 Merrow Street $91,231 |
| 2, the sophisticated one | the whole record with a linear time trend, evaluated at mid-2027 | 461 Tallman Street ($108,744), 173 Orrin Place ($96,532) in; 758 Fenwright Avenue, 137 Ashlar Street out (14th, 15th) | 12th 157 Lattermore Place $94,008; 13th 429 Quillen Avenue $88,895 |
| 3, the golden | each fuel's model on the spans since its last change, found in the record | none | 12th 137 Ashlar Street $75,180; 13th 633 Lattermore Place $68,388 |

- **The golden slate:** 808 Thornwick Avenue $260,354; 686 Fenwright Avenue $251,002; 76 Thornwick Avenue $239,558; 34
  Thornwick Avenue $159,752; 62 Merrow Street $148,767; 157 Lattermore Place $129,858; 185 Brennick Avenue $119,480; 758
  Fenwright Avenue $100,579; 151 Orrin Place $90,584; 843 Merrow Street $88,578; 937 Haddon Street $81,286; 137 Ashlar
  Street $75,180. First left out: 633 Lattermore Place $68,388; gap $6,792 (to $7,000). Of the 158 properties, 64 owe a
  2027 penalty and the search finds a change in 58.
- **Position:** the golden's twelve sit at 2, 3, 4, 1, 5, 7, 6, 13, 9, 18, 11 and 16 on the default path's ranking; 758
  Fenwright Avenue is 13th there, 8.8 per cent under the twelfth.
- **Margins:** the golden's cut is 1.10 times ($75,180 against $68,388); the three properties the default path brings in
  sit at $46,276, $41,659 and $37,371 on the golden (0.62, 0.55 and 0.50 of the twelfth). The cut holds under every
  variant of the golden method (unweighted fits, flagged values kept, missing days left out, normals averaged from the
  daily record, the generator's true change dates), asserted; a heating-only model,
  which the bills reject, keeps the slate and moves only the order of 151 Orrin Place and 843 Merrow Street and the gap.
- **Dominance:** the three properties the default path brings in changed between 29 December 2025 and 3 February 2026;
  their heating fuel's bills since run 10 to 20 per cent under the whole-record model at the same weather (single winter
  spans 26 to 51 per cent), and the whole record overstates their 2027 penalty 3.3, 3.8 and 3.4 times (429 Quillen
  Avenue, 461 Tallman Street, 173 Orrin Place); the latest twelve months still hold two to four pre-change spans,
  overstating 461 Tallman Street and 173 Orrin Place 3.0 and 2.4 times.
- **Grid:** two choices (the window: whole record, latest twelve months, since the last change; the trend: none or
  linear) give five cells, each a named slate above; the since-the-change window with a trend is not a cell (the trend
  term has nothing to estimate on seven to nine spans and is not asserted).
- **Worth:** the decisive move takes the three late changers' 2027 penalties from $140,659 to $154,452 down to $37,371
  to $46,276 and lifts the three it displaces back into the slate; on the latest twelve months it still moves two.
- **A second wrong route, not on the ladder:** summing each oil delivery into its calendar month and fitting monthly
  files another wrong slate (157 Lattermore Place's 2027 penalty up 50 per cent, 355 Gaskell Avenue into the slate);
  the tickets record deliveries, not use, and the field's method measures a tank fill to fill.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the register's 158 covered properties in the district, every one estimated | the cycle rules 2.1; the register (SF1, SF2) |
| 2 | Unit of account | the covered property, its accounts through the crosswalk | the law's 103-01(a) (SF1, SF9) |
| 3 | Attribution window | records through 30 September 2026, a bill by its period end, a delivery by its date | the cycle rules 2.1 and 3.1 (SF8); no record runs past the date (C1) |
| 4 | As-of dating | the exports as pulled (bills and tickets to 30 September 2026, the register's extract of 1 October 2026) | the dictionary |
| 5 | Version basis | each bill as issued, an estimated period measured with the next actual read | SF13, asserted (C1) |
| 6 | Denominator | none in the call (a penalty is a level); the limit from the register's occupancy areas | the law's 103-03(a) (SF4) |
| 7 | Weighting | each span weighted by its days in the fit | C1: unweighted fits keep every graded figure in its bin (asserted) |
| 8 | Window length | each fuel's spans since its last change, found in its own record; an unchanged fuel's whole record | the decisive step (HOW, forced by the records: a fit across the change mispredicts the property's own latest bills); C1 across the found and the true change dates (asserted) |
| 9 | Boundary inclusivity | twelve places, no tie at the cut | C1: $75,180 against $68,388 |
| 10 | Rounding path | rank on unrounded penalties, round each to $5,000; the gap from unrounded penalties to $1,000 | the prompt (SF15, SF16); asserted |
| 11 | Tie-break | none needed: adjacent slate penalties at least 2.3 per cent apart | C1, asserted |
| 12 | Maturity and censoring | a late changer's own record since its change is seven to nine spans, through a winter, a spring and a summer | asserted: every graded figure holds at the generator's true change dates |
| 13 | Order of operations | conform, assign to properties, find each fuel's change, fit, evaluate at the normals, convert, price | C4: no reordering is defined |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | none: no account and period appears twice | asserted |
| 16 | Identity normalisation | accounts to properties through the crosswalk; Velsby's customer numbers as text | SF9 |
| 17 | Netting against gross | a true-up bill's negative usage nets inside its span | SF13 |
| 18 | Dimensional units | kWh, therms, thousands of pounds, gross gallons; Table 1's coefficients | SF10, SF11, SF12; Table 1 |
| 19 | Code and status semantics | read types (A or E, ACT or EST, Actual or Estimated), fill flags (Y or N, FILL or PARTIAL), product names to grades | the dictionary (SF13, SF14) |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | 2.2 lets a 2026 advisee take a place, so it removes nobody | the cycle rules 2.2 (SF17) |
| 22 | Forward window contents | calendar 2027 at the normal weather, each property as it runs after its last change | the cycle rules 2.1; the records end 30 September 2026 |

## Literal reader

Executed word for word, the cycle rules ask for each covered property's penalty under the law for calendar year 2027
with the year's weather at the 1991 to 2020 normal, estimated from its own bills, statements and delivery tickets
through 30 September 2026; the law converts each fuel and prices the excess over the limit, summed over the register's
occupancy areas. The text leaves open how a property's 2027 is estimated from its records. A reader who fits every
record files the default path's slate, and the records rule that reading out as an estimate of 2027: for each of the
three properties it brings in, its heating fuel's bills since its change (January to February 2026) run 10 to 20
per cent under the whole-record model at the same weather, a winter span by 26 to 51 per cent, so the whole-record model
mispredicts the property's own latest eight months and every month of 2027 it is asked about. The latest twelve months
straddle those changes for 461 Tallman Street and 173 Orrin Place. Every model fitted only on the spans after each
change (found by the search or at the generator's own dates, weighted or not) files the
golden's twelve and the same graded figures. The owners' filings are not among the records 2.1 names.

## Oracles

None ties only under the golden. The owners' 2025 filings and the 2025 ledger (the asks' files) describe 2025 as filed
and billed; they reproduce the filings route's 2025 arithmetic, which is true for 2025, and report nothing for 2027 or
a normal year. The 2025 energy grades score 2025 intensity and the grid's hourly marginal emission rates are not the
law's coefficients; both are declared distractors. No file reports a normal-year figure, a 2027 figure or a change.

## Ask sheet

- **Ask A, for the district's multifamily, mixed-use, hotel and office properties, each type's 2025 Local Law 18
  penalties as the city billed them, net of deductions and reassessments, and how many properties of the type it billed
  (8 figures: four in whole dollars, four counts).** H18 home: the 2025 exposure every candidate carries, by type, read
  beside the slate at the climate office's sign-off; the call does not turn on it. Path: the Department of Finance's
  ledger (BBL, REPORT_YEAR, TRANSACTION, AMOUNT), its tax lot changes (RETIRED_LOTS, NEW_LOTS) and the register
  (TAX_LOTS, PRIMARY_PROPERTY_TYPE): three files, eight columns. Primary device: D7, records billed to a lot since
  retired: six billed properties (three multifamily, one mixed-use, one hotel, one office) had their 2025 lines posted
  in July 2026, before their lots were retired on 31 July 2026 by a condominium declaration or a merger, and the
  register lists their new lots, so the join on the register's lots drops them; the ledger's other districts' lines
  leave the dropped lines among hundreds of unmatched ones. Golden: Multifamily Housing $2,508,379 (46), Mixed Use
  Property $591,784 (10), Hotel $94,657 (2), Office $42,848 (1). Stops (asserted): the register's lots only (the
  cracker) $2,458,453 (43), $566,059 (9), $70,488 (1), $0 (0); payments netted in (H1) Multifamily $741,658 and Mixed
  Use $183,442 (no hotel or office has paid its 2025 penalty yet); the posting year 2026 for the report year (H2) moves
  Multifamily to $2,497,501 (2024 reassessments posted in 2026); assessments alone, before deductions, reversals and
  reassessments (H3) $2,506,685 and $645,030. Realism: a finance
  department keys each line to the lot it was posted to, and a condominium declaration or merger retires lots without
  moving the lines already on them.
- **Ask B, for the same four types, each type's 2025 emissions under the law and site energy on the owners' accepted
  filings (8 figures: whole tonnes, whole million Btu).** H18 home: the district's 2025 inventory by type as owners
  filed it, the baseline the accelerator reports its cycle against; the call does not turn on it. Path: the
  benchmarking export (Report Year, Filing ID, Tax Lot, the five energy columns), the register (TAX_LOTS,
  PRIMARY_PROPERTY_TYPE) and the law's Table 1 (coefficients, energy per unit): three files, eleven columns. Primary
  device: D6, a filing's quantity on every line it covers: the export writes one row for each tax lot of a filing,
  each carrying the property's whole use, so summing the rows counts a multi-lot property once per lot; every type
  holds one. Golden: Multifamily Housing 112,776 t and 1,678,848 million Btu, Mixed Use Property 31,951 t and 456,003,
  Hotel 7,887 t and 119,295, Office 12,292 t and 165,192. Stops (asserted): every row summed (the cracker) 126,293 t
  and 1,871,328, 43,635 and 620,863, 9,890 and 150,116, 15,226 and 205,129; the portal's greenhouse gas column at
  federal factors (H5) 107,500, 28,905, 7,214 and 10,809 t; site energy as Site EUI times the self-reported floor area
  (H6) 1 to 71 million Btu off in every type. Realism: a benchmarking export written by tax lot repeats a multi-lot
  property's filing on each lot's row.
- **The construction layer:** the conformed building energy record (one row per bill or delivery, 16,124 rows, the
  fields of the cycle rules' Table 1); the cracker has it, and the call's own construction feeds it.
- **Main population zero-counts (asserted):** the call reads no ledger, lot change or filing row (the call and every
  graded figure computed with those files deleted are identical); the asks read no bill, statement, ticket or weather
  row (Ask A and Ask B computed with those files deleted are identical). No device or hazard row sits in a file the
  call reads, and no main-call document carries an ask's organ (the law's 103-04 names the penalty only).
- **Hazard table (asserted):** H1 moves Multifamily and Mixed Use; H2 moves Multifamily; H3 moves
  Multifamily and Mixed Use; H5 every Ask B emissions figure; H6 every Ask B site energy figure.
- **Rounding edges (asserted):** every Ask A and Ask B figure is an exact sum of shipped values; each graded 2027
  penalty at least $888 inside its $5,000 bin (633 Lattermore Place; 686 Fenwright Avenue the closest in relative terms,
  0.60 per cent) and the gap $292 inside its $1,000 bin, under every variant of the golden method above.
- **Referee:** none; no total in an ask file ties only under one handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, 2025 penalties billed by type | nets assessments, deductions, reversals and reassessments for report year 2025, leaves out payments and interest, joins the ledger to the register's lots | miss |
| A, properties billed by type | counts the properties with a 2025 assessment on the register's lots | miss |
| B, 2025 emissions under the law by type | takes the accepted filings, converts kBtu by Table 1, applies the coefficients, sums the rows by the register's type | miss |
| B, 2025 site energy by type | sums each row's fuels at Table 1's energy per unit | miss |

- Mirror leakage: 15.8 per cent of ask weight (a response on the latest twelve months runs the same battery and keeps
  only the conformed record's criteria; it misses every Ask A and Ask B figure on the same devices as the cracker).
- Pair ceiling: 38.7 (planning weights 38 / 7 / 55; the main block's 38 as the twelve 8, their order 3, their twelve
  penalties 18 at 1.5 each, the first left out 3, its penalty 2, the gap 2 and the chart 2; the mirror on the latest
  twelve months keeps four penalties in their bins (686 Fenwright Avenue, 76 Thornwick Avenue, 157 Lattermore Place, 758
  Fenwright Avenue) and the chart, r = 4 x 1.5 + 2 = 8; the ask weight over 19 criteria, A 8, B 8, the record 3; the
  cracker keeps the record, 38 + 7 + 55 x 3 / 19 = 53.7; the mirror 8 + 7 + 8.7 = 23.7; average 38.7), rerun from the
  generated rubric at ship.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| estimated reads trued up at the next actual read | the utility's and the steam company's billing | WEG export, Thermal statements | each estimate taken as read | none: slate, order and every graded figure unchanged |
| gas in CCF with a heat factor per period | the utility's billing | WEG export | one average factor (1.037) | none (largest move 2.2 per cent, no bin) |
| steam in pounds with a text period from 2025 | Thermal's new billing system | Thermal statements | the period text split wrongly or pounds read as thousands | not a reading: only the conversion joins the 2024 and 2025 sheets (asserted) |
| two dealers' layouts: Y/N fill flag against FILL and PARTIAL, gross and net gallons, three product names | Dunmarrow's ticketing and Velsby's delivery report | the dealers' files | Velsby's net gallons; partial deliveries taken as fills | none: largest move 1.0 per cent; slate, order and bins unchanged |
| accounts replaced after service upgrades | the utility's account system | crosswalk | the validity dates ignored | none |
| weather in tenths of a degree Celsius with missing days and flagged values | the weather service | Lindqvist Field daily record | flagged values kept; missing days left out of the degree days | none: every graded figure in its bin |
| bills that closed in early 2023 from December 2022 | the billing cycle | WEG export, Thermal statements | dropped from the fits | none |
| lots with and without separators; the portal's own emissions column | the register, the portal, the ledger | asks' files | as the asks' hazards | asks only |

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each covered property's emissions
  in a year of normal weather as it now runs, estimated the way building energy analysts estimate it (inverse
  degree-day models of each fuel over billing periods and fill intervals, on a baseline that represents current
  operation, at the station's 1991 to 2020 normals) and priced against the law's limit; a fit over the whole record
  files the default path's slate, the latest twelve months, a time trend and the owners' 2025 filings each another. Two
  layers: the Layer 1 inventory above, each main-call item asserted neutral (R2 and SF9 to SF14: estimates taken as read,
  one heat factor, Velsby's net gallons, partials taken as fills, the crosswalk's dates dropped, bills before 2023
  dropped, flagged values kept, missing days left out) and each ask device confined to its ask with zero main-call rows
  (the separation checks); Layer 2 the baseline period since each fuel's last change. The decisive step is none of the
  three banned kinds, each executed in `checks.py`: not a plant (R3c: no document names a retrofit, a change, a
  baseline, a break, a regime or a normalization; no column flags one; no account replacement near the cut falls within
  120 days of a found change; no copied run of bills); not data semantics (every field read correctly still leaves the
  whole-record fit on its slate, and every field mishandled leaves the call and every graded figure where they are);
  not rule application (R3a: every filed rule executed with a whole-record fit on the clean truth files the default
  path's slate; R3b: only the fit from each fuel's true last change files the twelve, while the latest twelve months and
  a trend land elsewhere).
- **Gates.** 16 files in 3 formats (csv, pdf, xlsx); the station's daily record at 52,094 rows; two distractors (the 2025
  energy grades and the grid's hourly marginal emission rates) the solution never reads, the call, every rung and both
  asks unchanged with them deleted; 85 checks; `verify.py` from the bundle alone on its own break search; two builds
  byte-identical; `figures_check.py`, `precut.py` (49) and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK, every
  line answered: covered property IDs carry digits, the cycle rules use the estimand's own words, the register, filings
  and grades rank nothing on the 2027 question, the weather record's flag columns are the weather service's own); guard
  heart PASS (nearest task182 at 0.10); surface promoting task462 (two apart, PES x ETL, the population gap), task450
  (retired, the population gap and G4) and task136 (top 1 per cent) for the author's read; containers carry the
  fiction's owners and dates (H1 audit clean); the golden's chart is a PNG inside the workbook (the container
  normalizer had declared every part as XML; it now declares XML parts only, and a check opens every binary part).

## Tried and rejected

- Weather normalization alone, with oil fills and estimated reads as the interval structure: in a prototype of 150
  buildings, a degree-day regression on calendar-month bills with oil deliveries summed by month landed within 2 per
  cent of the fill-to-fill fit for most oil buildings (6 at most) and on the golden's slate, so a strong analyst's
  regression lands the call; the estimated reads and fills are Layer 1 (cleaning them makes the call easy) and stay
  there. The decisive structure is each building's change in how it runs.
- A first keying of the card on the time gap with pattern A and Gate G forecasting: the signature is spent in seven
  older builds; keyed on the population gap with G4 first, which also reads truer (the bills before a change are not
  the decided building).
- The 2025 benchmarking year scaled by degree days as the default path: the cycle rules name the bills, statements and
  tickets as the records, so a competent analyst fits them; the filings route stays below rung 0 and the default path
  is the whole-record fit.
- Ask B on the gap between the filings and the bills for 2025: its golden sat near zero for most types; Ask B now
  carries the filings' own emissions and site energy by type on the export's lot rows.
- A six-day sensor outage in April 2024 in the weather record: leaving missing days out of the degree days moved 808
  Thornwick Avenue and 686 Fenwright Avenue across their $5,000 bins; the outage now sits in April 2019, outside the
  billing years.
- Partial oil deliveries at random on every building: taking them as fills hid one building's boiler change from the
  search and put it in the slate; partials now fall in the 2022 to 2023 season, on no building near the cut, and every
  building away from the cut is held under $55,000 on a whole-record fit.
- The law's billing sentence ("bills it to the property's tax lot and posts any deduction ... against the same
  notice"): an ask organ in a document the call reads, and wrong against the ledger (a reassessment opens a new
  notice); cut.
- Round floor areas on the twenty buildings placed around the cut (each a multiple of 1,000, against none of the other
  138): a giveaway; each now carries an ordinary area and the calibration re-aims.
- Keeping estimated reads and partial deliveries off the buildings around the cut, to hold those items neutral: a second
  giveaway. Every building now carries the same processes: the utility's estimates land within a few per cent, as a
  weather-adjusted routine does (estimates missing by 20 to 40 per cent, read as actual, hid two slate properties'
  changes from the search), none after the advanced meters of October 2025 or the steam company's January 2025 system,
  and partial deliveries stop a few hundred gallons short, in the 2022 to 2023 season only.
- A window started one span after the found break as a variant the golden must hold under: no reader would choose it
  (the first span after a change is wholly post-change), and 62 Merrow Street moves 2 per cent under it; the variant
  asserted is the generator's own change dates.
- Architecture 1, the degree-day fit on each fuel's spans after its last change found in the property's own bills
  (2026-10-17): judged NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, underspecified_objective). The post-
  change window's first span and whether electricity is refit with the heating fuel are open (461 Tallman Street's
  electricity rises 1.35 times when its gas falls; refit, it is the first left out at $70,990 against 633 Lattermore
  Place's $68,577), a step search run as written flags dozens of series and moves four $5,000 amounts, and a $7,000
  12th-to-13th margin sits inside a $40,000 to $57,000 window freedom. Filing the window or a dated change log would make
  the step rule application; an undated change cannot be pinned without it. The architecture is spent and re-rooted.
- A first redraw (architecture 2 on paper, 2026-10-17): each district's claim under a state challenge judged by the
  upper end of its inventory's 95 per cent interval, the decisive move carrying each shared emission factor's error on
  the district's fuel total instead of building by building. The correlated-error lesson is already task228's,
  task229 v1's, task260's and task261's (an error shared by the units does not average away); dropped before
  registration.
