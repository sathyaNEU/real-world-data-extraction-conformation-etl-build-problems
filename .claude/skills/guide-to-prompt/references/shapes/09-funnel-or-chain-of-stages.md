# Shape 09 · Funnel or chain of stages

> **Where the criteria come from:** each stage's volume, its pass-through rate, and its unit cost.

You follow an ordered chain of stages, each with its starting volume, its pass-through rate, and
its unit cost. The answer is the one stage where a fixed budget buys the most finished output at
the end of the chain. The many criteria come from each stage's volume, rate, and cost.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis. It is
Root-Cause Analysis instead when the answer is the stage that caused a fall in finished output
rather than the stage that best absorbs new capacity.

## Sizing it to 25

Five worked stages plus the terminal gives six volumes. Add the capacity-lost pool at each stage,
the hours-per-item at each stage, and the finished output an added unit of capacity buys if
placed at each stage: that is twenty-one before the recommendation. The chosen stage, its hours,
its added finished output and the productive-hours figure sit in the recommendation, and the
funnel drawing with the recovered flow traced through to the terminal is the visual.

**What makes it hard rather than long.** The naive answer is the stage with the biggest lost
pool, and it has to be wrong. Downstream pass-through is what makes it wrong: an item recovered
at stage one still has to survive four more rates before it counts, so a smaller pool late in the
chain can beat a larger pool early. Make the per-item hours differ by stage as well, so the
budget buys different volumes at different stages, and make the counted output the terminal one
rather than the stage one.

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

### Nonprofit & Grant-making · 2 files · ~28 criteria
*Which pipeline stage gets the new associate*

I run grants operations at a health foundation and I need to name the single pipeline stage that
gets the new associate. My rule is the stage where their hours turn into the most grants that
close on time, counting only the work staff could not reach in the ops memo's base year. I want
the stage-by-stage funnel, grant_funnel_capacity.xlsx, each stage's base-year intake, what we
lost because nobody got to it, and the hours per item, then the on-time closures the hire adds at
each stage if placed there. Then one slide for the executive director, a deck, the stage we pick
and the on-time closures it adds, with the funnel drawn stage by stage and the hire's grants
flowing through to closeout.

*Criteria:* 5 worked stages plus the closed-on-time terminal give 6 intakes, 5 capacity-lost
pools, 5 hours-per-item and 5 placements. The chosen stage's hours, added closures and productive
hours sit in the recommendation, the rest supplementary, plus the two deliverables.

### Product Analytics · 2 files · ~27 criteria
*Where the new rep joins the sales funnel*

I run revenue operations for a mid-market SaaS company and I have to place one new rep at the
single funnel stage where their hours convert into the most closed-won deals, counting only the
pipeline we dropped last year because nobody had capacity to work it. Give me the stage-by-stage
funnel model, a workbook, each stage's base-year volume in, the deals lost to no follow-up, and
the rep hours per deal, then the closed-won each stage adds if the rep lands there. Then the
slide for the VP of Sales, headcount_case.pptx, the stage we pick and the closed-won it adds,
with the funnel drawn stage by stage and the rep's recovered deals flowing to close.

*Criteria:* 5 worked stages plus closed-won give 6 volumes, 5 capacity-lost pools, 5
hours-per-deal and 5 placements. The chosen stage's hours, added closed-won and rep productive
hours sit in the recommendation, the rest supplementary, plus the two deliverables.

### Supply Chain & Logistics · 2 files · ~27 criteria
*Which returns stage gets the new technician*

I manage reverse logistics for an electronics retailer and I need the single returns stage the
new technician joins. My rule is to put them where their hours become the most units back on the
resale shelf, counting only the units we scrapped last year because no one could get to them. I
want the stage-by-stage returns chain, a spreadsheet, each stage's base-year units in, the units
lost to no capacity, and the tech hours per unit, then the resold units the tech adds at each
stage if placed there. Then a one-pager for the DC director, staffing_case.pdf, the stage we pick
and the resold units it adds, with the chain drawn stage by stage and the tech's recovered units
flowing through to resale.

*Criteria:* 5 worked stations plus the resold terminal give 6 volumes, 5 capacity-lost pools, 5
hours-per-unit and 5 placements. The chosen stage's hours, added resold units and tech productive
hours sit in the recommendation, the rest supplementary, plus the two deliverables.

### Policy & Education · 2 files · ~28 criteria
*Where the new caseworker joins the benefits line*

I administer a state benefits program and I have to place one new caseworker at the single
processing stage where their hours become the most families enrolled on time, counting only the
applications we let lapse last year because staff could not reach them. Build the stage-by-stage
processing chain, processing_chain_capacity.xlsx, each stage's base-year applications in, the
applications lost to no capacity, and the caseworker hours per application, then the on-time
enrollments the caseworker adds at each stage. Then a slide for the division director, a deck,
the stage we pick and the on-time enrollments it adds, with the chain drawn stage by stage and
the caseworker's recovered applications flowing to enrollment.

*Criteria:* 5 worked stages plus the enrolled terminal give 6 volumes, 5 capacity-lost pools, 5
hours-per-application and 5 placements. The chosen stage's hours, added enrollments and
caseworker productive hours sit in the recommendation, the rest supplementary, plus the two
deliverables.
