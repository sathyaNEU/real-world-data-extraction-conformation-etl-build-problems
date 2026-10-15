# task461 design note

Architecture 1, drawn 2026-10-15 from seed ET18 (the world, the decision and the quantity; the pitfall re-found from
the data).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task461.json`, registered 2026-10-15. Guard PASS; the older same-driver
  signature (gap time, G13, method_or_model_selection) against task229 v2 and task501 v4 is differentiated on the card.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL, own pattern
  short-record-extension-through-overlap. Energy Systems & Utilities has no task type serving ETL, and emissions
  accounting (the ETL home of the last build) is barred back to back; data integration is the ETL task type whose own
  statistical object decides this call: combining a short direct record of the target with a long record of a
  correlated source through their overlap. The setting is the power market's, as General Statistics requires, and the
  swap is of the method.
- **Why this task type:** task449 (false links to the first plausible target), task454 (cost filled where a survey
  covers one presentation) and task456 (prevalence read through three erring feeds) spent linkage, coverage and
  multi-source misclassification; none carried a short record over a long one through their overlap.
- **Shape:** 04, one dial set from an allowed menu. Arithmetic: the setting, the next lower setting and its expected
  days (3); the expected 2027 cycling days at each of the eight settings (8); the warranty's full cycles in each month
  of 2026 through October and their total (11); the day-ahead net after fees in each of those months and its total (11);
  the net per cycle (1); the chart's named parts (4); the conformed daily-spread file (2): 40.
- **Strategy:** population_selection (the days the spread distribution is taken over: the node's one observed year
  against the full weather record carried to the node) on the time gap (the evidence at the node covers one windy year;
  the decision bets on an ordinary 2027), the population gap behind it (the hub's days are not the node's). Generators
  G13 (horizon) decisive, G14 (conditioned yield) and G16 (the overlap's functional form) behind.
- **World:** Tallgrove Storage Partners, an independent storage owner (invented), runs Redrock Draw Energy Storage, a
  100 MW / 400 MWh battery in commercial operation since 29 December 2025 at its own resource node in the Midplains
  Power Market (invented). MPI first priced the node on 2 December 2025 (at the North Hub's prices until the network
  model carried the resource on 15 December) and renamed it in March 2026; the North Hub's day-ahead prices go back to
  2019. The battery cycles once on each operating day whose day-ahead spread at its node reaches a threshold the owner
  sets each year from a menu of eight settings; the supply warranty allows 300 full cycles a contract year. The 2026
  threshold, the battery's first, is $35.
- **Forcing fact:** the trading services agreement requires the 2027 operating parameters by 1 December 2026, for the
  contract year starting 1 January 2027. The call faces forward (2027's cycling).
- **Forum and forcing event:** executive_team (the owner's management team approves the 2027 operating plan),
  purchase_order_or_contract (the trading services agreement's parameter deadline). Organisation
  utility_or_infrastructure; role portfolio_manager (the asset manager for storage). Personas from `guard.py names
  --geo "United States" --seed 461`: Stacey Garrett (asset manager for storage), Hailey Cooper (market analyst).
- **Data-native sentence:** a node created with its battery has a direct price record only as long as the battery has
  run, and that stretch is one draw of the weather; the hub's record spans the weather the market has seen, and the
  node's spreads move with the hub's in proportion (the congestion that widens them scales with the swing), so only the
  hub's years carried through that proportion show what an ordinary year looks like at the node. Here the node's year
  is a windy one: its average spread is ordinary, but a third of its days are flat (twice an ordinary year's share), as
  in 2020, after which the hub's flat days fell back.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data integration: propagate the integration's error to the
    estimate; here the integration is a record extension and its error is the record it rests on and the form of the
    relationship.
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data: the relationship the overlap
    shows (proportional, through the origin), not the market's additive basis convention.
  - `dataset-generation/references/layer1-messiness.md`: hour ending 24 on prevailing time, 23- and 25-hour days, a
    yearly archive whose formats changed, a renamed settlement point, prices set at the hub before the network model
    carried the node; none on the decisive step.
- **Same-puzzle and abstraction:** gap time, G13, Gate G method_or_model_selection, decision dial_setting. Nearest
  drivers on file 0.04 to 0.05 (task255, task457 lineage, task256, task135); none extends a short record through a
  long one.

## Default path

1. Read the node's day-ahead prices (`mpi_dam_settlement_point_prices_redrock_2025_2026.csv`), its two names joined
   through `mpi_settlement_point_list_2026.csv`.
2. Compute each operating day's spread as the policy defines it (the average of the four highest hourly prices less
   the average of the four lowest), on the operating day as the archive names it.
3. For each setting on the menu, take the share of the node's days since MPI first priced it (2 December 2025 to 2
   November 2026, 336 days) whose spread reaches the setting, times 365: the expected 2027 cycling days.
4. Pick the lowest setting whose expected days do not exceed the warranty's 300 (policy 4.2).

- **Ends on:** $15 per MWh (266 expected cycling days; $10 would give 334).
- **Golden:** $20 per MWh (275 expected cycling days; $15 gives 323, over the limit).

## Stump sentence

The default path counts the node's own days since MPI first priced it and sets the 2027 threshold at $15 per MWh; those
eleven months were a windy stretch whose average spread looks ordinary but a third of whose days were flat, twice an
ordinary year's share, so the node's own record shows too many quiet days for an ordinary 2027, and only the hub's eight
weather years, carried to the node through the proportional relationship their overlap shows, set $20.

## Three rules

- **Task type:** data integration (data-integration-record-linkage-entity-resolution): combining the node's short
  direct price record with the North Hub's long record through their overlap into one daily spread series for the node,
  after conforming MPI's two archive formats, the operating day's clock and the node's two names; the ETL objective's
  conformed daily spreads are the dataset the call is read from.
- **Domain test:** the deciding quantity is the node's daily day-ahead spread distribution over the weather a contract
  year can bring, whose low tail sets the expected cycling days at each setting; the field's data-integration estimator
  for it carries the long record of a correlated source to the target through the relationship their overlap shows (a
  ratio through the origin here), the way a short site record is corrected to the long term.
- **Swap:** General Statistics, so the swap is of the method: replace the extended distribution with a generic summary
  of either source alone and the call moves (the node's own record $15, the hub's record as it stands $10), and an
  additive basis instead of the proportional relationship moves it to $30; a noun swap ("a ward's 2027 overflow trigger
  from its first year of bed census") keeps the sentence and loses the task, with no long correlated reference record
  and no overlap whose form decides how it carries.
- **Layer 1:** MPI's yearly archive changed its date, hour and repeated-hour formats in 2022 and the appended hub file
  carries both (the operator's archive); hour ending 24 and the 23- and 25-hour days on prevailing time (the market's
  calendar); the node renamed on 18 March 2026 (a network model update) and priced at the hub for its first 13
  operating days (the network model had not yet carried the resource); the BMS export in UTC hour beginning, the site
  gateway's dropped hours filled by the portal with zero energy and the last state it saw, the BMS's mode codes changed
  by a June firmware update; the revenue meter in UTC interval ending; settlement statements issued initial and final,
  the administrative fee carried on every hour line of the day, the node's name on the statements as issued. Each is
  what the system that writes the file produces; none carries the call (R2: each main-call item mishandled leaves the
  call and the expected days at $15 and $20 on the same side of 300).
- **Layer 2:** data integration and estimation fit to the data: the node's spread distribution for an ordinary
  contract year built from its short record and the hub's long one through their overlap; the node's own eleven months
  are one windy draw, the hub's record alone is the wrong place, and an additive basis is the wrong form.
- **Decisive step:** extend the node's short record over the hub's eight weather years through the proportional
  relationship the overlap shows (the node's spread 2.21 times the hub's, through the origin) and read the expected
  cycling days at each setting from the extended record.
- **Not semantics:** every field, code, clock and name read correctly (the two archive formats, hour ending 24, the
  23- and 25-hour days, the rename, the hub-priced first days) still leaves the node's own record as the easy route
  ($15); what moves the call is the analysis that the record is one windy year in a market whose windy years revert and
  that the hub's years reach the node in proportion. No mishandled Layer 1 item moves it (R2).
- **Not rule application:** the policy files the estimand (the expected number of cycling days in the contract year at
  each setting, the lowest setting within the warranty's 300) and the spread's definition; no file says which days that
  expectation runs over or how a record shorter than a year should be extended, so executing every filed rule on the
  node's own record files $15 (R3a), and only the extension through the overlap files $20 (R3b).
- **Analyst test:** a strong analyst who reads every file correctly and applies every filed rule counts the node's own
  days since December 2025 and sets $15 (266 expected cycling days); one who wants more weather takes the hub's record
  for the node's and sets $10, or adds the node's average spread premium to it and sets $30, or scales the node's year to
  the hub's long-run average spread and sets $15 again; none sets $20.
- **Estimand:** policy 4.2: the expected number of cycling days in contract year 2027 (operating days whose spread at
  the Battery's settlement point is at or above the setting) at each setting on the menu, $5 to $40 in steps of $5,
  against the warranty's Annual Cycle Limit of 300; the threshold is the lowest setting within it
  (`tallgrove_storage_dispatch_policy_2026.pdf`).
- **No decoy:** nothing is planted: the price archive is the market's record and no block of it is copied or flat
  (R3c); the 2026 threshold ($35) is the first year's parameter and no rung lands on it; no memo, draft, email or
  stakeholder figure ships, and no document argues for the node's year, the hub's record or any setting for 2027.
- **No certified replay:** no certified or published figure carries an expected cycling count or a setting, so nothing
  is recovered by matching one; the method is the analyst's.
- **Lesson:** a quantile of a distribution seen directly over one short stretch is set by that stretch's weather, and a
  stretch whose average looks ordinary can still carry an extreme tail; the long record of a correlated source, carried
  through the relationship the overlap shows (here proportional), gives the distribution an ordinary year draws from.
  No build on file teaches it: task229 fitted one source's error rate, task501 weighted a mixture's regimes, task457
  aligned reference periods.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the node's own record ($15) | the policy defines the spread at the Battery's settlement point | the node's own price file | yes: the asset's own prices | no | no | a count | readable |
| R1 the hub's record plus the node's average spread premium ($30) | no | no | yes: the market's basis convention | no | no | one difference added | readable |
| R2 the node's record extended over the hub's through the overlap's proportional relationship (decisive) | no: the policy files the expectation, never the days it runs over or an extension | no column holds a carried spread; the price files share only the day | no: every reflex lands elsewhere (the node's year $15, the hub's record $10, the premium $30, the node's year scaled to the hub's long-run average $15, an hourly price regression $15) | no | no | a fitted relationship, an extension and a count | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | spread | the average of the four highest hourly day-ahead prices less the average of the four lowest, at the node | the largest less the smallest hourly price, or the charge-before-discharge spread | $20 under the policy's reading | policy 2.2 defines it |
| SF2 | operating day | midnight to midnight, Central prevailing time, hours by their ending | UTC days | same call; the price files carry no UTC clock | policy 2.1; the archive's hour ending |
| SF3 | expected number of cycling days in the contract year | 365 times the share of the record's days at or above the setting | the mean of each year's count, the full years 2019 to 2025 only, the median year | same call, the expected days at $15 and $20 on the same sides of 300 | asserted (C1) |
| SF4 | the Battery's settlement point | the node under both its names | the new name only (from 18 March 2026) | same call | `mpi_settlement_point_list_2026.csv` (predecessor); asserted |
| SF5 | the days MPI priced the node at the hub | left out of the overlap | kept | same call | the list's note; asserted |
| SF6 | hour ending 24 | the last hour of its operating day | the first hour of the next | same call | policy 2.1; asserted |
| SF7 | the 23- and 25-hour days | the spread over the hours the day has | the repeated hour dropped, the missing hour filled | same call | asserted |
| SF8 | does not exceed 300 | at or under 300 | under 300 | same call: no setting's expected days sit within a day of 300 | asserted |
| SF9 | a cycling day and a Full Cycle | one each (policy 3.2) | 2026's warranty cycles per cycling day | same call | policy 3.2; 2026's ratio is 1.00 to two decimals, asserted |
| SF10 | the extension's estimator | the overlap's ratio of total node spread to total hub spread, every day of the record, the node's own spread where MPI priced it | regression with an intercept or through the origin, variance ratio, quantile mapping, the overlap from the rename or with the hub-priced days, the full years only, 2023 onward | same call | asserted (C1) |
| SF11 | lowest setting | the smallest menu setting within the limit | none | same call | policy 4.2 |
| SF12 | contract year 2027 | the calendar year 2027 in Central prevailing time, 365 days | none | same call | policy 2.4; warranty 1.11 |

## Ladder

| Rung | Construction | Setting picked | Expected days at it | At the step below |
|---|---|---|---|---|
| R0 | the node's own record, 2 December 2025 to 2 November 2026 (336 days) | $15 | 266 | 334 at $10 |
| R1 | the hub's record plus the node's average spread premium over the overlap ($19.96) | $30 | 252 | 349 at $25 |
| R2 | the node's record extended over the hub's 2,863 days through the overlap's ratio (2.21) (golden) | $20 | 275 | 323 at $15 |

- **Other reflexes, each landing elsewhere:** the hub's record taken for the node's, $10 (254 at $10, 350 at $5); the
  node's year scaled by the hub's long-run over its 2026 average spread, $15 (282 at $15); the hourly basis by hour of day added
  to the hub's hourly prices, $30; the same basis by month and hour, $25; an hourly price regression's slope applied to
  the hub's spreads, $15.
- **Margins:** the golden record's 300-day level sits at $17.5, inside $15 to $20; R0's at $12.6; R1's at $27.9; the
  hub's at $7.9. Every estimator of the extension and every reading of the expectation (SF3, SF10) gives $20, with
  $15's expected days between 320 and 333 and $20's between 270 and 289.
- **Dominance:** the node's year differs from an ordinary one in its tail, not its average: the hub's 2026 average
  spread ($16.90) sits inside the 2019 to 2025 range ($16.17 to $19.14), while its share of days under $8 is 34 per cent
  against 11 to 16 per cent in every year but 2020 (31 per cent); in 2021 the share fell back to 14 per cent.
- **Grid:** two choices (which record: the node's own, the hub's, the node's extended over the hub's; which form: as it
  stands, plus a premium, in proportion) give five live cells, each naming a setting: the node's own $15, the hub as it
  stands $10, the hub plus a premium $30 (by month $25), the node's year rescaled $15, the extension in proportion $20.
  Every partial step lands on a wrong setting; only the proportional extension over the full record reaches $20
  (asserted).
- **Worth:** the per-setting expected days differ on every rung: R0 gives $20 210 days against the golden 275 and $15
  266 against 323; R1 gives $20 365 and $25 349 against 275 and 224; the hub's record gives $15 152 and $20 94.
- **Data-native structure:** the node's spread is 2.21 times the hub's on the overlap's days (correlation 0.99, the
  daily ratio's spread 0.25 around it, no intercept: 0.34 below zero against spreads of 2 to 620); the hub's flat days
  cluster in windy stretches (autumn 2019 to autumn 2020, autumn 2025 onward), and the node exists only inside the
  second.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the operating days of contract year 2027, each one draw of the market's weather | policy 4.2 and 2.4 |
| 2 | Unit of account | the operating day: one cycle on each cycling day | policy 3.1 and 3.2 |
| 3 | Attribution window | contract year 2027, Central prevailing time | policy 2.4; warranty 1.11 |
| 4 | As-of dating | MPI's archive as pulled 2 November 2026 | the manifest; one vintage of each file |
| 5 | Version basis | prices as MPI published them; the node's first 13 days at the hub's price as published | SF5 asserted |
| 6 | Denominator | the 365 days of 2027 | the expected count is 365 times the share of days |
| 7 | Weighting | each operating day of the record equally | SF3 converges with each year weighted equally |
| 8 | Window length | the full record, 1 January 2019 to 2 November 2026 | SF3 and SF10 converge with the full years only or 2023 onward |
| 9 | Boundary inclusivity | a spread at the setting counts | policy 3.1 ("at or above"); no day sits on a setting to the cent where it matters, asserted |
| 10 | Rounding path | expected days from unrounded spreads, shown in whole days; the call read from unrounded counts | the prompt's rounding sentence; SF8 |
| 11 | Tie-break | none needed | no setting's expected days equal 300 (asserted) |
| 12 | Maturity and censoring | the node's record starts at its creation; the record's last year runs to 2 November | the extension (the decisive step); SF3 converges on the partial year |
| 13 | Order of operations | conform the formats, clocks and names; compute each day's spread; fit the overlap; extend; count | C1 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | one row per point, operating day and hour; the repeated hour ending 2 is a real hour | the repeated-hour flag; asserted |
| 16 | Identity normalisation | the node's old and new names are one point | the settlement point list's predecessor (SF4) |
| 17 | Netting against gross | none in the main call | n/a |
| 18 | Dimensional units | dollars per MWh; days | the dictionary |
| 19 | Code and status semantics | the repeated-hour flag's two codings (Y/N to 2021, true/false from 2022) | the dictionary |
| 20 | Integerisation | none: expected days are counts times 365 over the record, shown whole | n/a |
| 21 | Clause scope | policy 4.2 applies to every setting alike | policy 4.2 |
| 22 | Forward window contents | contract year 2027 draws its weather from the market's record, windy years at their frequency | the decisive step; the hub's record from 2019 |

## Literal reader

Executed word for word, policy 4.2 asks, for each setting, how many operating days of 2027 are expected to have a
spread at the Battery's settlement point at or above it, and picks the lowest setting at which that number does not
exceed 300; the literal reader has eleven months of the node's own prices, a windy stretch, and the hub's eight years,
and an expectation over the weather 2027 can bring needs the node's spreads in years before it existed, which only the
hub's record carried through the overlap provides; every estimator of that extension (SF10) gives $20, with $15's
expected days over 300 and $20's under it. No filed sentence names the node's own year as the expectation's basis.

## Oracles

None ties only under the golden. The hub's yearly average spreads are honest and show 2026 as ordinary on every path;
the 2026 operating records (the BMS export, the meter, the statements) answer what the battery did at $35 and confirm no
setting for 2027; the settlement point list's note on the hub-priced days and the rename ties on every path.

## Ask sheet

- **Ask A, the full cycles the warranty counts in each month of 2026 through October, and their total (11 figures, two
  decimals).** H18 home: the audit trail of the call's constraint, the count the 300 is measured in (policy 5.1: the
  Asset Manager tracks the warranty's Full Cycles each contract month against the Annual Cycle Limit). Path: the BMS
  export, the revenue meter, the warranty excerpt, the capacity test reports, the dictionary (five files, nine
  columns). Primary device: D4, absence evidenced in another file: the site gateway's cellular link drops a few times a
  month, and the portal fills each dropped hour with zero energy and the last state of charge and mode it saw; at least
  one drop each month falls in an evening discharge (27 hours of discharge in 11 runs), the meter shows the energy delivered in those
  hours, and warranty 4.3 counts it at the meter's delivered energy over 0.975. Nothing marks a dropped hour: the zeros
  sit among real idle hours, the state of charge resumes at the next reading. Hazards: H1 the BMS in UTC against the
  warranty's contract months in prevailing time (D8); H2 the capacity tests left out (warranty 4.2), the September test
  logged MAINT after the June firmware update while the March one is TEST (D2, a label at the wrong vintage); H3 the
  power conversion system's AC columns beside the DC ones (D3). Stops (built, every figure outside its bin, asserted):
  the BMS's DC discharge as exported, every month low by 0.24 to 1.49 (January 7.21 against 7.95, September 9.52
  against 11.01); the same in UTC months (January 6.47, July 16.80); the TEST code alone left out (September 10.53); no
  test left out (March 5.76, September 10.53); the AC column (every month low by the conversion and the dropped hours);
  the meter's delivered energy over 0.975 everywhere (every month 1.0 to 1.9 per cent low); the golden. Realism: remote battery sites run on
  cellular gateways, and portals fill missed telemetry with zeros and held states.
- **Ask B, what the battery netted in the day-ahead market after MPI's fees in each month of 2026 through October, and
  the total (11 figures, thousands of dollars to one decimal).** H18 home: what a cycle earns, the value side of the
  call's trade-off (the policy sets the lowest setting within the warranty because each cycle earns its spread). Path:
  the statement lines and the dictionary (two files, eight columns). Primary device: D6, an event's quantity on every
  line it covers, grain unstated: the administrative fee is computed once per operating day on the day's day-ahead
  energy and the export carries it, bill determinant and amount, on every hour line of the day; summing the lines
  charges it 23, 24 or 25 times. The tell, a determinant larger than the hour's own awards, sits in the energy lines.
  Hazards: H4 initial and final statements (the final restates the operating day; the repriced 20 and 21 July change
  between them, D2); H5 MPI's sign (positive is owed by the QSE); H6 the statement's issue date against the operating
  day (D8); H7 the node's name on statements issued before the rename (resource constant). Stops (built, asserted):
  every fee line, every month low by $15.9k to $95.4k (January 231.9 against 268.9); no fee, every month high by $0.7k
  to $4.1k; the initial statements, July 677.7 against 671.7; both versions, every month doubled; issue months, every
  month moved; MPI's sign kept, every figure negative; the golden.
- **Ask C, the net per warranty cycle over January to October (1 figure, whole dollars).** Construction: Ask B's total
  over Ask A's; inherits both primaries ($33,905 on the exported discharge, $26,170 on every fee line, against $31,342),
  the same whole dollar whether the totals are taken unrounded or as shown (asserted).
- **The chart:** the cumulative 2026 warranty cycles at each month's end against a line to 300 at the year's end; its
  points carry Ask A's device.
- **The construction layer:** the expected 2027 cycling days at each setting (8) and the conformed daily-spread file
  (one row per settlement point and operating day, the node under one name); the cracker has them.
- **Main population zero-counts (asserted):** the main call reads no BMS, meter or statement row (every rung and the
  call computed with those files deleted are identical); the asks read no price row (Ask A and B computed with the price
  files deleted are identical). No device or hazard row sits in the price files.
- **Hazard table (built):** H1 moves January, February, July, August and October for a response grouping by UTC
  months; H2 moves September (TEST code alone) and March and September (no exclusion); H3 moves every month; H4 moves
  July (initial statements) or every month (both versions); H5 flips every month's sign; H6 moves every month; H7 drops
  January to mid-March for a response filtering on the current name.
- **Rounding edges (asserted):** every monthly cycle count at least 0.001 from its rounding edge, every monthly net at
  least $13 and the net per cycle at least $0.25 on every rounding path.
- **Referee:** the revenue meter arbitrates the dropped hours (warranty 4.3 names it) without handing over a level: it
  ties to the BMS only on hours the export kept, at the meter's side of the conversion.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, warranty cycles by month and total | converts UTC to prevailing time, leaves both capacity tests out from Cordell's reports, sums the BMS's DC discharge; the battery finds unique hours, no nulls and no duplicates, so every month keeps the dropped hours' zeros and runs low | miss |
| B, day-ahead net by month and total | takes the latest statement line per hour and charge type, reverses MPI's sign, sums every line; every month carries the fee 23 to 25 times | miss |
| C, net per cycle | B's total over A's | miss |
| Chart | A's cumulative counts | miss |

- Mirror leakage: about 9 per cent of ask weight (a response on R0 keeps the conformed file and the chart's labelled
  pace line; it misses every expected count but $5's, every cycle count and every net).
- Pair ceiling: 37.4 (planning weights 38 / 7 / 55 with the call, the next lower setting and the eight expected counts
  as the main block and r = 5; the ask weight spread over 29 criteria: A 11, B 11, C 1, the chart 4, the file 2; the
  cracker keeps the file and the chart's pace line and title, 4 of 29 or 0.14, 38 + 7 + 7.6 = 52.6; the mirror keeps
  r, instruction-following, the file and the pace line, 5 + 7 + 55 x 0.10 = 17.5; average 35.1, 37.4 with the eight
  counts weighted as asks), rerun from the generated rubric at build.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| dates MM/DD/YYYY and hours 01:00 to 24:00 to 2021, ISO dates and hours 1 to 24 from 2022, the repeated-hour flag Y/N then true/false | MPI's yearly archive, changed in 2022, appended by Tallgrove's market data team | hub file | one format's parser (loud), the flag read in one coding | none: the record holds 2,863 operating days of 23 to 25 hours under either era's reading (R1) |
| hour ending 24 | the market's calendar | hub and node files | read as the next day's first hour | SF6: the call, $15 over 300 (327) and $20 within (279) |
| the 23- and 25-hour days | daylight saving on prevailing time | hub and node files | the repeated hour dropped, the missing hour filled | SF7: the call and the counts unchanged |
| the node renamed on 18 March 2026 | MPI's network model update | node file, settlement point list, statements | the new name alone | SF4: the call unchanged; the default path still $15 |
| the node priced at the hub's price for its first 13 days | MPI's network model before it carried the resource | node file, the list's note | kept in the overlap or in the node's own record | SF5: the call unchanged; the default path still $15 |
| the BMS in UTC, hour beginning | Cordell's portal | BMS export | contract months taken in UTC | Ask A only (H1) |
| hours the site gateway dropped, filled with zero energy and the last state seen | the cellular gateway and the portal | BMS export | summed as idle hours | Ask A's primary; no main-call row |
| mode codes after the June firmware update (the capacity test MAINT, TEST a weekly self-test) | Cordell's BMS | BMS export | TEST alone taken as the capacity test | Ask A only (H2) |
| the power conversion system's AC energy beside the DC energy | the BMS | BMS export | the AC column counted | Ask A only (H3) |
| the meter's fifteen-minute intervals by their UTC end | MPI's meter data | revenue meter | an interval's end read as its start | Ask A's substitution at the edges of a dropped span only |
| initial and final statements, the fee on every hour line, MPI's sign, the issue date, the node's name as issued | MPI's settlement system and the QSE's portal export | statement lines | see the ask sheet | Ask B only; no main-call row |

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is the node's daily spread
  distribution for an ordinary contract year, built the data-integration way (its short record extended over the
  hub's long one through the relationship their overlap shows); replacing it with either source's own summary or an
  additive basis moves the call ($15, $10, $30). Two layers: the Layer 1 inventory above, each main-call item asserted
  neutral (R2, SF4 to SF7) and each ask item confined to its ask with zero main-call rows (the separation checks);
  Layer 2 the extension. The decisive step is none of the three banned kinds, each executed in `checks.py`: not a
  plant (R3c: no hub day repeats another's prices and none is flat; the only node days equal to the hub's are the 13
  the settlement point list names; no document names a 2027 setting, an expected count, a weather basis or an
  extension); not data semantics (R2 and SF1 to SF12: every field, clock and name mishandled leaves the call where it
  is, and every field read correctly still leaves the node's own record on $15); not rule application (R3a: with every
  filed rule executed on the clean truth the node's own record files $15; R3b: only the extension through the overlap
  files $20, while the hub's record alone files $10 and the hub plus the premium $30).
- **Gates.** 13 files in 3 formats (csv, pdf, xlsx); the hub file at 68,712 rows; two distractors (the hub's
  real-time prices and the ancillary service prices) the solution never reads, each deletion leaving the call and
  every ask unchanged; 89 checks (the net per cycle on one whole dollar by every rounding path among them);
  `verify.py` from the bundle alone; two builds byte-identical; `figures_check.py`,
  `precut.py` and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK); guard heart PASS; surface promoting task460
  (back to back; the shared register column sets were reshaped, what remains is the ETL lane's shared vocabulary) and
  task501 (the same gap, pattern and Gate G, differentiated on the card) for the author's read; the containers carry
  the fiction's people and dates.

## Leak check

- `leak.py`: REVIEW, no LEAK. Its three answer-figure lines are policy 4.2's own selection sentence and the warranty's
  300 Full Cycles, the filed criterion, neither a 2027 setting nor a count; its two vocabulary lines are the policy and
  the warranty in their own words (record, contract, average, prices, archive), neither naming the extension.
- Reader, first pass (2026-10-15): questions 1 to 4 none (no sentence names the step, no file gives a 2027 setting or
  count, no file exists only for the analyst, no figure reads as the answer); question 6 an analytical choice, the easy
  routes the hub's record alone ($10), the node's own year ($15) and the hub scaled ($20, the golden's family). It
  raised the record the expectation rests on as the determinism risk and two tells, both fixed in the generator in one
  pass: the settlement point list's other storage nodes, recent enough to read as a build-out behind a new regime, now
  enter before 2019, with the proxy-price note shortened; the capacity test report's last line (the BMS taking the
  measured energy as its setting) removed.
- Reader, second pass on the repaired pack (2026-10-15): CLEAN; questions 1 to 4 none; question 6 an analytical choice,
  "which price record the expected 2027 cycling days rest on and how it is scaled to the Battery's own node", the easy
  routes $15 and $10, the scaled record $20. The same record question raised, read on the 2026 median against 2024 and
  2025 alone; the pack's answer is its own earlier windy stretch (October 2019 to November 2020, 29 to 52 per cent of
  the hub's days under $8 in ten of its fourteen months, 2020's median 11.01 against 2026's 10.49, back to 14 per cent of days in
  2021), left for the judge to weigh: filing the record would hand over the step. The fee carried on every hour line of
  a day, read as a possible generator artefact, is Ask B's device (the QSE portal's hourly export of a daily charge) and
  stays; the dictionary's "Field definitions visible" was the sheet's title read with its visibility state.

## Determinism judge

- First pass (2026-10-15, `determinism_check_report.md`): DETERMINISTIC, FIX_NOW on the solution text only. Gate G
  forecasting with etl_conformance, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H
  domain pass, layers pass, decisive_step analytical; every figure reproduced. The finding, fixed in one generator pass:
  the net per cycle rounded to $31,339 or $31,338 by the cycles it was divided by; the small noise on each cycle's DC
  energy was redrawn so every path gives $31,342 (unrounded totals $31,341.80), the submission and the workbook saying
  it comes from the unrounded totals, asserted in `checks.py`. Its other two points stay as they are: the record the expectation rests on
  (rated low to moderate, closed by the hub's years) and the warranty's "unavailable" on the export's held zero rows
  (an ask-level reading; the held state and the meter's delivery make the golden the expert reading).
- Re-judge after FIX_NOW (2026-10-15, `determinism_check_report_pass2.md`): DETERMINISTIC, APPROVE. Gate G forecasting,
  analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain pass, layers pass, decisive_step
  analytical; every figure reproduced, the net per cycle $31,342 on every path. Every pooled estimator it tried picks $20
  (the full years alone, an intercept regression, the mean of the daily ratios, the last three and the last five years);
  only the node's own year ($15) and the hub unscaled ($10) move the call; margins 25 days at $20 and 23 at $15 against
  300, about two standard errors of the pooled mean. Its one open point, the optional pin filing the expectation over
  the price years in the extracts, is not taken: with that sentence the node's own year dies to a filed clause and the
  step it decides would be handed over.

## Tried and rejected

- 2026-10-15, draw: the seed's own stump, a replay grouped by UTC dates that moves the charge and discharge hours across
  the operating day. Rejected: catching the clock is reading a field correctly (data semantics), banned as the decisive
  step; the clocks stay as Layer 1 mess and must leave the call where it is.
- 2026-10-15, design: a mild 2026 that lowered every day's swing (the year's average spread 34 per cent under the
  others). Rejected: an average that low after seven flat years reads as a structural break, a defensible reason to
  keep the node's year, and the additive premium landed within a dollar of the golden's level; the windy year that
  widens the tail and keeps the average, with an earlier windy year that reverted, replaced it.
- 2026-10-15, design: the BMS's own cumulative cycle counter in the export. Dropped: it recovered the dropped hours'
  energy at the BMS's usable-energy denominator, a second recovery that disagreed with warranty 4.3 at two decimals.
- 2026-10-15, design: the node's spread exactly 2.2 times the hub's every day (correlation 1.000). Replaced by a daily
  congestion variation (the ratio's spread 0.25), which reads as a market and leaves every rung where it was.
