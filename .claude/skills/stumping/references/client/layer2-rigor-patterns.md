# Layer 2 library: rigor patterns by domain

The client's stumping-strategy library, kept as reference. Each pattern is a class of methodological pitfall an expert in the field recognises: the pitfall, the shortcut a capable analyst is tempted to take, and what in a task makes the rigorous method the only defensible one. **Patterns, not templates**: none names a dataset or a scenario. Pick a pattern that fits the data in hand and build your own version of it; two tasks with the same pattern on the same data structure are duplicates (the fingerprint card's `layer2_pattern` field and the guard enforce this). How a pattern is used in a build is in `../../SKILL.md` Part 2; how it is pinned without a plant is in `../../../determinism-check/SKILL.md` section A.

Pattern ids are `<domain-key>/<task-type-key>/<n>`; the domain keys are the ones in `../../../fingerprint/vocab.json`. Domains the client lists with no Layer 2 patterns of their own (Quantitative Finance; Banking, Credit & Financial Risk; Actuarial Science & Insurance; Physical & Environmental Sciences; Energy Systems & Utilities; Human Factors & Ergonomics) draw on the five families in `two-layer-task-design.md` and on the nearest domain here.

## Product Analytics  (`product-analytics`)

### Online experimentation (A/B test design & readout)  (`online-experimentation-a-b-test-design-readout`)

1. **Session metrics need the delta method.** When users are randomised but the metric is a ratio over sessions or page views, those units are correlated within user. Variance must come from the delta method or a user-level bootstrap; a session-level t-test understates the standard error and declares noise significant.
   - *Tempting shortcut:* Run a two-sample t-test treating every session as an independent observation.
   - *What pins it:* The design states randomisation by user and defines the metric as total clicks over total sessions per arm.
2. **Peeking inflates the false positive rate.** Checking significance daily and stopping at the first p below alpha raises the real false positive rate far above alpha. The readout must use the pre-registered horizon or the named sequential boundary; the first crossing is not a valid win.
   - *Tempting shortcut:* Declare the winner on the first day the running p-value dips below 0.05.
   - *What pins it:* The test plan fixes a sample size or names an alpha-spending rule, and the daily results log is supplied.
3. **Guardrail safety needs non-inferiority, not silence.** A guardrail passes only if the confidence interval excludes harm beyond the stated tolerance. A non-significant guardrail with a wide interval has not shown safety; underpowered guardrails must be read as inconclusive, which can block launch.
   - *Tempting shortcut:* Treat any guardrail without a significant drop as passed.
   - *What pins it:* The plan states a maximum tolerable degradation per guardrail, so the interval bound, not the p-value, decides.

### Observational causal inference  (`observational-causal-inference`)

1. **Adopters were already your best users.** Users who opt into a feature were more engaged before it existed. Comparisons must condition on pre-adoption engagement trajectories, by matching or difference-in-differences with checked pre-trends; raw adopter versus non-adopter retention mostly measures selection.
   - *Tempting shortcut:* Compare retention of adopters and non-adopters after launch and call the gap the feature effect.
   - *What pins it:* The prompt says the feature was not randomised and supplies pre-launch activity for every user.
2. **Staggered rollouts break two-way fixed effects.** When markets or platforms get the feature at different dates and effects grow over time, two-way fixed effects uses already-treated units as controls and can flip the sign. Use group-time estimates against not-yet-treated units, then aggregate.
   - *Tempting shortcut:* Regress the outcome on a treated dummy with unit and week fixed effects.
   - *What pins it:* Rollout dates differ by unit and the estimand is the average effect by weeks since rollout.
3. **Ever-used windows create immortal time.** Classing users as feature users if they used it any time in their first month gives them guaranteed survival until first use. Exposure must be time-varying or fixed at a landmark date, or the feature looks protective even with no effect.
   - *Tempting shortcut:* Label users by whether they ever used the feature in the window, then compare survival from signup.
   - *What pins it:* The question asks for retention from signup and first-use dates vary within the classification window.

### Metric definition & measurement science  (`metric-definition-measurement-science`)

1. **Validate metrics against known interventions.** A candidate north-star metric must be scored on past experiments with known outcomes: how often it detects real effects and agrees in direction, against its variance. The metric with the largest raw movement is often the noisiest, not the most sensitive.
   - *Tempting shortcut:* Pick the candidate that moved most in percent terms across past launches.
   - *What pins it:* The prompt supplies labelled past interventions and states sensitivity and directional agreement as the selection criteria.
2. **Ratio of sums is not mean of ratios.** A per-user average and a pooled ratio answer different questions; pooled ratios are dominated by heavy users. The metric must follow the stated unit of analysis, and its variance must match that choice.
   - *Tempting shortcut:* Divide total events by total users or sessions regardless of the stated unit.
   - *What pins it:* The metric definition names the unit, such as the average user's rate, which fixes the aggregation.
3. **Mix shift masquerades as behaviour change.** A topline metric can fall while every segment improves if the user mix shifts toward low-baseline groups such as new users or a weaker platform. Decompose the change into within-segment rate and composition effects before attributing it to behaviour.
   - *Tempting shortcut:* Read the topline change as a change in how users behave.
   - *What pins it:* The question asks whether user behaviour changed, and segment sizes and rates are given for both periods.

### Retention, cohort & lifetime-value modeling  (`retention-cohort-lifetime-value-modeling`)

1. **Young cohorts are censored, not churned.** Cohorts acquired recently have not reached later ages. Retention at a fixed age must use only cohorts observed that long, or a survival estimator; counting unobserved months as churn or averaging unequal horizons biases the curve.
   - *Tempting shortcut:* Average month-N retention over all cohorts, filling unobserved ages as zero or dropping them silently.
   - *What pins it:* Cohort acquisition dates and the data cutoff are given and the prompt asks retention at a fixed age.
2. **Constant churn understates heterogeneous lifetime.** Aggregate churn falls with tenure because fragile users leave first. Extrapolating lifetime value from early churn as a constant rate understates value; a heterogeneity model such as shifted-beta-geometric fits the flattening curve.
   - *Tempting shortcut:* Take the first-period churn rate and compute lifetime as one over that rate.
   - *What pins it:* The prompt names a heterogeneity-aware model or the observed curve visibly flattens over the stated horizon.
3. **Resample users, not cohort cells.** Lifetime value uncertainty must reflect user-level sampling within each cohort, with every period of a user kept together. Treating monthly retention rates as independent ignores their dependence and small cohort sizes, giving bounds far too narrow.
   - *Tempting shortcut:* Compute intervals from the spread of monthly cohort retention rates as if independent.
   - *What pins it:* The prompt asks for uncertainty bounds by cohort and user-level histories are supplied.

### Churn, propensity & uplift modeling  (`churn-propensity-uplift-modeling`)

1. **Target persuadables, not likely retainers.** Uplift is the treatment effect for a user, not their retention probability. Models must be trained and evaluated on randomised treatment and control, ranked by Qini or uplift curves; high-propensity users often retain anyway.
   - *Tempting shortcut:* Send the promotion to users with the highest predicted retention probability.
   - *What pins it:* The prompt asks whose retention would most increase and supplies a randomised promotion holdout.
2. **Features must predate the prediction moment.** Churn features computed through the label window leak the outcome, such as declining activity during the churn month. Build features as of a fixed cutoff, label from the period after, and backtest on a later cutoff.
   - *Tempting shortcut:* Compute features over the full history and label churn on the same extract.
   - *What pins it:* The prompt fixes a scoring date and churn definition, so only pre-cutoff information is admissible.

### Funnel & journey analysis  (`funnel-journey-analysis`)

1. **Funnel steps must be ordered and windowed.** A funnel counts users who complete each step after the prior step within the stated window. Counting unique users per step independently mixes journeys and can show later steps exceeding earlier ones, misplacing the biggest drop-off.
   - *Tempting shortcut:* Count distinct users who fired each event in the period and divide adjacent counts.
   - *What pins it:* The funnel definition states the step order and a conversion window per user or session.
2. **Small segments look like the worst leaks.** Ranking segments by raw step conversion surfaces tiny segments whose extreme rates are noise. Use intervals or partial pooling such as beta-binomial shrinkage, and rank by expected lost conversions, not raw rate.
   - *Tempting shortcut:* List the segments with the lowest observed conversion as the biggest problems.
   - *What pins it:* The prompt asks for drop-offs with uncertainty by segment and segment sizes vary widely.

### Network-effect & marketplace experimentation  (`network-effect-marketplace-experimentation`)

1. **Shared supply contaminates user-level tests.** In a two-sided marketplace, treated buyers draw down inventory or seller attention that control buyers would have used, inflating the measured lift. Randomise and analyse at the cluster or time-slot level that contains the interference.
   - *Tempting shortcut:* Randomise individual buyers or sellers and compare arm means.
   - *What pins it:* The design names cluster or switchback randomisation because both sides share inventory within a market.
2. **Switchbacks need burn-in and period-level inference.** After each switch, the previous regime carries over for a while, and adjacent periods are correlated. Drop the stated burn-in, analyse at the period level, and use randomisation inference over the switching schedule.
   - *Tempting shortcut:* Pool all orders in treated periods versus control periods and run an order-level test.
   - *What pins it:* The switch interval, carryover window and randomised schedule are stated in the design.

### Feature adoption & diffusion modeling  (`feature-adoption-diffusion-modeling`)

1. **Separate novelty from durable usage.** Early usage of a new feature includes curiosity trials that fade. Estimate effects by time since first exposure and judge durability from the later plateau or repeat use, not the average over the whole window.
   - *Tempting shortcut:* Average daily usage across the whole post-launch period and call it the steady state.
   - *What pins it:* The prompt asks for durable usage, and per-user exposure dates span enough weeks to see decay.
2. **Adoption rates need the eligible denominator.** During a staged rollout, only exposed and eligible users can adopt. Adoption hazards and diffusion curves must use the at-risk eligible base each period; dividing by all users confounds adoption speed with rollout speed.
   - *Tempting shortcut:* Divide cumulative adopters by total active users and fit a curve to that share.
   - *What pins it:* Rollout eligibility dates per user are given and the prompt asks how fast eligible users adopt.

## Marketing & Consumer Research  (`marketing-consumer-research`)

### Segmentation & market structure  (`segmentation-market-structure`)

1. **Clusters always appear; stability must be shown.** Any clustering algorithm returns k groups even in structureless data. The segment count must be chosen by a stated stability check (bootstrap or split-half agreement), so a solution that looks crisp once but reshuffles under resampling is rejected.
   - *Tempting shortcut:* Run k-means once, pick k from the elbow plot, and report the segments as real.
   - *What pins it:* The question asks for stable segments and names the resampling agreement measure and threshold a solution must pass.
2. **Size segments with posterior probabilities, not modal assignment.** In a latent class model each respondent has a probability of belonging to each class. Segment sizes and their uncertainty come from summing posterior probabilities and propagating parameter uncertainty; hard assignment to the most likely class biases sizes toward the larger classes.
   - *Tempting shortcut:* Assign everyone to their highest-probability class, count heads, and quote a binomial interval.
   - *What pins it:* The model is a latent class model and the prompt asks for segment sizes with intervals that reflect classification uncertainty.
3. **Scale-use style masquerades as attitude segments.** Respondents differ in how they use rating scales. Clustering raw agreement scores splits people into high raters and low raters rather than distinct attitudes, so ratings must be centred within respondent, or a forced-choice measure used, before clustering.
   - *Tempting shortcut:* Cluster the raw 1 to 7 agreement ratings directly.
   - *What pins it:* The stated procedure requires within-respondent standardisation of attitude batteries, or the battery is a best-worst design that removes scale use.
4. **Switching must be judged against share-based expectation.** Raw brand-switching counts mostly reflect brand size. Market partitions come from comparing observed duplication with the expectation under the duplication-of-purchase law; only excess duplication signals a closer competitive submarket.
   - *Tempting shortcut:* Call the brands with the most switchers between them the closest competitors.
   - *What pins it:* The prompt defines a submarket as pairs whose duplication exceeds the share-proportional expectation by a stated margin.

### Conjoint, choice & willingness-to-pay analysis  (`conjoint-choice-willingness-to-pay-analysis`)

1. **Logit simulators steal share from everyone equally.** Aggregate logit share simulation has the independence of irrelevant alternatives property: a near-clone takes share proportionally from all products. Simulations must use individual-level draws or a stated randomized first choice rule so a clone cannibalises mainly its twin.
   - *Tempting shortcut:* Plug aggregate part-worths into a single logit share formula and read off the new product's share.
   - *What pins it:* The task supplies individual-level posterior draws and names the simulation rule, and the scenario adds a product nearly identical to an existing one.
2. **WTP is a ratio of random utilities.** WTP equals an attribute utility divided by the price coefficient. Computing it per respondent draw and summarising with the stated statistic differs from dividing average utilities, and near-zero price coefficients make the mean explode, which is why the median is usually specified.
   - *Tempting shortcut:* Divide the mean attribute part-worth by the mean price coefficient.
   - *What pins it:* The prompt defines WTP as the population median of individual-level WTP computed across posterior draws.
3. **Preference share is not market share.** Shares among the tested profiles ignore buyers who would choose nothing. Volume forecasts must include the no-choice alternative as estimated, and only then apply any stated calibration to market data; dropping it inflates demand for every product.
   - *Tempting shortcut:* Report each product's share among the products shown as its expected market share.
   - *What pins it:* The design included a no-choice or dual-response option and the question asks for expected purchase volume, not relative preference.
4. **Do not simulate prices outside the tested range.** Part-worths are only identified at tested levels. Prices between levels are interpolated as the analysis plan states; a linear price coefficient extrapolated beyond the range invents a demand curve the experiment never measured, so out-of-range scenarios are reported as unsupported.
   - *Tempting shortcut:* Fit a linear price term and simulate any price management asks about.
   - *What pins it:* The prompt fixes the tested price levels, specifies piecewise-linear interpolation, and asks which in-range price maximises the stated objective.

### Brand, campaign & ad-effectiveness measurement  (`brand-campaign-ad-effectiveness-measurement`)

1. **Exposed versus unexposed is targeting, not lift.** Ad platforms show ads to people already likely to buy. Incremental lift must come from the randomized assignment contrast (intent to treat), divided by the exposure rate for the exposed, not from comparing people who saw the ad with those who did not.
   - *Tempting shortcut:* Compare conversion of exposed users with unexposed users and call the gap lift.
   - *What pins it:* The campaign had a randomized holdout and the question asks for lift caused by the campaign among exposed users.
2. **Compare exposed with would-have-been-exposed controls.** Exposed treated users differ from the whole control group, because only some users ever reach an ad slot. The valid comparison is with control users flagged as would-have-been-exposed (ghost ads) or an ITT divided by exposure rate.
   - *Tempting shortcut:* Compare exposed users in the test group with every user in the control group.
   - *What pins it:* The data carries a ghost-impression flag in the control arm and the estimand is the effect on users who were exposed.
3. **Carryover and saturation set marginal return.** Advertising works with delay and diminishing returns. A mix model must transform spend with the stated adstock decay and saturation curve; marginal return on the next dollar is the curve's slope at current spend, not the average return over all spend.
   - *Tempting shortcut:* Regress weekly sales on same-week spend and quote the coefficient as return per dollar.
   - *What pins it:* The prompt specifies the adstock and saturation forms and asks for marginal return at a stated spend increase.
4. **Geo tests have markets as the unit.** When regions are randomized, the independent units are the regions. Lift and its interval come from a market-level comparison using pre-period data (difference in differences or a synthetic control), not from millions of users treated as independent.
   - *Tempting shortcut:* Pool all users in test and control regions and run a user-level t-test.
   - *What pins it:* Assignment was by region, the number of regions is small, and the question asks whether lift is significant at a stated level.

### Customer satisfaction & driver analysis  (`customer-satisfaction-driver-analysis`)

1. **Correlated drivers need variance decomposition.** Service attributes are highly correlated, so multiple regression coefficients flip sign and size with small data changes. Relative importance must be shared out with the stated method, such as Shapley or relative weights, which split explained variance and sum to the total.
   - *Tempting shortcut:* Rank drivers by their standardised regression coefficients.
   - *What pins it:* The prompt asks for each attribute's share of explained variance in overall satisfaction using a named decomposition.
2. **Net Promoter change needs multinomial error.** NPS is the difference of two proportions from one multinomial sample, so its variance includes their covariance. Wave-to-wave changes must be tested with that variance; treating NPS as a mean of plus and minus scores mishandles it or ignores sampling noise entirely.
   - *Tempting shortcut:* Declare any NPS movement of a few points between waves a real change.
   - *What pins it:* The question asks whether the score changed between independent waves at a stated significance level.
3. **Penalties and rewards are asymmetric.** Some attributes hurt satisfaction when poor but add little when excellent, others the reverse. Penalty-reward analysis estimates the drop below adequate and the gain above it separately; one linear coefficient averages them and misclassifies basic needs as unimportant.
   - *Tempting shortcut:* Fit one linear slope per attribute and rank by it.
   - *What pins it:* The prompt asks for separate penalty and reward effects relative to a stated performance threshold.
4. **Link satisfaction to later loyalty behaviour.** Stated intent to return is measured with the same halo as satisfaction. Loyalty effects must use subsequent observed behaviour in a window after the survey, among all surveyed customers, so the predictor precedes the outcome and is not tautological.
   - *Tempting shortcut:* Correlate satisfaction with stated likelihood to repurchase from the same questionnaire.
   - *What pins it:* The prompt defines loyalty as renewal or repeat purchase observed within a stated period after the survey date.

