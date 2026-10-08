# Shape 05 · Allocation to a fixed total

> **Where the criteria come from:** each bucket's amount, and the outcome that amount buys.

You spread a fixed total across buckets under one rule, so the amounts add back up to the total
exactly. The answer is the single parameter, a rate, a cap, or a share, that makes the sum land.
The many criteria come from each bucket's amount and the outcome that amount buys.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis.

## Sizing it to 25

Eleven buckets is twenty-two criteria on its own, because each bucket carries two figures, the
dollars it receives and the units that money buys at its own local price. The committed rate is
one more, the weighted base the rate is struck on is another, and the eligible set, the floor,
the cap and the chart finish the count.

**What makes it hard rather than long.** The rate has to be solved, not applied. A floor and a
cap make the allocation non-linear: buckets that hit the floor or the cap stop scaling with the
rate, so the residual has to be redistributed and the rate re-struck until the total lands
exactly. A solver that strikes one rate on the whole weighted base and stops gets every bucket
slightly wrong and the total wrong, which is exactly the discrimination the shape is for. Set
the set-asides, the weighting and the eligibility screen in different shipped files.

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

### Policy & Education · 2 files · ~28 criteria
*Splitting the tutoring fund across districts*

I am the fiscal analyst in school finance who runs the tutoring-fund formula, and I need to
commit the single per-weighted-student rate we publish in the notice. Every eligible district
gets at least the floor, none more than the cap, and what is left after the set-asides goes out
at that one rate so it spends every dollar. Build the allocation table,
tutoring_fund_allocation_2026-27.xlsx, each eligible district's grant in dollars beside the
students it serves at its contract price. Then the cover page superintendents read, a Word
notice, stating the rate we publish and the students the fund serves statewide, with a chart of
every district's grant and the floor and cap drawn across it.

*Criteria:* 11 district grants + 11 students-served figures + the committed rate + the
weighted-student base the rate is struck on + the eligible set + the floor/cap chart + 2
deliverables.

### Nonprofit & Grant-making · 2 files · ~28 criteria
*Allocating the relief pool across chapters*

I run field finance for the disaster relief pool and I need one committed number, the
per-weighted-caseload rate the chapters are funded at. Every qualifying chapter gets at least the
floor, none over the cap, and the remainder goes out at that rate so the whole pool is spent.
Start with the allocation table for the field finance team, a workbook, each qualifying chapter's
grant in dollars next to the households it serves at its regional service cost. Then a memo for
the board, allocation_memo.pdf, with the rate we set and the households the pool serves
nationally, and a chart of every chapter's grant with the floor and cap drawn across it.

*Criteria:* the chapter grants + the households-served per chapter + the committed rate + the
weighted-caseload base the rate is struck on + the qualifying set + the floor/cap chart + 2
deliverables.

### Product Analytics · 2 files · ~28 criteria
*Spreading the incentive budget across channels*

I own growth finance and this quarter's acquisition-incentive budget is locked, so I need the
single per-weighted-signup bid rate we set across the channels. Every eligible channel gets at
least the floor spend, none over the cap, and the rest goes out at that rate so the whole budget
is spent. Give me the allocation table for the media plan, channel_allocation.xlsx, each eligible
channel's budget in dollars beside the signups it buys at its blended acquisition cost. Then a
slide for the growth review, a PPTX, with the rate we set and the signups the budget buys in the
quarter, and a bar chart of every channel's budget with the floor and cap drawn across it.

*Criteria:* the channel budgets + the signups-bought per channel + the committed rate + the
weighted-signup base the rate is struck on + the eligible set + the floor/cap chart + 2
deliverables.

### Supply Chain & Logistics · 2 files · ~28 criteria
*Paying carrier rebates across lanes*

I manage carrier settlements and the annual incentive pool is set, so the number I owe is the
per-weighted-volume rebate rate paid across the lanes. Every contracted lane gets at least the
floor rebate, none over the cap, and the remainder pays out at that one rate so the whole pool
clears. I want the allocation table for accounts payable, a workbook, each contracted lane's
rebate in dollars next to the loads that rebate covers at its lane cost. Then the notice the
carriers receive, rebate_notice.docx, giving the rate we set and the loads the pool covers
network-wide, with a chart of every lane's rebate and the floor and cap drawn across it.

*Criteria:* the lane rebates + the loads-covered per lane + the committed rate + the
weighted-volume base the rate is struck on + the contracted set + the floor/cap chart + 2
deliverables.
