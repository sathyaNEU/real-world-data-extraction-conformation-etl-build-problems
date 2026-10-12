# task254: the 2027 staff shuttle's morning departure

## Tags

**Domain:** Urban & Regional Science (network analysis: corridor travel-time reliability from probe segment data, setting a timetable departure).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The 2027 staff shuttle should leave the Cedar Grove park-and-ride lot at 7:05 a.m.**

Built day by day, each segment at the five-minute epoch in which the shuttle enters it, trips leaving at 7:05 a.m. would have reached the Brook Street stop by 8:00 a.m. on 238 of the 252 working weekdays against a bar of 227, and trips leaving at 7:10 a.m. on only 190. Not 7:15 a.m., which adds up the sixteen segments' travel times for the epoch the shuttle leaves in: that reads the queue ahead of the I-264 merge before the shuttle gets there, while it is still growing, so the trip it measures is one no vehicle made. Not 7:10 a.m. from the whole route read at the trip's midpoint or from 90th-percentile segment times summed at departure, nor 7:00 a.m. from a 90th-percentile profile walked through the epochs: none of them is any day's trip.

## 2. Critical Components

1. Working weekdays from 1 October 2025 to 30 September 2026: **252**, so the bar is **227**
2. Working weekdays on which trips leaving at 7:05 a.m. would have reached the stop by 8:00 a.m.: **238**
3. Working weekdays on which trips leaving at 7:10 a.m. would have reached the stop by 8:00 a.m.: **190**

## 3. Step-by-Step Solution

1. Took Monday to Friday from 1 October 2025 to 30 September 2026 less the 2025-26 holidays in hr_holiday_calendars.xlsx (shuttle standard 2.2): 252 working weekdays, so the bar is 227 (90 per cent, standard 2.1).
2. Read travel_time_passenger (standard 2.5) for the sixteen TMCs of route_cedar_grove_to_brook_st.xlsx from the twelve trelvane_tmc_export files, epochs in local time per trelvane_export_readme.txt: every route segment has a value in every morning epoch of the 252 days.
3. For each working weekday and each departure from 6:30 to 7:20 a.m., built the trip (standard 2.4): the route file's 4-minute lot leg, then each segment in order at its travel time for the five-minute epoch in which the shuttle enters it, the next segment entered as the last is left, then the 3-minute leg to the stop.
4. Counted the days arriving at or before 8:00 a.m.: 238 at 7:05 a.m. and 190 at 7:10 a.m., so 7:05 a.m. is the latest departure meeting the bar.
5. Counted the 8:00 a.m. starters on the permit roll (employee numbers) and the HR-granted spaces (payroll IDs mapped to employee numbers through hr_staff_extract_2026-10-02.csv) of cedar_grove_reassignment_list.xlsx, each person once, less the opt-outs: 410 riders, 15 vehicles at the 28 seats of ridgeline_schedule_of_charges_2027.xlsx, 10 seats left empty.
6. Added the legs and each code of ridgeline_deadhead_route_brook_st_yard.xlsx at its length in TMC_Identification.csv's release 2025.2, in force when the route was set up (in release 2026.1 its I-264 to Grade Lane code is an I-264 ramp): 10.96 miles; at $214.00 a vehicle a day and $3.50 a vehicle-mile over the 252 service days of the 2027 calendar, $953,920.80 for the 15 vehicles.
7. Counted each departure's late working weekdays, each carrying the 410 riders, as its late staff arrivals and added $38.00 for each to the vehicle charges (shuttle_service_budget_note_2027.docx): from $969,501 at 6:50 a.m. to $3,493,461 at 7:20 a.m.
8. Recommendation: the 2027 staff shuttle leaves Cedar Grove at 7:05 a.m.

## 4. Deliverable Answers

### shuttle_departures_2027.xlsx

1. Departure: 7:05 a.m.
2. Working weekdays on which trips would have reached the stop by 8:00 a.m.: 238 leaving at 7:05 a.m., 190 leaving at 7:10 a.m.
3. Staff who will ride the morning shuttle: 410
4. Vehicles it needs: 15
5. Seats left empty: 10

### shuttle_departure_costs_2027.html

1. Late staff arrivals a year and the 2027 cost of holding each departure, whole arrivals and whole dollars:
   - 6:50 a.m.: 410 late arrivals, $969,501
   - 6:55 a.m.: 410 late arrivals, $969,501
   - 7:00 a.m.: 1,230 late arrivals, $1,000,661
   - 7:05 a.m.: 5,740 late arrivals, $1,172,041
   - 7:10 a.m.: 25,420 late arrivals, $1,919,881
   - 7:15 a.m.: 47,560 late arrivals, $2,761,201
   - 7:20 a.m.: 66,830 late arrivals, $3,493,461
2. Bar chart above the table: one bar per departure from 6:50 to 7:20 a.m. in time order, each stacked into operator charges and late-arrival cost and labelled with its 2027 cost in whole dollars, on a dollar axis, titled with the rise in cost from 6:50 to 7:20 a.m.
