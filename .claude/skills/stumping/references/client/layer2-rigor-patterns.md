# Layer 2 library: rigor patterns by domain

The client's 300 methodological pitfalls by domain and task type, one line each: **the pitfall and the rigorous method**; Shortcut: what a capable analyst does instead; Pin: what in the task makes the rigorous method the only defensible one.

- **Learn, never copy.** No pattern names a dataset or scenario. Pick one the data in hand produces and build your own version; the design note says in one line why this data produces it.
- **Duplicates.** A card's `layer2_pattern` is `<domain-key>/<task-type-key>/<n>` (the domain key in parentheses on each `##`, the task-type key as each `###`, both as in `client_domains` in `../../../fingerprint/vocab.json`; never renumber) or `own:<short name>` for a pattern beyond the library. The same pattern on the same data structure is a duplicate `guard.py` blocks; on a new structure it warns, and the note says how this version differs.
- **The pin is a stated standard** (the estimand, the design, a named method) with the data ruling out the alternatives, never a hidden method recovered from certified or published figures. Turning a pattern into a stump: `../../SKILL.md` Parts 1 and 2; pinning it without a plant: `../../../determinism-check/SKILL.md` §1 and §2.
- Domains with no patterns here (Quantitative Finance; Banking, Credit & Financial Risk; Actuarial Science & Insurance; Physical & Environmental Sciences; Energy Systems & Utilities; Human Factors & Ergonomics) draw on the five families in `two-layer-task-design.md` and the nearest domain below.

## Product Analytics (`product-analytics`)

### online-experimentation-a-b-test-design-readout
1. **Session ratio metrics need the delta method** (or a user-level bootstrap). Shortcut: session-level t-test. Pin: randomised by user; metric is total clicks over total sessions per arm.
2. **Peeking inflates false positives**: read at the pre-registered horizon or the sequential boundary. Shortcut: first day p < 0.05 wins. Pin: fixed n or alpha-spending rule; daily log supplied.
3. **Guardrail safety needs non-inferiority**: the interval excludes harm beyond tolerance; underpowered = inconclusive. Shortcut: no significant drop = passed. Pin: a maximum tolerable degradation per guardrail.

### observational-causal-inference
1. **Adopters were already the best users**: match or DiD on pre-adoption trajectories, pre-trends checked. Shortcut: adopter vs non-adopter retention. Pin: not randomised; pre-launch activity for all users.
2. **Staggered rollouts break two-way FE**: group-time estimates against not-yet-treated units, then aggregate. Shortcut: treated dummy, unit and week FE. Pin: rollout dates differ; effect by weeks since rollout.
3. **Ever-used windows create immortal time**: time-varying exposure or a landmark. Shortcut: ever used in month one, survival from signup. Pin: retention from signup; first-use dates vary in the window.

