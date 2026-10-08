# Trap catalog: Root-Cause Analysis

> A metric moved and the task is to name the driver, with rival explanations ruled out on evidence.

**16 traps.** One catalog file per Axis 1 objective that has one (Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting have none of their own). Read `_cross-objective.md` alongside it, which carries the constraint, comparison and monitoring families that are not tied to one objective.

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
- **Insufficient evidence to name one driver**. *Not enough information to make a decision* is now an acceptable final answer, but only when it is forced by the evidence and reproduces like any other answer. See `stumping` Part 6.4 before building one.

## The traps

### Mix versus rate confusion

**What it is.** The aggregate metric moves because the composition of the population shifted, while the within-group rate barely changed, or the reverse.

**How it stumps the model.** A model reads the headline decline and attributes it to the process being measured without decomposing into a within-group rate effect and a between-group mix effect. It names the intuitive operational cause when the arithmetic actually points at a compositional shift.

### Volume growth mistaken for rate collapse

**What it is.** A rate falls purely because a large batch of new low-baseline units entered the denominator, not because any existing unit got worse.

**How it stumps the model.** The model treats the falling ratio as evidence that performance deteriorated for everyone, missing that continuing units held steady and the entire move is a denominator effect from new volume.

### Confounded co-movement

**What it is.** Two candidate drivers moved at the same time and are correlated with each other, so the raw association cannot separate them without conditioning.

**How it stumps the model.** The model latches onto whichever driver is more salient in the prompt and reports it, never holding the confounder constant to see that the association collapses once the other variable is controlled for.

### Correlated but not causal driver

**What it is.** A variable tracks the metric tightly but is a downstream symptom or a common-cause byproduct rather than the actual cause.

**How it stumps the model.** The model equates the strongest correlation with the root cause and stops, reporting the proxy instead of tracing back to the upstream variable that moves both the metric and the proxy.

### Base-rate neglect

**What it is.** A subgroup shows a large percentage swing but represents so little of the total that it cannot account for the aggregate move.

**How it stumps the model.** The model is drawn to the dramatic subgroup change and names it the driver, without weighting the swing by the subgroup's share, so it credits a segment that contributes almost nothing to the total.

### Seasonality read as a driver

**What it is.** The metric follows a recurring seasonal pattern the series shows every year, but the current dip is treated as a one-time causal event.

**How it stumps the model.** The model compares only against the immediately prior period instead of the same period in prior years, so it mistakes the normal seasonal trough for a new problem and hunts for a spurious cause.

### Aggregation masking the real driver

**What it is.** At the top level the metric looks flat or mildly down, but a large gain in one segment is cancelling a severe collapse in another (a Simpson-style masking).

**How it stumps the model.** The model reasons entirely at the aggregate, concludes the change is small or diffuse, and never disaggregates to find the offsetting movements that hide the one segment actually driving the story.

### Denominator redefinition drift

**What it is.** The population that qualifies for the metric changed over the window because an eligibility or inclusion boundary shifted, altering who is counted honestly.

**How it stumps the model.** The model compares the two periods as if the denominator were the same cohort, attributing the rate change to behavior when it is really who is now inside the measured set.

### Reversion to the mean mistaken for a cause

**What it is.** The metric spiked in the prior period for idiosyncratic reasons and the current move is just a return to the long-run level.

**How it stumps the model.** The model anchors on the abnormal prior period as the baseline, so the natural settling back reads as a decline that needs a driver, and it invents one.

### Single-driver bias on a multi-cause move

**What it is.** The change is the sum of several moderate contributors with no single dominant one, but the task format pressures a one-driver answer.

**How it stumps the model.** The model forces the largest of several similar contributions into the role of primary driver, overstating its share instead of reporting that no single driver dominates and the honest read is a shared cause or a hold.

### No governance document to anchor on

**What it is.** There is no policy memo, definition sheet, or spec stating which factor 'counts' as the driver, so the answer must be earned from the data decomposition alone.

**How it stumps the model.** The model looks for an authoritative statement to quote and, finding none, either fabricates a rule of thumb or defaults to the most-mentioned candidate rather than deriving the driver from the contribution math.

### Insufficient evidence to name one driver

**What it is.** The available tables cannot separate the leading candidates because the key conditioning variable is not present, so the honest output is a hold, not a pick.

**How it stumps the model.** The model produces a confident single driver anyway, treating absence of the discriminating variable as if the remaining correlation settled the question, instead of stating that the evidence does not identify a dominant cause.

### Level change versus trend change

**What it is.** The metric stepped to a new level at one point in time versus drifting gradually, and the two imply completely different classes of cause.

**How it stumps the model.** The model averages over the window and reports a gradual driver when the data show a discrete step, or vice versa, misclassifying the shape of the change and therefore the cause.

### Numerator and denominator moving together

**What it is.** Both parts of a ratio changed, so the ratio's movement understates or overstates what happened to the thing of interest in the numerator.

**How it stumps the model.** The model interprets the ratio as if only the numerator moved, crediting or blaming the top-line behavior when a proportional denominator shift is doing most of the work.

### Lagged driver misattributed to a concurrent event

**What it is.** The true cause acted with a delay, so a visible concurrent event lines up with the metric move by coincidence of timing.

**How it stumps the model.** The model matches the metric move to whatever happened in the same period and ignores the lag structure, naming the concurrent event over the earlier cause whose effect only now surfaced.

### Weighted contribution ignored

**What it is.** Several segments each moved, and identifying the driver requires ranking them by their share-weighted contribution to the total change rather than by their individual rate change.

**How it stumps the model.** The model ranks candidates by the size of their rate move rather than by rate move times share, so it elevates a large-swing small segment over the moderate-swing large segment that actually produced most of the aggregate change.

---

Ask anatomy and example asks for this objective: `../../../guide-to-prompt/references/objectives/root-cause-analysis.md`

Mechanism families, the refusal ladder and the fourteen generators: `../../SKILL.md`
