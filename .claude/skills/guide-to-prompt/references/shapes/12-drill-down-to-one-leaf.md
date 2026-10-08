# Shape 12 · Drill-down to one leaf

> **Where the criteria come from:** the piece of the movement stated at each drill level.

You break one overall movement down level by level, region, then platform inside it, then
version inside that, separating a shift in the traffic mix from a real change in the rate before
ranking any branch. The answer is the single leaf the drill lands on and the team that owns it.
The many criteria come from the piece of the movement stated at each drill level.

**Canonical Axis 1 objective under our roster:** Root-Cause Analysis.

## Sizing it to 25

Every graded branch at every level is a criterion: four other regions at level one, three other
platforms at level two, three other version buckets at level three is ten, plus the chosen branch
at each of the three levels and the leaf itself. Add the headline movement, the level-one mix
term, and the tree drawing with each box carrying its slice and the path highlighted.

**What makes it hard rather than long.** The **mix-versus-rate separation** is the whole shape. A
branch can show the largest raw movement purely because its share of volume moved, and the memo's
definition of how mix is separated out lives in a shipped document, not in the prompt. The drill
is greedy and level-ordered, so a solver that ranks leaves globally lands somewhere else, and a
solver that skips the mix term at level one drills into the wrong region and every level below it
is wrong. Make the mix term large enough at level one to invert the naive ranking.

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

### Product Analytics · 2 files · ~26 criteria
*Checkout conversion drop drilled to one team*

I lead product analytics and I have to assign the checkout-conversion incident to one team. The
rule is to drill region, then platform, then version, taking the biggest piece of the decline at
each step with traffic mix separated out the way the memo defines, and the team that owns the
landing version gets it. Write the assignment note, checkout_incident_memo.docx, naming the team
that gets the incident and the segment that puts it there, then each region's piece of the drop
and each platform and version down the path. And the tree for the standup deck, a PNG, one box
per region, platform and version each carrying its slice of the drop, with the path down to the
blamed segment highlighted.

*Criteria:* graded branches at each level (4 other regions, 3 other platforms, 3 non-leaf version
buckets), plus the chosen branch at each of the three levels and the leaf in the recommendation,
the headline drop and level-1 mix, and the two tree deliverables.

### Supply Chain & Logistics · 2 files · ~25 criteria
*On-time delivery drop drilled to one carrier*

I run transportation for a national retailer and I need one account owner named for the on-time
miss. Drill region, then DC, then carrier, taking the biggest piece of the decline at each step
with volume mix separated out as the memo defines, and the carrier's account team owns it. Give
me the tree for the review deck first, otd_drilldown.png, one box per region, DC and carrier each
with its slice of the drop, and the path to the blamed carrier segment highlighted. Then the
assignment note for the network review, a memo, the carrier team that owns the miss and the lane
segment that puts it there, then each region's piece of the on-time drop and each DC and carrier
down the path.

*Criteria:* graded branches at each level (other regions, other DCs, other carriers), plus the
chosen branch at each of the three levels and the leaf in the recommendation, the headline
on-time drop and its level-1 volume-mix term, and the two tree deliverables.

### Policy & Education · 2 files · ~25 criteria
*Graduation rate drop drilled to one school*

I analyze accountability data for the state education agency and I have to hand the turnaround
team one school. The rule is to drill region, then district, then school, taking the biggest piece
of the decline at each step with enrollment mix separated out as the memo defines, and the
school's turnaround office takes it. I want the assignment note for the deputy,
grad_rate_memo.docx, the school that gets the assignment and the level that puts it there, then
each region's piece of the drop and each district and school down the path. And the tree for the
leadership briefing, a PNG, one box per region, district and school each with its slice of the
drop, and the path to the named school highlighted.

*Criteria:* graded branches at each level (other regions, other districts, other schools), plus
the chosen branch at each of the three levels and the leaf school in the recommendation, the
headline rate drop and its level-1 enrollment-mix term, and the two tree deliverables.

### Demographic & Social Science · 2 files · ~25 criteria
*Recurring-gift churn drilled to one segment*

I run donor analytics for a large advocacy nonprofit and the director needs one owner for the
churn rise. Drill channel, then campaign, then donor cohort, taking the biggest piece of the rise
at each step with donor-mix separated out as the note defines, and the team owning that cohort
gets it. Give me the tree for the development standup, a PNG, one box per channel, campaign and
cohort each with its slice of the churn rise, and the path to the blamed cohort highlighted. Then
the assignment note for the executive director, churn_incident_memo.docx, the team that owns the
churn rise and the segment that puts it there, then each channel's piece of the rise and each
campaign and cohort down the path.

*Criteria:* graded branches at each level (other channels, other campaigns, other cohorts), plus
the chosen branch at each of the three levels and the leaf cohort in the recommendation, the
headline churn rise and its level-1 donor-mix term, and the two tree deliverables.
