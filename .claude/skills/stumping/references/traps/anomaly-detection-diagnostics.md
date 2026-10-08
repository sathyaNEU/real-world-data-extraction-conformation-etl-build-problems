# Trap catalog: Anomaly Detection & Diagnostics

> Something in the data looks wrong and the analyst must separate a real event from an artifact.

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

- **No governance document to anchor on**. The pack deliberately ships no rule to quote, so the criterion has to be earned from the data. This is the shape that most often separates a real analyst from a model looking for a sentence to cite.
- **Insufficient evidence: the right call is HOLD**. *Not enough information to make a decision* is now an acceptable final answer, but only when it is forced by the evidence and reproduces like any other answer. See `stumping` Part 6.4 before building one.

## The traps

### No governance document to anchor on

**What it is.** The task ships no SLA, control chart, or rulebook stating what size of deviation counts as actionable, leaving the analyst to derive a defensible threshold from the metric's own history and the cost of acting.

**How it stumps the model.** The model either invents an arbitrary bar like 'anything above 5% is an anomaly' or refuses and demands a rule that was never provided, when the right move is to build the threshold from historical variability.

### Insufficient evidence: the right call is HOLD

**What it is.** Every candidate deviation sits inside normal noise once properly conditioned, so the correct decision is to keep monitoring rather than act.

**How it stumps the model.** The model assumes any task about anomalies must contain an actionable one, so it manufactures a winner and recommends an intervention the data does not support.

### Expected seasonal / calendar variation misread as an event

**What it is.** A spike or dip is fully explained by seasonality, day-of-week, holidays, or weather, so it is routine once measured against the right baseline for that period.

**How it stumps the model.** The model compares the reading against an annual average instead of the seasonally appropriate baseline, so an ordinary swing looks like a novel anomaly.

### Multiple comparisons / look-elsewhere effect

**What it is.** When many series are scanned at once, such as stores, cities, or sensors, at least one will breach any fixed threshold by pure chance.

**How it stumps the model.** The model reports the single most extreme series as the anomaly without accounting for how many series it searched, so it inflates false positives.

### Base-rate neglect

**What it is.** When the true event is rare, even an accurate detector produces mostly false alarms because the low prior swamps the signal.

**How it stumps the model.** The model treats a flagged uptick as probably real without weighting how uncommon the event is, and over-escalates.

### Statistical significance vs. operational severity

**What it is.** Statistical significance measures whether an effect is real, while operational severity measures whether it is large enough in business terms to be worth acting on, and the two can point opposite ways.

**How it stumps the model.** With a huge sample the model escalates a trivial but significant change, and with a short window it dismisses a large, costly swing that failed to reach significance.

### Single-point spike vs. sustained level shift

**What it is.** A transient one-day outlier and a persistent regime change look similar on a chart but call for very different responses.

**How it stumps the model.** The model reacts to the peak day and recommends a durable, expensive intervention for what is really a one-off blip.

### Autocorrelation inflates apparent runs

**What it is.** Serially correlated data naturally produces long runs above or below the mean, so a streak is often just the series repeating itself.

**How it stumps the model.** The model reads a run such as nine days in a row as a deliberate signal, when the series' own autocorrelation makes runs that long common.

### Wrong baseline window

**What it is.** What counts as normal depends on the reference window, and a convenient recent stretch may itself have been a promo, an outage, or a prior peak.

**How it stumps the model.** The model anchors normal to an unrepresentative window, so the current reading looks anomalous or fine purely because of the reference it chose.

### Regression to the mean after an extreme period

**What it is.** After an unusually high or low stretch, a metric tends to drift back toward its long-run average on its own.

**How it stumps the model.** The model reads that reversion as a fresh anomaly or as proof that a prior intervention worked, when it is expected movement.

### Denominator/exposure-driven rate change (non-defect)

**What it is.** A rate moves because legitimate underlying volume changed, such as more transactions or more traffic, not because the numerator behavior shifted. The data are correct; the work is to normalize by real exposure.

**How it stumps the model.** The model reads the rate move as an anomaly instead of normalizing by the legitimately varying exposure and checking for a residual beyond it.

### Competing anomalies: pick the actionable one

**What it is.** Several series breach at once, and the one worth the single available intervention depends on persistence, cost, reversibility, and confidence, not size alone.

**How it stumps the model.** The model picks the largest deviation or biggest z-score, ignoring that the most extreme series is not always the most actionable.

### Threshold gaming at the boundary

**What it is.** The deviation lands just over a plausible action line while its confidence interval straddles that line, so the call is not robust.

**How it stumps the model.** The model treats 'over the line' as decisive and ignores that the uncertainty around the estimate crosses the threshold.

### Leading indicator vs. lagging confirmation

**What it is.** An early-warning signal like rising vibration or complaints climbs before the headline outcome such as power output or revenue shows any damage.

**How it stumps the model.** The model dismisses the early signal because the outcome metric still looks fine, missing the lead-lag relationship that justifies acting sooner.

### Simpson's reversal across segments

**What it is.** A stable-looking aggregate can hide a real event inside one subgroup, and a moving aggregate can be a mix shift with no subgroup actually changing.

**How it stumps the model.** Reading only the whole-population view, the model conceals a localized event or invents a spurious global one it never traced to a segment.

### Reporting/collection cadence artifacts (non-defect)

**What it is.** Legitimate reporting rhythms like weekend under-reporting, month-end batch posting, and backfill lag create sawtooth patterns. The data are correct; the cadence just needs to be accounted for.

**How it stumps the model.** The model flags a routine cadence-driven dip or spike as an anomaly instead of comparing like periods against the cadence-adjusted expectation.

### Cost-asymmetry of the decision

**What it is.** The real decision carries lopsided costs, where a missed event is catastrophic or an unnecessary intervention is very expensive, so the cost-optimal threshold is not the symmetric one.

**How it stumps the model.** The model applies a symmetric 'is it significant?' test and picks the statistically tidy answer instead of the one that minimizes expected cost.

### Short-window overreaction / not enough data yet

**What it is.** Only a few days of the apparent anomaly exist, too little to separate signal from noise with any confidence.

**How it stumps the model.** The model commits to an expensive, hard-to-reverse action on a sample that lacks the power to support it, rather than defining a confirmation window.

---

Ask anatomy and example asks for this objective: `../../../guide-to-prompt/references/objectives/anomaly-detection-diagnostics.md`

Mechanism families, the refusal ladder and the fourteen generators: `../../SKILL.md`
