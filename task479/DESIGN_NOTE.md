# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 2, drawn 2026-10-21 after architecture 1
(NFIP claims replayed on elevated buildings) was spent at stage 4; nothing of architecture 1's world or step is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v2, lineage v1 spent), registered 2026-10-21
  after a pull. Guard WARN only, answered here: `overuse.objective` (ETL in 9 of the last 12): the lane is ETL by
  assignment. `test.same_driver_older` (time, G9, forecasting) against task133 is answered by the card's
  differentiation line. Redrawn at the draw: shape 01 (task484's) to 05 and then 10 (an allocation grades a share per bucket, which no threshold
  protects, stumping 1.6a), forcing event budget_or_appropriation
  (task480's) to season_or_peak, decisive generator G13 and then G16 (spent signatures) to G9, the panel's survival
  against the whole's acquisition of new members. Re-registered at stage 2 with shape 10 and decision
  `designation_set`: WARN `repeat.decision` against task484 and `repeat.question_form` against task271, answered by the
  decision itself (a set of counties clearing a floor is a designation, and a designation asks which); `test.same_puzzle_older`
  against task100 v2 is differentiated on the card. People: Samantha Walter and Debbie Brady, from `guard.py names --geo
  us --seed 479`.
- **Pairing:** Survey Research & Official Statistics, task type `seasonal-adjustment-official-time-series-production`,
  which serves ETL: a monthly member panel benchmarked to the Department of Revenue's annual county receipts and
  restated onto that basis for the year the Department has not yet published. Objective: Data Extraction &
  Conformation.
- **The decision and the quantity:** a state lodging association matches its member counties' 2027 summer co-op
  marketing from a fixed Rising Destinations fund, split across the counties whose taxable lodging receipts grew at
  least five per cent from 2024 to 2025, in proportion to their 2025 receipts. The Department publishes 2025 in
  early 2027, after the season's co-op budgets close, so 2025 is restated from the association's monthly Lodging
  Monitor panel onto the Department's basis. The call is retrospective on its window (calendar 2025, closed) and forward
  on its release: the figure is the one the Department will publish, a year before it does.
- **Data-native sentence:** the Monitor panel was drawn in January 2018 from the members then reporting and takes no
  property opened since, so in the counties where hotels keep opening the Department's receipts have outgrown the
  panel's by a steady few points in every year both are known, while in a county that has been losing its non-member
  properties the panel has outgrown the Department; the 2024 ratio of the Department to the panel is a year behind 2025.
- **Shape:** `10`, a scorecard of metric-threshold checks in one file: each of the sixteen counties' growth against
  the 6 per cent floor (16), the qualifying set and the equal match, a bar chart with the floor, and two asks of sixteen
  counties times two figures each (64); the criteria come from the structure.
- **Strategy:** `forecast_method_backtest` (no back-test is filed: the pack lets an analyst ask how carrying the last
  benchmark by the panel's movement would have done in each earlier year). Gate G `forecasting`; gap `time`; generators
  G9, G13, G16. Layer 2 family `forecast_uncertainty`, pattern `own:benchmark-to-indicator ratio extrapolated on its own
  path past the last benchmark`.

- **Sources, one line each:** seed ET36 (nothing kept but the lane and number); the IMF Quarterly National Accounts
  Manual's benchmarking chapter (the benchmark-to-indicator ratio and why extrapolation runs on its path, not on the
  last annual ratio), stated in no shipped document; the client's official-statistics rigor patterns (vintages and
  revisions, point-in-time panels), used as Layer 1 and the asks' devices only.
- **Same-puzzle test:** gap time, decisive generator G9, decision designation_set against the last twelve builds,
  lineage included: no match. Same-driver test (time, G9, forecasting): task133 older, differentiated on the card.
