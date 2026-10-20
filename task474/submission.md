## Tags

**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: a Medicaid managed care plan's paid medical cost per member-month by primary care group).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate four of the twelve primary care groups for the 2027 Cost Performance Program: PG04, PG07, PG08 and PG10.**
Each group's paid medical cost per member-month for January to June 2026 is $412.00 or more once the member-months are the months its members were covered rather than the months the roster lists. The roster is the state's enrollment as processed by the 5th of each month: members who lost coverage at renewal and were reinstated back to the lapse are missing from the months they were later covered for, and members who died stay on it for months the state later took its capitation back for. The member-level lines of the state's capitation remittance record both. Counted on the roster alone, the groups with the most renewal churn look costlier and the groups with the most deaths look cheaper, and the designation would be PG02, PG04, PG08 and PG11.

## 2. Critical Components

1. Groups at or above $412.00 per member-month: **4** of 12.
2. Member-months: **135,979** covered, against **133,893** on the roster; **3,009** member-months added from the remittance's reinstatement lines and **923** roster member-months removed for recoupments.

## 3. Step-by-Step Solution

1. Took every group in provider_group_register_2026.xlsx (rule 2.1) and each member's group from pcp_group_id in enrollment_roster_2026h1.csv, roster_month 2026-01 to 2026-06.
2. Took the lines of capitation_remittance_2026.csv with a medicaid_id and a coverage_month from 2026-01 to 2026-06, mapped each medicaid_id to its member_id through the roster, and summed member_count per member and coverage month (a rate cell correction's two lines net to zero).
3. Covered member-months: the roster's member-months, plus each member and month netting above zero that the roster does not list, less each roster member-month netting below zero (rule 2.2).
4. Summed paid_amount in medical_claims_paid_2026h1.csv over claims with service_from from 2026-01-01 to 2026-06-30 and paid_date by 2026-10-31, by the member's group.
5. Divided each group's paid cost by its covered member-months and designated every group at $412.00 or more (rule 2.3): PG04, PG07, PG08 and PG10.
6. For the pharmacy summary (rule 3.1), took each claim_number in pharmacy_claims_2026h1.csv at its line with the latest processed_at, kept those whose fill_date falls from 2026-01-01 to 2026-06-30, classed each by its ndc in drug_class_crosswalk.xlsx, summed paid_amount by class and counted the claims whose latest line paid more than zero as fills.

## 4. Deliverable Answers

### provider_group_pmpm_2026h1.xlsx

1. Every primary care group, designated or not:
   - PG01: not designated
   - PG02: not designated
   - PG03: not designated
   - PG04: designated
   - PG05: not designated
   - PG06: not designated
   - PG07: designated
   - PG08: designated
   - PG09: not designated
   - PG10: designated
   - PG11: not designated
   - PG12: not designated
2. Every drug class, paid pharmacy cost (dollars, nearest dollar) and fills, January to June 2026:
   - ACE inhibitors: $48,665; 4,966 fills
   - Anticonvulsants: $275,874; 4,508 fills
   - Atypical antipsychotics: $659,407; 2,868 fills
   - Beta blockers: $38,676; 4,504 fills
   - Inhaled corticosteroids: $854,903; 4,576 fills
   - Insulins: $1,121,414; 2,742 fills
   - Metformin: $41,339; 5,580 fills
   - Opioid analgesics: $87,004; 4,104 fills
   - Proton pump inhibitors: $65,412; 5,012 fills
   - SSRIs: $96,219; 6,787 fills
   - Statins: $85,249; 7,276 fills
   - Thyroid hormones: $44,548; 3,415 fills

### provider_group_designations_2027.pdf

1. The designated groups: PG04, PG07, PG08 and PG10.
2. Bar chart of every group's paid medical cost per member-month, January to June 2026, against the $412.00 benchmark line, the designated groups' bars in orange.
