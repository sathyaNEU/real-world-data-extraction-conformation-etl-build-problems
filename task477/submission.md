## Tags

**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production: pay-date calendar effects in quarterly covered wages).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Name Information (22%), Finance and insurance (21%), Professional, scientific, and technical services (19%) and Construction (19%) as the 2027 to 2029 sector-partnership slate; Manufacturing (18%) is next in line.**
These are the four eligible industries with the fastest growth in pay per job from 2021 to 2025 for the work done in each year. Not Transportation and warehousing and Health care and social assistance, which wages as paid put on the slate (20% and 20%): 2025 carried an extra Thursday pay date (1 January 2026 paid on 31 December 2025) for the payrolls run on Thursdays, which these two industries largely are, so their 2025 wages hold more than a year's work.

## 2. Critical Components

1. Growth in pay per job, 2021 to 2025, for the work done: Transportation and warehousing **18%**, Health care and social assistance **18%**, Professional, scientific, and technical services **19%** and Construction **19%**.
2. Eligible industries (2025 annual average jobs of 1,000 or more): **15**.

## 3. Step-by-Step Solution

1. Took Tallis County's (52037) private sector rows (own_code 5, agglvl_code 74) from qcew_state52_county_2013_2019.csv, qcew_state52_county_2020_2025q3.csv and qcew_state52_county_2025_annual_release.csv, using the annual release for 2025 in place of the first-published quarters; 15 sectors had 2025 annual average jobs (the mean of the twelve monthly levels) of 1,000 or more (guidelines 2.1).
2. Counted each quarter's pay dates on four every-other-week phases (Fridays from 1 and 8 January 2021, Thursdays from 7 and 14 January 2021; a weekly payroll pays on both phases of its weekday), a date falling on a weekend or federal holiday paid the business day before, since qcew_county_file_layout_and_notes.pdf counts wages in the quarter paid.
3. For each eligible industry, regressed the log of quarterly wages per job (total_qtrly_wages over the mean of the three monthly levels), 2013 to 2025, on year and quarter effects and the four counts; each coefficient times 6.52 (the biweekly pay dates in an average quarter) is that phase's share of the payroll.
4. Divided each industry's 2021 and 2025 wages by 1 plus the sum over phases of share times (pay dates in the year times 14 over 365, less 1), then by annual average jobs, and took 2025 over 2021 less 1 (guidelines 2.2): Information 22%, Finance and insurance 21%, Professional, scientific, and technical services 19%, Construction 19%, Manufacturing 18%, Transportation and warehousing 18%, Health care and social assistance 18%, Wholesale trade 17%, Accommodation and food services 17%, Retail trade 15%, Administrative and support and waste services 15%, Other services 14%, Arts, entertainment, and recreation 14%, Educational services 13% and Real estate and rental and leasing 13%.
5. Counted each 2025 exiter in wioa_exits_2025.csv once, at the last exit; took wages above zero in the second quarter after that exit from ui_wage_match_return_2025q3_2026q2.csv; mapped a row reported under a professional employer organization's account to the client business through ui_acct and rptg_unit against peo_client_registrations_2025.csv (peo_acct, client_seq); kept the business paying the most and its NAICS sector in ui_employer_accounts_extract_2026-08.csv (manual 4.3): 753 exiters in eligible industries.
6. Took the checks in fiscal_agent_check_register_2025_2026.csv issued in 2025 and not voided, joined each to its lines in ita_voucher_ledger_2025.csv by check_no, valued each line at voucher_amount over of_installments (the last installment taking the cents left over, so a check's lines sum to its amount), and summed by the program's target industry in etpl_programs_2025.xlsx (guidelines 3.3): $876,413.
7. Named the four eligible industries with the highest growth (guidelines 2.3) and the fifth as next in line: Information, Finance and insurance, Professional, scientific, and technical services and Construction; next Manufacturing.

## 4. Deliverable Answers

### sector_partnership_application_2027.csv

1. One row per eligible industry, in order of growth: growth in pay per job 2021 to 2025 (whole percent), on the slate, 2025 exiters employed in the second quarter after exit, 2025 ITA payments (nearest dollar):
   - Information (51): 22%; on the slate; 13 exiters; $75,692
   - Finance and insurance (52): 21%; on the slate; 14 exiters; $102,142
   - Professional, scientific, and technical services (54): 19%; on the slate; 33 exiters; $32,442
   - Construction (23): 19%; on the slate; 46 exiters; $39,704
   - Manufacturing (31-33): 18%; not on the slate; 93 exiters; $55,792
   - Transportation and warehousing (48-49): 18%; not on the slate; 67 exiters; $40,206
   - Health care and social assistance (62): 18%; not on the slate; 153 exiters; $69,275
   - Wholesale trade (42): 17%; not on the slate; 33 exiters; $81,488
   - Accommodation and food services (72): 17%; not on the slate; 62 exiters; $46,835
   - Retail trade (44-45): 15%; not on the slate; 101 exiters; $113,010
   - Administrative and support and waste services (56): 15%; not on the slate; 61 exiters; $33,025
   - Other services (81): 14%; not on the slate; 24 exiters; $31,850
   - Arts, entertainment, and recreation (71): 14%; not on the slate; 19 exiters; $37,175
   - Educational services (61): 13%; not on the slate; 22 exiters; $26,554
   - Real estate and rental and leasing (53): 13%; not on the slate; 12 exiters; $91,223

### sector_partnership_slate_2027.docx

1. The slate for the board's vote: Information, Finance and insurance, Professional, scientific, and technical services and Construction; next in line Manufacturing.
2. Horizontal bar chart of every eligible industry's growth in pay per job, 2021 to 2025, each bar labelled with its whole percent, the slate's four bars darker.
3. The application table by industry with the same growth, exiter and ITA figures as sector_partnership_application_2027.csv.
