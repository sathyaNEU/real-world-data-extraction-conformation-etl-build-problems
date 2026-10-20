## Tags

**Domain:** Demographic & Social Science (income and poverty statistics from tax returns; Survey Research & Official Statistics, census, register and administrative data quality: the IRS ZIP code statistics conformed to the council's fourteen member counties, with each county's returns with qualifying children recovered from its credit returns and credit amount).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The Corran Valley Council of Governments should split the $20,000,000 2027 weatherization fund in proportion to each member county's tax-year 2023 earned income credit returns with qualifying children, and no county reaches the 12 per cent cap.**
Tallis County has the largest share, 11.46 per cent ($2,292,000), under the cap's $2,400,000. Not the statewide share of returns with children applied to every county's credit returns, which puts Tallis at 15.46 per cent and caps it, because Tallis's credit returns in the lowest income class claim far less than that share implies: far more of its claimants are childless workers than the state's. Not every credit return, which puts it at 16.54 per cent.

## 2. Critical Components

1. Tallis County's tax-year 2023 credit returns with qualifying children: **6,270.1**
2. The fourteen counties' credit returns with qualifying children: **54,712.6**
3. Tallis County's share: **11.46 per cent**, under the 12 per cent cap
4. Tallis County's allocation: **$2,292,000**

## 3. Step-by-Step Solution

1. Conformed irs_soi_zip_code_data_ty2023_extract.csv (the latest year the IRS has published, policy 3.1) to counties through the residential ratio of zip_county_relationship_2023q4.xlsx, the four P.O. Box ZIP codes by their total ratio, the 00000 and 99999 lines counted for no county (policy 4.1 and 4.2).
2. From Table 2 of dor_individual_income_tax_statistics_ty2023.pdf took the statewide average credit of a childless return and of a return with qualifying children in the IRS's first income class (the Department's first three classes): $394.88 and $4,723.49; in every higher class each credit return has a qualifying child.
3. Split each ZIP code's first-class credit returns into returns with and without qualifying children so that the two averages reproduce its credit amount (A59660, thousands of dollars), added its credit returns in the higher classes, and summed by county: Tallis 6,270.1 of 54,712.6.
4. Shared the fund in proportion to the counts (policy 5.1): the largest share, Tallis's 11.46 per cent, is under the 12 per cent cap (5.2), so nothing is redistributed; allocations rounded to the nearest hundred dollars (5.3), Tallis $2,292,000.
5. Ask A: took the units of the jobs in wx_job_export_2026-09-30.csv funded by DOE-WAP or STATE-WX whose first COMPLETED change in wx_job_status_history_2026-09-30.csv falls in 2025 (policy 6.1; the export's COMPLETED_DATE is the latest completion, after any callback), each placed by its dwelling's tract county (Tallis-Hesketh Community Action enters Tallis on its Hesketh jobs): Tallis 352; Hesketh 113; Brenmoor 135; Quarrow 81; Varden 200; Fennick 212; Kerrow 57; Stanwick 114; Wexley 129; Hollin 131; Esker 78; Ardley 176; Silbury 180; Ravell 51.
6. Ask B: summed the lines of cvcog_grants_ledger_2024-07_2026-09.csv posted in 2025 that carry a job number, at the amount posted (the close-out's convention), each read as the previous system's job number through the MOVED conversion notes in the status history (the agencies invoiced 2025 under their old numbers) and placed by the job's tract county: Tallis 1,653,025; Hesketh 591,270; Brenmoor 915,332; Quarrow 590,212; Varden 1,036,943; Fennick 1,061,199; Kerrow 377,202; Stanwick 672,024; Wexley 686,082; Hollin 745,436; Esker 448,447; Ardley 1,021,267; Silbury 785,088; Ravell 308,925.
7. Recommended the proportional split with no county capped, Tallis the largest at $2,292,000.

## 4. Deliverable Answers

### corran_valley_2027_weatherization_allocation.xlsx

1. No county reaches the 12 per cent cap ($2,400,000).
2. Tax-year 2023 earned income credit returns with qualifying children, one decimal:
   - Tallis: 6,270.1
   - Hesketh: 3,694.8
   - Brenmoor: 5,242.6
   - Quarrow: 2,752.4
   - Varden: 4,206.5
   - Fennick: 5,291.3
   - Kerrow: 2,724.1
   - Stanwick: 3,869.3
   - Wexley: 4,782.2
   - Hollin: 3,199.1
   - Esker: 2,307.2
   - Ardley: 4,863.2
   - Silbury: 2,961.3
   - Ravell: 2,548.6
3. Share of the fourteen counties' returns, per cent to two decimals:
   - Tallis: 11.46
   - Hesketh: 6.75
   - Brenmoor: 9.58
   - Quarrow: 5.03
   - Varden: 7.69
   - Fennick: 9.67
   - Kerrow: 4.98
   - Stanwick: 7.07
   - Wexley: 8.74
   - Hollin: 5.85
   - Esker: 4.22
   - Ardley: 8.89
   - Silbury: 5.41
   - Ravell: 4.66
4. 2027 allocation, nearest hundred dollars:
   - Tallis: $2,292,000
   - Hesketh: $1,350,600
   - Brenmoor: $1,916,400
   - Quarrow: $1,006,100
   - Varden: $1,537,700
   - Fennick: $1,934,200
   - Kerrow: $995,800
   - Stanwick: $1,414,400
   - Wexley: $1,748,100
   - Hollin: $1,169,400
   - Esker: $843,400
   - Ardley: $1,777,700
   - Silbury: $1,082,500
   - Ravell: $931,600
5. Bar chart of the fourteen allocations against a dashed line at the 12 per cent cap ($2,400,000) on the Allocation sheet, Tallis highlighted.
6. Dwellings the program weatherized in program year 2025, whole dwellings:
   - Tallis: 352
   - Hesketh: 113
   - Brenmoor: 135
   - Quarrow: 81
   - Varden: 200
   - Fennick: 212
   - Kerrow: 57
   - Stanwick: 114
   - Wexley: 129
   - Hollin: 131
   - Esker: 78
   - Ardley: 176
   - Silbury: 180
   - Ravell: 51
7. The program's spending on dwellings in program year 2025, whole dollars:
   - Tallis: $1,653,025
   - Hesketh: $591,270
   - Brenmoor: $915,332
   - Quarrow: $590,212
   - Varden: $1,036,943
   - Fennick: $1,061,199
   - Kerrow: $377,202
   - Stanwick: $672,024
   - Wexley: $686,082
   - Hollin: $745,436
   - Esker: $448,447
   - Ardley: $1,021,267
   - Silbury: $785,088
   - Ravell: $308,925

### corran_valley_ty2023_county_credit_families.csv

1. One row per member county with its tax-year 2023 earned income credit returns with qualifying children to one decimal, the figures in item 2 above, beside its credit returns of every kind.
