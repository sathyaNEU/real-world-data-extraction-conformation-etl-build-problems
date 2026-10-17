# task466 design note: Quillfield's 2027 emergency interconnect reservation

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: four architectures
were weighed for this seed and dropped before the card was registered, and two calibrations died at stage 3.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task466.json` (architecture v1), registered 2026-10-17. At stage 3 the
  guard's heart check, run with task265 and task157 in the corpus (both registered about forty minutes before this card
  and pulled with its DRAWN commit), blocked five card axes; the card was redrawn on them and the design did not move:
  decisive generator G17 (the likelihood fitted to the record's real observation structure) with G12 as its frame, role
  capacity_planner, context artifact register, strategy other (censored observation, named in the card's notes) and
  forcing event vote_or_meeting; a differentiation line against task449 was added. Heart is WARN only. Answered: Gate G
  method_or_model_selection repeats task265 and stands in 6 of the last 12 builds; it is the honest mechanism (two ways
  of fitting one filed distribution to one filed record, the data's structure deciding between them), and the batch
  varies elsewhere (gap population, a dial setting, shape 13, a censored-observation strategy, a town council). The
  question form how-much repeats task157 and follows the decision, a block size. Differentiated against task255 v1 (an
  upper tail truncated below a reporting floor: items under the floor never reach the record; here every year reaches
  the record, the earlier ones censored at one level), task456 (a latent class from three imperfect records), task462
  (snapshot surveys with a detection probability rising with size; here nothing goes undetected) and task449 (a share
  read through a link right one time in k; here no record is linked and no value is wrong).
- **Seed:** ET23 (a water utility's drought-restriction trigger and an emergency interconnect sized by replaying it over
  history). Kept: the world (a small water utility on a river under a withdrawal permit), the decision (how much
  emergency interconnect to contract) and the quantity (a 7-day low flow and its recurrence). Dropped: the seed's
  mechanism rows (calendar against climatic year, provisional data), which are data semantics and Layer 1; both survive
  here only as Layer 1 texture, each asserted neutral.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL, own pattern
  "historical threshold information entered as censored years in a low-flow frequency fit". Two records of one river,
  kept by two bodies under two observation mechanisms, are conformed into one annual low-flow record and one likelihood:
  the State Hydrologic Survey's gauge measures each year's 7-day low flow since 1951; the town's water-works reports
  since 1894 measured the river only in the seasons the works had to stop pumping. The client's GSDS rule makes the
  swap one of method: the deciding quantity is the fitted 50-year low flow, and replacing the censored likelihood with a
  fit to the values on file changes the reservation. GSDS x ETL last ran at task465 (statistical matching), eight builds
  back in draw order; the surface screen promotes the pair as consecutive numbers, a card-level note for the author.
- **Shape:** 13, scenarios and the flip point: the 10-, 25-, 50- and 100-year 7-day low flows at the intake, each with
  the withdrawal the permit allows and the Stage 2 shortfall, the 50-year one deciding the block, and the recurrence
  interval at which the recommended block stops covering; the conformed record and the asks add the rest.
- **Strategy:** censored observation (`other` on the card). The decisive step is how the silent years enter the fit:
  each is a year the river stayed above the suspension flow, and leaving them out (a year with no number looks like a
  year with no data) fits the dry seasons as if they were the river's whole early record. Gap population with G17 (a
  likelihood fitted to the record's real observation structure), framed by G12 (absence of record against record of
  absence) and G16 (method selection); Gate G method_or_model_selection.
- **World:** an unnamed New England state of the United States. The Town of Quillfield draws its water from the Varrow
  River at the old Ansel and Hale mill dam (drainage area 41.6 square miles). From 1893 the town's water works pumped at
  the dam under an agreement with the woollen mill: pumping stopped whenever the river's flow over the dam, averaged
  over any seven consecutive days, fell below two million gallons a day, and in those seasons the works' superintendent
  gauged the flow over the spillway and reported the season's lowest seven-day flow in the town's annual report. The
  mill closed in 1950 and the State Hydrologic Survey began recording at the dam in April 1951. The State Water
  Resources Board's low-flow guidance sets a small system's design drought flow as the 7-day low flow with a 50-year
  recurrence interval at its intake, from a log-Pearson Type III with the state's regional skew fitted by maximum
  likelihood to the river's record. After dry late summers from 2022 to 2025 the town's drought management plan
  requires firm emergency capacity covering the Stage 2 demand (0.91 MGD for 2027) less what the withdrawal permit
  allows at the design drought flow (the flow above a 0.50 cubic feet per second passby). The City of Castlewick offers
  firm interconnect capacity for 2027 to 2031 in blocks of 0.1 million gallons a day.
- **Forcing fact:** the Quillfield Select Board votes on the Castlewick interconnect agreement at its December 2026
  meeting (Castlewick needs the blocks named by 31 December) for service from 1 January 2027; the call faces forward,
  the capacity reserved for 2027. As-of: 16 October 2026, the morning the Survey's daily values were retrieved, the day
  the folder was assembled and the superintendent's memo is dated.
- **Forum and forcing event:** council_or_assembly (the select board), vote_or_meeting (its December vote). Organisation
  local_government; role capacity_planner (the superintendent plans the town's supply capacity). Personas from
  `guard.py names --geo "United States" --seed 466`: Jaime Galloway (Quillfield's water superintendent, who brings the
  reservation to the board), Phyllis Mitchell (the Quillfield Historical Society's archivist, who transcribed the
  water-works reports) and Darryl Powell (Castlewick's utilities director, who signs the offer).
- **Data-native sentence:** the water works measured the river only in the seasons the mill agreement made it stop
  pumping, so its reports hold a seven-day flow for every dry year and only "no stoppage" for the rest; each of those
  years is a censored observation (its seven-day low flow stayed above two million gallons a day, 3.0944 cubic feet per
  second), not a missing one, and a fit that leaves them out is a fit to the record's droughts.
- **The WHAT screen.** The estimand's five parts are filed: the population (every climatic year of the river's record:
  the gauge's complete approved years and the earlier years as the town's reports record them), the outcome (the year's
  7-day low flow at the intake), the window (1894 to 2024), the unit (cubic feet per second; the shortfall in million
  gallons a day, the reservation in 0.1 MGD blocks) and the comparison (the 50-year recurrence interval, the Stage 2
  demand less the permitted withdrawal). The distribution, its skew and the estimation method are the guidance's
  general method. The decisive step settles none of them: it is how a report year without a measured flow enters a
  maximum-likelihood fit, and the reports' own rule (the works stopped whenever the seven-day flow fell below two
  million gallons a day) makes each silent year a bound, not a blank.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution: the listed
    pattern propagates linkage error into an estimate; this build integrates two records of one quantity whose
    observation mechanisms differ, which the listed pattern does not cover.
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data (censoring and truncation):
    the client's own example of the data's real structure; here the censoring is in the earlier record's silent years.
  - The field's own practice: flood-frequency analysis enters historical information through a perception threshold
    (every historical year either above or below it, a censored observation, fitted by the expected moments algorithm or
    maximum likelihood); this build carries that logic to a low-flow record kept by a water works, and files neither the
    threshold logic nor the word censoring, only the estimand and the general method.
  - `dataset-generation/references/layer1-messiness.md`: an agency's tab-delimited daily export with comment lines and
    qualifier codes, approved and provisional values overlapping, climatic against water and calendar years, a
    transcribed report table with changing units and missing years; none on the decisive step, each asserted neutral.

## Default path

1. Read the State Water Resources Board's guidance: the design drought flow is the 7-day low flow at the intake with a
   50-year recurrence interval, from a log-Pearson Type III with the regional skew of -0.30 fitted by maximum likelihood
   to the gauge's complete climatic years of approved record and to the river's earlier records kept at the site.
2. Read the drought management plan: reserve the smallest 0.1 MGD block covering the 2027 Stage 2 demand (0.91 MGD)
   less the withdrawal the permit allows at the design drought flow (the flow above the 0.50 cfs passby).
3. Build the climatic-year (April to March) 7-day minima from the gauge's approved daily values, 1951 to 2024
   (74 years), leaving out the provisional months after September 2025.
4. Read the reports, 1894 to 1950: convert the measured lowest seven-day flows to cubic feet per second (gallons a day
   before 1921, second-feet after) and take the 14 seasons the pumps stopped; the 40 report years without a stoppage
   carry no flow and are left out, as are the three missing reports.
5. Fit the regional-skew log-Pearson Type III by maximum likelihood to the 88 annual low flows: the 50-year 7-day low
   flow is 1.31 cfs.
6. The permit allows (1.31 - 0.50) x 0.6463 = 0.53 MGD; the shortfall is 0.91 - 0.53 = 0.38 MGD; reserve 0.4 MGD.

Ends on: a 0.4 MGD reservation (a 50-year 7-day low flow of 1.31 cfs, a 0.38 MGD shortfall)

Golden: a 0.3 MGD reservation (a 50-year 7-day low flow of 1.55 cfs, a 0.23 MGD shortfall)

## Stump sentence

The default path fits the design drought to the gauge's 74 annual minima and the 14 report years with a measured flow,
leaving out the 40 report years without a stoppage because they carry no flow, so it fits the river's early record as
if it were all drought and lands on a 50-year 7-day low flow of 1.31 cfs and a 0.4 MGD reservation (a 0.38 MGD
shortfall), where the same fit with each silent year entered as a 7-day low flow above the 3.09 cfs suspension flow
gives 1.55 cfs and reserves 0.3 MGD.

## Three rules

Task type: data-integration-record-linkage-entity-resolution: two records of one river kept under different observation mechanisms (the gauge's measured annual minima since 1951 and the water-works reports since 1894, which measured the river only in the seasons pumping stopped) conformed into one annual low-flow record and one likelihood, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is the river's 50-year 7-day low flow at the intake from a log-Pearson Type III fitted by maximum likelihood to every year of both records; data integration across sources whose observation mechanisms differ enters each report year as what its source can say (a measured flow, or a flow above the suspension flow), and replacing that likelihood with a fit to the values on file, a generic union of the two files, moves the reservation from 0.3 to 0.4 MGD.

Swap: "the warehouse's 50-year lowest week of stock from its scanner record and the old clerk's ledger, which noted the stock only in the weeks it ran out" keeps the shape and loses the move only if nothing ties the ledger's silence to a level; here the 1893 agreement ties every silent season to a seven-day flow above two million gallons a day, and the design statistic, the recurrence interval and the permit's passby are the river's own.

Layer 1: the State Hydrologic Survey's tab-delimited daily export (comment lines, a field-width row, qualifier codes for approved, estimated and provisional values), provisional months after September 2025 overlapping the approved record, ice-estimated winter days, the climatic year (April to March) against the agency's water year and the town's calendar-year reports, the reports transcribed by the historical society into a PDF table with flows in gallons a day before 1921 and second-feet after, seasons stopped twice, and three reports missing, demand in million gallons a day against river flow in cubic feet per second; each asserted neutral (checks.py R2).

Layer 2: estimation that fits the data (censoring): the call flips on entering the report years without a stoppage as censored observations above the suspension flow instead of leaving them out of the fit.

Decisive step: fitting the regional-skew log-Pearson Type III by maximum likelihood to the gauge's annual minima, the measured suspension seasons and the silent report years as seven-day low flows above 3.0944 cfs, which places the 50-year low flow at 1.55 cfs and the reservation at 0.3 MGD; the fit to the values on file alone places it at 1.31 cfs and 0.4 MGD.

Not semantics: every field, code, unit and definition read correctly (two million gallons a day as 3.0944 cfs over any seven consecutive days, "no stoppage" as a season the flow stayed above it, the climatic year, the approved months, gallons a day and second-feet) still leaves the easy route fitting the years that carry a flow, because a year with no number looks like a year with no data; the step is how that year enters the likelihood, not what it means.

Not rule application: the guidance files the distribution, the skew, the estimation method and the records to use, and no rule or procedure says how a year without a measured flow enters the likelihood; executing every filed rule with the measured years alone files 0.4 MGD, so the step no rule performs is the censored likelihood.

Analyst test: a strong analyst who converts the units, builds the climatic-year minima from the approved daily values and adds the 14 report years with a measured flow fits the regional-skew log-Pearson Type III by maximum likelihood, gets a 50-year 7-day low flow of 1.31 cfs and reserves 0.4 MGD (the default path's Ends on).

Estimand: the State Water Resources Board's low-flow guidance (the design drought flow: the 7-day low flow at the intake with a 50-year recurrence interval, from a log-Pearson Type III with the regional skew of -0.30 fitted by maximum likelihood to the gauge's complete climatic years of approved record and to the river's earlier records kept at the site) and the drought management plan (the smallest 0.1 MGD block covering the Stage 2 demand less the withdrawal the permit allows at that flow).

No decoy: nothing is planted to be caught; the reports are the water works' annual reports as written, the station description and guidance describe their subjects, no memo, draft or briefing argues a method or a figure, and no document computes a design flow or a reservation.

No certified replay: no certified or published frequency statistic for the river ships; the guidance gives the regional skew only, the station description no statistics, and the regional regression report lists no value for the Varrow, so no figure reproduces a method.

Lesson: a record that measured only the bad years still says something about every year it is silent on, and a likelihood that drops the silent years fits the extremes as if they were typical; no build on file teaches censored historical information in a frequency fit (task255 v1 is truncation below a floor, task462 detection that rises with size).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the gauge's 74 approved annual minima alone (1.87 cfs; 0.1 MGD) | the guidance names the site's earlier records among the records, so the rung breaks a filed sentence | the daily-values file alone carries flows | yes: fit the series on file | no | no | one fit | readable |
| R1 the gauge and the 14 report years with a measured flow, the 40 silent years dropped (1.31 cfs; 0.4 MGD; the default path) | the guidance's records read as the years that carry a flow | the reports' flow cell is blank in a silent year | yes: drop the rows without a value | no | yes: the null filter | one fit | readable |
| R1b the silent years entered at the suspension flow, 3.09 cfs (1.23 cfs; 0.5 MGD) | none | the agreement gives the level | yes: impute the bound as a value | no | no | one fit | readable |
| R1c the measured years entered as below 3.09 cfs, the silent years dropped (1.30 cfs; 0.4 MGD) | none | none | partly: censor the known lows | no | no | one fit | readable |
| R2 every report year as its source records it: the measured flow, or a 7-day low flow above 3.0944 cfs (1.55 cfs; 0.3 MGD; decisive) | no: the guidance files the records, the distribution, the skew and maximum likelihood; the reports' introduction files the agreement and the superintendent's practice; no sentence names censoring, a bound, a survival term or the silent years | no column holds a bound or a censoring flag; a silent year's flow cell is blank like a missing report's | no: the reflex on a blank cell is to drop it | no: no control scores the fits | no: the battery's null filter files R1 | no: a likelihood term for each of 40 years | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the 50-year 7-day low flow | the flow a climatic year's lowest 7-day mean falls below with a probability of 1 in 50 (the 0.02 quantile of the fitted annual minima) | the daily flow exceeded on 98 per cent of days | a different call (no block) | the guidance's definition of the design drought flow |
| SF2 | climatic year | 1 April to 31 March, named by the year it begins | the water year (October to September); the calendar year | same call (asserted: 1.54 cfs under each, 0.3 MGD; every gauged year's lowest window ends in August or September) | the guidance |
| SF3 | complete climatic years of approved record | 1951 to 2024 | climatic year 2025 added (its low season approved, its winter provisional) | same call (asserted, 1.54 cfs) | the guidance; the station description's approval date |
| SF4 | the 7-day mean | the mean of seven consecutive daily means, the year's minimum over the windows ending in it | windows kept inside the year; centred windows | same call (asserted: no year's lowest window ends in the first week of April) | the guidance |
| SF5 | the reports' units | gallons a day to 1920, second-feet (cubic feet per second) from 1921 | second-feet read as million gallons a day | a different call (0.2 MGD) | the transcription's unit note |
| SF6 | the suspension flow | two million gallons a day averaged over any seven consecutive days, 3.0944 cubic feet per second | a single day below it; the level rounded to 3.09 or 3.094 cfs | same call (asserted: every measured season's flow lies below 3.0944 cfs, the highest 3.09; each level gives the same figures; a silent year's seven-day low stays above the level under either reading) | the 1893 agreement as the transcription quotes it |
| SF7 | the missing reports (1909, 1918, 1944) | left out: no record | entered as years without a stoppage | same call (asserted, 1.56 cfs, 0.3 MGD) | the transcription ("have not been found") |
| SF8 | the regional skew | -0.30 for the logarithms of the annual minima, base 10 or natural alike | the station skew (-0.26 for the gauge, -0.27 with the measured years) | same call (asserted) | the guidance |
| SF9 | maximum likelihood | the mean and standard deviation of the logarithms that maximise the likelihood of every record year with the skew held at -0.30 | the expected moments algorithm (each silent year's expectation above 3.0944 cfs) | same call (asserted, 1.53 cfs) | the guidance names maximum likelihood |
| SF10 | the withdrawal the permit allows | the flow above the 0.50 cfs passby, at 0.6463 MGD per cfs | the whole flow | a different call (no block) | the permit's passby condition |
| SF11 | the Stage 2 demand | 0.91 MGD, the plan's 2027 figure | the plan's 2026 figure, 0.89 MGD | same call (asserted) | the plan's table, 2027 row |
| SF12 | the block | the smallest multiple of 0.1 MGD at or above the shortfall | the nearest multiple | a different call (0.2 MGD) | the plan ("the smallest block offered that covers") |
| SF13 | the recurrence interval at which the block stops covering | the interval whose 7-day low flow leaves a shortfall of the block itself | none open | same figure | the prompt |
| SF14 | each Stage 2 period the board declared (the ask) | the periods in the board's notices, from the date in effect through the date rescinded | the days the permit's trigger was met on the gauge | different figures (asserted on all eight periods) | the prompt ("the select board has declared") |
| SF15 | water supplied to the town's own distribution system (the ask) | the plant's finished water less the Elm Hollow master meter, plus the Hollow Road wells | the plant's finished water; the plant alone | different figures (the ask's device) | the meter register (the master meter on the plant's high-service header); the plan's supply section |
| SF16 | approved record | every day coded A, estimated (A:e) or not | only the days coded A without the estimate code, every climatic year with an ice-estimated winter day dropped (43 gauged years left) | same call (asserted, 1.46 cfs) | the export's qualifier note ("e value estimated (combined with A or P, e.g. A:e)") |

## Ladder

| Rung | Construction | 50-year 7-day low flow (cfs) | Shortfall (MGD) | Block (MGD) |
|---|---|---|---|---|
| R0 | the gauge's minima alone | 1.87 | 0.02 | 0.1 |
| R1 | the gauge and the 14 measured report years (the default path) | 1.31 | 0.38 | 0.4 |
| R1b | the silent years entered at 3.09 cfs | 1.23 | 0.44 | 0.5 |
| R1c | the measured years entered as below 3.09 cfs, the silent years dropped | 1.30 | 0.39 | 0.4 |
| R1d | every report year censored, the measured values set aside | 1.58 | 0.21 | 0.3 |
| R2 | every report year as recorded: measured, or above 3.0944 cfs (golden) | 1.55 | 0.23 | 0.3 |

- **Margins:** the golden's 0.232 MGD shortfall sits 0.032 above the 0.2 edge and 0.068 below the 0.3 edge; the 50-year
  flow would have to rise above 1.599 cfs or fall below 1.444 cfs to move the block. The default path's 0.384 sits in
  the 0.4 block, 0.152 above the golden; the golden 50-year flow is 18 per cent above the default path's.
- **Position and dominance:** R0 to R1 overshoots (the measured years are the record's driest), R2 reverses part of it
  (the 40 silent years each say the season stayed above 3.0944 cfs); the golden is bracketed by R0 and R1. The moments
  of the values on file (R1m, 1.30 cfs) land with the default path.
- **Grid:** two choices, the treatment of the report years (dropped, at the level, below the level, censored both
  ways, measured and censored) and the Layer 1 handling (climatic, water or calendar year, 2025 in or out, missing
  reports in or out, ice-estimated years in or out): every R1 cell files 0.4, every R1b cell 0.5, every R0 cell 0.1,
  every R2 cell 0.3 (asserted for each Layer 1 cell on R2).
- **Worth:** the decisive rung moves the 50-year flow by 0.24 cfs and the block by 0.1 MGD; R1d lands the block with
  the 50-year flow wrong (1.58 cfs) and every scenario figure off.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every climatic year 1894 to 2024 the gauge's approved record or a report covers | the guidance; SF3, SF7, SF16 |
| 2 | Unit of account | the climatic year | the guidance; SF2 |
| 3 | Attribution window | the climatic year a low season falls in | C1: every low season lies in August and September (asserted); SF2 |
| 4 | As-of dating | the gauge approved through 30 September 2025, exported 15 October 2026 | the station description; SF3 |
| 5 | Version basis | approved values, provisional months out | the guidance; SF3 |
| 6 | Denominator | every record year in the likelihood | the guidance's records; the decisive step is how a year enters, not whether |
| 7 | Weighting | each year once in the likelihood | the guidance (maximum likelihood) |
| 8 | Window length | 1894 to 2024 | the guidance |
| 9 | Boundary inclusivity | below two million gallons a day stops the pumps | C1: every measured flow below 3.0944 cfs and the level's rounding moves no figure (asserted); SF6 |
| 10 | Rounding path | the flow and the shortfall unrounded, the block from the unrounded shortfall, figures shown to two decimals | the plan; the prompt; mid-bin asserted |
| 11 | Tie-break | none needed | n/a |
| 12 | Maturity and censoring | climatic year 2025 open (provisional winter); the silent years censored by their source | SF3; the decisive step |
| 13 | Order of operations | units, climatic-year minima, fit, quantile, withdrawal, shortfall, block | C1: the minima are order-free; SF12 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | one value a day in the export, one report a year (a season stopped twice carries one flow) | C1 (asserted) |
| 16 | Identity normalisation | one gauge at the dam; the reports' flow over the dam is the same site | the station description |
| 17 | Netting against gross | the gauge above the intake measures the river before the town's withdrawal; a stopped season's flow over the dam had no pumping in it | the station description; the transcription |
| 18 | Dimensional units | gallons a day, second-feet, cubic feet per second, million gallons a day | SF5, SF10; R2 units asserted |
| 19 | Code and status semantics | the export's qualifiers (approved, estimated, provisional); the reports' statuses (stopped, no stoppage, report not found) | SF3, SF7, SF16 |
| 20 | Integerisation | the block a multiple of 0.1 MGD | SF12 |
| 21 | Clause scope | the 50-year flow for the block; the 10-, 25- and 100-year flows as scenarios | the plan; the prompt |
| 22 | Forward window contents | 2027: the plan's Stage 2 demand and Castlewick's blocks | the plan; the offer |

## Literal reader

Executed word for word, the guidance fits a log-Pearson Type III with the regional skew of -0.30 by maximum likelihood
to every climatic year of the river's record (the gauge's complete approved years 1951 to 2024 and the earlier years
as the town's reports record them), takes the flow with a 1 in 50 chance of being undercut, and the plan reserves the
smallest 0.1 MGD block covering 0.91 MGD less the flow above the 0.50 cfs passby. The reports record each year as a
season's measured lowest seven-day flow or as no stoppage, which under the agreement quoted in the transcription means
the seven-day flow never fell below two million gallons a day; under maximum likelihood such a year contributes the
probability of a 7-day low flow above 3.0944 cfs. That fit gives 1.55 cfs and 0.3 MGD. The text is silent on the
missing reports, on climatic year 2025's approved months and on the year convention of a reader who reaches for water
years: each option computed (missing reports as silent years, 1.56 cfs; 2025 in, 1.54 cfs; water or calendar years,
1.54 cfs; ice-estimated years out, 1.46 cfs), the block 0.3 MGD under each. Dropping the silent years, the easy method
on the same literal estimand, gives 1.31 cfs and 0.4 MGD.

## Oracles

None ties only under the golden. No document reports a frequency statistic, a design flow or a fitted parameter for
the river; the guidance gives the regional skew only; the station description gives no statistics; the reports give
measured flows and statuses that every route reads alike. The ask's files carry no control that ties under one
handling of the wholesale water only. The two distractors (the state's regional regression report for ungauged sites,
which lists no value for the Varrow and says its equations are not used at gauged sites, and the town weather
station's monthly precipitation) confirm nothing.

## Ask sheet

- **Ask A, for each Stage 2 period the select board declared since 2012 (eight periods: 2016, two in 2020, 2022, 2023,
  2024 and two in 2025), the average and the highest daily water Quillfield supplied to its own distribution system
  (16 figures, million gallons a day to two decimals).** H18 home: the audit trail of the 2027 Stage 2 demand the call
  consumes (0.91 MGD), what the town's own system actually drew under each declared Stage 2. Path: the board's drought
  notices register, the plant's daily historian export (finished water and the Hollow Road wells' telemetered daily
  total), the Elm Hollow Water District master meter's daily reads, the Hollow Road operator's round sheets since the
  station's telemetry failed, the meter register and the data dictionary (six files). Primary device: D5, a population
  inflating every control equally: Elm Hollow's wholesale water leaves the plant's clearwell through the same
  high-service header, so the plant's finished-water total carries it on every day; its master meter on the header is
  the only record of it, and every period's average and highest day are high by it (0.075 to 0.09 MGD, asserted on all
  16 figures). Second device: D4, a reporter absent in stages: the Hollow Road station's telemetry failed on 14 June
  2023 and the historian has repeated its last daily total (0.09 MG) on every day since; the operator's daily
  totalizer readings are the record, so the eight figures after the failure move and none before (asserted). Texture:
  the historian's August 2020 restore re-sent three weeks of rows under new record numbers with identical totals
  (dropping them moves nothing; summing them moves two 2020 figures, asserted); the well log's readings in gallons, the
  master meter's in thousands of gallons; the log's morning readings close the day before, and either day convention
  gives the same 16 figures (asserted). Stops (asserted): the plant's finished water plus the telemetered wells (the
  cracker) misses all 16; the plant alone misses all 16; finished water less Elm Hollow with the telemetered wells is
  wrong on the eight figures after June 2023 and right before. Realism: a plant meters what leaves its clearwell, a
  wholesale customer's master meter sits on the plant's header, and a well station whose radio fails keeps reporting
  its last value until someone fixes it.
- **The construction layer:** the call, the 10-, 25-, 50- and 100-year flows with their withdrawals and shortfalls, the
  recurrence interval at which the block stops covering, the chart and the conformed file; the cracker has them.
- **Main population zero-counts (asserted):** the main call reads no notice, historian, master-meter, operator-log or
  meter-register row (the call and every rung computed with those files deleted are identical); the ask reads no
  gauge, report, guidance, permit, station, plan or offer row (the ask computed with those files deleted is identical).
- **Hazard table (asserted):** D5 moves all 16 figures; D4 moves the eight figures after June 2023; the restored rows
  move two 2020 figures for a response that sums them.
- **Referee:** none; no total in the ask's files ties under one handling only.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each declared Stage 2 period's average and highest daily water supplied to the town's own system | sums the plant's finished water and the telemetered wells over each period from the notices, duplicates removed; Elm Hollow's water kept, the stale well total kept | miss |

- Mirror leakage: 11.1 per cent of ask weight (a response on R1 keeps the two files and misses every Ask A figure on
  the same devices as the cracker).
- Pair ceiling: 34.6 (planning weights 38 / 7 / 55 with the call, the 50-year flow and shortfall, the three other
  scenarios, the recurrence interval, the chart and the conformed file in the main block and r = 5; the ask weight over
  18 criteria: Ask A 16, the two files 2; the cracker keeps the files, 38 + 7 + 6.1 = 51.1; the mirror keeps r,
  instruction-following and the files, 5 + 7 + 6.1 = 18.1; average 34.6), rerun from the generated rubric at ship.

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is the river's 50-year 7-day low flow
  at the intake, estimated the way a hydrologist fits a frequency distribution to a record that holds measured years
  and years known only against a level (each silent report year a bound in the likelihood); the fit to the values on
  file reserves 0.4 MGD, the silent years at the level 0.5 MGD, the gauge alone 0.1 MGD, the censored likelihood 0.3
  MGD. Two layers: the Layer 1 inventory in `## Three rules`, each item asserted neutral on the call (checks.py R2 and
  SF2, SF3, SF6, SF7, SF16); the ask's two devices confined to the town's operating files (the separation checks);
  Layer 2 the censored likelihood. The decisive step is none of the three banned kinds, each executed in `checks.py`:
  not a plant (R3c: no document names censoring, a threshold, a bound, a survival term or historical information; no
  copied or held block in the river's record; no repeated record in any file); not data semantics (SF1 to SF16: every
  field read right still leaves the fit to the values on file at 0.4 MGD); not rule application (R3a: every filed rule
  executed with the years that carry a flow reserves 0.4 MGD on the clean truth; R3b: only the censored likelihood
  reserves the golden 0.3 MGD, each lower rung's single correction staying wrong).
- **Gates.** 16 files in 4 formats (csv, pdf, txt, xlsx); varrow_river_at_quillfield_daily_values.txt at 27,592 rows;
  two distractors (the Board's regional regression report and the town weather station's precipitation) the solution
  never reads, each deletion asserted; 79 generator checks; `verify.py` from the bundle alone (pandas and pdftotext,
  its own gamma-function likelihood, every filed constant read from the PDFs); two builds byte-identical;
  `figures_check.py` (90 figures), `precut.py` (49) and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK); guard
  heart WARN (answered in the draw); the containers clean (H1 audit, pack and goldens). The surface screen promotes
  three card-level pairs for the author's read, none on the pack's surface: task465 (the same pairing, consecutive
  numbers), task449 (the same gap, G17 and dial setting, differentiated on the card) and task50 (surface similarity
  only). The data dictionary's columns were renamed after the screen matched them to task460's, and three gauge places
  in the regression report after the screen read them as people.

