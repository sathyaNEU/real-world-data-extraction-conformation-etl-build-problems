## Tags

**Domain:** Marketing & Consumer Research (customer satisfaction driver analysis).
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**Crowding accounts for most of the fall: 3 of the 5.2 points by which the share of passengers satisfied overall fell, from 86.4% in spring 2025 to 81.2% in spring 2026. Fund the crowding remedy.**
Measured on the conditions each surveyed passenger's own train ran under, journeys on a train carrying more passengers than seats rose from 7.2% to 16.8% and such a journey ends satisfied 32.5 points less often. Not on-board staffing, which the tracker's attribute ratings put first (2 points by derived importance) because passengers on a crowded train mark every aspect down; not 1 point with the ratings held as controls.

## 2. Critical Components

1. Every questionnaire is linked through its batch to the train it was handed out on and the passenger's own stations, so each of the four drivers is the Schedule 7 (3.1) condition of that passenger's trip.
2. Crowding: **7.2%** of journeys in spring 2025, **16.8%** in spring 2026, **32.5** points less likely satisfied when met, **3** points of the fall.
3. On-board staffing **1**, punctuality **1**, fares **0** points: trains without staff rose from **9.3%** to **39.0%** of journeys but cost **4.3** points when met; late arrivals rose from **8.0%** to **12.5%**.

## 3. Step-by-Step Solution

1. Took the Partnership's letter (a) with Schedule 7 Part 3: a driver's points are those by which the tracker's weighted share satisfied (codes 4 and 5) would have fallen less had its condition met passengers as in spring 2025, the other three as they were.
2. Linked each response's batch_id to the fieldwork log's train and the working timetable in force that day (Dec24 before 14 December 2025, Dec25 after; bank holidays on the SUN schedules), and coded the written-in stations to station codes.
3. Crowded: the load-weigh passengers of the train's units (class 166 vehicles summed) on departure from any station of the passenger's trip above the standard seats of the units formed that day; late: arrival at the passenger's station five minutes or more after the timetable; unstaffed: no as-worked crew row for the train; fares: the flow's change for the ticket type in spring 2026.
4. Fitted a weighted linear model of being satisfied on the four conditions and a spring 2026 term over both waves; each driver's points are minus its effect times the change in its weighted share of journeys.
5. On time: the Dec25 trains timetabled each day of the four weeks ending 19 September 2026 (31 August on the SUN schedules), on time when arriving at the final destination less than five minutes late, an arrival after midnight timed against the evening's schedule, a train with no arrival there not on time.
6. Staffed: of the trains with any movement row, those whose turn was Rostered or covered by an amendment, an amendment logged in the evening covering the next day's turn (its original_staff_ref).
7. Standing: weekday trains due at Marlvale Central from 07:00 to 09:59 (31 August left out, the same either way), each formed unit's load-weigh rows at the station before matched by unit and the minute the train left (a class 166's three vehicle rows, each carrying the unit's figure since the May 2026 system move, read once), less the standard seats (the refreshed units at their seats after return), summed where positive.
8. Crowding 3 points, on-board staffing 1, punctuality 1, fares 0; crowding accounts for most of the fall.

## 4. Deliverable Answers

### satisfaction_fall_spring2026.xlsx

1. Driver accounting for most of the fall: crowding
2. Points of the fall it accounts for: 3
3. Share of passengers satisfied overall: spring 2025 86.4%; spring 2026 81.2%
4. Trains on time at their final destination, four weeks ending 19 September 2026 (per cent):
   - Marlvale Main Line: 81.0
   - Hollin Vale: 84.6
   - Coastway: 85.0
   - Pellow Branch: 87.4
   - Corrington Link: 79.0
5. Trains that ran with on-board staff, same weeks (per cent):
   - Marlvale Main Line: 89.5
   - Hollin Vale: 43.9
   - Coastway: 47.6
   - Pellow Branch: 43.5
   - Corrington Link: 88.8
6. Passengers standing on weekday arrivals at Marlvale Central from 07:00 to 09:59, same weeks:
   - Marlvale Main Line: 1,720
   - Hollin Vale: 829
   - Coastway: 1,210
   - Corrington Link: 3,021

### satisfaction_bridge_spring2026.png

1. The fall in the share satisfied by driver (points): crowding 3, on-board staffing 1, punctuality 1, fares 0, not explained by the four 0; the fall 5.2.
