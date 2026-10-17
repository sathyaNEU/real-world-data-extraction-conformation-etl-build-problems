# task191 submission

## Tags

**Domain:** General Statistics & Data Science, multiple testing and selective inference (judging one monitored extreme when the extreme was picked out of every interconnect, evening and window the platform watches).
**Analytical objective:** Anomaly Detection & Diagnostics (whether an evening shortfall is a real degradation or what monitoring 1,851 windows a quarter produces on its own).

## 1. Final Recommendation

**Fund no interconnect augment this cycle.**

The quarter's worst evening shortfall is **318 kbps**, on **HVT-01** on 2027-02-17 in the 19:00 window. Clause 4.2 funds an augment where the shortfall is larger than the shortfall the network's own record shows the measurement produces without congestion, and the record is the eight earlier quarters of the same measurement on the same seven interconnects. Every quarter in it produced a larger worst window than this one, from 398 kbps up to 489, so the quarter is the quietest of the nine and no interconnect clears the record.

## 2. Critical Components

1. The figure the decision is taken on is the largest of the 1,809 interconnect evening windows the quarter leaves standing, so the record it is measured against is each earlier quarter's own largest at that same reach: 489, 471, 458, 447, 436, 424, 411, 398 kbps.
2. **HVT-01** comes closest at **318** kbps, which stands **28** per cent above its own 99th percentile for the quarter and **20** per cent below the smallest worst window any earlier quarter produced.
3. **14** evenings are left out, the ones on which work was booked inside an evening window. Keeping them would put the worst shortfall at **569** kbps on **STR-01**, above every quarter in the record, and fund an augment there.
4. **DLF-01** carries the largest shortfall across the quarter as a whole, a mean of **129.1** kbps against **112.0** on the next interconnect, and the record shows that level is ordinary for it.
5. Measured against its own evening-to-evening spread instead of the record, the quarter's worst window stands clear and would fund an augment on HVT-01.

## 3. Step-by-Step Solution

1. Read the minute panel, resolved the UTC stamps to local time across the 28 March change, and took each interconnect's reference band and evening window medians as the delivered quality standard defines them, cross-checking against the pipeline's own daily rollup.
2. Resolved every port code to the interconnect in service at the quarter end through interconnect_register.csv, which carries the port renamed on 12 February.
3. Left out the 14 evenings on which clause 4.4's booked work fell inside an evening window.
4. Computed the shortfall of every interconnect, evening and window the quarter's record holds, 1,851 of them, and took the largest of the 1,809 that survive step 3: 318 kbps on HVT-01.
5. Clause 4.2 asks whether that is larger than the shortfall the record shows the measurement produces without congestion, and the figure was selected as the largest of 1,809, so the comparison has to be with what the record produces at that same reach, not with one interconnect's own spread.
6. Took the same maximum from each of the eight earlier quarters in evening_quality_daily.csv: every one is larger than this quarter's, the smallest at 398 kbps and the largest at 489, so nothing is funded. The record holds 282 of its 15,330 windows at or above this quarter's worst, so the measurement plainly produces that level without congestion.
7. For the peers, summed each peer's ports at every five-minute instant and took the 1,296th highest sample of the quarter against the commitment both sides had accepted; for the client builds, split the sessions by the release log's own rollout windows; for the incidents, counted to the restoration time the duty engineer recorded.

## 4. Deliverable Answers

### augment_decision_2027Q1.xlsx

1. Recommendation: **fund no augment this cycle**.
2. Comes closest: **HVT-01**, at **318** kbps.
3. Evenings left out: **14**.
4. Worst evening shortfall and the evening it fell on, by interconnect and window:
   - DLF-01, the 19:00 window: 246 kbps, 2027-03-18
   - DLF-01, the 20:00 window: 303 kbps, 2027-02-14
   - DLF-01, the 21:00 window: 250 kbps, 2027-01-22
   - HVT-01, the 19:00 window: 318 kbps, 2027-02-17
   - HVT-01, the 20:00 window: 248 kbps, 2027-03-22
   - HVT-01, the 21:00 window: 269 kbps, 2027-03-19
   - KZD-01, the 19:00 window: 285 kbps, 2027-03-20
   - KZD-01, the 20:00 window: 278 kbps, 2027-03-03
   - KZD-01, the 21:00 window: 247 kbps, 2027-02-08
   - OPL-01, the 19:00 window: 311 kbps, 2027-02-25
   - OPL-01, the 20:00 window: 268 kbps, 2027-03-21
   - OPL-01, the 21:00 window: 301 kbps, 2027-01-21
   - RHN-01, the 19:00 window: 263 kbps, 2027-02-24
   - RHN-01, the 20:00 window: 307 kbps, 2027-01-09
   - RHN-01, the 21:00 window: 306 kbps, 2027-01-19
   - STR-01, the 19:00 window: 290 kbps, 2027-01-17
   - STR-01, the 20:00 window: 265 kbps, 2027-03-31
   - STR-01, the 21:00 window: 312 kbps, 2027-03-06
   - VSN-01, the 19:00 window: 249 kbps, 2027-02-14
   - VSN-01, the 20:00 window: 241 kbps, 2027-01-08
   - VSN-01, the 21:00 window: 237 kbps, 2027-01-01

### shortfall_overview.png

5. One bar for each interconnect of its worst evening shortfall across the quarter, the closest one marked: HVT-01 318, STR-01 312, OPL-01 311, RHN-01 307, DLF-01 303, KZD-01 285, VSN-01 249.

### Also requested

6. Per peer, the quarter's billable 95th percentile, the commitment billed on and the overage:
   - Delfzicht Breedband: 159 Mbps against 124 Mbps, 236 euros
   - Grensweg Carrier: 337 Mbps against 326 Mbps, 79 euros
   - Kabelnet Zuid: 238 Mbps against 196 Mbps, 246 euros
   - Noordlijn Transit: 648 Mbps against 540 Mbps, 583 euros
   - Rhenia Telecom: 142 Mbps against 130 Mbps, 85 euros
   - Vastnet: 198 Mbps against 183 Mbps, 92 euros
   - Zandpoort IX: 89 Mbps against 72 Mbps, 158 euros
7. Per client build, the sessions and the share that rebuffered:
   - b-41600 (4.16.0): 9,853,791 sessions, 3.0 per cent
   - b-41700 (4.17.0): 10,484,730 sessions, 2.8 per cent
   - b-41800 (4.18.0): 7,300,481 sessions, 5.8 per cent
   - b-41806 (4.18.0): 6,389,401 sessions, 3.2 per cent
   - b-41810 (4.18.1): 5,660,060 sessions, 3.1 per cent
   - b-41900 (4.19.0): 7,387,510 sessions, 3.2 per cent
8. Per month, the incidents opened, those restored inside the standard and those whose recorded cause sits outside the platform:
   - 2027-01: 47 opened, 26 restored inside the standard, 20 with a cause outside the platform
   - 2027-02: 44 opened, 30 restored inside the standard, 13 with a cause outside the platform
   - 2027-03: 57 opened, 37 restored inside the standard, 30 with a cause outside the platform
