# The domain taxonomy

The client's taxonomy has seven groups and twenty-one domains. Each domain has its own task types, and every task type serves one or two of the eight Axis 1 objectives. A build picks **one domain and one task type in it** (the card's `domain` and `subdomain`) and **one Axis 1 objective** that task type serves. The Layer 2 rigor patterns for the task type are in `../../../stumping/references/client/layer2-rigor-patterns.md`, and the domain's Layer 1 messiness techniques are in `../../../dataset-generation/references/layer1-messiness.md`.

Six domains (Quantitative Finance; Banking, Credit & Financial Risk; Actuarial Science & Insurance; Physical & Environmental Sciences; Energy Systems & Utilities; Human Factors & Ergonomics) come with Layer 1 techniques but no Layer 2 patterns. Their task types below are drawn from the field. A build there takes its pitfall from the five Layer 2 families in `../../../stumping/references/client/two-layer-task-design.md`.

**The nine house domains** the earlier spec named stay valid, and every card already filed uses them. The guard warns when a new draw uses one, so the draw also names the client domain it sits in. The map: `product-analytics` to `product-analytics`; `marketing-consumer-research` to `marketing-consumer-research`; `economics` to `economics-econometrics`; `policy-education` to `political-science-public-policy`, `education-learning-sciences`; `demographic-social-science` to `sociology-demography`, `survey-research-official-statistics`; `nonprofit-grant-making` to `political-science-public-policy`, `general-statistics-data-science`; `supply-chain-logistics` to `urban-regional-science`, `general-statistics-data-science`; `business-operations-analytics` to `general-statistics-data-science`, `human-factors-ergonomics`, `healthcare-delivery-health-economics`; `accounting-audit-forensic` to `banking-credit-financial-risk`, `actuarial-science-insurance`, `general-statistics-data-science`.

## Product analytics

### Product Analytics (`product-analytics`)

- `online-experimentation-a-b-test-design-readout`: Online experimentation (A/B test design & readout). Objectives: Experiment & Causal
- `observational-causal-inference`: Observational causal inference. Objectives: Experiment & Causal
- `metric-definition-measurement-science`: Metric definition & measurement science. Objectives: Descriptive & Distribution, Data Quality Monitoring
- `retention-cohort-lifetime-value-modeling`: Retention, cohort & lifetime-value modeling. Objectives: Forecasting
- `churn-propensity-uplift-modeling`: Churn, propensity & uplift modeling. Objectives: Forecasting, Opportunity Sizing
- `funnel-journey-analysis`: Funnel & journey analysis. Objectives: Descriptive & Distribution, Root-Cause
- `network-effect-marketplace-experimentation`: Network-effect & marketplace experimentation. Objectives: Experiment & Causal
- `feature-adoption-diffusion-modeling`: Feature adoption & diffusion modeling. Objectives: Forecasting, Descriptive & Distribution

### Marketing & Consumer Research (`marketing-consumer-research`)

- `segmentation-market-structure`: Segmentation & market structure. Objectives: Descriptive & Distribution
- `conjoint-choice-willingness-to-pay-analysis`: Conjoint, choice & willingness-to-pay analysis. Objectives: Opportunity Sizing, Forecasting
- `brand-campaign-ad-effectiveness-measurement`: Brand, campaign & ad-effectiveness measurement. Objectives: Experiment & Causal
- `customer-satisfaction-driver-analysis`: Customer satisfaction & driver analysis. Objectives: Root-Cause
- `media-reach-frequency-audience-measurement`: Media reach, frequency & audience measurement. Objectives: Descriptive & Distribution, Forecasting

## Quantitative finance and trading

### Quantitative Finance (`quantitative-finance`)

