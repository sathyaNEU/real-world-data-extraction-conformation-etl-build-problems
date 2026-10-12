# solver round: round 3

**Proxy score 87.1 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 45.1 of 58). Main call LANDED. 5 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Re-install Swift Current E, Kindersley W, Davidson W, Watrous S, Melfort N, Pense, Kandahar and Spiritwood N in the April 2027 window, in that order.

solver: Re-install CS187 Swift Current E (0.048 m³/m³), CS108 Kindersley W (0.045), CS133 Davidson W (0.042), CS118 Watrous S (0.040), CS182 Melfort N (0.038), CS121 Pense (0.037), CS148 Kandahar (0.035) and CS173 Spiritwood N (0.034) in spring 2027, largest tracking error first; CS160 Craik E would take a ninth slot at 0.024 m³/m³, 0.010 m³/m³ below the eighth; from 15 April 2027 the zones keep 12 Brown, 22 Dark Brown, 9 Black and 5 Dark Gray anchors.

tokens matched 9 of 9 (Swift Current, Kindersley, Davidson, Watrous, Melfort, Pense, Kandahar, Spiritwood, April)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| reinstall_list_2027.docx | 1 | 20 | 20 | 100% |
| reinstall_list_2027.docx | 2 | 4 | 4 | 100% |
| reinstall_list_2027.docx | 3 | 8 | 8 | 100% |
| reinstall_list_2027.docx | 4 | 10 | 12 | 83% |
| station_review_2027.csv | 1 | 117 | 173 | 68% |
| station_review_2027.png | 1 | 5 | 7 | 71% |
| station_review_2027.png | 2 | 0 | 0 | 0% |
| station_review_2027.png | 3 | 3 | 3 | 100% |

## Solver's path

1. Read pds_anchor_terms_2027.md, NS-03_reference_stations_rev2.docx and spring_campaign_2027_plan.md: 8 slots; tracking error = standard deviation of the station's own random error against the true cell soil moisture, after allowing for the station's own offset and scale, in station units; Ninox descending mornings of recommended quality, 1 May to 30 Sep of 2024 to 2026, current 5 cm probe only; anchor rule is active, not re-installed and at least 120 delivery days
2. station_register_2026-09.xlsx Stations: 56 active stations (Dark Brown 25, Brown 14, Black 11, Dark Gray 6); each station assigned to the EASE 36 km cell whose bounds in ninox_ease36_grid_sk.csv contain its coordinates (25 cells, all present in v5) and to the PLSM 0.1 degree box gp_id (50 boxes, all present)
3. Probes sheet, checked against field_visits PRB rows: current 5 cm probe install dates; only CS115 (2025-04-23) and CS184 (2025-04-29) changed inside the window, so their 2024 season and earlier 2025 mornings are dropped
4. ninox_l3sm_v5_2024-2026.csv (v5, not v4): pass D, retrieval_qual_flag bit 0 clear, soil_moisture not -9999, sm_date May to Sep 2024 to 2026 gives 9,083 cell-mornings; overpass time = J2000 epoch 2000-01-01 11:58:55.816 UTC + tb_time_s (12 to 13 UTC)
5. coteau_sm_hourly 2024 to 2026: 5 cm, vwc not -9999, deduplicated on site plus obs_time (re-transmissions are identical), current probe only; nearest reading to the overpass taken with merge_asof (largest gap 0.46 h); PLSM sw1_mm at the output time nearest the overpass
6. Error formula σ² = Cxx − Cxy·Cxz/Cyz on station, Ninox and PLSM over 255 to 382 mornings per station gives top eight CS187 0.0479, CS108 0.0450, CS133 0.0421, CS118 0.0399, CS182 0.0381, CS121 0.0369, CS148 0.0351, CS173 0.0340; ninth CS160 0.0241; gap 0.0099 rounds to 0.010; result identical with ±0.5 h and ±1 h match limits
7. Delivery: 2025 and 2026 hourly 5 cm rows, local day = obs_time minus 6 h, 1 Oct 2025 to 30 Sep 2026; valid when vwc is from 0.02 to 0.60 inclusive and tsoil_c > 0, deduplicated per hour; day counts at 20 or more valid hours; network 10,455 (Brown 2,691, Dark Brown 4,726, Black 1,995, Dark Gray 1,043); station minimum 165 (CS166), so none is under 120
8. Anchors from 15 April = zone station count minus re-installs: Brown 12, Dark Brown 22, Black 9, Dark Gray 5 (each zone keeps at least 2, so every weekly correction runs)

