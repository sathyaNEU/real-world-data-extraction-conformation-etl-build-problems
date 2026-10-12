# Prompt shapes

A shape is named for where the rubric's 25 or more criteria come from: the **structure of the answer**, never a
stack of asks. Pick the shape the data and the decision already have, size it on paper, write the arithmetic into the
design note. Each shape's full file (`01-` to `18-` here) carries four worked prompts from the client's paid-out tasks, read on
demand as idea seeds, never copied. The eighteen are patterns seen to carry a rich rubric, not a menu: a structure outside them is legal
(card `shape: other`) with its arithmetic written out. `fingerprint/vocab.json` keys the shapes `01` to `18`, and
`guard.py` (`SHAPE_OBJECTIVE`, `SHAPE_DECISIONS`) mirrors the objective column below.

**The shape is not the stump.** It decides where the criteria come from; `stumping` decides why the task is hard.
Each entry's *Hard* line is the seam between the two: worked without it the shape is wide and easy and the whole field
answers it. A filed rule may set the test, but the decisive step must be analysis the rule leaves to the analyst,
never applying the rule (`stumping` Part 1). Reusing a shape is legitimate; reusing a driver is a clone. The ask lines
are the client's, idea seeds only: never copy a scenario, entity, metric, file name or wording.

## Sizing to 25

| Unit | Times | Gives |
|---|---|---|
| The repeated unit (candidate, period, bucket, item, stage, cell, field, indicator, segment) | 10 to 20 | 10 to 20 |
| A second figure on the same unit (rank, verdict, range, cost) | same | doubles it |
| The call, the runner-up, the gap, the flip threshold | once each | 3 to 4 |
| A chart with its parts named (series, ordering, threshold line at its value, annotation, title stating the finding) | once | 5 to 7 |
| The deliverables, present and named | 1 to 3 | 1 to 3 |

Under 25 means a denser structure (more units, or a second figure per unit), never more asks. No ceiling.

**Drift.** Nine shapes default to Descriptive & Distribution, so check `guard.py recent` before drawing. Forecasting
is the most wanted objective and the tiebreak: 02 and 13 carry it natively, 04 and 06 whenever the bar is cleared over
an open window or the total rests on a rate the history pins. No shape defaults to Opportunity Sizing or Data Quality
Monitoring; those tags come from the objective's own test.

## The eighteen

| # | Shape | Criteria from | Objective | Files |
|---|---|---|---|---|
| 01 | Ranked list under a cap | each candidate's score, in or out, the first below the line | DD (F if the score is predicted) | 2 |
| 02 | Forecast across many periods | each period's forecast | **F** | 2 |
| 03 | Bridge between two totals | each reconciling item, both sides | ETL (DD for a growth walk) | 2 |
| 04 | Setting one dial | the outcome at every allowed setting | DD (F over an open window) | 2 |
| 05 | Allocation to a fixed total | each bucket's amount and what it buys | DD | 2 |
| 06 | Sequenced schedule under capacity | each item's finish period, running total | DD (F on a pinned run rate) | 2 |
| 07 | Grid of cells | every cell | **EC** (DD for observed rates) | 2 |
| 08 | Rule replayed on history | each period's four outcome cells | DD (AD for breaches) | 2 |
| 09 | Funnel or chain of stages | each stage's volume, rate, unit cost | DD (RC for a fall) | 2 |
| 10 | Scorecard against thresholds | each metric-threshold check per segment | DD | **1** |
| 11 | Before and after with a control | each unit's effects and pre-period check | **EC** | 2 |
| 12 | Drill-down to one leaf | the movement's piece at each level | **RC** | 2 |
| 13 | Scenarios and the flip point | each scenario cell, earliest failure, flip | **F** | 2 |
| 14 | Cuts of a distribution | each percentile cut in each segment | DD | 2 |
| 15 | Fields conformed to one schema | each target field: source and transform | ETL | 2 |
| 16 | Indicators into one score | each indicator as it enters | DD | 2 |
| 17 | Periods around a change point | each period around the change | **AD** | **1** |
| 18 | Hypotheses versus evidence | each cause-by-evidence cell | **RC** | 2 |

