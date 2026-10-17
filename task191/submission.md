# task191 submission

## Tags

**Domain:** General Statistics & Data Science, multiple testing and selective inference (judging one monitored extreme when the extreme was picked out of every interconnect, evening and window the platform watches).
**Analytical objective:** Anomaly Detection & Diagnostics (whether an evening shortfall is a real degradation or what monitoring 1,890 windows produces on its own).

## 1. Final Recommendation

**Fund no interconnect augment this cycle.**

The quarter's worst evening shortfall is **412 kbps**, on **HVT-01** on 2027-02-17 in the 19:00 window, and the largest worst-evening shortfall the network's own record shows at the same selection, seven interconnects over a quarter of evenings and three windows, is **489 kbps** in 2026Q1. Clause 4.2 funds an augment where the shortfall is larger than what the record shows the measurement produces without congestion, and 412 kbps is the fourth largest of the nine quarterly figures, so no interconnect clears it.

## 2. Critical Components

1. The figure the decision is taken on is a maximum over seven interconnects, 90 evenings and three windows, so the record it is measured against is the largest each earlier quarter produced at that same selection: **489**, 452, 441, 392, 379, 368, 361 and 352 kbps.
2. **HVT-01** comes closest at **412** kbps, which stands **32** per cent above its own 99th percentile for the quarter and **16** per cent below the record.
3. The call would change at **489** kbps, the largest the record holds.
4. Keeping the nine evenings clause 4.4 leaves out would put the worst shortfall at **544** kbps on **STR-01**, above the record, and fund an augment there.
5. **DLF-01** carries the largest shortfall across the quarter as a whole, a mean of **131.6** kbps, and its own 2026 fourth quarter was higher.

## 3. Step-by-Step Solution

1. Read the minute panel, resolved the UTC stamps to local time across the 28 March change, and took each interconnect's reference band and evening window medians as the delivered quality standard defines them, cross-checking against the pipeline's own daily rollup.
2. Resolved every port code to the interconnect in service at the quarter end through interconnect_register.csv, which carries the port renamed on 12 February.
3. Left out the nine evenings on which clause 4.4's booked work fell inside an evening window.
4. Computed the shortfall of every interconnect, evening and window, 1,890 of them, and took the largest: 412 kbps on HVT-01.
5. Clause 4.2 asks whether that is larger than the shortfall the record shows the measurement produces without congestion, and the figure was selected as the largest of 1,890, so the comparison is against the largest of 1,890 the record holds, not against one interconnect's own spread.
6. Took the same maximum from each of the eight earlier quarters in evening_quality_daily.csv: the largest is 489 kbps and three of the eight are above this quarter's, so the quarter ranks fourth of nine and nothing is funded.
7. For the peers, summed each peer's ports at every five-minute instant and took the 1,296th highest sample of the quarter against the commitment both sides had accepted; for the client builds, split the sessions by the release log's own rollout windows, since one version number was issued twice; for the incidents, counted to the restoration time the duty engineer recorded.

## 4. Deliverable Answers

### augment_decision_2027Q1.xlsx

1. Recommendation: **fund no augment this cycle**.
2. Comes closest: **HVT-01**, at **412** kbps.
3. The call would change at: **489** kbps.
4. Worst evening shortfall and the evening it fell on, by interconnect and window:
   - DLF-01, the 19:00 window: 301 kbps, 2027-03-18
   - DLF-01, the 20:00 window: 371 kbps, 2027-02-14
   - DLF-01, the 21:00 window: 298 kbps, 2027-01-22
   - HVT-01, the 19:00 window: 412 kbps, 2027-02-17
   - HVT-01, the 20:00 window: 311 kbps, 2027-03-22
   - HVT-01, the 21:00 window: 345 kbps, 2027-03-19
   - KZD-01, the 19:00 window: 368 kbps, 2027-03-20
   - KZD-01, the 20:00 window: 350 kbps, 2027-03-03
   - KZD-01, the 21:00 window: 306 kbps, 2027-02-08
   - OPL-01, the 19:00 window: 397 kbps, 2027-02-25
   - OPL-01, the 20:00 window: 334 kbps, 2027-03-19
   - OPL-01, the 21:00 window: 380 kbps, 2027-01-21
   - RHN-01, the 19:00 window: 332 kbps, 2027-02-24
   - RHN-01, the 20:00 window: 385 kbps, 2027-01-09
   - RHN-01, the 21:00 window: 392 kbps, 2027-01-19
   - STR-01, the 19:00 window: 370 kbps, 2027-01-17
   - STR-01, the 20:00 window: 333 kbps, 2027-03-31
   - STR-01, the 21:00 window: 400 kbps, 2027-03-06
   - VSN-01, the 19:00 window: 311 kbps, 2027-02-14
   - VSN-01, the 20:00 window: 296 kbps, 2027-01-08
   - VSN-01, the 21:00 window: 291 kbps, 2027-01-01

### shortfall_overview.png

5. One bar for each interconnect of its worst evening shortfall across the quarter, the one that comes closest marked, with the record drawn across at 489 kbps: HVT-01 412, STR-01 400, OPL-01 397, RHN-01 392, DLF-01 371, KZD-01 368, VSN-01 311.

### Also requested

6. Per peer, the quarter's billable 95th percentile, the commitment billed on and the overage:
   - Delfzicht Breedband: 159 Mbps against 124 Mbps, 236 euros
   - Grensweg Carrier: 338 Mbps against 326 Mbps, 86 euros
   - Kabelnet Zuid: 238 Mbps against 196 Mbps, 246 euros
   - Noordlijn Transit: 649 Mbps against 540 Mbps, 589 euros
   - Rhenia Telecom: 142 Mbps against 130 Mbps, 85 euros
   - Vastnet: 198 Mbps against 183 Mbps, 92 euros
   - Zandpoort IX: 89 Mbps against 72 Mbps, 158 euros
7. Per client build, the sessions and the share that rebuffered:
   - b-41600 (4.16.0): 7,838,242 sessions, 3.0 per cent
   - b-41700 (4.17.0): 8,340,125 sessions, 2.8 per cent
   - b-41800 (4.18.0): 5,807,199 sessions, 5.8 per cent
   - b-41806 (4.18.0): 5,082,479 sessions, 3.2 per cent
   - b-41810 (4.18.1): 4,502,318 sessions, 3.1 per cent
   - b-41900 (4.19.0): 5,876,425 sessions, 3.2 per cent
8. Per month, the incidents opened, those restored inside the standard and those whose recorded cause sits outside the platform:
   - 2027-01: 56 opened, 31 restored inside the standard, 30 with a cause outside the platform
   - 2027-02: 39 opened, 22 restored inside the standard, 11 with a cause outside the platform
   - 2027-03: 51 opened, 37 restored inside the standard, 27 with a cause outside the platform
