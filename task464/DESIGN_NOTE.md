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
  rows) is data semantics and rule application; it survives only as Layer 1 and lower rungs.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL, own pattern weather-normalized emissions on
  the current operating regime. A building-level emissions inventory for a city's covered buildings, conformed from the
  utilities' whole-building bills, the steam utility's statements and the oil dealers' fill tickets into one energy
  record and turned into each building's emissions by the law's coefficients, is emissions inventory work; weather
  normalization of building emissions is part of the field's inventory practice (temperature-adjusted series, like-for-like
  portfolio inventories). The last three draws are genomics, safety signals and provider quality (all anomaly
  detection); this task type last carried task263, nine builds back, and before it my lane's task462 and task460 (which
  share none of this mechanism).
- **Why this task type and mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457),
  capture and coverage of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450),
  a rotating panel's measurement change (453), a stratified sample on a revised map (452), latent classes (456),
  partial observation selected on the trait (458), an operating level (459), a dispatch margin (460), a record extended
  through an auxiliary series (461), detection-weighted snapshots (462) and a drift-free price index (463); none
  normalizes a unit's output to a standard year of an external driver, and none has to find, inside each unit's own
  record, the point from which the record describes the unit being decided.
- **Shape:** 01, a ranked list under a cap (twelve advisor places). Arithmetic: the twelve slate buildings (12), each
  one's normal-year emissions and penalty (24), the first building outside the slate and its gap to the twelfth (2),
  the asks (sized at stage 2), the chart's named parts (5) and the two files (2): 45 before the asks.
- **Strategy:** forecast_method_backtest (a regime change inside each building's own record makes the natural fit, over
  the whole record or the latest twelve months, wrong out of sample), on the population gap (a building's bills from
  before its last change in how it runs describe a building that is no longer the one decided) with the time gap behind
  it (the record's weather against the normal year). Generators G4 (each record split at its own change), G13 (the
  record's horizon against the normal year as run now) and G16 (a degree-day model over a ratio of degree days). Gate G
  forecasting.
- **World:** Wendlemere, an invented city in the northeastern United States. Its Local Law 18 of 2022 sets annual
  emissions limits on covered buildings (over 25,000 square feet) by occupancy group for 2024 to 2029, converts each
  fuel to tonnes of CO2e by a schedule of coefficients and charges $275 a tonne over the limit. The Wendlemere Building
  Decarbonization Accelerator, run under a city contract by the nonprofit Wendlemere Building Futures, gives covered
  buildings a year of free technical advisors; its 2027 cycle has twelve advisor places in Community District 4, about
  150 covered buildings (multifamily heated by oil, gas or district steam, offices, a hotel group, schools, retail and
  mixed-use blocks). Data: Wendlemere Electric & Gas's whole-building billing export (electricity and gas, January
  2023 to September 2026), Wendlemere Thermal's steam statements, two heating oil dealers' delivery tickets, the city's
  benchmarking submissions for 2023 to 2025, the covered buildings register, and the Lindqvist Field airport's daily
  weather record from 1991.
- **Forcing fact:** the 2027 cycle opens in January 2027 and the city's climate office signs off the slate before
  then; the call faces forward (which buildings the advisors take on for 2027) on a record that closes at the end of
  September 2026.
- **Forum and forcing event:** funder_or_donor (the city's Office of Climate and Environment funds the advisors and
  signs off the slate), launch_or_rollout (the 2027 advisory cycle). Organisation nonprofit_or_charity; role
  field_unit_lead. Personas from `guard.py names --geo "United States" --seed 464`: Kelli Pierce (the accelerator's
  district lead for Community District 4), Nicholas Clay (an advisor).
- **Data-native sentence:** Wendlemere's covered buildings are partway through their own decarbonization, so three and
  a half years of a building's bills often hold two buildings, the one before a boiler was replaced, heat pumps went in,
  a hot water plant was converted or a tenant fitted out and the one after, on a date no file records; and the years
  they cover ran milder than the 1991 to 2020 normals, around hot water and cooking loads the weather does not drive.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, forecasting and uncertainty: model choice on out-of-sample
    error; here a degree-day model fitted across a building's change in how it runs fails on its own latest months.
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

1. Read the accelerator's 2027 cycle rules: the twelve advisor places go to the covered buildings in Community
   District 4 with the largest penalty each would owe under Local Law 18 for a calendar year of normal weather (the
   1991 to 2020 normals at Lindqvist Field) as the building runs now.
2. Read the law's schedule: each fuel's coefficient, each occupancy group's limit per square foot for 2024 to 2029,
   $275 a tonne over the limit.
3. Take each covered building's 2025 benchmarking submission, the latest year reported under the law: its energy by
   fuel, a campus's buildings from its parent row; its limit from the register's floor area by occupancy group.
4. Normal weather the usual way: scale each heating fuel (gas, steam, oil) by the ratio of the normal year's heating
   degree days to 2025's at Lindqvist Field; leave electricity as reported.
5. Price each building's excess over its limit at $275 a tonne and take the twelve largest.

- **Ends on:** a slate of twelve that departs from the golden's where scaling a whole heating fuel inflates hot water
  and cooking loads the weather does not drive, and where 2025 mixes two ways of running (the names, the count of
  departures and each margin are fixed at stage 2 by calibration, targeting three or four departures).
- **Golden:** the twelve buildings with the largest penalty from degree-day models of each fuel (billing periods for
  metered fuels, fill-to-fill intervals for oil, heating and cooling terms where the bills show them) fitted on the
  bills since each building last changed how it runs and evaluated at the 1991 to 2020 normals.

