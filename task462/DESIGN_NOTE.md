# task462 design note

Architecture 1, drawn 2026-10-15 from seed ET19 (the decision and the quantity; the world moved off the seed's own
files, and the pitfall re-found from the data).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task462.json`, registered 2026-10-15. Guard WARN only. The older
  same-puzzle and same-driver signatures (gap population, G12, designation_set; method_or_model_selection) against
  task180 v4, task255 v1 and task456 are differentiated on the card. The four WARNs are answered below.
- **Seed:** ET19's world is EPA's CAMD unit emissions and GHGRP facility totals joined to EIA's plant data through the
  EPA-EIA crosswalk. task459 shipped that pack file for file (CAMD hourly emissions and monitoring plans, Forms EIA-860
  and EIA-923, the crosswalk), so this build keeps the seed's decision (what an emissions data company publishes for
  each emitter, for the customers who buy on it) and its quantity (an emissions intensity built across EPA's
  greenhouse gas reporting, production statistics and a measurement record whose keys join many-to-many). The
  intensity is a gas producer's methane intensity measured from aerial surveys.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL, own pattern detection-weighted snapshot
  totals. A measurement-informed methane inventory of each producer's sites, conformed from plume detections, flight
  coverage, the site register and the state's well production reports, is the emissions-inventory task type's own
  work. Emissions inventory last shipped in task460, four draws back; the last three draws are seasonal adjustment,
  metric definition and data integration.
- **Why this task type and mechanism:** task452 (an area from a stratified reference sample on a revised map), task459
  (CO2 per MWh read at the operating level the commitment fixes) and task460 (a marginal emission rate from hour-to-hour
  changes) spent sampling, operating level and dispatch margin; none turned snapshot detections of intermittent
  emitters, seen with a probability that rises with their rate, into a time-averaged total.
- **Shape:** 01, a slate of candidates each graded. Arithmetic: the rated set, the producer nearest the line on each
  side and its intensity (4); each of the twelve producers' measured methane in tonnes and intensity (24); the asks'
  per-producer figures (24: the gas each producer delivered to the plant and flared); the chart's named parts
  (4); the conformed detection file (2): 58.
- **Strategy:** maturity_censoring (a blank at an imaged site is a censored observation: the source was off, or on
  below what the pass could see) on the population gap (the plumes the survey recorded are not the emissions that
  happened), with the time gap behind it (four snapshots stand for a year of intermittent sources). Generators G12
  (absence against record of absence) decisive, G16 (method selection) and G13 (horizon) behind.
- **World:** Tarvane Methane Ratings, an emissions data and ratings company (invented), rates the twelve gas producers
  of the Tollaver Basin (invented, an unnamed US state) each year for the utilities and marketers that buy their gas;
  a producer rated low-methane for 2027 is one whose measured methane intensity over the rating year (the twelve months
  to 30 September 2026) is 0.20 per cent or less. Talmora Aerial (invented) flew four basin-wide campaigns for Tarvane
  in that year (November 2025, February, May and August 2026), imaging every producer site once per campaign from an
  aircraft-mounted imaging spectrometer; the producers are Calbrent Energy, Pinyon Draw Production, Brushy Mesa
  Operating, Lechuza Creek Resources, Anchell Oil & Gas, Corrandale Petroleum, Marrowind Operating, Ostrel Energy,
  Pellisto Gas Partners, Ruskmoor Exploration, Ashmund Production and Sunmere Natural Gas.
- **Forcing fact:** Tarvane's ratings committee issues the 2027 ratings on 9 December 2026, before the buyers' 2027
  supply contracts start on 1 January. The call faces forward (2027's rated supply) on a closed measurement year.
- **Forum and forcing event:** committee_or_panel (Tarvane's ratings committee), launch_or_rollout (the first ratings
  issued on aerial measurement). Organisation professional_services; role compliance_or_audit (the head of methane
  ratings, who signs the methodology). Personas from `guard.py names --geo "United States" --seed 462`: Aaron Watkins
  (head of methane ratings, owner of the standard), Kimberly Clements (Talmora Aerial's chief scientist).
- **Data-native sentence:** an aircraft images each site for a few seconds four times a year, so a tank battery that
  dumps a sixth of the time shows a large plume about once and nothing three times, while a 6 kg/h leak that never
  stops shows a plume on only about one pass in three; the survey's blanks mix "off" with "missed", and the mix depends
  on each plume's rate, which only the provider's blind releases of known rate measure.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data: censoring and truncation; here
    a detection probability that rises with the emission rate censors the small plumes, and the time average needs the
    blanks as well as the plumes.
  - `stumping/references/client/measured-drivers.md`, the held group: a conjunction of two independent corrections where
    each partial fix files its own wrong answer; time-averaging alone rates the producers with many small leaks,
    carrying each detected source alone drops the producers with tank dumps.
  - `dataset-generation/references/layer1-messiness.md`: several sources for one picture, imperfect keys (plumes placed
    by coordinates, sites that changed operator), vintages (amended production reports), units and UTC stamps, genuine
    overlap (plumes imaged twice on overlapping lines), coverage (cloud gaps); none on the decisive step.
- **Same-puzzle and abstraction:** gap population, G12, Gate G method_or_model_selection, decision designation_set.
  Nearest drivers on file 0.05 to 0.07 (task107 lineage, task253, task230 lineage, task452 lineage, task456); task230
  v2's detector whose hit rate varies was a forward residual of a fixed check, task180 v4's masking is by hour of the
  day and forecast for a changed network; none weights snapshot detections by a measured detection curve.
- **WARNs answered:** overuse.shape (01 in three of the last twelve): a rating slate grades every producer, and the
  per-producer figures are the work. repeat.gate_g (method_or_model_selection against task461): the deciding move is
  the estimator, and the mechanism differs (detection weighting of snapshots, not a record extension). repeat.deliverables
  (xlsx and csv against task461): a ratings committee's workbook and a conformed detection extract are what this work
  produces. repeat.question_form (which, against task228): a rated set is a which.

## Default path

1. Read Tarvane's rating standard (`tarvane_low_methane_rating_standard_2026.pdf`): rated if the measured methane
   intensity over the rating year is 0.20 per cent or less; a site's methane over an operator's part of the year is its
   emission rate averaged over the campaigns in that part, each counting equally, a twice-imaged site at the mean of
   its passes, times the hours.
2. Attribute each plume in Talmora's detection file to the nearest site in the site register within 150 m, and each
   site to the producer operating it on the day it was imaged.
3. For each site and pass, sum the plume rates (kg/h) at 5 kg/h or more, a site imaged without a plume counting zero;
   take the mean of a site's passes in a campaign and of its campaigns in each operator's part of the year, times the
   part's hours: tonnes of methane emitted.
4. Sum each producer's wells' gas over the rating year from the state's production reports (the latest version of
   each report, the operator of record each month), restated to 14.73 psia, times the methane share of its field's gas
   and 19.2 kg per Mcf: tonnes of methane produced.
5. Divide, and rate the producers at 0.20 per cent or less.

- **Ends on:** the campaigns' average with blanks as zeros rates eight producers: Calbrent, Pinyon Draw, Brushy Mesa,
  Anchell, Corrandale, Ostrel, Pellisto and Ashmund (Anchell 0.150, Pinyon Draw 0.155, Pellisto 0.179 and Ashmund
  0.181 per cent).
- **Golden:** four producers: Calbrent Energy, Ostrel Energy, Corrandale Petroleum and Brushy Mesa Operating (0.104,
  0.108, 0.119 and 0.134 per cent), each plume weighted by one over Talmora's detection probability at its rate before
  the passes and campaigns are averaged; Ashmund, Pinyon Draw, Anchell and Pellisto are over the line (0.232, 0.236,
  0.249 and 0.264).

## Stump sentence

The default path averages each producer's plume rates over its passes and campaigns, counting every imaged site without
a plume as zero, and rates eight producers low-methane, among them Anchell, Pinyon Draw, Pellisto and Ashmund (0.150,
0.155, 0.179 and 0.181 per cent), whose methane leaks from many 5 to 15 kg/h sources a pass catches less than half the
time; carrying each detected source through the year instead rates no producer at all, the tank-dump producers' plumes
seen once in four passes standing for the whole year; only weighting each plume by one over the survey's detection
probability at its rate, fitted to Talmora's blind controlled releases, before averaging rates the golden four:
Calbrent, Ostrel, Corrandale and Brushy Mesa.

## Three rules

- **Task type:** physical-environmental-sciences/emissions-inventory (serves ETL): a measurement-informed methane
  inventory of each producer's sites, conformed from aerial plume detections, flight coverage, the site register and
  the state's well production reports.
- **Domain test:** the deciding quantity is each producer's measured methane intensity, the time-averaged emission rate
  of its sites over the rating year against the methane its wells produced, estimated the way measurement-based methane
  inventories estimate it from aerial surveys: each plume weighted by the survey's probability of detecting a plume of
  its rate, measured on single-blind controlled releases, and the campaigns averaged.
- **Swap:** "rate the producers whose sites emitted at most 0.20 per cent of the methane they produced, from four
  aerial campaigns" with a hospital's nouns ("rate the wards whose infections were at most 0.20 per cent of their
  admissions, from four inspections") loses what decides it: a detection probability that rises with the emission rate
  of the thing detected, measured on releases of known rate, and intermittent tank dumps imaged as snapshots; an
  infection has no rate at which an inspection sees it.
- **Layer 1:** Talmora's plumes placed by coordinates and stamped in UTC, a few between two producers' pads; flight
  lines lost to cloud, and sites imaged twice where lines overlap; facility numbers shared by a pad and its battery,
  sites under two numbers, and facilities in the coverage file the register does not list; sites and wells that changed
  operator in 2026; the state's production reports with amended versions superseding the originals, at 14.65 psia; gas
  composition by field in two years' composites; kg per hour, Mcf and metric tons. Each comes from the system named;
  nothing is placed to be caught.
- **Layer 2:** estimation_fit (detection-limited snapshots of intermittent emitters): the choice that flips the call is
  weighting each plume by one over the survey's detection probability at its rate before averaging the campaigns.
- **Decisive step:** a blank at an imaged site is a partial observation: each plume stands for one over the detection
  probability at its rate of the plumes of that rate the pass could have recorded, the probability fitted to the
  provider's blind controlled releases, so each campaign's total is the detection-weighted sum and the year is the
  campaigns' average.
- **Not semantics:** every field read correctly (imaged sites, plume rates, coverage, operators, production) leaves the
  campaigns' average with blanks as zeros on eight producers; no field, code or unit says that a blank is part miss,
  which comes only from fitting the detection curve to the releases and carrying it into the estimator.
- **Not rule application:** the standard fixes the quantity (the methane emitted at rates of 5 kg/h or more over the
  rating year, against the methane produced), the 0.20 per cent line and how campaigns combine into the year (each
  counting equally, a twice-imaged site at the mean of its passes), and Talmora's note gives the form of its detection
  curve; no filed rule says what a pass that shows no plume at a site measures or how a detection curve enters a site's
  rate, so executing every stated rule with each pass's detected plumes taken as the site's rate files the eight.
- **Analyst test:** a strong analyst who attributes every plume, reads every field and applies the standard averages
  each producer's detected rates over its passes and campaigns with blanks as zeros and rates eight producers, the
  default path's `Ends on:`, four of them over the line though it puts them at 0.150, 0.155, 0.179 and 0.181 per cent
  (Anchell, Pinyon Draw, Pellisto, Ashmund).
- **Estimand:** the rating standard's measured methane intensity: the methane a producer's sites in the basin emitted
  at rates of 5 kg per hour or more over the rating year, 1 October 2025 to 30 September 2026, as a share of the
  methane in the gas its wells in the basin produced over the same twelve months, both in metric tons, each site and
  well counted to the producer operating it at the time, each site's methane its emission rate averaged over the
  campaigns in each operator's part of the year (`tarvane_low_methane_rating_standard_2026.pdf`, 2.4, 2.5 and 4.3).
- **No decoy:** no document gives a rating, an intensity, a weight or a correction; Talmora's methods note says how it
  images, detects and quantifies plumes, that a pass does not detect every plume, and the form of its detection curve (a
  logistic function of the log of the rate, fitted to its releases), as a provider does, with no level; the producers'
  inventories are their own filed reports, declared as a distractor.
- **No certified replay:** no published intensity, rating or total is reproduced; the controlled releases are the
  instrument's physical verification, raw, and confirm nothing about any producer.
- **Lesson:** a snapshot survey's blank is neither "off" nor "missed": a time-averaged total needs the campaigns'
  average for the sources that come and go and detection weighting for the sources the survey sees only sometimes,
  and each correction alone files its own wrong slate; no build on file weights detections by a measured detection
  curve.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the producers' reported 2025 inventories | the standard rates on measured methane | the greenhouse gas report file | yes: the filed figures | no | no | one division | readable |
| R1 each detected source carried through the year (none rated) | the standard's campaign average rules it out | plume coordinates group into sources | yes: a source inventory | no | no | a sum of mean rates | readable |
| R2 the passes and campaigns averaged with blanks as zeros (eight rated) | the standard's campaign average | the coverage file says which sites each pass imaged | yes: averaging snapshots | no | no | a mean of sums | readable |
| R3 each plume weighted by one over the detection probability at its rate, the passes and campaigns averaged (decisive) | no: Talmora's note says a pass does not detect every plume and gives its detection curve's form, as a provider does; no sentence names a weight, an inverse, a correction to a pass's total or a level of the curve | no column holds a detection probability or a weight; the release file holds metered rates and detected flags | no: every generic reflex lands elsewhere (blanks as zeros eight rated, carried sources none, the detected share of campaigns ten, carried sources weighted none); only a detection correction, fine or coarse, reaches the four | no | no | a curve fitted to the releases, a weight per plume and an average | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | producer | the producer operating the site or well at the time (each campaign by its imaging day, each production month by its operator of record) | the operator at the end of the rating year for the whole year | same call | the standard's 2.2 and 2.3; asserted |
| SF2 | rating year | 1 October 2025 to 30 September 2026, 8,760 hours | calendar 2026 | not executable: the production extract holds the rating year's twelve months, every campaign inside it | the standard's 2.1; asserted |
| SF3 | methane emitted | the methane the sites emitted at rates of 5 kg/h or more, whether or not a pass caught a plume | the plumes the passes recorded | not a reading: the recorded plumes are the default path's estimator of the same quantity | the standard ("emitted"); Talmora's note (a pass does not detect every plume) |
| SF4 | 5 kg/h | a plume counts when its quantified rate is 5 kg/h or more | every detected plume | same call | the standard's 2.5; asserted |
| SF5 | at or below 0.20 per cent | rated when the intensity is 0.20 per cent or less | below 0.20 | same call: no producer within 0.032 of the line | asserted |
| SF6 | the site a plume came from | the register site nearest the plume within 150 m | Talmora's facility number, mapped through the register | same call | the standard's 4.2; asserted |
| SF7 | a site imaged twice in a campaign | the mean of its passes | the first pass, the sum of both | same call | the standard's 4.3; asserted |
| SF8 | a site not imaged in a campaign | measured by its other campaigns | counted zero | same call | the standard's 4.3; asserted |
| SF9 | methane produced | the latest report for each well and month, the operator of record, gas at 14.73 psia, the field's 2026 composite methane share, 19.2 kg per Mcf | every report summed, 14.65 psia, the 2024 composites, the current operator | same call | the standard's 2.3 and 2.4; asserted |
| SF10 | the detection curve | a logistic function of ln(rate) alone, fitted by maximum likelihood to the 182 releases | probit, wind added, complementary log-log, logistic in the rate itself, binned shares | same call | Talmora's note 4.2; asserted |
| SF11 | the campaigns' weight | each campaign counting equally within each operator's part of the year | each a quarter of the year's hours; weighted by the days between campaign midpoints | same call | the standard's 4.3; asserted |
| SF12 | per cent | methane emitted over methane produced, both in tonnes | over the gas produced | adds Pinyon Draw and Ashmund | the standard's 2.5 ("as a share of its methane produced"); asserted |
| SF13 | tonnes | metric tonnes | short tons | same call | the standard; the dictionary |

## Ladder

| Rung | Construction | Producers rated | Nearest the line |
|---|---|---|---|
| R0 | each producer's reported 2025 inventory over its methane produced | all twelve | Ruskmoor highest, 0.154 |
| R1 | each detected source carried through the year at its mean detected rate | none | Calbrent 0.213, Brushy Mesa 0.214 |
| R2 | the passes and campaigns averaged, blanks as zeros (default) | eight: Calbrent, Pinyon Draw, Brushy Mesa, Anchell, Corrandale, Ostrel, Pellisto, Ashmund | Ashmund 0.181, Pellisto 0.179; Lechuza 0.215 the nearest unrated |
| R3 | each plume weighted by one over the detection probability at its rate, the passes and campaigns averaged (golden) | four: Calbrent, Ostrel, Corrandale, Brushy Mesa | Brushy Mesa 0.134, Ashmund 0.232 |

- **Other reflexes:** the share of imaged campaigns each grouped source was detected in, ten rated (Lechuza 0.183 and
  Sunmere 0.198 added); each grouped source carried with the weight, none; the coarse correction (each producer's
  default total over the mean detection chance of its plumes), the four, a detection correction all the same.
- **Margins:** the golden's rated four sit at 0.104 to 0.134 per cent and the nearest unrated, Ashmund, at 0.232 (16
  per cent over the line); the default path's wrongly rated four sit 9.5 to 25 per cent under it (Ashmund 0.181,
  Pellisto 0.179, Pinyon Draw 0.155, Anchell 0.150).
- **Dominance:** Pinyon Draw, Anchell and Pellisto hold 86 to 91 per cent of their methane outside episodes in
  persistent leaks of 5 to 15 kg/h, which a pass detects 28 to 78 per cent of the time (Ashmund 67 per cent beside its
  episodes); the tank-dump producers (Brushy Mesa, Corrandale, Ruskmoor) hold 17 per cent there, their plumes running 80
  to 200 kg/h and detected nearly every time they occur, so weighting barely moves them while carrying them through the
  year multiplies them by about four.
- **Grid:** two choices (time: each source carried, or the campaigns averaged; detection: unweighted or weighted) give
  four cells: carried unweighted none rated, carried weighted none, averaged unweighted eight, averaged weighted the
  golden four (asserted).
- **Worth:** every producer's intensity differs on every rung at three decimals; the golden moves Anchell, Pinyon Draw
  and Pellisto up 48 to 66 per cent from the default path, Ashmund 28, and the tank-dump producers 7 to 9.
- **Data-native structure:** the provider's releases detect 1 of 49 below 3 kg/h and 34 of 35 above 40 kg/h; the
  producers differ in where their methane sits, not in their size (the rated four produced 232 to 376 Bcf over the
  year, the rest 94 to 518).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the methane each producer's basin sites emitted at 5 kg/h or more over the rating year, plumes the passes missed included | the standard; Talmora's note that a pass does not detect every plume |
| 2 | Unit of account | the producer, its sites and wells by operator at the time | the standard (SF1) |
| 3 | Attribution window | 1 October 2025 to 30 September 2026; each campaign counting equally within each operator's part of the year | the standard's 2.1 and 4.3 (SF2, SF11) |
| 4 | As-of dating | the state's reports as pulled on 15 November 2026; Talmora's final campaign data | the manifest |
| 5 | Version basis | the latest report for each well and month | SF9 asserted |
| 6 | Denominator | the methane in the gas the producer's wells produced, tonnes | the standard (SF9, SF12) |
| 7 | Weighting | each campaign equally; each pass of a twice-imaged site equally | the standard's 4.3 (SF7, SF11), asserted |
| 8 | Window length | the four campaigns of the rating year | the standard; the campaigns dated |
| 9 | Boundary inclusivity | rated at 0.20 per cent or less; a plume at 5.0 kg/h counts | the standard (SF4, SF5) |
| 10 | Rounding path | intensities from unrounded tonnes, shown to three decimals; the rating read unrounded | the prompt's rounding sentence |
| 11 | Tie-break | none needed | no producer within 0.01 of the line (asserted) |
| 12 | Maturity and censoring | every campaign is final; a blank at an imaged site is an observation, at an unimaged site none | the standard's 4.3 and the coverage file (SF8); the decisive step |
| 13 | Order of operations | attribute, weight, sum per pass, average the passes then the campaigns per tenure, multiply by hours, sum, divide | the standard's 4.3; C1 |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | a plume imaged on two lines is two passes' observations, averaged; amended production reports supersede | SF7, SF9 |
| 16 | Identity normalisation | the register's site ids, the state's facility numbers and operator numbers mapped through the register and the operator list | SF6 asserted |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | kg/h, Mcf at 14.65 psia converted to 14.73, metric tonnes | the dictionary; the standard |
| 19 | Code and status semantics | report type (original or amended), imaged or lost to cloud | the dictionary |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the standard applies to every producer alike | the standard |
| 22 | Forward window contents | the 2027 rating rests on the measurement year just closed | the standard |

## Literal reader

Executed word for word, the standard asks for the methane each producer's sites emitted at rates of 5 kg/h or more over
the rating year against the methane its wells produced, each site's methane its emission rate averaged over the
campaigns in each operator's part of the year (each campaign equally, a twice-imaged site at the mean of its passes)
times the hours, and rates the producers at 0.20 per cent or less; the literal reader has four snapshots of each site,
Talmora's statement that a pass does not detect every plume, the form of its detection curve and the release study it
is fitted to, so a site's emission rate at a pass is the pass's plumes each weighted by the detection probability at
its rate; every other form of the curve (SF10) rates the same four. No filed sentence counts a blank as zero or says how
a pass's plumes become the site's rate.

## Oracles

None ties only under the golden. Talmora's campaign summary counts plumes reported and ties on every path; the
satellite's annual range for the whole basin, 66,795 to 227,468 t, holds every rung's total for the twelve (79,410 to
163,154 t), asserted; the reported inventories are the producers' filings, declared as a distractor, ruled out by the
standard's measured basis.

## Ask sheet

- **Ask A, the gas each producer delivered to the Tollaver processing plant over the rating year (12 figures, whole
  million cubic feet).** H18 home: the rating's input reconciled to another system's total (the gas the wells produced
  against the gas the plant received), and the rated supply a buyer can take at the plant's tailgate. Path: the plant's
  monthly allocation statement lines, its meter station list (stations to producers, the two energy-metered stations),
  the stations' monthly heating values, the operator list and the dictionary (five files, eleven columns). Primary
  device: D7, the true key elsewhere: each line's month column is the statement's accounting month, and the production
  month sits only in the line's reference ("Alloc 2026-03" on current lines, "PPA 2026-01 M-114 meter correction" on
  prior-period adjustments); the October 2025 statement carries September 2025 adjustments and the October 2026
  statement September 2026 adjustments at every producer's stations, so a filter on the month column moves every
  producer's figure. Hazards: H1 the March 2026 statement re-issued whole as revision 2 beside the original (D1); H2 two
  stations (Corrandale's and Sunmere's) metering energy only from July 2026, their volumes blank, converted with the
  station's heating value for the month (D3). Stops (asserted): the accounting month (the cracker) moves every producer
  110 to 408 MMcf; both March revisions add 8,562 to 41,381; MMBtu read as Mcf moves Corrandale up 253 and Sunmere up
  1,486; blank volumes read as zero take them down 4,661 and 21,789; the golden. Realism: a processing plant's
  allocation statements book measurement corrections in the month they are found.
- **Ask B, the gas each producer flared over the rating year (12 figures, whole million cubic feet).** H18 home: a
  measure every candidate carries that the rating does not turn on, the flaring a buyer weighs beside the methane
  rating. Path: the state's flaring and venting reports by lease and month, the lease register (lease to operator by
  month), the operator list, the commission's monthly basin summary and the dictionary (five files, nine columns).
  Primary device: D2, a label stored before a silent switch: from January 2026 the commission's reports split
  disposition code FL into FL (flared, emergency or upset) and FR (flared, routine), and the folder's dictionary carries
  the commission's code list from before the switch, FL flared and VT vented; a filter on FL keeps every producer's
  October to December 2025 flaring whole and its 2026 emergency flaring, so nothing looks empty, and drops its routine
  flaring from January. The commission's monthly basin summary ties only with FR counted (the referee). Hazards: H4
  leases that changed operator, credited to the operator of record each month (D7); H5 the reports' amended versions
  (D2, the latest supersedes). Stops (asserted): FL alone (the cracker) takes every producer down 318 to 3,054 MMcf; FL,
  FR and VT up 282 to 1,932; each lease to its final operator moves Calbrent and Sunmere by 429 and Ruskmoor and
  Pellisto by 123; every report version up 25 to 148; the golden. Realism: state commissions split flaring codes when a
  routine-flaring rule takes effect.
- **The construction layer:** each producer's methane emitted (tonnes) and measured intensity (per cent), the rating,
  the chart of every producer's intensity against the 0.20 per cent line, and the conformed plume file; the cracker has
  them.
- **Main population zero-counts (asserted):** the main call reads no plant statement, station, heating value, flaring
  report, lease or basin summary row (the call and every rung computed with those files deleted are identical); the
  asks read no plume, pass, release, site, well production or gas analysis row (Ask A and B computed with those files
  deleted are identical). No device or hazard row sits in a file the call reads.
- **Hazard table (asserted):** H1 moves every producer (the re-issued March statement covers every station); H2
  Corrandale and Sunmere; H4 the transfers' four producers (Calbrent, Sunmere, Ruskmoor, Pellisto); H5 every producer.
- **Rounding edges (asserted):** every Ask A and Ask B figure and total 0.04 MMcf or more from its whole-MMcf edge
  (0.055 and 0.043 the nearest); each producer's methane 0.05 t or more from its whole-tonne edge and each intensity
  0.00005 or more from its three-decimal edge.
- **Referee:** the commission's monthly basin flaring summary arbitrates FR without handing over a level (it ties with
  FL and FR every month, with FL alone only before January 2026, and is the basin's total, every operator together);
  Ask A has none, no plant total ships.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, gas delivered to the plant by producer | filters the statement lines on their month column, keeps the later revision of March, converts the two stations' energy with their heating values; every producer carries September 2025's adjustments and lacks September 2026's | miss |
| B, gas flared by producer | sums disposition code FL, the code the dictionary gives for flared gas, by the operator of record each month; every producer's routine flaring from January 2026 is missing | miss |

- Mirror leakage: about 8 per cent of ask weight (a response on R2 keeps the conformed plume file; it misses every Ask A
  and Ask B figure on the same devices as the cracker).
- Pair ceiling: 32.7 (planning weights 38 / 7 / 55 with the call, each producer's methane and intensity and the chart in
  the main block and r = 5; the ask weight spread over 26 criteria: A 12, B 12, the file 2; the cracker keeps the file,
  2 of 26 or 0.08, 38 + 7 + 4.2 = 49.2; the mirror keeps r, instruction-following and the file, 5 + 7 + 4.2 = 16.2;
  average 32.7), rerun from the generated rubric at ship.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| plumes placed by coordinates, a few within 150 m of two sites | Talmora's plume localisation | plume file | Talmora's facility number taken as the site | SF6: the call unchanged |
| a site under two facility numbers, a pad and its battery under one | the commission's permits | site register, coverage | a one-to-one join | the call unchanged |
| facilities in the coverage file the register does not list | Talmora's facility list against Tarvane's register | coverage | none needed: no producer plume sits within 150 m of one | asserted |
| a flight line lost to cloud in each campaign | the aircraft's operations | coverage | the line's sites counted zero | SF8: the call unchanged |
| sites imaged twice where lines overlap | the flight plan | coverage, plume file | both passes summed, or the first kept | SF7: the call unchanged |
| sites and wells that changed operator on 1 April and 1 July 2026 | the producers' acquisitions | site register, production | the year to the final operator | SF1: the call unchanged |
| amended production reports | the operators' filings | production | every report summed | SF9: the call unchanged |
| gas at 14.65 psia, the standard's density at 14.73 | the commission's pressure base | production | no conversion | SF9: the call unchanged |
| composite analyses for 2024 and 2026 by field | the operators' laboratories | gas analyses | the older composite | SF9: the call unchanged |
| image times in UTC | Talmora's processing | plume file, coverage | read as local time | no plume changes producer |

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each producer's measured methane
  intensity, its sites' time-averaged emissions over the rating year estimated the way measurement-informed inventories
  estimate them from aerial surveys (each plume over the survey's detection probability at its rate, the curve fitted
  to blind controlled releases); replacing it with the detected plumes alone (blanks as zeros), each detected source
  carried all year or the producers' reported inventories moves the call (eight, none, all twelve). Two layers: the
  Layer 1 inventory above, each main-call item asserted neutral (R2, SF1, SF6 to SF9) and each ask item confined to its
  ask with zero main-call rows (the separation checks); Layer 2 the detection weighting. The decisive step is none of
  the three banned kinds, each executed in `checks.py`: not a plant (R3c: no well's monthly gas, no plume's rate and
  origin and no lease's vented series repeats another's; no document names a producer, a rating, an intensity figure, a
  weight or a correction; the provider's note gives its curve's form and no level); not data semantics (R2 and SF1 to
  SF13: every field, clock, unit and name mishandled leaves the call where it is, and every field read correctly still
  leaves the default path on eight); not rule application (R3a: with every filed rule executed on the clean truth the
  default path rates the eight; R3b: only the detection weighting rates the four, while carried sources rate none and
  the detected share of campaigns ten).
- **Gates.** 19 files in 4 formats (csv, json, pdf, xlsx); the production file at 38,150 rows; two distractors (the
  producers' Subpart W reports and the satellite basin estimates) the solution never reads, each deletion leaving the
  call and every ask unchanged; 91 checks; `verify.py` from the bundle alone; two builds byte-identical;
  `figures_check.py`, `precut.py` and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK); guard heart WARN (the four
  draw WARNs, answered above); surface promoting task460 (two apart, the shared pairing; the dictionary's header, the
  one column set it repeated, was reshaped) and task456, task255 and task180 (the same gap, pattern and Gate G or
  decision type, differentiated on the card) for the author's read; the containers carry the fiction's people and
  dates; the invented names screened for near-misses of real places and firms (Dellmont, Sedgeway, Kestrin, Haskell,
  Ravenna, Bellwood, Harlan and the mailing cities renamed, every figure unchanged).

## Leak check

- `leak.py`: REVIEW, no LEAK. Its answer-figure lines are the 150 m attribution radius, filed in the standard and the
  provider's note, and "350,917" read across two cells of one production row (oil 350 bbl, water 917 bbl), no golden
  figure; its vocabulary lines are the standard and the provider's note in their own words (campaign, detection,
  imaged, coverage), neither naming the weighting; its announcements are the note's header and contact line; the
  register names the producers beside their sites' coordinates, which ranks nothing.
- Reader (2026-10-15, one pass): REVIEW, nothing hands over the decisive step or a rating. Questions 1 to 4 none: no
  sentence orders the correction ("the note and the workbook supply the ingredients and nothing orders the step"), no
  file ranks or helps, no figure reads as the answer; question 5's literal execution of the standard with the passes'
  plumes taken as the rate is the default path (its rough figures the eight, Calbrent 0.076 to Ashmund 0.179); question
  6 an analytical choice. Its three items stay as they are: the FR code is Ask B's device, the basin summary its
  referee (FL and FR tie it every month); the plant's prior-period lines carry the production month in their reference
  and the March statement's second revision re-issues it whole, Ask A's device and hazard, the delivery month being what
  "delivered over the rating year" reads as; the note's 4.2 is the form of the provider's detection curve, filed so the
  graded tonnes are determinate (Tried and rejected), and names no weight or correction. Its realism notes need nothing:
  site names carry the field's first word (Lechuza Creek, Corran Ridge), the four small operators are the commission's,
  and the folder was assembled on 18 November after the note's October issue.

## Determinism judge

- Pass 1 (2026-10-15, `determinism_check_report.md`): DETERMINISTIC, APPROVE. Every figure reproduced from the bundle:
  the detection curve (7.96 and 23.86 kg/h), the 2,348, 2,241 and 107 plume rows, and each producer's methane emitted,
  intensity, gas delivered and gas flared. Gate G analytical_non_defect (its mechanism label statistical_rigor, the
  estimator's choice on the card as method_or_model_selection), surface_read_dependency no, sole_data_defect no; Gate H
  domain pass, layers pass, decisive_step analytical. The four held under every variant it ran (Talmora's own facility
  attribution, no operator split, a logistic in the rate itself, no floor); only the uncorrected sum (the default path,
  eight) and a 10 kg/h floor outside the filed 5 move it. Stump power moderate on the call, high on the asks.
- Its three advisory forks stay as they are. The detection correction is the decisive step, left open with the
  estimand filed ("emitted") and the plume source's own documentation saying a pass does not detect every plume. The
  plant's prior-period lines and the FR code are Ask A's and Ask B's devices: a dictionary line for either would narrate
  the device and hand both asks to the top pair, while FR has its referee (the basin summary ties FL and FR every month)
  and the delivery month is what "delivered over the rating year" reads as.

## Tried and rejected

- 2026-10-15, draw: the seed's own world, plant CO2 per MWh across CAMD, GHGRP and EIA through the EPA-EIA crosswalk.
  Rejected: task459 shipped those files, and in that world the decisive candidates were the crosswalk key, scope and
  net-against-gross readings (data semantics) or the operating level (task459's step); the many-to-many keys stay as
  Layer 1 here.
- 2026-10-15, build: each producer's tonnes with the detection curve's form left open. Rejected: the call held under
  every form, but a complementary log-log, a wind-normalised or a binned curve moved the tonnes 5 to 25 per cent from the
  logistic, so a judge choosing its own form would not reproduce the graded figures; Talmora's note now gives the
  curve's form and the standard how campaigns combine into the year, the weighting itself left unstated.
- 2026-10-15, build: the production extract from July 2025. Rejected: summing the whole extract moves the call, a Layer
  1 item carrying weight; the extract holds the rating year.
- 2026-10-15, build: a permit shared by a pad and a battery on different flight lines. Rejected: the coverage file gave
  the pad passes it never had; a permit is shared only where both sit under the same lines.
- 2026-10-15, build: gas to one decimal of a million cubic feet. Rejected: sums of whole Mcf sat within 2 Mcf of a
  rounding edge; whole million cubic feet, with the plant's and the commission's streams drawn so every ask figure sits
  0.04 MMcf or more from its edge.
- 2026-10-15, build: every producer's site count a multiple of five and its year of gas a round level. Rejected as
  realism tells; the register leaves out a few imaged sites that carry no source and sit 400 m or more from every
  plume, and each producer's gas takes a non-round level.
