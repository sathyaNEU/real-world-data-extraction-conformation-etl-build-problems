# solver round: round 4

**Proxy score 78.7 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 36.7 of 58). Main call LANDED. 1 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Re-install Spiritwood N, Swift Current E, Kindersley W, Davidson W, Pense, Watrous S, Melfort N and Kandahar in the April 2027 window, largest tracking error first.

solver: Re-install CS173 (0.061 m3/m3), CS187 (0.054), CS108 (0.048), CS133 (0.043), CS121 (0.038), CS118 (0.034), CS182 (0.031) and CS148 (0.027) in spring 2027, largest tracking error first. Tracking error is the triple-collocation error SD on May-Sep 2024-26 recommended-quality Ninox v5 mornings. In the heavy-clay cells (46,201) and (46,203) it is taken from a station-station-Ninox triple, because Ninox and PLSM share soil-map error there. CS160 (0.020) is ninth, 0.007 below CS148. 47 stations anchor from 15 April 2027: Brown 12, Dark Brown 22, Black 9, Dark Gray 4. CS119 is also off the list after a 205-day run with no delivery.

tokens matched 1 of 9 (Spiritwood, Swift Current, Kindersley, Davidson, Pense, Watrous, Melfort, Kandahar, April)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| reinstall_list_2027.docx | 1 | 8 | 16 | 50% |
| reinstall_list_2027.docx | 2 | 2 | 4 | 50% |
| reinstall_list_2027.docx | 3 | 11 | 11 | 100% |
| station_review_2027.csv | 1 | 113 | 171 | 66% |
| station_review_2027.png | 1 | 1 | 2 | 50% |

## Solver's path

1. Read NS-03 rev2, the PDS anchor terms 2027, the campaign plan (8 slots), the Ninox v5 notes and the PLSM v3 note. Tracking error = SD of station random error after offset and scale, in station units, which means triple collocation (TC).
2. Matched each station to the Ninox EASE36 cell whose bounds hold its registered coordinates (ninox_ease36_grid_sk.csv): 25 cells. Matched each station to the PLSM 0.1-degree box gp_id from floor(lat,lon/0.1)+0.05: all 56 found.
3. Ninox v5 (replaces v4): pass D, retrieval_qual_flag bit0 clear, soil_moisture not -9999, sm_date 1 May-30 Sep of 2024, 2025 and 2026. Overpass UTC = 2000-01-01 11:58:55.816 + tb_time_s, giving 12-13 UTC. 9,083 cell-mornings.
4. Logger 5 cm hourly 2024-26: dropped repeated sends and -9999 values, then took the reading nearest the overpass (max offset 27 min). PLSM sw1_mm taken at the nearest output time (12 UTC). Applied the current 5 cm probe start from the Probes sheet, which drops 2024 for CS140 (replaced 2025-04-23) and CS144 (replaced 2025-04-29). 250-382 mornings per station.
5. Covariance TC on (station, Ninox, PLSM): sigma^2 = Cxx - Cxy*Cxz/Cyz. First-pass top 8: CS173 .061, CS187 .054, CS121 .050, CS108 .048, CS133 .043, CS116 .039, CS102 .038, CS174 .037.
6. Independence check: re-ran TC with (station, other station in the same cell, Ninox) in every cell with 2+ stations. Identical everywhere except the heavy-clay cells (46,201) and (46,203), where clay at 5 cm is 43-57% and Ninox and PLSM share the 1:1M soil-map clay. There the errors fall: CS121 .038, CS174 .011, CS102 .007, CS116 .008, CS107 .008. The station-station-PLSM triple and the other partner give the same values. Adopted these.
7. Final ranking: CS173, CS187, CS108, CS133, CS121, CS118, CS182, CS148 (.027). Ninth CS160 (.0199). Gap .0072, reported as 0.007.
8. Delivery year 1 Oct 2025-30 Sep 2026 in local days (UTC-6), from the 2025 and 2026 hourly files at 5 cm. Kept rows received within 48 h, one per hour (earliest receipt). Valid = vwc 0.02-0.60 and tsoil > 0; a day counts with 20+ valid readings. Counts 155-206 days, none below 120. Longest no-delivery run: CS119 205 days (modem dead Oct-28 Apr, readings loaded late), CS166 23 days.
9. Anchors = 56 - 8 re-installs - CS119 = 47, from the register soil_zone: Brown 12, Dark Brown 22, Black 9, Dark Gray 4, all at least 2.

