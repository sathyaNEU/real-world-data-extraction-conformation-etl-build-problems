# Trap catalog: Descriptive & Distribution Analysis

> The decision turns on how a population is composed or how a metric is distributed, not on why it moved.

**15 traps.** One catalog file per Axis 1 objective that has one (Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting have none of their own). Read `_cross-objective.md` alongside it, which carries the constraint, comparison and monitoring families that are not tied to one objective.

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

## The traps

### Mean/median summary hides the shape

**What it is.** A single central-tendency number stands in for the whole variable even though the underlying distribution is skewed, heavy-tailed, or multimodal and no one value is actually typical.

**How it stumps the model.** The model reports the mean or median plus maybe a standard deviation, then reasons as if the population were unimodal and symmetric. Its 'typical' value points at a region where almost no observations sit.

### Hidden sub-population (mixture masquerading as one group)

**What it is.** What reads as one broad distribution is really two or more populations laid on top of each other, like trial versus paying users or two device classes sharing an axis.

**How it stumps the model.** The model fits a single description, so its average segment describes nobody. Alternatively it draws a boundary straight through the middle of a real cluster.

### Heavy tail drives the aggregate but not the count

**What it is.** A handful of extreme observations, the whales or mega-orders or catastrophic claims, hold most of a metric's total while making up a tiny slice of the population.

**How it stumps the model.** The model conflates where the volume sits with where the customers sit. It recommends for the many when the money lives with the few, or the reverse, and never flags the split.

### Cutoff instability (the boundary is not robust)

**What it is.** A threshold gets placed on a steep, smooth part of the curve, so nudging the line even slightly reshuffles a large share of the population between tiers.

**How it stumps the model.** The recommendation looks precise but is fragile. A grader who moves the cutoff a little would land on a very different segmentation.

### Materiality vs distinctness trade-off

**What it is.** The most sharply separated segment is often tiny and not worth acting on, while the segment big enough to matter has fuzzy edges, forcing a trade between cleanliness and scale.

**How it stumps the model.** The model optimizes one property alone. It either recommends a beautifully distinct micro-segment that fails on size, or a huge vague blob that fails on coherence.

### Wrong unit of analysis / grain

**What it is.** The question is about people (customers, drivers, households) but the data sits at the transaction, session, or order level, so the two grains describe different things.

**How it stumps the model.** The model describes the distribution of events and reports it as the distribution of people. Frequent actors dominate and the population gets mischaracterized.

### Number-of-groups is a real choice, not a given

**What it is.** A prompt asks for tiers or bands without saying how many, leaving the count of groups as a genuine modeling decision the shape of the data should settle.

**How it stumps the model.** The model defaults to three, or whatever is conventional, without checking whether the data supports two or four. It either over-segments a smooth curve or collapses distinct groups together.

### Percentile tiers on a lumpy distribution

**What it is.** Equal-count quantile bins like quartiles or deciles assume a smooth continuous variable, but many variables are discrete or clumped, for example order sizes that are mostly exactly 1 or 2 items.

**How it stumps the model.** The model reaches for quantile cuts by reflex. Boundaries land inside a spike of identical values and split those identical entities across different tiers.

### Concentration metric misread

**What it is.** Concentration summaries like a Gini coefficient, a top-decile share, or an HHI are facts about where a metric pools, not verdicts and not answers by themselves.

**How it stumps the model.** The model quotes the number but never ties it back to the decision. It treats high concentration as automatically bad, or as the answer itself, rather than as guidance on where to target.

### Zeros and non-participants folded into the shape

**What it is.** A big mass of zeros or inactive entities, the never-spenders, no-claims policies, and dormant accounts, sits right next to the active distribution and belongs to a separate participation question.

**How it stumps the model.** The model either lets the zero spike dominate its description or quietly drops it. Either way it mischaracterizes who the population really is.

### Distribution vs its driver (composition confound)

**What it is.** The pooled shape is really the product of a mix shift across some obvious subgroup, so a mode or break in it is a proxy for that known category rather than a new behavioral segment.

**How it stumps the model.** The model describes the pooled shape and picks a boundary that just re-traces the subgroup split. It presents a known category as if it were a discovered segment.

### Outliers vs the genuine tail

**What it is.** Reflexive outlier rules like dropping beyond 3 SD or winsorizing the top 1% cannot tell an implausible data-entry value from a real, decision-relevant extreme.

**How it stumps the model.** The model applies the blanket rule and deletes exactly the heavy tail the task is about. Or it keeps absurd data-entry values that then distort every statistic.

### Smooth distribution with no natural break

**What it is.** Some variables are a genuine continuum with no gap, shoulder, or antimode anywhere, so there is simply no data-driven place to cut.

**How it stumps the model.** The model hunts for a natural boundary that does not exist and reports a spurious one. Or its break-finding approach returns nothing and it stalls.

### Log-scale phenomenon read on a linear axis

**What it is.** Spend, usage, and value variables are often roughly log-normal or power-law, and their tier structure only shows up once you look at them on a log scale.

**How it stumps the model.** On a linear axis everything crams against the left with a long right smear, so the model calls it one big low group plus outliers and misses the multiplicative structure that reveals the real tiers.

### Coherence of the recommended segment is asserted, not shown

**What it is.** A segment defined by one variable can still be wildly mixed on every other dimension that matters for the action, so internal similarity has to be demonstrated, not assumed.

**How it stumps the model.** The model names a target segment and assumes its members resemble each other. It never checks the other dimensions, so the group may be heterogeneous on exactly what the intended action depends on.

---

Ask anatomy and example asks for this objective: `../../../guide-to-prompt/references/objectives/descriptive-distribution-analysis.md`

Mechanism families, the refusal ladder and the fourteen generators: `../../SKILL.md`
