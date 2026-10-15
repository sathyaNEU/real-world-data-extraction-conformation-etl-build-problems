## Tags

**Domain:** Economics & Econometrics (forecasting and forecast evaluation: each import gateway's 2027 formal customs entries forecast at the 2027 network plan's planning exchange rates from the declared values of the shipments the plan carries forward, against the brokerage staffing standard's load of 560 entries a month per broker post).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Place two of the six new broker posts at Dorval and one at Calgary for 2027, and hold the other three to the next review.**
At the 2027 network plan's rates (USD 1.3400, EUR 1.6800) Dorval's second post is placed at a load of 600 against the standard 560, and after it the highest load, Mississauga's 525, is under 560. Not one post at each of the five gateways with one held, which carries the base year's formal entries per shipment onto the plan and so keeps the routing of the base year's exchange rates. Not a post at Mississauga, Richmond or Winnipeg, whose goods invoiced in US dollars fall under the CAD 3,300 line at USD 1.3400.

## 2. Critical Components

1. Forecast average monthly formal entries in 2027 at the plan's rates: Mississauga **3,700**, Dorval **3,600**, Richmond **3,050**, Calgary **2,450**, Winnipeg **1,500**
2. Posts placed in order at loads of **720** (Dorval), **610** (Calgary) and **600** (Dorval) formal entries a month per broker post
3. Loads once the posts are placed: Mississauga **525**, Dorval **515**, Richmond **510**, Calgary **490**, Winnipeg **505**, the highest under **560**, so **3** posts are held

## 3. Step-by-Step Solution

1. Read brk_std_03_brokerage_staffing_standard.pdf section 4 and appendix A: a gateway's load is its forecast average monthly formal entries in 2027 over its broker posts (Mississauga 7, Dorval 5, Richmond 6, Calgary 4, Winnipeg 3 at 1 January 2027, and the posts already placed), the forecast made on the 2027 network plan's shipments and planning assumptions, posts placed one at a time while the highest load exceeds 560.
2. Stacked highvalue_check_2025Q4.csv (the earlier layout, dates DD/MM/YYYY) with highvalue_check_2026Q1.csv, highvalue_check_2026Q2.csv and highvalue_check_2026Q3.csv, an amended shipment once at its later row: 246,894 shipments released from October 2025 to September 2026.
3. Routed each shipment as clr_ops_11_clearance_routing.docx section 3 routes it, at network_plan_2027.xlsx assumption 7's planning rate for its invoice currency (USD 1.3400, EUR 1.6800, GBP 1.8750, CNY 0.18800, JPY 0.0092500) in place of the customs rate of its day, formal when its value for duty at that rate exceeds CAD 3,300 or its goods are under an OGD program: Mississauga 43,058, Dorval 41,853, Richmond 35,134, Calgary 28,835, Winnipeg 17,610 formal entries.
4. Scaled each gateway's count by its 2027 inbound shipments on the plan's Inbound volumes sheet over its October 2025 to September 2026 inbound international shipments in gateway_activity_2024-10_2026-09.csv, and divided by twelve: Mississauga 3,700, Dorval 3,600, Richmond 3,050, Calgary 2,450, Winnipeg 1,500 formal entries a month.
5. Placed posts one at a time as BRK-STD-03 places them, the posts already placed counted: Dorval at 720, Calgary at 610, Dorval at 600; the highest load after those three is Mississauga's 525, under 560, so the other three are held.
6. Took the overtime lines (OT15, OT20, OT1.5, OT2.0) at their hours and the call-backs (CALLB, CB) at the time between their punches from ta_legacy_export_2025-04-01_2025-10-31.csv and ta_export_2025-10-27_2026-09-30.csv (its MIGRATED lines for 27 to 31 October 2025 are the legacy timecards, counted once), each on the desk hr_assignment_changes_2025-04_2026-09.csv gives for the work date, by fiscal quarter: 2,664 hours in fiscal 2025-26.
7. Took each Brandmoor statement's net before tax from ap_invoice_register_brandmoor_2025-04_2026-09.xlsx on the month of the transmissions it bills (the month before its date, as brandmoor_portal_detail_2025-04_2026-03.json shows for every statement it holds), Mississauga's February 2026 transmissions at the statement re-issued on 23 March 2026 (the original reversed by credit memo BCM-2026-00118), each cost centre on its desk in finance_cost_centres_2026.csv: CAD 220,798 in fiscal 2025-26.
8. Place two posts at Dorval and one at Calgary, and hold three to the next review.

## 4. Deliverable Answers

### broker_posts_2027.xlsx

1. New broker posts placed at each gateway for 2027, and held:
   - Mississauga: 0
   - Dorval: 2
   - Richmond: 0
   - Calgary: 1
   - Winnipeg: 0
   - Held to the next review: 3
2. Forecast average monthly formal entries for 2027 (nearest fifty) and formal entries per broker post once the posts are placed (nearest five):
   - Mississauga: 3,700 a month, 525 a post
   - Dorval: 3,600 a month, 515 a post
   - Richmond: 3,050 a month, 510 a post
   - Calgary: 2,450 a month, 490 a post
   - Winnipeg: 1,500 a month, 505 a post
3. Overtime hours worked at each gateway's brokerage desk in each quarter of fiscal 2025-26 (Q1 April to June 2025 through Q4 January to March 2026), nearest hour:
   - Mississauga: Q1 185, Q2 170, Q3 273, Q4 189
   - Dorval: Q1 164, Q2 160, Q3 194, Q4 165
   - Richmond: Q1 113, Q2 124, Q3 144, Q4 107
   - Calgary: Q1 46, Q2 96, Q3 131, Q4 118
   - Winnipeg: Q1 63, Q2 77, Q3 76, Q4 69
4. What Brandmoor charged before tax, desk by desk, for the entries it transmitted in each quarter of fiscal 2025-26, nearest dollar:
   - Mississauga: Q1 $10,849, Q2 $11,483, Q3 $26,554, Q4 $12,342
   - Dorval: Q1 $5,714, Q2 $7,563, Q3 $22,900, Q4 $8,804
   - Richmond: Q1 $6,509, Q2 $6,052, Q3 $18,636, Q4 $9,237
   - Calgary: Q1 $5,877, Q2 $6,964, Q3 $20,054, Q4 $7,052
   - Winnipeg: Q1 $6,241, Q2 $7,074, Q3 $14,924, Q4 $5,970

### establishment_review_2027.pptx

1. Slide 1, titled with the call: each desk's broker posts at 1 January 2027, new posts placed, forecast 2027 formal entries a month and formal entries a month per broker post after the review, Dorval and Calgary highlighted.
2. Slide 2: the overtime hours charted with one bar per desk in each quarter of fiscal 2025-26, each bar labelled with its hours, titled "Mississauga worked the most overtime of the five desks in every quarter of 2025-26".
