# task184 submission

## Tags

**Domain:** Urban & Regional Science, transport infrastructure operations (posting a national aviation screening agency's mobile screening unit to one of eight airports against a checkpoint wait standard).
**Analytical objective:** Anomaly Detection & Diagnostics (which flagged airport's queue breach the unit can actually relieve, separating the lanes it brings from the lanes its host stands down).

## 1. Final Recommendation

**Post the mobile screening unit to Halloran Bay from 15 June to 31 August 2027.**

There it moves 382,700 passengers within the 20-minute standard, against 237,700 at Cullinvale, the next best posting, and 14 per cent is the smallest whole per cent shortfall in Halloran Bay's forecast passengers at which another posting would move more. Not Cullinvale, which leads only when the unit's three lanes are added to its roster pattern: on every posted day last summer its duty managers, like every host but Halloran Bay, stood down two of their own lanes for the whole of the unit's day. Not Eskerford, which leads only when Halloran Bay's stand-down, all of it after its banks, is spread over the day.

## 2. Critical Components

1. On every posted day last summer each host except Halloran Bay stood down **2** of its own lanes from 05:00 to 21:00, so the unit adds **1** lane at their banks and **3** at Halloran Bay's, where none were stood down through the banks.
2. Halloran Bay's posting moves **382,700** passengers within the standard over the summer.
3. Cullinvale's, the runner-up, moves **237,700**.
4. The smallest whole per cent shortfall in Halloran Bay's forecast passengers at which another posting (Cullinvale) moves more is **14 per cent**.

## 3. Step-by-Step Solution

1. Counted each host's own lanes screening in every 15 minutes of its posted days (mobile_unit_postings_2026.csv) in checkpoint_lane_counts_20260615_20260831.csv, lanes M1 to M3 apart, against roster_plan_summer2026.csv: the same stand-down on every posted day, 2 lanes from 05:00 to 21:00 at seven hosts and none through Halloran Bay's banks, more after the banks at every host.
2. Took each airport's lanes with the unit there as roster_pattern_summer2027.xlsx less that stand-down by interval, plus the unit's 3 lanes from 05:00 to 21:00 (mobile_screening_unit_deployment_policy_2027.pdf).
3. Ran checkpoint_planning_standard_2026.pdf sections 4 and 6 on the three design days of summer2027_planning_sheet.xlsx without and with the unit and multiplied each day's difference by 16, 31 and 31 days: Halloran Bay 382,700, Cullinvale 237,700, every other airport less.
4. Cut Halloran Bay's design-day arrivals uniformly a whole per cent at a time: 14 per cent is the smallest cut at which its posting moves fewer passengers than Cullinvale's.
5. Summed pax_screened in the lane feed by airport over the passenger lanes and the unit's, leaving out the two lanes at each checkpoint that screen only before 05:00 and after 21:00, the staff and aircrew search the deployment policy describes, which the operators' returns in operator_traffic_returns_2026.csv do not include.
6. Divided each airport's invoice and credit-note amounts in hotel_invoices_CC4109_summer2026.xlsx, matched to postings by purchase order, by the officer-nights on its accommodation lines, each stay's nights counted once.
7. Counted each line of expense_claims_CC4109_2026.csv once by claim reference and line, assigned each claim to the posting week its subsistence days fall in, and divided each airport's total by its posting weeks.
8. Posted the unit to Halloran Bay.

## 4. Deliverable Answers

### mobile_team_posting_summer_2027.pdf

1. Post the mobile screening unit to Halloran Bay for 15 June to 31 August 2027.
2. Passengers the unit would move within the 20-minute standard over the summer, nearest hundred:
   - Halloran Bay: 382,700
   - Cullinvale: 237,700
   - Eskerford: 195,200
   - Faranloe: 187,200
   - Brennagh: 186,300
   - Dromkeel: 184,100
   - Ardcarrig: 180,900
   - Glenkessan: 166,600
3. Smallest whole per cent shortfall in Halloran Bay's forecast passengers at which another posting (Cullinvale) moves more: 14 per cent.
4. Bar chart of the passengers the unit would move at each airport over the summer on page 1, Halloran Bay marked.

### mobile_team_effect_2027.xlsx

1. The eight airports' summer figures and the 14 per cent smallest shortfall, as in the memo.
2. Passengers screened at each airport from 15 June to 31 August 2026 (passenger lanes and the unit's), nearest hundred:
   - Halloran Bay: 616,000
   - Cullinvale: 1,299,100
   - Eskerford: 890,200
   - Faranloe: 1,058,700
   - Brennagh: 757,600
   - Dromkeel: 866,300
   - Ardcarrig: 1,125,900
   - Glenkessan: 641,000
3. Hotel cost per officer-night of last summer's postings, euros to the cent:
   - Halloran Bay: EUR 112.98
   - Cullinvale: EUR 116.72
   - Eskerford: EUR 98.50
   - Faranloe: EUR 90.30
   - Brennagh: EUR 84.70
   - Dromkeel: EUR 95.40
   - Ardcarrig: EUR 110.01
   - Glenkessan: EUR 93.73
4. The unit's expense claims per posting week last summer, euros to the cent:
   - Halloran Bay: EUR 8,091.04
   - Cullinvale: EUR 7,135.92
   - Eskerford: EUR 8,163.34
   - Faranloe: EUR 7,991.56
   - Brennagh: EUR 8,247.46
   - Dromkeel: EUR 8,824.96
   - Ardcarrig: EUR 7,339.69
   - Glenkessan: EUR 8,724.60
