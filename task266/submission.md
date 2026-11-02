## Tags

**Domain:** Biomedical & Clinical Research, survival and time-to-event analysis.
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Set the Former Asbestos Workers Review Program's horizon at 60 years after first exposure for the term from 1 July 2027.**
93.3% of the workforce's mesotheliomas are diagnosed within 60 years against 85.1% within 55, so 60 is the shortest five-year step that reaches nine in ten. Not 55 from the register's latencies as they stand (92.7% within 55) or from a curve that admits each case only from 1 July 2004 (95.9%): both read the long latencies of the 1970s and 1980s workforce, which the register closed at 30 June 2026 cannot hold yet, as latencies that do not happen.

## 2. Critical Components

1. Register cases in the estimate (occupational, first exposed before 1 January 1986): **5,271**
2. Share of the workforce's mesotheliomas diagnosed within 55 years: **85.1%**
3. Share diagnosed within 60 years: **93.3%**

## 3. Step-by-Step Solution

1. Stacked ddcf_mesothelioma_register_2013-2026.csv and ddcf_mesothelioma_register_2004-2012_legacy.xlsx, reading the first system's refs DD/05/0213 as the histories' DD05-0213 and its codes OCC, DOM, ENV and NIL as the current words: 6,387 cases.
2. Took each case's first exposure from ddcf_occupational_histories_2026-09-30.csv as the earliest start of a period of work marked exposed (Y or Yes), per terms 2.2, and kept the occupational cases first exposed before 1 January 1986 per terms 2.1: 5,271 cases.
3. Measured each case's years from first exposure to diagnosis at 365.25 days (terms 4.3) and its window, the years its first exposure leaves between the register's start and its 2025-26 close as ddcf_annual_report_2025-26.pdf states them.
4. Estimated the distribution over every case whenever diagnosed (terms 4.2) by the nonparametric maximum likelihood estimate for doubly truncated data (Efron and Petrosian), no shape assumed (terms 4.4): 85.1% within 55 years and 93.3% within 60, so 60 is the shortest step at nine in ten.
5. Placed each Mobile Review Unit (site MRU) day of 2025-26 in review_appointments_2023-07_to_2026-06.csv in the town of the unit's midday purchase on mobile_review_unit_card_statement_2025-26.xlsx (11.30 to 14.00), which moves the four published visit pairs the unit worked the other way round, and in the published town where the day has none.
6. Counted a blank attendance row as a review on the unit days where mobile_review_unit_xray_qa_log_2025-26.xlsx (counter end less start less QC exposures, two exposures a review) fits the Attended and blank rows together rather than the Attended rows alone; blank rows on every other day are no-shows: 1,923 reviews across the circuit towns.
7. Took the distinct members with a review in 2025-26 on those readings (7,570) and counted those with fewer years than each setting since their first exposure in review_program_members_2026-06-30.csv on 1 July 2027 (terms 3.2).
8. Recommended setting the horizon at 60 years after first exposure.

## 4. Deliverable Answers

### review_horizon_board_paper_2027.docx

1. Recommendation: set the Program's horizon at 60 years after first exposure for the term from 1 July 2027.
2. Chart of the share of the workforce's mesotheliomas diagnosed by years after first exposure, each setting from 40 to 70 marked with its share, the nine-in-ten line drawn and the 60-year setting highlighted, under "How the shares were read".

### review_horizon_workbook_2027.xlsx

1. Share of the workforce's mesotheliomas diagnosed within each setting, per cent to one decimal:
   - 40 years: 32.1%
   - 45 years: 53.9%
   - 50 years: 72.4%
   - 55 years: 85.1%
   - 60 years: 93.3%
   - 65 years: 97.4%
   - 70 years: 99.1%
2. Members reviewed in 2025-26 with fewer years than the setting since first exposure on 1 July 2027:
   - 45 years: 355
   - 50 years: 1,457
   - 55 years: 3,272
   - 60 years: 5,286
   - 65 years: 6,685
   - 70 years: 7,340
3. Reviews the Mobile Review Unit held in each town in 2025-26:
   - Brinalong: 327
   - Corrinbar: 399
   - Dorrabee: 128
   - Fenalong: 93
   - Garrock: 84
   - Haskesford: 71
   - Kellowie: 116
   - Lathardine: 64
   - Ostlebury: 78
   - Pellandra: 109
   - Quillerton: 193
   - Strathowie: 127
   - Tarramore: 79
   - Wennobank: 55
