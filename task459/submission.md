## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics.
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Pay the 2027 in-home support budget of USD 14,630,000 as Coconino Home Support Services USD 1,002,560, Yavapai Senior In-Home Care USD 2,920,730, Rim Country Visiting Nurses Association USD 1,380,661, Valley Home Support Partners USD 4,674,222, Pinal Community Home Care USD 1,388,566, Desert Willow Caregivers of Southern Arizona USD 2,283,097 and River Region Home Health Cooperative USD 980,164.**
Each amount is the budget's share of the 11,105 Covered Members counted in the agency's region, where the plan's 2025 claims place each member on the most days. Not the address on file or the assigned primary care practice, which stay at the high-country homes that members who winter in the low desert leave from October to May. Not a count of claims or of days with a claim, which weights the summer months those members spend at home with their regular doctors.

## 2. Critical Components

1. Covered Members (enrolled on every day of 2025, aged 75 or over on 31 December 2025): **11,105**
2. Covered Members by 2025 region: Coconino **761**, Yavapai **2,217**, Rim Country **1,048**, Maricopa **3,548**, Pinal **1,054**, Southern Arizona **1,733**, Colorado River **744**

## 3. Step-by-Step Solution

1. Kept the members in sc_member_extract_20260102.csv whose spans in sc_enrollment_spans_20260102.csv cover every day of 2025 and who were 75 or over on 31 December 2025 (Schedule B, B.3): 11,105 Covered Members.
2. Placed each 2025 line in med_claims_svc2025_paid_thru_20260630.csv at the rendering practice's county on the date of service (provider_directory_20261001.xlsx, with provider_location_changes_2025.csv for practices that moved) and that county's region under B.1, leaving out place of service 81 (the reference laboratory bills from Phoenix) and telehealth (02 and 10).
3. Added each paid fill in pbm_claims_2025_PVHP.txt (cardholder PV plus the member number) at its Arizona pharmacy's region in pharmacy_network_2025.csv, mail-order and specialty pharmacies being out of state, and each visit in ihs_visit_claims_2025.csv at its agency's region.
4. Gave every day of 2025 the region of the member's nearest dated place and counted each Covered Member in the region holding the most days (B.4): the counts in block 2.
5. Multiplied USD 14,630,000 by each region's share of Covered Members, rounded to the nearest dollar (B.5): the allocations in block 1.
6. For members aged 65 to 74 on 31 December 2025, applied replacements and voids in ihs_visit_claims_2025.csv, chained claims for the same member, agency and date where one period starts as the previous ends into one Visit (B.7), and counted Visits by agency (AGENCY_NAME in the provider directory) and quarter, with their average minutes: block 4.
7. For the same members, summed PAID_AMT in med_claims_svc2025_paid_thru_20260630.csv net of replacements and voids by the region of the rendering practice on the date of service: block 4.
8. Recommend the allocations in block 1 for the 2027 agreements.

## 4. Deliverable Answers

### member_regions_2025.csv

1. One row per Covered Member, 11,105 rows, each with its 2025 region and its 2027 agency; region counts as in block 2.

### home_care_allocation_2027.pdf

1. 2027 allocations to the nearest dollar, with the Covered Members behind each:
   - Coconino Home Support Services (Coconino): USD 1,002,560, 761 Covered Members
   - Yavapai Senior In-Home Care (Yavapai): USD 2,920,730, 2,217 Covered Members
   - Rim Country Visiting Nurses Association (Rim Country): USD 1,380,661, 1,048 Covered Members
   - Valley Home Support Partners (Maricopa): USD 4,674,222, 3,548 Covered Members
   - Pinal Community Home Care (Pinal): USD 1,388,566, 1,054 Covered Members
   - Desert Willow Caregivers of Southern Arizona (Southern Arizona): USD 2,283,097, 1,733 Covered Members
   - River Region Home Health Cooperative (Colorado River): USD 980,164, 744 Covered Members
2. 2025 Visits by members aged 65 to 74, by calendar quarter:
   - Coconino Home Support Services: Q1 42, Q2 283, Q3 326, Q4 210
   - Yavapai Senior In-Home Care: Q1 205, Q2 468, Q3 497, Q4 371
   - Rim Country Visiting Nurses Association: Q1 136, Q2 231, Q3 249, Q4 156
   - Valley Home Support Partners: Q1 539, Q2 1,323, Q3 1,411, Q4 1,016
   - Pinal Community Home Care: Q1 141, Q2 281, Q3 291, Q4 184
   - Desert Willow Caregivers of Southern Arizona: Q1 189, Q2 500, Q3 515, Q4 358
   - River Region Home Health Cooperative: Q1 56, Q2 217, Q3 202, Q4 124
3. Average Visit length for those members, minutes to one decimal:
   - Coconino Home Support Services: 127.4
   - Yavapai Senior In-Home Care: 140.0
   - Rim Country Visiting Nurses Association: 120.5
   - Valley Home Support Partners: 140.8
   - Pinal Community Home Care: 140.8
   - Desert Willow Caregivers of Southern Arizona: 142.9
   - River Region Home Health Cooperative: 128.3
4. Plan-paid 2025 medical spend for those members by the region of the rendering practice on the date of service, USD thousands to one decimal:
   - Coconino: 259.7
   - Yavapai: 635.8
   - Rim Country: 311.5
   - Maricopa: 1,136.1
   - Pinal: 325.6
   - Southern Arizona: 574.6
   - Colorado River: 220.1
5. Bar chart of the 2027 allocation by agency with the Covered Members counted in each region (Figure 1).
