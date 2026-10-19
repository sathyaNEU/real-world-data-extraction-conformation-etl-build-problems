# The domain taxonomy

Seven groups, twenty-one client domains, each with its task types; every task type serves one or two of the eight
Axis 1 objectives. A build picks one domain and one task type (the card's `domain` and `subdomain`) and one objective
that task type serves. `fingerprint/vocab.json` (`client_domains`) is the copy the guard enforces.

Objectives: F Forecasting & Predictive Modeling, RC Root-Cause Analysis, AD Anomaly Detection & Diagnostics, EC
Experiment & Causal Analysis, DD Descriptive & Distribution Analysis, ETL Data Extraction & Conformation, OS
Opportunity Sizing & Decision Support, DQ Data Quality Monitoring & Alerting.

Layer 2 patterns per task type: `../../../stumping/references/client/layer2-rigor-patterns.md`. Layer 1 mess per
domain: `../../../dataset-generation/references/layer1-messiness.md`. Three domains (Physical & Environmental Sciences;
Energy Systems & Utilities; Human Factors & Ergonomics) have Layer 1 techniques but no Layer 2 patterns: take the
pitfall from the five Layer 2 families in `../../../stumping/references/client/two-layer-task-design.md`. Quantitative
Finance, Banking and Actuarial Science carry their patterns under the client's finer stumping-page task types, each
mapped in the library to the taxonomy task type the card's `subdomain` takes.

**Close calls.** Biomedical & Clinical Research is study data on treatments and trials; Epidemiology & Public Health
is populations, exposures and surveillance; Pharmacology is drug exposure and safety; Healthcare Delivery & Health
Economics is the system's operations, costs and claims. Economics is macro, labour, trade and fiscal reads, never
corporate finance, markets trading or lending. A platform selling into a sector is Product Analytics with that
sector's data as its market.

**House domains.** The nine domains of the earlier spec stay valid on filed cards; a new draw in one names the client
domain it sits in (the guard warns otherwise). `product-analytics` and `marketing-consumer-research` map to
themselves; `economics` to `economics-econometrics`; `policy-education` to `political-science-public-policy`,
`education-learning-sciences`; `demographic-social-science` to `sociology-demography`,
`survey-research-official-statistics`; `nonprofit-grant-making` to `political-science-public-policy`,
`general-statistics-data-science`; `supply-chain-logistics` to `urban-regional-science`,
`general-statistics-data-science`; `business-operations-analytics` to `general-statistics-data-science`,
`human-factors-ergonomics`, `healthcare-delivery-health-economics`; `accounting-audit-forensic` to
`banking-credit-financial-risk`, `actuarial-science-insurance`, `general-statistics-data-science`.

## Product analytics

### Product Analytics (`product-analytics`)

- `online-experimentation-a-b-test-design-readout`: EC
- `observational-causal-inference`: EC
- `metric-definition-measurement-science`: DD, DQ
- `retention-cohort-lifetime-value-modeling`: F
- `churn-propensity-uplift-modeling`: F, OS
- `funnel-journey-analysis`: DD, RC
- `network-effect-marketplace-experimentation`: EC
- `feature-adoption-diffusion-modeling`: F, DD

### Marketing & Consumer Research (`marketing-consumer-research`)

- `segmentation-market-structure`: DD
- `conjoint-choice-willingness-to-pay-analysis`: OS, F
- `brand-campaign-ad-effectiveness-measurement`: EC
- `customer-satisfaction-driver-analysis`: RC
- `media-reach-frequency-audience-measurement`: DD, F

## Quantitative finance and trading

### Quantitative Finance (`quantitative-finance`)

- `portfolio-construction-risk`: OS
- `factor-return-attribution`: RC
- `strategy-backtesting-evaluation`: F
- `market-microstructure-execution-cost`: DD
- `volatility-derivatives-pricing`: F
- `event-study`: EC

### Banking, Credit & Financial Risk (`banking-credit-financial-risk`)

- `credit-scoring-pd-modeling`: F
- `expected-credit-loss-provisioning`: F, OS
- `stress-testing-capital`: F
- `fraud-aml-detection`: AD
- `deposit-liquidity-behaviour`: F
- `collections-recovery`: OS

### Actuarial Science & Insurance (`actuarial-science-insurance`)

- `reserving-development-triangles`: F
- `pricing-ratemaking-credibility`: OS, F
- `mortality-longevity`: F
- `catastrophe-exposure-accumulation`: OS
- `claims-frequency-severity`: DD, F
- `reinsurance-capital`: OS

## Machine learning research

### General Statistics & Data Science (`general-statistics-data-science`)

- `exploratory-data-analysis-distribution-assessment`: DD, AD
- `regression-classification-model-diagnostics`: F
- `resampling-simulation-monte-carlo-methods`: F, DD
- `bayesian-modeling-posterior-inference`: F
- `missing-data-censoring-measurement-error`: DD, DQ
- `multiple-testing-selective-inference`: AD, EC
- `data-integration-record-linkage-entity-resolution`: ETL
- `benchmarking-and-ablations`: EC
- `scaling-laws`: F
- `robustness-analysis`: DD
- `interpretability`: RC

## Biomedical and health sciences

### Biomedical & Clinical Research (`biomedical-clinical-research`)

- `clinical-trial-design-analysis`: EC
- `survival-time-to-event-analysis`: F, DD
- `diagnostic-biomarker-accuracy`: DD
- `dose-response-pk-pd-modeling`: F
- `genomics-gwas-high-dimensional-association`: AD, DD
- `statistical-genomics`: DD
- `longitudinal-outcomes-repeated-measures`: EC
- `adaptive-platform-basket-trial-methods`: EC
- `real-world-evidence-comparative-effectiveness`: EC
- `medical-imaging-reader-study-evaluation`: DD

### Epidemiology & Public Health (`epidemiology-public-health`)

- `observational-study-design-cohort-case-control`: EC
- `disease-surveillance-outbreak-anomaly-detection`: AD, DQ
- `risk-factor-causal-effect-estimation`: EC
- `screening-diagnostic-policy-evaluation`: OS
- `health-burden-impact-modeling`: OS, F
- `infectious-disease-transmission-modeling`: F
- `cluster-stepped-wedge-community-trials`: EC
- `health-equity-disparity-decomposition`: RC

### Pharmacology, Pharmacoepidemiology & Safety (`pharmacology-pharmacoepidemiology-safety`)

- `population-pharmacokinetics-exposure-response`: F
- `drug-utilization-comparative-safety`: EC
- `safety-signal-detection`: AD
- `benefit-risk-assessment`: OS
- `medication-adherence-persistence`: DD

### Healthcare Delivery & Health Economics (`healthcare-delivery-health-economics`)

- `cost-effectiveness-decision-modeling`: OS
- `utilization-access-demand-forecasting`: F
- `provider-quality-risk-adjustment`: DD, AD
- `patient-flow-beds-workforce-optimization`: OS, F
- `payment-claims-health-plan-analytics`: ETL, AD

## Economics and quantitative social science

### Economics & Econometrics (`economics-econometrics`)

- `causal-identification-did-iv-rd-synthetic-control`: EC
- `structural-equilibrium-modeling`: OS
- `time-series-macro-econometrics`: F
- `panel-data-estimation`: EC, RC
- `elasticity-welfare-policy-impact-estimation`: OS
- `forecasting-forecast-evaluation`: F
- `discrete-choice-limited-dependent-variable-modeling`: F
- `spatial-econometrics-spillover-estimation`: EC

### Political Science & Public Policy (`political-science-public-policy`)

- `election-polling-forecasting`: F
- `policy-evaluation-administrative-data-inference`: EC
- `legislative-behavior-ideal-point-estimation`: DD
- `conflict-protest-event-data-analysis`: AD, DD
- `public-opinion-survey-experimentation`: EC
- `small-area-public-opinion-estimation-mrp`: DD

### Sociology & Demography (`sociology-demography`)

- `population-estimation-demographic-projection`: F
- `social-mobility-inequality-measurement`: DD
- `social-network-peer-effect-analysis`: EC
- `event-history-life-course-analysis`: DD, F
- `neighborhood-segregation-contextual-effects`: DD
- `fertility-mortality-life-table-estimation`: F, DD

### Psychology & Behavioral Science (`psychology-behavioral-science`)

- `experimental-design-power-analysis`: EC
- `psychometric-measurement-scale-validation`: DD, DQ
- `statistical-inference-hypothesis-testing`: EC
- `mediation-moderation-process-modeling`: RC
- `meta-analysis-evidence-synthesis`: EC
- `longitudinal-growth-curve-modeling`: DD
- `decision-making-computational-behavioral-modeling`: F
- `experience-sampling-intensive-longitudinal-analysis`: DD

### Criminology & Justice (`criminology-justice`)

- `crime-incidence-hotspot-analysis`: AD
- `recidivism-risk-assessment`: F
- `sentencing-bail-disparity-analysis`: RC
- `intervention-policing-policy-evaluation`: EC

## Engineering and physical sciences

### Physical & Environmental Sciences (`physical-environmental-sciences`)

- `environmental-monitoring-exceedance`: AD, DQ
- `climate-weather-extremes`: F
- `pollution-source-attribution`: RC
- `sensor-calibration-measurement`: DQ
- `hydrology-flood-frequency`: F
- `emissions-inventory`: ETL, DD

### Energy Systems & Utilities (`energy-systems-utilities`)

- `load-forecasting`: F
- `generation-capacity-planning`: OS
- `grid-reliability-outage-analysis`: RC, AD
- `tariff-demand-response-evaluation`: EC
- `asset-condition-maintenance`: F, OS
- `efficiency-savings-verification`: EC

### Human Factors & Ergonomics (`human-factors-ergonomics`)

- `usability-task-performance-studies`: EC
- `workload-fatigue-shift-analysis`: RC
- `safety-incident-error-analysis`: RC, AD
- `human-reliability-assessment`: F
- `anthropometric-design-fit`: DD
- `alarm-interface-evaluation`: EC

## Other

### Survey Research & Official Statistics (`survey-research-official-statistics`)

- `sample-design-allocation-weighting`: DD, OS
- `nonresponse-calibration-measurement-error-adjustment`: DD, DQ
- `questionnaire-mode-effects-research`: EC
- `small-area-estimation`: DD
- `census-register-administrative-data-quality`: DQ, ETL
- `seasonal-adjustment-official-time-series-production`: F, ETL
- `complex-survey-estimation-variance`: DD
- `anomaly-detection`: AD

### Urban & Regional Science (`urban-regional-science`)

- `land-use-spatial-development-modeling`: F
- `accessibility-agglomeration-location-analysis`: OS
- `municipal-service-demand-resource-allocation`: OS, F
- `regional-input-output-economic-impact`: OS
- `optimization`: OS
- `forecasting`: F
- `network-analysis`: DD

### Education & Learning Sciences (`education-learning-sciences`)

- `student-growth-value-added-modeling`: DD, EC
- `randomized-quasi-experimental-program-evaluation`: EC
- `item-response-theory-test-equating`: ETL, DD
- `learning-analytics-early-warning-models`: F
- `multilevel-classroom-school-research`: RC
- `psychometrics`: DD
- `text-analysis`: DD
