# task245 submission

## Tags

**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance: a borough air quality network's 2027 PM10 results against the 24-hour objective, each station's lost days counted).
**Analytical objective:** Data Quality Monitoring & Alerting (which stations' 2027 PM10 results carry the data-capture note into the Annual Status Report, with the NO2 annual mean at each council NO2 station and the dust deposition rate at each terminal gauge beside them).

## 1. Final Recommendation

**Three stations go into the 2027 Annual Status Report with the data-capture note: North Gate (TBT1), Harbour Walk (TH3) and South Yard (TBT4) count 22, 17 and 19 days above 50 µg/m³ among their valid daily means but 57, 51 and 51 over the whole year once their lost days are rebuilt; the other nine carry no note.**

Their analysers stopped on the days the terminal's dust blew onto them (the wind came from the terminal for six hours or more on 103 of their 229 lost days, against 72 of their 866 valid days), so the lost days are rebuilt from the other stations' median and each station's own response to the wind. Not the count scaled by data capture, which notes Market Street and Westholme Avenue (37.8 and 41.9), whose long outages fell in quiet spells, and none of the three. Not the lost days filled from the other stations alone, or by interpolation in time, which leave all three at 35 or under.

## 2. Critical Components

1. Whole-year days above 50 at the three noted stations (accepted range): **TBT1 57 (39 to 61); TH3 51 (45 to 58); TBT4 51 (44 to 56)**, more than 35 under every rebuild choice.
2. Their days above 50 among valid daily means: **TBT1 22; TH3 17; TBT4 19**, each 35 or fewer.
3. Market Street and Westholme Avenue over the whole year: **30 and 30** (23 to 33, 26 to 34), no note.

## 3. Step-by-Step Solution

1. Hourly PM10 on one grid: the council's export (status R only) and the terminal's workbook (status OK only; UK clock time, hour beginning, moved to GMT hour ending, the repeated 01:00 of 31 October read as BST then GMT).
2. Daily means of the valid hours where at least 18 are valid (AQ-QP-04 section 3) and, per station, the days above 50 among them.
3. The three stations' lost days against the port's met mast: the reported wind direction was within 22.5 degrees of the bearing from the station to the stockyard centre (the register's grid references, the plan's centre) for six hours or more on 103 of their 229 lost days and 72 of their 866 valid days, and on those valid days they averaged 53.9, 82.1 and 63.0 against the other stations' median daily mean of 19.9, 22.2 and 21.0.
4. Rebuild of every hour without a valid mean: the median of the other stations' valid hourly means that hour, plus the station's mean increment over that median in the hour's wind cell (16 sectors, speed under or at least 4 m/s, wet or dry day, a day being wet when the mast's rain totals more than 0.2 mm; a cell with fewer than five valid hours takes the sector's mean), taken from its valid hours; calm or missing directions take the nearest reported hour's.
5. Whole-year count (section 5.1): the valid daily means plus, for each day without one, the mean of its valid and rebuilt hours; the accepted range is the lowest to highest count under the other rebuild choices (4, 8, 12, 16 or 36 sectors or a smooth fit in the direction, with or without speed and rain, the council's background stations, the rural station or a station-and-hour fit as the background), a day either side.
6. The note (section 5.2): TBT1, TH3 and TBT4, each with 35 or fewer valid-day exceedances and more than 35 over the year.
7. NO2 (section 5.3): each council NO2 station's valid hours, each hour once (a week the analyser's store sent twice dropped), the hours from its new logger's fitting in June (service log, converted at 1.88) multiplied by 1.91/1.88.
8. Deposition (plan revision 3, section 3): each terminal gauge's periods that started in 2027, the void period out, each period's total deposit over the collecting area of the gauge exposed then (the laboratory's 0.0731 m2 to the 7 June exchange, the 227 mm Frisbee gauge's 0.0405 m2 from it, plan Annex A and service log) and its days, weighted by days.

## 4. Deliverable Answers

### thornmouth_pm10_2027_data_capture_review.xlsx

1. Stations, 12 rows in the register's order: days above 50 ug/m3 over the whole of 2027 (accepted range) and the note:
   - North Gate (TBT1): 57 over the whole year (39 to 61); note
   - East Berth (TBT2): 14 over the whole year (11 to 17); no note
   - Harbour Walk (TH3): 51 over the whole year (45 to 58); note
   - South Yard (TBT4): 51 over the whole year (44 to 56); note
   - Rail Sidings (TBT3): 16 over the whole year (15 to 17); no note
   - West Gate (TBT5): 14 over the whole year (8 to 16); no note
   - Market Street (TH5): 30 over the whole year (23 to 33); no note
   - Westholme Avenue (TH6): 30 over the whole year (26 to 34); no note
   - Town Hall (TH1): 24 over the whole year (23 to 25); no note
   - Grangefield (TH2): 15 over the whole year (14 to 16); no note
   - Ellerby Road (TH4): 11 over the whole year (10 to 12); no note
   - Rookwood Farm (TH7): 2 over the whole year (1 to 3); no note
2. NO2 annual mean 2027, ug/m3 to one decimal:
   - Harbour Walk (TH3) 19.0
   - Market Street (TH5) 29.0
   - Westholme Avenue (TH6) 26.3
   - Town Hall (TH1) 19.4
   - Grangefield (TH2) 15.5
   - Ellerby Road (TH4) 23.7
3. Dust deposition rate 2027, mg/m2 per day, whole number:
   - North Gate (TBT1) 69
   - East Berth (TBT2) 61
   - South Yard (TBT4) 60
   - Rail Sidings (TBT3) 59
   - West Gate (TBT5) 46

### asr2027_pm10_data_capture_note.pdf

- One page for the auditor: the three noted stations, why their lost days count, and a chart of every station's days above 50 over its valid daily means (open) and over the whole year (filled) against the 35-day line, the three noted stations marked.