- `portfolio-construction-risk`: Portfolio construction risk. Objectives: Opportunity Sizing
- `factor-return-attribution`: Factor return attribution. Objectives: Root-Cause
- `strategy-backtesting-evaluation`: Strategy backtesting evaluation. Objectives: Forecasting
- `market-microstructure-execution-cost`: Market microstructure execution cost. Objectives: Descriptive & Distribution
- `volatility-derivatives-pricing`: Volatility derivatives pricing. Objectives: Forecasting
- `event-study`: Event study. Objectives: Experiment & Causal

### Banking, Credit & Financial Risk (`banking-credit-financial-risk`)

- `credit-scoring-pd-modeling`: Credit scoring pd modeling. Objectives: Forecasting
- `expected-credit-loss-provisioning`: Expected credit loss provisioning. Objectives: Forecasting, Opportunity Sizing
- `stress-testing-capital`: Stress testing capital. Objectives: Forecasting
- `fraud-aml-detection`: Fraud aml detection. Objectives: Anomaly Detection
- `deposit-liquidity-behaviour`: Deposit liquidity behaviour. Objectives: Forecasting
- `collections-recovery`: Collections recovery. Objectives: Opportunity Sizing

### Actuarial Science & Insurance (`actuarial-science-insurance`)

- `reserving-development-triangles`: Reserving development triangles. Objectives: Forecasting
- `pricing-ratemaking-credibility`: Pricing ratemaking credibility. Objectives: Opportunity Sizing, Forecasting
- `mortality-longevity`: Mortality longevity. Objectives: Forecasting
- `catastrophe-exposure-accumulation`: Catastrophe exposure accumulation. Objectives: Opportunity Sizing
- `claims-frequency-severity`: Claims frequency severity. Objectives: Descriptive & Distribution, Forecasting
- `reinsurance-capital`: Reinsurance capital. Objectives: Opportunity Sizing

## Machine learning research

### General Statistics & Data Science (`general-statistics-data-science`)

- `exploratory-data-analysis-distribution-assessment`: Exploratory data analysis & distribution assessment. Objectives: Descriptive & Distribution, Anomaly Detection
- `regression-classification-model-diagnostics`: Regression, classification & model diagnostics. Objectives: Forecasting
- `resampling-simulation-monte-carlo-methods`: Resampling, simulation & Monte Carlo methods. Objectives: Forecasting, Descriptive & Distribution
- `bayesian-modeling-posterior-inference`: Bayesian modeling & posterior inference. Objectives: Forecasting
- `missing-data-censoring-measurement-error`: Missing data, censoring & measurement error. Objectives: Descriptive & Distribution, Data Quality Monitoring
- `multiple-testing-selective-inference`: Multiple testing & selective inference. Objectives: Anomaly Detection, Experiment & Causal
- `data-integration-record-linkage-entity-resolution`: Data integration, record linkage & entity resolution. Objectives: ETL
- `benchmarking-and-ablations`: Benchmarking and ablations. Objectives: Experiment & Causal
- `scaling-laws`: Scaling laws. Objectives: Forecasting
- `robustness-analysis`: Robustness analysis. Objectives: Descriptive & Distribution
- `interpretability`: Interpretability. Objectives: Root-Cause

## Biomedical and health sciences

### Biomedical & Clinical Research (`biomedical-clinical-research`)

- `clinical-trial-design-analysis`: Clinical trial design & analysis. Objectives: Experiment & Causal
- `survival-time-to-event-analysis`: Survival / time-to-event analysis. Objectives: Forecasting, Descriptive & Distribution
- `diagnostic-biomarker-accuracy`: Diagnostic & biomarker accuracy. Objectives: Descriptive & Distribution
- `dose-response-pk-pd-modeling`: Dose-response & PK/PD modeling. Objectives: Forecasting
- `genomics-gwas-high-dimensional-association`: Genomics / GWAS & high-dimensional association. Objectives: Anomaly Detection, Descriptive & Distribution
- `statistical-genomics`: Statistical genomics. Objectives: Descriptive & Distribution
- `longitudinal-outcomes-repeated-measures`: Longitudinal outcomes & repeated measures. Objectives: Experiment & Causal
- `adaptive-platform-basket-trial-methods`: Adaptive, platform & basket trial methods. Objectives: Experiment & Causal
- `real-world-evidence-comparative-effectiveness`: Real-world evidence & comparative effectiveness. Objectives: Experiment & Causal
- `medical-imaging-reader-study-evaluation`: Medical imaging & reader-study evaluation. Objectives: Descriptive & Distribution

