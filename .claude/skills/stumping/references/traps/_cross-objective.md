# Trap catalog: cross-objective

> These traps are not tied to one Axis 1 objective. They are the constraint, economics, comparison
> and monitoring failures that show up under a forecasting ask as readily as under a root-cause or
> a descriptive one. Read this file **after** the catalog for your own objective, and use it when
> the ladder needs a rung from a family your objective's own catalog does not carry.

**Provenance.** Every trap here already stumped a model, and every one transfers cleanly to at
least two of the live Axis 1 objectives.

**All of these run on honest data.** None of them needs a planted defect, a wrong stated figure or
a lie in the pack, which is why they clear Gate G. Most of them are instances of
`binding_constraint`, `decomposition_attribution`, `method_or_model_selection` or
`statistical_rigor`. Name the label when you adapt one.

---

## The constraint and economics family

The single most reliable non-defect rung available: every reported number is correct, and the
naive ranking still loses to a limit, a cost basis or a horizon the pack files somewhere.

### The binding constraint the naive winner breaches

**What it is.** A hard ceiling (budget, capacity hours, covenant, eligibility floor, concentration
cap) that the highest-value option quietly busts.

**How it stumps the model.** It ranks purely on value and recommends an option the constraint rules
out before scoring even begins. Gate G label: `binding_constraint`.

### The constraint written so it reads like a preference

**What it is.** A covenant, regulatory cap or eligibility rule filed as a boundary but phrased in
language the model can read as tradeable.

**How it stumps the model.** It treats the rule as soft, trades a little compliance for a lot of
value, and recommends something that cannot legally or contractually happen. The repair that keeps
it fair: the rule is filed and unjustified, never argued.

### Capacity saturation

**What it is.** The motion is bounded by a physical limit (chairs, rep-hours, plant throughput,
interconnection, crew availability), not by demand.

**How it stumps the model.** It sizes off demand and lands on a volume the resource cannot deliver.

### Gross versus contribution basis

**What it is.** The decision turns on contribution or fully loaded margin, and the options differ
enough in variable and servicing cost that revenue or gross profit ranks them the other way.

**How it stumps the model.** It ranks on the top line, so the high-revenue heavy-cost option wins on
paper. Pair this with the unit-of-value swap in `SKILL.md`.

### Marginal economics extrapolated linearly

**What it is.** Today's average unit economics stop holding at the target volume because marginal
acquisition cost rises, capacity fills or yield compresses.

**How it stumps the model.** It multiplies current unit economics straight out to target scale and
overstates the option that appears to scale cleanly.

### Cannibalisation inside an incremental number

**What it is.** Part of a new option's "incremental" volume is pulled from an existing product,
channel or catalogue entry.

**How it stumps the model.** It reports the gross figure and misses that the net view reorders the
field. The net calculation has to be reachable from the shipped records, not asserted.

### Ramp time against a decision window

**What it is.** The options ramp at different speeds and the decision window (a hold period, a
break-even horizon, a single funding cycle) decides how much of each option's value lands in time.

**How it stumps the model.** It compares everything at steady state and ranks the slow ramp as if
its full value were available on day one.

### Payback against return

**What it is.** A return measure paired with a time-based hurdle, and the two point at different
options.

**How it stumps the model.** It optimises one and drops the other.

### Sequencing mistaken for selection

**What it is.** Funding one option relieves a bottleneck that raises the value of the others, so
"what first" is not "what is biggest".

**How it stumps the model.** It treats the options as permanently exclusive and picks the largest
standalone value.

### Sunk cost and current-performance anchoring

**What it is.** One option is attached to the biggest existing book or asset.

**How it stumps the model.** It reads past scale as future incremental value.

### The amount is part of the answer

**What it is.** The ask is how much, marginal return falls with spend, and the right amount sits
below the available budget.

**How it stumps the model.** It names a target and defaults the amount to the whole budget, or
leaves it vague.

---

## The comparison family

Every one of these is a comparison whose inputs are all correct and whose conclusion still depends
on a choice the model made silently.

### Definitional change in scope between the two things compared

