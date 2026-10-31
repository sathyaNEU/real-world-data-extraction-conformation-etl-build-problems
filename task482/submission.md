## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a self-insured employer dental plan's 2027 annual maximum costed for collective bargaining, conformed from its claims administrator's two adjudication platforms, predetermination logs, eligibility spans, member crosswalk and network fee schedules).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Agree a 2,000 dollar annual maximum for 2027, not the union's 3,000.**
Costed under Finance Policy F-17, the 2,000 dollar maximum adds USD 1.55 per covered person month (USD 37.36 against USD 35.81 at the current 1,500), inside Board Resolution 2026-31's USD 1.90, and 3,000 dollars adds USD 2.34, over it. The 2025 claims alone put 3,000 dollars at USD 1.23, because 103 members whose predetermination showed the 1,500 dollar maximum reducing the plan's payment had that work done only after the plan year began again on 1 January 2026; at a higher maximum the work falls in the plan year, USD 94,459.50 of plan share at the 2027 fees, and 3,000 dollars no longer fits.

## 2. Critical Components

1. 2027 cost per covered person month under F-17 (the 2025 plan year at the 2027 fees): 1,500 dollars **USD 35.81**, 2,000 dollars **USD 37.36**, 3,000 dollars **USD 38.15**.
2. Increase over the current 1,500 dollar design against the mandate's USD 1.90: 2,000 dollars **USD 1.55**, 3,000 dollars **USD 2.34**.
3. Predetermined work put off past 31 December 2025 and costed in the plan year: **103** members, **USD 94,459.50** of plan share at the 2027 fees.
4. The 2025 plan year: **6,934** covered persons, **76,380** covered person months.

## 3. Step-by-Step Solution

1. Conformed Ridgeline's two platforms: Classic voided originals out and replacements in, Nexus superseded lines out, a Classic claim restated on Nexus taken from the restatement, every member through the July 2025 crosswalk.
2. Took 2025's covered persons and covered person months from both eligibility files (Classic spans to 30 June 2025, its open end written 12/31/9999; Nexus spans from 1 July 2025, an open end blank).
3. Priced each 2025 service line at the 2027 fee sheet with the deductible the plan applied to it and its class's coinsurance, frequency-denied lines out and the lines the maximum cut at their full share.
4. Marked the 2025 predetermination requests whose estimated plan payment the maximum reduced (Nexus stamps read in Central time).
5. Added to each person the estimated procedures of those requests not claimed for the same person, procedure and tooth in 2025 and claimed after 1 January 2026 within the estimate's 12 months, at the 2027 fee and coinsurance.
6. Costed each maximum as the sum over 2025's covered persons of the lesser of the person's amount (with that work at a higher maximum) and the maximum, per covered person month, each increase against 1,500 at the same fees.
7. Counted Schedule C requests by quarter of receipt (after 5:00 p.m. Central or on a non-business day, the next business day; a Nexus request every estimate for one member and dentist at one receipt time, answered at its last estimate) and those answered within five business days.
8. Followed each child's orthodontic treatment across a change of orthodontist through the crosswalk, its year from the first banding, and summed the unpaid benefit of children in treatment and covered on 30 September 2026.

## 4. Deliverable Answers

### pembrook_dental_member_year_2025.csv

1. One row per 2025 covered person: **6,934** rows, **76,380** covered person months.
2. Column totals in dollars: put-off work at the 2027 fees **USD 94,459.50**; cost at 1,500 **USD 2,735,231.20**, at 2,000 **USD 2,853,526.70**, at 3,000 **USD 2,914,027.70**.

### pembrook_dental_maximum_2027.pdf

1. Recommendation: agree a 2,000 dollar maximum from 1 January 2027.
2. Cost per covered person month: USD 35.81 (1,500), USD 37.36 (2,000), USD 38.15 (3,000); increases USD 1.55 and USD 2.34 against the USD 1.90 limit.
3. Predetermination requests by quarter of receipt, received and answered within five business days:
   - 2025Q1 (January to March 2025): 322 received, 313 answered within five business days
   - 2025Q2 (April to June 2025): 254 received, 228 answered within five business days
   - 2025Q3 (July to September 2025): 301 received, 192 answered within five business days
   - 2025Q4 (October to December 2025): 169 received, 140 answered within five business days
   - 2026Q1 (January to March 2026): 326 received, 296 answered within five business days
   - 2026Q2 (April to June 2026): 292 received, 279 answered within five business days
   - 2026Q3 (July to September 2026): 195 received, 177 answered within five business days
4. Orthodontic treatment by the year it began, children still in treatment on 30 September 2026 and the plan's payments still owed for them:
   - 2024: 1 child, USD 310.41
   - 2025: 39 children, USD 16,590.05
   - 2026: 43 children, USD 41,200.84

### pembrook_dental_maximum_2027.svg

1. Bar chart of each option's increase per covered person month, USD 1.55 at 2,000 dollars and USD 2.34 at 3,000 dollars, against a dashed line at the mandate's USD 1.90: the 2,000 bar falls under the line and the 3,000 bar rises over it.
