## Tags

**Domain:** Epidemiology & Public Health (health burden and impact modelling: the occupational injury burden twenty grocery distribution centers will carry in fiscal 2027 under a planned shift in work pace, through the recordable rate per hour worked fitted on pace against the engineered labor standards within each center).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The twenty ergonomics program DCs will log about 1,000 recordable cases in fiscal 2027 under the FY2027 operating plan.**
The plan's cases and labor hours have the crews working about 9 per cent faster against the engineered standards than in the latest twelve months, and within each DC the recordable rate per hour rises steeply with pace, so at the plan's pace each hour worked carries about a quarter more risk than today's. Not about 800, which carries each DC's rate per hour worked from the latest twelve months onto the planned hours as if they were worked at today's pace. Not a rate per case shipped (about 800) or per standard hour (about 900), which leave the faster pace out too. Not a fit on cases per hour (about 800), which the plan's heavier new freight holds near today's while pace rises, and which the history rejects.

## 2. Critical Components

1. The plan's cases and labor hours put the twenty DCs' pace against the engineered standards about **9** per cent above the latest twelve months'
2. Within each DC the recordable rate per hour rises with pace against standard, so at the plan's pace it is about **a quarter** above the latest twelve months' rate

## 3. Step-by-Step Solution

1. From ehs_legacy_case_export_fy21_2024-06-30.csv and ehs_platform_cases_2024-07-01_2026-11-02.json kept the recordable cases (first aid and cases removed as not work-related out, each case migrated at the 2024 go-live once through the platform's legacy reference, platform times read in each DC's local time) by fiscal week of the date of injury: 661 at the twenty DCs in fiscal 2025.
2. Took each DC's hours worked by fiscal week from wfm_hours_by_dept_week_fy21_fy26.csv (every department and pay code, EHS-RK-01 8) and its direct hours (RCV, PUT, SEL, LOD), DC numbers, WMS locations and establishments matched through site_register_2026-11-02.csv.
3. Built each DC-week's standard hours from wms_cases_shipped_by_category_week.parquet and ie_engineered_labor_standards.xlsx (minutes per case shipped by function and category, PUT and SEL at the site factor in force that week, the pre-FY2023 category codes mapped) and its pace against standard as standard hours over direct hours.
4. Fitted recordable cases on log pace with each DC its own baseline, Poisson on the fiscal periods of all 60 DCs from fiscal 2021 to fiscal 2026 week 44 with log hours worked as offset: a response of about 2.7 per cent for each one per cent of pace (standard error 0.2), the fit about 60 deviance points better than the same model on cases per direct hour.
5. Back-tested on fiscal 2021 to 2024, asking for fiscal 2025 and 2026 to date at each DC's hours: the pace model misses by 11 per cent a DC against 21 for each DC's fiscal 2024 rate per hour and 15 for the same model on cases per direct hour (20 against 9 at the 7 DCs whose standard minutes per case moved more than 3 per cent).
6. From fy2027_operating_plan_v3.xlsx took each program DC's planned cases by category and labor hours by period (standard hours at the site factors in force on 12/27/2026): the pace about 9 per cent above the latest twelve months'.
7. Carried each program DC-period's planned hours through the fit at its own baseline and the plan's pace and summed: 1,001.8 (standard error 26), about 1,000; the other constructions tried give 982 to 1,028, and today's rate per hour on the planned hours gives about 800.
8. Forecast about 1,000 recordable cases for the twenty DCs in fiscal 2027.

## 4. Deliverable Answers

### ergonomics_forecast_fy2027.xlsx

1. Forecast recordable cases for the twenty program DCs in fiscal 2027, to the nearest hundred: 1,000.
2. Days away from work and of job transfer or restriction, added together, that each DC's fiscal 2026 recordable cases have carried to 31 October 2026:
   - Groveport DC: 685 days
   - West Jefferson DC: 313 days
   - West Chester DC: 160 days
   - Plainfield DC: 358 days
   - Whitestown DC: 557 days
   - Fort Wayne DC: 621 days
   - Lebanon IN DC: 576 days
   - Joliet DC 2: 954 days
   - Rockford DC: 534 days
   - Lansing DC: 708 days
   - York DC: 163 days
   - Shepherdsville DC: 195 days
   - Mount Juliet DC: 631 days
   - Memphis DC: 421 days
   - Jackson DC: 401 days
   - Savannah DC: 737 days
   - Katy DC: 140 days
   - Lancaster DC: 523 days
   - Pleasant Prairie DC: 766 days
   - Sun Prairie DC: 703 days
3. Cases each DC picked from 28 December 2025 to 31 October 2026 that weighed more than 50 pounds:
   - Groveport DC: 948,540 cases
   - West Jefferson DC: 905,131 cases
   - West Chester DC: 887,878 cases
   - Plainfield DC: 783,854 cases
   - Whitestown DC: 1,734,902 cases
   - Fort Wayne DC: 2,041,509 cases
   - Lebanon IN DC: 1,170,134 cases
   - Joliet DC 2: 1,551,654 cases
   - Rockford DC: 1,146,239 cases
   - Lansing DC: 1,210,331 cases
   - York DC: 437,458 cases
   - Shepherdsville DC: 779,632 cases
   - Mount Juliet DC: 1,467,921 cases
   - Memphis DC: 477,853 cases
   - Jackson DC: 688,582 cases
   - Savannah DC: 960,715 cases
   - Katy DC: 670,764 cases
   - Lancaster DC: 475,031 cases
   - Pleasant Prairie DC: 692,958 cases
   - Sun Prairie DC: 710,735 cases

### ergonomics_forecast_fy2027.pptx

1. One slide whose title states the forecast: about 1,000 recordable cases at the twenty program DCs in fiscal 2027.
2. Column chart of the twenty DCs' recordable cases by fiscal year beside the forecast: FY2021 609, FY2022 623 (53 weeks), FY2023 637, FY2024 588, FY2025 661, and the FY2027 forecast bar at 1,000.
