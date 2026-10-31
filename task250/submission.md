# task250 submission

## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a parcel carrier's sort-scan completeness, where the hub an unscanned parcel passed through is itself missing and is recovered from the unloading it arrived in at its delivery depot).
**Analytical objective:** Data Quality Monitoring & Alerting (whether the TDS-4 scan alert fires at any of Kurier Warta's sort hubs for October 2026, and at which).

## 1. Final Recommendation

**Fire the October 2026 scan alerts at Sosnowiec, Strykow and Pruszkow, and at no other hub.**

Sosnowiec missed 1.34 per cent of its sort scans, Strykow 1.55 and Pruszkow 1.23, against the 1.00 per cent tolerance; the nearest hub under it is Bielany Wroclawskie at 0.79. On 24 mornings the Warsaw depots unloaded a second trailer from Strykow, which had sorted 1,440 parcels of Pruszkow's flow by hand; 130 of their sort scans are missing, against 205 missing from Pruszkow's own trailers on those mornings, so a parcel without a sort scan is charged to the hub whose trailer it came off, read from its unloading. Not the sort plan's hub, which charges Strykow's misses to Pruszkow (Pruszkow 1.76, Strykow 0.49) and leaves Strykow under the line. Not each depot morning's split of its sorted parcels, which assumes the two hubs missed alike (Strykow 0.77). Not the mornings with two hubs left out (Pruszkow 0.86, Strykow 0.55), nor the excess over Pruszkow's rate on its other mornings charged to Strykow (Strykow 2.30, Pruszkow 0.86): Pruszkow's own sorter missed more on the same heavy nights, so both clear Pruszkow.

## 2. Critical Components

1. Missed-scan rate by hub: Komorniki **0.48** per cent; Bielany Wroclawskie **0.79** per cent; Sosnowiec **1.34** per cent; Modlniczka **0.63** per cent; Strykow **1.55** per cent; Pruszkow **1.23** per cent
2. Parcels handled and missed sort scans at the three hubs that fire: Sosnowiec **16,530** and **222**; Strykow **12,178** and **189**; Pruszkow **24,425** and **301**
3. The mornings with two trailers: **24** depot mornings at Warszawa-Okecie and Warszawa-Targowek; **1,440** parcels off Strykow's trailers, **130** of them without a sort scan

## 3. Step-by-Step Solution

1. Took October's parcels from depot_scan_events_2026-10.csv, one per tracking number unloaded on the mornings of 1 to 31 October (TDS-4 s.2.1; the rows re-sent on 21 October are the same rows again): 91,324 parcels.
2. Took each parcel's hub from hub_sort_events_2026-10.parquet where it has a sort event (one hub per parcel; a second read on the sorter loop is the same sort); a parcel with none is a missed sort scan (s.2.2).
3. Split each depot door's arrival scans into unloadings wherever the door stood idle for more than ten minutes (any pause from one to 29 minutes gives the same 300 unloadings), and found every unloading's sorted parcels carrying one hub.
4. Charged each parcel without a sort scan to its unloading's hub, then counted each hub's parcels, missed sort scans and rate, and fired the alert above 1.00 per cent (s.2.3).
5. Courier events sent twice (TDS-4 s.3): a later-received record of the same parcel, event, courier and handheld carrying the first record's time cut to the minute, as local time from a TC52 and as UTC from a TC51 (two hours behind local until 25 October, one after); a second loop or the afternoon wave is a new scan; counted under the depot the event names.
6. Pre-advised parcels never picked up (TDS-4 s.4): each consignment's latest version with an October collection date, D-KRK1 read as D-KRK3 from 12 October, its pieces as parcels; a parcel the platform holds a pickup, sort, arrival or delivery record for was collected (trailer collections carry no pickup scan) and a failed pickup is not a collection; a piece label is the consignment number plus a three-digit piece number, and a marketplace order is matched on its first 20 characters, the orders sharing them counted against their pickups.

## 4. Deliverable Answers

### tracking_scorecard_2026-10.xlsx

1. Each hub's parcels handled, missed sort scans, missed-scan rate and alert:
   - Komorniki (HPOZ): 12,600 parcels, 61 missed, 0.48 per cent, does not fire
   - Bielany Wroclawskie (HWRO): 11,963 parcels, 95 missed, 0.79 per cent, does not fire
   - Sosnowiec (HKTW): 16,530 parcels, 222 missed, 1.34 per cent, fires
   - Modlniczka (HKRK): 13,628 parcels, 86 missed, 0.63 per cent, does not fire
   - Strykow (HLDZ): 12,178 parcels, 189 missed, 1.55 per cent, fires
   - Pruszkow (HWAW): 24,425 parcels, 301 missed, 1.23 per cent, fires
2. Each depot's courier events sent twice and pre-advised parcels never picked up:
   - D-POZ1 Poznan-Gluszyna: 581 sent twice, 106 never picked up
   - D-POZ2 Leszno: 125 sent twice, 257 never picked up
   - D-WRO1 Wroclaw-Pracze: 600 sent twice, 162 never picked up
   - D-WRO2 Opole: 272 sent twice, 139 never picked up
   - D-KTW1 Katowice-Zaleze: 324 sent twice, 110 never picked up
   - D-KTW2 Bielsko-Biala: 375 sent twice, 195 never picked up
   - D-KRK1 Krakow-Zablocie: 97 sent twice, 43 never picked up
   - D-KRK3 Krakow-Rybitwy: 200 sent twice, 86 never picked up
   - D-KRK2 Tarnow: 127 sent twice, 170 never picked up
   - D-LDZ1 Lodz-Olechow: 599 sent twice, 189 never picked up
   - D-LDZ2 Piotrkow Trybunalski: 292 sent twice, 309 never picked up
   - D-WAW1 Warszawa-Okecie: 942 sent twice, 145 never picked up
   - D-WAW2 Warszawa-Targowek: 736 sent twice, 346 never picked up

### scan_alerts_2026-10.pptx

3. One slide: a horizontal bar chart of each hub's missed-scan rate against the 1.00 per cent tolerance line, the bars of Sosnowiec, Strykow and Pruszkow marked as firing and the other three under the line, beside the six hubs' parcels, missed sort scans, rates and alerts.