### Epidemiology & Public Health (`epidemiology-public-health`)

- `observational-study-design-cohort-case-control`: Observational study design (cohort / case-control). Objectives: Experiment & Causal
- `disease-surveillance-outbreak-anomaly-detection`: Disease surveillance & outbreak / anomaly detection. Objectives: Anomaly Detection, Data Quality Monitoring
- `risk-factor-causal-effect-estimation`: Risk-factor & causal effect estimation. Objectives: Experiment & Causal
- `screening-diagnostic-policy-evaluation`: Screening & diagnostic-policy evaluation. Objectives: Opportunity Sizing
- `health-burden-impact-modeling`: Health-burden & impact modeling. Objectives: Opportunity Sizing, Forecasting
- `infectious-disease-transmission-modeling`: Infectious-disease transmission modeling. Objectives: Forecasting
- `cluster-stepped-wedge-community-trials`: Cluster, stepped-wedge & community trials. Objectives: Experiment & Causal
- `health-equity-disparity-decomposition`: Health equity & disparity decomposition. Objectives: Root-Cause

### Pharmacology, Pharmacoepidemiology & Safety (`pharmacology-pharmacoepidemiology-safety`)

- `population-pharmacokinetics-exposure-response`: Population pharmacokinetics & exposure response. Objectives: Forecasting
- `drug-utilization-comparative-safety`: Drug utilization & comparative safety. Objectives: Experiment & Causal
- `safety-signal-detection`: Safety-signal detection. Objectives: Anomaly Detection
- `benefit-risk-assessment`: Benefit-risk assessment. Objectives: Opportunity Sizing
- `medication-adherence-persistence`: Medication adherence & persistence. Objectives: Descriptive & Distribution

### Healthcare Delivery & Health Economics (`healthcare-delivery-health-economics`)

- `cost-effectiveness-decision-modeling`: Cost-effectiveness & decision modeling. Objectives: Opportunity Sizing
- `utilization-access-demand-forecasting`: Utilization, access & demand forecasting. Objectives: Forecasting
- `provider-quality-risk-adjustment`: Provider quality & risk adjustment. Objectives: Descriptive & Distribution, Anomaly Detection
- `patient-flow-beds-workforce-optimization`: Patient flow, beds & workforce optimization. Objectives: Opportunity Sizing, Forecasting
- `payment-claims-health-plan-analytics`: Payment, claims & health-plan analytics. Objectives: ETL, Anomaly Detection

## Economics and quantitative social science

### Economics & Econometrics (`economics-econometrics`)

- `causal-identification-did-iv-rd-synthetic-control`: Causal identification (DiD / IV / RD / synthetic control). Objectives: Experiment & Causal
- `structural-equilibrium-modeling`: Structural / equilibrium modeling. Objectives: Opportunity Sizing
- `time-series-macro-econometrics`: Time-series & macro-econometrics. Objectives: Forecasting
- `panel-data-estimation`: Panel-data estimation. Objectives: Experiment & Causal, Root-Cause
- `elasticity-welfare-policy-impact-estimation`: Elasticity & welfare / policy-impact estimation. Objectives: Opportunity Sizing
- `forecasting-forecast-evaluation`: Forecasting & forecast evaluation. Objectives: Forecasting
- `discrete-choice-limited-dependent-variable-modeling`: Discrete-choice & limited-dependent-variable modeling. Objectives: Forecasting
- `spatial-econometrics-spillover-estimation`: Spatial econometrics & spillover estimation. Objectives: Experiment & Causal

