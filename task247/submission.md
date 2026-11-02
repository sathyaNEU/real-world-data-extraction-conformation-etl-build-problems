# task247 submission

## Tags

**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance: a reef station's coral bleaching heat-stress watch on near-real-time and reprocessed satellite sea surface temperature).
**Analytical objective:** Data Quality Monitoring & Alerting (which reef sites' 2027 alert levels, declared weekly on the near-real-time record, stand on the reprocessed record of reference, and so which sites the November post-bleaching survey visits).

## 1. Final Recommendation

**Send the November post-bleaching survey to nine sites: PB06 Arrecife Los Pargos, PB07 Cayo Medusa, PB09 Arrecife Los Ronquillos, PB10 Punta Cascabel, PB11 Bajo Coralillo, PB12 Arrecife El Tiburon, PB13 Cabezo Morena, PB14 Bajo Rompiente and PB15 Punta Gorgonia.**

Their expected 2027 season maxima on the reprocessed record are 9, 11, 10, 12, 13, 10, 12, 9 and 11 degree Celsius weeks, all at Alert Level 2: PB06, PB07, PB09 and PB10 confirm the bulletins' Alert Level 2 and PB11, PB12, PB13, PB14 and PB15 raise their declared Alert Level 1.

Not the bulletins' four (PB06, PB07, PB09 and PB10), which leave out the southern sites: on every cloud-filled day the near-real-time analysis let the last observed anomaly fade toward the climatology, and under the August cloud over the south that took most of their HotSpots out. Not the three a correction by the past mean differences of observed and filled days keeps (PB07, PB09 and PB10): on hot filled days the analysis reads 0.26 degrees low, which the mean difference of all filled days (-0.007) does not restore.

## 2. Critical Components

1. The near-real-time analysis runs **0.06 degrees Celsius** warm of the reprocessed record on the days it observed, 2018 to 2026.
2. On the 2018 to 2026 days it did not observe, refilling each gap from the observed days either side reproduces the reprocessed record to **0.065 degrees** root mean square and **-0.001** on hot days (anomaly above 0.6), against **0.142** and **-0.263** for the record corrected by the mean differences of observed and filled days.
3. The bulletins' declared levels for the season: **PB01 No alert; PB02 No alert; PB03 No alert; PB04 Alert Level 1; PB05 No alert; PB06 Alert Level 2; PB07 Alert Level 2; PB08 Alert Level 1; PB09 Alert Level 2; PB10 Alert Level 2; PB11 Alert Level 1; PB12 Alert Level 1; PB13 Alert Level 1; PB14 Alert Level 1; PB15 Alert Level 1; PB16 No alert**.

## 3. Step-by-Step Solution

1. Near-real-time extract: the latest issue of each pixel and day (a later issue replaces the earlier, user guide section 3), the flag read by each row's version (from version 3.2, 2 observed and 1 not; before, 1 and 0), pixels to sites by the register; no analysis was issued for 17 June 2027.
2. Reprocessed record in kelvin less 273.15; on the 2018 to 2026 days the near-real-time analysis observed it runs 0.06 degrees warm of the reprocessed record (0.0595).
3. On a day it did not observe, the near-real-time value is the climatology plus the last observed anomaly fading day by day, so it understates a lasting warm anomaly: on 2018 to 2026 hot days it did not observe it reads 0.270 low, and 0.263 after the flag-mean correction, while refilling from the observed days either side leaves -0.001 (root mean square 0.065 against 0.142).
4. Each site's 2027 record: the observed days less 0.06, every other day (not observed, or not issued) by straight-line interpolation of the anomaly against the climatology file between the observed days either side; HotSpots of 1.0 degree or more above the register's maximum monthly mean, DHW the 84-day sum over 7, the season maximum over 1 June to 31 October (methods note sections 3 and 4).
5. Levels at 4 and 8 and each site's verdict against the highest level its season bulletins gave (sections 5 and 6): eight confirmed, eight raised, none lowered.
6. Loggers: each log row is placed at its site by its pin. The pin register holds the tags as the divers last checked them (April 2027), and on the four service trips from 18 August 2025 the boat's stops read through it as the sites north to south, four a day; on the five trips before, the tags are the pins' earlier ones (E01 PB07; E02 PB06; E03 PB09; E04 PB10; E05 PB02; E06 PB01; E07 PB03; E08 PB05; E09 PB11; E10 PB12; E11 PB15; E12 PB14; E13 PB04; E14 PB08; E15 PB16; E16 PB13), the site being the stop's place in the trip's route north to south, the same on every one of those trips. The times the log marks UTC (the Cozumel II's trips of August 2025 and April 2026) are five hours ahead of the loggers' local clocks. Then each logger's readings while in the water, June to October 2024 to 2026 in local time, one reading an hour, at or above the register's maximum monthly mean: from 2,565 hours at PB09 to 4,678 at PB04.
7. The survey list is the nine sites at Alert Level 2.

## 4. Deliverable Answers

### reef_heat_stress_2027.xlsx

1. Each site's expected 2027 season maximum on the reprocessed record (whole degree Celsius weeks), its alert level and its verdict against the declared level, 16 rows in the register's order:
   - PB01 Bajo Pelicano: 3; No alert; confirms (declared No alert)
   - PB02 Arrecife Las Garzas: 5; Alert Level 1; raises (declared No alert)
   - PB03 Cabezo Tortuga: 2; No alert; confirms (declared No alert)
   - PB04 Punta Abanico: 6; Alert Level 1; confirms (declared Alert Level 1)
   - PB05 Bajo del Ancla: 5; Alert Level 1; raises (declared No alert)
   - PB06 Arrecife Los Pargos: 9; Alert Level 2; confirms (declared Alert Level 2)
   - PB07 Cayo Medusa: 11; Alert Level 2; confirms (declared Alert Level 2)
   - PB08 Bajo Langosta: 7; Alert Level 1; confirms (declared Alert Level 1)
   - PB09 Arrecife Los Ronquillos: 10; Alert Level 2; confirms (declared Alert Level 2)
   - PB10 Punta Cascabel: 12; Alert Level 2; confirms (declared Alert Level 2)
   - PB11 Bajo Coralillo: 13; Alert Level 2; raises (declared Alert Level 1)
   - PB12 Arrecife El Tiburon: 10; Alert Level 2; raises (declared Alert Level 1)
   - PB13 Cabezo Morena: 12; Alert Level 2; raises (declared Alert Level 1)
   - PB14 Bajo Rompiente: 9; Alert Level 2; raises (declared Alert Level 1)
   - PB15 Punta Gorgonia: 11; Alert Level 2; raises (declared Alert Level 1)
   - PB16 Arrecife Sargazo: 6; Alert Level 1; raises (declared No alert)
2. Each site's hours at or above its maximum monthly mean at its logger while in the water, June to October 2024 to 2026:
   - PB01: 3584
   - PB02: 2783
   - PB03: 3333
   - PB04: 4678
   - PB05: 4074
   - PB06: 2859
   - PB07: 4412
   - PB08: 3188
   - PB09: 2565
   - PB10: 4338
   - PB11: 3743
   - PB12: 4350
   - PB13: 3413
   - PB14: 3862
   - PB15: 3757
   - PB16: 3683

### survey_list_note_2027.pdf

- The survey list, nine sites (PB06, PB07, PB09, PB10, PB11, PB12, PB13, PB14 and PB15), and a chart of each site's declared and expected season maximum against the Alert Level 1 and Alert Level 2 lines, the raised sites marked.
