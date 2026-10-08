# Descriptive & Distribution Analysis — 50 tasks (DA01–DA50)

Each file is a stump design note: the driving force, a ladder of defensible wrong answers on correct data, why the decisive move survives a strong solver, the calibration corpus, pins and voices, determinism, the prompt and the ask layer. `analytical_tasks_index.csv` at the repository root carries the header fields for all 300 tasks.

**Upgraded to the v2 stump design:** 1 of 50.

| ID | Task | Domain | Decision shape | Design |
|---|---|---|---|---|
| DA01 | [How concentrated is a state's income? Top shares from binned tax data need the right tail model](DA01_top-income-shares-pareto-interpolation.md) | Public finance / state revenue volatility / credit analysis | 14 · Cuts of a distribution | v1 |
| DA02 | [Which patent examining groups are slowest? Percentiles of waiting times when many cases are still waiting](DA02_patent-pendency-censored-percentiles.md) | Government operations / intellectual-property administration / workload planning | 01 · Ranked list under a cap | v1 |
| DA03 | [Severe rent burden by neighbourhood: survey weights, household weights and honest margins of error](DA03_acs-pums-replicate-weights-rent-burden.md) | Housing policy / grant eligibility / survey statistics | 10 · Scorecard against thresholds | v1 |
| DA04 | [Planning bands for wildfire response: most fires are small, most burned area is not](DA04_wildfire-size-area-weighted-cuts.md) | Wildland fire management / emergency resource planning / catastrophe insurance | 14 · Cuts of a distribution | v1 |
| DA05 | [How long do patients wait? The waiting list over-represents the people who wait longest](DA05_waiting-list-length-biased-snapshot.md) | Healthcare operations | 14 · Cuts of a distribution | v1 |
| DA06 | [Daily and monthly active contributors: uniques do not add up](DA06_contributor-stickiness-dau-mau-nonadditive.md) | Online community / product analytics | 07 · Grid of cells | v1 |
| DA07 | [Fleet fuel economy: averaging miles per gallon flatters the fleet](DA07_fleet-fuel-economy-harmonic-mean.md) | Automotive / fleet sustainability | 10 · Scorecard against thresholds | v1 |
| DA08 | [Portfolio web performance: you cannot average 75th percentiles](DA08_web-vitals-portfolio-p75-histogram-merge.md) | Web performance / product analytics | 14 · Cuts of a distribution | v1 |
| DA09 | [Salary bands from a self-selected survey: rake to the workforce before you cut percentiles](DA09_developer-salary-survey-raking.md) | Labour market / compensation | 14 · Cuts of a distribution | v1 |
| DA10 | [How long do credit unions last? A panel that starts in 1994 cannot see the ones that died before](DA10_institution-lifetimes-delayed-entry.md) | Financial institutions / industry structure | 14 · Cuts of a distribution | v1 |
| DA11 | [Wealth percentiles from a survey with five imputations: one implicate is not the data, five are not five times the sample](DA11_wealth-percentiles-multiple-imputation.md) | Household finance | 14 · Cuts of a distribution | v1 |
| DA12 | [Latency budgets across microservices: per-hop P99s do not add up to the user's P99](DA12_microservice-latency-budget-p99-nonadditive.md) | Distributed systems / SRE | 05 · Allocation to a fixed total | v1 |
| DA13 | [PFAS in drinking water: what you do with "below reporting limit" decides the answer](DA13_pfas-nondetects-regression-on-order-statistics.md) | Environmental health / water utilities | 14 · Cuts of a distribution | v1 |
| DA14 | [A weekly price index from scanner data: chaining through sales makes prices drift](DA14_scanner-price-index-chain-drift.md) | Retail pricing / price statistics | 03 · Bridge between two totals | v1 |
| DA15 | [Time spent: per participant, per person, and per day of the week](DA15_time-use-diary-weights-participants.md) | Media / consumer behaviour | 07 · Grid of cells | v1 |
| DA16 | [Did home prices fall? The median sale changed because different homes sold](DA16_property-price-change-repeat-sales.md) | Real estate | 03 · Bridge between two totals | v1 |
| DA17 | [Expected lifetime versus average age at exit: the age structure answers a different question](DA17_lifetime-period-life-table-vs-mean-age-at-exit.md) | Demography / actuarial analytics | 07 · Grid of cells | v1 |
| DA18 | [How dense is a metro for the people who live there? Area density averages in empty land](DA18_population-weighted-density-census-blocks.md) | Urban analytics / site selection | 01 · Ranked list under a cap | v1 |
| DA19 | [Attrition rates: the denominator is average headcount, and a transfer is not a loss to the enterprise](DA19_workforce-attrition-denominators-transfers.md) | Human resources / public workforce | 07 · Grid of cells | v1 |
| DA20 | ["A bus every 10 minutes": riders who arrive at random wait longer than half the headway](DA20_bus-wait-inspection-paradox.md) | Public transit operations | 01 · Ranked list under a cap | v1 |
| DA21 | [Who accounts for the spending? Concentration curves must include the people who spend nothing](DA21_spending-concentration-zeros-weights.md) | Health economics / payer analytics | 14 · Cuts of a distribution | v1 |
| DA22 | [How different are hospitals really? Observed spread includes sampling noise](DA22_patient-experience-true-variation-deconvolution.md) | Healthcare quality / patient experience | 14 · Cuts of a distribution | v1 |
| DA23 | [How heavy is the tail of open-source dependencies? A straight line on a log-log plot is not an estimate](DA23_package-dependents-power-law-tail.md) | Software ecosystems / security | 14 · Cuts of a distribution | v1 |
| DA24 | [Where to set the income cut so an affordability credit reaches exactly the 120,000 households it is budgeted for](DA24_affordability-credit-cut-conditioned-uptake.md) | Demographic & Social Science · household income and affordability | An allocation under a cap | v2 |
| DA25 | [The worst three hours: when the window crosses midnight, the arithmetic mean of clock time lies](DA25_collision-time-of-day-circular-windows.md) | Road safety / enforcement operations | 01 · Ranked list under a cap | v1 |
| DA26 | ["Your connections have more connections than you": the network as users experience it](DA26_developer-network-friendship-paradox.md) | Developer communities / social networks | 07 · Grid of cells | v1 |
| DA27 | [Market concentration by county: contracts are not competitors when one parent owns them](DA27_health-plan-market-concentration-parent-rollup.md) | Health insurance markets | 01 · Ranked list under a cap | v1 |
| DA28 | ["More billion-dollar storms than ever": a nominal threshold rises with prices and with what is built](DA28_storm-damage-constant-dollar-thresholds.md) | Catastrophe risk / insurance | 03 · Bridge between two totals | v1 |
| DA29 | [When did the corrosion start? Failures seen only at annual tests are interval-censored](DA29_vehicle-corrosion-interval-censored-ages.md) | Automotive reliability | 14 · Cuts of a distribution | v1 |
| DA30 | [Do households get the speed they pay for? Count households, not tests](DA30_broadband-speed-unit-vs-test-weighting.md) | Telecommunications / consumer protection | 10 · Scorecard against thresholds | v1 |
| DA31 | [Pay distributions with partial-year workers: annualise before you compare](DA31_payroll-annualization-partial-year.md) | Public-sector payroll / HR analytics | 14 · Cuts of a distribution | v1 |
| DA32 | [Annual traffic from a one-day count: expand with the right seasonal and weekday factors](DA32_road-traffic-aadf-expansion-factors.md) | Transport planning | 02 · Forecast across many periods | v1 |
| DA33 | [Is the species spreading, or are more people looking? Occurrence counts track observers](DA33_species-occurrence-effort-corrected-reporting.md) | Biodiversity / environmental consulting | 07 · Grid of cells | v1 |
| DA34 | [Sizing a feeder: the sum of each home's peak is not the peak of the homes](DA34_household-load-diversity-factor-coincident-peak.md) | Electricity distribution | 05 · Allocation to a fixed total | v1 |
| DA35 | ["Top 10% papers": percentiles only mean something within field and year](DA35_citation-percentiles-field-year-normalized.md) | Research analytics / funding | 01 · Ranked list under a cap | v1 |
| DA36 | [Which research area is growing fastest? Cross-listed papers are counted once, not three times](DA36_preprint-category-fractional-counting.md) | Research analytics / publishing | 03 · Bridge between two totals | v1 |
| DA37 | [Freight mode share: by shipments, by tons or by ton-miles — and always with the survey weights](DA37_freight-mode-share-weighting-basis.md) | Freight transportation | 07 · Grid of cells | v1 |
| DA38 | [Privacy-bucketed rates: report what the ranges allow, not what the midpoints suggest](DA38_range-coded-proficiency-bounds.md) | Education accountability | 10 · Scorecard against thresholds | v1 |
| DA39 | [How many journeys does the region's transit carry? Boardings count every leg](DA39_transit-linked-trips-transfer-factors.md) | Public transportation | 03 · Bridge between two totals | v1 |
| DA40 | [How local are people's friendships? A connectedness index needs destination weights](DA40_social-connectedness-distance-distribution.md) | Social networks / local products | 14 · Cuts of a distribution | v1 |
| DA41 | [Counting from a machine-learning layer: predicted positives are not the count](DA41_ml-derived-building-counts-misclassification.md) | Geospatial analytics / infrastructure planning | 10 · Scorecard against thresholds | v1 |
| DA42 | [Pooling an effect measured at many sites: simple averages hide heterogeneity](DA42_multisite-effects-random-effects-pooling.md) | Behavioural research / experimentation | 07 · Grid of cells | v1 |
| DA43 | [Infection rates from pooled tests: a positive pool may hold more than one positive](DA43_pooled-sample-infection-rate-mle.md) | Public health / vector control | 01 · Ranked list under a cap | v1 |
| DA44 | [An annual mean from 8,760 hours is not 8,760 independent observations](DA44_annual-mean-autocorrelated-effective-sample.md) | Air quality / environmental compliance | 10 · Scorecard against thresholds | v1 |
| DA45 | [How stable is a top-sites list? Set overlap ignores order and treats rank 1 like rank 10,000](DA45_top-list-stability-rank-biased-overlap.md) | Internet measurement / security research | 07 · Grid of cells | v1 |
| DA46 | [Reference percentiles from heaped, misdated records: clean the implausible tail before you cut](DA46_birthweight-reference-curves-heaping-misdating.md) | Maternal and child health | 14 · Cuts of a distribution | v1 |
| DA47 | [GPU fleet efficiency: the average job is not where the GPU-hours go](DA47_gpu-cluster-utilization-weighting.md) | ML infrastructure | 03 · Bridge between two totals | v1 |
| DA48 | [How many vulnerabilities have public exploits? Two incomplete lists and an estimate of what both miss](DA48_exploit-availability-capture-recapture.md) | Cybersecurity / vulnerability management | 14 · Cuts of a distribution | v1 |
| DA49 | [Reliability with storms set aside: major event days by the 2.5-beta rule, not by eye](DA49_power-reliability-major-event-days.md) | Electric utilities | 10 · Scorecard against thresholds | v1 |
| DA50 | [What solar actually earned: the time-weighted average price is not the price solar captured](DA50_solar-capture-price-generation-weighted.md) | Electricity markets / renewable investment | 07 · Grid of cells | v1 |
