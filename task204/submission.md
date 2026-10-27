## Tags

**Domain:** Physical and environmental sciences (indoor air quality monitoring of an education estate).
**Analytical objective:** Anomaly Detection and Diagnostics.

## 1. Final Recommendation

**January's minor-works allocation funds option A, replacing AHU-03 and AHU-04 and the Tulrohan supply and extract distribution.**
The block's six teaching spaces are supplied with **5.0** litres per second per occupant present across the term's timetabled sessions, so the **8** TGD-M4 requires is **1.58** times the rate achieved. Not the timetable change, which leaves the supply where it is. Not the commissioning record's design supply, which its own outstanding-items section records as never proved at the spaces.

## 2. Critical Components

1. Timetabled sessions in the six block rooms over 28 September to 11 December 2026: **1,728**
2. Occupant-hours present across those sessions: **70,404.6**
3. Shortest response time in the block, gross internal volume over the outdoor air recovered: **189 minutes**, against a teaching period of **55 minutes**
4. Block rooms below the requirement on their own records: **6 of 6**

## 3. Step-by-Step Solution

1. Keyed bms_co2_5min_autumn2026.csv to room codes through campus_room_register.csv and took each reading's excess over campus_outdoor_co2_hourly_2026.csv, filling the analyser's 12 to 25 October absence from macehead_gaw_co2_hourly_2026.csv.
2. Took the six rooms in scope from capital_bid_tulrohan_block.xlsx and their gross internal volumes from asbuilt_room_data_sheets_kilmoneen.pdf.
3. Took the block's sessions from timetable_autumn2026.csv and the occupants present in each from attendance_marks_autumn2026.csv: 1,728 sessions and 70,404.6 occupant-hours.
4. Integrated each session's carbon dioxide balance across the session, the stored term being the room's volume times the change between the session's first and last reading and the source term the 0.0072 litres per second per person in the TGD-M4 extract's design data table times the occupants present, and solved each session for the outdoor air supplied.
5. Divided the outdoor air so recovered by the occupant-seconds present over the same sessions: 5.0 litres per second per occupant present, against the 8 TGD-M4 requires.
6. Checked that no reading in the record is a settled one: the shortest response time in the block, volume over the recovered supply, is 189 minutes against a 55 minute period, and 6 of the 6 rooms sit below the requirement.
7. Counted occupied hours, hours over the indicator and readings received on procedure note EST-14's bases, the unit's occupied state from bms_plant_status_autumn2026.csv, five minutes to a reading, and 288 a day on the 48 teaching days in etb_academic_calendar_2026_27.xlsx.
8. The allocation funds option A in capital_bid_tulrohan_block.xlsx, the air-handling replacement, and not option B.

## 4. Deliverable Answers

### tulrohan_ventilation_assessment.xlsx