### Media reach, frequency & audience measurement  (`media-reach-frequency-audience-measurement`)

1. **Channel reaches overlap; do not add them.** Combined reach counts unique people. Duplication must come from single-source panel data, where people exposed through several channels are counted once; summing channel reaches overstates, and the random-duplication formula misses the real correlation between heavy users.
   - *Tempting shortcut:* Add television, web and mobile reach together, or apply independence across channels.
   - *What pins it:* A single-source panel records each person's exposures across channels and the question asks for unduplicated reach.
2. **Average frequency hides who reaches threshold.** Effective reach at three or more exposures needs the frequency distribution, which is skewed: heavy viewers get many exposures and light viewers few. GRPs divided by reach gives an average that, applied to everyone, overstates effective reach.
   - *Tempting shortcut:* Compute average frequency and count everyone as reached at that frequency.
   - *What pins it:* The prompt defines effective reach at a stated minimum frequency and the panel supplies person-level exposure counts or a fitted distribution.
3. **Campaign reach is not summed weekly reach.** Reach accumulates at a decreasing rate because the same people are reached week after week. Campaign reach must be the share of persons with at least one exposure over the whole flight, so weekly figures cannot be added or averaged.
   - *Tempting shortcut:* Sum the weekly reach figures across the flight.
   - *What pins it:* The question asks for cumulative unique reach across the full campaign window with person-level data supplied.
4. **Project panel results with person weights.** Measurement panels over- and under-represent groups that differ in media use. Reach and frequency must be computed with each panelist's weight projected to the stated universe; unweighted panel proportions misstate reach whenever heavy users are over-represented.
   - *Tempting shortcut:* Report the unweighted share of panelists reached as population reach.
   - *What pins it:* The panel file supplies projection weights and a universe estimate, and the question asks for reach in that universe.

## General Statistics & Data Science  (`general-statistics-data-science`)

### Exploratory data analysis & distribution assessment  (`exploratory-data-analysis-distribution-assessment`)

1. **Judge outliers on the right scale.** Whether a point is anomalous depends on the scale where the data are roughly symmetric. On heavily right-skewed data, mean plus three SD flags legitimate tail values; robust or log-scale rules flag the genuine departures.
   - *Tempting shortcut:* Flag every value beyond three standard deviations of the raw mean.
   - *What pins it:* The prompt states the anomaly rule or the distributional assumption, so the flagged set is fixed.
2. **Stratify before reading a correlation.** A pooled association can reverse inside every stratum when group sizes differ (Simpson's paradox). Profiling must check the relationship within the grouping that generates the data before calling it a real signal.
   - *Tempting shortcut:* Report the pooled correlation or trend as the dataset's finding.
   - *What pins it:* The question names the comparison within groups or the grouping that defines units, fixing the stratified estimand.

### Regression, classification & model diagnostics  (`regression-classification-model-diagnostics`)

1. **Influence needs leverage and residual together.** A point moves the fit when it has both high leverage and a large residual, measured by Cook's distance or DFBETAS. High-leverage points that fall on the line, or large-residual points at the centre, change little.
   - *Tempting shortcut:* Drop every point with a large raw residual and refit.
   - *What pins it:* The prompt asks which observations change the coefficients, a stated influence measure with a threshold.
2. **Use leave-out residuals for misfit.** Raw residuals understate misfit at high-leverage points because the fit chases them. Studentised or leave-one-out residuals reveal the curvature or heteroskedasticity, and robust standard errors are needed when variance changes with the mean.
   - *Tempting shortcut:* Inspect raw residuals and keep classical standard errors.
   - *What pins it:* A stated diagnostic standard (externally studentised residuals, HC-type errors) fixes the conclusion.

### Resampling, simulation & Monte Carlo methods  (`resampling-simulation-monte-carlo-methods`)

1. **Resample the independent unit.** A bootstrap is valid only when it resamples the units that are independent: clusters, subjects or blocks of a time series. Resampling individual rows of correlated data understates variance and produces intervals that undercover.
   - *Tempting shortcut:* Resample rows with replacement regardless of grouping or time order.
   - *What pins it:* The data's design (repeated measures, clusters, serial dependence) dictates the resampling unit.
2. **Pick the interval for a biased statistic.** For skewed or biased nonlinear statistics, percentile intervals undercover; bias-corrected and accelerated intervals or studentised bootstrap restore coverage. A simulation from a known truth is how the coverage claim is checked.
   - *Tempting shortcut:* Take the 2.5th and 97.5th bootstrap percentiles and call coverage verified.
   - *What pins it:* The prompt requires verified coverage at a stated nominal level, which the simulation must demonstrate.

### Bayesian modeling & posterior inference  (`bayesian-modeling-posterior-inference`)

1. **Partial pooling, not raw or grand means.** Sparse group estimates should be shrunk toward the population mean in proportion to their noise, via a hierarchical model. Raw group means overstate extreme small groups; complete pooling erases real differences.
   - *Tempting shortcut:* Rank groups by their raw estimates, or replace all with the overall mean.
   - *What pins it:* The prompt asks for a hierarchical model on sparse groups, so partial pooling is the specified estimator.
2. **Report posterior predictive, not posterior mean.** A prediction for a new observation integrates parameter uncertainty and observation noise. Intervals from the posterior of the group mean are too narrow for a new unit or a new group, which also needs between-group variance.
   - *Tempting shortcut:* Use the credible interval for the group mean as the prediction interval.
   - *What pins it:* The prompt asks for posterior predictions for new units or groups, defining the predictive estimand.
3. **Prior sensitivity on the variance component.** With few groups, the prior on the between-group scale drives shrinkage. A sensitivity analysis must vary that scale prior, not only the location priors, because flat-looking priors on variance can be strongly informative.
   - *Tempting shortcut:* Vary the prior on the mean and declare results robust.
   - *What pins it:* The prompt asks for sensitivity to priors in a sparse hierarchical model, where the scale prior is the influential one.

### Missing data, censoring & measurement error  (`missing-data-censoring-measurement-error`)

1. **Rubin's rules combine imputations.** Multiple imputation estimates must be pooled with Rubin's rules: average the estimates, add within- and between-imputation variance. Averaging imputed datasets into one and analysing it, or using one imputation, understates uncertainty.
   - *Tempting shortcut:* Average the imputed values into a single dataset and fit once.
   - *What pins it:* The prompt asks for the association after multiple imputation, which defines the pooled estimate and its variance.
2. **Errors in a covariate attenuate.** Random error in a covariate biases its coefficient toward zero and leaks bias into correlated covariates. Correction uses the reliability or validation data (regression calibration, SIMEX); ignoring it understates the target association.
   - *Tempting shortcut:* Treat the error-prone covariate as measured exactly.
   - *What pins it:* Supplied replicate or validation measurements give the error variance, making the correction unique.
3. **Delta-adjust for nonignorable missingness.** Imputation assumes data are missing at random. Sensitivity to not-at-random missingness shifts imputed values by stated offsets and finds the shift that overturns the conclusion; complete-case analysis is not a sensitivity analysis.
   - *Tempting shortcut:* Compare complete-case and imputed results and call agreement robustness.
   - *What pins it:* The prompt names the sensitivity grid or tipping-point question for nonignorable missingness.

### Multiple testing & selective inference  (`multiple-testing-selective-inference`)

1. **FDR on the whole family tested.** Benjamini-Hochberg controls false discoveries only when applied to every hypothesis in the family. Running it on the subset that looked promising, or per subgroup, inflates the real error rate.
   - *Tempting shortcut:* Apply BH only to the tests that passed a first screen.
   - *What pins it:* The prompt defines the family of hypotheses, so the full set enters the procedure.
2. **Do not reuse data for selection.** P-values from a model chosen on the same data are biased toward significance. Valid inference uses sample splitting or a selective-inference correction conditioned on the selection event.
   - *Tempting shortcut:* Select variables by stepwise search, then report the final model's p-values.
   - *What pins it:* The prompt explicitly asks to account for data-driven model selection, ruling out naive post-selection p-values.

### Data integration, record linkage & entity resolution  (`data-integration-record-linkage-entity-resolution`)

1. **Propagate linkage error to estimates.** False and missed links bias downstream estimates: false matches attenuate associations, missed matches can select on linkability. The analysis must estimate match error from match weights or clerical review and correct or bound the estimate.
   - *Tempting shortcut:* Keep links above a score cutoff and analyse them as truth.
   - *What pins it:* The prompt asks to quantify linkage error in downstream estimates, so uncorrected results do not answer it.

### Benchmarking and ablations  (`benchmarking-and-ablations`)

1. **Compare runs with variance across seeds.** Differences between methods must exceed run-to-run variation, estimated over multiple seeds on the same splits and tested with a paired comparison. One run per arm turns noise into a ranking.
   - *Tempting shortcut:* Compare one run per configuration and rank by the higher score.
   - *What pins it:* The benchmark protocol states the number of seeds and the paired test, fixing whether the gap is real.
2. **Ablate one component against a fixed baseline.** An ablation attributes effect only when one component changes and tuning budget is equal. Comparing a tuned full system with untuned ablations credits the component for hyperparameter effort.
   - *Tempting shortcut:* Remove components from the tuned model without retuning and compare.
   - *What pins it:* The prompt states equal tuning budget or a fixed protocol, so the matched comparison is the estimand.

### Scaling laws  (`scaling-laws`)

1. **Fit scaling laws in log space with floors.** A power law with an irreducible loss floor is not linear in log-log space; fitting a straight line to raw losses biases the exponent. The fit must model the floor and weight points appropriately, judged by extrapolation to held-out scales.
   - *Tempting shortcut:* Regress log loss on log compute with ordinary least squares and extrapolate.
   - *What pins it:* The stated functional form and the held-out largest scales define the fit and its check.

### Robustness analysis  (`robustness-analysis`)

1. **Robustness on the deployment shift.** A robustness claim must be tested under the shift that matters (covariate shift, subgroup, perturbation family), reporting worst-group or shifted performance with uncertainty. Average accuracy on an in-distribution test set says nothing about it.
   - *Tempting shortcut:* Report overall test accuracy as evidence of robustness.
   - *What pins it:* The prompt names the shift or subgroups, which fixes the evaluation distribution and metric.

### Interpretability  (`interpretability`)

1. **Attributions under correlated features.** Permutation importance and marginal attribution methods break with correlated features: permuting one creates impossible rows and splits credit arbitrarily. Grouped or conditional importance answers which information the model relies on.
   - *Tempting shortcut:* Rank features by individual permutation importance and call the top one the driver.
   - *What pins it:* The prompt asks for importance of features known to be correlated, pinning grouped or conditional attribution.

## Biomedical & Clinical Research  (`biomedical-clinical-research`)

### Clinical trial design & analysis  (`clinical-trial-design-analysis`)

1. **Analyze as randomized, not as treated.** Randomization only protects comparisons of arms as assigned. Under a treatment-policy estimand, every randomized patient is analyzed in their assigned arm; dropping non-adherers or crossovers compares self-selected groups whose prognosis differs, usually exaggerating the benefit.
   - *Tempting shortcut:* Exclude patients who switched or stopped treatment and compare those who received each drug.
   - *What pins it:* The prompt or protocol names an intention-to-treat or treatment-policy primary analysis and the data records assigned arm separately from received treatment.
2. **Time-to-event trials are sized by events.** Power for a log-rank or Cox comparison depends on the number of events, not patients. The design must compute required events from the target hazard ratio, then patients from accrual, follow-up and expected event probability, including dropout.
   - *Tempting shortcut:* Apply a two-proportion sample size formula to the expected event rates and call that the enrollment target.
   - *What pins it:* The primary endpoint is time to event with a stated hazard ratio, accrual period, minimum follow-up and control median.

### Survival / time-to-event analysis  (`survival-time-to-event-analysis`)

1. **Competing deaths are not censoring.** When death from other causes prevents the event of interest, one minus Kaplan-Meier treating those deaths as censored estimates a hypothetical world without them and overstates cumulative incidence. The Aalen-Johansen cumulative incidence function, with Gray's test or Fine-Gray, answers the real-world question.
   - *Tempting shortcut:* Censor competing deaths and read event probability off one minus the Kaplan-Meier curve.
   - *What pins it:* The prompt asks for the actual probability of the event by a stated time and the data codes competing events separately.
2. **Responders versus non-responders needs a landmark.** Response is observed after baseline, so patients must survive long enough to respond. Comparing survival by response status from baseline credits responders with guaranteed survival time. A landmark analysis from a fixed time, or response as a time-varying covariate, removes that guaranteed time.
   - *Tempting shortcut:* Split patients by best response and compare Kaplan-Meier curves from randomization.
   - *What pins it:* The question compares survival by a status attained during follow-up and the data dates when each response occurred.

### Diagnostic & biomarker accuracy  (`diagnostic-biomarker-accuracy`)

1. **Partial verification biases accuracy.** When mostly test-positives receive the reference standard, sensitivity is inflated and specificity deflated. If verification depends only on the test result and recorded covariates, the Begg-Greenes correction or inverse probability of verification weighting recovers accuracy for the full tested population.
   - *Tempting shortcut:* Compute sensitivity and specificity from the verified patients only.
   - *What pins it:* The prompt targets accuracy in all tested patients and the data shows verification rates differing by test result.
2. **A cutoff tuned in-sample is optimistic.** Choosing the threshold that maximizes Youden's index on the same data, then reporting its sensitivity and specificity, overstates performance because the cutoff fits noise. The cutoff must be chosen in a development set or by cross-validation and accuracy reported on held-out data.
   - *Tempting shortcut:* Pick the Youden-optimal cutoff and report its sensitivity and specificity from the same sample.
   - *What pins it:* The prompt asks for expected accuracy of the chosen cutoff in new patients and supplies a separate validation split or resampling plan.

### Dose-response & PK/PD modeling  (`dose-response-pk-pd-modeling`)

1. **Relative and absolute ED50 differ.** When the fitted maximum falls short of the defined full response, the dose at half the fitted range differs from the dose giving fifty percent response. Fit a four-parameter logistic on log dose and compute the ED50 the question defines, with log-scale bounds.
   - *Tempting shortcut:* Fit a curve and report its midpoint parameter as the ED50 regardless of where the plateau sits.
   - *What pins it:* The prompt defines ED50 against a stated reference response, such as half of a fixed maximum, and the fitted top plateau falls short of it.
2. **AUC to infinity needs terminal extrapolation.** Exposure for single-dose bioequivalence or clearance uses AUC from zero to infinity: AUC to the last measurable concentration plus that concentration over the terminal rate constant, estimated from log-linear terminal points. Stopping at the last sample understates exposure unevenly across subjects.
   - *Tempting shortcut:* Sum linear trapezoids up to the final sampled time and use it as total exposure.
   - *What pins it:* The prompt asks for clearance or AUC infinity under a named noncompartmental standard, and sampling ends before concentrations are negligible.

### Genomics / GWAS & high-dimensional association  (`genomics-gwas-high-dimensional-association`)

1. **Ancestry confounds genotype association.** Allele frequencies and phenotype both vary by ancestry, so an unadjusted scan finds loci that track ancestry. Adjust for genetic principal components or fit a linear mixed model with a kinship matrix, and check the genomic inflation factor before declaring hits.
   - *Tempting shortcut:* Run per-variant regressions of phenotype on genotype with only age and sex as covariates.
   - *What pins it:* The prompt requires control of population structure and the cohort shows ancestry clusters or an inflated lambda without adjustment.
2. **Discovery effect sizes suffer winner's curse.** Variants selected for crossing a stringent threshold have effects biased away from zero, worst near the threshold. Predicted replication power or variance explained must use effects from an independent replication sample or a selection-bias correction, not the discovery estimates.
   - *Tempting shortcut:* Plug the discovery-scan effect sizes straight into the replication power or explained-variance calculation.
   - *What pins it:* The prompt asks for expected effect or power in a new cohort, and hits were chosen in the same data that estimated them.

### Statistical genomics  (`statistical-genomics`)

1. **Count data needs library-size normalization.** RNA-seq counts depend on sequencing depth and composition, and variance grows with the mean. Differential expression needs a negative binomial model with size-factor or TMM normalization and shrunken dispersions, then false discovery rate control across genes.
   - *Tempting shortcut:* Divide by total counts, log-transform, and run per-gene t-tests at an unadjusted 0.05 threshold.
   - *What pins it:* The prompt asks for differentially expressed genes at a stated false discovery rate from raw counts with a few replicates per group.
2. **The lead SNP is not the causal variant.** Linkage disequilibrium spreads a signal across correlated variants, so the top p-value is often not causal. Fine-mapping must compute posterior inclusion probabilities using an LD matrix from a matched panel and report the credible set reaching the stated coverage.
   - *Tempting shortcut:* Name the variant with the smallest p-value in each region as the causal variant.
   - *What pins it:* The prompt asks for a credible set at a stated probability and supplies summary statistics with an ancestry-matched LD reference.

### Longitudinal outcomes & repeated measures  (`longitudinal-outcomes-repeated-measures`)

1. **Completers analysis assumes dropout is random.** Patients who drop out often differ in trajectory. A mixed model for repeated measures uses all observed visits and is valid under missing at random; completers-only or last observation carried forward bias the endpoint. Delta-adjusted or tipping-point analyses then probe missing not at random.
   - *Tempting shortcut:* Analyze only patients with the final visit, or carry their last value forward.
   - *What pins it:* The prompt names an MMRM primary analysis with a stated sensitivity approach, and dropout varies by arm and earlier response.
2. **Adjust for baseline, not change alone.** When baseline differs by chance between arms, regression to the mean makes raw change scores biased toward the arm with worse baseline. ANCOVA of the follow-up value with baseline as a covariate gives the unbiased, more efficient randomized comparison.
   - *Tempting shortcut:* Compare mean change from baseline between arms with an unadjusted t-test.
   - *What pins it:* The analysis plan specifies a baseline-adjusted estimate and the arms show baseline imbalance with an outcome correlated over time.

### Adaptive, platform & basket trial methods  (`adaptive-platform-basket-trial-methods`)

1. **Compare arms with concurrent controls only.** In a platform trial, arms enter at different times while standard of care and case mix drift. Each arm should be compared with controls randomized during its own enrollment window, or with a model that adjusts for period; pooling all controls imports time trends.
   - *Tempting shortcut:* Pool every control patient ever enrolled as the comparator for each experimental arm.
   - *What pins it:* The prompt specifies concurrent-control comparisons, and arm entry dates show controls accrued well before some arms opened.
2. **Interim looks spend alpha.** Repeated testing at nominal significance inflates type I error. Boundaries must come from the prespecified spending function, such as O'Brien-Fleming type, recomputed at the actual information fraction observed at each look, not the planned one.
   - *Tempting shortcut:* Test at the final significance level at every interim and stop at the first significant look.
   - *What pins it:* The protocol names a Lan-DeMets spending function and the interim occurred at an event count different from plan.

### Real-world evidence & comparative effectiveness  (`real-world-evidence-comparative-effectiveness`)

1. **Align time zero in target trial emulation.** Eligibility, treatment assignment and start of follow-up must coincide, as in the trial being emulated. Starting follow-up at diagnosis but classifying by later treatment grants immortal time to treated patients; cloning with a grace period or a sequential trial design avoids it.
   - *Tempting shortcut:* Define exposure as ever receiving the drug and follow everyone from diagnosis.
   - *What pins it:* The prompt names the target trial protocol with a time zero and grace period, and initiation dates trail eligibility.
2. **Per-protocol emulation needs inverse censoring weights.** Censoring patients when they deviate from their assigned strategy is informative because deviation depends on evolving prognosis. Weight remaining follow-up by inverse probability of staying uncensored given time-varying covariates, then standardize to get marginal risks and the one-year risk difference.
   - *Tempting shortcut:* Censor deviators and read the hazard ratio from an unweighted Cox model.
   - *What pins it:* The prompt asks for a per-protocol one-year risk difference and the data records time-varying covariates predicting treatment switching.

### Medical imaging & reader-study evaluation  (`medical-imaging-reader-study-evaluation`)

1. **Readers and cases are both random.** To generalize to new readers and new cases, the AUC difference needs variance from both sources and their interaction, using Obuchowski-Rockette or Dorfman-Berbaum-Metz. Pooling all reads as independent, or fixing readers, gives intervals far too narrow.
   - *Tempting shortcut:* Pool every reader's scores into one ROC per modality and compare with a DeLong test.
   - *What pins it:* The prompt asks whether the workflow helps readers in general, from a fully crossed multi-reader multi-case design.
2. **Lesions within a patient are clustered.** Multiple lesions or images from one patient share anatomy and reader impressions, so treating each as independent shrinks standard errors and overweights multi-lesion patients. Analyze at the patient level the question names, or use cluster-robust or JAFROC methods for localization.
   - *Tempting shortcut:* Treat every lesion or image as an independent unit when computing sensitivity and its interval.
   - *What pins it:* The prompt defines performance per patient or requires lesion localization, and patients contribute varying numbers of findings.

## Epidemiology & Public Health  (`epidemiology-public-health`)

### Observational study design (cohort / case-control)  (`observational-study-design-cohort-case-control`)

1. **Sample controls from the risk set.** Controls must represent the exposure distribution of the population that gave rise to the cases. Incidence-density sampling from those at risk at each case's time makes the odds ratio estimate the rate ratio; controls drawn from survivors or a convenience source do not.
   - *Tempting shortcut:* Take all non-cases at the end of follow-up, or hospital patients, as controls.
   - *What pins it:* The prompt asks for the incidence rate ratio from a nested case-control design within a defined cohort.
2. **Matched designs need conditional analysis.** Matching on a confounder introduces selection that only a matched-set analysis removes. Individually matched data must be analysed with conditional logistic regression or discordant-pair methods; an unmatched analysis typically biases the odds ratio toward the null.
   - *Tempting shortcut:* Pool matched cases and controls and fit ordinary logistic regression.
   - *What pins it:* Controls were individually matched to cases on stated factors and matched-set identifiers are given.
3. **Define exposure at baseline to avoid immortal time.** If exposure is defined by something occurring after cohort entry, the exposed must survive until it happens. Person-time before exposure must be classified as unexposed (time-varying exposure) or a landmark used, or the exposed get guaranteed survival.
   - *Tempting shortcut:* Classify people as exposed from entry if they were ever exposed during follow-up.
   - *What pins it:* The prompt fixes time zero at cohort entry and exposure begins later for some members.

### Disease surveillance & outbreak / anomaly detection  (`disease-surveillance-outbreak-anomaly-detection`)

1. **Compare against the seasonal baseline.** Many diseases rise every year at the same time. Expected counts must come from the same weeks in prior seasons, with trend and with past outbreak weeks downweighted, as in Farrington or Serfling methods; comparing with recent weeks flags normal seasonal increases.
   - *Tempting shortcut:* Compare this week's count with the average of the last few weeks.
   - *What pins it:* The prompt names the baseline algorithm and number of prior seasons, and asks whether the excess crosses its threshold.
2. **Recent weeks are incomplete; nowcast them.** Cases are reported with delay, so the latest weeks are undercounted and appear to fall. Recent counts must be corrected with the empirical reporting delay distribution before judging trend.
   - *Tempting shortcut:* Read the latest weeks' raw counts as the current trend.
   - *What pins it:* The data includes report dates so the delay distribution is estimable, and the question asks about trend in the latest weeks.
3. **Testing volume changes the count.** Case counts rise when testing rises. A real increase in transmission must show in test positivity or in counts adjusted for testing effort, not just raw counts that move with test volume.
   - *Tempting shortcut:* Treat a rise in confirmed cases as a rise in infection.
   - *What pins it:* The surveillance stream reports tests performed, and the outbreak definition in the prompt is based on positivity or adjusted rate.

### Risk-factor & causal effect estimation  (`risk-factor-causal-effect-estimation`)

1. **Odds ratios overstate common-outcome risk ratios.** When the outcome is common, the odds ratio is further from one than the risk ratio. A requested risk ratio must come from a log-binomial or modified Poisson model, or standardisation, not from logistic regression output.
   - *Tempting shortcut:* Report the adjusted logistic odds ratio as the risk ratio.
   - *What pins it:* The prompt asks for an adjusted risk ratio in a cohort where the outcome is common.
2. **Adjusted PAF uses cases' exposure prevalence.** With confounding, the population attributable fraction must use the proportion of cases exposed and the adjusted risk ratio (Miettinen's formula). Plugging an adjusted ratio into Levin's formula with population prevalence gives a biased fraction.
   - *Tempting shortcut:* Use Levin's formula with population prevalence and the adjusted risk ratio.
   - *What pins it:* The prompt asks for the attributable fraction based on the confounder-adjusted risk ratio.
