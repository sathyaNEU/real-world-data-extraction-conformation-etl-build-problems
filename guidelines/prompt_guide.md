# Writing the Prompt

> ## VOICE AND STRUCTURE UPDATE (2026-09-08), OPERATIVE, sits on top of the 2026-09-05 block below
>
> Client note, verbatim: *"Right now the majority of prompts are following the same exact voice and
> structure. 'I'm a X working at Y. Here's some context. Give me this main recommendation and here
> are the two deliverables that I need from me.' Let's try to switch it up and make every prompt
> feel different."* The note pointed at additional examples of varied prompt formats at
> `project-mark.learn.joinhandshake.com/taxonomy`, which is behind the Handshake login and is not
> mirrored here. The 72 worked prompts already imported into
> `.claude/skills/guide-to-prompt/references/shapes/` are the same client material and already show
> the variation the note is asking for.
>
> **Nothing in the 2026-09-05 contract below is retracted.** Prose, first person, one committed
> call, one to three deliverables, uncapped multi-dimensional asks, unit and rounding inside the
> sentence. What is retired is the **skeleton** in the block below, the one that prescribes context
> in two or three sentences and then one paragraph per deliverable in a fixed order. That skeleton
> is what produced the monoculture: across task66 to task83, 17 of 18 prompts opened in first
> person with a role verb in clause one, 12 with the literal words "I run", 18 of 18 shipped a PDF,
> and 16 of 18 shipped three files where three is the ceiling.
>
> **The working standard is the skill, as always.** `.claude/skills/guide-to-prompt/` carries the
> rewritten prescriptions, `references/prompt-voice.md` carries the twelve opening moves, the
> requirement-against-carrier table and the structural axes, and `references/voice-check.py` is the
> per-build and per-batch check. Read those rather than the skeleton below.

> ## FORMAT UPDATE (2026-09-05), OPERATIVE ON EVERYTHING EXCEPT THE SKELETON, supersedes the 2026-08-27 block below
>
> The prompt is now **prose**, first person, the way you would write to a colleague:
>
> ```
> [Context]        first person, two or three sentences: your role, the forcing event, the
>                  standard the call runs on, ending on the one call you owe
> [Deliverable 1]  one paragraph: the file and its format, then what it has to carry, run
>                  together as prose, with each figure's unit and rounding inside the sentence
> [Deliverable 2]  the same, and stop at three files
> ```
>
> - **One to three deliverables, and three is a ceiling.** This reversed: three was the floor on
> 2026-08-27 and is now the maximum, so a four-file build is a spec failure. **No format family
> is assigned.** The four families (Data: CSV, TSV, JSON, XLSX, Parquet · Visual: PPTX, PNG, SVG,
> HTML, JPG · Text: PDF, DOCX · Code: PY, IPYNB, SQL, R) still describe what a file is for, but
> nothing requires the set to span two of them. Pick the files a real analyst would actually
> produce for this decision, and be honest about it: `analysis_report.pdf` is not the best-suited
> deliverable for every task.
> - **Prioritize a visual where it genuinely helps.** Not mandatory, but a chart, a waterfall, a
> matrix, a heatmap or a table is what a stakeholder reads first, and a criteria-dense visual with
> its parts named is worth five to seven criteria where "include a chart" is worth one. The table
> does not have to be a standalone file: it can live inside a memo, inside a workbook, or be
> printed by a script.
> - **The asks are uncapped and untargeted, and each has to be multi-dimensional and hard.** The
> three-per-file floor is retired. One ask can span many rows, periods or cuts and still resolve
> to one defensible answer, and that is the ask you want. Unit and rounding survive, stated
> **inside the sentence** rather than in a bullet, and "one gradable thing per bullet" is replaced
> by: every figure inside an ask is separately gradable and separately determinate.
> - **The 25-criteria floor is unchanged, and the route to it changed.** A one-to-three file prompt
> is a small surface, so the criteria come from the **structure of the answer**, which has a name:
> the prompt shape. Eighteen shapes are documented with 72 worked prompts in
> `../.claude/skills/guide-to-prompt/references/shapes/`, each with where its criteria come from
> and how to size it past 25. **Never stack simple asks to reach 25.** That is the failure this
> update is aimed at.
> - **The bar is the top two responses averaging under 70 per cent, with at least one model
> genuinely stumped**, and the two conditions are conjunctive. The threshold moved from 50 to 70;
> the top-two structure never went away, so a prompt still has to hold against the single strongest
> solver. **Build to 60**, because the on-platform verifiers are not perfectly accurate and the task
> is regraded more accurately after submission. Weights: 30 to 40 per cent recommendation, 5 to 10
> instruction-following, about 55 on the asks.
> - **The golden deliverables must look business-realistic**, which is now a stated send-back cause.
> `../.claude/skills/golden-realism/` carries the per-format passes.
> - **First person is back and the persona ban of 2026-08-24 is retired.** All 72 worked prompts
> open with a role clause. What still costs you is the **roll call** of colleagues' opinions,
> because it hands the solver the ladder as a refutation checklist, which is a design defect rather
> than a style one.
>
> The input gates, the six domains and the six objectives are unchanged. The client's 2026-09-05
> example page offers a seventh objective filter, "Opportunity Sizing & Decision Support", and tags
> two examples "Comparative analysis and explanation"; **neither is a valid Axis 1 tag here**.
>
> Full guidance: `.claude/skills/guide-to-prompt/SKILL.md`. Shapes: that skill's
> `references/shapes/`. Rubric spec: `rubric.md`.

