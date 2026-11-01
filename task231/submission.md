## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: a highway district's road weather stations and its vendor's automated air temperature quality control).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Yes. The data quality standard sends eight stations back to Quillan for a re-tuned air temperature spatial test before winter 2027/28: SD-118 Halvorsen Meadow, SD-122 Bitterbrush Flat, SD-131 Teller Junction, SD-147 Kimball Grade, SD-204 Cutler Meadow, SD-211 Ransom Creek, SD-226 Echo Grade, SD-318 Ptarmigan Grade.**
Their false-rejection shares were 4.3, 16.1, 8.6, 11.5, 4.8, 6.8, 3.8, 4.2 per cent of the winter's 5,088 hours, against the standard's line of 2 per cent; the highest of the other stations was 0.5 per cent. At the basin floors the test withheld the cold pools' air on still nights, and at the three grades above the pools it withheld right readings because its estimate leaned on the cold floor stations nearby. Checked against an hourly lapse line or the HRRR forecast, the floor readings look wrong and only the three grades go on the list.

## 2. Critical Components

1. A withheld reading is right when it agrees within 2 C with the stations sharing its air that hour: a basin floor with its pool mates (Halvorsen Meadow, Bitterbrush Flat, Teller Junction; Cutler Meadow, Ransom Creek; Dutchman Flat, Hollis Junction; Upper Antler, Corrigan Lake; Maple Bend, Riverside Rest Area, Fenwick), any other station with the free-atmosphere stations within 50 km carried to its elevation at 6.5 C per km.
2. The cold floor readings the test withheld agree with their pool mates, so they count as false rejections: SD-118 4.3, SD-122 16.1, SD-131 8.6, SD-204 4.8, SD-211 6.8.
3. The grades above the pools agree with the free atmosphere around them: SD-147 11.5, SD-226 3.8, SD-318 4.2.
4. Withheld readings that were wrong and stay withheld: SD-158 connector (178 hours withheld, 0 right), SD-277 rime (239 hours withheld, 0 right), SD-336 rime (225 hours withheld, 17 right), SD-344 radiation shield (349 hours withheld, 0 right), SD-411 wet filter (67 hours withheld, 0 right).
5. The lapse-line route (each hour's elevation fit, within 5 C) re-tunes only SD-147, SD-226, SD-318.

## 3. Step-by-Step Solution

1. Joined the ESS export (tenths of a degree C, UTC hour-end stamps, RPU ids, re-sent rows kept once) to the site register and took the QC log's spatial-test air temperature rows, one per station and hour.
2. Each hour fitted the free-atmosphere line of temperature on elevation, refitted without stations more than 1.5 C below it.
3. Grouped the stations sharing a cold pool: night residuals from that line correlated above 0.8 on the hours both readings passed the QC, within 25 km and 80 m of each other, both below the line on an average night.
4. Judged each withheld reading against the median of its pool mates, or of the free-atmosphere stations within 50 km carried to its elevation at 6.5 C per km; right within 2 C, and every tolerance from 1.5 to 4.5 C gives the same hours.
5. Share = right withheld hours / 5,088 winter hours; re-tune above 2 per cent.
6. Unavailable hours: the message log's modems to sites through the modem register with removed modems kept and the unregistered spare placed at SD-171 Sheep Ridge by the export's observations, local times with their zone to UTC, each message's hours first to last, the earliest receipt within 20 minutes of the hour's end available, hours inside a notified outage excluded.
7. Freezing and ice hours: the pavement export with re-sent rows once, travel-lane ports only, each serial's model (replaced sensors from the register's notes) for its units, the firmware 4.1 code table from each serial's applied time and 3.4 before it and for SCAN-16 sensors.

## 4. Deliverable Answers

### spatial_check_retune_memo_2027.docx

1. Re-tune the spatial test before winter 2027/28 at: SD-118 Halvorsen Meadow, SD-122 Bitterbrush Flat, SD-131 Teller Junction, SD-147 Kimball Grade, SD-204 Cutler Meadow, SD-211 Ransom Creek, SD-226 Echo Grade, SD-318 Ptarmigan Grade.
2. Chart: every station's false-rejection share against the 2 per cent line, the re-tuned stations marked.

### rwis_spatial_check_review_2027.xlsx

1. False-rejection share of winter hours (per cent) and re-tune:
   - SD-109 0.2; SD-113 0.0; SD-118 4.3 re-tune; SD-122 16.1 re-tune; SD-127 0.0; SD-131 8.6 re-tune; SD-138 0.0; SD-147 11.5 re-tune; SD-158 0.0; SD-163 0.0; SD-171 0.0; SD-204 4.8 re-tune; SD-211 6.8 re-tune; SD-219 0.3; SD-226 3.8 re-tune; SD-233 0.0; SD-240 0.0; SD-251 0.0; SD-262 0.0; SD-277 0.0; SD-289 0.0; SD-307 0.5; SD-312 0.4; SD-318 4.2 re-tune; SD-336 0.3; SD-344 0.0; SD-351 0.1; SD-402 0.0; SD-405 0.0; SD-411 0.0; SD-416 0.0
2. Unavailable hours under Schedule B: SD-109 652; SD-113 544; SD-118 293; SD-122 423; SD-127 412; SD-131 276; SD-138 290; SD-147 264; SD-158 359; SD-163 211; SD-171 366; SD-204 197; SD-211 439; SD-219 319; SD-226 368; SD-233 543; SD-240 256; SD-251 328; SD-262 242; SD-277 372; SD-289 362; SD-307 479; SD-312 385; SD-318 409; SD-336 382; SD-344 397; SD-351 275; SD-402 315; SD-405 202; SD-411 510; SD-416 482.
3. Travel-lane freezing hours: SD-109 2,835; SD-113 3,067; SD-118 3,163; SD-122 3,212; SD-127 2,993; SD-131 3,205; SD-138 2,648; SD-147 3,496; SD-158 3,582; SD-163 4,049; SD-171 4,095; SD-204 3,481; SD-211 3,440; SD-219 3,571; SD-226 3,860; SD-233 3,472; SD-240 3,986; SD-251 3,165; SD-262 4,189; SD-277 4,367; SD-289 4,028; SD-307 3,697; SD-312 3,810; SD-318 4,141; SD-336 4,393; SD-344 3,484; SD-351 3,521; SD-402 2,853; SD-405 2,781; SD-411 2,924; SD-416 3,243.
4. Travel-lane ice hours: SD-109 617; SD-113 682; SD-118 604; SD-122 631; SD-127 658; SD-131 619; SD-138 575; SD-147 783; SD-158 801; SD-163 875; SD-171 885; SD-204 750; SD-211 723; SD-219 776; SD-226 858; SD-233 744; SD-240 870; SD-251 704; SD-262 895; SD-277 907; SD-289 889; SD-307 810; SD-312 835; SD-318 885; SD-336 898; SD-344 794; SD-351 803; SD-402 599; SD-405 588; SD-411 612; SD-416 724.
