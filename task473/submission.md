## Tags

**Domain:** General Statistics & Data Science (data integration: a fatal crash census whose surviving drivers were tested completely at three agencies and only after an arrest at the scene everywhere else, integrated into one completed count of alcohol-impaired-driving deaths per county, with the toxicology laboratory's specimens, the crash records system's reports and the DOT's vehicle miles).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Corwin, Hatchell, Ossian and Tanager are high-range for the FY2028 County Impaired Driving Task Force grants.**
Their 2023 to 2025 rates are Corwin 0.71, Hatchell 0.68, Ossian 0.68 and Tanager 0.66 per 100 million vehicle miles against the 0.60 line; the nearest below is Kittredge at 0.57. Not Corwin, Hatchell, Ossian and Pruett, which one share of unarrested drivers at .08 or more (7.2 per cent where every driver is tested) gives, because officers miss most drivers between .08 and .149 and few at .15 or more, so a county whose impaired drivers sit near the limit hides more of them; not Brisbin, Corwin, Hatchell and Ossian, which one catch rate for every BAC (60.9 per cent) gives.

## 2. Critical Components

1. At the State Patrol and the Corwin and Ossian sheriffs, which test every surviving driver, officers arrested **28.6%** of surviving drivers from .08 to .149 and **88.9%** at .15 or more.
2. Tanager's county and city agencies arrested 8 drivers found from .08 to .149 and 8 at .15 or more, so **21.0** impaired surviving drivers there were never tested.
3. Tanager's 2023 to 2025 rate is **0.66**, above the 0.60 line.

## 3. Step-by-Step Solution

1. Read fcc_2023_crash.csv and fcc_2023_person.csv (2011 form codes, results in thousandths) and fcc_2024_2025_crash.csv and fcc_2024_2025_person.csv (2024 form), kept each death within 30 days of a 2023 to 2025 crash by crash county, and took drivers as guidelines 2.3 defines them (ghso_fy2028_county_task_force_guidelines.pdf).
2. Identified the agencies that draw blood from every surviving driver (manual 4.2) through fcc_agency_directory.xlsx's agency numbers and former codes: the State Patrol posts and the Corwin and Ossian sheriffs.
3. At those agencies, divided the arrested surviving drivers by all surviving drivers in each band, .08 to .149 and .15 or more: 28.6% and 88.9%; holding out each State Patrol post in turn, these rates recover its unarrested drivers at .08 or more from its arrests with a root mean square miss of 1.1 drivers, against 3.4 for one unarrested share.
4. At every other agency, counted each arrested driver found at .08 or more as one over its band's catch rate (3.5 and 1.125), the excess being that county's untested impaired surviving drivers (21.0 in Tanager), and gave each of the county's untested surviving drivers the excess divided by their number.
5. Gave each crash its deaths times the chance that at least one driver was at .08 or more (guidelines 2.2), summed by county, and divided by the 2023 to 2025 vehicle miles of dot_county_dvmt_2023_2025.xlsx, each year's DVMT times its days (366 in 2024), per 100 million: Tanager 0.66.
6. From stl_specimen_extract_2023_2025.csv, kept the 2025 DUI arrests by local collection date, one per agency case number and one where a county jail's kit under the sheriff's number shares a department's collection site and minute, placed each in its agency's county from fcc_agency_directory.xlsx and each State Patrol arrest (submitted under SPHQ000) in its post's county from the post in its case number, and took the first specimen's whole-blood ethanol (serum divided by 1.16, the amended report over the superseded): the arrests and the per cent at .15 or more below.
7. From crs_reports_2025.csv and crs_units_2025.csv, took each report's latest accepted version, kept public-road crashes with an injury and a driver unit HAD BEEN DRINKING, counted a crash two agencies reported once (same date, road, time within minutes and drivers), and dropped those in the census, by agency and report number or, where the census cites a death investigation number, by date, road and time: the injury crashes below.
8. Certified Corwin, Hatchell, Ossian and Tanager as high-range (guidelines 2.4: 0.60 or more).

## 4. Deliverable Answers

### county_impaired_driving_rates_2023_2025.csv

1. Each county's 2023 to 2025 alcohol-impaired-driving deaths (whole numbers) and rate per 100 million vehicle miles (two decimals):
   - Aldous: 32 deaths, 0.52
   - Brisbin: 59 deaths, 0.54
   - Corwin: 60 deaths, 0.71
   - Delmont: 79 deaths, 0.51
   - Fairlee: 90 deaths, 0.45
   - Hatchell: 85 deaths, 0.68
   - Keswick: 78 deaths, 0.34
   - Kittredge: 43 deaths, 0.57
   - Lanier: 51 deaths, 0.54
   - Ossian: 54 deaths, 0.68
   - Pruett: 102 deaths, 0.55
   - Renwick: 67 deaths, 0.38
   - Stroud: 57 deaths, 0.41
   - Tanager: 66 deaths, 0.66
2. Each county's 2025 impaired-driving arrests with a blood specimen at the State Toxicology Laboratory and the per cent of them at .15 or more (one decimal):
   - Aldous: 171 arrests, 45.6%
   - Brisbin: 377 arrests, 64.7%
   - Corwin: 246 arrests, 45.1%
   - Delmont: 385 arrests, 50.1%
   - Fairlee: 429 arrests, 46.4%
   - Hatchell: 371 arrests, 49.9%
   - Keswick: 574 arrests, 47.4%
   - Kittredge: 206 arrests, 43.7%
   - Lanier: 275 arrests, 56.0%
   - Ossian: 224 arrests, 47.3%
   - Pruett: 415 arrests, 61.7%
   - Renwick: 409 arrests, 47.9%
   - Stroud: 341 arrests, 51.0%
   - Tanager: 454 arrests, 32.4%
3. Each county's 2025 injury crashes in which no one died within 30 days and an officer reported a driver had been drinking:
   - Aldous: 26
   - Brisbin: 78
   - Corwin: 56
   - Delmont: 77
   - Fairlee: 79
   - Hatchell: 79
   - Keswick: 122
   - Kittredge: 27
   - Lanier: 31
   - Ossian: 45
   - Pruett: 118
   - Renwick: 92
   - Stroud: 65
   - Tanager: 106

### fy2028_high_range_certification.pdf

1. High-range for FY2028: Corwin (0.71), Hatchell (0.68), Ossian (0.68) and Tanager (0.66).
2. Bar chart of the 14 counties' 2023 to 2025 rates against the 0.60 line, the high-range counties in red, on page 1.
