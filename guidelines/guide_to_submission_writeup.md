# RUBRIC AND GOLDEN UPDATE (2026-09-05), OPERATIVE, supersedes the 2026-08-27 block below

**The golden is one to three files, and three is the ceiling.** This reversed on 2026-09-05: the
2026-08-27 floor of three became the maximum, so a four-file golden is a spec failure on the count
alone. No format family is assigned. Ship the files a real analyst would actually produce for the
decision, and include a visual wherever one makes the call read at a glance. A table can live
inside the memo, inside a workbook, or be printed by a script rather than taking a slot of its own.

**Block 5, Deliverable Answers, got denser rather than longer.** The asks are uncapped and
untargeted now, each one multi-dimensional: a single ask can span every candidate on three measures
and owe thirty determinate figures. Every one of those figures is graded separately, so the block
has to **state them all** rather than summarise the ask it came from.

**The rubric is still generated for you and still must reach 25 or more criteria**, and the route
to 25 changed. A one-to-three file prompt is a small surface, so the criteria come from the
**prompt shape**, the structure of the answer, and never from stacking simple asks (`rubric.md`,
and the eighteen shapes in `../.claude/skills/guide-to-prompt/references/shapes/`). The weighting
moved to 30 to 40 percent on the recommendation and its critical components, 5 to 10 percent on
instruction-following, about 55 percent on the asks.

**The line "the write-up should score 100% on its own rubric" still reads: the golden output must
satisfy every positive criterion of the generated rubric.** You do not tune the rubric to the
golden; you make the prompt and the golden strong enough that the generated rubric is both wide
(25 or more criteria) and hard. **The pass bar is the top two responses averaging under 70 percent
with at least one model genuinely stumped**, the two conditions conjunctive. The threshold moved
from 50 to 70; the top-two structure never went away, and you should build to **60**, because the
on-platform verifiers are not perfectly accurate and the task is regraded more accurately after
submission.

**The golden deliverables must look business-realistic**, and this is now a stated send-back cause
rather than a preference: a golden that reads as overly LLM-generated is returned even when every
figure recomputes. Using an LLM to draft is fine; shipping its first draft is not. Run every golden
through `../.claude/skills/golden-realism/` before the bundle is declared ready.

---

# RUBRIC AND GOLDEN UPDATE (2026-08-27), SUPERSEDED by the 2026-09-05 block above, retained for reference


**The rubric is generated for you and you no longer edit it.** The old review pass, where you
opened the rubric and fixed genuine problems, is retired. The rubric is generated internally from
the prompt contract, the golden solution and the requested output files, it arrives fixed, and it
must reach **25 or more criteria** before the task can move forward. If it looks wrong, the fix is
upstream: correct the prompt or the golden and the rubric is regenerated from the corrected
pieces. The full spec, the weighting (about 30 percent on the recommendation and its critical
components across 3 or more criteria, 5 to 10 percent on instruction-following, about 60 percent
on the asks) and what a good criterion evaluates, lives in `rubric.md`.

**The golden is now three or more files**, matching the 2026-08-27 prompt format (three or more
deliverables across the two assigned format families, each carrying three or more asks). Block 5,
Deliverable Answers, covers every ask under every file, and block 6 lists every named file.

**The line "the write-up should score 100% on its own rubric" now reads: the golden output must
satisfy every positive criterion of the generated rubric.** You do not tune the rubric to the
golden; you make the prompt and the golden strong enough that the generated rubric is both wide
(25 or more criteria) and hard (the top two of twelve model responses average under 50 percent
against it, which is the pass bar that replaced stumping).

---

# FORMAT, as of 2026-08-20, still operative except where the blocks above amend it

**The submission is one file, `submission.md`,** and the golden ships alongside it as **every file
the prompt named**, in the requested formats.

**The blocks, in order:**

