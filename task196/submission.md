**Domain:** Banking, Credit & Financial Risk, fraud and AML detection.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Kelverstone Mutual should set Castlegate Payments' scam incidence index at 31 scam cases per million
payments sent for the indemnity year beginning 1 October 2027.**
The index rests on 688 indexed cases on the two-source estimate, 400 x 270 / 157, on 22,233,300
payments sent, against the 400 cases Castlegate's own register holds. Not the two-source estimate run
on every one of its 395 register matches, which counts its own fund-return requests coming back to it
as second sightings of its own cases. Not a rule on the
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
5. Attributed each match to a cause through fund_return_requests.csv: on 125 of them Castlegate had
   already asked the receiving firm for the money back, so the firm's registration answers Castlegate's
   own request and the match is its own case coming back rather than a second sighting of it. The
   remaining 270 are sightings its own action cannot have caused.
6. Estimated the cases its customers suffered from the two sightings that do not depend on each other, its
   own register and the 270 registrations no request of its own preceded, 157 of which it also holds:
   400 x 270 / 157 = 688 cases, 30.94 per million payments.
7. Walked its register to the index in index units, which every licensed form of the estimate gives
   alike: 18 recorded, 13 its own record did not hold, 31 indexed, per million payments sent. The
   whole-case counts behind them move with the form, so a count is read inside 686 to 689 indexed and
   286 to 289 not held for Castlegate, 138 to 139 for Saltmarch, 300 to 302 for Trentmoor and 516 to
   517 for Brindlemere, while the index is exact.
8. Set the index at 31 scam cases per million payments sent, and indexed the other three members of the
   review group on the same basis.

## 4. Deliverable Answers

### member_incidence_review.xlsx

1. Scam incidence index for each review-group member, cases per million payments sent, nearest case,
   each indexed count on the two-source estimate of the cases the member recorded against the register
   sightings no fund-return request of its own preceded:
   - Castlegate Payments (KM-104): 31, on 400 recorded and 688 indexed cases
   - Saltmarch Pay (KM-112): 22, on 109 recorded and 139 indexed cases
   - Trentmoor Money (KM-108): 15, on 246 recorded and 301 indexed cases
   - Brindlemere Remit (KM-101): 12, on 443 recorded and 517 indexed cases
2. Castlegate's walk from its recorded incidence to the one to plan on, one line per reconciling item,
   cases per million payments sent, nearest whole case:
   - Incidence its own register holds: 18
   - Incidence its own record did not hold: 13
   - Indexed incidence: 31
3. Bar chart of recorded against indexed incidence for the four review-group members on the incidence
   chart sheet, ordered by the indexed figure, Castlegate marked and annotated, titled on the finding
   that its own record holds under three in five of the cases its customers suffered.
4. Indemnity the advices settled on unauthorised fraud, by member tier and the 2026/27 quarter each
   case closed in, GBP to the pound, each quarter total taken from the unrounded tier amounts:
   - Q1 tier A: 389,667; tier B: 390,380; tier C: 204,473; quarter total: 984,521
   - Q2 tier A: 349,939; tier B: 277,918; tier C: 101,820; quarter total: 729,677
   - Q3 tier A: 343,190; tier B: 237,744; tier C: 92,670; quarter total: 673,605
   - Q4 tier A: 339,633; tier B: 181,104; tier C: 75,823; quarter total: 596,560
5. Distinct cases notified in the quarter to 30 June 2027, the 2027/28 first quarter, counted once
   each, and the value reported, per member, GBP to the pound:
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
6. Share of scam reimbursement recovered by route on cases from 2025/26 payments closed in each
   2025/26 quarter, from every case-level credit, per cent to one decimal, with each route's total over
   those four quarters:
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
