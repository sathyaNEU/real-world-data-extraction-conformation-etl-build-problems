## Tags

**Domain:** General Statistics & Data Science (resampling, simulation and Monte Carlo methods: a festival-city hotel's occupied rooms for each night of its August 2027 festival season, the bookings still to come forecast on the booking process's own unit, the stay, a run of consecutive nights taken only if every night has a room, for the housekeeping agency block).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Brennock's block should go to the closing week, Monday 23 to Sunday 29 August 2027, forecast at about 400 room-nights above the crew's capacity; the week that would come next is the concert week, Monday 9 to Sunday 15 August 2027, at about 200.**
Friday 13 and Saturday 14 August are already full on the book, and a stay is sold only if every night of it has a room, so none of the festival's stays booked from now on can run through them; in the five past seasons the stays booked after the same point that did so carried about 420 room-nights of that week's other five nights. Not the concert week, which each night's own past pickup puts first at about 600 by counting those stays. Not the opening weeks or the week after the concerts, each forecast below the concert week.

## 2. Critical Components

1. Friday 13 and Saturday 14 August 2027 are full on the book at 06:12 on Thursday 1 July 2027: **480** rooms each, the hotel's 480
2. The concert week, Monday 9 to Sunday 15 August 2027, is forecast at about **200** room-nights above the crew's capacity
3. The closing week, Monday 23 to Sunday 29 August 2027, is forecast at about **400** room-nights above the crew's capacity, the most of the five roster weeks

## 3. Step-by-Step Solution

1. From pms_reservations_extract_2027-07-01.csv (one row per room, times in UTC) took each night's book at the extract, the rooms booked before 06:12 on Thursday 1 July 2027 and not cancelled by then: Friday 13 and Saturday 14 August hold 480 rooms each.
2. For each season from 2022 to 2026 rebuilt the book at the Thursday five weeks before that year's opening night (HK-04's confirmation day, the opening night from festival_programme_dates.json), each reservation's dates as they then stood from pms_amendment_log_2027-07-01.csv, on the nights at the same place from the festival's first Friday as 2027's.
3. Split each past night's rooms that stayed (status OUT or INH) into the book's rooms and the stays booked after that point, and marked the later stays that ran through the aligned Friday and Saturday: about 420 room-nights a season of the concert week's other five nights.
4. Forecast each 2027 night as its book at the past seasons' rate of staying plus the past seasons' average later stays, less those through the two full nights, which cannot be sold this year; the full nights at 480 rooms less the event rate's no-shows.
5. Summed each roster week's nights above 380 (HK-04's rooms above capacity): the closing week about 400, the concert week next at about 200; each night's own past pickup instead puts the concert week first at about 600.
6. Counted the completed departure cleans and stayover services of each 2026 roster week in hk_task_log_2026-07-27_2026-08-30.csv by service date (re-cleans part of the service they repeat, do-not-disturb and refused rooms not serviced), each credited to who did it (the login's user, or the person a supervisor's note names), as Brennock's when that person is on Brennock's timesheet for the day in brennock_timesheets_weighhouse_summer_2026.xlsx (three logins the app now holds as crew belong to temps hr_housekeeping_staff_2027-06-28.xlsx shows taken on after the season), and the crew's overtime by the date worked in each line's reference in payroll_overtime_lines_2026-P14-P19.csv.
7. For each day of the block, 10 to 16 August 2026, joined each block temp to the day badge reception issued that day (reception_day_badge_log_2026-08.csv), took the first entry and last exit from staff_access_events_2026-08.csv with the loading bay reader LB-02 read on its UTC clock, and billed the framework agreement's hours at its rate (Sunday at one and a quarter times), before VAT.
8. Send Brennock's block to the closing week, Monday 23 to Sunday 29 August 2027.

## 4. Deliverable Answers

### housekeeping_block_2027.xlsx

1. Block week: Monday 23 to Sunday 29 August 2027, about 400 forecast room-nights above the crew's capacity.
2. The week that would come next: Monday 9 to Sunday 15 August 2027, about 200 forecast room-nights above the crew's capacity.
3. Last year's season by roster week, whole rooms and hours to the quarter hour:
   - Monday 27 July to Sunday 2 August 2026: crew departure cleans 920, crew stayover services 1,100, Brennock departure cleans 184, Brennock stayover services 206, crew overtime 17.25 hours
   - Monday 3 to Sunday 9 August 2026: crew departure cleans 796, crew stayover services 986, Brennock departure cleans 113, Brennock stayover services 166, crew overtime 20.75 hours
   - Monday 10 to Sunday 16 August 2026: crew departure cleans 788, crew stayover services 1,336, Brennock departure cleans 341, Brennock stayover services 577, crew overtime 15.25 hours
   - Monday 17 to Sunday 23 August 2026: crew departure cleans 929, crew stayover services 1,460, Brennock departure cleans 145, Brennock stayover services 249, crew overtime 11.25 hours
   - Monday 24 to Sunday 30 August 2026: crew departure cleans 962, crew stayover services 1,574, Brennock departure cleans 187, Brennock stayover services 276, crew overtime 14.25 hours
4. Last year's block week, the hours Brennock may bill for the block, to the quarter hour:
   - Monday 10 August 2026: 59.25 hours
   - Tuesday 11 August 2026: 59.50 hours
   - Wednesday 12 August 2026: 55.75 hours
   - Thursday 13 August 2026: 59.25 hours
   - Friday 14 August 2026: 59.75 hours
   - Saturday 15 August 2026: 59.75 hours
   - Sunday 16 August 2026: 59.75 hours
5. The week's charge before VAT: EUR 9,654.27.

### housekeeping_block_2027.pdf

1. One-page note titled with the call: the block to Monday 23 to Sunday 29 August 2027, about 400 room-nights above the crew's capacity, the concert week next at about 200.
2. Column chart of each night's forecast occupied rooms from Monday 26 July to Sunday 29 August 2027 against the crew's capacity line at 380 (and the hotel's 480), the block week's nights highlighted and the two full concert nights marked.
