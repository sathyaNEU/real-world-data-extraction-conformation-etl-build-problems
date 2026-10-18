**Domain:** Banking, Credit & Financial Risk, fraud and AML detection.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Kelverstone Mutual should set Castlegate Payments' scam incidence index at 31 scam cases per million
payments sent for the indemnity year beginning 1 October 2027.**
The index rests on 688 indexed cases on 22,233,300 payments sent, against the 400 cases Castlegate's own
register holds. Not the two-source estimate run on every one of its 395 register matches, which counts its
own fund-return requests coming back to it as second sightings of its own cases. Not a rule on the
registration date, which cannot tell a sighting another firm's victim produced from one Castlegate's own
request produced.

## 2. Critical Components

1. Scam cases Castlegate's own register holds for the scheme year to 31 March 2027: **400**
2. Its payments that match an account on the scheme register: **395**
3. Those matches that a fund-return request of its own preceded: **125**
4. Sightings its own action cannot have produced: **270**, of which **157** are also in its own register
5. Cases its own record did not hold: **288**

## 3. Step-by-Step Solution

1. Took the index's definition from indemnity_standard_v6.pdf: cases arising from payments the
   member's own customers sent in the scheme year to 31 March 2027, whether or not its systems
   recorded them, per million payments sent on its revised return, estimated on the evidence base as
   it stands when the review is prepared.
2. Counted Castlegate's scam reimbursement cases for 2026/27 in case_register_2024_27.csv: 400.
3. Summed its revised 2026/27 quarters in member_quarterly_returns.xlsx: 22,233,300 payments sent.
4. Took its payments matching an account on mule_account_register.csv from member_payment_matches.csv:
   395 matches.
5. Attributed each match through fund_return_requests.csv: 125 were registered on or after a fund-return
   request Castlegate had already sent on that payment, so they are its own case coming back rather than a
   second sighting of it.
6. Estimated the cases its customers suffered from the two sightings that do not depend on each other, its
   own register and the 270 registrations no request of its own preceded, 157 of which it also holds:
   400 x 270 / 157 = 688 cases, 30.94 per million payments.
7. Walked its register to the index: 400 recorded, 288 its own record did not hold, 688 indexed.
8. Set the index at 31 scam cases per million payments sent, and indexed the other three members of the
   review group on the same basis.

## 4. Deliverable Answers

### member_incidence_review.xlsx

1. Scam incidence index for each review-group member, cases per million payments sent, nearest case:
   - Castlegate Payments (KM-104): 31, on 400 recorded and 688 indexed cases
   - Saltmarch Pay (KM-112): 22, on 109 recorded and 139 indexed cases
   - Trentmoor Money (KM-108): 15, on 246 recorded and 301 indexed cases
   - Brindlemere Remit (KM-101): 12, on 443 recorded and 517 indexed cases
2. Castlegate's walk from its recorded cases to its index, one line per reconciling item, whole cases:
   - Cases Castlegate's own register holds: 400
   - Cases its own record did not hold: 288
   - Indexed cases: 688
3. Bar chart of recorded against indexed incidence for the four review-group members on the incidence
   chart sheet, ordered by the indexed figure, Castlegate marked and annotated, titled on the finding
   that its own record holds under three in five of the cases its customers suffered.
4. Indemnity paid on unauthorised fraud by member tier for each 2026/27 quarter, GBP to the nearest
   pound, each quarter total taken from the unrounded tier amounts:
   - Q1 tier A: 311,088; tier B: 271,791; tier C: 81,499; quarter total: 664,379
   - Q2 tier A: 309,882; tier B: 228,966; tier C: 83,191; quarter total: 622,039
   - Q3 tier A: 317,029; tier B: 222,673; tier C: 75,171; quarter total: 614,872
   - Q4 tier A: 339,633; tier B: 181,104; tier C: 75,823; quarter total: 596,560
5. Cases notified in the quarter to 30 June 2027 and the value reported, per member, GBP to the nearest
   pound:
   - Brindlemere Remit (KM-101): 193 cases, 460,362
   - Oakhanger Transfer (KM-102): 121 cases, 285,422
   - Wrenhall Pay (KM-103): 60 cases, 153,760
   - Castlegate Payments (KM-104): 109 cases, 307,226
   - Quayfield Remit (KM-106): 64 cases, 135,016
   - Trentmoor Money (KM-108): 111 cases, 243,325
   - Vellowe Pay (KM-110): 93 cases, 301,939
   - Saltmarch Pay (KM-112): 28 cases, 72,566
   - Pelbury Exchange (KM-115): 15 cases, 26,336
   - Netherby Pay (KM-118): 37 cases, 94,158
   - Thrimby Money (KM-121): 24 cases, 53,735
   - Garnock Exchange (KM-124): 101 cases, 231,542
6. Share of reimbursement recovered by route on cases closed in each 2025/26 quarter, from the
   case-level credits, per cent to one decimal, with each route's total over those four quarters:
   - Q1 beneficiary recall: 6.5; repatriation: 3.4; insurer contribution: 2.8
   - Q2 beneficiary recall: 15.1; repatriation: 3.3; insurer contribution: 3.8
   - Q3 beneficiary recall: 8.5; repatriation: 2.5; insurer contribution: 5.9
   - Q4 beneficiary recall: 5.4; repatriation: 2.5; insurer contribution: 7.4
   - Route totals over those four quarters, beneficiary recall: 8.5; repatriation: 2.7; insurer
     contribution: 6.0

### incidence_index_2027_28.csv

1. One row per review-group member, ordered by the index, cases per million payments sent:
   - KM-104, Castlegate Payments, 31
   - KM-112, Saltmarch Pay, 22
   - KM-108, Trentmoor Money, 15
   - KM-101, Brindlemere Remit, 12