## Leak check

`leak.py --asof 2026-10-16`: REVIEW, no LEAK. Each REVIEW line answered:
- The offer's block size (0.1 MGD) and its words (firm capacity, blocks, interconnect, 2027): the offer's own terms, a
  filed input; it names no reservation. Harmless.
- The plan's demand table (0.86, 0.87, 0.91, 0.93): the department's projection; 0.91 is the filed 2027 Stage 2
  demand the call consumes, and the other values coincide with Stage 2 figures of the ask only by range (every ask
  figure lies between 0.78 and 0.93). Harmless.
- Four daily discharge values in the gauge export equal golden figures (1.87, 1.89, 2.54, 131): single days of the raw
  record, never a 7-day statistic. Harmless.
- "Select Board" beside decision words in the plan and the offer: the forum's name. Harmless.
- The plan, the reports, the guidance and the station description carry three to seven stump-paragraph terms
  (guidance, agreement, records, season, stopped, approved, likelihood): each describes its own subject; the reports
  describe the agreement and what the superintendent measured, the evidence the decisive step reads, and none names
  censoring, a bound or how a silent year enters a fit. Harmless.

Reader, round 1 (answers in `leak_check_report.md`): nothing quoted for question 1 (the nearest, WR-14 section 3 and
the transcription's account of what the reports measured, file the records and the observation mechanism, not how a
silent year enters the fit); no ranking or computing file; no helping file; nothing reads as the answer; its literal
execution of WR-14 section 3 put the gauge's climatic years 1951 to 2024 and the report years 1894 to 1950 into the
fit, the measured years as values, the silent years as 7-day low flows at or above 3.09 cfs, the missing reports out:
the golden reading; question 6 an analytical choice (the method for the silent years is left to the solver). Its
realism tells were fixed in the generator, nothing graded moving (figures.json and submission.md byte-identical): two
declarations quoted a real-time reading at or above the level they cite (each now quotes the provisional 7-day mean
below the level, asserted), the notices' wording varied as a clerk's would be, the reports' notes on seasons stopped
twice no longer one repeated phrase, the export retrieved the morning after its last daily value (and the town's
exports dated the same way), the folder assembled that day (16 October) rather than in November, the dictionary's
qualifier definition naming A:e. Left as they are: the notices register named for 2012 to 2026 with its first notice
in 2014 (no stage was declared in 2012 or 2013), the transcribed flows to the nearest 10,000 gallons (as printed).

