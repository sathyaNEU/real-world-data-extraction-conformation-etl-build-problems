## Tags

**Domain:** Survey Research & Official Statistics, nonresponse, calibration and measurement-error adjustment (price collection quality assurance).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Place Halbrook North, Tamsin Bay, Fenwick and Westholm under corrective action, put Belmont Valley on a $1,775 service credit with corrective action, and assess the other nine regions as compliant.** Belmont Valley's estimated collection accuracy is 95 per cent, the only region below the 96.0 per cent band. Not the raw agreement between collector and Field Quality Team prices, which counts every price an outlet changed between the visit and the re-collection days later as a collector's error and would put seven compliant regions under corrective action and three corrective regions on credits ($7,049).

## 2. Critical Components

1. The Field Quality Team re-collected **6,260** prices it found on the shelf; the share whose re-collected price differs from the collector's runs from **1.1 per cent** in Halbrook Central to **7.1 per cent** in Belmont Valley.
2. Net of the chance that each item's shelf price changed between the visit and its re-collection, Belmont Valley's collection accuracy is **95 per cent** and Halbrook North, Tamsin Bay, Fenwick and Westholm each sit at **97 per cent**.
3. The service credit is 4 per cent of Belmont Valley's quarterly collection fee of $44,380: **$1,775**.

## 3. Step-by-Step Solution

1. Read pcqs_price_collection_quality_standard_v3.pdf: accuracy is the share of recorded prices that were the shelf price when the collector recorded it (3.1), estimated from the back-checks (3.2) and set against 98.0 and 96.0 per cent without rounding (3.3, section 4).
2. Took the back-checked prices the officer found from the three monthly sheets of fqt_backcheck_register_2026q3.xlsx (6,260 prices) and compared each collector price with the FQT price.
3. Dated each collector's visit from tallis_visit_log_2026-07_2026-09.csv (the local date of started), joined through cpi_outlet_register_2026-10.xlsx (outlet code to contractor outlet no.), and took each back-check's delay in calendar days to its Re-collected on date.
4. From cpi_field_quotes_2025-10_2026-09.csv, one row per quote and month with statuses read through handheld_status_codes.csv, took each COICOP class's monthly frequency of price change at multiples and at independents (outlet type in the register) over consecutive months priced on the same variety.
5. Gave each back-check its chance of no shelf-price change, (1 minus that frequency) to the power delay/30.4, and estimated each region's accuracy as its agreeing back-checks over the sum of those chances.
6. Applied section 4 and pcsa_schedule4_collection_fees.pdf: Belmont Valley service credit of $1,775, Halbrook North, Tamsin Bay, Fenwick and Westholm corrective action, the other regions compliant.
7. Timeliness and missed visits: took the scheduled visits in tallis_collection_schedule_2026q3.csv, followed each Lifeline Chemists branch closed on 31 July to the CareMed Pharmacy outlet in the register at the same address (its quotes continue there in the price database), and counted a visit completed when every visit row with prices for the outlet in the month fell from the index day to the fourth working day after it in nso_collection_calendar_2026.csv (17 August a holiday); a schedule row with no visit row is a missed visit.
8. Replacement acceptance: took the quarter's replacement rows (status R or 30) from the price database, gave each decision in commodity_replacement_decisions_2026.xlsx to the latest replacement of its quote visited before the decision date, and counted a replacement accepted when its latest Comparable or Not comparable decision is Comparable.

## 4. Deliverable Answers

### pcqs_2026q3_assessment.xlsx

1. One row per region, outcome, timeliness (per cent), missed visits and replacement acceptance (per cent):
   - CR01 Halbrook Central: Compliant, timeliness 96.3, missed visits 1, replacement acceptance 68.4
   - CR02 Halbrook North: Corrective action, timeliness 95.8, missed visits 1, replacement acceptance 63.2
   - CR03 Halbrook South: Compliant, timeliness 95.1, missed visits 2, replacement acceptance 80.0
   - CR04 Eastwick Coast: Compliant, timeliness 92.8, missed visits 0, replacement acceptance 62.5
   - CR05 Belmont Valley: Service credit, timeliness 92.8, missed visits 1, replacement acceptance 76.9
   - CR06 Harlow Plains: Compliant, timeliness 97.0, missed visits 0, replacement acceptance 60.0
   - CR07 Tamsin Bay: Corrective action, timeliness 95.5, missed visits 1, replacement acceptance 88.9
   - CR08 Greywater: Compliant, timeliness 95.8, missed visits 0, replacement acceptance 46.2
   - CR09 Ardmore Uplands: Compliant, timeliness 95.0, missed visits 0, replacement acceptance 42.9
   - CR10 Fenwick: Corrective action, timeliness 97.0, missed visits 0, replacement acceptance 78.6
   - CR11 Corran Peninsula: Compliant, timeliness 95.5, missed visits 1, replacement acceptance 65.0
   - CR12 Westholm: Corrective action, timeliness 98.4, missed visits 1, replacement acceptance 66.7
   - CR13 Rookby Downs: Compliant, timeliness 93.7, missed visits 1, replacement acceptance 64.3
   - CR14 Northreach: Compliant, timeliness 91.3, missed visits 0, replacement acceptance 66.7
2. Service credit for the quarter: $1,775.

### pcqs_2026q3_contractor_letter.pdf

1. Outcomes: corrective action for Halbrook North, Tamsin Bay, Fenwick and Westholm; service credit and corrective action for Belmont Valley; the other nine regions compliant.
2. Service credit: $1,775.
3. Chart on page 1: a horizontal bar for each region's estimated collection accuracy, coloured by outcome, with the 98.0 and 96.0 per cent bands marked.
