# Shape 08 · Rule replayed on history

> **Where the criteria come from:** each period's outcome cells, checked against that period's ceiling.

You take a rule that is already decided and replay it across every period of a labeled history
to see how it would have done. The answer is the operational quantity the replay frees up for
the coming year. The many criteria come from each period's outcome cells: cases the rule passes,
passes that were wrong, cases it missed, and cases its carve-outs remove, each checked against
that period's ceiling.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis. It is
Anomaly Detection & Diagnostics when the finding is which periods breached the ceiling rather
than what the rule frees.

## Sizing it to 25

Four periods times four outcome cells is sixteen criteria from one signed rule. The ceiling each
period is checked against is a criterion, the periods the rule runs in are another, the hours or
units freed sits in the recommendation, and the per-case saving that converts cases into hours is
one more. Note that the rule is *given*, not chosen: the difficulty is the replay, not the design.

**What makes it hard rather than long.** The four outcome cells have to be genuinely distinct
populations, so the labelled history needs both an eligibility label and an outcome label, and
the carve-outs have to remove cases that would otherwise have passed. The suspension clause is
what makes the answer non-obvious: a quarter whose replayed error rate breaches the ceiling
contributes nothing, so the freed quantity is a sum over a subset the solver has to determine.
The netting (time avoided *less* the rework on wrong passes) is the second axis and is where most
responses lose the figure.

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

### Policy & Education · 2 files · ~25 criteria
*Sizing the child care fast-track hours freed*

I supervise child care eligibility for the county, and I need to state the caseworker hours the
signed fast-track lane frees in FY2027. Under the state QC memo the lane stays off in any quarter
last year's replay breaches the ceiling, and we bank review time avoided less the rework on
wrongful approvals. Give me the quarter-by-quarter replay of the signed screen,
fast_track_replay.xlsx, and for each FY2026 quarter the families fast-tracked, the ones wrongly
approved, the eligible ones still sent to full review, and the ones the carve-outs keep out, with
the quarterly wrongful-approval rate beside the QC ceiling. Then the note for my director, a
memo, the hours the lane frees in FY2027 and the quarters it runs, with the four quarterly rates
charted against the ceiling.

*Criteria:* one signed screen replayed over 4 FY2026 quarters x 4 outcome cells = 16, plus the QC
ceiling they are checked against, the hours freed, the quarters that run, the per-application
minutes saved and the two deliverables.

### Supply Chain & Logistics · 2 files · ~26 criteria
*Touchless invoice hours freed next year*

I run accounts payable shared services for a distributor, and the number I owe is the AP staff
hours the auto-clear rule frees next year. The finance policy keeps the rule off in any quarter
last year's replay pushed the mispay rate over the ceiling, and we bank match-and-key time
avoided less the rework on invoices cleared in error. I want the quarter-by-quarter replay of the
signed rule, a workbook, each prior-year quarter's invoices auto-cleared, cleared in error, the
match-eligible ones still routed to a clerk, and the ones the carve-outs hold back, with the
quarterly error rate beside the policy ceiling. Then the one-pager for the controller,
ap_capacity_note.docx, the hours freed next year and the quarters the rule runs, with the four
quarterly error rates charted against the ceiling.

*Criteria:* one signed auto-clear rule replayed over 4 prior-year quarters x 4 outcome cells =
16, plus the error ceiling, the hours freed, the quarters that run, the per-invoice minutes saved
and the two deliverables.

### Product Analytics · 2 files · ~25 criteria
*Payout-review hours the auto-approve frees*

I lead marketplace operations and I need to state the review-team hours the auto-approve rule
frees next year. The risk policy suspends the rule in any quarter last year's replay ran the
chargeback rate over the ceiling, and we bank manual-review time avoided less the clawback work
on payouts approved in error. Build the quarter-by-quarter replay of the signed rule,
payout_replay.xlsx, each prior-year quarter's payouts auto-approved, approved in error, the clean
ones still sent to manual review, and the ones the carve-outs hold, with the quarterly chargeback
rate beside the policy ceiling. Then a slide for the finance review, a deck, the hours freed next
year and the quarters the rule runs, and the four quarterly chargeback rates charted against the
ceiling.

*Criteria:* one signed auto-approve rule replayed over 4 prior-year quarters x 4 outcome cells =
16, plus the chargeback ceiling, the hours freed, the quarters that run, the per-payout minutes
saved and the two deliverables.

### Nonprofit & Grant-making · 2 files · ~25 criteria
*Program-officer hours a light-touch reporting rule frees*

I run grants management at a family foundation, and I owe the program-officer hours the
light-touch reporting rule frees next year. The compliance memo keeps the rule off in any quarter
last year's replay ran the misreport rate over the ceiling, and we bank full-review time avoided
less the follow-up on reports waved through wrongly. Give me the cycle-by-cycle replay of the
signed rule, a workbook, each prior-year quarter's reports waved to light-touch, waved in error,
the compliant ones still sent to full review, and the ones the carve-outs hold at full review,
with the quarterly misreport rate beside the compliance ceiling. Then the memo for my director,
capacity_memo.docx, the hours freed next year and the quarters the rule runs, with the four
quarterly misreport rates charted against the ceiling.

*Criteria:* one signed reporting rule replayed over 4 prior-year quarters x 4 outcome cells = 16,
plus the misreport ceiling, the hours freed, the quarters that run, the per-report minutes saved
and the two deliverables.
