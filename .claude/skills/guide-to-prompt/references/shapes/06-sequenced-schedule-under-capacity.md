# Shape 06 · Sequenced schedule under capacity

> **Where the criteria come from:** each item's finish period, and the running total at the end of each period.

You put items in an order that respects a capacity limit, blackout dates, and one dependency.
The answer is the run order. The many criteria come from each item's finish period and the
running total at the end of each period.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis. It becomes
Forecasting & Predictive Modeling when the banked total rests on a run rate the supplied history
has to pin down rather than on a rate the pack states.

## Sizing it to 25

Twelve items, each with a finish period, is twelve criteria. Cumulative banked value at each of
the earlier quarter ends is four or five more, the end-of-horizon total sits in the
recommendation, and the run order itself is graded as a set. The Gantt earns several when its
parts are named: the shaded blackouts, the dependency link drawn, the labelled start and finish
on each bar, and the cumulative line with the period ends marked.

**What makes it hard rather than long.** Greedy-by-value is the wrong answer and has to be
*visibly* wrong. Make the blackouts fall where they punish the obvious order, make the
dependency invert one pair, and make one item's run rate high but its duration long enough that
starting it early costs more than it banks. The horizon has to bind, so items that finish after
it bank nothing.

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

### Supply Chain & Logistics · 2 files · ~25 criteria
*WMS migration sequence under one team*

I run the WMS program from the PMO at a broadline foodservice distributor, and the
twelve-warehouse migration sequence is mine to set. Order them for the most savings banked by the
end of 2027, one site at a time, never in a blackout week or the freeze, and the cross-dock
cannot go until its hub is live. I need the plan the team runs to, wms_migration_sequence.xlsx,
one row per site in run order with its start week and go-live week, and what is banked at each
quarter end through 2027. Then the steering-committee chart, a PNG, a bar per site with start and
go-live weeks labelled, the blackouts and freeze shaded and the hub link drawn, and cumulative
savings underneath with the quarter ends marked.

*Criteria:* 12 site go-live weeks + cumulative savings at the four earlier quarter-ends + the
end-2027 total in the recommendation + the run-rate basis + the run order + the shaded-blackout,
dependency-link and cumulative-line Gantt checks + 2 deliverables.

### Product Analytics · 2 files · ~25 criteria
*Service migration order under one crew*

I own the backend platform migration and the sequence is mine. Run the services for the most
infrastructure-cost savings banked by year end, one at a time, never during a code freeze or a
peak-traffic blackout, and checkout cannot cut over until payments is live. Give me the plan the
crew runs to, a workbook, one row per service in run order with its start week and cutover week,
and what is banked at each quarter end through the year. Then the chart for the platform review,
migration_gantt.png, a bar per service with start and cutover weeks labelled, freezes and
blackout weeks shaded and the dependency link drawn, cumulative savings underneath with the
quarter ends marked.

*Criteria:* the service cutover weeks + cumulative savings at the earlier quarter-ends + the
year-end total in the recommendation + the run-rate basis + the run order + the shaded-blackout,
dependency-link and cumulative-line Gantt checks + 2 deliverables.

### Policy & Education · 2 files · ~25 criteria
*School renovation sequence under one crew*

I run the district's bond construction program and the renovation schedule is mine. Sequence the
schools for the most energy savings banked by the bond deadline, one at a time, no work during
the state testing window or the school-year blackout, and the annex waits on its main building. I
want the plan the crew builds to, a spreadsheet, one row per school in run order with its start
week and completion week, and what is banked at each term end through the deadline. Then the
chart for the facilities committee, a PNG, a bar per school with start and completion weeks
labelled, testing windows and blackouts shaded and the dependency link drawn, cumulative energy
savings underneath with the term ends marked.

*Criteria:* the school completion weeks + cumulative savings at the earlier term-ends + the
deadline total in the recommendation + the run-rate basis + the run order + the shaded-blackout,
dependency-link and cumulative-line Gantt checks + 2 deliverables.

### Economics · 2 files · ~25 criteria
*Substation upgrade sequence under one crew*

I manage the capital program at our regional utility and the substation sequence is mine to
commit. Order the upgrades for the most loss-reduction savings banked by the filing deadline, one
substation at a time, no work in the storm-season blackout or the load-peak freeze, and the
downstream feeder waits for its trunk. Build upgrade_sequence.xlsx as the plan the crew runs to,
one row per substation in run order with its start week and energization week, and what is banked
at each quarter end through the deadline. Then the chart for the capital review,
upgrade_gantt.png, a bar per substation with start and energization weeks labelled, storm-season
and freeze weeks shaded and the dependency link drawn, cumulative savings underneath with the
quarter ends marked.

*Criteria:* the substation energization weeks + cumulative savings at the earlier quarter-ends +
the deadline total in the recommendation + the run-rate basis + the run order + the
shaded-blackout, dependency-link and cumulative-line Gantt checks + 2 deliverables.
