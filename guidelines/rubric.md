# The Rubric

> ## OPERATIVE as of 2026-09-05, supersedes the 2026-08-27 block below
>
> The rubric is generated for you and fixed. You do not write it and you do not edit it. It is
> generated internally from three things you already produced (the prompt contract, the golden
> solution, and the requested output files) and it must reach **25 or more criteria** before the
> task can move on.
>
> **What changed on 2026-09-05 is how you get there.** A task now ships **one to three
> deliverables** with **uncapped, multi-dimensional asks**, which is a small, honest prompt, so
> the old route to 25 (three or more files carrying three or more asks each) is closed. The
> criteria now come from the **structure of the answer**, which has a name: the **prompt shape**.
> A ranked list under a cap grades every candidate's score. A forecast across many periods grades
> every period. A grid grades every cell. A bridge grades every reconciling item. Eighteen shapes
> with 72 worked prompts are documented in
> `../.claude/skills/guide-to-prompt/references/shapes/`, and the picker there carries the
> criteria arithmetic. **Never stack simple asks to reach 25.**
>
> **The weights moved:** 30 to 40 per cent on the recommendation and its critical components, 5 to
> 10 per cent on instruction-following, about **55 per cent** on the asks.
>
> **The bar moved:** a task passes when the **top two responses average under 70 per cent** against
> the generated rubric **and at least one response is genuinely stumped**, well below the bar. The
> threshold moved from 50 to 70; the top-two structure never went away, and the two conditions are
> conjunctive. **Build to 60**, because the on-platform verifiers are not perfectly accurate and the
> task is regraded more accurately after submission.

> ## OPERATIVE as of 2026-08-27, SUPERSEDED by the block above, retained for reference
>
> The rubric is generated for you and fixed. You do not write it and you do not edit it. It is
> generated internally from three things you already produced (the prompt contract, the golden
> solution, and the requested output files) and it must reach **25 or more criteria** before the
> task can move on. Your job is to build a prompt, a golden and an evidence package strong enough
> that the generated rubric is wide and hard for a model to satisfy.

## You no longer review or edit the rubric

There is no review pass anymore. The old flow, where you opened the rubric and fixed genuine
problems, is retired. The rubric is produced for you and stays as generated. If it looks wrong,
the fix is upstream: correct the prompt contract or the golden output, and the rubric is
regenerated from the corrected pieces.

## The 25-criteria floor

A task whose generated rubric lands under 25 criteria does not move forward. Breadth is what
forces a model to be right across the whole task, not just on the headline call, so the surface
has to be wide. The way to clear 25, as of 2026-09-05, is the **prompt shape**: one repeated
structural unit (a candidate, a period, a bucket, a cell, a target field, an indicator), stated
for every instance, optionally with a second figure on each instance, plus the decision furniture.
Ten to twenty units carries most of the count on its own. Never padding, and never a longer list
of simple asks.

## Weighting

The score splits into three blocks, totalling 100 percent.

| Share | Block | What it covers |
|---|---|---|
| 30 to 40% | Recommendation and critical components | The deterministic call and the load-bearing components it rests on, split across three or more criteria with none over 20 percent of the total |
| 5 to 10% | Instruction-following | The requested files and their output shape: file present and named, one row per period, a required total row, a named column set, ordering, page length, printing the required figures. Unit and rounding ride inside the value they belong to, never a criterion of their own |
| ~55% | Supplementary questions and asks | The largest block by far, so the asks must be hard and discriminating rather than trivial lookups: a wrong analytical path should get them wrong |

**The ranges do not compose freely.** The three blocks sum to 100, so you cannot take every range
at its top: 40 plus 10 plus 55 is 105 and no rubric looks like that. When you need planning numbers
before the rubric exists, use a set that closes (38, 7, 55 is the working default), and treat the
**generated rubric as ground truth** for the real split the moment it arrives.

Because supplementary is the largest block, the asks carry most of the difficulty. A question a
model can answer with a surface lookup does not belong in it.

## The bar the rubric enforces

A task passes when the **top two responses average under 70 percent** against the generated rubric
**and at least one response is genuinely stumped**, well below the bar. The threshold moved from 50
to 70 on 2026-09-05; the **top-two structure never went away**, so the rubric still has to hold
against the single strongest solver in the room.

**Build to 60.** The client's instruction and their reason: the on-platform verifiers are not
perfectly accurate and the task is **regraded more accurately after submission**, so a build
measuring 68 can regrade past the bar after work has stopped.

Read the other half too. The *all-models* stump stays retired, so you do not need every response to
fail, but **one genuine stump is a pass condition again**, which it was not between 2026-08-27 and
2026-09-05.

Difficulty still matters and the same honest-data shapes still carry it (forecasting, method
selection, a binding constraint, a decomposition, a confirm-the-number, a hold); the planted
defect and the flip-the-wrong-number trap stay retired.

