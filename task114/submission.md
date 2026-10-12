# task114: Harrowfield meeting rooms for Level 21

## Tags

**Domain:** Business & Operations Analytics, facilities and workplace (the meeting-room count for a merged consultancy's one new floor, replayed from both legacy offices' reference year).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Build the new office with 31 meeting rooms.**

At 31 rooms the reference year replayed on the one floor runs short on 7 working days, inside the brief's twelve, and at 30 rooms it runs short on 14. Not the count from both offices' room bookings on one timeline, which leaves out the meetings that had one person in each office that day and so used no room. Not the two offices' own counts added together, which leaves them out too.

## 2. Critical Components

1. A meeting needs a room on the one floor when two or more of its invitees who had not declined were in either office that day: **27,607 meetings** in the reference year
2. The day's busiest moment runs above 31 rooms on **7 working days**
3. It runs above 30 rooms on **14 working days**

## 3. Step-by-Step Solution

1. Took the 246 working days from firm_calendar_fy2026.csv and each employee's office on each of them from granted card events in adelaide_access_events_fy2026.csv and door events in front_st_door_events_fy2026.csv, matched through staff_directory_fy2026.xlsx.
2. Kept the internal meetings in calendar_events_fy2026.parquet (not cancelled, not all-day, not client meetings or town halls, which new_office_brief_stage2.pdf sends to the client suite and the town hall space) and counted each one's invitees in calendar_attendees_fy2026.csv who had not declined and were in each office that day.
3. Every meeting with two or more such invitees in one office that day has a room booking in that office in adelaide_room_bookings_fy2026.csv or front_st_room_calendar_export.csv, so on one floor every meeting with two or more of them in either office takes a room.
4. Counted those meetings over the year: 27,607 need a room, 9,144 of them with one person in each office that day.
5. Took each working day's busiest moment, a room freed at a minute being free for a meeting that starts then as the close-outs' Method sheet counts it, and the fewest rooms short on no more than twelve working days per the brief: 31 rooms, short on 7 days, where 30 rooms are short on 14.
6. Rebuilt today's meeting-room holds from the two booking exports under the Method sheet of room_utilisation_close_outs_fy2026.xlsx, each room typed as the Changes sheet of room_register.xlsx had it on the day: an Adelaide Street booking held to its end or to its released_at, a combined booking on both halves as its own row has it, and a Front Street series row dropped wherever an exception of any status, in any room, took its slot.
7. Took a booking as one person's when its calendar item, a client meeting aside, carries one person of the firm (an Adelaide Street app or kiosk booking has no item, so its headcount says), as a call unless that item is a Focus time block, and left one-person bookings and the client meetings (the calendar's Client meeting items, which the brief sends to the client suite) out of the room count: the offices' own bookings justify 15 and 13 rooms, against 30 and 31 bookable on 30 September 2026.
8. Recommendation: build the new office with 31 meeting rooms.

## 4. Deliverable Answers

### meeting_rooms_brief.docx

1. Meeting rooms to build: 31
2. Working days the new office would have run short at 31 rooms: 7
3. Working days it would have run short at 30 rooms: 14
4. Meeting rooms today, both offices together: 61
5. Adelaide Street by quarter (hours its meeting rooms were held, of which one person booked for a call, most meeting rooms in use at once):
   - Q1, October to December 2025: 2,726.53 hours, 516.17 call hours, 18 rooms
   - Q2, January to March 2026: 2,683.83 hours, 534.77 call hours, 18 rooms
   - Q3, April to June 2026: 2,872.85 hours, 559.62 call hours, 23 rooms
   - Q4, July to September 2026: 2,795.75 hours, 542.72 call hours, 20 rooms
6. Front Street by quarter, the same three figures:
   - Q1, October to December 2025: 2,506.75 hours, 666.00 call hours, 19 rooms
   - Q2, January to March 2026: 2,684.50 hours, 670.50 call hours, 19 rooms
   - Q3, April to June 2026: 2,732.00 hours, 697.50 call hours, 18 rooms
   - Q4, July to September 2026: 2,778.50 hours, 718.00 call hours, 18 rooms
7. Bookable meeting rooms on 30 September 2026: Adelaide Street 30, Front Street 31
8. Rooms each office's own bookings would have justified under the brief: Adelaide Street 15, Front Street 13

### room_demand_fy2026.svg

1. One bar for each of the 246 working days, the new office's busiest moment in meeting rooms, sorted highest first
2. A labelled line at 31 rooms, the committed count
3. A labelled line at 61 rooms, today's two offices' meeting rooms combined
4. The 7 working days above 31 rooms marked in orange
5. Title: Build 31 meeting rooms: the new office would have run short on 7 of 246 working days
