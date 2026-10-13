# task453 submission

## Tags

**Domain:** Survey Research & Official Statistics, seasonal adjustment and official time-series production (a provincial statistics bureau's monthly payroll jobs for ten economic regions, built from the revenue agency's employer return statistics and seasonally adjusted for a statutory designation).
**Analytical objective:** Data Extraction & Conformation (ETL) (the agency's yearly tables to 2023, its monthly statistics from 2024 with the revision file's months in place of the preliminary ones and the bureau's municipal concordance conformed into each region's monthly payroll jobs, seasonally adjusted on one placement; the agency's workplace returns conformed into each region's employers and the jobs its workplaces lost).

## 1. Final Recommendation

**Certify Brennick Valley, the Capital and Pellmarsh Hills as designated for the first quarter of 2027.**

With each region's seasonal pattern estimated with the January 2026 move to workplace placement removed as a level shift, their seasonally adjusted payroll jobs for January to March 2027 stand 1.8 to 2.3 per cent (Brennick Valley), 1.5 to 1.7 per cent (the Capital) and 2.0 to 2.6 per cent (Pellmarsh Hills) below their 2026 averages, and every other region stands at least 0.63 points clear of the 1.0 per cent line. Not Kestrow North and Varrenby Shore, which a seasonal adjustment estimated across the change designates at 1.6 and 1.5 per cent below: the steps of 27.6 and 23.2 per cent that brought their mines, mills and plants into their series in January 2026 leak into the first quarter's seasonal factors and pull 2027 down, and the same leak lifts the Capital, which lost 16.3 per cent, to 0.6 per cent below.

## 2. Critical Components

1. The Capital's seasonally adjusted payroll jobs for the first quarter of 2027 are **1.5 to 1.7 per cent** below its 2026 average.
2. Brennick Valley's are **1.8 to 2.3 per cent** below and Pellmarsh Hills' **2.0 to 2.6 per cent** below their 2026 averages.
3. Kestrow North's and Varrenby Shore's each stand between **0.4 per cent below and 0.2 per cent above** their 2026 averages.

## 3. Step-by-Step Solution

1. Built each economic region's monthly payroll jobs from January 2021 to March 2027: the 2021 to 2023 sheets of pra_payroll_jobs_by_municipality_2021-2023.xlsx and pra_payroll_jobs_monthly_2024-01_2027-03.csv, with January to March 2027 from pra_payroll_jobs_revisions_2027-05-07.csv (regulation 3(2); the transmittal says the revision file replaces those months), each municipality placed in its economic region by bsea_municipal_concordance.xlsx, the retired Wexleigh and Dorran codes included.
2. Read pra_release_note_place_of_work_2026-02.pdf: from January 2026 the statistics place jobs at the workplace, before at the employer's account address, and the earlier months were not revised; each region's series steps at January 2026, by a level shift of 16.3 per cent down in the Capital and 27.6 and 23.2 per cent up in Kestrow North and Varrenby Shore.
3. Estimated each region's seasonal pattern on one placement: a regression of the logarithm of its monthly payroll jobs on month effects, a trend whose slope changes each January and a level shift from January 2026, the seasonally adjusted series being the jobs with the month effects removed; the ranges in block 2 span this regression with knots every one or two years and over 2023 to 2027 only; STL with a 7 or 13 year seasonal window and the classical decomposition, each on the history restated by the level shift; STL and the classical decomposition on the months before the change alone, their last year's factors carried forward; and STL on the history restated by the December to January, first-quarter or annual ratio.
4. Averaged each region's seasonally adjusted payroll jobs over January to March 2027 and set them against the average of its payroll jobs for the twelve months of 2026 (regulation 1(2)), unrounded (2(2)): Brennick Valley 1.9, the Capital 1.6 and Pellmarsh Hills 2.1 per cent below, every other region at least 0.63 points clear of the line.
5. Estimated across the change instead (STL or the classical decomposition over the whole history), the seasonal factors take up part of each step: Kestrow North and Varrenby Shore fall to 1.6 and 1.5 per cent below and the Capital rises to 0.6 per cent below.
6. For the jobs lost at each region's workplaces (regulation 4(1)(a)), compared each workplace's payroll jobs in March 2026 and March 2027 in pra_workplace_returns_2026-03_2027-03.csv, a workplace being its municipality and street address: a workplace sold, or moved to another of its employer's payroll accounts, keeps its address under a new account and workplace number, and a workplace listed on two of its employer's accounts is one workplace. At each workplace whose payroll jobs fell, the fall is the jobs lost, summed by region for the workplaces with none left in March 2027 (gone from the schedules or listed with no employees paid) and for those that kept some.
7. For each region's employers (regulation 4(1)(b)), counted the employers (the business number, a payroll account's first nine digits, of the employer that holds the account) with a March 2027 line in the region with payroll jobs above zero; an employer paying from two accounts is one employer.
8. Recommendation: certify Brennick Valley, the Capital and Pellmarsh Hills as designated for the first quarter of 2027.