### Political Science & Public Policy (`political-science-public-policy`)

- `election-polling-forecasting`: Election polling & forecasting. Objectives: Forecasting
- `policy-evaluation-administrative-data-inference`: Policy evaluation & administrative-data inference. Objectives: Experiment & Causal
- `legislative-behavior-ideal-point-estimation`: Legislative behavior & ideal-point estimation. Objectives: Descriptive & Distribution
- `conflict-protest-event-data-analysis`: Conflict, protest & event-data analysis. Objectives: Anomaly Detection, Descriptive & Distribution
- `public-opinion-survey-experimentation`: Public opinion & survey experimentation. Objectives: Experiment & Causal
- `small-area-public-opinion-estimation-mrp`: Small-area public-opinion estimation & MRP. Objectives: Descriptive & Distribution

### Sociology & Demography (`sociology-demography`)

- `population-estimation-demographic-projection`: Population estimation & demographic projection. Objectives: Forecasting
- `social-mobility-inequality-measurement`: Social mobility & inequality measurement. Objectives: Descriptive & Distribution
- `social-network-peer-effect-analysis`: Social network & peer-effect analysis. Objectives: Experiment & Causal
- `event-history-life-course-analysis`: Event-history & life-course analysis. Objectives: Descriptive & Distribution, Forecasting
- `neighborhood-segregation-contextual-effects`: Neighborhood, segregation & contextual effects. Objectives: Descriptive & Distribution
- `fertility-mortality-life-table-estimation`: Fertility, mortality & life-table estimation. Objectives: Forecasting, Descriptive & Distribution

### Psychology & Behavioral Science (`psychology-behavioral-science`)

- `experimental-design-power-analysis`: Experimental design & power analysis. Objectives: Experiment & Causal
- `psychometric-measurement-scale-validation`: Psychometric measurement & scale validation. Objectives: Descriptive & Distribution, Data Quality Monitoring
- `statistical-inference-hypothesis-testing`: Statistical inference & hypothesis testing. Objectives: Experiment & Causal
- `mediation-moderation-process-modeling`: Mediation, moderation & process modeling. Objectives: Root-Cause
- `meta-analysis-evidence-synthesis`: Meta-analysis & evidence synthesis. Objectives: Experiment & Causal
- `longitudinal-growth-curve-modeling`: Longitudinal & growth-curve modeling. Objectives: Descriptive & Distribution
- `decision-making-computational-behavioral-modeling`: Decision-making & computational behavioral modeling. Objectives: Forecasting
- `experience-sampling-intensive-longitudinal-analysis`: Experience sampling & intensive longitudinal analysis. Objectives: Descriptive & Distribution

### Criminology & Justice (`criminology-justice`)

- `crime-incidence-hotspot-analysis`: Crime incidence & hotspot analysis. Objectives: Anomaly Detection
- `recidivism-risk-assessment`: Recidivism & risk assessment. Objectives: Forecasting
- `sentencing-bail-disparity-analysis`: Sentencing, bail & disparity analysis. Objectives: Root-Cause
- `intervention-policing-policy-evaluation`: Intervention & policing-policy evaluation. Objectives: Experiment & Causal

## Engineering and physical sciences

### Physical & Environmental Sciences (`physical-environmental-sciences`)

- `environmental-monitoring-exceedance`: Environmental monitoring exceedance. Objectives: Anomaly Detection, Data Quality Monitoring
- `climate-weather-extremes`: Climate weather extremes. Objectives: Forecasting
- `pollution-source-attribution`: Pollution source attribution. Objectives: Root-Cause
- `sensor-calibration-measurement`: Sensor calibration measurement. Objectives: Data Quality Monitoring
- `hydrology-flood-frequency`: Hydrology flood frequency. Objectives: Forecasting
- `emissions-inventory`: Emissions inventory. Objectives: ETL, Descriptive & Distribution

### Energy Systems & Utilities (`energy-systems-utilities`)

