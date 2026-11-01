## Tags

**Domain:** Human Factors & Ergonomics (safety incident and error analysis: an airport's X-ray screening officers' missed threat items, read from the CT lanes' threat image projection records).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Take Douglas White (SC19116), Tina Anderson (SC46133), Meredith Rogers (SC42948), Leah Rangel (SC17045), Rhonda Perez (SC29369), Thomas Fernandez (SC46312), Emily Bridges (SC16884), Alicia Morrison (SC19645), Matthew Perry (SC43647), Valerie Scott (SC46282) off X-ray duty from 1 January 2027 for remedial training; recertify every other officer holding an X-ray endorsement on 30 November 2026.** Read on the threat objects each officer had not been shown before, their detection performance is below 75 per cent against the 80 per cent standard, and every other endorsed officer's is above 83 per cent. Not only the 3 casual officers whose hit rate over every projection in the year is under 80 per cent: that rate counts projections of objects the officer had already been shown and told were threats, which officers detect 99.5 per cent of the time against 88.5 per cent for objects new to them, so it carries the officers shown the library most over the line.

## 2. Critical Components

1. **91** officers hold an X-ray endorsement on 30 November 2026.
2. A projection is a first showing when no orientation of its threat object had been projected to the officer since the CT lanes opened: first showings are detected **88.5 per cent** of the time and repeat showings **99.5 per cent**.
3. The officers coming off detect fewer than **75 per cent** of their first showings; every other endorsed officer detects more than **83 per cent**.
4. **7** of the officers coming off clear 80 per cent on their hit rate over every projection, **6** of them full-time.

## 3. Step-by-Step Solution

1. Read SCS-04_screening_officer_competency_standard_rev6.pdf: detection performance is the probability that the officer detects a prohibited item carried in a passenger's cabin bag, assessed over the screening year 1 December 2025 to 30 November 2026 in Sydney time for every officer the register (screening_officer_register.xlsx) shows as Current on 30 November, 91 officers.
2. Conformed tip_events_20250701_20261130.csv: dropped the D3 records of 17 February 2026 that appear twice, moved event_utc to Sydney time, mapped every operator_login (the OP7 international logins used before 1 March 2026 included) to its staff_no through ct_operator_logins.csv, and every image_no, padded to six digits, to its object_code through the Images sheet of tip_library_catalogue_r1.xlsx.
3. Ordered each officer's projections from 1 July 2025 and marked a first showing where no image of the same object_code had been projected to that officer before: first showings in the screening year are detected 88.5 per cent of the time, repeat showings 99.5 per cent.
4. Took each endorsed officer's detection performance as their first showings detected over their first showings in the screening year: the officers in the recommendation fall below 75 per cent and every other officer is above 83 per cent.
5. For currency, shared each lane's rostered time in lane_roster_20251201_20261130.csv among the officers rostered on it at each moment, leaving out an officer on Personal leave that day in hr_leave_taken_20251201_20261130.csv (payroll_no to staff_no through the register), and counted the officers endorsed for the whole month with under 20 hours.
6. For throughput, placed each unit in ct_unit_bag_counts_hourly_utc.csv on the lane it stood on each day (KX6-0413 on D2 until 2 March 2026 and on D5 from 20 April, KX6-0416 on D5 until 19 April and on each lane for its two retrofit days, KX6-0590 on D2 from 5 March), kept the Sydney hours inside the lane's rostered time, which leaves out each retrofitted unit's count before the first officer starts, and summed by quarter of the screening year.
7. Recommended taking the officers named in the recommendation off X-ray duty from 1 January 2027 and recertifying the rest.

## 4. Deliverable Answers

### recertification_2027.csv

1. Officers coming off X-ray duty from 1 January 2027:
   - SC19116, Douglas White
   - SC46133, Tina Anderson
   - SC42948, Meredith Rogers
   - SC17045, Leah Rangel
   - SC29369, Rhonda Perez
   - SC46312, Thomas Fernandez
   - SC16884, Emily Bridges
   - SC19645, Alicia Morrison
   - SC43647, Matthew Perry
   - SC46282, Valerie Scott
2. Every other officer holding an X-ray endorsement on 30 November 2026 is recertified and keeps X-ray duty (81 officers).

### screening_year_review_2026.pdf

1. Call: the officers listed above come off X-ray duty from 1 January 2027 for remedial training; every other endorsed officer is recertified.
2. Chart in section 1 (Annual assessment): each endorsed officer's detection performance against the 80 per cent standard line, the officers coming off marked in red, each officer's hit rate over every projection shown as a hollow mark beside it.
3. Endorsed officers short of 20 hours of X-ray time, whole officers:
   - December 2025: 19
   - January 2026: 17
   - February 2026: 20
   - March 2026: 14
   - April 2026: 16
   - May 2026: 17
   - June 2026: 16
   - July 2026: 17
   - August 2026: 15
   - September 2026: 15
   - October 2026: 12
   - November 2026: 16
4. Passenger bags screened, nearest thousand:
   - D1: Dec-Feb 219,000, Mar-May 209,000, Jun-Aug 209,000, Sep-Nov 213,000
   - D2: Dec-Feb 212,000, Mar-May 199,000, Jun-Aug 204,000, Sep-Nov 204,000
   - D3: Dec-Feb 174,000, Mar-May 168,000, Jun-Aug 167,000, Sep-Nov 167,000
   - D4: Dec-Feb 137,000, Mar-May 132,000, Jun-Aug 131,000, Sep-Nov 133,000
   - D5: Dec-Feb 74,000, Mar-May 71,000, Jun-Aug 71,000, Sep-Nov 71,000
   - I1: Dec-Feb 144,000, Mar-May 136,000, Jun-Aug 135,000, Sep-Nov 140,000
   - I2: Dec-Feb 120,000, Mar-May 113,000, Jun-Aug 114,000, Sep-Nov 117,000