Judge, pass 1 (`determinism_check_report.md`): DETERMINISTIC, FIX_NOW on two metadata items, no graded figure among
them: the dictionary and the contents list dated after the data (the folder now assembled on 16 October, the as-of),
and the meter register putting the Hollow Road totalizer in service in 2014 while the historian carries its tag from
2012 (now in service 8 June 2010, the operator log's first reading the volume pumped since, asserted). Every figure
reproduced (the four scenario flows, withdrawals and shortfalls, the block, 64.78 years for the flip, all eight Stage
2 periods); the gauge alone (0.1), the silent years dropped (0.4) and the silent years at 3.09 cfs (0.5) refuted;
Gate G statistical_rigor, analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain pass,
layers pass, decisive step analytical. Its residual-risk note (WR-14 never says "censored", so a literal solver might
drop the silent years) is the stump: the transcription's quoted agreement ties every silent year to a flow above the
level, and the judge itself declined dropping them as a defensible reading.

Reader, round 2 (after the fix pass): nothing quoted for question 1 (the plan's reservation rule and WR-14's
distribution, skew and maximum likelihood named as the filed method); no ranking, helping or answer-shaped file; its
literal reading the golden (the "No stoppage" years at or above the 2 MGD level); question 6 an analytical choice,
nothing planted. Its one fixable tell, the operator log's single repeated note, was fixed in the generator (a
data-only change, `leak.py` re-run, REVIEW with the same lines); the notices' readings just under each level, the
plant's steady winter output and the plan's even projection steps left as they are.