confidence: High on the list of eight and the anchor counts: there is a clear 0.010 m³/m³ break between 8th and 9th, and the ranking holds across matching tolerances. Medium-high on the exact delivery-day totals, which depend on the local-day and validity rules as stated.

notes: No station falls under 120 delivery days, so anchor counts depend only on the re-installs. The 2026 firmware (fw) field showed no timing or value shift. The scratch scripts were run inline and not saved to work/ because the sandbox was read-only.

### reinstall_list_2027.docx (solver's answers)
- eight stations with tracking error, in order: 1 CS187 Swift Current E (Brown) 0.048 m³/m³; 2 CS108 Kindersley W (Brown) 0.045 m³/m³; 3 CS133 Davidson W (Dark Brown) 0.042 m³/m³; 4 CS118 Watrous S (Dark Brown) 0.040 m³/m³; 5 CS182 Melfort N (Black) 0.038 m³/m³; 6 CS121 Pense (Dark Brown) 0.037 m³/m³; 7 CS148 Kandahar (Black) 0.035 m³/m³; 8 CS173 Spiritwood N (Dark Gray) 0.034 m³/m³
- ninth-slot station, its tracking error, gap below eighth: CS160 Craik E (Dark Brown); tracking error 0.024 m³/m³; gap below CS173 = 0.010 m³/m³
- anchors per soil zone from 15 April 2027: Brown 12 (14 stations minus 2 re-installed); Dark Brown 22 (25 minus 3); Black 9 (11 minus 2); Dark Gray 5 (6 minus 1); network 48; no station is below 120 delivery days, so none sits out
- delivery statement 1 Oct 2025 to 30 Sep 2026, days that count: Network 10,455 station-days; Brown 2,691; Dark Brown 4,726; Black 1,995; Dark Gray 1,043 (whole days)

### station_review_2027.csv (solver's answers)
- all 56 stations in order: site, zone, tracking error (m³/m³, 3 dp), rank, re-installed, delivery days: 1 CS187 Brown 0.048 Y 197; 2 CS108 Brown 0.045 Y 183; 3 CS133 Dark Brown 0.042 Y 184; 4 CS118 Dark Brown 0.040 Y 177; 5 CS182 Black 0.038 Y 168; 6 CS121 Dark Brown 0.037 Y 193; 7 CS148 Black 0.035 Y 187; 8 CS173 Dark Gray 0.034 Y 167; 9 CS160 Dark Brown 0.024 N 192; 10 CS104 Black 0.023 N 192; 11 CS109 Brown 0.022 N 195; 12 CS197 Dark Gray 0.020 N 174; 13 CS141 Black 0.020 N 175; 14 CS129 Brown 0.019 N 194; 15 CS170 Brown 0.019 N 199; 16 CS140 Dark Brown 0.019 N 177; 17 CS192 Brown 0.018 N 193; 18 CS174 Dark Brown 0.017 N 194; 19 CS115 Dark Brown 0.017 N 181; 20 CS135 Brown 0.017 N 197; 21 CS1

### station_review_2027.png (solver's answers)
- title: how many of the eight each zone gives up: Dark Brown 3, Brown 2, Black 2, Dark Gray 1 (total 8)
- bars in CSV order coloured by zone; ninth-station reference line: 56 bars in the rank order above; horizontal line at CS160 Craik E tracking error 0.024 m³/m³, labelled with that value
