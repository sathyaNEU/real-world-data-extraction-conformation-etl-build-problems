## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: a highway district's road weather stations and its vendor's automated air temperature quality control).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Yes. The data quality standard sends eight stations back to Quillan for a re-tuned air temperature spatial test before winter 2027/28: SD-118 Halvorsen Meadow, SD-122 Bitterbrush Flat, SD-131 Teller Junction, SD-147 Larkspur Grade, SD-204 Cutler Meadow, SD-211 Ransom Creek, SD-226 Antimony Grade, SD-318 Ptarmigan Grade.**
Their false-rejection shares were 4, 14, 11, 14, 5, 8, 3, 3 per cent of the winter's 5,088 hours, against the standard's line of 2 per cent; every other station rounds to 0 per cent. At the basin floors the test withheld the cold pools' air on still nights, and at the three grades above the pools it withheld right readings because its estimate leaned on the cold floor stations nearby. Checked against an hourly lapse line or the HRRR forecast, the floor readings look wrong and only the three grades go on the list.

## 2. Critical Components

1. A withheld reading is right when it agrees within 2 C with the stations sharing its air that hour: a basin floor with its pool mates (Halvorsen Meadow, Bitterbrush Flat, Teller Junction; Cutler Meadow, Ransom Creek; Dutchman Flat, Hollis Junction; Upper Antler, Corrigan Lake; Maple Bend, Riverside Rest Area, Fenwick), any other station with the free-atmosphere stations within 50 km carried to its elevation at 6.5 C per km.
2. The cold floor readings the test withheld agree with their pool mates, so they count as false rejections: SD-118 4, SD-122 14, SD-131 11, SD-204 5, SD-211 8.
3. The grades above the pools agree with the free atmosphere around them: SD-147 14, SD-226 3, SD-318 3.
4. Withheld readings that were wrong and stay withheld: SD-158 connector (181 hours withheld, 0 right), SD-277 rime (240 hours withheld, 0 right), SD-336 rime (205 hours withheld, 0 right), SD-344 radiation shield (335 hours withheld, 0 right), SD-411 wet filter (65 hours withheld, 0 right).
5. The lapse-line route (each hour's elevation fit, within 5 C) re-tunes only SD-147, SD-226, SD-318.

## 3. Step-by-Step Solution

1. Joined the ESS export (tenths of a degree C, UTC hour-end stamps, RPU ids, re-sent rows kept once) to the site register and took the QC log's spatial-test air temperature rows, one per station and hour.
2. Each hour fitted the free-atmosphere line of temperature on elevation, refitted without stations more than 1.5 C below it.
3. Grouped the stations sharing a cold pool: night residuals from that line correlated above 0.8 on the hours both readings passed the QC, within 25 km and 80 m of each other, both below the line on an average night.
4. Judged each withheld reading against the median of its pool mates, or of the free-atmosphere stations within 50 km carried to its elevation at 6.5 C per km; right within 2 C, and every tolerance from 1.5 to 4.5 C gives the same hours.
5. Share = right withheld hours / 5,088 winter hours; re-tune above 2 per cent.
6. Unavailable hours: the message log's modems to sites through the modem register with removed modems kept, and each spell of a shop spare's messages placed at the one station whose export readings it carried (SD-171 Sheep Ridge, SD-211 Ransom Creek, SD-351 Antelope Bench, SD-411 Fenwick); local times with their zone to UTC, each message's hours first to last, the earliest receipt within 20 minutes of the hour's end available, hours inside a notified outage excluded; summed by maintenance section.
7. Freezing and ice hours: the pavement export with re-sent rows once, travel-lane ports only, the heads that came out during the winter kept on their RPU and port (IR65369, SC23676, SC23693, SC57331, an IRS-31 reporting whole tenths of a degree C, a SCAN-16 degrees F), the firmware 4.1 code table from each serial's applied time and 3.4 before it and for SCAN-16 sensors; summed by maintenance section.

## 4. Deliverable Answers

### spatial_check_retune_memo_2027.docx

1. Re-tune the spatial test before winter 2027/28 at: SD-118 Halvorsen Meadow, SD-122 Bitterbrush Flat, SD-131 Teller Junction, SD-147 Larkspur Grade, SD-204 Cutler Meadow, SD-211 Ransom Creek, SD-226 Antimony Grade, SD-318 Ptarmigan Grade.
2. Chart: every station's false-rejection share against the 2 per cent line, the re-tuned stations marked.

### rwis_spatial_check_review_2027.xlsx

1. False-rejection share of winter hours (whole per cent) and re-tune:
   - SD-109 0; SD-113 0; SD-118 4 re-tune; SD-122 14 re-tune; SD-127 0; SD-131 11 re-tune; SD-138 0; SD-147 14 re-tune; SD-158 0; SD-163 0; SD-171 0; SD-204 5 re-tune; SD-211 8 re-tune; SD-219 0; SD-226 3 re-tune; SD-233 0; SD-240 0; SD-251 0; SD-262 0; SD-277 0; SD-289 0; SD-307 0; SD-312 0; SD-318 3 re-tune; SD-336 0; SD-344 0; SD-351 0; SD-402 0; SD-405 0; SD-411 0; SD-416 0
2. Unavailable station-hours under Schedule B: Sawyer 1 1,225; Sawyer 2 851; Sawyer 3 1,391; Sawyer 4 1,105; network 4,572.
3. Travel-lane freezing station-hours: Sawyer 1 21,386; Sawyer 2 27,025; Sawyer 3 33,118; Sawyer 4 27,330; network 108,859.
4. Travel-lane ice station-hours: Sawyer 1 4,644; Sawyer 2 5,719; Sawyer 3 7,186; Sawyer 4 5,893; network 23,442.