> ## FORMAT UPDATE (2026-08-27), SUPERSEDED by the 2026-09-05 block above, retained for reference
>
> Four things changed on 2026-08-27, and all four are gate-level.
>
> ```
> [Context] two to four neutral sentences: the situation, the forcing event
> [Main Recommendation Ask] one committed call, the anchor of the whole task
> [Deliverable 1] file.ext (Family) one natural sentence requesting it
> - ask (unit and rounding stated)
> - ask
> - ask
> [Deliverable 2] file.ext (Family) one natural sentence requesting it
> - ask
> - ask
> - ask
> [Deliverable 3] file.ext (Family) one natural sentence requesting it
> - ask
> - ask
> - ask
> ```
>
> - **Three or more deliverables, with no upper limit.** The two-deliverable default is retired.
> - **Two format families are assigned per task**, and the deliverable set must span both of
> them. You can always add more files, in any family. The four families: Data (CSV, TSV, JSON,
> XLSX, Parquet) · Visual (PPTX, PNG, SVG, HTML, JPG) · Text (PDF, DOCX) · Code (PY, IPYNB,
> SQL, R). The listed formats are examples, not a fixed menu; the rule is variety across
> families.
> - **Each named file carries at least three asks**, each either a supplementary question with a
> determinate answer or a concrete requirement about what the file must contain. Every ask
> still states its unit and rounding and carries one gradable thing. The prompt's main bullets
> are the file requests, and one deterministic recommendation still anchors everything.
> - **The rubric is generated for you and must reach 25 or more criteria.** You no longer write
> or edit it; it is generated from the prompt, the golden and the requested files, and a task
> whose rubric lands under 25 criteria does not move forward. About 60 percent of the score
> sits on the asks, so they must be hard and discriminating rather than trivial lookups: a
> wrong analytical path should get them wrong. The full rubric spec is in `rubric.md`.
> - **The bar is no longer "stump the model".** A task passes when the top two of twelve model
> responses average under 50 percent against the generated rubric. The bottom ten are
> submitted without checking. Difficulty still matters and the same honest-data shapes still
> carry it; what changed is that breadth across the asks now does real work, because a solver
> that lands the main call but misses the hard asks still scores under the bar.
>
> Five levers move a prompt from the low twenties past 25 criteria, and they are about genuine
> material, never padding: build in three different findings rather than one restated; ask for
> one criteria-dense visual and name its parts (chart type, each series, a labeled threshold
> line with its value, an annotation, an ordering, a title that states the finding); add a
> second decision axis so the call weighs two things; require a breakdown with the grain, the
> columns and an ordering or total row named outright; and demand a robustness or validity
> check (a backtest against a naive baseline, a placebo, an interval, a sensitivity, a
> cross-file reconciliation). One rule underneath all five: every criterion is a distinct,
> determinate answer a wrong analytical path would get wrong, so never pad with rounding or
> units and never count one fact twice because two files display it.
>
> Everything else in the 2026-08-19 block stands: the families crossing rule (now over the two
> assigned families), unit and rounding on every ask, the single `.py` rule stays retired,
> prefer artifacts a script produces, and the asks replace the old standalone
> related-questions block.
>
> Full guidance: `.claude/skills/guide-to-prompt/SKILL.md`. Rubric spec: `rubric.md`.