- **Abstraction test:** task150 (a unit's next count from its own members carried on at a rate plus arrivals) carries
  arrivals as a component to forecast; here no arrival is observed or forecast, only the lagged complete count's ratio
  to a fixed sample. task268 v2 (a stock seen through collection records or a register) has two views of one stock at
  one time; here the complete view lags a year and the step is how its ratio to the sample moves. task474 (short
  counts carried to a year by reference sites) carries a calendar pattern; here the pattern is the year-over-year drift
  of a coverage ratio. None maps onto this driver.
- **WHAT screen:** the program terms file the population (the sixteen counties), the outcome (taxable lodging receipts
  as the Department first publishes them for tax year 2025), the window (calendar 2025, against tax year 2024 as
  published in the TY2024 report), the unit (dollars, growth per cent) and the comparison (6 per cent or more). The
  decisive step settles none of them: it estimates a quantity not yet observed (the Department's 2025 print), and the
  candidate estimators of that one quantity disagree only on how the benchmark-to-indicator ratio is carried a year.

## Default path

A strong analyst with every field read correctly:

1. Reads the program terms: a county qualifies when its tax year 2025 receipts, as the Department first publishes them,
   are at least 6 per cent above its tax year 2024 receipts in the TY2024 report; the fund is split equally.
2. Extracts the TY2024 report's county receipts (dollars) and conforms the Monitor: the legacy and InnSight exports,
   the later submission of each resubmitted month, InnSight cents in dollars, the legacy county names in one case.
3. Carries each county's 2024 receipts forward by its Monitor room revenue's growth from 2024 to 2025 (the same as
   scaling 2025's Monitor revenue by the 2024 ratio of the Department to the Monitor), the standard way to move a
   benchmark with its indicator.
4. Applies the floor and splits the fund.

**Ends on:** Arvenne, Brisholt, Corrigan Bay and Delvane qualify, $450,000 each

Growth on that path is 8.5, 7.2, 6.8 and 6.2 per cent for the four, and Elsmoor 3.4, Fallowmere 2.6, Grindell 4.2.

**Golden:** Arvenne, Brisholt, Elsmoor, Fallowmere and Grindell qualify, $360,000 each (9, 8, 10, 11 and 9 per cent);
Corrigan Bay and Delvane fall to 4 and 4.

## Stump sentence

The default path moves 2024's receipts by the Monitor's 2025 growth and files Arvenne, Brisholt, Corrigan Bay and
Delvane qualify, $450,000 each, because it never asks how the panel's growth has tracked the Department's in the years both are known: in
every year since 2019 the Department's receipts outgrew the panel by a steady margin in Elsmoor, Fallowmere and
Grindell and trailed it in Corrigan Bay and Delvane, and 2025 carries one more year of that drift.

## Three rules

Task type: seasonal-adjustment-official-time-series-production (Survey Research & Official Statistics): a monthly panel indicator benchmarked to the Department of Revenue's annual county receipts and restated onto that basis for the year the Department has not yet published, a conformation of the Monitor's records onto the official series, serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each county's tax year 2025 taxable lodging receipts on the Department's basis, worked the way official time-series production extrapolates a sub-annual indicator past its latest annual benchmark: on the path of the benchmark-to-indicator ratio, which a fixed panel's coverage of a changing whole moves at a steady pace, not at its last annual value.

Swap: "which school districts' 2025 enrolment grew 6 per cent, from a fixed sample of schools benchmarked to the state census" keeps the shape and is still official statistics; put a hospital's own bed-days for the panel and its own audited annual total for the benchmark and the sample covers the whole, the ratio never drifts and the step does not exist, because the drift lives in a fixed panel of one organisation's members against an official count of every establishment.

Layer 1: the Department's reports as seven PDFs in two layouts (thousands of dollars to 2020, dollars with county codes after), each report's prior-year column revised for amended returns, the Monitor in two exports across the 2022 system change (local received stamps against UTC submission stamps, dollars against cents, legacy property ids against InnSight ids with the vendor's crosswalk), resubmitted months beside the first submission, three legacy county names in capitals, properties that closed leaving the panel, September 2026 still coming in; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts each one mishandled keeps the call (SF1, SF3, SF9).

Layer 2: forecast_uncertainty, a quantity forecast one period past the last benchmark: the choice that flips the call is carrying the benchmark-to-indicator ratio on its own path (each county's line through 2018 to 2024) instead of at its 2024 value, its 2018 to 2024 mean or a statewide drift.

Decisive step: for each county, the first-print ratio of the Department's receipts to the Monitor's room revenue for 2018 to 2024, a straight line fitted to it and read at 2025, times the county's 2025 Monitor revenue, which moves Elsmoor, Fallowmere and Grindell above the floor (10, 11 and 9 per cent) and Corrigan Bay and Delvane below it (4 and 4).

Not semantics: every field, unit and definition read correctly (receipts in thousands then dollars, revenue in cents, the later submission, the first print against the revised year, the counties' names and codes) still leaves the easy route moving 2024 by the panel's growth, because no field says the panel's coverage of the Department's base changes, and nothing in any file compares the two series across years; the drift is found only by setting seven reports against eight years of panel revenue.

Not rule application: the program terms fix the population, the outcome (the Department's first print for tax year 2025), the comparison year (tax year 2024 as published) and the floor, and no rule or procedure says how a year the Department has not published is estimated; executing every filed rule with 2024's receipts moved by the panel files Arvenne, Brisholt, Corrigan Bay and Delvane.

Analyst test: a strong analyst who conforms every file and reads every rule, moving each county's 2024 receipts by its Monitor growth, files Arvenne, Brisholt, Corrigan Bay and Delvane qualify, $450,000 each (the default path's Ends on, Corrigan Bay at 6.8 and Delvane at 6.2 per cent); one who scales by the mean ratio files Arvenne, Corrigan Bay, Delvane and Nethervane; only the ratio carried on its own line files the golden five; checks.py runs the easy route and the decisive step on the clean truth (R3a, R3b).

Estimand: the program terms (tla_rising_destinations_2027_program.docx, section 2): the population (the state's sixteen counties), the outcome (taxable lodging receipts for tax year 2025 as the Department first publishes them in its Tax Year 2025 report), the window (calendar 2025, against tax year 2024 as published in the Tax Year 2024 report), the unit (growth per cent) and the comparison (at least 6 per cent), with the equal split in section 4.

No decoy: nothing is planted: the reports, the exports, the register and the crosswalk are the systems' own records, the program terms state the basis without a method, and no memo, earlier estimate, staff draft or published Monitor figure ranks the counties on 2025 or treats the panel one way; the reports' own change column covers published years only.

No certified replay: no certified, published or earlier 2025 figure ships, so nothing is recovered by reproducing a number; the line is fitted to the seven published first prints and read one year further.

Lesson: a fixed sample carried past the last complete count keeps losing or gaining share of the whole at the pace it has in every year both are known, so the last year's ratio is a year out of date; the analyst checks how the indicator has tracked the benchmark before trusting its movement. No build on file extrapolates a benchmark-to-indicator ratio.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 the Monitor's 2025 total as the county's receipts | the program terms read without "on the Department's basis" | readable |
| Layer 1: two report layouts, revisions, two exports, cents, resubmissions, county names | the reports' own headers, the dictionary and the methods note | readable |
| R1 (default path) 2024's receipts moved by the Monitor's 2025 growth | the program terms' 2024 base and the Monitor's monthly totals | readable |
| R2 the mean ratio 2018 to 2024, or one statewide drift on the 2024 ratio | the seven reports read for a stable ratio, or the drift pooled | readable |
| R3 the Department's own 2024 growth carried to 2025 | the TY2024 report's change column | readable |
| R4 (decisive) each county's ratio carried on its own line to 2025 | nothing: no sentence says the panel's coverage moves, the methods note describes a panel and its closures, no file sets the panel beside the Department across years, and the reports print only receipts | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the ratio history's receipts | each year's first print | the next report's revised figure for 2018 to 2023 | same call, same growth (asserted) | program terms section 2: the first print is the basis |
| SF2 | tax year 2024 receipts | the TY2024 report's figure | a revised 2024 | same call (no revised 2024 ships, asserted) | program terms section 2 |
| SF3 | a resubmitted month | the later submission | the first | same call (asserted) | methods note section 3 |
| SF4 | tax year | the calendar year | a fiscal year | same call | the reports: tax periods in calendar year y |
| SF5 | a report's county through 2025 | the county on the report | the register's county | same call (identical through 2025, asserted) | the dictionary; checks.py SF5 |
| SF6 | the floor | 6.0 per cent on the unrounded growth | on the whole-per-cent figure | same call (no county within 0.45 points under any family member, asserted) | program terms section 2; the prompt's rounding is for the report |
| SF7 | the match | the fund divided equally | in proportion to receipts | same call on the set; figures by section 4 | program terms section 4 |
| SF8 | the Monitor's 2025 | every month of 2025 for every reporting property | partial months | same call (twelve months each, asserted) | the export |
| SF9 | legacy county names | folded to one case | as written | same call (asserted) | the sixteen counties of the reports |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L5, C1, C2), growth of tax year 2025 on 2024 in per cent.

| Rung | Route | Qualifying | Corrigan Bay, Delvane | Elsmoor, Fallowmere, Grindell |
|---|---|---|---|---|
| R1 (default path) | 2024 moved by the Monitor's growth | Arvenne, Brisholt, Corrigan Bay, Delvane | 6.8, 6.2 | 3.4, 2.6, 4.2 |
| R2a | the mean ratio of 2018 to 2024 | Arvenne, Corrigan Bay, Delvane, Nethervane | 14.8, 12.5 | -16.8, -22.0, -9.6 |
| R2b | one statewide drift on the 2024 ratio | Arvenne, Brisholt, Corrigan Bay, Delvane, Hollin Ridge, Nethervane, Pellow Sound | 8.5, 7.9 | 5.0, 4.2, 5.8 |
| R3 | the Department's 2024 growth carried | Arvenne, Corrigan Bay, Fallowmere, Grindell, Orrin Falls | 6.6, 5.0 | 4.7, 9.8, 6.4 |
| Golden | each county's ratio on its own line | Arvenne, Brisholt, Elsmoor, Fallowmere, Grindell | 4.1, 4.0 | 10.1, 10.9, 8.8 |

- The estimator family (least squares on 2018 to 2024, on revised prior years, on 2021 to 2024, the mean yearly change,
  the last change) files the golden five and every county's growth at the same whole per cent (C1), each at least 0.45
  points off the floor (C2). The half step (the ratio at the end of 2024) and the log-linear line also file the five;
  the log-linear line misfits the drift counties' ratios by 0.70 to 3.14 per cent against the straight line's 0.04 to
  0.11 (S1), so the data refutes it.
- Dominance: the golden and R1 differ by Elsmoor, Fallowmere and Grindell against Corrigan Bay and Delvane; every rung
  files a wrong set (L2). Carrying the last benchmark by the panel missed every year 2019 to 2024 the same way in all
  five moving counties (S2): Fallowmere by 8.6 to 15.4 per cent, Corrigan Bay by -2.1 to -2.4.
- Position: on R1 Elsmoor, Fallowmere and Grindell sit 2.6, 3.4 and 1.8 points under the floor; on the golden Corrigan
  Bay and Delvane sit 1.9 and 2.0 under it.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the sixteen counties | filed (program terms 2) |
| 2 | Unit of account | taxable lodging receipts in dollars; growth per cent | filed (2) |
| 3 | Attribution window | tax year 2025 against tax year 2024 | filed (2) |
| 4 | As-of dating | the Department's first print; the Monitor extract of 2 October 2026 | filed (2); manifest |
| 5 | Version basis | first prints; the later submission of a month | filed (2); methods 3 (SF1, SF3) |
| 6 | Denominator | the TY2024 first print | filed (2; SF2) |
| 7 | Weighting | none: county totals | methods 4 |
| 8 | Window length | one calendar year | filed |
| 9 | Boundary inclusivity | at least 6 per cent | filed (2; SF6) |
| 10 | Rounding path | growth unrounded against the floor, printed to the whole per cent | prompt; SF6 |
| 11 | Tie-break | none arises (no county within 0.45 points) | C1 |
| 12 | Maturity and censoring | 2025 complete in the Monitor; September 2026 partial and outside every ask | SF8; prompt's months |
| 13 | Order of operations | conform, total, ratio, line, estimate, compare | commutes |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the later submission | methods 3 |
| 16 | Identity normalisation | county names folded; legacy ids linked for ask B | SF9; the asks |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | thousands then dollars; cents | the reports' headers; the dictionary |
| 19 | Code and status semantics | county codes in the reports; panel status in the register | dictionary; never the stump |
| 20 | Integerisation | the match in whole dollars | SF7 |
| 21 | Clause scope | the floor applies to every county | filed (2) |
| 22 | Forward window contents | the Department's TY2025 print, due December 2026 | filed (3) |

## Literal reader

The program terms executed word for word fix the population, the outcome, the comparison and the floor, and they ask
for the Department's 2025 first print a year before it exists: the literal question is an estimate of an unobserved
figure, and the records answer it, since seven first prints set against the Monitor show each county's ratio moving
along a straight line within 0.21 per cent in every year. A literal reader who moves 2024 by the panel's growth has
assumed the ratio stopped in 2024, which the seven reports contradict; every other reading converges or violates a
quoted sentence (fork table). Re-run on the finished pack at stage 3.

## Oracles

- The reports' change column (each tax year against the revised year before) ties under every handling and ranks no
  county on 2025 (O1).
- The visitor spending estimates end in 2024 and measure all visitor spending (O2, a distractor); they carry no 2025.
- No control ties only under the golden on the asks: the register's rooms are today's and tie to nothing in 2018.

## Ask sheet

- **Ask A, each county's Lodging Monitor occupancy and average daily rate for January to August 2026 (sixteen counties,
  two figures each, one decimal and the cent).** H18 home: a second measure every county carries, which the program
  terms (section 5) put beside the designation. Path: the InnSight export (prop_id, period, county_code, room-nights,
  revenue in cents, submission stamps), the property register (county), the methods note (definitions), the
  dictionary. Primary device: D7, records filed under another holder after a transfer: from April 2026 the 36
  properties Harbor & Pine Hospitality took over in twelve counties file through its portal account, which carries
  its office county's code (Arvenne's), while the register keeps each in its own county; only a property whose county
  code changes in April against its unchanged register county shows it. Hazards: resubmitted months (the later
  replaces), cents, September 2026 partial.
- **Ask B, for the panel properties reporting in January 2018 that still report in August 2026, each county's share of
  January 2018's panel rooms they hold and the change in their rooms since (sixteen counties, two figures each, one
  decimal).** H18 home: the audit trail of the call's input, the panel's standing against its draw (program terms
  section 5). Path: the legacy export (January 2018 and March 2022 rooms), the InnSight export (April 2022 and
  August 2026), the crosswalk, the register. Primary device: D7, the true key elsewhere: the vendor's crosswalk misses
  thirteen properties, one in each of thirteen counties, each rebranded at the system change and renovated since, so
  neither the crosswalk nor the name links them; only the one unmapped InnSight property in the county whose April
  2022 rooms equal the lost property's March 2022 rooms does. Hazards: rooms as room-nights over the month's days, the
  register's rooms being today's.
- **The construction layer:** the call, the sixteen growth figures and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no 2026 row, the register or the crosswalk; every device
  row is a 2026 row or a crosswalk gap, and the call is unchanged under either handling (X1, X2).
- **Hazard table (asserted):** A3 (resubmissions move 8 or more counties' rate), B2, B3 in checks.py; none moves the
  call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, occupancy and average daily rate, January to August 2026 | the battery's path: the later submission kept, cents in dollars, each report's county from its county code as the dictionary describes it; keeps 6 of 32 | miss |
| B, rooms share and rooms change of the January 2018 properties still reporting | the crosswalk, and the name for the legacy properties it misses; keeps 6 of 32 | miss |

- Mirror leakage: 18.8 per cent of ask weight on the cut pack (12 of 64 figures, the counties no device touches).
- Pair ceiling: 38.9 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call, instructions and 12 of 64 ask
  figures, 55.3; the mirror at the default path misses the set, keeps 3 of 16 growth figures and the same 12, 22.6).
  Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): earning premium by term rather
  than by policy effective year is a stated accounting rule (rule application), and a condominium master policy's unit
  count read as units is a field reading (data semantics); both stay in the pack as Layer 1 under filed sentences.
- A catastrophe-adjusted expected loss ratio by county (2026-10-20, screened): the estimator family for an expected
  catastrophe loss from a short record is open (window mean, frequency from a long declarations record times the
  window's severity, a fitted severity tail), so the graded figure forks, and filing the method makes it rule
  application.
- Event-clustered confidence bounds on each county's loss ratio (2026-10-20, screened): a variance-only correction that
  widens every interval, so the conservative reflex lands the hold; and the annual series shows the spread directly.
- The Risk Rating 2.0 glide path's full-risk premium for policies still capped (2026-10-20, screened): every policy
  transitioned within one year, so the full-risk premium is censored at the same multiple for all of them and the
  distribution beyond it is not identified; the cap itself is a statutory rule.
- The latest event's claims completed by days since landfall, and open claims from their adjusters' damage estimates
  (2026-10-20, screened): the first is task181's route-specific delay and task451's arrival history, the second is a
  policy-terms computation (rule application).
- Claims linked to policies by quasi-identifiers to rate premium bands (2026-10-20, screened): linkage error correction
  is spent (task449, task468) and a fusion through shared attributes is task465's.
- Policy tenure from originalNBDate with left truncation (2026-10-20, screened): task133's delayed entry.
- Rating each insured building at the claim rate of buildings in its present condition (2026-10-20, screened): the
  policy terms carry an elevated-building indicator for every term, so the rate by present state is one group-by on a
  visible column, the opponent's stratification reflex; kept as a wrong rung (it gives a raised building the later rate
  of elevated buildings in general, which on the river is the low rate of buildings never in a 2016-sized flood).
- Bridge deck deterioration from inspection pairs of different lengths (2026-10-20, screened in another world): per-year
  normalisation, the obvious correction, lands within rounding of the interval-aware estimate on fair decks, so the
  lever is too small.
- Every insured building as the population (2026-10-20, stage 2): the buildings below the base flood level carry the
  counties' whole flood history, so the lowest rates fell to the upland counties with or without the replay, and the
  replay moved no county across the fifth place; the population narrowed to the elevated insured buildings the pilot's
  insurers will quote, where the raised buildings are a third of some counties' book.
- The re-entered transfer claims carrying only NFIP Direct's own payments (2026-10-20, stage 2): summing every
  record's payment then lands each county's payments, so the payment half of ask A carried no device; the re-entry
  carries the claim's payments to date, as NFIP Direct's record of a transferred claim does.
- The Saltreach surge of 2005 a foot under the base flood level and Kettlemoor's 2016 middle reach 0.6 feet under it
  (2026-10-20, stage 2): the protection-to-the-base-flood-level rung (R3) and the class-rate rung (R2b) each filed the
  golden five; with the 2005 surge 0.6 feet under the level in Saltreach (still two feet and more under the raised
  floors) and Kettlemoor's middle reach a foot under it, both rungs file a wrong five.
- A persona pair whose first name the names script does not return (2026-10-20, stage 2): replaced with Samantha
  Walter from `guard.py names --geo us --seed 479`.
- Contents-only and unit owners' records joined to the building rate (2026-10-20, stage 2): neither moves the call,
  so they stay Layer 1 under 2.1 and 2.3 rather than a device.
- Architecture 1, NFIP claims replayed on the elevated buildings as they stand (2026-10-21, spent at stage 4): reader 1
  quoted guidelines 3.1 ("would bring ... as they stand") as the decisive text, replayed each claim's water on the
  present floor and landed the call, every rate and 30 of 72 figures; reader 2 missed on the claims since elevation
  but took ask B's counts from the final inspections; the judge NOT_DETERMINISTIC FIX_NOW on ask B's share, completion
  and county keys and called the estimand's wording an announcement. The estimand that files a counterfactual names
  it; re-rooted to architecture 2 in a fresh world.
