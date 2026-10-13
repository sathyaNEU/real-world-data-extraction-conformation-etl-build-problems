## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement error adjustment: a salary survey's reports carried from their filing dates to the reference date by the movement read within employers before the percentiles are read).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**File the Data Engineer III midpoint at $170,000 for the pay bands that take effect on 1 April 2027.**
It is the median base pay of the matched Tallyband respondents once each report is carried to 1 October 2026 at 2.7 per cent a year, the rate at which pay at a fixed level rises within the same employers across the reports' filing dates. Not $166,000, from carrying the reports at the 1.1 per cent a year that pay at a fixed level rises across all the reports pooled, which mixes the market's movement with the employers whose engineers began filing later and pay less at every level. Not $175,000, from carrying each report at the re-reporters' own growth between their two reports at the same level (4.7 per cent a year), which adds the merit people earn as they move up through a level the band holds still. Not $164,000, the median of the reports as filed.

## 2. Critical Components

1. The market's movement at a fixed level: **2.7 per cent a year**, the slope of log base pay on filing date with an intercept for each employer and each level, over the matched reports
2. Matched respondents, each counted once: **788, 1,234, 1,366 and 844** at Data Engineer I to IV

## 3. Step-by-Step Solution

1. Matched tallyband_extract_2026-10-01.csv as the compensation policy defines the market: respondents in the United States working full time, in the data engineering family with the primary focus data pipelines and platforms in tallyband_profiles_2026-10-01.csv (the job architecture's survey match), each employer level mapped through the level_crosswalk_2026.csv row in effect on the filing date, employer names tidied to the crosswalk's: 788, 1,234, 1,366 and 844 respondents at Data Engineer I to IV.
2. Fitted log base pay on filing date with an intercept for each employer and each level: pay at a fixed level rises 2.7 per cent a year within employers, while across the pooled reports it rises 1.1 per cent a year because the later filings come more and more from employers that pay less at every level, and the re-reporters' own pay rose 4.7 per cent a year between their two reports at the same level.
3. Carried each matched report from its filing date to 1 October 2026 at 2.7 per cent a year, the market as in effect on the benchmark date.
4. Read each level's 25th percentile, median and 75th percentile of the carried pay and filed them to the nearest thousand dollars: midpoints $119,000, $145,000, $170,000 and $204,000; Data Engineer III from $158,000 to $183,000.
5. Counted the Data Engineers employed on 1 October 2026 from hris_job_history_2026-10-14.csv: each employee's job record in effect that day (contingent workers out, employees on leave in), placed in the pay zone of their work location in pay_zones_2026.csv in force that day: 159.
6. Counted the Data Engineer requisitions open on 1 October 2026 from ats_requisitions_2026-10-14.csv, each requisition once across its postings, open from its opened_on until the fill or cancellation its status_date dates: 19.
7. Filed the Data Engineer III midpoint at $170,000.

## 4. Deliverable Answers

### data_engineer_bands_2027.xlsx

1. Midpoints, to the nearest thousand dollars:
   - Data Engineer I: $119,000
   - Data Engineer II: $145,000
   - Data Engineer III: $170,000
   - Data Engineer IV: $204,000
2. Data Engineer III: 25th percentile $158,000, 75th percentile $183,000
3. Data Engineers employed on 1 October 2026, by level and pay zone:
   - Data Engineer I: zone 1 19, zone 2 6, zone 3 5
   - Data Engineer II: zone 1 29, zone 2 12, zone 3 10
   - Data Engineer III: zone 1 27, zone 2 14, zone 3 14
   - Data Engineer IV: zone 1 14, zone 2 6, zone 3 3
4. Open requisitions on 1 October 2026:
   - Data Engineer I: 3
   - Data Engineer II: 5
   - Data Engineer III: 8
   - Data Engineer IV: 3

### data_engineer_bands_2027.svg

5. Horizontal bands for Data Engineer I to IV, each from its 25th to its 75th percentile on a dollar axis with its midpoint marked and labelled, Data Engineer III highlighted with its $158,000 and $183,000 ends labelled.