## Stump sentence

The default path takes each building's 2025 benchmarked energy, scales its heating fuels by the ratio of normal to 2025
heating degree days and files a slate that departs from the golden's, because the ratio scales hot water and cooking
loads the weather does not drive and a 2025 year that straddles a building's change in how it runs describes neither
building; a strong analyst's degree-day regression over each building's whole record, or over its latest twelve
months, files a second wrong slate, because the buildings near the line that changed how they run partway through the
record are modelled across the change (the slates, their names and margins fixed at stage 2).

## Three rules

- **Task type:** physical-environmental-sciences/emissions-inventory (serves ETL): a building-level emissions inventory
  of a city district's covered buildings, conformed from three utilities' and two oil dealers' records into one energy
  record and converted to emissions by the law's coefficients.
- **Domain test:** the deciding quantity is each building's emissions in a year of normal weather as it now runs,
  estimated the way building energy analysts estimate it: inverse degree-day models of each fuel over its billing
  periods or fill intervals, a baseline period that represents the building's current operation, and the station's
  1991 to 2020 normals, priced against the law's limit.
- **Swap:** "which twelve buildings would owe the largest penalty in a year of normal weather as they now run" with a
  clinic's nouns ("which twelve clinics would see the most visits in a normal flu season as they now operate") loses
  what decides it: a heating plant's response to degree days, a hot water and cooking load the weather does not drive,
  and a retrofit that changes the response partway through the bills.
- **Layer 1:** Wendlemere Electric & Gas's whole-building export (billing periods off the calendar, estimated reads
  trued up by the next actual read, gas in hundreds of cubic feet with a heat content factor per period), Wendlemere
  Thermal's statements in thousands of pounds of steam with a layout change in 2025, two oil dealers' tickets in their
  own layouts (fills and flagged partial deliveries, two grades), the benchmarking file's own greenhouse gas column at
  federal factors and a campus under one parent row, borough-block-lot numbers with and without separators, a utility
  account crosswalk, and the airport's daily record in tenths of a degree Celsius with missing days. Each comes from the
  system that writes it; nothing is placed to be caught, and each mishandled leaves the call and the critical components
  where they are (asserted per item at stage 3).
- **Layer 2:** field_method (and forecasting and uncertainty behind it): the choice that flips the call is the baseline
  period each building's degree-day models are fitted on, the stretch of its own record since it last changed how it
  runs, found from the record itself.
- **Decisive step:** a building whose response to the weather, or whose fixed draw, stepped partway through the record
  has two models in its bills; the normal year as it runs now comes from the bills after the step, found by the fit
  that breaks there, while a model over the whole record, or over the latest twelve months when the step falls inside
  them, describes a building that no longer exists.
- **Not semantics:** every field read correctly (billing periods, read types, heat content, steam pounds, gallons and
  grades, the weather record's units and flags, the register's occupancy areas, the law's coefficients) still leaves a
  model fitted over the whole record, or the latest twelve months, on the wrong slate; no field, code or flag records a
  building's change in how it runs.
- **Not rule application:** the law turns energy into tonnes and tonnes over the limit into dollars, and the cycle rules
  fix the quantity (the penalty for a calendar year of normal weather as the building runs now); nothing states how a
  building's normal year is estimated or which of its bills describe how it runs now, so executing every stated rule on
  the 2025 benchmarked year, or on a fit over the whole record, files a wrong slate.
- **Analyst test:** a strong analyst who conforms the bills, fills and weather correctly, reads the law and the cycle
  rules and normalizes each building the usual way, a degree-day regression of each fuel over its whole record or over
  its latest twelve months evaluated at the 1991 to 2020 normals, files a slate that keeps buildings whose record mixes
  the plant they had with the one they run now and drops buildings that changed the other way; the default path's
  `Ends on:` slate (scaled 2025 benchmarking) departs further.
- **Estimand:** the cycle rules: the covered buildings in Community District 4, ranked by the penalty each would owe
  under Local Law 18 for a calendar year of the 1991 to 2020 normal weather at Lindqvist Field as the building runs now,
  the twelve largest taking the places (filed in the cycle rules; the law's schedule converts and prices).
- **No decoy:** no document gives a normal-year figure, a penalty estimate or a ranking; the benchmarking submissions
  are the owners' filings under the law, correct for 2025 as reported, and its greenhouse gas column is Portfolio-style
  reporting at federal factors, labelled as such; no document records a building's retrofit, conversion or tenant
  change, describes or endorses any normalization, or argues for a slate.
- **No certified replay:** no published or certified figure is reproduced by the golden method and missed by another;
  the 2025 benchmarked year is a filing, not a control the method must replay.
- **Lesson:** a building's expected compliance exposure is a weather-normalized year on the regime it runs in now:
  scaling a reported year by degree days inflates fixed loads, and a model fitted across a retrofit describes neither
  building. No build on file normalizes an output to a standard year of its driver or locates each unit's own regime.

## Tried and rejected

- Weather normalization alone, with oil fills and estimated reads as the interval structure: in a prototype of 150
  buildings, a degree-day regression on calendar-month bills with oil deliveries summed by month landed within 2 per
  cent of the fill-to-fill fit for most oil buildings (6 at most) and on the golden's slate, so a strong analyst's
  regression lands the call; the estimated reads and fills are Layer 1 (cleaning them makes the call easy) and stay
  there. The decisive structure is each building's change in how it runs.
- A first keying of the card on the time gap with pattern A and Gate G forecasting: the signature is spent in seven
  older builds; keyed on the population gap with G4 first, which also reads truer (the bills before a change are not
  the decided building).