0. **Tags:** the Axis 0 domain and the Axis 1 analytical objective in the taxonomy's own wording, two lines under the title. The objective must be one of the six live labels. Axis 2 reasoning phases if the task folder tracks them.
1. **Final Recommendation:** one sentence, the single deterministic call, then the deciding figure, the margin over the runner up, and the rivals named with what each one leads on.
2. **Critical Components:** 2 to 5, each a step every possible methodology must calculate. Main recommendation only.
3. **Step-by-Step Solution:** numbered, method and outcome per step, no arithmetic.
4. **Justification:** defend yours, refute the alternative by naming its failure, and close the door on every other reading, written for a hostile expert.
5. **Deliverable Answers:** grouped by file, in the prompt's order, one item per ask, in its exact stated unit and rounding, each with a one-sentence Basis line.
6. **Golden Solution:** every file the prompt named.

**There is no Key Assumptions block and no Determinism block.** The forcedness argument the
determinism block used to carry lives inside the Justification, where the rival readings get refuted
by name. A convention call the prompt did not pin gets one clause inside the step that used it, and
if a competent analyst could reasonably reverse it then it is an unpinned fork and belongs pinned in
a shipped file.

**Binding:** Critical Components are strictly 2 to 5 and cover the main recommendation only; every
deliverable answer is graded at the same bar as the main recommendation; every figure shared between
two deliverables agrees in both, to the same rounding; the write-up should score 100% on its own
rubric; and it must not look LLM-generated, where em dashes are called out by name as a rejection
cause.

How to write each block, with the worked examples and the rules that decide whether it survives
review, lives in `.claude/skills/submission-writeup/SKILL.md`.

---

Writing the solution
The solution blocks are the answer key for a task. They drive the auto-generated rubric, so writing them well is what makes the rubric usable. Each Critical Component and each Step-by-Step result typically becomes a positive rubric criterion, and the Justification seeds a positive rationale criterion and the negative criteria. Write them after you have actually done the analysis, not from intuition.

Your own solution should score 100% on your rubric
Taken together, the blocks should score 100% on your own rubric. If they don't, either the solution is missing something or the rubric is.

How they fit together
Final Recommendation, the single committed decision.
Critical Components, the load-bearing intermediate results the decision rests on.
Step-by-Step Solution, the path a strong analyst takes from raw files to the decision.
Justification, why your method and conclusion are correct, why the competing option is wrong, and why no other reading survives, written to an expert.
Think of it as: the verdict, the pillars, the path, and the case.

Every block must agree exactly
Same recommendation, same numbers, everywhere. A reviewer will diff the blocks against each other, and the rubric is generated from them. A number in your Critical Components that does not match your Step-by-Step Solution is a defect that will break judge scoring downstream.

This page uses three running examples so you can see the same task carried through every block: ABC Corporation (acquire vs do not acquire), a Q3 product-line decision (cut vs double down), and a supplier switch (switch vs stay).

1. Final recommendation
One or two sentences that name the single committed conclusion.

Commit to a single deterministic conclusion. No hedge, no blend, no "it depends."
If the task names options, pick one and name what you are rejecting so the contrast is unambiguous. The recommendation may be two options, several options, or open-ended, as long as the conclusion is deterministic and 10 domain experts would agree on it.
If the task requires an exact ending phrase or format, state it verbatim.
No reasoning here. The "why" belongs in the blocks below.

Example 1 - ABC Corporation (acquire vs do not acquire)
Do not acquire Data Corporation at the asking price. Reject a full buyout at $99M.

Example 2 - Q3 product line (cut vs double down)
Double down on the product line for Q4. Do not cut it.

Example 3 - Supplier switch (switch vs stay)
Stay with Supplier A. Do not switch to Supplier B.

Weak example
The deal looks expensive, but there are strategic reasons to consider it, so a phased or conditional acquisition may be worth exploring.

Fails because it hedges, names no clear loser, and gives reasoning instead of committing to a single deterministic conclusion.
2. Critical components
The key intermediate results the recommendation depends on, each written as a short, checkable statement with a number.

**Aim for 2 to 5 components.**
Every potential solution methodology MUST calculate these components to arrive at the recommendation. If a component can be skipped under a defensible method and the analyst still lands the correct call, it is not critical, cut it.
Each should be something a rubric item could verify from the model's output.
Each component states its value or outcome; the high-level method for it appears in your Step-by-Step Solution.
Critical Components cover the **Main Recommendation only.** You do NOT provide Critical Components for the supplementary (Related) questions, those get short answers in the new Supplementary Questions Answers block instead.