1. Outdoor air supplied to the Tulrohan Block across the term's timetabled sessions: **5.0** litres per second per occupant present; remedy: option A, replace AHU-03 and AHU-04 and the Tulrohan supply and extract distribution.
2. Occupied hours recorded and occupied hours over 1,500 ppm, each monitored space by calendar month, 56 rows in room then month order, hours to two decimals:
   - ANG-012, September 2026: 22.42 recorded, 0.00 over
   - ANG-012, October 2026: 118.33 recorded, 0.00 over
   - ANG-012, November 2026: 148.17 recorded, 0.00 over
   - ANG-012, December 2026: 59.67 recorded, 0.00 over
   - ANG-016, September 2026: 22.50 recorded, 0.00 over
   - ANG-016, October 2026: 127.50 recorded, 0.00 over
   - ANG-016, November 2026: 127.50 recorded, 0.00 over
   - ANG-016, December 2026: 59.92 recorded, 0.00 over
   - ANG-103, September 2026: 21.58 recorded, 0.00 over
   - ANG-103, October 2026: 117.83 recorded, 0.08 over
   - ANG-103, November 2026: 140.00 recorded, 0.08 over
   - ANG-103, December 2026: 59.00 recorded, 0.00 over
   - ANG-107, September 2026: 21.67 recorded, 0.00 over
   - ANG-107, October 2026: 117.58 recorded, 0.00 over
   - ANG-107, November 2026: 147.92 recorded, 0.00 over
   - ANG-107, December 2026: 59.42 recorded, 0.00 over
   - DRM-104, September 2026: 22.17 recorded, 0.17 over
   - DRM-104, October 2026: 119.25 recorded, 1.00 over
   - DRM-104, November 2026: 148.67 recorded, 1.08 over
   - DRM-104, December 2026: 59.42 recorded, 0.50 over
   - DRM-108, September 2026: 22.50 recorded, 0.00 over
   - DRM-108, October 2026: 126.33 recorded, 0.75 over
   - DRM-108, November 2026: 141.58 recorded, 0.50 over
   - DRM-108, December 2026: 59.17 recorded, 0.50 over
   - DRM-205, September 2026: 22.33 recorded, 0.00 over
   - DRM-205, October 2026: 118.83 recorded, 0.58 over
   - DRM-205, November 2026: 140.67 recorded, 0.50 over
   - DRM-205, December 2026: 59.50 recorded, 0.17 over
   - DRM-211, September 2026: 21.75 recorded, 0.00 over
   - DRM-211, October 2026: 125.67 recorded, 0.42 over
   - DRM-211, November 2026: 140.67 recorded, 0.42 over
   - DRM-211, December 2026: 52.17 recorded, 0.08 over
   - TUL-F04, September 2026: 18.50 recorded, 0.42 over
   - TUL-F04, October 2026: 104.17 recorded, 1.83 over
   - TUL-F04, November 2026: 116.58 recorded, 2.17 over
   - TUL-F04, December 2026: 49.33 recorded, 0.00 over
   - TUL-F09, September 2026: 18.33 recorded, 0.00 over
   - TUL-F09, October 2026: 102.67 recorded, 0.00 over
   - TUL-F09, November 2026: 114.00 recorded, 0.00 over
   - TUL-F09, December 2026: 48.50 recorded, 0.00 over
   - TUL-F15, September 2026: 18.42 recorded, 0.58 over
   - TUL-F15, October 2026: 98.25 recorded, 0.50 over
   - TUL-F15, November 2026: 122.67 recorded, 0.50 over
   - TUL-F15, December 2026: 42.75 recorded, 0.50 over
   - TUL-G07, September 2026: 18.08 recorded, 0.00 over
   - TUL-G07, October 2026: 103.25 recorded, 0.33 over
   - TUL-G07, November 2026: 115.00 recorded, 0.92 over
   - TUL-G07, December 2026: 48.33 recorded, 0.00 over
   - TUL-G12, September 2026: 18.50 recorded, 1.00 over
   - TUL-G12, October 2026: 98.50 recorded, 18.33 over
   - TUL-G12, November 2026: 123.08 recorded, 18.08 over
   - TUL-G12, December 2026: 49.17 recorded, 9.58 over
   - TUL-G18, September 2026: 18.42 recorded, 0.00 over
   - TUL-G18, October 2026: 98.50 recorded, 0.33 over
   - TUL-G18, November 2026: 123.00 recorded, 0.92 over
   - TUL-G18, December 2026: 43.00 recorded, 0.50 over
3. Share of expected readings received over the term, each monitored space, one decimal as a percentage:
   - ANG-012: 96.8
   - ANG-016: 93.7
   - ANG-103: 94.1
   - ANG-107: 96.4
   - DRM-104: 97.2
   - DRM-108: 97.0
   - DRM-205: 94.9
   - DRM-211: 94.5
   - TUL-F04: 97.5
   - TUL-F09: 95.9
   - TUL-F15: 95.2
   - TUL-G07: 96.1
   - TUL-G12: 97.8
   - TUL-G18: 95.6
4. Mean occupants present per timetabled session, the six block rooms, nearest whole:
   - TUL-G07: 35
   - TUL-G12: 48
   - TUL-G18: 37
   - TUL-F04: 49
   - TUL-F09: 41
   - TUL-F15: 56
5. The four largest rises between a timetabled session's first and last reading in the block, in descending order:
   - TUL-G12, period P1 on 2026-11-02
   - TUL-G12, period P1 on 2026-10-19
   - TUL-G07, period P2 on 2026-10-13
   - TUL-G12, period P1 on 2026-11-09

### tulrohan_session_balance.png

6. One space's timetabled sessions across a day, the five-minute carbon dioxide trace against the campus outdoor analyser, the timetabled periods and the midday setback shaded, the 1,500 ppm screening indicator drawn and labelled, the occupants present marked on each period, and the block's rate against the requirement stated in the title.