> ## FORMAT UPDATE (2026-08-19), superseded by the 2026-08-27 block above, retained for reference
>
> The prompt is a short stakeholder context, one committed recommendation ask, then a bullet list of
> deliverables with their file types, and under each deliverable at least two specific asks.
>
> ```
> [Context] short, first person, one stakeholder, the forcing event
> [Main Recommendation Ask] one committed call, the only part that has to stump
> [Deliverable 1] file.ext (Family) one natural sentence requesting it
> - ask (unit and rounding stated)
> - ask
> [Deliverable 2] file.ext (Family) one natural sentence requesting it
> - ask
> - ask
> ```
>
> - **Two deliverables is the standing default.** The spec allows two to five and the count is
> assigned per task.
> - **The set crosses at least two data families.** Data: CSV, JSON, XLSX, Parquet · Visual: PPTX,
> PNG, HTML, JPG · Text: PDF, DOCX only · Code: PY, IPYNB, SQL, R.
> - **Each deliverable carries two or more asks**, each either a supplementary question or a
> specific requirement about what the file must contain. **These asks replace the old standalone
> numbered related-questions block**, which no longer exists.
> - **Every ask states its unit and its rounding**, and carries one gradable thing.
> - **The single `.py` deliverable rule is retired.** A `.py` is still welcome and can no longer be
> the only one. Prefer at least one artifact a script produces (a rendered chart, a written
> workbook, a conformed CSV), because a generated artifact cannot read as LLM-written text.
> - **Only the Main Recommendation Ask has to stump.** The other asks must be deterministic, correct
> and genuinely difficult; blatantly easy asks get the task rejected.
>
> Full guidance, with two worked prompts in the format: `.claude/skills/guide-to-prompt/SKILL.md`.
> Trap and prompt hygiene rules: `.claude/skills/stumping/SKILL.md` Part 7.

The prompt is where task difficulty lives. Two properties are non-negotiable: the prompt must be intentionally vague about method, and the task must resolve into a single deterministic recommendation with one committed conclusion that 10 independent domain experts would agree on.

> **"Not enough information to make a decision" is an acceptable final answer.** If the task lands there, license the non-pick as one option among the candidates and nothing more: *"name the single intervention to scale, or state that none should be scaled this cycle."* Never ask whether the evidence is sufficient, which is the answer wearing a question mark. The commit demand stays exactly as strict, because hold is one of the committed calls rather than permission to hedge.

> ## Where the canonical example asks live
>
> The taxonomy publishes **eighteen canonical example asks per Axis 1 objective**, 162 in total, mirrored into `.claude/skills/guide-to-prompt/references/` and sliced both by objective and by domain so you load one file instead of the whole corpus. Read the ask anatomy for your objective before drafting.
>
> Every one of those examples is a **Main Recommendation Ask only**. It is the middle of the four-part prompt above, not the whole prompt, so you still add the context, the deliverable request, the numbered related questions, and the golden solution.
>
> They also show how far a real ask goes in naming the tension. Naming the belief a stakeholder already holds, the generic threat to validity, the operating constraint, and the candidate set is fine and is what makes the decoy pressure real. Naming which evidence resolves any of it is not. Say *that* the analyst faces a confound, never *which* file defeats it. One thing several canonical asks do that we do not copy: listing the tables to combine ("by joining the demand file, the rate table and the cost sheet") is method dictation, and a Project Mark prompt names no input file.

## Worked example of the shape

> Q3 profitability fell below plan and management must remove exactly one product category from the
> next buying cycle. Review the attached commercial and operating evidence and recommend the single
> category whose removal produces the strongest defensible improvement in continuing-portfolio
> economics.
>
> Give me a board-ready business report in `category_decision.pdf` that makes the cut and defends it.
> - Name the category to remove and the continuing-portfolio margin change the removal produces, in percentage points to one decimal place.
> - Include a bar chart of continuing-portfolio margin by category, y-axis in percent to one decimal, before and after the cut, with the runner-up highlighted.
>
> Attach the working numbers in `category_scan.csv` so Finance can audit them.
> - One row per category with revenue in whole USD, and direct margin and continuing-portfolio margin as percentages to one decimal place.
> - A final column naming the single evidence-backed change that would make the runner-up the better cut.

