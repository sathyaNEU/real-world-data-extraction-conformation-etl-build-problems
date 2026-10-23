## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a state outcomes release of campus-by-cohort earnings cells and a workforce board's employer-quarter wage records, conformed with a four-campus college's completion extracts, grant roster and program inventory into the board's workforce value designation file).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Larkspur Basin Community College's workforce value designation lapses for the 2027-28 Career Training Grant year: 71 per cent of the 2024-25 completers of its tested programs (1,021 of 1,441) are in passing programs, under the 75 per cent the standard needs.**
Medical Assisting's completers earn a median 33 thousand dollars, under the 34.2 thousand benchmark, and 63 per cent of the Commercial Driver License program's grant completers were working on day 180, under 70. Not 84 per cent: averaging each program's campus-by-cohort medians puts Medical Assisting at 36 thousand, and counting any pay in the quarter holding day 180 puts the CDL program at 91 per cent, though 22 of its 79 grant completers had left their first carrier weeks before day 180 or started at the next weeks after it, inside that quarter.

## 2. Critical Components

1. Medical Assisting's median earnings, its six campus-by-cohort cells pooled, are **33** thousand dollars; its cells' medians averaged by completers give 36.
2. The CDL program's day-180 figure is **63** per cent (50 of 79 grant completers working); pay from any employer in the quarter gives 91.
3. Either correction alone keeps the designation: **77** per cent with the pooled medians and quarter pay, **78** with the averaged medians and the dated jobs.
4. The programs that fail on earnings: Child Development, Criminal Justice, Culinary Arts and Medical Assisting. On placement: Commercial Driver License, Class A; Emergency Medical Technician; and Medical Coding.

## 3. Step-by-Step Solution

1. Joined every program through larkspur_program_inventory_2025-26.xlsx (both student systems' program codes, the grant's program IDs, and the CIP codes Information Technology and Criminal Justice carried before fall 2022) and took the three-years-after cells for award year 2020-21 from postsecondary_earnings_outcomes_2024_edition.xlsx and 2021-22 from postsecondary_earnings_outcomes_2025_edition.csv, the 2024 earnings times 1.0294; Paralegal Studies' cells are suppressed, so it is not tested.
2. Rebuilt each cell's earnings distribution by joining its five percentiles straight, pooled the cells by completers with earnings and solved for the point where the pooled share reaches half: each credit program's median.
3. Took the grant completers from ctg_participant_roster_2023-2026.csv (exit reason Completed, sections ending 1 July 2024 to 30 June 2025; Forklift and Material Handling has 18, under 20, and is not tested) and day 180 as the section's last day plus 180 days.
4. In ctg_participant_wage_records_2022q3-2026q2.csv kept the latest report for each participant, employer and quarter, and counted a completer as working when a job paid in the quarter holding day 180 was paid in the quarters before and after too, or when its start (paid in the next quarter only) or its exit (paid in the one before only) dated from its pay in the quarter against its pay in its adjacent full quarter falls on the working side of day 180.
5. Counted each program's 2024-25 completers in fennimore_ridgefield_completions_2024-25.xlsx and copper_flats_antelope_springs_completions_2024-25.csv, grant participants or not, and took the share of the tested programs' 1,441 completers in passing programs: 1,021, 71 per cent.
6. For the grant tuition, took the board's payments to the college in ctg_provider_payments_fy2024-fy2026.csv dated 1 July 2024 to 30 June 2025 and split each by its invoice's lines in larkspur_ctg_invoice_register_2023-2026.xlsx: tuition and the section fee (once per section, though the board's line export from January 2025 carries it on every participant's line) to the section's program, each refund credit to the program of the participant it refunds (the roster), not the invoice that carried it.
7. For the loan principal, joined each credit program's 2024-25 completers by state student ID to larkspur_direct_loan_disbursements_2019-2026.csv, kept subsidized and unsubsidized disbursements with returns netted, and grossed the aid system's amounts from 1 July 2023 back up by the 1.057 per cent origination fee they are net of (larkspur_cost_of_attendance_2024-25.pdf); the median to the nearest 10 dollars.

## 4. Deliverable Answers

### larkspur_workforce_value_2027-28.xlsx

1. The call: the designation lapses for 2027-28.
2. Each credit program's earnings figure, whole thousands of dollars:
   - Automotive Technology: 44
   - Business Administration: 40
   - Child Development: 28
   - Criminal Justice: 27
   - Culinary Arts: 28
   - Diesel Technology: 52
   - Information Technology: 50
   - Medical Assisting: 33
   - Paralegal Studies: not tested (no published cell)
   - Radiologic Technology: 65
   - Registered Nursing: 71
   - Welding Technology: 47
3. Each short-term program's placement figure, whole per cent:
   - Commercial Driver License, Class A: 63
   - Emergency Medical Technician: 44
   - Forklift and Material Handling: not tested (18 grant completers)
   - HVAC Fundamentals: 92
   - IT Support Specialist: 83
   - Medical Coding: 50
   - Nursing Assistant: 91
   - Pharmacy Technician: 87
   - Phlebotomy Technician: 88
   - Warehouse and Logistics Technician: 90
   - Welding Fundamentals: 90
4. The programs that fail: Child Development; Criminal Justice; Culinary Arts; Medical Assisting; Commercial Driver License, Class A; Emergency Medical Technician; and Medical Coding.
5. The share of the 2024-25 completers of tested programs in passing programs: 71 per cent (1,021 of 1,441).
6. Each short-term program's grant tuition and fees the board paid in its July 2024 to June 2025 fiscal year, whole dollars:
   - Commercial Driver License, Class A: 388,825
   - Emergency Medical Technician: 116,900
   - Forklift and Material Handling: 7,470
   - HVAC Fundamentals: 121,920
   - IT Support Specialist: 177,545
   - Medical Coding: 118,900
   - Nursing Assistant: 136,560
   - Pharmacy Technician: 137,840
   - Phlebotomy Technician: 48,820
   - Warehouse and Logistics Technician: 81,300
   - Welding Fundamentals: 219,040
7. Each credit program's median Direct Loan principal among its 2024-25 completers who borrowed, nearest 10 dollars:
   - Automotive Technology: 14,830
   - Business Administration: 12,740
   - Child Development: 12,000
   - Criminal Justice: 12,000
   - Culinary Arts: 11,500
   - Diesel Technology: 10,660
   - Information Technology: 11,070
   - Medical Assisting: 7,750
   - Paralegal Studies: 3,580
   - Radiologic Technology: 16,040
   - Registered Nursing: 14,750
   - Welding Technology: 12,240

### larkspur_program_tests_2027-28.svg

8. Two bar panels, one bar per tested program, each labelled with its figure: the 11 credit programs' median earnings in thousands of dollars against a dashed line at 34.2, and the 10 short-term programs' day-180 shares against a dashed line at 70 per cent; passing programs in blue, failing in orange; the title states the call and the 71 per cent share.
