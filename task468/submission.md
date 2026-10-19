## Tags

**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: two pharmacy benefit managers' specialty claim files conformed into one repriced record of fills, from which each class's program-year spend for the members now on therapy is projected).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Staff the Specialty Clinical Pharmacy Program with 54 clinical pharmacists for July 2026 to June 2027: Inflammatory conditions (biologic and targeted therapy) 14; Multiple sclerosis 7; Oral oncology 6; Hepatitis C 1; Weight management (GLP-1 receptor agonists) 7; HIV 6; Severe asthma (biologics) 4; Cystic fibrosis 4; Migraine prevention (CGRP) 5.**
Each class's managed spend is its members on therapy on June 30, 2026 carried forward by the class's own spend and continuation at each month of an episode of therapy, starting each member at the months their current episode has run; a member back on a drug after a lapse of more than 60 days starts a new episode. Not the same projection counted from each member's first fill in the class, which gives weight management 8, severe asthma 5 and migraine prevention 6 (57 in all), because the members who came back to those drugs in 2026 after the step therapy change would be projected like the long-standing members who never stopped; not last year's on-therapy members' following-year spend applied to this June's members, which gives weight management 10; not the trailing year, which gives hepatitis C 4 (its courses end within twelve weeks).

## 2. Critical Components

1. Members on therapy on June 30, 2026 (the caseloads): IMM 484; MS 192; ONC 104; HCV 52; GLP 1,846; HIV 370; AST 287; CF 43; CGR 941.
2. Projected managed spend for the program year, $ million at the 2026 schedule: IMM 20; MS 10; ONC 8; HCV 0; GLP 10; HIV 8; AST 5; CF 5; CGR 7; total 73.
3. Pharmacists at one per $1.5 million of managed spend or part: IMM 14; MS 7; ONC 6; HCV 1; GLP 7; HIV 6; AST 4; CF 4; CGR 5; total 54.

## 3. Step-by-Step Solution

1. Conformed orrin_rx_specialty_claims_2019_2025.csv and tallis_specialty_claims_2026h1.csv into one record of fills: reversed claims removed with the claims they reverse (Orrin's REVERSAL lines, Tallis's R status), members linked to plan IDs through member_id_crosswalk_2026.csv, Orrin's 10-digit NDCs padded to 11 digits, each NDC's class from tallis_specialty_drug_list_2026.csv.
2. Priced every fill at tallis_specialty_price_schedule_2026.xlsx: units times the unit price plus the dispensing fee (charter 2.2).
3. Took each class's caseload: members with a fill whose days' supply reaches June 30, 2026 (charter 2.1).
4. Split each member's fills in a class into episodes of therapy, a new episode starting at a fill more than 60 days after every earlier supply had run out, and dated each member's months on therapy from the start of the episode; a member already filling in the first quarter of 2019 has an unseen start and sits in the longest-duration cell.
5. For each class and each month of an episode, averaged the spend over the following twelve months of the members on therapy at a month end at that month, over every month end from January 2019 whose twelve months are in the record (months from 36 on pooled).
6. Projected each caseload member at the month of the episode they had reached on June 30, 2026, summed by class, and staffed one pharmacist per $1.5 million or part (charter 3.1).
7. For the rebates, took orrin_rx_rebate_statement_2025.xlsx's contract quarters 2025-Q1 to 2025-Q4 (a contract year runs February to January, the only calendar on which its units tie to the claims), each product's quarterly rebate once although the statement repeats it on each channel line, plus January 2025's units at contract quarter 2024-Q4's rebate per unit.

## 4. Deliverable Answers

### merrow_specialty_pharmacist_staffing_2026_27.xlsx

1. Clinical pharmacists by class:
   - Inflammatory conditions (biologic and targeted therapy): 14
   - Multiple sclerosis: 7
   - Oral oncology: 6
   - Hepatitis C: 1
   - Weight management (GLP-1 receptor agonists): 7
   - HIV: 6
   - Severe asthma (biologics): 4
   - Cystic fibrosis: 4
   - Migraine prevention (CGRP): 5
2. Total: 54 pharmacists.
3. Managed spend for July 2026 to June 2027, $ million:
   - Inflammatory conditions (biologic and targeted therapy): 20
   - Multiple sclerosis: 10
   - Oral oncology: 8
   - Hepatitis C: 0
   - Weight management (GLP-1 receptor agonists): 10
   - HIV: 8
   - Severe asthma (biologics): 5
   - Cystic fibrosis: 5
   - Migraine prevention (CGRP): 7
4. Manufacturer rebates on fills dispensed in 2025, $ thousand:
   - Inflammatory conditions (biologic and targeted therapy): 5,328
   - Multiple sclerosis: 1,750
   - Oral oncology: 368
   - Hepatitis C: 1,209
   - Weight management (GLP-1 receptor agonists): 725
   - HIV: 724
   - Severe asthma (biologics): 744
   - Cystic fibrosis: 201
   - Migraine prevention (CGRP): 614
5. Bar chart of the pharmacists by class, on the Staffing sheet.
