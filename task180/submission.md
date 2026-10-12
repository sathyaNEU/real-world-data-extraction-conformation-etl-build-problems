# task180 submission

## Tags

**Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (induced seismicity at deep geothermal plants against a mining authority's traffic-light scheme).
**Analytical objective:** Anomaly Detection & Diagnostics (which plant's 2027 seismicity will break the traffic-light amber, diagnosed from what its 2026 network could not record).

## 1. Final Recommendation

**Pfeilbrunn will run over the traffic-light amber in the first and fourth quarters of 2027, at about 223 and 206 earthquakes of ML 1.0 or more within 5 km against more than 120, and no other plant will in any quarter.**

Pfeilbrunn's town stations record every earthquake down to about ML 0.6 only from 23:30 to 05:00, and at that night rate round the clock its reservoir gives 28.0 per 100,000 m³ injected, 2.9 times the 9.6 its whole-day record shows; the borehole networks count at that rate from January. Not "no plant", which is what each plant's located counts carried into 2027 give (Moorstetten highest at 92, Pfeilbrunn at 62 and 77), because the 2026 catalogue holds Pfeilbrunn's small earthquakes mostly from the night. Not Lanzenried, which only year-on-year growth puts over, the growth being LZR5 replacing LZR4 nearer the well in July 2025. Every other plant stays at 85 or under.

## 2. Critical Components

1. Pfeilbrunn's located earthquakes of ML 1.0 or more within 5 km, January 2023 to September 2026: **442** of **658** from 23:30 to 05:00, 5.5 hours of the day
2. Pfeilbrunn's rate over the whole day: **28.0** per 100,000 m³ injected from its night hours scaled to 24 hours, against **9.6** on its whole-day record
3. Pfeilbrunn in 2027: **223** in the first quarter and **206** in the fourth (**70** and **44** in the second and third)
4. Every other plant's highest quarter of 2027: Moorstetten **85**, Lanzenried **76**, Ottenmoos **47**, Wendelsried **45**

## 3. Step-by-Step Solution

1. Counted the earthquakes of ML 1.0 or more with an epicentre within 5 km of an injection well's open hole (`well_register.csv`) in `seismic_catalogue_reviewed_2023-01_2026-09.csv`, by calendar quarter in local time (`tls_scheme_2024.pdf` sections 2 and 3): every plant under amber in every quarter, Pfeilbrunn at 62 in the first quarter of 2026 and 77 in the fourth of 2025.
2. Split each plant's count by local hour: Pfeilbrunn has 442 of its 658 from 23:30 to 05:00, where the rural plants have about their 5.5 hours' share; Pfeilbrunn's four stations stand in the town (`station_inventory_2026-10-12.xml`).
3. Took Lanzenried's record from August 2025, the first whole month after LZR5 replaced LZR4 nearer the well on 15 July 2025 (the inventory's epochs), its earlier network missing most of its earthquakes of ML 1.0 or more.
4. Divided each plant's count over its complete record, Pfeilbrunn's night count scaled by 24 over 5.5 (the share of the day the window covers), by its injected volume as the scheme's section 6 defines it (the reported volumes of `injection_reports_2023-2026.xlsx`, each 2026 report counted for the month it reports, as in step 7): Pfeilbrunn 28.0 per 100,000 m³ against 9.6 on its whole-day record.
5. Multiplied each rate by the plant's 2027 volume (`operating_plans_2027.pdf`: each quarter as in 2026, the fourth as in 2025), the borehole networks locating every earthquake of ML 0.6 or more within 5 km (`monitoring_ordinance_2026.pdf` § 3): Pfeilbrunn 223 and 206 in the first and fourth quarters, no other plant above 85.
6. Recommendation: Pfeilbrunn alone over amber, in the first and fourth quarters of 2027.
7. Injected volume: the injection rows on the 2026 sheet of `injection_reports_2023-2026.xlsx`, each filed under the month after the one it reports (received in the month it is filed under, December 2025 filed again as 2026-01, the hourly telemetry matching each row in the month before), summed by the month reported, MST-Th4a counted as MST-GT4 (`well_register.csv`), the injected volume of the scheme's section 6.
8. Automatic counts from `origins_2023-01_2026-09.csv` (origins by scautoloc grouped into events by origin time, each at its last origin), and hours from each station's HHZ epochs in the inventory less its HHZ gaps in `availability_gaps_2026-01_2026-09.csv`, a station not recording between its old and new epochs on an exchange day.

## 4. Deliverable Answers

### amber_outlook_2027.docx
1. Plants over amber in 2027: Pfeilbrunn only, in the first quarter (about 223) and the fourth (about 206); no other plant in any quarter.
2. Chart (Figure 1): one bar per plant for each quarter of 2027 against a line at 120; only Pfeilbrunn's first and fourth quarter bars are above it.
3. Expected earthquakes of ML 1.0 or more within 5 km in 2027, whole numbers, each within 8 per cent under any other rate convention on the whole record and none across 120:
   - Pfeilbrunn: Q1 223, Q2 70, Q3 44, Q4 206
   - Moorstetten: Q1 85, Q2 37, Q3 26, Q4 81
   - Lanzenried: Q1 76, Q2 33, Q3 24, Q4 73
   - Ottenmoos: Q1 47, Q2 22, Q3 14, Q4 46
   - Wendelsried: Q1 45, Q2 21, Q3 15, Q4 45

### tls_annex_2026.xlsx
1. Injected volume, cubic metres to the nearest hundred:
   - Moorstetten: Q1 753,300, Q2 325,000, Q3 230,000
   - Pfeilbrunn: Q1 794,800, Q2 249,500, Q3 155,300
   - Lanzenried: Q1 728,600, Q2 311,800, Q3 231,400
   - Wendelsried: Q1 675,600, Q2 313,600, Q3 219,400
   - Ottenmoos: Q1 745,400, Q2 341,200, Q3 222,800
2. Earthquakes of ML 1.0 or more within 5 km that the automatic system located, whole numbers:
   - Moorstetten: Q1 117, Q2 50, Q3 42
   - Pfeilbrunn: Q1 80, Q2 23, Q3 17
   - Lanzenried: Q1 95, Q2 36, Q3 27
   - Wendelsried: Q1 62, Q2 31, Q3 20
   - Ottenmoos: Q1 64, Q2 22, Q3 22
3. Hours the network had fewer than four stations recording, to one decimal:
   - Moorstetten: Q1 95.0, Q2 44.4, Q3 57.1
   - Pfeilbrunn: Q1 77.2, Q2 13.7, Q3 27.6
   - Lanzenried: Q1 34.8, Q2 53.5, Q3 91.8
   - Wendelsried: Q1 59.6, Q2 21.2, Q3 87.2
   - Ottenmoos: Q1 81.4, Q2 28.5, Q3 78.0
