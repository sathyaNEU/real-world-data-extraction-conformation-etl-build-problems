## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Place CRO-AD, CRO-CV, CRO-FM, CRO-GQ, CRO-LW and CRO-MG on a timeliness improvement plan.**
Their median working days from a complete application to registration, for the applications received from 1 July to 30 September 2026, exceed 20; no other office's do. Part of each office's quarter is still open on 9 October, and the open applications are the slow ones, so each is kept at risk until its age (a product-limit median). On the registered applications alone only CRO-FM and CRO-MG are over; CRO-AD, CRO-CV, CRO-GQ and CRO-LW hold their backlog among the open applications.

## 2. Critical Components

1. Offices placed on a plan: **CRO-AD**, **CRO-CV**, **CRO-FM**, **CRO-GQ**, **CRO-LW**, **CRO-MG**
2. Offices not placed: CRO-BN, CRO-DL, CRO-ES, CRO-HL, CRO-IB, CRO-KM, CRO-NM, CRO-SL

## 3. Step-by-Step Solution

1. Stacked the legacy log (DD/MM/YYYY, two-letter office codes) and the case system's log, and kept the applications received 1 July to 30 September 2026.
2. Counted working days from the clock start (the complete day, not counted) to registration, excluding weekends and the holiday calendar.
3. Added the open caseload snapshot's third-quarter applications, each at its working days from clock start to 9 October, as still running.
4. For each office took the product-limit (Kaplan-Meier) survival estimate over registered and open applications and its median, the first duration at which the estimate falls to one half.
5. Placed the offices whose median exceeds 20: CRO-AD, CRO-CV, CRO-FM, CRO-GQ, CRO-LW, CRO-MG.
6. Ask: each payment dated by its settlement batch's terminal day (the payment file carries the settlement day, the next working day), payments taken 1 July to 30 September counted and summed by office.

## 4. Deliverable Answers

### cro_timeliness_plans_q3_2026.xlsx

1. Offices placed on a plan: CRO-AD, CRO-CV, CRO-FM, CRO-GQ, CRO-LW, CRO-MG.
2. Chart of each office's median working days against the 20-day line, the planned offices marked.
3. Card payments made in the third quarter, number and amount (whole euros):
   - CRO-AD: 10,113, EUR 426,480
   - CRO-BN: 4,497, EUR 187,185
   - CRO-CV: 3,420, EUR 142,795
   - CRO-DL: 5,398, EUR 226,105
   - CRO-ES: 2,389, EUR 99,735
   - CRO-FM: 4,167, EUR 174,420
   - CRO-GQ: 2,842, EUR 118,900
   - CRO-HL: 6,798, EUR 283,990
   - CRO-IB: 2,111, EUR 87,305
   - CRO-KM: 4,920, EUR 203,815
   - CRO-LW: 3,112, EUR 129,470
   - CRO-MG: 3,826, EUR 159,580
   - CRO-NM: 5,965, EUR 251,435
   - CRO-SL: 2,494, EUR 105,525