**What it is.** What the metric counts changed between the two periods or groups, for instance a
widened definition of enrolled, activated or defective, with the rule change filed and dated.

**How it stumps the model.** It differences the two numbers as if they measured the same thing and
credits a real change to a movement that is entirely the change in what was counted. Note this is
**not** a defect: the widening is legitimate and documented, which is what keeps it Gate G clean.

### Different inclusion criteria on each side

**What it is.** The two populations were assembled under different rules for who gets counted, so
one is filtered or trimmed in a way the other is not.

**How it stumps the model.** It compares them as though they were built the same way.

### Standardisation reference population

**What it is.** Adjusting for composition needs a reference population to weight to, and different
defensible references move which group leads.

**How it stumps the model.** It either skips standardisation or applies one weighting silently, and
never checks that the call is robust to the reference. **Determinism note:** if you use this, the
reference has to be pinned in a shipped file or the answer has to hold under every defensible
reference. Otherwise this is a fork, not a trap.

### Baseline or reference group flips the story

**What it is.** The comparison is framed relative to a chosen baseline, and an equally defensible
baseline reverses who looks better.

**How it stumps the model.** It anchors on the baseline handed to it and reports the direction as
fact. Same determinism note as above.

### Confounded gap read as a direct effect

**What it is.** The groups differ on the factor of interest and also on a lurking variable that
independently drives the metric, with that variable shipped as a real column.

**How it stumps the model.** It assigns the whole gap to the named factor. Gate G label:
`decomposition_attribution`.

### Ecological fallacy across aggregation levels

**What it is.** A relationship that holds at the group level and need not hold at the individual
level, or the reverse.

**How it stumps the model.** It transports the comparison between levels without checking.

### Regression to the mean between two readings

**What it is.** Units selected or noticed for an extreme first reading drift back toward typical on
the second, with the pre-selection distribution shipped so the expected drift is computable.

**How it stumps the model.** It reads the settling as a real improvement or decline with a cause.
Gate G label: `statistical_rigor`.

---

## The monitoring and threshold family

Useful under anomaly detection and under ETL, where the deliverable is a rule rather than a number.

### Static threshold on a seasonal series

**What it is.** Diurnal, weekly or close-cycle seasonality sits in the history, so any flat bar has
to account for the cycle.

**How it stumps the model.** It sets one flat number and pages every weekend, or misses a real
break inside a busy period.

### Freshness deadline read off the schedule rather than the arrival distribution

**What it is.** A feed's real arrival times spread around its nominal cadence, so a sound deadline
comes from observed lag.

**How it stumps the model.** It reads the deadline straight off the promised cadence and either
fires on normal jitter or misses a feed that is genuinely late.

### Cross-feed desync

**What it is.** Feeds that must reconcile against each other each look healthy alone while the
match rate between them collapses.

**How it stumps the model.** It monitors each table in isolation. The decisive check lives only in
the join, which is exactly where you want it.

### A rule with no gating action

**What it is.** A check only protects a consumer if firing it blocks a publish, quarantines a batch
or suppresses an output.

**How it stumps the model.** It defines thresholds and never says what trips on them, so the
deliverable detects nothing anyone acts on. Grade the action, not the threshold.

### Trust certified from one clean snapshot

**What it is.** Reliability is a property of behaviour over time, outages, correction latency and
variance, not the tidiness of the current pull.

**How it stumps the model.** It inspects the current sample, finds it clean, and certifies. The
history that contradicts the snapshot has to be in the pack.

---

## Two structural shapes that belong to no family

### No governing document to anchor on

The pack deliberately ships no rule to quote, so the criterion has to be earned from the data,
usually from a calibration corpus of settled cases. This is the shape that most reliably separates
an analyst from a model looking for a sentence to cite, and under Gate G v3 it is the strongest
single move available, because a rule recovered empirically is `method_or_model_selection` by
construction. See `SKILL.md` on the empirical pin.

### The answer is hold

Not enough evidence to make the call is an acceptable final answer, but only when a computed
blocking quantity forces it and that quantity reproduces from the pack like any other number. See
`SKILL.md` on building a hold.
