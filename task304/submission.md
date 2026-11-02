## Tags

**Domain:** Urban & Regional Science (municipal service demand and resource allocation: a junction safety scheme placed on a county road network).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Ardleshire should bid for the roundabout at Mill Lane Crossroads.** It would prevent 1.3 injury collisions a year, against 1.1 at Tollgate Crossroads. Not Saxby Cross, which had the most collisions in 2021 to 2025 but carries little traffic, so most of its count is the chance that listed it. Not Tollgate Crossroads, which carries the most traffic but whose own record runs well below what its traffic predicts.

## 2. Critical Components

1. Mill Lane Crossroads's expected injury collisions a year as it stands, at its 2026 traffic: **2.7**.
2. Mill Lane Crossroads's benefit (crossroads factor 0.52): **1.3** injury collisions prevented a year.
3. Tollgate Crossroads, the runner-up: **1.1** a year.

## 3. Step-by-Step Solution

1. Took the listed junctions from network_screening_2026.pdf (give-way or stop-controlled junctions with 12 or more injury collisions in 2021 to 2025) and their layout, control and traffic by year from junction_inventory_2026.xlsx.
2. Counted injury collisions by junction node and year for 2021 to 2025 in collision_records_2016_2025.csv, for every give-way or stop-controlled T, staggered and crossroads junction in the inventory (1,436 junctions, zero years included).
3. Fitted a negative binomial safety performance function to those junction-years (log of major and minor road traffic, layout and year terms): overdispersion 0.26.
4. Combined each listed junction's own 2021 to 2025 count with its predicted count by empirical Bayes (weight 1 / (1 + overdispersion x predicted five-year count) on the prediction) and carried the result to the junction's 2026 traffic at the window's average year level: Mill Lane Crossroads 2.7 a year.
5. Multiplied by one less the crash modification factor for each layout in Table 2 of junction_safety_fund_guidance_2027.pdf: Mill Lane Crossroads 1.3 prevented a year, Tollgate Crossroads 1.1.
6. For Annex A, read the old system's 2026 collisions and casualties to May and the new system's JSON export from June, kept each collision the migration re-sent once (the new record on the same date and road within 20 minutes and 40 metres of an old one replaces it), applied the 30-day deaths in fatal_casualty_notifications_2026.xlsx matched on date, road, time and casualty, and left out the trunk sections in road_network_register_2026.csv by road and easting.
7. Took a collision's severity from its most severely injured casualty and each casualty's road user from casualty_type (old system) or class and the vehicle they were in (new system), by quarter of the collision date.
8. Placed the roundabout at the junction with the largest benefit: Mill Lane Crossroads.

## 4. Deliverable Answers

### junction_bid_2027.docx

1. The junction: Mill Lane Crossroads.
2. Injury collisions a roundabout would prevent each year, every listed junction:
   - Mill Lane Crossroads: 1.3
   - Tollgate Crossroads: 1.1
   - Church Street Junction: 0.9
   - Saxby Cross: 0.8
   - Coppice Way Junction: 0.5
   - Fen Lane Junction: 0.4
3. Bar chart of those benefits by junction in Figure 1, Mill Lane Crossroads's bar marked as the junction chosen.

### bid_annex_2026.xlsx

1. Injury collisions on the county's roads in 2026 by quarter and severity (A1):
   - Q1 (January to March): fatal 15; serious 142; slight 477
   - Q2 (April to June): fatal 10; serious 158; slight 472
   - Q3 (July to September): fatal 11; serious 150; slight 492
2. Their casualties in 2026 by quarter and road user (A2):
   - Q1 (January to March): pedestrians 91; pedal cyclists 71; motorcyclists 73; car occupants 472
   - Q2 (April to June): pedestrians 95; pedal cyclists 47; motorcyclists 56; car occupants 462
   - Q3 (July to September): pedestrians 100; pedal cyclists 56; motorcyclists 55; car occupants 511