## Getting to 25: first the shape, then the five levers

**Pick the prompt shape first.** As of 2026-09-05 that is where the criteria come from, and the
five levers below put genuine material behind it rather than substituting for it. Size the shape
on paper before a file is generated: one repeated structural unit, times how often it repeats,
plus the decision furniture. Under 25 means a **denser structure**, more units or a second figure
on each unit, never more asks bolted on the side. The eighteen documented shapes and their
arithmetic are in `../.claude/skills/guide-to-prompt/references/shapes/`.

These five are what moved the worked examples from the low twenties past 25, and they are about
genuine material rather than padding.

1. **Build in three different findings, not one restated.** The top reason a prompt stalls near
   20 is that every ask re-expresses the same result: a median, a p90 and a top-tier share are
   all the same distribution finding. Make the task turn on distinct facts, a headline number, a
   driver, a threshold, a trend, because each independent fact a wrong path could miss is its own
   criterion.
2. **Ask for one criteria-dense visual, and name its parts.** "Include a chart" is worth one
   point. A visual is worth six or seven when you name what it must contain: the chart type, each
   series or panel, a labeled reference or threshold line with its value, an annotation on the
   key point, an ordering, and a title that states the finding.
3. **Add a second decision axis.** A recommendation that rests on one number is thin. Force the
   decision to weigh two things, the effect and its cost, the growth and the retention, the
   forecast and the capacity limit, because the trade-off adds the second value, its comparison,
   and the reconciliation between the two.
4. **State the repeated unit for every instance, in one ask.** This is the multi-dimensional ask
   the 2026-09-05 spec is asking for and it is where the bulk of the criteria live. "One row per
   segment (or period, or cohort) with these measures" multiplies criteria: each measure over each
   grouping is its own answer. Name the grain outright, name the columns, and ask for an ordering
   or a total row, in groupings where the values genuinely differ and matter. Note that this is
   **one** ask, not many, and that a solver holding the wrong structure loses all of it at once,
   which is what makes it discriminating rather than merely wide.
5. **Demand a robustness or validity check.** A backtest error against a naive baseline, a
   placebo or pre-trend check, a confidence interval or p-value, a sensitivity or leave-one-out
   result, or a cross-file reconciliation. These are the criteria that separate a rich task from
   a shallow one.

One rule underneath all five: every criterion is a distinct, determinate answer a wrong
analytical path would get wrong. Do not pad with rounding or units, and do not count one fact
twice because two files display it.

## What a good criterion evaluates

Criteria grade observable outcomes in the answer, the conclusion reached, the values reported,
the questions answered, the file delivered. They never grade how the analyst thought.

| Topic | Good | Neutral | Bad |
|---|---|---|---|
| Reaching the conclusion | States that mobile web regressed and recommends reverting only that surface, with direction and magnitude consistent with the shipped data | Names the regression but leaves the recommended action implicit | Explains its full chain of thought before answering, showing every intermediate calculation |
| Method | Reaches a result the shipped files support, by any defensible route | Mentions a method without tying it to a result | Requires a two-proportion z-test on the deduplicated holdout specifically |
| Numbers | Reports the corrected lift with correct sign, unit and rounding, allowing equivalent representations and reasonable tolerance | Reports the right value with a missing unit | Requires the exact string "+0.62pp, z = 2.45" |

Numeric questions can still require the correct value, unit, rounding and conclusion. The
criterion is written so equivalent representations pass: 0.62 percentage points, +0.62pp, and
"roughly six tenths of a point in favour of treatment" are the same answer, and reasonable
calculation tolerance is allowed rather than string matching.

**Never reward disclosure.** A criterion that awards points for showing work, naming a method, or
narrating steps rewards verbosity instead of correctness. If a step genuinely matters, the result
it produced is graded, not the fact that it was mentioned.

## What the generated rubric guarantees

The generated rubric is built to satisfy every row below. You do not tune these by hand; you make
them true upstream, in the prompt and the golden.

- [ ] The rubric holds 25 or more criteria, reached through the prompt shape rather than through a long list of asks
- [ ] The deterministic recommendation and its critical components carry 30 to 40 percent, spread across 3 or more criteria
- [ ] No single criterion is worth more than 20 percent
- [ ] Instruction-following covers the requested files and output-shape asks at 5 to 10 percent
- [ ] The supplementary block is about 55 percent and every question in it is hard, discriminating and multi-dimensional rather than a stacked lookup
- [ ] Every requested ask is covered exactly once, with no two criteria overlapping or contradicting
- [ ] The golden output satisfies every positive criterion
- [ ] Nothing rewards methodology disclosure or chain-of-thought
- [ ] Weights sum to 100 percent, and the block ranges were not each taken at their top
