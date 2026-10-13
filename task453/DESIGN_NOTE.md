# task453 design note

Architecture 1, drawn 2026-10-13 (wave 2, oviya1301). The seed (ET10, trial-results reporting compliance) is not kept: its world sits in the biomedical and pharmacology domains, none of whose task types serves ETL, and its rate is a stated deadline count, the backdrop the 10/10 rules ban. The three ETL task types the last three builds hold (payment and claims, emissions inventory, test equating) are banned, so the pairing comes from an ETL task type the client lists and no build has drawn: seasonal adjustment and official time-series production.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task453.json`, architecture v1, registered 2026-10-13. `guard.py check` returns WARN only. Each WARN is answered here.
  - `repeat.question_form` (which, as task451): the call is a designation set, and a set of regions is asked with which.
  - `test.same_driver` on (population, G16, method_or_model_selection) blocked the first card (task501 v4 and four older builds). The honest Gate G is conformance: the decisive move puts a series on one coverage basis before its seasonal pattern is estimated. The card carries etl_conformance, and differentiation against task139 and task30.
  - The nearest driver (task30 round 3, 0.08) segmented a calibration corpus to the cohort after a methodology change. Here the post-change span is 15 months, too short to estimate a seasonal pattern; segmenting to it is one of the wrong rungs, and the golden keeps the whole history with the change removed as a level shift.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / Data Extraction & Conformation (ETL). A provincial statistics bureau builds each economic region's monthly payroll-jobs series from the revenue service's monthly employer returns, seasonally adjusts it, and certifies to the Minister which regions a statutory trigger designates for the Regional Rapid Response Program. Removing a documented break in an administrative source as a level shift before the seasonal filters is official series production's own method (the client's pattern `survey-research-official-statistics/seasonal-adjustment-official-time-series-production/1`).
- **Objective:** ETL. The conformed dataset is each region's monthly payroll-jobs series on one coverage basis (two layouts of returns, a municipal concordance across an amalgamation, revised months replacing preliminary ones), seasonally adjusted, with the trigger read off it and two per-region measures beside it.
  - Retrospective by design: the trigger reads the quarter just closed (January to March 2027) against the calendar year before.
  - Not retaggable as Forecasting: nothing is predicted. The open part is the seasonal pattern used to adjust a closed quarter.
- **Shape:** 10, a scorecard against a threshold, one check per region. Criteria arithmetic (planned; the ask sheet fixes it at design):
  - each region's seasonally adjusted jobs for the quarter against its 2026 average, with its verdict, 10 regions;
  - two per-region asks on measures the trigger does not use (the region's employers with payroll jobs in March 2027, its March 2027 payroll jobs in the program's priority industries), 20;
  - the designated set, the chart and the two files.
  - About 35 in all.
- **Strategy:** population_selection. Rows before and after January 2026 count different populations of employers, and the decisive move is which history the seasonal pattern is estimated from, and on what basis.
- **Mechanism:**
  - Gap: population (decisive: the returns before January 2026 leave out the quarterly remitters, so the seasonal-irregular ratios around the change compare different populations), with time supporting (the seasonal pattern is estimated over a window that spans the change, while the compared periods both lie after it).
  - Generators: G16 decisive (the adjustment the data entitle), G6 (the counted population shifted under the series).
  - Gate G: etl_conformance. Layer 2: field_method, the client's SROS seasonal-adjustment pattern 1 (model level shifts in the regARIMA pre-adjustment before seasonal filtering).
- **World:** an unnamed Canadian province. Its Bureau of Statistics and Economic Analysis publishes monthly payroll jobs for ten economic regions, built from the employer returns that the province's revenue service collects and passes to the bureau each month.
  - From the January 2026 reference month, employers that had remitted source deductions quarterly began filing monthly returns. Their jobs are in the monthly statistics from that month and not before, as the revenue service's release note says.
  - The Regional Rapid Response Program Regulation designates a region for a quarter when its seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its average payroll jobs for the previous calendar year; the bureau certifies the regions to the Minister after each quarter's returns close.
- **As-of:** the first quarter of 2027; the revenue service's extract of 23 April 2027 and its revision file of 7 May 2027; the certification due 14 May 2027.
- **Furniture:**
  - Forum minister_or_cabinet (the bureau certifies to the Minister); forcing event period_close (the quarter's returns closed); organisation research_or_statistics_office (the provincial statistics bureau).
  - Role other (the manager of the bureau's regional labour statistics unit; the prompt names no one); context artifact register (the revenue service's return statistics); calibration none.
- **People:** drawn with `guard.py names --geo Canada --seed 453`, on the card: Joel Ferguson (Minister of Labour and Economic Development), Heidi Bond (the bureau's chief statistician), Jacqueline Chaney (the revenue service's statistical liaison, who signs the release note), Ryan Bentley (manager, regional labour statistics).
- **Data-native sentence:** the quarterly remitters are small employers, so they hold a fifth or more of the jobs in the rural regions and a few per cent in the city. Their arrival in January 2026 lifts every region's series by its own share at once. A seasonal adjustment run over the whole history reads that lift as part of January to June's seasonal pattern, because its trend cannot jump, so the first-quarter factors come out too high in proportion to the step. The first quarter of 2027 is then pulled down most where the remitters' share is largest, although both periods the trigger compares lie after the change. On a series whose coverage never changed, the trap would not exist.
- **Sources, one line each:**
  - `layer2-rigor-patterns.md`, SROS seasonal adjustment 1 (model outliers and level shifts in regARIMA before seasonal filtering; the shortcut runs the default adjustment and labels the event afterwards): the event and its date are documented, the step size is not, and the default adjustment is the easy route.
  - `strategies.md`, every reflex lands wrong: the reflexes for a seasonal series (STL, the classical method, robust STL, a year-on-year comparison, adjusting only the post-change months) each file a wrong set here; only removing the step first reaches the golden.
  - `layer1-messiness.md`, official statistics (layout changes across years, a preliminary and a revised release overlapping, a concordance across a boundary change): Layer 1, all of it neutral to the trigger and asserted so.
  - task450 (a new form linked to the reporting scale through shared items): both cross a change in the measuring instrument, but task450 links levels across forms for a cohort; here the levels need no link (both periods are after the change) and the change instead corrupts a seasonal pattern estimated across it.
- **Prototype** (scratch `t453/proto3.py` to `proto6.py`, ten simulated regions, statsmodels in a scratch venv): default STL and the classical moving-average method add the two high-step regions in every seed; robust STL lands the golden at a small irregular and misses at a regional irregular of 0.6 to 1.0 per cent; every step-aware method (a regression with a level shift over three windows, STL and the classical method on the restated history, pre-change factors) designates the same two regions. The build's measured ladder goes in `## Ladder`, asserted in `checks.py`.

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read the regulation: a region qualifies for a quarter when its seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below its average payroll jobs for the previous calendar year.
2. Conform the returns: the 2018 to 2023 yearly files and the 2024 to 2027 monthly file, municipalities to regions through the bureau's concordance (the 2025 amalgamation included), the revision file's months replacing the preliminary ones; sum each region's jobs by month.
3. Read the revenue service's release note: the quarterly remitters joined the monthly returns in January 2026. Both the first quarter of 2027 and the 2026 average are on the new coverage, so the comparison is like for like and the change needs no adjustment.
4. Seasonally adjust each region's monthly series over its whole history, January 2018 to March 2027, with a standard decomposition (STL, or the classical moving-average method).
5. Average each region's seasonally adjusted jobs over January to March 2027, compare with its 2026 average, and designate the regions more than 1.0 per cent below.

