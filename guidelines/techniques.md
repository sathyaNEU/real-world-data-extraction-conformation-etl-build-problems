# Task Design Reference

> ## BAR UPDATE (2026-09-05), OPERATIVE, supersedes the 2026-08-27 block below
>
> **A task passes when the top two responses average under 70 percent against the generated rubric
> and at least one response is genuinely stumped**, well below the bar. The threshold moved from 50
> to 70 on 2026-09-05; the **top-two structure never went away**, and the two conditions are
> conjunctive. The *all-models* stump stays retired, but **one genuine stump is a pass condition
> again**, so the mechanisms below are load-bearing in their own right rather than
> difficulty-flavouring behind a hard ask set.
>
> **Build to 60, not to 70**, because the on-platform verifiers are not perfectly accurate and the
> task is regraded more accurately after submission.
>
> Read the other half too. The asks carry about 55 percent of the score, and the 2026-09-05 spec
> asks for **uncapped, multi-dimensional** asks rather than a litany of basic ones, because a
> multi-dimensional ask is **correlated**: a solver holding the wrong structure loses all of it at
> once. Put that width on the asks the strongest solver cannot get right.
>
> **The mechanism rules below are unchanged and reaffirmed.** The planted defect and the
> flip-the-wrong-number trap stay retired, and the valid shapes remain the honest-data versions of
> the same six mechanisms: forecasting, method selection, a binding constraint, a decomposition, a
> confirm-the-number, and a hold. On honest data the mixed-subgroup lead is real and the trap is
> the tempting adjustment that would wrongly flip it; the metrics are both measured correctly and
> the work is choosing the one the problem structure requires; every extract is present and the
> top-ranked option breaks a capacity limit; the label semantics are documented and the work is
> conforming them to one event definition; the timestamps are correct and a known schedule change
> makes the next period genuinely differ; the rate and its denominator are correct and a real
> limit caps which option is feasible.

> ## BAR UPDATE (2026-08-27), SUPERSEDED by the 2026-09-05 block above, retained for reference
>
> The "stump the model" bar is retired. A task now passes when the **top two of twelve model
> responses average under 50 percent** against the generated rubric (`rubric.md`), so breadth
> across the deliverable asks now does real work alongside the trap. The mechanism rules below
> are unchanged and reaffirmed by the same update: the planted defect and the
> flip-the-wrong-number trap stay retired, and the valid shapes remain the honest-data versions
> of the same six mechanisms, forecasting, method selection, a binding constraint, a
> decomposition, a confirm-the-number, and a hold. On honest data the mixed-subgroup lead is
> real and the trap is the tempting adjustment that would wrongly flip it; the metrics are both
> measured correctly and the work is choosing the one the problem structure requires; every
> extract is present and the top-ranked option breaks a capacity limit; the label semantics are
> documented and the work is conforming them to one event definition; the timestamps are correct
> and a known schedule change makes the next period genuinely differ; the rate and its
> denominator are correct and a real limit caps which option is feasible.

> ## TRAP UPDATE (2026-08-20), OPERATIVE, supersedes the 2026-08-16 update and everything below
>
> Determinism judge v3 went further than the planted-defect retirement. **Surface-read rejection is
> banned as the primary stumping strategy at any depth.** A compound chain of two, three or four
> forced corrections is not a defence. Neither is an official artifact whose methodology is wrong
> and takes real recomputation to refute. Both were explicitly protected under v2 and both fail now.
> A third shape is banned too, `single_conceptual_flip`: honest data, an arithmetically correct
> stated number, and one lens or definition swap that flips the naive read.
>
> **The litmus, answered before anything else:** is the reported number or stakeholder conclusion
> the task overturns actually wrong or misleading, and is catching that the main thing that defeats
> the model? Yes to both is a send-back however many corrections it takes.
>
> **What this retires inside this file.** Any family whose payoff is "the shipped figure is wrong,
> catch it" is now a supporting rung at most. That includes the loud artifact, the stale-document
> traps, and Family D. They are still usable as texture at rung 1 or 2. They cannot be the decisive
> move.
>
> **What passes.** `forecasting` · `method_or_model_selection` · `binding_constraint` ·
> `decomposition_attribution` · `signal_vs_noise_or_hold` · `confirm_surface_read` ·
> `etl_conformance`. Name your primary mechanism with the judge's own label in the design note.
>
> **Read `.claude/skills/stumping/SKILL.md` Parts 1 and 2 before using any family below.** Part 1 carries
> the four gaps where difficulty can live when every number in the pack is correct, and Part 2
> carries the five patterns with the best approval record. This file is a catalog; that skill is the
> current standard.

Two complementary guides for authoring decision tasks that stump frontier models and reward careful analysts.

