# task229 submission

## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: the error a stream gauging network's published daily discharge carries when each station's stage-discharge rating is read at the day's mean water level below hydropeaking plants).
**Analytical objective:** Data Quality Monitoring & Alerting (from which month of 2027 each station's published daily discharge carries the below-grade-B flag).

## 1. Final Recommendation

**Flag the published daily discharge at Corriston River below Talbot Canyon (C104) and at Hollis Bridge (C105) from January 2027, at Sable Creek (C107) from May, and at Merrin Creek below Merrin Falls (C112) and at Dunlop Road (C113) from July; the other 18 stations hold grade B through December.**

Below the two peaking plants each station's rating, read at the day's mean water level, publishes 14 to 32 per cent under the day's mean flow in every peaking month, against grade B's 5 per cent. Not Sable Creek alone, which is what taking each published daily discharge as the day's mean flow files. Not C112 and C113 from June: Merrin Falls generates continuously until 30 June.

## 2. Critical Components

1. In every peaking month the published daily discharge at C104 and C105 below Talbot Canyon and C112 and C113 below Merrin Falls falls **14 to 32 per cent** below the day's mean flow, the least at Corriston River at Hollis Bridge (C105) in February (**14.4 per cent**)
2. At Merrin Creek near the mouth (C124) the Vardy River's inflow damps the swing, and the published daily discharge stays within **1.0 per cent** of the day's mean flow in every month
3. Talbot Canyon peaks in every month but May and June; Merrin Falls, in service from 1 June, peaks from **July**
4. Sable Creek's May and June flows (**8.65** and **9.44** m3/s) exceed one and a half times its largest gauging (**4.21** m3/s)

## 3. Step-by-Step Solution

1. Graded each station-month of 2027 under sections 3 and 4 of hydrometric_data_standard_ed2.pdf on the flows of water_supply_outlook_2027.xlsx and corriston_hydro_operating_plan_2027.pdf (data_plan_2027.docx, section 2).
2. Took each station's published daily discharge as data_dictionary.csv defines it, the rating in force applied to the day's mean water level, unchanged in 2027 (data plan, section 1), with the ratings of rating_book_issue2_2026.pdf.
3. Built each peaking day at C104 and C105 below Talbot Canyon and C112, C113 and C124 below Merrin Falls from the operating plan: the minimum release (1.8 and 0.7 m3/s) outside 06:00 to 10:00 and 16:00 to 21:00, the rest of the day's forebay or headpond inflow inside them with 30-minute ramps, plus the local inflow (the outlook's station flow less its TAL-FB or MER-HP row).
4. Carried each day's flow through the station's rating to the water level and read the rating at the day's mean water level: 14 to 32 per cent below the day's mean flow at C104 and C105 from January to April and July to December, and at C112 and C113 from July, after Merrin Falls' continuous generation through June; at C124 the Vardy River's inflow keeps it within 1.0 per cent.
5. Applied the extrapolation rule against each rating's gauged top in the rating book: Sable Creek (C107) in May and June only; every other station's flow is steady through the day, so its published discharge equals the month's flow.
6. Counted the 2026 water year's station-days in daily_records_wy2023_wy2026.csv holding a water level measured on the day: one per station and day, Mattin Creek once across its move (station_register.xlsx), and no row received before the day it covers had ended (the GOES ingest's held messages).
7. Compared each 2026-water-year gauging in gaugings_2016_2026.csv (litres converted, channel rows summed, days in local standard time) with the rating in force on its day: before 1 April 2026 the 2019 ratings, recovered from the record's published water levels and discharges before that date; from 1 April the rating book's.
8. Recommendation: flag C104 and C105 from January 2027, C107 from May, C112 and C113 from July; the other 18 stations hold.

## 4. Deliverable Answers

### discharge_grades_2027.png

1. Grid of the 23 stations against January to December 2027 with every month short of grade B shaded: C104 and C105 January to April and July to December; C107 May and June; C112 and C113 July to December; no other cell shaded

### record_review_wy2026.xlsx

1. Station-days holding a water level measured on that day, 2026 water year:
   - October 2025: 662
   - November 2025: 655
   - December 2025: 695
   - January 2026: 683
   - February 2026: 620
   - March 2026: 696
   - April 2026: 671
   - May 2026: 687
   - June 2026: 672
   - July 2026: 705
   - August 2026: 700
   - September 2026: 686
2. Mean of each station's 2026-water-year gauging differences from the rating in force on the gauging day, per cent of the rating's discharge, one decimal place:
   - C101 Ashlin River above Lake Ashlin: -1.2
   - C102 Lake Ashlin at the outlet weir: 1.5
   - C103 Wren Creek near Corriston: -1.5
   - C104 Corriston River below Talbot Canyon: 3.2
   - C105 Corriston River at Hollis Bridge: -2.5
   - C106 Tolley Creek at the highway: 2.1
   - C107 Sable Creek near the mouth: -1.8
   - C108 Marrock River at Brandt Flats: 2.2
   - C109 Fenn Creek below the powerhouse: -1.6
   - C111 Pellam Creek at the springs: 0.9
   - C112 Merrin Creek below Merrin Falls: -0.5
   - C113 Merrin Creek at Dunlop Road: 1.2
   - C114 Hallam Creek near the mouth: -0.9
   - C115 Garrow Creek at the springs: -1.8
   - C116 Cawdell Creek above the intake: 1.4
   - C117 Whitlow Creek at Marsh Road: -3.3
   - C118 Ostrey Creek near Hendry: 2.5
   - C119 Fallon River at the old bridge: -0.5
   - C120 Keddie Creek near Stowe: 2.2
   - C121 Rusk Creek at the fish fence: -1.0
   - C122 Mattin Creek at Quarry Road: -2.0
   - C123 Dorran Creek above the canyon: 1.7
   - C124 Merrin Creek near the mouth: -1.5