## 4. Deliverable Answers

### rapid_response_certification_2027q1.pdf

1. The regions certified as designated for the first quarter of 2027: Brennick Valley, the Capital and Pellmarsh Hills.
2. For each certified region (regulation 3(3)), its seasonally adjusted payroll jobs for the first quarter of 2027 as the range the step-aware routes give, nearest 10 (the certificate's own figure in brackets), and its payroll jobs for 2026, nearest 10:
   - Brennick Valley: 24,680 to 24,800 (24,770); 2026: 25,250
   - Capital: 81,940 to 82,070 (82,020); 2026: 83,320
   - Pellmarsh Hills: 21,810 to 21,930 (21,930); 2026: 22,390
3. Figure 1: a horizontal bar chart of every region's seasonally adjusted payroll jobs for the quarter against its 2026 average, in per cent to one decimal, with the designation line at 1.0 per cent below and the three certified regions dark.

### regional_payroll_jobs_2027q1.csv

One row per region in the Schedule's order (E01 to E10), with the columns economic_region_code, economic_region, employers_with_payroll_jobs_2027_03, jobs_lost_workplaces_none_left_2027_03 and jobs_lost_workplaces_kept_some_2027_03.

4. Employers with payroll jobs at each region's workplaces in March 2027, whole numbers (employers_with_payroll_jobs_2027_03):
   - Capital: 5,781
   - Saltmere Coast: 3,490
   - Brennick Valley: 2,125
   - Dunfallow Bay: 1,386
   - Quillon Plain: 2,197
   - Hethervale Lakes: 1,288
   - Ardvane Uplands: 1,116
   - Kestrow North: 1,158
   - Pellmarsh Hills: 1,617
   - Varrenby Shore: 1,070
5. Payroll jobs lost between March 2026 and March 2027 at each region's workplaces whose payroll jobs fell and that had none left in March 2027, nearest 10 (jobs_lost_workplaces_none_left_2027_03):
   - Capital: 2,390
   - Saltmere Coast: 1,430
   - Brennick Valley: 820
   - Dunfallow Bay: 570
   - Quillon Plain: 940
   - Hethervale Lakes: 490
   - Ardvane Uplands: 340
   - Kestrow North: 410
   - Pellmarsh Hills: 840
   - Varrenby Shore: 380
6. Payroll jobs lost between March 2026 and March 2027 at each region's workplaces whose payroll jobs fell and that kept some, nearest 10 (jobs_lost_workplaces_kept_some_2027_03):
   - Capital: 5,010
   - Saltmere Coast: 1,760
   - Brennick Valley: 1,670
   - Dunfallow Bay: 740
   - Quillon Plain: 1,220
   - Hethervale Lakes: 690
   - Ardvane Uplands: 540
   - Kestrow North: 1,190
   - Pellmarsh Hills: 1,660
   - Varrenby Shore: 760
