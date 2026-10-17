## Tags

**Domain:** Urban & Regional Science (forecasting: a city subway's weekday-morning platform crowds forecast for a roster pick, the busiest platforms' counted crowds read as a backlog behind trains that arrive carrying their branch).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The spring 2027 pick should fund 26 weekday-morning platform conductor shifts a week.** The Sallow Park Line 1 and Line 4 southbound crowds are riders left behind by trains that arrive carrying their branch, a backlog that forms only Tuesday to Thursday, and Corran Junction's Line 5 westbound backlog clears with the spring's eight-car trains. Not the count that carries last autumn's mid-week counts to Monday, Friday and the eight-car trains in proportion to entries, which posts Sallow Park on Mondays and Fridays and Corran Junction's Line 5 every weekday; not the count of one headway's arrivals, which misses the mid-week backlog.

## 2. Critical Components

1. Shifts by weekday: Monday **4**, Tuesday **6**, Wednesday **6**, Thursday **6**, Friday **4**.
2. Posted Monday to Friday: **GAR-2, COR-2, ALB-6, QUA-6** (**20** shifts).
3. Posted Tuesday to Thursday only: **SAL-1S, SAL-4S** (**6** shifts).
4. Not posted: **COR-5W** on any weekday, its backlog cleared by the eight-car trains.

## 3. Step-by-Step Solution

1. Converted station_census_2026-10.xlsx to people a minute onto and off each platform and through each passage, scaled each station to its autumn 2026 Tuesday-to-Thursday morning by the fare export's entries between 06:00 and 10:00 local on its census day.
2. From vtc_fare_entries_hourly_2024-06-03_2027-01-10.parquet (UTC to local), took each complex's autumn 2026 weekday index and the spring 2026 over autumn 2025 ratio for the spring pick.
3. Ran each line's trains through weekday_timetables_aut26_spr27.csv at cars times the fleet register's 150-person maximum load, each train taking at most its room after the riders it brings from upstream and the riders getting off, the rest waiting for the next train.
4. Checked the model against platform_counts_autumn_2026.xlsx on the AUT26 timetable: it builds a backlog on the counted mid-week mornings at SAL-1S, SAL-4S and COR-5W and none on COR-5W's hybrid-day Monday and Friday, as counted, where carrying the mid-week count by entries puts COR-5W over its capacity on both.
5. Forecast each watch-list platform's morning peak quarter-hour for an average spring weekday on the SPR27 timetable (Line 5 eight cars) and compared it with 85 per cent of its rated capacity in platform_capacity_register.csv on 1 March 2027, per platform_crowding_standard_rev4.pdf.
6. Counted the platform-weekdays over the line: 26 shifts a week.

## 4. Deliverable Answers

### spring_2027_platform_conductors.xlsx

1. Shifts a week: 26 (Monday 4, Tuesday 6, Wednesday 6, Thursday 6, Friday 4).
2. Posting schedule, each watch-list platform and its posted weekdays:
   - GAR-2 (Garnett Street, Line 2 island platform): Monday to Friday
   - GAR-3S (Garnett Street, Line 3 southbound platform): none
   - SAL-1S (Sallow Park, Line 1 southbound platform): Tuesday to Thursday
   - SAL-1N (Sallow Park, Line 1 northbound platform): none
   - SAL-4S (Sallow Park, Line 4 southbound platform): Tuesday to Thursday
   - HES-1S (Hesper Avenue, Line 1 southbound platform): none
   - HES-3 (Hesper Avenue, Line 3 island platform): none
   - COR-5W (Corran Junction, Line 5 westbound platform): none
   - COR-2 (Corran Junction, Line 2 island platform): Monday to Friday
   - FER-5W (Ferrier Square, Line 5 westbound platform): none
   - FER-4S (Ferrier Square, Line 4 southbound platform): none
   - FER-4N (Ferrier Square, Line 4 northbound platform): none
   - ALB-3S (Albrecht Place, Line 3 southbound platform): none
   - ALB-3N (Albrecht Place, Line 3 northbound platform): none
   - ALB-6 (Albrecht Place, Line 6 island platform): Monday to Friday
   - QUA-1S (Quarry Road, Line 1 southbound platform): none
   - QUA-6 (Quarry Road, Line 6 island platform): Monday to Friday
3. Platform escalators at their rated flows between 07:00 and 09:30 on the autumn 2026 pick's weekdays, people a minute down to the platforms and up from them:
   - Garnett Street: 72 down, 144 up
   - Sallow Park: 216 down, 72 up
   - Hesper Avenue: 108 down, 144 up
   - Corran Junction: 232 down, 96 up
   - Ferrier Square: 36 down, 248 up
   - Albrecht Place: 268 down, 36 up
   - Quarry Road: 132 down, 96 up
4. Elevator-hours out of service between 07:00 and 09:45 on the autumn 2026 pick's weekday mornings:
   - Garnett Street: 27.9
   - Sallow Park: 53.3
   - Hesper Avenue: 38.6
   - Corran Junction: 18.0
   - Ferrier Square: 45.5
   - Albrecht Place: 37.3
   - Quarry Road: 41.3

### platform_escalators_am_peak.png

1. Grouped bar chart, one pair of bars per watch-list complex, the escalator figures down to the platforms and up from them, each bar labelled with its value.