| Resource | What it is | Families |
|----------|------------|----------|
| [Part 1, Trap Catalog](#part-1-trap-catalog) | **14 Proven-in-Production traps**, the subset of the full catalog that has held up in shipped, graded tasks. Each trap includes symptom, why models miss it, a realistic example, its in-corpus antidote, pairings, and the Fundamentals behaviors it targets. | A–F (aggregation, causality, time, joins, documents, definitions) |
| [Part 2, Stumping Strategies](#part-2-stumping-strategies) | Task-authoring playbooks from graded tasks | A–E (headline metric, decoys, answer shape, arithmetic, rival stories) |
| [Older Task Feedbacks](#older-task-feedbacks) | Post-review lessons from shipped tasks | Spotlight task (determinism, brief, generation tells) |

> **Note:** Both use letters A–E but mean different things. Catalog **A1** = Simpson's paradox; Stumping **A1** = corrupt numerator and denominator at once.

> **Why only Proven-in-Production?** The full source catalog has 75 traps across the six families. Only the 14 below are flagged *Proven in production* in the [source catalog](https://project-mark.learn.joinhandshake.com/trap-design/catalog), they have carried shipped, graded tasks. The unproven traps have been removed from this file to keep the working set high-signal. If you want to reach outside this set, verify against the source catalog first.

---

# Part 1: Trap Catalog

> **14 Proven-in-Production traps** across **6 families**. Every trap has a stable URL: `.../catalog?family={A–F}#trap-{ID}`
> Each family lists the proven traps in a summary table, then gives **Trap Detail** for each carrying, per trap: **why models miss it**, a **realistic example**, the **in-corpus antidote**, **cross-family pairings**, and the [**Fundamentals**](#fundamentals--targeted-failure-behaviors) behaviors it targets.

**Source:** [Handshake Trap Design Catalog](https://project-mark.learn.joinhandshake.com/trap-design/catalog)

## Trap Catalog: Table of Contents

| Family | Title | Proven traps | Tagline |
|--------|-------|--------------|---------|
| [A](#family-a--aggregation-and-statistics) | Aggregation and statistics | 5 | The number is computed correctly and still means the wrong thing. |
| [B](#family-b--experiment-and-causality) | Experiment and causality | 2 | The comparison looks clean but the design underneath it is broken. |
| [C](#family-c--time-and-comparability) | Time and comparability | 1 | Two periods are placed side by side that were never comparable. |
| [D](#family-d--plumbing-and-joins) | Plumbing and joins | 2 | The data loads fine and the grain, keys, or units are lying. |
| [E](#family-e--documents-and-formats) | Documents and formats | 3 | The decisive fact is present, just not where a skim will find it. |
| [F](#family-f--definitions-and-framing) | Definitions and framing | 1 | The metric named in the prompt is not the metric the decision needs. |

---

## Family A: Aggregation and Statistics

**5 proven traps** · [View family A](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=A)

> The number is computed correctly and still means the wrong thing.

| ID | Trap | Symptom |
|----|------|---------|
| [A1](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=A#trap-A1) | **Simpson's paradox and mix shift** | The blended number moves one way while every segment moves the other. |
| [A5](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=A#trap-A5) | **Totals vs rates** | A headline count moves because the denominator moved. |
| [A7](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=A#trap-A7) | **Noise mistaken for trend** | A short move sits comfortably inside normal variance. |
| [A8](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=A#trap-A8) | **Seasonality read as effect** | The lift is the calendar, not the change. |
| [A10](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=A#trap-A10) | **Small-sample overgeneralization** | The winning cell is tiny. |

### Family A: Trap Detail

#### A1 · Simpson's paradox and mix shift

> The blended number moves one way while every segment moves the other.

**Why models miss it**, Models compute the headline rate and stop before segmenting.

**Realistic example**, Overall conversion is up 2 points, but every segment is down. Growth came from a mix shift toward a high-converting, low-LTV segment.

**In-corpus antidote**, Segment volumes in a separate dimension file, so the weighted decomposition is fully derivable.

**Pairs well with**, `D12` Dirty keys with meaning · `C12` Instrumentation change, not behavior change

**Targets**, 02 Anchoring on the first plausible number, 08 Arithmetic shortcuts *(Fundamentals)*

#### A5 · Totals vs rates

> A headline count moves because the denominator moved.

**Why models miss it**, Models report totals when the decision depends on a rate.

**Realistic example**, Support tickets doubled, but users tripled. The ticket rate actually fell.

**In-corpus antidote**, The user-count file covers the same window, so the rate is a one-step calculation.

**Pairs well with**, `F1` Competing metric definitions · `A1` Simpson's paradox and mix shift

**Targets**, 02 Anchoring on the first plausible number *(Fundamentals)*

#### A7 · Noise mistaken for trend

> A short move sits comfortably inside normal variance.

**Why models miss it**, Models build a narrative out of three data points.

**Realistic example**, A two-week decline is within the weekly variance visible in the 18-month history file.

**In-corpus antidote**, The long history file makes the variance band obvious.

**Pairs well with**, `A8` Seasonality read as effect · `B6` Underpowered null

**Targets**, 01 Head-of-file sampling, 02 Anchoring on the first plausible number *(Fundamentals)*

#### A8 · Seasonality read as effect

> The lift is the calendar, not the change.

**Why models miss it**, Models do not check the same window a year earlier.

**Realistic example**, A feature launched in November shows a lift that matches last year's holiday bump exactly.

**In-corpus antidote**, Prior-year data for the same weeks is in the corpus.

**Pairs well with**, `A7` Noise mistaken for trend · `C12` Instrumentation change, not behavior change

**Targets**, 02 Anchoring on the first plausible number, 10 Time laziness *(Fundamentals)*

#### A10 · Small-sample overgeneralization

> The winning cell is tiny.

**Why models miss it**, Models rarely compute or sanity-check n before ranking.

**Realistic example**, The winning variant leads in a segment with n equal to 43.

**In-corpus antidote**, Counts sit next to the rates in the same table.

**Pairs well with**, `B6` Underpowered null · `A7` Noise mistaken for trend

**Targets**, 08 Arithmetic shortcuts, 12 Premature synthesis *(Fundamentals)*

---

## Family B: Experiment and Causality

**2 proven traps** · [View family B](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=B)

> The comparison looks clean but the design underneath it is broken.

| ID | Trap | Symptom |
|----|------|---------|
| [B6](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=B#trap-B6) | **Underpowered null** | No significant effect is read as no effect. |
| [B9](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=B#trap-B9) | **Hidden confounder** | The correlation is produced by an eligibility rule. |

### Family B: Trap Detail

#### B6 · Underpowered null

> No significant effect is read as no effect.

**Why models miss it**, Models treat a wide confidence interval as evidence of equivalence.

**Realistic example**, The interval spans minus 2 percent to plus 14 percent and the deck calls it flat.

**In-corpus antidote**, Sample sizes and the interval are both printed in the readout.

**Pairs well with**, `A10` Small-sample overgeneralization · `E3` Authoritative but stale document

**Targets**, 08 Arithmetic shortcuts, 12 Premature synthesis *(Fundamentals)*

#### B9 · Hidden confounder

> The correlation is produced by an eligibility rule.

**Why models miss it**, The rule lives in an event schema doc, not the data.

**Realistic example**, Users of feature X retain better because feature X is only surfaced after onboarding step 5.

**In-corpus antidote**, The event schema doc states the surfacing rule.

**Pairs well with**, `F1` Competing metric definitions · `E1` Footnote overrides the table

**Targets**, 07 Format blind spots, 12 Premature synthesis *(Fundamentals)*

---

## Family C: Time and Comparability

**1 proven trap** · [View family C](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=C)

> Two periods are placed side by side that were never comparable.

| ID | Trap | Symptom |
|----|------|---------|
| [C12](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=C#trap-C12) | **Instrumentation change, not behavior change** | The event changed, the users did not. |

### Family C: Trap Detail

#### C12 · Instrumentation change, not behavior change

> The event changed, the users did not.

**Why models miss it**, Models read event volume as user behavior.

**Realistic example**, Signups dropped 40 percent because the event was renamed and split mid-period.

**In-corpus antidote**, The engineering changelog records the rename and the new event names appear in the stream.

**Pairs well with**, `A8` Seasonality read as effect · `A1` Simpson's paradox and mix shift

**Targets**, 09 Definition sloppiness, 06 Absence of data as signal *(Fundamentals)*

---

## Family D: Plumbing and Joins

**2 proven traps** · [View family D](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=D)

> The data loads fine and the grain, keys, or units are lying.

| ID | Trap | Symptom |
|----|------|---------|
| [D3](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=D#trap-D3) | **Partial duplicates** | Duplicates that carry distinct IDs, so they never look like duplicates. |
| [D12](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=D#trap-D12) | **Dirty keys with meaning** | The dirt is a breadcrumb pointing at one broken source. |

### Family D: Trap Detail

#### D3 · Partial duplicates

> Duplicates that carry distinct IDs, so they never look like duplicates.

**Why models miss it**, Models check for exact dupes only.

**Realistic example**, Retried payment events share an idempotency key while having new event IDs.

**In-corpus antidote**, The idempotency key is present and the payments README explains retries.

**Pairs well with**, `D12` Dirty keys with meaning · `A5` Totals vs rates

**Targets**, 11 Join naivety, 01 Head-of-file sampling *(Fundamentals)*

#### D12 · Dirty keys with meaning

> The dirt is a breadcrumb pointing at one broken source.

**Why models miss it**, Models normalize casing and move on without asking where the variants came from.

**Realistic example**, US, us, and a space-padded US all come from one integration that also drops a required field.

**In-corpus antidote**, The source system column identifies which integration produced each row.

**Pairs well with**, `D3` Partial duplicates · `A1` Simpson's paradox and mix shift

**Targets**, 06 Absence of data as signal *(Fundamentals)*

---

## Family E: Documents and Formats

**3 proven traps** · [View family E](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=E)

> The decisive fact is present, just not where a skim will find it.

| ID | Trap | Symptom |
|----|------|---------|
| [E1](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=E#trap-E1) | **Footnote overrides the table** | The qualifier lives pages away from the number. |
| [E3](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=E#trap-E3) | **Authoritative but stale document** | A polished deck beats a raw file in a model's mind. |
| [E7](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=E#trap-E7) | **Long-file burial** | The number that decides it is on page 14 of 18. |

### Family E: Trap Detail

#### E1 · Footnote overrides the table

> The qualifier lives pages away from the number.

**Why models miss it**, Models read the table and skip the appendix.

**Realistic example**, Excludes marketplace transactions, see appendix C, and appendix C holds the reconciliation.

**In-corpus antidote**, The appendix is in the same PDF and is explicit.

**Pairs well with**, `E7` Long-file burial · `E3` Authoritative but stale document

**Targets**, 07 Format blind spots, 04 Authority over correctness *(Fundamentals)*

#### E3 · Authoritative but stale document

> A polished deck beats a raw file in a model's mind.

**Why models miss it**, Models rank formatting as authority.

**Realistic example**, The dashboard PDF was exported before the restatement, per the tiny footer date.

**In-corpus antidote**, The export date and the restatement memo date can be ordered.

**Pairs well with**, `E1` Footnote overrides the table · `E7` Long-file burial

**Targets**, 04 Authority over correctness *(Fundamentals)*

#### E7 · Long-file burial

> The number that decides it is on page 14 of 18.

**Why models miss it**, Models skim long PDFs and quote the summary page.

**Realistic example**, The quarterly business review holds the segment table deep in the appendix.

**In-corpus antidote**, The table is legible text, not an image, and it is indexed in the contents.

**Pairs well with**, `E1` Footnote overrides the table · `E3` Authoritative but stale document

**Targets**, 01 Head-of-file sampling, 07 Format blind spots *(Fundamentals)*

---

## Family F: Definitions and Framing

**1 proven trap** · [View family F](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=F)

> The metric named in the prompt is not the metric the decision needs.

| ID | Trap | Symptom |
|----|------|---------|
| [F1](https://project-mark.learn.joinhandshake.com/trap-design/catalog?family=F#trap-F1) | **Competing metric definitions** | Two teams define conversion differently and the decision hinges on which one applies. |

### Family F: Trap Detail

#### F1 · Competing metric definitions

> Two teams define conversion differently and the decision hinges on which one applies.

**Why models miss it**, Models grab the nearest definition.

**Realistic example**, Marketing's conversion is visit to signup and product's is signup to activation.

**In-corpus antidote**, The stakeholder's question implies one of them, and a definitions doc pins both.

**Pairs well with**, `A5` Totals vs rates · `B9` Hidden confounder

**Targets**, 09 Definition sloppiness *(Fundamentals)*

---

## Fundamentals: Targeted Failure Behaviors

Every trap's **Targets** line points at one or more of these twelve model behaviors. They are the reason a trap fires.

| # | Behavior |
|---|----------|
| 01 | Head-of-file sampling |
| 02 | Anchoring on the first plausible number |
| 03 | No cross-file reconciliation |
| 04 | Authority over correctness |
| 05 | Plausibility bias |
| 06 | Absence of data as signal |
| 07 | Format blind spots |
| 08 | Arithmetic shortcuts |
| 09 | Definition sloppiness |
| 10 | Time laziness |
| 11 | Join naivety |
| 12 | Premature synthesis |

---

## Trap Catalog: Quick Reference by Symptom

References only the 14 proven-in-production traps kept above.

| If you see… | Check trap(s) |
|-------------|---------------|
| Blended metric contradicts the segments | A1 |
| Headline count moves because the denominator moved | A5 |
| A short move looks like a trend | A7 |
| The lift matches the calendar | A8 |
| Winning cell / segment / cohort is tiny | A10 |
| A wide confidence interval read as "no effect" | B6 |
| Correlation appears because of an eligibility rule | B9 |
| Event volume changed but user behavior did not | C12 |
| Duplicates that carry distinct IDs (retries, resends) | D3 |
| Dirty key values trace to one broken source integration | D12 |
| Decisive qualifier sits in a footnote or appendix | E1 |
| Polished deck / dashboard is beating a raw file | E3 |
| Decisive fact is on page 14 of an 18-page PDF | E7 |
| Two teams define the same metric differently | F1 |

---

# Part 2: Stumping Strategies

> How to author a decision task that three frontier models get wrong and a careful analyst gets right. 
> Every strategy below is drawn from a task that actually held up in grading, and every anti-pattern is drawn from one that did not.

## Stumping Strategies: Table of Contents

| Family | Title | Strategies |
|--------|-------|------------|
| [A](#stumping-family-a--undermine-the-headline-metric) | Undermine the headline metric | A1–A6 |
| [B](#stumping-family-b--disqualify-every-named-candidate) | Disqualify every named candidate | B1–B4 |
| [C](#stumping-family-c--reshape-the-answer-the-model-expects) | Reshape the answer the model expects | C1–C3 |
| [D](#stumping-family-d--change-the-arithmetic) | Change the arithmetic | D1–D4 |
| [E](#stumping-family-e--rule-out-the-rival-story) | Rule out the rival story | E1–E4 |

---

## Stumping Family A: Undermine the Headline Metric

**Core idea:** The stakeholder names a number in the prompt. Make that number unusable, and make the correct read require rebuilding it on a different foundation.

### Stumping A1: Corrupt the Numerator and Denominator at Once

**The setup.** In the e-commerce task (0.03), a tag container published at 10:47 UTC on the same day as the redesign broke the view-event stream in two ways:

- **Numerator inflated**, duplicated view fires.
- **Denominator deflated**, stopped emitting views for low-engagement bounce sessions.

The two defects roughly cancel. The headline adoption tile reads flat before and after, about 31.5% both sides.

**The trap.** A model that finds the duplication bug, corrects for it, and concludes the metric is fine has walked into it.

**The path through.** Recognize that the stream is corrupt in both directions and cannot be repaired. Rebuild adoption on a denominator the tag cannot touch: server-confirmed cart events over CDN edge requests.

**Why it works.** Models are trained to find a bug. Finding a second bug that hides the first is a different task.

**How to build it:**

1. Pick a ratio metric.
2. Corrupt the numerator with an obvious defect and the denominator with a subtle one.
3. Size them so the ratio looks stable.
4. Ship a tag-independent or server-side source that makes the true read recoverable.

---

### Stumping A2: Force Reasoning from Data That Was Withheld

**The setup.** In the hospital task (0.02), four patient-safety measures for the correct site appear in the earliest reporting cycle and are then withheld under a suppression footnote in the two later cycles. Every measure that remains visible is flat. The composite rises from about 0.89 to about 2.27.

**The path through.** Arithmetic on the absence. A composite built from all components, including suppressed ones, cannot rise 150% while every visible component holds flat unless the invisible ones deteriorated.

**Rubric pairing.** The task carries a penalty for fabricating values for the withheld measures, which is exactly the failure mode this invites. Pair the mechanism with that penalty.

**The near-miss to ship alongside.** The same task ships a second site whose measures were never reported at all, due to insufficient volume. That is a different thing from reported-then-withheld, and the rubric rewards distinguishing them. Shipping the near-miss alongside the real signal is what makes the inference load-bearing rather than lucky.

---

### Stumping A3: Denominator Artifacts, in Both Directions

Ship both mirror-image versions at once so the model cannot pattern-match.

| Pattern | What happened | Example |
|---|---|---|
| **Rate up, count flat** | The rate rose because the denominator collapsed | Hospital decoy: harm count steady at ~40–42 events across three cycles while inpatient volume fell 46% |
| **Count up, rate flat** | The count rose because the population doubled | Hospital decoy: rate up 5%, volume up 108% |
| **Normalized variant** | Airline-controlled delay minutes per scheduled flight | Airline task (0.40): Atlanta at ~12.47 vs 5.23 and 2.02, where raw totals point somewhere else |

**How to build it:**

- Whenever you ship a rate, ship the denominator separately and make it move.
- Whenever you ship a count, make the exposure base move.

---

### Stumping A4: Source-of-Truth Hierarchy

**The setup.** Ship two files that disagree about the same fact, where one is a system of record and the other is derived.

The payments task (0.36) ships a settlements ledger showing BNPL orders completing at a normal 69% rate, against a funnel flag reading 15%. Every other payment method reconciles between the two exactly one to one.

**Why the answer is forced.** That one-to-one agreement everywhere else establishes that "settled" means "completed" in this data. The single outlier has to be the flag, not the payments. The correct call is to fix the event mapping, not to disable the product.

**How to build it:**

1. Make the derived metric the one the stakeholder is watching.
2. Make the ledger boring and buried.
3. Reconcile every other segment perfectly so the exception is arithmetic rather than opinion.

---

### Stumping A5: Censoring and Maturity Illusions

**The setup.** Confirmed outcomes lag the events that cause them. Ship a snapshot whose recent window is therefore artificially clean, and a stakeholder reading it as improvement.

**Batch examples:**

| Task | Mechanism |
|---|---|
| Fraud-model (0.32) | Lags chargeback confirmations by ~10–100 days (avg ~40), making the post-cutover month look like a fraud collapse |
| Screening (0.27) | Correcting observed chargeback rates for maturity moves a recently deployed config from ~0.15% observed to ~0.35% matured, changing which configs breach a hard ceiling |
| Healthcare (0.53) | Same illusion on readmission windows |

**How to build it:**

1. Pick any outcome with a real-world reporting lag.
2. End your data snapshot inside that lag.
3. Make the censored window the one the stakeholder cites.

---

### Stumping A6: Blended Figures Hiding a Mix Shift

**The setup.** A channel, cohort, or segment ranks last on a blended metric purely because of who is in it.

The marketing task (0.33) ships a channel whose last-place blended conversion rank is entirely explained by a thin returning-user base, and which is a statistical tie once you segment to new users. The correct call includes explicitly **not** cutting it.

**Rubric pairing.** Require a significance test. That task's only defensible lean is the one difference that is actually significant, and rubrics in this batch penalize asserting or dismissing significance without testing.

---

## Stumping Family B: Disqualify Every Named Candidate

**Core idea:** The prompt hands the model a menu. Every item on it is wrong.

### Stumping B1: Name the Decoys in the Prompt, Put the Answer Off the Menu

**The setup.** The hospital task's prompt names three sites, each pushed by a different internal stakeholder with a different motive:

- Service line chiefs want site one.
- The analytics lead insists on site two.
- Site three's CMO called unprompted to get ahead of their numbers.

All three are wrong. The answer is a site nobody mentioned.

**Why it works.** Social pressure in the prompt is not decoration. It gives the model three confident narratives to choose from, and every one of them is a trap.

**How to build it:**

1. Write the prompt in a real executive's voice, with named internal advocates who disagree.
2. Disqualify each named candidate by a different mechanism, so no single correction clears the board.

---

### Stumping B2: The Obvious Cut Is Load-Bearing

**The setup.** The category task (0.09) asks which single product category to discontinue.

- **Components** has the lowest contribution-margin rate (~6%), making it the obvious answer.
- The bill of materials shows Components SKUs supply all Bike SKUs.
- **Bikes** are the largest contribution pool in the portfolio (~$681,000).
- Cutting Components takes Bikes with it. **Clothing** is the right answer: lowest contribution dollars (~$47,000) and no downstream dependency.

**Secondary lesson.** The task quietly teaches the right comparison basis, absolute contribution dollars rather than margin percentage, which is a second place models slip.

**How to build it:**

1. Give the obviously worst-performing entity a hidden dependency in a file the model has to join to notice.
2. Make the correct answer the second-worst on the obvious metric.

---

### Stumping B3: Hard Constraints in Prose That Close the Decision Space

**The setup.** Bury eliminating constraints in handbooks, agreements, and scanned PDFs rather than in the data files.

| Task | Constraints |
|---|---|
| Screening (0.27) | Starts with 12 candidate configurations; knocks out most before optimization: one threshold tier breaches daily surge review capacity of 1,550; another tier plus one config breach a 0.62% matured dispute ceiling; one model version fails a 90-day production-decisioning rider (shadow-only since June 20) |
| Growth-program (0.36) | Hard $150,000 cap plus documented affiliate clawback of $1,223,473 that destroys the option the partnerships lead is advocating for |

**How to build it:**

1. State each constraint once, in prose, in a document the model has to actually read rather than parse.
2. Make at least one constraint eliminate the option that looks best on the headline numbers.

---

### Stumping B4: Version-of-Record Traps

**The setup.** The allocation task (0.30) ships 33 files including plan revisions two, three, and four, an assignment export plus its retry, and multiple snapshots of the same membership.

- Only one plan is the active approved one.
- Only one routing map is valid for the launch.
- Assignment must be classified by audience membership at assignment time, not by the latest snapshot.
- Orders must be linked by the identity relationship in effect on the order date, not the latest.
- The unique winning portfolio beats the runner-up by 239.015 vs 238.677 expected purchases. A single wrong version anywhere changes the answer.

**How to build it:**

1. Ship the stale version as the more complete-looking, more recently named file.
2. Make the active-version signal a single line in a release log or review PDF.
3. **Use with care.** This is a work-volume trap as much as a reasoning trap; 33 files is near the ceiling of what is fair.

---

## Stumping Family C: Reshape the Answer the Model Expects

**Core idea:** The stakeholder frames a binary. The correct answer has a different shape.

### Stumping C1: The Answer Is "None"

**The setup.** The merchandising task (0.31) asks which category to cut. The correct answer is to cut nothing, and specifically to reject cutting the category that looks worst.

**Why it works.** The apparent decline is real and already reversed inside the shipped data.

- Garden and Outdoor falls from 36,826 to 23,002 pounds between Q2 and Q3, the only category to decline.
- October + November revenue is 26,872, exceeding the entire Q3 total.
- Three structural explanations are shipped and each falsifiable from the records: cancellations stay under 1% of revenue, top-five customer share holds at 14–15%, and the UK stays near 90% and declines at the category rate.

**Second example, DAU task (0.38).** The room is split between cutting a channel and restoring a paid budget.

- Reported January DAU is already ~4% above November, so there is no churn to stop.
- Paid clicks are a flat 4–5% of DAU, so restoring the budget cannot move the aggregate.
- Both options in the room are wrong.

**How to build it:**

1. Make the apparent problem genuinely visible in the obvious comparison window.
2. Ship the reversal or the falsification just outside it.
3. **Watch the trap on the other side.** That task's rubric penalizes presenting the rebound as proof of an annual seasonal cycle, since the data only supports an observed within-sample recovery.

---

### Stumping C2: The Answer Is Scoped, Not Binary

**The setup.** The fraud-model task (0.32) asks whether to keep or roll back a model. The answer is neither: keep it in production everywhere **except** international card-not-present transactions over $500, which revert to the old decision logic.

**Evidence for the carve-out:**

- False-decline rate ~6× higher in that segment: ~11.8% vs 1.9%.
- Fraud catch essentially unchanged at 70–75%.
- Significant at p ≈ 0.0002.
- Corroborated independently by support tickets going from zero to nine false-decline complaints.

**Second example, healthcare task (0.53).** Same shape: keep the call program for home discharges; redirect it to a direct clinical handoff for skilled-nursing discharges where the effect is a genuine null.

**How to build it:**

1. Put the real effect in one segment and make the aggregate ambiguous.
2. Give the model two independent evidence streams for the segment; one stream alone reads as a fishing expedition.
3. Rubric carefully: a scoped answer needs the recommendation criterion to specify both the keep and the carve-out.

---

### Stumping C3: Force the Model to Operationalize a Fuzzy Phrase

**The setup.** Write a decision rule in the prompt that is precise in meaning but requires the model to convert it into an explicit inclusion rule before any computation. The exclusion is what flips the answer.

**Examples:**

| Task | Rule |
|---|---|
| Banking (0.31) | Mid-sized banks that built durable deposit franchises "as entrants or expanders, not from explosive growth from a de novo or other sub-scale start." Operationalize as peers with a meaningful base year; success = flat-to-up deposits per office plus share gain. One metro has three successes; another drops from apparent leader to two once sub-scale starts are excluded. |
| Taxonomy (0.49) | Preserve a pairwise separation only where its direction agrees across all four source-and-tree combinations; pool otherwise. Exactly two pairs fail. The work is applying the rule exhaustively rather than discovering it. |

**How to build it:**

1. State the rule in the prompt in plain language.
2. Ship the data at a grain that makes the rule computable.
3. Ensure the naive read and the rule-following read give different answers.
4. **Pin the rule.** If two careful analysts would operationalize it differently, you have written an underspecified prompt rather than a stump.

---

## Stumping Family D: Change the Arithmetic

**Core idea:** The model does the calculation correctly and still gets the wrong answer, because one input is wrong.

### Stumping D1: A Single Buried Line Item

**The setup.** The bakery task (0.38) turns on a $12 surcharge applied to 198 deliveries over 15 miles, stated once on a rate card. Omitting it is the specific error that makes switching to third-party delivery look profitable.

**The math with the surcharge included:**

| Option | Profit |
|---|---|
| Third-party | $26,817 |
| In-house | $27,761 – $28,905 |

In-house wins under every routing baseline.

**Pinning the pricing window.** The rate card defines off-peak as 3pm–11am, and every delivery timestamp falls between 10:00 and 14:59, so in-window pricing is the only licensed reading.

**How to build it:**

1. Make one line item decisive and put it somewhere prose-shaped.
2. Make the correct treatment forced by the data rather than assumed, so a model that guesses cannot accidentally be right.

---

### Stumping D2: The Ranking Inverts When the Unit of Account Changes

**The setup.** The screening task (0.27) ships no blended average fraud cost. The only cost data is a per-case amount column, which forces valuing each missed fraud at its actual amount.

- One model family misses low-value cases averaging ~$90.
- The other misses account-takeover cases averaging $200+.
- The model that misses more frauds by **count** leaks fewer **dollars**: ~$288 vs $420 per thousand orders.

**The shortcut this defeats.** Count-based recall, which is what every fraud dashboard reports, ranks them backwards.

**How to build it:**

1. Deliberately withhold the summary statistic that lets the model shortcut to counts.
2. Shipping a blended average destroys this mechanism entirely, check your file bundle for one before you submit.

---

### Stumping D3: Bound the Upside with a Ceiling

**The setup.** The bakery task's apparent case for switching is a 51.85% capacity gain from moving staff off delivery onto preparation.

- Observed demand: ~730 orders.
- Expanded capacity: ~860.
- The capacity is unreachable. The expansion cannot pay for the fee load even if every unfulfilled order converts.
- Unmet demand in the following month is also lower than the current month, removing the growth argument.

**How to build it:**

1. Let the upside be real and let it be capped by something in the shipped data.
2. Make the recommendation hold even under the most generous assumption about that upside. Stating that the call survives the best case for the alternative is the strongest form of this.

---

### Stumping D4: A Dated Fact That Removes the Rival's Advantage

**The setup.** The screening task ships an October 1 regulatory step-up mandate that collapses BNPL recall to parity across model versions, removing the only genuine advantage the challenger model had during the spring. It also adds a per-order scoring fee that bills on the challenger from the same date.

**Why the window matters:**

| Window | Period |
|---|---|
| Decision window | Q4 |
| Evidence window | Spring |

A model that scores the options on the spring evidence gets the wrong answer even with perfect arithmetic.

> **Handle with care.** This mechanism only works when the dated fact is unambiguously present in the shipped files. A decisive fact that lives outside the shipped data, or that contradicts it, is a recurring batch defect and gets tasks rejected. If your regulatory or policy change is not in the bundle, it does not exist.

---

## Stumping Family E: Rule Out the Rival Story

**Core idea:** Every strong task ships a rival explanation that a smart analyst would reach for, and the data has to rule it out.

### Stumping E1: Timestamp-Level Onset

**The setup.** The e-commerce task deploys the redesign, publishes the broken tag container at 10:47 UTC, and sends the first gift-push email at 16:00 UTC, all on December 14. Growth marketing's story is that the drop is gift-season behavior.

**The kill.** The decline is localized to the 10:47–16:00 window: ~33 carting sessions per thousand requests vs ~52 for the same window pre-deploy, before the campaign starts.

**How to build it:**

1. Co-locate your cause and your confound on the same day, then separate them by hours.
2. Ship data at an hourly grain, daily aggregation makes this unreachable.

---

### Stumping E2: Persistence After the Confound Ends

**The setup.** The same task runs the decline through December 23–31, after the campaign ends on December 22. Seasonality would have released. It did not.

**Why it composes.** Onset before the confound starts, and persistence after it ends, together close the seasonality story from both sides. That task's rubric carries a penalty specifically for attributing the drop to holiday behavior.

---

### Stumping E3: Replicate on an Untouchable Denominator

> The strongest single validation move in the batch.

- The e-commerce task replicates the mobile decline on a home-template request denominator (which the product-detail-page redesign cannot possibly affect) and finds roughly −29%.
- It then bounds the remaining objection, that the redesign changed request patterns, by showing the ratio of product-page to home-page requests moved only 4–8%, and in the direction that would flatter the redesign.

**How to build it:**

1. Ship a second, structurally independent exposure measure.
2. This is also the highest-value rubric criterion you can write, because it separates a model that found the answer from one that guessed it.

---

### Stumping E4: Ship the Falsifiable Alternatives Explicitly

**The setup.** The fraud-model task ships three competing explanations, all plausible, all independently falsifiable:

1. The label-lag artifact.
2. A documented feature outage confined to March 1–14 that was already patched.
3. A new high-fraud merchant category that launched on the cutover date.

Each fails against a specific timestamp or window in the files.

**Rubric coupling.** The rubric awards points for ruling out each one by name. A model that reaches the right answer without ruling out the alternatives has not done the work, and the rubric should be able to tell.

**How to build it:**

1. For every strong task, write down the three explanations a good analyst would reach for first.
2. Ship the evidence that kills each.
3. Make the rejection of each a separate rubric criterion.

---

# Older Task Feedbacks

Lessons from **premium-member product spotlight** (task `0e870b13-1dd8-451e-951a-2a7545e34e13`). Traps reproduced as designed; task failed review because the **decision was not pinned** in shipped files.

## What worked (trap design aligned with this guide)

| Technique | What we built |
|-----------|---------------|
| Family D/E traps (joins, encoding, nested docs) | Tier encoding, JSON catalog, clickstream inflation, purchase ledger |
| Family F, wrong metric (F1) | Manifest pushes conversion + flat CSV |
| Stumping B4, version-of-record | Stale `products.csv` vs authoritative JSON |
| Stumping D2, ranking inverts by unit | Wilson wins units; Apple wins tx/buyers/views; Instant Pot wins revenue |

Reviewer confirmed all five traps reproduce and partial pipelines self-validate on Apple at 8 units.

## What we missed (and why review failed)

### Stumping C3: Pin the rule

> *If two careful analysts would operationalize it differently, you have written an underspecified prompt rather than a stump.*

We left “genuinely winning” fuzzy in the prompt and chose units, ≥30 browsers, and positive net cart **implicitly** in the author solution, not in anything the solver receives. Naive read and rule-following read gave different answers (Apple vs Wilson) with **no shipped document** stating which rule wins.

**Fix:** Ship a marketing campaign brief in the export: cohort, eligibility gates, rank by units (tie-break transactions). Keep the one-line prompt; the brief carries the pin.

### Stumping B3: Hard constraints in prose

> *Bury eliminating constraints in documents the model has to actually read.*

We should have shipped that brief **from day one**. The only written metric guidance was `export_manifest.json`, which steered toward the wrong metric and wrong catalog, so a careful solver obeying the only authority lost Wilson entirely.

### Stumping D2: Built the inversion, didn’t close it

D2: if count vs dollars (here units vs transactions vs revenue) inverts the ranking, **pin the unit of account**. We created the inversion on purpose but never named **units** in-fiction, three defensible answers after perfect cleaning (Wilson / Apple / Instant Pot), i.e. a lottery not a stump.

### Decisive facts must live in shipped files (D4 spirit)

Critical components cited internal `clean/`, `answer_key.json`, and author-only baselines. Per this guide: if it is not in the bundle, it does not exist for the grader. Rubric facts must come from `data.zip` only.

### Generation tells (finish work)

- Review boilerplate repeated verbatim across hundreds of rows.
- Product names as category mashups (e.g. “Instant Pot Microfiber Kitchenware”).
- Manifest dated before the data window it describes.

Cosmetic, but undermines realism; fix at generation or build-time polish.

## Action items from that review

| Feedback | Fix |
|----------|-----|
| Decision not pinned | Campaign brief in export: ≥30 browsers, positive net cart, rank by units |
| Determinism overclaimed | Solution cites brief as authority; prompt sets question only |
| Internal artifact refs | Critical components describe shipped export only |
| Wrong interaction count | Report raw row count and semantic-dedupe count from export |
| Review / name / manifest polish | Vary review text; coherent names; manifest date after data window |

## One-line lesson

We followed this guide for **how to break naive pipelines** (Stumping A/B/D, trap catalog) but not for **how to pin the winning rule in shipped prose** (C3 + B3 + D2). Trap density without a pinned decision rule produces a failed task even when every trap fires correctly.

