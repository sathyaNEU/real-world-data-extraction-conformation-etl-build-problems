**Domain:** Biomedical and clinical research (genomics and high-dimensional association).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Replace the contamination screen in service with the re-run mixture-fraction screen at the 0.030 cutoff for the quarter from 1 July 2027.**
At 0.030 the candidate screen detects 16 more of the parallel run's 393 confirmed contamination events, an increase of 4.07 percentage points whose 95 per cent interval, taken from the specimens the two screens call differently, is clear of zero on every paired estimator, and its false-call rate is 1.36 per cent against 1.67 per cent.
Not 0.050, whose increase of 2 specimens (0.51 points) is established by no reading of the parallel run.
Not 0.020 or 0.015, which clear both tests but are not the highest listed cutoff that does.
Not 0.010, whose false-call rate of 1.91 per cent is above the screen in service's.
Not holding the change, which follows only if each screen's detection rate is judged against its own interval rather than the increase being judged on the specimens that carry both calls.

## 2. Critical Components

1. The comparison holds **5,839** specimens, of which **393** are confirmed contamination events and **5,446** are panel-clean
2. The screen in service detects **292** of the 393 events and flags **91** of the panel-clean specimens, a false-call rate of **1.67** per cent
3. At the 0.030 cutoff the candidate screen detects **308** events, an increase of **16** specimens, **4.07** percentage points
4. The 0.030 cutoff's false-call rate is **1.36** per cent, and of the listed cutoffs only 0.010, at **1.91** per cent, is above the screen in service's

## 3. Step-by-Step Solution

1. Joined the accepted reads in the two quality-control exports to the accepted read set's mixture fraction and to the identity panel verdicts on specimen_id.
2. Applied KVAL-07 3.1 and 3.2 to that join: the comparison is 5,839 specimens, 393 of them with a MIXED verdict.
3. Counted detections per 3.4: the screen in service flags 292 of the events, the candidate screen 294, 308, 310, 319 and 326 at the five listed cutoffs.
4. Counted false calls on the 5,446 panel-clean specimens per 3.5: 91 for the screen in service against 61, 74, 80, 85 and 104, so 4.1(b) removes only the 0.010 cutoff.
5. Took the 95 per cent interval on each increase from the specimens the two screens call differently, both calls coming from one specimen's own read sets: every paired estimator puts the 0.030 increase of 4.07 points clear of zero and leaves the 0.050 increase short of it.
6. Read 4.1(a) at each cutoff: not established at 0.050, established at 0.030, 0.020, 0.015 and 0.010.
7. Applied 4.1: the highest listed cutoff meeting both conditions is 0.030.
8. Replace the screen in service at the 0.030 cutoff from 1 July 2027.

## 4. Deliverable Answers

### screen_change_validation_2027q3.xlsx

1. Per listed cutoff, the events detected, the increase in specimens, the increase in percentage points, the false-call rate in per cent, whether the increase clears the interval test and whether the false-call rate is not higher:
   - 0.050: 294, 2, 0.51, 1.12, no, yes
   - 0.030: 308, 16, 4.07, 1.36, yes, yes
   - 0.020: 310, 18, 4.58, 1.47, yes, yes
   - 0.015: 319, 27, 6.87, 1.56, yes, yes
   - 0.010: 326, 34, 8.65, 1.91, yes, no
2. The cutoff recommended: 0.030, replacing the screen in service from 1 July 2027.
3. Per weekly report issued in April or May, the distinct vials its results came from and the excess of results issued over vials, nine reports in order:
   - BA-2027-W13: 575, 14
   - BA-2027-W14: 596, 12
   - BA-2027-W15: 601, 12
   - BA-2027-W16: 628, 13
   - BA-2027-W17: 563, 14
   - BA-2027-W18: 541, 13
   - BA-2027-W19: 555, 15
   - BA-2027-W20: 519, 23
   - BA-2027-W21: 538, 26
4. The screen in service's flagged specimens, reviewed ones by their review outcome, per thousand specimens released in the month, each counted once, twelve months in order:
   - 2026-03: 15.6
   - 2026-04: 15.3
   - 2026-05: 13.9
   - 2026-06: 14.9
   - 2026-07: 14.2
   - 2026-08: 15.1
   - 2026-09: 17.6
   - 2026-10: 19.6
   - 2026-11: 19.7
   - 2026-12: 18.8
   - 2027-01: 20.7
   - 2027-02: 16.1
5. The dilution panel's median recovery as a share of the prepared level and how many results reported fall within a fifth of it, by level:
   - L1: 0.878, 7
   - L2: 0.865, 7
   - L3: 1.027, 6

### detection_gain_by_cutoff.png

1. The increase over the screen in service at each listed cutoff with its 95 per cent interval against a zero line, the adopted 0.030 cutoff distinguished and the 0.010 cutoff marked as above the screen in service's false-call rate.