Example 1 - ABC Corporation (acquire vs do not acquire)
Recurring revenue is calculated at $38M.
Top 2 customers are 61% of recurring revenue.
Normalized EBITDA margin is approximately 13%.
Implied purchase multiple is approximately 20x, above the 12x mandate ceiling.

Example 2 - Q3 product line (cut vs double down)
The lowest-revenue line carries the highest gross margin (68% vs 41% company average).
$1.8M of the $2.1M Q3 miss is one enterprise deal that slipped and closed on July 3 (Q4).
Adjusted for the slipped deal, the line is flat to +4% YoY, not declining.
The line is 9% of revenue but 22% of gross profit, so cutting it removes disproportionate margin.

Example 3 - Supplier switch (switch vs stay)
Supplier B's unit price is 12% below Supplier A ($8.40 vs $9.55).
Supplier B requires a 30,000-unit minimum order (3x current) and a 60-day lead time vs 14 days.
Net landed cost with B is higher once carrying cost and stockout risk are priced in.
Supplier B's historical defect rate is 4.1% vs 0.9% for Supplier A.

Weak example
The financials look weak, growth is slowing, and customer concentration is a concern.

Fails because there are no numbers, nothing a rubric item could verify, and removing any line would not change the recommendation, so none of it is load-bearing.
3. Step-by-step solution
A concise numbered list of the path from raw data to recommendation. Each step is an action plus the key decision or result it produced.

Start with data intake and cleaning. Deduplication, format detection, or spotting a duplicate file are real steps and are often where naive analysts go wrong.
Each step should carry a decision or a result, not just "looked at the data."
Each step states the high-level method and the outcome it produced, not the arithmetic. The figures must match Critical Components exactly; no separate calculations write-up is needed.
At least one step must be a trap you refused, stated as a decision (a merge you declined, a circular metric you discarded, a duplicated file you deduped).
End with the commit step: single option, any required phrase, any required references.
Aim for 6 to 10 steps. If you have 12, you are probably listing sub-analyses that belong inside one step.

Example 1 - ABC Corporation (acquire vs do not acquire)
Join the 6 files on customer_id; fix the leading-zero mismatch so rows match.
Normalize revenue: drop one-time and related-party sales. Recurring revenue is $38M, not $50M.
Test durability: top 2 customers are 61% of revenue, both contracts expiring within 12 months.
Normalize margin: real EBITDA margin is approximately 13% after restoring deferred R&D.
Reconcile price to value: the asking price is approximately 20x normalized EBITDA, above the 12x ceiling.
Commit: do not acquire at the asking price.

Example 2 - Q3 product line (cut vs double down)
Pull revenue by line and confirm the target line has the worst raw Q3 revenue.
Add margin: that same line has the highest gross margin (68% vs 41%).
Decompose the miss: $1.8M of the $2.1M shortfall is one enterprise deal that slipped into Q4.
Re-baseline: excluding the slipped deal, the line is flat to +4% YoY, so demand is not falling.
Weigh the cut: the line is 9% of revenue but 22% of gross profit.
Commit: double down for Q4; the miss is timing, not demand.

Example 3 - Supplier switch (switch vs stay)
Confirm the headline: Supplier B is 12% cheaper per unit.
Read the contract terms: B needs a 3x minimum order and a 60-day lead time vs A's 14 days.
Compute landed cost: carrying and stockout costs exceed the unit saving, so net cost is higher.
Check quality: B's defect rate is 4.1% vs A's 0.9%, adding returns and rework.
Commit: stay with Supplier A; the unit-price saving is erased once terms and defects are priced in.

Weak example
4. Justification
Justify your recommendation the way you would to another expert who will push back.

Make the case for why your method and conclusion are correct, and why the competing method or recommendation is wrong.
Defend your approach by naming the specific evidence and reasoning that make your recommendation the correct one.
Refute the alternative by naming the specific reason the competing method or recommendation fails, for example a circular metric, a non-causal correlation, a mismatched-population merge, or an unverifiable projection.
Write it to convince a skeptical peer who knows the domain, not to summarize for a layperson.