**01 Ranked list under a cap.** Rank every candidate on one score, fill from the top until the cap runs out.
*To 25:* 10 to 12 candidates, score plus verdict each; the first below the line (identity, score, shortfall), trimmed
awards, the screened-out set, the cutline on the chart. A short list with a cap that bites beats twenty rows.
*Hard:* the score is built, not read; screen and cap in different files; the cap runs out mid-list.
*Ask:* "every eligible applicant in score order with its score, its request, its award, and whether it was funded".

**02 Forecast across many periods.** Forecast each period, commit one level for the series.
*To 25:* 12 periods, the level, the period that sets it, the break-even count, the committed, spot and all-spot
costs, the chart with the level drawn across. *Hard:* the commit rule is built (a break-even from prices in the pack),
and peak versus mean moves every downstream figure at once.
*Ask:* "the forecast peak node demand for each month of 2027 next to the nodes left on demand under the commit".

**03 Bridge between two totals.** Walk one total to another item by item; adopt the source or figure.
*To 25:* two sources each bridged (5 or 6 items a side), each source's gap in three periods, raw and audited totals,
the flagged rows, the adopted source, the largest losing item. *Hard:* both bridges must be built before a source can
be named; the reconciling items are discoverable in the pack, never listed.
*Ask:* "the August bridge for each source, raw count down through one line per reconciling item to the ledger".

**04 Setting one dial.** Test every allowed setting, take the lowest that clears a fixed bar.
*To 25:* 11 settings at their worst period, the setting and the one below, periods short per setting, cost at
several settings, headroom, the worst-period chart with today's setting marked. *Hard:* the bar is a worst case, not
an average; a second axis (cost to hold) stops "set it to maximum".
*Ask:* "each allowed cover level with its lowest monthly fill rate and how many months it ran short".

**05 Allocation to a fixed total.** Spread a fixed total under one rule; solve the rate that makes it land.
*To 25:* 11 buckets with dollars and units bought at local price, the rate, the weighted base, eligible set, floor,
cap, chart. *Hard:* floor and cap make it non-linear, so the residual is redistributed and the rate re-struck; one
pass gets every bucket slightly wrong.
*Ask:* "each eligible district's grant in dollars beside the students it serves at its contract price".

**06 Sequenced schedule under capacity.** Order items under capacity, blackouts and one dependency.
*To 25:* 12 finish periods, cumulative value at each period end, the run order, a Gantt with its parts named.
*Hard:* greedy by value is visibly wrong: blackouts punish the obvious order, the dependency inverts a pair, one high
rate item runs long, and the horizon binds.
*Ask:* "one row per site in run order with its start week and go-live week, and what is banked at each quarter end".

**07 Grid of cells.** Rows against columns, one measured value per cell; pick per row or one column.
*To 25:* 5 by 3 is 15, 6 by 4 is 24; one column priced per row, the assignment vector, the population reached, a
heatmap with picks marked. *Hard:* a two-gate rule (effect floor and cost cap) makes one cell binding; a grid where
the largest number wins is a max() and everyone gets it.
*Ask:* "the activation rate for each segment under each flow with the flow each segment ends up on".

**08 Rule replayed on history.** Replay a decided rule on labelled history; state what it frees.
*To 25:* 4 periods by 4 outcome cells, each period's ceiling, the periods it runs, the freed quantity, the per-case
saving. *Hard:* the four cells are distinct populations; a period that breaches suspends the rule, so the total is a
sum over a subset; the netting (time saved less rework) is where most lose the figure.
*Ask:* "for each quarter the families fast-tracked, the ones wrongly approved, the eligible ones still sent to full review".

**09 Funnel or chain of stages.** Ordered stages with volume, pass-through and unit cost; where does a budget buy most
finished output. *To 25:* six volumes, lost pool, hours per item and added terminal output at each stage, the pick,
the funnel drawing. *Hard:* the biggest lost pool is wrong because downstream pass-through discounts early recoveries,
and hours per item differ by stage.
*Ask:* "each stage's base-year intake, what we lost because nobody got to it, and the hours per item".

