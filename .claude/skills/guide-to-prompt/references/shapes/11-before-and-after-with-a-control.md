# Shape 11 · Before and after with a control

> **Where the criteria come from:** each unit's before-and-after effect, and its pre-period check.

You measure each treated unit's change from before to after, against matched comparison units,
and first check that the comparison group tracked it beforehand. The answer is the keep, extend,
or revert call that the pooled, size-weighted effect triggers under the owner's tolerances. The
many criteria come from each unit's before-and-after effect and its pre-period check.

**Canonical Axis 1 objective under our roster:** Experiment & Causal Analysis.

## Sizing it to 25

Six treated units times three figures each (the first outcome effect, the second outcome effect,
and the pre-period gap) is eighteen criteria. Add the three pooled figures under the owner's own
weighting, the two comparison-side pooled changes, the population the decision reaches, the
one-word call, and the chart of every unit's two effects against the two tolerances.

**What makes it hard rather than long.** Three things carry the difficulty. The **weighting** is
the owner's, stated in a shipped memo (enrollment-weighted, caseload-weighted, size-weighted),
and a simple mean of the unit effects is the wrong pooled figure. The **pre-period check** is a
gate, not a footnote: a unit that fails it changes the pooled figure it feeds. And the call is
**three-way** (keep, extend, revert), decided by two tolerances rather than a significance test,
so the solver has to read the decision rule out of the pack rather than reach for a default.

---

## Four worked prompts


> **Before you draft, read [`../prompt-voice.md`](../prompt-voice.md).** The four prompts below are
> the client's. Across the eighteen shape files these examples open on the rule, the constraint,
> the deliverable, the question, the symptom, the number and the person, so **none of them is the
> template and the four below are not a menu of four.** Read four in a row and you will write the
> fifth in whichever voice you just read, which is how eighteen consecutive builds came to open
> with "I run". Pick the move from what forces your decision, then check it against the last three
> builds with `../voice-check.py`.

> **Idea seeds only.** Nothing below transfers into a build: not the scenario, not the entity,
> not the metric, not a file name, not the wording of a single ask.

### Economics · 2 files · ~28 criteria
*Extend the county minimum-wage pilot statewide*

I am the state labor department's chief economist and I need a one-word call on the pilot wage
step, extend, hold or revert. The Secretary's rule is to extend statewide if the pre-period check
passes and both pooled effects against the comparison counties sit inside her tolerances, and her
memo picks hold or revert otherwise. Write the committee two-pager, mw_extension_memo.docx, with
the call, whether the pre-period check passes, the pooled employment and hours effects, and the
workers who would get the raise statewide, plus a chart of each pilot county's employment and
hours effects against the two tolerances. And the effects table, a workbook, each pilot county's
employment and hours effects with the pooled row her rule uses, and each county's pre-period gap.

*Criteria:* 6 pilot counties x 3 figures (employment effect, hours effect, pre-period gap) = 18,
plus the 3 pooled figures her weighting produces, the statewide reach, the two comparison-side
pooled changes, the call and the two deliverables.

### Product Analytics · 2 files · ~27 criteria
*Roll the paywall change out to every market*

I run monetization for a consumer app and I owe one call on the paywall change, roll out
globally, hold or roll back. My director's rule is to roll out if the pre-period parallel check
passes and both pooled effects against the matched control markets land inside tolerance,
otherwise hold or roll back. Start with the per-market effects table, a workbook, each treated
market's revenue and retention effects with the pooled row the rule uses, and each market's
pre-period gap. Then the two-pager for the monetization review, paywall_rollout_brief.docx, the
call, whether the pre-period check passes, the pooled revenue and retention effects, and the
users the change would reach globally, with a chart of each treated market's revenue and
retention effects against the two tolerances.

*Criteria:* 6 treated markets x 3 figures (revenue effect, retention effect, pre-period gap) =
18, plus the 3 pooled figures under the brief's weighting, the global reach, the two
comparison-side pooled changes, the call and the two deliverables.

### Policy & Education · 2 files · ~27 criteria
*Expand the attendance program district-wide*

I direct research and evaluation for the district and I need a one-word call on the attendance
intervention, expand, keep or end. The superintendent's rule is to expand district-wide if the
pre-period check holds and both pooled effects against the comparison schools sit inside the
memo's tolerances, and the memo picks keep or end otherwise. Give me the board two-pager, a memo,
with the call, whether the pre-period check passes, the pooled attendance and achievement
effects, and the students the expansion would reach, plus a chart of each treated school's
attendance and achievement effects against the two tolerances. And the per-school effects table,
school_effects.xlsx, each treated school's attendance and achievement effects with the pooled row
the rule uses, and each school's pre-period gap.

*Criteria:* 6 treated schools x 3 figures (attendance effect, achievement effect, pre-period gap)
= 18, plus the 3 pooled figures under the memo's enrollment weighting, the district reach, the
two comparison-side pooled changes, the call and the two deliverables.

### Nonprofit & Grant-making · 2 files · ~27 criteria
*Scale the case-management model across sites*

I lead evaluation at a workforce nonprofit and I owe one call on the case-management model,
scale, hold or revert. Our evaluation plan says scale network-wide if the pre-period check passes
and both pooled effects against the comparison sites fall inside the plan's tolerances, otherwise
hold or revert. Build the per-site effects table, a workbook, each pilot site's placement and
retention effects with the pooled row the rule uses, and each site's pre-period gap. Then the
two-pager for the funder, casemgmt_scaling_memo.docx, the call, whether the pre-period check
passes, the pooled placement and retention effects, and the participants scaling would reach,
with a chart of each pilot site's placement and retention effects against the two tolerances.

*Criteria:* 6 pilot sites x 3 figures (placement effect, retention effect, pre-period gap) = 18,
plus the 3 pooled figures under the plan's caseload weighting, the network reach, the two
comparison-side pooled changes, the call and the two deliverables.