3. **Do not adjust for mediators of total effect.** Adjusting for a variable on the path from exposure to outcome removes part of the effect being estimated, and adjusting for a collider creates bias. The adjustment set must follow the stated causal diagram for the total effect.
   - *Tempting shortcut:* Adjust for every variable associated with exposure and outcome.
   - *What pins it:* The prompt supplies a causal diagram and asks for the total effect of exposure.

### Screening & diagnostic-policy evaluation  (`screening-diagnostic-policy-evaluation`)

1. **Survival from diagnosis rewards lead time.** Screening detects disease earlier, so survival from diagnosis lengthens even if death is not delayed. Benefit must be judged by disease-specific mortality per person randomised, comparing arms, not by survival among diagnosed cases.
   - *Tempting shortcut:* Compare five-year survival of screen-detected cases with clinically detected cases.
   - *What pins it:* The prompt provides a randomised trial with deaths per arm and asks whether screening reduces mortality.
2. **Overdiagnosis shows as persistent excess incidence.** Screening finds slow disease that would never cause harm. Overdiagnosis is estimated as excess cumulative incidence in the screened arm after follow-up long enough for lead time to be caught up, so detected cases are not all benefits.
   - *Tempting shortcut:* Count every additional screen-detected case as a case prevented from progressing.
   - *What pins it:* The prompt gives cumulative incidence by arm with follow-up beyond the screening period and defines overdiagnosis that way.
3. **Predictive value depends on prevalence.** Sensitivity and specificity transfer across settings; predictive values do not. Positive predictive value in the target population must be recomputed from the target prevalence, which in a low-prevalence screening population is much lower than in a study enriched with cases.
   - *Tempting shortcut:* Use the positive predictive value reported in the validation study.
   - *What pins it:* The prompt states target population prevalence and asks for false positives per true positive in that population.

### Health-burden & impact modeling  (`health-burden-impact-modeling`)

1. **Years of life lost use a reference table.** DALYs combine YLL and YLD. YLL counts deaths at each age times the remaining life expectancy from the stated reference life table, not the population's average life expectancy minus mean age at death.
   - *Tempting shortcut:* Compute YLL as deaths times life expectancy minus average age at death.
   - *What pins it:* The prompt names the reference life table and asks for DALYs by age group.
2. **Potential impact fraction is not scaled PAF.** The burden averted by cutting exposure depends on the shifted exposure distribution compared with the current one. It must be computed as the potential impact fraction against the stated counterfactual, not by multiplying the full PAF by the percentage reduction.
   - *Tempting shortcut:* Multiply the attributable fraction by twenty percent.
   - *What pins it:* The prompt specifies the exposure distribution, the relative risk function and the intervention shift.

### Infectious-disease transmission modeling  (`infectious-disease-transmission-modeling`)

1. **Rt needs onset timing and generation interval.** The reproduction number turns growth into transmission via the generation or serial interval. Estimation must use incidence by onset or infection date with the stated interval distribution, as in renewal-equation methods; report dates and the wrong interval give different Rt.
   - *Tempting shortcut:* Compute Rt as the ratio of this week's reported cases to last week's.
   - *What pins it:* The prompt specifies the serial interval distribution and supplies onset dates or a delay distribution.
2. **R comes from the next-generation matrix.** In an age-structured model the reproduction number is the dominant eigenvalue of the next-generation matrix built from contacts, susceptibility and infectiousness. Intervention effects must be computed on that eigenvalue, not as a population-weighted average of age-specific contact reductions.
   - *Tempting shortcut:* Average age-specific reductions in contact weighted by population size.
   - *What pins it:* The prompt supplies a contact matrix and age-specific parameters and asks for R under each intervention scenario.

### Cluster, stepped-wedge & community trials  (`cluster-stepped-wedge-community-trials`)

1. **Stepped wedge confounds calendar time.** In a stepped-wedge trial later periods have more clusters treated, so a secular trend looks like effect. Analysis must include period effects and compare treated with not-yet-treated clusters in the same period, not before and after within clusters.
   - *Tempting shortcut:* Compare outcomes before and after each cluster's crossover, pooled.
   - *What pins it:* Crossover dates are staggered by design and the question asks for the intervention effect adjusted for secular trend.
2. **Clusters, not individuals, carry the information.** Outcomes correlate within clusters, so the effective sample size is governed by the number of clusters and the intraclass correlation. Inference must account for clustering, with the stated small-sample correction when clusters are few.
   - *Tempting shortcut:* Analyse individuals as independent observations.
   - *What pins it:* Randomisation was by cluster, the number of clusters is small, and the prompt asks for a confidence interval at a stated level.

### Health equity & disparity decomposition  (`health-equity-disparity-decomposition`)

1. **Age-standardise before comparing group rates.** Preventable hospitalisation rates rise steeply with age, and groups differ in age structure. Disparities must be compared using rates standardised to the stated standard population; crude rate gaps mix age composition with real differences.
   - *Tempting shortcut:* Compare crude hospitalisation rates between groups.
   - *What pins it:* The prompt names the standard population and asks for the age-adjusted rate ratio or difference.
2. **Decomposition shares depend on the reference.** Explained and unexplained parts of a gap depend on which group's coefficients are used, and binary outcomes need a nonlinear decomposition. The split must follow the stated reference and method; swapping references changes the answer.
   - *Tempting shortcut:* Use a linear Oaxaca decomposition with whichever group's coefficients come first.
   - *What pins it:* The prompt specifies the decomposition method and reference coefficients, and asks for the explained share.

## Pharmacology, Pharmacoepidemiology & Safety  (`pharmacology-pharmacoepidemiology-safety`)

### Population pharmacokinetics & exposure response  (`population-pharmacokinetics-exposure-response`)

1. **Covariate effects need the random effects.** Covariate effects on clearance are estimated within a mixed-effects model where between-subject variability is random. Regressing individual post-hoc clearances on covariates uses shrunk estimates and understates or distorts effects when data are sparse.
   - *Tempting shortcut:* Fit each subject separately or take empirical Bayes estimates, then regress them on covariates.
   - *What pins it:* The prompt asks for covariate effects in a nonlinear mixed-effects model, fixing the population estimand.
2. **Allometric weight scaling is a model choice.** Body size effects on clearance and volume follow fixed or estimated allometric exponents centred on a reference weight. A linear weight term, or uncentred scaling, changes the typical value and the covariate interpretation across the range.
   - *Tempting shortcut:* Add body weight as a linear covariate on clearance.
   - *What pins it:* The stated covariate model or reference weight in the analysis plan defines the parameterisation.
3. **Exposure response confounded by clearance.** At a fixed dose, higher-exposure patients have lower clearance, which can track disease severity. A naive concentration-response slope then mixes drug effect with prognosis; multiple dose levels or adjusting for clearance determinants separate them.
   - *Tempting shortcut:* Regress response on observed exposure within one dose arm.
   - *What pins it:* The design (several randomised doses) or stated adjustment identifies the causal exposure-response slope.
4. **Model the BLQ observations.** Concentrations below the quantification limit are censored, not zero or missing. Dropping them or imputing half the limit biases terminal half-life and clearance; likelihood-based censoring handles them correctly.
   - *Tempting shortcut:* Delete below-limit samples or replace them with half the limit.
   - *What pins it:* The analysis plan states the censored-likelihood method for BLQ data, fixing the estimates.

### Drug utilization & comparative safety  (`drug-utilization-comparative-safety`)

1. **New users only, from first fill.** Comparing prevalent users includes people who tolerated the drug and survived early risk. A new-user design starts follow-up at first dispensing after a washout, with covariates measured before that date.
   - *Tempting shortcut:* Include everyone with any prescription in the window and start follow-up at cohort entry.
   - *What pins it:* The prompt names a new-user active-comparator design, which defines the cohort and time zero.
2. **No immortal time between entry and exposure.** Classifying patients as exposed by a prescription filled after follow-up starts credits them with event-free time before exposure. Time zero must coincide with treatment assignment, or exposure must be time-varying.
   - *Tempting shortcut:* Define exposure as ever filling the drug during follow-up and compare from the diagnosis date.
   - *What pins it:* The stated cohort entry and exposure definitions require aligned time zero.
3. **Pick on-treatment or initial-treatment and censor.** An as-treated analysis censors at discontinuation or switching, with a grace period and stated risk window after the last supply; initial-treatment analysis ignores later changes. Mixing them, or ignoring informative censoring, gives a different hazard ratio.
   - *Tempting shortcut:* Count all events in a fixed window regardless of whether patients stayed on the drug.
   - *What pins it:* The protocol states the exposure risk window, grace period and censoring rule.
4. **Weights must balance the stated covariates.** Propensity score weights or matching must achieve balance (standardised differences) on measured confounders, and the estimand (ATE vs ATT) follows from the weighting scheme. Adjusting for post-baseline variables blocks the causal path.
   - *Tempting shortcut:* Put every available variable, including ones after drug start, in an outcome regression.
   - *What pins it:* The prompt or plan names the estimand and baseline covariate window, fixing the weighting and adjustment set.

### Safety-signal detection  (`safety-signal-detection`)

1. **Disproportionality needs shrinkage for sparse cells.** Reporting odds ratios with a handful of reports are unstable; Bayesian shrinkage (information component, empirical Bayes geometric mean) or lower credibility bounds rank signals sensibly. Ranking by raw ratio promotes noise.
   - *Tempting shortcut:* Rank drug-event pairs by their crude reporting odds ratio.
   - *What pins it:* The stated signal criterion (lower bound threshold, minimum count) defines which pairs qualify.
2. **Mask confounding by indication and notoriety.** Spontaneous report disproportionality reflects reporting patterns: events tied to the indication, or stimulated reporting after publicity. The comparator background and stratification by period or indication must be stated before calling a signal.
   - *Tempting shortcut:* Compare against all other reports in the database without stratifying.
   - *What pins it:* The prompt specifies the comparator background and stratification, which fixes the disproportionality estimate.
