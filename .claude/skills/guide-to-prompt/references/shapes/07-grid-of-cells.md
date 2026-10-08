# Shape 07 · Grid of cells

> **Where the criteria come from:** every cell in the grid, each one its own answer.

You fill a grid of rows against columns, like segments against options, with one measured value
in each cell. The answer is either the best pick for each row or the one column you adopt
everywhere, decided by a rule that lives in the folder. Every cell in the grid is its own
criterion.

**Canonical Axis 1 objective under our roster:** Experiment & Causal Analysis when the cells are
measured effects. It is Descriptive & Distribution Analysis when the cells are observed costs or
rates rather than estimated effects.

## Sizing it to 25

A five-by-three grid is fifteen criteria before anything else counts, and six-by-four is
twenty-four. Then one column priced per row (the second decision axis, usually a cost or a
staffing load), the per-row assignment vector or the single adopted column, the population the
assignment reaches, and the heatmap with the chosen cell marked on each row.

**What makes it hard rather than long.** The decision rule has to be a two-gate rule: a cell
only wins if it clears the effect floor *and* the option stays under a cost cap that lives in a
different file. That makes one cell binding, and the binding cell is the recommendation. A grid
where the largest number simply wins is a max() over a table, and every response gets it. Keep
the floor and the cap in separate shipped documents, and let the population after exclusions be
something the solver has to compute rather than read.

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

### Product Analytics · 2 files · ~28 criteria
*Which onboarding flow each segment gets*

I own activation for our B2B workflow product and I need one onboarding flow assigned to each of
the five segments starting in January. A segment only leaves today's checklist if a flow clears
the test plan's floor, and the assisted flow also has to clear the cost cap in the CS staffing
note. Give me the segment-by-flow read the assignment is built on, rollout_assignment.xlsx, the
activation rate for each segment under each flow with the flow each segment ends up on, plus the
assisted flow's cost per extra activated account by segment. Then the slide for Monday's
leadership review, a deck, with the segment-by-flow heatmap and our pick marked on each row, the
extra activated accounts per quarter under this assignment, and the quarterly CS cost.

*Criteria:* 5 segments x 3 flows = 15 activation-rate cells, plus the assisted column priced per
segment (5, the binding one in the recommendation), two forecast-quarter aggregates, the
per-segment assignment, the two deliverables and the population after exclusions.

### Supply Chain & Logistics · 2 files · ~27 criteria
*One carrier awarded per freight lane*

I manage the truckload category for a beverage distributor, and I need the award vector, the one
carrier that takes each of the six lanes. The RFP rule is simple: the cheapest carrier on a lane
wins it, but only among carriers that cleared the service floor on that lane group last year.
Build the award grid the routing guide is built from, a workbook, the landed cost per load for
each lane under each bidding carrier with the carrier each lane is awarded to, and each carrier's
on-time rate on the lane it is considered for against the service floor. Then the one-page
exhibit for the sourcing review, award_heatmap.png, the lane-by-carrier cost heatmap with the
awarded cell marked on each lane, and annual spend under the award beside the incumbent-only
baseline.

*Criteria:* 6 lanes x 4 carriers = 24 landed-cost cells, plus the service-floor read that gates
each lane's eligible set (the binding one in the recommendation), the per-lane award vector and
the two deliverables.

### Policy & Education · 2 files · ~27 criteria
*One reading program per grade band*

I run curriculum and instruction for the district and I owe one reading program adopted for each
of the five grade bands next year. A band only moves off the current core if a pilot program's
gain clears the board memo's effect bar for that band, and any paid program has to stay under the
per-student license ceiling. I want the band-by-program read behind the adoption,
program_adoption.xlsx, the scaled score gain for each grade band under each pilot with the
program each band adopts, and the license cost per student for each paid program by band. Then
the brief the board reads before the vote, a PDF, the program each band adopts and the students
it covers, with a heatmap of the band-by-program gains and our pick marked on each band.

*Criteria:* 5 grade bands x 3 programs = 15 gain cells, plus the license-cost column priced per
band (the binding one in the recommendation), the covered-students aggregate, the per-band
adoption and the two deliverables.

### Nonprofit & Grant-making · 2 files · ~26 criteria
*One enrollment channel adopted region-wide*

I lead outreach for a benefits-access nonprofit and I need one outreach channel adopted across
all six regions next year. The rule is to take the single channel that clears the plan's sign-up
lift bar in every region and stays under the cost-per-enrollment cap in the budget note. Give me
the region-by-channel read the choice rests on, a workbook, the sign-up lift for each region
under each channel with the channel adopted region-wide, and the cost per enrollment for each
channel by region. Then one slide for the funder update, funder_slide.pptx, the region-by-channel
heatmap with the adopted column marked, the enrollments per year under that channel, and its
annual cost.

*Criteria:* 6 regions x 3 channels = 18 lift cells, plus the cost-per-enrollment read per channel
that gates the cap (the binding one in the recommendation), the adopted column, the annual
aggregates and the two deliverables.