Context and Main Ask in two sentences, two named output files crossing the Text and Data families,
two asks under each, a unit and a rounding on every numeric one, and the chart produced by the
analysis rather than described in prose.

## What a Good Prompt Looks Like

A good prompt reads like a short message a busy stakeholder would send: it sets the situation, names the decision to make, and asks for one committed call. Two to four sentences is plenty.

At its core, every prompt is three things:

- **A situation:** the business context or trigger (for example, "Q3 revenue came in below plan").
- **A decision:** the specific call the model must make, which resolves to a single deterministic recommendation.
- **An ask:** a request for one committed answer with reasoning, and no hedge.

### A Good Prompt

- Resolves to a **single deterministic recommendation**, one conclusion that 10 domain experts would agree on. It can be two options, several options, or open-ended, as long as the answer is determinate and gradable.
- Is **intentionally vague on method:** the model must infer the scope, cleaning rules, analysis window, and methodology.
- Leaks neither the method nor the answer, and never names the trap or the file that defuses it.
- Demands a **committed call:** no "it depends," no blended or conditional answer.
- Is **fair:** everything needed to reach the answer is derivable from the uploaded files, with no outside knowledge required.
- Is a **real, useful workplace decision**, not a textbook exercise.

The sections below go deeper on each of these. First, here are examples of good prompts across a few domains.

### Example: M&A

> We're weighing whether to acquire Data Corporation at the asking price. Look at what's attached and give me one call for the board on Friday, buy or walk away, with your reasoning.

- **Resolves to:** a single decision, acquire or walk away.
- **What the model must infer (not stated in the prompt):** which reported figures are inflated, how to normalize revenue and margin, and what multiple the asking price actually implies.

### Example: Healthcare Benefits

> We can fund exactly one care program next year, the diabetes screening benefit or the wellness redesign. Tell me which one to fund. I need a single recommendation I can defend to finance.

- **Resolves to:** a single decision, fund screening or fund the wellness redesign.
- **What the model must infer:** which program's effect is real versus confounded, and that neither option's ROI can actually be proven from the data.

### Example: Churn Models

> We're putting one of two churn models behind next quarter's retention campaign. Which model do we deploy, or neither? Give me one call with your reasoning.

- **Resolves to:** a single decision, Model A, Model B, or neither.
- **What the model must infer:** that the higher-scoring model's edge comes from data leakage, and that a proper time-based evaluation flips the ranking.

---

## Writing Deterministic Prompts

