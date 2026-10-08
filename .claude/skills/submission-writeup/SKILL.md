---
name: submission-writeup
description: Draft or revise submission.md, the Project Mark submission write-up, and every golden deliverable that ships with it. Invoke whenever a submission.md is being written, rewritten, extended or reviewed for a task folder, including when the request just says "write the submission", "draft the write-up", "do the submission for taskNN", or when a review says a block is thin. Carries the five blocks in order (tags, final recommendation, critical components, a step-by-step solution of at most eight one-line steps, and deliverable answers stated as bare answers grouped by file), the concision rule that keeps the write-up from failing the in-task determinism grader (every figure written is a claim the grader recomputes, so the write-up states the answer and a reproducible path and nothing else), and the golden deliverable rules for the one-to-three-file set. There is no deliverable format rationale, justification or golden solution block.
---

# Writing the Submission

> The write-up is the answer key, and the rubric is **generated from it and fixed**: it is produced from the prompt contract, the golden solution and the requested files, you do not write or edit it, and it must reach **25 or more criteria** before the task can advance. Each critical component and each step-by-step result typically becomes a positive criterion, the asks fill the largest block (about 55 to 60 percent of the score), and if the rubric looks wrong the fix is upstream, in the prompt or the golden, never in the rubric. Write the blocks after you have actually done the analysis, never from intuition. Full rubric spec: `guidelines/rubric.md`.
>
> **The golden is one to three files, three being the ceiling**, and the 25 criteria come from the **prompt shape** rather than from a long list of asks. The deliverable answers block therefore holds fewer, wider answers: one multi-dimensional ask can owe thirty determinate figures, and every one of them is graded, so the block states them all rather than summarising the ask.

## Short is the standard

