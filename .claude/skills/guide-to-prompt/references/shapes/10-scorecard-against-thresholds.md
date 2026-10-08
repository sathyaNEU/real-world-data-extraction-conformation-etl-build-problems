# Shape 10 · Scorecard against thresholds

> **Where the criteria come from:** each metric-against-threshold check, in each segment.

You run a fixed scorecard, computing each metric by its own written definition for each segment
and comparing it against its own threshold. The answer is the single go or no-go that the
folder's written pass-fail test resolves to. Each metric-against-threshold check is its own
criterion.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis.

## Sizing it to 25

Five metrics across four segments is twenty threshold checks, and this is the one shape that
reaches 25 comfortably on a **single deliverable**. Add the population behind each segment (four
more), the one-word call, and the count of checks missed. Note what is *not* a criterion here:
the pass-fail verdict and the underlying value are one criterion per cell, not two.

**What makes it hard rather than long.** Each metric is computed **by its own written
definition**, and those definitions live in the contract, not in the prompt. Different
denominators, different exclusion windows, different review periods per metric is what separates
this from a pivot table. The pass-fail test itself is compound ("every critical check clears and
the rest miss no more than the contract allows"), so the call turns on which checks are critical,
which is another clause in the shipped document. Three checks should be binding, and they carry
the recommendation.

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

### Supply Chain & Logistics · 1 file · ~29 criteria
*Renew the truckload carrier on the contract scorecard*

I run the truckload category for a consumer goods shipper and I owe a one-word renewal call on
this carrier, renew or do not renew. The test is the contract's own: every critical check clears
its threshold and the rest miss no more than the contract allows, over the review period the
contract defines. Put it in the scorecard memo for the sourcing committee,
carrier_renewal_scorecard.docx, leading with the call and how many checks they missed, then each
metric for each lane group over the review period beside its threshold and marked pass or fail,
and how many loads sit behind each lane group.

*Criteria:* 5 contract metrics x 4 lane groups = 20 threshold checks over the contract-defined
review period, plus 4 lane-group load counts, the renewal call, and the memo. The three binding
checks carry the recommendation.

### Product Analytics · 1 file · ~28 criteria
*Promote the feature to GA on the launch scorecard*

I am the PM for our collaboration feature and I need a one-word launch call, ship to GA or hold.
It runs off the launch plan's readiness scorecard: every gating metric clears its bar and the
non-gating ones miss no more than the plan allows, across the cohorts and window the plan
defines. I want it as the readiness slide for the launch review, a deck, leading with the call
and how many checks missed, then a metric-by-cohort scorecard grid over the window with each cell
set against its bar and marked pass or fail, and the active accounts behind each cohort.

*Criteria:* 5 readiness metrics x 4 cohorts = 20 threshold checks over the plan-defined window,
plus 4 cohort account counts, the GA call, and the deliverable. The three binding checks carry
the recommendation.

### Nonprofit & Grant-making · 1 file · ~28 criteria
*Renew the subrecipient on the compliance scorecard*

I handle grants compliance at a national intermediary and I owe a one-word funding call on this
subrecipient, renew or do not renew. The test is the subaward agreement's scorecard: every
critical measure clears its threshold and the rest miss no more than the agreement allows,
computed per program site over the review period. Write it up as subaward_scorecard.docx for the
awards committee, the call and how many checks they missed up top, then each measure for each
site over the review period beside its threshold and marked pass or fail, and the active
participants behind each site.

*Criteria:* 5 compliance measures x 4 program sites = 20 threshold checks over the
agreement-defined review period, plus 4 site participant counts, the renewal call, and the memo.
The three binding checks carry the recommendation.

### Policy & Education · 1 file · ~28 criteria
*Renew the charter on the performance scorecard*

I analyze renewals for a charter authorizer and the board needs a one-word call, renew the
charter or do not. It resolves on the accountability framework's scorecard: every must-clear
indicator meets its standard and the rest miss no more than the framework permits, computed per
grade band over the review term. Deliver the renewal recommendation for the authorizer board as a
PDF, the call and how many indicators the school missed first, then each indicator for each grade
band over the review term beside its standard and marked meets or misses, and the students
enrolled behind each grade band.

*Criteria:* 5 framework indicators x 4 grade bands = 20 threshold checks over the
framework-defined review term, plus 4 grade-band enrollment counts, the renewal call, and the
deliverable. The three binding checks carry the recommendation.