3. **Reports are not incidence.** Spontaneous reports lack a denominator and are subject to underreporting, so a disproportionality signal prioritises review; it does not estimate risk or compare drug safety. Prioritisation should use the stated clinical criteria alongside the statistic.
   - *Tempting shortcut:* Divide report counts by prescriptions and present it as the adverse-event rate.
   - *What pins it:* The prompt asks to prioritise signals for clinical review, so the output is a ranked list, not a risk estimate.
4. **Sequential surveillance spends alpha.** Repeatedly testing accumulating data inflates false alarms unless a sequential method (maximised SPRT, group sequential bounds) is used with a planned alpha spending. Re-running a fixed-sample test each period overstates signals.
   - *Tempting shortcut:* Run a standard test each month and flag the first significant result.
   - *What pins it:* The surveillance plan states the sequential method and total alpha, fixing the signalling time.

### Benefit-risk assessment  (`benefit-risk-assessment`)

1. **Absolute risks, not relative, drive benefit-risk.** Benefit-risk compares events prevented with events caused per patients treated, which depends on baseline risk. Constant relative effects imply very different net benefit across subgroups; comparing hazard ratios hides it.
   - *Tempting shortcut:* Compare relative risk reduction with relative harm increase.
   - *What pins it:* The prompt asks for subgroup benefit-risk, which requires absolute differences at each subgroup's baseline risk.
2. **Weight outcomes with stated preferences.** Net clinical benefit sums outcomes with weights reflecting their severity; unweighted sums treat a stroke and a minor bleed as equal. Weights and their sensitivity range must come from the stated framework.
   - *Tempting shortcut:* Add up all efficacy and safety events with equal weight.
   - *What pins it:* The benefit-risk framework in the prompt supplies the outcome weights and decision threshold.
3. **Subgroup effects need interaction tests.** Declaring benefit in one subgroup and not another because one p-value crosses the threshold is not evidence of difference. Heterogeneity is assessed by a treatment-by-subgroup interaction with its uncertainty.
   - *Tempting shortcut:* Call the subgroup with a significant effect the one that benefits.
   - *What pins it:* The prompt asks whether profiles differ across subgroups, which is an interaction estimand.
4. **Benefit-risk under competing risks.** When death prevents later events, Kaplan-Meier one-minus-survival overstates cumulative incidence of bleeding or efficacy endpoints. Cumulative incidence functions treat death as a competing event.
   - *Tempting shortcut:* Use one minus Kaplan-Meier for each event, censoring deaths.
   - *What pins it:* The outcome definitions and the presence of high mortality make cumulative incidence the stated quantity.

### Medication adherence & persistence  (`medication-adherence-persistence`)

1. **Truncate PDC to the observation window.** Proportion of days covered counts covered days within the window, shifting overlapping fills forward and handling hospital stays as stated. Medication possession ratio sums days supplied and can exceed one, inflating adherence.
   - *Tempting shortcut:* Sum days supplied and divide by window length.
   - *What pins it:* The adherence definition in the prompt (PDC with carryover and an 80% threshold) fixes each patient's value.
2. **Persistence gap defines discontinuation.** Persistence ends when the gap after supply runs out exceeds the permissible gap; patients still persistent at end of data or who die are censored. Treating end of follow-up as discontinuation biases persistence downward.
   - *Tempting shortcut:* Mark anyone without a fill at study end as discontinued.
   - *What pins it:* The stated gap length and censoring rules make the persistence curve unique.
3. **Healthy adherers mislead outcome links.** Adherent patients have better outcomes even on placebo, so adherence-outcome associations overstate drug benefit. Rigor uses an adherence-to-unrelated-drug negative control or comparison to placebo-arm adherers.
   - *Tempting shortcut:* Regress outcomes on adherence and read the coefficient as the drug's effect.
   - *What pins it:* The prompt explicitly asks to address healthy-adherer bias, requiring a negative control or equivalent.
4. **Measure adherence before the outcome.** Adherence measured over the whole follow-up includes the period after an event, when patients may stop drugs or be hospitalised. Exposure must be assessed in a window preceding the outcome, or as time-varying, to avoid reverse causation.
   - *Tempting shortcut:* Compute adherence across all follow-up and relate it to events during the same period.
   - *What pins it:* The stated exposure assessment window precedes outcome ascertainment, fixing the temporal ordering.

## Healthcare Delivery & Health Economics  (`healthcare-delivery-health-economics`)

### Cost-effectiveness & decision modeling  (`cost-effectiveness-decision-modeling`)

1. **Rank strategies incrementally after removing dominance.** With three or more options, ICERs must be computed between adjacent non-dominated strategies ordered by cost, after dropping strictly and extendedly dominated ones. ICERs against a common baseline can make a weakly efficient option look acceptable and pick the wrong strategy.
   - *Tempting shortcut:* Compute every option's ICER against usual care and choose the one under the threshold with most QALYs.
   - *What pins it:* The prompt names a willingness-to-pay threshold and asks which of several mutually exclusive strategies is cost-effective.
2. **Probability cost-effective comes from net benefit.** The probability a strategy is cost-effective is the share of probabilistic draws where its net monetary benefit is highest at the threshold. Counting draws with ICER below threshold misclassifies draws where the option is cheaper and worse, or dearer and better with negative increments.
   - *Tempting shortcut:* Count simulation draws whose ICER falls below the threshold.
   - *What pins it:* The task asks for the probability each treatment is cost-effective at a stated threshold from supplied PSA draws.
3. **Convert rates, not probabilities, across cycle lengths.** Transition probabilities reported for one interval must be turned into a rate and back for the model's cycle length, p = 1 - exp(-r t). Dividing an annual probability by twelve overstates monthly risk compounding errors over a lifetime horizon and shifts QALYs.
   - *Tempting shortcut:* Divide the annual event probability by the number of cycles per year.
   - *What pins it:* Source estimates are annual probabilities while the stated Markov model runs on monthly or shorter cycles.
4. **Apply within-cycle correction to discrete Markov traces.** A Markov trace counts membership at cycle boundaries, but transitions happen during cycles. Costs and QALYs must use the stated half-cycle or trapezoidal correction, then discount by cycle time, or life expectancy and lifetime costs are biased by about half a cycle per patient.
   - *Tempting shortcut:* Sum state membership at the start of each cycle times utility and cost, then discount by year.
   - *What pins it:* The prompt specifies a cycle-based cohort model with a stated within-cycle correction and discount rate for costs and QALYs.

### Utilization, access & demand forecasting  (`utilization-access-demand-forecasting`)

1. **Observed visits are capped demand, not need.** Where access is constrained, completed visits undercount demand: patients who left without being seen, were diverted, or were turned away by full schedules are missing. Unmet need is estimated from total arrivals or referrals against capacity, not by extrapolating completed encounters.
   - *Tempting shortcut:* Forecast demand by trending completed visits and call the gap to some benchmark unmet need.
   - *What pins it:* The prompt defines demand as all presentations or referrals, and walkout, diversion or waitlist counts are part of the source.
2. **Project demand with age-specific rates.** Future demand should be age-sex-specific utilization rates applied to the projected population structure. Trending total visits ignores ageing: a population with flat headcount but a growing older share needs more emergency and specialty care than the aggregate trend implies.
   - *Tempting shortcut:* Fit a linear trend to total annual visits and extend it to the target year.
   - *What pins it:* The prompt supplies age-band population projections and asks for demand in a future year by location.
3. **Measure access with floating catchments.** Spatial access depends on supply and competing demand across boundaries. A two-step floating catchment computes each provider's supply-to-population ratio within the stated travel threshold, then sums ratios reachable from each residence. Within-area provider-per-capita ratios ignore cross-border use and misrank shortage areas.
   - *Tempting shortcut:* Divide providers located in each area by that area's population.
   - *What pins it:* The task states a travel-time catchment and asks which resident areas fall below an access standard.
4. **Plan capacity to an overdispersed quantile.** Daily arrival counts are overdispersed relative to Poisson because of seasonality, weather and outbreaks. Capacity covering a stated percentile of days needs a negative binomial or empirical quantile; Poisson intervals around the mean forecast are too narrow and undersize coverage.
   - *Tempting shortcut:* Set capacity at the forecast mean plus a Poisson-based margin.
   - *What pins it:* The prompt asks for capacity meeting demand on a stated share of days, and count variance clearly exceeds the mean.

### Provider quality & risk adjustment  (`provider-quality-risk-adjustment`)

1. **Risk adjust only for present-on-admission factors.** Risk models must use conditions present before or at admission. Adjusting for complications or diagnoses acquired in hospital credits poor care as patient severity, so hospitals that cause harm look expected rather than unusual.
   - *Tempting shortcut:* Include every coded secondary diagnosis on the claim as a risk factor.
   - *What pins it:* The measure specification defines risk factors from prior encounters or present-on-admission flags only.
2. **Indirectly standardized ratios do not rank hospitals.** An observed-to-expected ratio compares each hospital to the reference population applied to its own case mix. Two hospitals' ratios are not directly comparable when case mixes differ; head-to-head comparison needs direct standardization or a common case mix.
   - *Tempting shortcut:* Rank hospitals by O/E ratio and declare the lower one better than its peer.
   - *What pins it:* The prompt asks whether one specific hospital outperforms another, not whether each differs from the expected benchmark.
3. **Shrink small hospitals toward the mean.** Raw rates from low-volume hospitals are noisy, so they populate both extremes of any ranking. A hierarchical model shrinks each hospital toward the overall mean in proportion to its reliability; the stated predicted-over-expected ratio then reflects signal, not volume.
   - *Tempting shortcut:* Rank hospitals by raw risk-adjusted rate and flag the top and bottom tails.
   - *What pins it:* The prompt names a random-effects or shrinkage method, as in standard public reporting, and volumes vary widely.
4. **Flag outliers with overdispersed funnel limits.** Unusual performance is judged against control limits that widen as volume falls. When unexplained between-hospital variation exists, limits must be inflated for overdispersion, or far too many hospitals are flagged. Fixed percentile cutoffs ignore volume entirely.
   - *Tempting shortcut:* Flag the worst decile, or every hospital outside plain binomial limits.
   - *What pins it:* The task asks for statistically unusual providers at a stated confidence level using funnel or control-limit methods.

### Patient flow, beds & workforce optimization  (`patient-flow-beds-workforce-optimization`)

1. **Size beds by blocking probability, not occupancy.** Delay rises nonlinearly as occupancy approaches capacity, and small units feel it most. Bed numbers must come from a queueing or loss model meeting the stated probability of delay or refusal; dividing mean census by a target occupancy undersizes small units.
   - *Tempting shortcut:* Beds = average daily census divided by an 85 percent occupancy target.
   - *What pins it:* The prompt sets a service standard as a maximum probability of waiting or being turned away.
2. **Staff to the hourly arrival curve.** Arrivals peak by hour and weekday, and queues build during peaks and drain afterward. Staffing must follow a time-varying or lagged model of the arrival curve; a stationary model on the daily average shows adequate capacity while peak waits breach the standard.
   - *Tempting shortcut:* Compute required staff from the average hourly arrival rate across the day.
   - *What pins it:* Arrivals are given by hour of day and the standard applies to every hour, not on average.
3. **Fix the downstream bottleneck causing boarding.** Emergency boarding is usually blocking from inpatient beds, driven by discharge timing and inpatient occupancy. A flow model linking admissions, transfers and discharges shows that adding emergency capacity does not reduce boarding; earlier discharges or inpatient capacity do.
   - *Tempting shortcut:* Add emergency beds or staff in proportion to boarding hours.
   - *What pins it:* The prompt asks which intervention reduces boarding, and data cover admission, transfer and discharge times across units.
4. **Staffing ratios bind per unit and shift.** Mandated nurse-to-patient ratios are integer constraints that apply in every unit and shift. Solving a relaxed model or meeting ratios on average across units, then rounding, produces schedules that breach the mandate somewhere.
   - *Tempting shortcut:* Solve a continuous staffing model and round to whole nurses, or check ratios on pooled totals.
   - *What pins it:* The stated rule sets minimum ratios per unit per shift and asks for a minimum-cost feasible roster.

### Payment, claims & health-plan analytics  (`payment-claims-health-plan-analytics`)

1. **Complete recent claims before comparing periods.** Recent service months are incomplete because claims arrive with lag. Costs must be completed with development or completion factors from lag triangles before comparing pre and post periods, or the latest period looks artificially cheap.
   - *Tempting shortcut:* Compare paid amounts by service month as they appear in the extract.
   - *What pins it:* The prompt asks for incurred cost by service period, and the extract has a paid-through date soon after period end.
2. **Evaluate voluntary bundles against a comparison group.** Providers that choose bundled payment differ from those that do not, and episode spending trends independently. The effect needs a difference-in-differences against comparable non-participants with checked pre-trends; a pre-post change in participants absorbs secular trend and selection.
   - *Tempting shortcut:* Report the participants' change in average episode spending before versus after joining.
   - *What pins it:* Participation was voluntary, the prompt asks for the program effect, and non-participant episodes are available.
3. **Apply reconciliation steps in contract order.** Bundled reconciliation follows a stated order: winsorize outlier episodes, compare to the target price, apply discount, then stop-loss and stop-gain caps. Changing the order, or capping episodes instead of the provider total, shifts each provider's risk exposure.
   - *Tempting shortcut:* Sum raw episode costs against target and cap each episode's loss.
   - *What pins it:* The contract terms state the outlier truncation, discount and aggregate stop-loss sequence used to settle payment.
4. **Risk-adjust PMPM as a ratio of totals.** Plan cost per member per month divides total cost by total member months, then by the member-month-weighted average risk score. Averaging each member's PMPM or using enrollee counts overweights short enrollees and misstates risk-adjusted cost.
   - *Tempting shortcut:* Average each member's monthly cost, or divide total cost by enrollee count times twelve.
   - *What pins it:* The prompt asks for risk-adjusted PMPM, and members enroll and disenroll during the year.

## Economics & Econometrics  (`economics-econometrics`)

### Causal identification (DiD / IV / RD / synthetic control)  (`causal-identification-did-iv-rd-synthetic-control`)

1. **Staggered adoption breaks naive two-way FE.** With staggered timing and effects that change over time, two-way fixed effects uses already-treated units as controls and can put negative weights on some cohorts. Estimate cohort-by-period effects against never- or not-yet-treated units, then aggregate with stated weights.
   - *Tempting shortcut:* Run one two-way fixed effects regression with a post-treatment dummy and report its coefficient.
   - *What pins it:* The prompt states staggered adoption and defines the estimand as the average effect on the treated, aggregated by cohort or event time.
2. **Weak instruments need robust inference.** A weak first stage biases 2SLS toward OLS and makes conventional t-tests reject too often. Report the first-stage F (the effective F under clustering) and use weak-instrument robust inference such as Anderson-Rubin confidence sets before calling the effect significant.
   - *Tempting shortcut:* Report the 2SLS point estimate with its conventional standard error as if the instrument were strong.
   - *What pins it:* The task states that significance is judged with a weak-IV robust confidence set or a named first-stage strength threshold.
3. **Regression discontinuity is local, not global.** RD identifies the effect only at the cutoff. Fit local linear regressions inside a data-driven bandwidth with a triangular kernel and check for sorting in the running-variable density. Global high-order polynomials let distant observations drive the jump estimate.
   - *Tempting shortcut:* Fit a global quartic in the running variable across the whole sample and read the jump.
   - *What pins it:* The prompt names a sharp cutoff, a local linear estimator and the bandwidth selector, leaving one defensible estimate.
4. **Synthetic control uses placebo-rank inference.** With one treated unit, regression standard errors mean nothing. Fit donor weights on pre-period outcomes, exclude donors hit by similar shocks, and judge significance by where the treated unit's post-to-pre RMSPE ratio ranks among in-space placebo runs.
   - *Tempting shortcut:* Run a t-test of the post-period treated-minus-synthetic gaps against zero.
   - *What pins it:* The task specifies permutation inference over placebo units, a donor exclusion rule and the rank needed to declare an effect.

### Structural / equilibrium modeling  (`structural-equilibrium-modeling`)

1. **Price is endogenous in demand estimation.** Firms set prices knowing unobserved product quality, so OLS of log share ratios on price biases the price coefficient toward zero and makes demand look inelastic. Instrument price with cost shifters or rival characteristics; markups and merger effects follow from that estimate.
   - *Tempting shortcut:* Regress log share minus log outside share on price and characteristics by OLS.
   - *What pins it:* The task supplies valid instruments and requires the IV demand estimates to drive the merger simulation.
2. **Merger simulation solves a new equilibrium.** Back out marginal costs from pre-merger Bertrand first-order conditions under the pre-merger ownership matrix, then re-solve all prices jointly under the merged ownership. Rivals respond, so the post-merger prices are a fixed point, not a one-step markup.
   - *Tempting shortcut:* Apply a single percentage price rise from diversion ratios or upward pricing pressure and stop.
   - *What pins it:* The prompt states Bertrand-Nash pricing with constant marginal cost and asks for equilibrium post-merger prices.

### Time-series & macro-econometrics  (`time-series-macro-econometrics`)

1. **Cointegration tests use their own critical values.** Regressing one integrated series on another in levels produces high R-squared and significant t-statistics even when unrelated. Test unit roots first, then test cointegration with Engle-Granger residual or Johansen critical values, not standard Dickey-Fuller or t tables.
   - *Tempting shortcut:* Run OLS in levels and use conventional p-values to claim a long-run relationship.
   - *What pins it:* The task asks whether the series are cointegrated at a stated level using a named test and its tabulated critical values.
