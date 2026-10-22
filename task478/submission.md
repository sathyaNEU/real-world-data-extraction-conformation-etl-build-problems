## Tags

**Domain:** General Statistics & Data Science (data integration: a turnpike authority's twelve weigh-in-motion stations of two sensor types conformed onto the static scale's weight basis through each station's loaded class 9 steer axles against the scale houses' tickets, then counted against the 80,000-lb gross limit by section).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Equip Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle Run with the 2027 virtual weigh stations.**
With each station's weights on the static scale's basis, 11, 16, 21, 11 and 11 per cent of the class 9 trucks their stations weighed in 2026 ran over 80,000 lb, against Dunmere's 7 per cent in sixth. Not Brannock or Ingram Mill, which lead on the weights as recorded (9 and 10 per cent) only because their stations read 6 and 5 per cent heavy; not Dunmere, which comes in only when the steer axles of empty and loaded tractors are pooled.

## 2. Critical Components

1. Against the scale houses' loaded static tickets, on the steer axles of loaded class 9 trucks, Brannock's and Ingram Mill's stations read **6 and 5** per cent heavy and Elk Ferry's and Kettle Run's **5 and 4** per cent light.
2. The lowest of the five shares is **11** per cent, against Dunmere's **7** in sixth.

## 3. Step-by-Step Solution

1. Read ctpa_wim_piezo_2026.txt (fixed width, tens of pounds) and ctpa_wim_bendingplate_2026.csv (kilograms), kept the class 9 weighings the controllers did not reject and put each station in its section by its milepost in ctpa_wim_stations.csv: 155,032 class 9 trucks weighed.
2. Took the loaded trucks in ctpa_scale_house_tickets_2026.xlsx (five axles summing over 50,000 lb): their steer axle's median on the static scale is 11,420 lb.
3. Divided each station's median steer axle of its loaded class 9 trucks (gross over 50,000 lb as recorded) by that median: factors from 0.951 (Elk Ferry) to 1.066 (Foxbriar).
4. Divided every weighing's gross by its station's factor and took each section's share over 80,000 lb (program 3.2): Cole Hollow 11, Elk Ferry 16, Garnet Ridge 21, Jessup Fork 11 and Kettle Run 11 lead, Dunmere is sixth at 7 per cent.
5. For the weekday entries, took each entry in ctpa_toll_entries_5axle_2026.csv once: a T26 row stamped up to 16 minutes before a numeric-id row of the same tag and plaza is the new host's backfill of that entry (the plazas moved one by one in May and June) and goes; the numeric-id rows are the old host's local stamps and the other T26 rows UTC; placed plaza P23 at Brannock Road to 30 April (ctpa_toll_schedule_2025.pdf) and at Halbrook East from 1 September (ctpa_toll_plazas.csv), and averaged over the 261 weekdays (program 5): 502 five-axle entries a weekday on the turnpike.
6. For the citations, placed each violation G row of ctpa_citations_2026.csv at its tag's last toll entry before the stop, the trip weighed (program 6.2), on those entries with the old host's stamps read as local time (read as UTC, the entry a cited truck makes coming back through the barrier after offloading falls before its stop), not at its entry_plaza, which the toll system returned when the citation was keyed: 1,279 gross overweight citations.
7. Recommended the five highest shares: Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle Run.

## 4. Deliverable Answers

### ctpa_vws_sections_2027.xlsx

1. The five sections to equip: Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle Run.
2. Share of the class 9 trucks each section's station weighed in 2026 that were over 80,000 lb, whole per cent:
   - Ashford Gap: 5 per cent
   - Brannock: 3 per cent
   - Cole Hollow: 11 per cent
   - Dunmere: 7 per cent
   - Elk Ferry: 16 per cent
   - Foxbriar: 3 per cent
   - Garnet Ridge: 21 per cent
   - Halbrook: 6 per cent
   - Ingram Mill: 4 per cent
   - Jessup Fork: 11 per cent
   - Kettle Run: 11 per cent
   - Lowfield: 5 per cent
3. Average five-axle trucks a weekday entering at each section's interchanges in 2026, whole trucks:
   - Ashford Gap: 58
   - Brannock: 58
   - Cole Hollow: 26
   - Dunmere: 55
   - Elk Ferry: 23
   - Foxbriar: 55
   - Garnet Ridge: 22
   - Halbrook: 31
   - Ingram Mill: 52
   - Jessup Fork: 27
   - Kettle Run: 41
   - Lowfield: 54
4. Gross overweight citations the scale houses issued in 2026 to five-axle trucks that had entered at each section, whole citations:
   - Ashford Gap: 65
   - Brannock: 173
   - Cole Hollow: 68
   - Dunmere: 178
   - Elk Ferry: 52
   - Foxbriar: 168
   - Garnet Ridge: 61
   - Halbrook: 107
   - Ingram Mill: 165
   - Jessup Fork: 63
   - Kettle Run: 121
   - Lowfield: 58

### ctpa_section_overweight_2026.csv

5. Twelve rows, one per section west to east, each with its share as in item 2.

### ctpa_overweight_share_2026.svg

6. Bar chart of the twelve shares west to east, each labelled with its whole per cent, the five sections to equip in blue and the others in grey.
