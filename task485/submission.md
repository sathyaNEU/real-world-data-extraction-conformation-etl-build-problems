## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a boundary commission's 2032 electorate forecast for a district's 23 wards, conformed from six electoral registers in two election management system layouts, the old system's notices of alteration, the address gazetteer, the council's completions monitoring and housing trajectory, and its polling district and ward schedules).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The draft recommendations should address Lorrimere West, Caldenstow Park, Quenbrook, Ebborby and Kettermere: on the forecast for the register to be published on 1 December 2032 these five wards lie more than 10 per cent from the district's average of 2,714 electors per councillor, and the other 18 are within it.**
Lorrimere West, Caldenstow Park, Quenbrook and Kettermere sit at +12.8, +12.2, +15.3 and +15.6 per cent and Ebborby at -12.3. Not Lorrimere North and Tibberfield, which the 2025 register plus the dwellings to come at the settled stock's electors per dwelling puts at +14.9 and +15.4: their sites complete from 2030, and a dwelling's electors join the register over the canvasses after it comes into use, so in 2032 they hold well under the settled level (+6.5 and +4.1). Not with Lorrimere West, Caldenstow Park and Quenbrook within, at +7.5, +3.8 and +3.7 on that route: their estates completed from 2024 are still joining the register.

## 2. Critical Components

1. Local government electors on the register published 1 December 2025: **109,512**.
2. Dwellings the housing trajectory expects from 1 October 2026 to 31 March 2032: **2,664**.

## 3. Step-by-Step Solution

1. Conformed the registers of 1 December 2022 to 2025 in ems_property_electorate_2022-2025.csv to llpg_extract_2026-10-12.csv through each property's UPRN (approved records in use, RD02 to RD04 houses, RD06 flats, the gazetteer's ward): 109,512 local government electors on the 2025 register.
2. Counted each dwelling's canvasses by each register from its gazetteer in-use date, a property being first canvassed in the year it is in use on 31 August and applications determined by 31 October reaching the 1 December register (lorrimere_annual_canvass_report_2025.pdf).
3. Took the settled level from the 2025 register at the dwellings at their seventh canvass or later (houses 1.84, flats 1.22 electors per dwelling) and, from the 2022 to 2025 registers at the dwellings in housing_completions_monitoring_2014-2026.xlsx, the share of it a dwelling holds: 0.08 on rolling registration alone, then 0.45, 0.69, 0.83, 0.91, 0.96, 0.97 at its first to sixth canvass.
4. Carried each dwelling at its seventh canvass or later on the 2025 register at its 2025 count and every other dwelling, in use since or due in housing_trajectory_2026-09-30.xlsx (2,664 from October 2026 to March 2032, and 2032/33's April to October, each year's completions spread evenly at the site's remaining mix), at its type's settled level times its share at its canvasses on 1 December 2032.
5. Divided each ward's forecast by its councillors (wards_councillors_2014_order.csv) against the district's 116,705 electors over 43 councillors, 2,714 each: five wards lie more than 10 per cent from it.
6. For the 2021 register, read ELECTRA_PROPERTY_ELECTORATE_REV_2021.txt as the register Electra held when it was switched off on 4 March 2022 (dwellings first in use after 31 October 2021 hold electors in it, each an addition in the 2022 notices) and backed each local government entry of the notices of 4 January, 1 February and 1 March 2022 in ELECTRA_NOTICES_OF_ALTERATION_2021-01_2022-03.txt out of each property's TOTAL less its attainers and overseas electors (an addition taken off, a deletion put back, F entries and attainers left), by the ward of its 2014 district through polling_district_review_2023_schedule.csv: 107,065 electors.
7. The draft recommendations address the five wards outside 10 per cent.

## 4. Deliverable Answers

### ward_electorate_forecast_2032.xlsx

1. Finding for each ward on the 2032 forecast:
   - Lorrimere Abbey: within 10 per cent
   - Lorrimere Castle: within 10 per cent
   - Lorrimere North: within 10 per cent
   - Lorrimere West: outside, above the average
   - Caldenstow Central: within 10 per cent
   - Caldenstow Park: outside, above the average
   - Quenbrook: outside, above the average
   - Tibberfield: within 10 per cent
   - Ebborby: outside, below the average
   - Kettermere: outside, above the average
   - Selwarstow: within 10 per cent
   - Vellanridge: within 10 per cent
   - Ostenworth: within 10 per cent
   - Harnwick: within 10 per cent
   - Brenningholme: within 10 per cent
   - Faulcott: within 10 per cent
   - Griselbrook: within 10 per cent
   - Dorranford: within 10 per cent
   - Pellanham: within 10 per cent
   - Rothenridge: within 10 per cent
   - Stellfield: within 10 per cent
   - Vardonham: within 10 per cent
   - Yarnmere: within 10 per cent
2. Local government electors on the register published 1 December 2021, whole electors:
   - Lorrimere Abbey: 7,758
   - Lorrimere Castle: 5,058
   - Lorrimere North: 5,104
   - Lorrimere West: 7,489
   - Caldenstow Central: 4,974
   - Caldenstow Park: 4,129
   - Quenbrook: 2,330
   - Tibberfield: 2,593
   - Ebborby: 2,362
   - Kettermere: 7,623
   - Selwarstow: 5,028
   - Vellanridge: 5,022
   - Ostenworth: 5,130
   - Harnwick: 2,628
   - Brenningholme: 7,461
   - Faulcott: 2,494
   - Griselbrook: 5,120
   - Dorranford: 7,478
   - Pellanham: 2,478
   - Rothenridge: 4,859
   - Stellfield: 4,873
   - Vardonham: 2,636
   - Yarnmere: 2,438

### ward_variance_2032.png

1. Horizontal bar chart of each ward's 2032 variance from the district average against the 10 per cent lines: the five wards outside (Lorrimere West, Caldenstow Park, Quenbrook, Ebborby and Kettermere) marked beyond the lines and the other 18 within them.