2. **Johansen rank depends on deterministic terms.** The cointegrating rank from a Johansen test changes with lag length and with whether constants or trends sit inside the cointegrating relation. Choose lags by the stated criterion and the deterministic case the data imply, then read the matching trace table.
   - *Tempting shortcut:* Accept the rank printed under the software's default lag and deterministic settings.
   - *What pins it:* The prompt fixes the lag-selection criterion and the deterministic specification, so only one rank is supported.
3. **A shock is defined by its identification.** Orthogonalised impulse responses change with the Cholesky ordering, so a consumption shock means something only under a stated recursive or structural scheme. In a VECM, shocks to the common trend have permanent effects, so responses need not return to zero.
   - *Tempting shortcut:* Report default-ordered or reduced-form responses as the effect of a consumption shock.
   - *What pins it:* The task names the variable ordering or structural restriction that defines the shock and the response horizon.

### Panel-data estimation  (`panel-data-estimation`)

1. **Lagged outcomes with fixed effects bias persistence.** In short panels, a lagged dependent variable with unit fixed effects is correlated with the demeaned error, biasing persistence downward and contaminating other coefficients. Use difference or system GMM with lagged levels as instruments and check AR(2) and overidentification tests.
   - *Tempting shortcut:* Run the within estimator with the lagged outcome plus firm and year fixed effects.
   - *What pins it:* The prompt states a short time dimension and requires a dynamic-panel estimator that addresses this bias.
2. **Too many GMM instruments fake validity.** Using every available lag as a GMM instrument overfits the endogenous regressors, pulls estimates toward the biased within estimate and drives the Hansen test p-value toward one. Collapse or cap the instrument set and report instrument count against groups.
   - *Tempting shortcut:* Use the full instrument matrix and cite a Hansen p-value near one as proof of validity.
   - *What pins it:* The task states a lag limit or collapse rule for the instrument set.
3. **Cluster where the treatment varies.** When the regressor of interest varies by group and errors are serially correlated within units, observation-level robust errors overstate precision. Cluster at the level where treatment is assigned; with few clusters use the wild cluster bootstrap.
   - *Tempting shortcut:* Report heteroskedasticity-robust standard errors at the observation level.
   - *What pins it:* The prompt says the policy varies at the group level and sets the significance level for the decision.

### Elasticity & welfare / policy-impact estimation  (`elasticity-welfare-policy-impact-estimation`)

1. **Added taxes cost a rectangle too.** When a tax already exists, an increase creates the new triangle plus the existing wedge times the extra quantity lost. Incremental deadweight loss grows with the square of the total tax, not the added tax alone.
   - *Tempting shortcut:* Compute a Harberger triangle using only the new tax increment.
   - *What pins it:* The task states the existing tax and asks for the incremental deadweight loss of the proposed change.
2. **Short-run coefficient is not long-run elasticity.** With partial adjustment, the price coefficient in a model with lagged consumption is the short-run elasticity; the long-run elasticity divides it by one minus the lag coefficient. A permanent tax's welfare cost uses the long-run response.
   - *Tempting shortcut:* Read the price coefficient directly as the elasticity for a permanent policy.
   - *What pins it:* The prompt asks for the effect of a permanent tax over a horizon long enough for full adjustment.

### Forecasting & forecast evaluation  (`forecasting-forecast-evaluation`)

1. **Backtest on real-time vintages.** Forecasts must use only data as published at each origin. Backtesting on final revised data rewards models that exploit later revisions and flatters accuracy. Score every model and benchmark against the target release the task names.
   - *Tempting shortcut:* Run a pseudo out-of-sample backtest on the latest revised series.
   - *What pins it:* The task supplies data vintages and defines which release counts as the realised outcome.
2. **Score densities with proper scoring rules.** Density forecasts are compared with the log score or CRPS and checked for calibration with PIT histograms. Ranking by squared error of the means ignores spread and rewards overconfident densities. Compare loss differences with tests that allow overlapping horizons.
   - *Tempting shortcut:* Rank the density forecasts by the mean squared error of their point forecasts.
   - *What pins it:* The prompt names the scoring rule, horizon and test used to rank the density forecasts.

### Discrete-choice & limited-dependent-variable modeling  (`discrete-choice-limited-dependent-variable-modeling`)

1. **Willingness to pay is a coefficient ratio.** Value of travel time is the time coefficient divided by the cost coefficient. Its interval needs the delta method or simulated draws from the joint coefficient distribution, because the ratio is skewed and ignores neither coefficient's uncertainty nor their covariance.
   - *Tempting shortcut:* Report the ratio of point estimates with an interval based only on the time coefficient's standard error.
   - *What pins it:* The task asks for willingness to pay with an interval and names the delta method or simulation method.
2. **Multinomial logit overpredicts similar alternatives.** Under independence of irrelevant alternatives, a new option draws share proportionally from all others, so a mode close to an existing one is overpredicted. Nest similar modes or use mixed logit and test IIA before forecasting.
   - *Tempting shortcut:* Forecast the new mode's share with plain multinomial logit.
   - *What pins it:* The prompt adds an alternative that closely substitutes for an existing one and specifies the nesting structure.

### Spatial econometrics & spillover estimation  (`spatial-econometrics-spillover-estimation`)

1. **Spatial coefficients are not marginal effects.** In spatial lag or Durbin models, the policy coefficient is not its effect. Direct and indirect effects come from the spatial multiplier, the inverse of the identity minus rho times W, averaged over units, and feedback inflates the direct effect.
   - *Tempting shortcut:* Read beta as the direct effect and the WX coefficient as the spillover.
   - *What pins it:* The task asks to separate direct from spillover effects in a named spatial lag or Durbin model.
2. **Neighbors' outcome is endogenous in OLS.** The spatially lagged outcome is correlated with the error because neighbors affect each other, so OLS with it as a regressor is inconsistent. Estimate by maximum likelihood or IV using spatially lagged covariates, under the weights matrix the design states.
   - *Tempting shortcut:* Add the neighbors' average outcome as an ordinary regressor in OLS.
   - *What pins it:* The task specifies the weights matrix and a maximum likelihood or GMM spatial estimator.

## Political Science & Public Policy  (`political-science-public-policy`)

### Election polling & forecasting  (`election-polling-forecasting`)

1. **Correlated race errors, not independent coin flips.** Seat or majority probabilities must simulate polling errors that are correlated across races through a shared national swing. Treating each race's error as independent shrinks the variance of the seat total and overstates the favourite's chance of a majority.
   - *Tempting shortcut:* Compute each race's win probability separately, then combine them as if they were independent draws.
   - *What pins it:* The question asks for a joint outcome, such as the probability of a majority or a seat count, which depends on the error covariance.
2. **Adjust house effects before averaging polls.** A polling average must remove each firm's persistent house effect and weight by sample size and recency. A raw mean lets a prolific pollster with a stable partisan lean dominate the average and shift the estimated margin toward its lean.
   - *Tempting shortcut:* Average every poll in the window with equal weight.
   - *What pins it:* The stated averaging method includes house-effect adjustment, or one firm supplies a large share of polls with a consistent lean.
3. **Likely voter screen defines the estimand.** The forecast target is share of votes cast, so adult and registered-voter samples must be mapped to the likely electorate before pooling. Mixing population definitions pulls the margin toward groups with low turnout.
   - *Tempting shortcut:* Pool adult, registered-voter and likely-voter toplines as one series.
   - *What pins it:* The prompt defines the target as share of votes cast and the polls report different population screens.
4. **Calibrate intervals on past forecast error.** Forecast uncertainty must come from the method's out-of-sample error in past cycles, which includes nonsampling error, undecided allocation and late swing. Intervals built from poll sampling error alone are far too narrow and miss their stated coverage.
   - *Tempting shortcut:* Use the pooled sampling margin of error as the forecast interval.
   - *What pins it:* The task asks for intervals with a stated coverage level, checked against outcomes in prior cycles.

### Policy evaluation & administrative-data inference  (`policy-evaluation-administrative-data-inference`)

1. **Not-yet-treated comparisons under phased rollout.** When a reform phases in across jurisdictions at different dates, effects must be estimated by group and period against never-treated or not-yet-treated units. Two-way fixed effects uses early adopters as controls for late ones and can flip sign when effects grow.
   - *Tempting shortcut:* Regress the outcome on a post-reform dummy with unit and period fixed effects.
   - *What pins it:* Adoption dates differ across units and the question asks for the average effect on treated units at stated event times.
2. **Intent-to-treat when take-up is voluntary.** When a reform changes eligibility but enrolment is a choice, the policy effect is the intent-to-treat contrast on the eligible population, scaled by take-up only if a participation effect is asked for. Comparing enrollees with nonenrollees confounds the reform with self-selection.
   - *Tempting shortcut:* Compare outcomes of participants with those of eligible nonparticipants.
   - *What pins it:* The question asks for the effect of the reform on the eligible population, not the effect of choosing to participate.
3. **Ashenfelter dip before program entry.** Administrative earnings typically fall just before people enter a benefit or training program, so before-after gains measured from the last pre-entry quarter are inflated by mean reversion. The baseline must come from periods well before the dip.
   - *Tempting shortcut:* Measure the effect as post-entry earnings minus earnings in the quarter just before entry.
   - *What pins it:* The design states the baseline window, or the pre-entry trajectory visibly drops in the quarters before entry.
4. **Local fits at the eligibility cutoff.** A score-based eligibility rule identifies a local effect at the cutoff, estimated with local linear fits on each side within a stated bandwidth. An above-versus-below mean difference or a global polynomial absorbs the running variable's own trend.
   - *Tempting shortcut:* Compare mean outcomes of everyone above the cutoff with everyone below it.
   - *What pins it:* Eligibility is assigned by a score threshold and the bandwidth and kernel are stated in the task.

### Legislative behavior & ideal-point estimation  (`legislative-behavior-ideal-point-estimation`)

1. **Anchor the ideal-point scale across sessions.** Ideal points are identified only up to location, scale and reflection, so comparing polarization over time needs a common scale through bridging legislators or fixed anchors. Scaling each session separately and comparing raw scores confuses scale drift with ideological change.
   - *Tempting shortcut:* Fit a separate scaling for each session and compare party means directly.
   - *What pins it:* The question asks for change in polarization across sessions, which is only defined on one common scale.
2. **Exclude lopsided votes before scaling.** Near-unanimous roll calls carry almost no information about ideology and can distort the recovered dimension and cutting lines. Standard scaling drops votes whose minority side falls below a stated share and legislators with too few votes.
   - *Tempting shortcut:* Scale every recorded vote, including unanimous and near-unanimous ones.
   - *What pins it:* The stated scaling procedure names a lopsidedness cutoff and a minimum number of votes per legislator.
3. **Party unity is not ideological distance.** Party-line voting rises when the majority controls which bills reach the floor, so higher party unity can reflect agenda selection rather than divergence. Polarization claims must rest on distances between estimated ideal points, not on unity scores.
   - *Tempting shortcut:* Treat a rising share of party-unity votes as rising polarization.
   - *What pins it:* The question defines polarization as the distance between party medians on the estimated ideal-point scale.

### Conflict, protest & event-data analysis  (`conflict-protest-event-data-analysis`)

1. **Reported events track media reach.** Event counts drawn from news reports scale with media density, urbanity and connectivity, so covariates correlated with coverage appear to drive conflict. Models must condition on the reporting proxy or use the source-corrected measure the task specifies.
   - *Tempting shortcut:* Regress raw reported event counts on socioeconomic covariates.
   - *What pins it:* The task supplies a coverage measure and asks for covariate effects conditional on reporting intensity.
2. **Onset excludes ongoing conflict years.** Onset models must drop years already in conflict or model continuation separately, and intensity needs a count model conditional on occurrence. Pooling ongoing years into one logit lets persistence drive the coefficients and conflates continuation with onset.
   - *Tempting shortcut:* Run one logit on conflict-present versus absent years, keeping years already in conflict.
   - *What pins it:* The question asks for onset probability, defined as a new episode after a stated peace interval.
3. **Overdispersed, spatially clustered event counts.** Geocoded event counts are overdispersed and clustered in space and time, so a negative binomial model with spatially clustered errors is needed. Poisson with independent errors understates standard errors and makes weak covariates look significant.
   - *Tempting shortcut:* Fit a Poisson regression and report its default standard errors.
   - *What pins it:* The variance far exceeds the mean and the question asks whether an effect is significant at a stated level.

### Public opinion & survey experimentation  (`public-opinion-survey-experimentation`)

1. **Group differences need an interaction test.** A vignette effect that is significant in one demographic group and not in another does not show the groups differ. The rigorous test is the treatment-by-group interaction, with multiple-comparison control across the groups tested.
   - *Tempting shortcut:* Declare heterogeneity because one subgroup's effect is significant and another's is not.
   - *What pins it:* The question asks whether treatment effects differ across groups, which is a test of the interaction term.
2. **Post-treatment attention checks break randomization.** Dropping respondents who fail a manipulation or attention check given after treatment conditions on a post-treatment variable and biases the effect. Exclusions must rest on pre-treatment checks, or the full randomized sample must be analysed.
   - *Tempting shortcut:* Drop everyone who failed the manipulation check and compare the remaining arms.
   - *What pins it:* The check is administered after assignment and the estimand is the effect among all randomized respondents.
3. **Marginal means for subgroup conjoint preferences.** In conjoint and factorial vignette designs, subgroup AMCE differences depend on the arbitrary reference level. Comparing preference levels across groups requires marginal means, and AMCEs must respect any randomization restrictions on attribute combinations.
   - *Tempting shortcut:* Compare subgroup AMCEs directly to say which group favours an attribute more.
   - *What pins it:* The task asks for differences in subgroup preference levels in a design with a stated baseline category.

### Small-area public-opinion estimation & MRP  (`small-area-public-opinion-estimation-mrp`)

1. **Poststratify on the joint area frame.** MRP weights each cell prediction by that cell's share of the area's population across all model variables jointly. Raking to separate marginals or weighting by the sample's own composition reproduces the sample's skew instead of the population's.
   - *Tempting shortcut:* Weight cell predictions by sample counts, or by each variable's area marginal share separately.
   - *What pins it:* The method is named as MRP and a joint poststratification table by area is defined.
2. **Area-level predictors carry sparse areas.** With few respondents per area, partial pooling leans on area-level predictors such as prior vote share or region. Omitting them shrinks small areas toward the national mean and flattens real geographic variation in opinion.
   - *Tempting shortcut:* Use only individual demographic predictors plus area random intercepts.
   - *What pins it:* Several areas have very few respondents and the specified model includes area-level covariates.
3. **Rank areas on posterior draws.** Deciding which areas exceed a threshold or rank highest requires computing the statistic on every posterior draw and summarizing it. Ordering point estimates ignores that sparse areas have wide, overlapping intervals.
   - *Tempting shortcut:* Rank areas by MRP point estimates and call the top ones clear leaders.
   - *What pins it:* The question asks for a posterior probability of exceeding a threshold, or ranks held with stated certainty.

## Sociology & Demography  (`sociology-demography`)

### Population estimation & demographic projection  (`population-estimation-demographic-projection`)

1. **Age the cohorts, do not extrapolate totals.** A projection by age and sex must age each cohort forward, apply survival, add births to the youngest group and add migration. Extrapolating the total misses population momentum from age structure, so growth and the age mix both come out wrong.
   - *Tempting shortcut:* Fit a trend line to past population totals and split it by the latest age shares.
   - *What pins it:* The question asks for projected counts by age and sex, or names the cohort-component method with supplied rates.
2. **Gross migration flows, not net rates.** Out-migration is a rate applied to the origin population at risk; in-migration comes from other regions' out-flows. Applying a net migration rate to a changing population compounds errors and can drive small regions toward impossible negative counts.
   - *Tempting shortcut:* Apply each region's historical net migration rate to its projected population.
   - *What pins it:* Gross origin-destination flows are supplied and the system must stay closed, so internal migrants sum to zero across regions.
3. **Scenario bounds are not prediction intervals.** A probabilistic interval comes from simulating fertility, mortality and migration paths jointly and taking quantiles of the simulated total. Stacking high variants of every component, or adding regional upper bounds, gives a range with no stated coverage.
   - *Tempting shortcut:* Report the high and low variant projections, or summed regional bounds, as the 80 percent interval.
   - *What pins it:* The prompt asks for a stated-coverage interval for an aggregate, and supplies component error distributions or simulation draws.
4. **Small areas must honor the control total.** Sub-state projections are fitted to the official parent projection, typically by proportional adjustment within age and sex cells. Projecting each county independently produces a sum that disagrees with the control and shifts county shares.
   - *Tempting shortcut:* Project every county on its own and report the unadjusted results.
   - *What pins it:* The task states the county projections must be consistent with a given state control total by age and sex.

### Social mobility & inequality measurement  (`social-mobility-inequality-measurement`)

1. **Rank-rank slope, not the log elasticity.** Comparing relative mobility across cohorts or regions with different inequality calls for the rank-rank slope. The log intergenerational elasticity drops zero incomes and rises mechanically when the children's income distribution widens, confusing inequality with immobility.
   - *Tempting shortcut:* Regress log child income on log parent income and compare elasticities across cohorts.
   - *What pins it:* The question asks about positional mobility across groups with different income dispersion, or names percentile ranks within each generation.
2. **Single-year income attenuates persistence.** Permanent income must be proxied by multi-year averages measured at mid-career. One year of income, especially at young ages when earnings growth varies, adds transitory noise and lifecycle bias that pushes persistence estimates toward zero.
   - *Tempting shortcut:* Use one year of parent and child income, whatever ages they were observed.
   - *What pins it:* The prompt defines permanent income as an average over a stated age window and several years.
