## Tags

**Domain:** Urban and regional science (transportation network planning).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Put the Center Street Bridge widening (TIP-28-009) forward for the FY2028 TIP's congestion-relief slot: with the 2028 peak-hour trips re-assigned to equilibrium on each build network it saves 323,000 vehicle-hours a year, 8,300 per million dollars.**
Not the Route 9 Millbrook auxiliary lane (159,000, 3,400 per million), which saves the most when its own links are re-timed at the no-build volumes, but once trips re-route its extra lane feeds the Route 9 bridge, which binds, while the Center Street lane draws trips off Route 9. Not the Southport signal and turn-lane package (126,000, 4,900 per million) or the Ferry Street exit ramp (37,000, 2,100 per million).

## 2. Critical Components

1. The Center Street Bridge widening saves **323,000** vehicle-hours a year
2. The Route 9 Millbrook auxiliary lane saves **159,000** vehicle-hours a year once trips re-route
3. The Center Street Bridge widening saves **8,300** vehicle-hours a year per million dollars

## 3. Step-by-Step Solution

1. Built the directed network from the two-way records in MAMPO_v42_subarea_links_2028NB.csv (capacity is each direction's lanes times Table 4.2's capacity per lane, times by Table 4.2's volume-delay functions) and coded each candidate's change from the Model coding sheet of FY2028_TIP_congestion_relief_candidates.xlsx: the Center Street Bridge widening is the largest change in the region's peak-hour vehicle-hours.
2. Assigned the AM and PM tables in MAMPO_v42_subarea_trips_2028.csv to user equilibrium (relative gap below 0.000001, documentation 6.1) on the no-build network and on each build network, and annualised each reduction per scoring guidance 2.2 (times 247 times 2.9): Center Street 323,000, Route 9 159,000, Southport 126,000, Ferry Street 37,000 vehicle-hours a year.
3. Divided by each candidate's year-of-expenditure cost in the Candidates sheet: Center Street 8,300, Southport 4,900, Route 9 3,400, Ferry Street 2,100 vehicle-hours per million dollars.
4. For the count stations (ATR_hourly_volumes_2025.csv, S-0103R continuing S-0103), an hour is a true count only when both directions answered with status OK, it is not the first answered poll after a missed one inside a running day (the station's counters carry the missed hours' vehicles into it), and the direction is outside a fault: from the first hour its share of the two-way traffic steps away from its usual share for that hour of the week through the day of the loop or detector card work order in the Maintenance 2025 sheet of ATR_station_inventory_2025.xlsx; valid days and the K-factor's hours follow manual 4.1 to 4.3, giving the AADT and K-factors in block 4.
5. For the validation, converted VOL_PCE in MAMPO_v42_base2025_station_volumes.csv to vehicles with HV_PCT (documentation 6.3) and compared it with the mean count at hour ending 8 (AM) and 18 (PM) over the valid Tuesdays to Thursdays of March to May and September to October 2025 (documentation 6.4), giving the percentages in block 4.
6. The slot goes to the largest annual benefit (scoring guidance 3.1): the Center Street Bridge widening.

## 4. Deliverable Answers

### mampo_tip2028_project_ranking.xlsx

1. Annual benefit and benefit per million dollars, each candidate (vehicle-hours a year to the nearest 1,000; vehicle-hours per USD 1 million to the nearest 100):
   - TIP-28-009 Center Street Bridge widening: 323,000; 8,300
   - TIP-28-014 Route 9 Millbrook auxiliary lane: 159,000; 3,400
   - TIP-28-030 Southport corridor signal and turn-lane package: 126,000; 4,900
   - TIP-28-021 Ferry Street exit ramp widening: 37,000; 2,100
2. The recommended project: TIP-28-009, Center Street Bridge widening.
3. 2025 AADT (whole vehicles) and K-factor (three decimals), each permanent station:
   - S-0101 Route 9, Ashkettle Bridge: AADT 77,018; K 0.126
   - S-0102 Center Street Bridge: AADT 12,021; K 0.125
   - S-0103 Southport Bridge: AADT 19,396; K 0.138
   - S-0104 Route 9 at Millbrook: AADT 54,773; K 0.113
   - S-0105 Route 9 south of Lakeview Road: AADT 36,800; K 0.112
   - S-0106 Millbrook Road at Quarry Lane: AADT 15,291; K 0.139
   - S-0107 Harbor Avenue at Dock Street: AADT 13,859; K 0.115
   - S-0108 Lakeview Parkway east of Harbor Avenue: AADT 10,188; K 0.115
4. 2025 base-year validation, model less count as a percentage of the count (one decimal):
   - S-0101 Route 9, Ashkettle Bridge eastbound AM peak hour: -5.5
   - S-0101 Route 9, Ashkettle Bridge eastbound PM peak hour: -5.8
   - S-0101 Route 9, Ashkettle Bridge westbound AM peak hour: -13.3
   - S-0101 Route 9, Ashkettle Bridge westbound PM peak hour: -13.1
   - S-0102 Center Street Bridge eastbound AM peak hour: 0.0
   - S-0102 Center Street Bridge eastbound PM peak hour: -0.6
   - S-0102 Center Street Bridge westbound AM peak hour: -2.6
   - S-0102 Center Street Bridge westbound PM peak hour: -1.2
   - S-0103 Southport Bridge eastbound AM peak hour: -0.1
   - S-0103 Southport Bridge eastbound PM peak hour: 0.5
   - S-0103 Southport Bridge westbound AM peak hour: 2.2
   - S-0103 Southport Bridge westbound PM peak hour: 1.5

### mampo_tip2028_executive_brief.pptx

1. Recommendation: put the Center Street Bridge widening forward, 323,000 vehicle-hours a year, 8,300 per million dollars.
2. Bar chart of the four candidates' annual benefits on slide 1, Center Street highlighted.
