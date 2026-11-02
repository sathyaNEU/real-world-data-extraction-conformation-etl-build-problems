## Tags

**Domain:** Urban & Regional Science (forecasting: a metropolitan transport authority's weekday commuter boardings at a new commuter-rail station, built from census place-of-work flows and a mobile network operator's resident stay panel).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Rathgarvan will carry about 1,300 commuter boardings on an average ordinary weekday in 2029 (to the nearest 100), below the 1,400 that justifies the full scheme, so build the reduced scheme.** A boarding is a journey to work made on the day, and the catchment's census commuters do not go in every weekday: the panel shows the Docklands commuters going in on 2.52 days a week, the hospital's on 2.78 and Carrigboy's on 2.73. Counting each census commuter as a boarding every weekday gives about 2,400 and the full scheme.

## 2. Critical Components

1. Weekday commuter boardings in 2029: **1,300** (to the nearest 100; 1312.0 before rounding), 88 below the full-scheme threshold of 1,400.
2. Scope: **reduced scheme**.
3. Boardings by workplace zone (nearest 10): University Hospital campus 360; Kilcarrow city centre 310; Kilcarrow Docklands 290; Carrigboy business park 150; Kilcarrow University 80; Lisnagry and Ardnagree 50; Port of Kilcarrow, Ringcurran 40; Airport business park 20; Ballymurragh retail park 10; Rest of County Kilcarrow 10.

## 3. Step-by-Step Solution

1. Census 2022 place-of-work tables, final release: commuters from the seven catchment small areas by workplace zone, held at 2022; home workers, no fixed place and outside the county left out.
2. Panel: stays converted from UTC to Irish time; 55 ordinary weekdays from 6 September to 26 November 2027 (October bank holiday and mid-term week out, from the calendar file).
3. Each device's usual workplace: the zone (cell lookup, largest area share) of most of its stays of four hours or more away from its home cell, where it has at least three; each identifier over its own first to last day.
4. Share of ordinary weekdays each zone's commuters travel there (commuting days over observed days): KW01 54.4 per cent; KW02 50.4 per cent; KW03 55.6 per cent; KW04 53.9 per cent; KW05 54.7 per cent; KW06 73.5 per cent; KW07 78.1 per cent; KW08 74.6 per cent; KW09 78.8 per cent; KW11 72.0 per cent.
5. Boardings per zone = census commuters x station share (refresh Table 2) x that share; summed, 1312.0; against the threshold of 1,400, the reduced scheme.
6. Arrival shares: each commuting day's workplace stay start in Irish time, 07:30 to 09:30 inclusive, over the zone's commuting days.
7. Station shares: ordinary-weekday entries, September to November, summed per station-day over the station's codes (UHK with KUH, CBH with CBY) and every gateline code G<station number><gateline>; 2027 average over 2019 average.

## 4. Deliverable Answers

### rathgarvan_boardings_2029.xlsx

1. Weekday commuter boardings, 2029: 1,300 (nearest 100).
2. Boardings by workplace zone (nearest 10):
   - KW01 Kilcarrow city centre: 310
   - KW02 Kilcarrow Docklands: 290
   - KW03 University Hospital campus: 360
   - KW04 Kilcarrow University: 80
   - KW05 Carrigboy business park: 150
   - KW06 Port of Kilcarrow, Ringcurran: 40
   - KW07 Ballymurragh retail park: 10
   - KW08 Airport business park: 20
   - KW09 Lisnagry and Ardnagree: 50
   - KW11 Rest of County Kilcarrow: 10
3. Share of journeys to work reaching the workplace between 07:30 and 09:30 (whole per cent):
   - KW01 Kilcarrow city centre: 83 per cent
   - KW02 Kilcarrow Docklands: 93 per cent
   - KW03 University Hospital campus: 92 per cent
   - KW04 Kilcarrow University: 97 per cent
   - KW05 Carrigboy business park: 40 per cent
   - KW09 Lisnagry and Ardnagree: 99 per cent
4. Average ordinary-weekday entries, September to November 2027 as a share of the same months of 2019 (whole per cent):
   - Ardnagree: 73 per cent
   - Lisnagry: 74 per cent
   - Kilcarrow Central: 65 per cent
   - Kilcarrow Docklands: 56 per cent
   - University Hospital (with UHK): 83 per cent
   - Carrigboy (with Carrigboy Halt): 79 per cent
   - Ardnagree line: 68 per cent

### rathgarvan_demand_note.docx

1. Call: about 1,300 commuter boardings on an average ordinary weekday in 2029, below 1,400, reduced scheme.
2. Chart: boardings by workplace zone, the values in item 2 above.
