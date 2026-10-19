## Tags

**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: two pharmacy benefit managers' specialty claim files conformed into one repriced record of fills, from which each class's program-year spend for the members now on therapy is projected).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Staff the Specialty Clinical Pharmacy Program with 48 clinical pharmacists for July 2026 to June 2027: Inflammatory conditions (biologic and targeted therapy) 13; Multiple sclerosis 7; Oral oncology 5; Hepatitis C 1; Weight management (GLP-1 receptor agonists) 5; HIV 6; Severe asthma (biologics) 4; Cystic fibrosis 4; Migraine prevention (CGRP) 3.**
Each class's managed spend is its members on therapy on June 30, 2026 carried forward by the class's own spend and continuation at each month on therapy, starting each member at the months they have already completed. Not last year's on-therapy members' following-year spend applied to this June's members, which gives weight management 7, severe asthma 5 and migraine prevention 4 (their 2026 members are new starters after the step therapy change, most of whom stop within months); not the class's spend from first fill, which gives oral oncology 3 (its members on therapy have already passed the early discontinuation); not the trailing year or the June run-rate, which give hepatitis C 4 (its courses end within twelve weeks).

## 2. Critical Components

1. Members on therapy on June 30, 2026 (the caseloads): IMM 433; MS 186; ONC 89; HCV 61; GLP 1,603; HIV 381; AST 220; CF 39; CGR 738.
2. Projected managed spend for the program year, $ million at the 2026 schedule: IMM 19; MS 10; ONC 7; HCV 0; GLP 7; HIV 8; AST 5; CF 5; CGR 4; total 65.
3. Pharmacists at one per $1.5 million of managed spend or part: IMM 13; MS 7; ONC 5; HCV 1; GLP 5; HIV 6; AST 4; CF 4; CGR 3; total 48.

## 3. Step-by-Step Solution

1. Conformed orrin_rx_specialty_claims_2019_2025.csv and tallis_specialty_claims_2026h1.csv into one record of fills: reversed claims removed with the claims they reverse (Orrin's REVERSAL lines, Tallis's R status), members linked to plan IDs through member_id_crosswalk_2026.csv, Orrin's 10-digit NDCs padded to 11 digits, each NDC's class from tallis_specialty_drug_list_2026.csv.
2. Priced every fill at tallis_specialty_price_schedule_2026.xlsx: units times the unit price plus the dispensing fee (charter 2.2).
3. Took each class's caseload: members with a fill whose days' supply reaches June 30, 2026 (charter 2.1).
4. Dated each member's therapy from the first fill in the class; members already filling in the first quarter of 2019 have an unseen start and sit in the longest-duration cell.
5. For each class and each month on therapy, averaged the spend over the following twelve months of the members on therapy at a month end at that duration, over every month end from January 2019 whose twelve months are in the record (durations from 36 months pooled).
6. Projected each caseload member at the duration they had reached on June 30, 2026, summed by class, and staffed one pharmacist per $1.5 million or part (charter 3.1).
7. For the rebates, summed orrin_rx_rebate_statement_2025.xlsx's lines with a 2025 utilization quarter, each product's rebate for a quarter counted once although the statement repeats it on each channel line.

## 4. Deliverable Answers

### merrow_specialty_pharmacist_staffing_2026_27.xlsx

1. Clinical pharmacists by class:
   - Inflammatory conditions (biologic and targeted therapy): 13
   - Multiple sclerosis: 7
   - Oral oncology: 5
   - Hepatitis C: 1
   - Weight management (GLP-1 receptor agonists): 5
   - HIV: 6
   - Severe asthma (biologics): 4
   - Cystic fibrosis: 4
   - Migraine prevention (CGRP): 3
2. Total: 48 pharmacists.
3. Managed spend for July 2026 to June 2027, $ million:
   - Inflammatory conditions (biologic and targeted therapy): 19
   - Multiple sclerosis: 10
   - Oral oncology: 7
   - Hepatitis C: 0
   - Weight management (GLP-1 receptor agonists): 7
   - HIV: 8
   - Severe asthma (biologics): 5
   - Cystic fibrosis: 5
   - Migraine prevention (CGRP): 4
4. Manufacturer rebates on 2025 utilization, $ thousand:
   - Inflammatory conditions (biologic and targeted therapy): 4,735
   - Multiple sclerosis: 1,690
   - Oral oncology: 340
   - Hepatitis C: 1,226
   - Weight management (GLP-1 receptor agonists): 760
   - HIV: 754
   - Severe asthma (biologics): 722
   - Cystic fibrosis: 183
   - Migraine prevention (CGRP): 606
5. Bar chart of the pharmacists by class, on the Staffing sheet.