### metric-definition-measurement-science
1. **Validate metrics on known interventions**: sensitivity and directional agreement against variance. Shortcut: pick the candidate that moved most. Pin: labelled past experiments, those two criteria stated.
2. **Ratio of sums is not mean of ratios**: aggregate by the stated unit, variance to match. Shortcut: total events over total users regardless of unit. Pin: the definition names the unit (e.g. the average user's rate).
3. **Mix shift masquerades as behaviour change**: split into within-segment rate and composition. Shortcut: topline move = behaviour. Pin: did behaviour change; segment sizes and rates, both periods.

### retention-cohort-lifetime-value-modeling
1. **Young cohorts are censored, not churned**: only cohorts observed that long, or a survival estimator. Shortcut: month-N over all cohorts, unobserved as zero or dropped. Pin: acquisition dates, cutoff, a fixed age.
2. **Constant churn understates heterogeneous lifetime**: fit a heterogeneity model (shifted-beta-geometric). Shortcut: lifetime = 1 / first-period churn. Pin: the model is named or the curve visibly flattens.
3. **Resample users, not cohort cells**, keeping each user's periods together. Shortcut: intervals from the spread of monthly rates as if independent. Pin: bounds by cohort asked; user-level histories supplied.

### churn-propensity-uplift-modeling
1. **Target persuadables, not likely retainers**: uplift trained on randomised arms, ranked by Qini. Shortcut: treat the likeliest retainers. Pin: whose retention would most rise; randomised holdout.
2. **Features must predate the prediction moment**: features at a cutoff, label after, backtest a later cutoff. Shortcut: full-history features, label on the same extract. Pin: a fixed scoring date and churn definition.

### funnel-journey-analysis
1. **Funnel steps are ordered and windowed per user.** Shortcut: distinct users per event, divide adjacent counts (later steps can exceed earlier). Pin: step order and a conversion window stated.
2. **Small segments look like the worst leaks**: beta-binomial shrinkage, rank by expected lost conversions. Shortcut: lowest raw conversion = worst. Pin: drop-offs with uncertainty; sizes vary widely.

### network-effect-marketplace-experimentation
1. **Shared supply contaminates user-level tests**: randomise and analyse at the cluster or time slot holding the interference. Shortcut: randomise buyers or sellers. Pin: cluster or switchback design named.
2. **Switchbacks need burn-in and period-level inference**: drop carryover, randomisation inference over the schedule. Shortcut: pooled order-level test. Pin: switch interval, carryover window and schedule stated.

### feature-adoption-diffusion-modeling
1. **Separate novelty from durable usage**: effect by time since first exposure, judged on the plateau. Shortcut: average over the whole window. Pin: durable usage asked; exposure dates span the decay.
2. **Adoption rates need the eligible denominator** at risk each period. Shortcut: cumulative adopters over all active users. Pin: per-user eligibility dates; asks how fast eligible users adopt.

## Marketing & Consumer Research (`marketing-consumer-research`)

### segmentation-market-structure
1. **Clusters always appear; show stability** by bootstrap or split-half agreement. Shortcut: k-means once, k from the elbow. Pin: the agreement measure and threshold are named.
2. **Size latent classes by posterior probabilities**, propagating parameter uncertainty. Shortcut: modal assignment, binomial interval. Pin: latent class model; intervals with classification uncertainty.
3. **Scale-use style masquerades as attitude segments**: centre within respondent, or use best-worst, before clustering. Shortcut: cluster raw 1 to 7 ratings. Pin: within-respondent standardisation required.
4. **Judge switching against the duplication-of-purchase expectation**; only excess duplication marks a submarket. Shortcut: most switchers = closest rivals. Pin: submarket defined as excess over the share-based expectation.

### conjoint-choice-willingness-to-pay-analysis
1. **Logit simulators steal share equally (IIA)**: individual draws or randomized first choice, so a clone eats its twin. Shortcut: aggregate part-worths in one logit. Pin: individual draws and rule given; a near-clone added.
2. **WTP is a ratio of random utilities**: compute per draw, summarise by the stated median. Shortcut: mean part-worth over mean price coefficient. Pin: WTP defined as the population median of individual WTP.
3. **Preference share is not market share**: keep the no-choice option, then calibrate. Shortcut: share among shown products = market share. Pin: the design had a no-choice option; volume asked.
4. **Never simulate prices outside the tested range**; interpolate as planned. Shortcut: linear price term at any price. Pin: tested levels, piecewise-linear interpolation, the best in-range price asked.

### brand-campaign-ad-effectiveness-measurement
1. **Exposed vs unexposed is targeting, not lift**: ITT from the randomised contrast over the exposure rate. Shortcut: exposed vs unexposed conversion. Pin: randomised holdout; lift among exposed asked.
2. **Compare exposed with would-have-been-exposed controls** (ghost ads). Shortcut: exposed test users vs all control users. Pin: a ghost-impression flag in control; effect on the exposed.
3. **Adstock and saturation set marginal return**: slope of the curve at current spend. Shortcut: same-week sales on spend. Pin: adstock and saturation forms given; return on a stated increase.
4. **Geo tests have markets as the unit**: market-level DiD or synthetic control on pre-period data. Shortcut: pooled user-level t-test. Pin: region assignment, few regions, significance at a stated level.

### customer-satisfaction-driver-analysis
1. **Correlated drivers need variance decomposition** (Shapley, relative weights). Shortcut: rank by standardised coefficients. Pin: each attribute's share of explained variance by a named method.
2. **NPS change needs multinomial error**, covariance of the two proportions included. Shortcut: any few-point move is real. Pin: change between independent waves at a stated level.
3. **Penalties and rewards are asymmetric**: estimate below and above adequate separately. Shortcut: one linear slope per attribute. Pin: separate effects around a stated threshold.
4. **Link satisfaction to later observed loyalty**, among all surveyed. Shortcut: correlate with stated repurchase intent in the same survey. Pin: loyalty defined as renewal or repeat in a window after the survey.

### media-reach-frequency-audience-measurement
1. **Channel reaches overlap**: duplication from a single-source panel. Shortcut: add channel reaches, or assume independence. Pin: single-source panel; unduplicated reach.
2. **Average frequency hides who reaches threshold**: use the skewed distribution. Shortcut: GRPs over reach applied to all. Pin: effective reach at a stated minimum; person-level counts.
3. **Campaign reach is not summed weekly reach**: persons with at least one exposure over the flight. Shortcut: sum weekly reach. Pin: cumulative unique reach asked; person-level data.
4. **Project panels with person weights** to the stated universe. Shortcut: unweighted share of panelists. Pin: projection weights and universe supplied.

## General Statistics & Data Science (`general-statistics-data-science`)

### exploratory-data-analysis-distribution-assessment
1. **Judge outliers on the symmetric scale**: robust or log-scale rules on skewed data. Shortcut: raw mean plus three SD. Pin: the anomaly rule or distributional assumption is stated.
2. **Stratify before reading a correlation** (Simpson's paradox). Shortcut: report the pooled trend. Pin: the within-group comparison or unit-defining grouping is named.

### regression-classification-model-diagnostics
1. **Influence needs leverage and residual together** (Cook's distance, DFBETAS). Shortcut: drop large raw residuals and refit. Pin: asks which points change the coefficients, by a stated measure and threshold.
2. **Use leave-out residuals for misfit**, robust SEs when variance moves with the mean. Shortcut: raw residuals, classical SEs. Pin: a stated diagnostic standard (externally studentised, HC errors).

### resampling-simulation-monte-carlo-methods
1. **Resample the independent unit**: clusters, subjects or blocks. Shortcut: resample rows. Pin: the design (repeats, clusters, serial dependence).
2. **Biased statistics need BCa or studentised intervals**, coverage shown by simulation from a known truth. Shortcut: 2.5th/97.5th percentiles. Pin: verified coverage at a stated nominal level.

### bayesian-modeling-posterior-inference
1. **Partial pooling, not raw or grand means**, via a hierarchical model. Shortcut: rank raw group estimates, or use the overall mean. Pin: a hierarchical model on sparse groups is asked.
2. **Predict with the posterior predictive**, including observation noise and between-group variance. Shortcut: the group-mean credible interval. Pin: predictions for new units or groups asked.
3. **Prior sensitivity belongs on the variance component.** Shortcut: vary the mean prior, declare robust. Pin: sparse hierarchical model, few groups, prior sensitivity asked.

### missing-data-censoring-measurement-error
1. **Pool imputations by Rubin's rules.** Shortcut: average imputed values into one dataset. Pin: the association after multiple imputation.
2. **Covariate error attenuates**: regression calibration or SIMEX from replicates. Shortcut: treat the covariate as exact. Pin: replicate or validation measurements give the error variance.
3. **Delta-adjust for nonignorable missingness** and find the tipping shift. Shortcut: complete-case agrees with MI = robust. Pin: a sensitivity grid or tipping-point question is named.

### multiple-testing-selective-inference
1. **FDR on the whole family tested.** Shortcut: BH on the screened subset or per subgroup. Pin: the family of hypotheses is defined.
2. **Do not reuse data for selection**: sample splitting or selective inference. Shortcut: stepwise selection then the final model's p-values. Pin: the prompt asks to account for data-driven selection.

### data-integration-record-linkage-entity-resolution
1. **Propagate linkage error to the estimate** (match weights, clerical review): false links attenuate, missed links select. Shortcut: links above a cutoff as truth. Pin: linkage error in downstream estimates asked.

### benchmarking-and-ablations
1. **Gaps must beat seed variance**: multiple seeds, same splits, paired test. Shortcut: one run per arm. Pin: seed count and paired test stated.
2. **Ablate one component at equal tuning budget.** Shortcut: strip components from the tuned model without retuning. Pin: equal budget or a fixed protocol stated.

### scaling-laws
1. **Fit the power law with its irreducible floor**, judged on held-out scales. Shortcut: OLS of log loss on log compute, extrapolate. Pin: the functional form and held-out largest scales are stated.

### robustness-analysis
1. **Test robustness on the deployment shift**: worst-group or shifted performance with uncertainty. Shortcut: in-distribution accuracy. Pin: the shift or subgroups are named.

### interpretability
1. **Correlated features need grouped or conditional importance.** Shortcut: single-feature permutation importance. Pin: importance of features known to correlate.

## Biomedical & Clinical Research (`biomedical-clinical-research`)

### clinical-trial-design-analysis
1. **Analyse as randomised (ITT, treatment policy).** Shortcut: drop switchers and non-adherers, compare as treated. Pin: ITT primary named; assigned arm recorded apart from received.
2. **Time-to-event trials are sized by events**, then patients from accrual, follow-up and dropout. Shortcut: two-proportion sample size. Pin: target HR, accrual, minimum follow-up and control median stated.

### survival-time-to-event-analysis
1. **Competing deaths are not censoring**: Aalen-Johansen CIF, Gray or Fine-Gray. Shortcut: 1 - KM censoring other deaths. Pin: the real-world probability by a stated time; competing events coded.
2. **Response status needs a landmark** or a time-varying covariate. Shortcut: KM by best response from randomisation. Pin: a status attained during follow-up, with dates.

### diagnostic-biomarker-accuracy
1. **Partial verification biases accuracy**: Begg-Greenes or inverse probability of verification weighting. Shortcut: accuracy on verified patients only. Pin: accuracy in all tested; verification rates differ by result.
2. **An in-sample tuned cutoff is optimistic**: choose in development, report held out. Shortcut: Youden cutoff scored on the same data. Pin: accuracy in new patients; a validation split or resampling plan.

### dose-response-pk-pd-modeling
1. **Relative and absolute ED50 differ** when the fitted top misses full response: 4PL on log dose, the ED50 as defined. Shortcut: report the midpoint parameter. Pin: ED50 defined on a reference response above the plateau.
2. **AUC to infinity needs terminal extrapolation**: AUClast + Clast / lambda_z. Shortcut: trapezoids to the last sample. Pin: named NCA standard; sampling ends before negligible levels.

### genomics-gwas-high-dimensional-association
1. **Ancestry confounds association**: PCs or an LMM with kinship, check lambda. Shortcut: regress with age and sex only. Pin: structure control required; ancestry clusters or inflated lambda.
2. **Discovery effects carry winner's curse**: replication estimates or a selection correction. Shortcut: discovery effects into replication power. Pin: expected effect in a new cohort; hits chosen in the same data.

### statistical-genomics
1. **Counts need size factors and a negative binomial model**, shrunken dispersion, FDR. Shortcut: total-count scaling, log, t-tests at raw 0.05. Pin: DE genes at a stated FDR from raw counts, few replicates.
2. **The lead SNP is not the causal variant**: fine-map with matched LD, report the credible set. Shortcut: smallest p = causal. Pin: credible set at a stated coverage; ancestry-matched LD supplied.

### longitudinal-outcomes-repeated-measures
1. **Completers analysis assumes random dropout**: MMRM on all visits, then delta or tipping-point. Shortcut: completers only or LOCF. Pin: MMRM primary named; dropout differs by arm and response.
2. **Adjust for baseline (ANCOVA), not change alone.** Shortcut: t-test on change scores. Pin: baseline-adjusted estimate specified; baseline imbalance with a correlated outcome.

### adaptive-platform-basket-trial-methods
1. **Compare arms with concurrent controls only**, or adjust for period. Shortcut: pool every control ever enrolled. Pin: concurrent controls specified; controls accrued before some arms opened.
2. **Interim looks spend alpha** at the actual information fraction. Shortcut: final alpha at each look. Pin: Lan-DeMets function named; the interim fell at an off-plan event count.

### real-world-evidence-comparative-effectiveness
1. **Align time zero in target trial emulation** (clone with a grace period, or sequential trials). Shortcut: ever-treated, followed from diagnosis. Pin: time zero and grace period stated; initiation trails eligibility.
2. **Per-protocol emulation needs inverse censoring weights** on time-varying covariates, then standardise. Shortcut: censor deviators, unweighted Cox. Pin: per-protocol one-year risk difference; covariates predict switching.

### medical-imaging-reader-study-evaluation
1. **Readers and cases are both random** (Obuchowski-Rockette, DBM). Shortcut: pooled ROC per modality, DeLong. Pin: generalise to readers; fully crossed MRMC design.
2. **Lesions within a patient cluster**: patient-level, cluster-robust or JAFROC. Shortcut: every lesion independent. Pin: performance per patient or localisation; patients contribute varying findings.

## Epidemiology & Public Health (`epidemiology-public-health`)

### observational-study-design-cohort-case-control
1. **Sample controls from the risk set** (incidence density) so the OR estimates the rate ratio. Shortcut: end-of-follow-up non-cases or hospital controls. Pin: IRR from a nested case-control in a defined cohort.
2. **Matched designs need conditional analysis.** Shortcut: ordinary logistic on pooled matched data. Pin: individual matching on stated factors; matched-set ids given.
3. **Exposure after entry creates immortal time**: time-varying exposure or a landmark. Shortcut: ever exposed = exposed from entry. Pin: time zero at entry; exposure starts later for some.

### disease-surveillance-outbreak-anomaly-detection
1. **Compare against the seasonal baseline** (Farrington, Serfling: same weeks of prior seasons, trend, past outbreaks downweighted). Shortcut: this week vs the last few. Pin: algorithm and seasons named.
2. **Nowcast incomplete recent weeks** with the empirical delay distribution. Shortcut: read raw latest counts as the trend. Pin: report dates make delay estimable; trend in latest weeks asked.
3. **Testing volume changes the count**: positivity or test-adjusted rates. Shortcut: more confirmed cases = more infection. Pin: tests performed reported; outbreak defined on positivity or adjusted rate.

### risk-factor-causal-effect-estimation
1. **ORs overstate common-outcome RRs**: log-binomial, modified Poisson or standardisation. Shortcut: report the logistic OR as RR. Pin: adjusted RR asked; common outcome.
2. **Adjusted PAF uses cases' exposure prevalence** (Miettinen). Shortcut: Levin with population prevalence and adjusted RR. Pin: PAF from the confounder-adjusted RR.
3. **Never adjust for mediators or colliders** of the total effect. Shortcut: adjust for everything associated. Pin: a causal diagram supplied; total effect asked.

### screening-diagnostic-policy-evaluation
1. **Survival from diagnosis rewards lead time**: disease mortality per person randomised. Shortcut: five-year survival screen vs clinically detected. Pin: randomised trial with deaths per arm.
2. **Overdiagnosis is persistent excess incidence** after lead time catches up. Shortcut: every extra detected case = a prevented progression. Pin: cumulative incidence by arm beyond the screening period.
3. **Predictive value depends on prevalence**: recompute PPV at target prevalence. Shortcut: the validation study's PPV. Pin: target prevalence stated; false positives per true positive asked.

### health-burden-impact-modeling
1. **YLL uses the reference life table** remaining expectancy at each age. Shortcut: deaths x (life expectancy - mean age at death). Pin: reference table named; DALYs by age group.
2. **Potential impact fraction is not scaled PAF**: compare the shifted exposure distribution. Shortcut: PAF x 20 percent. Pin: exposure distribution, RR function and shift specified.

### infectious-disease-transmission-modeling
1. **Rt needs onset timing and the generation interval** (renewal equation). Shortcut: this week's reports over last week's. Pin: serial interval given; onset dates or delay distribution.
2. **R is the next-generation matrix's dominant eigenvalue**; interventions act on it. Shortcut: population-weighted average of contact cuts. Pin: contact matrix and age parameters; R per scenario.

### cluster-stepped-wedge-community-trials
1. **Stepped wedge confounds calendar time**: period effects, treated vs not-yet-treated in the same period. Shortcut: pooled before-after per cluster. Pin: staggered crossover; effect adjusted for secular trend.
2. **Clusters carry the information**: ICC, small-sample correction. Shortcut: individuals as independent. Pin: cluster randomisation, few clusters, a CI at a stated level.

### health-equity-disparity-decomposition
1. **Age-standardise before comparing group rates.** Shortcut: crude rate gap. Pin: standard population named; age-adjusted ratio or difference.
2. **Decomposition shares depend on the reference** and binary outcomes need a nonlinear method. Shortcut: linear Oaxaca with whichever coefficients come first. Pin: method and reference coefficients specified.

## Pharmacology, Pharmacoepidemiology & Safety (`pharmacology-pharmacoepidemiology-safety`)

### population-pharmacokinetics-exposure-response
1. **Covariate effects belong inside the mixed model.** Shortcut: regress shrunk post-hoc clearances on covariates. Pin: covariate effects in an NLME model asked.
2. **Allometric scaling is a parameterisation**, centred on a reference weight. Shortcut: linear weight on clearance. Pin: covariate model or reference weight stated.
3. **Exposure-response is confounded by clearance**: several randomised doses or adjust for clearance determinants. Shortcut: response on exposure within one dose arm. Pin: multi-dose design or stated adjustment.
4. **Model BLQ as censored** (likelihood). Shortcut: drop them or impute LLOQ/2. Pin: the plan states the censored-likelihood method.

### drug-utilization-comparative-safety
1. **New users only, from first fill** after washout, covariates before it. Shortcut: prevalent users from cohort entry. Pin: new-user active-comparator design named.
2. **No immortal time between entry and exposure**: align time zero or vary exposure. Shortcut: ever filled, from diagnosis. Pin: stated entry and exposure definitions.
3. **Choose on-treatment or initial-treatment and censor to match** (grace period, risk window). Shortcut: all events in a fixed window regardless of persistence. Pin: risk window, grace and censoring rule stated.
4. **Weights must balance baseline covariates**; ATE vs ATT follows the scheme. Shortcut: every variable, post-start ones too, in an outcome model. Pin: estimand and baseline window named.

### safety-signal-detection
1. **Sparse cells need shrinkage** (IC, EBGM, lower bounds). Shortcut: rank by crude ROR. Pin: the signal criterion (lower bound, minimum count).
2. **Indication and notoriety mask as signal**: state the comparator background and stratify. Shortcut: compare against all other reports. Pin: comparator and stratification specified.
3. **Reports are not incidence**: a signal prioritises review. Shortcut: reports over prescriptions as the AE rate. Pin: a ranked list for clinical review asked.
4. **Sequential surveillance spends alpha** (maxSPRT, group sequential). Shortcut: a fixed test each month. Pin: method and total alpha stated.

### benefit-risk-assessment
1. **Absolute risks drive benefit-risk** at each subgroup's baseline. Shortcut: relative reduction vs relative harm. Pin: subgroup benefit-risk asked.
2. **Weight outcomes by stated preferences**, with sensitivity range. Shortcut: equal-weight event sum. Pin: weights and decision threshold supplied.
3. **Subgroup effects need an interaction test.** Shortcut: the subgroup with p < 0.05 benefits. Pin: asks whether profiles differ.
4. **Death competes**: cumulative incidence functions. Shortcut: 1 - KM censoring deaths. Pin: high mortality; CIF is the stated quantity.

### medication-adherence-persistence
1. **PDC truncates to the window** with carryover and stated hospital handling. Shortcut: MPR (days supplied over window, can exceed 1). Pin: PDC with carryover and an 80 percent threshold defined.
2. **The permissible gap defines discontinuation**; end of data and death are censored. Shortcut: no fill at study end = discontinued. Pin: gap length and censoring rules stated.
3. **Healthy adherers mislead outcome links**: unrelated-drug negative control or placebo-arm adherers. Shortcut: outcome on adherence as drug effect. Pin: the prompt asks to address healthy-adherer bias.
4. **Measure adherence before the outcome** or time-varying. Shortcut: adherence over all follow-up vs events in it. Pin: the exposure window precedes ascertainment.

## Healthcare Delivery & Health Economics (`healthcare-delivery-health-economics`)

### cost-effectiveness-decision-modeling
1. **Incremental ICERs after removing strict and extended dominance.** Shortcut: every ICER vs usual care, most QALYs under it. Pin: WTP threshold, several mutually exclusive strategies.
2. **Probability cost-effective comes from net benefit** per PSA draw. Shortcut: share of draws with ICER under threshold. Pin: PSA draws and a stated threshold.
3. **Convert rates, not probabilities, across cycle lengths**: p = 1 - exp(-rt). Shortcut: annual probability / 12. Pin: annual source probabilities, monthly-cycle model.
4. **Within-cycle correction on Markov traces** (half-cycle or trapezoid), discount by cycle time. Shortcut: start-of-cycle membership, annual discount. Pin: the correction and discount rate are stated.

### utilization-access-demand-forecasting
1. **Observed visits are capped demand**: count all presentations against capacity. Shortcut: trend completed visits. Pin: demand defined as all presentations; walkout, diversion or waitlist counts in the source.
2. **Project with age-sex rates** on the projected structure. Shortcut: linear trend on total visits. Pin: age-band projections; demand in a future year by location.
3. **Access needs a two-step floating catchment** within the travel threshold. Shortcut: providers in area over area population. Pin: a travel-time catchment and an access standard.
4. **Plan capacity to an overdispersed quantile** (negative binomial or empirical). Shortcut: mean plus a Poisson margin. Pin: coverage on a stated share of days; variance well above mean.

### provider-quality-risk-adjustment
1. **Risk-adjust only for present-on-admission factors.** Shortcut: every coded secondary diagnosis. Pin: the measure spec uses prior encounters or POA flags.
2. **Indirectly standardised O/E ratios do not rank hospitals** head to head: direct standardisation. Shortcut: lower O/E = better than peer. Pin: asks whether one hospital beats another.
3. **Shrink small hospitals toward the mean** (hierarchical, predicted over expected). Shortcut: rank raw risk-adjusted rates. Pin: a shrinkage method named; volumes vary widely.
4. **Funnel limits inflated for overdispersion.** Shortcut: worst decile, or plain binomial limits. Pin: unusual providers at a stated confidence by funnel or control limits.

### patient-flow-beds-workforce-optimization
1. **Size beds by blocking probability**, queueing or loss model. Shortcut: mean census / 85 percent. Pin: a maximum probability of delay or refusal.
2. **Staff to the hourly arrival curve** (time-varying or lagged model). Shortcut: staff from the daily average rate. Pin: hourly arrivals; the standard applies every hour.
3. **Boarding is a downstream bottleneck**: model admissions, transfers, discharges. Shortcut: add ED beds in proportion to boarding hours. Pin: asks which intervention reduces boarding; cross-unit flow times.
4. **Staffing ratios bind per unit and shift** as integer constraints. Shortcut: continuous solve rounded, or pooled ratios. Pin: minimum ratios per unit per shift; minimum-cost feasible roster.

### payment-claims-health-plan-analytics
1. **Complete recent claims** with lag-triangle factors before comparing. Shortcut: paid by service month as extracted. Pin: incurred cost asked; paid-through soon after period end.
2. **Voluntary bundles need a comparison group**: DiD with checked pre-trends. Shortcut: participants' pre-post change. Pin: voluntary participation; non-participant episodes available.
3. **Reconcile in contract order** (winsorize, target, discount, aggregate stop-loss and stop-gain). Shortcut: raw sum vs target, cap each episode. Pin: the contract sequence is stated.
4. **Risk-adjusted PMPM is a ratio of totals** over member months, by member-month-weighted risk. Shortcut: average member PMPM, or enrollees x 12. Pin: members enrol and leave mid-year.

## Economics & Econometrics (`economics-econometrics`)

### causal-identification-did-iv-rd-synthetic-control
1. **Staggered adoption breaks naive two-way FE**: cohort-by-period effects vs never or not-yet treated, aggregated. Shortcut: one TWFE post dummy. Pin: staggered timing; ATT by cohort or event time.
2. **Weak instruments need robust inference**: effective F, Anderson-Rubin sets. Shortcut: 2SLS with conventional SE. Pin: a weak-IV robust set or first-stage threshold named.
3. **RD is local**: local linear, data-driven bandwidth, triangular kernel, density check. Shortcut: global quartic. Pin: sharp cutoff, estimator and bandwidth selector named.
4. **Synthetic control uses placebo-rank inference** on the RMSPE ratio, shocked donors excluded. Shortcut: t-test of post gaps. Pin: placebo permutation, donor rule and required rank specified.

### structural-equilibrium-modeling
1. **Price is endogenous in demand**: instrument with cost shifters or rival characteristics. Shortcut: OLS on log share ratios. Pin: valid instruments supplied; IV demand drives the merger simulation.
2. **Merger simulation solves a new equilibrium**: back out costs, re-solve prices jointly. Shortcut: one UPP or diversion markup. Pin: Bertrand-Nash, constant marginal cost, equilibrium prices asked.

### time-series-macro-econometrics
1. **Cointegration tests use their own critical values** (Engle-Granger, Johansen), after unit-root tests. Shortcut: OLS in levels with conventional p-values. Pin: a named test at a stated level.
2. **Johansen rank depends on lags and deterministic terms.** Shortcut: software defaults. Pin: the lag criterion and deterministic case are fixed.
3. **A shock is defined by its identification**; VECM trend shocks are permanent. Shortcut: default-ordered or reduced-form IRFs. Pin: ordering or structural restriction and horizon named.

### panel-data-estimation
1. **Lagged outcome with FE biases persistence (Nickell)**: difference or system GMM, AR(2) and overid tests. Shortcut: within estimator with the lag. Pin: short T; a dynamic-panel estimator required.
2. **Too many GMM instruments fake validity**: collapse or cap, report count vs groups. Shortcut: full matrix, Hansen p near 1 as proof. Pin: a lag limit or collapse rule.
3. **Cluster where treatment varies**; wild cluster bootstrap when few. Shortcut: observation-level robust SE. Pin: group-level policy and a decision significance level.

### elasticity-welfare-policy-impact-estimation
1. **An added tax costs the existing wedge's rectangle too**; DWL grows with the square of the total tax. Shortcut: triangle on the increment. Pin: existing tax stated; incremental DWL asked.
2. **Short-run coefficient is not long-run elasticity**: divide by one minus the lag coefficient. Shortcut: price coefficient as the permanent elasticity. Pin: a permanent tax over a full-adjustment horizon.

### forecasting-forecast-evaluation
1. **Backtest on real-time vintages** against the named target release. Shortcut: pseudo out-of-sample on revised data. Pin: vintages supplied; realised-outcome release defined.
2. **Score densities with proper rules** (log score, CRPS, PIT), overlapping-horizon tests. Shortcut: MSE of the means. Pin: scoring rule, horizon and test named.

### discrete-choice-limited-dependent-variable-modeling
1. **WTP is a coefficient ratio**: delta method or joint draws with covariance. Shortcut: interval from the time coefficient's SE alone. Pin: WTP with an interval by a named method.
2. **MNL overpredicts similar alternatives (IIA)**: nest or mixed logit, test IIA. Shortcut: plain MNL share for the new mode. Pin: a close substitute added; nesting specified.

### spatial-econometrics-spillover-estimation
1. **Spatial coefficients are not marginal effects**: direct and indirect from (I - rho W)^-1. Shortcut: beta as direct, WX as spillover. Pin: named spatial lag or Durbin model; direct vs spillover asked.
2. **The neighbours' outcome is endogenous**: ML or IV with lagged covariates. Shortcut: neighbours' average in OLS. Pin: weights matrix and an ML or GMM estimator specified.

## Political Science & Public Policy (`political-science-public-policy`)

### election-polling-forecasting
1. **Race errors correlate through a national swing**: simulate jointly. Shortcut: combine per-race probabilities as independent. Pin: a joint outcome (majority, seat count) asked.
2. **Remove house effects before averaging**, weight by size and recency. Shortcut: equal-weight mean of all polls. Pin: house adjustment stated, or one leaning firm dominates.
3. **The likely-voter screen defines the estimand**: map samples to the likely electorate. Shortcut: pool adult, RV and LV toplines. Pin: target is share of votes cast; screens differ.
4. **Calibrate intervals on past forecast error.** Shortcut: pooled sampling margin. Pin: stated coverage checked against prior cycles.

### policy-evaluation-administrative-data-inference
1. **Phased rollout needs not-yet-treated comparisons** by group and period. Shortcut: post dummy with two-way FE. Pin: differing adoption dates; ATT at stated event times.
2. **Voluntary take-up means ITT on the eligible**, scaled by take-up only if asked. Shortcut: participants vs eligible non-participants. Pin: effect of the reform on the eligible.
3. **Ashenfelter dip**: baseline from well before the pre-entry drop. Shortcut: post minus the quarter before entry. Pin: baseline window stated, or the visible dip.
4. **Local fits at the eligibility cutoff** in a stated bandwidth. Shortcut: above vs below means, or a global polynomial. Pin: score threshold; bandwidth and kernel stated.

### legislative-behavior-ideal-point-estimation
1. **Anchor ideal points on one scale across sessions** (bridges or fixed anchors). Shortcut: separate scaling, compare party means. Pin: change in polarization across sessions.
2. **Drop lopsided votes before scaling.** Shortcut: scale every vote. Pin: a lopsidedness cutoff and minimum votes per legislator.
3. **Party unity is not ideological distance** (agenda control). Shortcut: rising unity = polarization. Pin: polarization defined as the distance between party medians.

### conflict-protest-event-data-analysis
1. **Reported events track media reach**: condition on the reporting proxy. Shortcut: raw counts on socioeconomic covariates. Pin: a coverage measure; effects conditional on reporting.
2. **Onset excludes ongoing conflict years**; intensity conditional on occurrence. Shortcut: one logit keeping ongoing years. Pin: onset defined as a new episode after a stated peace interval.
3. **Event counts are overdispersed and spatially clustered**: negative binomial, clustered errors. Shortcut: Poisson, default SE. Pin: variance far above mean; significance at a stated level.

### public-opinion-survey-experimentation
1. **Group differences need the interaction test**, with multiplicity control. Shortcut: significant in one group, not the other. Pin: asks whether effects differ.
2. **Post-treatment attention checks break randomisation.** Shortcut: drop failers. Pin: check given after assignment; effect among all randomised.
3. **Subgroup conjoint preferences need marginal means**, not AMCE gaps. Shortcut: compare subgroup AMCEs. Pin: preference levels across groups; a stated baseline category.

### small-area-public-opinion-estimation-mrp
1. **Poststratify on the joint area frame.** Shortcut: weight by sample counts or separate marginals. Pin: MRP named; a joint poststratification table.
2. **Area-level predictors carry sparse areas.** Shortcut: demographics plus area intercepts only. Pin: very sparse areas; the model includes area covariates.
3. **Rank areas on posterior draws.** Shortcut: order point estimates. Pin: probability of exceeding a threshold, or ranks with stated certainty.

## Sociology & Demography (`sociology-demography`)

### population-estimation-demographic-projection
1. **Age the cohorts (cohort-component)**, do not extrapolate totals. Shortcut: trend the total, split by latest shares. Pin: counts by age and sex, or the method named with rates.
2. **Gross migration flows, not net rates**; the system stays closed. Shortcut: net rate on the projected population. Pin: origin-destination flows; internal migrants sum to zero.
3. **Scenario bounds are not prediction intervals**: simulate components jointly. Shortcut: high and low variants, or summed regional bounds. Pin: stated coverage for an aggregate; error distributions or draws.
4. **Small areas honour the control total** by age-sex proportional adjustment. Shortcut: project each county alone. Pin: counties must match the state control.

### social-mobility-inequality-measurement
1. **Rank-rank slope, not log IGE**, across different inequality. Shortcut: log-log elasticities. Pin: positional mobility asked, or percentile ranks named.
2. **Single-year income attenuates persistence**: mid-career multi-year averages. Shortcut: one year at any age. Pin: permanent income defined over a stated age window.
3. **Decompose with an additively decomposable index** (Theil, MLD). Shortcut: population-weighted regional Ginis as within. Pin: an exact between-within split asked.

### social-network-peer-effect-analysis
1. **Homophily masquerades as contagion**: lagged peer adoption, own prior state, FE, or exogenous ties. Shortcut: cross-sectional adoption on friends' share. Pin: causal peer effect; tie and adoption dates separate.
2. **Reflection problem**: identify with intransitive triads (friends-of-friends instruments). Shortcut: own outcome on group mean incl. self. Pin: endogenous vs contextual asked; individual network supplied.
3. **Shared nodes break independence**: dyad-robust clustering or network permutation. Shortcut: default dyad-level p. Pin: tie-level significance; nodes in many dyads.

### event-history-life-course-analysis
1. **Competing exits are not censoring**: cumulative incidence. Shortcut: 1 - KM. Pin: share experiencing the transition by an age; competing exits recorded.
2. **Cause-specific vs subdistribution hazards answer different questions.** Shortcut: one censored Cox read as lifetime incidence. Pin: the wording names rate among those at risk or cumulative probability.
3. **Repeated spells need their own risk sets**, spell clocks, clustered by person. Shortcut: first spells only, or pooled with ordinary SE. Pin: multiple spells; recurrence asked.
4. **Late entry needs left truncation.** Shortcut: clock from the origin age. Pin: entry at differing ages, entry age recorded.

### neighborhood-segregation-contextual-effects
1. **Dissimilarity is biased in small units**: random-allocation expectation or corrected index. Shortcut: rank raw D. Pin: very different minority counts, or a bias-adjusted index named.
2. **Evenness and exposure differ**: exposure and isolation for experienced composition. Shortcut: D for contact. Pin: average neighbourhood share experienced by members.
3. **Contextual vs compositional**: multilevel with group-mean centring. Shortcut: tract rates on tract poverty (ecological). Pin: individual microdata; context net of own traits.

### fertility-mortality-life-table-estimation
1. **Period TFR is distorted by tempo**: tempo-adjust or use cohort fertility. Shortcut: period TFR drop = lower quantum. Pin: quantum net of timing; rates by order and mean ages.
2. **Life tables need proper separation factors** (infant a0 well below 0.5, open group Lx = lx/mx). Shortcut: all a = 0.5, half-width close. Pin: abridged table with infant and open groups.
3. **Smooth sparse ages exposure-weighted** (Poisson, a standard). Shortcut: drop zero ages, average raw rates. Pin: deaths and person-years; an exposure-weighted method.

## Psychology & Behavioral Science (`psychology-behavioral-science`)

### experimental-design-power-analysis
1. **Power the interaction, not the main effect.** Shortcut: main-effect d reused. Pin: the interaction is the key hypothesis, with effect or cell means.
2. **Within-subject power runs on dz**, via the correlation. Shortcut: a between-subjects d. Pin: within design; the correlation is given.
3. **Group randomisation needs the design effect** 1 + (m - 1) ICC. Shortcut: independent participants. Pin: group-level randomisation, ICC and group size.

### psychometric-measurement-scale-validation
1. **High alpha does not mean one factor**: fit the model, report omega. Shortcut: alpha over cutoff = unidimensional. Pin: congeneric reliability or omega named.
2. **Likert items need polychorics and WLSMV.** Shortcut: ML CFA on Pearson. Pin: ordinal items; the estimator named.
3. **Retain factors by parallel analysis.** Shortcut: eigenvalue > 1 or scree. Pin: parallel analysis or a retention criterion stated.

### statistical-inference-hypothesis-testing
1. **Stimuli are a random factor**: crossed random effects. Shortcut: average over stimuli, paired t. Pin: sampled stimuli; generalise to the stimulus population.
2. **Correct across the declared family** (e.g. Holm). Shortcut: every p < .05 counts. Pin: the family and method are defined.

### mediation-moderation-process-modeling
1. **Indirect effects need bootstrap intervals**; no total-effect prerequisite. Shortcut: causal steps and Sobel. Pin: bootstrap with stated resamples.
2. **Moderated mediation has its own index** with an interval. Shortcut: one subgroup indirect significant, the other not. Pin: asks whether the indirect path is moderated.
3. **Randomised treatment does not randomise the mediator**: adjust for pre-treatment confounders of M and Y. Shortcut: b path causal since randomised. Pin: baseline covariates named; M measured after treatment, before Y.

### meta-analysis-evidence-synthesis
1. **Random effects for heterogeneous studies**, named tau-squared estimator, prediction interval. Shortcut: fixed effect, I-squared as the spread. Pin: those three named.
2. **Effect sizes from one study are dependent**: multilevel or RVE. Shortcut: each as independent. Pin: multiple effects per study; the method named.
3. **Trim-and-fill is not a bias correction**: PET-PEESE or a selection model as named. Shortcut: trim-and-fill estimate as truth. Pin: the method is named and decides.

### longitudinal-growth-curve-modeling
1. **Slope change needs random slopes.** Shortcut: random intercepts only, or per-wave tests. Pin: treatment-by-time asked; random slopes specified.
2. **Dropout is informative**: FIML mixed model under MAR on all waves. Shortcut: completers or LOCF. Pin: MAR stated; all waves required.

### decision-making-computational-behavioral-modeling
1. **Compare models on penalised or held-out fit** (summed BIC, held-out likelihood). Shortcut: higher in-sample likelihood. Pin: criterion and fitting level named.
2. **Check parameter recovery before interpreting** (loss aversion vs curvature vs temperature). Shortcut: compare fitted parameters directly. Pin: a recovery check or a fixed parameter required.

### experience-sampling-intensive-longitudinal-analysis
1. **Separate within- from between-person effects**: person-mean centring. Shortcut: raw predictor, random intercept. Pin: the within-person association asked.
2. **Lagged effects need autoregressive control.** Shortcut: same-day correlation. Pin: a prospective effect at a stated lag with an AR term.

## Criminology & Justice (`criminology-justice`)

### crime-incidence-hotspot-analysis
1. **Rates need the named exposure denominator** (ambient population, targets, segments). Shortcut: crimes per resident. Pin: risk per a stated exposure.
2. **Persistence means staying in the top tier** across periods. Shortcut: top places in the latest year. Pin: a stated consecutive-period rule.
3. **Recorded crime mixes incidence, reporting and detection.** Shortcut: recorded change = crime change. Pin: reporting rates, or citizen calls split from officer-initiated.
4. **Test clusters against a spatial null** (Gi*, local Moran, multiplicity corrected). Shortcut: brightest KDE peaks. Pin: significance at a stated level by a named statistic.
5. **Smooth small-exposure rates** (empirical Bayes, minimum exposure). Shortcut: rank raw rates. Pin: EB or a minimum threshold specified.

### recidivism-risk-assessment
1. **Calibration is not discrimination.** Shortcut: good AUC = readable probabilities. Pin: an absolute probability threshold.
2. **Fixed window from release, time at risk.** Shortcut: share ever rearrested by data end. Pin: rearrest within a stated window, full follow-up required.
3. **Name the fairness criterion first**; base rates make criteria incompatible. Shortcut: similar overall accuracy = fair. Pin: e.g. equal FPR at a stated threshold.
4. **Validate on later release cohorts.** Shortcut: random split across years. Pin: future performance or a later holdout cohort.
5. **Selective labels**: outcomes exist only for the released. Shortcut: evaluate on the released as if all. Pin: performance across all scored, detained included.

### sentencing-bail-disparity-analysis
1. **Do not control for mediators of disparity** (charge reductions, detention). Shortcut: every case variable. Pin: the legally relevant pre-decision factors listed.
2. **Incarceration and length are separate stages.** Shortcut: length gap among the incarcerated. Pin: both outcomes defined separately.
3. **Outcome test, not population benchmark**: misconduct rates among the released. Shortcut: detention rates vs population or arrest shares. Pin: different release standards, defined by outcomes.
4. **Compare within court and judge** (fixed effects). Shortcut: pooled courts with case controls. Pin: similarly situated defendants before the same court.
5. **Measure departures from the guideline cell.** Shortcut: average length gap. Pin: a stated grid; departures from presumptive ranges asked.

### intervention-policing-policy-evaluation
1. **Count displacement in the catchment**; adjacent blocks are not controls. Shortcut: adjacent blocks as control. Pin: net effect incl. defined buffer zones.
2. **Places picked on spikes fall anyway** (regression to the mean). Shortcut: treated before-after. Pin: selection on recent highs; a comparably selected untreated pool.
3. **Harm-weighted index, not raw counts.** Shortcut: total incidents. Pin: harm asked; a severity weighting named.
4. **One treated city needs synthetic control** with placebo inference. Shortcut: vs the regional average. Pin: one treated unit, many donors.
5. **Diversion effect on those offered, not completers.** Shortcut: completers vs others. Pin: lottery or rotation; effect of being offered.

## Survey Research & Official Statistics (`survey-research-official-statistics`)

### sample-design-allocation-weighting
1. **Optimal allocation uses stratum SDs and costs** (N_h S_h / sqrt(c_h)). Shortcut: proportional allocation. Pin: minimum variance or cost asked; SDs and unit costs supplied.
2. **Domain CV targets are constraints**: size each region to its target first. Shortcut: optimise nationally. Pin: a maximum CV per published domain.
3. **Base weight multiplies every stage's probability**; realised cluster sizes break self-weighting. Shortcut: stratum N over n. Pin: PPS on a size measure, fixed take, actual sizes listed.

### nonresponse-calibration-measurement-error-adjustment
1. **Adjust nonresponse within cells on base weights.** Shortcut: one overall unweighted factor. Pin: adjustment cells named, before calibration.
2. **Rake until every margin converges.** Shortcut: one pass per margin. Pin: several marginal totals and a tolerance.
3. **Correct prevalence for sensitivity and specificity**: (p + Sp - 1) / (Se + Sp - 1). Shortcut: observed share, or divide by Se alone. Pin: record-check validation of both error types.

### questionnaire-mode-effects-research
1. **Separate mode selection from measurement** via the randomised-mode subsample. Shortcut: whole web vs phone gap = mode effect. Pin: random mode subsample; measurement effect asked.
2. **Split-ballot tests need Rao-Scott or Wald.** Shortcut: Pearson chi-square on weighted counts. Pin: random forms inside strata, PSUs and weights.
3. **Judge a series break on the difference's margin**, overlap covariance included. Shortcut: the old series' margin alone. Pin: break defined on the old-new difference; both variances given.

### small-area-estimation
1. **Fay-Herriot shrinks by sampling vs model variance.** Shortcut: direct where any sample exists. Pin: area-level model named; sampling variances and covariates supplied.
2. **Benchmark to the reliable total** by ratio. Shortcut: publish model estimates as produced. Pin: counties must add to the published state total.

### census-register-administrative-data-quality
1. **Dual-system estimates within post-strata, after erroneous enumerations.** Shortcut: one pooled Lincoln-Petersen on raw counts. Pin: matches and EE rates by post-stratum; net undercoverage asked.
2. **Net and gross classification error differ.** Shortcut: net change in totals as misclassification. Pin: asks bias in counts or share misclassified.

### seasonal-adjustment-official-time-series-production
1. **Model outliers and level shifts in regARIMA before seasonal filtering.** Shortcut: default adjustment, label the event afterwards. Pin: event dates and type given.
2. **Revisions compare real-time concurrent vintages.** Shortcut: latest series against itself. Pin: first release vs a stated later vintage.
3. **Date turning points on the trend-cycle** under a phase rule. Shortcut: first SA reversal. Pin: trend-cycle with a minimum phase rule.

### complex-survey-estimation-variance
1. **Variance reflects strata and PSUs** (linearisation or replicate weights). Shortcut: SRS formula. Pin: design ids or replicate weights with method and factor.
2. **Domain estimates keep the full design** (out-of-domain contributes zero). Shortcut: subset then estimate. Pin: a domain scattered across strata and PSUs.

### anomaly-detection
1. **Score edits by weighted impact on the estimate.** Shortcut: largest unweighted change. Pin: editing goal is impact on a total; weights and threshold given.
2. **Robust ratio tests scale by unit size** (Hidiroglou-Berthelot). Shortcut: z-score on raw ratios. Pin: HB test with size exponent and quartile bounds.

## Urban & Regional Science (`urban-regional-science`)

### land-use-spatial-development-modeling
1. **Parcels are spatially dependent**: spatial error or lag model, or robust SE. Shortcut: OLS p-value. Pin: significance at a stated level; a weights matrix named.
2. **Zoned capacity is not likely development**: residual land value or redevelopment screen. Shortcut: allowed minus existing units. Pin: expected units; a feasibility rule.
3. **Upzoning goes where growth already was**: boundary or matched comparison. Shortcut: rezoned before-after, or vs citywide. Pin: boundary-discontinuity or comparison design with bandwidth.

### accessibility-agglomeration-location-analysis
1. **Dense places attract productive workers**: worker FE or historical-density IV. Shortcut: cross-sectional wage-density slope. Pin: causal elasticity; worker panel or named instrument.
2. **Jobs reachable must be shared** (2SFCA). Shortcut: raw jobs within threshold. Pin: a supply-to-demand method with catchment and demand defined.
3. **Transit access depends on departure minute**: median over a window. Shortcut: one peak departure. Pin: median or percentile across a named window.

### municipal-service-demand-resource-allocation
1. **Complaints measure reporting, not failure**: verified failures per serviced unit. Shortcut: rank by complaints. Pin: need defined per unit, denominator named.
2. **Small areas top every rate ranking**: minimum volume or EB shrinkage. Shortcut: highest raw rate wins. Pin: a minimum count, credibility formula or shrinkage.
3. **Response standards are percentiles, not means.** Shortcut: mean time vs threshold. Pin: compliance at a stated percentile.

### regional-input-output-economic-impact
1. **Margin and localise spending first** (trade margins, RPCs). Shortcut: gross spend x multiplier. Pin: margins and RPCs supplied, or a model requiring them.
2. **Gross spending is not net new**: drop substitution and displacement. Shortcut: every dollar is new demand. Pin: net new impact; origin or substitution share.
3. **Leakage changes the whole inverse**: rebuild Leontief (Type II household row and column). Shortcut: scale the base multiplier. Pin: several leakage assumptions; transactions table supplied.

### optimization
1. **The stated objective decides the sites** (p-median, p-center, maximal covering differ). Shortcut: minimise average distance. Pin: the objective, k and candidates stated.
2. **Greedy siting misses the best set**: solve all k jointly. Shortcut: add the best next site. Pin: optimal k from a finite candidate list.
3. **Busy units leave coverage gaps**: expected coverage with availability (MEXCLP). Shortcut: covered once, always available. Pin: a busy fraction stated.

### forecasting
1. **Backtest from the forecast origin**, features known as of origin. Shortcut: random holdout sharing future info. Pin: a fixed origin and holdout period.
2. **Small-area forecasts meet the control total** by the stated allocation. Shortcut: independent neighbourhood forecasts. Pin: adopted control total and reconciliation method.
3. **Developed parcels leave the risk set**: discrete-time hazard with censoring. Shortcut: pooled logit keeping developed parcels. Pin: probability of first development within a horizon.

### network-analysis
1. **Catchments follow streets, not circles** (network shortest paths). Shortcut: fixed-radius buffer. Pin: coverage by network time or distance.
2. **Central links are not critical links**: remove each, recompute demand-weighted cost. Shortcut: rank by betweenness. Pin: criticality defined as added travel time or unreachable demand.

## Education & Learning Sciences (`education-learning-sciences`)

### student-growth-value-added-modeling
1. **Shrink small schools toward the mean** (empirical Bayes). Shortcut: rank raw mean residuals. Pin: shrunken effects, or variance components and credibly-below asked.
2. **Noisy prior scores under-adjust for intake**: correct with reliability or CSEMs, or several priors. Shortcut: OLS on one prior score. Pin: reliability or CSEMs supplied.
3. **Growth percentiles condition on score history** (quantile regression, school median). Shortcut: percentiles of raw gains, averaged. Pin: conditional percentile and median named.

### randomized-quasi-experimental-program-evaluation
1. **Assigned by school, inferred by school** (cluster-robust, small-cluster correction). Shortcut: student-level SE. Pin: school assignment, few schools, stated level.
2. **Scale the offer effect by take-up** (ITT over take-up difference, CACE). Shortcut: attended vs not. Pin: effect among compliers; assignment and take-up reported.
3. **Attrition decides the evidence rating**; then baseline equivalence. Shortcut: random assignment = RCT rating. Pin: attrition boundaries and equivalence thresholds given.

### item-response-theory-test-equating
1. **Match on ability before calling DIF** (Mantel-Haenszel, delta-scale categories). Shortcut: largest raw p-value gaps. Pin: matched method and classification rule named.
2. **Screen anchors for drift first**, then link. Shortcut: link on every common item. Pin: linking method and drift criterion named.
3. **Nonequivalent groups need anchor-based equating** (chained, post-stratification, IRT). Shortcut: random-groups equipercentile. Pin: NEAT design and method named.

### learning-analytics-early-warning-models
1. **Features must exist at alert time**; validate on a later cohort. Shortcut: all features, shuffled CV. Pin: fixed alert date, later held-out cohort.
2. **Set the cutoff by support capacity** (top k precision and recall). Shortcut: best AUC, flag at 0.5. Pin: students who can be served is stated.
3. **Flagged students differ**: RD at the risk-score cutoff. Shortcut: flagged vs unflagged outcomes. Pin: alerts triggered by a fixed cutoff.
4. **Equity means error rates by group.** Shortcut: similar flag shares = fair. Pin: criterion named (equal TPR); outcomes by subgroup.

### multilevel-classroom-school-research
1. **Model the classroom level.** Shortcut: two-level student-school ICC. Pin: variance shares at three levels; classroom ids.
2. **Centre within cluster to split effects.** Shortcut: raw predictor, one coefficient. Pin: within-school or contextual effect asked.
3. **Mobile students belong to several schools**: multiple membership by enrolled time. Shortcut: last school, or drop movers. Pin: a dosage rule crediting schools by share of days.

### psychometrics
1. **Alpha is not omega** under unequal loadings or a bifactor structure. Shortcut: alpha on the total scale. Pin: a factor model; omega or omega-h named.
2. **Score reliability is not decision reliability**: classification accuracy and consistency at the cut. Shortcut: overall reliability. Pin: consistency at a stated cut asked.

### text-analysis
1. **Benchmark machine scores against human-human agreement** (QWK, SMD by subgroup). Shortcut: correlation or exact agreement. Pin: thresholds tied to human-human kappa and a subgroup SMD limit.
2. **Type-token ratio falls with length**: MTLD, HD-D or fixed samples. Shortcut: raw TTR by group. Pin: a length-robust measure or sample length named.