3. **Use a decomposable inequality index.** Splitting inequality into between-group and within-group parts requires an additively decomposable index such as Theil or mean log deviation, with population and income shares as weights. The Gini leaves an overlap term, so its parts do not sum.
   - *Tempting shortcut:* Compute regional Ginis and report their population-weighted average as the within-region component.
   - *What pins it:* The task asks for an exact between and within decomposition of inequality change across cohorts or regions.

### Social network & peer-effect analysis  (`social-network-peer-effect-analysis`)

1. **Homophily masquerades as contagion.** Ties form between similar people, so adoption clusters in networks without any influence. A credible peer effect uses peer adoption lagged before ego's outcome, ego's own prior state and individual fixed effects, or exogenously assigned ties.
   - *Tempting shortcut:* Regress current adoption on the current share of adopting friends in a cross-section.
   - *What pins it:* The question asks for a causal peer effect and the longitudinal data date tie formation and adoption separately.
2. **The reflection problem in group means.** In linear-in-means models the group average outcome and own outcome reflect each other, so endogenous and contextual effects are not separately identified. Identification needs network structure such as intransitive triads, using friends-of-friends traits as instruments.
   - *Tempting shortcut:* Regress own outcome on the group mean outcome, including oneself, and peer characteristics together.
   - *What pins it:* The prompt asks to separate endogenous from contextual peer effects and supplies an individual-level network, not just group membership.
3. **Shared nodes break independent errors.** Dyads and egos that share members are dependent, so inference must use dyad-robust clustering or network permutation tests. Ordinary standard errors treat each tie as independent and overstate significance, often by a large factor.
   - *Tempting shortcut:* Fit a dyad-level regression and read the default p-value.
   - *What pins it:* The question asks whether a tie-level association is significant, and every node appears in many dyads.

### Event-history & life-course analysis  (`event-history-life-course-analysis`)

1. **Competing events are not censoring.** When death or emigration prevents the transition, the probability of experiencing it by a given age is the cumulative incidence function. Censoring competing events and reporting one minus Kaplan-Meier overstates that probability.
   - *Tempting shortcut:* Censor people at the competing event and read one minus the Kaplan-Meier curve.
   - *What pins it:* The prompt asks for the share experiencing the transition by an age, with competing exits recorded.
2. **Match the hazard model to the question.** Covariate effects on the rate among those still at risk come from cause-specific hazards; effects on the eventual share experiencing an event come from subdistribution models. The two can differ in sign when a covariate also speeds competing exits.
   - *Tempting shortcut:* Fit one Cox model with competing events censored and interpret it as an effect on lifetime incidence.
   - *What pins it:* The question's wording names either the instantaneous rate among those at risk or the cumulative probability of the event.
3. **Repeated spells need their own risk sets.** For repeated migrations or job spells, each episode enters the risk set with its own clock and spell order, and inference clusters by person. Modeling only first spells or treating spells as independent misstates re-entry rates and their uncertainty.
   - *Tempting shortcut:* Keep each person's first transition only, or pool all spells with ordinary standard errors.
   - *What pins it:* The data record multiple spells per person and the question concerns recurrence or rates over all episodes.
4. **Late entry requires left truncation.** People observed from a panel's start at different ages enter the risk set at their entry age, not at the origin. Counting them as at risk from the origin adds survivor time never observed and biases transition rates downward.
   - *Tempting shortcut:* Start every person's clock at the origin age, as if observed from then.
   - *What pins it:* The design states people enter observation at differing ages after the process origin, with entry age recorded.

### Neighborhood, segregation & contextual effects  (`neighborhood-segregation-contextual-effects`)

1. **Dissimilarity is biased in small units.** With few minority residents per unit, random allocation alone yields a sizable dissimilarity index. Comparisons across places of different group size need the random-allocation expectation or a bias-corrected index, otherwise small minorities look most segregated.
   - *Tempting shortcut:* Rank places by the raw dissimilarity index computed from unit counts.
   - *What pins it:* The question compares segregation across areas with very different minority counts per unit, or names a bias-adjusted index.
2. **Evenness and exposure answer different questions.** Dissimilarity measures evenness and ignores group shares; isolation and exposure indices measure the neighborhood composition a typical member experiences and move with overall composition. Choosing the wrong dimension can reverse a trend.
   - *Tempting shortcut:* Use the dissimilarity index to describe how much contact groups have with each other.
   - *What pins it:* The prompt asks about the average neighborhood share experienced by members of a group, which defines an exposure index.
3. **Separate contextual from compositional effects.** Individual outcomes nested in neighborhoods need a multilevel model with individual covariates and group-mean centering. Regressing area outcome rates on area traits commits the ecological fallacy and attributes composition to context.
   - *Tempting shortcut:* Regress tract-level outcome rates on tract poverty and read the slope as the neighborhood effect.
   - *What pins it:* Individual microdata nested in areas are supplied and the question asks for the context effect net of own characteristics.

### Fertility, mortality & life-table estimation  (`fertility-mortality-life-table-estimation`)

1. **Period fertility is distorted by timing.** When the mean age at childbearing is rising, period total fertility falls even if completed family size does not. A quantum question needs tempo adjustment or completed cohort fertility, not the raw period sum of rates.
   - *Tempting shortcut:* Sum age-specific period rates and read the drop as lower lifetime fertility.
   - *What pins it:* The prompt asks for fertility quantum net of timing, supplying rates by birth order and mean ages at birth.
2. **Life tables need proper separation factors.** Converting death rates to probabilities needs the average fraction of interval lived by decedents, which is far below one half in infancy, and the open age group closes with person-years equal to survivors over its rate.
   - *Tempting shortcut:* Set every separation factor to one half and close the table with a half-width interval.
   - *What pins it:* The task asks for life expectancy from an abridged table with an infant group and an open-ended oldest group.
3. **Smooth sparse ages on exposure, not rates.** Small populations give zero or wildly noisy rates at some ages. Smoothing must weight by exposure, such as Poisson models, borrowing strength from a standard or parametric fits at old ages; dropping zeros or averaging raw rates biases the schedule.
   - *Tempting shortcut:* Drop ages with zero events and average the remaining raw rates across years equally.
   - *What pins it:* The prompt requires smoothing with deaths and person-years supplied, and specifies an exposure-weighted method or standard schedule.

## Psychology & Behavioral Science  (`psychology-behavioral-science`)

### Experimental design & power analysis  (`experimental-design-power-analysis`)

1. **Power the interaction, not the main effect.** In a factorial design the interaction contrast usually has a much smaller standardized effect than either main effect, especially when it only attenuates an effect. Size the study for the hypothesis being tested, which can need a far larger sample.
   - *Tempting shortcut:* Compute sample size from the main-effect d and reuse it for the interaction hypothesis.
   - *What pins it:* The prompt states the key hypothesis is the interaction and specifies its expected effect or cell means.
2. **Within-subject power runs on dz.** Paired and repeated-measures power depends on the correlation between conditions through dz, not the between-groups d. Converting without that correlation misstates the required sample in either direction.
   - *Tempting shortcut:* Plug a between-subjects Cohen's d from the literature into a paired-test power calculation.
   - *What pins it:* The design is within-subject and the task supplies or fixes the correlation between repeated measures.
3. **Group randomization inflates the sample by design effect.** When classrooms or teams are randomized, required participants grow by one plus cluster size minus one times the ICC. Powering on individuals as if independent overstates power and understates the number of groups needed.
   - *Tempting shortcut:* Compute participants per arm assuming every participant is independent.
   - *What pins it:* The prompt states randomization at the group level with a given ICC and group size.

### Psychometric measurement & scale validation  (`psychometric-measurement-scale-validation`)

1. **High alpha does not mean one factor.** Cronbach's alpha assumes equal loadings and says nothing about dimensionality; with unequal loadings it misstates reliability. Fit the factor model first, then report omega from the loadings of the retained structure.
   - *Tempting shortcut:* Report alpha above the conventional cutoff and conclude the scale is unidimensional and reliable.
   - *What pins it:* The task asks for model-based reliability under a congeneric model or names omega as the standard.
2. **Likert items need categorical estimators.** Items with few response categories and skew violate continuous-indicator factor analysis; Pearson correlations attenuate loadings and distort fit. Use polychoric correlations with a categorical estimator such as WLSMV and judge fit with its scaled statistics.
   - *Tempting shortcut:* Run maximum likelihood CFA on Pearson correlations of five-point items.
   - *What pins it:* Items are stated as ordinal with few categories and the prompt names the categorical estimator.
3. **Retain factors by parallel analysis.** The eigenvalue-greater-than-one rule keeps too many factors in item sets, which changes which items cross-load and which get dropped. Compare observed eigenvalues to those from random data of the same size and retain only factors that exceed them.
   - *Tempting shortcut:* Keep every factor with an eigenvalue above one, or eyeball the scree plot.
   - *What pins it:* The task names parallel analysis or a stated retention criterion before item decisions.

### Statistical inference & hypothesis testing  (`statistical-inference-hypothesis-testing`)

1. **Stimuli are a random factor too.** When participants respond to a sample of items or stimuli and the claim generalizes to other stimuli, ignoring stimulus variance inflates Type I error. Fit a mixed model with crossed random effects for participants and stimuli.
   - *Tempting shortcut:* Average over stimuli per participant and run a paired t-test.
   - *What pins it:* The prompt says stimuli were sampled and the conclusion must generalize to the stimulus population.
2. **Correct across the declared family of tests.** Testing several outcomes or post hoc pairs each at alpha inflates the familywise error rate. Apply the correction the preregistration or task names, such as Holm, over exactly the declared family, which can flip borderline findings.
   - *Tempting shortcut:* Declare every comparison with p below .05 significant.
   - *What pins it:* The prompt or preregistration defines the hypothesis family and the correction method.

### Mediation, moderation & process modeling  (`mediation-moderation-process-modeling`)

1. **Indirect effects need bootstrap intervals.** The product of the a and b paths is not normally distributed, so Sobel tests are underpowered and symmetric intervals are wrong. Test the indirect effect with bootstrap or Monte Carlo intervals; mediation does not require a significant total effect.
   - *Tempting shortcut:* Follow causal-steps logic and a Sobel z test, rejecting mediation when the total effect is not significant.
   - *What pins it:* The task specifies a bootstrap interval with a stated number of resamples for the indirect effect.
2. **Test moderated mediation with its index.** Whether a moderator changes an indirect effect is tested by the index of moderated mediation, the interaction path times the b path, with its own interval. Comparing whether subgroup indirect effects are each significant is not a test of difference.
   - *Tempting shortcut:* Split the sample by the moderator and claim moderation because one indirect effect is significant and the other is not.
   - *What pins it:* The prompt asks whether the indirect path is moderated and names the conditional process model.
3. **Randomized treatment does not randomize the mediator.** Randomizing the program identifies the a path, but the mediator-to-outcome path can be confounded by traits affecting both. Adjust for pre-treatment confounders of mediator and outcome and use the stated temporal order before interpreting the indirect effect causally.
   - *Tempting shortcut:* Treat the b path as causal because the program was randomly assigned.
   - *What pins it:* The design names baseline covariates for adjustment and measures the mediator after treatment and before the outcome.

### Meta-analysis & evidence synthesis  (`meta-analysis-evidence-synthesis`)

1. **Pool heterogeneous studies with random effects.** When interventions and populations differ, the question is the mean of a distribution of true effects. Fit random effects with the named tau-squared estimator, report a prediction interval, and remember I-squared is relative, not the spread of effects.
   - *Tempting shortcut:* Pool with fixed-effect inverse-variance weights and report I-squared as the heterogeneity answer.
   - *What pins it:* The prompt asks for a random-effects mean with a named tau-squared estimator and a prediction interval.
2. **Effect sizes from one study are dependent.** Several outcomes or arms from the same sample share participants and error. Treating them as independent overweights those studies and shrinks standard errors. Use multilevel meta-analysis or robust variance estimation, or split shared control groups.
   - *Tempting shortcut:* Enter every effect size as if it came from a separate independent study.
   - *What pins it:* The task states that studies contribute multiple effect sizes and names the dependence method.
3. **Trim-and-fill is not a bias correction.** Funnel asymmetry can reflect small-study effects or heterogeneity, and trim-and-fill performs poorly when effects vary. Use the adjustment the task names, such as PET-PEESE or a selection model, and report how the pooled estimate shifts.
   - *Tempting shortcut:* Run trim-and-fill and report its adjusted estimate as the true effect.
   - *What pins it:* The prompt names the publication-bias method and bases the decision on its adjusted estimate.

### Longitudinal & growth-curve modeling  (`longitudinal-growth-curve-modeling`)

1. **Slope change needs random slopes.** Testing whether treatment changes trajectories means testing the time-by-treatment interaction in a model with random intercepts and slopes. Without random slopes, the interaction's standard error is too small and the test is anticonservative.
   - *Tempting shortcut:* Fit random intercepts only, or run separate group tests at each wave.
   - *What pins it:* The prompt asks whether treatment changes the slope and specifies participant-level random slopes.
2. **Dropout is informative in trajectories.** Participants who worsen tend to leave, so completer analyses bias trajectories. Mixed models fit by full-information likelihood use every available wave and are valid under missing at random; carrying the last value forward distorts slopes.
   - *Tempting shortcut:* Analyze completers only or carry the last observation forward.
   - *What pins it:* The task states the missing-at-random assumption and requires all available waves in the model.

### Decision-making & computational behavioral modeling  (`decision-making-computational-behavioral-modeling`)

1. **Compare models on penalized or held-out fit.** Reinforcement-learning and prospect-theory models differ in parameter count, so raw likelihood favors the more flexible model. Compare by the stated criterion, such as BIC summed over participants or held-out trial likelihood, with fits done per participant or hierarchically.
   - *Tempting shortcut:* Pick the model with the higher in-sample log-likelihood.
   - *What pins it:* The task names the comparison criterion and the fitting level.
2. **Check parameter recovery before interpreting.** Loss aversion, curvature and choice temperature trade off in prospect theory, as do learning rate and inverse temperature in learning models. Verify that simulated parameters are recovered before interpreting group differences in fitted parameters.
   - *Tempting shortcut:* Interpret differences in fitted loss aversion between groups directly.
   - *What pins it:* The task requires a recovery check or fixes a parameter by stated convention.

### Experience sampling & intensive longitudinal analysis  (`experience-sampling-intensive-longitudinal-analysis`)

1. **Separate within- from between-person effects.** Raw daily stress mixes stable differences between people with daily fluctuations, so one coefficient blends two effects that can differ in sign. Center stress at each person's mean, add the person mean at level two, and interpret the within coefficient.
   - *Tempting shortcut:* Regress sleep on raw stress in a random-intercept model.
   - *What pins it:* The prompt asks explicitly for the within-person association separated from between-person differences.
2. **Lagged effects need autoregressive control.** Whether stress predicts next night's sleep requires lagging within person over consecutive occasions and controlling prior sleep. Same-day correlations cannot order cause, and ignoring autocorrelation credits stress with sleep's own inertia.
   - *Tempting shortcut:* Correlate same-day stress and sleep and call it a temporal effect.
   - *What pins it:* The prompt asks for a prospective lagged effect with a stated lag and an autoregressive term.

## Criminology & Justice  (`criminology-justice`)

### Crime incidence & hotspot analysis  (`crime-incidence-hotspot-analysis`)

1. **Rates need the right exposure denominator.** Hotspot risk must be measured per the exposure the question names, such as ambient population, visitors, targets or street segments. Residential denominators make commercial and transit areas look like extreme hotspots because their at-risk population is mostly nonresident.
   - *Tempting shortcut:* Rank areas by crimes per resident.
   - *What pins it:* The question defines risk per a stated exposure measure, such as visitors, targets or street segment.
2. **Persistence means staying hot across periods.** Persistent hotspots are places that stay in the top concentration tier across a sequence of periods, found by trajectory analysis or a stated persistence rule. Ranking one year's counts captures noisy spikes that regress toward the mean.
   - *Tempting shortcut:* Pick the top places from the latest single year of counts.
   - *What pins it:* The question defines persistence as remaining in the top tier for a stated number of consecutive periods.
3. **Recorded crime mixes incidence and reporting.** Recorded offences combine victimization, victim reporting and police detection. Changes in low-reporting or officer-initiated categories track enforcement effort, so trends in underlying crime must be read through reporting rates or citizen-initiated calls.
   - *Tempting shortcut:* Treat a change in recorded incidents as a change in underlying crime.
   - *What pins it:* The question asks about underlying crime and supplies reporting rates or separates citizen calls from officer-initiated records.
4. **Test clusters against a spatial null.** Calling a cluster significant requires a local statistic such as Getis-Ord Gi* or local Moran's I with a correction for many simultaneous tests. Kernel density surfaces always have peaks, and a peak alone is not evidence of clustering.
   - *Tempting shortcut:* Label the brightest kernel density peaks as significant hotspots.
   - *What pins it:* The question asks for statistically significant hotspots at a stated level using a named local statistic.
5. **Smooth rates in small-exposure areas.** Rates for areas with tiny exposure swing wildly, so the highest raw rates are mostly small areas with a few incidents. Empirical Bayes smoothing or a minimum-exposure rule must be applied before ranking.
   - *Tempting shortcut:* Rank areas by raw rate and take the top of the list.
   - *What pins it:* The task specifies empirical Bayes rates or a minimum exposure threshold for inclusion in the ranking.

