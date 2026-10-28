## Tags

**Domain:** Sociology & Demography (fertility, mortality and life table estimation).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The 2028 to 2030 late-life frailty program should go to Windermoor, Coldwater Plains, Dunesford and Saltwick Shoals, the four areas whose life expectancy at 85 under their 2024 to 2026 death rates is below seven years.**
Their figures run from 6.6 years (Windermoor) to 6.9 (Saltwick Shoals), and the nearest area above the line is Cobbleton at 7.1. Not Spraymouth: splitting its 85-and-over population by its 2021 census ages puts it below the line, but its late-eighties cohorts of 2021 are now in their nineties and rebuilt by age it reads 7.2. Not on the census split either for Saltwick Shoals and Dunesford, which it puts above seven years because the coast's cohorts that turned 85 after census night are left out of their 85-and-over groups.

## 2. Critical Components

1. Saltwick Shoals' life expectancy at 85 is **6.9 years** and Dunesford's **6.9 years**
2. Spraymouth's life expectancy at 85 is **7.2 years**
3. Windermoor's is **6.6 years** and Coldwater Plains' **6.8 years**
4. The nearest area above the line, Cobbleton, is at **7.1 years**

## 3. Step-by-Step Solution

1. Took every death of a usual resident that occurred in 2024, 2025 or 2026 from bdm_death_registrations_tidewell_2016_2027.csv and interstate_deaths_tidewell_residents_2016_2027.xlsx, each resident's area from the usual residence's 2021 SA2 by asgs2021_sa2_to_lga2023.csv, ages in completed years from 85 to 94 and 95 and over (guidelines 3.3): 7,485 deaths at 85 and over across the twelve areas.
2. Rebuilt each area's population at each age at 30 June 2024, 2025 and 2026 from census2021_sa2_age_sex_ur.csv (SA2s summed to areas): each census age followed forward as its birth window, the 41 of 365 days born 1 July to 10 August a year younger at 30 June, less that window's deaths since census night, each year's 85-and-over total brought to the estimate in erp_lga_age_sex_2016_2026.xlsx.
3. Built each area's life table by single year to 94 with 95 and over closed on its own rate and half a year lived in the year of death (guidelines 3.2): life expectancy at 85 runs from 6.6 years (Windermoor) to 7.5 (Gannetmouth).
4. Named the areas below seven years on the unrounded figures (guidelines 3.1 and 3.4): Windermoor, Coldwater Plains, Dunesford and Saltwick Shoals.
5. Counted the after-hours visits in afterhours_attendances_2026.csv, which has one row per clinician attending: on each case, a clinician who arrives while the visit's clinicians are still there is the same visit and a later return is another, for residents aged 85 and over at the attendance by residence SA2 and arrival date in 2026.
6. Counted different residents across the service's 1 July 2026 system change by taking a carried-over client's January to June key from the new system's external_id, so each resident counts once.
7. Recommended the program for Windermoor, Coldwater Plains, Dunesford and Saltwick Shoals.

## 4. Deliverable Answers

### lga_life_expectancy_at_85_2024_2026.xlsx

1. Life expectancy at 85 in years and whether the area qualifies:
   - Bannockvale: 7.3, does not qualify
   - Cobbleton: 7.1, does not qualify
   - Coldwater Plains: 6.8, qualifies
   - Dunesford: 6.9, qualifies
   - Gannetmouth: 7.5, does not qualify
   - Kestrelmoor: 7.4, does not qualify
   - Mallowmere: 7.4, does not qualify
   - Merriwold: 7.2, does not qualify
   - Saltwick Shoals: 6.9, qualifies
   - Spraymouth: 7.2, does not qualify
   - Windermoor: 6.6, qualifies
   - Wolfram Ranges: 7.3, does not qualify
2. Times in 2026 the after-hours service visited the area's residents aged 85 and over:
   - Bannockvale: 1,002
   - Cobbleton: 340
   - Coldwater Plains: 278
   - Dunesford: 839
   - Gannetmouth: 1,156
   - Kestrelmoor: 568
   - Mallowmere: 630
   - Merriwold: 393
   - Saltwick Shoals: 1,109
   - Spraymouth: 828
   - Windermoor: 212
   - Wolfram Ranges: 304
3. Different residents aged 85 and over those visits reached:
   - Bannockvale: 697
   - Cobbleton: 233
   - Coldwater Plains: 211
   - Dunesford: 592
   - Gannetmouth: 829
   - Kestrelmoor: 407
   - Mallowmere: 471
   - Merriwold: 281
   - Saltwick Shoals: 797
   - Spraymouth: 596
   - Windermoor: 151
   - Wolfram Ranges: 229

### lga_life_expectancy_at_85.png

1. One bar for each of the twelve areas against a dashed line at 7.0 years, with Windermoor, Coldwater Plains, Dunesford and Saltwick Shoals marked as qualifying.
