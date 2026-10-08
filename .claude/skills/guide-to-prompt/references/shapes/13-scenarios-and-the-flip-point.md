# Shape 13 · Scenarios and the flip point

> **Where the criteria come from:** each scenario cell, the earliest point of failure, and the flip point.

You score one A-or-B decision in every cell of a scenario grid, where two sources of uncertainty
are crossed, and find the input levels where the base case flips. The answer is the committed
choice. The many criteria come from each scenario cell, the earliest point of failure, and the
flip point.

**Canonical Axis 1 objective under our roster:** Forecasting & Predictive Modeling, because the
grid is a projection over a window that has not closed. It is Descriptive & Distribution Analysis
when both axes are given scenarios rather than projections the history pins down.

## Sizing it to 25

Three projections crossed with three schedules is nine cells, and each cell carries two figures
(what the option needs, and what it can supply), so eighteen. One cell is the base case and sits
in the recommendation, the other eight are supplementary. Add the flip level under each of the
three schedules, the earliest period any scenario fails, the committed path, its dollar line, and
the crossover chart.

**What makes it hard rather than long.** The flip point is the hard part and it is where most
responses lose the shape: it is not a cell of the grid, it is the input level at which the base
case changes answer, so it has to be solved by inversion rather than read. Give the two axes
genuinely different mechanisms (one moves demand, the other moves the conversion between demand
and the constrained quantity), so the grid is not one axis restated, and put the maximum the
cheaper option can reach into a shipped facilities or capacity file rather than the prompt.

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

### Demographic & Social Science · 2 files · ~25 criteria
*Third school or additions across nine growth scenarios*

I plan facilities for our district and I own the growth-corridor line in the bond package, either
classroom additions at the two elementaries we already have or a third elementary school. The
board needs one committed bond line for the ballot. Build the nine-scenario grid so they can see
how tight each school gets, corridor_scenarios.xlsx, and for every demographer projection crossed
with every permit schedule show the permanent rooms the tighter school needs in its worst year
beside what it holds after the maximum additions the facilities memo allows. Then the one-page
note I read into the record, a memo: the choice and the dollar line for the bond, the earliest
year any scenario runs a school out of rooms, and the new-home child yield under each permit
schedule, plus the corridor capture rate, at which additions stop being enough.

*Criteria:* 3 demographer projections x 3 permit schedules = 9 grid cells (1 base cell in the
recommendation + 8 supplementary) + 3 flip yields + the flip capture rate + earliest run-out year
+ the bond dollar line + 2 deliverables + implicit context rows.

### Supply Chain & Logistics · 2 files · ~26 criteria
*Expand the hub or build a forward DC*

I run network design for our grocery distribution arm, and the decision is whether we expand the
Memphis hub one more time or stand up a forward DC in Dallas. I have to commit one path. Lay out
the scenario grid the way the committee likes to see throughput against the wall, a workbook, and
for each demand projection crossed with each lead-time regime show the peak-week outbound cases
the hub must push in its worst year beside what it can push after the maximum dock and mezzanine
mods in the facilities file. Then the memo I take to the capital committee, siting_memo.pdf, with
a chart they can read in ten seconds: the path we commit to and the capex line, the earliest year
any scenario overflows the hub charted against installed capacity, and the weekly case throughput
under each lead-time regime at which the hub first can no longer keep up.

*Criteria:* 3 demand projections x 3 lead-time regimes = 9 grid cells (base cell recommendation +
8 supplementary) + 3 flip throughputs + earliest overflow year + capex line + 2 deliverables +
implicit installed-capacity rows.

### Product Analytics · 2 files · ~25 criteria
*Self-host inference or stay on the managed API*

I lead platform infrastructure for our AI features and I have to commit one answer, keep buying
inference from the managed vendor or stand up our own GPU cluster. Give me the scenario grid that
puts the managed bill next to what self-hosting would amortize to, inference_scenarios.xlsx, and
for each traffic projection crossed with each price schedule show the managed inference bill in
its most expensive month beside the amortized monthly cost of a self-hosted cluster sized to that
month's peak. Then the decision memo for the CTO, a Word doc with the crossover drawn out: the
path we commit to and the annualized cost line, the earliest month any scenario tips past the
crossover charted with both cost curves, and the sustained requests-per-second under each price
schedule at which self-hosting becomes the cheaper path.

*Criteria:* 3 traffic projections x 3 price schedules = 9 grid cells (base cell recommendation +
8 supplementary) + 3 flip QPS levels + earliest crossover month + annualized cost line + 2
deliverables + implicit peak rows.

### Economics · 2 files · ~25 criteria
*Dredge the channel now or phase it*

I direct planning at the port authority, and the appropriation request needs one committed
recommendation, the single deep-dredge project this cycle or the phased dredging program. Set out
the scenario grid so the board can see draft against depth in every world, a workbook, and for
each cargo projection crossed with each vessel-upsizing schedule show the design-vessel laden
draft in the worst call year beside the channel depth the phased program reaches by then. Then
the appropriation memo with the crossover charted for the finance committee,
dredging_line_memo.pdf: the path we commit to and the appropriation dollar line, the earliest year
any scenario draws more water than the phased depth allows charted against the dredge timeline,
and the annual laden-call volume under each upsizing schedule at which the phased depth stops
clearing the fleet.

*Criteria:* 3 cargo projections x 3 upsizing schedules = 9 grid cells (base cell recommendation +
8 supplementary) + 3 flip call-volume levels + earliest under-depth year + appropriation line + 2
deliverables + implicit current-depth rows.
