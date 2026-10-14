# task184 submission

## Tags

**Domain:** Urban & Regional Science, transport infrastructure operations (posting a national aviation screening agency's mobile screening unit to one of eight airports against a checkpoint wait standard).
**Analytical objective:** Anomaly Detection & Diagnostics (which flagged airport's queue breach the unit can actually relieve, once the lanes a checkpoint really opens are told apart from the lanes its roster pattern plans).

## 1. Final Recommendation

**Post the mobile screening unit to Eskerford from 15 June to 31 August 2027.**

There it moves 342,200 passengers within the 20-minute standard, against 272,600 at Halloran Bay, the next best posting, and 13 per cent is the smallest whole per cent shortfall in Eskerford's forecast passengers at which another posting would move more. Not Cullinvale, which leads only when the unit's three lanes are added to each roster pattern: on every posted day last summer its duty managers, like every other host, stood down two of their own lanes through its banks. Not Halloran Bay, which leads once that stand-down is taken off but the roster patterns are still read as the lanes open: it is the one checkpoint of the eight that opens its pattern, and seven of the others, Eskerford by two lanes, leave bank lanes closed every day of the summer whether the unit is there or not.

## 2. Critical Components

1. Bank lanes each checkpoint's roster pattern plans and the checkpoint does not open, on its own days and its posted days alike: Eskerford **2**, Halloran Bay **0**, each of the other six **1**.
2. Eskerford's posting moves **342,200** passengers within the standard over the summer.
3. Halloran Bay's, the runner-up, moves **272,600**.
4. The smallest whole per cent shortfall in Eskerford's forecast passengers at which another posting (Halloran Bay) moves more is **13 per cent**.

## 3. Step-by-Step Solution

1. Counted each checkpoint's own lanes screening in every 15 minutes of checkpoint_lane_counts_20260615_20260831.csv, lanes M1 to M3 and the two lanes that run only before 05:00 and after 21:00 apart, against roster_plan_summer2026.csv, separately for the days the unit was posted there (mobile_unit_postings_2026.csv) and for its own days.
2. On its own days each checkpoint opens the same lanes every day, lane faults in lane_fault_log_2026.csv aside: its pattern less the bank lanes it never opens, 2 at Eskerford, 1 at six others and none at Halloran Bay, whose pattern staffs its five lanes right through the day.
3. On its posted days every checkpoint opens fewer still: the lanes it never opens and, on top of those, the lanes its duty managers stand down while the unit screens, two through the evening bank at all eight and through the morning bank at six of them, three or four in the quiet middle of the day and in the closing three quarters of an hour.
4. Took each airport's lanes without the unit as roster_pattern_summer2027.xlsx, which plans the same lanes as the 2026 pattern, less the bank lanes it does not open; and its lanes with the unit as the pattern less the whole posted-day gap, plus the unit's 3 lanes from 05:00 to 21:00 (mobile_screening_unit_deployment_policy_2027.pdf).
5. Ran checkpoint_planning_standard_2026.pdf sections 4 and 6 on the three design days of summer2027_planning_sheet.xlsx on both sets of lanes and multiplied each day's difference by 16, 31 and 31 days: Eskerford 342,200, Halloran Bay 272,600, every other airport less.
6. Cut Eskerford's design-day arrivals uniformly a whole per cent at a time: 13 per cent is the smallest cut at which its posting moves fewer passengers than Halloran Bay's.
7. Summed pax_screened in the lane feed by airport over the passenger lanes and the unit's, leaving out the two lanes at each checkpoint that screen only before 05:00 and after 21:00, the staff and aircrew search the deployment policy describes, which the operators' returns in operator_traffic_returns_2026.csv do not include.
8. Divided each airport's invoice and credit-note amounts in hotel_invoices_CC4109_summer2026.xlsx, matched to postings by purchase order, by the officer-nights on its accommodation lines, each stay's nights counted once.
9. Counted each line of expense_claims_CC4109_2026.csv once by claim reference and line, assigned each claim to the posting week its subsistence days fall in, and divided each airport's total by its posting weeks.
10. Posted the unit to Eskerford.

## 4. Deliverable Answers

### mobile_team_posting_summer_2027.pdf

1. Post the mobile screening unit to Eskerford for 15 June to 31 August 2027.
2. Passengers the unit would move within the 20-minute standard over the summer, nearest hundred:
   - Eskerford: 342,200
   - Halloran Bay: 272,600
   - Ardcarrig: 240,800
   - Cullinvale: 231,900
   - Faranloe: 202,800
   - Glenkessan: 163,700
   - Brennagh: 145,900
   - Dromkeel: 135,400
3. Smallest whole per cent shortfall in Eskerford's forecast passengers at which another posting (Halloran Bay) moves more: 13 per cent.
4. Bar chart of the passengers the unit would move at each airport over the summer on page 1, Eskerford marked.

### mobile_team_effect_2027.xlsx

1. The eight airports' summer figures and the 13 per cent smallest shortfall, as in the memo.
2. Passengers screened at each airport from 15 June to 31 August 2026 (passenger lanes and the unit's), nearest hundred:
   - Eskerford: 841,500
   - Halloran Bay: 590,000
   - Ardcarrig: 1,051,700
   - Cullinvale: 1,215,800
   - Faranloe: 992,800
   - Glenkessan: 593,300
   - Brennagh: 704,000
   - Dromkeel: 816,900
3. Hotel cost per officer-night of last summer's postings, euros to the cent:
   - Eskerford: EUR 98.50
   - Halloran Bay: EUR 112.98
   - Ardcarrig: EUR 110.01
   - Cullinvale: EUR 116.72
   - Faranloe: EUR 90.30
   - Glenkessan: EUR 93.73
   - Brennagh: EUR 84.70
   - Dromkeel: EUR 95.40
4. The unit's expense claims per posting week last summer, euros to the cent:
   - Eskerford: EUR 8,163.34
   - Halloran Bay: EUR 8,091.04
   - Ardcarrig: EUR 7,339.69
   - Cullinvale: EUR 7,135.92
   - Faranloe: EUR 7,991.56
   - Glenkessan: EUR 8,724.60
   - Brennagh: EUR 8,247.46
   - Dromkeel: EUR 8,824.96
