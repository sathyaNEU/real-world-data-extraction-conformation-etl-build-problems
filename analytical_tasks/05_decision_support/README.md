# Decision Support — 50 tasks (DS01–DS50)

Each task is one blueprint file in this folder. The header table of every file names the company problem it mirrors, the task shape, the core method, the analytical stump and the primary sources; sections 1–12 follow the template described in the repository README. `analytical_tasks_index.csv` at the repository root carries the same fields for all 300 tasks.

**Shapes used:** 01 · Ranked list under a cap (11), 02 · Forecast across many periods (1), 04 · Setting one dial (13), 06 · Sequenced schedule under capacity (1), 07 · Grid of cells (9), 10 · Scorecard against thresholds (6), 13 · Scenarios and the flip point (8), 16 · Indicators into one score (1).

| ID | Task | Domain | Shape |
|---|---|---|---|
| DS01 | [Launching a new recommendation policy: logged clicks evaluate the old policy, not the new one](DS01_recommender-policy-off-policy-evaluation.md) | E-commerce / recommender systems | 07 · Grid of cells |
| DS02 | [Which vulnerabilities to patch first: severity scores are not exploitation odds](DS02_patch-prioritisation-epss-time-split.md) | Cybersecurity operations | 04 · Setting one dial |
| DS03 | [Truck air-system maintenance: the cost-optimal threshold only works on calibrated probabilities](DS03_maintenance-threshold-calibrated-probabilities.md) | Fleet maintenance / heavy vehicles | 04 · Setting one dial |
| DS04 | [Deploying a readmission model to a new hospital system: the base rate moved, so the threshold must move](DS04_readmission-model-prior-shift-threshold.md) | Healthcare analytics | 04 · Setting one dial |
| DS05 | [Cutting loss-making routes: allocated overhead does not disappear when the route does](DS05_route-cuts-avoidable-vs-allocated-costs.md) | Passenger rail / transport finance | 01 · Ranked list under a cap |
| DS06 | [Funding emission-cutting projects under a budget: the best ratio first is not the best portfolio](DS06_climate-grant-portfolio-knapsack.md) | Climate finance / public grants | 01 · Ranked list under a cap |
| DS07 | [Repair or replace a water main: replace when the next break costs more than waiting](DS07_watermain-economic-replacement-threshold.md) | Water utilities / asset management | 13 · Scenarios and the flip point |
| DS08 | [Choosing crop-insurance coverage: the best expected return is not the best protection](DS08_crop-insurance-coverage-cvar.md) | Agriculture / insurance | 13 · Scenarios and the flip point |
| DS09 | [Delivery promise windows: plan on the 95th-percentile trip, not the average trip](DS09_delivery-promise-planning-time.md) | Freight / regional logistics | 04 · Setting one dial |
| DS10 | [Who should get the email? The likeliest buyers would buy anyway](DS10_campaign-targeting-uplift-not-response.md) | Retail marketing | 01 · Ranked list under a cap |
| DS11 | [How much to mark up a highway bid: you win most often exactly when you underestimated the cost](DS11_construction-bid-markup-competitor-distribution.md) | Construction / public procurement | 04 · Setting one dial |
| DS12 | [Fix the worst roads first? Preserving fair roads is cheaper than rebuilding them later](DS12_pavement-preservation-lifecycle-sequencing.md) | Transportation asset management | 06 · Sequenced schedule under capacity |
| DS13 | [Which bridges get more frequent inspection? Risk is probability of decline times consequence](DS13_bridge-inspection-risk-markov.md) | Infrastructure safety | 10 · Scorecard against thresholds |
| DS14 | [Approved-product scorecards: min–max scaling lets an irrelevant model change the winner](DS14_product-scorecard-normalization-rank-reversal.md) | Building equipment procurement / energy programmes | 16 · Indicators into one score |
| DS15 | [Choosing an industrial tariff: the bill is set by the worst 15 minutes, not the average load](DS15_industrial-tariff-choice-demand-charges.md) | Industrial energy procurement | 07 · Grid of cells |
| DS16 | [Settle or go to trial? Trial win rates come from the cases that were not settled](DS16_litigation-settlement-selected-trial-outcomes.md) | Legal operations / corporate litigation | 13 · Scenarios and the flip point |
| DS17 | [How many samples per window? A plan that rarely fails good plants also rarely catches bad ones](DS17_sampling-plan-operating-characteristic.md) | Food safety / meat and poultry processing | 10 · Scorecard against thresholds |
| DS18 | [How much cache memory to buy? A Zipf fit forgets that requests come in bursts](DS18_cache-sizing-trace-driven-miss-ratio.md) | Distributed systems / infrastructure cost | 04 · Setting one dial |
| DS19 | [Acting on probability forecasts: a "70% chance" is only worth what it verifies at](DS19_seasonal-outlook-cost-loss-reliability.md) | Energy trading / weather risk | 10 · Scorecard against thresholds |
| DS20 | [When to raise the flood wall: one sea-level projection is not a plan](DS20_coastal-flood-adaptation-minimax-regret.md) | Coastal infrastructure / climate adaptation | 13 · Scenarios and the flip point |
| DS21 | [Picking seed hybrids from yield trials: the top of a noisy table is partly luck](DS21_hybrid-selection-multi-location-blup.md) | Agriculture / seed procurement | 01 · Ranked list under a cap |
| DS22 | [Go for it on fourth down? Observed conversion rates come from the situations coaches chose](DS22_fourth-down-decisions-selection-bias.md) | Sports analytics | 07 · Grid of cells |
| DS23 | [Reservoir releases: planning on average inflow breaks the minimum-level guarantee in dry years](DS23_reservoir-release-chance-constraint.md) | Water resources / hydropower | 02 · Forecast across many periods |
| DS24 | [How much nitrogen to apply: the rate that maximises yield is not the rate that maximises profit](DS24_nitrogen-rate-economic-optimum.md) | Agronomy / farm management | 13 · Scenarios and the flip point |
| DS25 | [Picking the final model by the public leaderboard: the top of a reused test set is partly overfit](DS25_model-selection-public-leaderboard-overfit.md) | Machine learning operations | 07 · Grid of cells |
| DS26 | [Which backbone links to upgrade? Size for the day a neighbouring link fails](DS26_wan-upgrades-single-failure-utilisation.md) | Telecommunications / network engineering | 01 · Ranked list under a cap |
| DS27 | [Setting regional price relativities: small regions' raw claim experience is mostly noise](DS27_motor-pricing-credibility-relativities.md) | Motor insurance pricing | 07 · Grid of cells |
| DS28 | [Store the harvest or sell it? Compare each year's own spring price with its own harvest price, net of carrying costs](DS28_grain-storage-carry-paired-years.md) | Agriculture / commodity marketing | 13 · Scenarios and the flip point |
| DS29 | [Where to add edge locations: improving the average user is not improving the slow users](DS29_cdn-pop-placement-p95-latency.md) | Internet infrastructure | 01 · Ranked list under a cap |
| DS30 | [Setting a catch limit: the point estimate of the overfishing limit is not the limit](DS30_catch-limit-uncertainty-buffer.md) | Fisheries management | 04 · Setting one dial |
| DS31 | [Ranking items by average rating: who rated them matters as much as how good they are](DS31_rating-calibration-rater-leniency-anchors.md) | Content platforms / ratings | 01 · Ranked list under a cap |
| DS32 | [Choosing wind sites for a supply portfolio: the three best sites can all go quiet together](DS32_wind-site-portfolio-diversification.md) | Renewable energy procurement | 01 · Ranked list under a cap |
| DS33 | [Choosing referral hospitals for heart surgery: raw mortality punishes the hospitals that take the sickest patients](DS33_cardiac-referral-risk-adjusted-mortality.md) | Healthcare purchasing / centres of excellence | 01 · Ranked list under a cap |
| DS34 | [Removing bus stops: count the riders who save time, not the stops with few boardings](DS34_bus-stop-consolidation-rider-weighted.md) | Public transit operations | 01 · Ranked list under a cap |
| DS35 | [Choosing contracted power for each customer: commit to a high quantile, and fix the clock first](DS35_contracted-capacity-quantile-dst.md) | Electricity retail / B2B energy | 04 · Setting one dial |
| DS36 | [How hard to run the gas turbine: keep the 95th-percentile NOx under the permit, not the average](DS36_turbine-load-setpoint-compliance-quantile.md) | Power generation / environmental compliance | 04 · Setting one dial |
| DS37 | [When to close a lane for roadworks: delay explodes above capacity, so the average hour misleads](DS37_work-zone-window-nonlinear-queue-delay.md) | Highway operations | 07 · Grid of cells |
| DS38 | [Shutting down coastal facilities before a hurricane: "inside the cone" is not a decision rule](DS38_hurricane-shutdown-probabilistic-exposure.md) | Energy operations / emergency management | 10 · Scorecard against thresholds |
| DS39 | [Which crowd labels need expert review? Majority vote trusts every worker equally](DS39_label-quality-routing-dawid-skene.md) | Machine learning data operations | 04 · Setting one dial |
| DS40 | [Retiming traffic signals: the peak hour average hides the 15 minutes that break the intersection](DS40_signal-timing-peak-15-minute-flows.md) | Traffic engineering | 07 · Grid of cells |
| DS41 | [Is the extra data source worth buying? Measure it in decisions changed, not in AUC](DS41_data-source-value-of-information.md) | Consumer credit / risk management | 13 · Scenarios and the flip point |
| DS42 | [Combining analysts' probability forecasts: the simple average is systematically timid](DS42_forecast-aggregation-extremizing.md) | Forecasting / judgement aggregation | 10 · Scorecard against thresholds |
| DS43 | [Sell the flat now or in five years? Prices fall faster as the lease runs down](DS43_leasehold-flat-sell-or-hold-lease-decay.md) | Real estate / household finance | 13 · Scenarios and the flip point |
| DS44 | [Who gets the fundraising mailing? Likely donors give small amounts; big givers respond rarely](DS44_donor-mailing-two-part-expected-value.md) | Nonprofit fundraising / direct marketing | 01 · Ranked list under a cap |
| DS45 | [Can we drop support for an old Python version? Mirrors and CI bots download the most](DS45_python-version-deprecation-download-filtering.md) | Open-source software / developer platforms | 10 · Scorecard against thresholds |
| DS46 | [Choosing a drug plan: price the whole year through the benefit phases, not the average month](DS46_drug-plan-choice-expected-cost-phases.md) | Health insurance / benefits advising | 07 · Grid of cells |
| DS47 | [How often to checkpoint a long training job: failures do not arrive as a steady Poisson stream](DS47_checkpoint-interval-empirical-failures.md) | High-performance computing / ML infrastructure | 04 · Setting one dial |
| DS48 | [How much priority fee to bid: you only see the transactions that got in](DS48_transaction-fee-bidding-survivorship.md) | Payments / blockchain infrastructure | 04 · Setting one dial |
| DS49 | [Sizing an API rate limiter: average request rates say nothing about bursts](DS49_rate-limiter-burst-sizing.md) | Web infrastructure / API platform | 04 · Setting one dial |
| DS50 | [Shifting compute to "green" hours: average carbon intensity is not what your extra load emits](DS50_carbon-aware-load-shifting-marginal-emissions.md) | Electricity / sustainability operations | 07 · Grid of cells |
