# Types of Tasks

> **DOMAIN UPDATE (2026-08-27), OPERATIVE: Axis 0 carries six accepted domains.** The client's
> 2026-08-27 example-prompts page lists six accepted domains and drops **Biology, Biostatistics,
> Epidemiology & Bioinformatics** from the roster: Product Analytics · Supply Chain & Logistics ·
> Economics · Policy & Education · Demographic & Social Science · Nonprofit & Grant-making. Do
> not start a new build in Biology. References to "seven domains" below this block predate the
> change and are retained for reference.

> **Axis 1 carries six objectives, and the cut applies to every domain.**
>
> **Forecasting & Predictive Modeling** (the one most wanted) · **Root-Cause Analysis** ·
> **Anomaly Detection & Diagnostics** · **Experiment & Causal Analysis** · **Descriptive &
> Distribution Analysis** · **Data Extraction & Conformation (ETL / Pipeline Build)**.
>
> Nothing else is a valid tag. A task tagged outside the six is rejected on the tag alone.
>
> The six cover more than their names suggest. A like-for-like comparison, a binding constraint, a
> sizing exercise and a monitoring rule can each be the substance of a task, they just sit under one
> of the six. A comparison that names a driver is Root-Cause Analysis, one that separates an event
> from an artifact is Anomaly Detection, and a sizing exercise whose answer is a projected quantity
> is Forecasting.

**How do I classify my task?** Every task is tagged on three axes, inside one of seven domains. Tag before you write the prompt.

Task classification runs on three axes:

- **Axis 0: Domain**
- **Axis 1: Analytical objective**
- **Axis 2: Reasoning phase**

## Required Rules

- **Stay in scope.** One of the seven domains below. Anything outside them does not qualify, even if the data is excellent.
- **Use the canonical labels.** Domain and objective names come straight from the taxonomy below. Do not rename them and do not invent new ones.
- **Tag every axis.** Domain, analytical objective, and reasoning phase. A task missing a tag cannot be routed or reviewed.
- **One objective per task.** If two objectives fit equally, the decision is probably not deterministic yet. Split the task or sharpen the ask. See Writing the prompt for determinism.
- **Match the tags to the files.** The evidence in your input package has to support the objective you tagged, not a neighbouring one. See Sourcing for workspace complexity.
- **Ask before stretching the scope.** If you think your task is in scope but cannot map it to a domain below, message a Project Lead rather than guessing.

---

## Axis 0: Domain

Project Mark accepts tasks in seven domains. Your task must sit in exactly one.

| Domain | Typical decisions | Typical data |
| --- | --- | --- |
| Product Analytics | Growth, activation, retention, monetization, experimentation calls at a digital product company | Event logs, funnels, experiment results, billing/usage tables |
| Supply Chain & Logistics | Inventory, sourcing, routing, fulfillment decisions | Shipment, inventory, carrier, and procurement records |
| Economics | Labor, price, output, or trade reads and forecasts | Payroll, CPI/PPI, GDP, trade, and monetary series |
| Policy & Education | Program evaluation, enrollment, attainment, public-program outcomes | Administrative, enrollment, and survey data |
| Demographic & Social Science | Population structure, migration, housing, social outcomes | Census, survey, and administrative extracts |
| Nonprofit & Grant-making | Grant portfolios, grantee health, funding gaps, giving strategy | Award data, 990 filings, program budgets |
| Biology, Biostatistics, Epidemiology & Bioinformatics | Experimental, clinical-population, or omics analysis with quantitative methods | Assay, cohort, sequencing, and surveillance data |

### Product Analytics

- **Acquisition & growth:** channels, campaigns, signups, referral loops; marketing attribution (CAC, LTV:CAC); organic and content growth (SEO, virality)
- **Onboarding & activation:** the "aha" moment, time-to-value, first-key-action completion; signup, checkout, and multi-step funnels
- **Engagement & retention:** Dn retention, stickiness (DAU/MAU), resurrection; feature adoption and depth; lifecycle messaging; search, ranking and recommendations; session quality
- **Monetization & subscriptions:** MRR/ARR, ARPU, net and gross revenue retention; pricing and packaging; usage-based billing; free-to-paid and PLG conversion
- **Retention risk:** voluntary and involuntary churn, leading indicators, cohort-level drivers
- **Trust, safety & support:** payment fraud and chargebacks; abuse, spam and content integrity; support and CX (deflection, CSAT/NPS)
- **Experimentation & measurement:** A/B testing (lift, guardrails, sample-ratio checks); metric diagnosis; metric definition and goaling; segmentation and personas; instrumentation and data quality
- **Other:** anything else that fits product analytics, as long as it stays in scope

