# Trap catalog: Forecasting & Predictive Modeling

> The decision depends on a future value or a predicted outcome that the supplied history can pin down.

**18 traps.** One catalog file per Axis 1 objective that has one (Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting have none of their own). Read `_cross-objective.md` alongside it, which carries the constraint, comparison and monitoring families that are not tied to one objective.

**Two bans apply to every trap below, so read them before you adapt one.** The planted-defect
flip is banned: an answer that depends on a planted defect reversing the naive reading is not a
source of difficulty. And under determinism judge v3, **surface-read rejection is banned as the
primary strategy at any depth**, which also bans the honest-data version, a single lens or
definition swap that flips the naive read. Depth is not a defence.

Two tests on whichever trap you adapt, and it has to pass both:

- **Clean-data test.** If the data were perfectly clean and correct, would the task still be hard
  and the answer still non-obvious?
- **The litmus.** Is the reported number or stakeholder conclusion the task overturns actually
  wrong, and is catching that the main thing that defeats the model? If yes, redesign.

Most traps below pass both already, because they turn on analysis rather than on a broken file.
Where one does not, it is flagged in place. Messy multi-file data is still required, it just
cannot be the thing that flips the answer.

Build the trap into the evidence rather than the wording, keep it reconcilable from the shipped
files alone, and make sure the failure is a genuine analytical mistake rather than a formatting
or wording problem.

These are traps that have already stumped models on this objective. They are examples to adapt,
not a checklist to copy, and one trap is rarely a ladder on its own: stack two to four from
different gaps (`stumping` Part 1) and different families (`stumping` Part 6.3).

## Start here: the two structural traps

- **Insufficient evidence: the answer is HOLD**. *Not enough information to make a decision* is now an acceptable final answer, but only when it is forced by the evidence and reproduces like any other answer. See `stumping` Part 6.4 before building one.

## The traps

### Insufficient evidence: the answer is HOLD

**What it is.** Some series are just too short or too unstable to pin a number on, and the honest call is to hold and say so rather than commit.

**How it stumps the model.** The model emits a spuriously precise single number to look responsive, ignoring that the history cannot justify any point estimate.

### Level shift vs trend confusion

**What it is.** A one-time step change, like a platform launch or a price reset, permanently moves the series to a new level without implying any ongoing slope.

**How it stumps the model.** The model reads the jump as a trend and extrapolates continued growth from what was actually a single re-leveling.

### Growth-rate extrapolation of a decelerating series

**What it is.** Many series grow fast early and then slow down, so their sequential growth rate is falling even while the level keeps rising.

**How it stumps the model.** The model anchors on the early high-growth periods and fits a constant-growth or linear trend, over-forecasting the future.

### Seasonality period misidentification

**What it is.** A series can carry more than one seasonal cycle, and estimating any of them needs enough complete cycles in the history.

**How it stumps the model.** The model picks the wrong period or misses one entirely, such as catching daily but not weekly seasonality, or fitting annual seasonality with too few years to support it.

### Target leakage in a predictive model on honest data

**What it is.** Some features only become known after or because the outcome happened, so including them lets the model peek at the answer even when the data itself is clean.

**How it stumps the model.** The model keeps a post-outcome field like return_reason or a cancellation-date proxy, inflating backtested accuracy that cannot be reproduced at decision time.

### Random-split backtest on time series

**What it is.** Time series have to be evaluated in order, because a shuffled split lets the training set contain observations from after the test point.

**How it stumps the model.** The model uses random k-fold or a shuffled train/test split, letting future data inform predictions of the past and reporting optimistic, unachievable accuracy.

### Overfitting a short series with a complex model

**What it is.** When the history is short, a high-parameter method has too little signal to learn from and ends up fitting the noise.

**How it stumps the model.** The model reaches for a deep net, high-order ARIMA, or many regressors that fit in-sample but forecast poorly out of sample.

### Point forecast with no uncertainty

**What it is.** Decisions about capacity, contracts, or staffing usually turn on the tail of the distribution, not the central estimate.

**How it stumps the model.** The model delivers only point forecasts and omits prediction intervals, hiding the very risk the decision-maker needs to see.

### Horizon-blind accuracy

**What it is.** Forecast error grows the further out you go, so a number that is reliable next week is not reliable next quarter.

**How it stumps the model.** The model reports one error metric and treats a distant-horizon forecast as trustworthy as a near-term one.

### Intermittent demand treated as continuous

**What it is.** Slow-moving SKUs have long stretches of zero demand punctuated by occasional orders, which standard mean and smoothing methods handle badly.

**How it stumps the model.** The model smears demand across the zeros, biasing reorder quantities for exactly the items where getting them right matters.

### Ignoring a known covariate / driver

**What it is.** Sometimes a strong external driver is available, like temperature or a wind-speed forecast, and it carries signal the target's own history does not.

**How it stumps the model.** The model forecasts univariately and leaves obvious predictive signal on the table.

### Using a driver that isn't known at forecast time

**What it is.** The mirror problem: a covariate helps only if its future values will actually be available when the forecast has to be made.

**How it stumps the model.** The model conditions on a driver whose future is unknown in production, producing accuracy that cannot be reproduced when it counts.

### Outlier / anomaly vs new normal

**What it is.** A recent run of unusual observations might mark a durable shift in the series or just a temporary shock, and the right treatment depends on which.

**How it stumps the model.** The model either bakes the cluster in as the new baseline or discards it outright, without checking whether a real change occurred.

### Beating no baseline

**What it is.** A forecast is only worth its complexity if it beats a trivial method like naive or seasonal-naive on the same test.

**How it stumps the model.** The model deploys a sophisticated approach without benchmarking it, so it cannot show the complexity buys anything and sometimes it quietly loses to seasonal-naive.

### No-history / cold-start forecasting

**What it is.** A new product or site has no direct history, but comparable launches or proxy records often stand in for it.

**How it stumps the model.** The model either refuses outright or invents a forecast from the empty series, ignoring the available analogs.

### Discrimination without calibration in model selection

**What it is.** Ranking quality and probability accuracy are different things, and decisions that use the probabilities directly need them calibrated, not just well-ordered.

**How it stumps the model.** The model picks on AUC alone, leaving probabilities miscalibrated for the capacity or pricing decision that consumes them.

### Ignoring population / covariate drift

**What it is.** When the future population differs from the one a model was validated on, its historical performance no longer describes what will happen.

**How it stumps the model.** The model ships as-is despite a known shift in the applicant or customer mix, so backtested numbers overstate real performance.

### Non-stationarity ignored

**What it is.** Many methods assume a stable mean and variance, which breaks down on a series whose level drifts or whose volatility changes over time.

**How it stumps the model.** The model applies such a method without differencing or transforming first, producing forecasts and intervals that do not hold up.

---

Ask anatomy and example asks for this objective: `../../../guide-to-prompt/references/objectives/forecasting-predictive-modeling.md`

Mechanism families, the refusal ladder and the fourteen generators: `../../SKILL.md`