confidence: High for the list and the ninth: the clay-cell correction gives the same figure whichever partner or third product is used, and it matches the usual triple in every other cell. Delivery counts are far from the 120 threshold. Main residual risk: whether the intended handling of the clay cells matches this one.

notes: Tracking errors for CS121, CS102, CS174, CS116 and CS107 come from the station-station-Ninox triple, not the usual station-Ninox-PLSM triple. Without that correction the list would swap CS118, CS182 and CS148 for CS116, CS102 and CS174. The single-station cells (CS140, CS135, CS144) could not be cross-checked, but they are not heavy clay and have low errors.

### reinstall_list_2027.docx (solver's answers)
- eight stations with tracking errors, largest first: 1 CS173 Dark Gray 0.061 m3/m3; 2 CS187 Brown 0.054; 3 CS108 Brown 0.048; 4 CS133 Dark Brown 0.043; 5 CS121 Dark Brown 0.038; 6 CS118 Dark Brown 0.034; 7 CS182 Black 0.031; 8 CS148 Black 0.027 (m3/m3, 3 dp)
- ninth-slot station, its error and gap below eighth: CS160 (Dark Brown) tracking error 0.020 m3/m3; gap below CS148 = 0.007 m3/m3 (0.027111-0.019905=0.007206)
- anchors each zone keeps from 15 April 2027: Brown 12: CS106, CS109, CS111, CS129, CS135, CS144, CS145, CS161, CS167, CS170, CS190, CS192. Dark Brown 22: CS101, CS102, CS107, CS110, CS112, CS115, CS116, CS122, CS140, CS142, CS143, CS151, CS159, CS160, CS163, CS168, CS171, CS174, CS175, CS176, CS188, CS189. Black 9: CS104, CS120, CS141, CS146, CS149, CS166, CS183, CS184, CS194. Dark Gray 4: CS125, CS177, CS191, CS197. Total 47; every zone has at least 2 so the weekly correction runs in all four. Non-anchors: the 8 re-installs plus CS119 (205 consecutive days with no delivery).

### station_review_2027.csv (solver's answers)
- every station: tracking error m3/m3 3dp, anchors from 15 Apr (Y/N), 2025-26 counting days: CS101 0.010 Y 202; CS102 0.007 Y 202; CS104 0.015 Y 183; CS106 0.008 Y 193; CS107 0.008 Y 199; CS108 0.048 N 183; CS109 0.014 Y 195; CS110 0.010 Y 177; CS111 0.007 Y 198; CS112 0.011 Y 201; CS115 0.011 Y 171; CS116 0.008 Y 185; CS118 0.034 N 177; CS119 0.007 N 155; CS120 0.011 Y 185; CS121 0.038 N 199; CS122 0.010 Y 206; CS125 0.009 Y 172; CS129 0.012 Y 196; CS133 0.043 N 183; CS135 0.012 Y 196; CS140 0.012 Y 178; CS141 0.013 Y 174; CS142 0.011 Y 200; CS143 0.008 Y 187; CS144 0.009 Y 199; CS145 0.008 Y 203; CS146 0.011 Y 185; CS148 0.027 N 186; CS149 0.011 Y 190; CS151 0.007 Y 183; CS159 0.010

### station_review_2027.png (solver's answers)
- bars largest error first coloured by zone, ninth's error as labelled line: 56 bars from CS173 0.061 (Dark Gray) down to CS111 0.007. First eight bars: CS173 Dark Gray, CS187 Brown, CS108 Brown, CS133 Dark Brown, CS121 Dark Brown, CS118 Dark Brown, CS182 Black, CS148 Black. Horizontal line at CS160's error, labelled 0.020 m3/m3.