### Supply Chain & Logistics

- **Inventory & demand planning:** demand and shipment forecasting, replenishment, safety stock; stockouts, fill rate; lead-time variability
- **Sourcing & procurement flow:** supplier selection, single vs dual-sourcing, allocation; landed cost and supplier scorecards
- **Transportation & network:** routing, carrier on-time performance; distribution-network and lane design
- **Trade & flows:** imports and exports by commodity, exposure and concentration; port and border performance
- **Fulfillment & warehousing:** pick/pack productivity, dock-to-stock, distribution-center performance
- **Other:** anything else about the movement, flow, or handling of physical goods

### Economics

- **Labor markets:** payrolls, unemployment, participation, job openings; wages and occupational pay
- **Prices & inflation:** CPI, PPI, cost of living, inflation decomposition
- **Output & activity:** GDP by industry or state, industrial production, business dynamics
- **Trade & international economics:** trade balances and flows, terms of trade, external exposure
- **Public finance:** federal and state spending, tax statistics, deficits
- **Money & credit:** monetary and credit aggregates, forecasting an economic indicator
- **Other:** other macro, labor, trade, or fiscal reads (corporate finance, markets trading, and lending underwriting are out of scope)

### Policy & Education

- **Enrollment & attainment:** enrollment trends, completions, degree attainment, admissions
- **Institutional finance & aid:** institutional finances, faculty, student aid, cost and debt
- **K-12 outcomes:** proficiency, achievement gaps, school and district performance
- **Program evaluation:** the effect of a policy or program on outcomes, net of composition
- **Public administration:** public-program outcomes grounded in administrative or survey data
- **Other:** other public-policy or education-system questions answered with real administrative or survey data

### Demographic & Social Science

- **Population structure:** age, sex and race composition, fertility, household structure
- **Migration & mobility:** net migration, movers, geographic and residential mobility
- **Income, poverty & inequality:** income distribution, poverty, inequality across groups
- **Housing:** ownership vs rent, cost burden, permits, commuting
- **Population health & social statistics:** mortality, natality, prevalence, behavioral risk factors, social vulnerability
- **Crime & social surveys:** crime, time-use, and other social-survey analysis
- **Other:** other population or social-condition questions from census, survey, or administrative data (individual clinical care is out of scope)

> **Boundary note:** keep work here when the focus is population characteristics or social conditions from census, survey, or administrative data. Studies centred on biological mechanisms, biomedical study data, epidemiologic exposure and outcome modelling, genetics and genomics, or bioinformatics belong under Biology, Biostatistics, Epidemiology & Bioinformatics.

### Nonprofit & Grant-making

- **Grant & award portfolios:** who is funded, how much, by program, agency, or geography
- **Grantee financial health:** 990/990-PF/990-EZ filings, revenue, assets, program vs expense linkage
- **Funding gaps & landscape:** where funding is thin across a sector or region
- **Giving strategy & program funding:** foundation and agency giving strategy, alignment of awards to stated priorities
- **Other:** other questions about the funding of programs or research using grants, awards, or funding portfolios

### Biology, Biostatistics, Epidemiology & Bioinformatics

- **Experimental & molecular biology:** gene and protein expression, assays, phenotypes, pathways, dose-response, experimental comparisons
- **Biostatistics:** statistical analysis of biological or biomedical studies, effect estimation, uncertainty, survival and time-to-event analysis, repeated measures, multivariable modelling
- **Epidemiology:** incidence, prevalence, risk factors, exposures, outcomes, cohort and case-control analysis, outbreak or population-health analysis
- **Genetics & genomics:** variants, genotype and phenotype relationships, sequencing-derived measurements, genomic QC, population genetics
- **Bioinformatics:** sequence, expression, omics, annotation, pathway, feature, and computational biology analyses
- **Predictive biological modelling:** risk prediction, outcome prediction, classification, biomarker models, or forecasting when the data supports it
- **Other:** other quantitative biological, biostatistical, epidemiological, or bioinformatics analyses that meet the project's analytical requirements (individual diagnosis, treatment decisions, and hospital operations are out of scope)

