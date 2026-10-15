## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: each gas producer's methane emitted over the rating year, measured from four aerial campaigns whose passes detect a plume with a chance that rises with its rate, against the methane its wells produced).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Rate four Tollaver Basin producers low-methane for 2027: Calbrent Energy, Ostrel Energy, Corrandale Petroleum and Brushy Mesa Operating.**
Their measured methane intensities over the rating year are 0.104, 0.108, 0.119 and 0.134 per cent, under the 0.20 per cent line, and Ashmund Production, the nearest of the other eight, is at 0.232. Not the eight that averaging each producer's detected plumes over the four campaigns rates, adding Anchell Oil & Gas, Pinyon Draw Production, Pellisto Gas Partners and Ashmund Production: it counts every site a pass imaged without a plume as emitting nothing, though a pass detects a plume of 8.0 kg/h only half the time. Not none, as carrying each detected source through the whole year would have it, the tank batteries' dumps seen on one pass in four standing for every hour.

## 2. Critical Components

1. The chance that a pass detects a plume, fitted to Talmora's 182 controlled releases: one in two at **8.0 kg/h**, nine in ten at **23.9 kg/h**.
2. Brushy Mesa Operating, the rated producer nearest the line: **0.134** per cent.
3. Ashmund Production, the unrated producer nearest the line: **0.232** per cent.

## 3. Step-by-Step Solution

1. Attributed each plume in talmora_plume_detections_tollaver_2025_2026.csv to the site in tarvane_tollaver_site_register_2026.csv nearest it within 150 m, as the rating standard places plumes, and each attributed plume to the producer operating the site on its imaging day.
2. Placed each site under its flight lines through its facility numbers in talmora_flight_line_coverage_tollaver_2025_2026.csv: a site imaged on two lines in a campaign counts the mean of its two passes, and a site a line lost to cloud left without an image is measured by its other campaigns, as the standard combines them.
3. Fitted Talmora's logistic detection curve in the log of the metered rate to the 182 releases in talmora_controlled_release_study_2025.xlsx by maximum likelihood, as its methods note describes: 8.0 kg/h detected half the time, 23.9 kg/h nine times in ten.
4. Counted each plume at 5 kg/h or more at its rate divided by its chance of detection, summed each site's plumes on each pass, averaged its passes and then its campaigns within each operator's part of the rating year, and multiplied by that part's hours: each producer's methane emitted.
5. Took each producer's methane produced from ogc_well_production_tollaver_2025_2026.csv (the latest report for each well and month, to the operator of record, restated from 14.65 to 14.73 psia) with the 2026 composite methane shares in tollaver_gas_composite_analyses_2024_2026.csv at 19.2 kg per Mcf, and divided: each producer's measured methane intensity.
6. Summed the plant's lines in tollaver_plant_allocation_statements_2025_2026.csv by the production month in each line's reference, October 2025 to September 2026, with the March 2026 statement at its second revision and the energy-only lines restated at the station's heating value for the month, to producers through tollaver_plant_meter_stations_2026.csv: gas delivered.
7. Summed codes FL and FR (routine flaring from January 2026, counted as flared in ogc_basin_flaring_summary_2025_2026.csv) in ogc_flaring_venting_reports_tollaver_2025_2026.csv, the latest report for each lease, month and code, each lease to its operator of record in the month in ogc_lease_register_tollaver_2026.csv: gas flared.
8. Rated the producers at 0.20 per cent or less: Calbrent Energy (0.104), Ostrel Energy (0.108), Corrandale Petroleum (0.119) and Brushy Mesa Operating (0.134).

## 4. Deliverable Answers

### tollaver_producer_methane_ratings_2027.xlsx

1. Rated low-methane for 2027: Calbrent Energy, Ostrel Energy, Corrandale Petroleum and Brushy Mesa Operating; the other eight are not rated.
2. Methane emitted over the rating year in whole tonnes, measured methane intensity in per cent, and rating:
   - Anchell Oil & Gas: 7,961 t, 0.249, not rated
   - Ashmund Production: 19,510 t, 0.232, not rated
   - Brushy Mesa Operating: 5,895 t, 0.134, rated
   - Calbrent Energy: 5,314 t, 0.104, rated
   - Corrandale Petroleum: 4,612 t, 0.119, rated
   - Lechuza Creek Resources: 19,935 t, 0.268, not rated
   - Marrowind Operating: 7,058 t, 0.304, not rated
   - Ostrel Energy: 6,714 t, 0.108, rated
   - Pellisto Gas Partners: 11,242 t, 0.264, not rated
   - Pinyon Draw Production: 11,090 t, 0.236, not rated
   - Ruskmoor Exploration: 6,446 t, 0.420, not rated
   - Sunmere Natural Gas: 11,125 t, 0.292, not rated
3. Gas delivered to the Tollaver Gas Processing Plant over the rating year, whole million cubic feet:
   - Anchell Oil & Gas: 189,884
   - Ashmund Production: 486,628
   - Brushy Mesa Operating: 250,229
   - Calbrent Energy: 289,549
   - Corrandale Petroleum: 217,960
   - Lechuza Creek Resources: 431,339
   - Marrowind Operating: 134,458
   - Ostrel Energy: 350,917
   - Pellisto Gas Partners: 250,626
   - Pinyon Draw Production: 275,009
   - Ruskmoor Exploration: 88,158
   - Sunmere Natural Gas: 229,384
4. Gas flared over the rating year, whole million cubic feet:
   - Anchell Oil & Gas: 2,180
   - Ashmund Production: 5,258
   - Brushy Mesa Operating: 3,238
   - Calbrent Energy: 4,582
   - Corrandale Petroleum: 4,666
   - Lechuza Creek Resources: 4,324
   - Marrowind Operating: 2,524
   - Ostrel Energy: 6,868
   - Pellisto Gas Partners: 3,528
   - Pinyon Draw Production: 3,757
   - Ruskmoor Exploration: 625
   - Sunmere Natural Gas: 2,850
5. Chart: each producer's measured methane intensity as a bar against the 0.20 per cent line, on the Intensity chart sheet, the four rated producers under it.

### talmora_plumes_conformed_2025_2026.csv

1. 2,348 rows, one per plume Talmora reported in the four campaigns, 2,241 of them with the register site within 150 m and the producer operating it on the imaging day, and 107 with no producer site within 150 m.