Judge, pass 2 (`determinism_check_report_pass2.md`): DETERMINISTIC, APPROVE. Every figure reproduced again (64.84
years for the flip; the block holding for any 50-year flow from 1.444 to 1.599 cfs, the golden at 1.549); the three
easy readings each break a literal clause of WR-14 or the agreement; crediting the totalizer to another day moves no
figure. Gate G method_or_model_selection (censored-data frequency analysis), analytical_non_defect; Gate H domain pass,
layers pass, decisive step analytical. Its residual note, climatic year 2025 (taken in, the flip would read 63 years),
is closed by WR-14's "complete climatic years of the approved record" and the station description's approval date;
its two optional notes were taken without moving a figure: step 1 of the write-up says climatic year 2025 is left out
as provisional, and the memo's chart note names the Weibull plotting positions.

## Tried and rejected

- Candidate A, a record whose early years are single morning observer readings harmonised to daily means through the
  diurnal low-flow cycle the 15-minute record shows: dropped before registration, because a value column that is "not
  what it looks like" sits too close to the client's own data-semantics example (a rainfall column of multi-day totals)
  and the time-of-day reading reads as a clock item (Layer 1).
- Gap filling of a drought-season outage by baseflow recession: dropped, because a coverage gap is Layer 1 by the
  client's list and filling it would carry the stump in the mess.