### Recidivism & risk assessment  (`recidivism-risk-assessment`)

1. **Calibration is not discrimination.** A risk tool's AUC says nothing about whether predicted probabilities match observed reoffending rates. A decision threshold stated as a probability requires calibration checked by risk band or calibration slope, and recalibration when it fails.
   - *Tempting shortcut:* Cite a good AUC as proof that scores can be read as probabilities.
   - *What pins it:* The decision rule uses an absolute predicted-probability threshold, which only calibrated scores support.
2. **Fixed follow-up from release, time at risk.** Recidivism must be measured over a fixed window from release, excluding time back in custody, or with a survival estimator. People released near the data end have short follow-up, so an ever-rearrested share understates their risk.
   - *Tempting shortcut:* Compute the share ever rearrested by the data end date across all releasees.
   - *What pins it:* The outcome is defined as rearrest within a stated window from release, with full follow-up required.
3. **Name the fairness criterion before testing.** When base rates differ by group, equal false positive rates and within-group calibration cannot both hold. Subgroup error analysis must compute the criterion the question names at the stated threshold, not declare fairness from overall accuracy.
   - *Tempting shortcut:* Declare the tool fair because overall accuracy is similar across groups.
   - *What pins it:* The question names the criterion, such as equal false positive rates at a stated threshold.
4. **Validate on later release cohorts.** A risk model meant for future decisions must be validated on later release cohorts. Random splits across years share cohort-level policing and policy conditions between train and test, overstating performance and hiding drift.
   - *Tempting shortcut:* Use a random train-test split across all years pooled.
   - *What pins it:* The task asks how the model will perform on future releases or names a later holdout cohort.
5. **Selective labels from detention decisions.** Pretrial misconduct is observed only for released defendants, so validating on released cases says little about those detained. Thresholds tuned on the released population mislead when applied to everyone scored.
   - *Tempting shortcut:* Train and evaluate on released defendants as if they represent all defendants.
   - *What pins it:* The question asks about performance or impact across all scored defendants, including those detained.

### Sentencing, bail & disparity analysis  (`sentencing-bail-disparity-analysis`)

1. **Do not control for mediators of disparity.** Variables shaped by earlier decisions, such as charge reductions or pretrial detention, can carry part of the disparity. The estimand fixes which legally relevant, pre-decision characteristics are controls, and adding downstream variables absorbs disparity.
   - *Tempting shortcut:* Add every available case characteristic to the regression.
   - *What pins it:* The question lists the legally relevant factors measured before the decision and asks for disparity net of only those.
2. **Model incarceration and length as stages.** Sentence length is observed only for people incarcerated, and the in-out decision itself may differ by group. Length disparity among the incarcerated conditions on that earlier decision, so the two stages must be modeled separately or jointly.
   - *Tempting shortcut:* Estimate disparity in sentence length only among those sentenced to incarceration.
   - *What pins it:* The question defines the incarceration decision and sentence length as separate outcomes to report.
3. **Outcome test, not population benchmark.** Whether release standards differ by group is tested by comparing misconduct rates among released defendants, not by comparing detention rates with population or arrest shares, which ignores differences in risk and in who is arrested.
   - *Tempting shortcut:* Compare group detention rates with group shares of arrestees or residents.
   - *What pins it:* The question asks whether groups are held to different release standards, defined through outcomes of released defendants.
4. **Compare within the same court and judge.** Group composition varies across courts with different severity, so disparity must be estimated within court, judge or calendar using fixed effects. Pooled comparisons mix between-court sentencing levels with differential treatment.
   - *Tempting shortcut:* Pool all courts and compare groups with case-level controls only.
   - *What pins it:* The question asks for disparity among similarly situated defendants before the same court or judge.
5. **Measure departures from the guideline cell.** Under a guideline grid, sentences mostly reflect offence severity and criminal history. Disparity is measured as departure from the applicable cell's presumptive range, since raw length gaps largely restate grid-position differences.
   - *Tempting shortcut:* Compare average sentence lengths across groups.
   - *What pins it:* The jurisdiction uses a stated guideline grid and the question asks about departures from presumptive ranges.

### Intervention & policing-policy evaluation  (`intervention-policing-policy-evaluation`)

1. **Count displacement in the catchment.** Place-based effects must include buffer areas around treated places, because a drop inside the target with a rise next door is displacement. Using adjacent blocks as controls contaminates the comparison and doubles the apparent effect.
   - *Tempting shortcut:* Use adjacent blocks as the control group for treated hotspots.
   - *What pins it:* The question asks for the net effect including surrounding areas, with buffer zones defined.
2. **Places picked on spikes fall anyway.** Places chosen for treatment after a crime spike will tend to decline without intervention. The effect needs similarly selected untreated places or randomization, not the treated places' own before-after change.
   - *Tempting shortcut:* Report the drop at treated places from the year before to the year after.
   - *What pins it:* Places were selected on recent high counts and the design supplies a comparably selected untreated pool.
3. **Harm-weighted index, not raw counts.** An effect on harm requires weighting offences by the severity index the question names. Raw counts let numerous minor offences dominate, so a policy can show fewer incidents while serious harm rises.
   - *Tempting shortcut:* Measure the effect as the change in total recorded incidents.
   - *What pins it:* The question asks about harm and names or supplies a severity weighting such as a crime harm index.
4. **Synthetic control for one treated city.** With a single treated jurisdiction, the counterfactual is a synthetic control fit on pre-period outcomes, with placebo-in-space inference. Comparing with a regional average or a hand-picked neighbour attributes pre-existing trend gaps to the policy.
   - *Tempting shortcut:* Compare the treated city's change with the regional average change.
   - *What pins it:* One unit is treated, many untreated donors exist, and inference is by placebo permutation.
5. **Diversion effect on referrals, not completers.** Program completers are selected for lower risk and motivation, so a diversion effect must compare everyone offered the program with comparable non-offered cases under the assignment rule. Completer comparisons inflate the benefit.
   - *Tempting shortcut:* Compare recidivism of completers with noncompleters or non-referred defendants.
   - *What pins it:* Assignment was by lottery or rotation and the question asks for the effect of being offered diversion.

## Survey Research & Official Statistics  (`survey-research-official-statistics`)

### Sample design, allocation & weighting  (`sample-design-allocation-weighting`)

1. **Optimal allocation needs stratum SDs and costs.** For minimum variance at fixed budget, allocate to each stratum in proportion to its size times its standard deviation divided by the root of its unit cost. Proportional allocation over-samples homogeneous or expensive strata and yields different stratum sample sizes.
   - *Tempting shortcut:* Allocate the sample in proportion to stratum population because it is self-weighting and looks fair.
   - *What pins it:* The task asks for the minimum-variance or minimum-cost design and supplies stratum standard deviations and per-unit costs.
2. **Domain CV targets are constraints, not by-products.** When every region must meet a stated coefficient of variation, size each region to its own target first, then allocate any remainder. A nationally optimal allocation meets the national CV but leaves small regions failing theirs.
   - *Tempting shortcut:* Optimise the allocation for the national estimate and assume the regional CVs will be acceptable.
   - *What pins it:* The prompt sets a maximum CV for each published domain as well as the national estimate.
3. **Base weight multiplies every stage's selection probability.** In a PPS multistage design the base weight is the inverse of the product of PSU and within-PSU selection probabilities. When realised cluster sizes differ from the measure of size, the design stops being self-weighting and weights must reflect actual within-PSU probabilities.
   - *Tempting shortcut:* Set every weight to stratum population over stratum sample size, ignoring the PSU stage.
   - *What pins it:* The design specifies PPS selection on a measure of size, a fixed take per PSU and listed actual cluster sizes.

### Nonresponse, calibration & measurement-error adjustment  (`nonresponse-calibration-measurement-error-adjustment`)

1. **Adjust nonresponse within cells, using base weights.** Nonresponse adjustment factors must be computed within weighting classes that predict response and the outcome, as the base-weighted eligible total over the base-weighted respondent total. A single overall factor, or unweighted rates, leaves the differential nonresponse bias in place.
   - *Tempting shortcut:* Inflate all respondent weights by the inverse of the overall unweighted response rate.
   - *What pins it:* The task names the adjustment cells and asks for base-weighted, cell-level nonresponse adjustment before calibration.
2. **Rake until every margin converges.** Raking cycles through each control margin repeatedly until all weighted margins match their totals within tolerance. One pass matches only the last margin adjusted and leaves earlier margins off, so calibrated estimates differ from the converged solution.
   - *Tempting shortcut:* Run one pass of ratio adjustment per margin and treat the weights as calibrated.
   - *What pins it:* The task supplies marginal control totals for several variables and a stated convergence tolerance, not a joint cross-classification.
3. **Correct prevalence for both sensitivity and specificity.** When a validation study gives the item's sensitivity and specificity, the corrected proportion is the observed proportion plus specificity minus one, divided by sensitivity plus specificity minus one. Ignoring false positives, or dividing by sensitivity alone, biases rare-trait estimates badly.
   - *Tempting shortcut:* Report the observed survey proportion, or divide it by sensitivity alone to fix under-reporting.
   - *What pins it:* The task supplies record-check validation of both false negatives and false positives and asks for a misclassification-corrected estimate.

### Questionnaire & mode-effects research  (`questionnaire-mode-effects-research`)

1. **Separate mode selection from mode measurement.** In a sequential mixed-mode survey, web and phone respondents differ in who chooses each mode. The measurement effect must come from the randomised-mode comparison, or from adjustment for selection, not the raw difference between web and phone respondents.
   - *Tempting shortcut:* Attribute the whole difference between web and phone respondents' answers to the mode of interview.
   - *What pins it:* The design includes a randomly assigned mode subsample, and the prompt asks for the measurement effect specifically.
2. **Split-ballot tests need design-corrected chi-square.** A wording experiment embedded in a clustered, weighted survey must test distributional differences with a Rao-Scott or Wald test that accounts for the design. A Pearson chi-square on weighted counts treats weights as frequencies and overstates significance.
   - *Tempting shortcut:* Run a standard Pearson chi-square on the weighted cross-tabulation of form by response.
   - *What pins it:* The task embeds random form assignment in a design with strata, PSUs and weights, and asks for significance.
3. **Judge a series break against the difference's margin.** A redesign effect from a parallel run is a difference between two samples, so its margin of error comes from the variance of the difference, including any covariance from overlap. Comparing the effect to one sample's margin misdates or misses the break.
   - *Tempting shortcut:* Declare a break when the effect exceeds the published margin of error of the old series alone.
   - *What pins it:* The task defines a break as an effect exceeding the margin of the old-new difference, with both samples' variances given.

### Small-area estimation  (`small-area-estimation`)

1. **Shrink by sampling variance relative to model variance.** A Fay-Herriot estimate weights each area's direct estimate by model variance over model plus that area's sampling variance, giving the rest to the regression prediction. Equal weights, or direct estimates for sparse areas, ignore how unreliable each direct estimate is.
   - *Tempting shortcut:* Use the direct estimate where any sample exists and the regression prediction only for empty areas.
   - *What pins it:* The task names an area-level model and supplies each area's sampling variance and the administrative covariates.
2. **Benchmark small-area estimates to the reliable total.** Model-based area estimates rarely sum to the direct estimate for the larger domain, so official production rescales them to that total. Skipping benchmarking, or benchmarking with unweighted shares, leaves county figures inconsistent with the published state estimate.
   - *Tempting shortcut:* Publish the model-based county estimates as produced, without reconciling them to the state figure.
   - *What pins it:* The prompt states county estimates must add to the published direct state total by ratio benchmarking.

### Census, register & administrative-data quality  (`census-register-administrative-data-quality`)

1. **Dual-system estimates within post-strata, after erroneous enumerations.** Capture-recapture coverage estimates use correct enumerations times survey count over matches, computed within post-strata where capture probabilities are homogeneous. Pooling across groups with different coverage induces correlation bias, and counting duplicates or ineligibles inflates the population.
   - *Tempting shortcut:* Compute one pooled Lincoln-Petersen estimate from raw register and survey counts.
   - *What pins it:* The task supplies matched counts and erroneous enumeration rates by post-stratum and asks for net undercoverage.
2. **Net and gross classification error answer different questions.** From a linked reinterview, net difference rate measures bias in a category's total, while gross difference rate measures how many units are misclassified. Offsetting errors make net error small while gross is large, so the reported error depends on the estimand.
   - *Tempting shortcut:* Report the net change in category totals as the misclassification rate.
   - *What pins it:* The prompt asks either for bias in published category counts or the share of units misclassified, defining which.

### Seasonal adjustment & official time-series production  (`seasonal-adjustment-official-time-series-production`)

1. **Model unusual events before estimating seasonal factors.** Additive outliers, level shifts and temporary changes must be specified as regressors in the regARIMA step before seasonal filtering. Otherwise the event distorts seasonal factors for neighbouring years and shifts the adjusted series where nothing unusual happened.
   - *Tempting shortcut:* Run default seasonal adjustment on the raw series and label the event month afterwards.
   - *What pins it:* The task identifies the event dates and type and asks for its effect and the adjusted series.
2. **Measure revisions from real-time concurrent vintages.** Revision size compares the concurrent seasonally adjusted value first published for each month with a later vintage. Re-adjusting the full current series and comparing within it measures nothing, since end-point filter changes are what drive revisions.
   - *Tempting shortcut:* Compare the latest adjusted series with itself or with the unadjusted data to report revisions.
   - *What pins it:* The task defines revision as first release versus a stated later vintage under concurrent adjustment.
3. **Date turning points on trend-cycle, not adjusted series.** Seasonally adjusted series still contain the irregular, so single-month reversals produce false turning points. Turning points should be identified on the trend-cycle estimate under a stated dating rule, such as a minimum phase length.
   - *Tempting shortcut:* Call a turning point at the first month the seasonally adjusted series changes direction.
   - *What pins it:* The prompt specifies turning points on the trend-cycle with a minimum phase or cycle duration rule.

### Complex-survey estimation & variance  (`complex-survey-estimation-variance`)

1. **Variance must reflect strata and PSUs.** Standard errors for a stratified clustered sample come from Taylor linearisation over strata and PSUs, or from the supplied replicate weights with their stated factor. A weighted SRS formula ignores clustering and understates variance, often several-fold for clustered items.
   - *Tempting shortcut:* Use the weighted estimate with an SRS standard error formula based on respondent count.
   - *What pins it:* Stratum and PSU identifiers or replicate weights with a named method and coefficient are provided.
2. **Domain estimates keep the full design.** Subpopulation standard errors must be computed over the whole sample with out-of-domain units contributing zero, keeping every stratum and PSU. Subsetting first drops design structure, mis-states degrees of freedom and gives wrong intervals for domains that cross strata.
   - *Tempting shortcut:* Filter the file to the subgroup and compute design-based standard errors on the subset.
   - *What pins it:* The task asks for a domain estimate whose members are scattered across strata and PSUs, with confidence intervals.

### Anomaly detection  (`anomaly-detection`)

1. **Score edits by weighted impact on the estimate.** Selective editing ranks records by their weighted contribution to error in the published total, typically weight times deviation from an expected value over the domain total. Raw deviations flag low-weight units that cannot move the estimate.
   - *Tempting shortcut:* Flag the records with the largest unweighted change from expected or prior values.
   - *What pins it:* The stated editing goal is impact on a published estimate, with design weights and a score threshold given.
2. **Robust ratio tests account for unit size.** Period-to-period outlier detection should transform current over prior ratios to be symmetric, scale by unit size, and set bounds from medians and quartiles. A z-score on raw ratios over-flags small volatile units and is masked by the outliers inflating it.
   - *Tempting shortcut:* Flag units whose period-to-period ratio is more than a few standard deviations from the mean ratio.
   - *What pins it:* The task names a Hidiroglou-Berthelot style test with stated size exponent and quartile-based bound parameters.

## Urban & Regional Science  (`urban-regional-science`)

### Land-use & spatial-development modeling  (`land-use-spatial-development-modeling`)

1. **Neighbors are not independent observations.** Parcel land values and development outcomes cluster in space, so OLS residuals are spatially autocorrelated and standard errors shrink. The rigorous analysis tests residuals and uses a spatial error or lag model, or spatially robust errors, before declaring a zoning effect significant.
   - *Tempting shortcut:* Run OLS on parcels and read the zoning coefficient's p-value as if every parcel were an independent draw.
   - *What pins it:* The question asks whether the effect is significant at a stated level and names spatial dependence handling, such as a contiguity weights matrix.
2. **Zoned capacity is not likely development.** Buildable capacity under a zoning scenario counts what is legally allowed, not what pencils out. Rigorous forecasts screen parcels with a residual land value or redevelopment-ratio test, so scenario differences shrink sharply where new capacity is not economically feasible.
   - *Tempting shortcut:* Sum allowed units minus existing units across parcels and call that the scenario's development forecast.
   - *What pins it:* The prompt asks for expected units and supplies a feasibility rule, such as residual land value exceeding current improvement value.
3. **Upzoning goes where growth already was.** Planners rezone areas with rising demand, so before-after growth in rezoned parcels mixes treatment with pre-existing trends. A boundary comparison of similar parcels just across the rezoning line, or a matched untreated group, isolates the zoning effect.
   - *Tempting shortcut:* Compare permits in rezoned areas before and after rezoning, or against the citywide average.
   - *What pins it:* The question asks for the causal effect of rezoning and names a boundary-discontinuity or comparison-parcel design with a stated bandwidth.

