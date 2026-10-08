# Shape 02 · Forecast across many periods

> **Where the criteria come from:** every period's forecast value, each one its own check.

You forecast a value for each of many periods, then commit to one level for the whole series.
The answer is that single committed level. The many criteria come from every period's forecast
value, each one its own check.

**Canonical Axis 1 objective under our roster:** Forecasting & Predictive Modeling, which is
the most wanted objective and the tiebreak when two pairings are equally good.

## Sizing it to 25

Twelve periods forecast is twelve criteria before anything else counts. The committed level is
one more, the period that sets the level is another, and the break-even count that justifies
committing rather than buying spot carries a third. Then the cost comparison under the commit
(the committed leg, the spot leg, and the all-spot counterfactual) is three, and the chart with
the commitment drawn across the twelve months is worth several when its parts are named.

**What makes it hard rather than long.** The commit rule has to be a rule the solver builds,
not a threshold the prompt states. The canonical form is a break-even: a unit is worth
committing only if the forecast has it drawn on in enough periods to beat buying it on the open
market, and that "enough" is computed from prices living in the pack. Get the peak-versus-mean
distinction wrong, or the break-even count wrong, and every downstream figure moves together,
which is what makes the shape discriminating rather than merely wide.

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

### Product Analytics · 2 files · ~24 criteria
*GPU reservation for 2027*

I own infrastructure finance for our ML platform, and I need one committed number: how many GPU
nodes to reserve for 2027. The rule is that we reserve a node only if the forecast has us paying
on demand for it in enough months to cover the reservation. Put the month-by-month plan behind
the number in gpu_reservation_2027.xlsx, the forecast peak node demand for each month of 2027
next to the nodes left running on demand each month under the commit, then the 2027 bill under
the commit with reserved and on-demand split out and the all-on-demand cost beside it. Then a
one-pager for the CFO, a memo, stating the nodes we reserve and the month that sets the level,
with a chart of the twelve forecast months and the reservation drawn across them as a line.

*Criteria:* 12 monthly forecast points + the reserved level + the break-even busy-month count +
the reserved/on-demand/all-on-demand bills + the chart with the reservation line + 2
deliverables.

### Supply Chain & Logistics · 2 files · ~24 criteria
*Dedicated fleet commitment for next year*

Our dedicated-fleet contract renews and I run transportation planning, so I owe one committed
number, the count of dedicated trucks to reserve for next year. We keep a truck only if the
forecast has it beating the spot rate in enough months to earn its keep. I need the monthly load
plan under that commit as a workbook, forecast monthly load-miles next to the miles run on
dedicated trucks each month, then the annual transport bill with dedicated and spot separated
and the all-spot cost for comparison. Then the page for the transportation review,
fleet_memo.docx, naming the trucks we reserve and the peak month that sets the level, with a
twelve-month chart and the committed capacity drawn as a line.

*Criteria:* 12 monthly load-mile forecasts + the committed truck count + the break-even month
count + the dedicated/spot/all-spot bills + the chart with the capacity line + 2 deliverables.

### Economics · 2 files · ~24 criteria
*Firm capacity block for the power year*

I run resource planning at our municipal power authority and I need to commit one figure, the
firm capacity block in megawatts to reserve for next year. We commit a block only if the
forecast has peak load drawing on it in enough months to beat buying that power on the spot
market. Lay out the monthly plan under the block in capacity_commitment.xlsx: forecast monthly
peak load beside the load served firm each month under the commit, then the annual power cost
with firm and spot split out and the all-spot cost alongside. For the board's resource
committee, write a short brief, a PDF, giving the megawatts we commit and the peak month that
sets the level, and chart the twelve forecast months of load with the committed block drawn
across as a line.

*Criteria:* 12 monthly peak-load forecasts + the committed MW block + the break-even month count
+ the firm/spot/all-spot costs + the load chart with the block line + 2 deliverables.

### Demographic & Social Science · 2 files · ~24 criteria
*Standing bus runs for the year*

I plan service at our transit agency, and the question in front of me is one number, how many
standing bus runs to lock for the year. We keep a run only if the forecast has ridership filling
it in enough months to beat covering that demand with on-demand microtransit. I want the monthly
ridership plan under the commit in a workbook, forecast monthly ridership next to the rides the
standing runs carry each month, then the annual service cost with standing and on-demand
separated and the all-on-demand cost for the comparison. Give me service_memo.docx for the
service-planning committee too, the standing runs we commit and the peak month that sets the
level, with a twelve-month ridership chart and the committed run capacity drawn across as a
line.

*Criteria:* 12 monthly ridership forecasts + the committed run count + the break-even month
count + the standing/on-demand/all-on-demand costs + the ridership chart with the capacity line
+ 2 deliverables.
