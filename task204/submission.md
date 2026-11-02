## Tags

**Domain:** Criminology and justice, crime incidence and hotspot analysis (offender series linkage).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The summer plan should stand up four series teams: the Eastline group's team on districts 4, 6, 7 and 9, the Hollin station group's on district 5, the Cobb Street station group's on district 8 and the district 6 street robbery group's on district 6.**
The Eastline group's 42 offences are one series because 18 westbound trains each carried two or three of its snatches at different stations. Not seven teams, one per station cluster, which splits that group four ways by straight-line distance. Not three teams, which folds the Cobb Street group into it although on four evenings the two struck within three minutes of each other at stations no train joins in that time.

## 2. Critical Components

1. The Eastline group is **42** offences on the platforms at Ridgeview, Ashford Road, Millbrook and Union Yards, joined by **18** westbound train trips that each carried two or three of them; its ground is **districts 4, 6, 7 and 9**.
2. The Cobb Street station group is a separate group of **16** offences on **district 8**: none of its snatches sits on one of those trips, and on **4** evenings it struck within three minutes of the Eastline group at Union Yards.
3. The Hollin station group is **18** offences on **district 5** and the district 6 street robbery group **14** offences on **district 6**.
4. Patrol **districts 1, 2, 3 and 10** have no series in the review period.

## 3. Step-by-Step Solution

1. Took robbery and theft from the person with a phone taken (OPS-41 section 2) from rms_occurrence_extract_20260511.csv by occurred_from_local, 9 February to 3 May 2026, with the transit officer reports in tpo_occurrence_log_2025_2026.xlsx not already filed with the Service, and kept the 99 with two or more suspects (an offender group, section 3).
2. Linked those offences on method, overlapping suspect ages, 1 km and 28 days: seven local series, one each at Ridgeview, Ashford Road, Millbrook, Union Yards, Cobb Street and Hollin and one of street robberies in district 6.
3. Placed each platform offence on the train trips leaving its station within three minutes of occurred_from_local, from the gtfs/ feed with frequencies.txt expanded and calendar_dates.txt applied: 18 trips each carry two or three offences at different stations and join the Ridgeview, Ashford Road, Millbrook and Union Yards series into one group of 42.
4. Kept Cobb Street apart: no trip carries one of its offences with another, and four of its offences fell within three minutes of an Eastline group offence at Union Yards.
5. Took each group's ground from its offences' coordinates in patrol_districts_2026.geojson (OPS-41 section 4): four teams.
6. 2025 comparison: put each 2025 RMS offence in its 2026 district by coordinates, read each transit officer station code as the station whose gate array carried that code on the day (fare_gate_daily_summary_2025.csv with carvale_transit_codes.xlsx), dropped reports referred to the Service that match an RMS file at the same station, and counted by Mountain-time date: 257 offences.
7. Station figures: summed fare_gate_entries_hourly_2026.csv by gate array (codes were renumbered on 29 March) on Mountain-time dates, and counted every Eastline stop_times call with frequencies.txt trips expanded and calendar_dates.txt holiday services applied, in the twelve weeks.
8. Recommendation: the four teams in block 1.

## 4. Deliverable Answers

### series_assessment_2026.xlsx

1. Series teams, 4, with ground and series offences in the review period:
   - Eastline group: districts 4, 6, 7 and 9, 42 offences
   - Hollin station group: district 5, 18 offences
   - Cobb Street station group: district 8, 16 offences
   - District 6 street robbery group: district 6, 14 offences
2. Robbery and theft from the person with a phone taken, 2026 patrol districts, same twelve weeks of 2025:
   - District 1: 13 (10 Feb to 9 Mar 2025), 8 (10 Mar to 6 Apr 2025), 13 (7 Apr to 4 May 2025)
   - District 2: 6 (10 Feb to 9 Mar 2025), 8 (10 Mar to 6 Apr 2025), 10 (7 Apr to 4 May 2025)
   - District 3: 12 (10 Feb to 9 Mar 2025), 19 (10 Mar to 6 Apr 2025), 7 (7 Apr to 4 May 2025)
   - District 4: 11 (10 Feb to 9 Mar 2025), 8 (10 Mar to 6 Apr 2025), 13 (7 Apr to 4 May 2025)
   - District 5: 5 (10 Feb to 9 Mar 2025), 7 (10 Mar to 6 Apr 2025), 3 (7 Apr to 4 May 2025)
   - District 6: 10 (10 Feb to 9 Mar 2025), 9 (10 Mar to 6 Apr 2025), 12 (7 Apr to 4 May 2025)
   - District 7: 7 (10 Feb to 9 Mar 2025), 6 (10 Mar to 6 Apr 2025), 7 (7 Apr to 4 May 2025)
   - District 8: 5 (10 Feb to 9 Mar 2025), 5 (10 Mar to 6 Apr 2025), 9 (7 Apr to 4 May 2025)
   - District 9: 13 (10 Feb to 9 Mar 2025), 6 (10 Mar to 6 Apr 2025), 8 (7 Apr to 4 May 2025)
   - District 10: 7 (10 Feb to 9 Mar 2025), 9 (10 Mar to 6 Apr 2025), 1 (7 Apr to 4 May 2025)
3. Eastline stations, 9 February to 3 May 2026, fare-gate entries and scheduled Eastline train calls in both directions:
   - Westgate: 222,832 entries, 16,360 train calls
   - Centre Square: 709,302 entries, 16,360 train calls
   - Union Yards: 194,321 entries, 16,864 train calls
   - Millbrook: 311,291 entries, 16,528 train calls
   - Fairgrounds: 45,586 entries, 7,166 train calls
   - Cobb Street: 171,545 entries, 16,528 train calls
   - Ashford Road: 158,588 entries, 14,498 train calls
   - Ridgeview: 276,132 entries, 13,976 train calls
   - Prairie Gate: 235,756 entries, 13,976 train calls

### summer_series_deployment_memo.docx

1. One-page memo to the deputy chief recommending the four series teams and their ground as in item 1 above, with the reason the Eastline group is one group and the Cobb Street group another.