Example 1 - ABC Corporation (acquire vs do not acquire)
Rejecting the acquisition is correct because the durability of earnings falls apart under normalization: recurring revenue is only $38M once one-time and related-party sales are removed, the real EBITDA margin is about 13% after restoring deferred R&D, and 61% of revenue sits with two customers whose contracts expire within a year. On normalized earnings the asking price is roughly 20x, above the 12x mandate ceiling. The competing "buy" case is tempting only because the headline numbers look strong ($50M revenue, 22% margin, 9x multiple), but each of those figures is the pre-normalization number the data contradicts, so a buy rests on accepting inflated inputs an expert reviewer would flag on first pass.

Example 2 - Q3 product line (cut vs double down)
Doubling down is correct because the line carries the highest gross margin (68% vs 41%) and is 22% of gross profit on 9% of revenue, so removing it destroys disproportionate margin. The apparent Q3 shortfall is a decomposition artifact: $1.8M of the $2.1M miss is one enterprise deal that slipped and closed on July 3, and once excluded the line is flat to +4% YoY. The competing "cut" case relies on the raw Q3 revenue headline without decomposing the miss or weighting by margin, which is exactly the mistake to refuse: it treats a timing effect as a demand signal and ignores where profit actually comes from.

Example 3 - Supplier switch (switch vs stay)
Staying with Supplier A is correct because the 12% unit-price saving with B is more than offset once the contract terms are priced in: the 30,000-unit minimum (3x current) and 60-day lead time (vs 14) push carrying and stockout costs above the unit saving, and B's 4.1% defect rate versus A's 0.9% adds returns and rework on top. The competing "switch" case relies on the sticker price alone, which is a partial-cost view an expert would reject: landed cost, not unit price, is the decision variable, and on landed cost B is worse.

Weak example
The other option is worse because the numbers just do not support it.

Fails because it never defends the chosen method, never names why the wrong answer is tempting, and never attacks it on its own data with specific figures, so it does not convince a skeptical expert of either side.
4c. Closing the door, the third job of the Justification
Two to four sentences on why your recommendation is the only answer that could be reached from your prompt, input files, and domain knowledge. This used to be its own Determinism block; it now sits at the end of the Justification.

Name the specific constraints (in the prompt, in the data, or from domain norms) that close off every other conclusion.
Show that the alternatives fail on the evidence, not on taste or emphasis.
Keep it tighter than the Justification. This is not a re-run of the case; it is the reason no other case survives.

Example 1 - ABC Corporation (acquire vs do not acquire)
No other answer survives the normalization step. Once one-time and related-party sales are stripped, recurring revenue is $38M rather than $50M, and once deferred R&D is restored the EBITDA margin is about 13% rather than 22%, which puts the implied multiple at roughly 20x against the mandate's 12x ceiling. A "buy" or "conditional buy" can only be reached by keeping the pre-normalization numbers the data itself contradicts, so the disagreement is with the evidence, not a matter of judgment.

Example 2 - Q3 product line (cut vs double down)
"Cut" is only reachable by reading the Q3 revenue headline without decomposing it. Once the $1.8M slipped enterprise deal (closed July 3) is separated from the $2.1M miss, the line is flat to +4% YoY, and it still carries the highest gross margin (68% vs 41%) and 22% of gross profit on 9% of revenue. There is no defensible framing under which removing the highest-margin, non-declining line improves the portfolio, so "double down" is forced by the data, not chosen.

Example 3 - Supplier switch (switch vs stay)
The 12% unit-price advantage for Supplier B is fully consumed once the 3x minimum order, 60-day lead time, and 4.1% defect rate are priced into landed cost. A "switch" recommendation can only be reached by grading on sticker price alone, which the contract terms and quality data in the files rule out. On landed cost, Supplier A wins on every provided input, so staying is the only conclusion the evidence supports.

Weak example
Other analysts might disagree, but this is the answer we think is best given the tradeoffs.

Fails because it treats the decision as taste, names no constraint that closes off the alternative, and never shows the competing answer failing on the evidence.
