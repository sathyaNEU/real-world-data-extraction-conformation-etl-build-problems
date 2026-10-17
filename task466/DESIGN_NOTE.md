# task466 design note: Quillfield's 2027 emergency interconnect reservation

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: four architectures
were weighed for this seed and dropped before the card was registered.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task466.json` (architecture v1), registered 2026-10-17, guard WARN only.
  Answered: Gate G method_or_model_selection repeats task464 and stands in 6 of the last 12 builds; it is the honest
  mechanism (two ways of fitting one filed distribution to one filed record, the data's structure deciding between
  them), and the batch varies elsewhere (gap population with G12, a dial setting, shape 13, strategy
  population_selection, a town council). Differentiated against task255 v1 (an upper tail truncated below a reporting
  floor: items under the floor never reach the record; here every year reaches the record, the earlier ones censored at
  one level), task456 (a latent class from three imperfect records) and task462 (snapshot surveys with a detection
  probability rising with size; here nothing goes undetected).
- **Seed:** ET23 (a water utility's drought-restriction trigger and an emergency interconnect sized by replaying it over
  history). Kept: the world (a small water utility on a river under a withdrawal permit), the decision (how much
  emergency interconnect to contract) and the quantity (a 7-day low flow and its recurrence). Dropped: the seed's
  mechanism rows (calendar against climatic year, provisional data), which are data semantics and Layer 1; both survive
  here only as Layer 1 texture and ask devices.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL, own pattern
  "historical threshold information entered as censored years in a low-flow frequency fit". Two records of one river,
  kept by two bodies under two observation mechanisms, are conformed into one annual low-flow record and one likelihood:
  the State Hydrologic Survey's gauge measures each year's 7-day low flow since 1951; the town's water-works reports
  since 1894 measured the river only in the seasons the works had to stop pumping. The client's GSDS rule makes the
  swap one of method: the deciding quantity is the fitted 50-year low flow, and replacing the censored likelihood with a
  fit to the values on file changes the reservation. GSDS x ETL last ran at task465 (statistical matching), seven builds
  back.
- **Shape:** 13, scenarios and the flip point: the 10-, 25-, 50- and 100-year 7-day low flows at the intake, each with
  the withdrawal the permit allows and the Stage 2 shortfall, the 50-year one deciding the block, and the recurrence
  interval at which the recommended block stops covering; the conformed record and the asks add the rest.
- **Strategy:** population_selection. The decisive step is the denominator of the fit: the report years without a
  suspension are years the river stayed above the suspension flow, and leaving them out (a year with no number looks
  like a year with no data) fits the dry seasons as if they were the river's whole early record. Gap population with
  G12 (absence of record against record of absence) and G16 (method selection); Gate G method_or_model_selection.
- **World:** an unnamed New England state of the United States. The Town of Quillfield draws its water from the Varrow
  River at the old Ansel and Hale mill dam (drainage area 41.6 square miles). From 1893 the town's water works pumped at
  the dam under an agreement with the woollen mill: pumping stopped whenever the river's flow over the dam, averaged
  over any seven consecutive days, fell below two million gallons a day, and in those seasons the works' engineer
  gauged the flow over the spillway and reported the season's lowest seven-day flow in the town's annual report. The
  mill closed in 1950 and the State Hydrologic Survey opened a continuous gauge at the dam in October 1950. The State
  Water Resources Board's low-flow guidance sets a small system's design drought flow as the 7-day low flow with a
  50-year recurrence interval at its intake, from a log-Pearson Type III with the state's regional skew fitted by
  maximum likelihood to the river's record. After three dry autumns (2022 to 2024) the town's drought management plan
  requires firm emergency capacity covering the Stage 2 demand less what the withdrawal permit allows at the design
  drought flow (the flow above a 0.50 cubic feet per second passby). The City of Castlewick offers firm interconnect
  capacity for 2027 to 2031 in blocks of 0.1 million gallons a day.
- **Forcing fact:** the Quillfield Select Board approves the Castlewick interconnect agreement at its December 2026
  meeting for service from 1 January 2027; the call faces forward (the capacity reserved for 2027).
- **Forum and forcing event:** council_or_assembly (the select board), purchase_order_or_contract (the interconnect
  agreement). Organisation local_government; role operations_director. Personas from `guard.py names --geo "United
  States" --seed 466`: Jaime Galloway (Quillfield's water superintendent, who brings the reservation to the board),
  Phyllis Mitchell (the Quillfield Historical Society's archivist, who transcribed the water-works reports) and Darryl
  Powell (Castlewick's utilities director, who signs the offer).
- **Data-native sentence:** the water works measured the river only in the seasons the mill agreement made it stop
  pumping, so its reports hold a seven-day flow for every dry year and only "no suspension" for the rest; each of those
  years is a censored observation (its seven-day low flow stayed above two million gallons a day, 3.094 cubic feet per
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
    transcribed report table with changing units and missing years; none on the decisive step.

## Default path

1. Read the State Water Resources Board's guidance: the design drought flow is the 7-day low flow at the intake with a
   50-year recurrence interval, from a log-Pearson Type III with the regional skew of -0.30 fitted by maximum likelihood
   to the gauge's complete climatic years of approved record and to the river's earlier years in the town's reports.
2. Read the drought management plan: reserve the smallest 0.1 MGD block covering the 2027 Stage 2 demand (0.89 MGD)
   less the withdrawal the permit allows at the design drought flow (the flow above the 0.50 cfs passby).
3. Build the climatic-year (April to March) 7-day minima from the gauge's approved daily values, 1951 to 2024
   (74 years), leaving out the provisional months after September 2025.
4. Read the reports, 1894 to 1950: convert the measured lowest seven-day flows to cubic feet per second (gallons a day
   before 1921, second-feet after) and take the 14 suspension seasons' flows; the 40 report years without a suspension
   carry no flow and are left out, as are the three missing reports.
5. Fit the regional-skew log-Pearson Type III by maximum likelihood to the 88 annual low flows: the 50-year 7-day low
   flow is 1.29 cfs.
6. The permit allows (1.29 - 0.50) x 0.6463 = 0.51 MGD; the shortfall is 0.89 - 0.51 = 0.38 MGD; reserve 0.4 MGD.

Ends on: a 0.4 MGD reservation (a 50-year 7-day low flow of 1.29 cfs, a 0.38 MGD shortfall)

Golden: a 0.3 MGD reservation (a 50-year 7-day low flow of 1.53 cfs, a 0.22 MGD shortfall)

## Stump sentence

The default path fits the design drought to the gauge's 74 annual minima and the 14 report years with a measured flow,
leaving out the 40 report years without a suspension because they carry no flow, so it fits the river's early record as
if it were all drought and lands on a 50-year 7-day low flow of 1.29 cfs and a 0.4 MGD reservation (a 0.38 MGD
shortfall), where the same fit with each silent year entered as a 7-day low flow above the 3.094 cfs suspension flow
gives 1.53 cfs and reserves 0.3 MGD.

## Three rules

Task type: data-integration-record-linkage-entity-resolution: two records of one river kept under different observation mechanisms (the gauge's measured annual minima since 1951 and the water-works reports since 1894, which measured the river only in the seasons pumping stopped) conformed into one annual low-flow record and one likelihood, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is the river's 50-year 7-day low flow at the intake from a log-Pearson Type III fitted by maximum likelihood to every year of both records; data integration across sources whose observation mechanisms differ enters each report year as what its source can say (a measured flow, or a flow above the suspension flow), and replacing that likelihood with a fit to the values on file, a generic union of the two files, moves the reservation from 0.3 to 0.4 MGD.

Swap: "the warehouse's 50-year lowest week of stock from its scanner record and the old clerk's ledger, which noted the stock only in the weeks it ran out" keeps the shape and loses the move only if nothing ties the ledger's silence to a level; here the 1893 agreement ties every silent season to a seven-day flow above two million gallons a day, and the design statistic, the recurrence interval and the permit's passby are the river's own.

Layer 1: the State Hydrologic Survey's tab-delimited daily export (comment lines, a field-width row, qualifier codes for approved, estimated and provisional values), provisional months after September 2025 overlapping the approved record, the climatic year (April to March) against the agency's water year and the town's calendar-year reports, the reports transcribed by the historical society into a PDF table with flows in gallons a day before 1921 and second-feet after and three reports missing, demand in million gallons a day against river flow in cubic feet per second.

Layer 2: estimation that fits the data (censoring): the call flips on entering the report years without a suspension as censored observations above the suspension flow instead of leaving them out of the fit.

Decisive step: fitting the regional-skew log-Pearson Type III by maximum likelihood to the gauge's annual minima, the measured suspension seasons and the silent report years as seven-day low flows above 3.094 cfs, which places the 50-year low flow at 1.53 cfs and the reservation at 0.3 MGD; the fit to the values on file alone places it at 1.29 cfs and 0.4 MGD.

Not semantics: every field, code, unit and definition read correctly (two million gallons a day as 3.094 cfs over any seven consecutive days, "no suspension" as a season the flow stayed above it, the climatic year, the approved months, gallons a day and second-feet) still leaves the easy route fitting the years that carry a flow, because a year with no number looks like a year with no data; the step is how that year enters the likelihood, not what it means.

Not rule application: the guidance files the distribution, the skew, the estimation method and the records to use, and no rule or procedure says how a year without a measured flow enters the likelihood; executing every filed rule with the measured years alone files 0.4 MGD, so the step no rule performs is the censored likelihood.

Analyst test: a strong analyst who converts the units, builds the climatic-year minima from the approved daily values and adds the 14 report years with a measured flow fits the regional-skew log-Pearson Type III by maximum likelihood, gets a 50-year 7-day low flow of 1.29 cfs and reserves 0.4 MGD (the default path's Ends on).

Estimand: the State Water Resources Board's low-flow guidance (the design drought flow: the 7-day low flow at the intake with a 50-year recurrence interval, from a log-Pearson Type III with the regional skew of -0.30 fitted by maximum likelihood to the gauge's complete climatic years of approved record and to the river's earlier years as the town's water-works reports record them) and the drought management plan (the smallest 0.1 MGD block covering the Stage 2 demand less the withdrawal the permit allows at that flow).

No decoy: nothing is planted to be caught; the reports are the water works' annual reports as written, the station description and guidance describe their subjects, no memo, draft or briefing argues a method or a figure, and no document computes a design flow or a reservation.

No certified replay: no certified or published frequency statistic for the river ships; the guidance gives the regional skew only and the station description no statistics, so no figure reproduces a method.

Lesson: a record that measured only the bad years still says something about every year it is silent on, and a likelihood that drops the silent years fits the extremes as if they were typical; no build on file teaches censored historical information in a frequency fit (task255 v1 is truncation below a floor, task462 detection that rises with size).

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
