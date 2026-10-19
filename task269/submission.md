## Tags

**Domain:** Urban & Regional Science, network analysis (the waiting a frequent bus network's corridor riders do beyond the timetable, worked over the departures that serve each rider's destination where routes branch beyond a shared corridor).
**Analytical objective:** Descriptive & Distribution Analysis (how excess wait is distributed across Pellbrook Metro's eight frequent routes' corridor boardings in the August 2026 census fortnight).

## 1. Final Recommendation

**Give the 2027 headway supervisor teams to routes 3, 7, 31 and 40.**
Their corridor riders lose 1.5 (route 31), 1.1 (route 7), 1.1 (route 40) and 1.0 (route 3) minutes a boarding to excess waiting in the weekday peaks, against 0.8 on route 9, the first route below them. Not routes 7, 14, 31 and 40, which the excess wait worked over all of each route's departures gives (route 14 at 1.3), because 86 per cent of route 14's outbound corridor riders are bound for a branch and can take only that branch's buses, which keep their own interval: their excess wait is 0.1 minutes, not the 1.6 that both branches' bunched pairs would give. Not routes 3, 9, 31 and 40, which measuring each rider against the branch of the bus they boarded gives (route 7 at 0.6), because 66 per cent of route 7's outbound corridor riders are going to corridor stops and can take either branch's bus.

## 2. Critical Components

1. Route 14: **86** per cent of its outbound corridor boardings are bound for a branch; their excess wait is **0.1** minutes over their branch's departures against **1.6** over both branches'
2. Route 7: **66** per cent of its outbound corridor boardings are bound for corridor stops, where either branch's bus serves them
3. The cut: route 3 at **1.0** minutes a corridor boarding (fourth), route 9 at **0.8** (fifth)

## 3. Step-by-Step Solution

1. Took each trip's departure from each timing point from avl_timingpoint_departures_census_revised.csv (the later record where a bus reopened its doors, as the reliability standard sets out) and its timetabled times from the feed in force that day (gtfs_pellbrook_2026-07-20.zip to 16 August, gtfs_pellbrook_2026-08-17.zip from 17 August).
2. Took every tag-on in ticketing_journeys_census_2026-08.csv at a stop on its route's frequent corridor (frequent_corridors_2026.xlsx, the relocated route 22 stop 222199 read as 222111 through stop_changes_log_2026.csv) in the weekday peaks of 10 to 21 August 2026, 66,404 boardings, each at the last timing point at or before its stop.
3. Placed each outbound tag-off on routes 7, 14, 31 and 52 in the two branches' stop patterns from the timetable feeds: a corridor stop is served by both branches' buses and a branch stop by its branch's only; every inbound rider can take any bus to the City.
4. For each timing point, peak and census day, worked the random-arrival wait (the sum of squared headways over twice their sum, headways inside the peak) over the actual departures that serve the rider, less the same over the timetable's: route 14's branch-bound riders 0.1 minutes, against 1.6 over both branches' departures.
5. Gave each corridor boarding its cell's excess wait (a boarding with no tag-off the average of its cell's boardings with one) and averaged by route: 1.5 on route 31, 1.1 on routes 7 and 40, 1.0 on route 3, 0.8 on route 9, 0.7 on route 14, 0.6 on route 22, 0.4 on route 52.
6. Counted the pilot's shifts from pbc_supervision_timesheets_feb-jun_2026.csv, matching the payroll rows to the roster app's on the person (pbc_staff_list_2026-10-01.csv), the route (the pilot plan's posts), the day (payroll dates day first) and the peak, since both systems hold the shifts of 4 to 15 May; cancelled peaks and depot supervision out.
7. Costed the pilot from ledger_network_performance_fy2026_fy2027.csv: each route's post charges without the 30 June journal JNL-260630-11 (reversed on 1 July, June's invoices posted in July), plus each month's coordination fee shared by the month's shifts (headway_supervision_pilot_plan_2026.pdf).
8. Gave the four teams to the routes with the highest excess wait per corridor boarding, as the programme guidelines set out: routes 3, 7, 31 and 40.

## 4. Deliverable Answers

### pellbrook_2027_headway_programme_routes.xlsx

1. The four routes for the 2027 supervisor teams: 3, 7, 31 and 40
2. The first route below them: route 9
3. Excess wait per corridor boarding in the weekday peaks of the census fortnight (minutes, one decimal):
   - Route 3: 1.0
   - Route 7: 1.1
   - Route 9: 0.8
   - Route 14: 0.7
   - Route 22: 0.6
   - Route 31: 1.5
   - Route 40: 1.1
   - Route 52: 0.4
4. Supervisor shifts the 2026 pilot worked:
   - Route 3: 205
   - Route 7: 160
   - Route 9: 103
   - Route 14: 167
   - Route 22: 165
   - Route 31: 106
   - Route 40: 209
   - Route 52: 101
5. What the pilot cost (nearest dollar):
   - Route 3: $59,702
   - Route 7: $47,275
   - Route 9: $28,316
   - Route 14: $47,414
   - Route 22: $47,368
   - Route 31: $28,381
   - Route 40: $59,728
   - Route 52: $28,274

### excess_wait_by_route_census_2026.png

1. Bar chart of the eight routes' excess wait per corridor boarding in order, routes 3, 7, 31 and 40 marked and the cut drawn below the fourth, titled with the four routes.
