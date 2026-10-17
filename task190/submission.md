**Domain:** Banking, Credit & Financial Risk (fraud and AML detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The annual report should state that 400 cash deposits were split below the prescribed transaction threshold in the year ended 30 June 2027.**
Transport and courier is the largest segment at 90, ahead of trades and construction at 70. Not the 1,223 the same-day screen gives, which counts the band deposits of every business that pays its takings in more than once a day. Not the 3,520 deposits the band holds, which is mostly ordinary takings of that size. Not the 370 one profile fitted to the whole book gives, which the book's own residuals away from the band reject.

## 2. Critical Components

1. Cash deposits of 9,000 or more and below 10,000 paid in during the year: **3,520**
2. Deposits split, by segment: transport and courier **90**, trades and construction **70**, grocery and convenience **60**, hospitality **60**, clubs and community **30**, fuel and automotive **30**, personal services **30**, rural supply and horticulture **30**
3. Cash deposits paid in during the year, all amounts: **45,302**

## 3. Step-by-Step Solution

1. Joined both deposit feeds to the customer register through `customer_number_crosswalk.csv` and took each customer's segment from `business_customer_register.xlsx`, reading the April 2027 code reissue as the same eight segments per handbook paragraph 7.5.
2. Kept physical cash deposits paid in between 1 July 2026 and 30 June 2027, excluding the two reversed deposits and their reversing rows, converting the machine feed's UTC stamps to branch local dates and collapsing its re-sent rows: 45,302 deposits.
3. Counted the deposits paragraph 7.4 asks about, at 9,000 or more and below 10,000: 3,520.
4. Read each segment's own deposit-size profile either side of the band, in equal steps across the range the segment's record is log-linear over.
5. Fitted the profile on the steps either side of the band and took the deposits the band holds over the number the profile puts there: 400 for the bank, 90 for transport and courier.
6. Checked the reading against every other window and step width inside that range: each gives the same eight segment figures.
7. The report states 400 deposits split, transport and courier the largest segment at 90.

## 4. Deliverable Answers

### structured_cash_deposits_2027.xlsx

1. Deposits split, the bank: 400
2. Largest segment: Transport and courier, 90
3. One row per business segment, cash deposits paid in and deposits split, deposits split to the nearest 10:
   - Transport and courier: 3,223 paid in, 90 split
   - Trades and construction: 4,755 paid in, 70 split
   - Grocery and convenience: 12,138 paid in, 60 split
   - Hospitality: 10,592 paid in, 60 split
   - Clubs and community: 2,301 paid in, 30 split
   - Fuel and automotive: 5,995 paid in, 30 split
   - Personal services: 3,094 paid in, 30 split
   - Rural supply and horticulture: 3,204 paid in, 30 split
   - Total: 45,302 paid in, 400 split

### structured_deposits_by_segment.png

1. One bar per segment of the deposits split, in descending order, each labelled with its figure: Transport and courier 90, Trades and construction 70, Grocery and convenience 60, Hospitality 60, Clubs and community 30, Fuel and automotive 30, Personal services 30, Rural supply and horticulture 30.
2. The largest bar, Transport and courier, is marked in the darker colour.

### Also asked

1. Cash count sessions, sessions over the tolerance in force and net variance, by quarter, dollars to the cent:
   - 2026Q3: 1,061 sessions, 125 over tolerance, net variance -354.67
   - 2026Q4: 1,052 sessions, 116 over tolerance, net variance -554.18
   - 2027Q1: 998 sessions, 205 over tolerance, net variance -511.41
   - 2027Q2: 1,005 sessions, 210 over tolerance, net variance -80.38
2. Customers raised into the band, lowered into it, and raised into it then moved off it, by risk band:
   - Band 1 (A): 0 raised in, 261 lowered in, 0 raised then off
   - Band 2 (B): 462 raised in, 225 lowered in, 105 raised then off
   - Band 3 (C): 345 raised in, 236 lowered in, 62 raised then off
   - Band 4 (D): 322 raised in, 251 lowered in, 59 raised then off
   - Band 5 (E): 336 raised in, 0 lowered in, 69 raised then off
3. Hours the machine estate was out of service, by month, to one decimal:
   - 2026-07: 56.3
   - 2026-08: 47.5
   - 2026-09: 68.4
   - 2026-10: 44.5
   - 2026-11: 44.2
   - 2026-12: 59.4
   - 2027-01: 61.2
   - 2027-02: 52.7
   - 2027-03: 52.4
   - 2027-04: 54.2
   - 2027-05: 56.5
   - 2027-06: 67.6
4. Machines with no service record: 3, being SDM-09-1, SDM-25-1 and SDM-28-1.
5. Sites whose hours differ from the vendor's by more than two: 2, being AR04 and AR18.
