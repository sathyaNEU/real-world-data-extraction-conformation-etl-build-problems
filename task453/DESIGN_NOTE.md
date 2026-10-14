# task453 design note

Architecture 1, drawn 2026-10-13 (wave 2, oviya1301). The seed (ET10, trial-results reporting compliance) is not kept: its world sits in the biomedical and pharmacology domains, none of whose task types serves ETL, and its rate is a stated deadline count, the backdrop the 10/10 rules ban. The three ETL task types the last three builds hold (payment and claims, emissions inventory, test equating) are banned, so the pairing comes from an ETL task type the client lists and no build has drawn: seasonal adjustment and official time-series production.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task453.json`, architecture v1, registered 2026-10-13 and refined in place at design (the documented change became the move from account-address to workplace placement; `guard.py check` re-run, WARN only). Each WARN is answered here.
  - `repeat.question_form` (which, as task451): the call is a designation set, and a set of regions is asked with which.
  - `test.same_driver` on (population, G16, method_or_model_selection) blocked the first card (task501 v4 and four older builds). The honest Gate G is conformance: the decisive move puts each region's history on one placement before its seasonal pattern is estimated. The card carries etl_conformance, and differentiation against task139 and task30.
  - The nearest driver (task30 round 3, 0.08) segmented a calibration corpus to the cohort after a methodology change. Here the post-change span is 15 months, too short for a seasonal pattern; segmenting to it lands the right regions on wrong figures, and the golden keeps the whole history with the change removed as a level shift.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / Data Extraction & Conformation (ETL). A provincial statistics bureau builds each economic region's monthly payroll jobs from the revenue agency's employer return statistics, seasonally adjusts them, and certifies to the Minister which regions a statutory trigger designates for the Regional Rapid Response Program. Removing a documented break in an administrative source as a level shift before the seasonal filters is official series production's own method (the client's pattern `survey-research-official-statistics/seasonal-adjustment-official-time-series-production/1`).
- **Objective:** ETL. The conformed dataset is each region's monthly payroll jobs from January 2021 to March 2027 on one placement (two layouts of the agency's statistics, a municipal concordance across an amalgamation, revised months replacing preliminary ones), seasonally adjusted, with the trigger read off it and two per-region measures from the workplace returns beside it.
  - Retrospective by design: the trigger reads the quarter just closed (January to March 2027) against the calendar year before, and the regulation certifies a closed quarter.
  - Not retaggable as Forecasting: nothing is predicted; the open part is the seasonal pattern used to adjust a closed quarter.
- **Shape:** 10, a scorecard of every region against one line. Criteria arithmetic: the designated set and five critical components (the Capital, Brennick Valley, Pellmarsh Hills, Kestrow North and Varrenby Shore placed against the line); the certificate's figures for the three designated regions (6); the chart (3); jobs lost at each region's workplaces, two figures each (20); each region's employers (10); the two files. About 45.
- **Strategy:** population_selection. Before January 2026 the agency's regional figures count jobs where employers' account addresses are, from January 2026 where the jobs are; the decisive move is which history the seasonal pattern is estimated from, and on what placement.
- **Mechanism:**
  - Gap: population (decisive: the months before January 2026 place a different population of jobs in each region, so the seasonal-irregular ratios around the change compare two populations), with time supporting (the seasonal pattern is estimated over a span that crosses the change, while the compared periods both lie after it).
  - Generators: G16 decisive (the adjustment the data entitle), G6 (the population a region's series counts shifted under it).
  - Gate G: etl_conformance. Layer 2: field_method, the client's SROS seasonal-adjustment pattern 1 (model level shifts in the regARIMA pre-adjustment before seasonal filtering).
- **World:** an unnamed Canadian province. Its Bureau of Statistics and Economic Analysis builds monthly payroll jobs for ten economic regions from the employer return statistics of the Provincial Revenue Agency.
  - From the January 2026 reference month the monthly return carries a workplace schedule and the agency's statistics place each job at its workplace. Before, every job of an employer sat at the municipality of its account address (the head office, for employers with workplaces in several places), and the earlier months were not revised (the agency's release note of 16 February 2026). The province's total did not move. The Capital lost 16 per cent of its jobs to the regions where employers based in Wickmoor run mines, mills, plants, hospitals and stores (Kestrow North +28 per cent, Varrenby Shore +23); Saltmere Coast lost 6 per cent to Dunfallow Bay and Hethervale Lakes.
  - The Regional Rapid Response Program Regulation designates a region for a quarter when its seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its payroll jobs for the preceding calendar year; the bureau certifies the designated regions to the Minister within 45 days of the quarter's end, on the returns and revisions the agency has supplied by then.
- **As-of:** the first quarter of 2027; the agency's monthly file of 23 April 2027, its revision file and workplace returns of 7 May 2027; the certification of 13 May 2027.
- **Furniture:**
  - Forum minister_or_cabinet (the bureau certifies to the Minister); forcing event period_close (the quarter's returns closed and revised); organisation research_or_statistics_office.
  - Role other (the manager of the bureau's regional labour statistics; the prompt names no one); context artifact register (the agency's return statistics); calibration none.
- **People:** drawn with `guard.py names --geo Canada --seed 453`, on the card: Joel Ferguson (Minister of Labour and Economic Development), Heidi Bond (the bureau's chief statistician, who signs the certificate), Jacqueline Chaney (the agency's statistical liaison, who signs the release note and the transmittal), Ryan Bentley (manager, regional labour statistics).
- **Data-native sentence:** employers with workplaces across the province report from their head offices in Wickmoor and Saltmere, so until January 2026 the agency counted their mines, mills, hospitals and stores in the Capital and Saltmere Coast; the move to workplace placement lifted Kestrow North by 28 per cent and Varrenby Shore by 23 per cent in one month and cut the Capital by 16. A seasonal adjustment run over the whole history cannot let its trend jump, so it reads part of each step as the seasonal pattern of the months around it, and the first quarter's factors carry the step into 2027: the regions that gained are pulled down, the Capital pushed up, although both periods the trigger compares lie after the change. On a series whose placement never changed, the trap would not exist.
- **Sources, one line each:**
  - `layer2-rigor-patterns.md`, SROS seasonal adjustment 1 (model outliers and level shifts in regARIMA before seasonal filtering; the shortcut runs the default adjustment and labels the event afterwards): the event and its date are documented, the step size per region is not, and the default adjustment is the easy route. Labelling afterwards (dropping Kestrow North and Varrenby Shore as artefacts) misses the Capital, which the step pushes the other way.
  - `strategies.md`, every reflex lands wrong: the reflexes for a seasonal series (STL, the classical decomposition, robust STL) each file a wrong set; only removing the step before the pattern is estimated reaches the golden, and every step-aware variant does.
  - `layer1-messiness.md`, official statistics (layout changes across years, a preliminary and a revised release overlapping, a concordance across a boundary change): Layer 1, every item neutral to the call and asserted so.
  - task450 (a new form linked to the reporting scale through shared items): both cross a change in the measuring instrument, but task450 links levels across forms for a cohort; here the compared levels need no link (both after the change) and the change instead corrupts a seasonal pattern estimated across it.
- **Generator** (`task453/generator/`, seeded): the regional series are simulated with each region's own and branch jobs, the step, an irregular of 0.25 per cent (the Capital) to 0.9 per cent a month, and a seasonal amplitude of 2 to 4.5 per cent. Measured on the shipped pack: eleven step-aware routes designate the same three regions, at least 0.51 from the line; five default routes designate the same wrong four, at least 0.32 from the line; robust STL designates the Capital and Pellmarsh Hills.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the regulation: a region is designated for a quarter when its seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its payroll jobs for the preceding calendar year, each the average of its months, compared unrounded.
2. Conform the agency's statistics: the 2021 to 2023 yearly tables and the January 2024 to March 2027 monthly file, the revision file's January to March 2027 in place of the preliminary months, municipalities to economic regions through the concordance (the retired Wexleigh and Dorran codes included); sum each region by month.
3. Read the release note: from January 2026 the statistics place jobs at the workplace, earlier months at the account address and not revised. The first quarter of 2027 and 2026 are both on the workplace placement, so the comparison is like for like and the change needs no adjustment.
4. Seasonally adjust each region's monthly series over its whole history, January 2021 to March 2027, with STL (or the classical decomposition).
5. Average each region's seasonally adjusted jobs over January to March 2027, compare with its 2026 average and designate the regions more than 1.0 per cent below: Brennick Valley at 2.4 per cent, Kestrow North 1.6, Varrenby Shore 1.5 and Pellmarsh Hills 2.8, with the Capital at 0.6.

**Ends on:** designate Brennick Valley, Kestrow North, Varrenby Shore and Pellmarsh Hills.

**Golden:** designate Brennick Valley, the Capital and Pellmarsh Hills.

## Stump sentence

The default path designates Brennick Valley, Kestrow North, Varrenby Shore and Pellmarsh Hills because step 4 estimates each region's seasonal pattern across the January 2026 move to workplace placement without removing it: the step leaks into the first-quarter seasonal factors in proportion to its size, pulling the first quarter of 2027 below the line in Kestrow North and Varrenby Shore, whose mines, mills and plants the agency counted at head offices in Wickmoor until 2026, and lifting the Capital, which lost those jobs, above it; removing the step as a level shift before the seasonal pattern is estimated (or restating the earlier history to the new placement) designates Brennick Valley, the Capital and Pellmarsh Hills.

## Three rules

**Task type:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production (`seasonal-adjustment-official-time-series-production`), serving the ETL objective: the bureau's conformed regional payroll-jobs series, seasonally adjusted, built from the revenue agency's employer return statistics.

**Domain test:** the deciding quantity is each region's seasonally adjusted payroll jobs for the first quarter of 2027 against its 2026 average. Official time-series production removes a documented break in an administrative source as a level shift in the regARIMA pre-adjustment before the seasonal filters run (X-13's practice, the client's SROS seasonal-adjustment pattern 1). The series is an official one a statute reads, built from returns whose placement of jobs a filing change moved.

**Swap:** "the bureau certifies the regions whose seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below the previous year's average". Put another field's nouns in (a retailer's sales by district, a clinic's visits) and the object goes: there is no administrative return whose placement a filing change moved, no official seasonally adjusted series a statute reads, and such a business compares a quarter with the same quarter a year before; the decisive step (pre-adjusting a documented break before the seasonal pattern is estimated) is the official producer's practice for its own series.

**Layer 1:** what the revenue agency's and the bureau's systems produce, none of it on the decisive step.
- The statistics come in two layouts: yearly tables with a column a month and the agency's industry groups to 2023, a long monthly file by NAICS sector from 2024.
- Wexleigh and Dorran amalgamated as Wexleigh-Dorran on 1 January 2025; the concordance carries the retired codes with their dates, all in Quillon Plain.
- January to March 2027 are preliminary in the April file; the revision file of 7 May replaces them.
- The workplace returns list each workplace once per payroll account, under the account's own workplace number.
- The labour force survey's regional estimates and the population estimates sit beside the returns as distractors.

**Layer 2:** field_method. Each region's seasonal pattern is estimated from a history that spans a documented change in where the source places its jobs. The official producer removes the change as a level shift in the regARIMA pre-adjustment, or restates the earlier history to the new placement, before the seasonal filters run.

**Decisive step:** removing the January 2026 change of placement from each region's history before its seasonal pattern is estimated, although both periods the trigger compares lie after it. A default adjustment estimates the pattern across the change, its trend unable to jump, and the step leaks into the first-quarter factors in proportion to its size and in its direction.

**Not semantics:** every field, code and unit read right (the release note's change and its date, the placement before and after it, the layouts, the concordance, the preliminary and revised months) still leaves the seasonal pattern to be estimated. The default path reads the note correctly, concludes rightly that both compared periods are on the workplace placement, and still designates the wrong four.

**Not rule application:** the regulation files the WHAT (the quarter's seasonally adjusted jobs against the previous year's average, the 1.0 per cent line, regions by municipality, the returns and revisions in hand) and no method. No filed sentence says how to seasonally adjust or that a change of placement must be pre-adjusted, so executing every filed rule with a standard adjustment still designates the wrong four.

**Analyst test:** a strong analyst who conforms the statistics, reads the January 2026 release note correctly and seasonally adjusts each region's whole series with STL or the classical decomposition designates Brennick Valley, Kestrow North, Varrenby Shore and Pellmarsh Hills (the default path's `Ends on:`), against Brennick Valley, the Capital and Pellmarsh Hills.

**Estimand:** the Regional Rapid Response Program Regulation, sections 1 and 2. A region is designated for a quarter if its seasonally adjusted payroll jobs for the quarter (the average of its three months) are more than 1.0 per cent below its payroll jobs for the preceding calendar year (the average of the year's twelve months), compared unrounded; payroll jobs are the jobs on employers' monthly returns at workplaces in the region's municipalities; the certification uses the returns and revisions supplied by its date (section 3(2)).

**No decoy:** nothing is planted to be caught. The change of placement is an administrative event the agency documents in its release note. No published seasonally adjusted series, earlier certification, memo or preliminary figure states a region's adjusted jobs or verdict.

**No certified replay:** no shipped figure is reproduced to recover a method; no seasonal factors or adjusted series ship.

**Lesson:** a seasonal pattern estimated from a history that spans a documented change in what a region's series counts carries the change into the seasonal factors, even when every period compared lies after it, and in both directions, so the change is removed as a level shift before the pattern is estimated. No build on file teaches it (the nearest driver, task30 round 3 at 0.08, segmented a corpus to the post-change cohort).

## Readability screen

A row per move up the ladder. Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear; "fires" means the test hands the move over.

| Rung | Move | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|---|
| R1 | robust STL, outlier-resistant weights | no | no | fires: robust=True is a stock option | no | no | no | readable |
| R1b | the seasonal pattern from 2026 alone, the months on the new placement (year on year) | fires: the note says earlier months are not revised | no | no | no | no | fires: one ratio a month | readable |
| R2 (decisive) | the change removed as a level shift before the seasonal pattern is estimated (or the history restated) | no: the note speaks of placement and levels, the regulation of the comparison; neither speaks of the seasonal pattern | no: no column marks the change; the statistics carry no basis flag | no: the stock routes for a seasonal series (STL, the classical decomposition, robust STL) all run across the change | no: no published adjusted series, no earlier certification | no: every series passes the battery; the province total shows no break | no: the bias is a filter's leak, no subtraction finds it | silent |

## Semantic fork table

Each term of the main ask and each convention the computation needs; the stump is none of them.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | economic region | the Schedule's ten regions, municipalities by the concordance | Wexleigh and Dorran joined only under the current code (their 2021 to 2024 rows dropped) | same call (Quillon Plain stays above the line; asserted) | the concordance lists both retired codes with their dates, in Quillon Plain |
| SF2 | payroll jobs | jobs on employers' monthly returns (the dictionary: employees paid in the month's pay periods) | none in the files | same call | one measure ships |
| SF3 | at workplaces in the region's municipalities | 2026 and the quarter are on the workplace placement | the months before 2026 read as workplace jobs | same call (the comparison uses only months from 2026) | the release note: earlier months place jobs at the account address and are not revised |
| SF4 | payroll jobs for a quarter | the average of the quarter's three months | the March figure, or the sum | same call on the average; the sum is no comparison | regulation 1(2) |
| SF5 | payroll jobs for the preceding calendar year | the average of 2026's twelve months, unadjusted | the seasonally adjusted 2026 average | same call (every step-aware route; asserted) | regulation 1(2), and convergence |
| SF6 | more than 1.0 per cent below | strictly below minus 1.0 per cent, unrounded | at or below, or on rounded figures | same call (no region within 0.5 of the line on the eleven step-aware routes; asserted) | regulation 2(1), 2(2) |
| SF7 | seasonally adjusted | the region's jobs with its seasonal pattern removed, the pattern estimated on one placement | each step-aware method (regression with a level shift over two spans and two knot spacings, STL and the classical decomposition on the restated history, factors from before the change, three restatements) | same call (eleven routes; asserted) | convergence; the routes across the change are the stump, not a reading (Literal reader) |
| SF8 | the returns and revisions supplied by the date of certification | the revision file's January to March 2027 replace the April file's | the April file's preliminary months | same call (asserted) | regulation 3(2); the transmittal says the revision file replaces those months |
| SF9 | the quarter | January to March 2027 | another quarter | same call | the prompt and the regulation's definition of quarter |
| SF10 | rounding path | compared unrounded; jobs reported to the nearest 10 | rounded before comparing | same call (asserted) | regulation 2(2) |
| SF11 | direct or indirect adjustment | each region's own series adjusted | municipalities or sectors adjusted and summed | same call on the region's series; the cells are too small to adjust | the regulation's quantity is the region's |
| SF12 | the quarter's seasonally adjusted jobs | the average of the three months' adjusted jobs | the region's quarterly series adjusted with quarter effects | same call (a quarterly regression with a level shift; asserted) | convergence |

## Ladder

The candidates are the ten regions; the call is the set more than 1.0 per cent below. Per cent below the 2026 average for the five regions any route moves, on the shipped pack:

| Rung | Route | Capital | Brennick Valley | Kestrow North | Pellmarsh Hills | Varrenby Shore | Set |
|---|---|---|---|---|---|---|---|
| R0 | STL across the change (default) | -0.6 | -2.4 | -1.6 | -2.8 | -1.5 | Brennick Valley, Kestrow North, Varrenby Shore, Pellmarsh Hills |
| R0 | classical decomposition across the change | -0.2 | -2.4 | -2.0 | -2.8 | -1.5 | the same four |
| R1 | robust STL across the change | -1.4 | -0.2 | +1.8 | -2.0 | 0.0 | the Capital, Pellmarsh Hills |
| R1b | 2026 alone (year on year) | -2.5 | -3.5 | -0.4 | -3.6 | -0.4 | the golden three, on three components' figures outside their ranges |
| R2 | level shift removed (the bureau's regression) | -1.6 | -1.9 | -0.4 | -2.1 | +0.1 | Brennick Valley, the Capital, Pellmarsh Hills |
| R2 | eleven step-aware routes, range rounded outward | -1.7 to -1.5 | -2.3 to -1.8 | -0.4 to +0.2 | -2.6 to -2.0 | -0.4 to +0.2 | the same three |

- **Winners and margins:** every step-aware route keeps every region at least 0.51 from the line; every default route (STL on logs and on levels, STL with a 13-year seasonal window, the classical decomposition multiplicative and additive) keeps its wrong four at least 0.32 from the line.
- **Position:** the default answer shares two of four regions with the golden; it adds Kestrow North and Varrenby Shore (the two largest steps up, 28 and 23 per cent) and drops the Capital (the largest step down, 16 per cent).
- **Dominance:** the leak scales with the step: the default moves Kestrow North by 1.2 points, Varrenby Shore by 1.6 and the Capital by 1.0 the other way, against margins of 0.6 to 1.1 on the golden.
- **Worth:** R2 is the only move that reverses the Capital, Kestrow North and Varrenby Shore together; R1 reverses Brennick Valley the wrong way; R1b lands the set with the Capital's, Brennick Valley's and Pellmarsh Hills' figures outside their step-aware ranges.
- **Grid:** the five components each sit on one side of the line under every step-aware route and on the other under every default route; no partial correction (dropping the two regions that gained most, as the client's pattern calls labelling afterwards) adds the Capital.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the Schedule's ten regions; every municipality in the concordance | filed (regulation 1(1), the Schedule); C1 on the retired codes (SF1) |
| 2 Unit of account | the economic region's payroll jobs | filed (regulation 1(1)) |
| 3 Attribution window | January to March 2027 against January to December 2026, by reference month | filed (regulation 1(2)) |
| 4 As-of dating | returns and revisions supplied by the certification date | filed (regulation 3(2)); the transmittal dates the files |
| 5 Version basis | the revision file's months replace the preliminary ones | filed (3(2), transmittal); C1 (SF8) |
| 6 Denominator | the 2026 average, unadjusted | filed (2(1), 1(2)); C1 on the adjusted alternative (SF5) |
| 7 Weighting | months weighted equally in each average | filed (averages of months, 1(2)) |
| 8 Window length | the span the seasonal pattern is estimated on (2021 to 2027, 2023 to 2027, before the change only) | C1 across spans (asserted) |
| 9 Boundary inclusivity | strictly more than 1.0 per cent below | filed (2(1)); C1, nothing within 0.5 of the line |
| 10 Rounding path | unrounded comparison; jobs reported to 10 | filed (2(2)) |
| 11 Tie-break | none: a set against a line, not a ranking | C1, no region within 0.5 of the line |
| 12 Maturity and censoring | preliminary against revised months | filed (3(2)); C1 (SF8) |
| 13 Order of operations | conform, sum to regions, adjust the region's series | filed quantity is the region's (SF11) |
| 14 Row order | sums and averages | C1 by construction |
| 15 Duplicate resolution | the revision file replaces whole months; no repeated rows | C1 (asserted) |
| 16 Identity normalisation | municipal codes as text with leading zeros; retired codes | dictionary and concordance; C1 |
| 17 Netting against gross | net payroll jobs per region | filed (the regulation's jobs are a level) |
| 18 Dimensional units | jobs in every file | C1 |
| 19 Code and status semantics | status F, P, R | dictionary; C1 (SF8) |
| 20 Integerisation | none: jobs are whole, the test unrounded | n/a, asserted unrounded |
| 21 Clause scope | section 2 per region per quarter | filed |
| 22 Forward window contents | none: a closed quarter | n/a; retrospective by design (Draw) |

## Literal reader

The prompt and the regulation, executed word for word, fix the estimand: each region's seasonally adjusted payroll jobs for January to March 2027, the average of its three months, against the average of its payroll jobs for the twelve months of 2026, designated when more than 1.0 per cent below on unrounded figures, with payroll jobs the jobs on employers' returns at workplaces in the region's municipalities and the returns as revised on 7 May (SF1 to SF12). How the seasonal pattern is estimated is filed nowhere; the data force it. The release note documents that the agency's regional figures before January 2026 place each job at its employer's account address and were not revised, and each region's series steps at January 2026 by 6 to 28 per cent. A seasonal pattern estimated across that step takes up part of it (a movement that happened once, not one that recurs each year), so the first quarter's factors carry the step into 2027; every route that estimates the pattern on one placement (eleven of them) designates the same three regions, at least 0.51 from the line. The default's four come from the method, not from a reading.

## Oracles

- The province's total: no break at January 2026 (the change moved jobs between regions). It ties under every route and confirms nothing about a region.
- The release note: documents the change and its date; it states no adjusted figure and no method, so it confirms neither set.
- The workplace returns: their March 2026 and March 2027 totals tie to the statistics by region and cell under every route (asserted); no seasonal content.
- The labour force survey: residents' employment, unaffected by the agency's placement, as unadjusted three-month averages with sampling noise of 1.5 to 3.5 per cent; its first quarter of 2027 against its 2026 average designates a set that is neither the golden nor the default (asserted).
- The transmittal's row counts: tie under every route.
- None ties only under the golden; none ties only on the wrong read.

## Ask sheet

**The main call's declared population:** the agency's statistics (the 2021 to 2023 yearly tables, the 2024 to 2027 monthly file, the revision file), the concordance, the regulation and the release note. Zero ask device rows in it: the workplace returns are read by no step of the call, and deleting them leaves the call and every component (asserted); their March totals tie to the statistics, so they neither feed nor referee the call.

**Ask A: the payroll jobs lost between March 2026 and March 2027 at each region's workplaces whose payroll jobs fell** (20 figures: at those with none left in March 2027, and at those that kept some; nearest 10).
- H18 home: regulation 4(1)(a), workforce adjustment services for workers whose jobs at the region's workplaces ended or were cut. A measure every region carries; the call does not turn on it.
- Use: the Minister sizes the services in the regions certified.
- Construction: each workplace's payroll jobs in March 2026 and in March 2027, a workplace being the place (regulation 1(1): a place in the province at which an employer's employees work; on the returns, its municipality and street address), and the fall at each.
- Primary device: D7, records billed to another holder after a transfer. Fifty workplaces (five a region) changed hands between the two Marches and appear in March 2027 under the buyer's payroll account and its own workplace number at the same address; Larkmoor Express stores moved into the Larkmoor Foods account; about a thousand addresses in each March (1,048 in 2026, 1,040 in 2027) carry lines on two of one employer's accounts (teachers and support staff at most schools, salaried and hourly staff at most health sites, council and staff). Keyed on account and workplace number, each changed workplace closes and a new one opens, and each two-account workplace splits in two. Only the street address, shared across accounts and months, shows it; the regulation defines a workplace as a place and no sentence says a place can sit on two accounts or change hands.
- Hazards: nil lines (seasonal workplaces listed with no employees paid; seen); March 2026 and March 2027 in one file (seen).
- Path: the workplace returns, the concordance, the dictionary, the transmittal (four files, seven columns).
- Stops: account and workplace number (every figure off: none left +182 to +272, kept some -75 to -48); business number and address (+172 to +231, -78 to -46); legal name and address (+172 to +231, -76 to -46); the golden.
- Realism: a workplace sold or moved to another payroll account is re-registered on the new account's schedule with the next number, and the agency keeps one address standard.

**Ask B: the employers with payroll jobs at each region's workplaces in March 2027** (10 figures, whole numbers).
- H18 home: regulation 4(1)(b), outreach to the employers with workplaces in the region.
- Use: the outreach workload in each region.
- Construction: the employers (the payroll account's first nine digits, the business number of the employer that holds the account) with a March 2027 line in the region with payroll jobs above zero.
- Primary device: D1, the same records under two key schemes. Seventeen to 79 businesses a region pay from two payroll program accounts (RP0001 and RP0002): school divisions, the two health authorities, municipalities, the provincial services agency, Larkmoor Foods and about one local business in sixteen with 15 or more jobs. Counting accounts overcounts every region by 17 to 79; counting legal names overcounts by 9 to 27 (a second account keeps the name the business used before a rename); counting operating names undercounts by 50 to 946 (franchisees and family firms share trade names). The field descriptions give the account as the business number of the employer that holds it, the program identifier and a reference number; no sentence says an employer may hold two.
- Hazards: nil lines (counted, they add the seasonal workplaces' employers; seen); employers in several regions (counted in each; stated non-additivity).
- Path: the workplace returns, the concordance, the dictionary (three files, six columns).
- Stops: accounts, legal names, operating names, the golden.
- Realism: an employer paying two cycles or two bargaining units holds two payroll program accounts under one business number, and a rename reaches the account in daily use first.

**Construction layer:** the certificate's figures for the three designated regions (each one's seasonally adjusted payroll jobs for the quarter and its 2026 payroll jobs, regulation 3(3)), graded as the range the step-aware routes give. The cracker keeps them; the mirror's set leaves out the Capital and its Brennick Valley and Pellmarsh Hills adjusted figures fall outside the ranges.

**Hazard table:**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| a line in March 2027 read as payroll jobs (nil lines of closed and seasonal workplaces counted) | B | +7 to +51, every region |
| two months in one file read as one | A | every figure (no fall measured) |
| the concordance skipped (municipal codes read as regions) | A, B | every figure |

**Referee:** none; each ask's golden recomputes from the workplace returns and the concordance alone.

**Cracker sheet:** the cracker landed the call, ran the battery (keys unique on account, workplace number and month; no repeated rows; every municipal code joins) and keys workplaces on account and workplace number and employers on the payroll account, the file's identifiers.

| Ask figure | Cracker's read | Cracker | Golden | Verdict |
|---|---|---|---|---|
| A, Capital, none left | account and workplace number | 2,650 | 2,390 | miss |
| A, Capital, kept some | account and workplace number | 4,940 | 5,010 | miss |
| A, Saltmere Coast, none left | account and workplace number | 1,650 | 1,430 | miss |
| A, Saltmere Coast, kept some | account and workplace number | 1,710 | 1,760 | miss |
| A, Brennick Valley, none left | account and workplace number | 1,080 | 820 | miss |
| A, Brennick Valley, kept some | account and workplace number | 1,610 | 1,670 | miss |
| A, Dunfallow Bay, none left | account and workplace number | 780 | 570 | miss |
| A, Dunfallow Bay, kept some | account and workplace number | 690 | 740 | miss |
| A, Quillon Plain, none left | account and workplace number | 1,210 | 940 | miss |
| A, Quillon Plain, kept some | account and workplace number | 1,170 | 1,220 | miss |
| A, Hethervale Lakes, none left | account and workplace number | 670 | 490 | miss |
| A, Hethervale Lakes, kept some | account and workplace number | 630 | 690 | miss |
| A, Ardvane Uplands, none left | account and workplace number | 570 | 340 | miss |
| A, Ardvane Uplands, kept some | account and workplace number | 460 | 540 | miss |
| A, Kestrow North, none left | account and workplace number | 670 | 410 | miss |
| A, Kestrow North, kept some | account and workplace number | 1,130 | 1,190 | miss |
| A, Pellmarsh Hills, none left | account and workplace number | 1,080 | 840 | miss |
| A, Pellmarsh Hills, kept some | account and workplace number | 1,610 | 1,660 | miss |
| A, Varrenby Shore, none left | account and workplace number | 570 | 380 | miss |
| A, Varrenby Shore, kept some | account and workplace number | 700 | 760 | miss |
| B, Capital | payroll accounts | 5,860 | 5,781 | miss |
| B, Saltmere Coast | payroll accounts | 3,523 | 3,490 | miss |
| B, Brennick Valley | payroll accounts | 2,155 | 2,125 | miss |
| B, Dunfallow Bay | payroll accounts | 1,413 | 1,386 | miss |
| B, Quillon Plain | payroll accounts | 2,235 | 2,197 | miss |
| B, Hethervale Lakes | payroll accounts | 1,307 | 1,288 | miss |
| B, Ardvane Uplands | payroll accounts | 1,139 | 1,116 | miss |
| B, Kestrow North | payroll accounts | 1,187 | 1,158 | miss |
| B, Pellmarsh Hills | payroll accounts | 1,641 | 1,617 | miss |
| B, Varrenby Shore | payroll accounts | 1,087 | 1,070 | miss |

Mirror leakage: 10 per cent of ask weight (the mirror, stopping at the default path, keeps the chart's layout and the 2026 payroll jobs of Brennick Valley and Pellmarsh Hills, which it also certifies: about 4 of 41 ask-side criteria).

Pair ceiling: 37 (planning weights 38 / 7 / 55 with the designated set and its five components as the main block and r = 5; the cracker keeps the main block, the certificate's six figures and the chart's three parts, 38 + 7 + 55 x 9/41 = 57.1; the mirror keeps r, instruction-following and its four ask-side criteria, 5 + 7 + 55 x 4/41 = 17.4; (57.1 + 17.4) / 2 = 37.3).

Residual risk: ask B turns on counting payroll accounts or legal names. The field descriptions give an account's first nine digits as the business number of the employer that holds it (the pin that makes the ask determinate), so a solver who reads that line as identity lands ask B's ten figures; with the call landed and both top responses counting employers that way, the cracker keeps 19 of 41 ask-side criteria (70.5) and the mirror 14 (30.8), a pair of 50.7. Ask A needs one street address recognised as one place across accounts and months, which the regulation's definition of a workplace as a place does not point at.

## Pre-ship check

- **Three rules.** Domain: official statistics' own seasonal adjustment, each region's seasonal factors estimated with the January 2026 move to workplace placement taken out as a level shift, the way a regARIMA model with a level-shift regressor treats a documented break before seasonal filtering (swap test in the Three rules section). Two layers: the Layer 1 inventory (the agency's statistics in two layouts, municipal codes retired by the 2025 amalgamation and joined through the concordance, preliminary months beside the revision file, the move of placement documented in the release note; for the asks, workplace schedules keyed by account and number, with sales, two-account sites and nil lines), all of it what the agency's and the bureau's systems write; and the estimation of seasonal factors across a level shift, which carries the call. Decisive step analytical: the analyst who conforms every file, applies every filed rule and seasonally adjusts with STL or the classical decomposition files Brennick Valley, Kestrow North, Varrenby Shore and Pellmarsh Hills on the clean truth (R3a, asserted); changing only the level shift files the golden (R3b, asserted); robust STL and the year-on-year route stay off it.
- **Gates.** 11 files in 4 formats (csv, xlsx, pdf, txt); the workplace returns at 47,647 rows and the monthly statistics at 29,118; two distractors (the labour force survey's regional estimates and the population estimates) the solution never reads; 90 checks; `verify.py` from the bundle alone (the level-shift regression and the classical decomposition on the restated history, the default across the change, every CSV figure and the 2026 averages); two builds byte-identical; `figures_check.py` exit 0 (77 figures); `precut.py` exit 0; `leak.py --asof 2027-05-07` REVIEW with no LEAK; `guard.py heart` WARN (`repeat.question_form` against task451 v2, answered in the Draw: a designation set is asked with which); `guard.py surface` 0 pairs promoted, the personas in the pack the card's four.
- **The main call after stage 4.** The reader's fixes (the ask's wording, the employer and workplace pins, names and addresses varied, sectors absent from small municipalities, second lines at most sites rather than all) moved no main-call figure: the call, every region's percentage, range, adjusted jobs and 2026 average in `figures.json` are the ones the judge reproduced, the sectors' absence redistributing jobs inside each region and the workplace returns being read by no step of the call.

## Leak check

- `leak.py --asof 2027-05-07` (after the final build): REVIEW, no LEAK. The REVIEW lines: the regulation carries the call's words (the region names in its Schedule, designated and quarter in its test); the release note, the transmittal and the regulation share the design's ordinary vocabulary (change, January, months, statistics, workplace, seasonal, adjusted), none naming a method or the level shift; the concordance, the labour force survey's estimates and the workplace returns name the regions beside numbers (codes, monthly estimates, school divisions named for their regions), none ranking them.
- Reader, pass 1 (isolated, Sonnet, medium, fresh copies of the prompt and the pack): Q1 to Q4 none; Q5 every filed sentence executes to the golden's population (place of work, the quarter's and the year's averages, the revised months, unrounded), the seasonal adjustment named but not its method; Q6 an analytical choice. Q7 two tells: the two health authorities at 220 workplace lines each and the revision file a full rectangle of municipalities by sectors. Q8 three readings in the asks: an employer as an account or a business, "no payroll jobs" as the lines listed at zero or also the workplaces gone from the schedules, and the loss at "those with fewer" as gross or net.
- Reader, pass 2 (after the first fixes): Q1 to Q4 none; Q5 the golden's population; Q6 an analytical choice. Q7 business names templated and every operating name the legal name less its suffix. Q8 the employer still read either way, and a workplace read as an account's schedule line or a place.
- Reader, pass 3 (after the second fixes; same isolation, fresh copies): Q1 to Q4 none; Q5 every filed sentence executes to the golden's population, the seasonal adjustment's method left open; Q6 an analytical choice. Q8: the employer settled by the account's description (no fork); the losses read on account and workplace number, the ask's device path, the regulation's definition of a workplace as a place ruling that key out; a workplace on no March 2027 return read as having none left, regulation 1(1) counting payroll jobs as the jobs on the returns. Q7: second accounts' operating names carry a payroll's label (hourly, part-time, seasonal, support staff, council and fire, or none), numbered companies about one business in eight, every format regular as a system export; harmless. Every sweep line harmless.
- Fixes, in the generator: the ask asks for the jobs lost at the workplaces whose payroll jobs fell, for those with none left and those that kept some; the field description gives an account's first nine digits as the business number of the employer that holds it; the regulation defines a workplace as a place in the province at which an employer's employees work; about one health site in six and one school in fourteen pay on one account; small municipalities carry no jobs in sectors their economy lacks; numbered companies trading under their own or a franchise's name, family, initial and holding names, and rural and numbered-street addresses.

## Determinism judge

- Pass 1 (2026-10-13, isolated thread on the cut before the reader's fixes): DETERMINISTIC, APPROVE. Every figure reproduced: the 2026 averages, the level shifts (-16.3, +27.6 and +23.2 per cent), each region's quarter against its 2026 average on more than 20 step-aware variants (Brennick Valley 1.87 to 2.11 below, the Capital 1.45 to 1.67, Pellmarsh Hills 2.05 to 2.56, Kestrow North and Varrenby Shore between 0.4 below and 0.2 above, no other region nearer the line than 0.63), the certificate's ranges, and all 30 ask figures. Gate G method_or_model_selection, analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain pass, layers pass, decisive step analytical; Gate F adequate. Its notes: the seasonal adjustment's method is the one residual freedom and the data separate the candidates; the workplace key and the employer unit are mild exposures on the asks (both since pinned); optionally, name the CSV's columns and row order in the write-up (done). Report: `determinism_check_report.md`. No re-judge: the verdict was APPROVE, the main call's figures did not move, and `verify.py` recomputes every changed ask figure from the bundle.

## Tried and rejected

- 2026-10-13, draw: seed ET10's world (a patient-advocacy report card on trial results reporting). Rejected: its natural client domains (biomedical and clinical research, pharmacology) have no task type serving ETL, and the deciding rate is a deadline count under stated rules, a backdrop the 10/10 rules ban.
- 2026-10-13, draw: the quarter-on-quarter change in seasonally adjusted jobs (the fourth quarter of 2026 to the first of 2027) as the trigger. Rejected: at the end of a series the step-aware methods themselves disagree by up to a point on a quarter's change, too much for a determinate line; the trigger compares the quarter with the previous calendar year's average, which needs no adjustment.
- 2026-10-13, draw: growth from a base year before the change (2025) to the latest four quarters. Rejected: the change then enters the level directly, so every careful analyst links the series first, and the linking ladder (a December to January ratio, a year-on-year ratio, a regression) repeats task450's link-across-a-change structure.
- 2026-10-13, draw: the card's first signature (population, G16, method_or_model_selection). Rejected by the guard as a spent driver (task501 v4, task104, task134 v1, task70 v2); the decisive move is conformance of the series to one placement, filed as etl_conformance.
- 2026-10-13, draw: a regional irregular of 0.25 per cent in the simulation. Rejected: robust STL then down-weights the months around the step so completely that it lands the golden in 19 of 20 seeds; at the 0.6 to 1.0 per cent irregular regional payroll series carry, it misses.
- 2026-10-13, design: the quarterly remitters joining the monthly returns in January 2026 as the change. Rejected: every step is upward, so the default only over-designates and labelling the two big-step regions afterwards lands the golden; and a fifth of a rural region's jobs missing from monthly returns strains belief. The move from account-address to workplace placement gives steps both ways, leaves the province's total unchanged, and puts the Capital on the golden that no after-the-fact labelling adds.
- 2026-10-13, design: a history from January 2018. Rejected: a 2020 without the pandemic's payroll collapse reads as constructed; the series start in January 2021.
- 2026-10-13, design: turns inside 2026 to make the year-on-year route miss (a mid-year hump in Brennick Valley, an early-2026 high in Dunfallow Bay). Rejected: STL on the restated history then absorbs the turn and leaves the step-aware routes disagreeing near the line; the year-on-year route lands the golden set on figures outside every step-aware range, and stays there.
- 2026-10-13, design: hitting each region's target with an offset at the break. Rejected: the step-aware regression's level shift absorbs any offset at January 2026, so the offset ramps in from mid-2026.
- 2026-10-13, design: a designation column per region in the deliverable CSV. Rejected: the default path's set agrees with the golden on seven of ten verdicts, so ten such criteria hand the mirror most of a block; the CSV carries only the asks, the certificate the designated set.
- 2026-10-13, design: employer counts with one account per business and legal names unique. Rejected: counting legal names then lands the golden; second accounts keep the name before a rename, so only the business number counts businesses.
- 2026-10-13, design: group termination notices, payroll dollars in cents and priority industries through a code revision as ask devices. Rejected: notice amendments are battery-visible, cents need a filed specification to be determinate, and a code revision needs a filed rule or reissued codes; workplace identity across accounts and businesses across accounts are silent and determinate from the returns alone.
- 2026-10-13, stage 4: the ask worded "the payroll jobs its workplaces lost between March 2026 and March 2027, given separately for workplaces with no payroll jobs in March 2027 and for those with fewer". Rejected: the reader read "no payroll jobs" as the lines listed at zero only and "those with fewer" as possibly net of gains; the ask now asks for the jobs lost at the workplaces whose payroll jobs fell, for those with none left in March 2027 and those that kept some.
- 2026-10-13, stage 4: the payroll account described as "the business number (nine digits), the program identifier RP and a four-digit reference number", then as the business number "of the business that holds the account". Rejected: both times the reader found no sentence tying an employer to an account or to a business; the description now gives the business number of the employer that holds the account.
- 2026-10-13, stage 4: the workplace left to the field descriptions (its standardised street address, its sequence number on an account's schedule). Rejected: the second reader still read a workplace as an account's schedule line; the regulation defines a workplace as a place in the province at which an employer's employees work, and says nothing of accounts, numbers or changes of hands.
- 2026-10-13, stage 4: every health site and every school paying on both accounts, and every sector in every municipality. Rejected: the two health authorities came out at 220 workplace lines each and the revision file as a full rectangle of 43 municipalities by 20 sectors, tells the reader saw; about one health site in six and one school in fourteen now pay on one account, and small municipalities carry no jobs in sectors their economy lacks.
- 2026-10-13, stage 4: business names built from a feature word, a trade and a suffix, each operating under its legal name less the suffix. Rejected: the reader read them as templated; numbered companies trading under their own or a franchise's name, family, initial and holding names, former names in the same trade, and rural and numbered-street addresses vary the file.
- 2026-10-13, second-layer attempt after shipping (prototype): the seasonal pattern moved with the jobs (the branch jobs given their own winter trough, so a level-shift regressor alone would leave the Capital's factors carrying a pattern it lost and a month-by-month restatement through a 2025 dual tabulation would be the only right route). Rejected on the prototype: with the branch jobs' seasonal amplitude at 0.10 to 0.18 the step-aware routes still certified the golden three (the level shift removed and STL, the annual-ratio restatement, the monthly restatement and the classical decomposition all agreed); only the bureau's fixed month-effect regression lost the Capital, at amplitudes that make the receiving regions' winters implausible. STL's seasonal window adapts to the moved pattern within the post-change months, and the moved jobs are a sixth of the Capital's history, so the pattern's move stays inside the margins.