Open a domain above to see the areas it covers. These lists are a browsing aid, not a closed set, so be creative, and message a Project Lead if your task does not map cleanly.

Each domain also has its own file in `.claude/skills/guide-to-prompt/references/domains/`, carrying the same subdomain list plus every canonical example ask in that domain, so you can load one domain instead of the whole taxonomy.

### Two boundaries that decide close calls

| Question | Answer |
| --- | --- |
| Demographic & Social Science or Biology? | Stay in Demographic & Social Science for population characteristics or social conditions from census, survey, or administrative data. Move to Biology when the study centres on biological mechanisms, biomedical study data, epidemiologic exposure and outcome modelling, genetics, genomics, or bioinformatics. |
| What counts as Economics? | In scope: macro, labor, trade, and fiscal reads. Out of scope: corporate finance, markets trading, and lending underwriting. |

---

## Axis 1: Analytical Objective

**Reference:** what the task asks the analyst to produce. The same six objectives apply across all seven domains. Pick exactly one objective per task.

> **Especially encouraged: Forecasting & Predictive Modeling**
>
> Project Mark is currently looking for more high-quality tasks centred on Forecasting & Predictive Modeling. It is an **objective, not an eighth domain**: any accepted domain can carry it when the supplied evidence pins the answer down. This is an encouraged direction, not a requirement for every task, so only take it when the data and domain genuinely support it.

> **Where the example asks live.** The taxonomy publishes **eighteen canonical example asks per objective**, 162 in total, and they are mirrored into `.claude/skills/guide-to-prompt/references/`, sliced by objective and by domain so you load one file rather than the whole corpus. Each one is a **Main Recommendation Ask only**, so the prompt you ship still adds the context, the deliverable request, the numbered related questions, and the golden solution.
>

| Objective | One-line definition |
| --- | --- |
| Descriptive & Distribution Analysis | Characterize a population, cohort, or distribution and what its shape implies. |
| Anomaly Detection & Diagnostics | Find and validate whether a spike, drop, or outlier is real. |
| Root-Cause Analysis | Name the driver of a metric move, with rival explanations ruled out on evidence. |
| Experiment & Causal Analysis | Design, read out, or validate a causal claim from experimental or observational data. |
| Forecasting & Predictive Modeling (especially encouraged) | Predict a future value, risk, or outcome with a defensible, deterministic method. |
| Data Extraction & Conformation (ETL / Pipeline Build) | Build a clean, analysis-ready dataset from messy multi-source inputs. |

Open an objective below for its full shape: example prompts and the key questions that make each one deterministic.

### Descriptive & Distribution Analysis

#### Segmentation & cohort analysis

> **Example prompt:** Segment customers into cohorts by signup month and show how retention varies across cohorts over time.

**Key questions:**

- Cohort anchor (signup vs first purchase)?
- Retention definition (any activity vs purchase)?
- Period granularity?
- How to handle partial/most-recent cohorts?

#### Distribution shape & implications

> **Example prompt:** Examine the distribution of customer lifetime value in this dataset. Is it skewed, heavy-tailed, or multimodal? Identify any hidden sub-populations and explain what the shape implies.

**Key questions:**

- Which metric and population are in scope?
- How will you detect multimodality or sub-populations (density, clustering, mixture models)?
- How to handle outliers and the heavy tail?
- Is a log or other transform appropriate?
- Mean vs median given the skew?
- What decision does the shape inform?

### Anomaly Detection & Diagnostics

#### Spike / drop detection & diagnosis

> **Example prompt:** A key daily metric dropped sharply on one day. Detect the anomaly, quantify its magnitude versus the expected baseline, and determine whether it is a real change or a data artifact.

**Key questions:**

- What is the expected baseline (trailing average, seasonal)?
- What threshold counts as an anomaly?
- Is the drop a data gap or real?
- Any reporting lag or timezone effect?

#### Outlier detection & signal-vs-artifact validation

> **Example prompt:** Some values in this dataset look extreme. Identify the genuine outliers, and determine for each whether it reflects a real event or a data error.

**Key questions:**

- How are outliers defined (statistical vs domain rule)?
- Real event or artifact, what evidence distinguishes them?
- Global vs per-segment thresholds?
- What action (keep, cap, exclude, investigate)?

#### Segment-level anomaly localization

