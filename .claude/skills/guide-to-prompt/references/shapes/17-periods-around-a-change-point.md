# Shape 17 · Periods around a change point

> **Where the criteria come from:** each observed period around the change.

You line up the periods around a suspected change, stating each earlier period once and checking
each later period against a committed baseline, and find where the longest run of excess sits.
The answer is the go or no-go call and the amount it unlocks. The many criteria come from each
observed period around the change.

**Canonical Axis 1 objective under our roster:** Anomaly Detection & Diagnostics.

## Sizing it to 25

Four pre-change periods stated once, plus eight post-change periods stated twice (the observed
value and the baseline it is checked against), is twenty criteria, and this is the other shape
that reaches 25 on a **single deliverable**. Add the run-breaking period's observed and baseline
pair, the period the longest run starts, the amount the determination unlocks, the call itself,
the governing standard, and the deliverable's structural checks.

**What makes it hard rather than long.** The baseline is **committed and computed**, not
observed: the policy defines how it is built (which pre-periods count, what seasonal or exposure
adjustment applies), and a solver that uses a naive pre-period mean gets a different run and a
different call. The trigger is a **run-length test**, so a single breach is not enough and one
period that dips back below the tolerance breaks the run, which is why the run-breaking period is
its own criterion. Put the baseline construction in the policy memo and the run-length requirement
in a separate standard.

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

### Economics · 1 file · ~27 criteria
*Dislocation trigger after a plant closure notice*

I am the workforce board's research analyst, and the call is one determination, whether Ridgeport
initial claims meet the state's dislocation trigger in the Rapid Response memo, which is what
would release our layoff-aversion reserve. Write the brief for the executive director,
ridgeport_dislocation_brief.docx, with the week-by-week table and the trigger charted: whether we
meet the test and when the longest clearing run starts and how long it lasts, one row per week
from the pre-notice weeks through the latest showing area claims, the memo baseline, and whether
it clears, plotted with the trigger line, and the reserve release a declaration unlocks in
dollars.

*Criteria:* 4 pre-notice weeks stated once + 8 post-notice weeks stated twice (observed claims and
memo baseline) = 20 + the run-breaking week's observed/baseline pair + the run start week + the
reserve figure + the call + the state standard + 3 deliverable-structure checks.

### Product Analytics · 1 file · ~27 criteria
*Release freeze after a reliability regression*

I lead reliability, and under our SLO policy a sustained breach of the error budget triggers a
release freeze on the checkout service. I owe one call on whether it has breached. Draft the
reliability brief for leadership, a Word doc, with the daily table and the budget line charted:
whether we breach and when the longest over-budget run starts and how long it lasts, one row per
day from the pre-deploy days through the latest showing the observed error rate, the policy
baseline, and whether it is over budget, plotted with the trigger line, and the release-freeze
window length a breach imposes, from the schedule.

*Criteria:* 4 pre-deploy days stated once + 8 post-deploy days stated twice (observed rate and
policy baseline) = 20 + the run-breaking day's observed/baseline pair + the run start day + the
freeze-window figure + the call + the SLO standard + 3 deliverable-structure checks.

### Supply Chain & Logistics · 1 file · ~26 criteria
*Invoke the damage clause after a carrier switch*

I manage transportation procurement, and the contract's damage clause lets us claw back credits if
the rate clears the tolerance over the required consecutive weeks. I owe one call on whether it
fires. Write the brief for legal, damage_clause_brief.docx, with the weekly table and the
tolerance charted: whether the clause fires and when the longest breach run starts and how long it
lasts, one row per week from the pre-switch weeks through the latest showing the observed damage
rate, the SLA baseline, and whether it is over tolerance, plotted with the trigger line, and the
credit claw-back the clause unlocks in dollars.

*Criteria:* 4 pre-switch weeks stated once + 8 post-switch weeks stated twice (observed rate and
SLA baseline) = 20 + the run-breaking week's observed/baseline pair + the run start week + the
credit figure + the call + the SLA standard + 3 deliverable-structure checks.

### Policy & Education · 1 file · ~27 criteria
*Attendance alert after a bus-route change*

I coordinate attendance and MTSS for the district, and the state's early-warning policy releases a
support allotment when a zone clears the tolerance over the required consecutive weeks. I owe one
determination on whether the north zone meets it. Draft the brief for the superintendent, a memo,
with the weekly table and the alert line charted: whether the alert fires and when the longest
elevated run starts and how long it lasts, one row per week from the pre-change weeks through the
latest showing the observed absence rate, the policy baseline, and whether it is over tolerance,
plotted with the trigger line, and the support allotment a determination releases in dollars.

*Criteria:* 4 pre-change weeks stated once + 8 post-change weeks stated twice (observed rate and
policy baseline) = 20 + the run-breaking week's observed/baseline pair + the run start week + the
allotment figure + the call + the state standard + 3 deliverable-structure checks.