**10 Scorecard against thresholds.** Each metric by its own definition per segment, against its threshold; one
go or no-go. *To 25:* 5 metrics by 4 segments, the population per segment, the call, checks missed (value and verdict
are one criterion). *Hard:* different denominators and windows per metric, a compound pass test, three binding checks.
*Ask:* "each metric for each lane group over the review period beside its threshold and marked pass or fail".

**11 Before and after with a control.** Each treated unit's change against matched comparisons, after a pre-period
check; keep, extend or revert. *To 25:* 6 units by 3 figures (two effects, pre-period gap), pooled figures, comparison
changes, population, call, chart against two tolerances. *Hard:* the owner's weighting (a simple mean is wrong), the
pre-period check as a gate, a three-way call on tolerances.
*Ask:* "each pilot county's employment and hours effects with the pooled row, and each county's pre-period gap".

**12 Drill-down to one leaf.** Break one movement level by level, mix separated from rate, to one leaf and its owner.
*To 25:* every graded branch at every level, the chosen branch per level, the leaf, the headline, the level-one mix
term, the tree with the path highlighted. *Hard:* mix versus rate; ranking leaves globally lands elsewhere, and
skipping the mix term at level one sends every level below wrong.
*Ask:* "each region's piece of the drop and each platform and version down the path".

**13 Scenarios and the flip point.** One A-or-B decision scored in every cell of a grid crossing two uncertainties.
*To 25:* 3 by 3 cells by two figures, the flip level per schedule, the earliest failure, the path, its dollar line,
the crossover chart. *Hard:* the flip point is solved by inversion, not read; the two axes move different mechanisms.
*Ask:* "for every projection crossed with every permit schedule, the rooms the tighter school needs in its worst year".

**14 Cuts of a distribution.** Cut one weighted distribution at several percentiles across segments; bands that hit
committed coverage. *To 25:* 2 percentiles by 6 segments, share qualifying per segment, population per tier, the
reference boundary per tier, the scaling factor, the base, the exhibit. *Hard:* weighted percentiles, boundaries
solved backwards from coverage, nested through an equivalence scale.
*Ask:* "each tier's ceiling at each household size and the households receiving each tier's credit".

**15 Fields conformed to one schema.** Map many source columns into one target; adopt the matching rule as key.
*To 25:* 10 fields by source and transform, rows dropped per system, the lineage column, the rule, the conformed
count, the links it reunites. *Hard:* every candidate rule built in full, a two-part test that punishes over-merging.
On an ETL build, use it only when the decisive move is the choice between rules, not the conformance.
*Ask:* "each target field with its source column per district and the transformation applied, the rows dropped".

**16 Indicators into one score.** Several indicators scaled, weighted and screened into one composite; pick the unit.
*To 25:* 7 indicators by value and scaling range, weights, the selected and runner-up composites, the screened-out
set, the direction pins, the population, ranked bars. *Hard:* the range is the eligible set's own, so screen before
scaling; inverted indicators; top two close enough that one mis-scaled indicator flips them.
*Ask:* "each indicator as it enters, the range it was scaled over, its scaled score and its composite".

**17 Periods around a change point.** Periods before and after a suspected change against a computed baseline; go or
no-go and what it unlocks. *To 25:* 4 pre periods once, 8 post periods twice (observed and baseline), the
run-breaking period, the run start, the amount, the call. *Hard:* the baseline is constructed, not observed; a
run-length trigger, so one dip breaks the run.
*Ask:* "one row per week from the pre-notice weeks through the latest, the baseline, and whether it clears".

**18 Hypotheses versus evidence.** Causes against evidence lines, each cell consistent or not on a figure; one cause
acted on. *To 25:* 4 by 4 cells, the surviving cause, its share of the movement, the decisive affected-versus-
unaffected gap, the action, the total. *Hard:* every verdict rests on a computed figure; each rival dies on a
different line. Closest shape to surface-read rejection: every candidate cause is a real change and every reported
figure true; the evidence settles which one carries the movement, never whether a number lies.
*Ask:* "each candidate cause against each evidence line marked consistent or not with the figure behind it".
