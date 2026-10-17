**Domain:** Banking, Credit & Financial Risk (fraud and AML detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The annual report should state that 400 cash deposits were split below the prescribed transaction threshold in the year ended 30 June 2027.**
Transport and courier is the largest segment at 90, ahead of trades and construction at 70. Not the 2,196 deposits the band holds, which is mostly ordinary takings of that size. Not the 1,287 a same-day screen gives, which counts the band deposits of every business that pays its takings in more than once a day. Not the 1,406 from judging each customer against its own prior year.

## 2. Critical Components

1. Cash deposits of 9,000 or more and below 10,000 paid in during the year: **2,196**
2. Deposits split, by segment: transport and courier **90**, trades and construction **70**, grocery and convenience **60**, hospitality **60**, clubs and community **30**, fuel and automotive **30**, personal services **30**, rural supply and horticulture **30**
3. Cash deposits paid in during the year, all amounts: **44,964**

## 3. Step-by-Step Solution

1. Joined both deposit feeds to the customer register through `customer_number_crosswalk.csv` and took each customer's segment from `business_customer_register.xlsx`, reading the April 2027 code reissue as the same eight segments per handbook paragraph 7.5.
2. Kept physical cash deposits paid in between 1 July 2026 and 30 June 2027, excluding the two reversed deposits and their reversing rows, converting the machine feed's UTC stamps to branch local dates and collapsing its re-sent rows: 44,964 deposits.
3. Counted the deposits paragraph 7.4 asks about, at 9,000 or more and below 10,000: 2,196.
4. Read each segment's own deposit-size profile either side of the band, in equal steps across the range the record covers.
5. Fitted the profile on the steps either side of the band and took the deposits the band holds over the number the profile puts there: 400 for the bank, 90 for transport and courier.
6. Checked the reading against every window, step width and fit family the record supports: each gives the same eight segment figures.
7. The report states 400 deposits split, transport and courier the largest segment at 90.

## 4. Deliverable Answers

### structured_cash_deposits_2027.xlsx

1. Deposits split, the bank: 400
2. Largest segment: Transport and courier, 90
3. One row per segment, cash deposits paid in and deposits split, deposits split to the nearest 10:
   - Transport and courier: 2,300 paid in, 90 split
   - Trades and construction: 3,684 paid in, 70 split
   - Grocery and convenience: 14,111 paid in, 60 split
   - Hospitality: 11,297 paid in, 60 split
   - Clubs and community: 1,836 paid in, 30 split
   - Fuel and automotive: 6,658 paid in, 30 split
   - Personal services: 2,036 paid in, 30 split
   - Rural supply and horticulture: 3,042 paid in, 30 split
   - Total: 44,964 paid in, 400 split

### structured_deposits_by_segment.png

1. One bar per segment of the deposits split, in descending order, each labelled with its figure: Transport and courier 90, Trades and construction 70, Grocery and convenience 60, Hospitality 60, Clubs and community 30, Fuel and automotive 30, Personal services 30, Rural supply and horticulture 30.
2. The largest bar, Transport and courier, is marked in the darker colour.

### Also asked

1. Cash count sessions, sessions over the tolerance in force and net variance, by quarter, dollars to the cent:
   - 2026Q3: 1,145 sessions, 117 over tolerance, net variance 17.00
   - 2026Q4: 1,126 sessions, 119 over tolerance, net variance 100.28
   - 2027Q1: 1,081 sessions, 223 over tolerance, net variance -784.53
   - 2027Q2: 1,101 sessions, 240 over tolerance, net variance 869.81
2. Customers raised into the band, lowered into it, and raised into it then moved out again, by risk band:
   - Band 1 (A): 0 raised in, 276 lowered in, 0 raised then out
   - Band 2 (B): 470 raised in, 243 lowered in, 153 raised then out
   - Band 3 (C): 338 raised in, 270 lowered in, 92 raised then out
   - Band 4 (D): 291 raised in, 492 lowered in, 89 raised then out
   - Band 5 (E): 370 raised in, 0 lowered in, 96 raised then out
3. Hours the service log puts the estate out of service, by month, to one decimal:
   - 2026-07: 58.6
   - 2026-08: 87.1
   - 2026-09: 74.0
   - 2026-10: 75.3
   - 2026-11: 64.7
   - 2026-12: 116.4
   - 2027-01: 54.1
   - 2027-02: 103.0
   - 2027-03: 64.8
   - 2027-04: 92.8
   - 2027-05: 53.2
   - 2027-06: 66.3
4. Machines with no service record: 3, being SDM-1455, SDM-1509 and SDM-1562.
5. Sites whose hours differ from the vendor's by more than two: 2, being AR15 and AR19.