- A smart-meter panel (non-probability) calibrated to a random-sample survey to size the Stage 2 response: dropped,
  because the plant's daily production already observes the system total the decision needs, and a utility-plus-survey
  integration two builds after task465 reads as a template.
- Current-conditions (naturalised) flows, the record adjusted for upstream withdrawals since 1951: dropped, because the
  estimand would have to name today's withdrawals, leaving accounting, not analysis, and the decisive method would be
  hydrologic, not the task type's.
- Record extension from a long index gauge to the intake: spent by task461 (a low quantile carried by the overlap's
  proportional relation) and task464 (regression shrinkage).
- A low season reaching into October (the river's lowest weeks in September and October): read by water years, the gauge
  record lost a dry season into its neighbour's year and moved the reservation to 0.2 MGD, so a Layer 1 convention
  decided the call; the seasonal curve now puts every year's lowest week in August or September, and the climatic,
  water and calendar years each reserve 0.3 MGD (SF2, R2).
- A 2027 Stage 2 demand of 0.89 MGD with the declared periods' average days near 0.94: the record the asks audit drew
  more than the plan assumed; the operating model's Stage 2 restriction now cuts outdoor use to 30 per cent, every
  declared period's average day sits between 0.78 and 0.87 MGD and the plan's 2027 figure is 0.91 MGD.