**Ends on:** designate Brennick Valley, Kestrow North, Oslin Shore and Pellmarsh Hills (as designed; the generator places each region's path and step so the built ladder lands it, asserted in `checks.py`).

**Golden:** designate Brennick Valley and Pellmarsh Hills, the two regions more than 1.0 per cent below their 2026 averages once the January 2026 coverage step is removed as a level shift before the seasonal pattern is estimated.

## Stump sentence

The default path designates Brennick Valley, Kestrow North, Oslin Shore and Pellmarsh Hills because step 4 estimates each region's seasonal pattern across the January 2026 coverage step without removing it: the step inflates the first-quarter seasonal factors in proportion to its size, which pulls the first quarter of 2027 below the line in Kestrow North and Oslin Shore, where the quarterly remitters hold over a fifth of the jobs; removing the step as a level shift before the seasonal pattern is estimated (or restating the earlier history to the new coverage) designates Brennick Valley and Pellmarsh Hills only.

## Three rules

**Task type:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production (`seasonal-adjustment-official-time-series-production`), serving the ETL objective: the bureau's conformed regional payroll-jobs series, seasonally adjusted, built from the revenue service's monthly employer returns.

**Domain test:** the deciding quantity is each region's seasonally adjusted payroll jobs for the first quarter of 2027 against its 2026 average. Official time-series production removes a documented break in an administrative source as a level shift in the regARIMA pre-adjustment before the seasonal filters run (X-13's practice, the client's SROS seasonal-adjustment pattern 1). The series is an official one a statute reads, built from a return whose coverage a filing rule changed.

**Swap:** "the bureau certifies the regions whose seasonally adjusted payroll jobs for the quarter are more than 1.0 per cent below the previous year's average". Put another field's nouns in (a clinic's appointment counts, a retailer's sales) and the object goes: there is no administrative return whose coverage a filing rule changed, no official seasonally adjusted series and no statute reading it, and the decisive step (pre-adjusting a documented coverage break before the seasonal pattern is estimated) is the official producer's practice for its own series.

**Layer 1:** what the revenue service's and the bureau's systems produce, none of it on the decisive step.
- The returns come in two layouts: a yearly file with a column per month to 2023, a long monthly file from 2024.
- Municipal codes changed with a 2025 amalgamation, joined to the regions through the bureau's concordance.
- The latest months are preliminary in the extract, and a later revision file replaces them.
- The industry codes were revised in 2024, leaving the totals unchanged.
- The quarterly remitters' move into the monthly returns from January 2026 is documented in the revenue service's release note.
- The labour force survey's regional rates and the population estimates sit beside the returns as distractors.

**Layer 2:** field_method. The seasonal pattern is estimated from a history that spans a documented change in what the source counts. The official producer removes the change as a level shift in the regARIMA pre-adjustment, or restates the earlier history to the new coverage, before the seasonal filters run.

**Decisive step:** removing the January 2026 coverage step from each region's history before its seasonal pattern is estimated, although both periods the trigger compares lie after the step. A default adjustment estimates the pattern across the step, its trend unable to jump, and the step leaks into the first-quarter factors in proportion to its size.

**Not semantics:** every field, code and unit read right (the release note's coverage change and its date, the layouts, the concordance, the preliminary and revised months) still leaves the seasonal pattern to be estimated. The default path reads the coverage note correctly, concludes rightly that both compared periods are on the new coverage, and still designates four regions.

**Not rule application:** the regulation files the WHAT (the quarter's seasonally adjusted jobs against the previous year's average, the 1.0 per cent line, the regions by municipality) and no method. No filed sentence says how to seasonally adjust or that a coverage change must be pre-adjusted, so executing every filed rule with a standard adjustment still designates four regions.

**Analyst test:** a strong analyst who conforms the returns, reads the January 2026 coverage note correctly and seasonally adjusts each region's whole series with STL or the classical moving-average method designates Brennick Valley, Kestrow North, Oslin Shore and Pellmarsh Hills (the default path's `Ends on:`), against Brennick Valley and Pellmarsh Hills.

**Estimand:** the Regional Rapid Response Program Regulation. A region qualifies for a quarter when its seasonally adjusted payroll jobs for the quarter (the average of its three months) are more than 1.0 per cent below its average payroll jobs for the previous calendar year (the average of the year's twelve months). Payroll jobs are the jobs on the revenue service's monthly employer returns at establishments in the region's municipalities.

**No decoy:** nothing is planted to be caught. The coverage change is an administrative event the revenue service documents in its release note. No published seasonally adjusted series, earlier certification, memo or preliminary figure states a region's adjusted jobs or verdict.

**No certified replay:** no shipped figure is reproduced to recover a method; no seasonal factors or adjusted series ship.

**Lesson:** a seasonal pattern estimated from a history that spans a documented change in what a source counts carries the change into the seasonal factors, even when every period compared lies after it, so the change is removed as a level shift before the pattern is estimated. No build on file teaches it (the nearest driver, task30 round 3 at 0.08, segmented a corpus to the post-change cohort, which here is a wrong rung).

## Tried and rejected

- 2026-10-13, draw: seed ET10's world (a patient-advocacy report card on trial results reporting). Rejected: its natural client domains (biomedical and clinical research, pharmacology) have no task type serving ETL, and the deciding rate is a deadline count under stated rules, a backdrop the 10/10 rules ban.
- 2026-10-13, draw: the quarter-on-quarter change in seasonally adjusted jobs (the fourth quarter of 2026 to the first of 2027) as the trigger. Rejected: at the end of a series the step-aware methods themselves disagree by up to a point on a quarter's change, too much for a determinate line; the trigger compares the quarter with the previous calendar year's average, which needs no adjustment.
- 2026-10-13, draw: growth from a base year before the change (2025) to the latest four quarters. Rejected: the change then enters the level directly, so every careful analyst links the series first, and the linking ladder (a December to January ratio, a year-on-year ratio, a regression) repeats task450's link-across-a-change structure.
- 2026-10-13, draw: the card's first signature (population, G16, method_or_model_selection). Rejected by the guard as a spent driver (task501 v4, task104, task134 v1, task70 v2); the decisive move is conformance of the series to one coverage basis, filed as etl_conformance.
- 2026-10-13, draw: a regional irregular of 0.25 per cent in the simulation. Rejected: robust STL then down-weights the months around the step so completely that it lands the golden in 19 of 20 seeds; at the 0.6 to 1.0 per cent irregular regional payroll series carry, it misses.
