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
  per-producer and per-campaign figures (designed at stage 2, 15 or more); the chart's named parts (4); the conformed
  detection file (2): 49 or more.
- **Strategy:** maturity_censoring (a blank at an imaged site is a censored observation: the source was off, or on
  below what the pass could see) on the population gap (the plumes the survey recorded are not the emissions that
  happened), with the time gap behind it (four snapshots stand for a year of intermittent sources). Generators G12
  (absence against record of absence) decisive, G16 (method selection) and G13 (horizon) behind.
- **World:** Tarvane Methane Ratings, an emissions data and ratings company (invented), rates the twelve gas producers
  of the Tollaver Basin (invented, an unnamed US state) each year for the utilities and marketers that buy their gas;
  a producer rated low-methane for 2027 is one whose measured methane intensity over the rating year (the twelve months
  to 30 September 2026) is 0.20 per cent or less. Kestrin Aerial (invented) flew four basin-wide campaigns for Tarvane
  in that year (November 2025, February, May and August 2026), imaging every producer site once per campaign from an
  aircraft-mounted imaging spectrometer; the producers are Calbrent Energy, Pinyon Draw Production, Brushy Mesa
  Operating, Lechuza Creek Resources, Anchell Oil & Gas, Corrandale Petroleum, Marrowind Operating, Ostrel Energy,
  Dellmont Gas Partners, Ruskmoor Exploration, Sedgeway Production and Sunmere Natural Gas.
- **Forcing fact:** Tarvane's ratings committee issues the 2027 ratings on 9 December 2026, before the buyers' 2027
  supply contracts start on 1 January. The call faces forward (2027's rated supply) on a closed measurement year.
- **Forum and forcing event:** committee_or_panel (Tarvane's ratings committee), launch_or_rollout (the first ratings
  issued on aerial measurement). Organisation professional_services; role compliance_or_audit (the head of methane
  ratings, who signs the methodology). Personas from `guard.py names --geo "United States" --seed 462`: Aaron Watkins
  (head of methane ratings, owner of the standard), Kimberly Clements (Kestrin Aerial's chief scientist).
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
   intensity over the rating year is 0.20 per cent or less.
2. Attribute each plume in Kestrin's detection file to the nearest site in the site register, and each site to the
   producer operating it on the day it was imaged.
3. For each producer and campaign, sum the plume rates (kg/h) at its imaged sites, a site imaged without a plume
   counting zero; average the four campaigns; multiply by the rating year's 8,760 hours: tonnes of methane emitted.
4. Sum each producer's wells' gas over the rating year from the state's production reports (the latest version of
   each report, the operator of record each month), times the methane share of its field's gas and 19.2 kg per Mcf:
   tonnes of methane produced.
5. Divide, and rate the producers at 0.20 per cent or less.

- **Ends on:** the campaigns' average with blanks as zeros rates seven producers, three of them (the producers whose
  methane leaks from many sources the survey sees on fewer than half its passes) over the limit on the detection-weighted
  estimate (planned; the generator fixes the names).
- **Golden:** four producers (planned), each plume weighted by one over Kestrin's detection probability at its rate
  before the campaigns are averaged.

## Stump sentence

The default path averages each producer's plume rates over the four campaigns, counting every imaged site without a
plume as zero, and rates seven producers low-methane, three of whose methane leaks from many 3 to 15 kg/h sources the
survey catches on fewer than half its passes; carrying each detected source through the year instead fails the
producers whose methane comes from tank dumps seen once in four passes; only weighting each plume by one over the
survey's detection probability at its rate, measured on Kestrin's blind controlled releases, before averaging the
campaigns rates the golden four.

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
- **Layer 1:** Kestrin's plumes placed by coordinates and stamped in UTC, a few between two producers' pads; flight
  lines lost to cloud, and plumes imaged twice where lines overlap; the site register with sites that changed operator
  in 2026 and one site under two spellings; the state's production reports with amended versions superseding the
  originals and wells that changed operator; gas composition by field; kg per hour, Mcf and metric tons. Each comes from
  the system named; nothing is placed to be caught.
- **Layer 2:** estimation_fit (detection-limited snapshots of intermittent emitters): the choice that flips the call is
  weighting each plume by one over the survey's detection probability at its rate before averaging the campaigns.
- **Decisive step:** a blank at an imaged site is a partial observation: each plume stands for one over the detection
  probability at its rate of the plumes of that rate the pass could have recorded, the probability fitted to the
  provider's blind controlled releases, so each campaign's total is the detection-weighted sum and the year is the
  campaigns' average.
- **Not semantics:** every field read correctly (imaged sites, plume rates, coverage, operators, production) leaves the
  campaigns' average with blanks as zeros on seven producers; no field, code or unit says that a blank is part miss,
  which comes only from fitting the detection curve to the releases and carrying it into the estimator.
- **Not rule application:** the standard fixes the quantity (the methane emitted at rates of 3 kg/h or more over the
  rating year, against the methane produced) and the 0.20 per cent line; no filed rule says how four snapshots become a
  year or what a blank means, so executing every stated rule with the campaigns averaged files the seven.
- **Analyst test:** a strong analyst who attributes every plume, reads every field and applies the standard averages
  each producer's detected rates over the four campaigns with blanks as zeros and rates seven producers, the default
  path's `Ends on:`, three of them over the limit.
- **Estimand:** the rating standard's measured methane intensity: the methane a producer's sites in the basin emitted
  at rates of 3 kg per hour or more over the rating year, 1 October 2025 to 30 September 2026, as a share of the
  methane in the gas its wells in the basin produced over the same twelve months, both in metric tons, each site and
  well counted to the producer operating it at the time (`tarvane_low_methane_rating_standard_2026.pdf`).
- **No decoy:** no document gives a rating, an intensity, an estimator or a correction; Kestrin's methods note says how
  it images, detects and quantifies plumes and reports its controlled-release study as a provider does, and the
  producers' inventories are their own filed reports, declared as a distractor.
- **No certified replay:** no published intensity, rating or total is reproduced; the controlled releases are the
  instrument's physical verification, raw, and confirm nothing about any producer.
- **Lesson:** a snapshot survey's blank is neither "off" nor "missed": a time-averaged total needs the campaigns'
  average for the sources that come and go and detection weighting for the sources the survey sees only sometimes,
  and each correction alone files its own wrong slate; no build on file weights detections by a measured detection
  curve.

## Tried and rejected

- 2026-10-15, draw: the seed's own world, plant CO2 per MWh across CAMD, GHGRP and EIA through the EPA-EIA crosswalk.
  Rejected: task459 shipped those files, and in that world the decisive candidates were the crosswalk key, scope and
  net-against-gross readings (data semantics) or the operating level (task459's step); the many-to-many keys stay as
  Layer 1 here.