Every Project Mark task has to land on one answer that ten competent analysts would independently reach. The prompt should be vague on method (don't hand over the steps) but the underlying data must force exactly one decision.

A prompt is deterministic when all of these hold:

1. **One committed decision.** It asks for a single gradable call (X not Y, ship or no-ship, fund A or B) with no hedge.
2. **The objective is fixed.** Either the prompt states the goal, or the data makes only one goal sensible. If "which is best" could mean different things (most volume vs. most growth vs. best ROI), name the goal.
3. **No undefined terms.** Every term the decision hinges on (the metric, the time window, any threshold) is defined or supplied by the files. The model never has to guess what you meant.
4. **No arbitrary cutoff.** The answer is not a tunable threshold someone picks by taste. The data draws the line.
5. **The losing option is refuted on the data, not by an assumption.** A capable analyst who argues the other side loses because the files defeat them, not because they missed an unstated premise.
6. **Vague on method, precise on answer.** Withhold the steps and let the model choose its approach, but make sure every valid approach converges on the same call.

### Example: Churn Attribution

> Our monthly churn jumped in Q2 and leadership is split. The growth team blames the April price increase; the product team blames Northstar's competing launch. Everything the analysts pulled is in `/workspace/input/`. Tell me which one is actually driving the churn, and back it with the data. One answer, no hedging.

**Files uploaded:** `subscriptions.csv` (signup and cancel dates, plan, cohort), `price_change_log.csv` (effective date of the increase, by plan), `competitor_timeline.md` (Northstar's launch date), `support_tickets.csv`, `cancellation_reasons.csv`.

**Final recommendation:** the price increase, not the competitor.

**Why it's deterministic:**

- The decision is a clean binary (cause is X not Y), no room for a hedged answer.
- Churn rises only in the plans that received the increase and begins in April, weeks before Northstar's June launch, so chronology rules out the competitor.
- The trap is real (both explanations correlate with the Q2 spike at the aggregate level), but cross-referencing price-change dates and the launch date against cancel dates leaves only one survivor.
- The losing option is defeated on the files, not by an assumption.

### Example: Warehouse Expansion

> We can fund exactly one warehouse expansion next year, and the goal is simple: cut our late-delivery rate for the lowest capital cost. The two candidates are Memphis and Reno. All the data is in `/workspace/input/`. Give me one warehouse to fund, with your reasoning. Do not hedge.

**Files uploaded:** `shipments_2024.csv` (order, origin warehouse, promised vs. actual delivery date), `warehouse_capacity.csv`, `capex_quotes.csv`, `carrier_performance.csv`, `demand_forecast_2025.csv`.

**Final recommendation:** Reno.

**Why it's deterministic:**

- The objective is stated outright (reduce late deliveries per dollar of capex), so there is no "which metric did you mean" ambiguity.
- Memphis has the higher raw count of late deliveries (the naive pick), but `carrier_performance.csv` shows its lateness is driven by a carrier that misses windows regardless of volume, so expansion does not fix it.
- Reno's late deliveries spike exactly when order volume exceeds capacity, which expansion does fix, and at lower capex.
- Once you diagnose the cause of lateness in each, only Reno satisfies the stated objective. A second analyst optimizing the same goal lands in the same place.

### Example: Checkout Experiment

> We ran a four-week test on the new checkout flow and the deck says conversion is up, so the team wants to ship Monday. Before I sign off, look at everything in `/workspace/input/` and tell me ship or no-ship, with the reasoning. I want a straight call.

**Files uploaded:** `experiment_assignments.csv` (user, variant, enrollment date), `conversion_events.csv`, `revenue_by_order.csv`, `weekly_cohort_metrics.csv`, `guardrail_metrics.csv` (refund rate, page latency), `data_quality_notes.md` (flags a checkout-logging bug affecting the treatment arm in weeks 1 to 2).

**Final recommendation:** no-ship.

**Why it's deterministic:**

- The call is binary and the naive read (headline conversion is up) points the wrong way, which is what makes it hard, not ambiguous.
- `data_quality_notes.md` documents a logging bug that double-counted treatment conversions in weeks 1 to 2; drop that window and the lift goes flat.
- `weekly_cohort_metrics.csv` independently shows the effect decaying to zero by week 3 (a novelty effect).
- `guardrail_metrics.csv` shows refunds rising in treatment.
- Each of these alone defeats the ship case, and they all point the same way, so no defensible "ship" argument survives on the data.

---

## Design the Trap First

Difficulty is co-designed across the prompt and the input files. A vague prompt on clean, honest data is still easy: the model reads the files, sees the obvious answer, and wins. Difficulty comes from pairing the ambiguous ask with evidence engineered to mislead: a headline number that points the wrong way, a circular metric, a file that looks joinable but is a different population, a duplicated table that inflates a rate.

Decide what will fool a hasty analyst first, then write a prompt that frames the decision without warning the model about any of it. The prompt should never name the trap, name the file that defuses it, or hint that "one of these metrics is misleading." The catch has to be discoverable, not signposted.

→ Deep dive: Stumping strategies for the catalog of traps.

### Productive Ambiguity

**Productive ambiguity** hides how to solve the task: scope, cleaning rules, analysis window, methodology, what "underperforming" means. The model has to figure out the approach.

**Unfair ambiguity** hides what success is, or requires knowledge that is not in the files. The model should never have to guess what is being asked, and it should never have to reach for outside knowledge. Everything needed to reach the correct answer must be derivable from the uploaded bundle.

### Examples: Good vs. Bad Prompt

#### Good Prompt

> Q3 revenue came in below plan. Should we cut the underperforming product line or double down on it for Q4? Look at the attached data and give me a single call.

- Forces the model to decide **what data is relevant**
- Forces the model to define **what "underperforming" means**
- Resolves into a **single deterministic conclusion:** for example, cut or double down

#### Bad Prompt

> Using the transactions.csv file, join on customer_id, filter to 2024-07-01 through 2024-09-30, compute the delta vs. plan by product line, run a two-sample t-test on the top three lines, and identify the largest contributor to the miss.

- The prompt author has already **solved the problem**
- The model just has to **type the answer**
- No inference, no judgment, no analytical signal

Never give the model the exact steps or expected recommendation. The prompt states the situation and the ask, not the method, the answer, or the decision. If you find yourself writing "then compute X and compare against Y," delete that sentence.

---

## Writing the per-deliverable asks

The Main Recommendation Ask carries the stumping requirement. The deliverable asks do not, but they
still have to be deterministic, correct and difficult, and they are what lets the evaluation reach
more than one kind of evidence. There must be **two or more under each deliverable**, one gradable
thing per bullet, and every numeric one states its unit and its rounding. Blatantly easy asks get
the task rejected.

**Prefer asks a script satisfies:** a chart the deliverable renders, a table it writes, a control
total it prints. Those recompute, they cannot read as generated prose, and the reviewer can rerun
them.

### The three supplementary buckets

**Use at least two of these three buckets** so the evaluation reaches more than one kind of evidence.

- **Supporting / justification.** A direct metric or finding that backs the recommendation. For example: "By what percentage did the selected product's revenue change from FY24 to FY25?"
- **Comparison / related.** How the winner sits against the runner-up. For example: "By how many dollars did its FY27 value exceed the runner-up?"
- **Context / flip.** A related conclusion, including the evidence-backed change that would move the runner-up into first place. For example: "Excluding FY27, which year would have offered the best entry point?"

### What an ask must not do

It must not enumerate the analytical methodology, name the trap, identify the decisive file, or walk the model through the answer path. Avoid asking for every obvious intermediate calculation: handing over the ladder makes the task easier, not more rigorous.

### Structure example

A polished illustration of the shape only. The scenario is fictional and no answer or supporting
data is implied.

> The commission's FY27 continuity review now sits with me after Ostrander's departure. For the
> September board meeting, name exactly one stock for the Emergency Stock Action.
>
> Hand me a runnable `emergency_stock_action.py` that reproduces the call from the shipped files.
> - Print the recommended stock and by how many dollars its FY27 value exceeded the runner-up, to two decimal places.
> - Print the selected stock's price change from FY24 to FY25 as a percent to two decimal places.
>
> Write the one-page `emergency_stock_note.docx` I can put in front of the board.
> - State the recommendation and, excluding FY27, which year would have offered the best opportunity to buy it.
> - Name the evidence-backed change that would cause the runner-up to overtake it, as a numeric threshold in the deciding metric's unit.

One recommendation, two deliverables crossing the Code and Text families, two asks under each across
three buckets, and not a word about how to do the analysis. Every numeric ask states its rounding,
which is required.

---

## Updated Announcement

@channel Some of you may be feeling that the models are becoming more difficult to stump. The strong models have become harder to stump and this means that your current stumping techniques may no longer work.

One suggestion to increase the chance of getting stumps from the models is to think about asking a different style question. Instead of asking for a retrospective recommendation, ask a prospective or predictive recommendation. This will force the use statistical forecasting and prediction models where you can use linear regression analysis and then offer a prediction based on probabilistic modeling. The question should still lead to a business recommendation and not just a number:

Examples of questions that can be asked in a forecasting or predictive modeling:

- When will evacuations be necessary based on spread of the wildfire?
- Which crop type will be most affected by current weather patterns are disrupted by [x]?
- Is the virus likely to spread through the population and at what probability?
- Will seasonal spikes increase product demand this quarter and by how much?
- Which warehouse will face the greatest pressure to meet expectations in the next month, 3 months from now, 1-year from now?
- Will this new [reading/math/extracurricular] program raise test scores?
- Will reduction in class instruction-time risk retention of content knowledge?
- Which student demographic will benefit the most from after-school tutoring?
- Which software components are most vulnerable to bugs?
- When should we schedule preventive maintenance to avoid downtime?
- Will currency exchange rates fluctuate over the next [x] days and in what direction and magnitude?
- Which product is this customer segment most likely to buy next?
- What strategy will make free-trial users convert to a paid account?
- Which warehouse items is most likely to go out of stock in next [x] months?
- When will the expected passenger volume for [x] cause us to need additional coverage?
