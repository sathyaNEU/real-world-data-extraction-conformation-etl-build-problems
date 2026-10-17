**Domain:** Banking, Credit & Financial Risk (fraud and AML detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The annual report should state that 450 cash deposits were split below the prescribed transaction threshold in the reporting year to June 2027.**
Transport and courier is the largest segment at 150, ahead of grocery and convenience at 100, and two segments, rural supply and horticulture and clubs and community, show nothing the record can distinguish from their ordinary trade. Not the 2,583 deposits the near-threshold band holds, which is mostly ordinary takings of that size. Not the 1,438 a same-day screen gives, which counts the band deposits of every business that pays its takings in more than once a day. Not the 500 that reading the band on its own gives, which ignores that the takes those deposits replaced are missing from just above the threshold. Not the 1,633 from judging each customer against its own prior year.

## 2. Critical Components

1. Cash deposits of 9,000 or more and below 10,000 paid in during the year: **2,583**. Cash deposits of 10,000 or more and below 11,000: **1,428**, where the segments' own trade puts about 1,900.
2. Deposits split, by segment, to the nearest fifty: transport and courier **150**, grocery and convenience **100**, hospitality **50**, trades and construction **50**, fuel and automotive **50**, personal services **50**, rural supply and horticulture **0**, clubs and community **0**
3. Cash deposits paid in during the year, all amounts: **46,772**

## 3. Step-by-Step Solution

1. Joined both deposit feeds to the customer register through `customer_number_crosswalk.csv` and took each customer's segment from `business_customer_register.xlsx`, reading the April 2027 code reissue as the same eight segments per handbook paragraph 7.5.
2. Kept physical cash deposits paid in between 2026-07-01 and 2027-06-30, excluding the two reversed deposits and their reversing rows and collapsing the machine feed's re-sent rows: 46,772 deposits. Every machine row's UTC stamp and branch local date fall on the same day, so the reporting year does not turn on which is read.
3. Read each segment's own deposit-size profile in equal steps across the range the record covers, leaving out 9,000 to 11,000. Paragraph 7.4 makes the whole near-threshold band the thing being estimated, so no part of it evidences what it would have held.
4. Found that 10,000 to 11,000 is depleted, not merely that 9,000 to 10,000 is loaded: 1,428 deposits against about 1,900 the profile puts there. A take paid in as two deposits is one deposit fewer above the threshold and one more below it, so the two are the same quantity measured twice.
5. Took each segment's figure as its band surplus and its 10,000 to 11,000 deficit reconciled: 450 for the bank, 150 for transport and courier. Stated to the nearest fifty, which is the granularity the record's own scatter supports.
6. Re-ran the figure over 225 specifications: five windows from 5,000 to 20,000, bin widths of 50 to 500, Poisson, ordinary least squares and log least squares, polynomial orders one to three. The 50-dollar width drops out because every segment has an empty bin at that width, and 84 of the rest are refused by the record, whose surplus below and deficit above they fail to reconcile. **All 141 that stand give the same eight segment figures and the same bank figure of 450**, the closest segment sitting 15.8 deposits clear of its rounding edge.
7. The report states 450 deposits split, transport and courier the largest segment at 150. Transport and courier is neither the largest book (grocery and convenience, 15,131 deposits against 10,433) nor the largest band count (grocery and convenience, 808 against 632): it is the largest because its propensity to split is the highest, which only the estimate shows.

## 4. Deliverable Answers

### structured_cash_deposits_2027.xlsx

1. Deposits split, the bank: 450
2. Largest segment: Transport and courier, 150
3. One row per segment, cash deposits paid in and deposits split, deposits split to the nearest 50:
   - Transport and courier: 10,433 paid in, 150 split
   - Grocery and convenience: 15,131 paid in, 100 split
   - Hospitality: 4,758 paid in, 50 split
   - Trades and construction: 3,168 paid in, 50 split
   - Fuel and automotive: 4,175 paid in, 50 split
   - Personal services: 3,993 paid in, 50 split
   - Rural supply and horticulture: 2,396 paid in, 0 split
   - Clubs and community: 2,718 paid in, 0 split
   - Total: 46,772 paid in, 450 split

### structured_deposits_by_segment.png

1. One bar per segment of the deposits split, in descending order, each labelled with its figure: Transport and courier 150, Grocery and convenience 100, Hospitality 50, Trades and construction 50, Fuel and automotive 50, Personal services 50, Rural supply and horticulture 0, Clubs and community 0.
2. The largest bar, Transport and courier, is marked in the darker colour.

### Also asked

1. Cash count sessions, sessions over the tolerance in force and net variance, by quarter of the reporting year, dollars to the cent:
   - 2026Q3: 1,145 sessions, 117 over tolerance, net variance 17.00
   - 2026Q4: 1,126 sessions, 119 over tolerance, net variance 100.28
   - 2027Q1: 1,081 sessions, 223 over tolerance, net variance -798.74
   - 2027Q2: 1,101 sessions, 238 over tolerance, net variance 944.81
2. Customers raised into the band, lowered into it, and raised into it then moved out again, by risk band:
   - Band 1 (A): 0 raised in, 240 lowered in, 0 raised then out
   - Band 2 (B): 392 raised in, 241 lowered in, 153 raised then out
   - Band 3 (C): 402 raised in, 306 lowered in, 115 raised then out
   - Band 4 (D): 320 raised in, 391 lowered in, 3 raised then out
   - Band 5 (E): 230 raised in, 0 lowered in, 0 raised then out
3. Hours the service log puts the estate out of service, by month, to one decimal:
   - 2026-07: 75.9
   - 2026-08: 91.7
   - 2026-09: 94.0
   - 2026-10: 78.9
   - 2026-11: 56.9
   - 2026-12: 82.5
   - 2027-01: 95.4
   - 2027-02: 134.9
   - 2027-03: 54.2
   - 2027-04: 98.2
   - 2027-05: 72.9
   - 2027-06: 63.2
4. Machines with no service record: 3, being SDM-1455, SDM-1509 and SDM-1562.
5. Sites whose hours differ from the vendor's by more than two: 2, being AR15 and AR19.