> **Example prompt:** Overall revenue looks flat but something feels off, find which segment(s) have anomalous behavior.

**Also fits:** a sequencing QC metric shifting on one run batch, a lane or port disruption inside a shipment file, a case-count spike in one county, or a break in an economic series.

**Key questions:**

- Which dimensions to scan?
- Minimum segment size to consider?
- How to rank anomalies (impact vs deviation)?
- What baseline per segment?

### Root-Cause Analysis

#### Metric-movement decomposition

> **Example prompt:** Total revenue fell 8% week-over-week. Decompose the change by region, product, and price vs volume to find the main driver.

**Key questions:**

- How is revenue defined?
- Which dimensions to decompose?
- Additive or multiplicative decomposition?
- How to handle mix shifts and interaction terms?

#### Driver / contribution analysis

> **Example prompt:** Which factors explain the increase in customer churn last month? Rank the likely drivers with supporting evidence.

**Key questions:**

- Churn definition and window?
- Which candidate drivers exist in the data?
- Correlation vs causation expectations?
- What controls are needed?

#### Breakage & degradation diagnosis

> **Example prompt:** A KPI flatlined at zero after a certain date. Diagnose whether it is a real change, a logging break, or a pipeline issue.

**Also fits:** a delivery-time regression on one carrier lane, an assay reading that drifts after a reagent change, or a programme outcome that moves right after an eligibility rule changes.

**Key questions:**

- What changed around that date (schema, source, code)?
- Is upstream data present?
- Is the grain as expected?
- Are related metrics also affected?

#### Hypothesis-driven 'why' investigation

> **Example prompt:** Conversion dropped. Form competing hypotheses, test each against the data, and rule out the ones not supported.

**Key questions:**

- What are plausible hypotheses given context?
- What evidence would confirm or refute each?
- What data is needed to test them?
- Have we avoided stopping at the first plausible cause?

### Experiment & Causal Analysis

#### Experiment design

> **Example prompt:** We want to test whether a new checkout flow increases conversion. Design the experiment, define the success metric and guardrails, the randomization unit, and how long to run it / how many users we need.

**Key questions:**

- What is the primary metric and the minimum effect (MDE) worth detecting?
- Randomization unit (user / session / cluster)?
- Baseline rate and variance → required sample size and duration?
- Significance level and power?
- One- or two-sided?
- Guardrail metrics?
- Interference / network effects (cluster or switchback)?
- Ramp, peeking, and multiple-comparison plan?

#### A/B test readout & interpretation

> **Example prompt:** Given control vs treatment results (conversions and n per arm), is the lift statistically significant? Report effect size and confidence interval.

**Key questions:**

- What is the primary metric and randomization unit?
- Sample size per arm?
- One- or two-sided test?
- Significance level?
- Multiple-comparison correction?

#### Experiment validity & guardrail checks

> **Example prompt:** Check this experiment for sample-ratio mismatch, novelty effects, and guardrail-metric regressions before trusting the result.

**Key questions:**

- What split was expected vs observed?
- Is the pre-period balanced?
- Which guardrail metrics matter?
- What was the duration and ramp schedule?

#### Causal inference from observational data

> **Example prompt:** We cannot run an A/B test. Estimate the effect of a feature on retention using observational data, addressing confounders.

**Also fits:** a policy intervention, an education programme rollout, or a controlled biological experiment where assignment was not random.

**Key questions:**

- What are the treatment and outcome?
- Which confounders are observable?
- Is a natural experiment / diff-in-diff / matching feasible?
- What assumptions must hold?

#### Heterogeneous / segment effects

> **Example prompt:** Did the treatment effect differ by user segment? Identify where the effect is strongest.

**Key questions:**

- Which segments are prespecified vs exploratory?
- Sample size per segment?
- Multiple-testing correction?
- Is an interaction test expected?

### Forecasting & Predictive Modeling

> **Especially encouraged:** Project Mark wants more strong tasks here. A strong one asks for more than fitting a standard model and reporting a metric. The analyst should have to make defensible choices about target definition, feature construction, leakage, training and validation windows, time-aware splits, class imbalance, missingness, model comparison, calibration, evaluation metrics, uncertainty, and how a prediction becomes a deterministic recommendation. These are examples of what can make a task hard, not a recipe to follow.

#### Time-series forecasting

