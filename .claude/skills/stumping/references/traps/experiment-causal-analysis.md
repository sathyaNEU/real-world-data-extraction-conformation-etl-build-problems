# Trap catalog: Experiment & Causal Analysis

> The conclusion depends on a causal claim, from a designed test or from observational data with confounders.

**19 traps.** One catalog file per Axis 1 objective that has one (Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting have none of their own). Read `_cross-objective.md` alongside it, which carries the constraint, comparison and monitoring families that are not tied to one objective.

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

- **No governance document to anchor on**. The pack deliberately ships no rule to quote, so the criterion has to be earned from the data. This is the shape that most often separates a real analyst from a model looking for a sentence to cite.
- **Insufficient evidence, the answer is HOLD**. *Not enough information to make a decision* is now an acceptable final answer, but only when it is forced by the evidence and reproduces like any other answer. See `stumping` Part 6.4 before building one.

## The traps

### No governance document to anchor on

**What it is.** The task ships no stat plan, success criteria, or decision rule, so the standard for what counts as a win has to be reasoned up from the business context.

**How it stumps the model.** The model either invents an arbitrary cutoff like "p<0.05 so ship" or refuses to decide because nothing was pre-registered, instead of building a defensible bar from the cost of a wrong ship and the size of the base at stake.

### Insufficient evidence, the answer is HOLD

**What it is.** The experiment is underpowered or the confidence interval on the key metric spans zero, so no candidate can honestly be called the winner.

**How it stumps the model.** Feeling obligated to name a winner, the model commits to a point estimate that is indistinguishable from noise rather than calling hold and running longer.

### Peeking / early-stopping on an in-flight test

**What it is.** The test is still running and an early result that looks significant or large is put forward as if it were the final readout.

**How it stumps the model.** The model treats the interim number as decision-grade, ignoring that repeated looks inflate the false-positive rate and that early effects tend to regress toward the planned-horizon value.

### Multiple endpoints / multiple comparisons

**What it is.** Several metrics or arms were tested and only the single best one is presented as significant.

**How it stumps the model.** The model accepts the winner at its nominal p-value without counting the many tests behind it, so a chance high-water mark among a dozen comparisons gets shipped as a real effect.

### HARKing / post-hoc subgroup

**What it is.** The headline effect shows up only in a subgroup that was defined after the data was seen, such as "it works great for power users."

**How it stumps the model.** The model reports the subgroup as a confirmed finding rather than an exploratory hypothesis, letting it rescue an overall-null result and justify shipping.

### Self-selection / voluntary adoption confound

**What it is.** Treatment was opt-in, so the units that took it up differ systematically from those that did not.

**How it stumps the model.** The model reads the raw gap between adopters and non-adopters as the treatment effect, missing that selection bias, not the intervention, may explain it, and greenlights a scale-up on an unsupported causal claim.

### Pre/post with a co-occurring event (no control)

**What it is.** A single-arm before-and-after comparison runs alongside a concurrent shock like flu season, a formulary change, or a macro trend, with no group to net out the background.

**How it stumps the model.** The model credits the entire change to the intervention because there is no contemporaneous control to separate the effect from the co-occurring event.

### Novelty / primacy effect decay

**What it is.** The treatment effect is large in the first days or weeks and shrinks steadily across the test window as the novelty wears off.

**How it stumps the model.** The model bases the decision on the peak week and mistakes a transient novelty response for the durable steady-state effect.

### Underpowered test read as a null (absence of evidence)

**What it is.** A small sample produces a non-significant result, which is a failure to detect rather than proof there is nothing there.

**How it stumps the model.** The model concludes "no effect" and kills the feature, when the interval is wide enough to still contain a business-meaningful effect and the honest call is inconclusive.

### External validity / generalization gap

**What it is.** The tested population differs from the rollout population, for instance new signups only, one geography, or an engineering-only pilot.

**How it stumps the model.** The model extends the in-sample estimate to the whole base without qualification, conflating whether the effect was real with whether it transfers.

### Effect driven by a few units

**What it is.** The aggregate effect is carried by a handful of heavy units, like three high-volume agents or one whale segment.

**How it stumps the model.** The model reports the mean as if the effect were spread evenly, missing that a few influential points make it fragile and not something to mandate broadly.

### Statistical vs. practical significance

**What it is.** A large sample makes a tiny effect statistically significant even though it may be too small to matter to the business.

**How it stumps the model.** The model ships on p<0.05 alone without checking whether the effect size clears the threshold that would justify the cost and risk of rolling it out.

### Simpson's paradox in honest data

**What it is.** An aggregate effect reverses or disappears once a legitimate confounder like segment mix or cohort is conditioned on, with no data error in play.

**How it stumps the model.** The model reports either the aggregate or one stratum without checking for a mix shift, so it reads a composition artifact as a real directional result.

### Regression to the mean

**What it is.** Units were picked because they were extreme, such as the worst stores or lowest-adherence patients, and extremes naturally drift back toward average.

**How it stumps the model.** The model reads the subsequent rebound as a treatment effect, when those units would have improved on their own without any intervention.

### Wrong / missing counterfactual

**What it is.** The comparison group is not a valid stand-in for what would have happened anyway, for example Texas markets against the rest of the country or mismatched time periods.

**How it stumps the model.** The model takes the naive difference as the causal effect without checking baselines, timing, or pre-trends, so a broken counterfactual passes as a clean estimate.

### Confidence interval spanning the decision boundary

**What it is.** The point estimate looks favorable but its interval straddles break-even, so the sign of the business outcome is still unresolved.

**How it stumps the model.** The model reports the point estimate and ships, ignoring that the interval contains outcomes on both sides of the decision boundary.

### Ceiling / floor and non-inferiority confusion

**What it is.** The real question is whether the downside stays acceptable, such as a price increase that must not push churn past some margin.

**How it stumps the model.** The model runs a standard superiority test, finds no significant harm, and calls it safe, when the test never had the power to rule out a harmful effect.

### Confounded rollout timing / maturation

**What it is.** The intervention lands during an organic upward trend, a product maturation curve, or a learning effect that was already lifting the metric.

**How it stumps the model.** The model credits the intervention with improvement that was underway anyway, rather than attributing only the deviation from the pre-existing trajectory.

### Attrition / differential dropout bias

**What it is.** Participants leave the arms at different rates or for reasons tied to the outcome, so the survivors are no longer comparable.

**How it stumps the model.** The model analyzes only completers, which quietly turns a randomized test into a biased comparison and inflates or distorts the measured effect.

---

Ask anatomy and example asks for this objective: `../../../guide-to-prompt/references/objectives/experiment-causal-analysis.md`

Mechanism families, the refusal ladder and the fourteen generators: `../../SKILL.md`
