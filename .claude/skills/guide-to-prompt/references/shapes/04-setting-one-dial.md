# Shape 04 · Setting one dial

> **Where the criteria come from:** the outcome stated at every allowed setting of the dial.

You test one dial at every allowed setting and pick the lowest setting that clears a fixed bar.
The answer is that setting, with the setting just below it shown falling short. The many
criteria come from stating the outcome at each setting of the dial.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis. It is
Forecasting & Predictive Modeling when the bar has to be cleared over a window that has not
closed and the dial is set against a forecast rather than a replay.

## Sizing it to 25

Eleven allowed settings, each stated for its worst period, is eleven criteria. The committed
setting and the one below it carry the recommendation. Then the count of periods that fell short
at each setting under the commit, the annual cost or revenue at several settings (the second
decision axis), the headroom the committed setting leaves above the bar, and the worst-month
chart with today's setting marked.

**What makes it hard rather than long.** The bar has to be a worst-case test, not an average.
"Would have kept us inside the contract fill rate in every month it is measured" is a different
setting from "on average", and which months count is a definition living in a shipped contract.
The second axis, what each setting costs to hold, is what stops the answer from being "set the
dial to maximum".

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

### Supply Chain & Logistics · 2 files · ~27 criteria
*Lowest cover that clears the fill commitment*

I run inventory at our Columbus DC and I need one committed number, the days-of-cover level for
the paper family. My rule is the lowest cover the system allows that would still have kept us
inside the contract fill rate in every month it is measured. Behind it I want the level-by-level
table in cover_levels_paper.xlsx, each allowed cover level with its lowest monthly fill rate and
how many months it ran short, plus what each level costs a year to hold. Then a one-pager for
operations, a memo, with the cover we set and the room it leaves above the contract line, and a
chart of every level's worst month against that line with today's setting marked.

*Criteria:* the 11 allowed cover levels each stated for its worst-month fill rate (with the
committed level and the one below in the recommendation) + months-below at the levels under the
commit + holding cost at several levels + the worst-month chart + the committed level + 2
deliverables.

### Product Analytics · 2 files · ~27 criteria
*Auto-approval score for new sellers*

I lead trust and safety on our marketplace and I owe one setting, the risk-score threshold for
auto-approving a new seller. Take the lowest threshold the system allows that would have kept our
chargeback rate under the payments-contract ceiling in every month it is measured. Give me the
threshold-by-threshold table behind it, a workbook, each allowed threshold with its highest
monthly chargeback rate and the months it went over the ceiling, and the approvals lost per year
at each one. Then threshold_memo.pdf for the policy review, the threshold we set and the headroom
under the ceiling, and a chart of each threshold's worst month against the ceiling line with
today's threshold marked.

*Criteria:* the allowed thresholds each stated for its worst-month chargeback rate (with the
committed threshold and the one below in the recommendation) + months-over at the thresholds
under the commit + approvals-lost at several thresholds + the worst-month chart + the committed
threshold + 2 deliverables.

### Policy & Education · 2 files · ~27 criteria
*Staffing that clears the call-center SLA*

I manage the benefits call center for the county and I need one integer, the number of agents to
staff it. My rule is the lowest agent count the workforce system allows that would have kept the
answer-speed service level above the SLA in every month it is measured. Lay out the
level-by-level table behind the setting, a spreadsheet, each allowed agent count with its lowest
monthly service level and the months it fell below the SLA, plus what each level costs a year to
staff. And the one-pager for the division director, staffing_memo.docx, the agent count we set
and the room it leaves above the SLA line, with a chart of every level's worst month against the
SLA and today's staffing marked.

*Criteria:* the allowed agent counts each stated for its worst-month service level (with the
committed level and the one below in the recommendation) + months-below at the levels under the
commit + staffing cost at several levels + the worst-month chart + the committed level + 2
deliverables.

### Economics · 2 files · ~27 criteria
*Meter price that clears the occupancy target*

I run curbside management for the city and I have to commit one setting, the hourly meter price
step for the district. The rule is the lowest step the ordinance allows that would have held peak
occupancy at or under the congestion target in every month it is measured. I want the
step-by-step table behind the price, a workbook, each allowed price step with its highest monthly
occupancy and the months it ran over the target, and the annual meter revenue at each step. Then
a one-pager for the mobility board, a PDF with the chart, giving the step we set and the headroom
under the occupancy target, and plotting each step's worst month against the target with today's
price marked.

*Criteria:* the allowed price steps each stated for its worst-month occupancy (with the committed
step and the one below in the recommendation) + months-over at the steps under the commit + meter
revenue at several steps + the worst-month chart + the committed step + 2 deliverables.
