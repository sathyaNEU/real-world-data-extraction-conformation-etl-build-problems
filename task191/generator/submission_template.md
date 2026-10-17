# task191 submission

## Tags

**Domain:** General Statistics & Data Science, multiple testing and selective inference (judging one monitored extreme when the extreme was picked out of every interconnect, evening and window the platform watches).
**Analytical objective:** Anomaly Detection & Diagnostics (whether an evening shortfall is a real degradation or what monitoring {nwin} windows produces on its own).

## 1. Final Recommendation

**Fund no interconnect augment this cycle.**

The quarter's worst evening shortfall is **{dec} kbps**, on **{port}** on {day} in the {win} window. Clause 4.2 funds an augment where the shortfall is larger than the shortfall the network's own record shows the measurement produces without congestion, and the record is the eight earlier quarters of the same measurement on the same seven interconnects. Every quarter in it produced a larger worst window than this one, from {qmin} kbps up to {qmax}, so the quarter is the quietest of the nine and no interconnect clears the record.

## 2. Critical Components

1. The figure the decision is taken on is a maximum over seven interconnects, {ev} evenings and three windows, so the record it is measured against is each earlier quarter's own maximum at that same reach: {rec} kbps.
2. **{port}** comes closest at **{dec}** kbps, which stands **{over}** per cent above its own 99th percentile for the quarter and **{below}** per cent below the smallest worst window any earlier quarter produced.
3. **{out}** evenings are left out, the ones on which work was booked inside an evening window. Keeping them would put the worst shortfall at **{r0}** kbps on **{r0p}**, above every quarter in the record, and fund an augment there.
4. **{r2p}** carries the largest shortfall across the quarter as a whole, a mean of **{r2}** kbps against **{r2n}** on the next interconnect, and the record shows that level is ordinary for it.
5. Measured against its own evening-to-evening spread instead of the record, the quarter's worst window stands clear and would fund an augment on {port}.

## 3. Step-by-Step Solution

1. Read the minute panel, resolved the UTC stamps to local time across the 28 March change, and took each interconnect's reference band and evening window medians as the delivered quality standard defines them, cross-checking against the pipeline's own daily rollup.
2. Resolved every port code to the interconnect in service at the quarter end through interconnect_register.csv, which carries the port renamed on 12 February.
3. Left out the {out} evenings on which clause 4.4's booked work fell inside an evening window.
4. Computed the shortfall of every interconnect, evening and window, {nwin} of them, and took the largest: {dec} kbps on {port}.
5. Clause 4.2 asks whether that is larger than the shortfall the record shows the measurement produces without congestion, and the figure was selected as the largest of {nwin}, so the comparison has to be with what the record produces at the same reach, not with one interconnect's own spread.
6. Took the same maximum from each of the eight earlier quarters in evening_quality_daily.csv: every one is larger than this quarter's, the smallest at {qmin} kbps and the largest at {qmax}, so nothing is funded. Every other figure of the record a planner might take, its mean, its median, its upper percentiles and the same figures per interconnect, is larger too.
7. For the peers, summed each peer's ports at every five-minute instant and took the 1,296th highest sample of the quarter against the commitment both sides had accepted; for the client builds, split the sessions by the release log's own rollout windows; for the incidents, counted to the restoration time the duty engineer recorded.

## 4. Deliverable Answers

### augment_decision_2027Q1.xlsx

1. Recommendation: **fund no augment this cycle**.
2. Comes closest: **{port}**, at **{dec}** kbps.
3. Evenings left out: **{out}**.
4. Worst evening shortfall and the evening it fell on, by interconnect and window:
{rows}

### shortfall_overview.png

5. One bar for each interconnect of its worst evening shortfall across the quarter, the closest one marked: {bars}.

### Also requested

6. Per peer, the quarter's billable 95th percentile, the commitment billed on and the overage:
{peers}
7. Per client build, the sessions and the share that rebuffered:
{builds}
8. Per month, the incidents opened, those restored inside the standard and those whose recorded cause sits outside the platform:
{months}