### Accessibility, agglomeration & location analysis  (`accessibility-agglomeration-location-analysis`)

1. **Dense places attract productive workers.** Wages and productivity rise with density partly because skilled workers sort into dense, accessible areas. A causal agglomeration elasticity needs worker fixed effects or an instrument such as historical density; the cross-sectional slope overstates the effect of added accessibility.
   - *Tempting shortcut:* Regress average wage on employment density across neighborhoods and report the slope as the agglomeration elasticity.
   - *What pins it:* The prompt asks for the causal elasticity and supplies a worker panel or a named historical instrument, ruling out the pooled cross-section.
2. **Jobs reachable must be shared.** Counting jobs within a travel-time threshold ignores how many workers compete for them, so dense central areas look best by default. A competition-adjusted measure, such as two-step floating catchment, divides opportunities by the demand that can reach them.
   - *Tempting shortcut:* Rank neighborhoods by raw cumulative jobs reachable within the threshold.
   - *What pins it:* The stated accessibility standard names a supply-to-demand ratio method with the catchment threshold and the demand population defined.
3. **Transit access depends on departure minute.** Transit travel times swing with headways and transfer timing, so access computed at one departure time is a lucky or unlucky draw. Rigorous analysis computes travel time at every minute over a departure window and takes the stated summary, usually the median.
   - *Tempting shortcut:* Compute one transit travel-time matrix at a single peak departure time and treat it as the neighborhood's accessibility.
   - *What pins it:* The standard defines accessibility as the median, or a stated percentile, of travel times across a named departure window.

### Municipal service-demand & resource allocation  (`municipal-service-demand-resource-allocation`)

1. **Complaints measure reporting, not failure.** Call and app volumes reflect each neighborhood's propensity to report and its size, not underlying service failure. Allocation by need must use failure rates per serviced stop or household from operational records, which can reverse a ranking built on raw complaint counts.
   - *Tempting shortcut:* Rank neighborhoods by total complaints received and allocate extra crews or pilots to the top of that list.
   - *What pins it:* The allocation rule defines need as verified failures per serviced unit, with the denominator source named.
2. **Small areas top every rate ranking.** Neighborhoods with few serviced units produce extreme rates by chance, so they dominate both ends of a ranking. Rigorous allocation applies the stated minimum-volume threshold or empirical Bayes shrinkage toward the citywide rate before ranking.
   - *Tempting shortcut:* Rank areas by raw observed rate and award the resource to the highest one, regardless of how many events it rests on.
   - *What pins it:* The rule states a minimum count, a credibility formula or a shrinkage method to apply before ranking.
3. **Response standards are percentiles, not means.** Emergency response standards judge compliance by the share of calls answered within a threshold, often the 90th percentile. Skewed response times let a station meet the standard on average yet fail at the percentile, which changes which stations need added units.
   - *Tempting shortcut:* Compare each station's mean response time to the threshold and flag only those whose average exceeds it.
   - *What pins it:* The cited standard defines compliance as a stated percentile of incident response times falling within the stated minutes.

### Regional input-output & economic impact  (`regional-input-output-economic-impact`)

1. **Margin and localize spending first.** Facility or visitor spending must be margined, so retail purchases count only the local trade margin, and filtered through regional purchase coefficients before entering the model. Applying multipliers to gross spending credits the region with goods produced and imported from elsewhere.
   - *Tempting shortcut:* Multiply total project or visitor spending by the regional output multiplier.
   - *What pins it:* The question asks for regional impact and supplies margins and regional purchase coefficients, or a named model that requires them.
2. **Gross spending is not net new.** Spending by residents who would have spent locally anyway, or business displaced from competitors, is substitution, not new regional demand. Impact analysis counts only spending that originates outside the region or would otherwise have leaked out.
   - *Tempting shortcut:* Treat every dollar spent at the new facility as new final demand for the region.
   - *What pins it:* The prompt asks for net new regional impact, defines the region's boundary, and supplies the visitor origin or substitution share.
3. **Leakage changes the whole inverse.** Changing the local purchase share changes every round of indirect and induced spending, so multipliers respond nonlinearly. Sensitivity to leakage requires recomputing the Leontief inverse, including the household row and column for Type II, under each assumption.
   - *Tempting shortcut:* Scale the base multiplier's indirect and induced parts in proportion to the change in local purchase share.
   - *What pins it:* The question asks for impacts at each stated leakage assumption and supplies the transactions table needed to rebuild the inverse.

### Optimization  (`optimization`)

1. **The objective decides the best sites.** Minimizing average travel distance, minimizing the worst-case distance and maximizing population covered within a threshold choose different sites. The rigorous answer solves the objective the standard states, not the one that is easiest to compute.
   - *Tempting shortcut:* Pick sites that minimize total or average distance to demand because that is the familiar p-median setup.
   - *What pins it:* The prompt states the objective, such as maximal population within a response threshold, plus the number of sites and candidate set.
2. **Adding sites one by one.** Greedy siting fixes the first facility at the best single location, which is often not part of the best set of k. The rigorous solution optimizes all k sites jointly, by integer programming or exhaustive search over the candidate set.
   - *Tempting shortcut:* Choose the best single site, then add the next best given the first, until k sites are placed.
   - *What pins it:* The question asks for the optimal set of k sites from a finite candidate list under one stated objective.
3. **Busy units leave coverage gaps.** Emergency units are often already on a call, so a neighborhood covered by one unit is uncovered part of the time. Expected-coverage models weight backup coverage by unit availability, which favors redundancy in high-demand areas over single coverage of more ground.
   - *Tempting shortcut:* Maximize the population covered at least once, assuming every unit is always available.
   - *What pins it:* The prompt states a unit busy fraction or availability probability and asks for expected coverage, as in the maximal expected covering model.

### Forecasting  (`forecasting`)

1. **Backtest from the forecast origin.** Development and service-demand forecasts must be validated on rolling origins where every feature is known as of the origin date. Including later permits, rezonings or infrastructure completions as predictors makes a model look far better than it would in real use.
   - *Tempting shortcut:* Fit on all parcel-years, then score a random holdout that shares future information with the training data.
   - *What pins it:* The question fixes a forecast origin and holdout period and asks which model wins on out-of-sample error.
2. **Neighborhood forecasts must meet control totals.** Regional practice allocates growth from an adopted city or county control total down to small areas. Independent neighborhood forecasts rarely sum to that total, so rigorous work reconciles them, by proportional raking or the stated allocation rule, before ranking areas.
   - *Tempting shortcut:* Forecast each neighborhood separately and report the forecasts as they come out of the model.
   - *What pins it:* The prompt supplies an adopted regional control total and states the allocation or reconciliation method small-area forecasts must follow.
3. **Developed parcels leave the risk set.** Parcel development is a first event: once built, a parcel is no longer at risk in the same way. A discrete-time hazard model drops parcel-years after development and treats undeveloped parcels as censored, which a pooled logit on all years ignores.
   - *Tempting shortcut:* Fit a logit of developed or not on every parcel-year, keeping parcels in the data after they develop.
   - *What pins it:* The question asks for the probability of first development within a stated horizon, implying a hazard with right censoring.

### Network analysis  (`network-analysis`)

1. **Catchments follow streets, not circles.** Service areas drawn as straight-line buffers include homes cut off by rivers, rail lines and freeways and miss those reachable along streets. Rigorous catchments use shortest paths on the street network with one-way restrictions and impedance by travel time.
   - *Tempting shortcut:* Draw a fixed-radius buffer around each facility and count residents inside it.
   - *What pins it:* The standard defines coverage by network travel time or distance along the street network, with the threshold stated.
2. **Central links are not critical links.** High betweenness marks heavily used links, but a link with good parallel alternatives costs little when lost. Criticality must be measured by removing each link and recomputing weighted shortest paths or total travel cost across the origin-destination demand.
   - *Tempting shortcut:* Rank road links by betweenness centrality and call the top links the most critical.
   - *What pins it:* The question defines criticality as the increase in total travel time or unreachable demand when the link is removed.

## Education & Learning Sciences  (`education-learning-sciences`)

### Student growth & value-added modeling  (`student-growth-value-added-modeling`)

1. **Shrink small schools toward the mean.** School effects from a few dozen students are noisy, so raw mean residuals put small schools at both the top and bottom. Rigorous estimates apply empirical Bayes shrinkage using the between-school variance and each school's sampling variance before ranking or flagging.
   - *Tempting shortcut:* Rank schools on their raw average residual or average gain and flag the extremes.
   - *What pins it:* The prompt asks for shrunken or reliability-adjusted school effects, or supplies variance components and asks which schools are credibly below average.
2. **Noisy prior scores under-adjust for intake.** Prior test scores carry measurement error, so regressing current on prior scores attenuates the prior coefficient and leaves intake differences in school effects. Rigorous models correct with known reliability or conditional standard errors, or use several prior scores, which changes which schools look weak.
   - *Tempting shortcut:* Regress current score on one observed prior score with OLS and treat residual means as school effects.
   - *What pins it:* The prompt supplies test reliability or conditional SEMs and asks for effects corrected for measurement error in prior achievement.
3. **Growth percentiles condition on score history.** A student growth percentile ranks current achievement among students with the same prior score history, estimated by conditional quantile regression, and schools are summarised by the median. Percentiles of raw gains or mean percentiles give different school rankings, especially for high and low starters.
   - *Tempting shortcut:* Compute each student's raw gain, rank gains statewide, and average the resulting percentiles by school.
   - *What pins it:* The stated growth model defines growth as a conditional percentile given prior scores and names the median as the school summary.

### Randomized & quasi-experimental program evaluation  (`randomized-quasi-experimental-program-evaluation`)

1. **Assigned by school, inferred by school.** When tutoring is assigned at the school level, students within a school share shocks, so the effective sample is the number of schools. Rigorous inference uses cluster-robust errors with a small-cluster correction or a school-level analysis, which often removes significance.
   - *Tempting shortcut:* Run a student-level regression on the treatment indicator and read the conventional standard error.
   - *What pins it:* The design states assignment by school, the number of schools is small, and the question asks for significance at a stated level.
2. **Scale the offer effect by take-up.** With noncompliance, the effect of actually receiving tutoring among compliers is the intent-to-treat effect divided by the difference in take-up between arms, using random assignment as the instrument. Comparing tutored to untutored students imports selection on motivation and need.
   - *Tempting shortcut:* Compare outcomes of students who attended tutoring with those who did not, regardless of assignment.
   - *What pins it:* The prompt asks for the effect of receiving the program among compliers and reports assignment and take-up separately.
3. **Attrition decides the evidence rating.** An evidence standard treats a randomized study as compromised when overall and differential attrition exceed set boundaries; it must then show baseline equivalence on the analytic sample. Reporting the impact estimate alone ignores that the design may only qualify as a quasi-experiment.
   - *Tempting shortcut:* Accept the study as a randomized trial because assignment was random and report the impact estimate.
   - *What pins it:* The prompt supplies an evidence standard with attrition boundaries and baseline-equivalence thresholds and asks for the study's rating.

### Item response theory & test equating  (`item-response-theory-test-equating`)

1. **Match on ability before calling DIF.** Groups can differ in item success because they differ in ability, not because the item is biased. Rigorous DIF analysis conditions on total score, for example Mantel-Haenszel across score strata, and classifies items by effect size and significance, not raw difficulty gaps.
   - *Tempting shortcut:* Compare each item's proportion correct between groups and flag items with the largest gaps.
   - *What pins it:* The prompt names a matched DIF method and an item classification rule, such as delta-scale size categories with significance tests.
2. **Screen anchor items for drift first.** Common items link forms only if their parameters are stable. Rigorous linking screens anchors for parameter drift, for example with a robust displacement statistic, drops drifting items, then computes the linking constants, which shifts the scale transformation and reported trend.
   - *Tempting shortcut:* Compute mean-mean or characteristic-curve linking constants using every common item as given.
   - *What pins it:* The prompt names the linking method and a drift criterion for removing anchor items before linking.
3. **Nonequivalent groups need anchor-based equating.** When different populations take each form, raw score differences mix form difficulty with group ability. Rigorous equating uses the anchor test, via chained or post-stratification equipercentile or IRT methods, rather than assuming equivalent groups.
   - *Tempting shortcut:* Treat the two groups as equivalent and apply random-groups equipercentile equating or compare percent correct.
   - *What pins it:* The design states a nonequivalent-groups anchor test data collection and names the equating method to use.

### Learning analytics & early-warning models  (`learning-analytics-early-warning-models`)

1. **Features must exist at alert time.** An early-warning model is used at a fixed point in the year, so predictors must be measured as of that date and validated on a later cohort. Using end-of-term grades or full-year attendance inflates accuracy and picks different students.
   - *Tempting shortcut:* Train on all available student-year features and report cross-validated accuracy on randomly shuffled students.
   - *What pins it:* The prompt fixes the alert date and asks for performance on a later held-out cohort.
2. **Set the cutoff by support capacity.** With rare dropout and limited counselors, the useful metric is precision and recall among the students the school can serve. Rigorous choice of threshold flags the top k by risk, so models with similar AUC can rank differently.
   - *Tempting shortcut:* Pick the model with the highest AUC or accuracy and flag everyone above a 0.5 predicted probability.
   - *What pins it:* The prompt states how many students can receive support and asks which model or threshold serves the most true at-risk students.
3. **Flagged students differ, so use the cutoff.** Students who receive alerts are riskier, so comparing flagged and unflagged outcomes shows targeting, not impact. When alerts follow a risk-score cutoff, a regression discontinuity estimate at the threshold with local linear fits identifies the alert's effect.
   - *Tempting shortcut:* Compare later outcomes of all flagged students with all unflagged students, perhaps controlling for a few covariates.
   - *What pins it:* The prompt states alerts were triggered by a fixed risk-score cutoff and asks for the alert's effect on outcomes.
4. **Equity means error rates by group.** Equal flag rates across groups can hide unequal misses when base rates differ. A rigorous equity check compares the stated fairness criterion, such as true positive rate or calibration within each group, using actual outcomes, not flag shares.
   - *Tempting shortcut:* Compare the share of each subgroup flagged and call the model fair if the shares are similar.
   - *What pins it:* The prompt names the fairness criterion, such as equal true positive rates, and supplies observed outcomes by subgroup.

### Multilevel classroom & school research  (`multilevel-classroom-school-research`)

1. **Model the classroom level, not skip it.** Students nest in classrooms nested in schools. A two-level student-school model pushes classroom variance into the school and student levels, distorting intraclass correlations and the share of variation attributed to schools.
   - *Tempting shortcut:* Fit a two-level model with students in schools and report the school intraclass correlation.
   - *What pins it:* The prompt asks for the variance share at student, classroom and school levels and supplies classroom identifiers.
2. **Center within cluster to split effects.** A classroom practice measure varies both within and between schools. Rigorous models group-mean center the predictor and include the school mean, separating the within-school association from the contextual effect that the raw coefficient blends.
   - *Tempting shortcut:* Enter the raw practice score in a random-intercept model and interpret its single coefficient as the classroom effect.
   - *What pins it:* The question asks specifically for the within-school association, or for the contextual effect, of the classroom practice.
3. **Mobile students belong to several schools.** Students who change schools during the window contribute to more than one school's outcome. A multiple-membership model weights each school by enrolled time, while assigning students to their last school or dropping them biases effects for high-mobility schools.
   - *Tempting shortcut:* Attribute each student wholly to the school they attended at test time, or drop movers.
   - *What pins it:* The prompt states a dosage rule crediting schools by share of enrolled days and asks for school effects.

### Psychometrics  (`psychometrics`)

1. **Alpha is not omega here.** Coefficient alpha assumes every item loads equally on one factor. When a fitted factor model shows unequal loadings or a general factor plus subscales, rigorous reliability uses omega or omega hierarchical, which can fall well below alpha for the total score.
   - *Tempting shortcut:* Report Cronbach's alpha for the total scale and call the composite reliable.
   - *What pins it:* The prompt supplies or asks for a factor model and names omega or omega hierarchical as the reliability index.
2. **Score reliability is not decision reliability.** A test can be reliable overall yet classify students near a proficiency cut inconsistently. Rigorous evaluation estimates classification accuracy and consistency at the cut, which depends on score density and conditional error there.
   - *Tempting shortcut:* Cite the overall reliability coefficient as evidence that pass or fail decisions are dependable.
   - *What pins it:* The question asks how accurately or consistently students are classified at a stated cut score.

### Text analysis  (`text-analysis`)

1. **Benchmark machine scores against human raters.** Automated essay scores are judged on agreement with humans relative to human-human agreement, using quadratic weighted kappa and standardized mean differences, including within subgroups. Exact accuracy or Pearson correlation alone can pass a scorer that is biased or compressed.
   - *Tempting shortcut:* Report the correlation or percent exact agreement between machine and human scores and call it valid.
   - *What pins it:* The prompt states agreement thresholds tied to human-human kappa and a subgroup mean-difference limit.
2. **Type-token ratio falls with length.** Raw type-token ratio declines as texts get longer, so older students writing longer essays look less lexically diverse. Rigorous comparisons use a length-robust index, such as MTLD or HD-D, or fixed-length samples.
   - *Tempting shortcut:* Compute type-token ratio for each essay and compare grade or group averages directly.
   - *What pins it:* The prompt names a length-robust diversity measure or a fixed sample length for comparing lexical diversity.