- `load-forecasting`: Load forecasting. Objectives: Forecasting
- `generation-capacity-planning`: Generation capacity planning. Objectives: Opportunity Sizing
- `grid-reliability-outage-analysis`: Grid reliability outage analysis. Objectives: Root-Cause, Anomaly Detection
- `tariff-demand-response-evaluation`: Tariff demand response evaluation. Objectives: Experiment & Causal
- `asset-condition-maintenance`: Asset condition maintenance. Objectives: Forecasting, Opportunity Sizing
- `efficiency-savings-verification`: Efficiency savings verification. Objectives: Experiment & Causal

### Human Factors & Ergonomics (`human-factors-ergonomics`)

- `usability-task-performance-studies`: Usability task performance studies. Objectives: Experiment & Causal
- `workload-fatigue-shift-analysis`: Workload fatigue shift analysis. Objectives: Root-Cause
- `safety-incident-error-analysis`: Safety incident error analysis. Objectives: Root-Cause, Anomaly Detection
- `human-reliability-assessment`: Human reliability assessment. Objectives: Forecasting
- `anthropometric-design-fit`: Anthropometric design fit. Objectives: Descriptive & Distribution
- `alarm-interface-evaluation`: Alarm interface evaluation. Objectives: Experiment & Causal

## Other

### Survey Research & Official Statistics (`survey-research-official-statistics`)

- `sample-design-allocation-weighting`: Sample design, allocation & weighting. Objectives: Descriptive & Distribution, Opportunity Sizing
- `nonresponse-calibration-measurement-error-adjustment`: Nonresponse, calibration & measurement-error adjustment. Objectives: Descriptive & Distribution, Data Quality Monitoring
- `questionnaire-mode-effects-research`: Questionnaire & mode-effects research. Objectives: Experiment & Causal
- `small-area-estimation`: Small-area estimation. Objectives: Descriptive & Distribution
- `census-register-administrative-data-quality`: Census, register & administrative-data quality. Objectives: Data Quality Monitoring, ETL
- `seasonal-adjustment-official-time-series-production`: Seasonal adjustment & official time-series production. Objectives: Forecasting, ETL
- `complex-survey-estimation-variance`: Complex-survey estimation & variance. Objectives: Descriptive & Distribution
- `anomaly-detection`: Anomaly detection. Objectives: Anomaly Detection

### Urban & Regional Science (`urban-regional-science`)

- `land-use-spatial-development-modeling`: Land-use & spatial-development modeling. Objectives: Forecasting
- `accessibility-agglomeration-location-analysis`: Accessibility, agglomeration & location analysis. Objectives: Opportunity Sizing
- `municipal-service-demand-resource-allocation`: Municipal service-demand & resource allocation. Objectives: Opportunity Sizing, Forecasting
- `regional-input-output-economic-impact`: Regional input-output & economic impact. Objectives: Opportunity Sizing
- `optimization`: Optimization. Objectives: Opportunity Sizing
- `forecasting`: Forecasting. Objectives: Forecasting
- `network-analysis`: Network analysis. Objectives: Descriptive & Distribution

### Education & Learning Sciences (`education-learning-sciences`)

- `student-growth-value-added-modeling`: Student growth & value-added modeling. Objectives: Descriptive & Distribution, Experiment & Causal
- `randomized-quasi-experimental-program-evaluation`: Randomized & quasi-experimental program evaluation. Objectives: Experiment & Causal
- `item-response-theory-test-equating`: Item response theory & test equating. Objectives: ETL, Descriptive & Distribution
- `learning-analytics-early-warning-models`: Learning analytics & early-warning models. Objectives: Forecasting
- `multilevel-classroom-school-research`: Multilevel classroom & school research. Objectives: Root-Cause
- `psychometrics`: Psychometrics. Objectives: Descriptive & Distribution
- `text-analysis`: Text analysis. Objectives: Descriptive & Distribution