The in-task grader reads the final recommendation, the critical components, the steps and every
deliverable answer, and it recomputes every figure in them from the shipped files (the "reproduce,
do not assume" rule in `guidelines/determinism_judge_system_prompt.md`). Every extra figure,
sub-count, convention clause or aside is one more claim it has to reproduce, and one more place it
can find a second reading, a rounding that does not match, or a file the pack does not carry, so a
long write-up fails determinism even when the answer is right. The write-up states the answer and a
path someone can rerun, and stops there.

Two rules carry it, and they govern every block below:

- **Cut words and incidental figures, never owed figures.** A figure that a critical component or an
  ask owes stays, every one of them, because each is a rubric criterion and the 25-criteria floor is
  fed mostly by the answers block. A figure that only shows working (a sub-count, a denominator, a
  rival's intermediate, a rate on the way to the rate) goes. Concise means fewer words around the
  answers, never fewer answers: a ranked list of six still gets six points.
- **Reproducible, not low-level.** The steps say which file and which rule produce each result, so
  someone can rerun it. They do not walk the arithmetic, restate the data dictionary or narrate the
  cleaning. A convention that needs a paragraph to defend belongs pinned in a shipped file, and the
  step cites that file in a few words.

**Not written:** a Deliverable Format Rationale, a Justification, a Golden Solution listing, a Key
Assumptions block or a Determinism block. The author does not use them, the grader is never given a
justification (it assesses forcedness itself), and every sentence they would carry is more surface to
fail on. Do not copy one in from an older `submission.md` or from `guidelines/`. The golden files
themselves ship, under the rules in **Golden deliverables** below.

**Format: one file, `submission.md`.** The golden solution ships alongside it as **every file the
prompt named**, in the requested formats.

**Prerequisite.** The analysis is finished, every golden deliverable is built and consistent with the
others, and every figure reproduces from the shipped bundle. If a number in the write-up cannot be
recomputed from `target/`, it does not exist, and the determinism review will find it.

**Run this last.** The order is: build, `determinism-check`, then this skill, then `golden-realism`.
Writing the submission before the determinism pass means rewriting it after.

---

## The blocks, in order

| # | Block | Length | What it is for |
|---|---|---|---|
| 0 | Tags | 2 to 3 lines | Domain and analytical objective, so the task is filed correctly |
| 1 | Final Recommendation | 1 sentence, the deciding figure, 1 clause per rival | The single committed call |
| 2 | Critical Components | 2 to 5, one line each | The rubric's backbone |
| 3 | Step-by-Step Solution | at most 8 one-liners | Raw data to recommendation, reproducible |
| 4 | Deliverable Answers | grouped by file, answer lines only | Every figure each ask owes, written as points |

Nothing else goes in the file.

## 0. Tags

Two lines under the title, naming the Axis 0 domain and the Axis 1 analytical objective from the
canonical taxonomy in the `guide-to-prompt` skill. The objective must be one of the **eight**
labels; any other tag gets the task rejected on the tag alone. Add the Axis 2
reasoning phases if the task folder tracks them. Use the exact taxonomy wording, not a paraphrase.

> **Domain:** Economics, prices and inflation (cost of living, place to place price comparison,
> inflation decomposition).
> **Analytical objective:** Forecasting and predictive modelling (cross-domain prediction from settled outcomes).

The heading is `## Tags`, unnumbered, and the numbering starts at `## 1. Final Recommendation`. No
scenario recap.

## 1. Final Recommendation

The call in one sentence, with no conditions and no "subject to". It does not have to be binary, as
long as ten domain experts would land on it. A **hold** is stated as a call in the same shape ("We
should fund none of the three programs this cycle"), with the blocking quantity named in block 2.

Then one line with the deciding figure and the margin over the runner-up, then the rivals, one clause
each: what the rival leads on and the one reason it loses. No paragraph per rival, and no figure here
that blocks 2 to 4 do not already carry.

> **We should not acquire Data Corporation at the asking price.**
>
> The price is 20x normalized EBITDA against the 12x mandate ceiling. Not the reported revenue case,
> which counts one-time and related-party sales. Not the trailing margin, which defers R&D.

## 2. Critical Components

The load-bearing intermediate results that **every possible methodology must calculate** to reach the
recommendation. Strictly 2 to 5, one line each, the figure in bold at the rounding used everywhere
else it appears, no explanatory clause.

> 1. Recurring revenue is **$38M**
> 2. The top 2 customers are **61%** of recurring revenue
> 3. Normalized EBITDA margin is **13%**
> 4. The asking price is **20x** normalized EBITDA

**The test that cuts the list down:** if a defensible method could skip this step and still land the
correct call, it is not critical. A component only one route computes fails solvers who took another
valid route. Cover the main recommendation only.

## 3. Step-by-Step Solution

**At most eight steps, one line each, the last one being the recommendation.** Each line is the method,
the shipped file or rule it uses, and the one result it produced. Fewer than eight is fine; never pad
to eight and never cram two steps into one line to fit.

> 1. Joined the six files on `customer_id`, padding the leading zeros the CRM export drops.
> 2. Removed one-time and related-party sales per the revenue policy: recurring revenue is $38M.
> 3. Summed recurring revenue by customer in the billing export: the top 2 are 61% of it.
> 4. Restored deferred R&D from the ledger: normalized EBITDA margin is 13%.
> 5. Divided the asking price in the term sheet by normalized EBITDA: 20x, above the mandate's 12x ceiling.
> 6. Recommendation: do not acquire at the asking price.

What keeps a line to one line:

- **One sentence, no sub-bullets.** A step that needs a second sentence is either two steps or carrying
  a figure nobody needs.
- **Carry only the result the next step uses or the call rests on.** The grader recomputes every
  pivotal number in a step, so rows dropped, denominators, every candidate's value on the way and
  per-component cost build-ups stay out. If an ask owes them, they live in block 4, once.
- **Cite where a convention is pinned, do not restate it.** "Per the revenue policy" or "as the data
  dictionary defines a start" is enough. A convention a competent analyst could reasonably reverse is
  an unpinned fork, and the fix is pinning it in a shipped file, not explaining it here.
- **Name only files the pack ships, by their names in the pack.** A step that relies on a file the
  pack does not carry fails the grader as missing input data.
- **End in a figure or a finding, never an intention.** "Analyzed the cohort data" is not a step.
  "Day-30 retention is 41%, not the 47% the deck reports" is.

## 4. Deliverable Answers

Grouped by file, in the prompt's order of files and of asks inside each file. **These are graded at the
same bar as the main recommendation**: each must reproduce from the shipped files and be uniquely
forced, and one wrong or two-way-defensible answer fails the gate as if the main call had that flaw.

**Answer lines only.** The answer in the exact unit and rounding the prompt asked for, and nothing
else: no Basis line, no restating the ask, no reasoning, no method. "4.7 percentage points",
"$1,842,900", "yes", or the named candidate.

```
## 4. Deliverable Answers

### <first_file.ext>
1. <answer, in the exact unit and rounding the prompt specified>
2. <answer>

### <second_file.ext>
1. <answer>
2. <answer>
```

**Concise is not summarised.** An ask that owes a row-set or many figures gets every one of them, one
point per row, every column value named inside the point, in the deliverable's own order. Each point is
one separately gradable claim, and dropping them shrinks the rubric toward the 25 floor. Keep it to one
level of points under the numbered item.

> 1. Transfers, 42 rows in the file's order, whole units:
>    - Store 118: send 340 to store 204, 1,120 on hand now, 780 after
>    - Store 204: receive 340 from store 118, 260 on hand now, 600 after

**Never a markdown table here.** A name with a pipe in it shifts every column, a wide table wraps into
noise, and a weirdly formatted table is a named LLM tell. The deliverable itself keeps whatever tables
its genre calls for.

**A content requirement** ("include a chart of X with the runner-up highlighted") gets one line saying
what the deliverable contains and where:

> 2. Bar chart of margin by category on page 2 of the memo, percent to one decimal, runner-up highlighted.

**Answers agree across deliverables.** A figure quoted in two files carries the same rounding in both
and in this block. Compute it once in the code deliverable and carry it.

---

## Golden deliverables (ship alongside, not written into submission.md)

**Every file the prompt named, in its requested format.** That is **one to three deliverables**, three
being the ceiling, with no format family assigned and a visual wherever one makes
the decision read at a glance. A four-file golden is a spec failure on the count alone, and a standalone
table the memo should have carried is a slot spent badly. Between them the files answer every ask and
the main recommendation, and they satisfy every positive criterion the generated rubric will carry; if
they would not, the fix is in the prompt or the golden, because the rubric is regenerated from them.

- **Business-realistic is a gate.** The client sends back goldens that read as LLM-generated **even when
  every figure recomputes**. Once the figures are correct and asserted, run every golden through the
  **`golden-realism`** skill.
- **The main recommendation is unmissable.** A reader should not have to infer it from output.
- **The code deliverable prints the figures the critical components name**, not only the final answer.
- **Prefer artifacts the code produces.** A chart from a plotting library, a workbook the script writes,
  a conformed CSV the pipeline emits: these recompute and cannot read as generated text. Where a text
  deliverable needs a chart, the chart still comes from the script.
- **Consistency across the set is graded.** Every shared figure agrees, to the same rounding, in every
  file that carries it and in block 4.

---

## What gets a write-up rejected

**It must not look LLM-generated.** This is a rejection cause, not a style preference.

- **No em dashes.** Use a comma, or parentheses for an aside.
- No weirdly formatted tables, no oceans of white space, no headers beyond the five blocks and the
  per-file headings in block 4.
- No corporate filler: *leverage, robust, seamless, comprehensive, it is worth noting that*.
- No hedging anywhere near the recommendation. The point is a committed call.
- Plain English, with the domain terms that actually carry meaning left in.

**Other rejection causes:**

- A figure that does not recompute from the shipped bundle, wherever it sits in the file.
- A write-up padded with working. Every incidental figure is a claim the grader recomputes, and one
  that does not reproduce fails the task even when the answer is right.
- Critical components that a valid alternative method would never compute.
- A convention call a competent analyst could reasonably reverse, which is an unpinned fork.
- A recommendation stated with conditions attached.

## Checklist

- [ ] `submission.md` holds exactly the five blocks: Tags, Final Recommendation, Critical Components, Step-by-Step Solution, Deliverable Answers
- [ ] No Deliverable Format Rationale, Justification, Golden Solution, Key Assumptions or Determinism block
- [ ] Tags name the Axis 0 domain and the Axis 1 objective in the taxonomy's own wording
- [ ] Block 1 is one committed sentence, the deciding figure, one clause per rival, and no figure blocks 2 to 4 do not carry
- [ ] Block 2 has 2 to 5 one-line components, each one every methodology must calculate
- [ ] Block 3 has at most 8 steps, each one sentence ending in a figure or finding, naming only shipped files, the last being the recommendation
- [ ] Block 4 covers every ask under every deliverable, in the prompt's order, answer lines only with no Basis line, in the exact stated unit and rounding
- [ ] Every figure an ask owes is stated, one point per row or figure, never summarised and never in a table
- [ ] No incidental figure anywhere: each number in the file is owed by a component, an ask or the call
- [ ] Every figure shared between deliverables and block 4 agrees, to the same rounding
- [ ] The deliverable set is one to three files, a visual where it helps, any chart rendered by the code, and the code prints the critical components' figures
- [ ] Every golden run through `golden-realism` after its figures were frozen, and the bundle verifier green afterwards
- [ ] Every number in every block recomputes from `target/`
- [ ] No em dashes anywhere; read it once more for LLM tells before filing
