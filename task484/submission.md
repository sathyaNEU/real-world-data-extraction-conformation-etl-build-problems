## Tags

**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Nine of the sections the Council counted in 2025 carried more than three million vehicles and go into the noise mapping contract's scope: Ashfield Road, Brookfield Way, Hollins Lane, Holloway Hill, Infirmary Road, Kingsway, Priory Road, Station Street and Wharf Street.** Not the set the permanent counters' factors give, which puts College Road and Grange Road over the line and leaves Brookfield Way, Hollins Lane and Infirmary Road under it: those sections' weeks and years follow the school, the campus, the retail park, the leisure park and the hospital at their ends, not the commuter roads the counters sit on, and each one's own year is on the signal detectors of its approach.

## 2. Critical Components

1. Over the line on their own detectors: Brookfield Way 3.4 million; Hollins Lane 3.2 million; Infirmary Road 3.2 million.
2. Under it on their own detectors: College Road 2.5 million; Grange Road 2.7 million; Castlegate Road 2.6 million.
3. The other sections over 3.0 million: Ashfield Road 3.8; Holloway Hill 3.4; Kingsway 4.3; Priory Road 3.4; Station Street 3.6; Wharf Street 5.0.

## 3. Step-by-Step Solution

1. Read traffic_estimate_terms_2025.pdf (a section's annual traffic is every motor vehicle passing along it, both directions, on all days of the year) and noise_mapping_2026_scope.pdf (every section counted in 2025; over three million vehicle passages is mapped).
2. Summed each section's 2025 manual count in manual_counts_2025.csv (all motor vehicles, 07:00 to 19:00, both directions) by count point.
3. Found each section's own approach in utc_asset_register_2025.xlsx: the junction named by the section's road and one of its end roads in count_points_2025.xlsx (street types abbreviated in the register), and on it the detectors whose approach is the section's road; Brookfield Way, Castlegate Road, College Road, Grange Road, Hollins Lane, Infirmary Road, Kingsway, Mill Lane and Station Street have one.
4. For those sections: the count times the detectors' mean full day over 2025 in utc_detector_daily_2025.csv, over the same detectors' 07:00 to 19:00 flow on the count day (the detectors see one approach, so their level cancels).
5. For the rest: the count times the same-day ratio of the permanent counters in the section's setting (atc_daily_2025.csv, atc_sites_2025.csv), their annual mean over their 07:00 to 19:00 flow on the count day.
6. Annual traffic is the daily flow times 365; 9 sections are over 3.0 million.
7. Counters' heavy goods vehicles: classes 5 to 7 of the legacy table until 2025-09-08, when the outstations' channel 5 switched from two-axle rigid lorries to buses, and classes 6 to 8 of the TX-8 table from it, averaged over each counter's recorded days.
8. The two renewed junctions: each channel's series before its renewal matched to the current channel carrying the same lane on level and weekend shares across the dark days, then each approach's recorded vehicles summed over 2025.

## 4. Deliverable Answers

### noise_round_sections_2025.csv

1. 2025 annual traffic, millions of vehicles, and whether over three million:
   - Ashfield Road (count point 466552, 0.73 km): 3.8, yes
   - Brookfield Way (count point 828200, 0.62 km): 3.4, yes
   - Castlegate Road (count point 476623, 0.95 km): 2.6, no
   - College Road (count point 542938, 0.58 km): 2.5, no
   - Cradock Lane (count point 438496, 1.37 km): 2.3, no
   - Grange Road (count point 778164, 0.74 km): 2.7, no
   - Hollins Lane (count point 440787, 0.81 km): 3.2, yes
   - Holloway Hill (count point 352234, 1.48 km): 3.4, yes
   - Infirmary Road (count point 929104, 0.47 km): 3.2, yes
   - Kingsway (count point 477800, 0.69 km): 4.3, yes
   - Lower Heath Road (count point 699061, 1.92 km): 1.5, no
   - Mill Lane (count point 410389, 0.88 km): 2.6, no
   - Oakhill Road (count point 578667, 0.79 km): 2.0, no
   - Priory Road (count point 705957, 0.66 km): 3.4, yes
   - Sandy Lane (count point 528367, 0.57 km): 2.4, no
   - Station Street (count point 424332, 0.52 km): 3.6, yes
   - Tanhouse Lane (count point 526023, 0.84 km): 2.5, no
   - Wharf Street (count point 979192, 0.41 km): 5.0, yes

### section_traffic_2025.png

1. One horizontal bar per counted section with its 2025 traffic, a dashed line at 3.0 million and the sections over it in red.

### traffic_network_2025.xlsx

1. Counters, heavy goods vehicles a day in 2025:
   - WRA291 (Pelham Lane): 350
   - WRA302 (Lea Road): 640
   - WRA472 (Coventry Road): 780
   - WRA508 (Stafford Road): 1060
   - WRA661 (Birmingham Road): 1380
   - WRA689 (Northgate Road): 850
   - WRA754 (Ashby Road): 400
   - WRA756 (Western Avenue): 1590
   - WRA843 (Lichgate Road): 440
   - WRA872 (Ring Road North): 1740
   - WRA898 (Fenwick Road): 1120
2. Vehicles recorded on each approach in 2025, thousands:
   - Ring Road / Tanyard Lane, Ring Road EB: 4,373
   - Ring Road / Tanyard Lane, Ring Road WB: 3,217
   - Ring Road / Tanyard Lane, Tanyard Lane NB: 1,396
   - Ring Road / Tanyard Lane, Tanyard Lane SB: 1,680
   - Western Avenue / Fenwick Road, Fenwick Road EB: 2,715
   - Western Avenue / Fenwick Road, Fenwick Road WB: 1,893
   - Western Avenue / Fenwick Road, Western Avenue NB: 3,875
   - Western Avenue / Fenwick Road, Western Avenue SB: 4,979
