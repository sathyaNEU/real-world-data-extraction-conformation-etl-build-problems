## Tags

**Domain:** Banking, Credit & Financial Risk, credit scoring and PD modelling.
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**About 250 of the 2,400 Libranza Empresarial loans disbursed on 1 February 2027 will go into default by 31 January 2028.**
A payroll-deduction loan defaults almost only when its borrower stops being paid by the payroll with the loan open, 53 per cent of such public loans went into default, and the agreement employers' staff with a year's service work their last month at about 3 per cent a month. Not the 50 a PD model on the public book's borrower attributes gives, which reads the public servants' rare leaving as borrower quality.

## 2. Critical Components

1. Of the public loans whose borrower stopped being paid by the payroll with the loan open, **53 per cent** went into default.
2. Staff with a year's service at the employers of the launch loans work their last month at about **3 per cent** a month.

## 3. Step-by-Step Solution

1. Joined payroll_loans_public_2017_2026.csv, treasury_deduction_returns_2017_2026.csv (legacy numbers through legacy_core_crosswalk_2021.csv) and default_register_2017_2026.csv; marked the first month of each run of SIN SALARIO (01) returns on a loan, the month the Tesoreria stopped paying the borrower with the loan open.
2. For runs starting January 2017 to December 2025, took the share of those loans whose default date falls within each number of months of that first month: 53 per cent by five months, none before three, the conversion by months left.
3. Took the monthly default rate of loans still paid by the payroll (defaults with no SIN SALARIO run before them, per loan-month) as the on-payroll route.
4. From employer_payroll_registers_2025_2026.csv (repeated uploads dropped, employee ids without the CC prefix and dots), took each employer's monthly rate of staff with twelve or more months' service working their last month (the LIQUIDACION row), over employee-months since its first register.
5. For each loan in libranza_empresarial_disbursement_file_2027-02-01.csv, summed over February 2027 to January 2028 the chance its borrower leaves at the end of each month times the conversion for the months then left, plus the on-payroll route; by sector through deduction_agreements_register.xlsx.
6. Savings in savings_contribution_schedules_2025_2026.csv: where an employer filed a second schedule for a month with the same members, only the later counts, and a schedule for members missing from the month adds to it; received from collection_account_statement_2025_2026.csv, a returned transfer counted once, a group parent's single transfer paying its own and its subsidiary's schedules of the month (its amount is their sum).
7. Recoveries in defaulted_loan_receipts_2023_2026.csv on the loans whose default date in default_register_2017_2026.csv falls in 2023 or 2024, net of reversals, leaving out transfers from the borrowing member's own account in member_savings_ledger_2023_2026.csv (another member's savings account paying is a recovery), by unit_type in payroll_loans_public_2017_2026.csv.
8. Recommendation: about 250 of the 2,400 loans in default by 31 January 2028.

## 4. Deliverable Answers

### libranza_empresarial_default_forecast.xlsx

1. Libranza Empresarial loans in default by 31 January 2028: 250.
2. Share of each sector's launch loans in default by 31 January 2028, nearest 5 per cent:
   - Contact centres: 20 per cent
   - Retail chains: 10 per cent
   - Security services: 10 per cent
   - Logistics and courier: 10 per cent
   - Food processing: 10 per cent
   - Private clinics: 5 per cent
3. Members' savings contributions the employers deducted for the months of 2026, VMP to the nearest 1,000:
   - Contact centres: VMP 793,629,000
   - Retail chains: VMP 521,966,000
   - Security services: VMP 572,968,000
   - Logistics and courier: VMP 444,405,000
   - Food processing: VMP 547,196,000
   - Private clinics: VMP 474,370,000
4. Of that, not received by 31 December 2026, VMP to the nearest 1,000:
   - Contact centres: VMP 79,019,000
   - Retail chains: VMP 46,902,000
   - Security services: VMP 51,867,000
   - Logistics and courier: VMP 37,041,000
   - Food processing: VMP 51,328,000
   - Private clinics: VMP 38,066,000
5. Recovered by 31 December 2026 other than by netting the member's own savings, VMP to the nearest 1,000:
   - Defaulted in 2023, national: VMP 561,001,000
   - Defaulted in 2023, territorial: VMP 247,085,000
   - Defaulted in 2023, health: VMP 86,931,000
   - Defaulted in 2023, education: VMP 222,767,000
   - Defaulted in 2024, national: VMP 759,670,000
   - Defaulted in 2024, territorial: VMP 412,827,000
   - Defaulted in 2024, health: VMP 147,806,000
   - Defaulted in 2024, education: VMP 175,862,000

### launch_default_note.docx

1. The forecast for the board: about 250 of the 2,400 loans in default by 31 January 2028, with the reason (leaving the payroll with the loan open, far more frequent at the agreement employers).
2. Bar chart of the expected share in default by sector against the public loans' first-year rate.