> **Example prompt:** Forecast the next 12 weeks of shipment demand from this weekly history, with seasonality and a confidence interval.

**Key questions:**

- What horizon and granularity?
- Is there seasonality or holiday effects?
- Recent trend changes?
- Acceptable error metric?
- Are prediction intervals required?

#### Predictive / propensity modeling

> **Example prompt:** Build a model to predict which customers will churn next month from this feature table; report key drivers and performance.

**Key questions:**

- Label definition and window?
- Time-based train/test split?
- Class imbalance handling?
- Target metric (AUC, recall)?
- Interpretability requirements?

#### Cross-domain prediction & risk classification

> **Example prompt:** From this cohort file plus the lab-assay and covariate tables, predict which participants are at elevated risk of the study outcome and recommend the cut-off the programme should use.

**Other shapes that fit:** economic indicator forecasting, enrolment or programme-demand forecasting, demographic projections, grant demand or award-outcome prediction, epidemiological outcome prediction, and biomarker or risk-score classification.

**Key questions:**

- Is the outcome defined identically across every source file?
- Which split respects time or cohort structure?
- How are missing measurements and rare positives handled?
- Is the model calibrated well enough to set a threshold?
- What decision does the prediction force?

#### What-if / scenario projection

> **Example prompt:** If we increase price by 5%, project the impact on revenue given historical price elasticity.

**Key questions:**

- Where does the elasticity estimate come from?
- What is held constant?
- What scenario range?
- Confidence bounds?
- Time horizon?

### Data Extraction & Conformation (ETL / Pipeline Build)

#### End-to-end warehouse / dataset build from messy multi-source inputs

> **Example prompt:** Build a cleaned, analysis-ready warehouse from these messy multi-format source files (CSV/JSON/TSV), conforming to the target schema, and load the final tables.

**Key questions:**

- Which source is authoritative when records conflict?
- How are duplicate and late-arriving records handled?
- Full rebuild or incremental load?
- What is the grain of each output table?
- Where must the deliverables be written (paths / contract)?

#### Schema / contract-driven conformation & migration

> **Example prompt:** Conform this source dataset to the provided target schema and output contract, exact tables, column names, types, and required deliverables.

**Key questions:**

- What are the exact required fields, types, and output paths?
- Are extra columns allowed?
- How should optional or missing fields be filled?
- What happens to records that violate the target types?
- How is conformance verified?

#### Entity resolution & deduplication across sources

> **Example prompt:** Reconcile and deduplicate customer records spread across these sources, producing one canonical record per entity.

**Key questions:**

- Which fields identify an entity (exact vs fuzzy match)?
- What match threshold?
- Which source wins on conflicting attributes?
- How to handle one-to-many and ambiguous matches?
- How to measure match precision/recall?

## Axis 2: Analytical Reasoning Phase

The steps of the reasoning loop the task exercises. Ideally, tag all five. Skipping a phase is fine when it does not fit, but if you are skipping three, the task is probably too narrow. Your rubric criteria get tagged with Axis 2.

> Tasks that only exercise the last two phases are memorization tests, not analytical intelligence tests.

**Example:** a churn-diagnosis task that hands over raw event logs exercises every reasoning phase, because the analyst has to find and profile the data before any hypothesis is testable.

1. **Explore / Discover.** Find, understand, and confirm the right data before analyzing. Discover sources, profile schema and quality, resolve entities and joinability, and pin down metric definitions.
2. **Hypothesize.** Form competing, testable hypotheses about what is going on before committing to an answer.
3. **Analyze / Validate.** Perform the analysis correctly and validate signal vs noise, including data-quality and statistical validity.
4. **Synthesize.** Turn results into a coherent, prioritized set of findings. The 'so what'.
5. **Recommend / Communicate.** Deliver a clear, decision-ready recommendation with caveats, in the right format for the audience.

---

## Next Action

Choose the pairing before you write a word of the prompt. The `guide-to-prompt` skill runs the four steps (domain, objective, boundaries, save the pairing) and serves the canonical example asks one file at a time.

With your domain, objective, and reasoning phases chosen, write the ask.

- **Next:** Writing the prompt turns the tags into a precise decision with method left unspecified.
- **Then:** Sourcing data and building inputs assembles evidence that supports the objective you tagged. The per-objective evidence requirements are tabulated in `.claude/skills/dataset-generation/SKILL.md` §1.
